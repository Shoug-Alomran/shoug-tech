#!/usr/bin/env python3
"""Repair academic slide-breakdown viewers from filesystem truth.

The authored breakdown HTML is authoritative.  If it exists, the wrapper must
show one correctly styled Open in New Tab action, must embed that HTML, and
must not retain a stale Coming Soon state.
"""

from __future__ import annotations

import html
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACADEMICS = ROOT / "docs" / "academics"
sys.path.insert(0, str(ROOT / "scripts"))
from slide_breakdown_utils import breakdown_source, slide_breakdown_roots  # noqa: E402

PRIMARY_BUTTON_RE = re.compile(
    r'<(?:a|span)\b(?=[^>]*class=["\'][^"\']*\bbtn-primary\b[^"\']*["\'])[^>]*>.*?</(?:a|span)>',
    re.I | re.S,
)
ACTION_DIV_RE = re.compile(r'<div\b[^>]*class=["\'][^"\']*\baction-buttons\b[^"\']*["\'][^>]*>', re.I)
EMBED_DIV_RE = re.compile(r'<div\b[^>]*class=["\'][^"\']*\bembed-area-wrapper\b[^"\']*["\'][^>]*>', re.I)
COMING_SOON_RE = re.compile(r'<div\b[^>]*class=["\'][^"\']*\bcoming-soon-panel\b[^"\']*["\'][^>]*>', re.I)
DIR_ROW_RE = re.compile(
    r'(<a\b[^>]*href="(?P<href>[^"]+/slide-breakdowns/(?P<slug>[^"]+)/?)"[^>]*class="[^"]*\bdir-row\b[^"]*"[^>]*>.*?'
    r'<span\b[^>]*class="[^"]*\bstatus-tag\b[^"]*"[^>]*>)(?P<status>[^<]*)(</span>)', re.I | re.S)

# Some newer course shells include a second plain-text "open" link in addition
# to the real .btn-primary action.  It is the source of the blue duplicate seen
# on ISC213.  Only remove links whose visible text is explicitly Open in New Tab;
# navigation/back links are left untouched.
DUPLICATE_OPEN_RE = re.compile(
    r'<a\b(?![^>]*class=["\'][^"\']*\bbtn-primary\b)[^>]*>\s*'
    r'(?:\[\s*)?(?:↗\s*)?OPEN\s+IN\s+NEW\s+TAB(?:\s*-?&gt;)?(?:\s*\])?\s*</a>',
    re.I | re.S,
)

# Force the primary viewer action to use the site's purple treatment even on
# legacy wrappers whose local CSS does not define .btn-primary consistently.
VIEWER_STYLE = """
<style id="slide-breakdown-viewer-action-style">
.action-buttons .btn-primary,
.se371-viewer-actions .btn-primary {
  color: var(--brand-purple, #b829ea) !important;
  border: 1px solid var(--brand-purple, #b829ea) !important;
  background: transparent !important;
  text-decoration: none !important;
  box-shadow: inset 0 0 0 1px transparent;
}
.action-buttons .btn-primary:hover,
.se371-viewer-actions .btn-primary:hover {
  color: #d978ff !important;
  background: rgba(184, 41, 234, 0.10) !important;
  box-shadow: 0 0 12px rgba(184, 41, 234, 0.20);
}
</style>
"""


def replace_balanced_div(page: str, start: int, replacement: str) -> str:
    tags = re.compile(r"<div\b[^>]*>|</div\s*>", re.I)
    depth = 0
    for match in tags.finditer(page, start):
        if match.start() == start or depth:
            if match.group().lower().startswith("</"):
                depth -= 1
                if depth == 0:
                    return page[:start] + replacement + page[match.end():]
            else:
                depth += 1
    return page


def replace_matching_div(page: str, pattern: re.Pattern[str], replacement: str) -> str:
    match = pattern.search(page)
    return replace_balanced_div(page, match.start(), replacement) if match else page


def viewer_embed(href: str) -> str:
    safe = html.escape(href, quote=True)
    return (
        '<div class="embed-area-wrapper">\n'
        '  <div class="embed-container" id="embedded-content">\n'
        '    <div class="rendered-content">\n'
        f'      <iframe class="embed-frame legacy-html-frame" src="{safe}" loading="lazy" title="Slide breakdown"></iframe>\n'
        '    </div>\n'
        '  </div>\n'
        '</div>'
    )


def relative_href(source: Path, index_path: Path) -> str:
    rel = os.path.relpath(source, index_path.parent).replace(os.sep, "/")
    if not rel.startswith("."):
        rel = "./" + rel
    return rel


def open_button(source: Path, index_path: Path) -> str:
    safe = html.escape(relative_href(source, index_path), quote=True)
    return (f'<a class="btn btn-primary" href="{safe}" target="_blank" '
            'rel="noopener noreferrer">[ OPEN IN NEW TAB -&gt; ]</a>')


def insert_before_closing(page: str, markup: str) -> str:
    for closing in ("</main>", "</body>"):
        pos = page.lower().rfind(closing)
        if pos >= 0:
            return page[:pos] + "\n" + markup + "\n" + page[pos:]
    return page + "\n" + markup + "\n"


def ensure_action_style(page: str) -> str:
    if 'id="slide-breakdown-viewer-action-style"' in page:
        return page
    head_end = page.lower().find("</head>")
    if head_end >= 0:
        return page[:head_end] + VIEWER_STYLE + page[head_end:]
    return VIEWER_STYLE + page


def repair_viewer(index_path: Path, source: Path) -> bool:
    original = index_path.read_text(encoding="utf-8")
    page = original
    rel_src = relative_href(source, index_path)
    embed = viewer_embed(rel_src)

    if EMBED_DIV_RE.search(page):
        page = replace_matching_div(page, EMBED_DIV_RE, embed)
    elif COMING_SOON_RE.search(page):
        page = replace_matching_div(page, COMING_SOON_RE, embed)
    else:
        page = insert_before_closing(page, embed)

    # An authored source means AVAILABLE, regardless of stale wrapper text.
    # Replace the existing primary control (including disabled Coming Soon spans)
    # with the one canonical action.
    button = open_button(source, index_path)
    if PRIMARY_BUTTON_RE.search(page):
        page = PRIMARY_BUTTON_RE.sub(button, page, count=1)
    else:
        actions = ACTION_DIV_RE.search(page)
        if actions:
            page = page[:actions.end()] + "\n            " + button + page[actions.end():]
        else:
            embed_match = EMBED_DIV_RE.search(page)
            if embed_match:
                page = page[:embed_match.start()] + '<div class="action-buttons">' + button + '</div>\n' + page[embed_match.start():]
            else:
                page = insert_before_closing(page, button)

    # Remove any extra plain Open-in-New-Tab action left by a newer shell.  The
    # canonical .btn-primary inserted above remains because the regex excludes it.
    page = DUPLICATE_OPEN_RE.sub("", page)

    # Remove stale availability copy/classes after the source has been proven to
    # exist.  This covers wrappers that had a Coming Soon button but a real iframe.
    page = page.replace("This HTML slide breakdown is coming soon.", "")
    page = re.sub(r'\bbtn-disabled\b', '', page)
    page = ensure_action_style(page)

    if page != original:
        index_path.write_text(page, encoding="utf-8")
        return True
    return False


def update_listing(listing: Path) -> bool:
    original = listing.read_text(encoding="utf-8")

    def repl(match: re.Match[str]) -> str:
        slug = match.group("slug").rstrip("/")
        folder = listing.parent / slug
        status = "AVAILABLE" if (folder / "index.html").is_file() and breakdown_source(folder, listing.parent) else "COMING SOON"
        return match.group(1) + status + match.group(5)

    page = DIR_ROW_RE.sub(repl, original)
    if page != original:
        listing.write_text(page, encoding="utf-8")
        return True
    return False


def main() -> None:
    if not ACADEMICS.exists():
        raise SystemExit(f"Academic root not found: {ACADEMICS}")

    repaired = available = listings = 0
    for slide_root in slide_breakdown_roots(ACADEMICS):
        for folder in sorted(p for p in slide_root.iterdir() if p.is_dir()):
            index_path = folder / "index.html"
            if not index_path.is_file():
                continue
            source = breakdown_source(folder, slide_root)
            if source is None:
                continue
            available += 1
            if repair_viewer(index_path, source):
                repaired += 1
                display_source = os.path.relpath(source, index_path.parent).replace(os.sep, "/")
                print(f"repaired {index_path.relative_to(ROOT)} -> {display_source}")
        listing = slide_root / "index.html"
        if listing.exists() and update_listing(listing):
            listings += 1
            print(f"updated statuses in {listing.relative_to(ROOT)}")

    print(f"slide breakdown repair complete: {available} available viewers checked, "
          f"{repaired} viewer pages repaired, {listings} listings updated")


if __name__ == "__main__":
    main()

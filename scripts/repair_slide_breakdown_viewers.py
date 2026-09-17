#!/usr/bin/env python3
"""Repair academic slide-breakdown viewer pages from the files that actually exist.

A breakdown is AVAILABLE when its viewer directory contains a real HTML
breakdown file besides index.html. This deliberately avoids legacy URL/path
assumptions and works across all courses under docs/academics.
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
COMING_SOON_TEXT = "This HTML slide breakdown is coming soon."

PRIMARY_BUTTON_RE = re.compile(
    r'<(?:a|span)\b[^>]*class="[^"]*\bbtn\s+btn-primary\b[^"]*"[^>]*>'
    r'\s*\[[^\]]*(?:-&gt;|->|COMING SOON)[^\]]*\]\s*</(?:a|span)>', re.I | re.S)
IFRAME_SRC_RE = re.compile(r'(<iframe\b[^>]*\bsrc=["\'])([^"\']+)(["\'][^>]*>)', re.I | re.S)
DIR_ROW_RE = re.compile(
    r'(<a\b[^>]*href="(?P<href>[^"]+/slide-breakdowns/(?P<slug>[^"]+)/?)"[^>]*class="[^"]*\bdir-row\b[^"]*"[^>]*>.*?'
    r'<span\b[^>]*class="[^"]*\bstatus-tag\b[^"]*"[^>]*>)(?P<status>[^<]*)(</span>)', re.I | re.S)


def replace_div_block(page: str, marker: str, replacement: str) -> str:
    """Replace one balanced div block identified by a stable class marker."""
    marker_start = page.find(marker)
    if marker_start < 0:
        return page
    div_start = page.rfind("<div", 0, marker_start + 1)
    tags = re.compile(r"<div\b[^>]*>|</div\s*>", re.I)
    depth = 0
    for match in tags.finditer(page, div_start):
        if match.group().lower().startswith("</"):
            depth -= 1
            if depth == 0:
                return page[:div_start] + replacement + page[match.end():]
        else:
            depth += 1
    return page


def viewer_container(href: str) -> str:
    safe = html.escape(href, quote=True)
    return (
        '  <div class="embed-container" id="embedded-content">\n'
        '    <div class="rendered-content" data-lang-panel="en">'
        f'<iframe class="embed-frame legacy-html-frame" src="{safe}" loading="lazy" title="Slide breakdown"></iframe></div>\n'
        '    <div class="rendered-content" data-lang-panel="ar" hidden>'
        f'<iframe class="embed-frame legacy-html-frame" src="{safe}" loading="lazy" title="Slide breakdown"></iframe></div>\n'
        '  </div>\n'
    )


def viewer_embed(href: str) -> str:
    return '<div class="embed-area-wrapper" vid="82">\n' + viewer_container(href) + '</div>\n'


def open_button(filename: str) -> str:
    safe = html.escape(filename, quote=True)
    return (f'<a class="btn btn-primary" href="./{safe}" target="_blank" '
            'rel="noopener noreferrer">[ OPEN IN NEW TAB -&gt; ]</a>')


def repair_viewer(index_path: Path, source: Path) -> bool:
    original = index_path.read_text(encoding="utf-8")
    page = original
    rel_src = os.path.relpath(source, index_path.parent).replace(os.sep, "/")
    if not rel_src.startswith("."):
        rel_src = "./" + rel_src

    if COMING_SOON_TEXT in page or "coming-soon-panel" in page:
        page = replace_div_block(page, 'class="embed-area-wrapper"', viewer_embed(rel_src))
        if page == original:
            page = replace_div_block(page, 'class="embed-container" id="embedded-content"', viewer_container(rel_src))

    # Every iframe in a slide-breakdown viewer should load the real sibling
    # breakdown. This also repairs stale absolute paths after SEO renames.
    page = IFRAME_SRC_RE.sub(lambda m: m.group(1) + rel_src + m.group(3), page)

    if PRIMARY_BUTTON_RE.search(page):
        page = PRIMARY_BUTTON_RE.sub(open_button(source.name), page, count=1)

    if page != original:
        index_path.write_text(page, encoding="utf-8")
        return True
    return False


def update_listing(listing: Path) -> bool:
    original = listing.read_text(encoding="utf-8")

    def repl(match: re.Match[str]) -> str:
        slug = match.group("slug").rstrip("/")
        status = "AVAILABLE" if breakdown_source(listing.parent / slug, listing.parent) else "COMING SOON"
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
            source = breakdown_source(folder, slide_root)
            index_path = folder / "index.html"
            if source is None or not index_path.exists():
                continue
            available += 1
            if repair_viewer(index_path, source):
                repaired += 1
                print(f"repaired {index_path.relative_to(ROOT)} -> {source.relative_to(index_path.parent)}")
        listing = slide_root / "index.html"
        if listing.exists() and update_listing(listing):
            listings += 1
            print(f"updated statuses in {listing.relative_to(ROOT)}")

    print(f"slide breakdown repair complete: {available} available viewers checked, "
          f"{repaired} viewer pages repaired, {listings} listings updated")


if __name__ == "__main__":
    main()

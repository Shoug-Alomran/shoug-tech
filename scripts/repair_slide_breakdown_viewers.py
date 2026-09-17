#!/usr/bin/env python3
"""Repair academic slide-breakdown viewers from filesystem truth.

Every dedicated breakdown directory that contains an authored HTML sibling is
AVAILABLE. Its wrapper is rebuilt to embed that sibling regardless of whatever
stale viewer markup a previous migration/generator left behind.
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
DIR_ROW_RE = re.compile(
    r'(<a\b[^>]*href="(?P<href>[^"]+/slide-breakdowns/(?P<slug>[^"]+)/?)"[^>]*class="[^"]*\bdir-row\b[^"]*"[^>]*>.*?'
    r'<span\b[^>]*class="[^"]*\bstatus-tag\b[^"]*"[^>]*>)(?P<status>[^<]*)(</span>)', re.I | re.S)


def replace_div_block(page: str, marker: str, replacement: str) -> str:
    """Replace one balanced div block containing marker."""
    marker_start = page.find(marker)
    if marker_start < 0:
        return page
    div_start = page.rfind("<div", 0, marker_start + 1)
    if div_start < 0:
        return page
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


def viewer_embed(href: str) -> str:
    safe = html.escape(href, quote=True)
    return (
        '<div class="embed-area-wrapper" vid="82">\n'
        '  <div class="embed-container" id="embedded-content">\n'
        '    <div class="rendered-content">\n'
        f'      <iframe class="embed-frame legacy-html-frame" src="{safe}" loading="lazy" title="Slide breakdown"></iframe>\n'
        '    </div>\n'
        '  </div>\n'
        '</div>'
    )


def relative_href(source: Path, index_path: Path) -> str:
    """Return a browser-safe path even when source lives in the slide root."""
    rel = os.path.relpath(source, index_path.parent).replace(os.sep, "/")
    if not rel.startswith("."):
        rel = "./" + rel
    return rel


def open_button(source: Path, index_path: Path) -> str:
    safe = html.escape(relative_href(source, index_path), quote=True)
    return (f'<a class="btn btn-primary" href="{safe}" target="_blank" '
            'rel="noopener noreferrer">[ OPEN IN NEW TAB -&gt; ]</a>')


def repair_viewer(index_path: Path, source: Path) -> bool:
    original = index_path.read_text(encoding="utf-8")
    page = original
    rel_src = relative_href(source, index_path)

    # Rebuild the embed region unconditionally for every available viewer.
    # This fixes Coming Soon shells, missing iframes, and stale iframe paths in
    # one deterministic operation instead of trying to recognize old variants.
    replaced = replace_div_block(page, 'class="embed-area-wrapper"', viewer_embed(rel_src))
    if replaced == page:
        replaced = replace_div_block(page, "embed-area-wrapper", viewer_embed(rel_src))
    page = replaced

    # The first primary action on a breakdown viewer is Open in New Tab.
    button = open_button(source, index_path)
    if PRIMARY_BUTTON_RE.search(page):
        page = PRIMARY_BUTTON_RE.sub(button, page, count=1)
    else:
        actions = page.find('class="action-buttons"')
        if actions >= 0:
            insert_at = page.find(">", actions) + 1
            page = page[:insert_at] + "\n            " + button + page[insert_at:]

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
                # Do not use Path.relative_to here: legacy courses such as
                # ISC113 keep authored HTML one level above the viewer folder.
                # os.path.relpath handles both sibling and parent-level sources.
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

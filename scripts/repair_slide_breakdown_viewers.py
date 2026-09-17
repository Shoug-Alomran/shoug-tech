#!/usr/bin/env python3
"""Repair academic slide-breakdown viewer pages from the files that actually exist.

This is intentionally filesystem-driven. A breakdown is AVAILABLE when its
viewer directory contains a real HTML breakdown file besides index.html.
It does not depend on legacy /Academics/ URL patterns, course-specific names,
or absolute iframe URLs.

The script repairs false "Coming Soon" viewers, broken/missing iframe sources,
OPEN IN NEW TAB buttons, and AVAILABLE/COMING SOON labels on each course's
slide-breakdowns/index.html.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACADEMICS = ROOT / "docs" / "academics"

COMING_SOON_TEXT = "This HTML slide breakdown is coming soon."

EMBED_AREA_RE = re.compile(
    r'<div class="embed-area-wrapper"[^>]*>.*?(?=\s*</main>)', re.S
)
EMBED_CONTAINER_RE = re.compile(
    r'<div class="embed-container" id="embedded-content">.*?</div>\s*</div>', re.S
)
PRIMARY_BUTTON_RE = re.compile(
    r'<(?:a|span)\b[^>]*class="[^"]*\bbtn\s+btn-primary\b[^"]*"[^>]*>'
    r'\s*\[[^\]]*(?:-&gt;|->|COMING SOON)[^\]]*\]\s*</(?:a|span)>',
    re.I | re.S,
)
IFRAME_SRC_RE = re.compile(
    r'(<iframe\b[^>]*\bsrc=["\'])([^"\']+)(["\'][^>]*>)', re.I | re.S
)
DIR_ROW_RE = re.compile(
    r'(<a\b[^>]*href="(?P<href>[^"]+/slide-breakdowns/(?P<slug>[^"]+)/?)"[^>]*class="[^"]*\bdir-row\b[^"]*"[^>]*>.*?'
    r'<span\b[^>]*class="[^"]*\bstatus-tag\b[^"]*"[^>]*>)(?P<status>[^<]*)(</span>)',
    re.I | re.S,
)


def breakdown_file(folder: Path) -> Path | None:
    """Return the real breakdown HTML in a viewer directory, if one exists."""
    if not folder.is_dir():
        return None
    candidates = [
        p for p in folder.glob("*.html")
        if p.name.lower() != "index.html" and not p.name.lower().endswith(".ar.html")
    ]
    if not candidates:
        return None

    # Prefer the conventional file matching the slug tail (02-html -> html.html),
    # then the only/largest authored HTML. This avoids accidentally embedding a
    # tiny helper page when older courses contain more than one HTML file.
    slug_tail = re.sub(r"^\d+[-_]", "", folder.name).lower()
    preferred = [
        p for p in candidates
        if p.stem.lower() in {slug_tail, slug_tail.replace("-", "_"), slug_tail.split("-")[0]}
    ]
    pool = preferred or candidates
    return max(pool, key=lambda p: p.stat().st_size)


def viewer_embed(filename: str) -> str:
    safe = html.escape(filename, quote=True)
    return (
        '<div class="embed-area-wrapper" vid="82">\n'
        '  <div class="embed-container" id="embedded-content">\n'
        '    <div class="rendered-content" data-lang-panel="en">'
        f'<iframe class="embed-frame legacy-html-frame" src="./{safe}" loading="lazy" '
        'title="Slide breakdown"></iframe></div>\n'
        '    <div class="rendered-content" data-lang-panel="ar" hidden>'
        f'<iframe class="embed-frame legacy-html-frame" src="./{safe}" loading="lazy" '
        'title="Slide breakdown"></iframe></div>\n'
        '  </div>\n'
        '</div>\n'
    )


def open_button(filename: str) -> str:
    safe = html.escape(filename, quote=True)
    return (
        f'<a class="btn btn-primary" href="./{safe}" target="_blank" '
        'rel="noopener noreferrer">[ OPEN IN NEW TAB -&gt; ]</a>'
    )


def repair_viewer(index_path: Path, source: Path) -> bool:
    original = index_path.read_text(encoding="utf-8")
    page = original
    rel_src = f"./{source.name}"

    # Repair a false Coming Soon state by replacing the complete embed area.
    if COMING_SOON_TEXT in page or "coming-soon-panel" in page:
        if EMBED_AREA_RE.search(page):
            page = EMBED_AREA_RE.sub(viewer_embed(source.name), page, count=1)
        elif EMBED_CONTAINER_RE.search(page):
            # Fallback for older shells that do not have embed-area-wrapper.
            container = viewer_embed(source.name)
            container = re.sub(r'^<div class="embed-area-wrapper"[^>]*>\n|\n</div>\n$', '', container)
            page = EMBED_CONTAINER_RE.sub(container, page, count=1)

    # If a viewer already has iframes but they point at stale absolute/renamed
    # locations, use the real sibling file. Restrict this to slide breakdown
    # viewer pages so unrelated iframes are untouched.
    if "slide-breakdowns" in str(index_path).replace("\\", "/"):
        page = IFRAME_SRC_RE.sub(lambda m: m.group(1) + rel_src + m.group(3), page)

    # Restore the primary action if a previous fixer disabled it.
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
        available = breakdown_file(listing.parent / slug) is not None
        status = "AVAILABLE" if available else "COMING SOON"
        return match.group(1) + status + match.group(4)

    page = DIR_ROW_RE.sub(repl, original)
    if page != original:
        listing.write_text(page, encoding="utf-8")
        return True
    return False


def main() -> None:
    if not ACADEMICS.exists():
        raise SystemExit(f"Academic root not found: {ACADEMICS}")

    repaired = 0
    available = 0
    listings = 0

    for slide_root in ACADEMICS.glob("*/*/slide-breakdowns"):
        if not slide_root.is_dir():
            continue

        for folder in sorted(p for p in slide_root.iterdir() if p.is_dir()):
            source = breakdown_file(folder)
            index_path = folder / "index.html"
            if source is None or not index_path.exists():
                continue
            available += 1
            if repair_viewer(index_path, source):
                repaired += 1
                print(f"repaired {index_path.relative_to(ROOT)} -> ./{source.name}")

        listing = slide_root / "index.html"
        if listing.exists() and update_listing(listing):
            listings += 1
            print(f"updated statuses in {listing.relative_to(ROOT)}")

    print(
        f"slide breakdown repair complete: {available} available viewers checked, "
        f"{repaired} viewer pages repaired, {listings} listings updated"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Validate production slide-breakdown viewers against filesystem truth.

This validator intentionally checks the deterministic markup emitted by
repair_slide_breakdown_viewers.py instead of trying to parse the repository's
many generations of legacy viewer HTML.  The filesystem is the source of
truth: if an authored breakdown exists, the final viewer must literally
contain an iframe and primary link to that file.
"""

from __future__ import annotations

import html
import os
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
ACADEMICS = ROOT / "docs" / "academics"
sys.path.insert(0, str(ROOT / "scripts"))
from slide_breakdown_utils import breakdown_source, slide_breakdown_roots  # noqa: E402

COMING_SOON = "This HTML slide breakdown is coming soon."
ROW_RE = re.compile(
    r'<a\b(?P<attrs>[^>]*\bclass=["\'][^"\']*\bdir-row\b[^"\']*["\'][^>]*)>(?P<body>.*?)</a>',
    re.I | re.S,
)
HREF_RE = re.compile(r'\bhref=["\']([^"\']+)["\']', re.I)
STATUS_RE = re.compile(
    r'(<span\b[^>]*class=["\'][^"\']*\bstatus-tag\b[^"\']*["\'][^>]*>)([^<]*)(</span>)',
    re.I | re.S,
)


def relative_href(source: Path, index: Path) -> str:
    rel = os.path.relpath(source, index.parent).replace(os.sep, "/")
    return rel if rel.startswith(".") else "./" + rel


def attr_points_to(text: str, tag: str, attr: str, expected: str, required_class: str | None = None) -> bool:
    """Check literal final HTML markup without depending on legacy document parsing."""
    for match in re.finditer(rf"<{tag}\b[^>]*>", text, re.I | re.S):
        markup = match.group(0)
        if required_class:
            class_match = re.search(r'\bclass=["\']([^"\']*)["\']', markup, re.I)
            if not class_match or required_class not in class_match.group(1).split():
                continue
        attr_match = re.search(rf'\b{attr}=["\']([^"\']+)["\']', markup, re.I)
        if attr_match and html.unescape(attr_match.group(1)) == expected:
            return True
    return False


def validate_viewer(index: Path, source: Path, errors: list[str]) -> None:
    text = index.read_text(encoding="utf-8", errors="ignore")
    expected = relative_href(source, index)

    if COMING_SOON in text or re.search(
        r'<div\b[^>]*class=["\'][^"\']*\bcoming-soon-panel\b', text, re.I
    ):
        errors.append(f"available viewer still says Coming Soon: {index.relative_to(ROOT)}")

    if not attr_points_to(text, "iframe", "src", expected):
        errors.append(
            f"available viewer missing expected iframe src {expected!r}: {index.relative_to(ROOT)}"
        )

    if not attr_points_to(text, "a", "href", expected, "btn-primary"):
        errors.append(
            f"available viewer missing expected Open in New Tab href {expected!r}: {index.relative_to(ROOT)}"
        )

    if not source.is_file():
        errors.append(f"authored breakdown disappeared: {source.relative_to(ROOT)}")


def generic_viewer_source(href: str) -> Path | None:
    parsed = urlparse(html.unescape(href))
    query = parse_qs(parsed.query)
    values = query.get("src")
    if not values:
        return None
    src = unquote(values[0])
    if not src.startswith("/academics/"):
        return None
    return ROOT / "docs" / src.lstrip("/")


def validate_listing(listing: Path, root: Path, errors: list[str]) -> None:
    text = listing.read_text(encoding="utf-8", errors="ignore")
    for match in ROW_RE.finditer(text):
        href_match = HREF_RE.search(match.group("attrs"))
        status_match = STATUS_RE.search(match.group("body"))
        if not href_match or not status_match:
            continue
        href = html.unescape(href_match.group(1))
        actual = re.sub(r"\s+", " ", status_match.group(2)).strip().upper()

        direct_source = generic_viewer_source(href)
        if direct_source is not None:
            expected = "AVAILABLE" if direct_source.is_file() else "COMING SOON"
        else:
            parsed = urlparse(href)
            slug = parsed.path.rstrip("/").split("/")[-1]
            folder = (root / slug).resolve()
            expected = "AVAILABLE" if (folder / "index.html").is_file() and breakdown_source(folder, root) else "COMING SOON"

        if actual != expected:
            errors.append(
                f"listing status {actual!r}, expected {expected!r}: "
                f"{listing.relative_to(ROOT)} -> {href}"
            )


def main() -> int:
    errors: list[str] = []
    roots = slide_breakdown_roots(ACADEMICS)
    checked = 0
    for root in roots:
        for folder in sorted(path for path in root.iterdir() if path.is_dir()):
            index = folder / "index.html"
            if not index.is_file():
                continue
            source = breakdown_source(folder, root)
            if source is not None:
                checked += 1
                validate_viewer(index, source, errors)
        listing = root / "index.html"
        if listing.is_file():
            validate_listing(listing, root, errors)

    for path in ACADEMICS.rglob("*"):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if re.search(r"/Academics/", text):
            errors.append(f"stale /Academics/ URL in production file: {path.relative_to(ROOT)}")

    if errors:
        print("slide-breakdown validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"slide-breakdown validation passed: {checked} available viewers across {len(roots)} roots")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

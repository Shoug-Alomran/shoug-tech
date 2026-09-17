#!/usr/bin/env python3
"""Validate production slide-breakdown viewers against filesystem truth."""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
ACADEMICS = ROOT / "docs" / "academics"
sys.path.insert(0, str(ROOT / "scripts"))
from slide_breakdown_utils import breakdown_source, slide_breakdown_roots  # noqa: E402

COMING_SOON = "This HTML slide breakdown is coming soon."
IFRAME_RE = re.compile(r"<iframe\b[^>]*\bsrc=[\"']([^\"']+)", re.I)
OPEN_RE = re.compile(
    r'<a\b(?=[^>]*class=["\'][^"\']*\bbtn-primary\b[^"\']*["\'])(?=[^>]*href=["\']([^"\']+)["\'])[^>]*>',
    re.I,
)
ROW_RE = re.compile(
    r'<a\b(?P<attrs>[^>]*\bclass=["\'][^"\']*\bdir-row\b[^"\']*["\'][^>]*)>(?P<body>.*?)</a>',
    re.I | re.S,
)
HREF_RE = re.compile(r'\bhref=["\']([^"\']+)["\']', re.I)
STATUS_RE = re.compile(
    r'(<span\b[^>]*class=["\'][^"\']*\bstatus-tag\b[^"\']*["\'][^>]*>)([^<]*)(</span>)',
    re.I | re.S,
)


def local_target(index: Path, href: str) -> Path | None:
    parsed = urlparse(html.unescape(href))
    if parsed.scheme or parsed.netloc:
        return None
    if parsed.path.startswith("/"):
        if not parsed.path.startswith("/academics/"):
            return None
        return ROOT / "docs" / parsed.path.lstrip("/")
    return (index.parent / parsed.path).resolve()


def validate_viewer(index: Path, source: Path, errors: list[str]) -> None:
    text = index.read_text(encoding="utf-8", errors="ignore")
    if COMING_SOON in text or "coming-soon-panel" in text:
        errors.append(f"available viewer still says Coming Soon: {index.relative_to(ROOT)}")

    iframe_matches = IFRAME_RE.findall(text)
    if not iframe_matches:
        errors.append(f"available viewer has no iframe: {index.relative_to(ROOT)}")
    elif not any(local_target(index, href) == source.resolve() for href in iframe_matches):
        errors.append(f"available viewer does not embed authored source {source.name}: {index.relative_to(ROOT)}")

    open_matches = OPEN_RE.findall(text)
    if not open_matches:
        errors.append(f"available viewer has no Open in New Tab: {index.relative_to(ROOT)}")
    elif not any(local_target(index, href) == source.resolve() for href in open_matches):
        errors.append(f"Open in New Tab does not target authored source {source.name}: {index.relative_to(ROOT)}")

    for label, matches in (("iframe", iframe_matches), ("Open in New Tab", open_matches)):
        for href in matches:
            target = local_target(index, href)
            if target is not None and not target.is_file():
                errors.append(f"missing {label} target {href!r}: {index.relative_to(ROOT)}")


def generic_viewer_source(href: str) -> Path | None:
    """Resolve /viewer/?src=/academics/... links used by STAT101-style listings."""
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
    for root in slide_breakdown_roots(ACADEMICS):
        # Only directories with index.html are dedicated viewer directories.
        # Direct-source layouts (e.g. STAT101) are represented by generic
        # /viewer/?src= links and are checked from the listing instead.
        for folder in sorted(path for path in root.iterdir() if path.is_dir()):
            index = folder / "index.html"
            if not index.is_file():
                continue
            source = breakdown_source(folder, root)
            if source is not None:
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
    print(f"slide-breakdown validation passed ({len(slide_breakdown_roots(ACADEMICS))} roots)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

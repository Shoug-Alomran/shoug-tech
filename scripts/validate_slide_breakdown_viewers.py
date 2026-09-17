#!/usr/bin/env python3
"""Validate production slide-breakdown viewers against the filesystem."""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
ACADEMICS = ROOT / "docs" / "academics"
sys.path.insert(0, str(ROOT / "scripts"))
from slide_breakdown_utils import breakdown_source, slide_breakdown_roots  # noqa: E402

COMING_SOON = "This HTML slide breakdown is coming soon."
IFRAME_RE = re.compile(r"<iframe\b[^>]*\bsrc=[\"']([^\"']+)", re.I)
OPEN_RE = re.compile(
    r'<a\b[^>]*class=["\'][^"\']*\bbtn-primary\b[^"\']*["\'][^>]*href=["\']([^"\']+)',
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


def validate_viewer(index: Path, errors: list[str]) -> None:
    text = index.read_text(encoding="utf-8", errors="ignore")
    if COMING_SOON in text or "coming-soon-panel" in text:
        errors.append(f"available viewer still says Coming Soon: {index.relative_to(ROOT)}")
    for label, pattern in (("iframe", IFRAME_RE), ("Open in New Tab", OPEN_RE)):
        matches = pattern.findall(text)
        if not matches:
            errors.append(f"available viewer has no {label}: {index.relative_to(ROOT)}")
        for href in matches:
            target = local_target(index, href)
            if target is None or not target.is_file():
                errors.append(f"missing {label} target {href!r}: {index.relative_to(ROOT)}")


def validate_listing(listing: Path, root: Path, errors: list[str]) -> None:
    text = listing.read_text(encoding="utf-8", errors="ignore")
    for match in ROW_RE.finditer(text):
        href_match = HREF_RE.search(match.group("attrs"))
        status_match = STATUS_RE.search(match.group("body"))
        if not href_match or not status_match:
            continue
        href = html.unescape(href_match.group(1))
        parsed = urlparse(href)
        folder = (root / parsed.path.rstrip("/").split("/")[-1]).resolve()
        expected = "AVAILABLE" if breakdown_source(folder, root) else "COMING SOON"
        actual = re.sub(r"\s+", " ", status_match.group(2)).strip().upper()
        if actual != expected:
            errors.append(
                f"listing status {actual!r}, expected {expected!r}: "
                f"{listing.relative_to(ROOT)} -> {href}"
            )


def main() -> int:
    errors: list[str] = []
    for root in slide_breakdown_roots(ACADEMICS):
        for folder in sorted(path for path in root.iterdir() if path.is_dir()):
            source = breakdown_source(folder, root)
            index = folder / "index.html"
            if source is None:
                continue
            if not index.is_file():
                errors.append(f"authored breakdown has no viewer index: {folder.relative_to(ROOT)}")
                continue
            validate_viewer(index, errors)
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
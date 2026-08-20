#!/usr/bin/env python3
"""Rewrite internal links to match the real on-disk casing.

macOS resolves paths case-insensitively, so `/Academics/...` and
`CS330/Images/...` work locally and 404 on GitHub Pages, which serves from a
case-sensitive filesystem. Canonical tags pointing at those URLs are worse
than a broken link: search engines follow them to a 404.

Only rewrites a reference when a file exists at exactly one casing, so an
ambiguous match is reported rather than guessed at.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit, quote

DOCS = Path(__file__).resolve().parent.parent / "docs"
SITE_HOSTS = {"shoug-tech.com", "www.shoug-tech.com"}

# href/src attributes plus the metadata tags that carry absolute site URLs.
REF = re.compile(
    r'(?P<attr>\b(?:href|src|content)\s*=\s*")(?P<url>[^"]*)(?P<tail>")',
    re.I,
)

_listing_cache: dict[Path, dict[str, str]] = {}


def listing(d: Path) -> dict[str, str]:
    """lowercased name -> real name, for one directory."""
    cached = _listing_cache.get(d)
    if cached is None:
        try:
            cached = {e.name.lower(): e.name for e in d.iterdir()}
        except OSError:
            cached = {}
        _listing_cache[d] = cached
    return cached


def real_path(url_path: str) -> str | None:
    """Return url_path with each segment corrected, or None if unresolvable."""
    decoded = unquote(url_path)
    trailing = decoded.endswith("/")
    parts = [p for p in decoded.strip("/").split("/") if p]
    if not parts:
        return None

    current = DOCS
    fixed: list[str] = []
    for part in parts:
        entries = listing(current)
        real = entries.get(part.lower())
        if real is None:
            return None
        fixed.append(real)
        current = current / real

    out = "/" + "/".join(fixed)
    if trailing:
        out += "/"
    return out


def fix_url(url: str) -> str | None:
    if not url or url.startswith(("#", "data:", "mailto:", "tel:", "javascript:")):
        return None

    split = urlsplit(url)
    if split.scheme and split.scheme.lower() not in {"http", "https"}:
        return None
    if split.netloc and split.netloc.lower() not in SITE_HOSTS:
        return None
    if not split.path.startswith("/"):
        return None  # relative paths are handled per-page below

    corrected = real_path(split.path)
    if corrected is None or corrected == unquote(split.path):
        return None

    rebuilt = quote(corrected, safe="/:@&=+$,-_.!~*'()%")
    if split.query:
        rebuilt += "?" + split.query
    if split.fragment:
        rebuilt += "#" + split.fragment
    if split.netloc:
        rebuilt = f"{split.scheme}://{split.netloc}{rebuilt}"
    return rebuilt


def fix_relative(url: str, page: Path) -> str | None:
    """Correct a page-relative reference such as ../images/Layers.png."""
    if not url or url.startswith(("#", "/", "data:", "mailto:", "tel:", "javascript:")):
        return None
    if urlsplit(url).scheme:
        return None

    split = urlsplit(url)
    base = (page.parent / unquote(split.path)).resolve()
    try:
        rel = base.relative_to(DOCS.resolve())
    except ValueError:
        return None

    corrected = real_path("/" + rel.as_posix())
    if corrected is None:
        return None

    target = DOCS / corrected.lstrip("/")
    if target == base:
        return None

    import os
    new_rel = os.path.relpath(target, page.parent)
    if unquote(split.path).endswith("/") and not new_rel.endswith("/"):
        new_rel += "/"
    rebuilt = quote(new_rel, safe="/:@&=+$,-_.!~*'()%")
    if split.query:
        rebuilt += "?" + split.query
    if split.fragment:
        rebuilt += "#" + split.fragment
    return rebuilt


def main() -> int:
    apply = "--apply" in sys.argv
    pages = 0
    changes = 0
    samples: list[str] = []

    for p in sorted(DOCS.rglob("*.html")):
        text = p.read_text(encoding="utf-8", errors="ignore")
        local = 0

        def repl(m: re.Match[str]) -> str:
            nonlocal local
            url = m.group("url")
            new = fix_url(url) or fix_relative(url, p)
            if not new or new == url:
                return m.group(0)
            local += 1
            if len(samples) < 8:
                samples.append(f"{url}  ->  {new}")
            return m.group("attr") + new + m.group("tail")

        out = REF.sub(repl, text)
        if local:
            pages += 1
            changes += local
            if apply:
                p.write_text(out, encoding="utf-8")

    verb = "fixed" if apply else "would fix"
    print(f"{verb} {changes} references across {pages} pages")
    for s in samples:
        print(f"  {s}")
    if not apply:
        print("re-run with --apply to write changes")
    return 0


if __name__ == "__main__":
    sys.exit(main())

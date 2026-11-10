#!/usr/bin/env python3
"""Normalize canonical and Open Graph URLs for generated HTML and drop hreflang.

The deployed filesystem route is authoritative. This prevents copied/generated
folder pages from retaining the canonical URL of their template page.
"""

from __future__ import annotations

import html
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "docs"
ORIGIN = "https://shoug-tech.com"


def route_url(path: Path) -> str:
    rel = path.relative_to(SITE).as_posix()
    if rel == "index.html":
        rel = ""
    elif rel.endswith("/index.html"):
        rel = rel[:-len("index.html")]
    return ORIGIN + "/" + quote(rel, safe="/:.-_%")


def replace_attr(tag: str, attr: str, value: str) -> str:
    escaped = html.escape(value, quote=True)
    pattern = rf'(\b{re.escape(attr)}\s*=\s*["\'])(.*?)(["\'])'
    if re.search(pattern, tag, flags=re.I | re.S):
        return re.sub(pattern, lambda m: m.group(1) + escaped + m.group(3), tag,
                      count=1, flags=re.I | re.S)
    return tag


def normalize(document: str, path: Path) -> str:
    url = route_url(path)

    # Every index.html is the canonical representation of its own folder route.
    document = re.sub(
        r'<link\b(?=[^>]*\brel\s*=\s*["\']canonical["\'])[^>]*>',
        lambda m: replace_attr(m.group(0), "href", url),
        document, flags=re.I | re.S,
    )

    # og:url must agree with canonical.
    document = re.sub(
        r'<meta\b(?=[^>]*\bproperty\s*=\s*["\']og:url["\'])[^>]*>',
        lambda m: replace_attr(m.group(0), "content", url),
        document, flags=re.I | re.S,
    )

    # Pages rebuilt after the optimizer can inherit these from a template; Arabic is
    # applied in place, so no separate URL exists for an alternate to name.
    document = re.sub(
        r'[ \t]*<link\b(?=[^>]*\brel\s*=\s*["\']alternate["\'])(?=[^>]*\bhreflang\s*=)[^>]*>[ \t]*\n?',
        "", document, flags=re.I | re.S,
    )
    return document


def main() -> None:
    changed = checked = 0
    for path in SITE.rglob("index.html"):
        checked += 1
        original = path.read_text(encoding="utf-8")
        updated = normalize(original, path)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"normalized {path.relative_to(ROOT)} -> {route_url(path)}")
    print(f"URL normalization complete: {checked} folder pages checked, {changed} updated")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Patch generated HTML for Lighthouse-friendly static output."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"


LOGO_SIZE = 'width="1022" height="385"'
HEADER_LOGO_SIZE = 'width="255" height="96"'
FAVICON_SIZE = 'width="128" height="121"'
TWEMOJI_SIZE = 'width="20" height="20" loading="lazy" decoding="async"'


def add_attr_once(tag: str, attr: str, value: str | None = None) -> str:
    name = attr.split("=", 1)[0]
    if re.search(rf"\s{name}(?:=|\s|>)", tag):
        return tag
    insertion = f" {attr}" if value is None else f' {attr}="{value}"'
    if tag.endswith("/>"):
        return tag[:-2].rstrip() + insertion + ">"
    return tag[:-1] + insertion + ">"


def optimize_images(html: str) -> str:
    def patch_img(match: re.Match[str]) -> str:
        tag = match.group(0)

        if "logo-header.png" in tag:
            tag = add_attr_once(tag, HEADER_LOGO_SIZE)
            tag = add_attr_once(tag, "decoding", "async")
            tag = add_attr_once(tag, "fetchpriority", "high")
            return tag

        if "logo.png" in tag:
            tag = add_attr_once(tag, LOGO_SIZE)
            tag = add_attr_once(tag, "decoding", "async")
            tag = add_attr_once(tag, "fetchpriority", "high")
            return tag

        if "google.png" in tag:
            tag = add_attr_once(tag, FAVICON_SIZE)
            tag = add_attr_once(tag, "decoding", "async")
            return tag

        if "twemoji" in tag:
            for part in TWEMOJI_SIZE.split():
                name, value = part.split("=", 1)
                tag = add_attr_once(tag, name, value.strip('"'))
            return tag

        tag = add_attr_once(tag, "loading", "lazy")
        tag = add_attr_once(tag, "decoding", "async")
        return tag

    return re.sub(r"<img\b[^>]*>", patch_img, html)


def page_variants(path: Path) -> tuple[str, str]:
    rel = path.relative_to(SITE).as_posix()
    is_ar = rel.startswith("ar/")

    if rel.endswith("index.html"):
        route = rel[: -len("index.html")]
    else:
        route = rel

    if is_ar:
        ar_route = route
        en_route = route[3:]
    else:
        en_route = route
        ar_route = f"ar/{route}"

    return en_route, ar_route


def add_alternates(html: str, path: Path) -> str:
    if 'rel="alternate"' in html:
        return html

    en_route, ar_route = page_variants(path)
    en = f"https://shoug-tech.com/{en_route}".replace("index.html", "")
    ar = f"https://shoug-tech.com/{ar_route}".replace("index.html", "")

    links = (
        f'      <link rel="alternate" hreflang="en" href="{en}">\n'
        f'      <link rel="alternate" hreflang="ar" href="{ar}">\n'
        f'      <link rel="alternate" hreflang="x-default" href="{en}">\n'
    )
    return html.replace("      <link rel=\"icon\"", links + "      <link rel=\"icon\"", 1)


def patch_accessibility(html: str) -> str:
    html = html.replace(
        '<div class="md-search" data-md-component="search" role="dialog">',
        '<div class="md-search" data-md-component="search" role="dialog" aria-label="Search dialog">',
    )
    html = html.replace(
        '<div class="md-dialog" data-md-component="dialog">',
        '<div class="md-dialog" data-md-component="dialog" role="dialog" aria-label="Site message">',
    )
    return html


def main() -> int:
    if not SITE.is_dir():
        print("[warn] site directory not found; skipping HTML optimization")
        return 0

    changed = 0
    for path in SITE.rglob("*.html"):
        original = path.read_text(encoding="utf-8")
        html = patch_accessibility(original)
        html = optimize_images(html)
        html = add_alternates(html, path)

        if html != original:
            path.write_text(html, encoding="utf-8")
            changed += 1

    print(f"[ok] optimized generated HTML: {changed} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())

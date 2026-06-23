#!/usr/bin/env python3
"""Check generated pages for basic SEO metadata quality."""

from __future__ import annotations

import re
import sys
from html import unescape
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
if not SITE.is_dir() and (ROOT / "docs").is_dir():
    SITE = ROOT / "docs"
GENERIC_TITLES = {"overview", "intro", "introduction", "home", "index"}
SITE_DESCRIPTION_START = "Shoug Fawaz Alomran: Software Engineering & Cybersecurity student"
BAD_DESCRIPTION_FRAGMENTS = {
    "SYSTEM_DIRECTORY",
    "ACADEMICS/",
    "SLIDE BREAKDOWNS",
    "STUDY MATERIAL",
}


def attr(html: str, pattern: str) -> str | None:
    match = re.search(pattern, html, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return None
    return unescape(match.group(1).strip())


def route_for(path: Path) -> str:
    rel = path.relative_to(SITE).as_posix()
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def is_redirect(html: str) -> bool:
    return "http-equiv=\"refresh\"" in html[:500].lower() or "location.replace(" in html[:800]


def main() -> int:
    if not SITE.exists():
        print("[error] site directory not found. Run `mkdocs build` first.")
        return 1

    failures: list[str] = []
    checked = 0

    for path in sorted(SITE.rglob("index.html")):
        stat = path.stat()
        if stat.st_size > 0 and stat.st_blocks == 0:
            continue
        html = path.read_text(encoding="utf-8", errors="ignore")
        if is_redirect(html):
            continue

        checked += 1
        route = route_for(path)
        title = attr(html, r"<title\b[^>]*>(.*?)</title>")
        description = attr(
            html,
            r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
        )
        canonical = attr(
            html,
            r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']',
        )
        og_url = attr(
            html,
            r'<meta\s+property=["\']og:url["\']\s+content=["\'](.*?)["\']',
        )

        if not title or title.split(" - ", 1)[0].strip().lower() in GENERIC_TITLES:
            failures.append(f"{route}: generic or missing title")
        if (
            not description
            or description.startswith(SITE_DESCRIPTION_START)
            or any(fragment in description for fragment in BAD_DESCRIPTION_FRAGMENTS)
        ):
            failures.append(f"{route}: generic or missing description")
        if canonical and og_url and canonical != og_url:
            failures.append(f"{route}: og:url does not match canonical")

    if failures:
        print("[error] SEO metadata issues found:")
        for failure in failures[:80]:
            print(f"- {failure}")
        if len(failures) > 80:
            print(f"- ...and {len(failures) - 80} more")
        return 1

    print(f"[ok] SEO metadata: {checked} canonical pages checked")

    standalone_sitemap = SITE / "standalone-sitemap.xml"
    if standalone_sitemap.exists():
        sitemap = standalone_sitemap.read_text(encoding="utf-8", errors="ignore")
        if "404.html" in sitemap:
            print("[error] standalone sitemap includes 404.html")
            return 1

        standalone_failures: list[str] = []
        standalone_checked = 0
        for path in sorted(SITE.rglob("*.html")):
            if path.name in {"index.html", "404.html"}:
                continue

            stat = path.stat()
            if stat.st_size > 0 and stat.st_blocks == 0:
                continue
            html = path.read_text(encoding="utf-8", errors="ignore")
            if is_redirect(html):
                continue

            standalone_checked += 1
            route = route_for(path)
            description = attr(
                html,
                r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
            )
            canonical = attr(
                html,
                r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']',
            )
            og_title = attr(
                html,
                r'<meta\s+property=["\']og:title["\']\s+content=["\'](.*?)["\']',
            )

            if not description:
                standalone_failures.append(f"{route}: missing description")
            if not canonical:
                standalone_failures.append(f"{route}: missing canonical")
            if not og_title:
                standalone_failures.append(f"{route}: missing Open Graph title")

        if standalone_failures:
            print("[error] Standalone HTML SEO issues found:")
            for failure in standalone_failures[:80]:
                print(f"- {failure}")
            if len(standalone_failures) > 80:
                print(f"- ...and {len(standalone_failures) - 80} more")
            return 1

        print(f"[ok] SEO metadata: {standalone_checked} standalone HTML pages checked")

    return 0


if __name__ == "__main__":
    sys.exit(main())

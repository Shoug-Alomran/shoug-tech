#!/usr/bin/env python3
"""Keep docs/sitemap.xml and docs/standalone-sitemap.xml correct.

Rebuilds both sitemaps in memory with the same page selection optimize_site_html.py uses at deploy
(without rewriting any HTML), then validates the result and the page metadata it depends on.

    python3 scripts/check_sitemap.py          # report only; exit 1 if the sitemaps are stale or anything is wrong
    python3 scripts/check_sitemap.py --write  # also rewrite the two sitemap files when they are stale

Problems that regeneration cannot fix are page-level and must be fixed in the HTML:
  - a canonical that points to a page that does not exist
  - a folder page (index.html) whose canonical names some other page (copy-paste), which drops it from the sitemap
  - an inner page that defers its canonical to a page that is not itself in the sitemap
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parent))
import optimize_site_html as o  # noqa: E402

LINK_TAG = re.compile(r"<link\b[^>]*>", re.IGNORECASE)
REL_CANONICAL = re.compile(r'rel=["\']canonical["\']', re.IGNORECASE)
HREF = re.compile(r'href=["\']([^"\']+)', re.IGNORECASE)
LOC = re.compile(r"<loc>([^<]*)</loc>")


def declared_canonical(html: str) -> str | None:
    for tag in LINK_TAG.findall(html):
        if REL_CANONICAL.search(tag):
            match = HREF.search(tag)
            return match.group(1) if match else None
    return None


def resolve(url: str) -> Path | None:
    if not url.startswith(o.SITE_URL):
        return None
    rel = unquote(url[len(o.SITE_URL):].split("?")[0].split("#")[0])
    path = o.SITE / rel
    if rel == "" or rel.endswith("/"):
        path = path / "index.html"
    return path if path.is_file() else None


def build() -> tuple[list[Path], list[Path], dict[Path, str]]:
    standalone, all_pages, canonicals = [], [], {}
    for path in sorted(o.SITE.rglob("*.html")):
        stat = path.stat()
        if stat.st_size == 0 or stat.st_blocks == 0:
            continue  # offline filesystem placeholder
        html = path.read_text(encoding="utf-8")
        # Same in-memory transforms the deploy build applies; nothing is written back.
        for fn in (o.patch_accessibility, o.update_brand_favicon, o.optimize_images):
            html = fn(html)
        html = o.add_clarity(o.add_alternates(o.ensure_meta(html, path), path))
        if o.is_indexable_standalone(path, html):
            standalone.append(path)
        if o.is_indexable(path, html):
            all_pages.append(path)
        if not (path.name == "404.html" or o.is_redirect(html) or o.is_noindex(html)):
            canonical = declared_canonical(html)
            if canonical:
                canonicals[path] = canonical
    return standalone, all_pages, canonicals


def render(paths: list[Path]) -> str:
    urls = [
        "    <url>\n" f"        <loc>{o.escape_attr(o.canonical_url(p))}</loc>\n" "    </url>"
        for p in sorted(paths)
    ]
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )


def main() -> int:
    write = "--write" in sys.argv[1:]
    standalone, all_pages, canonicals = build()
    problems: list[str] = []
    rewritten: list[str] = []

    for filename, paths in ((o.STANDALONE_SITEMAP, standalone), (o.SITEMAP, all_pages)):
        target = o.SITE / filename
        expected = render(paths)
        current = target.read_text(encoding="utf-8") if target.exists() else ""
        if current != expected:
            if write:
                o.write_urlset(filename, paths)
                rewritten.append(f"{filename} ({len(paths)} URLs)")
            else:
                problems.append(f"{filename} is stale: run python3 scripts/check_sitemap.py --write")

        # Validate what is on disk now (post-write), so a bad generator change is caught too.
        locs = LOC.findall(target.read_text(encoding="utf-8")) if target.exists() else []
        seen: set[str] = set()
        for loc in locs:
            if loc in seen:
                problems.append(f"{filename}: duplicate {loc}")
            seen.add(loc)
            page = resolve(loc)
            if page is None:
                problems.append(f"{filename}: broken {loc}")
                continue
            html = page.read_text(encoding="utf-8")
            if o.is_noindex(html):
                problems.append(f"{filename}: noindex page listed {loc}")
            if o.is_redirect(html):
                problems.append(f"{filename}: redirect page listed {loc}")
            canonical = declared_canonical(html)
            if canonical and canonical != loc:
                problems.append(f"{filename}: {loc} declares canonical {canonical}")

    listed = {o.canonical_url(p) for p in all_pages}
    for path, canonical in canonicals.items():
        rel = path.relative_to(o.SITE).as_posix()
        own = o.canonical_url(path)
        if canonical.startswith(o.SITE_URL) and resolve(canonical) is None:
            problems.append(f"{rel}: canonical points to a page that does not exist: {canonical} (expected {own})")
        elif canonical == own:
            continue
        elif path.name == "index.html":
            problems.append(f"{rel}: folder page canonical names another page {canonical} -- set canonical/og:url/hreflang to {own}")
        elif canonical.startswith(o.SITE_URL) and canonical not in listed:
            problems.append(f"{rel}: canonical {canonical} is not an indexable page, so neither URL reaches the sitemap")

    for line in rewritten:
        print(f"[ok] rewrote stale {line}")
    if problems:
        print(f"[error] {len(problems)} sitemap problem(s):")
        for line in problems[:60]:
            print(f"  {line}")
        if len(problems) > 60:
            print(f"  ... and {len(problems) - 60} more")
        return 1
    print(f"[ok] sitemaps valid: {len(all_pages)} URLs, {len(standalone)} standalone")
    return 0


if __name__ == "__main__":
    sys.exit(main())

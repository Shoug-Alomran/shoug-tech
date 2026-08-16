#!/usr/bin/env python3
"""Point generated mindmap pages at their own canonical URL.

build_se401_study_tools.mindmap_html() renders every map from the ETHCS303
chapter-1 page and rewrites the description/OG/Twitter tags, but never rewrote
the canonical, og:url, or hreflang alternates. Every map generated from it -
SE322, SE401, CYS405, CYS406 - therefore declared the ETHCS303 ethics page as
its canonical, so search engines saw ~49 duplicates of one URL.

This rewrites those four URL tags to each page's own address. Pages whose
canonical is a deliberate legacy alias (a pre-restructure path for the same
document) are left alone.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SITE = "https://shoug-tech.com"

TAGS = (
    r'(<link rel="canonical" href=")[^"]*(">)',
    r'(<meta property="og:url" content=")[^"]*(">)',
    r'(<link rel="alternate" hreflang="en" href=")[^"]*(">)',
    r'(<link rel="alternate" hreflang="x-default" href=")[^"]*(">)',
)


def site_path(page: Path) -> str:
    """The page's own canonical path, using the site's capitalised /Academics/ form."""
    relative = str(page.relative_to(DOCS))
    return "/" + re.sub(r"^academics/", "Academics/", relative)


def stale_pages():
    """Generated map pages whose canonical does not point at themselves.

    Only ``*/mindmaps/*/`` content pages are considered. They are all generated
    by this repo's build scripts and have no pre-restructure URLs, so a
    mismatch here is always a bug rather than a deliberate legacy alias.
    """
    for page in sorted(DOCS.rglob("*/mindmaps/*/*.html")):
        if page.name == "index.html":
            continue
        text = page.read_text(errors="ignore")
        match = re.search(r'<link rel="canonical" href="([^"]*)"', text)
        if match and match.group(1) != SITE + site_path(page):
            yield page, text


def main() -> int:
    fixed = 0
    for page, text in stale_pages():
        path = site_path(page)
        for tag in TAGS:
            text = re.sub(tag, lambda m: m.group(1) + SITE + path + m.group(2), text, count=1)
        text = re.sub(r'(<link rel="alternate" hreflang="ar" href=")[^"]*(">)',
                      lambda m: m.group(1) + SITE + "/ar" + path + m.group(2), text, count=1)
        text = re.sub(r'("@type":"WebPage","url":")[^"]*(")',
                      lambda m: m.group(1) + SITE + path + m.group(2), text, count=1)
        page.write_text(text)
        fixed += 1
        print("fixed", page.relative_to(DOCS))
    print(f"{fixed} mindmap page(s) repointed at their own canonical")
    return 0


if __name__ == "__main__":
    sys.exit(main())

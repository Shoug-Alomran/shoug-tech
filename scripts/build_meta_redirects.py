#!/usr/bin/env python3
"""Turn meta-refresh redirect pages into real 301 redirects on Cloudflare Pages.

Old pages forward visitors with <meta http-equiv="refresh">, which many bots and
AI fetchers do not follow, so they stop at a near-empty page. This writes
.pages-build/meta-redirects.json (old path -> new path), which the Pages
middleware in functions/_middleware.js answers with a 301, and docs/_routes.json,
which tells Pages which requests run the middleware (shared scripts, styles and
images skip it, which keeps it well inside the free 100,000 requests a day).
Runs at deploy on the final build output; the stub pages stay as a fallback:

    python3 scripts/build_meta_redirects.py
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = ROOT / ".pages-build" / "meta-redirects.json"
ROUTES = {
    "version": 1,
    "include": ["/*"],
    "exclude": ["/assets/*", "/javascripts/*", "/styles/*", "/ai-context/*", "/search-index.json",
                "/search-pdf-index.json", "/sw.js", "/favicon.ico", "/site.webmanifest"],
}
ORIGIN = "https://shoug-tech.com"
REFRESH = re.compile(r'<meta[^>]*http-equiv=["\']refresh["\'][^>]*content=["\'][^"\']*?url=([^"\'>]+)', re.I)
EXCLUDED = "/ethcs303/"


def route(page: Path) -> str:
    rel = "/" + page.relative_to(DOCS).as_posix()
    return rel[: -len("index.html")] if rel.endswith("/index.html") else rel


def exists(target: str) -> bool:
    path = urlsplit(target).path
    file = DOCS / path.lstrip("/")
    return (file / "index.html").is_file() if path.endswith("/") else file.is_file()


def main() -> int:
    found: dict[str, str] = {}
    for page in DOCS.rglob("*.html"):
        match = REFRESH.search(page.read_text(encoding="utf-8", errors="ignore")[:20000])
        source = route(page)
        if not match or EXCLUDED in source:
            continue
        target = urljoin(ORIGIN + source, html.unescape(match.group(1)).strip())
        if not target.startswith(ORIGIN + "/"):
            continue
        target = target[len(ORIGIN):]
        if exists(target) and urlsplit(target).path != source:
            found[source] = target

    def final(target: str) -> str:
        # Collapse chains so every redirect is a single hop.
        seen = set()
        while urlsplit(target).path in found and target not in seen:
            seen.add(target)
            target = found[urlsplit(target).path]
        return target

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({s: final(t) for s, t in sorted(found.items())}, indent=1) + "\n", encoding="utf-8")
    (DOCS / "_routes.json").write_text(json.dumps(ROUTES, indent=1) + "\n", encoding="utf-8")
    print(f"{OUT.relative_to(ROOT)}: {len(found)} redirects from refresh pages; wrote docs/_routes.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

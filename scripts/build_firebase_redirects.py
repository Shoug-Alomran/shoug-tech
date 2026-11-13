#!/usr/bin/env python3
"""Turn meta-refresh redirect pages into real 301 redirects in firebase.json.

Old pages forward visitors with <meta http-equiv="refresh">, which many bots and
AI fetchers do not follow, so they stop at a near-empty page. Firebase Hosting
applies firebase.json redirects before serving files. Runs in the deploy job on
the final build output; the stub pages stay as a fallback:

    python3 scripts/build_firebase_redirects.py
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
CONFIG = ROOT / "firebase.json"
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
        head = page.read_text(encoding="utf-8", errors="ignore")[:20000]
        match = REFRESH.search(head)
        source = route(page)
        if not match or EXCLUDED in source:
            continue
        target = urljoin(ORIGIN + source, html.unescape(match.group(1)).strip())
        if not target.startswith(ORIGIN + "/"):
            continue
        target = target[len(ORIGIN):]
        if exists(target) and urlsplit(target).path != source:
            found[source] = target
    # Collapse chains so every redirect is a single hop.
    def final(target: str) -> str:
        seen = set()
        while urlsplit(target).path in found and target not in seen:
            seen.add(target)
            target = found[urlsplit(target).path]
        return target

    rules = []
    for source in sorted(found):
        escaped = re.escape(source)
        pattern = f"^{escaped}(?:index\\.html)?$" if source.endswith("/") else f"^{escaped}$"
        if source.endswith("/"):
            pattern = f"^{re.escape(source[:-1])}(?:/|/index\\.html)?$"
        rules.append({"regex": pattern, "destination": final(found[source]), "type": 301})
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    config["hosting"]["redirects"] = rules
    CONFIG.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    print(f"firebase.json: {len(rules)} redirects from refresh pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

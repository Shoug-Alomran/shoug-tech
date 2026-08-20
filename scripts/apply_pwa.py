#!/usr/bin/env python3
"""Link the web app manifest and register the service worker on every page.

Skips documents that are only ever loaded inside another page's iframe: a
nested frame registering its own worker duplicates work and the manifest is
meaningless there.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

DOCS = Path(__file__).resolve().parent.parent / "docs"

MANIFEST = '<link rel="manifest" href="/site.webmanifest">'
THEME = '<meta name="theme-color" content="#050508">'
SW = '<script src="/javascripts/register-sw.js" defer></script>'

HEAD_CLOSE = re.compile(r"</head>", re.I)
BODY_CLOSE = re.compile(r"</body>", re.I)
SRC = re.compile(r'<(?:iframe|embed)[^>]*\bsrc="([^"]+)"', re.I)

SKIP_FILES = {"offline.html"}


def embedded_documents() -> set[Path]:
    embedded: set[Path] = set()
    for p in DOCS.rglob("*.html"):
        text = p.read_text(encoding="utf-8", errors="ignore")
        for src in SRC.findall(text):
            path = unquote(urlsplit(src).path)
            if not path.endswith(".html"):
                continue
            target = (DOCS / path.lstrip("/")) if path.startswith("/") \
                else (p.parent / path)
            try:
                target = target.resolve()
            except OSError:
                continue
            if target.is_file() and target != p.resolve():
                embedded.add(target)
    return embedded


def main() -> int:
    apply = "--apply" in sys.argv
    embedded = embedded_documents()
    touched = 0

    for p in sorted(DOCS.rglob("*.html")):
        if p.name in SKIP_FILES or p.resolve() in embedded:
            continue

        text = p.read_text(encoding="utf-8", errors="ignore")
        original = text

        head = HEAD_CLOSE.search(text)
        if head:
            additions = []
            if 'rel="manifest"' not in text:
                additions.append(MANIFEST)
            if 'name="theme-color"' not in text:
                additions.append(THEME)
            if additions:
                block = "\n" + "\n".join("    " + a for a in additions) + "\n"
                text = text[: head.start()] + block + text[head.start():]

        if "register-sw.js" not in text:
            body = BODY_CLOSE.search(text)
            if body:
                text = text[: body.start()] + SW + "\n" + text[body.start():]

        if text != original:
            touched += 1
            if apply:
                p.write_text(text, encoding="utf-8")

    verb = "updated" if apply else "would update"
    print(f"{verb} {touched} pages ({len(embedded)} embedded documents skipped)")
    if not apply:
        print("re-run with --apply to write changes")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Give every page a real <h1>.

100 pages render their title as a styled <div> (.hdr-title, .nav-title and
friends), so crawlers and screen readers saw a document with no heading at
all. Promoting those divs would inherit heading margins and shift bespoke
layouts, so a visually hidden <h1> carrying the page title is inserted
instead -- announced and indexed, invisible on screen.
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
BODY = re.compile(r"<body\b[^>]*>", re.I)
SKIP = re.compile(r'<a class="shoug-skip-link"[^>]*>.*?</a>', re.S | re.I)

BRAND_SUFFIXES = (
    " — SHOUG.TECH", " | SHOUG.TECH", " · SHOUG.TECH",
    " // SHOUG.TECH", " - SHOUG.TECH",
)


def heading_text(raw: str) -> str:
    t = html.unescape(re.sub(r"\s+", " ", raw)).strip()
    for suffix in BRAND_SUFFIXES:
        if t.upper().endswith(suffix.upper()):
            t = t[: -len(suffix)]
            break
    t = t.strip(" -–—|·/")
    return t


def main() -> int:
    apply = "--apply" in sys.argv
    added = skipped = 0

    for p in sorted(DOCS.rglob("*.html")):
        text = p.read_text(encoding="utf-8", errors="ignore")
        if "<h1" in text:
            continue

        tm = TITLE.search(text)
        if not tm:
            skipped += 1
            continue
        label = heading_text(tm.group(1))
        if not label:
            skipped += 1
            continue

        bm = BODY.search(text)
        if not bm:
            skipped += 1
            continue

        # Sit after the skip link so it stays the first focusable element.
        insert_at = bm.end()
        sm = SKIP.search(text, bm.end(), bm.end() + 400)
        if sm:
            insert_at = sm.end()

        tag = (f'\n<h1 class="shoug-visually-hidden">'
               f'{html.escape(label)}</h1>')
        text = text[:insert_at] + tag + text[insert_at:]
        added += 1
        if apply:
            p.write_text(text, encoding="utf-8")

    verb = "added" if apply else "would add"
    print(f"{verb} {added} hidden headings" +
          (f", {skipped} pages skipped (no usable title)" if skipped else ""))
    if not apply:
        print("re-run with --apply to write changes")
    return 0


if __name__ == "__main__":
    sys.exit(main())

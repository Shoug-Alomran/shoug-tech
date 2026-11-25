#!/usr/bin/env python3
"""Add read-aloud (docs/javascripts/slide-reader.js) to Annotated Slides decks and slide breakdowns.

Safe to run again: a page that already has the tag gets its ?v= updated, nothing else.
Wrapper pages (index.html) are skipped: they show the deck or lesson in an iframe, and the
file inside that iframe carries the script."""
import re
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"
VERSION = "1"
TAG = f'<script src="/javascripts/slide-reader.js?v={VERSION}" defer></script>'
EXISTING = re.compile(r'<script src="/javascripts/slide-reader\.js(?:\?v=[^"]*)?"(?: defer)?></script>')


def pages():
    for page in DOCS.glob("academics/*/*/annotated-slides/*/*.html"):
        if page.name != "index.html":
            yield page, "data-slide="
    for page in DOCS.glob("academics/*/*/slide-breakdowns/**/*.html"):
        if page.name != "index.html":
            yield page, None


def main():
    changed = 0
    for page, needle in pages():
        text = page.read_text(encoding="utf-8")
        if needle and needle not in text:
            continue
        if EXISTING.search(text):
            updated = EXISTING.sub(TAG, text, count=1)
        elif "</body>" in text:
            updated = text.replace("</body>", TAG + "\n</body>", 1)
        else:
            continue
        if updated != text:
            page.write_text(updated, encoding="utf-8")
            changed += 1
    print(f"Read-aloud installed or updated on {changed} pages.")


if __name__ == "__main__":
    main()

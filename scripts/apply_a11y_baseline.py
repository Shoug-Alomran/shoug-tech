#!/usr/bin/env python3
"""Add the accessibility baseline to every page carrying the site chrome.

Three things, all idempotent:
  1. link styles/a11y.css (skip link, focus rings, reduced motion)
  2. insert a "Skip to content" link as the first focusable element
  3. give <main> an id + tabindex="-1" so the skip link can land on it

A skip link only earns its place where there is navigation to skip: pages
with the site chrome, and standalone study documents that carry their own
in-page <nav>. Documents with neither get the stylesheet only.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
CSS_HREF = "/styles/a11y.css"
CSS_LINK = f'<link rel="stylesheet" href="{CSS_HREF}">'
SKIP_ID = "main-content"
SKIP_LINK = (
    f'<a class="shoug-skip-link" href="#{SKIP_ID}">Skip to content</a>'
)

BODY_OPEN = re.compile(r"<body\b[^>]*>", re.I)
MAIN_OPEN = re.compile(r"<main\b([^>]*)>", re.I)
HEAD_CLOSE = re.compile(r"</head>", re.I)
# One page's CSS comment describes the layout using the literal text "<main>".
# Matching that instead of the element put the skip target inside a comment,
# so anything before </style> or inside a comment is masked out first.
MASKED = re.compile(r"<style\b.*?</style>|<script\b.*?</script>|<!--.*?-->", re.S | re.I)


def add_stylesheet(text: str) -> str:
    if CSS_HREF in text:
        return text
    m = HEAD_CLOSE.search(text)
    if not m:
        return text
    return text[: m.start()] + "    " + CSS_LINK + "\n" + text[m.start():]


def add_skip_link(text: str) -> str:
    if "shoug-skip-link" in text:
        return text

    # Search a copy with style/script/comment regions blanked so offsets still
    # line up with the real document.
    haystack = MASKED.sub(lambda mm: " " * len(mm.group(0)), text)
    m = MAIN_OPEN.search(haystack)
    if not m:
        return text

    attrs = m.group(1)
    if re.search(r'\bid\s*=\s*"', attrs):
        target = re.search(r'\bid\s*=\s*"([^"]*)"', attrs).group(1)
        new_main = m.group(0)
    else:
        target = SKIP_ID
        new_main = f'<main{attrs} id="{SKIP_ID}" tabindex="-1">'

    if 'tabindex=' not in new_main:
        new_main = new_main[:-1] + ' tabindex="-1">'

    text = text[: m.start()] + new_main + text[m.end():]

    link = f'<a class="shoug-skip-link" href="#{target}">Skip to content</a>'
    b = BODY_OPEN.search(text)
    if not b:
        return text
    return text[: b.end()] + "\n" + link + text[b.end():]


def main() -> int:
    apply = "--apply" in sys.argv
    styled = skipped = 0

    for p in sorted(DOCS.rglob("*.html")):
        original = p.read_text(encoding="utf-8", errors="ignore")
        text = add_stylesheet(original)
        if text != original:
            styled += 1

        # Either the site chrome, or a document with its own table-of-contents
        # nav that a keyboard user would otherwise tab through every visit.
        needs_skip = "shoug-site-header" in text or (
            "<nav" in text and "<main" in text
        )
        if needs_skip:
            before = text
            text = add_skip_link(text)
            if text != before:
                skipped += 1

        if text != original and apply:
            p.write_text(text, encoding="utf-8")

    verb = "updated" if apply else "would update"
    print(f"{verb}: {styled} pages linked {CSS_HREF}, {skipped} gained a skip link")
    if not apply:
        print("re-run with --apply to write changes")
    return 0


if __name__ == "__main__":
    sys.exit(main())

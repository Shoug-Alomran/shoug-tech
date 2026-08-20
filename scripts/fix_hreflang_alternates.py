#!/usr/bin/env python3
"""Point the Arabic hreflang alternates at the URL that actually serves Arabic.

The alternates were written as https://shoug-tech.com/ar/<path>, but there is
no /ar/ tree: javascripts/arabic-localization.js switches language in place off
a ?lang=ar query parameter. Every Arabic alternate therefore resolved to a 404,
which tells search engines the translation does not exist.

Rewrites each ar alternate to the page's own canonical URL plus ?lang=ar.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"

AR_ALT = re.compile(
    r'<link\s+rel="alternate"\s+hreflang="ar"\s+href="([^"]*)"\s*/?>',
    re.I,
)
CANONICAL = re.compile(r'<link\s+rel="canonical"\s+href="([^"]*)"\s*/?>', re.I)


def main() -> int:
    apply = "--apply" in sys.argv
    fixed = skipped = 0

    for p in sorted(DOCS.rglob("*.html")):
        text = p.read_text(encoding="utf-8", errors="ignore")
        m = AR_ALT.search(text)
        if not m:
            continue

        canon = CANONICAL.search(text)
        if not canon:
            skipped += 1
            continue

        base = canon.group(1)
        target = base + ("&" if "?" in base else "?") + "lang=ar"
        if m.group(1) == target:
            continue

        new_tag = f'<link rel="alternate" hreflang="ar" href="{target}">'
        out = text[: m.start()] + new_tag + text[m.end():]
        fixed += 1
        if apply:
            p.write_text(out, encoding="utf-8")

    verb = "fixed" if apply else "would fix"
    print(f"{verb} {fixed} Arabic alternates")
    if skipped:
        print(f"{skipped} pages skipped (no canonical to derive the URL from)")
    if not apply:
        print("re-run with --apply to write changes")
    return 0


if __name__ == "__main__":
    sys.exit(main())

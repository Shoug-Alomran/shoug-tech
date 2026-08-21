#!/usr/bin/env python3
"""Rebuild the hreflang alternates from each page's canonical URL.

Two separate defects produced alternates that resolved to 404s:

  * Arabic alternates were written as https://shoug-tech.com/ar/<path>, but
    there is no /ar/ tree -- javascripts/arabic-localization.js switches
    language in place off a ?lang=ar query parameter.

  * Some pages kept en/x-default alternates pointing at paths from an earlier
    site structure (flat slide-breakdowns/Chapter-2/ rather than the numbered
    folders used now).

The canonical is the one URL each page already asserts is correct, so all
three alternates are derived from it: en and x-default match it exactly, ar
appends ?lang=ar.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"

def alt_pattern(lang: str) -> re.Pattern[str]:
    return re.compile(
        r'<link\s+rel="alternate"\s+hreflang="' + re.escape(lang)
        + r'"\s+href="([^"]*)"\s*/?>',
        re.I,
    )


ALTS = {lang: alt_pattern(lang) for lang in ("en", "ar", "x-default")}
CANONICAL = re.compile(r'<link\s+rel="canonical"\s+href="([^"]*)"\s*/?>', re.I)


def main() -> int:
    apply = "--apply" in sys.argv
    fixed = skipped = 0

    for p in sorted(DOCS.rglob("*.html")):
        text = p.read_text(encoding="utf-8", errors="ignore")
        if "hreflang" not in text:
            continue

        canon = CANONICAL.search(text)
        if not canon:
            skipped += 1
            continue

        base = canon.group(1)
        targets = {
            "en": base,
            "x-default": base,
            "ar": base + ("&" if "?" in base else "?") + "lang=ar",
        }

        changed = False
        for lang, pattern in ALTS.items():
            m = pattern.search(text)
            if not m or m.group(1) == targets[lang]:
                continue
            tag = (f'<link rel="alternate" hreflang="{lang}" '
                   f'href="{targets[lang]}">')
            text = text[: m.start()] + tag + text[m.end():]
            changed = True

        if not changed:
            continue

        fixed += 1
        if apply:
            p.write_text(text, encoding="utf-8")

    verb = "fixed" if apply else "would fix"
    print(f"{verb} hreflang alternates on {fixed} pages")
    if skipped:
        print(f"{skipped} pages skipped (no canonical to derive the URL from)")
    if not apply:
        print("re-run with --apply to write changes")
    return 0


if __name__ == "__main__":
    sys.exit(main())

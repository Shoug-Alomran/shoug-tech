#!/usr/bin/env python3
"""Correct the casing of site URLs inside JSON-LD structured data.

fix_link_case.py only touches href/src/content attributes, so the URLs Google
reads out of <script type="application/ld+json"> kept pointing at the
capitalised /Academics/ path that 404s on GitHub Pages.

Scoped to ld+json blocks on purpose: the site's own JavaScript contains the
regex literal /Academics/g, which a blind search-and-replace would corrupt.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
LD_BLOCK = re.compile(
    r'(<script[^>]*type\s*=\s*["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',
    re.I | re.S,
)
SITE_URL = re.compile(r'(https://(?:www\.)?shoug-tech\.com)(/[^"\'\\\s]*)')

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix_link_case import real_path  # noqa: E402


def fix_block(body: str) -> tuple[str, int]:
    count = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal count
        host, path = m.group(1), m.group(2)
        corrected = real_path(path)
        if corrected is None or corrected == path:
            return m.group(0)
        count += 1
        return host + corrected

    return SITE_URL.sub(repl, body), count


def main() -> int:
    apply = "--apply" in sys.argv
    pages = fixes = 0

    for p in sorted(DOCS.rglob("*.html")):
        text = p.read_text(encoding="utf-8", errors="ignore")
        if "ld+json" not in text:
            continue
        local = 0

        def repl(m: re.Match[str]) -> str:
            nonlocal local
            body, n = fix_block(m.group(2))
            local += n
            return m.group(1) + body + m.group(3)

        out = LD_BLOCK.sub(repl, text)
        if local:
            pages += 1
            fixes += local
            if apply:
                p.write_text(out, encoding="utf-8")

    verb = "fixed" if apply else "would fix"
    print(f"{verb} {fixes} JSON-LD URLs across {pages} pages")
    if not apply:
        print("re-run with --apply to write changes")
    return 0


if __name__ == "__main__":
    sys.exit(main())

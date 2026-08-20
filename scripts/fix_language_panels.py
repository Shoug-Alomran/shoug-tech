#!/usr/bin/env python3
"""Repair the bilingual embed panels.

Two defects, both invisible until you switch a page to Arabic:

  1. syncLanguagePanels(lang) ignored its argument and hard-coded 'en', so the
     Arabic panel was hidden on every page that had one -- the translations
     were shipped but unreachable.

  2. 49 Arabic panels point at .ar.html files that were never generated. Once
     defect 1 is fixed those would render a 404 inside the frame, so the dead
     panels are removed and the page falls back to English.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

DOCS = Path(__file__).resolve().parent.parent / "docs"

BROKEN = "panel.hidden = panel.getAttribute('data-lang-panel') !== 'en';"
FIXED = (
    "var wanted = panels.some(function (p) "
    "{ return p.getAttribute('data-lang-panel') === lang; }) ? lang : 'en';\n"
    "                    panels.forEach(function (panel) {\n"
    "                        panel.hidden = "
    "panel.getAttribute('data-lang-panel') !== wanted;"
)

# The whole forEach wrapper is replaced so the fallback is computed once.
OLD_LOOP = re.compile(
    r"panels\.forEach\(function \(panel\) \{\s*"
    r"panel\.hidden = panel\.getAttribute\('data-lang-panel'\) !== 'en';",
)

AR_PANEL = re.compile(
    r'<div class="rendered-content" data-lang-panel="ar"[^>]*>.*?</div>',
    re.S,
)
SRC = re.compile(r'src="([^"]+)"')


def panel_target_missing(panel_html: str, page: Path) -> bool:
    m = SRC.search(panel_html)
    if not m:
        return False
    path = unquote(urlsplit(m.group(1)).path)
    target = (DOCS / path.lstrip("/")) if path.startswith("/") else (page.parent / path)
    return not target.is_file()


def main() -> int:
    apply = "--apply" in sys.argv
    logic_fixed = panels_removed = 0
    pages = set()

    for p in sorted(DOCS.rglob("*.html")):
        text = p.read_text(encoding="utf-8", errors="ignore")
        original = text

        if BROKEN in text:
            text = OLD_LOOP.sub(FIXED, text)
            logic_fixed += 1

        if 'data-lang-panel="ar"' in text:
            def drop(m: re.Match[str]) -> str:
                nonlocal panels_removed
                if panel_target_missing(m.group(0), p):
                    panels_removed += 1
                    return ""
                return m.group(0)
            text = AR_PANEL.sub(drop, text)

        if text != original:
            pages.add(p)
            if apply:
                p.write_text(text, encoding="utf-8")

    verb = "fixed" if apply else "would fix"
    print(f"{verb}: {logic_fixed} pages' panel logic, "
          f"{panels_removed} dead Arabic panels removed, "
          f"{len(pages)} pages touched")
    if not apply:
        print("re-run with --apply to write changes")
    return 0


if __name__ == "__main__":
    sys.exit(main())

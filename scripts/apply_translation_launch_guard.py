#!/usr/bin/env python3
"""Temporarily remove language toggles without deleting translations."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
INCLUDE = '    <script src="/javascripts/translation-launch-guard.js"></script>\n'
TOGGLE_RE = re.compile(
    r"\s*<(?:button|a)\b(?=[^>]*(?:data-lang-toggle|class=[\"'][^\"']*\bshoug-lang-btn\b))[^>]*>.*?</(?:button|a)>",
    re.I | re.S,
)


def main() -> None:
    updated = 0
    for path in DOCS.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        cleaned = TOGGLE_RE.sub("", text)
        if "translation-launch-guard.js" not in cleaned:
            cleaned = cleaned.replace("</head>", INCLUDE + "</head>", 1)
        if cleaned != text:
            path.write_text(cleaned, encoding="utf-8")
            updated += 1
    print(f"Removed visible translation toggles from {updated} HTML files")


if __name__ == "__main__":
    main()

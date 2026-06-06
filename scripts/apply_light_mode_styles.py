#!/usr/bin/env python3
"""Attach the shared light-mode polish stylesheet to theme-aware HTML pages."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
INCLUDE = '    <link rel="stylesheet" href="/styles/light-mode.css">\n'


def main() -> None:
    updated = 0
    for path in DOCS.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        if "shoug-light-mode" not in text or "/styles/light-mode.css" in text:
            continue
        path.write_text(text.replace("</head>", INCLUDE + "</head>", 1), encoding="utf-8")
        updated += 1
    print(f"Added shared light-mode styles to {updated} HTML files")


if __name__ == "__main__":
    main()


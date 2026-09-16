#!/usr/bin/env python3
"""Install the progressive contents disclosure in standalone breakdowns."""
import hashlib
import os
import re
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"


def main():
    changed = 0
    for page in DOCS.glob("academics/*/*/slide-breakdowns/**/*.html"):
        if page.name == "index.html":
            continue
        text = page.read_text()
        original = text
        for kind, folder in [("css", "styles"), ("js", "javascripts")]:
            asset = DOCS / folder / f"breakdown-contents.{kind}"
            url = os.path.relpath(asset, page.parent) + "?v=" + hashlib.sha256(asset.read_bytes()).hexdigest()[:12]
            pattern = rf'[^"\s<>]*breakdown-contents\.{kind}(?:\?v=[a-f0-9]+)?'
            if re.search(pattern, text):
                text = re.sub(pattern, url, text)
            else:
                tag = f'<link rel="stylesheet" href="{url}">' if kind == "css" else f'<script src="{url}" defer></script>'
                text = text.replace("</head>", tag + "\n</head>", 1)
        if text != original:
            page.write_text(text)
            changed += 1
    print(f"Updated {changed} breakdown pages.")


if __name__ == "__main__":
    main()

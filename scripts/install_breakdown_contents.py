#!/usr/bin/env python3
"""Install the progressive contents disclosure in standalone breakdowns.

    python3 scripts/install_breakdown_contents.py                       # every course
    python3 scripts/install_breakdown_contents.py academics/business/econ102   # one course
"""
import hashlib
import os
import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"


def pages(roots):
    if not roots:
        return DOCS.glob("academics/*/*/slide-breakdowns/**/*.html")
    return (p for root in roots for p in (DOCS / root.strip("/")).glob("slide-breakdowns/**/*.html"))


def main():
    changed = 0
    for page in pages(sys.argv[1:]):
        if page.name == "index.html":
            continue
        text = page.read_text(encoding="utf-8")
        original = text
        for kind, folder in [("css", "styles"), ("js", "javascripts")]:
            asset = DOCS / folder / f"breakdown-contents.{kind}"
            # as_posix: a URL needs forward slashes, also on Windows.
            url = (Path(os.path.relpath(asset, page.parent)).as_posix()
                   + "?v=" + hashlib.sha256(asset.read_bytes()).hexdigest()[:12])
            pattern = rf'[^"\s<>]*breakdown-contents\.{kind}(?:\?v=[a-f0-9]+)?'
            if re.search(pattern, text):
                text = re.sub(pattern, lambda _m: url, text)
            else:
                tag = f'<link rel="stylesheet" href="{url}">' if kind == "css" else f'<script src="{url}" defer></script>'
                text = text.replace("</head>", tag + "\n</head>", 1)
        if text != original:
            page.write_text(text, encoding="utf-8", newline="")
            changed += 1
    print(f"Updated {changed} breakdown pages.")


if __name__ == "__main__":
    main()

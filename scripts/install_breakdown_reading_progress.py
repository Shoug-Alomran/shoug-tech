#!/usr/bin/env python3
"""Install live section highlighting and remaining-section progress on breakdown lessons."""
import hashlib
import os
import re
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"


def asset_url(asset: Path, page: Path) -> str:
    relative = Path(os.path.relpath(asset, page.parent)).as_posix()
    version = hashlib.sha256(asset.read_bytes()).hexdigest()[:12]
    return f"{relative}?v={version}"


def main() -> None:
    css = DOCS / "styles" / "breakdown-reading-progress.css"
    js = DOCS / "javascripts" / "breakdown-reading-progress.js"
    css_tag = '<link rel="stylesheet" href="{url}">'
    js_tag = '<script src="{url}" defer></script>'
    legacy = re.compile(
        r'\s*<link rel="stylesheet" href="[^"]*se423-reading-progress\.css(?:\?v=[a-f0-9]+)?">\s*'
        r'<script src="[^"]*se423-reading-progress\.js(?:\?v=[a-f0-9]+)?" defer></script>',
        re.I,
    )
    changed = 0
    for page in DOCS.glob("academics/*/*/slide-breakdowns/**/*.html"):
        if page.name == "index.html":
            continue
        text = page.read_text(encoding="utf-8")
        original = text
        text = legacy.sub("", text)
        tags = [
            css_tag.format(url=asset_url(css, page)),
            js_tag.format(url=asset_url(js, page)),
        ]
        patterns = (
            r'<link rel="stylesheet" href="[^"]*breakdown-reading-progress\.css(?:\?v=[a-f0-9]+)?">',
            r'<script src="[^"]*breakdown-reading-progress\.js(?:\?v=[a-f0-9]+)?" defer></script>',
        )
        for pattern, tag in zip(patterns, tags):
            if re.search(pattern, text, re.I):
                text = re.sub(pattern, tag, text, count=1, flags=re.I)
            elif "</head>" in text:
                text = text.replace("</head>", "    " + tag + "\n  </head>", 1)
        if text != original:
            page.write_text(text, encoding="utf-8", newline="")
            changed += 1
    print(f"Installed or updated reading progress on {changed} breakdown pages.")


if __name__ == "__main__":
    main()

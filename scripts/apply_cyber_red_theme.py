#!/usr/bin/env python3
"""Keep the cybersecurity track red: no purple anywhere under /academics/cybersecurity/.

The cyber pages were cloned from the purple site design, so their inline CSS, markup
and generated scripts still carry purple accents (brand glow, tab and hover colours,
mindmap levels, breakdown and exam accents) and violet-tinted surfaces. This rewrites
those colours to red or neutral equivalents and links /styles/cyber-track.css, which
overrides what the shared stylesheets and runtime scripts inject (light mode, search,
PDF embeds) and gives the tab bar the bracketed mono style of the overview sub-nav.

    python3 scripts/apply_cyber_red_theme.py            # rewrite the cybersecurity pages
    python3 scripts/apply_cyber_red_theme.py --check    # list pages that still need it; exit 1 if any
    python3 scripts/apply_cyber_red_theme.py PATH ...   # limit to files or folders

Idempotent. Course builders call apply_tree() after generating pages, and the deploy
workflow runs it as a safety net.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CYBER = ROOT / "docs/academics/cybersecurity"
STYLESHEET = '<link rel="stylesheet" href="/styles/cyber-track.css">'

HEX = {
    # Saturated purple accents -> reds.
    "b829ea": "ff2a4b", "d978ff": "ff5c77", "a855f7": "ff4d6a", "aa59f7": "ff4d6a", "9933ff": "e11d48",
    "b366ff": "ff5c77", "bf6de8": "ff6b81", "9b3fc8": "d91a3a", "764ba2": "9f1239", "c084fc": "ff8095",
    "7c3aed": "d91a3a", "8250df": "a40e26", "d2a8ff": "ff9aa8", "a78bfa": "ff4d6a", "bb72ff": "ff5c77",
    "7536b5": "b3122e", "c4b5fd": "ff9aa8",
    # Violet-tinted surfaces and muted text -> neutral, faintly warm equivalents.
    "110822": "140a0c", "2a1b3d": "2d1a1f", "241a31": "261a1d", "21152f": "221417", "2a1f3d": "3a1c22",
    "ede9fe": "fde8ec", "8b7ea8": "9a9499", "ebe7f4": "efeaeb", "e2d9f3": "ece3e5", "f0eafa": "f7eeef",
    "4a3b69": "4d3a40",
}
# Pinks (#f472b6, #e11d90, #ff3fa4) are not purple and stay.
RGB = {
    (184, 41, 234): (255, 42, 75), (167, 139, 250): (255, 77, 106), (168, 85, 247): (255, 77, 106),
    (170, 89, 247): (255, 77, 106), (124, 58, 237): (217, 26, 58), (192, 132, 252): (255, 128, 149),
    (150, 120, 255): (255, 99, 120),
}
HEX_RE = re.compile(r"#(" + "|".join(HEX) + r")\b", re.I)
RGB_RE = re.compile(r"(rgba?\(\s*)(\d{1,3})(\s*,\s*)(\d{1,3})(\s*,\s*)(\d{1,3})")


def recolor(text: str) -> str:
    text = HEX_RE.sub(lambda m: "#" + HEX[m.group(1).lower()], text)

    def rgb(m: re.Match[str]) -> str:
        new = RGB.get((int(m.group(2)), int(m.group(4)), int(m.group(6))))
        if not new:
            return m.group(0)
        return f"{m.group(1)}{new[0]}{m.group(3)}{new[1]}{m.group(5)}{new[2]}"

    text = RGB_RE.sub(rgb, text)
    if "/styles/cyber-track.css" not in text:
        # Last in <head>, so it follows the page styles and the shared stylesheets it overrides.
        text, n = re.subn(r"</head>", STYLESHEET + "\n</head>", text, count=1, flags=re.I)
        if not n:
            # Formatter-minified wrappers omit </head>; <body> still closes the implicit head.
            text = re.sub(r"<body\b", STYLESHEET + "\n<body", text, count=1, flags=re.I)
    return text


def html_files(paths):
    for path in map(Path, paths):
        if path.is_dir():
            yield from sorted(path.rglob("*.html"))
        elif path.suffix == ".html":
            yield path


def apply_tree(paths=(CYBER,), write: bool = True) -> list[Path]:
    changed = []
    for page in html_files(paths):
        old = page.read_text(encoding="utf-8")
        new = recolor(old)
        if new != old:
            changed.append(page)
            if write:
                page.write_text(new, encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="*", default=[str(CYBER)])
    parser.add_argument("--check", action="store_true", help="report without writing; exit 1 if any page needs it")
    args = parser.parse_args()
    changed = apply_tree(args.paths, write=not args.check)
    if args.check:
        for page in changed:
            print(f"needs red theme: {page.relative_to(ROOT)}")
        return 1 if changed else 0
    print(f"red theme applied to {len(changed)} cybersecurity page(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

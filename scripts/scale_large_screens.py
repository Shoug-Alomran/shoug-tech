#!/usr/bin/env python3
"""Make viewport units survive the large-screen zoom in styles/site-shell.css.

On PCs, 1440p/4K monitors and TVs, site-shell.css sets `zoom` on <html> (with a
matching `--zoom-fix` custom property) so every page scales up like a laptop
layout instead of sitting in a narrow column. Chrome, Safari and Firefox
multiply vh/vw by that zoom, so `100vh` would become 1.5 screens tall. This
script rewrites every viewport length in CSS to `calc(<n>vh / var(--zoom-fix, 1))`,
which cancels the zoom exactly and is a no-op wherever no zoom applies.

Runs at deploy over the built docs/ (idempotent). Only CSS is touched: <style>
blocks, style="" attributes and .css files. @media/@container/@supports
conditions are left alone (var() is invalid there).

Pages whose inline scripts place elements from getBoundingClientRect (plan
grids, mind maps, calendar, analytics, bookmarks) get <html data-zoom="off">:
those app layouts already stretch to the screen, and their coordinate maths
assumes no zoom. Shared scripts handle zoom themselves via pageZoom().

Usage: python3 scripts/scale_large_screens.py docs [--check]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

UNIT = re.compile(r"(?<![\w.#-])(-?\d*\.?\d+)((?:d|s|l)?v(?:h|w|min|max|i|b))\b")
STYLE_BLOCK = re.compile(r"(<style\b[^>]*>)(.*?)(</style>)", re.S | re.I)
STYLE_ATTR = re.compile(r"""(\sstyle\s*=\s*)(["'])(.*?)\2""", re.S | re.I)
AT_RULE = re.compile(r"@(?:media|container|supports|import)\b[^{;]*", re.I)
MARK = "var(--zoom-fix"
SCRIPT_BLOCK = re.compile(r"<script\b(?![^>]*\bsrc=)[^>]*>(.*?)</script>", re.S | re.I)
PLACES = re.compile(r"style\.(?:left|top)\s*=|Object\.assign\(\s*\w+\.style")
HTML_TAG = re.compile(r"<html\b([^>]*)>", re.I)


def fix_css(css: str) -> str:
    if "v" not in css:
        return css
    out, pos = [], 0
    # Skip at-rule preludes; rewrite everything else.
    for m in AT_RULE.finditer(css):
        out.append(_rewrite(css[pos:m.start()]))
        out.append(m.group(0))
        pos = m.end()
    out.append(_rewrite(css[pos:]))
    return "".join(out)


def _rewrite(chunk: str) -> str:
    def repl(m: re.Match) -> str:
        num, unit = m.group(1), m.group(2)
        if float(num) == 0:
            return m.group(0)
        # Already wrapped by an earlier run.
        tail = chunk[m.end():m.end() + 24]
        if tail.lstrip().startswith("/ " + MARK) or tail.lstrip().startswith("/" + MARK):
            return m.group(0)
        return f"calc({num}{unit} / var(--zoom-fix, 1))"
    return UNIT.sub(repl, chunk)


def positions_by_coordinates(text: str) -> bool:
    return any("getBoundingClientRect" in js and PLACES.search(js) for js in SCRIPT_BLOCK.findall(text))


def fix_html(text: str) -> str:
    if positions_by_coordinates(text):
        text = HTML_TAG.sub(lambda m: m.group(0) if "data-zoom" in m.group(1) else f'<html{m.group(1)} data-zoom="off">', text, count=1)
    text = STYLE_BLOCK.sub(lambda m: m.group(1) + fix_css(m.group(2)) + m.group(3), text)
    return STYLE_ATTR.sub(lambda m: m.group(1) + m.group(2) + fix_css(m.group(3)) + m.group(2), text)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+", type=Path)
    ap.add_argument("--check", action="store_true", help="report files that would change")
    args = ap.parse_args()
    files: list[Path] = []
    for p in args.paths:
        files += [p] if p.is_file() else [f for f in p.rglob("*") if f.suffix in {".html", ".css"}]
    changed = 0
    for f in files:
        try:
            src = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        new = fix_css(src) if f.suffix == ".css" else fix_html(src)
        if new != src:
            changed += 1
            if not args.check:
                f.write_text(new, encoding="utf-8")
    print(f"scale_large_screens: {changed} of {len(files)} files {'need' if args.check else 'got'} viewport-unit fixes")
    return 0


if __name__ == "__main__":
    sys.exit(main())

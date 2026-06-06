#!/usr/bin/env python3
"""
Fix two issues across all generated HTML pages in docs/Academics/courses/:
1. body { height: 100vh; overflow: hidden } clips the sidebar — replace with
   min-height: 100vh; overflow-y: auto; so the layout never clips.
2. "Open in new tab" links in .rendered-content are plain bullet-point list items;
   style them to match the terminal aesthetic.
"""

from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSES_DIR = ROOT / "docs" / "Academics" / "courses"

# CSS to inject just before </style> in content-viewer pages
OPEN_IN_NEW_TAB_CSS = """
        /* ── open-in-new-tab link styling ── */
        .rendered-content ul li:only-child > a,
        .rendered-content > ul:first-of-type li a {
            display: inline-block;
            font-family: var(--font-mono);
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--brand-purple);
            text-decoration: none;
            border: 1px solid rgba(184, 41, 234, 0.5);
            padding: 6px 14px;
            margin: 6px 0;
            transition: background 160ms, box-shadow 160ms;
        }
        .rendered-content ul li:only-child > a::before,
        .rendered-content > ul:first-of-type li a::before {
            content: "[ ";
        }
        .rendered-content ul li:only-child > a::after,
        .rendered-content > ul:first-of-type li a::after {
            content: " -> ]";
        }
        .rendered-content ul li:only-child > a:hover,
        .rendered-content > ul:first-of-type li a:hover {
            background: rgba(184, 41, 234, 0.1);
            box-shadow: 0 0 12px rgba(184, 41, 234, 0.25);
        }
        .rendered-content ul li:only-child,
        .rendered-content > ul:first-of-type li {
            list-style: none;
            margin-left: 0;
            padding-left: 0;
        }
        .rendered-content ul li:only-child::marker,
        .rendered-content > ul:first-of-type li::marker {
            display: none;
        }
"""

# Pattern: body block containing height:100vh + overflow:hidden
# We replace those two lines to avoid clipping the sidebar layout
BODY_FIX_OLD = "        height: 100vh;\n        overflow: hidden;"
BODY_FIX_NEW = "        min-height: 100vh;\n        overflow-y: auto;"

# Also the 3-line variant (in case there's a display:flex check needed)
BODY_FIX_OLD2 = "    height: 100vh;\n    overflow: hidden;"
BODY_FIX_NEW2 = "    min-height: 100vh;\n    overflow-y: auto;"


def fix_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    # Fix 1: body overflow clipping
    text = text.replace(BODY_FIX_OLD, BODY_FIX_NEW)
    text = text.replace(BODY_FIX_OLD2, BODY_FIX_NEW2)

    # Fix 2: inject "open in new tab" CSS only in pages that have .rendered-content
    if "rendered-content" in text and "open-in-new-tab link styling" not in text:
        # Inject before the closing </style> tag (the first one after <head>)
        text = text.replace("    </style>\n</head>", OPEN_IN_NEW_TAB_CSS + "    </style>\n</head>", 1)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    skipped = 0
    for html_file in sorted(COURSES_DIR.rglob("*.html")):
        if fix_file(html_file):
            changed += 1
        else:
            skipped += 1

    print(f"Fixed {changed} files, {skipped} already correct.")


if __name__ == "__main__":
    main()

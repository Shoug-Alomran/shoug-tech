#!/usr/bin/env python3
"""Give every academic directory listing the same folder-row treatment.

Two conventions had drifted apart across the courses: some listings put the
folder icon before the label and some after it, and the icon was sized 18px,
20px or 24px depending on the page. This normalises both — icon first at 20px,
the label always wrapped in .dir-title-text — so a folder row looks identical
wherever it appears.

Run scripts/sort_academic_folder_rows.py afterwards to keep folders above files.

Usage:
    python3 scripts/normalize_folder_rows.py           # rewrite all listings
    python3 scripts/normalize_folder_rows.py --check   # report drift, write nothing
"""

import argparse
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACADEMICS = os.path.join(REPO, 'docs', 'academics')

ICON_SIZE = '20px'

# <div class="dir-title"><span class="dir-title-text">Label</span><svg class="dir-folder-icon" ...></svg>
TRAILING_ICON_RE = re.compile(
    r'(<div class="dir-title">)\s*(<span class="dir-title-text">.*?</span>)\s*'
    r'(<svg class="dir-folder-icon".*?</svg>)', re.S)

# A bare label sitting next to the icon, with no .dir-title-text wrapper. The
# icon match must stay inside its own .dir-title, or it runs on to the next row.
BARE_LABEL_RE = re.compile(
    r'(<div class="dir-title">\s*<svg class="dir-folder-icon"(?:(?!</div>).)*?</svg>)'
    r'\s*([^<\s][^<]*?)\s*(</div>)', re.S)

ICON_RULE_RE = re.compile(r'\.dir-folder-icon\s*\{[^}]*\}')
DIMENSION_RE = re.compile(r'\b(width|height)(\s*:\s*)([\d.]+px)')


def resize(rule):
    """Retarget the icon box, leaving the page's own spacing style alone."""
    return DIMENSION_RE.sub(
        lambda m: m.group(1) + m.group(2) + ICON_SIZE if m.group(3) != ICON_SIZE else m.group(0),
        rule)


def normalize(text):
    text = TRAILING_ICON_RE.sub(r'\1\3\2', text)
    text = BARE_LABEL_RE.sub(r'\1<span class="dir-title-text">\2</span>\3', text)
    text = ICON_RULE_RE.sub(lambda m: resize(m.group(0)), text)
    return text


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true', help='report drift without writing')
    args = ap.parse_args()

    changed = []
    for dirpath, _dirnames, filenames in os.walk(ACADEMICS):
        for name in filenames:
            if not name.endswith('.html'):
                continue
            path = os.path.join(dirpath, name)
            with open(path, encoding='utf-8') as fh:
                original = fh.read()
            if 'dir-folder-icon' not in original:
                continue
            updated = normalize(original)
            if updated == original:
                continue
            changed.append(path)
            if not args.check:
                with open(path, 'w', encoding='utf-8') as fh:
                    fh.write(updated)
    verb = 'would normalise' if args.check else 'normalised'
    print('%s %d listing(s)' % (verb, len(changed)))
    for path in changed:
        print('  %s' % os.path.relpath(path, REPO))
    return 1 if (args.check and changed) else 0


if __name__ == '__main__':
    sys.exit(main())

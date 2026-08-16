#!/usr/bin/env python3
"""Put real slide counts into the syllabus index of every course hub page.

ETHCS303, SE322, SE423, CS331 and CYS401 show the page count of each deck next
to its syllabus topic, plus a `// N_DECKS // N_SLIDES` header and a Σ total row.
This script gives every other course the same treatment: counts come from the
PDFs in the course's slides/ folder, and the topic -> deck mapping lives in
scripts/course-slide-index.json.

Usage:
    python3 scripts/build_slide_counts.py           # rewrite the hub pages
    python3 scripts/build_slide_counts.py --check   # report drift, write nothing
"""

import argparse
import json
import os
import re
import sys

from pypdf import PdfReader

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, 'docs')
MAP_FILE = os.path.join(REPO, 'scripts', 'course-slide-index.json')

LIST_OPEN_RE = re.compile(r'<div class="topics-list"[^>]*>')
DIV_RE = re.compile(r'<div\b[^>]*>|</div>')
LABEL_RE = re.compile(r'(<div class="section-label" id="section-syllabus-index"[^>]*>)(.*?)(</div>)', re.S)
ITEM_RE = re.compile(r'<div class="topic-item[^"]*">.*?</div>(?=\s*(?:<div class="topic-item|$))', re.S)
META_RE = re.compile(r'<span\s+class="topic-meta"[^>]*>.*?</span>', re.S)
TOTAL_AR = 'مجموع الشرائح'
TOTAL_AVAILABLE_AR = 'مجموع الشرائح المتاحة'


def deck_pages(course_dir, rel):
    path = os.path.join(course_dir, 'slides', rel)
    return len(PdfReader(path, strict=False).pages)


def all_decks(course_dir):
    root = os.path.join(course_dir, 'slides')
    out = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in sorted(filenames):
            if name.lower().endswith('.pdf'):
                out.append(os.path.relpath(os.path.join(dirpath, name), root))
    return sorted(out)


def total_row(count, complete):
    name = 'Total Slides' if complete else 'Total Slides Available'
    arabic = TOTAL_AR if complete else TOTAL_AVAILABLE_AR
    return ('<div class="topic-item exam-total"><span class="topic-num">Σ</span>'
            '<span class="topic-name" data-ar-text="%s">%s</span>'
            '<span class="topic-meta">%d SLIDES</span></div>' % (arabic, name, count))


def set_meta(item, text, arabic=None):
    ar = ' data-ar-text="%s"' % arabic if arabic else ''
    span = '<span class="topic-meta"%s>%s</span>' % (ar, text)
    if META_RE.search(item):
        return META_RE.sub(lambda m: span, item, count=1)
    return item[:item.rindex('</div>')] + span + '</div>'


def rewrite(course_url, spec, check_only):
    course_dir = os.path.join(DOCS, course_url.strip('/'))
    page = os.path.join(course_dir, 'index.html')
    html = open(page, encoding='utf-8').read()

    open_tag = LIST_OPEN_RE.search(html)
    if not open_tag:
        raise SystemExit('no syllabus topics-list found in ' + page)
    depth, inner_start, inner_end = 1, open_tag.end(), None
    for m in DIV_RE.finditer(html, inner_start):
        depth += -1 if m.group(0) == '</div>' else 1
        if depth == 0:
            inner_end = m.start()
            break
    if inner_end is None:
        raise SystemExit('unbalanced topics-list in ' + page)
    items = ITEM_RE.findall(html[inner_start:inner_end])
    keep = set(spec.get('keep', []))
    labels = spec.get('labels', {})
    ignored = set(spec.get('ignore_decks', []))

    decks = [d for d in all_decks(course_dir) if d not in ignored]
    pages = {d: deck_pages(course_dir, d) for d in decks}
    assigned = set()

    out, changed_rows = [], 0
    for index, item in enumerate(items, start=1):
        if 'exam-total' in item.split('>')[0]:
            continue                      # rebuilt below
        if index in keep:
            out.append(item)
            continue
        if str(index) in labels:
            text, arabic = labels[str(index)]
            new = set_meta(item, text, arabic)
        else:
            rels = spec['rows'].get(str(index))
            if rels is None:
                out.append(item)
                continue
            missing = [r for r in rels if r not in pages]
            if missing:
                raise SystemExit('%s row %d: deck not found: %s' % (course_url, index, missing))
            assigned.update(rels)
            count = sum(pages[r] for r in rels)
            new = set_meta(item, '%d SLIDES' % count if rels else 'NO DECK YET')
        if new != item:
            changed_rows += 1
        out.append(new)

    total = sum(pages.values())
    complete = assigned == set(decks)
    out.append(total_row(total, complete))
    new_block = '\n                                '.join(out)
    html = html[:inner_start] + '\n                                ' + new_block + '\n                            ' + html[inner_end:]

    label = LABEL_RE.search(html)
    if label:
        base = re.sub(r'\s*//.*', '', label.group(2), flags=re.S).strip()
        header = '%s // %d_DECKS // %d_SLIDES' % (base, len(decks), total)
        html = html[:label.start(2)] + header + html[label.end(2):]

    original = open(page, encoding='utf-8').read()
    if html != original and not check_only:
        with open(page, 'w', encoding='utf-8') as fh:
            fh.write(html)
    return html != original, len(decks), total, complete


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true', help='report drift without writing')
    ap.add_argument('--only', help='limit to one course url')
    args = ap.parse_args()

    mapping = json.load(open(MAP_FILE, encoding='utf-8'))
    touched = 0
    for course_url, spec in mapping.items():
        if course_url.startswith('_') or (args.only and args.only != course_url):
            continue
        changed, decks, total, complete = rewrite(course_url, spec, args.check)
        touched += bool(changed)
        print('%-46s %2d decks %5d slides %s%s'
              % (course_url.replace('/academics/', ''), decks, total,
                 'all decks mapped' if complete else 'some decks unmapped',
                 '  (updated)' if changed else ''))
    print('%s %d page(s)' % ('would update' if args.check else 'updated', touched))
    return 1 if (args.check and touched) else 0


if __name__ == '__main__':
    sys.exit(main())

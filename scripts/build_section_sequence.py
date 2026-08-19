#!/usr/bin/env python3
"""Keep every section listing, its item numbers, and its prev/next chain in step.

Each course section page (slides/, slide-breakdowns/, exams/, ...) lists its
items as numbered `.dir-row` links. That listing is the course's real order, so
it is the source of truth here: this script renumbers the listing 01..N and
rewrites each item page's `ITEM_NN` label and PREVIOUS/NEXT links to match.

Usage:
    python3 scripts/build_section_sequence.py           # rewrite the pages
    python3 scripts/build_section_sequence.py --check   # report drift only
"""

import argparse
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, 'docs')
ACADEMICS = os.path.join(DOCS, 'academics')

DIR_ROW_RE = re.compile(r'<a href="([^"]+)"[^>]*class="dir-row"[^>]*>.*?</a>', re.S)
DIR_NUM_RE = re.compile(r'(<div class="dir-num">)(\d+)(</div>)')
ITEM_RE = re.compile(r'(class="ch-label">ITEM_)(\d+)')
PREV_RE = re.compile(r'<(?:a href="[^"]*"|span) class="nav-link prev(?: disabled)?">(.*?)</(?:a|span)>', re.S)
NEXT_RE = re.compile(r'<(?:a href="[^"]*"|span) class="nav-link next(?: disabled)?">(.*?)</(?:a|span)>', re.S)


def read(path):
    with open(path, encoding='utf-8', errors='replace') as fh:
        return fh.read()


def write(path, text):
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(text)


def section_pages():
    """(section index path, ordered item urls) for every numbered listing."""
    for dirpath, _dirnames, filenames in os.walk(ACADEMICS):
        if 'index.html' not in filenames:
            continue
        path = os.path.join(dirpath, 'index.html')
        html = read(path)
        rows = DIR_ROW_RE.findall(html[html.rfind('</nav>'):])
        if len(rows) > 1:
            yield path, rows


def link(url, direction, label):
    return '<a href="%s" class="nav-link %s">%s</a>' % (url, direction, label)


def disabled(direction, label):
    return '<span class="nav-link %s disabled">%s</span>' % (direction, label)


def fix_item_page(path, position, prev_url, next_url, check_only):
    html = original = read(path)
    html = ITEM_RE.sub(lambda m: m.group(1) + '%02d' % position, html, count=1)

    def swap(pattern, direction, url):
        def repl(m):
            label = m.group(1)
            return link(url, direction, label) if url else disabled(direction, label)
        return pattern.sub(repl, html, count=1)

    html = swap(PREV_RE, 'prev', prev_url)
    html = swap(NEXT_RE, 'next', next_url)
    if html != original and not check_only:
        write(path, html)
    return html != original


def renumber_listing(path, check_only):
    html = original = read(path)
    split = html.rfind('</nav>')
    head, tail = html[:split], html[split:]
    counter = [0]

    def repl(m):
        counter[0] += 1
        return DIR_NUM_RE.sub(lambda n: n.group(1) + '%02d' % counter[0] + n.group(3), m.group(0), count=1)

    tail = DIR_ROW_RE.sub(repl, tail)
    html = head + tail
    if html != original and not check_only:
        write(path, html)
    return html != original


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true', help='report drift without writing')
    args = ap.parse_args()

    sections = items = renumbered = missing = 0
    for index_path, order in section_pages():
        sections += 1
        renumbered += bool(renumber_listing(index_path, args.check))
        for i, url in enumerate(order):
            item_path = os.path.join(DOCS, url.strip('/'), 'index.html')
            if not os.path.exists(item_path):
                missing += 1
                continue
            items += fix_item_page(item_path,
                                   i + 1,
                                   order[i - 1] if i else None,
                                   order[i + 1] if i + 1 < len(order) else None,
                                   args.check)
    verb = 'would fix' if args.check else 'fixed'
    print('%d section listing(s) scanned; %s %d listing number block(s) and %d item page(s)'
          % (sections, verb, renumbered, items))
    if missing:
        print('%d listed item(s) have no page' % missing)
    return 1 if (args.check and (renumbered or items)) else 0


if __name__ == '__main__':
    sys.exit(main())

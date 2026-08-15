#!/usr/bin/env python3
"""Render the academic sidebar from a single source of truth.

The SYSTEM_DIRECTORY sidebar used to be copy-pasted into every academic page, so
the copies drifted apart (missing courses, stale labels, broken markup). This
script keeps one definition in scripts/academic-sidebar.json and stamps it into
every academic page, with the active course/section/item marked per page.

Usage:
    python3 scripts/build_academic_sidebar.py            # rewrite all pages
    python3 scripts/build_academic_sidebar.py --check    # report drift, write nothing
    python3 scripts/build_academic_sidebar.py --harvest  # rebuild the JSON from the pages
"""

import argparse
import collections
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, 'docs')
ACADEMICS = os.path.join(DOCS, 'academics')
DATA_FILE = os.path.join(REPO, 'scripts', 'academic-sidebar.json')

NAV_RE = re.compile(r'<nav class="[^"]*academic-sidebar[^"]*"[^>]*>.*?</nav>', re.S)
LI_RE = re.compile(r'<li class="tree-item[^"]*">\s*<a class="tree-file"([^>]*)>(.*?)</a>\s*</li>', re.S)
HREF_RE = re.compile(r'href="([^"]+)"')
UL_TAG_RE = re.compile(r'<ul\b[^>]*>|</ul>')
DOT = '<span class="status-dot"></span>'

# Pages outside docs/academics/ that also use the academic tree.
EXTRA_PAGES = ['academic-plan-themes/academic-plan/index.html']


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #

def ul_blocks(html, cls):
    """Yield (start, end, inner) for every <ul> whose open tag contains cls."""
    stack = []
    for m in UL_TAG_RE.finditer(html):
        if m.group(0).startswith('</'):
            if stack:
                start, tag = stack.pop()
                if cls in tag:
                    yield start, m.end(), html[html.index('>', start) + 1:m.start()]
        else:
            stack.append((m.start(), m.group(0)))


def page_urls():
    """Every page that carries the academic sidebar, as (path, url)."""
    out = []
    for dirpath, dirnames, filenames in os.walk(ACADEMICS):
        if 'index.html' not in filenames:
            continue
        path = os.path.join(dirpath, 'index.html')
        url = '/' + os.path.relpath(dirpath, DOCS).replace(os.sep, '/') + '/'
        out.append((path, url))
    for rel in EXTRA_PAGES:
        path = os.path.join(DOCS, rel)
        if os.path.exists(path):
            out.append((path, '/' + os.path.dirname(rel) + '/'))
    return sorted(out)


def load_data():
    with open(DATA_FILE, encoding='utf-8') as fh:
        return json.load(fh)


# --------------------------------------------------------------------------- #
# harvest: rebuild the JSON from whatever the pages currently say
# --------------------------------------------------------------------------- #

def harvest():
    """Majority-vote the per-course section lists and nested item lists."""
    shapes = collections.defaultdict(collections.Counter)   # parent -> Counter[url tuple]
    meta = collections.defaultdict(collections.Counter)     # (parent, url) -> Counter[(attrs, label)]

    def record(parent, entries):
        seen, uniq = set(), []
        for url, attrs, label in entries:
            if url in seen:
                continue
            seen.add(url)
            uniq.append((url, attrs, label))
        shapes[parent][tuple(e[0] for e in uniq)] += 1
        for url, attrs, label in uniq:
            meta[(parent, url)][(attrs, label)] += 1

    def parse_level(inner):
        """Entries at this level, plus (parent url, inner html) for nested lists.

        A nested <ul class="item-children"> always follows the <li> it belongs
        to, so the preceding link is its parent.
        """
        nested = [(s, e, body) for s, e, body in ul_blocks(inner, 'item-children')]
        top = []
        for s, e, body in nested:
            if not any(s2 < s and e <= e2 for s2, e2, _b in nested if (s2, e2) != (s, e)):
                top.append((s, e, body))
        entries, children, cursor, last = [], [], 0, None
        for s, e, body in sorted(top):
            for m in LI_RE.finditer(inner, cursor, s):
                attrs, label = m.group(1), m.group(2)
                url = HREF_RE.search(attrs).group(1)
                entries.append((url, HREF_RE.sub('', re.sub(r'\s+', ' ', attrs)).strip(),
                                label.replace(DOT, '').strip()))
                last = url
            children.append((last, body))
            cursor = e
        for m in LI_RE.finditer(inner, cursor):
            attrs, label = m.group(1), m.group(2)
            url = HREF_RE.search(attrs).group(1)
            entries.append((url, HREF_RE.sub('', re.sub(r'\s+', ' ', attrs)).strip(),
                            label.replace(DOT, '').strip()))
        return entries, children

    def walk_level(parent, inner):
        entries, children = parse_level(inner)
        if entries:
            record(parent, entries)
        for child_parent, body in children:
            if child_parent:
                walk_level(child_parent, body)

    for path, _url in page_urls():
        with open(path, encoding='utf-8', errors='replace') as fh:
            nav = NAV_RE.search(fh.read())
        if not nav:
            continue
        nav = nav.group(0)
        for _s, _e, inner in ul_blocks(nav, 'section-children'):
            entries, _children = parse_level(inner)
            if entries:
                walk_level(entries[0][0], inner)    # OVERVIEW points at the course root

    resolved = {}
    for parent, counter in shapes.items():
        shape = max(counter.items(), key=lambda kv: (kv[1], len(kv[0])))[0]
        resolved[parent] = [
            dict(zip(('url', 'attrs', 'label'), (url,) + meta[(parent, url)].most_common(1)[0][0]))
            for url in shape
        ]

    data = load_data()
    courses = {c['url'] for c in walk_courses(data['tree'])}
    data['sections'] = {k: v for k, v in sorted(resolved.items()) if k in courses}
    data['children'] = {k: v for k, v in sorted(resolved.items()) if k not in courses}
    with open(DATA_FILE, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write('\n')
    print('harvested %d course section lists, %d nested lists'
          % (len(data['sections']), len(data['children'])))


# --------------------------------------------------------------------------- #
# render
# --------------------------------------------------------------------------- #

def walk_courses(nodes):
    for node in nodes:
        if node.get('type') == 'group':
            for child in walk_courses(node['children']):
                yield child
        elif node.get('type') == 'course':
            yield node


def group_path(nodes, course_url, trail=()):
    """Toggle ids of every group that contains course_url."""
    for node in nodes:
        if node.get('type') != 'group':
            continue
        here = trail + (node['id'],)
        found = group_path(node['children'], course_url, here)
        if found:
            return found
        if any(c['url'] == course_url for c in node['children'] if c.get('type') == 'course'):
            return here
    return ()


def link(url, label, attrs='', active=False, classes='tree-item'):
    cls = classes + ' file-active' if active else classes
    extra = ' ' + attrs if attrs else ''
    body = (DOT if active else '') + label
    return '<li class="%s"><a class="tree-file" href="%s"%s>%s</a></li>' % (cls, url, extra, body)


def render_children(data, parent, url):
    """Nested item lists along the active path (slides, chapters, labs, ...)."""
    entries = data['children'].get(parent)
    if not entries:
        return ''
    out = ['<ul class="tree-children item-children is-open">']
    descend = None
    for e in entries:
        active = url.startswith(e['url'])
        if active and (descend is None or len(e['url']) > len(descend['url'])):
            descend = e
    for e in entries:
        out.append(link(e['url'], e['label'], e['attrs'],
                        active=(descend is not None and e['url'] == descend['url']),
                        classes='tree-item tree-viewer'))
        if descend is not None and e['url'] == descend['url']:
            out.append(render_children(data, e['url'], url))
    out.append('</ul>')
    return ''.join(out)


def render_sections(data, course_url, url):
    entries = data['sections'].get(course_url)
    if not entries:
        return ''
    # The active section is the longest section url that prefixes this page.
    active = None
    for e in entries:
        if url.startswith(e['url']) and (active is None or len(e['url']) > len(active)):
            active = e['url']
    if url == course_url:
        active = course_url
    out = ['<ul class="tree-children section-children">']
    for e in entries:
        is_active = e['url'] == active
        out.append(link(e['url'], e['label'], e['attrs'], is_active, 'tree-item tree-section'))
        if is_active and e['url'] != course_url:
            out.append(render_children(data, e['url'], url))
    out.append('</ul>')
    return ''.join(out)


def render_nodes(data, nodes, url, course_url, open_groups):
    out = []
    for node in nodes:
        kind = node.get('type')
        if kind == 'link':
            out.append(link(node['url'], node['label'], node.get('attrs', ''),
                            active=(url == node['url'])))
        elif kind == 'root':
            out.append('<li class="tree-item root-dir"><a class="tree-course-link" href="%s">%s</a></li>'
                       % (node['url'], node['label']))
        elif kind == 'course':
            active = node['url'] == course_url
            out.append(link(node['url'], node['label'], node.get('attrs', ''), active))
            if active:
                out.append(render_sections(data, node['url'], url))
        elif kind == 'group':
            is_open = node['id'] in open_groups
            li_cls = 'tree-item dir-open' if is_open else 'tree-item'
            if node.get('class'):
                li_cls += ' ' + node['class']
            out.append(
                '<li class="%s"><button class="tree-course-link tree-toggle-button" type="button" '
                'data-tree-toggle="%s" aria-expanded="%s"><span class="tree-toggle">%s</span> %s</button></li>'
                % (li_cls, node['id'], 'true' if is_open else 'false',
                   '[-]' if is_open else '[+]', node['label']))
            out.append('<ul id="%s" class="tree-children%s">%s</ul>'
                       % (node['id'], ' is-open' if is_open else '',
                          render_nodes(data, node['children'], url, course_url, open_groups)))
    return ''.join(out)


def render_nav(data, url):
    course_url = ''
    for course in walk_courses(data['tree']):
        if url.startswith(course['url']) and len(course['url']) > len(course_url):
            course_url = course['url']
    open_groups = set(group_path(data['tree'], course_url)) if course_url else set()
    if not course_url and url != '/academics/':
        # A hub page (/academics/cybersecurity/) opens the group it belongs to.
        def open_hub(nodes):
            for node in nodes:
                if node.get('type') != 'group':
                    continue
                if any(c['url'].startswith(url) for c in walk_courses(node['children'])):
                    open_groups.add(node['id'])
                    open_hub(node['children'])
        open_hub(data['tree'])
    return (
        '<nav class="sidebar academic-sidebar" aria-label="Academic directory">'
        '<div class="sidebar-header"><span class="sidebar-title">SYSTEM_DIRECTORY</span>'
        '<button class="sidebar-collapse-button" type="button" data-sidebar-collapse '
        'aria-expanded="true"><span class="collapse-icon">&lt;</span></button></div>'
        '<div class="file-tree"><ul class="tree-node">'
        + render_nodes(data, data['tree'], url, course_url, open_groups) +
        '</ul></div></nav>'
    )


def build(check_only=False):
    data = load_data()
    changed, skipped = [], []
    for path, url in page_urls():
        with open(path, encoding='utf-8') as fh:
            html = fh.read()
        match = NAV_RE.search(html)
        if not match:
            skipped.append(path)
            continue
        nav = render_nav(data, url)
        if match.group(0) == nav:
            continue
        changed.append(path)
        if not check_only:
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write(html[:match.start()] + nav + html[match.end():])
    verb = 'would update' if check_only else 'updated'
    print('%s %d page(s); %d page(s) have no sidebar' % (verb, len(changed), len(skipped)))
    return 1 if (check_only and changed) else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true', help='report drift without writing')
    ap.add_argument('--harvest', action='store_true', help='rebuild the JSON from the pages')
    args = ap.parse_args()
    if args.harvest:
        harvest()
        return 0
    return build(check_only=args.check)


if __name__ == '__main__':
    sys.exit(main())

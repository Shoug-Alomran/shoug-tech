#!/usr/bin/env python3
"""Embed course resource files automatically: drop a file in, get the pages.

Any folder shaped like

    docs/academics/<track>/<course>/extra-resources/<section>/{solved,unsolved}/...

(SE322/SE423 "activity", CYS401 "labs", CS331 "tutorials", or any new one) is
treated as a resource section. The files on disk are the source of truth for
*what* is listed; this script rebuilds everything around them:

  * the section page (Solved / Unsolved folder rows with file counts),
  * a listing page for solved/, unsolved/ and every nested folder,
  * a PDF viewer page for every PDF (docx/png/... link straight to the file),
  * the section's row on the course's Study Material page,
  * the SYSTEM_DIRECTORY entries in scripts/academic-sidebar.json,
  * then scripts/build_academic_sidebar.py to stamp the sidebars.

Titles can't be derived from filenames ("Activity 4: UML II — Activity &
Sequence Diagrams"), so they live in scripts/resource-titles.json, keyed by the
file's path under docs/academics/. Before each run the titles already shown on
the pages are harvested into that file, so hand-edited titles are never lost.
A new file without a title borrows its solved/unsolved counterpart's title
(activity-5.pdf <- activity-5.docx), else a readable name from the filename;
either way it is written to the JSON so you can rename it there.

Usage:
    python3 scripts/embed_resources.py                  # rebuild everything
    python3 scripts/embed_resources.py --check          # exit 1 if pages are stale
    python3 scripts/embed_resources.py --from-index     # only files staged/tracked in git
    python3 scripts/embed_resources.py --changed-list F # write touched paths to F

The pre-commit hook in .githooks/ runs this automatically; enable it once with
    git config core.hooksPath .githooks
"""

import argparse
import glob
import html
import json
import os
import re
import shutil
import subprocess
import sys
from urllib.parse import quote, unquote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_activity_and_project_pages as tpl  # noqa: E402  (shared ENG103 templates)

REPO = tpl.REPO
DOCS = tpl.DOCS
ACADEMICS = os.path.join(DOCS, 'academics')
TITLES_FILE = os.path.join(REPO, 'scripts', 'resource-titles.json')
SIDEBAR_FILE = os.path.join(REPO, 'scripts', 'academic-sidebar.json')
SIDEBAR_BUILDER = os.path.join(REPO, 'scripts', 'build_academic_sidebar.py')

STATES = ('solved', 'unsolved')
IGNORED = {'.DS_Store', 'index.html', 'Thumbs.db'}
IMAGE_TAG = {'png': 'png', 'jpg': 'png', 'jpeg': 'png', 'gif': 'png', 'webp': 'png', 'svg': 'png'}

NAV_RE = re.compile(r'<nav class="[^"]*academic-sidebar[^"]*"[^>]*>.*?</nav>', re.S)
ROW_RE = re.compile(
    r'<a\b([^>]*)>\s*<div class="dir-num">.*?</div>\s*<div class="dir-title">(.*?)</div>\s*'
    r'<div class="dir-status">', re.S)
PDF_SRC_RE = re.compile(r'data-pdf-src="([^"]+)"')


# --------------------------------------------------------------------------- #
# small helpers
# --------------------------------------------------------------------------- #

def rel(path):
    """Path under docs/academics/, the key used in resource-titles.json."""
    return os.path.relpath(path, ACADEMICS).replace(os.sep, '/')


def url_of(path):
    """Site URL of a directory (trailing slash) or file under docs/."""
    r = '/' + os.path.relpath(path, DOCS).replace(os.sep, '/')
    return r + '/' if os.path.isdir(path) or not os.path.splitext(path)[1] else r


def read(path):
    with open(path, encoding='utf-8') as fh:
        return fh.read()


def natural_key(name):
    return [int(p) if p.isdigit() else p.lower() for p in re.split(r'(\d+)', name)]


def strip_tags(text):
    return html.unescape(re.sub(r'<[^>]+>', '', text)).strip()


def humanize(stem):
    words = re.sub(r'[-_\s]+', ' ', stem).strip().split(' ')
    return ' '.join(w if w.isupper() else w[:1].upper() + w[1:] for w in words if w)


def plural(n, word):
    return '%d %s%s' % (n, word, '' if n == 1 else 'S')


def squash(markup):
    """Markup with formatter noise removed (`<a href="x" >`, `</a >`, wrapped text)."""
    markup = re.sub(r'\s+', ' ', markup)
    markup = re.sub(r'\s*>\s*', '>', markup)
    return re.sub(r'\s*<\s*', '<', markup).strip()


def same_sidebar(old_bytes, new_bytes):
    """True when two page versions differ only in sidebar whitespace."""
    old, new = old_bytes.decode('utf-8'), new_bytes.decode('utf-8')
    a, b = NAV_RE.search(old), NAV_RE.search(new)
    if not (a and b) or NAV_RE.sub('', old) != NAV_RE.sub('', new):
        return False
    return squash(a.group(0)) == squash(b.group(0))


def is_viewer_dir(path):
    """A generated PDF viewer: a folder holding nothing but its index.html."""
    if not os.path.isdir(path):
        return False
    names = [n for n in os.listdir(path) if n not in ('.DS_Store',)]
    return names == ['index.html'] and 'data-pdf-src=' in read(os.path.join(path, 'index.html'))


def owned_pdf(path):
    """The PDF a folder's own viewer shows when that PDF sits beside it, else None.

    Such a folder is one file, not a folder: its parent lists it as a PDF row."""
    index = os.path.join(path, 'index.html')
    if not os.path.isdir(path):
        return None
    match = PDF_SRC_RE.search(read(index)) if os.path.isfile(index) else None
    pdf = os.path.normpath(os.path.join(path, unquote(match.group(1)))) if match else None
    if pdf and os.path.dirname(pdf) == os.path.normpath(path) and os.path.isfile(pdf):
        return pdf
    return lone_pdf(path)


def is_own_viewer(path):
    index = os.path.join(path, 'index.html')
    match = os.path.isfile(index) and PDF_SRC_RE.search(read(index))
    return bool(match) and os.path.normpath(os.path.join(path, unquote(match.group(1)))) == lone_pdf(path)


def lone_pdf(path):
    """<name>/<name>.pdf with nothing else beside it but its (listing) page and generated viewers."""
    names = [n for n in os.listdir(path) if n not in IGNORED and not n.startswith('.')
             and not is_viewer_dir(os.path.join(path, n))]
    pdf = os.path.join(path, os.path.basename(path) + '.pdf')
    return pdf if names == [os.path.basename(pdf)] and os.path.isfile(pdf) else None


# --------------------------------------------------------------------------- #
# discovery
# --------------------------------------------------------------------------- #

def indexed_files():
    """Files in the git index (tracked + staged), minus staged deletions."""
    out = subprocess.run(['git', 'ls-files', '-z', '--', 'docs/academics'], cwd=REPO,
                         capture_output=True, check=True).stdout.decode('utf-8')
    return {os.path.join(REPO, p) for p in out.split('\0') if p}


def find_sections():
    sections = []
    for sec in sorted(glob.glob(os.path.join(ACADEMICS, '*', '*', 'extra-resources', '*', ''))):
        sec = sec.rstrip(os.sep)
        if any(os.path.isdir(os.path.join(sec, s)) for s in STATES):
            sections.append(sec)
    return sections


def content_files(folder, allowed):
    """(files, subfolders) that are real content, skipping generated viewers."""
    files, dirs = [], []
    for name in sorted(os.listdir(folder), key=natural_key):
        path = os.path.join(folder, name)
        if name in IGNORED or name.startswith('.'):
            continue
        if os.path.isdir(path):
            pdf = owned_pdf(path)
            if pdf:
                if allowed is None or pdf in allowed:
                    files.append(path)
            elif not is_viewer_dir(path) and has_content(path, allowed):
                dirs.append(path)
        elif allowed is None or path in allowed:
            files.append(path)
    return files, dirs


def has_content(folder, allowed):
    files, dirs = content_files(folder, allowed)
    return bool(files or dirs)


# --------------------------------------------------------------------------- #
# titles
# --------------------------------------------------------------------------- #

def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)


def dump_json(path, data):
    text = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    if os.path.exists(path) and read(path) == text:
        return False
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(text)
    return True


def harvest(sections, titles):
    """Copy titles already shown on the pages into the manifest (missing keys only)."""
    found = {}
    for sec in sections:
        for page in glob.glob(os.path.join(sec, '**', 'index.html'), recursive=True):
            here = os.path.dirname(page)
            text = read(page)
            if 'data-pdf-src=' in text:          # viewer: its h1 titles its PDF
                src = PDF_SRC_RE.search(text).group(1)
                h1 = re.search(r'<h1 class="ch-title">(.*?)</h1>', text, re.S)
                if h1:
                    target = os.path.normpath(os.path.join(here, unquote(src)))
                    found.setdefault(rel(target), strip_tags(h1.group(1)))
                continue
            for attrs, title in ROW_RE.findall(text):
                href = re.search(r'href="([^"]+)"', attrs)
                if not href or href.group(1).startswith(('http', '#', 'mailto')):
                    continue
                h = unquote(href.group(1))
                target = os.path.normpath(os.path.join(DOCS, h.lstrip('/')) if h.startswith('/')
                                          else os.path.join(here, h))
                if os.path.basename(target) in STATES:
                    continue
                if is_viewer_dir(target):
                    src = PDF_SRC_RE.search(read(os.path.join(target, 'index.html'))).group(1)
                    target = os.path.normpath(os.path.join(target, unquote(src)))
                found[rel(target)] = strip_tags(title)   # a row title beats a viewer h1
    added = 0
    for key, title in found.items():
        if key not in titles and title:
            titles[key] = title
            added += 1
    return added


def title_for(path, section, titles, notes):
    key = rel(path)
    if key in titles:
        return titles[key]
    stem, _ext = os.path.splitext(os.path.basename(path))
    # borrow the counterpart's title: solved/activity-5.pdf <- unsolved/activity-5.docx
    parts = key.split('/')
    for i, part in enumerate(parts):
        if part in STATES:
            other = parts[:i] + [STATES[1 - STATES.index(part)]] + parts[i + 1:]
            prefix = '/'.join(other[:-1]) + '/' + stem
            for k, v in sorted(titles.items()):
                if os.path.splitext(k)[0] == prefix:
                    titles[key] = v
                    notes.append('titled %s as "%s" (from %s)' % (key, v, k))
                    return v
    guess = humanize(re.sub(r'^[a-z]{2,4}-?\d{3}-', '', stem, flags=re.I))
    titles[key] = guess
    notes.append('titled %s as "%s" — rename it in scripts/resource-titles.json' % (key, guess))
    return guess


# --------------------------------------------------------------------------- #
# rendering (ENG103 templates via build_activity_and_project_pages)
# --------------------------------------------------------------------------- #

def course_context(section):
    """Tabs + breadcrumb head copied from the course's own Study Material page."""
    course_dir = os.path.dirname(os.path.dirname(section))
    code = os.path.basename(course_dir).upper()
    study = os.path.join(course_dir, 'extra-resources', 'index.html')
    text = read(study)
    tabs = re.search(r'<nav class="content-tabs">.*?</nav>', text, re.S).group(0)
    crumb = re.search(r'<div class="breadcrumb">(.*?)</div>', text, re.S).group(1)
    # course pages wrap these links over several lines and vary attribute order
    trail = []
    for attrs, label in re.findall(r'<a\b([^>]*)>(.*?)</a\s*>', crumb, re.S):
        link = re.search(r'href="([^"]+)"', attrs)
        if link:
            trail.append((strip_tags(label), link.group(1)))
    trail.append(('Study Material', url_of(os.path.join(course_dir, 'extra-resources'))))
    return {'code': code, 'course': code.lower(), 'tabs': tabs, 'trail': trail, 'study': study}


def listing_html(url, ctx, type_label, trail, body, meta_title):
    page = tpl.add_extra_css(tpl.read(tpl.LIST_TEMPLATE))
    page = tpl.head(page, meta_title, url, tpl.TPL_TITLE, tpl.TPL_URL)
    page = re.sub(r'<div class="breadcrumb">.*?</div>', lambda _m: tpl.breadcrumb(trail),
                  page, count=1, flags=re.S)
    page = page.replace('<h1 class="course-code">ENG103</h1>',
                        '<h1 class="course-code">%s</h1>' % ctx['code'], 1)
    page = re.sub(r'<div class="type-label">.*?</div>',
                  lambda _m: '<div class="type-label">%s</div>' % type_label, page, count=1, flags=re.S)
    page = re.sub(r'<nav class="content-tabs">.*?</nav>', lambda _m: ctx['tabs'], page, count=1, flags=re.S)
    return re.sub(r'<div class="directory-container">.*?\n            </div>\n        </main>',
                  lambda _m: body + '\n        </main>', page, count=1, flags=re.S)


def viewer_html(url, ctx, item_label, title, trail, pdf_src, back_url):
    page = tpl.read(tpl.VIEW_TEMPLATE)
    page = tpl.head(page, '%s // %s' % (ctx['code'], title), url, tpl.TPL_VIEW_TITLE, tpl.TPL_VIEW_URL)
    page = re.sub(r'<div class="breadcrumb">.*?</div>', lambda _m: tpl.breadcrumb(trail),
                  page, count=1, flags=re.S)
    page = page.replace('<div class="ch-label">ITEM_07 // STUDY MATERIAL</div>',
                        '<div class="ch-label">%s</div>' % item_label, 1)
    page = re.sub(r'<h1 class="ch-title">.*?</h1>',
                  lambda _m: '<h1 class="ch-title">%s</h1>' % html.escape(title, quote=False),
                  page, count=1, flags=re.S)
    page = re.sub(r'<a class="btn btn-secondary" href="[^"]*"',
                  lambda _m: '<a class="btn btn-secondary" href="%s"' % back_url, page, count=1)
    page = re.sub(r'<div class="nav-strip">.*?</div>',
                  lambda _m: '<div class="nav-strip">\n                '
                             '<a href="%s" class="nav-link prev">&lt;- BACK TO INDEX</a>\n'
                             '                <span class="nav-link next disabled">NEXT -&gt;</span>\n'
                             '            </div>' % back_url, page, count=1, flags=re.S)
    page = tpl.TPL_VIEW_PDF.sub(pdf_src, page)
    page = page.replace('ENG103 Group Work Log and Deadlines',
                        html.escape('%s %s' % (ctx['code'], title), quote=True))
    # the template's SEO copy (description, og/twitter, JSON-LD) names ENG103 too
    name = '%s | %s' % (ctx['code'], title)
    page = re.sub(r'<script type="application/ld\+json">.*?</script>',
                  lambda m: m.group(0).replace('ENG103 | Group Work Log and Deadlines',
                                               json.dumps(name, ensure_ascii=False)[1:-1]),
                  page, flags=re.S)
    return page.replace('ENG103 | Group Work Log and Deadlines', html.escape(name, quote=True))


def viewer_slug(pdf, taken):
    stem = os.path.splitext(os.path.basename(pdf))[0]
    parent = os.path.basename(os.path.dirname(pdf))
    slug = re.sub(r'^[a-z]{2,4}-?\d{3}-', '', stem, flags=re.I)
    if slug.lower().startswith(parent.lower() + '-') and len(slug) > len(parent) + 1:
        slug = slug[len(parent) + 1:]
    slug = re.sub(r'[^a-z0-9]+', '-', slug.lower()).strip('-') or 'document'
    if slug in taken:
        slug += '-pdf'
    return slug


# --------------------------------------------------------------------------- #
# the build
# --------------------------------------------------------------------------- #

class Build:
    def __init__(self, check, allowed):
        self.check = check
        self.allowed = allowed
        self.changed = []          # paths written or removed
        self.stale = []            # --check: paths that would change
        self.notes = []
        self.titles = load_json(TITLES_FILE, {})
        self.sidebar = load_json(SIDEBAR_FILE, None)

    # -- file output ------------------------------------------------------- #
    def put(self, path, text):
        """Write unless only the (separately stamped) sidebar would differ."""
        if os.sep + 'cybersecurity' + os.sep in path:
            from apply_cyber_red_theme import recolor   # cyber track pages stay red
            text = recolor(text)
        if os.path.exists(path):
            old = read(path)
            if NAV_RE.sub('', old) == NAV_RE.sub('', text):
                return
            nav = NAV_RE.search(old)
            if nav:                      # keep the stamped sidebar until the builder reruns
                text = NAV_RE.sub(lambda _m: nav.group(0), text, count=1)
        if self.check:
            self.stale.append(path)
            return
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(text)
        self.changed.append(path)

    def remove_dir(self, path):
        if self.check:
            self.stale.append(path)
            return
        shutil.rmtree(path)
        self.changed.append(path)

    # -- one resource section ---------------------------------------------- #
    def section(self, sec):
        ctx = course_context(sec)
        name = os.path.basename(sec)
        sec_title = self.titles.get(rel(sec), humanize(name))
        sec_url = url_of(sec)
        base_trail = ctx['trail'] + [(sec_title, sec_url)]

        rows, sidebar_rows = [], []
        for state in STATES:
            folder = os.path.join(sec, state)
            if not os.path.isdir(folder):
                continue
            files, dirs = content_files(folder, self.allowed)
            rows.append((state.title(), './%s/' % state, self.describe(files, dirs), 'available', True, False))
            sidebar_rows.append((url_of(folder), state.title()))
            self.folder(folder, ctx, sec_title, [state.title()], base_trail + [(state.title(), url_of(folder))])

        self.put(os.path.join(sec, 'index.html'),
                 listing_html(sec_url, ctx, sec_title, ctx['trail'] + [(sec_title, None)],
                              tpl.rows(rows), '%s | %s' % (ctx['code'], sec_title)))
        self.set_children(sec_url, sidebar_rows, keep_labels=True)
        self.ensure_study_row(ctx, sec, sec_title)
        self.set_children(ctx['trail'][-1][1], [(sec_url, sec_title)], keep_labels=True, merge=True)

    def describe(self, files, dirs):
        parts = []
        if files:
            parts.append(plural(len(files), 'FILE'))
        if dirs:
            parts.append(plural(len(dirs), 'FOLDER'))
        return ', '.join(parts) or 'EMPTY'

    def folder(self, folder, ctx, sec_title, labels, trail):
        """Listing page for solved/, unsolved/ or a nested folder, plus its viewers."""
        files, dirs = content_files(folder, self.allowed)
        url = url_of(folder)
        # A dedicated viewer now owns its PDF; keep it a viewer on rebuild.
        if owned_pdf(folder):
            return
        taken = {os.path.basename(p).lower() for p in dirs + files if os.path.isdir(p)}
        rows, sidebar_rows, viewers = [], [], set()

        for d in dirs:
            sub_files, sub_dirs = content_files(d, self.allowed)
            t = title_for(d, folder, self.titles, self.notes)
            rows.append((t, './%s/' % quote(os.path.basename(d)), self.describe(sub_files, sub_dirs),
                         'available', True, False))
            sidebar_rows.append((url_of(d), t))
            self.folder(d, ctx, sec_title, labels + [t], trail[:-1] + [(trail[-1][0], url), (t, url_of(d))])

        for f in files:
            if os.path.isdir(f):         # a viewer folder holding its own PDF is a file row
                t = title_for(owned_pdf(f), folder, self.titles, self.notes)
                if lone_pdf(f) and not is_own_viewer(f):
                    # a PDF just moved into its own folder: that folder becomes its viewer
                    for name in os.listdir(f):
                        if is_viewer_dir(os.path.join(f, name)):
                            self.remove_dir(os.path.join(f, name))
                            self.drop_children(url_of(os.path.join(f, name)))
                    self.put(os.path.join(f, 'index.html'), viewer_html(
                        url_of(f), ctx, '%s // %s' % (sec_title.upper(), labels[0].upper()), t,
                        trail[:-1] + [(trail[-1][0], url), (t, None)],
                        quote(os.path.basename(lone_pdf(f))), url))
                    self.drop_children(url_of(f))
                rows.append((t, './%s/' % quote(os.path.basename(f)), 'PDF', 'pdf', False, False))
                sidebar_rows.append((url_of(f), t))
                continue
            t = title_for(f, folder, self.titles, self.notes)
            ext = os.path.splitext(f)[1].lstrip('.').lower()
            if ext == 'pdf':
                slug = viewer_slug(f, taken)
                taken.add(slug)
                viewers.add(slug)
                v_dir = os.path.join(folder, slug)
                v_url = url + slug + '/'
                rows.append((t, './%s/' % slug, 'PDF', 'pdf', False, False))
                sidebar_rows.append((v_url, t))
                self.put(os.path.join(v_dir, 'index.html'), viewer_html(
                    v_url, ctx, '%s // %s' % (sec_title.upper(), labels[0].upper()), t,
                    trail[:-1] + [(trail[-1][0], url), (t, None)],
                    '../%s' % quote(os.path.basename(f)), url))
            else:
                href = './%s' % quote(os.path.basename(f))
                rows.append((t, href, ext.upper() or 'FILE', IMAGE_TAG.get(ext, ext), False, True))
                sidebar_rows.append((url + quote(os.path.basename(f)), t))

        # viewers whose PDF is gone (or was renamed) are generated, so they go too
        for name in os.listdir(folder):
            path = os.path.join(folder, name)
            if name not in viewers and name.lower() not in {os.path.basename(d).lower() for d in dirs} \
                    and is_viewer_dir(path):
                self.remove_dir(path)
                self.drop_children(url_of(path))

        state_label = ' // '.join([sec_title] + labels)
        meta = '%s | %s: %s' % (ctx['code'], labels[-1] if len(labels) > 1 else sec_title, labels[0])
        self.put(os.path.join(folder, 'index.html'),
                 listing_html(url, ctx, state_label, trail[:-1] + [(trail[-1][0], None)],
                              tpl.rows(rows), meta))
        self.set_children(url, sidebar_rows)

    # -- Study Material row -------------------------------------------------- #
    def ensure_study_row(self, ctx, sec, sec_title):
        page = ctx['study']
        text = read(page)
        name = os.path.basename(sec)
        if re.search(r'href="(?:\./|%s)%s/"' % (re.escape(url_of(os.path.dirname(sec))), re.escape(name)), text):
            return
        rows = list(ROW_RE.finditer(text))
        if not rows:
            self.notes.append('could not add a %s row to %s (no directory rows found)' % (sec_title, rel(page)))
            return
        end = text.index('</a>', rows[-1].end()) + len('</a>')
        row = ('<a class="dir-row directory-folder" href="%s">'
               '<div class="dir-num">%02d</div><div class="dir-title">%s<span class="dir-title-text">%s</span></div>'
               '<div class="dir-status"><span class="status-tag available">AVAILABLE</span></div>'
               '<div class="dir-arrow">-&gt;</div></a>') % (url_of(sec), len(rows) + 1, tpl.FOLDER, sec_title)
        # Site-wide rule: folder rows sit above file rows, so never leave the new
        # folder appended after a single-file row.
        from sort_academic_folder_rows import sort_folder_rows
        self.put(page, sort_folder_rows(text[:end] + row + text[end:])[0])

    # -- sidebar JSON --------------------------------------------------------- #
    def set_children(self, parent_url, entries, keep_labels=False, merge=False):
        if self.sidebar is None:
            return
        children = self.sidebar.setdefault('children', {})
        old = children.get(parent_url, [])
        labels = {e['url']: e['label'] for e in old}
        new = [{'url': u, 'attrs': next((e.get('attrs', '') for e in old if e['url'] == u), ''),
                'label': labels[u] if keep_labels and u in labels else t} for u, t in entries]
        if merge:
            urls = {e['url'] for e in old}
            new = old + [e for e in new if e['url'] not in urls]
        if new != old:
            children[parent_url] = new

    def drop_children(self, url):
        if self.sidebar is not None:
            self.sidebar.get('children', {}).pop(url, None)

    # -- run ---------------------------------------------------------------- #
    def run(self):
        sections = find_sections()
        added = harvest(sections, self.titles)
        if added:
            self.notes.append('harvested %d existing title(s) into scripts/resource-titles.json' % added)
        for sec in sections:
            self.section(sec)

        if self.check:
            return
        if dump_json(TITLES_FILE, dict(sorted(self.titles.items()))):
            self.changed.append(TITLES_FILE)
        if self.sidebar is not None and dump_json(SIDEBAR_FILE, self.sidebar):
            self.changed.append(SIDEBAR_FILE)
        if self.changed:
            self.stamp_sidebars()

    def stamp_sidebars(self):
        """Run the sidebar builder, but keep its effect inside the courses we touched.

        build_academic_sidebar.py rewrites every academic page. Pages whose sidebar
        has merely drifted from the JSON (formatting, unrelated courses) would
        otherwise ride along into every commit, so anything outside the touched
        courses is put back exactly as it was.
        """
        courses = {os.path.join(ACADEMICS, *rel(p).split('/')[:2]) + os.sep
                   for p in self.changed if os.path.abspath(p).startswith(ACADEMICS + os.sep)}
        pages = glob.glob(os.path.join(DOCS, '**', 'index.html'), recursive=True)
        before = {}
        for p in pages:
            with open(p, 'rb') as fh:
                before[p] = fh.read()
        subprocess.run([sys.executable, SIDEBAR_BUILDER], cwd=REPO, check=True, stdout=subprocess.DEVNULL)
        for p, old in before.items():
            with open(p, 'rb') as fh:
                new = fh.read()
            if new == old:
                continue
            if any(p.startswith(c) for c in courses) and not same_sidebar(old, new):
                if p not in self.changed:
                    self.changed.append(p)
            else:
                with open(p, 'wb') as fh:
                    fh.write(old)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--check', action='store_true', help='report stale pages, write nothing')
    ap.add_argument('--from-index', action='store_true',
                    help='only embed files present in the git index (what the commit will contain)')
    ap.add_argument('--changed-list', metavar='FILE', help='write every touched path to FILE')
    args = ap.parse_args()

    build = Build(args.check, indexed_files() if args.from_index else None)
    build.run()

    for note in build.notes:
        print('  - ' + note)
    if args.check:
        for p in build.stale:
            print('stale: ' + os.path.relpath(p, REPO))
        print('%d resource page(s) out of date' % len(build.stale))
        sys.exit(1 if build.stale else 0)

    print('embed_resources: %d path(s) updated' % len(build.changed))
    if args.changed_list:
        with open(args.changed_list, 'w', encoding='utf-8') as fh:
            fh.write(''.join(os.path.relpath(p, REPO) + '\n' for p in build.changed))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Build annotated-slides/search-index.json for courses, used by docs/javascripts/annotated-search.js.

The index holds each slide's title, slide text, notes, tips and question stems. Answers and option text stay
out, so searching can't reveal them. annotated_slides.build() refreshes the course it just built.

Usage: python3 scripts/annotated_search.py [course-dir ...]   (default: every course with annotated slides)
Also adds the search script to any deck page that doesn't have it yet.
"""
import json
import logging
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import unquote

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, 'docs')
TAG = '<script src="/javascripts/annotated-search.js?v=1"></script>'
BOOKMARK_TAG = '<script src="/javascripts/slide-bookmarks.js?v=3"></script>'
SKIP_TAGS = {'details', 'svg', 'button', 'textarea', 'script', 'style', 'header', 'h4', 'select', 'figure'}
SKIP_CLASSES = {'picks', 'opt-why', 'verdict', 'reveal-ans', 'weight', 'slide-foot', 'num', 'kind'}
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}


class Text(HTMLParser):
    """Visible study text of one card, leaving out answers and controls."""

    def __init__(self, keep_figure=False):
        super().__init__(convert_charrefs=True)
        self.out, self.skip = [], 0
        self.skip_tags = SKIP_TAGS - ({'figure'} if keep_figure else set())

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        classes = set((dict(attrs).get('class') or '').split())
        if self.skip or tag in self.skip_tags or classes & SKIP_CLASSES:
            self.skip += 1

    def handle_endtag(self, tag):
        if tag not in VOID and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def clean(text):
    return re.sub(r'\s+', ' ', text).strip()


def card_text(html):
    parser = Text()
    parser.feed(html)
    return clean(' '.join(parser.out))


def plain(html):
    return clean(re.sub(r'<[^>]+>', ' ', html)).replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'").replace('&#x27;', "'")


def source_pdf(page, deck_dir):
    """The original lecture PDF, from the link in the page's footer."""
    footer = re.search(r'<footer class="end">(.*?)</footer>', page, re.S)
    if not footer:
        return None
    for href in re.findall(r'href="([^"#?]+)"', footer.group(1)):
        href = unquote(href)
        path = os.path.join(DOCS, href.lstrip('/')) if href.startswith('/') else os.path.normpath(os.path.join(deck_dir, href))
        if os.path.isdir(path):  # the deck's slides folder: same pick as annotated_slides.deck_pdf
            pdfs = sorted(f for f in os.listdir(path) if f.endswith('.pdf'))
            path = os.path.join(path, pdfs[0]) if pdfs else ''
        if path.endswith('.pdf') and os.path.exists(path):
            return path
    return None


def pdf_text(path, pages):
    """Per-page text, empty for picture-only pages. A PDF with a different page count is the wrong file, so skip it."""
    import pdfplumber
    from annotated_page import uncid
    logging.getLogger('pdfminer').setLevel(logging.ERROR)
    out = {}
    with pdfplumber.open(path) as pdf:
        if len(pdf.pages) != pages:
            return out
        for i, pg in enumerate(pdf.pages, 1):
            try:
                out[i] = clean(uncid(pg.extract_text() or ''))
            except Exception:
                out[i] = ''
    return out


def read_deck(deck_dir, slug):
    for name in sorted(os.listdir(deck_dir)):
        if not name.endswith('.html') or name == 'index.html':
            continue
        path = os.path.join(deck_dir, name)
        with open(path, encoding='utf-8') as fh:
            page = fh.read()
        if 'id="t-notes"' in page:
            opener, anchor = r'<section class="card[^"]*" id="slide-\d+" data-slide="(\d+)"', 'slide-'
        elif 'id="as-jump"' in page:
            opener, anchor = r'<article\s+class="sheet[^"]*"[^>]*?\sdata-n="(\d+)"', 's-'
        else:
            continue
        return path, page, opener, anchor
    return None


def deck_entry(deck_dir, slug):
    found = read_deck(deck_dir, slug)
    if not found:
        return None
    path, page, opener, anchor = found
    brand = re.search(r'<small>(.*?)</small><strong>(.*?)</strong>', page, re.S)
    chapter = re.sub(r'\s*·\s*Annotated Slides$', '', plain(brand.group(1))) if brand else slug
    title = plain(brand.group(2)) if brand else slug
    end = page.find('</main>')
    marks = list(re.finditer(opener, page))
    words = {}
    if anchor == 'slide-':
        pdf = source_pdf(page, deck_dir)
        if pdf:
            words = pdf_text(pdf, len(marks))
    slides = []
    for i, m in enumerate(marks):
        chunk = page[m.start():marks[i + 1].start() if i + 1 < len(marks) else (end if end > 0 else len(page))]
        n = int(m.group(1))
        if anchor == 'slide-':
            head = re.search(r'<h3>(.*?)</h3>', chunk, re.S)
            name = plain(head.group(1)) if head else ''
        else:
            head = re.search(r'<h2>(.*?)</h2>', chunk, re.S)
            name = plain(head.group(1)) if head else ''
        text = clean('%s %s' % (card_text(chunk), words.get(n, '')))
        slides.append([n, name, text])
    return dict(s=slug, f=os.path.basename(path), t=title, c='%s: %s' % (chapter, title), a=anchor, n=slides), path, page


def build_course(course_dir):
    section = os.path.join(course_dir, 'annotated-slides')
    decks = []
    for slug in sorted(os.listdir(section)):
        deck_dir = os.path.join(section, slug)
        if not os.path.isdir(deck_dir):
            continue
        entry = deck_entry(deck_dir, slug)
        if not entry:
            continue
        data, path, page = entry
        decks.append(data)
        missing = ''.join(t + '\n' for t in (TAG, BOOKMARK_TAG) if t not in page)
        if missing:
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write(page.replace('</body>', missing + '</body>', 1))
    with open(os.path.join(section, 'search-index.json'), 'w', encoding='utf-8') as fh:
        json.dump(dict(decks=decks), fh, ensure_ascii=False, separators=(',', ':'))
    return len(decks), sum(len(d['n']) for d in decks)


def all_courses():
    for root, dirs, _ in os.walk(os.path.join(DOCS, 'academics')):
        if 'annotated-slides' in dirs:
            yield root
            dirs[:] = []


if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    for course in (sys.argv[1:] or sorted(all_courses())):
        n, s = build_course(course)
        size = os.path.getsize(os.path.join(course, 'annotated-slides', 'search-index.json'))
        print('%s: %d decks, %d slides, %d KB' % (os.path.relpath(course, DOCS), n, s, size // 1024), flush=True)

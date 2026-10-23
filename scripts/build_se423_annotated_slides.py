#!/usr/bin/env python3
"""Build SE423 "Annotated Slides": the lecture decks rebuilt as HTML with study notes on top.

Each deck in scripts/se423_annotated/ becomes
  annotated-slides/<slug>/<file>.html   standalone deck (styles/annotated-slides.css + javascripts/annotated-slides.js)
  annotated-slides/<slug>/index.html    site wrapper, cloned from the matching slide-breakdown wrapper
  annotated-slides/<slug>/figures/      diagrams cropped from the original PDF
plus the section directory annotated-slides/index.html (cloned from slides/index.html).

The script also wires the section into the rest of the course: the "Annotated Slides" tab
on every SE423 page that has a tab bar, the SE423 block of the academic sidebar (rendered
with scripts/build_academic_sidebar.py's own functions, so it matches the other sections),
and scripts/academic-sidebar.json. It is safe to re-run.

Usage: python3 scripts/build_se423_annotated_slides.py
"""
import html
import importlib
import json
import os
import re
import subprocess
import sys
import tempfile

import pdfplumber
from PIL import Image, ImageOps

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'scripts'))

import build_academic_sidebar as sidebar  # noqa: E402
from se423_annotated.common import DECKS, PAPERS  # noqa: E402
from se423_annotated import pdftext  # noqa: E402

COURSE = os.path.join(REPO, 'docs', 'academics', 'software-engineering', 'se423')
BASE = '/academics/software-engineering/se423/'
SECTION = BASE + 'annotated-slides/'
SITE = 'https://shoug-tech.com'
AR_LABEL = 'الشرائح المشروحة'

# Decks with annotation content, in course order.
BUILT = ['ch01_introduction', 'ch01_2_performance_domains', 'ch01_3_tailoring', 'ch02_organizational_context', 'ch03_team', 'ch04_development_approach', 'ch05_risk_management', 'ch06_estimation', 'ch06_2_scheduling', 'ch07_quality']

TYPE_LABEL = {'mcq': 'MCQ', 'tf': 'True / False', 'scenario': 'Scenario', 'short': 'Written'}
WEIGHT = {1: ('Low', '●○○'), 2: ('Medium', '●●○'), 3: ('High', '●●●')}
CIRCLED = '⓪①②③④⑤⑥⑦⑧⑨⑩⑪⑫'


def e(s):
    return html.escape(str(s), quote=True)


# --------------------------------------------------------------------------- #
# text markup
# --------------------------------------------------------------------------- #

MARKUP = [
    (re.compile(r'\{\((.+?)\)\}'), r'<span class="pm-circle">\1</span>'),
    (re.compile(r'\{\{(.+?)\}\}'), r'<span class="pm-mark">\1</span>'),
    (re.compile(r'==(.+?)=='), r'<mark class="an-hl">\1</mark>'),
    (re.compile(r'__(.+?)__'), r'<span class="an-ul">\1</span>'),
    (re.compile(r'\(\((.+?)\)\)'), r'<span class="an-circle">\1</span>'),
    (re.compile(r'\*\*\*(.+?)\*\*\*'), r'<strong><em>\1</em></strong>'),
    (re.compile(r'\*\*(.+?)\*\*'), r'<strong>\1</strong>'),
    (re.compile(r'\^(\d+\.\d+|[a-zA-Z])'), r'<sup>\1</sup>'),
    (re.compile(r'\^(\d+)'), lambda m: '<sup class="an-ref">%s</sup>' % CIRCLED[int(m.group(1))]),
]


def rich(text):
    out = html.escape(text, quote=False)
    for pattern, repl in MARKUP:
        out = pattern.sub(repl, out)
    return out.replace('\n', '<br>')


def plain(text):
    """Slide text with the markup stripped (for search snippets and alt text)."""
    out = re.sub(r'\{\((.+?)\)\}|\{\{(.+?)\}\}|==(.+?)==|__(.+?)__|\(\((.+?)\)\)',
                 lambda m: next(g for g in m.groups() if g is not None), text)
    out = re.sub(r'\*+', '', out)
    return re.sub(r'\^\d+', '', out)


def render_lines(lines, start=1):
    """Turn the '-', '--', '#', '##' line prefixes into nested lists."""
    out, stack = [], []  # open lists as (tag, level); each has an open <li>

    def close_deeper(level):
        while stack and stack[-1][1] > level:
            out.append('</li></%s>' % stack.pop()[0])

    for raw in lines:
        m = re.match(r'^(-{1,4}|#{1,2}) (.*)$', raw)
        if not m or m.group(1) == '##':
            close_deeper(0)
            out.append('<h3>%s</h3>' % rich(m.group(2)) if m else '<p>%s</p>' % rich(raw))
            continue
        tag = 'ol' if m.group(1) == '#' else 'ul'
        level = 1 if tag == 'ol' else len(m.group(1))
        close_deeper(level)
        if stack and stack[-1][1] == level and stack[-1][0] == tag:
            out.append('</li><li>')
        else:
            if stack and stack[-1][1] == level:
                out.append('</li></%s>' % stack.pop()[0])
            first = tag == 'ol' and start > 1 and not any(t == 'ol' for t, _ in stack)
            out.append('<%s%s><li>' % (tag, ' start="%d"' % start if first else ''))
            stack.append((tag, level))
        out.append(rich(m.group(2)))
    close_deeper(0)
    return ''.join(out)


def card_points(points):
    items = []
    for p in points:
        head, *subs = p.split('\n')
        sub_html = ''
        if subs:
            sub_html = '<ul>%s</ul>' % ''.join('<li>%s</li>' % rich(s.lstrip('• ').strip()) for s in subs)
        items.append('<li>%s%s</li>' % (rich(head), sub_html))
    return '<ul>%s</ul>' % ''.join(items)


# --------------------------------------------------------------------------- #
# figures
# --------------------------------------------------------------------------- #

def deck_pdf(key):
    folder = os.path.join(COURSE, 'slides', DECKS[key][2])
    return next(os.path.join(folder, f) for f in sorted(os.listdir(folder)) if f.endswith('.pdf'))


def auto_box(pdf, page, mode):
    """Region to crop: the slide's body images ('auto'), the area under the title ('body') or the whole page ('page')."""
    with pdfplumber.open(pdf) as doc:
        p = doc.pages[page - 1]
        if mode == 'auto':
            boxes = [(i['x0'], i['top'], i['x1'], i['bottom']) for i in p.images
                     if i['x1'] - i['x0'] > 25 and i['bottom'] - i['top'] > 18 and i['top'] > 50 and i['bottom'] < float(p.height) - 15
                     and i['x1'] - i['x0'] < float(p.width) * 0.95]
            if boxes:
                return (min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes))
        if mode == 'vec':
            title_bottom = max([w['bottom'] for w in p.extract_words(extra_attrs=['size']) if w['size'] >= 24 and w['top'] < 130] or [50])
            objs = [(o['x0'], o['top'], o['x1'], o['bottom']) for o in p.rects + p.lines + p.curves + p.images
                    if o['top'] > title_bottom + 2 and o['bottom'] < float(p.height) - 36 and (o['x1'] - o['x0']) < float(p.width) * 0.98]
            if objs:
                return (max(0, min(o[0] for o in objs) - 6), min(o[1] for o in objs) - 6,
                        min(float(p.width), max(o[2] for o in objs) + 6), max(o[3] for o in objs) + 6)
        if mode.startswith('below:'):
            return (6, float(mode.split(':')[1]), float(p.width) - 6, float(p.height) - 34)
        if mode == 'page':
            return (4, 4, float(p.width) - 4, float(p.height) - 4)
        return (8, 80, float(p.width) - 8, float(p.height) - 24)


def trim(img, pad=10):
    """Cut the white margin around a crop."""
    grey = img.convert('L').point(lambda v: 255 if v > 244 else 0)
    box = ImageOps.invert(grey).getbbox()
    if not box:
        return img
    x0, y0, x1, y1 = box
    return img.crop((max(0, x0 - pad), max(0, y0 - pad), min(img.width, x1 + pad), min(img.height, y1 + pad)))


def crop_figures(deck, mod, out_dir):
    pdf = deck_pdf(deck['key'])
    os.makedirs(out_dir, exist_ok=True)
    dpi = 220
    k = dpi / 72
    cache_file = os.path.join(tempfile.gettempdir(), 'se423-annotated-crops.json')
    try:
        with open(cache_file) as fh:
            cache = json.load(fh)
    except (OSError, ValueError):
        cache = {}
    for name, (page, box) in getattr(mod, 'CROPS', {}).items():
        target = os.path.join(out_dir, name.rsplit('.', 1)[0] + '.webp')
        # Re-rendering every crop is slow; skip ones whose spec is unchanged since the last run.
        spec = json.dumps([pdf, os.path.getmtime(pdf), page, box])
        if os.path.exists(target) and cache.get(target) == spec:
            continue
        cache[target] = spec
        mode = box if isinstance(box, str) else None
        x0, y0, x1, y1 = auto_box(pdf, page, mode) if mode else box
        with tempfile.TemporaryDirectory() as tmp:
            stem = os.path.join(tmp, 'crop')
            subprocess.run(['pdftoppm', '-r', str(dpi), '-f', str(page), '-l', str(page), '-singlefile', '-png',
                            '-x', str(int(x0 * k)), '-y', str(int(y0 * k)),
                            '-W', str(int((x1 - x0) * k)), '-H', str(int((y1 - y0) * k)), pdf, stem],
                           check=True, stderr=subprocess.DEVNULL)
            img = Image.open(stem + '.png').convert('RGB')
            if mode:
                img = trim(img)
            img.save(target, 'WEBP', quality=86, method=6)
    with open(cache_file, 'w') as fh:
        json.dump(cache, fh)


def figure_html(fig, slug):
    name, alt, cap = fig[:3]
    big = len(fig) > 3 and fig[3]
    src = 'figures/' + name.rsplit('.', 1)[0] + '.webp'
    path = os.path.join(COURSE, 'annotated-slides', slug, src)
    w, h = Image.open(path).size
    shape = ' tall' if big or h > w * 1.1 else ''
    return ('<figure class="slide-fig%s"><img src="%s" alt="%s" width="%d" height="%d" loading="lazy" decoding="async">'
            '<figcaption>%s</figcaption></figure>' % (shape, src, e(alt), w, h, rich(cap)))


def chart_svg(chart):
    pts = chart['points']
    w, h, left, right, top, bottom = 640, 300, 64, 18, 34, 34
    ymax = 1400000
    xs = [left + i * (w - left - right) / (len(pts) - 1) for i in range(len(pts))]
    ys = [top + (1 - v / ymax) * (h - top - bottom) for _, v in pts]
    grid = ''.join(
        '<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" stroke="#e3e3e3"/><text x="%d" y="%.1f" text-anchor="end" font-size="11" fill="#555">%s</text>'
        % (left, w - right, top + (1 - g / ymax) * (h - top - bottom), top + (1 - g / ymax) * (h - top - bottom),
           left - 6, top + (1 - g / ymax) * (h - top - bottom) + 4, '{:,}'.format(g))
        for g in range(0, ymax + 1, 200000))
    line = '<polyline fill="none" stroke="#21a35b" stroke-width="3" points="%s"/>' % ' '.join(
        '%.1f,%.1f' % p for p in zip(xs, ys))
    dots = ''.join('<circle cx="%.1f" cy="%.1f" r="3.6" fill="#21a35b"/>' % p for p in zip(xs, ys))
    labels = ''.join('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="9.5" fill="#333">%s</text>'
                     % (x, y - 8, '{:,}'.format(v)) for x, y, (_, v) in zip(xs, ys, pts))
    years = ''.join('<text x="%.1f" y="%d" text-anchor="middle" font-size="11" fill="#555">%d</text>'
                    % (x, h - 12, yr) for x, (yr, _) in zip(xs, pts))
    title = '<text x="%d" y="18" text-anchor="middle" font-size="13" font-weight="700" fill="#222">%s</text>' % (
        w // 2, e(chart['title']))
    desc = '; '.join('%d: %s' % (yr, '{:,}'.format(v)) for yr, v in pts)
    return ('<figure class="slide-fig"><svg viewBox="0 0 %d %d" role="img" aria-label="%s. %s">%s%s%s%s%s%s</svg>'
            '<figcaption>Redrawn from the slide’s chart (the original image is overlapped by slide text).</figcaption></figure>'
            % (w, h, e(chart['title']), e(desc), title, grid, line, dots, labels, years))


# --------------------------------------------------------------------------- #
# deck page
# --------------------------------------------------------------------------- #

def deck_url(key, n=None):
    slug, file_, folder, _ = DECKS[key]
    if key in BUILT_KEYS:
        return '../%s/%s.html%s' % (slug, file_, '#s-%d' % n if n else ''), False
    return BASE + 'slides/%s/' % folder, True


def render_slide(deck, s, mod):
    slug = deck['slug']
    kind = s['kind']
    n = s['n']
    head = ''
    if kind == 'content':
        sub = '<span class="sub">%s</span>' % e(s['sub']) if s['sub'] else ''
        head = '<div class="slide-head"><h2>%s%s</h2></div>' % (e(s['title']), sub)
        inner = []
        if s['card']:
            name, lead, points = s['card']
            inner.append('<div class="pcard"><h4>%s</h4><div class="pcard-body"><div class="pcard-lead">%s</div>%s</div></div>'
                         % (e(name), rich(lead), card_points(points)))
        elif s['cols']:
            cols, start = [], 1
            for col in s['cols']:
                cols.append('<div>%s</div>' % render_lines(col, start))
                start += sum(1 for line in col if line.startswith('# '))
            inner.append('<div class="slide-cols">%s</div>' % ''.join(cols))
        elif s['body']:
            inner.append('<div class="slide-text">%s</div>' % render_lines(s['body']))
        figs = s['fig'] if isinstance(s['fig'], list) else [s['fig']] if s['fig'] else []
        if len(figs) > 1:
            inner.append('<div class="fig-stack">%s</div>' % ''.join(figure_html(f, slug) for f in figs))
        elif figs:
            inner.append(figure_html(figs[0], slug))
        if s['chart']:
            inner.append(chart_svg(getattr(mod, 'CHARTS', {})[s['chart']]))
        has_text = bool(s['card'] or s['cols'] or s['body'])
        has_fig = bool(s['fig'] or s['chart'])
        cls = 'slide-body' + (' has-fig' if has_text and has_fig else '') + (' fig-only' if has_fig and not has_text else '')
        body = '<div class="%s">%s</div>' % (cls, ''.join(inner))
    else:
        sub = '<div class="tsub">%s</div>' % e(s['sub']) if s['sub'] else ''
        body = '<h2>%s</h2>%s' % (e(s['title']), sub)
    foot = '<div class="slide-foot"><span class="bar"></span><span class="num">%d</span></div>' % n
    direct = [p for p in s['past'] if not p['related']]
    stamp = '<div class="stamp">★ Past exam</div>' if direct else ''
    slide_html = '<div class="slide %s">%s<div class="slide-inner">%s%s%s</div></div>' % (kind, stamp, head, body, foot)
    prof = ''.join('<p class="prof-note">%s</p>' % rich(p) for p in s['prof'])

    margin = ''
    if s['notes'] or kind == 'content':
        label, dots = WEIGHT[s['weight']]
        notes = ''.join('<li data-n="%d">%s</li>' % (i, rich(t)) for i, t in enumerate(s['notes'], 1))
        margin = ('<aside class="margin" aria-label="Notes for slide %d"><div class="weight" title="How likely this slide is to be examined">'
                  'Exam weight <span class="dots" aria-hidden="true">%s</span> %s</div><ol>%s</ol></aside>'
                  % (n, dots, label, notes))

    extras = []
    if s['tips']:
        names = {'tip': 'Tip', 'trick': 'Memory trick', 'trap': 'Exam trap'}
        extras.append('<div class="stickies">%s</div>' % ''.join(
            '<div class="sticky %s"><b>%s</b>%s</div>' % (k, names[k], rich(t)) for k, t in s['tips']))
    if s['past']:
        links = []
        for p in s['past']:
            title, folder = PAPERS[p['paper']]
            links.append('<a class="%s" href="%sexams/%s/" target="_top">%s%s · %s</a>' % (
                'rel' if p['related'] else 'dir', BASE, folder, '' if p['related'] else '★ ', e(title), e(p['label'])))
        label = 'Asked in a real exam' if direct else 'Related real-exam questions'
        extras.append('<div class="past"><p class="row-label">%s</p><div class="links">%s</div></div>' % (label, ''.join(links)))
    if s['seen']:
        links = []
        for ref in s['seen']:
            if ref['deck'] == deck['key']:
                href, external = '#s-%d' % ref['n'], False
            else:
                href, external = deck_url(ref['deck'], ref['n'])
            chapter = DECKS[ref['deck']][3].split(' · ')[0]
            target = ' target="_top"' if external else ''
            links.append('<a href="%s"%s>↻ %s, slide %d · <small>%s</small></a>' % (
                e(href), target, e(chapter if ref['deck'] != deck['key'] else 'This deck'), ref['n'], e(ref['label'])))
        extras.append('<div class="seen"><p class="row-label">Seen again</p><div class="links">%s</div></div>' % ''.join(links))
    if s['exam']:
        qs = []
        for i, q in enumerate(s['exam']):
            t = q['type']
            head_q = '<span class="q-type %s">%s</span>' % (t, TYPE_LABEL[t])
            if t == 'mcq':
                opts = ''.join('<button type="button" class="opt" data-right="%d">%s</button>'
                               % (int(j == q['a']), e(o)) for j, o in enumerate(q['opts']))
                why = q['why'] or 'Correct: %s.' % q['opts'][q['a']]
                body_q = '<div class="opts">%s</div><p class="why" hidden>%s</p>' % (opts, e(why))
            elif t == 'tf':
                opts = ''.join('<button type="button" class="opt" data-right="%d">%s</button>' % (int(v == q['a']), v)
                               for v in (True, False))
                why = ('True. ' if q['a'] else 'False. ') + q['why']
                body_q = '<div class="opts tf-opts">%s</div><p class="why" hidden>%s</p>' % (opts, e(why.strip()))
            else:
                body_q = ('<button type="button" class="reveal" aria-expanded="false">Show model answer</button>'
                          '<p class="why" hidden>%s</p>' % e(q['a']))
            qs.append('<div class="q">%s<p>%s</p>%s</div>' % (head_q, e(q['q']), body_q))
        extras.append('<details class="radar" open><summary>🎯 How this can come up · %d question%s</summary>'
                      '<div class="radar-items">%s</div></details>' % (len(qs), '' if len(qs) == 1 else 's', ''.join(qs)))

    grid_cls = 'sheet' + ('' if margin else ' no-margin')
    return ('<article class="%s" id="s-%d" data-n="%d" data-past="%d" aria-label="Slide %d: %s">'
            '<div class="sheet-grid"><div>%s%s</div>%s</div>%s</article>'
            % (grid_cls, n, n, int(bool(s['past'])), n, e(s['title']), slide_html, prof, margin,
               '<div class="extras">%s</div>' % ''.join(extras) if extras else ''))


MARK_WRAP = {'pm': '{{%s}}', 'pmc': '{(%s)}', 'hl': '==%s==', 'ul': '__%s__', 'circ': '((%s))'}


def overlay(lines, ann, n):
    """Apply an annotation's phrase marks and note anchors to the slide's text lines."""
    lines = list(lines)

    def place(phrase, fmt):
        for i, line in enumerate(lines):
            bare = line.replace('**', '')
            if phrase in line:
                lines[i] = line.replace(phrase, fmt % phrase, 1)
                return
            if phrase in bare and '**' in line:
                lines[i] = bare.replace(phrase, fmt % phrase, 1)
                return
        raise ValueError('slide %d: phrase not found: %r' % (n, phrase))
    for i, phrase in enumerate(ann.get('refs', ()), 1):
        if phrase is not None:
            place(phrase, '%s^' + str(i))
    for key, fmt in MARK_WRAP.items():
        for phrase in ann.get(key, ()):
            place(phrase, fmt)
    return lines


def deck_slides(mod):
    """Slides for a deck: hand-written (SLIDES) or the PDF's own text plus annotations (ANN)."""
    if hasattr(mod, 'SLIDES'):
        return mod.SLIDES
    from se423_annotated.common import slide as make
    pages = pdftext.read_deck(deck_pdf(mod.DECK['key']))
    out = []
    for p in pages:
        ann = mod.ANN.get(p['n'], {})
        if ann.get('skip'):
            continue
        kind = ann.get('kind', p['kind'])
        body = ann['body'] if 'body' in ann else ([] if ann.get('drop_body') else p['body'])
        for bad, good in list(getattr(mod, 'FIX', {}).items()) + list(ann.get('fix', {}).items()):
            body = [line.replace(bad, good) for line in body]
        body = [line for line in body if line.strip('*- ') not in ann.get('drop_lines', ())]
        if 'body' not in ann:
            body = overlay(body, ann, p['n'])
        elif ann.get('refs') or any(k in ann for k in MARK_WRAP):
            body = overlay(body, ann, p['n'])
        weight = ann.get('weight', 2 if ann.get('exam') or ann.get('past') else 1)
        out.append(make(p['n'], ann.get('title', p['title']), body, kind=kind, sub=ann.get('sub'), cols=ann.get('cols'),
                        card=ann.get('card'), fig=ann.get('fig'), chart=ann.get('chart'), notes=ann.get('notes', ()),
                        prof=ann.get('prof', ()), tips=ann.get('tips', ()), seen=ann.get('seen', ()),
                        exam=ann.get('exam', ()), past=ann.get('past', ()), weight=weight))
    return out


def deck_page(deck, mod):
    slides = deck_slides(mod)
    n_q = sum(len(s['exam']) for s in slides)
    n_past = sum(1 for s in slides if any(not p['related'] for p in s['past']))
    n_rel = sum(1 for s in slides if s['past']) - n_past
    title = '%s — %s' % (deck['chapter'], deck['title'])
    options = ''.join('<option value="s-%d">%d · %s</option>' % (s['n'], s['n'], e(s['title'])) for s in slides)
    sheets = ''.join(render_slide(deck, s, mod) for s in slides)
    desc = 'SE423 %s annotated slides: every slide rebuilt with notes, memory tricks, cross-references and likely exam questions.' % title
    return '''<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SE423 · Annotated Slides · {title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{site}{section}{slug}/">
<meta name="robots" content="noindex, follow">
<link rel="icon" type="image/png" sizes="256x256" href="/assets/shoug-favicon-v4.png">
<script>try{{var t=localStorage.getItem("shoug-theme");document.documentElement.setAttribute("data-theme",t==="dark"||t==="light"?t:(matchMedia("(prefers-color-scheme: light)").matches?"light":"dark"))}}catch(e){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles/annotated-slides.css">
</head>
<body class="mode-scroll">
<header class="as-top"><div class="as-wrap">
<div class="as-brand"><small>SE423 · Annotated Slides</small><strong>{title}</strong></div>
<div class="as-controls">
<div class="seg" role="group" aria-label="View mode"><button type="button" data-group="mode" data-value="scroll" aria-pressed="true">Scroll</button><button type="button" data-group="mode" data-value="flip" aria-pressed="false">Flip</button></div>
<div class="seg" role="group" aria-label="Which slides"><button type="button" data-group="filter" data-value="all" aria-pressed="true">All</button><button type="button" data-group="filter" data-value="past" aria-pressed="false">★ Exam slides</button></div>
<button type="button" class="chip-btn" id="as-ann" aria-pressed="true">✎ Notes on</button>
<button type="button" class="chip-btn" id="as-theme">☾ Dark</button>
<select class="as-jump" id="as-jump" aria-label="Jump to slide">{options}</select>
</div></div></header>
<div class="as-wrap">
<section class="as-intro">
<div class="kicker">{chapter} · Annotated slides</div>
<h1>{name}</h1>
<p>{lede}</p>
<ul class="as-stats"><li><b>{count}</b> slides</li><li><b>{n_past}</b> asked in real exams</li><li><b>{n_rel}</b> related to real exam questions</li><li><b>{n_q}</b> practice questions</li></ul>
<div class="legend" aria-label="Ink key">
<span><i class="lg-ink"></i>Slide text</span>
<span><i class="lg-prof"></i>Instructor’s marks (from the original PDF)</span>
<span><i class="lg-red"></i>Study notes</span>
<span><i class="lg-hl"></i>Highlight: key words</span>
<span><i class="lg-tip"></i>Tips, tricks &amp; traps</span>
<span><i class="lg-seen"></i>Seen again elsewhere</span>
<span><i class="lg-exam"></i>How it can come up</span>
</div>
</section>
<main class="as-deck" id="main">
{sheets}
<p class="empty-filter" id="as-empty" hidden>No slides match this filter.</p>
</main>
<footer class="as-foot">Rebuilt from the SE423 lecture slides as a study aid. Check exact wording against the <a href="{pdf}" target="_top">original deck</a>. Made by Shoug Alomran.</footer>
</div>
<nav class="flipbar" aria-label="Slide navigation"><button type="button" id="flip-prev" aria-label="Previous slide">◀ Prev</button><div class="flip-pos"><span id="flip-text">Slide 1</span><span class="track"><span class="fill" id="flip-fill"></span></span></div><button type="button" id="flip-next" aria-label="Next slide">Next ▶</button></nav>
<script src="/javascripts/annotated-slides.js"></script>
</body>
</html>
'''.format(title=e(title), desc=e(desc), site=SITE, section=SECTION, slug=deck['slug'], options=options,
           chapter=e(deck['chapter']), name=e(deck['title']), lede=e(deck['lede']), count=len(slides),
           n_past=n_past, n_rel=n_rel, n_q=n_q, sheets=sheets, pdf=deck['pdf'])


# --------------------------------------------------------------------------- #
# site wiring
# --------------------------------------------------------------------------- #

def read(path):
    with open(path, encoding='utf-8') as fh:
        return fh.read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(text)
    print('wrote', os.path.relpath(path, REPO))


def update_sidebar_data():
    data = sidebar.load_data()
    entry = {'url': SECTION, 'attrs': 'data-en-text="ANNOTATED SLIDES" data-ar-text="%s"' % AR_LABEL,
             'label': 'ANNOTATED SLIDES'}
    sections = data['sections'][BASE]
    sections[:] = [s for s in sections if s['url'] != SECTION]
    at = next(i for i, s in enumerate(sections) if s['url'] == BASE + 'slides/') + 1
    sections.insert(at, entry)
    data['children'][SECTION] = [
        {'url': SECTION + DECKS[k][0] + '/', 'attrs': '', 'label': '%s - %s' % (DECKS[k][3].split(' · ')[1], DECKS[k][3].split(' · ')[0].replace('Ch ', 'Chapter '))}
        for k in DECKS if k in BUILT_KEYS]
    with open(sidebar.DATA_FILE, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write('\n')
    return data


def section_block_span(page):
    """(start, end) of the SE423 section list inside the sidebar."""
    course = re.search(r'href="%s"\s*>(?:<span class="status-dot"></span>)?\s*SE423</a' % re.escape(BASE), page)
    if not course:
        return None
    start = page.find('<ul class="tree-children section-children">', course.end())
    if start < 0:
        return None
    depth = 0
    for m in sidebar.UL_TAG_RE.finditer(page, start):
        depth += 1 if m.group(0).startswith('<ul') else -1
        if depth == 0:
            return start, m.end()
    return None


def set_sections(page, data, url):
    span = section_block_span(page)
    if not span:
        return page
    return page[:span[0]] + sidebar.render_sections(data, BASE, url) + page[span[1]:]


TAB_RE = re.compile(r'(?P<indent>[ \t]*)<a\s+href="%sslides/"\s+class="tab(?: active)?"[^>]*>\s*Slides</a\s*>' % re.escape(BASE))


def add_tab(page, active=False):
    if 'href="%s" class="tab' % SECTION in page or re.search(r'href="%s"\s+class="tab' % re.escape(SECTION), page):
        return page
    m = TAB_RE.search(page)
    if not m:
        return page
    ind = m.group('indent')
    tab = ('\n%s<a\n%s  href="%s"\n%s  class="tab%s"\n%s  data-en-text="Annotated Slides"\n%s  data-ar-text="%s"\n%s  >Annotated Slides</a\n%s>'
           % (ind, ind, SECTION, ind, ' active' if active else '', ind, ind, AR_LABEL, ind, ind))
    return page[:m.end()] + tab + page[m.end():]


def page_url(path):
    rel = os.path.relpath(os.path.dirname(path), os.path.join(REPO, 'docs'))
    return '/' + rel.replace(os.sep, '/') + '/'


def replace_meta(page, title, desc, url_from, url_to):
    page = re.sub(r'<title>.*?</title>', '<title>%s</title>' % title, page, count=1, flags=re.S)
    for attr, value in (('name="description"', desc), ('property="og:title"', title), ('property="og:description"', desc),
                        ('name="twitter:title"', title), ('name="twitter:description"', desc)):
        page = re.sub(r'(<meta\s+%s\s+content=")[^"]*(")' % re.escape(attr), lambda m: m.group(1) + value + m.group(2), page)
    page = re.sub(r'("name":\s*")[^"]*(")', lambda m: m.group(1) + title + m.group(2), page, count=1)
    page = re.sub(r'("description":\s*")[^"]*(")', lambda m: m.group(1) + desc + m.group(2), page, count=1)
    head_end = page.index('</head>')
    return page[:head_end].replace(url_from, url_to) + page[head_end:]


def outside_nav(page, fn):
    m = sidebar.NAV_RE.search(page)
    if not m:
        return fn(page)
    return fn(page[:m.start()]) + m.group(0) + fn(page[m.end():])


def build_wrapper(deck, data, prev_key, next_key):
    key = deck['key']
    template_dir = os.path.join(COURSE, 'slide-breakdowns', '01-introduction')
    page = read(os.path.join(template_dir, 'index.html'))
    url = SECTION + deck['slug'] + '/'
    name = '%s - %s' % (deck['title'], deck['chapter'])
    title = 'SE423 | %s (Annotated Slides)' % e(name)
    desc = 'SE423 %s annotated slides: the original slides rebuilt with study notes, memory tricks, cross-references and likely exam questions.' % e(name)
    page = replace_meta(page, title, desc, BASE + 'slide-breakdowns/01-introduction/', url)

    def body(part):
        part = re.sub(r'href="%sslide-breakdowns/"\s*>Slide Breakdowns</a\s*>\s*/\s*<span class="current"\s*>.*?</span\s*>' % re.escape(BASE),
                      'href="%s"\n              >Annotated Slides</a\n            >\n            /<span class="current">%s</span>' % (SECTION, e(name)),
                      part, flags=re.S)
        part = part.replace('ITEM_01 // SLIDE BREAKDOWNS', 'ITEM_%02d // ANNOTATED SLIDES' % (list(DECKS).index(key) + 1))
        part = re.sub(r'<h1 class="ch-title">.*?</h1>', '<h1 class="ch-title">%s</h1>' % e(name), part, flags=re.S)
        part = part.replace('href="./introduction.html"', 'href="./%s.html"' % deck['file'])
        part = part.replace('src="./introduction.html"', 'src="./%s.html"' % deck['file'])
        part = part.replace('href="%sslide-breakdowns/"' % BASE, 'href="%s"' % SECTION)
        part = part.replace('title="Slide breakdown"', 'title="Annotated slides"')

        def nav_link(k, cls, text):
            if not k:
                return '<span class="nav-link %s disabled">%s</span>' % (cls, text)
            return '<a\n            href="%s%s/"\n            class="nav-link %s"\n            >%s</a\n          >' % (SECTION, DECKS[k][0], cls, text)
        part = re.sub(r'<div class="nav-strip">.*?</div>',
                      '<div class="nav-strip">\n          %s\n          %s\n        </div>' % (
                          nav_link(prev_key, 'prev', '&lt;- PREVIOUS'), nav_link(next_key, 'next', 'NEXT -&gt;')),
                      part, count=1, flags=re.S)
        return part
    page = outside_nav(page, body)
    page = set_sections(page, data, url)
    write(os.path.join(COURSE, 'annotated-slides', deck['slug'], 'index.html'), page)


def build_directory(data):
    page = read(os.path.join(COURSE, 'slides', 'index.html'))
    title = 'SHOUG.TECH | SE423 Annotated Slides'
    desc = ('SE423 Software Project Management annotated slides: every lecture slide rebuilt with study notes, '
            'memory tricks, cross-references, past-exam links and likely exam questions.')
    page = replace_meta(page, title, desc, BASE + 'slides/', SECTION)

    def body(part):
        part = re.sub(r'<span class="current" data-en-text="Slides" data-ar-text="الشرائح"\s*>Slides</span\s*>',
                      '<span class="current" data-en-text="Annotated Slides" data-ar-text="%s">Annotated Slides</span>' % AR_LABEL, part)
        part = re.sub(r'<div class="type-label" data-en-text="SLIDES" data-ar-text="الشرائح">\s*SLIDES\s*</div>',
                      '<div class="type-label" data-en-text="ANNOTATED SLIDES" data-ar-text="%s">ANNOTATED SLIDES</div>' % AR_LABEL, part)
        part = re.sub(r'(<a\s+href="%sslides/"\s+class=")tab active(")' % re.escape(BASE), r'\1tab\2', part)
        part = add_tab(part, active=True)
        rows = []
        arrow = ('<div class="dir-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
                 'stroke-linecap="square"><path d="M5 12h14M12 5l7 7-7 7" /></svg></div>')
        for i, (k, (slug, _, _, label)) in enumerate(DECKS.items(), 1):
            chapter, name = label.split(' · ')
            text = '%s - %s' % (name, chapter.replace('Ch ', 'Chapter '))
            if k in BUILT_KEYS:
                rows.append('<a href="%s%s/" class="dir-row"><div class="dir-num">%02d</div><div class="dir-title">%s</div>'
                            '<div class="dir-status"><span class="status-tag available">AVAILABLE</span></div>%s</a>'
                            % (SECTION, slug, i, e(text), arrow))
            else:
                rows.append('<div class="dir-row"><div class="dir-num">%02d</div><div class="dir-title">%s</div>'
                            '<div class="dir-status"><span class="status-tag coming-soon">COMING SOON</span></div>%s</div>'
                            % (i, e(text), arrow))
        start = part.find('<div class="directory-container">')
        if start >= 0:
            header_end = part.index('</div>', part.index('<div class="dir-header">', start)) + len('</div>')
            depth, end = 0, None
            for m in re.finditer(r'<div\b|</div>', part[start:]):
                depth += 1 if m.group(0) == '<div' else -1
                if depth == 0:
                    end = start + m.end()
                    break
            part = part[:header_end] + '\n          ' + '\n          '.join(rows) + '\n        </div>' + part[end:]
        return part
    page = outside_nav(page, body)
    page = set_sections(page, data, SECTION)
    write(os.path.join(COURSE, 'annotated-slides', 'index.html'), page)


SLIDES_LI_RE = re.compile(
    r'(?P<indent>[ \t]*)<li class="tree-item tree-section[^"]*">\s*<a\s+class="tree-file"\s+href="%sslides/".*?</li>' % re.escape(BASE),
    re.S)


def add_section_li(page):
    """Insert the ANNOTATED SLIDES entry after SLIDES (and its open item list), in the page's own formatting."""
    span = section_block_span(page)
    if not span or 'href="%s"' % SECTION in page[span[0]:span[1]]:
        return page
    m = SLIDES_LI_RE.search(page, span[0], span[1])
    if not m:
        return page
    at = m.end()
    nxt = re.match(r'\s*<ul class="tree-children item-children', page[at:])
    if nxt:
        depth = 0
        for t in sidebar.UL_TAG_RE.finditer(page, at):
            depth += 1 if t.group(0).startswith('<ul') else -1
            if depth == 0:
                at = t.end()
                break
    attrs = 'data-en-text="ANNOTATED SLIDES" data-ar-text="%s"' % AR_LABEL
    if '\n' in m.group(0):
        ind = m.group('indent')
        li = ('\n%s<li class="tree-item tree-section">\n%s  <a\n%s    class="tree-file"\n%s    href="%s"\n'
              '%s    data-en-text="ANNOTATED SLIDES"\n%s    data-ar-text="%s"\n%s    >ANNOTATED SLIDES</a\n%s  >\n%s</li>'
              % (ind, ind, ind, ind, SECTION, ind, ind, AR_LABEL, ind, ind, ind))
    else:
        li = sidebar.link(SECTION, 'ANNOTATED SLIDES', attrs, classes='tree-item tree-section')
    return page[:at] + li + page[at:]


def wire_course_pages():
    """Add the tab and the sidebar entry to every other SE423 page."""
    skip = os.path.join(COURSE, 'annotated-slides')
    changed = 0
    for dirpath, _, files in os.walk(COURSE):
        if dirpath.startswith(skip) or 'index.html' not in files:
            continue
        path = os.path.join(dirpath, 'index.html')
        page = read(path)
        new = add_section_li(add_tab(page))
        if new != page:
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write(new)
            changed += 1
    print('wired %d existing SE423 page(s)' % changed)


# --------------------------------------------------------------------------- #

def main():
    global BUILT_KEYS
    mods = [importlib.import_module('se423_annotated.' + name) for name in BUILT]
    BUILT_KEYS = {m.DECK['key'] for m in mods}
    data = update_sidebar_data()
    keys = [k for k in DECKS if k in BUILT_KEYS]
    for mod in mods:
        deck = mod.DECK
        out = os.path.join(COURSE, 'annotated-slides', deck['slug'])
        crop_figures(deck, mod, os.path.join(out, 'figures'))
        write(os.path.join(out, deck['file'] + '.html'), deck_page(deck, mod))
        i = keys.index(deck['key'])
        build_wrapper(deck, data, keys[i - 1] if i > 0 else None, keys[i + 1] if i + 1 < len(keys) else None)
    build_directory(data)
    wire_course_pages()


BUILT_KEYS = set()

if __name__ == '__main__':
    main()

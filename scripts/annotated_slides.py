"""Shared builder for a course's "Annotated Slides": lecture decks rebuilt as HTML with study notes on top.

Each deck module (scripts/<course>_annotated/) becomes
  annotated-slides/<slug>/<file>.html   standalone deck (styles/annotated-slides.css + javascripts/annotated-slides.js)
  annotated-slides/<slug>/index.html    site wrapper, cloned from one of the course's slide-breakdown wrappers
  annotated-slides/<slug>/figures/      diagrams cropped from the original PDF
plus the section directory annotated-slides/index.html (cloned from slides/index.html).

It also wires the section into the rest of the course: the "Annotated Slides" tab on every
course page that has a tab bar, the course block of the academic sidebar (rendered with
scripts/build_academic_sidebar.py's own functions, so it matches the other sections), and
scripts/academic-sidebar.json. It is safe to re-run.

A course calls build(Course(...)); see build_se423_annotated_slides.py and
build_cs331_annotated_slides.py.
"""
import glob
import hashlib
import html
import importlib
import json
import os
import re
import subprocess
import sys
import tempfile
import csv
import io

import pdfplumber
from PIL import Image, ImageDraw, ImageOps

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'scripts'))

import build_academic_sidebar as sidebar  # noqa: E402

SITE = 'https://shoug-tech.com'
AR_LABEL = 'الشرائح المشروحة'


class Course:
    """Everything that differs between courses.

    code, name       'SE423', 'Software Project Management'
    track            folder under docs/academics, e.g. 'software-engineering'
    package          the content package, e.g. 'se423_annotated' (its common.py holds DECKS and PAPERS)
    built            deck modules with annotation content, in course order
    read_deck        pdf path -> pages (the package's pdftext.read_deck)
    template         slide-breakdown wrapper to clone: (folder, standalone file name), or
                     (other course path, folder, file) to borrow one from a course of the same track
    after            section the new tab and sidebar entry follow: (url part, tab label)
    page_name        deck -> name used in the wrapper title and breadcrumb
    item_label       DECKS label -> label in the sidebar and the section directory
    papers           wording for real-exam links (see PAPER_WORDS)
    prof_legend      whether decks carry instructor marks from the PDF
    """

    def __init__(self, **kw):
        self.papers = PAPER_WORDS
        self.prof_legend = True
        self.__dict__.update(kw)
        self.dir = os.path.join(REPO, 'docs', 'academics', self.track, self.code.lower())
        self.base = '/academics/%s/%s/' % (self.track, self.code.lower())
        self.section = self.base + 'annotated-slides/'
        common = importlib.import_module(self.package + '.common')
        self.decks, self.paper_list = common.DECKS, common.PAPERS
        self.built_keys = set()


PAPER_WORDS = {'stamp': '★ Past exam', 'direct': 'Asked in a real exam', 'related': 'Related real-exam questions',
               'n_direct': 'asked in real exams', 'n_related': 'related to real exam questions', 'folder': 'exams/',
               'desc': 'past-exam'}

C = None  # the course being built

TYPE_LABEL = {'mcq': 'MCQ', 'tf': 'True / False', 'scenario': 'Scenario', 'short': 'Written'}
WEIGHT = {1: ('Low', '●○○'), 2: ('Medium', '●●○'), 3: ('High', '●●●')}
CIRCLED = '⓪①②③④⑤⑥⑦⑧⑨⑩⑪⑫'


# Figures and whole-slide images are JPEG so they open and save in Preview and other image editors.
FIG_EXT = '.jpg'

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

def deck_folder(key):
    """A deck's PDF folder: under slides/ unless DECKS names another section."""
    folder = C.decks[key][2]
    return folder if '/' in folder else 'slides/' + folder


def deck_pdf(key):
    folder = os.path.join(C.dir, deck_folder(key))
    if folder.endswith('.pdf'):  # a deck stored as a loose PDF in slides/
        return folder
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
        if mode == 'fig':
            # Everything drawn under the title line: pictures, shapes and their labels, minus the
            # page frame, the template's corner decoration and the footer.
            w, h = float(p.width), float(p.height)
            words = p.extract_words()
            top = [x for x in words if x['top'] < 110]
            title_bottom = 0
            if top:
                first = min(x['top'] for x in top)
                title_bottom = max(x['bottom'] for x in top if x['top'] - first < 4)
            y_min = max(title_bottom + 2, 48)
            objs = [(o['x0'], o['top'], o['x1'], o['bottom']) for o in p.images + p.rects + p.curves + p.lines + words
                    if o['top'] >= y_min and o['bottom'] < h - 30 and not (o['x1'] < 100 and o['top'] < 85)
                    and not (o['x1'] - o['x0'] > w * 0.97 and o['bottom'] - o['top'] > h * 0.9)]
            if objs:
                return (max(0, min(o[0] for o in objs) - 6), min(o[1] for o in objs) - 4,
                        min(w, max(o[2] for o in objs) + 6), min(h, max(o[3] for o in objs) + 6))
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


_PAGES = {}


def read_pages(pdf):
    """C.read_deck, read once per build."""
    if pdf not in _PAGES:
        _PAGES[pdf] = C.read_deck(pdf)
    return _PAGES[pdf]


def auto_figure(mod, p, ann):
    """With AUTO_SLIDES on, a slide that has no hand-made figure or body gets one: the whole slide
    when its layout is too rich to retype (tables, diagrams, two columns), else its picture."""
    if getattr(mod, 'AUTO_SLIDES', False) == 'all':
        return 'slide-%02d.png' % p['n'], 'slide'
    if not getattr(mod, 'AUTO_SLIDES', False):
        return None
    if p['kind'] == 'title' and 'kind' not in ann and 'title' not in ann:
        return 'slide-%02d.png' % p['n'], 'slide'  # an unannotated cover slide: show the cover itself
    if ann.get('kind', p['kind']) != 'content':
        return None
    if any(k in ann for k in ('fig', 'body', 'cols', 'card', 'chart')) or ann.get('drop_body') or ann.get('no_auto'):
        return None
    if p['complex'] or ann.get('whole'):
        return 'slide-%02d.png' % p['n'], 'slide'
    if p['pictures']:
        return 'picture-%02d.png' % p['n'], 'auto'
    return None


def deck_crops(mod):
    crops = dict(getattr(mod, 'CROPS', {}))
    if getattr(mod, 'AUTO_SLIDES', False):
        for p in read_pages(deck_pdf(mod.DECK['key'])):
            auto = auto_figure(mod, p, mod.ANN.get(p['n'], {}))
            if auto:
                crops[auto[0]] = (p['n'], auto[1])
    return crops


_HIGHLIGHT_STOP = set('a an and are as at be been between by can code do does for from has have how in into is it its of on or that the their them then there these this to was were what when where which with would'.split())
_HIGHLIGHT_GENERIC = set('chapter lecture slide slides overview summary introduction extra example examples design software system component components class method object objects pattern patterns code diagram figure following above below'.split())


def fallback_highlights(pages):
    """Pick a couple of concise terms for original slides lacking manual highlights."""
    def words(text):
        return re.findall(r"[\w]+", re.sub(r'\*+', '', text).casefold())

    page_words = {p['n']: words(' '.join([p.get('title', '')] + p.get('body', []))) for p in pages}
    df = {}
    for terms in page_words.values():
        for token in set(terms):
            df[token] = df.get(token, 0) + 1
    total = max(1, len(pages))
    result = {}
    for p in pages:
        title = p.get('title', '')
        body = p.get('body', [])
        emphasized = []
        for text in [title] + body:
            emphasized.extend(re.findall(r'\*\*(.+?)\*\*', text))
        candidates = []
        for phrase in emphasized:
            candidates.extend(t for t in words(phrase)
                              if len(t) >= 4 and t not in _HIGHLIGHT_GENERIC | _HIGHLIGHT_STOP)
        terms = page_words[p['n']]
        scored = []
        for i, term in enumerate(terms):
            if len(term) < 4 or term in _HIGHLIGHT_STOP | _HIGHLIGHT_GENERIC:
                continue
            score = 1.0 + (total - df.get(term, 0)) / total + min(len(term), 12) * 0.02
            scored.append((score - i * 0.0005, term))
        for _, term in sorted(scored, reverse=True):
            if term not in candidates:
                candidates.append(term)
            if len(candidates) >= 2:
                break
        if not candidates:
            candidates = [title]
        result[p['n']] = candidates[:2]
    return result


def crop_figures(deck, mod, out_dir):
    pdf = deck_pdf(deck['key'])
    os.makedirs(out_dir, exist_ok=True)
    pages = read_pages(pdf)
    fallback_hl = fallback_highlights(pages)
    page_data = {p['n']: p for p in pages}
    pdf_word_pages = {}
    if getattr(mod, 'AUTO_SLIDES', False) == 'all':
        with pdfplumber.open(pdf) as source_pdf:
            pdf_word_pages = {i: (float(p.width), float(p.height), p.extract_words())
                              for i, p in enumerate(source_pdf.pages, 1)}
    dpi = 220
    k = dpi / 72
    cache_file = os.path.join(tempfile.gettempdir(), '%s-annotated-crops.json' % C.code.lower())
    try:
        with open(cache_file) as fh:
            cache = json.load(fh)
    except (OSError, ValueError):
        cache = {}
    for name, (page, box) in deck_crops(mod).items():
        target = os.path.join(out_dir, name.rsplit('.', 1)[0] + FIG_EXT)
        highlights = ((mod.ANN[page]['hl'] if 'hl' in mod.ANN.get(page, {}) else fallback_hl.get(page, ()))
                      if box == 'slide' else ())
        # Re-rendering every crop is slow; skip ones whose spec is unchanged since the last run.
        manual_boxes = mod.ANN.get(page, {}).get('hl_boxes', ()) if box == 'slide' else ()
        spec_parts = [pdf, os.path.getmtime(pdf), page, box, list(highlights)]
        spec_parts.append(list(manual_boxes))
        if manual_boxes:
            spec_parts.append('manual-highlight-box-v2')
        if box == 'slide':
            spec_parts.append('1200-jpeg-highlight-v5')
        spec = json.dumps(spec_parts)
        if os.path.exists(target) and cache.get(target) == spec:
            continue
        cache[target] = spec
        mode = box if isinstance(box, str) else None
        with tempfile.TemporaryDirectory() as tmp:
            stem = os.path.join(tmp, 'crop')
            if mode == 'slide':
                # A whole slide shown as an image: full page, sized for reading, not zooming.
                subprocess.run(['pdftoppm', '-scale-to-x', '1200', '-scale-to-y', '-1', '-f', str(page), '-l', str(page),
                                '-singlefile', '-png', pdf, stem], check=True, stderr=subprocess.DEVNULL)
            else:
                x0, y0, x1, y1 = auto_box(pdf, page, mode) if mode else box
                subprocess.run(['pdftoppm', '-r', str(dpi), '-f', str(page), '-l', str(page), '-singlefile', '-png',
                                '-x', str(int(x0 * k)), '-y', str(int(y0 * k)),
                                '-W', str(int((x1 - x0) * k)), '-H', str(int((y1 - y0) * k)), pdf, stem],
                               check=True, stderr=subprocess.DEVNULL)
            img = Image.open(stem + '.png').convert('RGB')
            if mode and mode != 'slide':
                img = trim(img)
            elif mode == 'slide' and (highlights or manual_boxes):
                page_w, page_h, words = pdf_word_pages.get(page, (float(img.width), float(img.height), []))
                scale_x, scale_y = img.width / page_w, img.height / page_h
                def tokens(value):
                    return re.findall(r"[\w]+", value.casefold())
                overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
                draw = ImageDraw.Draw(overlay)
                word_tokens = [tokens(w['text']) for w in words]
                marked = 0
                def draw_pdf_phrase(phrase):
                    nonlocal marked
                    wanted = tokens(phrase)
                    if not wanted:
                        return False
                    for start in range(len(words)):
                        combined = []
                        end = start
                        while end < len(words) and len(combined) < len(wanted):
                            if abs(float(words[end]['top']) - float(words[start]['top'])) > 3.5:
                                break
                            combined.extend(word_tokens[end])
                            end += 1
                        if combined[:len(wanted)] == wanted:
                            matched = words[start:end]
                            x0 = min(w['x0'] for w in matched) * scale_x - 2
                            y0 = min(w['top'] for w in matched) * scale_y - 1
                            x1 = max(w['x1'] for w in matched) * scale_x + 2
                            y1 = max(w['bottom'] for w in matched) * scale_y + 1
                            draw.rounded_rectangle((x0, y0, x1, y1), radius=4, fill=(255, 220, 55, 105))
                            marked += 1
                            return True
                    return False
                for phrase in highlights:
                    draw_pdf_phrase(phrase)
                # A few slides embed code as a raster image, so neither PDF text extraction
                # nor OCR can locate useful words. Allow a small, intentional highlight on
                # a known line in those cases, using normalized slide coordinates.
                for x0, y0, x1, y1 in manual_boxes:
                    draw.rounded_rectangle((x0 * img.width, y0 * img.height,
                                            x1 * img.width, y1 * img.height),
                                           radius=4, fill=(255, 220, 55, 105))
                    marked += 1
                if marked == 0:
                    # Some lecture PDFs store slide text as vector outlines or embedded images,
                    # so pdfplumber cannot locate the phrases. Use OCR boxes for those slides.
                    ocr = subprocess.run(['tesseract', stem + '.png', 'stdout', 'tsv'],
                                         check=False, capture_output=True, text=True).stdout
                    rows = [r for r in csv.DictReader(io.StringIO(ocr), delimiter='\t')
                            if r.get('level') == '5' and r.get('text', '').strip()]
                    rows = [r for r in rows if float(r.get('conf') or -1) >= 25]
                    title = page_data.get(page, {}).get('title', '')
                    body = ' '.join(page_data.get(page, {}).get('body', []))
                    notes = ' '.join(mod.ANN.get(page, {}).get('notes', []))
                    candidates = list(highlights)
                    candidates.extend(re.findall(r'\*\*(.+?)\*\*', ' '.join((title, body, notes))))
                    candidates.extend(t for t in re.findall(r'[A-Za-z][A-Za-z0-9-]*', title)
                                      if len(t) >= 4 and t.casefold() not in _HIGHLIGHT_GENERIC | _HIGHLIGHT_STOP)
                    ocr_tokens = [tokens(r['text']) for r in rows]
                    for phrase in candidates:
                        wanted = tokens(phrase)
                        if not wanted:
                            continue
                        for start in range(len(rows)):
                            combined = []
                            end = start
                            while end < len(rows) and len(combined) < len(wanted):
                                combined.extend(ocr_tokens[end])
                                end += 1
                            if combined[:len(wanted)] == wanted:
                                matched = rows[start:end]
                                x0 = min(int(r['left']) for r in matched) - 2
                                y0 = min(int(r['top']) for r in matched) - 1
                                x1 = max(int(r['left']) + int(r['width']) for r in matched) + 2
                                y1 = max(int(r['top']) + int(r['height']) for r in matched) + 1
                                draw.rounded_rectangle((x0, y0, x1, y1), radius=4, fill=(255, 220, 55, 105))
                                marked += 1
                                break
                        if marked >= 2:
                            break
                    if marked == 0:
                        for row in sorted(rows, key=lambda r: (int(r['top']), -float(r['conf']))):
                            term = row['text'].strip()
                            if (len(term) < 5 or not re.search(r'[A-Za-z]', term)
                                    or term.casefold() in _HIGHLIGHT_STOP | _HIGHLIGHT_GENERIC):
                                continue
                            x0, y0 = int(row['left']) - 2, int(row['top']) - 1
                            x1, y1 = x0 + int(row['width']) + 4, y0 + int(row['height']) + 2
                            draw.rounded_rectangle((x0, y0, x1, y1), radius=4, fill=(255, 220, 55, 105))
                            marked += 1
                            if marked >= 2:
                                break
                img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
            img.save(target, 'JPEG', quality=80 if mode == 'slide' else 88, optimize=True, progressive=True)
    # Figures used to be WebP, which Preview and most editors can't edit in place; drop the old copies.
    for old in glob.glob(os.path.join(out_dir, '*.webp')):
        os.remove(old)
    with open(cache_file, 'w') as fh:
        json.dump(cache, fh)


def figure_html(fig, slug):
    name, alt, cap = fig[:3]
    big = len(fig) > 3 and fig[3]
    src = 'figures/' + name.rsplit('.', 1)[0] + FIG_EXT
    path = os.path.join(C.dir, 'annotated-slides', slug, src)
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
    slug, file_, _, _ = C.decks[key]
    if key in C.built_keys:
        return '../%s/%s.html%s' % (slug, file_, '#slide-%d' % n if n else ''), False
    return C.base + deck_folder(key) + '/', True


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
    stamp = '<div class="stamp">%s</div>' % C.papers['stamp'] if direct else ''
    if kind == 'image':
        # The original slide shown as it is (AUTO_SLIDES): the picture is the whole slide.
        src = 'figures/' + s['fig'][0].rsplit('.', 1)[0] + FIG_EXT
        w, h = Image.open(os.path.join(C.dir, 'annotated-slides', slug, src)).size
        slide_html = ('<div class="slide image">%s<img src="%s" alt="Slide %d: %s" width="%d" height="%d" loading="lazy" decoding="async"></div>'
                      % (stamp, src, n, e(s['fig'][1]), w, h))
    else:
        slide_html = '<div class="slide %s">%s<div class="slide-inner">%s%s%s</div></div>' % (kind, stamp, head, body, foot)
    prof = ''.join('<p class="prof-note">%s</p>' % rich(p) for p in s['prof'])

    margin = ''
    if s['notes'] or kind in ('content', 'image'):
        label, dots = WEIGHT[s['weight']]
        notes = ''.join('<li data-n="%d">%s</li>' % (i, rich(t)) for i, t in enumerate(s['notes'], 1))
        margin = ('<div class="margin" role="note" aria-label="Notes for slide %d"><div class="weight" title="How likely this slide is to be examined">'
                  'Exam weight <span class="dots" aria-hidden="true">%s</span> %s</div><ol>%s</ol></div>'
                  % (n, dots, label, notes))

    extras = []
    if s['tips']:
        names = {'tip': 'Tip', 'trick': 'Memory trick', 'trap': 'Exam trap'}
        extras.append('<div class="stickies">%s</div>' % ''.join(
            '<div class="sticky %s"><b>%s</b>%s</div>' % (k, names[k], rich(t)) for k, t in s['tips']))
    if s['past']:
        links = []
        for p in s['past']:
            title, folder = C.paper_list[p['paper']]
            href = C.base + C.papers['folder'] + folder + ('' if folder.endswith('.html') else '/')
            links.append('<a class="%s" href="%s" target="_top">%s%s · %s</a>' % (
                'rel' if p['related'] else 'dir', href, '' if p['related'] else '★ ', e(title), e(p['label'])))
        label = C.papers['direct'] if direct else C.papers['related']
        extras.append('<div class="past"><p class="row-label">%s</p><div class="links">%s</div></div>' % (label, ''.join(links)))
    if s['seen']:
        links = []
        for ref in s['seen']:
            if ref['deck'] == deck['key']:
                href, external = '#s-%d' % ref['n'], False
            else:
                href, external = deck_url(ref['deck'], ref['n'])
            chapter = C.decks[ref['deck']][3].split(' · ')[0]
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
                               % (int(j == q['a']), e(q['opts'][j])) for j in option_order(q))
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


def option_order(q):
    """MCQ options in a stable shuffled order, so the answer isn't always where the author typed it.
    Catch-all options ("All of the above", "Both ...") stay last."""
    def key(j):
        o = q['opts'][j]
        last = re.match(r'(All|None|Both|Neither) (of|the|[a-z])', o) is not None
        return (last, hashlib.md5((q['q'] + '|' + o).encode('utf-8')).hexdigest())
    return sorted(range(len(q['opts'])), key=key)


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
    make = importlib.import_module(C.package + '.common').slide
    pages = read_pages(deck_pdf(mod.DECK['key']))
    out = []
    for p in pages:
        ann = mod.ANN.get(p['n'], {})
        if ann.get('skip'):
            continue
        auto = auto_figure(mod, p, ann)
        if auto:
            ann = dict(ann, fig=(auto[0], ann.get('alt', p['title'] or 'Slide %d' % p['n']), ''))
            if auto[1] == 'slide':
                # No text to mark up on an image slide.
                ann = {k: v for k, v in ann.items() if k not in MARK_WRAP and k != 'refs'}
                ann['drop_body'], ann['kind'] = True, 'image'
        kind = ann.get('kind', p['kind'])
        body = ann['body'] if 'body' in ann else ([] if ann.get('drop_body') else p['body'])
        for bad, good in list(getattr(mod, 'FIX', {}).items()) + list(ann.get('fix', {}).items()):
            body = [line.replace(bad, good) for line in body]
        body = [line for line in body if line.strip('*- ') not in ann.get('drop_lines', ())]
        cols = ann.get('cols')
        if cols and 'body' not in ann:
            # Columns replace the PDF text, so the marks go on the column lines instead.
            marked = overlay([line for col in cols for line in col], ann, p['n'])
            cols, i = [], 0
            for col in ann['cols']:
                cols.append(marked[i:i + len(col)])
                i += len(col)
        elif 'body' not in ann:
            body = overlay(body, ann, p['n'])
        elif ann.get('refs') or any(k in ann for k in MARK_WRAP):
            body = overlay(body, ann, p['n'])
        weight = ann.get('weight', 2 if ann.get('exam') or ann.get('past') else 1)
        out.append(make(p['n'], ann.get('title', p['title']), body, kind=kind, sub=ann.get('sub'), cols=cols,
                        card=ann.get('card'), fig=ann.get('fig'), chart=ann.get('chart'), notes=ann.get('notes', ()),
                        prof=ann.get('prof', ()), tips=ann.get('tips', ()), seen=ann.get('seen', ()),
                        exam=ann.get('exam', ()), past=ann.get('past', ()), weight=weight))
    return out


# --------------------------------------------------------------------------- #
# the deck page in the linked-notes format (annotated_page.py)
# --------------------------------------------------------------------------- #

WRAPPED = re.compile(r'\{\((.+?)\)\}|\{\{(.+?)\}\}|==(.+?)==|__(.+?)__|\(\((.+?)\)\)')
NOTE_REF = re.compile(r'\^(\d+)(?![\d.])')


def unmark(text):
    """Engine markup -> the page's: marks and note anchors dropped, **bold** kept."""
    out = text
    while WRAPPED.search(out):
        out = WRAPPED.sub(lambda m: next(g for g in m.groups() if g is not None), out)
    out = NOTE_REF.sub('', out).replace('***', '**')
    return out


def _key(t):
    return re.sub(r'[^0-9a-z]+', '', t.lower())


def slide_marks(s):
    """(phrase, note number or None) for every mark and note anchor in a slide's text."""
    lines = list(s['body'])
    for col in s['cols'] or ():
        lines += col
    if s['card']:
        lines += [s['card'][1]] + [p for p in s['card'][2]]
    out = []
    for line in lines:
        for line in line.split('\n'):
            line = re.sub(r'^(-{1,4}|#{1,2}) ', '', line).replace('*', '')
            for m in WRAPPED.finditer(line):
                ref = NOTE_REF.match(line, m.end())
                out.append((unmark(m.group(0)), int(ref.group(1)) if ref else None))
            # bare anchors ("Project Managers^3"): the words just before the anchor
            start = 0
            for m in NOTE_REF.finditer(line):
                before = line[start:m.start()]
                start = m.end()
                if WRAPPED.search(before[-200:]) and re.search(r'(==|__|\}\}|\)\}|\)\))$', before):
                    continue  # already taken with its mark
                words = unmark(before).strip(' .,:;–-').split()[-8:]
                if words:
                    out.append((' '.join(words), int(m.group(1))))
    return out


def note_for(phrase, notes):
    """The first note that mentions phrase, or 0."""
    k = _key(phrase)
    if len(k) < 3:
        return 0
    for i, t in enumerate(notes, 1):
        if k in _key(t):
            return i
    return 0


def exam_items(s):
    """Past-paper pointers first, then the practice questions (a question whose explanation names a real paper is tagged past)."""
    out = []
    for p in s['past']:
        title, folder = C.paper_list[p['paper']]
        href = C.base + C.papers['folder'] + folder + ('' if folder.endswith('.html') else '/')
        out.append({'kind': 'past', 'ref': title, 'href': href, 'label': ('Related question: ' if p['related'] else '') + p['label']})
    titles = [t for t, _ in C.paper_list.values()]
    for q in s['exam']:
        named = [t for t in titles if t in (q.get('why') or '')]
        item = {'kind': 'past' if named else 'predict', 'ref': ' · '.join(named), 'q': unmark(q['q']), 'why': unmark(q.get('why') or '')}
        if q['type'] == 'mcq':
            order = option_order(q)
            item.update(opts=[unmark(q['opts'][j]) for j in order], a=order.index(q['a']))
        elif q['type'] == 'tf':
            item.update(tf=bool(q['a']))
        else:
            item.update(a=unmark(q['a']), why='')
        out.append(item)
    return out


def page_slides(deck, mod):
    """deck_slides() in the page schema: numbered notes with the slide's marks linked to them."""
    out = {}
    for s in deck_slides(mod):
        texts = [unmark(t) for t in s['notes']]
        notes = list(texts)
        notes += [{'text': unmark(t), 'kind': 'prof'} for t in s['prof']]
        notes += [{'text': unmark(t), 'kind': k} for k, t in s['tips']]
        for ref in s['seen']:
            if ref['deck'] == deck['key']:
                href, where = '#slide-%d' % ref['n'], 'this deck'
            else:
                href, _ = deck_url(ref['deck'], ref['n'])
                where = C.decks[ref['deck']][3].split(' · ')[0]
            notes.append({'text': '[%s, slide %d](%s): %s' % (where[0].upper() + where[1:], ref['n'], href, unmark(ref['label'])), 'kind': 'seen'})
        all_text = [n if isinstance(n, str) else n['text'] for n in notes]
        hl, seen = [], set()
        for phrase, ref in slide_marks(s):
            note = ref if ref and ref <= len(notes) else note_for(phrase, all_text)
            if (phrase, note) not in seen:
                seen.add((phrase, note))
                hl.append((phrase, note))
        have = {_key(p) for p, _ in hl}
        for i, t in enumerate(all_text, 1):  # bold terms in a note, found on the slide, point to that note
            for term in re.findall(r'\*\*(.+?)\*\*', t):
                if 3 <= len(_key(term)) and len(term) <= 40 and _key(term) not in have:
                    have.add(_key(term))
                    hl.append((term, i, 0, True))
        out[s['n']] = {'notes': notes, 'hl': hl, 'exam': exam_items(s), 'title': unmark(s['title'])}
    return out


def build_page(deck, mod, out):
    """Write the deck page (and figures) with annotated_page; decks rewritten in the page schema name it in DECK['page']."""
    import annotated_page
    url = SITE + C.section + deck['slug'] + '/'
    spec = dict(out_dir=out, file=deck['file'], url=url, key='%s-%s' % (C.code.lower(), deck['slug']),
                chapter='%s · %s' % (C.code, deck['chapter']), title=deck['title'], lede=deck['lede'],
                original=deck['pdf'],
                footer='Original slides from the %s lecture deck, with study notes. Check exact wording against the '
                       '[original deck](%s). Notes and questions are study aids. Made by Shoug Alomran.' % (C.code, deck['pdf']))
    if deck.get('page'):
        page = importlib.import_module('%s.%s' % (C.package, deck['page']))
        spec.update(src=os.path.join(REPO, deck['src']) if deck.get('src') else deck_pdf(deck['key']),
                    title=page.TITLE, chapter=page.CHAPTER, overview=page.OVERVIEW, slides=page.SLIDES,
                    titles=getattr(page, 'TITLES', {}), strict=True, pdf='--no-pdf' not in sys.argv,
                    width=deck.get('width', annotated_page.WIDTH))
        spec['footer'] = getattr(page, 'FOOTER', spec['footer'])
    else:
        slides = page_slides(deck, mod)
        summary = '\n\n'.join(p for p in (getattr(mod, 'OVERVIEW', ''), deck['lede']) if p)
        spec.update(src=deck_pdf(deck['key']), slides=slides, overview={'summary': summary},
                    titles={n: sd['title'] for n, sd in slides.items() if sd['title']})
    spec['head_title'] = '%s · %s · Annotated Slides' % (C.code, deck['chapter'])
    spec['description'] = ('%s %s annotated slides: every original slide with numbered study notes linked to the highlighted '
                           'words, past-exam links and practice questions.' % (C.code, deck['chapter']))
    report = annotated_page.build(spec)
    print('  %s: %d slides, %d highlights%s' % (deck['slug'], report['slides'], report['highlights'],
                                                ', %d marks not found on the slide' % len(report['missing']) if report['missing'] else ''))
    return report


def deck_page(deck, mod):
    slides = deck_slides(mod)
    n_q = sum(len(s['exam']) for s in slides)
    n_past = sum(1 for s in slides if any(not p['related'] for p in s['past']))
    n_rel = sum(1 for s in slides if s['past']) - n_past
    title = '%s — %s' % (deck['chapter'], deck['title'])
    overview_title = deck['chapter'].split(' · ')[0] + ' overview'
    overview = getattr(mod, 'OVERVIEW', '')
    overview_html = ('<div class="chapter-overview"><div class="overview-heading"><h2>%s</h2>'
                     '<button type="button" class="chip-btn" id="as-overview" aria-pressed="true">▤ Overview on</button>'
                     '</div><p class="overview-content">%s</p></div>' % (e(overview_title), e(overview))) if overview else ''
    options = ''.join('<option value="s-%d">%d · %s</option>' % (s['n'], s['n'], e(s['title'])) for s in slides)
    sheets = ''.join(render_slide(deck, s, mod) for s in slides)
    rendering = 'original slides' if getattr(mod, 'AUTO_SLIDES', False) == 'all' else 'rebuilt slides'
    desc = C.code + ' %s annotated slides: %s with notes, memory tricks, cross-references and likely exam questions.' % (title, rendering)
    return '''<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{code} · Annotated Slides · {title}</title>
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
<div class="as-brand"><small>{code} · Annotated Slides</small><strong>{title}</strong></div>
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
{overview}
<ul class="as-stats"><li><b>{count}</b> slides</li><li><b>{n_past}</b> {w_direct}</li><li><b>{n_rel}</b> {w_related}</li><li><b>{n_q}</b> practice questions</li></ul>
<div class="legend" aria-label="Ink key">
<span><i class="lg-ink"></i>Slide text</span>
{prof_legend}<span><i class="lg-red"></i>Study notes</span>
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
<footer class="as-foot">{display} from the {code} lecture slides, with study notes. Check exact wording against the <a href="{pdf}" target="_top">original deck</a>. Made by Shoug Alomran.</footer>
</div>
<nav class="flipbar" aria-label="Slide navigation"><button type="button" id="flip-prev" aria-label="Previous slide">◀ Prev</button><div class="flip-pos"><span id="flip-text">Slide 1</span><span class="track"><span class="fill" id="flip-fill"></span></span></div><button type="button" id="flip-next" aria-label="Next slide">Next ▶</button></nav>
<script src="/javascripts/annotated-slides.js"></script>
</body>
</html>
'''.format(code=C.code, w_direct=C.papers['n_direct'], w_related=C.papers['n_related'], overview=overview_html,
           display='Original slides' if getattr(mod, 'AUTO_SLIDES', False) == 'all' else 'Rebuilt slides',
           prof_legend='<span><i class="lg-prof"></i>Instructor’s marks (from the original PDF)</span>\n' if C.prof_legend else '',
           title=e(title), desc=e(desc), site=SITE, section=C.section, slug=deck['slug'], options=options,
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
    entry = {'url': C.section, 'attrs': 'data-en-text="ANNOTATED SLIDES" data-ar-text="%s"' % AR_LABEL,
             'label': 'ANNOTATED SLIDES'}
    sections = data['sections'][C.base]
    sections[:] = [s for s in sections if s['url'] != C.section]
    at = next(i for i, s in enumerate(sections) if s['url'] == C.base + C.after[0]) + 1
    sections.insert(at, entry)
    data['children'][C.section] = [{'url': C.section + C.decks[k][0] + '/', 'attrs': '', 'label': C.item_label(C.decks[k][3])}
                                   for k in C.decks if k in C.built_keys]
    with open(sidebar.DATA_FILE, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write('\n')
    return data


def section_block_span(page):
    """(start, end) of the course's section list inside the sidebar."""
    course = re.search(r'href="%s"\s*>(?:<span class="status-dot"></span>)?\s*%s</a' % (re.escape(C.base), C.code), page)
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
    return page[:span[0]] + sidebar.render_sections(data, C.base, url) + page[span[1]:]


def add_tab(page, active=False):
    if 'href="%s" class="tab' % C.section in page or re.search(r'href="%s"\s+class="tab' % re.escape(C.section), page):
        return page
    m = re.search(r'(?P<indent>[ \t]*)<a\s+href="%s"\s+class="tab(?: active)?"[^>]*>\s*%s</a\s*>'
                  % (re.escape(C.base + C.after[0]), re.escape(C.after[1])), page)
    if not m:
        return page
    ind = m.group('indent')
    tab = ('\n%s<a\n%s  href="%s"\n%s  class="tab%s"\n%s  data-en-text="Annotated Slides"\n%s  data-ar-text="%s"\n%s  >Annotated Slides</a\n%s>'
           % (ind, ind, C.section, ind, ' active' if active else '', ind, ind, AR_LABEL, ind, ind))
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
    donor = None
    if len(C.template) == 3:
        # The course has no slide breakdowns: borrow another course's wrapper (same track) and
        # rewrite its course references; the whole sidebar is re-rendered below.
        donor, folder, template_file = C.template
        page = read(os.path.join(REPO, 'docs', 'academics', donor, 'slide-breakdowns', folder, 'index.html'))
        donor_code = donor.rsplit('/', 1)[1].upper()
        page = page.replace('/academics/%s/' % donor, C.base)
        page = re.sub(r'\b%s\b' % donor_code, C.code, page)
    else:
        folder, template_file = C.template
        page = read(os.path.join(C.dir, 'slide-breakdowns', folder, 'index.html'))
    url = C.section + deck['slug'] + '/'
    name = C.page_name(deck)
    title = '%s | %s (Annotated Slides)' % (C.code, e(name))
    desc = C.code + ' %s annotated slides: every original slide with numbered study notes linked to the highlighted words, past-exam links and practice questions.' % e(name)
    page = replace_meta(page, title, desc, C.base + 'slide-breakdowns/%s/' % folder, url)

    def crumb(m):
        sep = '\n            <span class="separator">/</span>\n            ' if 'separator' in m.group(1) else '\n            /'
        return 'href="%s"\n              >Annotated Slides</a\n            >%s<span class="current">%s</span>' % (C.section, sep, e(name))

    def body(part):
        part = re.sub(r'href="%sslide-breakdowns/"\s*>Slide Breakdowns</a\s*>(\s*/|\s*<span class="separator">/</span>)\s*<span class="current"\s*>.*?</span\s*>'
                      % re.escape(C.base), crumb, part, flags=re.S)
        part = re.sub(r'(<div class="ch-label[^"]*">).*?(</div>)',
                      lambda m: '%sITEM_%02d // ANNOTATED SLIDES%s' % (m.group(1), list(C.decks).index(key) + 1, m.group(2)), part, count=1, flags=re.S)
        part = re.sub(r'(<h1 class="ch-title[^"]*">).*?(</h1>)', lambda m: m.group(1) + e(name) + m.group(2), part, flags=re.S)
        part = part.replace('href="./%s.html"' % template_file, 'href="./%s.html"' % deck['file'])
        part = part.replace('src="./%s.html"' % template_file, 'src="./%s.html"' % deck['file'])
        part = part.replace('href="%sslide-breakdowns/"' % C.base, 'href="%s"' % C.section)
        part = part.replace('title="Slide breakdown"', 'title="Annotated slides"')

        def nav_link(k, cls, text):
            if not k:
                return '<span class="nav-link %s disabled">%s</span>' % (cls, text)
            return '<a\n            href="%s%s/"\n            class="nav-link %s"\n            >%s</a\n          >' % (C.section, C.decks[k][0], cls, text)
        part = re.sub(r'(<div class="nav-strip[^"]*">).*?</div>',
                      lambda m: '%s\n          %s\n          %s\n        </div>' % (
                          m.group(1), nav_link(prev_key, 'prev', '&lt;- PREVIOUS'), nav_link(next_key, 'next', 'NEXT -&gt;')),
                      part, count=1, flags=re.S)
        return part
    page = outside_nav(page, body)
    if donor:
        page = sidebar.NAV_RE.sub(lambda m: sidebar.render_nav(data, url), page, count=1)
    else:
        page = set_sections(page, data, url)
    write(os.path.join(C.dir, 'annotated-slides', deck['slug'], 'index.html'), page)


def build_directory(data):
    page = read(os.path.join(C.dir, 'slides', 'index.html'))
    title = 'SHOUG.TECH | %s Annotated Slides' % C.code
    desc = ('%s %s annotated slides: every original lecture slide with linked study notes, '
            'memory tricks, cross-references, %s links and likely exam questions.' % (C.code, C.name, C.papers['desc']))
    page = replace_meta(page, title, desc, C.base + 'slides/', C.section)

    def body(part):
        part = re.sub(r'<span class="current" data-en-text="Slides" data-ar-text="الشرائح"\s*>Slides</span\s*>',
                      '<span class="current" data-en-text="Annotated Slides" data-ar-text="%s">Annotated Slides</span>' % AR_LABEL, part)
        part = re.sub(r'<div class="type-label" data-en-text="SLIDES" data-ar-text="الشرائح">\s*SLIDES\s*</div>',
                      '<div class="type-label" data-en-text="ANNOTATED SLIDES" data-ar-text="%s">ANNOTATED SLIDES</div>' % AR_LABEL, part)
        part = re.sub(r'(<a\s+href="%sslides/"\s+class=")tab active(")' % re.escape(C.base), r'\1tab\2', part)
        part = add_tab(part, active=True)
        rows = []
        arrow = ('<div class="dir-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
                 'stroke-linecap="square"><path d="M5 12h14M12 5l7 7-7 7" /></svg></div>')
        for i, (k, (slug, _, _, label)) in enumerate(C.decks.items(), 1):
            text = C.item_label(label)
            if k in C.built_keys:
                rows.append('<a href="%s%s/" class="dir-row"><div class="dir-num">%02d</div><div class="dir-title">%s</div>'
                            '<div class="dir-status"><span class="status-tag available">AVAILABLE</span></div>%s</a>'
                            % (C.section, slug, i, e(text), arrow))
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
    page = set_sections(page, data, C.section)
    write(os.path.join(C.dir, 'annotated-slides', 'index.html'), page)


def add_section_li(page):
    """Insert the ANNOTATED SLIDES entry after the `after` section (and its open item list), in the page's own formatting."""
    span = section_block_span(page)
    if not span or 'href="%s"' % C.section in page[span[0]:span[1]]:
        return page
    m = re.compile(r'(?P<indent>[ \t]*)<li class="tree-item tree-section[^"]*">\s*<a\s+class="tree-file"\s+href="%s".*?</li>'
                   % re.escape(C.base + C.after[0]), re.S).search(page, span[0], span[1])
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
              % (ind, ind, ind, ind, C.section, ind, ind, AR_LABEL, ind, ind, ind))
    else:
        li = sidebar.link(C.section, 'ANNOTATED SLIDES', attrs, classes='tree-item tree-section')
    return page[:at] + li + page[at:]


def wire_course_pages():
    """Add the tab and the sidebar entry to every other page of the course."""
    skip = os.path.join(C.dir, 'annotated-slides')
    changed = 0
    for dirpath, _, files in os.walk(C.dir):
        if dirpath.startswith(skip) or 'index.html' not in files:
            continue
        path = os.path.join(dirpath, 'index.html')
        page = read(path)
        new = add_section_li(add_tab(page))
        if new != page:
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write(new)
            changed += 1
    print('wired %d existing %s page(s)' % (changed, C.code))


# --------------------------------------------------------------------------- #

def load_deck(name):
    """A deck module, or 'module:Name' for one of several short decks kept in a single module."""
    module, _, attr = name.partition(':')
    mod = importlib.import_module('%s.%s' % (C.package, module))
    return getattr(mod, attr) if attr else mod


def build(course):
    global C
    C = course
    mods = [load_deck(name) for name in C.built]
    C.built_keys = {m.DECK['key'] for m in mods}
    data = update_sidebar_data()
    keys = [k for k in C.decks if k in C.built_keys]
    # --deck KEY (repeatable) rebuilds only those decks' pages and wrappers.
    only = {sys.argv[i + 1] for i, a in enumerate(sys.argv[:-1]) if a == '--deck'}
    for mod in mods:
        deck = mod.DECK
        out = os.path.join(C.dir, 'annotated-slides', deck['slug'])
        if only and deck['key'] not in only:
            continue
        build_page(deck, mod, out)
        i = keys.index(deck['key'])
        build_wrapper(deck, data, keys[i - 1] if i > 0 else None, keys[i + 1] if i + 1 < len(keys) else None)
    build_directory(data)
    wire_course_pages()

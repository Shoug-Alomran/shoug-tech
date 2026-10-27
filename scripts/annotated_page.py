"""Render an annotated-slides deck page: the original slides as images, numbered notes beside each one,
highlights linked to their notes, exam questions, an overview, and an optional PDF export.

Used by annotated_slides.build() for every deck (content converted from the deck module, or written in
the page schema directly, e.g. se322_annotated/ch05_2_page.py).

Content schema (one dict per slide number):
  notes  list of notes: a string, or {'text', optional 'code': [(line, explanation)], 'items': [(term, meaning)], 'pre': str,
         'kind': 'trap'|'trick'|'tip'|'seen'}
  hl     [(phrase, note number[, occurrence])]: a highlight on the slide, linked to one note (0 = not linked)
  exam   [{'kind': 'past'|'predict', 'ref', 'q', 'a', optional 'opts' (MCQ, 'a' = index) or 'tf' (bool), 'why', 'href'}]
Markup inside text: **bold**, `code`, *italic*.

Slide images are untouched JPEGs; highlights are an SVG layer placed from the PDF's word boxes (Tesseract OCR
for slides that are pictures), so they never cover the image and can be switched off.
"""
import html
import os
import re
import subprocess
import tempfile

import pdfplumber
from PIL import Image

WIDTH = 1440      # rendered slide width (px)
QUALITY = 82      # JPEG quality


def e(s):
    return html.escape(str(s), quote=True)


def rich(s):
    s = e(s)
    s = re.sub(r'`([^`]+)`', lambda m: '<code>%s</code>' % m.group(1), s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![\w*])\*([^*\s][^*]*?)\*(?![\w*])', r'<em>\1</em>', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', lambda m: '<a href="%s"%s>%s</a>' % (
        m.group(2), '' if m.group(2).startswith(('#', '../')) else ' target="_top"', m.group(1)), s)
    return s


def norm(t):
    return re.sub(r'[^0-9a-z]+', '', t.lower())


def raw(t):
    return re.sub(r'\s+', '', t.lower())


# ---------------------------------------------------------------- slides and word boxes

def render(src, out_dir, width=WIDTH):
    """Write figures/slide-NN.jpg for every page (skipped when the PDF and settings are unchanged)."""
    figs = os.path.join(out_dir, 'figures')
    os.makedirs(figs, exist_ok=True)
    st = os.stat(src)
    stamp = '%s|%d|%d|%d|%d' % (os.path.basename(src), st.st_size, int(st.st_mtime), width, QUALITY)
    stamp_file = os.path.join(figs, '.render-stamp')
    with pdfplumber.open(src) as p:
        n_pages = len(p.pages)
    have = [f for f in os.listdir(figs) if re.match(r'slide-\d+\.jpg$', f)]
    if os.path.exists(stamp_file) and open(stamp_file).read() == stamp and len(have) == n_pages:
        return
    for f in os.listdir(figs):  # figures are generated: start clean
        os.remove(os.path.join(figs, f))
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(['pdftoppm', '-scale-to-x', str(width), '-scale-to-y', '-1', '-png', src, os.path.join(tmp, 's')], check=True)
        pngs = sorted((f for f in os.listdir(tmp) if f.startswith('s-')), key=lambda f: int(re.findall(r'\d+', f)[-1]))
        for i, f in enumerate(pngs, 1):
            Image.open(os.path.join(tmp, f)).convert('RGB').save(
                os.path.join(figs, 'slide-%02d.jpg' % i), 'JPEG', quality=QUALITY, optimize=True, progressive=True)
    with open(stamp_file, 'w') as fh:
        fh.write(stamp)


CID = re.compile(r'\(cid:(\d+)\)')


def uncid(t):
    """Fonts without a ToUnicode map come out as (cid:N); in these decks N is the Unicode code point."""
    return CID.sub(lambda m: chr(int(m.group(1))), t)


def pdf_words(pdf):
    out = []
    for pg in pdf.pages:
        W, H = float(pg.width), float(pg.height)
        ws = []
        for w in pg.extract_words(keep_blank_chars=False, use_text_flow=True, return_chars=True):
            if w['top'] / H > 0.92:  # footer
                continue
            chars = [(uncid(c['text']), c['x0'] / W, c['x1'] / W) for c in w['chars']]
            # a decoded (cid:32) is a space the word splitter could not see: split there
            run = []
            for c in chars + [(' ', 0, 0)]:
                if c[0].isspace():
                    if run:
                        ws.append(dict(t=''.join(x[0] for x in run), x0=run[0][1], x1=run[-1][2],
                                       y0=w['top'] / H, y1=w['bottom'] / H, chars=run))
                    run = []
                else:
                    run.append(c)
        out.append(ws)
    return out


def ocr_words(src, n):
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(['pdftoppm', '-f', str(n), '-l', str(n), '-scale-to-x', '1920', '-scale-to-y', '-1', '-png',
                        src, os.path.join(tmp, 'p')], check=True)
        png = os.path.join(tmp, sorted(os.listdir(tmp))[0])
        tsv = subprocess.run(['tesseract', png, '-', '--psm', '11', 'tsv'], capture_output=True, text=True).stdout
        W, H = Image.open(png).size
    out = []
    for row in tsv.splitlines()[1:]:
        c = row.split('\t')
        if len(c) < 12 or not c[11].strip() or float(c[10]) < 30:
            continue
        x, y, w, h = map(int, c[6:10])
        out.append(dict(t=c[11], x0=x / W, x1=(x + w) / W, y0=y / H, y1=(y + h) / H))
    out.sort(key=lambda w: (round(w['y0'] * 60), w['x0']))
    return out


def find(words, phrase, occ=0):
    """Boxes (one per text line) for the occ-th occurrence of phrase, or None.

    Tries an exact match first (symbols kept, so "<<interface>>" doesn't match "(Interface)"),
    then a letters-and-digits-only match. The first and last word boxes are trimmed to the phrase
    using the character boxes (bullet glyphs like ➢ and ✓ are wider than letters)."""
    for key in (raw, norm):
        target = key(phrase)
        if not target:
            return None
        toks = [key(w['t']) for w in words]
        hits = []
        for i in range(len(words)):
            first = toks[i]
            if not first:
                continue
            # where the phrase starts inside this token: the rest of the token contains it or begins it
            k = next((k for k in range(len(first)) if first.startswith(target, k) or target.startswith(first[k:])), -1)
            if k < 0:
                continue
            acc, j = first[k:], i
            while len(acc) < len(target) and j + 1 < len(words):
                j += 1
                acc += toks[j]
            if acc.startswith(target):
                hits.append((i, j, k, len(acc) - len(target)))
        if len(hits) > occ:
            break
    else:
        return None
    i, j, lead, tail = hits[occ]
    sel = [dict(w) for w in words[i:j + 1]]

    def shrink(w, before, after):
        kept = [c for c in w.get('chars', ()) if key(c[0])]
        if kept and len(kept) == len(key(w['t'])):
            w['x0'] = kept[before][1]
            w['x1'] = kept[len(kept) - 1 - after][2]
            return
        n = max(1, len(key(w['t'])))
        span = w['x1'] - w['x0']
        w['x0'] += span * before / n
        w['x1'] -= span * after / n
    if i == j:
        shrink(sel[0], lead, tail)
    else:
        shrink(sel[0], lead, 0)
        shrink(sel[-1], 0, tail)
    lines = []
    for w in sel:
        for ln in lines:
            if abs(ln['y0'] - w['y0']) < 0.5 * (w['y1'] - w['y0']):
                ln.update(x0=min(ln['x0'], w['x0']), x1=max(ln['x1'], w['x1']), y0=min(ln['y0'], w['y0']), y1=max(ln['y1'], w['y1']))
                break
        else:
            lines.append(dict(w))
    return lines


def slide_title(pdf, n):
    pg = pdf.pages[n - 1]
    lines = {}
    for w in pg.extract_words(extra_attrs=['size']):
        if w['top'] / float(pg.height) > 0.3:
            continue
        lines.setdefault(round(w['top']), []).append(w)
    if not lines:
        return ''
    best = max(lines.values(), key=lambda ws: max(w['size'] for w in ws))
    t = ' '.join(w['text'] for w in sorted(best, key=lambda w: w['x0']))
    t = re.sub(r'^[➢✓•\s]+', '', t).strip()
    return t if len(t) > 2 else ''


# ---------------------------------------------------------------- HTML

KIND_LABEL = {'trap': 'Trap', 'trick': 'Memory trick', 'tip': 'Tip', 'seen': 'Seen again', 'prof': 'Instructor'}


def note_html(n, i, note):
    if isinstance(note, str):
        note = {'text': note}
    parts = ['<p>%s</p>' % rich(note['text'])] if note.get('text') else []
    if note.get('code'):
        rows = ''.join('<tr><td class="src"><code>%s</code></td><td>%s</td></tr>' % (e(src), rich(ex)) for src, ex in note['code'])
        parts.append('<table class="walk"><thead><tr><th>Code</th><th>What it does</th></tr></thead><tbody>%s</tbody></table>' % rows)
    if note.get('items'):
        parts.append('<dl class="reading">%s</dl>' % ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (rich(a), rich(b)) for a, b in note['items']))
    if note.get('pre'):
        parts.append('<pre>%s</pre>' % e(note['pre']))
    kind = note.get('kind')
    if kind in KIND_LABEL and parts and parts[0].startswith('<p>'):
        parts[0] = '<p><span class="kind %s">%s</span> ' % (kind, KIND_LABEL[kind]) + parts[0][3:]
    return '<li id="n%d-%d" data-n="%d"><span class="num" aria-hidden="true">%d</span><div class="body">%s</div></li>' % (
        n, i, i, i, ''.join(parts))


def answer_html(q):
    why = rich(q['why']) if q.get('why') else ''
    if q.get('opts') is not None:
        a = q['a']
        return '<strong>%s. %s</strong>%s' % ('ABCDEFG'[a], rich(q['opts'][a]), (' — ' + why) if why else '')
    if q.get('tf') is not None:
        return '<strong>%s</strong>%s' % ('True' if q['tf'] else 'False', (' — ' + why) if why else '')
    return rich(q.get('a', '')) + ((' ' + why) if why else '')


def exam_html(n, exams):
    if not exams:
        return ''
    cards, k = [], 0
    for q in exams:
        past = q['kind'] == 'past'
        ref = e(q.get('ref', ''))
        if q.get('href'):
            ref = '<a href="%s" target="_top">%s</a>' % (e(q['href']), ref)
        tag = ('<span class="tag past">Past exam · %s</span>' % ref) if past else '<span class="tag predict">Prediction</span>'
        if not q.get('q'):  # a past-paper pointer without the question text
            cards.append('<article class="q past ptr"><header>%s</header><p>%s</p></article>' % (tag, rich(q.get('label', ''))))
            continue
        k += 1
        opts = ''
        if q.get('opts') is not None:
            opts = '<ol class="opts" type="A">%s</ol>' % ''.join('<li>%s</li>' % rich(o) for o in q['opts'])
        cards.append('<article class="q %s"><header>%s<span class="qn">Q%d</span></header><p>%s</p>%s'
                     '<details><summary>Show answer</summary><p>%s</p></details></article>' % (
                         'past' if past else 'predict', tag, k, rich(q['q']), opts, answer_html(q)))
    return '<section class="exam" aria-label="Exam practice for slide %d"><h4>Exam angle</h4>%s</section>' % (n, ''.join(cards))


def slide_html(n, total, title, sd, rects, size):
    W, H = size
    svg = ''.join('<rect class="hl%s" data-n="%d" x="%.4f" y="%.4f" width="%.4f" height="%.4f" rx="0.004"><title>%s</title></rect>' % (
        '' if note else ' free', note, x0, y0 * H / W, x1 - x0, (y1 - y0) * H / W, ('Note %d' % note) if note else 'Key term')
        for note, (x0, y0, x1, y1) in rects)
    notes = ''.join(note_html(n, i, nt) for i, nt in enumerate(sd.get('notes', ()), 1))
    exam = exam_html(n, sd.get('exam'))
    has_notes = bool(notes or exam)
    side = ('<div class="notes" id="notes-%d">%s%s</div>' % (n, ('<h4>Notes</h4><ol>%s</ol>' % notes) if notes else '', exam)) if has_notes else ''
    toggle = ('<button type="button" class="note-toggle" aria-expanded="true" aria-controls="notes-%d">Hide notes</button>' % n) if has_notes else ''
    return '''
<section class="card%(bare)s" id="slide-%(n)d" data-slide="%(n)d">
  <header class="card-head"><span class="sn">Slide %(n)d <span>/ %(total)d</span></span><h3>%(title)s</h3>%(toggle)s</header>
  <div class="row">
    <figure class="slide"><img src="figures/slide-%(n)02d.jpg" width="%(W)d" height="%(H)d" alt="Slide %(n)d: %(alt)s" loading="%(loading)s" decoding="async">
      <svg class="hl-layer" viewBox="0 0 1 %(ratio).5f" preserveAspectRatio="none" aria-hidden="true">%(svg)s</svg></figure>
    %(side)s
  </div>
</section>''' % dict(n=n, total=total, title=e(title), W=W, H=H, alt=e(title), svg=svg, ratio=H / W, side=side, toggle=toggle,
                      bare='' if has_notes else ' bare', loading='eager' if n <= 2 else 'lazy')


def overview_html(spec, titles):
    o = spec.get('overview') or {}
    summary = o.get('summary') or spec.get('lede', '')
    ideas = ''.join('<div class="idea"><h4>%s</h4><p>%s</p></div>' % (e(a), rich(b)) for a, b in o.get('ideas', ()))
    secs = ''.join('<li><a href="#slide-%s">%s</a><span>%s</span></li>' % (
        re.match(r'Slides? (\d+)', a).group(1), e(a), e(b)) for a, b in o.get('sections', ()))
    exam = o.get('exam') or spec.get('exam_focus', '')
    toc = ''.join('<li><a href="#slide-%d"><b>%d</b> %s</a></li>' % (n, n, e(t)) for n, t in titles)
    how = ('<p>Every original slide is shown unchanged. <span class="key-hl">Yellow marks</span> on a slide point to a numbered note: '
           'hover or tap a mark to jump to its note, and hover a note to see its marks. Questions tagged <span class="tag past">Past exam</span> '
           'appeared on a real paper; <span class="tag predict">Prediction</span> questions are likely angles, not confirmed.</p>')
    left = ('<div><h4>How the lecture is organized</h4><ul class="secs">%s</ul></div>' % secs) if secs else ''
    right = '<div>%s<h4>How to read this page</h4>%s</div>' % (('<h4>Exam focus</h4><p>%s</p>' % rich(exam)) if exam else '', how)
    return '''
<section class="card overview" id="overview">
  <header class="card-head"><span class="sn">Overview</span><h3>%(title)s</h3>
    <button type="button" class="ov-toggle" aria-expanded="true" aria-controls="ov-body">Hide overview</button></header>
  <div id="ov-body" class="ov-body">
    %(summary)s
    %(ideas)s
    <div class="ov-grid">%(left)s%(right)s</div>
    <details class="toc"><summary>All %(count)d slides</summary><ol>%(toc)s</ol></details>
  </div>
</section>''' % dict(title=e(spec['title']), summary=''.join('<p class="lead">%s</p>' % rich(p) for p in summary.split('\n\n') if p.strip()), ideas=('<div class="ideas">%s</div>' % ideas) if ideas else '',
                      left=left, right=right, toc=toc, count=len(titles))


CSS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'annotated_page.css')
JS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'annotated_page.js')

THEME_BOOT = ('<script>try{var t=localStorage.getItem("shoug-theme");document.documentElement.setAttribute("data-theme",'
              't==="dark"||t==="light"?t:(matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light"))}catch(e){}</script>')


def page_html(spec, cards, titles, has_pdf):
    pdf_btn = ('<a class="btn" href="%s.pdf" download>PDF</a>' % e(spec['file'])) if has_pdf else (
        ('<a class="btn" href="%s" target="_top">Original</a>' % e(spec['original'])) if spec.get('original') else '')
    se322_mcq_css = '<link rel="stylesheet" href="/styles/se322-mcq-practice.css">' if spec.get('key', '').startswith('se322-') else ''
    se322_mcq_js = '<script src="/javascripts/se322-mcq-practice.js"></script>' if spec.get('key', '').startswith('se322-') else ''
    return '''<!doctype html>
<html lang="en" data-theme="light" data-sg-styled>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%(head)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(url)s">
<meta name="robots" content="noindex, follow">
<link rel="icon" type="image/png" sizes="256x256" href="/assets/shoug-favicon-v4.png">
%(boot)s
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
%(se322_mcq_css)s
<style>%(css)s</style>
</head>
<body data-key="%(key)s">
<header class="top"><div class="wrap">
  <div class="brand"><small>%(chapter)s · Annotated Slides</small><strong>%(title)s</strong></div>
  <div class="controls" role="group" aria-label="Page controls">
    <div class="seg" role="group" aria-label="View mode"><button type="button" id="m-scroll" aria-pressed="true" title="All slides on one scrolling page">Scroll</button><button type="button" id="m-flip" aria-pressed="false" title="One slide at a time (arrow keys or swipe to turn)">Flip</button></div>
    <button type="button" id="t-notes" aria-pressed="true" title="Show or hide all notes">Notes</button>
    <button type="button" id="t-hl" aria-pressed="true" title="Show or hide the highlights on the slides">Highlights</button>
    <button type="button" id="t-ans" aria-pressed="false" title="Show or hide every exam answer">Answers</button>
    %(pdf)s
    <button type="button" id="t-theme" title="Switch light or dark theme">Dark</button>
  </div>
</div></header>
<main>
%(overview)s
%(cards)s
</main>
<nav class="flipbar" aria-label="Slide navigation" hidden>
  <button type="button" id="f-prev" aria-label="Previous slide">Previous</button>
  <select id="f-jump" aria-label="Go to slide"></select>
  <button type="button" id="f-next" aria-label="Next slide">Next</button>
</nav>
<footer class="end">%(footer)s</footer>
<script>%(js)s</script>
%(se322_mcq_js)s
</body>
</html>
''' % dict(head=e(spec['head_title']), desc=e(spec['description']), url=e(spec['url']), boot=THEME_BOOT,
           css=open(CSS_PATH, encoding='utf-8').read(), key=e(spec['key']), chapter=e(spec['chapter']), title=e(spec['title']),
           pdf=pdf_btn, overview=overview_html(spec, titles), cards=''.join(cards), footer=rich(spec['footer']),
           js=open(JS_PATH, encoding='utf-8').read(), se322_mcq_css=se322_mcq_css, se322_mcq_js=se322_mcq_js)


def export_pdf(html_path, pdf_path):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel='chrome')
        pg = browser.new_page()
        pg.goto('file://' + html_path, wait_until='networkidle')
        pg.evaluate('''() => { document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager');
                         document.querySelectorAll('details').forEach(d => d.open = true);
                         document.documentElement.setAttribute('data-theme', 'light'); }''')
        pg.wait_for_function('() => Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)')
        pg.emulate_media(media='print')
        pg.pdf(path=pdf_path, format='A4', print_background=True,
               margin=dict(top='12mm', bottom='12mm', left='12mm', right='12mm'), prefer_css_page_size=True)
        browser.close()


def build(spec):
    """Write <out_dir>/<file>.html (+ figures, + <file>.pdf when spec['pdf']). Returns a small report.

    spec: src (PDF), out_dir, file, url, key (storage prefix), head_title, description, chapter, title, lede,
          overview (optional dict), exam_focus, footer, original (link to the original deck), slides (schema above),
          titles (optional {n: title}), strict (missing highlight phrase = error), pdf (bool), width."""
    src = spec['src']
    pdf = pdfplumber.open(src)
    total = len(pdf.pages)
    slides = spec['slides']
    extra = sorted(n for n in slides if not 1 <= n <= total)
    if extra:
        raise SystemExit('%s: notes for slides that are not in the PDF: %s' % (spec['key'], extra))
    render(src, spec['out_dir'], spec.get('width', WIDTH))
    size = Image.open(os.path.join(spec['out_dir'], 'figures', 'slide-01.jpg')).size
    pwords = pdf_words(pdf)
    ocr = {}
    cards, titles, missing, n_hl = [], [], [], 0
    for n in range(1, total + 1):
        sd = slides.get(n, {})
        rects = []
        for h in sd.get('hl', ()):
            phrase, note = h[0], h[1]
            occ = h[2] if len(h) > 2 else 0
            # h[3]: True = found automatically (a bold term from a note), 'ocr' = a label inside a picture;
            # both are skipped quietly when absent, and only 'ocr' marks pay for OCR on slides that have text
            soft = h[3] if len(h) > 3 else False
            got = find(pwords[n - 1], phrase, occ)
            if got is None and (soft in (False, 'ocr') or not pwords[n - 1]):
                if n not in ocr:
                    ocr[n] = ocr_words(src, n)
                got = find(ocr[n], phrase, occ)
            if got is None:
                if soft:
                    continue
                missing.append((n, phrase))
                continue
            pad_x, pad_y = 0.003, 0.004
            rects += [(note, (max(0, b['x0'] - pad_x), max(0, b['y0'] - pad_y), min(1, b['x1'] + pad_x), min(1, b['y1'] + pad_y))) for b in got]
        n_hl += len(rects)
        t = (spec.get('titles') or {}).get(n) or sd.get('title') or slide_title(pdf, n) or 'Slide %d' % n
        titles.append((n, t))
        cards.append(slide_html(n, total, t, sd, rects, size))
    pdf.close()
    if missing and spec.get('strict'):
        raise SystemExit('%s: highlight phrases not found on their slides:\n%s' % (
            spec['key'], '\n'.join('  slide %d: %r' % m for m in missing)))
    out_html = os.path.join(spec['out_dir'], spec['file'] + '.html')
    out_pdf = os.path.join(spec['out_dir'], spec['file'] + '.pdf')
    has_pdf = bool(spec.get('pdf')) or os.path.exists(out_pdf)
    with open(out_html, 'w', encoding='utf-8') as fh:
        fh.write(page_html(spec, cards, titles, has_pdf))
    if spec.get('pdf'):
        export_pdf(out_html, out_pdf)
    return dict(slides=total, highlights=n_hl, missing=missing, ocr=sorted(ocr))

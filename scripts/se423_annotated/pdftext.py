"""Read slide text straight from an SE423 lecture PDF, in the annotated-slides body markup.

The decks use fonts whose glyph ids are Unicode code points, so pdfplumber reports
"(cid:87)" for "W"; those are decoded here. Text recognised from the instructor's
handwriting (the iPad OCR layer, fonts named ".SFUI-...") is dropped: it is not slide
text, and the annotation files record what it says by hand instead. Words in the title's
font below title size are the slide's bold text.
"""
import re
import unicodedata

import pdfplumber

CID = re.compile(r'\(cid:(\d+)\)')
BULLETS = ('•', '', '▪', '◦', '–', '➢', '✓', 'o', '-', '>', '->', '§', 'Ø', '')
# Mis-encoded Arabic glosses come out as IPA/combining marks; they are noise here.
NOISE = re.compile(r'[Ā-ͯ֐-ۿ]')


def clean(text):
    text = CID.sub(lambda m: chr(int(m.group(1))), text)
    text = NOISE.sub('', text)
    text = re.sub(r'[\u02b0-\u02ff]', '', text)
    text = unicodedata.normalize('NFKC', text)
    text = re.sub(r'\(\s*\)', '', text)
    return re.sub(r'[ \t]+', ' ', text)


def _lines(words):
    lines = []
    for w in sorted(words, key=lambda w: (round(w['top']), w['x0'])):
        for line in lines:
            if abs(line['top'] - w['top']) < 3.5 and w['x0'] >= line['x1'] - 2 and w['x0'] - line['x1'] < 40:
                line['words'].append(w)
                line['x1'] = w['x1']
                break
        else:
            lines.append({'top': w['top'], 'x0': w['x0'], 'x1': w['x1'], 'words': [w]})
    for line in lines:
        line['words'].sort(key=lambda w: w['x0'])
    return sorted(lines, key=lambda l: (round(l['top'] / 4), l['x0']))


def _text(line, bold_font):
    out, run = [], []

    def flush():
        if run:
            joined = ' '.join(run).strip()
            if joined:
                out.append('**%s**' % joined)
            run.clear()
    for w in line['words']:
        t = clean(w['text']).strip()
        if not t:
            continue
        if bold_font and w['fontname'] == bold_font and t not in BULLETS:
            run.append(t)
        else:
            flush()
            out.append(t)
    flush()
    text = re.sub(r'\*\* \*\*', ' ', ' '.join(out))
    text = re.sub(r'\s*\(\s*\)', '', text)
    text = re.sub(r'(?<=\w) +([.,:;])(?=\s|$)', r'\1', text)
    return re.sub(r'Copyright ©.*?All Rights Reserved', '', text).strip()


def read_deck(pdf_path):
    pages = []
    with pdfplumber.open(pdf_path) as doc:
        for number, page in enumerate(doc.pages, 1):
            words = page.extract_words(extra_attrs=['size', 'fontname'], keep_blank_chars=True, x_tolerance=1.5)
            words = [w for w in words if 'SFUI' not in w['fontname'] and clean(w['text']).strip()]
            words = [w for w in words if not (w['size'] < 11 and w['top'] > 400 and clean(w['text']).strip().isdigit())]
            title_words = [w for w in words if w['size'] >= 27 and w['top'] < 80]
            big = [w for w in words if w['size'] >= 38]
            kind = 'content'
            if not title_words and big:
                kind, title_words = 'section', big
            title = ' '.join(' '.join(clean(w['text']).strip() for w in l['words'])
                             for l in _lines(title_words)).strip()
            title = re.sub(r'^\d{1,2}\s+(?=[A-Z])|\s+\d{1,2}$', '', re.sub(r'\s+', ' ', title))
            bold_font = title_words[0]['fontname'] if title_words else None
            body_words = [w for w in words if w not in title_words and w['size'] < 38]
            pages.append({'n': number, 'kind': kind, 'title': title, 'body': _body(_lines(body_words), bold_font),
                          'width': float(page.width), 'height': float(page.height)})
    return pages


def _join(a, b):
    return a + b if re.search(r'[A-Za-z]-$', a) else (a + ' ' + b).strip()


def _body(lines, bold_font):
    items = []  # [x0_of_bullet, text, numbered]
    for line in lines:
        text = _text(line, bold_font)
        if not text:
            continue
        first = clean(line['words'][0]['text']).strip()
        bullet = first in BULLETS or text.startswith('• ')
        numbered = re.match(r'^(\d{1,2})[.)]\s*(.*)$', text)
        if bullet:
            text = re.sub(r'^(\*\*)?(•|||▪|◦|–|➢|✓|o|-|>|->|§|Ø)(\*\*)?\s*', '', text).strip()
            if not text:
                items.append([line['x0'], '', False, True])
                continue
            items.append([line['x0'], text, False, True])
        elif numbered and len(numbered.group(2)) > 0:
            items.append([line['x0'], numbered.group(2), True, True])
        elif items and items[-1][3] and (line['x0'] > items[-1][0] + 4 or items[-1][1] == '') :
            items[-1][1] = _join(items[-1][1], text)
        elif items and not items[-1][3] and abs(line['x0'] - items[-1][0]) < 6:
            items[-1][1] = _join(items[-1][1], text)
        else:
            items.append([line['x0'], text, False, False])
    items = [i for i in items if i[1]]
    xs = sorted({round(i[0]) for i in items if i[3]})
    levels = []
    for x in xs:
        if not levels or x - levels[-1] > 9:
            levels.append(x)

    def level(x):
        return min(4, 1 + max((i for i, lx in enumerate(levels) if x >= lx - 5), default=0))
    out = []
    for x0, text, numbered, is_item in items:
        text = re.sub(r'\*\*\s*\*\*', '', text)
        if numbered:
            out.append('# ' + text)
        elif is_item:
            out.append('-' * level(x0) + ' ' + text)
        else:
            out.append(text)
    return out

"""Read slide text straight from a CS331 lecture PDF, in the annotated-slides body markup.

The CS331 decks (Forouzan's McGraw-Hill slides, edited by the instructor) have no fixed
title size, so the title is the top line of the slide. "Figure x.y" captions at the top
become the title. Words drawn over a picture are figure labels and are dropped, as are
the McGraw-Hill footer and page numbers. Bold words count as bold only when most of the
slide is in a regular weight (several decks set every word in bold).
"""
import re

import pdfplumber

from se423_annotated.pdftext import BULLETS, _lines, clean

BULLET_GLYPHS = set(BULLETS) | {'■', '◼', '▪', '', '', '❑', '', '●', '⮚', '🡺'}


def picture_boxes(page):
    """Pictures on the slide, leaving out background tiles that run off the page or fill most of it."""
    w, h = float(page.width), float(page.height)
    return [(i['x0'], i['top'], i['x1'], i['bottom']) for i in page.images
            if (i['x1'] - i['x0']) * (i['bottom'] - i['top']) > 4000 and i['x1'] <= w + 2 and i['bottom'] <= h + 2
            and (i['x1'] - i['x0']) * (i['bottom'] - i['top']) < w * h * 0.6]


def _in_picture(w, pictures):
    cx, cy = (w['x0'] + w['x1']) / 2, (w['top'] + w['bottom']) / 2
    return any(x0 - 2 <= cx <= x1 + 2 and y0 - 2 <= cy <= y1 + 2 for x0, y0, x1, y1 in pictures)


def _join(a, b):
    """Join a wrapped line onto the previous one; a word broken at a hyphen stays one word."""
    return a + b if re.search(r'[A-Za-z]-(\*\*)?$', a) else (a + ' ' + b).strip()


def _snap_bullets(words):
    """Bullet glyphs are set smaller than their text, so they sit on their own baseline; move them onto it."""
    texts = [w for w in words if clean(w['text']).strip() not in BULLET_GLYPHS]
    for b in words:
        if clean(b['text']).strip() not in BULLET_GLYPHS:
            continue
        mid = (b['top'] + b['bottom']) / 2
        near = [w for w in texts if 0 <= w['x0'] - b['x0'] < 60 and abs((w['top'] + w['bottom']) / 2 - mid) < 14]
        if near:
            w = min(near, key=lambda w: (w['x0'], abs((w['top'] + w['bottom']) / 2 - mid)))
            b['top'], b['bottom'] = w['top'], w['bottom']
    return words


def _title_lines(lines):
    """The slide title: the first line, plus following lines in the same size that sit right under it."""
    if not lines or lines[0]['top'] > 110:
        return []
    first = lines[0]
    size = first['words'][0]['size']
    out = [first]
    for line in lines[1:]:
        prev = out[-1]
        gap = line['top'] - max(w['bottom'] for w in prev['words'])
        if abs(line['words'][0]['size'] - size) < 1 and gap < size * 0.55 and line['top'] < 140:
            out.append(line)
        else:
            break
    return out


def read_deck(pdf_path):
    pages = []
    with pdfplumber.open(pdf_path) as doc:
        for number, page in enumerate(doc.pages, 1):
            h = float(page.height)
            pictures = picture_boxes(page)
            words = page.extract_words(extra_attrs=['size', 'fontname'], keep_blank_chars=True, x_tolerance=1.5)
            words = [w for w in words if clean(w['text']).strip() and w['top'] < h - 28 and not _in_picture(w, pictures)]
            lines = _lines(_snap_bullets(words))
            title_lines = _title_lines(lines)
            title = ' '.join(' '.join(clean(w['text']).strip() for w in l['words']) for l in title_lines)
            title = re.sub(r'\s+', ' ', title).strip()
            fig = re.match(r'^(Figure\s*[\d.]*\s*:?)\s*(.*)$', title)
            if fig and fig.group(2):
                title = '%s %s' % (fig.group(2).strip(), '(%s)' % fig.group(1).rstrip(' :') if re.search(r'\d', fig.group(1)) else '')
                title = title.strip()
            title_words = [w for l in title_lines for w in l['words']]
            body_words = [w for w in words if w not in title_words]
            text_words = [w for w in body_words if clean(w['text']).strip() not in BULLET_GLYPHS]
            bold = sum(1 for w in text_words if 'Bold' in w['fontname'])
            bold_font = 'Bold' if text_words and bold / len(text_words) < 0.5 else None
            for w in body_words:
                w['fontname'] = 'Bold' if 'Bold' in w['fontname'] else 'Regular'
            kind = 'title' if number == 1 else 'content'
            pages.append({'n': number, 'kind': kind, 'title': title, 'body': _body(_lines(body_words), bold_font),
                          'width': float(page.width), 'height': h, 'pictures': len(pictures)})
    return pages


def _body(lines, bold_font):
    """se423_annotated.pdftext._body, but "1.1 Data" is a heading, not item 1, and bold is any Bold font."""
    items = []  # [x0_of_bullet, text, numbered, is_item]
    for line in lines:
        text = _text(line, bold_font)
        if not text:
            continue
        first = clean(line['words'][0]['text']).strip()
        bullet = first in BULLET_GLYPHS
        numbered = re.match(r'^(\d{1,2})[.)-]\s+(?!\d)(.*)$', text)
        if bullet:
            text = re.sub(r'^(\*\*)?(%s)(\*\*)?\s*' % '|'.join(map(re.escape, BULLET_GLYPHS)), '', text).strip()
            items.append([line['x0'], text, False, True])
        elif numbered and numbered.group(2):
            items.append([line['x0'], numbered.group(2), True, True])
        elif items and items[-1][3] and (line['x0'] > items[-1][0] + 4 or items[-1][1] == '' or re.match(r'[a-z(]', text)):
            items[-1][1] = _join(items[-1][1], text)
        elif items and not items[-1][3] and abs(line['x0'] - items[-1][0]) < 6 and not items[-1][1].endswith(('.', ':', '?')):
            items[-1][1] = _join(items[-1][1], text)
        else:
            items.append([line['x0'], text, False, False])
    # Stray slide numbers ("28", "26.13") are not slide text.
    items = [i for i in items if i[1] and not re.fullmatch(r'\d{1,2}(\.\d{1,2})?', i[1].strip())]
    xs = sorted({round(i[0]) for i in items if i[3]})
    levels = []
    for x in xs:
        if not levels or x - levels[-1] > 9:
            levels.append(x)

    def level(x):
        return min(4, 1 + max((i for i, lx in enumerate(levels) if x >= lx - 5), default=0))
    out = []
    for x0, text, numbered, is_item in items:
        text = re.sub(r'\*\*(\s*)\*\*', r'\1', text)
        text = re.sub(r'\*\* +([.,:;)])', r'**\1', text)
        if numbered:
            out.append('# ' + text)
        elif is_item:
            out.append('-' * level(x0) + ' ' + text)
        else:
            out.append(text)
    return out


def _text(line, bold_font):
    out, run = [], []

    def flush():
        if run:
            out.append('**%s**' % ' '.join(run).strip())
            run.clear()
    for w in line['words']:
        t = clean(w['text']).strip()
        if not t:
            continue
        if bold_font and w['fontname'] == bold_font and t not in BULLET_GLYPHS:
            run.append(t)
        else:
            flush()
            out.append(t)
    flush()
    text = re.sub(r'\*\* \*\*', ' ', ' '.join(out))
    text = re.sub(r'\*\*(\s*[(),.:;]\s*)\*\*', r'\1', text)
    text = re.sub(r'(?<=\w) +([.,:;)])(?=\s|$)', r'\1', text)
    text = re.sub(r'\( +', '(', text)
    text = re.sub(r'\*\* +([.,:;)])', r'**\1', text)
    text = re.sub(r'\( \*\*', '(**', text)
    return text.strip()


if __name__ == '__main__':
    import sys
    for p in read_deck(sys.argv[1]):
        print('=== %d [%s] %s  (pictures: %d)' % (p['n'], p['kind'], p['title'], p['pictures']))
        for line in p['body']:
            print('   ', line)


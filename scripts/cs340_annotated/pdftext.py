"""Read slide text from a CS340 lecture PDF with the shared reader (CS331's, with the SE322 bullet glyphs).

Several CS340 decks set their titles in widely letter-spaced capitals, so the reader sees every letter
as its own word ("L E A R N I N G G O A L S"). Those titles are rebuilt here from the page's
characters, keeping the real space glyphs. Any "(cid:N)" code left over is plain ASCII."""
import re

import pdfplumber

from cys401_annotated import pdftext

CID = re.compile(r'\(cid:(\d+)\)')
SPACED = re.compile(r'^(?:\S ){3,}\S')


def _decode(text):
    return CID.sub(lambda m: chr(int(m.group(1))) if 31 < int(m.group(1)) < 127 else ' ', text)


def _title_from_chars(page):
    top = [c for c in page.chars if c['top'] < page.height * 0.3 and c['text'] != '\n']
    if not top:
        return ''
    big = max(c['size'] for c in top)
    chars = sorted((c for c in top if c['size'] >= big * 0.9), key=lambda c: (round(c['top'] / 8), c['x0']))
    lines, last = [], None
    for c in chars:
        row = round(c['top'] / 8)
        if row != last:
            lines.append('')
            last = row
        lines[-1] += _decode(c['text'])
    return re.sub(r'\s+', ' ', ' '.join(lines)).strip()


def read_deck(pdf_path):
    pages = pdftext.read_deck(pdf_path)
    with pdfplumber.open(pdf_path) as pdf:
        for p in pages:
            if SPACED.match(p['title']) or (p['title'].isupper() and len(p['title']) > 3):
                p['title'] = _title_from_chars(pdf.pages[p['n'] - 1]) or p['title']
            p['title'] = _decode(p['title'])
            p['body'] = [_decode(line) for line in p['body']]
    return pages


if __name__ == '__main__':
    import sys
    for p in read_deck(sys.argv[1]):
        print('=== %d [%s] %s  (pictures: %d)%s' % (p['n'], p['kind'], p['title'], p['pictures'], ' COMPLEX' if p['complex'] else ''))
        for line in p['body']:
            print('   ', line)

"""Read slide text from an SE322 lecture PDF: the CS331 reader, plus SE322's check-mark and
Wingdings bullets and its "Prince Sultan University | Slides prepared from ..." footer."""
from cs331_annotated import pdftext

GLYPHS = ('✓', '✔', '➢', '', '', '', '', '−', '¥', '')
FOOTER = r'Prince Sultan University|Slides prepared from|Dr\. Banda|^Ramadan$'


# Some decks were exported with Mac Roman punctuation read as Latin-1.
MAC_ROMAN = str.maketrans({'Ð': '–', 'Ñ': '—', 'Õ': '’', 'Ô': '‘', 'Ò': '“', 'Ó': '”', 'É': '…', '¥': '• '})


def read_deck(pdf_path):
    pages = pdftext.read_deck(pdf_path, glyphs=GLYPHS, footer=FOOTER)
    for p in pages:
        p['title'] = p['title'].translate(MAC_ROMAN)
        p['body'] = [line.translate(MAC_ROMAN) for line in p['body']]
    return pages


if __name__ == '__main__':
    import sys
    for p in read_deck(sys.argv[1]):
        print('=== %d [%s] %s  (pictures: %d)' % (p['n'], p['kind'], p['title'], p['pictures']))
        for line in p['body']:
            print('   ', line)

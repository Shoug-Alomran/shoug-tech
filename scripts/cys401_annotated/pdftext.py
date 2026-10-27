"""Read slide text from a CYS401 lecture PDF: the CS331 reader with the SE322 bullet glyphs."""
from cs331_annotated import pdftext
from se322_annotated.pdftext import GLYPHS as SE322_GLYPHS, MAC_ROMAN

GLYPHS = SE322_GLYPHS + ('◻',)

FOOTER = r'^\d+$|Prince Sultan University|Fundamentals of Cybersecurity$'


def read_deck(pdf_path):
    pages = pdftext.read_deck(pdf_path, glyphs=GLYPHS, footer=FOOTER)
    for p in pages:
        p['title'] = p['title'].translate(MAC_ROMAN)
        p['body'] = [line.translate(MAC_ROMAN) for line in p['body']]
    return pages


if __name__ == '__main__':
    import sys
    for p in read_deck(sys.argv[1]):
        print('=== %d [%s] %s  (pictures: %d)%s' % (p['n'], p['kind'], p['title'], p['pictures'], ' COMPLEX' if p['complex'] else ''))
        for line in p['body']:
            print('   ', line)

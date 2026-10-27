"""Read slide text from a CYS403 lecture PDF: the CS331 reader with the SE322 bullet glyphs, minus the
"Dr. Suliman Gaber, PSU, <date>" footer stamped on every slide."""
import re

from cs331_annotated import pdftext
from cys401_annotated.pdftext import GLYPHS
from se322_annotated.pdftext import MAC_ROMAN

FOOTER = r'^\d+$|^\d \d$|Dr\. Suliman Gaber|^PSU,'


def read_deck(pdf_path):
    pages = pdftext.read_deck(pdf_path, glyphs=GLYPHS, footer=FOOTER)
    for p in pages:
        p['title'] = '' if re.match(r'^\d \d$', p['title']) else p['title'].translate(MAC_ROMAN)
        p['body'] = [line.translate(MAC_ROMAN) for line in p['body']]
    return pages

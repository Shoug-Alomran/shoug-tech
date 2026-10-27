"""Read slide text from an SE311 lecture PDF. The Movie Shop exercise decks set their titles in
letter-spaced capitals without space glyphs, so this uses the CS340 reader (which rebuilds such titles
from the page's characters) and then puts the word breaks back."""
import re

from cs340_annotated import pdftext

WORDS = ('EXERCISE:', 'MOVIE', 'SHOP', 'DOMAIN', 'MODEL', 'ANALYSIS', 'SOLUTION', 'COMMON', 'ERRORS', 'USE-CASE',
         'FUNCTIONALITY', 'AND', 'GROUPING', 'INITIAL', 'REFINED', 'DIAGRAM')
GLUED = re.compile('(%s)' % '|'.join(map(re.escape, sorted(WORDS, key=len, reverse=True))))


def _space(title):
    if not title.startswith('EXERCISE'):
        return title
    return re.sub(r'\s+', ' ', GLUED.sub(r' \1 ', title)).strip()


def read_deck(pdf_path):
    pages = pdftext.read_deck(pdf_path)
    for p in pages:
        p['title'] = _space(p['title'])
    return pages

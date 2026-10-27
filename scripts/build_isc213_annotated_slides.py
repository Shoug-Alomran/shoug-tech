#!/usr/bin/env python3
"""Build ISC213 "Annotated Slides": the lecture decks rebuilt as HTML with study notes on top.

Content lives in scripts/isc213_annotated/ (one module per deck); the page engine and the
site wiring are in scripts/annotated_slides.py. It is safe to re-run.

Usage: python3 scripts/build_isc213_annotated_slides.py
"""
import annotated_slides
from isc213_annotated import pdftext

COURSE = annotated_slides.Course(
    code='ISC213',
    name='Islamic Financial Transactions',
    track='other-courses',
    package='isc213_annotated',
    # Decks with annotation content, in course order.
    built=['decks:transactions', 'decks:rights', 'decks:incorporeal', 'decks:insurance', 'decks:securities', 'decks:shares', 'decks:bonds', 'decks:lease', 'decks:murabaha'],
    read_deck=pdftext.read_deck,
    template=('computer-science/cs331', '01-data-communications-and-networking', 'data-communications-and-networking'),
    after=('slides/', 'Slides'),
    page_name=lambda deck: annotated_slides.C.decks[deck['key']][3],
    item_label=lambda label: label,
    papers=annotated_slides.PAPER_WORDS,
    prof_legend=False,
)

if __name__ == '__main__':
    annotated_slides.build(COURSE)

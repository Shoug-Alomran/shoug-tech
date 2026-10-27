#!/usr/bin/env python3
"""Build ISC113 "Annotated Slides": the lecture decks rebuilt as HTML with study notes on top.

Content lives in scripts/isc113_annotated/ (one module per deck); the page engine and the
site wiring are in scripts/annotated_slides.py. It is safe to re-run.

Usage: python3 scripts/build_isc113_annotated_slides.py
"""
import annotated_slides
from isc113_annotated import pdftext

COURSE = annotated_slides.Course(
    code='ISC113',
    name='Islamic Economy',
    track='other-courses',
    package='isc113_annotated',
    # Decks with annotation content, in course order.
    built=['decks:concept', 'decks:systems', 'decks:terms', 'decks:budget', 'decks:revenues', 'decks:dilemma', 'decks:production', 'decks:consumption', 'decks:market', 'decks:pricing', 'decks:money', 'decks:banks'],
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

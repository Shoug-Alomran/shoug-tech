#!/usr/bin/env python3
"""Build CS340 "Annotated Slides": the lecture decks rebuilt as HTML with study notes on top.

Content lives in scripts/cs340_annotated/ (one module per deck); the page engine and the
site wiring are in scripts/annotated_slides.py. It is safe to re-run.

Usage: python3 scripts/build_cs340_annotated_slides.py
"""
import annotated_slides
from cs340_annotated import pdftext

COURSE = annotated_slides.Course(
    code='CS340',
    name='Computer Architecture',
    track='computer-science',
    package='cs340_annotated',
    # Decks with annotation content, in course order.
    built=['decks:intro', 'decks:concepts', 'decks:eer', 'decks:relational', 'decks:mapping', 'decks:basic_sql', 'decks:advanced_sql', 'decks:normalization', 'decks:nosql'],
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

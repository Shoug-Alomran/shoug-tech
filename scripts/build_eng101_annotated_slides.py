#!/usr/bin/env python3
"""Build ENG101 "Annotated Slides": the lecture decks rebuilt as HTML with study notes on top.

Content lives in scripts/eng101_annotated/ (one module per deck); the page engine and the
site wiring are in scripts/annotated_slides.py. It is safe to re-run.

Usage: python3 scripts/build_eng101_annotated_slides.py
"""
import annotated_slides
from eng101_annotated import pdftext

COURSE = annotated_slides.Course(
    code='ENG101',
    name='Intensive Writing',
    track='other-courses/english',
    package='eng101_annotated',
    # Decks with annotation content, in course order.
    built=['decks:thesis_guide', 'decks:thesis_practice', 'decks:thesis_worksheet', 'decks:transitions', 'decks:transitions_punct', 'decks:connecting', 'decks:commas', 'decks:process', 'decks:classification', 'decks:cause_effect', 'decks:cc_overview', 'decks:cc_keywords', 'decks:cc_essay', 'decks:cc_assignment', 'decks:argumentative'],
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

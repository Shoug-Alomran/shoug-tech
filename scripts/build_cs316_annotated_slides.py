#!/usr/bin/env python3
"""Build CS316 "Annotated Slides": the lecture decks as slide images with study notes on top.

Content lives in scripts/cs316_annotated/; the page engine and site wiring are in
scripts/annotated_slides.py. It is safe to re-run.

Usage: python3 scripts/build_cs316_annotated_slides.py
"""
import annotated_slides
from cs316_annotated import pdftext

COURSE = annotated_slides.Course(
    code='CS316',
    name='Introduction to AI and Data Science',
    track='computer-science',
    package='cs316_annotated',
    built=['decks:%s' % key for key in annotated_slides.importlib.import_module('cs316_annotated.common').DECKS],
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

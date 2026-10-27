#!/usr/bin/env python3
"""Build CS330 "Annotated Slides": the lecture decks rebuilt as HTML with study notes on top.

Content lives in scripts/cs330_annotated/ (one module per deck); the page engine and the
site wiring are in scripts/annotated_slides.py. It is safe to re-run.

Usage: python3 scripts/build_cs330_annotated_slides.py
"""
import annotated_slides
from cs330_annotated import pdftext

COURSE = annotated_slides.Course(
    code='CS330',
    name='Introduction to Operating Systems',
    track='computer-science',
    package='cs330_annotated',
    # Decks with annotation content, in course order.
    built=['decks:intro', 'decks:services', 'decks:processes', 'decks:threads', 'decks:scheduling', 'decks:sync', 'decks:memory', 'decks:virtual_memory', 'decks:fs_interface', 'decks:fs_impl'],
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

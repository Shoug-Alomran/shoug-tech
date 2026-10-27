#!/usr/bin/env python3
"""Build SE201 "Annotated Slides": the lecture decks rebuilt as HTML with study notes on top.

Content lives in scripts/se201_annotated/ (one module per deck); the page engine and the
site wiring are in scripts/annotated_slides.py. It is safe to re-run.

Usage: python3 scripts/build_se201_annotated_slides.py
"""
import annotated_slides
from se201_annotated import pdftext

COURSE = annotated_slides.Course(
    code='SE201',
    name='Introduction to Software Engineering',
    track='software-engineering',
    package='se201_annotated',
    # Decks with annotation content, in course order.
    built=['decks:practices', 'decks:processes', 'decks:agile', 'decks:project_management', 'decks:requirements', 'decks:modeling', 'decks:design', 'decks:construction', 'decks:testing'],
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

#!/usr/bin/env python3
"""Build SE401 "Annotated Slides": the lecture decks rebuilt as HTML with study notes on top.

Content lives in scripts/se401_annotated/ (one module per deck); the page engine and the
site wiring are in scripts/annotated_slides.py. It is safe to re-run.

Usage: python3 scripts/build_se401_annotated_slides.py
"""
import annotated_slides
from se401_annotated import pdftext

COURSE = annotated_slides.Course(
    code='SE401',
    name='Software Testing and Quality',
    track='software-engineering',
    package='se401_annotated',
    # Decks with annotation content, in course order.
    built=['decks:introduction', 'decks:sdlc', 'decks:software_quality', 'decks:quality', 'decks:test_cases', 'decks:test_design', 'decks:black_box', 'decks:white_box', 'decks:code_coverage', 'decks:unit_testing', 'decks:regression', 'decks:metrics_tools', 'decks:advanced'],
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

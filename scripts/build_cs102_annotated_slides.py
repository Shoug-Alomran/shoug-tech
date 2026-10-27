#!/usr/bin/env python3
"""Build CS102 "Annotated Slides": the lecture decks rebuilt as HTML with study notes on top.

Content lives in scripts/cs102_annotated/ (one module per deck); the page engine and the
site wiring are in scripts/annotated_slides.py. It is safe to re-run.

Usage: python3 scripts/build_cs102_annotated_slides.py
"""
import annotated_slides
from cs102_annotated import pdftext

COURSE = annotated_slides.Course(
    code='CS102',
    name='Computer Programming 2',
    track='computer-science',
    package='cs102_annotated',
    # Decks with annotation content, in course order.
    built=['decks_a:classes', 'decks_a:interfaces', 'decks_a:files', 'decks_a:generics', 'decks_b:inheritance', 'decks_c:collections', 'decks_c:linked_lists', 'decks_b:polymorphism', 'decks_b:recursion', 'decks_c:collections_2', 'decks_b:arrays_2d'],
    read_deck=pdftext.read_deck,
    template=('computer-science/cs331', '01-data-communications-and-networking', 'data-communications-and-networking'),
    after=('slides/', 'Slides'),
    page_name=lambda deck: annotated_slides.C.decks[deck['key']][3],  # labels are the deck titles
    item_label=lambda label: label,
    papers=annotated_slides.PAPER_WORDS,
    prof_legend=False,
)

if __name__ == '__main__':
    annotated_slides.build(COURSE)

#!/usr/bin/env python3
"""Build CS101 "Annotated Slides": the lecture decks rebuilt as HTML with study notes on top.

Content lives in scripts/cs101_annotated/ (one module per deck); the page engine and the
site wiring are in scripts/annotated_slides.py. It is safe to re-run.

Usage: python3 scripts/build_cs101_annotated_slides.py
"""
import annotated_slides
from cs101_annotated import pdftext


def item_label(label):
    """'Ch 2 · Elementary Programming' -> 'Chapter 2 Elementary Programming'."""
    chapter, name = label.split(' · ')
    return '%s %s' % (chapter.replace('Ch ', 'Chapter '), name)

COURSE = annotated_slides.Course(
    code='CS101',
    name='Computer Programming 1',
    track='computer-science',
    package='cs101_annotated',
    # Decks with annotation content, in course order.
    built=['ch01_introduction', 'ch02_elementary_programming', 'ch03_selections', 'ch04_functions_characters_strings', 'ch05_loops', 'ch06_methods', 'ch07_arrays', 'ch12_exceptions_and_text_io'],
    read_deck=pdftext.read_deck,
    template=('computer-science/cs331', '01-data-communications-and-networking', 'data-communications-and-networking'),
    after=('slides/', 'Slides'),
    page_name=lambda deck: item_label(annotated_slides.C.decks[deck['key']][3]),
    item_label=item_label,
    papers=annotated_slides.PAPER_WORDS,
    prof_legend=False,
)

if __name__ == '__main__':
    annotated_slides.build(COURSE)

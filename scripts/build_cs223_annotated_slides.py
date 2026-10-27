#!/usr/bin/env python3
"""Build CS223 "Annotated Slides": the lecture decks rebuilt as HTML with study notes on top.

Content lives in scripts/cs223_annotated/ (one module per deck); the page engine and the
site wiring are in scripts/annotated_slides.py. It is safe to re-run.

Usage: python3 scripts/build_cs223_annotated_slides.py
"""
import annotated_slides
from cs223_annotated import pdftext

COURSE = annotated_slides.Course(
    code='CS223',
    name='Computational Linear Algebra',
    track='math',
    package='cs223_annotated',
    # Decks with annotation content, in course order.
    built=['decks:row_reduction', 'decks:vector_equations', 'decks:matrix_equation', 'decks:independence', 'decks:transformations', 'decks:matrix_operations', 'decks:inverse', 'decks:lu', 'decks:subspaces', 'decks:determinants', 'decks:det_properties', 'decks:cramer', 'decks:vector_spaces', 'decks:dimension_rank', 'decks:difference_equations', 'decks:eigen', 'decks:characteristic', 'decks:diagonalization', 'decks:eigen_transformations', 'decks:complex_eigen', 'decks:orthogonality', 'decks:orthogonal_sets', 'decks:projections', 'decks:least_squares', 'decks:linear_models', 'decks:iterative'],
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

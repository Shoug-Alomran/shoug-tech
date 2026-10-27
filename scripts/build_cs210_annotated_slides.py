#!/usr/bin/env python3
"""Build CS210 "Annotated Slides": the lecture decks rebuilt as HTML with study notes on top.

Content lives in scripts/cs210_annotated/ (one module per deck); the page engine and the
site wiring are in scripts/annotated_slides.py. It is safe to re-run.

Usage: python3 scripts/build_cs210_annotated_slides.py
"""
import annotated_slides
from cs210_annotated import pdftext

COURSE = annotated_slides.Course(
    code='CS210',
    name='Data Structures',
    track='computer-science',
    package='cs210_annotated',
    # Decks with annotation content, in course order.
    built=['decks:algorithm_analysis', 'decks:recursion', 'decks:lists', 'decks:circular_linked_lists', 'decks:stacks_and_queues', 'decks:elementary_sorting_algorithms', 'decks:merge_sort', 'decks:quick_sort', 'decks:trees', 'decks:binary_search_trees', 'decks:avl_trees', 'decks:heaps_and_priority_queues', 'decks:heaps', 'decks:hash_tables', 'decks:undirected_graphs', 'decks:directed_graphs'],
    read_deck=pdftext.read_deck,
    template=('01-lists', 'lists'),
    after=('slides/', 'Slides'),
    page_name=lambda deck: annotated_slides.C.decks[deck['key']][3],
    item_label=lambda label: label,
    papers=annotated_slides.PAPER_WORDS,
    prof_legend=False,
)

if __name__ == '__main__':
    annotated_slides.build(COURSE)

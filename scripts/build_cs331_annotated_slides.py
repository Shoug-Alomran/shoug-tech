#!/usr/bin/env python3
"""Build CS331 "Annotated Slides": the lecture decks rebuilt as HTML with study notes on top.

Content lives in scripts/cs331_annotated/ (one module per deck); the page engine and the
site wiring are in scripts/annotated_slides.py. It is safe to re-run.

Usage: python3 scripts/build_cs331_annotated_slides.py
"""
import re

import annotated_slides
from cs331_annotated import pdftext


def item_label(label):
    """'Ch 1 Part 2 · Introduction' -> 'Chapter 01 — Introduction Part 2', as in the course's slide lists."""
    chapter, name = label.split(' · ')
    m = re.match(r'Ch (\d+)(?: Part (\d+))?$', chapter)
    return 'Chapter %02d — %s%s' % (int(m.group(1)), name, ' Part %s' % m.group(2) if m.group(2) else '')


COURSE = annotated_slides.Course(
    code='CS331',
    name='Data Communications and Computer Networks',
    track='computer-science',
    package='cs331_annotated',
    # Decks with annotation content, in course order.
    built=['ch01_1_introduction', 'ch01_2_introduction', 'ch02_1_physical_layer', 'ch02_2_physical_layer',
           'ch03_1_data_link_layer', 'ch03_2_data_link_layer', 'ch04_lans', 'ch06_connecting_devices',
           'ch07_network_layer', 'ch08_routing', 'ch09_transport_layer', 'ch10_application_layer'],
    read_deck=pdftext.read_deck,
    template=('01-data-communications-and-networking', 'data-communications-and-networking'),
    after=('slides-with-notes/', 'Slides with Notes'),
    page_name=lambda deck: item_label(annotated_slides.C.decks[deck['key']][3]),
    item_label=item_label,
    papers={'stamp': '★ Tutorial', 'direct': 'Asked in a course tutorial', 'related': 'Related tutorial questions',
            'n_direct': 'asked in course tutorials', 'n_related': 'related to tutorial questions', 'folder': '',
            'desc': 'tutorial'},
    prof_legend=False,
)

if __name__ == '__main__':
    annotated_slides.build(COURSE)

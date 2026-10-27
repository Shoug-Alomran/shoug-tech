#!/usr/bin/env python3
"""Build SE322 "Annotated Slides": the lecture decks rebuilt as HTML with study notes on top.

Content lives in scripts/se322_annotated/ (one module per deck); the page engine and the
site wiring are in scripts/annotated_slides.py. It is safe to re-run.

Usage: python3 scripts/build_se322_annotated_slides.py
"""
import re

import annotated_slides
from se322_annotated import pdftext


def item_label(label):
    """'Ch 2 L1 · Software Architecture' -> 'Chapter 2 Software Architecture (Lecture 1)', as in the course's slide list."""
    chapter, name = label.split(' · ')
    m = re.match(r'Ch (\d+)(?: L(\d+))?$', chapter)
    return 'Chapter %s %s%s' % (m.group(1), name, ' (Lecture %s)' % m.group(2) if m.group(2) else '')


COURSE = annotated_slides.Course(
    code='SE322',
    name='Software Design and Architecture',
    track='software-engineering',
    package='se322_annotated',
    # Decks with annotation content, in course order.
    built=['ch01_introduction', 'ch02_1_software_architecture', 'ch02_2_software_architecture', 'ch02_3_software_architecture', 'ch03_1_quality_attributes', 'ch03_2_quality_attributes', 'ch04_1_architecture_patterns', 'ch04_2_architecture_patterns', 'ch04_3_architecture_patterns', 'ch05_1_detailed_design', 'ch05_2_detailed_design', 'ch05_3_detailed_design', 'ch06_1_creational_patterns', 'ch06_2_creational_patterns', 'ch06_3_creational_patterns', 'ch07_1_structural_patterns', 'ch07_2_behavioral_patterns', 'ch08_architecture_evaluation', 'ch09_documentation'],
    read_deck=pdftext.read_deck,
    template=('01-chapter-1-introduction-to-software-design-and-architecture-extra',
              'chapter-1-introduction-to-software-design-and-architecture-extra'),
    after=('slides/', 'Slides'),
    page_name=lambda deck: item_label(annotated_slides.C.decks[deck['key']][3]),
    item_label=item_label,
    prof_legend=False,
)

if __name__ == '__main__':
    annotated_slides.build(COURSE)

#!/usr/bin/env python3
"""Build SE423 "Annotated Slides": the lecture decks rebuilt as HTML with study notes on top.

Content lives in scripts/se423_annotated/ (one module per deck); the page engine and the
site wiring are in scripts/annotated_slides.py. It is safe to re-run.

Usage: python3 scripts/build_se423_annotated_slides.py
"""
import annotated_slides
from se423_annotated import pdftext

COURSE = annotated_slides.Course(
    code='SE423',
    name='Software Project Management',
    track='software-engineering',
    package='se423_annotated',
    # Decks with annotation content, in course order.
    built=['ch01_introduction', 'ch01_2_performance_domains', 'ch01_3_tailoring', 'ch02_organizational_context', 'ch03_team',
           'ch04_development_approach', 'ch05_risk_management', 'ch06_estimation', 'ch06_2_scheduling', 'ch07_quality',
           'ch08_stakeholders', 'ch09_change_management'],
    read_deck=pdftext.read_deck,
    template=('01-introduction', 'introduction'),
    after=('slides/', 'Slides'),
    page_name=lambda deck: '%s - %s' % (deck['title'], deck['chapter']),
    item_label=lambda label: '%s - %s' % (label.split(' · ')[1], label.split(' · ')[0].replace('Ch ', 'Chapter ')),
)

if __name__ == '__main__':
    annotated_slides.build(COURSE)

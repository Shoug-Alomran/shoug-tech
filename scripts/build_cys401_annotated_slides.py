#!/usr/bin/env python3
"""Build CYS401 "Annotated Slides": the lecture decks rebuilt as HTML with study notes on top.

Content lives in scripts/cys401_annotated/ (one module per deck); the page engine and the
site wiring are in scripts/annotated_slides.py. It is safe to re-run.

Usage: python3 scripts/build_cys401_annotated_slides.py
"""
import re

import annotated_slides
from cys401_annotated import pdftext


def item_label(label):
    """'Ch 6.1 · Asymmetric Cryptography and PKI' -> 'Chapter 6.1 Asymmetric Cryptography and PKI', as in the course's slide list."""
    chapter, name = label.split(' · ')
    return '%s %s' % (chapter.replace('Ch ', 'Chapter '), name)


COURSE = annotated_slides.Course(
    code='CYS401',
    name='Fundamentals of Cybersecurity',
    track='cybersecurity',
    package='cys401_annotated',
    # Decks with annotation content, in course order.
    built=['ch01_introduction', 'ch02_foundations', 'ch03_threat_modeling', 'ch04_information_assets', 'ch05_cryptography', 'ch06_1_asymmetric', 'ch06_2_pki', 'ch07_security_models', 'ch08_vulnerabilities', 'ch09_ics_scada', 'ch10_access_control'],
    read_deck=pdftext.read_deck,
    template=('01-chapter-1-introduction-to-cybersecurity', 'chapter-1'),
    after=('slides/', 'Slides'),
    page_name=lambda deck: item_label(annotated_slides.C.decks[deck['key']][3]),
    item_label=item_label,
    prof_legend=False,
)

if __name__ == '__main__':
    annotated_slides.build(COURSE)

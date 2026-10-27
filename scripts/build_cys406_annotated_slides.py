#!/usr/bin/env python3
"""Build CYS406 "Annotated Slides": the lecture decks rebuilt as HTML with study notes on top.

Content lives in scripts/cys406_annotated/ (one module per deck); the page engine and the
site wiring are in scripts/annotated_slides.py. It is safe to re-run.

Usage: python3 scripts/build_cys406_annotated_slides.py
"""
import annotated_slides
from cys406_annotated import pdftext

COURSE = annotated_slides.Course(
    code='CYS406',
    name='Data and Network Security',
    track='cybersecurity',
    package='cys406_annotated',
    # Decks with annotation content, in course order.
    built=['decks:fundamentals', 'decks:iam', 'decks:symmetric', 'decks:rsa', 'decks:ecc', 'decks:rc4_modes', 'decks:hashing', 'decks:diffie_hellman', 'decks:key_management', 'decks:protocols', 'decks:firewalls', 'decks:ids_ips', 'decks:vpn', 'decks:honeypots', 'decks:siem', 'decks:data_security'],
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

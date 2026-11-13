"""CS331 explaining notes and explained questions added to the annotated decks (see annotated_slides.build_page).

One module per deck (extra_chXX.py) holds NOTES (rewritten notes, in the same slots as the originals so highlight
links stay valid) and Q (every question, each wrong option with its reason). Decks in REPLACE drop their old
questions without reasons, since the bank rewrites them all.
"""
from . import (extra_ch01_1, extra_ch01_2, extra_ch02_1, extra_ch02_2, extra_ch03_1, extra_ch03_2, extra_ch04,
               extra_ch06, extra_ch07, extra_ch08, extra_ch09, extra_ch10)

_DECKS = {
    'ch1.1': extra_ch01_1,
    'ch1.2': extra_ch01_2,
    'ch2.1': extra_ch02_1,
    'ch2.2': extra_ch02_2,
    'ch3.1': extra_ch03_1,
    'ch3.2': extra_ch03_2,
    'ch4': extra_ch04,
    'ch6': extra_ch06,
    'ch7': extra_ch07,
    'ch8': extra_ch08,
    'ch9': extra_ch09,
    'ch10': extra_ch10,
}

QUESTIONS = {k: m.Q for k, m in _DECKS.items()}
NOTES = {k: m.NOTES for k, m in _DECKS.items()}
REPLACE = set(_DECKS)

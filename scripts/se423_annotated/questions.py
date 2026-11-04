"""SE423 practice questions and explaining notes added to slides, by deck key and slide number (see annotated_slides.build_page)."""
from . import ch05_extra, ch06_2_extra, ch06_extra, ch07_09_extra, questions_ch1_2, questions_ch1_3_ch2, questions_ch3, questions_ch4

QUESTIONS = {
    'ch1.2': questions_ch1_2.Q,
    'ch1.3': questions_ch1_3_ch2.CH1_3,
    'ch2': questions_ch1_3_ch2.CH2,
    'ch3': questions_ch3.Q,
    'ch4': questions_ch4.Q,
    'ch5': ch05_extra.Q,
    'ch6': ch06_extra.Q,
    'ch6.2': ch06_2_extra.Q,
    'ch7': ch07_09_extra.Q_7,
    'ch8': ch07_09_extra.Q_8,
    'ch9': ch07_09_extra.Q_9,
}

# Explaining notes for decks not in the page schema: they replace a slide's first notes (None keeps one).
NOTES = {
    'ch5': ch05_extra.NOTES,
    'ch6': ch06_extra.NOTES,
    'ch6.2': ch06_2_extra.NOTES,
    'ch7': ch07_09_extra.NOTES_7,
    'ch8': ch07_09_extra.NOTES_8,
    'ch9': ch07_09_extra.NOTES_9,
}

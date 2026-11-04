"""SE423 practice questions added to slides, by deck key and slide number (see annotated_slides.build_page)."""
from . import questions_ch1_2, questions_ch1_3_ch2, questions_ch3, questions_ch4

QUESTIONS = {
    'ch1.2': questions_ch1_2.Q,
    'ch1.3': questions_ch1_3_ch2.CH1_3,
    'ch2': questions_ch1_3_ch2.CH2,
    'ch3': questions_ch3.Q,
    'ch4': questions_ch4.Q,
}

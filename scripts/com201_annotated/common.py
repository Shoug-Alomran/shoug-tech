"""Constructors for COM201 annotated-slide content. The markup is the SE423 one (see se423_annotated/ch01_introduction.py)."""
from se423_annotated.common import mcq, scen, section, short, slide, tf, tip, trap, trick  # noqa: F401
from cs331_annotated.common import fig  # noqa: F401

# Every COM201 deck, in course order: key -> (annotated slug, standalone file, slides folder, label).
DECKS = {
    'd01': ('01-introduction-to-human-communication', 'introduction-to-human-communication', '01-chapter-1', 'Chapter 1: Introduction to Human Communication'),
    'd02': ('02-perception-self-and-communication', 'perception-self-and-communication', '02-chapter-2', 'Chapter 2: Perception, Self and Communication'),
    'd03': ('03-language-and-meaning', 'language-and-meaning', '03-chapter-3', 'Chapter 3: Language and Meaning'),
    'd04': ('04-nonverbal-communication', 'nonverbal-communication', '04-chapter-4', 'Chapter 4: Nonverbal Communication'),
    'd05': ('05-listening', 'listening', '05-chapter-5', 'Chapter 5: Listening'),
    'd06': ('06-interpersonal-communication', 'interpersonal-communication', '06-chapter-6', 'Chapter 6: Interpersonal Communication'),
    'd07': ('07-inclusive-communication', 'inclusive-communication', '07-chapter-7', 'Chapter 7: Prejudice, Bias and Inclusive Communication'),
    'd08': ('08-small-group-communication', 'small-group-communication', '08-chapter-8', 'Chapter 8: Small-Group Communication'),
}

# The real COM201 papers in exams/.
# exams/ has a study guide but no past papers.
PAPERS = {
}


def past(paper, label, related=False):
    assert paper in PAPERS, paper
    return {'paper': paper, 'label': label, 'related': related}


def see(deck, n, label):
    assert deck in DECKS, deck
    return {'deck': deck, 'n': n, 'label': label}

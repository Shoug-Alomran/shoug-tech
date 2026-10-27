"""Constructors for CS101 annotated-slide content. The markup is the SE423 one (see se423_annotated/ch01_introduction.py)."""
from se423_annotated.common import mcq, scen, section, short, slide, tf, tip, trap, trick  # noqa: F401
from cs331_annotated.common import fig  # noqa: F401

# Every CS101 deck, in course order: key -> (annotated slug, standalone file, slides folder, label).
DECKS = {
    'ch1': ('01-introduction-to-computers-programs-and-java', 'introduction-to-computers-programs-and-java', 'chapter-1', 'Ch 1 · Introduction to Computers, Programs, and Java'),
    'ch2': ('02-elementary-programming', 'elementary-programming', 'chapter-2', 'Ch 2 · Elementary Programming'),
    'ch3': ('03-selections', 'selections', 'chapter-3', 'Ch 3 · Selections'),
    'ch4': ('04-mathematical-functions-characters-and-strings', 'mathematical-functions-characters-and-strings', 'chapter-4',
            'Ch 4 · Mathematical Functions, Characters, and Strings'),
    'ch5': ('05-loops', 'loops', 'chapter-5', 'Ch 5 · Loops'),
    'ch6': ('06-methods', 'methods', 'chapter-6', 'Ch 6 · Methods'),
    'ch7': ('07-single-dimensional-arrays', 'single-dimensional-arrays', 'chapter-7', 'Ch 7 · Single-Dimensional Arrays'),
    'ch12': ('08-exception-handling-and-text-io', 'exception-handling-and-text-io', 'chapter-12', 'Ch 12 · Exception Handling and Text I/O'),
}

# The real CS101 papers in exams/.
PAPERS = {
}


def past(paper, label, related=False):
    assert paper in PAPERS, paper
    return {'paper': paper, 'label': label, 'related': related}


def see(deck, n, label):
    assert deck in DECKS, deck
    return {'deck': deck, 'n': n, 'label': label}

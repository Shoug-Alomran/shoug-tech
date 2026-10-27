"""Constructors for SE201 annotated-slide content. The markup is the SE423 one (see se423_annotated/ch01_introduction.py)."""
from se423_annotated.common import mcq, scen, section, short, slide, tf, tip, trap, trick  # noqa: F401
from cs331_annotated.common import fig  # noqa: F401

# Every SE201 deck, in course order: key -> (annotated slug, standalone file, slides folder, label).
DECKS = {
    'd01': ('01-software-engineering-practices-and-ethics', 'software-engineering-practices-and-ethics', 'chapter-1-software-engineering-practices-and-ethics', 'Chapter 1: Software Engineering Practices and Ethics'),
    'd02': ('02-software-processes', 'software-processes', 'chapter-2-software-processes', 'Chapter 2: Software Processes'),
    'd03': ('03-agile-software-engineering', 'agile-software-engineering', 'chapter-3-agile-software-engineering', 'Chapter 3: Agile Software Engineering'),
    'd04': ('04-software-project-management', 'software-project-management', 'chapter-4-software-project-management', 'Chapter 4: Software Project Management'),
    'd05': ('05-requirements-engineering', 'requirements-engineering', 'chapter-5-1-requirements-engineering', 'Chapter 5.1: Requirements Engineering'),
    'd06': ('06-system-modeling', 'system-modeling', 'chapter-5-2-system-modeling', 'Chapter 5.2: System Modeling'),
    'd07': ('07-software-design', 'software-design', 'chapter-6-software-design', 'Chapter 6: Software Design'),
    'd08': ('08-software-construction-implementation', 'software-construction-implementation', 'chapter-7-software-construction-implementation', 'Chapter 7: Software Construction (Implementation)'),
    'd09': ('09-software-testing', 'software-testing', 'chapter-8-software-testing', 'Chapter 8: Software Testing'),
}

# The real SE201 papers in exams/.
PAPERS = {
    'q1': ('Quiz 1 (Ch. 1 & 2)', '09-quiz-1-ch-1-and-2'),
}


def past(paper, label, related=False):
    assert paper in PAPERS, paper
    return {'paper': paper, 'label': label, 'related': related}


def see(deck, n, label):
    assert deck in DECKS, deck
    return {'deck': deck, 'n': n, 'label': label}

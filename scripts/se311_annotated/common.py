"""Constructors for SE311 annotated-slide content. The markup is the SE423 one (see se423_annotated/ch01_introduction.py)."""
from se423_annotated.common import mcq, scen, section, short, slide, tf, tip, trap, trick  # noqa: F401
from cs331_annotated.common import fig  # noqa: F401

# Every SE311 deck, in course order: key -> (annotated slug, standalone file, slides folder, label).
DECKS = {
    'd01': ('01-software-requirements-engineering-fundamentals', 'software-requirements-engineering-fundamentals', 'chapter-1-software-requirements-engineering-fundamentals', 'Chapter 1: Software Requirements Engineering Fundamentals'),
    'd02': ('02-requirements-inception', 'requirements-inception', 'chapter-2-requirements-inception', 'Chapter 2: Requirements Inception'),
    'd03': ('03-requirements-elicitation-process', 'requirements-elicitation-process', 'chapter-3-requirements-elicitation-process', 'Chapter 3: Requirements Elicitation Process'),
    'd04': ('04-requirements-elicitation-techniques', 'requirements-elicitation-techniques', 'chapter-4-requirements-elicitation-techniques', 'Chapter 4: Requirements Elicitation Techniques'),
    'd05': ('05-requirements-analysis-domain-modeling', 'requirements-analysis-domain-modeling', 'chapter-5-1-requirements-analysis-domain-modeling', 'Chapter 5.1: Requirements Analysis: Domain Modeling'),
    'd06': ('06-requirements-analysis', 'requirements-analysis', 'chapter-5-2-requirements-analysis', 'Chapter 5.2: Domain Model Exercise (Movie Shop)'),
    'd07': ('07-requirements-analysis', 'requirements-analysis', 'chapter-5-5-requirements-analysis', 'Chapter 5.5: Use-Case Model Exercise (Movie Shop)'),
    'd08': ('08-requirements-analysis', 'requirements-analysis', 'chapter-5-6-requirements-analysis', 'Chapter 5.6: Use-Case Detailed Specification'),
    'd09': ('09-writing-excellent-requirements', 'writing-excellent-requirements', 'chapter-6-writing-excellent-requirements', 'Chapter 6: Writing Excellent Requirements'),
    'd10': ('10-requirements-specification', 'requirements-specification', 'chapter-7-requirements-specification', 'Chapter 7: Requirements Specification'),
}

# The real SE311 papers in exams/.
PAPERS = {
    'q1': ('Quiz 1 (Ch. 1–3)', '08-quiz-1'),
}


def past(paper, label, related=False):
    assert paper in PAPERS, paper
    return {'paper': paper, 'label': label, 'related': related}


def see(deck, n, label):
    assert deck in DECKS, deck
    return {'deck': deck, 'n': n, 'label': label}

"""Constructors for CYS403 annotated-slide content. The markup is the SE423 one (see se423_annotated/ch01_introduction.py)."""
from se423_annotated.common import mcq, scen, section, short, slide, tf, tip, trap, trick  # noqa: F401
from cs331_annotated.common import fig  # noqa: F401

# Every CYS403 deck, in course order: key -> (annotated slug, standalone file, slides folder, label).
DECKS = {
    'd01': ('01-security-risk-management-governance-and-control', 'security-risk-management-governance-and-control', 'chapter-1-security-risk-management-governance-and-control', 'Chapter 1: Security Risk Management, Governance and Control'),
    'd02': ('02-risk-management-fundamentals', 'risk-management-fundamentals', 'chapter-2-risk-management-fundamentals', 'Chapter 2: Risk Management Fundamentals'),
    'd03': ('03-threat-and-vulnerability-management', 'threat-and-vulnerability-management', 'chapter-3-threat-and-vulnerability-management', 'Chapter 3: Threat and Vulnerability Management'),
    'd04': ('04-risk-management-lifecycle', 'risk-management-lifecycle', 'chapter-4-risk-management-lifecycle', 'Chapter 4: Risk Management Lifecycle'),
    'd05': ('05-risk-assessment-approaches', 'risk-assessment-approaches', 'chapter-5-risk-assessment-approaches', 'Chapter 5: Risk Assessment Approaches'),
    'd06': ('06-performing-risk-assessment', 'performing-risk-assessment', 'chapter-6-performing-risk-assessment', 'Chapter 6: Performing Risk Assessment'),
}

# The real CYS403 papers in exams/.
PAPERS = {
    'q222': ('Quiz 1, Term 222', '09-past-term-222-quiz-1'),
    'q2': ('Quiz 2', '10-past-term-unknown-quiz-2'),
    'major': ('Major exam', '11-past-term-unknown-major-exam'),
}


def past(paper, label, related=False):
    assert paper in PAPERS, paper
    return {'paper': paper, 'label': label, 'related': related}


def see(deck, n, label):
    assert deck in DECKS, deck
    return {'deck': deck, 'n': n, 'label': label}

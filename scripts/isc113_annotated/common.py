"""Constructors for ISC113 annotated-slide content. The markup is the SE423 one (see se423_annotated/ch01_introduction.py)."""
from se423_annotated.common import mcq, scen, section, short, slide, tf, tip, trap, trick  # noqa: F401
from cs331_annotated.common import fig  # noqa: F401

# Every ISC113 deck, in course order: key -> (annotated slug, standalone file, slides folder, label).
DECKS = {
    'd01': ('01-concept-and-definition-of-the-islamic-economy', 'concept-and-definition-of-the-islamic-economy', 'lecture-1', 'Lecture 1: Concept and Definition of the Islamic Economy'),
    'd02': ('02-islamic-capitalist-and-socialist-economic-systems', 'islamic-capitalist-and-socialist-economic-systems', 'lecture-2', 'Lecture 2: Islamic, Capitalist and Socialist Economic Systems'),
    'd03': ('03-prime-economic-terms', 'prime-economic-terms', 'lecture-3', 'Lecture 3: Prime Economic Terms'),
    'd04': ('04-the-state-budget-and-public-loans', 'the-state-budget-and-public-loans', 'lecture-4', 'Lecture 4: The State Budget and Public Loans'),
    'd05': ('05-public-revenues-and-expenditure-in-islam', 'public-revenues-and-expenditure-in-islam', 'lecture-5', 'Lecture 5: Public Revenues and Expenditure in Islam'),
    'd06': ('06-islam-and-the-economic-dilemma', 'islam-and-the-economic-dilemma', 'lecture-6', 'Lecture 6: Islam and the Economic Dilemma'),
    'd07': ('07-factors-of-production', 'factors-of-production', 'lecture-7', 'Lecture 7: Factors of Production'),
    'd08': ('08-consumption-and-consumer-conduct', 'consumption-and-consumer-conduct', 'lecture-8', 'Lecture 8: Consumption and Consumer Conduct'),
    'd09': ('09-the-market-in-islamic-economic-thought', 'the-market-in-islamic-economic-thought', 'lecture-9', 'Lecture 9: The Market in Islamic Economic Thought'),
    'd10': ('10-pricing-in-islam', 'pricing-in-islam', 'lecture-10', 'Lecture 10: Pricing in Islam'),
    'd11': ('11-money-and-its-rules-in-islam', 'money-and-its-rules-in-islam', 'lecture-11', 'Lecture 11: Money and Its Rules in Islam'),
    'd12': ('12-commercial-and-islamic-banks', 'commercial-and-islamic-banks', 'lecture-12', 'Lecture 12: Commercial and Islamic Banks'),
}

# The real ISC113 papers in exams/.
PAPERS = {
    'exam1': ('Exam 1', '01-exam-1'),
    'exam2': ('Exam 2', '02-exam-2'),
    'final': ('Final exam', '03-final-exam'),
}


def past(paper, label, related=False):
    assert paper in PAPERS, paper
    return {'paper': paper, 'label': label, 'related': related}


def see(deck, n, label):
    assert deck in DECKS, deck
    return {'deck': deck, 'n': n, 'label': label}

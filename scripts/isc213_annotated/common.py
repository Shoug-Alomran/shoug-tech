"""Constructors for ISC213 annotated-slide content. The markup is the SE423 one (see se423_annotated/ch01_introduction.py)."""
from se423_annotated.common import mcq, scen, section, short, slide, tf, tip, trap, trick  # noqa: F401
from cs331_annotated.common import fig  # noqa: F401

# Every ISC213 deck, in course order: key -> (annotated slug, standalone file, slides folder, label).
DECKS = {
    'd01': ('01-contemporary-financial-transactions', 'contemporary-financial-transactions', 'lecture-1', 'Lecture 1: Contemporary Financial Transactions'),
    'd02': ('02-researching-contemporary-cases-and-rights', 'researching-contemporary-cases-and-rights', 'lecture-2', 'Lecture 2: Researching Contemporary Cases and Rights'),
    'd03': ('03-incorporeal-rights-authorship-patents-and-trade-names', 'incorporeal-rights-authorship-patents-and-trade-names', 'lecture-3', 'Lecture 3: Incorporeal Rights: Authorship, Patents and Trade Names'),
    'd04': ('04-insurance', 'insurance', 'lecture-4', 'Lecture 4: Insurance'),
    'd05': ('05-securities-and-the-stock-market', 'securities-and-the-stock-market', 'lecture-5', 'Lecture 5: Securities and the Stock Market'),
    'd06': ('06-shares', 'shares', 'lecture-6', 'Lecture 6: Shares'),
    'd07': ('07-bonds', 'bonds', 'lecture-7', 'Lecture 7: Bonds'),
    'd08': ('08-lease-ending-with-ownership', 'lease-ending-with-ownership', 'lecture-8', 'Lecture 8: Lease Ending with Ownership'),
    'd09': ('09-murabaha-cost-plus-financing', 'murabaha-cost-plus-financing', 'lecture-9', 'Lecture 9: Murabaha (Cost-Plus Financing)'),
}

# The real ISC213 papers in exams/.
PAPERS = {
    'exam1': ('Exam 1', '01-exam-1'),
    'mid1': ('Midterm 1', '01-midterm-1'),
    'exam2': ('Exam 2', '02-exam-2'),
    'mid1c': ('Midterm 1 (comprehensive)', '02-midterm-1-comprehensive'),
    'final': ('Final exam', '03-final-exam'),
    'mid2': ('Midterm 2', '04-midterm-2'),
}


def past(paper, label, related=False):
    assert paper in PAPERS, paper
    return {'paper': paper, 'label': label, 'related': related}


def see(deck, n, label):
    assert deck in DECKS, deck
    return {'deck': deck, 'n': n, 'label': label}

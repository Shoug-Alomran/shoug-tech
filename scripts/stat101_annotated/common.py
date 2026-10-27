"""Constructors for STAT101 annotated-slide content. The markup is the SE423 one (see se423_annotated/ch01_introduction.py)."""
from se423_annotated.common import mcq, scen, section, short, slide, tf, tip, trap, trick  # noqa: F401
from cs331_annotated.common import fig  # noqa: F401

# Every STAT101 deck, in course order: key -> (annotated slug, standalone file, slides folder, label).
DECKS = {
    'd01': ('01-where-why-and-how-of-data-collection', 'where-why-and-how-of-data-collection', 'chapter-1.pdf', 'Chapter 1: The Where, Why and How of Data Collection'),
    'd02': ('02-graphs-charts-and-tables', 'graphs-charts-and-tables', 'chapter-2.pdf', 'Chapter 2: Graphs, Charts and Tables'),
    'd03': ('03-describing-data-using-numerical-measures', 'describing-data-using-numerical-measures', 'chapter-3.pdf', 'Chapter 3: Describing Data Using Numerical Measures'),
    'd04': ('04-introduction-to-probability', 'introduction-to-probability', 'chapter-4.pdf', 'Chapter 4: Introduction to Probability'),
    'd05': ('05-discrete-probability-distributions', 'discrete-probability-distributions', 'chapter-5.pdf', 'Chapter 5: Discrete Probability Distributions'),
    'd06': ('06-continuous-probability-distributions', 'continuous-probability-distributions', 'chapter-6.pdf', 'Chapter 6: Introduction to Continuous Probability Distributions'),
    'd07': ('07-sampling-distributions', 'sampling-distributions', 'chapter-7.pdf', 'Chapter 7: Introduction to Sampling Distributions'),
    'd08': ('08-estimating-population-parameters', 'estimating-population-parameters', 'chapter-8.pdf', 'Chapter 8: Estimating Single Population Parameters'),
    'd09': ('09-linear-regression-and-correlation', 'linear-regression-and-correlation', 'chapter-14.pdf', 'Chapter 14: Introduction to Linear Regression and Correlation Analysis'),
}

# The real STAT101 papers in exams/.
# exams/ holds per-chapter practice quizzes, not past papers.
PAPERS = {
}


def past(paper, label, related=False):
    assert paper in PAPERS, paper
    return {'paper': paper, 'label': label, 'related': related}


def see(deck, n, label):
    assert deck in DECKS, deck
    return {'deck': deck, 'n': n, 'label': label}

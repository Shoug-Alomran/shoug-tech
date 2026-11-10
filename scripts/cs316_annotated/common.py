"""Shared definitions for CS316 study content (annotated slides, breakdowns, mind maps, quizzes)."""
from se423_annotated.common import mcq, scen, section, short, slide, tf, tip, trap, trick  # noqa: F401
from cs331_annotated.common import fig  # noqa: F401

# Every CS316 deck in course order: key -> (annotated slug, file name, slides folder, label).
# d15 was added later; its folder number differs from its position, so URLs of the others stay put.
DECKS = {
    'd01': ('01-introduction-to-ai-and-data-science', 'introduction-to-ai-and-data-science',
            'chapter-1-introduction-to-ai-and-data-science', 'Chapter 1: Introduction to AI and Data Science'),
    'd02': ('02-pandas-for-data-analytics', 'pandas-for-data-analytics',
            'chapter-2-1-pandas-for-data-analytics', 'Chapter 2.1: Pandas for Data Analytics'),
    'd03': ('03-importing-summarizing-and-visualizing-data', 'importing-summarizing-and-visualizing-data',
            'chapter-2-2-importing-summarizing-and-visualizing-data', 'Chapter 2.2: Importing, Summarizing and Visualizing Data'),
    'd04': ('04-handling-missing-data', 'handling-missing-data',
            'chapter-2-3-handling-missing-data', 'Chapter 2.3: Handling Missing Data'),
    'd05': ('05-statistical-learning', 'statistical-learning',
            'chapter-3-statistical-learning', 'Chapter 3: Statistical Learning'),
    'd06': ('06-foundations-of-predictive-modeling', 'foundations-of-predictive-modeling',
            'chapter-4-foundations-of-predictive-modeling', 'Chapter 4: Foundations of Predictive Modeling'),
    'd07': ('07-classification-bayes-error-and-metrics', 'classification-bayes-error-and-metrics',
            'classification-part-1-bayes-error-and-metrics', 'Classification Part 1: Bayes Error and Metrics'),
    'd08': ('08-binary-classification', 'binary-classification',
            'classification-part-2-binary-classification', 'Classification Part 2: Binary Classification'),
    'd09': ('09-normalization-why-feature-scaling-matters', 'normalization-why-feature-scaling-matters',
            'normalization-why-feature-scaling-matters', 'Normalization: Why Feature Scaling Matters'),
    'd10': ('10-numpy-and-similarity-measures', 'numpy-and-similarity-measures',
            'chapter-7-1-numpy-and-similarity-measures', 'Chapter 7.1: NumPy and Similarity Measures'),
    'd11': ('11-dimensionality-reduction-with-pca', 'dimensionality-reduction-with-pca',
            'chapter-7-2-dimensionality-reduction-with-pca', 'Chapter 7.2: Dimensionality Reduction with PCA'),
    'd12': ('12-dimensionality-reduction-with-t-sne', 'dimensionality-reduction-with-t-sne',
            'chapter-7-3-dimensionality-reduction-with-t-sne', 'Chapter 7.3: Dimensionality Reduction with t-SNE'),
    'd15': ('15-cross-validation-and-grid-search', 'cross-validation-and-grid-search',
            'chapter-8-cross-validation-and-grid-search', 'Chapter 8: Cross-Validation and Grid Search'),
    'd13': ('13-fundamental-statistical-theorems', 'fundamental-statistical-theorems',
            'chapter-9-fundamental-statistical-theorems', 'Chapter 9: Fundamental Statistical Theorems'),
    'd14': ('14-hypothesis-testing', 'hypothesis-testing',
            'chapter-10-hypothesis-testing', 'Chapter 10: Hypothesis Testing'),
}

# No real CS316 papers are on the site yet; exams/ holds practice quizzes written from the slides.
PAPERS = {}


def N(note, tip=None, trap=None, trick=None, weight=None):
    """One slide's annotation: a note plus optional tip, trap and memory trick."""
    return {'note': note, 'tip': tip, 'trap': trap, 'trick': trick, 'weight': weight}


def Q(slide_no, question, correct, wrong, why):
    """A multiple-choice question tied to the slide it tests."""
    assert len(wrong) == 3, question
    return {'slide': slide_no, 'q': question, 'correct': correct, 'wrong': wrong, 'why': why}


def S(slide_no, question, keywords, answer):
    """A written question with the keywords the self-grader looks for."""
    return {'slide': slide_no, 'q': question, 'keywords': keywords, 'answer': answer}

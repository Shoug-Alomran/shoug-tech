"""Constructors for CS223 annotated-slide content. The markup is the SE423 one (see se423_annotated/ch01_introduction.py)."""
from se423_annotated.common import mcq, scen, section, short, slide, tf, tip, trap, trick  # noqa: F401
from cs331_annotated.common import fig  # noqa: F401

# Every CS223 deck, in course order: key -> (annotated slug, standalone file, slides folder, label).
DECKS = {
    'd02': ('02-ch1-lecture-2', 'ch1-lecture-2', 'ch1-lecture-2', '1.2 Row Reduction and Echelon Forms'),
    'd03': ('03-ch1-lecture-3', 'ch1-lecture-3', 'ch1-lecture-3', '1.3 Vector Equations'),
    'd04': ('04-ch1-lecture-4', 'ch1-lecture-4', 'ch1-lecture-4', '1.4 The Matrix Equation Ax = b'),
    'd05': ('05-ch1-lecture-5', 'ch1-lecture-5', 'ch1-lecture-5', '1.5 Linear Independence'),
    'd06': ('06-ch1-lecture-6', 'ch1-lecture-6', 'ch1-lecture-6', '1.6 Linear Transformations'),
    'd07': ('07-ch2-lecture-1', 'ch2-lecture-1', 'ch2-lecture-1', '2.1 Matrix Operations'),
    'd08': ('08-ch2-lecture-2', 'ch2-lecture-2', 'ch2-lecture-2', '2.2 The Inverse of a Matrix'),
    'd09': ('09-ch2-lecture-3', 'ch2-lecture-3', 'ch2-lecture-3', '2.3 LU Factorization'),
    'd10': ('10-ch2-lecture-4', 'ch2-lecture-4', 'ch2-lecture-4', '2.4 Subspaces of Rn'),
    'd11': ('11-ch3-lecture-1', 'ch3-lecture-1', 'ch3-lecture-1', '3.1 Introduction to Determinants'),
    'd12': ('12-ch3-lecture-2', 'ch3-lecture-2', 'ch3-lecture-2', '3.2 Properties of Determinants'),
    'd13': ('13-ch3-lecture-3', 'ch3-lecture-3', 'ch3-lecture-3', "3.3 Cramer's Rule and Volume"),
    'd14': ('14-ch4-lecture-1', 'ch4-lecture-1', 'ch4-lecture-1', '4.1 Vector Spaces and Subspaces'),
    'd15': ('15-ch4-lecture-2', 'ch4-lecture-2', 'ch4-lecture-2', '4.2 Dimension and Rank'),
    'd16': ('16-ch4-lecture-3', 'ch4-lecture-3', 'ch4-lecture-3', '4.3 Difference Equations'),
    'd17': ('17-ch5-lecture-1', 'ch5-lecture-1', 'ch5-lecture-1', '5.1 Eigenvectors and Eigenvalues'),
    'd18': ('18-ch5-lecture-2', 'ch5-lecture-2', 'ch5-lecture-2', '5.2 The Characteristic Equation'),
    'd19': ('19-ch5-lecture-3', 'ch5-lecture-3', 'ch5-lecture-3', '5.3 Diagonalization'),
    'd20': ('20-ch5-lecture-4', 'ch5-lecture-4', 'ch5-lecture-4', '5.4 Eigenvectors and Transformations'),
    'd21': ('21-ch5-lecture-5', 'ch5-lecture-5', 'ch5-lecture-5', '5.5 Complex Eigenvalues'),
    'd22': ('22-ch6-lecture-1', 'ch6-lecture-1', 'ch6-lecture-1', '6.1 Inner Product and Orthogonality'),
    'd23': ('23-ch6-lecture-2', 'ch6-lecture-2', 'ch6-lecture-2', '6.2 Orthogonal Sets'),
    'd24': ('24-ch6-lecture-3', 'ch6-lecture-3', 'ch6-lecture-3', '6.3 Projections, Gram-Schmidt, QR'),
    'd25': ('25-ch6-lecture-4', 'ch6-lecture-4', 'ch6-lecture-4', '6.4 Least-Squares Problems'),
    'd26': ('26-ch6-lecture-5', 'ch6-lecture-5', 'ch6-lecture-5', '6.5 Linear Models'),
    'd27': ('27-iterative-methods', 'iterative-methods', 'iterative-methods', 'Iterative Methods'),
}

# The real CS223 papers in exams/.
PAPERS = {
    'q242': ('Quiz 1 (242)', '01-quiz-1-242'),
    'm1': ('Major 1 (251)', '02-major-1-251'),
    'm2': ('Major 2 (251)', '03-major-2-251'),
    'f231': ('Final (231)', '04-final-231'),
    'f232': ('Final (232)', '05-final-232'),
    'sf': ('Sample final (223)', '06-sample-final-223'),
    'bank': ('Final review bank', '08-final-review-bank'),
}


def past(paper, label, related=False):
    assert paper in PAPERS, paper
    return {'paper': paper, 'label': label, 'related': related}


def see(deck, n, label):
    assert deck in DECKS, deck
    return {'deck': deck, 'n': n, 'label': label}

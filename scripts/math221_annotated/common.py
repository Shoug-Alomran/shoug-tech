"""Constructors for MATH221 annotated-slide content. The markup is the SE423 one (see se423_annotated/ch01_introduction.py)."""
from se423_annotated.common import mcq, scen, section, short, slide, tf, tip, trap, trick  # noqa: F401
from cs331_annotated.common import fig  # noqa: F401

# Every MATH221 deck, in course order: key -> (annotated slug, standalone file, slides folder, label).
DECKS = {
    'd01': ('01-review-of-calculus', 'review-of-calculus', '1-1', '1.1 Review of Calculus'),
    'd02': ('02-round-off-errors-computer-arithmetic-and-convergence', 'round-off-errors-computer-arithmetic-and-convergence', '1-2-1-3', '1.2–1.3 Round-off Errors, Computer Arithmetic and Convergence'),
    'd03': ('03-the-bisection-method', 'the-bisection-method', '2-1', '2.1 The Bisection Method'),
    'd04': ('04-newtons-method-and-its-extensions', 'newtons-method-and-its-extensions', '2-3', '2.3 Newton\'s Method and Its Extensions'),
    'd05': ('05-error-analysis-for-iterative-methods', 'error-analysis-for-iterative-methods', '2-4', '2.4 Error Analysis for Iterative Methods'),
    'd06': ('06-accelerating-convergence', 'accelerating-convergence', '2-5', '2.5 Accelerating Convergence'),
    'd07': ('07-interpolation-and-the-lagrange-polynomial', 'interpolation-and-the-lagrange-polynomial', '3-1', '3.1 Interpolation and the Lagrange Polynomial'),
    'd08': ('08-data-approximation-and-nevilles-method', 'data-approximation-and-nevilles-method', '3-2', '3.2 Data Approximation and Neville\'s Method'),
    'd09': ('09-divided-differences', 'divided-differences', '3-3', '3.3 Divided Differences'),
    'd10': ('10-hermite-interpolation', 'hermite-interpolation', '3-4', '3.4 Hermite Interpolation'),
    'd11': ('11-cubic-spline-interpolation', 'cubic-spline-interpolation', '3-5', '3.5 Cubic Spline Interpolation'),
    'd12': ('12-numerical-differentiation', 'numerical-differentiation', '4-1', '4.1 Numerical Differentiation'),
    'd13': ('13-elements-of-numerical-integration', 'elements-of-numerical-integration', '4-3', '4.3 Elements of Numerical Integration'),
    'd14': ('14-composite-numerical-integration', 'composite-numerical-integration', '4-4', '4.4 Composite Numerical Integration'),
    'd15': ('15-the-elementary-theory-of-initial-value-problems', 'the-elementary-theory-of-initial-value-problems', '5-1', '5.1 The Elementary Theory of Initial-Value Problems'),
    'd16': ('16-eulers-method', 'eulers-method', '5-2', '5.2 Euler\'s Method'),
    'd17': ('17-higher-order-taylor-methods', 'higher-order-taylor-methods', '5-3', '5.3 Higher-Order Taylor Methods'),
    'd18': ('18-linear-systems-of-equations', 'linear-systems-of-equations', '6-1', '6.1 Linear Systems of Equations'),
    'd19': ('19-pivoting-strategies', 'pivoting-strategies', '6-2', '6.2 Pivoting Strategies'),
    'd20': ('20-linear-algebra-and-matrix-inversion', 'linear-algebra-and-matrix-inversion', '6-3', '6.3 Linear Algebra and Matrix Inversion'),
    'd21': ('21-norms-of-vectors-and-matrices', 'norms-of-vectors-and-matrices', '7-1', '7.1 Norms of Vectors and Matrices'),
    'd22': ('22-eigenvalues-and-eigenvectors', 'eigenvalues-and-eigenvectors', '7-2', '7.2 Eigenvalues and Eigenvectors'),
    'd23': ('23-the-jacobi-and-gauss-seidel-iterative-techniques', 'the-jacobi-and-gauss-seidel-iterative-techniques', '7-3', '7.3 The Jacobi and Gauss–Seidel Iterative Techniques'),
}

# The real MATH221 papers in exams/.
PAPERS = {
}


def past(paper, label, related=False):
    assert paper in PAPERS, paper
    return {'paper': paper, 'label': label, 'related': related}


def see(deck, n, label):
    assert deck in DECKS, deck
    return {'deck': deck, 'n': n, 'label': label}

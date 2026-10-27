"""CS223 annotated slides — every Computational Linear Algebra lecture (Lay, Linear Algebra and Its Applications).

The decks are almost all handwritten-style math, so AUTO_SLIDES shows each slide as the original image and
the notes, tips and practice questions sit beside it. past(...) points at the past-paper pages in exams/
(related=True: the topic is examined there, not this exact slide). See cs331_annotated/ch01_1_introduction.py
for the ANN keys."""
from .common import DECKS, mcq, past, see, short, tf, tip, trap, trick


def deck(key, title, chapter, lede):
    slug, file, folder, label = DECKS[key]
    return {'key': key, 'slug': slug, 'file': file, 'title': title, 'chapter': chapter,
            'pdf': '/academics/math/cs223/slides/%s/' % folder, 'lede': lede}


def seen_in(*papers):
    return [past(p, 'this topic is examined', related=True) for p in papers]


IMT = ('Invertible Matrix Theorem (n×n A): A invertible ⇔ n pivots ⇔ A ~ I ⇔ Ax = 0 has only the trivial solution ⇔ columns '
       'linearly independent ⇔ columns span ℝⁿ ⇔ Ax = b has a unique solution for every b ⇔ det A ≠ 0 ⇔ 0 is not an eigenvalue ⇔ rank A = n.')


class row_reduction:
    AUTO_SLIDES = True
    DECK = deck('d02', 'Row Reduction and Echelon Forms', 'Chapter 1',
                'Echelon and reduced echelon form, pivot positions and columns, the row reduction algorithm, basic and '
                'free variables, parametric solutions, and existence and uniqueness of solutions.')
    ANN = {
        3: dict(notes=['Echelon form: zero rows at the bottom, each leading entry to the right of the one above, zeros below each leading entry. REDUCED: leading entries are 1 and are the only nonzero entries in their columns.'],
                tips=[trap('A matrix has many echelon forms but only ONE reduced echelon form.')],
                exam=[tf('Each matrix is row equivalent to exactly one reduced echelon matrix.', True, '')], weight=3),
        4: dict(notes=['Pivot position: location of a leading 1 in the reduced echelon form; pivot column: a column containing one.']),
        9: dict(notes=['Basic variables correspond to pivot columns; free variables to the others.']),
        11: dict(notes=['Write the general solution in parametric form: basic variables in terms of the free ones.']),
        13: dict(notes=['Existence and uniqueness: consistent ⇔ the last column of the augmented matrix is NOT a pivot column (no row [0 … 0 | b], b ≠ 0). If consistent: unique ⇔ no free variables; infinitely many ⇔ at least one free variable.'],
                 past=seen_in('m1'),
                 exam=[mcq('An augmented matrix reduces to a row [0 0 0 | 5]. The system is:', ['Inconsistent', 'Consistent with a unique solution', 'Consistent with infinitely many solutions', 'Homogeneous'], 0, ''),
                       mcq('A consistent system with 3 equations, 5 unknowns has:', ['Infinitely many solutions', 'Exactly one solution', 'No solution', 'Exactly two solutions'], 0, 'At least 2 free variables.')], weight=3),
    }


class vector_equations:
    AUTO_SLIDES = True
    DECK = deck('d03', 'Vector Equations', 'Chapter 1',
                'Vectors in ℝ², ℝ³ and ℝⁿ, the parallelogram rule, linear combinations, writing a system as a vector '
                'equation, Span{v₁, …, vₚ} and its geometric meaning.')
    ANN = {
        11: dict(notes=['y = c₁v₁ + … + cₚvₚ is a linear combination with weights c₁ … cₚ.']),
        13: dict(notes=['b is a linear combination of a₁, …, aₙ ⇔ the augmented matrix [a₁ … aₙ | b] is consistent.'],
                 exam=[short('How do you decide whether b is a linear combination of a₁ and a₂?', 'Row reduce [a₁ a₂ | b]. If the system is consistent (no row [0 0 | nonzero]), b is a linear combination and the solution gives the weights; otherwise it is not.')], weight=3),
        17: dict(notes=['Span{v} = a line through the origin; Span{u, v} (not parallel) = a plane through the origin.'],
                 exam=[tf('Span{u, v} always contains the zero vector.', True, '0 = 0u + 0v.')], weight=3),
        21: dict(notes=['The vector equation x₁a₁ + … + xₙaₙ = b, the matrix equation Ax = b and the augmented matrix all describe the same system.']),
    }


class matrix_equation:
    AUTO_SLIDES = True
    DECK = deck('d04', 'The Matrix Equation Ax = b and Solution Sets', 'Chapter 1',
                'The product Ax as a linear combination of A’s columns, the row-vector rule, properties of Ax, homogeneous '
                'systems and nontrivial solutions, and solution sets in parametric vector form (p + vₕ).')
    ANN = {
        2: dict(notes=['Ax = x₁a₁ + … + xₙaₙ (columns weighted by x). Defined only if A has as many columns as x has entries.']),
        5: dict(notes=['A(u + v) = Au + Av and A(cu) = c(Au).']),
        6: dict(notes=['For m×n A these are equivalent: Ax = b has a solution for EVERY b ⇔ columns span ℝᵐ ⇔ A has a pivot in every ROW.'],
                tips=[trap('Spanning ℝᵐ needs a pivot in every ROW; uniqueness needs a pivot in every COLUMN.')], weight=3),
        8: dict(notes=['Ax = 0 always has the trivial solution x = 0; it has a NONTRIVIAL solution ⇔ there is at least one free variable.'],
                exam=[mcq('A homogeneous system with more unknowns than equations:', ['Always has a nontrivial solution', 'Has only the trivial solution', 'Is inconsistent', 'Has exactly one solution'], 0, '')], weight=3),
        12: dict(notes=['If Ax = b is consistent with particular solution p, every solution is p + vₕ where vₕ solves Ax = 0 (the solution set is a translated null space).']),
    }


class independence:
    AUTO_SLIDES = True
    DECK = deck('d05', 'Linear Independence', 'Chapter 1',
                'Linear independence and dependence of vectors and of a matrix’s columns, special cases (one vector, two '
                'vectors, more vectors than entries, the zero vector).')
    ANN = {
        1: dict(notes=['{v₁, …, vₚ} is linearly independent ⇔ c₁v₁ + … + cₚvₚ = 0 only for c = 0 ⇔ Ax = 0 has only the trivial solution ⇔ a pivot in every column.'],
                past=seen_in('m1', 'f232'), weight=3),
        5: dict(notes=['Facts: a set containing 0 is dependent; two vectors are dependent ⇔ one is a multiple of the other; MORE vectors than entries (p > n) ⇒ dependent.'],
                tips=[trick('p vectors in ℝⁿ with p > n are always dependent.')],
                exam=[mcq('Four vectors in ℝ³ are:', ['Always linearly dependent', 'Always independent', 'Independent if none is zero', 'Cannot be decided'], 0, ''),
                      tf('If a set contains the zero vector, it is linearly dependent.', True, '')], weight=3),
    }


class transformations:
    AUTO_SLIDES = True
    DECK = deck('d06', 'Linear Transformations', 'Chapter 1',
                'Matrix transformations x ↦ Ax, domain, codomain and range, linearity and superposition, shear, '
                'rotation, reflection and projection examples, the standard matrix A = [T(e₁) … T(eₙ)], and one-to-one '
                'and onto transformations.')
    ANN = {
        2: dict(notes=['T: ℝⁿ → ℝᵐ, x ↦ Ax. Domain ℝⁿ, codomain ℝᵐ, range = set of all Ax (= Col A).']),
        12: dict(notes=['T is linear ⇔ T(u + v) = T(u) + T(v) and T(cu) = cT(u). Consequently T(0) = 0.'],
                 tips=[trick('Quick test: if T(0) ≠ 0, T is NOT linear.')],
                 exam=[mcq('Which map is NOT linear?', ['T(x) = x + (1, 0)', 'T(x) = 3x', 'T(x) = Ax', 'T(x) = 0'], 0, 'T(0) ≠ 0.')], weight=3),
        19: dict(notes=['Standard matrix: A = [T(e₁) T(e₂) … T(eₙ)], the images of the identity columns.'],
                 exam=[short('Find the standard matrix of the rotation of ℝ² by 90° counter-clockwise.', 'T(e₁) = (0, 1), T(e₂) = (−1, 0), so A = [[0, −1], [1, 0]].')], weight=3),
        24: dict(notes=['Geometric maps: reflections, contractions/expansions, shears, projections (see the tables).']),
        25: dict(notes=['Onto ℝᵐ ⇔ columns span ℝᵐ ⇔ pivot in every row. One-to-one ⇔ T(x) = 0 has only the trivial solution ⇔ columns independent ⇔ pivot in every column.'],
                 past=seen_in('m1'),
                 exam=[mcq('T: ℝ³ → ℝ² can never be:', ['One-to-one', 'Onto', 'Linear', 'Represented by a matrix'], 0, '3 columns in ℝ² are dependent.')], weight=3),
    }


class matrix_operations:
    AUTO_SLIDES = True
    DECK = deck('d07', 'Matrix Operations', 'Chapter 2',
                'Sums and scalar multiples, matrix multiplication as composition, the row–column rule, properties, '
                'powers and transposes.')
    ANN = {
        4: dict(notes=['AB = [Ab₁ … Abₚ]; defined when A is m×n and B is n×p, giving m×p. (AB)ᵢⱼ = row i of A · column j of B.'],
                tips=[trap('AB ≠ BA in general; AB = AC does not imply B = C; AB = 0 does not imply A = 0 or B = 0.')],
                exam=[mcq('A is 3×2 and B is 2×4. AB is:', ['3×4', '2×2', '4×3', 'undefined'], 0, '')], weight=3),
        10: dict(notes=['Transpose: (Aᵀ)ᵀ = A, (A + B)ᵀ = Aᵀ + Bᵀ, (AB)ᵀ = BᵀAᵀ (order reverses).'],
                 exam=[mcq('(AB)ᵀ equals:', ['BᵀAᵀ', 'AᵀBᵀ', 'AB', 'BA'], 0, '')], weight=3),
    }


class inverse:
    AUTO_SLIDES = True
    DECK = deck('d08', 'The Inverse of a Matrix', 'Chapter 2',
                'The 2×2 inverse formula, solving Ax = b with A⁻¹, properties of inverses, elementary matrices, the '
                'algorithm [A | I] ~ [I | A⁻¹], the Invertible Matrix Theorem and invertible linear transformations.')
    ANN = {
        2: dict(notes=['For A = [[a, b], [c, d]]: A⁻¹ = (1/(ad − bc))·[[d, −b], [−c, a]], when ad − bc ≠ 0.'],
                past=seen_in('m1', 'sf', 'bank'),
                exam=[mcq('The inverse of [[2, 1], [5, 3]] is:', ['[[3, −1], [−5, 2]]', '[[2, −1], [−5, 3]]', '[[3, 1], [5, 2]]', 'It does not exist'], 0, 'det = 1.')], weight=3),
        4: dict(notes=['(A⁻¹)⁻¹ = A, (AB)⁻¹ = B⁻¹A⁻¹, (Aᵀ)⁻¹ = (A⁻¹)ᵀ.'],
                tips=[trap('(AB)⁻¹ = B⁻¹A⁻¹: the order reverses.')], weight=3),
        6: dict(notes=['Algorithm: row reduce [A | I]. If A reduces to I, the right block is A⁻¹; otherwise A is not invertible.']),
        8: dict(notes=[IMT], tips=[tip(IMT)],
                exam=[tf('If A is n×n and Ax = 0 has a nontrivial solution, then A is invertible.', False, 'It is NOT invertible.')], weight=3),
    }


class lu:
    AUTO_SLIDES = True
    DECK = deck('d09', 'LU Factorization', 'Chapter 2',
                'Factoring A = LU (unit lower triangular L, echelon U), solving Ly = b then Ux = y, and the algorithm '
                'that builds L from the row-replacement multipliers.')
    ANN = {
        1: dict(notes=['A = LU with L unit lower triangular and U an echelon form of A. Solve Ax = b by Ly = b (forward substitution), then Ux = y (back substitution).'],
                exam=[mcq('After factoring A = LU, solving Ax = b takes:', ['Ly = b, then Ux = y', 'Ux = b, then Ly = x', 'Computing A⁻¹ first', 'Only Ux = b'], 0, '')], weight=3),
        3: dict(notes=['Row reduce A to U using only row REPLACEMENTS (adding multiples of rows above); L stores the multipliers with opposite sign below its unit diagonal.'],
                tips=[trick('If R2 → R2 − 3R1, put +3 in L at position (2, 1).')], weight=3),
    }


class subspaces:
    AUTO_SLIDES = True
    DECK = deck('d10', 'Subspaces of ℝⁿ', 'Chapter 2',
                'Subspaces, the column space and null space of a matrix, bases, finding bases for Col A (pivot columns of '
                'A) and Nul A (parametric solution of Ax = 0), coordinates, dimension and rank, and the Rank Theorem.')
    ANN = {
        1: dict(notes=['A subspace H of ℝⁿ contains 0 and is closed under addition and scalar multiplication.'],
                exam=[mcq('Which is a subspace of ℝ²?', ['A line through the origin', 'A line not through the origin', 'The first quadrant', 'The unit circle'], 0, '')], weight=3),
        6: dict(notes=['Col A: span of A’s columns (subspace of ℝᵐ). Nul A: all solutions of Ax = 0 (subspace of ℝⁿ).']),
        12: dict(notes=['dim Nul A = number of free variables; dim Col A = rank = number of pivot columns.'],
                 past=seen_in('m2', 'f232', 'bank')),
        15: dict(notes=['Basis of Col A: the pivot columns of the ORIGINAL A (not of its echelon form). Basis of Nul A: the vectors in the parametric solution of Ax = 0.'],
                 tips=[trap('Take the pivot columns from A itself, not from the reduced matrix.')], weight=3),
        19: dict(notes=['Rank Theorem: rank A + dim Nul A = n (number of columns).'],
                 exam=[mcq('A 5×7 matrix has rank 4. dim Nul A =', ['3', '1', '4', '2'], 0, '7 − 4.')], weight=3),
    }


class determinants:
    AUTO_SLIDES = True
    DECK = deck('d11', 'Introduction to Determinants', 'Chapter 3',
                'The 2×2 and 3×3 determinant, minors and cofactors, cofactor expansion along any row or column, and the '
                'determinant of a triangular matrix.')
    ANN = {
        4: dict(notes=['det A = Σ aᵢⱼCᵢⱼ along any row or column, with cofactor Cᵢⱼ = (−1)^(i+j) det Aᵢⱼ. Expand along the row/column with the most zeros.'],
                past=seen_in('m2', 'f231', 'sf'), weight=3),
        8: dict(notes=['Triangular matrix: det = product of the diagonal entries.'],
                exam=[mcq('det of [[2, 5, 1], [0, 3, 7], [0, 0, −1]] is:', ['−6', '6', '0', '−1'], 0, '2·3·(−1).')], weight=3),
    }


class det_properties:
    AUTO_SLIDES = True
    DECK = deck('d12', 'Properties of Determinants', 'Chapter 3',
                'How row operations change the determinant, computing det by row reduction, det A ≠ 0 ⇔ A invertible, '
                'det Aᵀ = det A and det(AB) = det A · det B.')
    ANN = {
        1: dict(notes=['Row replacement: det unchanged. Row interchange: det changes sign. Scaling a row by k: det multiplied by k.'],
                tips=[trick('Replace → same; Swap → minus; Scale by k → times k.')],
                exam=[mcq('If B is A with two rows swapped and det A = 5, det B =', ['−5', '5', '10', '0'], 0, '')], weight=3),
        8: dict(notes=['A is invertible ⇔ det A ≠ 0. det Aᵀ = det A. det(AB) = det A · det B. det(kA) = kⁿ det A for n×n A. det A⁻¹ = 1/det A.'],
                tips=[trap('det(A + B) ≠ det A + det B, and det(kA) = kⁿ·det A, not k·det A.')],
                exam=[mcq('A is 3×3 with det A = 2. det(2A) =', ['16', '4', '8', '2'], 0, '2³·2.')], weight=3),
    }


class cramer:
    AUTO_SLIDES = True
    DECK = deck('d13', "Cramer's Rule, the Inverse Formula, Area and Volume", 'Chapter 3',
                "Cramer's rule xᵢ = det Aᵢ(b) / det A, the adjugate formula A⁻¹ = adj A / det A, and determinants as "
                'areas and volumes, including how a linear transformation scales area.')
    ANN = {
        1: dict(notes=["Cramer's rule: xᵢ = det Aᵢ(b) / det A, where Aᵢ(b) replaces column i with b. A⁻¹ = (1/det A)·adj A, adj A = transpose of the cofactor matrix."],
                past=seen_in('m2'),
                exam=[short("Use Cramer's rule: 3x₁ − 2x₂ = 6, −5x₁ + 4x₂ = 8.", 'det A = 12 − 10 = 2. det A₁ = 6·4 − (−2)·8 = 40 → x₁ = 20. det A₂ = 3·8 − 6·(−5) = 54 → x₂ = 27.')], weight=3),
        5: dict(notes=['|det A| = area of the parallelogram (2×2) or volume of the parallelepiped (3×3) spanned by the columns. A transformation multiplies areas by |det A|.'],
                exam=[mcq('T(x) = Ax with det A = −3 maps a region of area 4 to area:', ['12', '−12', '4/3', '7'], 0, '')], weight=3),
    }


class vector_spaces:
    AUTO_SLIDES = True
    DECK = deck('d14', 'Vector Spaces, Subspaces, Bases and Coordinates', 'Chapter 4',
                'Vector space axioms and subspaces, spans as subspaces, null space, column space and row space, kernel '
                'and range of a linear transformation, spanning sets and bases, and coordinate vectors.')
    ANN = {
        10: dict(notes=['Span{v₁, …, vₚ} is always a subspace.']),
        15: dict(notes=['Kernel of T = Nul A; range of T = Col A.']),
        18: dict(notes=['Spanning Set Theorem: removing a vector that is a combination of the others doesn’t change the span; some subset is a basis.']),
        20: dict(notes=['Basis: a linearly independent spanning set. Col A: pivot columns of A. Row A: nonzero rows of an echelon form.'],
                 tips=[trap('Row space basis comes from the ECHELON form; column space basis from the ORIGINAL A.')],
                 past=seen_in('m2', 'f231', 'sf'), weight=3),
        23: dict(notes=['Coordinates: x = c₁b₁ + … + cₙbₙ ⇒ [x]_B = (c₁, …, cₙ); find them by solving P_B·c = x.']),
    }


class dimension_rank:
    AUTO_SLIDES = True
    DECK = deck('d15', 'Dimension and Rank', 'Chapter 4',
                'Dimension of a vector space, dimensions of Nul A, Col A and Row A, rank, the Rank Theorem, and rank in '
                'the Invertible Matrix Theorem.')
    ANN = {
        2: dict(notes=['dim H = number of vectors in any basis of H.']),
        5: dict(notes=['rank A = dim Col A = dim Row A = number of pivots. Rank Theorem: rank A + dim Nul A = n.'],
                past=seen_in('m2', 'f231', 'sf'),
                exam=[mcq('A 6×9 matrix has a 4-dimensional null space. Its rank is:', ['5', '4', '6', '3'], 0, '9 − 4.'),
                      tf('rank A = rank Aᵀ.', True, 'Row and column spaces have the same dimension.')], weight=3),
    }


class difference_equations:
    AUTO_SLIDES = True
    DECK = deck('d16', 'Applications to Difference Equations and Signals', 'Chapter 4',
                'Discrete-time signals, periodic signals, linear difference equations, and the solution space of a '
                'homogeneous linear difference equation.')
    ANN = {
        1: dict(notes=['A discrete signal is a sequence {yₖ}. A linear difference equation: a₀yₖ₊ₙ + … + aₙyₖ = zₖ.']),
        5: dict(notes=['Solutions of a homogeneous n-th order linear difference equation form an n-dimensional space; try yₖ = rᵏ to get the auxiliary equation.']),
    }


class eigen:
    AUTO_SLIDES = True
    DECK = deck('d17', 'Eigenvectors and Eigenvalues', 'Chapter 5',
                'Eigenvectors Ax = λx, checking eigenvalues by solving (A − λI)x = 0, eigenspaces, eigenvalues of '
                'triangular matrices, and independence of eigenvectors for distinct eigenvalues.')
    ANN = {
        2: dict(notes=['x ≠ 0 is an eigenvector of A with eigenvalue λ if Ax = λx. λ is an eigenvalue ⇔ (A − λI)x = 0 has a nontrivial solution.'],
                past=seen_in('f231', 'f232', 'sf', 'bank'),
                exam=[tf('The zero vector can be an eigenvector.', False, 'Eigenvectors are nonzero (but 0 can be an eigenvalue).')], weight=3),
        5: dict(notes=['Eigenspace of λ = Nul(A − λI); its dimension = number of free variables.']),
        7: dict(notes=['Eigenvalues of a triangular matrix are its diagonal entries. 0 is an eigenvalue ⇔ A is not invertible. Eigenvectors for distinct eigenvalues are linearly independent.'],
                exam=[mcq('The eigenvalues of [[3, 6, −8], [0, 0, 6], [0, 0, 2]] are:', ['3, 0, 2', '3, 6, −8', '0 only', '3, 6, 2'], 0, '')], weight=3),
    }


class characteristic:
    AUTO_SLIDES = True
    DECK = deck('d18', 'The Characteristic Equation', 'Chapter 5',
                'Determinants recalled, the characteristic equation det(A − λI) = 0, algebraic multiplicity, and '
                'similar matrices.')
    ANN = {
        3: dict(notes=['λ is an eigenvalue ⇔ det(A − λI) = 0 (the characteristic equation). Multiplicity as a root = algebraic multiplicity.'],
                exam=[short('Find the eigenvalues of A = [[2, 3], [3, −6]].', 'det(A − λI) = (2 − λ)(−6 − λ) − 9 = λ² + 4λ − 21 = (λ + 7)(λ − 3), so λ = 3 and λ = −7.')], weight=3),
        6: dict(notes=['Similar matrices (B = P⁻¹AP) have the same characteristic polynomial, hence the same eigenvalues.'],
                tips=[trap('Same eigenvalues does NOT imply similar; row-equivalent matrices usually have different eigenvalues.')], weight=3),
    }


class diagonalization:
    AUTO_SLIDES = True
    DECK = deck('d19', 'Diagonalization', 'Chapter 5',
                'A = PDP⁻¹ and fast powers Aᵏ = PDᵏP⁻¹, the Diagonalization Theorem (n independent eigenvectors), the '
                'step-by-step procedure, and when distinct eigenvalues guarantee diagonalizability.')
    ANN = {
        1: dict(notes=['A is diagonalizable ⇔ it has n linearly independent eigenvectors. Then A = PDP⁻¹: P’s columns are eigenvectors, D’s diagonal the matching eigenvalues. Aᵏ = PDᵏP⁻¹.'],
                past=seen_in('f231', 'f232', 'sf'),
                tips=[trick('n distinct eigenvalues ⇒ diagonalizable (sufficient, not necessary).')],
                exam=[tf('A 3×3 matrix with 3 distinct eigenvalues is diagonalizable.', True, ''),
                      tf('Every diagonalizable matrix is invertible.', False, '0 can be an eigenvalue.')], weight=3),
        5: dict(notes=['Steps: eigenvalues → basis of each eigenspace → if the total is n vectors, build P and D (same order).']),
    }


class eigen_transformations:
    AUTO_SLIDES = True
    DECK = deck('d20', 'Eigenvectors and Linear Transformations', 'Chapter 5',
                'The matrix of a linear transformation relative to bases, the B-matrix [T]_B = P⁻¹AP, and diagonal '
                'matrix representations.')
    ANN = {
        4: dict(notes=['The B-matrix of x ↦ Ax is [T]_B = P⁻¹AP where P has the basis vectors as columns. If B is an eigenvector basis, [T]_B is diagonal.']),
    }


class complex_eigen:
    AUTO_SLIDES = True
    DECK = deck('d21', 'Complex Eigenvalues and Dynamical Systems', 'Chapter 5',
                'Complex eigenvalues and eigenvectors in conjugate pairs, rotation–scaling matrices, long-term behaviour '
                'of xₖ₊₁ = Axₖ, population models and steady-state vectors.')
    ANN = {
        2: dict(notes=['For real A, complex eigenvalues come in conjugate pairs λ, λ̄ with eigenvectors x, x̄.']),
        4: dict(notes=['Long-term behaviour of xₖ = Aᵏx₀: write x₀ in the eigenvector basis; terms with |λ| > 1 grow, |λ| < 1 decay.']),
        15: dict(notes=['Steady-state vector of a stochastic (Markov) matrix P: Pq = q with entries summing to 1: solve (P − I)q = 0.'],
                 exam=[short('How do you find the steady-state vector of a stochastic matrix P?', 'Solve (P − I)x = 0, pick a nonzero solution, and scale it so its entries add up to 1.')], weight=3),
    }


class orthogonality:
    AUTO_SLIDES = True
    DECK = deck('d22', 'Inner Product, Length and Orthogonality', 'Chapter 6',
                'The dot product, length and unit vectors, distance, orthogonal vectors and the Pythagorean theorem, '
                'orthogonal complements, and (Row A)⊥ = Nul A.')
    ANN = {
        2: dict(notes=['u · v = uᵀv. ‖v‖ = √(v · v). Unit vector: v/‖v‖. dist(u, v) = ‖u − v‖.'],
                exam=[mcq('The length of v = (3, 4) is:', ['5', '7', '25', '12'], 0, '')], weight=3),
        5: dict(notes=['u ⊥ v ⇔ u · v = 0 ⇔ ‖u + v‖² = ‖u‖² + ‖v‖².']),
        7: dict(notes=['W⊥ = vectors orthogonal to every vector in W. (Row A)⊥ = Nul A and (Col A)⊥ = Nul Aᵀ.'],
                past=seen_in('f231', 'f232'), weight=3),
    }


class orthogonal_sets:
    AUTO_SLIDES = True
    DECK = deck('d23', 'Orthogonal Sets and Orthogonal Matrices', 'Chapter 6',
                'Orthogonal and orthonormal sets and bases, weights in an orthogonal basis cⱼ = (y · uⱼ)/(uⱼ · uⱼ), and '
                'matrices with orthonormal columns (UᵀU = I).')
    ANN = {
        1: dict(notes=['An orthogonal set of nonzero vectors is linearly independent. In an orthogonal basis, y = Σ cⱼuⱼ with cⱼ = (y · uⱼ)/(uⱼ · uⱼ): no row reduction needed.'], weight=3),
        4: dict(notes=['Orthonormal columns ⇔ UᵀU = I. A square such U is an orthogonal matrix: U⁻¹ = Uᵀ, and it preserves lengths and angles.'],
                exam=[mcq('For an orthogonal (square) matrix U, U⁻¹ equals:', ['Uᵀ', 'U', '−U', 'det(U)·U'], 0, '')], weight=3),
    }


class projections:
    AUTO_SLIDES = True
    DECK = deck('d24', 'Orthogonal Projections, Gram–Schmidt and QR', 'Chapter 6',
                'Orthogonal projection onto a subspace ŷ = Σ (y·uᵢ)/(uᵢ·uᵢ) uᵢ, the orthogonal decomposition y = ŷ + z, '
                'the best approximation theorem, the Gram–Schmidt process and the QR factorization.')
    ANN = {
        1: dict(notes=['Projection onto W with orthogonal basis {u₁, …, uₚ}: ŷ = Σ (y·uᵢ)/(uᵢ·uᵢ) uᵢ. Then z = y − ŷ ∈ W⊥, and ŷ is the closest point in W to y.'],
                past=seen_in('f231', 'sf'), weight=3),
        4: dict(notes=['Gram–Schmidt: v₁ = x₁, v₂ = x₂ − (x₂·v₁)/(v₁·v₁) v₁, v₃ = x₃ − proj onto v₁ − proj onto v₂ … then normalize for an orthonormal basis.'],
                past=seen_in('f232', 'bank'),
                exam=[short('Apply Gram–Schmidt to x₁ = (3, 6, 0), x₂ = (1, 2, 2).', 'v₁ = (3, 6, 0). x₂·v₁ = 15, v₁·v₁ = 45, so v₂ = (1, 2, 2) − (1/3)(3, 6, 0) = (0, 0, 2). Orthogonal basis {(3, 6, 0), (0, 0, 2)}.')], weight=3),
        7: dict(notes=['QR: A = QR, Q has orthonormal columns (Gram–Schmidt on A’s columns), R = QᵀA is upper triangular with positive diagonal.']),
    }


class least_squares:
    AUTO_SLIDES = True
    DECK = deck('d25', 'Least-Squares Problems', 'Chapter 6',
                'Least-squares solutions of inconsistent systems, the normal equations AᵀAx̂ = Aᵀb, uniqueness when the '
                'columns are independent, the least-squares error, and solving with QR.')
    ANN = {
        2: dict(notes=['Least-squares solution x̂ minimizes ‖b − Ax‖. Solve the normal equations AᵀAx̂ = Aᵀb. Unique ⇔ A’s columns are independent ⇔ AᵀA invertible: x̂ = (AᵀA)⁻¹Aᵀb.'],
                past=seen_in('f231', 'f232', 'sf'),
                tips=[tip('Least-squares error = ‖b − Ax̂‖.')],
                exam=[mcq('The least-squares solutions of Ax = b are the solutions of:', ['AᵀAx = Aᵀb', 'Ax = b', 'AAᵀx = b', 'Aᵀx = b'], 0, '')], weight=3),
        6: dict(notes=['With A = QR: Rx̂ = Qᵀb (more stable numerically).']),
    }


class linear_models:
    AUTO_SLIDES = True
    DECK = deck('d26', 'Applications to Linear Models', 'Chapter 6',
                'Regression as least squares: the design matrix X, parameter vector β and observation vector y, the '
                'least-squares line y = β₀ + β₁x, residuals, and fitting other curves.')
    ANN = {
        1: dict(notes=['Linear model y = Xβ + ε. Least-squares line: X has a column of 1s and a column of x values; solve XᵀXβ = Xᵀy.'],
                exam=[short('Set up the design matrix for fitting y = β₀ + β₁x to points (2, 1), (5, 2), (7, 3).', 'X = [[1, 2], [1, 5], [1, 7]], y = (1, 2, 3); solve XᵀXβ = Xᵀy.')], weight=3),
        4: dict(notes=['Other curves (e.g. y = β₀ + β₁x + β₂x²) are still LINEAR in the parameters: add a column for x².']),
    }


class iterative:
    AUTO_SLIDES = True
    DECK = deck('d27', 'Iterative Methods for Linear Systems', 'Iterative Methods',
                'Why iterative methods for large sparse systems, convergence and diagonal dominance, the Jacobi and '
                'Gauss–Seidel methods with worked examples, and successive over-relaxation (SOR).')
    ANN = {
        3: dict(notes=['Iterative methods start from a guess and improve it; good for large sparse systems where elimination is too costly.']),
        12: dict(notes=['Strictly diagonally dominant: |aᵢᵢ| > Σ_{j≠i} |aᵢⱼ| in every row. Then Jacobi and Gauss–Seidel converge for any starting vector.'],
                 exam=[mcq('Which matrix is strictly diagonally dominant?', ['[[4, 1], [2, 5]]', '[[1, 3], [2, 1]]', '[[2, 2], [1, 3]]', '[[1, 1], [1, 1]]'], 0, '')], weight=3),
        15: dict(notes=['Jacobi: xᵢ⁽ᵏ⁺¹⁾ = (bᵢ − Σ_{j≠i} aᵢⱼxⱼ⁽ᵏ⁾)/aᵢᵢ: every component uses the OLD vector.']),
        19: dict(notes=['Gauss–Seidel: same formula but uses each NEW component as soon as it is computed; usually converges faster.'],
                 tips=[trick('Jacobi = all old values; Gauss–Seidel = newest values immediately.')],
                 exam=[short('One Jacobi step for 4x − y = 3, x + 5y = 6 from (0, 0).', 'x = (3 + y)/4 = 0.75, y = (6 − x)/5 = 1.2 using the old x = 0, so (0.75, 1.2). (Gauss–Seidel would use x = 0.75: y = (6 − 0.75)/5 = 1.05.)')], weight=3),
        23: dict(notes=['SOR: Gauss–Seidel with a relaxation factor ω (1 < ω < 2 over-relaxes to speed convergence; ω = 1 is Gauss–Seidel).']),
    }


DECKS_HERE = [row_reduction, vector_equations, matrix_equation, independence, transformations, matrix_operations, inverse, lu,
              subspaces, determinants, det_properties, cramer, vector_spaces, dimension_rank, difference_equations, eigen,
              characteristic, diagonalization, eigen_transformations, complex_eigen, orthogonality, orthogonal_sets,
              projections, least_squares, linear_models, iterative]

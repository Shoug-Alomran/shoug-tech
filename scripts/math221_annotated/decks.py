"""MATH221 annotated slides — every numerical-methods section deck (Burden & Faires, Numerical Analysis).

The decks are scanned or hand-worked slides with little or no text layer, so every slide is shown as the
original image (whole=True) and the notes, tips and practice questions sit beside it. Each deck is a
namespace class built by section(); see cs331_annotated/ch01_1_introduction.py for the ANN keys."""
from .common import DECKS, mcq, see, short, tf, tip, trap, trick


def section(key, chapter, count, lede, ann):
    slug, file, folder, label = DECKS[key]
    title = label.split(' ', 1)[1]
    return type(key, (), {
        'AUTO_SLIDES': True,
        'DECK': {'key': key, 'slug': slug, 'file': file, 'title': title, 'chapter': chapter,
                 'pdf': '/academics/math/math221/slides/%s/' % folder, 'lede': lede},
        'ANN': {n: dict(ann.get(n, {}), whole=True) for n in range(1, count + 1)},
    })


calculus = section('d01', 'Chapter 1', 3, 'Continuity, the Intermediate and Mean Value Theorems, and Taylor polynomials with their remainder.', {
    1: dict(notes=['Intermediate Value Theorem: f continuous on [a, b] and K between f(a) and f(b) ⇒ some c in (a, b) has f(c) = K. It is why bisection works.',
                   'Taylor: f(x) = Pₙ(x) + Rₙ(x), Rₙ(x) = f⁽ⁿ⁺¹⁾(ξ)(x − x₀)ⁿ⁺¹/(n + 1)!'],
            exam=[mcq('The theorem that guarantees a root of a continuous f on [a, b] when f(a)·f(b) < 0 is the:', ['Intermediate Value Theorem', 'Mean Value Theorem', 'Rolle’s Theorem', 'Taylor’s Theorem'], 0, '')], weight=3),
})

roundoff = section('d02', 'Chapter 1', 8, 'Floating-point representation, chopping vs. rounding, absolute and relative error, significant digits, loss of significance, and rates of convergence.', {
    2: dict(notes=['k-digit chopping drops extra digits; rounding rounds the k-th digit.', 'Absolute error |p − p*|; relative error |p − p*| / |p|.'],
            tips=[trap('Relative error divides by the TRUE value p, not the approximation.')],
            exam=[mcq('p = 3.1416, p* = 3.14. The relative error is about:', ['5.1 × 10⁻⁴', '1.6 × 10⁻³', '0.0016', '3.14'], 0, '0.0016 / 3.1416.')], weight=3),
    5: dict(notes=['Subtracting nearly equal numbers loses significant digits; rewrite the formula (e.g. rationalize) to avoid it.']),
})

bisection = section('d03', 'Chapter 2', 8, 'The bisection method: halving [a, b] on the sign change, stopping criteria and the error bound |pₙ − p| ≤ (b − a)/2ⁿ.', {
    1: dict(notes=['Bisection: pₙ = (aₙ + bₙ)/2; keep the half where f changes sign. Always converges (slowly, linearly).'],
            tips=[tip('Error bound: |pₙ − p| ≤ (b − a)/2ⁿ. To reach tolerance ε, need n ≥ log₂((b − a)/ε).')],
            exam=[mcq('How many bisection steps on [1, 2] guarantee an error below 10⁻³?', ['10', '3', '7', '1000'], 0, '2⁻ⁿ < 10⁻³ ⇒ n ≥ 10.'),
                  short('Do one bisection step for f(x) = x³ + 4x² − 10 on [1, 2].', 'f(1) = −5 < 0, f(2) = 14 > 0. p₁ = 1.5, f(1.5) = 2.375 > 0, so the root is in [1, 1.5].')], weight=3),
})

newton = section('d04', 'Chapter 2', 19, "Newton–Raphson, the secant method and the method of false position (regula falsi): formulas, worked examples and how they compare.", {
    3: dict(notes=['Newton: pₙ = pₙ₋₁ − f(pₙ₋₁)/f′(pₙ₋₁). Quadratic convergence near a simple root, but needs f′ and a good starting point.'],
            exam=[short('One Newton step for f(x) = x² − 2 from p₀ = 1.', 'p₁ = 1 − (1 − 2)/(2·1) = 1.5.')], weight=3),
    10: dict(notes=['Secant: replaces f′ with the slope through the last two points: pₙ = pₙ₋₁ − f(pₙ₋₁)(pₙ₋₁ − pₙ₋₂)/(f(pₙ₋₁) − f(pₙ₋₂)). No derivative needed.']),
    12: dict(notes=['False position: secant formula but keeps the two points that bracket the root (like bisection), so it always converges.'],
             tips=[trick('Newton needs f′; secant drops f′; false position = secant + bracketing.')],
             exam=[mcq('Which method keeps the root bracketed at every step?', ['False position', 'Secant', 'Newton', 'Fixed-point iteration'], 0, '')], weight=3),
})

error_analysis = section('d05', 'Chapter 2', 14, 'Order of convergence (linear vs. quadratic, asymptotic error constant), multiple roots and the modified Newton method.', {
    3: dict(notes=['Order α: |pₙ₊₁ − p| / |pₙ − p|^α → λ. α = 1 linear, α = 2 quadratic.'],
            exam=[mcq('Newton’s method near a simple root converges:', ['Quadratically', 'Linearly', 'Cubically', 'It doesn’t converge'], 0, '')], weight=3),
    12: dict(notes=['At a multiple root Newton is only linear; modified Newton uses μ = f/f′: pₙ = pₙ₋₁ − f f′/((f′)² − f f″).']),
})

acceleration = section('d06', 'Chapter 2', 23, "Aitken's Δ² method and Steffensen's method for accelerating linearly convergent sequences.", {
    2: dict(notes=["Aitken's Δ²: p̂ₙ = pₙ − (pₙ₊₁ − pₙ)² / (pₙ₊₂ − 2pₙ₊₁ + pₙ)."], weight=3),
    19: dict(notes=["Steffensen: apply Aitken to fixed-point iterates every third step: quadratic convergence without derivatives."],
             exam=[mcq("Steffensen's method accelerates:", ['Fixed-point iteration', 'Bisection', 'Euler’s method', 'Gaussian elimination'], 0, '')], weight=3),
})

lagrange = section('d07', 'Chapter 3', 14, 'Interpolation and the Lagrange interpolating polynomial, its error formula, and worked examples.', {
    2: dict(notes=['Lagrange: P(x) = Σ f(xₖ)Lₖ(x), Lₖ(x) = Π_{i≠k} (x − xᵢ)/(xₖ − xᵢ). Degree ≤ n through n + 1 points.',
                   'Error: f(x) − P(x) = f⁽ⁿ⁺¹⁾(ξ)/(n + 1)! · Π(x − xᵢ).'],
            exam=[short('Find the linear Lagrange polynomial through (2, 4) and (5, 1).', 'P(x) = 4(x − 5)/(2 − 5) + 1(x − 2)/(5 − 2) = −(4/3)(x − 5) + (1/3)(x − 2) = −x + 6.')], weight=3),
})

neville = section('d08', 'Chapter 3', 12, "Neville's method: building interpolating values recursively in a table.", {
    2: dict(notes=["Neville: Q_{i,j} = ((x − x_{i−j})Q_{i,j−1} − (x − xᵢ)Q_{i−1,j−1}) / (xᵢ − x_{i−j}). Good for evaluating P at ONE x."], weight=3),
})

divided = section('d09', 'Chapter 3', 8, "Newton's divided differences, the divided-difference table, and Newton's forward- and backward-difference formulas.", {
    2: dict(notes=['f[xᵢ, xᵢ₊₁] = (f[xᵢ₊₁] − f[xᵢ])/(xᵢ₊₁ − xᵢ), and so on. Pₙ(x) = f[x₀] + f[x₀, x₁](x − x₀) + f[x₀, x₁, x₂](x − x₀)(x − x₁) + …'],
            tips=[trick('Adding a new point only adds one new term: no need to start over (unlike Lagrange).')],
            exam=[mcq('With f(1) = 2, f(2) = 5, the first divided difference f[1, 2] is:', ['3', '7', '2.5', '1'], 0, '')], weight=3),
    4: dict(notes=['Equally spaced nodes: forward differences Δ and the binomial-coefficient form.']),
})

hermite = section('d10', 'Chapter 3', 9, 'Hermite interpolation: matching both function values and derivatives, built with repeated nodes in a divided-difference table.', {
    1: dict(notes=['Hermite polynomial agrees with f AND f′ at the nodes; degree ≤ 2n + 1. Use the divided-difference table with each node listed twice and f[zᵢ, zᵢ₊₁] = f′(xᵢ) where they repeat.'], weight=3),
})

splines = section('d11', 'Chapter 3', 22, 'Cubic spline interpolation: piecewise cubics with continuous first and second derivatives, natural vs. clamped boundary conditions, and solving for the coefficients.', {
    1: dict(notes=['Cubic spline: Sⱼ(x) = aⱼ + bⱼ(x − xⱼ) + cⱼ(x − xⱼ)² + dⱼ(x − xⱼ)³ on each subinterval; S, S′, S″ continuous.']),
    4: dict(notes=['Natural spline: S″(x₀) = S″(xₙ) = 0.']),
    8: dict(notes=['Clamped spline: S′(x₀) = f′(x₀), S′(xₙ) = f′(xₙ) (usually more accurate).'],
            exam=[mcq('A natural cubic spline satisfies at the endpoints:', ['S″ = 0', 'S′ = 0', 'S = 0', 'S′ = f′'], 0, '')], weight=3),
})

differentiation = section('d12', 'Chapter 4', 15, 'Numerical differentiation: forward/backward differences, three- and five-point endpoint and midpoint formulas, and the second-derivative midpoint formula.', {
    3: dict(notes=['Three-point endpoint: f′(x₀) ≈ (−3f(x₀) + 4f(x₀ + h) − f(x₀ + 2h))/(2h).']),
    4: dict(notes=['Three-point midpoint: f′(x₀) ≈ (f(x₀ + h) − f(x₀ − h))/(2h), error O(h²).'],
            exam=[mcq('The three-point midpoint formula for f′(x₀) is:', ['(f(x₀+h) − f(x₀−h))/(2h)', '(f(x₀+h) − f(x₀))/h', '(f(x₀+h) − 2f(x₀) + f(x₀−h))/h²', '(f(x₀) − f(x₀−h))/h'], 0, '')], weight=3),
    8: dict(notes=['Second derivative midpoint: f″(x₀) ≈ (f(x₀ − h) − 2f(x₀) + f(x₀ + h))/h².']),
})

integration = section('d13', 'Chapter 4', 13, "Elements of numerical integration: the trapezoidal rule and Simpson's rule with their error terms, degree of precision, and Newton–Cotes formulas.", {
    3: dict(notes=['Trapezoidal: ∫ₐᵇ f ≈ (h/2)(f(a) + f(b)), h = b − a; exact for degree ≤ 1.', "Simpson's: ∫ ≈ (h/3)(f(x₀) + 4f(x₁) + f(x₂)), h = (b − a)/2; exact for degree ≤ 3."],
            tips=[trap("Simpson's rule has degree of precision 3, not 2.")],
            exam=[mcq("Simpson's rule for ∫₀² x² dx gives:", ['8/3 (exact)', '4', '2', '3'], 0, '(1/3)(0 + 4·1 + 4) = 8/3.')], weight=3),
})

composite = section('d14', 'Chapter 4', 4, "Composite trapezoidal and Simpson's rules over n subintervals.", {
    1: dict(notes=['Composite trapezoidal: (h/2)[f(a) + 2Σf(xⱼ) + f(b)]. Composite Simpson (n even): (h/3)[f(a) + 4Σ odd + 2Σ even + f(b)].'],
            exam=[mcq("Composite Simpson's rule requires the number of subintervals n to be:", ['Even', 'Odd', 'Prime', 'Any'], 0, '')], weight=3),
})

ivp_theory = section('d15', 'Chapter 5', 5, 'Initial-value problems y′ = f(t, y), y(a) = α: Lipschitz conditions, existence and uniqueness, and well-posed problems.', {
    2: dict(notes=['f satisfies a Lipschitz condition in y if |f(t, y₁) − f(t, y₂)| ≤ L|y₁ − y₂|; then the IVP has a unique solution and is well-posed.']),
})

euler = section('d16', 'Chapter 5', 6, "Euler's method wᵢ₊₁ = wᵢ + h f(tᵢ, wᵢ) and its error.", {
    2: dict(notes=["Euler: w₀ = α, wᵢ₊₁ = wᵢ + h·f(tᵢ, wᵢ). First order: global error O(h)."],
            exam=[short("Use Euler with h = 0.5 for y′ = y − t² + 1, y(0) = 0.5. Find w₁.", 'w₁ = 0.5 + 0.5·(0.5 − 0 + 1) = 1.25.')], weight=3),
})

taylor = section('d17', 'Chapter 5', 9, 'Higher-order Taylor methods (order 2 and beyond) using derivatives of f.', {
    2: dict(notes=['Taylor order 2: wᵢ₊₁ = wᵢ + h[f(tᵢ, wᵢ) + (h/2) f′(tᵢ, wᵢ)], where f′ = df/dt along the solution. Local error O(h³), global O(h²).'], weight=3),
})

linear_systems = section('d18', 'Chapter 6', 18, 'Linear systems: augmented matrices, Gaussian elimination with backward substitution, and operation counts.', {
    1: dict(notes=['Gaussian elimination: reduce to upper triangular, then back-substitute. About n³/3 multiplications/divisions.'],
            exam=[mcq('Gaussian elimination on an n×n system takes on the order of:', ['n³ operations', 'n operations', 'n² operations', '2ⁿ operations'], 0, '')], weight=3),
})

pivoting = section('d19', 'Chapter 6', 5, 'Pivoting strategies: partial pivoting, scaled partial pivoting and why small pivots cause round-off errors.', {
    1: dict(notes=['Partial pivoting: swap so the LARGEST |entry| in the column is the pivot. Scaled partial pivoting: compare |aᵢₖ|/sᵢ, sᵢ = largest |entry| in row i.'],
            tips=[trap('A tiny pivot multiplies round-off errors: that’s why we pivot.')], weight=3),
})

inversion = section('d20', 'Chapter 6', 2, 'Matrix algebra and inversion: nonsingular matrices and computing inverses.', {
    2: dict(notes=['A is nonsingular ⇔ A⁻¹ exists ⇔ det A ≠ 0 ⇔ Ax = 0 has only x = 0.']),
})

norms = section('d21', 'Chapter 7', 6, 'Vector norms (l₁, l₂, l∞), distances and matrix norms.', {
    2: dict(notes=['‖x‖∞ = max |xᵢ|; ‖x‖₂ = √(Σxᵢ²); ‖x‖₁ = Σ|xᵢ|. Matrix ∞-norm = maximum absolute ROW sum.'],
            exam=[mcq('‖(1, −4, 2)‖∞ =', ['4', '7', '√21', '2'], 0, ''),
                  mcq('The ∞-norm of [[1, −2], [3, 4]] is:', ['7', '6', '4', '10'], 0, 'Max row sum: |3| + |4|.')], weight=3),
})

eigen = section('d22', 'Chapter 7', 10, 'Eigenvalues and eigenvectors, the spectral radius, and convergent matrices.', {
    2: dict(notes=['Spectral radius ρ(A) = max |λ|. ‖A‖₂ = √ρ(AᵀA). A is convergent (Aᵏ → 0) ⇔ ρ(A) < 1.'], weight=3),
})

jacobi = section('d23', 'Chapter 7', 11, 'The Jacobi and Gauss–Seidel iterative techniques and their convergence.', {
    2: dict(notes=['Jacobi: xᵢ⁽ᵏ⁾ = (bᵢ − Σ_{j≠i} aᵢⱼxⱼ⁽ᵏ⁻¹⁾)/aᵢᵢ (all old values).']),
    4: dict(notes=['Gauss–Seidel: uses the newest values as soon as they are computed; usually faster. Both converge if A is strictly diagonally dominant.'],
            tips=[trick('Jacobi = old values; Gauss–Seidel = newest values.')],
            exam=[short('One Gauss–Seidel step for 10x − y = 9, −x + 10y = 9 from (0, 0).', 'x = (9 + 0)/10 = 0.9; y = (9 + 0.9)/10 = 0.99.')], weight=3),
})

DECKS_HERE = [calculus, roundoff, bisection, newton, error_analysis, acceleration, lagrange, neville, divided, hermite, splines,
              differentiation, integration, composite, ivp_theory, euler, taylor, linear_systems, pivoting, inversion, norms, eigen, jacobi]

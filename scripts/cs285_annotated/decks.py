"""CS285 annotated slides — every Discrete Mathematics deck (Rosen chapters 1, 2, 4, 5, 6, 8, 9).

One module holds all the decks: each deck is a namespace class with DECK and ANN (and AUTO_SLIDES,
because the decks are full of formulas and tables that read best as the original slide). Slides
without an ANN entry are shown without notes. See cs331_annotated/ch01_1_introduction.py for the ANN keys."""
from .common import DECKS, mcq, see, short, tf, tip, trap, trick


def deck(key, title, chapter, lede):
    slug, file, folder, _ = DECKS[key]
    return {'key': key, 'slug': slug, 'file': file, 'title': title, 'chapter': chapter,
            'pdf': '/academics/computer-science/cs285/slides/%s/' % folder, 'lede': lede}


IMPLIES = 'p → q is FALSE only when p is true and q is false. Same as ¬p ∨ q, and as its contrapositive ¬q → ¬p.'


class logic:
    AUTO_SLIDES = True
    DECK = deck('d01', 'Logic and Proofs', 'Chapter 1',
                'Propositions and connectives, truth tables, implication and its converse / inverse / contrapositive, '
                'translating English, consistent specifications, logical equivalences and De Morgan, satisfiability, '
                'predicates and quantifiers (and negating them), nested quantifiers, and the rules of inference '
                'including resolution.')
    ANN = {
        2: dict(notes=['1.1–1.3 propositional logic and equivalences · 1.4–1.5 predicates and quantifiers · 1.6 rules of inference.'],
                tips=[tip(IMPLIES)]),
        8: dict(notes=['A proposition is a declarative sentence that is either true or false, not both. Questions, commands and "x + 1 = 2" (x unknown) are NOT propositions.'],
                exam=[mcq('Which of these is a proposition?', ['5 + 2 = 8', 'What time is it?', 'Close the door.', 'x + 1 = 2'], 0, 'It is false, but it is still a declarative sentence with a truth value.')], weight=3),
        10: dict(notes=['p ∧ q (and) is true only when both are true.']),
        11: dict(notes=['p ∨ q (inclusive or) is false only when both are false.']),
        12: dict(notes=['English "or" can be inclusive (∨) or exclusive (⊕: exactly one true).'],
                 exam=[mcq('p ⊕ q is true when:', ['Exactly one of p, q is true', 'Both are true', 'Both are false', 'At least one is true'], 0, '')], weight=2),
        14: dict(notes=[IMPLIES, 'Readings: "if p then q", "p only if q", "q whenever p", "q is necessary for p", "p is sufficient for q".'],
                 tips=[trap('"p only if q" is p → q, NOT q → p.')],
                 exam=[mcq('When is p → q false?', ['p true, q false', 'p false, q true', 'Both false', 'Both true'], 0, ''),
                       tf('If p is false, p → q is true no matter what q is.', True, 'A false hypothesis makes the implication vacuously true.')], weight=3),
        18: dict(notes=['From p → q: converse q → p, inverse ¬p → ¬q, contrapositive ¬q → ¬p.', 'Only the contrapositive is equivalent to the original; the converse and inverse are equivalent to each other.'],
                 tips=[trick('CONtrapositive = CONverse + inverse together (swap AND negate).')],
                 exam=[mcq('The contrapositive of "If it rains, then I stay home" is:', ['If I don’t stay home, then it doesn’t rain', 'If I stay home, then it rains', 'If it doesn’t rain, then I don’t stay home', 'It rains and I don’t stay home'], 0, ''),
                       tf('An implication is logically equivalent to its converse.', False, 'It is equivalent to its contrapositive.')], weight=3),
        21: dict(notes=['p ↔ q is true when p and q have the SAME truth value ("if and only if", "necessary and sufficient").'],
                 exam=[mcq('p ↔ q is equivalent to:', ['(p → q) ∧ (q → p)', '(p → q) ∨ (q → p)', 'p ⊕ q', '¬p ∨ q'], 0, '')], weight=3),
        22: dict(notes=['p ↔ q is the negation of p ⊕ q.']),
        24: dict(notes=['A compound proposition with n variables has 2ⁿ rows in its truth table.'],
                 exam=[mcq('How many rows does the truth table of a proposition with 4 variables have?', ['16', '8', '4', '32'], 0, '2⁴ = 16.')], weight=3),
        32: dict(notes=['Precedence: ¬ first, then ∧, then ∨, then →, then ↔. So p ∨ q → ¬r means (p ∨ q) → (¬r).'],
                 exam=[mcq('p ∧ q ∨ r is read as:', ['(p ∧ q) ∨ r', 'p ∧ (q ∨ r)', '(p ∨ r) ∧ q', 'It is ambiguous'], 0, '∧ binds tighter than ∨.')], weight=3),
        36: dict(notes=['Translate: pick atomic propositions, then join them with connectives. "You can access the Internet only if you are a CS major or not a freshman" → a → (c ∨ ¬f).'], weight=2),
        39: dict(notes=['A set of specifications is consistent if ONE assignment of truth values makes all of them true at the same time.'],
                 exam=[short('How do you check that a list of system specifications is consistent?', 'Translate each into propositional logic and look for one truth assignment (a row of the truth table) that makes every specification true at once. If such a row exists the specs are consistent; if none exists they are inconsistent.')], weight=3),
        44: dict(notes=['Logic gates: inverter (¬), AND (∧), OR (∨); circuits compute compound propositions.']),
        47: dict(notes=['Tautology: always true (p ∨ ¬p). Contradiction: always false (p ∧ ¬p). Contingency: neither.'],
                 exam=[mcq('p ∨ ¬p is a:', ['Tautology', 'Contradiction', 'Contingency', 'Biconditional'], 0, ''),
                       mcq('(p → q) ∧ p ∧ ¬q is a:', ['Contradiction', 'Tautology', 'Contingency', 'Proposition with no truth value'], 0, 'p and ¬q make p → q false.')], weight=3),
        48: dict(notes=['p ≡ q (logically equivalent) when p ↔ q is a tautology: same truth value in every row.']),
        51: dict(notes=['De Morgan: ¬(p ∧ q) ≡ ¬p ∨ ¬q and ¬(p ∨ q) ≡ ¬p ∧ ¬q.'],
                 tips=[trick('Negate each part and FLIP the operator.')],
                 exam=[mcq('¬(p ∨ q) is equivalent to:', ['¬p ∧ ¬q', '¬p ∨ ¬q', 'p ∧ q', '¬p → q'], 0, '')], weight=3),
        52: dict(notes=['Identity, domination, idempotent, double negation, negation laws.']),
        53: dict(notes=['Commutative, associative, distributive, absorption laws.']),
        54: dict(notes=['Implication laws: p → q ≡ ¬p ∨ q ≡ ¬q → ¬p; p ↔ q ≡ (p → q) ∧ (q → p).'], weight=3),
        56: dict(notes=['Equivalence proof: rewrite step by step, naming the law used at each step (no truth table).'],
                 exam=[short('Show that ¬(p → q) ≡ p ∧ ¬q without a truth table.', '¬(p → q) ≡ ¬(¬p ∨ q) (implication law) ≡ ¬¬p ∧ ¬q (De Morgan) ≡ p ∧ ¬q (double negation).')], weight=3),
        64: dict(notes=['Satisfiable: SOME assignment makes it true. Unsatisfiable: none does (its negation is a tautology).'],
                 exam=[tf('A compound proposition is unsatisfiable exactly when its negation is a tautology.', True, '')], weight=2),
        72: dict(notes=['A propositional function P(x) becomes a proposition when x gets a value or is quantified.']),
        75: dict(notes=['∀x P(x): true when P(x) holds for EVERY x in the domain. ∃x P(x): true when it holds for AT LEAST ONE.']),
        76: dict(notes=['One counterexample makes ∀x P(x) false.'],
                 exam=[mcq('Domain: all integers. ∀x (x² ≥ x) is:', ['True', 'False, counterexample x = 0', 'False, counterexample x = −1', 'Not a proposition'], 0, 'x² ≥ x holds for every integer (it fails only for 0 < x < 1).')], weight=3),
        77: dict(notes=['∃x P(x) is false only when P(x) is false for every x. Over an empty domain ∃ is false and ∀ is true.']),
        81: dict(notes=['∀ and ∃ bind tighter than all connectives: ∀x P(x) ∨ Q(x) means (∀x P(x)) ∨ Q(x).']),
        84: dict(notes=['"Every student has a computer": ∀x (S(x) → C(x)). "Some student has a computer": ∃x (S(x) ∧ C(x)).'],
                 tips=[trap('∀ pairs with →, ∃ pairs with ∧. ∃x (S(x) → C(x)) is true as soon as one x is not a student.')],
                 exam=[mcq('Domain: all people. "Some students are lazy" is:', ['∃x (S(x) ∧ L(x))', '∃x (S(x) → L(x))', '∀x (S(x) ∧ L(x))', '∀x (S(x) → L(x))'], 0, '')], weight=3),
        88: dict(notes=['¬∀x P(x) ≡ ∃x ¬P(x) and ¬∃x P(x) ≡ ∀x ¬P(x) (De Morgan for quantifiers).'],
                 tips=[trick('Push ¬ inside and flip ∀ ↔ ∃.')],
                 exam=[mcq('¬∀x (x > 0) is equivalent to:', ['∃x (x ≤ 0)', '∀x (x ≤ 0)', '∃x (x > 0)', '∀x (x < 0)'], 0, '')], weight=3),
        91: dict(notes=['Nested quantifiers: order matters when they differ. ∀x ∃y (x + y = 0) is true over the integers; ∃y ∀x (x + y = 0) is false.'],
                 exam=[mcq('Domain: integers. Which is TRUE?', ['∀x ∃y (x + y = 0)', '∃y ∀x (x + y = 0)', '∃x ∀y (x < y)', '∀x ∀y (x < y)'], 0, 'Each x has its own y = −x; no single y works for all x.')], weight=3),
        93: dict(notes=['∀x∀y and ∃x∃y can be swapped freely; ∀x∃y and ∃y∀x cannot.']),
        104: dict(notes=['An argument is valid if the conclusion must be true whenever all premises are true (the conditional (p₁ ∧ … ∧ pₙ) → q is a tautology).']),
        114: dict(notes=['The 8 rules: modus ponens, modus tollens, hypothetical syllogism, disjunctive syllogism, addition, simplification, conjunction, resolution.']),
        115: dict(notes=['Modus ponens: p, p → q ∴ q.'],
                 exam=[mcq('"If it snows, school closes. It snows. Therefore school closes." uses:', ['Modus ponens', 'Modus tollens', 'Hypothetical syllogism', 'Addition'], 0, '')], weight=3),
        116: dict(notes=['Modus tollens: ¬q, p → q ∴ ¬p.'],
                  tips=[trap('p → q, q ∴ p is the fallacy of affirming the conclusion; p → q, ¬p ∴ ¬q is denying the hypothesis. Neither is valid.')],
                  exam=[mcq('From p → q and ¬q we may conclude:', ['¬p', 'p', 'q', 'Nothing'], 0, 'Modus tollens.')], weight=3),
        117: dict(notes=['Hypothetical syllogism: p → q, q → r ∴ p → r.']),
        118: dict(notes=['Disjunctive syllogism: p ∨ q, ¬p ∴ q.'],
                  exam=[mcq('"Either the file is corrupt or the disk is full. The disk is not full. So the file is corrupt." uses:', ['Disjunctive syllogism', 'Resolution', 'Modus ponens', 'Simplification'], 0, '')], weight=2),
        119: dict(notes=['Addition: p ∴ p ∨ q.']), 120: dict(notes=['Simplification: p ∧ q ∴ p.']),
        121: dict(notes=['Conjunction: p, q ∴ p ∧ q.']),
        122: dict(notes=['Resolution: p ∨ q, ¬p ∨ r ∴ q ∨ r (the clashing literal p cancels).'],
                  exam=[mcq('From p ∨ q and ¬p ∨ r, resolution gives:', ['q ∨ r', 'q ∧ r', 'p ∨ r', '¬q ∨ r'], 0, '')], weight=3),
        123: dict(notes=['Build an argument as a numbered list of steps, each a premise or a rule applied to earlier steps.'],
                  exam=[short('Premises: p → q, q → r, p. Show r with rules of inference.', '1. p → q (premise) 2. q → r (premise) 3. p → r (hypothetical syllogism 1, 2) 4. p (premise) 5. r (modus ponens 3, 4).')], weight=3),
    }


class structures:
    AUTO_SLIDES = True
    DECK = deck('d02', 'Basic Structures: Sets, Functions, Sequences, Sums, and Matrices', 'Chapter 2',
                'Sets (roster and set-builder notation, subsets, cardinality, power sets, Cartesian products), set '
                'operations and identities, functions (one-to-one, onto, bijections, inverses, composition, floor '
                'and ceiling), sequences and summations, recurrence relations, and matrices including zero-one '
                'matrices and Boolean products.')
    ANN = {
        6: dict(notes=['A set is an unordered collection of distinct elements; a ∈ A means a is an element of A.']),
        8: dict(notes=['Roster method lists the elements: {a, e, i, o, u}. Order and repetition don’t matter: {1, 2, 2} = {2, 1}.'],
                exam=[tf('{1, 3, 3, 5} and {5, 3, 1} are equal sets.', True, '')], weight=2),
        10: dict(notes=['Set-builder: {x | P(x)}, e.g. {x ∈ ℤ⁺ | x is odd and x < 10}.']),
        12: dict(notes=['ℕ natural numbers, ℤ integers, ℤ⁺ positive integers, ℚ rationals, ℝ reals.']),
        13: dict(notes=['Universal set U holds everything under discussion; ∅ = {} has no elements, and {∅} is NOT empty (it has one element).'],
                 tips=[trap('∅ ≠ {∅}: |∅| = 0 but |{∅}| = 1.')],
                 exam=[mcq('|{∅, {∅}}| equals:', ['2', '0', '1', '3'], 0, 'Two distinct elements: ∅ and {∅}.')], weight=3),
        17: dict(notes=['A ⊆ B when every element of A is in B. ∅ ⊆ every set, and every set ⊆ itself.'],
                 exam=[tf('∅ ⊆ A for every set A.', True, '')], weight=3),
        20: dict(notes=['Proper subset A ⊂ B: A ⊆ B and A ≠ B.']),
        23: dict(notes=['|A| = number of distinct elements (cardinality).']),
        25: dict(notes=['Power set P(A) = the set of all subsets of A. If |A| = n then |P(A)| = 2ⁿ.'],
                 exam=[mcq('If A = {a, b, c}, |P(A)| is:', ['8', '6', '3', '9'], 0, '2³ = 8, including ∅ and A.'),
                       mcq('P(∅) equals:', ['{∅}', '∅', '{}', '{{∅}}'], 0, 'The only subset of ∅ is ∅ itself.')], weight=3),
        27: dict(notes=['Ordered n-tuples: order matters, (1, 2) ≠ (2, 1).']),
        29: dict(notes=['A × B = {(a, b) | a ∈ A, b ∈ B}; |A × B| = |A|·|B|; A × B ≠ B × A in general.'],
                 exam=[mcq('If |A| = 3 and |B| = 4, |A × B| is:', ['12', '7', '64', '81'], 0, '')], weight=3),
        37: dict(notes=['A ∪ B: in A or B (or both).']), 38: dict(notes=['A ∩ B: in both. Disjoint sets: A ∩ B = ∅.']),
        39: dict(notes=['Complement Ā = U − A.']), 40: dict(notes=['A − B: in A but not in B (= A ∩ B̄).']),
        41: dict(notes=['|A ∪ B| = |A| + |B| − |A ∩ B| (inclusion–exclusion).'],
                 exam=[mcq('|A| = 10, |B| = 7, |A ∩ B| = 3. |A ∪ B| = ', ['14', '17', '20', '4'], 0, '10 + 7 − 3.')], weight=3),
        43: dict(notes=['Symmetric difference A ⊕ B: in A or B but not both = (A − B) ∪ (B − A).']),
        44: dict(notes=['Set identities mirror the logical equivalences (∪ ↔ ∨, ∩ ↔ ∧, complement ↔ ¬).'], weight=2),
        47: dict(notes=['Prove set identities by: mutual subsets, set-builder notation with logical equivalences, or a membership table.']),
        48: dict(notes=['De Morgan for sets: (A ∩ B)‾ = Ā ∪ B̄ and (A ∪ B)‾ = Ā ∩ B̄.'], weight=3),
        52: dict(notes=['Membership table: 1/0 for "in"/"not in"; the identity holds if both columns match.']),
        56: dict(notes=['A function f: A → B assigns EXACTLY ONE element of B to each element of A. A is the domain, B the codomain, f(A) the range.'],
                 tips=[trap('Range ⊆ codomain; they are not always equal.')],
                 exam=[mcq('For f: A → B, the set of values actually taken by f is the:', ['Range', 'Codomain', 'Domain', 'Preimage'], 0, '')], weight=3),
        62: dict(notes=['One-to-one (injective): f(a) = f(b) ⇒ a = b, no two inputs share an output.']),
        63: dict(notes=['Onto (surjective): every b in the codomain is hit by some a.']),
        64: dict(notes=['Bijection: one-to-one AND onto; only bijections have inverses.'],
                 exam=[mcq('f: ℤ → ℤ, f(x) = x + 1 is:', ['A bijection', 'One-to-one but not onto', 'Onto but not one-to-one', 'Neither'], 0, ''),
                       mcq('f: ℤ → ℤ, f(x) = 2x is:', ['One-to-one but not onto', 'Onto but not one-to-one', 'A bijection', 'Neither'], 0, 'Odd numbers are never hit.'),
                       mcq('f: ℝ → ℝ, f(x) = x² is:', ['Neither one-to-one nor onto', 'A bijection', 'One-to-one only', 'Onto only'], 0, 'f(−1) = f(1), and negatives are never hit.')], weight=3),
        67: dict(notes=['To show one-to-one: assume f(x) = f(y) and derive x = y. To show onto: take any y and solve for an x with f(x) = y.']),
        73: dict(notes=['Inverse f⁻¹(b) = a when f(a) = b; exists only for bijections.'],
                 exam=[short('Find the inverse of f: ℝ → ℝ, f(x) = 3x − 2.', 'Let y = 3x − 2, so x = (y + 2)/3; f⁻¹(y) = (y + 2)/3. It exists because f is a bijection.')], weight=3),
        79: dict(notes=['(f ∘ g)(x) = f(g(x)): apply g FIRST.'],
                 tips=[trap('f ∘ g ≠ g ∘ f in general.')],
                 exam=[mcq('f(x) = 2x + 3, g(x) = 3x + 2. (f ∘ g)(x) =', ['6x + 7', '6x + 11', '5x + 5', '6x² + 13x + 6'], 0, 'f(3x + 2) = 2(3x + 2) + 3.')], weight=3),
        89: dict(notes=['⌊x⌋ largest integer ≤ x; ⌈x⌉ smallest integer ≥ x. ⌊−1.5⌋ = −2, ⌈−1.5⌉ = −1.'],
                 exam=[mcq('⌊−2.3⌋ + ⌈2.3⌉ equals:', ['0', '−1', '1', '5'], 0, '−3 + 3.')], weight=3),
        90: dict(notes=['n! = 1·2·…·n, 0! = 1.']),
        96: dict(notes=['Geometric progression: a, ar, ar², … ; arithmetic: a, a + d, a + 2d, …']),
        110: dict(notes=['Key sums: Σk = n(n+1)/2, Σk² = n(n+1)(2n+1)/6, Σarᵏ (k = 0…n) = (arⁿ⁺¹ − a)/(r − 1) for r ≠ 1.'],
                  exam=[mcq('Σ_{k=1}^{100} k =', ['5050', '5000', '10100', '4950'], 0, '100·101/2.')], weight=3),
        119: dict(notes=['A recurrence defines aₙ from earlier terms plus initial conditions.'],
                  exam=[mcq('aₙ = aₙ₋₁ + 3, a₀ = 2. a₃ =', ['11', '9', '14', '8'], 0, '2, 5, 8, 11.')], weight=3),
        122: dict(notes=['Fibonacci: f₀ = 0, f₁ = 1, fₙ = fₙ₋₁ + fₙ₋₂.']),
        124: dict(notes=['Iteration (forward/backward substitution): expand until a pattern appears, then close the formula.']),
        126: dict(notes=['Compound interest: Pₙ = 1.11·Pₙ₋₁ → Pₙ = (1.11)ⁿ·P₀.']),
        133: dict(notes=['A (m×k) times B (k×n) gives an m×n matrix; cᵢⱼ = row i of A · column j of B. Inner sizes must match.'],
                  tips=[trap('AB ≠ BA in general, and BA may not even be defined.')],
                  exam=[mcq('A is 2×3 and B is 3×4. AB is:', ['2×4', '3×3', '4×2', 'Undefined'], 0, '')], weight=3),
        139: dict(notes=['Transpose Aᵗ swaps rows and columns; symmetric when A = Aᵗ.']),
        141: dict(notes=['Zero-one matrices: join A ∨ B (entrywise OR), meet A ∧ B (entrywise AND).']),
        143: dict(notes=['Boolean product A ⊙ B: like a matrix product with ∧ for × and ∨ for +.'], weight=3),
    }


class number_theory:
    AUTO_SLIDES = True
    DECK = deck('d03', 'Number Theory and Cryptography', 'Chapter 4',
                'Divisibility, primes and the Fundamental Theorem of Arithmetic, GCD and LCM, the division algorithm, '
                'mod and congruences, then classical ciphers (Caesar, shift, affine), public-key cryptography with '
                'RSA, and the Diffie–Hellman key exchange.')
    ANN = {
        3: dict(notes=['a | b ("a divides b") when b = ac for some integer c (a ≠ 0).'],
                exam=[tf('3 | 12 and 12 | 3.', False, '3 | 12 is true; 12 | 3 is false.')], weight=2),
        6: dict(notes=['If a | b and a | c then a | (b + c); if a | b then a | bc; if a | b and b | c then a | c.']),
        7: dict(notes=['Prime: integer > 1 whose only positive divisors are 1 and itself. 1 is NOT prime.']),
        8: dict(notes=['Every integer > 1 is a unique product of primes (Fundamental Theorem of Arithmetic).']),
        9: dict(notes=['If n is composite, it has a prime divisor ≤ √n. So test primes up to √n only.'],
                exam=[mcq('To show 101 is prime it is enough to test divisibility by primes up to:', ['10', '50', '101', '7'], 0, '√101 ≈ 10.05: try 2, 3, 5, 7.')], weight=3),
        14: dict(notes=['gcd(a, b): largest integer dividing both. Relatively prime when gcd = 1.']),
        15: dict(notes=['gcd via prime factorizations: take the MIN power of each prime. lcm: take the MAX power.', 'gcd(a, b)·lcm(a, b) = a·b.'],
                 exam=[mcq('gcd(120, 500) =', ['20', '10', '60', '40'], 0, '2³·3·5 and 2²·5³ → 2²·5.'),
                       mcq('If gcd(a, b) = 6 and ab = 360, lcm(a, b) =', ['60', '54', '2160', '36'], 0, '360 / 6.')], weight=3),
        20: dict(notes=['Pairwise relatively prime: every pair has gcd 1.']),
        25: dict(notes=['Division algorithm: a = dq + r with 0 ≤ r < d; q = a div d, r = a mod d.'],
                 tips=[trap('The remainder is never negative: −11 div 3 = −4, −11 mod 3 = 1 (−11 = 3·(−4) + 1).')],
                 exam=[mcq('−11 mod 3 =', ['1', '−2', '2', '−1'], 0, '')], weight=3),
        32: dict(notes=['a ≡ b (mod m) when m | (a − b), i.e. a mod m = b mod m.'],
                 exam=[tf('17 ≡ 5 (mod 6).', True, '6 | 12.')], weight=3),
        34: dict(notes=['If a ≡ b and c ≡ d (mod m) then a + c ≡ b + d and ac ≡ bd (mod m).']),
        40: dict(notes=['Symmetric encryption: the same secret key encrypts and decrypts.']),
        42: dict(notes=['Caesar cipher: f(p) = (p + 3) mod 26; decrypt with (c − 3) mod 26.'],
                 exam=[mcq('Caesar (shift 3) encrypts "HI" as:', ['KL', 'EF', 'IJ', 'JK'], 0, 'H(7)+3 = K, I(8)+3 = L.')], weight=3),
        46: dict(notes=['Shift cipher: f(p) = (p + k) mod 26, f⁻¹(c) = (c − k) mod 26.']),
        50: dict(notes=['Affine cipher: f(p) = (ap + b) mod 26 with gcd(a, 26) = 1 so it can be inverted.'],
                 exam=[mcq('In an affine cipher f(p) = (ap + b) mod 26, a must satisfy:', ['gcd(a, 26) = 1', 'a is even', 'a < b', 'a = 13'], 0, '')], weight=2),
        51: dict(notes=['Frequency analysis breaks shift and affine ciphers (E, T, A are the most common letters).']),
        55: dict(notes=['Public key: anyone can encrypt with the public key; only the private key decrypts.']),
        57: dict(notes=['RSA: n = pq, choose e with gcd(e, (p−1)(q−1)) = 1, d = e⁻¹ mod (p−1)(q−1).'], weight=3),
        65: dict(notes=['Encrypt: C = Mᵉ mod n.']),
        67: dict(notes=['Decrypt: M = Cᵈ mod n.'],
                 exam=[short('RSA with p = 3, q = 11, e = 3. Find n, φ, and d.', 'n = 33, φ = (p−1)(q−1) = 20. d is the inverse of 3 mod 20: 3·7 = 21 ≡ 1, so d = 7.'),
                       mcq('In RSA, which key is kept secret?', ['d', 'e', 'n', 'e and n'], 0, '(e, n) is public.')], weight=3),
        75: dict(notes=['Diffie–Hellman: agree on prime p and base g; Alice sends gᵃ mod p, Bob sends gᵇ mod p; both compute the shared key gᵃᵇ mod p.'],
                 exam=[mcq('p = 23, g = 5, a = 6, b = 15. Alice sends:', ['5⁶ mod 23 = 8', '5¹⁵ mod 23 = 19', '6⁵ mod 23', '23⁵ mod 6'], 0, '')], weight=3),
    }


class induction_handout:
    AUTO_SLIDES = True
    DECK = deck('d04', 'Induction and Recursion (Handout)', 'Chapter 5',
                'Worked handout: the ladder and domino intuition, the basis step and inductive step, solved induction '
                'proofs for sums, divisibility and inequalities, and recursively defined functions.')
    ANN = {
        2: dict(notes=['Ladder: you can reach rung 1, and from rung k you can reach rung k + 1 ⇒ you can reach every rung.']),
        4: dict(notes=['Dominoes: first falls + each one knocks the next ⇒ all fall.']),
        7: dict(notes=['Basis step: prove P(1) (or the first value). Inductive step: assume P(k) (the inductive hypothesis) and prove P(k + 1).'],
                tips=[trap('In the inductive step you must USE P(k); just proving P(k + 1) from scratch is not induction.')], weight=3),
        26: dict(notes=['Recursive definition: give f(0), then f(n + 1) in terms of f(n).']),
    }


class induction:
    AUTO_SLIDES = True
    DECK = deck('d05', 'Mathematical Induction and Recursion', 'Chapter 5',
                'The principle of mathematical induction, its template, proofs of summation formulas, inequalities '
                'and divisibility, conjecturing a formula, and recursively defined functions.')
    ANN = {
        4: dict(notes=['To prove ∀n P(n): basis P(1); inductive step ∀k (P(k) → P(k + 1)).'],
                exam=[mcq('In an induction proof, the assumption that P(k) is true is called the:', ['Inductive hypothesis', 'Basis step', 'Conclusion', 'Contrapositive'], 0, '')], weight=3),
        6: dict(notes=['Template: state P(n) → basis → assume P(k) → show P(k + 1) → conclude.']),
        8: dict(notes=['Sum example: 1 + 2 + … + n = n(n + 1)/2. Add (k + 1) to both sides of P(k).'],
                exam=[short('Prove 1 + 2 + … + n = n(n + 1)/2 for n ≥ 1.', 'Basis: n = 1: 1 = 1·2/2. Inductive step: assume 1 + … + k = k(k + 1)/2. Then 1 + … + k + (k + 1) = k(k + 1)/2 + (k + 1) = (k + 1)(k + 2)/2, which is P(k + 1). So P(n) holds for all n ≥ 1.')], weight=3),
        12: dict(notes=['Divisibility example: n³ − n divisible by 3. Expand (k + 1)³ − (k + 1) = (k³ − k) + 3(k² + k).'], weight=2),
        14: dict(notes=['Inequality example: 2ⁿ < n!. The basis may start later than 1 (here n ≥ 4).'],
                 exam=[mcq('The basis step for "2ⁿ < n! for n ≥ 4" checks:', ['n = 4', 'n = 1', 'n = 0', 'n = k + 1'], 0, '')], weight=2),
        18: dict(notes=['Conjecture a formula by computing the first few values, then prove it by induction.']),
        25: dict(notes=['Recursively defined function: basis f(0); recursive step f(n + 1) from f(n).'],
                 exam=[mcq('f(0) = 3, f(n + 1) = 2f(n) + 3. f(2) =', ['21', '9', '15', '18'], 0, 'f(1) = 9, f(2) = 21.')], weight=3),
    }


class counting:
    AUTO_SLIDES = True
    DECK = deck('d06', 'Counting', 'Chapter 6',
                'The sum, product and subtraction (inclusion–exclusion) rules, permutations and combinations, the '
                'binomial theorem, and Pascal’s triangle.')
    ANN = {
        8: dict(notes=['Sum rule: a task done EITHER one of n₁ ways OR one of n₂ ways (no overlap) → n₁ + n₂ ways.'],
                exam=[mcq('A student picks a project from list A (23) or list B (15), no overlap. Number of choices:', ['38', '345', '23', '15'], 0, '')], weight=3),
        13: dict(notes=['Product rule: a task done in stages, n₁ ways THEN n₂ ways → n₁·n₂ ways.'],
                 tips=[trick('"or" → add, "and then" → multiply.')],
                 exam=[mcq('How many bit strings of length 8 are there?', ['256', '16', '64', '8'], 0, '2⁸.'),
                       mcq('License plates of 3 letters followed by 3 digits:', ['26³·10³', '26·10', '3·26 + 3·10', 'C(26,3)·C(10,3)'], 0, '')], weight=3),
        23: dict(notes=['Subtraction rule: n₁ + n₂ − (ways counted twice).']),
        24: dict(notes=['|A ∪ B| = |A| + |B| − |A ∩ B|.'],
                 exam=[mcq('How many bit strings of length 8 start with 1 or end with 00?', ['160', '192', '128', '64'], 0, '128 + 64 − 32.')], weight=3),
        30: dict(notes=['Permutation (order matters): P(n, r) = n!/(n − r)!.'],
                 exam=[mcq('Ways to award gold, silver, bronze among 8 runners:', ['336', '56', '512', '24'], 0, 'P(8,3) = 8·7·6.')], weight=3),
        31: dict(notes=['Combination (order doesn’t matter): C(n, r) = n!/(r!(n − r)!), and C(n, r) = C(n, n − r).'],
                 tips=[trick('Ask: does swapping two chosen items give a new outcome? Yes → permutation; no → combination.')],
                 exam=[mcq('Ways to choose a 5-player team from 10 people:', ['252', '30240', '50', '120'], 0, 'C(10,5).')], weight=3),
        45: dict(notes=['Binomial theorem: (x + y)ⁿ = Σ C(n, j)·xⁿ⁻ʲ·yʲ.'],
                 exam=[mcq('The coefficient of x²y³ in (x + y)⁵ is:', ['10', '5', '20', '15'], 0, 'C(5,3).'),
                       mcq('The coefficient of x³ in (2x + 1)⁴ is:', ['32', '8', '4', '16'], 0, 'C(4,3)·2³ = 4·8.')], weight=3),
        48: dict(notes=['Pascal’s identity: C(n + 1, k) = C(n, k − 1) + C(n, k); each entry = sum of the two above it.'], weight=2),
    }


class advanced_counting:
    AUTO_SLIDES = True
    DECK = deck('d07', 'Advanced Counting Techniques', 'Chapter 8',
                'Recurrence relations and modelling with them, solving linear homogeneous recurrences with constant '
                'coefficients (distinct and repeated roots, degree 2 and higher), and linear nonhomogeneous '
                'recurrences with particular solutions.')
    ANN = {
        5: dict(notes=['A recurrence expresses aₙ in terms of earlier terms; initial conditions pin down one solution.']),
        11: dict(notes=['Linear homogeneous of degree k with constant coefficients: aₙ = c₁aₙ₋₁ + … + cₖaₙ₋ₖ (no extra term).'],
                 exam=[mcq('Which is a linear homogeneous recurrence with constant coefficients?', ['aₙ = 3aₙ₋₁ + 4aₙ₋₂', 'aₙ = aₙ₋₁ + 2', 'aₙ = aₙ₋₁²', 'aₙ = n·aₙ₋₁'], 0, '')], weight=3),
        14: dict(notes=['Try aₙ = rⁿ → characteristic equation r² − c₁r − c₂ = 0.']),
        15: dict(notes=['Distinct roots r₁, r₂: aₙ = α₁r₁ⁿ + α₂r₂ⁿ; find α’s from initial conditions.'],
                 exam=[short('Solve aₙ = aₙ₋₁ + 2aₙ₋₂, a₀ = 2, a₁ = 7.', 'Characteristic r² − r − 2 = 0 → r = 2, −1. aₙ = α₁2ⁿ + α₂(−1)ⁿ. a₀: α₁ + α₂ = 2; a₁: 2α₁ − α₂ = 7 → α₁ = 3, α₂ = −1. So aₙ = 3·2ⁿ − (−1)ⁿ.')], weight=3),
        19: dict(notes=['Repeated root r₀: aₙ = α₁r₀ⁿ + α₂·n·r₀ⁿ.'],
                 tips=[trap('Forgetting the extra factor n on the second term for a repeated root.')],
                 exam=[mcq('Characteristic root 3 with multiplicity 2 gives the general solution:', ['α₁3ⁿ + α₂n3ⁿ', 'α₁3ⁿ + α₂3ⁿ', '(α₁ + α₂)3ⁿ', 'α₁3ⁿ + α₂(−3)ⁿ'], 0, '')], weight=3),
        23: dict(notes=['Degree k: k distinct roots → aₙ = Σ αᵢrᵢⁿ.']),
        26: dict(notes=['Root of multiplicity m contributes (α₀ + α₁n + … + αₘ₋₁nᵐ⁻¹)rⁿ.']),
        30: dict(notes=['Nonhomogeneous: aₙ = (homogeneous solution) + (a particular solution for F(n)).'], weight=3),
        34: dict(notes=['Guess the particular solution by the form of F(n): constant → C, linear → cn + d, quadratic → an² + bn + c, sⁿ → C·sⁿ (times nᵐ if s is a root).'],
                 exam=[mcq('For aₙ = 3aₙ₋₁ + 2n, the particular solution to try is:', ['cn + d', 'C', 'C·3ⁿ', 'Cn²'], 0, 'F(n) = 2n is linear.')], weight=3),
    }


class relations:
    AUTO_SLIDES = True
    DECK = deck('d08', 'Relations', 'Chapter 9',
                'Binary relations and how to write them (roster, set-builder, graph, table), relations on a set, '
                'reflexive / irreflexive, symmetric / antisymmetric and transitive relations, combining and composing '
                'relations, zero-one matrices and digraphs, closures, and equivalence relations.')
    ANN = {
        4: dict(notes=['A binary relation from A to B is a subset of A × B; (a, b) ∈ R is written aRb.']),
        18: dict(notes=['A relation on A is a subset of A × A. There are 2^(n²) relations on a set with n elements.'],
                 exam=[mcq('How many relations are there on a set with 3 elements?', ['512', '9', '64', '27'], 0, '2⁹.')], weight=3),
        23: dict(notes=['Reflexive: (a, a) ∈ R for EVERY a. Irreflexive: (a, a) ∉ R for every a.']),
        25: dict(notes=['"Not reflexive" ≠ "irreflexive": a relation can be neither (some loops but not all).'],
                 tips=[trap('Not reflexive just needs ONE missing loop; irreflexive needs ALL loops missing.')],
                 exam=[tf('A relation that is not reflexive must be irreflexive.', False, 'It can have some loops and not others.')], weight=3),
        29: dict(notes=['Symmetric: aRb ⇒ bRa. Antisymmetric: aRb and bRa ⇒ a = b.', 'A relation can be both (e.g. equality) or neither.'],
                 exam=[mcq('R = {(1,1), (1,2), (2,1)} on {1, 2} is:', ['Symmetric, not antisymmetric', 'Antisymmetric, not symmetric', 'Both', 'Neither'], 0, ''),
                       tf('A relation can be both symmetric and antisymmetric.', True, 'E.g. {(1,1), (2,2)}.')], weight=3),
        36: dict(notes=['Transitive: aRb and bRc ⇒ aRc.'],
                 exam=[mcq('R = {(1,2), (2,3)} on {1, 2, 3} is not transitive because it lacks:', ['(1,3)', '(3,1)', '(2,1)', '(1,1)'], 0, '')], weight=3),
        38: dict(notes=['Relations are sets: combine with ∪, ∩, −, ⊕.']),
        40: dict(notes=['Composite S ∘ R = {(a, c) | ∃b: (a, b) ∈ R and (b, c) ∈ S}: R first, then S.'],
                 exam=[mcq('R = {(1,2)}, S = {(2,3)}. S ∘ R =', ['{(1,3)}', '{(2,2)}', '{(3,1)}', '∅'], 0, '')], weight=3),
        43: dict(notes=['Powers: R¹ = R, Rⁿ⁺¹ = Rⁿ ∘ R. R is transitive iff Rⁿ ⊆ R for all n.']),
        49: dict(notes=['Zero-one matrix M_R: mᵢⱼ = 1 if (aᵢ, bⱼ) ∈ R.']),
        52: dict(notes=['Reflexive ⇔ all 1s on the diagonal; symmetric ⇔ M = Mᵗ; antisymmetric ⇔ no pair of 1s mirrored off the diagonal.'],
                 exam=[mcq('In the matrix of a reflexive relation:', ['Every diagonal entry is 1', 'Every diagonal entry is 0', 'The matrix equals its transpose', 'The matrix is all 1s'], 0, '')], weight=3),
        58: dict(notes=['M_(S∘R) = M_R ⊙ M_S (Boolean product, R’s matrix on the left).']),
        65: dict(notes=['M_(Rⁿ) = M_R ⊙ … ⊙ M_R (n times).']),
        69: dict(notes=['Digraph: an edge a → b for each (a, b); a loop at a for (a, a).']),
        72: dict(notes=['Digraph test: reflexive = loop at every vertex; symmetric = every edge has a reverse edge; antisymmetric = no two-way edges between distinct vertices; transitive = every 2-step path has a shortcut.'], weight=2),
        77: dict(notes=['Reflexive closure: R ∪ Δ (add all missing loops).'],
                 exam=[mcq('The reflexive closure of R = {(1,2)} on {1, 2} is:', ['{(1,1), (1,2), (2,2)}', '{(1,2), (2,1)}', '{(1,1), (2,2)}', '{(1,2)}'], 0, '')], weight=3),
        80: dict(notes=['Symmetric closure: R ∪ R⁻¹ (add the reverse of every pair).']),
        83: dict(notes=['Transitive closure R*: R ∪ R² ∪ … ∪ Rⁿ (keep adding shortcuts until nothing changes).'],
                 exam=[short('Find the transitive closure of R = {(1,2), (2,3), (3,4)} on {1, 2, 3, 4}.', 'R ∪ R² ∪ R³ = {(1,2), (2,3), (3,4), (1,3), (2,4), (1,4)}.')], weight=3),
        92: dict(notes=['Equivalence relation: reflexive + symmetric + transitive (e.g. congruence mod m). Its equivalence classes partition the set.'],
                 tips=[trick('Equivalence = RST: Reflexive, Symmetric, Transitive.')],
                 exam=[mcq('Which is an equivalence relation on ℤ?', ['a ≡ b (mod 4)', 'a < b', 'a | b', 'a ≠ b'], 0, ''),
                       mcq('A partial order is reflexive, transitive and:', ['Antisymmetric', 'Symmetric', 'Irreflexive', 'Total'], 0, '')], weight=3),
    }


DECKS_HERE = [logic, structures, number_theory, induction_handout, induction, counting, advanced_counting, relations]

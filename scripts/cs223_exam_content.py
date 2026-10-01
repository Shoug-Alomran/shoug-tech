"""Question data for the CS223 interactive exams (built by build_cs223_course.py).

Every exam is re-typeset from the papers Shoug collected; the papers themselves are
not published. Worked solutions are written fresh and every numeric answer was
checked with sympy. Where an official answer key exists and is wrong, the part
carries a `note` explaining the correction.

Part kinds (see docs/javascripts/cs223-exam.js):
    mcq      options + 0-based answer index
    fields   [(label, answer, mode)]; answer may hold alternatives split by "|";
             mode None (exact list), "parallel" (any nonzero multiple), "set" (any order)
    written  no auto-check; the reader reveals the solution and marks themself
Prompts, steps and notes are HTML with $...$ / $$...$$ KaTeX math.
"""


# --------------------------------------------------------------------------- #
# LaTeX helpers
# --------------------------------------------------------------------------- #

def mat(spec, env="bmatrix"):
    """mat("1 2; 3 4") -> a bmatrix; entries are whitespace-separated."""
    rows = [r.split() for r in spec.split(";")]
    body = r" \\ ".join(" & ".join(r) for r in rows)
    return r"\begin{%s}%s\end{%s}" % (env, body, env)


def det(spec):
    return mat(spec, "vmatrix")


def vec(spec):
    return mat(";".join(spec.split()))


def aug(spec, left):
    """Augmented matrix with a bar after `left` columns."""
    rows = [r.split() for r in spec.split(";")]
    cols = len(rows[0])
    fmt = "c" * left + "|" + "c" * (cols - left)
    body = r" \\ ".join(" & ".join(r) for r in rows)
    return r"\left[\begin{array}{%s}%s\end{array}\right]" % (fmt, body)


def system(*lines):
    return r"\begin{cases}" + r" \\ ".join(lines) + r"\end{cases}"


def D(tex):
    """Display math."""
    return "$$" + tex + "$$"


def P(label, pts, prompt, kind="written", **kw):
    part = {"label": label, "pts": pts, "prompt": prompt, "kind": kind}
    part.update(kw)
    return part


def S(title, pts, parts, intro=""):
    return {"title": title, "pts": pts, "parts": parts, "intro": intro}


YES_NO = ["Yes", "No"]


# --------------------------------------------------------------------------- #
# 1. Quiz 1 - Term 242
# --------------------------------------------------------------------------- #

QUIZ_1_242 = {
    "slug": "quiz-1-242",
    "title": "Quiz 1 (Term 242)",
    "kicker": "CS223 // Quiz 1 // Term 242",
    "lede": "Linear systems, row reduction, parametric solutions and consistency. "
            "Show every step: pivots, basic and free variables, and the RREF when the system is consistent.",
    "meta": ["Chapter 1", "7 questions", "Points not printed: 1 per question"],
    "duration": 0,
    "sections": [
        S("Questions 1 to 7", 7, [
            P("Q1", 1, "Solve the linear system." + D(system("x + y + 2z = 3", "x + 2y + z = 1", "2x + y + z = 0")),
              "fields", fields=[("x", "-1"), ("y", "0"), ("z", "2")],
              steps=["Augmented matrix: " + D(aug("1 1 2 3; 1 2 1 1; 2 1 1 0", 3)),
                     r"$R_2 \leftarrow R_2 - R_1$ and $R_3 \leftarrow R_3 - 2R_1$: " + D(aug("1 1 2 3; 0 1 -1 -2; 0 -1 -3 -6", 3)),
                     r"$R_3 \leftarrow R_3 + R_2$: the last row is $-4z = -8$, so $z = 2$.",
                     r"Back-substitute: $y - z = -2 \Rightarrow y = 0$, then $x + y + 2z = 3 \Rightarrow x = -1$.",
                     "Three pivots and no free variables, so the solution is unique. RREF: " + D(aug("1 0 0 -1; 0 1 0 0; 0 0 1 2", 3))],
              final=r"$(x, y, z) = (-1,\ 0,\ 2)$"),
            P("Q2", 1, "Solve the linear system and give the parametric description of its solutions." +
              D(system("x + y + z - 3t = 1", "2x + y - z + t = -1")),
              "fields", fields=[("(x, y, z, t) when z = t = 0", "-2,3,0,0")],
              hint="Enter the four numbers separated by commas.",
              steps=["Augmented matrix: " + D(aug("1 1 1 -3 1; 2 1 -1 1 -1", 4)),
                     r"$R_2 \leftarrow R_2 - 2R_1$, then $R_2 \leftarrow -R_2$, then $R_1 \leftarrow R_1 - R_2$: " +
                     D(aug("1 0 -2 4 -2; 0 1 3 -7 3", 4)),
                     r"Pivots in the $x$ and $y$ columns: $x, y$ are basic, $z, t$ are free.",
                     r"$x = -2 + 2z - 4t$ and $y = 3 - 3z + 7t$.",
                     "Parametric vector form: " + D(r"\begin{bmatrix}x\\y\\z\\t\end{bmatrix} = " + vec("-2 3 0 0") +
                                                    " + z" + vec("2 -3 1 0") + " + t" + vec("-4 7 0 1"))],
              final="Infinitely many solutions, two free variables."),
            P("Q3", 1, r"Find the triplet $(a, b, c)$, if possible, such that $P(x) = ax^2 + bx + c$ satisfies "
                       r"$P(-1) = 5$, $P(1) = 1$ and $P(2) = 2$.",
              "fields", fields=[("a", "1"), ("b", "-2"), ("c", "2")],
              steps=["Each condition is a linear equation in $a, b, c$: " +
                     D(system("a - b + c = 5", "a + b + c = 1", "4a + 2b + c = 2")),
                     r"Subtract the first from the second: $2b = -4$, so $b = -2$ and $a + c = 3$.",
                     r"The third becomes $4a + c = 6$. Subtract $a + c = 3$: $3a = 3$, so $a = 1$ and $c = 2$."],
              final=r"$P(x) = x^2 - 2x + 2$, so $(a, b, c) = (1, -2, 2)$."),
            P("Q4", 1, "Solve the linear system." + D(system("x + 2z = 1", "-y + z = 2", "x - 2y = 1")),
              "fields", fields=[("x", "-1"), ("y", "-1"), ("z", "1")],
              steps=["Augmented matrix: " + D(aug("1 0 2 1; 0 -1 1 2; 1 -2 0 1", 3)),
                     r"$R_3 \leftarrow R_3 - R_1$: $(0, -2, -2 \mid 0)$. Then $R_3 \leftarrow R_3 - 2R_2$: $(0, 0, -4 \mid -4)$, so $z = 1$.",
                     r"$-y + z = 2 \Rightarrow y = -1$, and $x + 2z = 1 \Rightarrow x = -1$."],
              final=r"$(x, y, z) = (-1, -1, 1)$, a unique solution."),
            P("Q5", 1, "Solve the linear system." + D(system("2x + 2y + 2z - 6t = 1", "x + y + z - 3t = 1")),
              "mcq", options=["A unique solution", "Infinitely many solutions with three free variables",
                              "Infinitely many solutions with one free variable", "No solution (inconsistent)"],
              answer=3,
              steps=[r"Swap the rows and apply $R_2 \leftarrow R_2 - 2R_1$: " + D(aug("1 1 1 -3 1; 0 0 0 0 -1", 4)),
                     r"The second row reads $0 = -1$."],
              final="The system is inconsistent: no solution."),
            P("Q6", 1, "Are the two matrices row equivalent? If so, show how one matrix can be transformed into the other "
                       "using elementary row operations." + D(mat("1 2 4; 5 6 2; 3 4 5") + r"\qquad " + mat("3 4 5; 2 2 -3; 2 4 8")),
              "mcq", options=YES_NO, answer=0,
              steps=[r"$\det\!" + mat("1 2 4; 5 6 2; 3 4 5") + r" = -8 \neq 0$ and $\det\!" + mat("3 4 5; 2 2 -3; 2 4 8") + r" = 16 \neq 0$.",
                     r"A square matrix with nonzero determinant has a pivot in every column, so both reduce to $I_3$.",
                     r"Row operations are reversible: reduce the first matrix to $I_3$, then apply the inverse of each step "
                     r"that took the second matrix to $I_3$, in reverse order. That chain turns the first matrix into the second."],
              final="Yes: both matrices are row equivalent to $I_3$, hence to each other."),
            P("Q7", 1, r"For which values of $a$ and $b$ is the system consistent with a unique solution, and for which is it inconsistent?" +
              D(system("x + ay = b", "ax + y = b")),
              "fields", fields=[("Values of a where the solution is NOT unique (list)", "1,-1", "set")],
              steps=[r"Coefficient determinant: $\det" + mat("1 a; a 1") + r" = 1 - a^2$.",
                     r"If $a \neq \pm 1$ the determinant is nonzero: one solution, $x = y = \dfrac{b}{1 + a}$.",
                     r"If $a = 1$ both equations are $x + y = b$: consistent for every $b$, with infinitely many solutions.",
                     r"If $a = -1$: $x - y = b$ and $-x + y = b$. Adding them gives $0 = 2b$, so the system is inconsistent when "
                     r"$b \neq 0$ and has infinitely many solutions when $b = 0$."],
              final=r"Unique for $a \neq \pm 1$ (any $b$). Inconsistent exactly when $a = -1$ and $b \neq 0$."),
        ]),
    ],
}


# --------------------------------------------------------------------------- #
# 2. Major 1 - Term 251
# --------------------------------------------------------------------------- #

M1_MATRIX = aug("2 5 3 8 7 6; 0 5 7 4 2 3; 0 0 0 8 0 0; 0 0 0 0 0 0", 5)

MAJOR_1_251 = {
    "slug": "major-1-251",
    "title": "Major 1 (Term 251)",
    "kicker": "CS223 // Major Exam 1 // Term 251",
    "lede": "Echelon forms, linear combinations, parametric solutions, independence, linear transformations, "
            "inverses and LU factorization.",
    "meta": ["Chapters 1 to 2", "60 minutes", "20 points"],
    "duration": 60,
    "sections": [
        S("Question 1: Choose the correct answer", 4, intro="Consider the augmented matrix" + D(M1_MATRIX), parts=[
            P("1", 1, "Which statement describes the matrix?", "mcq",
              options=["The matrix is in reduced echelon form", "The matrix is in echelon form",
                       "The matrix is not in any standard form", "None of the above"], answer=1,
              steps=["Zero rows are at the bottom and each leading entry sits to the right of the one above (columns 1, 2, 4).",
                     "It is not <em>reduced</em>: the leading entries are 2, 5, 8 rather than 1, and there are nonzero entries above them."],
              final="Echelon form (b)."),
            P("2", 1, "About the variables of the system the matrix represents:", "mcq",
              options=["There is no free variable", "There is one free variable", "There are 4 basic variables", "None of the above"],
              answer=3,
              steps=["Five variable columns; pivots in columns 1, 2 and 4.",
                     r"Basic: $x_1, x_2, x_4$ (three of them). Free: $x_3, x_5$ (two of them). None of (a) to (c) is true."],
              final="None of the above (d)."),
            P("3", 1, "About the solutions:", "mcq",
              options=["The system has 3 solutions", "The system has a unique solution",
                       "The system has an infinite number of solutions", "The system is inconsistent"], answer=2,
              steps=["No row of the form $[0 \\ \\cdots \\ 0 \\mid c]$ with $c \\neq 0$, so the system is consistent.",
                     "Consistent with free variables means infinitely many solutions."],
              final="Infinitely many solutions (c)."),
            P("4", 1, "About the constants:", "mcq",
              options=["The system is homogeneous", "The system is non-homogeneous",
                       "The system contains no constant terms", "None of the above"], answer=1,
              steps=["The last column (constants) is $(6, 3, 0, 0)$, which is not all zero."],
              final="Non-homogeneous (b)."),
        ]),
        S("Question 2", 8, [
            P("1", 2, r"Let $\mathbf u = " + vec("1 2 0") + r"$, $\mathbf v = " + vec("-1 1 1") + r"$ and $\mathbf w = " + vec("-1 7 3") +
              r"$. Find scalars $a$ and $b$ such that $\mathbf w = a\mathbf u + b\mathbf v$.",
              "fields", fields=[("a", "2"), ("b", "3")],
              steps=[r"Solve $\begin{bmatrix}\mathbf u & \mathbf v\end{bmatrix}\begin{bmatrix}a\\b\end{bmatrix} = \mathbf w$: " +
                     D(aug("1 -1 -1; 2 1 7; 0 1 3", 2)),
                     r"Row 3 gives $b = 3$. Row 1: $a - 3 = -1$, so $a = 2$. Row 2 checks: $2(2) + 3 = 7$."],
              final=r"$\mathbf w = 2\mathbf u + 3\mathbf v$"),
            P("2", 2.5, "Describe the solutions of the system in parametric vector form and give one solution." +
              D(system("x + y + 12z = 1", "x + 2y + 9z = -1")),
              "fields", fields=[("The solution with z = 0, as (x, y, z)", "3,-2,0"),
                                ("A direction vector for the line of solutions", "-15,3,1", "parallel")],
              steps=[r"$R_2 \leftarrow R_2 - R_1$: $(0, 1, -3 \mid -2)$. Then $R_1 \leftarrow R_1 - R_2$: " + D(aug("1 0 15 3; 0 1 -3 -2", 3)),
                     r"$z$ is free: $x = 3 - 15z$, $y = -2 + 3z$.",
                     D(r"\mathbf x = " + vec("3 -2 0") + " + z" + vec("-15 3 1") + r",\quad z \in \mathbb R")],
              final=r"One solution ($z = 0$): $(3, -2, 0)$. Another ($z = 1$): $(-12, 1, 1)$."),
            P("3", 1.5, "Given that" + D(aug("1 2 3 0; 5 2 8 0; 1 1 9 0", 3) + r"\sim" + aug("1 2 3 0; 0 -8 -7 0; 0 0 55 0", 3)) +
              r"is the set $\left\{" + vec("1 5 1") + "," + vec("2 2 1") + "," + vec("3 8 9") + r"\right\}$ linearly independent?",
              "mcq", options=YES_NO, answer=0,
              steps=["The echelon form has a pivot in every one of the three columns, so there is no free variable.",
                     r"The homogeneous equation $A\mathbf x = \mathbf 0$ has only the trivial solution."],
              final="Yes, the vectors are linearly independent."),
            P("4a", 1, r"$T:\mathbb R^2 \to \mathbb R^2$ has standard matrix $" + mat("1 2; 1 h") +
              r"$. Find $h$ so that $T\!\left(" + vec("2 3") + r"\right) = " + vec("8 11") + "$.",
              "fields", fields=[("h", "3")],
              steps=[r"$" + mat("1 2; 1 h") + vec("2 3") + " = " + r"\begin{bmatrix}2 + 6\\ 2 + 3h\end{bmatrix}$.",
                     r"The first entry is 8 for any $h$. The second needs $2 + 3h = 11$, so $h = 3$."],
              final="$h = 3$"),
            P("4b", 1, r"For the same $T$, find the value(s) of $h$ for which $T$ maps $\mathbb R^2$ onto $\mathbb R^2$.",
              "fields", fields=[("T is onto for every h except h =", "2")],
              steps=[r"$T$ is onto exactly when its standard matrix has a pivot in every row, i.e. $\det \neq 0$.",
                     r"$\det" + mat("1 2; 1 h") + r" = h - 2$."],
              final=r"Onto for every $h \neq 2$."),
        ]),
        S("Question 3", 8, [
            P("1", 1.5, r"Find the inverse of $A = " + mat("1 2; 3 7") + "$.",
              "fields", fields=[("Entries of A⁻¹, row by row", "7,-2,-3,1")],
              hint="Four numbers, e.g. a, b, c, d for the matrix [a b; c d].",
              steps=[r"$\det A = 1\cdot 7 - 2 \cdot 3 = 1$.",
                     r"$A^{-1} = \dfrac{1}{\det A}" + mat("7 -2; -3 1") + " = " + mat("7 -2; -3 1") + "$."],
              final=r"$A^{-1} = " + mat("7 -2; -3 1") + "$"),
            P("2", 1.5, "Use the inverse from part 1 to solve" + D(system("x + 2y = 5", "3x + 7y = 12")),
              "fields", fields=[("x", "11"), ("y", "-3")],
              steps=[r"$\mathbf x = A^{-1}\mathbf b = " + mat("7 -2; -3 1") + vec("5 12") + " = " + vec("35-24 -15+12") + " = " + vec("11 -3") + "$."],
              final="$x = 11$, $y = -3$"),
            P("3", 2, r"Given the LU factorization of $A = " + mat("2 3; 4 5") + r"$ with $L = " + mat("1 0; 2 1") + r"$ and $U = " + mat("2 3; 0 -1") +
              r"$, use it to solve $A\mathbf x = \mathbf b$ where $\mathbf b = " + vec("5 11") + "$.",
              "fields", fields=[("y from Ly = b", "5,1"), ("x from Ux = y", "4,-1")],
              steps=[r"Forward substitution, $L\mathbf y = \mathbf b$: $y_1 = 5$, then $2(5) + y_2 = 11$, so $\mathbf y = (5, 1)$.",
                     r"Back substitution, $U\mathbf x = \mathbf y$: $-x_2 = 1 \Rightarrow x_2 = -1$; $2x_1 + 3(-1) = 5 \Rightarrow x_1 = 4$.",
                     r"Check: $A\mathbf x = (8 - 3,\ 16 - 5) = (5, 11)$."],
              final=r"$\mathbf x = (4, -1)$"),
            P("4a", 1, r"Let $A = " + mat("1 0; 1 1; 0 1") + r"$. Find $A^TA$.",
              "fields", fields=[("Entries of AᵀA, row by row", "2,1,1,2")],
              steps=[r"$A^TA = " + mat("1 1 0; 0 1 1") + mat("1 0; 1 1; 0 1") + " = " + mat("2 1; 1 2") + "$."],
              final=r"$A^TA = " + mat("2 1; 1 2") + "$"),
            P("4b", 2, r"With $B = " + mat("2 3; 1 2") + r"$, find the matrix $X$ such that $A^TA\,X = B$.",
              "fields", fields=[("Entries of X, row by row", "1,4/3,0,1/3")],
              steps=[r"$\det(A^TA) = 4 - 1 = 3$, so $(A^TA)^{-1} = \tfrac13" + mat("2 -1; -1 2") + "$.",
                     r"$X = (A^TA)^{-1}B = \tfrac13" + mat("2 -1; -1 2") + mat("2 3; 1 2") + r" = \tfrac13" + mat("3 4; 0 1") + "$."],
              final=r"$X = " + mat(r"1 \tfrac43; 0 \tfrac13") + "$"),
        ]),
    ],
}


# --------------------------------------------------------------------------- #
# 3. Major 2 - Term 251
# --------------------------------------------------------------------------- #

M2_A = mat("0 2 1; 3 1 4; 2 0 5")

MAJOR_2_251 = {
    "slug": "major-2-251",
    "title": "Major 2 (Term 251)",
    "kicker": "CS223 // Major Exam 2 // Term 251",
    "lede": "Determinants by cofactors, row reduction and Cramer's rule, then null space, column space, bases and rank.",
    "meta": ["Chapters 3 to 4", "20 points"],
    "duration": 0,
    "sections": [
        S("Question 1: Determinants", 11, intro=D("A = " + M2_A), parts=[
            P("a", 2, r"Compute $\det A$ by cofactor expansion along the first row.",
              "fields", fields=[("det A", "-16")],
              steps=[r"$\det A = 0\cdot C_{11} + 2\cdot C_{12} + 1\cdot C_{13}$.",
                     r"$C_{12} = -" + det("3 4; 2 5") + r" = -(15 - 8) = -7$ and $C_{13} = " + det("3 1; 2 0") + r" = 0 - 2 = -2$.",
                     r"$\det A = 2(-7) + 1(-2) = -16$."],
              final=r"$\det A = -16$"),
            P("b", 2, r"Compute $\det A$ by row reduction.",
              "fields", fields=[("det A", "-16")],
              steps=[r"Swap $R_1 \leftrightarrow R_2$ (sign flips): " + D(mat("3 1 4; 0 2 1; 2 0 5")),
                     r"$R_3 \leftarrow R_3 - \tfrac23 R_1$: $(0, -\tfrac23, \tfrac73)$. Then $R_3 \leftarrow R_3 + \tfrac13 R_2$: $(0, 0, \tfrac83)$.",
                     r"Triangular: product of the diagonal $= 3 \cdot 2 \cdot \tfrac83 = 16$. One swap, so $\det A = -16$."],
              final=r"$\det A = -16$"),
            P("c", 1, "Using your determinant, is $A$ invertible?", "mcq", options=YES_NO, answer=0,
              steps=[r"$\det A = -16 \neq 0$, and a square matrix is invertible exactly when its determinant is nonzero."],
              final="Yes, $A$ is invertible."),
            P("d", 3, r"Using Cramer's rule and $\det A$, solve" + D(system("2y + z = 0", "3x + y + 4z = 0", "2x + 5z = 1")),
              "fields", fields=[("x", "-7/16"), ("y", "-3/16"), ("z", "3/8")],
              steps=[r"The coefficient matrix is $A$ and $\mathbf b = (0, 0, 1)$. Replace one column of $A$ by $\mathbf b$ each time.",
                     r"$\det A_1(\mathbf b) = " + det("0 2 1; 0 1 4; 1 0 5") + r" = 1\cdot(8 - 1) = 7$",
                     r"$\det A_2(\mathbf b) = " + det("0 0 1; 3 0 4; 2 1 5") + r" = 1\cdot(3 - 0) = 3$",
                     r"$\det A_3(\mathbf b) = " + det("0 2 0; 3 1 0; 2 0 1") + r" = 1\cdot(0 - 6) = -6$",
                     r"$x = \tfrac{7}{-16}$, $y = \tfrac{3}{-16}$, $z = \tfrac{-6}{-16}$."],
              final=r"$x = -\tfrac{7}{16},\ y = -\tfrac{3}{16},\ z = \tfrac38$"),
            P("e-i", 1, r"Using $\det A$, find $" + det("0 4 2; 4 0 10; 6 2 8") + "$. Justify.",
              "fields", fields=[("Determinant", "128")],
              steps=[r"Row 1 is $2\times$ row 1 of $A$, row 2 is $2\times$ row 3 of $A$, row 3 is $2\times$ row 2 of $A$.",
                     r"Factor 2 out of each row: $2^3 = 8$. The rows are $A$'s with rows 2 and 3 swapped: factor $-1$.",
                     r"$8 \cdot (-1) \cdot (-16) = 128$."],
              final="$128$"),
            P("e-ii", 1, r"Using $\det A$, find $" + det("0 2 1; 1 1 -1; 2 0 5") + "$. Justify.",
              "fields", fields=[("Determinant", "-16")],
              steps=[r"Row 2 is $(3, 1, 4) - (2, 0, 5)$: $A$ with $R_2 \leftarrow R_2 - R_3$.",
                     "Adding a multiple of one row to another does not change the determinant."],
              final="$-16$"),
            P("e-iii", 1, r"Using $\det A$, find $\det(-A^2)$. Justify.",
              "fields", fields=[("det(−A²)", "-256")],
              steps=[r"$\det(-A^2) = (-1)^3\det(A^2) = -(\det A)^2$ for a $3\times 3$ matrix.",
                     r"$-(-16)^2 = -256$."],
              final="$-256$"),
        ]),
        S("Question 2: Vector spaces", 9, [
            P("a", 2, r"Let $A = " + mat("-6 12; -3 6") + r"$ and $\mathbf w = " + vec("2 1") +
              r"$. Is $\mathbf w$ in $\operatorname{Col} A$? Is it in $\operatorname{Nul} A$?",
              "mcq", options=["In both Col A and Nul A", "In Col A only", "In Nul A only", "In neither"], answer=0,
              steps=[r"$A\mathbf w = (-12 + 12,\ -6 + 6) = (0, 0)$, so $\mathbf w \in \operatorname{Nul} A$.",
                     r"$\operatorname{Col} A = \operatorname{Span}\{(-6, -3)\} = \operatorname{Span}\{(2, 1)\}$ because column 2 is $-2\times$ column 1.",
                     r"$\mathbf w = -\tfrac13(-6, -3)$, so $\mathbf w \in \operatorname{Col} A$ as well."],
              final="$\\mathbf w$ is in both spaces."),
            P("b", 2, r"Let $\mathbf v_1 = " + vec("7 4 -9 -5") + r"$, $\mathbf v_2 = " + vec("4 -7 2 5") + r"$, $\mathbf v_3 = " + vec("1 -5 3 4") +
              r"$ with $\mathbf v_1 - 3\mathbf v_2 + 5\mathbf v_3 = \mathbf 0$. Find a basis for $H = \operatorname{Span}\{\mathbf v_1, \mathbf v_2, \mathbf v_3\}$.",
              "mcq", options=[r"$\{\mathbf v_1, \mathbf v_2, \mathbf v_3\}$", r"$\{\mathbf v_1, \mathbf v_2\}$", r"$\{\mathbf v_1\}$", r"$\{\mathbf 0\}$"],
              answer=1,
              steps=[r"The relation gives $\mathbf v_3 = \tfrac15(3\mathbf v_2 - \mathbf v_1)$, so $\mathbf v_3$ adds nothing to the span.",
                     r"$\mathbf v_1$ and $\mathbf v_2$ are not multiples of each other, so they are independent.",
                     "By the Spanning Set Theorem, the two remaining vectors form a basis (any two of the three would work)."],
              final=r"Basis: $\{\mathbf v_1, \mathbf v_2\}$, so $\dim H = 2$."),
            P("c", 4, "Assume $A$ is row equivalent to $B$. Find bases for Nul $A$, Col $A$ and Row $A$, and find rank $A$, "
                      "dim Nul $A$, dim Col $A$ and dim Row $A$." +
              D("A = " + mat("-2 4 -2 -4; 2 -6 -3 1; -3 8 2 -3") + r",\qquad B = " + mat("1 0 6 5; 0 2 5 3; 0 0 0 0")),
              "fields", fields=[("rank A", "2"), ("dim Nul A", "2"), ("dim Col A", "2"), ("dim Row A", "2")],
              steps=[r"$B$ has pivots in columns 1 and 2, so rank $A = 2$ and $\dim\operatorname{Nul}A = 4 - 2 = 2$.",
                     r"Nul $A$: from $B$, $x_1 = -6x_3 - 5x_4$ and $2x_2 = -5x_3 - 3x_4$. Basis: " +
                     D(r"\left\{" + vec(r"-6 -\tfrac52 1 0") + "," + vec(r"-5 -\tfrac32 0 1") + r"\right\}"),
                     "Col $A$: the pivot columns of the <em>original</em> $A$: " + D(r"\left\{" + vec("-2 2 -3") + "," + vec("4 -6 8") + r"\right\}"),
                     "Row $A$: the nonzero rows of the echelon form $B$: $\\{(1, 0, 6, 5),\\ (0, 2, 5, 3)\\}$.",
                     r"$\dim\operatorname{Col}A = \dim\operatorname{Row}A = \operatorname{rank}A = 2$."],
              final="rank = 2, dim Nul = 2, dim Col = 2, dim Row = 2"),
            P("d", 1, r"A $4\times 7$ matrix $A$ has rank 4. Find nullity $A$ and rank $A^T$.",
              "fields", fields=[("nullity A", "3"), ("rank Aᵀ", "4")],
              steps=[r"Rank theorem: rank $A$ + nullity $A = n = 7$, so nullity $= 3$.",
                     r"rank $A^T$ = rank $A = 4$ (row rank equals column rank)."],
              final="nullity $A = 3$, rank $A^T = 4$"),
        ]),
    ],
}


# --------------------------------------------------------------------------- #
# 4. Final - Term 231
# --------------------------------------------------------------------------- #

FINAL_231 = {
    "slug": "final-231",
    "title": "Final Exam (Term 231)",
    "kicker": "CS223 // Final Exam // Term 231",
    "lede": "Covers all six chapters: Gauss-Jordan elimination, parameter cases, matrix algebra, determinants, "
            "vector spaces, eigenvalues and orthogonal projection.",
    "meta": ["Chapters 1 to 6", "2 hours", "40 points"],
    "duration": 120,
    "sections": [
        S("Question 1: Linear equations and matrix algebra", 17, [
            P("a", 3, "Solve the linear system by Gauss-Jordan elimination (reduced echelon form)." +
              D(system("3x - y + z + 7w = 13", "-2x + y - z - 3w = -9", "-2x + y - 7w = -8")),
              "fields", fields=[("The solution with w = 0, as (x, y, z, w)", "4,0,1,0"),
                                ("Direction vector for w (in x, y, z, w order)", "-4,-1,4,1", "parallel")],
              steps=["Augmented matrix: " + D(aug("3 -1 1 7 13; -2 1 -1 -3 -9; -2 1 0 -7 -8", 4)),
                     r"$R_1 \leftarrow R_1 + R_2$ gives $(1, 0, 0, 4 \mid 4)$, a convenient first pivot.",
                     r"Clear column 1: $R_2 \leftarrow R_2 + 2R_1$, $R_3 \leftarrow R_3 + 2R_1$, then continue to the RREF: " +
                     D(aug("1 0 0 4 4; 0 1 0 1 0; 0 0 1 -4 1", 4)),
                     r"$w$ is free: $x = 4 - 4w$, $y = -w$, $z = 1 + 4w$."],
              final=r"$(x, y, z, w) = (4, 0, 1, 0) + w(-4, -1, 4, 1)$, $w \in \mathbb R$"),
            P("b", 3, r"For which values of $a$ does the system have no solution? Exactly one? Infinitely many?" +
              D(system("x + 2y - 3z = 4", "3x - y + 5z = 2", "4x + y + (a^2 - 14)z = a + 2")),
              "fields", fields=[("a giving NO solution", "-4"), ("a giving INFINITELY many", "4")],
              steps=[r"$R_2 \leftarrow R_2 - 3R_1$, $R_3 \leftarrow R_3 - 4R_1$, then $R_3 \leftarrow R_3 - R_2$: " +
                     D(aug("1 2 -3 4; 0 -7 14 -10; 0 0 a^2-16 a-4", 3)),
                     r"If $a^2 - 16 \neq 0$ ($a \neq \pm 4$): a pivot in every column, one solution.",
                     r"$a = 4$: the last row is $0 = 0$, so a free variable and infinitely many solutions.",
                     r"$a = -4$: the last row is $0 = -8$, inconsistent."],
              final=r"None at $a = -4$; infinitely many at $a = 4$; exactly one for every other $a$."),
            P("c-i", 3, r"$A = " + mat("2 4 1; 5 2 -1; 4 2 2") + r"$, $B = " + mat("2 3; 2 -2; 7 5") +
              r"$ and $C = AB$. Find $C_{11}$, $C_{32}$ and $C_{21}$.",
              "fields", fields=[("C₁₁", "19"), ("C₃₂", "18"), ("C₂₁", "7")],
              steps=[r"$C_{ij}$ = (row $i$ of $A$) $\cdot$ (column $j$ of $B$).",
                     r"$C_{11} = 2(2) + 4(2) + 1(7) = 19$",
                     r"$C_{32} = 4(3) + 2(-2) + 2(5) = 18$",
                     r"$C_{21} = 5(2) + 2(2) + (-1)(7) = 7$"],
              final=r"$C_{11} = 19,\ C_{32} = 18,\ C_{21} = 7$"),
            P("c-ii", 2, r"Find $C^T$, and the transpose of $(A + B)$.",
              "fields", fields=[("Entries of Cᵀ, row by row", "19,7,26,3,6,18")],
              steps=[r"$C = AB = " + mat("19 3; 7 6; 26 18") + r"$, so $C^T = " + mat("19 7 26; 3 6 18") + "$.",
                     r"$A$ is $3\times3$ and $B$ is $3\times2$, so $A + B$ is undefined and so is $(A + B)^T$."],
              final=r"$C^T = " + mat("19 7 26; 3 6 18") + r"$; $(A + B)^T$ does not exist."),
            P("d", 3, r"If $A^{-1} = " + mat("2 5; -1 4") + r"$ and $\mathbf b = " + vec("7 -3") + r"$, solve $A\mathbf x = \mathbf b$.",
              "fields", fields=[("x", "-1"), ("y", "-19")],
              steps=[r"$\mathbf x = A^{-1}\mathbf b = " + mat("2 5; -1 4") + vec("7 -3") + " = " + vec("14-15 -7-12") + "$."],
              final="$x = -1$, $y = -19$"),
            P("e", 3, r"Find all values of $a$ and $b$ that make both $A = " + mat("a+b-1 0; 0 3") + r"$ and $B = " + mat("5 0; 0 2a-3b-7") +
              "$ not invertible.",
              "fields", fields=[("a", "2"), ("b", "-1")],
              steps=[r"Both are diagonal, so each determinant is the product of the diagonal.",
                     r"$\det A = 3(a + b - 1) = 0 \Rightarrow a + b = 1$.",
                     r"$\det B = 5(2a - 3b - 7) = 0 \Rightarrow 2a - 3b = 7$.",
                     r"Solve together: $a = 1 - b$, so $2 - 2b - 3b = 7$ and $b = -1$, $a = 2$."],
              final="$a = 2$, $b = -1$"),
        ]),
        S("Question 2: Determinants", 4, [
            P("a", 2, r"If $" + det("2x-4 0 0; 0 x+3 0; 0 0 x") + r" = 0$, find $x$.",
              "fields", fields=[("All solutions x (list)", "2,-3,0", "set")],
              steps=["The matrix is diagonal, so the determinant is $(2x - 4)(x + 3)x$.",
                     "Set each factor to zero."],
              final="$x = 2$, $x = -3$ or $x = 0$"),
            P("b", 2, r"Find the determinant of $A = " + mat("1 2 6 0; 3 2 5 4; 0 6 0 4; 3 0 7 1") +
              "$ by cofactor expansion from position (row 3, column 2).",
              "fields", fields=[("det A", "-50")],
              steps=[r"Expand along row 3, $(0, 6, 0, 4)$: only $a_{32}$ and $a_{34}$ contribute.",
                     r"$C_{32} = (-1)^{5}" + det("1 6 0; 3 5 4; 3 7 1") + r" = -31$",
                     r"$C_{34} = (-1)^{7}" + det("1 2 6; 3 2 5; 3 0 7") + r" = -(-34) = 34$",
                     r"$\det A = 6(-31) + 4(34) = -186 + 136 = -50$."],
              final=r"$\det A = -50$"),
        ]),
        S("Question 3: Vector spaces", 9, [
            P("a", 1.5, r"Let $S = \{(1, 2), (-1, 1)\}$ and $\mathbf u = (3, 5)$. Is $\mathbf u$ a linear combination of $S$?",
              "fields", fields=[("c₁ in u = c₁(1,2) + c₂(−1,1)", "8/3"), ("c₂", "-1/3")],
              steps=[r"Solve $c_1 - c_2 = 3$ and $2c_1 + c_2 = 5$. Adding: $3c_1 = 8$.",
                     r"$c_1 = \tfrac83$, $c_2 = c_1 - 3 = -\tfrac13$."],
              final=r"Yes: $\mathbf u = \tfrac83(1, 2) - \tfrac13(-1, 1)$."),
            P("b", 1.5, r"Let $S = \{(1, 1, 1), (3, 2, -1), (1, 0, -3)\}$. Does $S$ span $\mathbb R^3$?",
              "mcq", options=YES_NO, answer=1,
              steps=[r"Three vectors span $\mathbb R^3$ only if the matrix with them as columns is invertible.",
                     r"$" + det("1 3 1; 1 2 0; 1 -1 -3") + r" = 1(-6 - 0) - 3(-3 - 0) + 1(-1 - 2) = -6 + 9 - 3 = 0$.",
                     r"Indeed $(1, 0, -3) = -2(1, 1, 1) + (3, 2, -1)$."],
              final=r"No, the vectors are dependent and span only a plane."),
            P("c-1-3", 3, r"For $A = " + mat("10 -3 -2; 0 0 0; 0 0 0") + r"$ find the rank, $\dim\operatorname{Col}A$ and the nullity.",
              "fields", fields=[("rank A", "1"), ("dim Col A", "1"), ("nullity A", "2")],
              steps=["One nonzero row, already in echelon form: one pivot.",
                     r"rank $= \dim\operatorname{Col}A = 1$; nullity $= 3 - 1 = 2$."],
              final="rank 1, dim Col 1, nullity 2"),
            P("c-4", 1, r"Find a basis of $\operatorname{Col}A$.",
              "fields", fields=[("Basis vector", "10,0,0", "parallel")],
              steps=["The pivot column of $A$ is column 1."],
              final=r"$\{(10, 0, 0)\}$"),
            P("c-5", 2, r"Find a basis of $\operatorname{Nul}A$.",
              steps=[r"$10x_1 - 3x_2 - 2x_3 = 0$, so $x_1 = 0.3x_2 + 0.2x_3$ with $x_2, x_3$ free.",
                     D(r"\mathbf x = x_2" + vec(r"\tfrac{3}{10} 1 0") + " + x_3" + vec(r"\tfrac15 0 1"))],
              final=r"Basis: $\{(3, 10, 0),\ (1, 0, 5)\}$ (any nonzero multiples work)."),
        ]),
        S("Question 4: Eigenvalues and eigenvectors", 6, [
            P("a", 3, r"Find the eigenvalues of $A = " + mat("0 0 -2; 1 2 1; 1 0 3") + "$.",
              "fields", fields=[("Eigenvalues with repeats (list)", "1,2,2", "set")],
              steps=[r"Expand $\det(A - \lambda I)$ along column 2, which has one nonzero entry, $2 - \lambda$:",
                     r"$\det(A - \lambda I) = (2 - \lambda)\det" + mat(r"-\lambda -2; 1 3-\lambda") + r" = (2 - \lambda)(\lambda^2 - 3\lambda + 2)$.",
                     r"$= (2 - \lambda)(\lambda - 1)(\lambda - 2)$."],
              final=r"$\lambda = 1$ and $\lambda = 2$ (multiplicity 2)"),
            P("b-1", 1, r"Let $A = " + mat("3 5; 0 4") + r"$. Is $A$ diagonalizable?", "mcq", options=YES_NO, answer=0,
              steps=["Triangular, so the eigenvalues are the diagonal entries 3 and 4.",
                     r"Two distinct eigenvalues for a $2\times2$ matrix guarantee diagonalizability."],
              final="Yes."),
            P("b-2", 2, r"Find $D$ and $P$ such that $D = P^{-1}AP$.",
              "fields", fields=[("Eigenvector for λ = 3", "1,0", "parallel"), ("Eigenvector for λ = 4", "5,1", "parallel")],
              steps=[r"$\lambda = 3$: $A - 3I = " + mat("0 5; 0 1") + r"$ forces $x_2 = 0$: $\mathbf v_1 = (1, 0)$.",
                     r"$\lambda = 4$: $A - 4I = " + mat("-1 5; 0 0") + r"$ gives $x_1 = 5x_2$: $\mathbf v_2 = (5, 1)$."],
              final=r"$P = " + mat("1 5; 0 1") + r",\quad D = " + mat("3 0; 0 4") + "$"),
        ]),
        S("Question 5: Orthogonality and least squares", 4, [
            P("1", 4, r"Let $\mathbf y = " + vec("6 5") + r"$ and $\mathbf u = " + vec("3 1") +
              r"$. Find the orthogonal projection of $\mathbf y$ onto $\mathbf u$ and write $\mathbf y$ as the sum of a vector in "
              r"$\operatorname{Span}\{\mathbf u\}$ and a vector orthogonal to $\mathbf u$.",
              "fields", fields=[("ŷ = proj_u y", "69/10,23/10"), ("z = y − ŷ", "-9/10,27/10")],
              note="The paper prints \"the orthogonal projection of y onto y\"; the intended question is the projection onto u.",
              steps=[r"$\mathbf y\cdot\mathbf u = 18 + 5 = 23$ and $\mathbf u\cdot\mathbf u = 9 + 1 = 10$.",
                     r"$\hat{\mathbf y} = \tfrac{23}{10}\mathbf u = (6.9,\ 2.3)$.",
                     r"$\mathbf z = \mathbf y - \hat{\mathbf y} = (-0.9,\ 2.7)$. Check: $\mathbf z\cdot\mathbf u = -2.7 + 2.7 = 0$."],
              final=r"$\mathbf y = (6.9, 2.3) + (-0.9, 2.7)$"),
        ]),
    ],
}


# --------------------------------------------------------------------------- #
# 5. Final - Term 232
# --------------------------------------------------------------------------- #

FINAL_232 = {
    "slug": "final-232",
    "title": "Final Exam (Term 232)",
    "kicker": "CS223 // Final Exam // Term 232",
    "lede": "Gauss-Jordan, parameter cases, transposes, LU solving, determinant tricks, the four fundamental subspaces, "
            "eigen-decomposition, Gram-Schmidt and QR.",
    "meta": ["Chapters 1 to 6", "3 hours", "40 points", "Official key checked: 1 correction"],
    "duration": 180,
    "sections": [
        S("Question 1: Linear equations and matrix algebra", 16, [
            P("1", 3, "Solve by Gauss-Jordan elimination (reduced row echelon form)." +
              D(system("-2x_1 + 3x_2 - 4x_3 = -2", "x_1 - 2x_2 + 2x_3 = 2", "3x_1 + x_2 - x_3 = 1")),
              "fields", fields=[("x₁", "4/7"), ("x₂", "-2"), ("x₃", "-9/7")],
              steps=[r"$R_1 \leftarrow R_1/(-2)$, $R_2 \leftarrow R_2 - R_1$, $R_3 \leftarrow R_3 - 3R_1$, $R_2 \leftarrow -2R_2$.",
                     r"$R_1 \leftarrow R_1 + \tfrac32R_2$, $R_3 \leftarrow R_3 - \tfrac{11}{2}R_2$, $R_3 \leftarrow R_3/(-7)$, $R_1 \leftarrow R_1 - 2R_3$.",
                     "RREF: " + D(aug(r"1 0 0 \tfrac47; 0 1 0 -2; 0 0 1 -\tfrac97", 3)),
                     r"Check in row 1: $-2(\tfrac47) + 3(-2) - 4(-\tfrac97) = \tfrac{-8 - 42 + 36}{7} = -2$."],
              final=r"$x_1 = \tfrac47,\ x_2 = -2,\ x_3 = -\tfrac97$"),
            P("2a", 1.5, "For which values of $a$ does the system have a unique solution?" +
              D(system("x_1 + 2x_2 + x_3 = 3", "-x_1 + ax_2 + 4x_3 = -2", "2x_1 - 3x_2 + ax_3 = b")),
              "mcq", options=[r"Every real $a$", r"Every $a$ except $a = \pm\sqrt{31}$", r"Every $a$ except $a = 0$", r"No real $a$"],
              answer=0,
              steps=[r"$\det A = 1(a^2 + 12) - 2(-a - 8) + 1(3 - 2a) = a^2 + 31$.",
                     r"$a^2 + 31 \geq 31 > 0$ for every real $a$, so the coefficient matrix is always invertible."],
              note=r"The official key writes $a \neq \pm i\sqrt{31}$. That is the same statement, since $\pm i\sqrt{31}$ are not real.",
              final="Unique for every real $a$."),
            P("2b", 1.5, r"Find the pairs $(a, b)$ for which the system has more than one solution.",
              "mcq", options=["There is no real pair", r"$(a, b) = (0, 6)$", r"$(a, b) = (\sqrt{31}, 6)$", "Every pair with $b = 0$"],
              answer=0,
              steps=[r"Row reduction ends in $\left[\,0 \;\; 0 \;\; a^2 + 31 \mid ab - 6a + 2b - 5\,\right]$.",
                     r"More than one solution needs $a^2 + 31 = 0$, which has no real solution."],
              note=r"The key lists complex pairs: $a = \pm i\sqrt{31}$ with $b = \tfrac{11 + 6i\sqrt{31}}{2 + i\sqrt{31}}$ or "
                   r"$\tfrac{5 - 6i\sqrt{31}}{2 - i\sqrt{31}}$. Over the reals, no pair exists.",
              final="No real pair."),
            P("3a", 3, r"$A = " + mat("-1 2 -3; 2 1 -1; -2 3 1") + r"$, $B = " + mat("1 -2; -1 3; -3 3") + r"$. Let $C = B^TA^T$. Find $C$.",
              "fields", fields=[("Entries of C, row by row", "6,4,-8,-1,-4,16")],
              steps=[r"$C = B^TA^T = " + mat("1 -1 -3; -2 3 3") + mat("-1 2 -2; 2 1 3; -3 -1 1") + " = " + mat("6 4 -8; -1 -4 16") + "$."],
              final=r"$C = " + mat("6 4 -8; -1 -4 16") + "$"),
            P("3b", 2, "Write $C$ in terms of $A$ and $B$.", "mcq",
              options=[r"$C = (AB)^T$", r"$C = (BA)^T$", r"$C = A^TB^T$", r"$C = BA$"], answer=0,
              steps=[r"The transpose of a product reverses the order: $(AB)^T = B^TA^T$."],
              final=r"$C = (AB)^T$"),
            P("4", 3, "Solve the system using the given factorization $A = LU$." +
              D(mat("1 -2 1; -1 3 2; 1 0 1") + r"\begin{bmatrix}x_1\\x_2\\x_3\end{bmatrix} = " + vec("3 -1 2") +
                r",\qquad " + mat("1 -2 1; -1 3 2; 1 0 1") + " = " + mat("1 0 0; -1 1 0; 1 2 1") + mat("1 -2 1; 0 1 3; 0 0 -6")),
              "fields", fields=[("z from Lz = b", "3,2,-5"), ("x from Ux = z", "7/6,-1/2,5/6")],
              steps=[r"Let $U\mathbf x = \mathbf z$ and solve $L\mathbf z = \mathbf b$ forward: $z_1 = 3$, $z_2 = -1 + 3 = 2$, $z_3 = 2 - 3 - 4 = -5$.",
                     r"Solve $U\mathbf x = \mathbf z$ backward: $-6x_3 = -5 \Rightarrow x_3 = \tfrac56$; $x_2 + 3x_3 = 2 \Rightarrow x_2 = -\tfrac12$;",
                     r"$x_1 - 2x_2 + x_3 = 3 \Rightarrow x_1 = 3 - 1 - \tfrac56 = \tfrac76$."],
              final=r"$\mathbf x = \left(\tfrac76,\ -\tfrac12,\ \tfrac56\right)$"),
            P("5", 2, r"Which values of $a$ and $b$ make $" + mat("3 -2 1; 0 a-2 3; 0 0 b+1") + "$ singular?", "mcq",
              options=[r"$a = 2$ or $b = -1$", r"Only $a = 2$ and $b = -1$ together", r"$a = -2$ or $b = 1$", "No values"], answer=0,
              steps=[r"Upper triangular: $\det = 3(a - 2)(b + 1)$.",
                     "The product is zero when either factor is zero."],
              final=r"Singular exactly when $a = 2$ or $b = -1$ (or both)."),
        ]),
        S("Question 2: Determinants", 4, [
            P("1", 2, r"Find $\det A$ for $A = " + mat("2 3 -1 4; 1 -2 3 0; 2 -1 0 -2; -3 2 -1 3") + r"$ given that $" +
              det("6 -4 2 -6; 3 -3 3 -2; 3 -6 9 0; 2 3 -1 4") + " = -42$.",
              "fields", fields=[("det A", "7")],
              steps=["Undo the operations that turn the given matrix into $A$, tracking the determinant:",
                     r"Swap $R_1, R_4$: $-1 \times (-42) = 42$.",
                     r"Scale $R_4$ by $-\tfrac12$: $42 \times (-\tfrac12) = -21$.",
                     r"Swap $R_2, R_3$: $21$. Scale $R_2$ by $\tfrac13$: $7$.",
                     r"$R_3 \leftarrow R_3 - R_2$ leaves it unchanged: $7$."],
              final=r"$\det A = 7$"),
            P("2", 2, r"Find $\det A$ by cofactor expansion based on row 2 and column 3, where $A = " +
              mat("-2 0 1 -2; 0 0 2 0; -1 6 0 -3; -2 1 0 -2") + "$.",
              "fields", fields=[("det A", "8")],
              steps=[r"Row 2 has a single nonzero entry, $a_{23} = 2$.",
                     r"$\det A = (-1)^{2+3}\cdot 2 \cdot " + det("-2 0 -2; -1 6 -3; -2 1 -2") + "$.",
                     r"The $3\times3$ minor is $-2(-12 + 3) - 0 + (-2)(-1 + 12) = 18 - 22 = -4$.",
                     r"$\det A = -2 \cdot (-4) = 8$."],
              final=r"$\det A = 8$"),
        ]),
        S("Question 3: Vector spaces", 10, intro=r"Let $\mathbf v_1 = " + vec(r"1 -3 \tfrac12") + r"$, $\mathbf v_2 = " + vec("1 1 -1") +
          r"$, $\mathbf v_3 = " + vec("-1 2 -2") + r"$ and $A = \begin{bmatrix}\mathbf v_1 & \mathbf v_2 & \mathbf v_3\end{bmatrix}$.", parts=[
            P("1", 2, "Are these vectors linearly independent?", "mcq", options=YES_NO, answer=0,
              steps=[r"$\det A = -\tfrac{15}{2} \neq 0$, so $A\mathbf x = \mathbf 0$ has only the trivial solution."],
              final="Yes."),
            P("2", 2, "Find the null space and the nullity of $A$.", "fields", fields=[("nullity A", "0")],
              steps=[r"Only the trivial solution, so $\operatorname{Nul}A = \{\mathbf 0\}$."],
              note="The key calls the null space \"empty\". A null space always contains the zero vector, so the precise answer is {0}, with dimension 0.",
              final=r"$\operatorname{Nul}A = \{\mathbf 0\}$, nullity $0$"),
            P("3", 2, "Find the column space and rank of $A$.", "fields", fields=[("rank A", "3")],
              steps=[r"rank $= 3 - $ nullity $= 3$, so the three columns are a basis of $\operatorname{Col}A = \mathbb R^3$."],
              final=r"rank $3$, $\operatorname{Col}A = \operatorname{Span}\{\mathbf v_1, \mathbf v_2, \mathbf v_3\} = \mathbb R^3$"),
            P("4", 2, "Find the row space of $A$.",
              steps=[r"$A$ reduces to $I_3$, whose rows are the standard basis vectors."],
              final=r"$\operatorname{Row}A = \mathbb R^3$, basis $\{(1,0,0), (0,1,0), (0,0,1)\}$"),
            P("5", 2, r"Find the left null space of $A$ (the solutions of $A^T\mathbf x = \mathbf 0$).",
              "fields", fields=[("dim of the left null space", "0")],
              steps=[r"A square matrix with independent columns also has independent rows, so $A^T$ is invertible.",
                     r"$A^T\mathbf x = \mathbf 0$ has only $\mathbf x = \mathbf 0$."],
              final=r"Left null space $= \{\mathbf 0\}$"),
        ]),
        S("Question 4: Eigenvalues and eigenvectors", 6, intro=D("A = " + mat("4 1 -1; 2 5 -2; 1 1 2")), parts=[
            P("1", 2, "Find the eigenvalues of $A$.", "fields", fields=[("Eigenvalues with repeats (list)", "3,3,5", "set")],
              steps=[r"$\det(A - \lambda I) = -\lambda^3 + 11\lambda^2 - 39\lambda + 45 = -(\lambda - 3)^2(\lambda - 5)$."],
              final=r"$\lambda_1 = 3$ (multiplicity 2), $\lambda_2 = 5$"),
            P("2", 2, "Find the eigenvector for the largest eigenvalue.", "fields",
              fields=[("Eigenvector for λ = 5", "1,2,1", "parallel")],
              steps=[r"$A - 5I = " + mat("-1 1 -1; 2 0 -2; 1 1 -3") + r"$ reduces to $x_1 = x_3$, $x_2 = 2x_3$."],
              final=r"$\mathbf v = \alpha(1, 2, 1)$, $\alpha \neq 0$"),
            P("3", 2, r"Can you find $A^2$ using the eigen-decomposition $A = SDS^{-1}$?", "mcq", options=YES_NO, answer=0,
              steps=[r"$A - 3I = " + mat("1 1 -1; 2 2 -2; 1 1 -1") + r"$ has rank 1, so the eigenspace for $\lambda = 3$ is 2-dimensional: "
                     r"$x_1 = -x_2 + x_3$ gives $(-1, 1, 0)$ and $(1, 0, 1)$.",
                     r"With $(1, 2, 1)$ for $\lambda = 5$ that is three independent eigenvectors: $A$ is diagonalizable.",
                     D(r"S = " + mat("-1 1 1; 1 0 2; 0 1 1") + r",\quad D = " + mat("3 0 0; 0 3 0; 0 0 5") +
                       r",\quad A^2 = SD^2S^{-1} = " + mat("17 8 -8; 16 25 -16; 8 8 1"))],
              note="The official key answers No, claiming the eigenvector matrix has two identical columns. That is wrong: "
                   "a repeated eigenvalue only blocks diagonalization when its eigenspace is too small, and here it has "
                   "dimension 2. You can check the result: squaring A directly gives the same matrix.",
              final="Yes."),
        ]),
        S("Question 5: Orthogonality and least squares", 4, intro=D("A = " + mat("1 -1 2; -1 1 0; 1 2 -1")), parts=[
            P("1", 2, "Orthogonalize the columns of $A$ with the Gram-Schmidt process.", "fields",
              fields=[("u₂ (orthogonal, any scale)", "-1,1,2", "parallel"), ("u₃ (orthogonal, any scale)", "1,1,0", "parallel")],
              steps=[r"$\mathbf u_1 = \mathbf a_1 = (1, -1, 1)$.",
                     r"$\mathbf a_2\cdot\mathbf u_1 = -1 - 1 + 2 = 0$, so $\mathbf u_2 = \mathbf a_2 = (-1, 1, 2)$.",
                     r"$\mathbf u_3 = \mathbf a_3 - \tfrac{\mathbf a_3\cdot\mathbf u_1}{\mathbf u_1\cdot\mathbf u_1}\mathbf u_1 - \tfrac{\mathbf a_3\cdot\mathbf u_2}{\mathbf u_2\cdot\mathbf u_2}\mathbf u_2 "
                     r"= (2, 0, -1) - \tfrac13(1, -1, 1) + \tfrac46(-1, 1, 2) = (1, 1, 0)$.",
                     r"Normalize: $\mathbf e_1 = \tfrac{1}{\sqrt3}(1, -1, 1)$, $\mathbf e_2 = \tfrac{1}{\sqrt6}(-1, 1, 2)$, $\mathbf e_3 = \tfrac{1}{\sqrt2}(1, 1, 0)$."],
              final=r"Orthonormal columns $\mathbf e_1, \mathbf e_2, \mathbf e_3$ as above"),
            P("2", 2, "Using that result, find the QR decomposition of $A$.", "fields",
              fields=[("R₁₁, R₁₂, R₁₃", "sqrt(3),0,sqrt(3)/3"), ("R₂₂, R₂₃", "sqrt(6),-2sqrt(6)/3"), ("R₃₃", "sqrt(2)")],
              hint="Type sqrt(3) or √3; decimals also work.",
              steps=[r"$Q = \begin{bmatrix}\mathbf e_1 & \mathbf e_2 & \mathbf e_3\end{bmatrix}$ and, since $Q^TQ = I$, $R = Q^TA$.",
                     r"$R_{ij} = \mathbf e_i\cdot\mathbf a_j$: $R_{11} = \sqrt3$, $R_{12} = 0$, $R_{13} = \tfrac{1}{\sqrt3}$, "
                     r"$R_{22} = \sqrt6$, $R_{23} = -\tfrac{4}{\sqrt6}$, $R_{33} = \sqrt2$.",
                     D(r"Q = " + mat(r"\tfrac{\sqrt3}{3} -\tfrac{\sqrt6}{6} \tfrac{\sqrt2}{2}; -\tfrac{\sqrt3}{3} \tfrac{\sqrt6}{6} \tfrac{\sqrt2}{2}; \tfrac{\sqrt3}{3} \tfrac{\sqrt6}{3} 0") +
                       r",\quad R = " + mat(r"\sqrt3 0 \tfrac{\sqrt3}{3}; 0 \sqrt6 -\tfrac{2\sqrt6}{3}; 0 0 \sqrt2"))],
              final="$A = QR$ with $Q$, $R$ as above"),
        ]),
    ],
}


# --------------------------------------------------------------------------- #
# 6. Sample Final - Term 223
# --------------------------------------------------------------------------- #

SAMPLE_FINAL_223 = {
    "slug": "sample-final-223",
    "title": "Sample Final (Term 223)",
    "kicker": "CS223 // Sample Final Exam // Summer 223",
    "lede": "A full sample final from the summer term: systems, rank, unitary and inverse matrices, four determinant "
            "techniques, column space membership, eigen-decomposition and projections.",
    "meta": ["Chapters 1 to 6", "2 hours", "37 of 40 points", "Q6(c) omitted"],
    "duration": 120,
    "notice": "Question 6(c), a least-squares problem worth 3 points, is left out: the source file is missing the matrix A "
              "and vector b it refers to.",
    "sections": [
        S("Question 1: Linear equations", 6, [
            P("i", 3, "Solve the system." + D(system("x + y + z = 6", "x + 2y + 3z = 14", "x + 4y + 7z = 30")),
              "fields", fields=[("The solution with z = 0, as (x, y, z)", "-2,8,0"),
                                ("Direction vector of the solution line", "1,-2,1", "parallel")],
              steps=[r"$R_2 \leftarrow R_2 - R_1$: $(0, 1, 2 \mid 8)$. $R_3 \leftarrow R_3 - R_1$: $(0, 3, 6 \mid 24)$. $R_3 \leftarrow R_3 - 3R_2$: a zero row.",
                     r"RREF: " + D(aug("1 0 -1 -2; 0 1 2 8; 0 0 0 0", 3)),
                     r"$z$ is free: $x = -2 + z$, $y = 8 - 2z$."],
              note="The answer table on the paper has a single box for each of x, y, z, but the system is consistent with a free "
                   "variable, so it has infinitely many solutions.",
              final=r"$(x, y, z) = (-2, 8, 0) + z(1, -2, 1)$"),
            P("ii", 3, "Solve the system." + D(system("x_1 - 2x_2 + x_3 - 4x_4 = 1", "x_1 + 3x_2 + 7x_3 + 2x_4 = 2", "x_1 - 12x_2 - 11x_3 - 16x_4 = 5")),
              "mcq", options=["A unique solution", "Infinitely many solutions", "No solution"], answer=2,
              steps=[r"$R_2 \leftarrow R_2 - R_1$: $(0, 5, 6, 6 \mid 1)$. $R_3 \leftarrow R_3 - R_1$: $(0, -10, -12, -12 \mid 4)$.",
                     r"$R_3 \leftarrow R_3 + 2R_2$: $(0, 0, 0, 0 \mid 6)$, which reads $0 = 6$."],
              final="Inconsistent: no solution."),
        ]),
        S("Question 2: Matrix algebra", 6, [
            P("a", 1, r"Find the rank and the nullity of $A = " + mat("1 -2 -1 4; 2 -4 3 5; -1 2 6 -7") + "$.",
              "fields", fields=[("rank A", "2"), ("nullity A", "2")],
              steps=[r"$R_2 \leftarrow R_2 - 2R_1$: $(0, 0, 5, -3)$. $R_3 \leftarrow R_3 + R_1$: $(0, 0, 5, -3)$. $R_3 \leftarrow R_3 - R_2$: zero row.",
                     "Pivots in columns 1 and 3: rank 2, and nullity $= 4 - 2 = 2$."],
              final="rank 2, nullity 2"),
            P("b", 1, r"Show that $A = \tfrac15" + mat("-1+2i -4-2i; 2-4i -2-i") + r"$ is unitary ($i^2 = -1$).",
              "mcq", options=["Yes, A is unitary", "No, A is not unitary"], answer=0,
              steps=[r"For a complex matrix, unitary means $A^{H}A = I$ with $A^H = \overline{A}^{\,T}$ (the conjugate transpose).",
                     r"Column 1 has squared length $\tfrac{1}{25}(|{-1+2i}|^2 + |2-4i|^2) = \tfrac{5 + 20}{25} = 1$, and so does column 2.",
                     r"Their Hermitian inner product is $\tfrac{1}{25}\left[(-1-2i)(-4-2i) + (2+4i)(-2-i)\right] = \tfrac{1}{25}\left[(0 + 10i) + (0 - 10i)\right] = 0$."],
              note=r"The hint on the paper says $U^TU = I$. With complex entries you need the conjugate transpose: "
                   r"the plain $A^TA$ here has diagonal $\tfrac{(1-2i)^2}{5}$ and $\tfrac{(2+i)^2}{5}$, not 1.",
              final="Yes: $A^HA = I$."),
            P("c", 2, r"Are $A = " + mat("1 0 1; 1 1 2; 0 1 1") + r"$ and $B = " + mat("0 1 -1; 1 0 1; 1 2 1") + "$ inverses of each other?",
              "mcq", options=YES_NO, answer=1,
              steps=[r"$AB = " + mat("1 3 0; 3 5 2; 2 2 2") + r" \neq I$.",
                     r"In fact $\det A = 0$ (column 3 = column 1 + column 2), so $A$ has no inverse at all."],
              final="No."),
            P("d", 2, r"Find the inverse of $A = " + mat(r"-8 17 2 \tfrac13 -1; 4 0 \tfrac25 -9 4; 0 0 0 0 0; -1 13 4 2 2; 2 -1 -3 -5 7") + "$ if it exists.",
              "mcq", options=["The inverse exists", "A has no inverse"], answer=1,
              steps=[r"Row 3 is all zeros, so $\det A = 0$ (expand along that row).",
                     "A matrix with zero determinant is not invertible."],
              final="No inverse."),
        ]),
        S("Question 3: Determinants", 7, [
            P("a", 1, r"Find $\det A$ using elementary row operations, $A = " + mat("2 3 4; 5 6 7; 8 9 1") + "$.",
              "fields", fields=[("det A", "27")],
              steps=[r"$R_2 \leftarrow R_2 - \tfrac52R_1$: $(0, -\tfrac32, -3)$. $R_3 \leftarrow R_3 - 4R_1$: $(0, -3, -15)$.",
                     r"$R_3 \leftarrow R_3 - 2R_2$: $(0, 0, -9)$. Replacements keep the determinant.",
                     r"$\det A = 2 \cdot (-\tfrac32)(-9) = 27$."],
              final=r"$\det A = 27$"),
            P("b", 2, r"Find $\det B$ by making the boxed entry $b_{23} = 1$ a pivot for its column, $B = " +
              mat(r"5 4 2 1; 2 3 \boxed{1} -2; -5 -7 -3 9; 1 -2 -1 4") + "$.",
              "fields", fields=[("det B", "38")],
              steps=[r"Clear column 3 with $R_1 \leftarrow R_1 - 2R_2$, $R_3 \leftarrow R_3 + 3R_2$, $R_4 \leftarrow R_4 + R_2$ (determinant unchanged):" +
                     D(mat("1 -2 0 5; 2 3 1 -2; 1 2 0 3; 3 1 0 2")),
                     r"Expand along column 3: $\det B = (-1)^{2+3}\cdot 1\cdot" + det("1 -2 5; 1 2 3; 3 1 2") + "$.",
                     r"The minor is $1(4 - 3) + 2(2 - 9) + 5(1 - 6) = 1 - 14 - 25 = -38$, so $\det B = 38$."],
              final=r"$\det B = 38$"),
            P("c", 2, r"Find $\det C$, $C = " + mat("3 2 4 5 7; 8 9 7 5 6; 2 3 1 0 1; 5 4 3 2 1; 1 2 3 4 5") +
              r"$, using $\det D = -54$ for $D = " + mat("1 2 3 4 5; 5 4 3 2 1; 3 2 4 5 7; 8 9 7 5 6; 2 3 1 0 1") + "$.",
              "fields", fields=[("det C (from the given det D)", "54|-54")],
              steps=[r"The rows of $C$ are rows 3, 4, 5, 2, 1 of $D$, so $C = PD$ for a permutation matrix $P$, and $\det C = \det P\cdot\det D$.",
                     r"The permutation $(3, 4, 5, 2, 1)$ splits into the cycles $(1\,3\,5)(2\,4)$: an even 3-cycle times one swap, so it is odd and $\det P = -1$.",
                     r"$\det C = -\det D = -(-54) = 54$."],
              note=r"Computing $D$ directly gives $\det D = +54$, so the printed value has a sign slip. With the true value, "
                   r"$\det C = -54$. Both answers are accepted here; the row-permutation argument is what the question tests.",
              final=r"$\det C = -\det D = 54$ (using the given value)"),
            P("d", 2, r"Find $\det U$, $U = " + mat("2 3 4 7 8; -1 5 3 2 1; 0 0 2 1 5; 0 0 3 -1 4; 0 0 5 2 6") + "$.",
              "fields", fields=[("det U", "377")],
              steps=[r"$U$ is block upper triangular: a $2\times2$ block on top-left and a $3\times3$ block on bottom-right, zeros below.",
                     r"$" + det("2 3; -1 5") + r" = 10 + 3 = 13$.",
                     r"$" + det("2 1 5; 3 -1 4; 5 2 6") + r" = 2(-6 - 8) - 1(18 - 20) + 5(6 + 5) = -28 + 2 + 55 = 29$.",
                     r"$\det U = 13 \cdot 29 = 377$."],
              final=r"$\det U = 377$"),
        ]),
        S("Question 4: Vector spaces", 7, [
            P("a-i", 0.5, r"Is $\mathbf v = " + vec("-2 10") + r"$ in $\operatorname{Col}A$ for $A = " + mat("1 3; 4 -6") +
              "$? If so, give the combination of columns.",
              "fields", fields=[("Coefficients (c₁, c₂)", "1,-1")],
              steps=[r"Solve $c_1 + 3c_2 = -2$, $4c_1 - 6c_2 = 10$: $c_1 = 1$, $c_2 = -1$."],
              final=r"Yes: $\mathbf v = \mathbf a_1 - \mathbf a_2$"),
            P("a-ii", 0.5, r"Is $\mathbf v = " + vec("-1 0 2") + r"$ in $\operatorname{Col}A$ for $A = " + mat("1 1 2; 1 0 1; 2 1 3") + "$?",
              "mcq", options=YES_NO, answer=1,
              steps=[r"Column 3 = column 1 + column 2, so Col $A$ is a plane. Reduce $[A \mid \mathbf v]$:",
                     r"$R_2 - R_1$: $(0, -1, -1 \mid 1)$; $R_3 - 2R_1$: $(0, -1, -1 \mid 4)$; subtract: $(0, 0, 0 \mid 3)$, inconsistent."],
              final="No."),
            P("a-iii", 1, r"Is $\mathbf v = " + vec("5 1 -1") + r"$ in $\operatorname{Col}A$ for $A = " + mat("1 -1 1; 9 3 1; 1 1 1") +
              "$? If so, give the combination.",
              "fields", fields=[("Coefficients (c₁, c₂, c₃)", "1,-3,1")],
              steps=[r"$\det A = 16 \neq 0$, so every $\mathbf v$ is in Col $A$; solving gives $c = (1, -3, 1)$.",
                     r"Check: $(1 + 3 + 1,\ 9 - 9 + 1,\ 1 - 3 + 1) = (5, 1, -1)$."],
              final=r"Yes: $\mathbf v = \mathbf a_1 - 3\mathbf a_2 + \mathbf a_3$"),
            P("b", 3, r"For $A = " + mat("1 -1 3; 5 -4 -4; 7 -6 2") + r"$ find a basis of $\operatorname{Nul}A$, the nullity, a basis of $\operatorname{Col}A$ and the rank.",
              "fields", fields=[("Null space basis vector", "16,19,1", "parallel"), ("nullity A", "1"), ("rank A", "2")],
              steps=["RREF: " + D(mat("1 0 -16; 0 1 -19; 0 0 0")),
                     r"$x_1 = 16x_3$, $x_2 = 19x_3$: $\operatorname{Nul}A = \operatorname{Span}\{(16, 19, 1)\}$, nullity 1.",
                     r"Pivot columns 1 and 2 of $A$: $\operatorname{Col}A$ basis $\{(1, 5, 7), (-1, -4, -6)\}$, rank 2."],
              final="Nul basis (16, 19, 1); nullity 1; Col basis = columns 1 and 2; rank 2"),
            P("c", 1, r"$\operatorname{Col}A$ has basis $\left\{(2, -3, 1, 8, 7),\ (-3, 2, 1, -9, 6)\right\}$ and $\operatorname{Nul}A$ has a basis "
                      "of exactly 2 vectors. How many columns does $A$ have?",
              "fields", fields=[("Number of columns", "4")],
              steps=[r"rank $= \dim\operatorname{Col}A = 2$ and nullity $= 2$.",
                     r"Rank theorem: $n = \text{rank} + \text{nullity} = 4$."],
              final="4 columns"),
            P("d", 1, r"$A$ is $4\times5$ with nullity 3. What is the rank of $A$?",
              "fields", fields=[("rank A", "2")],
              steps=[r"rank $= n - $ nullity $= 5 - 3 = 2$."],
              final="rank 2"),
        ]),
        S("Question 5: Eigenvalues and eigenvectors", 8, [
            P("a", 2, r"Find the eigenvalues of $A = " + mat("0 -1 -1; -1 0 -1; -1 -1 0") + "$.",
              "fields", fields=[("Eigenvalues with repeats (list)", "-2,1,1", "set")],
              steps=[r"$A = I - J$ where $J$ is the all-ones matrix, whose eigenvalues are $3, 0, 0$.",
                     r"So $A$ has eigenvalues $1 - 3 = -2$ and $1 - 0 = 1$ (twice). Expanding $\det(A - \lambda I) = -(\lambda + 2)(\lambda - 1)^2$ agrees."],
              final=r"$\lambda = -2,\ 1,\ 1$"),
            P("b", 2, r"Find the eigenvalues of $A = " + mat("1 0 0; -1 2 0; 0 1 3") + "$.",
              "fields", fields=[("Eigenvalues (list)", "1,2,3", "set")],
              steps=["Lower triangular: the eigenvalues are the diagonal entries."],
              final=r"$\lambda = 1,\ 2,\ 3$"),
            P("c-i", 1, r"Which of $\mathbf v_1 = " + vec("1 3 -2") + r"$, $\mathbf v_2 = " + vec("-2 2 1") + r"$, $\mathbf v_3 = " + vec("0 1 -5") +
              r"$ are eigenvectors of $A = " + mat("1 3 6; 2 1 4; 1 0 3") + "$?",
              "mcq", options=[r"$\mathbf v_1$ only", r"$\mathbf v_2$ only", r"$\mathbf v_1$ and $\mathbf v_3$", "None of them"], answer=3,
              steps=[r"$A\mathbf v_1 = (-2, -3, -5)$, $A\mathbf v_2 = (10, 2, 1)$, $A\mathbf v_3 = (-27, -19, -15)$.",
                     r"None of these is a scalar multiple of the vector it came from. (The eigenvalues of $A$ are $1$ and $2 \pm \sqrt{13}$.)"],
              final="None of them."),
            P("c-ii", 1, r"Is $A = " + mat("1 4; 2 3") + r"$ diagonalizable? If yes, find $P$ and $D$ with $A = PDP^{-1}$.",
              "mcq", options=YES_NO, answer=0,
              steps=[r"$\lambda^2 - 4\lambda - 5 = (\lambda - 5)(\lambda + 1)$: distinct eigenvalues $-1, 5$.",
                     r"$\lambda = -1$: $(-2, 1)$. $\lambda = 5$: $(1, 1)$."],
              final=r"Yes: $P = " + mat("-2 1; 1 1") + r",\ D = " + mat("-1 0; 0 5") + "$"),
            P("d", 2, r"$A = " + mat("-4 5; 5 -4") + r"$ has eigenvectors $\mathbf u_1 = (1, 1)$ with $\lambda_1 = 1$ and $\mathbf u_2 = (1, -1)$ with $\lambda_2 = -9$. Find $A^{10}$.",
              "fields", fields=[("Entries of A¹⁰, row by row", "1743392201,-1743392200,-1743392200,1743392201")],
              steps=[r"$A^{10} = SD^{10}S^{-1}$ with $S = " + mat("1 1; 1 -1") + r"$, $S^{-1} = \tfrac12" + mat("1 1; 1 -1") + r"$, $D^{10} = \operatorname{diag}(1, 9^{10})$.",
                     r"$A^{10} = \tfrac12" + mat(r"1+9^{10} 1-9^{10}; 1-9^{10} 1+9^{10}") + r"$ and $9^{10} = 3\,486\,784\,401$."],
              final=r"$A^{10} = " + mat("1743392201 -1743392200; -1743392200 1743392201") + "$"),
        ]),
        S("Question 6: Orthogonality", 3, intro=r"Let $\mathbf u = " + vec("1 1 1") + r"$, $\mathbf v = " + vec("2 1 1") + r"$, $\mathbf w = " + vec("-1 2 -2") + "$.", parts=[
            P("a", 1.5, r"Find $\operatorname{proj}_{\mathbf u}\mathbf v$.", "fields", fields=[("proj_u v", "4/3,4/3,4/3")],
              steps=[r"$\dfrac{\mathbf v\cdot\mathbf u}{\mathbf u\cdot\mathbf u}\mathbf u = \tfrac43(1, 1, 1)$."],
              final=r"$\left(\tfrac43, \tfrac43, \tfrac43\right)$"),
            P("b", 1.5, r"Let $\mathbf z = \mathbf v - \operatorname{proj}_{\mathbf u}\mathbf v$ (perpendicular to $\mathbf u$). Find the projection of $\mathbf w$ onto $\operatorname{Span}\{\mathbf u, \mathbf z\}$.",
              "fields", fields=[("Projection of w", "-1,0,0")],
              steps=[r"$\mathbf z = (\tfrac23, -\tfrac13, -\tfrac13)$, orthogonal to $\mathbf u$.",
                     r"$\dfrac{\mathbf w\cdot\mathbf u}{\mathbf u\cdot\mathbf u} = -\tfrac13$ and $\dfrac{\mathbf w\cdot\mathbf z}{\mathbf z\cdot\mathbf z} = \dfrac{-2/3}{2/3} = -1$.",
                     r"$\hat{\mathbf w} = -\tfrac13(1, 1, 1) - (\tfrac23, -\tfrac13, -\tfrac13) = (-1, 0, 0)$."],
              final=r"$(-1, 0, 0)$"),
        ]),
    ],
}


# --------------------------------------------------------------------------- #
# 7. Final practice paper (photographed, term not printed)
# --------------------------------------------------------------------------- #

FINAL_PRACTICE = {
    "slug": "final-practice-paper",
    "title": "Final Practice Paper",
    "kicker": "CS223 // Final Exam Practice Paper",
    "lede": "A five-question final covering linear systems, linear transformations, determinants, the fundamental "
            "subspaces, eigenvalues and QR. Term not printed on the paper.",
    "meta": ["Chapters 1 to 6", "Points mostly not printed: 1 per part"],
    "duration": 0,
    "sections": [
        S("Question 1", 8, [
            P("1", 1, "Solve the system and check whether it is consistent." + D(system("4x - y + 2z = 0", "2x + y - z = -11", "2x - 2y + z = 3")),
              "fields", fields=[("x", "-5/2"), ("y", "-2"), ("z", "4")],
              steps=[r"$R_2 \leftarrow 2R_2 - R_1$: $(0, 3, -4 \mid -22)$. $R_3 \leftarrow 2R_3 - R_1$: $(0, -3, 0 \mid 6)$.",
                     r"Row 3 gives $y = -2$; row 2: $-6 - 4z = -22 \Rightarrow z = 4$; row 1: $4x + 2 + 8 = 0 \Rightarrow x = -\tfrac52$."],
              final=r"Consistent, unique: $\left(-\tfrac52, -2, 4\right)$"),
            P("2", 1, r"$T:\mathbb R^3 \to \mathbb R^2$ is linear with $T(1, 0, 1) = (1, 2)$ and $T(2, 1, 0) = (4, 1)$. Find $T(3, 2, 1)$. Justify.",
              "mcq", options=["$(5, 3)$", "$(9, 4)$", "$(1, 6)$", "It cannot be determined from the given information"], answer=3,
              steps=[r"Linearity only fixes $T$ on $\operatorname{Span}\{(1,0,1), (2,1,0)\}$. Try $a(1,0,1) + b(2,1,0) = (3, 2, 1)$:",
                     r"the third entry forces $a = 1$, the second forces $b = 2$, but then the first is $1 + 4 = 5 \neq 3$.",
                     r"$(3, 2, 1)$ is outside the span, so its image depends on how $T$ acts on the missing direction.",
                     r"$(5, 3)$ is $T(3, 1, 1)$, the sum of the two given images, and $(9, 4)$ comes from forcing $a = 1$, $b = 2$ anyway."],
              final="Not determined: $(3, 2, 1)$ is not a combination of the two given vectors."),
            P("3", 1, "Solve the homogeneous system by Gauss-Jordan elimination. Are the columns of the coefficient matrix independent?" +
              D(system("x_1 + 2x_2 - 3x_3 = 0", "2x_1 + 6x_2 - 5x_3 = 0", "x_1 - 2x_2 + 7x_3 = 0")),
              "mcq", options=["Only the trivial solution; the columns are independent", "Infinitely many solutions; the columns are dependent",
                              "No solution", "Only the trivial solution; the columns are dependent"], answer=0,
              steps=[r"$R_2 - 2R_1$: $(0, 2, 1)$. $R_3 - R_1$: $(0, -4, 10)$. $R_3 + 2R_2$: $(0, 0, 12)$.",
                     r"Three pivots ($\det = 24$), so the RREF is $I_3$ and $\mathbf x = \mathbf 0$ is the only solution."],
              final="Only the trivial solution; the columns are independent."),
            P("4a", 1, r"$T:\mathbb R^3 \to \mathbb R^3$ with $T(\mathbf e_1) = \mathbf e_1 + 2\mathbf e_2$, $T(\mathbf e_2) = -\mathbf e_2 + 3\mathbf e_3$, "
                       r"$T(\mathbf e_3) = 5\mathbf e_1 - \mathbf e_3$. Find the standard matrix of $T$.",
              "fields", fields=[("Entries row by row", "1,0,5,2,-1,0,0,3,-1")],
              steps=[r"The columns are $T(\mathbf e_1), T(\mathbf e_2), T(\mathbf e_3)$: $(1, 2, 0)$, $(0, -1, 3)$, $(5, 0, -1)$."],
              final=r"$A = " + mat("1 0 5; 2 -1 0; 0 3 -1") + "$"),
            P("4b", 1, "Is this transformation one-to-one? Does it map onto $\\mathbb R^3$?", "mcq",
              options=["One-to-one and onto", "One-to-one but not onto", "Onto but not one-to-one", "Neither"], answer=0,
              steps=[r"$\det A = 1(1 - 0) - 0 + 5(6 - 0) = 31 \neq 0$.",
                     "For a square standard matrix, invertible means both one-to-one and onto."],
              final="Both."),
            P("5a", 1, r"$T:\mathbb R^4 \to \mathbb R^4$, $T(x, y, z, t) = (x - y + z,\ y + z + t,\ 0,\ x + y + 3z + 2t)$. Find the matrix of $T$.",
              "fields", fields=[("Entries row by row (16 numbers)", "1,-1,1,0,0,1,1,1,0,0,0,0,1,1,3,2")],
              steps=[r"$T(\mathbf e_1) = (1, 0, 0, 1)$, $T(\mathbf e_2) = (-1, 1, 0, 1)$, $T(\mathbf e_3) = (1, 1, 0, 3)$, $T(\mathbf e_4) = (0, 1, 0, 2)$ are the columns."],
              final=r"$A = " + mat("1 -1 1 0; 0 1 1 1; 0 0 0 0; 1 1 3 2") + "$"),
            P("5b", 2, "Is $T$ one-to-one? Onto? Is $A$ invertible?", "mcq",
              options=["One-to-one, onto and invertible", "One-to-one only", "Onto only", "Neither one-to-one nor onto; not invertible"], answer=3,
              steps=[r"Row 3 is zero and $R_4 - R_1 - 2R_2 = 0$, so rank $A = 2 < 4$.",
                     "Free variables exist (not one-to-one) and not every row has a pivot (not onto)."],
              final="Neither; $A$ is not invertible."),
        ]),
        S("Question 2", 5, [
            P("1", 1, r"Find the area of the parallelogram formed by $(2, 3)$ and $(1, 4)$.", "fields", fields=[("Area", "5")],
              steps=[r"Area $= \left|\det" + mat("2 1; 3 4") + r"\right| = |8 - 3| = 5$."],
              final="5"),
            P("2", 1, r"$B$ and $C$ are invertible $n\times n$ matrices. Simplify $(-2I + C^{-1})C + B(C - B^{-1} + 2B^{-1}C)$.",
              "mcq", options=["$BC$", "$CB$", "$I + BC$", "$2C + BC$"], answer=0,
              steps=[r"$(-2I + C^{-1})C = -2C + I$.",
                     r"$B(C - B^{-1} + 2B^{-1}C) = BC - I + 2C$.",
                     r"Sum: $-2C + I + BC - I + 2C = BC$."],
              final="$BC$"),
            P("3", 3, r"$A = " + mat("3 0 0; -2 2 0; 7 1 -5") + r"$, $B = " + mat("2 1 3; 0 4 -1; 0 2 0") +
              r"$. Find $\det A$, $\det B$ (cofactors), $\det(AB)$, $\det(2A)$ and $\det(B^{-1}A^3B^T)$.",
              "fields", fields=[("det A", "-30"), ("det B", "4"), ("det(AB)", "-120"), ("det(2A)", "-240"), ("det(B⁻¹A³Bᵀ)", "-27000")],
              steps=[r"$A$ is lower triangular: $3 \cdot 2 \cdot (-5) = -30$.",
                     r"Expand $B$ down column 1: $2\cdot" + det("4 -1; 2 0") + r" = 2(0 + 2) = 4$.",
                     r"$\det(AB) = (-30)(4) = -120$; $\det(2A) = 2^3(-30) = -240$.",
                     r"$\det(B^{-1}A^3B^T) = \tfrac{1}{\det B}(\det A)^3\det B = (-30)^3 = -27000$."],
              final="−30, 4, −120, −240, −27000"),
        ]),
        S("Question 3", 3, intro=D("A = " + mat("2 4 6; 1 3 6; 0 2 4")), parts=[
            P("1", 1, "Find bases for Col $A$ and Nul $A$.", "fields", fields=[("dim Col A", "3"), ("dim Nul A", "0")],
              steps=[r"$\det A = 2(12 - 12) - 4(4 - 0) + 6(2 - 0) = -4 \neq 0$: three pivots.",
                     r"Col $A = \mathbb R^3$ with the three columns as a basis; Nul $A = \{\mathbf 0\}$ (empty basis)."],
              final=r"Col basis: the columns of $A$; Nul $A = \{\mathbf 0\}$"),
            P("2", 1, "Determine the rank and nullity. Are $A$ and $A^T$ invertible?", "mcq",
              options=["rank 3, nullity 0; A and Aᵀ invertible", "rank 2, nullity 1; neither invertible",
                       "rank 3, nullity 0; only A invertible", "rank 2, nullity 1; only Aᵀ invertible"], answer=0,
              steps=[r"rank $3$, nullity $3 - 3 = 0$. $\det A^T = \det A = -4 \neq 0$, so both are invertible."],
              final="rank 3, nullity 0, both invertible"),
            P("3", 1, r"Is $\mathbf v = (-2, 1, 0)$ in Nul $A$? Find a vector in Col $A$.", "mcq", options=YES_NO, answer=1,
              steps=[r"$A\mathbf v = (-4 + 4,\ -2 + 3,\ 0 + 2) = (0, 1, 2) \neq \mathbf 0$, so $\mathbf v \notin \operatorname{Nul}A$.",
                     r"Any column works for Col $A$, e.g. $(2, 1, 0)$; so does $A\mathbf v = (0, 1, 2)$. (Col $A$ is all of $\mathbb R^3$.)"],
              final=r"No; for example $(2, 1, 0) \in \operatorname{Col}A$."),
        ]),
        S("Question 4", 3, intro=D("A = " + mat("5 4 0; 0 3 2; 0 0 2")), parts=[
            P("1a", 1, "Compute the eigenvalues of $A$.", "fields", fields=[("Eigenvalues (list)", "5,3,2", "set")],
              steps=["Upper triangular: the eigenvalues are the diagonal entries."],
              final="5, 3, 2"),
            P("1b", 1, "Is $A$ diagonalizable?", "mcq", options=YES_NO, answer=0,
              steps=[r"Three distinct eigenvalues for a $3\times3$ matrix guarantee three independent eigenvectors."],
              final="Yes."),
            P("2", 1, "Find the eigenvector for the largest eigenvalue.", "fields", fields=[("Eigenvector for λ = 5", "1,0,0", "parallel")],
              steps=[r"$A - 5I = " + mat("0 4 0; 0 -2 2; 0 0 -3") + r"$ forces $x_3 = 0$ and $x_2 = 0$, leaving $x_1$ free."],
              final=r"$(1, 0, 0)$"),
        ]),
        S("Question 5", 2, intro=D("A = " + mat("1 1; 1 -1; 0 1")), parts=[
            P("1", 1, "Use Gram-Schmidt to compute an orthogonal basis for Col $A$.", "fields",
              fields=[("v₁", "1,1,0", "parallel"), ("v₂", "1,-1,1", "parallel")],
              steps=[r"$\mathbf v_1 = \mathbf x_1 = (1, 1, 0)$.",
                     r"$\mathbf x_2\cdot\mathbf v_1 = 1 - 1 + 0 = 0$, so $\mathbf v_2 = \mathbf x_2 = (1, -1, 1)$ already."],
              final=r"$\{(1, 1, 0),\ (1, -1, 1)\}$"),
            P("2", 1, "Compute orthonormal bases and find $Q$ and $R$.", "fields",
              fields=[("R₁₁, R₁₂, R₂₂", "sqrt(2),0,sqrt(3)")],
              steps=[r"Normalize: $\mathbf q_1 = \tfrac{1}{\sqrt2}(1, 1, 0)$, $\mathbf q_2 = \tfrac{1}{\sqrt3}(1, -1, 1)$.",
                     r"$R = Q^TA$: $R_{11} = \mathbf q_1\cdot\mathbf x_1 = \sqrt2$, $R_{12} = \mathbf q_1\cdot\mathbf x_2 = 0$, $R_{22} = \mathbf q_2\cdot\mathbf x_2 = \sqrt3$."],
              final=r"$Q = " + mat(r"\tfrac{1}{\sqrt2} \tfrac{1}{\sqrt3}; \tfrac{1}{\sqrt2} -\tfrac{1}{\sqrt3}; 0 \tfrac{1}{\sqrt3}") + r",\ R = " + mat(r"\sqrt2 0; 0 \sqrt3") + "$"),
        ]),
    ],
}


# --------------------------------------------------------------------------- #
# 8. Final review question bank
# --------------------------------------------------------------------------- #

def bank(n, title, parts):
    return S("Question %s: %s" % (n, title), sum(p["pts"] for p in parts), parts)


FINAL_REVIEW_BANK = {
    "slug": "final-review-bank",
    "title": "Final Review Question Bank",
    "kicker": "CS223 // Final Exam Review // 25 Questions",
    "lede": "A 25-question review set with worked answers for every chapter. Each part counts 1 point. "
            "The original key was checked line by line; corrections are flagged where they apply.",
    "meta": ["Chapters 1 to 6", "25 questions", "Key checked: 4 corrections"],
    "duration": 0,
    "sections": [
        bank(1, "Parameter cases (2 × 2)", [
            P("1", 1, r"Write the matrix form of $\;x_1 + ax_2 = 4,\; ax_1 + 9x_2 = b$.",
              steps=[D(mat("1 a; a 9") + r"\begin{bmatrix}x_1\\x_2\end{bmatrix} = " + vec("4 b"))],
              final=r"$A\mathbf x = \mathbf b$ with $A = " + mat("1 a; a 9") + "$"),
            P("2", 1, "For which values of $a$ is the solution unique?", "fields", fields=[("Excluded values of a (list)", "3,-3", "set")],
              steps=[r"$-a\cdot\text{Eq}_1 + \text{Eq}_2$: $(9 - a^2)x_2 = b - 4a$.",
                     r"Unique when $9 - a^2 \neq 0$."],
              final=r"$a \neq \pm 3$"),
            P("3", 1, "Find the pairs $(a, b)$ giving infinitely many solutions.", "fields",
              fields=[("b when a = 3", "12"), ("b when a = −3", "-12")],
              steps=[r"Need $9 - a^2 = 0$ and $b - 4a = 0$ together: $b = 4a$."],
              final=r"$(3, 12)$ and $(-3, -12)$"),
        ]),
        bank(2, "Parameter cases (3 × 3)", [
            P("1", 1, "For which $a$ is the solution unique?" + D(system("x_1 + 2x_2 + x_3 = 3", "ax_2 + 5x_3 = 10", "2x_1 + 7x_2 + ax_3 = b")),
              "fields", fields=[("Excluded values of a (list)", "-3,5", "set")],
              steps=[r"$R_3 \leftarrow R_3 - 2R_1$: $(0, 3, a - 2 \mid b - 6)$. Then $R_3 \leftarrow aR_3 - 3R_2$:",
                     D(aug("1 2 1 3; 0 a 5 10; 0 0 a^2-2a-15 ab-6a-30", 3)),
                     r"$a^2 - 2a - 15 = (a - 5)(a + 3)$. (At $a = 0$ the scaling step is not allowed, but then the matrix still has three pivots.)"],
              final=r"Unique for $a \neq -3$ and $a \neq 5$"),
            P("2", 1, "Find the pairs $(a, b)$ giving infinitely many solutions.", "fields",
              fields=[("b when a = 5", "12"), ("b when a = −3", "-4")],
              steps=[r"Need $a^2 - 2a - 15 = 0$ and $ab - 6a - 30 = 0$.",
                     r"$a = 5$: $5b - 30 - 30 = 0 \Rightarrow b = 12$.",
                     r"$a = -3$: $-3b + 18 - 30 = 0 \Rightarrow -3b = 12 \Rightarrow b = -4$."],
              note="The key writes b = 4 for a = −3 and then lists the pair as (3, −4). Both are slips: the pair is (−3, −4).",
              final=r"$(5, 12)$ and $(-3, -4)$"),
        ]),
        bank(3, "Inconsistent system", [
            P("1", 1, "Solve " + D(mat("1 2 -3; 2 4 -2; 3 6 -4") + r"\begin{bmatrix}x\\y\\z\end{bmatrix} = " + vec("0 2 3")),
              "mcq", options=["Unique solution", "Infinitely many solutions", "No solution"], answer=2,
              steps=[r"$R_2 - 2R_1$: $(0, 0, 4 \mid 2)$. $R_3 - 3R_1$: $(0, 0, 5 \mid 3)$. $4R_3 - 5R_2$: $(0, 0, 0 \mid 2)$.",
                     r"That row reads $0 = 2$."],
              final="No solution."),
        ]),
        bank(4, "Parametric solution", [
            P("1", 1, "Solve the system." + D(system("x_1 + 2x_2 - 3x_3 - 2x_4 + 4x_5 = 1", "2x_1 + 5x_2 - 8x_3 - x_4 + 6x_5 = 4", "x_1 + 4x_2 - 7x_3 + 5x_4 + 2x_5 = 8")),
              "fields", fields=[("Solution with x₃ = x₅ = 0, as (x₁, …, x₅)", "21,-7,0,3,0")],
              steps=["RREF: " + D(aug("1 0 1 0 24 21; 0 1 -2 0 -8 -7; 0 0 0 1 2 3", 5)),
                     r"Basic $x_1, x_2, x_4$; free $x_3, x_5$: $x_1 = 21 - x_3 - 24x_5$, $x_2 = -7 + 2x_3 + 8x_5$, $x_4 = 3 - 2x_5$.",
                     D(r"\mathbf x = " + vec("21 -7 0 3 0") + " + x_3" + vec("-1 2 1 0 0") + " + x_5" + vec("-24 8 0 -2 1"))],
              note="The key's final vector drops a row and prints −1 + 2a + 8b for x₂; from its own RREF the constant is −7.",
              final="As above, with two free variables."),
        ]),
        bank(5, "Determinant by row reduction", [
            P("1", 1, r"Find $\det" + mat("1 2 3; 4 5 6; 7 8 9") + "$.", "fields", fields=[("det", "0")],
              steps=[r"$R_2 - 4R_1$, $R_3 - 7R_1$, then $R_3 - 2R_2$ gives a zero row."],
              final="0"),
        ]),
        bank(6, "2 × 2 determinant", [
            P("1", 1, r"Find $\det" + mat("a b; c d") + "$.", "mcq", options=["$ad - bc$", "$ab - cd$", "$ac - bd$", "$ad + bc$"], answer=0,
              steps=["Main diagonal product minus the other diagonal product."],
              note="The key prints a·b − c·d, which is a typo: the determinant is ad − bc.",
              final="$ad - bc$"),
        ]),
        bank(7, "Determinants with a parameter", [
            P("a", 1, r"Find $a$ such that $\det" + mat("1 2; 3 a") + r" \neq 0$.", "fields", fields=[("Nonzero for every a except a =", "6")],
              steps=[r"$\det = a - 6$."], final=r"$a \neq 6$"),
            P("b", 1, r"Write $\det" + mat("a b c; d e f; g h i") + "$ by cofactor expansion along row 1.",
              steps=[r"$\det = a(ei - fh) - b(di - fg) + c(dh - eg)$."],
              final=r"$a(ei - fh) - b(di - fg) + c(dh - eg)$"),
        ]),
        bank(8, "Expansion around a chosen pivot", [
            P("1", 1, r"Find $\det A$ using the pivot at row 2, column 3, $A = " + mat("5 4 2 1; 2 3 1 -2; -5 -7 -3 9; 1 -2 -1 4") + "$.",
              "fields", fields=[("det A", "38")],
              steps=[r"$R_1 - 2R_2$, $R_3 + 3R_2$, $R_4 + R_2$ clear column 3; expand along it.",
                     r"$\det A = (-1)^{5}" + det("1 -2 5; 1 2 3; 3 1 2") + r" = -(-38) = 38$."],
              final="38"),
        ]),
        bank(9, "Determinant after row operations", [
            P("1", 1, r"$A = " + mat("1 -2 0 5; 2 3 1 -2; -5 -7 -3 9; 1 -2 -1 4") + r"$ has $\det A = 38$. Matrix $B$ is obtained by: swap $R_1, R_3$; "
                      r"$R_2 \leftarrow R_2 + 2R_3$; $R_3 \leftarrow -3R_3$; $R_4 \leftarrow -2R_4$, giving" +
              D("B = " + mat("-5 -7 -3 9; 4 -1 1 8; -3 6 0 -15; -2 4 2 -8")) + r"Find $\det B$.",
              "fields", fields=[("det B", "-228")],
              steps=[r"Swap: $-38$. Replacement: still $-38$. Scale by $-3$: $114$. Scale by $-2$: $-228$."],
              note="On the source sheet, the B printed under \"Find the determinant of matrix B\" has rows (0, −1, 1, 1) and "
                   "(3, 6, 0, −15), which do not match its own row operations. This version uses the B those operations produce.",
              final=r"$\det B = -228$"),
        ]),
        bank(10, "2 × 2 inverse", [
            P("1", 1, r"Find the inverse of $" + mat("1 2; 3 4") + "$.", "fields", fields=[("Entries of A⁻¹, row by row", "-2,1,3/2,-1/2")],
              steps=[r"Row reduce $[A \mid I]$: $R_2 - 3R_1$, $R_1 + R_2$, $R_2 / (-2)$.",
                     r"Or use $\tfrac{1}{\det A}" + mat("4 -2; -3 1") + r"$ with $\det A = -2$."],
              final=r"$" + mat(r"-2 1; \tfrac32 -\tfrac12") + "$"),
        ]),
        bank(11, "Singular 3 × 3", [
            P("1", 1, r"Find the inverse of $" + mat("1 2 3; 4 5 6; 7 8 9") + "$.", "mcq", options=["It exists", "It does not exist"], answer=1,
              steps=[r"Row reducing $[A \mid I]$ produces a zero row on the left, so $I$ cannot be reached."],
              final="No inverse."),
        ]),
        bank(12, "Dependent columns", [
            P("1", 1, r"Find the inverse of $" + mat("4 2 -4 -2 -6; 2 1 -2 -1 -3; -4 -2 4 2 6; -2 -1 2 1 3; -6 -3 6 3 9") + "$.",
              "mcq", options=["It exists", "It does not exist"], answer=1,
              steps=["Every row is a multiple of (2, 1, −2, −1, −3): rank 1, so the columns are dependent."],
              final="No inverse."),
        ]),
        bank(13, "Invertibility independent of a", [
            P("1", 1, r"For which $a$ is $" + mat("-1 -3 1; 1 a 2; -2 0 2") + "$ invertible?", "mcq",
              options=["Every real a", "a ≠ 6", "a ≠ 0", "No real a"], answer=0,
              steps=[r"$\det = -1(2a) + 3(2 + 4) + 1(0 + 2a) = 12$, whatever $a$ is."],
              final="Every real $a$."),
        ]),
        bank(14, "Invertibility with a parameter", [
            P("1", 1, r"For which $a$ is $" + mat("a -3 1; 1 -1 2; -2 0 2") + "$ invertible?", "fields",
              fields=[("Invertible for every a except a =", "8")],
              steps=[r"Expand along row 1: $a(-2 - 0) + 3(2 + 4) + 1(0 - 2) = -2a + 18 - 2 = 16 - 2a$."],
              note="The key gets −2a + 14 and a ≠ 7: it uses +2 for the last cofactor, but 1·0 − (−1)(−2) = −2.",
              final=r"$a \neq 8$"),
        ]),
        bank(15, "Null space membership", [
            P("1", 1, r"Write $x_1 - 3x_2 - 2x_3 = 0,\; -5x_1 + 9x_2 + x_3 = 0$ in matrix form.",
              steps=[D(mat("1 -3 -2; -5 9 1") + r"\begin{bmatrix}x_1\\x_2\\x_3\end{bmatrix} = " + vec("0 0"))],
              final=r"$A\mathbf x = \mathbf 0$ with $A = " + mat("1 -3 -2; -5 9 1") + "$"),
            P("2", 1, r"Is $\mathbf u = (5, 3, -2)$ in Nul $A$?", "mcq", options=YES_NO, answer=0,
              steps=[r"$A\mathbf u = (5 - 9 + 4,\ -25 + 27 - 2) = (0, 0)$."], final="Yes."),
            P("3", 1, r"If $\mathbf u, \mathbf w \in \operatorname{Nul}A$, show $\mathbf u + \mathbf w \in \operatorname{Nul}A$.",
              steps=[r"$A(\mathbf u + \mathbf w) = A\mathbf u + A\mathbf w = \mathbf 0 + \mathbf 0 = \mathbf 0$."],
              final="Closed under addition."),
        ]),
        bank(16, "Null space and column space", [
            P("1", 1, r"Find a spanning set for Nul $A$, $A = " + mat("3 6 -1 1 -7; 1 -2 2 3 -1; 2 -4 5 8 -4") + "$, and the nullity.",
              "fields", fields=[("nullity A", "2")],
              steps=["RREF: " + D(mat(r"1 0 0 0 0; 0 1 0 \tfrac12 -\tfrac32; 0 0 1 2 -2")),
                     r"$x_1 = 0$, $x_2 = -\tfrac12x_4 + \tfrac32x_5$, $x_3 = -2x_4 + 2x_5$ with $x_4, x_5$ free:",
                     D(r"\operatorname{Nul}A = \operatorname{Span}\left\{" + vec(r"0 -\tfrac12 -2 1 0") + "," + vec(r"0 \tfrac32 2 0 1") + r"\right\}")],
              final="Two spanning vectors, nullity 2"),
            P("2", 1, "Find a spanning set (basis) for Col $A$ and the rank.", "fields", fields=[("rank A", "3")],
              steps=["Pivots in columns 1, 2, 3: take those columns of the original $A$.",
                     D(r"\left\{" + vec("3 1 2") + "," + vec("6 -2 -4") + "," + vec("-1 2 5") + r"\right\}"),
                     "rank $= 5 - 2 = 3$."],
              final="rank 3"),
        ]),
        bank(17, "Row space", [
            P("1", 1, r"Find a spanning set for Row $A$, $A = " + mat("1 1 0; 2 3 -2; -1 -4 6") + "$.", "fields", fields=[("dim Row A", "2")],
              steps=[r"$R_2 - 2R_1$, $R_3 + R_1$, $R_1 - R_2$, $R_3 + 3R_2$ give " + D(mat("1 0 2; 0 1 -2; 0 0 0"))],
              note="The key writes the last step as R3 = R3 + 3R3; the operation that produces its matrix is R3 = R3 + 3R2.",
              final=r"$\operatorname{Row}A = \operatorname{Span}\{(1, 0, 2), (0, 1, -2)\}$"),
        ]),
        bank(18, "Left null space", [
            P("1", 1, r"Find a spanning set for the left null space of $A = " + mat("2 -1; -6 3") + "$.", "fields",
              fields=[("Spanning vector", "3,1", "parallel")],
              steps=[r"Solve $A^T\mathbf x = \mathbf 0$: $A^T = " + mat("2 -6; -1 3") + r"$ reduces to $x_1 = 3x_2$."],
              final=r"$\operatorname{Span}\{(3, 1)\}$"),
        ]),
        bank(19, "Left null space and Aᵀ", [
            P("1", 1, r"Show that the left null space of $A$ is the null space of $A^T$.",
              steps=[r"The left null space is $\{\mathbf x : \mathbf x^TA = \mathbf 0^T\}$.",
                     r"Transpose both sides: $(\mathbf x^TA)^T = A^T\mathbf x = \mathbf 0$.",
                     r"So $\mathbf x$ is in the left null space exactly when $\mathbf x \in \operatorname{Nul}A^T$."],
              final=r"$\operatorname{LeftNul}A = \operatorname{Nul}A^T$"),
        ]),
        bank(20, "Trivial left null space", [
            P("1", 1, r"Find the left null space of $A = " + mat("1 -2 -2; 2 1 3; -1 3 -3") + "$.", "fields",
              fields=[("dim of the left null space", "0")],
              steps=[r"$\det A = -32 \neq 0$, so $A^T$ has a pivot in every column and $A^T\mathbf x = \mathbf 0$ forces $\mathbf x = \mathbf 0$."],
              final=r"$\{\mathbf 0\}$"),
        ]),
        bank(21, "Eigenvalues (2 × 2)", [
            P("1", 1, r"Find the eigenvalues and eigenvectors of $A = " + mat("1 2; 3 4") + "$.", "fields",
              fields=[("Eigenvalues (list)", "(5-sqrt(33))/2,(5+sqrt(33))/2", "set"),
                      ("Eigenvector for the larger eigenvalue", "(sqrt(33)-3)/6,1", "parallel")],
              steps=[r"$\det(A - \lambda I) = \lambda^2 - 5\lambda - 2 = 0 \Rightarrow \lambda = \tfrac{5 \pm \sqrt{33}}{2}$.",
                     r"For $\lambda_2 = \tfrac{5 + \sqrt{33}}{2}$: $3v_1 + (4 - \lambda_2)v_2 = 0 \Rightarrow v_1 = \tfrac{\sqrt{33} - 3}{6}v_2$.",
                     r"For $\lambda_1$: $\mathbf v_1 = \left(\tfrac{-\sqrt{33} - 3}{6},\ 1\right)$."],
              final=r"$\lambda = \tfrac{5 \pm \sqrt{33}}{2}$"),
        ]),
        bank(22, "Eigenvalues (3 × 3, numerical)", [
            P("1", 1, r"Find the eigenvalues of $A = " + mat("-1 2 1; 2 1 -1; 1 -1 -2") + "$ (3 decimals).", "fields",
              fields=[("Eigenvalues (list)", "-3.508,-0.756,2.264", "set")],
              steps=[r"$\det(A - \lambda I) = -\lambda^3 - 2\lambda^2 + 7\lambda + 6 = 0$ has three real roots (no rational ones), found numerically."],
              final=r"$\lambda \approx -3.508,\ -0.756,\ 2.264$"),
            P("2", 1, "Find the eigenvector for the largest eigenvalue.", "fields",
              fields=[("Eigenvector (scaled so the last entry is 1)", "-5.957,-10.221,1", "parallel")],
              steps=[r"Solve $(A - 2.264I)\mathbf v = \mathbf 0$ with $v_3 = 1$."],
              final=r"$\mathbf v_3 \approx (-5.957,\ -10.221,\ 1)$"),
        ]),
        bank(23, "Gram-Schmidt", [
            P("1", 1, r"Apply Gram-Schmidt to the columns of $A = " + mat("1 -2 1; 2 0 1; 3 -2 3") + "$.", "fields",
              fields=[("u₂ (any scale)", "-5,4,-1", "parallel"), ("u₃ (any scale)", "-1,-1,1", "parallel")],
              steps=[r"$\mathbf u_1 = (1, 2, 3)$, $\|\mathbf u_1\|^2 = 14$.",
                     r"$\mathbf u_2 = \mathbf c_2 - \tfrac{-8}{14}\mathbf u_1 = \left(-\tfrac{10}{7}, \tfrac87, -\tfrac27\right)$, $\|\mathbf u_2\|^2 = \tfrac{24}{7}$.",
                     r"$\mathbf u_3 = \mathbf c_3 - \tfrac{12}{14}\mathbf u_1 - \tfrac{-8/7}{24/7}\mathbf u_2 = \left(-\tfrac13, -\tfrac13, \tfrac13\right)$.",
                     r"Check: $\mathbf u_1\cdot\mathbf u_2 = \mathbf u_1\cdot\mathbf u_3 = \mathbf u_2\cdot\mathbf u_3 = 0$."],
              final="Orthogonal basis $\\mathbf u_1, \\mathbf u_2, \\mathbf u_3$"),
        ]),
        bank(24, "QR decomposition", [
            P("1", 1, r"Find the QR decomposition of the same $A = " + mat("1 -2 1; 2 0 1; 3 -2 3") + "$.", "fields",
              fields=[("R₁₁, R₁₂, R₁₃", "sqrt(14),-4sqrt(14)/7,6sqrt(14)/7"), ("R₂₂, R₂₃", "2sqrt(42)/7,-2sqrt(42)/21"), ("R₃₃", "sqrt(3)/3")],
              steps=[r"$Q$ has the normalized $\mathbf u_i$ as columns; $R = Q^TA$, upper triangular.",
                     D(r"R = " + mat(r"\sqrt{14} -\tfrac{4\sqrt{14}}{7} \tfrac{6\sqrt{14}}{7}; 0 \tfrac{2\sqrt{42}}{7} -\tfrac{2\sqrt{42}}{21}; 0 0 \tfrac{\sqrt3}{3}"))],
              final="$A = QR$"),
        ]),
        bank(25, "LU decomposition", [
            P("1", 1, r"Find the LU decomposition of $A = " + mat("1 -2 1; 2 0 1; 3 -2 3") + "$.", "fields",
              fields=[("Multipliers ℓ₂₁, ℓ₃₁, ℓ₃₂", "2,3,1"), ("U, row by row", "1,-2,1,0,4,-1,0,0,1")],
              steps=[r"$R_2 - 2R_1$, $R_3 - 3R_1$, then $R_3 - R_2$. The multipliers fill $L$ below the diagonal.",
                     D(r"L = " + mat("1 0 0; 2 1 0; 3 1 1") + r",\quad U = " + mat("1 -2 1; 0 4 -1; 0 0 1"))],
              final="Check: $LU = A$"),
        ]),
    ],
}


EXAMS = [QUIZ_1_242, MAJOR_1_251, MAJOR_2_251, FINAL_231, FINAL_232, SAMPLE_FINAL_223, FINAL_PRACTICE, FINAL_REVIEW_BANK]

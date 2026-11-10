@head Lecture 3
@title Recurrences
@sources lecture-3-recurrences
@count 35
@tldr A recursive algorithm's running time is an equation that refers to itself, and three methods turn that equation into a normal Big-O.
@why Loops can be read straight off the page, but recursion can't. A recurrence is how you write down what recursion costs. Every divide-and-conquer algorithm from here on needs this, and the Master theorem is one of the most dependable sets of marks in the course.
@connect This uses Lecture 2's counting. Lecture 4's merge sort and quick sort are direct applications, and dynamic programming returns to the same recurrences.
@goals

- Write the recurrence for a recursive algorithm
- Solve recurrences with the iteration method
- Apply the Master theorem and pick the correct case
- Use the extended Master theorem with log factors
- Prove a guess using substitution
  @vocab
  Recurrence | An equation that defines a function in terms of itself on smaller inputs.
  Base case | The input size where the recursion stops.
  Back-substitution | Replacing T(smaller) by its own formula, over and over.
  lg | Logarithm base 2.
  Regularity condition | An extra check needed in Master theorem Case 3.
  @map
  2-12 | Writing recurrences | WRITE | Binary search and factorial
  13-15 | Common recurrences and answers | MEMORIZE | Slide 15's table
  16-19 | Iteration method | WRITE | Both examples
  20-29 | Master theorem | WRITE | Identify a, b, f(n), then the case
  23 | Extended Master theorem | MEMORIZE | The log-factor version
  30-35 | Substitution method | WRITE | Guess and prove by induction

## Writing the recurrence | Slides 2-15 | must

A **recurrence** describes a function in terms of its value on smaller inputs. To write one, answer just two questions.

::steps Turn code into a recurrence
**How many recursive calls, and on what size?** That gives the T(...) terms.
**How much work outside the recursive calls?** That gives the extra term.
**What's the base case?** Usually T(1) or T(0) is a constant.
::
::example Binary search (slide 7)
`mid` is computed, x is compared (constant work, c), and then **one** call is made on half of the array.

T(n) = T(n/2) + c
::
::example Factorial (slide 12)
One call on n − 1, plus a multiplication: constant work.

T(n) = T(n − 1) + 1
::

Slide 15's table is worth committing to memory.

| Recurrence         | What the algorithm does       | Solution       |
| ------------------ | ----------------------------- | -------------- |
| T(n) = T(n/2) + 1  | Halves, constant work         | **O(log n)**   |
| T(n) = T(n/2) + n  | Halves, scans everything      | **O(n)**       |
| T(n) = 2T(n/2) + 1 | Two halves, constant work     | **O(n)**       |
| T(n) = 2T(n/2) + n | Two halves, scans everything  | **O(n log n)** |
| T(n) = T(n−1) + 1  | Removes one, constant work    | **O(n)**       |
| T(n) = T(n−1) + n  | Removes one, scans everything | **O(n²)**      |
| T(n) = 2T(n−1) + 1 | Two calls, each one smaller   | **O(2ⁿ)**      |

::says Slide 8's handwriting | T(n) = T(n) would never end
The size must shrink. A recursive call on the same size never terminates, so usually you'll see **subtraction or division** on the input. That's the slide's point: subtraction gives you the iteration method's easy patterns, and division is the Master theorem's territory.
::
::key

- A recurrence defines a function in terms of smaller inputs
- Count recursive calls for the T terms and non-recursive work for the extra term
- Binary search: T(n) = T(n/2) + c
- Merge-style: T(n) = 2T(n/2) + n is O(n log n)
- T(n) = 2T(n−1) + 1 is exponential
  ::

## Method 1: Iteration | Slides 16-19 | must

Keep expanding the formula until you see a pattern, then jump to the base case.

::steps Solve T(n) = c + T(n/2)
Expand once: T(n) = c + c + T(n/4).
Twice: T(n) = c + c + c + T(n/8).
Pattern after k steps: T(n) = k·c + T(n / 2<sup>k</sup>).
Stop when n / 2<sup>k</sup> = 1, meaning k = lg n.
So T(n) = c·lg n + T(1) = **Θ(lg n)**.
::
::steps Solve T(n) = n + 2T(n/2)
Expand: n + 2(n/2 + 2T(n/4)) = n + n + 4T(n/4).
Again: n + n + n + 8T(n/8).
After i steps: i·n + 2<sup>i</sup>T(n / 2<sup>i</sup>).
Stop at i = lg n: n lg n + n·T(1).
So T(n) = **Θ(n lg n)**.
::

The recursion tree shows why.

::graph T(n) = 2T(n/2) + n: each of the lg n levels does n work in total
n a 200 0 n *
n b 90 75 n/2
n c 310 75 n/2
n d 30 150 n/4
n e 150 150 n/4
n f 250 150 n/4
n g 370 150 n/4
e a b
e a c
e b d
e b e
e c f
e c g
::

::example Subtraction forms, from the handwriting on slide 11

- T(n) = T(n−1) + n: sum n + (n−1) + ... + 1 = **O(n²)**.
- T(n) = T(n−1) + log n: sum of logs = log(n!) = **O(n log n)**.
- T(n) = 2T(n−1) + 1: expands to 1 + 2 + 4 + ... + 2<sup>n−1</sup> = **O(2ⁿ)**.
  ::
  ::key
- Iteration expands the recurrence until a pattern appears
- Stop when the argument reaches the base case
- T(n) = c + T(n/2) is Θ(lg n)
- T(n) = n + 2T(n/2) is Θ(n lg n)
  ::

## Method 2: The Master theorem | Slides 20-29 | must

It's a cookbook for one form:

::formula Master form
T(n) = a·T(n/b) + f(n), where a ≥ 1, b > 1, f(n) > 0
::

| Symbol   | Meaning                    |
| -------- | -------------------------- |
| **a**    | Number of subproblems      |
| **b**    | How much each shrinks      |
| **f(n)** | Work outside the recursion |

**The idea:** compare f(n) with n<sup>log<sub>b</sub>a</sup>. Whichever is bigger wins. On a tie, you get an extra log.

| Case  | Condition                                                                                 | Answer                               |
| ----- | ----------------------------------------------------------------------------------------- | ------------------------------------ |
| **1** | f(n) is smaller: O(n<sup>log<sub>b</sub>a − ε</sup>)                                      | Θ(n<sup>log<sub>b</sub>a</sup>)      |
| **2** | They tie: Θ(n<sup>log<sub>b</sub>a</sup>)                                                 | Θ(n<sup>log<sub>b</sub>a</sup> lg n) |
| **3** | f(n) is bigger: Ω(n<sup>log<sub>b</sub>a + ε</sup>), and a·f(n/b) ≤ c·f(n) for some c < 1 | Θ(f(n))                              |

::analogy A tug-of-war
On one side, the leaves: lots of tiny subproblems (n<sup>log<sub>b</sub>a</sup>). On the other, the root: the work f(n). The stronger side sets the running time. If they are evenly matched, every level contributes equally, so you multiply by the number of levels, lg n.
::
::steps The procedure (slide 22)
Check the recurrence fits the form.
Extract a, b and f(n).
Compute n<sup>log<sub>b</sub>a</sup>.
Compare with f(n) and pick the case. For Case 3, also check regularity.
::

Every example from the slides, worked out:

| Recurrence       | a, b   | n<sup>log<sub>b</sub>a</sup> | f(n)           | Case | Answer        |
| ---------------- | ------ | ---------------------------- | -------------- | ---- | ------------- |
| 2T(n/2) + √n     | 2, 2   | n                            | √n, smaller    | 1    | **Θ(n)**      |
| 9T(n/3) + n      | 9, 3   | n²                           | n, smaller     | 1    | **Θ(n²)**     |
| 2T(n/2) + n      | 2, 2   | n                            | n, tie         | 2    | **Θ(n lg n)** |
| T(2n/3) + 1      | 1, 3/2 | n⁰ = 1                       | 1, tie         | 2    | **Θ(lg n)**   |
| 2T(n/2) + n²     | 2, 2   | n                            | n², bigger     | 3    | **Θ(n²)**     |
| 3T(n/4) + n lg n | 3, 4   | n<sup>0.79</sup>             | n lg n, bigger | 3    | **Θ(n lg n)** |

::example The regularity check for 2T(n/2) + n²
Need a·f(n/b) ≤ c·f(n). Here: 2 × (n/2)² = n²/2 ≤ c·n². So c = 1/2, which is less than 1. It passes.
::
::trap Master doesn't fit everything
T(n) = T(n − 1) + n has subtraction, so **no Master theorem**: use iteration. And Case 3 demands the regularity check; don't skip it.
::
::check Solve T(n) = 4T(n/2) + n.
a = 4, b = 2, n<sup>log₂4</sup> = n². f(n) = n is smaller. Case 1: **Θ(n²)**.
::
::check Solve T(n) = 4T(n/2) + n².
n<sup>log₂4</sup> = n², which ties with f(n). Case 2: **Θ(n² lg n)**.
::

### The extended version (slide 23)

If f(n) = Θ(n<sup>k</sup> log<sup>p</sup> n), compare a with b<sup>k</sup>.

| Comparison        | Sub-case | Answer                                              |
| ----------------- | -------- | --------------------------------------------------- |
| a > b<sup>k</sup> |          | Θ(n<sup>log<sub>b</sub>a</sup>)                     |
| a = b<sup>k</sup> | p > −1   | Θ(n<sup>log<sub>b</sub>a</sup> log<sup>p+1</sup> n) |
| a = b<sup>k</sup> | p = −1   | Θ(n<sup>log<sub>b</sub>a</sup> log log n)           |
| a = b<sup>k</sup> | p < −1   | Θ(n<sup>log<sub>b</sub>a</sup>)                     |
| a < b<sup>k</sup> | p ≥ 0    | Θ(n<sup>k</sup> log<sup>p</sup> n)                  |
| a < b<sup>k</sup> | p < 0    | O(n<sup>k</sup>)                                    |

::example 2T(n/2) + n log n
a = 2, b = 2, k = 1, p = 1. a = b<sup>k</sup> and p > −1, so **Θ(n log² n)**. The basic Master theorem can't handle this, since n log n isn't _polynomially_ larger than n.
::
::key

- Form: T(n) = aT(n/b) + f(n), with a ≥ 1 and b > 1
- Compare f(n) with n to the (log base b of a)
- Case 1: leaves win. Case 2: tie, multiply by lg n. Case 3: root wins, check regularity
- Recurrences that subtract do not fit the Master theorem
- Extended form compares a with b^k and uses the log exponent p
  ::

## Method 3: Substitution | Slides 30-35 | must

Guess the answer, then **prove it with induction**. It's more work, but works on anything if you can guess.

::steps Prove T(n) = 2T(n−1) + 1 with T(0) = 0 solves to 2ⁿ − 1
**Base case:** T(0) = 2⁰ − 1 = 0. True.
**Hypothesis:** assume T(n−1) = 2<sup>n−1</sup> − 1.
**Inductive step:** T(n) = 2(2<sup>n−1</sup> − 1) + 1 = 2ⁿ − 2 + 1 = **2ⁿ − 1**. Done.
::
::steps Prove T(n+1) = 3T(n) + 4 with T(1) = 1 solves to 3ⁿ − 2
**Base case:** T(1) = 3 − 2 = 1. True.
**Hypothesis:** T(n) = 3ⁿ − 2.
**Step:** T(n+1) = 3(3ⁿ − 2) + 4 = 3<sup>n+1</sup> − 6 + 4 = **3<sup>n+1</sup> − 2**. Done.
::
::steps Prove T(n) = 2T(n/2) + n is O(n lg n)
**Goal:** T(n) ≤ c·n lg n.
**Hypothesis:** T(n/2) ≤ c(n/2)lg(n/2).
**Substitute:** T(n) ≤ 2c(n/2)lg(n/2) + n = cn lg(n/2) + n = cn lg n − cn + n.
**Solve for c:** this is ≤ cn lg n whenever −cn + n ≤ 0, i.e. **c ≥ 1**.
::
::trap Keep the exact form
When you assume T(k) ≤ d·g(k), you must prove the **same inequality** with the **same d**. Ending at "d·g(n) + n" and calling it O(g(n)) isn't a proof.
::
::key

- Substitution: guess a solution, then prove it by induction
- Assume the bound for smaller inputs and prove the same bound for n
- Find values of the constants that make the proof work
- T(n) = 2T(n−1) + 1 with T(0) = 0 is 2ⁿ − 1
  ::
  @cheat

### Standard answers

- T(n/2)+1: log n
- T(n/2)+n: n
- 2T(n/2)+1: n
- 2T(n/2)+n: n log n
- T(n−1)+1: n
- T(n−1)+n: n²
- 2T(n−1)+1: 2ⁿ

### Master theorem

- T(n) = aT(n/b) + f(n)
- Compare f(n) with n^(log_b a)
- f smaller: Θ(n^(log_b a))
- Tie: Θ(n^(log_b a) lg n)
- f larger + regularity: Θ(f(n))

### Extended master

- f = n^k log^p n; compare a, b^k
- a > b^k: Θ(n^(log_b a))
- a = b^k, p > −1: multiply by log^(p+1)
- a = b^k, p = −1: multiply by log log n
- a < b^k, p ≥ 0: Θ(n^k log^p n)

### Methods

- Iteration: expand and spot the pattern
- Master: only for T(n/b) form
- Substitution: guess then induct

### Base-case trick

- n/2^k = 1 gives k = lg n
- n − k = 0 gives k = n
  @mcq 26
  Solve T(n) = 2T(n/2) + n.

* Θ(n lg n)

- Θ(n)
- Θ(n²)
- Θ(lg n)

> n^(log₂2) = n ties with f(n), so Case 2 adds a factor of lg n.
> @mcq 25
> Solve T(n) = 9T(n/3) + n.

- Θ(n²)

* Θ(n)
* Θ(n³)
* Θ(n log n)

> n^(log₃9) = n². f(n) = n is smaller, so Case 1.
> @mcq 28
> Solve T(n) = 2T(n/2) + n².

- Θ(n²)

* Θ(n)
* Θ(n² lg n)
* Θ(n lg n)

> f(n) is larger than n, regularity holds with c = 1/2, so Case 3 gives Θ(f(n)).
> @mcq 27
> Solve T(n) = T(2n/3) + 1.

- Θ(lg n)

* Θ(n)
* Θ(1)
* Θ(n^(2/3))

> a = 1, b = 3/2, n⁰ = 1 ties with f(n), so Case 2 gives Θ(lg n).
> @mcq 15
> What is the solution of T(n) = T(n−1) + n?

- O(n²)

* O(n)
* O(n log n)
* O(2ⁿ)

> Summing n + (n−1) + ... + 1 gives n(n+1)/2.
> @mcq 15
> What is the solution of T(n) = 2T(n−1) + 1?

- O(2ⁿ)

* O(n²)
* O(n)
* O(n log n)

> Each level doubles the calls, giving 1 + 2 + 4 + ... + 2^(n−1).
> @mcq 7
> The recurrence for binary search is:

- T(n) = T(n/2) + c

* T(n) = 2T(n/2) + c
* T(n) = T(n/2) + n
* T(n) = T(n−1) + c

> Only one half is searched, with constant work per call.
> @mcq 21
> Case 3 of the Master theorem additionally requires:

- a·f(n/b) ≤ c·f(n) for some c < 1

* a must be equal to b
* f(n) must be a polynomial of degree 1
* n must be a power of 2

> That extra check is called the regularity condition.
> @mcq 21
> In T(n) = 3T(n/4) + n, what is a?

- 3, the number of subproblems

* 4, the shrink factor
* n, the work per call
* 1, because there is one equation

> a is the number of subproblems, and b is how much each shrinks.
> @mcq 15
> Which recurrence CANNOT be solved directly by the basic Master theorem?

- T(n) = T(n−1) + n

* T(n) = 2T(n/2) + n
* T(n) = 4T(n/2) + n²
* T(n) = 3T(n/3) + 1

> The Master theorem needs division of n by b. Subtraction doesn't fit.
> @mcq 23
> By the extended theorem, T(n) = 2T(n/2) + n log n is:

- Θ(n log² n)

* Θ(n log n)
* Θ(n²)
* Θ(n)

> a = b^k with p = 1 > −1, giving n · log^(p+1) n.
> @mcq 31
> Solving T(n) = 2T(n−1)+1, T(0)=0 gives T(3) =

- 7

* 3
* 5
* 8

> T(1)=1, T(2)=3, T(3)=7, which matches 2ⁿ − 1.
> @short 21
> Use the Master theorem to solve T(n) = 4T(n/2) + n log n. State a, b, the comparison and the case.
> ~ a=4, b=2, n², case 1, Θ(n²)
> a = 4 and b = 2, so n^(log₂4) = n². f(n) = n log n is polynomially smaller, so Case 1 gives T(n) = Θ(n²).
> @short 19
> Solve T(n) = n + 2T(n/2) by iteration, showing the pattern.
> ~ pattern, 2^i, lg n, n lg n
> After i expansions, T(n) = i·n + 2^i T(n/2^i). The expansion stops at i = lg n, giving n lg n + n T(1), which is Θ(n lg n).
> @short 33
> Describe the steps of the substitution method.
> ~ guess, induction, hypothesis, constants, prove
> Guess the form of the solution. State the induction goal with an unknown constant. Assume it holds for smaller inputs, substitute, and find values of the constant and n₀ that make the same inequality true.

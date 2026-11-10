@head Lecture 1
@title Algorithm Analysis and Asymptotic Notation
@sources lecture-1-algorithm-analysis-and-asymptotic-notation, lecture-1-algorithm-analysis-and-asymptotic-notation-second-copy, asymptotic-notation-practice
@count 66
@tldr To compare algorithms fairly, count how the number of steps grows as the input grows, and use Big-O, Big-Omega and Big-Theta to describe that growth while ignoring small details.
@why This lecture is the language of the entire course. Every later chapter ends with a sentence like "so it runs in O(n log n)". If that sentence means nothing to you, nothing after it will land. The proofs on these slides also turn up reliably on the major exam, and they follow a simple recipe that you can learn in one sitting.
@connect You've written algorithms in CS102 and CS210. Here you learn how to measure them. Lecture 2 applies this to real loops, and Lecture 3 applies it to recursion.
@goals
- Explain why we analyse algorithms instead of timing programs
- Count primitive operations in pseudocode
- Rank common functions by growth rate
- Prove a Big-O, Big-Omega or Big-Theta claim by finding c and n<sub>0</sub>
- Use a limit to compare two functions
@vocab
Algorithm | A step-by-step procedure for solving a problem in a finite amount of time.
Input size n | How big the problem is, such as how many items are in the array.
Primitive operation | A basic step that takes constant time, such as an assignment or comparison.
Asymptotic | What happens as n becomes very large.
Upper bound | A guarantee that something grows no faster than this.
Lower bound | A guarantee that something grows at least this fast.
@map
2-6 | What algorithm analysis is about | SKIM | Time vs space, and the three questions
7-10 | Worst case, experiments vs theory | MEMORIZE | Limits of experiments
11-16 | Sequential vs binary search | WRITE | Comparisons table
17-21 | Pseudocode, counting operations | WRITE | Count arrayMax yourself
22-31 | Growth rates, best/worst/average | MEMORIZE | The ranking on slide 25
32-45 | Big-O definition and rules | WRITE | Prove the examples
46-60 | Θ, Ω, little-o, little-ω | WRITE | Definitions and proofs
61-65 | Properties and limits | MEMORIZE | Transitivity, the limit rule
Practice deck | Six proofs and a ranking | WRITE | Do them with the recipe below

## What we measure, and why not just time it | Slides 2-10 | must
An **algorithm** is a step-by-step procedure for solving a problem in a finite amount of time. A problem is a mapping from instances to solutions: for sorting, each list maps to its sorted version.

We assess algorithms in two dimensions:

- **Time complexity:** how long it takes, as a function of the input size.
- **Space complexity:** how much memory it uses, as a function of the input size.

There are two ways to measure time.

| | Experimental | Theoretical |
|---|---|---|
| How | Code it, run it, plot time vs size | Analyse the pseudocode |
| Must you implement it? | **Yes** | No |
| Covers all inputs? | No, only those you tried | **Yes** |
| Depends on hardware? | Yes, so compare on the same machine | **No** |

::analogy Comparing two cars
Timing programs is like comparing two cars by having different drivers race them on different days. It tells you a lot about that day. Analysis is like comparing the engines on paper: you learn something true regardless of the weather.
::
::tip The worst case gets the attention
Running time grows with input size. Average case is often hard to determine, so we focus on the **worst case**: it is easier to analyse, and it's the guarantee that matters in games, finance and robotics.
::
::key
- Algorithm analysis looks at time complexity and space complexity as functions of input size
- Experiments require implementation and depend on hardware and chosen inputs
- Theoretical analysis uses pseudocode, covers all inputs and ignores the environment
- We usually focus on worst-case running time
::

## Sequential search versus binary search | Slides 11-16 | must
This comparison shows why any of this matters.

**Sequential search** checks items one at a time. **Binary search** works on a sorted array, checking the middle and discarding half each time.

| Array size n | Sequential comparisons | Binary comparisons |
|---|---|---|
| 128 | 128 | 8 |
| 1,024 | 1,024 | 11 |
| 1,048,576 | 1,048,576 | 21 |
| 4,294,967,296 | 4,294,967,296 | 33 |

::analogy Finding a name in a phone book
Sequential search is reading from page one. Binary search is opening at the middle and throwing away the half that can't contain the name. Four billion names take about 32 halvings.
::
::steps Why binary search takes lg n + 1 comparisons in the worst case
Start with n items.
After one comparison, n/2 remain. After two, n/4.
After k comparisons, n / 2<sup>k</sup> remain.
You stop when one item remains, so 2<sup>k</sup> = n, giving k = lg n. One more comparison checks that last item.
For n = 128: lg 128 + 1 = 7 + 1 = **8**, matching the table.
::
::trap Binary search needs sorted data
It only works if the array is sorted. Slide 12's handwriting points out that sorting is the condition that makes the halving valid.
::
::key
- Sequential search does up to n comparisons
- Binary search does about lg n + 1 comparisons, on sorted data
- Halving turns four billion items into 33 comparisons
::

## Counting operations in pseudocode | Slides 17-21 | must
**Pseudocode** is a high-level description: more structured than English and less detailed than a program. **Primitive operations** are the basic steps, assumed to take constant time: evaluating an expression, assigning a value, indexing into an array, calling a method, returning.

Count `arrayMax`, which finds the largest element:

| Line | Operations (worst case) |
|---|---|
| `currentMax ← A[0]` | 2 |
| `for i ← 1 to n − 1` (tests and setup) | 2 + n |
| `if A[i] > currentMax` | 2(n − 1) |
| `currentMax ← A[i]` | 2(n − 1) |
| `i ← i + 1` | 2(n − 1) |
| `return currentMax` | 1 |
| **Total** | **7n − 1** |

Let a be the time of the fastest operation and b of the slowest. Then a(7n − 1) ≤ T(n) ≤ b(7n − 1). **Either way, it's trapped between two straight lines.** The exact count doesn't matter; the fact that it's linear does.

::key
- Primitive operations are assumed to take constant time
- arrayMax performs 7n − 1 operations in the worst case
- T(n) is bounded between two linear functions
::

## Growth rates | Slides 22-30 | must
Changing hardware changes T(n) by a constant factor, but **doesn't alter the growth rate**. So we ignore constants and lower-order terms. 10<sup>2</sup>n + 10<sup>5</sup> is linear. 10<sup>5</sup>n² + 10<sup>8</sup>n is quadratic.

::formula Memorize this ranking (slide 25)
1 &lt; log n &lt; √n &lt; n &lt; n log n &lt; n² &lt; n³ &lt; 2<sup>n</sup> &lt; n<sup>n</sup>
::
::plot How common running times grow. Exponential leaves the chart almost immediately | input size n | steps | 12 | 40
fn 2^n 5: 2**x
fn n² 4: x**2
fn n log n 3: x*log2(x)
fn n 2: x
fn log n 8: log2(x)
::
::analogy Why the shape beats the constant (slide 28)
One algorithm takes 100n steps, the other 0.01n². At n = 1,000, the second wins easily (10,000 vs 100,000). But at n = 100,000, the first takes 10 million and the second takes 100 million. Beyond n = 10,000, the quadratic loses forever. **Eventually the shape wins.**
::

Slide 26's table makes this concrete. For n = 40, a cubic algorithm at 1 nanosecond per step takes only 64 microseconds, while an exponential algorithm takes around 18 minutes. At n = 60 the exponential takes 31.7 years.

| Case | What it means | Tells you |
|---|---|---|
| **Worst** | Most steps on any input of size n | A guarantee: upper bound on cost |
| **Best** | Fewest steps on any input of size n | A goal: lower bound on cost |
| **Average** | Expected cost on random input | Prediction, but needs a model of "random" |

::trap Big-O is not "the worst case"
They are separate ideas. Worst/best/average say **which inputs** you're considering. O/Ω/Θ say **how you are bounding** the function. You can give a Big-O for the best case.
::
::key
- Hardware changes constants, and not the growth rate
- Ignore constant factors and lower-order terms
- Ranking: 1 < log n < √n < n < n log n < n² < n³ < 2ⁿ < nⁿ
- Worst case gives a guarantee, best case a goal, average case a prediction
::

## Big-O: the upper bound, and how to prove it | Slides 32-45 | must
::formula Definition
f(n) is O(g(n)) if there exist positive constants c and n<sub>0</sub> such that f(n) ≤ c·g(n) for all n ≥ n<sub>0</sub>
::

In plain words: **past some point, f never rises above a constant multiple of g.**

::plot From n₀ onward, f stays beneath c·g | n | time | 10 | 10
curve f(n) 2: 0.5,5 2,2.5 4,3.5 6,5 8,6.2
curve c·g(n) 5: 0.5,1 2,2 4,4.2 6,6.4 8,8.6
guide 3.4,3.3
ticks x: 3.4=n₀
::

::steps The proof recipe that works on nearly every question
Write the inequality you need: f(n) ≤ c·g(n).
Replace every lower-order term with the top-power term, which only makes the left side bigger (valid for n ≥ 1).
Add the coefficients together. That sum is your c.
Take n<sub>0</sub> = 1, or whatever value you needed.
::
::example Prove 2n² + 3n + 4 is O(n²)  (Practice Q1)
For n ≥ 1: 3n ≤ 3n² and 4 ≤ 4n². So 2n² + 3n + 4 ≤ 2n² + 3n² + 4n² = **9n²**.

Pick **c = 9, n<sub>0</sub> = 1**. Done.
::
::example Prove 100n + 10000 is O(n²)  (Practice Q2)
For n ≥ 1: 100n ≤ 100n² and 10000 ≤ 10000n². Sum: 10100n². Pick **c = 10100, n<sub>0</sub> = 1**.

Notice this is true but loose: it's also O(n), which is a tighter statement.
::
::example Prove 5n² − 3n + 20 is O(n²)  (Practice Q3)
The handwriting on this slide gives the trick: **drop the negative term**, as removing −3n only makes the left side bigger. So 5n² − 3n + 20 ≤ 5n² + 20 ≤ 5n² + 20n² = 25n² for n ≥ 1. Pick **c = 25, n<sub>0</sub> = 1**.
::
::example Why n² is NOT O(n)  (slide 40)
Suppose n² ≤ cn for all large n. Divide by n: n ≤ c. But n keeps growing and c is fixed, so it's a contradiction.
::

**Rules** (slide 44): for a polynomial of degree d, f(n) is O(n<sup>d</sup>). Drop lower-order terms, drop constants, use the smallest class, and write the simplest form.

::trap Give the tightest answer
"2n is O(n²)" is technically true, but the slide says to write O(n). In an exam asking for the complexity, give the smallest class that is correct.
::
::check Find c and n₀ for 3n³ + 20n² + 5 being O(n³).
Recipe: 3 + 20 + 5 = 28, so c = 28, n<sub>0</sub> = 1 works. Slide 41 uses c = 4, n<sub>0</sub> = 21, which also works: any valid pair is fine.
::
::key
- f(n) is O(g(n)) if f(n) ≤ c·g(n) for all n ≥ n₀
- Big-O is an upper bound on growth rate
- To prove: bound lower-order terms by the top power and add the coefficients
- Drop negative terms when proving an upper bound
- Drop lower-order terms and constants, and use the smallest class
::

## Omega, Theta and the little ones | Slides 46-64 | must
Three main notations bound a function from different sides.

| Notation | Meaning | Think | Definition |
|---|---|---|---|
| **O(g)** | Upper bound | f ≤ g | f(n) ≤ c·g(n) |
| **Ω(g)** | Lower bound | f ≥ g | c·g(n) ≤ f(n) |
| **Θ(g)** | Tight bound | f = g | c<sub>1</sub>g(n) ≤ f(n) ≤ c<sub>2</sub>g(n) |
| **o(g)** | Strict upper | f < g | Limit of f/g is 0 |
| **ω(g)** | Strict lower | f > g | Limit of f/g is ∞ |

::mnemonic Oh is Over, oMega is under, Theta is Tight
**O** sits **o**ver the function. Ω is **m**inimum, so it's beneath. **Θ** is **T**ight, wrapping it from both sides.
::

**The key theorem (slide 57):** f(n) = Θ(g(n)) **if and only if** f(n) = O(g(n)) and f(n) = Ω(g(n)). To prove Θ, prove both directions.

::example Prove 2n³ − 7n + 1 is Ω(n³)  (Practice Q4)
Need c·n³ ≤ 2n³ − 7n + 1. Try c = 1: that requires n³ − 7n + 1 ≥ 0.

n = 2 gives 8 − 14 + 1 = −5, which fails. n = 3 gives 27 − 21 + 1 = 7, so it holds from there on.

Pick **c = 1, n<sub>0</sub> = 3**.
::
::example Prove 2n³ − 7n + 1 is Θ(n³)  (Practice Q5)
We have the lower bound from Q4. For the upper bound: −7n + 1 is negative for n ≥ 1, so 2n³ − 7n + 1 ≤ 2n³.

Pick **c<sub>1</sub> = 1, c<sub>2</sub> = 2, n<sub>0</sub> = 3**.
::
::example Slide 52: n²/2 − 3n is Θ(n²)
Divide by n²: c<sub>1</sub> ≤ 1/2 − 3/n ≤ c<sub>2</sub>. The middle is always below 1/2, so **c<sub>2</sub> = 1/2**. At n = 7 it equals 1/2 − 3/7 = 1/14, so **c<sub>1</sub> = 1/14 and n<sub>0</sub> = 7**.
::
::check Slide 55: which are true? 1,000,000n² ∈ Ω(n²), (n−1)n/2 ∈ Ω(n²), n/2 ∈ Ω(n²), lg(n²) ∈ Ω(lg n), n² ∈ Ω(n).
All true except **n/2 ∈ Ω(n²)**. Constants don't matter, so the first is fine. (n−1)n/2 is quadratic. n/2 grows slower than n². lg(n²) = 2 lg n. And n² grows faster than n.
::
::key
- Big-Omega is a lower bound, and Big-Theta is a tight bound
- Θ holds exactly when both O and Ω hold
- To prove Θ, prove the upper and lower bounds and use the same n₀
- Little-o and little-ω are strict bounds that aren't asymptotically tight
::

## Using limits, and the useful properties | Slides 61-66 | must
Instead of hunting for constants, you can often compare two functions with a limit.

::formula The limit rule (slide 65)
lim<sub>n→∞</sub> g(n) / f(n) = c > 0 → g(n) ∈ Θ(f(n))
lim<sub>n→∞</sub> g(n) / f(n) = 0 → g(n) ∈ o(f(n))
lim<sub>n→∞</sub> g(n) / f(n) = ∞ → f(n) ∈ o(g(n))
::
::example Compare n²/2 with n³
lim (n²/2) / n³ = lim 1 / (2n) = **0**, so n²/2 ∈ o(n³). The top is negligible beside the bottom.
::

| Property | Holds for | Means |
|---|---|---|
| **Transitivity** | Θ, O, Ω, o, ω | If f ≤ g and g ≤ h, then f ≤ h |
| **Reflexivity** | Θ, O, Ω | f(n) = Θ(f(n)) |
| Not reflexive | o, ω | f can't be strictly smaller than itself |

::tip Log rules you'll keep using (slide 66)
log(xy) = log x + log y. log(x/y) = log x − log y. log x<sup>a</sup> = a log x. Change of base: log<sub>b</sub>a = log<sub>x</sub>a / log<sub>x</sub>b.
::
::check Rank these from fastest to slowest: n log n, 2ⁿ, √n, 1, log n, n!
1, log n, √n, n log n, 2ⁿ, n!. That's the ranking question from the practice deck, using slide 25's order. n! outgrows 2ⁿ.
::
::key
- A limit of a positive constant means Θ
- A limit of 0 means little-o, and a limit of ∞ means the reverse
- All five notations are transitive
- Θ, O and Ω are reflexive, and little-o and little-ω are not
::
@cheat
### Definitions
- O: f ≤ c·g for n ≥ n₀ (upper)
- Ω: c·g ≤ f for n ≥ n₀ (lower)
- Θ: c₁g ≤ f ≤ c₂g (tight)
- Θ holds exactly when O and Ω both hold
- o: limit f/g = 0. ω: limit f/g = ∞
### Growth ranking
- 1 < log n < √n < n
- n < n log n < n² < n³
- n³ < 2ⁿ < n! < nⁿ
### Proof recipe
- Write f ≤ c·g
- Bound smaller terms by the top power
- Drop negative terms for upper bounds
- Add coefficients to get c, take n₀ = 1
### Search facts
- Sequential search: up to n comparisons
- Binary search: about lg n + 1, sorted data only
- arrayMax: 7n − 1 primitive operations
### Cases
- Worst: guarantee, upper bound on cost
- Best: lower bound on cost
- Average: needs a model of random input
### Limit rule
- lim g/f = c > 0: g ∈ Θ(f)
- lim g/f = 0: g ∈ o(f)
- lim g/f = ∞: f ∈ o(g)
@mcq 25
Which ordering of growth rates is correct, from slowest to fastest?
+ log n, √n, n, n log n, n², 2ⁿ
- √n, log n, n, n², n log n, 2ⁿ
- log n, n, √n, n log n, 2ⁿ, n²
- n, log n, √n, n², n log n, 2ⁿ
> Slide 25 gives 1 < log n < √n < n < n log n < n² < n³ < 2ⁿ.
@mcq 39
To show 2n + 10 is O(n), which pair of constants works?
+ c = 3, n₀ = 10
- c = 1, n₀ = 10
- c = 2, n₀ = 10
- c = 3, n₀ = 1
> We need 2n + 10 ≤ cn. With c = 3, this means 10 ≤ n, so n₀ = 10. With c = 2 it can never hold.
@mcq 16
Worst-case comparisons for binary search on 1,024 sorted items?
+ 11
- 10
- 512
- 1,024
> lg 1024 + 1 = 10 + 1 = 11, as in the table on slide 16.
@mcq 57
f(n) is Θ(g(n)) if and only if:
+ f(n) is both O(g(n)) and Ω(g(n))
- f(n) is O(g(n)) or Ω(g(n))
- f(n) is o(g(n)) and ω(g(n))
- f(n) is O(g(n)) but not Ω(g(n))
> Slide 57's theorem: Θ is the intersection of O and Ω.
@mcq 9
Which is a limitation of experimental analysis?
+ Results may not apply to inputs you did not test
- It cannot measure real running time
- It only works on pseudocode
- It ignores the input size
> Slide 9 lists: must implement it, results may not reflect other inputs, and comparisons need the same environment.
@mcq 44
According to the Big-Oh rules, how should 3n + 5 be described?
+ O(n)
- O(3n)
- O(n²)
- O(3n + 5)
> Use the simplest expression of the smallest class. O(n²) is true but not tight.
@mcq 40
Why is n² not O(n)?
+ n ≤ c would have to hold for a fixed c, and n grows without limit
- n² is smaller than n for large n
- Big-O only applies to linear functions
- No constant n₀ can be positive
> Dividing n² ≤ cn by n gives n ≤ c, which cannot hold for all large n.
@mcq 28
Algorithm A takes 100n steps and B takes 0.01n². For very large n:
+ A is faster
- B is faster
- They take the same time
- It depends only on the hardware
> Linear eventually beats quadratic regardless of the constants. The crossover is at n = 10,000.
@mcq 30
The worst-case running time gives:
+ A guarantee for all inputs of size n
- The cost of the easiest input
- The expected cost on random input
- A lower bound on every input
> Worst case is the upper bound on cost, a guarantee for every input.
@mcq 58
If lim f(n)/g(n) = 0 as n goes to infinity, then:
+ f(n) is o(g(n))
- f(n) is Θ(g(n))
- f(n) is ω(g(n))
- g(n) is o(f(n))
> Little-o means f becomes insignificant relative to g.
@mcq 61
Which property does little-o NOT have?
+ Reflexivity
- Transitivity
- Being defined on natural numbers
- Describing an upper bound
> A function cannot be strictly smaller than itself. Transitivity holds for all five notations.
@mcq 21
arrayMax runs in 7n − 1 operations. Why doesn't the 7 matter for its order?
+ Constants change only by a factor, not the growth rate
- Each operation takes zero time
- The 7 cancels with the −1
- Only quadratic terms count
> T(n) is trapped between two linear functions, and constant factors don't alter growth rate.
@short 39
Prove that 4n² + 6n + 2 is O(n²), stating c and n₀.
~ c, n0, 12, n², bound, coefficients
> For n ≥ 1, 6n ≤ 6n² and 2 ≤ 2n², so 4n² + 6n + 2 ≤ 12n². Choose c = 12 and n₀ = 1.
@short 9
Give two reasons to prefer theoretical analysis over experiments.
~ implement, hardware, inputs, independent, all
> It does not require implementing the algorithm, it accounts for all possible inputs, and it is independent of hardware and software, so algorithms can be compared fairly.
@short 57
Explain what you must show to prove f(n) = Θ(g(n)).
~ upper, lower, O, Omega, constants
> You must show both an upper bound, f(n) = O(g(n)), and a lower bound, f(n) = Ω(g(n)), giving constants c₁, c₂ and n₀ so that c₁g(n) ≤ f(n) ≤ c₂g(n) for n ≥ n₀.

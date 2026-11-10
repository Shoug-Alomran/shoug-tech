@head Lecture 8
@title Randomized Algorithms
@sources randomized-algorithms
@count 27
@tldr Adding a coin flip to an algorithm can make it simpler and faster, at the cost of a little uncertainty in either its running time or its answer.
@why This short deck has one major distinction: Las Vegas or Monte Carlo. Almost every question depends on it. You'll also see Karger's min-cut and the microchip calculation.
@connect It fixes the quick sort worst case from Lecture 4. And it's one practical way to handle the hard problems of the final lecture.
@goals

- Distinguish deterministic, Las Vegas and Monte Carlo algorithms
- Explain why randomized quick sort avoids the sorted-input worst case
- Run Karger's min-cut algorithm
- Calculate a Monte Carlo error probability
- Explain pseudorandom numbers
  @vocab
  Deterministic | Same input always gives the same output and the same running time.
  Expected running time | Average time, over the algorithm's own random choices.
  Min-cut | The smallest set of edges whose removal splits a graph in two.
  Seed | The starting value of a random number generator.
  @map
  2-4 | Deterministic vs randomized | MEMORIZE | What depends on random bits
  5-6 | Las Vegas and Monte Carlo | MEMORIZE | The key slide
  7-8 | Randomized quick sort | MEMORIZE | Time no longer depends on input order
  9-12 | Finding a large element | WRITE | Why sampling works
  13-16 | Karger's min-cut | WRITE | Trace contraction
  17-18 | Primality test | SKIM | Fermat's little theorem
  19-21 | Microchip test | WRITE | The 0.9 to the k calculation
  22-26 | Pseudorandom numbers | SKIM | LCG and the seed

## Las Vegas and Monte Carlo | Slides 2-6 | must

A **randomized algorithm** depends on random bits as well as on its input. It's often simpler and faster than a deterministic counterpart.

|              | Las Vegas             | Monte Carlo                              |
| ------------ | --------------------- | ---------------------------------------- |
| Answer       | **Always correct**    | **May be wrong**, with small probability |
| Running time | Random, usually fast  | **Fast and fixed**                       |
| Example      | Randomized quick sort | Karger's min-cut, primality test         |

::mnemonic Latency Varies, Maybe Correct
**L**as **V**egas: **L**atency **V**aries. **M**onte **C**arlo: **M**aybe **C**orrect. The initials carry the whole slide.
::
::analogy Two ways to find your keys
**Las Vegas:** keep searching random places until you find them. You always end up with the keys, but it might take a while. **Monte Carlo:** give yourself exactly five minutes and then leave. You'll be on time, but you may leave without them.
::
::tip Lowering the error
Run a Monte Carlo algorithm several times with independent random bits, and the failure probability shrinks fast. Failing with probability 1/2 in each run gives 0.5<sup>100</sup> after 100 runs, which is less likely than a hardware failure.
::
::key

- A randomized algorithm depends on the input and on random bits
- Las Vegas: always correct, running time varies
- Monte Carlo: fast, but may be wrong with bounded probability
- Repeated independent runs reduce Monte Carlo error
  ::

## Randomized quick sort | Slides 7-8 | must

Ordinary quick sort is **distribution sensitive**: an unlucky input order causes O(n²). If the pivot is chosen **at random**, the time no longer depends on the order of the input. It depends only on the algorithm's own coin flips, giving **O(n log n) on average** for every input.

It's a **Las Vegas** algorithm: the array always ends up sorted, and only the time varies.

::trap The worst case didn't disappear
Randomization doesn't make the worst case impossible. It makes it unrelated to the input, and extremely unlikely. No particular array can cause it reliably.
::
::key

- Randomized pivot removes dependence on input order
- It runs in O(n log n) on average
- It is a Las Vegas algorithm
  ::

## Sampling, min-cut, primes and chips | Slides 9-21 | must

**Find a value at or above the median among 100 billion numbers (slides 9-12).** A deterministic method needs O(n) time. Instead, pick 100 numbers at random and return the largest, in constant time. It's wrong only if all 100 land below the median, with probability (1/2)<sup>100</sup>.

### Karger's min-cut (slides 13-16)

::steps Algorithm
Pick a random edge (u, v).
**Merge** its endpoints into one super-vertex, and delete any self-loops. Keep parallel edges.
Repeat until only two vertices remain.
Return the edges between those two as the cut.
::

It can be wrong, as slide 16 shows: one run finds a cut of size 2 and the other a cut of size 3. So it's **Monte Carlo**, and you run it many times and keep the smallest cut found.

### Primality test (slides 17-18)

::formula Fermat's little theorem
If n is prime, then aⁿ − a ≡ 0 (mod n) for all a in [1, n−1]
::
::example Two quick tests
n = 15, a = 2: 2¹⁵ − 2 = 32766, and 32766 mod 15 = 6, which isn't 0. So 15 is **composite for certain**.

n = 7, a = 3: 3⁷ − 3 = 2184 = 7 × 312, which is 0 mod 7. So 7 is **probably prime**.
::

Failing the test is proof. Passing is only evidence, which is what makes this Monte Carlo.

### The microchip test (slides 19-21)

An untested batch has P(bad) = 0.1. Test k random chips. If all are good, conclude the batch has been tested.

::steps Working out the risk
Chance one chip from an untested batch looks good: 0.9.
Chance k chips in a row all look good: 0.9<sup>k</sup>.
For k = 66: 0.9<sup>66</sup> ≈ 0.00095, which is **less than 1 in 1,000**.
Running time is O(k), **independent of n**. Fast, with high probability of being correct.
::
::check Is the microchip test Las Vegas or Monte Carlo?
**Monte Carlo.** The time is fixed by k, and it might wrongly approve a bad batch.
::
::key

- Sampling 100 values gives an above-median value in constant time, with tiny error
- Karger's algorithm contracts random edges until two vertices remain
- Fermat: failing proves composite, and passing suggests prime
- Microchip test error is 0.9^k, and its time is O(k)
  ::

## Pseudorandom numbers | Slides 22-26 | skim

Computers follow formulas, so they make **pseudorandom** numbers: they look random but are predictable if you know the formula. That's fine for most uses but not for serious security.

::formula Linear congruential method
X<sub>n+1</sub> = (a · X<sub>n</sub> + b) mod m
::

X<sub>0</sub> is the **seed**. The same seed gives the same sequence, which is handy for debugging.

::key

- Computers generate pseudorandom numbers using formulas
- The same seed gives the same sequence
- Pseudorandom numbers aren't suitable for serious security
  ::
  @cheat

### Two types

- Las Vegas: Latency Varies, always correct
- Monte Carlo: Maybe Correct, fast

### Examples

- Randomized quick sort: Las Vegas
- Karger's min-cut: Monte Carlo
- Primality test: Monte Carlo
- Microchip test: Monte Carlo

### Karger

- Pick random edge
- Merge endpoints
- Until two vertices remain
- Repeat for the best cut

### Formulas

- Microchip error: 0.9^k
- Sample error: (1/2)^100
- Fermat: aⁿ − a ≡ 0 mod n
- LCG: X = (aX + b) mod m
  @mcq 6
  A Las Vegas algorithm:

* Always gives a correct answer, with random running time

- Is fast but may be wrong
- Never uses random numbers
- Has a fixed running time and random output

> Slide 6.
> @mcq 6
> A Monte Carlo algorithm:

- Is fast but may be wrong with some probability

* Is always correct
* Has unbounded running time
* Must use no random bits

> Slide 6.
> @mcq 6
> Randomized quick sort is:

- Las Vegas

* Monte Carlo
* Deterministic
* Branch and bound

> The array always ends up sorted, and only the time varies.
> @mcq 16
> Karger's algorithm can give different cut sizes on the same graph because:

- It picks edges at random

* It is deterministic
* It rejects cycles
* It sorts the edges first

> Slide 16 shows runs giving cuts of 2 and 3.
> @mcq 8
> What determines randomized quick sort's running time?

- The random choice of pivots

* The initial order of the array
* The size of the largest element
* The number of equal elements only

> Slide 8.
> @mcq 21
> The chance a bad batch passes 3 chip tests with P(good) = 0.9 is:

- 0.729

* 0.9
* 0.27
* 0.1

> 0.9³ = 0.729.
> @mcq 21
> The running time of the microchip test is:

- O(k), independent of n

* O(n)
* O(n log n)
* O(kn)

> Slide 21.
> @mcq 18
> If aⁿ − a is not 0 mod n for a chosen a, n is:

- Definitely composite

* Definitely prime
* Probably prime
* Even

> Fermat's theorem says a prime would always pass.
> @mcq 23
> In the LCG formula, X₀ is called the:

- Seed

* Modulus
* Multiplier
* Increment

> Slide 23.
> @mcq 12
> Returning the max of 100 random numbers runs in:

- O(1)

* O(n)
* O(log n)
* O(n²)

> It looks at a fixed number of elements, regardless of n.
> @short 6
> Compare Las Vegas and Monte Carlo algorithms with an example of each.
> ~ correct, running time, probability, quick sort, min-cut
> Las Vegas algorithms are always correct but have a random running time, such as randomized quick sort. Monte Carlo algorithms have a bounded running time but can be wrong with some probability, such as Karger's min-cut.
> @short 15
> Describe Karger's algorithm for min-cut.
> ~ random edge, merge, two vertices, repeat, cut
> Repeatedly pick a random edge and merge its endpoints, until two vertices remain, and return the edges between them as the cut. Repeat many times and keep the smallest cut found.
> @short 21
> Calculate the probability a bad batch escapes after k = 10 tests, and state the type of algorithm.
> ~ 0.9, 0.35, Monte Carlo, k
> The probability is 0.9¹⁰ ≈ 0.35. The time is fixed but it can wrongly pass a bad batch, so it's a Monte Carlo algorithm.

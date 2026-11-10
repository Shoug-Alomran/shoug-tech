@head Lecture 2
@title Analysis of Algorithms
@sources lecture-2-analysis-of-algorithms, lecture-2-execution-time-exercises
@count 27
@tldr Most running times come from just looking at the loops: how many times each one runs and how they are nested.
@why You will be handed a piece of code and asked for its complexity on every exam. It's the most practised skill in the course, and there are only a few patterns to recognize. This page collects all of them, and solves all thirteen exercises from the exercise deck.
@connect Lecture 1 defined Big-O. Lecture 2 shows how to get a Big-O from real code. Lecture 3 does the same when the code calls itself.
@goals
- Predict running time from a table of experiments
- Apply the rules for loops, nested loops, sequences and if-else
- Solve all the standard loop patterns on sight
- Calculate T(n) for exchange sort and sequential search
- Use the summation formulas
@vocab
T(n) | The number of basic operations for input size n.
Basic operation | The instruction you decide to count, usually the innermost one.
W(n) | Worst-case number of basic operations.
A(n) | Average-case number of basic operations.
Summation Σ | A compact way of writing "add all of these".
@map
2-9 | Why compare algorithms mathematically | SKIM | The 3-Sum doubling experiment
10-15 | Cost of statements and loops | WRITE | Build the cost tables
16 | Four general rules | MEMORIZE | Loops, nesting, sequences, if-else
17-19 | T(n) worked examples | WRITE | Add, exchange sort, sequential search
20-23 | Summations and logs | MEMORIZE | Know the arithmetic series
24-27 | Complexity categories | SKIM | Names for common orders
Exercises | 13 loop problems | WRITE | The core skill, all solved below

## Predicting from experiments, and why we stop | Slides 4-9 | know
Slide 8 times **3-Sum**, which counts triples that add to zero using three nested loops:

| n | Seconds |
|---|---|
| 1,000 | 0.1 |
| 2,000 | 0.8 |
| 4,000 | 6.4 |
| 8,000 | 51.1 |
| 16,000 | ? |

Each time n doubles, the time multiplies by about 8. Since 8 = 2³, this looks like n³. So the answer for 16,000 is around 51.1 × 8 ≈ **409 seconds**.

::tip The doubling trick
Double n and divide the new time by the old. A ratio near **2** suggests n, near **4** suggests n², and near **8** suggests n³.
::

But slide 9 says programs depend on how they're coded, which computer they run on, and what data they're given. We want analysis independent of all three.

::key
- Doubling n and comparing times reveals the power of n
- Programs depend on implementation, computer and data
- Analysis must be independent of these
::

## The four rules | Slides 10-16 | must
Each statement has a cost, and the total is the sum of (cost × how many times it runs).

::example Reading a simple loop (slide 14)
| Statement | Cost | Times |
|---|---|---|
| `i = 1` | c1 | 1 |
| `sum = 0` | c2 | 1 |
| `while (i <= n)` | c3 | **n + 1** |
| `i = i + 1` | c4 | n |
| `sum = sum + i` | c5 | n |

Note the loop test runs **one more time** than the body, because the last test is the one that fails. Total is c1 + c2 + (n+1)c3 + n·c4 + n·c5, which is proportional to n.
::

| Rule | How to apply it | Example |
|---|---|---|
| **Loop** | Body cost × iterations | Loop n times with O(1) body → O(n) |
| **Nested loops** | Multiply the sizes of all loops | n × n → O(n²) |
| **Consecutive statements** | Add them, and the largest dominates | O(n) then O(n²) → O(n²) |
| **If/else** | Test + the **larger** branch | Takes O(1) or O(n) → O(n) |

::mnemonic Inside Multiplies, After Adds
Code **inside** a loop **multiplies** by that loop. Code **after** a loop **adds** to it. Most mistakes come from confusing those two.
::
::trap The if statement isn't always the bigger branch
It's the worst-case bound: test plus the larger branch. In a best-case analysis, the shorter branch might apply.
::
::key
- Total cost is the sum of cost × times executed
- A while test runs one more time than the body
- Nested loops multiply and consecutive blocks add
- If/else costs the test plus the larger branch
::

## All the loop patterns | Exercise deck | must
Almost every code question is one of these. Learn to recognize what the **loop variable** does.

| Loop counter does | Iterations | Complexity |
|---|---|---|
| `i++` or `i--` up to n | n | O(n) |
| `i += 2` (any constant) | n / 2 | O(n) |
| `i *= 2` | log<sub>2</sub> n | O(log n) |
| `i /= 2` | log<sub>2</sub> n | O(log n) |
| `p += i` while p < n | √(2n) | O(√n) |

::mnemonic Add is Linear, Multiply is Log
A counter that **adds** a constant gives **linear** time. A counter that **multiplies** gives **log** time.
::

Here are the thirteen exercises, solved.

| # | Code | Work | Answer |
|---|---|---|---|
| 1 | Sum an array with one loop | n passes | **O(n)** |
| 2 | `for(i=n; i>0; i--)` | n passes | **O(n)** |
| 3 | Add two matrices, two nested loops to n | n × n | **O(n²)** |
| 4 | `for(i=0; i<n; i+=2)` | n/2 | **O(n)** |
| 5 | `for i<n` then `for j<i` | 0+1+...+(n−1) = n(n−1)/2 | **O(n²)** |
| 6 | `for(i=1; p<n; i++) p=p+i` | see below | **O(√n)** |
| 7 | `for(i=1; i<n; i=i*2)` | Doubling | **O(log n)** |
| 8 | `for(i=n; i>=1; i=i/2)` | Halving | **O(log n)** |
| 9 | Two separate loops to n | n + n = 2n | **O(n)** |
| 10 | Log loop computes p, then log loop to p | log n + log log n | **O(log n)** |
| 11 | `Method_2(n/2) + Method_2(n/2)` | T(n) = 2T(n/2) + c | **O(n)** |
| 12 | Mystery1 | see below | **O(n³ log n)** |
| 13 | Mystery2 | see below | **O(n⁵ log n)** |

::steps Exercise 6: why it is √n
After k iterations, p = 1 + 2 + ... + k = k(k+1)/2.
The loop stops when p ≥ n, so k(k+1)/2 ≥ n.
That is about k²/2 ≥ n, giving k ≈ √(2n).
So the complexity is **O(√n)**.
::
::steps Exercise 12: Mystery1, one loop at a time, from the inside
Inner loop: `k` doubles until it reaches j, so log j steps.
Middle loop: j runs from 1 to i², so the work is about i² × log(i²) = 2i² log i.
Outer loop: i runs from 1 to n, summing 2i² log i, which is proportional to **n³ log n**.
::
::steps Exercise 13: Mystery2 calls Mystery1
For each i, j runs from 1 to i, and each call costs about j³ log j.
Summing up to i gives about i⁴ log i.
Summing i from 1 to n gives **n⁵ log n**.
::
::says Typing slips in the exercise deck
Exercise 2 is printed as `for(i=n; n>0; i--)`, and the summary slide as `for(i=n; i<1; i--)`, which would never run. Exercise 10 starts `i=0` and multiplies by 2, which would loop forever. Read them as `i>0`, `i>=1` and `i=1`, which is clearly what's intended.
::
::trap Sequence, not nesting
Exercise 9 has two loops one **after** the other. That's O(n), not O(n²). Check the braces before you multiply.
::
::check What is the complexity of `for(i=1; i<n; i=i*3)`?
**O(log n)**, specifically log base 3. Multiplying by any constant above 1 gives a logarithm, and the base doesn't change the order.
::
::key
- Additive counters give O(n), even with larger constant steps
- Multiplying or dividing counters give O(log n)
- A counter accumulating 1+2+...+k takes O(√n) iterations
- Nested loops where j depends on i often sum to n(n−1)/2, which is O(n²)
- Work from the innermost loop outward
::

## Exact counts: three classics | Slides 17-19 | must
For an exact T(n), pick a **basic operation** and count how many times it runs.

**Adding an array:** the loop always does n passes, whatever the values. **T(n) = n**.

**Exchange sort:** the outer loop makes n − 1 passes, and the inner one makes n−1, n−2, ..., 1 passes.

::formula Slide 18
T(n) = (n−1) + (n−2) + ... + 1 = n(n−1)/2
::

Throw away the low-order n/2 and it's Θ(n²).

**Sequential search** depends on the input:

| Case | Basic operations | When |
|---|---|---|
| Best | B(n) = 1 | x is the first item |
| Worst | W(n) = n | x is last or absent |
| Average (x is in the array) | A(n) = (n + 1)/2 | Each position equally likely |

::example Exchange sort on 5 items
Passes of the inner loop: 4 + 3 + 2 + 1 = 10. The formula gives 5 × 4 / 2 = **10**.
::
::key
- Count a single basic operation to get T(n)
- Adding an array has T(n) = n for every input
- Exchange sort has T(n) = n(n−1)/2, which is Θ(n²)
- Sequential search: W(n) = n, and average about (n+1)/2
::

## Formulas to carry with you | Slides 20-27 | must
| Series | Sum | Grows like |
|---|---|---|
| 1 + 2 + ... + n | n(n+1)/2 | n² |
| 1² + 2² + ... + n² | n(n+1)(2n+1)/6 | n³ |
| 1³ + 2³ + ... + n³ | n²(n+1)²/4 | n⁴ |
| Geometric: 1 + x + ... + xⁿ | (x<sup>n+1</sup> − 1)/(x − 1) | xⁿ |

::mnemonic Sum raises the power
Adding i<sup>k</sup> from 1 to n gives something that grows like n<sup>k+1</sup>. Sum of i is n², sum of i² is n³.
::

**Common complexity categories (slide 27):** Θ(lg n), Θ(n), Θ(n lg n), Θ(n²), Θ(n³), Θ(2ⁿ). A function in Θ(n²) is called **quadratic-time**.

::key
- Sum of 1 to n is n(n+1)/2
- Summing i to the k grows like n to the (k+1)
- Geometric series is dominated by the largest term
- Θ(n²) algorithms are called quadratic-time
::
@cheat
### Loop patterns
- i++ or i+=c: O(n)
- i*=2 or i/=2: O(log n)
- p+=i while p<n: O(√n)
- Nested to n: O(n²)
- j<i nested: n(n−1)/2 = O(n²)
### Rules
- Nested: multiply
- Sequence: add, largest wins
- If/else: test + larger branch
- While test runs n+1 times
### Exact counts
- Exchange sort: n(n−1)/2
- Sequential: W = n, A = (n+1)/2
- Add array: T = n
### Series
- Σi = n(n+1)/2
- Σi² = n(n+1)(2n+1)/6
- Σi³ = n²(n+1)²/4
- Geometric: (xⁿ⁺¹ − 1)/(x − 1)
### Doubling test
- Ratio 2: linear
- Ratio 4: quadratic
- Ratio 8: cubic
@mcq Exercises
What is the complexity of `for(i=1; i<n; i=i*2) { x++; }`?
+ O(log n)
- O(n)
- O(√n)
- O(n log n)
> i takes values 1, 2, 4, 8..., so it reaches n after log₂ n steps.
@mcq Exercises
What is the complexity of two separate, consecutive loops, each running from 0 to n?
+ O(n)
- O(n²)
- O(log n)
- O(n log n)
> Consecutive statements add: n + n = 2n, which is O(n).
@mcq Exercises
`p=0; for(i=1; p<n; i++) p=p+i;` runs in:
+ O(√n)
- O(n)
- O(log n)
- O(n²)
> p equals k(k+1)/2 after k iterations, so k is about √(2n).
@mcq 18
Exchange sort performs how many comparisons on 6 items?
+ 15
- 36
- 30
- 6
> n(n−1)/2 = 6 × 5 / 2 = 15.
@mcq 16
A loop running n times contains a statement that costs O(log n). Total?
+ O(n log n)
- O(n + log n)
- O(log n)
- O(n²)
> A statement inside a loop is multiplied by the number of iterations.
@mcq 14
In `while (i <= n)` with i from 1, how many times does the test run?
+ n + 1
- n
- n − 1
- 2n
> The final failing test counts, so one more than the body's n executions.
@mcq 8
Timing doubles from 6.4 s to 51.1 s as n doubles from 4,000 to 8,000. Likely order?
+ n³
- n²
- n
- n log n
> The ratio is about 8, and 2³ = 8.
@mcq 19
Average comparisons for sequential search when x is present, with all positions equally likely:
+ (n + 1)/2
- n/4
- n
- log n
> The average of positions 1 through n is (n+1)/2.
@mcq 20
1 + 2 + ... + 100 equals:
+ 5,050
- 5,000
- 10,000
- 4,950
> n(n+1)/2 = 100 × 101 / 2 = 5,050.
@mcq Exercises
`for(i=0;i<n;i++) for(j=0;j<i;j++) x++;` executes x++ how many times?
+ n(n−1)/2
- n²
- n
- n(n+1)
> j runs 0, 1, ..., n−1 times across the outer iterations, summing to n(n−1)/2.
@mcq Exercises
A recursive function does `f(n/2) + f(n/2)` plus constant work. Its complexity is:
+ O(n)
- O(log n)
- O(n log n)
- O(2ⁿ)
> T(n) = 2T(n/2) + c. The recursion tree's levels sum to about 2n nodes.
@mcq 16
Which rule applies to `if (a) O(1) else O(n)` in worst-case analysis?
+ O(n): test plus the larger branch
- O(1): take the smaller branch
- O(n²): multiply the branches
- O(n + 1): both branches always run
> Slide 16: never more than the test plus the larger of the two.
@short Exercises
Find the complexity of `for(i=0;i<n;i++) for(j=1;j<n;j=j*2) x++;` and justify it.
~ n, log, multiply, nested, inner
> The outer loop runs n times and the inner loop doubles j, so it runs log n times. Nested loops multiply, giving O(n log n).
@short 16
State the four general rules for estimating running time.
~ loop, nested, consecutive, if, larger
> A loop costs its body times its iterations. Nested loops multiply all their sizes. Consecutive statements add. If/else costs the test plus the larger of the two branches.
@short 8
Explain how you would predict the runtime of 3-Sum at n = 16,000 from slide 8.
~ doubling, ratio, 8, cubic, 409
> Each doubling of n multiplies time by about 8, which suggests cubic growth. So 51.1 × 8 gives around 409 seconds at n = 16,000.

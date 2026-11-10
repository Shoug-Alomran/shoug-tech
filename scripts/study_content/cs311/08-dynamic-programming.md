@head Lecture 6
@title Dynamic Programming
@sources lecture-6-dynamic-programming
@count 83
@tldr When subproblems repeat, solve each one once, store the answer in a table, and build up to the final answer from the bottom.
@why At 83 slides this is the largest deck in the course, and one where filling tables by hand brings real exam marks. Once you see the two questions that define any DP solution, matrix chain and knapsack stop feeling like separate topics.
@connect Greedy failed on 0/1 knapsack and on some coin sets. Divide and conquer wasted effort when subproblems overlapped. DP fixes both problems.
@goals

- Compare DP with greedy and divide and conquer
- State when DP can be applied
- Fill in the matrix chain table and rebuild the parenthesization
- Fill in the 0/1 knapsack table and recover the items
- Apply DP to coin change
  @vocab
  Subproblem | A smaller version of the problem.
  Overlapping | The same subproblem appears again and again.
  Optimal substructure | The best overall answer contains the best answers to its subproblems.
  Bottom-up | Solving the smallest cases first and building upward.
  Memoization | Storing results to avoid recomputing.
  @map
  3-6 | What DP is; vs greedy and D&C | MEMORIZE | Slides 5 and 6's comparison tables
  7-14 | Fibonacci | WRITE | Why recursion explodes
  15-38 | Matrix chain product | WRITE | Fill the table, recover the split
  39 | The general technique | MEMORIZE | Three ingredients
  40-73 | 0/1 knapsack | WRITE | Build the table and find the items
  74-79 | Binomial, coin change | WRITE | Coin DP table
  80-83 | When it applies | MEMORIZE | Optimal substructure, overlap

## What dynamic programming is | Slides 3-6 | must

"Programming" here means **planning**, as in filling in a table. It was invented by Richard Bellman in the 1950s to solve optimization problems.

::steps The main idea
Solve smaller, overlapping subproblems.
Record the solutions in a table so each is only solved once.
The final state of the table is, or contains, the solution.
::

|             | Greedy                | Dynamic programming                      |
| ----------- | --------------------- | ---------------------------------------- |
| Decides by  | What's best right now | Considering earlier subproblem solutions |
| Looks back? | Never                 | Yes                                      |
| Optimal?    | Sometimes             | **Yes, when it applies**                 |

|                 | Divide and conquer | Dynamic programming |
| --------------- | ------------------ | ------------------- |
| Direction       | Top-down           | Bottom-up           |
| Subproblems     | **Independent**    | **Overlapping**     |
| Stores results? | No                 | Yes                 |

::analogy Writing the answer on the board
Ask a class "what's 8 + 7 + 5?" They work out 20. Now ask "what's 8 + 7 + 5 + 3?" Nobody re-adds. They use 20 and add 3. DP is writing past answers on the board.
::
::mnemonic Overlap means Store
If subproblems **o**verlap, you must **s**tore. Independent subproblems: divide and conquer. Overlapping: dynamic programming.
::
::key

- DP solves overlapping subproblems once and stores them in a table
- Greedy never looks back, while DP uses earlier results
- D&C subproblems are independent, DP's overlap
- DP is typically built bottom-up
  ::

## Fibonacci: the clearest example | Slides 7-14 | must

::formula Recurrence
f(0) = 0, f(1) = 1, f(n) = f(n−1) + f(n−2)
::

Calling this recursively recomputes the same values over and over.

::graph The recursive tree for f(4): f(2) is computed twice
n a 200 0 f(4)
n b 100 70 f(3)
n c 310 70 f(2) *
n d 40 140 f(2) *
n e 160 140 f(1)
n f 260 140 f(1)
n g 370 140 f(0)
e a b
e a c
e b d
e b e
e c f
e c g
::

The bottom-up version just fills an array from left to right.

| Version      | Code idea                | Time      | At n = 100            |
| ------------ | ------------------------ | --------- | --------------------- |
| Recursive    | `fib(n-1) + fib(n-2)`    | **O(2ⁿ)** | About 13 days at 1 ns |
| Bottom-up DP | `f[i] = f[i-1] + f[i-2]` | **O(n)**  | **101 ns**            |

::key

- Plain recursion recomputes overlapping subproblems and takes O(2ⁿ)
- Bottom-up DP fills a table in O(n)
- At n = 100, the difference is 13 days versus 101 nanoseconds
  ::

## Matrix chain multiplication | Slides 15-38 | must

Multiplying a d × e matrix by an e × f matrix costs **d × e × f** operations. The order of multiplication doesn't change the answer but it hugely changes the cost.

::example Slide 17: B is 3×100, C is 100×5, D is 5×5
**(B·C)·D:** B·C costs 3×100×5 = 1500 and gives a 3×5 matrix. Times D: 3×5×5 = 75. Total **1575**.

**B·(C·D):** C·D costs 100×5×5 = 2500. B times that: 3×100×5 = 1500. Total **4000**.
::

Trying every parenthesization is exponential (nearly 4ⁿ), and both greedy ideas fail with counterexamples (slides 19 and 20). DP asks one clever question: **where's the last multiplication?**

::formula Characterizing equation
m[i, j] = min over k of { m[i, k] + m[k+1, j] + p<sub>i−1</sub> · p<sub>k</sub> · p<sub>j</sub> }
m[i, i] = 0
::

Read it as: cost of the left part, plus cost of the right part, plus cost of multiplying those two results.

::steps Fill the table for slide 28's six matrices
Dimensions p = 10, 20, 5, 15, 50, 10, 15 (so A1 is 10×20, A2 is 20×5, and so on).
Length 1 entries are all 0.
Length 2: m[1,2] = 10×20×5 = 1000; m[2,3] = 1500; m[3,4] = 3750; m[4,5] = 7500; m[5,6] = 7500.
Length 3: m[1,3] = min(0 + 1500 + 10×20×15, 1000 + 0 + 10×5×15) = min(4500, **1750**) = 1750.
Continue through lengths 4 and 5, one diagonal at a time.
Final: m[1,6] = **8750**, with the best split at k = 2.
::

To rebuild the answer, store in s[i, j] the k that gave the minimum.

::example Recovering the parenthesization
s[1,6] = 2 gives (A1A2)(A3...A6). s[3,6] = 5 gives (A3A4A5)A6. s[3,5] = 4 gives (A3A4)A5.

Result: **((A1A2)(((A3A4)A5)A6))**.
::

**Time: O(n³)** (O(n²) table entries, each taking O(n)). **Space: O(n²)**.

::mnemonic Length by Length
The table fills **diagonal by diagonal**, by chain length, since each entry needs shorter chains.
::
::trap p subscripts are off by one
A<sub>i</sub> has dimensions p<sub>i−1</sub> × p<sub>i</sub>. So A3 here is p<sub>2</sub> × p<sub>3</sub> = 5 × 15. Write out the p list before you begin.
::
::check Cost of the chain A(2×3), B(3×5), C(5×2) with the best order?
(AB)C = 2×3×5 + 2×5×2 = 30 + 20 = 50. A(BC) = 3×5×2 + 2×3×2 = 30 + 12 = **42**. So A(BC). It matches m[1,3] = 42 in slide 36's table.
::
::key

- Multiplying d×e by e×f costs d·e·f
- m[i,j] = min over k of left + right + p(i−1)·p(k)·p(j)
- Fill the table by chain length, diagonal by diagonal
- Store the best k in s[i,j] to recover the parenthesization
- Time is O(n³) and space is O(n²)
  ::

## 0/1 knapsack | Slides 40-73 | must

You must take each item **entirely or not at all**. Greedy fails here, and DP handles it.

Define **B[k, w]** as the best benefit using the first k items with capacity w. For item k there are only two options: **skip it or take it**.

::formula Recurrence (slides 44-45)
If w<sub>k</sub> > w: B[k, w] = B[k−1, w]
Otherwise: B[k, w] = max( B[k−1, w], B[k−1, w − w<sub>k</sub>] + b<sub>k</sub> )
::
::example Fill the table: W = 5, items (2,3), (3,4), (4,5), (5,6) as (weight, benefit)

| i \ w       | 0   | 1   | 2   | 3   | 4   | 5     |
| ----------- | --- | --- | --- | --- | --- | ----- |
| **0**       | 0   | 0   | 0   | 0   | 0   | 0     |
| **1** (2,3) | 0   | 0   | 3   | 3   | 3   | 3     |
| **2** (3,4) | 0   | 0   | 3   | 4   | 4   | **7** |
| **3** (4,5) | 0   | 0   | 3   | 4   | 5   | 7     |
| **4** (5,6) | 0   | 0   | 3   | 4   | 5   | 7     |

The highlighted cell: i = 2, w = 5. Skip gives B[1,5] = 3. Take gives B[1, 2] + 4 = 3 + 4 = 7. Take it.

The best benefit is the bottom-right value: **7**.
::
::steps Recover which items were taken (slides 70-73)
Start at i = 4, k = 5. B[4,5] = 7 and B[3,5] = 7: same value, so item 4 is **out**.
i = 3: B[3,5] = 7 and B[2,5] = 7: same, so item 3 is **out**.
i = 2: B[2,5] = 7 and B[1,5] = 3: different, so item 2 is **in**. Reduce k to 5 − 3 = 2.
i = 1: B[1,2] = 3 and B[0,2] = 0: different, so item 1 is **in**. k = 0, stop.
Optimal knapsack = **{1, 2}**, benefit 7.
::

**Running time: O(nW)**, against brute force's O(2ⁿ).

::mnemonic Different means Delivered
Compare a cell with the cell **above** it. If they're **different**, the item was **delivered** into the knapsack.
::
::trap Greedy on 0/1
On slide 41's data, picking by ratio works, but in general, taking the best-ratio item may leave the bag badly filled. Only the table is guaranteed.
::
::key

- B[k,w] is the best benefit using the first k items and capacity w
- Skip it: B[k−1,w]. Take it: B[k−1,w−wk] + bk
- Answer is at B[n,W]
- Running time is O(nW), brute force is O(2ⁿ)
- If a cell differs from the one above, that item was taken
  ::

## Coin change, and when DP applies | Slides 74-83 | must

Greedy failed for some coin sets, and DP doesn't.

::formula Recurrence
C[0] = 0
C[p] = min over coins d<sub>i</sub> ≤ p of { 1 + C[p − d<sub>i</sub>] }
::
::example Slide 79: amount 5, coins {1, 2, 3}

| p    | 0   | 1   | 2   | 3   | 4   | 5     |
| ---- | --- | --- | --- | --- | --- | ----- |
| C[p] | 0   | 1   | 1   | 1   | 2   | **2** |

C[5] = 1 + min(C[4], C[3], C[2]) = 1 + 1 = **2**, using coins {2, 3}.
::

Binomial coefficients follow the same pattern: C(n, k) = C(n−1, k−1) + C(n−1, k), with C(n, 0) = C(n, n) = 1.

DP applies when the problem has:

| Ingredient               | Meaning                                                  |
| ------------------------ | -------------------------------------------------------- |
| **Simple subproblems**   | Defined with a few variables, like i, j, k               |
| **Optimal substructure** | The best answer contains the best answers to subproblems |
| **Subproblem overlap**   | The same subproblems appear repeatedly                   |

::mnemonic SOS
A DP problem sends **SOS**: **S**imple subproblems, **O**ptimal substructure, **S**ubproblem overlap.
::
::tip The crucial step
Slide 80 says the crucial step is deriving a **recurrence** that relates the answer to smaller subinstances. Once you have the recurrence, the table is just arithmetic.
::
::key

- Coin change: C[p] = min of 1 + C[p − di]
- DP needs simple subproblems, optimal substructure and overlap
- Deriving the recurrence is the crucial step
  ::
  @cheat

### DP recipe

- Define subproblem
- Write recurrence
- Fill table bottom-up
- Read answer from final cell
- Trace back for the actual choice

### vs other strategies

- Greedy: no look-back
- D&C: independent subproblems
- DP: overlapping, stored

### Matrix chain

- Cost of d×e × e×f: d·e·f
- m[i,j] = min left + right + p(i−1)p(k)p(j)
- Fill by chain length
- O(n³) time, O(n²) space

### 0/1 knapsack

- Skip: B[k−1,w]
- Take: B[k−1,w−wk] + bk
- Differs from above: taken
- O(nW)

### Coin change

- C[0] = 0
- C[p] = min 1 + C[p − di]

### Fibonacci

- Recursive: O(2ⁿ)
- Bottom-up: O(n)
  @mcq 6
  How do DP subproblems differ from divide-and-conquer subproblems?

* DP's overlap, while D&C's are independent

- DP's are always larger
- D&C's overlap, while DP's are independent
- There is no difference

> Slide 6's comparison.
> @mcq 17
> A is 2×3 and B is 3×4. Multiplying A·B costs:

- 24

* 9
* 12
* 6

> d × e × f = 2 × 3 × 4.
> @mcq 25
> The matrix chain DP runs in:

- O(n³) time and O(n²) space

* O(n²) time and O(n) space
* O(2ⁿ) time and O(n²) space
* O(n log n) time and O(n) space

> Slide 28 states this.
> @mcq 47
> The 0/1 knapsack DP runs in:

- O(nW)

* O(n²)
* O(2ⁿ)
* O(W²)

> n rows, W + 1 columns.
> @mcq 44
> In B[k,w] when item k fits, the value is:

- max(B[k−1,w], B[k−1,w−wk] + bk)

* B[k−1,w] + bk
* max(B[k,w−1], bk)
* B[k−1,w−wk]

> The maximum of skipping and taking.
> @mcq 72
> Comparing B[i,k] with B[i−1,k], a different value means:

- Item i was taken

* Item i was skipped
* The table has an error
* The capacity is exceeded

> Slides 69 to 73 use this to recover the items.
> @mcq 8
> The plain recursive Fibonacci runs in:

- O(2ⁿ)

* O(n)
* O(log n)
* O(n²)

> It recomputes overlapping subproblems.
> @mcq 39
> Which is NOT one of the three DP ingredients on slide 39?

- Random pivot selection

* Simple subproblems
* Subproblem optimality
* Subproblem overlap

> Random pivots belong to quick sort.
> @mcq 79
> With coins {1, 2, 3}, the minimum number of coins to make 5 is:

- 2

* 3
* 5
* 1

> 2 + 3.
> @mcq 34
> In matrix chain, s[i,j] stores:

- The best split point k

* The minimum cost
* The matrix dimensions
* The chain length

> It's used to reconstruct the parenthesization.
> @mcq 40
> What makes it the "0/1" knapsack?

- Each item is taken whole or not at all

* Weights are either 0 or 1
* The bag holds 0 or 1 items
* Benefits are binary

> xᵢ is 0 or 1.
> @mcq 3
> The word "programming" in dynamic programming means:

- Planning

* Writing code
* Recursion
* Compiling

> It refers to filling in a table, per slide 3.
> @short 44
> Write the recurrence for 0/1 knapsack and explain each case.
> ~ skip, take, weight, max, B
> If item k's weight exceeds w, it can't fit: B[k,w] = B[k−1,w]. Otherwise take the better of skipping it, B[k−1,w], or taking it, B[k−1,w−wk] + bk.
> @short 23
> Explain the meaning of each term in the matrix chain recurrence.
> ~ left, right, multiply, split, minimum
> For every split point k, the cost is the cost of the left chain m[i,k], plus the right chain m[k+1,j], plus multiplying the two results, p(i−1)·p(k)·p(j). The minimum over all k is the answer.
> @short 81
> What two properties must a problem have for DP to apply? Explain them.
> ~ optimal substructure, overlapping, subproblems, table
> Optimal substructure: the optimal solution contains optimal solutions to smaller instances. Overlapping subproblems: the same subproblems recur, so storing their solutions avoids recomputation.

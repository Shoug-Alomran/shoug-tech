@head Lecture 5.1
@title Greedy Algorithms
@sources lecture-5-1-greedy-algorithms
@count 24
@tldr A greedy algorithm always takes whatever looks best right now and never reconsiders, which is fast and sometimes perfect, but is sometimes badly wrong.
@why Greedy is simple to describe and tricky to trust. The exam will often give you a problem and ask you to run a greedy method, and then ask whether its answer is optimal. So you need the algorithm and a counterexample ready.
@connect Dijkstra's algorithm and the minimum spanning tree algorithms in the next two lectures are both greedy. Dynamic programming is what you turn to when greedy fails.
@goals

- State the three properties each greedy choice must have
- Solve the fractional knapsack problem
- Give a case where greedy fails
- Schedule jobs with deadlines to maximize profit
  @vocab
  Optimization problem | One where you want the best solution, and not just any solution.
  Objective function | The score you want to maximize or minimize.
  Feasible | Meets the problem's constraints.
  Local optimum | Best option among the current choices.
  Global optimum | Best option overall.
  @map
  2-6 | What greedy is, general form | MEMORIZE | Feasible, locally optimal, irrevocable
  7-11 | Counting money and when it fails | WRITE | The krons example
  12-15 | Fractional knapsack | WRITE | Work the example
  16-20 | Scheduling and travelling salesman | SKIM | Greedy is fast, not always best
  22-24 | Scheduling with deadlines | WRITE | Trace the algorithm

## How a greedy algorithm thinks | Slides 2-9 | must

In an optimization problem you want the _best_ solution. A greedy algorithm works in phases, and at each one you **take the best you can get right now, without regard for future consequences**, hoping that a series of local best choices adds up to a global best.

::code text
Greedy(a, n):
solution = EMPTY
for i = 1 to n:
x = Select(a)
if Feasible(solution, x):
solution = Union(solution, x)
return solution
::

Each choice must be:

| Property            | Meaning                                      |
| ------------------- | -------------------------------------------- |
| **Feasible**        | Satisfies the problem's constraints          |
| **Locally optimal** | Best among all feasible choices at this step |
| **Irrevocable**     | Once made, it can't be changed               |

::mnemonic FLIP is forbidden
You can't **flip** your decision: **F**easible, **L**ocally optimal, **I**rrevocable. The P reminds you it's a one-Pass process, with no going back.
::

It works best on problems with the **greedy-choice property**: a globally optimal solution can always be reached by a series of local improvements.

::analogy Hiking toward a summit in fog
Always stepping uphill gets you to a top quickly. On a single mountain that's the highest point. In a mountain range, you might finish on a small hill and never find out.
::
::key

- Greedy takes the best option now, ignoring the future
- Each choice is feasible, locally optimal and irrevocable
- It works best on problems with the greedy-choice property
- It can be fast but doesn't always give the optimum
  ::

## Making change: when greedy wins and loses | Slides 7-11 | must

**Greedy rule:** always use the largest coin that doesn't overshoot.

For $6.39 in US money: $5, $1, 25¢, 10¢, then four 1¢ coins. For US money, this always gives the fewest coins.

::example The krons (slide 8)
Coins of 1, 7 and 10 krons. Make 15.

**Greedy:** 10, then 1 + 1 + 1 + 1 + 1. That's **6 coins**.

**Best:** 7 + 7 + 1. That's **3 coins**.

Grabbing the 10 first locked it out of the better answer.
::
::example Another failure (slide 11)
Coins of 30¢, 20¢, 5¢ and 1¢. Make 40¢.

**Greedy:** 30 + 5 + 5 = 3 coins. **Best:** 20 + 20 = 2 coins.
::
::trap "Greedy works for coins" isn't a general truth
It depends on the coin set. For an exam question, one counterexample like the ones above is enough to prove that greedy is not optimal for that set.
::
::key

- Change-making rule: take the largest coin that fits
- Works for US money, but not for every coin system
- Krons 1, 7, 10 making 15: greedy uses 6 coins, best uses 3
  ::

## Fractional knapsack | Slides 12-15 | must

You have items with a benefit and a weight, and a bag that holds weight W. **You may take fractions of an item.** Greedy _does_ give the best answer here.

**Greedy rule:** sort by value = benefit ÷ weight, and take the highest value first.

::example Slide 14: capacity 10 ml

| Item | Weight | Benefit | Value ($/ml) |
| ---- | ------ | ------- | ------------ |
| 1    | 4 ml   | $12     | 3            |
| 2    | 8 ml   | $32     | 4            |
| 3    | 2 ml   | $40     | 20           |
| 4    | 6 ml   | $30     | 5            |
| 5    | 1 ml   | $50     | 50           |

Take in order of value:

- **All 1 ml of item 5** → $50, 9 ml left
- **All 2 ml of item 3** → $40, 7 ml left
- **All 6 ml of item 4** → $30, 1 ml left
- **1 ml of item 2** → $4, full

**Total: $124**.
::

**Run time: O(n log n)**, because of the sort.

**Why it's optimal:** suppose a better solution used less of a high-value item and more of a lower-value one. Swapping a little of the low-value item for the high-value one would improve it, which is a contradiction.

::trap Fractional is greedy, 0/1 is not
When you must take **all or none** of an item, the greedy rule can fail. That version, 0/1 knapsack, needs dynamic programming (Lecture 6).
::
::key

- Fractional knapsack allows partial items
- Greedy by benefit-to-weight ratio is optimal
- Time is O(n log n) due to sorting
- The 0/1 version needs dynamic programming
  ::

## Scheduling: fast, but not always the best | Slides 16-20 | know

Nine jobs (3, 5, 6, 10, 11, 14, 15, 18, 20 minutes) on three processors.

| Strategy           | Completion time |
| ------------------ | --------------- |
| Longest job first  | 35 min          |
| Shortest job first | 40 min          |
| Best possible      | **34 min**      |

The total work is 102, and 102 / 3 = 34, so no schedule can beat 34. That's why it's "clearly optimal". Finding it requires trying assignments, which can take exponential time.

**Travelling salesman:** always going to the nearest unvisited city produces a tour, but not the shortest. Slide 20: greedy's route costs 16 and the true shortest costs 14.

::key

- Longest-first gave 35 minutes, shortest-first 40, the optimum 34
- Nearest-neighbour doesn't solve the travelling salesman problem optimally
- Greedy trades optimality for speed on many hard problems
  ::

## Scheduling with deadlines | Slides 22-24 | must

Each job takes one time unit and pays a profit only if finished by its deadline.

::steps The greedy method
Sort jobs by profit, highest first.
For each job, add it if a feasible schedule exists with it. Otherwise reject it.
Keep the accepted jobs in order of deadline.
::
::example Slide 24

| Job      | 1   | 2   | 3   | 4   | 5   | 6   | 7   |
| -------- | --- | --- | --- | --- | --- | --- | --- |
| Deadline | 3   | 1   | 1   | 3   | 1   | 3   | 2   |
| Profit   | 40  | 35  | 30  | 25  | 20  | 15  | 10  |

- S = {} then add job 1: **[1]** is feasible.
- Add 2: **[2, 1]** (job 2 must be first).
- Try 3: deadline 1 but job 2 already holds that slot. **Rejected.**
- Add 4: **[2, 1, 4]** fits, finishing at time 3.
- Jobs 5, 6 and 7: no slot left. **Rejected.**

Profit: 35 + 40 + 25 = **100**.
::
::tip Feasible sequence or feasible set
A **sequence** is feasible if every job starts by its deadline: [4, 1] may work while [1, 4] doesn't. A **set** is feasible if at least one feasible sequence exists.
::
::key

- Sort by profit, descending
- Add a job only if a feasible schedule still exists
- Keep the schedule ordered by deadline
- On the slide's example the best set is jobs 1, 2 and 4, with profit 100
  ::
  @cheat

### Greedy choice

- Feasible
- Locally optimal
- Irrevocable

### Optimal by greedy

- Fractional knapsack
- Change with US coins
- Dijkstra (non-negative edges)
- Kruskal and Prim
- Huffman codes

### Greedy is an approximation

- Travelling salesman
- 0/1 knapsack
- Coin sets like 1, 7, 10

### Fractional knapsack

- Value = benefit ÷ weight
- Take highest value first
- Partial item at the end
- O(n log n)

### Deadline scheduling

- Sort profits descending
- Add if still feasible
- Keep in deadline order
  @mcq 9
  Which set of properties must each greedy choice have?

* Feasible, locally optimal, irrevocable

- Feasible, globally optimal, revocable
- Recursive, overlapping, optimal
- Random, feasible, reversible

> Slide 9 lists these three properties.
> @mcq 8
> With coins 1, 7, 10, what does greedy use to make 15?

- 6 coins

* 3 coins
* 2 coins
* 5 coins

> 10 + five 1s. The optimum 7 + 7 + 1 uses 3.
> @mcq 15
> The greedy rule for fractional knapsack takes items by:

- Highest benefit-to-weight ratio

* Highest benefit
* Lowest weight
* Original order

> That ratio is the item's value per unit of weight.
> @mcq 14
> For slide 14's items and capacity 10 ml, the maximum benefit is:

- $124

* $122
* $132
* $102

> 50 + 40 + 30 + 4 = 124.
> @mcq 15
> Fractional knapsack by greedy takes:

- O(n log n)

* O(n²)
* O(2ⁿ)
* O(nW)

> The sort dominates the running time.
> @mcq 12
> Which problem can greedy solve optimally?

- Fractional knapsack

* 0/1 knapsack
* Travelling salesman
* General coin change

> Partial items make the ratio rule optimal. The other three can fail.
> @mcq 24
> Deadline scheduling first sorts jobs by:

- Profit, in non-increasing order

* Deadline, in increasing order
* Job number
* Profit, in increasing order

> High-profit jobs are considered first.
> @mcq 19
> Nine jobs total 102 minutes on 3 processors. The lowest possible completion time is:

- 34 minutes

* 35 minutes
* 40 minutes
* 102 minutes

> 102 / 3 = 34, and the slide's best schedule reaches it.
> @mcq 3
> A greedy algorithm at each step:

- Takes the best option available now

* Tries every possible option
* Solves all overlapping subproblems
* Backtracks when a choice is bad

> It ignores the future. Backtracking is a different strategy.
> @mcq 20
> The nearest-neighbour rule for travelling salesman:

- Produces a tour that may not be shortest

* Always finds the shortest tour
* Requires dynamic programming
* Fails to produce any tour

> On slide 20 it costs 16, while the best tour costs 14.
> @short 8
> Give a counterexample showing that greedy change-making isn't always optimal.
> ~ coins, greedy, optimal, fewer, example
> With coins 1, 7 and 10 making 15, greedy takes 10 and five 1s, which is 6 coins. The optimal solution 7 + 7 + 1 uses only 3 coins.
> @short 15
> Explain why the greedy strategy is optimal for fractional knapsack.
> ~ ratio, swap, higher, better, contradiction
> If a better solution used less of a high-ratio item and more of a lower-ratio item, swapping some of the lower-ratio item for the higher-ratio one would increase the benefit, which contradicts it being optimal.
> @short 24
> Schedule jobs with deadlines 2, 1, 2 and profits 50, 40, 30 to maximize profit.
> ~ sort, profit, feasible, jobs, 90
> Sorted by profit: job 1 (50), job 2 (40), job 3 (30). Accept 1. Accept 2 as sequence [2, 1]. Job 3 has no free slot within its deadline. Total profit is 90.

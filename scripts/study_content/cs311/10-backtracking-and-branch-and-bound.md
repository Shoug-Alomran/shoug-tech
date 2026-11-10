@head Lecture 7
@title Backtracking and Branch and Bound
@sources backtracking-and-branch-and-bound, backtracking-and-branch-and-bound-second-copy
@count 43
@tldr Explore a tree of choices and cut off whole branches as soon as you can prove they're useless: backtracking cuts branches that break the rules, and branch and bound cuts those that can't beat your best answer.
@why Some problems have no known fast algorithm. These two methods are how you solve them in practice. You'll be asked to draw a state-space tree for four queens or graph colouring, and to compute a bound in branch and bound.
@connect Backtracking is a depth-first search (Topic 7) over a tree of decisions. The last lecture explains why these problems seem to resist a polynomial solution.
@goals
- Describe the state-space tree and pruning
- Solve four queens with backtracking
- Run graph colouring with backtracking
- Compute a lower bound for the travelling salesman
- Compare backtracking and branch and bound
@vocab
State-space tree | A tree whose nodes are partial solutions.
Promising | Could still lead to a solution.
Pruning | Refusing to explore below a node.
Bounding function | An estimate of the best value reachable from a node.
Feasible | Meets the constraints.
@map
2-10 | Backtracking idea | MEMORIZE | State space, promising, pruning
11-15 | n-queens | WRITE | Draw the 4-queens tree
16-28 | Graph colouring | WRITE | Follow the code
29-35 | Limits and knapsack | SKIM | Worst case stays exponential
36-38 | Branch and bound idea | MEMORIZE | Bound vs best so far
39-43 | Travelling salesman | WRITE | Compute a lower bound

## Backtracking: try, check, undo | Slides 2-10 | must
**Backtracking** is a methodical way of trying sequences of decisions until one works. Each decision leads to new choices, and if a path fails you step back and try another.

::code text
Explore(node N):
    if N is a goal: return success
    if N is a dead end: return failure
    for each child C of N:
        if Explore(C) is successful: return success
    return failure
::

It's depth-first search over a **state-space tree**: the root is the initial state and each node records the choices so far.

- **Promising node:** might still lead to a solution, so keep going.
- **Non-promising node:** can't lead to a solution, so **prune** it and go back to the parent.

::analogy Walking a maze with chalk
At each junction, pick a corridor. At a dead end, go back to the last junction and try a different one. Chalk marks make sure that you never re-explore a corridor.
::
::mnemonic Choose, Check, Change back
**Choose** an option. **Check** whether it can still work, and recurse. **Change back** if it fails, so the state is clean for the next option.
::
::trap Pruning isn't a guarantee of speed
The worst case is still exponential. Slide 29 says the success of backtracking varies by problem and instance. Pruning simply avoids much of the tree in practice.
::
::key
- Backtracking is depth-first search of a state-space tree
- Non-promising nodes are pruned
- On failure it backs up to the parent and tries the next option
- The worst case remains exponential
::

## Four queens | Slides 11-15 | must
Place 4 queens on a 4 × 4 board so that none attack each other. Each queen gets its own row, so choose a column for each row.

::steps Finding the first solution
Row 1: try column 1. Row 2: columns 1 and 2 are attacked, so try column 3.
Row 3: every column is attacked. **Dead end.** Back up.
Row 2: try column 4. Row 3: try column 2.
Row 4: every column is attacked. **Dead end.** Back up, and every option for Row 2 with Q1 in column 1 fails.
Row 1: move to column 2. Row 2: column 4. Row 3: column 1. Row 4: column 3. **Success: [2, 4, 1, 3]**.
::
::example The solutions
Written as the column for each row: **[2, 4, 1, 3]** and its mirror image **[3, 1, 4, 2]**. Slide 15 suggests using that symmetry to find the second solution.

| | C1 | C2 | C3 | C4 |
|---|---|---|---|---|
| **R1** | | Q | | |
| **R2** | | | | Q |
| **R3** | Q | | | |
| **R4** | | | Q | |
::
::check Why does putting each queen in a different row shrink the search?
Without this rule, there would be 16 choose 4 = 1,820 placements. With one queen per row, there are only 4⁴ = 256 possibilities before any pruning.
::
::key
- Place one queen per row and choose a column
- A position is promising if no earlier queen attacks it
- The 4-queens solutions are [2,4,1,3] and [3,1,4,2]
::

## Graph colouring | Slides 16-28 | must
Colour the vertices with at most m colours so that no neighbours match. Regions of a map become nodes and borders become edges. The **Four Colour Theorem** says that any map on a plane needs at most four.

::code cpp
graphColour(k):
    for c = 1 to m:
        if isSafe(k, c):        // no neighbour already has colour c
            x[k] = c
            if k + 1 < n: graphColour(k + 1)
            else: print x
::
::example Slide 19: m = 3, edges 0–1, 0–3, 1–2, 1–3, 2–3
Node 0: red. Node 1 is adjacent to 0, so: green. Node 2 is adjacent to 1 only (of those coloured): red works. Node 3 is adjacent to 0, 1 and 2 (red, green, red): blue.

Result: **{red, green, red, blue}**.
::

Without pruning, there are **mⁿ** possible colourings of n nodes, which is why the problem is expensive.

::tip Backtracking versus greedy on knapsack (slide 30)
A 50 lb knapsack with items of 40, 32, 22, 22, 15 and 5 lb. Greedy takes 40 then 5, reaching 45 lb. Exhaustive search finds 22 + 22 + 5 = **49 lb**.
::
::key
- Adjacent vertices must have different colours
- isSafe checks the neighbours' colours
- Unpruned search covers m to the n colourings
- Backtracking can beat greedy on knapsack-type problems
::

## Branch and bound | Slides 36-43 | must
Branch and bound uses the same state-space tree, with two differences. It's for **optimization** problems, and it isn't limited to depth-first order.

**At each node, compute a bound on the best value that can be reached below that node.** Compare the bound with the best complete solution so far.

| Bound vs best so far | Decision |
|---|---|
| Bound is **better** | Promising: expand |
| Bound is **no better** | Non-promising: prune |

| | Backtracking | Branch and bound |
|---|---|---|
| Problem type | Mostly non-optimization | **Optimization only** |
| Traversal | **Depth-first** | Any, such as best-first |
| Prunes when | Constraints are broken | Bound can't beat the best so far |

::analogy Shopping for the cheapest flight
You've already found a ticket for 900. A route's first leg alone costs 1,000. There's no point looking at the rest of that route, since it can't possibly beat 900.
::

### Lower bound for travelling salesman
A tour enters and leaves every vertex once. So each vertex must use two edges, and we can bound the tour by the two cheapest edges at each vertex.

::formula Bound on slide 41
lb = ⌈ (sum over vertices of the two cheapest incident edges) / 2 ⌉
::
::example Slide 42's graph (a to e)
Edge costs: a–b 3, a–c 1, a–d 5, a–e 8, b–c 6, b–d 7, b–e 9, c–d 4, c–e 2, d–e 3.

| Vertex | Two cheapest edges | Sum |
|---|---|---|
| a | 1, 3 | 4 |
| b | 3, 6 | 9 |
| c | 1, 2 | 3 |
| d | 3, 4 | 7 |
| e | 2, 3 | 5 |

Total = 28. lb = 28 / 2 = **14**, which is the root value on the slide. Any tour must cost at least 14. The best tour found, **a, b, d, e, c, a**, costs 3 + 7 + 3 + 2 + 1 = **16**.
::
::trap The direction of the comparison
For **minimization**, a node is pruned when its **lower bound ≥ best so far**. For maximization, it's when its upper bound ≤ best so far.
::
::key
- Branch and bound is used only for optimization problems
- It computes a bound at each node and compares it to the best so far
- It may traverse the tree in any order
- TSP lower bound: half the sum of each vertex's two cheapest edges
- Prune when the bound can't beat the current best
::
@cheat
### Backtracking
- DFS of state-space tree
- Promising: continue
- Non-promising: prune
- Back up and try next option
### 4 queens
- One queen per row
- Solutions: [2,4,1,3], [3,1,4,2]
### Graph colouring
- Adjacent nodes differ
- isSafe checks neighbours
- mⁿ without pruning
- Any planar map needs at most 4
### Branch and bound
- Optimization only
- Any traversal order
- Prune when bound no better than best
### TSP lower bound
- Sum two cheapest edges per vertex
- Divide by 2, round up
@mcq 10
Backtracking explores the state-space tree using:
+ Depth-first search
- Breadth-first search only
- Best-first search only
- Random order
> Slide 10.
@mcq 10
What happens at a non-promising node?
+ The subtree below it is pruned
- It is expanded first
- The search restarts
- It is marked as a solution
> Search backs up to the parent.
@mcq 15
Which is a solution to 4 queens, written as the column per row?
+ [2, 4, 1, 3]
- [1, 3, 2, 4]
- [1, 2, 3, 4]
- [4, 3, 2, 1]
> Others share a column, or a diagonal.
@mcq 18
Graph colouring on n nodes with m colours has how many unpruned possibilities?
+ mⁿ
- nᵐ
- m × n
- 2ᵐ
> Each of n nodes can take any of m colours.
@mcq 37
Branch and bound is used for:
+ Optimization problems only
- Non-optimization problems only
- Sorting problems
- Only depth-first traversal
> Slide 37.
@mcq 38
In a minimization problem, a node is pruned when:
+ Its lower bound is no better than the best so far
- Its lower bound is the smallest so far
- It has no parent
- It is the root
> It can't improve on what you already have.
@mcq 41
The TSP lower bound uses, for each vertex:
+ The two cheapest incident edges
- All incident edges
- The single most expensive edge
- The degree of the vertex
> A tour enters and leaves every vertex.
@mcq 42
Sum of the two cheapest edges per vertex is 28. The lower bound is:
+ 14
- 28
- 7
- 56
> Half the sum, since each edge is counted from both ends.
@mcq 30
On the 50 lb knapsack from slide 30, the best load found by exhaustive search is:
+ 49 lb
- 45 lb
- 50 lb
- 47 lb
> 22 + 22 + 5.
@mcq 37
A key difference between branch and bound and backtracking is:
+ Branch and bound isn't restricted to DFS
- Branch and bound doesn't use a tree
- Backtracking is only for optimization
- Backtracking uses bounds
> Slide 37.
@short 38
Explain how branch and bound decides whether to expand a node.
~ bound, best so far, promising, prune, compare
> It computes a bound on the best value reachable from the node. If the bound is better than the best solution so far, the node is promising and expanded; otherwise it is pruned.
@short 10
Describe the state-space tree used in backtracking.
~ root, node, choice, promising, prune
> The root is the initial state, and each node represents a partial solution built from choices so far. Promising nodes are explored further, and non-promising ones are pruned.
@short 19
Run backtracking to 3-colour a triangle with vertices 0, 1, 2. Give the colouring.
~ adjacent, different, red, green, blue
> Vertex 0 takes red. Vertex 1 is adjacent to 0, so green. Vertex 2 is adjacent to both, so it takes blue. All three colours are needed.

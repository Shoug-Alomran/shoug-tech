@head Lecture 9
@title Complexity Classes: P, NP, NP-Complete and NP-Hard
@sources complexity-classes-p-np-np-complete-and-np-hard
@count 41
@tldr P problems can be solved quickly, NP problems can be checked quickly, and NP-complete problems are the hardest of the checkable ones: solve one fast and you've solved them all.
@why This is the most abstract lecture, and exams mainly test definitions and the direction of a reduction. The whole topic rests on a few short sentences. Once you have them, most questions are easy.
@connect Backtracking and branch and bound were your practical tools for hard problems. This lecture explains why so many problems seem to need them.
@goals
- Define P, NP, NP-hard and NP-complete
- Explain what a reduction is and which direction it goes in
- State the steps to prove a problem NP-complete
- Explain the reductions to Vertex Cover and Clique
- Say what to do when a problem is NP-complete
@vocab
Decision problem | One whose answer is yes or no.
Polynomial time | Running in O(nᵏ) for some constant k.
Certificate | A proposed answer that can be checked.
Reduction | Turning any instance of one problem into an instance of another.
SAT | Whether a Boolean formula can be made true.
@map
2-7 | Decision problems and class P | MEMORIZE | Polynomial-time cut-off
8-11 | Class NP | MEMORIZE | NP doesn't mean non-polynomial
12-15 | NP-hard and NP-complete | MEMORIZE | The definitions
16-24 | Circuit-SAT and reductions | MEMORIZE | Cook-Levin, transitivity
25-30 | SAT and 3SAT | MEMORIZE | CNF
31-37 | Vertex Cover and Clique | WRITE | The constructions
38-40 | Other NPC problems and proof steps | MEMORIZE | The four-step proof

## The classes | Slides 2-15 | must
The theory focuses on **decision problems**, those with a yes or no answer, and treats **polynomial time** as the cut-off for "efficient". An optimization question can usually be recast: not "what's the shortest tour?" but "is there a tour no longer than d?"

| Class | Plain meaning | Example |
|---|---|---|
| **P** | **Solved** in polynomial time | Sorting, shortest path |
| **NP** | A proposed solution can be **verified** in polynomial time | Does this graph have a Hamiltonian cycle? |
| **NP-hard** | At least as hard as everything in NP | Halting problem, TSP optimization |
| **NP-complete** | In NP **and** NP-hard | SAT, 3SAT, Clique, Vertex Cover |

::analogy A jigsaw puzzle
**Solving** a 10,000-piece puzzle is hard. **Checking** whether a finished one is correct takes a quick glance. NP problems are the ones that are easy to check, however hard they may be to solve.
::

::graph If P ≠ NP, the classes look like this | directed
n h 200 0 NP-hard
n c 200 90 NP-complete\nboth NP and NP-hard *
n n 200 190 NP\nquickly verifiable
n p 200 280 P\nquickly solvable
e p n contained in
e c n is in
e c h is in
::

::trap "NP" means Non-deterministic Polynomial
It does **not** mean "non-polynomial". This is slide 11's first question. And **P ⊆ NP**: anything you can solve quickly, you can check quickly.
::
::mnemonic Solve vs See
**P** you can **solve**. **NP** you can only **see** is right once someone hands it to you.
::
::key
- P: solvable in polynomial time
- NP: verifiable in polynomial time; stands for non-deterministic polynomial
- P is a subset of NP
- NP-hard: every NP problem reduces to it, and it needn't be in NP
- NP-complete: in NP and NP-hard
::

## Reductions | Slides 20-24 | must
A **reduction** M → L converts any instance x of problem M into an instance x′ of L, in polynomial time, such that x is a yes **if and only if** x′ is a yes.

So if you could solve L fast, you could solve M fast. **L is at least as hard as M.**

::analogy Translating into a language you speak
You can't read Spanish but have an excellent translator into English. "If I can solve English questions, I can solve Spanish ones." The translator is the reduction.
::
::trap The direction catches everyone
To prove your new problem S is NP-hard, reduce a **known NP-hard problem → S**. Going the other way (S → known) proves nothing about S's hardness.
::
::mnemonic Known goes INto New
Reductions flow from **K**nown to **N**ew: known problem → your problem.
::

**Reductions are transitive:** if A → B and B → C, then A → C. So one starting NP-hard problem is enough, and all others are chained from it.

**Cook-Levin (1971):** CIRCUIT-SAT is NP-complete. That first proof showed every NP problem reduces to it, using properties common to all NP problems.

If any NP-complete problem had a polynomial solution, then **P = NP**. Almost everyone believes P is a proper subset of NP, but nobody has proved it.

::key
- A reduction transforms instances in polynomial time and preserves the answer
- Reduce a known NP-hard problem to your problem, never the reverse
- Reductions are transitive
- Cook-Levin: CIRCUIT-SAT is NP-complete
- If any NP-complete problem is in P, then P = NP
::

## The chain of NP-complete problems | Slides 25-39 | must
::graph How the proofs chain together | directed
n a 180 0 CIRCUIT-SAT
n b 180 75 SAT
n c 180 150 3SAT
n d 60 225 Vertex Cover
n e 300 225 Clique
n f 0 310 Set Cover
n g 120 310 Subset Sum
n h 240 310 Hamiltonian Cycle
e a b
e b c
e c d
e c e
e d f
e d g
e d h
::

**SAT:** can a Boolean formula be made true? **CNF** means an AND of ORs. **3SAT** restricts each clause to three literals and is still NP-complete.

### Vertex Cover (slides 31-35)
A set of vertices that touches every edge. Question: is there one of size at most K?

::steps Reducing 3SAT to Vertex Cover
For each variable x, make a pair of nodes x and ¬x, joined by an edge.
For each clause, make a triangle with one node per literal.
Connect each triangle node to its matching literal's node.
Set **K = n + 2m**, with n variables and m clauses.
The graph has a vertex cover of size K exactly when the formula is satisfiable.
::
::example Slide 35
(a + b + c)(¬a + b + ¬c)(¬b + ¬c + ¬d) has n = 4 variables and m = 3 clauses, so K = 4 + 2(3) = **10**.
::

### Clique (slides 36-37)
A subset of vertices in which every pair is connected. Reduction from CNF-SAT: make a vertex for each literal in each clause, and join two vertices when they're in **different clauses** and **aren't negations of each other**. A clique of size k (the number of clauses) exists exactly when the formula is satisfiable.

Others on the slides: **Set Cover, Subset Sum, 0/1 Knapsack, Hamiltonian Cycle, Travelling Salesperson**.

::says Slide 39 | 0/1 Knapsack is NP-complete, yet Lecture 6 solved it in O(nW)
Both are true. O(nW) depends on the *value* of W, and input size counts the *bits* needed to write W. So O(nW) isn't polynomial in the size of the input. It's called **pseudo-polynomial**.
::
::key
- SAT asks if a Boolean formula can be satisfied
- 3SAT limits each clause to three literals and remains NP-complete
- Vertex Cover reduction: K = n + 2m
- Clique reduction joins compatible literals in different clauses
- Knapsack's O(nW) is pseudo-polynomial
::

## Proving a problem is NP-complete | Slides 14-15, 40 | must
::steps The four-step recipe (slide 40)
Show that S is in NP: give a polynomial-time verifier.
Pick a known NP-complete problem R.
Give a polynomial-time reduction from R to S.
Conclude: every NP problem reduces to R and R reduces to S, so S is NP-complete.
::

And when you must actually solve an NP-complete problem (slide 15): don't look for a fast exact algorithm. Use **approximation algorithms** for near-optimal answers, or backtracking and branch and bound.

::check Is "Is this given list sorted?" in P, NP, or both?
Both. It can be solved in O(n), so it's in P, and every problem in P is also in NP.
::
::key
- Show S is in NP, then reduce a known NP-complete problem to S
- Transitivity gives the conclusion that S is NP-hard
- For NP-complete problems in practice, use approximation algorithms
::
@cheat
### Classes
- P: solvable in poly time
- NP: verifiable in poly time
- NP-hard: every NP problem reduces to it
- NP-complete: NP and NP-hard
- P ⊆ NP
### Reductions
- Known → your problem
- Polynomial time
- Yes iff yes
- Transitive
### Proof recipe
- Show S in NP
- Choose known NPC problem R
- Reduce R to S
- Conclude S is NPC
### Famous NPC
- CIRCUIT-SAT, SAT, 3SAT
- Vertex Cover, Clique
- Set Cover, Subset Sum
- 0/1 Knapsack, Hamiltonian, TSP
### Constructions
- Vertex Cover: K = n + 2m
- Clique: literals in different clauses, not negations
@mcq 11
NP stands for:
+ Non-deterministic polynomial time
- Non-polynomial time
- No polynomial solution
- Negative polynomial
> Slide 11 warns against reading it as non-polynomial.
@mcq 11
Which statement is correct?
+ Every P problem is also in NP
- P and NP have no problems in common
- NP problems can never be solved
- P contains every NP problem, proven
> P ⊆ NP. Whether P = NP is open.
@mcq 14
An NP-complete problem is:
+ In NP and NP-hard
- Not in NP
- Always in P
- Only an optimization problem
> Slide 14.
@mcq 12
A problem L is NP-hard if:
+ Every NP problem reduces to it in polynomial time
- It reduces to every NP problem
- It is in P
- It can be verified quickly
> Slide 12. It needn't be in NP at all.
@mcq 40
To show S is NP-hard, you reduce:
+ A known NP-complete problem to S
- S to a known NP-complete problem
- S to a problem in P
- S to itself
> The direction is known → new.
@mcq 21
Which problem was the first shown to be NP-complete by Cook-Levin?
+ CIRCUIT-SAT
- Clique
- Vertex Cover
- Sorting
> Slides 20 and 21.
@mcq 35
For 3SAT with 4 variables and 3 clauses, the vertex cover size K is:
+ 10
- 7
- 12
- 4
> K = n + 2m = 4 + 6.
@mcq 22
If one NP-complete problem had a polynomial algorithm:
+ P would equal NP
- NP would be empty
- P would be empty
- Nothing else would change
> Every NP problem reduces to it.
@mcq 36
A clique is a subset of vertices where:
+ Every pair is connected
- No two vertices are connected
- Every edge is touched
- The vertices form a path
> Slide 36. Touching every edge is a vertex cover.
@mcq 15
Facing an NP-complete problem in practice, the slides suggest:
+ Approximation algorithms
- Giving up completely
- Always using greedy for exact answers
- Expecting a polynomial exact algorithm
> Slide 15.
@mcq 28
3SAT requires each clause to have:
+ 3 literals
- 3 variables in the formula overall
- 3 clauses in total
- 3 AND operators
> Each clause has exactly three literals.
@short 40
State the steps to prove that a problem is NP-complete.
~ NP, verifier, known, reduce, polynomial
> Show the problem is in NP with a polynomial-time verifier. Pick a known NP-complete problem. Reduce it to the new problem in polynomial time. By transitivity, every NP problem reduces to the new problem, so it is NP-complete.
@short 11
Explain the difference between P and NP.
~ solve, verify, polynomial, subset
> P contains problems that can be solved in polynomial time. NP contains problems whose proposed solutions can be verified in polynomial time. Every P problem is also in NP.
@short 39
Why doesn't the O(nW) knapsack algorithm contradict knapsack being NP-complete?
~ pseudo-polynomial, W, bits, input size
> O(nW) is pseudo-polynomial: it depends on the numeric value of W, whereas the input size counts the bits needed to write W. So it is not polynomial in the input size.

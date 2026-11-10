@head Lecture 5.2
@title Dijkstra's Algorithm
@sources lecture-5-2-dijkstras-algorithm
@count 20
@tldr Keep a best-known distance for every vertex, finalize the closest unfinished vertex, relax its neighbours, and repeat until they're all done.
@why GPS navigation and internet routing both use this idea. Tracing the table by hand is an almost guaranteed exam question, and you'll also be asked why the priority queue version is faster and what makes the algorithm fail.
@connect It is a greedy algorithm (Lecture 5.1). Prim's algorithm in the next lecture looks nearly identical, with a single important change.
@goals

- State what problem Dijkstra's algorithm solves
- Trace the algorithm's table by hand
- Reconstruct a shortest path
- State the running time of each implementation
- Explain why negative edges break it
  @vocab
  Weighted graph | A graph whose edges each carry a number.
  Source | The vertex you start from.
  Relaxation | Checking if going through a vertex offers a shorter route, and updating if so.
  Known vertex | One whose shortest distance is final.
  Priority queue | A structure that returns the smallest item quickly.
  @map
  2-3 | What it does, pseudocode | MEMORIZE | Non-negative weights
  6-14 | Worked example | WRITE | Reproduce the table
  15-16 | Time complexity | MEMORIZE | List vs priority queue
  17-20 | Exercise | WRITE | Practise on your own

## The idea | Slides 2-3 | must

Dijkstra's algorithm finds **shortest (minimum weight) paths from a source** in a weighted graph with **non-negative** edge weights. It keeps a table holding, for every vertex, the best-known distance and the previous vertex, and improves it until it's final.

::code text
Dijkstra(v1, v2):
for each vertex v:
v.distance = infinity; v.previous = none
v1.distance = 0
List = all vertices
while List is not empty:
v = remove vertex in List with minimum distance
mark v as known
for each unknown neighbour n of v:
dist = v.distance + weight(v, n)
if dist < n.distance:
n.distance = dist; n.previous = v
reconstruct the path from v2 back using previous pointers
::
::analogy Water spreading through pipes
Pour water in at the source. It reaches the nearest junction first. The moment it arrives, you know that was the fastest route, and nothing later can beat it. From there it spreads further.
::
::mnemonic Pick, Pin, Push
**Pick** the closest unknown vertex. **Pin** it as final. **Push** updates out to its neighbours. Repeat.
::
::key

- Finds shortest paths from one source
- Edge weights must be non-negative
- Stores a distance and a previous vertex for each vertex
- Greedy: always finalizes the closest unknown vertex
  ::

## Worked example | Slides 6-14 | must

The graph from the slides, starting at A:

::graph Slide 6's directed graph | directed
n A 80 0
n B 240 0
n C 0 110
n D 160 110
n E 320 110
n F 80 220
n G 240 220
e A B 2
e A D 1
e B D 3
e B E 10
e C A 4
e C F 5
e D C 2
e D E 2
e D F 8
e D G 4
e E G 6
e G F 1
::

| Step | Finalize | A     | B     | C     | D     | E     | F     | G     | What just happened                   |
| ---- | -------- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ------------------------------------ |
| 0    |          | **0** | ∞     | ∞     | ∞     | ∞     | ∞     | ∞     | Initialize                           |
| 1    | A        | **0** | 2     | ∞     | 1     | ∞     | ∞     | ∞     | Relax B and D                        |
| 2    | D        | 0     | 2     | 3     | **1** | 3     | 9     | 5     | D has C, E, F, G                     |
| 3    | B        | 0     | **2** | 3     | 1     | 3     | 9     | 5     | Via B: D known; E would be 12, so no |
| 4    | E        | 0     | 2     | 3     | 1     | **3** | 9     | 5     | Via E: G would be 9, so no           |
| 5    | C        | 0     | 2     | **3** | 1     | 3     | 8     | 5     | F improves: 3 + 5 = 8                |
| 6    | G        | 0     | 2     | 3     | 1     | 3     | 6     | **5** | F improves: 5 + 1 = 6                |
| 7    | F        | 0     | 2     | 3     | 1     | 3     | **6** | 5     | Done                                 |

(C and E are tied at 3, and either order is valid.)

::steps Rebuild the path to F using previous pointers
F's previous is G, since the last improvement came through G.
G's previous is D, since 1 + 4 = 5.
D's previous is A.
So the shortest path is **A → D → G → F**, with cost 1 + 4 + 1 = **6**.
::
::trap Update only if strictly better
On slide 10, distance(E) stays at 3 because going via B would give 12. And distance(D) isn't touched since D is already known.
::
::check What's the shortest path to E, and what's its cost?
A → D → E, cost 1 + 2 = **3**.
::
::key

- Always pick the unknown vertex with the smallest distance
- Update a neighbour only if the new distance is smaller
- Follow previous pointers backward to get the path
- Known vertices never change
  ::

## Running time and limits | Slides 15-16 | must

| Implementation     | Find min | Update   | Total          | Best for      |
| ------------------ | -------- | -------- | -------------- | ------------- |
| **Array or list**  | O(V)     | O(1)     | **O(V²)**      | Dense graphs  |
| **Priority queue** | O(log V) | O(log V) | **O(E log V)** | Sparse graphs |

::steps Why the list version is O(V²)
The while loop runs V times.
Each time, finding the minimum scans all vertices, costing V.
So far that's V².
There are at most E updates at O(1) each.
Total: O(V² + E) = **O(V²)**, as E is at most about V².
::
::why Why negative edges break it
Once a vertex is finalized, the algorithm trusts that no later route can be shorter. That's only true if edges can't decrease the total. A later negative edge could make an already "final" answer wrong.
::
::tip Which to choose
**Sparse** graph, with far fewer than V² edges: priority queue. **Dense** graph: the simple array, whose O(V²) beats E log V when E is close to V².
::
::key

- Using a list: O(V²), good for dense graphs
- Using a priority queue: O(E log V), good for sparse graphs
- Negative edge weights break Dijkstra's greedy guarantee
  ::
  @cheat

### Steps

- All distances ∞, source 0
- Pick smallest unknown vertex
- Mark it known
- Relax unknown neighbours
- Update only if smaller

### Complexity

- List: O(V²), dense graphs
- Priority queue: O(E log V), sparse graphs

### Facts

- Greedy algorithm
- Non-negative edges only
- Known vertices never change
- Path comes from previous pointers
  @mcq 2
  Dijkstra's algorithm requires edge weights that are:

* Non-negative

- All equal
- Integers only
- Strictly negative

> Slide 2 states the graph must have non-negative edge weights.
> @mcq 3
> At each step, Dijkstra's algorithm chooses:

- The unknown vertex with the smallest distance

* The vertex with the most edges
* A random unknown vertex
* The most recently updated vertex

> That greedy choice is what makes it work.
> @mcq 15
> Using a simple list, Dijkstra's running time is:

- O(V²)

* O(E log V)
* O(V log E)
* O(E²)

> Each of the V iterations scans V vertices for the minimum.
> @mcq 16
> Using a priority queue, the running time is:

- O(E log V)

* O(V²)
* O(V + E)
* O(E²)

> Deletions and updates cost O(log V), for up to V + E operations.
> @mcq 9
> In the example, after finalizing D with distance 1, an edge D to G of weight 4 gives G:

- Distance 5

* Distance 4
* Distance 1
* Distance 8

> 1 + 4 = 5.
> @mcq 13
> F currently has distance 8. G is finalized at 5 and has an edge to F of weight 1. F becomes:

- 6

* 8
* 1
* 9

> min(8, 5 + 1) = 6.
> @mcq 10
> Why is D not updated when B is processed?

- D is already known

* B has no edge to D
* Its weight is negative
* B was processed first

> Only unknown neighbours are relaxed.
> @mcq 15
> For a dense graph, which implementation is usually better?

- The simple array or list

* The priority queue
* Neither can run on dense graphs
* A binary search tree of edges

> With E near V², E log V exceeds V².
> @mcq 3
> The previous pointers are used to:

- Reconstruct the shortest path

* Detect cycles
* Choose the next vertex
* Store weights

> Follow them backward from the destination.
> @mcq 2
> Dijkstra's algorithm belongs to which design strategy?

- Greedy

* Divide and conquer
* Backtracking
* Randomized

> It makes one irrevocable local choice per step.
> @short 15
> Explain the time complexity of Dijkstra's algorithm using a list.
> ~ V, loop, minimum, E, V²
> The while loop runs V times and finding the minimum scans V vertices, giving V². There are up to E updates at O(1). So the total is O(V² + E), which is O(V²).
> @short 2
> Explain why Dijkstra's algorithm can't be trusted with negative edges.
> ~ final, known, negative, shorter, greedy
> A vertex is finalized on the assumption that no later route can be shorter. A negative edge could produce a shorter route after a vertex has been made final, so the greedy guarantee no longer holds.
> @short 3
> Describe how relaxation works when vertex v is finalized.
> ~ neighbour, distance, weight, smaller, update, previous
> For each unknown neighbour n, compute v's distance plus the edge weight. If it's smaller than n's distance, update n's distance and set n's previous vertex to v.

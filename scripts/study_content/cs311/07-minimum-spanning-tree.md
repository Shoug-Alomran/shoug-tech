@head Lecture 5.3
@title Minimum Spanning Tree
@sources lecture-5-3-minimum-spanning-tree
@count 43
@tldr A minimum spanning tree connects every vertex at the lowest total cost, and both Kruskal and Prim find one by repeatedly adding the cheapest edge that makes sense.
@why Whenever you need to connect everything as cheaply as possible, from network cables to roads, this is the tool. You'll be asked to run both algorithms on a graph and to compare them.
@connect Both algorithms are greedy (Lecture 5.1), and Prim closely resembles Dijkstra (Lecture 5.2).
@goals

- Define a spanning tree and minimum spanning tree
- Run Kruskal's algorithm and reject cycle-forming edges
- Run Prim's algorithm from a start vertex
- Compare both algorithms and their running times
  @vocab
  Tree | A connected graph with no cycles.
  Spanning tree | A subgraph that contains all vertices and is a tree.
  Cycle | A path that returns to where it started.
  Forest | A collection of separate trees.
  @map
  2-5 | Spanning trees | MEMORIZE | n vertices need n − 1 edges
  6-24 | Kruskal's algorithm | WRITE | Trace with cycle checks
  25 | Kruskal's running time | MEMORIZE | O(m log n)
  26-40 | Prim's algorithm | WRITE | Grow one tree
  41-43 | Comparison | MEMORIZE | Depends on the graph

## What a spanning tree is | Slides 2-5 | must

A **spanning tree** of a graph is a subgraph that **contains all the vertices and is a tree**. A graph can have many. The **minimum spanning tree (MST)** is the one with the smallest total edge weight.

Two facts that the slides stress:

- A spanning tree on n vertices always has **n − 1 edges**.
- **Adding any one more edge creates a cycle.**

Slide 3 shows that a complete graph with 4 vertices has **16** spanning trees.

::analogy Connecting villages with fibre
You want every village reachable, at the lowest cost, and a loop would be wasted cable. That's a minimum spanning tree.
::
::trap MST doesn't give shortest paths
An MST minimizes the **total** cable. The route between two particular vertices through the tree could be longer than their direct shortest path. Dijkstra and MST solve different problems.
::
::key

- A spanning tree contains all vertices and has no cycle
- n vertices need exactly n − 1 edges
- Adding one more edge creates a cycle
- The MST has the lowest total edge weight
  ::

## Kruskal's algorithm: cheapest edges anywhere | Slides 6-25 | must

Start with every vertex as its own tree, a forest. Add the cheapest edge that joins two different trees.

::steps Kruskal
Put each vertex in its own tree.
Sort edges by weight (or use a priority queue).
Take the cheapest remaining edge.
If it makes a cycle, reject it. Otherwise add it, merging two trees.
Stop once you have n − 1 edges.
::

Here's a small graph to practise on.

::graph Practice graph with the MST in bold
n A 0 80
n B 110 0
n C 110 160
n D 260 0
n E 260 160
n F 380 80
e A B 4
e A C 2 *
e B C 1 *
e B D 5 *
e C D 8
e C E 10
e D E 2 *
e D F 6
e E F 3 *
::

| Edge | Weight | Action                                | Edges so far |
| ---- | ------ | ------------------------------------- | ------------ |
| B–C  | 1      | Add                                   | 1            |
| A–C  | 2      | Add                                   | 2            |
| D–E  | 2      | Add                                   | 3            |
| E–F  | 3      | Add                                   | 4            |
| A–B  | 4      | **Reject: A, B, C already connected** | 4            |
| B–D  | 5      | Add, joins the two groups             | 5, done      |

**Total: 1 + 2 + 2 + 3 + 5 = 13**.

::mnemonic Kruskal Kicks around the whole graph
**K**ruskal picks edges from **anywhere**, so you can have several separate pieces growing at once.
::
::tip Running time: O(m log n)
Here m is the number of edges and n the number of vertices. The sort dominates, and the algorithm works best when there are few edges.
::
::key

- Kruskal builds a forest and merges trees
- Always take the cheapest remaining edge
- Reject an edge that would create a cycle
- Stop at n − 1 edges
- Running time is O(m log n)
  ::

## Prim's algorithm: grow one tree | Slides 26-40 | must

Start at one vertex, and keep attaching the cheapest edge that connects a new vertex to the tree.

::steps Prim
Pick any start vertex. It forms the tree.
Find the cheapest edge joining a tree vertex to a non-tree vertex.
Add that edge and vertex.
Repeat until all the vertices are in the tree.
::
::example Same graph, starting from A

- Tree {A}. Options: A–B 4, A–C 2. Take **A–C**.
- Tree {A, C}. Options: A–B 4, C–B 1, C–D 8, C–E 10. Take **C–B**.
- Tree {A, B, C}. Options: B–D 5, C–D 8, C–E 10. Take **B–D**.
- Tree {A, B, C, D}. Options: C–E 10, D–E 2, D–F 6. Take **D–E**.
- Tree {A, B, C, D, E}. Options: D–F 6, E–F 3. Take **E–F**.

**Total: 2 + 1 + 5 + 2 + 3 = 13**, the same as Kruskal.
::
::says Slide 10's handwriting | "Same cost, but different spanning tree, both are correct"
When edges tie, the two algorithms may choose different edges. The total cost is the same, and either tree is a correct answer.
::

|               | Kruskal                 | Prim                                       |
| ------------- | ----------------------- | ------------------------------------------ |
| Starts from   | All vertices separately | One vertex                                 |
| While running | A forest of pieces      | One growing tree                           |
| Picks         | Cheapest edge anywhere  | Cheapest edge touching the tree            |
| Cycle check   | Needed explicitly       | Automatic: only adds new vertices          |
| Better when   | Edges are few           | Both edges and vertices are few (slide 41) |

::mnemonic Prim Pushes outward
**P**rim grows from one **p**oint outward, always connected. **K**ruskal picks up **k**ernels from everywhere and joins them later.
::
::trap Prim is not Dijkstra
They look alike, but Prim compares the **single edge weight**. Dijkstra compares the **total distance from the source**.
::
::check In a graph with 10 vertices, how many edges does an MST have?
**9** (always n − 1).
::
::key

- Prim grows a single tree from a start vertex
- Add the cheapest edge between the tree and the rest
- Kruskal and Prim give the same total cost
- With ties, different correct trees can occur
- Prim compares edge weights, Dijkstra compares total distances
  ::
  @cheat

### Spanning tree

- All vertices, no cycles
- n − 1 edges exactly
- One more edge makes a cycle

### Kruskal

- Forest of single nodes
- Cheapest edge anywhere
- Reject if it makes a cycle
- O(m log n)

### Prim

- Start at one vertex
- Cheapest edge touching tree
- One connected tree always

### Comparison

- Same total cost
- Ties can give different trees
- Prim uses edge weight
- Dijkstra uses total distance
  @mcq 3
  A spanning tree on n vertices has how many edges?

* n − 1

- n
- n + 1
- 2n

> A tree on n vertices always has n − 1 edges.
> @mcq 3
> Adding one more edge to a spanning tree:

- Creates a cycle

* Disconnects it
* Lowers its total weight
* Removes a vertex

> Its endpoints are already connected, so the new edge closes a loop.
> @mcq 8
> What does Kruskal do when the cheapest edge would create a cycle?

- Rejects it and moves on

* Adds it anyway
* Restarts the algorithm
* Removes an existing edge

> A cycle-forming edge links two vertices already in one tree.
> @mcq 25
> Kruskal's running time for m edges and n vertices:

- O(m log n)

* O(n²m)
* O(m + n)
* O(2ⁿ)

> Slide 25 gives this result.
> @mcq 26
> Prim's algorithm grows:

- A single tree from a start vertex

* A forest of separate trees
* Two trees that meet in the middle
* A cycle covering all vertices

> It adds one new vertex per step to one connected tree.
> @mcq 3
> How many spanning trees does a complete graph on 4 vertices have?

- 16

* 4
* 6
* 12

> Slide 3 shows all 16.
> @mcq 10
> Two correct MST algorithms give different trees on a graph with tied edges. Their total weights are:

- Equal

* Different
* Double each other
* Impossible to compare

> Every MST has the same minimum total, even when the edges differ.
> @mcq 41
> According to the slides, Kruskal has better running times when:

- The number of edges is low

* The number of edges is very high
* All weights are equal
* The graph has cycles only

> Slide 41 notes this.
> @mcq 7
> Kruskal's algorithm initially treats the vertices as:

- n separate single-node trees

* One connected tree
* A cycle
* A sorted list of edges

> It starts with a forest and merges.
> @mcq 26
> Prim differs from Dijkstra because Prim compares:

- A single edge weight

* Total distance from the source
* The number of neighbours
* The vertex labels

> Dijkstra accumulates distance, and Prim looks only at the connecting edge.
> @short 7
> Describe Kruskal's algorithm and how it avoids cycles.
> ~ forest, cheapest, cycle, reject, n-1
> Start with each vertex as its own tree. Repeatedly take the cheapest remaining edge. If it would connect two vertices in the same tree it forms a cycle and is rejected; otherwise it merges two trees. Stop after n − 1 edges.
> @short 26
> Explain the main difference between Prim's and Kruskal's approach.
> ~ tree, forest, connected, anywhere, start
> Prim grows one connected tree from a start vertex, always adding the cheapest edge touching it. Kruskal considers the cheapest edge anywhere in the graph, building a forest whose trees merge over time.
> @short 2
> Define minimum spanning tree and give a real-world use.
> ~ all vertices, no cycles, minimum, weight, network
> It is a subgraph that connects all vertices without cycles and has the smallest total edge weight. It is used to design networks such as cables or roads at the lowest cost.

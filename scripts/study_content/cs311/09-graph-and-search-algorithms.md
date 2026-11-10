@head Topic 7
@title Graph and Search Algorithms
@sources topic-7-graph-and-search-algorithms
@count 68
@tldr Graphs model connections, and BFS and DFS are the two systematic ways to visit everything in one: BFS spreads out in layers using a queue, and DFS dives deep using a stack.
@why Traversals are short to code, and they appear everywhere. An exam will usually give you a graph and ask for the BFS or DFS order and tree, and those answers follow mechanically from the data structure. Most of this deck's 68 slides are just one example stepped through slowly.
@connect Dijkstra and MST were graph algorithms already. Backtracking in the next lecture is a depth-first search of a tree of choices.
@goals
- Use the terms adjacent, incident, degree, path, cycle, tree and forest correctly
- Choose an adjacency matrix or list for a given graph
- Trace BFS and DFS and label tree and non-tree edges
- State the properties of each traversal
@vocab
Vertex | A node of the graph.
Edge | A connection between two vertices.
Adjacent | Two vertices joined by an edge.
Incident | An edge and a vertex it touches.
Degree | How many edges touch a vertex.
Connected component | A maximal connected part of the graph.
@map
2-11 | Vocabulary | MEMORIZE | Adjacent, incident, simple path, cycle, tree, forest
12-13 | Representations | MEMORIZE | Matrix vs list and their space
14-28 | ExploreGraph | SKIM | The general template
29-43 | BFS | WRITE | Trace with a queue
44-58 | DFS | WRITE | Trace with a stack
59-68 | MST recap | SKIM | Same as Lecture 5.3

## The vocabulary of graphs | Slides 2-11 | must
A graph is a pair **G = (V, E)**: a set of vertices and a set of edges between them.

| Term | Meaning |
|---|---|
| **Adjacent** | Two vertices joined by an edge |
| **Incident** | An edge and a vertex at one of its ends |
| **Degree** | Number of incident edges (a self-loop counts twice) |
| **Isolated** | Degree 0 |
| **Pendant** | Degree 1 |
| **Directed edge** | Ordered pair (v, w), from source v to target w |
| **Path** | A sequence of vertices joined by edges |
| **Simple path** | No vertex appears more than once |
| **Cycle** | A path that returns to its start |
| **Connected** | There's a path between any two vertices |
| **Tree** | Connected with no cycles |
| **Forest** | No cycles, possibly disconnected |

::mnemonic Adjacent Ain't an edge
**Adjacent** relates **two vertices**. **Incident** relates a **vertex and an edge**. If both things are vertices, it's adjacent.
::
::tip Complete graph (slide 62)
Every pair of vertices is connected. K<sub>n</sub> has **n(n − 1)/2** undirected edges. K<sub>5</sub> has 10.
::
::key
- A graph is a set of vertices and a set of edges
- Adjacent is vertex to vertex, incident is vertex to edge
- A simple path repeats no vertex
- A tree is connected and acyclic, a forest is acyclic
- A complete graph has n(n−1)/2 edges
::

## Storing a graph | Slides 12-13 | must
| | Adjacency matrix | Adjacency list |
|---|---|---|
| Structure | V × V table of 0s and 1s | Each vertex has a list of neighbours |
| Space | **O(V²)** | **O(V + E)** |
| Is edge (u, v) present? | O(1) | Must scan u's list |
| Best for | **Dense** graphs | **Sparse** graphs |

::example Same small graph, both ways
Edges: 1–2, 1–3, 2–3, 3–4.

| | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| **1** | 0 | 1 | 1 | 0 |
| **2** | 1 | 0 | 1 | 0 |
| **3** | 1 | 1 | 0 | 1 |
| **4** | 0 | 0 | 1 | 0 |

List: 1 → 2, 3. 2 → 1, 3. 3 → 1, 2, 4. 4 → 3.
::
::analogy Seating chart or contact list
A matrix is a giant grid of every person against every other person, mostly blank. A list is each person's own short contact list. In a class of 1,000 where each person knows only 10 others, nobody would use the grid.
::
::key
- Adjacency matrix uses O(V²) space and suits dense graphs
- Adjacency list uses O(V+E) space and suits sparse graphs
- An undirected graph's matrix is symmetric
::

## BFS and DFS: same code, different container | Slides 14-58 | must
Slides 14 to 28 show a general procedure, `ExploreGraph`. It keeps a set S of edges still to look at. **BFS and DFS are that exact procedure, differing only in how S hands back the next edge.**

| | BFS | DFS |
|---|---|---|
| S is a | **Queue** (first in, first out) | **Stack** (last in, first out) |
| Shape of search | Layer by layer | One long path, then back up |
| Running time | **O(V + E)** | **O(V + E)** |

::mnemonic BFS is Broad, DFS is Deep
**B**FS goes **b**road, like people waiting in a **queue**. **D**FS goes **d**eep, like a **stack** of plates, where you always take the one you just added.
::

The example graph from the slides:

::graph Slide 16's graph | undirected
n 1 150 0
n 2 60 90
n 4 150 90
n 5 240 90
n 6 60 180
e 1 2
e 1 4
e 1 5
e 2 4
e 4 5
e 2 6
::

::steps BFS from vertex 1
Visit 1. Queue its edges: (1,4), (1,5), (1,2).
Dequeue (1,4). 4 is new: **tree edge**. Queue 4's edges.
Dequeue (1,5). 5 is new: **tree edge**.
Dequeue (1,2). 2 is new: **tree edge**.
The remaining edges from 4 and 5 lead only to visited vertices: **non-tree edges**.
Dequeue (2,6). 6 is new: **tree edge**.
Layers: **{1}, then {4, 5, 2}, then {6}**.
::
::steps DFS from vertex 1
Visit 1. Push (1,4), (1,2), (1,5) with (1,4) on top.
Pop (1,4). 4 is new: **tree edge**. Push 4's edges.
Pop (4,5). 5 is new: **tree edge**. Its edges lead to visited vertices.
Pop (4,2). 2 is new: **tree edge**. Push 2's edges.
Pop (2,6). 6 is new: **tree edge**.
Visit order: **1, 4, 5, 2, 6**.
::

| Property | BFS | DFS |
|---|---|---|
| Key theorem | Visits vertices by **increasing distance** from the root | For any non-tree edge, one end is an **ancestor** of the other |
| Edge constraint | Edge (v, w) with levels i, j: \|i − j\| ≤ 1 | |
| Useful for | Shortest path by number of edges | Exploring all options, cycle detection |

::tip Theorems about ExploreGraph (slide 28)
It visits every vertex. Each iteration of the for-loop explores one connected component. The tree edges form a spanning forest. So count the for-loop's iterations to count the components.
::
::trap Order depends on the neighbour order
The order in which neighbours are listed changes the traversal. If a question doesn't specify, use ascending or alphabetical order and say so.
::
::check Why is the running time O(V + E), rather than O(V × E)?
Each vertex is visited once and each edge is examined a constant number of times. The work adds up; it doesn't multiply.
::
::key
- BFS uses a queue and DFS uses a stack
- Both run in O(V+E)
- BFS visits by increasing distance from the root
- Tree edges reach new vertices, non-tree edges reach visited ones
- Each for-loop iteration in ExploreGraph finds one connected component
::
@cheat
### Terms
- Adjacent: two vertices
- Incident: vertex and edge
- Degree: edges at a vertex
- Tree: connected, acyclic
- Forest: acyclic
### Storage
- Matrix: O(V²), dense
- List: O(V+E), sparse
### BFS
- Queue
- Layers by distance
- O(V+E)
### DFS
- Stack (or recursion)
- Goes deep first
- O(V+E)
### Edges
- Tree edge: reaches new vertex
- Non-tree: reaches visited vertex
### Counts
- K<sub>n</sub> edges: n(n−1)/2
- Spanning tree: n−1 edges
@mcq 29
BFS uses which data structure?
+ Queue
- Stack
- Heap
- Hash table
> First in, first out gives layer-by-layer order.
@mcq 44
DFS uses which data structure?
+ Stack
- Queue
- Linked list only
- Min-heap
> Last in, first out makes it dive deep. Recursion uses the call stack.
@mcq 29
The running time of BFS and DFS using adjacency lists is:
+ O(V + E)
- O(V × E)
- O(V²)
- O(E log V)
> Each vertex and edge is handled a constant number of times.
@mcq 13
Space used by an adjacency list:
+ O(V + E)
- O(V²)
- O(E²)
- O(V log V)
> One entry per vertex and two per undirected edge.
@mcq 12
Which representation is better for a dense graph?
+ Adjacency matrix
- Adjacency list
- Edge list only
- Neither works
> When E is near V², the matrix wastes little space.
@mcq 43
BFS visits vertices by:
+ Increasing distance from the root
- Decreasing degree
- Alphabetical order only
- Depth, then backtracking
> Slide 43's theorem.
@mcq 62
A complete graph on 6 vertices has how many edges?
+ 15
- 12
- 30
- 36
> n(n − 1)/2 = 6 × 5 / 2.
@mcq 5
A simple path is one where:
+ No vertex appears twice
- No edge has weight
- It has at most 2 edges
- It returns to its start
> Slide 5.
@mcq 11
A forest is a graph that:
+ Contains no cycles but may be disconnected
- Is connected with one cycle
- Has exactly one tree
- Must be directed
> Each connected component of a forest is a tree.
@mcq 28
Each iteration of ExploreGraph's for-loop that starts on an unexplored vertex explores:
+ One connected component
- One edge
- All the vertices
- One layer
> Slide 28's second theorem.
@short 29
Explain the difference between BFS and DFS, including the data structures and search shape.
~ queue, stack, layers, deep, distance
> BFS uses a queue, so it explores in layers by increasing distance from the start. DFS uses a stack, so it follows one path as deep as possible and then backs up.
@short 12
When would you choose an adjacency list over a matrix?
~ sparse, space, O(V+E), edges
> For sparse graphs, where E is much smaller than V². A list uses O(V+E) space rather than O(V²).
@short 14
Define tree edge and non-tree edge in ExploreGraph.
~ unexplored, new vertex, visited, edge
> A tree edge is one that leads to an unexplored vertex, adding it to the search tree. A non-tree edge leads to a vertex that has already been visited.

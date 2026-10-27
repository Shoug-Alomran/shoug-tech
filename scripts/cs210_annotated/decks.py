"""CS210 annotated slides — all 16 decks (Goodrich/Tamassia and Sedgewick/Wayne slides).

The decks are mostly figures and code, so AUTO_SLIDES shows nearly every slide as the original image;
notes and practice questions are attached to the slides that carry the key ideas. Each deck is a
namespace class (see build_cs210_annotated_slides.py). Past-exam links point to the course's question
banks (Midterm 1, Quiz 1, Quiz 2)."""
from .common import mcq, past, scen, see, short, tf, tip, trap, trick

BIGO = 'Growth rates, slow → fast: 1 < log n < n < n log n < n² < n³ < 2ⁿ. Drop constants and lower-order terms.'


class algorithm_analysis:
    AUTO_SLIDES = True
    DECK = {'key': 'algorithm-analysis', 'slug': '01-algorithm-analysis', 'file': 'algorithm-analysis', 'title': 'Algorithm Analysis', 'chapter': 'Analysis',
            'pdf': '/academics/computer-science/cs210/slides/algorithm-analysis/',
            'lede': ('Measuring running time experimentally and its limits, primitive operations and theoretical analysis, '
                     'the seven important functions, growth rates, Big-Oh (and Big-Omega, Big-Theta), and the prefix-averages '
                     'example (quadratic vs. linear). Quiz 2 asked for the Big-O of code statements.')}
    ANN = {
        1: dict(kind='title', title='Analysis of Algorithms', body=[], tips=[tip(BIGO)]),
        10: dict(notes=['Experiments need an implementation, depend on hardware/software, and can’t cover all inputs → theoretical analysis.']),
        14: dict(notes=['Theoretical analysis: count primitive operations as a function of input size n; take the worst case.']),
        15: dict(notes=['Primitive operations: assignment, arithmetic, comparison, array index, method call, return.']),
        21: dict(notes=['Seven functions: constant, log n, n, n log n, n², n³, 2ⁿ.'], tips=[tip(BIGO)],
                 exam=[mcq('Which grows fastest?', ['2ⁿ', 'n³', 'n log n', 'n²'], 0, '')], weight=3),
        25: dict(notes=['Changing hardware changes T(n) by a constant factor but not the growth rate.']),
        32: dict(notes=['f(n) is O(g(n)) if f(n) ≤ c·g(n) for all n ≥ n₀ (some positive c, n₀).'],
                 exam=[mcq('7n − 2 is:', ['O(n)', 'O(1)', 'O(n²) only', 'O(log n)'], 0, 'It is also O(n²), but the tight bound is O(n).'),
                       mcq('3n³ + 20n² + 5 is:', ['O(n³)', 'O(n²)', 'O(n)', 'O(20n²)'], 0, '')], weight=3),
        40: dict(notes=['Big-Oh is an UPPER bound on the growth rate.']),
        42: dict(notes=['Asymptotic analysis: find the worst-case number of primitive operations, express it in Big-Oh.'],
                 past=[past('q2', 'Big-O of each statement')],
                 exam=[mcq('for (i = 0; i < n; i++) for (j = 0; j < n; j++) sum++; is:', ['O(n²)', 'O(n)', 'O(2n)', 'O(n log n)'], 0, ''),
                       mcq('for (i = 1; i < n; i *= 2) sum++; is:', ['O(log n)', 'O(n)', 'O(n²)', 'O(1)'], 0, '')], weight=3),
        44: dict(notes=['prefixAverage1 recomputes each sum → 1 + 2 + … + n → O(n²).']),
        46: dict(notes=['prefixAverage2 keeps a running sum → O(n).'],
                 exam=[short('Why is the second prefix-averages algorithm linear?', 'It keeps a running total, adding one element per step instead of re-summing all earlier elements, so each of the n steps is constant time: O(n) instead of O(n²).')], weight=2),
        48: dict(notes=['Big-Omega = lower bound; Big-Theta = tight bound (both upper and lower).'],
                 exam=[mcq('f(n) is Θ(g(n)) means:', ['f is both O(g) and Ω(g)', 'f is only an upper bound', 'f is only a lower bound', 'f equals g'], 0, '')], weight=3),
    }


class recursion:
    AUTO_SLIDES = True
    DECK = {'key': 'recursion', 'slug': '02-recursion', 'file': 'recursion', 'title': 'Recursion', 'chapter': 'Recursion',
            'pdf': '/academics/computer-science/cs210/slides/recursion/',
            'lede': 'Factorial, the English ruler, binary search and its analysis, linear, tail, binary and multiple recursion, recursive squaring, and Fibonacci (bad vs. good).'}
    ANN = {
        1: dict(kind='title', title='Recursion', body=[]),
        5: dict(notes=['English ruler: drawInterval(L) = drawInterval(L−1), a tick of length L, drawInterval(L−1).']),
        10: dict(notes=['Binary search halves the search range each call.']),
        12: dict(notes=['Binary search runs in O(log n).'],
                 exam=[mcq('Binary search on a sorted array of n elements is:', ['O(log n)', 'O(n)', 'O(1)', 'O(n log n)'], 0, '')], weight=3),
        13: dict(notes=['Linear recursion: at most one recursive call per invocation (sum, reverse array).']),
        20: dict(notes=['Recursive squaring: xⁿ = (x^(n/2))² → O(log n) multiplications.'], weight=2),
        22: dict(notes=['Tail recursion: the recursive call is the last step → easy to convert to a loop.']),
        23: dict(notes=['Binary recursion: two recursive calls per non-base case.']),
        25: dict(notes=['Naïve Fibonacci (binary recursion) is exponential: it recomputes the same values.'],
                 exam=[tf('The naïve recursive Fibonacci runs in linear time.', False, 'Exponential: about φⁿ calls.')], weight=3),
        27: dict(notes=['Better Fibonacci returns a pair (F(k), F(k−1)) → linear recursion, O(n).']),
    }


class lists:
    AUTO_SLIDES = True
    DECK = {'key': 'lists', 'slug': '03-lists', 'file': 'lists', 'title': 'Arrays, Linked Lists and Array Lists', 'chapter': 'Lists',
            'pdf': '/academics/computer-science/cs210/slides/lists/',
            'lede': ('Arrays (the scoreboard example, inserting and removing by shifting), singly linked lists (insert/remove at '
                     'head and tail), doubly linked lists with header and trailer sentinels, array lists, growable arrays '
                     '(incremental vs. doubling, amortized analysis), positional lists and iterators. The Midterm 1 and Quiz 1 '
                     'question banks are mostly linked-list code. (This handout carries an earlier student’s handwritten notes.)')}
    ANN = {
        1: dict(kind='content', whole=True, notes=['Arrays: length/capacity, declaring, the GameEntry/Scoreboard example.']),
        3: dict(notes=['Adding an entry at index i shifts n − i elements forward; removing shifts them back.'],
                exam=[mcq('Inserting at index 0 of an array holding n elements costs:', ['O(n)', 'O(1)', 'O(log n)', 'O(n²)'], 0, '')], weight=3),
        7: dict(notes=['Singly linked list: nodes with element + next; head (and tail) references.']),
        9: dict(notes=['Insert at head: new node → newest.next = head → head = newest. O(1).'],
                past=[past('q1', 'code to insert at the head')],
                exam=[mcq('Correct code to insert node N at the head of a doubly linked list:', ['N.next = Head; Head.prev = N; Head = N;', 'Head = N; N.next = Head;', 'N.next = Head.next; Head = N;', 'Head.next = N; Head = N;'], 0, 'Quiz 1.')],
                weight=3),
        10: dict(notes=['Insert at tail: O(1) with a tail reference.']),
        11: dict(notes=['Remove at head: head = head.next. O(1). Remove at tail of a SINGLY linked list is NOT O(1): you must walk to the node before the tail.'],
                 past=[past('m1', 'remove the last node / second-to-last'), past('q1', 'which operation is slowest in an SLL')],
                 exam=[mcq('Which singly-linked-list operation takes O(n) even with a tail pointer?', ['Removing the last node', 'Removing the first node', 'Inserting at the head', 'Inserting at the tail'], 0, '')],
                 weight=3),
        12: dict(notes=['Doubly linked list: prev and next; header and trailer sentinels simplify the edge cases.']),
        13: dict(notes=['Insert between p and its successor: link the new node both ways (4 pointer updates). Delete p: p.prev.next = p.next; p.next.prev = p.prev.'],
                 past=[past('q1', 'Before.next = After; After.prev = Before')],
                 exam=[mcq('To unlink node X between Before and After in a DLL:', ['Before.next = After; After.prev = Before;', 'Before.next = After.prev; After.prev = Before.next;', 'Before = After;', 'X.next = null only'], 0, 'Quiz 1.'),
                       mcq('A doubly linked list beats a singly linked list for:', ['Traversing in reverse order', 'Inserting at the head', 'Searching for a value', 'Memory usage'], 0, 'Quiz 1.')],
                 weight=3),
        17: dict(notes=['Array list (java.util.List): get, set, add(i, e), remove(i); add/remove at i shift elements → O(n).']),
        20: dict(notes=['Growable array: when full, copy into a bigger array.']),
        21: dict(notes=['Incremental strategy (+c each time): n pushes cost O(n²) → amortized O(n) per push. Doubling: O(n) total → amortized O(1).'],
                 tips=[trick('Grow by DOUBLING, not by a constant.')],
                 exam=[mcq('With the doubling strategy, the amortized cost of a push is:', ['O(1)', 'O(n)', 'O(log n)', 'O(n²)'], 0, '')], weight=3),
        22: dict(notes=['Positional list ADT: positions stay valid while other elements change.']),
        26: dict(notes=['Iterator: hasNext(), next(). Iterable: iterator(). for-each uses them.']),
    }


class circular_linked_lists:
    AUTO_SLIDES = True
    DECK = {'key': 'circular-linked-lists', 'slug': '04-circular-linked-lists', 'file': 'circular-linked-lists', 'title': 'Circular Linked Lists and Iterators',
            'chapter': 'Lists', 'pdf': '/academics/computer-science/cs210/slides/circular-linked-lists/',
            'lede': 'Round-robin scheduling, circular linked lists with only a tail reference (rotate, add, remove), and the Iterator and Iterable interfaces.'}
    ANN = {
        2: dict(notes=['Round-robin scheduling: each process gets a time slice, then goes to the back.']),
        4: dict(notes=['Circular list: the tail’s next points back to the head; keep only tail (head = tail.next).'],
                past=[past('q1', 'circular list operations'), past('m1', 'circular list size / remove')],
                exam=[mcq('In a circular singly linked list with a tail reference, the head is:', ['tail.next', 'tail.prev', 'null', 'tail'], 0, '')], weight=3),
        7: dict(notes=['rotate(): tail = tail.next moves the first element to the back in O(1).'], weight=2),
        13: dict(notes=['Iterable has iterator(); for-each works on any Iterable.']),
    }


class stacks_and_queues:
    AUTO_SLIDES = True
    DECK = {'key': 'stacks-and-queues', 'slug': '05-stacks-and-queues', 'file': 'stacks-and-queues', 'title': 'Stacks and Queues', 'chapter': 'Stacks & Queues',
            'pdf': '/academics/computer-science/cs210/slides/stacks-and-queues/',
            'lede': ('The stack ADT (LIFO) and its array and linked implementations, parentheses and HTML tag matching, evaluating '
                     'arithmetic expressions with two stacks; the queue ADT (FIFO), circular-array implementation, round robin, '
                     'and the Big-O of each implementation.')}
    ANN = {
        2: dict(notes=['Stack = last in, first out: push, pop, top, size, isEmpty.'],
                exam=[mcq('After push(1), push(2), push(3), pop(), the top is:', ['2', '3', '1', 'empty'], 0, '')], weight=3),
        10: dict(notes=['Array stack: O(1) operations but fixed capacity.']),
        13: dict(notes=['Parentheses matching: push openers, pop and compare on closers; stack empty at the end = balanced.'],
                 exam=[short('How does a stack check that ( [ { } ] ) is balanced?', 'Scan left to right: push every opening symbol; on a closing symbol pop and check it matches. If a pop finds the stack empty or a mismatch, it’s unbalanced; at the end the stack must be empty.')], weight=3),
        17: dict(notes=['Expression evaluation uses an operator stack and a value stack with precedence.']),
        23: dict(notes=['Queue = first in, first out: enqueue, dequeue, first.'],
                 exam=[mcq('enqueue(1), enqueue(2), enqueue(3), dequeue() returns:', ['1', '3', '2', 'null'], 0, '')], weight=3),
        33: dict(notes=['Circular array queue: f (front index) and size; r = (f + size) mod N.'],
                 exam=[mcq('In a circular array queue of capacity N, the index after r is:', ['(r + 1) mod N', 'r + 1', 'r − 1', 'N − r'], 0, '')], weight=3),
        36: dict(notes=['Round robin with a queue: dequeue, serve, enqueue.']),
        37: dict(notes=['Array queue and linked queue: all operations O(1).']),
    }


class elementary_sorting_algorithms:
    AUTO_SLIDES = True
    DECK = {'key': 'elementary-sorting-algorithms', 'slug': '06-elementary-sorting-algorithms', 'file': 'elementary-sorting-algorithms',
            'title': 'Elementary Sorting Algorithms', 'chapter': 'Sorting', 'pdf': '/academics/computer-science/cs210/slides/elementary-sorting-algorithms/',
            'lede': 'Sorting with callbacks (Comparable), selection sort and insertion sort: inner loops, Java code, animations, and their compare and exchange counts.'}
    ANN = {
        9: dict(notes=['Sort any type that implements Comparable (compareTo).']),
        15: dict(notes=['Selection sort: find the minimum of the rest, swap it into position i.'],
                 past=[past('q2', 'selection sort steps')]),
        19: dict(notes=['Selection sort: ~n²/2 compares and n exchanges, regardless of input order.'],
                 exam=[mcq('Selection sort on an already sorted array takes:', ['Quadratic time', 'Linear time', 'Logarithmic time', 'Constant time'], 0, '')], weight=3),
        22: dict(notes=['Insertion sort: move element i left past every larger element.']),
        28: dict(notes=['Insertion sort: best case (sorted) ~n compares; worst (reverse) ~n²/2; average ~n²/4.'],
                 exam=[mcq('Which elementary sort runs in linear time on an already sorted array?', ['Insertion sort', 'Selection sort', 'Both', 'Neither'], 0, '')], weight=3),
    }


class merge_sort:
    AUTO_SLIDES = True
    DECK = {'key': 'merge-sort', 'slug': '07-merge-sort', 'file': 'merge-sort', 'title': 'Merge Sort', 'chapter': 'Sorting',
            'pdf': '/academics/computer-science/cs210/slides/merge-sort/',
            'lede': 'Mergesort: merging, the recursive top-down sort and bottom-up version, its N log N analysis and extra memory, comparators, and stability.'}
    ANN = {
        2: dict(notes=['Mergesort: sort each half recursively, then merge.']),
        13: dict(notes=['Mergesort uses at most N lg N compares (and ~6 N lg N array accesses).'],
                 exam=[mcq('Mergesort’s running time in the worst case is:', ['O(n log n)', 'O(n²)', 'O(n)', 'O(log n)'], 0, '')], weight=3),
        17: dict(notes=['Mergesort needs extra memory proportional to N (the aux array): not in place.'],
                 exam=[tf('Standard mergesort sorts in place with constant extra memory.', False, 'It needs an auxiliary array of size N.')], weight=3),
        20: dict(notes=['Bottom-up mergesort: merge subarrays of size 1, 2, 4, 8… without recursion.'],
                 past=[past('q2', 'merge sort tree for airport codes')],
                 exam=[short('Merge sort [RUH, AMM, DMM, JED, KWI, DXB, SFO]. (Quiz 2)', 'Split to single items, then merge: [AMM, RUH] [DMM, JED] [DXB, KWI] [SFO] → [AMM, DMM, JED, RUH] [DXB, KWI, SFO] → [AMM, DMM, DXB, JED, KWI, RUH, SFO].')], weight=3),
        34: dict(notes=['Stable sort: equal keys keep their relative order. Insertion and merge sort are stable; selection sort (and quicksort) are not.'],
                 exam=[mcq('Which sort is stable?', ['Mergesort', 'Selection sort', 'Quicksort', 'Heapsort'], 0, '')], weight=3),
    }


class quick_sort:
    AUTO_SLIDES = True
    DECK = {'key': 'quick-sort', 'slug': '08-quick-sort', 'file': 'quick-sort', 'title': 'Quick Sort', 'chapter': 'Sorting',
            'pdf': '/academics/computer-science/cs210/slides/quick-sort/',
            'lede': 'Quicksort: partitioning, the Java implementation, best/worst/average case, why we shuffle, duplicate keys, and how it compares with the other sorts.'}
    ANN = {
        11: dict(notes=['Partition around a pivot: smaller items left, larger right; the pivot lands in its final place.'],
                 past=[past('q2', 'partition after the first round')]),
        15: dict(notes=['Shuffle first, partition, then sort each part recursively.']),
        21: dict(notes=['Best case: ~N lg N compares. Worst case (already sorted, no shuffle): ~N²/2.'],
                 past=[past('q2', 'which sequence makes quicksort O(n²)')],
                 exam=[mcq('Without shuffling, quicksort (first element as pivot) is slowest on:', ['An already sorted array', 'A random array', 'An array of distinct keys', 'A small array'], 0, 'Quiz 2.')], weight=3),
        28: dict(notes=['Average ~1.39 N lg N compares; in place; not stable.'],
                 exam=[mcq('Quicksort’s average running time is:', ['O(n log n)', 'O(n²)', 'O(n)', 'O(log n)'], 0, '')], weight=3),
        36: dict(notes=['Summary: selection n²/2, insertion n²/4 average, merge N lg N (stable, extra space), quick 1.39 N lg N (in place, fastest in practice).']),
    }


class trees:
    AUTO_SLIDES = True
    DECK = {'key': 'trees', 'slug': '09-trees', 'file': 'trees', 'title': 'Trees', 'chapter': 'Trees',
            'pdf': '/academics/computer-science/cs210/slides/trees/',
            'lede': 'Tree terminology and ADT, preorder/postorder traversals, binary trees and their properties, inorder traversal, expression trees, Euler tour, and linked and array representations.'}
    ANN = {
        3: dict(notes=['Root, internal and external (leaf) nodes, ancestors, descendants, depth (from root), height (max depth), subtree.'],
                exam=[mcq('The height of a tree is:', ['The maximum depth of any node', 'The number of nodes', 'The number of leaves', 'The depth of the root'], 0, '')], weight=3),
        6: dict(notes=['Preorder: node, then children. Postorder: children, then node.']),
        9: dict(notes=['Binary tree: each node has at most two children (left, right). Proper: 0 or 2 children.']),
        14: dict(notes=['Proper binary tree: e = i + 1 (leaves = internal + 1); h ≤ i; e ≤ 2ʰ.'],
                 exam=[mcq('A proper binary tree with 7 internal nodes has how many leaves?', ['8', '7', '14', '6'], 0, 'e = i + 1.')], weight=3),
        16: dict(notes=['Inorder: left, node, right.'],
                 exam=[mcq('Inorder traversal of a BST gives the keys:', ['In sorted order', 'In reverse order', 'In insertion order', 'Level by level'], 0, '')], weight=3),
        17: dict(notes=['Print an arithmetic expression: inorder with parentheses. Evaluate it: postorder.']),
        19: dict(notes=['Euler tour: visit each node on the left, from below, and on the right (generalizes all three).']),
        23: dict(notes=['Array representation: root at 1 (or 0); children of node i at 2i and 2i + 1 (with root at 1).'],
                 exam=[mcq('With the root at index 1, the children of node i are at:', ['2i and 2i + 1', 'i + 1 and i + 2', '2i − 1 and 2i', 'i/2'], 0, '')], weight=3),
    }


class binary_search_trees:
    AUTO_SLIDES = True
    DECK = {'key': 'binary-search-trees', 'slug': '10-binary-search-trees', 'file': 'binary-search-trees', 'title': 'Binary Search Trees', 'chapter': 'Trees',
            'pdf': '/academics/computer-science/cs210/slides/binary-search-trees/',
            'lede': 'BST definition, search and insert (Java), tree shape and its effect on cost, lazy deletion, deleting the minimum, and Hibbard deletion.'}
    ANN = {
        3: dict(notes=['BST: every node’s key is larger than all keys in its left subtree and smaller than all in its right.']),
        8: dict(notes=['Search: compare and go left or right; cost = depth.']),
        13: dict(notes=['Shape depends on insertion order: random → ~1.39 lg N; sorted order → a path (N).'],
                 exam=[mcq('Inserting 1, 2, 3, 4, 5 in order into an empty BST gives height:', ['4 (a path)', '2', '3', '1'], 0, '')], weight=3),
        16: dict(notes=['BST: average O(log N), worst O(N) for search and insert.']),
        21: dict(notes=['Delete min: go left until null left link, replace that node by its right link.']),
        22: dict(notes=['Hibbard deletion: 0 children → remove; 1 child → replace with child; 2 children → replace with successor (min of right subtree).'],
                 exam=[short('How do you delete a node with two children from a BST?', 'Find its successor (the minimum of its right subtree), copy the successor’s key into the node, then delete the successor (which has at most one child).')], weight=3),
        29: dict(notes=['Hibbard deletion makes trees unbalanced over time (√N height).']),
    }


class avl_trees:
    AUTO_SLIDES = True
    DECK = {'key': 'avl-trees', 'slug': '11-avl-trees', 'file': 'avl-trees', 'title': 'AVL Trees', 'chapter': 'Trees',
            'pdf': '/academics/computer-science/cs210/slides/avl-trees/',
            'lede': 'The AVL height-balance property, why it keeps height O(log n), insertion with trinode restructuring (single and double rotations), removal, and performance.'}
    ANN = {
        2: dict(notes=['AVL property: for every node, the heights of its two children differ by at most 1.'],
                exam=[mcq('An AVL tree requires that for every node, the children’s heights differ by at most:', ['1', '0', '2', 'log n'], 0, '')], weight=3),
        5: dict(notes=['Height of an AVL tree with n nodes is O(log n).']),
        9: dict(notes=['Trinode restructuring: take the unbalanced node z, its taller child y and grandchild x; make the middle one the root of the subtree.']),
        11: dict(notes=['Single rotation when x, y, z are in a straight line (LL or RR).']),
        15: dict(notes=['Double rotation when they zig-zag (LR or RL).'],
                 exam=[mcq('An imbalance caused by inserting into the right subtree of a node’s left child needs a:', ['Double rotation', 'Single rotation', 'No rotation', 'Rehash'], 0, '')], weight=3),
        21: dict(notes=['Search, insert and remove are all O(log n) in an AVL tree.'],
                 exam=[mcq('Worst-case search in an AVL tree with n nodes:', ['O(log n)', 'O(n)', 'O(1)', 'O(n log n)'], 0, '')], weight=3),
    }


class heaps_and_priority_queues:
    AUTO_SLIDES = True
    DECK = {'key': 'heaps-and-priority-queues', 'slug': '12-heaps-and-priority-queues', 'file': 'heaps-and-priority-queues', 'title': 'Heaps and Priority Queues',
            'chapter': 'Heaps', 'pdf': '/academics/computer-science/cs210/slides/heaps-and-priority-queues/',
            'lede': 'The priority queue API and applications, elementary implementations, complete binary trees, binary heaps in an array, swim (promotion) and sink (demotion), and the cost summary.'}
    ANN = {
        5: dict(notes=['MaxPQ: insert, delMax, isEmpty.']),
        7: dict(notes=['Unordered array: insert O(1), delMax O(N). Ordered array: insert O(N), delMax O(1). Binary heap: both O(log N).'],
                exam=[mcq('With a binary heap, insert and delete-max are:', ['O(log N) each', 'O(1) each', 'O(N) each', 'O(1) and O(N)'], 0, '')], weight=3),
        9: dict(notes=['Complete binary tree: perfectly balanced except the bottom level, filled left to right; height ⌊lg N⌋.']),
        13: dict(notes=['Heap-ordered: every parent ≥ its children (max-heap). Array: parent of k is k/2; children 2k, 2k + 1.'],
                 exam=[mcq('In a 1-based heap array, the parent of the node at index 9 is at:', ['4', '5', '18', '8'], 0, '')], weight=3),
        17: dict(notes=['Insert: add at the end, swim up while larger than parent.']),
        19: dict(notes=['Delete max: swap root with the last item, remove it, sink the new root.']),
    }


class heaps:
    AUTO_SLIDES = True
    DECK = {'key': 'heaps', 'slug': '13-heaps', 'file': 'heaps', 'title': 'Heaps', 'chapter': 'Heaps',
            'pdf': '/academics/computer-science/cs210/slides/heaps/',
            'lede': 'Heaps (Goodrich): the priority queue ADT and PQ-sorting, heap-order and completeness, height, insertion with upheap, removal with downheap, heap-sort, array-based heaps, merging, and bottom-up construction in O(n).'}
    ANN = {
        4: dict(notes=['Heap: heap-order (key(v) ≥ key(parent(v)) for a min-heap) and a complete binary tree.']),
        11: dict(notes=['A heap with n keys has height O(log n).']),
        14: dict(notes=['Upheap after insertion: swap up while the key is smaller than its parent → O(log n).']),
        17: dict(notes=['Downheap after removeMin: swap down with the smaller child → O(log n).']),
        19: dict(notes=['Heap-sort: n inserts + n removeMins → O(n log n).'],
                 exam=[mcq('Heap-sort runs in:', ['O(n log n)', 'O(n²)', 'O(n)', 'O(log n)'], 0, '')], weight=3),
        22: dict(notes=['Bottom-up construction builds a heap from n keys in O(n).'],
                 exam=[tf('Bottom-up heap construction takes O(n log n) and cannot be faster.', False, 'It is O(n).')], weight=3),
    }


class hash_tables:
    AUTO_SLIDES = True
    DECK = {'key': 'hash-tables', 'slug': '14-hash-tables', 'file': 'hash-tables', 'title': 'Hash Tables', 'chapter': 'Hashing',
            'pdf': '/academics/computer-science/cs210/slides/hash-tables/',
            'lede': 'Hash functions and Java’s hashCode conventions, modular hashing, the uniform hashing assumption, collisions, separate chaining, linear probing, resizing and deletion, and the cost summary.'}
    ANN = {
        2: dict(notes=['Hashing: compute an array index from the key; handle collisions.']),
        6: dict(notes=['Java: if x.equals(y) then x.hashCode() == y.hashCode().'],
                 exam=[tf('Two objects with the same hashCode must be equal.', False, 'Equal objects must have equal hash codes, not the reverse.')], weight=3),
        16: dict(notes=['Modular hashing: (key.hashCode() & 0x7fffffff) % M.']),
        20: dict(notes=['Collision: two keys hash to the same index.']),
        23: dict(notes=['Separate chaining: each slot holds a linked list of the keys that hash there.'],
                 exam=[mcq('In separate chaining, colliding keys are stored:', ['In a linked list at that index', 'In the next empty slot', 'In a second table', 'They are rejected'], 0, '')], weight=3),
        33: dict(notes=['Open addressing / linear probing: on collision, try the next slot (i + 1) until empty.'],
                 exam=[mcq('With linear probing, a key that hashes to a full slot goes to:', ['The next free slot', 'A linked list', 'The previous slot', 'The end of the table'], 0, '')], weight=3),
        37: dict(notes=['Keep the table at most about half full for linear probing (α ≤ ½).']),
        44: dict(notes=['Hashing: constant expected time for search/insert/delete; no ordered operations.'],
                 exam=[mcq('Expected cost of search in a well-sized hash table:', ['O(1)', 'O(log n)', 'O(n)', 'O(n log n)'], 0, '')], weight=3),
    }


class undirected_graphs:
    AUTO_SLIDES = True
    DECK = {'key': 'undirected-graphs', 'slug': '15-undirected-graphs', 'file': 'undirected-graphs', 'title': 'Undirected Graphs', 'chapter': 'Graphs',
            'pdf': '/academics/computer-science/cs210/slides/undirected-graphs/',
            'lede': 'Graph terminology and applications, the Graph API, representations (edge list, adjacency matrix, adjacency lists), depth-first search, breadth-first search and shortest paths, and connected components.'}
    ANN = {
        13: dict(notes=['Path, cycle, connected, degree. Two vertices are connected if there is a path between them.']),
        21: dict(notes=['Adjacency matrix: V × V booleans, O(V²) space; check an edge in O(1).']),
        22: dict(notes=['Adjacency lists: a list of neighbours per vertex; space O(E + V). Used in practice (sparse graphs).'],
                 exam=[mcq('For a large sparse graph, the usual representation is:', ['Adjacency lists', 'Adjacency matrix', 'Edge list only', 'Incidence matrix'], 0, '')], weight=3),
        33: dict(notes=['DFS: go as deep as possible, backtrack; marks every vertex connected to s in time proportional to the sum of degrees.']),
        44: dict(notes=['BFS: visit vertices in order of distance from s using a QUEUE; finds shortest paths (fewest edges).'],
                 exam=[mcq('Which search finds the path with the fewest edges in an unweighted graph?', ['Breadth-first search', 'Depth-first search', 'Both always', 'Neither'], 0, ''),
                       mcq('BFS uses which data structure?', ['A queue', 'A stack', 'A heap', 'A hash table'], 0, '')], weight=3),
        55: dict(notes=['Connected components: run DFS from each unmarked vertex; label vertices with a component id.']),
    }


class directed_graphs:
    AUTO_SLIDES = True
    DECK = {'key': 'directed-graphs', 'slug': '16-directed-graphs', 'file': 'directed-graphs', 'title': 'Directed Graphs', 'chapter': 'Graphs',
            'pdf': '/academics/computer-science/cs210/slides/directed-graphs/',
            'lede': 'Digraph applications, the Digraph API and adjacency lists, reachability with DFS, BFS in digraphs (web crawler), topological sort, and directed cycle detection.'}
    ANN = {
        3: dict(notes=['Digraph: edges have a direction (v → w).']),
        16: dict(notes=['Adjacency lists, but each edge appears once (in v’s list only).']),
        21: dict(notes=['Reachability: which vertices can be reached from s → DFS.']),
        32: dict(notes=['BFS in digraphs finds directed shortest paths.']),
        43: dict(notes=['Topological sort: order vertices so every edge points forward. Possible only for a DAG. Reverse DFS postorder gives it.'],
                 exam=[mcq('A topological order exists if and only if the digraph:', ['Has no directed cycle (is a DAG)', 'Is strongly connected', 'Is undirected', 'Has a cycle'], 0, '')], weight=3),
        49: dict(notes=['Directed cycle detection with DFS (a back edge to a vertex on the stack).']),
    }


DECKS_HERE = [algorithm_analysis, recursion, lists, circular_linked_lists, stacks_and_queues, elementary_sorting_algorithms, merge_sort, quick_sort,
              trees, binary_search_trees, avl_trees, heaps_and_priority_queues, heaps, hash_tables, undirected_graphs, directed_graphs]

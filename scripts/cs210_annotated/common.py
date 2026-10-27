"""Constructors for CS210 annotated-slide content. The markup is the SE423 one (see se423_annotated/ch01_introduction.py)."""
from se423_annotated.common import mcq, scen, section, short, slide, tf, tip, trap, trick  # noqa: F401
from cs331_annotated.common import fig  # noqa: F401

# Every CS210 deck, in course order: key -> (annotated slug, standalone file, slides folder, label).
DECKS = {
    'algorithm-analysis': ('01-algorithm-analysis', 'algorithm-analysis', 'algorithm-analysis', 'Algorithm Analysis'),
    'recursion': ('02-recursion', 'recursion', 'recursion', 'Recursion'),
    'lists': ('03-lists', 'lists', 'lists', 'Arrays, Linked Lists and Array Lists'),
    'circular-linked-lists': ('04-circular-linked-lists', 'circular-linked-lists', 'circular-linked-lists', 'Circular Linked Lists and Iterators'),
    'stacks-and-queues': ('05-stacks-and-queues', 'stacks-and-queues', 'stacks-and-queues', 'Stacks and Queues'),
    'elementary-sorting-algorithms': ('06-elementary-sorting-algorithms', 'elementary-sorting-algorithms', 'elementary-sorting-algorithms', 'Elementary Sorting Algorithms'),
    'merge-sort': ('07-merge-sort', 'merge-sort', 'merge-sort', 'Merge Sort'),
    'quick-sort': ('08-quick-sort', 'quick-sort', 'quick-sort', 'Quick Sort'),
    'trees': ('09-trees', 'trees', 'trees', 'Trees'),
    'binary-search-trees': ('10-binary-search-trees', 'binary-search-trees', 'binary-search-trees', 'Binary Search Trees'),
    'avl-trees': ('11-avl-trees', 'avl-trees', 'avl-trees', 'AVL Trees'),
    'heaps-and-priority-queues': ('12-heaps-and-priority-queues', 'heaps-and-priority-queues', 'heaps-and-priority-queues', 'Heaps and Priority Queues'),
    'heaps': ('13-heaps', 'heaps', 'heaps', 'Heaps'),
    'hash-tables': ('14-hash-tables', 'hash-tables', 'hash-tables', 'Hash Tables'),
    'undirected-graphs': ('15-undirected-graphs', 'undirected-graphs', 'undirected-graphs', 'Undirected Graphs'),
    'directed-graphs': ('16-directed-graphs', 'directed-graphs', 'directed-graphs', 'Directed Graphs'),
}

# The real CS210 papers in exams/.
PAPERS = {
    'm1': ('Midterm 1 question bank', '01-midterm-1'),
    'q1': ('Quiz 1 question bank', '02-quiz-1'),
    'q2': ('Quiz 2 question bank', '03-quiz-2'),
}


def past(paper, label, related=False):
    assert paper in PAPERS, paper
    return {'paper': paper, 'label': label, 'related': related}


def see(deck, n, label):
    assert deck in DECKS, deck
    return {'deck': deck, 'n': n, 'label': label}

"""Constructors for CS102 annotated-slide content. The markup is the SE423 one (see se423_annotated/ch01_introduction.py)."""
from se423_annotated.common import mcq, scen, section, short, slide, tf, tip, trap, trick  # noqa: F401
from cs331_annotated.common import fig  # noqa: F401

# Every CS102 deck, in course order: key -> (annotated slug, standalone file, slides folder, label).
DECKS = {
    'classes': ('01-classes', 'classes', 'classes', 'Classes'),
    'interfaces': ('02-comparable-comparator-and-interfaces', 'comparable-comparator-and-interfaces', 'comparable-comparator-and-interfaces',
                   'Comparable, Comparator and Interfaces'),
    'files': ('03-files', 'files', 'files', 'Files'),
    'generics': ('04-generic-classes', 'generic-classes', 'generic-classes', 'Generic Classes and Methods'),
    'inheritance': ('05-inheritance', 'inheritance', 'inheritance', 'Inheritance'),
    'collections': ('06-java-collection-framework', 'java-collection-framework', 'java-collection-framework', 'Java Collection Framework'),
    'linked-lists': ('07-linked-lists', 'linked-lists', 'linked-lists', 'Linked Lists'),
    'polymorphism': ('08-polymorphism', 'polymorphism', 'polymorphism', 'Polymorphism'),
    'recursion': ('09-recursion', 'recursion', 'recursion', 'Recursion'),
    'collections-2': ('10-java-collection-framework-part-2', 'java-collection-framework-part-2', 'java-collection-framework-part-2',
                      'Java Collection Framework Part 2'),
    'arrays-2d': ('11-multidimensional-arrays', 'multidimensional-arrays', 'chapter-8', 'Multidimensional Arrays (Chapter 8)'),
}

# The real CS102 papers in exams/.
PAPERS = {
}


def past(paper, label, related=False):
    assert paper in PAPERS, paper
    return {'paper': paper, 'label': label, 'related': related}


def see(deck, n, label):
    assert deck in DECKS, deck
    return {'deck': deck, 'n': n, 'label': label}

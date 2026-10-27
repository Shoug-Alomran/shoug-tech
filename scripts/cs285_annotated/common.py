"""Constructors for CS285 annotated-slide content. The markup is the SE423 one (see se423_annotated/ch01_introduction.py)."""
from se423_annotated.common import mcq, scen, section, short, slide, tf, tip, trap, trick  # noqa: F401
from cs331_annotated.common import fig  # noqa: F401

# Every CS285 deck, in course order: key -> (annotated slug, standalone file, slides folder, label).
DECKS = {
    'd01': ('01-logic-and-proofs', 'logic-and-proofs', 'chapter-1-logic-and-proofs', 'Chapter 1: Logic and Proofs'),
    'd02': ('02-basic-structures', 'basic-structures', 'chapter-2-basic-structures', 'Chapter 2: Basic Structures'),
    'd03': ('03-number-theory-and-cryptography', 'number-theory-and-cryptography', 'chapter-4-number-theory-and-cryptography', 'Chapter 4: Number Theory and Cryptography'),
    'd04': ('04-induction-and-recursion-handout', 'induction-and-recursion-handout', 'chapter-5-induction-and-recursion-handout', 'Chapter 5: Induction and Recursion (Handout)'),
    'd05': ('05-mathematical-induction-and-recursion', 'mathematical-induction-and-recursion', 'chapter-5-mathematical-induction-and-recursion', 'Chapter 5: Mathematical Induction and Recursion'),
    'd06': ('06-counting', 'counting', 'chapter-6-counting', 'Chapter 6: Counting'),
    'd07': ('07-advanced-counting-techniques', 'advanced-counting-techniques', 'chapter-8-advanced-counting-techniques', 'Chapter 8: Advanced Counting Techniques'),
    'd08': ('08-relations', 'relations', 'chapter-9-relations', 'Chapter 9: Relations'),
}

# The real CS285 papers in exams/.
PAPERS = {
}


def past(paper, label, related=False):
    assert paper in PAPERS, paper
    return {'paper': paper, 'label': label, 'related': related}


def see(deck, n, label):
    assert deck in DECKS, deck
    return {'deck': deck, 'n': n, 'label': label}

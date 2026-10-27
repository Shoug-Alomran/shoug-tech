"""Constructors for CS340 annotated-slide content. The markup is the SE423 one (see se423_annotated/ch01_introduction.py)."""
from se423_annotated.common import mcq, scen, section, short, slide, tf, tip, trap, trick  # noqa: F401
from cs331_annotated.common import fig  # noqa: F401

# Every CS340 deck, in course order: key -> (annotated slug, standalone file, slides folder, label).
DECKS = {
    'd01': ('01-introduction-to-databases', 'introduction-to-databases', 'chapter-1-introduction-to-databases', 'Chapter 1: Introduction to Databases'),
    'd02': ('02-database-system-concepts-and-architecture', 'database-system-concepts-and-architecture', 'chapter-2-database-system-concepts-and-architecture', 'Chapter 2: Database System Concepts and Architecture'),
    'd03': ('03-data-modeling-using-er-and-eer', 'data-modeling-using-er-and-eer', 'chapter-3-data-modeling-using-er-and-eer', 'Chapter 3: Data Modeling Using ER and EER'),
    'd04': ('04-relational-model', 'relational-model', 'chapter-4-relational-model', 'Chapter 4: Relational Model'),
    'd05': ('05-er-to-relational-mapping-and-ddl', 'er-to-relational-mapping-and-ddl', 'chapter-5-er-to-relational-mapping-and-ddl', 'Chapter 5: ER-to-Relational Mapping and DDL'),
    'd06': ('06-basic-sql', 'basic-sql', 'chapter-6-basic-sql', 'Chapter 6: Basic SQL'),
    'd07': ('07-advanced-sql', 'advanced-sql', 'chapter-7-advanced-sql', 'Chapter 7: Advanced SQL'),
    'd08': ('08-normalization', 'normalization', 'chapter-9-normalization', 'Chapter 9: Normalization'),
    'd09': ('09-nosql-and-object-oriented-databases', 'nosql-and-object-oriented-databases', 'chapter-10-nosql-and-object-oriented-databases', 'Chapter 10: NoSQL and Object-Oriented Databases'),
}

# The real CS340 papers in exams/.
PAPERS = {
    'mid': ('Midterm exam', '09-midterm-exam'),
    'f251': ('Final exam 251 (practice replica)', '08-final-exam-251-practice'),
}


def past(paper, label, related=False):
    assert paper in PAPERS, paper
    return {'paper': paper, 'label': label, 'related': related}


def see(deck, n, label):
    assert deck in DECKS, deck
    return {'deck': deck, 'n': n, 'label': label}

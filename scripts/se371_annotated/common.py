"""Constructors for SE371 annotated-slide content. The markup is the SE423 one (see se423_annotated/ch01_introduction.py)."""
from se423_annotated.common import mcq, scen, section, short, slide, tf, tip, trap, trick  # noqa: F401
from cs331_annotated.common import fig  # noqa: F401

# Every SE371 deck, in course order: key -> (annotated slug, standalone file, slides folder, label).
DECKS = {
    'd01': ('01-introduction-to-the-web', 'introduction-to-the-web', 'chapter-01-introduction-to-the-web', 'Chapter 1: Introduction to the Web'),
    'd02': ('02-html-2', 'html-2', 'chapter-02-html-2', 'Chapter 2: HTML'),
    'd03': ('03-css', 'css', 'chapter-03-css', 'Chapter 3: CSS'),
    'd04': ('04-javascript', 'javascript', 'chapter-04-javascript', 'Chapter 4: JavaScript'),
    'd05': ('05-javascript-in-the-front-end', 'javascript-in-the-front-end', 'chapter-05-javascript-in-the-front-end', 'Chapter 5: JavaScript in the Front End'),
    'd06': ('06-server-side-node', 'server-side-node', 'chapter-06-server-side-node', 'Chapter 6: Server-Side Node'),
    'd07': ('07-working-with-databases', 'working-with-databases', 'chapter-07-working-with-databases', 'Chapter 7: Working with Databases'),
}

# The real SE371 papers in exams/.
PAPERS = {
}


def past(paper, label, related=False):
    assert paper in PAPERS, paper
    return {'paper': paper, 'label': label, 'related': related}


def see(deck, n, label):
    assert deck in DECKS, deck
    return {'deck': deck, 'n': n, 'label': label}

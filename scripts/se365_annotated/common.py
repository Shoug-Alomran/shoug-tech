"""Constructors for SE365 annotated-slide content. The markup is the SE423 one (see se423_annotated/ch01_introduction.py)."""
from se423_annotated.common import mcq, scen, section, short, slide, tf, tip, trap, trick  # noqa: F401
from cs331_annotated.common import fig  # noqa: F401

# Every SE365 deck, in course order: key -> (annotated slug, standalone file, slides folder, label).
DECKS = {
    'd01': ('01-lecture-01-introduction-to-human-computer-interaction', 'lecture-01-introduction-to-human-computer-interaction', 'lecture-01-introduction-to-human-computer-interaction', 'Lecture 1: Introduction to Human–Computer Interaction'),
    'd02': ('02-lecture-02-cognitive-aspects', 'lecture-02-cognitive-aspects', 'lecture-02-cognitive-aspects', 'Lecture 2: Cognitive Aspects'),
    'd03': ('03-lecture-03-emotional-interaction', 'lecture-03-emotional-interaction', 'lecture-03-emotional-interaction', 'Lecture 3: Emotional Interaction'),
    'd04': ('04-lecture-04-interaction-and-interfaces', 'lecture-04-interaction-and-interfaces', 'lecture-04-interaction-and-interfaces', 'Lecture 4: Interaction and Interfaces'),
    'd05': ('05-lecture-05-the-process-of-interaction-design', 'lecture-05-the-process-of-interaction-design', 'lecture-05-the-process-of-interaction-design', 'Lecture 5: The Process of Interaction Design'),
    'd06': ('06-lecture-06-07-establishing-requirements', 'lecture-06-07-establishing-requirements', 'lecture-06-07-establishing-requirements', 'Lectures 6–7: Establishing Requirements'),
    'd07': ('07-lecture-08-design-principles-and-guidelines', 'lecture-08-design-principles-and-guidelines', 'lecture-08-design-principles-and-guidelines', 'Lecture 8: Design Principles and Guidelines'),
    'd08': ('08-lecture-09-10-design-prototyping-and-construction', 'lecture-09-10-design-prototyping-and-construction', 'lecture-09-10-design-prototyping-and-construction', 'Lectures 9–10: Design, Prototyping and Construction'),
    'd09': ('09-lecture-11-evaluation-foundations', 'lecture-11-evaluation-foundations', 'lecture-11-evaluation-foundations', 'Lecture 11: Evaluation Foundations'),
    'd10': ('10-lecture-12-evaluation-decide-usability-testing-and-experiments', 'lecture-12-evaluation-decide-usability-testing-and-experiments', 'lecture-12-evaluation-decide-usability-testing-and-experiments', 'Lecture 12: Evaluation: DECIDE, Usability Testing and Experiments'),
    'd11': ('11-lecture-13-evaluation-inspections-heuristics-and-walkthroughs', 'lecture-13-evaluation-inspections-heuristics-and-walkthroughs', 'lecture-13-evaluation-inspections-heuristics-and-walkthroughs', 'Lecture 13: Evaluation: Inspections, Heuristics and Walkthroughs'),
}

# The real SE365 papers in exams/.
# SE365's exams/ holds per-lecture practice sets, not real past papers.
PAPERS = {
}


def past(paper, label, related=False):
    assert paper in PAPERS, paper
    return {'paper': paper, 'label': label, 'related': related}


def see(deck, n, label):
    assert deck in DECKS, deck
    return {'deck': deck, 'n': n, 'label': label}

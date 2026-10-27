"""Constructors for PHY205 annotated-slide content. The markup is the SE423 one (see se423_annotated/ch01_introduction.py)."""
from se423_annotated.common import mcq, scen, section, short, slide, tf, tip, trap, trick  # noqa: F401
from cs331_annotated.common import fig  # noqa: F401

# Every PHY205 deck, in course order: key -> (annotated slug, standalone file, slides folder, label).
DECKS = {
    'd01': ('01-electric-charge', 'electric-charge', 'phy205-chapter-21-electric-charge-halliday', 'Chapter 21: Electric Charge'),
    'd02': ('02-electric-fields', 'electric-fields', 'phy205-chapter-22-electric-fields-halliday', 'Chapter 22: Electric Fields'),
    'd03': ('03-gauss-law', 'gauss-law', 'phy205-chapter-23-gauss-law-halliday', "Chapter 23: Gauss' Law"),
    'd04': ('04-electric-potential', 'electric-potential', 'phy205-chapter-24-electric-potential-halliday', 'Chapter 24: Electric Potential'),
    'd05': ('05-capacitance', 'capacitance', 'phy205-chapter-25-capacitance-halliday', 'Chapter 25: Capacitance'),
    'd06': ('06-current-and-resistance', 'current-and-resistance', 'phy205-chapter-26-current-and-resistance-halliday', 'Chapter 26: Current and Resistance'),
    'd07': ('07-circuits', 'circuits', 'phy205-chapter-27-circuits-halliday', 'Chapter 27: Circuits'),
    'd08': ('08-magnetic-fields-and-induction', 'magnetic-fields-and-induction', 'phy205-chapters-28-29-30-magnetic-fields-and-induction-halliday', 'Chapters 28–30: Magnetic Fields and Induction'),
}

# The real PHY205 papers in exams/.
PAPERS = {
}


def past(paper, label, related=False):
    assert paper in PAPERS, paper
    return {'paper': paper, 'label': label, 'related': related}


def see(deck, n, label):
    assert deck in DECKS, deck
    return {'deck': deck, 'n': n, 'label': label}

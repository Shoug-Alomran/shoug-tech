"""Constructors for SCI101 annotated-slide content. The markup is the SE423 one (see se423_annotated/ch01_introduction.py)."""
from se423_annotated.common import mcq, scen, section, short, slide, tf, tip, trap, trick  # noqa: F401
from cs331_annotated.common import fig  # noqa: F401

# Every SCI101 deck, in course order: key -> (annotated slug, standalone file, slides folder, label).
DECKS = {
    'd01': ('01-patterns-of-motion-and-equilibrium', 'patterns-of-motion-and-equilibrium', 'sci101-chapter-1-patterns-of-motion-and-equilibrium', 'Chapter 1: Patterns of Motion and Equilibrium'),
    'd02': ('02-newtons-laws-of-motion', 'newtons-laws-of-motion', 'sci101-chapter-2-newtons-laws-of-motion', "Chapter 2: Newton's Laws of Motion"),
    'd03': ('03-momentum-and-energy', 'momentum-and-energy', 'sci101-chapter-3-momentum-and-energy', 'Chapter 3: Momentum and Energy'),
    'd04': ('04-gravity', 'gravity', 'sci101-chapter-4-gravity', 'Chapter 4: Gravity'),
    'd05': ('05-fluid-mechanics', 'fluid-mechanics', 'sci101-chapter-5-fluid-mechanics', 'Chapter 5: Fluid Mechanics'),
    'd06': ('06-thermal-energy-and-thermodynamics', 'thermal-energy-and-thermodynamics', 'sci101-chapter-6-thermal-energy-and-thermodynamics', 'Chapter 6: Thermal Energy and Thermodynamics'),
    'd07': ('07-heat-transfer-and-change-of-phase', 'heat-transfer-and-change-of-phase', 'sci101-chapter-7', 'Chapter 7: Heat Transfer and Change of Phase'),
    'd08': ('08-waves-and-sound', 'waves-and-sound', 'sci101-chapter-10', 'Chapter 10: Waves and Sound'),
    'd09': ('09-atoms-and-chemical-bonding', 'atoms-and-chemical-bonding', 'sci101-chapters-12-and-15', 'Chapters 12 and 15: Atoms, the Periodic Table and Chemical Bonding'),
}

# The real SCI101 papers in exams/.
PAPERS = {
}


def past(paper, label, related=False):
    assert paper in PAPERS, paper
    return {'paper': paper, 'label': label, 'related': related}


def see(deck, n, label):
    assert deck in DECKS, deck
    return {'deck': deck, 'n': n, 'label': label}

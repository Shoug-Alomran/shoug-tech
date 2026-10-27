"""Constructors for PHY105 annotated-slide content. The markup is the SE423 one (see se423_annotated/ch01_introduction.py)."""
from se423_annotated.common import mcq, scen, section, short, slide, tf, tip, trap, trick  # noqa: F401
from cs331_annotated.common import fig  # noqa: F401

# Every PHY105 deck, in course order: key -> (annotated slug, standalone file, slides folder, label).
DECKS = {
    'd01': ('01-introduction', 'introduction', 'chapter-1-introduction', 'Chapter 1: Introduction, Units and Measurement'),
    'd02': ('02-one-dimensional-kinematics', 'one-dimensional-kinematics', 'chapter-2-vectors', 'Chapter 2: One-Dimensional Kinematics'),
    'd03': ('03-vectors', 'vectors', 'chapter-3-motion-in-two-and-three-dimensions', 'Chapter 3: Vectors'),
    'd04': ('04-two-dimensional-and-projectile-motion', 'two-dimensional-and-projectile-motion', 'chapter-4-projectile-motion', 'Chapter 4: Two-Dimensional and Projectile Motion'),
    'd05': ('05-newtons-laws-of-motion', 'newtons-laws-of-motion', 'chapter-5-forces-and-motion', "Chapter 5: Newton's Laws of Motion"),
    'd06': ('06-friction-springs-and-circular-motion', 'friction-springs-and-circular-motion', 'chapter-6-force-and-motion-ii', 'Chapter 6: Friction, Springs and Circular Motion'),
    'd07': ('07-work-and-kinetic-energy', 'work-and-kinetic-energy', 'chapter-7-work-and-kinetic-energy', 'Chapter 7: Work and Kinetic Energy'),
    'd08': ('08-potential-energy-and-conservation', 'potential-energy-and-conservation', 'chapter-8-potential-energy', 'Chapter 8: Potential Energy and Conservation of Energy'),
    'd09': ('09-linear-momentum-and-collisions', 'linear-momentum-and-collisions', 'chapter-9-momentum', 'Chapter 9: Linear Momentum and Collisions'),
    'd10': ('10-temperature-and-heat', 'temperature-and-heat', 'chapter-16-temperature', 'Chapter 16: Temperature and Heat'),
}

# The real PHY105 papers in exams/.
PAPERS = {
}


def past(paper, label, related=False):
    assert paper in PAPERS, paper
    return {'paper': paper, 'label': label, 'related': related}


def see(deck, n, label):
    assert deck in DECKS, deck
    return {'deck': deck, 'n': n, 'label': label}

"""Constructors for SE401 annotated-slide content. The markup is the SE423 one (see se423_annotated/ch01_introduction.py)."""
from se423_annotated.common import mcq, scen, section, short, slide, tf, tip, trap, trick  # noqa: F401
from cs331_annotated.common import fig  # noqa: F401

# Every SE401 deck, in course order: key -> (annotated slug, standalone file, slides folder, label).
DECKS = {
    'd01': ('01-introduction', 'introduction', 'introduction', 'Introduction'),
    'd02': ('02-testing-throughout-the-sdlc', 'testing-throughout-the-sdlc', 'testing-throughout-the-sdlc', 'Testing throughout the SDLC'),
    'd03': ('03-software-quality', 'software-quality', 'software-quality', 'Software Quality'),
    'd04': ('04-quality', 'quality', 'quality', 'Quality'),
    'd05': ('05-test-cases', 'test-cases', 'test-cases', 'Test Cases'),
    'd06': ('06-test-design-techniques', 'test-design-techniques', 'test-design-techniques', 'Test Design Techniques'),
    'd07': ('07-black-box-testing-techniques', 'black-box-testing-techniques', 'black-box-testing-techniques', 'Black Box Testing Techniques'),
    'd08': ('08-white-box-testing', 'white-box-testing', 'white-box-testing', 'White Box Testing'),
    'd09': ('09-code-coverage', 'code-coverage', 'code-coverage', 'Code Coverage'),
    'd10': ('10-unit-testing-and-junit', 'unit-testing-and-junit', 'unit-testing-and-junit', 'Unit Testing and JUnit'),
    'd11': ('11-regression-testing', 'regression-testing', 'regression-testing', 'Regression Testing'),
    'd12': ('12-testing-metrics-and-tools', 'testing-metrics-and-tools', 'testing-metrics-and-tools', 'Testing Metrics and Tools'),
    'd13': ('13-advanced-topics', 'advanced-topics', 'advanced-topics', 'Advanced Topics'),
}

# The real SE401 papers in exams/.
PAPERS = {
}


def past(paper, label, related=False):
    assert paper in PAPERS, paper
    return {'paper': paper, 'label': label, 'related': related}


def see(deck, n, label):
    assert deck in DECKS, deck
    return {'deck': deck, 'n': n, 'label': label}

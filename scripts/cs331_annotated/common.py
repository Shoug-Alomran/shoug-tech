"""Constructors for CS331 annotated-slide content. The markup is the SE423 one (see se423_annotated/ch01_introduction.py)."""
from se423_annotated.common import mcq, scen, section, short, slide, tf, tip, trap, trick  # noqa: F401

# Every CS331 deck, in course order: key -> (annotated slug, standalone file, PDF folder, label).
# The folder is under slides/ unless it names another section. Chapters 8 and 10 have no clean
# upload yet, so they are read from the Set B highlighted copy in slides-with-notes/.
DECKS = {
    'ch1.1': ('01-introduction-part-1', 'introduction-part-1', 'chapter-1-data-communications-and-networking-part-1',
              'Ch 1 Part 1 · Introduction'),
    'ch1.2': ('02-introduction-part-2', 'introduction-part-2', 'chapter-1-data-communications-and-networking-part-2',
              'Ch 1 Part 2 · Introduction'),
    'ch2.1': ('03-physical-layer-part-1', 'physical-layer-part-1', 'physical-layer-part-1', 'Ch 2 Part 1 · Physical Layer'),
    'ch2.2': ('04-physical-layer-part-2', 'physical-layer-part-2', 'physical-layer-part-2', 'Ch 2 Part 2 · Physical Layer'),
    'ch3.1': ('05-data-link-layer-part-1', 'data-link-layer-part-1', 'data-link-layer-part-1', 'Ch 3 Part 1 · Data Link Layer'),
    'ch3.2': ('06-data-link-layer-part-2', 'data-link-layer-part-2', 'data-link-layer-part-2', 'Ch 3 Part 2 · Data Link Layer'),
    'ch4': ('07-local-area-networks', 'local-area-networks', 'data-link-layer-part-3', 'Ch 4 · Local Area Networks (Ethernet)'),
    'ch6': ('08-connecting-devices-and-vlans', 'connecting-devices-and-vlans', 'interconnecting-devices-and-vlans',
            'Ch 6 · Connecting Devices & Virtual LANs'),
    'ch7': ('09-network-layer-data-transfer', 'network-layer-data-transfer', 'network-layer-data-transfer-part-1',
            'Ch 7 · Network Layer Data Transfer'),
    'ch8': ('10-network-layer-routing', 'network-layer-routing', 'slides-with-notes/chapter-08-network-layer-routing-notes',
            'Ch 8 · Network Layer: Routing of Packets'),
    'ch9': ('11-transport-layer', 'transport-layer', 'transport-layer', 'Ch 9 · Transport Layer'),
    'ch10': ('12-application-layer', 'application-layer', 'slides-with-notes/chapter-10-application-layer-notes',
             'Ch 10 · Application Layer'),
}

# CS331 has no past papers on the site; the instructor's tutorials stand in for them.
PAPERS = {
    't1': ('Tutorial 1', 'extra-resources/tutorials/unsolved/tutorial-1'),
    't1s': ('Tutorial 1 solutions', 'extra-resources/tutorials/solved/tutorial-1-solutions.html'),
    't3': ('Tutorial 3 (solved)', 'extra-resources/tutorials/solved/physical-layer-activity'),
    't4': ('Tutorial 4', 'extra-resources/tutorials/unsolved/tutorial-4'),
}


def past(paper, label, related=False):
    assert paper in PAPERS, paper
    return {'paper': paper, 'label': label, 'related': related}


def see(deck, n, label):
    assert deck in DECKS, deck
    return {'deck': deck, 'n': n, 'label': label}


def fig(name, alt, cap='', big=False):
    return (name, alt, cap, big)

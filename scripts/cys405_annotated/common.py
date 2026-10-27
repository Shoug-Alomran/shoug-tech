"""Constructors for CYS405 annotated-slide content. The markup is the SE423 one (see se423_annotated/ch01_introduction.py)."""
from se423_annotated.common import mcq, scen, section, short, slide, tf, tip, trap, trick  # noqa: F401
from cs331_annotated.common import fig  # noqa: F401

# Every CYS405 deck, in course order: key -> (annotated slug, standalone file, slides folder, label).
DECKS = {
    'd01': ('01-introduction-to-ethical-hacking-and-penetration-testing', 'introduction-to-ethical-hacking-and-penetration-testing', 'chapter-1-introduction-to-ethical-hacking-and-penetration-testing', 'Chapter 1: Introduction to Ethical Hacking and Penetration Testing'),
    'd02': ('02-information-gathering-footprinting-and-reconnaissance', 'information-gathering-footprinting-and-reconnaissance', 'chapter-2-information-gathering-footprinting-and-reconnaissance', 'Chapter 2: Information Gathering, Footprinting and Reconnaissance'),
    'd03': ('03-scanning', 'scanning', 'chapter-3-scanning', 'Chapter 3: Scanning'),
    'd04': ('04-enumeration', 'enumeration', 'chapter-4-enumeration', 'Chapter 4: Enumeration'),
    'd05': ('05-vulnerability-analysis', 'vulnerability-analysis', 'chapter-5-vulnerability-analysis', 'Chapter 5: Vulnerability Analysis'),
    'd06': ('06-system-hacking', 'system-hacking', 'chapter-6-system-hacking', 'Chapter 6: System Hacking'),
    'd07': ('07-malware', 'malware', 'chapter-7-malware', 'Chapter 7: Malware'),
    'd08': ('08-web-and-database-hacking', 'web-and-database-hacking', 'chapter-8-web-and-database-hacking', 'Chapter 8: Web and Database Hacking'),
    'd09': ('09-social-engineering', 'social-engineering', 'chapter-9-social-engineering', 'Chapter 9: Social Engineering'),
    'd10': ('10-sniffing-and-dos-attacks', 'sniffing-and-dos-attacks', 'chapter-10-sniffing-and-dos-attacks', 'Chapter 10: Sniffing and DoS Attacks'),
    'd11': ('11-wireless-network-hacking', 'wireless-network-hacking', 'chapter-11-wireless-network-hacking', 'Chapter 11: Wireless Network Hacking'),
}

# The real CYS405 papers in exams/.
PAPERS = {
}


def past(paper, label, related=False):
    assert paper in PAPERS, paper
    return {'paper': paper, 'label': label, 'related': related}


def see(deck, n, label):
    assert deck in DECKS, deck
    return {'deck': deck, 'n': n, 'label': label}

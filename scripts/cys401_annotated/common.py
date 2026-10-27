"""Constructors for CYS401 annotated-slide content. The markup is the SE423 one (see se423_annotated/ch01_introduction.py)."""
from se423_annotated.common import mcq, scen, section, short, slide, tf, tip, trap, trick  # noqa: F401
from cs331_annotated.common import fig  # noqa: F401

# Every CYS401 deck, in course order: key -> (annotated slug, standalone file, slides folder, label).
DECKS = {
    'ch1': ('01-introduction-to-cybersecurity', 'introduction-to-cybersecurity', 'chapter-1-introduction-to-cybersecurity', 'Ch 1 · Introduction to Cybersecurity'),
    'ch2': ('02-security-foundations-and-principles', 'security-foundations-and-principles', 'chapter-2-security-foundations-and-principles',
            'Ch 2 · Security Foundations and Principles'),
    'ch3': ('03-threat-modeling', 'threat-modeling', 'chapter-3-threat-modeling', 'Ch 3 · Threat Modeling'),
    'ch4': ('04-protection-of-information-assets', 'protection-of-information-assets', 'chapter-4-protection-of-information-assets',
            'Ch 4 · Protection of Information Assets'),
    'ch5': ('05-cryptography', 'cryptography', 'chapter-5-cryptography', 'Ch 5 · Cryptography'),
    'ch6.1': ('06-asymmetric-cryptography-and-pki-part-1', 'asymmetric-cryptography-and-pki-part-1', 'chapter-6-1-asymmetric-cryptography-and-pki',
              'Ch 6.1 · Asymmetric Cryptography and PKI'),
    'ch6.2': ('07-asymmetric-cryptography-and-pki-part-2', 'asymmetric-cryptography-and-pki-part-2', 'chapter-6-2-asymmetric-cryptography-and-pki',
              'Ch 6.2 · Asymmetric Cryptography and PKI'),
    'ch7': ('08-security-design-models-and-capabilities', 'security-design-models-and-capabilities', 'chapter-7-security-design-models-and-capabilities',
            'Ch 7 · Security Design Models and Capabilities'),
    'ch8': ('09-security-vulnerabilities-threats-and-countermeasures', 'security-vulnerabilities-threats-and-countermeasures',
            'chapter-8-computer-architecture-security', 'Ch 8 · Security Vulnerabilities, Threats and Countermeasures'),
    'ch9': ('10-ics-and-scada-system-security', 'ics-and-scada-system-security', 'chapter-9-systems-architecture-security',
            'Ch 9 · ICS and SCADA System Security'),
    # The chapter-10 slides folder holds the Authentication and Access Control deck (the folder names are swapped).
    'ch10': ('11-authentication-and-access-control', 'authentication-and-access-control', 'chapter-10-ics-and-scada-system-security',
             'Ch 10 · Authentication and Access Control'),
}

# The real CYS401 papers in exams/.
PAPERS = {
    'q222': ('Quiz 1 · 222', '09-quiz-1-semester-222'),
    'f221a': ('Final 221 · A', '10-final-exam-221-version-a'),
    'f221b': ('Final 221 · B', '11-final-exam-221-version-b'),
    'm181': ('Major 181', '12-major-exam-semester-181'),
    'q232': ('Quiz 1 · 232', '13-quiz-1-semester-232'),
    'mA': ('Major A', '14-major-exam-a-term-unknown'),
    'mB': ('Major B', '15-major-exam-b-term-unknown'),
    'mC': ('Major C', '16-major-exam-c-term-unknown'),
}


def past(paper, label, related=False):
    assert paper in PAPERS, paper
    return {'paper': paper, 'label': label, 'related': related}


def see(deck, n, label):
    assert deck in DECKS, deck
    return {'deck': deck, 'n': n, 'label': label}

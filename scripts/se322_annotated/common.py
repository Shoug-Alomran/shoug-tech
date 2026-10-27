"""Constructors for SE322 annotated-slide content. The markup is the SE423 one (see se423_annotated/ch01_introduction.py)."""
from se423_annotated.common import mcq, scen, section, short, slide, tf, tip, trap, trick  # noqa: F401
from cs331_annotated.common import fig  # noqa: F401

# Every SE322 deck, in course order: key -> (annotated slug, standalone file, slides folder, label).
DECKS = {
    'ch1': ('01-introduction', 'introduction', 'chapter-1-introduction-to-software-design-and-architecture-extra',
            'Ch 1 · Introduction to Software Design and Architecture'),
    'ch2.1': ('02-software-architecture-lecture-1', 'software-architecture-lecture-1', 'chapter-2-software-architecture-lecture-1-extra',
              'Ch 2 L1 · Software Architecture'),
    'ch2.2': ('03-software-architecture-lecture-2', 'software-architecture-lecture-2', 'chapter-2-software-architecture-lecture-2-extra',
              'Ch 2 L2 · Software Architecture'),
    'ch2.3': ('04-software-architecture-lecture-3', 'software-architecture-lecture-3', 'chapter-2-software-architecture-lecture-3-extra',
              'Ch 2 L3 · Software Architecture'),
    'ch3.1': ('05-quality-attributes-lecture-1', 'quality-attributes-lecture-1', 'chapter-3-quality-attributes-lecture-1-extra',
              'Ch 3 L1 · Quality Attributes'),
    'ch3.2': ('06-quality-attributes-lecture-2', 'quality-attributes-lecture-2', 'chapter-3-quality-attributes-lecture-2-extra',
              'Ch 3 L2 · Quality Attributes'),
    'ch4.1': ('07-architecture-patterns-lecture-1', 'architecture-patterns-lecture-1', 'chapter-4-architecture-patterns-lecture-1-extra',
              'Ch 4 L1 · Architecture Patterns'),
    'ch4.2': ('08-architecture-patterns-lecture-2', 'architecture-patterns-lecture-2', 'chapter-4-architecture-patterns-lecture-2-extra',
              'Ch 4 L2 · Architecture Patterns'),
    'ch4.3': ('09-architecture-patterns-lecture-3', 'architecture-patterns-lecture-3', 'chapter-4-architecture-patterns-lecture-3-extra',
              'Ch 4 L3 · Architecture Patterns'),
    'ch5.1': ('10-principles-of-detailed-design-lecture-1', 'principles-of-detailed-design-lecture-1', 'chapter-5-principles-of-detailed-design-lecture-1',
              'Ch 5 L1 · Principles of Detailed Design'),
    'ch5.2': ('11-principles-of-detailed-design-lecture-2', 'principles-of-detailed-design-lecture-2', 'chapter-5-principles-of-detailed-design-lecture-2-extra',
              'Ch 5 L2 · Principles of Detailed Design'),
    'ch5.3': ('12-principles-of-detailed-design-lecture-3', 'principles-of-detailed-design-lecture-3', 'chapter-5-principles-of-detailed-design-lecture-3-extra',
              'Ch 5 L3 · Principles of Detailed Design'),
    'ch6.1': ('13-creational-design-patterns-lecture-1', 'creational-design-patterns-lecture-1', 'chapter-6-creational-design-patterns-abstract-factory',
              'Ch 6 L1 · Creational Design Patterns'),
    'ch6.2': ('14-creational-design-patterns-lecture-2', 'creational-design-patterns-lecture-2', 'chapter-6-creational-design-patterns-ii',
              'Ch 6 L2 · Creational Design Patterns'),
    'ch6.3': ('15-creational-design-patterns-lecture-3', 'creational-design-patterns-lecture-3', 'chapter-6-creational-design-patterns-iii',
              'Ch 6 L3 · Creational Design Patterns'),
    'ch7.1': ('16-structural-design-patterns', 'structural-design-patterns', 'chapter-7-structural-design-patterns-lecture-1',
              'Ch 7 L1 · Structural Design Patterns'),
    'ch7.2': ('17-behavioral-design-patterns', 'behavioral-design-patterns', 'chapter-7-behavioral-design-patterns-lecture-2',
              'Ch 7 L2 · Behavioral Design Patterns'),
    'ch8': ('18-architecture-evaluation', 'architecture-evaluation', 'chapter-8-architecture-evaluation', 'Ch 8 · Architecture Evaluation'),
    'ch9': ('19-documentation', 'documentation', 'chapter-9-documentation', 'Ch 9 · Documentation'),
}

# The real SE322 papers in exams/.
PAPERS = {
    'm252': ('Midterm 252', '10-midterm-252'),
    'q261': ('Quiz 1 · 261', '11-quiz-1-261'),
    'm261': ('Midterm 261', '12-midterm-261'),
    'f252': ('Final 252', '13-final-252'),
}


def past(paper, label, related=False):
    assert paper in PAPERS, paper
    return {'paper': paper, 'label': label, 'related': related}


# Exam questions for decks written in the page schema (see ch05_2_page.py): `asked` only for a question that is
# really on one of the PAPERS (worded as on the paper), `likely` for everything else.
def _question(kind, q, a, opts, tf, why):
    d = {'kind': kind, 'q': q, 'why': why}
    if opts is not None:
        d.update(opts=opts, a=a)
    elif tf is not None:
        d['tf'] = tf
    else:
        d['a'] = a
    return d


def asked(paper, where, q, a=None, opts=None, tf=None, why=''):
    title, folder = PAPERS[paper]
    d = _question('past', q, a, opts, tf, why)
    d.update(ref='%s · %s' % (title, where), href='/academics/software-engineering/se322/exams/%s/' % folder)
    return d


def likely(q, a=None, opts=None, tf=None, why=''):
    return _question('predict', q, a, opts, tf, why)


def see(deck, n, label):
    assert deck in DECKS, deck
    return {'deck': deck, 'n': n, 'label': label}

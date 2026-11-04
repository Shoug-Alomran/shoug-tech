"""Constructors for SE423 annotated-slide content. See ch01_introduction.py for the markup."""

# Every SE423 deck, in course order: key -> (annotated slug, standalone file, slides folder, label).
DECKS = {
    'ch1': ('01-introduction', 'introduction', 'chapter-1', 'Ch 1 · Introduction'),
    'ch1.2': ('02-performance-domains', 'performance-domains', 'chapter-1.2', 'Ch 1.2 · Project Performance Domains'),
    'ch1.3': ('03-tailoring', 'tailoring', 'chapter-1.3', 'Ch 1.3 · Tailoring, Models, Methods & Artifacts'),
    'ch2': ('04-organizational-context', 'organizational-context', 'chapter-2', 'Ch 2 · The Organizational Context'),
    'ch3': ('05-team', 'team', 'chapter-3', 'Ch 3 · Team'),
    'ch4': ('06-development-approach', 'development-approach', 'chapter-4', 'Ch 4 · Development Approach'),
    'ch5': ('07-risk-management', 'risk-management', 'chapter-5', 'Ch 5 · Risk Management'),
    'ch6': ('08-estimation', 'estimation', 'chapter-6', 'Ch 6 · Estimation'),
    'ch6.2': ('09-scheduling-and-tracking', 'scheduling-and-tracking', 'chapter-6.2', 'Ch 6.2 · Scheduling and Tracking'),
    'ch7': ('10-quality', 'quality', 'chapter-7', 'Ch 7 · Quality'),
    'ch8': ('11-stakeholders', 'stakeholders', 'chapter-8', 'Ch 8 · Stakeholders'),
    'ch9': ('12-change-management', 'change-management', 'chapter-9', 'Ch 9 · Change Management'),
}

# The real SE423 papers in exams/ (built by scripts/build_se423_past_papers.py).
PAPERS = {
    'f242': ('Final 242', '14-final-242'),
    'm251v1': ('Midterm 251 · V1', '15-midterm-251-version-1'),
    'm251v2': ('Midterm 251 · V2', '16-midterm-251-version-2'),
    'f251': ('Final 251', '17-final-251'),
}


def slide(n, title, body=None, *, kind='content', sub=None, cols=None, card=None, fig=None, chart=None,
          notes=(), prof=(), tips=(), seen=(), exam=(), past=(), weight=1):
    return {'n': n, 'title': title, 'kind': kind, 'sub': sub, 'body': body or [], 'cols': cols, 'card': card,
            'fig': fig, 'chart': chart, 'notes': list(notes), 'prof': list(prof), 'tips': list(tips),
            'seen': list(seen), 'exam': list(exam), 'past': list(past), 'weight': weight}


def section(n, title):
    return slide(n, title, kind='section')


def mcq(q, opts, a, why=''):
    return {'type': 'mcq', 'q': q, 'opts': opts, 'a': a, 'why': why}


def tf(q, a, why=''):
    return {'type': 'tf', 'q': q, 'a': a, 'why': why}


def scen(q, a):
    return {'type': 'scenario', 'q': q, 'a': a}


def short(q, a):
    return {'type': 'short', 'q': q, 'a': a}


def past(paper, label, related=False):
    assert paper in PAPERS, paper
    return {'paper': paper, 'label': label, 'related': related}


def see(deck, n, label):
    assert deck in DECKS, deck
    return {'deck': deck, 'n': n, 'label': label}


def tip(text):
    return ('tip', text)


def trick(text):
    return ('trick', text)


def trap(text):
    return ('trap', text)


# Exam questions for decks written in the page schema (see se322_annotated/ch05_2_page.py): `asked` only for a
# question that is really on a past paper (worded as on the paper), `likely` for everything else.
# 'm261' is the instructor's own 2026 midterm, kept in the midterm cheat sheet rather than in exams/.
ASKED_ON = dict({k: (t, '/academics/software-engineering/se423/exams/%s/' % f) for k, (t, f) in PAPERS.items()},
                m261=('Midterm 261', '/academics/software-engineering/se423/extra-resources/midterm-cheat-sheet/'))


def _question(kind, q, a, opts, tf, why, wrong=None):
    d = {'kind': kind, 'q': q, 'why': why}
    if wrong:
        d['wrong'] = wrong
    if opts is not None:
        d.update(opts=opts, a=a)
    elif tf is not None:
        d['tf'] = tf
    else:
        d['a'] = a
    return d


def asked(paper, where, q, a=None, opts=None, tf=None, why='', wrong=None):
    title, href = ASKED_ON[paper]
    d = _question('past', q, a, opts, tf, why, wrong)
    d.update(ref='%s · %s' % (title, where), href=href)
    return d


def likely(q, a=None, opts=None, tf=None, why='', wrong=None):
    return _question('predict', q, a, opts, tf, why, wrong)


def pick(q, right, why, *wrongs):
    """A predicted MCQ: the right answer and why, then (wrong option, why it is wrong) pairs. Options are shuffled when built."""
    return likely(q, a=0, opts=[right] + [w[0] for w in wrongs], why=why, wrong={i: w[1] for i, w in enumerate(wrongs, 1)})


def truth(q, value, why, wrong):
    """A predicted true/false question: why the answer is right, and what to fix if the other one was picked."""
    return likely(q, tf=value, why=why, wrong=wrong)


def apply_notes(slides, notes):
    """Swap in rewritten notes. A list keeps its slide's length and order (highlights link to note numbers); None keeps that note."""
    for n, new in notes.items():
        old = slides[n]['notes']
        if len(new) != len(old):
            raise SystemExit('notes for slide %d: %d given, %d expected' % (n, len(new), len(old)))
        slides[n]['notes'] = [o if x is None else x for x, o in zip(new, old)]

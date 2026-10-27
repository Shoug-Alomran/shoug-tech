"""Constructors for ENG101 annotated-slide content. The markup is the SE423 one (see se423_annotated/ch01_introduction.py)."""
from se423_annotated.common import mcq, scen, section, short, slide, tf, tip, trap, trick  # noqa: F401
from cs331_annotated.common import fig  # noqa: F401

# Every ENG101 deck, in course order: key -> (annotated slug, standalone file, slides folder, label).
DECKS = {
    'd01': ('01-thesis-statement-guide', 'thesis-statement-guide', 'thesis-statement-guide', 'Thesis Statements: A Guide'),
    'd02': ('02-thesis-statement-practice', 'thesis-statement-practice', 'thesis-statement-practice', 'Writing Thesis Statements: Practice'),
    'd03': ('03-thesis-statement-worksheet', 'thesis-statement-worksheet', 'thesis-statement-worksheet', 'Thesis Statement Worksheet'),
    'd04': ('04-transition-signals', 'transition-signals', 'transition-signals', 'Transition Signals'),
    'd05': ('05-transitions-punctuation', 'transitions-punctuation', 'transitions-punctuation', 'Transition Words and Their Punctuation'),
    'd06': ('06-punctuation-for-connecting-words', 'punctuation-for-connecting-words', 'punctuation-for-connecting-words', 'Punctuation for Connecting Words'),
    'd07': ('07-commas-guide', 'commas-guide', 'commas-guide', 'Using Commas'),
    'd08': ('08-process-analysis-essay', 'process-analysis-essay', 'process-analysis-essay', 'The Process Analysis Essay'),
    'd09': ('09-classification-essay', 'classification-essay', 'classification-essay', 'The Classification Essay'),
    'd10': ('10-cause-effect-essay-notes', 'cause-effect-essay-notes', 'cause-effect-essay-notes', 'The Cause and Effect Essay'),
    'd11': ('11-compare-contrast-overview', 'compare-contrast-overview', 'compare-contrast-overview', 'Writing a Compare and Contrast Essay'),
    'd12': ('12-compare-contrast-keywords', 'compare-contrast-keywords', 'compare-contrast-keywords', 'Compare and Contrast Keywords'),
    'd13': ('13-compare-contrast-essay', 'compare-contrast-essay', 'compare-contrast-essay', 'Compare and Contrast Essay Structures'),
    'd14': ('14-compare-contrast-essay-assignment', 'compare-contrast-essay-assignment', 'compare-contrast-essay-assignment', 'Compare and Contrast Essay Assignment'),
    'd15': ('15-argumentative-essay', 'argumentative-essay', 'argumentative-essay', 'The Argumentative Essay'),
}

# The real ENG101 papers in exams/.
PAPERS = {
}


def past(paper, label, related=False):
    assert paper in PAPERS, paper
    return {'paper': paper, 'label': label, 'related': related}


def see(deck, n, label):
    assert deck in DECKS, deck
    return {'deck': deck, 'n': n, 'label': label}

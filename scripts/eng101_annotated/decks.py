"""ENG101 annotated slides — the Intensive Writing handouts and slide decks, from thesis statements to essay types.

Most items are one- or two-page handouts and worksheets, so every page is shown as the original image
(whole=True) and the notes, tips and practice questions sit beside it. Each item is a namespace class built
by handout(); see cs331_annotated/ch01_1_introduction.py for the ANN keys."""
from .common import DECKS, mcq, see, short, tf, tip, trap, trick


def handout(key, count, lede, ann):
    slug, file, folder, label = DECKS[key]
    return type(key, (), {
        'AUTO_SLIDES': True,
        'DECK': {'key': key, 'slug': slug, 'file': file, 'title': label, 'chapter': 'ENG101',
                 'pdf': '/academics/other-courses/english/eng101/slides/%s/' % folder, 'lede': lede},
        'ANN': {n: dict(ann.get(n, {}), whole=True) for n in range(1, count + 1)},
    })


THESIS = 'Thesis = topic + controlling idea (your position), usually with the main points: one clear, specific, arguable sentence at the end of the introduction.'

thesis_guide = handout('d01', 1, 'What a thesis statement is, where it goes, and how to make it specific and arguable.', {
    1: dict(notes=[THESIS], tips=[tip(THESIS)],
            exam=[mcq('Which is the strongest thesis statement?', ['Online classes save students time, money and travel, but they demand more self-discipline.', 'This essay is about online classes.', 'Online classes exist.', 'Do you like online classes?'], 0, ''),
                  tf('A thesis statement can be a question.', False, 'It is a statement of your position.')], weight=3),
})

thesis_practice = handout('d02', 10, 'Practice turning topics into thesis statements: narrowing the topic, adding a controlling idea and listing sub-points.', {
    1: dict(notes=['A topic is not a thesis: "Smartphones" is a topic; "Smartphones help students organize their time, find information and stay in touch" is a thesis.'],
            tips=[trap('Announcements ("In this essay I will…") and plain facts are not thesis statements.')]),
    3: dict(notes=['Narrow broad topics until they can be covered in one essay.'],
            exam=[short('Turn the topic "exercise" into a thesis statement with three points.', 'For example: "Regular exercise improves students’ health, lowers stress and helps them concentrate in class."')], weight=3),
})

thesis_worksheet = handout('d03', 6, 'Topics vs. thesis statements, creating a thesis, including sub-topics, and using narrow statements.', {
    2: dict(notes=['Topic: what the essay is about. Thesis: what you say about it.']),
    4: dict(notes=['Including sub-topics in the thesis previews the body paragraphs in the same order.']),
    5: dict(notes=['Narrow statements are more effective than broad ones.']),
})

transitions = handout('d04', 2, 'Transition signals grouped by function: time, addition, contrast, cause and effect, examples, conclusion.', {
    1: dict(notes=['Transitions link ideas: addition (furthermore, in addition), contrast (however, on the other hand), cause/effect (therefore, as a result), example (for example), time (first, then, finally), conclusion (in conclusion).'],
            exam=[mcq('Which transition shows CONTRAST?', ['However', 'Furthermore', 'Therefore', 'For example'], 0, ''),
                  mcq('Which transition shows a RESULT?', ['Consequently', 'Moreover', 'Similarly', 'For instance'], 0, '')], weight=3),
})

transitions_punct = handout('d05', 3, 'Transition words vs. coordinating and subordinating conjunctions and the common punctuation structures for each.', {
    2: dict(notes=['Coordinating conjunctions (FANBOYS: for, and, nor, but, or, yet, so): Clause, FANBOYS clause.']),
    3: dict(notes=['Conjunctive adverbs: Clause; however, clause. (semicolon before, comma after). Subordinators (because, although): Although clause, clause. / Clause because clause.'],
            tips=[trick('However/therefore join two sentences with a semicolon, never just a comma.')],
            exam=[mcq('Which is punctuated correctly?', ['It rained; however, we played.', 'It rained, however we played.', 'It rained however, we played.', 'It rained; however we played.'], 0, '')], weight=3),
})

connecting = handout('d06', 15, 'Punctuating sentences joined by coordinators, conjunctive adverbs and subordinators, with exercises.', {
    1: dict(notes=['Three ways to join independent clauses: comma + FANBOYS, semicolon (+ conjunctive adverb + comma), or a subordinator making one clause dependent.']),
    5: dict(notes=['A comma alone between two independent clauses is a comma splice; no punctuation at all is a run-on (fused) sentence.'],
            exam=[mcq('"I studied hard, I passed the exam." is a:', ['Comma splice', 'Correct compound sentence', 'Fragment', 'Complex sentence'], 0, '')], weight=3),
})

commas = handout('d07', 2, 'Main comma rules: after introductory elements, between items in a series, before coordinators joining clauses, around non-essential information, and with transitions.', {
    1: dict(notes=['Use commas: after introductory words/phrases, in a series, before FANBOYS joining two clauses, around non-essential clauses and appositives.'],
            exam=[mcq('Which uses commas correctly?', ['After class, we went to the library.', 'After class we, went to the library.', 'After, class we went to the library.', 'After class we went, to the library.'], 0, '')], weight=3),
})

process = handout('d08', 3, 'The process analysis essay: directional vs. informational process, organizing steps in chronological order, and transitions of time.', {
    1: dict(notes=['Process analysis explains how to do something (directional) or how something happens (informational), step by step in chronological order.'],
            exam=[mcq('An essay explaining how a volcano erupts is a(n):', ['Informational process essay', 'Directional process essay', 'Classification essay', 'Argumentative essay'], 0, '')], weight=3),
})

classification = handout('d09', 1, 'The classification essay: sorting a topic into categories using one consistent principle.', {
    1: dict(notes=['Classification sorts items into groups by ONE principle (e.g. types of students by study habits); categories should not overlap.'],
            tips=[trap('Mixing principles (e.g. "lazy, hard-working and tall students") breaks a classification.')], weight=3),
})

cause_effect = handout('d10', 3, 'Writing a cause and effect essay: focusing on causes, effects or both, block vs. chain organization, and cause/effect signal words.', {
    1: dict(notes=['Focus on causes OR effects (or both); organize in block (all causes then all effects) or chain (cause → effect → effect…) order. Signals: because, due to, as a result, consequently.'],
            exam=[mcq('An essay on why students drop out of university focuses on:', ['Causes', 'Effects', 'Comparison', 'Classification'], 0, '')], weight=3),
})

cc_overview = handout('d11', 5, 'Writing a compare/contrast essay: choosing subjects with a basis for comparison, brainstorming with a Venn diagram, and organization.', {
    3: dict(notes=['Brainstorm similarities and differences with a Venn diagram or a T-chart.']),
    4: dict(notes=['Block method: all about subject A, then all about B. Point-by-point method: each point compares A and B together.'],
            tips=[trick('Block = A then B. Point-by-point = A/B, A/B, A/B.')],
            exam=[mcq('Discussing cost for both phones, then battery for both, then cameras for both is the:', ['Point-by-point method', 'Block method', 'Chain method', 'Chronological method'], 0, '')], weight=3),
})

cc_keywords = handout('d12', 1, 'Signal words for comparison (similarly, likewise, both) and contrast (however, whereas, unlike, on the other hand).', {
    1: dict(notes=['Comparison: similarly, likewise, both, also, just as. Contrast: however, whereas, while, unlike, on the other hand, in contrast.'],
            exam=[mcq('Which word signals COMPARISON?', ['Likewise', 'Whereas', 'Unlike', 'However'], 0, '')], weight=3),
})

cc_essay = handout('d13', 6, 'Compare and contrast essay structures, with outlines of the block and point-by-point patterns.', {
    1: dict(notes=['Introduction with a thesis naming both subjects and the points of comparison; body paragraphs in block or point-by-point order; conclusion that sums up the significance.']),
})

cc_assignment = handout('d14', 1, 'The compare and contrast essay assignment and its requirements.', {
    1: dict(notes=['Read the requirements for length, structure, number of points and sources before you plan the essay.']),
})

argumentative = handout('d15', 2, 'The argumentative essay: claim, reasons and evidence, counter-arguments and refutation, and its historical background.', {
    1: dict(notes=['Argumentative essay: a debatable claim supported by reasons and evidence; acknowledge the opposing view (counter-argument) and refute it.'],
            tips=[tip('Structure: introduction + thesis (claim) → body paragraphs with reasons and evidence → counter-argument and refutation → conclusion.')],
            exam=[mcq('Answering the opposing side’s strongest point in your essay is called:', ['Refutation', 'Thesis', 'Hook', 'Transition'], 0, '')], weight=3),
})

DECKS_HERE = [thesis_guide, thesis_practice, thesis_worksheet, transitions, transitions_punct, connecting, commas, process, classification,
              cause_effect, cc_overview, cc_keywords, cc_essay, cc_assignment, argumentative]

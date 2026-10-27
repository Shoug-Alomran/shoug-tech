"""SE322 annotated slides — Chapter 5, Lecture 1: overview and key tasks of detailed design.
See ch01_introduction.py for AUTO_SLIDES and the ANN keys."""
from .common import mcq, past, scen, see, short, tf, tip, trap, trick

AUTO_SLIDES = 'all'
OVERVIEW = 'This chapter shows how to turn architecture into implementation-ready component designs. Across three lectures it covers the five detailed-design tasks, object-oriented component structure and behavior, all five SOLID principles, design models, and practical rules for keeping designs clear, changeable, and testable.'

DECK = {
    'key': 'ch5.1',
    'slug': '10-principles-of-detailed-design-lecture-1',
    'file': 'principles-of-detailed-design-lecture-1',
    'title': 'Principles of Detailed Design: Overview and Key Tasks',
    'chapter': 'Chapter 5 · Lecture 1',
    'page': 'ch05_1_page',  # notes, highlights and exam questions in the page schema
    'pdf': '/academics/software-engineering/se322/slides/chapter-5-principles-of-detailed-design-lecture-1/',
    'lede': ('What detailed design is, where it sits (the bridge between architecture and code), and its five key '
             'tasks: understand architecture and requirements, create designs, evaluate them with technical '
             'reviews, document them in the SDD, and manage implementation through design synchronicity.'),
}

TASKS = 'Detailed design key tasks: understand architecture & requirements → create detailed designs → evaluate (technical reviews) → document (SDD) → manage implementation (synchronicity).'

ANN = {
    1: dict(kind='title', title='Principles of Detailed Design', body=[], sub='SE322 · Chapter 5, Lecture 1', tips=[tip(TASKS)]),
    2: dict(notes=['Detailed design is the refinement from architecture to implementable components. This lecture follows its five tasks: understand requirements and architecture, create component designs, evaluate them, document them, and keep implementation synchronized.']),
    3: dict(notes=['The lifecycle moves from requirements to high-level architecture, then detailed design, then construction. Each step adds precision while preserving decisions made earlier.']),
    4: dict(notes=['Detailed design = refining and expanding the preliminary (architectural) design so it is ready to code: components, interfaces, internal structure and behaviour.'],
            seen=[see('ch1', 28, 'Detailed design first introduced')], exam=[mcq('What is the primary focus of detailed design?', ['Refining components until their structure and behavior are ready to implement', 'Defining only system-wide quality attributes', 'Discovering stakeholder needs', 'Testing completed source code'], 0, 'Final 252, Q1.')], past=[past('f252', 'Q1 MCQ · primary focus of detailed design')]),
    5: dict(hl=['architecture', 'construction', 'requirements', 'full understanding',
                'detailed design', 'design and code', 'object-oriented', 'programming languages',
                'software quality control'],
            notes=['Architecture bridges requirements and design; detailed design bridges design and CODE. Designers must understand both architecture and construction.'],
            exam=[mcq('Detailed design is the bridge between:', ['Design and code', 'Requirements and architecture', 'Testing and deployment', 'Users and managers'], 0, '')], weight=2),
    6: dict(notes=['Designer’s mental model: from requirements + architecture, design down to code; from code, you should be able to rebuild the design (forward and reverse).']),
    7: dict(notes=['The five tasks are understanding architecture and requirements, creating designs, evaluating designs, documenting them, and monitoring implementation. They form a feedback loop: review and coding discoveries can trigger clarification or redesign.'], tips=[tip(TASKS)],
            exam=[mcq('Which is NOT a key task of detailed design?', ['Eliciting requirements from stakeholders', 'Creating detailed designs', 'Evaluating detailed designs', 'Documenting detailed designs'], 0, '')], weight=3),
    8: dict(notes=['Detailed designers focus on the requirements of their ASSIGNED components (architecture components like SensorManager go to teams).']),
    9: dict(hl=['components', 'Interface', 'Graphical User Interface', 'Internal Component Design', 'Data Design'],
            notes=['Creating designs covers interface design (internal and external), GUI design, internal component design (structure and behaviour), and data design.']),
    10: dict(hl=['Technical Reviews', 'Send a review notice', 'technical expert', 'stakeholders',
                 'quality assurance', 'testing team', 'functional and non-functional requirements', 'action items'],
             notes=['Evaluate with **technical reviews**: send notices early, include a technical expert, stakeholders and QA/testing, focus on functional and non-functional requirements, record action items.'],
             exam=[mcq('The most popular technique for evaluating detailed designs is:', ['Technical reviews', 'Load testing', 'Pair programming', 'Prototyping only'], 0, '')], weight=3),
    11: dict(notes=['Documentation goes in the **Software Design Document (SDD)** / software design description, used by programmers, testers and maintainers.'],
             exam=[mcq('Detailed designs are mainly documented in the:', ['Software Design Document (SDD)', 'Software Requirements Specification', 'Test plan', 'Project charter'], 0, '')], weight=2),
    12: dict(notes=['The SDD table of contents is a navigation aid for component designs, interfaces, data, behavior, constraints, and rationale. Tailor sections to the system, but ensure readers can find the information they need.']),
    13: dict(notes=['Managing implementation = keeping detailed design synchronicity: code follows design, design follows architecture. Low synchronicity signals a flaw and project risk.'],
             seen=[see('ch2.1', 28, 'Design synchronicity')]),
    14: dict(notes=['Review the lecture as a workflow: understand context, produce a precise but not over-constrained design, review it, record the decisions, and check that implementation remains aligned.'], tips=[tip(TASKS)]),
}

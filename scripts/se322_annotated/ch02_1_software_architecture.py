"""SE322 annotated slides — Chapter 2, Lecture 1: Software Architecture (fundamentals and key tasks).
See ch01_introduction.py for AUTO_SLIDES and the ANN keys."""
from .common import mcq, past, scen, see, short, tf, tip, trap, trick

AUTO_SLIDES = 'all'
OVERVIEW = 'This chapter develops software architecture from requirements through design decisions and stakeholder views. It connects requirements engineering to architecture, examines quality-driven decisions, and uses the 4+1 model to describe logical structure, runtime behavior, development, deployment, and scenarios.'

DECK = {
    'key': 'ch2.1',
    'slug': '02-software-architecture-lecture-1',
    'file': 'software-architecture-lecture-1',
    'title': 'Software Architecture: Fundamentals and Key Tasks',
    'chapter': 'Chapter 2 · Lecture 1',
    'page': 'ch02_1_page',  # notes, highlights and exam questions in the page schema
    'pdf': '/academics/software-engineering/se322/slides/chapter-2-software-architecture-lecture-1-extra/',
    'lede': ('What software architecture is (and is not), the formal definition and its five parts, and the key '
             'tasks of architectural design: stakeholder concerns, quality attributes and tactics, views, styles '
             'and patterns, components and interfaces, evaluation, and design synchronicity. Midterm 252, '
             'Midterm 261 and Final 252 all asked about the definition or the key tasks.'),
}

TASKS = 'Key tasks: identify stakeholder concerns · identify views · identify styles and patterns · identify major components and interfaces · evaluate and validate · introduce policies for design synchronicity.'

ANN = {
    1: dict(kind='title', title='Software Architecture', body=[], sub='SE322 · Chapter 2, Lecture 1',
            notes=['The lecture defines software architecture, unpacks the pieces of that definition, and introduces the architect’s main tasks. The sequence moves from what architecture is to the decisions and views used to make it useful.']),
    2: dict(notes=['The lecture has two halves: fundamentals explain what architecture is and why it matters; key tasks explain how architects identify concerns, select views and patterns, define components, and evaluate the result.'], tips=[tip(TASKS)]),
    3: dict(notes=['Architecture is the important parts of a system and the rules for how they communicate. A box diagram helps only if it clarifies responsibilities and connections enough for teams to make consistent decisions.'],
            past=[past('m252', 'Q1 MCQ · software architecture is NOT about')],
            exam=[mcq('Software architecture is NOT about:', ['Algorithms and data structures', 'The parts of the system', 'How the parts fit together', 'Communication between parts'], 0, 'Midterm 252, Q1.')],
            weight=3),
    4: dict(notes=['High-level structures of a system, the discipline of creating them, and their documentation.',
                   'Three dimensions: structure, communication (behaviour), non-functional requirements. Focus on what would be hard to change later.'],
            exam=[mcq('Which is NOT one of the three primary dimensions architecture captures?', ['Source code style', 'Structure', 'Communication (behaviour)', 'Non-functional requirements'], 0, '')], weight=2),
    5: dict(hl=['foundational software design activity', 'collection of design elements', 'major components of the system'],
            notes=['Formal definition: (1) the FOUNDATIONAL design activity that translates functional and non-functional requirements into design elements describing the structure and behaviour of the MAJOR components, their quality and relationships, to SUPPORT detailed design and construction; (2) the PRODUCT of that activity.'],
            tips=[trick('Five parts to explain: foundational · translates requirements · collection of design elements · major components with quality · supports detailed design.')],
            past=[past('f252', 'Q2 · define architecture and explain three parts'), past('m252', 'Q1 MCQ · why architecture is foundational', related=True)],
            exam=[short('Define software architecture formally and explain three parts of the definition. (Final 252)',
                        'Architecture is the foundational design activity that evaluates and translates functional and non-functional requirements into a collection of design elements describing the structure and behaviour of the major components, their quality and relationships, so as to support detailed design and construction; it is also the product of that activity. Foundational: it is not optional, it is where designing for quality starts. Translates requirements: textual requirements become graphical design elements that can be traced. Collection of design elements: no single diagram is enough, so many views are needed.')],
            weight=3),
    6: dict(notes=['Architecture = big picture (frontend, backend, DB, payment). Detailed design = inside each part (ShoppingCart class methods).']),
    7: dict(notes=['Architecture asks which components communicate; detailed design asks what happens inside one component. Keeping these questions separate stops high-level diagrams from becoming code blueprints.']),
    8: dict(notes=['Detailed design describes the internals of components: classes, methods, data structures, and object-level collaborations. It refines architectural boundaries rather than replacing them.']),
    9: dict(notes=['Five things to unpack from the definition: foundational, transforms requirements, collection of design elements, major components with quality, support for detailed design.']),
    10: dict(notes=['Foundational: architecture is a major, not optional, activity; forward engineering, not reverse engineering. Designing for quality starts here.'],
             past=[past('m252', 'Q1 MCQ · architecture as a foundational activity')],
             exam=[mcq('Why is software architecture called a foundational design activity?', ['It is where designing for quality begins and it is not optional', 'It is done after coding', 'It only concerns the user interface', 'It replaces detailed design'], 0, 'Midterm 252, Q1.')],
             weight=3),
    11: dict(notes=['Architecture turns textual requirements into graphical design elements, which makes requirements traceable. Architects must be good at requirements engineering.']),
    12: dict(notes=['A view is a focused answer to a stakeholder’s question, not a different system. Developers may need a class view while operators need a deployment view; together they describe one architecture without one crowded diagram.'],
             past=[past('m252', 'Q1 MCQ · why multiple views are needed')],
             exam=[mcq('Why are multiple architectural views needed?', ['No single diagram can capture all structures and quality concerns', 'To make the documentation longer', 'Because UML forbids combining diagrams', 'To replace detailed design'], 0, 'Midterm 252, Q1.')],
             weight=3),
    13: dict(notes=['Architecture specifies major components AND the quality (e.g. performance, availability) each must provide.']),
    14: dict(notes=['Quality requirements identified during architecture flow down into component-level decisions and eventually implementation. For example, an availability target may require redundancy in the architecture and recovery behavior in component designs.']),
    15: dict(notes=['Architecture must support detailed design and construction; architecture alone cannot guarantee quality.']),
    16: dict(notes=['Wrap-up: architecture is an early stage linking specification and design: major components, their communication and required quality.']),
    17: dict(notes=['The six key tasks of architectural design.'], tips=[tip(TASKS)],
             past=[past('f252', 'Q2 · list five key tasks'), past('m261', 'MCQ · pick the four key tasks'), past('m252', 'Q1 MCQ · which task is architectural', related=True)],
             exam=[short('List five key tasks in architectural design. (Final 252)', 'Identify stakeholders’ concerns; identify appropriate architectural views; identify architectural styles and patterns; identify the major components and interfaces; evaluate and validate the architecture; introduce policies for design synchronicity.'),
                   mcq('Which is NOT a key task of architectural design?', ['Writing unit tests for each class', 'Identifying stakeholder concerns', 'Identifying views, styles and patterns', 'Introducing policies for design synchronicity'], 0, '')],
             weight=3),
    18: dict(notes=['Stakeholders: anyone with a direct or indirect stake (engineers, managers, customers, testers, QA, configuration management). A concern = high-level information about desired characteristics.']),
    19: dict(notes=['Concerns must be elicited before design starts. University app: students want schedules, professors want grade entry, admins want reports and security.']),
    20: dict(notes=['Quality attributes stakeholders care about: usability, availability, performance, security, modifiability, testability…'],
             seen=[see('ch3.1', 3, 'Quality attributes in depth')]),
    21: dict(notes=['“Make the system secure” does not tell developers what to build. A tactic translates that goal into a design decision—such as authentication or access control—that can be checked against concrete threats.']),
    22: dict(hl=['tactic'],
             notes=['**Tactic** = a design decision that influences the response of a quality attribute. Architects choose tactics for each quality.'],
             past=[past('q261', 'fill-in · a design decision for a quality attribute is a tactic')],
             exam=[mcq('A design decision intended to control the response of a quality attribute is called a(n):', ['Architectural tactic', 'Architectural view', 'Stakeholder concern', 'Design pattern'], 0, 'Quiz 1 261.')],
             weight=3),
    23: dict(notes=['Security tactics: resist attacks (authenticate, limit exposure and access), detect attacks (intrusion detection), recover.'],
             seen=[see('ch3.2', 3, 'Tactics for each quality attribute')]),
    24: dict(notes=['Different stakeholders perceive the system differently, so they evaluate it through different views.']),
    25: dict(notes=['An architectural view = a representation of the system from one stakeholder perspective; each view evaluates certain properties.'],
             seen=[see('ch2.3', 3, 'The 4+1 view model')]),
    26: dict(notes=['Styles and patterns: proven, documented strategies for families of systems; architects must know them to pick the right one.'],
             seen=[see('ch4.1', 15, 'Architecture pattern classification')]),
    27: dict(notes=['Evaluate and validate early and iteratively: defects found early are much cheaper to fix (Amazon example: check scalability before building).'],
             seen=[see('ch8', 3, 'Architecture evaluation methods')]),
    28: dict(hl=[], notes=['Synchronicity means the design record and actual code agree. If they drift, developers make decisions from a false picture; update the design or correct the code so future work has a trustworthy reference.'],
             past=[past('m252', 'Q1 MCQ · design synchronicity ensures that')],
             exam=[mcq('Design synchronicity ensures that:', ['The implementation stays consistent with the architectural design', 'All teams finish at the same time', 'Processes run concurrently', 'The UI is responsive'], 0, 'Midterm 252, Q1.')],
             weight=3),
    29: dict(notes=['Architectural problem solving uses the holistic framework from Chapter 1: understand the problem and constraints, explore possible solutions, then evaluate whether the selected design meets the goal.'], seen=[see('ch1', 12, 'The holistic problem-solving framework')]),
    30: dict(notes=['Review both the definition and the architect’s tasks. Architecture communicates the major structures, quality decisions, and relationships that guide detailed design and construction.'], tips=[tip(TASKS)]),
}

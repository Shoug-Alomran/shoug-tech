"""SE322 annotated slides — Chapter 4, Lecture 1: styles and patterns, their history and classification.
See ch01_introduction.py for AUTO_SLIDES and the ANN keys."""
from .common import mcq, past, scen, see, short, tf, tip, trap, trick

AUTO_SLIDES = 'all'
OVERVIEW = 'This chapter studies reusable architecture patterns and their trade-offs, including data-centered systems, pipes and filters, distributed systems, MVC, and layered architectures. For each pattern, focus on the problem it solves and how its structure affects system qualities.'

DECK = {
    'key': 'ch4.1',
    'slug': '07-architecture-patterns-lecture-1',
    'file': 'architecture-patterns-lecture-1',
    'title': 'Architecture Patterns: Overview, History and Classification',
    'chapter': 'Chapter 4 · Lecture 1',
    'page': 'ch04_1_page',  # notes, highlights and exam questions in the page schema
    'pdf': '/academics/software-engineering/se322/slides/chapter-4-architecture-patterns-lecture-1-extra/',
    'lede': ('Why styles and patterns exist (reuse of proven solutions), who introduced them (Alexander 1977, '
             'the 1990s styles, the Gang of Four 1994, Buschmann et al. 1996), architectural vs. design patterns, '
             'and the five system types with their patterns. That classification is the map for Lectures 2 and 3.'),
}

CLASSES = ('System type → pattern: DATA-CENTERED → blackboard (repository) · DATA FLOW → pipes and filters · '
           'DISTRIBUTED → client-server, broker · INTERACTIVE → MVC · HIERARCHICAL → layered (main program and subroutine).')

ANN = {
    1: dict(kind='title', title='Architecture Patterns', body=[], sub='SE322 · Chapter 4, Lecture 1', tips=[tip(CLASSES)]),
    2: dict(notes=['A style describes a broad system organization; a pattern gives a reusable solution to a recurring problem in a stated context. They are starting points, not recipes: check that the pattern’s assumptions match your requirements.']),
    3: dict(notes=['Analogy: once you have a method to compute an average, you reuse it for any list. Styles and patterns are reusable recipes.']),
    4: dict(notes=['Systems are decomposed into logical components; past experience (styles and patterns) gives proven strategies for that decomposition.']),
    5: dict(notes=['Building architects reuse established styles; software architects reuse documented structures for similar problems. The analogy is about applying a proven organization, not copying every detail regardless of context.']),
    6: dict(notes=['Pattern and style catalogues capture a solution’s context, structure, trade-offs, and consequences. They help architects communicate and compare designs, but the system’s requirements determine whether a catalogue entry fits.']),
    7: dict(notes=['Benefits of reuse: generic, understood solutions; better quality, faster design, shared vocabulary, fewer risks.'],
            exam=[short('What is the benefit of reusing architectural styles and patterns?', 'They are proven, documented solutions: design is faster, quality is better because they encode best practices, risk is lower, and the team shares a common vocabulary that makes the design easier to understand and communicate.')], weight=2),
    8: dict(notes=['1977: Christopher Alexander (buildings), a pattern language with picture, context, problem, solution.']),
    9: dict(notes=['In the 1990s, software architects began documenting recurring high-level organizations as architectural styles. A style describes a family of systems with characteristic components and interactions.']),
    10: dict(notes=['1994: the Gang of Four (Gamma, Helm, Johnson, Vlissides): 23 object-oriented DESIGN patterns, inspired by Alexander.'],
             exam=[mcq('The Gang of Four catalogued how many design patterns?', ['23', '12', '253', '5'], 0, ''),
                   mcq('The 1994 Gang of Four book is about:', ['Detailed design patterns', 'Architectural styles', 'Building architecture', 'Requirements engineering'], 0, '')], weight=2),
    11: dict(notes=['1996: Buschmann et al. merged styles and patterns into ARCHITECTURAL PATTERNS (context-problem-solution).',
                    'Architectural patterns = system-wide structure. Design patterns = medium scale, inside subsystems.'],
             tips=[trap('Architectural patterns shape the WHOLE system; design patterns work at the level of classes inside a subsystem.')],
             exam=[mcq('Architectural patterns differ from design patterns because they:', ['Specify system-wide structural properties', 'Only describe class code', 'Were invented by the GoF', 'Apply only to buildings'], 0, '')], weight=3),
    12: dict(notes=['The timeline connects the history of pattern thinking: Alexander’s building patterns, software architectural styles, the Gang of Four design patterns, and later architectural pattern catalogues.']),
    13: dict(notes=['Timeline summary: 1977 Alexander (253 patterns), 1990s styles, 1994 GoF (23), 1996 Buschmann (architectural patterns).'],
             tips=[trick('77 → 90s → 94 → 96: Alexander, styles, GoF, Buschmann.')]),
    14: dict(notes=['Choose a pattern based on system needs and quality priorities, not its name. A large system can combine a layered structure with client-server deployment because patterns describe different aspects of the design.']),
    15: dict(notes=['Five system types: data-centered, data flow, distributed, interactive, hierarchical.'], tips=[tip(CLASSES)],
             exam=[mcq('Pipes and filters belongs to which system type?', ['Data flow', 'Data-centered', 'Distributed', 'Hierarchical'], 0, ''),
                   mcq('MVC is classified under:', ['Interactive systems', 'Distributed systems', 'Data flow systems', 'Hierarchical systems'], 0, '')],
             weight=3),
    16: dict(notes=['A repository lets independent components read and update shared data. That makes data sharing straightforward, but the store can become a bottleneck or single point of failure.']),
    17: dict(notes=['In a hospital-record system, departments share a central patient database. The example illustrates how multiple independent clients can access common information while needing rules for consistent updates.']),
    18: dict(notes=['In data-flow design, each stage transforms an input and hands its output to the next. This fits pipelines such as a compiler turning source text into tokens, syntax trees, and machine code.']),
    19: dict(notes=['A compiler is a transformation pipeline: lexical analysis produces tokens, parsing builds structure, and code generation emits output. Each stage consumes one representation and produces another.']),
    20: dict(notes=['Distributed components run on separate machines, so network delay or partial failure can occur even when the software is correct. The design needs timeouts and a plan for what to do when only part of the system is reachable.'], past=[past('m261', 'Q6 · match scenarios to architectural styles', related=True)]),
    21: dict(notes=['Online banking separates browser/mobile clients and server-side services, often across machines. The example is distributed because components communicate over a network rather than sharing one process.']),
    22: dict(notes=['Interactive designs separate changing presentation from the data and rules it displays. That helps when the same information needs several screens or the UI changes more often than business logic.']),
    23: dict(notes=['A word processor or app may offer multiple views of the same underlying data. Separating view and model helps keep the data authoritative while allowing the interface to respond to user actions.']),
    24: dict(notes=['Interactive describes a system organized around user interaction; distributed describes components separated across machines. These are different classification dimensions, and one system can be both.']),
    25: dict(notes=['Hierarchical: components in levels where each uses the level below (layered, main program and subroutine).']),
    26: dict(notes=['Operating systems and network stacks use hierarchical organization: each layer offers services to the layer above and relies on the layer below. Layer boundaries constrain dependencies and simplify reasoning.']),
    27: dict(notes=['A DBMS can be seen as a repository (data-centered) or as a layered system, depending on the viewpoint.']),
    28: dict(notes=['The next lecture studies the patterns in detail. For each pattern, focus on the problem it addresses, its components and interactions, and the quality trade-offs it introduces.'], seen=[see('ch4.2', 6, 'Blackboard pattern')]),
}

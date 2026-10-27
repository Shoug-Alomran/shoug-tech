"""SE322 annotated slides — Chapter 2, Lecture 2: the architecture process and requirements engineering.
See ch01_introduction.py for AUTO_SLIDES and the ANN keys."""
from .common import mcq, past, scen, see, short, tf, tip, trap, trick

AUTO_SLIDES = 'all'
OVERVIEW = 'This chapter develops software architecture from requirements through design decisions and stakeholder views. It connects requirements engineering to architecture, examines quality-driven decisions, and uses the 4+1 model to describe logical structure, runtime behavior, development, deployment, and scenarios.'

DECK = {
    'key': 'ch2.2',
    'slug': '03-software-architecture-lecture-2',
    'file': 'software-architecture-lecture-2',
    'title': 'Software Architecture: Process and Requirements',
    'chapter': 'Chapter 2 · Lecture 2',
    'page': 'ch02_2_page',  # notes, highlights and exam questions in the page schema
    'pdf': '/academics/software-engineering/se322/slides/chapter-2-software-architecture-lecture-2-extra/',
    'lede': ('The five-step architecture process, then the first step in depth: requirements engineering '
             '(elicitation, analysis, specification, validation) and the six characteristics of a good '
             'requirement. Quiz 1 261 built most of its fill-in and scenario questions from this lecture.'),
}

GOOD = 'A good requirement is: Specific · Correct · Complete · Consistent · Attainable · Verifiable (“SC3AV”).'

ANN = {
    1: dict(kind='title', title='Software Architecture', body=[], sub='SE322 · Chapter 2, Lecture 2',
            notes=['This lecture explains the architecture process and then examines requirements engineering, the first major activity. Keep the sequence in view: architectural decisions depend on good requirements, and later views and evaluations depend on those decisions being clear.']),
    2: dict(notes=['The architecture process has five steps; this lecture focuses on requirements engineering. Requirements establish the functional needs and quality constraints that later architecture work must address.']),
    3: dict(notes=['Architecture process: understand and evaluate requirements → design → evaluate → document → monitor and control implementation.'],
            tips=[trick('“U-D-E-D-M”: Understand, Design, Evaluate, Document, Monitor.')],
            past=[past('q261', 'match the architecture process activities'), past('q261', 'fill-in · architecture evaluation')],
            exam=[mcq('After designing the architecture, the activity that checks it satisfies important requirements and concerns is:', ['Architecture evaluation', 'Architecture documentation', 'Monitoring implementation', 'Requirements elicitation'], 0, 'Quiz 1 261.'),
                  mcq('Which is the LAST step of the architecture process?', ['Monitor and control implementation', 'Document the architecture', 'Evaluate the architecture', 'Design the architecture'], 0, '')],
            weight=3),
    4: dict(notes=['Elicitation discovers needs; analysis resolves ambiguity and conflict; specification records the agreement; validation checks it with stakeholders. Skipping a step can turn a misunderstood need into a precise but wrong design.'],
            exam=[mcq('Which is NOT a requirements engineering activity in the slides?', ['Deployment', 'Elicitation', 'Analysis', 'Validation'], 0, '')], weight=2),
    5: dict(hl=['Elicitation'], notes=['Elicitation: identify stakeholders, uncover needs and wants, and find the non-functional requirements. Starts by listing every source of requirements.'],
            past=[past('q261', 'fill-in · discovering needs = elicitation')],
            exam=[mcq('The requirements activity that discovers stakeholder needs through interviews and observation is:', ['Elicitation', 'Specification', 'Validation', 'Negotiation'], 0, 'Quiz 1 261.')],
            weight=3),
    6: dict(notes=['Techniques: interviews, facilitated meetings, observation, scenarios (also prototypes, questionnaires).'],
            past=[past('q261', 'scenario · interviews, observation, workshop = elicitation')],
            exam=[scen('An architect interviews end users, observes their current work, and runs a facilitated workshop. Which requirements activity is this?', 'Elicitation: these are elicitation techniques for discovering what stakeholders need.')],
            weight=3),
    7: dict(notes=['Analysis fixes contradictory, incomplete, vague or wrong requirements before detailed design. Tasks: classification, prioritization and negotiation, conceptual modeling.']),
    8: dict(notes=['Banking-app example of analysis: conflicting availability vs. maintenance-downtime requirements get resolved.']),
    9: dict(notes=['A functional requirement names an action (“transfer funds”); a quality requirement sets a condition on it (“confirm within two seconds”). Both matter: a function can exist and still be too slow or difficult to use.'],
            exam=[mcq('“The system must load within 2 seconds” is a:', ['Non-functional requirement', 'Functional requirement', 'Process requirement', 'Design pattern'], 0, '')], weight=2),
    10: dict(hl=['negotiation'], notes=['Prioritization finds the most important functions and orders the work (builds). **Negotiation** resolves conflicts between requirements.'],
             past=[past('q261', 'resolving conflicting stakeholder requirements')],
             exam=[mcq('Two stakeholder groups want requirements that cannot both be fully met. Which activity resolves this?', ['Prioritization and negotiation', 'Elicitation', 'Classification', 'Deployment'], 0, 'Quiz 1 261.')],
             weight=3),
    11: dict(notes=['Conceptual modeling: understand context and system boundaries; often where architectural design begins (decomposition).']),
    12: dict(hl=['validation'], notes=['Specification documents the results; **validation** checks with stakeholders that the documented requirements correctly represent their needs.'],
             tips=[tip(GOOD)],
             past=[past('q261', 'fill-in · checking requirements represent needs = validation')],
             exam=[mcq('Checking that documented requirements correctly represent stakeholder needs is requirements:', ['Validation', 'Elicitation', 'Classification', 'Prioritization'], 0, 'Quiz 1 261.')],
             weight=3),
    13: dict(notes=['A specific requirement has one plausible interpretation, is concise, and expresses one idea. “The app is fast and easy” bundles two vague qualities; separate them and define measurable acceptance conditions.']),
    14: dict(notes=['Specific: “search using product ID”, “respond within ½ second”. Non-specific: “user-friendly”, “fast”.']),
    15: dict(notes=['Correctness means a requirement accurately reflects the intended system behavior. If the requirement is wrong, a perfectly implemented design can still produce the wrong system, so validation must involve relevant stakeholders.']),
    16: dict(notes=['Each requirement must be detailed enough to stand alone, while the full set must cover the system’s scope. A clear login requirement does not make the SRS complete if account recovery was never considered.']),
    17: dict(notes=['Consistent: requirements don’t block each other (offline-only vs. online payments). Attainable: possible with the budget, schedule and technology.']),
    18: dict(notes=['A requirement is verifiable when a reviewer can decide pass or fail using evidence. “Respond quickly” invites disagreement; “respond within two seconds under the stated load” can be measured.'],
             tips=[tip(GOOD)],
             past=[past('q261', 'T/F · “respond quickly” is verifiable (false)')],
             exam=[tf('The requirement “The system should respond quickly” is specific and verifiable.', False, 'Quiz 1 261. It has no measurable target.')],
             weight=3),
    19: dict(notes=['The next lecture introduces the 4+1 view model, which organizes architecture around different stakeholder concerns. Requirements from this lecture become the basis for choosing and describing those views.'], seen=[see('ch2.3', 4, 'The 4+1 view model')]),
}

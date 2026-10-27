"""SE322 annotated slides — Chapter 2, Lecture 3: the 4+1 view model.
See ch01_introduction.py for AUTO_SLIDES and the ANN keys."""
from .common import mcq, past, scen, see, short, tf, tip, trap, trick

AUTO_SLIDES = 'all'
OVERVIEW = 'This chapter develops software architecture from requirements through design decisions and stakeholder views. It connects requirements engineering to architecture, examines quality-driven decisions, and uses the 4+1 model to describe logical structure, runtime behavior, development, deployment, and scenarios.'

DECK = {
    'key': 'ch2.3',
    'slug': '04-software-architecture-lecture-3',
    'file': 'software-architecture-lecture-3',
    'title': 'Software Architecture: the 4+1 View Model',
    'chapter': 'Chapter 2 · Lecture 3',
    'page': 'ch02_3_page',  # notes, highlights and exam questions in the page schema
    'pdf': '/academics/software-engineering/se322/slides/chapter-2-software-architecture-lecture-3-extra/',
    'lede': ('Kruchten’s 4+1 views (logical, process, development, physical, plus the user/scenario view): what '
             'each one shows, who reads it, and which UML diagrams model it, with the ATM example. Midterm 252 '
             'Q4 was a full 4+1 table, and Quiz 1 and Midterm 261 asked which view fits which concern.'),
}

TABLE = ('4+1 cheat sheet: LOGICAL = functionality · end users, analysts, designers · class, object, sequence, communication, state, activity. '
         'PROCESS = run-time, concurrency, synchronization · integrators · activity (and sequence). '
         'DEVELOPMENT = code organisation into modules/packages · programmers, project managers · package, component. '
         'PHYSICAL = deployment on hardware, availability, performance, scalability · system engineers · deployment. '
         'USER (+1, scenarios) = use cases that tie the others together · everyone · use case.')

ANN = {
    1: dict(kind='title', title='Software Architecture', body=[], sub='SE322 · Chapter 2, Lecture 3: the 4+1 View Model', tips=[tip(TABLE)]),
    2: dict(notes=['The model uses four architecture views plus the user/scenario view. Each view answers different questions for different stakeholders; learn the summary table by pairing each view with its focus, audience, and common diagrams.']),
    3: dict(notes=['No single view shows everything, so the architecture is described through several views, each for particular stakeholders. This manages complexity.'],
            past=[past('m252', 'Q1 MCQ · why multiple views')],
            seen=[see('ch2.1', 12, 'No single diagram describes an architecture')], weight=2),
    4: dict(notes=['The logical, process, development, and physical views answer different questions about one system; scenarios tie them together by showing how the system is used. A change should make sense across all relevant views, not just one diagram.'],
            exam=[mcq('The 4+1 view model was introduced by:', ['Philippe Kruchten', 'Grady Booch', 'The Gang of Four', 'IEEE'], 0, '')], weight=2),
    5: dict(hl=['functional requirements'],
            notes=['LOGICAL view: decomposition into classes/objects and their connections; an abstraction of the FUNCTIONAL requirements.',
                   'Static: class/object diagrams. Dynamic: sequence, communication, state, activity, interaction overview.', 'Stakeholders: end users, analysts, designers.'],
            past=[past('q261', 'fill-in · view of major functional elements = logical'), past('m252', 'Q4 · 4+1 table')],
            exam=[mcq('The 4+1 view that captures major functional elements and their relationships is the:', ['Logical view', 'Development view', 'Process view', 'Physical view'], 0, 'Quiz 1 261.')],
            weight=3),
    6: dict(notes=['The ATM class diagram is a logical view: it shows the important classes, their responsibilities, and static relationships. Use it to understand the system’s object-oriented structure, not the timing of runtime messages.']),
    7: dict(notes=['A communication diagram emphasizes which objects collaborate; its message numbers show call order. Use it to see the network of participants, while a sequence diagram is clearer when timing is the main question.']),
    8: dict(notes=['A sequence diagram lays out participating objects and messages over time. Read from top to bottom to follow a scenario, and use it when timing or message order matters.']),
    9: dict(notes=['The process view describes what runs at the same time and how those activities coordinate. It helps expose races, bottlenecks, or synchronization risks that a static class diagram cannot show.'],
            past=[past('q261', 'which view for concurrency and synchronization')],
            exam=[mcq('Analysing concurrent execution, communication among running processes and synchronization uses the:', ['Process view', 'Logical view', 'Development view', 'Physical view'], 0, 'Quiz 1 261.')],
            weight=3),
    10: dict(notes=['The ATM activity diagram illustrates workflow and control flow in the process view. Follow branches and actions to understand what the system does during the scenario.']),
    11: dict(hl=['static organization'],
             notes=['DEVELOPMENT view: static organisation of the code into modules, packages, libraries, subsystems. Package and component diagrams. Stakeholders: programmers, project managers.'],
             past=[past('q261', 'fill-in · organisation of source modules = development view')],
             exam=[mcq('The view that organizes source-code modules, packages and development units is the:', ['Development view', 'Logical view', 'Physical view', 'Process view'], 0, 'Quiz 1 261.')],
             weight=3),
    12: dict(notes=['The development view describes how software is organized for implementation, such as modules, components, and interfaces. It helps developers understand code ownership, dependencies, and build organization.']),
    13: dict(hl=['deployment'],
             notes=['PHYSICAL view: deployment onto hardware nodes (deployment diagrams). Used to evaluate availability (redundant nodes), performance and scalability.'],
             past=[past('m252', 'Q1 MCQ · view for scalability and performance'), past('q261', 'which view maps software to servers')],
             exam=[mcq('Which view mainly helps evaluate scalability and performance?', ['Physical view', 'Logical view', 'Development view', 'User view'], 0, 'Midterm 252, Q1.'),
                   mcq('A deployment engineer wants to know which software runs on which servers. Which view?', ['Physical view', 'Process view', 'Development view', 'Logical view'], 0, 'Quiz 1 261.')],
             weight=3),
    14: dict(notes=['The physical view maps software elements onto hardware nodes and connections. An ATM deployment diagram shows where components run and how the deployed pieces communicate.']),
    15: dict(notes=['USER (scenario) view, the “+1”: use cases showing how users use the system. It ties the other four together and is used to discover and validate the architecture.'],
             tips=[trap('The +1 view is the user/scenario view (use cases), NOT the database.')],
             past=[past('m261', 'T/F · the +1 view is the database (false)')],
             exam=[tf('The “+1” view represents the database structure of the system.', False, 'Midterm 261. It is the user/scenario view built from use cases.')],
             weight=3),
    16: dict(notes=['The user view (the “+1”) captures important scenarios or use cases that connect the other views. An ATM use-case diagram summarizes the goals users pursue with the system.']),
    17: dict(notes=['For each view, remember its main question and the diagrams commonly used to express it. Logical is structure; process is runtime concurrency; development is implementation organization; physical is deployment; scenarios tie them together.'], tips=[tip(TABLE)]),
    18: dict(notes=['Use the summary table as a matching tool: identify the stakeholder’s question, then choose the view and notation that can answer it. The 4+1 views are complementary perspectives, not five competing architectures.'], tips=[tip(TABLE)],
             past=[past('m252', 'Q4 · fill in the 4+1 table'), past('q261', 'match each view to its concern')],
             exam=[short('For each 4+1 view, give its description, stakeholders and UML diagrams. (Midterm 252, Q4)',
                         'Logical: functionality / end users, analysts, designers / class, object, sequence, communication, state, activity. Process: run-time concurrency and synchronization / integrators / activity. Development: code organisation into modules and packages / programmers, managers / package, component. Physical: deployment on hardware, availability, performance / system engineers / deployment. User (+1): scenarios that tie the views together / all stakeholders / use case.'),
                   mcq('Which UML diagram belongs to the development view?', ['Package diagram', 'Deployment diagram', 'Use case diagram', 'State diagram'], 0, '')],
             weight=3),
    19: dict(notes=['The five-view recap is a retrieval exercise: name each view, its concern, its stakeholders, and a representative diagram. The views complement one another; none alone explains the entire architecture.']),
}

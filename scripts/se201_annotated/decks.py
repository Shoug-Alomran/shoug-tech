"""SE201 annotated slides — every Introduction to Software Engineering deck (Sommerville / Pressman).

One module holds all the decks: each deck is a namespace class with DECK and ANN (and AUTO_SLIDES).
Slides without an ANN entry are shown without notes. past('q1', ...) points at Quiz 1 (Ch. 1 & 2) in
exams/. See cs331_annotated/ch01_1_introduction.py for the ANN keys."""
from .common import DECKS, mcq, past, see, short, tf, tip, trap, trick


def deck(key, title, chapter, lede):
    slug, file, folder, _ = DECKS[key]
    return {'key': key, 'slug': slug, 'file': file, 'title': title, 'chapter': chapter,
            'pdf': '/academics/software-engineering/se201/slides/%s/' % folder, 'lede': lede}


class practices:
    AUTO_SLIDES = True
    DECK = deck('d01', 'Software Engineering Practices and Ethics', 'Chapter 1',
                'What software engineering is and why it matters, software costs and failures, generic vs. customized '
                'products, attributes of good software, how software differs from hardware, application types, web '
                'software engineering, the layered view, the generic process framework and umbrella activities, and '
                'professional ethics (ACM/IEEE code) with the insulin-pump and Mentcare case studies.')
    ANN = {
        4: dict(notes=['Software engineering: an engineering discipline concerned with ALL aspects of software production, from specification to maintenance.'],
                past=[past('q1', 'the primary focus of software engineering')],
                exam=[mcq('The primary focus of software engineering is:', ['Software production and maintenance', 'Hardware development', 'Network management', 'Database administration'], 0, '')], weight=3),
        5: dict(notes=['Software costs more than hardware, and maintaining it costs more than developing it.']),
        10: dict(notes=['Generic products: sold on the open market; the DEVELOPER owns the specification. Customized (bespoke): built for one customer, who owns the specification.'],
                 past=[past('q1', 'who owns the specification of a generic product')],
                 exam=[mcq('For a generic software product, the specification is owned by:', ['The developer', 'The customer', 'The government', 'The end user'], 0, '')], weight=3),
        12: dict(notes=['Essential attributes: maintainability, dependability and security, efficiency, acceptability.'],
                 exam=[mcq('Which is NOT one of the essential attributes of good software?', ['Popularity', 'Maintainability', 'Dependability', 'Efficiency'], 0, '')], weight=3),
        16: dict(notes=['Hardware WEARS OUT (bathtub curve); software doesn’t wear out but DETERIORATES as changes introduce defects.'],
                 past=[past('q1', 'wear out vs. deteriorate')],
                 tips=[trap('Software deteriorates; it does NOT wear out.')],
                 exam=[tf('Software does not deteriorate over time; it wears out.', False, 'It is the other way round.')], weight=3),
        17: dict(notes=['Issues affecting most software: heterogeneity, business and social change, security and trust, scale.']),
        20: dict(notes=['Application types: stand-alone, interactive transaction-based, embedded control, batch, entertainment, modeling and simulation, data collection, systems of systems.']),
        29: dict(notes=['Layers: quality focus (bedrock) → process → methods → tools.'],
                 exam=[mcq('The foundation layer of software engineering is:', ['A quality focus', 'Tools', 'Methods', 'Process'], 0, '')], weight=3),
        33: dict(notes=['Generic framework activities: communication, planning, modeling, construction, deployment.'],
                 tips=[trick('C-P-M-C-D: Communication, Planning, Modeling, Construction, Deployment.')],
                 exam=[mcq('Which is NOT a generic framework activity?', ['Risk management', 'Communication', 'Modeling', 'Deployment'], 0, 'Risk management is an umbrella activity.')], weight=3),
        35: dict(notes=['Umbrella activities run throughout: project tracking and control, risk management, quality assurance, technical reviews, measurement, configuration management, reusability management, work-product preparation.'], weight=3),
        41: dict(notes=['Professional responsibility: confidentiality, competence, intellectual property rights, computer misuse.']),
        46: dict(notes=['ACM/IEEE code: 8 principles: public, client and employer, product, judgment, management, profession, colleagues, self. Act in the PUBLIC interest first.'],
                 exam=[mcq('According to the ACM/IEEE code, software engineers shall act consistently with the interest of:', ['The public', 'Their manager only', 'Shareholders only', 'Themselves'], 0, '')], weight=3),
        50: dict(notes=['Ethical dilemmas: disagreeing with management policy, being asked to release unsafe software, working on military systems.']),
        52: dict(notes=['Case studies: insulin pump (safety-critical embedded), Mentcare (patient information system).']),
    }


class processes:
    AUTO_SLIDES = True
    DECK = deck('d02', 'Software Processes', 'Chapter 2',
                'Software process descriptions, plan-driven vs. agile processes, the waterfall and modified waterfall '
                'models, incremental development, evolutionary models (prototyping, spiral), component-based and '
                'reuse-oriented development, the Unified Process, and the Agile manifesto values and principles.')
    ANN = {
        3: dict(notes=['Software process: a structured set of activities: specification, design and implementation, validation, evolution.']),
        5: dict(notes=['Plan-driven: all activities planned in advance, progress measured against the plan. Agile: incremental planning, easy to change.']),
        8: dict(notes=['Waterfall: separate sequential phases; each must finish before the next. Good when requirements are well understood and stable.'],
                exam=[mcq('The waterfall model is most appropriate when:', ['Requirements are well understood and unlikely to change', 'Requirements change weekly', 'The customer wants early working versions', 'The system is highly experimental'], 0, '')], weight=3),
        11: dict(notes=['Drawback: inflexible partitioning makes it hard to respond to changing requirements; working software appears late.']),
        13: dict(notes=['Incremental: deliver the system in increments; each adds functionality. Combines linear sequences applied in parallel (staggered).'],
                 past=[past('q1', 'incremental = linear + parallel flow')],
                 exam=[tf('The incremental model combines elements of linear and parallel process flow.', True, '')], weight=3),
        16: dict(notes=['Benefits: lower cost of change, earlier customer feedback, earlier delivery of useful software.']),
        17: dict(notes=['Problems: the process is not visible, and structure degrades as increments are added.']),
        19: dict(notes=['Prototyping: build a quick version to clarify requirements when they are fuzzy. Risk: customers think the prototype is the product.'],
                 exam=[mcq('Prototyping is most useful when:', ['Requirements are unclear', 'The system is safety-critical and fully specified', 'There is no customer', 'The team is very large'], 0, '')], weight=3),
        23: dict(notes=['Spiral (Boehm): iterative loops of planning, RISK ANALYSIS, engineering and evaluation. Risk-driven.'],
                 tips=[trick('Spiral = risk-driven.')],
                 exam=[mcq('Which process model is explicitly risk-driven?', ['Spiral', 'Waterfall', 'Incremental', 'Code-and-fix'], 0, '')], weight=3),
        27: dict(notes=['Component-based development: assemble the system from existing (COTS) components.']),
        31: dict(notes=['Reuse: faster, cheaper, more reliable, but compromises on requirements and less control over evolution.']),
        32: dict(notes=['Unified Process: use-case driven, architecture-centric, iterative and incremental. Phases: inception, elaboration, construction, transition. Requirements are refined across phases.'],
                 past=[past('q1', 'requirements across UP phases')],
                 exam=[mcq('The four phases of the Unified Process are:', ['Inception, elaboration, construction, transition', 'Planning, design, coding, testing', 'Communication, modeling, construction, deployment', 'Sprint, review, retrospective, release'], 0, '')], weight=3),
        40: dict(notes=['Agile values: individuals and interactions over processes and tools; working software over documentation; customer collaboration over contract negotiation; responding to change over following a plan.'],
                 tips=[trap('The manifesto says the items on the right still have value; the left is valued MORE.')],
                 exam=[mcq('Which is an Agile Manifesto value?', ['Responding to change over following a plan', 'Comprehensive documentation over working software', 'Contract negotiation over customer collaboration', 'Processes over individuals'], 0, '')], weight=3),
        43: dict(notes=['12 principles: satisfy the customer through early, continuous delivery; welcome changing requirements; deliver frequently; business and developers work together daily; working software is the measure of progress…']),
        48: dict(notes=['Feature matrix: compare models by requirements stability, customer involvement, risk, delivery speed.']),
    }


class agile:
    AUTO_SLIDES = True
    DECK = deck('d03', 'Agile Software Engineering', 'Chapter 3',
                'Extreme Programming and its practices (user stories, test-first development, pair programming, '
                'refactoring, continuous integration), Scrum terminology, roles, sprints and the product backlog, '
                'and agile project management.')
    ANN = {
        4: dict(notes=['XP: an influential agile method taking good practice to the "extreme": very frequent releases, small increments.']),
        5: dict(notes=['XP practices: incremental planning, small releases, simple design, test-first development, refactoring, pair programming, collective ownership, continuous integration, sustainable pace, on-site customer.']),
        7: dict(notes=['User stories: short scenarios from the user’s view; broken into task cards that are estimated.']),
        10: dict(notes=['Test-first (TDD): write the test before the code; tests are automated and run on every build.'],
                 exam=[mcq('In XP, tests are written:', ['Before the code they test', 'After release', 'Only by testers', 'Never'], 0, '')], weight=3),
        12: dict(notes=['Refactoring: improve structure without changing behaviour. Pair programming: two developers at one computer, roles swap.'],
                 exam=[mcq('Improving code structure without changing what it does is:', ['Refactoring', 'Re-engineering', 'Regression testing', 'Debugging'], 0, '')], weight=3),
        17: dict(notes=['Scrum terms: product backlog, sprint backlog, sprint (2–4 weeks), daily scrum, velocity, potentially shippable increment.']),
        19: dict(notes=['Roles: Product Owner (owns and prioritizes the backlog), Scrum Master (coach, removes impediments), Development Team (self-organizing).'],
                 tips=[trap('The Scrum Master is NOT a traditional project manager; the Product Owner prioritizes.')],
                 exam=[mcq('Who prioritizes the product backlog?', ['Product Owner', 'Scrum Master', 'Development Team', 'Stakeholders'], 0, ''),
                       mcq('Who removes impediments for the team?', ['Scrum Master', 'Product Owner', 'Customer', 'Tester'], 0, '')], weight=3),
        21: dict(notes=['Sprint: a fixed time-box producing a potentially shippable increment. Sprint planning → daily scrums → review → retrospective.'],
                 exam=[mcq('The daily scrum is a short meeting where the team:', ['Shares progress, plans and blockers', 'Writes the requirements document', 'Demos to the customer', 'Assigns blame'], 0, '')], weight=3),
        25: dict(notes=['Product backlog: a prioritized list of items (features, bugs, tech work) to do.']),
        27: dict(notes=['PBI states: ready for consideration → ready for refinement → ready for implementation.']),
        33: dict(notes=['Agile PM: the team estimates and commits; the Scrum Master facilitates; transparency through boards and burndown charts.']),
    }


class project_management:
    AUTO_SLIDES = True
    DECK = deck('d04', 'Software Project Management', 'Chapter 4',
                'The 4 Ps (people, product, process, project), stakeholders, team leaders and team structures, scope '
                'and problem decomposition, signs of project risk, the triple constraint, estimation and scheduling, '
                'precedence (activity-on-node) diagrams, the critical path and float, Gantt charts, and risk management.')
    ANN = {
        3: dict(notes=['Management spectrum: the 4 Ps: People, Product, Process, Project.']),
        4: dict(notes=['Stakeholders: senior managers, project managers, practitioners, customers, end users.']),
        14: dict(notes=['Scope: context, information objectives, function and performance. Bounded before estimation.']),
        21: dict(notes=['Signs of trouble: no customer understanding, poorly defined scope, poor change management, unrealistic deadlines, lack of skills.']),
        25: dict(notes=['Triple constraint: scope, time, cost (quality in the middle); change one and the others move.'],
                 exam=[mcq('The triple constraint consists of:', ['Scope, time and cost', 'People, process and tools', 'Risk, quality and value', 'Requirements, design and testing'], 0, '')], weight=3),
        31: dict(notes=['Precedence diagram (activity on node): ES/EF from the forward pass, LS/LF from the backward pass; slack (float) = LS − ES.'],
                 tips=[tip('Forward pass: EF = ES + duration, ES = max(EF of predecessors). Backward pass: LS = LF − duration, LF = min(LS of successors). Critical path = activities with zero float.')],
                 exam=[mcq('The critical path is the:', ['Longest path, made of zero-float activities', 'Shortest path', 'Path with the most activities', 'Path with the most resources'], 0, ''),
                       short('Activity A (3 days) → B (4 days) and A → C (2 days); B and C → D (1 day). Find the project length and the critical path.', 'A–B–D = 3 + 4 + 1 = 8 days; A–C–D = 6 days. Project length 8 days; critical path A–B–D; C has 2 days of float.')], weight=3),
        62: dict(notes=['Gantt chart: bars on a calendar show each task’s duration and timing.']),
        67: dict(notes=['Risk = an event that may adversely affect the project. Categories: project, product, business risks.'],
                 exam=[mcq('Staff turnover is mainly a:', ['Project risk', 'Product risk', 'Business risk', 'Technology risk'], 0, '')], weight=3),
        70: dict(notes=['Process: identification → analysis (probability, effects) → planning (avoid, minimize, contingency) → monitoring.'],
                 exam=[mcq('Correct order of the risk-management process:', ['Identify, analyse, plan, monitor', 'Plan, identify, monitor, analyse', 'Analyse, identify, monitor, plan', 'Monitor, plan, analyse, identify'], 0, '')], weight=3),
        77: dict(notes=['Strategies: avoidance (lower probability), minimization (lower impact), contingency plans (what to do if it happens).']),
    }


class requirements:
    AUTO_SLIDES = True
    DECK = deck('d05', 'Requirements Engineering', 'Chapter 5.1',
                'User vs. system requirements and their readers, stakeholders, functional, non-functional and domain '
                'requirements, the requirements engineering process (elicitation, specification, validation), user '
                'stories and scenarios, natural-language specification, the requirements document, and management.')
    ANN = {
        6: dict(notes=['User requirements: natural language + diagrams for customers. System requirements: detailed, structured, for developers and contracts.']),
        10: dict(notes=['Functional: what the system should DO (services). Non-functional: constraints on HOW (performance, security, usability, reliability). Domain: from the application domain.'],
                 tips=[trick('If it says "the system shall <do something>", it is functional; if it talks about speed, availability, platform, it is non-functional.')],
                 exam=[mcq('"The system shall be available 99.9% of the time" is a:', ['Non-functional requirement', 'Functional requirement', 'Domain requirement', 'User story'], 0, ''),
                       mcq('"A user shall be able to search the appointment list" is a:', ['Functional requirement', 'Non-functional requirement', 'Design constraint', 'Process requirement'], 0, '')], weight=3),
        16: dict(notes=['Non-functional types: product (performance, usability, reliability), organizational (process, standards), external (legal, ethical).']),
        18: dict(notes=['RE process: elicitation and analysis → specification → validation, iterated (spiral).']),
        21: dict(notes=['Elicitation problems: stakeholders don’t know what they want, use their own terms, conflict, change their minds; politics.']),
        25: dict(notes=['Techniques: interviews (closed/open), ethnography (observation), scenarios, use cases, stories.']),
        28: dict(notes=['User story: "As a <role>, I want <goal> so that <benefit>." Scenarios describe a real interaction in more detail.']),
        36: dict(notes=['Guidelines: a standard format, "shall" for mandatory, "should" for desirable, highlight key parts, avoid jargon, explain why.']),
        39: dict(notes=['The SRS: the official statement of what is required; WHAT, not HOW.']),
        41: dict(notes=['Validation checks: validity, consistency, completeness, realism, verifiability.'],
                 exam=[mcq('Checking that requirements do not contradict each other is a check for:', ['Consistency', 'Realism', 'Verifiability', 'Completeness'], 0, '')], weight=3),
        43: dict(notes=['Validation techniques: requirements reviews, prototyping, test-case generation.']),
        45: dict(notes=['Requirements management: track changes, traceability, change control.']),
    }


class modeling:
    AUTO_SLIDES = True
    DECK = deck('d06', 'System Modeling with UML', 'Chapter 5.2',
                'Context, interaction, structural and behavioral models, then UML in detail: use-case diagrams with '
                'include/extend/generalization, sequence diagrams and messages, class diagrams with association, '
                'aggregation, composition, generalization and multiplicity, activity diagrams with swimlanes, and '
                'state machine diagrams.')
    ANN = {
        7: dict(notes=['Perspectives: external (context), interaction, structural, behavioral.']),
        8: dict(notes=['Key UML diagrams: activity, use case, sequence, class, state.']),
        10: dict(notes=['Context model: shows the system boundary and the other systems around it.']),
        16: dict(notes=['Use case: a task an actor performs with the system; stick-figure actors and ovals.']),
        19: dict(notes=['Sequence diagram: objects across the top, lifelines down, messages in time order.']),
        24: dict(notes=['Class diagram: classes (name, attributes, operations) and the relationships between them.']),
        36: dict(notes=['<<include>>: the base use case ALWAYS uses the included one. <<extend>>: optional behaviour that extends the base under a condition.'],
                 tips=[trap('Include arrow points TO the included use case; extend arrow points FROM the extension TO the base.')],
                 exam=[mcq('"Print receipt" happens only if the customer asks. Relative to "Withdraw cash" it is:', ['<<extend>>', '<<include>>', 'Generalization', 'Association'], 0, ''),
                       mcq('Every "Withdraw cash" must "Authenticate user". This is:', ['<<include>>', '<<extend>>', 'Generalization', 'Dependency'], 0, '')], weight=3),
        51: dict(notes=['Messages: synchronous (filled arrowhead, caller waits), asynchronous (open arrowhead), return (dashed), self-message.']),
        60: dict(notes=['alt fragment: alternatives with guards; opt: optional; loop: repetition.']),
        71: dict(notes=['Relationships: dependency (dashed arrow), association (line), generalization (hollow triangle), aggregation (hollow diamond), composition (filled diamond).']),
        74: dict(notes=['Generalization = inheritance ("is-a"): hollow triangle points to the parent.']),
        75: dict(notes=['Multiplicity: 1, 0..1, *, 1..* at each end of an association.'],
                 exam=[mcq('A multiplicity of 1..* means:', ['One or more', 'Zero or more', 'Exactly one', 'Zero or one'], 0, '')], weight=3),
        81: dict(notes=['Aggregation: whole–part where parts can exist alone (Department–Professor). Composition: parts die with the whole (House–Room).'],
                 tips=[trick('Filled diamond = "dies with" (composition). Hollow diamond = "can live without" (aggregation).')],
                 exam=[mcq('An Order and its OrderLines (deleted with the order) is best modeled as:', ['Composition', 'Aggregation', 'Generalization', 'Dependency'], 0, '')], weight=3),
        82: dict(notes=['Association class: attributes that belong to the link itself (Enrollment with grade between Student and Course).']),
        90: dict(notes=['Activity diagram: workflow of actions; initial node, actions, decisions (diamond), fork/join bars, final node.']),
        101: dict(notes=['Swimlanes show WHO performs each activity.']),
        103: dict(notes=['State machine: states an object can be in and the transitions triggered by events [guard] / action.'],
                  exam=[mcq('Which diagram best shows how one object changes state in response to events?', ['State machine diagram', 'Sequence diagram', 'Class diagram', 'Use-case diagram'], 0, '')], weight=3),
    }


class design:
    AUTO_SLIDES = True
    DECK = deck('d07', 'Software Design', 'Chapter 6',
                'The purpose of design, quality guidelines and design principles, fundamental concepts (abstraction, '
                'architecture, modularity, information hiding, stepwise refinement, functional independence: cohesion '
                'and coupling), architectural patterns (MVC, layered, client–server, repository, pipe and filter) and '
                'user-interface design rules.')
    ANN = {
        3: dict(notes=['Design translates requirements into a blueprint for construction; it is where quality is built in.']),
        10: dict(notes=['Principles: design should be traceable to requirements, not reinvent the wheel, minimize the gap with the problem, be uniform, accommodate change.']),
        13: dict(notes=['Fundamental concepts: abstraction, architecture, patterns, separation of concerns, modularity, information hiding, functional independence, refinement, refactoring.']),
        17: dict(notes=['Modularity: divide into modules. Too few = hard to understand; too many = integration cost. Aim for the minimum-cost region.']),
        20: dict(notes=['Information hiding: modules hide their internal details and expose only interfaces.']),
        21: dict(notes=['Stepwise refinement: top-down elaboration from high-level to detailed.']),
        23: dict(notes=['Functional independence: HIGH cohesion (a module does one thing) and LOW coupling (few dependencies between modules).'],
                 tips=[trick('High cohesion, low coupling.')],
                 exam=[mcq('A good design aims for:', ['High cohesion and low coupling', 'Low cohesion and high coupling', 'High cohesion and high coupling', 'Low cohesion and low coupling'], 0, '')], weight=3),
        29: dict(notes=['Architectural pattern: a proven, reusable solution to a recurring architecture problem.']),
        30: dict(notes=['MVC: Model (data and logic), View (presentation), Controller (handles input, updates model). Lets one model have many views.'],
                 exam=[mcq('In MVC, the component that handles user input is the:', ['Controller', 'Model', 'View', 'Router'], 0, '')], weight=3),
        33: dict(notes=['Layered: each layer uses only the layer below (UI → business logic → data). Easy to replace layers; performance overhead.']),
        36: dict(notes=['Client–server: services on servers, clients request them over a network.']),
        37: dict(notes=['Repository: components share a central data store.']),
        40: dict(notes=['Pipe and filter: data flows through a sequence of transformations (compilers, batch processing).'],
                 exam=[mcq('A compiler (lexer → parser → code generator) best fits which pattern?', ['Pipe and filter', 'MVC', 'Repository', 'Client–server'], 0, '')], weight=3),
        45: dict(notes=['Golden rules (Mandel): place the user in control, reduce the user’s memory load, make the interface consistent.'],
                 exam=[mcq('Which is one of Mandel’s golden rules?', ['Reduce the user’s memory load', 'Hide all feedback', 'Use as many colours as possible', 'Make every screen different'], 0, '')], weight=3),
    }


class construction:
    AUTO_SLIDES = True
    DECK = deck('d08', 'Software Construction (Implementation)', 'Chapter 7',
                'Construction activities and fundamentals: minimizing complexity, anticipating change, constructing for '
                'verification, standards, reuse and open-source software.')
    ANN = {
        2: dict(notes=['Construction: detailed creation of working software through coding, verification, unit testing, integration testing and debugging.']),
        4: dict(notes=['Fundamentals: minimize complexity, anticipate change, construct for verification, reuse, use standards.']),
        5: dict(notes=['Minimize complexity: simple readable code, coding standards, modular design.']),
        6: dict(notes=['Anticipate change: design so future modifications are easy (parameters, encapsulation).']),
        8: dict(notes=['Standards: communication methods, programming languages, coding standards, platforms, tools.']),
        9: dict(notes=['Reuse levels: abstraction, object, component, system. Costs: finding, understanding and adapting the components.'],
                exam=[mcq('Reusing a whole application system configured for a new client is reuse at the:', ['System level', 'Object level', 'Abstraction level', 'Component level'], 0, '')], weight=2),
        11: dict(notes=['Open source: source code is published and volunteers can contribute; licences: GPL (reciprocal), LGPL, BSD (non-reciprocal).'],
                 exam=[mcq('Which licence requires derived works to be released under the same licence?', ['GPL', 'BSD', 'MIT', 'Apache'], 0, '')], weight=3),
    }


class testing:
    AUTO_SLIDES = True
    DECK = deck('d09', 'Software Testing', 'Chapter 8',
                'What testing is, black-box testing (decision tables, equivalence partitioning, boundary-value '
                'analysis), white-box basis path testing with flow graphs and cyclomatic complexity, unit and '
                'integration testing (top-down, bottom-up, stubs and drivers), system, non-functional, acceptance and '
                'regression testing.')
    ANN = {
        6: dict(notes=['Testing: running a program to find defects before it is put into use. It shows the presence of bugs, not their absence.']),
        9: dict(notes=['Black-box: test from the specification without looking at the code.']),
        14: dict(notes=['Decision table: conditions × actions; each column is a rule → one test case. n binary conditions → up to 2ⁿ rules.'],
                 exam=[mcq('How many rules does a full decision table with 3 binary conditions have?', ['8', '6', '3', '9'], 0, '2³.')], weight=3),
        20: dict(notes=['Equivalence partitioning: divide inputs into classes that behave the same; test one value from each (valid and invalid).'],
                 exam=[mcq('Valid ages are 18–60. How many equivalence classes?', ['3 (below, inside, above)', '2', '1', '60'], 0, '')], weight=3),
        24: dict(notes=['Boundary value analysis: test at and around the edges: min−1, min, min+1, max−1, max, max+1.'],
                 exam=[mcq('Valid range 1–100. Which set is BVA?', ['0, 1, 2, 99, 100, 101', '1, 50, 100', '−1, 0, 101', '25, 50, 75'], 0, '')], weight=3),
        32: dict(notes=['Basis path testing (white-box): draw the flow graph, compute cyclomatic complexity, find independent paths, design one test per path.']),
        38: dict(notes=['Cyclomatic complexity V(G) = E − N + 2 = P + 1 (P = predicate/decision nodes) = number of regions. It is the number of independent paths.'],
                 tips=[tip('V(G) = E − N + 2 = decisions + 1 = regions.')],
                 exam=[mcq('A flow graph has 9 edges and 7 nodes. V(G) =', ['4', '2', '16', '3'], 0, '9 − 7 + 2.'),
                       mcq('A function with 3 if-statements (no loops) has V(G) =', ['4', '3', '2', '6'], 0, '')], weight=3),
        50: dict(notes=['Unit testing: test individual components (methods, classes) in isolation, usually by developers.']),
        55: dict(notes=['Integration testing: test the interfaces between combined units.']),
        63: dict(notes=['Stub: a dummy CALLED module (replaces a lower module in top-down integration). Driver: a dummy CALLING module (replaces an upper module in bottom-up).'],
                 tips=[trick('Top-down needs Stubs; Bottom-up needs Drivers.')],
                 exam=[mcq('Top-down integration testing needs:', ['Stubs', 'Drivers', 'Neither', 'Only system tests'], 0, '')], weight=3),
        67: dict(notes=['System testing: test the complete integrated system against requirements (functional and non-functional: performance, load, stress, security, usability).']),
        73: dict(notes=['Acceptance testing: customers test with their data to decide whether to accept the system (alpha: at the developer’s site; beta: at users’ sites).'],
                 exam=[mcq('Testing by real users at their own sites before release is:', ['Beta testing', 'Alpha testing', 'Unit testing', 'Integration testing'], 0, '')], weight=3),
        74: dict(notes=['Regression testing: re-run tests after changes to make sure nothing that worked is now broken.']),
    }


DECKS_HERE = [practices, processes, agile, project_management, requirements, modeling, design, construction, testing]

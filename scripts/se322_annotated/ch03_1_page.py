"""SE322 Chapter 3, Lecture 1 (Quality Attributes): page content for the annotated deck.

Schema: see annotated_page.py. Marks with a 4th element 'ocr' are labels inside pictures (skipped if OCR can't
read them). Past-exam questions are copied from the papers in exams/; everything else is a prediction.
"""
from .common import asked, likely

TITLE = 'Quality Attributes: Scenarios, Tactics and Design Decisions'
CHAPTER = 'SE322 · Chapter 3 · Lecture 1'

OVERVIEW = {
    'summary': ('Functional requirements say what the system does; quality attributes say how well it does it, and the '
                'plan for meeting them lives in the architecture. Because quality words are vague and overlap (is a '
                'denial-of-service attack an availability, performance or security problem?), qualities are pinned down '
                'with quality attribute scenarios: six parts from source to response measure. Tactics are the design '
                'techniques that achieve a scenario’s response, and the lecture ends with the seven categories of design '
                'decision through which an architect shapes quality.'),
    'ideas': [
        ('QA vs. functional', 'Functional = what the system shall do (planned in detailed design). Quality = criteria for judging the system as a whole (planned in the architecture).'),
        ('Six-part scenario', 'Source, stimulus, environment, artifact, response, response measure. The measure is what makes it testable.'),
        ('Tactics', 'Primitive, proven design techniques that control a quality attribute response (redundancy, caching…).'),
        ('Seven decision types', 'Responsibilities, coordination, data model, resources, binding time, technology, mapping.'),
    ],
    'sections': [
        ('Slides 1–5', 'Architecture and requirements: functional vs. quality, who cares about which quality'),
        ('Slides 6–12', 'Quality attribute considerations and scenarios, with three worked examples'),
        ('Slides 13–14', 'Tactics'),
        ('Slides 15–18', 'The seven categories of quality design decisions'),
    ],
    'exam': ('Scenarios are the most examined idea in SE322. Quiz 1 261 had six matching questions on scenario parts '
             '(one on the definitions, five on usability, performance, availability, testability and security examples), '
             'Midterm 261 Q10 (3 marks) asked for the six parts of an online-voting scenario, Midterm 252 Q5 asked for an '
             'availability scenario, and Final 252 Q3-2 asked you to construct a general availability scenario.'),
}

TITLES = {10: 'Quality Attribute Scenarios: a performance example', 11: 'Quality Attribute Scenarios: a maintainability example',
          16: 'Extra: Quality Design Decisions explained', 17: 'Extra: Quality Design Decisions explained (cont.)'}

SCENARIO_PARTS = ('**Source**: who or what generates the stimulus. **Stimulus**: the event or condition that arrives. '
                  '**Environment**: the conditions the system is in when it arrives. **Artifact**: the part of the system that is '
                  'stimulated. **Response**: what the system does. **Response measure**: how the response is measured, so the requirement can be tested.')

SLIDES = {
    1: dict(
        hl=[('[Quality Attributes]', 1)],
        notes=['Chapter 3 is about **quality attributes**, the non-functional requirements that architecture exists to satisfy. Lecture 1 gives the tools (scenarios, tactics, design decisions); Lecture 2 applies them to six major qualities.']),
    2: dict(
        hl=[('Architecture and Requirements', 1), ('Quality Attribute Considerations', 2), ('Quality Design Decisions', 3), ('Major Quality Attributes', 4)],
        notes=['First, how functional and quality requirements relate to architecture.',
               'Then how qualities are specified precisely (scenarios) and achieved (tactics).',
               'Then the categories of design decisions that affect quality.',
               'The six major quality attributes themselves come in Lecture 2.']),
    3: dict(
        hl=[('Functional requirements:', 1), ('system shall do', 1), ('detailed design', 2), ('Non-functional requirements or Quality attributes (QA)', 3),
            ('as a whole', 3), ('system architecture', 4)],
        notes=['**Functional requirements** state what the system must do, usually written as “the system shall …”. Each defines a specific behaviour or function.',
               'The plan for implementing functional requirements is produced in the **detailed design**.',
               '**Non-functional requirements**, also called **quality attributes (QA)**, are criteria for judging how the system operates **as a whole**, not a specific behaviour: speed, reliability, security…',
               'The plan for implementing them is detailed in the **architecture**. That split (functions → detailed design, qualities → architecture) is the reason architecture spends so much effort on quality.'],
        exam=[asked('q261', 'Q14 (true/false)', 'Software architecture is concerned only with functional structure and does not need to consider non-functional requirements.',
                    tf=False, why='Architecture must address important quality attributes such as performance, security and availability; their plan lives in the architecture.')]),
    4: dict(
        hl=[('design,', 1), ('implementation, and deployment', 1), ('unable to achieve qualities', 2), ('foundation', 2)],
        notes=['Quality has to be considered in **every phase**: design, implementation and deployment. A fast architecture can still be ruined by slow code or a badly configured server.',
               'Architecture **cannot achieve qualities on its own**. It provides the **foundation**, but the foundation is useless if the details in later phases are ignored (the same point as Chapter 2: architecture alone cannot guarantee quality).']),
    5: dict(
        hl=[('variety of system stakeholders', 1), ('their own opinion', 2), ('maintainability', 3), ('testability', 3), ('end user', 4)],
        notes=['Architecture documents are read by many stakeholders: developers, managers, sales, testers, support, maintenance staff and customers.',
               'Each has **their own opinion** about which quality matters most, so the architect has to weigh them against each other.',
               'The development team cares about **maintainability** (easy to change) more than the customer does; the QA team cares about **testability**.',
               'The **end user** (the slide’s question) mostly cares about qualities they can feel: usability, performance and availability.'],
        exam=[likely('Which quality attribute is the QA (testing) team most likely to prioritise, and which the development team?',
                     a='QA: testability. Development team: maintainability (modifiability).')]),
    6: dict(
        hl=[('constraints on the manner', 1), ('criteria for evaluating', 2), ('green', 3), ('performance QA', 4), ('availability QA', 4), ('usability QA', 4)],
        notes=['Quality attributes are **constraints on the manner** in which the system implements and delivers its functionality: they say *how* a function must be achieved, not *what* it is.',
               'They are used as **criteria** to evaluate the system during and after development: efficiency, availability, scalability, adaptability, security, dependability…',
               'Take one functional requirement: “when the user presses the **green** button, the Options dialog appears”. The function is the same in every case below; only the quality constraint changes.',
               'A **performance** QA says how quickly the dialog appears; an **availability** QA says how often this function may fail; a **usability** QA says how easy the function is to learn.'],
        exam=[likely('For the requirement “when the user presses the green button the Options dialog appears”, write one performance and one usability quality requirement.',
                     a='Performance: the dialog appears within 0.5 seconds of the press. Usability: a first-time user can find and open the dialog without help in under 10 seconds.')]),
    7: dict(
        hl=[('unstable definition', 1), ('denial of service attack', 2), ('quality attribute scenarios', 3), ('payment server crashes', 4)],
        notes=['Quality attribute words have **unstable definitions** and **overlapping concerns**: people mean different things by “reliable” or “secure”.',
               'The DoS example shows the overlap: a denial-of-service attack makes the system down (availability), very slow (performance), is an attack (security) and stops users reaching the service (usability). Which quality does it “belong” to?',
               'The solution is to characterise qualities with **quality attribute scenarios**: concrete stories with a stimulus, a response and a measure, instead of vague words.',
               'Real example: if the payment server **crashes during a transaction** (stimulus), the system switches to a backup within 2 seconds (response), keeping 99.99% uptime (measure). That is clear, testable and no longer overlaps with other qualities.']),
    8: dict(
        hl=[('Stimulus – a condition', 1), ('Source of stimulus', 2), ('Environment - what are the conditions', 3), ('Artifact – what elements', 4),
            ('Response – the activity', 5), ('Response measure – when the response', 6)],
        notes=['**Stimulus**: a condition that needs to be considered when it arrives at the system: a request, a failure, an attack, a change request.',
               '**Source of stimulus**: the entity that generates it: a human, another computer system, an internal component.',
               '**Environment**: the conditions the system is in when the stimulus occurs: normal operation, overload, start-up, maintenance.',
               '**Artifact**: the element of the system that is stimulated: the whole system, a database, a server, the UI, the code.',
               '**Response**: the activity the system undertakes after the stimulus arrives: process it, log it, fail over, deny access.',
               '**Response measure**: the response must be **measurable**, so the requirement can be tested: response time under 2 seconds, 99% uptime, repair within 30 minutes. A scenario without a measure is not testable.'],
        exam=[asked('q261', 'Q22 (matching)', 'Match each quality attribute scenario element with its meaning: source, stimulus, artifact, environment, response, response measure.',
                    a='Source → **entity that generates the stimulus**. Stimulus → **event or condition that affects the system**. Artifact → **system element affected by the stimulus**. Environment → **condition under which the stimulus occurs**. Response → **what the system does after the stimulus**. Response measure → **measurable criterion used to evaluate the response**.')]),
    9: dict(
        hl=[('(source)', 1), ('(stimulis)', 1), ('artefact', 1), ('(environment)', 1), ('(response)', 1), ('(response measure)', 1)],
        notes=['The one-sentence template: some **source** generates some event (**stimulus**) that arrives at some **artifact** under some conditions (**environment**) and must be dealt with (**response**) in a satisfactory way (**response measure**). Write any scenario by filling these six slots in this order. ' + SCENARIO_PARTS],
        exam=[asked('m261', 'Q10 · 3 marks', 'Online Voting System: “During an election, thousands of eligible voters access the Online Voting System to submit their votes. While the system is operating under heavy election-day traffic, a voter submits a vote for a selected candidate. The system must validate the voter, securely record the vote, prevent duplicate voting, and display a confirmation message. The complete voting transaction must be processed within 4 seconds for at least 95% of voting requests.” Identify the six elements of the quality attribute scenario.',
                    a='**Source**: eligible voters. **Stimulus**: submitting a vote for a selected candidate. **Environment**: heavy election-day traffic. **Artifact**: the Online Voting System. **Response**: validate the voter, securely record the vote, prevent duplicate voting and display a confirmation. **Response measure**: processed within 4 seconds for at least 95% of voting requests.'),
              asked('q261', 'Q24 (matching)', 'Performance scenario: “During peak registration time, an enrolled student submits a course search request to the university registration system. The system processes the request and displays matching course sections. The search results must be displayed within 2 seconds for at least 95% of requests.” Match the six elements.',
                    a='Source: enrolled student. Stimulus: submits a course search request. Artifact: university registration system. Environment: peak registration time. Response: processes the request and displays matching course sections. Response measure: results displayed within 2 seconds for at least 95% of requests.')]),
    10: dict(
        hl=[('A Performance Scenario Example', 1), ('Source:', 2, 0, 'ocr'), ('Stimulus:', 2, 0, 'ocr'), ('Artifact:', 2, 0, 'ocr'),
            ('Environment:', 2, 0, 'ocr'), ('Response:', 3, 0, 'ocr'), ('Measure:', 3, 0, 'ocr')],
        notes=['A **performance** scenario drawn as a picture. Read it left to right, like the template on slide 9.',
               '**Source**: users. **Stimulus**: they initiate transactions (the handwritten note gives “orders” as an example). **Artifact**: the system. **Environment**: under normal operations.',
               '**Response**: the transactions are processed. **Response measure**: with an average latency of two seconds. The measure is what turns “the system should be fast” into a requirement you can test.'],
        exam=[likely('In the performance scenario on this slide, which part is “with average latency of two seconds”?',
                     a=0, opts=['Response measure', 'Response', 'Environment', 'Stimulus'])]),
    11: dict(
        hl=[('A maintainability Scenario Example', 1), ('Developer', 2, 0, 'ocr'), ('Code', 2, 0, 'ocr'), ('No Side Effects', 3, 0, 'ocr')],
        notes=['A **maintainability** (modifiability) scenario. Here the “stimulus” is not a failure or a request but a wish to change the system.',
               '**Source**: a developer. **Stimulus**: wishes to change the UI. **Artifact**: the code. **Environment**: at design time (not while the system runs).',
               '**Response**: the modification is made with no side effects. **Response measure**: in three hours. If the UI is well separated from the rest of the code, the change stays small and the measure is met.'],
        exam=[likely('Write a modifiability scenario in which a developer must add a new payment method.',
                     a='Source: developer. Stimulus: needs to add a new payment method. Artifact: the payment module code. Environment: design/development time. Response: the method is added and tested without changing other modules (no side effects). Measure: within 2 person-days, touching no more than one module.')]),
    12: dict(
        hl=[('General Availability Scenario', 1), ('Source', 2), ('Stimulus', 3), ('Crash', 3), ('Omission', 3)],
        notes=['A **general** scenario lists the *possible* values of each part for one quality (here availability). A concrete scenario then picks one value per part.',
               '**Source**: internal to the system (a software bug, a memory leak) or external (a power outage, a hacking attempt).',
               '**Stimulus** (the fault): **crash** (sudden failure), **omission** (no response when one was expected), **timing** (response at the wrong time), no response, or an incorrect response.',
               {'text': 'The rest of the picture:', 'items': [
                   ('Artifact', 'The system’s processors, communication channels or persistent storage.'),
                   ('Environment', 'Normal operation, start-up, shutdown, repair mode, degraded (fail-safe) mode, overloaded operation.'),
                   ('Response', 'Prevent the failure, log it, notify users or operators, disable the source of the failure, or be temporarily unavailable.'),
                   ('Measure', 'Time interval available, availability %, detection time, repair time, degraded-mode time interval, unavailability time.')]},
               'The handwritten notes show one concrete pick: hardware failure → primary server crash → normal operation → switch to a backup server → restored in 30 seconds.'],
        exam=[asked('f252', 'Q3-2 · 2 marks', 'Construct one quality attribute general scenario for availability.',
                    a='**Source**: heartbeat monitor (internal to the system). **Stimulus**: a server becomes unresponsive (crash/omission). **Environment**: normal operation. **Artifact**: the server process. **Response**: detect the fault, notify the operator, disable the failed source and switch to the backup, then repair it. **Response measure**: failover within 3 seconds; repair time under 30 minutes; 99.9% availability. All six parts with a measurable response measure earn the marks.'),
              asked('q261', 'Q25 (matching)', 'Availability scenario: “A monitoring service detects that the primary application server has stopped responding during normal operation. The system redirects requests to a standby server and restores service within 30 seconds with no more than 0.1% failed requests.” Match the six elements.',
                    a='Source: monitoring service. Stimulus: detects the primary application server has stopped responding. Artifact: application service/server infrastructure. Environment: normal operation. Response: redirects requests to a standby server and restores service. Response measure: restored within 30 seconds with no more than 0.1% failed requests.')]),
    13: dict(
        hl=[('primitive design techniques', 1), ('primitives tactics', 2), ('like design patterns', 3)],
        notes=['Architects have a collection of **primitive design techniques** for achieving a quality attribute response.',
               'These architectural design primitives are called **tactics**. A tactic targets one quality response (Chapter 2: a tactic is a design decision that controls a quality attribute response).',
               'Like design patterns, tactics are proven techniques experienced architects have used for years; we capture them and apply them. Lecture 2 lists tactics for each major quality.']),
    14: dict(
        hl=[('Redundancy', 1), ('multiple instances of critical components', 1), ('Caching', 2), ('frequently accessed data', 2)],
        notes=['**Redundancy** (availability): run multiple instances of critical components so that if one fails another takes over. Stimulus: hardware failure or network outage. Response: automatic failover to the backup.',
               '**Caching** (performance): keep frequently accessed data in fast temporary storage. Stimulus: many read requests. Response: serve from the cache instead of fetching from primary storage, which cuts response time and load.'],
        exam=[likely('Keeping several instances of a critical component so that another takes over when one fails is a tactic for:',
                     a=0, opts=['Availability', 'Usability', 'Testability', 'Modifiability'])]),
    15: dict(
        hl=[('systematic approach to making design decisions', 1), ('Allocation of system responsibilities', 2), ('Coordination model', 2), ('Data model', 2),
            ('Management of resources', 3), ('Binding time decisions', 3), ('Choice of technology', 3), ('Mapping among architectural elements', 3)],
        notes=['Architecture design is a **systematic** way of making design decisions, and every quality is achieved through them. They fall into seven categories.',
               'The first three are about the system’s parts: **allocation of responsibilities** (which element does which function), the **coordination model** (how elements interact) and the **data model** (data abstractions, their operations and properties).',
               'The last four: **management of resources**, **binding time** (how and when elements are bound), **choice of technology**, and **mapping** among elements (modules to run-time elements). Slides 16–17 give an example of each.'],
        exam=[likely('List the seven categories of quality design decisions.',
                     a='Allocation of responsibilities, coordination model, data model, management of resources, binding time decisions, choice of technology, mapping among architectural elements.')]),
    16: dict(
        hl=[('Allocation of System Responsibilities', 1), ('Coordination Model', 2), ('Data Model', 3)],
        notes=['**Allocation of responsibilities**: deciding which part handles which task. In a shopping app, one part handles logins, another the cart, another payments.',
               '**Coordination model**: how the parts communicate and work together, e.g. how the payment system tells the inventory system an item was bought (direct call? event? message queue?).',
               '**Data model**: which data the system uses, how it is organised and accessed, e.g. a Customer object with name, address and order history.']),
    17: dict(
        hl=[('Management of Resources', 1), ('Mapping among Architectural Elements', 2), ('Binding Time Decisions', 3), ('Choice of Technology', 4)],
        notes=['**Management of resources**: how memory, CPU time and network bandwidth are used and allocated, e.g. making sure there is enough server capacity during peak traffic (a performance decision).',
               '**Mapping**: how code modules correspond to run-time elements (processes, tasks), e.g. which services run when the UI module is used.',
               '**Binding time**: *when* something is fixed: at compile time, installation, start-up or run time. Example: is the user’s language chosen at installation or switchable at run time? Later binding gives flexibility (modifiability) at some cost (performance, complexity).',
               '**Choice of technology**: languages, databases, platforms, e.g. Python on the server, PostgreSQL, AWS hosting.'],
        exam=[likely('Deciding whether a user’s language is set at installation or can change at run time is which kind of design decision?',
                     a=0, opts=['Binding time decision', 'Coordination model', 'Data model', 'Management of resources'])]),
    18: dict(
        hl=[('Next … Major Quality Attributes', 1)],
        notes=['Next lecture: the major quality attributes one by one (availability, performance, security, modifiability, testability, usability…), each with its general scenario and tactics. Practise writing one six-part scenario for each.']),
}

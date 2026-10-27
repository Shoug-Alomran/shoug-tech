"""SE322 Chapter 2, Lecture 3 (Designing the Architecture with the 4+1 View Model): page content.

Schema: see annotated_page.py. Marks with a 4th element 'ocr' are labels inside the ATM pictures (found by OCR,
skipped if OCR can't read them). Past-exam questions are copied from the papers in exams/; everything else is a
prediction.
"""
from .common import asked, likely

TITLE = 'Designing the Architecture with the 4+1 View Model'
CHAPTER = 'SE322 · Chapter 2 · Lecture 3'

OVERVIEW = {
    'summary': ('No single diagram can describe a whole architecture, so Kruchten’s 4+1 model splits the description '
                'into four views (logical, process, development, physical), each answering one stakeholder group’s '
                'questions with its own UML diagrams, plus the scenario (user) view whose use cases tie the four together '
                'and validate them. Each view is illustrated with the same ATM system, so the lecture is also a tour of '
                'how to read a class, communication, sequence, activity, component, deployment and use case diagram.'),
    'ideas': [
        ('Logical', 'What the system does: classes and objects and their relationships. Functional requirements. Class, object, sequence, communication and state diagrams.'),
        ('Process', 'How it runs: processes, threads, concurrency and synchronisation. Performance and scalability. Activity diagrams.'),
        ('Development', 'How the code is organised: modules, packages, libraries. Package and component diagrams.'),
        ('Physical + scenarios', 'Physical: which software runs on which hardware (deployment diagram). +1: use cases that drive and validate the other four.'),
    ],
    'sections': [
        ('Slides 1–4', 'Why several views, and the 4+1 model'),
        ('Slides 5–8', 'Logical view with ATM class, communication and sequence diagrams'),
        ('Slides 9–10', 'Process view with the ATM activity diagram'),
        ('Slides 11–12', 'Development view with the ATM component diagram'),
        ('Slides 13–14', 'Physical view with the ATM deployment diagram'),
        ('Slides 15–16', 'User (scenario) view with the ATM use case diagram'),
        ('Slides 17–19', 'Summary table'),
    ],
    'exam': ('The 4+1 model is examined every term. Midterm 252 asked which view evaluates scalability and performance '
             '(the process view) and had a whole question filling in the view table (description, stakeholders, UML). '
             'Quiz 1 261 asked five questions on the views (logical, development, process, physical, and a matching), '
             'and Midterm 261 asked whether the “+1” is the database (false: it is the scenarios).'),
}

TITLES = {17: 'Extra: The 4+1 views at a glance', 18: 'The 4+1 View Model (Summary)'}

SLIDES = {
    1: dict(
        hl=[('[Software Architecture]', 1)],
        notes=['Third architecture lecture. Lecture 1 said an architecture needs several views; this one names the standard set of views and shows each on one example system, an ATM.']),
    2: dict(
        hl=[('4+1view model', 1), ('Plus … The user view', 2)],
        notes=['The four views are logical, process, development and physical.',
               'The “+1” is the user view, also called the scenario view. It is not a fifth independent description but the use cases that connect and check the other four.']),
    3: dict(
        hl=[('no single', 1), ('collection of different views', 2), ('partial representation', 3), ('4+1 view model', 4)],
        notes=['No single view can present every aspect of a system. A class diagram says nothing about servers; a deployment diagram says nothing about classes.',
               'So designers organise their architectural decisions as a **collection of views**. This breaks a complex system into understandable perspectives and manages complexity.',
               'Each view is a **partial representation** aimed at specific stakeholders (users, analysts, developers…), so every group gets the view that answers its own concerns.',
               'The best-known way to organise those views is the **4+1 view model**.'],
        exam=[asked('m252', 'Q1 MCQ 2', 'Why are multiple architectural views required in complex systems?',
                    a=1, opts=['To reduce documentation effort', 'Because no single view can represent all system aspects for all stakeholders',
                               'To replace requirements engineering', 'To simplify coding'])]),
    4: dict(
        hl=[('Philippe Kruchten', 1), ('1995', 1), ('four essential', 2), ('several use cases', 3)],
        notes=['The model was introduced by **Philippe Kruchten in 1995**.',
               'It has **four essential views**: logical, process, physical and development. Each one has its own stakeholders, concerns and diagrams.',
               'To keep the four **consistent** with one another, the user’s perspective is captured in use cases that form the user view. Running a use case through every view checks that they all describe the same system.'],
        exam=[likely('Who introduced the 4+1 view model, and what is the role of the “+1” view?',
                     a='Philippe Kruchten (1995). The +1 is the user (scenario) view: use cases that tie the four views together, help discover architectural elements and validate the design.')]),
    5: dict(
        hl=[('conceptual entities', 1), ('abstraction of the system\'s functional', 2), ('Static diagrams', 3), ('Dynamic diagrams', 3),
            ('end-users, analysts, and', 4)],
        notes=['The **logical view** decomposes the system into conceptual entities (objects or classes) and the connections between them.',
               'It is an abstraction of the **functional requirements**: it shows what the system does, in terms of the things it is made of.',
               'Diagrams: **static** ones (class and object diagrams) for structure, and **dynamic** ones (interaction overview, sequence, communication, state and activity diagrams) for how those objects behave together.',
               'Its stakeholders are **end users, analysts and designers**, the people who care about functionality.'],
        exam=[asked('q261', 'Q17 (fill in)', 'Fill in the blank: The 4+1 view that emphasizes the major functional elements of the system and their relationships is the ___ view.',
                    a='**Logical** view.')]),
    6: dict(
        hl=[('Class diagrams', 1), ('Directionality', 2), ('Arrow from Subclass to Superclass', 3), ('Names above arrows', 4), ('Multiplicities', 5),
            ('Maintains', 4, 0, 'ocr'), ('Current Account', 3, 0, 'ocr'), ('Withdrawl Transaction', 3, 0, 'ocr')],
        notes=['A **class diagram** shows the classes, their attributes and operations, and the relationships between them. For the ATM: Bank, ATM Info, Customer, Debit Card, Account and ATM Transaction, each box listing attributes (`+code`, `+address`) and operations (`+manages()`).',
               '**Directionality**: the arrow from ATM Transaction to Account (“Modifies”) means the transaction acts on the account, and not the other way round. A bidirectional association has two arrowheads or none.',
               '**Inheritance**: the lines ending in a hollow triangle point from subclass to superclass. Current Account and Saving Account are kinds of Account; Withdrawal, Query, Transfer and PIN-validation transactions are kinds of ATM Transaction.',
               '**Association names** describe the relationship in words: Bank *Maintains* ATM Info, Customer *Owns* Account, Debit Card *Provides Access to* Account.',
               '**Multiplicities** give how many objects take part: `1` means exactly one, `1..*` one or more. One Bank maintains one or more ATMs.'],
        exam=[likely('In the ATM class diagram, what do the hollow triangles from Current Account and Saving Account to Account mean, and how is “1..*” read?',
                     a='Inheritance (generalisation): Current Account and Saving Account are specialised kinds of Account. “1..*” is a multiplicity meaning one or more.')]),
    7: dict(
        hl=[('Bank Client:', 1), ('ATM Machine', 1), ('inserts card', 2), ('Collaboration diagram', 3)],
        notes=['The **communication (collaboration) diagram** shows the objects that cooperate in one scenario (Bank Client, ATM Machine, Account, Checking Account) as boxes joined by links.',
               {'text': 'Messages are written along the links with a number that gives their order. Reading the withdrawal scenario:', 'items': [
                   ('1–4', 'The ATM asks for the transaction kind and amount; the client enters them.'),
                   ('5–8', 'The ATM asks Account to process the transaction; Account withdraws from the Checking Account and reports success.'),
                   ('9–14', 'The ATM dispenses cash, the client takes it, the ATM asks whether to continue, the session ends and a receipt is printed.')]},
               'It focuses on **who talks to whom**. The same messages appear on the next slide as a sequence diagram, which focuses on **when**.'],
        exam=[likely('How does a communication (collaboration) diagram differ from a sequence diagram?',
                     a='Both show objects exchanging messages. A communication diagram emphasises the links between objects and shows order only through message numbers; a sequence diagram lays messages out top to bottom along lifelines, so the time order is the main thing shown.')]),
    8: dict(
        hl=[('Sequence diagram', 1), ('time-order', 1), ('Class Diagram (Structure)', 2), ('Sequence Diagram (Behavior)', 2), ('who does what', 3)],
        notes=['A **sequence diagram** models the interactions between design units, the messages they exchange, and the **time order** of those messages.',
               {'text': 'How to read it:', 'items': [
                   ('Boxes along the top', 'The participants: `C : customer`, `A : ATM`, `Accnt : Account`, and later `CKA : Checking Account` (object name : class).'),
                   ('Dashed vertical lines', 'Lifelines. Time runs downward.'),
                   ('Thin rectangles', 'Activations: the period when that object is busy handling a message.'),
                   ('Numbered arrows', 'Messages in order: 1 insert card, 2 request PIN, 3 PIN entered, 4 verify PIN, 5 PIN OK … 11 withdraw from checking, 13 transaction successful, 14 dispense cash … 19 print receipt.')]},
               'The class diagram (slide 6) gives the **structure**; the sequence diagram gives the **behaviour over time** for one use case, making clear who does what and in which order.'],
        exam=[likely('Which logical-view diagram should you use to show the time order of the messages exchanged during an ATM withdrawal?',
                     a=0, opts=['Sequence diagram', 'Class diagram', 'Deployment diagram', 'Package diagram'])]),
    9: dict(
        hl=[('dynamic aspects', 1), ('processes or threads', 2), ('synchronization and concurrency', 2), ('scalability and performance', 3),
            ('activity diagram', 4), ('developers and', 5)],
        notes=['The **process view** covers the dynamic, run-time behaviour of the system.',
               'It is an abstraction of the **processes and threads** and shows their **concurrency** (what runs at the same time) and **synchronisation** (how they share resources and data without interfering).',
               'It contributes to non-functional requirements such as **scalability and performance**, which depend on how work is spread across processes.',
               'UML support: the **activity diagram** and the interaction overview diagram.',
               'Stakeholders: **developers and integrators**, who put the running pieces together.'],
        exam=[asked('m252', 'Q1 MCQ 3', 'Which architectural view mainly contributes to evaluating scalability and performance?',
                    a=2, opts=['Logical view', 'Development view', 'Process view', 'User view'],
                    why='The process view covers runtime processes, concurrency and communication, from which performance and scalability are judged. (The physical view also concerns performance, through hardware; when the options include the process view and the question is about runtime behaviour, choose process.)'),
              asked('q261', 'Q19', 'Which 4+1 view should an architect emphasize when analyzing concurrent execution, communication among running processes, and synchronization?',
                    a=3, opts=['Development view', 'Scenario view', 'Logical view', 'Process view'])]),
    10: dict(
        hl=[('Activity diagram', 1), ('flow the', 1)],
        notes=['An **activity diagram** describes the flow of the system: its operations and processes, in order, with decisions and parallel paths.',
               {'text': 'Reading the ATM diagram (three swimlanes: customer, ATM machine, bank):', 'items': [
                   ('Filled circle', 'Start. The customer inserts the card and the ATM validates it.'),
                   ('Diamonds', 'Decisions: an invalid card is ejected; the PIN is authorised (valid/invalid); the balance is checked against the amount.'),
                   ('Thick bars', 'Fork and join: “take money from slot” and “debit account” happen in parallel, then join. This parallelism is exactly what the process view is about.'),
                   ('Circle with ring', 'End, after the balance is shown and the card is ejected and taken.')]}]),
    11: dict(
        hl=[('static organization', 1), ('class library, sub-system, or packages', 2), ('package diagrams and component diagrams', 3),
            ('physical files and directories', 4), ('programmers and software project manager', 5)],
        notes=['The **development view** describes the static organisation of the software modules, from the implementation point of view: how the source code is arranged.',
               'Modules here are building blocks that group classes: class libraries, subsystems, packages.',
               'UML support: **package diagrams** and **component diagrams**.',
               'It lets you analyse how logical components map onto **physical files and directories**, which matters for builds, reuse and team ownership.',
               'Stakeholders: **programmers and software project managers** (who assign modules to teams).'],
        exam=[asked('q261', 'Q18 (fill in)', 'Fill in the blank: The 4+1 view that focuses on the organization of source-code modules, packages, and development units is the ___ view.',
                    a='**Development** view (also accepted: implementation).')]),
    12: dict(
        hl=[('Component diagram:', 1), ('Full banking system', 2), ('Bank Database', 2, 0, 'ocr'), ('Account Information', 3, 0, 'ocr')],
        notes=['A **component diagram** shows the system’s components with their interfaces, ports and the relationships between them.',
               {'text': 'Reading the banking system:', 'items': [
                   ('Rectangles with two small tabs', 'Components: ATM Machine, Customer Console, Card Reader, Bank Database, Web Page, Client Desktop, Employee Console.'),
                   ('Dashed arrows into Bank Database', 'Dependencies: the ATM, card reader, web page and client desktop all depend on the database.'),
                   ('Small circles (lollipops)', 'Provided interfaces, e.g. ATM Transaction, Account Information, Online Transaction, Web Merchant Transaction.')]},
               'Reading tip: a circle attached to a component is an interface it **provides**. In the development view these components are units of code that teams build and package separately.']),
    13: dict(
        hl=[('deployment aspects', 1), ('Deployment diagrams', 2), ('Availability', 3), ('Performance and scalability', 3), ('Security', 3),
            ('system installers, system administrators', 4)],
        notes=['The **physical view** represents deployment: how the software is configured and installed on hardware.',
               'UML support: **deployment diagrams**.',
               'It is the right view to evaluate **availability** (redundant nodes), **performance and scalability** (processor speed, bandwidth) and **security** (firewalls), because all of these depend on the hardware layout.',
               'Stakeholders: **system installers, system administrators and system engineers**.'],
        exam=[asked('q261', 'Q20', 'A deployment engineer wants to know which software elements run on which servers and hardware nodes. Which 4+1 view is most useful?',
                    a=3, opts=['Process view', 'Development view', 'Logical view', 'Physical view'])]),
    14: dict(
        hl=[('Deployment diagram:', 1), ('ATM_Machine', 2, 0, 'ocr'), ('Bank_Database', 2, 0, 'ocr')],
        notes=['A **deployment diagram** models the physical structure the software runs on.',
               'The 3-D boxes are **nodes** (hardware or execution environments): ATM_Machine, Customer Console, Card_Reader, Bank_Database, Web_Page, Client_Desktop, Employee_Console. The lines are communication paths. Most nodes connect to Bank_Database, so it is the node whose failure takes everything down, which is where you would add redundancy for availability.']),
    15: dict(
        hl=[('scenario view', 1), ('foundation for other 4 views', 2), ('discover architectural elements', 3), ('validate the architectural design', 3),
            ('consistent', 4)],
        notes=['The **user (scenario) view** describes the system’s functionality as the user experiences it: how users use the system and what services it provides them.',
               'It provides the **foundation** for the other four views and lets them work together logically: every view has to support the same use cases.',
               'It is used twice: to **discover** architectural elements during design (what does this scenario need?) and to **validate** the design afterwards (walk the scenario through each view).',
               'So it keeps the architecture **consistent** and validated against both functional and non-functional requirements.'],
        exam=[asked('m261', 'Q8 (true/false)', 'The “+1” view represents the database structure of the system.',
                    tf=False, why='The +1 is the scenario (use case) view that illustrates and validates the other four; the database is not a view of its own.')]),
    16: dict(
        hl=[('Use case diagram:', 1), ('Bank ATM Transaction', 2, 0, 'ocr'), ('Approval process', 3, 0, 'ocr')],
        notes=['A **use case diagram** is a behavioural diagram that captures, specifies and visualises the required system behaviour from the user’s side.',
               'The stick figure is the actor, **Bank Client**. The ovals are use cases: Bank ATM Transaction, Checking Tran, Saving Transaction History, Deposit Amount, Withdrawal Amount, Approval process, Invalid pin.',
               '**«uses»** (include): Bank ATM Transaction always uses the Approval process. **«extends»**: optional or special-case behaviour added to a base use case, e.g. Deposit and Withdrawal extend the transaction, and Invalid pin extends the approval process.']),
    17: dict(
        hl=[('Logical View', 1), ('Process View', 2), ('Development View', 3), ('Physical View', 4), ('User (Scenario) View', 5)],
        notes=['**Logical**: what the system should do, the functionality for end users. Class (static), sequence (dynamic) and collaboration diagrams.',
               '**Process**: how the system works at run time: concurrency, control flow, processes. Activity, interaction overview and state machine diagrams.',
               '**Development**: how the system is built, its software organisation in code. Package and component diagrams.',
               '**Physical**: how the software is mapped to hardware (servers, devices), where components run. Deployment diagram.',
               '**+1 User (scenario)**: captures user scenarios and requirements that drive the other four. Use case diagrams and textual scenarios.']),
    18: dict(
        hl=[('Description', 1), ('Stake', 2), ('Consider', 3), ('UML –', 4)],
        notes=['**Description** row. Logical: the objects of the system and their interaction. Process: processes and workflow rules and how they communicate (dynamic). Development: building-block view, the static organisation of modules. Physical: installation, configuration and deployment. Scenario: shows the design is complete by validating and illustrating it.',
               '**Stakeholders** row. Logical: end users, analysts, designers. Process: integrators and developers. Development: programmers and software project managers. Physical: system engineers, operators, administrators, installers. Scenario: the stakeholders of the other views and their evaluators.',
               '**Considers** row. Logical: functional requirements. Process: non-functional requirements. Development: software module organisation (reuse, tool constraints). Physical: non-functional requirements tied to the hardware. Scenario: system consistency and validity.',
               '**UML** row. Logical: class, state, object, sequence, communication. Process: activity. Development: component, package. Physical: deployment. Scenario: use case.'],
        exam=[asked('m252', 'Q4 (table)', 'Complete the 4+1 table: for each of the logical, process, development, physical and scenario views, give its description, stakeholders and UML diagrams.',
                    a='Logical: objects of the system and their interactions / end users, analysts, designers / class, object, state, sequence, communication. Process: processes and how they communicate (dynamic) / integrators, developers / activity. Development: building blocks, static module organisation / programmers, project managers / component, package. Physical: installation, configuration and deployment / system engineers, operators, administrators / deployment. Scenario: validates and illustrates that the design is complete / the other views’ stakeholders and evaluators / use case.'),
              asked('q261', 'Q21 (matching)', 'Match each 4+1 view with its primary concern: logical, process, development, physical, scenario/user.',
                    a='Logical → major functional elements and their relationships. Process → runtime behaviour, concurrency and communication. Development → organisation of software modules and packages. Physical → deployment of software onto hardware nodes. Scenario/User → use cases that illustrate and validate the architecture.'),
              likely('Which UML diagram belongs to the development view?', a=0, opts=['Package diagram', 'Deployment diagram', 'Use case diagram', 'State diagram'])]),
    19: dict(
        hl=[('4+1view model', 1)],
        notes=['Recap: be able to name each view and give its concern, stakeholders and diagrams from memory. The summary table on slide 18 is the most likely written question from this lecture.']),
}

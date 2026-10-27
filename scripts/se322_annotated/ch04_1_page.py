"""SE322 Chapter 4, Lecture 1 (Architecture Patterns: overview, history, classification): page content.

Schema: see annotated_page.py. Marks with a 4th element 'ocr' are words inside pictures (skipped if OCR can't
read them). Past-exam questions are copied from the papers in exams/; everything else is a prediction.
"""
from .common import asked, likely

TITLE = 'Architecture Patterns: Overview, History and Classification'
CHAPTER = 'SE322 · Chapter 4 · Lecture 1'

OVERVIEW = {
    'summary': ('Architects rarely design from scratch: architectural styles and patterns are documented, reusable '
                'solutions with known benefits and consequences. This lecture separates the terms (a style is the overall '
                'shape, a pattern a specific recipe; architectural patterns are system-wide, design patterns work inside '
                'subsystems), traces their history from Alexander’s building patterns to Buschmann’s architectural '
                'patterns, and classifies systems into five types, each with its typical patterns. Lectures 2 and 3 then '
                'study those patterns one by one.'),
    'ideas': [
        ('Style vs. pattern', 'A style is a high-level template for the whole structure (e.g. data flow); a pattern is a specific reusable solution within it (e.g. pipes and filters).'),
        ('History', '1977 Alexander (253 building patterns) → 1990s architectural styles → 1994 Gang of Four (23 design patterns) → 1996 Buschmann et al. (architectural patterns).'),
        ('Architectural vs. design patterns', 'Architectural patterns fix system-wide structure; design patterns are medium-scale and don’t change the fundamental structure.'),
        ('Five system types', 'Data-centered (blackboard, repository), data flow (pipes and filters), distributed (client-server, broker), interactive (MVC), hierarchical (layered).'),
    ],
    'sections': [
        ('Slides 1–7', 'Styles vs. patterns, and why reuse them'),
        ('Slides 8–13', 'History: Alexander, styles, Gang of Four, Buschmann'),
        ('Slides 14–26', 'Classification: data-centered, data flow, distributed, interactive, hierarchical'),
        ('Slides 27–28', 'Exercise and summary'),
    ],
    'exam': ('The classification table (system type → pattern) is the base of every pattern question. Midterm 261 Q6 '
             '(3.5 marks) matched seven scenarios to layered, pipe-and-filter, broker, blackboard, MVC, client-server and '
             'peer-to-peer; Final 252 Q4 and Midterm 252 Q5 asked you to pick and draw a pattern for a scenario.'),
}

TITLES = {3: 'Extra: Calculating the average, a reusable recipe', 5: 'Overview: the caveman and today’s architect',
          6: 'Overview: reusing documented patterns', 12: 'Extra: Architectural patterns vs. design patterns',
          13: 'Extra: Timeline of styles and patterns', 17: 'Extra: Data Centered Systems', 19: 'Extra: Data Flow Systems',
          21: 'Extra: Distributed Systems', 23: 'Extra: Interactive Systems', 24: 'Extra: Interactive vs. Distributed Systems',
          26: 'Extra: Hierarchal Systems', 27: 'Extra: Question – pick the pattern'}

SLIDES = {
    1: dict(
        hl=[('[Architecture Patterns]', 1), ('Serverless architecture', 2)],
        notes=['Chapter 4 is about **architecture patterns**: ready-made system structures. This first lecture is the overview and classification; the patterns themselves come in Lectures 2 and 3.',
               'Homework on the title slide: research **serverless architecture** (applications built from cloud functions that the provider runs on demand, with no server you manage).']),
    2: dict(
        hl=[('Architectural Style:', 1), ('Architectural Pattern:', 2), ('Data-Centered', 3), ('Hierarchical', 3)],
        notes=['An **architectural style** is a high-level template that defines the overall structure of a system, like “layered”.',
               'An **architectural pattern** is a specific, reusable solution to a common problem inside that structure, like MVC within a layered system. In short: styles set the big picture, patterns give the detailed recipe.',
               'The classification at the end uses five system types: data-centered, data flow, distributed, interactive and hierarchical.']),
    3: dict(
        hl=[('Calculating the Average', 1), ('Data flows Style:', 2), ('Pipes-and-Filters:', 3)],
        notes=['An analogy for reuse: once you know the three steps for an average (list the numbers, total them, divide), you reuse them for students’ scores, weekly temperatures, anything.',
               'Seen as a **style**, the steps are a flow of data: input (the list) → processing (the sum) → output (the average).',
               'Seen as a **pattern**, each step is a *filter* that transforms the data and passes it to the next one: pipes and filters. Because each step is independent, the same pipeline is reused for different averages.']),
    4: dict(
        hl=[('different perspectives', 1), ('logical components', 2), ('past experience', 3), ('architectural styles and architectural patterns', 4)],
        notes=['Systems must be architected and evaluated from **different perspectives**, because stakeholders with different backgrounds care about different qualities.',
               'This chapter focuses on decomposing a system into **logical components** whose structure supports the functional and non-functional requirements.',
               'Good logical architectures come from **past experience**: strategies that already worked in other systems.',
               'That experience is packaged as **architectural styles and patterns**, the mainstream way to achieve reuse at the architectural level.']),
    5: dict(
        hl=[('Caveman!', 1, 0, 'ocr'), ('Important:', 2, 0, 'ocr')],
        notes=['The caveman has to invent the structure of a house from scratch, which is slow and risky.',
               'Today’s architect reuses years of documented experience. The boxed point is the lesson: it is more efficient to build systems from successfully employed designs than to design from scratch.']),
    6: dict(
        hl=[('benefit', 1), ('patterns', 2)],
        notes=['The software version of the same story: the customer asks for “an interactive system that displays data from storage in multiple displays and formats”, and the architect recognises the requirement as the **Model-View-Controller** pattern.',
               'Once a pattern is identified, the architect looks it up in a pattern catalogue for its documented structure (the MVC class and sequence diagrams on the right) and knows the quality properties a system built that way will have.']),
    7: dict(
        hl=[('generic, reusable solutions', 1), ('Improved Quality', 2), ('Consistency', 2), ('Increased Efficiency', 2), ('years of documented experience', 3)],
        notes=['Styles and patterns are **generic, reusable** solutions that are easy to understand and apply to new problems with similar needs.',
               'Benefits of that reuse: **improved quality** (they encode refined best practice), **consistency** (the same structure across an application or across projects, so it is easier to understand and maintain), and **efficiency** (well-understood, tested designs speed up design and implementation).',
               'Decisions based on them benefit from **years of documented experience** describing the solution, its benefits, and the consequences (trade-offs) of using it. Knowing the consequences in advance is the real value.'],
        exam=[likely('What is the benefit of reusing architectural styles and patterns?',
                     a='They are proven, documented solutions: quality improves because they encode best practice, designs are consistent and easier to maintain, design and implementation are faster, and their benefits and consequences are known in advance, which lowers risk and gives the team a shared vocabulary.')]),
    8: dict(
        hl=[('Christopher Alexander', 1), ('1977', 1), ('253 patterns', 2), ('Context of the pattern', 2)],
        notes=['In **1977 Christopher Alexander**, a building architect, published a pattern language to help people design good buildings and towns of any size.',
               'It became a catalogue of **253 patterns**, each documented with a picture, its context, the problem it solves, evidence that it works, and related patterns. That documentation format is the ancestor of every software pattern catalogue.']),
    9: dict(
        hl=[('In the 1990s', 1), ('architectural styles', 1), ('a million times over', 2), ('Light on Two Sides of Every Room', 3), ('Client–Server', 3)],
        notes=['In the **1990s** software engineers began cataloguing recurring high-level solutions (elements and their relationships) and called them **architectural styles**. Their focus was the solution.',
               'Like Alexander’s patterns, a style can be used “**a million times over, without ever doing it the same way twice**”: the idea is reused, the details differ every time.',
               'Alexander’s example: “light on two sides of every room”. The software example: client–server, reused in Gmail (browser client, mail server) and a banking app (mobile client, transaction server), each implemented its own way.']),
    10: dict(
        hl=[('Gang', 1), ('of Four (GoF)', 1), ('1994', 1), ('Design Patterns', 2), ('23', 2)],
        notes=['In **1994** Gamma, Helm, Johnson and Vlissides, the **Gang of Four (GoF)**, published finer-grained, object-oriented **detailed design** solutions.',
               'Inspired by Alexander, they called them **design patterns**: a catalogue of **23** patterns, each described in a fixed specification format. Chapters 6–7 study several of them (Singleton, Builder, Composite, Observer…).'],
        exam=[likely('The Gang of Four (1994) catalogued how many design patterns, at what level?', a=0,
                     opts=['23 detailed-design (object-oriented) patterns', '253 building patterns', '23 architectural styles', '5 system types'])]),
    11: dict(
        hl=[('In 1996', 1), ('Architectural Patterns', 1), ('system-wide structural properties', 2), ('medium-scale patterns', 3), ('no effect on the fundamental structure', 3)],
        notes=['In **1996 Buschmann** et al. combined the two lines of work: well-known architectural styles written in a pattern format (context – problem – solution). They called these **architectural patterns**.',
               'Their definition: architectural patterns specify the **system-wide structural properties** of an application and affect the architecture of its subsystems.',
               'Design patterns are **medium-scale**: applying one has **no effect on the fundamental structure** of the system, though it may strongly shape one subsystem. That sentence is the clearest way to tell the two apart.'],
        exam=[likely('How do architectural patterns differ from design patterns (Buschmann et al.)?',
                     a='Architectural patterns specify system-wide structural properties and affect the architecture of all subsystems (e.g. client-server, layers). Design patterns are medium-scale: they do not change the fundamental structure of the system, only the design inside a subsystem (e.g. Observer, Factory).')]),
    12: dict(
        hl=[('Architectural Patterns', 1, 0, 'ocr'), ('Design Patterns', 2, 0, 'ocr'), ('In short:', 3, 0, 'ocr')],
        notes=['**Architectural patterns** define the overall structure of the whole system and how all subsystems are organised and interact: client–server, layers, pipes and filters. The diagram groups them by system type (data-centered: blackboard, repository; data flow: pipes and filters; distributed: client-server, broker; interactive and hierarchical).',
               '**Design patterns** are solutions at the subsystem or component level that do not change the overall structure: Observer, Factory, Strategy. The lower diagram groups them as creational, structural, concurrency and behavioural.',
               'In short: architectural pattern = the big picture (system-wide structure); design pattern = the medium picture (subsystem or component behaviour).']),
    13: dict(
        hl=[('1977 – Christopher Alexander', 1), ('1990s – Software Engineering Community', 2), ('1994 – Gang of Four (GoF)', 3), ('1996 – Buschmann et al.', 4)],
        notes=['**1977, Alexander**: 253 building patterns documenting problem, solution and context. He gave the world the language of patterns.',
               '**1990s, the software community**: architectural styles, reuse of whole-system structures (client–server, layered).',
               '**1994, GoF**: the Design Patterns book, 23 object-oriented patterns at the class and object level.',
               '**1996, Buschmann et al.**: combined both into architectural patterns (system-wide) as opposed to design patterns (subsystem level).'],
        exam=[likely('Put in order and match: Gang of Four, Buschmann et al., Alexander, architectural styles.',
                     a='Alexander 1977 (253 building patterns) → architectural styles in the 1990s → Gang of Four 1994 (23 design patterns) → Buschmann et al. 1996 (architectural patterns).')]),
    14: dict(
        hl=[('type of system, requirements, and desired quality attributes', 1), ('more than one architectural pattern', 2), ('type of system', 3, 1)],
        notes=['Which pattern to apply depends on the **type of system, its requirements and the desired quality attributes**. These, not the pattern’s popularity, decide between patterns.',
               'Large systems often **combine patterns**: a client–server system whose server is internally layered, for example.',
               'Patterns are classified by the **type of system** they suit (next slide).']),
    15: dict(
        hl=[('Major types of systems:', 1), ('Data-', 2, 0, 'ocr'), ('Data Flow', 2, 0, 'ocr'), ('Distributed', 2, 0, 'ocr'), ('Interactive', 2, 0, 'ocr'), ('Hierarchical', 2, 0, 'ocr')],
        notes=['The five system types, each with its typical patterns (slides 16–26).',
               {'text': 'The table:', 'items': [
                   ('Data-centered', 'A centralised repository of data that clients access and work on → blackboard, repository.'),
                   ('Data flow', 'Built around transporting and transforming a stream of data → pipes and filters.'),
                   ('Distributed', 'Independent processing units interacting over a network → client–server, broker.'),
                   ('Interactive', 'User-centric systems → MVC.'),
                   ('Hierarchical', 'Components arranged in levels of abstraction and responsibility → layered (main program and subroutine).')]}],
        exam=[asked('m261', 'Q6 · 3.5 marks', 'Match each scenario with the most suitable architectural style (each used once): (1) payroll app whose UI, salary rules and data storage must evolve independently; (2) security-log app where separate units extract fields, normalise timestamps, remove sensitive values and summarise; (3) hospital app talking to lab equipment from different vendors through one request format; (4) speech-understanding app whose components repeatedly add and reconsider partial interpretations; (5) museum ticketing shown differently on desktop and kiosks, updated by user actions; (6) classroom response app with one authoritative session for hundreds of phones; (7) emergency messaging between nearby phones with no Internet and no central node.',
                    a='(1) **Layered**. (2) **Pipe-and-filter**. (3) **Broker**. (4) **Blackboard**. (5) **MVC**. (6) **Client-server**. (7) **Peer-to-peer**. Layered separates responsibilities; pipe-and-filter chains independent transformations; broker hides vendor-specific communication; blackboard combines partial solutions through shared knowledge; MVC separates model, views and control; client-server uses one authoritative service; peer-to-peer needs no central node.'),
              likely('Pipes and filters belongs to which system type?', a=0, opts=['Data flow', 'Data-centered', 'Distributed', 'Hierarchical'])]),
    16: dict(
        hl=[('centralized', 1), ('Used in DBMS', 2), ('Data store', 3, 0, 'ocr')],
        notes=['**Data-centered** systems are a centralised repository of data that clients access and work on.',
               'Uses: DBMSs, library information systems, the CORBA interface repository, compilers and CASE tools, speech and image recognition, security systems, business resource management.',
               'The diagram: many client software components around one **data store** (repository or blackboard). Clients don’t talk to each other, only to the store. Sharing data is easy; the store can become a bottleneck and a single point of failure.']),
    17: dict(
        hl=[('Blackboard, Repository', 1), ('central data store', 2), ('do not communicate directly', 3)],
        notes=['Patterns for data-centered systems: **blackboard** and **repository**.',
               'Components interact through a **central data store**: they retrieve, add and modify data there.',
               'They **do not communicate directly** with each other; the repository is the intermediary. In a repository the store is passive; in a blackboard, components react to changes on the shared data (Lecture 2).']),
    18: dict(
        hl=[('transport', 1), ('transformation', 1), ('video streaming', 2)],
        notes=['**Data flow** systems are organised around the **transport and/or transformation** of a stream of data.',
               'Example: video streaming. The picture shows data entering from a source, passing through processing nodes (which may branch and rejoin), and leaving to the cloud: each node transforms the stream and hands it on.']),
    19: dict(
        hl=[('Pipes-and-Filters', 1), ('called filters', 2), ('connected by pipes', 2), ('signal processing', 3)],
        notes=['Pattern for data flow systems: **pipes and filters**.',
               'Processing elements called **filters** are connected by **pipes** that carry data from one filter to the next. Each filter takes input, transforms it, and produces output.',
               'Typical uses: signal processing and data streaming, compilers (lexer → parser → code generator), image and video processing.']),
    20: dict(
        hl=[('several independent', 1), ('world', 2), ('Distributed system layer (middleware)', 3, 0, 'ocr')],
        notes=['**Distributed** systems are made of **several independent processing units** that interact over a network.',
               'Example: web applications (the World Wide Web).',
               'The diagram: four computers, each with its own local OS, running applications A, B (spread over two machines) and C, joined by a **middleware** layer that hides the network so the applications can talk as if local. Network delays and partial failures are the price of distribution.']),
    21: dict(
        hl=[('Client-Server, Broker', 1), ('Client-Server:', 2), ('Broker:', 3)],
        notes=['Patterns for distributed systems: **client–server** and **broker**.',
               '**Client–server**: many clients request resources and services from a central server, which processes the requests and returns responses. It is the basis of the web (browser clients, web server).',
               '**Broker**: a broker component coordinates communication between components in different processes or machines. It routes requests, translates messages, and adds security and scalability, as in service-oriented architectures where services talk through a messaging system.']),
    22: dict(
        hl=[('(user-centric systems)', 1), ('mobile', 2), ('offline only', 3), ('requires server communication', 3)],
        notes=['**Interactive** systems serve users and need heavy interaction between the user and the system (user-centric).',
               'Example: mobile applications.',
               'The Extra rule: an app that works **offline only** (calculator, offline dictionary, offline game) is interactive; an app that **needs a server** (WhatsApp, Gmail, banking) is distributed. Many real apps are both: interactive on the phone, distributed overall.']),
    23: dict(
        hl=[('Interactive Systems', 1), ('Desktop Calculator App', 2, 0, 'ocr')],
        notes=['An interactive system as described here: the user interacts directly with the software, and all logic and data are handled on the same machine.',
               'Example: a desktop calculator. The flow is user interface (handles interaction) → application logic (processes commands) → data management → local database. This separation of interface from logic is what MVC formalises.']),
    24: dict(
        hl=[('Interactive (Local)', 1), ('Distributed (Networked)', 2)],
        notes=['**Interactive (local)**: runs fully on one machine, works offline, one user (calculator, offline dictionary).',
               '**Distributed (networked)**: split across machines (client + server), needs the Internet, supports many users (Gmail, banking).'],
        exam=[likely('Is an offline dictionary app interactive or distributed? Is WhatsApp?',
                     a='The offline dictionary is interactive (runs fully on one machine). WhatsApp is distributed (clients communicate through servers over the network).')]),
    25: dict(
        hl=[('hierarchy', 1), ('levels of', 1), ('control systems', 2)],
        notes=['**Hierarchical** systems arrange components in a **hierarchy**, vertically and horizontally, reflecting levels of abstraction and responsibility.',
               'Example: control systems in manufacturing, robotics and vehicles. In the diagram the top-level node sends tasks and goals down; lower nodes pass sensations and results up; sensors and actuators at the bottom touch the controlled process.']),
    26: dict(
        hl=[('structured in layers', 1), ('Operating systems', 2)],
        notes=['Hierarchical systems are structured in **layers**, each with a specific responsibility, separating concerns vertically (layers) or horizontally (modules).',
               'Example: an **operating system**, from hardware interaction at the lowest layer to user-interface management at the top. Each layer uses only the services of the layer below it. The pattern is **layered** (and main program and subroutine).']),
    27: dict(
        hl=[('Blackboard, Pipe-Filter, Client-Server, Broker', 1, 0, 'ocr'), ('DBMS', 2)],
        notes=[{'text': 'The exercise: pick the pattern for each requirement.', 'items': [
                   ('1. Video processing in a fixed sequence (decode, filter, encode)', '**Pipe-and-filter**: a chain of transformations.'),
                   ('2. Online banking used through web, mobile and desktop', '**Client-server**: many clients, one central service.'),
                   ('3. Financial analysis where collaborating modules contribute expertise to one evolving solution', '**Blackboard**: independent knowledge sources refine shared data.')]},
               'A **DBMS** can be seen two ways: as a **repository** (data-centered: all applications share one database) or as part of a **client–server** system (distributed: clients send SQL queries, the server processes them). The classification depends on the viewpoint.']),
    28: dict(
        hl=[('Classification of Architectural Styles and Patterns', 1), ('Blackboard and Pipes-and-Filters', 2)],
        notes=['Recap: styles vs. patterns, their history, and the five system types.',
               'Next lecture: data-centered and data flow systems in detail, with the **blackboard** and **pipes-and-filters** patterns.']),
}

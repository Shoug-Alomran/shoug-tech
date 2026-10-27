"""SE322 Chapter 5, Lecture 1 (Principles of Detailed Design I: overview and key tasks): page content.

Schema: see annotated_page.py. Marks with a 4th element 'ocr' are labels inside pictures (skipped if OCR can't
read them). Past-exam questions are copied from the papers in exams/; everything else is a prediction.
"""
from .common import asked, likely

TITLE = 'Principles of Detailed Design I: What Detailed Design Is and Its Key Tasks'
CHAPTER = 'SE322 · Chapter 5 · Lecture 1'

OVERVIEW = {
    'summary': ('Detailed design takes the architecture’s black-box components and refines them until they can be coded: '
                'their internal structure, their behaviour, their interfaces and their data. Architecture bridges requirements '
                'and design; detailed design bridges design and code. The lecture places it in the life cycle and lists its five '
                'key tasks: understand the architecture and the requirements allocated to your component, create the detailed '
                'design, evaluate it with technical reviews, document it in the software design document (SDD), and keep the '
                'implementation synchronised with it.'),
    'ideas': [
        ('Refinement', 'Detailed design refines and expands the architecture until the design is complete enough to implement.'),
        ('Both directions', 'From requirements and architecture forward to code, and from code backward (reverse engineering) to the design.'),
        ('Five tasks', 'Understand → create → evaluate (technical reviews) → document (SDD) → monitor and control implementation.'),
        ('Synchronicity', 'Detailed design follows the architecture and the code follows the detailed design; low synchronicity signals project risk.'),
    ],
    'sections': [
        ('Slides 1–6', 'What detailed design is and where it fits'),
        ('Slides 7–9', 'Key tasks 1–2: understanding requirements, creating designs'),
        ('Slides 10–12', 'Key tasks 3–4: technical reviews and the SDD'),
        ('Slides 13–14', 'Key task 5: managing implementation, and summary'),
    ],
    'exam': ('Final 252 Q1 asked for the primary focus of detailed design (the internals of components and their behaviour to '
             'meet functional requirements). Expect short questions on the five key tasks, technical-review guidelines, the SDD '
             'and synchronicity; Lecture 2 holds the SOLID questions.'),
}

TITLES = {3: 'Where we are: from requirements to construction', 6: 'Designer’s Mental Model During Detailed Design',
          8: 'Key task 1: Understanding Architecture and Requirements', 9: 'Key task 2: Creating Detailed Designs',
          10: 'Key task 3: Evaluating Detailed Designs', 11: 'Key task 4: Documenting Detailed Designs',
          12: 'Key task 4: SDD sections and table of contents', 13: 'Key task 5: Managing Implementation'}

SLIDES = {
    1: dict(
        hl=[('[Principles of Detailed Design]', 1)],
        notes=['Chapter 5 moves from architecture to **detailed design**, the second major design activity. Lecture 1 explains what it is and the tasks it involves; Lectures 2 and 3 cover the principles (SOLID) used to judge a detailed design.']),
    2: dict(
        hl=[('Overview of Detailed Design', 1), ('Key Tasks in Detailed Design', 2)],
        notes=['First: what detailed design is and where it fits in the life cycle.',
               'Then its five key tasks, each on its own slide (7–13).']),
    3: dict(
        hl=[('Start (Requirements Phase)', 1), ('Architecture (High-Level Design)', 2), ('Detailed Design (Refinement)', 3), ('Goal (Construction Phase)', 4)],
        notes=['**Requirements**: gather and document what the system must do, e.g. banking-app users must check balances and transfer money.',
               '**Architecture**: define the overall structure and interactions, e.g. a client–server system with a database, the app and a security layer.',
               '**Detailed design**: break the architecture into smaller components and detailed functions, e.g. for login, specify password validation, authentication and session management. The diagram marks this “we are here”: design shifts from a macro approach to a **micro** one, decomposing components into fine-grained elements, functions and data.',
               '**Construction**: start coding from the detailed design (login, account management, transfers).']),
    4: dict(
        hl=[('refining', 1), ('expanding', 1), ('sufficiently', 1), ('internal structure', 2), ('behavioral', 2), ('blueprints before construction', 3), ('Construction Phase (Implementation)', 4)],
        notes=['**Definition**: detailed design is the process of **refining and expanding** the preliminary design (the software architecture) of a system or component until the design is **complete enough to be implemented**.',
               'Designers go deep into each component to define its **internal structure** and **behaviour**, so that construction becomes natural and efficient. Structure = how the component is built inside; behaviour = how it acts and reacts in different scenarios.',
               'Detailed design produces specifications, algorithms, database schemas, interface definitions and class diagrams, but **no code yet**. Login example: password rules (minimum length, special characters), hashing plus salting for authentication, session timeout and refresh tokens. It is the blueprint before building.',
               '**Construction** then translates that design into code: writing `validatePassword()`, implementing the authentication API, coding session management. It is building the house from the blueprint.'],
        exam=[asked('f252', 'Q1 MCQ 7', 'What is the primary focus of “Detailed Design”?',
                    a=2, opts=['External properties of software components and non-functional requirements.',
                               'The overall development process for both hardware and software.',
                               'The internals of system components and their behavior to fulfill functional requirements.',
                               'Project management tasks like staffing and tracking.'])]),
    5: dict(
        hl=[('architecture', 1), ('construction', 1), ('full understanding', 1), ('bridge between design and code', 2), ('design strategies', 3)],
        notes=['Detailed design sits between **architecture** and **construction**, so detailed designers need a **full understanding** of both the requirements and the architecture they are refining.',
               'The bridge analogy: architecture bridges **requirements and design**; detailed design bridges **design and code**.',
               'Designers must also be proficient in **design strategies** (e.g. object-oriented), programming languages, and quality-control methods, because their output must be directly implementable.'],
        exam=[likely('Detailed design provides the bridge between:', a=0, opts=['Design and code', 'Requirements and architecture', 'Testing and deployment', 'Users and managers'])]),
    6: dict(
        hl=[('If given requirements and', 1, 0, 'ocr'), ('If given code', 2, 0, 'ocr'), ('Reverse Engineering', 3), ('Important:', 4, 0, 'ocr')],
        notes=['**Forward**: given requirements and architecture, detailed designers must move the project all the way to code (the funnel: requirements/architecture → detailed design → code).',
               '**Backward**: given code, they must be able to **reverse engineer** it into detailed and architectural designs. Starting at detailed design, you must be able to produce both the code and the architecture.',
               '**Reverse engineering** means analysing existing code to recover what the system does, how it is structured, and how it maps back to design and requirements (useful for legacy systems and maintenance).',
               '**Tools** are essential at this stage: UML modelling, code generation, compilers, reverse-engineering tools and configuration management.']),
    7: dict(
        hl=[('Understanding the architecture and requirements', 1), ('Creating detailed designs', 2), ('Evaluating detailed designs', 3),
            ('Documenting software design', 4), ('Monitoring and controlling implementation', 5)],
        notes=['**1. Understand** the architecture and the requirements allocated to your components (slide 8).',
               '**2. Create** the detailed designs: interfaces, GUI, internal structure and behaviour, data (slide 9).',
               '**3. Evaluate** them, mainly through technical reviews (slide 10).',
               '**4. Document** them, mainly in the SDD (slides 11–12).',
               '**5. Monitor and control implementation**, keeping code and design in sync (slide 13). The tasks form a loop: a review or a coding discovery can send you back to an earlier task.'],
        exam=[likely('List the five key tasks of detailed design.',
                     a='Understanding the architecture and requirements; creating detailed designs; evaluating detailed designs (technical reviews); documenting the design (SDD); monitoring and controlling implementation (synchronicity).')]),
    8: dict(
        hl=[('requirements allocated to their specific components', 1), ('assigned to teams', 2), ('possible for designers', 3, 0, 'ocr')],
        notes=['In architecture the **whole** set of requirements is evaluated. In detailed design, each designer focuses on the **requirements allocated to their specific component**.',
               'Architecture components (SensorManager, VideoManager, ClientManager in the diagram) are **assigned to teams**, each with the functional and quality requirements allocated to it. Each team refines its component and prepares it for coding.',
               'During detailed design, designers may also **derive new requirements** for their component (validation rules, performance limits) and impose them on its implementation.']),
    9: dict(
        hl=[('structural and behavioral designs', 1), ('Interface Design', 2), ('Graphical User Interface (GUI) Design', 3), ('Internal Component Design', 4), ('Data Design', 5)],
        notes=['Once the architecture and requirements for the assigned component are understood, detailed design starts. It covers both **structural and behavioural** design.',
               '**Interface design**: internal interfaces (between components of the system) and external ones (with other systems).',
               '**GUI design**: the screens users interact with.',
               '**Internal component design**: the structure (classes, relationships) and behaviour (interactions, states) inside each component. Lectures 2–3 give the principles for this.',
               '**Data design**: the database and the data dictionary (the definitions of every data element).']),
    10: dict(
        hl=[('Technical Reviews', 1), ('review notice', 2), ('technical expert', 3), ('quality assurance', 3), ('functional and non-functional requirements', 4), ('action items', 5)],
        notes=['The most popular way to evaluate detailed designs is a **technical review**.',
               'Send the **review notice** early enough that reviewers can study the design thoroughly.',
               'Include a **technical expert**, the **stakeholders** of your design, and a member of the **QA or testing** team.',
               'During the review, focus on what matters: how the design meets the **functional and non-functional** requirements. E-commerce checkout example: secure payments (non-functional) and smooth order processing (functional).',
               '**Document** the review, and make sure every **action item** is captured and assigned to someone.'],
        exam=[likely('Give three guidelines for conducting a technical review of a detailed design.',
                     a='Send the review notice early so reviewers can prepare; include a technical expert, stakeholders and a QA/testing member; focus on how the design meets functional and non-functional requirements; document the review and assign every action item.')]),
    11: dict(
        hl=[('software design document (SDD)', 1), ('Interface Control Document', 2), ('Version Control Document', 3)],
        notes=['The design is documented mainly in the **software design document (SDD)**, also called the software design description. It is used throughout development by programmers, testers, maintainers and system integrators.',
               'The **interface control document** describes the system’s interfaces and how components communicate.',
               'The **version control document** lists what each software release contains (files, scripts, executables); different versions of the design correspond to specific releases.'],
        exam=[likely('Detailed designs are documented mainly in the:', a=0, opts=['Software Design Document (SDD)', 'Software Requirements Specification', 'Test plan', 'Project charter'])]),
    12: dict(
        hl=[('sections of the SDD', 1), ('Date of issue', 2, 0, 'ocr'), ('Body', 3, 0, 'ocr'), ('Glossary', 4, 0, 'ocr')],
        notes=['The SDD sections and a sample table of contents.',
               '**Front matter**: date of issue and status (each formal release gets a new date), scope (the intended purpose of the software), issuing organisation, authorship, references (every document or technology referred to), and context.',
               '**Body**: the main section where the design itself is documented, the part stakeholders read to understand how the software is to be built. In the sample contents it holds the software architecture (stakeholders, concerns, architectural viewpoints and views) and the detailed design (one viewpoint per component).',
               '**Back matter**: summary, **glossary** (definitions of all terms and acronyms) and **change history** (what was added, removed or changed).']),
    13: dict(
        hl=[('synchronicity', 1), ('Low degree of synchronicity', 2), ('maintenance', 3), ('new engineers', 3), ('encrypted login', 4)],
        notes=['**Detailed design synchronicity** measures how well the detailed design adheres to the architecture and how well the code adheres to the detailed design.',
               'A **low degree** of synchronicity points to a flaw in the process and can lead to project failure.',
               'It needs particular attention when the project enters **maintenance** or **new engineers** join, the moments when design and code drift apart. Processes must be in place to keep it high.',
               'Example: the architecture requires **encrypted login**, the detailed design forgets encryption, and the code stores plain passwords. Each level broke synchronicity with the one above.'],
        exam=[likely('What is detailed design synchronicity, and why does low synchronicity matter?',
                     a='It is the degree to which the detailed design follows the architecture and the code follows the detailed design. Low synchronicity means the documentation no longer describes the real system; it points to a process flaw and can lead to project failure, especially during maintenance or when new engineers join.')]),
    14: dict(
        hl=[('Key Tasks in Detailed Design', 1), ('Next … Design Patterns', 2)],
        notes=['Recap: detailed design refines the architecture until it can be coded, through five tasks: understand, create, evaluate, document, monitor.',
               'Next: the principles for judging a detailed design (SOLID, Lectures 2–3), then design patterns.']),
}

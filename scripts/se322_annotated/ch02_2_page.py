"""SE322 Chapter 2, Lecture 2 (Software Architecture Process and Requirements Engineering): page content.

Schema: see annotated_page.py. Past-exam questions are copied from the papers in exams/ (Quiz 1 261 Q1–Q6, Q15);
everything else is a prediction.
"""
from .common import asked, likely

TITLE = 'The Architecture Process and Requirements Engineering'
CHAPTER = 'SE322 · Chapter 2 · Lecture 2'

OVERVIEW = {
    'summary': ('The architecture process has five steps: understand and evaluate the requirements, design the '
                'architecture, evaluate it, document it, and monitor and control its implementation. This lecture '
                'covers the first step in depth. Requirements engineering runs four activities (elicitation, analysis, '
                'specification and validation), and a requirement worth designing from must be specific, correct, '
                'complete, consistent, attainable and verifiable. Every bad-requirement example on the slides fails at '
                'least one of those six tests.'),
    'ideas': [
        ('Five-step process', 'Understand requirements → design → evaluate → document → monitor and control implementation.'),
        ('Four RE activities', 'Elicit (discover needs), analyse (classify, prioritise, negotiate, model), specify (write down), validate (check with stakeholders).'),
        ('Six qualities', 'Specific, correct, complete, consistent, attainable, verifiable. “The system shall be fast” fails specific and verifiable.'),
        ('Architects live in requirements', 'Architects go back and forth between requirements and design, and conceptual modelling is often where architecture starts.'),
    ],
    'sections': [
        ('Slides 1–3', 'The software architecture process'),
        ('Slides 4–6', 'Requirements engineering and elicitation'),
        ('Slides 7–11', 'Analysis: classification, prioritisation and negotiation, conceptual modelling'),
        ('Slides 12–18', 'Specification and validation; the six characteristics of good requirements'),
        ('Slide 19', 'Summary and the 4+1 views next'),
    ],
    'exam': ('Quiz 1 261 drew seven questions from this lecture: elicitation (twice), validation, negotiation, matching '
             'the five architecture-process activities to their purposes, architecture evaluation, and whether “the '
             'system should respond quickly” is verifiable (it is not).'),
}

TITLES = {8: 'Extra: Banking App requirements analysis', 14: 'Extra: Specific vs. non-specific requirements',
          17: 'Understand and Evaluate Requirements: consistent and attainable'}

SLIDES = {
    1: dict(
        hl=[('[Software Architecture]', 1)],
        notes=['Week 3, second lecture. Lecture 1 listed what an architect does; this one gives the order in which it is done, and then studies the first step, understanding the requirements, in detail.']),
    2: dict(
        hl=[('Software Architecture Process', 1), ('Requirements Engineering', 2)],
        notes=['Part 1 is the five-step **architecture process** (slide 3).',
               'Part 2 is **requirements engineering**, the discipline behind step 1, with its four activities: elicitation, analysis, specification, validation.']),
    3: dict(
        hl=[('Understand and evaluate requirements', 1), ('Design the architecture', 2), ('Evaluate the architecture', 3),
            ('Document the architecture', 4), ('Monitor and control implementation', 5)],
        notes=['**Understand and evaluate requirements**: find the architectural drivers, meaning the requirements, quality attributes and constraints that will shape the structure.',
               '**Design the architecture**: define the major structures (components, connectors) and the design decisions behind them.',
               '**Evaluate the architecture**: check whether it satisfies the important requirements and stakeholder concerns before building on it.',
               '**Document the architecture**: communicate the structures and decisions to everyone who needs them (chapter 9).',
               '**Monitor and control implementation**: check that the code stays consistent with the architecture. This is design synchronicity from Lecture 1, and it is why architecture work doesn’t end when coding starts.'],
        exam=[asked('q261', 'Q5 (matching)', 'Match each architecture process activity with its main purpose: understand and evaluate requirements; design architecture; document architecture; evaluate architecture; monitor and control implementation.',
                    a='Understand and evaluate requirements → **identify architectural drivers and constraints**. Design architecture → **define major structures and design decisions**. Document architecture → **communicate architectural structures and decisions**. Evaluate architecture → **assess whether the architecture satisfies important concerns**. Monitor and control implementation → **check that implementation remains consistent with the architecture**. (Design and document are the pair most often swapped.)'),
              asked('q261', 'Q6 (fill in)', 'Fill in the blank: After designing an architecture, the activity used to determine whether it satisfies important requirements and stakeholder concerns is architecture ___.',
                    a='**Evaluation.**')]),
    4: dict(
        hl=[('Requirements engineering', 1), ('Elicitation', 2), ('Analysis', 2), ('Specification', 2, 1), ('Validation', 2),
            ('back and', 3), ('completely immersed', 3)],
        notes=['**Requirements engineering** is the part of software engineering concerned with a systematic approach to requirements: getting them, understanding them and writing them down properly.',
               'It has four activities, explained on the next slides: **elicitation** (discover), **analysis** (clean up), **specification** (document) and **validation** (confirm).',
               'Architects spend a lot of time here. Even after requirements are specified they keep going **back and forth** between requirements and design, because designing exposes gaps and conflicts. On some projects they are completely immersed in the requirements phase and help write the specification.'],
        exam=[likely('List the four activities of requirements engineering in order.', a='Elicitation, analysis, specification, validation.')]),
    5: dict(
        hl=[('identifying stakeholders', 1), ('non-functional', 1), ('all sources of information', 2), ('similar but different visions', 3),
            ('Stakeholders', 4, 1), ('Goals', 4), ('Domainknowledge', 4), ('Operational and organizationalenvironment', 4)],
        notes=['**Elicitation** is the discovery activity: identify the stakeholders, uncover what the customer needs and wants, and determine the non-functional requirements (which customers rarely state unprompted).',
               'It starts by listing **every source of information** that can produce requirements, before collecting a single requirement.',
               'Sources may have **similar but different visions** of the system: two departments can describe “the same” workflow differently. Spotting that early prevents conflicts later.',
               'Common sources: **stakeholders**; **goals** (the business objectives the system serves); **domain knowledge** (how banking, medicine or education works); and the **operational and organisational environment** (existing systems, policies, hardware the new system must live with).'],
        exam=[asked('q261', 'Q1 (fill in)', 'Fill in the blank: The requirements activity in which stakeholder needs are discovered using techniques such as interviews and observation is called ___.',
                    a='**Elicitation**: the discovery step, before anything is documented.')]),
    6: dict(
        hl=[('Interviews', 1), ('Facilitatedmeetings', 2), ('Observation', 3), ('Scenarios', 4)],
        notes=['**Interviews**: ask stakeholders directly, one at a time or in small groups. Good for detail; limited by what people remember to say.',
               '**Facilitated meetings** (workshops): bring stakeholder groups together with a facilitator so conflicting views surface and get discussed in one place.',
               '**Observation**: watch users do their current work. It reveals steps and workarounds that people never mention in interviews because they take them for granted.',
               '**Scenarios**: walk through concrete stories of use (“a student registers for a full course…”) to discover what the system must do and how it should respond.'],
        exam=[asked('q261', 'Q2', 'An architect interviews end users, observes their current work, and runs a facilitated workshop to discover system needs. Which requirements activity is being performed?',
                    a=2, opts=['Negotiation', 'Architecture documentation', 'Elicitation', 'Classification'],
                    why='Interviews, observation and facilitated meetings are elicitation techniques.')]),
    7: dict(
        hl=[('contradicting, incomplete, vague, or just wrong', 1), ('24/7', 2), ('clear the air', 3), ('Requirement classification', 4),
            ('Requirement prioritization', 4), ('Requirement negotiation', 4), ('Conceptual modeling', 4)],
        notes=['**Analysis** takes requirements in their raw form and fixes the ones that are **contradictory, incomplete, vague or simply wrong**.',
               'Contradiction example: one requirement says the system runs 24/7, another needs daily maintenance downtime. Both can’t be true as written, so someone must decide.',
               'Analysis lets architects **clear the air** about what really needs to be done before they invest in detailed designs.',
               'Its four tasks: **classification** (slide 9), **prioritisation** and **negotiation** (slide 10), and **conceptual modelling** (slide 11).']),
    8: dict(
        hl=[('R1: Secure login', 1), ('R2: Fast & seamless user', 2), ('R3: Multiple payment', 3), ('R4: 24/7 availability', 4)],
        notes=['**R1 Secure login** is *vague*: “secure” could mean a password, two-factor authentication or a fingerprint. Resolution: clarify the exact login method with the stakeholders.',
               '**R2 Fast & seamless experience** may *conflict* with R1, since strong security slows things down. Resolution: a design that balances the two (efficient encryption, smart caching).',
               '**R3 Multiple payment methods** is *incomplete*: which methods (card, PayPal, crypto)? Resolution: define them explicitly.',
               '**R4 24/7 availability** *contradicts* the need for maintenance downtime. Resolution: rolling updates or redundant servers, so updates happen without the service going down. Each row is one of slide 7’s problem types.'],
        exam=[likely('For each banking-app requirement, name the problem analysis would find: (a) “secure login”, (b) “multiple payment methods”, (c) “24/7 availability” alongside planned maintenance downtime.',
                     a='(a) Vague: “secure” is undefined. (b) Incomplete: the payment methods aren’t listed. (c) Contradictory: 24/7 conflicts with downtime; resolved with rolling updates or redundant servers.')]),
    9: dict(
        hl=[('identifying the nature of each', 1), ('Functional vs. non-functional', 2), ('Product vs. process', 3), ('Imposed vs. Derived', 4)],
        notes=['**Classification** identifies the nature of each requirement, along three independent axes.',
               '**Functional vs. non-functional**: functional says *what* the system does (“users can log in”); non-functional says *how well* it behaves (“the page loads within 2 seconds”).',
               '**Product vs. process**: a product requirement is about the delivered software (“the app supports online payments”); a process requirement is about how it is developed (“the app must be developed using Agile”).',
               '**Imposed vs. derived**: an imposed requirement comes straight from stakeholders (“the app runs on iOS and Android”); a derived one is worked out by the team to meet a higher goal (“to support both platforms, use Flutter”).'],
        exam=[likely('Classify “The app must be developed using the Agile methodology” on the product/process axis, and “To support both platforms we will use Flutter” on the imposed/derived axis.',
                     a='The first is a process requirement (about how the product is developed). The second is derived: the team chose it to satisfy the imposed requirement “run on iOS and Android”.'),
              likely('“The system must load within 2 seconds” is a:', a=0,
                     opts=['Non-functional requirement', 'Functional requirement', 'Process requirement', 'Derived requirement'])]),
    10: dict(
        hl=[('most important functions', 1), ('refine the projected schedule', 2), ('different builds', 3), ('during negotiation', 4)],
        notes=['**Prioritisation** identifies the most important functions: login security matters more than a theme colour.',
               'Done well, it refines the schedule by deciding which requirements are handled **first**: payment and security early, less urgent features later.',
               'It also defines the **builds** (releases): Release 1 has the core features, Release 2 adds the chatbot and extras.',
               'And it supports **negotiation** when requirements conflict: “security now, chatbot in a later update” is a negotiated outcome based on priority.'],
        exam=[asked('q261', 'Q4', 'Two stakeholder groups request requirements that cannot both be fully satisfied. Which activity is most directly used to resolve this conflict?',
                    a=2, opts=['Requirements classification', 'Code inspection', 'Requirements negotiation', 'Requirements elicitation'],
                    why='Classification only groups requirements; negotiation reaches an acceptable trade-off.')]),
    11: dict(
        hl=[('Conceptual models', 1), ('bounds of the software system', 2), ('this is where architectural design begins', 3), ('Inside:', 2), ('Outside:', 2)],
        notes=['**Conceptual models** help identify requirements by showing their context, the system’s **boundaries**, and how the system interacts with its environment.',
               'Boundaries decide what is inside and outside the system. Online banking: login, balance and transfers are **inside**; ATM hardware and cash withdrawal are **outside**. Getting this wrong means designing (or forgetting) whole subsystems.',
               'This is often **where architectural design begins**, because building a good conceptual model already requires decomposing the system into parts. The slide marks this as important.']),
    12: dict(
        hl=[('formally captured and', 1), ('review', 2), ('Specific', 3, 2), ('Correct', 3), ('Complete', 3, 1), ('Consistent', 3), ('Attainable', 3), ('Verifiable', 3)],
        notes=['**Specification** formally captures the results of elicitation and analysis in a document format that every stakeholder can use and review (the SRS).',
               '**Validation**: stakeholders review the documented requirements to confirm they are accurate, complete and feasible, i.e. that they really represent their needs.',
               'Each requirement must have six characteristics: **specific, correct, complete, consistent, attainable, verifiable**. Slides 13–18 take them one at a time.'],
        exam=[asked('q261', 'Q3 (fill in)', 'Fill in the blank: Checking whether documented requirements correctly represent stakeholder needs is called requirements ___.',
                    a='**Validation.** (Analysis and correctness were the common wrong answers.)'),
              likely('List the six characteristics a well-specified requirement should have.', a='Specific, correct, complete, consistent, attainable, verifiable.')]),
    13: dict(
        hl=[('clear, concise', 1), ('Clearrequirements', 2), ('deceptive validation', 2), ('Conciserequirements', 3), ('Exclusiverequirements', 4)],
        notes=['**Specific** has three parts: the requirement is clear, concise and exclusive.',
               '**Clear**: not open to interpretation. Ambiguity leads to wrong designs, wrong code, and *deceptive validation*: a test can “pass” against one reading of the requirement while the stakeholder meant another.',
               '**Concise**: short and to the point, so it is easy to understand.',
               '**Exclusive**: each requirement states one and only one thing, which makes it easy to verify; a requirement that bundles two things can be half met.']),
    14: dict(
        hl=[('search for a product using the product ID', 1), ('authenticate users with user ID and password', 1), ('within 1/2 second', 1),
            ('search the database', 2), ('be secure.', 3), ('secure and fast', 4)],
        notes=['Specific examples: searching **by product ID**, authenticating **with user ID and password**, acknowledging **within ½ second**. Each says exactly what, how, or how much.',
               '“The software shall search the database” is not specific: search for what, by which criteria, returning what?',
               '“The software shall be secure” is not specific: security covers encryption, authentication, access control… which one is required?',
               '“Secure and fast” fails twice: two vague qualities in one sentence (not exclusive), with no measurable meaning for either.'],
        exam=[likely('Rewrite “The software shall be secure and fast” as specific requirements.',
                     a='Split it and make each measurable, e.g. “The system shall authenticate users with a user ID and password and lock the account after 5 failed attempts” and “The system shall return search results within 2 seconds for 95% of requests.”')]),
    15: dict(
        hl=[('accurately describe a', 1), ('incorrect or undesired behavior', 1), ('unique combinationof user', 2)],
        notes=['A requirement is **correct** when it accurately describes a function the stakeholders actually want. A wrong requirement, implemented perfectly, still gives wrong or undesired behaviour.',
               'The cartoon is an incorrect requirement in action. The specification said each **user ID + password combination must be unique**, so registering as user123/pwd123 is rejected with “you must use a unique combination”. But that error tells the new user that someone else already has exactly that username and password: the system has just given away another person’s login. The code did what the requirement said; the requirement was wrong. (Usernames should be unique; passwords should never be compared across users.)'],
        exam=[likely('Explain why “each username and password combination must be unique” is an incorrect requirement.',
                     a='Enforcing it means telling a registering user that their chosen combination already exists, which discloses another user’s valid credentials. The requirement describes undesired behaviour; the correct one is that usernames are unique.')]),
    16: dict(
        hl=[('individuallyand as collectiveset', 1), ('software requirements specification (SRS)', 2), ('Incomplete requirements lead to incomplete designs', 3)],
        notes=['**Complete** applies at two levels. Individually, each requirement is specified thoroughly enough to describe fully the function it asks for.',
               'Collectively, the whole set in the **SRS** (software requirements specification) must cover all the required functionality: nothing missing, everything specified. A perfect login requirement doesn’t make the SRS complete if account recovery was never written down.',
               'Incompleteness propagates: incomplete requirements → incomplete design → incomplete construction.']),
    17: dict(
        hl=[('do not preclude', 1), ('System must be offline only', 2), ('serve nopurpose', 3), ('time, technology, budget', 3), ('1 billion users', 4)],
        notes=['**Consistent**: requirements don’t preclude (prevent) the design or construction of other requirements, i.e. no conflicts.',
               'Consistent pair: “support online payments” and “support credit-card payments” work together. Conflicting pair: “the system must be offline only” and “the system must support online payments”.',
               '**Attainable**: unattainable requirements serve no purpose. A requirement is attainable if it can realistically be achieved within the project’s constraints of time, technology, budget and resources, and this applies to both product and process requirements.',
               'Attainable: “handle 1,000 simultaneous users”. Not attainable: “handle 1 billion users on a $500 budget”.']),
    18: dict(
        hl=[('most obvious desirable', 1), ('cannot be claimed as met', 2), ('serious flaw early on', 2), ('maximize speed', 3), ('at least 1 Mbps', 3)],
        notes=['**Verifiable** is perhaps the most obvious desirable characteristic: there must be a suitable way (test, measurement, demonstration) to confirm the requirement has been met.',
               'A requirement that can’t be verified can’t be claimed as met, and being unable to verify a requirement points to a serious flaw early in development: nobody knows what “done” means.',
               '“The system shall maximise speed” is not verifiable (maximise compared with what?). “The system’s data rate shall be at least 1 Mbps” is. Rule of thumb: use numbers, limits or conditions.'],
        exam=[asked('q261', 'Q15 (true/false)', 'The requirement “The system should respond quickly” is sufficiently specific and verifiable for architectural evaluation.',
                    tf=False, why='“Quickly” is vague unless replaced by a measurable criterion such as “within 2 seconds for 95% of requests”.')]),
    19: dict(
        hl=[('create good', 1), ('4+1 View Model', 2)],
        notes=['This lecture gave the basics of requirements engineering, enough to write good requirements: elicit, analyse, specify and validate, then check each requirement against the six characteristics.',
               'Next: designing the architecture with the **4+1 view model**: logical, development, process and physical views, plus the user (scenario) view that ties them together.']),
}

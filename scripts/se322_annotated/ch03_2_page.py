"""SE322 Chapter 3, Lecture 2 (Major Quality Attributes): page content for the annotated deck.

Schema: see annotated_page.py. Marks with a 4th element 'ocr' are labels inside pictures (skipped if OCR can't
read them). Past-exam questions are copied from the papers in exams/; everything else is a prediction.
Slide 14's general security scenario reuses the performance scenario's environment, response and measure
columns; the note says so.
"""
from .common import asked, likely

TITLE = 'Major Quality Attributes: Definitions, Scenarios and Tactics'
CHAPTER = 'SE322 · Chapter 3 · Lecture 2'

OVERVIEW = {
    'summary': ('Six quality attributes, each in the same three steps: a definition, a general scenario (the possible '
                'values of the six scenario parts) with a concrete example, and a tree of tactics that achieve it. '
                'Availability is about failures and their duration, modifiability about the cost of change, performance '
                'about timeliness, security about resisting unauthorised access, testability about how easily faults can '
                'be revealed, and usability about how easily users accomplish tasks.'),
    'ideas': [
        ('Availability', 'Detect faults (ping/echo, heartbeat, exceptions), prepare and repair (voting, redundancy, spare), reintroduce (shadow, resync, rollback), prevent (removal from service, transactions, process monitor).'),
        ('Modifiability and performance', 'Modifiability: localise changes, prevent ripple effects, defer binding time. Performance: resource demand, management, arbitration.'),
        ('Security and testability', 'Security: resist, detect, recover from attacks. Testability: manage input/output, internal monitoring.'),
        ('Usability', 'Separate the user interface, support user initiative (cancel, undo, aggregate), support system initiative (user, system, task models).'),
    ],
    'sections': [
        ('Slides 2–3', 'Definitions of the major quality attributes'),
        ('Slides 4–6', 'Availability: general scenario, example, tactics'),
        ('Slides 7–10', 'Modifiability: scenarios and tactics'),
        ('Slides 11–13', 'Performance: scenario and tactics'),
        ('Slides 14–16', 'Security: scenario and tactics'),
        ('Slides 17–19', 'Testability: scenario and tactics'),
        ('Slides 20–22', 'Usability: scenario and tactics'),
        ('Slides 23–24', 'Summary and a tactics exercise'),
    ],
    'exam': ('Final 252 Q3 (5 marks) asked you to define three quality attributes and to construct a general availability '
             'scenario; Midterm 252 Q5 asked for an availability scenario; Midterm 261 Q5 asked whether heartbeat is a '
             'performance tactic (it is availability); Quiz 1 261 matched the parts of usability, testability and security '
             'scenarios.'),
}

TITLES = {2: 'Lecture Outlines and quality definitions', 4: 'Availability: general scenario', 6: 'Availability – tactics',
          7: 'Extra: Modifiability – Scenario Example', 8: 'Extra: three modifiability scenarios', 11: 'Performance – Scenario Example',
          15: 'Extra: Security – Scenario Example', 16: 'Security – tactics', 22: 'Usability – tactics', 24: 'Extra: Question – one tactic per quality'}

SLIDES = {
    1: dict(
        hl=[('[Quality Attributes]', 1)],
        notes=['Second quality lecture. Lecture 1 gave the tools (scenarios and tactics); this one applies them to each major quality attribute in turn.']),
    2: dict(
        hl=[('Major Quality Attributes', 1), ('Example with scenario', 1), ('Tactics', 1), ('Usability', 2), ('Availability', 2)],
        notes=['Each quality gets a **definition**, an **example scenario**, and its **tactics**.',
               'The table repeats Chapter 2’s one-line descriptions: usability (complexity of learning or using), modifiability (complexity of changing), security (protecting information), performance (useful work under time and resource limits), reliability (failure rate), portability, testability, availability (uptime), interoperability.']),
    3: dict(
        hl=[('Availability:', 1), ('Modifiability:', 2), ('Performance:', 3), ('Security:', 4), ('Testability:', 5), ('Usability:', 6)],
        notes=['**Availability** is concerned with system failure and the **duration** of failures. A failure means the system does not provide the service it was intended for.',
               '**Modifiability** is about the **cost of change**, in time and money.',
               '**Performance** is about **timeliness**: events occur and the system must respond to them in time.',
               '**Security** is the ability to prevent or resist **unauthorised access while still serving legitimate users**. An attack is an attempt to breach security.',
               '**Testability** is how easily the software can be made to **demonstrate its faults**. To be testable, a system must let testers control its inputs and observe its outputs.',
               '**Usability** is how easy it is for users to accomplish tasks, and what support the system gives them to do so.'],
        exam=[asked('f252', 'Q3-1 · 3 marks', 'List and define three of the major quality attributes of software architecture.',
                    a='Any three, one mark each: **Availability**: the system is ready to carry out its task when needed; concerned with failures and their duration. **Performance**: timeliness, how quickly the system responds to events (latency, throughput). **Security**: the ability to resist unauthorised access while still serving legitimate users. **Modifiability**: the cost in time and money of making a change. **Usability**: how easy the system is to learn and use. **Testability**: how easily the software can be made to show its faults through testing.'),
              likely('Which quality attribute is about the cost of change in time and money?', a=0,
                     opts=['Modifiability', 'Performance', 'Availability', 'Usability'])]),
    4: dict(
        hl=[('General availability scenario', 1), ('Internal to', 2, 0, 'ocr'), ('Crash', 2, 0, 'ocr'), ('Normal operation', 3, 0, 'ocr'),
            ('Prevent the failure', 3, 0, 'ocr'), ('Repair time', 4, 0, 'ocr')],
        notes=['The **general availability scenario** lists every possible value of each part. Pick one value per column to write a concrete scenario.',
               '**Source**: internal or external to the system. **Stimulus** (the fault): crash, omission, timing, no response, incorrect response. **Artifact**: processors, communication channels, persistent storage.',
               '**Environment**: normal operation, start-up, shutdown, repair mode, degraded (fail-safe) mode, overloaded. **Response**: prevent the failure, log it, notify users or operators, disable the source, or be temporarily unavailable.',
               '**Measure**: time interval available, availability %, detection time, repair time, degraded-mode time interval, unavailability time.'],
        exam=[asked('m252', 'Q5d · 1 mark', 'Trip planning system (blackboard design): write an availability quality attribute scenario.',
                    a='**Source**: heartbeat monitor (internal to the system). **Stimulus**: the Trip Planning Service (or a worker) becomes unresponsive or crashes. **Artifact**: the Trip Planning Service process. **Environment**: normal operation. **Response**: detect the failure, inform the operator, fail over to a backup instance and continue to operate. **Response measure**: no downtime (or recovers within 5 seconds, 99.9% availability).')]),
    5: dict(
        hl=[('Switching to a backup server', 1), ('Response Measure:', 2), ('The time taken to restore service', 2), ('6 Steps for Using Quality Attribute', 3)],
        notes=['A concrete availability **response**: if a server becomes unresponsive, switch to a backup server, reallocate resources, or take other corrective action to keep the service running.',
               'The **response measure** judges how well the response worked, focusing on its effect on the whole system: the time taken to restore service, or whether the system kept operating with no downtime.',
               'The right-hand box repeats the six parts with examples: source (user, attacker, system), stimulus (request, failure, attack), environment (under load, during maintenance), artifact (database, server, UI), response (log, retry, deny access), measure (under 2 s, 99% uptime).']),
    6: dict(
        hl=[('Fault Detection', 1), ('Heartbeat', 1), ('Recovery-Preparation and Repair', 2), ('Active redundancy', 2), ('passive redundancy', 2),
            ('Recovery Reintroduction', 3), ('Shadow', 3), ('Resynchronization', 3), ('Prevention', 4), ('Removal from Service', 4)],
        notes=['**Fault detection**: *ping/echo* (send a ping, expect an echo), *heartbeat* (a component sends a regular “I’m alive” signal; a missing beat means a fault), *exceptions* (catch the error when it happens). The goal is to find faults quickly.',
               '**Recovery – preparation and repair**: *voting* (several components compute the result and the majority wins), *active redundancy* (a duplicate runs in parallel, ready to take over instantly), *passive redundancy* (the backup starts only when the primary fails), *spare* (a standby that must be configured before use).',
               '**Recovery – reintroduction** brings a repaired part back: *shadow* (run it alongside the active one, or keep a shadow copy of the state, e.g. a database shadow page to fall back to), *state resynchronisation* (bring its data up to date with the others, e.g. sessions and caches after a server restarts), *rollback* (restore a previous good state).',
               '**Prevention** stops faults recurring: *removal from service* (take a failing component out, e.g. switch off a payment gateway that keeps failing and route customers to another), *transactions* (all-or-nothing updates), *process monitor* (watch processes and restart them). The diagram: a fault enters, tactics act, and the fault is masked or repaired.'],
        exam=[asked('m261', 'Q5 (true/false)', 'Heartbeat is a performance tactic used to reduce response time.',
                    tf=False, why='Heartbeat is an availability tactic for fault detection; it monitors whether a component is still functioning.'),
              likely('What is the difference between active and passive redundancy?',
                     a='In active redundancy the duplicate processes the same inputs in parallel and can take over immediately; in passive redundancy the backup only takes over (after being updated) when the primary fails, so recovery is slower but cheaper.')]),
    7: dict(
        hl=[('Source: End User', 1), ('Source: Developer', 2), ('Source :System Administrator', 3)],
        notes=['Three modifiability scenarios, differing by **who** wants the change. **End user**: cannot change the code, so they *request* changes (“I want dark mode”, “it’s too slow with 500 users”). Environment: run time. Artifact: interfaces, resources, configuration. Response: developers or admins implement and redeploy. Measure: cost in money, time, downtime and user satisfaction.',
               '**Developer**: adds, modifies or deletes functionality or qualities (refactoring, improving security). Environment: design, compile or build time. Artifact: code, components, data. Response: implement → test → integrate. Measure: coding and testing effort, complexity of the changed artifacts.',
               '**System administrator**: changes capacity or technology (scale servers, upgrade the database, adjust configuration). Environment: initialisation or run time. Artifact: configurations, resources, deployment environments. Response: apply → redeploy → test stability. Measure: downtime, effort, risk of errors.']),
    8: dict(
        hl=[('End user', 1), ('Developer', 2), ('system administrator', 3), ('three', 2)],
        notes=['End user version: a user requests a feature or reports a bug that affects the UI or a function; feedback is handled during updates at run time; the team updates the UI or function; success = user satisfaction and fewer complaints.',
               'Developer version: a developer wants to enhance the UI; the change affects the UI code; it is made at design time; the developer updates and tests it; success = done and tested within **three hours** (the classic sample scenario on slide 9).',
               'Administrator version: the system faces more load or needs stronger security; scripts, network setup and security settings change during live operation or planned downtime; success = better reliability, faster responses, improved security.']),
    9: dict(
        hl=[('Sample modifiability scenario', 1, 0, 'ocr'), ('More information about general', 1)],
        notes=['The textbook’s **sample modifiability scenario**: source developer; stimulus wishes to change the UI; artifact code; environment design time; response change made and unit tested; response measure in three hours. Memorise this one as the model answer shape for a modifiability scenario.']),
    10: dict(
        hl=[('Localize Changes', 1), ('Prevention of Ripple Effect', 2), ('Defer Binding Time', 3), ('config file at runtime', 3), ('Response Measures in Context', 4)],
        notes=['**Localise changes**: assign responsibilities so a likely change touches as few modules as possible. Tactics: semantic coherence (keep related responsibilities together), anticipate expected changes, generalise the module, limit possible options, abstract common services. Changing the UI should only touch UI components.',
               '**Prevent ripple effects**: stop a change in one module from forcing changes in others. Tactics: hide information, maintain existing interfaces, restrict communication paths, use an intermediary. Updating a banking app’s UI must not affect how account data is processed.',
               '**Defer binding time**: postpone decisions as late as possible, ideally to run time, so changes need no recompile. Tactics: runtime registration, configuration files, polymorphism, component replacement, adherence to defined protocols. Example: a UI theme read from a config file at run time instead of hard-coded; a language the user can switch while the app runs.',
               'The response measures for modifiability are costs: time, effort and complexity of implementing the change. The diagram’s output: changes made, tested and deployed within time and budget.'],
        exam=[likely('Name the three categories of modifiability tactics and give one tactic for each.',
                     a='Localise changes (semantic coherence, generalise module); prevent ripple effects (hide information, maintain existing interfaces, use an intermediary); defer binding time (configuration files, runtime registration, polymorphism).')]),
    11: dict(
        hl=[('Normal Mode', 1), ('Overload Mode', 1), ('Periodic Events', 2), ('Sporadic Events', 2), ('Bursty Events', 2), ('Latency', 3), ('Throughput', 3), ('Jitter', 3), ('Miss Rate', 3)],
        notes=['**Environment** for performance: normal mode, overload (beyond usual capacity), reduced capacity (maintenance or partial failure), emergency (high-priority work first), peak (highest expected demand). The same system may meet its target in one mode and fail in another.',
               '**Stimulus** = how events arrive: *periodic* (regular, e.g. daily backups), *sporadic* (occasional and unpredictable, e.g. a sudden large upload), *bursty* (sudden spikes, e.g. everyone logging in at once), *stochastic* (random with a probability distribution, e.g. network traffic). Source: internal (a process) or external (users, other systems). Artifact: the component whose performance matters (server, database, network). Response: process the events, or change the level of service (degrade non-essential services to protect core ones).',
               '**Measures**: *latency* (delay before work starts, e.g. 2 s before a video plays), *deadline* (latest finish time, e.g. payment confirmed within 5 s), *throughput* (work per unit time, e.g. 1,000 requests/minute), *jitter* (variation in response time), *miss rate* (share of deadlines missed, e.g. 2 of 100 frames = 2%), *data loss* (data that never arrives).'],
        exam=[likely('Define latency, throughput and jitter as performance response measures.',
                     a='Latency: the delay before a response (or before data starts moving). Throughput: the amount of work done per unit time. Jitter: the variation (inconsistency) in response times.')]),
    12: dict(
        hl=[('Sample performance scenario', 1, 0, 'ocr'), ('More information about general', 1)],
        notes=['The **sample performance scenario**: source users; stimulus initiate transactions; artifact system; environment normal operation; response transactions are processed; response measure average latency of two seconds. The same scenario as Lecture 1, slide 10.']),
    13: dict(
        hl=[('Resource Demand', 1), ('Resource Management', 2), ('Resource Arbitration', 3)],
        notes=['**Resource demand**: reduce the work that reaches the system. Tactics: increase computational efficiency (better algorithms), reduce computational overhead, manage the event rate, control the frequency of sampling.',
               '**Resource management**: make better use of the resources you have. Tactics: introduce concurrency (process requests in parallel), maintain multiple copies (of data or computations, e.g. caches and replicas), increase available resources (faster CPU, more memory).',
               '**Resource arbitration**: decide which task gets a contended resource first, through a **scheduling policy** (FIFO, priority, deadline-first). Events arrive, the tactics act, and the response is generated within time constraints.'],
        exam=[likely('Choosing which waiting request gets the CPU first is which category of performance tactic?', a=0,
                     opts=['Resource arbitration', 'Resource demand', 'Resource management', 'Fault detection'])]),
    14: dict(
        hl=[('General security scenario', 1), ('Hacker from', 2, 0, 'ocr'), ('Attempt to modify', 2, 0, 'ocr'), ('Data within the system', 2, 0, 'ocr'),
            ('Latency', 3, 0, 'ocr')],
        notes=['The **general security scenario**. Read the first three columns: **source** an identified user, an unknown user, or a hacker from outside or inside the organisation.',
               '**Stimulus**: an attempt to display, modify or delete data, or to access system services. **Artifact**: system services, data within the system, a component or resource, data produced or consumed by the system.',
               '**Careful:** the Environment, Response and Measure columns on this slide (normal/overload/peak mode; process events; latency, throughput, jitter) are the **performance** scenario’s values, copied by mistake. For security, the textbook uses: environment online/offline, connected or not, behind a firewall or not; response authenticate, block access, encrypt, log and notify; measure time or effort to break in, probability of detecting the attack, how much data was exposed, time to restore. Use those in an exam.'],
        exam=[likely('Give a correct environment, response and response measure for a security scenario (the slide’s columns belong to performance).',
                     a='Environment: online, connected to the public Internet (or behind a firewall). Response: authenticate the user, block the access, log the attempt and notify an administrator. Response measure: attack detected within 1 minute; account locked after 5 failed attempts; no data exposed; data restored within 1 day.')]),
    15: dict(
        hl=[('Dissatisfied person', 1), ('modify the pay rate data', 1), ('Artifact:', 2), ('Environment:', 2), ('audit trail', 3), ('how quickly the correct data is restored', 4)],
        notes=['A concrete security scenario. **Source**: a dissatisfied person (e.g. an employee) working from a remote location. **Stimulus**: the attempt to modify pay-rate data.',
               '**Artifact**: the targeted payroll data. **Environment**: normal operation.',
               '**Response**: the system maintains an **audit trail**, a record of who did what and when, so the change can be traced.',
               '**Response measure**: how quickly the correct data is restored and whether the source of tampering is identified (the textbook version: correct data restored within a day, source identified).'],
        exam=[asked('q261', 'Q27 (matching)', 'Security scenario: “While the system is connected to the public Internet, an unauthorized external user repeatedly attempts to log in using incorrect credentials to an administrative account. The authentication service rejects the attempts, records the activity, and temporarily locks the account after repeated failures. The system must block the account after 5 failed attempts within 10 minutes and generate an audit record for every attempt.” Match the six elements.',
                    a='Source: unauthorized external user. Stimulus: repeatedly attempts to log in with incorrect credentials. Artifact: authentication service / administrative account. Environment: system connected to the public Internet. Response: rejects the attempts, records the activity, temporarily locks the account. Response measure: account blocked after 5 failed attempts within 10 minutes; an audit record for every attempt.')]),
    16: dict(
        hl=[('Resisting Attacks:', 1), ('Detecting Attacks:', 2), ('Recovering from an Attack:', 3)],
        notes=['**Resisting attacks** (keep them out): authenticate users (who are you?), authorise users (what may you do?), maintain data confidentiality (encryption), maintain integrity (checksums, hashes), limit exposure (fewer entry points), limit access (firewalls, need-to-know).',
               '**Detecting attacks**: intrusion detection, comparing traffic and behaviour against known attack patterns.',
               '**Recovering from an attack**: *restoration* (uses the availability tactics, “see availability” in the tree) and *identification* of the attacker through an **audit trail**. The output: the system detects, resists or recovers from attacks.'],
        exam=[likely('Authenticating and authorising users belong to which category of security tactics?', a=0,
                     opts=['Resisting attacks', 'Detecting attacks', 'Recovering from attacks', 'Resource arbitration'])]),
    17: dict(
        hl=[('General testability scenario', 1), ('Unit tester', 2, 0, 'ocr'), ('Execution of tests', 2, 0, 'ocr'), ('Effort to find fault', 3, 0, 'ocr')],
        notes=['The **general testability scenario**. **Source**: unit, integration, system or acceptance tester, an end user, or automated testing tools.',
               '**Stimulus**: tests are executed because a code increment is complete. **Artifact**: the portion of the system being tested. **Environment**: design, development, compile, integration, deployment or run time.',
               '**Response**: execute the test suite and capture results, capture the cause of a fault, control and monitor the system’s state. **Measures**: effort to find a fault, effort to reach a coverage %, probability that the next test reveals a fault, time to perform tests, effort to detect faults.']),
    18: dict(
        hl=[('Unit Tester', 1), ('completion of a code unit', 1), ('Development environment', 2), ('85% path coverage within three hours', 3)],
        notes=['A concrete testability scenario. **Source**: the unit tester. **Stimulus**: a code unit is completed. **Artifact**: that code unit.',
               '**Environment**: the development environment. **Response**: the test results are captured.',
               '**Response measure**: **85% path coverage within three hours**. Coverage plus a time limit makes the testability goal checkable.'],
        exam=[asked('q261', 'Q26 (matching)', 'Testability scenario: “During pre-release system testing, a QA engineer initiates an automated test suite to verify the order-processing component. The system exposes the required interfaces, records internal test results, and reports failed test cases. The complete test suite must finish within 15 minutes and identify the failing component in at least 95% of injected faults.” Match the six elements.',
                    a='Source: QA engineer. Stimulus: initiates an automated test suite. Artifact: order-processing component. Environment: pre-release system testing. Response: exposes test interfaces, records results and reports failed test cases. Response measure: suite finishes within 15 minutes and identifies the failing component in at least 95% of injected faults.')]),
    19: dict(
        hl=[('Manage Input/Output', 1), ('Internal Monitoring', 2)],
        notes=['**Manage input/output**: control what goes in and observe what comes out. Tactics: *record/playback* (capture real inputs and replay them to reproduce a failure), *separate interface from implementation* (swap in test doubles behind the interface), *specialised access routines/interfaces* (test-only hooks into a component).',
               '**Internal monitoring**: *built-in monitors* that expose the component’s internal state (counters, logs, performance data) during testing. The diagram: an increment is completed, the tactics act, and faults are detected.'],
        exam=[likely('Give two testability tactics.',
                     a='Record/playback and separating interface from implementation (manage input/output); built-in monitors (internal monitoring).')]),
    20: dict(
        hl=[('General usability scenario', 1), ('End user', 2, 0, 'ocr'), ('Learn to use the', 2, 0, 'ocr'), ('Task time', 3, 0, 'ocr')],
        notes=['The **general usability scenario**. **Source**: an end user, possibly in a special role. **Stimulus**: what the user wants: use the system efficiently, learn it, minimise the impact of errors, adapt it, configure it.',
               '**Artifact**: the system, or the part the user is interacting with. **Environment**: run time or configuration time. **Response**: provide the features needed and anticipate the user’s needs.',
               '**Measures**: task time, number of errors, number of tasks accomplished, user satisfaction, gain of user knowledge.']),
    21: dict(
        hl=[('Users who initiate the test', 1), ('downloading and starting the', 1), ('real-time', 2), ('within two minutes', 3)],
        notes=['A concrete usability scenario. **Source**: users. **Stimulus**: downloading and starting a new app. **Artifact**: the system that runs the app.',
               '**Environment**: at run time, while the app is used. **Response**: the user can use the app effectively almost immediately.',
               '**Response measure**: the user is productive **within two minutes** of starting the app. That number is what makes “easy to learn” testable.'],
        exam=[asked('q261', 'Q23 (matching)', 'Usability scenario: “A first-time student user uses the university Learning Management System during normal operation and attempts to submit an assignment for the first time. The system provides clear instructions, guides the student through selecting and uploading the file, and displays a confirmation message after successful submission. The student should complete the task within 2 minutes, without external help, and with no more than one input error.” Match the six elements.',
                    a='Source: first-time student user. Stimulus: attempts to submit an assignment for the first time. Artifact: assignment submission interface / LMS. Environment: normal operation. Response: provides instructions, guides the file upload and confirms success. Response measure: task completed within 2 minutes, without help, with at most one input error.')]),
    22: dict(
        hl=[('Separate User Interface', 1), ('Support User Initiative', 2), ('Undo', 2), ('Support System Initiative', 3), ('User Model', 3)],
        notes=['**Separate the user interface** from the system’s operations, so the UI can change on its own. Example: a blog platform’s visual editor changes the design without touching the code (MVC in Chapter 4 does exactly this).',
               '**Support user initiative**: give users tools to manage their own actions: *cancel* (remove items before checkout), *undo* (revert an edit), *aggregate* (combine many items into one, e.g. a weekly activity summary).',
               '**Support system initiative**: the system anticipates the user using models: a *user model* (recommendations from viewing history), a *system model* (sync the most important emails first), a *task model* (deadline reminders from the project timeline).'],
        exam=[likely('An “Undo” button supports which usability tactic?', a=0,
                     opts=['Support user initiative', 'Support system initiative', 'Separate the user interface', 'Resource arbitration'])]),
    23: dict(
        hl=[('General and sample scenario examples', 1), ('Next … Architecture Design Patterns', 2)],
        notes=['For each major quality you should be able to give the definition, write a general and a sample scenario, and name its tactics.',
               'Next chapter: architecture patterns, ready-made structures that bundle several of these tactics (e.g. MVC separates the UI, a broker hides locations).']),
    24: dict(
        hl=[('List one design tactic', 1), ('Resisting Attacks', 2), ('Separate interface from implementation', 2), ('Localize changes', 2), ('Concurrency', 2)],
        notes=['The exercise: give one tactic per quality attribute. Name the tactic, not the quality again.',
               'Model answers from the slide: **security** resisting or detecting attacks, authenticate users; **testability** separate interface from implementation; **modifiability** localise changes, encapsulation, hide information; **performance** concurrency, increase available resources. Add **availability**: heartbeat or redundancy, and **usability**: undo or cancel.'],
        exam=[likely('List one design tactic for each of: security, testability, modifiability, performance, availability, usability.',
                     a='Security: authenticate users. Testability: record/playback or separate interface from implementation. Modifiability: localise changes (semantic coherence) or hide information. Performance: introduce concurrency or increase resources. Availability: heartbeat or active redundancy. Usability: undo/cancel.')]),
}

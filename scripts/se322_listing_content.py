#!/usr/bin/env python3
"""Content for the SE322 Listing Vault — one page per chapter.

Each chapter is (folder, chapter_label, slug, title, blurb, cards).
A card is a dict:
    title  — card heading
    badge  — small count/label chip
    note   — optional one-line description under the heading
    full   — optional bool, makes the card span the grid
    items  — list of HTML list items (ordered list)
    table  — optional {"cols": [...], "rows": [[...], ...]} instead of items
    groups — optional [(subheading, [items])] rendered as a subgrid
"""

CHAPTERS = [
    # --------------------------------------------------------------- CH 1 ---
    (
        "01-introduction-to-software-design-and-architecture",
        "01",
        "introduction-to-software-design-and-architecture",
        "Introduction to Software Design and Architecture",
        "Foundations: what software engineering claims to be, where design sits in the lifecycle, "
        "who the architecture serves, and what separates an architectural decision from a detailed one.",
        [
            {
                "title": "IEEE Definition — Keywords",
                "badge": "3 + 3",
                "note": "A systematic, disciplined, quantifiable approach to software development, operation and maintenance.",
                "groups": [
                    ("The approach", ["Systematic — repeatable and reviewable",
                                      "Disciplined — follows agreed practice, not taste",
                                      "Quantifiable — measurable against stated targets"]),
                    ("Applied to", ["Development", "Operation", "Maintenance"]),
                ],
            },
            {
                "title": "SDLC Phases",
                "badge": "6",
                "items": ["Requirements", "Design", "Implementation", "Testing", "Deployment", "Maintenance"],
            },
            {
                "title": "Engineering Problem Solving",
                "badge": "6",
                "items": [
                    "Initial state", "Goal state", "Constraints",
                    "Candidate solutions", "Evaluation of candidates", "Implementation",
                ],
            },
            {
                "title": "Why Study Design",
                "badge": "3",
                "items": [
                    "Defects are cheaper to remove before construction",
                    "Costly decisions are easier to reverse on paper",
                    "Cost of change grows roughly by an order of magnitude per phase",
                ],
            },
            {
                "title": "Architecture Addresses",
                "badge": "3",
                "note": "The three things an architecture description is about.",
                "items": [
                    "Elements — the parts the system is built from",
                    "Externally visible properties — provided services, performance, resource use",
                    "Relationships — how the elements are connected and interact",
                ],
            },
            {
                "title": "Architecture vs Detailed Design",
                "badge": "compare",
                "full": True,
                "table": {
                    "cols": ["", "Architecture", "Detailed Design"],
                    "rows": [
                        ["Scope", "System-wide structures", "Individual components and collaborations"],
                        ["Output", "Elements, visible properties, relationships", "Classes, interfaces, algorithms, data structures"],
                        ["Cost to reverse", "Expensive, affects many teams and qualities", "Local and cheaply replaced"],
                        ["Example", "Split the shop into catalog, cart and payment services over HTTP", "Inside the cart, a HashMap keyed by SKU and a Strategy per discount rule"],
                    ],
                },
            },
            {
                "title": "Managing Complexity",
                "badge": "3",
                "items": ["Abstraction", "Decomposition", "Separation of concerns"],
            },
            {
                "title": "Stakeholders &amp; Their Concerns",
                "badge": "5",
                "items": [
                    "<b>Users</b> — usability, reliability",
                    "<b>Developers</b> — modifiability",
                    "<b>Operators</b> — deployability, observability",
                    "<b>Business</b> — time to market, cost, market position",
                    "<b>Maintainers</b> — testability, comprehensibility",
                ],
            },
            {
                "title": "Viewpoint vs View",
                "badge": "2",
                "items": [
                    "<b>Viewpoint</b> — frames particular concerns and says what to show and for whom",
                    "<b>View</b> — the resulting representation of the system from that viewpoint",
                ],
            },
            {
                "title": "Architectural Drivers",
                "badge": "4",
                "note": "The small set of requirements with major architectural influence.",
                "items": [
                    "Business goals",
                    "Functional requirements (only the few that are architecturally significant)",
                    "Quality attributes",
                    "Constraints — mandated technology, regulation, budget, legacy integration",
                ],
            },
            {
                "title": "Design Process Activities",
                "badge": "5",
                "items": [
                    "Understand requirements and context",
                    "Decompose around responsibilities and change boundaries",
                    "Define structures, responsibilities and interfaces",
                    "Record decisions, rationale, assumptions and rejected alternatives",
                    "Validate early with scenarios, prototypes, reviews and risk analysis",
                ],
            },
            {
                "title": "Attribute-Driven Design (ADD) Iteration",
                "badge": "5",
                "items": [
                    "Choose an element to decompose",
                    "Pick the driving requirement for this round",
                    "Select tactics and patterns",
                    "Allocate responsibilities and define interfaces",
                    "Verify, then start the next round",
                ],
            },
            {
                "title": "Qualities of Good Design",
                "badge": "6",
                "items": [
                    "Correctness", "Simplicity", "Cohesion",
                    "Low coupling", "Information hiding", "Evolvability",
                ],
            },
            {
                "title": "Design Challenges",
                "badge": "5",
                "items": [
                    "Volatile, changing requirements",
                    "Inconsistent development processes",
                    "Rapidly changing technology (AI/ML adds fast-moving constraints)",
                    "Competing design influences and conflicting quality goals",
                    "Professional and ethical obligations as real constraints",
                ],
            },
            {
                "title": "Essential vs Accidental Complexity",
                "badge": "2",
                "items": [
                    "<b>Essential</b> — comes from the problem itself and cannot be designed away",
                    "<b>Accidental</b> — comes from our chosen solution and is the part we can remove",
                ],
            },
        ],
    ),
    # --------------------------------------------------------------- CH 2 ---
    (
        "02-software-architecture",
        "02",
        "software-architecture",
        "Software Architecture",
        "Structures, views, requirements engineering, the 4+1 model, architectural decisions, "
        "interfaces and the architecture lifecycle.",
        [
            {
                "title": "The Three Structure Categories",
                "badge": "3",
                "full": True,
                "table": {
                    "cols": ["Structure", "Shows", "Answers"],
                    "rows": [
                        ["Module", "Implementation units and their dependencies", "What can a developer change, and what breaks?"],
                        ["Component-and-connector", "Runtime elements and their interactions", "What is running, and how does it talk?"],
                        ["Allocation", "Software mapped to hardware, teams, files, environments", "Where does it live, and who owns it?"],
                    ],
                },
            },
            {
                "title": "Why Structures Cannot Be One Diagram",
                "badge": "2",
                "items": [
                    "One module can map to many runtime components",
                    "One component can span many modules",
                ],
            },
            {
                "title": "A Viewpoint Defines",
                "badge": "4",
                "items": ["Conventions and notation", "Stakeholders", "Concerns addressed", "Modeling rules"],
            },
            {
                "title": "Requirements Engineering Activities",
                "badge": "5",
                "items": ["Elicitation", "Analysis", "Specification", "Validation", "Management"],
            },
            {
                "title": "Elicitation Techniques",
                "badge": "4",
                "items": ["Interviews", "Facilitated meetings", "Observation", "Scenarios"],
            },
            {
                "title": "Requirements Analysis Includes",
                "badge": "4",
                "items": ["Classification", "Prioritization", "Negotiation", "Conceptual modeling"],
            },
            {
                "title": "Properties of a Good Requirement",
                "badge": "6",
                "items": ["Specific", "Consistent", "Correct", "Attainable", "Complete", "Verifiable"],
            },
            {
                "title": "Requirement Classifications",
                "badge": "2 &times; 2",
                "items": [
                    "<b>Imposed</b> — from outside: law, standards, corporate policy",
                    "<b>Derived</b> — consequences the team infers from imposed ones",
                    "<b>Product-oriented</b> — about the delivered system",
                    "<b>Process-oriented</b> — about how the system is built",
                ],
            },
            {
                "title": "Kruchten 4+1 Views",
                "badge": "5",
                "full": True,
                "table": {
                    "cols": ["View", "Serves", "Typical diagrams"],
                    "rows": [
                        ["Logical", "End users", "Class, collaboration, sequence"],
                        ["Process", "Integrators", "Activity models"],
                        ["Development", "Programmers", "Component, package"],
                        ["Physical", "System engineers", "Deployment"],
                        ["Scenarios (+1)", "All of them — validates the other four", "Use cases, textual flows"],
                    ],
                },
            },
            {
                "title": "ADR Contents",
                "badge": "5",
                "items": ["Context", "Decision", "Alternatives considered", "Consequences", "Status"],
            },
            {
                "title": "ADR Status Values",
                "badge": "4",
                "items": ["Proposed", "Accepted", "Deprecated", "Superseded"],
            },
            {
                "title": "Interface Contract Covers",
                "badge": "6",
                "items": ["Syntax", "Semantics", "Protocols", "Errors", "Timing", "Versioning"],
            },
            {
                "title": "The Two Sides of an Interface",
                "badge": "2",
                "items": [
                    "<b>Provided</b> — the services this element offers",
                    "<b>Required</b> — what it needs from others; document only the provided half and you hide half the coupling",
                ],
            },
            {
                "title": "Making Semantics Checkable",
                "badge": "3",
                "items": ["Preconditions", "Postconditions", "Invariants"],
            },
            {
                "title": "Architecture Lifecycle Activities",
                "badge": "6",
                "items": ["Analysis", "Synthesis", "Documentation", "Implementation", "Evaluation", "Governance"],
            },
            {
                "title": "Erosion vs Drift",
                "badge": "2",
                "items": [
                    "<b>Erosion</b> — the code violates the intended structure",
                    "<b>Drift</b> — the design evolves and the documentation does not follow",
                ],
            },
        ],
    ),
    # --------------------------------------------------------------- CH 3 ---
    (
        "03-quality-attributes",
        "03",
        "quality-attributes",
        "Quality Attributes",
        "Quality scenarios, the seven design decision categories, and the tactic catalogues for "
        "performance, availability, security, modifiability, testability, usability and interoperability.",
        [
            {
                "title": "Six-Part Quality Scenario",
                "badge": "6",
                "full": True,
                "items": [
                    "<b>Source</b> — who or what triggers it",
                    "<b>Stimulus</b> — what arrives",
                    "<b>Environment</b> — the system state at the time (normal, peak, degraded)",
                    "<b>Artifact</b> — the part of the system that is hit",
                    "<b>Response</b> — what the system does",
                    "<b>Response measure</b> — how the response is measured",
                ],
            },
            {
                "title": "General vs Concrete Scenario",
                "badge": "2",
                "items": [
                    "<b>General</b> — reusable, system-independent template",
                    "<b>Concrete</b> — instantiated for this system with real numbers",
                ],
            },
            {
                "title": "Seven Categories of Design Decision",
                "badge": "7",
                "full": True,
                "items": [
                    "Allocation of responsibilities — where behavior and knowledge live",
                    "Coordination model — how elements interact",
                    "Data model — what is stored, where, partitioning, replication and consistency",
                    "Management of resources — threads, memory, connections, bandwidth",
                    "Mapping among architectural elements — what scales, fails or releases independently",
                    "Binding time — compile time, build, startup or run time",
                    "Choice of technology — flexibility traded against complexity and cost",
                ],
            },
            {
                "title": "Performance — Concerns",
                "badge": "5",
                "items": ["Latency", "Throughput", "Capacity", "Deadlines", "Resource use"],
            },
            {
                "title": "Performance — Tactics",
                "badge": "2 groups",
                "groups": [
                    ("Control demand", ["Sampling / manage sampling rate", "Admission control and rate limiting",
                                        "Prioritize events", "Reduce overhead", "Bound execution times"]),
                    ("Manage resources", ["Increase resources", "Introduce concurrency", "Replicate computation or data",
                                          "Bound queue sizes", "Schedule resources"]),
                ],
            },
            {
                "title": "Performance — Measurement Rules",
                "badge": "3",
                "items": [
                    "Measure percentile latency (p95, p99), not averages",
                    "Measure under representative load, not a quiet machine",
                    "Keep headroom — latency rises sharply as utilization nears capacity",
                ],
            },
            {
                "title": "Availability — Definition &amp; Arithmetic",
                "badge": "3",
                "items": [
                    "Readiness for correct service despite faults",
                    "Availability = MTBF / (MTBF + MTTR)",
                    "99.9% &asymp; 8.8 hours downtime/year &middot; 99.99% &asymp; 53 minutes/year",
                ],
            },
            {
                "title": "Availability — Tactics",
                "badge": "4 groups",
                "full": True,
                "groups": [
                    ("Detect faults", ["Ping / echo", "Heartbeat", "Exceptions", "Voting", "Monitor", "Timestamp"]),
                    ("Recover — preparation &amp; repair", ["Active redundancy", "Passive redundancy", "Spare",
                                                            "Rollback", "Retry", "Exception handling"]),
                    ("Recover — reintroduction", ["Shadow operation", "State resynchronization",
                                                  "Escalating restart", "Non-stop forwarding"]),
                    ("Prevent faults", ["Removal from service", "Transactions", "Process monitor", "Predictive model"]),
                ],
            },
            {
                "title": "Fault vs Failure",
                "badge": "2",
                "items": [
                    "<b>Fault</b> — something has gone wrong internally",
                    "<b>Failure</b> — the fault has reached the user; masking it fast enough is a valid strategy",
                ],
            },
            {
                "title": "Security — Properties Protected",
                "badge": "6",
                "items": ["Confidentiality", "Integrity", "Availability",
                          "Authenticity", "Accountability", "Non-repudiation"],
            },
            {
                "title": "Security — Tactic Groups",
                "badge": "4",
                "items": ["Detect attacks", "Resist attacks", "React to attacks", "Recover from attacks"],
            },
            {
                "title": "Security — Core Controls",
                "badge": "5",
                "items": [
                    "Authenticate subjects", "Authorize actions", "Limit exposure and apply least privilege",
                    "Encrypt data", "Audit activity",
                ],
            },
            {
                "title": "Threat Modeling Links",
                "badge": "4",
                "items": ["Assets", "Threats", "Vulnerabilities", "Mitigations"],
            },
            {
                "title": "Modifiability — Tactics",
                "badge": "4",
                "items": [
                    "Reduce the size of a module",
                    "Increase cohesion",
                    "Reduce coupling (encapsulate, use an intermediary, abstract common services)",
                    "Defer binding time",
                ],
            },
            {
                "title": "Testability — Requirements",
                "badge": "4",
                "items": ["Controllability", "Observability", "Isolation", "Repeatability"],
            },
            {
                "title": "Usability — Tactics",
                "badge": "2 groups",
                "groups": [
                    ("Support user initiative", ["Cancel", "Undo", "Pause / resume", "Aggregate"]),
                    ("Support system initiative", ["Maintain a model of the user",
                                                   "Maintain a model of the task",
                                                   "Maintain a model of the system"]),
                ],
            },
            {
                "title": "Interoperability — Requires",
                "badge": "4",
                "items": ["Shared syntax", "Shared semantics", "Shared protocols", "Shared identity assumptions"],
            },
            {
                "title": "Interoperability — Tactics",
                "badge": "3",
                "items": ["Discover service", "Orchestrate", "Tailor interface"],
            },
        ],
    ),
    # --------------------------------------------------------------- CH 4 ---
    (
        "04-architecture-patterns",
        "04",
        "architecture-patterns",
        "Architecture Patterns",
        "Styles and patterns: layered, MVC, pipes and filters, client-server and broker, "
        "repository and blackboard, and event-driven architecture — with their costs, not just their benefits.",
        [
            {
                "title": "Style Categories",
                "badge": "5",
                "full": True,
                "table": {
                    "cols": ["Category", "Members"],
                    "rows": [
                        ["Data-centered", "Repository, Blackboard"],
                        ["Data-flow", "Pipes and Filters (batch sequential)"],
                        ["Distributed", "Client-Server, Broker, Three-tier / n-tier"],
                        ["Interactive", "Model-View-Controller"],
                        ["Hierarchical", "Layered, Main program and subroutine"],
                    ],
                },
            },
            {
                "title": "A Pattern Is Documented As",
                "badge": "4",
                "items": [
                    "Problem", "Context", "Solution",
                    "Consequences — the part that makes it a design tool, not a template",
                ],
            },
            {
                "title": "A Style Is",
                "badge": "2",
                "items": [
                    "A vocabulary of element and connector types",
                    "Constraints on how they may be combined",
                ],
            },
            {
                "title": "Layered — Classic Four Layers",
                "badge": "4",
                "items": ["Presentation", "Business", "Persistence", "Database"],
            },
            {
                "title": "Layered — Benefits",
                "badge": "3",
                "items": ["Portability", "Replaceability of a layer", "Separation of concerns"],
            },
            {
                "title": "Layered — Costs",
                "badge": "3",
                "items": ["Added latency", "Duplicated transformations between layers", "Pressure to bypass layers"],
            },
            {
                "title": "Layered — Open vs Closed",
                "badge": "2 + 1",
                "items": [
                    "<b>Closed layer</b> — a request may only call the layer directly below",
                    "<b>Open layer</b> — a request may skip it",
                    "<b>Sinkhole anti-pattern</b> — most requests pass through layers that add no logic",
                ],
            },
            {
                "title": "MVC — The Three Parts",
                "badge": "3",
                "items": [
                    "<b>Model</b> — domain state; notifies observing views of change and knows no specific view",
                    "<b>View</b> — presentation; observes the model",
                    "<b>Controller</b> — interprets input and updates the model",
                ],
            },
            {
                "title": "MVC — Consequences",
                "badge": "4",
                "items": [
                    "Multiple views can share one model",
                    "UI change is isolated from domain logic",
                    "Interaction complexity increases",
                    "Poor allocation gives fat controllers or anemic models",
                ],
            },
            {
                "title": "MVC — Variants",
                "badge": "2",
                "items": ["MVP — Model-View-Presenter", "MVVM — Model-View-ViewModel"],
            },
            {
                "title": "Pipes and Filters — Properties",
                "badge": "4",
                "items": [
                    "Filters are independent and stateless with respect to their neighbours",
                    "Filters can be reused, reordered and run concurrently",
                    "Throughput is limited by the slowest filter",
                    "A single shared data format is what keeps filters recombinable",
                ],
            },
            {
                "title": "Pipes and Filters — Must Define",
                "badge": "4",
                "items": ["Data formats", "Error propagation", "Backpressure", "Termination"],
            },
            {
                "title": "Pipes and Filters — Poor Fit",
                "badge": "2",
                "items": ["Shared state across filters", "Interactive workflows that go backwards"],
            },
            {
                "title": "Broker — Responsibilities",
                "badge": "4",
                "items": ["Register servers", "Locate a server for the client",
                          "Forward the request", "Return results or exceptions"],
            },
            {
                "title": "Distribution — What Networks Add",
                "badge": "4",
                "items": ["Partial failure", "Latency", "Retries (make operations idempotent)", "Versioning"],
            },
            {
                "title": "Repository vs Blackboard",
                "badge": "2",
                "full": True,
                "table": {
                    "cols": ["", "Repository", "Blackboard"],
                    "rows": [
                        ["Data", "Passive shared data store", "Shared blackboard of partial solutions"],
                        ["Control", "Clients drive control", "Changes to the data decide which agent runs next"],
                        ["Parts", "Central data store + client components", "Blackboard + knowledge sources + controller"],
                        ["Suits", "Consistent shared state, many tools on one model", "Problems with no deterministic solution sequence"],
                        ["Risk", "Bottleneck and coupling point", "Hard to predict, hard to debug"],
                    ],
                },
            },
            {
                "title": "Event-Driven — Topologies",
                "badge": "2",
                "items": [
                    "<b>Mediator</b> — an orchestrator routes the event through a multi-step workflow",
                    "<b>Broker</b> — consumers chain directly, simpler flows, no central coordinator",
                ],
            },
            {
                "title": "Event-Driven — Design For",
                "badge": "4",
                "items": ["Idempotency", "Duplicate delivery", "Eventual consistency", "Failure handling"],
            },
            {
                "title": "Event-Driven — Trade-offs",
                "badge": "2",
                "items": [
                    "<b>Gains</b> — decoupling, scalability, easy fan-out to new consumers",
                    "<b>Costs</b> — ordering, debugging without a call stack (needs correlation IDs and tracing)",
                ],
            },
        ],
    ),
    # --------------------------------------------------------------- CH 5 ---
    (
        "05-principles-of-detailed-design",
        "05",
        "principles-of-detailed-design",
        "Principles of Detailed Design",
        "The detailed-design workflow, object-oriented modeling, cohesion and coupling ladders, "
        "SOLID, composition over inheritance and the named code smells.",
        [
            {
                "title": "Detailed-Design Tasks",
                "badge": "8",
                "full": True,
                "items": [
                    "Understand the architecture and the requirements",
                    "Design external interfaces",
                    "Design internal interfaces",
                    "Design the GUI",
                    "Design component structure and behavior",
                    "Design data and the database",
                    "Evaluate and document the design",
                    "Manage implementation of the design",
                ],
            },
            {
                "title": "Design Documentation Artifacts",
                "badge": "3",
                "items": ["Interface control documents", "Data dictionaries", "Version-controlled design records"],
            },
            {
                "title": "OO Relationships",
                "badge": "5",
                "full": True,
                "table": {
                    "cols": ["Relationship", "Meaning", "Lifetime"],
                    "rows": [
                        ["Association", "One class uses or refers to another", "Independent"],
                        ["Aggregation", "Has-a, shared parts", "Part survives the whole"],
                        ["Composition", "Has-a, exclusive parts", "Part dies with the whole"],
                        ["Generalization", "Is-a (inheritance)", "&mdash;"],
                        ["Realization", "A classifier implements an interface", "&mdash;"],
                    ],
                },
            },
            {
                "title": "Class Kinds",
                "badge": "2",
                "items": [
                    "<b>Abstract</b> — defers some implementation, cannot be instantiated",
                    "<b>Concrete</b> — fully implemented, can be instantiated",
                ],
            },
            {
                "title": "Cohesion Ladder",
                "badge": "7",
                "note": "Weakest at the top, strongest at the bottom.",
                "items": ["Coincidental", "Logical", "Temporal", "Procedural",
                          "Communicational", "Sequential", "Functional &larr; the goal"],
            },
            {
                "title": "Coupling Ladder",
                "badge": "5",
                "note": "Worst at the top, preferred at the bottom.",
                "items": ["Content &larr; worst", "Common", "Control", "Stamp", "Data &larr; preferred"],
            },
            {
                "title": "Ways to Reduce Coupling",
                "badge": "3",
                "items": ["Program to interfaces", "Communicate through events", "Invert dependencies"],
            },
            {
                "title": "Abstraction &amp; Encapsulation Rules",
                "badge": "4",
                "items": [
                    "Program to contracts, not concrete details",
                    "Information hiding localizes likely change",
                    "Encapsulation includes behavioral invariants, not only private fields",
                    "Parnas: modularize around the decisions most likely to change",
                ],
            },
            {
                "title": "SOLID",
                "badge": "5",
                "full": True,
                "table": {
                    "cols": ["Principle", "Statement", "Violation cue"],
                    "rows": [
                        ["S — Single Responsibility", "One reason to change; aligned to one actor",
                         "A class serving finance and operations at once"],
                        ["O — Open/Closed", "Open to extension, closed to modification",
                         "A growing switch statement edited for every new case"],
                        ["L — Liskov Substitution", "Subtypes must preserve client expectations",
                         "An override that throws UnsupportedOperationException"],
                        ["I — Interface Segregation", "No client depends on operations it does not use",
                         "Implementers stubbing out methods they never need"],
                        ["D — Dependency Inversion", "Policy and detail both depend on abstractions",
                         "The domain importing the database driver"],
                    ],
                },
            },
            {
                "title": "LSP Rules",
                "badge": "2",
                "items": [
                    "A subtype may not strengthen preconditions",
                    "A subtype may not weaken postconditions",
                ],
            },
            {
                "title": "Dependency Inversion — The Detail",
                "badge": "3",
                "items": [
                    "The abstraction is owned by the high-level module, so the detail conforms to policy",
                    "Dependency injection supplies collaborators from outside",
                    "DI is a mechanism; DIP is the goal — you can have one without the other",
                ],
            },
            {
                "title": "Composition over Inheritance",
                "badge": "3",
                "items": [
                    "Inheritance binds subclass to superclass implementation at compile time",
                    "Composition can be reconfigured at run time",
                    "Composition avoids the fragile base class problem",
                ],
            },
            {
                "title": "Named Code Smells &rarr; Refactoring",
                "badge": "6",
                "full": True,
                "table": {
                    "cols": ["Smell", "Usual refactoring"],
                    "rows": [
                        ["Long method", "Extract method"],
                        ["Large class", "Extract class"],
                        ["Long parameter list", "Introduce parameter object"],
                        ["Shotgun surgery", "Move method / move field to gather the change"],
                        ["Feature envy", "Move method to the class it envies"],
                        ["Duplicated code", "Extract method, pull up to a common place"],
                    ],
                },
            },
            {
                "title": "Refactoring Ground Rules",
                "badge": "3",
                "items": [
                    "Refactoring is behavior-preserving by definition",
                    "Automated tests make safe incremental refactoring possible",
                    "Smells indicate design pressure, not an automatic rewrite command",
                ],
            },
        ],
    ),
    # --------------------------------------------------------------- CH 6 ---
    (
        "06-creational-design-patterns",
        "06",
        "creational-design-patterns",
        "Creational Design Patterns",
        "GoF classification, the five creational patterns, and the question each one answers "
        "about what varies when an object is built.",
        [
            {
                "title": "GoF Classification",
                "badge": "3 &times; 2",
                "groups": [
                    ("By purpose", ["Creational — how objects get created",
                                    "Structural — how classes and objects are composed",
                                    "Behavioral — how behavior and communication are distributed"]),
                    ("By scope", ["Class — varies through inheritance",
                                  "Object — varies through composition"]),
                ],
            },
            {
                "title": "A Pattern Entry Documents",
                "badge": "6",
                "items": ["Intent", "Applicability", "Structure", "Participants", "Consequences", "Examples"],
            },
            {
                "title": "The Five Creational Patterns",
                "badge": "5",
                "full": True,
                "table": {
                    "cols": ["Pattern", "Scope", "Intent"],
                    "rows": [
                        ["Factory Method", "Class", "Define a creation operation and let subclasses choose the concrete product"],
                        ["Abstract Factory", "Object", "Create families of related products without naming concrete classes"],
                        ["Builder", "Object", "Build a complex object step by step, separating construction from representation"],
                        ["Prototype", "Object", "Create new objects by copying a configured prototype"],
                        ["Singleton", "Object", "Ensure one instance with a well-known access point"],
                    ],
                },
            },
            {
                "title": "Factory Method — Key Points",
                "badge": "4",
                "items": [
                    "The creator uses the product but delegates the <code>new</code> to an overridable factory method",
                    "Removes direct construction from client policy",
                    "Use when the product type varies through extension",
                    "Cost: extra classes and one more level of indirection",
                ],
            },
            {
                "title": "Abstract Factory — Key Points",
                "badge": "4",
                "items": [
                    "Enforces compatibility within a product family",
                    "Clients depend on abstract product and factory interfaces",
                    "Adding a new family is easy — one new class",
                    "Adding a new product kind changes the interface and every factory",
                ],
            },
            {
                "title": "Builder — Key Points",
                "badge": "4",
                "items": [
                    "Handles optional parameters, validation and multiple representations",
                    "A director can encode a reusable construction sequence",
                    "Avoids telescoping constructors, at the cost of ceremony",
                    "Validation belongs in <code>build()</code> — the one point where the object is complete",
                ],
            },
            {
                "title": "Prototype — Key Points",
                "badge": "4",
                "items": [
                    "Use when construction is expensive or runtime types vary",
                    "Deep versus shallow copying must be a deliberate decision",
                    "Hazards: identity, shared references, mutable state",
                    "A prototype registry lets clients ask for a copy by key",
                ],
            },
            {
                "title": "Singleton — Key Points",
                "badge": "4",
                "items": [
                    "Complications: concurrency, lifecycle, serialization, class loaders",
                    "A naive lazy <code>getInstance()</code> is not thread-safe",
                    "Fixes: eager static field, double-checked locking, or an enum",
                    "Costs: global state, hidden dependencies, harder testing",
                ],
            },
            {
                "title": "Pattern Selection Guide",
                "badge": "4",
                "full": True,
                "table": {
                    "cols": ["What varies", "Pattern"],
                    "rows": [
                        ["Many kinds of one product, chosen by extension", "Factory Method"],
                        ["Families of products that must stay consistent", "Abstract Factory"],
                        ["One product with many optional parts or representations", "Builder"],
                        ["Expensive or run-time-configured setup to reuse", "Prototype"],
                        ["Singularity is a genuine invariant", "Singleton"],
                    ],
                },
            },
            {
                "title": "Selection Ground Rules",
                "badge": "3",
                "items": [
                    "Start with a plain constructor; add a pattern when the construction decision itself changes",
                    "Prefer the simplest mechanism that preserves the required flexibility",
                    "Patterns combine — an Abstract Factory is often a Singleton whose methods are Factory Methods",
                ],
            },
        ],
    ),
    # -------------------------------------------------------------- CH 7a ---
    (
        "07-structural-design-patterns",
        "07",
        "structural-design-patterns",
        "Structural Design Patterns",
        "How classes and objects are composed into larger structures: Adapter, Bridge, Composite, "
        "Decorator, Facade and Proxy — and the pairs that are easy to confuse.",
        [
            {
                "title": "The Structural Family",
                "badge": "6",
                "full": True,
                "table": {
                    "cols": ["Pattern", "One-line intent"],
                    "rows": [
                        ["Adapter", "Translate one interface into another a client expects"],
                        ["Bridge", "Separate an abstraction from its implementation so both vary independently"],
                        ["Composite", "Represent part-whole hierarchies so leaves and composites look alike"],
                        ["Decorator", "Attach responsibilities dynamically by wrapping an object"],
                        ["Facade", "Provide a simpler entry point to a complex subsystem"],
                        ["Proxy", "Control access to another object through the same interface"],
                    ],
                },
            },
            {
                "title": "Adapter — Key Points",
                "badge": "4",
                "items": [
                    "Object adapter uses composition; class adapter uses inheritance where supported",
                    "Changes the interface, not the core responsibility",
                    "Common at legacy and third-party boundaries",
                    "A two-way adapter implements both interfaces so either side can use the object",
                ],
            },
            {
                "title": "Bridge — Key Points",
                "badge": "4",
                "items": [
                    "Prevents subclass explosion across two independent dimensions of change",
                    "The abstraction delegates implementation-specific work to an implementor",
                    "m abstractions &times; n implementations becomes m + n classes instead of m &times; n",
                    "Refined abstractions extend one side without touching the other",
                ],
            },
            {
                "title": "Composite — Key Points",
                "badge": "4",
                "items": [
                    "Clients treat leaves and composites uniformly — no conditionals",
                    "Recursive operations make tree processing simple",
                    "Needs care with ownership, cycles and traversal policy",
                    "Participants: Component, Leaf, Composite, Client",
                ],
            },
            {
                "title": "Composite — Transparent vs Safe",
                "badge": "2",
                "items": [
                    "<b>Transparent</b> — child management lives on the Component; uniform but leaves expose meaningless operations",
                    "<b>Safe</b> — child management lives only on the Composite; type-safe but clients must check types",
                ],
            },
            {
                "title": "Decorator — Key Points",
                "badge": "4",
                "items": [
                    "The decorator shares the component's interface and holds a reference to it",
                    "It adds behavior before, after or instead of forwarding",
                    "Composes features without subclass explosion",
                    "Order of wrapping can change behavior; many small wrappers complicate identity and debugging",
                ],
            },
            {
                "title": "Facade — Key Points",
                "badge": "4",
                "items": [
                    "Simplifies an existing interface without adding functionality",
                    "Reduces client coupling but does not forbid direct subsystem access",
                    "Often the natural entry point of a layer",
                    "Risk: it grows into an all-knowing god object",
                ],
            },
            {
                "title": "Proxy — The Four Kinds",
                "badge": "4 + 1",
                "items": [
                    "<b>Remote</b> — represents an object in another address space",
                    "<b>Virtual</b> — defers creating an expensive object until it is needed",
                    "<b>Protection</b> — checks access rights before forwarding",
                    "<b>Caching</b> — stores results of expensive calls",
                    "<b>Smart reference</b> — adds reference counting, lazy loading or locking",
                ],
            },
            {
                "title": "Easily Confused Pairs",
                "badge": "4",
                "full": True,
                "table": {
                    "cols": ["Pair", "The distinguishing question"],
                    "rows": [
                        ["Proxy vs Decorator", "Same structure — Proxy controls access, Decorator adds responsibilities"],
                        ["Adapter vs Bridge", "Adapter is applied after the fact; Bridge is designed in up front"],
                        ["Facade vs Adapter", "Facade simplifies an interface; Adapter converts one interface to another"],
                        ["Composite vs Decorator", "Composite composes many children; Decorator wraps exactly one component"],
                    ],
                },
            },
            {
                "title": "Emphasized in This Course",
                "badge": "3",
                "note": "The lecture's own summary table names these three as the structural patterns covered.",
                "items": ["Adapter", "Composite", "Facade"],
            },
        ],
    ),
    # -------------------------------------------------------------- CH 7b ---
    (
        "07-behavioral-design-patterns",
        "07",
        "behavioral-design-patterns",
        "Behavioral Design Patterns",
        "How behavior and communication are distributed among objects. The lecture covers Iterator "
        "and Observer in detail and names the rest of the family for recognition.",
        [
            {
                "title": "Definition &amp; Mnemonic",
                "badge": "I.O.",
                "items": [
                    "Behavioral patterns are responsible for the efficient and safe distribution of behaviors among a program's objects",
                    "<b>I</b>terate &mdash; Iterator gives a standard way to <b>walk</b> a collection",
                    "<b>O</b>bserve &mdash; Observer gives a standard way to <b>watch</b> an object for changes",
                ],
            },
            {
                "title": "The Behavioral Family",
                "badge": "11",
                "full": True,
                "note": "Covered in detail: Iterator and Observer. The rest are named so you recognize them as behavioral.",
                "items": [
                    "Chain of Responsibility", "Command", "Interpreter",
                    "<b>Iterator</b> &mdash; covered", "Mediator", "Memento",
                    "<b>Observer</b> &mdash; covered", "State", "Strategy",
                    "Template Method", "Visitor",
                ],
            },
            {
                "title": "Iterator — Intent",
                "badge": "2 keys",
                "items": [
                    "Access the elements of a collection <b>sequentially</b>, one after another in a defined order",
                    "<b>Without knowing the representation</b> — array, linked list or tree, no client breaks",
                ],
            },
            {
                "title": "Iterator — Participants",
                "badge": "5",
                "items": [
                    "<b>Client</b> — talks to the Aggregate and Iterator interfaces only",
                    "<b>Aggregate</b> — declares <code>createIterator()</code>",
                    "<b>ConcreteAggregate</b> — returns a concrete iterator over its own data",
                    "<b>Iterator</b> — declares <code>hasNext()</code> and <code>next()</code>",
                    "<b>ConcreteIterator</b> — holds the position and accesses the concrete aggregate",
                ],
            },
            {
                "title": "Iterator — Build Order (I.C.C.A.)",
                "badge": "5 steps",
                "items": [
                    "<b>I</b> — design the Iterator interface",
                    "<b>C</b> — design a concrete Iterator for each collection structure",
                    "Implement its methods in terms of that data structure",
                    "<b>C</b> — create the Collection interface with the iterator-creating method",
                    "<b>A</b> — implement the Aggregate interface in each collection class",
                ],
            },
            {
                "title": "Iterator — Benefits",
                "badge": "3",
                "items": [
                    "A consistent way for clients to iterate over any collection",
                    "Abstracts the internals — collections can change without changing clients",
                    "Extensible — many iterators for different traversals (standard, reverse, filtered)",
                ],
            },
            {
                "title": "Iterator — The Key Detail",
                "badge": "1",
                "items": [
                    "The position lives on the <b>iterator</b>, not the collection — so several iterators can walk one collection independently",
                ],
            },
            {
                "title": "Observer — Intent",
                "badge": "3 keys",
                "items": [
                    "<b>One-to-many</b> — one Subject, many Observers",
                    "<b>Dependency</b> — observers care about the subject's state; the subject does not care what they do with it",
                    "<b>Automatically</b> — nobody polls; the subject pushes the notification on state change",
                ],
            },
            {
                "title": "Observer — Participants",
                "badge": "4",
                "items": [
                    "<b>Subject</b> — holds the observer list; <code>attach()</code>, <code>detach()</code>, <code>notifyAll()</code>",
                    "<b>ConcreteSubject</b> — holds the state and notifies on change",
                    "<b>Observer</b> — declares the abstract <code>update()</code>",
                    "<b>ConcreteObserver</b> — implements <code>update()</code> and registers itself",
                ],
            },
            {
                "title": "Observer — Build Order (S.I.O.I.R.)",
                "badge": "5 steps",
                "items": [
                    "<b>S</b> — design the Subject interface with attach, detach and notify",
                    "<b>I</b> — inherit from it in classes holding information of interest",
                    "<b>O</b> — design the Observer interface with an abstract <code>update()</code>",
                    "<b>I</b> — implement <code>update()</code> in every observer",
                    "<b>R</b> — register observers at run time; the subject iterates and calls update on change",
                ],
            },
            {
                "title": "Observer — Benefits",
                "badge": "2",
                "items": [
                    "Flexibility to add new services without touching the Subject",
                    "Services are compartmentalized, so maintaining and modifying them is easier",
                ],
            },
            {
                "title": "Iterator vs Observer",
                "badge": "compare",
                "full": True,
                "table": {
                    "cols": ["", "Iterator", "Observer"],
                    "rows": [
                        ["Solves", "Walking a collection without knowing how it stores elements",
                         "Many objects reacting the moment one object's state changes"],
                        ["Relationship", "One client to one traversal at a time", "One Subject to many Observers"],
                        ["Cue phrase", "\"access the elements sequentially without exposing the representation\"",
                         "\"one-to-many dependency, notified automatically\""],
                        ["Where they meet", "The Subject <em>iterates</em> its observer list inside notifyAllObservers()", ""],
                    ],
                },
            },
            {
                "title": "The Three Categories, Side by Side",
                "badge": "3",
                "full": True,
                "table": {
                    "cols": ["Category", "Concerned with", "This course's patterns"],
                    "rows": [
                        ["Creational", "How objects get created",
                         "Abstract Factory, Factory Method, Singleton, Builder, Prototype"],
                        ["Structural", "How classes and objects are composed into larger structures",
                         "Adapter, Composite, Facade"],
                        ["Behavioral", "How behavior and communication are distributed",
                         "Iterator, Observer"],
                    ],
                },
            },
        ],
    ),
    # --------------------------------------------------------------- CH 8 ---
    (
        "08-architecture-evaluation",
        "08",
        "architecture-evaluation",
        "Architecture Evaluation",
        "Why architectures are evaluated, the three methods, and the nine ATAM steps with the "
        "outputs an evaluation is supposed to produce.",
        [
            {
                "title": "Purpose of Evaluation",
                "badge": "4",
                "items": [
                    "Check that decisions satisfy business goals and quality requirements",
                    "Expose risks, sensitivity points, trade-off points and missing information",
                    "Evaluate early and repeat when drivers or the architecture change",
                    "Aim for informed decisions, not a pass/fail verdict",
                ],
            },
            {
                "title": "The Four Output Concepts",
                "badge": "4",
                "full": True,
                "table": {
                    "cols": ["Concept", "Definition"],
                    "rows": [
                        ["Risk", "A decision or gap that endangers a quality goal — e.g. failover never tested under load"],
                        ["Non-risk", "A decision checked and found sound, with the reason recorded"],
                        ["Sensitivity point", "A property where a change strongly affects <b>one</b> quality attribute"],
                        ["Trade-off point", "A property that is a sensitivity point for <b>two or more</b> attributes at once"],
                    ],
                },
            },
            {
                "title": "The Three Evaluation Methods",
                "badge": "3",
                "full": True,
                "table": {
                    "cols": ["Method", "Focus", "Use when"],
                    "rows": [
                        ["SAAM", "Scenario-based modifiability and functionality; came first",
                         "The question is how costly a set of planned changes will be"],
                        ["ATAM", "All quality attributes and their interactions; generalized SAAM",
                         "A finished architecture has competing quality goals"],
                        ["ARID", "Active design review of an intermediate, unfinished design",
                         "A partial design must be validated by the teams that will use it"],
                    ],
                },
            },
            {
                "title": "ATAM — The Nine Steps",
                "badge": "9",
                "full": True,
                "items": [
                    "Present the ATAM method",
                    "Present the business drivers",
                    "Present the architecture",
                    "Identify the architectural approaches",
                    "Generate the quality attribute utility tree",
                    "Analyze the architectural approaches",
                    "Brainstorm and prioritize scenarios",
                    "Analyze the architectural approaches again (with the prioritized scenarios)",
                    "Present the results",
                ],
            },
            {
                "title": "ATAM — Phases",
                "badge": "3",
                "items": [
                    "<b>Preparation / Phase 1</b> — work with the core design team",
                    "<b>Evaluation / Phase 2</b> — widen to the broader stakeholder group",
                    "<b>Follow-up / Phase 3</b> — deliver the report and track the actions",
                ],
            },
            {
                "title": "ATAM — Participants",
                "badge": "3",
                "items": [
                    "The evaluation team and its roles",
                    "Project decision makers",
                    "Architecture stakeholders",
                ],
            },
            {
                "title": "ATAM — Outputs",
                "badge": "7",
                "items": [
                    "The utility tree", "The architectural approaches", "The prioritized scenarios",
                    "Risks", "Non-risks", "Sensitivity points", "Trade-off points",
                ],
            },
            {
                "title": "Utility Tree Structure",
                "badge": "4 levels",
                "items": [
                    "<b>Utility</b> — the root",
                    "<b>Quality attribute</b> — performance, availability, security, modifiability…",
                    "<b>Refinement</b> — a narrower concern within that attribute",
                    "<b>Concrete scenario</b> — a leaf, rated (importance, difficulty) such as (H,H)",
                ],
            },
            {
                "title": "Prioritization Rule",
                "badge": "1",
                "items": [
                    "(H,H) leaves are analyzed first — most business value and most architectural uncertainty",
                ],
            },
            {
                "title": "Scenario Parts Used in Evaluation",
                "badge": "5",
                "items": ["Stimulus", "Environment", "Artifact", "Response", "Response measure"],
            },
            {
                "title": "Analysis Discipline",
                "badge": "4",
                "items": [
                    "Trace each scenario through runtime and development structures",
                    "Record the decisions each approach embodies and the questions asked about it",
                    "Prototype or measure where reasoning alone is weak",
                    "Keep assumptions and evidence visibly separate",
                ],
            },
            {
                "title": "Review Outcomes to Capture",
                "badge": "5",
                "items": [
                    "Risks and non-risks", "Risk themes grouped from related weaknesses",
                    "Decisions made during the review", "Open questions",
                    "Recommended experiments, each with an owner and a date",
                ],
            },
        ],
    ),
    # --------------------------------------------------------------- CH 9 ---
    (
        "09-architecture-documentation",
        "09",
        "architecture-documentation",
        "Architecture Documentation",
        "The documentation rules, what belongs in a view, the established view approaches, "
        "what lives beyond views, and how documentation stays alive.",
        [
            {
                "title": "Documentation Principles",
                "badge": "7",
                "full": True,
                "items": [
                    "Write from the reader's point of view",
                    "Avoid unnecessary repetition — one source of truth per fact",
                    "Avoid ambiguity; define the notation",
                    "Use a standard organization and provide a roadmap",
                    "Record rationale",
                    "Keep documentation current",
                    "Review documentation for fitness with its intended readers",
                ],
            },
            {
                "title": "What Belongs in a View",
                "badge": "5",
                "full": True,
                "items": [
                    "<b>Primary presentation</b> — usually a diagram plus key annotations",
                    "<b>Element catalog</b> — responsibilities, interfaces and relationships",
                    "<b>Context diagram</b> — the view boundary and external dependencies",
                    "<b>Variability guide</b> — where options exist and their permitted values",
                    "<b>Rationale</b> — why the view looks this way and what was rejected",
                ],
            },
            {
                "title": "Variability Binding Times",
                "badge": "3",
                "items": ["Configurable", "Build-time choice", "Run-time setting"],
            },
            {
                "title": "Established View Approaches",
                "badge": "6 + 1",
                "items": [
                    "Kruchten 4+1", "Siemens Four-Views", "Herzum and Sims",
                    "Software Cost Reduction (SCR)", "RUP", "SEI Views and Beyond",
                    "C4 — a widely used modern variant",
                ],
            },
            {
                "title": "Siemens Four Views",
                "badge": "4",
                "items": ["Conceptual", "Module", "Execution", "Code"],
            },
            {
                "title": "C4 Levels",
                "badge": "4",
                "items": ["Context", "Container", "Component", "Code"],
            },
            {
                "title": "A Complete Documentation Package",
                "badge": "7",
                "full": True,
                "items": [
                    "Documentation roadmap — which part answers which question",
                    "The view documents themselves",
                    "System overview",
                    "Rationale and decisions (ADRs)",
                    "Directory / index",
                    "Glossary",
                    "Acronym list",
                ],
            },
            {
                "title": "Cross-Cutting Concerns",
                "badge": "6",
                "note": "Belong to no single view but constrain all of them.",
                "items": ["Interfaces", "Data", "Security", "Error handling", "Deployment", "Build concerns"],
            },
            {
                "title": "Diagram Quality Rules",
                "badge": "5",
                "items": [
                    "Every diagram needs a key defining shapes, line styles and colors",
                    "Boxes and lines are ambiguous without defined semantics",
                    "Show only what is relevant to the view and audience",
                    "One diagram should answer one question",
                    "Automated diagrams help freshness but still need curation",
                ],
            },
            {
                "title": "Living Documentation",
                "badge": "5",
                "items": [
                    "Version documentation with the code where appropriate",
                    "Review for drift and link decisions to implementation evidence",
                    "Make documentation part of the definition of done",
                    "Generate what changes most often — API references, dependency graphs, topologies",
                    "Concise enough to maintain, detailed enough to act on",
                ],
            },
        ],
    ),
]

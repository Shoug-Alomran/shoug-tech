"""SE322 annotated slides — Chapter 5, Lecture 3: ISP, DIP, internal behaviour and the rules of design.
See ch01_introduction.py for AUTO_SLIDES and the ANN keys."""
from .common import mcq, past, scen, see, short, tf, tip, trap, trick

AUTO_SLIDES = 'all'
OVERVIEW = 'This chapter refines architecture into implementable component designs. It covers the detailed-design workflow, object-oriented structure, all five SOLID principles, behavior modeling, and practical rules for making designs clear, changeable, and testable.'

DECK = {
    'key': 'ch5.3',
    'slug': '12-principles-of-detailed-design-lecture-3',
    'file': 'principles-of-detailed-design-lecture-3',
    'title': 'Principles of Detailed Design: ISP, DIP and the Rules of Design',
    'chapter': 'Chapter 5 · Lecture 3',
    'page': 'ch05_3_page',  # notes, highlights and exam questions in the page schema
    'pdf': '/academics/software-engineering/se322/slides/chapter-5-principles-of-detailed-design-lecture-3-extra/',
    'lede': ('The last two SOLID principles (interface segregation with the game characters, dependency inversion '
             'with Manager and Worker), modelling a component’s internal behaviour with sequence diagrams, and the '
             'rules of design and common design mistakes.'),
}

ANN = {
    1: dict(kind='title', title='Principles of Detailed Design', body=[], sub='SE322 · Chapter 5, Lecture 3'),
    2: dict(notes=['This lecture completes SOLID with Interface Segregation and Dependency Inversion, then applies modelling rules and common design checks. The goal is focused contracts and stable dependency direction.'], seen=[see('ch5.2', 18, 'SRP, OCP and LSP')]),
    3: dict(notes=['**ISP**: classes should not be forced to depend on methods they don’t use. Game: land, air and water enemies plus a SuperCharacter that does all three.'],
            exam=[mcq('“Clients should not be forced to depend on methods they do not use” is the:', ['Interface Segregation Principle', 'Dependency Inversion Principle', 'Open-Closed Principle', 'Liskov Substitution Principle'], 0, '')], weight=3),
    4: dict(notes=['One fat interface pollutes classes with unused methods (an aerial character forced to have run()). Many client-specific interfaces beat one general-purpose interface.'],
            tips=[trick('ISP = small, role-specific interfaces (IRunner, IFlyer, ISwimmer).')], weight=3),
    5: dict(notes=['A fat interface may also violate LSP when only SuperCharacter can honor every operation. Other character types would need to reject valid-looking calls or provide misleading behavior.']),
    6: dict(notes=['Split the broad interface into focused movement capabilities. Each class implements only the operations it can truly support; SuperCharacter can implement all of them.']),
    7: dict(notes=['Read the ISP diagram by matching each type to the capabilities it supports. A client should depend on the narrow capability it uses, while a class may implement several independent interfaces.']),
    8: dict(hl_boxes=[(0.02, 0.025, 0.36, 0.07)], notes=['Walk through the code from the contracts to the concrete classes. `SuperCharacter` declares fly(), run(), and swim(), but separate interfaces such as `AerialCharacter`, `TerrestrialCharacter`, and `AquaticCharacter` each extend it with only the capability relevant to that role. The clients then implement the narrow interface they need: the aerial client supplies fly(), the terrestrial client supplies run(), and the aquatic client supplies swim(). `SuperCharacterClient` can still implement the broad interface because it supports all three operations. In `main`, each specialized reference is created and only its supported method is called; the final calls through the broad `SuperCharacter` reference work because that object implements the full contract. This makes unsupported operations impossible to request through specialized references and avoids forcing every class to provide meaningless methods.']),
    9: dict(notes=['**DIP**: source-code dependencies should point to abstractions (interfaces, abstract classes), not concrete, frequently changing modules.']),
    10: dict(notes=['High-level modules must not depend on low-level modules; both depend on abstractions. Abstractions don’t depend on details; details depend on abstractions.'],
             exam=[mcq('According to DIP, high-level modules should depend on:', ['Abstractions', 'Low-level modules', 'Concrete classes', 'Global variables'], 0, '')], weight=3),
    11: dict(notes=['The DIP illustration shows high-level policy and low-level details connected through an abstraction. The source dependency points toward the stable contract even when runtime calls reach a concrete implementation.']), 12: dict(notes=['Trace both arrows carefully: the manager’s source code refers to the worker interface, so compile-time dependency points inward to the abstraction. At runtime, a concrete worker implements that interface and receives the call. Replacing the worker changes the wiring, not the manager’s policy code.']),
    13: dict(notes=['Manager’s concrete Worker field couples high-level coordination logic to one low-level worker implementation. Adding a new type or substituting a test double requires changing the manager.']),
    14: dict(notes=['Fix: Manager depends on the IWorker interface; RobotWorker, AIWorker, InternWorker can be added without changing Manager.'],
             exam=[scen('A Manager class holds a Worker object directly. Which principle is violated and how do you fix it?', 'The Dependency Inversion Principle: the high-level Manager depends on the concrete low-level Worker. Introduce an IWorker interface with work(); Worker and any new worker types implement it, and Manager holds an IWorker. Manager then works with any worker type without modification.')],
             weight=3),
    15: dict(notes=['Internal STRUCTURE of a component → class diagram. Internal BEHAVIOUR → sequence diagram.'],
             exam=[mcq('A component’s internal behaviour is modelled with a:', ['Sequence diagram', 'Class diagram', 'Deployment diagram', 'Package diagram'], 0, '')], weight=2),
    16: dict(notes=['Clarify the problem, requirements, and constraints before choosing a structure. Then define WHAT behavior is needed before deciding HOW to implement it, so a convenient technology does not narrow the solution prematurely.']),
    17: dict(notes=['Design a component’s external behavior as a black box first: define its services and interactions. Then refine its internals, keeping the solution simple and independent concerns separate.']),
    18: dict(notes=['Move between high-level responsibilities and lower-level interfaces or algorithms as needed. Design for plausible change, but avoid speculative flexibility that adds complexity without a requirement.']),
    19: dict(notes=['Use a quick high-level prototype to test risky assumptions before full implementation. Let stable abstractions guide detail implementations so low-level decisions do not dictate high-level policy.']),
    20: dict(notes=['Common closure groups classes that tend to change together; common reuse groups classes that clients need together. Dependencies should point toward more stable components so volatile parts can change with less ripple.']),
    21: dict(notes=['Depth-first design can perfect one feature while leaving requirements uncovered. Directly converting the requirements specification into a structure can over-constrain alternatives; missing likely changes or adding too much detail also makes a design brittle.']),
    22: dict(notes=['The recap combines ISP, DIP, behavior modeling, and general rules. Focus on keeping contracts focused, directing dependencies toward abstractions, and building from requirements and external behavior inward.']),
    23: dict(notes=['The design rules reinforce one another: define the problem and WHAT first, separate concerns, design externally visible behavior before internals, keep things simple, move across abstraction levels, prototype uncertainty, depend on abstractions, and group by change and reuse.']),
    24: dict(notes=['Analysis models describe the problem and required behavior; design models refine them into software components, interfaces, data, and interactions. Maintain traceability so design choices serve requirements and add implementation guidance.']),
}

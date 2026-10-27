"""SE322 annotated slides — Chapter 6, Lecture 1: design patterns, classification, and the Abstract Factory.
See ch01_introduction.py for AUTO_SLIDES and the ANN keys."""
from .common import mcq, past, scen, see, short, tf, tip, trap, trick

AUTO_SLIDES = 'all'
OVERVIEW = 'This chapter covers creational design patterns that organize object construction: Abstract Factory, Factory Method, Builder, Singleton, and Prototype. Compare the creation problem each pattern solves and how it reduces client dependence on concrete classes.'

DECK = {
    'key': 'ch6.1',
    'slug': '13-creational-design-patterns-lecture-1',
    'file': 'creational-design-patterns-lecture-1',
    'title': 'Creational Design Patterns: Classification and Abstract Factory',
    'chapter': 'Chapter 6 · Lecture 1',
    'page': 'ch06_1_page',  # notes, highlights and exam questions in the page schema
    'pdf': '/academics/software-engineering/se322/slides/chapter-6-creational-design-patterns-abstract-factory/',
    'lede': ('Design patterns vs. architectural patterns, the purpose and scope classification, how patterns are '
             'documented, the five creational patterns, and the Abstract Factory with the computer store example '
             '(CPU, monitor and keyboard families built by EnterpriseFactory and HomeFactory).'),
}

CREATIONAL = 'Creational patterns (5): Abstract Factory · Factory Method · Builder · Prototype · Singleton.'

ANN = {
    1: dict(kind='title', title='Creational Design Patterns', body=[], sub='SE322 · Chapter 6, Lecture 1', tips=[tip(CREATIONAL)]),
    2: dict(notes=['Patterns in detailed design → classification → documentation → creational patterns → Abstract Factory.']),
    3: dict(notes=['A design pattern captures a solution that worked repeatedly in a particular context. Architecture patterns organize major system parts; object-oriented patterns solve smaller collaboration or responsibility problems inside them.'],
            seen=[see('ch4.1', 11, 'Architectural vs. design patterns')]),
    4: dict(notes=['Purpose tells which design problem a pattern addresses; scope tells whether relationships are fixed among classes or assembled among runtime objects. Use both labels to compare patterns without confusing their roles.'],
            exam=[mcq('Design patterns that deal with how classes interact and assign responsibilities are:', ['Behavioral', 'Creational', 'Structural', 'Architectural'], 0, ''),
                  mcq('Patterns that compose existing objects into larger structures are:', ['Structural', 'Creational', 'Behavioral', 'Data flow'], 0, '')],
            weight=3),
    5: dict(notes=['Scope: CLASS patterns (relationships between classes, fixed at design/compile time) vs. OBJECT patterns (relationships between objects, at run time).'],
            exam=[mcq('A pattern whose relationships are set up between objects at run time has which scope?', ['Object', 'Class', 'Creational', 'Global'], 0, '')], weight=2),
    6: dict(notes=['Documentation template: intent, motivation, applicability, structure, participants, collaborations, consequences… (not required in this course).']),
    7: dict(notes=['Creational patterns move construction choices out of ordinary client code. Rather than scattering concrete `new` calls, the design centralizes how objects are selected, making substitutions easier.'], tips=[tip(CREATIONAL)],
            exam=[mcq('Which is NOT a creational pattern?', ['Composite', 'Builder', 'Singleton', 'Prototype'], 0, '')], weight=3),
    8: dict(notes=['Abstract Factory fits when products must vary together—for example, every widget in a theme should match. The client requests abstract products, while one selected factory supplies a compatible family.'],
            weight=3),
    9: dict(notes=['The family constraint prevents accidental mixes such as pairing products that do not work together. The client uses product interfaces, so switching families does not require rewriting assembly logic.'],
            exam=[mcq('The Abstract Factory pattern is used to create:', ['Families of related objects without specifying concrete classes', 'Exactly one instance of a class', 'A complex object step by step', 'Copies of a prototype'], 0, '')], weight=3),
    10: dict(notes=['The furniture analogy describes a family of related products: a modern set and a Victorian set each contain compatible items. Abstract Factory creates a matching family without the client naming each concrete product.']),
    11: dict(notes=['Start at Client and follow its call to AbstractFactory; then follow the returned abstract product to the family-specific implementation. This shows exactly where the pattern hides concrete class names.']),
    12: dict(notes=['The factory interface names the product operations, while each concrete factory supplies one matching family. Product interfaces give the client a common vocabulary; concrete classes provide the actual family-specific behavior.']), 13: dict(notes=['The key relationship is that every concrete factory returns implementations of the same product interfaces. That lets a client remain unchanged when the selected family changes.']), 14: dict(notes=['Check each product family as a set: the concrete factory must create mutually compatible products. If the client chooses each concrete product separately, it can accidentally mix families and lose the pattern’s guarantee.']),
    15: dict(notes=['Participants: AbstractFactory (create methods), ConcreteFactory (creates one family), AbstractProduct, ConcreteProduct, Client (uses only the abstract types).'],
             tips=[trick('Factories make families; the client only ever sees the abstract types.')], weight=3),
    16: dict(notes=['Define product contracts first, then one factory implementation per family and give the client the selected factory. Swapping that one object changes the family while preserving the client’s code.']),
    17: dict(notes=['Check the structure by tracing factory calls to the corresponding abstract product types. A concrete factory must create products that belong to the same family.']),
    18: dict(notes=['Treat Enterprise and Home as alternative configurations of the same computer-building process. Each configuration supplies a CPU, monitor, and keyboard; choosing a family should be one decision, not three unrelated selections.']),
    19: dict(notes=['Trace the request from the selected factory to the product returned for each operation. The client should use the product interface so switching from Home to Enterprise does not change how it assembles a computer.']), 20: dict(notes=['The example’s classes separate “what a CPU is” from “which CPU this family creates.” That indirection allows new CPU implementations without teaching the client every product class.']), 21: dict(notes=['Read the complete diagram by following dependencies outward: client → factory abstraction → concrete family factory → product abstractions → concrete products. Concrete names should be confined to the factory side.']),
    22: dict(notes=['The CPU hierarchy defines a common CPU contract and concrete enterprise/home implementations. Client code can use the interface while the selected factory determines which CPU is created.']),
    23: dict(notes=['The monitor interface represents the capability all monitors share; EnterpriseMonitor and HomeMonitor implement it differently. The same client operation works with either because both honor that contract.']), 24: dict(notes=['The keyboard hierarchy follows the same pattern as CPU and monitor. Repeating product abstractions is deliberate: each product type can vary independently in implementation while the factory keeps the family combination consistent.']),
    25: dict(notes=['Separate interface from implementation in the code: the CPU contract tells the client what it can ask for, and each concrete class decides how it behaves. The factory controls which implementation is returned.']), 26: dict(notes=['Read the sibling product classes as parallel implementations of one product contract: each concrete monitor or keyboard supports the operations the client needs, but supplies family-specific behavior. The concrete factory chooses the matching implementation; callers should keep using the abstract product type.']),
    27: dict(notes=['The factory interface is a menu of construction operations, not the concrete construction itself. Every concrete family factory implements that menu and returns the appropriate variant for each product type.']),
    28: dict(notes=['To switch the full system configuration, supply a different concrete factory. The client’s object-assembly logic stays the same, while the factory ensures all products match.']),
    29: dict(notes=['The client computer receives the factory as a dependency and asks it for parts. This is the critical decoupling point: the client orchestrates assembly without selecting product classes.']),
    30: dict(notes=['Trace a full run from factory selection through creation and use of each product. If any client class still names HomeCPU or EnterpriseMonitor directly, concrete knowledge has leaked past the factory boundary.']),
    31: dict(notes=['The example works because every creation request goes through one family factory and each returned part implements an abstract product type. This makes family switching local and compatibility easier to preserve.']),
    32: dict(notes=['Build the pattern from abstractions outward: define each product contract, define the family factory, implement one concrete factory per family, then inject a factory into client code. The client should never branch on family names.']),
    33: dict(notes=['Abstract Factory makes it easy to add a new family, but adding a new product category requires changing every factory. It fits when families vary more often than the kinds of products in each family.'],
             exam=[mcq('A drawback of the Abstract Factory is that:', ['Adding a new kind of product requires changing all factories', 'Families can be mixed freely', 'Clients must know concrete classes', 'Only one object can exist'], 0, '')], weight=3),
    34: dict(notes=['Use the repeated summary to retrieve the pattern’s intent and participants. The central distinction is creating a compatible family of products rather than one product at a time.']), 35: dict(notes=['Pros and cons repeated.']),
    36: dict(notes=['For a new example, identify which products form a family and which alternatives must stay compatible. If products do not need to vary together, a simpler Factory Method or direct construction may be clearer.']), 37: dict(notes=['Use the diagram to verify that the client depends only on factory and product interfaces. Concrete classes should appear behind the concrete factory implementations, where changing families is contained.']),
    38: dict(notes=['The pattern does not eliminate concrete classes; it isolates them at the construction boundary. Factories instantiate concrete products, while the rest of the application speaks through interfaces.']),
    39: dict(notes=['Review the pattern by naming its intent, participants, and trade-off: family consistency and reduced coupling in exchange for extra interfaces and factory classes.'], seen=[see('ch6.2', 3, 'Factory Method')]),
}

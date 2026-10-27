"""SE322 annotated slides — Chapter 6, Lecture 3: Builder, Singleton (and Prototype extra).
See ch01_introduction.py for AUTO_SLIDES and the ANN keys."""
from .common import mcq, past, scen, see, short, tf, tip, trap, trick

AUTO_SLIDES = 'all'
OVERVIEW = 'This chapter covers creational design patterns that organize object construction: Abstract Factory, Factory Method, Builder, Singleton, and Prototype. Compare the creation problem each pattern solves and how it reduces client dependence on concrete classes.'

DECK = {
    'key': 'ch6.3',
    'slug': '15-creational-design-patterns-lecture-3',
    'file': 'creational-design-patterns-lecture-3',
    'title': 'Creational Design Patterns: Builder and Singleton',
    'chapter': 'Chapter 6 · Lecture 3',
    'page': 'ch06_3_page',  # notes, highlights and exam questions in the page schema
    'pdf': '/academics/software-engineering/se322/slides/chapter-6-creational-design-patterns-iii/',
    'lede': ('Abstract Factory and Factory Method revisited, then the Builder (construct a complex object step by '
             'step, with a director) and the Singleton (one instance, global access, with Java code), plus an '
             'extra Prototype example. Final 252 Q6 asked for a Builder class diagram (sandwich ordering) and the '
             'Singleton diagram converted to code.'),
}

SINGLETON = 'Singleton recipe: private static instance field · private constructor · public static getInstance() that creates the instance on first call and returns it.'

ANN = {
    1: dict(kind='title', title='Creational Design Patterns', body=[], sub='SE322 · Chapter 6, Lecture 3', tips=[tip(SINGLETON)]),
    2: dict(notes=['The lecture revisits Abstract Factory and Factory Method, then introduces Builder and Singleton. Compare each pattern by what creation problem it solves and who controls the construction.']),
    3: dict(notes=['Abstract Factory groups related products into families and creates a compatible set. The client selects a family factory and uses product interfaces.'], seen=[see('ch6.1', 8, 'Abstract Factory')]),
    4: dict(notes=['Trace the diagram from the abstract factory to its concrete family factories and product interfaces. Verify that each concrete factory creates matching products.']),
    5: dict(notes=['Factory Method puts the product-creation decision in a creator method that subclasses can override. The creator’s shared workflow uses the product abstraction.'], seen=[see('ch6.2', 3, 'Factory Method')]), 6: dict(notes=['Factory Method revised, diagram.']),
    7: dict(notes=['Builder helps when an object needs several construction steps or optional parts. It separates the order of those steps from the representation, avoiding a constructor full of flags and allowing different valid outputs.'],
            past=[past('f252', 'Q6 · sandwich ordering = Builder')],
            exam=[mcq('A Sandwich can’t be created until bread and meat are set, and its construction must be separate from the Sandwich class. Which pattern? (Final 252)', ['Builder', 'Singleton', 'Prototype', 'Adapter'], 0, '')],
            weight=3),
    8: dict(notes=['Follow the construction flow: Client selects a concrete Builder and gives it to Director; Director calls the required build steps in order; Builder stores each part in Product; Client retrieves the finished product. Different builders can follow the same sequence but assemble different representations without product-specific code in Director.']),
    9: dict(notes=['Builder separates HOW a product is assembled from WHAT the product is. A director can sequence construction steps, while different builders produce different representations.']),
    10: dict(notes=['In the diagram, identify the Director, Builder interface, concrete builders, and product. Trace how the director invokes steps and how the builder returns the completed representation.']),
    11: dict(notes=['The director controls step order, a concrete builder decides what each step creates, and the product is the finished object. If construction is simple or step order varies completely, a builder may add unnecessary structure.'],
             tips=[trick('Director knows the ORDER; Builder knows the PARTS.')],
             exam=[mcq('In the Builder pattern, which participant calls the construction steps in the right order?', ['Director', 'ConcreteBuilder', 'Product', 'Client'], 0, '')], weight=3),
    12: dict(notes=['Build the code in four steps: define Product and its required state; declare Builder operations for each construction step; implement ConcreteBuilder methods so each step sets the corresponding product field; write Director to call those steps in a valid order. Client supplies a builder, asks Director to construct, then requests Product. Replace or reset the builder before each run so old state does not leak into the next object.']),
    13: dict(notes=['Read the builder steps as a sequence of calls that the director controls. Different builders can respond to the same calls with different ingredients or representations while preserving the agreed order.']), 14: dict(notes=['In the code, locate the product’s partially built state, the builder operations that fill it, and the final build/getResult step. Keeping construction there avoids a long constructor and gives one place to validate a complete object.']),
    15: dict(notes=['Stepwise construction makes validation and optional parts manageable; separate builders can create different representations. It also keeps construction logic out of the product’s business behavior.'], weight=2),
    16: dict(notes=['The extra explanation reinforces Builder’s value when construction is multi-step or has optional parts. For a simple object, a builder may add needless indirection.']),
    17: dict(notes=['Question: burgers (beef, chicken, veggie) with the same preparation steps → Builder.'],
             exam=[scen('Design the class diagram for the Final 252 sandwich ordering system with the Builder pattern.', 'Product: Sandwich (bread, meat, cheese, sauce). Builder interface SandwichBuilder: setBread(), setMeat(), addCheese(), addSauce(), getSandwich(). Concrete builders: ChickenSandwichBuilder, BeefSandwichBuilder. Director: SandwichMaker.make(builder) calls setBread() and setMeat() first, then the optional steps, and returns builder.getSandwich().')],
             weight=3),
    18: dict(notes=['The Builder interface describes construction steps; a concrete builder stores the intermediate product and implements those steps. It is the concrete builder—not the director—that decides the representation.']), 19: dict(notes=['Builder answer diagram.']), 20: dict(notes=['Builder answer, continued.']),
    21: dict(notes=['Review Builder by asking whether construction is complex enough to separate, whether the sequence should be reused, and which parts vary between representations.']), 22: dict(notes=['The example is useful when a product has several optional parts or configurations. A builder lets callers name the choices clearly and lets the builder reject incomplete combinations before returning the object.']), 23: dict(notes=['Follow the director’s ordered calls and compare what each concrete builder adds at each step. Same sequence with different results is the pattern’s central promise.']),
    24: dict(notes=['The code turns each construction step into an operation and returns a completed product only after the required steps. This separates a valid object’s construction rules from the code that uses it.']), 25: dict(notes=['Builder recap.']),
    26: dict(notes=['Singleton controls access to one shared instance; it is not merely a class with static methods. Use it only when one shared identity is needed, since global state can hide dependencies and make tests harder.'],
             exam=[mcq('Which pattern guarantees exactly one instance with global access?', ['Singleton', 'Prototype', 'Factory Method', 'Facade'], 0, '')], weight=3),
    27: dict(notes=['The private constructor blocks ordinary callers from creating extra instances, the static field stores the shared object, and getInstance() controls access. In multithreaded code, initialization must also be thread-safe.'], tips=[tip(SINGLETON)],
             past=[past('f252', 'Q6 · Singleton diagram and code')], weight=3),
    28: dict(notes=['A logger or configuration manager is often presented as a Singleton because callers need a shared access point. Consider whether one shared instance is truly required; global access can make tests and dependencies harder to manage.']),
    29: dict(notes=['The Singleton recipe works line by line: a private static field stores the instance; a private constructor blocks callers from using new; public static getInstance() checks whether the field is empty, creates the object once, then returns the stored reference on every call. Concurrent first calls need synchronization or another thread-safe initialization strategy.']),
    30: dict(notes=['The diagram should show one controlled access path to the shared instance. If clients can call the constructor directly, the class cannot guarantee there is only one instance.']), 31: dict(notes=['A Singleton’s state belongs to its shared instance, so all callers observe the same configuration or log. That shared identity is useful in narrow cases but can make tests order-dependent if state is not reset.']),
    32: dict(notes=['Lazy initialization creates the instance only when first requested, avoiding startup work if it is never needed. Ensure two threads cannot both create separate instances during the first call.'],
             exam=[short('Draw the Singleton class and write its code. (Final 252)', 'class Logger { private static Logger instance; private Logger() {} public static Logger getInstance() { if (instance == null) instance = new Logger(); return instance; } }  In UML: Logger with -instance: Logger {static}, -Logger(), +getInstance(): Logger {static}.')],
             weight=3),
    33: dict(notes=['Follow Logger.getInstance(): the first call initializes the static instance; later calls skip creation and return the same reference. Logging calls on that reference reach shared logger state. This works only if every construction path is blocked and initialization is thread-safe when calls can be concurrent.']),
    34: dict(notes=['Benefits: controlled access to the sole instance, saves resources, lazy initialization.'],
             exam=[tf('A Singleton’s constructor should be public so the instance can be created when needed.', False, 'It is private; access goes through getInstance().')], weight=2),
    35: dict(notes=['A banking application may use one logger for consistent audit records. The example illustrates shared access, while also prompting a check that the logger’s lifecycle and concurrency are controlled.']), 36: dict(notes=['Banking example: transaction system.']),
    37: dict(notes=['Review Singleton’s intent, construction controls, and trade-offs. A single instance can coordinate shared resources, but global mutable state can complicate testing and parallel execution.']),
    38: dict(notes=['The Prototype flow starts with a configured Circle or Square. Client asks the prototype to clone itself instead of naming and rebuilding its concrete class; the clone copies the shape’s fields and is returned through the shared Shape type. Check shallow versus deep copying: nested mutable objects can otherwise remain shared with the original.'],
             exam=[mcq('Creating new objects by cloning an existing instance is the:', ['Prototype pattern', 'Builder pattern', 'Singleton pattern', 'Composite pattern'], 0, '')], weight=2),
    39: dict(notes=['Prototype uses an existing instance as a template. The client asks for a copy without depending on the concrete class constructor, which is useful when setup is expensive or the object has a configuration worth preserving.']), 40: dict(notes=['The clone operation should copy the state needed by the new object. Check nested references: a shallow copy may cause edits to the clone to unexpectedly change the original.']), 41: dict(notes=['A prototype registry can hold named examples and return clones on request. The registry centralizes which prototypes are available, while callers get independent working copies.']), 42: dict(notes=['Compare the printed values before and after cloning to check which state was copied. Mutating one result should not affect the other unless sharing that state is intentional.']),
    43: dict(notes=['Choose by the construction problem: Abstract Factory creates a compatible family, Factory Method delegates one product choice, Builder assembles a complex object, Singleton controls shared identity, and Prototype copies an existing configuration.']),
}

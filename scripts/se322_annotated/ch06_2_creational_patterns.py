"""SE322 annotated slides — Chapter 6, Lecture 2: the Factory Method.
See ch01_introduction.py for AUTO_SLIDES and the ANN keys."""
from .common import mcq, past, scen, see, short, tf, tip, trap, trick

AUTO_SLIDES = 'all'
OVERVIEW = 'This chapter covers creational design patterns that organize object construction: Abstract Factory, Factory Method, Builder, Singleton, and Prototype. Compare the creation problem each pattern solves and how it reduces client dependence on concrete classes.'

DECK = {
    'key': 'ch6.2',
    'slug': '14-creational-design-patterns-lecture-2',
    'file': 'creational-design-patterns-lecture-2',
    'title': 'Creational Design Patterns: Factory Method',
    'chapter': 'Chapter 6 · Lecture 2',
    'page': 'ch06_2_page',  # notes, highlights and exam questions in the page schema
    'pdf': '/academics/software-engineering/se322/slides/chapter-6-creational-design-patterns-ii/',
    'lede': ('The Factory Method: a creator class defers the choice of concrete product to its subclasses. Its '
             'structure, worked example, design steps and benefits, plus extra exercises (document readers and '
             'parsers, notification senders and channels).'),
}

ANN = {
    1: dict(kind='title', title='Creational Design Patterns', body=[], sub='SE322 · Chapter 6, Lecture 2: Factory Method'),
    2: dict(notes=['Factory Method delegates product selection to creator subclasses. This lecture studies its structure, a worked example, implementation steps, benefits, and how it differs from Abstract Factory.']),
    3: dict(notes=['Walk the pattern in call order: Product declares the operation; ConcreteProduct implements it. Creator defines factoryMethod() returning Product and keeps the larger workflow in a normal method. ConcreteCreator overrides factoryMethod(), constructs the chosen ConcreteProduct, and returns it through Product. Client uses Creator and Product, so it has no concrete new call or product-specific branch.'],
            tips=[trick('Factory Method = ONE product, chosen by a subclass. Abstract Factory = a FAMILY of products, chosen by a factory object.')],
            exam=[mcq('Which pattern lets subclasses decide which concrete class to instantiate through an overridable creation method?', ['Factory Method', 'Abstract Factory', 'Singleton', 'Builder'], 0, '')],
            weight=3),
    4: dict(notes=['The creator calls its factory method inside a larger workflow; concrete creators override that method to select a product. Trace who calls the method and who constructs the product to keep the roles distinct.']),
    5: dict(notes=['Trace the code from the client’s creator call to factoryMethod(), then follow the returned Product reference into its operation. The concrete creator decides which class to instantiate; the base creator’s workflow continues using only Product. A new product needs a product implementation and creator override, not edits throughout the workflow.']),
    6: dict(notes=['Locate the creator’s factory method and note its Product return type. The concrete creator overrides it and returns the selected product. The client invokes the creator’s regular operation; that operation calls the factory hook and uses the returned product interface, keeping product selection separate from product use.']), 7: dict(notes=['Steps of the Factory Method, illustrated.']),
    8: dict(notes=['Trace the creation call: the creator’s workflow invokes factoryMethod(), and the concrete creator returns a concrete product through the Product type. This lets the workflow use the product without knowing its class.']), 9: dict(notes=['When reading the code, distinguish the factory method from ordinary creator operations. The method that varies belongs in the subclass; the stable workflow belongs in the base creator and consumes only Product.']), 10: dict(notes=['A new product variant should require a matching creator override, not a new conditional inside every client. If selection logic is still scattered through callers, the Factory Method boundary is incomplete.']), 11: dict(notes=['The output confirms which concrete product the selected creator supplied. Use it to connect the runtime result back to the override that made the decision.']),
    12: dict(notes=['Steps: product interface → concrete products → abstract creator with an abstract factory method → concrete creators override it → client uses the creator.']),
    13: dict(notes=['The step diagrams show how to move from a direct `new ConcreteProduct` dependency toward a product abstraction and an overridable creation method.']),
    14: dict(notes=['Factory Method supports extension when each new product can be paired with a creator subtype, keeping existing workflow code stable. If creator variants have no real meaning, the extra subclasses add needless indirection.'],
             exam=[tf('The Factory Method helps follow the Open-Closed Principle when new product types are added.', True, '')], weight=2),
    15: dict(notes=['Review the intent and trade-off: subclasses control which product is created, which supports extension but can add creator subclasses.']),
    16: dict(notes=['Abstract Factory selects a compatible family through a factory object; Factory Method delegates one product choice to an overridable method. A Factory Method can also implement one operation inside an Abstract Factory.']), 17: dict(notes=['Extra example.']),
    18: dict(notes=['DocumentReader is the creator abstraction and Parser is the product abstraction. PdfReader can supply PdfParser while the read workflow stays independent of PDF-specific parsing classes.'],
             exam=[scen('A DocumentReader must create the right Parser for PDF, Word or HTML files. Apply the Factory Method.', 'Make Parser an interface with parse(). DocumentReader is abstract with an abstract createParser() and a read() method that calls createParser().parse(). PdfReader, WordReader and HtmlReader extend DocumentReader and return PdfParser, WordParser or HtmlParser. New formats need only a new reader and parser.')],
             weight=2),
    19: dict(notes=['Follow the inheritance and realization arrows separately: concrete readers specialize the creator, while parsers implement the product interface. The factory method links those two hierarchies.']), 20: dict(notes=['The exercise is a pattern fit if different document formats share one reading workflow but need different parsers. Put format-specific creation in reader subclasses and keep common processing in the creator.']), 21: dict(notes=['Check that the caller asks a reader to perform the workflow instead of constructing PdfParser directly. That dependency direction is what makes adding another format less invasive.']),
    22: dict(notes=['Email, SMS, and push are alternative products behind one channel contract. The design should let a notification workflow send through any channel without implementing delivery details itself.']),
    23: dict(notes=['Answer: Channel interface; abstract NotificationSender with createChannel(); EmailSender, SmsSender… override it.']),
    24: dict(notes=['Check the answer diagram by following NotificationSender to its creation method and then to the Channel interface. Concrete senders select concrete channels while shared logic uses the abstraction.']),
}

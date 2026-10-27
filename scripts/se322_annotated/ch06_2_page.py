"""SE322 Chapter 6, Lecture 2 (Factory Method): page content for the annotated deck.

Schema: see annotated_page.py. Most code and UML here are pictures, so their marks use 'ocr' (skipped if OCR
can't read them) and the notes walk through the code. Factory Method has not appeared on a past paper yet, so all
questions are predictions.
"""
from .common import likely

TITLE = 'The Factory Method Pattern'
CHAPTER = 'SE322 · Chapter 6 · Lecture 2'

OVERVIEW = {
    'summary': ('Factory Method is a class-creational pattern: an abstract creator declares one factory method that '
                'returns a product interface, and each concrete creator subclass overrides it to decide which concrete '
                'product to instantiate. The creator’s other methods use the product only through its interface. The '
                'lecture works through a computer store (StandardComputerStore makes StandardComputer, '
                'AdvancedComputerStore makes AdvancedComputer) in C++ and Java, lists the design steps and benefits, '
                'contrasts it with Abstract Factory, and practises it on document readers and notification senders.'),
    'ideas': [
        ('Intent', 'Define an interface for creating an object, but let subclasses decide which class to instantiate; defer instantiation to subclasses.'),
        ('Four roles', 'Creator (abstract, declares the factory method), ConcreteCreator (overrides it), Product (interface), ConcreteProduct.'),
        ('One product vs. a family', 'Factory Method creates one product through one overridable method; Abstract Factory creates a family through a factory object with several methods.'),
        ('Benefits', 'Code is separated from product-specific classes, so new products need only a new creator subclass (OCP); easier reuse, maintenance and testing.'),
    ],
    'sections': [
        ('Slides 1–4', 'Factory Method: intent and structure'),
        ('Slides 5–13', 'Computer-store example: diagram, C++ and Java code'),
        ('Slides 14–15', 'Design steps, benefits, summary'),
        ('Slides 16–21', 'Exercise: document readers and parsers; Factory Method vs. Abstract Factory'),
        ('Slides 22–24', 'Exercise: notification senders and channels'),
    ],
    'exam': ('Not yet on a past paper, but it fits the Final’s “which pattern? draw the class diagram” format (Final 252 Q6 '
             'did this for Builder and Singleton). Know the four roles, the code shape (abstract createX() overridden in '
             'subclasses) and the difference from Abstract Factory.'),
}

TITLES = {5: 'Extra: Question – the computer store', 6: 'Factory Method Example: class diagram', 7: 'Extra: Steps of Factory Method',
          11: 'Factory Method Example: creator and product classes', 13: 'Extra: The computer store in Java', 16: 'Extra: Question – Document Reader',
          17: 'Extra: Document Reader class diagram', 18: 'Document Reader class diagram', 19: 'Extra: General order for writing classes',
          20: 'Extra: Document Reader code', 21: 'Extra: Factory Method vs. Abstract Factory', 22: 'Extra: Question – Notification Sender',
          23: 'Notification Sender class diagram', 24: 'Extra: Notification Sender code'}

SLIDES = {
    1: dict(
        hl=[('[Creational Design Patterns]', 1)],
        notes=['Second creational-patterns lecture: **Factory Method**, the single-product cousin of Abstract Factory.']),
    2: dict(
        hl=[('Factory Method Design Pattern', 1), ('Steps of Designing Factory Method Pattern', 2), ('Benefits of Factory Method', 3)],
        notes=['The pattern and the computer-store example.',
               'The design steps.',
               'The benefits.']),
    3: dict(
        hl=[('class creational pattern', 1), ('defer object instantiation', 1), ('let subclasses decide', 2), ('One product at a time', 3), ('Creator (abstract class or interface)', 4)],
        notes=['Factory Method is a **class** creational pattern (it works through inheritance, so its relationships are fixed at design time) that encapsulates object creation and **defers instantiation to derived classes**.',
               '**Intent**: define an interface for creating an object, but **let subclasses decide** which class to instantiate.',
               'It creates **one product at a time** through **one** method. Key idea: “defer instantiation to subclasses”.',
               '**Structure**: (1) **Creator**, an abstract class or interface that declares the factory method; (2) **ConcreteCreator**, which overrides it; (3) **Product**, the interface every product implements; (4) **ConcreteProduct**.'],
        exam=[likely('Which pattern lets subclasses decide which concrete class to instantiate through one overridable creation method?', a=0,
                     opts=['Factory Method', 'Abstract Factory', 'Singleton', 'Builder']),
              likely('State the intent of the Factory Method and name its four participants.',
                     a='Define an interface for creating an object, but let subclasses decide which class to instantiate (defer instantiation to subclasses). Participants: Creator (declares the factory method), ConcreteCreator (overrides it), Product (interface), ConcreteProduct.')]),
    4: dict(
        hl=[('only one creational', 1), ('concrete product and concrete creator', 2), ('one product type with multiple', 3), ('Creator', 4, 0, 'ocr')],
        notes=['Like Abstract Factory it has creator and product classes, but the creator needs **only one** creational method, for products that share the same interface.',
               'So for each product in the system there is one **concrete product** and one **concrete creator** class.',
               'Rule of thumb: Factory Method for **one product type with several implementations**; Abstract Factory for **several product types**, each with several implementations.',
               {'text': 'Reading the generic diagram:', 'items': [
                   ('Creator', '*createProduct()* in italics: abstract, the factory method. *someOperator()* is a normal method that calls createProduct() and uses the result.'),
                   ('ConcreteCreator', 'Inherits from Creator (solid line, hollow triangle) and implements createProduct().'),
                   ('«interface» Product / ConcreteProduct', 'ConcreteProduct realises Product (dashed line). The arrow from ConcreteCreator to ConcreteProduct shows which product it creates.')]}]),
    5: dict(
        hl=[('Standard Computers', 1), ('only build its own type of computer', 2), ('common interface', 3), ('easy to add more computer categories', 4), ('Identify the Design Pattern', 5)],
        notes=['The scenario: an electronics store sells **standard** (affordable) and **advanced** (gaming) computers.',
               'Each store type builds **only its own** kind: the Standard Store builds standard computers, the Advanced Store advanced ones.',
               'Customers get a **common interface**: ask a store for a computer and display its details (monitor, CPU, keyboard, cost).',
               'New categories (Workstation Store, Budget Store) must be addable **without changing existing code**.',
               'Tasks: identify the pattern (Factory Method: one product type, a creator subclass per variant), write the code, draw the class diagram.']),
    6: dict(
        hl=[('ComputerStore (Abstract Class)', 1), ('Derived Classes', 2), ('Computer Interface', 3), ('StandardComputer and AdvancedComputer', 4), ('Summary:', 5)],
        notes=['**ComputerStore** (abstract creator): declares the abstract factory method `createComputer(type)`, returning a `Computer`, and `displayComputer(type)`, which displays the computer that createComputer produces.',
               '**StandardComputerStore** and **AdvancedComputerStore** (concrete creators) each implement `createComputer()` to return their own kind of Computer.',
               '**Computer** (product interface): `displayMonitorInfo()`, `displayCpuInfo()`, `displayKeyboardInfo()`, `displayCost()`. Note the italics in the diagram: abstract operations.',
               '**StandardComputer** and **AdvancedComputer** (concrete products) implement those display methods.',
               'Summary: different Computers are created without changing client code; the creation logic lives in ComputerStore and its subclasses.']),
    7: dict(
        hl=[('Computer', 1, 0, 'ocr'), ('ComputerStore', 2, 0, 'ocr')],
        notes=['The writing order: (1) the `Computer` interface; (2) the concrete computers `StandardComputer`, `AdvancedComputer`; (3) the abstract `ComputerStore` with `createComputer()` and `displayComputer()`; (4) the concrete stores; (5) `main` to test. Products first, then creators, then the client: the same order you should use in an exam answer.']),
    8: dict(
        hl=[('virtual', 1, 0, 'ocr'), ('Notes Extra', 2, 0, 'ocr')],
        notes=[{'text': 'The C++ creator class:', 'code': [
                    ('class Computer;', 'Forward declaration: ComputerStore only needs to know the type exists.'),
                    ('class ComputerStore {', 'The creator. It is abstract, so specific derived stores are needed.'),
                    ('    virtual Computer* createComputer(std::string type);', 'The factory method: `virtual` lets derived classes override it (made pure virtual with `= 0` in a strictly abstract creator).'),
                    ('    void displayComputer(std::string type); };', 'A normal method that will use the created computer.')]},
               'How to spot abstract methods: in code, look for the `virtual` keyword (C++) or `abstract` (Java); in UML diagrams, methods in *italics*.']),
    9: dict(
        hl=[('createComputer(type)', 1, 0, 'ocr'), ('displayMonitorInfo', 2, 0, 'ocr')],
        notes=[{'text': '`displayComputer` in C++:', 'code': [
                    ('void ComputerStore::displayComputer(string type) {', 'Defined once, in the abstract creator.'),
                    ('    Computer* computer = createComputer(type);', 'Delegates creation to the derived class through the factory method: this line is the whole pattern.'),
                    ('    computer->displayMonitorInfo(); computer->displayCpuInfo();', 'Uses the product only through the Computer interface.'),
                    ('    computer->displayKeyboardInfo(); computer->displayCost(); }', 'The output differs by store, but this code never changes.')]}]),
    10: dict(
        hl=[('StandardComputerStore::createComputer', 1, 0, 'ocr'), ('NullComputer', 2, 0, 'ocr')],
        notes=[{'text': 'A concrete creator in C++:', 'code': [
                    ('Computer* StandardComputerStore::createComputer(string type) {', 'The standard store’s override of the factory method.'),
                    ('    if (type.compare("standard") == 0) computer = new StandardComputer;', 'It can only build standard computers.'),
                    ('    else computer = new NullComputer;', 'Anything else returns a NullComputer: an object that does nothing, so callers never get a null pointer.'),
                    ('    return computer; }', 'Clients are responsible for freeing the returned object (C++).')]}]),
    11: dict(
        hl=[('Creator', 1, 0, 'ocr'), ('Products need to obey', 2, 0, 'ocr')],
        notes=['The complete example diagram. **Creator classes**: abstract ComputerStore (*createComputer(type): Computer*, displayComputer(type)) with subclasses StandardComputerStore and AdvancedComputerStore.',
               '**Product classes**: «interface» Computer, realised by StandardComputer and AdvancedComputer; the arrows from each store to its computer show which product each creator makes. Products must obey the product interface.']),
    12: dict(
        hl=[('Identify and design the product interface', 1), ('concrete products', 2), ('Design the factory interface', 3), ('concrete factories', 4), ('Associate each factory', 5)],
        notes=['**Step 1**: identify and design the product interface (Computer).',
               '**Step 2**: design the concrete products that realise it (StandardComputer, AdvancedComputer).',
               '**Step 3**: design the factory (creator) interface, ComputerStore, with **one abstract factory method** that delegates creation to derived classes.',
               '**Step 4**: design one concrete factory (creator) per product from step 2.',
               '**Step 5**: associate each factory with its product.'],
        exam=[likely('Apply the Factory Method to a logistics app where RoadLogistics creates Trucks and SeaLogistics creates Ships. Name the classes and the factory method.',
                     a='Product interface: Transport (deliver()). Concrete products: Truck, Ship. Abstract creator: Logistics with abstract createTransport(): Transport and planDelivery() that calls createTransport().deliver(). Concrete creators: RoadLogistics returns new Truck(); SeaLogistics returns new Ship().')]),
    13: dict(
        hl=[('abstract class ComputerStore', 1, 0, 'ocr'), ('StandardComputerStore extends', 2, 0, 'ocr'), ('interface Computer', 3, 0, 'ocr'), ('main', 4, 0, 'ocr')],
        notes=[{'text': 'The same example in Java:', 'code': [
                    ('abstract class ComputerStore { public abstract Computer createComputer(String type);', 'The factory method, implemented by subclasses.'),
                    ('    public String displayComputer(String type) { Computer c = createComputer(type); … }', 'A helper that formats the product info, using only Computer.'),
                    ('class StandardComputerStore extends ComputerStore { @Override public Computer createComputer(String type) {', 'The standard creator…'),
                    ('    if ("standard".equalsIgnoreCase(type)) return new StandardComputer();', '…builds a StandardComputer…'),
                    ('    return new NullComputer("Standard store only builds \'standard\' computers"); } }', '…or a NullComputer with a message.'),
                    ('class AdvancedComputerStore extends ComputerStore { … new AdvancedComputer() … }', 'The advanced creator, same shape.')]},
               {'text': 'Products and client:', 'code': [
                    ('interface Computer { String displayMonitorInfo(); String displayCpuInfo(); String displayKeyboardInfo(); String displayCost(); }', 'The product interface.'),
                    ('class StandardComputer implements Computer { … "Monitor: 24\\" 1080p" … "Cost: $699" }', 'Concrete products return their own details.'),
                    ('ComputerStore standardStore = new StandardComputerStore(); standardStore.displayComputer("standard");', 'The client works through ComputerStore.'),
                    ('advancedStore.displayComputer("standard");', 'The mismatch example: the advanced store asked for a standard computer returns the NullComputer message.')]}]),
    14: dict(
        hl=[('Separates code from product-specific classes', 1), ('efficient', 2), ('reuse', 3), ('maintain', 3), ('Testability', 4)],
        notes=['It **separates code from product-specific classes**, so the same code works with existing and newly created products. New product = new creator subclass, no edits elsewhere (OCP).',
               'Development is more **efficient**: different developers can work on different creators and products at the same time.',
               'Specific parts are easier to **reuse** and **maintain**.',
               '**Testability** improves: a test can subclass the creator to return a fake product.'],
        exam=[likely('True or false: the Factory Method helps follow the Open-Closed Principle when new product types are added.', tf=True,
                     why='A new product needs a new concrete product and a new creator subclass; existing creators and client code are not modified.')]),
    15: dict(
        hl=[('Factory Method', 1), ('Builder', 2), ('Singleton', 2)],
        notes=['This lecture: **Factory Method**.',
               'Next: **Builder** and **Singleton**, which complete the creational patterns (both were on Final 252).']),
    16: dict(
        hl=[('Document Reader', 1), ('single overridable method', 2), ('One common', 3), ('Each concrete reader subclass', 4), ('Which design pattern is most appropriate here?', 5)],
        notes=['Scenario: a document-reader framework handles PDF, Word and Excel files. An abstract **DocumentReader** base class implements the overall reading workflow.',
               'It declares a **single overridable method** whose job is to return the parser to use: that is the factory method.',
               '**One common Parser interface** is used by all concrete parsers (the product).',
               'Each concrete reader (PdfReader, WordReader, ExcelReader) overrides that method to return the right parser; a new type (PowerPoint, Text) means a new reader subclass, with no client changes.',
               'Answer: **Factory Method**. The next slides give the UML and code.'],
        exam=[likely('A DocumentReader framework must create the right Parser for PDF, Word or Excel files through one overridable method. Which pattern, and what are the classes?',
                     a='Factory Method. Parser is the product interface (parse()); PdfParser, WordParser, ExcelParser implement it. DocumentReader is the abstract creator with abstract createParser(): Parser and a read() workflow that calls createParser().parse(). PdfReader, WordReader and ExcelReader extend DocumentReader and return their parser.')]),
    17: dict(
        hl=[('DocumentReader', 1, 0, 'ocr'), ('Parser', 2, 0, 'ocr')],
        notes=['The solution diagram: «abstract» **DocumentReader** with `createParser(t): Parser`; PdfReader, ExcelReader and WordReader extend it (creator classes).',
               '«Interface» **Parser** with `Parse()`, realised by PdfParser, ExcelParser and WordParser (product classes). Each reader points to the parser it creates.']),
    18: dict(
        hl=[('DocumentReader', 1, 0, 'ocr'), ('Products need to obey', 2, 0, 'ocr')],
        notes=['The same diagram labelled with the pattern’s roles: **creator classes** on the left (DocumentReader and its readers), **product classes** on the right (Parser and its parsers). Products must obey the Parser interface; each concrete reader is paired with exactly one concrete parser.']),
    19: dict(
        hl=[('Product (Interface or Abstract Class)', 1, 0, 'ocr'), ('Concrete Products', 2, 0, 'ocr'), ('Creator (Abstract Class)', 3, 0, 'ocr'), ('Concrete Creators', 4, 0, 'ocr'), ('Client', 5, 0, 'ocr')],
        notes=['**1. Product**: the common behaviour (Parser with `parse()`).',
               '**2. Concrete products**: one per variant (PdfParser, WordParser, ExcelParser).',
               '**3. Creator**: the abstract class that declares the factory method (DocumentReader with `createParser()`).',
               '**4. Concrete creators**: implement the factory method to return the right product (PdfReader → PdfParser…).',
               '**5. Client**: `main` uses the **creator** type, never the concrete products directly.']),
    20: dict(
        hl=[('abstract class DocumentReader', 1, 0, 'ocr'), ('PdfReader extends', 2, 0, 'ocr'), ('interface Parser', 3, 0, 'ocr'), ('reader = new PdfReader', 4, 0, 'ocr')],
        notes=[{'text': 'The Java solution:', 'code': [
                    ('abstract class DocumentReader { public abstract Parser createParser(); // Factory Method }', '1) The creator.'),
                    ('class PdfReader extends DocumentReader { public Parser createParser() { return new PdfParser(); } }', '2) Concrete creators, one per format (WordReader, ExcelReader are the same).'),
                    ('interface Parser { void parse(); }', '3) The product.'),
                    ('class PdfParser implements Parser { public void parse() { System.out.println("Parsing PDF..."); } }', '4) Concrete products.'),
                    ('DocumentReader reader; reader = new PdfReader(); reader.createParser().parse();', '5) The client holds a DocumentReader; switching to `new WordReader()` changes the output to “Parsing Word...” without other changes.')]}]),
    21: dict(
        hl=[('Differences Between Factory Method and Abstract Factory', 1, 0, 'ocr'), ('Purpose', 2, 0, 'ocr'), ('Client dependency', 3, 0, 'ocr')],
        notes=['**Purpose**: Factory Method defines a single factory method to create **one product** at a time; Abstract Factory provides an interface for creating **families** of related products.',
               '**Factory and products**: one (often parameterised) method whose subclasses decide the product, with one product hierarchy (Parser → PdfParser, WordParser); versus a factory interface with one method per product type and several related hierarchies (Button, Checkbox for Windows and Mac).',
               '**Flexibility and client**: Factory Method is lighter, used when only one kind of product is needed, and the client calls a single method (`createParser()`); Abstract Factory is more complex but guarantees consistency across a family, and the client calls several methods (`createButton()`, `createCheckbox()`). Examples: DocumentReader creates one parser; GUIFactory creates a set of widgets.'],
        exam=[likely('Give two differences between the Factory Method and the Abstract Factory patterns.',
                     a='Factory Method creates one product through one overridable method in a creator subclass (inheritance, class scope); Abstract Factory creates a family of related products through a factory object with one method per product type (composition, object scope). Factory Method has one product hierarchy; Abstract Factory has several related hierarchies and guarantees the family is consistent.')]),
    22: dict(
        hl=[('Notification Sender framework', 1, 0, 'ocr'), ('one overridable method', 2, 0, 'ocr'), ('Questions:', 3, 0, 'ocr')],
        notes=['A second exercise: a notification-sender framework sends messages through Email, SMS or Push. The abstract base class **NotificationSender** implements the workflow (validate message → create channel → send).',
               'It declares **one overridable method** that returns the **Channel** to use; one common `Channel` interface; each sender subclass (EmailSender, SmsSender, PushSender) overrides that method; a new channel (WhatsApp) means a new sender and channel class, no client changes.',
               'Questions: which pattern (Factory Method), draw the UML, write simple Java. Solutions on slides 23–24.']),
    23: dict(
        hl=[('NotificationSender', 1, 0, 'ocr'), ('EmailChannel', 2, 0, 'ocr')],
        notes=['Creator classes: «abstract» **NotificationSender** with `createChannel(): Channel`; EmailSender, SMSSender and PushSender extend it.',
               'Product classes: «Interface» **Channel** with `send(String)`, realised by EmailChannel, SmsChannel and PushChannel. Each sender creates its matching channel.']),
    24: dict(
        hl=[('Product Interface', 1, 0, 'ocr'), ('Abstract Creator', 2, 0, 'ocr'), ('Concrete Creators', 3, 0, 'ocr')],
        notes=[{'text': 'The Java solution:', 'code': [
                    ('interface Channel { void send(String msg); }', 'The product.'),
                    ('class EmailChannel implements Channel { public void send(String msg) { System.out.println("Email: " + msg); } }', 'Concrete products (SmsChannel, PushChannel similar).'),
                    ('abstract class NotificationSender { public void notify(String msg) { Channel channel = createChannel(); channel.send(msg); }', 'The workflow, written once in the creator…'),
                    ('    protected abstract Channel createChannel(); }', '…and the factory method it relies on.'),
                    ('class EmailSender extends NotificationSender { protected Channel createChannel() { return new EmailChannel(); } }', 'Concrete creators decide the channel (SmsSender, PushSender similar).')]},
               '`notify()` is the “some operation” of the generic structure: it never names a concrete channel, which is exactly what makes adding WhatsApp a matter of two new classes.']),
}

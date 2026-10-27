"""SE322 Chapter 6, Lecture 3 (Builder and Singleton, plus a Prototype exercise): page content.

Schema: see annotated_page.py. Much of this deck is code and UML pictures, so marks there use 'ocr' (skipped if
OCR can't read them). Past-exam questions are copied from Final 252 Q6; everything else is a prediction.
"""
from .common import asked, likely

TITLE = 'Creational Patterns III: Builder and Singleton'
CHAPTER = 'SE322 · Chapter 6 · Lecture 3'

SANDWICH = ('Customized sandwiches must follow a correct, consistent assembly process; a Sandwich cannot be created until at '
            'least the bread and meat are set, and construction is separate from the Sandwich itself. Which pattern would you '
            'use? Draw its class diagram.')

OVERVIEW = {
    'summary': ('After revising Abstract Factory and Factory Method, the lecture adds two creational patterns. Builder '
                'separates the step-by-step construction of a complex object from its representation: a Director calls the '
                'same build steps in order, and each ConcreteBuilder implements them differently (C++ vs. Java code, beef vs. '
                'chicken burger), returning the product at the end. Singleton ensures a class has only one instance with a '
                'global access point: private static instance, private constructor, public static getInstance(). A '
                'Prototype exercise (copying shapes with clone()) closes the creational patterns.'),
    'ideas': [
        ('Builder roles', 'Director (runs the steps in order), Builder interface (buildPartA/B/C, getResult), ConcreteBuilders (one per representation), Product.'),
        ('Builder vs. Abstract Factory', 'Builder builds one complex object step by step; Abstract Factory creates a family of related objects all at once.'),
        ('Singleton recipe', 'Private constructor, private static instance field, public static getInstance() that creates the instance once and returns it.'),
        ('Prototype', 'Objects copy themselves with clone() instead of being created with new.'),
    ],
    'sections': [
        ('Slides 2–6', 'Abstract Factory and Factory Method revised'),
        ('Slides 7–21', 'Builder: intent, steps, structure, code generator, benefits, burger exercise'),
        ('Slides 22–25', 'Builder: code-generator example in detail'),
        ('Slides 26–37', 'Singleton: intent, structure, event manager, Java code, steps, benefits, banking logger'),
        ('Slides 38–43', 'Prototype exercise and summary'),
    ],
    'exam': ('Final 252 Q6 (5 marks) came straight from this lecture: Q6-1 (3 marks) asked for the Builder pattern and its class '
             'diagram for a sandwich-ordering system, and Q6-2 (2 marks) for the standard Singleton class diagram and its code.'),
}

TITLES = {3: 'Abstract Factory Pattern – Revised', 4: 'Abstract Factory Pattern – Revised: computer store', 6: 'Factory Method Pattern – Revised: computer store',
          9: 'Extra: Builder pattern in one slide', 12: 'Extra: Builder Pattern – how to solve', 13: 'Extra: Builder code skeleton',
          14: 'Builder Design Pattern Example: class diagram', 16: 'Extra: Builder in simple words', 17: 'Question: burger builder',
          18: 'The Builder Pattern: structure (repeated)', 19: 'Burger builder: solution code', 20: 'Burger builder: client code',
          23: 'Builder Design Pattern Example: class diagram', 24: 'Builder Design Pattern Example: the builder interface',
          25: 'Builder Design Pattern Example: the C++ builder', 29: 'Extra: Why Singleton?', 30: 'Singleton Design Pattern Example: class diagrams',
          31: 'Java Code for the Singleton Pattern: the class', 35: 'Extra: Real-World Scenario – banking logger', 36: 'Extra: Transaction and notification systems',
          37: 'Singleton Design Pattern Example: C++ EventManager', 38: 'Extra: Example – copying shapes (Prototype)', 39: 'Prototype step 1: the common interface',
          40: 'Prototype step 2: Circle', 41: 'Prototype step 3: Square', 42: 'Prototype step 4: the client'}

SLIDES = {
    1: dict(
        hl=[('[Creational Design Patterns]', 1)],
        notes=['Last creational-patterns lecture: a revision of Abstract Factory and Factory Method, then **Builder** and **Singleton**. Both were on Final 252.']),
    2: dict(
        hl=[('Abstract Factory Pattern', 1), ('Builder', 2), ('Singleton', 3)],
        notes=['Revision of the two factory patterns.',
               '**Builder**, with a code-generator example.',
               '**Singleton**, with an event-manager example.']),
    3: dict(
        hl=[('Creator', 1, 0, 'ocr'), ('Product', 2, 0, 'ocr')],
        notes=['Abstract Factory revised: an AbstractFactory with one create method per product; ConcreteFactory1 and 2 each create one **family** (A1+B1, A2+B2). Creator classes on the left, product classes on the right; the client uses only the interfaces.']),
    4: dict(
        hl=[('Creator', 1, 0, 'ocr')],
        notes=['The same structure applied to the computer store: ComputerPartsFactory creates a Monitor, CPU and Keyboard; the Advanced and Standard factories each create their own matching set.']),
    5: dict(
        hl=[('Factories need to', 1, 0, 'ocr'), ('Products need to obey', 2, 0, 'ocr')],
        notes=['Factory Method revised: an abstract **Creator** with *createProduct()* and someOperation(); a **ConcreteCreator** overrides createProduct() to return a **ConcreteProduct**. One product, chosen by a subclass. Factories must obey the factory (creator) interface; products must obey the product interface.']),
    6: dict(
        hl=[('ComputerStore', 1, 0, 'ocr')],
        notes=['Factory Method applied: ComputerStore’s *createComputer(type)* is overridden by StandardComputerStore and AdvancedComputerStore, which return StandardComputer and AdvancedComputer through the Computer interface.']),
    7: dict(
        hl=[('Separate', 1), ('construction', 1), ('complex object', 1), ('representation', 2), ('different representations', 2)],
        notes=['The **Builder**’s intent: **separate the construction of a complex object from its representation**…',
               '…**so that the same construction process can create different representations**. The steps (the algorithm) stay fixed; what each step produces varies with the builder.'],
        exam=[asked('f252', 'Q6-1 · 3 marks', SANDWICH,
                    a='**Pattern: Builder.** It separates the construction of a complex object from its representation and builds it step by step. **SandwichBuilder** (interface): `setBread()`, `setMeat()`, `setCheese()`, `build()`. **CustomSandwichBuilder**: stores the parts; `build()` refuses to create the Sandwich unless bread and meat are set (consistency). **SandwichDirector**: runs the steps in the correct order. **Sandwich**: the product (bread, meat, cheese). Diagram: Director → (directs) SandwichBuilder; CustomSandwichBuilder ⇢ realizes SandwichBuilder and creates Sandwich.')]),
    8: dict(
        hl=[('product class', 1), ('creational process and algorithm', 2), ('design the builder interface', 3), ('different representations', 4)],
        notes=['**Step 1**: identify and design the **product** class (GeneratedProduct).',
               '**Step 2**: identify the product’s **creational process and algorithm**, and design a class that executes it (CodeGenerator, the director).',
               '**Step 3**: from steps 1–2, design the **builder interface**: abstract methods for every part that must be created for the whole product to exist; concrete builders implement them.',
               '**Step 4**: design one class per **representation** of the product (CppMessageBuilder, JavaMessageBuilder…).']),
    9: dict(
        hl=[('Intent:', 1), ('When useful:', 2), ('Key roles:', 3), ('Flow (always the same):', 4), ('Builder vs Abstract Factory', 5)],
        notes=['**Intent**: separate *how* a complex object is built (the steps) from *what* the result looks like (the representation).',
               '**When useful**: same construction steps, different outputs, e.g. generating Java vs. C# code, or a small vs. large burger.',
               '**Roles**: **Director** (orchestrates the steps in order, knows no details); **Builder** interface (declares the step methods `buildPartA/B/C…` and `getProduct()`); **ConcreteBuilders** (implement the steps for each representation); **Product** (the thing built).',
               '**Flow**: the client chooses a ConcreteBuilder and gives it to the Director → the Director runs the steps in sequence → the client asks the builder for the finished product.',
               '**Builder vs. Abstract Factory**: Builder builds **one complex object step by step**; Abstract Factory creates **a family of related objects all at once**.'],
        exam=[likely('Contrast the Builder and Abstract Factory patterns.',
                     a='Builder constructs one complex object step by step under a director’s control, returning it at the end; different builders give different representations of the same object. Abstract Factory creates a family of related objects, each in a single call, ensuring the family is consistent.')]),
    10: dict(
        hl=[('Code Generator', 1, 0, 'ocr'), ('Same construction', 2, 0, 'ocr'), ('Different', 3, 0, 'ocr')],
        notes=['The code-generator example as a picture. **In**: a messaging-specification document (message names, attributes, operations).',
               'The **code generator** runs the **same construction process** for every language: open and read the file, find message names, attributes and operations, generate language-specific code, close the file.',
               '**Out**: Java, C++ or C# code, i.e. **different representations** of the same messages. That combination (fixed process, varying output) is exactly the Builder’s use case.']),
    11: dict(
        hl=[('Director', 1, 0, 'ocr'), ('AbstractBuilder', 2, 0, 'ocr'), ('ConcreteBuilder', 3, 0, 'ocr'), ('Product', 4, 0, 'ocr')],
        notes=['**Director** with `construct()`: “this guy orchestrates the creational process”. It holds an AbstractBuilder and calls its steps in order.',
               '«interface» **AbstractBuilder** with *buildProductPartA/B/C()*: these methods specify the multistep creational process for the product.',
               '**ConcreteBuilder** must implement those creational methods, plus `getProduct()`.',
               '**Product**: the class being built; the ConcreteBuilder creates and assembles it. Creator classes = Director, AbstractBuilder, ConcreteBuilder; product class = Product.'],
        exam=[likely('In the Builder pattern, which participant calls the construction steps in the right order?', a=0,
                     opts=['Director', 'ConcreteBuilder', 'Product', 'Client'])]),
    12: dict(
        hl=[('Recognize it', 1), ('Define the Product', 2), ('Declare the Builder interface', 3), ('Implement Concrete Builders', 4), ('Create the Director', 5), ('Verify extensibility', 6)],
        notes=['**0) Recognise a Builder problem**: the same sequence of steps must give different final representations; a complex object is built step by step; construction should be hidden from the client and new variants easy to add.',
               '**1) Define the product**: name what is built (Report, Burger, Form, House) and list its parts.',
               '**2) Declare the builder interface**: the multistep API (`buildPartA(...)`, `buildPartB(...)`, `getResult()`). Steps say *what* to build, not how.',
               '**3) Implement concrete builders**: one class per variant (PdfReportBuilder, HtmlReportBuilder), each storing intermediate state; `getResult()` returns the finished product.',
               '**4) Create the director** (optional but recommended): a `construct()` method calls the steps in sequence, keeping the process reusable and consistent. **5) Client wiring**: pick a ConcreteBuilder, pass it to the Director, call `construct()`, get the product.',
               '**6) Verify extensibility**: a new variant needs only a new ConcreteBuilder; client and director stay unchanged.']),
    13: dict(
        hl=[('Product', 1, 0, 'ocr'), ('Builder Interface', 2, 0, 'ocr'), ('Concrete Builders', 3, 0, 'ocr'), ('Director', 4, 0, 'ocr'), ('Points to Remember', 5)],
        notes=[{'text': 'The skeleton in Java:', 'code': [
                    ('class Product { /* the final object being built */ }', '1. The product.'),
                    ('interface Builder { void buildPartA(); void buildPartB(); Product getResult(); }', '2. The builder interface.'),
                    ('class JavaBuilder implements Builder { buildPartA() { /* step A for Java */ } … getResult() { return new Product(); } }', '3. Concrete builders (CSharpBuilder the same, with C# steps).'),
                    ('class Director { private Builder builder; Director(Builder builder) { this.builder = builder; }', '4. The director receives a builder…'),
                    ('    Product construct() { builder.buildPartA(); builder.buildPartB(); return builder.getResult(); } }', '…and runs the steps in a fixed order.'),
                    ('Builder javaBuilder = new JavaBuilder(); Director director = new Director(javaBuilder); Product javaProduct = director.construct();', '5. The client chooses the builder; C# is the same three lines with CSharpBuilder.')]},
               '**Points to remember**: product = the final object; builder interface = declares the steps; concrete builders = implement them differently; director = controls the order; client = chooses the builder. Same construction steps, different final representations.']),
    14: dict(
        hl=[('Director', 1, 0, 'ocr'), ('Abstract Builder', 2, 0, 'ocr'), ('Concrete', 3, 0, 'ocr'), ('Notice that we moved', 4, 0, 'ocr')],
        notes=['The code-generator design. **Director**: CodeGenerator (`generateCode()`).',
               '**Abstract builder**: MessageBuilder with the steps `buildNewClass(name)`, `buildClassAttributes(attributes)`, `buildClassOperations(operations)`, `closeClass()`, `getFileExtension()`, plus `getGeneratedProduct()`.',
               '**Concrete builders**: CppMessageBuilder and JavaMessageBuilder implement every step for their language. The **product** is GeneratedProduct (`addCode()`, `getCode()`, `getStats()`…).',
               'Note: `getGeneratedProduct()` was moved up into the abstract builder, because every language returns the same product type. That isn’t possible in every problem (if products differ per builder, each builder returns its own).']),
    15: dict(
        hl=[('Separates', 1), ('Changes to existing representations', 2), ('finer control', 3), ('discrete points', 3), ('maintainability, testability, and reusability', 4)],
        notes=['It **separates** construction from representation, so new representations (a C# builder) are added easily.',
               '**Existing representations change** without touching the creational process (the director).',
               'It gives **finer control** over construction: parts of an object are created at **discrete points in time**, unlike Abstract Factory, which creates each product in one call.',
               'It improves **maintainability, testability and reusability**.'],
        exam=[likely('Give two benefits of the Builder pattern.',
                     a='Construction is separated from representation, so new representations can be added without changing the construction process; it gives finer control, building parts at discrete points; it improves maintainability, testability and reuse.')]),
    16: dict(
        hl=[('Idea in Simple Words', 1, 0, 'ocr'), ('Without Builder', 2, 0, 'ocr'), ('With Builder Pattern', 3, 0, 'ocr')],
        notes=['In simple words: use Builder when an object is created step by step instead of all at once, like ordering food where you pick bread, meat and sauce and the meal is assembled.',
               'Without it: `Burger("big bun", "double meat", "cheese", "ketchup", "lettuce")`, a constructor with many parameters that is hard to read, hard to customise and easy to get wrong.',
               'With it: `new BurgerBuilder().addBun("Big Bun").addPatty("Beef").addCheese().addLettuce().addSauce("Ketchup").build();`, each step named and optional. (This fluent, chained style is a common variant of Builder without a director.)']),
    17: dict(
        hl=[('Beef Burger', 1), ('Add Bun', 2), ('Sesame Bun', 3), ('construction steps are the same', 4), ('draw class diagram based on builder pattern', 5)],
        notes=['The exercise: a restaurant prepares **Beef** and **Chicken** burgers.',
               'Every burger is prepared in the **same sequence**: add bun, add patty, add sauce.',
               'The **ingredients differ**: beef = sesame bun + beef patty + BBQ sauce; chicken = whole-wheat bun + chicken patty + mayo.',
               'Requirements: same steps for all burgers, new burger types easy to add, and the client chooses only the type while construction stays hidden: textbook Builder.',
               'Tasks: draw the class diagram and write the Java (solution on slides 19–20).']),
    18: dict(
        hl=[('Director', 1, 0, 'ocr'), ('ConcreteBuilder', 2, 0, 'ocr')],
        notes=['The structure again, as the template for the burger answer: Director (Chef) → AbstractBuilder (BurgerBuilder) ← ConcreteBuilders (BeefBurgerBuilder, ChickenBurgerBuilder) → Product (Burger).']),
    19: dict(
        hl=[('Product (Burger)', 1, 0, 'ocr'), ('Builder Interface', 2, 0, 'ocr'), ('Concrete Builders', 3, 0, 'ocr'), ('Director', 4, 0, 'ocr')],
        notes=[{'text': 'The solution:', 'code': [
                    ('class Burger { String bun; String patty; String sauce; public String toString() { return bun + " + " + patty + " + " + sauce; } }', '1. The product.'),
                    ('interface BurgerBuilder { void addBun(); void addPatty(); void addSauce(); Burger getBurger(); }', '2. The three steps plus the result.'),
                    ('class BeefBurgerBuilder implements BurgerBuilder { Burger burger = new Burger();', '3. The beef recipe keeps its burger under construction…'),
                    ('    public void addBun() { burger.bun = "Sesame Bun"; } … addPatty → "Beef Patty" … addSauce → "BBQ Sauce"', '…and fills each part its own way.'),
                    ('class ChickenBurgerBuilder implements BurgerBuilder { … "Whole Wheat Bun" … "Chicken Patty" … "Mayo Sauce" }', 'The chicken recipe: same steps, other ingredients.'),
                    ('class Chef { private BurgerBuilder builder; Chef(BurgerBuilder builder) { this.builder = builder; }', '4. The director.'),
                    ('    public Burger construct() { builder.addBun(); builder.addPatty(); builder.addSauce(); return builder.getBurger(); } }', 'The fixed order lives here, once.')]}]),
    20: dict(
        hl=[('Client Code', 1, 0, 'ocr')],
        notes=[{'text': '5. The client:', 'code': [
                    ('Chef beefChef = new Chef(new BeefBurgerBuilder());', 'Choose the burger type by choosing the builder.'),
                    ('Burger beefBurger = beefChef.construct(); System.out.println("Built: " + beefBurger);', 'Prints “Built: Sesame Bun + Beef Patty + BBQ Sauce”.'),
                    ('Chef chickenChef = new Chef(new ChickenBurgerBuilder()); Burger chickenBurger = chickenChef.construct();', 'Same director code, different representation.')]},
               'A Veggie burger would need only a VeggieBurgerBuilder; Chef and the client logic stay unchanged.']),
    21: dict(
        hl=[('encapsulates both the creational process and the', 1), ('created', 2), ('multistep', 3), ('discrete points', 4)],
        notes=['Builder is an object creational pattern that **encapsulates both the creational process and the representation** of product objects.',
               'In **Abstract Factory**, the various product objects are **created all at once** (one call each).',
               'Builder lets clients control the **multistep** creational process of a **single** product.',
               'It dictates the creation of individual parts at **discrete points** throughout the software’s operation.']),
    22: dict(
        hl=[('code generator', 1), ('interface specification document (ICD)', 1), ('generates C++ classes', 2), ('Java and C#', 3)],
        notes=['The textbook example: a **code generator** works from an interface specification document (ICD) for custom hardware.',
               'The company sells the hardware plus a library to monitor and control it. The generator reads the messaging specification and **generates C++ classes** that customers use with the hardware.',
               'The ICD is complex, and customers now want **Java and C#** as well: the same generation process, new representations, so Builder.']),
    23: dict(
        hl=[('Director', 1, 0, 'ocr'), ('Abstract Builder', 2, 0, 'ocr'), ('Concrete', 3, 0, 'ocr')],
        notes=['The design (same as slide 14): CodeGenerator is the **director**, MessageBuilder the **abstract builder**, CppMessageBuilder and JavaMessageBuilder the **concrete builders**, GeneratedProduct the **product**. A C# version would add only a CSharpMessageBuilder.']),
    24: dict(
        hl=[('The Builder interface for', 1, 0, 'ocr'), ('The same', 2, 0, 'ocr')],
        notes=[{'text': 'The builder interface in C++:', 'code': [
                    ('class MessageBuilder { public:', 'The builder interface for generating code.'),
                    ('    virtual void buildNewClass(string name) = 0;', 'Step: start a class. `= 0` makes it pure virtual (abstract).'),
                    ('    virtual void buildClassAttributes(string attributeList) = 0;', 'Step: its attributes.'),
                    ('    virtual void buildClassOperations(string operationList) = 0;', 'Step: its operations.'),
                    ('    virtual void closeClass() = 0; virtual string getFileExtension() = 0;', 'Step: close it; and the language’s file extension.'),
                    ('    GeneratedProduct* getGeneratedProduct() { return _codeProduct; }', 'Shared by all builders: return the product.'),
                    ('private: GeneratedProduct* _codeProduct; };', 'The product holds the generated code and statistics.')]},
               'The same steps are used to create products in every target language.']),
    25: dict(
        hl=[('C++ Builder', 1, 0, 'ocr'), ('Step 1', 2, 0, 'ocr'), ('C++ Product Created!', 3, 0, 'ocr')],
        notes=['The C++ concrete builder, step by step (each step adds its code to the product with `getGeneratedProduct()->addCode(...)`).',
               '**Step 1** `buildNewClass(name)` writes `class MessageOne {`. **Step 2** `buildClassAttributes` adds `private: int attributeOne; int attributeTwo;`. **Step 3** `buildClassOperations` adds `public: void setValueOne(unsigned char x);`. **Step 4** `closeClass()` writes `};`.',
               'Result: a complete C++ class, the “C++ product created”. JavaMessageBuilder runs the same four calls and produces a Java class instead.']),
    26: dict(
        hl=[('object', 1), ('creational', 1), ('prevent objects', 1), ('one instance', 2), ('global', 2)],
        notes=['**Singleton** is an object creational pattern that **prevents a class from being instantiated more than once** in a running program.',
               'Its intent: **ensure a class has only one instance, and provide a global point of access to it**.'],
        exam=[likely('Which pattern guarantees exactly one instance of a class with a global access point?', a=0,
                     opts=['Singleton', 'Prototype', 'Factory Method', 'Builder'])]),
    27: dict(
        hl=[('Private Constructor', 1, 0, 'ocr'), ('Private static instance', 2, 0, 'ocr'), ('Public static getInstance()', 3, 0, 'ocr')],
        notes=['The UML, member by member. `-Singleton()`: a **private constructor** (minus sign) restricts instantiation, so no other class can call `new Singleton()`.',
               '`-instance : Singleton` (underlined): a **private static** attribute that holds the one instance. Underlined members are static in UML.',
               '`+getInstance() : Singleton` (underlined): a **public static** method that creates the instance if needed and gives everyone access to the one and only object. `+operation()` stands for the class’s ordinary behaviour.'],
        exam=[asked('f252', 'Q6-2 · 2 marks', 'Draw the standard class diagram of the Singleton pattern and convert it into code (any language).',
                    a='Diagram: class **Singleton** with `- instance: Singleton {static}`, `- Singleton()`, `+ getInstance(): Singleton {static}`. Code: `public class Singleton { private static Singleton instance; private Singleton() { } public static Singleton getInstance() { if (instance == null) { instance = new Singleton(); } return instance; } }`. The private constructor stops other classes calling `new`; the instance is created on first use and the same one is returned afterwards.')]),
    28: dict(
        hl=[('event logging', 1), ('event manage', 2), ('only one instance of the event manager', 3), ('Event Manager', 2)],
        notes=['The problem: an application needs **event logging**. Many objects generate events (actions, status, errors).',
               'The design: one central **event manager** that every object uses. It creates an event list on instantiation, adds events as they are logged, and writes them to a file at specific points.',
               'To prevent conflicts (two managers writing the same file), there must be **only one instance of the event manager** at any time: Singleton.']),
    29: dict(
        hl=[('Why Is There a Problem?', 1), ('Multiple log files', 2), ('Why Singleton Fixes This?', 3)],
        notes=['Why there is a problem: login, payment and notification systems all need to log. If each creates its own logger, you get **multiple log files or conflicting writes**, inconsistent data, and a system that is harder to debug and audit.',
               'The real problem is conflicts, redundancy and loss of control.',
               'Singleton fixes it: only one EventManager exists, every part shares it, so there is one log file and central control. One object → one responsibility → no conflict.']),
    30: dict(
        hl=[('logEvent', 1, 0, 'ocr'), ('operation()', 2, 0, 'ocr')],
        notes=['The example mapped onto the generic structure: **EventManager** has `-instance_ : EventManager*` (static), a private constructor `-EventManager()`, `+getInstance(): EventManager*` (static) and `+logEvent(eventDescription: string)`.',
               'Compared with the generic **Singleton** box, only the names changed: `logEvent` is the class’s real `operation()`.']),
    31: dict(
        hl=[('static', 1, 0, 'ocr'), ('private Singleton()', 2, 0, 'ocr')],
        notes=[{'text': 'The Java class:', 'code': [
                    ('public class Singleton {', ''),
                    ('    private static Singleton singleton = new Singleton();', 'The one instance, created when the class loads (eager initialisation).'),
                    ('    private Singleton() { }', 'A private constructor prevents any other class from instantiating it.'),
                    ('    public static Singleton getInstance() { return singleton; }', 'The static “instance” method: always returns the same object.'),
                    ('    protected static void demoMethod() { System.out.println("demoMethod for singleton"); } }', 'Other methods, reached through the instance.')]},
               'A **static** variable is allocated statically: it lives for the entire run of the program, which is why it can hold the single instance. Compare with the exam version (slide 27), which creates the instance lazily inside getInstance().']),
    32: dict(
        hl=[('Singleton.getInstance', 1, 0, 'ocr'), ('The main program file', 2, 0, 'ocr')],
        notes=[{'text': 'Using it:', 'code': [
                    ('public class SingletonDemo { public static void main(String[] args) {', 'The main program.'),
                    ('    Singleton tmp = Singleton.getInstance();', 'Not `new Singleton()` (that would not compile): ask the class for its instance.'),
                    ('    tmp.demoMethod(); } }', 'Use it like any object.')]}]),
    33: dict(
        hl=[('constructor', 1), ('private static member', 2), ('public static getInstance()', 3)],
        notes=['**1.** Make the **constructor private**.',
               '**2.** Define a **private static** attribute that stores a reference to the one instance.',
               '**3.** Create a **public static `getInstance()`** method that uses the private constructor to create one object (if it doesn’t exist yet) and returns it to clients. These three steps are the whole answer to “write the Singleton code”.'],
        exam=[likely('List the three steps to design a class with the Singleton pattern.',
                     a='(1) Make the constructor private. (2) Add a private static attribute holding the single instance. (3) Add a public static getInstance() that creates the instance through the private constructor if it doesn’t exist and returns it.')]),
    34: dict(
        hl=[('controlled access to a single instance', 1), ('variable number of instances', 2), ('multithreading', 3)],
        notes=['**Benefit**: controlled access to a **single instance** of a type.',
               '**Benefit**: it can be customised to allow a **variable number** of instances (e.g. a pool of at most N), since creation goes through one method.',
               '**Drawback**: it doesn’t work well in **multithreaded** environments: two threads calling `getInstance()` at the same moment can both see `instance == null` and create two objects, unless the method is synchronised.'],
        exam=[likely('True or false: a Singleton’s constructor should be public so the instance can be created when needed.', tf=False,
                     why='It must be private; clients get the instance through the public static getInstance().'),
              likely('Why can the lazy Singleton fail in a multithreaded program, and how is it fixed?',
                     a='Two threads can call getInstance() at the same time, both find instance == null and both create an object. Fix: synchronise getInstance() (or use eager initialisation / double-checked locking).')]),
    35: dict(
        hl=[('Banking App', 1), ('Step 1', 2, 0, 'ocr'), ('Why don', 3)],
        notes=['The scenario: a banking app’s login, transaction and notification systems all log events, and everything must go to **one log in the correct order**.',
               {'text': 'Step 1, the Singleton class:', 'code': [
                    ('public class EventLogger { private static EventLogger instance;', 'The one instance.'),
                    ('    private EventLogger() {}', 'Prevents outside creation.'),
                    ('    public static EventLogger getInstance() { if (instance == null) { instance = new EventLogger(); } return instance; }', 'The global access point, created on first use.'),
                    ('    public void log(String message) { System.out.println("Log: " + message); } }', 'In real use this would write to a file.')]},
               'Step 2, the login system: `EventLogger.getInstance().log("User " + username + " logged in.");`. Why not `instance.log()`? Because `instance` is private and static inside the class; from outside, `getInstance()` is the public way to reach the one object, and then you call `.log()` on it.']),
    36: dict(
        hl=[('Transaction System', 1), ('Notification System', 2), ('Main Class to Run the App', 3)],
        notes=['The **transaction system** logs `"Transferred $" + amount + " from " + from + " to " + to` through `EventLogger.getInstance().log(...)`.',
               'The **notification system** logs `"Notification sent to " + user + ": " + message` the same way.',
               'The **main class** runs login, a transfer and a notification, then prints `EventLogger.getInstance() == EventLogger.getInstance()`, which is `true`: proof that all three systems used the same logger object.']),
    37: dict(
        hl=[('Create the one and only instance', 1, 0, 'ocr')],
        notes=[{'text': 'The textbook EventManager in C++:', 'code': [
                    ('EventManager* EventManager::_instance = 0;', 'Initialise the static member: no instance yet.'),
                    ('EventManager::EventManager(void) { /* Intentionally left blank. */ }', 'The private constructor.'),
                    ('EventManager* EventManager::getInstance(void) {', 'The global point of access.'),
                    ('    if (_instance == 0) { _instance = new EventManager; }', 'Create the one and only instance the first time.'),
                    ('    return _instance; }', 'Every call returns the same pointer.'),
                    ('void EventManager::logEvent(string eventDescription) { cout << eventDescription << endl; }', 'The method that logs events.')]}]),
    38: dict(
        hl=[('Circle', 1), ('by copying existing ones', 2), ('Tasks:', 3), ('How Students Should See It', 4)],
        notes=['An extra exercise on the fifth creational pattern, **Prototype**: a drawing app needs many copies of **Circle** (radius) and **Square** (side).',
               'New shapes should be created **by copying existing ones** instead of from scratch.',
               'Tasks: draw the class diagram; write Java with a common interface, a self-copy method in each shape, and a `main` that copies a Circle and a Square.',
               'The plan: a Prototype interface with `clone()`, concrete prototypes Circle and Square, and a client that clones instead of calling `new`.'],
        exam=[likely('Which pattern creates new objects by copying an existing instance?', a=0, opts=['Prototype', 'Builder', 'Singleton', 'Composite'])]),
    39: dict(
        hl=[('interface Shape', 1, 0, 'ocr')],
        notes=[{'text': 'Step 1:', 'code': [('interface Shape { Shape clone(); }', 'Every shape can duplicate itself; the copy is returned as a Shape.')]}]),
    40: dict(
        hl=[('class Circle implements Shape', 1, 0, 'ocr')],
        notes=[{'text': 'Step 2:', 'code': [
                    ('class Circle implements Shape { int radius; Circle(int r) { this.radius = r; }', 'A concrete prototype with its state.'),
                    ('    @Override public Shape clone() { return new Circle(this.radius); }', 'Makes a copy with the same radius.'),
                    ('    public void show() { System.out.println("Circle with radius " + radius); } }', '')]}]),
    41: dict(
        hl=[('class Square implements Shape', 1, 0, 'ocr')],
        notes=[{'text': 'Step 3:', 'code': [
                    ('class Square implements Shape { int side; Square(int s) { this.side = s; }', 'The second concrete prototype.'),
                    ('    @Override public Shape clone() { return new Square(this.side); }', 'Copies the side length.'),
                    ('    public void show() { System.out.println("Square with side " + side); } }', '')]}]),
    42: dict(
        hl=[('PrototypeDemo', 1, 0, 'ocr'), ('Expected Output', 2, 0, 'ocr'), ('Key Idea', 3, 0, 'ocr')],
        notes=[{'text': 'Step 4, the client:', 'code': [
                    ('Shape c1 = new Circle(10); Shape c2 = c1.clone();', 'Create an original circle, then clone it.'),
                    ('Shape s1 = new Square(5); Shape s2 = s1.clone();', 'The same for a square.'),
                    ('((Circle)c1).show(); ((Circle)c2).show(); ((Square)s1).show(); ((Square)s2).show();', 'Prints “Circle with radius 10” twice and “Square with side 5” twice.')]},
               'Key idea: a clone is an identical but separate copy (c1 and c2 have equal state but are different objects). With nested mutable fields, decide between shallow and deep copies.']),
    43: dict(
        hl=[('Builder', 1), ('Singleton', 1), ('structural', 2), ('behavioral', 2)],
        notes=['This lecture: **Builder** and **Singleton** (plus a Prototype exercise), completing the creational patterns.',
               'Next: **structural** and **behavioural** design patterns (Chapter 7).']),
}

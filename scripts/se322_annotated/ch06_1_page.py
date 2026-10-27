"""SE322 Chapter 6, Lecture 1 (Design patterns overview and the Abstract Factory): page content.

Schema: see annotated_page.py. Most of this deck is UML and code pictures, so many marks use 'ocr' (skipped if
OCR can't read them) and the notes walk through the code. Past-exam questions are copied from the papers in
exams/; everything else is a prediction (Abstract Factory has not appeared on a past paper yet).
"""
from .common import likely

TITLE = 'Design Patterns and the Abstract Factory'
CHAPTER = 'SE322 · Chapter 6 · Lecture 1'

OVERVIEW = {
    'summary': ('Design patterns are recurring solutions to object-oriented design problems in a given context, smaller in '
                'scale than architectural patterns. They are classified by purpose (creational, structural, behavioural) and '
                'by scope (class or object). Creational patterns control how objects are created. The first one, Abstract '
                'Factory, gives a client one interface for creating a whole family of related products (dark-theme widgets, '
                'advanced computer parts) without naming their concrete classes, so switching families means swapping one '
                'factory object.'),
    'ideas': [
        ('Purpose and scope', 'Creational = creating objects; structural = composing structures; behavioural = interaction and responsibilities. Class scope = design time; object scope = run time.'),
        ('Five creational patterns', 'Abstract Factory, Factory Method, Builder, Prototype, Singleton.'),
        ('Abstract Factory roles', 'AbstractFactory (one create method per product), ConcreteFactory per family, AbstractProduct per product type, ConcreteProducts, and a Client that sees only the abstract types.'),
        ('Trade-off', 'Adding a new family is easy (a new factory and products, OCP); adding a new kind of product touches every factory. Many classes.'),
    ],
    'sections': [
        ('Slides 1–7', 'Design patterns: definition, purpose and scope, documentation, creational patterns'),
        ('Slides 8–17', 'Abstract Factory: intent, the theme example, structure, adding families and products'),
        ('Slides 18–31', 'Computer-store example: products, factories, client and main program'),
        ('Slides 32–39', 'Step-by-step summary, pros and cons, the car-factory exercise, recap'),
    ],
    'exam': ('Final 252 Q6 examined creational patterns through Builder and Singleton (Lectures 2–3). For Abstract '
             'Factory expect a design question: given a scenario with product families (themes, car brands, computer '
             'grades), name the pattern, draw the class diagram with factory and product interfaces, and explain how a new '
             'family is added.'),
}

TITLES = {3: 'Patterns in Detailed Design', 10: 'Extra: Question – Dark and Light themes', 11: 'Extra: The theme demo running',
          12: 'Extra: Theme example class diagram', 13: 'Extra: Theme example code, steps 1–3', 14: 'Extra: Theme example code, steps 4–5',
          15: 'The Abstract Factory Pattern: structure', 16: 'The Abstract Factory Pattern: adding a new family',
          17: 'The Abstract Factory Pattern: adding a new product', 19: 'The Abstract Factory Pattern – Example: the computer store',
          20: 'The Abstract Factory Pattern – Example: class diagram', 21: 'The product interfaces', 25: 'The CPU Product Implementation',
          31: 'Extra: The computer-parts demo running', 34: 'Abstract Factory Step by Step Summary (repeated)', 35: 'Cons & Pros of Abstract Factory (repeated)',
          36: 'Extra Example: RiyadhHQ car factories', 37: 'Extra: RiyadhHQ class diagram', 38: 'Extra: Do we create concrete classes?'}

SLIDES = {
    1: dict(
        hl=[('[Creational Design Patterns]', 1)],
        notes=['Chapter 6 starts **design patterns**, the detailed-design counterpart of Chapter 4’s architectural patterns. This lecture: what design patterns are, how they are classified, and the first creational pattern, **Abstract Factory**.']),
    2: dict(
        hl=[('Patterns in Detailed Design', 1), ('Classification of Design Patterns', 2), ('Abstract Factory', 3)],
        notes=['First, how design patterns differ from architectural patterns.',
               'Then how they are classified (purpose and scope) and documented.',
               'Then the creational patterns, starting with **Abstract Factory** and its computer-store example.']),
    3: dict(
        hl=[('recurring solutions to object-oriented design', 1), ('different than architectural', 2), ('reusable solutions to common problems', 1)],
        notes=['**Design patterns** are recurring solutions to object-oriented design problems in a particular context. They give templates that solve problems efficiently and consistently, so developers don’t reinvent the wheel.',
               'They are **different from architectural patterns** (Chapter 4, slide 11 of Lecture 1): architectural patterns fix the system-wide structure; design patterns work at the level of classes and objects inside a subsystem and don’t change the overall structure.']),
    4: dict(
        hl=[('Purpose', 1), ('Creational:', 2), ('Structural:', 3), ('Behavioral:', 4)],
        notes=['Patterns are classified by **purpose** (what kind of problem they solve) and **scope** (next slide).',
               '**Creational**: deal with the creation of objects (this chapter).',
               '**Structural**: deal with composing objects and classes into larger structures (Chapter 7: Adapter, Composite…).',
               '**Behavioural**: deal with how classes interact, how behaviour varies, and how responsibilities are assigned between objects (Chapter 7: Observer…).'],
        exam=[likely('Patterns that deal with how classes interact and how responsibilities are assigned between objects are:', a=0,
                     opts=['Behavioral', 'Creational', 'Structural', 'Architectural'])]),
    5: dict(
        hl=[('scope criterion', 1), ('classes', 2), ('objects', 3), ('Class-level patterns:', 2), ('Object-level patterns:', 3)],
        notes=['The **scope** criterion says whether a pattern applies mainly to classes or to objects.',
               '**Class-level** patterns deal with relationships between classes, fixed at design time through inheritance. Examples in the table: Factory Method (creational), Adapter (structural), Interpreter and Template Method (behavioural).',
               '**Object-level** patterns deal with relationships between objects, set up at run time through composition. Most patterns are here: Abstract Factory, Builder, Prototype, Singleton (creational); Adapter, Bridge, Composite, Decorator, Façade, Proxy (structural); Chain of Responsibility, Command, Iterator, Mediator, Memento, Flyweight, Observer, State, Strategy, Visitor (behavioural).'],
        exam=[likely('Classify Abstract Factory, Composite and Observer by purpose and scope.',
                     a='Abstract Factory: creational, object scope. Composite: structural, object scope. Observer: behavioural, object scope.')]),
    6: dict(
        hl=[('design patterns are', 1), ('intent', 2), ('not concerned with', 3, 0, 'ocr')],
        notes=['Each pattern is documented with the same categories, so patterns can be compared and looked up.',
               '**The categories**: name and classification, intent (what problem it solves), also known as, motivation (an example scenario), applicability (when to use it), structure (UML class diagram), participants, collaborations, consequences (good and bad effects), implementation, sample code, known uses, related patterns.',
               'Note on the slide: this course is **not** concerned with presenting the full documentation for each pattern; focus on intent, structure and participants.']),
    7: dict(
        hl=[('abstract and control the way objects are created', 1), ('common creational interface', 1), ('The AbstractFactory', 2), ('The Singleton', 2)],
        notes=['**Creational** patterns abstract and control how objects are created, by giving clients a **common creational interface** instead of scattered `new ConcreteClass()` calls.',
               'The five: **Abstract Factory**, **Factory Method**, **Builder**, **Prototype**, **Singleton**. This chapter covers Abstract Factory, Factory Method, Builder and Singleton.'],
        exam=[likely('Which of these is NOT a creational pattern?', a=0, opts=['Composite', 'Builder', 'Singleton', 'Prototype'])]),
    8: dict(
        hl=[('object-creational design pattern', 1), ('family of products', 1), ('creating families of related objects', 2), ('creator classes and product classes', 3)],
        notes=['The **Abstract Factory** is an object-creational pattern that manages and encapsulates the creation of a set of objects that belong together: a **family of products**.',
               'Its **intent**: provide an interface for **creating families of related objects without specifying their concrete classes**.',
               'Like all creational patterns it has **creator** classes (the factories) and **product** classes. (Some creational patterns, such as Singleton, fuse creator and product into one class.)'],
        exam=[likely('What is the intent of the Abstract Factory pattern?', a=0,
                     opts=['Provide an interface for creating families of related objects without specifying their concrete classes', 'Ensure a class has exactly one instance', 'Construct a complex object step by step', 'Create objects by copying a prototype'])]),
    9: dict(
        hl=[('Encapsulation:', 1), ('Flexibility:', 2)],
        notes=['The same definition, plus the two benefits. **Encapsulation**: the client knows the abstract product names (Button, Textbox) but **not** the concrete classes (DarkButton, LightTextbox).',
               '**Flexibility**: a new family is added by creating a new factory, without changing the client.']),
    10: dict(
        hl=[('Dark Theme', 1), ('GUIFactory', 2), ('DarkThemeFactory', 3), ('One stop shop', 4)],
        notes=['The exercise: a program with a **Dark** theme (black button and text field) and a **Light** theme (white ones). Instead of `if (dark)` checks everywhere, use Abstract Factory.',
               'The factory interface **GUIFactory** declares `createButton()` and `createTextField()`.',
               '**DarkThemeFactory** returns a DarkButton and DarkTextField; **LightThemeFactory** returns the light versions. The client asks its factory for a Button and a TextField and never knows which concrete class came back.',
               'Adding a Blue theme means adding BlueThemeFactory, BlueButton and BlueTextbox, with no change to the client. In one line: Abstract Factory is a “one-stop shop” for creating a related family of objects while hiding their concrete classes.']),
    11: dict(
        hl=[('Dark Button', 1, 0, 'ocr'), ('Light Button', 1, 0, 'ocr')],
        notes=['The theme example running. Choosing **Dark** and pressing Apply Theme swaps in the DarkThemeFactory, and the window shows a dark button and text box; choosing **Light** swaps in the LightThemeFactory. The client code that builds the window is identical in both cases; only the factory object changed.']),
    12: dict(
        hl=[('GUIFactory', 1, 0, 'ocr'), ('Button', 2, 0, 'ocr'), ('LightThemeFactory', 3, 0, 'ocr'), ('Client', 4, 0, 'ocr')],
        notes=['The class diagram mapped onto the pattern’s role names. «interface» **GUIFactory** (AbstractFactory) declares `createButton()` and `createTextField()`.',
               '«interface» **Button** (AbstractProductA) and **TextField** (AbstractProductB) are the product types the client uses.',
               '**LightThemeFactory** (ConcreteFactory1) creates LightButton and LightTextField (ConcreteProductA1/B1); **DarkThemeFactory** (ConcreteFactory2) creates DarkButton and DarkTextField (A2/B2). The hollow triangles are realizations; the arrows from factories to products show what each creates.',
               'The **Client** (AbstractFactoryDemo) depends only on the three interfaces.']),
    13: dict(
        hl=[('Step 1', 1, 0, 'ocr'), ('Step 2', 2, 0, 'ocr'), ('Step 3', 3, 0, 'ocr')],
        notes=[{'text': 'The code, steps 1–3:', 'code': [
                    ('interface GUIFactory { Button createButton(); TextField createTextField(); }', 'Step 1: the abstract factory, one create method per product type.'),
                    ('class DarkThemeFactory implements GUIFactory {', 'Step 2: a concrete factory for the dark family…'),
                    ('    public Button createButton() { return new DarkButton(); }', '…returns the dark button, typed as the abstract Button.'),
                    ('    public TextField createTextField() { return new DarkTextField(); } }', '…and the matching dark text field.'),
                    ('class LightThemeFactory implements GUIFactory { … new LightButton() … new LightTextField() … }', 'The light family, same shape.'),
                    ('interface Button { void draw(); }', 'Step 3: the abstract products.'),
                    ('interface TextField { void display(); }', '')]},
               'The only place `new DarkButton()` appears is inside DarkThemeFactory. That is the point of the pattern.']),
    14: dict(
        hl=[('Step 4', 1, 0, 'ocr'), ('Step 5', 2, 0, 'ocr')],
        notes=[{'text': 'Steps 4–5:', 'code': [
                    ('class DarkButton implements Button { public void draw() { …"Drawing Dark Button"… } }', 'Step 4: concrete products, one per family per product type.'),
                    ('class LightTextField implements TextField { public void display() { …"Showing Light TextField"… } }', '(LightButton and DarkTextField are written the same way.)'),
                    ('GUIFactory lightFactory = new LightThemeFactory();', 'Step 5, the client: pick a family once…'),
                    ('Button lightBtn = lightFactory.createButton(); TextField lightTxt = lightFactory.createTextField();', '…ask that factory for the parts, typed as abstract products…'),
                    ('lightBtn.draw(); lightTxt.display();', '…and use them. Prints “Drawing Light Button”, “Showing Light TextField”.'),
                    ('GUIFactory darkFactory = new DarkThemeFactory(); … darkBtn.draw(); darkTxt.display();', 'The dark run is the same code with a different factory.')]}]),
    15: dict(
        hl=[('Clients only know', 1, 0, 'ocr'), ('Factories need to obey', 2, 0, 'ocr'), ('Products need to obey', 2, 0, 'ocr'), ('Creator', 3, 0, 'ocr')],
        notes=['The general structure. Clients only know the **creator and product interfaces**, so behaviour can vary without changing client code.',
               'Every factory must obey the **Factory interface** (AbstractFactory with `createProductA()`, `createProductB()`), and every product its **Product interface**.',
               '**Creator classes** on the left (ConcreteFactory1, ConcreteFactory2); **product classes** on the right (ConcreteProductA1, B1, A2, B2). Each concrete factory creates exactly one family: factory 1 → A1 and B1; factory 2 → A2 and B2.'],
        exam=[likely('Name the participants of the Abstract Factory pattern.',
                     a='AbstractFactory (interface with one create method per product), ConcreteFactory (one per family), AbstractProduct (one interface per product type), ConcreteProduct (one class per family per product), and Client (uses only AbstractFactory and AbstractProduct).')]),
    16: dict(
        hl=[('Adding a new', 1, 0, 'ocr'), ('ConcreteFactory3', 2, 0, 'ocr')],
        notes=['**Adding a new family** (the red parts): add **ConcreteFactory3**, which implements the existing AbstractFactory, plus ConcreteProductA3 and B3, which implement the existing product interfaces.',
               'No existing class changes: the system is extended, not modified. This is the Open-Closed Principle in action, and the case Abstract Factory handles best.']),
    17: dict(
        hl=[('Adding a new', 1, 0, 'ocr'), ('AbstractProductC', 2, 0, 'ocr')],
        notes=['**Adding a new product to the existing families** is harder: add «interface» **AbstractProductC** and a concrete C product for every family (C1, C2, C3)…',
               '…and add `createProductC()` to the **AbstractFactory interface** and therefore to **every concrete factory**. Existing classes must change, which is the pattern’s main weakness.'],
        exam=[likely('Why is adding a new product type harder than adding a new family in Abstract Factory?',
                     a='A new family only needs a new concrete factory and new concrete products, with no change to existing code. A new product type needs a new create method in the AbstractFactory interface, so every existing concrete factory must be modified (plus a new abstract product and one concrete product per family).')]),
    18: dict(
        hl=[('advanced computers', 1), ('standard computers', 1), ('CPU, keyboard, and Monitor', 2), ('remote information sources', 3)],
        notes=['The textbook example: a computer store that sells two grades of computer, **advanced** (top of the line) and **standard** (inexpensive). More grades will come.',
               'Each computer is made of products from its own grade: an advanced CPU, keyboard and monitor, or standard ones. The example uses only **CPU, keyboard and monitor**.',
               'For each product the system looks up information (reviews, customer comments, manufacturer notes) from **remote sources**, and each grade’s products come from different sources. So “advanced” and “standard” are product families.']),
    19: dict(
        hl=[('Customer', 1, 0, 'ocr'), ('Each computer product is associated', 3, 0, 'ocr')],
        notes=['The store as a picture: a **customer** chooses an advanced or standard computer from the console menu (1 Advanced, 2 Standard).',
               'The **computer store** system builds that computer from its products.',
               'Each product is associated with one or more **information sources**, which are used to find out information about the product.']),
    20: dict(
        hl=[('ComputerPartsFactory', 1, 0, 'ocr'), ('AdvancedComputerPartsFactory', 2, 0, 'ocr'), ('Creator', 3, 0, 'ocr')],
        notes=['The example’s class diagram. «interface» **ComputerPartsFactory** declares `createMonitor()`, `createCPU()` and `createKeyboard()`.',
               '**AdvancedComputerPartsFactory** creates AdvancedCPU, AdvancedMonitor and AdvancedKeyboard; **StandardComputerPartsFactory** creates the standard ones.',
               '«interface» **CPU**, **Monitor** and **Keyboard** are the abstract products; **Computer** is the client and uses only the interfaces. Creator classes on the left, product classes on the right, exactly the general structure of slide 15.']),
    21: dict(
        hl=[('Interface for CPU', 1, 0, 'ocr'), ('Notice the italics', 2, 0, 'ocr')],
        notes=[{'text': 'Step 1 of the example: the product interfaces.', 'code': [
                    ('public interface Cpu { void displayCpuInformation(); }', 'Every CPU, of any grade, can display its information.'),
                    ('public interface Monitor { void displayMonitorInformation(); }', 'The monitor contract.'),
                    ('public interface Keyboard { void displayKeyboardInformation(); }', 'The keyboard contract.')]},
               'In the UML on the left the method names are in *italics*: in UML, italics mark abstract operations (no body).']),
    22: dict(
        hl=[('Cpu.java', 1, 0, 'ocr'), ('AdvancedCpu', 2, 0, 'ocr'), ('StandardCpu', 2, 0, 'ocr')],
        notes=['The CPU product design: «interface» **Cpu** with the abstract `displayCpuInformation()`, realised by **AdvancedCpu** and **StandardCpu**.',
               {'text': 'The code:', 'code': [
                    ('public class AdvancedCpu implements Cpu {', 'The advanced family’s CPU.'),
                    ('    public AdvancedCpu() { /* Constructor */ }', ''),
                    ('    @Override public void displayCpuInformation() { /* Implementation code */ } }', 'Its own way of displaying information.'),
                    ('public class StandardCpu implements Cpu { … @Override public void displayCpuInformation() { … } }', 'The standard family’s CPU, same contract.')]}]),
    23: dict(
        hl=[('Monitor.java', 1, 0, 'ocr'), ('AdvancedMonitor', 2, 0, 'ocr')],
        notes=['The monitor product design follows the same shape: «interface» **Monitor** with `displayMonitorInformation()`, realised by **AdvancedMonitor** and **StandardMonitor**, each with a constructor and an `@Override` of the display method.']),
    24: dict(
        hl=[('StandardKeyboard', 1, 0, 'ocr'), ('Hopefully by this point', 2, 0, 'ocr')],
        notes=['The keyboard product design: «interface» **Keyboard**, realised by **AdvancedKeyboard** and **StandardKeyboard**.',
               'As the callout says, the pattern for designing products should now be visible: one interface per product type, one concrete class per family.']),
    25: dict(
        hl=[('Information Source', 1, 0, 'ocr'), ('The code in this function', 2, 0, 'ocr')],
        notes=[{'text': 'The CPU implementations:', 'code': [
                    ('public class AdvancedCpu { public AdvancedCpu() { } …', 'Constructor intentionally left blank.'),
                    ('    public void displayCpuInformation() { … System.out.println("\\nInformation retrieved from source A.\\nDisplaying the advanced CPU’s information.\\n"); }', 'The advanced CPU gets its data from **information source A** (database A, file A…).'),
                    ('public class StandardCpu { … displayCpuInformation() { … "retrieved from source B" … } }', 'The standard CPU gets its data from **source B**.')]},
               'Each concrete product knows how to reach its own source (connection, format, location). The client never sees this: it just calls `displayCpuInformation()`.']),
    26: dict(
        hl=[('All other products', 1, 0, 'ocr')],
        notes=['The keyboards and monitors are implemented the same way: advanced products print “Information retrieved from source A”, standard products “source B”, each followed by its own display text.']),
    27: dict(
        hl=[('ComputerPartsFactory', 1, 0, 'ocr')],
        notes=['The example class diagram again (same as slide 20) before the factories are built: the creator classes are next.']),
    28: dict(
        hl=[('ComputerPartsFactory', 1, 0, 'ocr'), ('This design connects the products', 2, 0, 'ocr')],
        notes=['The factories in detail: «interface» **ComputerPartsFactory** with `createMonitor()`, `createCpu()`, `createKeyboard()`.',
               '**AdvancedComputerPartsFactory** is connected to AdvancedMonitor, AdvancedCpu and AdvancedKeyboard; **StandardComputerPartsFactory** to the standard three. This design connects the products from the previous slides to the factories that abstract their creation.']),
    29: dict(
        hl=[('ComputerStore', 1, 0, 'ocr'), ('computerPartsFactory', 2, 0, 'ocr')],
        notes=[{'text': 'The client:', 'code': [
                    ('class ComputerStore { private Monitor monitor; private Cpu cpu; private Keyboard keyboard;', 'Its fields are abstract product types only.'),
                    ('    public ComputerStore(ComputerPartsFactory computerPartsFactory) {', 'The factory is passed in: the store never chooses the family itself.'),
                    ('        this.monitor = computerPartsFactory.createMonitor();', 'Ask the factory for each part…'),
                    ('        this.cpu = computerPartsFactory.createCpu(); this.keyboard = computerPartsFactory.createKeyboard(); }', '…all from the same family, so they always match.'),
                    ('    public void displayMonitorInfo() { monitor.displayMonitorInformation(); }', 'Using a part: a call on the interface.'),
                    ('    … displayCpuInfo(), displayKeyboardInfo() …', '')]},
               'In the UML the client (Computer) depends on ComputerPartsFactory and on the Cpu, Monitor and Keyboard interfaces, and on nothing concrete.']),
    30: dict(
        hl=[('advancedFactory', 1, 0, 'ocr'), ('ComputerStore(advancedFactory)', 2, 0, 'ocr')],
        notes=[{'text': 'The main program:', 'code': [
                    ('AdvancedComputerPartsFactory advancedFactory = new AdvancedComputerPartsFactory();', 'Create one factory per family (the only place concrete factories are named).'),
                    ('StandardComputerPartsFactory standardFactory = new StandardComputerPartsFactory();', ''),
                    ('while (option != 0) { … option = scanner.nextInt();', 'Menu: 0 Exit, 1 Advanced, 2 Standard.'),
                    ('    if (option == 1) cs = new ComputerStore(advancedFactory);', 'Choosing the family = choosing the factory.'),
                    ('    else if (option == 2) cs = new ComputerStore(standardFactory);', ''),
                    ('    if (cs != null) { cs.displayMonitorInfo(); cs.displayKeyboardInfo(); cs.displayCpuInfo(); } }', 'The same calls for either family.')]},
               'The console on the right shows option 1: every line says “retrieved from source A”, so all parts came from the advanced family.']),
    31: dict(
        hl=[('AdvancedCPU', 1, 0, 'ocr')],
        notes=['A Swing version of the example: picking **Advanced** or **Standard** in the Factory menu and pressing Apply swaps the factory, and the CPU, monitor and keyboard shown (AdvancedCPU RTX-Pro, AdvancedMonitor 4K HDR, AdvancedKeyboard Mechanical RGB) all switch family together.']),
    32: dict(
        hl=[('Design the product interfaces', 1), ('Identify the different families', 2), ('Create the factory interface', 3), ('Create the Client', 4)],
        notes=['**Steps 1–3**: design the product interfaces (Cpu, Monitor, Keyboard); identify the families (standard, advanced); for each family, design concrete products that realise the interfaces.',
               '**Steps 4–6**: create the factory interface with one method per product interface (ComputerPartsFactory); create one concrete factory per family; associate each concrete factory with its family’s products.',
               '**Step 7**: create the client (Computer), associated with both the product interfaces and the factory interface.',
               'This recipe is the model answer to “apply Abstract Factory to …” questions: name the product interfaces, the families, the factory interface and the concrete factories, then draw them.'],
        exam=[likely('Apply the Abstract Factory pattern to a furniture shop that sells Modern and Victorian sets, each with a Chair and a Sofa. Name all classes and interfaces.',
                     a='Product interfaces: Chair, Sofa. Families: Modern, Victorian. Concrete products: ModernChair, ModernSofa, VictorianChair, VictorianSofa. Factory interface: FurnitureFactory with createChair(), createSofa(). Concrete factories: ModernFurnitureFactory, VictorianFurnitureFactory, each creating its own family. Client: Shop, which holds a FurnitureFactory and uses only Chair and Sofa.')]),
    33: dict(
        hl=[('Large number of classes', 1), ('Isolates concrete product classes', 2), ('consistency', 2), ('obeying the OCP', 2)],
        notes=['**Con**: a large number of classes (an interface per product, a class per product per family, a factory per family).',
               '**Pros**: concrete product classes are isolated, so they are easier to reuse; products within a family are guaranteed **consistent**; adding a new family needs no change to existing code, because additions are made by extension (**OCP**); modifiability increases. (The hidden con from slide 17: adding a new product type changes every factory.)'],
        exam=[likely('Give one disadvantage and two advantages of the Abstract Factory pattern.',
                     a='Disadvantage: many classes (and adding a new product type requires changing every factory). Advantages: concrete classes are isolated from the client; products of a family are always consistent; new families are added by extension without modifying existing code (OCP), increasing modifiability.')]),
    34: dict(
        hl=[('Design the product interfaces', 1)],
        notes=['The seven-step summary repeated (see slide 32).']),
    35: dict(
        hl=[('Large number of classes', 1)],
        notes=['The pros and cons repeated (see slide 33).']),
    36: dict(
        hl=[('RiyadhHQ', 1), ('CarFactory', 2), ('JeddahCarFactory', 3), ('Now answer the following', 4)],
        notes=['An exercise: **RiyadhHQ** is the client that requests cars from different branches, without creating JeddahMercedes or DammamBMW itself.',
               '**CarFactory** is the abstract factory: it defines the products RiyadhHQ can request, a Mercedes and a BMW.',
               '**JeddahCarFactory** makes JeddahMercedes and JeddahBMW; **DammamCarFactory** makes DammamMercedes and DammamBMW. Each city is a family.',
               'The questions: RiyadhHQ doesn’t need to know the city because it only uses CarFactory, Mercedes and BMW; switching factories at run time is just passing a different CarFactory object; and the example shows Abstract Factory because each concrete factory creates a consistent family of related products behind one interface.'],
        exam=[likely('Why does RiyadhHQ not need to know which branch produced its cars, and how does it switch branches?',
                     a='It depends only on the CarFactory interface and the abstract Mercedes and BMW types, so the concrete classes stay hidden in the branch factories. Switching branches means giving RiyadhHQ a different CarFactory object (JeddahCarFactory or DammamCarFactory) at run time; its own code does not change.')]),
    37: dict(
        hl=[('CarFactory', 1, 0, 'ocr'), ('Riyadh HQ', 2, 0, 'ocr')],
        notes=['The model diagram: «interface» **CarFactory** with `makeMercedes()` and `makeBMW()`; **JeddahCarFactory** and **DammamCarFactory** implement it.',
               'Client **Riyadh HQ** uses CarFactory and the abstract products **Mercedes** and **BMW**; JeddahMercedes/DammamMercedes and JeddahBMW/DammamBMW are the concrete products, each created by its own city’s factory.']),
    38: dict(
        hl=[('create concrete classes', 1), ('decoupling', 2), ('Why this matters', 3)],
        notes=['Yes, concrete classes are still written (DarkButton, LightTextField…), and concrete factories that instantiate them. Otherwise nothing real would exist.',
               'But the **client** doesn’t care: the point of the pattern is **decoupling**. Client code works only with abstract types (`Button btn; GUIFactory factory = FactoryProvider.getFactory("dark"); btn = factory.createButton();`) and never writes `new DarkButton()`.',
               'Why it matters: a new NeonThemeFactory with NeonButton and NeonTextField needs no client change. Without the pattern you get if-else “spaghetti” creating `new DarkButton()` or `new LightButton()` all over the client.']),
    39: dict(
        hl=[('Abstract Factory', 1), ('Factory method', 2), ('Singleton', 2)],
        notes=['This lecture: design-pattern basics and the **Abstract Factory**.',
               'Next: the other creational patterns, **Factory Method**, **Builder** and **Singleton**.']),
}

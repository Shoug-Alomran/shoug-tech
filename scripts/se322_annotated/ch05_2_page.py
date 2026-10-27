"""SE322 Chapter 5, Lecture 2 (Principles of Detailed Design II): content for the hand-built annotated page.

Rendered by scripts/annotated_page.py (via the SE322 build) from the original PowerPoint (exported to
se322_annotated/source/SE322_Chapter05-L02.pdf, 39 slides, same order and wording as the .pptx).

Each slide entry:
  notes  list of numbered notes. A note is a string, or a dict with 'text' plus optional
         'code' [(source line, explanation), ...] or 'items' [(element, meaning), ...] or 'pre' (a code block).
  hl     [(phrase on the slide, note number), ...] or (phrase, note, occurrence) to pick a later match.
         Each highlight belongs to exactly one note; a phrase that can't be found stops the build.
  exam   [dict(kind='past'|'predict', ref=..., q=..., a=...)]: 'past' only for questions that really
         appeared on a paper in exams/ (Final 252 Q5); everything else is labelled a prediction.
Markup inside text: **bold**, `code`.
"""

TITLE = 'Principles of Detailed Design II: Component Design, SRP, OCP and LSP'
CHAPTER = 'SE322 · Chapter 5 · Lecture 2'
FOOTER = ('Slides: SE322 Software Design and Architecture, Prince Sultan University, prepared from “Software Engineering '
          'Design: Theory and Practice”. Notes and questions are study aids.')

# Slides whose title is part of a picture (no title text on the slide).
TITLES = {1: 'Software Design and Architecture: Principles of Detailed Design', 9: 'Further reading',
          19: 'SRP: does every function need its own class?', 20: 'SRP Applies to Responsibilities, Not Methods',
          24: 'The Open-Close Principle: the add() code', 26: 'The Open-Closed Principle (OCP): first attempt',
          27: 'The Open-Closed Principle (OCP): GameEngine with type checks', 28: 'The Open-Closed Principle (OCP): one move() for all',
          29: 'The Open-Closed Principle (OCP): the redesign', 37: 'LSP: a sanity check'}

OVERVIEW = {
    'summary': ('Architecture names the components; component design decides what goes inside them. This lecture '
                'shows how a component becomes classes and interfaces, refreshes the four object-oriented ideas '
                'you need for that (classes, abstract classes and interfaces, inheritance, polymorphism), and then '
                'covers the first three SOLID principles. Each principle is a test you can run on a class diagram.'),
    'ideas': [
        ('Component design', 'Defines the internal structure (classes, data) and behavior (algorithms, interactions) of each architectural component. In OO it is drawn as class diagrams.'),
        ('SRP: Single Responsibility', 'A class should have one reason to change, meaning one actor or policy drives its changes. It is about responsibilities, not about having one method.'),
        ('OCP: Open-Closed', 'Add new behavior by adding new classes behind a stable abstraction, not by editing working code.'),
        ('LSP: Liskov Substitution', 'A subclass must be usable anywhere its parent is expected without breaking what callers rely on.'),
    ],
    'sections': [
        ('Slides 1–6', 'Component design: from architecture components to classes and interfaces'),
        ('Slides 7–14', 'OOP refresher: abstract classes, interfaces, inheritance, polymorphism (Java and UML)'),
        ('Slides 15–21', 'SOLID intro and SRP: Person/Email, Employee, payroll exercise'),
        ('Slides 22–31', 'OCP: the game engine redesign and the salary exercise'),
        ('Slides 32–38', 'LSP: flying “terrestrial” character, square/rectangle, License, fruit exercise'),
        ('Slide 39', 'What comes next: ISP, DIP and internal behavior'),
    ],
    'exam': ('Confirmed: Final 252 Q5 (5 marks) asked you to name the SRP violation in a BookManager class and redraw it, '
             'then draw an OCP class diagram so E-books can be added (see slides 21 and 31). LSP has not appeared on a '
             'past paper here, so the LSP questions on this page are predictions.'),
}

SLIDES = {
    1: dict(
        hl=[('Principles of Detailed Design', 1)],
        notes=['This is the second lecture of Chapter 5. Lecture 1 described the detailed design process; this one is about '
               'the **principles** that make a detailed design good: easy to change, reuse and test.']),
    2: dict(
        hl=[('Structure', 1), ('(SOLID)', 2), ('Behavior', 3)],
        notes=['**Internal structure** means which classes and interfaces a component contains and how they relate. It is drawn with class diagrams.',
               'SOLID is five principles. Only the first three (S, O, L) are taught in this lecture; slide 39 moves I and D to the next one.',
               '**Internal behavior** (what the classes do at run time, drawn with sequence or state diagrams) is also left for the next lecture.']),
    3: dict(
        hl=[('detailed design', 1), ('internal logical structure', 1), ('behavior', 1),
            ('identified during the architecture activity', 2), ('one or more class diagrams', 3)],
        notes=['Component design is the part of detailed design that opens each component up. **Structure** is what it is made of (classes, attributes, interfaces); **behavior** is how those parts act to deliver the component’s services.',
               'It does not invent new top-level components. It refines the ones the architect already chose, so every class you design belongs to one architectural component.',
               'In an object-oriented system each component’s inside is usually shown with one or more class diagrams. A large component may need several.']),
    4: dict(
        hl=[('During Architecture', 1), ('During Detailed Design', 2), ('ConcreteServer', 4), ('Important:', 5)],
        notes=[{'text': 'How to read the top diagram (architecture view):', 'items': [
                    ('ClientSystem, ServerSystem', 'UML components: boxes with the small component icon. They are black boxes at this stage.'),
                    ('Ball-and-socket on ServerInterface', 'The circle (ball) is the interface ServerSystem **provides**; the half-circle (socket) is what ClientSystem **requires**. Joined, they mean the client uses that service.')]},
               {'text': 'The bottom diagram is the same two components after detailed design: they are opened up to show the classes inside.', 'items': [
                    ('Client', 'A class inside ClientSystem.'),
                    ('«interface» ServerInterface', 'The provided interface, now an actual interface type inside ServerSystem.')]},
               'The dashed arrow with an open arrowhead from Client to ServerInterface is a **dependency**: Client calls the interface and never names the concrete class.',
               'The dashed line with a hollow triangle from ConcreteServer to ServerInterface is **realization**: ConcreteServer implements the interface. Another class could replace it and Client would not change.',
               'The takeaway box says it in one line: in detailed design you stop thinking in components and start thinking in classes, interfaces and types.']),
    5: dict(
        hl=[('internal data structures', 1), ('algorithms', 1), ('interface details', 1), ('communication mechanisms', 1),
            ('functional correctness', 2), ('TaxCalculator, DiscountManager, PaymentProcessor', 3)],
        notes=['Four things are decided in component design. **Data structures** say how information is stored. **Algorithms** say how results are computed. **Interface details** are the exact method names, parameters and return types. **Communication mechanisms** say how components talk: direct calls, messages or events.',
               'That makes component design the place where functional correctness is won or lost. Architecture can be perfect, but if the algorithm or the data passed between classes is wrong, the system still gives wrong answers.',
               'In the payment example the three classes must agree on details like the order of operations (discount before tax?) and the number format. Only then is the total right for every valid input. Those agreements are exactly what component design writes down.']),
    6: dict(
        hl=[('functional success of the system', 1), ('Classes / objects', 2), ('Abstract classes and Interfaces', 2), ('Inheritance', 2), ('Polymorphism', 2)],
        notes=['Because component design fixes the actual logic, it is a major factor in whether the system does what users need.',
               {'text': 'The four object-oriented ideas a component designer must be fluent in. Slides 7–14 refresh each one:', 'items': [
                   ('Class / object', 'A class is the blueprint; an object is one instance created from it at run time.'),
                   ('Abstract class / interface', 'Types that define a contract other classes must complete or implement.'),
                   ('Inheritance', 'A subclass reuses and specializes a parent (“is-a”).'),
                   ('Polymorphism', 'One call, such as `animal.sound()`, runs different code depending on the actual object.')]}]),
    7: dict(
        hl=[('abstract keyword', 1), ('at least one abstract method', 1), ('inheriting class should implement the abstract method', 2),
            ('cannot be instantiated', 3), ('default functionality', 4), ('code reusability', 4)],
        notes=['An abstract class is declared with the `abstract` keyword. It can mix **abstract methods** (a signature with no body) and **concrete methods** (normal methods with code). The slide’s definition requires at least one abstract method. Java itself also accepts an abstract class with none, but answer with the slide’s definition in the exam.',
               'Any concrete (non-abstract) subclass must give a body to every abstract method it inherits. If it doesn’t, it must be declared abstract too.',
               '“Cannot be instantiated” means `new Animal()` is a compile error when Animal is abstract. You can still declare a variable of that type: `Animal a = new Cat();`.',
               'The four reasons all come down to sharing: common code lives once in the parent (default functionality, reuse), and the abstract methods fix a common set of operations every subclass must offer (template, common interface).',
               {'text': 'Reading the small diagram:', 'items': [
                   ('Top box «abstract»', 'The abstract class. It holds an abstract method (italic) and `+ concreteMethod()`, which has a body.'),
                   ('Arrow to ConcreteClass', 'ConcreteClass derives from it and supplies `+ abstractMethod()`. The slide draws the arrow downward; standard UML points a hollow triangle from the subclass up to the parent.')]}],
        exam=[dict(kind='predict', q='True or false: an abstract class can contain concrete methods, and it can be instantiated with `new`.',
                   a='Half true. It can contain concrete methods, but it can never be instantiated directly. Only a concrete subclass can be created.')]),
    8: dict(
        hl=[('special type of abstract classes', 1), ('All the methods of an interface', 1), ('An interface cannot be instantiated', 2),
            ('public static', 3), ('loose coupling', 4), ('dynamic method resolution at run time', 4)],
        notes=['An interface is a pure contract: it lists method signatures and no code. The slide says no concrete methods at all. Modern Java also allows `default` and `static` methods, but for this course an interface has only abstract methods.',
               'You cannot write `new AnimalInterface()`. You create an object of a class that implements it and refer to it through the interface type.',
               'Interfaces hold no instance variables (no per-object state). The only fields allowed are constants: `public static final`.',
               'Benefits: **loose coupling**, because callers depend on the contract and not on a specific class. **Dynamic method resolution**: at run time Java runs the method of the actual object behind the interface. It also lets unrelated classes share a capability outside one inheritance tree, since a Java class can implement many interfaces but extend only one class.'],
        exam=[dict(kind='predict', q='Give two differences between an abstract class and an interface (as defined in this course).',
                   a='An abstract class can have concrete methods and instance variables; an interface has only abstract methods and constants. A class extends one abstract class (`extends`) but can implement many interfaces (`implements`). In UML an abstract class is shown in italics, an interface with «interface».')]),
    9: dict(
        hl=[('interface-vs-abstract-class-java', 1), ('uml-relationships-with-example', 2)],
        notes=['Further reading on when to choose an interface or an abstract class in Java.',
               'Further reading on UML relationships. The `#4` anchor jumps to the section on generalization and realization, the two arrows used on slides 10–12.']),
    10: dict(
        hl=[('implements', 1), ('drawe', 2), ('<<interface>>', 3)],
        notes=[{'text': 'The code, line by line:', 'code': [
                    ('public interface AnimalInterface {', 'Declares a contract named AnimalInterface.'),
                    ('    public void sound();', 'A required method: signature only, ending in `;`, with no body.'),
                    ('    public void drawe ();', 'A second required method (spelled “drawe” on the slide).'),
                    ('}', 'End of the contract.'),
                    ('public class Cat implements AnimalInterface{', '`implements` promises that Cat supplies a body for every method in the interface.'),
                    ('    public void sound(){ System.out.println("Miaw"); }', 'Cat’s own version of sound(): prints Miaw.'),
                    ('    public void eat(){ System.out.println("Cat is eating fish!"); }', 'Cat’s eat() body.')]},
               '**Watch the mismatch:** the interface asks for `drawe()`, but Cat provides `eat()`. As printed, Java would reject Cat (“does not override abstract method drawe()”). The UML on the right shows what was intended: the interface has `sound()` and `eat()`.',
               {'text': 'Reading the UML:', 'items': [
                   ('«interface» Animal', 'The stereotype in guillemets marks the box as an interface.'),
                   ('Horse, Cat', 'Classes that each provide `+ sound()` and `+ eat()`.'),
                   ('Dashed lines with a hollow triangle', '**Realization**: the triangle points at the interface each class implements.')]}],
        exam=[dict(kind='predict', q='Which UML notation shows that class Cat implements interface Animal?',
                   a='A dashed line from Cat to Animal ending in a hollow triangle at Animal (realization), with Animal marked «interface».')]),
    11: dict(
        hl=[('extends', 1), ('Abstract class is italic in UML', 2), ('Realization Relationship', 3)],
        notes=[{'text': 'The code, line by line:', 'code': [
                    ('public abstract class Animal {', 'An abstract class: it can’t be instantiated.'),
                    ('    public abstract void sound();', 'Abstract method: no body, and every concrete subclass must implement it.'),
                    ('    public void eat() { System.out.println("Animal is eating.."); }', 'Concrete method: inherited as-is unless a subclass overrides it.'),
                    ('public class Cat extends Animal {', '`extends` = inherits from Animal (a Java class can extend only one class).'),
                    ('    public void sound(){ System.out.println("Miaw"); }', 'Required: fills in the abstract sound().'),
                    ('    public void eat(){ System.out.println("Cat is eating fish!"); }', 'Optional: overrides the inherited eat() with Cat’s version.')]},
               'In UML, italics carry meaning: the class name *Animal* in italics means abstract class, and *sound()* in italics means abstract operation. `eat()` is upright because it has a body.',
               '**Notation trap:** the slide calls the dashed arrows “Realization”. Standard UML uses realization (dashed line, hollow triangle) for implementing an **interface**, and generalization (solid line, hollow triangle) for **extending a class**, abstract or not. In an exam, draw `extends` with a solid line and say why.'],
        exam=[dict(kind='predict', q='A class Dog extends an abstract class Animal. Which UML line connects them, and how is Animal’s name written?',
                   a='A solid line with a hollow triangle pointing at Animal (generalization), and Animal’s name in italics because it is abstract.')]),
    12: dict(
        hl=[('Generalization', 3)],
        notes=[{'text': 'Here Animal is an ordinary (concrete) class, so every method already has a body:', 'code': [
                    ('public class Animal {', 'A normal class: it can be instantiated.'),
                    ('    public void sound(){ ..."Animal is making a sound"... }', 'Default sound().'),
                    ('    public void eat(){ ..."Animal is eating.."... }', 'Default eat().'),
                    ('public class Horse extends Animal{', 'Horse is-a Animal.'),
                    ('    @Override public void sound(){ ..."Neigh"... }', '`@Override` asks the compiler to check that a matching parent method exists, which catches typos.'),
                    ('    @Override public void eat(){ ..."Horse is eating hay!"... }', 'Horse’s own eat().'),
                    ('public class Cat extends Animal{ ...sound "Miaw", eat "Cat is eating fish!" }', 'Cat overrides both methods the same way.')]},
               'Unlike slide 11, nothing forces the subclasses to override: they could inherit Animal’s versions unchanged. Overriding is a choice here, not a requirement.',
               'The UML shows **generalization**: solid lines meeting at one hollow triangle that points at the parent, Animal. Read it as “Horse is an Animal” and “Cat is an Animal”.']),
    13: dict(
        hl=[('Animal is making a sound', 1), ('Neigh', 1), ('Miaw', 1)],
        notes=[{'text': 'The demo creates one object of each class and calls both methods:', 'code': [
                    ('Animal a = new Animal(); a.sound(); a.eat();', 'Prints “Animal is making a sound” then “Animal is eating..”.'),
                    ('Horse h = new Horse(); h.sound(); h.eat();', 'Prints “Neigh” then “Horse is eating hay!”.'),
                    ('Cat c = new Cat(); c.sound(); c.eat();', 'Prints “Miaw” then “Cat is eating fish!”.')]},
               'The output panel on the right confirms each object runs the version defined in its own class. Every variable here has the same type as its object, so this is plain inheritance. Slide 14 shows what changes when the types differ.']),
    14: dict(
        hl=[('new Horse', 1), ('new Cat', 1), ('Neigh', 2), ('Miaw', 2)],
        notes=[{'text': 'The variables are declared as Animal but hold a Horse and a Cat:', 'code': [
                    ('Animal ah = new Horse();', 'Declared type Animal, actual object Horse. This is allowed because a Horse is an Animal.'),
                    ('ah.sound(); ah.eat();', 'Prints “Neigh” and “Horse is eating hay!”: the HORSE’s versions, not Animal’s.'),
                    ('Animal ac = new Cat();', 'Same idea with a Cat.'),
                    ('ac.sound(); ac.eat();', 'Prints “Miaw” and “Cat is eating fish!”.')]},
               'This is **polymorphism (dynamic binding)**. The declared type (Animal) decides which methods you are allowed to call; the actual object (Horse or Cat) decides which code runs. The choice happens at run time.',
               'Why it matters for this lecture: OCP (slides 22–31) works because a GameEngine holding a `Character` reference can call `move()` and get each character’s own movement without knowing its class.'],
        exam=[dict(kind='predict', q='`Animal x = new Cat(); x.sound();` What is printed, and what is this mechanism called?',
                   a='“Miaw”. It is polymorphism (dynamic binding): the overriding method of the actual object runs, even though the variable’s type is Animal.')]),
    15: dict(
        hl=[('less complex', 1), ('reusable', 1), ('easier to modify', 1), ('easier to maintain', 1), ('(SOLID):', 2)],
        notes=['The goal of every principle that follows: designs that are less complex, reusable, easier to modify and easier to maintain.',
               'SOLID is the acronym for the five principles: **S**ingle Responsibility, **O**pen-Closed, **L**iskov Substitution, **I**nterface Segregation, **D**ependency Inversion. S, O and L are covered in this lecture.']),
    16: dict(
        hl=[('least well understood principle', 1), ('every module should do just one thing', 1),
            ('responsible to one, and only one, user or stakeholder', 2), ('only one reason to change', 2)],
        notes=['The common misreading: “every module should do just one thing.” That is good advice for small functions, but it is **not** what SRP says.',
               'SRP is about who causes change. A module should answer to **one** actor (a user group, stakeholder or policy). Equivalently, a class has one reason to change. If the accountants and the IT team could each force edits to the same class, it has two responsibilities.'],
        exam=[dict(kind='predict', q='State the Single Responsibility Principle and explain what “reason to change” means.',
                   a='A class should have only one reason to change, i.e. it should be responsible to one actor or stakeholder. A reason to change is a source of change requests: a policy, user group or concern (data format, tax rules, report layout). Two independent sources mean two responsibilities that should be separated.')]),
    17: dict(
        hl=[('should not include email validation', 1)],
        notes=[{'text': 'The code (TypeScript-style), line by line:', 'code': [
                    ('class Person {', 'Represents a person.'),
                    ('    public name : string; public surname : string; public email : string;', 'Person data: three text fields.'),
                    ('    constructor(name, surname, email){', 'Runs when a Person is created.'),
                    ('        this.surname = surname; this.name = name;', 'Stores the names.'),
                    ('        if(this.validateEmail(email)) { this.email = email; }', 'Checks the address format before storing it.'),
                    ('        else { throw new Error("Invalid email!"); }', 'Rejects a bad address by throwing an error.'),
                    ('    validateEmail(email : string) {', 'Email-format rule, living inside Person (the boxed part on the slide).'),
                    ('        var re = /^([\\w-]+(?:\\.[\\w-]+)*)@(...)/;', 'A regular expression describing a valid address.'),
                    ('        return re.test(email); }', 'True if the address matches the pattern.'),
                    ('    greet() { alert("Hi!"); }', 'Genuine person behavior.')]},
               'The boxed lines show the violation: Person now has two reasons to change. Its fields change when what a person is changes; `validateEmail` changes when the email rules change (new domains, longer TLDs). You also can’t test the email rule without building a Person.']),
    18: dict(
        hl=[('removing the responsibility of', 1), ('email validation', 1), ('single responsibility', 2), ('(for a single', 2)],
        notes=[{'text': 'The refactoring moves validation into its own class:', 'code': [
                    ('class Email {', 'New class that owns everything about an email address.'),
                    ('    constructor(email){ if(this.validateEmail(email)) {...} else { throw ... } }', 'An Email object can only exist if the address is valid.'),
                    ('    validateEmail(email){ ... return re.test(email); }', 'The same rule, now in its only home.'),
                    ('class Person {', 'Back to pure person data and behavior.'),
                    ('    public email : Email;', 'The field’s type is now Email, not string.'),
                    ('    constructor(name, surname, email : Email){ this.email = email; ... }', 'Person receives an already-validated Email, so no check is needed.'),
                    ('    greet() { alert("Hi!"); }', 'Unchanged.')]},
               'Each class now has one reason to change: email-rule changes touch only Email, and person changes touch only Person. A class with one responsibility (one actor) is also easier to read, test and extend.']),
    19: dict(
        hl=[('Stores employee data,', 1), ('(Three reasons!)', 1), ('Only stores employee data', 2), ('does it sound like now for every function', 3)],
        notes=['The violating Employee class stores data, calculates taxes and prints pay stubs. Three different things can force edits: the data structure, the tax laws and the print format.',
               'The SRP version keeps only the employee data in Employee. Tax calculation and pay-stub printing move to their own classes, so Employee changes only when the data changes.',
               'The slide’s question has a clear answer, given on slide 20: **no**. SRP does not mean one class per function.']),
    20: dict(
        hl=[('Responsibilities', 1), ('Not Methods', 1), ('Bad Example (Violation):', 2), ('Good Example (Following SRP):', 3), ('new, distinct reason for change', 4)],
        notes=['A responsibility is usually carried out by **several** related methods working together. SRP limits the number of responsibilities, not the number of methods.',
               'ReportGenerator mixes three responsibilities: calculation (`calculateTax`), formatting (`printToPDF`) and communication (`sendEmail`). Each changes for a different reason.',
               'TaxCalculator has three methods but one responsibility, tax calculation. The table adds two more good examples: UserAuthentication (login state, four methods) and ProductValidator (product data correctness, three methods).',
               'The test for splitting: if you change method A, would you also have to change method B? If yes, they belong together (both tax methods change with tax law). If no, they belong in separate classes (`calculateTax` and `printToPDF`).']),
    21: dict(
        hl=[('Employee Payroll System', 1), ('calculate the salary', 1), ('save the employee\'s data', 1), ('generate a report', 1),
            ('Draw a class diagram that violates SRP.', 2), ('Redraw to achieve SRP.', 3)],
        notes=['Three requirements means three potential reasons to change: pay rules, storage technology and report format.',
               {'text': 'Question 1, a design that violates SRP (one class does everything):', 'pre':
                   'Employee\n  - id, name, baseSalary\n  + calculateSalary(): double\n  + saveToDatabase(): void\n  + generateReport(): String'},
               {'text': 'Question 2, the SRP redesign. Employee keeps the data; each job gets its own class, and each one depends on (uses) Employee:', 'pre':
                   'Employee\n  - id, name, baseSalary          (data only)\n\nSalaryCalculator\n  + calculateSalary(e: Employee): double\nEmployeeRepository\n  + save(e: Employee): void\nEmployeeReportGenerator\n  + generate(e: Employee): String\n\nall three  - - ->  Employee    (dependency)'}],
        exam=[dict(kind='past', ref='Final 252 · Q5-1 · 2.5 marks',
                   q='NextGen Library: a junior developer put fee calculation, book data and report formatting into one BookManager class. Which detailed-design principle is violated? Draw a class diagram that fixes it.',
                   a='The Single Responsibility Principle: BookManager has three reasons to change (book data, loan and fee rules, report format). Fix: Book (title, ISBN, author), LoanCalculator (due date and late fee) and MonthlyReportGenerator (text report), each with one responsibility; LoanCalculator and the report class use Book.')]),
    22: dict(
        hl=[('reusable', 1), ('modifiable', 1), ('open to extension but', 2), ('closed for modification.', 2), ('untouched', 2),
            ('modifications should be done by adding new code', 3), ('does not require old', 3)],
        notes=['OCP is what lets a system keep growing for years without every new feature breaking old ones.',
               '“Open to extension” means you can add new behavior. “Closed for modification” means code that already works and is tested stays as it is.',
               'There is no contradiction: the system still changes, but by **adding** classes (a new subclass, a new implementation) that plug into existing abstractions. No working code has to be edited for that.'],
        exam=[dict(kind='predict', q='Explain how a design can be both “open for extension” and “closed for modification”.',
                   a='New behavior is added as new code (new classes implementing an existing interface or extending an abstract class) that the system uses through that abstraction, so existing, tested classes are never edited.')]),
    23: dict(
        hl=[('several types of', 1), ('new characters will be added', 1), ('This design violates the OCP principle', 3)],
        notes=['The scenario matters: several kinds of characters exist, and **more will be added**. A change is expected, so the design must be ready for it.',
               {'text': 'Reading the diagram:', 'items': [
                   ('GameEngine', 'Has one operation, `add(pCharacter: TerrestrialCharacter*)`. The `*` is a C++ pointer.'),
                   ('Dashed arrow', 'A dependency: GameEngine uses TerrestrialCharacter directly.'),
                   ('TerrestrialCharacter', 'A concrete class with `draw()` and `run()`.')]},
               'Why it violates OCP: GameEngine names a **concrete** class. Every new kind of character (one that flies, one that swims) forces a change to GameEngine, the code that already works.']),
    24: dict(
        hl=[('What can you tell me about', 2), ('AerialCharacter that can fly?', 3)],
        notes=[{'text': 'The C++ code, line by line:', 'code': [
                    ('class TerrestrialCharacter {', 'A character that moves over land.'),
                    ('  virtual void draw() { ... }', '`virtual` = subclasses may override it, and the call is resolved at run time.'),
                    ('  virtual void run() { ... }', 'Land movement.'),
                    ('class GameEngine {', 'Manages the game.'),
                    ('  void add(TerrestrialCharacter* pCharacter) {', 'Accepts only terrestrial characters.'),
                    ('    pCharacter->draw();', '`->` calls a method through a pointer: show the character.'),
                    ('    pCharacter->run();', 'Make it move by running.')]},
               '`add(...)` is hard-wired to one concrete type and one way of moving (`run`).',
               'An AerialCharacter that flies doesn’t fit: it isn’t a TerrestrialCharacter and has no `run()`. Supporting it means editing `add(...)`, which is working code. That edit is the OCP violation.']),
    25: dict(
        hl=[('Do you have suggestions to fix it', 1)],
        notes=['The fix students should propose: introduce an abstraction (an interface or abstract class) named **Character** with the operations every character has, and make GameEngine depend on Character instead of on a concrete class. Slides 26–29 show how a first attempt still goes wrong, and then the correct version.']),
    26: dict(
        hl=[('Inherits from Character', 1), ('Inherits from Character', 1, 1), ('getType(...) function should', 3)],
        notes=[{'text': 'Joe’s first attempt (C++):', 'code': [
                    ('class Character { virtual string getType() = 0; virtual void draw() = 0; };', '`= 0` makes a method **pure virtual** (abstract). A class with only pure virtual methods acts as an interface.'),
                    ('class AerialCharacter : public Character {', '`: public Character` = inherits from (realizes) Character.'),
                    ('  getType() { return "aerial"; }  draw() {...}  fly() {...}', 'Reports its type, draws itself, and has its own `fly()`.'),
                    ('class TerrestrialCharacter : public Character {', 'Same shape:'),
                    ('  getType() { return "terrestrial"; }  draw() {...}  run() {...}', 'its own `run()`.')]},
               'Joe abstracted the drawing, but movement was left to each subtype under **different names** (`fly`, `run`). Character itself has no movement operation.',
               'The `getType()` method is the warning sign: a caller that has to ask “what type are you?” is about to branch on the answer. Slide 27 shows that branch.']),
    27: dict(
        hl=[('Encapsulate Variation', 2), ('always vary', 1), ('Aquatic Character', 3)],
        notes=[{'text': 'GameEngine.add with Joe’s design:', 'code': [
                    ('void add( Character* pCharacter ) {', 'Now takes any Character, which is better.'),
                    ('  pCharacter->draw();', 'Drawing works for every character.'),
                    ('  if( pCharacter->getType().compare("aerial") == 0 ) {', 'Asks for the type string.'),
                    ('    AerialCharacter* pAerial = dynamic_cast<AerialCharacter*>(pCharacter);', '`dynamic_cast` = a checked downcast to the concrete type.'),
                    ('    pAerial->fly(); }', 'Only then can it call fly().'),
                    ('  else { TerrestrialCharacter* pTerrestrial = dynamic_cast<...>(pCharacter);', 'Otherwise assume terrestrial…'),
                    ('    pTerrestrial->run(); }', '…and run.'),
                    ('test driver: TerrestrialCharacter madRabbit; AerialCharacter killerBee; engine.add(&madRabbit); engine.add(&killerBee);', 'Prints: drawing terrestrial / running / drawing aerial / flying.')]},
               '**Encapsulate variation:** the part that changes (how each character moves) should be hidden behind one stable operation. Here it leaks into GameEngine as an if/else that “will always vary” with the set of characters.',
               'It runs correctly, but it still violates OCP: adding an AquaticCharacter means editing `add()` again with another branch and another cast.']),
    28: dict(
        hl=[('Encapsulate the movement behavior', 1), ('must provide the implementation', 2)],
        notes=['The fix: put one movement operation, `move()`, into Character itself (`virtual void move() = 0`). “How it moves” becomes each subtype’s private business.',
               {'text': 'Each subtype implements the full contract:', 'items': [
                   ('AerialCharacter', '`draw()` draws it, `move()` makes it fly.'),
                   ('TerrestialCharacter (sic)', '`draw()` draws it, `move()` makes it run.')]}]),
    29: dict(
        hl=[('New redesign! Adheres to OCP!', 1), ('Old design! Violates OCP!', 1), ('New Aquatic Character added by', 2),
            ('pCharacter->move();', 3)],
        notes=[{'text': 'Reading the new diagram (left) against the old one (right):', 'items': [
                   ('GameEngine - - -> «interface» Character', 'GameEngine depends only on the interface. The italic `+draw()` and `+move()` are abstract operations.'),
                   ('Aerial / Terrestrial / AquaticCharacter', 'Each realizes Character (dashed line, hollow triangle) and implements both operations.'),
                   ('Old design', 'GameEngine depended on the concrete TerrestrialCharacter.')]},
               'AquaticCharacter is added by **writing one new class**. GameEngine, Character and the existing characters are not touched. That is OCP.',
               {'text': '`add()` now just calls `draw()` and `move()`; polymorphism (slide 14) runs the right movement. The same design in Java:', 'pre':
                   'interface Character {\n    void draw();\n    void move();\n}\nclass AquaticCharacter implements Character {\n    public void draw() { /* draw a fish */ }\n    public void move() { /* swim */ }\n}\nclass GameEngine {          // never changes\n    void add(Character c) {\n        c.draw();\n        c.move();\n    }\n}'}]),
    30: dict(
        hl=[('No design will be 100% closed for modification.', 1), ('likely to vary', 2), ('polymorphism', 2)],
        notes=['OCP is a direction, not an absolute. Something always has to be edited: a factory, a configuration or a list of characters.',
               'The skill is to predict **where** change is likely (new character types, new salary types, new payment methods), hide that variation behind an abstraction, and let polymorphism pick the implementation.']),
    31: dict(
        hl=[('open for extension but closed for modification', 1), ('Hourly', 2), ('weekly', 2), ('apply OCP', 2)],
        notes=['The same rule restated for any software entity: a class, module or function.',
               {'text': 'Model answer: make the varying part (how a salary is computed) an interface, so a new salary type is a new class.', 'pre':
                   '«interface» SalaryPolicy\n  + calculate(e: Employee): double\n\nMonthlySalary, HourlySalary, WeeklySalary\n  - - -|>  SalaryPolicy        (realization)\n\nSalaryCalculator               (never edited)\n  + calculateSalary(e: Employee,\n                    p: SalaryPolicy): double\n\nNew CommissionSalary = one new class\nthat implements SalaryPolicy.'}],
        exam=[dict(kind='past', ref='Final 252 · Q5-2 · 2.5 marks',
                   q='NextGen Library (physical books now, E-books soon): by applying the Open/Closed Principle for E-books, draw the class diagram.',
                   a='Introduce an abstract class or interface (e.g. LibraryItem with title, ISBN, author and an abstract operation such as calculateLateFee()). PhysicalBook and EBook extend or implement it. The loan and report classes depend only on LibraryItem, so adding EBook (or audiobooks later) needs no change to existing classes.')]),
    32: dict(
        hl=[('implied contract', 1), ('replaceable with instances of', 2), ('"Treat Alike" Rule', 2), ('Signatures', 3), ('Subtype specification', 3)],
        notes=['The “implied contract” is everything callers rely on: the method names and types, but also the **behavior** (what the method promises to do and what it requires before it is called).',
               'If code works with a parent object, it must keep working when you hand it a child object instead. The slide calls this the “treat alike” rule.',
               'Two requirements: the method signatures stay compatible, and anything you could conclude from the parent’s specification must still hold for the subtype.'],
        exam=[dict(kind='predict', q='State the Liskov Substitution Principle in one sentence.',
                   a='Objects of a superclass must be replaceable by objects of any subclass without altering the correctness of the program: subtypes must honor the base type’s contract.')]),
    33: dict(
        hl=[('The Signature Rule:', 1), ('The Methods Rule:', 2), ('without anything breaking', 3)],
        notes=['**Signature rule:** if a program type-checks against the parent’s methods, it type-checks with the child too (same methods with compatible parameters and return types). The compiler mostly enforces this.',
               '**Methods rule:** reasoning about a call stays valid even though the child’s code runs. If `move()` promises “moves over land”, every override must still move over land. The compiler can’t check this, so the designer must.',
               'The plain-language version: a child class must work anywhere the parent works, without anything breaking.'],
        exam=[dict(kind='predict', q='Which LSP rule does the compiler NOT check for you, and why?',
                   a='The methods rule (behavior). It concerns what methods do: pre- and postconditions and side effects. Types alone can’t express that, so a subclass can compile and still break callers.')]),
    34: dict(
        hl=[('Does this example apply', 1), ('the character fly!', 2), ('the character fly.', 2, 1), ('adhering to the OCP', 3)],
        notes=[{'text': 'The code and its contract:', 'code': [
                    ('class TerrestrialCharacter : public Character {', 'The parent.'),
                    ('  // Pre-Condition: Character is drawn on screen.', 'What must be true before calling `move()`.'),
                    ('  // Post-Condition: Character roams around randomly over land...', 'What `move()` promises: it stays on land, walking or running.'),
                    ('  virtual void move() { //code to make the character walk or run }', 'Honors the promise.'),
                    ('class EntryLevelTerrestrialCharacter : public TerrestrialCharacter {', 'A “kind of” terrestrial character.'),
                    ('  virtual void move() { // code to make the character fly. }', 'Overrides move() to FLY.')]},
               '**Answer: no, it violates LSP.** It compiles (signature rule OK) but breaks the postcondition “roams over land”. Code that relies on terrestrial characters staying on the ground, such as collision with water or bridges, misbehaves when given this subclass.',
               'The lesson in red: OCP alone isn’t enough. The class was added by extension (OCP satisfied), yet the design is wrong because the subtype isn’t substitutable. A similar trap is a subclass whose `move()` throws an exception (“Ghosts don’t move!”): that also breaks the contract.'],
        exam=[dict(kind='predict', q='A subclass compiles and overrides every method, but one override throws UnsupportedOperationException. Does it satisfy LSP?',
                   a='No. It satisfies the signature rule but violates the methods rule: callers of the base type expect the operation to work. The subclass can’t replace its parent without breaking the program.')]),
    35: dict(
        hl=[('square/rectangle problem', 1), ('independently mutable', 2), ('must', 3), ('confused', 4)],
        notes=['The classic LSP violation. Mathematically every square is a rectangle, but in software Square should not inherit from Rectangle.',
               'Rectangle’s implied contract: `setH` and `setW` change only their own dimension. A user that sets width 5 and height 2 expects an area of 10.',
               'A Square has to keep its sides equal, so its setters change both. After `setW(5); setH(2)` the area is 4, not 10.',
               {'text': 'Diagram and fix:', 'items': [
                   ('User → Rectangle', 'Solid arrow: User is associated with and uses Rectangle (`+setH`, `+setW`).'),
                   ('Square → Rectangle (hollow triangle)', 'Generalization: Square inherits from Rectangle and adds `+setSide`.'),
                   ('Fix', 'Don’t inherit. Make Square and Rectangle siblings under a Shape abstraction that offers only what both can honor, e.g. `area()`.')]}],
        exam=[dict(kind='predict', q='Why does Square extends Rectangle violate LSP? Use a short example.',
                   a='Rectangle lets width and height change independently. Code like `r.setW(5); r.setH(2); assert r.area()==10` works for a Rectangle, but a Square forces both sides equal, so the area is 4 and the assertion fails. A Square can’t substitute for a Rectangle.')]),
    36: dict(
        hl=[('calcFee()', 1), ('different algorithms', 2), ('conforms to the LSP', 3), ('substitutable', 3)],
        notes=[{'text': 'Reading the diagram:', 'items': [
                   ('Billing → License', 'Billing uses License and calls `calcFee()`.'),
                   ('<I> License', 'An interface with one operation, `+ calcFee()`.'),
                   ('PersonalLicense, BusinessLicense', 'Implement License. BusinessLicense also keeps `- users` (a private field) because its fee depends on the number of users.')]},
               'Each subtype computes the fee differently (a flat personal fee; a fee per business user), but both honor the contract “return this license’s fee”.',
               {'text': 'Billing’s behavior never depends on which subtype it receives, so both are substitutable: LSP holds. It is also OCP-compliant, because a new license type is a new class. In Java:', 'pre':
                   'interface License { double calcFee(); }\n\nclass PersonalLicense implements License {\n    public double calcFee() { return 100.0; }\n}\nclass BusinessLicense implements License {\n    private int users;\n    public double calcFee() {\n        return users * 50.0;\n    }\n}\nclass Billing {\n    void printBill(License l) {\n        System.out.println(l.calcFee());\n    }\n}'}]),
    37: dict(
        hl=[('important sanity check', 1), ('expected behavior', 2)],
        notes=['Use LSP to sanity-check every inheritance arrow you draw: ask whether the child can stand in for the parent everywhere.',
               'Inheritance is about keeping **expected behavior**, not just reusing code. If the honest answer is “only sometimes”, use composition or a different abstraction instead.']),
    38: dict(
        hl=[('Base Class (Parent):', 1), ('Derived Class (Child 1):', 2), ('Derived Class (Child 2):', 3)],
        notes=['Fruit promises two operations every fruit can do: `Peel()` and `MakeSmoothie()`.',
               'Orange: peeling and blending both work exactly as Fruit promises. **LSP holds.**',
               {'text': 'Coconut: you don’t peel a coconut like other fruit; you crack it open. If `Coconut.Peel()` throws an error or does something callers don’t expect, a program that peels any Fruit breaks. **LSP is violated.** Model drawing and fix:', 'pre':
                   'Violation\n  Fruit  (+Peel(), +MakeSmoothie())\n    ^ Orange    both work\n    ^ Coconut   Peel() fails\n\nFix\n  «interface» Peelable   (+Peel())\n  «interface» Blendable  (+MakeSmoothie())\n  Orange  implements Peelable, Blendable\n  Coconut implements Blendable\n          and adds its own +Crack()'}],
        exam=[dict(kind='predict', q='Does Coconut violate LSP if Fruit declares Peel()? How would you fix the design?',
                   a='Yes, if Coconut can’t honor Peel() (it throws or behaves differently), code written for Fruit breaks. Fix: don’t promise Peel() for every fruit. Split the capabilities into separate interfaces (Peelable, Blendable) and have each fruit implement only what it can do. This also previews the Interface Segregation Principle.')]),
    39: dict(
        hl=[('(Next lecture)', 1, 0), ('(next lecture)', 1, 1), ('(next lecture)', 2, 2)],
        notes=['Covered so far: component design, the OO refresher, and S, O and L. The **Interface Segregation** and **Dependency Inversion** principles come in the next lecture.',
               'Also next lecture: designing the **internal behavior** of components.']),
}

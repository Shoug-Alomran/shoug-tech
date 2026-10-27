"""SE322 Chapter 5, Lecture 3 (Principles of Detailed Design III: ISP, DIP, internal behaviour, rules of design).

Schema: see annotated_page.py. Code on slides 7, 8 and 11–14 is a picture, so its marks use 'ocr' (skipped if
OCR can't read them) and the notes walk through the code line by line. Past-exam questions are copied from the
papers in exams/; everything else is a prediction (ISP and DIP have not appeared on a past paper yet).
"""
from .common import likely

TITLE = 'Principles of Detailed Design III: ISP, DIP, Internal Behaviour and Rules of Design'
CHAPTER = 'SE322 · Chapter 5 · Lecture 3'

OVERVIEW = {
    'summary': ('This lecture finishes SOLID. The Interface Segregation Principle says no class should be forced to '
                'depend on methods it does not use, so one bloated interface is split into small, role-specific ones. '
                'The Dependency Inversion Principle says high-level modules and low-level details should both depend on '
                'abstractions, so a Manager talks to an IWorker interface instead of a concrete Worker. It then shows how '
                'a component’s internal behaviour is modelled (sequence diagrams, next to class diagrams for structure), '
                'and closes with sixteen rules of design and four common design mistakes.'),
    'ideas': [
        ('ISP', 'Many client-specific interfaces are better than one general-purpose interface. Classes shouldn’t implement methods they can’t honour.'),
        ('DIP', 'Depend on abstractions, not concretions: high-level policy and low-level detail both point at an interface.'),
        ('Structure vs. behaviour', 'A component’s internal structure is a class diagram; its internal behaviour is a sequence diagram.'),
        ('Rules of design', 'What before how, external before internal, keep it simple, depend on abstractions, dependencies toward stability.'),
    ],
    'sections': [
        ('Slides 2–8', 'Interface Segregation Principle: the enemy-character game and the Worker example'),
        ('Slides 9–14', 'Dependency Inversion Principle: charger, switch and Manager examples'),
        ('Slide 15', 'Modelling the internal behaviour of a component'),
        ('Slides 16–23', 'Rules of design and common design mistakes'),
        ('Slide 24', 'From analysis models to design models'),
    ],
    'exam': ('SRP and OCP from Lecture 2 have appeared on Final 252; ISP and DIP have not yet, so the questions here are '
             'predictions. Expect “which principle is violated?” scenarios: a class forced to implement a method it can’t '
             'support (ISP), or a high-level class that holds a concrete low-level class (DIP).'),
}

TITLES = {4: 'ISP: one general interface vs. many specific ones', 5: 'Extra: ISP and LSP explained', 6: 'ISP: the segregated design',
          7: 'ISP: the segregated design in Java', 8: 'ISP: Worker violation vs. applied', 11: 'Extra: DIP – charger and switch (bad)',
          12: 'Extra: DIP – switch with an interface (good)', 23: 'Extra: The rules of design in one list', 24: 'Analysis Models to Design Models'}

SLIDES = {
    1: dict(
        hl=[('[Principles of Detailed Design]', 1)],
        notes=['Third detailed-design lecture: the last two SOLID principles (I and D), then how to model a component’s behaviour and general rules of good design.']),
    2: dict(
        hl=[('Single Responsibility Principle', 1), ('Interface-Segregation Principle', 2), ('Dependency-Inversion Principle', 2), ('Rules of Design', 3)],
        notes=['Already covered in Lecture 2: **S**RP, **O**CP and **L**SP.',
               'This lecture: the **I**nterface Segregation Principle and the **D**ependency Inversion Principle, completing SOLID.',
               'Then designing internal behaviour and the rules of design.']),
    3: dict(
        hl=[('one (and only one)', 1), ('more information than they should', 2), ('forced to depend on', 3), ('roam over land', 4), ('Bloated interface!', 5, 0, 'ocr')],
        notes=['The starting point is SRP: a well-designed class has one reason to change.',
               'When that is violated, the **interfaces** the class offers usually provide more than they should, which makes designs harder to maintain and reuse.',
               'The **Interface Segregation Principle (ISP)**: classes (or methods) should not be **forced to depend on methods they do not use**.',
               'The example: a game with enemy characters that roam over land, fly or swim, plus a super enemy that can do all three.',
               'The tempting design: one `EnemyCharacter` with `fly()`, `run()` and `swim()`, inherited by Aerial, Terrestrial, Aquatic and SuperCharacter. The slide labels it a **bloated interface**.'],
        exam=[likely('“Clients should not be forced to depend on methods they do not use” states the:', a=0,
                     opts=['Interface Segregation Principle', 'Dependency Inversion Principle', 'Open-Closed Principle', 'Liskov Substitution Principle'])]),
    4: dict(
        hl=[('many client-specific interfaces', 1), ('These classes are polluted', 2), ('violates the LSP', 3), ('Only the SuperCharacter conforms', 4)],
        notes=['The rule of thumb: **many client-specific interfaces are better than one general-purpose interface**.',
               'Aerial, Terrestrial and Aquatic characters are **polluted** with methods they can’t perform: an aerial character inherits `run()` and `swim()`, a terrestrial one `fly()`.',
               'The design also **violates LSP** (Lecture 2): code holding an `EnemyCharacter` may call `fly()`, but a TerrestrialCharacter put in its place can’t fly, so it can’t safely substitute for its parent.',
               'Only **SuperCharacter** conforms to the base type syntactically and semantically. It is the only class that really needs (and honours) all three methods, so it is the only one that satisfies LSP.'],
        exam=[likely('In the enemy-character design where every character extends EnemyCharacter with fly(), run() and swim(), which principles are violated and why?',
                     a='ISP: Aerial, Terrestrial and Aquatic characters are forced to depend on methods they don’t use. LSP: a TerrestrialCharacter cannot replace an EnemyCharacter where code expects fly(), so subclasses don’t behave like their parent. Only SuperCharacter conforms.')]),
    5: dict(
        hl=[('ISP (Interface Segregation Principle)', 1), ('(Liskov Substitution Principle)', 2), ('In short:', 3)],
        notes=['**ISP**: use small, specific interfaces instead of one big interface full of unused methods. Problem here: AerialCharacter and AquaticCharacter are forced to implement `run()`; the interface is polluted.',
               '**LSP**: a subclass must replace its parent without breaking correctness. Problem here: a TerrestrialCharacter can’t replace an EnemyCharacter when the code expects `fly()`.',
               'In short: ISP → interfaces should be specific; LSP → subclasses must behave consistently with their base class. Fixing the interfaces (next slide) fixes both.']),
    6: dict(
        hl=[('AerialCharacter', 1, 0, 'ocr'), ('SuperCharacter', 2, 0, 'ocr'), ('Extra:', 3)],
        notes=['The ISP fix: three small interfaces, «interface» **AerialCharacter** (`fly()`), **TerrestrialCharacter** (`run()`) and **AquaticCharacter** (`swim()`). Each client class (dashed realization arrows) implements only the one it can honour.',
               '«interface» **SuperCharacter** declares all three operations and is implemented by SuperCharacterClient. In the slide’s version the three small interfaces extend SuperCharacter (hollow triangles pointing down to it); conceptually it is the combination of the three capabilities.',
               {'text': 'The Extra box: Java rules about overriding when types are combined:', 'items': [
                   ('Abstract class implements an interface', 'No override needed: it can leave the methods abstract.'),
                   ('Abstract class extended by a concrete class', 'Yes: the concrete subclass must override every abstract method.'),
                   ('Normal class implements an interface', 'It must override all the interface’s abstract methods.'),
                   ('Interface extends interface', 'No override: interfaces only add declarations.')]}]),
    7: dict(
        hl=[('SuperCharacter', 1, 0, 'ocr'), ('AerialCharacterClient', 2, 0, 'ocr')],
        notes=[{'text': 'The code, top to bottom:', 'code': [
                    ('interface SuperCharacter { void fly(); void run(); void swim(); }', 'The full contract: all three capabilities.'),
                    ('interface AerialCharacter extends SuperCharacter { void fly(); }', 'A specialised interface that names the capability its clients use. (Because it *extends* SuperCharacter, a class implementing it must still provide all three methods; to apply ISP strictly, the small interfaces should not extend the big one.)'),
                    ('interface TerrestrialCharacter extends SuperCharacter { void run(); }', 'The same for running.'),
                    ('interface AquaticCharacter extends SuperCharacter { void swim(); }', 'The same for swimming.'),
                    ('class SuperCharacterClient implements SuperCharacter { fly(){…} run(){…} swim(){…} }', 'The only class that really supports all three; each prints what it is doing.'),
                    ('class AerialCharacterClient implements AerialCharacter { public void fly(){ … "is flying" } }', 'Implements only `fly()`. As printed it would not compile, because the inherited `run()` and `swim()` are missing; with stand-alone small interfaces it would.'),
                    ('class TerrestrialCharacterClient implements TerrestrialCharacter { run() }', 'Runs only.'),
                    ('class AquaticCharacterClient implements AquaticCharacter { swim() }', 'Swims only.'),
                    ('AerialCharacterClient arialObject = new AerialCharacterClient(); arialObject.fly();', 'In `main`, each object is used through the capability it supports.'),
                    ('SuperCharacterClient superCharacter = new SuperCharacterClient(); superCharacter.fly(); …swim(); …run();', 'The super character can be asked for all three.')]},
               'The intent: a reference of a narrow type can only request what that character can do, so unsupported calls become impossible. Exam answers should draw the small interfaces as independent, each implemented by the classes that need it.']),
    8: dict(
        hl=[('ISP Violation (bad)', 1, 0, 'ocr'), ('ISP Applied (good)', 2, 0, 'ocr')],
        notes=[{'text': '**Violation**: one `Worker` interface with `work()` and `eat()`.', 'code': [
                    ('interface Worker { void work(); void eat(); }', 'One fat interface for two unrelated capabilities.'),
                    ('class Robot implements Worker {', 'A robot can work but cannot eat…'),
                    ('    public void work() { System.out.println("Robot working"); }', '…so `work()` is meaningful,'),
                    ('    public void eat() { }  // Robot does not eat', 'but `eat()` is forced on it and left empty: a lie in the type.')]},
               {'text': '**Applied**: split the interface by capability.', 'code': [
                    ('interface Workable { void work(); }', 'The working capability.'),
                    ('interface Eatable { void eat(); }', 'The eating capability.'),
                    ('class Robot implements Workable { work() }', 'The robot implements only what it can do.'),
                    ('class Human implements Workable, Eatable { work() … eat() }', 'A human implements both: a class may implement several small interfaces.')]}],
        exam=[likely('A Robot class implements a Worker interface that declares work() and eat(), and leaves eat() empty. Which principle is violated, and how do you fix it?',
                     a='The Interface Segregation Principle: Robot is forced to depend on eat(), which it does not use. Split Worker into Workable (work()) and Eatable (eat()); Robot implements Workable only, Human implements both.')]),
    9: dict(
        hl=[('dependencies refer only to', 1), ('use', 2), ('import', 2), ('Nothing concrete should be depended on', 3), ('actively developing', 4)],
        notes=['The **Dependency Inversion Principle (DIP)**: the most flexible systems are those whose source-code dependencies refer **only to abstractions**, not to concretions.',
               'In a statically typed language like Java, that means **use, import and include** statements should name only interfaces, abstract classes or other abstract declarations.',
               '**Nothing concrete should be depended on**: concrete classes change often, abstractions rarely.',
               'In particular, avoid depending on modules that are **actively being developed** and change frequently: every change there would ripple into your code.']),
    10: dict(
        hl=[('High-level modules should NOT depend', 1), ('Both should depend on abstractions', 1), ('Abstractions should NOT depend on details', 2), ('Details should depend on abstractions', 2)],
        notes=['The two rules. **(1)** High-level modules (policy, e.g. a Manager) must not depend on low-level modules (details, e.g. a Worker). **Both** depend on an abstraction (an interface).',
               '**(2)** Abstractions must not depend on details; details depend on abstractions.',
               'The diagram: **without** inversion, Object A in Package A references Object B in Package B directly. **With** inversion, Object A references Interface A, and Object B implements (inherits) Interface A. The arrow from B now points *toward* the abstraction, the opposite (“inverted”) direction of the original dependency.'],
        exam=[likely('According to DIP, a high-level module should depend on:', a=0, opts=['Abstractions (interfaces)', 'Low-level modules', 'Concrete classes', 'Global variables'])]),
    11: dict(
        hl=[('Bad idea', 1, 0, 'ocr'), ('Good idea', 2, 0, 'ocr'), ('WITHOUT Dependency Inversion', 3, 0, 'ocr')],
        notes=['The real-life idea: a charger that only works with Samsung phones is useless when you change phones (bad). A **USB** charger works with any phone (good): USB is the interface, the abstraction.',
               'The same mistake in code, the **charger that only fits one phone**:',
               {'text': 'Switch without dependency inversion:', 'code': [
                    ('class Fan { void turnOn() { System.out.println("Fan is ON"); } }', 'A concrete low-level device.'),
                    ('class Switch {', 'The high-level module.'),
                    ('    Fan fan = new Fan();  // directly depends on Fan', 'The switch creates and holds a concrete Fan.'),
                    ('    void press() { fan.turnOn(); } }', 'Pressing can only ever turn on a fan.')]},
               'The problem: Switch works **only** with Fan. To control a Light you must change Switch.']),
    12: dict(
        hl=[('WITH Dependency Inversion', 1, 0, 'ocr'), ('Step 1', 2, 0, 'ocr'), ('Step 3', 3, 0, 'ocr')],
        notes=[{'text': 'The fix in three steps:', 'code': [
                    ('interface Device { void turnOn(); }', 'Step 1: the abstraction (the “USB port”).'),
                    ('class Fan implements Device { public void turnOn() { …"Fan is ON"… } }', 'Step 2: the details implement the abstraction.'),
                    ('class Light implements Device { public void turnOn() { …"Light is ON"… } }', 'A second device, added without touching Switch.'),
                    ('class Switch { Device device; Switch(Device device) { this.device = device; } void press() { device.turnOn(); } }', 'Step 3: Switch knows only Device; the concrete device is passed in through the constructor.'),
                    ('Switch s1 = new Switch(new Fan()); s1.press();', 'Wiring a fan: prints “Fan is ON”.'),
                    ('Switch s2 = new Switch(new Light()); s2.press();', 'Wiring a light: prints “Light is ON”. Same Switch class.')]},
               'Passing the dependency in from outside (instead of `new Fan()` inside) is called dependency injection; it is the usual way to apply DIP.']),
    13: dict(
        hl=[('violates DIP', 1), ('Worker worker;', 2), ('Problem', 3)],
        notes=[{'text': 'The textbook bad example, line by line:', 'code': [
                    ('class Worker { public void work() { // ....working } }', 'A concrete worker.'),
                    ('class Manager {', 'The high-level module (the boss).'),
                    ('    Worker worker;', 'The manager is fixed to one concrete type.'),
                    ('    public void setWorker(Worker w) { worker = w; }', 'It can only be given a Worker (the circled parameter type).'),
                    ('    public void manage() { worker.work(); } }', 'It tells that worker to work.')]},
               'Manager is the high-level module and depends directly on the low-level Worker.',
               '**Problem**: the boss only understands Worker. A Robot or an Intern can’t be managed without changing Manager, and tests can’t substitute a fake worker.']),
    14: dict(
        hl=[('interface IWorker', 1, 0, 'ocr'), ('IWorker worker', 2, 0, 'ocr'), ('RobotWorker', 3)],
        notes=[{'text': 'The good example:', 'code': [
                    ('interface IWorker { public void work(); }', 'The contract: any worker must know how to work.'),
                    ('class Worker implements IWorker { public void work() { // ....working } }', 'The original worker now follows the contract.'),
                    ('class RobotWorker implements IWorker { public void work() { …"Robot is working..."… } }', 'A new kind of worker, added without touching Manager.')]},
               {'text': 'Manager now depends only on the abstraction:', 'code': [
                    ('class Manager { IWorker worker;', 'The boss only cares about the interface, not the exact type.'),
                    ('    public void setWorker(IWorker w) { worker = w; }', 'Any worker (human, robot, AI, intern) can be assigned.'),
                    ('    public void manage() { worker.work(); } }', 'At run time the actual object’s `work()` runs.')]},
               'Bad code: Manager → Worker (tightly coupled). Good code: Manager → IWorker ← Worker, RobotWorker (loosely coupled and flexible). New workers such as **RobotWorker**, AIWorker or InternWorker need no change to Manager, which also makes Manager open for extension (OCP).'],
        exam=[likely('A Manager class holds a field of the concrete type Worker and calls worker.work(). Which principle does this violate? Draw or describe the fix.',
                     a='The Dependency Inversion Principle: the high-level Manager depends on the concrete low-level Worker. Fix: introduce interface IWorker { work(); }; Worker, RobotWorker, etc. implement it; Manager holds an IWorker and receives it through setWorker(IWorker). In UML: Manager → IWorker (dependency/association), Worker and RobotWorker ⇢ IWorker (realization).')]),
    15: dict(
        hl=[('internal structure and', 1), ('class diagram', 2), ('sequence', 3), ('Activate Sensors', 4, 0, 'ocr')],
        notes=['Component design models both the **internal structure** and the **behaviour** of a component.',
               'The internal **structure** is modelled with a **class diagram** (as in Lecture 2).',
               'The internal **behaviour** is modelled with a **sequence diagram**.',
               {'text': 'Reading the “Activate Sensors” example:', 'items': [
                   ('1: timer expires', 'An outside event reaches the ScheduleManager (`sm`).'),
                   ('2: getMsg() / 4: interpretMsg()', 'It fetches the scheduled message from `s : Schedule` and interprets it (a self-call).'),
                   ('alt frame', 'A choice: if `msgId == HEAT_MSG_ID` it sends 5: activate() to the HeatSensor; if `msgId == VIBRATE_MSG_ID` it sends 6: activate() to the VibrationSensor. Only one branch runs.')]}],
        exam=[likely('Which UML diagrams model a component’s internal structure and its internal behaviour?', a=0,
                     opts=['Class diagram for structure, sequence diagram for behaviour', 'Deployment diagram for structure, use case diagram for behaviour', 'Package diagram for both', 'Sequence diagram for structure, class diagram for behaviour'])]),
    16: dict(
        hl=[('well-defined', 1), ('What comes before how', 2), ('Separate orthogonal concerns', 3)],
        notes=['**Make sure the problem is well defined**: know all design criteria, requirements and constraints before starting the design.',
               '**What comes before how**: at every level of abstraction, define the functions to be performed before choosing the structures that implement them.',
               '**Separate orthogonal concerns**: don’t connect what is independent (orthogonal = unrelated, changing for different reasons).']),
    17: dict(
        hl=[('Design external functionality before internal functionality', 1), ('black-box', 1), ('Keep it simple', 2), ('simple problems huddled together', 2)],
        notes=['**External before internal**: first treat the solution as a black box and decide how it interacts with its environment; then decide how the box is organised inside, usually as smaller black boxes refined the same way.',
               '**Keep it simple**: fancy designs are buggier, harder to implement and verify, and often slower. Problems that look complex are often simple problems huddled together; the designer’s job is to separate them and solve each one.']),
    18: dict(
        hl=[('Work at multiple levels of abstraction', 1), ('Design for extensibility', 2), ('open-ended', 2), ('immaterial', 2)],
        notes=['**Work at multiple levels of abstraction**: good designers move quickly between the big picture and the details.',
               '**Design for extensibility**: a good design is “open-ended”, easy to extend. Don’t introduce what is immaterial (unimportant) and don’t restrict what is irrelevant (unrelated): both make later extension harder.']),
    19: dict(
        hl=[('rapid prototyping', 1), ('Details should depend upon abstractions', 2), ('share common closure', 3)],
        notes=['**Rapid prototyping**: before implementing, build a high-level prototype and check that the design criteria are met.',
               '**Details depend on abstractions; abstractions don’t depend on details**: the DIP stated as a rule of design.',
               '**Common closure**: classes in a released component should change together; if one needs to change, they all probably do (“what affects one, affects all”). Group classes by the reasons they change.']),
    20: dict(
        hl=[('reused together', 1), ('direction of stability', 2), ('more stable than the depender', 2), ('abstract', 3)],
        notes=['**Common reuse**: classes in a released component are reused together; you can’t take part of a component.',
               '**Stable dependencies**: dependencies between components must run in the direction of stability. The component depended on (dependee) must be more stable than the one depending on it.',
               '**Stable abstractions**: the more stable a component is, the more it should consist of abstract classes; a completely stable component contains nothing but abstractions. That is why interfaces sit at the stable end of DIP diagrams.'],
        exam=[likely('State the stable-dependencies rule and explain why stable components should be abstract.',
                     a='Dependencies must point toward more stable components (the dependee is more stable than the depender). Stable components are hard to change because many others depend on them, so they should consist of abstractions that can be extended without modification.')]),
    21: dict(
        hl=[('Depth-first design', 1), ('Directly refining requirements specification', 2), ('Failure to consider potential changes', 3), ('Making the design too detailed', 4)],
        notes=['**Depth-first design**: perfecting one part early and only partially satisfying the requirements overall. Experience is the best cure.',
               '**Directly refining the requirements specification** into a design: produces overly constrained, inefficient designs, because the structure copies the document instead of the problem.',
               '**Failing to consider potential changes**: always design for extension and contraction (adding and removing features).',
               '**Making the design too detailed**: over-constrains the implementation and leaves programmers no sensible choices.'],
        exam=[likely('Name two common design mistakes and their consequences.',
                     a='Any two: depth-first design (only partially satisfies requirements); directly refining the requirements specification (overly constrained, inefficient design); failing to consider potential changes (hard to extend); making the design too detailed (over-constrains the implementation).')]),
    22: dict(
        hl=[('Design Principles for Internal Component Design', 1), ('Designing Internal Behavior of Components', 2), ('Creational Design Patterns', 3)],
        notes=['Recap: the internal-component design principles (the slide lists SRP and DIP; this lecture added ISP and DIP to Lecture 2’s SRP, OCP and LSP).',
               'Internal behaviour is modelled with sequence diagrams, and the rules of design guide every decision.',
               'Next chapter: **creational design patterns**.']),
    23: dict(
        hl=[('Define the problem first', 1), ('What before how', 1), ('Keep it simple', 2), ('Depend on abstractions, not details', 3), ('Dependencies go toward stability', 4)],
        notes=['The rules from slides 16–20 in one list. Problem and requirements first; **what before how**; separate independent concerns; design external behaviour first.',
               '**Keep it simple**; work at several abstraction levels; design for extensibility; avoid the unnecessary; prototype early.',
               '**Depend on abstractions, not details** (DIP).',
               'Component rules: classes that change together and are reused together belong in one component; **dependencies go toward stability**; stable components should be abstract.']),
    24: dict(
        hl=[('Analysis', 1), ('Domain model class diagram', 2, 0, 'ocr'), ('Design class diagrams', 3, 0, 'ocr')],
        notes=['How analysis (requirements) models turn into design models. Left: the analysis models describe the problem.',
               'The **domain model class diagram** (Customer, Order) becomes the **design class diagrams** (with attributes and operations such as `changeName()`, `shipOrder()`); use case diagrams and activity diagrams feed the component and interaction (sequence) diagrams.',
               'System sequence diagrams become detailed **interaction diagrams**; requirements state machines (Ready → Shipped) become design state machines; and package diagrams organise the result into layers. Each design model traces back to an analysis model.']),
}

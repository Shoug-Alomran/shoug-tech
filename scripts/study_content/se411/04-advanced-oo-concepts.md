@head Chapter 4
@title Advanced OO Concepts
@sources chapter-4-advanced-oo-concepts
@count 191
@tldr Good object-oriented code hides details behind a contract, picks the right relationship between classes, lets one variable work with many object types (polymorphism), and prefers small interfaces plus composition over deep inheritance trees.
@why This is the longest chapter (191 slides) and the one most exam questions come from: constructor-chaining traces, "will this compile?", overriding vs overloading output, dynamic binding, final, interface vs abstract class, immutability traps, compareTo and shallow vs deep copy. Every one has a worked example below.
@connect Chapter 2's generics (`Comparable<E>`) and functional interfaces reappear here. Chapter 5's Runnable is an interface, and Chapter 6's Spring Boot is built on "program to an interface". Chapter 7 uses final classes and immutability for security.
@goals
- Explain abstraction, encapsulation and class contracts
- Tell association, aggregation, composition and inheritance apart
- Trace constructor chaining and fix missing no-arg constructors
- Distinguish overriding from overloading and predict output
- Explain dynamic binding, upcasting, downcasting and instanceof
- Use final, abstract classes, interfaces, default, static and private interface methods
- Use private constructors and factory methods
- Choose composition plus interfaces over inheritance where appropriate
- Build immutable classes and implement Comparable and Cloneable
@vocab
Encapsulation | Hiding a class's data and details behind public methods.
Contract | The public method signatures and constants users rely on.
Aggregation | Has-a: the whole holds parts that can live on their own.
Composition | Strong has-a: the parts die with the whole.
Overriding | A subclass replaces an inherited method with the same signature.
Overloading | Same method name, different parameter list.
Dynamic binding | The JVM picks the method from the object's actual class at run time.
Marker interface | An empty interface that tags a class, such as Cloneable.
Immutable | An object whose state can't change after construction.
@map
4 | Abstraction and encapsulation | MEMORIZE | Black-box contract
5-12 | Class relationships | MEMORIZE | Association to composition
13-33 | Inheritance, super, constructor chaining | WRITE | Trace and fix exercises
34-38 | Designing a class | MEMORIZE | Coherence, SRP, modifiers
39-48 | Overriding, overloading, dynamic binding | WRITE | Predict output
49-55 | Polymorphism | MEMORIZE | Compile-time vs runtime
56-92 | Payroll case study, downcasting | SKIM | Abstract earnings()
93-97 | final methods and classes | MEMORIZE | Can't override / extend
99-131 | Interfaces and Payable | MEMORIZE | default, static, private
132-144 | Private constructors, factories | WRITE | Exercises
145-163 | Interface vs inheritance, composition | MEMORIZE | Strong vs weak is-a
164-176 | Class design review, immutability | MEMORIZE | No setters isn't enough
177-191 | Comparable, Cloneable, deep copy | WRITE | compareTo exercise

## Abstraction, encapsulation and class relationships | Slides 4-12 | must
**Class abstraction** separates how a class is **implemented** from how it's **used**. The creator publishes a **contract**: the public method signatures and public constants. Users work only through that contract; the implementation is a **black box**, encapsulated and hidden.

::analogy A vending machine
You know the contract: insert money, press B4, get a drink. You don't know (or care) about the motors inside. The owner can replace the whole mechanism and you'd never notice, as long as the buttons still work the same way.
::

### Four relationships, from weakest to strongest
| Relationship | Meaning | Example | Lifetime |
|---|---|---|---|
| **Association** | Two independent classes interact (1-1, 1-many, many-many) | Student takes Course | Independent, no ownership |
| **Aggregation** | Has-a: whole contains parts | Library has Books | Parts survive without the whole |
| **Composition** | Strong has-a, exclusive ownership | House has Rooms | Parts die with the whole |
| **Inheritance** | Is-a, via `extends` | Circle is a GeometricObject | |

Aggregation and composition are usually coded as a **data field** in the owning class. Aggregation can even be on the **same class**: a `JFXLayout` may have a `parentLayout` field of type `JFXLayout` (or a list of them if a layout can sit inside many parents).

::mnemonic AACI: weakest to strongest
**A**ssociation, **A**ggregation, **C**omposition, then **I**nheritance as a different kind (is-a, not has-a). Think "a library doesn't own its readers (association), holds books it could give away (aggregation), but its rooms disappear with the building (composition)".
::
::check A University and its Departments: if the university closes, the departments no longer exist. Which relationship?
Composition: the parts' lifetime depends on the whole.
::
::key
- Abstraction separates use from implementation; users rely on the contract
- Association: independent classes interact
- Aggregation: has-a, parts can exist alone
- Composition: has-a, parts die with the whole
- Inheritance: is-a, using extends
::

## Inheritance, super and constructor chaining | Slides 13-33 | must
A subclass inherits fields and methods, can **add** new ones and can **override** inherited methods. But **constructors are NOT inherited**. A subclass constructor can only call them with `super(...)`.

**The hidden rule**: if a constructor doesn't explicitly call `this(...)` or `super(...)`, the compiler inserts `super();` as its **first statement**.

| super usage | Example |
|---|---|
| Call a superclass constructor | `super(width, height);` must be the **first** statement |
| Call an overridden superclass method | `super.toString()` |

::trap Calling the superclass constructor by name
`GeometricObject();` inside a subclass is a syntax error. You must write `super();`, and it must come first.
::

**Constructor chaining**: creating an object runs **every** constructor up the inheritance chain, top-down in output.

::code java
class Person {
    public Person() { System.out.println("(1) Person's no-arg constructor"); }
}
class Employee extends Person {
    public Employee() {
        this("(2) Invoke Employee's overloaded constructor");
        System.out.println("(3) Employee's no-arg constructor");
    }
    public Employee(String s) { System.out.println(s); }   // implicit super()
}
public class Faculty extends Employee {
    public Faculty() { System.out.println("(4) Faculty's no-arg constructor"); }  // implicit super()
    public static void main(String[] args) { new Faculty(); }
}
::
::steps Tracing new Faculty()
Faculty() starts and implicitly calls super(), meaning Employee().
Employee() calls this("(2)..."), meaning Employee(String).
Employee(String) implicitly calls super(), meaning Person().
Person() prints **(1)**, then returns.
Employee(String) prints **(2)**, then returns.
Employee() prints **(3)**, then returns.
Faculty() prints **(4)**.
::
::analogy Building floors
You can't build floor 3 before floors 1 and 2. Calls go **up** the chain first; printing happens on the way back **down**, so the most general class prints first.
::

### The missing no-arg constructor
::example Slides 31-33
`class Vehicle { public Vehicle(String brand) {...} }` and `class Car extends Vehicle { public Car() { System.out.println("Car constructor"); } }`.

**Does it compile? No.** Car() implicitly calls `super()`, meaning `Vehicle()`, which doesn't exist: once you write any constructor, Java no longer supplies a default one.

**Fix 1**: add `super("Toyota");` as the first line of Car(). **Fix 2**: add a no-arg `Vehicle()` constructor. Either way the output is "Vehicle constructor" then "Car constructor".
::
::tip Always give a class a no-arg constructor
If a class might be extended, provide one so subclasses don't break, as slide 30's Apple and Fruit example also shows.
::
::key
- Constructors are not inherited; call them with super(...)
- super(...) must be the first statement
- With no explicit call, the compiler inserts super()
- Chaining runs all constructors; the top superclass prints first
- No no-arg superclass constructor means a compile error in a subclass that relies on super()
::

## Designing a class | Slides 34-38, 164-169 | know
| Guideline | Meaning |
|---|---|
| **Coherence** | One class describes **one** entity, and all its operations fit together |
| **Single responsibility** | Split a class with too many jobs: String (immutable), StringBuilder (mutable) and StringBuffer (mutable, synchronized) |
| **Design for reuse** | Let users set properties in any order and call methods in any order; give a public no-arg constructor; override equals and toString |
| **Style** | Informative names; fields, then constructors, then methods; lowercase package names |
| **Visibility** | `private` fields with `public` accessors for users; `protected` for extenders |

::example Slide 164-166: the StoreOwner class
A `StoreOwner` class held identity data, draft store-design fields (theme, banner, cover image) and login details (password, googleId, authProvider). That breaks coherence. The fix splits it into `StoreOwner`, `StoreDesign` and `Authentication`, each with one responsibility.
::

A class has **two contracts**: one for **users** (public) and one for **extenders** (protected). The extenders' contract includes the users' one. Limiting scope and exposure is a principle of defensive programming.

::key
- A class should model one entity coherently
- Split classes that carry too many responsibilities
- Design for reuse: any order, no-arg constructor, equals and toString
- private fields with public accessors for users; protected for extenders
::

## Overriding, overloading and dynamic binding | Slides 39-55 | must
| | Overriding | Overloading |
|---|---|---|
| Where | Subclass vs superclass | Same class (or inherited) |
| Signature | **Same** name and parameters | Same name, **different** parameters |
| Decided | At **run time** (dynamic binding) | At **compile time** |
| Polymorphism type | Runtime (dynamic) | Compile-time (static) |

::code java
class B { public void p(double i) { System.out.println(i * 2); } }

// Version 1: OVERRIDES (same parameter type)
class A extends B { public void p(double i) { System.out.println(i); } }
// a.p(10) → 10.0     a.p(10.0) → 10.0

// Version 2: OVERLOADS (different parameter type)
class A extends B { public void p(int i) { System.out.println(i); } }
// a.p(10) → 10       a.p(10.0) → 20.0  (B's version)
::

::trap private and static methods can't be overridden
A **private** method isn't visible to the subclass, so a same-named method there is a completely unrelated method. A **static** method can be inherited but not overridden: redefining it **hides** it, and which one runs depends on the **variable's declared type**, not the object. No runtime polymorphism.
::

### Polymorphism and dynamic binding
**Polymorphism**: a variable of a supertype can refer to an object of any subtype. So `m(Object x)` accepts a GraduateStudent, a Student, a Person or a plain Object.

**Dynamic binding**: when `x.toString()` is called, the JVM searches for the method starting at the object's **actual** class (the most specific, C1) and moving up (C2, C3, ... Cn). It uses the **first** one found.

::example Slide 48
`C3 x = new C1(); x.p();`. The declared type is C3, but the object is a C1. Does C1 have p()? Yes, so C1's p() runs. C2 and C3 aren't searched.
::
::analogy A remote that asks "who are you?"
The variable type is the label on the remote ("Animal"). When you press speak, the remote asks the actual object what it is: a dog barks, a cat meows. The label only decides which buttons the remote has; the object decides what each button does.
::

**Upcasting** (subclass to superclass) is automatic. **Downcasting** (superclass to subclass) needs an explicit cast and should be guarded with `instanceof`. In the payroll case study, only a `BasePlusCommissionEmployee` gets a 10% base-salary raise, so the loop downcasts it to call `setBaseSalary`:

::code java
for (Employee e : employees) {
    if (e instanceof BasePlusCommissionEmployee) {
        BasePlusCommissionEmployee b = (BasePlusCommissionEmployee) e;   // downcast
        b.setBaseSalary(1.10 * b.getBaseSalary());
    }
    System.out.println(e.earnings());     // dynamic binding
}
::

**Rule**: through a superclass reference you can only call methods the **superclass declares**. That's why downcasting is needed for subclass-only methods. `getClass().getName()` gives an object's actual class name.

::mnemonic Overloading = cOmpile time; oVerRiding = Run time
Over**l**oading is decided at compile time from the parameter **l**ist. Over**r**iding is decided at **r**un time from the object.
::
::key
- Overriding: same signature in a subclass, chosen at run time
- Overloading: different parameters, chosen at compile time
- private methods can't be overridden; static methods are hidden, not overridden
- Dynamic binding searches from the object's actual class upward
- Downcast with an instanceof check to reach subclass-only methods
::

## Abstract classes and final | Slides 56-97 | must
The **payroll case study**: four employee types (salaried, hourly, commission, base-plus-commission). An **abstract class Employee** declares an **abstract `earnings()`** method because there's no sensible general formula; each concrete subclass implements its own. The program then pays everyone in one loop, polymorphically. Hourly pay is wage times hours, with **1.5 times the wage for hours over 40**.

| `final` on | Means |
|---|---|
| A method | Can't be **overridden** |
| A class | Can't be **extended**; all its methods are implicitly final |

`private` methods are implicitly final (they can't be overridden), and so are static methods (they're hidden, not overridden). **String is a final class**: nobody can subclass it and change its behaviour, so code can trust String objects and nobody can bypass its security checks.

::trap final ≠ abstract
An abstract method **must** be overridden; a final method **can't** be. So a method can't be both.
::
::key
- An abstract class can hold an abstract method each subclass implements
- The payroll loop pays every employee type with one earnings() call
- A final method can't be overridden; a final class can't be extended
- String is final, so its behaviour can be trusted
::

## Interfaces | Slides 99-131, 145-163 | must
The accounts-payable program must pay **employees and invoices**, which are unrelated (a person and a bill). Inheritance can't link them, but an **interface** can: both implement `Payable` with `getPaymentAmount()`, and one loop over `Payable[]` processes both.

::code java
public interface Payable {
    double getPaymentAmount();       // implicitly public abstract
}
public class Invoice implements Payable { ... }
public abstract class Employee implements Payable { ... }
::

**Interface rules**

| Rule | Detail |
|---|---|
| Methods with no modifier | Implicitly `public abstract` |
| Fields | Implicitly `public static final` (constants) |
| `default` methods (Java 8) | Have a body; implementing classes get them for free and may override them |
| `static` methods (Java 8) | Helper methods called as `Shape.printArea(c)` |
| `private` methods (Java 9) | Helpers shared by the interface's own methods |
| Multiple | A class can **extend one class but implement many interfaces** |

**Default methods** let you add a method to an existing interface without breaking every class that already implements it.

A class that implements an interface "signs a contract": implement every abstract method, or be declared abstract. Common API interfaces: **Comparable** (ordering), **Serializable** (can be saved or sent), **Runnable** (a task for a thread), **ActionListener**, **Comparator**. Any interface with one abstract method is a **functional interface** (SAM), so it works with lambdas (Chapter 2).

### Interface or abstract class?
| | Strong is-a | Weak is-a (is-kind-of) |
|---|---|---|
| Meaning | A true parent-child relationship | Has a capability or property |
| Model with | A **class** (inheritance) | An **interface** |
| Examples | Dog is an Animal; Student is a Person | String is Comparable; an Employee has a CompensationModel |

::analogy Family vs skills
Inheritance is your family tree: you have one set of biological parents. Interfaces are certificates: you can be a certified driver, swimmer and first-aider at once. "Comparable" is a skill, not a parent.
::

**Conflicting interfaces**: if two interfaces define the same constant with different values, or the same method signature with different return types, the compiler reports the error.

### Composition plus interfaces beat deep inheritance
Implementation inheritance suits **small, tightly coupled** hierarchies, but tight coupling makes big hierarchies hard to change. The slides redesign payroll: employees aren't really different, **their pay model is**. So `Employee` **has a** `CompensationModel` (an interface), with `SalariedCompensationModel`, `HourlyCompensationModel` and `CommissionCompensationModel` implementations.

| Change | Inheritance hierarchy | Composition + interface |
|---|---|---|
| Commission rule changes | Also affects the BasePlus subclass | Edit one model class |
| Add retirement plans | Touch the whole tree | Add a `RetirementPlan` interface |
| Employee is promoted | Must create a new object of another class | `setCompensationModel(newModel)` |

::mnemonic Program to an Interface, Not an Implementation: PINI
Declare variables and parameters by interface type, so the implementation can be swapped.
::
::key
- An interface lets unrelated classes share a type, such as Payable
- Interface methods are public abstract; fields are public static final
- default (Java 8), static (Java 8) and private (Java 9) methods are allowed
- A class extends one class but can implement many interfaces
- Strong is-a: class; weak is-a capability: interface
- Composition plus interfaces is more flexible than deep inheritance
::

## Private constructors and factory methods | Slides 132-144 | know
A **private constructor** has three uses:

| Use | Example |
|---|---|
| **Prevent instantiation** of a class that only has static members | `Calculator`, `UtilityLogger` with `private UtilityLogger() {}` |
| **Share initialization code** among constructors | Public constructors delegate with `this(...)` to one private one |
| **Force factory methods** | Clients call a `public static` method that creates the object |

::code java
public abstract class Logger {
    public abstract void log(String message);

    public static Logger getLogger(String type) {          // factory method
        if (type == null) throw new IllegalArgumentException("Logger type cannot be null");
        if (type.equalsIgnoreCase("console")) return new ConsoleLogger();
        if (type.equalsIgnoreCase("file"))    return new FileLogger("app.log");
        throw new IllegalArgumentException("Unknown logger type: " + type);
    }
}
::

The return type is the abstract `Logger`, so callers never depend on `ConsoleLogger` or `FileLogger` directly: program to an interface again.

::key
- A private constructor stops other classes using new
- Utility classes with only static methods use one
- Public constructors can delegate to a private one with this(...)
- A factory method is a public static method that returns a new object, typed as the abstraction
::

## Immutable objects | Slides 170-176 | must
An **immutable** object can't change after it's created; String is the classic example.

::code java
public class Student {
    private String name;
    private int[] grades;
    public int[] getGrades() { return grades; }   // leaks the array
}
int[] g = student.getGrades();
g[0] = 100;    // the Student's grades just changed
::
::trap No setters ≠ immutable
The getter above hands out a reference to the mutable array, so callers can change the Student. Fix: `return grades.clone();`. The same leak happens with a `BirthDate` object field.
::

::formula Immutable class checklist
All fields private
No mutator (set) methods
No accessor returns a reference to a mutable field
::

Returning a String field is safe because String itself is immutable: `x = "Ali";` points `x` at a new String and leaves the original untouched.

| Advantage | Why |
|---|---|
| Simplicity | Only one state, so easier reasoning and debugging |
| **Thread safety** | Nothing changes, so no synchronization needed (Chapter 5) |
| Robustness | Shared references can't be corrupted |

::key
- Immutable: the state can't change after construction
- Requires private fields, no setters, and no leaked mutable references
- Return a copy (clone) of mutable fields
- Immutable objects are simple and thread-safe
::

## Comparable and Cloneable | Slides 177-191 | must
Operators such as `<` don't work on objects. **`Comparable<E>`** has one method, `int compareTo(E o)`: negative if this is smaller, 0 if equal, positive if larger. Integer, String, Date and the wrapper classes implement it, which is why `Arrays.sort(cities)` works on a String array. `Arrays.sort` requires its elements to be Comparable.

::code java
public class ComparableRectangle extends Rectangle
        implements Comparable<ComparableRectangle> {
    @Override
    public int compareTo(ComparableRectangle o) {
        if (getArea() > o.getArea()) return 1;
        else if (getArea() < o.getArea()) return -1;
        else return 0;
    }
}
::
::example Exercise: ComparableEmployee (slide 190)
Compare by **rank** first; if ranks are equal, compare **salary**. Return 1, -1 or 0. Write the rank comparison as the outer if/else and the salary comparison inside the "ranks equal" branch.
::

### Cloneable: a marker interface
**Cloneable** is **empty**: a **marker interface** that says "objects of this class may be copied with `clone()`". To support it, override `clone()` and make it **public** (it's protected in Object).

::code java
@Override
public House clone() throws CloneNotSupportedException {
    House cloned = (House) super.clone();               // shallow copy
    cloned.whenBuilt = (Date) whenBuilt.clone();         // deep copy the mutable field
    return cloned;
}
::

| | Shallow copy | Deep copy |
|---|---|---|
| What's copied | Field values; object fields still **point to the same objects** | Mutable object fields are cloned too |
| Default `Object.clone()` | Yes | No, you add it |
| Fine when | Fields are primitives or immutable (String, Integer) | Fields are mutable (Date, ArrayList) |

`calendar == calendarCopy` is **false** (different objects), but `calendar.equals(calendarCopy)` is **true** (same contents).

::trap final fields and clone
A `final` field can't be reassigned after cloning, so you can't deep-copy it. That often makes cloning not useful for such classes.
::
::analogy Photocopying a folder
A shallow copy photocopies the cover page that says "see the drawer for documents": both copies point at the same drawer. A deep copy also photocopies everything in the drawer.
::
::key
- compareTo returns negative, zero or positive
- Arrays.sort needs Comparable elements
- Cloneable is a marker interface with no methods
- Override clone() as public; Object.clone() is a shallow copy
- Deep-copy mutable fields such as Date or ArrayList
::
@cheat
### Relationships
- Association: independent
- Aggregation: has-a, parts survive
- Composition: parts die with whole
- Inheritance: is-a
### Constructors
- Not inherited; super(...) first
- Implicit super() if none
- Chain: top class prints first
- No no-arg super → compile error
### Override vs overload
- Override: same signature, run time
- Overload: different params, compile time
- private: not overridden; static: hidden
- Dynamic binding: actual class upward
- Downcast after instanceof
### final / abstract
- final method: no override
- final class: no extend (String)
- abstract method: must override
### Interfaces
- Methods public abstract; fields public static final
- default, static (8); private (9)
- Extend one, implement many
- Weak is-a → interface
- Composition + interface > deep tree
### Objects
- Private constructor: utility, shared init, factory
- Immutable: private, no setters, no leaks
- compareTo: neg / 0 / pos
- Cloneable = marker; deep-copy mutable fields
@mcq 7
A Library holds Books that can exist without the library. This is:
+ Aggregation
- Composition
- Inheritance
- No relationship
> Parts' lifetime doesn't depend on the whole.
@mcq 9
A House and its Rooms, where rooms can't exist without the house, is:
+ Composition
- Aggregation
- Association
- Inheritance
> Strong ownership.
@mcq 15
Which statement about constructors is true?
+ Superclass constructors are not inherited
- Subclasses inherit all superclass constructors
- super() may appear anywhere in a constructor
- A subclass constructor never calls a superclass constructor
> Slide 15.
@mcq 33
`class Vehicle { Vehicle(String b){} }` and `class Car extends Vehicle { Car(){} }`. What happens?
+ Compile error: Vehicle() is undefined
- Prints "Vehicle constructor"
- Runtime exception
- Compiles with no output
> Car() implicitly calls super().
@mcq 29
In the Person, Employee, Faculty chain, which line prints first?
+ Person's no-arg constructor
- Faculty's no-arg constructor
- Employee's no-arg constructor
- Employee's overloaded constructor
> Calls go up first; printing comes back down.
@mcq 45
B has `p(double)`; A extends B with `p(int)`. `a.p(10.0)` calls:
+ B's p(double), because A overloads rather than overrides
- A's p(int)
- A compile error
- Both methods
> Overloading: different parameter types.
@mcq 43
A static method redefined in a subclass is:
+ Hidden, chosen by the variable's declared type
- Overridden, chosen by the object's type
- A compile error
- Made final automatically
> Slide 43.
@mcq 48
`C3 x = new C1(); x.p();` where C1, C2 and C3 all define p(). Which runs?
+ C1's p()
- C3's p()
- C2's p()
- A compile error
> Dynamic binding starts at the actual class.
@mcq 50
Runtime polymorphism is achieved through:
+ Method overriding
- Method overloading
- Private constructors
- Static methods
> Slide 50.
@mcq 96
A final class:
+ Can't be extended
- Can't be instantiated
- Must have abstract methods
- Can only have static methods
> String is final.
@mcq 104
Fields declared in an interface are implicitly:
+ public static final
- private
- protected abstract
- instance variables
> Slide 104.
@mcq 125
Why were default methods added to interfaces in Java 8?
+ To add methods without breaking existing implementing classes
- To allow interfaces to have constructors
- To let interfaces hold instance variables
- To replace abstract classes completely
> Slide 125.
@mcq 163
"A String can be compared" is a weak is-a relationship, so it is best modelled as:
+ An interface (Comparable)
- A superclass
- Composition
- A final class
> Slide 163.
@mcq 155
In the redesigned payroll, promoting an employee means:
+ Calling setCompensationModel with a new model
- Creating an object of a different Employee subclass
- Changing the Employee superclass
- Deleting the Employee
> Composition plus interfaces.
@mcq 132
A class with only static helper methods should:
+ Have a private constructor
- Be abstract with an abstract method
- Implement Cloneable
- Have a public setter for every field
> Prevents instantiation.
@mcq 172
A class has private fields and no setters but returns its int[] field directly. Is it immutable?
+ No, callers can change the array through the returned reference
- Yes, because there are no setters
- Yes, because the fields are private
- Only if the class is final
> Return a clone instead.
@mcq 184
Cloneable is called a marker interface because:
+ It has no methods or constants
- It marks methods as final
- It has exactly one abstract method
- It can only be used with Strings
> Slide 184.
@mcq 187
The default Object.clone() makes:
+ A shallow copy
- A deep copy
- No copy
- A serialized copy
> Slide 187.
@short 20
Trace `new Faculty()` for Person, Employee (no-arg calls this("(2)...")) and Faculty, and give the output order.
~ super, this, Person, chain, (1) (2) (3) (4)
> Faculty() calls super(), meaning Employee(), which calls this(...), meaning Employee(String), which calls super(), meaning Person(). Person prints (1), Employee(String) prints (2), Employee() prints (3), and Faculty prints (4).
@short 150
Explain why the slides redesign the Employee hierarchy using composition and an interface.
~ CompensationModel, has-a, flexible, promotion, coupling
> Employees differ only in how they're paid, so each Employee has a CompensationModel interface instead of being a subclass. This reduces coupling: a pay rule changes in one class, new capabilities such as retirement plans become new interfaces, and a promotion just calls setCompensationModel.
@short 175
List the conditions for a class to be immutable, and explain why a class with no setters may still be mutable.
~ private, no mutators, reference, mutable field, clone
> All fields must be private, there must be no mutator methods, and no accessor may return a reference to a mutable field. Without setters, a getter that returns an array or Date object still lets callers change the internal state, so return a copy instead.

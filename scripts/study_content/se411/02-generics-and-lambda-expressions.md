@head Chapter 2
@title Generics and Lambda Expressions
@sources chapter-2-generics-and-lambda-expressions
@count 80
@tldr Generics let one class or method work safely with any type, and lambdas let you pass a small piece of behaviour around like a value.
@why Both features remove repetitive code, which is what Chapter 1 asked for. Exams in this course usually give you code with a blank to fill in (a lambda, a generic class header) or ask why `List<Integer>` can't be passed where `List<Object>` is expected. This page covers every one of those patterns.
@connect Chapter 1 said to avoid duplication. Generics stop you writing the same class for each type, and lambdas stop you writing a whole class for one method. Both return in Chapter 5's threads and Chapter 6's Spring code.
@goals
- Write lambda expressions for a functional interface
- Explain why a lambda can be stored in a variable
- Write generic classes, generic methods and generic interfaces
- Explain why `List<Integer>` isn't a `List<Object>`, and use wildcards
- Use the Java Collections Framework with generics
@vocab
Functional interface | An interface with exactly one abstract method.
Lambda | An unnamed function: parameters, an arrow, and a body.
Type parameter | A placeholder such as `T` for a real type.
Wildcard | `?`, meaning "some unknown type".
Bounded wildcard | `? extends X`: some type that is X or a subclass.
@map
4-11 | Lambda expressions and exercises | WRITE | Fill in the lambda
12-20 | Generics: classes and methods | WRITE | Box, Pair, Pair2, count
21-23 | Subclassing and wildcards | MEMORIZE | Why List<Integer> fails
24 | AI and functional Java | SKIM | Verify rewrites
25-41 | Collections Framework | MEMORIZE | List methods, no primitives
45-72 | Deeper look: arrays, Stack, Bag | WRITE | Reuse with generics
73-80 | Exercises, passing and returning lambdas | WRITE | Practice

## Lambda expressions | Slides 4-11, 78-79 | must
A lambda (added in Java 8) is **like a function without a name**: it takes parameters and runs some code.

::formula Syntax
(parameter1, parameter2) -> { code block }
x -> x * 2              (one parameter, one expression)
::

::code java
ArrayList<Integer> numbers = new ArrayList<>(List.of(5, 9, 8));
numbers.forEach(n -> System.out.println(n));
::

**Why can a lambda be stored in a variable?** Because the variable's type is a **functional interface**: an interface with **exactly one abstract method**. The lambda supplies that method's body, so it must have the same number of parameters and the same return type.

::code java
interface Calculator { int calculate(int a, int b); }

Calculator add = (a, b) -> a + b;
System.out.println(add.calculate(5, 3));   // 8
::
::analogy A job description with one task
A functional interface is a job description with exactly one duty. A lambda is the person you hire who knows how to do that one thing. Because there's only one duty, nobody has to say which method the lambda is for.
::

Before Java 8 the same thing needed an anonymous inner class:

::code java
// Java 8+
btnAlert.setOnAction(event -> new AlertBox().display("Warning", "Alert!"));

// Java 7 and below
btnAlert.setOnAction(new EventHandler<ActionEvent>() {
    @Override
    public void handle(ActionEvent event) {
        new AlertBox().display("Warning", "Alert!");
    }
});
::

::example Slide exercises: fill in the blank
`Greeting { void sayHello(String name); }` → `Greeting greeting = name -> System.out.println("Hello " + name);`

`NumberChecker { boolean check(int number); }` → `NumberChecker even = number -> number % 2 == 0;`
::

Lambdas can also be **passed to methods** (slide 78) and **returned from methods** (slide 79):

::code java
static int performOperation(int a, int b, Operation op) { return op.execute(a, b); }
int result = performOperation(5, 3, (a, b) -> a + b);       // 8

static Function<Integer, Integer> getSquareLambda() { return x -> x * x; }
getSquareLambda().apply(4);                                  // 16
::
::trap Two abstract methods means no lambda
A lambda can only target an interface with **one** abstract method. Add a second and the lambda no longer compiles. `@FunctionalInterface` makes the compiler check this for you.
::
::mnemonic One Abstract method = Lambda-ready (OAL)
If the interface has **o**ne **a**bstract method, it's **l**ambda-ready.
::
::key
- A lambda is an unnamed function: parameters -> body
- It can be stored in a variable whose type is a functional interface
- A functional interface has exactly one abstract method
- The lambda must match that method's parameters and return type
- Lambdas can be passed to and returned from methods
::

## Generic classes and methods | Slides 12-20 | must
Generics express code that is **independent of a specific type**. The type parameter `T` is a placeholder for any type.

::code java
class Box<T> {
    private T value;
    void set(T value) { this.value = value; }
    T get() { return value; }
}

Box<Integer> intBox = new Box<>();
intBox.set(10);        // fine
intBox.set("Hello");   // compile-time error
::

**Before generics**, collections stored `Object`, which caused two problems: you needed a **cast** when reading, and **no type checking** stopped you adding the wrong type, so errors appeared only at run time.

::analogy A labelled storage box
An `Object` box is an unlabelled cardboard box: anything goes in, and you find out what it is when you open it. A `Box<Integer>` is labelled "integers only", and the compiler refuses anything else at the door.
::

Two type parameters (slide 19, Exercise 3):

::code java
public class Pair2<T, S> {
    private T first;
    private S second;
    public Pair2(T first, S second) { this.first = first; this.second = second; }
    public T getFirst()  { return first; }
    public S getSecond() { return second; }
}
::

**Generic methods** put the type parameter **before the return type**:

::code java
public static <T> int count(T... a) { return a.length; }
public static <T> T getFirst(T... a) { return a[0]; }
::

`T... a` (varargs) accepts any number of arguments of type T.

**Generic interfaces** (slide 77) work the same way: `interface Pair<K, V> { K getKey(); V getValue(); }`, implemented by `class KeyValue<K, V> implements Pair<K, V>`.

::example Swapping a Pair (slide 75)
`public Pair<U, T> swap() { return new Pair<>(second, first); }`: the types swap places too.
::
::trap No primitive type arguments
`List<int>` doesn't compile. Use the wrapper: `List<Integer>`, `List<Double>`.
::
::key
- A type parameter is a placeholder for any type
- Generics give compile-time type checking and remove casts
- Use two parameters, such as T and S, when attributes differ in type
- A generic method declares its type parameter before the return type
- Primitive types can't be type arguments
::

## Subclassing and wildcards | Slides 21-23, 69-72 | must
This surprises everyone:

::code java
private void printList(List<Object> myList) { ... }

List<Integer> intList = new ArrayList<>();
printList(intList);   // ERROR
::

**Integer is a subclass of Object, but `List<Integer>` is NOT a subclass of `List<Object>`.** If it were, `printList` could add a String into your list of integers.

| Parameter type | Accepts |
|---|---|
| `List<Object>` | Only a `List<Object>` |
| `List<?>` (wildcard) | A list of **any** type |
| `List<? extends Button>` (bounded) | A list of Button **or any subclass**, such as `List<CancelButton>` |

::analogy A fruit basket and an apple basket
An apple is a fruit. But a basket of apples isn't a "basket that accepts any fruit": if you treated it as one, someone could drop a banana into your apple basket. Wildcards say "I'll only look, not add".
::
::mnemonic Extends = Each one is at least an X
`? extends Button` means **each** element is at least a Button, so you can safely call Button methods on all of them.
::
::check Which header lets you pass a `List<Integer>` and a `List<String>`?
`printList(List<?> myList)`.
::
::key
- `List<Integer>` is not a subclass of `List<Object>`
- The wildcard `?` accepts a list of any type
- `? extends X` accepts lists of X or any subclass of X
::

## The Java Collections Framework | Slides 25-41 | know
The **JCF** gives interfaces and classes for common data structures. Generics were added in Java 5 mainly to make the collections type-safe.

::code java
List<String> list1 = new ArrayList<>();   // ArrayList implementation
List<String> list2 = new LinkedList<>();  // LinkedList implementation
::

Program to the **interface** (`List`) and choose the implementation on the right.

| List method | Does |
|---|---|
| `add()` / `addAll()` | Add one / all elements |
| `get()` | Random access by index |
| `set()` | Change an element |
| `remove()` / `removeAll()` | Remove one / all matching |
| `iterator()` | Returns an Iterator for sequential access |

**Iterator** methods: `hasNext()`, `next()`, `remove()`.

### Reuse in practice (slides 45-72)
The slides show the same duplication twice: `printArray` written for `Integer[]`, `Double[]` and `Character[]`, and a Stack plus near-identical tests for each type. One generic version replaces all of them. The **Bag** exercise (slides 63-68) is a generic ADT: an `IBag<T>` interface and a `ListBag<T>` implementation backed by an `ArrayList<T>`.

::key
- The JCF provides interfaces such as List and implementations such as ArrayList
- Declare by interface, construct by implementation
- Iterator offers hasNext, next and remove
- One generic class or method can replace several type-specific copies
::
@cheat
### Lambdas
- (params) -> body
- Target: functional interface (one abstract method)
- Same parameters and return type
- Pass to / return from methods
### Generics
- class Box<T>
- class Pair2<T, S>
- <T> before return type for methods
- T... = varargs
- No primitives: List<Integer>
### Subtyping
- List<Integer> is not a List<Object>
- List<?> accepts any list
- ? extends X: X or subclasses
### Collections
- List<String> l = new ArrayList<>()
- add, get, set, remove, iterator
- Iterator: hasNext, next, remove
@mcq 5
A lambda can be stored in a variable when the variable's type is:
+ An interface with exactly one abstract method
- Any class
- An interface with two abstract methods
- A primitive type
> A functional interface.
@mcq 11
Which lambda checks if a number is even?
+ number -> number % 2 == 0
- number -> number / 2
- (number) => even
- number -> return number % 2
> It returns a boolean, matching check(int).
@mcq 9
For `interface Greeting { void sayHello(String name); }`, which is valid?
+ Greeting g = name -> System.out.println("Hello " + name);
- Greeting g = () -> System.out.println("Hello");
- Greeting g = (a, b) -> a + b;
- Greeting g = name -> name;
> One parameter and no return value.
@mcq 14
Before generics, collections stored elements as:
+ Object references
- Primitive ints
- Strings only
- Lambdas
> That required casts and gave no type checking.
@mcq 13
Given Box<Integer> b, which line fails to compile?
+ b.set("Hello");
- b.set(10);
- Integer x = b.get();
- b.set(Integer.valueOf(3));
> A String isn't an Integer.
@mcq 20
In a generic method, the type parameter is placed:
+ Before the return type
- After the method name
- At the end of the parameter list
- Inside the method body
> public static <T> int count(T... a).
@mcq 21
Why can't a List<Integer> be passed to a method expecting List<Object>?
+ List<Integer> isn't a subclass of List<Object>
- Integer isn't a subclass of Object
- Generics don't work with methods
- Lists can't be parameters
> Otherwise the method could add non-Integers.
@mcq 23
`List<? extends Button>` accepts:
+ A list of Button or any subclass of Button
- Only List<Button>
- Lists of any type
- Only List<Object>
> A bounded wildcard.
@mcq 41
Which declaration is valid?
+ List<Integer> numbers;
- List<int> numbers;
- List<double> values;
- List<char> letters;
> Primitive types can't be type arguments.
@mcq 19
To let `first` and `second` have different types, the class header should be:
+ public class Pair2<T, S>
- public class Pair2<T>
- public class Pair2<Object>
- public class Pair2<T extends S>
> Two type parameters.
@mcq 29
The Iterator interface is used to:
+ Access elements of a collection one at a time
- Sort a collection
- Create a lambda
- Compile generic code
> hasNext and next.
@mcq 7
Before Java 8, behaviour like a lambda was written as:
+ An anonymous inner class
- A generic method
- A wildcard
- A static variable
> Slide 7.
@short 5
Explain why `Calculator add = (a, b) -> a + b;` compiles.
~ functional interface, one abstract method, parameters, return type
> Calculator is a functional interface with one abstract method, calculate(int, int). The lambda has two parameters and returns an int, so it supplies that method's body.
@short 21
Explain why List<Integer> isn't a List<Object>, and how a wildcard fixes the method header.
~ subclass, add, type safety, ?, wildcard
> If List<Integer> were a List<Object>, a method could add a String to a list of integers, breaking type safety. Declaring the parameter as List<?> accepts a list of any type without allowing unsafe additions.
@short 14
Give two problems that generics solved.
~ cast, type checking, runtime, compile
> Without generics, reading from a collection needed a cast, and nothing stopped you adding the wrong type, so errors appeared only at run time. Generics remove the cast and check types at compile time.

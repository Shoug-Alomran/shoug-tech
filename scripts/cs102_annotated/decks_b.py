"""CS102 annotated slides — Inheritance, Polymorphism, Recursion, Multidimensional Arrays.
See decks_a.py for how several decks share one module."""
from .common import mcq, scen, short, tf, tip, trap, trick


class inheritance:
    AUTO_SLIDES = True
    DECK = {'key': 'inheritance', 'slug': '05-inheritance', 'file': 'inheritance', 'title': 'Inheritance', 'chapter': 'Inheritance',
            'pdf': '/academics/computer-science/cs102/slides/inheritance/',
            'lede': ('Superclasses and subclasses, direct vs. indirect superclasses and Object, is-a vs. has-a, the '
                     'CommissionEmployee / BasePlusCommissionEmployee example with and without inheritance, constructors and '
                     'super(...), overriding with @Override, and private members in a hierarchy.')}
    ANN = {
        1: dict(kind='title', title='Inheritance', body=[], sub='CS102'),
        3: dict(notes=['Inheritance = reuse: a new class absorbs an existing class’s members and adds or modifies some.']),
        4: dict(notes=['Existing class = superclass; new class = subclass (extends).'],
                exam=[mcq('Which keyword makes a class inherit from another?', ['extends', 'implements', 'inherits', 'super'], 0, '')], weight=3),
        5: dict(notes=['Direct superclass: the one you extend. Indirect: higher up. Every class ultimately extends Object.'],
                exam=[tf('Java supports multiple inheritance of classes (a class can extend two classes).', False, 'Single inheritance; use interfaces for more.')], weight=3),
        7: dict(notes=['Superclasses are more general, subclasses more specific; a subclass object IS-A superclass object.']),
        11: dict(notes=['is-a = inheritance (a Car is a Vehicle). has-a = composition (a Car has an Engine).'],
                 exam=[mcq('“A Manager is an Employee” suggests:', ['Inheritance', 'Composition', 'An interface constant', 'A static method'], 0, '')], weight=3),
        13: dict(notes=['A subclass may inherit methods it doesn’t want; it can override them.']),
        14: dict(notes=['Without inheritance, BasePlusCommissionEmployee copies almost all of CommissionEmployee.']),
        19: dict(notes=['Constructors are NOT inherited. A subclass constructor must call a superclass constructor first (explicitly with super(...) or implicitly).'],
                 exam=[tf('Constructors are inherited by subclasses.', False, '')], weight=3),
        20: dict(notes=['Overriding: same signature in the subclass; @Override asks the compiler to check it.'],
                 tips=[trap('Overloading = same name, different parameters (same class). Overriding = same signature in a subclass.')],
                 exam=[mcq('A subclass method with the same signature as a superclass method:', ['Overrides it', 'Overloads it', 'Hides the class', 'Causes a compile error'], 0, '')], weight=3),
        23: dict(notes=['Copy-and-paste reuse is error-prone and a maintenance nightmare → use inheritance.']),
        24: dict(notes=['class BasePlusCommissionEmployee extends CommissionEmployee: only the base salary is new.']),
        25: dict(notes=['super(args) must be the FIRST statement in the subclass constructor.'],
                 exam=[mcq('Where must the call super(first, last, ssn) appear in a subclass constructor?', ['As the first statement', 'Anywhere in the body', 'As the last statement', 'Outside the constructor'], 0, '')], weight=3),
        26: dict(notes=['A subclass can’t access the superclass’s PRIVATE fields directly → use get methods (or protected).'],
                 exam=[tf('A subclass can directly read its superclass’s private instance variables.', False, 'Use getters or protected access.')], weight=3),
    }


class polymorphism:
    AUTO_SLIDES = True
    DECK = {'key': 'polymorphism', 'slug': '08-polymorphism', 'file': 'polymorphism', 'title': 'Polymorphism', 'chapter': 'Polymorphism',
            'pdf': '/academics/computer-science/cs102/slides/polymorphism/',
            'lede': ('Programming in the general: superclass references to subclass objects, dynamic binding, abstract classes '
                     'and methods, the polymorphic payroll system (Employee hierarchy), instanceof and downcasting, final '
                     'methods and classes, and interfaces (Measurable, Payable) for unrelated classes.')}
    ANN = {
        1: dict(kind='title', title='Polymorphism', body=[], sub='CS102 · Java How to Program, Chapter 10'),
        3: dict(notes=['Polymorphism: write code for the superclass and it works for every subclass (“program in the general”).']),
        5: dict(notes=['Same message (move) → different behaviour per object (fish swims, bird flies).']),
        6: dict(notes=['Polymorphic systems are extensible: add new subclasses with little or no change.']),
        8: dict(notes=['A superclass reference can point to a subclass object; the OBJECT’s type decides which method runs.'],
                exam=[mcq('Employee e = new SalariedEmployee(); e.earnings(); runs which earnings()?', ['SalariedEmployee’s', 'Employee’s', 'Object’s', 'Compile error'], 0, '')], weight=3),
        9: dict(notes=['A superclass object is NOT a subclass object; downcasting needs an explicit cast.']),
        14: dict(notes=['Compile time: the variable’s type must have the method. Run time: the object’s type picks the version → dynamic binding.'],
                 tips=[trick('Compiler checks the REFERENCE type; JVM runs the OBJECT type.')], weight=3),
        15: dict(notes=['Abstract classes: never instantiated; used as superclasses; incomplete.']),
        17: dict(notes=['abstract method = no body (public abstract void draw();). A class with an abstract method must be abstract. Concrete subclasses must implement it.'],
                 exam=[tf('A class that contains an abstract method must itself be declared abstract.', True, ''),
                       tf('Constructors can be declared abstract.', False, '')], weight=3),
        18: dict(notes=['You can’t create objects of an abstract class, but you can declare variables of its type.'],
                 exam=[mcq('Given abstract class Shape, which is legal?', ['Shape s = new Circle();', 'Shape s = new Shape();', 'new Shape().draw();', 'abstract Shape s;'], 0, '')], weight=3),
        20: dict(notes=['Payroll case study: salaried, hourly, commission and base-plus-commission employees.']),
        24: dict(notes=['Employee declares abstract earnings(); each subclass overrides it.']),
        34: dict(notes=['Process objects polymorphically; give BasePlusCommission employees a 10% raise using instanceof.']),
        35: dict(notes=['toString and earnings calls are resolved at run time: dynamic (late) binding.']),
        37: dict(notes=['Downcasting to the wrong type throws ClassCastException → check with instanceof first.'],
                 exam=[mcq('Before downcasting an Employee reference to BasePlusCommissionEmployee you should check with:', ['instanceof', 'equals', 'getClass().getName()', '=='], 0, '')], weight=3),
        38: dict(notes=['getClass().getName() returns the object’s class name.']),
        40: dict(notes=['Assigning a superclass reference to a subclass variable needs a cast.']),
        41: dict(notes=['final method: can’t be overridden (static binding). private and static methods are implicitly final.']),
        42: dict(notes=['final class: can’t be extended (e.g., String).'],
                 exam=[mcq('A class declared final:', ['Cannot be extended', 'Cannot be instantiated', 'Has only static methods', 'Must be abstract'], 0, '')], weight=3),
        43: dict(notes=['An interface lists methods to implement; a class can implement many interfaces.']),
        46: dict(notes=['Interface methods are implicitly public abstract; fields are public static final.'],
                 exam=[mcq('Fields declared in an interface are implicitly:', ['public static final', 'private', 'protected', 'instance variables'], 0, '')], weight=3),
        47: dict(notes=['implements = a contract; a class that doesn’t implement every method must be abstract.']),
        55: dict(notes=['Use an interface instead of an abstract class when there’s no default implementation to inherit.']),
        56: dict(notes=['Implementing classes have an is-a relationship with the interface type.']),
        59: dict(notes=['UML: «interface» stereotype; realization = dashed arrow with hollow head.']),
        70: dict(notes=['One superclass, many interfaces: class X extends A implements I1, I2.'],
                 exam=[tf('A Java class can implement more than one interface.', True, '')], weight=3),
    }


class recursion:
    AUTO_SLIDES = True
    DECK = {'key': 'recursion', 'slug': '09-recursion', 'file': 'recursion', 'title': 'Recursion', 'chapter': 'Recursion',
            'pdf': '/academics/computer-science/cs102/slides/recursion/',
            'lede': ('Recursive methods, base cases and recursive cases, countdown, the call sequence, infinite recursion and '
                     'stack overflow, recursion vs. iteration, tail recursion, factorial, Fibonacci, and a recursive power method.')}
    ANN = {
        1: dict(kind='title', title='Recursion', body=[], sub='CS102 · Savitch, Chapter 11'),
        3: dict(notes=['A recursive method calls itself on a smaller version of the same problem.']),
        4: dict(notes=['First handle the BASE CASE (stopping condition).']),
        8: dict(notes=['Keys: a branch to separate cases, a recursive call on a SMALLER argument, and a base case with no recursion.'],
                exam=[short('What three things does a correct recursive method need?', 'A branch that separates cases; at least one recursive call on a smaller version of the problem; and a base case that stops without recursing.')], weight=3),
        9: dict(notes=['No base case (or not getting smaller) → infinite recursion → StackOverflowError.'],
                exam=[mcq('Infinite recursion in Java eventually causes:', ['StackOverflowError', 'An infinite loop with no error', 'NullPointerException', 'ArithmeticException'], 0, '')], weight=3),
        10: dict(notes=['Every recursive method can be rewritten iteratively.']),
        11: dict(notes=['Recursion uses more memory (a stack frame per call) and is often slower; but can be clearer.'], weight=2),
        14: dict(notes=['Tail recursion: the recursive call is the last action.']),
        16: dict(notes=['n! = n × (n − 1)!, with 0! = 1! = 1.'],
                 exam=[short('Write a recursive factorial method.', 'public static long factorial(long n) { if (n <= 1) return 1; return n * factorial(n - 1); }')], weight=3),
        22: dict(notes=['Fibonacci: 0, 1, 1, 2, 3, 5, 8…; fib(n) = fib(n − 1) + fib(n − 2).'],
                 exam=[mcq('With fib(0) = 0 and fib(1) = 1, fib(6) is:', ['8', '5', '13', '6'], 0, '')], weight=3),
        23: dict(notes=['Two base cases: fib(0) = 0, fib(1) = 1. Naïve recursion repeats work exponentially.']),
        26: dict(notes=['power(base, exp) = base × power(base, exp − 1); power(base, 1) = base.'],
                 exam=[short('Write a recursive power(base, exponent).', 'public static int power(int base, int exponent) { if (exponent == 1) return base; return base * power(base, exponent - 1); }')], weight=3),
    }


class arrays_2d:
    AUTO_SLIDES = True
    DECK = {'key': 'arrays-2d', 'slug': '11-multidimensional-arrays', 'file': 'multidimensional-arrays', 'title': 'Multidimensional Arrays',
            'chapter': 'Chapter 8', 'pdf': '/academics/computer-science/cs102/slides/chapter-8/',
            'lede': 'Declaring and creating 2D arrays, initializers, lengths, ragged arrays, the processing loops (input, random, print, sum, column sums), passing 2D arrays to methods, and 3D arrays.'}
    ANN = {
        1: dict(kind='title', title='Multidimensional Arrays', body=[], sub='CS102 · Liang, Chapter 8'),
        4: dict(notes=['int[][] matrix = new int[5][5]; matrix[0][0] = 3;']),
        8: dict(notes=['matrix.length = number of rows; matrix[0].length = columns of row 0.'],
                exam=[mcq('For int[][] m = new int[3][4];, m.length and m[0].length are:', ['3 and 4', '4 and 3', '12 and 4', '3 and 3'], 0, '')], weight=3),
        10: dict(notes=['Ragged arrays: rows of different lengths: new int[5][] then each row separately.'], weight=2),
        16: dict(notes=['Sum all: nested for over rows and columns.']),
        17: dict(notes=['Column sums: outer loop over columns, inner over rows.'],
                 exam=[short('Write code that sums each column of int[][] m.', 'for (int c = 0; c < m[0].length; c++) { int total = 0; for (int r = 0; r < m.length; r++) total += m[r][c]; System.out.println(total); }')], weight=3),
        18: dict(notes=['Pass a 2D array: public static int sum(int[][] m).']),
        19: dict(notes=['3D arrays: double[][][] scores = new double[6][5][2];']),
    }


DECKS_HERE = [inheritance, polymorphism, recursion, arrays_2d]

"""CS102 annotated slides — Classes, Interfaces (Comparable/Comparator), Files, Generics.

One module holds several short decks: each deck is a namespace class with DECK and ANN (and
AUTO_SLIDES). Slides without an ANN entry are shown without notes. See
cs331_annotated/ch01_1_introduction.py for the ANN keys."""
from .common import mcq, scen, short, tf, tip, trap, trick


class classes:
    AUTO_SLIDES = True
    DECK = {'key': 'classes', 'slug': '01-classes', 'file': 'classes', 'title': 'Classes and Objects', 'chapter': 'Classes',
            'pdf': '/academics/computer-science/cs102/slides/classes/',
            'lede': ('Classes as blueprints, instance variables and methods, constructors and overloading, information hiding '
                     'and encapsulation (private + getters/setters), this, static variables and methods, toString, equals, '
                     'copy constructors and composition (has-a), built up through three versions of a Student class.')}
    ANN = {
        1: dict(kind='title', title='Classes and Objects', body=[], sub='CS102'),
        4: dict(notes=['A class is the blueprint; an object is one instance built from it.'],
                exam=[mcq('A class is best described as:', ['A blueprint for creating objects', 'An instance of an object', 'A method', 'A variable'], 0, '')], weight=2),
        9: dict(notes=['Attributes (instance variables) hold an object’s state; methods are its behaviour.']),
        12: dict(notes=['Constructor: same name as the class, NO return type (not even void), runs when you call new.'],
                 tips=[trap('Writing a return type (even void) makes it an ordinary method, not a constructor.')],
                 exam=[mcq('Which is true of a constructor?', ['It has the same name as the class and no return type', 'It must return void', 'It is called with the dot operator', 'A class can have only one'], 0, '')], weight=3),
        13: dict(notes=['If you write no constructor, Java supplies a no-argument default constructor.']),
        14: dict(notes=['Constructor overloading: several constructors with different parameter lists.'], weight=2),
        15: dict(notes=['Make attributes private (data hiding) and expose them through public methods.']),
        18: dict(notes=['Data hiding lets setters VALIDATE values (e.g., reject a negative age).'],
                 exam=[short('Why should instance variables be private?', 'So other classes can only change them through methods, which can validate the values (data validation) and hide the implementation; the class can then change internally without breaking its users.')], weight=3),
        19: dict(notes=['Encapsulation: hide the details, show only the interface (like a car’s pedals).']),
        20: dict(notes=['Recipe: private instance variables + public accessors (getters) and mutators (setters).'], weight=2),
        22: dict(notes=['this = the current object. Use it when a parameter has the same name as a field: this.name = name; and to call another constructor: this(...).'],
                 exam=[mcq('In a constructor with parameter name, which assigns the field?', ['this.name = name;', 'name = name;', 'name = this.name;', 'Student.name = name;'], 0, '')], weight=3),
        24: dict(notes=['static = one shared copy for the whole class; final = constant.']),
        25: dict(notes=['A static variable (e.g., count of Students) is shared by all objects; static final = constant.'],
                 exam=[mcq('A counter of how many Student objects have been created should be:', ['A static variable', 'An instance variable', 'A local variable', 'A final instance variable'], 0, '')], weight=3),
        27: dict(notes=['Static methods belong to the class, not an object (Math.max). They can’t use this or instance variables directly.'],
                 exam=[tf('A static method can directly access instance variables.', False, 'It has no object (no this).')], weight=3),
        30: dict(notes=['toString() returns a String describing the object; println(obj) calls it automatically.'], weight=2),
        31: dict(notes=['Object.equals compares REFERENCES; override it to compare contents (e.g., same ID).'],
                 tips=[trap('== on objects compares addresses; equals (if overridden) compares contents.')], weight=3),
        33: dict(notes=['Copy constructor: Student(Student s) builds a separate object with the same values.']),
        38: dict(notes=['Composition = has-a: a class holds an object of another class (Student has a Date).'],
                 tips=[trick('is-a → inheritance; has-a → composition.')],
                 exam=[mcq('A Student class with a Date birthDate field is an example of:', ['Composition (has-a)', 'Inheritance (is-a)', 'Polymorphism', 'Overloading'], 0, '')], weight=3),
    }


class interfaces:
    AUTO_SLIDES = True
    DECK = {'key': 'interfaces', 'slug': '02-comparable-comparator-and-interfaces', 'file': 'comparable-comparator-and-interfaces',
            'title': 'Comparable, Comparator and Interfaces', 'chapter': 'Interfaces',
            'pdf': '/academics/computer-science/cs102/slides/comparable-comparator-and-interfaces/',
            'lede': ('The Comparable interface and compareTo (negative / zero / positive), sorting objects with Arrays.sort, the '
                     'Fruit and Person examples, and the Comparator interface (compare, equals) for sorting by different '
                     'attributes such as grade or name.')}
    ANN = {
        4: dict(notes=['Comparable imposes a natural ordering; it has one method: compareTo.']),
        6: dict(notes=['a.compareTo(b) returns NEGATIVE if a comes before b, ZERO if equal, POSITIVE if a comes after b.'],
                exam=[mcq('"apple".compareTo("orange") returns:', ['A negative number', 'Zero', 'A positive number', 'true'], 0, '')], weight=3),
        7: dict(notes=['Person implements Comparable<Person> and compares by age: return this.age - other.age;']),
        10: dict(notes=['Arrays.sort calls compareTo on the objects, so they must implement Comparable.'],
                 exam=[tf('Arrays.sort can sort an array of your own class even if it doesn’t implement Comparable (and no Comparator is given).', False, 'It throws ClassCastException.')], weight=3),
        15: dict(notes=['Comparator (java.util) defines compare(a, b) and equals; use it for orderings other than the natural one.']),
        16: dict(notes=['compare(obj1, obj2): 0 if equal, positive if obj1 > obj2, negative otherwise.']),
        17: dict(notes=['Use Comparator to sort by different attributes: Arrays.sort(students, new GradeComparator()).'],
                 tips=[trick('Comparable = ONE built-in order inside the class. Comparator = MANY orders in separate classes.')],
                 exam=[mcq('To sort students sometimes by name and sometimes by grade, you should use:', ['Separate Comparator classes', 'One compareTo method', 'The equals method', 'A static variable'], 0, '')], weight=3),
    }


class files:
    AUTO_SLIDES = True
    DECK = {'key': 'files', 'slug': '03-files', 'file': 'files', 'title': 'Files', 'chapter': 'Files',
            'pdf': '/academics/computer-science/cs102/slides/files/',
            'lede': 'Reading files with Scanner, writing with FileWriter/PrintWriter, and splitting lines with String.split.'}
    ANN = {
        1: dict(kind='title', title='Files Revision', body=[], sub='CS102', notes=['Remember Integer.parseInt(string) to turn text fields into numbers.']),
        3: dict(notes=['FileWriter writes characters; new FileWriter(name, true) APPENDS instead of overwriting.'],
                exam=[mcq('new FileWriter("data.txt", true) will:', ['Append to the file', 'Overwrite the file', 'Read the file', 'Delete the file'], 0, '')], weight=2),
        5: dict(notes=['split(regex) returns a String[] of the pieces: "a,b,c".split(",") → ["a", "b", "c"].'],
                exam=[mcq('"Ali:20:A".split(":") returns an array of length:', ['3', '2', '1', '6'], 0, '')], weight=3),
        6: dict(notes=['Read a line, split it, parse the numeric fields, display.']),
    }


class generics:
    AUTO_SLIDES = True
    DECK = {'key': 'generics', 'slug': '04-generic-classes', 'file': 'generic-classes', 'title': 'Generic Classes and Methods', 'chapter': 'Generics',
            'pdf': '/academics/computer-science/cs102/slides/generic-classes/',
            'lede': ('Why generics (one method or class for many types, checked at compile time), generic methods such as '
                     'printArray and maximum, bounded type parameters (T extends Comparable<T>), and generic classes '
                     'like Sample<T> and LinkedList<E>.')}
    ANN = {
        3: dict(notes=['Generic methods and classes: one declaration for a set of related types, with compile-time type safety.'], weight=2),
        4: dict(notes=['Motivation: three overloaded printArray methods differ only in the element type → one generic method.']),
        5: dict(notes=['A generic method declares its type parameter before the return type: public static <T> void printArray(T[] a).'],
                exam=[mcq('Which header declares a generic method?', ['public static <T> void print(T[] a)', 'public static void <T> print(T[] a)', 'public static void print(<T> a)', 'public <T> static void print(T a)'], 0, '')], weight=3),
        7: dict(notes=['To compare with >, the type must be bounded: <T extends Comparable<T>> T maximum(T x, T y, T z).'], weight=3),
        10: dict(notes=['Comparable is the upper bound; the default bound is Object. extends is used even for interfaces.'],
                 exam=[tf('In a bounded type parameter you write implements for interfaces, e.g. <T implements Comparable<T>>.', False, 'Always extends.')], weight=3),
        13: dict(notes=['Generic class: class Sample<T> { private T data; … }']),
        14: dict(notes=['Sample<String> s = new Sample<String>(); — the type argument can’t be primitive (use Integer, not int).'],
                 exam=[mcq('Which is NOT allowed as a type argument?', ['int', 'Integer', 'String', 'Double'], 0, '')], weight=3),
        17: dict(notes=['LinkedList<E> is a generic class; E is the element type.']),
    }


DECKS_HERE = [classes, interfaces, files, generics]

"""CS101 annotated slides — Chapter 1: Introduction to Computers, Programs, and Java.

The Liang decks put a picture on every slide, so AUTO_SLIDES shows each slide as the original image;
the notes and questions sit beside it. See cs331_annotated/ch01_1_introduction.py for the ANN keys."""
from .common import mcq, scen, short, tf, tip, trap, trick

AUTO_SLIDES = True

DECK = {
    'key': 'ch1',
    'slug': '01-introduction-to-computers-programs-and-java',
    'file': 'introduction-to-computers-programs-and-java',
    'title': 'Introduction to Computers, Programs, and Java',
    'chapter': 'Chapter 1',
    'pdf': '/academics/computer-science/cs101/slides/chapter-1/',
    'lede': ('Computer basics (CPU, memory, storage, I/O), software and operating systems, machine vs. assembly vs. '
             'high-level languages, compilers vs. interpreters, why Java and how a Java program is written, '
             'compiled to bytecode and run on the JVM, the anatomy of a program, style, and the three kinds of '
             'programming errors.'),
}

ERRORS = 'Three error types: SYNTAX (compiler catches it: missing ;, misspelled keyword) · RUNTIME (program crashes while running: divide by zero, bad input) · LOGIC (runs but gives the wrong answer).'

ANN = {
    1: dict(kind='title', title='Introduction to Computers, Programs, and Java', body=[], sub='CS101 · Chapter 1', tips=[tip(ERRORS)]),
    2: dict(notes=['Computer basics → programs and languages → Java → first program → errors.']),
    3: dict(notes=['A computer = CPU, memory, storage devices, input and output devices, communication devices, connected by the bus.']),
    4: dict(notes=['CPU: fetches instructions from memory and executes them. Two parts: control unit and arithmetic/logic unit. Speed in hertz (GHz).'],
            exam=[mcq('The part of the computer that retrieves and executes instructions is the:', ['CPU', 'Memory', 'Hard disk', 'Monitor'], 0, '')], weight=2),
    5: dict(notes=['Memory (RAM): ordered bytes holding data and program instructions; a byte = 8 bits; each byte has an address.'],
            exam=[mcq('One byte is:', ['8 bits', '4 bits', '16 bits', '1024 bits'], 0, '')], weight=2),
    6: dict(notes=['Everything is stored as bits (0 and 1), because digital devices have two stable states (on/off). Encoding schemes map characters to bits.']),
    7: dict(notes=['Memory is VOLATILE (lost when power is off); storage devices (disks, CDs/DVDs, USB flash) keep data permanently. Programs are loaded from storage into memory to run.'],
            exam=[tf('Memory (RAM) keeps its data when the power is turned off.', False, 'It is volatile.')], weight=2),
    8: dict(notes=['Monitor quality depends on resolution and dot pitch.']),
    9: dict(notes=['Resolution = number of pixels; dot pitch = space between pixels (smaller is sharper).']),
    10: dict(notes=['Communication devices: modem, DSL, cable modem, NIC (LAN), wireless.']),
    11: dict(notes=['Software = programs = instructions to the computer, written in programming languages.']),
    12: dict(notes=['Two kinds of software: system software (OS, utilities) and application software (word processors, games).']),
    13: dict(notes=['Same slide continued.']),
    14: dict(notes=['The OS manages and controls the computer’s activities: allocates resources, schedules operations, controls hardware.'],
             exam=[mcq('Which program manages and controls a computer’s activities?', ['The operating system', 'The compiler', 'The web browser', 'The text editor'], 0, '')], weight=2),
    15: dict(notes=['Machine language: the CPU’s native binary instructions. Hard to read and write.']),
    16: dict(notes=['Assembly language: mnemonics (ADDF3 R1, R2, R3) translated by an ASSEMBLER into machine code; still machine-dependent.']),
    17: dict(notes=['High-level languages: English-like, portable (area = 5 * 5 * 3.1415;).'],
             exam=[mcq('Which language is machine-independent and English-like?', ['High-level language', 'Assembly language', 'Machine language', 'Binary code'], 0, '')], weight=2),
    18: dict(notes=['Popular high-level languages: Ada, BASIC, C, C++, C#, COBOL, Fortran, Java, Pascal, Python, Visual Basic.']),
    19: dict(notes=['Source code must be translated: by an INTERPRETER or a COMPILER.']),
    20: dict(notes=['Interpreter: translates and executes ONE statement at a time.']),
    21: dict(notes=['Compiler: translates the WHOLE program into machine code first, then it runs.'],
             tips=[trick('Interpreter = live translator, line by line. Compiler = translates the whole book first.')],
             exam=[mcq('Which translator converts the entire source program into machine code before execution?', ['Compiler', 'Interpreter', 'Assembler', 'Linker'], 0, '')], weight=3),
    22: dict(notes=['Java: general-purpose, runs on servers, desktops and mobile; “write once, run anywhere”.']),
    23: dict(notes=['Java can build standalone apps, applets, servlets, Android apps.']),
    24: dict(notes=['James Gosling at Sun Microsystems; originally Oak (1991), renamed Java (1995).']),
    25: dict(notes=['Java characteristics: simple, object-oriented, distributed, interpreted, robust, secure, architecture-neutral, portable, high-performance, multithreaded, dynamic.']),
    26: dict(notes=['Characteristics, continued.']), 27: dict(notes=['Characteristics, continued.']), 28: dict(notes=['Characteristics, continued.']),
    29: dict(notes=['Characteristics, continued.']), 30: dict(notes=['Characteristics, continued.']), 31: dict(notes=['Characteristics, continued.']),
    32: dict(notes=['Characteristics, continued.']), 33: dict(notes=['Characteristics, continued.']), 34: dict(notes=['Characteristics, continued.']),
    35: dict(notes=['Characteristics, continued.']), 36: dict(notes=['Characteristics, continued.']),
    37: dict(notes=['IDEs: NetBeans, Eclipse, IntelliJ.']),
    38: dict(notes=['First program: public class Welcome { public static void main(String[] args) { System.out.println("Welcome to Java!"); } }']),
    39: dict(notes=['Create (editor) → compile (javac Welcome.java → Welcome.class bytecode) → run (java Welcome on the JVM).'],
             exam=[mcq('Compiling Welcome.java produces:', ['Welcome.class (bytecode)', 'Welcome.exe', 'Welcome.obj', 'Welcome.txt'], 0, ''),
                   mcq('Java bytecode is executed by the:', ['Java Virtual Machine (JVM)', 'CPU directly', 'Compiler', 'Operating system shell'], 0, '')],
             weight=3),
    40: dict(notes=['Bytecode is platform-independent; any machine with a JVM can run it.'], weight=2),
    41: dict(notes=['Trace: the program starts at main.']), 42: dict(notes=['Trace: println executes.']), 43: dict(notes=['Trace: output appears.']),
    44: dict(notes=['Anatomy: class name, main method, statements, statement terminator, reserved words, comments, blocks.']),
    45: dict(notes=['Every program has at least one class; class names start with a capital letter (Welcome).']),
    46: dict(notes=['The program starts executing at main: public static void main(String[] args).']),
    47: dict(notes=['A statement is an action; System.out.println displays a string.']),
    48: dict(notes=['Every statement ends with a semicolon.']),
    49: dict(notes=['Reserved words (keywords) have special meaning and can’t be used as identifiers: class, public, static, void.'],
             exam=[mcq('Which is a Java reserved word?', ['static', 'Welcome', 'main', 'String'], 0, '')], weight=2),
    50: dict(notes=['A pair of braces forms a block (class block, method block).']),
    51: dict(notes=['Special symbols: { } ( ) ; // " ".']),
    52: dict(notes=['{ } — denotes a block.']), 53: dict(notes=['( ) — used with methods.']), 54: dict(notes=['; — ends a statement.']),
    55: dict(notes=['// — line comment (/* */ block comment).']), 56: dict(notes=['" " — encloses a string.']),
    57: dict(notes=['Program with three println messages.']), 58: dict(notes=['Printing the result of an expression: (10.5 + 2 * 3) / (45 - 3.5).']),
    59: dict(notes=['Style: comments, naming conventions, indentation, block style.']),
    60: dict(notes=['Comment the program’s purpose and key steps.']),
    61: dict(notes=['Naming: meaningful names; classes Capitalized (ComputeArea).']),
    62: dict(notes=['Indent each nested level (two spaces); spaces around operators.']),
    63: dict(notes=['Block styles: next-line vs. end-of-line braces; be consistent.']),
    64: dict(notes=['Three kinds of errors.'], tips=[tip(ERRORS)]),
    65: dict(notes=['Syntax (compile) errors: detected by the compiler.'],
             exam=[mcq('A missing semicolon is a:', ['Syntax error', 'Runtime error', 'Logic error', 'No error'], 0, '')], weight=3),
    66: dict(notes=['Runtime errors: the program aborts while running (e.g., dividing an int by zero).'],
             exam=[mcq('int x = 1 / 0; compiles but crashes when run. This is a:', ['Runtime error', 'Syntax error', 'Logic error', 'Warning'], 0, '')], weight=3),
    67: dict(notes=['Logic errors: the program runs but gives wrong results (e.g., Celsius conversion with integer 5 / 9 = 0).'],
             exam=[mcq('A program converting temperatures prints the wrong value but does not crash. This is a:', ['Logic error', 'Syntax error', 'Runtime error', 'Compilation error'], 0, '')], weight=3),
}

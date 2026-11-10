@head Chapter 3
@title Dependency Management, Exception Handling and Logging
@sources chapter-3-dependency-management-exception-handling-and-logging
@count 105
@tldr Maven downloads your libraries and builds your project in fixed phases; exceptions let a program recover from errors instead of crashing; logging records what happened so you can debug it later.
@why These are the three things that separate a homework program from real software. Exams love the checked-vs-unchecked split, tracing a try/catch/finally flow, the order of the Maven phases, and "exception or assertion?" questions. All four are worked through on this page.
@connect Chapter 1's `mvn clean verify` and JUnit both come from Maven. Exceptions return in Chapter 5 (InterruptedException), and Chapter 6's Spring Boot is configured with Maven. Chapter 7 says never to log secrets or show stack traces to users.
@goals
- Explain what dependency management is and why Maven automates it
- List the Maven default lifecycle phases in order
- Classify exceptions as checked or unchecked using the hierarchy
- Use try, catch, finally, throw and throws correctly
- Trace a try/catch/finally program
- Write a custom exception class
- Choose between exceptions and assertions
- Use log levels and explain SLF4J
@vocab
Dependency | A library your project needs in order to compile or run.
POM | pom.xml: Maven's project file listing dependencies and plugins.
GAV | groupId, artifactId, version: how Maven identifies a library.
Checked exception | Checked by the compiler; must be caught or declared.
Unchecked exception | RuntimeException, Error and their subclasses; not checked by the compiler.
Assertion | A boolean statement that should always be true; checks your own logic.
Facade | A simple front that hides the system behind it (SLF4J).
@map
5-9 | Dependency management, Maven, POM | MEMORIZE | Why and what
10-14 | Plugins and lifecycles | MEMORIZE | Phase order
15-26 | Maven in Eclipse, plugins, advantages | SKIM | Screenshots
27-43 | Exceptions: why, types, hierarchy | MEMORIZE | Checked vs unchecked
44-60 | Keywords, catch or declare, rethrow | WRITE | throw vs throws
61-72 | finally and the trace | WRITE | Trace exercises
73-82 | When to use, custom exceptions, best practice | MEMORIZE | Custom class code
83-93 | Assertions | MEMORIZE | Exception or assertion
94-104 | Logging, SLF4J, best practice | MEMORIZE | Levels and facade

## Dependency management and Maven | Slides 5-26 | must
**Dependency management** means identifying, tracking and controlling the libraries your project depends on. By hand that's slow and error-prone: you'd download each JAR, plus the JARs *those* need, and keep versions consistent. Tools such as **Maven** and **Gradle** automate it **declaratively**: you list what you need, and the tool fetches it.

::analogy A shopping list, not a shopping trip
Without Maven you drive to every shop yourself. With Maven you write a list (pom.xml), and everything, including the things your items need, is delivered to your door.
::

Maven uses a **Project Object Model**, the `pom.xml`, to centralize the build, reporting and documentation. It includes the POM, a set of standards, a project lifecycle, the dependency system, and plugins whose **goals** run at defined phases.

::code xml
<dependency>
    <groupId>org.slf4j</groupId>          <!-- organization -->
    <artifactId>slf4j-api</artifactId>    <!-- library name -->
    <version>2.0.9</version>              <!-- exact version -->
</dependency>
::

Those three tags are the **GAV**, and your own project has one too.

**Plugins** are scripts Maven executes. Each defines **goals**, such as `javafx:run`, the `site` goal (generates documentation) or the shade plugin's `shade` goal at the `package` phase (builds an executable JAR with its dependencies).

### Three built-in lifecycles
| Lifecycle | Job | Phases |
|---|---|---|
| **default** | Compile, package, deploy | validate → compile → test → package → verify → install → deploy |
| **clean** | Remove previous build output | pre-clean → clean → post-clean |
| **site** | Generate documentation | pre-site → site → post-site → site-deploy |

| Default phase | Does |
|---|---|
| validate | Checks the project is correct and dependencies are available |
| compile | Compiles source code |
| test | Runs unit tests (no packaging needed) |
| package | Builds the JAR or WAR |
| verify | Extra checks on the package |
| install | Copies it into your **local** repository |
| deploy | Pushes it to a **remote** repository for others |

::mnemonic Very Cool Teams Package Very Important Deliveries
**V**alidate, **C**ompile, **T**est, **P**ackage, **V**erify, **I**nstall, **D**eploy. Running a phase runs every phase before it, so `mvn install` also compiles and tests.
::
::trap install vs deploy
**install** = your machine's local repository. **deploy** = a remote repository shared with the team. Say "local" or "remote" in your answer.
::

Advantages from the slides: simple dependency management, multi-module projects, consistent builds, easy to learn (declarative XML), and strong community support.

::key
- Dependency management tracks and controls the libraries a project needs
- Maven declares them in pom.xml using groupId, artifactId and version
- Plugins define goals that run at lifecycle phases
- Default lifecycle: validate, compile, test, package, verify, install, deploy
- install is local; deploy is remote
::

## What exceptions are and their types | Slides 27-43 | must
An **exception** is an event that disrupts the normal flow of a program; in Java it's an **object thrown at run time**. Without handling, a runtime error **terminates the program abnormally**. Exception handling lets the program **continue or terminate gracefully**.

| Common exception | Typical cause |
|---|---|
| ArithmeticException | Divide by zero |
| NullPointerException | Using a variable that is null |
| NumberFormatException | `Integer.parseInt("abc")` |
| ArrayIndexOutOfBoundsException | Index past the end of an array |
| InputMismatchException | Scanner expected an int, got text |

**Why not just use if/else?** For a divide by zero you can, because you know what might go wrong. But when you connect to a database, write a file or read hardware, you can't predict every failure. Exceptions let the method that *detects* the error hand it to the code that knows how to *handle* it.

### The hierarchy
::graph Java exception hierarchy | directed
n obj 300 30 Object
n thr 300 95 Throwable
n err 140 165 Error\nunchecked ~
n exc 460 165 Exception
n rte 360 240 RuntimeException\nunchecked ~
n chk 580 240 IOException,\nClassNotFound\nchecked *
n vm 140 240 VirtualMachineError,\nLinkageError ~
n npe 360 320 NullPointer, Arithmetic,\nIndexOutOfBounds ~
e obj thr
e thr err
e thr exc
e exc rte
e exc chk
e err vm
e rte npe
::

| Branch | Meaning | Handle it? |
|---|---|---|
| **Error** | System errors thrown by the JVM, such as running out of memory | Rarely; little you can do |
| **RuntimeException** | Programming logic errors (null, bad index, divide by zero) | Fix the code |
| **Other Exception** subclasses | Outside conditions (missing file, network) | Must catch or declare |

::formula The rule
Unchecked = RuntimeException + Error + their subclasses
Checked   = every other Exception
::
::analogy Weather vs your own mistakes
A **checked** exception is like rain: it comes from outside and you can't prevent it, so Java makes you bring an umbrella (catch or declare). An **unchecked** exception is like tripping on your own shoelace: the fix is to tie your shoes (fix the code), not to carry a stretcher everywhere.
::
::trap ClassNotFoundException is checked
It's a sibling of IOException, not under RuntimeException. NullPointerException, ArithmeticException and IndexOutOfBoundsException are the unchecked ones.
::
::key
- An exception is an object thrown at run time that disrupts normal flow
- Handling lets the program continue or end gracefully
- Error and RuntimeException (and subclasses) are unchecked
- All other exceptions are checked: catch or declare them
- Checked exceptions come from outside conditions; unchecked from logic errors
::

## throw, throws, try and catch | Slides 44-60 | must
| Keyword | Where | Does |
|---|---|---|
| `try` | Around risky code | Must be followed by catch or finally |
| `catch` | After try | Handles one exception type |
| `finally` | After try/catch | Always runs |
| `throw` | Inside a method body | **Throws** one exception object now |
| `throws` | In the method signature | **Declares** what the method might throw |

::code java
public void checkAge(int age) {
    if (age < 18) throw new IllegalArgumentException("You must be 18 or older");
    System.out.println("You can enter.");
}

public void readFile() throws IOException {      // declares
    FileReader file = new FileReader("data.txt");
}
::
::mnemonic throwS = Signature
The one with the **s** goes in the **s**ignature and can list **s**everal types. `throw` (no s) throws **one** object.
::

**Catch or declare.** If `p2()` declares `throws IOException`, any caller `p1()` must either wrap the call in try/catch **or** declare `throws IOException` itself. For an **unchecked** exception the caller can call it with neither.

::code java
void p1() {                          // (a) catch it
    try { p2(); }
    catch (IOException ex) { ... }
}
void p1() throws IOException {       // (b) pass it up
    p2();
}
::

**How the catch is found.** When an exception is thrown, Java looks for a matching catch in the current method. If none, the method ends and Java checks its caller, then that method's caller, down the call stack to main. If nobody catches it, the program terminates.

**Rethrowing**: a catch block that can't fully handle the exception can do something (such as log it) and then `throw ex;` so a higher level handles it.

::trap Order of catch blocks
List the **specific** exceptions first. `catch (Exception e)` before `catch (IOException e)` makes the second block unreachable, which is a compile error.
::
::check `setRadius` throws IllegalArgumentException for a negative value. Must callers use try/catch?
No. IllegalArgumentException extends RuntimeException, so it's unchecked. They may catch it, but the compiler doesn't force them to.
::
::key
- throw throws one exception object; throws declares possible exceptions
- A checked exception must be caught or declared by every caller
- Java searches up the call stack for a matching catch
- Rethrow when a catch block can only partly handle the error
- Order catch blocks from specific to general
::

## The finally clause: tracing execution | Slides 61-72 | must
**finally always runs**, whether or not an exception was thrown, and whether or not it was caught.

::steps Case 1: no exception
All try statements run.
catch is skipped.
**finally runs.**
The next statement after the block runs.
::
::steps Case 2: exception thrown and caught
statement2 throws Exception1, so statement3 is **skipped**.
The matching catch(Exception1) handles it.
**finally runs.**
The next statement after the block runs.
::
::steps Case 3: caught, then rethrown
statement2 throws Exception2; catch(Exception2) handles it and does `throw ex;`.
**finally still runs.**
Control goes to the **caller**; the "next statement" in this method is **not** run.
::
::analogy Locking the door on the way out
Whatever happens inside the house (a normal day, a burnt dinner you dealt with, or a fire that sends you running) you always lock the door as you leave. That's finally, which is why it's used to close files, database connections and sockets.
::
::check In Case 3, list what runs after statement2 throws.
The catch(Exception2) block, then finally, then control jumps to the caller. statement3 and "Next statement" don't run.
::
::key
- finally always runs: no exception, caught, or rethrown
- Statements after the throwing line in try are skipped
- After a rethrow, the next statement in the method does not run
- Use finally to release resources
::

## Using exceptions well | Slides 73-82 | must
**Cost.** Exception handling separates error code from normal code, which makes programs easier to read. But it costs time and resources: an exception object must be created and the call stack searched.

**When to throw**: if the caller should decide what to do, throw. If you can handle it right there, don't throw.

**When to use try/catch**: for **unexpected** conditions only. For simple, expected situations, use an if:

::code java
// Wrong: try/catch for an expected case
try { System.out.println(refVar.toString()); }
catch (NullPointerException ex) { System.out.println("refVar is null"); }

// Right
if (refVar != null) System.out.println(refVar.toString());
else System.out.println("refVar is null");
::

### Custom exceptions
Extend **Exception** for a checked exception or **RuntimeException** for an unchecked one. Use Java's built-in classes when they fit; write your own when you need to carry extra information to the handler.

::code java
public class InvalidRadiusException extends Exception {
    private double radius;
    public InvalidRadiusException(double radius) {
        super("Invalid radius " + radius);
        this.radius = radius;
    }
    public double getRadius() { return radius; }
}

public void setRadius(double newRadius) throws InvalidRadiusException {
    if (newRadius >= 0) radius = newRadius;
    else throw new InvalidRadiusException(newRadius);
}
::

The handler can now call `ex.getRadius()` to see the bad value.

| Best practice | Why |
|---|---|
| Catch only what you can handle | Catching `Exception` can hide bugs |
| Use specific types | `FileNotFoundException`, not `Exception` |
| Don't swallow exceptions | An empty catch hides the failure; at least log it |
| Use finally for resources | Files, connections and sockets always get closed |

::trap The empty catch block
`catch (Exception e) { }` is the worst option: the program carries on as if nothing happened, and nobody ever learns why the data is wrong.
::
::key
- Exceptions cost time, so use them for unexpected conditions
- Use an if for simple, expected cases such as null checks
- Custom exceptions extend Exception (checked) or RuntimeException (unchecked)
- Custom exceptions can carry data, such as the bad radius
- Catch specific types, never swallow, and close resources in finally
::

## Assertions | Slides 83-93 | know
An **assertion** states an assumption that should be true while the program runs. If it's false, Java throws an **AssertionError**.

::code java
assert i == 10;
assert sum > 10 && sum < 5 * 10 : "sum is " + sum;   // with a detail message
::

Assertions are **disabled by default**. Enable them with `java -ea AssertionDemo` (`-da` disables). They can be switched on or off by class or package.

| | Assertions | Exception handling |
|---|---|---|
| Purpose | Check **your own logic** is correct | Deal with **unusual run-time circumstances** |
| Can be switched off? | Yes, at startup | No |
| Use for public method arguments? | **Never** | Yes |

::trap Never check public arguments with assert
A public method's valid inputs are part of its contract, which must hold even when assertions are disabled. Validate public arguments with an exception (IllegalArgumentException) instead.
::
::tip A good use of assert
A switch with all 12 months as cases can have `default: assert false : "Invalid month: " + month;`, which flags something you believed impossible.
::
::key
- An assertion checks an assumption; a false one throws AssertionError
- Assertions are off by default; enable them with -ea
- Assertions check program logic; exceptions handle run-time problems
- Never use assertions to check public method arguments
::

## Logging | Slides 94-104 | must
**Logging** records information about program execution, errors and important events at run time. It helps you debug, monitor applications and understand program flow, especially in production where you can't attach a debugger.

| Level | Use for |
|---|---|
| **SEVERE** (error) | Critical issues such as a crash |
| **WARNING** | Potential problems, such as a deprecated method |
| **INFO** | General information, such as startup |
| **DEBUG** | Details for debugging |
| **TRACE** | Very fine-grained flow |

::mnemonic Should We Investigate Deeper Today?
**S**EVERE, **W**ARNING, **I**NFO, **D**EBUG, **T**RACE: from most serious to most detailed.
::

### SLF4J: a facade
**SLF4J** (Simple Logging Facade for Java) is one API for logging that hides which logging framework actually does the work: **Logback**, **Log4j** or java.util.logging. You write code against SLF4J and choose the backend at deployment by changing a Maven dependency, without editing code.

::analogy A universal TV remote
SLF4J is a universal remote: you press the same buttons no matter which TV brand (Logback, Log4j) is plugged in. Swap the TV and your fingers do exactly the same thing.
::
::code java
private static final Logger logger = LoggerFactory.getLogger(SLF4JExample.class);

logger.info("Application has started");
logger.debug("Debugging an issue");
logger.warn("This is a warning message");
logger.error("An error has occurred");
::

In Maven you add **slf4j-api** (the facade) and **logback-classic** (the implementation). **Logback** succeeded Log4j, from the same team as SLF4J, with better performance and easier configuration.

| Logging best practice | |
|---|---|
| Right level | Errors at SEVERE, routine at INFO |
| **Never log sensitive data** | No passwords, keys or private user data |
| Structured logs | JSON makes logs easy to search |
| Watch performance | Don't log heavily inside hot loops; use asynchronous logging |

::key
- Logging records run-time events for debugging and monitoring
- Levels: SEVERE, WARNING, INFO, DEBUG, TRACE
- SLF4J is a facade over Logback, Log4j and others
- Switch backends by changing a dependency, not code
- Never log passwords, keys or private data
::
@cheat
### Maven
- pom.xml, GAV
- Plugins → goals
- validate, compile, test, package, verify, install, deploy
- install = local, deploy = remote
- clean and site lifecycles
### Exception types
- Unchecked: RuntimeException, Error
- Checked: all other Exceptions
- Checked = catch or declare
### Keywords
- throw: one object, in body
- throws: signature, declares
- finally: always runs
- Specific catch blocks first
### Using them
- try/catch for unexpected only
- Custom: extends Exception / RuntimeException
- Don't swallow; close in finally
### Assertions
- assert cond : msg
- Off by default; -ea
- Never for public arguments
### Logging
- SEVERE, WARNING, INFO, DEBUG, TRACE
- SLF4J facade → Logback / Log4j
- Never log secrets
@mcq 12
Which is the correct order of Maven default phases?
+ validate, compile, test, package, verify, install, deploy
- compile, validate, test, package, install, verify, deploy
- validate, test, compile, package, verify, deploy, install
- compile, test, validate, package, verify, install, deploy
> Slide 12.
@mcq 12
Which Maven phase copies the packaged archive into the local repository?
+ install
- deploy
- package
- verify
> deploy pushes to a remote repository.
@mcq 10
In Maven, groupId, artifactId and version together identify:
+ A project or library
- A lifecycle phase
- A test case
- A log level
> The GAV coordinates.
@mcq 42
Which of these is a checked exception?
+ IOException
- NullPointerException
- ArithmeticException
- IndexOutOfBoundsException
> The other three extend RuntimeException.
@mcq 42
Unchecked exceptions are:
+ RuntimeException, Error and their subclasses
- Exception and all its subclasses
- Only Error
- Any exception declared with throws
> Slide 42.
@mcq 45
The keyword used in a method signature to declare possible exceptions is:
+ throws
- throw
- catch
- finally
> throw raises one object inside the body.
@mcq 55
Method p2 declares `throws IOException`. A caller p1 must:
+ Catch it in try/catch or declare throws IOException
- Do nothing
- Use an assertion
- Extend RuntimeException
> Catch or declare.
@mcq 63
When does the finally block run?
+ Always, whether or not an exception occurs
- Only if an exception occurs
- Only if no exception occurs
- Only if the exception is rethrown
> Slides 62-72.
@mcq 72
An exception is caught and rethrown in a catch block. What happens next?
+ finally runs, then control passes to the caller
- The next statement in the method runs
- The program restarts the try block
- finally is skipped
> Slide 72.
@mcq 76
For a possible null reference, the slides recommend:
+ An if statement checking for null
- Catching NullPointerException
- An assertion
- A custom checked exception
> Use exceptions for unexpected conditions only.
@mcq 77
To create a custom checked exception, extend:
+ Exception
- RuntimeException
- Error
- AssertionError
> RuntimeException would make it unchecked.
@mcq 91
Assertions should NOT be used to:
+ Check arguments of public methods
- Check internal assumptions
- Mark impossible switch cases
- Check loop results
> Public argument checks must work even when assertions are off.
@mcq 88
Assertions are enabled with:
+ java -ea
- java -da
- mvn assert
- They are always on
> Disabled by default.
@mcq 99
SLF4J is best described as:
+ A facade over logging frameworks such as Logback and Log4j
- A replacement for Maven
- A unit-testing framework
- A type of exception
> Slide 99.
@mcq 104
Which is a logging best practice?
+ Never log passwords or private keys
- Log everything at SEVERE
- Log inside every loop iteration
- Use empty catch blocks instead of logging
> Slide 104.
@short 42
Explain the difference between checked and unchecked exceptions, with one example of each.
~ compile time, catch or declare, RuntimeException, IOException, NullPointerException
> Checked exceptions are checked at compile time and must be caught or declared, for example IOException. Unchecked exceptions are RuntimeException, Error and their subclasses, which reflect logic errors and aren't enforced by the compiler, for example NullPointerException.
@short 69
In a try with statement1 to statement3, statement2 throws Exception2, which is caught and rethrown. Trace what executes.
~ statement3 skipped, catch, finally, caller, next statement
> statement1 runs, statement2 throws, statement3 is skipped. The catch(Exception2) block runs and rethrows. finally runs. Control passes to the caller, so the next statement in the method does not run.
@short 79
Write a custom exception that carries the invalid radius back to the caller.
~ extends Exception, field, constructor, super, getRadius
> class InvalidRadiusException extends Exception { private double radius; public InvalidRadiusException(double r) { super("Invalid radius " + r); radius = r; } public double getRadius() { return radius; } }

@head Chapter 1
@title Introduction to Software Construction
@sources chapter-1-introduction-to-software-construction
@count 64
@tldr Software construction is the hands-on part of building software: writing, testing and fixing code, and the whole craft comes down to keeping complexity under control.
@why This chapter sets the rules the rest of the course enforces: simple, readable code; Git to manage change; JUnit to prove the code works; and a firm habit of verifying anything an AI writes for you. The boundary-testing exercises at the end are exactly the kind of question you'll see on an exam.
@connect Chapters 2 to 7 are all techniques for writing code that stays simple: generics, exceptions, OO design, concurrency, frameworks and security. Chapter 1 explains why that matters.
@goals

- Define software construction and list what it involves
- Explain why managing complexity is the central technical challenge
- Apply KISS, guard clauses, good naming and "why" comments
- Explain parsing, compilation and interpretation
- Use the core Git commands and explain merging and branching
- Write JUnit tests, including boundary tests for AI-generated code
  @vocab
  Construction | Coding, verifying, debugging and integrating: the actual building of software.
  Complexity | How hard code is to understand and change safely.
  Refactor | Restructure code without changing what it does.
  AST | Abstract syntax tree: the tree a parser builds from code.
  Repository | Where version control stores every version of the code.
  Unit test | A small automated test of one piece of code.
  @map
  2-8 | What construction is, AI in the loop | MEMORIZE | Four activities; "verify the AI"
  9-22 | Managing complexity | MEMORIZE | KISS, naming, comments
  23-27 | Parsers and compilers | MEMORIZE | Compiled vs interpreted
  28-50 | Git and version control | WRITE | Commands, merge flow, branching
  51-57 | JUnit and TDD | WRITE | Red, Green, Refactor
  58-64 | Verify the AI exercises | WRITE | Boundary tests

## What software construction is | Slides 2-8 | must

Requirements come before, system testing after; **construction is where the software is actually created**. It is the detailed process of:

| Activity        | Meaning                                        |
| --------------- | ---------------------------------------------- |
| **Coding**      | Writing source code                            |
| **Verifying**   | Testing unit by unit to make sure it's correct |
| **Debugging**   | Finding and fixing errors                      |
| **Integrating** | Combining pieces into a working whole          |

Specific tasks include designing classes and routines, naming variables and constants, choosing control structures, unit and integration testing, reviewing code and tuning it.

::analogy Building a house
Requirements are the client's wish list and the architect's plan. Construction is the builders actually laying bricks and wiring, and checking each wall as they go.
::

**AI in the construction loop.** Assistants can now help with every activity: generating code, drafting tests, explaining errors, writing glue code. But **AI output is plausible, not guaranteed correct**. The developer's job shifts from typing to **specifying, reviewing and verifying**, and **you remain fully responsible for every line you submit**.

| Tool type         | Examples                       |
| ----------------- | ------------------------------ |
| Chat assistants   | ChatGPT, Claude, Gemini        |
| In-IDE completion | GitHub Copilot, Cursor         |
| Agentic tools     | Work across files on their own |

::mnemonic Clever Vets Diagnose It
**C**oding, **V**erifying, **D**ebugging, **I**ntegrating, in the order work flows.
::
::key

- Construction is the central activity of software development
- It covers coding, verifying, debugging and integrating
- AI output is plausible, not guaranteed correct
- You remain responsible for every line you submit
  ::

## Managing complexity | Slides 9-22 | must

**The biggest technical risk isn't not knowing the syntax; it's uncontrolled complexity.** If code is too complex, we can't understand it, change it or fix it safely. The slides call managing complexity **the most important technical topic in software development**.

The goal of every design technique: **break a complicated problem into simple pieces**, because several simple pieces are easier to understand than one complicated one.

### KISS: Keep It Simple and Straightforward

::code java
// Hard to read: deep nesting, magic number
public void process(int[] data) {
if (data != null) {
for (int i = 0; i < data.length; i++) {
if (data[i] > 100) {
System.out.println("Big: " + data[i]);
}
}
}
}

// Flatter and self-documenting
private static final int THRESHOLD = 100;
public void process(int[] data) {
if (data == null) return; // guard clause
for (int value : data) {
if (value > THRESHOLD) System.out.println("Big: " + value);
}
}
::

Two moves made the difference: a **guard clause** that exits early so the rest isn't nested, and a **named constant** instead of the magic number 100.

| Rule for simple code                | Why                                |
| ----------------------------------- | ---------------------------------- |
| Divide into small meaningful blocks | Each piece is understandable alone |
| Avoid duplication                   | One fix, not five                  |
| Refactor continuously               | Keep it clean as it grows          |
| Delete what has no purpose          | Less to read and maintain          |

### Readable code: written for people first

Readability improves comprehension, review, debugging and modification, and lowers the error rate.

| Naming rule               | Good                 | Bad         |
| ------------------------- | -------------------- | ----------- |
| Full, pronounceable words | `customerCount`      | `cc`        |
| Booleans as questions     | `isValid`, `hasNext` | `flag`      |
| Verbs for methods         | `calculateTotal()`   | `total()`   |
| Nouns for classes         | `Invoice`            | `DoInvoice` |

**Comments explain WHY, not WHAT.** `i++; // increment i` is noise. Use comments for intent, warnings and trade-offs the code can't show. A comment isn't a fix for unclear code: rewrite the code first.

::trap AI makes complexity worse, not better
AI produces lots of code quickly, often with abstraction the problem doesn't need. "It compiles and runs" doesn't mean "it's simple and maintainable". Apply KISS to what the AI over-builds.
::
::check Rewrite `if (user != null) { if (user.isActive()) { send(user); } }` using a guard clause.
`if (user == null || !user.isActive()) return;` then `send(user);`. One level of indentation instead of two.
::
::key

- Uncontrolled complexity is the biggest technical risk
- Break complicated problems into simple pieces
- KISS: guard clauses, named constants, small methods
- Name to reveal intent; comments explain why, not what
- Simplify AI-generated code that is over-built
  ::

## Parsers, compilers and interpreters | Slides 23-27 | know

| Term                              | What it does                                                                    |
| --------------------------------- | ------------------------------------------------------------------------------- |
| **Parser**                        | Turns text into a structured tree, the **abstract syntax tree (AST)**           |
| **Compiler**                      | Parses source code and translates it into machine-executable code ahead of time |
| **Interpreter**                   | Parses the source and executes it directly, simulating the computation          |
| **Parser generator** (e.g. ANTLR) | Takes a grammar definition and generates a parser program                       |

::analogy Translating a book or translating live
A **compiler** translates the whole book before anyone reads it. An **interpreter** translates sentence by sentence while you listen.
::
::key

- A parser builds an AST from text
- A compiler translates source to machine code ahead of time
- An interpreter executes the source directly
- ANTLR generates parsers from a grammar
  ::

## Version control with Git | Slides 28-50 | must

**Version control** keeps every historical version of the code, supports team collaboration, and makes build automation and continuous integration possible. **Git** is a distributed version control system; **GitHub** hosts Git repositories online.

Two philosophies for avoiding conflicts:

|          | Lock (check-out, edit, check-in)           | Copy, modify, merge                |
| -------- | ------------------------------------------ | ---------------------------------- |
| How      | You lock a file; nobody else can change it | Everyone edits; changes are merged |
| Downside | Others wait                                | Occasional merge conflicts         |

**Distributed**: every developer has a full clone. If the server goes down, people can keep working and sync with each other.

| Command      | Does                                           |
| ------------ | ---------------------------------------------- |
| `git clone`  | Downloads a repository                         |
| `git status` | Shows what changed                             |
| `git add`    | Stages changes for the next commit             |
| `git commit` | Saves staged changes as a new local version    |
| `git push`   | Uploads local commits to the remote            |
| `git pull`   | Downloads and merges the latest remote changes |

::steps Two people editing the same file (slides 38-41)
Both start in sync with the remote.
Both edit the file locally.
User A pushes first: it succeeds.
User B tries to push: it **fails**, because the remote moved on.
User B **pulls** A's changes and merges them (usually automatic).
User B pushes again: now it succeeds. Everyone pulls and is in sync.
::
::mnemonic Add, Commit, Push: "A Cat Purrs"
Your change goes **A**dd (stage), **C**ommit (save locally), **P**ush (share).
::

**Branching** lets you work on a copy without disturbing `main`. Keep `main` (or master) for production-ready code and do active work on a `dev` branch or feature branches, merging back when finished. A strategy such as **GitFlow** organizes this for teams.

**Code review**: most defects are found by people reading code, not running it. Review small changes often.

::trap Never commit secrets
An assistant might echo back API keys or passwords. Keep AI changes in small, reviewable commits and add tool artifacts and local config to `.gitignore`.
::
::key

- Git is distributed; every clone has full history
- add stages, commit saves locally, push shares, pull fetches and merges
- A push fails if the remote has changes you haven't pulled
- Keep main production-ready and work on branches
- Review code in small changes; never commit secrets
  ::

## Verifying with JUnit and TDD | Slides 51-64 | must

**JUnit** is the standard unit-testing framework for Java. For a class `A`, write a test class `ATest` with methods marked `@Test`.

::code java
public class UtilTest {
private Util calculator;

    @BeforeEach
    void setUp() { calculator = new Util(); }   // runs before every test

    @Test
    @DisplayName("Simple multiplication should work")
    void testMultiply() {
        assertEquals(20, calculator.multiply(4, 5));
    }

}
::

| Annotation                                    | Meaning               |
| --------------------------------------------- | --------------------- |
| `@Test`                                       | This method is a test |
| `@BeforeEach` (JUnit 5) / `@Before` (JUnit 4) | Runs before each test |
| `@DisplayName`                                | Readable test name    |

Common assertions: `assertEquals`, `assertTrue`, `assertFalse`.

**Test-driven development (TDD):**

::steps Red, Green, Refactor
**Red:** write a failing test for the next small behaviour.
**Green:** write the simplest code that makes it pass.
**Refactor:** clean up, with the test as a safety net.
::

### Verify the AI: test the boundaries

::example Exercise 1: "a student passes with a mark greater than or equal to 50"
The AI wrote `return mark > 50;`. Test 49, 50 and 51:

- 49 → should fail: passes the test.
- **50 → should pass: the test fails**, because `>` excludes 50.
- 51 → should pass: passes.

Fix: `return mark >= 50;`. The bug lives exactly on the boundary, which is why you always test the boundary value itself.
::
::example Exercise 2: "a username is valid if not empty and only letters"
The AI wrote `return username.matches("[a-zA-Z]+");`. Tests: "Asma" valid; "Asma Sattar" invalid; "" invalid; "Asma123" invalid; **null → crashes** with a NullPointerException.

Fix: check `if (username == null || username.isEmpty()) return false;` first.
::
::trap AI tests can share the AI's mistake
If the AI writes both the code and the tests, the tests may encode the same wrong assumption. Treat tests as **your** specification, and add your own edge cases: null, empty, boundaries, errors.
::
::mnemonic NEBE: Null, Empty, Boundary, Error
The four edge cases to add to every AI-generated test suite.
::
::key

- JUnit test classes use @Test methods and assertions
- @BeforeEach sets up fresh state before every test
- TDD: Red, Green, Refactor
- Always test boundary values such as 49, 50 and 51
- Add null, empty, boundary and error cases to AI tests
  ::
  @cheat

### Construction

- Coding, verifying, debugging, integrating
- AI output: plausible, not guaranteed
- You own every line

### Simple code

- KISS
- Guard clauses, named constants
- Small methods, no duplication
- Names reveal intent
- Comments: why, not what

### Tools

- Parser → AST
- Compiler: ahead of time
- Interpreter: runs directly

### Git

- clone, status, add, commit, push, pull
- Push fails until you pull
- main = production-ready

### JUnit

- @Test, @BeforeEach
- assertEquals / True / False
- TDD: Red, Green, Refactor
- Test null, empty, boundary, error
  @mcq 4
  Which is NOT one of the core activities of software construction?

* Requirements gathering

- Coding
- Debugging
- Verifying

> Requirements gathering happens before construction.
> @mcq 10
> According to the slides, the biggest technical risk in software development is:

- Uncontrolled complexity

* Not knowing the syntax
* Slow computers
* Too many comments

> Slide 10.
> @mcq 13
> KISS stands for:

- Keep It Simple and Straightforward

* Keep Integration Short and Safe
* Know Important Software Standards
* Keep Interfaces Small and Separate

> Slide 13.
> @mcq 14
> Returning early when input is invalid, to avoid nesting, is called a:

- Guard clause

* Magic number
* Lambda
* Merge

> Slide 14.
> @mcq 21
> Good comments should mainly explain:

- Why the code does something

* What each line does
* The name of each variable
* The date of each change

> Slide 21.
> @mcq 20
> Which is the best name for a boolean?

- isValid

* flag
* v
* validate

> Booleans read as questions.
> @mcq 24
> A parser transforms text into:

- An abstract syntax tree

* Machine code directly
* A Git commit
* A unit test

> Slide 24.
> @mcq 37
> Which command stages changes for the next commit?

- git add

* git push
* git pull
* git clone

> Slide 37.
> @mcq 39
> User B's push fails because User A pushed first. User B should:

- Pull and merge, then push again

* Delete the repository
* Force the push without merging
* Clone the repository again

> Slides 39 and 40.
> @mcq 43
> The main or master branch should hold:

- Production-ready code

* Experimental features
* Only documentation
* Each developer's private work

> Slide 43.
> @mcq 53
> The order of the TDD loop is:

- Red, Green, Refactor

* Green, Red, Refactor
* Refactor, Red, Green
* Red, Refactor, Green

> Slide 53.
> @mcq 60
> Requirement: pass if mark ≥ 50. The AI wrote `mark > 50`. Which test fails?

- 50

* 49
* 51
* 100

> 50 should pass but `>` excludes it.
> @short 60
> Explain why boundary testing matters for AI-generated code, using the pass mark example.
> ~ boundary, 50, >=, fails, edge
> AI code often gets the boundary condition wrong, such as using > instead of >=. Testing 49, 50 and 51 shows that 50 wrongly fails, which reveals the bug exactly at the boundary.
> @short 39
> Describe what happens when two developers edit the same file and push to a shared Git remote.
> ~ push, fails, pull, merge, sync
> The first push succeeds. The second fails because the remote has changed. The second developer pulls and merges the first one's changes, then pushes successfully, and both sync again.
> @short 13
> List three practices that keep code simple and readable.
> ~ guard clause, naming, duplication, small, comments
> Use guard clauses to avoid deep nesting, name things to reveal intent, and break code into small methods without duplication.

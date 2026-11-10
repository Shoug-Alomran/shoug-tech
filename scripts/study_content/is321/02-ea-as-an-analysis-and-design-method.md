@head Lecture 2
@title EA as an Analysis and Design Method
@sources lecture-2-ea-as-an-analysis-and-design-method
@count 31
@tldr The EA3 Cube organizes an enterprise along three dimensions, and comparing current and future views of it shows exactly what has to change.
@why The cube is the framework used throughout this course, and it comes back in Lectures 3, 5, 11 and 13. Students lose marks by mixing up levels, lines of business, components and threads, and slide 18 exists to untangle them. So does this page.
@connect Lecture 1 named the core elements. This lecture shows how the framework and documentation really work. Lecture 3 goes through each of the five levels.
@goals

- Describe the three dimensions of the EA3 Cube
- Name the six elements of EA analysis and design
- Distinguish current from future architecture
- Tell apart level, LOB, segment, component and thread
- Use the top-down questions for each level
  @vocab
  Sub-architecture | One of the five levels of the framework.
  Segment | A complete vertical slice for one line of business.
  Component | A changeable goal, process, standard or resource.
  Artifact | A document that describes a component.
  Reference architecture | Standards for one kind of capability across the enterprise.
  @map
  2-4 | The EA3 Cube and history | MEMORIZE | Three dimensions
  5-6 | Six elements of analysis and design | MEMORIZE | Name all six
  7-9 | The framework | MEMORIZE | Levels, segments, artifacts
  10-11 | Components | MEMORIZE | Vertical vs crosscutting
  12-15 | Current, future, management plan | MEMORIZE | 1-2 year and 3-10 year horizons
  16-17 | Threads | MEMORIZE | Security, standards, skills
  18-19 | Term comparison | MEMORIZE | Slide 18 is key
  20-27 | Questions at each level | WRITE | Questions per level
  28-30 | The repository | SKIM | Returns in Lecture 5

## The EA3 Cube | Slides 2-9 | must

The EA3 Cube is a **three-dimensional way to document an entire enterprise**, so that top managers can see how the organization works and how technology connects to strategy.

| Dimension        | What it is                           | Examples                        |
| ---------------- | ------------------------------------ | ------------------------------- |
| **1. Levels**    | Five hierarchical sub-architectures  | Goals down to infrastructure    |
| **2. Segments**  | Lines of business (functional areas) | Finance, HR, Admissions         |
| **3. Artifacts** | Documentation at each level          | Strategic plan, data dictionary |

::graph The five levels, from top to bottom | directed
n a 150 0 Goals & Initiatives
n b 150 60 Products & Services
n c 150 120 Data & Information
n d 150 180 Systems & Applications
n e 150 240 Networks & Infrastructure
e a b
e b c
e c d
e d e
::

Through every level run three **threads**: Security, Standards and Skills.

::mnemonic Good People Do Serious Networking
The levels, top to bottom and in order: **G**oals, **P**roducts, **D**ata, **S**ystems, **N**etworks.
::
::analogy A block of flats
Each **floor** is a level. Each **vertical column of flats** is a line of business. The **lift shaft and wiring** running through all floors are the threads. The **floor plans** on file are the artifacts.
::
::key

- The cube has three dimensions: levels, segments, artifacts
- Five levels run from goals to infrastructure
- Security, standards and skills are threads through all levels
  ::

## The six elements of analysis and design | Slides 5-6, 10-17 | must

| Element                     | Meaning                                                  |
| --------------------------- | -------------------------------------------------------- |
| **1. Framework**            | Sets the scope and relationships of the documentation    |
| **2. Components**           | The changeable goals, processes, standards and resources |
| **3. Current architecture** | The "as-is" baseline inventory                           |
| **4. Future architecture**  | The "to-be" state needed to close gaps                   |
| **5. EA Management Plan**   | How to manage the move, a living document                |
| **6. Threads**              | Security, standards and skills                           |

::mnemonic Four Cats Can Find Many Treats
**F**ramework, **C**omponents, **C**urrent, **F**uture, **M**anagement plan, **T**hreads.
::
::trap Two different lists of six
Lecture 1's **six core elements** (governance, methodology, framework, artifacts, standards, best practices) describe a complete EA _approach_. This list of six describes EA _analysis and design_. Read which one the question asks for.
::

**Components** come in two kinds. **Vertical** components serve only one line of business, such as an HR payroll system. **Crosscutting** (horizontal) components serve several, such as email.

**Future architecture** is driven at three points: new directions and goals, changing business priorities, and emerging technologies. It covers **tactical changes (1 to 2 years)** and **strategic changes (3 to 10 years)**.

::example The gap
**Current:** three separate student-record systems. **Future:** one cloud platform. **The gap:** migration. **EA Management Plan:** sequencing it campus by campus.
::
::key

- Six elements: framework, components, current, future, management plan, threads
- Current view is the baseline, future view closes performance gaps
- Tactical changes are 1-2 years, strategic ones are 3-10 years
- Vertical components serve one LOB, crosscutting components serve several
- The EA Management Plan is a living document
  ::

## Keeping the terms straight | Slides 18-19 | must

Slide 18 is the most useful in the deck.

| Term                       | Definition                                     | Example                              |
| -------------------------- | ---------------------------------------------- | ------------------------------------ |
| **Level**                  | A hierarchical layer of the cube               | Data & Information                   |
| **Line of business**       | A distinct functional area                     | Finance                              |
| **Segment**                | Architecture view for one or more LOBs         | Finance from goals to infrastructure |
| **Component**              | A changeable goal, process, system or resource | Student portal                       |
| **Vertical component**     | Supports only one LOB                          | HR payroll system                    |
| **Crosscutting component** | Supports several LOBs                          | Email, intranet                      |
| **Thread**                 | A concern present in all levels                | Security                             |
| **Artifact**               | Documentation describing a component           | A data dictionary                    |

**Reference architecture:** standards for a type of capability throughout the enterprise, such as cloud computing. **Segment architecture:** focuses on business units or functions, such as finance.

::tip Level or LOB?
**Levels are horizontal rows** (what kind of thing). **LOBs are vertical columns** (which part of the organization).
::
::key

- Levels are layers and LOBs are functional columns
- A segment is a vertical slice of the architecture
- A thread is present at every level
- Artifacts are the documents, stored in the repository
  ::

## Asking the right questions at each level | Slides 20-27 | know

The framework can be used top-down, bottom-up or for a single component. Top-down, ask:

| Level                         | Key questions                                                                    |
| ----------------------------- | -------------------------------------------------------------------------------- |
| **Goals & Initiatives**       | Why do we exist? What are our goals and the initiatives to reach them?           |
| **Products & Services**       | What lines of business do we need? What do they deliver? How do we measure them? |
| **Data & Information**        | What information flows are needed? How do we standardize and protect them?       |
| **Systems & Applications**    | Which systems generate, share and store the data? How do they work together?     |
| **Networks & Infrastructure** | What networks and buildings do we need? How do they integrate?                   |

::key

- The framework can be used top-down, bottom-up or for a single component
- Each level has its own questions
- Information must be standardized and protected to be shared
  ::
  @cheat

### EA3 Cube

- Levels (5)
- Segments / LOBs
- Artifacts
- Threads run through all

### Five levels

- Goals & Initiatives
- Products & Services
- Data & Information
- Systems & Applications
- Networks & Infrastructure

### Six analysis elements

- Framework, Components
- Current, Future
- Management Plan, Threads

### Terms

- Vertical: one LOB
- Crosscutting: several LOBs
- Thread: all levels
- Tactical: 1-2 yrs
- Strategic: 3-10 yrs
  @mcq 8
  Which level sits at the top of the EA3 Cube?

* Goals & Initiatives

- Networks & Infrastructure
- Data & Information
- Systems & Applications

> Strategy is at the top, infrastructure at the bottom.
> @mcq 16
> Which is a thread?

- Security

* Finance
* Goals & Initiatives
* A data dictionary

> The threads are security, standards and skills.
> @mcq 18
> A payroll system used only by HR is a:

- Vertical component

* Crosscutting component
* Thread
* Level

> It supports only one line of business.
> @mcq 18
> An email system used by all departments is a:

- Crosscutting component

* Vertical component
* Segment
* Artifact

> It serves several lines of business.
> @mcq 13
> Strategic changes in the future architecture look how far ahead?

- 3 to 10 years

* 1 to 2 years
* Less than 6 months
* 20 years or more

> Tactical changes are 1 to 2 years.
> @mcq 12
> The current architecture serves mainly as:

- A baseline inventory

* A list of future goals
* A vendor contract
* A marketing plan

> It shows what exists today, so gaps can be seen.
> @mcq 15
> The EA Management Plan is described as:

- A living document

* A one-time report
* A hardware list
* A legal contract

> It's continually updated.
> @mcq 18
> Lines of business correspond in the cube to:

- Vertical columns

* Horizontal levels
* Threads
* The repository

> Levels are horizontal; LOBs are vertical.
> @mcq 19
> A reference architecture provides:

- Standards for a type of capability across the enterprise

* Documents for one employee
* A single LOB's budget
* A list of hardware vendors

> Slide 19, for example cloud computing or mobile services.
> @mcq 5
> Which is one of the six elements of EA analysis and design?

- Future architecture

* Marketing plan
* Pay structure
* Sales forecast

> The six are framework, components, current, future, management plan and threads.
> @short 18
> Explain the difference between a level, a line of business and a thread.
> ~ layer, functional, column, all levels, security
> A level is a horizontal layer such as Data & Information. A line of business is a vertical functional area such as Finance. A thread such as security runs through every level.
> @short 5
> Name the six elements of EA analysis and design.
> ~ framework, components, current, future, plan, threads
> Framework, components, current architecture, future architecture, EA Management Plan and threads.
> @short 14
> What three things drive the future architecture?
> ~ goals, priorities, technologies
> New strategic directions and goals, changing business priorities, and emerging technologies.

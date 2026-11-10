@head Lecture 1
@title Enterprise Architecture: Introduction, Purpose and Elements
@sources lecture-1-enterprise-architecture-introduction
@count 26
@tldr Enterprise architecture is a holistic way to plan an organization so that its strategy, business and technology all pull in the same direction.
@why Many organizations buy systems one department at a time and end up with duplicated, disconnected technology. EA exists to stop that. This lecture introduces the words used for the rest of the course, and the six core elements and four management-program benefits come up regularly on exams.
@connect Everything in this course builds on the equation in this lecture. Lecture 2 explains the method in more detail, and Lecture 4 goes into running EA as a program.
@goals

- Define enterprise architecture in your own words
- Explain EA = Strategy + Business + Technology
- Name the six core elements of an EA approach
- Explain why EA is called a meta-discipline
- List the four things EA does as a management program
  @vocab
  Enterprise | An organization, or a part of one, with a shared purpose.
  Holistic | Looking at the whole, and not just one part.
  Stakeholder | Anyone affected by, or with an interest in, the outcome.
  Line of business (LOB) | A distinct activity area, such as Finance or HR.
  As-is / to-be | The current state and the desired future state.
  @map
  3-5 | Definition and principles | MEMORIZE | Definition, and the four kinds of principle
  6-8 | EA = S + B + T, benefits | MEMORIZE | The equation and the six benefits
  9 | The EA process | SKIM | A continuous, agile cycle
  10-12 | EA as a meta-discipline | MEMORIZE | Umbrella for other best practices
  13-16 | Six core elements | MEMORIZE | Name and explain all six
  17-23 | Management program and method | MEMORIZE | Four program functions
  24-26 | Further reading | SKIM | ArchiMate reference

## What enterprise architecture is | Slides 3-8 | must

The slide's definition: EA is _"a well-defined practice for conducting enterprise analysis, design, planning, and implementation, using a holistic approach at all times, for the successful development and execution of strategy."_

In plain language, it's **a blueprint and a planning discipline for a whole organization**. It answers what the business does, what information it needs, and what technology supports it.

::formula The whole course in one line (slide 6)
EA = Strategy + Business + Technology
::

The equation separates EA from ordinary IT planning, which starts with technology.

| Part           | Question it answers                     | University example               |
| -------------- | --------------------------------------- | -------------------------------- |
| **Strategy**   | Why do we exist and where are we going? | Expand access to remote learners |
| **Business**   | What do we do and deliver?              | Offer an online degree           |
| **Technology** | What do we need to run it?              | Learning system, cloud servers   |

::analogy The city planner
Without planning, every building has its own water pipe and road. It works at first and ends in chaos. A city plan makes sure that roads, water and power serve the whole city. EA is the city plan for an organization's systems.
::
::why Why the slides call this a challenge
Slide 6 notes that technology has historically not been seen as an enterprise-wide resource, so planning focused on single solutions for particular requirements. That's how you get duplicated, disconnected systems.
::

Slides 4 and 5 list the **principles** EA applies, in four groups: **general** (IT and business alignment, maximum benefit at lowest cost and risk, business continuity, compliance, best practices), **information** (information as an asset, shared, accessible, common terminology, security), **application** (technology independence, ease of use, reusability, flexibility, low coupling), and **technology** (changes based on requirements, control of diversity and suppliers, interoperability).

::key

- EA is a holistic practice for analysis, design, planning and implementation in support of strategy
- EA = Strategy + Business + Technology
- Four groups of principles: general, information, application, technology
- Benefits include IT alignment, optimized performance, better communication and easier change
  ::

## EA as a meta-discipline | Slides 10-12 | must

Organizations already use many best-practice methods: project management (PMBOK), business process improvement, capital planning. Each has its own view and they can compete. Slide 10 calls this the **"battle of best practices"**.

EA resolves that by being the **overarching, highest-level discipline**: the "meta-context" or umbrella in which all the others fit.

::analogy Conductor of an orchestra
The violinists and drummers are all excellent. The conductor doesn't replace any of them, but makes sure they play the same piece at the same tempo. EA is the conductor of IT and management practices.
::
::trap Meta doesn't mean it replaces the others
EA doesn't replace project management or security practice. It's the **organizing context and standards authority** for them.
::
::key

- EA is holistic and serves as a meta-context for other practices
- It resolves the battle of best practices
- It adds strategic planning as the primary driver of requirements
  ::

## The six core elements | Slides 13-16 | must

For an EA approach to be complete, **all six must be present and work together**.

| Element            | What it provides                                             | Plain meaning             |
| ------------------ | ------------------------------------------------------------ | ------------------------- |
| **Governance**     | Planning, decision-making and oversight processes and groups | Who decides, and how      |
| **Methodology**    | Specific steps to establish and maintain the program         | The recipe                |
| **Framework**      | Scope and organization of the documentation                  | The filing system         |
| **Artifacts**      | The documentation in each sub-architecture                   | The actual documents      |
| **Standards**      | Business and technology standards at every level             | The agreed rules          |
| **Best practices** | Proven ways to implement parts of the architecture           | What has worked elsewhere |

::mnemonic BAGS FM
Picture a radio station called **BAGS FM**: **B**est practices, **A**rtifacts, **G**overnance, **S**tandards, **F**ramework, **M**ethodology.
::
::tip The framework's internal parts (slide 15)
Three **threads** run through it: security, standards and workforce skills. Its sub-architecture levels are strategic direction, business practices, information flows, systems and applications, and technology resources.
::
::check Which element answers "who approves a new enterprise-wide system?"
**Governance**, since it covers the decision-making and oversight processes.
::
::key

- Six core elements: governance, methodology, framework, artifacts, standards, best practices
- All six must be present and work together
- Threads are security, standards and workforce skills
  ::

## EA's two jobs: program and method | Slides 17-23 | must

EA is carried out through a **management program** and an **analysis and design method**.

As a **management program** it does four things:

| Function                | What it does                                                        |
| ----------------------- | ------------------------------------------------------------------- |
| **Strategic alignment** | Connects goals, activities and resources                            |
| **Standardized policy** | Sets policy for resource governance and implementation              |
| **Decision support**    | Supports IT decisions at executive, management and technical levels |
| **Resource oversight**  | Oversees capability development and reduces risk                    |

::mnemonic SSDR: Strategy Sets Decisions and Resources
**S**trategic alignment, **S**tandardized policy, **D**ecision support, **R**esource oversight.
::

As an **analysis and design method** it provides the EA approach, current views (as-is), future views (to-be), and an EA Management Plan for moving between them.

::example One initiative, four functions
A hospital wants online appointments.

- **Strategic alignment:** does it serve the goal of patient access?
- **Standardized policy:** must follow the data-privacy policy.
- **Decision support:** executives see that it duplicates a clinic's existing tool.
- **Resource oversight:** the project is tracked for cost and schedule.
  ::
  ::key
- EA is both a management program and an analysis and design method
- Program functions: strategic alignment, standardized policy, decision support, resource oversight
- The method provides current views, future views and a management plan
  ::
  @cheat

### Definition

- Holistic analysis, design, planning, implementation
- EA = Strategy + Business + Technology

### Six core elements (BAGS FM)

- Best practices, Artifacts
- Governance, Standards
- Framework, Methodology

### Management program

- Strategic alignment
- Standardized policy
- Decision support
- Resource oversight

### Method provides

- Current views (as-is)
- Future views (to-be)
- EA Management Plan

### Meta-discipline

- Umbrella for best practices
- Resolves battle of best practices
  @mcq 6
  Which equation summarizes EA on slide 6?

* EA = Strategy + Business + Technology

- EA = Hardware + Software + People
- EA = Security + Standards + Skills
- EA = Data + Systems + Networks

> This equation separates EA from other kinds of IT planning.
> @mcq 13
> Which of these is one of the six core elements of an EA approach?

- Governance

* Marketing
* Recruitment
* Accounting

> The six are governance, methodology, framework, artifacts, standards and best practices.
> @mcq 14
> Which core element covers planning, decision-making and oversight processes?

- Governance

* Artifacts
* Framework
* Standards

> Slide 14.
> @mcq 15
> Which core element is the actual documentation?

- Artifacts

* Methodology
* Governance
* Best practices

> Artifacts are the documents in each sub-architecture.
> @mcq 10
> EA is called a meta-discipline because it:

- Serves as an umbrella for other practices

* Replaces project management
* Only deals with hardware
* Is limited to one department

> It's the organizing context for other best practices.
> @mcq 15
> The three threads in the framework are:

- Security, standards and skills

* Goals, products and data
* Cost, time and quality
* Planning, design and testing

> Slide 15.
> @mcq 18
> Which is a function of EA as a management program?

- Decision support

* Writing application code
* Replacing all legacy systems
* Payroll processing

> The four functions are strategic alignment, standardized policy, decision support and resource oversight.
> @mcq 19
> The EA Management Plan is for:

- Moving from the current to the future architecture

* Listing employees' salaries
* Replacing the framework
* Recording only past projects

> Slide 19.
> @mcq 10
> The "battle of best practices" refers to:

- Competition between sub-architectural domains

* A contest between vendors
* Debates about pricing
* Fights over office space

> EA resolves this competition.
> @mcq 6
> Historically, IT planning has tended to focus on:

- Individual technology solutions

* The enterprise as a whole
* Long-term strategy first
* Common standards

> That is the problem EA is meant to fix.
> @short 13
> Name the six core elements of an EA approach and say what any two do.
> ~ governance, methodology, framework, artifacts, standards, best practices
> Governance, methodology, framework, artifacts, standards and best practices. Governance sets the planning and decision-making processes; the framework defines the scope and organization of documentation.
> @short 6
> Explain EA = S + B + T using a real example.
> ~ strategy, business, technology, align, example
> Strategy says where the organization is going, business says what it delivers, and technology supports delivery. A bank aiming to grow online (strategy) offers mobile accounts (business) using a mobile app and cloud services (technology).
> @short 18
> List the four functions of EA as a management program.
> ~ strategic alignment, policy, decision support, resource oversight
> Strategic alignment, standardized policy, decision support and resource oversight.

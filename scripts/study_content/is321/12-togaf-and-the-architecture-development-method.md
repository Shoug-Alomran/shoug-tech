@head Lecture 12
@title TOGAF and the Architecture Development Method
@sources lecture-12-togaf-and-the-architecture-development-method
@count 38
@tldr TOGAF describes an enterprise in four domains and gives you a nine-phase repeating method, the ADM, to take it from where it is to where it needs to be.
@why This is the longest of the later decks because each phase has a full slide. The slides themselves say the core concepts are the most important thing on the exam. And you need the ADM's phases in order, with what each one produces.
@connect Lecture 11 positioned TOGAF. Here's the full method. Lecture 13 compares it with the Cube.
@goals

- Name the four BDAT domains
- Distinguish deliverable, artifact and building block
- Describe the Enterprise Continuum's four tiers
- List ADM phases in order and state each one's purpose
- Explain Requirements Management's central role
  @vocab
  ADM | Architecture Development Method.
  Baseline | The current state.
  Target | The desired future state.
  Work package | A group of related tasks.
  Transition architecture | An interim state on the way to the target.
  @map
  3-4 | What TOGAF is | SKIM | Origin and when to use
  5-12 | Seven core concepts | MEMORIZE | The slide calls these key
  13-14 | ADM overview and iteration | MEMORIZE | Nine phases around a hub
  15-34 | Each phase | MEMORIZE | Purpose and key output
  35-36 | Requirements Management | MEMORIZE | The hub

## Seven core concepts | Slides 5-12 | must

### 1. The four domains: BDAT

| Letter | Domain      | Covers                                                        |
| ------ | ----------- | ------------------------------------------------------------- |
| **B**  | Business    | Strategy, governance, organization, key processes             |
| **D**  | Data        | Logical and physical data assets                              |
| **A**  | Application | Blueprint for individual applications and their relationships |
| **T**  | Technology  | Hardware, networks and other capabilities needed              |

::mnemonic BDAT: Big Dogs Adore Treats
**B**usiness, **D**ata, **A**pplication, **T**echnology, in the order the ADM covers them.
::

### 2. Deliverables, artifacts and building blocks

| Term               | Meaning                                                   | Think of                |
| ------------------ | --------------------------------------------------------- | ----------------------- |
| **Deliverable**    | Contractually specified, formally reviewed and signed off | The signed report       |
| **Artifact**       | A catalog, diagram or matrix, part of a deliverable       | One chart in the report |
| **Building block** | A potentially reusable component                          | A LEGO brick            |

**Deliverable contains artifacts, which describe building blocks.**

### 3. The Enterprise Continuum

A way of classifying artifacts from generic to specific. The handwriting on the slide warns you "may be asked to classify these tiers".

| Tier                      | How generic                | Example                                        |
| ------------------------- | -------------------------- | ---------------------------------------------- |
| **Foundation**            | Extremely generic          | Programming languages, operating systems, ITIL |
| **Common Systems**        | Still generic, some detail | Security architecture, MS Office               |
| **Industry**              | Industry-specific          | Credit-card processing in retail               |
| **Organization-Specific** | Most specific              | Your own services and functions                |

::mnemonic Fruit Comes In Orchards
**F**oundation, **C**ommon systems, **I**ndustry, **O**rganization-specific: generic to specific.
::

### 4-7. The rest

- **Architecture Repository:** holds all the output, "an empty box you fill".
- **Architecture Capability:** the business capability for doing architecture itself.
- **Governance:** how architectures are managed and controlled. Three levels: strategic, segment and capability.
- **Stakeholders, Views and Viewpoints:** a **stakeholder** has concerns; a **view** is what's seen; a **viewpoint** is the perspective from which it's taken.

::analogy View and viewpoint
From the top of a tower (**viewpoint**), you see the city (**view**). The tower is where you stand; the scene is what you get.
::

**Capability assessment:** first created in Phase A and updated in Phase E, it tracks baseline and target capabilities.

::check Classify: Linux, a bank's own loan-approval service, retail credit-card processing, an industry-neutral security architecture.
Linux: Foundation. Loan service: Organization-Specific. Card processing: Industry. Security architecture: Common Systems.
::
::key

- BDAT: Business, Data, Application, Technology
- A deliverable is signed off, an artifact is part of one, a building block is reusable
- Enterprise Continuum: Foundation, Common Systems, Industry, Organization-Specific
- A viewpoint is the perspective, a view is what's seen from it
  ::

## The ADM: nine phases around a hub | Slides 13-36 | must

The ADM is **a method for developing and managing the lifecycle of an enterprise architecture**: a Preliminary phase plus eight phases in a cycle, around continuous Requirements Management.

::graph The ADM wheel, with Requirements Management at the centre | directed
n P 200 0 Preliminary
n A 200 70 A Vision
n B 350 120 B Business
n C 400 220 C Info Systems
n D 350 320 D Technology
n E 200 370 E Opportunities
n F 50 320 F Migration
n G 0 220 G Governance
n H 50 120 H Change Mgmt
n R 200 220 Requirements\nManagement *
e P A
e A B
e B C
e C D
e D E
e E F
e F G
e G H
e H A
::

| Phase      | Name                      | Purpose                                                           | Key output                                  |
| ---------- | ------------------------- | ----------------------------------------------------------------- | ------------------------------------------- |
| **Prelim** | Preliminary               | Prepare: define the enterprise, principles, framework             | Architecture principles, tailored framework |
| **A**      | Architecture Vision       | High-level vision, approval to proceed                            | Approved **Statement of Architecture Work** |
| **B**      | Business Architecture     | Baseline, target and gaps for business                            | Definition document v1.0                    |
| **C**      | Information Systems       | Baseline, target and gaps for Data and Application                | Definition document v1.0                    |
| **D**      | Technology Architecture   | Baseline, target and gaps for technology                          | Definition document v1.0                    |
| **E**      | Opportunities & Solutions | Initial complete roadmap; work packages, transition architectures | **Architecture Roadmap**                    |
| **F**      | Migration Planning        | Finalize roadmap and plan; assign business value                  | **Implementation & Migration Plan**         |
| **G**      | Implementation Governance | Make sure that projects conform to the target                     | Compliance, change requests                 |
| **H**      | Change Management         | Keep the architecture alive                                       | Change requests that may start a new cycle  |
| **Hub**    | Requirements Management   | Sustained through all phases; assesses changes                    | Updated requirements                        |

::mnemonic Very Busy Cats Do Eat Fish, Getting Happier
The wheel from Phase A: **V**ision, **B**usiness, **C** (Information Systems), **D** (Technology), **E** Opportunities, **F** Migration, **G** Governance, **H** Change Management.
::
::tip B, C and D share one recipe
Each one: **develop the baseline, develop the target, identify the gaps**. Baseline is often bottom-up, and target is normally top-down from goals.
::

**ADM is iterative in three ways** (slide 14):

- **Across the whole process:** Phase H flows back into a new Phase A.
- **Between phases:** Phase C might reveal something that forces a return to Phase B.
- **Within a phase:** several passes to get a detailed target right.

Four dimensions of scope are decided for each iteration: **breadth, level of detail, time period and BDAT domains**.

::trap Requirements Management isn't a step
It's at the centre and is **continuous**, not a phase you pass through once. Requirements change because of competitors, law, or disproved assumptions.
::
::trap Phase C covers two domains
Data and Application are developed separately, in either order or together, but they're both Phase C.
::
::check Which phase produces the Statement of Architecture Work? Which finalizes the Implementation and Migration Plan?
Phase A. Phase F.
::
::key

- ADM is a preliminary phase plus eight phases around Requirements Management
- A: Vision, B: Business, C: Data and Application, D: Technology
- E: roadmap, F: migration plan, G: governance, H: change management
- B, C and D each develop baseline, target and gaps
- The ADM is iterative across, between and within phases
  ::
  @cheat

### BDAT

- Business, Data
- Application, Technology

### Work products

- Deliverable: signed off
- Artifact: catalog, diagram, matrix
- Building block: reusable

### Enterprise Continuum

- Foundation
- Common Systems
- Industry
- Organization-Specific

### ADM phases

- Prelim: prepare
- A Vision
- B Business
- C Data + Application
- D Technology
- E Opportunities and Solutions
- F Migration Planning
- G Implementation Governance
- H Change Management
- Centre: Requirements Management

### Key outputs

- A: Statement of Architecture Work
- E: Architecture Roadmap
- F: Implementation & Migration Plan
  @mcq 6
  BDAT stands for:

* Business, Data, Application, Technology

- Budget, Design, Analysis, Testing
- Business, Design, Application, Tools
- Backup, Data, Access, Technology

> Slide 6.
> @mcq 7
> A work product formally reviewed and signed off is a:

- Deliverable

* Artifact
* Building block
* Viewpoint

> Slide 7.
> @mcq 7
> A catalog, diagram or matrix is a:

- Artifact

* Deliverable
* Stakeholder
* Phase

> Slide 7.
> @mcq 8
> The most generic tier in the Enterprise Continuum is:

- Foundation

* Organization-Specific
* Industry
* Common Systems

> Slide 8.
> @mcq 18
> The Statement of Architecture Work is approved in:

- Phase A

* Phase B
* Phase E
* Phase H

> Slide 18.
> @mcq 21
> Phase C covers:

- Data and Application

* Business only
* Technology only
* Migration planning

> Slides 21 to 24.
> @mcq 27
> The initial complete Architecture Roadmap is generated in:

- Phase E

* Phase A
* Phase G
* Preliminary

> Slide 27.
> @mcq 31
> Phase G is concerned with:

- Ensuring implementation conforms to the target

* Writing the vision
* Defining the enterprise
* Choosing data standards

> Slide 31.
> @mcq 35
> Requirements Management:

- Runs continuously at the centre of the ADM

* Happens once, in Phase A
* Replaces Phase H
* Is optional and rarely used

> Slide 35.
> @mcq 11
> The perspective from which a view is taken is a:

- Viewpoint

* Stakeholder
* Building block
* Deliverable

> Slide 11.
> @mcq 14
> Discovering in Phase C that Phase B needs revising is iteration:

- Between phases

* Across the whole process
* Within a phase
* Not allowed

> Slide 14.
> @short 13
> List the ADM phases in order, and state what sits at the centre.
> ~ preliminary, vision, business, information, technology, opportunities, migration, governance, change, requirements
> Preliminary, A Vision, B Business, C Information Systems, D Technology, E Opportunities and Solutions, F Migration Planning, G Implementation Governance and H Change Management, with Requirements Management at the centre.
> @short 7
> Distinguish deliverable, artifact and building block.
> ~ signed, catalog, diagram, reusable
> A deliverable is a contractually specified work product signed off by stakeholders. An artifact is a catalog, diagram or matrix that forms part of a deliverable. A building block is a potentially reusable component.
> @short 19
> What three things do Phases B, C and D each do?
> ~ baseline, target, gap
> Each develops the baseline architecture, develops the target architecture, and identifies the gaps between them.

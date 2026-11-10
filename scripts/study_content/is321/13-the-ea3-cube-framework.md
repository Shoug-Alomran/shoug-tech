@head Lecture 13
@title The EA3 Cube Framework
@sources lecture-13-the-ea3-cube-framework
@count 18
@tldr Levels say what kind of thing, segments say which part of the business, and artifacts are the documents, and any item in an enterprise sits at one intersection of the three.
@why This lecture pulls together everything about the Cube. Expect to be asked to locate one item in all three dimensions, like the Amanah Bank example, and to spot the common mistakes on slide 15.
@connect Pulls in Lectures 2, 3, 5, 7 and 11. It's a good summary before the final.
@goals

- Describe all three dimensions and how they intersect
- Locate an item in the cube
- Distinguish vertical and crosscutting components
- Connect the cube to the repository
- Avoid the three common pitfalls
  @vocab
  Cell | One intersection of a level, a segment and an artifact.
  Crosswalk | A mapping between two structures.
  Line of business | A vertical slab of the cube with its own five-level documentation.
  @map
  3-4 | Why revisit, three dimensions | MEMORIZE | Levels, Segments, Artifacts
  5-7 | Components, current vs future, threads | MEMORIZE | Vertical vs crosscutting
  8-13 | Segments, artifacts, one cell | WRITE | Locate an item
  14 | Crosswalk to repository | MEMORIZE | Levels plus security
  15-16 | Pitfalls and contrasts | MEMORIZE | The three pitfalls

## Three dimensions, one location | Slides 3-13 | must

| Dimension                        | Answers                     | Examples                                  |
| -------------------------------- | --------------------------- | ----------------------------------------- |
| **Levels**                       | What kind of thing?         | Goals, Products, Data, Systems, Networks  |
| **Segments** (lines of business) | Which part of the business? | Retail Banking, Licensing, Online Degrees |
| **Artifacts**                    | How is it documented?       | Plans, diagrams, inventories              |

**Every level, within every segment, is documented by a set of artifacts.** Each line of business gets its own complete five-level documentation.

::steps Locate Amanah Bank's new API account access product
**Level:** Products & Services, Level 2.
**Segment:** Retail Banking, one line of business among several.
**Artifact:** the Business Service/Function Catalog entry that documents it.
::
::steps Locate the university's LMS integration
**Level:** Systems & Applications, Level 4.
**Segment:** Online-Degree Programs.
**Artifact:** the Application Inventory entry for its interfaces and data flows.
::

Artifacts fall into three groups:

| Group                      | Examples                                                 |
| -------------------------- | -------------------------------------------------------- |
| **Plans & Reports**        | Strategic plan, management summaries                     |
| **Diagrams & Models**      | Org charts, process flows, data models, network diagrams |
| **Matrices & Inventories** | Application inventories, technology standards            |

What counts as a segment depends on the enterprise: a **bank** has retail, commercial and wealth management. A **government agency** has licensing, public health and revenue collection. A **university** has programs and functions.

::analogy An address
Level is the **floor**, segment is the **building**, artifact is the **document in the file** about that room. You need all three to find anything.
::
::key

- Three dimensions: levels, segments, artifacts
- Each segment has its own five-level documentation
- Any item can be located by level, segment and artifact
- Artifacts: plans and reports, diagrams and models, matrices and inventories
  ::

## Components, threads and pitfalls | Slides 5-7, 14-16 | must

**Vertical and crosscutting components.**

::says Slide 16 | "Vertical belongs to one Level; crosscutting ... all five"
This lecture defines them across **levels**: a crosscutting component such as an intranet, telecommunications or buildings spans every level. Lecture 2's slide 18 defined them across **lines of business**. Use the definition that matches the context: if the question is about the cube's levels, use this one.
::

**Threads**: Security, Standards and Skills run through all five levels without being a level themselves.

**The repository crosswalk:** its six columns are the cube's five levels **plus the Security thread**. Each column holds artifacts for that level, and segments act as a filter ("show me only Retail Banking").

**The current-to-future transition** is bridged by the Architecture Management Plan.

Three common mistakes (slide 15):

| Pitfall                      | Correction                                                                  |
| ---------------------------- | --------------------------------------------------------------------------- |
| **Treating levels as steps** | They're simultaneous views of one enterprise, updated together              |
| **Ignoring the threads**     | Skipping them leaves major gaps                                             |
| **One cube per company**     | Large enterprises need one cube instance per segment or organizational unit |

::mnemonic STOP
**St**eps, **T**hreads, **O**ne cube: stop making those three **P**itfalls.
::
::tip The three contrasts on slide 16
**Vertical vs crosscutting. Current vs future. Levels vs segments.** Make sure you can explain each in one sentence.
::
::check The Security Solutions column comes from which part of the cube?
From the **Security thread**, which is given its own repository column.
::
::key

- Crosscutting components span all five levels, such as intranets and buildings
- Threads run through all levels but aren't levels themselves
- Repository columns are the five levels plus the Security thread
- Levels aren't steps; don't forget threads; large enterprises need more than one cube
  ::
  @cheat

### Three dimensions

- Levels: what kind
- Segments: which part
- Artifacts: documentation

### Artifact types

- Plans & Reports
- Diagrams & Models
- Matrices & Inventories

### Repository crosswalk

- Five levels + Security thread
- Segments act as a filter

### Pitfalls

- Levels aren't steps
- Don't skip threads
- One cube isn't enough for large firms

### Contrasts

- Vertical vs crosscutting
- Current vs future
- Levels vs segments
  @mcq 4
  The EA3 Cube's three dimensions are:

* Levels, segments and artifacts

- Cost, time and quality
- Rows, columns and tables
- Data, systems and networks

> Slide 4.
> @mcq 8
> Segments in the cube correspond to:

- Lines of business

* Threads
* The five levels
* ADM phases

> Slide 8.
> @mcq 8
> Each line of business has:

- Its own complete five-level documentation

* A single shared document
* No artifacts
* Just one level

> Slide 8.
> @mcq 15
> Which is a common pitfall?

- Treating levels as steps to do in order

* Documenting all threads
* Having a repository
* Updating levels together

> Slide 15.
> @mcq 14
> The repository's six columns are:

- The five levels plus the Security thread

* The six Zachman questions
* Six lines of business
* Six ADM phases

> Slide 14.
> @mcq 10
> An application inventory is an example of:

- Matrices & Inventories

* Plans & Reports
* Diagrams & Models
* Threads

> Slide 10.
> @mcq 10
> A network diagram is an example of:

- Diagrams & Models

* Plans & Reports
* Matrices & Inventories
* Segments

> Slide 10.
> @mcq 12
> For a government agency, a segment might be:

- Licensing

* A network cable
* A data dictionary
* A strategic goal

> Slide 12.
> @mcq 16
> Levels are described as:

- Horizontal slices: what kind of thing

* Vertical slices: which part of the business
* The documentation itself
* Sequential steps

> Slide 16.
> @mcq 7
> Threads are:

- Concerns that touch all five levels

* A sixth level
* A type of artifact
* A line of business

> Slide 7.
> @short 9
> Locate a hospital's patient-records database in the cube.
> ~ level, segment, artifact, data, systems
> Level: Systems & Applications, or Data & Information for the records themselves. Segment: Clinical Services. Artifact: an application inventory entry or a data model.
> @short 15
> Name the three pitfalls and how to avoid them.
> ~ steps, threads, one cube, simultaneous
> Don't treat levels as steps, as they're simultaneous views. Don't ignore the security, standards and skills threads. And don't assume that one cube is enough for a large enterprise.
> @short 16
> Explain the difference between levels and segments.
> ~ horizontal, vertical, kind, part
> Levels are horizontal slices that say what kind of thing it is. Segments are vertical slices that say which part of the business it belongs to.

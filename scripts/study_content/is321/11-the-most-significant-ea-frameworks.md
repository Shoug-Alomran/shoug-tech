@head Lecture 11
@title The Most Significant EA Frameworks
@sources lecture-11-the-most-significant-ea-frameworks
@count 14
@tldr There are about twenty EA frameworks; learn the four main ones by what each is best for: Zachman classifies, TOGAF builds, the EA3 Cube documents, DoDAF serves defense.
@why Slide 12's "which framework for which need" is an exam question waiting to happen. So is the fact that Zachman is a classification schema rather than a method.
@connect You know the Cube from earlier lectures. Lecture 12 goes deep on TOGAF, and Lecture 13 revisits the Cube.
@goals
- Describe the Zachman matrix: rows and columns
- Explain why Zachman is not a method
- Compare Zachman, TOGAF, EA3 Cube and DoDAF
- Choose a framework for a given need
@vocab
Schema | A structure for classifying things.
Ontology | A formal classification of what exists in a domain.
Interrogative | A question word, such as what or why.
Viewpoint | The perspective from which something is described.
@map
3 | Why so many | SKIM | About 20 exist
4-7 | Zachman | MEMORIZE | Rows, columns, uses
8-10 | TOGAF, Cube, DoDAF recap | MEMORIZE | One line each
11-12 | Comparison, choosing | MEMORIZE | The table on slide 12

## The Zachman Framework | Slides 4-7 | must
John Zachman's 1987 schema combines two old classifications: **the basic questions** and **stages of reification** (turning an abstract idea into a real thing). It's a **6 × 6 matrix: 36 cells**.

| Rows: Who is asking? | Concerned with |
|---|---|
| **Executive** | Size and cost |
| **Business Management** | Process interaction |
| **Architect** | How software represents the model |
| **Engineer** | Applying technology to problems |
| **Technician** | Following instructions |
| **Enterprise** | The operational system itself |

| Columns: What is asked? | About |
|---|---|
| **What?** | Data |
| **How?** | Functions and processes |
| **Where?** | Locations and logistics |
| **Who?** | Organizational units and people |
| **When?** | Business cycles and events |
| **Why?** | Goals and strategy |

::analogy A library's card catalogue
A catalogue tells you where every book belongs, and it doesn't write any books. Zachman is the catalogue for an enterprise: **a master file for classifying what to document**.
::
::mnemonic Reporters' questions
The columns are the six questions every journalist asks: what, how, where, who, when, why.
::
::trap Zachman is a schema, not a method
It says **what** to document, and not **how** to build it. The handwriting on slide 4 says just that. That's why it combines so well with other frameworks.
::
::key
- Zachman is a 6×6 classification schema with 36 cells
- Rows are perspectives, columns are fundamental questions
- It organizes what to document, not how to build it
- It's easily combined with other frameworks
::

## Four frameworks side by side | Slides 8-12 | must
| Framework | Origin | Type | Structure | Use when you need |
|---|---|---|---|---|
| **Zachman** | John Zachman, 1987 | Classification schema | 6×6 matrix | To make sure nothing goes undocumented |
| **TOGAF** | The Open Group, 1995 | Development method | 9-phase cyclical ADM, Requirements Management in the centre | A repeatable process to build the architecture |
| **EA3 Cube** | Scott Bernard, 2005 | Academic and practitioner framework | 5 levels × segments × artifacts, with threads | A structured repository and ongoing management plan |
| **DoDAF** | U.S. Department of Defense | Viewpoints and views | Operational, Systems/Service and Technical Standard views | Defense or large government interoperability |

::mnemonic Zachman Zips, TOGAF Takes steps, Cube Catalogues, DoDAF Defends
**Z**achman zips up gaps by checking completeness. **T**OGAF **t**akes you through steps. The **C**ube **c**atalogues documentation. **D**oDAF **d**efends.
::
::example DoDAF, from the handwriting on slide 10
A drone built by one contractor needs to talk to a satellite built by another. DoDAF's standardized views let different manufacturers' systems work together.
::
::tip They aren't competitors
Slide 13 says many real implementations use Zachman's completeness check alongside TOGAF's process.
::
::check You need a step-by-step process for developing your architecture. Which framework?
**TOGAF**, with its ADM.
::
::key
- About 20 EA frameworks exist
- TOGAF: repeatable process through the ADM
- EA3 Cube: structured repository and management plan
- DoDAF: defense and government interoperability
- Frameworks can be combined
::
@cheat
### Zachman
- 6×6, 36 cells
- Rows: Executive, Business Mgmt, Architect, Engineer, Technician, Enterprise
- Columns: What, How, Where, Who, When, Why
- Schema, not a method
### Choose by need
- Completeness: Zachman
- Repeatable process: TOGAF
- Repository and plan: EA3 Cube
- Defense: DoDAF
### DoDAF views
- Operational
- Systems / Service
- Technical Standard
### Origins
- Zachman 1987
- TOGAF 1995
- EA3 Cube 2005
@mcq 5
How many cells does the Zachman Framework have?
+ 36
- 25
- 6
- 12
> Six rows by six columns.
@mcq 4
Zachman is best described as a:
+ Classification schema
- Step-by-step method
- Programming language
- Cloud service
> It says what to document, not how to build it.
@mcq 5
Which is a column in Zachman?
+ When?
- Budget
- Level
- Segment
> What, How, Where, Who, When, Why.
@mcq 5
Which is a Zachman row?
+ Engineer
- Why
- Where
- Who
> Rows are perspectives.
@mcq 12
"I need a repeatable process to build the architecture." Choose:
+ TOGAF
- Zachman
- DoDAF
- None of them
> Slide 12.
@mcq 12
"I haven't missed documenting something." Choose:
+ Zachman
- TOGAF
- EA3 Cube
- DoDAF
> Its completeness guarantee.
@mcq 12
Defense with strict interoperability rules suggests:
+ DoDAF
- Zachman
- EA3 Cube
- SaaS
> Purpose-built for it.
@mcq 11
Who developed the EA3 Cube?
+ Scott Bernard
- John Zachman
- Harold Leavitt
- The Open Group
> Slide 11.
@mcq 11
TOGAF comes from:
+ The Open Group
- The U.S. Department of Defense
- Scott Bernard
- NIST
> Slide 11.
@mcq 10
Which is a DoDAF core view?
+ Operational View
- Financial View
- Marketing View
- Student View
> Operational, Systems/Service and Technical Standard.
@short 5
Describe the structure of the Zachman Framework.
~ six, rows, perspectives, columns, questions, 36
> It's a 6×6 matrix of 36 cells. Rows are perspectives from executive to enterprise, and columns are the six questions: what, how, where, who, when and why.
@short 12
For each of the four frameworks, state when you'd use it.
~ Zachman, TOGAF, Cube, DoDAF, repeatable, defense
> Zachman to check that nothing is undocumented. TOGAF for a repeatable process. EA3 Cube for a structured repository and management plan. DoDAF for defense or government interoperability.
@short 4
Why can Zachman be combined with TOGAF?
~ schema, what, how, process, complementary
> Zachman classifies what to document and TOGAF gives the process for how to build it, so they complement rather than compete with each other.

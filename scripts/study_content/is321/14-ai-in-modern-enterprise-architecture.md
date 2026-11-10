@head Lecture 14
@title AI in Modern Enterprise Architecture
@sources lecture-14-ai-in-modern-enterprise-architecture
@count 12
@tldr AI drafts, checks and finds EA documentation faster than people can, but a person must still verify it.
@why A short final lecture, and it ties together the AI theme from Lectures 3, 6, 8 and 10. Know the three capabilities and the three limitations, and remember the phrase "AI drafts, human verifies".
@connect This is the end of the AI thread that began in Lecture 3, layered on the cube and TOGAF, which themselves don't change.
@goals
- Say why AI is being adopted in EA now
- Describe the three AI capabilities
- State the three limitations
- Apply the guardrails
@vocab
Hallucination | When an AI confidently states something false.
Drift | When real systems stop matching the approved standards.
Semantic search | Searching by meaning rather than exact keywords.
Guardrail | A rule that keeps a tool's use safe.
@map
3 | Why now | MEMORIZE | Three shifts
4-6 | Three capabilities | MEMORIZE | Modeling, governance, repositories
7-8 | Risks and guardrails | MEMORIZE | Three limitations
9-11 | Worked example, recap | WRITE | Trace one change

## Why now, and what AI does | Slides 3-6 | must
The EA3 Cube and TOGAF's ADM both predate modern AI. **Neither framework changes.** AI is being layered on top because of three shifts: **documentation volume**, **mature AI tooling** and **faster change cycles**.

| Capability | Traditional way | With AI | Example |
|---|---|---|---|
| **AI-assisted modeling** | Build every cell by hand | Drafts first-pass Current Architecture and flags gaps | Upload Amanah Bank's system documents |
| **AI-supported governance** | Scheduled compliance reviews | Continuously scans for drift from approved standards | Flags a service not matching a standard |
| **Smart repositories** | Browse by structure or keyword | Semantic search and cross-segment linking | "Which segments already built an API gateway?" |

::mnemonic Draft, Detect, Discover
**Draft** (modeling), **Detect** (governance), **Discover** (repository). One word per capability.
::
::analogy A very fast junior assistant
It drafts a report in seconds. It might also invent a figure. Nobody sensible publishes that report without reading it first.
::
::key
- The frameworks don't change; AI is layered on top
- Three drivers: documentation volume, mature tooling, faster change
- Modeling drafts, governance detects drift, smart repositories find related work
::

## Limits and guardrails | Slides 7-11 | must
| Limitation | What goes wrong | Response |
|---|---|---|
| **Hallucinated documentation** | A plausible entry that doesn't match reality | Verify against source systems before publishing |
| **Governance blind spots** | Can't catch a standard never documented | Keep standards complete |
| **Training data bias** | Suggestions repeat gaps in past documents | Have an architect review suggestions |

Guardrails: **acknowledge AI use** as the syllabus requires, and **the architect reviews, AI drafts**: AI produces a first pass, and a person verifies it before it becomes official.

::steps Slide 9: one change through all three capabilities
An architect adds a new API gateway to Retail Banking.
AI drafts the first-pass Current Architecture entry (**modeling**).
A tool checks it against approved data-storage standards before deployment (**governance**).
Once published, a smart repository makes it discoverable (**repository**).
Six months later, another segment planning something similar finds it and reuses it.
::
::trap AI doesn't replace architectural judgment
Slide 7 says so directly. An exam statement that AI removes the need for an architect is false.
::
::key
- Three limitations: hallucinated documentation, governance blind spots, training data bias
- AI cannot catch a standard that was never documented
- Guardrails: acknowledge AI use, and have an architect review all drafts
::
@cheat
### Three capabilities
- Modeling: drafts
- Governance: detects drift
- Repositories: semantic search
### Why now
- Documentation volume
- Mature AI tooling
- Faster change cycles
### Limitations
- Hallucinated documentation
- Governance blind spots
- Training data bias
### Guardrails
- Acknowledge AI use
- Architect reviews, AI drafts
@mcq 4
AI-assisted modeling mainly:
+ Drafts first-pass Current Architecture
- Replaces the Cube
- Writes the syllabus
- Removes the need for review
> Slide 4.
@mcq 5
AI-supported governance detects:
+ Drift from approved standards
- Employee absences
- Student grades
- Room temperature
> Slide 5.
@mcq 6
A smart repository adds:
+ Semantic search and cross-segment discovery
- Physical storage
- More printers
- Paper backups
> Slide 6.
@mcq 3
According to the slides, AI causes the EA frameworks to:
+ Remain the same, with AI layered on top
- Be replaced by AI
- Be merged into one
- Become illegal
> Slide 3.
@mcq 7
A plausible but false architecture entry is called:
+ Hallucinated documentation
- A governance blind spot
- Training data bias
- A thread
> Slide 7.
@mcq 7
Which can AI governance NOT catch?
+ A standard that was never documented
- Drift from a documented standard
- Non-conforming deployed services
- Differences from approved rules
> Slide 7.
@mcq 8
"AI drafts" is paired with:
+ The architect reviews
- The executive signs without reading
- The vendor decides
- No one checks
> Slide 8.
@mcq 3
Which is one of the reasons for AI in EA now?
+ Faster change cycles
- Fewer applications
- Less documentation
- Slower systems
> Documentation volume, mature tools and faster change.
@mcq 7
Suggestions that repeat gaps in old documents reflect:
+ Training data bias
- Hallucination only
- A hot site
- Virtualization
> Slide 7.
@mcq 8
Under the course policy, AI-assisted work must be:
+ Disclosed
- Hidden
- Avoided entirely
- Submitted twice
> Slide 8.
@short 4
Name the three AI capabilities in EA with one example each.
~ modeling, governance, repository, draft, drift, search
> AI-assisted modeling drafts Current Architecture from existing documents. AI-supported governance flags drift from standards. Smart repositories use semantic search to find related work across segments.
@short 7
State the three limitations of AI in EA.
~ hallucinated, blind spots, bias
> Hallucinated documentation, governance blind spots where a standard was never documented, and training data bias that carries forward old gaps.
@short 8
Why must an architect review AI drafts?
~ verify, source, hallucination, judgment
> AI can produce plausible but incorrect entries, so a person must verify them against source systems before they become official. AI doesn't replace architectural judgment.

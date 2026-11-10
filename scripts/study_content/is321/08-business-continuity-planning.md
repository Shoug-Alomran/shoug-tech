@head Lecture 8
@title Business Continuity Planning
@sources lecture-8-business-continuity-planning
@count 18
@tldr BCP is deciding in advance how to keep the enterprise running when something goes badly wrong, and it never finishes.
@why There are two models to memorize, the five-stage life cycle and the four phases, and students confuse them. The cost curve and hot or cold site comparison are classic questions.
@connect BCP is the sort of cross-cutting concern that EA has to plan for. The AI section extends the course's recurring theme.
@goals
- Define BCP and senior management's role
- Name the BCP life cycle stages and the four phases
- Explain the disaster recovery cost curve
- Compare hot and cold sites
@vocab
Disaster recovery (DR) | Restoring IT systems after a catastrophic event.
Mitigation | Reducing a risk before it occurs.
Failover | Automatic switch to a backup system.
Anomaly detection | Spotting unusual behaviour in data.
@map
3-5 | BCP, why, and who governs | MEMORIZE | Senior management's duties
6-8 | Life cycle and four phases | MEMORIZE | Two complementary models
9 | Maintaining the plan | SKIM | Everyone's job
10-12 | Disaster recovery | MEMORIZE | Cost curve, hot vs cold
13-16 | AI for BCP | SKIM | Three uses

## What BCP is and who owns it | Slides 3-6 | must
The definition: **a proactive process that identifies and prioritizes an enterprise's critical functions and the likely threats to them, sustained through regular personnel training, plan testing and maintenance.**

**Why do it?** It's the right thing to do for the business, staff and communities. It meets regulations. And it avoids interruptions, financial losses, fines and damage.

**Senior management** is responsible: it defines worst-case scenarios, approves funding and staffing, establishes policy, makes sure that the BCP is reviewed and approved **at least annually**, ensures staff are trained, and makes sure that it's regularly tested.

Three features of how it works: it's a **process, not a project**; methods are based on **established, certifiable disciplines**; and plans **start simple and grow more sophisticated**.

::analogy A fire drill
You don't work out where the exits are while the building is burning. You agree in advance, assign roles and practise regularly.
::
::key
- BCP is proactive and identifies critical functions and threats
- Senior management defines scenarios and approves funding
- The BCP is reviewed and approved at least annually
- BCP is a process and not a project
::

## Two models of the same discipline | Slides 7-8 | must
| | BCP Life Cycle | Four Phases |
|---|---|---|
| Describes | How the **plan gets built and maintained** | The **timeline of an incident** |
| Parts | Identify → Analyze → Design → Execute → Measure | Mitigation → Preparedness → Response → Recovery |
| Continuous? | Yes, a loop | Runs around an incident |

**Life cycle:**
- **Identify:** risk assessment
- **Analyze:** business impact
- **Design:** strategy selection, plan development
- **Execute:** implement
- **Measure:** train, test and maintain

**Four phases:**

| Phase | When | What |
|---|---|---|
| **Mitigation** | Before | Avoid the risk or reduce its impact |
| **Preparedness** | Before | Be as ready as you can |
| **Response** | During | Take reasonable actions as the incident happens |
| **Recovery** | After | Return to normal operations |

::mnemonic My Pets Run Round
**M**itigation, **P**reparedness, **R**esponse, **R**ecovery, in order.
::
::mnemonic I Always Draw Each Map
The life cycle: **I**dentify, **A**nalyze, **D**esign, **E**xecute, **M**easure.
::
::check Installing a backup generator: which phase? And calling staff during an outage?
The generator is **Mitigation** (reducing impact in advance) or Preparedness. Calling staff during the outage is **Response**.
::
::key
- Life cycle: Identify, Analyze, Design, Execute, Measure
- Four phases: Mitigation, Preparedness, Response, Recovery
- The two models are complementary
- Maintaining the BCP is everyone's job
::

## Disaster recovery | Slides 10-12 | must
A **disaster recovery plan** is a detailed process for recovering information or an IT system after a catastrophic event such as fire or flood. Best practices: mind the EA, set up recovery plans in advance, monitor network quality, train staff, ensure fast response.

**The cost curve.** Two costs move in opposite directions as time passes after the disaster.

::plot The optimal plan is where the two costs cross | time from the disaster | cost | 10 | 10
curve cost of downtime 5: 0.5,1 3,2.4 6,5.4 9,9.4
curve cost to recover 2: 0.5,9.4 3,5.6 6,2.6 9,1
dot optimal: 4.55,3.8
::

::analogy Insurance
Pay too little and a disaster ruins you. Pay too much and you waste money every month. The sensible amount sits in between, and that's the crossing point.
::

| | Hot site | Cold site |
|---|---|---|
| Facility | Separate, fully equipped | Separate, no computer equipment |
| Resume | Immediately | Later, after installing equipment |
| Cost | High | Low |

::mnemonic Hot is Happening, Cold is Blank
**H**ot means ready to **h**appen right now. A **c**old site is a **c**lear empty space.
::
::key
- A DR plan details how to recover IT after a catastrophe
- The optimal DR plan is where downtime cost and recovery cost cross
- A hot site is fully equipped and immediate
- A cold site is a space with no computer equipment
::

## AI for continuity | Slides 13-16 | know
| Use | Traditional | With AI |
|---|---|---|
| **Incident prediction** (Identify) | Periodic risk assessments | Anomaly detection continuously flags early warnings |
| **DR optimization** | Once-a-year estimate | Recalculates the cost curve's crossing as systems change |
| **Automated monitoring** (Measure) | Scheduled tests | Continuously verifies backups and failover |

::key
- AI anomaly detection supports the Identify stage
- AI can recompute the optimal DR investment
- Automated monitoring supports the Measure stage
::
@cheat
### BCP definition
- Proactive; critical functions and threats
- Training, testing, maintenance
- Reviewed at least annually
### Life cycle
- Identify, Analyze, Design
- Execute, Measure
### Four phases
- Mitigation, Preparedness
- Response, Recovery
### DR
- Optimal where two costs cross
- Hot: full, immediate, costly
- Cold: empty, slow, cheap
### Senior management
- Defines worst-case scenarios
- Approves funding and staffing
- Ensures testing and training
@mcq 3
BCP is best described as:
+ A proactive process
- A reactive repair after failure
- A one-time document
- A network protocol
> Slide 3.
@mcq 5
Who oversees the BCP process?
+ Senior management
- Only IT support
- External customers
- Interns
> Slide 5.
@mcq 5
The BCP should be reviewed and approved:
+ At least annually
- Every decade
- Only after a disaster
- Never
> Slide 5.
@mcq 7
Which is a stage in the BCP life cycle?
+ Analyze
- Mitigate
- Recover
- Prepare
> Identify, Analyze, Design, Execute, Measure. The others are phases.
@mcq 8
Which is one of the four phases of continuity planning?
+ Preparedness
- Design
- Identify
- Measure
> Mitigation, Preparedness, Response, Recovery.
@mcq 8
Returning to normal operations is:
+ Recovery
- Response
- Mitigation
- Preparedness
> The last phase.
@mcq 11
The optimal DR plan is:
+ Where the cost of unavailability and of recovery cross
- As cheap as possible
- The most expensive available
- At time zero
> Slide 11.
@mcq 12
A hot site is:
+ A fully equipped facility where business can resume immediately
- An empty space
- A hot climate office
- A public cloud account
> Slide 12.
@mcq 12
A cold site has:
+ No computer equipment
- Duplicate live systems
- Immediate failover
- Real-time data replication
> It's just a place to move to.
@mcq 14
AI anomaly detection improves which stage?
+ Identify
- Design
- Recovery
- Mitigation only
> It flags early warning signs.
@short 7
Name both BCP models and list their parts.
~ identify, analyze, design, execute, measure, mitigation, preparedness, response, recovery
> Life cycle: Identify, Analyze, Design, Execute, Measure. Four phases: Mitigation, Preparedness, Response, Recovery.
@short 12
Compare hot and cold sites.
~ equipped, immediately, cost, empty
> A hot site is fully equipped so business can resume immediately, at high cost. A cold site has no computer equipment, so it's cheaper but much slower.
@short 11
Explain the disaster recovery cost curve.
~ unavailability, recovery, cross, optimal
> As time passes after a disaster, the cost of unavailability rises while the cost to recover falls. The optimal disaster recovery plan is at the crossing point.

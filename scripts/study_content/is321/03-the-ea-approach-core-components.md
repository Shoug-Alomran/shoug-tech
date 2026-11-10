@head Lecture 3
@title The EA Approach: Core Components
@sources lecture-3-the-ea-approach-core-components
@count 18
@tldr Every enterprise can be described on five levels from strategy down to wiring, and a change at one level can be traced through all the others.
@why Two things are examined from this lecture: putting a specific item on the correct level, and tracing how one change ripples through them. The Amanah Bank example shows you the exact pattern.
@connect Lecture 2 introduced the cube. Here you learn each level properly, and the AI section previews the course's recurring AI theme.
@goals
- Describe and give an example of each level
- Explain top-down and bottom-up planning
- Trace a strategic goal through all five levels
- Describe three AI uses in EA
@vocab
Open banking | Letting approved outside apps access bank data through secure interfaces.
API | A defined way for software to talk to other software.
LMS | Learning Management System.
Process mining | Analysing logs to see how work really flows.
Predictive analytics | Using historical data to forecast what will happen.
@map
3-4 | Why five levels | MEMORIZE | One structure for the whole enterprise
5-9 | The five levels | MEMORIZE | Layer name and example of each
10 | Top-down and bottom-up | MEMORIZE | Which is the normal direction
11 | Amanah Bank | WRITE | Trace a goal through the levels
12-16 | AI for decision support | MEMORIZE | Three uses and which level
17-18 | Summary | SKIM | Review

## The five levels | Slides 3-9 | must
The approach **organizes everything an enterprise does into five consistent levels**, so the whole enterprise can be documented, compared and changed.

Follow one university initiative through every level:

| Level | Nickname | Defines | Online degree example |
|---|---|---|---|
| **1. Goals & Initiatives** | Strategic layer | Mission, goals, programs | Goal: expand access to remote learners |
| **2. Products & Services** | Delivery layer | What's delivered, and business processes | A fully online bachelor's degree |
| **3. Data & Information** | Knowledge layer | Facts, records, flows, independent of any system | Enrolment records, advising notes |
| **4. Systems & Applications** | Processing layer | Software that processes the data | LMS, student information system |
| **5. Networks & Infrastructure** | Foundation layer | Hardware, networks, cloud | Cloud servers with enough bandwidth |

::analogy Opening a restaurant
**Goal:** be the top family restaurant in town. **Product:** a set family menu. **Data:** recipes and bookings. **Systems:** booking app and till. **Infrastructure:** kitchen, wiring, Wi-Fi. Each layer exists to support the one above.
::
::trap Data is not the database
Level 3 defines **the information itself**, independent of which system stores it. The database software is Level 4 and the server is Level 5.
::
::check Place these: a mission statement, a data dictionary, an HR app, a fibre link, a mobile banking service.
Mission statement: Level 1. Data dictionary: Level 3. HR app: Level 4. Fibre link: Level 5. Mobile banking service: Level 2.
::
::key
- Levels: Goals, Products, Data, Systems, Networks
- Each level supports the one above
- Level 3 defines information independent of any system
::

## Top-down, bottom-up, and the ripple effect | Slides 10-11 | must
| Direction | How it works | Example |
|---|---|---|
| **Top-down** (normal) | A goal creates requirements for products, data, systems, infrastructure | A new strategy needs a new system |
| **Bottom-up** (occasional) | A new technology makes new services or goals possible | Cloud enables new online services |

::steps Amanah Bank's goal ripples through every level
**L1, Goal:** achieve open banking compliance.
**L2, Product:** a new API-based account access product.
**L3, Data:** consent-management records for shared data.
**L4, System:** a new API gateway, deployed to connect outside fintech apps.
**L5, Infrastructure:** secure cloud hosting for the gateway.
::
::tip The chain is your answer template
When asked to "trace a goal through the EA levels", write one line per level, in order, with a concrete item on each.
::
::key
- Requirements normally flow top-down from strategy to infrastructure
- Technology can occasionally enable bottom-up change
- A single goal can be traced through all levels
::

## AI-driven decision support | Slides 12-16 | know
Traditionally EA documentation sat in static files. AI turns it into an active decision-making tool.

| AI use | What it does | Example |
|---|---|---|
| **Strategic decision-making** | Finds patterns across the levels that a person would miss | Spots three products all relying on one ageing system |
| **Business process optimization** | Analyses how work actually flows, recommends automation | Merges two of five manual handoffs |
| **Predictive analytics** | Uses Level 3 data to forecast demand on Levels 4 and 5 | Enrolment up 40% each term, so plan capacity |

Across levels: L1 flags under-resourced goals, L2 recommends process improvements, L3 finds data-quality gaps, L4 surfaces redundant applications, and L5 forecasts capacity.

::key
- AI turns static documentation into a decision-making tool
- Three uses: strategic decisions, process optimization, predictive analytics
- Predictive analytics forecasts demand on systems and infrastructure
::
@cheat
### Levels and nicknames
- L1 Goals: strategic layer
- L2 Products: delivery layer
- L3 Data: knowledge layer
- L4 Systems: processing layer
- L5 Networks: foundation layer
### Planning direction
- Top-down: normal
- Bottom-up: technology enables change
### Amanah Bank chain
- Open banking goal
- API account product
- Consent records
- API gateway
- Secure cloud hosting
### AI uses
- Strategic decisions
- Process optimization
- Predictive analytics
@mcq 7
Student enrolment records defined independently of any system belong to:
+ Data & Information
- Systems & Applications
- Products & Services
- Goals & Initiatives
> Level 3 is defined independent of where it is stored.
@mcq 8
A Learning Management System belongs to:
+ Systems & Applications
- Goals & Initiatives
- Data & Information
- Networks & Infrastructure
> It is a software application.
@mcq 9
Cloud servers belong to:
+ Networks & Infrastructure
- Products & Services
- Systems & Applications
- Data & Information
> Level 5 is the foundation layer.
@mcq 5
A strategic initiative belongs to:
+ Goals & Initiatives
- Products & Services
- Systems & Applications
- Networks & Infrastructure
> Level 1.
@mcq 10
In EA, requirements normally flow:
+ Top-down, from strategy to infrastructure
- Bottom-up in every case
- Sideways between LOBs only
- Randomly
> Bottom-up change happens occasionally.
@mcq 10
A new technology enabling new services is an example of:
+ Bottom-up change
- Top-down change
- A thread
- Governance
> Slide 10, such as cloud computing.
@mcq 11
In the Amanah Bank example, the API gateway is at:
+ Level 4
- Level 1
- Level 2
- Level 5
> It is a system.
@mcq 6
Level 2 is also called the:
+ Delivery layer
- Foundation layer
- Knowledge layer
- Strategic layer
> Products and services delivered to customers.
@mcq 15
Predictive analytics uses data from which level to forecast demand?
+ Level 3
- Level 1
- Level 2
- Level 5
> It uses historical Data & Information to forecast demand on Levels 4 and 5.
@mcq 14
Process mining mainly helps with:
+ Business process optimization
- Writing mission statements
- Buying land
- Hiring executives
> Slide 14.
@short 11
Trace a goal of "24-hour customer support" through all five EA levels.
~ goal, service, data, system, infrastructure
> L1: the 24-hour support goal. L2: a chat support service. L3: customer tickets and history. L4: a chatbot and ticketing application. L5: cloud hosting and network capacity.
@short 10
Compare top-down and bottom-up planning in EA.
~ strategy, requirements, technology, enables
> Top-down starts with strategy, which creates requirements for each lower level and is the normal direction. Bottom-up starts with a technology that makes new services or goals possible.
@short 12
Give two ways AI changes EA documentation.
~ patterns, optimization, forecast, decision
> AI can find patterns across levels to support strategic decisions, and it can forecast demand on systems through predictive analytics. Documentation becomes an active tool rather than a static file.

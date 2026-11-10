@head Lecture 10
@title EA Technology Planning and Intelligent Enterprise Systems
@sources lecture-10-ea-technology-planning-and-intelligent-systems
@count 18
@tldr Five technologies form the plumbing that supports the business, and AI is now making the systems built on that plumbing adapt and predict.
@why The IaaS, PaaS and SaaS comparison was stressed in class, and the handwriting on slide 5 says so. Know the "who controls what" gradient and the definition of each of the five technologies, and you'll have most of this lecture.
@connect Lecture 9 said technology should follow strategy. This lecture covers the technologies themselves, and the AI section continues the course's thread.
@goals

- Define web services, SOA, virtualization and grid computing
- Compare IaaS, PaaS and SaaS by who controls what
- Explain SOA's before and after picture
- Define digital transformation and five traits of the modern architect
- Describe three AI-driven enterprise uses
  @vocab
  Interoperability | Different systems working together.
  Thin client | A simple front end, such as a browser.
  Virtual machine | A software computer running on physical hardware.
  ERP | Enterprise Resource Planning: one system for core business functions.
  IoT | Internet of Things: everyday objects connected to networks.
  @map
  3 | Web services | MEMORIZE | Shared protocols, interoperability
  4-5 | Cloud: NIST and service models | MEMORIZE | Stressed in class
  6-7 | SOA | MEMORIZE | Before and after
  8-9 | Virtualization | MEMORIZE | Many environments on one machine
  10 | Grid computing | MEMORIZE | Geographically dispersed resources
  12-13 | Digital transformation | MEMORIZE | Five traits
  14-16 | AI in enterprise systems | SKIM | ERP, decisions, adaptation

## The five technologies | Slides 3-10 | must

| Technology          | One-line meaning                                                                      | Everyday picture                      |
| ------------------- | ------------------------------------------------------------------------------------- | ------------------------------------- |
| **Web services**    | Web resources using shared protocols, so different vendors' systems can exchange data | A universal plug adapter              |
| **Cloud computing** | On-demand network access to a shared pool of resources                                | Electricity from the grid             |
| **SOA**             | The business as linked, reusable services with defined interfaces                     | LEGO blocks                           |
| **Virtualization**  | Dividing one computer's resources into multiple execution environments                | Apartments in one building            |
| **Grid computing**  | Combining dispersed computing, storage and network resources                          | Many friends each doing part of a job |

### Cloud: the most stressed topic

NIST: _"a model for enabling ubiquitous, convenient, on-demand network access to a shared pool of configurable computing resources that can be rapidly provisioned and released with minimal management effort."_

| Model    | You control                      | Provider controls                           | Examples                     |
| -------- | -------------------------------- | ------------------------------------------- | ---------------------------- |
| **IaaS** | OS and applications              | Physical hardware                           | Amazon EC2, Compute Engine   |
| **PaaS** | Your deployed application        | Platform: OS, runtime, database, web server | Google App Engine, Force.com |
| **SaaS** | Almost nothing but user settings | Everything underneath                       | Gmail, Office 365            |

::analogy Pizza as a service
**IaaS:** you rent a kitchen and make the pizza yourself. **PaaS:** you bring toppings, and the dough, oven and staff are provided. **SaaS:** the pizza arrives at your door, ready to eat.
::
::mnemonic I Pick Software
Control falls as you go: **I**aaS, then **P**aaS, then **S**aaS. **I** control the most, and **S**aaS the least.
::
::example From the handwriting on slide 2
A university using Google Drive and Gmail is a SaaS **user**: the servers are physically hosted on Google's infrastructure.
::
::trap More control means more responsibility
IaaS isn't "better" than SaaS. It's a gradient: more control and more responsibility at the IaaS end, more convenience at the SaaS end.
::

### SOA: from silos to shared services

**Before SOA:** siloed, closed, monolithic and brittle, with order processing and account management each duplicating the same logic. **After SOA:** shared, collaborative, interoperable and integrated. A service is a business task, such as checking a customer's credit rating, that many applications can reuse through a defined interface.

### Virtualization and grid

**Virtualization** maximizes hardware you've already paid for: rather than three physical servers for accounting, marketing and a student portal, one powerful server runs three virtual machines using VMware or Hyper-V. Handwriting on the slide adds that it helps cut operational costs and allows expansion at minimal cost.

**Grid computing** aggregates dispersed resources, giving instant access to massive resources, leveraging existing investments, and staying robust because **if one computer fails, others maintain operations**.

::check A startup deploys its web app without wanting to manage an operating system. Which cloud model?
**PaaS.** The platform is managed for you, and you just deploy your application.
::
::key

- Web services use shared protocols for interoperability
- IaaS: you control OS and apps. PaaS: you control your app. SaaS: only user settings
- SOA turns siloed applications into reusable services
- Virtualization divides one computer into multiple environments
- Grid computing aggregates dispersed resources
  ::

## Digital transformation and AI | Slides 12-16 | know

**Digital transformation** is the profound change of business activities, processes, competencies and models using digital technologies, to meet evolving market and customer expectations. It's enabled by cloud, social, mobile and analytics, and is driven by Big Data and the Internet of Things.

The **five traits of tomorrow's enterprise architect**:

| Trait                         | Means                                                    |
| ----------------------------- | -------------------------------------------------------- |
| **Analytical problem solver** | Grasps and structures information quickly                |
| **Data-driven decisions**     | Treats data as a strategic asset                         |
| **Tech-savvy**                | Knows APIs, microservices, DevOps                        |
| **Collaborator**              | Facilitates collaboration, close to every C-suite office |
| **Agile**                     | Fluent in Scrum and Kanban: leaves the "ivory tower"     |

**Intelligent enterprise systems:**

| AI use                        | What it adds                                                        |
| ----------------------------- | ------------------------------------------------------------------- |
| **AI-powered ERP**            | Embeds machine learning in core processes, forecasting demand       |
| **Decision support**          | Recommends specific actions, instead of only presenting a dashboard |
| **AI-enabled transformation** | Systems continuously learn and adjust their processes               |

::key

- Digital transformation uses digital technologies to change processes and models
- Five traits: analytical, data-driven, tech-savvy, collaborative, agile
- AI-powered ERP embeds machine learning into core processes
  ::
  @cheat

### Five technologies

- Web services: shared protocols
- Cloud: on-demand shared pool
- SOA: reusable services
- Virtualization: many on one machine
- Grid: dispersed resources together

### Cloud control

- IaaS: OS and apps
- PaaS: your app
- SaaS: user settings only

### Examples

- IaaS: Amazon EC2
- PaaS: Google App Engine
- SaaS: Gmail, Office 365

### SOA

- Before: siloed, brittle
- After: shared, interoperable

### Digital transformation

- Driven by Big Data and IoT
- Five architect traits
  @mcq 5
  In IaaS, the customer controls:

* The OS and applications

- Only user settings
- Physical hardware
- Nothing

> Slide 5.
> @mcq 5
> Gmail is an example of:

- SaaS

* IaaS
* PaaS
* Grid computing

> It's a ready-to-use application.
> @mcq 5
> Google App Engine is an example of:

- PaaS

* IaaS
* SaaS
* SOA

> It provides a platform on which you deploy your app.
> @mcq 5
> Amazon EC2 is an example of:

- IaaS

* PaaS
* SaaS
* Virtual reality

> Virtualized compute, storage and networking.
> @mcq 3
> Web services mainly provide:

- Interoperability between different systems

* Faster printers
* Physical security
* Employee training

> They use shared protocols and standards.
> @mcq 7
> SOA replaces siloed applications with:

- Shared, reusable services

* Larger monolithic systems
* Paper-based processes
* A single spreadsheet

> Slide 7's before and after.
> @mcq 8
> Virtualization mainly helps to:

- Maximize existing hardware

* Eliminate software
* Make hardware physically bigger
* Replace networking

> Slide 8.
> @mcq 10
> Grid computing is:

- An aggregation of geographically dispersed resources

* One large single server
* A type of spreadsheet
* A printing standard

> Slide 10.
> @mcq 12
> Digital transformation is driven by data and:

- The Internet of Things

* Fax machines
* Paper archives
* Fixed office hours

> Slide 12.
> @mcq 5
> Moving from IaaS to SaaS, the customer gets:

- Less control and more convenience

* More control and less convenience
* The same control throughout
* Physical hardware ownership

> It's a control gradient.
> @short 5
> Compare IaaS, PaaS and SaaS, stating who controls what and giving an example.
> ~ OS, platform, application, control, provider
> IaaS: you control the OS and apps, and the provider runs hardware, such as Amazon EC2. PaaS: you control your deployed app, and the provider runs the platform, such as Google App Engine. SaaS: you control only settings and the provider does everything else, such as Gmail.
> @short 7
> Explain how SOA improves on siloed systems.
> ~ reusable, services, interface, duplicate, interoperable
> Siloed systems duplicate logic and are brittle. SOA exposes business tasks as reusable services with defined interfaces, making applications interoperable and easier to change.
> @short 8
> Describe how virtualization saves money, with an example.
> ~ one server, virtual machines, hardware, cost
> One powerful physical server can run several virtual machines instead of buying a separate server for each system. For example, a university can run accounting, marketing and the student portal on one machine.

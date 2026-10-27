"""SE423 Chapter 1 (Introduction): page content for the annotated deck.

Schema: see annotated_page.py. The principle cards (slides 59–70) are pictures, so their marks use 'ocr' (skipped
if OCR can't read them). Past-exam questions are copied from the papers in exams/ and from the instructor's own
2026 midterm (m261); everything else is a prediction. The instructor tests understanding and application, not
statistics or history, so the statistics slides get context notes but no questions.
"""
from .common import asked, likely

TITLE = 'Introduction to Software Project Management'
CHAPTER = 'SE423 · Chapter 1'

OVERVIEW = {
    'summary': ('Chapter 1 gives the vocabulary for the whole course. It defines project management, places it in '
                'history, describes what a project manager does and needs to be good at, and then works through the '
                'PMBOK 7 standard: the 12 principles (how to behave) and 8 performance domains (what to manage), the key '
                'terms (portfolio, program, project, product, outcome, value), the system for value delivery with its '
                'governance, functions and environment, and how product management relates to projects. The last part '
                'gives each principle its own card.'),
    'ideas': [
        ('Principles vs. domains', '12 principles guide behaviour (stewardship, team, value, systems thinking…); 8 performance domains are areas of focus that run at the same time. Neither is a set of steps.'),
        ('Portfolio, program, project', 'Portfolio = grouped for strategy (may be unrelated, includes operations). Program = related projects for extra benefits. Project = temporary + unique.'),
        ('Value chain', 'Components → deliverables → outcomes → benefits → value. Value is the ultimate measure of success.'),
        ('Coordination', 'Decentralized: authority spread across a self-organizing team. Centralized: a designated PM leads. Both can be mixed.'),
    ],
    'sections': [
        ('Slides 1–6', 'What project management is and why it matters'),
        ('Slides 7–13', 'History, PMOs, global issues, certification, ethics'),
        ('Slides 14–18', 'Project managers: responsibilities, skills, competencies, advantages of formal PM'),
        ('Slides 19–28', 'PMBOK: the standard, 12 principles, 8 domains, key terms'),
        ('Slides 29–45', 'The system for value delivery: value, information flow, governance, functions, environment'),
        ('Slides 46–52', 'Product management considerations'),
        ('Slides 53–70', 'The 12 principles in detail'),
    ],
    'exam': ('Midterm 251 (both versions) took six MCQs from this deck: decentralized decision-making, program, performance '
             'domains, stewardship, system for value delivery, and (from 1.2) cadence. The instructor’s 2026 midterm asked '
             'project vs. product management and two principle scenarios (Focus on Value; system interactions). Finals asked '
             'about constraints, the PMO, and PM vs. general management. She tests application, so expect scenarios that '
             'name a situation and ask which principle, term or coordination style applies.'),
}

TITLES = {3: 'Introduction (section)', 7: 'Project Management History (section)', 14: 'Project Managers (section)',
          19: 'Project Management Body of Knowledge (section)', 23: 'Key Terms and Concepts (section)',
          29: 'A System for Value Delivery (section)', 53: 'Project Management Principles (section)'}

SLIDES = {
    1: dict(
        hl=[('Introduction', 1), ('SE423: Software Project Management', 2)],
        notes=['This deck is the language of the course: every later chapter assumes the terms defined here (project, program, portfolio, value, principles, performance domains).',
               'The examinable core is slides 20–52 (the PMBOK standard, key terms and the system for value delivery) plus the principle cards on 59–70. The early slides on statistics and history are context.']),
    2: dict(
        hl=[('Introduction', 1), ('Project Management History', 2), ('Project Managers', 3), ('PMBOK', 4)],
        notes=['**Introduction**: what project management is and why organizations care about it.',
               '**History**: from early large projects to the Manhattan Project and the PMOs of the 1990s.',
               '**Project managers**: what they are responsible for, the skills they need, and the 14 competencies.',
               '**PMBOK**: the biggest and most examined part: the standard, the 12 principles, the 8 performance domains, key terms and the system for value delivery.']),
    3: dict(notes=['Section divider: why project management matters.']),
    4: dict(
        hl=[('knowledge, skills, tools, and techniques', 1), ('guiding the project work', 2), ('predictive, hybrid, and adaptive', 3)],
        notes=['**Definition**: project management is the application of **knowledge, skills, tools and techniques** to project activities to meet project requirements. Learn the four nouns exactly; distractors swap one for “budgets”, “contracts” or “policies”.',
               'Project management is about **guiding** the work toward the intended outcomes, not doing the work itself. The developers write the code; the PM makes sure the work adds up to the outcome the organization wanted.',
               'Teams can get there with a range of approaches: **predictive** (plan everything up front, waterfall), **adaptive** (iterate and adjust, agile) and **hybrid** (a mix). Chapter 4 explains how to choose; here it is enough that no single approach is required.'],
        exam=[likely('Project management is the application of ______ to project activities to meet project requirements.', a=0,
                     opts=['Knowledge, skills, tools, and techniques', 'Budgets, schedules, and contracts', 'People, processes, and products', 'Policies, procedures, and standards'])]),
    5: dict(
        hl=[('new or renewed interest', 1), ('87.7 million', 2), ('2.3 million', 2)],
        notes=['Organizations are paying new attention to project management because more and more of their work is organized as projects.',
               'The PMI figures show the demand: 87.7 million people in PM-oriented roles needed by 2027, and 2.3 million new PM employees each year until 2030. These are context for why the course matters; the instructor does not test statistics.']),
    6: dict(
        hl=[('team-work, problem-solving, and', 1), ('$97 million for every $1 billion', 2), ('Saudi Smart Government Strategy', 3)],
        notes=['The skills employers want most from new graduates (teamwork, problem-solving, verbal communication) are all PM skills, which is why PM is taught to software engineers.',
               'Organizations waste about **$97 million of every $1 billion** spent on projects (about 10%). That waste, from poor planning, unclear scope and weak control, is the argument for formal project management (slide 18).',
               'The Saudi figures (AI market, record technology spending) show the local demand: large national technology programs need people who can manage projects. Context only, not examined.']),
    7: dict(notes=['Section divider: the history of the profession.']),
    8: dict(
        hl=[('growing at a very rapid pace', 1), ('history', 2), ('professional societies', 2), ('project management software', 2)],
        notes=['The profession is growing quickly.',
               'Three things explain it: its **history** (next slides), its **professional societies** such as PMI (slide 12), and the growth of **project management software** (scheduling tools such as Gantt-chart software, Chapter 6.2).']),
    9: dict(
        hl=[('Egyptian pyramids', 1), ('Manhattan Project', 2), ('separate', 3), ('technical manager', 3)],
        notes=['Some argue that the Egyptian pyramids and the Great Wall of China were projects: large, unique, temporary efforts with a goal.',
               'The **Manhattan Project** is usually considered the first to use **modern** project management.',
               'Its structure is the lesson: a **separate project manager and technical manager**. Managing the project (schedule, people, resources) and leading the technology are different jobs, a split that returns in Chapter 3 as project vs. technical leadership. (History is context; the instructor does not ask dates or figures.)']),
    10: dict(
        hl=[('In the 1990s', 1), ('PMOs', 1), ('Project Management Office (PMO)', 2), ('coordinating the project management function', 2)],
        notes=['In the 1990s, companies began creating **PMOs** because they had more projects, and more complex ones, than they could coordinate informally.',
               '**Definition**: a **Project Management Office (PMO)** is an organizational unit responsible for **coordinating the project management function** throughout an organization. In practice it sets PM standards and templates, supports and trains project managers, coordinates resources and priorities across projects, and reports project performance to senior management. (The chart shows that the larger the company, the more likely it has a PMO.)'],
        exam=[asked('f242', 'Q1.3', 'What is a Project Management Office (PMO) and its role in organizations?',
                    a='A PMO is a centralized organizational unit that oversees and standardizes how projects are managed. It sets PM standards, methods and templates, trains and supports project managers, monitors and reports on project performance, and coordinates resources across projects. Its control ranges from supportive (consultative) to controlling (requires compliance) to directive (manages the projects directly).')]),
    11: dict(
        hl=[('Talent development', 1), ('Basic project management techniques', 2), ('more agile approaches', 3), ('Benefits realization', 4)],
        notes=['**Talent development** for project and program managers is a top concern: organizations can’t find enough capable PMs.',
               'Basic PM techniques are now **core competencies** expected of many roles, not just of PMs.',
               'Organizations want **more agile** approaches (Chapter 4).',
               '**Benefits realization** is a key metric: success is judged by whether the project delivered the benefits it promised, not only by whether it finished on time. This is the outcome → benefit → value chain on slide 34.']),
    12: dict(
        hl=[('Project Management Institute', 1), ('Project Management Professional', 2), ('Certified Associate in Project', 3)],
        notes=['The **Project Management Institute (PMI)** is the leading professional body for project management, and it publishes the PMBOK standard this course follows.',
               'PMI certifies experienced practitioners as **Project Management Professionals (PMP)**; the chart shows the number of PMP holders more than doubling over ten years.',
               'Students can join at a reduced fee and earn the entry-level **Certified Associate in Project Management (CAPM)**. (Certificate names are context; the instructor does not test them.)']),
    13: dict(
        hl=[('set of principles that guide our decision', 1), ('ethical dilemmas', 2), ('Code of Ethics and Professional Conduct', 3)],
        notes=['**Ethics**: a set of principles that guide decisions based on personal values of right and wrong.',
               'Project managers often face **ethical dilemmas**: pressure to hide a delay from the client, to approve work that doesn’t meet quality, or to favor a vendor.',
               'PMI’s **Code of Ethics and Professional Conduct**, which every PMP must accept, rests on four values (slide 55): responsibility, respect, fairness, honesty. It connects to the stewardship principle (slide 59).']),
    14: dict(notes=['Section divider: the project manager’s role.']),
    15: dict(
        hl=[('Schedule', 1), ('Budget', 1), ('Quality', 1), ('Delivery of products', 2), ('Locking in resources', 2), ('chasing and collecting the status', 3)],
        notes=['The PM is responsible for everything that affects the project. The classic three are **schedule, budget and quality**: the competing constraints the PM keeps in balance. Shortening the schedule usually costs money or quality; cutting the budget costs time or scope.',
               'Also **delivering the products** to the customer and **locking in resources** (people, equipment) before they are taken by other projects.',
               'In practice, much of a PM’s time goes to **chasing and collecting the status** of tasks. That is why tracking tools exist: status reports, burndown charts and earned value (Chapter 6.2).'],
        exam=[asked('f242', 'Q1.1', 'Define the term ‘project constraints’ and explain how they influence project planning and execution. Provide at least three examples of common constraints and discuss their interrelationship.',
                    a='Project constraints are the limits a project must be delivered within. The classic three are scope, time and cost, often with quality, resources and risk. They drive planning because every schedule, budget and scope decision has to fit inside them, and during execution the PM keeps trading them off. They are interrelated (the triple constraint): cutting the schedule usually needs more cost or less scope, and adding scope needs more time or money; quality sits in the middle and suffers if they are squeezed.')]),
    16: dict(
        hl=[('planning, scheduling, coordinating', 1), ('experienced', 2), ('comfortable with change', 3), ('Understand the organizations', 3), ('lead teams', 3)],
        notes=['Job descriptions vary, but the PM’s role is consistently **planning, scheduling, coordinating and working with people** to reach the project goals.',
               'Successful projects are mostly led by **experienced** PMs, who know how to influence the factors that make a project succeed.',
               'Three skills the slide singles out: be **comfortable with change** (plans will change), **understand the organization** you work in (its culture, politics and structure, Chapter 2), and be able to **lead teams** toward the goals (Chapter 3).']),
    17: dict(
        hl=[('People skills', 1), ('Leadership', 1), ('Strong at building trust', 2), ('Conflict resolution', 3), ('Negotiating', 3), ('Process and technical', 4)],
        notes=['Fourteen competencies. Most are **people** competencies: people skills, leadership, listening, verbal communication, building teams, mentoring.',
               '**Trust and integrity** (building trust, ethical and consistent behavior) are what make people follow a PM who often has no formal authority over them.',
               '**Organizational and political** competencies: conflict resolution, negotiating, influencing the organization, understanding and balancing priorities, critical thinking.',
               'Only one is technical: **process and technical expertise**. A PM is mostly a people role; the instructor’s scenarios usually ask which people skill a situation calls for.'],
        exam=[likely('Two senior developers keep arguing about the architecture in every meeting, and the rest of the team has stopped contributing. Which project manager competencies does this call for, and what should the PM do?',
                     a='Conflict resolution/management, listening and building trust (plus team building). The PM should bring the disagreement into the open, keep it about the ideas rather than the people, make sure everyone is heard, and drive the group to a decision that the whole team commits to.')]),
    18: dict(
        hl=[('Better control of financial, physical, and human resources', 1), ('Shorter development times', 2), ('Higher quality', 2), ('Positive impact on meeting strategic goals', 3), ('Higher worker morale', 4)],
        notes=['**Resources and money**: better control of financial, physical and human resources, lower costs, higher productivity and profit margins.',
               '**Time and quality**: shorter development times, higher quality and reliability, better customer relations.',
               '**Strategy**: better internal coordination and a positive impact on meeting strategic goals (projects are how strategy gets carried out, Chapter 2).',
               '**People**: higher morale and less overworked staff, because work is planned instead of rushed.'],
        exam=[asked('f251', 'Q1.1', 'How does project management contribute to organizations in achieving their strategic objectives? Please elaborate.',
                    a='Strategy is carried out through projects. Project management selects and prioritizes projects (through portfolios and programs) so they align with strategic objectives, then delivers them so the outputs create the intended outcomes, benefits and value. It uses limited resources efficiently, controls scope, time and cost, and manages risk and change. That lets the organization reach its goals and respond to its market faster than competitors.')]),
    19: dict(notes=['Section divider: the PMBOK standard (7th edition), the core of the chapter.']),
    20: dict(
        hl=[('basis for understanding project management', 1), ('regardless of industry, location, size, or delivery', 2), ('governance', 3), ('product management', 3)],
        notes=['The **Standard for Project Management** gives a common basis for understanding project management and how it produces the intended outcomes.',
               'It applies **regardless of industry, location, size or delivery approach** (predictive, hybrid or adaptive). A statement that it applies only to large, software or waterfall projects is false.',
               'It describes the **system** projects operate in: governance, the functions around projects, the project environment, and the relationship with product management. Those are exactly the sections on slides 30–52.']),
    21: dict(
        hl=[('Stewardship', 1), ('Team', 2), ('Stakeholders', 2), ('Value', 3), ('Systems Thinking', 3), ('Tailoring', 4), ('Quality', 4), ('Risk', 5), ('Adaptability and Resiliency', 5), ('Change', 5)],
        notes=['The **12 principles** describe how people on a project should **behave**; slides 59–70 give each one a card. Remember 12 principles vs. 8 performance domains (next slide). **Stewardship**: act responsibly and ethically with resources and people.',
               '**Team** (trust, respect, open communication) and **Stakeholders** (involve them proactively): the people principles.',
               '**Value** (prioritize what delivers value), **Systems thinking** (see how parts interact) and **Leadership**: the direction principles.',
               '**Tailoring** (adapt methods to the context), **Quality** (build it in from the start) and **Complexity**: the delivery principles.',
               '**Risk**, **Adaptability and resiliency** (bend with change, recover from setbacks) and **Change** (support the transition to the future state): the uncertainty principles.'],
        exam=[asked('m251v1', 'MCQ 5', 'Which of the following best reflects the principle of “Stewardship” in project management?',
                    a=1, opts=['Delegating all responsibility for ethical practices to external auditors', 'Taking personal responsibility for the careful use of resources, upholding values, and acting with integrity',
                               'Focusing only on delivering project outputs, regardless of long-term impacts.', 'Ensuring accountability is limited to the project sponsor alone.'],
                    why='Stewardship means acting with integrity, care, trustworthiness and compliance, inside and outside the organization. (Also Midterm 251 V2 MCQ 4.)'),
              asked('m261', 'MCQ', 'A project team has limited resources and must choose the feature that will provide the greatest benefit to users. Which principle applies?',
                    a=0, opts=['Focus on Value', 'Navigate Complexity', 'Embrace Adaptability and Resiliency', 'Tailor Based on Context'],
                    why='Value is the ultimate indicator of project success; prioritizing the most beneficial feature is focusing on value.')]),
    22: dict(
        hl=[('key areas of focus', 1), ('Stakeholders', 2), ('Development Approach and Life Cycle', 2), ('Planning', 2), ('Delivery', 2), ('Measurement', 2), ('Uncertainty', 2)],
        notes=['A **performance domain** is a group of related activities that is a **key area of focus** for delivering project outcomes. The domains are **not** phases or steps done in order: they run at the same time and interact. They are also not optional and not deliverables.',
               'The eight: **stakeholders, team, development approach and life cycle, planning, project work, delivery, measurement, uncertainty**. Chapter 1.2 gives each its own section. Distractors often list “procurement” or “integration”, knowledge areas from older PMBOK editions.'],
        exam=[asked('m251v1', 'MCQ 3', 'Which of the following best explains the nature of project performance domains?',
                    a=0, opts=['They represent distinct areas of focus that guide effective project management.', 'They are rigid processes that must be followed in order, from initiation to closure.',
                               'They are optional tools that project managers may use only in large projects.', 'They are specific deliverables required at the end of each project phase.'],
                    why='Performance domains are areas of focus that run concurrently; they are not sequential processes or deliverables. (Also Midterm 251 V2 MCQ 1.)')]),
    23: dict(notes=['Section divider: the key terms. These definitions are examined word for word, and the instructor likes near-identical terms (program vs. portfolio, project vs. product).']),
    24: dict(
        hl=[('Outcome', 1), ('benefits and value', 1), ('Portfolio', 2), ('strategic objectives', 2), ('Product', 3), ('quantifiable', 3)],
        notes=['**Outcome**: an end result or consequence of a process or project. It can include outputs, but it focuses on the **benefits and value** the project was meant to deliver. An app is an output; customers ordering 30% faster is an outcome.',
               '**Portfolio**: projects, programs, subsidiary portfolios and **operations** managed as a group to achieve **strategic objectives**. Its items don’t have to be related (a company’s R&D, marketing campaigns and infrastructure upgrades), and it is the only grouping that includes operations.',
               '**Product**: an artifact that is produced and **quantifiable**, either an end item itself or a component of one.'],
        exam=[likely('“Projects, programs, subsidiary portfolios, and operations managed as a group to achieve strategic objectives” defines a:', a=0,
                     opts=['Portfolio', 'Program', 'Product', 'Value stream'])]),
    25: dict(
        hl=[('Program', 1), ('benefits not available from managing them', 1), ('Project', 2), ('temporary endeavor', 2), ('unique product, service, or result', 2), ('stand alone', 3)],
        notes=['**Program**: **related** projects, subsidiary programs and program activities managed in a coordinated way to obtain **benefits not available from managing them individually** (e.g. a company-wide digital transformation). The tell-tale phrase is “benefits not available individually”.',
               '**Project**: a **temporary endeavor** undertaken to create a **unique product, service or result**. Temporary means it has a defined beginning and end, not that it is short; a three-year project is still temporary. Repeated work such as monthly payroll is an operation, not a project.',
               'Projects can **stand alone** or be part of a program or portfolio; they don’t have to belong to one.'],
        exam=[asked('m251v1', 'MCQ 2', 'A group of related projects managed in a coordinated manner to obtain benefits not available from managing them individually is called a:',
                    a=0, opts=['Program', 'Portfolio', 'Project', 'Value stream'],
                    why='A program is related projects managed together for benefits; a portfolio groups projects, programs and operations for strategic objectives and they can be unrelated. (Also Midterm 251 V2 MCQ 3, options shuffled.)')]),
    26: dict(
        hl=[('assigned by the performing organization', 1), ('facilitating the project', 2), ('managing the processes', 2)],
        notes=['The **project manager** is the person **assigned by the performing organization** to lead the team responsible for achieving the project objectives (not elected by the team, not chosen by the customer).',
               'The PM does two kinds of work: **facilitating** the team’s work toward the outcomes (removing obstacles, coordinating people) and **managing the processes** that deliver them (planning, tracking, controlling).']),
    27: dict(
        hl=[('Project team', 1), ('Project Management Team', 2), ('directly involved in project', 2), ('System for value delivery', 3), ('Portfolios, programs, projects, products, and operations', 3)],
        notes=['**Project team**: everyone performing the project’s work.',
               '**Project management team**: the members **directly involved in managing** the project. It is a subset of the project team: everyone works on the project, only some manage it.',
               '**System for value delivery**: a collection of strategic business activities aimed at building, sustaining or advancing an organization. **Portfolios, programs, projects, products and operations** can all be part of it; none is the sole contributor.'],
        exam=[asked('m251v1', 'MCQ 9', 'In the context of the “system for value delivery,” which of the following is the most accurate statement?',
                    a=1, opts=['Only portfolios and programs contribute to value delivery in an organization, while projects and products have no significant role.',
                               'A system for value delivery includes portfolios, programs, projects, products, and operations, all working together to build, sustain, or advance an organization.',
                               'Value delivery systems are only relevant to large organizations and do not apply to smaller projects.',
                               'Products are the sole contributor to value delivery, with programs and projects playing a supporting role only.'],
                    why='The value delivery system is the whole set of portfolios, programs, projects, products and operations working together. (Also Midterm 251 V2 MCQ 10.)')]),
    28: dict(
        hl=[('worth, importance, or usefulness', 1), ('Different stakeholders perceive value', 1), ('Customers', 2), ('business value', 3), ('Societal value', 4)],
        notes=['**Value** is the worth, importance or usefulness of something, and **different stakeholders perceive it differently**: the same product can be valuable to one group and not to another.',
               '**Customers** see value in being able to use specific features or functions.',
               '**Organizations** see **business value**, measured financially: the benefits minus the cost of achieving them.',
               '**Society** sees value in contributions to communities, groups or the environment.'],
        exam=[likely('An organization measures a project’s “benefits less the cost of achieving those benefits”. Which type of value is this?', a=0,
                     opts=['Business value', 'Customer value', 'Societal value', 'Technical value'])]),
    29: dict(notes=['Section divider: the system for value delivery. Slide 30 is the map for slides 31–52.']),
    30: dict(
        hl=[('context for value delivery', 1), ('How to Create Value', 2), ('Organizational Governance System', 3), ('Functions Associated with Projects', 4), ('The Project Environment', 5), ('Product Management Considerations', 6)],
        notes=['The system for value delivery gives the context for value delivery, governance, project functions, the project environment and product management.',
               '**Creating value** (slides 31–36): how projects operate inside a system to produce value for the organization and its stakeholders.',
               '**Governance** (37–38): the policies and oversight that guide the system.',
               '**Functions** (39–42): the roles that support projects.',
               '**Environment** (43–45): the internal and external factors that influence projects.',
               '**Product management** (46–52): how portfolios, programs, projects and products relate.']),
    31: dict(
        hl=[('larger system', 1), ('new product, service, or result', 2), ('social or environmental contributions', 2), ('Improving efficiency', 2), ('desired future state', 2), ('Sustaining benefits', 2)],
        notes=['Projects exist inside a **larger system** (a government agency, an organization, a contract), and organizations use them to create value for stakeholders.',
               {'text': 'Five ways projects create value:', 'items': [
                   ('New product, service or result', 'Meeting customers’ or users’ needs (a new banking app).'),
                   ('Social or environmental contribution', 'A public-health portal, an energy-saving system.'),
                   ('Efficiency and responsiveness', 'Tablets replacing paper forms so nurses spend less time on admin.'),
                   ('Enabling change', 'Moving the organization to its desired future state (a digital transformation).'),
                   ('Sustaining benefits', 'Keeping benefits from earlier programs, projects or operations going (upgrading a system that still serves customers).')]}],
        exam=[likely('A hospital project replaces paper forms with tablets so nurses spend less time on administration. Which way of creating value does it show?', a=0,
                     opts=['Improving efficiency, productivity, effectiveness, or responsiveness', 'Creating positive social or environmental contributions', 'Sustaining benefits from previous programs', 'Creating a new product for customers'])]),
    32: dict(
        hl=[('individually and collectively', 1), ('aligned with the organization', 2), ('Operations can directly support', 3), ('influence each other', 4)],
        notes=['Portfolios, programs, projects, products and operations can create value **individually and collectively**.',
               'Together they form a system for delivering value **aligned with the organization’s strategy**; any project or program can include products.',
               '**Operations** (payroll, supply chain, finance, HR, customer service) are the ongoing work. They directly support portfolios, programs and projects, and they receive what projects deliver.',
               'Portfolios, programs and projects **influence each other** and operations; the diagram shows the nested boxes with operations alongside.']),
    33: dict(
        hl=[('internal environment', 1), ('policies, procedures, methodologies', 1), ('external environment', 2), ('economy', 2)],
        notes=['The value delivery system sits inside the organization’s **internal environment**, which is governed by its policies, procedures, methodologies, frameworks and governance structures.',
               'That internal environment sits inside the **external environment**: the economy, competitors, laws. Read the diagram as nested boxes: system ⊂ internal environment ⊂ external environment (slides 44–45 list each).']),
    34: dict(
        hl=[('deliverables used', 1), ('outcome is the end result', 2), ('long-', 2), ('benefits, which are gains', 3), ('Benefits, in turn, create value', 4)],
        notes=['The components of the system create **deliverables**, and deliverables are used to produce **outcomes**.',
               'An **outcome** is the end result or consequence of a process or project. Focusing decisions on outcomes (not just deliverables) emphasizes the project’s **long-range** performance.',
               'Outcomes create **benefits**: gains realized by the organization.',
               'Benefits create **value**: something of worth, importance or usefulness. The full chain: components → deliverables → outcomes → benefits → value.'],
        exam=[likely('Which sequence matches the value delivery chain?', a=0,
                     opts=['Deliverables → outcomes → benefits → value', 'Benefits → outcomes → deliverables → value', 'Value → benefits → outcomes → deliverables', 'Outcomes → deliverables → value → benefits'])]),
    35: dict(
        hl=[('information and', 1), ('feedback are shared consistently', 1), ('Senior leadership shares strategic information', 2), ('Portfolios share the desired outcomes', 3), ('Deliverables from', 4)],
        notes=['A value delivery system works best when **information and feedback flow consistently** between its parts, keeping it aligned with strategy and the environment.',
               '**Senior leadership → portfolios**: strategic information.',
               '**Portfolios → programs and projects**: the desired outcomes, benefits and value.',
               '**Programs and projects → operations**: the deliverables, with information on how to support and maintain them. This is the downward flow: “what we want”.']),
    36: dict(
        hl=[('Information from operations', 1), ('adjustments, fixes, and updates', 1), ('performance information', 2), ('evaluations on portfolio', 3), ('strategy is advancing', 4)],
        notes=['The upward flow, “how it is going”. **Operations → programs and projects**: suggestions for adjustments, fixes and updates to deliverables (bugs found in use, change requests).',
               '**Programs and projects → portfolios**: performance information and progress toward the desired outcomes, benefits and value.',
               '**Portfolios → senior leadership**: evaluations of portfolio performance.',
               '**Operations → the organization**: information on how well the strategy is advancing.'],
        exam=[likely('Information flowing from operations back to programs and projects mainly suggests:', a=0,
                     opts=['Adjustments, fixes, and updates to deliverables', 'New strategic objectives', 'Portfolio performance evaluations', 'The project budget'])]),
    37: dict(
        hl=[('governance system works alongside', 1), ('framework with functions and processes', 2), ('oversight, control, value assessment', 3), ('evaluating', 4)],
        notes=['The **governance system** works alongside the value delivery system to keep work flowing, manage issues and support decisions.',
               'It provides a **framework of functions and processes** that guide activities: the rules and the decision rights.',
               'A governance framework can include **oversight, control, value assessment, integration** among components, and **decision-making** capabilities.',
               'It gives an integrated structure for **evaluating changes, issues and risks** from the environment or any component.']),
    38: dict(
        hl=[('portfolio objectives, program benefits, and deliverables', 1), ('project management office', 2), ('authority to approve changes', 3), ('aligned with program', 4)],
        notes=['Governance covers each level: **portfolio objectives, program benefits and project deliverables**.',
               'Projects can sit in a program or portfolio or stand alone; in some organizations a **PMO** supports programs and projects within a portfolio.',
               '**Project governance** defines the **authority to approve changes** and make other business decisions on the project (who can approve a scope change, a budget increase). Chapter 9’s change control board is an example.',
               'Project governance is **aligned with** program and organizational governance, so a project can’t set rules that contradict the organization’s.'],
        exam=[likely('Defining who has the authority to approve changes on a project is part of:', a=0,
                     opts=['Project governance', 'The project environment', 'Product management', 'Benefits realization'])]),
    39: dict(
        hl=[('People drive project delivery', 1), ('one person, by a group of people', 2), ('Coordinating a collective work effort', 3), ('decentralized coordination', 4)],
        notes=['**People drive project delivery** by carrying out the functions a project needs.',
               'A function can be fulfilled by **one person, a group, or combined into defined roles**; there is no fixed one-person-per-function rule.',
               '**Coordinating** the collective effort is critical, and the right type of coordination depends on the context.',
               '**Decentralized coordination**: team members **self-organize and self-manage**, so decision-making authority is spread across the team and accountability is shared (as in Scrum, Chapter 4).'],
        exam=[asked('m251v1', 'MCQ 1', 'In decentralized project management, decision-making authority is primarily:',
                    a=0, opts=['Distributed among team members to encourage shared accountability.', 'Concentrated in the hands of a single project manager.',
                               'Transferred to external auditors for oversight.', 'Reserved exclusively for senior executives in the organization.'],
                    why='Decentralized management spreads decisions across the team; centralized puts them with one person such as the PM. (Also Midterm 251 V2 MCQ 2.)')]),
    40: dict(
        hl=[('centralized coordination', 1), ('designated project manager', 1), ('self-organized project teams for portions', 2), ('continuous engagements', 3)],
        notes=['**Centralized coordination**: a **designated project manager** (or similar role) leads and guides. This is the distractor in the decentralized MCQ.',
               'The two can be mixed: a centrally coordinated project can include **self-organized teams for portions** of the work (a PM leads a compliance project while the UI team plans its own sprints).',
               'Whatever the style, **continuous engagement** between the team and stakeholders is necessary for success.'],
        exam=[likely('A government system has a strict compliance deadline and a designated PM, but the UI team works in two-week sprints and plans its own tasks. Which coordination style is this?',
                     a='Centralized coordination (a designated PM leads the project) with a self-organized team for a portion of the work, a combination the slide explicitly allows.')]),
    41: dict(
        hl=[('collective effort of the', 1), ('additional functions', 2), ('needs of the project, organization, and environment', 3)],
        notes=['However a project is coordinated, it is the **collective effort** of the team that delivers outcomes, benefits and value.',
               'The team may be supported by **additional functions** depending on the deliverables, industry and organization (legal review, security, procurement).',
               'The **needs of the project, organization and environment** decide which functions are used and how: there is no fixed list. It is tailoring applied to roles.']),
    42: dict(
        hl=[('Provide oversight and coordination', 1), ('Present objectives and feedback', 2), ('Facilitate and support', 3), ('Apply expertise', 4), ('Provide business direction', 5), ('Provide resources and direction', 6), ('Enforcing regulatory and internal standards', 7)],
        notes=['**Oversight and coordination**: monitoring progress and performance (usually the PM).',
               '**Objectives and feedback**: defining success criteria (where we are going) and feedback (how far we have come), usually the customer or product owner.',
               '**Facilitate and support**: hosting meetings, workshops and stand-ups (a Scrum master). **Perform work and contribute insights**: completing deliverables (the team).',
               '**Apply expertise**: advising on technical or domain matters (a subject-matter expert).',
               '**Business direction and insight**: market trends and customer needs (a product owner).',
               '**Resources and direction**: allocating budget, people and infrastructure (the sponsor).',
               '**Maintain governance**: enforcing regulatory and internal standards (a PMO or governance board).'],
        exam=[likely('A sponsor approves the budget and assigns two extra engineers to the project. Which project function is this?', a=0,
                     opts=['Provide resources and direction', 'Apply expertise', 'Present objectives and feedback', 'Perform work and contribute insights']),
              likely('A product owner tells the team that customers in a new market now expect Arabic support. Which project function is this?', a=0,
                     opts=['Provide business direction and insight', 'Maintain governance', 'Facilitate and support', 'Provide oversight and coordination'])]),
    43: dict(
        hl=[('internal and external environments', 1), ('influence planning', 2), ('favorable, unfavorable, or neutral', 3)],
        notes=['Projects operate in **internal and external environments** that influence value delivery to different degrees.',
               'Those environments **influence planning** and other project activities.',
               'The influence can be **favorable, unfavorable or neutral**: a factor is not automatically a problem (a skilled team is a favorable internal factor).']),
    44: dict(
        hl=[('Internal Environment', 1), ('lessons learned', 2), ('Process assets', 3), ('Resource availability', 3), ('Employee capability', 3)],
        notes=['**Internal** factors come from inside the organization: the organization itself, a portfolio, a program or another project. Test: does the organization own or control it?',
               'They include artifacts, practices and **internal knowledge**, such as **lessons learned** and completed artifacts from earlier projects.',
               'Examples: process assets (templates, methods), governance documentation, data and knowledge assets, security and safety, infrastructure, IT software, **resource availability** and **employee capability**. Staff shortages and skill gaps are internal, a common trap.'],
        exam=[likely('Half of the developers have never used the cloud platform the project depends on. Is this an internal or external factor, and which example does it match?',
                     a='Internal: it is employee capability (and resource availability), which the organization owns and controls.')]),
    45: dict(
        hl=[('External Environment', 1), ('enhance, constrain, or have a neutral', 1), ('Marketplace conditions', 2), ('Regulatory environment', 2), ('Academic research', 3), ('Industry standards', 3)],
        notes=['**External** factors come from outside the organization and can **enhance, constrain or have a neutral** influence on outcomes.',
               'Examples: **marketplace conditions**, social and cultural influences, the **regulatory environment** (a new data-privacy law), financial considerations and the physical environment.',
               'Also **commercial databases, academic research and industry standards**: the team uses them, but they come from outside, so they are external.'],
        exam=[likely('A new national data-privacy law forces the team to redesign its storage layer. This is which kind of factor?', a=0,
                     opts=['External: regulatory environment', 'Internal: governance documentation', 'Internal: process assets', 'External: academic research'])]),
    46: dict(
        hl=[('more interlinked', 1), ('beyond the', 2), ('artifact that is produced', 3)],
        notes=['Portfolio, program, project and product management are becoming **more interlinked**.',
               'Portfolio, program and product management are **beyond the scope** of the standard and this course; what matters is how they relate to projects whose deliverables are products.',
               'A **product** is an artifact that is produced, is quantifiable, and is either an end item or a component (the same definition as slide 24).']),
    47: dict(
        hl=[('integration of people, data,', 1), ('throughout its life cycle', 1), ('introduction through growth, maturity', 2)],
        notes=['**Product management** integrates **people, data, processes and business systems** to create, maintain and develop a product or service **throughout its life cycle**. Contrast with project management, which delivers a temporary, unique piece of work and then ends.',
               'The **product life cycle**: introduction → growth → maturity → retirement.'],
        exam=[asked('m261', 'Short answer', 'Explain the difference between project management and product management. (Careful: product, not project.)',
                    a='**Project management** is the application of knowledge, skills, tools and techniques to project activities to meet project requirements; a project is temporary, with a start and an end, and creates a unique result. **Product management** integrates people, data, processes and business systems to create, maintain and develop a product throughout its whole life cycle (introduction, growth, maturity, retirement). Product management lasts as long as the product does and can start projects or programs at any point in that life cycle to create or improve the product.',
                    why='The instructor’s own question; she uses near-identical terms on purpose, so read “product” carefully.')]),
    48: dict(
        hl=[('at any point', 1), ('initial product', 2), ('add or improve', 3), ('full life cycle', 4)],
        notes=['Product management may **initiate programs or projects at any point** in the life cycle to create or enhance components, functions or capabilities.',
               'The **initial product** may itself be the deliverable of a program or project.',
               'Over the life cycle, new programs or projects **add or improve** components and capabilities, creating more value.',
               'Sometimes a single program covers the **full life cycle** of a product to manage its benefits directly.']),
    49: dict(
        hl=[('Portfolio Governance', 1, 0, 'ocr'), ('Project 1', 2, 0, 'ocr'), ('Project 7', 3, 0, 'ocr')],
        notes=['Reading the diagram: everything sits under **portfolio governance**, with **Program A** and **Program B** grouping the projects. The curve is the product’s usage, sales or impact over time.',
               '**Project 1** creates the product (introduction); **Projects 2–3** add features (growth); **Projects 4–6** revise it (maturity).',
               '**Project 7** retires it (decline/retirement). One product, many projects over its life, which is exactly the difference between product and project management.']),
    50: dict(
        hl=[('Program management within a product life cycle', 1), ('very large or long-running products', 2)],
        notes=['Form 1 of product management: **program management within a product life cycle**, which brings related projects, subsidiary programs and program activities together.',
               'Used for **very large or long-running products**, where one life-cycle phase is complex enough to need a set of programs and projects (e.g. modernizing the whole product years after launch).']),
    51: dict(
        hl=[('Project management within a product life cycle', 1), ('ongoing business activity', 2), ('charters individual projects', 3)],
        notes=['Form 2: **project management within a product life cycle**.',
               'The product’s development and maturing is run as an **ongoing business activity**.',
               'Portfolio governance **charters individual projects** as needed for enhancements or other unique outcomes (e.g. modernizing the UI years after launch).']),
    52: dict(
        hl=[('Product management within a program', 1), ('full product life cycle within the purview', 2), ('POC', 3)],
        notes=['Form 3: **product management within a program**.',
               'The **whole product life cycle** happens inside the boundaries of one program.',
               'Example: building a **proof of concept (POC)** to show possible directions for the program, then ending it. Size order of the three forms: a program within a big product’s life cycle → individual projects within the life cycle → a small product living inside a program.'],
        exam=[likely('After five years, a company charters a single project to modernize its app’s user interface. Which form of product management is this?', a=0,
                     opts=['Project management within a product life cycle', 'Program management within a product life cycle', 'Product management within a program', 'Portfolio management'])]),
    53: dict(notes=['Section divider: the 12 principles in detail.']),
    54: dict(
        hl=[('foundational guidelines', 1), ('prescriptive', 2), ('not prescriptive', 2), ('guide the behavior', 3), ('do not necessarily, reflect morals', 4)],
        notes=['A profession’s principles are **foundational guidelines** for strategy, decision-making and problem-solving; standards and methods are built on them.',
               'In some professions principles are laws or rules (**prescriptive**). Project management principles are **not prescriptive**: they don’t say exactly what to do.',
               'They **guide the behavior** of people on projects, and they are broad, so there are many ways to stay aligned with them.',
               'Principles **can, but do not necessarily**, reflect morals. A T/F trap will say “always reflect morals”.'],
        exam=[likely('True or false: the principles of project management are prescriptive rules that must be followed exactly.', tf=False,
                     why='They are not prescriptive; they guide behavior and can be applied in many ways.')]),
    55: dict(
        hl=[('code of ethics is related to morals', 1), ('Responsibility', 2), ('Respect', 2), ('Fairness', 2), ('Honesty', 2)],
        notes=['A **code of ethics**, unlike the principles, is related to morals: it sets expectations for moral conduct in a profession.',
               'The PMI Code of Ethics and Professional Conduct rests on four values: **responsibility, respect, fairness, honesty**. “Integrity” is not one of the four (it belongs to stewardship), which makes it the classic distractor.'],
        exam=[likely('Which of the following is NOT one of the four values of the PMI Code of Ethics and Professional Conduct?', a=0,
                     opts=['Integrity', 'Responsibility', 'Fairness', 'Honesty'])]),
    56: dict(
        hl=[('degree of', 1), ('application', 1), ('internally consistent', 2), ('practical dilemmas', 3), ('overlap with general', 4)],
        notes=['Because principles guide rather than prescribe, the **degree of application** and how they are applied depend on the context: organization, project, deliverables, team and stakeholders.',
               'The principles are **internally consistent**: no principle contradicts another.',
               'But **practical dilemmas** can still arise. Example: sharing information helps systems thinking, but confidentiality may require keeping it private.',
               'Project management principles also **overlap with general management**: both focus on delivering value (next slide).']),
    57: dict(
        hl=[('Project', 1, 1, 'ocr'), ('General', 2, 1, 'ocr')],
        notes=['The Venn diagram: project management principles and **general management** principles overlap. Both focus on delivering value, leading people and making decisions.',
               'Where they differ is the subject of a Final question: project management runs temporary, unique work with a fixed scope and a borrowed, cross-functional team; general management runs ongoing operations with permanent staff and line authority.'],
        exam=[asked('f251', 'Q1.2', 'What are the key distinctions between project management and general management, particularly concerning their respective focuses, skill sets, and approaches to managing teams and resources?',
                    a='**Focus**: project management delivers temporary, unique work with a defined start, end and scope; general management runs the ongoing, repetitive operations of a function. **Skills**: a PM needs planning, scheduling, risk, stakeholder and integration skills across functions; a general manager needs depth in one function and long-term operational skills. **Teams and resources**: a PM leads a temporary, cross-functional team, often borrowed from functional managers, so works by influence and negotiation within a fixed budget and schedule; a general manager has permanent staff, line authority and an ongoing budget.')]),
    58: dict(
        hl=[('steward', 1), ('collaborative project', 2), ('engage with', 3), ('Focus on value', 4), ('system interactions', 5), ('Demonstrate leadership', 6), ('Tailor based on context', 7), ('Navigate complexity', 8), ('Optimize risk responses', 9), ('envisioned future state', 10)],
        notes=['The 12 principles as full PMI statements; exams may use either the short name (slide 21) or this wording. **Stewardship** = be a diligent, respectful and caring steward.',
               '**Team** = create a collaborative project team environment.',
               '**Stakeholders** = effectively engage with stakeholders.',
               '**Value** = focus on value.',
               '**Systems thinking** = recognize, evaluate and respond to system interactions.',
               '**Leadership** = demonstrate leadership behaviors.',
               '**Tailoring** = tailor based on context. (**Quality** = build quality into processes and deliverables.)',
               '**Complexity** = navigate complexity.',
               '**Risk** = optimize risk responses. (**Adaptability and resiliency** = embrace adaptability and resiliency.)',
               '**Change** = enable change to achieve the envisioned future state.']),
    59: dict(
        hl=[('STEWARDSHIP', 1, 0, 'ocr'), ('Integrity', 2, 0, 'ocr'), ('holistic view of stewardship', 3, 0, 'ocr')],
        notes=['**Stewardship**: stewards act responsibly, carrying out activities with integrity, care and trustworthiness while complying with internal and external guidelines. It covers responsibilities **inside and outside** the organization, and it is personal: it can’t be handed to auditors or the sponsor.',
               'Stewardship includes four things: **integrity, care, trustworthiness and compliance**.',
               'A holistic view considers **financial, social, technical and environmental** impacts, not just delivering outputs.']),
    60: dict(
        hl=[('Project teams are made', 1, 0, 'ocr'), ('own “local”', 2, 0, 'ocr'), ('collaborative project team environment', 3, 1, 'ocr')],
        notes=['**Team**: projects are delivered by teams of people with diverse skills, and a collaborative team reaches a shared objective more effectively than individuals working alone.',
               'Teams work within organizational and professional cultures, but often build their own **“local” culture** (their norms and ways of working). Chapter 3 covers how.',
               'A collaborative environment supports alignment with other cultures, individual and team learning, and the best contribution from each person.'],
        exam=[asked('f242', 'Q5.2', 'How does fostering trust and managing conflict within a software project team contribute to improved collaboration and project success?',
                    a='Trust lets members admit mistakes, share information and ask for help, so problems surface early and people cooperate instead of protecting themselves. Managed (healthy) conflict means ideas are debated openly and respectfully, which gives better technical decisions and avoids groupthink or disputes that turn personal. Together they lead to real commitment and collaboration, which drives quality and project success.',
                    why='Chapter 3 covers trust and conflict in depth; the principle introduces them.')]),
    61: dict(
        hl=[('Engage stakeholders', 1, 0, 'ocr'), ('proactively and to the', 2, 0, 'ocr'), ('advances value delivery', 3, 0, 'ocr')],
        notes=['**Stakeholders**: engage them **proactively and to the degree needed**: don’t wait for complaints, and don’t engage everyone equally. This leads to the power/interest grid in Chapter 8.',
               'Stakeholders influence projects, performance and outcomes, and teams serve stakeholders by engaging with them.',
               'Proactive engagement **advances value delivery**, because stakeholders define what value means.']),
    62: dict(
        hl=[('Continually evaluate and', 1, 0, 'ocr'), ('ultimate indicator of project success', 2, 0, 'ocr'), ('throughout the project', 3, 0, 'ocr')],
        notes=['**Value**: continually evaluate and adjust the project’s alignment with business objectives and intended benefits.',
               'Value is the **ultimate indicator of project success**, more than being on time or on budget.',
               'Value can be realized **throughout** the project, at its end, or after it; and it can be defined in quantitative or qualitative terms. Focusing on outcomes helps teams support the intended benefits.']),
    63: dict(
        hl=[('SYSTEMS THINKING', 1, 0, 'ocr'), ('interdependent', 2, 0, 'ocr'), ('holistic view', 2, 0, 'ocr')],
        notes=['**Systems thinking**: recognize, evaluate and respond to the dynamic circumstances within and around the project holistically.',
               'A project is a **system of interdependent, interacting parts**; systems thinking takes a holistic view of how they interact with each other and with external systems. Systems keep changing, so attention must be continuous, and responding to interactions lets the team turn them to its advantage.'],
        exam=[asked('m261', 'MCQ', 'A team discovers that changing the database will affect the payment system and the registration system. Which principle is most directly demonstrated?',
                    a=0, opts=['Recognize, Evaluate, and Respond to System Interactions', 'Build Quality into Processes and Deliverables', 'Demonstrate Leadership Behaviors', 'Focus on Value'],
                    why='A project is a system of interdependent parts; seeing how one change ripples into others is systems thinking.')]),
    64: dict(
        hl=[('Demonstrate and adapt', 1, 0, 'ocr'), ('Any project team member', 2, 0, 'ocr'), ('different than authority', 2, 0, 'ocr'), ('adapt their style', 3, 0, 'ocr')],
        notes=['**Leadership**: demonstrate and adapt leadership behaviors to support individual and team needs. Effective leadership contributes to project success.',
               '**Any team member** can show leadership, not only the PM, and leadership is **different from authority**: a junior developer who organizes a fix is leading without any formal power.',
               'Effective leaders **adapt their style** to the situation, recognize that people are motivated differently, and model honesty, integrity and ethical conduct. Chapter 3’s technical vs. adaptive leadership builds on this.']),
    65: dict(
        hl=[('TAILORING', 1, 0, 'ocr'), ('“just enough” process', 2, 0, 'ocr'), ('iterative', 3, 0, 'ocr')],
        notes=['**Tailoring**: design the development approach based on the context: the project’s objectives, stakeholders, governance and environment.',
               'Use a **“just enough”** process: enough to achieve the outcome while maximizing value, managing cost and enhancing speed, but no heavier.',
               'Every project is unique, so success depends on adapting the methods to it. Tailoring is **iterative and continuous** throughout the project, not a one-time decision at the start.'],
        exam=[likely('True or false: tailoring is a one-time activity performed when the project is initiated.', tf=False,
                     why='Tailoring is iterative and continuous throughout the project.')]),
    66: dict(
        hl=[('Maintain a focus on', 1, 0, 'ocr'), ('acceptance criteria', 2, 0, 'ocr'), ('processes are appropri', 3, 0, 'ocr')],
        notes=['**Quality**: keep a focus on quality that produces deliverables meeting the objectives and the needs, uses and acceptance requirements of stakeholders.',
               'Quality means satisfying stakeholders’ expectations and fulfilling project and product requirements, measured against the **acceptance criteria** for deliverables.',
               'It applies to the **processes** too: they must be appropriate and as effective as possible. Chapter 7 develops this as quality assurance (process) vs. quality control (product).']),
    67: dict(
        hl=[('Continually evaluate', 1, 0, 'ocr'), ('human behavior, system interactions', 2, 0, 'ocr'), ('emerge at any point', 3, 0, 'ocr')],
        notes=['**Complexity**: continually evaluate and navigate complexity so the approach and plans let the team succeed.',
               'Complexity comes from **human behavior, system interactions, uncertainty and ambiguity**.',
               'It can emerge **at any point** and can be introduced by events affecting value, scope, communications, stakeholders, risk or technology; teams stay vigilant and use methods to reduce its amount or impact.']),
    68: dict(
        hl=[('exposure to risk', 1, 0, 'ocr'), ('positive (opportunities)', 2, 0, 'ocr'), ('Appropriate for the significance', 3, 0, 'ocr')],
        notes=['**Risk**: continually evaluate exposure to risk, both **opportunities and threats**, to maximize positive impacts and minimize negative ones. Individual and overall risks both matter, and the organization’s risk attitude and threshold shape the response.',
               'Risks can be **positive (opportunities) or negative (threats)** and are addressed throughout the project, not once.',
               'Good responses are **appropriate** to the risk’s significance, **cost-effective**, **realistic** in context, **agreed** by the relevant stakeholders, and **owned** by a responsible person. Chapter 5 covers the strategies.'],
        exam=[asked('f242', 'Q2.5', 'As the project manager for the smart solar panel system, you’re expected to manage risks proactively throughout the 12-month development cycle. Describe two techniques you would use during the planning phase to identify and document project risks. Explain how a Risk Assessment Matrix helps in making informed decisions about which risks need immediate action.',
                    a='Brainstorming with engineers, hardware specialists and developers, and expert interviews / Delphi with people who have done regulatory approvals, both recorded in a risk register (risk, cause, owner, response). A checklist from past projects also works. The Risk Assessment Matrix plots each risk’s probability against its impact; the score ranks the risks, so high-probability, high-impact (red) risks get immediate responses and owners, medium ones are planned for, and low ones are just monitored.',
                    why='Detailed in Chapter 5; the principle sets the expectation.')]),
    69: dict(
        hl=[('Build adaptability and', 1, 0, 'ocr'), ('respond to changing conditions', 2, 0, 'ocr'), ('recover', 3, 0, 'ocr')],
        notes=['**Adaptability and resiliency**: build them into the organization’s and team’s approaches so the project can accommodate change, recover from setbacks and keep advancing.',
               '**Adaptability** is the ability to respond to **changing conditions** (bend with change).',
               '**Resiliency** is the ability to absorb impacts and **recover** quickly from a setback or failure (bounce back). A focus on outcomes rather than outputs makes adapting easier.'],
        exam=[likely('A critical server failure takes the test environment down, and the team restores it from backups and resumes work within a day. Which quality does this show?', a=0,
                     opts=['Resiliency', 'Adaptability', 'Tailoring', 'Stewardship'])]),
    70: dict(
        hl=[('Prepare those impacted', 1, 0, 'ocr'), ('structured approach to change', 2, 0, 'ocr'), ('change fatigue', 3, 0, 'ocr')],
        notes=['**Change**: prepare the people affected to adopt the new behaviors and processes needed to move from the current state to the future state the project creates.',
               'A **structured approach** helps individuals and groups make the transition; change can come from internal or external sources, and not every stakeholder embraces it.',
               'Too much change in a short time causes **change fatigue** and resistance; stakeholder engagement and motivation help adoption.'],
        exam=[likely('A ministry rolls out a new ERP, a new HR system and a new workflow in the same month. Staff start ignoring announcements and avoiding the new tools. What is happening, and what does the Change principle recommend?',
                     a='Change fatigue and resistance from attempting too much change in a short time. The principle recommends a structured approach to change: pace the changes, engage the affected stakeholders early, and use motivational approaches so people adopt the new behaviors.')]),
}

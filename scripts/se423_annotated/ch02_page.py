"""SE423 Chapter 2 (The Organizational Context: Strategy, Structure, and Culture): page content.

Schema: see annotated_page.py. Figures are pictures, so their marks use 'ocr' (skipped if OCR can't read them).
Past-exam questions are copied from the papers in exams/ and the instructor's 2026 midterm (m261); everything
else is a prediction.
"""
from .common import asked, likely

TITLE = 'The Organizational Context: Strategy, Structure, and Culture'
CHAPTER = 'SE423 · Chapter 2'

OVERVIEW = {
    'summary': ('Projects don’t happen in a vacuum: three features of the parent organization shape how they are run. '
                'Strategy: strategic management formulates, implements and evaluates decisions, and projects are how '
                'strategy gets implemented; stakeholders inside and outside the organization pull projects in different '
                'directions. Structure: functional, project and matrix organizations (and heavyweight project teams), each '
                'with strengths and weaknesses for projects, plus the PMO’s levels, forms and models. Culture: the unwritten '
                'rules of behavior, what shapes them, and the four ways they affect project management.'),
    'ideas': [
        ('Projects implement strategy', 'Strategic management = formulate, implement and evaluate cross-functional decisions; projects (new plants, products, IT) carry the strategy out.'),
        ('Three structures', 'Functional = grouped by similar activities (deep expertise, silos). Project = temporary project teams (fast, expensive). Matrix = dual hierarchy (coordination, two bosses).'),
        ('PMO', 'Levels 1–3 (project → business unit → corporate); forms by control (supportive, controlling, directive); models by purpose (weather station, control tower, resource pool).'),
        ('Culture', 'Unwritten rules of behavior, shared by a subset, taught to newcomers; affects departmental interaction, commitment, planning and performance evaluation.'),
    ],
    'sections': [
        ('Slides 1–5', 'Strategy: strategic management, projects reflect strategy, the A380'),
        ('Slides 6–8', 'Stakeholder management: internal and external stakeholders'),
        ('Slides 9–18', 'Structure: functional, project, matrix and heavyweight organizations'),
        ('Slides 19–22', 'Project management offices: levels, forms, models'),
        ('Slides 23–25', 'Organizational culture and its effects on projects'),
    ],
    'exam': ('The instructor’s 2026 midterm asked three questions from this deck: how employees are grouped in a functional '
             'organization, what describes a project organization, and the main purpose of strategic management. Finals asked '
             'about the PMO (Final 242) and how PM helps achieve strategic objectives (Final 251); the Midterm 251 case asked '
             'which team structure you would set up.'),
}

TITLES = {4: 'Strategy example: the Airbus A380', 8: 'Figure 2.3 Project Stakeholder Relationships', 11: 'Figure 2.4 A Functional Organizational Structure',
          18: 'Figure 2.8 Perceived Effectiveness of Structures'}

SLIDES = {
    1: dict(
        hl=[('The Organizational Context: Strategy, Structure, and Culture', 1)],
        notes=['This chapter (from Pinto’s *Project Management*) looks at the three organizational features that shape how projects are run: **strategy** (why projects exist), **structure** (who reports to whom and how resources are shared) and **culture** (the unwritten rules people follow).']),
    2: dict(
        hl=[('Strategic management', 1), ('formulating,', 1), ('implementing, and evaluating cross-functional decisions', 1), ('vision and mission statements', 2), ('Achieving objectives', 3)],
        notes=['**Strategic management** is the science of **formulating, implementing and evaluating cross-functional decisions** that enable an organization to achieve its objectives. Cross-functional matters: strategy cuts across departments, and so do the projects that carry it out.',
               'It starts by developing **vision and mission statements**, then formulates, implements and evaluates strategies, making cross-functional decisions along the way…',
               '…all aimed at **achieving the organization’s objectives**.'],
        exam=[asked('m261', 'MCQ', 'What is the main purpose of strategic management?',
                    a=0, opts=['To formulate, implement, and evaluate decisions that help achieve organizational objectives', 'To manage employees’ daily activities only',
                               'To eliminate all organizational risks', 'To focus only on project costs'],
                    why='The slide’s definition: formulating, implementing and evaluating cross-functional decisions to achieve objectives.')]),
    3: dict(
        hl=[('Projects Reflect Strategy', 1), ('New product development projects', 2), ('Reengineering projects', 2), ('Reverse engineering projects', 3), ('Enterprise IT efforts', 3)],
        notes=['The table’s point: **projects are how strategy gets implemented**. Each strategic intention on the left becomes a type of project on the right.',
               'A strategy of greater market penetration becomes **new product development** projects; a strategy of more efficient business processes becomes **reengineering** projects; operating initiatives become new or modernized plants.',
               'Matching competitors’ products becomes **reverse engineering**; better cross-organization communication in the supply chain becomes **enterprise IT** efforts; better departmental coordination becomes concurrent engineering. Pick one or two rows as examples when explaining how PM supports strategy.'],
        exam=[asked('f251', 'Q1.1', 'How does project management contribute to organizations in achieving their strategic objectives? Please elaborate.',
                    a='Strategy is carried out through projects. Project management selects and prioritizes projects (through portfolios and programs) so they align with strategic objectives, then delivers them so the outputs create the intended outcomes, benefits and value. It uses limited resources efficiently, controls scope, time and cost, and manages risk and change. That lets the organization reach its goals and respond to its market faster than competitors.')]),
    4: dict(
        hl=[('What went wrong for the A380?', 1), ('strategic decisions', 1), ('much bigger planes', 2), ('medium-sized wide-body jets', 3)],
        notes=['The **Airbus A380** case: what went wrong was mainly **strategic**, not execution.',
               'Airbus and Boeing saw the same facts (air traffic doubling every 15 years). Airbus concluded the future needed **much bigger planes** to serve congested hub airports, and built the A380.',
               'Boeing concluded that **medium-sized wide-body jets** flying directly between more cities fitted the future better, and the market followed Boeing. Lesson: a project can be well run and still fail if the strategy behind it is wrong.']),
    5: dict(
        hl=[('Developing vision statements and mission statements', 1), ('Formulating, implementing, and evaluating', 2), ('key ingredients in', 2), ('Making cross-functional decisions', 3), ('TOWS Matrix', 4)],
        notes=['**Vision and mission statements** state what the organization hopes to accomplish or become.',
               '**Formulating, implementing and evaluating**: projects are the **key ingredients in strategy implementation**. The firm evaluates opportunities by setting its vision, assessing internal strengths and weaknesses and external opportunities and threats, setting long-range objectives, and choosing among alternatives.',
               '**Cross-functional decisions** and **achieving objectives** complete the process.',
               'The **TOWS matrix** turns SWOT into strategies: SO (use strengths to seize opportunities), ST (use strengths against threats), WO (overcome weaknesses using opportunities), WT (minimize weaknesses and avoid threats).'],
        exam=[likely('In a TOWS matrix, a strategy that uses internal strengths to take advantage of external opportunities is called:', a=0,
                     opts=['SO', 'WT', 'ST', 'WO'])]),
    6: dict(
        hl=[('external effects of their decisions', 1), ('stakeholder analysis', 2), ('irresolvable conflicts', 3), ('active stake', 4)],
        notes=['Organizations and project teams can’t ignore the **external effects** of their decisions.',
               '**Stakeholder analysis** shows how the PM and the project relate to the rest of the organization…',
               '…and exposes the seemingly **irresolvable conflicts** that new projects create (a new system that helps sales may burden operations).',
               '**Project stakeholders**: all individuals or groups with an **active stake** in the project who can affect its development positively or negatively.']),
    7: dict(
        hl=[('Internal Stakeholders', 1), ('External Stakeholders', 2), ('intervenor groups', 3)],
        notes=['**Internal stakeholders**: top management, the accountant, other functional managers, project team members.',
               '**External stakeholders**: clients, **competitors**, suppliers, and environmental, political, consumer and other intervenor groups.',
               '**Intervenor groups** are external groups with the power to intervene and disrupt a project. Environmental groups used lawsuits and lobbying to halt the Dakota Access Pipeline and delay the Keystone XL pipeline for years.'],
        exam=[asked('m251v1', 'Case Q3', 'Edugate scheduling system: identify three main stakeholder groups for this project, describe their roles, and explain how their input will shape the system.',
                    a='Students are the end users; their input shapes usability and flexibility (0.3). The IT/Edugate team ensures integration, security and compliance with PSU IT policies (0.3). Faculty advisors and administration ensure study-plan rules are enforced and use the system to monitor students (0.4).')]),
    8: dict(
        hl=[('on loan from', 1, 0, 'ocr'), ('as quickly as', 2, 0, 'ocr'), ('top management control', 3, 0, 'ocr'), ('monitor project budgets', 4, 0, 'ocr')],
        notes=['What each stakeholder wants. **Functional managers**: most project staff are **on loan** from their departments, so functional managers want their people back and their own work protected.',
               '**Clients**: receive the project **as quickly as possible** so their investment starts generating returns.',
               '**Top management**: support the project but **control** project managers and regulate their freedom of action.',
               '**Accountants**: support and actively **monitor project budgets**. The PM sits in the middle, balancing all of them.']),
    9: dict(
        hl=[('formal reporting relationships', 1), ('span of control', 1), ('groupings of', 2), ('effective communication', 3), ('integration of effort', 3)],
        notes=['**Organizational structure** has three elements. (1) **Formal reporting relationships**: who reports to whom, how many levels the hierarchy has, and each manager’s **span of control** (how many people report to them).',
               '(2) **Groupings**: individuals into departments and departments into the organization.',
               '(3) **Systems** that ensure effective communication, coordination and **integration of effort** across departments. Projects cut across departments, so this third element is where they succeed or struggle.']),
    10: dict(
        hl=[('Functional organizations', 1), ('similar activities', 1), ('Project organizations', 2), ('temporary assignments', 2), ('Matrix organizations', 3), ('dual hierarchy', 3)],
        notes=['**Functional** organizations group people who perform **similar activities** into departments (marketing, finance, engineering).',
               '**Project** organizations group people into **project teams on temporary assignments**.',
               '**Matrix** organizations create a **dual hierarchy** in which functions and projects have equal prominence: staff report to both a functional manager and a project manager.'],
        exam=[asked('m261', 'MCQ', 'How are employees grouped in a functional organization?',
                    a=0, opts=['According to similar activities or functions', 'According to temporary project assignments only', 'According to their personal interests', 'Randomly across the organization']),
              asked('m261', 'MCQ', 'Which statement best describes a project organization?',
                    a=0, opts=['People are grouped into project teams for temporary assignments', 'Employees remain permanently grouped only by function',
                               'All projects are managed by external suppliers', 'Project managers have no authority over project teams'])]),
    11: dict(
        hl=[('President', 1, 0, 'ocr'), ('Finance', 2, 0, 'ocr')],
        notes=['A **functional** structure: departments (engineering, manufacturing, marketing, finance, accounting) under the president, each with its own sub-units.',
               'The vertical arrows show **communication channels running up and down inside each function**, not across. Coordinating a cross-functional project means going up one chain and down another, which is slow: the root of the silo weakness on the next slide.']),
    12: dict(
        hl=[('no disruption or change', 1), ('in-depth knowledge', 2), ('standard career paths', 3), ('Functional siloing', 4), ('Lack of customer focus', 5), ('Longer time to complete projects', 6)],
        notes=['**Strengths for projects**. Projects run inside the existing structure, so there is **no disruption** to the firm’s design.',
               'It develops **in-depth knowledge** and intellectual capital within each function.',
               'It allows **standard career paths**: people grow within their specialty.',
               '**Weaknesses**. **Functional siloing**: unwillingness to consider other viewpoints or collaborate makes cross-functional cooperation hard.',
               '**Lack of customer focus**: each function serves its boss, not the customer.',
               '**Longer project times** (slower communication through the hierarchy) and varying interest or commitment, since the project is nobody’s main job.'],
        exam=[likely('Which is a weakness of functional structures for project management?', a=0,
                     opts=['Functional siloing and lack of customer focus', 'In-depth knowledge development', 'Standard career paths', 'No disruption to the firm’s design'])]),
    13: dict(
        hl=[('self-', 1), ('contained business unit', 1), ('dedicated project team', 1), ('for the time period they are needed', 2), ('Construction companies', 3)],
        notes=['In a **project organization** each project is a **self-contained business unit** with a **dedicated team**.',
               'The firm assigns resources from functional pools directly to the project **for as long as they are needed**.',
               'Firms whose business is projects organize this way: **construction companies**, Boeing and Airbus, pharmaceutical firms, and many software consulting and R&D organizations.']),
    14: dict(
        hl=[('Project manager sole', 1), ('Improved communication', 2), ('Rapid response to market', 3), ('Expensive to set up', 4), ('loyalty to the project', 5), ('concern about future', 6)],
        notes=['**Strengths**: the **PM has sole authority** over the project.',
               '**Improved communication** and **effective decision-making** inside a dedicated team, and the firm develops project-management experts.',
               '**Rapid response to market opportunities**.',
               '**Weaknesses**: **expensive** to set up and maintain dedicated teams.',
               'Members may become **loyal to the project rather than the firm**, and pooled expertise is hard to keep (contractors leave when the project ends).',
               'Members **worry about their future** once the project ends.'],
        exam=[likely('Which is a strength of the project organizational structure?', a=0,
                     opts=['The project manager has sole authority', 'It is cheap to set up', 'Pooled expertise is easy to keep', 'Team members never worry about the future'])]),
    15: dict(
        hl=[('vice president of projects', 1), ('loans of personnel', 2), ('Resources', 2, 0, 'ocr')],
        notes=['A **matrix** structure. The **vice president of projects** controls the project managers (rows)…',
               '…but the PMs must work closely with the functional departments (columns) to staff their teams through **loans of personnel** from each function: the “2 resources”, “1.5 resources” cells show how many people each department lends to each project.']),
    16: dict(
        hl=[('Suited to dynamic environments', 1), ('Equal emphasis', 2), ('Promotes coordination', 3), ('Maximizes scarce resources', 4), ('two bosses', 5), ('Negotiation required', 6)],
        notes=['**Strengths**: suited to **dynamic environments** (resources shift as projects change).',
               '**Equal emphasis** on project management and functional efficiency.',
               'It **promotes coordination** across functional units.',
               'It **maximizes scarce resources**: a specialist can be shared across several projects.',
               '**Weaknesses**: the dual hierarchy means **two bosses**, and workers get caught between competing project and functional demands.',
               '**Negotiation** is needed to share resources between project and functional managers. “Two bosses” is never a strength.'],
        exam=[likely('What is the main weakness of the matrix structure?', a=0,
                     opts=['The dual hierarchy gives workers two bosses', 'There is no coordination across units', 'It wastes scarce resources', 'It is unsuitable for dynamic environments'])]),
    17: dict(
        hl=[('fully dedicated project organization', 1), ('Skunk works', 2), ('Project manager authority expanded', 3), ('market', 4), ('external customer', 5)],
        notes=['Organizations sometimes benefit from a **fully dedicated** project organization: a **heavyweight** project team.',
               'Lockheed’s **Skunk Works** model: a small, autonomous team of hand-picked, highly skilled people with complete freedom, and a PM with full authority, status and responsibility.',
               'In heavyweight organizations **PM authority is expanded**…',
               '…functional alignment is abandoned in favour of **market** opportunism, with direct reporting to the top executives…',
               '…and the focus is on the **external customer**.']),
    18: dict(
        hl=[('Functional', 1, 0, 'ocr'), ('Project team', 2, 0, 'ocr')],
        notes=['A survey of managers’ perceptions of how effective each structure is for project success, from **functional** through functional matrix, balanced matrix and project matrix to **project team**.',
               'The trend: the more project-oriented the structure, the more effective managers judge it for projects; for new product development the project matrix and project team score highest. (A survey result to understand, not to memorize.)']),
    19: dict(
        hl=[('Centralized units', 1), ('Technical details', 2), ('Repository', 2), ('Center for excellence', 2), ('shifts some of the burden', 3)],
        notes=['**Project management offices (PMOs)** are centralized units that oversee or improve the management of projects.',
               'They act as resource centres for **technical details**, **expertise**, a **repository** (templates, lessons learned, past project data) and a **center of excellence** for PM practice.',
               'A PMO **shifts some of the burden** of PM work (activity scheduling, resource allocation, monitoring and control) from the project manager to dedicated support staff.'],
        exam=[asked('f242', 'Q1.3', 'What is a Project Management Office (PMO) and its role in organizations?',
                    a='A PMO is a centralized organizational unit that oversees and standardizes how projects are managed. It sets PM standards, methods and templates, trains and supports project managers, monitors and reports on project performance, and coordinates resources across projects. Its control ranges from supportive (consultative) to controlling (requires compliance) to directive (manages the projects directly).')]),
    20: dict(
        hl=[('corporate level (Level', 1), ('functional level', 2), ('(Level 2)', 2), ('project level (Level 1)', 3)],
        notes=['A PMO can sit at three levels. **Level 3, corporate**: serves an overall corporate support function.',
               '**Level 2, business unit**: serves the needs within one business unit or function.',
               '**Level 1, project**: decentralized to the individual project, giving direct support. The numbering runs upward: Level 1 is the narrowest scope, Level 3 the widest.'],
        exam=[likely('A PMO that serves the needs within one specific business unit is at which level?', a=0,
                     opts=['Level 2', 'Level 1', 'Level 3', 'Level 0'])]),
    21: dict(
        hl=[('Supportive', 1), ('low control', 1), ('Controlling', 2), ('requires compliance', 2), ('Directive', 3), ('directly manages projects', 3)],
        notes=['Three **forms** of PMO, by how much control they exert. **Supportive** (low control): consultative; provides templates, best practices, training and access to information.',
               '**Controlling** (moderate control): requires **compliance** with adopted PM standards, templates and processes, e.g. through audits.',
               '**Directive** (high control): **directly manages** the projects; the PMs belong to it.'],
        exam=[likely('A PMO that requires projects to comply with its adopted standards and templates, but does not run the projects itself, is which form?', a=0,
                     opts=['Controlling', 'Supportive', 'Directive', 'Resource pool'])]),
    22: dict(
        hl=[('Weather station', 1), ('monitoring and tracking device', 1), ('Control tower', 2), ('skill to be protected', 2), ('Resource pool', 3), ('cadre of skilled project', 3)],
        notes=['Three **models** of PMO, by purpose (not to be confused with the forms, which are about how much control). **Weather station**: only **monitors and tracks** project status, without trying to influence or control projects.',
               '**Control tower**: treats PM as a **skill to be protected and supported**; it improves methodology and practices and helps PMs apply them.',
               '**Resource pool**: maintains and supplies a **cadre of skilled** project managers and professionals to the company’s projects.'],
        exam=[likely('A consultancy keeps a bench of certified project managers and assigns them to client projects as needed. Which PMO model is this?', a=0,
                     opts=['Resource pool', 'Weather station', 'Control tower', 'Directive'])]),
    23: dict(
        hl=[('organizational culture', 1, 1), ('unwritten rules of behavior', 2), ('Unwritten', 3), ('Held by some subset', 3), ('Taught to all new members', 3)],
        notes=['The third contextual variable is **organizational culture**.',
               '**Definition**: the **unwritten rules of behavior**, or norms, that shape and guide behavior, shared by some subset of organizational members and taught to all new members.',
               'The four parts: **unwritten** (rarely written down); **rules of behavior** (how to react to events); **held by a subset** (not necessarily company-wide: engineering can have a different culture from sales); **taught to new members** (newcomers pick it up by watching others). Example: a culture that rewards collaboration between functional groups.']),
    24: dict(
        hl=[('Technology', 1), ('Environment', 1), ('Reward systems', 2), ('Rolls-Royce', 2), ('Critical incidents', 3)],
        notes=['Factors that shape culture: **technology**, **environment** (the industry and market), geographical location…',
               '…**reward systems**, rules and procedures, and key organizational members. GE’s jet-engine division and Rolls-Royce make the same product for the same markets, yet GE rewards aggressiveness and high commitment (with high burnout) while Rolls-Royce is paternalistic and rewards loyalty and long tenure, largely because of what each rewards.',
               '**Critical incidents**: moments when the real culture becomes visible, e.g. how leadership reacts to a failed project.']),
    25: dict(
        hl=[('Departmental interaction', 1), ('Employee commitment to goals', 2), ('Project planning', 3), ('wider estimates', 3), ('Performance evaluation', 4)],
        notes=['Culture affects project management in four ways. **Departmental interaction**: cultures where functions actively cooperate with projects succeed far more than disinterested or adversarial ones.',
               '**Employee commitment to goals**: a culture of commitment (extra effort when needed) beats one where going through the motions is fine as long as you don’t get caught.',
               '**Project planning**: where lateness is punished, people pad their estimates to protect themselves; a **culture of trust** produces honest estimates.',
               '**Performance evaluation**: if the organization quietly rewards caution and playing it safe, its projects will be cautious too.'],
        exam=[likely('Your team pads every estimate by 50% because missing a date is punished. Which effect of culture is this, and how would you address it?',
                     a='Culture affecting project planning: a culture that punishes lateness reinforces inflated estimates. Build a culture of trust in which honest estimates are not punished, handle uncertainty openly with risk reserves, and estimates become realistic.')]),
}

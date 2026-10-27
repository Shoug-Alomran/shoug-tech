"""SE423 Chapter 1.3 (Tailoring, Models, Methods, and Artifacts): page content for the annotated deck.

Schema: see annotated_page.py. Diagrams and the reference tables are pictures, so their marks use 'ocr' (skipped
if OCR can't read them). Past-exam questions are copied from the papers in exams/; everything else is a prediction.
"""
from .common import asked, likely

TITLE = 'Tailoring, Models, Methods, and Artifacts'
CHAPTER = 'SE423 · Chapter 1.3'

OVERVIEW = {
    'summary': ('Two parts. Tailoring is the deliberate adaptation of the project-management approach, governance and '
                'processes to the environment and the work: what can be tailored (life cycle, processes, engagement, tools, '
                'methods and artifacts), why (commitment, customer focus, efficient resources), and the four-step process '
                '(select an initial approach, tailor for the organization, tailor for the project, keep improving). The second '
                'part is the PMBOK toolbox: models (ways of thinking, such as situational leadership, Herzberg, ADKAR, Cynefin, '
                'Tuckman), methods (ways of doing, such as estimating and meetings) and artifacts (things produced, such as the '
                'business case, registers and plans).'),
    'ideas': [
        ('Tailoring', 'Deliberate, continuous adaptation; more critical projects need more rigor. Steps: select → organization → project → improve.'),
        ('What you tailor', 'Life cycle and approach, processes (add, modify, remove, blend, align), engagement, tools, methods and artifacts.'),
        ('Model, method, artifact', 'Model = a way of thinking; method = a way of doing; artifact = a template, document or deliverable.'),
        ('Models to know', 'Situational Leadership II, Herzberg’s hygiene and motivators, Maslow, Theory X/Y/Z, ADKAR, Kotter’s 8 steps, Cynefin, Stacey, Tuckman, salience.'),
    ],
    'sections': [
        ('Slides 1–12', 'Tailoring: definition, competing demands, why and what to tailor'),
        ('Slides 13–22', 'The tailoring process: organization and project factors, ongoing improvement'),
        ('Slides 23–27', 'Models, methods and artifacts: definitions and costs'),
        ('Slides 28–34', 'Commonly used models'),
        ('Slides 35–41', 'Commonly used methods and artifacts'),
    ],
    'exam': ('The instructor said to understand these models rather than memorize them; expect scenarios such as “which model '
             'helps here?” or “is this a hygiene factor or a motivator?”. Tuckman (Midterm 251 MCQ 7) is tested in Chapter 3, '
             'and Final 251 asked for a PM tool or technique for a complex software project.'),
}

TITLES = {3: 'Tailoring (section)', 13: 'The Tailoring Process', 21: 'Situations and Tailoring Suggestions', 23: 'Models, Methods, and Artifacts (section)',
          26: 'Principles, domains and the toolbox together', 34: 'Models by performance domain', 36: 'Methods by performance domain',
          37: 'Methods by performance domain (cont.)', 39: 'Artifacts by performance domain', 40: 'Artifacts by performance domain (cont.)',
          41: 'Artifacts by performance domain (cont.)'}

TABLE = ('A reference table showing which performance domains each item is useful in (an X per domain). Don’t memorize it; use it to '
         'pick a suitable tool when a scenario asks which method or artifact would help.')

SLIDES = {
    1: dict(
        hl=[('Tailoring, Models, Methods,', 1), ('SE423: Software Project Management', 2)],
        notes=['**Tailoring** means fitting the project-management approach to the project. **Models, methods and artifacts** are the toolbox it picks from.',
               'This finishes Chapter 1: principles (how to behave) and performance domains (what to manage) are applied through a tailored selection of tools.']),
    2: dict(
        hl=[('Tailoring', 1), ('Models, Methods, and Artifacts', 2)],
        notes=['Part 1, slides 3–22: tailoring.', 'Part 2, slides 23–41: models, methods and artifacts.']),
    3: dict(notes=['Section divider: tailoring.']),
    4: dict(
        hl=[('deliberate adaptation', 1), ('development', 2), ('approach, processes, project life cycle', 2), ('criticality', 3), ('nuclear reactor', 4)],
        notes=['**Tailoring** is the **deliberate** adaptation of the project-management approach, governance and processes to suit the environment and the work at hand. Deliberate is the key word: it is a conscious design choice, not cutting corners.',
               'It covers the **development approach**, processes, project life cycle, deliverables and who to engage.',
               'Many variables drive it, including the project’s **criticality** and the number of stakeholders.',
               'Example: a **nuclear reactor** needs far more rigor, checks and balances and reporting than a new office building. More critical means more process, never less.'],
        exam=[likely('Which statement best defines tailoring?', a=0,
                     opts=['The deliberate adaptation of the project management approach, governance and processes to the environment and the work', 'Following one standard methodology on every project', 'Removing all documentation to save time', 'Choosing the cheapest vendor for each task'])]),
    5: dict(
        hl=[('project context, goals, and', 1), ('competing demands', 2), ('Delivering as quickly as possible', 2), ('compliance with regulatory standards', 2), ('Adapting to change', 2)],
        notes=['Tailoring starts with understanding the project’s **context, goals and operating environment**.',
               'Projects must balance **competing demands**: speed, low cost, value, quality, regulatory compliance, diverse stakeholder expectations, and adapting to change. No project can maximize all seven at once (the fastest delivery is rarely the cheapest or the most thoroughly checked), which is why the approach has to be tailored to what matters most here.']),
    6: dict(
        hl=[('direct and indirect benefits', 1), ('More commitment', 2), ('Customer-oriented focus', 3), ('More efficient use of project resources', 4)],
        notes=['Tailoring brings **direct and indirect benefits**:',
               '**More commitment** from team members, because they helped shape the approach they now follow.',
               'A **customer-oriented focus**, because the customer’s needs drive the tailoring.',
               '**More efficient use of resources**: effort goes where the project needs it, not into unneeded process.'],
        exam=[likely('Which is a stated benefit of tailoring?', a=0,
                     opts=['More commitment from team members who helped tailor the approach', 'Eliminating the need for a project manager', 'A guaranteed fixed scope', 'No further need for stakeholder input'])]),
    7: dict(
        hl=[('Life cycle and development approach selection', 1), ('Processes', 2), ('Engagement', 3), ('Tools', 4), ('Methods and artifacts', 5)],
        notes=['Five aspects can be tailored (slides 8–12 take one each). **Life cycle and development approach**.',
               '**Processes**.', '**Engagement** of people.', '**Tools**.', '**Methods and artifacts**.']),
    8: dict(
        hl=[('Deciding on a life cycle', 1), ('development and delivery approach', 2), ('new data center', 3), ('hybrid approach', 4)],
        notes=['Choosing the **life cycle** and its phases is a form of tailoring.',
               'So is choosing the **development and delivery approach**.',
               'Example: a **new data center** uses a predictive approach for the building’s construction and finishing, and an iterative approach to discover and establish the computing capabilities it needs.',
               'At the project level that combination is **hybrid**, even though each team only experiences its own approach (the construction team sees predictive, the computing team sees iterative).'],
        exam=[likely('A new data center is built in fixed construction phases, while its computing capabilities are worked out in iterations. What is the overall approach?', a=0,
                     opts=['Hybrid', 'Predictive', 'Adaptive', 'Incremental only'])]),
    9: dict(
        hl=[('Process tailoring', 1), ('Added', 2), ('Modified', 2), ('Removed', 2), ('Blended', 2), ('Aligned', 2)],
        notes=['**Process tailoring** decides which parts of the chosen approach’s processes are:',
               '**Added** (extra rigor, e.g. a security review), **modified** (changed to fit, e.g. a lighter weekly report), **removed** (dropped as unnecessary), **blended** (elements from different methods combined into one, e.g. Scrum ceremonies with a predictive budget process) or **aligned** (harmonized so definitions and terms are consistent across teams).'],
        exam=[likely('Combining elements of two different methods into one process is which process-tailoring action?', a=0,
                     opts=['Blending', 'Aligning', 'Adding', 'Removing'])]),
    10: dict(
        hl=[('Engagement', 1), ('People', 2), ('Empowerment', 2), ('Integration', 2)],
        notes=['**Engagement** tailoring decides how people are involved:',
               '**People**: who is on the team and with which skills and capabilities. **Empowerment**: how much responsibility and local decision-making the team gets (a mature team gets more). **Integration**: how contractors, partners and other organizations are brought into the team.']),
    11: dict(
        hl=[('Selecting the tools', 1), ('best insight', 2), ('associated costs', 2), ('constraints that the project team cannot', 3)],
        notes=['Choosing the **tools** (software, equipment) is tailoring.',
               'The team usually has the **best insight** into which tools suit the work, but choices may be tempered by their **cost**.',
               'Organizational leaders may also impose **constraints** the team can’t change (a mandated corporate tool).']),
    12: dict(
        hl=[('Methods and artifacts', 1), ('environment and the culture', 2), ('documents, templates', 3)],
        notes=['**Methods** (the means of achieving outcomes) are tailored to fit the **environment and culture**.',
               '**Artifacts** (documents, templates) are tailored so they are appropriate for the project and organization: a two-page charter for a small internal project, a full one for a regulated contract.']),
    13: dict(
        hl=[('Select Initial', 1, 0, 'ocr'), ('Tailor for', 2, 0, 'ocr'), ('3) Tailor for', 3, 0, 'ocr'), ('Implement', 4, 0, 'ocr')],
        notes=['The tailoring process, step **1**: **select the initial development approach**: choose the approach best suited to the endeavor (the ticked set of gears).',
               'Step **2**: **tailor for the organization**: modify it to fit organizational requirements and constraints.',
               'Step **3**: **tailor for the project**: adjust for size, criticality and other project factors.',
               'Step **4**: **implement ongoing improvement**: inspect and adapt; the loop arrow shows it never ends.'],
        exam=[likely('Put the four steps of the tailoring process in order.',
                     a='(1) Select the initial development approach; (2) tailor the approach for the organization; (3) tailor it for the project; (4) implement ongoing improvement (inspect and adapt throughout the project).')]),
    14: dict(
        hl=[('Selecting the Initial Development Approach', 1, 1, 'ocr'), ('Tailoring the Approach for the Organization', 2, 0, 'ocr'), ('Tailoring the Approach for the Project', 3, 0, 'ocr'), ('Implement Ongoing Improvement', 4, 0, 'ocr')],
        notes=['Step 1 in pictures: choose the base approach, e.g. agile or waterfall (the handwritten note).',
               'Step 2: one set of gears becomes the organization’s adapted version.',
               'Step 3: elements are removed (the crossed boxes) and adjusted for this project.',
               'Step 4: the remaining process keeps being refined.']),
    15: dict(
        hl=[('Tailoring at the', 1, 0, 'ocr'), ('Tailoring at the Project Level', 2, 0, 'ocr'), ('Environmental Factors', 3, 0, 'ocr')],
        notes=['Tailoring happens at **two levels**. At the **organizational** level, a general PM methodology and development approach are adapted into the organization’s own methodologies, e.g. one for small projects and one for large or sensitive projects.',
               'At the **project** level, each project tailors further (methodologies for projects A–E differ).',
               'Both levels are guided by **environmental factors**, general guides, and the available models, methods and artifacts.']),
    16: dict(
        hl=[('Many attributes influence', 1), ('Product/deliverable', 2), ('Project team', 2), ('Culture', 2)],
        notes=['Tailoring for the project depends on many attributes, grouped into three:',
               '**Product/deliverable** (slide 17), **project team** (slide 18) and **culture** (slide 19).']),
    17: dict(
        hl=[('Product/Deliverable', 1), ('Compliance/criticality', 2), ('Stability of requirements', 3), ('Security', 3)],
        notes=['**Product/deliverable** attributes.',
               '**Compliance and criticality**: how much rigor and assurance are needed. Also the type of product, the industry market, the technology and the time frame.',
               '**Stability of requirements** (stable favours predictive, volatile favours adaptive) and **security** needs.']),
    18: dict(
        hl=[('Project Team', 1), ('Project team size', 2), ('geography', 2), ('Project team experience', 3), ('Access to customer', 3)],
        notes=['**Project team** considerations.',
               'Team **size** and **geography** (co-located or distributed), and how it is distributed across the organization.',
               'Team **experience** (an experienced team needs less prescribed process) and **access to the customer** (adaptive approaches need frequent customer input).']),
    19: dict(
        hl=[('shared norms, beliefs, and practices', 1), ('formal and hierarchical, agile and collaborative', 2), ('Buy-in', 3), ('Trust', 3), ('Empowerment', 3)],
        notes=['**Culture** is the organization’s **shared norms, beliefs and practices**.',
               'Tailoring checks how the approach fits it: is the culture **formal and hierarchical, agile and collaborative**, risk-averse or innovation-driven? An agile process forced onto a strictly hierarchical culture struggles.',
               'Evaluate **buy-in** (support from key stakeholders), **trust**, **empowerment** and the organizational culture as a whole.']),
    20: dict(
        hl=[('not a single, one-time exercise', 1), ('progressive elaboration', 2), ('Review points, phase gates, and retrospectives', 3)],
        notes=['Tailoring is **not a one-time exercise** done at the start.',
               'During **progressive elaboration**, problems with how the team works or how the product evolves show where more tailoring would help.',
               '**Review points, phase gates and retrospectives** are the opportunities to inspect and adapt the process, the approach and the delivery frequency.'],
        exam=[likely('True or false: tailoring is done once, when the project is initiated.', tf=False,
                     why='It continues throughout the project; reviews, phase gates and retrospectives are chances to adapt.')]),
    21: dict(
        hl=[('Poor quality deliverables', 1, 0, 'ocr'), ('Long delays waiting for approvals', 2, 0, 'ocr'), ('Too much work in progress', 3, 0, 'ocr'), ('Lack of visibility', 4, 0, 'ocr')],
        notes=['The pattern in this table: name the problem, then tailor in the missing control. **Poor quality deliverables** → add feedback, verification loops and quality-assurance steps. Members unsure how to proceed → add guidance, training and verification.',
               '**Long approval delays** → streamline decisions: fewer people authorized to decide, up to value thresholds.',
               '**Too much work in progress or scrap** → value-stream mapping and kanban boards to visualize the work and find the problems. Disengaged stakeholders → check information sharing and feedback loops; deeper engagement may work better than simply communicating.',
               '**Lack of visibility of progress** → make sure the right measures are collected, analysed and discussed, and validated with the team and stakeholders. Recurring surprises → root-cause analysis of gaps in the process.'],
        exam=[likely('A team keeps waiting several days for approvals before it can proceed. What tailoring change does the table suggest?',
                     a='Streamline approval decisions: authorize fewer people to make decisions, up to certain value thresholds, so routine approvals don’t queue.')]),
    22: dict(
        hl=[('considered adaptation', 1), ('people elements, the processes employed, and the tools', 2), ('Select initial approach', 3), ('Implement ongoing improvement', 3)],
        notes=['Summary: tailoring is the **considered adaptation** of approach, governance and processes to the environment and project.',
               'It involves analysing, designing and deliberately modifying the **people, processes and tools**.',
               'Four steps: **select** the initial approach → tailor for the **organization** → tailor for the **project** → **implement ongoing improvement**.']),
    23: dict(notes=['Section divider: models, methods and artifacts.']),
    24: dict(
        hl=[('high-level description', 1), ('not intended to be exhaustive or', 2)],
        notes=['This section gives a **high-level description** of common models, methods and artifacts.',
               'It is **not exhaustive or prescriptive**: a menu of options to tailor from, not a checklist to use every time.']),
    25: dict(
        hl=[('Model', 1, 1), ('thinking strategy', 1), ('Method', 2, 1), ('means for achieving an outcome', 2), ('Artifact', 3, 1), ('template, document, output', 3)],
        notes=['A **model** is a **thinking strategy** that explains a process, framework or phenomenon (e.g. Tuckman explains how teams develop).',
               'A **method** is the **means for achieving** an outcome, output, result or deliverable (e.g. estimating, a retrospective).',
               'An **artifact** is a **template, document, output or deliverable** (e.g. a risk register, a project charter). Model = think, method = do, artifact = thing.'],
        exam=[likely('A risk register is best classified as a:', a=0, opts=['Artifact', 'Model', 'Method', 'Principle']),
              asked('f251', 'Q1.4', 'Give an example of a project management tool or technique that you might use to manage a complex software development project, and explain how it could help you ensure project success.',
                    a='A Work Breakdown Structure: it decomposes the complex system into smaller deliverables and work packages that can be estimated, assigned and tracked. Nothing is forgotten, ownership is clear, and the WBS is the base for the schedule, budget and risk analysis, so problems show up early and progress is measurable. (Other valid answers: Gantt chart, CPM, risk register, Scrum board with a burndown chart, each with its benefit explained.)')]),
    26: dict(
        hl=[('Principles of Project Management', 1, 0, 'ocr'), ('Guide Behavior', 2, 0, 'ocr'), ('Project Performance', 3, 0, 'ocr')],
        notes=['The whole PMBOK 7 picture in one diagram. At the top, the **12 principles**…',
               '…**guide behavior** in…',
               '…the **8 performance domains** (the circle), which are carried out with **models, methods and artifacts** (left and right) to produce deliverables. Everything sits inside the system for value delivery and the internal and external environments, and is **tailored to fit the project context** (bottom).']),
    27: dict(
        hl=[('associated costs', 1), ('consider these implications', 2), ('Duplicates or adds unnecessary effort', 3), ('incorrect or misleading information', 3), ('individual needs', 3)],
        notes=['Every model, method and artifact has **costs**: time, the expertise needed to use it, the impact on productivity.',
               'Teams should **weigh these** before adopting one.',
               'Avoid anything that **duplicates** work or adds unnecessary effort, isn’t useful to the team and stakeholders, produces **incorrect or misleading** information, or serves one **individual’s** needs rather than the team’s (a report one manager likes but nobody reads).']),
    28: dict(
        hl=[('Situational Leadership® II', 1), ('OSCAR Model', 2), ('Cross-Cultural Communication', 3), ('Effectiveness of Communication Channels', 3), ('Gulf of Execution and Evaluation', 4)],
        notes=['**Situational Leadership II**: the PM adapts style to each member’s **development level** (competence and commitment): directing a beginner, coaching, supporting, then delegating to an expert. The instructor’s note: understand these models, don’t memorize them.',
               '**OSCAR** (Outcome, Situation, Choices/consequences, Actions, Review): a coaching model for guiding conversations, solving problems and developing people.',
               '**Communication models**: cross-cultural communication (principles for communicating across cultures) and the effectiveness of communication **channels** (clarity, speed, richness, recordability, accessibility, suitability): pick the channel that fits the message.',
               '**Gulf of execution and evaluation** (from UX): the gap between a user’s goal and what the system lets them do, and between the system’s response and the user’s ability to interpret it.'],
        exam=[likely('Which model helps a project manager adapt leadership style to each team member’s development level?', a=0,
                     opts=['Situational Leadership II', 'Cynefin framework', 'ADKAR', 'Salience model'])]),
    29: dict(
        hl=[('Hygiene and Motivational Factors', 1), ('Intrinsic', 2), ('Extrinsic', 2), ('hierarchy of Needs', 3), ('Theory X, Theory Y, and Theory Z', 4)],
        notes=['**Herzberg’s hygiene and motivational factors**: **hygiene** factors (salary, benefits, conditions, policies, job security) only prevent dissatisfaction; real **motivators** are achievement, recognition, advancement, responsibility, the work itself and growth. A pay rise is hygiene, not a motivator.',
               '**Intrinsic** motivation comes from the work itself (it excites you); **extrinsic** from outside rewards (pay, grades).',
               '**Maslow’s hierarchy of needs**: physiological → safety → love/belonging → esteem → self-actualization; lower needs come first.',
               '**Theory X**: people dislike work and must be controlled. **Theory Y**: people want to work and should be empowered. **Theory Z**: long-term employment, loyalty and involvement.'],
        exam=[likely('In Herzberg’s model, which of these is a motivator rather than a hygiene factor?', a=0,
                     opts=['Recognition', 'Salary', 'Working conditions', 'Job security']),
              likely('A manager assumes employees dislike work and must be closely supervised. Which theory does this reflect?', a=0,
                     opts=['Theory X', 'Theory Y', 'Theory Z', 'Situational Leadership'])]),
    30: dict(
        hl=[('ADKAR® Model', 1), ('8-Step Process for Leading Change', 2), ('Virginia Satir Change Model', 3), ('Transition Model', 4)],
        notes=['**ADKAR** focuses on **individual** change: Awareness → Desire → Knowledge → Ability → Reinforcement.',
               '**Kotter’s 8 steps** lead **organizational** change: create urgency → build a guiding coalition → form a vision → enlist volunteers → remove barriers → generate short-term wins → sustain acceleration → institute the change.',
               '**Virginia Satir** model: how individuals and organizations **emotionally** respond to change (an initial dip in performance before improvement).',
               '**Transition model** (Bridges): the emotional journey through change: ending, neutral zone, new beginning.'],
        exam=[likely('Which change model focuses on the individual, through awareness, desire, knowledge, ability and reinforcement?', a=0,
                     opts=['ADKAR', 'Kotter’s 8-step process', 'Stacey matrix', 'Tuckman ladder'])]),
    31: dict(
        hl=[('Cynefin Framework', 1), ('rigid processes to unpredictable', 1), ('Stacey Matrix', 2), ('Waterfall, Agile, or hybrid', 2)],
        notes=['**Cynefin** sorts situations into obvious (apply best practice), complicated (analyse with experts), complex (probe and experiment) and chaotic (act first). It stops teams applying rigid processes to unpredictable projects.',
               'The **Stacey matrix** places a project by how uncertain its requirements and its technology are: the more uncertain both are, the more an agile or adaptive approach fits. It helps choose waterfall, agile or hybrid.'],
        exam=[likely('Which model helps decide between waterfall, agile and hybrid approaches based on how uncertain the requirements and technology are?', a=0,
                     opts=['Stacey matrix', 'ADKAR', 'OSCAR', 'Salience model'])]),
    32: dict(
        hl=[('Tuckman Ladder', 1), ('Drexler/Sibbet Team Performance Model', 2)],
        notes=['**Tuckman ladder**: forming → storming → norming → performing → adjourning. Chapter 3 covers each stage, and the midterm asked which stage has members competing for leadership (storming).',
               '**Drexler/Sibbet**: seven stages: orientation → trust building → goal clarification → commitment → implementation → high performance → renewal.'],
        exam=[asked('m251v1', 'MCQ 7', 'According to Tuckman’s model of team development, which stage is characterized by members competing for leadership and struggling with group processes?',
                    a=0, opts=['Storming', 'Norming', 'Adjourning', 'Performing'],
                    why='Storming is when members compete for leadership and test group processes; norming comes after, when agreement is reached. (Also Midterm 251 V2 MCQ 7.)')]),
    33: dict(
        hl=[('Conflict Model', 1), ('Negotiation', 1), ('Process Groups', 1), ('Salience Model', 2)],
        notes=['Other models: conflict (styles of handling conflict, Chapter 3), negotiation, planning, and process groups (initiating, planning, executing, monitoring and controlling, closing).',
               'The **salience model** prioritizes stakeholders by **power, legitimacy and urgency** to decide how much attention each needs (Chapter 8).'],
        exam=[asked('f251', 'Q3.2', 'How can project managers identify and prioritize stakeholders, and what strategies can they use to communicate effectively with each stakeholder group?',
                    a='Identify stakeholders by brainstorming with the team, reading the charter and contracts, and interviewing key people, then record them in a stakeholder register. Prioritize them with a power/interest grid (or the salience model: power, legitimacy, urgency). Then tailor communication: high power and high interest → manage closely with interactive meetings; high power, low interest → keep satisfied with concise push reports; low power, high interest → keep informed with push updates or pull (portal); low/low → monitor.',
                    why='Chapter 8 develops stakeholder management.')]),
    34: dict(hl=[('Situational Leadership', 1, 0, 'ocr'), ('Stacey matrix', 1, 0, 'ocr')], notes=[TABLE + ' Models: e.g. situational leadership and OSCAR help the team and project-work domains; the Stacey matrix helps choose the development approach and handle uncertainty.']),
    35: dict(
        hl=[('Data gathering and analysis', 1), ('Estimating', 2), ('Meetings and events', 3)],
        notes=['Method families: **data gathering and analysis** (alternatives analysis, root-cause analysis, cost of quality, earned value, SWOT…).',
               '**Estimating** (affinity grouping, function points, story points, Delphi…).',
               '**Meetings and events** (kickoff, stand-up, retrospective, review, steering committee…), and other methods.']),
    36: dict(hl=[('Alternatives analysis', 1, 0, 'ocr'), ('Make-or-buy analysis', 1, 0, 'ocr')], notes=[TABLE + ' Data methods: e.g. make-or-buy analysis serves planning and project work; probability-and-impact matrices serve uncertainty.']),
    37: dict(notes=[TABLE + ' Estimating methods and meetings (e.g. retrospectives serve team and project work; risk reviews serve uncertainty).']),
    38: dict(
        hl=[('Strategy Artifacts', 1), ('Logs and registers', 2), ('Plans', 3), ('Baselines', 3), ('Agreements and contracts', 3)],
        notes=['**Strategy artifacts**: strategic plan, vision and mission statements, roadmap, **business case**.',
               '**Logs and registers**: issue log, risk register, communication log, stakeholder register, lessons-learned register.',
               'Also **plans** (risk management plan, communications plan…), hierarchy charts (WBS, org chart), **baselines** (scope, schedule, cost), visual data (burn charts, Gantt charts), reports, **agreements and contracts**, and others.'],
        exam=[likely('A business case belongs to which category of artifacts?', a=0,
                     opts=['Strategy artifacts', 'Logs and registers', 'Baselines', 'Reports'])]),
    39: dict(hl=[('Business case', 1, 0, 'ocr'), ('Risk register', 1, 0, 'ocr')], notes=[TABLE + ' Artifacts: e.g. the business case and charter serve stakeholders and planning; the risk register serves planning, project work, delivery and uncertainty.']),
    40: dict(notes=[TABLE + ' Hierarchy charts, baselines and visual data (e.g. burn charts serve measurement).']),
    41: dict(notes=[TABLE + ' Reports, agreements and contracts.']),
}

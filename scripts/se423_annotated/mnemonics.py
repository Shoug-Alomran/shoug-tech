"""SE423 memory aids added to slides as Tips & tricks, by deck key and slide number.

Shoug's rule: an acronym spells a real word wherever possible. A list whose order doesn't matter may be reordered to
get one, and lowercase filler letters are fine (the capitals are the initials). A list whose order matters keeps it,
as a word or a sentence. Chapter 1 keeps its tips in ch01_page.py. A `**WORD**: a, b, c.` tip is checked at build time.
"""
import re

TIPS = {
    'ch1.2': {
        11: ['Sentence, in slide order: **V**ery **R**ich **P**eople **G**et **G**old. Vision and objectives, Roles and responsibilities, Project team operations, Guidance, Growth.'],
        13: ['**CRyPTICS**: Courage, Respect, Positive discourse, Transparency, Integrity, Celebrating success, Support.'],
        14: ['**R**oller **COASTERS**: Recognition, then Collaboration, Open communication, Adaptability, Shared understanding, Trust, Empowerment, Resilience, Shared ownership.'],
        15: ['**MICE**: Motivation, Interpersonal skills, Critical thinking, Establishing and maintaining vision.'],
        17: ['**DEMO**: Distributed teams, Experience with the project type, Maturity of team members, Organizational governance.'],
        23: ['**HeAP**: Hybrid, Adaptive, Predictive.'],
        29: ['Sentence, in slide order: **D**on’t **R**ush **S**cope: **E**very **D**elivery **R**isks **S**afety **R**ules. Degree of innovation, Requirements certainty, Scope stability, Ease of change, Delivery options, Risk, Safety requirements, Regulations.'],
        30: ['**SaFeS**: Stakeholders, Funding availability, Schedule constraints.'],
        31: ['**SuCCeSs**: Structure, Culture, Capability, Size and location of the team.'],
        41: ['The order matters here: **D**ogs **S**neak **E**very **A**pple **A**way. Decompose, Sequence, Estimate, Allocate, Adjust.'],
        42: ['**DIME**: Discretionary, Internal, Mandatory, External.'],
        83: ['**DIV**, like the HTML tag: Dashboards, Information radiators, Visual controls.'],
        89: ['**CRAVe**: Complexity, Risk, Ambiguity, Volatility.'],
        91: ['**PLATE SPinning**: Political, Legal, Ambiguity, Technical, Economic, Social and market, Physical.'],
        97: ['**lIFE**: Iterate, Fail safe, Engage.'],
        102: ['Threats, the **A TEAM**: Accept, Transfer, Escalate, Avoid, Mitigate.'],
        104: ['Opportunities, in slide order: **E**ach **E**xtra **S**hare **E**arns **A**gain. Exploit, Escalate, Share, Enhance, Accept.'],
    },
    'ch1.3': {
        5: ['**COMPADreS**: Creating high-quality deliverables, Optimizing value, Minimizing costs, Providing compliance, Adapting to change, Delivering quickly, Satisfying stakeholders.'],
        7: ['**TEMPLe**: Tools, Engagement, Methods and artifacts, Processes, Life cycle and development approach.'],
        9: ['**A RuMBA**: Aligned, Removed, Modified, Blended, Added.'],
        10: ['**PIE**: People, Integration, Empowerment.'],
        16: ['**CoPPer**: Culture, Project team, Product or deliverable.'],
        17: ['Sentence, in slide order: **C**ats **T**ake **I**n **T**oo **T**iny **S**nacks, **S**adly. Compliance, Type of product, Industry market, Technology, Time frame, Stability of requirements, Security.'],
        18: ['**SAGE O**wl: Size of the team, Access to customer, Geography, Experience, Organizational distribution.'],
        19: ['**TO BE**: Trust, Organizational culture, Buy-in, Empowerment.'],
        22: ['The order matters here: **S**mart **T**eams **T**ailor **I**teratively. Select the initial approach, Tailor for the organization, Tailor for the project, Implement ongoing improvement.'],
        25: ['**MaMA**: Model, Method, Artifact.'],
        35: ['**DEMO**: Data gathering and analysis, Estimating, Meetings and events, Other methods.'],
        38: ['Sentence, in slide order: **S**tudents **L**ove **P**izza, **H**ot **B**urgers, **V**anilla **R**olls **A**nd **O**reos. Strategy, Logs and registers, Plans, Hierarchy charts, Baselines, Visual data, Reports, Agreements, Other.'],
    },
    'ch2': {
        5: ['The order matters here: **D**on’t **F**orget **M**y **A**im. Developing vision and mission, Formulating strategy, Making cross-functional decisions, Achieving objectives.'],
        10: ['**PerFuMe**: Project, Functional, Matrix.'],
        19: ['**CRaTE**: Center for excellence, Repository, Technical details, Expertise.'],
        21: ['**SCoreD**, from low control to high: Supportive, Controlling, Directive.'],
        22: ['**CRoW**: Control tower, Resource pool, Weather station.'],
        23: ['**HURT**: Held by a subset of the organization, Unwritten, Rules of behavior, Taught to new members.'],
        24: ['**CRaG TREK**: Critical incidents, Reward systems, Geographical location, Technology, Rules and procedures, Environment, Key organizational members.'],
        25: ['**PEPpeD**: Project planning, Employee commitment, Performance evaluation, Departmental interaction.'],
    },
    'ch3': {
        8: ['The order matters, and they rhyme: **F**orm, **S**torm, **N**orm, **P**erform, then **A**djourn.'],
        15: ['Sentence, in slide order: **C**ool **C**ats **W**ill **S**till **C**alm **F**ights. Confronting, Compromising, Withdrawal, Smoothing, Collaborating, Forcing.'],
        17: ['**CuB**: Clarity, Buy-in.'],
        27: ['Team models, in slide order: **B**usy **D**evelopers **C**ode **S**uper **S**oftware. Business, Democratic, Chief-programmer, Skunk works, SWAT.'],
        30: ['**BAT CLiP**: Backup programmer, Administrator, Tool-smith, Chief programmer, Language lawyer, Program clerk.'],
        37: ['Sentence, in slide order: **P**roject **M**anagers **P**lan, **E**stimate, **C**ontrol, **O**rganize. Problem solving, Motivating, Planning, Estimating, Controlling, Organizing.'],
        38: ['Maslow from the bottom up, where the order matters: **P**lease **S**tudents, **S**tudy **E**very **S**ession. Physiological, Safety, Social, Esteem, Self-realization.'],
        41: ['**SIT**: Self-oriented, Interaction-oriented, Task-oriented.'],
        44: ['**WIN**: Working alone, Interaction with others, Non-productive.'],
        53: ['Sentence, in slide order: **A**ll **P**rogrammers **P**refer **E**asy **C**ode **A**nd **A**wesome **P**izza. Application domain, Platform, Programming language, Educational background, Communication ability, Adaptability, Attitude, Personality.'],
        54: ['**PaCiFy**: Privacy, Comfort, Facilities.'],
        55: ['**POP**: Privacy, Outside awareness, Personalization.'],
        58: ['**SLiMMIng**: Shaping project culture, Leadership, Managing people, Making people better, Interpersonal skills.'],
        60: ['Slides 59 and 60 together, **IMPLEmeNt**: Influencing, Motivation, Problem solving, Leadership, Effective communication, Negotiation.'],
        62: ['Cultural roles, in slide order: **L**azy **L**ions **C**atch **E**very **C**ow. Leader, Listener or talker, Complainer, Expert, Charger or plodder.'],
        75: ['The order matters here: **P**lease **S**it **D**own, **W**e **C**onfirm. Pose the problem, Solicit input, Discuss pros and cons, Work toward the best options, Confirm the choice.'],
    },
    'ch4': {
        10: ['**MAP**: Milestones, Activities, Process.'],
        11: ['**STaR**: Skills, Teams, Roles.'],
        12: ['**PuTT**: Products, Techniques, Tools.'],
        20: ['The order matters here: **R**eal **A**rchitects **D**raw, **C**onstruct, **Q**uality-check, **D**eploy. Requirements, Analysis, Design, Construction, Quality assurance, Deployment.'],
        23: ['**FALConS**: Familiar technology, Adequate time, Low complexity, Clear requirements, Stable schedule.'],
        25: ['**CIRCA**: Component-based development, Iterative life cycle, Round-trip engineering, Change management environment, Architecture first.'],
        26: ['**InfECT**, already in order: Inception, Elaboration, Construction, Transition.'],
        32: ['**RUSHeS**, the opposite of slide 23: Reasonably clear requirements, Unfamiliar technology, Short time, High complexity, Schedule variability.'],
        38: ['The four values, in order: **I** **W**ill **C**hange **R**eadily. Individuals and interactions, Working software, Customer collaboration, Responding to change.'],
        42: ['Slides 41 and 42 together, **MIdFiElD**: Maintain simplicity, Involve the customer, Focus on people, Embrace change, Develop incrementally.'],
        47: ['The order matters here: **C**ooks **R**oast **I**n **I**ron **D**ishes. Choose features, Refine them, Implement and test, Integrate and test, Deliver.'],
        50: ['Slides 50 to 54, **STRICt**: Small releases, Test-driven development, Refactoring, Incremental planning, Continuous integration.'],
        60: ['**PoST**: Product owner, ScrumMaster, Team.'],
        63: ['**STeP**: Self-organizing teams, Timeboxed sprints, Product backlog.'],
        66: ['**CRIb**, already in order: Consideration, Refinement, Implementation.'],
        82: ['**COMMiTteD**: Collaborative culture, On-time and quality, MVP mindset, Metrics, Tools, Dependencies.'],
    },
    'ch5': {
        2: ['The order matters here: **I** **A**m **P**lanning **M**ore. Identification, Analysis, Planning, Monitoring.'],
        5: ['**MULe**: Manageable, Uncertainty, Loss or gain.'],
        6: ['Threat types, in slide order: **R**isky **C**ode **S**hips **Q**uite **L**ate. Requirements, Cost, Schedule, Quality, Life cycle.'],
        14: ['Slides 13 and 14 together, **PUnK**: Predictable, Unpredictable, Known.'],
        18: ['Slides 18 to 20, **uPBeaT**: Project, Business, Technical.'],
        19: ['Sentence, in slide order: **D**on’t **I**gnore **I**nterface **V**erification, **C**utover, **M**aintenance, **S**ecurity. Design, Implementation, Interfacing, Verification, Cutover, Maintenance, Security.'],
        22: ['Slides 22 to 25, **ACID**: Assumptions analysis, Checklist analysis, Information gathering, Documentation reviews.'],
        31: ['Sentence, in slide order: **P**eople **B**uy **C**offee, **P**ay **D**ollars, **T**ip **S**taff. Product size, Business impact, Customer characteristics, Process definition, Development environment, Technology, Staff size and experience.'],
        60: ['Slides 60 and 61 together, in order: **M**ost **R**isks **B**ite. **T**eams **C**an **T**ame **R**isks **T**oday. Methodology, Roles, Budgeting, Timing, Categories, Tolerances, Reporting formats, Tracking.'],
        63: ['Slides 62 and 63 together, **A CAT**: Agreed, Cost-effective, Assigned, Timely.'],
        65: ['Slides 65 to 70, **CAT MAt**: Contingency, Avoidance, Transfer, Mitigation, Acceptance.'],
        68: ['**MMM**, all three start the same: Mitigation, Monitoring, Management.'],
        78: ['**CRAWleRS**: Closing risks, Reassessments, Audits, Workarounds, Reserve analysis, Status meetings.'],
    },
    'ch6': {
        9: ['**BEAT PoP**: Bottom-up, Expert judgment, Analogy, Top-down, Priced to win, Parametric.'],
        23: ['The causes, in slide order: **V**ery **U**nlucky **E**stimators **M**iss. Varying skill levels, Unexpected events, Efficiency of work time, Mistakes and misunderstandings.'],
        27: ['**ORE**: Organization policy, Resource availability, Enterprise environment.'],
        34: ['**MOP**: Most likely, Optimistic, Pessimistic.'],
        40: ['**hOSE**, from small to large: Organic, Semi-detached, Embedded.'],
        53: ['**NoRM**: New, Reused, Modified.'],
        57: ['**ARM**, already in order: Aggregation, Risk analysis, Management reserves.'],
    },
    'ch6.2': {
        4: ['**PEST**, already in order: Plan, Estimating, Scheduling, Tracking.'],
        6: ['The order matters here: **D**on’t **S**kip **R**eal **D**ates. Definition, Sequencing, Resource estimating, Duration estimating.'],
        11: ['**HiPPo**: Hybrid, Process, Product.'],
        15: ['Slides 15 to 19, **RABBiT**: Rolling wave, Analogy, Bottom-up, Brainstorming, Top-down.'],
        20: ['**CROC MaN**: Costing, Risk analysis, Organizational structure, Control, Measurement, Network scheduling.'],
        23: ['Sentence, in slide order: **G**ood **C**rews **C**heck **W**ork **R**egularly. Gantt charts, Critical path, Critical chain, What-if analysis, Resource leveling.'],
        33: ['**MOP** again: Most likely, Optimistic, Pessimistic.'],
        45: ['**PReF**: Project buffer, Resource buffer, Feeder buffer.'],
        53: ['**CARS**: Concurrency, Adding resources, Reducing scope, Substitution of activities.'],
    },
    'ch7': {
        19: ['**WHOA**: Within budget, High quality, On schedule, According to requirements.'],
        21: ['Sentence, in slide order: **E**very **U**ser **E**njoys **C**lear **M**aps **S**o **F**ew **F**eel **R**ushed. Executive support, User involvement, Experienced manager, Clear objectives, Minimized scope, Standard infrastructure, Firm requirements, Formal methodology, Reliable estimates.'],
        22: ['**GRaSP**: Get approval, Receive cooperation, Secure resources, Provide leadership.'],
        41: ['**SPeD**: Static product analysis, Process data collation, Dynamic product analysis.'],
    },
    'ch8': {
        8: ['The levels, in order: **U**ncle **R**eally **N**eeds **S**ome **L**ove. Unaware, Resistant, Neutral, Supportive, Leading.'],
        26: ['The order matters here: **I** **U**sually **A**sk **P**eople **E**very **M**onth. Identify, Understand, Analyze, Prioritize, Engage, Monitor.'],
        37: ['**PIP**: Push, Interactive, Pull.'],
        40: ['Sentence, in slide order: **S**ome **P**eople **T**ell **F**unny **V**ery **E**xciting **L**ies. Status, Progress, Trend, Forecasting, Variance, Earned value, Lessons learned.'],
    },
    'ch9': {
        16: ['**MAR**: Maintenance, Architectural transformation, Re-engineering.'],
        25: ['**SCulPT**: Staff skills, Contractual responsibility, Program age and structure, Team stability.'],
        37: ['Sentence, in slide order: **R**eal **T**eams **D**eliver **M**any **M**ilestones. Release checklist, Training, Documentation, Migration, Maintenance.'],
        41: ['**MUSSeS**: Maintenance engineers, Users, Sales and marketing, System operators, Sales engineers. Then add Support staff.'],
        49: ['**CaRROt**: Criteria, Responsibility, Rehearsals, Operations.'],
        58: ['**CoInS**: Cut the size, Increase productivity, Slip the schedule.'],
        62: ['Sentence, in slide order: **M**y **R**ed **V**an **C**ould **F**ly. Minimal specification, Requirements scrubbing, Versioned development, Change control, Feature cuts.'],
    },
}


def check():
    """Every `**WORD**: a, b, c.` tip: the word's capitals must be the items' initials, in the same order."""
    bad = []
    for key, slides in TIPS.items():
        for n, tips in slides.items():
            for tip in tips:
                m = re.search(r'\*\*([A-Za-z ]+)\*\*[^:]*: ([^.]+)\.$', tip)
                if not m or not re.search(r'[A-Z]{2}|[a-z][A-Z]', m.group(1)):
                    continue
                caps = re.sub(r'[^A-Z]', '', m.group(1))
                items = re.sub(r'^.*?: ', '', m.group(2)) if ': ' in m.group(2) else m.group(2)
                initials = ''.join(i.strip()[0].upper() for i in items.split(','))
                if caps != initials:
                    bad.append('%s slide %d: %s spells %s, items give %s' % (key, n, m.group(1), caps, initials))
    if bad:
        raise SystemExit('Mnemonics that do not match their lists:\n' + '\n'.join(bad))


check()

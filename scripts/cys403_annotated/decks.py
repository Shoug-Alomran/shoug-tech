"""CYS403 annotated slides — every Security Risk Management, Governance and Control deck.

One module holds all the decks: each deck is a namespace class with DECK and ANN (and AUTO_SLIDES).
Slides without an ANN entry are shown without notes. past(...) points at the three past papers in
exams/ (Quiz 1 Term 222, Quiz 2, Major exam). See cs331_annotated/ch01_1_introduction.py for the ANN keys."""
from .common import DECKS, mcq, past, see, short, tf, tip, trap, trick


def deck(key, title, chapter, lede):
    slug, file, folder, _ = DECKS[key]
    return {'key': key, 'slug': slug, 'file': file, 'title': title, 'chapter': chapter,
            'pdf': '/academics/cybersecurity/cys403/slides/%s/' % folder, 'lede': lede}


ALE = 'SLE = AV × EF · ARO = how many times a year · ALE = SLE × ARO · Value of a control = ALE(before) − ALE(after) − annual cost of the control.'


class governance:
    AUTO_SLIDES = True
    DECK = deck('d01', 'Security Risk Management, Governance and Control', 'Chapter 1',
                'Why cyber risk matters to the business, IT risk vs. IT value (Risk IT, Val IT, COBIT), the CIA '
                'triad, business-driven security, cybersecurity management and governance, security blueprints, '
                'the policy hierarchy (policies, standards, procedures, baselines, guidelines) and planning horizons.')
    ANN = {
        4: dict(notes=['Every business decision carries risk; security exists to support business goals, not the other way round.']),
        9: dict(notes=['IT risk is the flip side of IT value: managing risk protects the value IT creates.']),
        10: dict(notes=['Risk IT extends Val IT and COBIT (ISACA frameworks) to cover IT-related business risk.'],
                 past=[past('q222', 'the framework for compliance, risk and IT alignment')],
                 exam=[mcq('Which framework helps organizations with regulatory compliance, risk management and aligning IT strategy with business goals?', ['COBIT', 'OCTAVE', 'STRIDE', 'DREAD'], 0, '')], weight=3),
        12: dict(notes=['CIA triad: Confidentiality (only authorized people see it), Integrity (not altered improperly), Availability (there when needed).'],
                 past=[past('q222', 'only those supposed to access the data can')],
                 exam=[mcq('Making sure only those who are supposed to access the data can access it is:', ['Confidentiality', 'Integrity', 'Availability', 'Non-repudiation'], 0, '')], weight=3),
        13: dict(notes=['Business-driven security: start from business requirements and risk appetite, then choose controls.']),
        14: dict(notes=['Management support is the most important factor for a successful security program.'],
                 past=[past('q222', 'the most important factor for security to succeed')],
                 exam=[mcq('The most important factor in ensuring security succeeds in an organization is:', ['Senior management support', 'The latest technology', 'A large security budget', 'Strong passwords'], 0, '')], weight=3),
        19: dict(notes=['Governance: the board and executives set direction, accountability and oversight; management executes.'],
                 past=[past('q2', 'who should be involved in security risk management')],
                 exam=[short('Why should executives and IT/security teams communicate well?', 'Executives own the business risk and the budget; IT/security understand the threats and controls. Without shared understanding, security spending won’t match business priorities and executives can’t make informed risk decisions.')], weight=3),
        21: dict(notes=['Data owner (a senior manager) decides the classification level of information; the custodian implements the protection.'],
                 past=[past('q222', 'who decides the classification level'), past('major', 'the person in charge of a data domain', related=True)],
                 tips=[trap('Owner DECIDES classification; custodian (IT) IMPLEMENTS controls; auditors MEASURE effectiveness.')],
                 exam=[mcq('Who has primary responsibility for determining the classification level of information?', ['The data owner', 'The data custodian', 'The security administrator', 'The user'], 0, ''),
                       mcq('Who should measure the effectiveness of information-security controls?', ['IS auditors', 'Data custodians', 'End users', 'Developers'], 0, '')], weight=3),
        23: dict(notes=['Policies: high-level management statements of what must be protected and why (mandatory, technology-neutral).'],
                 past=[past('q222', 'what security policies are')],
                 exam=[mcq('Security policies are best described as:', ['High-level statements of management’s intent', 'Step-by-step instructions', 'Minimum configuration levels', 'Optional recommendations'], 0, '')], weight=3),
        26: dict(notes=['Hierarchy: policy (why) → standards (mandatory what) → procedures (step-by-step how) → baselines (minimum level) → guidelines (optional advice).'],
                 tips=[trick('Policy = WHY, Standard = WHAT (mandatory), Procedure = HOW, Baseline = MINIMUM, Guideline = SHOULD.')],
                 exam=[mcq('Detailed step-by-step instructions for a task are:', ['Procedures', 'Policies', 'Guidelines', 'Baselines'], 0, ''),
                       mcq('Recommended but optional actions are:', ['Guidelines', 'Standards', 'Procedures', 'Policies'], 0, '')], weight=3),
        27: dict(notes=['Data classification groups data by sensitivity (e.g. public, internal, confidential, secret) so each level gets suitable controls.']),
        32: dict(notes=['Planning horizons: strategic (long term, 3–5 years), tactical (mid term, 6 months–1 year or more), operational (short term, day to day to ~6 months).'],
                 past=[past('q2', 'Renee’s one-to-six-month plan')],
                 exam=[mcq('A short-term security plan with a one- to six-month horizon is:', ['Operational', 'Strategic', 'Tactical', 'Contingency'], 0, '')], weight=3),
        33: dict(notes=['Functionality = what a security mechanism does; assurance = the confidence that it does it correctly.'],
                 past=[past('q222', 'functionality vs. assurance')],
                 exam=[mcq('Security functionality defines what a mechanism does; assurance defines:', ['The degree of confidence that it works as expected', 'Its cost', 'Who installs it', 'Its performance'], 0, '')], weight=3),
    }


class fundamentals:
    AUTO_SLIDES = True
    DECK = deck('d02', 'Risk Management Fundamentals', 'Chapter 2',
                'Definitions of risk, threat, vulnerability, asset, exposure and safeguard, risk factors, the risk '
                'equation, risk-management steps and the risk register, quantitative (SLE, ARO, ALE) vs. qualitative '
                'analysis, mitigation options, countermeasure selection and types of security controls.')
    ANN = {
        5: dict(notes=['Risk = the likelihood that a threat exploits a vulnerability, and the impact if it does.']),
        8: dict(notes=['Asset: anything of value. Threat: potential cause of harm. Vulnerability: a weakness. Exposure: being open to loss. Safeguard/countermeasure: reduces risk.'],
                exam=[mcq('A weakness that a threat can exploit is a:', ['Vulnerability', 'Risk', 'Asset', 'Safeguard'], 0, '')], weight=3),
        12: dict(notes=['Threat amplifiers raise the chance of an attack (publicity, a known weakness); threat inhibitors lower it (fear of capture, strong controls).'],
                 past=[past('major', 'threat amplifiers and inhibitors')]),
        16: dict(notes=['Risk management = identify, assess, and reduce risk to an acceptable level. It never removes ALL risk.'],
                 past=[past('q222', 'the best definition of risk management'), past('major', 'the prime directive of risk management')],
                 exam=[mcq('The goal of risk management is to:', ['Reduce risk to an acceptable level', 'Eliminate all risk', 'Transfer all risk', 'Avoid every threat'], 0, '')], weight=3),
        21: dict(notes=['Total risk = threats × vulnerabilities × asset value. Residual risk = total risk − controls gap (what is left after controls).'],
                 past=[past('major', 'the formula for total risk')],
                 exam=[mcq('Total risk is represented by:', ['Threats × Vulnerability × Asset value', 'Threats + Controls', 'ALE − SLE', 'Asset value / Controls'], 0, '')], weight=3),
        22: dict(notes=['Steps: identify assets → identify threats and vulnerabilities → assess (likelihood, impact) → choose responses → monitor.'],
                 past=[past('q2', 'when risk identification happens')]),
        27: dict(notes=['Risk register: one row per risk with owner, likelihood, impact, rating, response and status.']),
        29: dict(notes=['Quantitative: numbers and money (objective, costly). Qualitative: ratings like high/medium/low (fast, subjective).'],
                 past=[past('major', 'what a quantitative analysis is')]),
        30: dict(notes=[ALE],
                 past=[past('major', 'the DoS SLE / ARO / ALE / cost–benefit calculation')],
                 tips=[tip(ALE)],
                 exam=[mcq('Asset value $100,000, exposure factor 25%, ARO 0.5. ALE =', ['$12,500', '$25,000', '$50,000', '$125,000'], 0, 'SLE = 25,000; ALE = 25,000 × 0.5.'),
                       short('Profit is $20,000 a week and a DoS attack lowers sales by 40%. Four attacks happen every 6 months. Find SLE, ARO and ALE.', 'SLE = 20,000 × 0.40 = $8,000. ARO = 4 per 6 months = 8 per year. ALE = 8,000 × 8 = $64,000.')], weight=3),
        34: dict(notes=['Qualitative analysis uses scenarios, ratings and expert judgement (Delphi, brainstorming, checklists).']),
        40: dict(notes=['Four responses: mitigate (reduce), transfer (insurance, outsourcing), avoid (stop the activity), accept (document and live with it).'],
                 past=[past('q2', 'an example of mitigation'), past('major', 'when not acting is acceptable; when to avoid')],
                 tips=[trap('Accepting a risk is a valid, documented decision when the cost of a control exceeds the expected loss.')],
                 exam=[mcq('Buying cyber insurance is risk:', ['Transference', 'Mitigation', 'Avoidance', 'Acceptance'], 0, ''),
                       mcq('It is acceptable not to act on an identified risk when:', ['The cost of the countermeasure exceeds the potential loss', 'The risk is high', 'Management is unaware', 'There is no budget review'], 0, '')], weight=3),
        42: dict(notes=['Choose a countermeasure when its value is positive: ALE before − ALE after − annual cost > 0 (cost–benefit analysis).'], weight=3),
        45: dict(notes=['Control types by nature: administrative, technical (logical), physical. By function: preventive, detective, corrective, deterrent, recovery, compensating.'],
                 past=[past('major', 'logical access control category; encrypting payment files')],
                 exam=[mcq('Logical mechanisms that control access and authenticate users are:', ['Technical controls', 'Administrative controls', 'Physical controls', 'Deterrent controls'], 0, ''),
                       mcq('Encrypting payment files to stop tampering is a:', ['Preventive control', 'Detective control', 'Corrective control', 'Recovery control'], 0, '')], weight=3),
    }


class threats:
    AUTO_SLIDES = True
    DECK = deck('d03', 'Threat and Vulnerability Management', 'Chapter 3',
                'Threat sources and types (network, host, application), threat agents, common vulnerabilities and CVE, '
                'threat modeling methods (STRIDE, PASTA, LINDDUN, CVSS, attack trees, persona non grata, security cards, '
                'hTMM, Trike, VAST, OCTAVE, DREAD) and threat/vulnerability pairs.')
    ANN = {
        6: dict(notes=['Threat sources: human (intentional or accidental), natural, environmental, technical.']),
        7: dict(notes=['Threat categories by target: network, host, application.'],
                past=[past('major', 'SQL injection’s threat type; what is not a threat')],
                exam=[mcq('SQL injection is a(n) ____ threat.', ['Application', 'Network', 'Host', 'Physical'], 0, '')], weight=3),
        12: dict(notes=['Threat agent: the actor (hacker, insider, malware) that carries out the threat.']),
        16: dict(notes=['Vulnerabilities come from design flaws, misconfiguration, missing patches, weak processes and people.']),
        20: dict(notes=['CVE: a public dictionary of known vulnerabilities, each with a CVE-ID (CVE-YEAR-NUMBER).'],
                 exam=[mcq('CVE provides:', ['Standard identifiers for publicly known vulnerabilities', 'Severity scores', 'A threat-modeling method', 'Firewall rules'], 0, 'Scores come from CVSS.')], weight=3),
        23: dict(notes=['Threat modeling: identify what can go wrong in a system and how to address it, early in design.']),
        25: dict(notes=['STRIDE: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege (each breaks one property).'],
                 past=[past('major', 'threat modeling an Azure App Service app')],
                 tips=[trick('Spoofing↔authentication, Tampering↔integrity, Repudiation↔non-repudiation, Info disclosure↔confidentiality, DoS↔availability, EoP↔authorization.')],
                 exam=[mcq('In STRIDE, "Tampering" violates:', ['Integrity', 'Confidentiality', 'Availability', 'Authentication'], 0, ''),
                       mcq('Microsoft’s threat-modeling method for an app is:', ['STRIDE', 'OCTAVE', 'LINDDUN', 'PASTA'], 0, '')], weight=3),
        28: dict(notes=['PASTA: Process for Attack Simulation and Threat Analysis: a 7-stage, risk-centric method.']),
        30: dict(notes=['LINDDUN: privacy threats (Linkability, Identifiability, Non-repudiation, Detectability, Disclosure, Unawareness, Non-compliance).'],
                 exam=[mcq('Which method focuses on PRIVACY threats?', ['LINDDUN', 'STRIDE', 'DREAD', 'Trike'], 0, '')], weight=3),
        33: dict(notes=['CVSS: scores a vulnerability’s severity 0–10 (base, temporal, environmental metrics).']),
        35: dict(notes=['Attack tree: root = attacker’s goal, children = ways to achieve it (AND/OR nodes).']),
        47: dict(notes=['OCTAVE: organizational, self-directed risk assessment of operational risk (Carnegie Mellon).']),
        49: dict(notes=['DREAD rates threats: Damage, Reproducibility, Exploitability, Affected users, Discoverability.'],
                 exam=[mcq('The "R" in DREAD stands for:', ['Reproducibility', 'Repudiation', 'Risk', 'Recovery'], 0, '')], weight=3),
        52: dict(notes=['Threat/vulnerability pair: a threat matters only if a matching vulnerability exists (and vice versa).']),
    }


class lifecycle:
    AUTO_SLIDES = True
    DECK = deck('d04', 'Risk Management Lifecycle', 'Chapter 4',
                'Accountability for risk, the risk-management cycle, risk identification, building an information-asset '
                'inventory, classifying, valuing and ranking assets, threat identification, vulnerability assessment and '
                'the TVA worksheet.')
    ANN = {
        5: dict(notes=['Everyone has a role: management sets direction, IT/security implement, users follow policy, auditors check.']),
        6: dict(notes=['Cycle: identify → assess → treat → monitor and review → repeat. Risk identification happens continuously, not once.'],
                past=[past('q2', 'when risk identification is performed')],
                exam=[mcq('Risk identification should be performed:', ['Continuously, throughout the lifecycle', 'Once at project start', 'Only after an incident', 'Only during audits'], 0, '')], weight=3),
        9: dict(notes=['Risk identification = identify, classify and prioritize assets, then the threats and vulnerabilities against them.']),
        10: dict(notes=['Asset types: people, procedures, data, software, hardware, networking.'],
                 past=[past('major', 'asset identification documentation; two assets with two attributes')],
                 exam=[short('List two information assets with two attributes each.', 'Server: name/IP address, location (or MAC, serial number). Customer database: data owner, classification level (or format, size). Any asset with identifying attributes such as name, ID, location, owner, version, classification.')], weight=3),
        18: dict(notes=['Classify assets (confidential, internal, public…) and categorize them so their importance can be compared.']),
        20: dict(notes=['Valuation questions: how critical to the mission, how much revenue or profit, cost to replace or protect, embarrassment if lost.'], weight=2),
        23: dict(notes=['Rank assets by weighted factor analysis to decide what to protect first.']),
        25: dict(notes=['Vulnerability assessment: for each threat to each asset, list how it could be exploited.']),
        28: dict(notes=['TVA worksheet: assets (ranked) on one axis, threats (ranked) on the other; each cell lists the vulnerabilities; work from the top-left (highest priority).'],
                 exam=[mcq('In a TVA worksheet, the highest-priority cells are:', ['Most valuable asset × most dangerous threat', 'Least valuable asset × weakest threat', 'Random cells', 'Only the bottom row'], 0, '')], weight=3),
    }


class approaches:
    AUTO_SLIDES = True
    DECK = deck('d05', 'Risk Assessment Approaches', 'Chapter 5',
                'Why risk assessments matter, their critical components, quantitative assessment with SLE, ARO, ALE '
                'and cost–benefit analysis, qualitative assessment with likelihood/impact matrices, and the risk '
                'assessment report.')
    ANN = {
        8: dict(notes=['A risk assessment tells management which risks matter most and where to spend money.']),
        11: dict(notes=['Critical components: scope, data collection, threats and vulnerabilities, likelihood, impact, risk determination, recommendations, documentation.']),
        15: dict(notes=['Types: quantitative, qualitative, and hybrid (semi-quantitative).']),
        17: dict(notes=[ALE], tips=[tip(ALE)], seen=[see('d02', 30, 'the same formulas')],
                 exam=[short('ALE is $64,000 a year. A mitigation service cuts attacks to 80% of the original number and costs $1,000/month + $1,500 installation. What is the control’s value in year one?', 'ALE after = 64,000 × 0.8 = $51,200. Annual cost = 12 × 1,000 + 1,500 = $13,500. Value = 64,000 − 51,200 − 13,500 = −$700, so in the first year the control costs more than it saves.')], weight=3),
        23: dict(notes=['Cost–benefit analysis (CBA) is the BEST technique to decide whether a control is cost-effective.'],
                 past=[past('major', 'the technique for deciding if a control is cost-effective')],
                 exam=[mcq('The best technique to decide whether a control is cost-effective is:', ['Cost–benefit analysis', 'Penetration testing', 'Threat modeling', 'Brainstorming'], 0, '')], weight=3),
        24: dict(notes=['Qualitative: rate likelihood and impact (e.g. low/medium/high) and read the risk level from a matrix.'],
                 past=[past('major', 'decision-tree analysis')]),
        28: dict(notes=['The report: findings, risk ratings, recommended controls, residual risk; presented to management for decisions.']),
    }


class performing:
    AUTO_SLIDES = True
    DECK = deck('d06', 'Performing a Risk Assessment', 'Chapter 6',
                'Preparing for a risk assessment, the RA plan, identifying assets and activities, evaluating threats, '
                'vulnerabilities and countermeasures, writing mitigating recommendations, presenting the results and '
                'best practices.')
    ANN = {
        2: dict(notes=['Prepare: define scope and boundaries, get management support, identify stakeholders and data sources.']),
        7: dict(notes=['RA plan: the step-by-step list of what will be assessed, by whom, how and when.']),
        8: dict(notes=['Identify the assets and activities in scope (systems, data, processes) and who owns them.']),
        11: dict(notes=['Evaluate relevant threats: which threat sources could target each asset, and how likely they are.']),
        12: dict(notes=['Evaluate vulnerabilities: scans, audits, interviews, documentation reviews.']),
        13: dict(notes=['Evaluate existing countermeasures: what is in place and how effective it is.']),
        15: dict(notes=['Recommend mitigations: controls ranked by the risk they reduce and their cost.']),
        16: dict(notes=['Present the results to management, then track the agreed actions (implementation, monitoring, reassessment).'],
                 past=[past('major', 'two steps after finishing the risk assessment')],
                 exam=[short('Name two steps to do after finishing a risk assessment.', 'Present the results and recommendations to management for decisions; implement the approved controls (a mitigation plan with owners and deadlines); then monitor and reassess the risks periodically.')], weight=3),
        17: dict(notes=['Best practices: involve stakeholders, use a consistent method, document everything, repeat regularly.']),
    }


DECKS_HERE = [governance, fundamentals, threats, lifecycle, approaches, performing]

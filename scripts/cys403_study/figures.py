"""Slide diagrams shown inside the CYS403 breakdowns.

chapter -> [(slide page, crop box, section number, caption)]
The crop box is (left, top, right, bottom) as fractions of the slide; it keeps the
title and the university footer band out, and extract_cys403_figures.py trims the
white margin left over. Section numbers are 1-based positions in chNN.SECTIONS.

    python3 scripts/extract_cys403_figures.py      # render + crop into figures/
    python3 scripts/build_cys403_study_tools.py    # place them in the pages
"""

FIGURES = {
    1: [
        (5, (.55, .28, 1, .9), 1, "IT's business focus: business requirements drive IT resources and processes, which deliver the organisation's information (adapted from COBIT)."),
        (10, (.47, .22, 1, .9), 2, "Risk IT, Val IT and COBIT overlap: risk management, value management and IT process management meet around IT-related events."),
        (11, (.45, .22, .97, .9), 2, "Where IT risk fits in: existing frameworks were either generic enterprise-risk or IT-security oriented, leaving the gap Risk IT fills."),
        (13, (.02, .22, .98, .9), 3, "The business-driven security lifecycle: a security strategy that aligns with business needs."),
        (14, (.03, .03, .97, .9), 3, "IT security requirements structure: corporate governance at the top, security solutions at the base."),
        (17, (.55, .28, 1, .9), 4, "Cybersecurity management spans people, process and technology."),
        (18, (.38, .27, .98, .9), 4, "Strategic policies and frameworks feed the tactical guidelines, baselines and procedures."),
        (19, (0, .45, .98, .9), 4, "Governance (evaluate, direct, monitor) versus management (plan, build, run, monitor)."),
        (20, (0, .03, 1, .9), 4, "Where the CISO and CRO sit in the organisation chart."),
        (23, (.02, .2, .98, .9), 5, "The policy environment: regulations, laws, goals, objectives and shareholder interests shape the overarching policy."),
        (24, (.08, .25, .95, .9), 5, "Policy hierarchy: the overarching policy drives functional policies, carried out through standards, baselines, procedures and guidelines."),
        (26, (.6, .35, .95, .9), 6, "The four supporting documents: standards, procedures, baselines and guidelines."),
        (33, (.05, .22, .99, .9), 8, "Governance, risk and compliance as one continuous cycle."),
    ],
    2: [
        (7, (0, .2, .95, .9), 1, "Risk lives where threats meet the vulnerabilities in your assets."),
        (14, (.02, .2, .98, .9), 2, "A threat agent gives rise to a threat that exploits a vulnerability, creating risk to an asset that safeguards counter."),
        (15, (.02, .18, 1, .9), 2, "Risk management concept flow: owners, safeguards, vulnerabilities, threat agents, threats, risk and assets."),
        (11, (.6, .35, 1, .9), 3, "Controls filter risk down; whatever drips through is residual risk."),
        (21, (0, .15, 1, .9), 4, "The risk equation, and the activities under assessment, mitigation and evaluation."),
        (20, (.02, .02, .98, .9), 5, "The components of risk management: identification, assessment and control."),
        (46, (.05, .15, .95, .9), 6, "The risk management process: identify, assess, control, review."),
        (27, (0, .2, 1, .9), 6, "A sample risk register."),
        (32, (0, .2, 1, .9), 7, "Worked quantitative example: asset value and exposure factor give SLE, ARO gives ALE, then the control's cost/benefit."),
        (38, (.05, .05, .95, .9), 8, "Techniques used in qualitative and quantitative risk analysis."),
        (36, (.02, .2, 1, .9), 8, "AS/NZS 4360 risk levels: likelihood against consequence."),
        (39, (.1, .22, .95, .9), 8, "Quantitative versus qualitative risk analysis compared."),
    ],
    3: [
        (3, (.1, .05, .95, .9), 1, "Common types of attack against an organisation's systems."),
        (6, (.05, .12, 1, .9), 1, "The seven IT infrastructure domains threats can come from (Kim and Solomon)."),
        (7, (0, .15, 1, .9), 2, "Threats against the network, the host and the application."),
        (26, (.05, .2, .95, .9), 7, "STRIDE: the question each threat category asks."),
        (27, (.02, .2, .98, .9), 7, "Each STRIDE threat mapped to the security property it violates."),
        (29, (.1, .15, .95, .9), 8, "The seven stages of PASTA."),
        (30, (.4, .6, 1, .9), 8, "LINDDUN's six steps, from the problem space to the solution space."),
        (34, (.02, .2, .98, .9), 8, "CVSS v3.0 base score metrics."),
        (36, (.05, .3, .98, .9), 8, "Attack tree in graph notation: the goal \"read file\" decomposed into approaches."),
        (44, (.1, .05, .95, .9), 9, "Quantitative TMM: a component attack tree, then CVSS scores for its nodes."),
        (48, (.05, .15, .98, .9), 9, "The OCTAVE process in three phases."),
        (49, (.02, .2, .95, .9), 10, "The five DREAD rating questions."),
        (50, (.02, .14, .98, .9), 10, "DREAD scoring example: cookie theft by eavesdropping versus XSS."),
    ],
    4: [
        (6, (.58, .25, 1, .9), 1, "The risk management cycle."),
        (7, (.1, .18, .9, .9), 3, "Risk management action points: from threat source to acceptance or control."),
        (9, (.1, .19, .9, .9), 3, "The risk identification process, top to bottom."),
        (11, (.02, .2, .98, .9), 4, "IT system components mapped to risk management components."),
        (19, (.08, .05, .9, .9), 5, "An example classification of information assets."),
        (22, (.02, .22, .98, .9), 6, "Weighted criteria analysis for valuing assets."),
        (24, (.18, .4, .98, .9), 7, "Threats ranked by weighted score."),
        (25, (.05, .15, .9, .9), 7, "Vulnerability assessment: each threat with its possible vulnerabilities."),
        (27, (.05, .25, .95, .9), 7, "Summary of threat and vulnerability analysis."),
        (29, (.05, .2, .95, .9), 8, "The TVA worksheet: assets across the top, threats down the side."),
    ],
    5: [
        (25, (.02, .2, .98, .9), 6, "Probability and impact scales."),
        (26, (.05, .2, .98, .9), 6, "Probability versus impact matrix."),
        (27, (.1, .35, .95, .9), 6, "Qualitative survey results: risk level = probability x impact."),
        (36, (0, .2, 1, .9), 8, "A ranked risk worksheet."),
        (37, (0, .05, 1, .9), 8, "The deliverables of risk identification and what each is for."),
        (38, (.02, .05, .98, .9), 8, "Where the process stands: identification and assessment done, risk control next."),
    ],
    6: [
        (4, (.02, .2, .98, .9), 2, "Operational characteristics and system mission for an email server."),
        (14, (.1, .02, .9, .9), 8, "Control classes and their control families."),
    ],
}


def image_name(page: int) -> str:
    return f"slide-{page:02d}.webp"

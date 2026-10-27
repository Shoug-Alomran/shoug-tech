"""SE322 annotated slides — Chapter 8: Architecture Evaluation (ATAM and lightweight ATAM).
See ch01_introduction.py for AUTO_SLIDES and the ANN keys."""
from .common import mcq, past, scen, see, short, tf, tip, trap, trick

AUTO_SLIDES = 'all'
OVERVIEW = 'This chapter explains how to evaluate software architecture before construction. ATAM uses stakeholder goals and quality scenarios to reveal risks, sensitivity points, and trade-offs; lightweight ATAM adapts the evaluation process for smaller projects.'

DECK = {
    'key': 'ch8',
    'slug': '18-architecture-evaluation',
    'file': 'architecture-evaluation',
    'title': 'Architecture Evaluation',
    'chapter': 'Chapter 8',
    'page': 'ch08_page',  # notes, highlights and exam questions in the page schema
    'pdf': '/academics/software-engineering/se322/slides/chapter-8-architecture-evaluation/',
    'lede': ('Why architectures are evaluated before construction, the benefits, the methods (ATAM, SAAM…), and '
             'ATAM in full: participants, nine steps, utility tree, risks, sensitivity points and trade-offs, '
             'outputs, and the lightweight ATAM. Final 252 asked three questions straight from this deck.'),
}

STEPS = ('ATAM in 9 steps: 1 present ATAM · 2 present business drivers · 3 present the architecture · 4 identify architectural approaches · '
         '5 generate the quality attribute utility tree · 6 analyze approaches · 7 brainstorm and prioritize scenarios · 8 analyze approaches again · 9 present results.')

ANN = {
    1: dict(kind='title', title='Architecture and Design Evaluation', body=[], sub='SE322 · Chapter 8', tips=[tip(STEPS)]),
    2: dict(notes=['The lecture explains why architecture is evaluated, surveys evaluation methods, then studies ATAM and a lightweight version. The emphasis is on finding quality risks before construction makes change expensive.']),
    3: dict(notes=['Architecture is shaped by three drivers: functional requirements, non-functional requirements and business constraints.'],
            exam=[mcq('Which is NOT one of the three drivers that shape a software architecture?', ['The programming language syntax', 'Functional requirements', 'Non-functional requirements', 'Business constraints'], 0, '')], weight=2),
    4: dict(notes=['Evaluation asks whether the design can meet important quality goals before implementation makes change expensive. A review cannot prove perfection, but it can expose risky assumptions while they are still inexpensive to revise.'], seen=[see('ch2.1', 27, 'Evaluation as a key task')]),
    5: dict(notes=['Benefits: prioritizes conflicting goals, forces a clear explanation of the architecture, improves documentation, uncovers missing requirements, finds risks early, improves the architecture.'],
            past=[past('f252', 'Q8 · two benefits of architecture evaluation')],
            exam=[short('State two benefits of architecture evaluation. (Final 252)', 'It forces the architecture to be clearly explained and improves its documentation; it prioritizes conflicting goals; and it finds risks and problems early, when they are cheap to fix.')],
            weight=3),
    6: dict(notes=['Evaluation methods use scenarios to test design decisions against quality goals. A method is useful when it produces evidence—risks, trade-offs, or questions—not merely because the team completed a workshop.'],
            past=[past('f252', 'Q8 · the shared point of all evaluation methods')],
            exam=[short('What do all architecture evaluation methods have in common? (Final 252)', 'They all evaluate the architecture against its quality attribute requirements (and stakeholder concerns), typically by analysing scenarios.')],
            weight=3),
    7: dict(notes=['ATAM is a structured way to ask what architectural choices do to quality goals under stress. It helps stakeholders see consequences rather than treating each quality attribute as an isolated checklist.'],
            exam=[mcq('ATAM stands for:', ['Architecture Tradeoff Analysis Method', 'Architecture Testing and Analysis Model', 'Automated Trade Analysis Method', 'Architecture Template Assessment Method'], 0, '')], weight=3),
    8: dict(notes=['Security controls may add processing time; caching may improve speed but expose stale or sensitive data. ATAM surfaces these interactions so stakeholders can choose acceptable trade-offs.']),
    9: dict(notes=['Three groups of qualities: end-user (performance, availability, usability, security), technical (modifiability, portability, reusability, testability, interoperability), business (cost, time to market…).']),
    10: dict(notes=['Participants: evaluation team (3–5 experienced architects), project decision makers (manager, customer), architecture stakeholders.']),
    11: dict(notes=['The leader keeps the evaluation focused, the scribe preserves decisions and evidence, and questioners probe assumptions. Clear roles help the workshop produce analyzable findings rather than an unstructured discussion.']),
    12: dict(notes=['The first ATAM steps establish shared context: explain the method, understand business goals, present the architecture, identify approaches, build a prioritized utility tree, and analyze key scenarios.'], tips=[tip(STEPS)],
             exam=[mcq('In which ATAM step is the quality attribute utility tree generated?', ['Step 5', 'Step 2', 'Step 7', 'Step 9'], 0, '')], weight=3),
    13: dict(notes=['The later ATAM steps broaden participation: stakeholders add and prioritize scenarios, the team analyzes the highest priorities, then presents findings. This checks whether the initial architecture presentation missed important concerns.'], tips=[tip(STEPS)]),
    14: dict(notes=['The phases organize who participates and when. Early phases build the decision-makers’ shared understanding; later phases bring the wider stakeholder group into scenario generation and analysis.']),
    15: dict(notes=['The report should preserve reasoning, not just a verdict. Risks may prevent a quality goal; sensitivity points show where small parameter changes matter; trade-off points help one goal while hurting another.']),
    16: dict(kind='section', title='ATAM steps in more detail'),
    17: dict(notes=['Start by agreeing on what ATAM will do and what evidence it produces. This gives participants a shared process and prevents the workshop from being mistaken for a code review or a pass/fail certification.']),
    18: dict(notes=['Business drivers explain why the system exists, who matters, and which constraints are fixed. They are needed to judge whether an architectural trade-off is acceptable, not merely technically interesting.']),
    19: dict(notes=['The architecture presentation gives evaluators enough structure to reason about scenarios. Stakeholders should be able to trace a quality concern through the relevant components and deployment choices.'], seen=[see('ch2.3', 4, 'The 4+1 views')]),
    20: dict(notes=['Name the approaches actually used—such as layering, caching, or client-server—because these are the mechanisms whose consequences the team will analyze. Pattern labels alone are not findings.']),
    21: dict(notes=['The utility tree refines broad qualities into specific, prioritized scenarios. “Performance” becomes a measurable response under a stated load, and priorities show which scenarios deserve the deepest analysis.'],
             exam=[mcq('A utility tree organizes:', ['Quality attribute goals refined into prioritized scenarios', 'Classes by inheritance', 'Deployment nodes', 'Project tasks by date'], 0, '')], weight=3),
    22: dict(notes=['The utility-tree example shows how a broad goal is decomposed into scenarios with importance and difficulty ratings. Prioritization directs analysis effort toward scenarios that matter and may be hard to achieve.']), 23: dict(notes=['Compare the scenario priorities and ratings: a high-importance, high-difficulty case deserves early analysis. This is a practical way to allocate workshop time instead of attempting exhaustive proof.']),
    24: dict(notes=['For each important scenario, trace which decisions affect the response. A risk may prevent the goal; a sensitivity point strongly affects it; a trade-off point affects several goals at once.'],
             exam=[mcq('A decision that affects two quality attributes in opposite directions is recorded as a:', ['Trade-off', 'Non-risk', 'Business driver', 'Utility tree leaf'], 0, '')], weight=2),
    25: dict(notes=['The analysis form links a scenario to the architectural decisions that affect it and records risks, non-risks, sensitivity points, and trade-offs. This traceable evidence makes results actionable after the workshop.']),
    26: dict(notes=['Stakeholders propose realistic situations that stress the architecture, then prioritize them so evaluation time goes to the most important cases rather than every imaginable event.']),
    27: dict(notes=['Step 8 applies the same reasoning to scenarios raised by the broader stakeholder group. New concerns may reveal risks that were invisible when only the core decision-makers defined priorities.']),
    28: dict(notes=['Present results in terms stakeholders can act on: what is risky, which decisions caused the concern, and what options exist. The goal is informed design decisions, not simply a polished slide deck.']),
    29: dict(notes=['Lightweight ATAM shortens the workshop for a smaller, lower-risk project, but keeps the core reasoning: stakeholder goals, scenarios, design approaches, and recorded risks. Lightweight does not mean skipping evaluation.'],
             tips=[trap('Lightweight ATAM is shorter and internal; full ATAM is longer, with an external evaluation team.')],
             past=[past('f252', 'Q8 · ATAM vs. lightweight ATAM')],
             exam=[short('What is the main difference between ATAM and lightweight ATAM? (Final 252)', 'Lightweight ATAM is a reduced version for smaller, lower-risk projects: it can be done in a day or half a day and entirely by people inside the organisation, while full ATAM runs over several days with an external evaluation team and all stakeholders.')],
             weight=3),
    30: dict(notes=['A short agenda should still preserve the essential sequence: goals and architecture context, important scenarios, analysis, and recorded decisions. Compressing time is safest when the project scope and risk are modest.']),
    31: dict(notes=['Review the evaluation purpose, ATAM roles and steps, utility tree, and outputs. The method connects business goals and quality scenarios to concrete architectural risks and trade-offs.'], tips=[tip(STEPS)]),
}

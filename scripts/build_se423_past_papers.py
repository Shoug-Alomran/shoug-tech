#!/usr/bin/env python3
"""Build the SE423 past-paper exams (interactive, keyword graded).

Each paper becomes exams/<slug>/ with:
  <slug>-bank.js   window.PAPER (questions, marks, keys, model answers)
  <slug>.html      standalone page (se423.css + exams/past-paper.js engine)
  index.html       site wrapper, cloned from the midterm mock exam wrapper

Questions follow the original papers' order and marks. Keys come from the
instructor's key where one exists (Midterm 251); the rest are model answers
written from the course slides. Run: python3 scripts/build_se423_past_papers.py
then rebuild the sidebar (scripts/build_academic_sidebar.py).
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMS = ROOT / "docs/academics/software-engineering/se423/exams"
BASE = "/academics/software-engineering/se423/exams/"
SITE = "https://shoug-tech.com"


def e(s):
    return html.escape(s, quote=False)


def mcq(q, opts, a, why="", c=""):
    return {"type": "mcq", "q": q, "opts": opts, "a": a, "why": why, "pts": 0.5, "c": c}


def short(q, pts, groups, model, c=""):
    return {"type": "short", "q": q, "pts": pts, "groups": groups, "model": model, "c": c}


# ---------------------------------------------------------------- shared bits
RACI_ROLES = ["Project Manager (PM)", "Lead Developer", "UI/UX Designer", "QA Engineer", "Client Representative", "Marketing Specialist"]
RACI_TASKS = ["T1. Define app requirements", "T2. Design user interface", "T3. Develop core features", "T4. Test the application", "T5. Launch the app", "T6. Promote the app"]
RACI_KEY = {
    0: ["A", "C", "C", "I", "R", "I"],
    1: ["I", "C", "R", "I", "C", "I"],
    2: ["I", "R", "C", "I", "I", "I"],
    3: ["I", "C", "I", "R", "I", "I"],
    4: ["A", "R", "I", "C", "C", "C"],
    5: ["I", "I", "C", "I", "C", "R"],
}


def raci(rows):
    names = " and ".join(RACI_TASKS[r].split(". ")[0] for r in rows)
    return {
        "type": "raci", "pts": 1.5, "c": "RACI matrix",
        "q": "Your team has been assigned to develop a mobile app for a local fitness center. The app will allow users to book classes, track workouts, and receive personalized fitness tips. The project is expected to be completed in 8 weeks. Fill in the RACI assignments for " + names + " only. Assign one or more roles to each task: R = Responsible (does the work), A = Accountable (owns the outcome), C = Consulted (provides input), I = Informed (kept updated).",
        "roles": RACI_ROLES, "tasks": RACI_TASKS, "graded": rows, "key": {str(k): v for k, v in RACI_KEY.items()},
        "model": "These cells come from the instructor's key. The person who does the work is R (the client representative for requirements, the UI/UX designer for the interface, the lead developer for building and launching, the marketing specialist for promotion). Whoever's expertise is needed is C, and everyone else is I. The key makes the PM Accountable (A) for requirements and launch, the two tasks that commit the project; on the other tasks the PM is kept Informed.",
    }


def mid_mcqs():
    return {
        "domains": mcq("Which of the following best explains the nature of project performance domains?", ["They represent distinct areas of focus that guide effective project management.", "They are rigid processes that must be followed in order, from initiation to closure.", "They are optional tools that project managers may use only in large projects.", "They are specific deliverables required at the end of each project phase."], 0, "Performance domains are groups of related activities (areas of focus) that run concurrently; they are not sequential processes or deliverables.", "Performance domains"),
        "decentral": mcq("In decentralized project management, decision-making authority is primarily:", ["Distributed among team members to encourage shared accountability.", "Concentrated in the hands of a single project manager.", "Transferred to external auditors for oversight.", "Reserved exclusively for senior executives in the organization."], 0, "Decentralized management spreads decisions across the team; centralized puts them with one person such as the PM.", "Centralized vs decentralized"),
        "program_v1": mcq("A group of related projects managed in a coordinated manner to obtain benefits not available from managing them individually is called a:", ["Program", "Portfolio", "Project", "Value stream"], 0, "A program is related projects managed together for benefits; a portfolio groups projects, programs and operations for strategic objectives and they can be unrelated.", "Project vs program vs portfolio"),
        "program_v2": mcq("A group of related projects managed in a coordinated manner to obtain benefits not available from managing them individually is called a:", ["Portfolio", "Program", "Project", "Value stream"], 1, "A program is related projects managed together for benefits; a portfolio groups projects, programs and operations for strategic objectives and they can be unrelated.", "Project vs program vs portfolio"),
        "steward": mcq("Which of the following best reflects the principle of “Stewardship” in project management?", ["Delegating all responsibility for ethical practices to external auditors", "Taking personal responsibility for the careful use of resources, upholding values, and acting with integrity.", "Focusing only on delivering project outputs, regardless of long-term impacts.", "Ensuring accountability is limited to the project sponsor alone."], 1, "Stewardship means acting with integrity, care, trustworthiness and compliance, inside and outside the organization.", "PM principles"),
        "cadence": mcq("In project management, what is the primary purpose of establishing a project cadence?", ["To create a predictable rhythm that supports coordination, communication, and timely delivery.", "To enforce strict deadlines that cannot be adjusted under any circumstances.", "To eliminate the need for stakeholder engagement during development.", "To ensure that all deliverables are produced only at the end of the project."], 0, "Cadence is the rhythm of activities (single, multiple, periodic or continuous delivery) that keeps the work coordinated.", "Delivery cadence"),
        "iterative": mcq("In which type of project would an iterative development approach be most beneficial?", ["A project where requirements are unclear and expected to evolve over time.", "A project with well-defined, unchanging requirements from the start.", "A project that must deliver the entire product only at final completion.", "A project that cannot accommodate stakeholder feedback during execution."], 0, "Iterative development refines ideas through feedback, which suits unclear or evolving requirements.", "Development approaches"),
        "tuck_v1": mcq("According to Tuckman’s model of team development, which stage is characterized by members competing for leadership and struggling with group processes?", ["Storming", "Norming", "Adjourning", "Performing"], 0, "Storming is when members compete for leadership and test group processes; norming comes after, when agreement is reached.", "Tuckman stages"),
        "tuck_v2": mcq("According to Tuckman’s model of team development, which stage is characterized by members competing for leadership and struggling with group processes?", ["Storming", "Forming", "Norming", "Performing"], 0, "Storming is when members compete for leadership and test group processes; forming is only getting to know each other.", "Tuckman stages"),
        "trust": mcq("Which of the following is considered the foundation of teamwork?", ["Accountability", "Trust", "Commitment", "Consensus"], 1, "Trust is the base of the team pyramid: trust, managed conflict, commitment, accountability, results.", "Team pyramid"),
        "cohesive": mcq("In a cohesive team, which of the following is an advantage?", ["Members avoid challenging each other’s work to reduce conflict.", "Group quality standards can be developed and maintained collectively.", "Each member works independently without needing oversight.", "Decision-making is always faster due to consensus."], 1, "Cohesive groups can set and keep shared quality standards, learn from each other and practise egoless programming. Avoiding challenge is groupthink, a risk of cohesion.", "Group cohesiveness"),
        "value": mcq("In the context of the “system for value delivery,” which of the following is the most accurate statement?", ["Only portfolios and programs contribute to value delivery in an organization, while projects and products have no significant role.", "A system for value delivery includes portfolios, programs, projects, products, and operations, all working together to build, sustain, or advance an organization.", "Value delivery systems are only relevant to large organizations and do not apply to small businesses.", "Products are the sole contributor to value delivery, with programs and projects serving as support."], 1, "The value delivery system is the whole set of portfolios, programs, projects, products and operations working together.", "System for value delivery"),
    }


MID_SHORT = {
    "good": short("What are key characteristics of a good team?", 0.75, [
        ["Trust and open, honest communication", ["trust", "open", "honest", "communicat"]],
        ["A clear, shared goal and clear roles", ["goal", "purpose", "objective", "vision", "role"]],
        ["Healthy conflict, commitment, accountability and a focus on results", ["conflict", "commit", "accountab", "result", "collaborat", "cooperat"]],
    ], "A good team trusts each other enough to speak openly and admit mistakes, shares a clear goal with clear roles, debates ideas in healthy conflict, commits to decisions, holds each other accountable, and puts team results ahead of individual credit.", "Characteristics of a good team"),
    "vuln": short("What does vulnerability-based trust involve?", 0.75, [
        ["Admitting mistakes and weaknesses", ["mistake", "weakness", "admit", "wrong", "error"]],
        ["Asking for help or saying “I don't know”", ["help", "dont know", "not know", "ask"]],
        ["Without fear of being judged or punished (feeling safe)", ["fear", "safe", "comfortable", "judg", "embarrass", "punish"]],
    ], "Team members are comfortable being open with each other: admitting mistakes and weaknesses, asking for help, and saying “I don't know”, without fear that it will be used against them. It is the foundation of the team pyramid.", "Building trust"),
    "acct": short("What’s the best time to reinforce accountability?", 0.75, [
        ["Early: set clear, public expectations from the start", ["start", "early", "begin", "expectation", "clear"]],
        ["Immediately when a commitment is missed, not at the end", ["immediate", "right away", "as soon", "when it happens", "missed", "promptly"]],
        ["Continuously through regular reviews, peers holding each other accountable", ["regular", "review", "continu", "ongoing", "peer"]],
    ], "As early and as often as possible: make expectations and commitments clear and public at the start, then address a missed commitment immediately when it happens instead of waiting for the end-of-project review, and keep reinforcing it in regular progress reviews where peers hold each other accountable.", "Accountability"),
    "conflict": short("Why is healthy conflict important in teams?", 0.75, [
        ["Different ideas are debated, leading to better decisions", ["better decision", "decision", "idea", "solution", "perspective", "debate"]],
        ["Avoids groupthink and artificial harmony; problems surface early", ["groupthink", "harmony", "problem", "early", "risk", "surface"]],
        ["Members feel heard, so they commit (buy-in)", ["commit", "buy in", "heard", "trust"]],
    ], "Healthy conflict is open debate about ideas, not people. It brings out different perspectives so the team makes better decisions, avoids groupthink and artificial harmony, and surfaces problems early. Because everyone has been heard, members are more willing to commit to the final decision even if they disagreed.", "Healthy conflict"),
    "bizdem": short("What’s the difference between a Business Team and a Democratic Team?", 0.75, [
        ["Business team: a technical lead with members of equal status under the lead (hierarchy)", ["technical lead", "lead", "hierarch", "equal status", "leader decides"]],
        ["Democratic team: the group decides by consensus", ["consensus", "group decid", "together", "democrat", "vote", "agree"]],
        ["Democratic: leader is only the external interface; tasks by ability; needs experienced members", ["external", "interface", "ability", "experience", "self organiz"]],
    ], "A business team has a technical lead who is the principal contact and makes or facilitates decisions, with the other members at equal status under the lead (a strong or loose hierarchy). A democratic team acts as a group: decisions are made by consensus, the leader is only the external interface, tasks are allocated by ability and experience, and it works best with experienced, competent members.", "Business vs democratic team"),
    "lead": short("How can a project manager balance technical leadership with adaptive leadership in a software team?", 0.5, [
        ["Technical leadership: known problems solved by expertise and best practices, leader's vision", ["known", "best practice", "expert", "vision", "technical"]],
        ["Adaptive leadership: new problems with no known solution, team learns and experiments, sense of purpose", ["unknown", "new problem", "learn", "experiment", "purpose", "adaptive", "no known"]],
        ["Balance: diagnose the problem type and switch style; involve and empower the team", ["diagnos", "depend", "situation", "switch", "both", "empower", "involve", "balance"]],
    ], "First diagnose the problem. When it can be solved by known means (a coding standard, an architecture choice the PM knows well), use technical leadership: give direction from expertise and vision. When it can't (new technology, unclear requirements), use adaptive leadership: frame the purpose, ask questions, let the team experiment and learn, and motivate through visible progress. Switching between the two as the situation changes is the balance.", "Technical vs adaptive leadership"),
}

CASE_EDUGATE = (
    "<h4>Case study: Edugate Integrated Mobile Scheduling Assistant</h4>"
    "<p>Prince Sultan University (PSU) plans to introduce a new <b>mobile application service</b> integrated with the existing <b>Edugate system</b>. The purpose is to allow students to <b>proactively design their preferred schedules early</b>, before official course registration opens.</p>"
    "<p><b>Key requirements</b></p><ul>"
    "<li>The app must allow students to create <b>draft schedules</b> with preferred timings, instructors, and free periods.</li>"
    "<li>All schedules must comply with <b>PSU study plan rules</b> (course load limits, prerequisites, track requirements).</li>"
    "<li>The app must <b>sync automatically with Edugate</b> so that official registration offerings match students’ pre-designed schedules.</li>"
    "<li>Advisors must be able to <b>view and comment</b> on student schedules before registration.</li>"
    "<li>The system must provide a <b>bilingual interface (Arabic/English)</b>.</li>"
    "<li>Security and compliance with PSU’s IT policies must be ensured during integration.</li></ul>"
    "<p><b>Challenges</b></p><ul>"
    "<li>During sprint deployment, a critical feature was discovered to be <b>not properly tested</b>.</li>"
    "<li><b>Faculty advisors</b> request complex features (early alerts for overloaded students, GPA-based recommendations), creating scope creep.</li>"
    "<li><b>Students</b> prioritize flexibility and ease of use, while administrators prioritize strict enforcement of PSU study plan rules.</li>"
    "<li>The project requires a <b>clear team structure</b> to balance technical, academic, and administrative needs.</li></ul>"
)

EDUGATE_QS = [
    short("During a sprint deployment, a key feature was discovered to be not thoroughly tested and caused issues after release. As the project manager, what steps would you follow to address this issue and ensure accountability within the team?", 1.5, [
        ["RACI matrix: identify who was Responsible, Accountable, Consulted and Informed for testing (0.5)", ["raci", "responsible", "accountable"], 2],
        ["Investigation: hold a retrospective to find the root cause (0.25)", ["retrospective", "root cause", "investigat", "analy"]],
        ["Accountability: make responsible roles clear without blame (0.25)", ["blame", "without blam", "no blame", "clear role", "ownership"]],
        ["Corrective action: hotfix, redistribute tasks, add automated testing (0.25)", ["hotfix", "fix", "automated test", "redistribut", "reassign", "rollback", "roll back"]],
        ["Communication: inform stakeholders of the recovery plan (0.25)", ["inform", "stakeholder", "communicat", "recovery plan"]],
    ], "Use a RACI matrix to establish who was Responsible, Accountable, Consulted and Informed for testing that feature (0.5). Hold a retrospective to find the root cause (0.25). Make the responsible roles clear without blaming individuals (0.25). Take corrective action: release a hotfix, redistribute tasks, and add automated testing so it can't recur (0.25). Inform the stakeholders of the recovery plan (0.25).", "Accountability and RACI"),
    short("Given the evolving requirements (student usability, advisor requests, IT integration rules), which development approach (Agile, Waterfall, or Hybrid) would you recommend, and why would it be the best fit for this project?", 1, [
        ["Agile (Scrum) chosen (0.5)", ["agile", "scrum"]],
        ["Justification: handles evolving requirements, iterative delivery, integrates with DevOps pipelines (0.5)", ["evolv", "chang", "iterat", "feedback", "sprint", "devops", "increment"]],
    ], "Agile (Scrum) (0.5), because it handles the evolving requirements from students, advisors and IT, delivers iteratively so each sprint gets feedback, and integrates with DevOps pipelines for frequent tested releases (0.5).", "Development approaches"),
    short("Identify three main stakeholder groups for this project, describe their roles, and explain how their input will shape the system.", 1, [
        ["Students: end users, influence usability (0.3)", ["student"], 3],
        ["IT / Edugate team: ensure integration and compliance (0.3)", ["it ", "edugate", "it team", "integration", "technical"], 3],
        ["Faculty advisors / administration: ensure policy enforcement and monitoring (0.4)", ["advisor", "faculty", "admin", "registrar"], 4],
    ], "Students are the end users; their input shapes usability and flexibility (0.3). The IT/Edugate team ensures integration, security and compliance with PSU IT policies (0.3). Faculty advisors and administration ensure study-plan rules are enforced and use the system to monitor students (0.4).", "Stakeholder identification"),
    short("As the project manager, you must establish the team structure for this project. What team structure would you create to ensure smooth development, stakeholder engagement, and integration with Edugate, and why?", 1.5, [
        ["Roles: PM, Product Owner (Edugate/IT rep), developers, UI/UX designer, QA/testers, faculty advisor rep, student rep (1.0)", ["product owner", "developer", "ui", "ux", "designer", "qa", "tester"], 2],
        ["Includes stakeholder representatives (advisor and student reps)", ["advisor rep", "student rep", "representative", "faculty"], 1],
        ["Rationale: cross-functional Agile team, stakeholder voices, balances usability vs compliance, iterative delivery (0.5)", ["cross functional", "agile", "balance", "iterative", "voice"], 1.5],
    ], "A cross-functional Agile team: a Project Manager, a Product Owner from Edugate/IT, developers, a UI/UX designer, QA testers, a faculty advisor representative and a student representative (1.0). This puts every stakeholder's voice inside the team, balances usability against compliance, and supports iterative delivery (0.5).", "Team structure"),
]


def midterm(version):
    m = mid_mcqs()
    if version == 1:
        order = ["decentral", "program_v1", "domains", "cadence", "steward", "iterative", "tuck_v1", "trust", "value", "cohesive"]
        shorts = [MID_SHORT[k] for k in ["good", "vuln", "conflict", "bizdem", "lead"]] + [raci([0, 5])]
    else:
        order = ["domains", "decentral", "program_v2", "steward", "cadence", "iterative", "tuck_v2", "trust", "cohesive", "value"]
        shorts = [MID_SHORT[k] for k in ["vuln", "acct", "conflict", "bizdem", "lead"]] + [raci([1, 4])]
    return [
        {"title": "Part 1 · MCQs", "items": [m[k] for k in order]},
        {"title": "Part 2 · Short questions", "items": shorts},
        {"title": "Part 3 · Case study", "intro": CASE_EDUGATE, "items": EDUGATE_QS},
    ]


# ---------------------------------------------------------------- network diagrams
def network_svg(nodes, edges, crit, w, h):
    """nodes: name -> (x, y, duration). Activity-on-node boxes; critical edges in accent."""
    out = [f'<svg class="net" viewBox="0 0 {w} {h}" role="img" aria-label="Network diagram">',
           '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>']
    bw, bh = 64, 40
    for a, b in edges:
        x1, y1, _ = nodes[a]
        x2, y2, _ = nodes[b]
        c = "crit" if a in crit and b in crit else ""
        out.append(f'<line class="{c}" x1="{x1 + bw / 2}" y1="{y1}" x2="{x2 - bw / 2 - 2}" y2="{y2}" marker-end="url(#ah)"/>')
    for n, (x, y, d) in nodes.items():
        c = "crit" if n in crit else ""
        out.append(f'<g class="node {c}"><rect x="{x - bw / 2}" y="{y - bh / 2}" width="{bw}" height="{bh}" rx="8"/>'
                   f'<text x="{x}" y="{y - 2}">{n}</text>' + (f'<text class="d" x="{x}" y="{y + 13}">{d}</text>' if d != "" else "") + "</g>")
    out.append("</svg>")
    return "".join(out)


def table(head, rows):
    return ('<div class="tbl-scroll"><table class="grid-tbl given"><thead><tr>' + "".join(f"<th>{e(h)}</th>" for h in head) +
            "</tr></thead><tbody>" + "".join("<tr>" + "".join(f"<td>{e(str(c))}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")


# Final 242 network
F242_ACTS = [("A", "-----", 5), ("B", "A", 5), ("C", "A", 7), ("D", "A", 9), ("E", "B, D", 3), ("F", "E", 5), ("G", "F", 2), ("H", "C, G", 2)]
F242_NET = network_svg(
    {"Start": (40, 110, ""), "A": (130, 110, 5), "B": (240, 50, 5), "D": (240, 130, 9), "C": (240, 205, 7), "E": (350, 90, 3), "F": (450, 90, 5), "G": (550, 90, 2), "H": (650, 150, 2), "End": (750, 150, "")},
    [("Start", "A"), ("A", "B"), ("A", "D"), ("A", "C"), ("B", "E"), ("D", "E"), ("E", "F"), ("F", "G"), ("G", "H"), ("C", "H"), ("H", "End")],
    {"Start", "A", "D", "E", "F", "G", "H", "End"}, 800, 240)

# Final 251 network
F251_ACTS = [("A", 6, "Start"), ("B", 9, "A"), ("C", 3, "B"), ("D", 4, "A"), ("E", 5, "C"), ("F", 7, "C"), ("G", 6, "D,E"), ("H", 12, "F"), ("I", 6, "G"), ("J", 7, "H,I")]
F251_NET = network_svg(
    {"Start": (40, 120, ""), "A": (125, 120, 6), "B": (215, 70, 9), "C": (305, 70, 3), "F": (400, 30, 7), "E": (400, 120, 5), "D": (305, 205, 4), "H": (500, 30, 12), "G": (500, 160, 6), "I": (600, 160, 6), "J": (700, 95, 7), "End": (790, 95, "")},
    [("Start", "A"), ("A", "B"), ("A", "D"), ("B", "C"), ("C", "E"), ("C", "F"), ("D", "G"), ("E", "G"), ("F", "H"), ("G", "I"), ("H", "J"), ("I", "J"), ("J", "End")],
    {"Start", "A", "B", "C", "F", "H", "J", "End"}, 840, 240)


def final242():
    q1 = [
        short("Define the term ‘project constraints’ and explain how they influence project planning and execution. Provide at least three examples of common constraints and discuss their interrelationship.", 2, [
            ["Definition: limits or restrictions the project must work within", ["limit", "restrict", "boundar", "constrain"]],
            ["Three examples: scope, time/schedule, cost/budget (also quality, resources, risk)", ["scope", "time", "schedule", "cost", "budget"]],
            ["Influence: planning and decisions must balance them (trade-offs)", ["plan", "trade off", "tradeoff", "balance", "decision"]],
            ["Interrelationship: changing one affects the others (triple constraint)", ["affect", "impact", "triangle", "triple", "increase", "reduce", "change one"]],
        ], "Project constraints are the limits a project must be delivered within. The classic three are scope, time and cost, often with quality, resources and risk. They drive planning because every schedule, budget and scope decision has to fit inside them, and during execution the PM keeps trading them off. They are interrelated (the triple constraint): cutting the schedule usually needs more cost or less scope, and adding scope needs more time or money; quality sits in the middle and suffers if they are squeezed.", "Project constraints"),
        short("Explain what is a Gantt chart and describe its significance in planning and tracking project activities. In your answer, define the terms milestone and dependency, and provide one example of each as they would appear in a Gantt chart.", 2.5, [
            ["Gantt chart: bar chart of activities against a time scale (start, finish, duration)", ["bar", "timeline", "time scale", "calendar", "start", "duration"]],
            ["Significance: plan the sequence and track actual vs planned progress", ["track", "progress", "plan", "actual", "monitor", "visual"]],
            ["Milestone: a significant event with zero duration (diamond)", ["milestone", "zero", "event", "diamond", "checkpoint"]],
            ["Dependency: a task that can't start or finish until another one does (arrow, finish-to-start)", ["depend", "finish to start", "predecessor", "cannot start", "arrow", "link"]],
            ["Concrete example of each", ["sign off", "approved", "approval", "release", "launch", "coding", "testing", "design"]],
        ], "A Gantt chart is a bar chart with activities down the side and a time scale across, where each bar shows an activity's start, finish and duration. It makes the schedule easy to read for planning (sequence, overlaps, who works when) and for tracking, because actual progress is shaded against the planned bars. A milestone is a significant point or event with zero duration, shown as a diamond, e.g. “Requirements signed off”. A dependency is a logical relationship where one activity can't start (or finish) until another does, shown as an arrow, e.g. “Coding” can't start until “Design approved” finishes (finish-to-start).", "Gantt charts"),
        short("What is a Project Management Office (PMO) and its role in organizations?", 1.5, [
            ["A centralized unit / department that oversees project management", ["central", "unit", "department", "office", "oversee"]],
            ["Role: standards, methods, templates and training", ["standard", "method", "template", "training", "best practice", "process"]],
            ["Role: support, monitor and report on projects; may manage them (supportive, controlling, directive)", ["support", "monitor", "report", "control", "direct", "track"]],
        ], "A PMO is a centralized organizational unit that oversees and standardizes how projects are managed. It sets PM standards, methods and templates, trains and supports project managers, monitors and reports on project performance, and coordinates resources across projects. Its control ranges from supportive (consultative) to controlling (requires compliance) to directive (manages the projects directly).", "PMO"),
    ]
    case2 = ("<h4>Solar-Tech Innovations</h4><p>You are managing a project for Solar-Tech Innovations, a company focused on renewable energy solutions. Your task is to oversee the development of a smart solar panel system that will incorporate energy storage, monitoring capabilities, and advanced efficiency features. The project timeline is <b>12 months</b>, with a team of <b>eight</b> engineers, <b>four</b> hardware specialists, and <b>two</b> software developers. Initial research has been completed, but extensive design, prototyping, testing, and regulatory approvals are still required. Your goal is to deliver the project within the budget, meet performance targets, and ensure timely delivery while managing risks and engaging with stakeholders.</p>")
    q2 = [
        short("As the project manager, you must ensure that the 12-month development timeline is realistic and achievable. Identify three project scheduling methods/techniques you would use to plan the sequence and timing of tasks. Briefly explain how each method helps in identifying delays or managing overlapping activities.", 2, [
            ["Critical Path Method (CPM): longest path, zero-slack activities", ["critical path", "cpm"]],
            ["Gantt chart: shows timing and overlaps visually", ["gantt"]],
            ["PERT / network diagram: dependencies and three-point durations", ["pert", "network", "three point"]],
            ["How they help: slack/float shows which delays matter; overlaps and dependencies are visible", ["slack", "float", "delay", "overlap", "depend"]],
        ], "1) Network diagram + Critical Path Method: shows dependencies and the longest path; any delay on a zero-slack critical activity delays the whole project, while slack shows how much other tasks can slip. 2) Gantt chart: shows each task on a timeline, so overlapping activities, resource clashes and slipping bars (actual vs planned) are easy to spot. 3) PERT: uses optimistic, most-likely and pessimistic durations ((O + 4M + P) / 6), useful for uncertain design, prototyping and regulatory work, so likely delays are built in.", "Scheduling techniques"),
        short("To plan accurately for the design, prototyping, and testing phases, you need to estimate the time and effort required. Choose two effort estimation techniques you would apply to this project. Explain how each technique supports better planning and risk control in this scenario.", 2, [
            ["Names two techniques (e.g. three-point/PERT, Delphi/expert judgment, analogous, bottom-up, COCOMO, function points)", ["three point", "pert", "delphi", "expert", "analog", "bottom up", "cocomo", "function point", "parametric", "wideband"], 2],
            ["How it improves planning: ranges, historical data or task-level detail", ["range", "optimistic", "pessimistic", "historical", "past", "detail", "wbs", "breakdown"]],
            ["Risk control: captures uncertainty, adds contingency, cross-checks estimates", ["risk", "uncertain", "contingency", "buffer", "valid", "compare", "cross check"]],
        ], "Three-point (PERT) estimation: each design, prototyping and test activity gets optimistic, most-likely and pessimistic values, (O + 4M + P) / 6, so the plan reflects the uncertainty of hardware prototyping and the spread shows where contingency is needed. Delphi / expert judgment: hardware and software experts estimate anonymously and converge over rounds, which brings in experience with regulatory testing and removes single-person bias. Comparing the two estimates cross-checks them and exposes risky tasks early.", "Estimation techniques"),
        short("You are responsible for managing a diverse team with varying availability and skill sets. Describe two strategies you would use to allocate your team’s resources efficiently across tasks. How would you adjust your resource plan if one hardware specialist becomes unavailable for 4 weeks?", 2, [
            ["Strategy: match tasks to skills and availability (skills matrix / RAM / RACI)", ["skill", "matrix", "ram", "raci", "availab", "expertise"]],
            ["Strategy: resource leveling / smoothing or histograms to avoid overallocation", ["level", "smooth", "histogram", "overallocat", "balance", "workload"]],
            ["Adjustment: use slack to delay non-critical work, reassign or cross-train, bring in a contractor", ["slack", "float", "non critical", "reassign", "cross train", "contract", "temporary", "reschedul"]],
            ["Update the schedule and inform stakeholders", ["update", "inform", "communicat", "stakeholder", "schedule"]],
        ], "1) Use a skills matrix and RAM to assign work by skill and availability, so specialists only do work that needs them. 2) Use resource leveling (and a resource histogram) to remove overallocation, shifting non-critical tasks within their slack. If a hardware specialist is out for 4 weeks: move their non-critical tasks inside their float, give critical tasks to the other three specialists (cross-training if needed) or bring in a temporary contractor, then update the schedule and tell the stakeholders the impact.", "Resource allocation"),
        {"type": "num", "pts": 2, "c": "COCOMO", "q": "You are estimating the effort required to develop the monitoring software for the smart solar panel system. Based on the COCOMO model for an Organic project: size 32 KLOC; a = 2.4, b = 1.05, c = 2.5, d = 0.38. Calculate the estimated effort in person-months, development time and average staff size for the project.",
         "fields": [{"label": "Effort E", "a": 91.33, "tol": 0.6, "unit": "person-months"}, {"label": "Development time TDEV", "a": 13.9, "tol": 0.2, "unit": "months"}, {"label": "Average staff size", "a": 6.57, "tol": 0.15, "unit": "people"}],
         "model": "E = a × KLOC^b = 2.4 × 32^1.05 = 2.4 × 38.05 ≈ 91.33 person-months. TDEV = c × E^d = 2.5 × 91.33^0.38 ≈ 2.5 × 5.56 ≈ 13.90 months. Staff = E ÷ TDEV = 91.33 ÷ 13.90 ≈ 6.57, about 7 people."},
        short("As the project manager for the smart solar panel system, you’re expected to manage risks proactively throughout the 12-month development cycle. Describe two techniques you would use during the planning phase to identify and document project risks. Explain how a Risk Assessment Matrix helps in making informed decisions about which risks need immediate action.", 2, [
            ["Two identification techniques (brainstorming, Delphi, checklists, interviews, SWOT, assumption analysis)", ["brainstorm", "delphi", "checklist", "interview", "swot", "assumption", "expert", "root cause", "historical"], 2],
            ["Documented in a risk register", ["register", "document", "log"]],
            ["Matrix: rates probability against impact", ["probability", "likelihood", "impact"]],
            ["High-probability, high-impact risks get immediate action (prioritization)", ["priorit", "high", "immediate", "red", "rank", "score"]],
        ], "Brainstorming with engineers, hardware specialists and developers, and expert interviews / Delphi with people who have done regulatory approvals, both recorded in a risk register (risk, cause, owner, response). A checklist from past projects also works. The Risk Assessment Matrix plots each risk's probability against its impact; the score ranks the risks, so high-probability, high-impact (red) risks get immediate responses and owners, medium ones are planned for, and low ones are just monitored.", "Risk identification and assessment"),
    ]
    q3 = [
        short("How does the stakeholder management process contribute to the success of a project? Identify two inputs, techniques and outputs of the stakeholder management process, and explain their role in ensuring effective stakeholder management.", 3, [
            ["Contribution: identifies and engages stakeholders, gaining support and reducing resistance and surprises", ["support", "resist", "expectation", "engag", "satisf", "align"]],
            ["Inputs (project charter, procurement documents, EEFs, OPAs, stakeholder register, communication plan)", ["charter", "procurement", "environmental", "process asset", "communication plan"]],
            ["Techniques (stakeholder analysis, power/interest grid, salience model, expert judgment, meetings, interpersonal skills)", ["analysis", "power", "interest", "grid", "salience", "expert judgment", "meeting", "interpersonal"]],
            ["Outputs (stakeholder register, engagement plan, change requests, issue log)", ["register", "engagement plan", "management plan", "change request", "issue log"]],
        ], "Stakeholder management identifies everyone affected, understands their interests and influence, and keeps them engaged, so the project gains support, catches conflicting expectations early and avoids late resistance. Inputs: the project charter (who sponsors and is affected) and enterprise environmental factors / organizational process assets (culture, past registers). Techniques: stakeholder analysis with a power/interest grid or salience model (prioritize who needs the most attention) and meetings with interpersonal skills (build relationships). Outputs: the stakeholder register (who they are, their interest, influence and engagement level) and the stakeholder engagement plan (how each one will be engaged and communicated with).", "Stakeholder management process"),
        {"type": "num", "pts": 1, "c": "Communication channels", "q": "Calculate the number of communication channels for a project team of 7 members.",
         "fields": [{"label": "Channels", "a": 21, "tol": 0}], "model": "n(n − 1) / 2 = 7 × 6 / 2 = 21 channels."},
        {"type": "rows", "pts": 3, "c": "Stakeholder engagement levels", "head": ["Engagement level", "Characteristics and best-suited communication method"],
         "q": "Compare stakeholder engagement levels in the context of their influence and impact on the project. Fill in the table with appropriate characteristics and explain the best-suited communication method in terms of Pull, Push, or Interactive communication.",
         "rows": [
             {"label": "Unaware", "groups": [["Not aware of the project or its impact", ["not aware", "unaware", "dont know", "doesnt know", "no knowledge"]], ["Push communication to create awareness (emails, memos, newsletters)", ["push", "email", "memo", "newsletter", "announce"]]],
              "model": "Doesn't know about the project or how it affects them. Push communication (emails, memos, announcements) to make them aware."},
             {"label": "Resistant", "groups": [["Aware but opposes the project or change", ["resist", "oppos", "against", "negative"]], ["Interactive communication to address concerns (meetings, one-to-one)", ["interactive", "meeting", "one to one", "discussion", "dialogue", "face"]]],
              "model": "Aware of the project and its impact but resists it. Interactive communication (meetings, one-to-one conversations) to listen to and address their concerns."},
             {"label": "Leading", "groups": [["Aware and actively engaged in making the project succeed", ["active", "champion", "engaged", "ensure success", "support", "lead"]], ["Interactive communication to keep them involved in decisions", ["interactive", "meeting", "collaborat", "workshop", "involv"]]],
              "model": "Aware of the project and actively engaged in ensuring it succeeds. Interactive communication (collaborative meetings, workshops) to keep them involved in decisions; push reports keep them updated."},
         ]},
    ]
    q4 = [
        {"type": "self", "pts": 2, "c": "Network diagrams", "q": "Produce a network diagram using the data provided in the table.",
         "model": "Activity-on-node, durations under each letter; the critical path is highlighted." + F242_NET},
        {"type": "cpm", "pts": 3, "c": "Critical path: ES, EF, LS, LF, slack", "q": "Identify and fill in the table: Early Start (ES), Early Finish (EF), Late Start (LS) and Late Finish (LF) time of each activity. Calculate slack time.",
         "acts": list("ABCDEFGH"), "cols": ["ES", "EF", "LS", "LF", "Slack"],
         "key": {"A": [0, 5, 0, 5, 0], "B": [5, 10, 9, 14, 4], "C": [5, 12, 17, 24, 12], "D": [5, 14, 5, 14, 0], "E": [14, 17, 14, 17, 0], "F": [17, 22, 17, 22, 0], "G": [22, 24, 22, 24, 0], "H": [24, 26, 24, 26, 0]}},
        {"type": "paths", "pts": 1, "c": "Network paths", "q": "Identify all the paths on the network diagram and calculate how long they are.",
         "paths": [["ADEFGH", 26], ["ABEFGH", 22], ["ACH", 14]],
         "model": "A-D-E-F-G-H = 5 + 9 + 3 + 5 + 2 + 2 = 26 (critical). A-B-E-F-G-H = 22. A-C-H = 14."},
        {"type": "num", "pts": 1, "c": "Critical path", "q": "What is the minimum completion time of this project?",
         "fields": [{"label": "Minimum completion time", "a": 26, "tol": 0}], "model": "26, the length of the critical path A-D-E-F-G-H."},
    ]
    q4_intro = "<h4>Activities</h4><p>The following table shows the main activities and their immediate predecessors that are carried out to build a new software system.</p>" + table(["Activity", "Predecessor(s)", "Duration"], F242_ACTS)
    q5 = [
        short("In the context of the Team Needs Pyramid, explain how a project manager can foster commitment among team members.", 2, [
            ["Pyramid order: trust, conflict, commitment, accountability, results; commitment builds on trust and healthy conflict", ["trust", "conflict", "pyramid", "foundation"]],
            ["Clarity: clear decisions, goals, deadlines and roles", ["clarity", "clear", "deadline", "goal", "role"]],
            ["Buy-in: let everyone be heard so they commit even if they disagreed (no consensus needed)", ["buy in", "heard", "opinion", "input", "consensus", "disagree"]],
            ["Review and communicate decisions (e.g. at the end of meetings)", ["review", "communicat", "summar", "confirm", "cascad"]],
        ], "In the pyramid (trust → managed conflict → commitment → accountability → results), commitment sits on trust and healthy conflict: people commit when they trust each other and have had their say. The PM fosters it with clarity (clear decisions, goals, roles and deadlines, confirmed at the end of each meeting) and buy-in (letting everyone voice their views so they support the decision even if they disagreed; consensus isn't required).", "Team pyramid: commitment"),
        short("How does fostering trust and managing conflict within a software project team contribute to improved collaboration and project success?", 2, [
            ["Trust: members admit mistakes, share information and ask for help openly", ["admit", "mistake", "share", "open", "help", "honest"]],
            ["Managed conflict: ideas are debated constructively, giving better decisions", ["debate", "better decision", "idea", "constructive", "healthy"]],
            ["Avoids groupthink, hidden problems and personal conflict", ["groupthink", "hidden", "personal", "harmony", "early"]],
            ["Leads to commitment, collaboration and project success", ["commit", "collaborat", "success", "result", "productiv"]],
        ], "Trust lets members admit mistakes, share information and ask for help, so problems surface early and people cooperate instead of protecting themselves. Managed (healthy) conflict means ideas are debated openly and respectfully, which gives better technical decisions and avoids groupthink or disputes that turn personal. Together they lead to real commitment and collaboration, which drives quality and project success.", "Trust and conflict"),
        short("Your software project team is experiencing delays due to unclear task ownership and inconsistent updates. As the project manager, how would you apply a team-based approach to improve accountability and transparency within the team? Describe specific steps you would take to enhance collaboration and increase the project’s chances of success.", 2, [
            ["Clarify ownership with a RACI / RAM", ["raci", "ram", "responsib", "owner", "assign"]],
            ["Regular updates: daily stand-ups or status meetings", ["stand up", "standup", "daily", "status", "meeting", "update"]],
            ["Transparency: shared task board or tool with visible goals", ["board", "kanban", "jira", "trello", "visible", "transparen", "dashboard", "tool"]],
            ["Peer accountability and retrospectives", ["peer", "retrospective", "review", "feedback", "accountab"]],
        ], "1) Clarify ownership with a RACI matrix so every task has one Responsible and one Accountable person. 2) Hold short daily stand-ups (done, next, blocked) so updates are consistent. 3) Put all tasks on a shared board (e.g. Jira or Kanban) with visible goals and deadlines so progress is transparent. 4) Encourage peer accountability and run retrospectives to fix what caused the delays.", "Accountability and transparency"),
    ]
    q6 = [
        short("How can the use of crashing and fast-tracking affect the overall project cost and risk?", 2, [
            ["Crashing: adding resources to critical-path activities to shorten them", ["crash", "add resource", "more resource", "overtime", "extra"]],
            ["Crashing increases cost (with diminishing returns)", ["cost", "expens", "diminish"]],
            ["Fast-tracking: overlapping activities that were sequential (in parallel)", ["fast track", "overlap", "parallel", "concurren"]],
            ["Fast-tracking increases risk of rework and quality problems", ["risk", "rework", "quality", "error"]],
        ], "Crashing shortens critical-path activities by adding resources (people, overtime, equipment). It raises cost, often with diminishing returns, and adds coordination risk. Fast-tracking overlaps activities that would normally run in sequence. It adds little direct cost but raises risk, because work starts on incomplete inputs and may need rework.", "Crashing and fast-tracking"),
        short("How can a burn chart help a project manager track progress and identify if the team is ahead or behind schedule?", 2, [
            ["Plots remaining (burndown) or completed (burnup) work against time", ["remaining", "completed", "work", "time", "story point"]],
            ["Compares actual line with the ideal / planned line", ["ideal", "planned", "compare", "line", "actual"]],
            ["Above the ideal line = behind; below = ahead (burndown)", ["above", "below", "behind", "ahead"]],
            ["Early warning so the PM can act (reprioritize, adjust scope)", ["early", "warning", "act", "adjust", "corrective", "scope"]],
        ], "A burndown chart plots the work remaining (e.g. story points) against time, next to an ideal line from the total down to zero at the end of the sprint. If the actual line is above the ideal line the team is behind; below it, ahead. A burnup chart shows completed work rising toward the scope line and also reveals scope changes. Either one gives an early warning, so the PM can act (remove blockers, re-prioritize, adjust scope) before the deadline.", "Burn charts"),
    ]
    return [
        {"title": "Question 1 · Motivation, principles and terminology", "items": q1},
        {"title": "Question 2 · Estimation, resourcing, scheduling and risk", "intro": case2, "items": q2},
        {"title": "Question 3 · Communication and stakeholders", "items": q3},
        {"title": "Question 4 · Project management principles", "intro": q4_intro, "items": q4},
        {"title": "Question 5 · Team-based collaboration", "items": q5},
        {"title": "Question 6 · Project control", "items": q6},
    ]


def final251():
    q1 = [
        short("How does project management contribute to organizations in achieving their strategic objectives? Please elaborate.", 2, [
            ["Aligns projects with strategy (selecting projects through portfolios and programs)", ["strateg", "align", "portfolio", "program", "select"]],
            ["Delivers outcomes, benefits and value", ["value", "benefit", "outcome", "deliver"]],
            ["Uses resources efficiently and controls scope, time and cost", ["resource", "efficien", "cost", "time", "scope", "budget"]],
            ["Manages risk and change for competitive advantage", ["risk", "change", "competit", "adapt"]],
        ], "Strategy is carried out through projects. Project management selects and prioritizes projects (through portfolios and programs) so they align with strategic objectives, then delivers them so the outputs create the intended outcomes, benefits and value. It uses limited resources efficiently, controls scope, time and cost, and manages risk and change. That lets the organization reach its goals and respond to its market faster than competitors.", "PM and strategy"),
        short("What are the key distinctions between project management and general management, particularly concerning their respective focuses, skill sets, and approaches to managing teams and resources?", 2, [
            ["Focus: project management handles temporary, unique work; general management handles ongoing, repetitive operations", ["temporary", "unique", "ongoing", "operation", "repetitive", "routine", "permanent"]],
            ["Skills: PM plans, schedules, manages risk and integrates across functions; GM needs functional expertise", ["plan", "schedul", "risk", "integrat", "cross functional", "functional"]],
            ["Teams: PM leads temporary teams, often without formal authority; GM has permanent staff and line authority", ["authority", "influence", "negotiat", "borrow", "matrix", "line", "staff"]],
            ["Resources: PM works to a fixed budget/schedule and negotiates for resources; GM manages departmental budgets", ["budget", "negotiat", "resource", "department"]],
        ], "Focus: project management delivers temporary, unique work with a defined start, end and scope; general management runs the ongoing, repetitive operations of a function. Skills: a PM needs planning, scheduling, risk, stakeholder and integration skills across functions; a general manager needs depth in one function and long-term operational skills. Teams and resources: a PM leads a temporary, cross-functional team, often borrowed from functional managers, so works by influence and negotiation within a fixed budget and schedule; a general manager has permanent staff, line authority and an ongoing departmental budget.", "Project vs general management"),
        short("Describe the significance of a project scope statement in project management and elaborate on how it aids in mitigating project risks and ensuring successful project outcomes.", 2, [
            ["Defines the scope: objectives, deliverables, acceptance criteria", ["deliverable", "objective", "acceptance", "requirement", "define"]],
            ["States exclusions, assumptions and constraints (boundaries)", ["exclusion", "out of scope", "assumption", "constraint", "boundar"]],
            ["Prevents scope creep and is the baseline for change control", ["scope creep", "creep", "baseline", "change control", "change request"]],
            ["Shared understanding with stakeholders; basis for WBS and estimates", ["stakeholder", "expectation", "agree", "understand", "wbs", "estimat"]],
        ], "The scope statement defines what the project will and won't deliver: objectives, deliverables, acceptance criteria, exclusions, assumptions and constraints. It reduces risk because everyone agrees on the boundaries up front, it's the baseline for change control (so scope creep is caught and evaluated rather than absorbed), and it's the basis for the WBS, estimates and schedule. That leads to realistic plans and a result the stakeholders will accept.", "Scope statement"),
        short("Give an example of a project management tool or technique that you might use to manage a complex software development project, and explain how it could help you ensure project success.", 2, [
            ["Names a specific tool or technique (WBS, Gantt, CPM, risk register, Scrum board, burndown, Jira)", ["wbs", "work breakdown", "gantt", "critical path", "cpm", "risk register", "scrum", "kanban", "burndown", "jira", "raci"]],
            ["Explains what it does", ["break", "show", "track", "visual", "decompos", "identif"]],
            ["Explains how it supports success (control, early problem detection, communication)", ["success", "control", "early", "on track", "communicat", "deadline", "delay", "risk"]],
        ], "A Work Breakdown Structure: it decomposes the complex system into smaller deliverables and work packages that can be estimated, assigned and tracked. Nothing is forgotten, ownership is clear, and the WBS is the base for the schedule, budget and risk analysis, so problems show up early and progress is measurable. (Other valid answers: Gantt chart, CPM, risk register, Scrum board with a burndown chart, each with its benefit explained.)", "PM tools"),
    ]
    case2 = ("<h4>TechNova Solutions</h4><p>You work for <b>TechNova Solutions</b>, a software development company specializing in intelligent business applications. You have been assigned to lead a project to <b>develop a cloud-based inventory management system</b> for a rapidly growing retail client. The project is scheduled to run <b>for five months</b> and requires a team of <b>four software developers, one UX designer, and one QA analyst</b>.</p>"
             "<p>You are given a detailed list of functional requirements, including real-time stock tracking, automated reorder alerts, multi-store synchronization, analytics dashboards, and user-role security features. Your role is to create a <b>comprehensive project plan</b> that covers <b>software effort estimation, resource allocation, sprint scheduling, stakeholder communication, quality assurance processes, and risk mitigation strategies.</b></p>"
             "<p>Your objective is to deliver a <b>robust, scalable software system</b> within the approved budget and timeline, while effectively managing scope changes, minimizing technical risks, and ensuring the client is fully satisfied with both the project process and the final software product.</p>")
    q2 = [
        short("What software estimation techniques would you use to estimate the time and effort required to complete the project, and why? How would you validate your estimates?", 2, [
            ["Names techniques (function points, story points/planning poker, three-point/PERT, Delphi, analogous, bottom-up, COCOMO)", ["function point", "story point", "planning poker", "three point", "pert", "delphi", "analog", "bottom up", "cocomo", "expert"], 2],
            ["Why: fits the detailed requirements list and the uncertainty", ["requirement", "uncertain", "feature", "detail", "range", "size"]],
            ["Validation: compare techniques, historical data, expert review, track velocity and re-estimate", ["compare", "historical", "past", "review", "velocity", "re estimat", "valid", "actual"]],
        ], "Function points (or story points with planning poker) sized from the detailed requirements list: dashboards, reorder alerts, multi-store sync and role security are countable functions. Then three-point (PERT) estimates per feature to capture uncertainty, especially for multi-store synchronization. Validate by comparing the two methods and historical data from similar projects, having the developers review the estimates, and tracking actual velocity in the first sprints to re-estimate.", "Estimation techniques"),
        short("How would you go about resourcing the project, taking into account the skills and availability of your team members, as well as any potential risks or constraints?", 2, [
            ["Skills matrix / RAM / RACI to match people to tasks", ["skill", "matrix", "ram", "raci", "expertise", "assign"]],
            ["Check availability and level the workload (no overallocation)", ["availab", "level", "overallocat", "workload", "calendar", "capacity"]],
            ["Risks: key-person dependency, cross-training, single QA/UX bottleneck, buffers", ["risk", "single", "bottleneck", "cross train", "backup", "buffer", "depend"]],
        ], "Build a skills matrix for the four developers, the UX designer and the QA analyst, and assign work with a RAM/RACI so each feature has a clear owner who has the right skills. Check everyone's availability per sprint and level the workload so no one is overallocated. Plan for risks: the single UX designer and single QA analyst are bottlenecks and key-person risks, so cross-train developers to help test, keep a schedule buffer, and agree escalation for extra resources.", "Resource planning"),
        short("What scheduling techniques would you use to create a realistic timeline for the project, and how would you ensure that you stay on track throughout the development process?", 2, [
            ["Techniques: WBS, network diagram / critical path, Gantt chart, sprint or release planning", ["wbs", "critical path", "cpm", "gantt", "network", "sprint", "release plan", "milestone"]],
            ["Realistic: dependencies, estimates and buffers", ["depend", "buffer", "contingency", "realistic", "estimat"]],
            ["Stay on track: burndown charts, stand-ups, milestone reviews, variance tracking", ["burndown", "burn", "stand up", "standup", "review", "monitor", "track", "variance"]],
        ], "Break the work down with a WBS, sequence it in a network diagram to find the critical path, and lay it out as a release plan of sprints across the five months on a Gantt chart with milestones. Include a buffer for integration and testing. To stay on track, use burndown charts and daily stand-ups within sprints, review milestones against the baseline, and re-plan or re-prioritize the backlog as soon as variance appears.", "Scheduling techniques"),
        short("List any 2 software risk identification techniques and explain how would you mitigate potential risks that could impact the success of the project? How would you prioritize and monitor these risks throughout the project lifecycle?", 2, [
            ["Two techniques (brainstorming, Delphi, checklists, interviews, SWOT, assumption analysis)", ["brainstorm", "delphi", "checklist", "interview", "swot", "assumption", "expert", "historical"], 2],
            ["Mitigation responses (prototype, testing, avoid, transfer, mitigate, contingency)", ["mitigat", "avoid", "transfer", "contingency", "prototype", "test", "response"]],
            ["Prioritize by probability × impact (risk matrix)", ["probability", "impact", "matrix", "priorit", "score"]],
            ["Monitor: risk register, owners, regular reviews, triggers", ["register", "owner", "review", "monitor", "trigger", "track"]],
        ], "Identify risks by brainstorming with the team and by using a checklist from past cloud projects (or expert interviews / Delphi). Mitigate them with planned responses, e.g. prototype multi-store synchronization early, add automated testing for the reorder logic, transfer hosting risk to the cloud provider's SLA, and keep contingency time. Prioritize each risk by probability × impact on a risk matrix, record it in a risk register with an owner and trigger, and review the register every sprint.", "Risk management"),
        {"type": "num", "pts": 2, "c": "COCOMO", "q": "A software project with 20 KLOC is being developed using the organic mode of COCOMO (a = 2.4, b = 1.05, c = 2.5, d = 0.38). Calculate the effort, development time, productivity, and staff required for this project.",
         "fields": [{"label": "Effort E", "a": 55.76, "tol": 0.5, "unit": "person-months"}, {"label": "Development time TDEV", "a": 11.52, "tol": 0.15, "unit": "months"},
                    {"label": "Productivity", "a": 358.7, "tol": 4, "unit": "LOC per person-month", "show": "358.7"}, {"label": "Staff", "a": 4.84, "tol": 0.12, "unit": "people"}],
         "model": "E = 2.4 × 20^1.05 = 2.4 × 23.23 ≈ 55.76 person-months. TDEV = 2.5 × 55.76^0.38 ≈ 2.5 × 4.61 ≈ 11.52 months. Productivity = size ÷ E = 20,000 ÷ 55.76 ≈ 358.7 LOC per person-month (0.359 KLOC/PM). Staff = E ÷ TDEV = 55.76 ÷ 11.52 ≈ 4.84, about 5 people. The paper doesn't print the constants; these are the standard organic values from the slides."},
    ]
    q3 = [
        short("In what ways do proficient communication abilities contribute to the management of project risks and the attainment of project success? Illustrate with an instance of how a breakdown in communication could affect a project, and propose methods for prevention or resolution.", 4, [
            ["Risks and issues are raised and escalated early", ["early", "escalat", "raise", "identif", "surface"]],
            ["Shared understanding of requirements and expectations; alignment and decisions", ["understand", "requirement", "expectation", "align", "decision", "clarity"]],
            ["Example of a breakdown and its effect (rework, delay, defects, conflict)", ["rework", "delay", "misunderst", "defect", "wrong", "conflict", "fail"]],
            ["Prevention: communication plan, regular meetings / stand-ups, documentation", ["communication plan", "meeting", "stand up", "standup", "document", "single source"]],
            ["Resolution: active listening, confirm understanding, feedback, clarify and update", ["listen", "confirm", "feedback", "clarif", "paraphras", "update"]],
        ], "Good communication surfaces risks and issues early so they can be handled while they are cheap, keeps requirements and expectations shared across the team and stakeholders, and supports fast, informed decisions, all of which drive success. Example: the backend team changes an API without telling the frontend team; integration fails at the end of the sprint, causing rework, a missed release and an unhappy client. Prevention: a communication plan (who needs what, how often, which channel), daily stand-ups, documented decisions in one shared place, and change notifications. Resolution: an immediate joint meeting, active listening to clarify the misunderstanding, confirming the agreed interface in writing, and updating the plan and stakeholders.", "Communication and risk"),
        short("How can project managers identify and prioritize stakeholders, and what strategies can they use to communicate effectively with each stakeholder group?", 2, [
            ["Identify: brainstorming, project charter, interviews, stakeholder register", ["brainstorm", "charter", "interview", "register", "identify", "document"]],
            ["Prioritize: power/interest grid or salience model (power, legitimacy, urgency)", ["power", "interest", "grid", "salience", "influence", "legitimacy", "urgency"]],
            ["Strategies: manage closely, keep satisfied, keep informed, monitor", ["manage closely", "keep satisfied", "keep informed", "monitor"]],
            ["Communication methods: interactive, push, pull, tailored to the group", ["interactive", "push", "pull", "tailor", "meeting", "report"]],
        ], "Identify stakeholders by brainstorming with the team, reading the charter and contracts, and interviewing key people, then record them in a stakeholder register. Prioritize them with a power/interest grid (or the salience model: power, legitimacy, urgency). Then tailor communication: high power and high interest → manage closely with interactive meetings; high power, low interest → keep satisfied with concise push reports; low power, high interest → keep informed with push updates or pull (portal); low/low → monitor.", "Stakeholder prioritization"),
    ]
    q4_intro = "<h4>Activities</h4><p>The following table shows the main activities and their immediate predecessors that are carried out to build a new software system.</p>" + table(["Task", "Duration", "Predecessor"], F251_ACTS)
    q4 = [
        {"type": "self", "pts": 3, "c": "Network diagrams", "q": "Create the network diagram using the given data.",
         "model": "Activity-on-node, durations under each letter; the critical path A-B-C-F-H-J is highlighted. Paths: A-B-C-F-H-J = 44, A-B-C-E-G-I-J = 42, A-D-G-I-J = 29." + F251_NET},
        {"type": "num", "pts": 1, "c": "Critical path", "q": "What is the minimum completion time of this project?",
         "fields": [{"label": "Minimum completion time", "a": 44, "tol": 0}], "model": "44: the critical path A-B-C-F-H-J = 6 + 9 + 3 + 7 + 12 + 7. (A-B-C-E-G-I-J = 42 and A-D-G-I-J = 29.)"},
        short("Imagine that you are the project manager for a software development project. Describe the steps you would take to develop a project plan that incorporates basic project management principles. How would you ensure that the plan is communicated effectively to all stakeholders?", 2, [
            ["Define scope and objectives with stakeholders", ["scope", "objective", "requirement", "charter", "goal"]],
            ["WBS, estimates, schedule, resources and budget", ["wbs", "work breakdown", "estimat", "schedul", "resource", "budget"]],
            ["Risk, quality and communication plans", ["risk", "quality", "communication plan"]],
            ["Communicate: kickoff meeting, tailored reports, shared access, regular updates and feedback", ["kickoff", "kick off", "meeting", "report", "update", "feedback", "share", "present"]],
        ], "Define the objectives and scope with the stakeholders (charter and scope statement); break the work into a WBS; estimate effort and durations; build the schedule (network diagram, critical path, Gantt); assign resources and set the budget; then add a risk plan, a quality plan and a communication plan, applying principles such as stakeholder engagement, value focus and tailoring. Communicate it through a kickoff meeting, a version of the plan tailored to each stakeholder group, a shared location everyone can access, and regular status updates with a way to give feedback.", "Project planning"),
    ]
    q5 = [
        short("Share an experience from a software project you were involved in where collaboration among team members significantly contributed to its success. Describe the specific strategies or techniques you employed to foster collaboration.", 2, [
            ["Describes a concrete project and the outcome", ["project", "app", "system", "website", "we ", "team", "deliver"]],
            ["Communication practices (regular meetings, stand-ups, group chat)", ["meeting", "stand up", "standup", "chat", "communicat", "weekly", "daily"]],
            ["Shared tools and clear roles (Git, task board, RACI)", ["git", "github", "board", "trello", "jira", "role", "raci", "divid"]],
            ["Collaboration techniques (pair programming, code reviews, shared decisions, helping each other)", ["pair", "review", "help", "decid", "together", "feedback", "brainstorm"]],
        ], "Any honest experience earns marks if it names concrete techniques. For example: in a course project building a booking app, we split the work by feature with clear owners, met twice a week for short stand-ups, tracked tasks on a shared Trello board, used GitHub pull requests so every change was reviewed by a teammate, and paired up on the hardest integration work. Decisions were discussed openly, so everyone committed to them, and we delivered on time.", "Team collaboration"),
        short("You are leading a cross-functional team tasked with selecting a continuous integration/continuous deployment (CI/CD) platform for an upcoming project. The team includes software developers, DevOps engineers, and QA testers, each with distinct expectations regarding automation workflows and pipeline management. Describe your approach to collaboratively choosing the most suitable CI/CD platform. Explain how you would involve all team members in the decision-making process and specify the criteria you would apply to evaluate different CI/CD solutions.", 2, [
            ["Involve everyone: gather requirements from each role in a workshop or meeting", ["workshop", "meeting", "each role", "requirement", "involve", "input", "survey"]],
            ["Evaluate with a shared weighted scoring matrix and/or a pilot / proof of concept", ["weighted", "scoring", "matrix", "pilot", "proof of concept", "poc", "trial", "demo"]],
            ["Criteria: integration with tools, automation and testing support, scalability, security, cost, ease of use, support", ["integrat", "automat", "scal", "security", "cost", "ease", "support", "performance"]],
            ["Decide together and commit (consensus or buy-in)", ["consensus", "buy in", "commit", "vote", "agree", "decide together"]],
        ], "Run a kickoff workshop where developers, DevOps engineers and QA testers each list their needs (build speed, deployment control, test automation), then agree the criteria and their weights together: integration with our repository and tools, automation and test support, pipeline flexibility, scalability and performance, security, cost, ease of use, and vendor/community support. Shortlist two or three platforms, run a short pilot or proof of concept with members from every role, score each platform on the weighted matrix, and discuss the results openly so the final choice has everyone's buy-in.", "Collaborative decision making"),
        short("Your team has just completed a major milestone in the project development process. How would you celebrate this achievement collaboratively with your team members? How would you recognize individual contributions to the team’s success? What actions would you take to ensure that team morale remains high as you move forward in the project?", 2, [
            ["Celebrate together (team event, lunch, announcement)", ["celebrat", "lunch", "dinner", "event", "party", "outing", "announce"]],
            ["Recognize individuals specifically and publicly (praise, certificates, rewards)", ["recogni", "thank", "praise", "certificate", "reward", "acknowledg", "specific", "public"]],
            ["Keep morale high: feedback, balanced workload, growth opportunities, involvement", ["feedback", "workload", "balance", "growth", "learn", "involve", "support", "burnout"]],
            ["Share the success with stakeholders and keep momentum (next goals)", ["stakeholder", "share", "next", "goal", "momentum", "retrospective"]],
        ], "Celebrate as a team, e.g. a team lunch and an announcement of the milestone to the stakeholders. Recognize individuals specifically and publicly: name what each person contributed in the meeting, send thank-you notes to their managers, and give certificates or small rewards. Keep morale high with a retrospective that captures what went well, clear and achievable next goals, a balanced workload to avoid burnout, growth opportunities, and continued recognition, not only at milestones.", "Motivation and recognition"),
    ]
    q6 = [
        short("What does a burndown chart measure, and how are its two axes labeled in Agile project management?", 1, [
            ["Measures the work remaining over time", ["remaining", "left", "work"]],
            ["X-axis: time (days, sprints or iterations)", ["time", "day", "sprint", "iteration", "x axis", "horizontal"]],
            ["Y-axis: remaining work (story points, hours or tasks)", ["story point", "hours", "task", "y axis", "vertical", "effort"]],
        ], "It measures the work remaining against time, showing whether the team will finish on schedule. X-axis: time (days of the sprint, or sprints/iterations). Y-axis: work remaining (story points, hours or tasks).", "Burn charts"),
        short("What is a Gantt chart, and what does it show in project management?", 1, [
            ["A bar chart of activities against a time scale", ["bar", "time", "timeline", "calendar", "horizontal"]],
            ["Shows start and finish dates and durations", ["start", "finish", "end", "duration", "date"]],
            ["Shows dependencies, milestones and progress", ["depend", "milestone", "progress", "overlap", "sequence"]],
        ], "A Gantt chart is a horizontal bar chart of the project's activities against a time scale. It shows each task's start and finish dates and duration, the overlaps and dependencies between tasks, the milestones, and the progress made.", "Gantt charts"),
        short("What are two advantages of using a Gantt chart?", 1, [
            ["Easy to read and communicate to stakeholders (visual)", ["easy", "visual", "simple", "understand", "communicat", "clear"]],
            ["Helps plan and track progress, overlaps, dependencies and resources", ["track", "progress", "overlap", "depend", "plan", "resource", "deadline"]],
        ], "1) It's visual and easy to understand, so it communicates the schedule well to the team and stakeholders. 2) It helps plan and track: overlaps, dependencies and deadlines are visible, and actual progress can be compared with the plan.", "Gantt charts"),
        short("What are two limitations of Gantt charts?", 1, [
            ["Hard to maintain and cluttered for large, complex or changing projects", ["update", "maintain", "large", "complex", "clutter", "change", "difficult"]],
            ["Doesn't clearly show dependencies, critical path, effort, resources or uncertainty", ["depend", "critical path", "effort", "resource", "uncertain", "cost", "not show"]],
        ], "1) They become hard to read and to keep updated on large, complex or frequently changing projects. 2) They don't clearly show the critical path, the strength of dependencies, the effort or resources behind a bar, or uncertainty in durations.", "Gantt charts"),
    ]
    return [
        {"title": "Question 1 · Motivation, principles and terminology", "items": q1},
        {"title": "Question 2 · Estimation, resourcing, scheduling and risk", "intro": case2, "items": q2},
        {"title": "Question 3 · Communication skills and stakeholders", "items": q3},
        {"title": "Question 4 · Project management principles", "intro": q4_intro, "items": q4},
        {"title": "Question 5 · Team-based collaboration", "items": q5},
        {"title": "Question 6 · Project control", "items": q6},
    ]


PAPERS = [
    {"slug": "14-final-242", "file": "final-242", "title": "Final Exam (242)", "short": "FINAL · 242", "item": 13,
     "meta": [["Term", "242 (2nd term, 2024/2025)"], ["Date", "17 May 2025"], ["Duration", "3 hours"], ["Total", "40 marks"]],
     "lede": "The real SE423 final from term 242, in its original order with its real marks. Every chapter is in scope. There was no answer key for this paper, so the model answers are written from the course slides, graded strictly by keyword. Drawing questions are self-marked against the model diagram.",
     "parts": final242},
    {"slug": "15-midterm-251-version-1", "file": "midterm-251-version-1", "title": "Midterm Exam (251) - Version 1", "short": "MIDTERM · 251 · V1", "item": 14,
     "meta": [["Term", "251 (1st term, 2025/2026)"], ["Date", "7 October 2025"], ["Duration", "50 minutes"], ["Total", "15 marks"]],
     "lede": "The real SE423 midterm from term 251, version 1 (chapters 1–3), in its original order with its real marks. MCQ answers, the RACI cells and the case-study marks come from the instructor's key, which was written for version 2 and shares these questions. The other short answers are model answers written from the course slides.",
     "parts": lambda: midterm(1)},
    {"slug": "16-midterm-251-version-2", "file": "midterm-251-version-2", "title": "Midterm Exam (251) - Version 2", "short": "MIDTERM · 251 · V2", "item": 15,
     "meta": [["Term", "251 (1st term, 2025/2026)"], ["Date", "7 October 2025"], ["Duration", "50 minutes"], ["Total", "15 marks"]],
     "lede": "The real SE423 midterm from term 251, version 2 (chapters 1–3), the version the instructor's key was written for. MCQ answers, the RACI cells and the case-study marking scheme come from that key. The other short answers are model answers written from the course slides.",
     "parts": lambda: midterm(2)},
    {"slug": "17-final-251", "file": "final-251", "title": "Final Exam (251)", "short": "FINAL · 251", "item": 16,
     "meta": [["Term", "251 (1st term, 2025/2026)"], ["Date", "Unknown"], ["Duration", "Unknown"], ["Total", "40 marks"]],
     "lede": "The real SE423 final from term 251 (the year is read from the cover sheet in the photos), in its original order with its real marks. Every chapter is in scope. There was no answer key, so the model answers are written from the course slides, graded strictly by keyword. The network diagram is self-marked against the model.",
     "parts": final251},
]

NOTES = {
    "15-midterm-251-version-1": "Part 2 question 5 has no printed mark; it is set to 0.5 so Part 2 totals 5 like the cover sheet.",
    "16-midterm-251-version-2": "Part 2 question 5 has no printed mark; it is set to 0.5 so Part 2 totals 5 like the cover sheet.",
    "17-final-251": "Question 4's total is cut off in the photo; its parts add up to 6.",
}

PAGE_CSS = """
      .exam-meta { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 170px), 1fr)); gap: 10px; margin: 18px 0 0; }
      .exam-meta div { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 12px 14px; font-size: 15px; font-weight: 600; }
      .exam-meta b { display: block; font: 700 11.5px/1.4 var(--mono); letter-spacing: 0.08em; text-transform: uppercase; color: var(--accent); margin-bottom: 2px; }
      .note { margin: 12px 0 0; color: var(--dim); font-size: 14px; }
      .section-head { display: flex; flex-wrap: wrap; align-items: baseline; gap: 6px 14px; margin: 34px 0 14px; border-bottom: 1px solid var(--border); padding-bottom: 8px; }
      .section-head h2 { margin: 0; font-family: var(--serif); font-size: clamp(22px, 2.6vw, 30px); }
      .section-head span { color: var(--dim); font: 600 13px var(--mono); }
      .card.case { margin-bottom: 14px; }
      .card.case ul { margin: 4px 0 10px; }
      .q .q-text { font-weight: 600; }
      .q .num { font: 700 12px var(--mono); color: var(--accent); margin-right: 6px; }
      .q .opt .letter { font: 700 13px var(--mono); color: var(--accent); min-width: 18px; }
      .q textarea { min-height: 130px; }
      .q textarea.small { min-height: 84px; }
      .words { font: 600 11.5px var(--mono); color: var(--faint); margin-top: 4px; text-align: right; }
      .tbl-scroll { overflow-x: auto; margin: 10px 0; }
      .grid-tbl { border-collapse: collapse; width: 100%; font-size: 14px; }
      .grid-tbl th, .grid-tbl td { border: 1px solid var(--border); padding: 6px 8px; text-align: center; vertical-align: middle; }
      .grid-tbl thead th { background: var(--accent-soft); font: 700 12px/1.3 var(--mono); }
      .grid-tbl tbody th { text-align: left; font-weight: 600; min-width: 120px; }
      .grid-tbl.given { width: auto; min-width: min(100%, 360px); }
      .grid-tbl tr.not-asked { color: var(--faint); }
      .grid-tbl tr.not-asked small { font: 600 11px var(--mono); }
      .grid-tbl select, .num-in { font: 600 14px var(--mono); padding: 5px 6px; border: 1px solid var(--border); border-radius: 6px; background: var(--surface); color: var(--text); }
      .num-in.cell { width: 3.6em; text-align: center; }
      .grid-tbl td.right { background: var(--good-soft); }
      .grid-tbl td.wrong { background: var(--bad-soft); position: relative; }
      .grid-tbl td.wrong::after { content: attr(data-key); display: block; font: 700 11px var(--mono); color: var(--good); }
      .num-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 200px), 1fr)); gap: 10px; margin: 10px 0; }
      .num-field { display: flex; flex-direction: column; gap: 4px; padding: 10px 12px; border: 1px solid var(--border); border-radius: 10px; }
      .num-field span { font-weight: 600; font-size: 14px; }
      .num-field small { color: var(--faint); font: 600 11.5px var(--mono); }
      .num-field.right { border-color: var(--good); background: var(--good-soft); }
      .num-field.wrong { border-color: var(--bad); background: var(--bad-soft); }
      .rows-tbl { border: 1px solid var(--border); border-radius: 10px; overflow: hidden; margin: 10px 0; }
      .rows-head, .rows-row { display: grid; grid-template-columns: minmax(90px, 160px) 1fr; gap: 10px; padding: 10px 12px; align-items: start; }
      .rows-head { background: var(--accent-soft); font: 700 12px/1.3 var(--mono); }
      .rows-row + .rows-row { border-top: 1px solid var(--border); }
      .rows-row b { padding-top: 6px; }
      .row-fb + .row-fb { margin-top: 12px; padding-top: 10px; border-top: 1px dashed var(--border); }
      .self-mark { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; margin: 10px 0 0; font-size: 14px; color: var(--dim); }
      svg.net { width: 100%; min-width: 480px; height: auto; color: var(--dim); display: block; margin-top: 10px; }
      .model .tbl-scroll, .feedback .net-wrap { overflow-x: auto; }
      svg.net line { stroke: currentColor; stroke-width: 1.6; }
      svg.net line.crit { stroke: var(--accent); stroke-width: 2.6; color: var(--accent); }
      svg.net rect { fill: var(--surface); stroke: var(--border-strong, var(--dim)); stroke-width: 1.4; }
      svg.net .crit rect { stroke: var(--accent); stroke-width: 2.4; fill: var(--accent-soft); }
      svg.net text { text-anchor: middle; font: 700 15px var(--mono); fill: var(--text); }
      svg.net text.d { font: 600 11.5px var(--mono); fill: var(--dim); }
      .submit-bar { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; justify-content: space-between; margin: 28px 0; padding: 16px 18px; background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); box-shadow: var(--shadow); }
      .submit-bar p { margin: 0; color: var(--dim); font-size: 14px; }
      .verdict-pill { font: 700 11px/1 var(--mono); letter-spacing: 0.06em; text-transform: uppercase; padding: 5px 8px; border-radius: 6px; }
      .verdict-pill.ok { color: var(--good); background: var(--good-soft); }
      .verdict-pill.part { color: var(--warn); background: var(--warn-soft); }
      .verdict-pill.no { color: var(--bad); background: var(--bad-soft); }
      .model { margin-top: 8px; padding: 10px 12px; border-left: 3px solid var(--good); background: var(--good-soft); border-radius: 8px; font-size: 14px; overflow-x: auto; }
      .missing { margin: 6px 0 0; padding-left: 18px; color: var(--bad); font-size: 14px; }
      .results { display: none; }
      .graded .results { display: block; }
      .review-list { columns: 2 260px; padding-left: 18px; margin: 8px 0 0; }
      .review-list li { break-inside: avoid; margin: 3px 0; }
      .review-list li span { color: var(--dim); font: 600 12px var(--mono); }
      @media (max-width: 640px) { .topnav .long { display: none; } .rows-head, .rows-row { grid-template-columns: 1fr; gap: 6px; } .rows-head span:last-child { display: none; } .grid-tbl tr.not-asked { display: none; } }
"""


def esc_models(parts):
    for p in parts:
        for it in p["items"]:
            if it["type"] != "self" and it.get("model"):
                it["model"] = e(it["model"])
            for r in it.get("rows", []):
                r["model"] = e(r["model"])
    return parts


def page(p, parts):
    url = f"{SITE}{BASE}{p['slug']}/"
    total = sum(it["pts"] for part in parts for it in part["items"])
    desc = f"SE423 {p['title']} as an interactive exam: the real paper's questions and marks, check each answer as you go, strict keyword grading and model answers."
    nav = "\n".join(f'          <a href="#part-{i + 1}">{"Part " if p["file"].startswith("midterm") else "Q"}{i + 1}</a>' for i, part in enumerate(parts))
    meta = "".join(f"<div><b>{e(k)}</b>{e(v)}</div>" for k, v in p["meta"])
    note = f'<p class="note">{e(NOTES[p["slug"]])}</p>' if p["slug"] in NOTES else ""
    return f"""<!doctype html>
<html lang="en" data-sg-styled>
  <head>
    <link rel="icon" type="image/png" sizes="256x256" href="/assets/shoug-favicon-v4.png" />
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/shoug-apple-touch-icon-v4.png" />
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>SE423 | {e(p['title'])}</title>
    <meta name="description" content="{e(desc)}" />
    <link rel="canonical" href="{url}" />
    <meta property="og:title" content="SE423 | {e(p['title'])}" />
    <meta property="og:description" content="{e(desc)}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:type" content="website" />
    <meta property="og:image" content="https://shoug-tech.com/assets/og-banner.png" />
    <meta name="twitter:card" content="summary_large_image" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,650&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet" />
    <script src="/javascripts/html-theme-sync.js"></script>
    <link rel="stylesheet" href="/styles/se423.css" />
    <style>{PAGE_CSS}    </style>
  </head>
  <body>
    <header class="topbar">
      <div class="wrap">
        <span class="brand"><b>SE423</b> // {e(p['short'])}</span>
        <nav class="topnav" aria-label="Exam sections">
{nav}
        </nav>
        <div class="topbar-end">
          <div data-page-search-host></div>
          <button class="btn" type="button" onclick="toggleTheme()"><span data-theme-label>Dark</span></button>
        </div>
      </div>
    </header>
    <main class="wrap" id="exam">
      <section class="hero">
        <div class="eyebrow">SE423 · Software Project Management · Past paper</div>
        <h1>{e(p['title'])}</h1>
        <p class="lede">{e(p['lede'])} Use <b>Check answer</b> on any question to see its result and model answer straight away, or submit at the end for your total.</p>
        <div class="exam-meta">{meta}</div>
        {note}
      </section>

      <div class="results" id="results"></div>
      <div id="paper"></div>

      <div class="submit-bar">
        <p id="progress">Your answers are saved in this browser as you type.</p>
        <div style="display: flex; gap: 8px; flex-wrap: wrap">
          <button class="btn" type="button" id="reset">Start over</button>
          <button class="btn primary" type="button" id="submit">Submit for grading</button>
        </div>
      </div>
      <p class="foot">SE423 · {e(p['title'])} · {total:g} marks · original questions, model answers from the course slides</p>
    </main>
    <script src="./{p['file']}-bank.js"></script>
    <script src="../past-paper.js"></script>
  </body>
</html>
"""


def wrapper(p, prev_slug, next_slug, template):
    s = template
    old_title = "Midterm Mock Exam - Chapters 1–3"
    s = s.replace(old_title, p["title"])
    s = re.sub(r"SE423 mock midterm for chapters 1–3 in the instructor's style[^\"]*", f"SE423 {p['title']}: the real past paper as an interactive exam with per-question checking, strict keyword grading and model answers.", s)
    s = s.replace("exams/midterm-mock-exam/", f"exams/{p['slug']}/")
    s = s.replace("./midterm-mock-exam.html", f"./{p['file']}.html")
    s = s.replace("ITEM_04 // EXAMS", f"ITEM_{p['item']:02d} // EXAMS")
    s = re.sub(r'(href=")[^"]*("\s*class="nav-link prev")', rf"\g<1>{BASE}{prev_slug}/\2", s)
    s = re.sub(r'(href=")[^"]*("\s*class="nav-link next")', rf"\g<1>{BASE}{next_slug}/\2", s)
    assert "midterm-mock-exam" not in s.split("<nav class=\"sidebar")[0], p["slug"]
    return s


def main():
    template = (EXAMS / "midterm-mock-exam/index.html").read_text()
    chain = ["09-software-engineering-quiz"] + [p["slug"] for p in PAPERS] + ["04-introduction-quiz"]
    for i, p in enumerate(PAPERS):
        parts = esc_models(p["parts"]())
        d = EXAMS / p["slug"]
        d.mkdir(exist_ok=True)
        bank = {"id": p["file"], "parts": parts}
        (d / f"{p['file']}-bank.js").write_text(
            f"/* SE423 {p['title']}: generated by scripts/build_se423_past_papers.py. Edit the builder, not this file. */\nwindow.PAPER = "
            + json.dumps(bank, ensure_ascii=False, indent=1) + ";\n")
        (d / f"{p['file']}.html").write_text(page(p, parts))
        (d / "index.html").write_text(wrapper(p, chain[i], chain[i + 2], template))
        total = sum(it["pts"] for part in parts for it in part["items"])
        print(f"{p['slug']}: {sum(len(x['items']) for x in parts)} questions, {total:g} marks")


if __name__ == "__main__":
    main()

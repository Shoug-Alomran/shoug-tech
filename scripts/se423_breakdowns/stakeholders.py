"""SE423 Chapter 8 — Stakeholders (all 42 slides of slides/chapter-8/stakeholders.pdf)."""
from . import sec, hook, box, strip, sub, col, two, table, qa, bullets, cheat, mistakes, quiz

PAGE = {
    "brand": "Stakeholder<span>·</span>Playbook",
    "chapter": "Chapter 8",
    "footer": "SE423 · Software Project Management · Chapter 8 — Stakeholders",
    "eyebrow": "SE423 · Software Project Management · Chapter 8",
    "title": "Know who cares,<br /><em>then tell them the truth.</em>",
    "lead": ("Stakeholder management is developing the right strategy for every person or group the project affects, so they stay engaged "
             "across the life cycle. It rests on communication: who needs what information, why, when, how, and from whom, delivered honestly. "
             "This chapter covers the register and plan, engagement levels, the mapping models, push/pull/interactive communication, "
             "ethics, and the reports that keep expectations realistic."),
    "badges": ["Register &amp; plan", "Engagement levels", "Salience · knowledge base · power/interest", "Push · pull · interactive", "Report types"],
    "nav": [("manage", "Management"), ("reporting", "Reporting"), ("communication", "Communication"), ("ethics", "Ethics"),
            ("engage", "Engagement"), ("models", "Mapping Models"), ("expectations", "Expectations &amp; Reports"),
            ("cheat", "Cheat Sheet"), ("mistakes", "Mistakes"), ("quiz", "Pop Quiz")],
}

S = []

S.append(sec("manage", "§ 01 — STAKEHOLDER MANAGEMENT", "Strategies for everyone the project touches",
    "Stakeholder management is the process of developing appropriate management strategies for all project stakeholders. Its goal is to "
    "engage them effectively throughout the life cycle, analyzing their needs, interests and potential impact, and to give the project a plan "
    "for interacting with them in the project's interest.",
    qa("Inputs, tools and outputs", "process", None,
       table(["", "Items"], [
           ["Inputs", "<b>Project charter</b> (authorizes the project, names key stakeholders such as the sponsor and client) · <b>procurement "
            "documents</b> (reveal external stakeholders: vendors, contractors, partners) · <b>enterprise environmental factors</b> (culture, "
            "regulations, market) · <b>organizational process assets</b> (templates, past stakeholder lists, lessons learned, communication policies)"],
           ["Tools and techniques", "<b>Stakeholder analysis</b> (who they are, their interests, influence and impact) · expert judgment · meetings and company visits"],
           ["Outputs", "<b>Stakeholder register</b> · <b>stakeholder management plan</b>"]])),
    two(col(sub("The stakeholder register"),
            box("The primary output of Identify Stakeholders. For each stakeholder: name · position · location · role in the project · contact "
                "information · major requirements · main expectations · potential influence · the life-cycle phase of most interest · a "
                "<b>classification</b> (internal/external; supporter/neutral/resister; high/medium/low influence, power, impact or interest).")),
        col(sub("Engagement levels"),
            box("<b>Unaware</b>: unaware of the project and its impacts<br /><b>Resistant</b>: aware, and resistant to the changes<br />"
                "<b>Neutral</b>: aware, neither supportive nor resistant<br /><b>Supportive</b>: aware, and supportive of the changes<br />"
                "<b>Leading</b>: aware, and actively engaged in making the project succeed"))),
    qa("The stakeholder management plan", "supplements the register",
       "It identifies the strategies needed to engage stakeholders, adding to the register:",
       box("• <b>desired and current</b> engagement levels of key stakeholders<br />• scope and impact of the change on each stakeholder<br />"
           "• interrelationships and overlap between stakeholders<br />• communication requirements<br />"
           "• information to distribute (language, format, content, level of detail), why, and its expected impact on engagement<br />"
           "• time frame and frequency of distribution"),
       strip("<b>Sensitive document.</b> The PMBOK warns that information given to resistant stakeholders can be damaging, so think about who "
             "sees the plan and what is shared."), accent="accent-2"),
    two(col(sub("The agile view"),
            box("Identifying stakeholders is valuable: the more inclusive your understanding, the better. Agile favors <b>transparency</b> "
                "(it builds trust) and uses <b>information radiators</b>, such as a project wiki, that make progress and impediments visible to "
                "everyone. That minimizes miscommunication and short-circuits rumors.")),
        col(sub("Tailoring information per stakeholder"),
            box("Stakeholder management sometimes tailors information access and flow to each stakeholder. That can be justified on a volatile, "
                "highly politicized project, but it carries risk."),
            box("<b>Champion:</b> often a senior leader, sponsor or influential stakeholder who backs the project.", style="margin-top: 10px"))),
))

S.append(sec("reporting", "§ 02 — STAKEHOLDER REPORTING IN AGILE AND DEVOPS", "Iterative work is hard to see from outside",
    None,
    two(col(box("Agile and DevOps need proper <b>tooling for reporting</b> to key stakeholders. A complex tool chain has grown up to manage agile "
                "projects, because iterative work makes it hard for stakeholders to tell what is happening, or whether the project is on time "
                "and on budget.")),
        col(box("Those stakeholders include not only Dev and Ops but <b>management, product management, marketing, sales and finance</b>, and "
                "the problem grows when they look across multiple projects. <b>Business value metrics dashboards</b> give managers real-time, "
                "automated reporting on best-practice KPIs, and customers can set targets to see which agile processes need improving."))),
))

S.append(sec("communication", "§ 03 — COMMUNICATION", "The most important factor in engaging stakeholders",
    "Communication planning overlaps with identifying, analyzing, prioritizing and engaging stakeholders.",
    hook("❓", "Who · What · Why · How · When · Who has it",
         "The six questions for planning communication: who needs information, what each stakeholder needs, why share it, the best way to "
         "provide it, when and how often, and who has the information. Information may be internal or external, sensitive or public, general "
         "or detailed; analyzing all of this is the foundation of the communication plan."),
    two(col(sub("Communication concepts"),
            box("Communication passes through a <b>channel</b> and is distorted by <b>noise</b>. Types include push, pull and interactive "
                "(see § 05).<br /><br /><b>Number of communication channels</b> for N people = <b>N(N − 1) / 2</b>.<br /><br />"
                "<b>Blockers:</b> no agenda, poor timing and similar barriers.")),
        col(sub("For a successful meeting"),
            box("• send notice in advance<br />• set a time limit<br />• regular, but not too frequent<br />"
                "• a clear purpose and agenda announced beforehand<br />• assign action items with clear deadlines and owners<br />"
                "• document and publish the minutes"))),
    qa("Plan communications", "who, when, what channel, how often",
       "Consider culture, expectations, technology, methods, and established policies and procedures. Then plan what to communicate:",
       table(["Type", "Examples"], [
           ["Project documents", "Charter, project management plan"],
           ["Schedule and resources", "WBS, resource needs, meeting schedule, work assignments (upcoming and current)"],
           ["Status", "General status, impacts to and from other projects, performance reports"],
           ["Risks", "New risks, uncertainties, realized risks (problems)"],
           ["Change control", "Scope changes, communications with the change control board (CCB): sponsors, PMs, technical leads, QA and others who approve changes"]]),
       box("The <b>communication management plan</b> is the primary output of Plan Communications.", style="margin-top: 14px"), accent="accent-2"),
))

S.append(sec("ethics", "§ 04 — ETHICAL AND PROFESSIONAL RESPONSIBILITY", "Communication is not effective unless it is honest",
    None,
    two(col(sub("Ethical responsibility"),
            box("Communication is at the heart of ethical behavior for a PM or team member:<br />• try to understand the truth<br />"
                "• be careful: your perception of the truth may be false<br />• seek the whole truth<br />• be truthful in all communications<br />"
                "• communicate honestly even if the project is in trouble<br />• create an environment where others tell the truth; telling it "
                "consistently shows that only the truth is acceptable")),
        col(sub("Professional responsibility"),
            box("• accept only assignments you are qualified for (lack of qualification is a major risk)<br />"
                "• protect proprietary information; report unethical behavior and violations<br />• keep an attitude of mutual cooperation<br />"
                "• consider other projects and operations when asking for resources<br />• protect team members' reputations<br />"
                "• ask which communication method stakeholders prefer<br />• be direct with conflict: discuss it openly with the other party, "
                "not behind their back<br />• look for conflicts of interest and disclose them"))),
))

S.append(sec("engage", "§ 05 — STAKEHOLDER ENGAGEMENT", "Six steps, and the right way to talk",
    None,
    two(col(sub("The six steps"),
            box("1. <b>Identify</b> your stakeholders<br />2. <b>Understand</b> them<br />3. <b>Analyze</b> them<br />4. <b>Prioritize</b> them<br />"
                "5. <b>Engage</b> them<br />6. <b>Monitor</b> them"),
            sub("Identifying stakeholders means"),
            box("1. Analyze stakeholders continuously · 2. Create and maintain a stakeholder register · 3. Create and execute a stakeholder management strategy")),
        col(sub("What engaging involves"),
            box("Working collaboratively with stakeholders to introduce the project, <b>elicit requirements</b>, manage expectations, resolve issues, "
                "negotiate, prioritize, solve problems and make decisions.<br /><br />It needs <b>soft skills</b> (active listening, interpersonal "
                "skills, conflict management) and <b>leadership skills</b> (establishing the vision, critical thinking)."))),
    qa("Push, pull and interactive communication", "communication methods", None,
       table(["Method", "Examples", "Notes"], [
           ["<b>Push</b>", "Memos, emails, status reports, voice mail", "One-way, to individuals or groups. You can't immediately gauge reaction "
            "or understanding, so use it deliberately"],
           ["<b>Pull</b>", "Intranet policies and templates, internet searches, online repositories", "Sought by the stakeholder; used for indirect "
            "sensing of stakeholder concerns; suits large audiences"],
           ["<b>Interactive</b>", "Meetings, calls, video conferences", "Two-way and real time; best for building shared understanding"]]),
       box("<b>Quick feedback loops</b> (with every method) confirm how far the message was heard, whether stakeholders agree with it, any "
           "nuanced or unintended messages they picked up, and other insights.", style="margin-top: 14px"), accent="accent-2"),
))

S.append(sec("models", "§ 06 — STAKEHOLDER MAPPING MODELS", "Three ways to prioritize",
    None,
    qa("Power/interest grid", "prioritize communication effort",
       "Two dimensions: the stakeholder's power (influence) and their interest in the project.",
       table(["Quadrant", "Strategy"], [
           ["High power · high interest", "<b>Manage closely</b>: engage regularly and manage expectations"],
           ["High power · low interest", "<b>Keep satisfied</b>: meet their needs and actively consult"],
           ["Low power · high interest", "<b>Keep informed</b>: maintain their interest"],
           ["Low power · low interest", "<b>Monitor</b>: provide information as needed"]])),
    two(col(sub("Salience model"),
            box("Prioritizes stakeholders by how much attention they demand, using three attributes: <b>power</b>, <b>legitimacy</b> and "
                "<b>urgency</b>. All three make a <b>definitive</b> stakeholder; two make dominant (power + legitimacy), dangerous (power + urgency) "
                "or dependent (legitimacy + urgency); one makes dormant, discretionary or demanding.")),
        col(sub("Stakeholder knowledge base chart"),
            box("Shapes communication tactics by how much a stakeholder <b>knows</b> and whether they <b>support or oppose</b>:<br /><br />"
                "<b>Aware · opposition</b>: may be a risk; needs management<br />"
                "<b>Aware · support</b>: keep informed so they keep championing<br />"
                "<b>Ignorant · opposition</b>: more understanding may change their attitude<br />"
                "<b>Ignorant · support</b>: engage them to keep them on board and strengthen support"))),
))

S.append(sec("expectations", "§ 07 — MANAGING EXPECTATIONS AND REPORTING", "Reports that help, not hide",
    "Managing expectations applies communication methods, interpersonal skills and management skills to the people important to the project.",
    two(col(sub("Items that may need regular communication"),
            box("• schedule, budget, forecasts<br />• risk register, issue log, change log<br />• items outside the project's control that affect it")),
        col(sub("Making reports and metrics useful"),
            box("Collect, analyze, package and send information to stakeholders, with the right level of detail and channel.<br />"
                "• don't let reports stop you managing the project<br />• measure against a consistent baseline<br />"
                "• be truthful, with accurate metrics<br />• cover all three sides of the triangle plus quality<br />"
                "• enhance with forecasts · get feedback · use several report types"))),
    qa("Performance report types", "know the question each answers", None,
       table(["Report", "Answers"], [
           ["Status", "Where is the project against the performance measurement baseline?"],
           ["Progress", "What has been accomplished?"],
           ["Trend", "Is performance improving or deteriorating?"],
           ["Forecasting", "What are the predictions for the future?"],
           ["Variance", "How do actual results compare with the baselines?"],
           ["Earned value", "Where is the project in pure earned value / cost management terms?"],
           ["Lessons learned", "What could be useful for future projects?"]]), accent="accent-2"),
    box("<b>Conclusion:</b> apply communication concepts to stakeholders and the team alike; communication is only effective if it is ethical "
        "and honest; expectation management starts with understanding each stakeholder and choosing the best communication for them; view "
        "reports and metrics from the stakeholder's perspective.", style="margin-top: 18px"),
))

S.append(cheat([
    ["Stakeholder management", "Develop strategies to engage all stakeholders across the life cycle"],
    ["Inputs", "Charter · procurement documents · enterprise environmental factors · organizational process assets"],
    ["Outputs", "Stakeholder register · stakeholder management plan"],
    ["Engagement levels", "Unaware · resistant · neutral · supportive · leading"],
    ["Engagement steps", "Identify · understand · analyze · prioritize · engage · monitor"],
    ["Power/interest", "Manage closely · keep satisfied · keep informed · monitor"],
    ["Salience", "Power + legitimacy + urgency = definitive"],
    ["Knowledge base chart", "Aware/ignorant × support/opposition"],
    ["Communication planning", "Who · what · why · how · when · who has it"],
    ["Channels", "N(N − 1) / 2"],
    ["Push / pull / interactive", "Sent one-way / fetched when needed / two-way real time"],
    ["Report types", "Status · progress · trend · forecasting · variance · earned value · lessons learned"],
    ["Plan Communications output", "Communication management plan"],
]))

S.append(mistakes([
    ("Register vs plan", "“The stakeholder plan lists names, roles and contact details.”", "That is the register. The plan adds strategies: desired vs current engagement, communication requirements, distribution."),
    ("Push vs pull", "Calling a portal or wiki “push”.", "Pull: stakeholders fetch it when they need it. Push is sent to specific people (emails, memos, reports)."),
    ("Keep satisfied vs keep informed", "High power, low interest → keep informed.", "High power, low interest → keep satisfied. Low power, high interest → keep informed."),
    ("Status vs progress report", "Using the two names interchangeably.", "Status: where we stand against the baseline. Progress: what was accomplished in a period."),
    ("Neutral vs unaware", "A stakeholder who doesn't react is “unaware”.", "Unaware stakeholders don't know about the project; neutral ones know and neither support nor resist."),
    ("Honesty under pressure", "Softening bad news to keep stakeholders calm.", "Communicate honestly even when the project is in trouble; only the truth should be acceptable."),
]))

S.append(quiz([
    ("What are the two outputs of stakeholder identification and analysis?", "The <b>stakeholder register</b> and the <b>stakeholder management plan</b>."),
    ("List five things the stakeholder register holds for each stakeholder.", "Any five of: name, position, location, role, contact info, major requirements, expectations, potential influence, phase of most interest, classification."),
    ("Name the five engagement levels.", "Unaware, resistant, neutral, supportive, leading."),
    ("Why is the stakeholder management plan sensitive?", "It records frank assessments; sharing it with resistant stakeholders can be damaging."),
    ("What is an information radiator?", "A tool such as a project wiki that makes progress and impediments visible to every interested stakeholder."),
    ("How many communication channels for 9 people?", "9 × 8 / 2 = <b>36</b>."),
    ("Give the six questions for planning communication.", "Who needs it, what they need, why share it, how best to provide it, when and how often, who has it."),
    ("What is the weakness of push communication?", "It is one-way, so you can't immediately gauge reaction or understanding."),
    ("What makes a stakeholder “definitive” in the Salience model?", "Having all three attributes: power, legitimacy and urgency."),
    ("Which strategy fits an aware stakeholder who opposes the project?", "Treat them as a risk that needs active management."),
    ("Which report answers “is performance improving or deteriorating?”", "The <b>trend</b> report."),
]))

SECTIONS = S

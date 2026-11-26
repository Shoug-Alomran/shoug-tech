"""SE423 Chapter 3 — Team (all 77 slides of slides/chapter-3/team.pdf)."""
from . import sec, hook, box, strip, sub, col, two, table, qa, bullets, cheat, mistakes, quiz

PAGE = {
    "brand": "Team<span>·</span>Playbook",
    "chapter": "Chapter 3",
    "footer": "SE423 · Software Project Management · Chapter 3 — Team",
    "eyebrow": "SE423 · Software Project Management · Chapter 3",
    "title": "Projects fail on <em>people</em><br />before they fail on code.",
    "lead": ("McConnell: software projects fail because the team lacks the <b>knowledge</b> to run the project, or lacks the "
             "<b>resolve</b> (determination, commitment, mental toughness) to run it well. This chapter is the people side: how a team "
             "forms, builds trust, handles conflict, commits and holds itself accountable, which team model to use, and how a project "
             "manager motivates, selects, leads and grows people."),
    "badges": ["Team needs pyramid", "Tuckman's stages", "RACI &amp; skills matrix", "Team models", "Motivation &amp; leadership"],
    "nav": [("develop", "Development"), ("trust", "Trust"), ("conflict", "Conflict"), ("commit", "Commitment"), ("models", "Team Models"),
            ("motivation", "Motivation"), ("groups", "Groups"), ("staff", "Staff &amp; Space"), ("pmskills", "PM Skills"),
            ("manage", "Managing"), ("leadership", "Leadership"), ("cheat", "Cheat Sheet"), ("mistakes", "Mistakes"), ("quiz", "Pop Quiz")],
}

S = []

S.append(sec("develop", "§ 01 — TEAM DEVELOPMENT", "From a group of people to a team",
    "The questions the chapter opens with: what are your responsibilities as a team member, and as a PM? How does team development "
    "relate to the project triangle? What matters more, strong individuals or a strong team? What makes a good team?",
    hook("🔺", "Trust → Conflict → Commitment → Accountability → Results",
         "The <b>team needs pyramid</b>. Lower-level needs must be satisfied before higher-level needs can be addressed: without trust "
         "there is no healthy conflict, without conflict no real commitment, and so on up to results. The chapter's sections follow this order."),
    two(col(sub("Five types of influence a leader can use"),
            table(["Influence", "Where it comes from"], [
                ["Authority (position)", "Granted by the organizational hierarchy or role"],
                ["Reward", "The ability to offer incentives"],
                ["Punishment (coercive)", "The threat or use of punishment"],
                ["Expert", "Specialized knowledge or skills"],
                ["Referent", "Personal traits, charisma or likability"]])),
        col(sub("Tuckman's model of team development"),
            box("<b>1. Forming</b>: the group comes together and gets to know one another.<br /><br />"
                "<b>2. Storming</b>: chaotic competition for leadership and trials of group processes (competing for influence or control, "
                "often without clear structure or authority).<br /><br />"
                "<b>3. Norming</b>: agreement is eventually reached on how the group operates.<br /><br />"
                "<b>4. Performing</b>: the group practices its craft and becomes effective in meeting its objectives.<br /><br />"
                "<b>5. Dissolving / adjourning</b>: the work ends and the team disbands."))),
    qa("Team structure follows the team's objective", "three objectives",
       "Ask first: what is the team's objective? Each of the three objectives shapes the team's structure, behavior and competencies.",
       table(["Objective", "Structure", "Team traits"], [
           ["<b>Problem resolution</b>: a complex, poorly defined problem; focus on 1–3 specific issues (e.g. fixing a showstopper defect)",
            "Flexible roles, rapid decision-making, often a temporary task force", "Sense of urgency and pressure"],
           ["<b>Creativity</b>: new product development, generating new ideas, products or approaches",
            "Looser hierarchy, diverse skill sets, a culture that supports risk-taking", "Independence and freedom to explore"],
           ["<b>Tactical execution</b>: carrying out a well-defined plan",
            "Clear roles, well-defined tasks and accountability", "Clarity, focus and precision"]]),
       accent="accent-2"),
))

S.append(sec("trust", "§ 02 — BUILDING TRUST", "Trust is the foundation of teamwork",
    "Without trust, teams struggle to collaborate, share ideas or resolve conflict.",
    two(col(sub("Vulnerability-based trust"),
            box("Trust is about <b>vulnerability</b>, which is hard for most people. It means being comfortable:<br />"
                "• admitting mistakes<br />• asking for help<br />• saying “I don't know”<br /><br />"
                "Trust <b>takes time</b>: consistent behavior, follow-through on commitments and shared experiences, especially under pressure. "
                "It also has to be <b>maintained</b> over time."),
            strip("<b>Technique:</b> behavioral profiling (like Myers-Briggs) helps people admit strengths and weaknesses, e.g. recognize "
                  "someone's introverted tendencies and adjust task assignments to match their strengths.")),
        col(sub("Establishing a basis of trust"),
            box("A solid basis for trust is <b>earned, not granted</b>: most people in most situations are naturally wary of others.<br /><br />"
                "• Maintain <b>open communication</b>: communication barriers create project risks<br />"
                "• <b>Be fallible</b>: take responsibility for mistakes, correct them, and say how you will avoid them<br />"
                "• <b>Lead by example</b>, not by mandate<br />"
                "• <b>Complete commitments on time</b>; if you can't, give notice and an explanation, not an excuse<br />"
                "• <b>Don't confuse friendship with leadership</b>"))),
))

S.append(sec("conflict", "§ 03 — MANAGING CONFLICT", "Healthy conflict needs trust",
    "Good conflict is unfiltered, passionate debate around issues. Even on the best teams it is sometimes uncomfortable.",
    two(col(sub("Conflict norms"),
            box("Conflict norms vary by team and must be discussed and made clear. <b>Norms are the rules of engagement</b>: what is acceptable "
                "in debate (tone, language, timing, emotional expression).<br /><br />"
                "Fear of occasional personal conflict should not stop regular, productive debate. <b>Avoidance is costly</b>: teams that fear "
                "conflict fall into <b>groupthink</b>, where a cohesive group puts harmony and consensus ahead of critical thinking.")),
        col(sub("Disagreement is not conflict"),
            box("Every team meets conflict: <b>successful teams resolve it</b>, unsuccessful teams push it into the background.<br /><br />"
                "Conflict involves a <b>hardening of positions</b> and intractability; disagreement does not. Almost every conflict traces back "
                "to a clash between two parties.<br /><br />"
                "People outside the conflict should stay <b>neutral</b>, even if they agree with one side, and one of them takes the role of "
                "<b>conciliator</b>, mediating to defuse the situation and reduce the conflict."))),
    qa("Six conflict resolution techniques", "know all six",
       None,
       table(["Technique", "What it does"], [
           ["<b>Confronting (problem solving)</b>", "Resolve the root cause through open, honest dialogue"],
           ["<b>Compromising</b>", "Reach a middle ground through mutual concessions"],
           ["<b>Withdrawal (avoidance)</b>", "Delay or sidestep the conflict"],
           ["<b>Smoothing (accommodating)</b>", "Keep harmony by playing down the differences"],
           ["<b>Collaborating</b>", "Integrate several perspectives into a creative solution"],
           ["<b>Forcing</b>", "Impose a solution through authority or pressure"]]),
       box("<b>Problem solving in six steps:</b> 1) define the real (root) problem · 2) analyze it · 3) identify solutions · "
           "4) pick a solution · 5) implement it · 6) review it and confirm it solved the problem.", style="margin-top: 14px"),
       accent="accent-2"),
))

S.append(sec("commit", "§ 04 — COMMITMENT, ACCOUNTABILITY, RESULTS", "The top of the pyramid",
    None,
    two(col(sub("Achieving commitment = clarity + buy-in"),
            box("<b>Clarity</b>: everyone knows exactly what was decided, why it matters and what happens next. Avoid assumptions and "
                "ambiguity; end discussions with a clear understanding of the decision.<br /><br />"
                "<b>Buy-in</b>: members support the decision even if they didn't fully agree, because they trust the process and feel heard.<br /><br />"
                "<b>Buy-in does not require consensus.</b> Great teams disagree and still commit.")),
        col(sub("Embracing accountability"),
            box("On a strong team, accountability happens <b>directly among peers</b>: members hold each other to standards instead of "
                "waiting for the manager.<br /><br />"
                "The leader must show a <b>willingness to confront</b> accountability: model transparency, follow through, and address "
                "underperformance respectfully but firmly. The best moments are meetings and regular reviews of accomplishments."),
            strip("Sprint review: “We committed to five stories but completed three. Let's explore what happened and how we can improve next sprint.”"))),
    qa("RACI and the responsibility assignment matrix (RAM)", "who does what",
       "RACI: <b>R</b>esponsible (does the work), <b>A</b>ccountable (the single owner who signs off), <b>C</b>onsulted (gives input), "
       "<b>I</b>nformed (kept up to date). Some variants add <b>S</b>upport (RASCI) for collaborative roles; it is not part of the original acronym.",
       two(col(sub("Responsibility assignment matrix"),
               box("A resource planning tool: <b>who does what</b>. Used for both planning and tracking, it identifies authority, accountability "
                   "and responsibility. “Who” can be a person, a team or a department, and rows or columns can carry totals (e.g. total "
                   "contributors on a task).")),
           col(sub("Skills matrix"),
               box("Another resource planning tool: resources on one axis, skills on the other. Skills can be high-level or very specific; "
                   "cells hold X's or numbers (e.g. level, years of experience)."))),
       accent="accent-2"),
    box("<b>Focusing on results.</b> The true measure of a great team is that it achieves the results it set out to achieve. Members put the "
        "team's results ahead of individual or department needs, and the team publicly states its desired results and keeps them visible.",
        style="margin-top: 18px"),
))

S.append(sec("models", "§ 05 — TEAM MODELS", "Pick the structure that fits the work",
    "Two early philosophies: <b>decentralized / democratic</b> and <b>centralized / autocratic</b>, with a middle variation, "
    "<b>controlled decentralized</b>.",
    table(["Model", "How it works", "Watch out for"], [
        ["<b>Business team</b> (most common)", "Technical lead plus a team of equal status; hierarchical with one principal contact. The hierarchy "
         "can be <b>strong</b> (lead has clear authority) or <b>loose</b> (lead facilitates). Adaptable and general; the usual starting point.",
         "Can evolve toward a democratic team as trust and shared norms grow"],
        ["<b>Democratic team</b> (self-organizing)", "The group decides as a whole by consensus. The leader is the external interface but does "
         "not allocate work; tasks go by ability and experience.", "Works only when all members are experienced and competent"],
        ["<b>Agile programming groups</b>", "A variant of democratic teams: some management decisions are delegated to members. In XP, "
         "programmers work in pairs and share collective responsibility for the code.", "Needs mature, self-directed people"],
        ["<b>Chief programmer (surgical) team</b>", "IBM, 1970s. A superstar writes the core code, like a surgeon supported by anesthetists and "
         "nurses: a backup programmer (co-pilot), program clerk (documentation, version control), administrator, toolsmith and other specialists.",
         "See the four problems below"],
        ["<b>Skunk works team</b>", "Talented, creative developers placed away from the “mother ship”, literally or figuratively. "
         "<b>Pro:</b> high ownership and buy-in. <b>Con:</b> little visibility into progress.",
         "For exploratory work needing creativity, not well-defined or narrow problems"],
        ["<b>SWAT team</b>", "A highly skilled team whose skills tightly match the goal; members often work together (e.g. a security SWAT "
         "team, an Oracle performance team).", "Narrow by design"],
        ["<b>Large teams</b>", "Communication grows with the square of the number of people, so it must be formalized and a hierarchy is "
         "always used; break the work into units of optimal size.", "Keep units under 10"]]),
    two(col(sub("Problems with chief programmer teams"),
            box("• Talented designers and programmers are hard to find; without exceptional people it fails<br />"
                "• Other members may resent the chief taking the credit, and undermine the role<br />"
                "• High project risk: the project fails if both the chief and the deputy are unavailable<br />"
                "• Organizational structures and grades may not accommodate this type of group")),
        col(sub("Team size"),
            box("Communication paths = <b>n(n − 1) / 2</b>: 50 programmers ≈ 1,225 paths (the slide rounds it to about 1,200).<br /><br />"
                "Keep teams <b>under 10</b> (seven plus or minus one); the optimal size is <b>4–6 developers</b> plus a tech lead, with QA, "
                "ops and design on top. Small projects create stronger identification and more cohesion."))),
))

S.append(sec("motivation", "§ 06 — MANAGING PEOPLE: MOTIVATION", "Motivation is needs-based",
    "People are an organization's most important assets. A manager's tasks are people-oriented: without some understanding of people, "
    "management will fail.",
    two(col(sub("People-related management activities"),
            box("• <b>Problem solving</b> using the available people<br />• <b>Motivating</b> the people on the project<br />"
                "• <b>Planning</b> what people will do<br />• <b>Estimating</b> how fast people will work<br />"
                "• <b>Controlling</b> people's activities<br />• <b>Organizing</b> the way people work")),
        col(sub("Maslow's hierarchy of needs"),
            box("From the base: <b>physiological → safety → social → esteem → self-realization (self-actualization)</b>.<br /><br />"
                "Managers can usually assume physiological and safety needs are met, so <b>social, esteem and self-realization</b> matter most. "
                "If a lower need stays unmet for a long time, a person temporarily drops back to focus on it until it is satisfied again."))),
    qa("How to satisfy each need at work", "need satisfaction", None,
       table(["Need", "What the manager can do"], [
           ["Social", "Communal facilities (shared spaces, break rooms, collaborative zones); allow informal communication (casual chats, lunch)"],
           ["Esteem", "Recognize achievements; appropriate rewards (bonuses, promotions, certificates, symbolic gestures)"],
           ["Self-realization", "Training, because people want to learn more; responsibility, empowering people to make decisions"]])),
    qa("Personality types", "balance all three",
       "The needs hierarchy is almost certainly an over-simplification; motivation also depends on personality type.",
       table(["Type", "Motivated by"], [
           ["<b>Task-oriented</b>", "The work itself"],
           ["<b>Self-oriented</b>", "Personal goals; the work is a means to an end (get rich, buy a house, travel)"],
           ["<b>Interaction-oriented</b>", "The presence and actions of co-workers; they like going to work"]]),
       box("<b>Motivation balance:</b> each person's motivation mixes all three, and the balance shifts with personal circumstances and "
           "external events. People are also motivated by belonging to a group and culture, and by the people they work with.", style="margin-top: 14px"),
       accent="accent-2"),
))

S.append(sec("groups", "§ 07 — GROUPS", "Composition, cohesiveness and communication",
    "Most software engineering is a group activity: non-trivial schedules can't be met by one person, and group interaction is a key "
    "determinant of performance. Managers have limited flexibility and must do their best with the people available.",
    two(col(sub("Where a developer's time goes"),
            box("Time splits between <b>working alone</b>, <b>interaction with other people</b> and <b>non-productive activities</b>, so "
                "interaction is a large part of the job, not an interruption to it."),
            sub("Group composition"),
            box("A group whose members share the same motivation is a problem:<br />• all <b>task-oriented</b>: everyone does their own thing<br />"
                "• all <b>self-oriented</b>: everyone wants to be the boss<br />• all <b>interaction-oriented</b>: too much chatting, not enough work<br /><br />"
                "An effective group <b>balances all three</b>, which is hard because most engineers are task-oriented.")),
        col(sub("Group leadership"),
            box("• Leadership depends on <b>respect, not titular status</b> (holding a title)<br />"
                "• There may be both a <b>technical</b> and an <b>administrative</b> leader<br />"
                "• <b>Democratic leadership is more effective than autocratic</b><br />"
                "• Support a career path based on technical competence"),
            sub("Group organization"),
            box("Keep groups small: <b>under 10</b>, ideally under seven. Break big projects into smaller ones. Small teams can be informal "
                "and democratic; chief programmer teams try to make the best use of skills and experience."))),
    qa("Cohesiveness, and its dark side", "groupthink",
       "In a cohesive group, members put the group ahead of any individual in it.",
       two(col(sub("Advantages"),
               box("• Group quality standards can be developed<br />• Members work closely, so inhibitions caused by ignorance shrink<br />"
                   "• Members learn from each other and know each other's work<br />"
                   "• <b>Egoless programming</b>: members improve each other's programs")),
           col(sub("Developing cohesiveness"),
               box("Influenced by organizational culture and the personalities in the group. Encourage it with social events (team outings), "
                   "a group identity and territory, explicit team building, and <b>openness with information</b>."))),
       box("<b>Group loyalty and groupthink:</b> members are loyal to cohesive groups. Groupthink is preserving the group regardless of "
           "technical or organizational considerations; management should prevent it by <b>forcing external involvement</b> with each group.",
           style="margin-top: 14px"),
       accent="accent-2"),
    box("<b>Group communications</b> carry work status, design decisions and changes to earlier decisions, and they strengthen cohesion. "
        "They are affected by: the <b>status</b> of members (higher-status people dominate), <b>personalities</b> (too many of one type is a "
        "problem) and <b>channels</b> (routing everything through a central coordinator tends to be ineffective).", style="margin-top: 18px"),
))

S.append(sec("staff", "§ 08 — CHOOSING PEOPLE AND THE WORKPLACE", "Selection, environment and how you see people",
    None,
    two(col(sub("Choosing and keeping people"),
            box("Choosing people is a major managerial responsibility. Decisions usually rest on: information from the candidate (resume or CV), "
                "the interview, interviews with potential co-workers, and recommendations from people who know the candidate. Some companies "
                "use psychological or aptitude tests, but <b>there is no agreement that they are useful</b>.")),
        col(sub("Working environments"),
            box("The physical workplace affects productivity and satisfaction: <b>comfort, privacy, facilities</b>, plus health and safety "
                "(lighting, heating, furniture).<br /><br />"
                "<b>Environmental factors:</b> privacy (an area for uninterrupted work), outside awareness (people prefer natural light), "
                "personalization (people organize their space differently).<br /><br />"
                "<b>Workspace organization:</b> private spaces without interruption (individual offices raise productivity), plus shared space "
                "for formal and informal meetings."))),
    qa("Staff selection factors", "Sommerville table", None,
       table(["Factor", "Why it matters"], [
           ["Application domain experience", "Developers must understand the domain to build a successful system"],
           ["Platform experience", "Significant if low-level programming is involved; otherwise not usually critical"],
           ["Programming language experience", "Mainly matters on short projects with no time to learn a new language"],
           ["Problem-solving ability", "Essential: engineers constantly solve technical problems"],
           ["Educational background", "Indicates fundamentals and ability to learn; matters less as experience grows"],
           ["Communication ability", "Engineers must communicate with colleagues, managers and customers"],
           ["Adaptability", "Judged from varied experience; shows the ability to learn"],
           ["Attitude", "A positive attitude to the work and a willingness to learn new skills"],
           ["Personality", "Hard to assess, but people must be able to work well in a team"]])),
    qa("“Human resources” is the wrong frame", "collaborators, not resources",
       "The phrase comes from economics and corporate assets, which creates two problems: people are treated like inanimate resources "
       "(“maximize the ROI in human capital”), and as uniform, interchangeable and expendable.",
       box("Instead, treat team members as <b>collaborators, stakeholders and teammates</b>: recognize and nurture individual talent, and foster "
           "psychological safety and cohesion."), accent="accent-2"),
))

S.append(sec("pmskills", "§ 09 — THE PROJECT MANAGER'S PEOPLE SKILLS", "Five areas a PM has to develop",
    "Interpersonal skills · shaping project culture · managing people · making people better · leadership.",
    qa("Interpersonal skills", "communicate, influence, motivate", None,
       table(["Skill", "What it means"], [
           ["Effective communication", "Follows a defined protocol (status reports, stand-ups, escalation paths), reaches everyone on time, "
            "gives all the information needed, no more and no less"],
           ["Influencing the organization", "Getting the project done depends on respect for the PM; influence, negotiate, build credibility"],
           ["Leadership", "One of the most misunderstood concepts; it is not the same as authority"],
           ["Motivation", "Incentives to act in the project's interest; <b>financial incentives are among the least effective</b> motivators"],
           ["Negotiation and conflict management", "Reaching agreement and overcoming differences; consensus and defusing conflict"],
           ["Problem solving", "Recognize and define problems, then evaluate and decide on solutions; it can be learned with practice"]])),
    two(col(sub("Shaping project culture"),
            box("Shape the project culture inside the organization's culture. Understand the organization's attitude to the project and to "
                "project management (some embrace structured methods, others are ad hoc; real practice differs from “fanciful” practice). "
                "Understand each member's engineering and personal background."),
            box("<b>Cultural roles:</b> leader, listener/talker, complainer/naysayer, expert, charger/plodder.<br />"
                "<b>Project roles:</b> project manager (plans and tracks), team leader (builds the team), development leader (produces a "
                "superior product).<br />Remain <b>non-judgmental</b>: every cultural role has value.", style="margin-top: 10px")),
        col(sub("Monitor culture like a technical issue"),
            box("• Make each person's role clear<br />• Understand each personality and say so positively<br />"
                "• State and keep your view of the team (“we are all equals, but in a crisis I decide”)<br />"
                "• Spot cultural role problems early (a dominant voice, a skeptic undermining morale)<br />"
                "• Monitor role satisfaction, especially at launch when roles change easily<br />"
                "• Check <b>task-to-people fit</b>: mismatches cause problems and schedule slip<br />"
                "• Watch the overall climate by listening to each member"),
            sub("Project environment"),
            box("Social and cultural factors (economic, educational, ethical, ethnic, religious) can affect the PM's authority. International and "
                "political factors matter as projects globalize, as do mundane ones: time zones, holidays, travel, teleconferencing."))),
))

S.append(sec("manage", "§ 10 — MANAGING AND GROWING PEOPLE", "The problems are sociological, not technological",
    "Most technical managers manage as if solving an engineering problem, and ignore individual quirks that can make or break a project "
    "(optional reading: <i>Peopleware</i>).",
    two(col(sub("Guidelines for managing people"),
            box("• <b>Gain visibility without micromanagement</b><br />"
                "• <b>Review process and products, not people</b>: “This testing regime lets too many bugs through; what can we do?”, not "
                "“You don't know how to write unit tests.”<br />"
                "• <b>Coordinate, don't manipulate</b>: use knowledge, not position<br />"
                "• <b>Channel people, don't dam them</b>: redirect misplaced effort, don't cut it off<br />"
                "• <b>Focus on project and people needs</b>, not your authority")),
        col(sub("How NOT to manage thought workers"),
            box("Applying production-line efficiency to thought workers is a sign of disaster:<br />"
                "• squeeze out error so the “machine” runs smoothly<br />"
                "• take a hard line on “goofing off” (creative people need time to reflect)<br />"
                "• treat workers as interchangeable parts<br />• optimize the steady state, ignore start-up and shut-down<br />"
                "• standardize procedure, run by the book<br />• eliminate experimentation"))),
    qa("Making people better", "professional development", None,
       box("Make professional development a <b>project goal</b>. Separate <b>short-term</b> goals (skills for this project) from <b>long-term</b> "
           "goals (future projects), and let each person set personal goals, using a competency framework (technical, leadership, domain, "
           "personal, communication, management)."),
       box("For a fixed period, have members <b>track their time in detail</b> (reading, writing, meetings, training, requirements, design, coding, "
           "testing, e-mail, phone). It goes beyond a weekly timesheet and is for <b>awareness, not monitoring</b>. The formal version is the "
           "<b>Personal Software Process (PSP)</b>, which teaches developers to manage quality, make commitments they can meet, improve "
           "estimating and planning, and reduce defects.", style="margin-top: 10px")),
))

S.append(sec("leadership", "§ 11 — LEADERSHIP AND CONSENSUS", "Mobilize the group, don't just command it",
    "Leadership is the capacity to mobilize a group to solve its most challenging problems; it is wrong to think it is about authority.",
    table(["", "Technical leadership", "Adaptive leadership"], [
        ["When", "The problem can be solved by known means", "The problem cannot be solved by known means (complex or novel)"],
        ["Approach", "The leader directs, instructs and applies best practices", "Learning for leader and group; leading with good questions"],
        ["Vision", "The leader's personal vision drives the team (“Here's what I see for us”)", "A shared sense of purpose (“Why does this matter?”)"],
        ["Motivation comes from", "Charisma, expertise, confidence, decisiveness", "Learning, iteration and visible movement toward clarity"]]),
    box("Choose based on whether the problem can be solved by known means. Most IT projects mix known and unknown problems, and an "
        "<b>adaptive leader can handle known problems by delegating</b> them to someone who can lead with known means.", style="margin-top: 14px"),
    two(col(sub("Working toward consensus"),
            box("Consensus means general agreement, but in a team it means <b>everyone feels heard</b> and the group moves forward with shared "
                "commitment, not that everyone agrees. Seek it on all decisions affecting the team: simple majority rule can hurt a small team "
                "where everyone's commitment matters. Leaders curate the debate, highlighting valid arguments and constructively disqualifying invalid ones."),
            box("<b>Steps:</b> 1) pose the problem · 2) solicit options · 3) discuss pros and cons · 4) work toward the most beneficial option · "
                "5) help opponents buy in: persuade, don't dictate.<br />Consensus takes longer than a mandate but pays off hugely. "
                "<b>Beware passive-aggressive agreement</b>: it is buried conflict.", style="margin-top: 10px")),
        col(sub("Leading people (a reprise of trust)"),
            box("• Be confident in yourself and the team<br />• Keep communication open<br />• Be fallible<br />• Lead by example<br />"
                "• Use all the talents of the team: you can't succeed alone<br />• Meet commitments, or explain early<br />"
                "• Don't confuse friendship with leadership"),
            sub("Key points"),
            box("Managers need to understand human factors to avoid unrealistic demands. Selection factors include education, domain experience, "
                "adaptability and personality. Groups should be small and cohesive; their communication depends on status, size, composition and "
                "organization. The working environment strongly affects productivity. Monitor project culture and technical status early and continuously."))),
))

S.append(cheat([
    ["Team needs pyramid", "Trust → managed conflict → commitment → accountability → results"],
    ["Tuckman", "Forming → storming → norming → performing → adjourning"],
    ["Team objectives", "Problem resolution · creativity · tactical execution"],
    ["Influence types", "Authority · reward · punishment · expert · referent"],
    ["Conflict techniques", "Confronting (problem solving) · compromising · withdrawal · smoothing · collaborating · forcing"],
    ["Commitment", "Clarity + buy-in; buy-in does not require consensus"],
    ["RACI", "Responsible (does) · Accountable (one owner) · Consulted · Informed (+ Support in RASCI)"],
    ["Communication paths", "n(n − 1) / 2; teams under 10, optimal 4–6 developers"],
    ["Team models", "Business (most common) · democratic · agile/XP · chief programmer · skunk works · SWAT · large (hierarchy)"],
    ["Maslow", "Physiological → safety → social → esteem → self-realization; managers focus on the top three"],
    ["Personality types", "Task-, self- and interaction-oriented; an effective group balances all three"],
    ["Management activities", "Problem solving · motivating · planning · estimating · controlling · organizing"],
    ["Groupthink", "Preserving the group over technical sense; prevent with external involvement"],
    ["Technical vs adaptive", "Known means, leader directs vs no known solution, leader asks questions and mobilizes learning"],
    ["Consensus steps", "Pose · solicit · discuss pros/cons · work toward best · help opponents buy in"],
]))

S.append(mistakes([
    ("Buy-in vs consensus", "“A team can only commit when everyone agrees.”", "Buy-in does not require consensus: members can disagree and still commit because they were heard."),
    ("Responsible vs Accountable", "“Several people can be Accountable for a task.”", "Exactly one Accountable owner; several people can be Responsible for doing the work."),
    ("Disagreement vs conflict", "Treating every disagreement as conflict to be avoided.", "Conflict is a hardening of positions; healthy disagreement is debate the team needs. Avoiding it leads to groupthink."),
    ("Communication paths", "Paths grow linearly: 10 people means 10 paths.", "n(n − 1) / 2: 10 people means 45 paths, 50 people about 1,225."),
    ("Leadership = authority", "“The leader is whoever has the title.”", "Leadership is the capacity to mobilize a group; it depends on respect, not titular status."),
    ("Motivating with money", "“Bonuses are the best motivator.”", "Studies show financial incentives are among the least effective; social, esteem and self-realization needs matter most."),
    ("Cohesive is always good", "“A more cohesive group is always better.”", "Cohesion brings quality standards and learning, but also groupthink, which management must counter."),
    ("Chief programmer risk", "“A chief programmer team removes risk by relying on the best person.”", "It adds risk: the project fails if both the chief and the backup are unavailable."),
]))

S.append(quiz([
    ("Order the team needs pyramid from the base.", "<b>Trust → managed conflict → commitment → accountability → results.</b> Lower levels must be satisfied first."),
    ("What does vulnerability-based trust mean?", "Being comfortable admitting mistakes, asking for help and saying “I don't know”."),
    ("Name the six conflict resolution techniques.", "Confronting (problem solving), compromising, withdrawal (avoidance), smoothing (accommodating), collaborating, forcing."),
    ("What two things does commitment require?", "<b>Clarity</b> (everyone knows what was decided and why) and <b>buy-in</b> (support even without full agreement)."),
    ("What is the difference between a RAM and a skills matrix?", "A RAM maps people to tasks (who does what); a skills matrix maps people to skills."),
    ("Give one pro and one con of a skunk works team.", "Pro: high ownership and buy-in. Con: little visibility into progress."),
    ("How many communication paths in a team of 7?", "7 × 6 / 2 = <b>21</b>."),
    ("Which three needs matter most to a manager, and why?", "Social, esteem and self-realization, because physiological and safety needs can usually be assumed met."),
    ("What goes wrong if everyone in a group is self-oriented?", "Everyone wants to be the boss."),
    ("What is groupthink, and how should management prevent it?", "Preserving the group regardless of technical or organizational sense; force external involvement with the group."),
    ("When is adaptive leadership needed instead of technical leadership?", "When the problem can't be solved by known means (complex or novel); the leader frames questions and mobilizes learning."),
    ("What is the Personal Software Process (PSP) for?", "Tracking your own time and work to manage quality, make realistic commitments, improve estimates and reduce defects."),
]))

SECTIONS = S

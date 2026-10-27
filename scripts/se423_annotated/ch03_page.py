"""SE423 Chapter 3 (Team): page content.

Schema: see annotated_page.py. Marks on pictures use 'ocr' (skipped if OCR can't read them).
Past-exam questions are copied from the papers in exams/ and the instructor's 2026 midterm (m261); everything
else is a prediction.
"""
from .common import asked, likely

TITLE = 'Team'
CHAPTER = 'SE423 · Chapter 3'

OVERVIEW = {
    'summary': ('The most examined chapter in SE423: both 251 midterms took most of their short questions from it, and both '
                'finals have a whole team-based collaboration question. It has three parts. Team development: Tuckman’s stages, '
                'team objectives and structures, and the team needs pyramid (trust → managed conflict → commitment → '
                'accountability → results) with RACI and skills matrices as the accountability tools. Team models: business, '
                'democratic, chief-programmer, skunk works, SWAT, and why large teams need hierarchy (n(n−1)/2 channels). '
                'Managing people: motivation and personality types, cohesiveness and groupthink, staff selection, working '
                'environments, shaping project culture, technical vs. adaptive leadership, and reaching consensus.\n\n'
                'The instructor’s style: questions ask you to apply an idea to a team situation (“team members disagree: how do '
                'you encourage collaboration?”). Saying one word (“negotiation”) is not enough; explain what you do, how, and why.'),
    'ideas': [
        ('Team pyramid', 'Trust → managed conflict → commitment → accountability → results. Each layer needs the one below; trust is the foundation.'),
        ('Tuckman', 'Forming → storming (competing for leadership) → norming (agree how to work) → performing → adjourning.'),
        ('RACI', 'R does the work, A owns the outcome (exactly one per task), C gives input (two-way), I is kept updated (one-way).'),
        ('Team models', 'Business (tech lead + equals, most common), democratic (whole team decides), chief-programmer (surgical), skunk works, SWAT.'),
        ('Leadership', 'Technical leadership for problems solvable by known means; adaptive leadership for new or complex ones. Most IT projects need both.'),
        ('Consensus', 'Not unanimous agreement: everyone feels heard and the group moves forward committed. Persuade, don’t dictate.'),
    ],
    'sections': [
        ('Slides 1–9', 'Team development: influence, the pyramid, Tuckman, team objectives'),
        ('Slides 10–24', 'The pyramid layer by layer: trust, conflict, commitment, accountability (RACI, RAM, skills matrix), results'),
        ('Slides 25–34', 'Team models and team size'),
        ('Slides 35–56', 'Managing people: motivation, personality types, cohesiveness, communication, selection, environment'),
        ('Slides 57–70', 'Project culture, managing thought workers, making people better'),
        ('Slides 71–77', 'Leadership, consensus and key points'),
    ],
    'exam': ('Midterm 251 (both versions): MCQs on Tuckman’s storming stage, the foundation of teamwork and the advantage of a '
             'cohesive team; short questions on good-team characteristics, vulnerability-based trust, healthy conflict, the best '
             'time to reinforce accountability, business vs. democratic teams, technical vs. adaptive leadership and a RACI table; '
             'a case on accountability after an untested release. Finals: commitment, trust and conflict, accountability and '
             'transparency (Final 242 Q5), the communication-channel formula (Final 242), a CI/CD consensus decision and a '
             'milestone celebration (Final 251 Q5). The instructor’s 2026 midterm asked how a PM encourages collaboration when '
             'members disagree.'),
}

TITLES = {9: 'Team Structure', 35: 'Managing People', 57: 'Our perspective about the team members', 63: 'Project environments (context: project culture)',
          70: 'Making People Better', 72: 'Technical vs. adaptive leadership'}

SLIDES = {
    1: dict(
        hl=[('SE423: Software Project Management', 1)],
        notes=['The deck has three parts: **team development** and the team needs pyramid (slides 3–24), **team models** (25–34) and **managing people** (35–77). The pyramid (trust → conflict → commitment → accountability → results) is the spine of the chapter and of most exam questions on it.']),
    2: dict(
        hl=[('Team Development', 1), ('Building Trust', 2), ('Embracing Accountability', 2), ('Team Models', 3), ('Managing People', 3)],
        notes=['**Team development** first: how a group becomes a team.',
               'Then three of the pyramid layers in order: **building trust**, **managing conflict**, **embracing accountability** (commitment and results are covered between them).',
               'Then the **team models** (how teams are organized) and **managing people** (motivation, selection, culture, leadership).']),
    3: dict(notes=['Section divider: **Team Development**.']),
    4: dict(
        hl=[('responsibilities as a team member', 1), ('Project Triangle', 2), ('individual team members', 3), ('characteristics of a good team', 4)],
        notes=['Discussion questions to open the topic. As a **team member** you own your tasks and support others; as a **PM** you build the conditions for the team to work: clear goals, roles, trust.',
               'The link to the **project triangle**: a weak team costs you on scope, schedule or cost. People are the resource that turns the plan into results.',
               'Individuals vs. team: a team of strong individuals who don’t trust each other usually loses to a well-functioning team of average people. Team strength wins.',
               '“Characteristics of a good team” was a real midterm short question. Answer it with the pyramid, from the bottom up.'],
        exam=[asked('m251v1', 'Short Q1', 'What are key characteristics of a good team?',
                    a='Members trust each other (the foundation), so they speak openly and admit mistakes; they have healthy conflict about ideas rather than people; they commit to decisions with clarity and buy-in; they hold each other accountable; and they put team results ahead of individual credit. A good team also shares a clear goal with clear roles, communicates openly, is cohesive, balances personality types and is the right size (about 4–6 developers plus a lead).')]),
    5: dict(
        hl=[('lacks the knowledge', 1), ('lacks the resolve', 2)],
        notes=['McConnell’s two reasons projects fail. **Knowledge**: the team doesn’t know how to run a software project. Training, hiring and process fix this.',
               '**Resolve** (determination, commitment, mental toughness): the team knows how but doesn’t push through. This is what team building, motivation and leadership fix, and it is what the rest of the chapter is about.']),
    6: dict(
        hl=[('Authority granted by', 1), ('ability to offer', 2), ('the threat or use of', 3), ('specialized', 4), ('personal traits,', 5)],
        notes=['The **types of influence** a PM can use. **Formal (legitimate)**: authority granted by the organizational hierarchy or role. The skills table above lists the PM’s team skills (planning, negotiation, hiring, risk management, judgement) and the bottom table lists leadership styles (directing, facilitating, coaching, supporting, etc.).',
               '**Reward**: influence through the ability to offer incentives (bonuses, interesting assignments).',
               '**Penalty (coercive)**: influence through the threat or use of punishment. It gets compliance, not commitment.',
               '**Expert**: influence based on specialized knowledge or skills.',
               '**Referent**: influence based on personal traits, charisma or likability. Formal, reward and penalty come from your **position**; expert and referent come from **you**, and they last longer because people choose to follow.'],
        exam=[likely('A senior developer persuades the team because everyone respects her deep database knowledge. This is:', a=0,
                     opts=['Expert influence', 'Formal influence', 'Reward influence', 'Penalty influence']),
              likely('Which types of influence come from the person rather than from the position?', a=0,
                     opts=['Expert and referent', 'Formal and reward', 'Reward and penalty', 'Formal and penalty'])]),
    7: dict(
        hl=[('Lower level needs must be satisfied', 1), ('Trust', 2, 0, 'ocr'), ('Managed Conflict', 2, 0, 'ocr'), ('Results', 3, 0, 'ocr')],
        notes=['The rule from Maslow: **lower-level needs must be satisfied before higher ones** can be addressed. On the left is Maslow’s individual pyramid; on the right the **team needs pyramid** (Lencioni).',
               'The team pyramid from the bottom: **trust**, then **managed conflict**, then **commitment**, then **accountability**, then **results**. You can’t have healthy conflict without trust, or commitment without having debated the decision.',
               '**Results** sit at the top: the team’s collective goals. The ticks on the slide show a team that has secured trust and conflict but is stuck at commitment, so the PM works on that layer next.'],
        exam=[asked('m251v1', 'MCQ 8 (also V2 MCQ 8)', 'Which of the following is considered the foundation of teamwork?', a=1,
                    opts=['Accountability', 'Trust', 'Commitment', 'Consensus'],
                    why='Trust is the base of the team pyramid: trust, managed conflict, commitment, accountability, results.'),
              likely('In the team needs pyramid, which layer sits directly above trust?', a=0,
                     opts=['Managed conflict', 'Commitment', 'Results', 'Accountability'])]),
    8: dict(
        hl=[('Forming', 1), ('Storming', 2), ('competing for leadership', 2), ('Norming', 3), ('Performing', 4), ('Dissolving/Adjourning', 5)],
        notes=['**Tuckman’s model**. **Forming**: the group comes together and members get to know each other; they are polite and depend on the leader.',
               '**Storming**: a chaotic competing for leadership and trials of group processes; members compete for influence or control, often without clear structure or authority. The PM’s job here is to surface and manage the conflict, not suppress it.',
               '**Norming**: agreement is reached on how the group operates (roles, norms, ways of working).',
               '**Performing**: the group practices its craft and becomes effective at meeting its objectives.',
               '**Adjourning**: the team dissolves at the end of the project. Order: form → storm → norm → perform → adjourn.'],
        exam=[asked('m251v1', 'MCQ 7 (also V2 MCQ 7)', 'According to Tuckman’s model of team development, which stage is characterized by members competing for leadership and struggling with group processes?',
                    a=0, opts=['Storming', 'Norming', 'Adjourning', 'Performing'],
                    why='Storming is when members compete for leadership and test group processes; norming comes after, when agreement is reached.'),
              likely('The stage where the team reaches agreement on how it will operate is:', a=0,
                     opts=['Norming', 'Forming', 'Storming', 'Performing'])]),
    9: dict(
        hl=[('Problem resolution', 1), ('temporary task force', 1, 1), ('Creativity', 2), ('Looser hierarchy', 2), ('Tactical execution', 3), ('tight', 3)],
        notes=['The team’s **objective** shapes its structure. **Problem resolution**: a complex, poorly defined problem focused on 1–3 issues (e.g. a showstopper defect). Traits: urgency and pressure. Structure: flexible roles, rapid decision-making, possibly a **temporary task force**.',
               '**Creativity**: new product development, generating new ideas. Traits: divergent thinking, experimentation, tolerance of ambiguity. Structure: **looser hierarchy**, diverse skills, a culture that supports risk-taking.',
               '**Tactical execution**: carrying out a well-defined plan. Traits: clear roles, timelines, coordination, accountability. Structure: hierarchical or matrix with **tight controls** and performance tracking. (The instructor noted she spent time explaining this slide.)'],
        exam=[asked('m251v1', 'Case Q4 (also V2)', 'As the project manager, you must establish the team structure for this project. What team structure would you create to ensure smooth development, stakeholder engagement, and integration with Edugate, and why?',
                    a='A cross-functional Agile team: a Project Manager, a Product Owner from Edugate/IT, developers, a UI/UX designer, QA testers, a faculty advisor representative and a student representative (1.0). This puts every stakeholder’s voice inside the team, balances usability against compliance, and supports iterative delivery (0.5).'),
              likely('A team must roll out an already-designed module on a fixed timeline. Which objective type and structure fit?',
                     a='Tactical execution: carrying out a well-defined plan. Use a hierarchical or matrix structure with clear roles, tight controls and performance tracking, because the work is known and the risk is in coordination and deadlines, not in discovering what to build.')]),
    10: dict(notes=['Section divider: **Building Trust**, the base of the pyramid.']),
    11: dict(
        hl=[('Trust is the foundation of teamwork', 1), ('Admitting mistakes, Asking for help, Saying', 2), ('Takes time', 3), ('Needs to be maintained over time', 3), ('Behavioral profiling', 4)],
        notes=['**Trust is the foundation of teamwork**: without it teams struggle to collaborate, share ideas or resolve conflict.',
               'Trust is about **vulnerability**. **Vulnerability-based trust** means admitting mistakes, asking for help and saying “I don’t know” without fear it will be used against you. This list was a real midterm question.',
               'It **takes time** (consistent behavior, follow-through on commitments, shared experiences under pressure) and must be **maintained**: one broken promise can undo months.',
               'A technique: **behavioral profiling** (e.g. Myers-Briggs) helps people admit strengths and weaknesses openly; the PM can adjust assignments to match strengths and create a psychologically safe space.'],
        exam=[asked('m251v1', 'Short Q2 (also V2 Short Q1)', 'What does vulnerability-based trust involve?',
                    a='Team members are comfortable being open with each other: admitting mistakes and weaknesses, asking for help, and saying “I don’t know”, without fear that it will be used against them. It takes time to build through consistent behavior, follow-through and shared experiences under pressure, must be maintained, and is the foundation of the team pyramid.'),
              asked('f242', 'Q5.2', 'How does fostering trust and managing conflict within a software project team contribute to improved collaboration and project success?',
                    a='Trust lets members admit mistakes, share information and ask for help, so problems surface early and people cooperate instead of protecting themselves. Managed (healthy) conflict means ideas are debated openly and respectfully, which gives better technical decisions and avoids groupthink or disputes that turn personal. Together they lead to real commitment and collaboration, which drives quality and project success.')]),
    12: dict(
        hl=[('earned, not granted', 1), ('open communication', 2), ('Be fallible', 3), ('Lead by example', 4), ('Complete all your commitments on time', 5), ('confuse friendship with leadership', 6)],
        notes=['Trust is **earned, not granted**: a title doesn’t make people trust you, and most people are naturally wary of others.',
               'Keep **open communication**: communication barriers are project risks because problems stay hidden.',
               '**Be fallible**: own your mistakes, correct them and explain how you’ll avoid them in future. This models the vulnerability you want from the team.',
               '**Lead by example**, not by mandate: show the standard you expect.',
               'Keep **commitments**; if you can’t, give notice and an explanation, not an excuse.',
               '**Friendship ≠ leadership**: warmth helps, but leading needs clarity and boundaries (repeated on slide 76).'],
        exam=[likely('Which behavior does the slide recommend for establishing trust?', a=0,
                     opts=['Admit mistakes and explain how you will avoid them', 'Hide mistakes to protect your authority', 'Lead by mandate', 'Give excuses when commitments slip'])]),
    13: dict(notes=['Section divider: **Managing Conflict**, the second layer.']),
    14: dict(
        hl=[('unfiltered, passionate debate', 1), ('uncomfortable', 2), ('rules of engagement', 3), ('groupthink', 4), ('dissent', 4)],
        notes=['**Healthy conflict** is unfiltered, passionate debate around **issues**, not people, and it requires trust underneath.',
               'Even in the best teams it will sometimes be **uncomfortable**; that is normal, not a sign of failure.',
               '**Conflict norms** are the team’s **rules of engagement** (tone, language, timing, emotional expression); they differ per team and must be discussed and made explicit.',
               '**Avoidance is costly**: teams that fear conflict fall into **groupthink** (harmony over critical thinking), suppress dissent and make poor decisions nobody challenged.'],
        exam=[asked('m251v1', 'Short Q3 (also V2 Short Q3)', 'Why is healthy conflict important in teams?',
                    a='Healthy conflict is open debate about ideas, not people. It brings out different perspectives so the team makes better decisions, avoids groupthink and artificial harmony, and surfaces problems early. Because everyone has been heard, members are more willing to commit to the final decision even if they disagreed. It needs trust underneath and agreed conflict norms.'),
              likely('A team values harmony so much that it stops critically evaluating ideas. This is:', a=0,
                     opts=['Groupthink', 'Storming', 'Healthy conflict', 'Accountability'])]),
    15: dict(
        hl=[('Confronting (Problem Solving)', 1), ('Compromising', 2), ('Withdrawal (Avoidance)', 3), ('Smoothing (Accommodating)', 3), ('Collaborating', 4), ('Forcing', 5), ('Define the real/root problem', 6)],
        notes=['**Confronting (problem solving)**: resolve the root cause through open, honest dialogue. Gives the most lasting result.',
               '**Compromising**: both sides give something up to reach a middle ground. Quick, but nobody gets what they needed.',
               '**Withdrawal** delays or sidesteps the conflict; **smoothing** keeps harmony by downplaying differences. Both leave the cause in place.',
               '**Collaborating**: integrate multiple perspectives into a creative solution. With confronting, the preferred approach for a team.',
               '**Forcing**: impose a solution through authority or pressure. Fast in an emergency, but it costs buy-in.',
               'The **problem-solving steps**: define the real/root problem → analyze it → identify solutions → pick one → implement it → review that it solved the problem.'],
        exam=[asked('m261', 'Short', 'Team members disagree about the best solution to a problem. How can the project manager encourage collaboration? (Saying “negotiation” alone is not enough: explain.)',
                    a='Treat it as healthy conflict and use collaborating/confronting (problem solving) rather than forcing or smoothing. Bring the people together for an open discussion focused on the problem, not on people; define the real problem and agree the criteria for a good solution; ask each person to present their option with its reasoning and data; weigh the pros and cons of each option together; then converge on the option that best serves the project, or combine ideas into a better one. Work with those who preferred other options so they buy in. This gives a better decision and real commitment because everyone was heard.'),
              likely('A PM ends a debate by declaring “we use my design, end of discussion.” Which technique is this?', a=0,
                     opts=['Forcing', 'Smoothing', 'Compromising', 'Confronting'])]),
    16: dict(
        hl=[('successful teams resolve', 1), ('Disagreement is not the same as', 2), ('hardening of position', 2), ('neutral stance', 3), ('role of conciliator', 3), ('reconciliation', 4)],
        notes=['Every team meets conflict: successful teams **resolve** it, unsuccessful ones push it into the background where it festers.',
               '**Disagreement ≠ conflict**. A disagreement is about an idea; a conflict involves a **hardening of position** and intractability (nobody will move). Almost every conflict traces back to a clash between two parties.',
               'Those outside the conflict stay **neutral**, even if they agree with one side, and one of them acts as **conciliator**, mediating to defuse the situation. The goal is to reduce the conflict back to a disagreement that can be settled by consensus.',
               'Finally, aim for **reconciliation** between the two parties so the working relationship survives.'],
        exam=[likely('Disagreement and conflict are the same thing.', tf=False, why='Conflict involves a hardening of position and intractability; the goal is to reduce it back to a disagreement.')]),
    17: dict(
        hl=[('clarity & buy-in', 1), ('Clarity ensures everyone knows', 2), ('Buy-in means', 3), ('avoid assumptions and ambiguity', 2), ('Buy-in does not require consensus', 4)],
        notes=['**Commitment** (the third layer) requires **clarity and buy-in**.',
               '**Clarity**: everyone knows exactly what was decided, why it matters and what is expected next. Teams avoid assumptions and ambiguity and end each discussion with an explicit decision.',
               '**Buy-in**: members support the decision even if they didn’t fully agree, because they trust the process and felt heard (this is why healthy conflict comes first).',
               '**Buy-in does not require consensus**: great teams can disagree and still commit (“disagree and commit”). A common trap: “commitment requires everyone to agree” is false.'],
        exam=[asked('f242', 'Q5.1', 'In the context of the Team Needs Pyramid, explain how a project manager can foster commitment among team members.',
                    a='In the pyramid (trust → managed conflict → commitment → accountability → results), commitment sits on trust and healthy conflict: people commit when they trust each other and have had their say. The PM fosters it with clarity (clear decisions, goals, roles and deadlines, confirmed at the end of each meeting, with no assumptions) and buy-in (letting everyone voice their views so they support the decision even if they disagreed; consensus isn’t required). Recording decisions and owners (e.g. in a RACI) then lets commitment be followed by accountability.'),
              likely('Team buy-in requires that every member agrees with the decision.', tf=False, why='Buy-in does not require consensus.')]),
    18: dict(notes=['Section divider: **Embracing Accountability**, the fourth layer.']),
    19: dict(
        hl=[('directly among peers', 1), ('willingness to confront accountability', 2), ('Best opportunity occurs during meetings', 3), ('We committed to five stories but completed three', 3)],
        notes=['On a strong team accountability happens **directly among peers**: members hold each other to standards instead of waiting for the manager.',
               'The leader must show a **willingness to confront accountability**: be transparent, follow through, and address underperformance respectfully but firmly. If the PM avoids it, so will the team.',
               'The **best opportunity** is during **meetings and regular reviews** of accomplishments, e.g. at a sprint review: “We committed to five stories but completed three. Let’s explore what happened and how we can improve.” Note the tone: about the commitment, not blaming a person.'],
        exam=[asked('m251v2', 'Short Q2', 'What’s the best time to reinforce accountability?',
                    a='During meetings and regular reviews of accomplishments, such as sprint reviews and status meetings, where what was committed is compared with what was done (e.g. “we committed to five stories but completed three; let’s explore why”). Make commitments clear and public at the start and address a missed commitment when it happens rather than waiting for the end of the project, so peers hold each other accountable continuously.'),
              asked('m251v1', 'Case Q1 (also V2)', 'During a sprint deployment, a key feature was discovered to be not thoroughly tested and caused issues after release. As the project manager, what steps would you follow to address this issue and ensure accountability within the team?',
                    a='Use a RACI matrix to establish who was Responsible, Accountable, Consulted and Informed for testing that feature (0.5). Hold a retrospective to find the root cause (0.25). Make the responsible roles clear without blaming individuals (0.25). Take corrective action: release a hotfix, redistribute tasks, and add automated testing so it can’t recur (0.25). Inform the stakeholders of the recovery plan (0.25).'),
              asked('f242', 'Q5.3', 'Your software project team is experiencing delays due to unclear task ownership and inconsistent updates. As the project manager, how would you apply a team-based approach to improve accountability and transparency within the team? Describe specific steps you would take to enhance collaboration and increase the project’s chances of success.',
                    a='1) Clarify ownership with a RACI matrix so every task has a Responsible person and exactly one Accountable person. 2) Hold short daily stand-ups (done, next, blocked) so updates are consistent. 3) Put all tasks on a shared board (e.g. Jira or Kanban) with visible goals and deadlines so progress is transparent. 4) Review commitments against results in regular reviews, encourage peer accountability, and run retrospectives to fix what caused the delays.')]),
    20: dict(
        hl=[('Responsible, Accountable', 1), ('Support', 2), ('Activity 4', 3, 0, 'ocr')],
        notes=['**RACI**: **R**esponsible does the work; **A**ccountable owns the outcome and signs off (exactly **one** A per activity); **C**onsulted gives input before or during the work (two-way); **I**nformed is kept updated (one-way). Several R’s on one activity are fine.',
               '**Support** (the S in RASCI variants) is not in the original acronym; it marks people who help the Responsible person.',
               'In the example, Activity 4 has the project manager as **RA**: one person can be both Responsible and Accountable for a task they do and own.'],
        exam=[asked('m251v1', 'Short Q6 (V2 asked T2 and T5)', 'Your team has been assigned to develop a mobile app for a local fitness center. The app will allow users to book classes, track workouts, and receive personalized fitness tips. The project is expected to be completed in 8 weeks. Fill in the RACI assignments for T1 and T6 only.',
                    a='These cells come from the instructor’s key. The person who does the work is R (the client representative for requirements, the UI/UX designer for the interface, the lead developer for building and launching, the marketing specialist for promotion). Whoever’s expertise is needed is C, and everyone else is I. The key makes the PM Accountable (A) for requirements and launch, the two tasks that commit the project; on the other tasks the PM is kept Informed.'),
              likely('In RACI, who owns the outcome and signs off on the task?', a=0, opts=['Accountable', 'Responsible', 'Consulted', 'Informed'])]),
    21: dict(
        hl=[('A resource planning tool', 1), ('Who does What', 1), ('both planning and tracking', 2), ('individual, team or department', 3)],
        notes=['A **Responsibility Assignment Matrix (RAM)** is a resource planning tool showing **who does what**; RACI is one kind of RAM.',
               'It is used for both **planning** (assigning work) and **tracking** (checking each task has an owner), and makes authority, accountability and responsibility visible.',
               'The “who” can be an **individual, team or department**, and rows or columns can have totals (e.g. the number of contributors on a task).']),
    22: dict(
        hl=[('RACI – Responsible, Accountable, (Support), Consulted, Informed', 1)],
        notes=['A real RAM: project deliverables grouped by phase (initiate, plan, execute, control, close) down the side, and roles grouped as project leadership, team members, sub-teams and external resources across the top. Each cell holds a RACI letter, so you can read across a row to see who is involved in a deliverable, or down a column to see one role’s workload.']),
    23: dict(
        hl=[('Another resource planning tool', 1), ('Resources on one axis, skills on other', 1), ('high level or very specific', 2), ('numeric', 2)],
        notes=['A **skills matrix** is another resource planning tool: **people on one axis, skills on the other**.',
               'Skills can be high level or very specific (PHP, MySQL, React); cells can be X’s or **numeric** levels (the legend: expert, practitioner, novice). Use it to assign tasks to the right people and to spot gaps, e.g. only one person is an expert in a key technology, which is a key-person risk.'],
        exam=[asked('f242', 'Q2.3', 'You are responsible for managing a diverse team with varying availability and skill sets. Describe two strategies you would use to allocate your team’s resources efficiently across tasks. How would you adjust your resource plan if one hardware specialist becomes unavailable for 4 weeks?',
                    a='1) Build a skills matrix and assign tasks to the people whose skills match, recording owners in a RAM/RACI. 2) Check availability per period and level the workload so nobody is overallocated, using float on non-critical tasks. If the hardware specialist is out for 4 weeks: move their non-critical tasks later within their float, reassign what others can do (using the skills matrix to find the next-best person), bring in a contractor or borrow a specialist for critical work, and update the schedule and inform stakeholders if the critical path moves.')]),
    24: dict(
        hl=[('accomplishes the results', 1), ('prioritize the results of the', 2), ('publicly clarify their desired results', 3)],
        notes=['The top of the pyramid. The true measure of a great team is that it **accomplishes the results** it set out to achieve.',
               'Members must **prioritize team results** over individual or departmental needs (status, credit, their department’s agenda).',
               'To stay focused, the team **publicly clarifies its desired results** and keeps them visible, e.g. sprint goals on the board.']),
    25: dict(notes=['Section divider: **Team Models**, the ways a software team can be organized.']),
    26: dict(
        hl=[('Decentralized/democratic', 1), ('Centralized/autocratic', 1), ('Controlled Decentralized', 2)],
        notes=['The two early philosophies: **decentralized/democratic** (the team decides together) and **centralized/autocratic** (one person decides).',
               'The variation in between, **controlled decentralized**, has a leader who coordinates while sub-groups decide within their own areas.']),
    27: dict(
        hl=[('Business Team', 1), ('Most common model', 1), ('Technical lead + team', 2), ('strong', 2), ('loose hierarchy', 2), ('Democratic Team', 3), ('All decisions made by whole team', 3)],
        notes=['The **business team** is the **most common** model in software and general business.',
               'A **technical lead plus the team** (the others at equal status), hierarchical with one principal contact. It can be a **strong** hierarchy (the lead has clear authority) or a **loose** one (the lead facilitates rather than commands). It is adaptable and general.',
               'The variation, the **democratic team**: all decisions are made by the whole team. Teams often start as a business team and evolve toward democratic as they mature, gain trust and develop shared norms.'],
        exam=[asked('m251v1', 'Short Q4 (also V2 Short Q4)', 'What’s the difference between a Business Team and a Democratic Team?',
                    a='A business team has a technical lead who is the principal contact and makes or facilitates decisions, with the other members at equal status under the lead (a strong or loose hierarchy); it is the most common model. A democratic team acts as a group: decisions are made by consensus, the leader is only the external interface and does not allocate work, tasks are allocated by ability and experience, and it works best with experienced, competent members. Teams often move from business to democratic as trust and norms develop.')]),
    28: dict(
        hl=[('comes to a consensus', 1), ('external interface', 2), ('does', 2), ('ability and experience', 3), ('experienced and competent', 4), ('self-organizing teams', 4)],
        notes=['In a **democratic team** the group acts as a whole and **comes to a consensus** on decisions affecting the system.',
               'The leader is only the **external interface** and does **not** allocate specific work items.',
               'Work is discussed by the whole group and tasks are allocated by **ability and experience**.',
               'It succeeds only when **all members are experienced and competent**; such teams are also called **self-organizing teams** (as in Scrum).']),
    29: dict(
        hl=[('variants of democratic organization', 1), ('delegated to group members', 1), ('Programmers work in pairs', 2), ('collective responsibility', 2)],
        notes=['**Agile groups** are variants of democratic organization: some management decisions (estimating, task assignment) are delegated to the group members.',
               'In **XP**, programmers work in pairs and take **collective responsibility** for the code: anyone can change any part, and nobody “owns” a module.']),
    30: dict(
        hl=[('Chief-Programmer Team', 1), ('surgical team', 1), ('Backup Programmer/co-pilot', 2), ('Program Clerk', 3), ('Tool-smith', 3), ('Language lawyer', 3), ('Ego issues', 4)],
        notes=['The **chief-programmer (surgical) team**, from IBM in the 1970s: a superstar writes the core code, supported by specialists, like a surgeon supported by anesthetists and nurses.',
               'The **backup programmer (co-pilot)** is equally skilled, shadows and reviews the chief, and can step in if needed.',
               'The **program clerk** manages documentation and version control; the **administrator** handles admin work; the **tool-smith** builds and maintains tools and environments; the **language lawyer** is the deep expert in the programming language.',
               'Issues: it is **difficult to achieve** (superstars are rare) and has **ego problems** on both sides. It can suit creative projects or tactical execution.'],
        exam=[likely('In a chief-programmer team, who is equally skilled and ready to step in for the chief?', a=0,
                     opts=['The backup programmer (co-pilot)', 'The program clerk', 'The tool-smith', 'The language lawyer'])]),
    31: dict(
        hl=[('kernel of specialists', 1), ('wide difference in', 2), ('very', 3)],
        notes=['A chief-programmer team is a **kernel of specialists**, with others added to the project as required.',
               'The motivation: the **wide difference in ability** between programmers. If the best are many times more productive, build the team around them.',
               'It gives **very able programmers** a supporting environment so they can be responsible for most of the system.']),
    32: dict(
        hl=[('hard to find', 1), ('resent the chief programmer', 2), ('High project risk', 3), ('Organizational structures and grades', 4)],
        notes=['Problems with the chief-programmer approach. Talented designers and programmers are **hard to find**; without exceptional people it fails.',
               'Other members may **resent the chief taking the credit** and deliberately undermine them.',
               '**High project risk**: the project fails if both the chief and the deputy are unavailable (a key-person risk).',
               'The organization’s **structures and pay grades** may not accommodate a team where one person is far above the rest.'],
        exam=[likely('A chief-programmer team carries high project risk because the project fails if both the chief and the deputy are unavailable.', tf=True)]),
    33: dict(
        hl=[('Skunk works Team', 1), ('high ownership', 1), ('Little visibility', 2), ('exploratory projects', 2), ('SWAT Team', 3), ('Skills tightly match goal', 3)],
        notes=['**Skunk works**: a group of talented, creative developers placed away from the “mother ship”, literally or figuratively. Pro: **high ownership and buy-in**.',
               'Con: **little visibility** into their progress. Use it for **exploratory projects** needing creativity, not for well-defined or narrow problems.',
               '**SWAT team**: highly skilled people whose **skills tightly match the goal**, who often work together repeatedly (e.g. a security SWAT team, an Oracle performance team).'],
        exam=[likely('A team of database experts is brought in to fix Oracle performance problems. This is a:', a=0,
                     opts=['SWAT team', 'Skunk works team', 'Democratic team', 'Chief-programmer team']),
              likely('A company sends a few creative developers off-site to explore a new product idea with little reporting. This is a:', a=0,
                     opts=['Skunk works team', 'SWAT team', 'Business team', 'Chief-programmer team'])]),
    34: dict(
        hl=[('Communication increases multiplicatively', 1), ('50 programmers = 1200 possible paths', 1), ('Always use a hierarchy', 2), ('Always less than 10', 2), ('4-6 developers', 3), ('Increases cohesiveness', 3)],
        notes=['In **large teams** communication paths grow with roughly the square of the team size. The exact formula is **n(n − 1) / 2**: 50 people → 1,225 paths (the slide rounds to 1,200); 7 people → 21.',
               'So large teams must formalize communication, **always use a hierarchy**, and break into units of optimal size: **always fewer than 10** (seven plus or minus one).',
               'The **optimal team size** is **4–6 developers** plus a tech lead, with QA, operations and design on top. Small teams inspire stronger identification and **cohesiveness**.'],
        exam=[asked('f242', 'Q3.2', 'Calculate the number of communication channels for a project team of 7 members.',
                    a='n(n − 1) / 2 = 7 × 6 / 2 = 21 channels.'),
              likely('Your team grows from 5 to 10 people. By how much do the communication channels increase?',
                     a='From 5 × 4 / 2 = 10 to 10 × 9 / 2 = 45 channels: the team doubled but channels grew 4.5 times. That is why large teams need hierarchy and should be split into sub-teams under 10.')]),
    35: dict(notes=['Section divider: **Managing People**.']),
    36: dict(
        hl=[('most important assets', 1), ('people oriented', 2)],
        notes=['People are an organization’s **most important assets**.',
               'A manager’s tasks are essentially **people-oriented**; without understanding people, management fails however good the technical plan is.']),
    37: dict(
        hl=[('Problem solving', 1), ('Motivating', 1), ('Planning', 2), ('Estimating', 2), ('Controlling', 3), ('Organizing', 3)],
        notes=['Every management activity is about people: **problem solving** with the people available and **motivating** those on the project…',
               '…**planning** what people will do and **estimating** how fast they will work…',
               '…**controlling** their activities and **organizing** the way they work.']),
    38: dict(
        hl=[('motivation is needs-based', 1), ('Basic needs', 2), ('Personal needs', 2), ('Social needs', 2), ('Maslow’s hierarchy of needs', 3)],
        notes=['A key role of the manager is to **motivate**, and motivation is **needs-based**: people act to satisfy needs.',
               'Three kinds: **basic** (food, sleep), **personal** (respect, self-esteem) and **social** (being accepted as part of a group).',
               '**Maslow’s hierarchy**: physiological → safety → social → esteem → self-realization (self-actualization).']),
    39: dict(
        hl=[('physiological and safety needs are satisfied', 1), ('Social, esteem and self-realization', 2), ('shift focus downwards', 3)],
        notes=['At work you can assume **physiological and safety needs are satisfied** (salary, safe workplace).',
               'So **social, esteem and self-realization** needs are the ones that matter for a manager.',
               'But if a lower need stays unmet for a long time (e.g. job security during layoffs), people **shift focus downwards** to it until it is satisfied again, and higher motivators stop working.']),
    40: dict(
        hl=[('communal facilities', 1), ('informal communications', 1), ('Recognition of achievements', 2), ('Appropriate rewards', 2), ('Training', 3), ('Responsibility', 3)],
        notes=['How to satisfy each need. **Social**: communal facilities (shared spaces, break rooms) and informal communication (team chats, lunch).',
               '**Esteem**: **recognition of achievements** and appropriate rewards (bonuses, promotions, certificates, symbolic gestures).',
               '**Self-realization**: **training** (people want to learn) and **responsibility** (empower them to make decisions).'],
        exam=[asked('f251', 'Q5.3', 'Your team has just completed a major milestone in the project development process. How would you celebrate this achievement collaboratively with your team members? How would you recognize individual contributions to the team’s success? What actions would you take to ensure that team morale remains high as you move forward in the project?',
                    a='Celebrate as a team (social need), e.g. a team lunch and an announcement of the milestone to the stakeholders. Recognize individuals specifically and publicly (esteem): name what each person contributed in the meeting, send thank-you notes to their managers, and give certificates or small rewards. Keep morale high (self-realization): hold a retrospective that captures what went well, set clear and achievable next goals, balance the workload, and offer training and more responsibility to those who want to grow.'),
              likely('Sending a developer on a cloud-architecture course mainly satisfies which need?', a=0,
                     opts=['Self-realization', 'Social', 'Safety', 'Physiological'])]),
    41: dict(
        hl=[('over-simplification', 1), ('Task-oriented', 2), ('Self-oriented', 3), ('Interaction-oriented', 4)],
        notes=['The needs hierarchy is an **over-simplification**; motivation also depends on **personality type**.',
               '**Task-oriented**: the motivation is the work itself (they love solving the problem).',
               '**Self-oriented**: the work is a means to personal goals (get rich, buy a house, travel).',
               '**Interaction-oriented**: the main motivation is the presence and actions of co-workers; they come to work because they like being with the team.'],
        exam=[likely('A developer works mainly to save for a house. This personality type is:', a=0,
                     opts=['Self-oriented', 'Task-oriented', 'Interaction-oriented', 'Democratic'])]),
    42: dict(
        hl=[('elements of each class', 1), ('Balance can change', 1), ('part of a group and culture', 2)],
        notes=['Real people have **elements of each class**, and the balance changes with personal circumstances (a new baby makes someone more self-oriented for a while).',
               'People are also motivated by being **part of a group and culture**: they go to work partly for the people they work with.']),
    43: dict(
        hl=[('group activity', 1), ('cannot be completed by one person', 1), ('Group interaction is a key determinant', 2), ('Flexibility in group composition is limited', 3)],
        notes=['Most software engineering is a **group activity**; non-trivial schedules can’t be met by one person.',
               '**Group interaction** is a key determinant of performance, so how the group works together matters as much as individual skill.',
               'Flexibility in **group composition is limited**: managers rarely pick an ideal team and must do their best with the people available.']),
    44: dict(
        hl=[('Interaction with', 1), ('Working alone', 2), ('Non-productive', 2)],
        notes=['About **50%** of an engineer’s time is spent interacting with other people (meetings, reviews, discussions), so communication skills matter far more than people expect.',
               'Only about **30%** is working alone, and **20%** goes on non-productive activities (admin, waiting, travel).'],
        exam=[likely('According to the time-distribution chart, roughly how much of an engineer’s time is spent interacting with other people?', a=0,
                     opts=['50%', '30%', '20%', '80%'])]),
    45: dict(
        hl=[('same motivation', 1), ('everyone wants to do their own thing', 2), ('everyone wants to be the boss', 2), ('too much chatting', 2), ('balance of all types', 3), ('most engineers are task-oriented', 3)],
        notes=['A group whose members all share the **same motivation** is a problem.',
               'All **task**-oriented → everyone wants to do their own thing; all **self**-oriented → everyone wants to be the boss; all **interaction**-oriented → too much chatting, not enough work.',
               'An effective group has a **balance of all types**, which is hard because **most engineers are task-oriented**. The interaction-oriented members are valuable because they keep communication going.'],
        exam=[likely('A team where “everyone wants to be the boss” is dominated by which personality type?', a=0,
                     opts=['Self-oriented', 'Task-oriented', 'Interaction-oriented', 'Balanced'])]),
    46: dict(
        hl=[('respect not titular status', 1), ('technical and an administrative leader', 2), ('Democratic leadership is more effective', 3), ('career path based on technical competence', 4)],
        notes=['Leadership depends on **respect, not title**.',
               'A group may have both a **technical leader** and an **administrative leader**.',
               '**Democratic leadership** is more effective than autocratic in software groups.',
               'Support a **technical career path** so good engineers don’t have to become managers to progress.']),
    47: dict(
        hl=[('more important', 1), ('Group quality standards can be developed', 2), ('inhibitions caused by ignorance are', 2), ('learn from each other', 3), ('Egoless programming', 4)],
        notes=['In a **cohesive group** members consider the group **more important** than any individual in it.',
               'Advantages: **group quality standards** can be developed and kept collectively; members work closely, so inhibitions caused by ignorance are reduced.',
               'Members **learn from each other** and know each other’s work, so anyone can cover for anyone.',
               '**Egoless programming**: members try to improve each other’s programs and don’t treat code as personal property.'],
        exam=[asked('m251v1', 'MCQ 10 (also V2 MCQ 9)', 'In a cohesive team, which of the following is an advantage?', a=1,
                    opts=['Members avoid challenging each other’s work to reduce conflict.', 'Group quality standards can be developed and maintained collectively.',
                          'Each member works independently without needing oversight.', 'Decision-making is always faster due to consensus.'],
                    why='Cohesive groups can set and keep shared quality standards, learn from each other and practise egoless programming. Avoiding challenge is groupthink, a risk of cohesion.')]),
    48: dict(
        hl=[('organizational', 1), ('Social events', 2), ('group identity and territory', 2), ('team-building activities', 2), ('Openness with information', 3)],
        notes=['Cohesiveness is influenced by the **organizational culture** and the personalities in the group.',
               'Encourage it through **social events** (team outings), a **group identity and territory** (a team name, its own space) and explicit **team-building**.',
               '**Openness with information** is the simplest tool: when everyone knows what is going on, everyone feels part of the group.']),
    49: dict(
        hl=[('loyal to cohesive groups', 1), ('preservation of group', 2), ('forcing', 3), ('external involvement', 3)],
        notes=['Members are **loyal to cohesive groups**, which is good until it isn’t.',
               '**Groupthink**: preserving the group regardless of technical or organizational considerations (defending a bad design because the group made it).',
               'Management should prevent it by **forcing external involvement** with each group: outside reviewers, cross-team reviews, rotating members.'],
        exam=[likely('How should management counter groupthink?', a=0,
                     opts=['Force external involvement with the group', 'Isolate the group further', 'Reward unanimous agreement', 'Remove all conflict'])]),
    50: dict(
        hl=[('status of work, design decisions', 1), ('strengthens group cohesion', 1), ('Higher status members tend to dominate', 2), ('Too many people of the same personality type', 3), ('central coordinator', 4)],
        notes=['Good communication is essential: information on the **status of work, design decisions** and changes to them must be exchanged, and it **strengthens cohesion**.',
               'Three things affect it. **Status**: higher-status members dominate conversations, so juniors’ ideas get lost.',
               '**Personalities**: too many of the same type is a problem (slide 45).',
               '**Channels**: communication routed through a **central coordinator** tends to be ineffective, a bottleneck.']),
    51: dict(
        hl=[('< 10', 1), ('Break big projects down', 1), ('informal, democratic way', 2), ('Chief programmer teams', 3)],
        notes=['Keep groups small (**< 10**, ideally under 7), and **break big projects down** into smaller ones.',
               'Small teams can be organized in an **informal, democratic** way…',
               '…while **chief-programmer teams** try to make the most effective use of scarce skills and experience.']),
    52: dict(
        hl=[('major managerial', 1), ('resume or CV', 2), ('information gained at an interview', 2), ('recommendations from other people', 2), ('psychological or aptitude tests', 3)],
        notes=['Choosing people is a **major managerial responsibility**.',
               'Decisions are usually based on the candidate’s **CV**, the **interview**, interviews with potential co-workers and **recommendations** from people who know them.',
               'Some companies use **psychological or aptitude tests**, but there is no agreement on whether they are useful.']),
    53: dict(
        hl=[('Application domain experience', 1), ('Platform experience', 2), ('Programming language', 2), ('Educational background', 3), ('Communication ability', 4), ('Adaptability', 4), ('Attitude', 5), ('Personality', 5)],
        notes=['**Application domain experience**: developers must understand the domain to build a successful system. One of the most important factors.',
               '**Platform experience** matters only for low-level work; **programming language** experience matters only for short projects with no time to learn a new language. A common trap: it is not the most critical factor.',
               '**Education** indicates fundamentals and ability to learn, and becomes less relevant with experience.',
               '**Communication ability** is very important (staff talk to engineers, managers and customers); **adaptability** (judged from varied experience) shows ability to learn.',
               '**Attitude** and **personality** are important but hard to assess. No personality type is better suited to software engineering; candidates must just fit with the team.'],
        exam=[likely('According to the table, programming language experience is significant mainly when:', a=0,
                     opts=['The project is short with no time to learn a new language', 'The project is long', 'The candidate has a postgraduate degree', 'The project is fully agile'])]),
    54: dict(
        hl=[('individual', 1), ('Comfort', 2), ('Privacy', 2), ('Health and safety', 3)],
        notes=['The physical workplace affects **individual productivity and satisfaction**.',
               'Provide **comfort**, **privacy** and facilities…',
               '…and take **health and safety** into account: lighting, heating, furniture.']),
    55: dict(
        hl=[('uninterrupted work', 1), ('natural light', 2), ('Personalization', 3)],
        notes=['**Privacy**: each engineer needs an area for **uninterrupted work**, because deep work is destroyed by interruptions.',
               '**Outside awareness**: people prefer working in **natural light**.',
               '**Personalization**: people organize their environment differently and like to do it their own way.']),
    56: dict(
        hl=[('without interruption', 1), ('increase productivity', 1), ('formal and informal meetings', 2)],
        notes=['Provide private spaces to work **without interruption**; individual offices have been shown to **increase productivity**.',
               'But teams also need shared spaces for **formal and informal meetings**. Balance focus and collaboration.']),
    57: dict(
        hl=[('economic and', 1), ('inanimate', 2), ('interchangeable, and expendable', 2), ('collaborators', 3), ('psychological safety', 3)],
        notes=['“Human resources” comes from an **economic** term for a corporate asset.',
               'That causes two problems: people get treated like **inanimate** resources (“maximize ROI in human capital”) and as **uniform, interchangeable and expendable**.',
               'Instead, the PM should treat team members as **collaborators**, stakeholders and teammates: recognize and nurture each person’s talent and foster **psychological safety** and cohesion.']),
    58: dict(
        hl=[('Interpersonal skills', 1), ('Shaping project culture', 1), ('Managing people', 2), ('Making people better', 2), ('Leadership', 3)],
        notes=['The PM’s people skills fall into five areas, covered in order on the next slides: **interpersonal skills** and **shaping project culture**…',
               '…**managing people** and **making people better**…',
               '…and **leadership**.']),
    59: dict(
        hl=[('Effective communication', 1), ('structured channels and formats', 1), ('all recipients in a timely manner', 1), ('Influencing the organization', 2), ('little to do with authority', 3)],
        notes=['**Effective communication** follows a defined protocol (structured channels and formats: status reports, stand-ups, escalation paths), reaches **all recipients in a timely manner**, and gives all the information needed, no more and no less.',
               '**Influencing the organization**: getting the project done depends on the PM’s abilities and the respect they earn; they influence, negotiate and build credibility.',
               '**Leadership** is one of the most misunderstood concepts: it has **little to do with authority**; it is about inspiring, guiding and aligning people toward a shared goal.'],
        exam=[asked('f251', 'Q3.1', 'In what ways do proficient communication abilities contribute to the management of project risks and the attainment of project success? Illustrate with an instance of how a breakdown in communication could affect a project, and propose methods for prevention or resolution.',
                    a='Good communication surfaces risks and issues early, while they are cheap to handle; keeps requirements and expectations shared across the team and stakeholders; and supports fast, informed decisions. Example: the backend team changes an API without telling the frontend team, integration fails at the end of the sprint, causing rework and a missed release. Prevention: a communication plan with defined channels (stand-ups, change notifications, API contracts), timely updates to everyone affected, and an escalation path; resolution: a joint meeting to agree the interface and re-plan.')]),
    60: dict(
        hl=[('Motivation', 1), ('among the least effective motivators', 1), ('Negotiation and conflict management', 2), ('Reaching consensus', 2), ('Problem solving', 3), ('progressive', 3)],
        notes=['**Motivation**: giving people incentives to act in the project’s interest and overcome challenges. Studies show **financial incentives are among the least effective** motivators; recognition, growth and meaningful work do more.',
               '**Negotiation and conflict management**: working with others to reach agreement and overcome differences; **reaching consensus** and defusing conflict are its two elements.',
               '**Problem solving**: recognize and define problems, then formulate, evaluate and decide on solutions. It can be learned with practice; **progressive elaboration** (refining step by step) helps manage complex problems.'],
        exam=[likely('Studies show financial incentives are among the most effective motivators for project teams.', tf=False, why='The slide says they are among the least effective.')]),
    61: dict(
        hl=[('broader context', 1), ('Understand organizational culture', 1), ('practices that exist in theory but not in reality', 2), ('engineering and personal background', 3), ('cultural role', 4)],
        notes=['The PM shapes the **project culture** within the **broader context** of the organization’s culture, so first understand the organizational culture: its values and attitude toward projects (structured methods or ad hoc).',
               'Organizations differ widely in their attitude to **real** PM as opposed to “fanciful” PM: practices that exist in theory but not in reality.',
               'Understand each member’s **engineering and personal background**: education, experience, generation and personality decide which roles suit them.',
               'Assess each member’s **cultural role** (next slide) and match it to their project role.']),
    62: dict(
        hl=[('Leader', 1), ('Listener/talker', 1), ('Complainer/naysayer', 2), ('Expert', 1), ('Charger/plodder', 1), ('Team leader', 3), ('Development leader', 3), ('non-judgmental', 4)],
        notes=['**Cultural roles**: **leader** (takes initiative, inspires), **listener/talker** (bridges communication gaps), **expert** (deep knowledge, credibility), **charger/plodder** (pushes forward with energy)…',
               '…and the **complainer/naysayer**, who habitually voices negative or skeptical views but raises concerns and challenges assumptions, often the first to spot a risk.',
               '**Project roles**: the **project manager** guides planning and tracks progress; the **team leader** builds and maintains an effective team; the **development leader** produces a superior product.',
               'Remain **non-judgmental**: every cultural role has potential value for the team.']),
    63: dict(
        hl=[('social and cultural context', 1), ('authority of the project manager', 1), ('local laws and customs', 2), ('time zone differences', 3)],
        notes=['Projects run in a **social and cultural context**: economic, educational, ethical, ethnic and religious factors can affect the **authority of the PM** (e.g. how far people accept direction from a younger manager).',
               'With globalization, familiarity with **local laws and customs** is essential, and shifting political factors can dramatically affect a project.',
               'Mundane factors matter too: **time zone differences**, holidays, travel and teleconferencing capabilities.']),
    64: dict(
        hl=[('Monitor and manage team culture', 1), ('role clear', 2), ('State and maintain your view of the team', 3), ('Recognize potential cultural role problems', 4), ('Solve project role problems', 4)],
        notes=['**Monitor and manage team culture** as you would manage technical issues: it is a project variable, not background.',
               'Make each person’s **project role clear** and show, positively, that you understand their personality and social role.',
               '**State and maintain your view of the team**, e.g. “we are all equals in this team, but if a critical situation arises, I will make the decision.”',
               '**Recognize cultural role problems** (a dominant voice silencing others, a skeptic undermining morale) and **solve project role problems** before they harm the team or project.']),
    65: dict(
        hl=[('satisfaction with their role', 1), ('during project launch', 1), ('task-to-people fit', 2), ('Role mismatches', 2), ('cultural climate', 3)],
        notes=['Monitor members’ **satisfaction with their role** throughout the project, especially **during launch** when roles are easy to change.',
               'Monitor the **task-to-people fit**: can each person actually do their engineering tasks? **Role mismatches** cause project problems and schedule slip, and without reviewing fit you won’t know.',
               'Monitor the **cultural climate** of the whole team by watching and listening, and guide it by your own example, to build confident people and a confident team.']),
    66: dict(
        hl=[('sociological in nature', 1), ('Peopleware', 2), ('engineering problem', 3), ('individual idiosyncrasies', 3)],
        notes=['The main problems in our work are **sociological**, not technological.',
               '**Peopleware** (DeMarco and Lister) is the recommended optional reading on managing people.',
               'Most technical managers manage as if solving an **engineering problem** and ignore **individual idiosyncrasies**, yet these can make or break a project.']),
    67: dict(
        hl=[('Gain visibility without micromanagement', 1), ('Review process and products, not people', 2), ('Coordinate, don’t manipulate', 3), ('Channel people, don’t put dams', 3), ('Focus on project and people needs', 4)],
        notes=['**Gain visibility without micromanagement**: know the status through boards and reviews, not by watching over shoulders.',
               '**Review process and products, not people**. Say “this testing regime lets too many bugs through to the customer; what can we do?”, not “you don’t know how to write unit tests.”',
               '**Coordinate, don’t manipulate** (use knowledge, not position), and **channel people** rather than damming them: redirect misplaced energy instead of cutting it off.',
               '**Focus on project and people needs**, not your authority; that maintains your leadership without explicit effort.'],
        exam=[likely('Which statement follows the guideline “review process and products, not people”?', a=0,
                     opts=['“This testing regime lets too many bugs through; how can we fix it?”', '“You don’t know how to write unit tests.”', '“Whoever wrote this is careless.”', '“I’ll decide, since I’m the manager.”'])]),
    68: dict(
        hl=[('production line', 1, 1), ('Squeeze out error', 2), ('goofing off', 2), ('interchangeable pieces', 3), ('Optimize the steady state', 3), ('Standardize procedure', 4), ('Eliminate experimentation', 4)],
        notes=['Applying **production-line** efficiency to thought workers can be a sign of disaster. The common errors:',
               '**Squeeze out error** (expecting the “machine” to run perfectly) and taking a hard line on “**goofing off**”, assuming any non-visible output is laziness when creative people need time to reflect.',
               'Treating workers as **interchangeable pieces** and **optimizing the steady state** while ignoring start-up and shut-down (ramp-up of new people, handover at the end).',
               '**Standardizing procedure** (run everything by the book) and **eliminating experimentation**, which kills the creativity software needs.']),
    69: dict(
        hl=[('professional development a project goal', 1), ('Short-term goals', 2), ('Long-term goals', 2), ('personal improvement goals', 3), ('awareness-building activity, not a monitoring activity', 4), ('Personal Software Process', 4)],
        notes=['Make **professional development a project goal**, not an afterthought.',
               '**Short-term** goals focus on skills needed for this project; **long-term** goals prepare members for future projects.',
               'Let each member set **personal improvement goals**, starting from a competency framework (technical, leadership, domain, personal, communication, management).',
               'For a fixed period have members track their time in detail. It is an **awareness-building** activity, **not monitoring**. The **Personal Software Process (PSP)** formalizes the idea.']),
    70: dict(
        hl=[('One element of PSP is to track', 1), ('Manage the quality of their projects', 2), ('Make commitments they can meet', 2), ('Improve estimating and planning', 2), ('Reduce defects', 2)],
        notes=['PSP has developers track **daily time** on every project activity (reading, writing, meetings, training, requirements, design, coding, testing, deployment, e-mail, phone), beyond the weekly timesheet.',
               'It shows developers how to **manage quality**, **make commitments they can meet**, **improve estimating and planning**, and **reduce defects**, because they learn from their own real data.']),
    71: dict(
        hl=[('mobilize a group to solve the most', 1), ('Technical leadership', 2), ('known means', 2), ('Adaptive leadership', 3), ('learning on the part of the leader', 3), ('leading with good questions', 3), ('deep clarity of purpose', 4)],
        notes=['**Leadership** is the capacity to **mobilize a group** to solve its most challenging problems; it is wrong to think it is about authority.',
               '**Technical leadership** (a.k.a. authority) works when the problem can be solved by **known means**: the leader directs, instructs and applies best practices.',
               '**Adaptive leadership** is needed when the problem can’t be solved by known means (complex or novel). It requires **learning by the leader** as well as the group, and often means **leading with good questions** that provoke thinking.',
               'It also needs **deep clarity of purpose** to keep the team anchored, e.g. in brainstorming the leader stops the discussion drifting into unimportant arguments and brings it back to the essential questions.']),
    72: dict(
        hl=[('solves problems', 1), ('Vision: personal view of outcome', 2), ('Sense of purpose', 2), ('Charisma, technical', 3), ('Progress: Motivation comes from learning', 3)],
        notes=['**Approach**: technical leadership solves problems by known means; adaptive leadership approaches problems that known means can’t solve.',
               '**Motivation driver**: technical uses the leader’s **personal vision** (“here’s what I see for us”); adaptive uses a shared **sense of purpose** (“why does this matter?”).',
               '**Tool for motivation**: technical relies on **personality**: charisma, expertise, confidence, decisiveness. Adaptive relies on **progress**: learning, iteration and visible movement toward clarity. In short: technical = “follow me, I know”; adaptive = “let’s figure it out together.”'],
        exam=[asked('m251v1', 'Short Q5 (also V2 Short Q5)', 'How can a project manager balance technical leadership with adaptive leadership in a software team?',
                    a='First diagnose the problem: can it be solved by known means? When it can (a coding standard, a deployment the team has done before), use technical leadership: give direction from expertise and vision, or delegate it to someone who can lead it. When it can’t (new technology, unclear requirements), use adaptive leadership: frame the purpose, lead with questions, let the team experiment and learn, and motivate through visible progress. Most IT projects mix both, so the PM switches between the two as the situation changes, delegating the known parts and focusing on the unknown ones.')]),
    73: dict(
        hl=[('whether the problem can be solved by known means', 1), ('mix of known and unknown problems', 2), ('by delegation', 3)],
        notes=['Choose the leadership type by asking **whether the problem can be solved by known means**.',
               'Most IT projects have a **mix of known and unknown** problems, so a PM needs both.',
               'An adaptive leader can handle known problems **by delegation**: let someone who can lead the team through the known solution do so.'],
        exam=[likely('An adaptive leader should personally solve all known technical problems.', tf=False, why='They can address known problems by delegation.')]),
    74: dict(
        hl=[('everyone feels heard', 1), ('reach consensus on all decisions', 2), ('Simple majority rule can be detrimental', 2), ('curate the quality of discourse', 3), ('constructively disqualified', 3)],
        notes=['**Consensus** in a project team doesn’t mean everyone agrees; it means **everyone feels heard** and the group moves forward with shared commitment.',
               'Reach consensus on all decisions affecting the team where possible. **Simple majority rule can be harmful** on a small team where everyone’s commitment is essential: the outvoted minority disengages.',
               'The leader must **curate the quality of discourse**: highlight valid arguments (e.g. someone citing user data) and **constructively disqualify** invalid ones to protect decision quality.'],
        exam=[asked('f251', 'Q5.1', 'Share an experience from a software project you were involved in where collaboration among team members significantly contributed to its success. Describe the specific strategies or techniques you employed to foster collaboration.',
                    a='Any honest experience earns marks if it names concrete techniques. For example: in a course project building a booking app, we split the work by feature with clear owners, met twice a week for short stand-ups, tracked tasks on a shared board, used pull requests so every change was reviewed by a teammate, and paired up on the hardest integration work. Decisions were discussed until everyone had been heard, so we committed to them even when we disagreed.')]),
    75: dict(
        hl=[('Pose the problem', 1), ('Solicit input on options', 1), ('Discuss and weigh pros and cons', 1), ('most benefit for the project', 1), ('persuade, don’t dictate', 2), ('passive/aggressive agreement', 3)],
        notes=['The steps: **pose** the problem or decision → **solicit input** on options → **discuss and weigh pros and cons** of each → work toward the options with the **most benefit for the project**.',
               'When the best option is clear, work with its opponents to help them buy in: **persuade, don’t dictate**. Consensus takes longer than a mandate but pays off in commitment.',
               'Beware **passive-aggressive agreement**: people who say yes but don’t act on it. It is just hidden (subsumed) conflict.'],
        exam=[asked('f251', 'Q5.2', 'You are leading a cross-functional team tasked with selecting a continuous integration/continuous deployment (CI/CD) platform for an upcoming project. The team includes software developers, DevOps engineers, and QA testers, each with distinct expectations regarding automation workflows and pipeline management. Describe your approach to collaboratively choosing the most suitable CI/CD platform.',
                    a='Run the consensus steps. Pose the decision in a kickoff workshop where developers, DevOps engineers and QA testers each list their needs (build speed, deployment control, test automation). Agree the criteria and their weights together: integration with the repository and tools, automation and test support, pipeline flexibility, scalability, security, cost, ease of use and vendor support. Shortlist options, weigh each against the criteria (a weighted scoring table, or a short proof of concept), converge on the one with the most benefit for the project, then work with those who preferred others so they buy in. Don’t just vote or dictate, and watch for passive-aggressive agreement.')]),
    76: dict(
        hl=[('reprise', 1), ('Be confident in yourself and the team', 2), ('Utilize all the talents of your team', 2), ('clarity, boundaries, and accountability', 3)],
        notes=['A **reprise** of slide 12 on establishing trust, now framed as how to lead.',
               'Two additions: **be confident** in yourself and the team, and **use all the talents** of your team, since you can’t make the project succeed alone.',
               'Friendship ≠ leadership: warmth and connection are vital, but leadership requires **clarity, boundaries and accountability**.']),
    77: dict(
        hl=[('human factors', 1), ('education, domain experience', 2), ('small and', 3), ('status, group size', 3), ('working environment', 4), ('monitor the project culture', 4)],
        notes=['Managers need to understand **human factors** to avoid unrealistic demands.',
               'Staff selection factors include **education, domain experience**, adaptability and personality.',
               'Groups should be **small and cohesive**; group communication is affected by **status, group size**, composition and organization.',
               'The **working environment** affects productivity, and the PM should **monitor the project culture** and technical status early and throughout.']),
}

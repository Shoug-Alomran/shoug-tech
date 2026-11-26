"""Study tools data for the SE423 Annotated Slides (scripts/install_annotated_study.py).

FINAL   which decks the final exam covers (the instructor dropped Ch 6.2 and Ch 7).
DRILLS  slides that get a calculation drill with new numbers on every try
        (docs/javascripts/annotated-study.js draws them).
EXPLAIN "Explain it to me" boxes: the idea in plain words, a small example, and the trap
        examiners set. Written for slides that had no tip of their own, mostly the
        formula and method slides.
"""

COURSE = "se423"
TITLE = "SE423"

# deck folder -> (on the final?, chapter label)
FINAL = {
    "01-introduction": (True, "Ch 1"),
    "02-performance-domains": (True, "Ch 1.2"),
    "03-tailoring": (True, "Ch 1.3"),
    "04-organizational-context": (True, "Ch 2"),
    "05-team": (True, "Ch 3"),
    "06-development-approach": (True, "Ch 4"),
    "07-risk-management": (True, "Ch 5"),
    "08-estimation": (True, "Ch 6"),
    "09-scheduling-and-tracking": (False, "Ch 6.2"),
    "10-quality": (False, "Ch 7"),
    "11-stakeholders": (True, "Ch 8"),
    "12-change-management": (True, "Ch 9"),
}

# deck -> {slide: drill type}. Types: cocomo, pert, risk, channels, ev, ci, duration.
DRILLS = {
    "05-team": {50: "channels"},
    "07-risk-management": {43: "risk"},
    "08-estimation": {21: "duration", 34: "pert", 46: "cocomo"},
    "09-scheduling-and-tracking": {33: "pert", 58: "channels", 75: "ev"},
    "10-quality": {45: "ci"},
    "11-stakeholders": {20: "channels"},
}

# deck -> {slide: (plain idea, example, exam trap)}
EXPLAIN = {
    "04-organizational-context": {
        15: (
            "In a matrix, people stay in their functional department but are loaned to projects, so each one reports to a functional manager and a project manager at the same time.",
            "A tester belongs to the QA department (who does her appraisal) but spends three months on the banking-app project (whose PM assigns her tasks).",
            "The weakness examiners want is “two bosses”: conflicting priorities and negotiation over shared staff, not “slow decisions” in general.",
        ),
        20: (
            "A PMO can sit at three heights: Level 3 serves the whole company, Level 2 serves one business unit, Level 1 sits inside a single project.",
            "A bank-wide PMO setting standards for every IT project is Level 3; a PMO that only supports the mobile division is Level 2.",
            "Level numbers go up with height: Level 1 is the project level, not the top.",
        ),
    },
    "05-team": {
        21: (
            "A Responsibility Assignment Matrix is a grid of tasks × people that says who does what, so nobody is unsure of their role and nothing is left unowned.",
            "Rows: requirements, design, testing. Columns: Sara, Omar, client. Each cell holds a letter such as R or A.",
            "It is a planning and tracking tool for people and roles, not a schedule: it says who, not when.",
        ),
        22: (
            "RACI letters: Responsible does the work, Accountable owns the result and signs off, Consulted gives input before, Informed is told after.",
            "Testing: tester = R, QA lead = A, developer = C, client = I.",
            "Exactly one A per task. Several people can be R, but two A’s on one task is a wrong answer.",
        ),
        72: (
            "Technical leadership solves problems that already have a known fix; adaptive leadership is for problems with no known answer, where people must change how they work.",
            "Fixing a slow database query is technical; moving a team from waterfall habits to agile is adaptive.",
            "Adaptive leaders give the problem back to the team and build shared purpose; they don’t hand down the answer.",
        ),
        74: (
            "Consensus means everyone has been heard and will commit to the decision, even if it was not their first choice. It is not unanimous agreement.",
            "Two developers prefer React, one prefers Vue; after discussion all three agree to commit to React.",
            "Majority vote is the trap: on a small team it can leave the out-voted members uncommitted.",
        ),
    },
    "07-risk-management": {
        4: (
            "A risk is an uncertain event that, if it happens, affects a project objective. It can be negative (a threat) or positive (an opportunity).",
            "“The cloud provider may give a 20% discount” is a risk too: a positive one.",
            "Something that has already happened is an issue, not a risk. Risk always means uncertainty.",
        ),
        21: (
            "A Risk Breakdown Structure groups risks into a hierarchy of categories, just like a WBS breaks down work.",
            "Project risk → Technical (new framework, performance) → External (vendor, law) → Organizational (budget, staff).",
            "RBS is an identification and categorization tool; it does not rank risks. Ranking comes from the probability–impact matrix.",
        ),
        41: (
            "Risk assessment turns a list of risks into priorities: where each risk comes from, its exposure, how soon to act, and which are most severe.",
            "Of 30 identified risks, assessment shows that 5 have high exposure and could hit within a month.",
            "Assessment comes after identification and before response planning: you can’t plan responses to unranked risks.",
        ),
        44: (
            "Probability is easier to estimate with words mapped to ranges, such as “likely” = 60–80%, than with exact numbers.",
            "The team says a vendor delay is “likely”, so you use about 70% when computing exposure.",
            "Know the five-point scale (highly unlikely <20% … highly likely >80%) and that a three-point scale is used when the situation is less well defined.",
        ),
        46: (
            "A probability–impact matrix turns two values into one rating (low, medium or high), so different risks can be compared and ranked.",
            "High probability and medium impact lands in the red “high” cell; low and low lands in green.",
            "The rating is ordinal (an order), not an exact amount. For a number, use exposure P × I.",
        ),
        48: (
            "Prioritize with the 80/20 rule: a few risks cause most of the damage, so spend effort on the high-exposure ones and watch the rest.",
            "Sort the risk register by exposure and plan responses for the top rows first.",
            "Low risks are not deleted; they stay on a watch list.",
        ),
        54: (
            "Urgency adds “how soon?” to “how big?”. Plan responses now for risks that could hit soon, and actively manage only about the top ten.",
            "A licensing risk due next week gets a response plan before a bigger risk that can only happen in month 9.",
            "Remaining risks go on a watch list and are promoted when they become urgent: like rolling-wave planning.",
        ),
        64: (
            "There are four basic ways to resolve a threat: avoid it (remove the cause), mitigate it (lower P or I), transfer it (someone else carries it), or acquire knowledge (research to reduce uncertainty).",
            "Unknown tech → build a prototype first (knowledge acquisition); risky feature → cut it (avoidance).",
            "Contingency plans and extra resources fall under mitigation (problem control), not avoidance.",
        ),
        66: (
            "Transfer hands the risk and its consequences to a third party, usually by contract or insurance. The risk still exists; someone else now manages it.",
            "Outsourcing KYC checks to a licensed provider transfers the legal-compliance risk.",
            "Transfer works best for financial risks and usually costs a fee. It does not remove the risk.",
        ),
        72: (
            "Opportunities have mirror-image strategies: exploit (make sure it happens), share (partner with someone who can exploit it), enhance (raise P or I) and accept.",
            "Put the senior developers on critical tasks to finish early (exploit); form a joint venture with a marketing firm (share).",
            "“Exploit” and “share” are for positive risks; “avoid” and “transfer” are for threats. Don’t mix them up.",
        ),
        73: (
            "A secondary risk is created by your response; a residual risk is what remains after the response.",
            "You hire an expert consultant (response), and the consultant may fall ill (secondary). Even so, some delay risk stays (residual).",
            "Secondary risks get fallback plans; residual risks are accepted, often covered by contingency reserve.",
        ),
    },
    "08-estimation": {
        7: (
            "The cone of uncertainty: estimates made early can be off by 0.25× to 4×, and the range narrows as the project learns more.",
            "At the idea stage a 10-month estimate could really be 2.5 to 40 months; after design it may be 8 to 12.",
            "That’s why you re-estimate at each phase and don’t commit to early target dates.",
        ),
        11: (
            "Top-down: estimate the whole project from its overall characteristics, then split the number among the parts.",
            "“Projects like this usually cost 50 person-months”, then 20% of that goes to testing.",
            "Fast and good early, but it misses detail. Analogy, expert judgment and algorithmic models are types of top-down.",
        ),
        12: (
            "Bottom-up: break the work into a WBS, estimate each small task, then add them up.",
            "Login (3 days) + payments (8 days) + reports (5 days) … = 40 days in total.",
            "Most accurate, but it needs a WBS and detailed knowledge, so it can’t be used at the very start.",
        ),
        13: (
            "Analogy: estimate from a finished past project that is similar enough (technology, type, organization), adjusting for the differences.",
            "The last e-commerce site took 12 months with similar features, so estimate about 12, adjusted for the extra payment gateway.",
            "Its strength is real historical data; its weakness is that no two projects are the same, and the old data may have been measured badly.",
        ),
        16: (
            "Wideband Delphi: experts estimate alone and anonymously, discuss the differences, then re-estimate, repeating until the numbers converge.",
            "Round 1: 4, 9 and 15 weeks. After discussion: 8, 9 and 10. Consensus: about 9 weeks.",
            "Anonymity is the point: it stops the loudest or most senior person from anchoring everyone else.",
        ),
        18: (
            "Function points measure size by what the software does for the user (inputs, outputs, inquiries, files, interfaces), not by lines of code.",
            "A screen that takes a new order is an input; the monthly sales report is an output.",
            "FP is language-independent and can be counted from requirements, before any code exists. That is its advantage over LOC.",
        ),
        19: (
            "Function point steps: count the functions in each category, weight each one by complexity (simple, average, complex) to get unadjusted FP, then adjust with the influence factors.",
            "10 average inputs × 4 + 5 average outputs × 5 = 65 unadjusted FP, which is then multiplied by the adjustment factor.",
            "Unadjusted ≠ adjusted. The 14 general system characteristics change the final total.",
        ),
        21: (
            "Effort is the total work (person-days); duration is the calendar time it takes. Duration = Effort ÷ People.",
            "60 person-days of work with 3 people takes 20 working days.",
            "Duration counts working days only, and adding people doesn’t shorten it linearly (Brooks’s law).",
        ),
        22: (
            "Labor time is the hands-on hours; clock time is the elapsed time, which is longer because nobody is productive 100% of the day.",
            "40 hours of labor at about 80% productivity needs about 50 business hours.",
            "Use labor time for cost and clock time for the schedule.",
        ),
        25: (
            "Over- and under-estimating both hurt. Too high: the project may not be funded, and Parkinson’s law makes work fill the time. Too low: rushed testing, poor quality and burnout.",
            "A padded 12-month estimate loses the bid; a 4-month promise leads to skipped testing.",
            "Watch for “double padding”, where both the developer and the manager add a buffer.",
        ),
        32: (
            "Keep all estimates in one time unit, then convert once at the end.",
            "Estimate everything in hours (12 h, 30 h, 6 h = 48 h), then convert: 48 h = 6 working days.",
            "Mixing days and hours in one schedule causes arithmetic mistakes in exam answers.",
        ),
        35: (
            "Three-point estimating on each function: (O + 4M + P) ÷ 6, then add the results for the total LOC.",
            "UICF: (1,500 + 4 × 2,300 + 3,100) ÷ 6 = 13,800 ÷ 6 = 2,300 LOC.",
            "Multiply only M by 4, and divide by 6, not 3.",
        ),
        36: (
            "With function points, each function’s count is multiplied by its category weight before you add them up.",
            "8 inputs × weight 4 = 32 FP for inputs; do the same for each category and add.",
            "Use the weight for the right category and complexity; the exam table gives them.",
        ),
        38: (
            "COCOMO turns size (KLOC) into effort with E = a·KLOC^b, then effort into time with TDEV = c·E^d. Staff = E ÷ TDEV.",
            "7.5 KLOC organic → E ≈ 20 person-months → TDEV ≈ 8 months → 2.5 people.",
            "Pick the right mode (organic, semi-detached or embedded) first: the constants depend on it.",
        ),
        41: (
            "The same size gives very different effort by mode, because the exponent b grows with complexity (1.05 → 1.12 → 1.20).",
            "200 KLOC: organic 626, semi-detached 1,133, embedded 2,077 person-months.",
            "Write the formula with the numbers in it: a·(KLOC)^b, then the result with units (person-months).",
        ),
        42: (
            "Development time comes from effort, not size: TDEV = 2.5 × E^d, in months.",
            "Organic with E = 20: 2.5 × 20^0.38 ≈ 8 months.",
            "Common slip: putting KLOC into the TDEV formula instead of E.",
        ),
        44: (
            "Average staff size = Effort ÷ Development time: how many people, on average, over the schedule.",
            "E = 100 person-months, TDEV = 10 months → SS = 100 ÷ 10 = 10 people.",
            "Show the division with your numbers (100/10). The answer is people, not person-months.",
        ),
        45: (
            "Productivity = LOC ÷ Effort: how many lines each person produces per month.",
            "7,500 LOC ÷ 20 person-months = 375 LOC per person-month.",
            "Use LOC, not KLOC, in the numerator if the expected answer is in LOC per person-month.",
        ),
        47: (
            "Embedded projects have the highest a and b, so effort grows fastest and productivity per person is lowest.",
            "50 KLOC embedded: E = 3.6 × 50^1.2 ≈ 394 person-months, TDEV ≈ 17 months, about 23 people, about 127 LOC per person-month.",
            "Compare with the organic example (375 LOC per person-month): complexity, not team laziness, explains the drop.",
        ),
        48: (
            "Intermediate COCOMO multiplies basic effort by cost drivers (15 ratings such as team ability, reliability needed and tool use) to correct for things LOC ignores.",
            "Very high reliability (×1.40) and a capable team (×0.86) adjust the basic estimate up or down.",
            "Basic COCOMO depends only on KLOC; the cost drivers are what makes it “intermediate”.",
        ),
    },
    "09-scheduling-and-tracking": {
        25: (
            "The critical path is the longest path through the network. Its activities have zero slack, so any delay on it delays the whole project.",
            "Paths A-C-D-E (35 days) and A-B-D-E (30 days): A-C-D-E is critical.",
            "Critical means longest, not “most important” or “most expensive”.",
        ),
        31: (
            "PERT expected time = (a + 4m + b) ÷ 6, where a = optimistic, m = most likely, b = pessimistic.",
            "a = 2, m = 4, b = 6 → (2 + 16 + 6) ÷ 6 = 4.",
            "The standard deviation (b − a) ÷ 6 measures uncertainty: a bigger spread means a riskier task.",
        ),
        34: (
            "Slack (float) is how long an activity can slip without delaying the project: LF − EF (or LS − ES).",
            "EF = 10, LF = 14 → slack = 4 days.",
            "Critical activities have slack = 0. Negative slack means the schedule is already late.",
        ),
        35: (
            "CPM: a forward pass gives the early start and finish, a backward pass gives the late start and finish, and the difference is slack.",
            "Forward pass: ES of the next task = the largest EF of its predecessors.",
            "CPM ignores resource limits. That gap is what the critical chain method and resource leveling fix.",
        ),
        42: (
            "Critical chain is critical path plus resource availability. Padding is removed from individual tasks and pooled into shared buffers.",
            "Each task estimate is cut to about 50% confidence, and a project buffer is added at the end of the chain.",
            "The buffers (project and feeding) are the key idea, against Parkinson’s law and student syndrome.",
        ),
        48: (
            "Resource leveling reschedules tasks so no person is over-allocated, often making the project longer.",
            "Omar is booked on two tasks in week 3, so one task slides into its slack or later.",
            "Leveling can extend the end date; smoothing only moves tasks within their slack.",
        ),
        54: (
            "Schedule compression shortens the schedule without cutting scope. Crashing adds resources (it costs money); fast-tracking runs tasks in parallel (it adds risk).",
            "Crash: hire two contractors for testing. Fast-track: start coding before design sign-off.",
            "Crash only critical-path tasks: shortening a task that has slack gains nothing.",
        ),
        56: (
            "Brooks’s law: adding people to a late software project makes it later, because of ramp-up and growing communication paths n(n−1)/2.",
            "Going from 5 to 10 people takes paths from 10 to 45.",
            "Effort (person-months) is not interchangeable with progress: men and months don’t trade.",
        ),
        71: (
            "Percent complete can be misleading: finishing the early, easy phases looks like 50% done while the hard work (coding, testing) is still ahead.",
            "Design and specs are done, so the report says “60%”, but most of the effort remains.",
            "That’s why earned value gives credit only for completed tasks with objective evidence.",
        ),
        73: (
            "Earned value compares planned value (PV), earned value (EV) and actual cost (AC). CPI = EV ÷ AC, SPI = EV ÷ PV.",
            "PV = 100, EV = 80, AC = 120 → CPI 0.67 (over budget), SPI 0.8 (behind schedule).",
            "Below 1 is bad for both indexes. CV = EV − AC and SV = EV − PV are negative when bad.",
        ),
        76: (
            "In most software EV tracking, a task earns credit only at 100% complete: no partial credit for “90% done”.",
            "A 40-hour task that is 90% done still earns 0 hours of EV.",
            "Keep tasks small (8–80 hours) so this all-or-nothing rule still shows steady progress.",
        ),
        77: (
            "Velocity is how many story points the team completes per iteration. It forecasts how much fits in the next one.",
            "Last three sprints: 18, 22 and 20 points → plan about 20 for the next sprint.",
            "Velocity compares a team with itself; comparing velocity between teams is meaningless.",
        ),
        79: (
            "A burn-down chart plots the work remaining against time. A line above the ideal line means you are behind.",
            "Day 5 of 10 with 70 of 100 points left is above the ideal 50, so behind.",
            "Burn-down shows remaining work; burn-up shows completed work and scope changes.",
        ),
    },
    "11-stakeholders": {
        19: (
            "Communication goes through a channel and is disturbed by noise. Choose the channel by urgency, audience and how much feedback you need.",
            "An urgent design conflict → a meeting (interactive); a monthly status → an email report (push).",
            "Know push (send it), pull (they fetch it) and interactive (two-way) and when each fits.",
        ),
        34: (
            "Power/interest grid: high power + high interest → manage closely; high power + low interest → keep satisfied; low + high → keep informed; low + low → monitor.",
            "The CEO who rarely asks about the project: keep satisfied. End users eager for the app: keep informed.",
            "Don’t swap “keep satisfied” (power) and “keep informed” (interest).",
        ),
    },
}

#!/usr/bin/env python3
"""Build the SE401 past-paper exams (interactive, keyword graded).

Each paper becomes docs/academics/software-engineering/se401/exams/<slug>/ with:
  <file>-bank.js   window.PAPER (questions, marks, keys, model answers)
  <file>.html      standalone page (se423.css + se401/exams/past-paper.js engine)
  index.html       site wrapper, cloned from the chapter 13 quiz wrapper

Questions follow the original papers' order and marks. Shared helpers and the
page CSS come from build_se423_past_papers.py. Run:
  python3 scripts/build_se401_past_papers.py
then rebuild the sidebar (scripts/build_academic_sidebar.py).
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_se423_past_papers import PAGE_CSS, e, mcq, short  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
EXAMS = ROOT / "docs/academics/software-engineering/se401/exams"
BASE = "/academics/software-engineering/se401/exams/"
SITE = "https://shoug-tech.com"
TEMPLATE = "13-white-box-testing-quiz"

EXTRA_CSS = """
      .pick-row select { font: 600 14px var(--sans, inherit); padding: 6px 8px; border: 1px solid var(--border); border-radius: 6px; background: var(--surface); color: var(--text); width: 100%; }
      .pick-row.right { background: var(--good-soft); }
      .pick-row.wrong { background: var(--bad-soft); }
      .code { font: 500 13px/1.55 var(--mono); background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 12px 14px; overflow-x: auto; white-space: pre; margin: 8px 0 0; }
      .bank { border-collapse: collapse; width: 100%; font-size: 14px; margin: 6px 0 12px; }
      .bank td { border: 1px solid var(--border); padding: 6px 8px; }
"""


def raw(it):
    """Mark an item whose model answer is already HTML (not escaped at build)."""
    it["raw"] = True
    return it


def esc_models(parts):
    for part in parts:
        for it in part["items"]:
            if it.get("model") and it["type"] != "self" and not it.pop("raw", False):
                it["model"] = e(it["model"])
            it.pop("raw", None)
    return parts


def picks(q, opts, rows, pts, c="", why="", model=""):
    return {"type": "picks", "q": q, "opts": opts, "rows": [{"label": l, "a": a} for l, a in rows], "pts": pts, "c": c, "why": why, "model": model}


def tf(q, a, why, c):
    """True/False as a two-option MCQ (a: True or False)."""
    return mcq(q, ["True", "False"], 0 if a else 1, why, c)


# ------------------------------------------------------------ Final Exam (242)
CODE = """public static void compareArrays(int[] A, int[] B, int[] C) {
  if (A.length != B.length || B.length != C.length) {
    System.out.println("Arrays are not of equal length.");
    return;
  }
  for (int i = 0; i < A.length; i++) {
    if (A[i] > B[i]) {
      if (A[i] > C[i]) {
        System.out.println("A[" + i + "] is the largest");
      } else if (A[i] == C[i]) {
        System.out.println("A[" + i + "] equals C[" + i + "] and is larger than B[" + i + "]");
      } else {
        System.out.println("C[" + i + "] is the largest");
      }
    } else if (B[i] > C[i]) {
      System.out.println("B[" + i + "] is the largest");
    } else {
      System.out.println("C[" + i + "] is the largest or equal to B[" + i + "]");
    }
  }
}"""


def final242():
    q1 = [
        mcq("Which testing level is most responsible for validating the fitness for use by the end-user?", ["Unit testing", "Integration testing", "System testing", "Acceptance testing"], 3, "Acceptance testing checks the system against the users' and business needs: is it fit for use?", "Test levels"),
        mcq("In the V-model, which phase directly corresponds to system testing?", ["Requirements specification", "Architectural design", "Detailed design", "System design"], 3, "Each V-model development phase pairs with a test level: requirements ↔ acceptance, system design ↔ system testing, architectural design ↔ integration, detailed design ↔ unit.", "V-model"),
        mcq("Which of the following best defines path coverage in white-box testing?", ["Executing each decision outcome at least once", "Testing all input combinations", "Testing all unique logical paths through the code", "Ensuring all statements are executed at least once"], 2, "Path coverage executes every unique path. Each decision outcome is decision (branch) coverage; every statement is statement coverage.", "Code coverage"),
        mcq("What is the primary goal of regression testing?", ["Find new features", "Verify usability compliance", "Ensure changes haven’t broken existing functionality", "Optimize performance"], 2, "Regression testing re-runs tests after a change to make sure existing behaviour still works.", "Regression testing"),
        mcq("Which of the following is an invalid equivalence partition for a login form with a required 6–12 character password?", ["Password with 8 characters", "Password with 6 characters", "Password with 15 characters", "Password with 12 characters"], 2, "6–12 characters is the valid partition; 15 falls in the invalid partition above 12.", "Equivalence partitioning"),
        mcq("What does cyclomatic complexity measure in a program?", ["The number of input variables", "The number of loops", "The number of possible independent paths through a program", "The depth of inheritance"], 2, "Cyclomatic complexity is the number of linearly independent paths, which is also the minimum number of tests for basis-path coverage.", "Cyclomatic complexity"),
        mcq("Which of the following is NOT typically considered part of static testing?", ["Code inspection", "Walkthrough", "Statement coverage analysis", "Desk checking"], 2, "Statement coverage is measured by running the code, so it's dynamic. Inspections, walkthroughs and desk checks examine the code without running it.", "Static testing"),
        mcq("In a system with high cyclomatic complexity, what is the best justification for applying condition coverage instead of relying solely on statement coverage?", ["Statement coverage alone always achieves 100% functional validation", "Condition coverage is simpler and faster to implement", "Statement coverage can miss logical errors in compound Boolean expressions", "Cyclomatic complexity only affects black-box test cases"], 2, "Statement coverage can execute an `if (a || b)` line without ever testing each condition as true and false, so faults in compound conditions slip through.", "Code coverage"),
        mcq("The cost of fixing a fault:", ["Is more expensive if found in requirements than functional design.", "Decreases as we move the product towards production.", "Can never be determined.", "Increases as we move the product towards production."], 3, "The later a defect is found, the more work has been built on it, so the cost of fixing it rises the closer the product gets to production.", "Cost of defects"),
        mcq("Why is desk checking considered a limited form of static testing?", ["It requires automated tools", "It focuses only on syntax", "It lacks structured review and may miss subtle defects", "It involves the full team"], 2, "Desk checking is one person reading their own code, with no structured process or second pair of eyes, so subtle defects get missed.", "Static testing"),
        mcq("In JUnit, what happens when an assertion fails?", ["The test is skipped", "The test is marked as failed", "The system halts", "The test is deleted"], 1, "A failed assertion throws an AssertionError; JUnit records that test as failed and carries on with the others.", "JUnit"),
        mcq("Which metric indicates how many defects are found during testing versus those found by users post-release?", ["Test execution coverage", "Test effort metric", "Defect detection efficiency", "Test case completeness"], 2, "Defect detection efficiency (DDE) = defects found in testing ÷ (defects found in testing + defects found after release).", "Testing metrics"),
        mcq("Consider a test case designed using Equivalence Partitioning for a shipping system charging $5 for weights 0–1 kg, $3/kg for 1.01–5 kg, $2/kg for 5.01–15 kg, and $1/kg for >15 kg. Which of the following test inputs would best validate a boundary condition defect missed by typical partitioning?", ["1.0 kg", "5.0 kg", "5.01 kg", "5.00 kg and 5.01 kg in a single comparative test"], 3, "A boundary defect sits exactly where one rate switches to the next. Testing 5.00 and 5.01 together checks both sides of that boundary, which a single value from each partition can miss. (This key is our answer: on the marked paper, 5.0 kg alone was marked wrong.)", "Boundary value analysis"),
        mcq("Why is test case prioritization important in regression testing?", ["It eliminates redundant code", "It ensures faster code compilation", "It reduces cost and time by focusing on the most critical tests first", "It improves database efficiency"], 2, "Regression suites grow large; prioritizing runs the most important or riskiest tests first, so major problems are found early when time is short.", "Regression testing"),
    ]
    q2 = [
        short("Why is test coverage (e.g., requirement coverage and code coverage) considered a key quality metric in software testing? Discuss how it influences test planning.", 2, [
            ["Requirement coverage = requirements tested ÷ total requirements; code coverage = code executed by tests ÷ total code", ["requirement", "code", "execut", "total", "%"]],
            ["Shows how much has (and hasn't) been tested, i.e. the untested gaps", ["untested", "gap", "miss", "not tested", "how much"]],
            ["Low coverage means risk / undetected defects; gives confidence in quality", ["risk", "confiden", "defect", "quality"]],
            ["Planning: target the gaps, add tests, set exit criteria and priorities", ["plan", "exit", "criteria", "prioriti", "add test", "more test", "focus", "next"]],
        ], "Coverage measures how much of the system the tests actually exercise: requirement coverage = requirements covered by tests ÷ total requirements × 100, code coverage = statements/branches executed ÷ total × 100. It's a key quality metric because untested requirements and code are where defects hide, so low coverage means high risk and little confidence. In planning it shows exactly where the gaps are: the team adds tests for uncovered requirements and code, prioritizes the riskiest gaps, and uses coverage targets as exit criteria (you can't control what you can't measure).", "Test coverage"),
        short("In integration testing, explain the difference between top-down and bottom-up approaches. When would you prefer each strategy?", 2, [
            ["Top-down: start from the top (main/control) modules and work down", ["top", "main", "control", "high level", "down"]],
            ["Top-down uses stubs for lower modules not yet built", ["stub"]],
            ["Bottom-up: start from the lowest-level modules and work up", ["bottom", "lowest", "low level", "up"]],
            ["Bottom-up uses drivers to call the modules under test", ["driver"]],
            ["When: top-down for an early working skeleton / validating the main flow and design; bottom-up when low-level modules are critical or ready first", ["early", "skeleton", "prototype", "design", "critical", "ready", "prefer", "when"]],
        ], "Top-down integration starts with the top-level control module and adds the modules below it one level at a time, using stubs to stand in for lower modules that aren't ready. Bottom-up starts with the lowest-level modules, tests them together in clusters and works upward, using drivers to call them. Prefer top-down when you want an early working skeleton of the system and to check the main control flow and design early. Prefer bottom-up when the low-level modules (utilities, hardware or data access) are critical, complex or finished first, since faults there are found early and no stubs are needed.", "Integration testing"),
        short("What role does a test oracle play in software testing? Provide an example where a poorly defined oracle can lead to incorrect test results.", 2, [
            ["Oracle: the source of the expected result for a test", ["expected", "correct output", "expected result", "expected output"]],
            ["Used to decide pass or fail by comparing actual with expected", ["compar", "pass", "fail", "actual", "verdict"]],
            ["Example of a vague/poor oracle (e.g. 'fast', 'large number', wrong spec)", ["example", "vague", "subjective", "ambiguous", "fast", "huge", "large", "wrong"]],
            ["Consequence: false passes or false failures", ["false", "incorrect", "wrong result", "miss", "pass when"]],
        ], "A test oracle is the source that tells you the expected result of a test (a spec, a previous version, a calculation, a human expert). The tester compares the actual result with it to decide pass or fail. If the oracle is poorly defined the verdict is unreliable. Example: the requirement says the search must be “fast”. One tester passes a 4-second response, another fails it, so the same behaviour gets different verdicts, and a real performance defect can pass (a false pass). An oracle built from an outdated spec can also fail correct behaviour (a false failure).", "Test oracle"),
        short("Explain how test metrics like “defect density” and “test case effectiveness” can guide decision-making in the final stages of a software release.", 2, [
            ["Defect density = defects ÷ size (KLOC, function points or modules)", ["defect density", "kloc", "size", "lines", "per module", "function point"]],
            ["Test effectiveness = how many defects the tests find (vs those found later)", ["effective", "found", "detect", "escap", "post release"]],
            ["High density / low effectiveness = not ready: more testing or fixing, delay release", ["not ready", "delay", "more test", "postpone", "fix"]],
            ["Low density and high effectiveness = confidence to release (go/no-go decision)", ["release", "ready", "confiden", "go", "decision"]],
        ], "Defect density (defects ÷ size, e.g. per KLOC or per module) shows how buggy the product or each component still is, and which modules are hot spots. Test case effectiveness (defects found by tests ÷ total defects, or defects found per test) shows whether the tests are actually catching defects. Near release they drive the go/no-go decision: high density or low effectiveness means the product isn't ready, so add or improve tests on the weak modules, fix the defects or delay the release; low density with high effectiveness gives confidence to release.", "Testing metrics"),
        short("Static Testing can help in checking several things, give 4 things can be tested in static testing.", 2, [
            ["Requirements / design documents (ambiguities, missing or inconsistent items)", ["requirement", "design", "document", "spec", "ambigu"]],
            ["Coding standards and conventions", ["standard", "convention", "style"]],
            ["Syntax and logic errors", ["syntax", "logic"]],
            ["Unreachable or dead code, unused variables", ["unreach", "dead", "unused", "untouched", "variable"]],
            ["Security vulnerabilities / maintainability / complexity", ["security", "vulnerab", "maintain", "complex", "interface"]],
        ], "Any four of: requirements and design documents (ambiguities, omissions, inconsistencies); deviations from coding standards; syntax and logic errors; unreachable (dead) code and unused or undefined variables; interface mismatches; security vulnerabilities; maintainability and code complexity; test plans and test cases themselves.", "Static testing"),
    ]
    q3_intro = "<h4>Code under test</h4><p>Consider the following Java method:</p><pre class=\"code\">" + e(CODE) + "</pre>"
    q3 = [
        short("Is decision coverage enough to cover all paths for the above program?", 2, [
            ["No", ["no", "not enough", "not sufficient", "insufficient"]],
            ["Decision coverage only makes each decision true and false once", ["each decision", "true and false", "each branch", "outcome", "once"]],
            ["Paths are combinations of decisions (and loop iterations), so many paths stay untested", ["combination", "path", "loop", "iteration"]],
            ["The compound condition (||) needs each condition tested on its own", ["compound", "combined", "condition", "or", "||"]],
        ], "No. Decision coverage only requires every decision to take its true and its false outcome at least once. The number of paths is the number of combinations of those outcomes, plus the loop running 0, 1 or many times, so 100% decision coverage still leaves most paths untested. The first if also combines two conditions with ||, and decision coverage can make it true and false without ever testing B.length != C.length on its own.", "Code coverage"),
        {"type": "self", "pts": 4, "c": "Decision coverage",
         "q": "Write down one or more test cases, such that this/these test case(s) together satisfy Decision coverage. State clearly which parts of the test(s) cover which part of the code.",
         "model": "Six decisions need a true and a false outcome each: D1 the length check, D2 the for loop, D3 A[i] &gt; B[i], D4 A[i] &gt; C[i], D5 A[i] == C[i], D6 B[i] &gt; C[i].<div class='tbl-scroll'><table class='grid-tbl'><thead><tr><th>Test</th><th>A</th><th>B</th><th>C</th><th>Covers</th></tr></thead><tbody>"
                  "<tr><th>T1</th><td>{1}</td><td>{1, 2}</td><td>{1}</td><td>D1 true (lengths differ, prints “not of equal length”)</td></tr>"
                  "<tr><th>T2</th><td>{3, 2, 2, 1, 1}</td><td>{1, 1, 1, 3, 2}</td><td>{1, 2, 3, 2, 3}</td><td>D1 false; D2 true five times then false. i=0: D3 T, D4 T (A largest). i=1: D3 T, D4 F, D5 T (A equals C). i=2: D3 T, D4 F, D5 F (C largest). i=3: D3 F, D6 T (B largest). i=4: D3 F, D6 F (C largest or equal to B)</td></tr>"
                  "</tbody></table></div>Two tests give 100% decision coverage. Splitting T2 into five one-element tests is just as correct; what matters is that every decision is shown both true and false and you say which test covers which outcome."},
        {"raw": True, "type": "num", "pts": 2, "c": "Cyclomatic complexity",
         "q": "Calculate the cyclomatic complexity.",
         "fields": [{"label": "Cyclomatic complexity V(G)", "a": 7, "alts": [8], "tol": 0}],
         "model": "V(G) = number of decisions + 1. The decisions are the length check, the for loop, A[i] &gt; B[i], A[i] &gt; C[i], A[i] == C[i] and B[i] &gt; C[i]: 6 decisions, so V(G) = 6 + 1 = <b>7</b>. If you count each condition of the compound <code>||</code> as its own predicate node, you get 7 + 1 = <b>8</b>, which is also accepted. (The marked paper gave full marks for 5 + 1 = 6, which leaves out the for loop.)"},
    ]
    q4_intro = (
        "<h4>A. Room Booking System</h4><p>A university is developing a Room Booking System for faculty members. The system checks the following conditions before approving a booking request:</p><ol>"
        "<li><b>User Role</b>: the user must be a faculty member (not a student or guest).</li>"
        "<li><b>Room Availability</b>: the requested room must be available for the selected time slot.</li>"
        "<li><b>Advance Notice</b>: the booking must be made at least 24 hours in advance of the requested time.</li></ol>"
        "<p>Depending on the combination of these conditions, the system behaves differently:</p><ul>"
        "<li>If all conditions are met, the booking is approved automatically.</li>"
        "<li>If the room is unavailable, the booking is denied with a “Room Unavailable” message.</li>"
        "<li>If the user is not faculty, the booking is rejected with an “Unauthorized User” message.</li>"
        "<li>If the advance notice is not met (i.e., request is too late), the booking is flagged for manual approval.</li>"
        "<li>If multiple conditions fail, the system returns the most critical error message in this priority: 1. Unauthorized User, 2. Room Unavailable, 3. Late Request.</li></ul>"
    )
    actions = ["Unauthorized User", "Room Unavailable", "Late Request (flag for manual approval)", "Approved"]
    rules = []
    for i, (f, r, n) in enumerate([(f, r, n) for f in (0, 1) for r in (0, 1) for n in (0, 1)]):
        tfv = lambda b: "T" if b else "F"
        act = 0 if not f else 1 if not r else 2 if not n else 3
        rules.append((f"Rule {i + 1}: Faculty = {tfv(f)}, Room available = {tfv(r)}, 24h notice = {tfv(n)}", act))
    q4 = [
        picks("Design the decision table for this system: for each combination of the three conditions, choose the action the system takes. (On the paper you also had to pick the technique and draw the table yourself.)", actions, rules, 3, "Decision tables",
              "3 conditions give 2³ = 8 rules. Whenever the user isn't faculty the answer is Unauthorized User whatever else fails (highest priority); otherwise an unavailable room gives Room Unavailable; otherwise a late request is flagged; only all-true is approved. The technique to name is the decision table (black-box), because the output depends on combinations of conditions."),
        raw(short("B. You are testing a mobile data plan billing system based on monthly data usage. The billing rules are: the first 2 GB are included in the monthly base plan and cost nothing extra; the next 3 GB (up to 5 GB) are charged at $2 per GB; the next 5 GB (up to 10 GB) are charged at $1.5 per GB; any usage above 10 GB is charged at $1 per GB. Using the Equivalence Partitioning technique, identify the different equivalence classes for the data usage field and provide at least one test case for each class.", 2, [
            ["Invalid class: negative usage (< 0)", ["negative", "less than 0", "< 0", "below 0", "invalid"]],
            ["Valid class 0–2 GB (free), e.g. 1 GB", ["0 2", "free", "included", "base"]],
            ["Valid class >2–5 GB ($2/GB), e.g. 3.5 GB", ["2 5", "2 01", "$2"]],
            ["Valid class >5–10 GB ($1.5/GB), e.g. 7 GB", ["5 10", "5 01", "1 5"]],
            ["Valid class >10 GB ($1/GB), e.g. 15 GB", ["10", "above 10", "more than 10", "$1"]],
        ], "Classes for usage U (GB), one test value from inside each: <b>invalid</b> U &lt; 0 → −1 (rejected); <b>valid 1</b> 0 ≤ U ≤ 2 → 1 GB, $0 extra; <b>valid 2</b> 2 &lt; U ≤ 5 → 3.5 GB, 1.5 × $2 = $3; <b>valid 3</b> 5 &lt; U ≤ 10 → 7 GB, $6 + 2 × $1.5 = $9; <b>valid 4</b> U &gt; 10 → 15 GB, $6 + $7.5 + 5 × $1 = $18.5. Decide which class 2, 5 and 10 GB themselves fall in (the marker asked “what about = 10?”) and say so.", "Equivalence partitioning")),
        raw(short("C. You are testing the Online Loan Application System for a financial institution. The system validates: (1) Applicant Age between 21 and 65 years inclusive; (2) Annual Income at least $15,000 USD; (3) Requested Loan Amount between $5,000 and $500,000, and not more than 10× the applicant’s annual income; (4) Credit Score 600 or higher. Using Boundary Value Analysis, identify the key boundary values for each of the four input fields, and design a minimum of 2 test cases per field.", 2, [
            ["Age: 20, 21 (and 65, 66)", ["20", "21", "65", "66"]],
            ["Income: 14,999 and 15,000", ["14999", "15000", "14 999", "15 000"]],
            ["Loan: 4,999 / 5,000 and 500,000 / 500,001", ["4999", "5000", "500000", "500001", "4 999", "500 001"]],
            ["Loan vs 10× income: exactly 10× and just over", ["10x", "10 x", "10 times", "ten times", "10×"]],
            ["Credit score: 599 and 600", ["599", "600"]],
        ], "Test just below, on and just above each boundary. <b>Age</b>: 20 (reject), 21 (accept), 65 (accept), 66 (reject). <b>Income</b>: 14,999 (reject), 15,000 (accept). <b>Loan amount</b>: 4,999 (reject), 5,000 (accept), 500,000 (accept), 500,001 (reject); and against income, with income $20,000: loan 200,000 = 10× (accept) and 200,001 (reject). <b>Credit score</b>: 599 (reject), 600 (accept). Note the boundaries themselves (21, 65, 15,000, 5,000, 500,000, 600) are valid; the marked paper lost marks for testing only 20/66 and 22/64.", "Boundary value analysis")),
    ]
    q5_intro = (
        "<h4>Case-based metrics analysis</h4><p>You are reviewing a QA report from a completed sprint of a software project. The team executed a comprehensive testing cycle, and the following summary was presented:</p>"
        "<div class='tbl-scroll'><table class='grid-tbl given'><thead><tr><th>Metric description</th><th>Value</th></tr></thead><tbody>"
        + "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in [
            ("Total test cases executed", "150"), ("Test cases passed", "100"), ("Test cases failed", "50"),
            ("Total defects reported during testing", "50"), ("Critical defects reported", "20"),
            ("Defects successfully fixed before release", "40"), ("Requirements validated through test cases", "50"),
            ("Total system requirements", "200"), ("Total executed tests", "300"),
            ("Cumulative hours spent on fixing defects", "10 hours"), ("Defects discovered post-release (by customers)", "150")])
        + "</tbody></table></div>"
    )
    q5 = [
        {"raw": True, "type": "num", "pts": 4, "c": "Testing metrics",
         "q": "Using the data above, calculate the following metrics.",
         "fields": [
             {"label": "a. Requirements Coverage", "a": 25, "unit": "%", "tol": 0.5},
             {"label": "b. Defect Density per Test Hour", "a": 5, "unit": "defects / hour", "tol": 0.05},
             {"label": "c. Average Time to Repair a Defect", "a": 15, "unit": "minutes (0.25 h)", "tol": 0.5},
             {"label": "d. Fixed Defects Percentage", "a": 80, "unit": "%", "tol": 0.5},
             {"label": "e. Test Effectiveness", "a": 25, "unit": "%", "tol": 0.5}],
         "model": "a. Requirements coverage = validated ÷ total requirements × 100 = 50 ÷ 200 = <b>25%</b>. b. Defect density per test hour = defects found ÷ hours = 50 ÷ 10 = <b>5 defects/hour</b> (the only hours given are the 10 hours; the marked paper accepted this). c. MTTR = repair hours ÷ defects fixed = 10 ÷ 40 = 0.25 h = <b>15 minutes</b>. d. Fixed defects % = fixed ÷ defects reported × 100 = 40 ÷ 50 = <b>80%</b> (the marked paper lost marks for dividing by the 150 test cases). e. Test effectiveness = defects found in testing ÷ (found in testing + found post-release) × 100 = 50 ÷ (50 + 150) = <b>25%</b>."},
        short("Interpret your results: for each metric calculated, briefly explain what the value implies about the software quality, testing efficiency, or release readiness of the system.", 2, [
            ["Coverage 25%: only a quarter of requirements tested, 75% untested, high risk", ["quarter", "75", "low coverage", "untested", "not tested", "25"]],
            ["Defect density 5/hour: many defects, poor product quality / unstable", ["many defect", "high", "unstable", "poor quality", "5"]],
            ["MTTR 15 min: fixes are fast, efficient team", ["fast", "quick", "efficient", "15"]],
            ["80% fixed: 10 defects (20%) still open, some may be critical", ["80", "open", "remaining", "unfixed", "10 defect"]],
            ["Effectiveness 25%: tests missed most defects (150 found by users); not ready for release", ["not ready", "missed", "customer", "user", "release", "ineffective"]],
        ], "Requirements coverage 25%: three quarters of the requirements were never validated, so most of the system is untested and risky. 5 defects per hour: the product is defect-heavy. MTTR 15 minutes: once found, defects are fixed quickly, so the fixing process is efficient. 80% fixed: 10 known defects (some possibly critical) were released unfixed. Test effectiveness 25%: customers found three times as many defects as testing did, so the testing was ineffective. Overall the system was not ready for release: widen coverage and improve the tests before the next release.", "Interpreting metrics"),
        short("List three types of data that need to be tested for performance testing, then discuss the importance of using appropriate test data in performance testing.", 2, [
            ["Volume / large data sets (database size)", ["volume", "large", "big data", "data set", "database", "record"]],
            ["Load: number of concurrent users / transactions", ["concurren", "user", "load", "transaction", "request"]],
            ["Boundary, peak or stress data (and response time, throughput measures)", ["peak", "stress", "boundary", "response time", "throughput", "spike"]],
            ["Importance: realistic, production-like data gives valid, reliable results", ["realistic", "real", "production", "representative", "accurate", "valid", "reliable"]],
            ["Wrong data hides bottlenecks / gives misleading results", ["bottleneck", "mislead", "hide", "wrong", "false"]],
        ], "Three kinds of test data: (1) volume data, i.e. production-sized databases and large files; (2) load data, i.e. realistic numbers of concurrent users, sessions and transactions; (3) peak or stress data, beyond the expected maximum and with varied, realistic input mixes, while measuring response time and throughput. Appropriate data matters because performance depends on the data: a small or unrealistic data set makes the system look fast and hides bottlenecks (slow queries, memory leaks, locking), so the results would be misleading. Production-like data gives results you can trust when deciding whether the system will cope in real use.", "Performance testing"),
    ]
    return [
        {"title": "Question 1 · MCQs", "items": q1},
        {"title": "Question 2 · Short questions", "items": q2},
        {"title": "Question 3 · White-box test design", "intro": q3_intro, "items": q3},
        {"title": "Question 4 · Black-box test design", "intro": q4_intro, "items": q4},
        {"title": "Question 5 · Testing metrics", "intro": q5_intro, "items": q5},
    ]


# ---------------------------------------------- Past exam: MCQ + fill-in (20)
BANK = [("a", "Stub"), ("b", "Unit testing"), ("c", "Integration testing"), ("d", "Test driver"),
        ("e", "Stress testing"), ("f", "System testing"), ("g", "Component testing"), ("h", "Static testing"),
        ("i", "Acceptance testing"), ("j", "Test coverage"), ("k", "Dynamic testing"), ("l", "Smoke testing"),
        ("m", "White box testing"), ("n", "Black box testing"), ("o", "Maintenance testing"), ("p", "Test suite")]
BANK_OPTS = [f"{k}. {v}" for k, v in BANK]


def blank(n, letter, why, c):
    it = picks(f"Blank ({n})", BANK_OPTS, [(f"({n})", "abcdefghijklmnop".index(letter))], 1, c, why)
    it["n"] = str(n)
    return it


def past_mcq():
    q1 = [
        mcq("Total Cost of Quality (CoQ) includes", ["Cost of Conformance (CoC) + Cost of Non-Conformance (CoNC)", "Cost of Conformance (CoC) + Cost of Non-Conformance (CoNC) + Manual efforts", "Cost of Conformance (CoC) + Manual efforts", "All of the above"], 0, "CoQ = cost of conformance (prevention + appraisal) + cost of non-conformance (internal + external failures).", "Cost of quality"),
        mcq("Which of the following is NOT included in the Cost of Non-Conformance?", ["Internal failures", "Rework", "External failure", "Quality Planning"], 3, "Quality planning is prevention, which is a cost of conformance. Failures and rework are the cost of non-conformance.", "Cost of quality"),
        mcq("Is a test that is performed at the development organization site.", ["Alpha test", "Beta test", "Smoke test", "All of the above"], 0, "Alpha testing happens at the developer's site; beta testing happens at the customers' sites.", "Acceptance testing"),
        mcq("Which of the following defines “Average amount of time a system operates before it fails”?", ["Mean time between failures", "Mean time to failures", "Mean time to repair", "None of the above"], 1, "MTTF is the average operating time before a failure. MTBF = MTTF + MTTR, and MTTR is the average repair time.", "Reliability metrics"),
        mcq("Which of the following defines “The probability of a system to operate without failures”?", ["Reliability", "Availability", "Security", "Failure-ability"], 0, "Reliability is the probability of failure-free operation over a period. Availability is the share of time the system is up.", "Reliability metrics"),
        mcq("Deviation of the observed behavior of a system from its specification, i.e., its expected behavior is called", ["Defect", "Failure", "Error", "Issue"], 1, "A failure is the visible deviation from expected behaviour. An error (mistake) by a person causes a defect (fault) in the code, which may cause a failure when executed.", "Error, defect, failure"),
        mcq("Which of the following defines “software validation”?", ["Are we building the software right?", "Are we building the right software?", "Both A and B", "None of the above"], 1, "Validation: are we building the right product (does it meet the user's needs)? Verification: are we building the product right (does it meet the spec)?", "Verification vs validation"),
        mcq("Which of the following is CORRECT about the term “test oracle”?", ["The expected outputs of software for given input", "A part of test cases", "Hardest problem in auto-testing", "All of the above"], 3, "An oracle supplies the expected output, the expected result is part of every test case, and automating the oracle is one of the hardest problems in test automation.", "Test oracle"),
        mcq("If the cyclomatic complexity value of a code/program is more than 40, what can be said about the code/program?", ["It is well-written code and testability is high", "It is moderately complicated and testability is medium", "It is extremely complicated and not testable", "It is very complicated and testability is low"], 2, "From the white-box slides: 1–10 well-written, high testability; 10–20 moderately complex, medium; 20–40 very complex, low testability; above 40 not testable. (The answer sheet photo appears to show D, but D is the 20–40 band.)", "Cyclomatic complexity"),
        mcq("Which of the following should be noted for each test level?", ["The generic objectives", "The test objectives", "The test basis", "All of the above"], 3, "Each test level is described by its generic objectives, test basis, test objects, typical defects and responsibilities.", "Test levels"),
        mcq("Which of the following testing types includes functional and non-functional testing?", ["Unit testing", "Component testing", "Smoke Testing", "Stress Testing"], 1, "Component testing can cover both functional and non-functional characteristics (e.g. memory leaks, robustness). Stress testing is only non-functional; smoke testing is a quick functional check. This follows the answer sheet.", "Test levels"),
        mcq("Which of the following “is a way of testing software products (including code) and can be performed well before dynamic test execution”?", ["Stress testing", "Reviews", "System testing", "All of the above"], 1, "Reviews are static testing: they examine work products without running them, so they can start long before execution.", "Static testing"),
        mcq("Which one of the following is a very formal review?", ["Walkthrough", "Technical review", "Inspection", "All of the above"], 2, "Inspection is the most formal review: trained moderator, defined roles, entry/exit criteria and metrics.", "Review types"),
        mcq("Which of the following roles has the chief responsibility for the documents to be reviewed and for the rework to be done during the reviews?", ["Author", "Review leader", "Management", "Facilitator"], 0, "The author wrote the work product and fixes the defects found in it.", "Review roles"),
        tf("Software testing is NOT required to be a systematic process to identify the correctness, completeness, and quality of developed software.", False, "Testing must be systematic: planned, designed and controlled.", "Testing fundamentals"),
        tf("With reference to the V-model, for every development activity there is a corresponding testing activity.", True, "That's the core V-model principle: each development phase has a matching test level.", "V-model"),
        tf("Test levels can be combined or reorganized depending on the nature of the project or the system architecture.", True, "Test levels are a model; projects merge or reorganize them to fit the context.", "Test levels"),
        tf("Static and dynamic testing have the same objective.", True, "Both aim to find defects as early as possible and assess quality; they differ in how (without vs with executing the code).", "Static testing"),
        tf("Static analysis can identify both the defects and failures.", False, "Static analysis finds defects directly in the code; failures only appear when the code runs (dynamic testing).", "Static testing"),
        tf("Testing reduces the probability of undiscovered defects remaining in the software but even if no defects are found, it is not a proof of their absence.", True, "Principle 1: testing shows the presence of defects, not their absence.", "Testing principles"),
    ]
    intro = (
        "<h4>Answers to choose from</h4><table class='bank'><tbody>"
        + "".join("<tr>" + "".join(f"<td><b>{k}.</b> {v}</td>" for k, v in BANK[r:r + 4]) + "</tr>" for r in range(0, 16, 4))
        + "</tbody></table><h4>Scenario</h4>"
        "<p>The development team at <b>PSUTech Solutions</b> is preparing to release their new online payment platform for student registration. During a team meeting, the QA Lead explains that before executing any code, the team will conduct a review session to check for syntax and logical errors without running the program. This activity is part of ______ <b>(21)</b>.</p>"
        "<p>Afterward, the developers begin testing individual modules such as user login, transaction validation, and balance calculation separately to ensure that each works correctly on its own. This step is known as ______ <b>(22)</b>. Once those modules pass, the team connects the login module with the transaction system to verify how they interact together, a process called ______ <b>(23)</b>.</p>"
        "<p>However, because the notification service isn’t finished yet, the testers decide to simulate its behavior using a ______ <b>(24)</b> while they also develop a ______ <b>(25)</b> to trigger and validate the functions of the modules under test.</p>"
        "<p>After the integration phase, the QA team conducts full end-to-end verification of the entire payment system to ensure it meets functional and performance expectations, which is referred to as ______ <b>(26)</b>. They then invite selected customers to test the system in a real-world environment and confirm it meets all business needs, which falls under ______ <b>(27)</b>. Before each built deployment, the team runs a few quick tests to confirm that core features like login and payment still work; this is called ______ <b>(28)</b>.</p>"
        "<p>Later, they simulate heavy transaction traffic to check how the system behaves under pressure, this is ______ <b>(29)</b>. Finally, to ensure that every line of code has been properly examined during testing, they analyze their ______ <b>(30)</b> report.</p>"
    )
    q2 = [
        blank(21, "h", "Reviewing code for errors without running it is static testing.", "Static testing"),
        blank(22, "b", "Testing individual modules on their own is unit testing.", "Test levels"),
        blank(23, "c", "Connecting modules and testing how they interact is integration testing.", "Integration testing"),
        blank(24, "a", "A stub simulates a module that's called but not built yet (the notification service).", "Stubs and drivers"),
        blank(25, "d", "A test driver calls (triggers) the modules under test.", "Stubs and drivers"),
        blank(26, "f", "End-to-end testing of the whole system against functional and performance requirements is system testing.", "Test levels"),
        blank(27, "i", "Customers confirming it meets business needs in a real environment is acceptance testing.", "Acceptance testing"),
        blank(28, "l", "A few quick tests that core features still work on each build is smoke testing.", "Smoke testing"),
        blank(29, "e", "Simulating heavy traffic to see how the system behaves under pressure is stress testing.", "Performance testing"),
        blank(30, "j", "A report on how much of the code was exercised is a test coverage report.", "Code coverage"),
    ]
    return [
        {"title": "Question 1 · Multiple choice and true/false", "items": q1},
        {"title": "Question 2 · Fill in the blanks", "intro": intro, "items": q2},
    ]


PAPERS = [
    {"slug": "14-final-242", "file": "final-242", "title": "Final Exam (242)", "short": "FINAL · 242", "item": 13,
     "meta": [["Term", "242 (2nd term, 2024/2025)"], ["Date", "29 May 2025"], ["Duration", "3 hours"], ["Total", "40 marks"]],
     "lede": "The SE401 final from term 242 (Prof. Mohammad Akour, Dr. Reem Alsuhaibani, Ms. Sana Sultan). Every chapter is in scope. There was no answer key: MCQ keys follow the marked paper where the marking shows the answer, and the written answers are model answers from the course slides, graded strictly by keyword. The decision-coverage test cases are self-marked against the model.",
     "parts": final242},
    {"slug": "15-past-exam-mcq-and-fill-in", "file": "past-exam-mcq-and-fill-in", "title": "Final Exam - MCQ and Fill in the Blanks", "short": "FINAL · MCQ", "item": 14,
     "meta": [["Term", "Unknown"], ["Questions", "30"], ["Format", "MCQ, true/false, fill in the blanks"], ["Total", "20 marks"]],
     "lede": "A past SE401 final (term unknown) with 20 MCQ and true/false questions and a 10-blank testing scenario. The keys follow the answer sheet that came with it, except Q9, which follows the white-box slides.",
     "parts": past_mcq},
]

NOTES = {
    "14-final-242": "Question 1 has 14 MCQs at 0.5 marks each (7 marks).",
}


def page(p, parts):
    url = f"{SITE}{BASE}{p['slug']}/"
    total = sum(it["pts"] for part in parts for it in part["items"])
    desc = f"SE401 {p['title']} as an interactive exam: check each answer as you go, strict keyword grading and model answers."
    nav = "\n".join(f'          <a href="#part-{i + 1}">Q{i + 1}</a>' for i in range(len(parts)))
    meta = "".join(f"<div><b>{e(k)}</b>{e(v)}</div>" for k, v in p["meta"])
    note = f'<p class="note">{e(NOTES[p["slug"]])}</p>' if p["slug"] in NOTES else ""
    return f"""<!doctype html>
<html lang="en" data-sg-styled>
  <head>
    <link rel="icon" type="image/png" sizes="256x256" href="/assets/shoug-favicon-v4.png" />
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/shoug-apple-touch-icon-v4.png" />
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>SE401 | {e(p['title'])}</title>
    <meta name="description" content="{e(desc)}" />
    <link rel="canonical" href="{url}" />
    <meta property="og:title" content="SE401 | {e(p['title'])}" />
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
    <style>{PAGE_CSS}{EXTRA_CSS}    </style>
    <link rel="stylesheet" href="/styles/site-shell.css" />
    <script defer src="/javascripts/site-palette.js"></script>
    <link rel="stylesheet" href="/styles/quiz-motion.css" />
    <script defer src="/javascripts/quiz-motion.js"></script>
  </head>
  <body>
    <header class="topbar">
      <div class="wrap">
        <span class="brand"><b>SE401</b> // {e(p['short'])}</span>
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
        <div class="eyebrow">SE401 · Software Quality Assurance &amp; Testing · Past paper</div>
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
      <p class="foot">SE401 · {e(p['title'])} · {total:g} marks · model answers from the course slides</p>
    </main>
    <script src="./{p['file']}-bank.js"></script>
    <script src="../past-paper.js"></script>
  </body>
</html>
"""


def wrapper(p, prev_slug, next_slug, template):
    s = template
    s = s.replace("SE401 · Chapter 12 Quiz — White Box Testing", f"SE401 · {p['title']}")
    s = s.replace("SE401 \\u00b7 Chapter 12 Quiz \\u2014 White Box Testing", f"SE401 \\u00b7 {p['title']}")
    s = s.replace("Chapter 12: White Box Testing Quiz", p["title"])
    s = re.sub(r"Interactive SE401 Chapter 12 White Box Testing\s+self-graded\s+practice\s+exam\s+from\s+Shoug(&#x27;|')s\s+Digital\s+Garden\.",
               lambda m: f"SE401 {e(p['title'])}: the real past paper as an interactive exam with per-question checking, strict keyword grading and model answers.", s)
    s = s.replace(f"exams/{TEMPLATE}/\"", f"exams/{p['slug']}/\"").replace(f"exams/{TEMPLATE}/?", f"exams/{p['slug']}/?")
    s = s.replace("./white-box-testing-quiz.html", f"./{p['file']}.html")
    s = s.replace("ITEM_12 // EXAMS", f"ITEM_{p['item']:02d} // EXAMS")
    s = re.sub(r'(href=")[^"]*("\s*class="nav-link prev")', rf"\g<1>{BASE}{prev_slug}/\2", s)
    s = re.sub(r'(href=")[^"]*("\s*class="nav-link next")', rf"\g<1>{BASE}{next_slug}/\2", s)
    head = s.split('<nav class="sidebar')[0]
    assert "white-box-testing-quiz" not in head and "Chapter 12" not in head, p["slug"]
    return s


def main():
    template = (EXAMS / TEMPLATE / "index.html").read_text(encoding="utf-8")
    chain = [TEMPLATE] + [p["slug"] for p in PAPERS] + [PAPERS[-1]["slug"]]
    for i, p in enumerate(PAPERS):
        parts = esc_models(p["parts"]())
        d = EXAMS / p["slug"]
        d.mkdir(exist_ok=True)
        bank = {"id": p["file"], "parts": parts}
        (d / f"{p['file']}-bank.js").write_text(
            f"/* SE401 {p['title']}: generated by scripts/build_se401_past_papers.py. Edit the builder, not this file. */\nwindow.PAPER = "
            + json.dumps(bank, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
        (d / f"{p['file']}.html").write_text(page(p, parts), encoding="utf-8")
        (d / "index.html").write_text(wrapper(p, chain[i], chain[i + 2], template), encoding="utf-8")
        total = sum(it["pts"] for part in parts for it in part["items"])
        print(f"{p['slug']}: {sum(len(x['items']) for x in parts)} questions, {total:g} marks")


if __name__ == "__main__":
    main()

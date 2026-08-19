#!/usr/bin/env python3
"""Build comprehensive interactive mindmaps and chapter exams for SE401."""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_design_html as sitegen

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/academics/software-engineering/se401"
MAPS = BASE / "extra-resources/mindmaps"
EXAMS = BASE / "exams"
REF = ROOT / "docs/academics/software-engineering/se423"
ETHICS_MAP_TEMPLATE = ROOT / "docs/academics/other-courses/ethcs303/extra-resources/mindmap/01-moral-systems-ethical-concepts-and-theories/moral-systems-ethical-concepts-and-theories.html"

CHAPTERS = [
    ("advanced-topics", "Advanced Topics", [
        ("Web Testing", "Validate functionality, usability, interfaces, compatibility, performance, and security across browsers and networks.", ["Static websites primarily present content; web applications accept input and maintain state.", "Check links, forms, cookies, sessions, database interactions, error handling, and browser behavior.", "Performance testing covers load, stress, scalability, and response time."]),
        ("Web Automation", "Browser automation improves repeatability for stable, high-value regression paths.", ["Selenium WebDriver controls real browsers through language bindings.", "Use robust locators, explicit waits, isolated tests, and maintainable page objects.", "Automation complements rather than replaces exploratory and usability testing."]),
        ("Mobile Applications", "Native, mobile-web, and hybrid apps have different packaging, access, and portability trade-offs.", ["Native apps target a platform and can deeply access device features.", "Mobile web apps run in a browser; hybrid apps wrap web content in a native shell.", "Test install, launch, interruption, permissions, updates, offline behavior, and resource use."]),
        ("Mobile Context", "Device fragmentation and real-world context make mobile testing distinctive.", ["Cover screen sizes, OS versions, orientations, networks, battery levels, memory pressure, and sensors.", "Test calls, notifications, backgrounding, roaming, and connectivity changes.", "Emulators are fast and broad; real devices expose hardware and network realities."]),
        ("Specialized Quality", "Accessibility, localization, security, and recovery are cross-cutting quality concerns.", ["Accessibility includes keyboard use, focus, labels, contrast, zoom, and assistive technology.", "Localization checks language, direction, date, currency, layout expansion, and cultural fit.", "Recovery tests verify safe behavior after crashes, dropped connections, and partial operations."]),
    ]),
    ("black-box-testing-techniques", "Black Box Testing Techniques", [
        ("Black-Box View", "Derive tests from externally visible behavior without relying on internal code structure.", ["Use requirements, specifications, interfaces, business rules, and user workflows as test bases.", "Good tests cover valid behavior, invalid behavior, and boundaries.", "Black-box techniques apply at component, integration, system, and acceptance levels."]),
        ("Equivalence Partitioning", "Divide an input or output domain into classes expected to behave alike; sample representatives.", ["Create valid and invalid partitions.", "Each test should clearly exercise the intended partition.", "Partitions reduce redundant testing while preserving meaningful coverage."]),
        ("Boundary Value Analysis", "Defects cluster near the edges of ordered partitions.", ["Test minimum, just above minimum, nominal, just below maximum, and maximum.", "Robust testing also checks just outside valid boundaries.", "Apply BVA to ranges, counts, sizes, dates, and ordered outputs."]),
        ("Decision Tables", "Model combinations of conditions and the actions they trigger.", ["Columns are rules; each rule represents a meaningful condition combination.", "Use limited-entry tables for Boolean conditions and extended-entry tables for richer values.", "Collapse impossible or irrelevant combinations to keep the table manageable."]),
        ("State Transition Testing", "Verify behavior as a system moves between states in response to events.", ["Cover valid transitions, invalid transitions, states, events, guards, and actions.", "A transition tree can expose sequences and loops.", "Useful for login, workflow, protocol, device, and order-lifecycle behavior."]),
        ("Use Cases & Error Guessing", "Scenario tests follow actor goals; experience-based tests target likely failures.", ["Use-case paths include basic, alternate, and exceptional flows.", "Error guessing draws on defect history, domain knowledge, and tester intuition.", "Check empty, null, duplicate, malformed, repeated, interrupted, and out-of-order operations."]),
        ("Static, Dynamic & Exploratory", "Static testing examines work products without execution; dynamic testing executes software; exploratory testing combines learning, design, and execution.", ["Black-box specification techniques contrast with white-box structure techniques.", "Special-value testing targets troublesome domain values.", "Race, limit, stress, recovery, configuration, compatibility, and documentation testing address risks beyond correctness."]),
    ]),
    ("code-coverage", "Code Coverage", [
        ("Coverage Purpose", "Coverage measures which code structures a test suite executes; it reveals gaps, not correctness.", ["High coverage cannot prove the absence of defects.", "Use coverage to guide additional tests and assess regression suites.", "Coverage criteria form a subsumption hierarchy, but stronger coverage can cost more."]),
        ("Statement Coverage", "Execute every executable statement at least once.", ["Statement coverage is easy to measure but can miss decision outcomes.", "100% statement coverage does not imply 100% branch coverage.", "Unreachable code prevents full coverage unless removed or justified."]),
        ("Decision & Branch Coverage", "Exercise every decision outcome or control-flow branch at least once.", ["For a Boolean decision, cover both true and false outcomes.", "Branch coverage generally subsumes statement coverage.", "Short-circuit expressions may require condition-focused criteria."]),
        ("Condition Coverage", "Exercise atomic Boolean conditions as both true and false.", ["Condition coverage alone may not force the whole decision to both outcomes.", "Decision/condition coverage combines decision and atomic-condition obligations.", "MC/DC shows each condition independently affects the decision outcome."]),
        ("Path & Loop Coverage", "Path coverage targets execution paths; loops create a potentially unbounded set.", ["Complete path coverage is often infeasible because of loops and path explosion.", "For loops, test zero, one, two, typical, maximum, and boundary-adjacent iterations.", "Basis-path testing uses cyclomatic complexity to identify independent paths."]),
        ("Control-Flow Graphs", "A CFG represents statements or blocks as nodes and flow transfers as edges.", ["Cyclomatic complexity V(G) = E − N + 2 for one connected component.", "It also equals the number of predicate nodes plus one in common structured code.", "Independent paths add at least one previously unused edge."]),
    ]),
    ("introduction", "Introduction", [
        ("Testing Fundamentals", "Testing evaluates software and related work products to find defects and provide quality information.", ["Testing includes static and dynamic activities.", "Debugging locates, analyzes, and removes defect causes; it is not the same as testing.", "Testing shows the presence of defects, not their complete absence."]),
        ("Error–Defect–Failure", "A human error may introduce a defect; executing that defect under triggering conditions may cause failure.", ["Root causes explain why errors occur.", "Not every defect causes failure on every execution.", "Failures are observable deviations from expected service."]),
        ("Testing Principles", "Exhaustive testing is impossible, so testing must be risk-based, context-sensitive, and renewed.", ["Early testing saves time and cost.", "Defects cluster in a small number of components.", "Repeated unchanged tests lose effectiveness: the pesticide paradox.", "Absence-of-errors is a fallacy if the product does not meet user needs."]),
        ("Test Process", "Plan, monitor, analyze, design, implement, execute, complete, and improve testing.", ["Trace test conditions and cases back to the test basis.", "Compare actual and expected results and log anomalies.", "Completion assesses exit criteria, residual risk, and lessons learned."]),
        ("Test Independence", "Different degrees of independence bring different perspectives and trade-offs.", ["Authors find defects quickly with context but may share blind spots.", "Independent testers challenge assumptions but can become isolated.", "Collaboration and respectful feedback are essential."]),
        ("Core Distinctions", "Testing, verification, validation, and debugging answer different questions.", ["Verification checks specified requirements; validation checks real user needs.", "Debugging locates and removes a defect after failure evidence.", "A test passes when expected and actual agree, fails on a violated assertion, and errors when it cannot execute normally."]),
    ]),
    ("quality", "Quality", [
        ("Quality Concepts", "Quality is the degree to which inherent characteristics fulfill requirements and stakeholder needs.", ["Quality of design chooses appropriate characteristics; quality of conformance implements them correctly.", "Fitness for use emphasizes the user's context and goals.", "Quality is multidimensional and involves trade-offs."]),
        ("Quality Assurance", "QA provides confidence that suitable processes are defined and followed.", ["QA is preventive and process-oriented.", "Audits, standards, training, and process improvement are common QA activities.", "QA does not remove the need for product testing."]),
        ("Quality Control", "QC evaluates work products to detect defects and verify conformance.", ["Reviews, inspections, testing, and measurement are QC activities.", "QC is product-oriented and often detective.", "QA and QC reinforce each other."]),
        ("Cost of Quality", "Quality costs include prevention, appraisal, internal failure, and external failure.", ["Prevention and appraisal are conformance costs.", "Rework before release is internal failure; warranty and reputation damage after release are external failure.", "Earlier prevention and detection generally reduce total cost."]),
        ("Quality Planning", "Define standards, objectives, metrics, responsibilities, reviews, tests, tools, and acceptance criteria.", ["Quality plans must be measurable and tailored to risk.", "Entry and exit criteria make decisions explicit.", "Continuous improvement uses evidence and feedback."]),
        ("Measurement Perspectives", "Size-, function-, web-, product-, process-, and project-oriented measures illuminate different concerns.", ["Static product metrics require no execution; dynamic product metrics do.", "Private process measures support personal improvement while public measures support organizational decisions.", "Testing supplies quality evidence; it cannot build quality into a poorly engineered product."]),
    ]),
    ("regression-testing", "Regression Testing", [
        ("Regression Purpose", "Re-test previously tested software after change to detect unintended effects in unchanged areas.", ["Changes include fixes, features, refactoring, configuration, environment, and dependencies.", "Confirmation testing checks the specific fix; regression testing checks broader side effects.", "Regression scope depends on change impact and risk."]),
        ("Test Selection", "Select a subset of existing tests relevant to affected and high-risk areas.", ["Retest-all is safest but often too expensive.", "Modification-, minimization-, and coverage-based selection reduce cost differently.", "Unsafe selection can omit tests that reveal regression faults."]),
        ("Prioritization", "Order tests so the most valuable failures are found earlier.", ["Prioritize by risk, recent changes, business criticality, defect history, coverage, and execution time.", "Prioritization does not necessarily remove tests.", "Use feedback from recent runs to adapt ordering."]),
        ("Suite Maintenance", "Keep regression suites trustworthy, fast, independent, and aligned with current behavior.", ["Remove obsolete and duplicate tests; repair flaky tests.", "Refactor fixtures and test data as the product evolves.", "Track runtime, failure yield, maintenance cost, and coverage."]),
        ("Automation & CI", "Automate stable, repeatable checks and run them at appropriate pipeline stages.", ["Use a test pyramid: many fast unit tests, fewer service tests, and focused UI tests.", "Parallelism and incremental selection shorten feedback.", "Quarantine is temporary; diagnose flaky tests rather than normalizing them."]),
        ("Impact Analysis", "Trace a change through dependencies, interfaces, requirements, code, tests, and operational risks.", ["Direct impact is not the whole regression surface.", "Version control, dependency graphs, traceability, and coverage data support analysis.", "Risk determines the breadth and depth of reruns."]),
        ("Obsolete vs Redundant", "An obsolete case describes outdated behavior; a redundant case adds no useful coverage beyond retained cases.", ["Repair or remove obsolete cases because their oracle is stale.", "Consolidate redundant cases to reduce maintenance cost.", "Selection chooses tests to run; prioritization orders them."]),
    ]),
    ("software-quality", "Software Quality", [
        ("Product Quality Model", "A quality model organizes characteristics used to specify and evaluate a software product.", ["Functional suitability: completeness, correctness, appropriateness.", "Performance efficiency: time behavior, resource utilization, capacity.", "Compatibility: coexistence and interoperability."]),
        ("Interaction Quality", "Usability and accessibility determine whether intended users achieve goals effectively, efficiently, and safely.", ["Usability includes learnability, operability, error protection, engagement, and accessibility.", "Accessibility must be designed and tested, not added at the end.", "Context of use changes what good quality means."]),
        ("Dependability", "Reliability, security, and safety address continuity, protection, resilience, and harm.", ["Reliability includes maturity, availability, fault tolerance, and recoverability.", "Security includes confidentiality, integrity, non-repudiation, accountability, and authenticity.", "Safety analysis considers hazards and unacceptable risk."]),
        ("Maintainability", "Modularity, reusability, analyzability, modifiability, and testability support economical change.", ["High coupling and low cohesion increase change risk.", "Readable code, modular design, diagnostics, and automated tests improve maintainability.", "Technical debt creates future cost and uncertainty."]),
        ("Portability & Flexibility", "Adaptability, installability, replaceability, and scalability support changing environments and needs.", ["Portability concerns movement across environments.", "Compatibility concerns coexistence and information exchange.", "Measure characteristics with operationally meaningful metrics."]),
        ("Verification, Validation & Stages", "Verification checks conformance to specifications; validation checks fitness for user needs.", ["The V-model pairs development work with corresponding test work.", "Integration, system, acceptance, alpha, and beta testing have different scopes and participants.", "MTTF measures time to failure; MTBF measures time between failures."]),
    ]),
    ("test-cases", "Test Cases", [
        ("Test Case Anatomy", "A test case specifies preconditions, inputs, actions, expected results, and postconditions.", ["Use a unique ID, objective, priority, traceability, environment, and data.", "Expected results must be observable and unambiguous.", "Keep cases atomic enough to diagnose failures."]),
        ("From Conditions to Cases", "Test analysis identifies what to test; test design turns conditions into coverage-oriented cases.", ["Derive conditions from requirements, risks, models, code, and experience.", "Use techniques deliberately rather than inventing examples at random.", "Record coverage items and trace them to cases."]),
        ("Test Data", "Data must represent valid, invalid, boundary, special, and state-dependent situations.", ["Protect privacy with synthetic or masked data.", "Make setup repeatable and cleanup reliable.", "Manage dependencies, clocks, randomness, and identifiers."]),
        ("Expected Results", "Use an oracle to decide whether observed behavior is correct.", ["Oracles include specifications, calculations, trusted systems, invariants, and expert judgment.", "Oracle problems occur when correct output is difficult to know.", "Avoid merely copying implementation logic into expected results."]),
        ("Review & Maintenance", "Review cases for correctness, coverage, clarity, feasibility, and duplication.", ["Update cases when requirements and interfaces change.", "Separate reusable intent from brittle UI detail.", "A passing obsolete test provides false confidence."]),
        ("Execution Infrastructure", "Drivers, stubs, harnesses, oracles, smoke tests, and defect tracking support repeatable execution.", ["A driver calls the unit under test; a stub substitutes for a called dependency.", "Comparison-based, self-checking, and capture-replay mechanisms are oracle strategies.", "Test code should avoid vague data, brittle identity comparisons, unnecessary logic, and unrelated assertions."]),
    ]),
    ("test-design-techniques", "Test Design Techniques", [
        ("Technique Families", "Specification-based, structure-based, and experience-based techniques expose different defect classes.", ["Specification-based techniques use external behavior and models.", "Structure-based techniques use code or architecture.", "Experience-based techniques use knowledge, heuristics, and defect history."]),
        ("Choosing Techniques", "Choose based on test level, objective, risk, basis quality, skill, time, and system type.", ["Combine complementary techniques for stronger coverage.", "Document the coverage criterion and stopping rule.", "Critical features justify deeper and more diverse design."]),
        ("Combinatorial Testing", "Pairwise and t-way testing cover interactions among parameters with far fewer combinations than exhaustive testing.", ["Define parameters, values, and constraints carefully.", "Pairwise covers every pair, not every possible fault.", "Increase interaction strength where risk or evidence demands it."]),
        ("Domain Testing", "Partitions and boundaries make large input spaces manageable.", ["Identify valid and invalid equivalence classes.", "Probe boundary values and values immediately around them.", "Consider output domains and internal ranges too."]),
        ("Model-Based Design", "Decision tables, state machines, workflows, and cause-effect models generate systematic tests.", ["Models make omissions and contradictions visible.", "Coverage can target rules, states, transitions, or paths.", "Keep the model synchronized with intended behavior."]),
    ]),
    ("testing-metrics-and-tools", "Testing Metrics and Tools", [
        ("Measurement Goals", "Metrics support decisions only when tied to a clear goal and interpreted in context.", ["Use Goal–Question–Metric: define goal, ask questions, then select measures.", "Avoid vanity metrics and gaming.", "Combine leading and lagging indicators."]),
        ("Progress Metrics", "Track planned versus executed tests, pass/fail/block rates, effort, schedule, and remaining work.", ["A high pass rate can be meaningless if coverage is weak.", "Burn-up and trend views reveal direction better than isolated totals.", "Report blockers and uncertainty, not just counts."]),
        ("Defect Metrics", "Analyze discovery, severity, density, leakage, removal efficiency, age, and reopen rate.", ["Defect density normalizes defects by product size but size measures have limitations.", "Leakage or escape rate reflects defects found in later phases or production.", "Severity and business impact matter more than raw counts."]),
        ("Coverage & Effectiveness", "Requirements, risk, code, and model coverage indicate exercised scope; effectiveness indicates detection value.", ["Coverage is necessary evidence, not a quality verdict.", "Defect detection percentage compares pre-release discoveries with total known defects.", "Mutation testing evaluates whether tests detect seeded changes."]),
        ("Tool Categories", "Tools support management, static analysis, design, execution, performance, security, data, and CI/CD.", ["Pilot tools against a real need before organization-wide adoption.", "Account for licensing, integration, training, maintenance, and false results.", "Tool output needs human interpretation."]),
        ("Metric Families & Ethics", "Base metrics are raw counts; calculated coverage, effectiveness, effort, tracking, quality, and efficiency metrics answer defined questions.", ["Effectiveness concerns detection value; efficiency relates useful output to effort.", "Segment and call-pair coverage measure different obligations.", "Metrics and tools must follow ACM/IEEE professional responsibilities rather than be manipulated as targets."]),
    ]),
    ("testing-throughout-the-sdlc", "Testing Throughout the SDLC", [
        ("Shift Left", "Start test thinking early through reviews, examples, risk analysis, and testable requirements.", ["Early feedback prevents defects and reduces rework.", "Testers collaborate in refinement, architecture, and design.", "Shift left does not mean eliminating later system testing."]),
        ("Test Levels", "Component, integration, system, and acceptance testing have distinct objects and objectives.", ["Component testing isolates units.", "Integration testing focuses on interfaces and interactions.", "System testing evaluates end-to-end behavior; acceptance testing validates business readiness."]),
        ("Development Models", "Testing is adapted to sequential, iterative, incremental, and agile lifecycles.", ["In a V-model, each development activity has a corresponding test activity.", "Iterative delivery repeats analysis, implementation, and testing.", "Continuous delivery relies on automation and rapid feedback."]),
        ("Static Testing", "Reviews and static analysis evaluate work products without executing the software.", ["Static testing can find ambiguity, inconsistency, unreachable code, standards violations, and security weaknesses early.", "Reviews range from informal review to walkthrough, technical review, and inspection.", "Static and dynamic testing are complementary."]),
        ("Maintenance Testing", "Changes, migrations, retirements, and environment updates trigger maintenance testing.", ["Analyze impact to select confirmation and regression tests.", "Data conversion and operational procedures need testing during migration.", "Retirement includes archive, restore, access, and data-retention checks."]),
        ("Integration & ISO 9126", "Integration strategy and nonfunctional characteristics determine what must be exercised beyond isolated components.", ["Component integration precedes system integration; big-bang integration weakens fault isolation.", "ISO 9126 groups functionality, reliability, usability, efficiency, maintainability, and portability.", "Confirmation checks a fix; regression checks unaffected behavior after change."]),
    ]),
    ("unit-testing-and-junit", "Unit Testing and JUnit", [
        ("Unit Test Qualities", "Good unit tests are fast, isolated, repeatable, self-checking, readable, and focused.", ["Use Arrange–Act–Assert or Given–When–Then structure.", "Test behavior and contracts rather than private implementation details.", "One conceptual reason to fail improves diagnosis."]),
        ("JUnit Lifecycle", "Annotations declare tests, setup, teardown, disabling, nesting, display names, and parameterization.", ["@Test marks a test; @BeforeEach and @AfterEach manage per-test fixtures.", "@BeforeAll and @AfterAll manage class-level resources.", "Tests should not depend on execution order."]),
        ("Assertions", "Assertions compare actual behavior with expected outcomes.", ["Use assertEquals, assertTrue, assertNull, assertThrows, assertAll, and timeout assertions appropriately.", "Messages should explain intent when failure context is not obvious.", "Floating-point comparisons need a tolerance delta."]),
        ("Fixtures & Doubles", "Fixtures establish controlled state; doubles isolate collaborators.", ["Stubs provide answers; mocks verify interactions; fakes provide lightweight working implementations.", "Mock boundaries, not every object.", "Dependency injection improves isolation and controllability."]),
        ("Parameterized Tests", "Run the same behavior over multiple input–expected-output sets.", ["Use value, CSV, method, or custom argument sources.", "Name cases so failures are understandable.", "Parameterized tests are especially useful for partitions and boundaries."]),
        ("TDD", "Red–Green–Refactor: write a failing test, make it pass minimally, then improve design safely.", ["TDD is a design and feedback discipline, not proof of complete testing.", "Keep cycles small.", "Retain regression tests while refactoring."]),
        ("JUnit Outcomes & Comparisons", "JUnit distinguishes a pass, an assertion failure, and an execution error.", ["assertEquals compares values while assertSame compares identity.", "Floating-point comparisons need a tolerance delta.", "Cleanup belongs in lifecycle hooks so it runs even after failures."]),
    ]),
    ("white-box-testing", "White Box Testing", [
        ("Structural Perspective", "White-box testing derives coverage obligations from internal structure.", ["Typical bases include control flow, data flow, calls, branches, conditions, and paths.", "It can reveal unexecuted logic invisible from requirements alone.", "Structural coverage complements specification-based testing."]),
        ("Control-Flow Testing", "Use a control-flow graph to identify statements, branches, decisions, and independent paths.", ["Nodes represent blocks; edges represent transfers of control.", "Cyclomatic complexity estimates linearly independent paths.", "Basis paths are a practical subset, not all possible paths."]),
        ("Condition Testing", "Target decisions and the atomic conditions inside them.", ["Decision coverage requires every outcome.", "Condition coverage requires each atomic condition true and false.", "MC/DC demonstrates independent effect and is used in safety-critical contexts."]),
        ("Loop Testing", "Loops need special tests because iteration counts create boundary and path risks.", ["Test zero, one, two, typical, maximum, and above-maximum where meaningful.", "For nested loops, hold outer loops minimal while varying the inner loop, then work outward.", "Watch initialization, termination, and off-by-one defects."]),
        ("Data-Flow Testing", "Trace where variables are defined, used, killed, or used before definition.", ["Definition-use pairs expose suspicious data lifecycles.", "Look for defined-but-never-used and used-before-defined anomalies.", "Data-flow coverage can reveal faults missed by branch coverage."]),
        ("Static White-Box Reviews", "Desk checks, walkthroughs, Fagan inspections, and static-analysis tools inspect internal work products without execution.", ["Walkthroughs are author-led; formal inspections use defined roles, preparation, logging, and follow-up.", "Static analysis automates rule and anomaly checks.", "White-box testing includes static examination and executable structural testing."]),
        ("Coverage Relationships", "Statement, decision, condition, decision/condition, multiple-condition, function, and path coverage provide different guarantees.", ["Condition coverage need not force every decision outcome, and decision coverage need not toggle every atomic condition.", "Multiple-condition coverage does not imply all program paths.", "Cyclomatic complexity guides a basis set of independent paths."]),
    ]),
]


def branch_parts(branch):
    """Unpack a chapter branch, tolerating the optional 4th examples element.

    Chapters may be written as (name, desc, facts) or
    (name, desc, facts, examples); examples are worked illustrations that
    belong on the mindmap but should not become extra exam questions.
    """
    name, desc, facts = branch[0], branch[1], branch[2]
    examples = list(branch[3]) if len(branch) > 3 else []
    return name, desc, list(facts), examples


def slug_label(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def mindmap_html(chapter_no: int, title: str, branches: list) -> str:
    tree = {"id": "root", "label": title, "desc": f'<span class="panel-tag">SE401 · Chapter {chapter_no}</span><p>A comprehensive concept map for <strong>{html.escape(title)}</strong>. Expand branches, select a node for detail, search topics, zoom, pan, or export the full map.</p>', "children": []}
    for branch_index, raw_branch in enumerate(branches, 1):
        name, desc, facts, examples = branch_parts(raw_branch)
        branch = {
            "id": f"branch-{branch_index}",
            "label": name,
            "desc": f'<span class="panel-tag">Core Concept</span><p>{html.escape(desc)}</p>',
            "children": [],
        }
        for fact_index, fact in enumerate(facts, 1):
            words = fact.rstrip('.').split()
            label = ' '.join(words[:7]) + ('…' if len(words) > 7 else '')
            branch["children"].append({
                "id": f"branch-{branch_index}-detail-{fact_index}",
                "label": label,
                "desc": f'<span class="panel-tag">Key Detail</span><p>{html.escape(fact)}</p>',
            })
        if examples:
            example_node = {
                "id": f"branch-{branch_index}-examples",
                "label": "Examples",
                "desc": f'<span class="panel-tag">Examples</span><p>Worked illustrations of <strong>{html.escape(name)}</strong> in real systems and code.</p>',
                "children": [],
            }
            for example_index, (example_label, example_text) in enumerate(examples, 1):
                example_node["children"].append({
                    "id": f"branch-{branch_index}-example-{example_index}",
                    "label": example_label,
                    "desc": f'<span class="panel-tag">Example</span><p>{html.escape(example_text)}</p>',
                })
            branch["children"].append(example_node)
        tree["children"].append(branch)
    text = ETHICS_MAP_TEMPLATE.read_text()
    page_title = f"{title} — SE401 Mindmap"
    description = f"Interactive SE401 Chapter {chapter_no} {title} mindmap with expandable concepts, search, zoom, pan, details, and PNG export."
    canonical = f"https://shoug-tech.com/academics/software-engineering/se401/extra-resources/mindmaps/{chapter_no:02d}-{slug_label(title)}/{slug_label(title)}.html"
    text = re.sub(r'<title>.*?</title>', f'<title>{html.escape(page_title)}</title>', text, count=1, flags=re.S)
    text = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(description, quote=True)}">', text, count=1)
    text = re.sub(r'(<meta property="og:title" content=")[^"]*(">)', rf'\1{html.escape(page_title, quote=True)}\2', text)
    text = re.sub(r'(<meta property="og:description" content=")[^"]*(">)', rf'\1{html.escape(description, quote=True)}\2', text)
    text = re.sub(r'(<meta name="twitter:title" content=")[^"]*(">)', rf'\1{html.escape(page_title, quote=True)}\2', text)
    text = re.sub(r'(<meta name="twitter:description" content=")[^"]*(">)', rf'\1{html.escape(description, quote=True)}\2', text)
    # Without these the map keeps the ETHCS303 template's canonical, so every
    # generated map declares itself a duplicate of that one ethics page.
    # scripts/fix_mindmap_canonicals.py repairs the URL once the real output
    # folder is known (callers rename the course and slug afterwards).
    text = re.sub(r'(<link rel="canonical" href=")[^"]*(">)', rf'\1{canonical}\2', text, count=1)
    text = re.sub(r'(<meta property="og:url" content=")[^"]*(">)', rf'\1{canonical}\2', text, count=1)
    text = re.sub(r'(<link rel="alternate" hreflang="(?:en|x-default)" href=")[^"]*(">)', rf'\1{canonical}\2', text)
    text = re.sub(r'(<link rel="alternate" hreflang="ar" href=")[^"]*(">)',
                  rf'\1{canonical.replace("shoug-tech.com/", "shoug-tech.com/ar/")}\2', text, count=1)
    raw_schema = '<script type="application/ld+json">' + json.dumps({"@context":"https://schema.org","@type":"WebPage","url":canonical,"name":page_title,"description":description,"isPartOf":{"@type":"WebSite","name":"Shoug's Digital Garden","url":"https://shoug-tech.com/"}}) + '</script>'
    text = re.sub(r'<script\s+type="application/ld\+json">.*?</script>', lambda _m: raw_schema, text, count=1, flags=re.S)
    text = text.replace('Moral Systems, Ethical Concepts, and Theories Mindmap', f'{html.escape(title)} Mindmap')
    text = re.sub(r'const DATA = \{.*?\n\};\n\n        // ─+\n        // STATE', lambda _m: 'const DATA = ' + json.dumps(tree, ensure_ascii=False, indent=4) + ';\n\n        // ─────────────────────────────────────────────\n        // STATE', text, count=1, flags=re.S)
    return text

    # Legacy card-map implementation retained below for reference; the live output
    # deliberately uses the Ethics node-canvas interaction model above.
    data = []
    for i, (name, desc, facts) in enumerate(branches, 1):
        data.append({"id": f"b{i}", "name": name, "desc": desc, "facts": facts})
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    return f'''<!doctype html><html lang="en" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SE401 · Chapter {chapter_no} — {html.escape(title)} Mindmap</title><meta name="description" content="Interactive SE401 {html.escape(title)} concept map with searchable definitions, relationships, and exam-focused details."><link rel="icon" href="/assets/shoug-favicon-v3.png"><style>
    :root{{--bg:#071019;--panel:#0f1d2b;--card:#14283a;--line:#2b4960;--text:#eef8ff;--muted:#9db3c5;--cyan:#38d9ff;--lime:#7bf59a;--violet:#bd7bff;--orange:#ffb454;--shadow:rgba(0,0,0,.42)}}
    [data-theme="light"]{{--bg:#eef8fc;--panel:#fff;--card:#f4fbff;--line:#b8d7e5;--text:#132632;--muted:#58707e;--cyan:#007fa3;--lime:#188340;--violet:#7041ae;--orange:#a55c00;--shadow:rgba(24,69,88,.16)}}
    *{{box-sizing:border-box}}body{{margin:0;background:radial-gradient(circle at 12% 8%,color-mix(in srgb,var(--cyan) 15%,transparent),transparent 32rem),radial-gradient(circle at 90% 80%,color-mix(in srgb,var(--violet) 14%,transparent),transparent 34rem),var(--bg);color:var(--text);font:15px/1.55 system-ui,sans-serif;min-height:100vh;transition:.25s}}
    header{{position:sticky;top:0;z-index:10;background:color-mix(in srgb,var(--bg) 84%,transparent);backdrop-filter:blur(18px);border-bottom:1px solid var(--line);padding:12px clamp(14px,3vw,42px);display:flex;gap:12px;align-items:center;flex-wrap:wrap}}h1{{font-size:clamp(18px,2.3vw,28px);margin:0 auto 0 0}}.eyebrow{{color:var(--cyan);font:700 11px ui-monospace;letter-spacing:.15em}}input{{min-width:190px;flex:0 1 280px;background:var(--panel);color:var(--text);border:1px solid var(--line);border-radius:10px;padding:10px 12px}}button{{border:1px solid var(--line);background:var(--panel);color:var(--text);border-radius:10px;padding:9px 12px;cursor:pointer}}button:hover{{border-color:var(--cyan);transform:translateY(-1px)}}
    main{{max-width:1500px;margin:auto;padding:clamp(18px,4vw,52px)}}.root{{max-width:760px;margin:0 auto 35px;text-align:center;padding:26px;border:1px solid var(--cyan);border-radius:22px;background:linear-gradient(135deg,color-mix(in srgb,var(--cyan) 16%,var(--panel)),color-mix(in srgb,var(--violet) 12%,var(--panel)));box-shadow:0 20px 60px var(--shadow);animation:rise .55s both}}.root h2{{font-size:clamp(28px,5vw,52px);margin:3px}}.root p{{color:var(--muted)}}
    .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,310px),1fr));gap:18px}}.branch{{position:relative;background:linear-gradient(145deg,var(--card),var(--panel));border:1px solid var(--line);border-radius:18px;padding:20px;box-shadow:0 12px 34px var(--shadow);animation:rise .5s both;transition:.22s}}.branch:hover{{transform:translateY(-5px);border-color:var(--cyan)}}.branch h3{{margin:0 0 8px;color:var(--lime);font-size:20px}}.branch p{{color:var(--muted);margin:0 0 14px}}.branch ul{{margin:0;padding-left:20px}}.branch li{{margin:8px 0}}.branch li::marker{{color:var(--orange)}}.hidden{{display:none}}mark{{background:var(--orange);color:#111;padding:0 2px}}.count{{color:var(--muted);font:12px ui-monospace}}
    @keyframes rise{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:none}}}}@media(prefers-reduced-motion:reduce){{*{{animation:none!important;transition:none!important}}}}@media(max-width:620px){{header{{align-items:stretch}}input{{order:3;width:100%;flex-basis:100%}}}}
    </style></head><body><header><div><div class="eyebrow">SE401 · CHAPTER {chapter_no}</div><h1>{html.escape(title)} Mindmap</h1></div><input id="search" type="search" placeholder="Search concepts and details…" aria-label="Search mindmap"><span class="count" id="count"></span><button id="expand">Collapse details</button><button id="theme" aria-label="Toggle theme">☀</button></header><main><section class="root"><div class="eyebrow">SOFTWARE TESTING & QUALITY</div><h2>{html.escape(title)}</h2><p>Explore the major concepts, then search to isolate definitions, comparisons, techniques, and exam cues.</p></section><section class="grid" id="grid"></section></main><script>
    const DATA={payload};const grid=document.getElementById('grid'),search=document.getElementById('search'),count=document.getElementById('count');let details=true;
    function esc(s){{return s.replace(/[&<>]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;'}}[c]))}}function render(q=''){{q=q.trim().toLowerCase();let shown=0;grid.innerHTML='';DATA.forEach((b,i)=>{{const hay=[b.name,b.desc,...b.facts].join(' ').toLowerCase();if(q&&!hay.includes(q))return;shown++;const card=document.createElement('article');card.className='branch';card.style.animationDelay=(i*.05)+'s';let body='<h3>'+esc(b.name)+'</h3><p>'+esc(b.desc)+'</p>';if(details)body+='<ul>'+b.facts.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul>';card.innerHTML=body;grid.appendChild(card)}});count.textContent=shown+' / '+DATA.length+' branches'}}
    search.addEventListener('input',()=>render(search.value));document.getElementById('expand').onclick=e=>{{details=!details;e.currentTarget.textContent=details?'Collapse details':'Expand details';render(search.value)}};const root=document.documentElement;try{{root.dataset.theme=localStorage.getItem('shoug-theme')||'dark'}}catch(e){{}}document.getElementById('theme').onclick=()=>{{root.dataset.theme=root.dataset.theme==='dark'?'light':'dark';try{{localStorage.setItem('shoug-theme',root.dataset.theme)}}catch(e){{}}}};render();
    </script></body></html>'''


def exam_html(chapter_no: int, title: str, branches: list) -> str:
    facts = []
    for raw_branch in branches:
        name, desc, details, _examples = branch_parts(raw_branch)
        facts.append((name, desc))
        facts.extend((name, d) for d in details)
    # Every concept written into the slide-audited chapter model becomes an MCQ.
    # Keeping this exhaustive prevents later additions to a mindmap from silently
    # disappearing from its companion exam.
    selected = facts
    mcqs = []
    labels = [b[0] for b in branches]
    prompts = [
        'Which concept best matches this statement? “{statement}”',
        'During a review, the team identifies this concern: “{statement}” Which topic should guide the response?',
        'Which chapter area includes the following principle or practice? “{statement}”',
    ]
    for i, (topic, statement) in enumerate(selected):
        distract = [x for x in labels if x != topic]
        opts = [topic] + distract[:3]
        shift = i % len(opts)
        opts = opts[shift:] + opts[:shift]
        mcqs.append({"q": prompts[i % len(prompts)].format(statement=statement), "options": opts, "correct": opts.index(topic), "why": f"{topic} is correct because this statement describes its defining purpose or practice. The other choices cover different concerns within {title}."})
    shorts = []
    for raw_branch in branches:
        topic, statement = raw_branch[0], raw_branch[1]
        words = [w.lower() for w in re.findall(r"[A-Za-z]{5,}", statement) if w.lower() not in {"which","their","about","these","through","where","every"}][:3]
        shorts.append({"q": f"In 1–2 sentences, explain {topic} and include one important detail.", "keywords": [topic.lower()] + words, "answer": statement})
    payload_m = json.dumps(mcqs).replace("</", "<\\/")
    payload_s = json.dumps(shorts).replace("</", "<\\/")
    question_count = len(mcqs) + len(shorts)
    max_points = len(mcqs) + len(shorts) * 2
    minutes = max(35, ((question_count * 3 + 1) // 2 // 5) * 5)
    return f'''<!doctype html><html lang="en" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SE401 · Chapter {chapter_no} Quiz — {html.escape(title)}</title><meta name="description" content="Self-graded SE401 {html.escape(title)} chapter exam with explanations and model answers."><link rel="icon" href="/assets/shoug-favicon-v3.png"><style>
    :root{{--bg:#0b1020;--panel:#141c31;--card:#19243b;--text:#f4f7ff;--muted:#aab6cc;--line:#34415e;--purple:#bb72ff;--cyan:#42dcff;--green:#54d889;--red:#ff6475;--gold:#f5b94c}}[data-theme="light"]{{--bg:#f5f4fb;--panel:#fff;--card:#f9f8ff;--text:#1c2435;--muted:#5e687b;--line:#d6d7e5;--purple:#7536b5;--cyan:#007c9a;--green:#14753b;--red:#ba2c41;--gold:#9a6100}}*{{box-sizing:border-box}}body{{margin:0;background:radial-gradient(circle at 12% 5%,color-mix(in srgb,var(--purple) 15%,transparent),transparent 34rem),radial-gradient(circle at 90% 35%,color-mix(in srgb,var(--cyan) 12%,transparent),transparent 30rem),var(--bg);color:var(--text);font:16px/1.55 system-ui,sans-serif;min-height:100vh}}.top{{position:sticky;top:0;z-index:10;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(16px);border-bottom:1px solid var(--line)}}.topin,main{{max-width:1450px;margin:auto;padding:14px clamp(14px,4vw,58px)}}.topin{{display:flex;align-items:center;gap:14px}}.brand{{margin-right:auto}}.eyebrow{{font:700 11px ui-monospace;color:var(--cyan);letter-spacing:.16em}}button{{cursor:pointer}}.timer,.theme{{border:1px solid var(--line);border-radius:10px;background:var(--panel);color:var(--text);padding:9px 12px;font:600 14px ui-monospace}}.hero{{padding:clamp(28px,6vw,72px) 0 28px}}h1{{font-size:clamp(34px,6vw,68px);line-height:1;margin:8px 0;background:linear-gradient(100deg,var(--text),var(--purple),var(--cyan));background-clip:text;color:transparent}}.hero p{{max-width:850px;color:var(--muted)}}.meta{{display:flex;gap:16px;flex-wrap:wrap;font:13px ui-monospace;color:var(--muted)}}.progress{{height:7px;background:var(--line);border-radius:9px;overflow:hidden;margin:24px 0}}.progress i{{display:block;width:0;height:100%;background:linear-gradient(90deg,var(--purple),var(--cyan));transition:.25s}}section{{background:linear-gradient(135deg,var(--panel),color-mix(in srgb,var(--purple) 5%,var(--panel)));border:1px solid var(--line);border-radius:18px;padding:clamp(16px,3vw,30px);margin:20px 0;box-shadow:0 18px 50px rgba(0,0,0,.18)}}section h2{{margin-top:0}}.q{{border-top:1px solid var(--line);padding:22px 0}}.q:first-of-type{{border-top:0}}.qnum{{color:var(--gold);font:700 13px ui-monospace}}.prompt{{font-weight:650;margin:7px 0 13px}}label{{display:block;border:1px solid var(--line);background:var(--card);border-radius:11px;padding:11px 13px;margin:8px 0;transition:.18s}}label:hover{{border-color:var(--cyan);transform:translateX(4px)}}textarea{{width:100%;min-height:100px;border:1px solid var(--line);background:var(--card);color:var(--text);border-radius:11px;padding:12px;font:inherit}}.feedback{{display:none;margin-top:12px;padding:14px;border:2px solid transparent;border-radius:10px}}.feedback.show{{display:block}}.correct{{border-color:var(--green)!important;background:color-mix(in srgb,var(--green) 24%,var(--card))!important;color:var(--text);box-shadow:inset 5px 0 0 var(--green),0 0 0 1px color-mix(in srgb,var(--green) 35%,transparent)}}.wrong{{border-color:var(--red)!important;background:color-mix(in srgb,var(--red) 24%,var(--card))!important;color:var(--text);box-shadow:inset 5px 0 0 var(--red),0 0 0 1px color-mix(in srgb,var(--red) 35%,transparent)}}label.correct::after{{content:' ✓  CORRECT';float:right;color:var(--green);font-weight:900}}label.wrong::after{{content:' ✕  YOUR ANSWER';float:right;color:var(--red);font-weight:900}}textarea.correct,textarea.wrong{{border-width:3px}}.actions{{text-align:center;padding:20px}}.submit{{border:0;border-radius:12px;background:linear-gradient(105deg,var(--purple),var(--cyan));color:white;padding:14px 28px;font-weight:800;font-size:16px;box-shadow:0 12px 35px color-mix(in srgb,var(--purple) 30%,transparent)}}.score{{display:none;text-align:center;font-size:clamp(24px,5vw,48px);padding:22px;border:3px solid transparent;border-radius:16px}}.score.show{{display:block}}.score.pass{{border-color:var(--green);background:color-mix(in srgb,var(--green) 20%,var(--panel))}}.score.fail{{border-color:var(--red);background:color-mix(in srgb,var(--red) 20%,var(--panel))}}@media(prefers-reduced-motion:reduce){{*{{transition:none!important}}}}
    </style></head><body><div class="top"><div class="topin"><div class="brand"><div class="eyebrow">SE401 · CHAPTER {chapter_no}</div><strong>{html.escape(title)} — Chapter Quiz</strong></div><div class="timer" id="timer">{minutes}:00</div><button class="theme" id="theme" aria-label="Toggle theme">☀</button></div></div><main><header class="hero"><div class="eyebrow">SELF-GRADED · COMPREHENSIVE PRACTICE</div><h1>{html.escape(title)}</h1><p>Apply the chapter’s definitions, distinctions, techniques, and quality implications. Submit for instant grading; every item includes an explanation or model answer.</p><div class="meta"><b>{question_count} questions</b><span>{len(mcqs)} MCQ + {len(shorts)} short answer</span><span>{max_points} points</span><span>{minutes} minutes</span></div><div class="progress"><i id="bar"></i></div></header><section><h2>Multiple Choice — Concept Application</h2><div id="mcq"></div></section><section><h2>Short Answer — Explain and Connect</h2><div id="short"></div></section><div class="actions"><button class="submit" id="submit">Submit Exam</button><button class="theme" id="reset" hidden>Reset</button></div><div class="score" id="score"></div></main><script>
    const MCQ={payload_m},SHORT={payload_s};const mc=document.getElementById('mcq'),sa=document.getElementById('short');MCQ.forEach((x,i)=>mc.insertAdjacentHTML('beforeend','<article class="q" data-i="'+i+'"><span class="qnum">Q'+(i+1)+'</span><div class="prompt">'+x.q+'</div>'+x.options.map((o,j)=>'<label><input type="radio" name="m'+i+'" value="'+j+'"> '+String.fromCharCode(65+j)+'. '+o+'</label>').join('')+'<div class="feedback" id="fm'+i+'"></div></article>'));SHORT.forEach((x,i)=>sa.insertAdjacentHTML('beforeend','<article class="q"><span class="qnum">Q'+(MCQ.length+i+1)+'</span><div class="prompt">'+x.q+'</div><textarea id="s'+i+'" placeholder="Write your answer…"></textarea><div class="feedback" id="fs'+i+'"></div></article>'));
    function update(){{const done=document.querySelectorAll('input:checked').length+[...document.querySelectorAll('textarea')].filter(x=>x.value.trim()).length;document.getElementById('bar').style.width=(done/(MCQ.length+SHORT.length)*100)+'%'}}document.addEventListener('input',update);let left={minutes * 60},t=setInterval(()=>{{left--;document.getElementById('timer').textContent=String(Math.floor(left/60)).padStart(2,'0')+':'+String(left%60).padStart(2,'0');if(left<=0){{clearInterval(t);grade()}}}},1000);
    function grade(){{clearInterval(t);let points=0;MCQ.forEach((x,i)=>{{const inputs=[...document.querySelectorAll('input[name=m'+i+']')],chosen=inputs.find(n=>n.checked),f=document.getElementById('fm'+i);inputs.forEach(n=>{{n.disabled=true;if(+n.value===x.correct)n.closest('label').classList.add('correct')}});if(chosen&&+chosen.value===x.correct){{points++;f.className='feedback show correct';f.innerHTML='<b>✓ Correct.</b> '+x.why}}else{{if(chosen)chosen.closest('label').classList.add('wrong');f.className='feedback show wrong';f.innerHTML='<b>✕ Incorrect. Correct answer: '+String.fromCharCode(65+x.correct)+'. '+x.options[x.correct]+'.</b> '+x.why}}}});SHORT.forEach((x,i)=>{{const area=document.getElementById('s'+i),v=area.value.toLowerCase(),hits=x.keywords.filter(k=>v.includes(k)).length,earned=Math.min(2,hits),state=earned>=1?'correct':'wrong';points+=earned;area.classList.add(state);const f=document.getElementById('fs'+i);f.className='feedback show '+state;f.innerHTML='<b>'+(earned>=1?'✓ Credit earned':'✕ Needs review')+' ('+earned+'/2 by keyword check).</b> Model answer: '+x.answer;area.disabled=true}});const maxPoints=MCQ.length+SHORT.length*2,passed=points/maxPoints>=.6,score=document.getElementById('score');score.className='score show '+(passed?'pass':'fail');score.innerHTML='<b>'+(passed?'✓ ':'✕ ')+points+' / '+maxPoints+'</b><br><small>Review the color-coded answers above, then retry to strengthen weak areas.</small>';document.getElementById('submit').hidden=true;document.getElementById('reset').hidden=false}}document.getElementById('submit').onclick=grade;document.getElementById('reset').onclick=()=>location.reload();const root=document.documentElement;try{{root.dataset.theme=localStorage.getItem('shoug-theme')||'dark'}}catch(e){{}}document.getElementById('theme').onclick=()=>{{root.dataset.theme=root.dataset.theme==='dark'?'light':'dark';try{{localStorage.setItem('shoug-theme',root.dataset.theme)}}catch(e){{}}}};
    </script></body></html>'''


def transform_reference(text: str, chapter_no: int, old_slug: str, old_title: str, new_slug: str, new_title: str, kind: str) -> str:
    text = text.replace("se423", "se401").replace("SE423", "SE401")
    old_exam = f"{old_slug}-quiz"
    new_exam = f"{new_slug}-quiz"
    text = text.replace(old_exam, new_exam)
    text = re.sub(rf'(?<=/{chapter_no:02d}-){re.escape(old_slug)}(?=/|\")', new_slug, text)
    text = text.replace(old_title, new_title)
    text = re.sub(rf"Chapter\s+{chapter_no}:?\s*[^<\n]*Quiz", f"Chapter {chapter_no}: {new_title} Quiz", text)
    if kind == "exam":
        text = re.sub(r'(<iframe\b[^>]*\bsrc=")[^"]+', rf'\1./{new_exam}.html', text, count=1)
    else:
        text = re.sub(r'(<iframe\b[^>]*\bsrc=")[^"]+', rf'\1./{new_slug}.html', text, count=1)
    active_section = "Exams" if kind == "exam" else "Study Material"
    text = sitegen.replace_academic_sidebar(text, "SE401", active_section)
    if kind == "exam":
        rows = []
        for index, (slug, label, *_rest) in enumerate(CHAPTERS, 1):
            folder = f"{index:02d}-{slug}-quiz"
            active = slug == new_slug
            rows.append(
                f'<li class="tree-item tree-viewer{" file-active" if active else ""}"><a class="tree-file" '
                f'href="/academics/software-engineering/se401/exams/{folder}/">'
                f'{"<span class=\"status-dot\"></span>" if active else ""}Chapter {index}: {html.escape(label)} Quiz</a></li>'
            )
        children = '<ul class="tree-children item-children is-open">' + ''.join(rows) + '</ul>'
        text = re.sub(
            r'(<li class="tree-item tree-section file-active"><a class="tree-file"[^>]+>.*?EXAMS</a></li>)(?:<ul class="tree-children item-children is-open">.*?</ul>)?',
            r'\1' + children, text, count=1, flags=re.S,
        )
    canonical = f"https://shoug-tech.com/academics/software-engineering/se401/{'exams' if kind == 'exam' else 'extra-resources/mindmaps'}/{chapter_no:02d}-{new_slug}{'-quiz' if kind == 'exam' else ''}/"
    page_name = f"SE401 · Chapter {chapter_no} {'Quiz' if kind == 'exam' else 'Mindmap'} — {new_title}"
    page_desc = f"Interactive SE401 Chapter {chapter_no} {new_title} {'self-graded practice exam' if kind == 'exam' else 'concept map'} from Shoug's Digital Garden."
    text = re.sub(r'<title>.*?</title>', f'<title>{html.escape(page_name)}</title>', text, count=1, flags=re.S)
    text = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(page_desc, quote=True)}">', text, count=1)
    text = re.sub(r'<link rel="canonical"\s+href="[^"]+">', f'<link rel="canonical" href="{canonical}">', text, count=1)
    text = re.sub(r'(<link rel="alternate" hreflang="(?:en|x-default)"\s+href=")[^"]+', lambda m: m.group(1) + canonical, text)
    text = re.sub(r'(<link rel="alternate" hreflang="ar"\s+href=")[^"]+', lambda m: m.group(1) + canonical.replace('.com/', '.com/ar/'), text)
    text = re.sub(r'(<meta property="og:title" content=")[^"]*(">)', rf'\1{html.escape(page_name, quote=True)}\2', text)
    text = re.sub(r'(<meta property="og:description"\s+content=")[^"]*(">)', rf'\1{html.escape(page_desc, quote=True)}\2', text)
    text = re.sub(r'(<meta property="og:url"\s+content=")[^"]*(">)', rf'\1{canonical}\2', text)
    text = re.sub(r'(<meta name="twitter:title" content=")[^"]*(">)', rf'\1{html.escape(page_name, quote=True)}\2', text)
    text = re.sub(r'(<meta name="twitter:description"\s+content=")[^"]*(">)', rf'\1{html.escape(page_desc, quote=True)}\2', text)
    structured_data = '<script type="application/ld+json">' + json.dumps({"@context":"https://schema.org","@type":"WebPage","url":canonical,"name":page_name,"description":page_desc,"isPartOf":{"@type":"WebSite","name":"Shoug\'s Digital Garden","url":"https://shoug-tech.com/"}}) + '</script>'
    text = re.sub(r'<script\s+type="application/ld\+json">.*?</script>', lambda _match: structured_data, text, count=1, flags=re.S)
    raw_file = new_exam + '.html' if kind == 'exam' else new_slug + '.html'
    text = re.sub(r'(<a class="btn btn-primary" href=")[^"]+("[^>]*>)', rf'\1./{raw_file}\2', text, count=1)
    route_base = '/academics/software-engineering/se401/exams/' if kind == 'exam' else '/academics/software-engineering/se401/extra-resources/mindmaps/'
    previous_route = route_base if chapter_no == 1 else route_base + f'{chapter_no-1:02d}-{CHAPTERS[chapter_no-2][0]}{"-quiz" if kind == "exam" else ""}/'
    next_route = route_base if chapter_no == len(CHAPTERS) else route_base + f'{chapter_no+1:02d}-{CHAPTERS[chapter_no][0]}{"-quiz" if kind == "exam" else ""}/'
    text = re.sub(r'<div class="nav-strip"[^>]*>.*?</div>', f'<div class="nav-strip"><a href="{previous_route}" class="nav-link prev">&lt;- PREVIOUS</a><a href="{next_route}" class="nav-link next">NEXT -&gt;</a></div>', text, count=1, flags=re.S)
    text = text.replace('/Academics/courses/se401/', '/academics/software-engineering/se401/')
    text = text.replace('/academics/software-engineering/se401/study-material/', '/academics/software-engineering/se401/extra-resources/')
    text = text.replace('/academics/software-engineering/se401/quizzes/', '/academics/software-engineering/se401/exams/')
    text = re.sub(r'<li class="tree-item tree-section"><a class="tree-file" href="/academics/software-engineering/se401/exams/"[^>]*>QUIZZES</a></li>', '', text)
    return re.sub(r'[ \t]+\n', '\n', text)


def write_wrappers() -> None:
    old = [
        ("change-management", "Change Management"), ("development-approach", "Development Approach"),
        ("estimation", "Estimation"), ("introduction", "Introduction"),
        ("project-performance-domains", "Project Performance Domains"), ("quality", "Quality"),
        ("risk-management", "Risk Management"), ("scheduling-and-tracking", "Scheduling and Tracking"),
        ("software-engineering", "Software Engineering"), ("stakeholders", "Stakeholders"),
        ("tailoring-models-methods-and-artifacts", "Tailoring Models, Methods & Artifacts"), ("team", "Team"),
    ]
    for i, (slug, title, *_rest) in enumerate(CHAPTERS, 1):
        ref_i = min(i, 12)
        old_slug, old_title = old[ref_i - 1]
        map_ref = REF / f"extra-resources/mindmaps/{ref_i:02d}-{old_slug}/index.html"
        exam_ref = REF / f"exams/{ref_i:02d}-{old_slug}-quiz/index.html"
        map_dest = MAPS / f"{i:02d}-{slug}"
        exam_dest = EXAMS / f"{i:02d}-{slug}-quiz"
        map_dest.mkdir(parents=True, exist_ok=True); exam_dest.mkdir(parents=True, exist_ok=True)
        map_dest.joinpath("index.html").write_text(transform_reference(map_ref.read_text(), ref_i, old_slug, old_title, slug, title, "map"))
        exam_dest.joinpath("index.html").write_text(transform_reference(exam_ref.read_text(), ref_i, old_slug, old_title, slug, title, "exam"))


def replace_rows(hub: str, kind: str) -> str:
    rows = []
    for i, (slug, title, *_rest) in enumerate(CHAPTERS, 1):
        folder = f"{i:02d}-{slug}" + ("-quiz" if kind == "exam" else "")
        label = f"Chapter {i}: {title}" + (" Quiz" if kind == "exam" else " Mindmap")
        route_base = "exams" if kind == "exam" else "extra-resources/mindmaps"
        rows.append(f'<a class="dir-row" href="/academics/software-engineering/se401/{route_base}/{folder}/"><div class="dir-num">{i}</div><div class="dir-title">{html.escape(label)}</div><div class="dir-status"><span class="status-tag available">AVAILABLE</span></div><div class="dir-arrow">-&gt;</div></a>')
    block = '<div class="directory-container"><div class="dir-header"><span>SEQ</span><span>DESCRIPTOR</span><span>SYS_STATE</span><span></span></div>' + ''.join(rows) + '</div>\n'
    hub = re.sub(r'<div class="directory-container">.*?(?=<footer class="shoug-site-footer">)', block, hub, count=1, flags=re.S)
    hub = sitegen.replace_academic_sidebar(hub, "SE401", "Exams" if kind == "exam" else "Study Material")
    return re.sub(r'[ \t]+\n', '\n', hub)


def main() -> None:
    MAPS.mkdir(parents=True, exist_ok=True); EXAMS.mkdir(parents=True, exist_ok=True)
    for i, (slug, title, branches) in enumerate(CHAPTERS, 1):
        mp = MAPS / f"{i:02d}-{slug}"; ep = EXAMS / f"{i:02d}-{slug}-quiz"
        mp.mkdir(parents=True, exist_ok=True); ep.mkdir(parents=True, exist_ok=True)
        mp.joinpath(f"{slug}.html").write_text(mindmap_html(i, title, branches))
        ep.joinpath(f"{slug}-quiz.html").write_text(exam_html(i, title, branches))
    write_wrappers()
    map_hub = (REF / "extra-resources/mindmaps/index.html").read_text().replace("se423", "se401").replace("SE423", "SE401")
    exam_hub = (REF / "exams/index.html").read_text().replace("se423", "se401").replace("SE423", "SE401")
    MAPS.joinpath("index.html").write_text(replace_rows(map_hub, "map"))
    EXAMS.joinpath("index.html").write_text(replace_rows(exam_hub, "exam"))
    extra_hub_path = BASE / "extra-resources/index.html"
    extra_hub = extra_hub_path.read_text()
    folder_icon = '<svg class="dir-folder-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square" stroke-linejoin="square" aria-hidden="true"><path d="M3 7a1 1 0 0 1 1-1h5l2 2h9a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V7z"/></svg>'
    resource_rows = f'''<div class="directory-container"><div class="dir-header"><span>SEQ</span><span>DESCRIPTOR</span><span>SYS_STATE</span><span></span></div>
        <a class="dir-row" href="/academics/software-engineering/se401/extra-resources/mindmaps/"><div class="dir-num">1</div><div class="dir-title"><span class="dir-title-text">Mindmaps</span>{folder_icon}</div><div class="dir-status"><span class="status-tag available">AVAILABLE</span></div><div class="dir-arrow">-&gt;</div></a>
        <a class="dir-row" href="/academics/software-engineering/se401/extra-resources/summary/"><div class="dir-num">2</div><div class="dir-title">Course Summary</div><div class="dir-status"><span class="status-tag available">AVAILABLE</span></div><div class="dir-arrow">-&gt;</div></a></div>'''
    extra_hub = re.sub(r'<style id="empty-section-state-style">.*?<div class="coming-soon-container".*?</div>\s*</div>', resource_rows, extra_hub, count=1, flags=re.S)
    extra_hub = extra_hub.replace('<div class="dir-title">Mindmaps</div>', f'<div class="dir-title"><span class="dir-title-text">Mindmaps</span>{folder_icon}</div>')
    extra_hub = extra_hub.replace(f'{folder_icon}<span class="dir-title-text">Mindmaps</span>', f'<span class="dir-title-text">Mindmaps</span>{folder_icon}')
    if '.dir-folder-icon {' not in extra_hub:
        extra_hub = extra_hub.replace('</style>', '''
        .dir-title:has(.dir-folder-icon) { display: flex; align-items: center; gap: 10px; }
        .dir-folder-icon { width: 20px; height: 20px; flex: 0 0 auto; color: var(--text-tertiary); transition: color .2s ease, transform .2s ease; }
        .dir-row:hover .dir-folder-icon { color: var(--brand-purple); transform: translateY(-1px); }
        </style>''', 1)
    extra_hub_path.write_text(re.sub(r'[ \t]+\n', '\n', extra_hub))
    print(f"Built {len(CHAPTERS)} SE401 mindmaps and {len(CHAPTERS)} SE401 exams")
    from fix_mindmap_sidebar_state import apply_course
    apply_course("se401", BASE)
    from fix_academic_sidebar_links import fix_page
    for page in [MAPS / "index.html", EXAMS / "index.html", *MAPS.glob("*/index.html"), *EXAMS.glob("*/index.html")]:
        fix_page(page)


if __name__ == "__main__":
    main()

"""SE401 annotated slides — every Software Testing and Quality deck.

One module holds all the decks: each deck is a namespace class with DECK and ANN (and AUTO_SLIDES).
Slides without an ANN entry are shown without notes. Three decks (Software Quality, Code Coverage,
Regression Testing) embed fonts with no text layer, so every slide in them is shown as the original
image (whole=True) with the notes beside it. See cs331_annotated/ch01_1_introduction.py for the ANN keys."""
from .common import DECKS, mcq, see, short, tf, tip, trap, trick


def deck(key, title, chapter, lede):
    slug, file, folder, _ = DECKS[key]
    return {'key': key, 'slug': slug, 'file': file, 'title': title, 'chapter': chapter,
            'pdf': '/academics/software-engineering/se401/slides/%s/' % folder, 'lede': lede}


def images(count, ann):
    """Every slide shown whole (the deck has no text layer), keeping the notes in ann."""
    return {n: dict(ann.get(n, {}), whole=True) for n in range(1, count + 1)}


ERRORS = 'A human makes an ERROR (mistake) → it leaves a DEFECT (fault, bug) in the code → running it may cause a FAILURE (wrong observable behaviour).'
PRINCIPLES = ('Seven principles: testing shows presence of defects (not absence) · exhaustive testing is impossible · early testing · '
              'defect clustering · pesticide paradox · testing is context dependent · absence-of-errors fallacy.')


class introduction:
    AUTO_SLIDES = True
    DECK = deck('d01', 'Introduction to Software Testing', 'Introduction',
                'Why testing is necessary (famous failures, the cost of poor quality), errors vs. defects vs. failures, '
                'what testing is and its objectives, test concepts (test case, oracle, scaffolding, fixture, suite, '
                'adequacy), the seven testing principles, the fundamental test process, the psychology of testing and '
                'independence, and the limits of testing.')
    ANN = {
        4: dict(notes=['Testing reduces the risk of failures in operation (Ariane 5, Therac-25, failed satellites, bank errors): poor quality is very expensive.']),
        11: dict(notes=['Ariane 5 (1996): reused Ariane 4 code overflowed converting a 64-bit float to a 16-bit integer: not a coding slip, an untested assumption.']),
        44: dict(notes=[ERRORS], tips=[tip(ERRORS)],
                 exam=[mcq('A programmer types < instead of <=. The wrong operator in the code is a:', ['Defect (fault)', 'Failure', 'Error message', 'Test oracle'], 0, 'The typing mistake is the error; the result in the code is the defect.'),
                       tf('Every defect causes a failure.', False, 'Only if the defective code is executed under the right conditions.')], weight=3),
        50: dict(notes=['Verdicts: pass, fail, inconclusive.']),
        53: dict(notes=['Test oracle: the mechanism that decides whether an output is correct (expected results, a reference implementation, assertions).'],
                 exam=[mcq('The source that tells you the expected result of a test is the:', ['Test oracle', 'Test driver', 'Test stub', 'Test fixture'], 0, '')], weight=3),
        55: dict(notes=['Fixture: the fixed state the tests run against. Suite: a collection of test cases. Scaffolding: drivers, stubs, harnesses.']),
        65: dict(notes=[PRINCIPLES], tips=[tip(PRINCIPLES)], weight=3),
        67: dict(notes=['Testing can show defects are present, never that they are absent.']),
        68: dict(notes=['Exhaustive testing is impossible except in trivial cases: use risk and priorities.']),
        70: dict(notes=['Defect clustering: a small number of modules contain most of the defects (Pareto).']),
        71: dict(notes=['Pesticide paradox: repeating the same tests finds no new bugs: review and add tests regularly.'],
                 exam=[mcq('Running the same tests over and over stops finding new defects. This is the:', ['Pesticide paradox', 'Defect clustering principle', 'Absence-of-errors fallacy', 'Early testing principle'], 0, '')], weight=3),
        73: dict(notes=['Absence-of-errors fallacy: a bug-free system that doesn’t meet users’ needs is still a failure.']),
        74: dict(notes=['Fundamental test process: planning and control → analysis and design → implementation and execution → evaluating exit criteria and reporting → test closure.']),
        82: dict(notes=['Psychology: testers need curiosity, professional pessimism, attention to detail, good communication; report defects objectively.']),
        84: dict(notes=['Independence levels: the author tests their own code → another developer → an independent test team → outside organization. More independence finds different defects.']),
        91: dict(notes=['"Program testing can be used to show the presence of bugs, but never to show their absence." (Dijkstra)']),
    }


class sdlc:
    AUTO_SLIDES = True
    DECK = deck('d02', 'Testing throughout the Software Development Life Cycle', 'Testing throughout the SDLC',
                'Verification vs. validation, the V-model and iterative models, the test levels (component, '
                'integration, system, acceptance) with their objectives, test basis and typical defects, the test types '
                '(functional, non-functional, structural, change-related), and maintenance testing.')
    VV = 'Verification: "Are we building the product RIGHT?" (meets its specification). Validation: "Are we building the RIGHT product?" (meets users’ needs).'
    ANN = {
        4: dict(notes=[VV], tips=[tip(VV)],
                exam=[mcq('"Are we building the right product?" is:', ['Validation', 'Verification', 'Regression', 'Inspection'], 0, '')], weight=3),
        5: dict(notes=['V-model: each development phase on the left has a matching test level on the right (requirements ↔ acceptance, design ↔ system/integration, code ↔ component).']),
        7: dict(notes=['Testing should begin as early as possible: reviews of requirements and designs find defects when they are cheapest.']),
        13: dict(notes=['Component (unit) testing: individual components in isolation, usually by developers, often with stubs and drivers.']),
        18: dict(notes=['Integration testing: interfaces and interactions between components (component integration) or systems (system integration).']),
        23: dict(notes=['System testing: the behaviour of the whole system against the requirements, in an environment close to production.']),
        28: dict(notes=['Acceptance testing: establish confidence that the system is fit for use: user acceptance, operational, contract and regulation, alpha and beta.'],
                 exam=[mcq('Testing against contract requirements before the customer signs off is:', ['Contract acceptance testing', 'Component testing', 'Smoke testing', 'Integration testing'], 0, '')], weight=3),
        32: dict(notes=['Functional testing: WHAT the system does. Non-functional: HOW WELL (performance, load, usability, security, reliability).']),
        38: dict(notes=['Confirmation testing (re-testing): check that a fixed defect is really fixed. Regression testing: check that the change broke nothing else.'],
                 tips=[trap('Re-testing confirms the FIX; regression testing looks for SIDE EFFECTS.')],
                 exam=[mcq('Running the failed test again after a bug fix is:', ['Confirmation testing (re-testing)', 'Regression testing', 'Smoke testing', 'Exploratory testing'], 0, '')], weight=3),
        41: dict(notes=['Maintenance testing: triggered by modifications, migration or retirement of a live system; includes impact analysis and regression testing.']),
    }


class software_quality:
    AUTO_SLIDES = True
    DECK = deck('d03', 'Software Quality', 'Software Quality',
                'Factors in project success and failure (Chaos report), the HealthCare.gov launch case study, '
                'reliability metrics (MTTF, MTTR, MTBF, availability), the spectrum of quality attributes '
                '(correctness, reliability, robustness, safety…), the cost of quality and of defects, verification '
                'and validation, the V-model and the levels of testing.')
    ANN = images(79, {
        6: dict(notes=['Chaos report: only a minority of projects succeed (on time, on budget, full scope); the rest are challenged or fail.']),
        9: dict(notes=['HealthCare.gov (2013): ~$500M+, crashed at launch: changing requirements, late and inadequate testing (no end-to-end test until days before launch), poor management.'],
                exam=[short('Name two software-engineering failures behind the HealthCare.gov launch.', 'Inadequate testing (full testing only weeks or days before launch, no end-to-end or load testing close to real volume) and constantly changing requirements combined with a write-everything-then-build process; also poor coordination among contractors.')], weight=3),
        24: dict(notes=['MTTF: mean time to failure. MTTR: mean time to repair. MTBF = MTTF + MTTR.']),
        25: dict(notes=['Availability = MTTF / (MTTF + MTTR) × 100%.'],
                 exam=[mcq('MTTF = 98 hours, MTTR = 2 hours. Availability =', ['98%', '96%', '2%', '100%'], 0, '98 / 100.')], weight=3),
        27: dict(notes=['"Five nines" (99.999%) availability ≈ 5 minutes of downtime a year.']),
        33: dict(notes=['Qualities: correctness, reliability, robustness, safety, performance, usability, security, maintainability, reusability, portability, interoperability.']),
        34: dict(notes=['Correctness: consistent with the specification (all or nothing). Reliability: probability of operating without failure under a usage profile (statistical).']),
        35: dict(notes=['Safety: prevents undesirable behaviours (hazards). Robustness: behaves reasonably (degrades gracefully) outside normal conditions.'],
                 exam=[mcq('A system that keeps working in a degraded mode when the network fails is:', ['Robust', 'Correct', 'Portable', 'Reusable'], 0, '')], weight=3),
        48: dict(notes=['Cost of quality: prevention (training, reviews) + appraisal (testing) + internal failure (rework before release) + external failure (after release: support, recalls).']),
        55: dict(notes=['The later a defect is found, the more it costs to fix (up to 100× after release).']),
        59: dict(notes=['Verification: does it meet the specification? Validation: does it meet the user’s real needs?'], seen=[see('d02', 4, 'V&V')]),
        68: dict(notes=['V-model: user requirements ↔ acceptance test, system spec ↔ system test, design ↔ integration test, code ↔ unit test.']),
        77: dict(notes=['Alpha testing: by potential users at the developer’s site (controlled). Beta: by real users in their own environment.']),
    })


class quality:
    AUTO_SLIDES = True
    DECK = deck('d04', 'Quality Assurance, Quality Control and Metrics', 'Quality',
                'Definitions of software quality, quality assurance vs. quality control, the SQA group’s role, what makes '
                'projects succeed or fail, and software measurement: measures, metrics, product vs. process metrics, '
                'direct vs. indirect measures and size-oriented metrics.')
    ANN = {
        7: dict(notes=['Quality assurance (QA): PROCESS-oriented, preventive: make sure the right processes are followed so defects aren’t introduced.']),
        10: dict(notes=['Quality control (QC): PRODUCT-oriented, detective: inspect and test the product to find defects.'],
                 tips=[trick('QA = prevent (process). QC = detect (product). Testing is part of QC.')],
                 exam=[mcq('Testing a product to find defects is an example of:', ['Quality control', 'Quality assurance', 'Configuration management', 'Risk acceptance'], 0, '')], weight=3),
        21: dict(notes=['Success factors: executive support, user involvement, experienced project manager, clear objectives, small scope, standard infrastructure.']),
        29: dict(notes=['Measure: a quantitative value of an attribute. Metric: a measure related to a goal (defects per KLOC).']),
        32: dict(notes=['Product metrics (size, complexity, defects), process metrics (effort, defect-removal efficiency), project metrics (cost, schedule).']),
        38: dict(notes=['Direct measures: LOC, execution speed, defects. Indirect: functionality, quality, complexity, maintainability.']),
        45: dict(notes=['Size-oriented metrics normalise by size: errors per KLOC, cost per KLOC, pages of documentation per KLOC.'],
                 exam=[mcq('12 defects in 4,000 lines of code is:', ['3 defects per KLOC', '12 defects per KLOC', '0.3 defects per KLOC', '48 defects per KLOC'], 0, '')], weight=3),
    }


class test_cases:
    AUTO_SLIDES = True
    DECK = deck('d05', 'Test Cases', 'Test Cases',
                'Test selection, what a test case is and what makes a good one, the triangle example, why we write test '
                'cases, when testing is complete, test scaffolding (drivers, stubs, harnesses), test oracles, defect '
                'tracking and smoke tests.')
    ANN = {
        6: dict(notes=['Test case: inputs, preconditions, expected results and postconditions for one test objective. Must be repeatable.']),
        9: dict(notes=['Good test cases: simple, one thing at a time, traceable to requirements, with a clear expected result.']),
        14: dict(notes=['Triangle problem: classify three sides as equilateral, isosceles, scalene, or not a triangle: include invalid inputs (0, negatives, a + b ≤ c).'],
                 exam=[short('Give three test cases for a program that classifies a triangle from three integer sides.', '(3, 3, 3) → equilateral; (3, 3, 4) → isosceles; (3, 4, 5) → scalene; plus invalid ones such as (1, 2, 3) → not a triangle (a + b = c) and (0, 4, 5) or (−1, 2, 2) → invalid input.')], weight=3),
        22: dict(notes=['Testing is "complete" when exit criteria are met (coverage, remaining risk, time/budget), never when all bugs are gone.']),
        26: dict(notes=['Test driver: code that CALLS the unit under test. Stub: replaces a module the unit calls. Harness: drivers + stubs + tools.'], seen=[see('d10', 4, 'unit testing')]),
        30: dict(notes=['Oracle: decides pass/fail (comparison-based with expected outputs, or checks of properties).']),
        35: dict(notes=['Smoke test: a quick subset of tests to check the build is stable enough for further testing.'],
                 exam=[mcq('A quick check that a new build’s main functions work before deeper testing is a:', ['Smoke test', 'Regression test', 'Stress test', 'Beta test'], 0, '')], weight=3),
    }


DESIGN = {
    5: dict(notes=['Test development: test analysis (what to test: test conditions) → test design (how: test cases) → test implementation (procedures, scripts, schedule).']),
    13: dict(notes=['Knight Capital (2012): dead "zombie" code reactivated during a deployment lost $440M in 45 minutes: missing regression and deployment testing.']),
    19: dict(notes=['Black-box (specification-based) vs. white-box (structure-based) vs. experience-based techniques.']),
    39: dict(notes=['Equivalence partitioning: divide inputs into classes expected to behave the same; one test per class (valid and invalid).'],
             exam=[mcq('A field accepts integers 1–100. The equivalence classes are:', ['< 1, 1–100, > 100', '1 and 100', '0, 50, 101', 'Only 1–100'], 0, '')], weight=3),
    56: dict(notes=['Boundary value analysis: errors cluster at edges: test min, max and just outside/inside them.'],
             exam=[mcq('For a valid range 18–65, two-value BVA tests:', ['17, 18, 65, 66', '18, 40, 65', '0, 18, 65, 100', '19, 64'], 0, '')], weight=3),
    72: dict(notes=['Decision tables: combinations of conditions → actions; each rule (column) is a test case; collapse rules whose outcome doesn’t depend on a condition.'],
             exam=[mcq('Four independent binary conditions give at most how many rules?', ['16', '8', '4', '32'], 0, '')], weight=3),
    82: dict(notes=['State transition testing: states, events, transitions and actions; cover every valid transition and try invalid (null) ones.'],
             exam=[mcq('Testing an ATM that locks the card after 3 wrong PINs is best done with:', ['State transition testing', 'Equivalence partitioning only', 'Statement coverage', 'Error guessing only'], 0, '')], weight=3),
    89: dict(notes=['Use-case testing: one test per main and alternative flow; good for acceptance and system tests.']),
    97: dict(notes=['Non-functional: performance (response time), load (expected volume), stress (beyond the limits), security, usability, recovery, compatibility.'],
             exam=[mcq('Pushing a system beyond its normal capacity to see how it fails is:', ['Stress testing', 'Load testing', 'Usability testing', 'Smoke testing'], 0, '')], weight=3),
    111: dict(notes=['Error guessing: use experience to anticipate likely mistakes (empty inputs, zero, nulls).']),
    112: dict(notes=['Exploratory testing: simultaneous learning, test design and execution, often time-boxed.']),
}


class test_design:
    AUTO_SLIDES = True
    DECK = deck('d06', 'Test Design Techniques', 'Test Design Techniques',
                'The test development process, the Knight Capital case study, specification-based (black-box) '
                'techniques: equivalence partitioning, boundary value analysis, decision tables, state transition and '
                'use-case testing, non-functional testing, and experience-based techniques (error guessing, '
                'exploratory testing).')
    ANN = DESIGN


class black_box:
    AUTO_SLIDES = True
    DECK = deck('d07', 'Black-Box Testing Techniques', 'Black Box Testing Techniques',
                'The black-box version of the test-design lecture: equivalence partitioning, boundary value analysis, '
                'decision tables, state transition and use-case testing, non-functional testing, error guessing and '
                'exploratory testing.')
    ANN = DESIGN


class white_box:
    AUTO_SLIDES = True
    DECK = deck('d08', 'White-Box Testing', 'White Box Testing',
                'Static white-box testing (desk checking, walkthroughs, formal inspections and their roles) and dynamic '
                'white-box testing: statement, path, branch/decision, condition and decision/condition coverage, basis '
                'path testing with flow graphs and cyclomatic complexity.')
    ANN = {
        6: dict(notes=['White-box (structural) testing needs access to the code; tests are derived from its structure.']),
        9: dict(notes=['Static testing: examine code without running it (reviews, walkthroughs, inspections, static analysis).']),
        14: dict(notes=['Formal inspection: author, moderator, reader, recorder/scribe, inspectors; preparation, meeting, rework, follow-up.'],
                 exam=[mcq('In a formal inspection, who leads the meeting and keeps it on track?', ['Moderator', 'Author', 'Scribe', 'Reader'], 0, '')], weight=3),
        26: dict(notes=['Coverage criteria from weak to strong: statement → branch/decision → condition → decision/condition → multiple-condition → path.']),
        28: dict(notes=['Statement coverage: every statement executed at least once. Weak: can miss the false branch of an if.'],
                 tips=[trap('100% statement coverage does NOT imply 100% branch coverage; 100% branch coverage DOES imply 100% statement coverage.')],
                 exam=[tf('100% decision (branch) coverage guarantees 100% statement coverage.', True, ''),
                       tf('100% statement coverage guarantees 100% decision coverage.', False, 'An if without else can be fully covered by one true case.')], weight=3),
        42: dict(notes=['Cyclomatic complexity V(G) = E − N + 2 = decision nodes + 1 = number of independent paths (minimum tests for basis path coverage).'],
                 exam=[mcq('A flow graph has 11 edges and 9 nodes. V(G) =', ['4', '2', '20', '3'], 0, '11 − 9 + 2.')], weight=3),
        53: dict(notes=['Decision (branch) coverage: every decision takes both true and false outcomes.']),
        61: dict(notes=['Condition coverage: every individual condition in a decision takes both true and false. Doesn’t guarantee decision coverage.']),
        65: dict(notes=['Decision/condition coverage: both every condition AND every decision take both outcomes.'],
                 exam=[mcq('For "if (A && B)", tests (A=T, B=F) and (A=F, B=T) achieve:', ['Condition coverage but not decision coverage', 'Decision coverage only', 'Both', 'Neither'], 0, 'Both make the decision false.')], weight=3),
    }


class code_coverage:
    AUTO_SLIDES = True
    DECK = deck('d09', 'Code Coverage', 'Code Coverage',
                'What code coverage measures, its benefits and its false sense of security, best practices, and Google’s '
                'code-coverage best practices (60/75/90% guidelines, coverage of changed code, gating deployments).')
    ANN = images(27, {
        3: dict(notes=['Code coverage: the percentage of code (statements, branches, functions, lines) executed by the test suite.']),
        4: dict(notes=['Coverage finds UNTESTED code; it does not prove the tested code is correct: high coverage can give a false sense of security.'],
                exam=[tf('High code coverage guarantees high-quality tests.', False, 'Lines can run without their results being checked.')], weight=3),
        5: dict(notes=['Benefit: pinpoints which files and branches lack tests, guiding where to write more.']),
        8: dict(notes=['Coverage ≠ quality-tested code; a coverage target must not replace code review.']),
        9: dict(notes=['Write tests from the specification first, then use coverage to see what you missed.']),
        19: dict(notes=['Google guideline: 60% acceptable, 75% commendable, 90% exemplary (no single "ideal" number).'],
                 exam=[mcq('Google’s guideline calls 75% code coverage:', ['Commendable', 'Acceptable', 'Exemplary', 'Insufficient'], 0, '')], weight=3),
        23: dict(notes=['Make sure frequently changing code is covered (per-commit coverage goals).']),
        25: dict(notes=['Gate deployments on coverage carefully: thresholds can become a checkbox that encourages bad tests.']),
    })


class unit_testing:
    AUTO_SLIDES = True
    DECK = deck('d10', 'Unit Testing and JUnit', 'Unit Testing and JUnit',
                'What unit testing is and why, JUnit 5 test classes and methods, verdicts, assertion methods '
                '(assertEquals, assertTrue, assertNull, assertSame, assertArrayEquals, assertThrows), floating-point '
                'deltas, expected exceptions, and best practices with @BeforeEach, @AfterEach, @BeforeAll, @AfterAll '
                'and repeated tests.')
    ANN = {
        4: dict(notes=['Unit testing: test one unit (method/class) in isolation, written by developers, run automatically and often.']),
        8: dict(notes=['JUnit: a framework for writing repeatable automated Java tests; a test method is annotated @Test and returns void.']),
        20: dict(notes=['Verdicts: pass, fail (assertion failed), error (unexpected exception).']),
        22: dict(notes=['Assertions: Boolean checks that make the test fail if they are false.']),
        41: dict(notes=['assertEquals(expected, actual), assertTrue, assertFalse, assertNull, assertNotNull, assertSame (same reference), assertArrayEquals.'],
                 tips=[trap('assertEquals uses equals(); assertSame checks the two references are the SAME object.')],
                 exam=[mcq('Which assertion checks that two references point to the same object?', ['assertSame', 'assertEquals', 'assertTrue', 'assertArrayEquals'], 0, '')], weight=3),
        49: dict(notes=['Floating point: assertEquals(expected, actual, delta), e.g. assertEquals(0.3, 0.1 + 0.2, 0.0001).']),
        51: dict(notes=['Expected exceptions: assertThrows(IllegalArgumentException.class, () -> obj.method(-1));'],
                 exam=[mcq('JUnit 5 checks that code throws an exception with:', ['assertThrows', '@Test(expected=…) only', 'assertFalse', 'assertNull'], 0, '')], weight=3),
        56: dict(notes=['Each test must be independent of the others (no shared mutable state, any order).']),
        58: dict(notes=['@BeforeEach / @AfterEach run before/after EVERY test; @BeforeAll / @AfterAll run once per class and must be static.'],
                 exam=[mcq('Setup code that must run once before all tests in the class uses:', ['@BeforeAll (static)', '@BeforeEach', '@Test', '@AfterEach'], 0, '')], weight=3),
        68: dict(notes=['@RepeatedTest(n) runs a test n times.']),
    }


class regression:
    AUTO_SLIDES = True
    DECK = deck('d11', 'Regression Testing', 'Regression Testing',
                'Software evolution and why changes break things, what regression testing is, reasons for it, its '
                'problems (test-suite maintenance, obsolete and redundant tests, cost), and selecting and prioritizing '
                'regression tests (code-based, specification-based, prioritized rotating selection).')
    ANN = images(17, {
        3: dict(notes=['Changes (fixes, new features, refactoring, new environments) can break unchanged parts, uncover old bugs or reintroduce fixed ones.']),
        4: dict(notes=['Regression test: re-test a previously tested program after modification to make sure no new defects were introduced in unchanged areas.'],
                exam=[mcq('Regression testing is performed:', ['Whenever the software or its environment changes', 'Only once before release', 'Only at the unit level', 'Only by customers'], 0, '')], weight=3),
        6: dict(notes=['Keep a test suite, run it after every change, compare with previous results, add new tests as needed.']),
        10: dict(notes=['Problems: maintaining the test suite, and the cost of re-testing (proportional to product size, not change size).']),
        12: dict(notes=['Obsolete test: no longer valid for the changed system. Redundant test: doesn’t differ significantly from others.']),
        13: dict(notes=['Selection: run only the tests relevant to the change. Prioritization: run the most important ones first when time is short.']),
        14: dict(notes=['Code-based selection: only tests that execute changed or new code.'],
                 exam=[mcq('Selecting only the tests that execute modified code is:', ['Code-based regression test selection', 'Specification-based selection', 'Exhaustive testing', 'Smoke testing'], 0, '')], weight=3),
        16: dict(notes=['Prioritized rotating selection: run all tests eventually, some sooner (round robin, track record of finding faults, structural coverage).']),
    })


class metrics_tools:
    AUTO_SLIDES = True
    DECK = deck('d12', 'Testing Metrics and Tools', 'Testing Metrics and Tools',
                'Why measure testing, base vs. calculated metrics (test-case productivity, execution and pass rates, '
                'defect density, defect leakage, defect removal efficiency, coverage), test tool classes (management, '
                'static, design, execution, performance, monitoring), benefits and risks of tools, and interview '
                'questions on QA vs. QC and verification vs. validation.')
    ANN = {
        3: dict(notes=['"You cannot improve what you cannot measure": metrics show progress, quality and where to act.']),
        12: dict(notes=['Base metrics: raw counts (test cases written, executed, passed, failed, blocked; defects found). Calculated metrics are derived from them.']),
        14: dict(notes=['Examples: % test cases executed = executed / total × 100; pass rate = passed / executed × 100; defect density = defects / size (KLOC).'],
                 exam=[mcq('200 test cases, 160 executed, 120 passed. The pass rate of executed tests is:', ['75%', '60%', '80%', '120%'], 0, '120 / 160.')], weight=3),
        31: dict(notes=['Defect removal efficiency (DRE) = defects found before release / (before + after release) × 100.'],
                 exam=[mcq('90 defects found in testing, 10 found by customers after release. DRE =', ['90%', '10%', '100%', '81%'], 0, '90 / 100.')], weight=3),
        36: dict(notes=['Tools support test management, static testing, test design, execution and logging, performance and monitoring.']),
        43: dict(notes=['Static analysis tools (SpotBugs, checkstyle, JDepend) find defects in code without running it.']),
        57: dict(notes=['Test execution tools run scripted tests; harnesses and unit frameworks provide drivers and stubs.']),
        74: dict(notes=['Benefits: less repetitive work, consistency, objective assessment. Risks: unrealistic expectations, underestimated effort, over-reliance on the tool.']),
        85: dict(notes=['Stop testing when exit criteria are met: coverage, defect rates, deadlines, budget, acceptable residual risk.']),
    }


class advanced:
    AUTO_SLIDES = True
    DECK = deck('d13', 'Advanced Topics: Web and Mobile Testing', 'Advanced Topics',
                'Websites vs. web applications, web testing (functionality: links, forms, cookies, HTML/CSS, databases; '
                'usability, interface, compatibility, security, performance), automation with Selenium, and mobile '
                'testing: native, web and hybrid apps, and the challenges and types of mobile testing.')
    ANN = {
        4: dict(notes=['Website: mostly static informational pages. Web application: interactive client–server program run in a browser.']),
        11: dict(notes=['Web testing: functionality, usability, interface, compatibility, security, performance.']),
        13: dict(notes=['Functionality: check all links (broken, internal, external, mailto), forms, cookies, HTML/CSS validity, database integrity.']),
        24: dict(notes=['Compatibility: browsers, operating systems, devices, screen sizes.']),
        26: dict(notes=['Security: unauthorized access, session expiry, SQL injection, XSS, HTTPS.']),
        28: dict(notes=['Performance: load and stress testing of the site.']),
        32: dict(notes=['Selenium: open-source tool to automate browser testing.'],
                 exam=[mcq('Which tool automates web browser testing?', ['Selenium', 'JUnit only', 'SpotBugs', 'JDepend'], 0, '')], weight=3),
        39: dict(notes=['Native apps (built for one platform), mobile web apps (run in the browser), hybrid apps (web code inside a native wrapper).'],
                 exam=[mcq('An app built with web technologies inside a native container is:', ['Hybrid', 'Native', 'Mobile web', 'Desktop'], 0, '')], weight=3),
        47: dict(notes=['Mobile challenges: many devices and OS versions, screen sizes, networks, battery, interruptions (calls, notifications).']),
        70: dict(notes=['Also test installation, interruptions, crash recovery and battery/network conditions.']),
    }


DECKS_HERE = [introduction, sdlc, software_quality, quality, test_cases, test_design, black_box, white_box, code_coverage,
              unit_testing, regression, metrics_tools, advanced]

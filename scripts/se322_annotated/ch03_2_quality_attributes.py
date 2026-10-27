"""SE322 annotated slides — Chapter 3, Lecture 2: the major quality attributes with scenarios and tactics.
See ch01_introduction.py for AUTO_SLIDES and the ANN keys."""
from .common import mcq, past, scen, see, short, tf, tip, trap, trick

AUTO_SLIDES = 'all'
OVERVIEW = 'This chapter turns quality goals such as availability, performance, security, modifiability, testability, and usability into concrete scenarios and architectural tactics. The aim is to make quality requirements measurable so they can guide and validate architecture decisions.'

DECK = {
    'key': 'ch3.2',
    'slug': '06-quality-attributes-lecture-2',
    'file': 'quality-attributes-lecture-2',
    'title': 'Quality Attributes: Availability, Modifiability, Performance, Security, Testability, Usability',
    'chapter': 'Chapter 3 · Lecture 2',
    'page': 'ch03_2_page',  # notes, highlights and exam questions in the page schema
    'pdf': '/academics/software-engineering/se322/slides/chapter-3-quality-attributes-lecture-2-extra/',
    'lede': ('The six major quality attributes, each with its definition, a general and a concrete scenario, and '
             'its tactics. Final 252 asked for three definitions and an availability scenario; Midterm 261 '
             'tested which quality the heartbeat tactic belongs to.'),
}

TACTICS = ('Tactics by quality: AVAILABILITY detect (ping/echo, heartbeat, exceptions), recover (voting, redundancy, spare, shadow, checkpoint/rollback), prevent (removal from service, transactions, process monitor) · '
           'MODIFIABILITY localize changes, prevent ripple effects, defer binding · PERFORMANCE resource demand, management, arbitration · '
           'SECURITY resist, detect, recover from attacks · TESTABILITY manage input/output, internal monitoring · USABILITY separate the UI, support user initiative (cancel, undo), support system initiative.')

ANN = {
    1: dict(kind='title', title='Quality Attributes', body=[], sub='SE322 · Chapter 3, Lecture 2', tips=[tip(TACTICS)]),
    2: dict(notes=['Short definitions of the qualities (usability, modifiability, performance, security, availability, testability).']),
    3: dict(hl=['Availability:', 'Modifiability:', 'Performance:', 'Security:', 'Testability:', 'Usability:'],
            notes=['Availability asks how often a service works and how quickly it recovers; modifiability asks how much effort a change takes; performance asks how quickly or how much work it handles. Keep their measures distinct.'],
            past=[past('f252', 'Q3 · list and define three quality attributes')],
            exam=[short('List and define three major quality attributes. (Final 252)', 'Availability: concerned with system failures and their duration. Performance: about timeliness, how fast the system responds to events. Security: the ability to resist unauthorised access while still serving legitimate users. (Also: modifiability = cost of change; testability = ease of exposing faults; usability = ease of accomplishing tasks.)'),
                  mcq('Which quality attribute is about the cost of change in time and money?', ['Modifiability', 'Performance', 'Availability', 'Usability'], 0, '')],
            weight=3),
    4: dict(title='Availability: general scenario', notes=['General availability scenario: the possible sources, stimuli, artifacts, environments, responses and measures.'],
            past=[past('f252', 'Q3 · construct a general availability scenario')],
            exam=[short('Construct one quality attribute general scenario for availability. (Final 252)',
                        'Source: internal or external to the system. Stimulus: a fault: omission, crash, timing or wrong response. Artifact: processors, communication channels, storage, processes. Environment: normal or degraded operation. Response: detect the event, record it, notify parties, disable the cause, continue in degraded mode or recover. Response measure: time interval the system must be available, availability percentage, repair time.')],
            weight=3),
    5: dict(notes=['Concrete example: an unresponsive server → switch to a backup. Response measure = downtime allowed / availability percentage.']),
    6: dict(notes=['Availability tactics follow the failure timeline: detect a fault, keep service running or repair it, then restore normal operation. A heartbeat detects a missing process; redundancy provides a replacement; resynchronization catches the recovered copy up.'],
            tips=[trap('Heartbeat is a fault-DETECTION tactic for AVAILABILITY, not performance.')],
            past=[past('m261', 'T/F · heartbeat is a performance tactic (false)')],
            exam=[tf('Heartbeat is a performance tactic used to reduce response time.', False, 'Midterm 261. It detects faults: an availability tactic.'),
                  mcq('Ping/echo, heartbeat and exceptions are tactics for:', ['Fault detection (availability)', 'Resource arbitration (performance)', 'Resisting attacks (security)', 'Localizing changes (modifiability)'], 0, '')],
            weight=3),
    7: dict(notes=['Modifiability scenario: an end user asks for a new feature at runtime; developers change interfaces/configuration and redeploy; measured in effort/time.']),
    8: dict(notes=['The modifiability examples vary who requests a change: an end user, a developer, or an administrator. The source matters because each may have different authority, urgency, and access to the system.']),
    9: dict(notes=['The general modifiability scenario identifies a source of change, the requested modification, the affected artifact, the environment, and the cost or time of making the change. Use it to compare designs against a measurable change goal.']),
    10: dict(notes=['Modifiability improves when a likely change is contained behind one module or interface. If a new tax rule changes only pricing policy, the rest of checkout should not need edits—that is change localization.'],
             exam=[mcq('Keeping interfaces stable so a change in one module doesn’t spread is a ___ tactic.', ['Modifiability (prevent ripple effect)', 'Availability', 'Performance', 'Usability'], 0, '')], weight=2),
    11: dict(notes=['Performance must be considered under several operating environments: normal load, overload, reduced capacity, and emergencies. A design that meets a response target only under ideal conditions may fail in its real operating context.']),
    12: dict(notes=['General performance scenario: events arrive (periodic, sporadic, stochastic); response measured in latency, throughput, jitter, miss rate.']),
    13: dict(notes=['Performance tactics ask whether we can reduce work, schedule or parallelize it, and allocate limited resources fairly. Caching reduces repeated work; concurrency increases throughput; priorities protect time-sensitive requests.'],
             exam=[mcq('Choosing which waiting task gets the CPU first is the performance tactic:', ['Resource arbitration', 'Resource demand', 'Heartbeat', 'Semantic coherence'], 0, '')], weight=2),
    14: dict(notes=['The general security scenario describes a threat source and attack, the protected system asset, the operating context, the response, and a measurable security outcome. It helps turn “make it secure” into something that can be reasoned about and tested.']),
    15: dict(notes=['Concrete security scenario: a dissatisfied employee tries to change pay rates remotely; the system keeps an audit trail and restores data within a day.']),
    16: dict(notes=['Security is layered: resist attacks, detect suspicious activity, and recover with evidence afterward. Authentication identifies a user; authorization limits actions; audit logs help explain an incident.'],
             exam=[mcq('Authenticating users and limiting access are tactics for:', ['Resisting attacks', 'Detecting attacks', 'Recovering from attacks', 'Resource demand'], 0, '')], weight=2),
    17: dict(notes=['A testability scenario asks how easily a tester can set up a test, control inputs, observe behavior, and identify faults. Architecture can improve testability by isolating components and making dependencies replaceable.']),
    18: dict(notes=['A unit tester checks a completed code unit in isolation. The example highlights the value of clear component boundaries and controllable dependencies, which make a unit easier to exercise and diagnose.']),
    19: dict(notes=['A system is testable when tests can control inputs, observe outputs, and inspect state without fragile workarounds. Recording inputs makes failures repeatable and speeds diagnosis.']),
    20: dict(notes=['The general usability scenario describes a user, task or stimulus, interface, context, system response, and a measurable usability result. It gives teams a concrete target such as task completion time or error rate.']),
    21: dict(notes=['The new-user example measures how quickly someone can download and become productive with an application. It turns usability into an observable outcome rather than an unsupported claim that an interface is “easy.”']),
    22: dict(notes=['Usability tactics: separate the UI; support USER initiative (cancel, undo, aggregate); support SYSTEM initiative (user/task/system models).'],
             exam=[mcq('An “Undo” button supports which usability tactic?', ['Support user initiative', 'Support system initiative', 'Separate the user interface', 'Resource arbitration'], 0, '')], weight=2),
    23: dict(notes=['The next lecture turns from quality attributes to architecture patterns: reusable structural solutions that help organize components and their interactions.']),
    24: dict(notes=['For each quality attribute, connect a tactic to the mechanism it provides. For example, redundancy supports availability, caching can improve performance, and authentication or encryption can support security; the tactic must fit the scenario.'], tips=[tip(TACTICS)],
             exam=[short('Give one tactic for security, availability, performance and usability.', 'Security: authenticate users (resisting attacks). Availability: heartbeat or active redundancy. Performance: caching/increase resources or scheduling (arbitration). Usability: undo/cancel (support user initiative).')],
             weight=2),
}

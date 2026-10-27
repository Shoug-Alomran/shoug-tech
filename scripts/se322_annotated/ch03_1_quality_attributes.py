"""SE322 annotated slides — Chapter 3, Lecture 1: quality attributes, scenarios, tactics and design decisions.
See ch01_introduction.py for AUTO_SLIDES and the ANN keys."""
from .common import mcq, past, scen, see, short, tf, tip, trap, trick

AUTO_SLIDES = 'all'
OVERVIEW = 'This chapter turns quality goals such as availability, performance, security, modifiability, testability, and usability into concrete scenarios and architectural tactics. The aim is to make quality requirements measurable so they can guide and validate architecture decisions.'

DECK = {
    'key': 'ch3.1',
    'slug': '05-quality-attributes-lecture-1',
    'file': 'quality-attributes-lecture-1',
    'title': 'Quality Attributes: Scenarios, Tactics and Design Decisions',
    'chapter': 'Chapter 3 · Lecture 1',
    'page': 'ch03_1_page',  # notes, highlights and exam questions in the page schema
    'pdf': '/academics/software-engineering/se322/slides/chapter-3-quality-attributes-lecture-1-extra/',
    'lede': ('Functional vs. non-functional requirements, why stakeholders weigh qualities differently, the six-part '
             'quality attribute scenario (source, stimulus, artifact, environment, response, response measure), '
             'tactics, and the categories of quality design decisions. Writing a scenario is asked on every paper: '
             'Quiz 1, Midterm 252 Q5D, Midterm 261 and Final 252.'),
}

SCENARIO = ('Scenario in one line: SOURCE generates a STIMULUS that hits an ARTIFACT in some ENVIRONMENT; the system '
            'gives a RESPONSE, judged by a RESPONSE MEASURE. Mnemonic: “Some Students Always Eat Rice Rapidly.”')

ANN = {
    1: dict(kind='title', title='Quality Attributes', body=[], sub='SE322 · Chapter 3, Lecture 1', tips=[tip(SCENARIO)]),
    2: dict(notes=['Requirements vs. qualities → scenarios → tactics → design decisions. Lecture 2 covers the six major qualities.']),
    3: dict(notes=['A functional requirement says what service exists; a quality requirement shapes how well it works. “Search for a course” is a function, while “show results within one second” constrains that function.'],
            past=[past('q261', 'T/F · architecture ignores non-functional requirements (false)', related=True)],
            exam=[tf('Software architecture is concerned only with functional structure and need not consider non-functional requirements.', False, 'Quiz 1 261. Quality attributes are architecture’s main concern.')],
            weight=3),
    4: dict(notes=['Quality must be considered through design, implementation AND deployment. Architecture gives the foundation but can’t guarantee quality alone.']),
    5: dict(notes=['Different stakeholders rank qualities differently: developers → maintainability, QA → testability, end users → usability and performance.']),
    6: dict(notes=['Quality attributes constrain HOW the system delivers its functions (e.g., how fast the Options dialog appears).']),
    7: dict(notes=['One event can affect several qualities: a denial-of-service attack is a security threat, slows performance, and can make service unavailable. Scenarios give each concern a concrete event and measurable outcome so trade-offs can be discussed.']),
    8: dict(notes=['Read a quality scenario as a test story: who triggers what, which part is affected, under what conditions, what should happen, and how success is measured. This turns “available” into something the design can be evaluated against.'], tips=[tip(SCENARIO)],
            past=[past('q261', 'match each scenario element to its meaning')],
            exam=[mcq('In a quality attribute scenario, the event that arrives at the system is the:', ['Stimulus', 'Source', 'Artifact', 'Response measure'], 0, 'Quiz 1 261.'),
                  mcq('The condition the system is in when the stimulus arrives (normal, overloaded) is the:', ['Environment', 'Artifact', 'Response', 'Source'], 0, ''),
                  mcq('“Within 2 seconds, 99% of the time” is an example of the:', ['Response measure', 'Response', 'Stimulus', 'Environment'], 0, '')],
            weight=3),
    9: dict(notes=['Template: some SOURCE generates a STIMULUS that arrives at an ARTIFACT under an ENVIRONMENT; the system RESPONDS, measured by a RESPONSE MEASURE.'],
            past=[past('q261', 'match scenario parts to an example'), past('m252', 'Q5D · availability scenario for the airline system'), past('m261', 'Q · scenario for an online voting system'),
                  past('f252', 'Q3 · general availability scenario', related=True)],
            exam=[scen('Write an availability scenario for an online airline itinerary service. (Midterm 252, Q5D)',
                       'Source: hardware/internal fault. Stimulus: the Trip Planning Service crashes. Artifact: the planning service process. Environment: normal operation. Response: detect the failure, fail over to a standby instance and keep accepting requests (log and notify). Response measure: downtime under 30 seconds; 99.9% availability.')],
            weight=3),
    10: dict(notes=['Performance scenario example (figure): users → requests → system → processed with an average latency target.']),
    11: dict(notes=['A general quality-attribute scenario lists the possible values for each scenario part. It is a reusable template for a quality, while a concrete scenario fills in a specific source, stimulus, environment, response, and measurable result.']),
    12: dict(notes=['General availability scenario: source internal/external; stimulus omission, crash, timing, response; artifact processors, channels, storage; environment normal/degraded; response detect, record, notify, recover; measure time available, repair time.'],
             seen=[see('ch3.2', 4, 'Availability in detail')], weight=2),
    13: dict(notes=['A tactic is a design technique with a predictable effect on a quality. Redundancy can improve availability because a backup takes over after failure; that is more actionable than saying “make it reliable.”'],
             seen=[see('ch2.1', 22, 'Tactics first introduced')],
             exam=[tf('Tactics are design decisions that influence the response of a quality attribute.', True, '')], weight=2),
    14: dict(notes=['Examples: redundancy (availability: failover), caching (performance), load balancing, encryption (security).'],
             exam=[mcq('Keeping multiple instances so another takes over when one fails is a tactic for:', ['Availability', 'Usability', 'Testability', 'Modifiability'], 0, '')], weight=2),
    15: dict(notes=['Categories of quality design decisions: allocation of responsibilities, coordination model, data model, management of resources, mapping among architectural elements, binding time decisions (and choice of technology).'],
             exam=[mcq('Deciding how and when architectural elements are bound together is a:', ['Binding time decision', 'Coordination model decision', 'Data model decision', 'Resource management decision'], 0, '')], weight=2),
    16: dict(notes=['Allocation: which part handles which task. Coordination: how parts communicate. Data model: data abstractions and operations.']),
    17: dict(notes=['Resource management assigns memory, CPU, and bandwidth to runtime work. Mapping links code modules to runtime elements; coordination specifies how runtime elements interact. These architecture decisions affect whether the system can meet quality targets.']),
    18: dict(notes=['The next lecture studies six major quality attributes individually. For each one, learn the definition, a concrete scenario, and tactics that help an architecture achieve it.']),
}

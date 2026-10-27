"""SE322 annotated slides — Chapter 4, Lecture 2: blackboard, pipes and filters, client-server and broker.
See ch01_introduction.py for AUTO_SLIDES and the ANN keys."""
from .common import mcq, past, scen, see, short, tf, tip, trap, trick

AUTO_SLIDES = 'all'
OVERVIEW = 'This chapter studies reusable architecture patterns and their trade-offs, including data-centered systems, pipes and filters, distributed systems, MVC, and layered architectures. For each pattern, focus on the problem it solves and how its structure affects system qualities.'

DECK = {
    'key': 'ch4.2',
    'slug': '08-architecture-patterns-lecture-2',
    'file': 'architecture-patterns-lecture-2',
    'title': 'Architecture Patterns: Blackboard, Pipes and Filters, Client-Server, Broker',
    'chapter': 'Chapter 4 · Lecture 2',
    'page': 'ch04_2_page',  # notes, highlights and exam questions in the page schema
    'pdf': '/academics/software-engineering/se322/slides/chapter-4-architecture-patterns-lecture-2-extra/',
    'lede': ('Four patterns with their components, component and sequence diagrams, and quality properties. '
             'Midterm 252 Q5 was a blackboard system (airline itinerary) and Q6 the face-recognition pipe and '
             'filter from this deck; Final 252 asked for a pipe-and-filter component diagram (StreamFlow).'),
}

ROLES = ('Roles to name in an exam: BLACKBOARD = blackboard (shared data), knowledge sources (independent workers), controller. '
         'PIPES AND FILTERS = data source, filters, pipes, data sink. BROKER = client, client-side proxy, broker, server-side proxy, server.')

ANN = {
    1: dict(kind='title', title='Architecture Patterns', body=[], sub='SE322 · Chapter 4, Lecture 2', tips=[tip(ROLES)]),
    2: dict(notes=['This lecture covers data-centered, data-flow, and distributed styles, with examples such as blackboard, pipes and filters, client-server, and broker. Compare how each style organizes components and communication.']),
    3: dict(notes=['A data-centered system uses a shared central store that independent components access. This can simplify data sharing, but the repository becomes a key availability and consistency concern.']),
    4: dict(notes=['In a repository, components choose when to read and write the shared store. In a blackboard, the evolving shared state helps determine which specialist should act next; this suits problems with no fixed processing order.']),
    5: dict(notes=['Data integrity means stored information remains complete, accurate, and consistent. Repository updates may need validation, synchronization, or transaction policies to prevent conflicting clients from corrupting shared state.']),
    6: dict(notes=['A blackboard suits problems where independent specialists can each improve a partial solution. They read shared state, contribute what they know, and stop when a completion rule says the problem is solved.'],
            past=[past('m252', 'Q5 · airline itinerary system = blackboard'), past('m261', 'match scenario to style', related=True)],
            exam=[mcq('Independent components repeatedly read and improve a shared draft until it is final. Which pattern?', ['Blackboard', 'Pipes and filters', 'Broker', 'Layered'], 0, 'Midterm 252, Q5A.')],
            weight=3),
    7: dict(notes=['Analogy: scientists at a blackboard; a mediator (controller) decides who writes next; each advances the solution a little.']),
    8: dict(notes=['The blackboard analogy is collaborative problem solving: specialists contribute partial knowledge to a shared space, and a controller coordinates progress toward a solution.']),
    9: dict(notes=['ER example: patient chart = blackboard; doctors, nurses, lab = knowledge sources; head nurse = controller.']),
    10: dict(notes=['Components: **blackboard** (shared data), **knowledge sources** (independent specialists), **controller** (monitors and schedules).'],
             tips=[tip(ROLES)],
             past=[past('m252', 'Q5B · identify each component’s role')],
             exam=[scen('In the airline system (Midterm 252, Q5B), give the blackboard role of each component: Passenger App, Trip Planning Service, Route Builder, Constraint Checker, Best Option Selector, Draft Itinerary Record.',
                        'Passenger App: client. Trip Planning Service: controller. Route Builder, Constraint Checker and Best Option Selector: knowledge sources (workers). Draft Itinerary Record: the blackboard (shared data).')],
             weight=3),
    11: dict(notes=['On the component diagram, trace the three roles: the controller coordinates work, knowledge sources provide specialist behavior, and the blackboard stores the evolving shared result. Provided/required interfaces show how each part can be replaced or tested.']),
    12: dict(notes=['Adding a specialist can extend the system without rewriting others, but opportunistic control makes behavior harder to reproduce. Tests need representative blackboard states and clear rules for when the controller chooses each specialist.']),
    13: dict(notes=['Evaluate the pattern’s qualities and trade-offs: central data sharing can support integration and extensibility, but performance, consistency, and repository failure can affect the whole system.']),
    14: dict(notes=['Follow one controller cycle: choose a knowledge source, let it read the current board, then write a partial result back. The new state may enable a different specialist, so the order is driven by progress rather than a hard-coded pipeline.'],
             past=[past('m252', 'Q5C · build the component diagram')]),
    15: dict(notes=['Use the sequence diagram to follow time: controller selection comes before a knowledge source reads or updates the board. The important point is that each source contributes only when the shared state makes its knowledge useful.']),
    16: dict(notes=['Continue the sequence by checking which component initiates each action and how the shared blackboard makes intermediate results visible to other knowledge sources.']), 17: dict(notes=['Read each interaction from top to bottom: the controller selects a knowledge source, that specialist reads the current blackboard state, performs its part of the analysis, then writes its result back. The controller can select another specialist using the updated state; no specialist needs to call every other specialist directly.']),
    18: dict(notes=['The deployment view shows where the blackboard components run. Physical placement can affect response time, availability, and the communication cost of accessing shared data.']),
    19: dict(notes=['A component diagram shows software parts and their interfaces; a deployment diagram shows where those parts run. Keeping these questions separate lets hardware placement change without changing the logical design.'],
             exam=[mcq('Which diagram shows physical nodes and the software deployed on them?', ['Deployment diagram', 'Component diagram', 'Class diagram', 'Sequence diagram'], 0, '')], weight=2),
    20: dict(notes=['For speech recognition, the blackboard can hold candidate sounds, words, and sentence interpretations. Independent recognizers contribute evidence until one interpretation is strong enough; this allows context to refine earlier guesses.']),
    21: dict(notes=['Each knowledge source contributes a different level of evidence, such as phoneme candidates, word hypotheses, or grammar constraints. The controller coordinates updates until a coherent interpretation is reached.']),
    22: dict(notes=['The component solution separates the blackboard, controller, and knowledge sources. Even without interface notation, identify each component’s responsibility and the shared data through which they collaborate.']),
    23: dict(notes=['The sequence diagram should show repeated read–reason–write cycles, not one specialist doing the whole job. Each contribution changes the board and may affect which specialist the controller schedules next.']),
    24: dict(notes=['Batch-sequential processing waits for a complete output before the next stage begins; pipes-and-filters can stream data as it arrives. Streaming reduces waiting, but stages must agree on formats and partial-data behavior.']),
    25: dict(notes=['Batch sequential processing waits for one stage to finish a complete batch; pipes and filters can stream output incrementally. Streaming can reduce latency, but it requires compatible data formats and error handling between filters.']),
    26: dict(notes=['Each filter transforms data without knowing the entire application; pipes carry results between filters. A stage is reusable when its input and output contracts match its neighbors.'],
             past=[past('m252', 'Q6 · pipe-and-filter sequence diagram'), past('f252', 'Q4 · StreamFlow pipe-and-filter'), past('m261', 'Q6 · match scenarios to architectural styles', related=True)],
             weight=3),
    27: dict(hl=['Data source', 'Filter', 'Pipes'], notes=['Components: data SOURCE, FILTERS (transform), PIPES (connect), data SINK.'],
             exam=[mcq('In pipes and filters, the component that transforms the data is the:', ['Filter', 'Pipe', 'Sink', 'Source'], 0, '')], weight=3),
    28: dict(notes=['The processing-chain example should be read from source to sink. At each step identify what representation enters a filter, what transformation occurs, and what output is passed onward.']),
    29: dict(notes=['Name each filter’s responsibility and the data passed between filters. Clear boundaries make stages easier to replace or test independently.']),
    30: dict(notes=['The diagram assembles the filters and pipes into a complete pipeline. Check that the order matches the required transformation and that each connection carries the expected data.']),
    31: dict(notes=['A video pipeline is easy to reason about stage by stage: detect faces in frames, recognize each face, then infer identity. If the final identity is wrong, inspect each stage’s input and output to locate where evidence was lost.'],
             past=[past('m252', 'Q6 · the same face-recognition system')],
             exam=[mcq('In the face-recognition pipeline, which filter comes right after “detects faces”?', ['Recognizes faces', 'Predicts the identity', 'Accesses videos', 'Plays audio'], 0, 'Midterm 252, Q6.')],
             weight=3),
    32: dict(notes=['The component diagram shows the processing stages and their connections. Separate the transformation logic from the transport mechanism so each filter can focus on its task.']),
    33: dict(notes=['Example 2 sequence: each filter passes its output to the next (video+audio → detected faces → recognized faces → identity).']),
    34: dict(notes=['Example 2 sequence diagram.'],
             exam=[short('Order the lifelines of the face-recognition pipe-and-filter sequence diagram. (Midterm 252, Q6)', 'Access videos → detect faces → recognize faces → predict the identity (data flows left to right through the filters).')], weight=3),
    35: dict(notes=['Independent filters can be reused or run concurrently, but every boundary needs a compatible data format. This pattern is less suitable when users must interrupt or steer work in the middle.']),
    36: dict(notes=['Pipes and filters encourage reuse and parallel work, but data-format mismatches and error handling can complicate the pipeline. A filter that needs global context may not fit this style cleanly.']),
    37: dict(notes=['A distributed design crosses machine boundaries. Treat calls as messages that may be slow or fail, and keep the responsibilities that must remain available from depending on one remote node.']),
    38: dict(notes=['Middleware hides network plumbing, but cannot make a remote call behave like a local one. Messages can be delayed and nodes can fail independently, so timeouts, retries, and partial results need explicit handling.']),
    39: dict(notes=['Internet services, web services, and file or music sharing are distributed because participants communicate across machines. Their deployment and network boundaries affect reliability and security.']),
    40: dict(notes=['In client-server, clients request services and servers provide them. This separates requesters from service providers, but server load and availability can become system-wide concerns.'], past=[past('m261', 'Q6 · match scenarios to architectural styles', related=True)]),
    41: dict(notes=['Trace a client-server interaction from request to response and identify the server’s service boundary. The diagram is about roles and communication, not necessarily one client or one physical server.']),
    42: dict(notes=['When clients know the locations and protocols of many servers, each server change spreads to callers. A broker centralizes discovery and routing so clients use one intermediary instead of managing every connection.'],
             exam=[mcq('The main drawback of client-server that the broker pattern fixes is:', ['Clients are tightly coupled to servers', 'It cannot store data', 'It needs a blackboard', 'It has no clients'], 0, '')], weight=3),
    43: dict(notes=['The broker lets clients use services without knowing their network location or communication details. This is helpful when servers move or protocols vary, but the broker becomes an important dependency that itself needs resilience.'],
             weight=3, past=[past('m261', 'Q6 · match scenarios to architectural styles', related=True)]),
    44: dict(notes=['A broker architecture uses a client proxy, broker, server proxy, and server. Proxies hide location and communication details; the broker routes requests to the appropriate service.'], tips=[tip(ROLES)]),
    45: dict(notes=['Walk through a broker call: the client invokes its local proxy, the broker locates or forwards to a server-side proxy, and the server performs the request before a response returns.']),
    46: dict(notes=['The client-side proxy resolves locally or forwards to the broker; the broker isolates communication concerns from application logic.']),
    47: dict(notes=['Qualities: interoperability, modifiability, portability, reusability.'],
             exam=[mcq('Which is a quality property of the broker pattern?', ['Interoperability across platforms', 'Lower security', 'Tight coupling', 'No middleware'], 0, '')], weight=2),
    48: dict(notes=['Compare blackboard/repository, pipes and filters, client-server, and broker by where shared state lives and how components communicate. Each pattern supports different needs and introduces distinct trade-offs.']),
}

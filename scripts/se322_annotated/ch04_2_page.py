"""SE322 Chapter 4, Lecture 2 (Blackboard, Pipes-and-Filters, Client-Server, Broker): page content.

Schema: see annotated_page.py. The PDF's text layer has mis-encoded punctuation (apostrophes and dashes), so
highlight phrases avoid them. Marks with a 4th element 'ocr' are labels inside pictures (skipped if OCR can't
read them). Past-exam questions are copied from the papers in exams/; everything else is a prediction.
"""
from .common import asked, likely

TITLE = 'Data-Centered, Data-Flow and Distributed Patterns: Blackboard, Pipes-and-Filters, Client-Server, Broker'
CHAPTER = 'SE322 · Chapter 4 · Lecture 2'

AIRLINE = ('Best Flight Itinerary system (Midterm 252): a Passenger App sends a trip request to the Trip Planning Service, '
           'which creates an empty itinerary draft in the Draft Itinerary Record. The Route Builder lists possible routes, the '
           'Constraint Checker filters out routes that break the passenger’s or airline’s rules, and the Best Option Selector picks '
           'the best one; each step retrieves the current draft, improves it and saves it back, until the draft is stable and '
           'the service returns it to the app.')

OVERVIEW = {
    'summary': ('Four patterns for three system types. Data-centered systems revolve around shared data: in the blackboard '
                'pattern, independent knowledge sources (agents) improve a shared solution on the blackboard while a '
                'controller decides who works next. Data-flow systems move and transform a stream: pipes-and-filters chains '
                'independent filters with pipes from a data source to a data sink. Distributed systems spread work over the '
                'network: client–server is direct and tightly coupled, and the broker pattern puts a mediator (with client- and '
                'server-side proxies) between them to loosen that coupling.'),
    'ideas': [
        ('Blackboard', 'Blackboard (shared data) + agents/knowledge sources (independent specialists) + controller (schedules them). Opportunistic: no fixed order of steps.'),
        ('Pipes and filters', 'Data source → filter → pipe → filter → … → data sink. Filters are independent, so they can be added, reordered, reused and run in parallel.'),
        ('Client–server', 'Clients request, a central server provides. Interoperable and easy to update centrally, but clients are tightly coupled to the server.'),
        ('Broker', 'Client → client proxy → broker → server proxy → server. Clients need only the broker, so servers can move or change.'),
    ],
    'sections': [
        ('Slides 2–5', 'Data-centered systems: data manager, workers, integrity'),
        ('Slides 6–23', 'Blackboard: analogy, ER example, components, scheduling-system diagrams, speech-recognition exercise'),
        ('Slides 24–36', 'Data flow and pipes-and-filters: compiler and face-recognition examples, qualities'),
        ('Slides 37–42', 'Distributed systems and client–server'),
        ('Slides 43–48', 'Broker pattern and summary'),
    ],
    'exam': ('Every pattern here has been examined. Midterm 252 Q5 (6 marks) was a whole blackboard problem (name the pattern, '
             'give each component’s role, build the component diagram, write an availability scenario) and Q6 (2 marks) a '
             'pipe-and-filter sequence diagram for the face-recognition system on slides 31–35. Final 252 Q4-2 asked for the '
             'pipe-and-filter diagram of a video-processing app, and Midterm 261 Q6 matched scenarios to blackboard, '
             'pipe-and-filter, broker and client-server.'),
}

TITLES = {8: 'Extra: Blackboard as a group project', 9: 'Extra: Real-World Example: Emergency Room (ER)',
          12: 'Blackboard: Students’ Scheduling System component diagram', 13: 'Extra: Blackboard roles and interfaces',
          14: 'Blackboard: scheduling system sequence diagram', 15: 'Extra: Blackboard sequence, phase 1',
          16: 'Extra: Blackboard sequence, phase 2', 17: 'Extra: Blackboard sequence, phases 3–4', 19: 'Extra: Deployment vs. Component Diagram',
          21: 'Extra: Speech-recognition agents at work', 22: 'Extra: Solution – component diagram', 23: 'Extra: Solution – sequence diagram',
          26: 'Pipes-and-Filters Architectural Pattern', 29: 'Pipes-and-Filters – Example 1: language processor',
          30: 'Pipes-and-Filters – Example 1 as UML', 35: 'Pipes-and-Filters – Example 2 sequence diagram', 45: 'Broker Pattern components'}

SLIDES = {
    1: dict(
        hl=[('[Architecture Patterns]', 1)],
        notes=['Second patterns lecture: the patterns for the first three system types of Lecture 1. For each one learn its components (the roles you will be asked to name), how they communicate, and its quality properties.']),
    2: dict(
        hl=[('Data-Centered Systems', 1), ('Data Flow Systems', 2), ('Distributed Systems', 3)],
        notes=['**Data-centered** → the blackboard pattern.',
               '**Data flow** → pipes and filters.',
               '**Distributed** → client–server and broker. Interactive and hierarchical systems come in Lecture 3.']),
    3: dict(
        hl=[('central repository', 1), ('Data management component', 2), ('Worker components', 3)],
        notes=['A **data-centered** system is decomposed around one **central repository** of data.',
               'The **data management component** (the “Data Manager” in the diagram) controls, provides and manages access to the system’s data.',
               '**Worker components** do the actual work, operating on that data.']),
    4: dict(
        hl=[('Communication', 1), ('one bidirectional communication', 1), ('do not interact', 2)],
        notes=['Communication is **one-to-one and two-way** between each worker and the data manager (the “two way communication” arrows).',
               'Workers **do not interact with each other** directly; everything goes through the data management component. That keeps workers independent, but makes the data manager critical: if it is slow or down, everyone is.']),
    5: dict(
        hl=[('Data integrity', 1), ('complete, accurate, and', 1), ('Communication protocols', 2)],
        notes=['Because everything depends on shared data, these systems must handle **data integrity**: data stays complete, accurate and consistent across operations, even when several workers update it (the diagram adds transactions and recovery, and security, at the data manager).',
               'They must also define the **communication protocols** (and security) between the workers and the data manager. The Extra box repeats Lecture 1: a DBMS can be seen as a repository or as the server in client–server.']),
    6: dict(
        hl=[('central data component', 1), ('work independently', 2), ('opportunistic problem-solving', 2), ('no predetermined', 3)],
        notes=['The **blackboard** pattern decomposes a system into components that work around a **central data component** to solve complex problems.',
               'The components work **independently**, each providing a **partial solution**, in an **opportunistic** way: whoever can contribute something useful given the current state does so.',
               'There is **no predetermined sequence** of operations that leads to the answer. That is the key difference from pipes and filters, whose order is fixed.'],
        exam=[asked('m252', 'Q5a · 1 mark', AIRLINE + ' Write the name of the most suitable architectural pattern for this system.',
                    a='**Blackboard.** Several independent components (Route Builder, Constraint Checker, Best Option Selector) repeatedly read and update one shared data store (the Draft Itinerary Record) until the solution is stable, and a controller (the Trip Planning Service) decides which one runs next. Pipe-and-filter is the tempting wrong answer: there, filters pass output directly to the next filter and no shared store is repeatedly updated.')]),
    7: dict(
        hl=[('group of scientists', 1), ('mediator controls access', 2), ('advances its solution', 3), ('no more progress', 3), ('expert systems', 4)],
        notes=['The pattern copies how a **group of scientists** would attack a hard problem together at one blackboard.',
               'A **mediator (controller)** controls access to the board. When it hands control to a scientist, that scientist looks at the current state and, if possible, advances the solution before releasing the board.',
               'With the new knowledge on the board, control goes to the next scientist who can improve it, and so on until **no more progress** can be made. There is no fixed order: each contributes when the current state makes their expertise useful.',
               'This is how **expert systems** work (AI that applies knowledge and inference rules like a human expert, in medicine or finance), so the blackboard pattern is a good fit for their logical architecture.']),
    8: dict(
        hl=[('Blackboard:', 1), ('Agents:', 2), ('Controller:', 3)],
        notes=['**Blackboard**: the shared whiteboard in a group project, where all information is displayed and updated and everyone can see it.',
               '**Agents**: independent contributors with different skills who read the board and add their expertise.',
               '**Controller**: the organiser who manages when and how agents access the board, so the project progresses in an orderly way.']),
    9: dict(
        hl=[('Emergency Room (ER)', 1), ('Blackboard:', 2), ('Agents:', 3), ('Controller:', 4)],
        notes=['An emergency room maps onto the pattern exactly.',
               '**Blackboard**: the patient’s chart, visible to all staff and continuously updated.',
               '**Agents**: doctors, nurses and specialists. A nurse updates vital signs, a doctor orders tests or medication, a specialist adds an opinion. Each reads the chart and contributes from their own expertise.',
               '**Controller**: decides who gets access to the chart and when, prioritising contributions as the patient’s condition changes.']),
    10: dict(
        hl=[('Blackboard:', 1), ('Agents:', 2), ('Controller:', 3), ('Process:', 4)],
        notes=['**Blackboard**: the central data repository where all current information is displayed and accessible.',
               '**Agents** (knowledge sources): Agent 1–4, each with unique expertise for part of the problem. In the cartoon, agents cannot touch the board until the controller grants access.',
               '**Controller**: decides which agent accesses the board at any time, keeping problem solving orderly.',
               '**Process**: Agent 1 currently has access and advances the solution; Agents 2–4 wait their turn.'],
        exam=[asked('m252', 'Q5b · 1 mark', AIRLINE + ' Based on the pattern you selected, identify the role of each component.',
                    a='**Passenger App** → client (sends the trip request, shows the result). **Trip Planning Service** → controller (manages the process and decides which component runs next). **Draft Itinerary Record** → blackboard (the shared data everyone reads and updates). **Route Builder, Constraint Checker, Best Option Selector** → workers / knowledge sources.')]),
    11: dict(
        hl=[('Used in speech recognition', 1), ('Agent 1', 2, 0, 'ocr')],
        notes=['Typical uses: speech recognition, image recognition, security systems, business resource management. All are problems where several kinds of knowledge must be combined with no fixed order.',
               'The structure diagram: the **controller** at the top connects to every agent (to invoke them) and to the **blackboard**; Agents 1…n each connect to the blackboard to read and write. Agents never connect to each other.']),
    12: dict(
        hl=[('Scheduling System', 1), ('A shared knowledge base', 2), ('Specialized problem solvers', 3), ('Coordinates when', 4), ('Why Blackboard Has Provider Interfaces', 5), ('Why Agents Provide Interfaces to Controller', 6)],
        notes=['Example: a students’ scheduling system that builds a schedule from completed courses, the student’s work schedule, and the courses offered.',
               '**Blackboard** (ScheduleBlackboard): the shared knowledge base that controller and agents read and write.',
               '**Agents** (StudentHistory, WorkSchedule, CourseOfferings): specialised problem solvers that contribute when they can.',
               '**Controller** (ScheduleManager): decides when and which agent acts, and the order of problem solving.',
               'Interfaces in the component diagram: the **blackboard provides** an interface (IStudentHistory, IWorkSchedule… read/write/update) because both the controller and the agents need its data. The controller provides nothing to the agents: it orchestrates, it doesn’t store data.',
               'The **agents provide** an interface (e.g. `run()`, `workOnSchedule()`) that the controller requires, so the controller can invoke them when it decides they should act.'],
        exam=[asked('m252', 'Q5c · 3 marks', AIRLINE + ' Build the component diagram with the correct provided and required interfaces.',
                    a='Trip Planning Service **provides** ITripPlanningAPI and the Passenger App **requires** it (the client only talks to the controller). Draft Itinerary Record **provides** IItineraryStore; the Trip Planning Service and each worker (Route Builder, Constraint Checker, Best Option Selector) **require** it. The Trip Planning Service invokes the three workers. Wrong connections: Route Builder passing routes directly to the Constraint Checker (that is pipe-and-filter), the Passenger App using the store directly, the blackboard requiring an interface from the controller, a worker providing the API to the client.')]),
    13: dict(
        hl=[('Who does what', 1), ('Step-by-step flow', 2), ('Why those interfaces in the component diagram', 3), ('General guideline', 4)],
        notes=['**Who does what**: the blackboard is the shared store with a read/write/update API; agents are specialised solvers that use that API when invoked; the controller (scheduler) orchestrates when and which agent runs, and does not pass data around.',
               '**One cycle**: (1) the controller decides “Agent A runs now” and calls `AgentA.run()`; (2) A reads what it needs from the blackboard; (3) A computes and writes its results back; (4) the controller checks the board (or is notified) and picks the next agent.',
               '**Interfaces**: the blackboard provides the data API (agents and controller require it); agents provide a service interface such as `run()` (the controller requires it); the controller generally provides nothing to agents.',
               '**Guideline**: control flows controller → agents (invocation); data flows agents ↔ blackboard (read/write). Agents never talk to each other; they communicate only through the blackboard, and only when scheduled.']),
    14: dict(
        hl=[('Client:', 1), ('ScheduleManager:', 2), ('StudentHistory:', 3), ('ScheduleBlackboard:', 4)],
        notes=['The sequence diagram for the scheduling system. **Client**: the student portal; the student clicks “Generate Schedule”, which calls `generateSchedule()`.',
               '**ScheduleManager** (controller) runs the process and decides which scheduler goes next (`nextScheduler()`).',
               '**StudentHistory**, **CourseOfferings**, **WorkSchedule**: the agents. Each improves the draft: check eligibility from passed courses, keep only sections actually offered, remove conflicts with work hours.',
               '**ScheduleBlackboard** holds the current draft, accessed through `getSchedule()` and `setSchedule()`. Slides 15–17 walk through the 19 messages.']),
    15: dict(
        hl=[('How Your Schedule is Built', 1), ('Phase 1: StudentHistory Agent Works', 2)],
        notes=['Messages 1–2: the client calls `generateSchedule()` on the ScheduleManager, which calls `nextScheduler()` to choose the first agent.',
               '**Phase 1** (messages 3–6): the manager calls `workOnScheduler()` on StudentHistory; StudentHistory reads the draft with `getSchedule()`, adjusts it for past courses and degree requirements, saves it with `setSchedule(sch)`, and returns control to the manager.']),
    16: dict(
        hl=[('Phase 2: CourseOfferings Agent Works', 1)],
        notes=['**Phase 2** (messages 7–11): the manager picks the next agent (`nextScheduler()`) and calls `workOnScheduler()` on CourseOfferings. It reads the draft, keeps only courses actually offered this semester, saves the realistic version back, and returns control. Note the pattern repeating: manager invokes → agent reads → agent writes → control returns.']),
    17: dict(
        hl=[('Phase 3: WorkSchedule Agent Works', 1), ('Phase 4: Schedule is Delivered', 2)],
        notes=['**Phase 3** (messages 12–16): WorkSchedule reads the draft, removes conflicts with the student’s work commitments, and saves the final conflict-free version.',
               '**Phase 4** (messages 17–19): the manager retrieves the finished schedule from the blackboard with one last `getSchedule()` and returns it to the client.']),
    18: dict(
        hl=[('Modifiability', 1), ('Reusability', 2), ('Maintainability', 3)],
        notes=['**Modifiability**: agents are independent, so adding or removing one is easy, e.g. a new SportsSchedule agent without touching the others.',
               '**Reusability**: specialised agents can be reused elsewhere, e.g. StudentHistory in a graduation checker.',
               '**Maintainability**: knowledge is separated, so fixing a bug in CourseOfferings doesn’t touch WorkSchedule. (The cost: the controller’s scheduling makes behaviour harder to predict and test.)'],
        exam=[likely('Give two quality properties of the blackboard pattern with a short justification.',
                     a='Modifiability: agents are independent, so new ones can be added without changing others. Reusability: specialised agents can be reused in other systems. Maintainability: knowledge sources are separated, so one can be fixed without touching the rest.')]),
    19: dict(
        hl=[('Deployment Diagram', 1), ('Component Diagram', 2), ('Hardware, runtime nodes', 1), ('Software components', 2)],
        notes=['A **deployment diagram** shows the physical deployment of artifacts (programs, libraries) onto hardware: servers, devices, run-time nodes and the communication links between them. Web-app example: how the web server, application server and database server are configured and connected.',
               'A **component diagram** shows how software components are organised and depend on each other through interfaces. Web-app example: the authentication library, data-access objects and business logic, and how they interact. Component = logical structure; deployment = where it runs.'],
        exam=[likely('Which diagram shows hardware nodes and the software deployed on them?', a=0,
                     opts=['Deployment diagram', 'Component diagram', 'Class diagram', 'Sequence diagram'])]),
    20: dict(
        hl=[('speech', 1), ('waveform', 1), ('component and sequence diagrams', 2), ('Controller', 3, 0, 'ocr')],
        notes=['The exercise: a speech-recognition system. Input is speech as a waveform (single words or whole sentences); output is English text on the screen.',
               'Using the structure on the left (Segmentation, Word creation and Phrase creation agents around a controller and a blackboard holding segments S1…S9, words and phrases), draw the **component and sequence diagrams** with the blackboard pattern.',
               '(The table on the right is unreadable in the PDF because of a font problem; slides 21–23 give its content and the solution.) The **controller** coordinates the agents; the **blackboard** is the shared memory where segments, words and phrases are stored and refined.']),
    21: dict(
        hl=[('Segmentation Agent', 1), ('Phrase Creation Agent', 2), ('Final Structured Output', 3)],
        notes=['A walk-through on sample text. **Segmentation agent**: splits the input into sentences (“Artificial intelligence is transforming education.” …).',
               'The **word creation agent** (between them) builds words from segments; the **phrase creation agent** groups words into grammatically correct phrases: NP “Artificial intelligence”, VP “is transforming”, NP “education”.',
               'The **final structured output** on the blackboard holds the sentence, its words and its phrases, each written by a different agent.']),
    22: dict(
        hl=[('Solution', 1), ('If the', 2), ('controller is active', 2)],
        notes=['The component solution: Segmentation, Word Creation and Phrase Creation agents each require the blackboard (reads/writes) and provide their own operation; the controller requires the agents and the blackboard and orchestrates them; the blackboard provides read/write and event services. (The table is garbled in the PDF; the diagram on the right shows the same structure.)',
               'The note answers a common doubt: give the controller a **provided interface** only if it is **active** (offers services such as scheduling or policies to others); if it just manages agents and the blackboard internally, it has none.']),
    23: dict(
        hl=[('Solution', 1), ('Controller', 2, 0, 'ocr')],
        notes=['The sequence solution, top to bottom: the controller initialises the blackboard, then repeats the same cycle for each agent: **request** (segmentation, word creation, phrase creation) → the agent returns its data → the controller **updates** the blackboard → the blackboard confirms (dashed feedback arrows).',
               'It ends with `CheckCompletion()` / `CompletionStatus()` and `Finalize()`. In this solution the controller writes to the blackboard on the agents’ behalf; in the scheduling example the agents wrote themselves. Both are accepted variants: what matters is that agents never call each other.']),
    24: dict(
        hl=[('transporting data', 1), ('Worker components', 2), ('Transport components', 3)],
        notes=['**Data flow** systems are decomposed around **transporting** data streams and **transforming** them on the way to meet application needs.',
               '**Worker components** perform work on the data.',
               '**Transport components** move the data.']),
    25: dict(
        hl=[('Encryption and decryption', 1), ('Compression and decompression', 1), ('Changing data format', 1), ('Transport components abstract the management', 2)],
        notes=['Worker components abstract the transformations applied before data is forwarded: encryption/decryption, compression/decompression, changing format (binary to XML, raw data to information), enhancing, modifying or storing data.',
               'Transport components abstract how data is moved and controlled. The data-flow pattern studied here is **pipes and filters**: filters are the workers, pipes the transport.']),
    26: dict(
        hl=[('Data Source', 1), ('Carry data from one step', 2), ('Process the data', 3), ('Data Sink', 4), ('Important Note', 5)],
        notes=['**Data source**: produces the input data.',
               '**Pipes**: carry data from one step to the next.',
               '**Filters**: process the data (transform, clean, analyse) and pass it on. In the diagram data branches: Filter 1 feeds Filters 2, 3 and 4, which rejoin at Filter 5.',
               '**Data sink**: the final destination where the processed data is stored or used.',
               '**Important**: the box-and-line diagram is not UML and hides how pipes really work; in real systems pipes can be function calls, files, queues or sockets.'],
        exam=[asked('f252', 'Q4-2 · 2.5 marks', 'StreamFlow: a desktop app for broadcasters processes live video in real time. Frames are modified as they pass through the application before being sent to the streaming server, through transformations in a specific order: Noise Reduction, Color Grading, Watermarking and Compression. Identify the architecture pattern and draw its component diagram.',
                    a='**Pipe-and-filter.** Each transformation is an independent filter; frames flow between them through pipes in a fixed order, so filters can be replaced or reordered without touching the others: Live feed (source) → Noise Reduction → Color Grading → Watermarking → Compression → Streaming server (sink).')]),
    27: dict(
        hl=[('Data source - produces the data', 1), ('Filter - processes', 2), ('Pipes - Provide connections', 3), ('Data Sink - data consumer', 4)],
        notes=['The four components, formally. **Data source**: produces the data.',
               '**Filter**: processes, enhances or modifies the data.',
               '**Pipe**: connects source → filter, filter → filter, and filter → sink.',
               '**Data sink**: consumes the data.'],
        exam=[likely('In pipes and filters, which component transforms the data?', a=0, opts=['Filter', 'Pipe', 'Data sink', 'Data source'])]),
    28: dict(
        hl=[('Language Processor', 1)],
        notes=['Example 1: a **language processor** (compiler or interpreter) is the classic pipes-and-filters system: source code flows through lexical analysis, parsing, code generation and optimisation.']),
    29: dict(
        hl=[('Lexical Analyzer', 1, 0, 'ocr'), ('Parser', 2, 0, 'ocr'), ('Optimizer', 3, 0, 'ocr')],
        notes=['**Lexical analyser** (filter 1): breaks source code into tokens. `int x = 5;` becomes `int`, `x`, `=`, `5`, `;`.',
               '**Parser**: builds a parse tree from the tokens (a declaration node for `int x`, an initialisation node for `= 5`). **Code generator**: turns the tree into machine code or an intermediate form (allocate memory for x, move 5 into it).',
               '**Optimizer**: makes the code faster or smaller (e.g. one instruction that both reserves and initialises x). In an **interpreter** pipeline the last filter executes the intermediate form directly instead. The diagram shows that filters are reusable: the same lexer and parser serve both pipelines.']),
    30: dict(
        hl=[('Lexical Analyzer (1:call())', 1), ('Parser (2:process()', 2), ('Code Generator (', 3), ('Optimizer (6:process())', 4)],
        notes=['The same pipeline as a UML sequence diagram (“Important: a UML diagram!”). **1: call()** feeds input to the lexical analyser.',
               'The parser **2: process()**es the tokens into a parse tree and **3: call()**s the code generator.',
               'The code generator **4: process()**es the tree into code and **5: call()**s the optimizer.',
               'The optimizer **6: process()**es the code. Here the pipes are simply function calls between filters.']),
    31: dict(
        hl=[('access videos', 1), ('detects faces', 1), ('recognizes faces', 1), ('predicts the identity', 1), ('next slide', 2)],
        notes=['Example 2: software that identifies people automatically. In order: it **accesses videos** (with audio) from YouTube, **detects faces** (is there a face?), **recognises faces** (whose face is it?), and **predicts the identity** of the individuals.',
               'Each step consumes the previous step’s output, which makes it a pipes-and-filters system; the next slides model it.'],
        exam=[asked('m252', 'Q6 · 2 marks', 'A piece of software works out who a person is automatically with a pipe-and-filter architecture: it accesses videos (with audio) from YouTube, detects faces, recognizes faces, and predicts the identity. (1) Place the lifelines of the sequence diagram from left to right in the order the data flows. (2) Which statements about the correct diagram are true?',
                    a='**Order**: access videos → detects faces → recognizes faces → predicts the identity. **True statements**: “access videos” sends the video/audio stream (message 1) to “detects faces”; “detects faces” has a self-message (1.1) for its own processing before passing detected faces on (1.2); “recognizes faces” receives the detected faces and sends recognized faces (1.2.2) to “predicts the identity”; the flow ends with “predicts the identity” running its own prediction step (1.2.2.1), forwarding nothing (it is the sink).')]),
    32: dict(
        hl=[('Big Video File', 1), ('YouTube Manager', 1), ('Face Detection', 2), ('Face Recognition', 3), ('Identity Manager', 4)],
        notes=['The box-and-line view: a **big video file** enters the **YouTube Manager**, which prepares it.',
               '**Face detection** turns the video into data containing only the detected faces.',
               '**Face recognition** matches the detected faces against known ones.',
               '**Identity manager** produces the final output, such as an identity report (“Wanted: Joe Developer”). The callout asks the design question: if a better recognition algorithm appears, only that one filter changes.']),
    33: dict(
        hl=[('how data is transported', 1), ('UML component', 2)],
        notes=['The box-and-line diagram shows the components but says nothing about **how data is transported** between filters, i.e. the pipes.',
               'A UML component diagram (next slide) makes the transport explicit.']),
    34: dict(
        hl=[('FileSystemWatcher', 1), ('Processing Pipeline', 2), ('IFileSystemPipe', 3, 0, 'ocr')],
        notes=['Here the pipe is the **file system**: a FileSystemManager component (built on .NET’s FileSystemWatcher) monitors directories and fires an event when a new file appears.',
               'The pipeline components (VideoManager, FaceDetection, FaceRecognition, IdentityManager) each require the **IFileSystemPipe** interface the manager provides. A filter writes its output as a file; the manager detects it and triggers the next filter. The warning notes this is not the typical pipes-and-filters example but shows how flexible the pattern is.']),
    35: dict(
        hl=[('VideoManager', 1), ('FaceDetection', 2), ('FaceRecognition', 3), ('IdentityManager', 4), ('FileSystemManager', 5)],
        notes=['**VideoManager**: `put(file)` places a new video file into the system (message 4).',
               '**FaceDetection**: `register()`s with the FileSystemManager at start-up, then, when notified, `process()`es the video for faces and `put(file)`s its result.',
               '**FaceRecognition**: registers, processes the detected faces when notified, and puts the recognised-face data forward.',
               '**IdentityManager**: registers and, when notified, processes the recognition data to determine identity (the last step: “identity determined!”).',
               '**FileSystemManager**: the coordinator. Its `onFileDetected(file)` notifies the registered filter whenever a new or processed file appears, which is what moves data along the pipeline.']),
    36: dict(
        hl=[('Quality properties', 1), ('Extensibility', 1), ('Efficiency', 1), ('Reusability', 1), ('Modifiability', 1), ('Security', 1), ('Maintainability', 1)],
        notes=['**Extensibility**: add new filters easily (a spam filter). **Efficiency**: filters can run in parallel. **Reusability**: filters are reused across systems. **Modifiability**: add, remove or change filters independently. **Security**: security filters can be inserted anywhere in the chain. **Maintainability**: independent filters make updates simple. Trade-off: every boundary needs agreed data formats, and the pattern suits batch-like flows, not interactive ones where the user steers the work midway.'],
        exam=[likely('List three quality properties of the pipes-and-filters pattern.',
                     a='Any three of: extensibility (new filters), efficiency (filters run concurrently), reusability, modifiability (add/remove/reorder filters), security (insert security filters), maintainability.')]),
    37: dict(
        hl=[('multiple processes', 1), ('collaborate', 1), ('client', 2), ('peer nodes', 3), ('similar capabilities', 3)],
        notes=['**Distributed** systems are decomposed into multiple processes that usually collaborate over a network.',
               '**Client–server**: client-side processes work for users and act as a bridge to a remote server that does the work delegated to it.',
               '**Peer-to-peer**: peer nodes with similar capabilities collaborate as equals, e.g. music-sharing applications. The pictures contrast a mesh of peers with a star around one server.']),
    38: dict(
        hl=[('multiple physical nodes', 1), ('multi-core processors', 2)],
        notes=['Those systems are easy to spot because they are deployed on **multiple physical nodes**.',
               'With **multi-core processors**, distributed architecture also applies inside a single machine: work is spread across cores instead of computers.']),
    39: dict(
        hl=[('Internet systems', 1), ('Client-Server Pattern', 2), ('Broker Pattern', 2), ('Peer-to-Peer (P2P)', 3)],
        notes=['Examples: Internet systems, web services, file- and music-sharing systems, high-performance computing.',
               'Common patterns: **client–server** (clients request, a central server provides, e.g. browser and web server) and **broker**.',
               '**Peer-to-peer**: every node is both client and server, sharing resources with no central server (BitTorrent).'],
        exam=[likely('How does peer-to-peer differ from client–server?',
                     a='In client–server, clients request services from a central server. In peer-to-peer every node acts as both client and server and they collaborate without relying on one central node, so the system keeps working when any single peer leaves.')]),
    40: dict(
        hl=[('Server:', 1), ('Client:', 2), ('Bottom part (UML Deployment Diagram)', 3), ('HTTP', 4)],
        notes=['**Server**: a program or device that provides functionality to other programs or devices, its clients.',
               '**Client**: hardware or software that accesses a service the server makes available. Many independent clients talk to the server, and **clients do not talk to each other**.',
               '**Deployment diagram** (bottom): the PC node runs `pc_browser.exe`, the mobile node runs `mp_browser.exe`, and the server node runs `web_server.exe` (artifacts on nodes).',
               'Clients communicate with the server over **HTTP**; the server responds with processed data. The box-and-line diagram above shows the same thing as request/response arrows.']),
    41: dict(
        hl=[('Interoperability', 1), ('Modifiability', 2), ('Availability', 3), ('Reusability', 4)],
        notes=['**Interoperability**: clients on different platforms work with servers on different platforms (any browser, any OS).',
               '**Modifiability**: changes are made once at the server and reach all clients.',
               '**Availability**: backup server nodes keep the service and data available.',
               '**Reusability**: server services and data can be reused by different applications.'],
        exam=[asked('m261', 'Q6 (one of seven)', 'A classroom response application allows hundreds of students to submit answers from their phones while an instructor watches the results on a dashboard. Scores and question status must come from one authoritative course session so that every participant sees consistent information. Which architectural style?',
                    a='**Client-server**: one authoritative central service that many clients use.')]),
    42: dict(
        hl=[('tightly coupled', 1), ('exact IP/URL/protocol', 2), ('Broker pattern was introduced', 3)],
        notes=['The main problem: **clients are tightly coupled to servers**, which becomes complex when services come from many servers in different places.',
               'The client must know the server’s exact IP/URL/protocol, and any server change forces client code updates.',
               'The **broker** pattern was introduced to remove that coupling.'],
        exam=[likely('What is the main drawback of client–server that the broker pattern fixes?', a=0,
                     opts=['Clients are tightly coupled to specific servers', 'It cannot store data', 'It needs a blackboard', 'Clients talk to each other'])]),
    43: dict(
        hl=[('mediator between the two components', 1), ('decreases coupling', 2), ('Client-Server', 3), ('Communication goes through a', 3)],
        notes=['The **broker** pattern gives more flexibility between clients and servers in a distributed environment by acting as a **mediator** between them.',
               'It **decreases coupling**: one client can transparently use the services of many servers, knowing only the broker.',
               'Comparison: **client–server** is direct, the client must know the server’s address and protocol, server changes need client updates, simpler but less flexible. **Broker** goes through middleware, the client knows only the broker, server changes don’t affect clients, more scalable. In short: direct and tight vs. indirect and loose.'],
        exam=[asked('m261', 'Q6 (one of seven)', 'A hospital application sends requests to several types of laboratory equipment supplied by different vendors. Equipment can be replaced or added over time, but the clinical application should continue using the same request format and should not need vendor-specific logic. Which architectural style?',
                    a='**Broker**: the broker hides vendor- and service-specific communication behind one request format.')]),
    44: dict(
        hl=[('coordinating communication', 1), ('flexible', 2), ('interoperable', 2), ('Broker can communicate', 3, 0, 'ocr')],
        notes=['The **broker** coordinates communication between clients and servers: it forwards requests and transmits results and exceptions back.',
               'This makes systems more **flexible and interoperable**. In the diagram the client relies on Broker 1 for services from Server 1, and Broker 1 can talk to Broker 2 to reach Server 2’s services too.']),
    45: dict(
        hl=[('Applications that use the services', 1), ('Local service to Client', 2), ('mediates between client and server', 3), ('transparency (at server)', 4), ('Real application services', 5), ('Optional component', 6)],
        notes=['**Client**: uses services of one or more servers. Provides nothing; requires the client proxy.',
               '**Client proxy**: makes remote components look local to the client (transparency). Provides a local service to the client; requires the broker.',
               '**Broker**: mediates between client and server components. Provides mediation to the client proxy; requires the server proxy.',
               '**Server proxy**: makes remote components look local on the server side. Provides a local service to the broker; requires the server.',
               '**Server**: provides the real application services (it may also act as a client of the broker).',
               '**Bridge** (optional): connects different brokers so they can interoperate.'],
        exam=[likely('List the components of the broker pattern in the order a request passes through them.',
                     a='Client → client-side proxy → broker → server-side proxy → server (a bridge optionally connects brokers). The response returns the same way.')]),
    46: dict(
        hl=[('The client side proxy decides', 1), ('Separates system', 2), ('Detailed Broker Pattern', 3, 0, 'ocr')],
        notes=['The **client-side proxy** decides whether a request can be resolved locally or must be forwarded to the broker.',
               'The pattern **separates communication functionality from application functionality**: everything about networks and messages sits in the broker and proxies, so clients and servers contain only application logic.',
               {'text': 'Reading the detailed class diagram:', 'items': [
                   ('Client-side proxy', '`packData()`, `unpackData()`, `sendRequest()`, `return()`: marshals requests into messages and results back out.'),
                   ('Broker', '`registerService()`, `findServer()`, `findClient()`, `forwardRequest()`, `forwardResponse()`: knows where services are and routes messages.'),
                   ('Server-side proxy', '`packData()`, `unpackData()`, `callService()`, `sendResponse()`: calls the real service.'),
                   ('Client / Server / Bridge', 'The client calls `callServer()` via the broker API; the server `registerService()`s and `runService()`s; the bridge transmits messages between brokers.')]}]),
    47: dict(
        hl=[('Interoperability', 1), ('Modifiability', 2), ('Portability', 3), ('Reusability', 4)],
        notes=['**Interoperability**: clients work with servers on different platforms, and with multiple servers.',
               '**Modifiability**: server changes are centralised and reach many clients quickly.',
               '**Portability**: the broker can be ported to new platforms, opening the services to new clients.',
               '**Reusability**: because brokers handle the system calls, complex services can be reused in other applications.'],
        exam=[likely('Which is a quality property of the broker pattern?', a=0,
                     opts=['Interoperability across platforms', 'Tighter client–server coupling', 'No need for middleware', 'Guaranteed fastest performance'])]),
    48: dict(
        hl=[('Blackboard pattern', 1), ('Pipes-and-Filters pattern', 2), ('Client Server pattern', 3), ('Broker pattern', 3), ('Interactive Systems', 4)],
        notes=['Data-centered → **blackboard**.',
               'Data flow → **pipes and filters**.',
               'Distributed → **client–server** and **broker**.',
               'Next: interactive systems (MVC) and hierarchical systems (layered).']),
}

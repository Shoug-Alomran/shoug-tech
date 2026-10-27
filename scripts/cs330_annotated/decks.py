"""CS330 annotated slides — every Operating Systems deck (Silberschatz chapters 1–6, 8, 9, 11, 12).

One module holds all the decks: each deck is a namespace class with DECK and ANN (and AUTO_SLIDES).
Slides without an ANN entry are shown without notes. past('q1', ...) points at the real past-exam
questions collected in exams/08-quiz-1-ch-1-and-2. See cs331_annotated/ch01_1_introduction.py for the ANN keys."""
from .common import DECKS, mcq, past, see, short, tf, tip, trap, trick


def deck(key, title, chapter, lede):
    slug, file, folder, _ = DECKS[key]
    return {'key': key, 'slug': slug, 'file': file, 'title': title, 'chapter': chapter,
            'pdf': '/academics/computer-science/cs330/slides/%s/' % folder, 'lede': lede}


class intro:
    AUTO_SLIDES = True
    DECK = deck('d01', 'Introduction to Operating Systems', 'Chapter 1',
                'What an operating system does, computer-system organization (interrupts, storage hierarchy, caching, '
                'DMA), single- and multiprocessor and clustered systems, multiprogramming and time-sharing, dual-mode '
                'operation and the timer, and process, memory and storage management.')
    ANN = {
        4: dict(notes=['OS = a program that acts as an intermediary between the user and the hardware.'],
                past=[past('q1', 'Q1: the intermediary between user and hardware')],
                exam=[mcq('A program that acts as an intermediary between a user of a computer and the hardware is:', ['Operating system', 'Interrupt service routine', 'Caching', 'CPU'], 0, '')], weight=3),
        5: dict(notes=['Four components: hardware, operating system, application programs, users.'],
                past=[past('q1', 'Q21: list the four components')],
                exam=[short('List the four main components of a computer system.', 'Hardware (CPU, memory, I/O), operating system (controls and coordinates hardware use), application programs (solve the users’ problems with the resources), and users (people, machines, other computers).')], weight=3),
        9: dict(notes=['OS is a resource allocator (decides between conflicting requests) and a control program (prevents errors and misuse).'],
                past=[past('q1', 'Q18: deciding between conflicting requests')],
                exam=[mcq('When the OS decides between conflicting requests for CPU, memory and I/O, it acts as a:', ['Resource allocator', 'Control program', 'Process creator', 'User interface'], 0, '')], weight=3),
        10: dict(notes=['The kernel is "the one program running at all times"; everything else is a system program or an application.']),
        11: dict(notes=['Bootstrap program: loaded at power-up (in ROM/firmware), initializes the system and loads the kernel.']),
        15: dict(notes=['Interrupts transfer control to an interrupt service routine through the interrupt vector. A trap (exception) is a SOFTWARE-generated interrupt (error or system call).'],
                 past=[past('q1', 'Q14: the software-generated interrupt')],
                 exam=[mcq('Which is a software-generated interrupt?', ['Trap', 'Disk completion', 'Power failure', 'Keyboard input'], 0, '')], weight=3),
        20: dict(notes=['Main memory is the only large storage the CPU accesses directly; it is volatile. Secondary storage (disks, SSDs) is nonvolatile.'],
                 past=[past('q1', 'Q7, Q11, Q20: main memory vs. secondary storage')],
                 exam=[mcq('The only large storage media that the CPU can access directly is:', ['Main memory', 'Solid-state disk', 'Magnetic disk', 'Optical disk'], 0, ''),
                       mcq('Compared with magnetic disks, SSDs are:', ['Faster and nonvolatile', 'Faster but volatile', 'Slower but cheaper', 'Larger and volatile'], 0, '')], weight=3),
        21: dict(notes=['Storage hierarchy: registers → cache → main memory → SSD → disk → optical/tape. Higher = faster, smaller, costlier, usually volatile.']),
        22: dict(notes=['Caching: copy data into faster storage temporarily to minimize access time.'],
                 past=[past('q1', 'Q4, Q15: why caching matters'), past('q1', 'Q22: what the CPU fetches', related=True)],
                 exam=[mcq('Caching is important in OS design to:', ['Minimize access time', 'Expand storage', 'Replace secondary memory', 'Reduce volatility'], 0, '')], weight=3),
        25: dict(notes=['DMA: the device controller moves a whole block between the device and memory without the CPU; one interrupt per block, not per byte.'],
                 past=[past('q1', 'Q5: moving large blocks without the CPU')],
                 exam=[mcq('______ moves large amounts of data between I/O devices and main memory without the CPU.', ['DMA', 'ISR', 'SSD', 'DLM'], 0, '')], weight=3),
        30: dict(notes=['Multiprocessor advantages: increased throughput, economy of scale, increased reliability (graceful degradation / fault tolerance).'],
                 past=[past('q1', 'Q2, Q13: multiprocessor advantages')],
                 exam=[mcq('Multiprocessor systems’ advantage is:', ['All of the above', 'Economy of scale', 'Increased throughput', 'Increased reliability'], 0, '')], weight=3),
        31: dict(notes=['Asymmetric: boss–worker, each processor has a specific task. Symmetric (SMP): each processor performs all tasks.'],
                 past=[past('q1', 'Q10: recognising SMP')],
                 tips=[trap('"Boss–worker" and "each processor assigned a specific task" describe ASYMMETRIC multiprocessing.')],
                 exam=[mcq('Which indicates a symmetric multiprocessing system?', ['Each processor performs all tasks in the OS', 'Each processor is assigned a specific task', 'A boss–worker relationship between processors', 'Only one processor runs the kernel'], 0, '')], weight=3),
        32: dict(notes=['Clustered systems: multiple systems working together over a network, usually sharing storage; high availability.']),
        35: dict(notes=['Multiprogramming keeps several jobs in memory so the CPU always has one to run (overlaps CPU with I/O). Time-sharing switches so often that users can interact with each job.'],
                 past=[past('q1', 'Q12, Q17, Q23: multiprogramming vs. time-sharing')],
                 exam=[short('What is the difference between multiprogramming and time-sharing?', 'Multiprogramming organizes jobs so the CPU always has one to execute: when a job waits (e.g. for I/O) the OS switches to another, increasing CPU utilization. Time-sharing extends this by switching so frequently that users can interact with each program while it runs (interactive computing, short response time).')], weight=3),
        37: dict(notes=['Dual mode: user mode and kernel mode (mode bit). Privileged instructions run only in kernel mode; a system call switches to kernel mode.'],
                 exam=[tf('Privileged instructions can be executed in user mode.', False, 'They trap to the OS if attempted in user mode.')], weight=3),
        38: dict(notes=['The timer interrupts after a set period so a user program can’t run forever and keep the CPU from the OS.'],
                 past=[past('q1', 'Q3, Q19: what the timer prevents')],
                 exam=[mcq('A ____ prevents a user program from never returning control to the OS.', ['Timer', 'Portal', 'Firewall', 'Program counter'], 0, '')], weight=3),
        39: dict(notes=['A process is a program in execution (active); a program is passive.']),
        40: dict(notes=['Process management: create/delete, suspend/resume, and mechanisms for synchronization, communication and deadlock handling.'],
                 past=[past('q1', 'Q8: process-management activities')], weight=2),
    }


class services:
    AUTO_SLIDES = True
    DECK = deck('d02', 'Operating System Services and Structures', 'Chapter 2',
                'OS services, command-line, GUI and touch interfaces, system calls and APIs (POSIX, Win32, Java), '
                'parameter passing, types of system calls, and OS structures: monolithic, layered, microkernel, '
                'modules and hybrid systems.')
    ANN = {
        4: dict(notes=['Services for the user: UI, program execution, I/O, file-system manipulation, communication, error detection.']),
        5: dict(notes=['Services for the system itself: resource allocation, accounting (logging), protection and security.']),
        7: dict(notes=['CLI (command interpreter / shell) reads and runs commands; GUI uses windows and a mouse; touch interfaces use gestures.']),
        12: dict(notes=['System calls are the programming interface to OS services; programs usually reach them through an API (Win32, POSIX, Java API).'],
                 past=[past('q1', 'Q25, Q26, Q31: system-call interface and APIs')],
                 tips=[trap('The JVM is not a system-call API; the Java API is.')],
                 exam=[mcq('The API that Unix-like systems give programmers is:', ['POSIX', 'Win32', 'JVM', 'DirectX'], 0, ''),
                       mcq('The three most common APIs for system calls include all EXCEPT:', ['Java Virtual Machine', 'POSIX', 'Win32', 'Java API'], 0, '')], weight=3),
        14: dict(notes=['The system-call interface uses a table indexed by system-call number; the caller doesn’t need to know how it is implemented.']),
        15: dict(notes=['Passing parameters: in registers, in a block/table in memory (address in a register), or pushed on the stack.'],
                 exam=[mcq('Which is NOT a way to pass parameters to a system call?', ['Through the file system', 'Registers', 'A block in memory whose address is in a register', 'The stack'], 0, '')], weight=2),
        17: dict(notes=['Types: process control, file management, device management, information maintenance, communications, protection.'],
                 past=[past('q1', 'Q24, Q27: fork() and system-call categories')],
                 exam=[mcq('Which system call creates a process in UNIX?', ['fork()', 'exec()', 'open()', 'read()'], 0, 'exec() replaces the program in an existing process.')], weight=3),
        19: dict(notes=['printf() is a C library function that eventually calls the write() system call; it is not itself a system call.'],
                 past=[past('q1', 'Q29, Q30: printf and calling system calls directly')],
                 exam=[tf('printf() in C is a system call.', False, 'It is a library function that invokes write().')], weight=3),
        22: dict(notes=['Layered: layer 0 = hardware … layer N = UI; each uses only the layers below. Advantage: easy debugging and maintenance. Disadvantage: hard to define layers, overhead.'],
                 past=[past('q1', 'Q33: advantage of layering')],
                 exam=[short('Give one advantage of the layered approach.', 'Simple construction and debugging: each layer is debugged on top of already-verified lower layers, so an error is found in the layer being tested; layers can also be changed independently.')], weight=3),
        24: dict(notes=['Microkernel: move most services into user space; communicate by message passing. + easier to extend, port, more reliable and secure. − message-passing overhead.'],
                 past=[past('q1', 'Q28, Q32: microkernel location and disadvantage')],
                 exam=[mcq('In a microkernel OS, most OS functionality runs:', ['In user-space processes', 'In the kernel', 'In hardware', 'In device drivers only'], 0, ''),
                       short('Give one disadvantage of the microkernel approach.', 'Performance overhead: user-space services communicate through the kernel by message passing, which costs extra copies and context switches.')], weight=3),
        25: dict(notes=['Loadable kernel modules: core kernel + modules loaded as needed (like layers but any module can call any other).']),
        26: dict(notes=['Hybrid systems mix structures: Linux/Solaris monolithic + modules; Windows mostly monolithic + microkernel parts; macOS/iOS Mach + BSD.']),
    }


class processes:
    AUTO_SLIDES = True
    DECK = deck('d03', 'Process Management', 'Chapter 3',
                'The process concept and its memory layout, process states and the PCB, scheduling queues and '
                'schedulers, context switches, process creation (fork/exec) and termination, and interprocess '
                'communication with shared memory (bounded buffer) and message passing.')
    ANN = {
        4: dict(notes=['Process = program in execution. Parts: text (code), data (globals), heap (dynamic), stack (calls, locals), plus program counter and registers.']),
        6: dict(notes=['Memory layout from low to high: text, data, heap (grows up) … stack (grows down).'],
                exam=[mcq('Local variables and return addresses are stored in the process’s:', ['Stack', 'Heap', 'Data section', 'Text section'], 0, '')], weight=3),
        7: dict(notes=['States: new, ready, running, waiting, terminated.']),
        8: dict(notes=['Transitions: ready → running (dispatch), running → ready (interrupt), running → waiting (I/O or event wait), waiting → ready (I/O done).'],
                tips=[trap('A waiting process goes to READY when its I/O completes, never straight to running.')],
                exam=[mcq('When a process’s I/O completes, it moves from waiting to:', ['Ready', 'Running', 'Terminated', 'New'], 0, '')], weight=3),
        9: dict(notes=['PCB (task control block) stores state, program counter, registers, scheduling, memory-management, accounting and I/O status info.'],
                exam=[mcq('Which is NOT stored in a PCB?', ['The program’s source code', 'Program counter', 'Process state', 'CPU registers'], 0, '')], weight=3),
        14: dict(notes=['Ready queue: processes in memory waiting for the CPU. Wait queues: waiting for an event or device.']),
        16: dict(notes=['Short-term (CPU) scheduler: picks the next ready process, runs very often. Long-term (job) scheduler: controls the degree of multiprogramming.'],
                 exam=[mcq('The scheduler that controls the degree of multiprogramming is the:', ['Long-term scheduler', 'Short-term scheduler', 'Dispatcher', 'Medium-term scheduler'], 0, '')], weight=3),
        17: dict(notes=['Medium-term scheduler: swaps processes out of memory and back in to reduce the degree of multiprogramming.']),
        18: dict(notes=['I/O-bound processes: many short CPU bursts. CPU-bound: few long bursts. A good mix keeps both CPU and devices busy.']),
        19: dict(notes=['Context switch: save the old process’s state into its PCB and load the new one’s. Pure overhead: no useful work is done.'],
                 exam=[tf('During a context switch the system does useful work for the processes.', False, 'It is overhead.')], weight=3),
        22: dict(notes=['Parent creates children → a tree of processes (identified by pid). Parent and child may share all, some or no resources; parent may wait or run concurrently.']),
        23: dict(notes=['UNIX: fork() makes a copy of the parent; exec() replaces the child’s memory with a new program; wait() lets the parent wait.'],
                 exam=[mcq('After fork(), the return value in the child process is:', ['0', 'The child’s pid', 'The parent’s pid', '−1'], 0, 'The parent receives the child’s pid; −1 means failure.')], weight=3),
        27: dict(notes=['exit() ends a process; the parent collects the status with wait(). Zombie: terminated but parent hasn’t called wait(). Orphan: parent ended without waiting.'],
                 exam=[mcq('A process that has terminated but whose parent has not yet called wait() is a:', ['Zombie', 'Orphan', 'Daemon', 'Thread'], 0, '')], weight=3),
        31: dict(notes=['Independent vs. cooperating processes. Cooperation reasons: information sharing, computation speed-up, modularity, convenience.']),
        32: dict(notes=['Two IPC models: shared memory (fast, processes synchronize themselves) and message passing (kernel involved, easier for small data and distributed systems).'],
                 exam=[mcq('Which IPC model is usually faster once set up?', ['Shared memory', 'Message passing', 'Pipes over a network', 'Signals'], 0, 'No system call per exchange after the region is set up.')], weight=3),
        33: dict(notes=['Producer–consumer: producer fills a buffer, consumer empties it. Unbounded vs. bounded buffer.']),
        35: dict(notes=['Circular bounded buffer: in = next free slot, out = first full slot. Empty when in == out; full when (in + 1) % SIZE == out, so only SIZE − 1 items fit.'],
                 exam=[mcq('With the in/out bounded-buffer solution and BUFFER_SIZE = 10, at most how many items can be in the buffer?', ['9', '10', '11', '5'], 0, 'One slot stays empty to tell full from empty.')], weight=3),
        38: dict(notes=['Adding a count variable lets all slots be used, but count++ / count-- then need synchronization (race condition → Ch 6).'],
                 seen=[see('d06', 6, 'the race on count')]),
        41: dict(notes=['Message passing: send(message) and receive(message) over a communication link.']),
        44: dict(notes=['Direct communication: name the process explicitly (send(P, msg)); one link per pair.']),
        45: dict(notes=['Indirect communication: send to / receive from a mailbox (port); a link can join many processes.'],
                 exam=[mcq('In indirect communication, messages are sent to:', ['A mailbox (port)', 'A named process', 'The PCB', 'The ready queue'], 0, '')], weight=2),
        47: dict(notes=['Blocking (synchronous) vs. non-blocking (asynchronous) send and receive. Blocking send + blocking receive = rendezvous.']),
    }


class threads:
    AUTO_SLIDES = True
    DECK = deck('d04', 'Threads and Concurrency', 'Chapter 4',
                'Why threads, single vs. multithreaded processes, benefits, multicore programming and its challenges, '
                'concurrency vs. parallelism, user and kernel threads, and the many-to-one, one-to-one, many-to-many '
                'and two-level models.')
    ANN = {
        5: dict(notes=['A thread is a basic unit of CPU use: thread ID, program counter, registers, stack. Threads of one process SHARE code, data and open files.'],
                exam=[mcq('Which is NOT shared between threads of the same process?', ['Stack', 'Code section', 'Global data', 'Open files'], 0, 'Each thread has its own stack and registers.')], weight=3),
        9: dict(notes=['Benefits: responsiveness, resource sharing, economy (cheaper than processes), scalability on multicore.'],
                exam=[mcq('Which is a benefit of multithreading?', ['All of these', 'Responsiveness', 'Resource sharing', 'Economy'], 0, '')], weight=3),
        10: dict(notes=['Multicore challenges: identifying tasks, balance, data splitting, data dependency, testing and debugging.']),
        12: dict(notes=['Concurrency: more than one task making progress (possible on one core by interleaving). Parallelism: tasks running at the same time (needs multiple cores).'],
                 tips=[trick('Parallelism ⇒ concurrency, but concurrency does not need parallelism.')],
                 exam=[tf('Concurrency is possible on a single-core system.', True, 'By interleaving.'),
                       tf('Parallelism is possible on a single-core system.', False, '')], weight=3),
        13: dict(notes=['User threads: managed by a user-level library (POSIX Pthreads, Java, Windows threads APIs).']),
        14: dict(notes=['Kernel threads: managed by the OS kernel.']),
        17: dict(notes=['Many-to-one: many user threads → one kernel thread. One blocking call blocks all; no parallelism on multicore.'],
                 exam=[mcq('In the many-to-one model, if one thread makes a blocking system call:', ['The whole process blocks', 'Only that thread blocks', 'A new kernel thread is created', 'The call fails'], 0, '')], weight=3),
        18: dict(notes=['One-to-one: each user thread gets a kernel thread (Windows, Linux). More concurrency, but many kernel threads may hurt performance.']),
        19: dict(notes=['Many-to-many: many user threads multiplexed on a smaller or equal number of kernel threads.']),
        20: dict(notes=['Two-level: many-to-many that also lets a user thread be bound to a kernel thread.']),
    }


class scheduling:
    AUTO_SLIDES = True
    DECK = deck('d05', 'CPU Scheduling', 'Chapter 5',
                'CPU–I/O burst cycle, preemptive vs. nonpreemptive scheduling, the dispatcher, scheduling criteria, '
                'FCFS, SJF and SRTF (with exponential averaging), Round Robin, priority, multilevel and multilevel '
                'feedback queues, thread and real-time scheduling, and algorithm evaluation.')
    GANTT = 'Waiting time = turnaround − burst. Turnaround = completion − arrival. Response = first run − arrival. Draw the Gantt chart first.'
    ANN = {
        4: dict(notes=['Processes alternate CPU bursts and I/O bursts; most CPU bursts are short.']),
        7: dict(notes=['Scheduling decisions when a process: 1) running → waiting, 2) running → ready, 3) waiting → ready, 4) terminates. Only 1 and 4 → nonpreemptive; otherwise preemptive.'],
                exam=[mcq('Under nonpreemptive scheduling, the CPU is taken from a process only when it:', ['Terminates or switches to waiting', 'Uses up its time quantum', 'A higher-priority process arrives', 'An interrupt occurs'], 0, '')], weight=3),
        9: dict(notes=['Dispatcher gives the CPU to the chosen process: context switch, switch to user mode, jump to the right instruction. Dispatch latency = time to do this.']),
        10: dict(notes=['Maximize CPU utilization and throughput; minimize turnaround, waiting and response time.'],
                 tips=[tip(GANTT)],
                 exam=[mcq('Which criterion should be MINIMIZED?', ['Waiting time', 'CPU utilization', 'Throughput', 'All of these'], 0, '')], weight=3),
        12: dict(notes=['FCFS: run in arrival order; nonpreemptive. Convoy effect: short processes wait behind a long one.'],
                 exam=[mcq('P1 = 24, P2 = 3, P3 = 3 arrive in that order at time 0. FCFS average waiting time:', ['17', '3', '10', '27'], 0, '(0 + 24 + 27) / 3.')], weight=3),
        13: dict(notes=['Order P2, P3, P1 gives average wait (6 + 0 + 3) / 3 = 3: order matters a lot.']),
        14: dict(notes=['SJF: run the shortest next CPU burst. Optimal: minimum average waiting time for a given set. Problem: you can’t know the next burst length.'],
                 exam=[tf('SJF gives the minimum average waiting time for a given set of processes.', True, '')], weight=3),
        16: dict(notes=['Predict the next burst: τₙ₊₁ = α·tₙ + (1 − α)·τₙ (exponential averaging), usually α = ½.'],
                 exam=[mcq('τ₀ = 10, α = 0.5, the actual burst t₀ = 6. τ₁ =', ['8', '6', '10', '16'], 0, '0.5·6 + 0.5·10.')], weight=3),
        19: dict(notes=['SRTF = preemptive SJF: a new arrival with a shorter burst than the remaining time preempts the running process.'],
                 tips=[trap('In SRTF compare the newcomer with the REMAINING time of the running process, not its original burst.')], weight=3),
        21: dict(notes=['Round Robin: each process gets a time quantum q, then goes to the back of the ready queue. No process waits more than (n − 1)q.'],
                 exam=[mcq('P1 = 24, P2 = 3, P3 = 3, RR with q = 4. P1 completes at time:', ['30', '24', '28', '26'], 0, 'P1 runs 0–4, P2 4–7, P3 7–10, then P1 alone until 30.')], weight=3),
        23: dict(notes=['Large q → behaves like FCFS. Small q → too many context switches. q should be large compared with the context-switch time (80% of bursts < q).'],
                 exam=[mcq('If the RR time quantum is very large, RR behaves like:', ['FCFS', 'SJF', 'Priority', 'SRTF'], 0, '')], weight=3),
        25: dict(notes=['Priority scheduling (smaller number = higher priority here). Problem: starvation. Solution: aging (raise priority over time).'],
                 exam=[mcq('The solution to starvation in priority scheduling is:', ['Aging', 'Swapping', 'Paging', 'Thrashing'], 0, '')], weight=3),
        28: dict(notes=['Multilevel queue: separate queues (e.g. foreground RR, background FCFS), each with its own algorithm; scheduling between queues by fixed priority or time slices.']),
        31: dict(notes=['Multilevel feedback queue: processes MOVE between queues (demote CPU-hogs, age old ones up).'],
                 exam=[mcq('What distinguishes a multilevel FEEDBACK queue from a multilevel queue?', ['Processes can move between queues', 'It has more queues', 'It uses only FCFS', 'It never preempts'], 0, '')], weight=3),
        33: dict(notes=['Process-contention scope (user threads on LWPs) vs. system-contention scope (kernel threads competing system-wide).']),
        36: dict(notes=['Rate-monotonic: static priority = shorter period gets higher priority.']),
        43: dict(notes=['Deterministic modelling: compute each algorithm’s numbers for a given workload.']),
    }


class sync:
    AUTO_SLIDES = True
    DECK = deck('d06', 'Process Synchronization', 'Chapter 6',
                'Race conditions, the critical-section problem and its three requirements, Peterson’s solution, '
                'hardware support (test_and_set, swap), semaphores and their implementation, deadlock and starvation, '
                'the bounded-buffer, readers–writers and dining-philosophers problems, and monitors.')
    ANN = {
        6: dict(notes=['count++ is load–increment–store; interleaving these steps from two processes can lose an update.']),
        7: dict(notes=['Race condition: the result depends on the order in which processes access shared data.'],
                exam=[mcq('A situation where the outcome depends on the order of access to shared data is a:', ['Race condition', 'Deadlock', 'Starvation', 'Context switch'], 0, '')], weight=3),
        10: dict(notes=['Critical section: the code that touches shared data. Structure: entry section, critical section, exit section, remainder section.']),
        11: dict(notes=['Requirements: Mutual exclusion (one at a time), Progress (no needless waiting when the CS is free), Bounded waiting (no starvation).'],
                 tips=[trick('M-P-B: Mutual exclusion, Progress, Bounded waiting.')],
                 exam=[mcq('Which is NOT a requirement of a critical-section solution?', ['Preemption', 'Mutual exclusion', 'Progress', 'Bounded waiting'], 0, '')], weight=3),
        13: dict(notes=['Peterson’s solution (2 processes): shared turn and flag[2]. Pᵢ sets flag[i] = true, turn = j, then waits while flag[j] && turn == j.'], weight=3),
        16: dict(notes=['Hardware support: atomic (uninterruptible) instructions such as test_and_set and compare_and_swap.']),
        17: dict(notes=['test_and_set returns the old value and sets the lock to true, in one atomic step.']),
        21: dict(notes=['Semaphore S: integer accessed only by wait() (P: decrement, block if < 0) and signal() (V: increment, wake one).'],
                 exam=[mcq('wait(S) on a semaphore:', ['Decrements S and may block', 'Increments S', 'Always blocks', 'Resets S to 0'], 0, '')], weight=3),
        22: dict(notes=['Binary semaphore (0/1) = mutex lock. Counting semaphore controls access to N instances; initialize it to N.'],
                 exam=[mcq('A counting semaphore guarding 5 identical printers should be initialized to:', ['5', '1', '0', '−5'], 0, '')], weight=3),
        23: dict(notes=['Busy waiting (spinlock) wastes CPU; better implementation blocks the process on the semaphore’s waiting list.']),
        26: dict(notes=['Deadlock: each process waits for an event only another waiting process can cause. Starvation: indefinite blocking.'],
                 exam=[short('P0 runs wait(S); wait(Q); and P1 runs wait(Q); wait(S); with S = Q = 1. What can happen?', 'Deadlock: P0 gets S, P1 gets Q, then each waits forever for the semaphore the other holds.')], weight=3),
        28: dict(notes=['Bounded buffer: mutex = 1, full = 0, empty = n. Producer: wait(empty); wait(mutex); … signal(mutex); signal(full).'],
                 tips=[trap('Swapping the order to wait(mutex); wait(empty) can deadlock when the buffer is full.')],
                 exam=[mcq('In the bounded-buffer solution with n slots, empty starts at:', ['n', '0', '1', 'n − 1'], 0, '')], weight=3),
        31: dict(notes=['Readers–writers: many readers may read together; a writer needs exclusive access. rw_mutex = 1, mutex = 1, read_count = 0.']),
        35: dict(notes=['Dining philosophers: one semaphore per chopstick can deadlock if all pick up the left one at once.'],
                 exam=[mcq('Which avoids deadlock in dining philosophers?', ['Allow at most 4 philosophers at the table', 'Every philosopher picks up the left chopstick first', 'Use one more semaphore per chopstick', 'Let philosophers eat in any order'], 0, 'Also: pick up both only if both are free, or odd/even asymmetric ordering.')], weight=3),
        36: dict(notes=['Semaphore misuse: signal before wait, wait twice, or forgetting one → broken mutual exclusion or deadlock.']),
        37: dict(notes=['Monitor: high-level construct; only one process active inside at a time.']),
        40: dict(notes=['Condition variables: x.wait() suspends the caller; x.signal() resumes one waiting process (no effect if none).']),
    }


class memory:
    AUTO_SLIDES = True
    DECK = deck('d07', 'Memory Management', 'Chapter 8',
                'Address binding, logical vs. physical addresses and the MMU, swapping, contiguous allocation (first, '
                'best and worst fit) and fragmentation, segmentation, paging and address translation, the TLB and '
                'effective access time, protection and shared pages.')
    ANN = {
        4: dict(notes=['Binding at compile time (absolute code), load time (relocatable code) or execution time (needs hardware: MMU).']),
        6: dict(notes=['Logical (virtual) address: generated by the CPU. Physical address: seen by the memory unit. They differ under execution-time binding.']),
        8: dict(notes=['MMU maps logical to physical at run time; simplest form adds the relocation (base) register.'],
                exam=[mcq('With relocation register 14000, logical address 346 maps to:', ['14346', '346', '13654', '14000'], 0, '')], weight=3),
        9: dict(notes=['Swapping: move a process temporarily to a backing store and back. Transfer time dominates.']),
        12: dict(notes=['Contiguous allocation: each process in one block; base + limit registers protect it.']),
        15: dict(notes=['First fit: first hole big enough. Best fit: smallest hole big enough. Worst fit: largest hole.'],
                 exam=[mcq('Holes: 100, 500, 200, 300, 600 KB. Best fit places a 212 KB request in:', ['300 KB', '500 KB', '600 KB', '200 KB'], 0, ''),
                       mcq('Same holes; first fit places 212 KB in:', ['500 KB', '300 KB', '600 KB', '100 KB'], 0, '')], weight=3),
        18: dict(notes=['External fragmentation: enough total free memory but not contiguous (fix: compaction, paging). Internal: allocated block larger than requested.'],
                 tips=[trap('Paging has NO external fragmentation but can have internal fragmentation in the last page.')],
                 exam=[mcq('Paging eliminates:', ['External fragmentation', 'Internal fragmentation', 'Page faults', 'The need for a page table'], 0, '')], weight=3),
        20: dict(notes=['Segmentation: memory as a collection of variable-size segments (main, stack, symbol table…); logical address = <segment, offset>.']),
        23: dict(notes=['Segment table has base and limit; offset d must be < limit, else trap. Physical = base + d.']),
        25: dict(notes=['Segment-table exercise: check d < limit first, then add base.'],
                 exam=[short('Segment 0 has base 219, limit 600. Translate (0, 430) and (0, 700).', '(0, 430): 430 < 600 → physical 219 + 430 = 649. (0, 700): 700 ≥ 600 → addressing error (trap).')], weight=3),
        27: dict(notes=['Paging: physical memory split into fixed-size frames, logical memory into pages of the same size; a page table maps page → frame.']),
        28: dict(notes=['Logical address = page number p (high m − n bits) + offset d (low n bits) for page size 2ⁿ and logical space 2ᵐ.'],
                 exam=[mcq('With 4 KB pages, how many bits are the page offset?', ['12', '4', '10', '32'], 0, '2¹² = 4096.')], weight=3),
        32: dict(notes=['Exercise: logical space 256 pages × 4 KB = 2²⁰ → 20-bit logical address (8-bit page number + 12-bit offset).'],
                 exam=[mcq('256 pages of 4 KB each need a logical address of:', ['20 bits', '12 bits', '8 bits', '32 bits'], 0, '8 + 12.')], weight=3),
        35: dict(notes=['Page table in memory (PTBR, PTLR) means two memory accesses per reference; the TLB (associative cache) fixes this.']),
        38: dict(notes=['EAT = h·(TLB + memory) + (1 − h)·(TLB + 2·memory), with h the hit ratio.'],
                 exam=[mcq('TLB 20 ns, memory 100 ns, hit ratio 80%. EAT =', ['140 ns', '120 ns', '220 ns', '100 ns'], 0, '0.8·120 + 0.2·220.')], weight=3),
        41: dict(notes=['Protection: a valid–invalid bit per page-table entry; also read/write/execute bits.']),
        43: dict(notes=['Shared pages: one copy of read-only (reentrant) code mapped into several processes.']),
    }


class virtual_memory:
    AUTO_SLIDES = True
    DECK = deck('d08', 'Virtual Memory', 'Chapter 9',
                'Virtual memory larger than physical memory, demand paging and the valid–invalid bit, page faults and '
                'their handling, demand-paging performance, page replacement (FIFO and Belady’s anomaly, optimal, '
                'LRU) and thrashing.')
    REF = 'Practice string: 7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1 with 3 frames → FIFO 15 faults, OPT 9, LRU 12.'
    ANN = {
        4: dict(notes=['Virtual memory separates logical memory from physical memory: only part of a program needs to be in memory.']),
        7: dict(notes=['Demand paging: load a page only when it is needed (lazy swapper / pager).']),
        9: dict(notes=['Valid–invalid bit: v = in memory, i = not in memory (or not legal).']),
        11: dict(notes=['Referencing an invalid page → page fault trap to the OS.']),
        12: dict(notes=['Handling: trap → check the reference → find a free frame → read the page from disk → update the table, set v → restart the instruction.'],
                 exam=[mcq('After the page is loaded, the OS:', ['Restarts the faulting instruction', 'Terminates the process', 'Skips the instruction', 'Reboots'], 0, '')], weight=3),
        14: dict(notes=['EAT = (1 − p)·memory access + p·page-fault time. Even a tiny p hurts because a fault costs milliseconds.'],
                 exam=[mcq('Memory 200 ns, fault service 8 ms, p = 0.001. EAT ≈', ['8.2 µs', '200 ns', '8 ms', '1 µs'], 0, '0.999·200 + 0.001·8,000,000 ≈ 8,200 ns.')], weight=3),
        16: dict(notes=['Page replacement: if no free frame, pick a victim; use a dirty (modify) bit so only modified pages are written back.']),
        20: dict(notes=['Goal: lowest page-fault rate. Evaluate on a reference string.'], tips=[tip(REF)]),
        22: dict(notes=['FIFO: replace the oldest page.']),
        24: dict(notes=['Belady’s anomaly: with FIFO, MORE frames can cause MORE page faults.'],
                 exam=[mcq('Belady’s anomaly occurs with:', ['FIFO', 'LRU', 'Optimal', 'All stack algorithms'], 0, '')], weight=3),
        25: dict(notes=['Optimal (OPT/MIN): replace the page not used for the longest time in the future. Lowest fault rate but needs the future: used as a benchmark.'],
                 exam=[tf('The optimal page-replacement algorithm can be implemented in a real OS.', False, 'It needs future knowledge.')], weight=3),
        27: dict(notes=['LRU: replace the page not used for the longest time in the past. Implemented with counters or a stack; no Belady’s anomaly.'],
                 exam=[short('Reference string 1 2 3 4 1 2 5 1 2 3 4 5 with 3 frames. Count FIFO page faults.', '9 faults (and 10 with 4 frames: Belady’s anomaly).')], weight=3),
        29: dict(notes=['Thrashing: the process spends more time paging than executing because it has too few frames; CPU utilization drops.'],
                 exam=[mcq('Thrashing is when a process:', ['Spends more time paging than executing', 'Has too many frames', 'Uses only the TLB', 'Never page-faults'], 0, '')], weight=3),
    }


class fs_interface:
    AUTO_SLIDES = True
    DECK = deck('d09', 'File-System Interface', 'Chapter 11',
                'The file concept and attributes, file operations and the open-file table, file types and structure, '
                'sequential, direct and indexed access, directory structures (single-level, two-level, tree, acyclic '
                'and general graph) and protection with access lists.')
    ANN = {
        5: dict(notes=['Attributes: name, identifier, type, location, size, protection, time/date/user.']),
        7: dict(notes=['Operations: create, write, read, reposition (seek), delete, truncate; open() and close().']),
        8: dict(notes=['Open-file table plus per-file data: file pointer, open count, disk location, access rights.']),
        11: dict(notes=['Sequential access: read next / write next (like a tape). Direct (relative) access: read block n in any order.'],
                 exam=[mcq('Reading block n of a file without reading earlier blocks is:', ['Direct access', 'Sequential access', 'Indexed directory', 'Linked allocation'], 0, '')], weight=3),
        13: dict(notes=['Index access: an index of pointers to blocks; large files use a multi-level index.']),
        19: dict(notes=['Single-level directory: all files in one directory; naming and grouping problems.']),
        20: dict(notes=['Two-level: a separate directory per user; same file name for different users; no grouping.']),
        21: dict(notes=['Tree-structured: absolute vs. relative path names, current directory, efficient searching and grouping.'],
                 exam=[mcq('A path name that starts at the root is:', ['Absolute', 'Relative', 'Symbolic', 'Indexed'], 0, '')], weight=2),
        24: dict(notes=['Acyclic graph: shared subdirectories and files (links). Problems: aliasing, dangling pointers on deletion.']),
        26: dict(notes=['General graph allows cycles; needs garbage collection or a cycle check when adding links.']),
        28: dict(notes=['Protection by type of access: read, write, execute, append, delete, list.']),
        29: dict(notes=['UNIX: owner, group, public, each with r w x bits (e.g. 761).'],
                 exam=[mcq('UNIX mode 754 gives the group:', ['Read and execute', 'Read, write, execute', 'Read only', 'Write and execute'], 0, '5 = r-x.')], weight=3),
    }


class fs_impl:
    AUTO_SLIDES = True
    DECK = deck('d10', 'File-System Implementation', 'Chapter 12',
                'On-disk and in-memory file-system structures, the allocation methods (contiguous, linked, FAT, '
                'indexed and the UNIX combined scheme), and free-space management with bit vectors, linked lists, '
                'grouping and counting.')
    ANN = {
        5: dict(notes=['On disk: boot control block, volume control block (superblock), directory structure, per-file FCB (inode).']),
        7: dict(notes=['In memory: mount table, directory cache, system-wide and per-process open-file tables.']),
        10: dict(notes=['Contiguous: each file occupies consecutive blocks (start, length). Fast sequential and direct access; external fragmentation, hard to grow.'],
                 exam=[mcq('Which allocation method suffers from external fragmentation?', ['Contiguous', 'Linked', 'Indexed', 'FAT'], 0, '')], weight=3),
        14: dict(notes=['Linked: each block points to the next. No external fragmentation, but direct access is slow and a lost pointer breaks the chain.'],
                 exam=[tf('Linked allocation supports efficient direct access.', False, 'You must follow the chain from the start.')], weight=3),
        20: dict(notes=['FAT: the next-block pointers live in a table at the start of the volume (cached), so direct access is faster.']),
        21: dict(notes=['Indexed: each file has an index block of pointers. Direct access without external fragmentation; costs the index block.'], weight=3),
        24: dict(notes=['UNIX inode: 12 direct pointers + single, double and triple indirect blocks.'],
                 exam=[short('4 KB blocks and 4-byte pointers. How much data can one single-indirect block address?', '4096 / 4 = 1024 pointers × 4 KB = 4 MB.')], weight=3),
        26: dict(notes=['Bit vector: one bit per block (1 = free in the slides). Easy to find contiguous space; the map takes disk-size / block-size bits.'],
                 exam=[mcq('A 1 TB disk with 4 KB blocks needs a bit map of:', ['32 MB', '4 MB', '256 MB', '1 GB'], 0, '2⁴⁰/2¹² = 2²⁸ bits = 2²⁵ bytes.')], weight=3),
        31: dict(notes=['Linked free list: each free block points to the next; no wasted space but slow to traverse.']),
        33: dict(notes=['Grouping: the first free block stores the addresses of n free blocks.']),
        35: dict(notes=['Counting: store (first free block, count of contiguous free blocks).']),
    }


DECKS_HERE = [intro, services, processes, threads, scheduling, sync, memory, virtual_memory, fs_interface, fs_impl]

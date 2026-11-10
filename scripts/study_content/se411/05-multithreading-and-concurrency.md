@head Chapter 5
@title Multithreading and Concurrency
@sources chapter-5-multithreading-and-concurrency
@count 79
@tldr A thread is an independent path of execution; several threads let a program do many things at once, but threads sharing data must take turns (synchronized, locks) or the data gets corrupted.
@why Concurrency bugs are invisible until they bite: the 100-pennies account that ends with less than 100 cents is the slide example every exam reuses. Expect questions on Runnable vs Thread, start() vs run(), thread states, thread pools, race conditions, synchronized, ReentrantLock, deadlock and resource ordering.
@connect Runnable is a functional interface (Chapters 2 and 4), so a task can be a lambda. Chapter 4's immutable objects are thread-safe for free. Chapter 6's web servers handle every request on its own thread.
@goals

- Define a thread and contrast threads with processes
- Distinguish concurrency from parallelism
- Create threads with Runnable or by extending Thread
- Explain start, sleep, yield, join, interrupt, isAlive and priorities
- Use ExecutorService thread pools
- Explain race conditions and fix them with synchronized or ReentrantLock
- Explain deadlock and prevent it with resource ordering
- Use synchronized collections and the Fork/Join framework
  @vocab
  Thread | The smallest unit of execution: an independent path inside a process.
  Process | A running program with its own memory; it contains one or more threads.
  Task | The work to do: a Runnable's run() method.
  Race condition | The result depends on which thread happens to run first.
  Critical region | Code that only one thread at a time may execute.
  Thread-safe | Works correctly when used by many threads at once.
  Deadlock | Threads each wait forever for a lock another one holds.
  Starvation | A thread waits for a lock but never gets it.
  @map
  4-10 | Threads, processes, multithreading | MEMORIZE | Concurrency vs parallelism
  11-18 | Tasks and threads, Runnable examples | WRITE | start() vs run()
  19-35 | Thread class methods and states | MEMORIZE | Five states, sleep, yield, join
  36-39 | Thread pools | WRITE | ExecutorService
  40-54 | Race conditions and synchronized | WRITE | 100 pennies
  55-62 | Locks, fairness, conditions | MEMORIZE | lock / try / finally unlock
  63-66 | Deadlock | MEMORIZE | Resource ordering
  67-70 | Synchronized collections | MEMORIZE | Fail-fast iterators
  71-78 | Fork/Join | SKIM | Parallel merge sort

## Threads, processes and multithreading | Slides 4-10 | must

A **thread** is the **smallest unit of execution** in a program, with its own path of execution. Threads are independent: an exception in one shouldn't affect the others. They run **inside a process**, and the OS runs many processes at once.

|                | Process           | Thread                               |
| -------------- | ----------------- | ------------------------------------ |
| What           | A running program | A path of execution inside a process |
| Memory         | Its own           | **Shares** the process's memory      |
| Cost to create | Heavy             | Light                                |

**Multithreading** means running several threads concurrently. It's used for multimedia, video games, web servers and application servers. It turns messy asynchronous code into simple straight-line code and is the easiest way to use multiple processors.

|            | Concurrency (multithreading)                    | Parallelism (multiprocessing)                        |
| ---------- | ----------------------------------------------- | ---------------------------------------------------- |
| Hardware   | Threads **share one CPU**, taking turns quickly | Threads run on **multiple CPUs** at the same instant |
| Feels like | Juggling                                        | Several people each holding one ball                 |

::analogy A kitchen
A process is a restaurant kitchen with its own pantry (memory). Threads are the cooks: they share the pantry, which is fast and convenient, and also why two cooks can grab the last egg at the same time.
::
::key

- A thread is the smallest unit of execution, inside a process
- Threads in a process share its memory
- Concurrency: threads share one CPU; parallelism: multiple CPUs
- Used in games, media, and web and application servers
  ::

## Creating tasks and threads | Slides 11-18, 27-29 | must

Separate **what to do** (the task: a `Runnable` with `run()`) from **who does it** (the `Thread`).

::code java
class TaskClass implements Runnable {
@Override
public void run() {
for (int i = 1; i <= 5; i++)
System.out.println(Thread.currentThread().getName() + " : " + i);
}
}

Thread thread = new Thread(new TaskClass(), "Worker");
thread.start(); // new thread runs run()
System.out.println("Main thread continues...");
::

The output order **isn't fixed**: "Main thread continues..." may print before, between or after the Worker's lines, because both threads run concurrently.

::trap start() vs run()
`thread.start()` creates a **new thread**, and the JVM calls `run()` on it. Calling `task.run()` directly is just a normal method call on the **current** thread: nothing runs in parallel.
::

| Approach                | Plus                                                                 | Minus                                                                          |
| ----------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| **implements Runnable** | Class can still extend another class; task kept separate from thread | Client wraps it: `new Thread(task)`                                            |
| **extends Thread**      | Cleaner client code: `new MyThread().start()`                        | Uses up your single superclass; "pollutes" the class with all Thread's methods |

Since Runnable has one abstract method, a lambda works too: `new Thread(() -> System.out.println("hi")).start();`.

::example The AdditionTask frequency example (slides 15-17)
Each task loops forever, increments a counter, then sleeps `1000 / frequency` ms. Frequency 4 → every 250 ms; frequency 10 → every 100 ms. Two threads with different frequencies interleave their output.
::
::key

- Runnable = the task (what); Thread = the worker (who)
- start() makes a new thread that calls run()
- Calling run() directly doesn't create a thread
- Prefer Runnable: you keep the superclass free
- Thread output order is unpredictable
  ::

## Thread methods and states | Slides 19-35 | must

::graph Thread states | directed
n new 70 110 New
n ready 230 110 Ready *
n run 410 110 Running *
n blk 320 230 Blocked ~
n fin 560 110 Finished
e new ready start()
e ready run scheduled
e run ready yield / time up
e run blk sleep, join, wait
e blk ready wakes up
e run fin run() ends
::

| Method                      | Does                                                                                        |
| --------------------------- | ------------------------------------------------------------------------------------------- |
| `start()`                   | Begins execution; JVM calls run() on the new thread                                         |
| `isAlive()`                 | true if Ready, Running or Blocked; false if New or Finished                                 |
| `setPriority(int)`          | 1 (MIN) to 10 (MAX); default **NORM = 5**                                                   |
| `Thread.sleep(ms)` (static) | Pauses the current thread; may throw **InterruptedException** (checked)                     |
| `Thread.yield()` (static)   | Temporarily gives the CPU to other threads                                                  |
| `join()`                    | Waits for **another** thread to finish                                                      |
| `interrupt()`               | Ready/Running: sets the interrupted flag. Blocked: wakes it and throws InterruptedException |
| `isInterrupted()`           | Tests the flag                                                                              |

::mnemonic New Ready Runners Become Finishers
**N**ew, **R**eady, **R**unning, **B**locked, **F**inished.
::
::trap Priority is only a hint
`setPriority` is implemented natively and depends on the OS; if the OS ignores priorities, it does nothing. Never rely on priority for correctness.
::
::check A thread is sleeping. What does isAlive() return?
true. Sleeping means Blocked, and only New and Finished threads give false.
::
::key

- Five states: New, Ready, Running, Blocked, Finished
- isAlive is false only for New and Finished
- Priorities 1 to 10, default 5, and only a hint
- sleep pauses; yield gives way; join waits for another thread
- sleep throws the checked InterruptedException
  ::

## Thread pools | Slides 36-39 | must

Creating a new thread for every task wastes time and can hurt throughput. A **thread pool** reuses a fixed set of threads. Java 5 added the **Executor** interface (run tasks) and its subinterface **ExecutorService** (manage them). Create one with the static **Executors** factory methods.

::code java
ExecutorService executor = Executors.newFixedThreadPool(3);
for (int i = 0; i < 20; i++)
executor.execute(new CountingTask("Task_" + i, 20, 20));
executor.shutdown(); // no new tasks; existing ones finish
::

All 20 tasks run, but **only 3 at a time**.

| Factory                 | Pool                                           |
| ----------------------- | ---------------------------------------------- |
| `newFixedThreadPool(n)` | Exactly n threads; extra tasks wait in a queue |
| `newCachedThreadPool()` | Creates threads as needed and reuses idle ones |

`isTerminated()` returns true once every task has finished after shutdown.

::analogy A taxi rank
Hiring and training a new driver per customer is slow. A pool is a rank with three taxis: customers queue, and each taxi takes the next customer when it returns.
::
::key

- A pool reuses threads instead of creating one per task
- ExecutorService manages tasks; Executors creates pools
- Fixed pool: n threads; cached pool: grows as needed
- shutdown stops new tasks; isTerminated checks they've all finished
  ::

## Race conditions and synchronized | Slides 40-54 | must

**100 threads each add a penny to an empty account.** Expected balance: 100. Actual: often far less.

::code java
public void deposit(int amount) {
int newBalance = balance + amount; // read
Thread.sleep(1); // delay to magnify the problem
balance = newBalance; // write
}
::

| Step | balance | Task 1             | Task 2             |
| ---- | ------- | ------------------ | ------------------ |
| 1    | 0       | newBalance = 0 + 1 |                    |
| 2    | 0       |                    | newBalance = 0 + 1 |
| 3    | 1       | balance = 1        |                    |
| 4    | **1**   |                    | balance = 1        |

Two deposits, but the balance is 1: Task 2 **overwrote** Task 1's work. This is a **race condition**, and a class without this problem is **thread-safe**.

::analogy Two people editing a shared spreadsheet offline
Both open it showing 0, both type 1, both save. The last save wins, and one deposit vanishes.
::

The fix: stop more than one thread entering the **critical region** at once.

::code java
public synchronized void deposit(double amount) { ... }

// Same thing as a synchronized block:
public void deposit(double amount) {
synchronized (this) { ... }
}
::

| synchronized on               | Lock taken on                  |
| ----------------------------- | ------------------------------ |
| An instance method            | **The object** (`this`)        |
| A static method               | **The class**                  |
| A block `synchronized (expr)` | The object `expr` evaluates to |

A thread acquires the lock, runs the code and releases the lock. Any other thread calling it is **blocked** until then. A synchronized **block** can protect just the critical lines instead of a whole method.

::mnemonic RMW: Read, Modify, Write
A race happens when another thread sneaks in between your **r**ead and your **w**rite. Make the whole read-modify-write one locked step.
::
::key

- A race condition: the result depends on thread timing
- Read-modify-write on shared data must be protected
- synchronized makes a method or block one-thread-at-a-time
- Instance method locks the object; static method locks the class
- Any synchronized method can be rewritten as synchronized (this)
  ::

## Explicit locks and conditions | Slides 55-62 | know

Java 5 added explicit locks: the **Lock** interface and the **ReentrantLock** class in `java.util.concurrent.locks`, giving more control than synchronized.

::code java
private Lock lock = new ReentrantLock();

public void deposit(int amount) {
lock.lock(); // acquire
try {
balance = balance + amount;
} finally {
lock.unlock(); // ALWAYS release
}
}
::

|                               | synchronized | ReentrantLock                                                      |
| ----------------------------- | ------------ | ------------------------------------------------------------------ |
| Acquire / release             | Automatic    | **Explicit** lock() / unlock()                                     |
| Fairness option               | No           | `new ReentrantLock(true)`                                          |
| Conditions (wait for a state) | No           | `lock.newCondition()`                                              |
| Reentrant                     | Yes          | Yes: a thread holding it can lock it again without blocking itself |

**Fairness**: `true` gives the lock to the **longest-waiting** thread, which prevents **starvation** but lowers overall performance. `false` (default) grants it in no particular order.

**Conditions** (slide 62, a bounded buffer): `put()` waits with `notFull.await()` while the buffer is full; `take()` waits with `notEmpty.await()` while it's empty. Each side signals the other after changing the buffer.

::trap Forgetting unlock
If an exception happens between lock() and unlock() without a finally, the lock is never released and every other thread waits forever. Always unlock in finally.
::
::key

- ReentrantLock: explicit lock() and unlock()
- Always unlock in a finally block
- Fair locks prevent starvation but are slower
- Conditions let threads wait until a state changes (await)
  ::

## Deadlock | Slides 63-66 | must

Thread 1 holds the lock on **object1** and waits for **object2**. Thread 2 holds **object2** and waits for **object1**. Each waits for the other forever: **deadlock**.

::graph Deadlock: a circular wait | directed
n t1 100 70 Thread 1
n o2 400 70 object2
n t2 400 210 Thread 2
n o1 100 210 object1
e t1 o2 waits for ~
e o2 t2 held by
e t2 o1 waits for ~
e o1 t1 held by
::

**Prevention: resource ordering.** Give every lock a global order (Lock A < Lock B < Lock C) and make **every** thread acquire locks in that order. Then Thread 2 must also ask for object1 first; it waits, Thread 1 gets both, finishes and releases them. No cycle can form, so the **circular wait** condition, one of the four required for deadlock, is gone.

::analogy Two people, two chopsticks
If each person grabs the chopstick on their left and waits for the right one, nobody eats. The rule "always pick up the lower-numbered chopstick first" breaks the circle.
::
::key

- Deadlock: each thread holds one lock and waits for another's
- Resource ordering: acquire locks in one global order
- It removes circular wait, so deadlock is impossible
  ::

## Thread-safe collections and Fork/Join | Slides 67-78 | know

The Java Collections Framework classes (ArrayList, HashSet...) are **not thread-safe**. Wrap them:

::code java
List<String> syncList = Collections.synchronizedList(new ArrayList<>());
syncList.add("Apple");
synchronized (syncList) { // lock while iterating
for (String fruit : syncList) System.out.println(fruit);
}
::

The `Collections` class has six such **synchronization wrappers**. **Vector, Stack and Hashtable** are old classes whose methods are already synchronized.

::trap Iterators are fail-fast
If another thread modifies the collection while you iterate, the iterator throws **ConcurrentModificationException** (a RuntimeException). That's why you lock the collection during traversal.
::

**Fork/Join** (Java 7) splits a big problem into independent subtasks that run in parallel on multiple cores. Tasks extend **ForkJoinTask**, usually through `RecursiveAction` (no result) or `RecursiveTask` (returns a result), and run in a **ForkJoinPool**, an ExecutorService that manages worker threads. In the parallel merge sort, `compute()` sorts directly below a **threshold** of 500 elements; otherwise it splits the array in half, runs both halves in parallel and merges them.

::key

- JCF collections aren't thread-safe; use Collections.synchronizedXxx
- Lock the collection while iterating, since iterators are fail-fast
- Vector, Stack and Hashtable are already synchronized
- Fork/Join splits work into parallel subtasks in a ForkJoinPool
- Below a threshold, solve directly instead of splitting
  ::
  @cheat

### Basics

- Thread: smallest unit, shares process memory
- Concurrency: one CPU; parallelism: many
- Runnable = task; Thread = worker
- start() → new thread; run() = normal call

### Methods

- States: New, Ready, Running, Blocked, Finished
- isAlive false only New / Finished
- Priority 1-10, default 5, a hint
- sleep, yield, join, interrupt

### Pools

- Executors.newFixedThreadPool(n)
- newCachedThreadPool()
- execute, shutdown, isTerminated

### Races

- Read-modify-write interleaving
- synchronized method: lock on object
- static synchronized: lock on class
- synchronized (this) { }

### Locks

- lock(); try { } finally { unlock(); }
- Fair = longest waiter, no starvation
- Conditions: await / signal

### Deadlock and more

- Circular wait on locks
- Fix: resource ordering
- Collections.synchronizedList
- Fail-fast → ConcurrentModificationException
- Fork/Join: RecursiveAction, ForkJoinPool
  @mcq 4
  A thread is best defined as:

* The smallest unit of execution within a program

- A running program with its own memory
- A type of exception
- A Maven plugin

> Slide 4.
> @mcq 10
> Multiple threads sharing a single CPU is called:

- Concurrency

* Parallelism
* Deadlock
* Synchronization

> Slide 10.
> @mcq 13
> What happens when you call task.run() directly instead of thread.start()?

- run() executes on the current thread, with no new thread

* A new thread is created
* A compile error
* The task runs twice in parallel

> start() is what creates the thread.
> @mcq 29
> A downside of extending Thread instead of implementing Runnable is:

- The class can't extend any other class

* The thread can't be started
* run() can't be overridden
* It can't print output

> Java allows one superclass.
> @mcq 21
> isAlive() returns false when the thread is:

- New or Finished

* Running
* Blocked
* Ready

> Slide 21.
> @mcq 24
> The default thread priority is:

- 5 (NORM_PRIORITY)

* 1
* 10
* 0

> Slide 24.
> @mcq 39
> With newFixedThreadPool(3) and 20 submitted tasks:

- All 20 run, at most 3 at a time

* Only 3 tasks run
* 20 threads are created
* It throws an exception

> Slide 39.
> @mcq 46
> 100 threads each add a penny without synchronization, and the balance ends below 100. This is:

- A race condition

* A deadlock
* Starvation
* A fail-fast iterator

> Slide 46.
> @mcq 48
> A synchronized static method acquires a lock on:

- The class

* The object
* Every object of the class
* No lock

> Slide 48.
> @mcq 58
> When using ReentrantLock, unlock() should be called:

- In a finally block

* Before lock()
* Only if an exception occurs
* Never; it's automatic

> Always release the lock.
> @mcq 59
> A fair ReentrantLock gives the lock to:

- The longest-waiting thread

* The highest-priority thread
* A random thread
* The newest thread

> Prevents starvation.
> @mcq 65
> Resource ordering prevents deadlock by:

- Making every thread acquire locks in the same global order

* Giving threads higher priority
* Removing all locks
* Using more threads

> It breaks circular wait.
> @mcq 70
> Modifying a synchronized collection while another thread iterates it throws:

- ConcurrentModificationException

* InterruptedException
* NullPointerException
* IOException

> Iterators are fail-fast.
> @mcq 69
> Which class's methods are already synchronized?

- Vector

* ArrayList
* LinkedList
* HashSet

> Vector, Stack and Hashtable.
> @short 46
> Explain how 100 deposit threads can leave an account with less than 100, and how to fix it.
> ~ read, write, overwrite, race condition, synchronized, lock
> Two threads read the same balance, both add 1, and the second write overwrites the first, so a deposit is lost. This race condition is fixed by making deposit synchronized, or by using a ReentrantLock, so only one thread runs the read-modify-write at a time.
> @short 64
> Describe a deadlock between two threads and how resource ordering prevents it.
> ~ object1, object2, waits, circular, order
> Thread 1 holds object1 and waits for object2 while Thread 2 holds object2 and waits for object1, so neither can continue. With resource ordering, both threads must lock object1 before object2, so Thread 2 waits for object1 and no circular wait can form.
> @short 27
> Compare implementing Runnable with extending Thread.
> ~ superclass, separate, task, client code, pollute
> Implementing Runnable keeps the task separate from the thread and leaves the class free to extend another class, though the client must wrap it in a Thread. Extending Thread gives cleaner client code but uses up the single superclass and adds all of Thread's methods to the class.

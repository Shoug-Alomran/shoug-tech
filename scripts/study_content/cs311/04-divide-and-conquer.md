@head Lecture 4
@title Divide and Conquer
@sources lecture-4-divide-and-conquer
@count 34
@tldr Split a problem into smaller copies of itself, solve those, and stitch the answers together; merge sort and quick sort are the two classic examples, and they put their hard work in opposite places.
@why This is the first design strategy of the course, and the template reappears in many other algorithms. Tracing merge sort and partitioning for quick sort by hand are common exam questions, and so is explaining why quick sort can degrade to O(n²).
@connect Lecture 3's recurrences solve the running times here directly. Dynamic programming later handles the case in which the subproblems overlap, which divide and conquer handles badly.
@goals
- Name the three steps of divide and conquer
- Trace merge sort on an array
- Trace quick sort's partition step by step
- Derive the best and worst cases of quick sort
- Explain median-of-three pivot selection
@vocab
Partition | Rearranging an array around a pivot, smaller values before it and larger after.
Pivot | The element chosen to split the array.
Merge | Combining two sorted lists into one sorted list.
In place | Using almost no extra memory.
@map
2-4 | The strategy | MEMORIZE | Divide, Conquer, Combine
5-15 | Merge sort example | WRITE | Trace one by hand
16-20 | Merge pseudocode and analysis | WRITE | The recurrence
21-27 | Quick sort and partitioning | WRITE | Trace the partition
28-31 | Best and worst case | MEMORIZE | When O(n²) happens
32-34 | Better pivots, exercise | WRITE | Median-of-three

## The strategy | Slides 2-4 | must
Every divide-and-conquer algorithm has three moves.

::steps Divide, Conquer, Combine
**Divide** the problem into smaller subproblems of the same kind.
**Conquer** them by solving each one recursively. If one is small enough, solve it directly.
**Combine** the solutions into a solution of the original problem.
::
::analogy Marking a pile of 1,000 exams
You hand half to each of two assistants, who each split theirs again, until everyone has a tiny pile. Everyone marks their pile and passes the sorted results back up, combining as they go.
::
::mnemonic DCC: the Divide, Conquer, Combine routine
Think of the DC Comics hero sorting out a city: **D**ivide it up, **C**onquer each part, **C**ombine the results.
::
::key
- Divide into similar, smaller subproblems
- Conquer recursively, solving small cases directly
- Combine the sub-answers
- Analysis uses recurrence equations
::

## Merge sort: easy split, clever combine | Slides 5-20 | must
- **Divide:** cut the array into two halves. Trivial.
- **Conquer:** sort each half with merge sort.
- **Combine:** merge the two sorted halves. **All the real work is here.**

::graph Merge sort on 8 3 2 9 7 1 5 4: split all the way down, then merge back up | directed
n a 240 0 8 3 2 9 7 1 5 4
n b 110 75 8 3 2 9
n c 370 75 7 1 5 4
n d 40 150 8 3
n e 180 150 2 9
n f 300 150 7 1
n g 440 150 5 4
n h 40 225 3 8
n i 180 225 2 9
n j 300 225 1 7
n k 440 225 4 5
n l 110 300 2 3 8 9
n m 370 300 1 4 5 7
n o 240 375 1 2 3 4 5 7 8 9 *
e a b
e a c
e b d
e b e
e c f
e c g
e d h
e e i
e f j
e g k
e h l
e i l
e j m
e k m
e l o
e m o
::

### How merging works
Keep a finger on the front of each sorted list. Repeatedly copy the smaller front value to the output, and advance that finger. When one list runs out, copy the rest of the other.

::steps Merge [2, 3, 8, 9] with [1, 4, 5, 7]
Compare 2 and 1: take **1**.
Compare 2 and 4: take **2**.
Compare 3 and 4: take **3**.
Compare 8 and 4: take **4**.
Compare 8 and 5: take **5**.
Compare 8 and 7: take **7**.
The second list is empty. Copy the rest: **8, 9**.
::

Merging touches each element once: **Θ(p + q) = Θ(n)**.

### Analysis
| Step | Cost |
|---|---|
| Divide (find the middle) | Θ(1) |
| Conquer (two halves) | 2T(n/2) |
| Combine (merge) | Θ(n) |

::formula Recurrence
T(n) = 2T(n/2) + Θ(n) → T(n) = Θ(n log n)
::

From Lecture 3, this is the tie case of the Master theorem. There are log n levels and each does n work.

::tip Merge sort is reliable
Its O(n log n) holds for **every** input: the split is always half and half. The cost is that merging needs extra memory for the output array.
::
::key
- Merge sort splits in half and does its real work while merging
- Merging two sorted lists takes Θ(n) time
- T(n) = 2T(n/2) + Θ(n), which is Θ(n log n)
- The running time is the same for best, worst and average
::

## Quick sort: clever split, easy combine | Slides 21-27 | must
Quick sort reverses the idea. **All the real work is in dividing**, and combining is free.

- **Divide:** pick a pivot and partition into smaller and larger values.
- **Conquer:** quick sort each side.
- **Combine:** nothing, since it's already in order.

::mnemonic Merge Mends later, Quick Quarrels first
**Merge** sort splits lazily and **mends** everything at the end. **Quick** sort **quarrels** up front, forcing each element to the correct side.
::
::steps Partition routine (slide 25), first element as pivot
Choose the first value as pivot.
From the left, find the first element ≥ pivot.
From the right, find the first element < pivot.
Swap them.
Continue from where you left off until the two searches cross.
Swap the pivot with the last element of the smaller part. The pivot is now in its **final position**.
::
::example The exercise on slide 34: sort 7 2 9 10 5 4
**Pivot 7.** From left: 9. From right: 4. Swap: 7 2 **4** 10 5 **9**.

Continue. From left: 10. From right: 5. Swap: 7 2 4 **5** **10** 9.

The searches have crossed. Swap pivot 7 with 5: **5 2 4** [7] **10 9**. Seven is home.

**Left part 5 2 4:** pivot 5 is the largest, so swap it with the last: 4 2 [5]. Then 4 2 becomes 2 [4].

**Right part 10 9:** pivot 10, swap to get 9 [10].

Result: **2 4 5 7 9 10**.
::
::key
- Quick sort does its work when partitioning
- Combine does nothing
- After partitioning, the pivot is in its final position
- Partition scans from both ends and swaps out-of-place pairs
::

## Best and worst cases, and better pivots | Slides 28-33 | must
Everything depends on how balanced the partition is.

| Case | Partition | Recurrence | Result |
|---|---|---|---|
| **Best** | Pivot lands in the middle | T(n) = 2T(n/2) + bn | **O(n log n)** |
| **Worst** | Pivot is always the smallest or largest | T(n) = T(n−1) + cn | **O(n²)** |

::steps Why the worst case is quadratic
Partitioning n elements costs about n.
One side is empty, and the other has n − 1 elements.
So the sum is n + (n−1) + (n−2) + ... + 2.
That equals about n²/2, which is **O(n²)**.
::

With the first element as pivot, the worst case occurs on an array that's **already sorted, or sorted in reverse**, which is the irony of the algorithm.

::analogy Picking team captains badly
If you split a class by asking "who's shorter than the shortest person?", nobody is. You've made one group of nobody and one group of everyone else, and you've learned almost nothing.
::

**Better pivot: median-of-three.** The true median would be perfect but it's hard to find quickly, so approximate it using the median of the left, centre and right elements.

::example Slide 33
S = 0, 1, 2, ..., 9. Left is 0, right is 9, centre index is (0 + 9)/2 = 4, so the centre value is 4. The median of 0, 9 and 4 is **4**. A sorted array no longer triggers the worst case.
::

| | Merge sort | Quick sort |
|---|---|---|
| Worst case | O(n log n) | O(n²) |
| Average | O(n log n) | O(n log n) |
| Work happens in | Combine | Divide |
| Extra memory | Needs an array | In place |
| In practice | Reliable | Fastest known in practice (slide 21) |

::trap Picking the last element doesn't help
Slide 32 says it plainly: a sorted array is just as bad with the last element as with the first. Only a pivot that tends to fall near the middle fixes the problem.
::
::check Which recurrence describes quick sort if each partition splits 9 to 1?
T(n) = T(9n/10) + T(n/10) + n, which is still **O(n log n)**. Each level still costs at most n, and there are about log n levels. Any constant fraction is fine: the trouble only comes when one side is empty.
::
::key
- Best case: balanced partition, O(n log n)
- Worst case: pivot always extreme, O(n²)
- First-element pivot gives the worst case on sorted or reverse-sorted arrays
- Median-of-three uses the left, centre and right elements
- Merge sort is always O(n log n), while quick sort is fast in practice
::
@cheat
### Divide and conquer
- Divide into smaller subproblems
- Conquer recursively
- Combine the answers
### Merge sort
- Split in half (trivial)
- Work is in merge: Θ(n)
- T(n) = 2T(n/2) + Θ(n)
- Θ(n log n), every case
- Needs extra array
### Quick sort
- Pivot, partition, recurse
- Combine does nothing
- Best: T(n) = 2T(n/2) + n
- Worst: T(n) = T(n−1) + n = O(n²)
- Worst on sorted input with first pivot
### Partition
- From left: first ≥ pivot
- From right: first < pivot
- Swap, continue until they cross
- Swap pivot into place
### Median-of-three
- Median of left, centre and right
- Fixes the sorted-input worst case
@mcq 18
What is the recurrence for merge sort?
+ T(n) = 2T(n/2) + Θ(n)
- T(n) = T(n/2) + Θ(n)
- T(n) = 2T(n/2) + Θ(1)
- T(n) = T(n−1) + Θ(n)
> Two halves are sorted, and merging costs linear time.
@mcq 30
Quick sort's worst-case recurrence is:
+ T(n) = T(n−1) + cn
- T(n) = 2T(n/2) + cn
- T(n) = T(n/2) + c
- T(n) = 2T(n−1) + c
> The partition puts everything on one side, leaving n−1 elements.
@mcq 31
With the first element as the pivot, quick sort is at its worst when the array is:
+ Already sorted or reverse sorted
- Randomly shuffled
- All different values
- Of even length
> Each pivot is then the smallest or largest element.
@mcq 21
Where does quick sort do most of its work?
+ In the partition step
- In the combine step
- In the base case
- In comparing recursion depths
> The combine step does nothing.
@mcq 18
Where does merge sort do most of its work?
+ In the merge step
- In picking the pivot
- In computing the midpoint
- In the base case
> Dividing is constant time. Merging costs Θ(n) per level.
@mcq 33
Median-of-three chooses as pivot the median of:
+ The left, centre and right elements
- Three random elements
- The first three elements
- The three largest elements
> It approximates the true median cheaply.
@mcq 17
Merging sorted lists of sizes p and q takes:
+ Θ(p + q)
- Θ(p × q)
- Θ(log(p + q))
- Θ(max(p, q)²)
> Each element is moved exactly once.
@mcq 6
Merge sort's overall running time is:
+ Θ(n log n) for all inputs
- Θ(n²) in the worst case
- Θ(n) for sorted inputs
- Θ(log n) on average
> Halving is independent of the data, so every input takes the same shape of work.
@mcq 22
After a partition step, the pivot is:
+ In its final sorted position
- At the front of the array
- Still to be placed by combine
- At the end of the array
> Every smaller value is before it and every larger value is after it.
@mcq 32
Why not always use the exact median as pivot?
+ It is hard to find quickly without sorting
- It makes partitioning unstable
- It gives O(n²) behaviour
- It cannot be computed
> Slide 32: the median would be ideal, but it's expensive to calculate.
@short 26
Show the first partition of 5 3 8 4 9 1 with the first element as pivot.
~ pivot, 5, swap, 8, 1, final
> Pivot is 5. From the left, 8 is ≥ 5; from the right, 1 is < 5. Swap to get 5 3 1 4 9 8. The searches cross, so swap the pivot with the last smaller value, 4, giving 4 3 1 5 9 8.
@short 30
Explain why quick sort becomes O(n²) on a sorted array when the first element is the pivot.
~ pivot, smallest, n-1, unbalanced, sum
> Each pivot is the smallest element, so one partition is empty and the other has n−1 elements. The costs add up to n + (n−1) + ... + 2, which is O(n²).
@short 18
Derive the running time of merge sort from its three steps.
~ divide, conquer, combine, 2T(n/2), n log n
> Dividing is Θ(1), conquering is 2T(n/2) and combining is Θ(n). So T(n) = 2T(n/2) + Θ(n), which is Θ(n log n).

@head Chapter 7.1
@title NumPy and Similarity Measures
@sources chapter-7-1-numpy-and-similarity-measures
@count 39
@tldr Turn anything into a list of numbers, and then "how similar are these two things?" becomes simple arithmetic on vectors.
@why Face unlock, song recommendations and search engines all reduce to one question: how close are two vectors? Hand calculations of the dot product, norm and cosine similarity are quick, reliable exam marks, and PCA in the next deck is built on them.
@connect Chapters 2.x handled tables. This chapter moves to the maths under those tables. Chapter 7.2 uses dot products to compress features.
@goals

- Do vector arithmetic in NumPy
- Compute a dot product by hand and explain what its value means
- Normalize a vector using L1 and L2
- Compute cosine similarity and explain why it beats the raw dot product
  @vocab
  Vector | An ordered list of numbers.
  Embedding | A vector that represents an object such as a word or face.
  Dimension | How many numbers the vector holds.
  Norm | A vector's length.
  Magnitude | Another word for the length.
  @map
  3-8 | Why similarity, embeddings | SKIM | Understand objects as vectors
  10-17 | NumPy and vector operations | WRITE | Be able to code these
  19-26 | Dot product | MEMORIZE | Formula, properties and meaning of 0
  28-34 | Norms and normalization | WRITE | Compute L1, L2 and a unit vector
  36-39 | Cosine similarity | MEMORIZE | Compute by hand

## Objects as vectors, and why NumPy | Slides 3-17 | know

A computer can't compare two faces directly, but it can compare two lists of numbers. An **embedding model** converts each object, whether a face, a voice clip or a word, into a vector, so that similar objects land near each other. Then similarity is just geometry.

::analogy Coordinates on a map
Two cities are "similar in location" if their coordinates are close. Embeddings give words and faces coordinates, in hundreds of dimensions instead of two.
::

**NumPy** is Python's library for fast number arrays. On slide 10, summing the same numbers took 0.303 s with a list and 0.010 s with a NumPy array, about **30 times faster**, thanks to its C implementation. Slide 12 gives three reasons to use it: performance, functionality and integration with other libraries.

Arithmetic is element by element:

::code python
a = np.array([2, 4, 6])
b = np.array([1, 0, 1])
a + b # [3, 4, 7]
a * 2 # [4, 8, 12]
::

A scalar in NumPy is a zero-dimensional array: `np.array(5)`.

::key

- Embeddings turn objects into vectors, so similarity becomes vector maths
- NumPy was about 30 times faster than a list on slide 10
- Vector arithmetic works element by element
  ::

## The dot product | Slides 19-26 | must

Multiply matching positions, then add.

::formula Dot product
a · b = a<sub>1</sub>b<sub>1</sub> + a<sub>2</sub>b<sub>2</sub> + ... + a<sub>n</sub>b<sub>n</sub>
::
::steps Compute [2, 3, 4] · [1, 0, −1]
Multiply the first pair: 2 × 1 = 2.
The second: 3 × 0 = 0.
The third: 4 × −1 = −4.
Add: 2 + 0 − 4 = **−2**.
::

In code: `np.dot(a, b)` or `a @ b`.

| Dot product        | Meaning                                         |
| ------------------ | ----------------------------------------------- |
| Large and positive | Pointing in a similar direction                 |
| **0**              | Perpendicular: no similarity under this measure |
| Negative           | Pointing in opposite directions                 |

::example Why the raw dot product can mislead (slides 25-26, 33)
With a 300-dimension embedding: apple · banana = **911**, while apple · lion = **161**. Good, fruit is closer to fruit.

With a 96-dimension model the same pairs give **39** and **35**, nearly equal.

And the vectors have different lengths: norms of 43.4, 31.6 and 55.1. A long vector gets a big dot product with nearly anything, so raw values aren't comparable. The fix is coming next.
::
::key

- Dot product: multiply matching positions, then add
- np.dot and the @ operator give the same result for 1-D arrays
- Zero means perpendicular
- Raw dot products depend on vector lengths, so they aren't directly comparable
  ::

## Norms and normalization | Slides 28-34 | must

**Normalizing** a vector keeps its direction but sets its length to 1. It removes the effect of size so that only direction matters.

| Norm                          | Recipe                | For [3, 4]    | Normalized   |
| ----------------------------- | --------------------- | ------------- | ------------ |
| **L2** (straight-line length) | Square, add, root     | √(9 + 16) = 5 | [0.6, 0.8]   |
| **L1** (sum of sizes)         | Absolute values added | 3 + 4 = 7     | [0.43, 0.57] |

The slide's L1 example: [3, 2] has L1 norm 5, so it normalizes to [0.6, 0.4].

::mnemonic L1 Lines up, L2 Takes the shortcut
Think of a city grid. **L1** is the distance walking along the blocks, adding up each side. **L2** is the straight-line distance a bird would fly.
::
::code python
norm = np.linalg.norm(v) # L2 by default
unit = v / norm if norm != 0 else v
::
::trap The zero vector
A vector of all zeros has length 0, and dividing by zero fails. That is why slide 34 checks for it first.
::
::check Normalize [6, 8] with L2.
Length = √(36 + 64) = 10, so the unit vector is [0.6, 0.8].
::
::key

- Normalizing keeps direction and sets length to 1
- L2 norm = square root of the sum of squares, np.linalg.norm's default
- L1 norm = sum of absolute values
- Check for a zero vector before dividing
  ::

## Cosine similarity | Slides 36-39 | must

Divide the dot product by both lengths, and you have removed length altogether. What remains depends only on the **angle** between the vectors.

::formula Cosine similarity
cos θ = (a · b) / (‖a‖ × ‖b‖)
::

| Value | Meaning                  |
| ----- | ------------------------ |
| 1     | Same direction           |
| 0     | Perpendicular, unrelated |
| −1    | Opposite direction       |

::steps Compute it for a = [3, 4] and b = [4, 3]
Dot product: 3×4 + 4×3 = 24.
‖a‖ = √(9 + 16) = 5 and ‖b‖ = 5.
cos θ = 24 / (5 × 5) = **0.96**. Very similar.
::
::analogy A review written twice
One person writes a 50-word review and another writes 500 words, both praising the same things. Their vector sizes differ wildly, but their _direction_ is the same. Cosine similarity spots that, and a raw dot product does not.
::
::tip The shortcut in slide 38
If both vectors are already normalized, the denominator equals 1, so the cosine is just `np.dot(a, b)`.
::
::trap Cosine similarity is not a distance
High cosine means **more similar**. For a distance, a smaller number means closer. Check which the question is asking for.
::
::key

- Cosine similarity = dot product ÷ product of the two norms
- It depends on the angle only, not the vectors' lengths
- Range is −1 to 1, and 1 means the same direction
- After normalization, cosine similarity equals the dot product
  ::

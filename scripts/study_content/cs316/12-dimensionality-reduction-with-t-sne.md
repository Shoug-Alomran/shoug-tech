@head Chapter 7.3
@title Dimensionality Reduction with t-SNE
@sources chapter-7-3-dimensionality-reduction-with-t-sne
@count 15
@tldr t-SNE draws high-dimensional data on a flat map by keeping neighbours next to each other, which makes it great for seeing clusters and bad for anything else.
@why The maths barely appears on the exam. The questions are about **what you may and may not conclude from a t-SNE plot**. It's a short deck with a very high density of examinable facts.
@connect Chapter 7.2's PCA keeps global straight-line variance. t-SNE fixes the case in which the data has a curved shape, at a cost in speed and interpretability.
@goals
- Explain how t-SNE works in three steps
- Describe what perplexity controls
- List what you can and can't trust in a t-SNE plot
- Choose between PCA and t-SNE for a given task
@vocab
Local structure | Who each point's nearest neighbours are.
Global structure | Overall shape and distances between far-apart groups.
Perplexity | Roughly how many neighbours each point pays attention to.
KL divergence | A measure of how different two probability distributions are.
@map
2-5 | What t-SNE is, pros and cons | MEMORIZE | The five-point description
6-8 | MNIST example | SKIM | Why some digits overlap
9-10 | Perplexity and reading a plot | MEMORIZE | Trust vs do not over-read
11-14 | PCA comparison, practice | MEMORIZE | Slide 11's table

## How t-SNE works | Slides 2-8 | must
**PCA is linear:** it can crush curved structure flat. **t-SNE is non-linear:** it keeps neighbourhoods together, so curves survive.

::analogy Flattening a globe
PCA is like photographing Earth from space: you get one view with one hemisphere hidden. t-SNE is more like asking "who lives next door to whom?" and redrawing a map where neighbours stay neighbours, even if continents get moved around.
::
::steps The three steps (slide 14)
**Measure** neighbours: in the original space, compute how likely each pair of points is to be neighbours.
**Place** the points randomly in 2-D or 3-D.
**Adjust** positions step by step to make the two sets of similarities match, by minimizing KL divergence.
::

On MNIST digits (slides 7-8), t-SNE separates the classes clearly even though **it never saw the labels**: the colours are added just for display. Similar digits (5, 8 and 3) overlap, which makes sense. It is slow because pairwise similarities are expensive to calculate.

::tip Handwritten tip on slide 5
t-SNE can be used **after** PCA: first reduce with PCA, then run t-SNE on the output. It runs faster and carries less noise.
::
::key
- t-SNE is non-linear and preserves local neighbourhoods
- Steps: measure neighbours, place points, adjust by minimizing KL divergence
- It is mainly for visualization, usually in 2-D or 3-D
- It is computationally expensive
- Neither t-SNE nor PCA uses the class labels
::

## Perplexity and reading the plot | Slides 9-10 | must
**Perplexity** is the main setting. It roughly says how many neighbours each point pays attention to. The typical range is **5 to 50**.

| Perplexity | Result |
|---|---|
| Too low | Tiny fragments, noisy confetti |
| Sweet spot | Clear local groups |
| Too high | Clusters blur and merge |

Slide 10 is the most examinable slide of the deck.

| You can trust | Do not over-read |
|---|---|
| Points close together are similar | **Distance between clusters** means little |
| Tight groups usually indicate real local neighbourhoods | **Cluster size and density** are not reliable |
| Outliers and mislabelled items often sit in the wrong island | **Axes have no meaning**, and a rerun can rotate or flip the map |
| | Random data can still show fake-looking clusters |

::mnemonic Neighbours yes, Distances no
Read a t-SNE plot as a **seating chart**: you know who's at the same table. You don't know how far apart the tables truly are.
::
::trap Always try more than one setting
Before reporting "there are five clusters", rerun with several perplexities and random seeds. A pattern that disappears when you change a setting wasn't real.
::
::key
- Perplexity is the main knob, typically 5 to 50
- Points close together are similar
- Distance between clusters and cluster size mean little
- The axes have no meaning, and reruns can flip the map
- Random data can produce fake-looking clusters
::

## PCA or t-SNE? | Slides 11-14 | must
| | PCA | t-SNE |
|---|---|---|
| Type | Linear | Non-linear |
| Preserves | Global variance | Local neighbourhoods |
| Speed on big data | Very fast | Slow |
| Transforms new points | **Yes** | **No, refit needed** |
| Best for | Preprocessing, features | Visual exploration |

### Answers to the slide's own practice
::check Scenario 1: You ran t-SNE once and saw 5 clusters. What do you do before reporting it?
Rerun with several perplexity values and random seeds, and check that the clusters persist.
::
::check Scenario 2: "Clusters A and B are closer than A and C, so A is more similar to B." Safe?
No. Distances between clusters mean little on a t-SNE plot.
::
::check Scenario 3: You need 2-D input for a classifier trained today and used on new data tomorrow.
**PCA.** t-SNE can't transform new points without refitting.
::
::check Quick true or false from slide 13.
1. Axes have a fixed meaning: **false**. 2. Perplexity roughly sets how many neighbours each point attends to: **true**. 3. A bigger cluster always means a bigger group: **false**. 4. A trained t-SNE applies directly to new data: **false**. 5. PCA before t-SNE can speed it up and reduce noise: **true**.
::
::key
- PCA is linear, fast and transforms new points
- t-SNE is non-linear, slow and can't transform new points
- Use PCA for preprocessing and t-SNE for visual exploration
::

@head Classification Part 1
@title Bayes Error and Metrics
@sources classification-part-1-bayes-error-and-metrics
@count 36
@tldr The best possible classifier picks the most likely class, but even it makes mistakes, and accuracy alone can hide how dangerous those mistakes are.
@why Two classifiers on slide 28 have almost identical accuracy, 99.55% and 99.54%. One is safe to run a secure site with and the other lets in nine times as many intruders. This lecture gives you the tools to see that difference. Expect a confusion-matrix calculation on any exam.
@connect Chapter 3 defined loss and risk. Here they are applied to category answers. Part 2 builds a real classifier and evaluates it with these exact metrics.
@goals
- Say what the optimal classifier does and why it can still err
- Read a confusion matrix and extract TP, FP, FN and TN for any class
- Compute accuracy, precision, recall, specificity and F1
- Pick the right metric for a given cost of mistakes
- Score multilabel predictions
@vocab
Classifier | A function that outputs a class.
Positive class | Whichever class you are trying to detect. It doesn't have to be a "good" thing.
Conditional probability P(Y=y given X=x) | The chance of class y once you have seen features x.
argmax | The option that gives the largest value.
@map
3-8 | The framework and zero-one loss | MEMORIZE | Risk becomes the probability of a mistake
9-13 | Optimal classifier and Bayes error | MEMORIZE | Pick the most probable class
15-17 | Train and test, confusion matrix | WRITE | Rows actual, columns predicted
19-23 | TP, FP, FN, TN | WRITE | Slide 22's practice problem
24-30 | Why accuracy fails, the extra metrics | WRITE | All four formulas
31-34 | Multilabel and hierarchical | WRITE | Slide 34's worked example
36 | Exit ticket | WRITE | Answers are below

## The optimal classifier and Bayes error | Slides 3-13 | must
A classifier takes features X and outputs one of c classes. With **zero-one loss** (correct costs 0, wrong costs 1), the risk becomes simply *the probability of being wrong*.

So what's the best possible rule? Common sense turns out to be the theorem:

::formula Slide 9
g*(x) = argmax<sub>y</sub> P[Y = y | X = x]
::

**Given what you see, pick the most probable class.** Suppose for one patient the probabilities are 0.70 for class 1, 0.20 for class 0, 0.10 for class 2. Pick class 1.

Even so, that rule is wrong 30% of the time *on patients like this one*. Averaged across all patients, this unavoidable error is the **Bayes error rate**.

::plot Where the two classes overlap, even the best boundary makes errors | feature value | density | 14 | 10
area - 4: 5.6,0.09 5.8,0.15 6.0,0.24 6.2,0.37 6.4,0.57 6.6,0.84 6.8,1.21 7.0,1.68 7.2,1.36 7.4,0.95 7.6,0.64 7.8,0.42 8.0,0.27 8.2,0.16 8.4,0.10 8.6,0.06 8.8,0.03 9.0,0.02 9.2,0.01 9.2,0 5.6,0
fn - 2: 9*exp(-((x-5)/1.6)**2)
fn - 5: 8*exp(-((x-9)/1.6)**2)
text healthy: 5,9.5
text sick: 9,8.5
::

::analogy Lemon or lime, judged by weight alone
Some weights could easily be either fruit. Even a perfect guesser who knows the exact probabilities will often be wrong there, because weight simply does not contain enough information.
::
::trap You can't actually compute g*
It needs the true probabilities, which are unknown. Classifiers such as logistic regression and k-nearest neighbours are all ways to *approximate* it from data.
::
::tip Pre-classifier (slide 13)
Some models output a score first and turn it into a label afterward. With classes −1 and +1 and a score in [−1, 1], the label is the sign of the score: −0.4 becomes class −1 and 0.7 becomes class +1.
::
::key
- Zero-one risk equals the probability of misclassification
- The optimal classifier picks the class with highest conditional probability
- The Bayes error rate is the irreducible risk of that classifier
- The rule divides feature space into one region per class
::

## The confusion matrix | Slides 15-23 | must
A confusion matrix counts every prediction. **Rows are what it actually was and columns are what the model said.** Correct predictions run down the diagonal.

Slide 17's data, with n = 135:

| Actual ↓ / Predicted → | Dog | Cat | Possum |
|---|---|---|---|
| **Dog** | **30** | 2 | 6 |
| **Cat** | 8 | **22** | 15 |
| **Possum** | 7 | 4 | **41** |

Correct = 30 + 22 + 41 = 93. **Accuracy = 93 / 135 = 68.9%** and error is 31.1%. The most common single mistake is Cat predicted as Possum (15).

Now choose one class as "positive" and every cell falls into one of four boxes:

::steps Four counts for the Dog class
**TP** (true positive): dogs called dogs, the diagonal = **30**.
**FN** (false negative): dogs called something else, the rest of the Dog *row* = 2 + 6 = **8**.
**FP** (false positive): non-dogs called dogs, the rest of the Dog *column* = 8 + 7 = **15**.
**TN** (true negative): everything outside the Dog row and column = 22 + 15 + 4 + 41 = **82**.
Check: 30 + 8 + 15 + 82 = 135.
::
::mnemonic Positives in Pillars, Negatives Along the Rows
False **P**ositives live in the **column** (a pillar stands upright). False **N**egatives run along the row. This is the slide's own memory aid, made easy to picture.
::
::tip Reading the name of a count
The second word is what the model **said**. The first word says whether that was **correct**. "False negative": the model said negative, and it was wrong, so it really was positive.
::
::check Do it for Cat, then check against slide 23.
TP = 22. FN = 8 + 15 = 23. FP = 2 + 4 = 6. TN = 30 + 6 + 7 + 41 = 84. Total: 22 + 23 + 6 + 84 = 135.
::
::key
- Rows are actual classes, and columns are predicted classes
- TP is the diagonal cell
- FN is the rest of the row, and FP is the rest of the column
- TN is everything outside that row and column
- Zero-one loss = 1 − trace(M)/n
::

## Why accuracy can lie, and the metrics that don't | Slides 24-30 | must
A fingerprint scanner guards a secret base. It sees 100,550 people:

| Actual ↓ / Predicted → | Authorized | Not authorized |
|---|---|---|
| **Authorized** | 100 (TP) | 400 (FN) |
| **Not authorized** | 50 (FP) | 100,000 (TN) |

Accuracy = 100,100 / 100,550 = **99.55%**. Excellent? It let in **50 intruders**. When one class vastly outnumbers another, simply saying "not authorized" every time gets a superb accuracy.

There are two fixes. **Fix 1** (slide 26) makes the dangerous mistake cost more, such as a loss of 1000 for admitting an intruder. **Fix 2** is to look at more metrics.

| Metric | Formula | The question it answers |
|---|---|---|
| **Precision** | tp / (tp + fp) | Of everything I **called** positive, how much really is? |
| **Recall** (sensitivity) | tp / (tp + fn) | Of everything that really **is** positive, how much did I find? |
| **Specificity** | tn / (fp + tn) | Of all real negatives, how many did I correctly reject? |
| **F<sub>β</sub>** | (β²+1)tp / ((β²+1)tp + β²fn + fp) | One number that combines precision and recall |

With β = 1, the F1 score balances the two equally.

::example Both classifiers on slides 28 and 29
| Metric | Classifier 1 (TP 100, FN 400, FP 50) | Classifier 2 (TP 50, FN 10, FP 450) |
|---|---|---|
| Accuracy | 0.9955 | 0.9954 |
| Precision | 100/150 = **0.667** | 50/500 = **0.100** |
| Recall | 100/500 = **0.200** | 50/60 = **0.833** |
| Specificity | 0.9995 | 0.9955 |
| F1 | 0.3077 | 0.1786 |

For a secure site, a false positive is the disaster. Classifier 1 admits 50 intruders and Classifier 2 admits 450. So **high precision wins**, and we prefer Classifier 1. Change the cost of the mistakes, say to free discount vouchers, and the answer could flip.
::
::analogy Fishing with a net
**Precision:** of the things in your net, how many are fish, rather than boots? **Recall:** of all the fish in the lake, how many did you catch? A tiny net gets only fish (high precision) but misses most (low recall). A huge net does the opposite.
::
::mnemonic PREcision PREdicted, REcall REal
**Pre**cision divides by what you **pre**dicted positive: tp + fp. **Re**call divides by what was **re**ally positive: tp + fn.
::
::trap Which mistake costs more?
**Missed disease:** a false negative is the disaster, so maximize **recall**. **Spam filter eating real email:** a false positive for the spam class is the disaster, so maximize **precision**. Always ask "which error would be worse?" first.
::
::key
- Accuracy can hide costly mistakes, especially with imbalanced classes
- Precision = tp / (tp + fp), recall = tp / (tp + fn)
- Specificity = tn / (fp + tn)
- F-beta combines precision and recall into a single number
- The best metric depends on the cost of each kind of mistake
::

## Multilabel and hierarchical classification | Slides 31-36 | know
In standard classification each object gets exactly one class. In **multilabel** classification it can have any subset, for example, a satellite image that is "clear" and also contains "road" and "river". **Hierarchical** classification adds structure: farm and barn sit under "rural", and skyscraper under "urban".

Scoring treats the true labels Y and predicted labels Ŷ as **sets**.

::example One image (slide 34)
True labels: {clear, road, river}. Predicted: {clear, road}. Five labels exist altogether.

- **Exact match:** the sets differ, so **0**.
- **Accuracy:** correct over everything involved: |Y ∩ Ŷ| / |Y ∪ Ŷ| = 2/3.
- **Precision:** correct over predicted = 2/2 = **1**.
- **Recall:** correct over actual = 2/3.
- **Hamming loss:** wrong yes/no decisions over all labels = 1/5.
::

### Answers to slide 36's exit ticket
::check 1. Why can even the optimal classifier not reach zero error?
Because classes overlap. For some inputs, more than one class is possible, so the best choice is still sometimes wrong. That is the Bayes error rate.
::
::check 2. A spam filter must never send real email to junk. Which metric for the spam class?
**Precision.** Sending real email to junk is a false positive for the spam class, and precision is what falls when false positives rise.
::
::check 3. True labels {a, b}, predicted {b, c}. Precision and recall?
Only b is correct. Precision = 1/2 and recall = 1/2.
::
::key
- Multilabel: each object can have any subset of labels
- Hierarchical: labels form a tree that records how they relate
- Exact match needs the whole set to be correct
- Hamming loss is the share of wrong yes/no decisions over all labels
::

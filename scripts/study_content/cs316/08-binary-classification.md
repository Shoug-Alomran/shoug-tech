@head Classification Part 2
@title Binary Classification
@sources classification-part-2-binary-classification
@count 40
@tldr Logistic regression turns a weighted sum of features into a probability, and ROC curves judge how well it separates the two classes at every possible cut-off.
@why This is the one lecture where you see a complete model built from start to finish on real heart-disease data. Exams like to show you a code snippet or a classification report and ask what it means, and also to test the logit and sigmoid, the ROC axes, and what AUC values mean.
@connect Part 1 gave you the metrics. This chapter gives you the model that the metrics judge. Normalization shows how to make it train faster, and Chapter 8 shows how to tune it safely.
@goals
- Choose between label encoding and one-hot encoding
- Write the sigmoid and logit and say what each one does
- Explain why logarithms are used in maximum likelihood
- Read a classification report line by line
- Interpret an ROC curve and AUC value
@vocab
Odds | The chance something happens divided by the chance it doesn't. p = 0.8 means odds of 4 to 1.
Log-odds or logit | The logarithm of the odds.
Sigmoid | An S-shaped function squashing any number into the range 0 to 1.
Likelihood | How probable the observed data is, for given parameters.
Threshold | The probability above which we say "yes".
@map
2-8 | Dataset and encoding | WRITE | Label vs one-hot
10-12 | Logistic function, logit, sigmoid | MEMORIZE | Know both formulas
14-15 | Likelihood | MEMORIZE | Why logs are used
17-21 | Training pipeline | WRITE | Read each code step
23-30 | Prediction, metrics, interpretation | WRITE | Read a classification report
32-40 | Threshold limits, ROC, AUC | MEMORIZE | Axes, diagonal, AUC meanings

## Turning categories into numbers | Slides 2-8 | must
Models work with numbers, so text categories must be converted first. There are two ways.

| | Label encoding | One-hot encoding |
|---|---|---|
| Result | One column of integers | One 0-or-1 column per category |
| NO / YES | NO = 0, YES = 1 | `is_NO`, `is_YES` |
| Red / Green / Blue | 0, 1, 2 | Three columns |
| Risk | Implies a false order | Adds more columns |

::example Why label encoding can mislead
Encode city as Riyadh = 0, Jeddah = 1, Dammam = 2. The model now believes that Dammam is "twice as much" as Jeddah. It's nonsense, so use one-hot for categories with no natural order. For a binary target, label encoding is fine, because two values can't have a false middle.
::

::code python
# scikit-learn
enc = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
# Pandas
pd.get_dummies(df, columns=['cp', 'thal'])
::

`handle_unknown='ignore'` stops the model crashing if a new category shows up at prediction time. `get_dummies` may print True and False in newer Pandas, where older versions printed 1 and 0. They mean the same.

::key
- Label encoding maps each category to an integer and can imply a false order
- One-hot creates one binary column per category
- scikit-learn has OneHotEncoder and Pandas has get_dummies
- handle_unknown="ignore" prevents errors on unseen categories
::

## Logistic regression: score to probability | Slides 10-12 | must
Despite its name, **logistic regression is a classifier**. It works in two moves.

::steps From features to a decision
Compute a linear score: z = b<sub>0</sub> + b<sub>1</sub>x<sub>1</sub> + ... + b<sub>n</sub>x<sub>n</sub>. It can be any number.
Squash it through the sigmoid to get a probability between 0 and 1.
Compare the probability with a threshold, by default 0.5.
::
::formula Two functions that undo each other
Sigmoid (score to probability): σ(z) = 1 / (1 + e<sup>−z</sup>)
Logit (probability to score): log( p / (1 − p) ) = z
::

::plot The sigmoid squeezes every score into the range 0 to 1 | score z | probability | 12 | 10
fn - 1: 10/(1+exp(-(x-6)))
dash - 5: 0,5 12,5
ticks x: 1=-5 6=0 11=5
ticks y: 0=0 5=0.5 10=1
::

::example Computing both directions
- z = 0: σ(0) = 1 / (1 + 1) = **0.5**. A score of zero means a coin flip, which is the default decision boundary.
- z = 2: σ(2) = 1 / (1 + 0.135) = **0.88**.
- p = 0.9: logit = log(0.9 / 0.1) = log(9) ≈ **+2.2**.
- p = 0.1: logit = log(1/9) ≈ **−2.2**.
::
::analogy An exchange office
The **logit** converts probabilities into "score currency", where you can simply add up evidence. The **sigmoid** converts back. The model does its adding in score currency, which is why it is called linear *in the log-odds*.
::
::mnemonic Sigmoid Squashes, Logit Lets it out
**S**igmoid **s**quashes any score into (0, 1). The **l**ogit **l**ets a probability back out to the full number line.
::
::trap Regression in the name, classification in the job
If a question asks whether logistic regression predicts a continuous value such as a price, the answer is no. It outputs the probability of a class.
::
::key
- Logistic regression is a classifier that outputs a probability
- Linear score z = b0 + b1 x1 + ... + bn xn
- Sigmoid σ(z) = 1 / (1 + e^−z) maps any real number into (0, 1)
- Logit log(p / (1 − p)) is the log-odds and is the inverse of the sigmoid
- p = 0.5 means log-odds of 0, the default decision boundary
::

## Maximum likelihood: how it learns | Slides 14-15 | must
How does the model pick its coefficients? It asks: **which values make the outcomes we actually observed most probable?**

::example Likelihood for three patients
The model gives these probabilities of disease:

| Patient | Actually sick? | P(sick) | Probability of the actual outcome |
|---|---|---|---|
| A | Yes | 0.9 | 0.9 |
| B | No | 0.2 | 1 − 0.2 = 0.8 |
| C | Yes | 0.7 | 0.7 |

**Likelihood** = 0.9 × 0.8 × 0.7 = **0.504**.

**Log-likelihood** = ln 0.9 + ln 0.8 + ln 0.7 = −0.105 − 0.223 − 0.357 = **−0.685**.

Better coefficients raise this number toward 0.
::
::why Why take the logarithm?
Multiplying thousands of numbers below 1 quickly gives a value too small for a computer to hold accurately. Logs **turn a product into a sum**, which is numerically stable and easier to differentiate. And the coefficients that maximize one also maximize the other.
::
::key
- Likelihood is a product of probabilities over independent observations
- Log-likelihood turns products into sums and improves numerical stability
- Coefficients are fitted by maximum likelihood estimation
::

## The full scikit-learn workflow | Slides 17-30 | must
::code python
df['Target'] = df['num'].apply(lambda x: 'YES' if x > 0 else 'NO')
X = df.drop(['num', 'Target'], axis=1)      # drop BOTH
y = df['Target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = LogisticRegression(max_iter=1000).fit(X_train, y_train)
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
::

Here `num` of 0 means no disease and 1 to 4 means some degree of disease, so any value above 0 is recoded as YES.

::trap Dropping `num` is not optional
Target was computed directly from `num`. Leaving `num` among the features **leaks the answer** into the model, which then scores suspiciously well and is useless in real life.
::

### Reading a classification report
The layout looks like this. The support numbers are invented for illustration, and the 0.84 values match slide 29.

::code text
              precision    recall  f1-score   support
          NO       0.84      0.84      0.84        92
         YES       0.84      0.84      0.84        92
::

- **Precision for YES:** of all patients predicted to have disease, 84% really had it.
- **Recall for YES:** of all the patients with disease, 84% were caught.
- **Support:** how many actual cases of that class exist in the test set. It is a count, not a score.
- **macro avg** treats each class equally, and **weighted avg** weights by support.

Slide 30 notes that in medicine a missed case is the serious error, so **recall** for the disease class gets priority.

::says Slide 21 | A variable named log_likelihood
The slide stores `model.score()` in a variable called `log_likelihood`. On a classifier `score` returns **accuracy**, and the slide points this out. Don't be fooled by the name.
::
::key
- Recode num > 0 as YES and num = 0 as NO
- Drop both num and Target from the features to avoid leakage
- classification_report gives precision, recall, F1 and support per class
- Support is the number of actual occurrences of each class
- model.score on a classifier returns accuracy
::

## ROC curves and AUC | Slides 32-40 | must
Precision and recall are snapshots at a single threshold. Change the threshold and they change: lowering it from 0.5 to 0.2 made the model say YES more often, and precision fell from 0.85 to 0.74. ROC analysis looks at **all thresholds at once**.

::formula The two axes
True Positive Rate (y-axis) = TP / (TP + FN), also called recall or sensitivity
False Positive Rate (x-axis) = FP / (FP + TN), which is 1 − specificity
::

::plot Hugging the top-left corner is good, and the diagonal is coin-flipping | False Positive Rate | True Positive Rate | 10 | 10
curve - 3: 0,0 0.6,4.5 1.5,7 3,8.6 6,9.6 10,10
line - 5: 0,0 10,10
text good model: 3,9.3
text random: 6.6,5.2
ticks x: 0=0 10=1
ticks y: 0=0 10=1
::

::steps Walking along the curve
Threshold very high: nothing is called positive, so you start at (0, 0).
Lower it: you catch more real positives, and the curve climbs.
Lower it further: false positives start to pile up and the curve moves right.
Threshold very low: everything is called positive, so you end at (1, 1).
::

**AUC**, the area under the curve, summarizes the whole curve as a single number:

| AUC | Meaning |
|---|---|
| 1.0 | Perfect separation |
| 0.5 | Random guessing: the diagonal |
| Below 0.5 | Worse than random |

::analogy Metal detector sensitivity
Turn the dial up and you find every coin (high true positive rate) along with many bottle caps (high false positive rate). The ROC curve records that trade-off at every dial setting. AUC says how good the detector is overall, regardless of dial.
::
::trap AUC does not depend on the threshold
That is the whole point. Precision and recall do. If asked for a single threshold-independent way to compare two models, say AUC.
::
::key
- Precision and recall change with the decision threshold
- ROC plots TPR against FPR across thresholds
- The diagonal is a random classifier
- AUC of 1.0 is perfect, 0.5 is random, and below 0.5 is worse than random
- AUC is threshold-independent
::

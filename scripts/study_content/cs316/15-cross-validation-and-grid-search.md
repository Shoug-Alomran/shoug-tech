@head Chapter 8
@title Cross-Validation and Grid Search
@sources chapter-8-cross-validation-and-grid-search
@count 4
@tldr Instead of trusting one lucky split, test your model on every part of the data in turn, then use that same fair process to choose its settings.
@why There are only four slides, but they answer two questions that come up in every real project: "How good is my model really?" and "Which settings should I use?" The fit-counting question on slide 4 is an easy mark that many students get wrong.
@connect It formalizes Chapter 3's validation set and Chapter 4's bias and variance. Chapter 10's paired t-test then compares the fold scores of two models.
@goals

- Give the two problems with a single train-test split
- Describe k-fold cross-validation round by round
- Distinguish parameters from hyperparameters
- Count how many fits a grid search needs
  @vocab
  Fold | One of the k equal parts of the training data.
  Hyperparameter | A setting you choose before training, such as C or gamma.
  Parameter | A value the model learns during training, such as a coefficient.
  Grid | Every combination of the hyperparameter values you listed.
  @map
  2 | Why one split is not enough | MEMORIZE | The two problems
  3 | K-fold cross-validation | WRITE | Draw the rounds
  4 | Grid search | WRITE | Parameters vs hyperparameters; count the fits

## Why one split isn't enough | Slide 2 | must

Two separate problems arise with a single train-test split.

1. **It is noisy.** Your score depends on which rows happened to land in the test set. Another random split could give a quite different number.
2. **Tuning on the test set contaminates it.** Try many settings, keep the one with the best test score, and that score is no longer an honest estimate.

::analogy A single exam question
Judging a student from one question is unfair: they might have happened to know it. Asking several different questions gives both an **average** and a sense of how **consistent** they are.
::
::key

- One split gives a noisy estimate
- Tuning on the test set contaminates it
- Cross-validation gives both a mean and a spread
  ::

## K-fold cross-validation | Slide 3 | must

Split the training data into k equal folds. Every fold takes one turn as the validation set.

| Round | Fold 1  | Fold 2  | Fold 3  | Fold 4  | Fold 5  |
| ----- | ------- | ------- | ------- | ------- | ------- |
| 1     | **Val** | Train   | Train   | Train   | Train   |
| 2     | Train   | **Val** | Train   | Train   | Train   |
| 3     | Train   | Train   | **Val** | Train   | Train   |
| 4     | Train   | Train   | Train   | **Val** | Train   |
| 5     | Train   | Train   | Train   | Train   | **Val** |

::example With k = 5
The model is trained **five times**, each time on 80% of the training data, and validated on the remaining 20%. Suppose the scores are 0.90, 0.92, 0.88, 0.91 and 0.89. The mean is **0.90**, and the small spread suggests that the model is stable.
::
::code python
scores = cross_val_score(model, X_train, y_train, cv=5)
print(scores.mean(), scores.std())
::
::trap The test set stays untouched
Cross-validation runs on the training data. Keep a final test set for a single last evaluation.
::
::tip Avoid leakage inside the folds
Scale inside each fold, using a `Pipeline`. Scaling first would let validation rows influence the scaler, which is the same mistake as in the Normalization lecture.
::
::key

- Each fold validates exactly once
- k rounds train the model k times
- Report the mean and the spread of the fold scores
- Keep a separate test set for the final evaluation
  ::

## Grid search | Slide 4 | must

|             | Parameter               | Hyperparameter                    |
| ----------- | ----------------------- | --------------------------------- |
| Who sets it | The model **learns** it | **You choose** it before training |
| Examples    | Regression coefficients | C, gamma, learning rate, k in KNN |

Grid search tries **every combination** of the values you list, scoring each one with cross-validation.

::steps Count the fits
C has 3 values and gamma has 3 values, giving 3 × 3 = **9 combinations**.
Each combination is cross-validated with 5 folds.
Total model fits: 9 × 5 = **45**.
On the slide, C = 10 and gamma = 0.1 has the best mean score, **0.97**.
::
::code python
grid = GridSearchCV(model, {'C': [1, 10, 100], 'gamma': [0.01, 0.1, 1]}, cv=5)
grid.fit(X_train, y_train)
grid.best_params_
::
::mnemonic Parameters are Picked up, Hyperparameters are Handed in
The model **p**icks up parameters during training. You **h**and it the hyperparameters beforehand.
::
::trap It is combinations times folds
The answer isn't 9. Multiply by the number of folds: 3 × 3 × 5 = 45. Add another hyperparameter with 4 values and it jumps to 180, which is why grid search gets expensive quickly.
::
::key

- Parameters are learned, and hyperparameters are chosen
- Grid search tries every combination using cross-validation
- Total fits = combinations × folds
- Best on the slide: C = 10 and gamma = 0.1, score 0.97
  ::

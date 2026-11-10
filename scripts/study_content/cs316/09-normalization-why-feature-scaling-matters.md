@head Normalization
@title Why Feature Scaling Matters
@sources normalization-why-feature-scaling-matters
@count 7
@tldr Put every feature on a similar scale so that training converges quickly, and always learn the scaling numbers from the training data alone.
@why Only seven slides, yet the last rule on them is a classic exam trap. If you scale before splitting, your test score becomes dishonest. The formulas are also quick marks.
@connect This fixes a problem Chapter 4's gradient descent runs into when features have very different ranges. Chapter 8 returns to it using Pipelines inside cross-validation.
@goals
- Apply the standardization and min-max formulas by hand
- Explain why scaling changes the loss surface
- Define data leakage and avoid it
- Pick a scaler based on outliers
@vocab
Standardize | Rescale to mean 0 and standard deviation 1.
Data leakage | Information from the test set sneaking into training.
IQR | Interquartile range: Q3 minus Q1.
Solver | The optimization routine that fits the model.
@map
2-3 | The problem and the formulas | MEMORIZE | Both formulas
4-5 | Loss surface and results | MEMORIZE | Why convergence improves
6 | Fit on training only | MEMORIZE | Data leakage
7 | Choosing a scaler | MEMORIZE | Outlier sensitivity of each

## The problem and the two fixes | Slides 2-3 | must
In the breast-cancer dataset, one feature (worst area) has a standard deviation of **569.4** and another (fractal dimension error) of **0.0026**. That is a difference of around **200,000 times**. To a gradient-based model, the big numbers shout and the small numbers whisper.

| | Standardization | Min-max scaling |
|---|---|---|
| Formula | z = (x − μ) / σ | x′ = (x − min) / (max − min) |
| Result | Mean 0, standard deviation 1 | Values in [0, 1] |
| Use | The default for regression models | When you need a fixed range |
| Weakness | Moderate outlier sensitivity | Very sensitive to outliers |

::example Both by hand on 10, 20, 30
Mean μ = 20. σ = √(((−10)² + 0² + 10²) / 3) = √66.67 = 8.16.

**Standardized:** (10 − 20)/8.16 = **−1.22**, then **0**, then **1.22**.

**Min-max:** (10 − 10)/20 = **0**, (20 − 10)/20 = **0.5**, (30 − 10)/20 = **1**.
::
::analogy Mixing currencies in one sum
Add a salary in riyals to a height in metres and the salary swamps everything. Scaling is like converting all features into one shared unit first.
::
::key
- Features often differ enormously in spread
- Standardization: z = (x − mean) / standard deviation
- Min-max: x′ = (x − min) / (max − min), which maps to [0, 1]
- Standardization is the default for regression models
::

## Why training gets faster | Slides 4-5 | must
Unscaled features turn the loss surface into a **long, narrow valley**. The gradient points across the valley walls instead of along the valley floor, so gradient descent zigzags and needs a tiny learning rate. Scaled features make a **round bowl**, where the gradient points right at the minimum.

::analogy Rolling a ball down a canyon
In a narrow canyon the ball bounces from wall to wall on its way down. In a round bowl it goes straight to the bottom.
::

The numbers on slide 5 are worth remembering.

| Measure | Raw | Scaled |
|---|---|---|
| Solver iterations to converge | 2,342 | **19** |
| Test accuracy at default 100-iteration limit | 0.951 | **0.986** |
| Training log-loss after 500 steps, η = 0.01 | 2.40 | **0.127** |
| From-scratch gradient descent, test accuracy | 0.902 | **0.958** |

::key
- Unscaled features give a long, narrow valley, and gradient descent zigzags
- Scaled features give a round bowl
- Scaling cut iterations from 2,342 to 19 on the slide
::

## The leakage rule | Slide 6 | must
::steps The correct order
Split into training and test sets **first**.
Learn μ and σ from the **training set only** (`fit`).
Apply those same numbers to the training set (`transform`).
Apply those same numbers to the test set. **Never refit on it.**
::
::code python
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)     # transform only
::
::why Why it matters
If you scale the full dataset first, test rows influence μ and σ. **Information leaks** from the test set into training and the score comes out too optimistic. The test set is meant to stand in for the future, and the future can't influence today's scaling.
::
::mnemonic Fit once, Transform twice
**Fit** on training, one time. **Transform** both training and test.
::
::trap `fit_transform` on the test set
It looks harmless and even runs without error, but it recalculates the mean using test data. Test data only ever gets `transform`.
::
::tip Pipelines
A scikit-learn `Pipeline` enforces this rule automatically in every cross-validation fold.
::
::key
- Learn scaling statistics from the training set only
- Apply the same statistics to every other set
- Scaling before the split leaks test information
- A Pipeline applies this rule automatically
::

## Choosing a scaler | Slide 7 | must
| Scaler | Uses | Outlier sensitivity |
|---|---|---|
| `MinMaxScaler` | Min and max | **High** |
| `StandardScaler` | Mean and standard deviation | Moderate |
| `RobustScaler` | Median and IQR | **Low** |

::example One billionaire in the room (slide 7)
Take five ordinary salaries and one of 1,000,000. **Min-max** squeezes the five into the range 0 to 0.03, since one huge number stretches the max. They become almost identical. **Robust scaling** keeps them spread from −0.88 to 0.64, since the median and IQR ignore the extreme value.
::
::tip Rule of thumb
No big outliers: `StandardScaler`. Clear outliers: `RobustScaler`. Need a fixed range: `MinMaxScaler`.
::
::key
- MinMax has high outlier sensitivity
- StandardScaler has moderate outlier sensitivity
- RobustScaler uses the median and IQR, giving low outlier sensitivity
::

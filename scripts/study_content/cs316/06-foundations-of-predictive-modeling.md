@head Chapter 4
@title Foundations of Predictive Modeling
@sources chapter-4-foundations-of-predictive-modeling
@count 58
@tldr Training a model means walking downhill on a loss surface, and the art is stopping at a model that is complex enough to learn the pattern but not so complex that it memorizes the noise.
@why Chapter 3 said we want the function with the smallest loss. This chapter answers _how do we find it?_ Gradient descent is the engine inside almost every model you will hear about, and the bias-variance table is one of the most reliable exam questions in the course.
@connect This builds directly on Chapter 3's training and test loss. Classification, normalization and cross-validation all rely on these ideas.
@goals

- Tell convex from non-convex problems
- Compute a gradient and run gradient descent by hand
- Compare gradient descent with Newton's method
- Calculate MSE, RMSE and MAE
- Diagnose underfitting and overfitting from train and test errors
  @vocab
  Objective function | The quantity training tries to minimize. Also called loss or cost.
  Parameter | A number the model learns, such as a slope.
  Gradient | The vector of slopes in every direction. Points uphill.
  Learning rate (α or η) | How large each downhill step is.
  Hyperparameter | A setting you choose before training, such as the learning rate.
  @map
  3-8 | Optimization, convex vs non-convex | MEMORIZE | Definitions and an example of each
  10-18 | Gradient, Jacobian, Hessian | WRITE | Read the corrections for slides 17 and 18
  20-26 | Constrained problems, GD vs Newton | MEMORIZE | The four comparison points
  28-32 | Gradient descent | WRITE | Run the update rule by hand
  35 | MSE, RMSE, MAE | WRITE | Compute all three
  36-46 | Overfitting and underfitting | MEMORIZE | Slide 46's three pictures
  47-58 | Bias, variance and error decomposition | MEMORIZE | Slide 56 is the classic table

## Learning is optimization | Slides 3-8 | must

**Optimization** means selecting the best element from a set of alternatives, which in maths usually means finding a function's minimum or maximum. In machine learning, the function being minimized is the **objective function** (also called loss or cost), which measures the gap between predictions and actual values.

So "training a model" is just: _search all possible parameter values for the ones giving the lowest loss._

The shape of the loss surface decides how hard the search will be.

::plot Convex: only one bottom to find. Non-convex: you can get stuck in the wrong valley | parameter value | loss | 22 | 10
curve convex 2: 1,9 2.5,5 5,2 7,1.2 9,2 11,5 12,8
curve non-convex 5: 13,8 14.5,4 16,6 17.5,2.5 19,5.5 20,3.2 21,8.5
::

|                | Convex                                   | Non-convex                              |
| -------------- | ---------------------------------------- | --------------------------------------- |
| **Definition** | Convex objective and convex feasible set | Objective or feasible set is non-convex |
| **Minimum**    | Any local minimum is the global minimum  | Many local minima and saddle points     |
| **Example**    | Least-squares linear regression          | Neural network training                 |

::analogy A bowl versus a mountain range
Drop a marble in a **bowl** and it always reaches the one lowest point. Release it in a **mountain range** and it rolls into whichever valley is nearest, and that might not be the lowest one in the region.
::
::tip Why logistic regression counts as convex (slide 7)
It maximizes a _concave_ log-likelihood. Maximizing a concave function is the same as minimizing its negative, which is convex. So you will see it described as a convex problem.
::
::key

- Optimization selects the best element from a set of alternatives
- Training minimizes an objective, loss or cost function
- Convex: any local minimum is also global
- Non-convex: multiple local minima and saddle points, as in neural networks
- Linear regression has a quadratic objective, so it is convex
  ::

## The derivative toolkit | Slides 10-18 | must

You already know the derivative of one variable: the slope. These three objects extend the idea.

| Object          | What it holds                                                   | Order  | Tells you                               |
| --------------- | --------------------------------------------------------------- | ------ | --------------------------------------- |
| **Gradient** ∇f | All partial derivatives of a scalar function                    | First  | The direction of steepest ascent        |
| **Jacobian**    | First derivatives of a vector function, with one row per output | First  | How each output changes with each input |
| **Hessian**     | All second partial derivatives, in a square matrix              | Second | The curvature of the surface            |

::example Build a gradient and a Hessian
Let f(x, y) = x² + y².

- ∂f/∂x = 2x and ∂f/∂y = 2y, so **∇f = (2x, 2y)**.
- At (1, 1), the gradient is (2, 2). It points directly away from the minimum at the origin, which is why we walk the _opposite_ way.
- Second derivatives: ∂²f/∂x² = 2, ∂²f/∂y² = 2, and the mixed terms are 0. So the **Hessian is [[2, 0], [0, 2]]**. Positive on the diagonal means it curves up in every direction: a bowl.
  ::
  ::mnemonic Hessian = How it bends
  The **H**essian says **H**ow the surface bends, since it has second derivatives. The **J**acobian is about **J**ust the first derivatives of many outputs.
  ::

**Convexity test.** For one variable: if f″(x) is non-negative everywhere, f is convex. For many variables: if the Hessian is **positive semidefinite** across the domain, f is convex.

::says Slides 17 and 18 | Two statements to correct
The slides contain two errors.

- Slide 17 lists **log(x)** as convex. It is **concave**: f″(x) = −1/x² is negative. It is **−log(x)** that is convex.
- Slide 18 says **|x|** is neither convex nor concave. Standard maths treats |x| as **convex**. Convexity doesn't require smoothness, and the sharp corner at zero does not matter.

If an exam question copies the slide's wording exactly, mention the correct fact in your answer.
::
::key

- The gradient points in the direction of steepest ascent
- The Jacobian holds first derivatives of a vector-valued function
- The Hessian holds second derivatives and describes curvature
- A function is convex if its Hessian is positive semidefinite across its domain
  ::

## Gradient descent, step by step | Slides 20-32 | must

The gradient points uphill. To go downhill, step in the opposite direction. That is the entire algorithm.

::formula Update rule
x<sub>new</sub> = x<sub>old</sub> − α · ∇f(x<sub>old</sub>)
::

::analogy Walking down a hill in thick fog
You can't see the valley, only the ground beneath your feet. Feel which way is steepest, take a step the other way, repeat. **α** is your stride length: too long and you leap over the valley, too short and you'll be walking all night.
::
::steps Run it on f(x) = x² − 4x + 4 with α = 0.1, starting at x = 0
Derivative: f′(x) = 2x − 4. The true minimum is at x = 2.
Step 1: f′(0) = −4, so x = 0 − 0.1(−4) = **0.4**.
Step 2: f′(0.4) = −3.2, so x = 0.4 + 0.32 = **0.72**.
Step 3: f′(0.72) = −2.56, so x = 0.72 + 0.256 = **0.976**.
Each step is smaller than the last, because the slope is flattening. The steps shrink toward x = 2.
::

The algorithm on slide 32 repeats this until the change is tiny (it has converged) or until it hits `max_iters`.

Slide 20 uses that same function for a **constrained** problem: with the rule x ≤ 1, you can't reach 2, so the best allowed answer is **x = 1**. Constraints are limits on where you may search.

### Gradient descent versus Newton's method

Newton's method uses curvature as well as slope:

::formula Newton's update
x<sub>new</sub> = x<sub>old</sub> − H<sup>−1</sup> · ∇f(x<sub>old</sub>)
::

On our function, f″ = 2, so x = 0 − (−4)/2 = **2**: the exact minimum in one step. That is the power of curvature on a quadratic. Now the catch:

|                        | Gradient descent            | Newton's method                    |
| ---------------------- | --------------------------- | ---------------------------------- |
| Information used       | First derivatives only      | Hessian and its inverse too        |
| Cost per step          | Cheap                       | Expensive                          |
| Scales to large models | Yes                         | Impractical in high dimensions     |
| Convergence            | Steady                      | Fast near the minimum              |
| Non-convex behaviour   | May stop at a local minimum | Can reach saddle points or diverge |
| Step size              | A learning rate you tune    | Determined by the Hessian          |

::mnemonic Gradient is Grounded, Newton is Nimble
**Grounded:** cheap, simple and reliable. **Nimble:** fast near the target, but demanding and easy to knock off course.
::
::trap Learning rate is not "the bigger the better"
Too large, and the updates overshoot and can diverge. Too small and training crawls. It is a hyperparameter you tune.
::
::check For f(x) = x², from x = 3 with α = 0.1, what are the next two values?
f′(x) = 2x. First: 3 − 0.1(6) = **2.4**. Second: 2.4 − 0.1(4.8) = **1.92**.
::
::key

- Update rule: x_new = x_old − α × gradient
- The learning rate controls the step size
- Stop on convergence or at max_iters
- Newton uses the inverse Hessian: faster near the minimum but expensive
- Gradient descent scales better to high dimensions
  ::

## Measuring regression models: MSE, RMSE, MAE | Slide 35 | must

All three reduce a list of errors to a single number. Use one example. Errors (actual minus predicted) are **2, −1, 0, 3**.

| Metric   | Recipe                        | Working             | Result   |
| -------- | ----------------------------- | ------------------- | -------- |
| **MSE**  | Square, then average          | (4 + 1 + 0 + 9) / 4 | **3.5**  |
| **RMSE** | Root of MSE                   | √3.5                | **1.87** |
| **MAE**  | Absolute values, then average | (2 + 1 + 0 + 3) / 4 | **1.5**  |

::tip Which to use?
**RMSE** is in the same units as y, so it's easy to explain. **MSE** punishes large errors heavily, because they are squared. **MAE** treats all errors in proportion, so it is less bothered by outliers.
::
::key

- MSE averages squared errors
- RMSE is the square root of MSE and uses the units of y
- MAE averages absolute errors
- Squaring punishes large errors more
  ::

## Underfitting, overfitting and the sweet spot | Slides 36-46 | must

As you make a model more complex, training error always falls. Test error falls at first, then climbs back up. **The lowest point of the test curve is where you want to be.**

::plot Training error keeps falling, but test error turns back up | model complexity | error | 11 | 10
curve training 3: 1,8.8 3,4.8 6,2.2 10,0.8
curve test 5: 1,9.4 3,5.8 5,4 7,5 10,8.6
guide 5,4
ticks x: 2=underfit 5=best 9=overfit
::

| Fit          | Training error | Test error | Model is    |
| ------------ | -------------- | ---------- | ----------- |
| **Underfit** | High           | High       | Too simple  |
| **Good fit** | Low            | Low        | About right |
| **Overfit**  | Very low       | High       | Too complex |

The slides demonstrate this with polynomials. A straight line (degree 1) underfits. Degree 15 overfits: its training MSE of 0.011 looks far better than the line's 0.186, yet it wiggles through noise. A degree around 4 to 7 balances them.

::analogy Three students
**Underfit:** skimmed the headings and fails both practice and real exams. **Overfit:** memorized practice answers, aces the practice, fails the real one. **Good fit:** understood the material and does well on both.
::
::trap A lower training error doesn't mean a better model
Slide 42's degree 15 has the lowest training error and is the worst model. Always compare on data the model hasn't seen.
::
::key

- Underfitting: high training and high test error
- Overfitting: low training and high test error
- Training error keeps falling with complexity, while test error falls then rises
- The goal is generalizing to unseen data
  ::

## Bias, variance and what you can fix | Slides 47-58 | must

Expected error splits into three components.

::formula Error decomposition
Expected error = Bias² + Variance + Irreducible error
::

- **Bias** is error from overly simple assumptions. The model keeps missing in the same direction.
- **Variance** is error from being too sensitive to the particular training set. Change the data slightly and the model changes a lot.
- **Irreducible error** is noise. Nothing removes it.

::analogy Archery (slide 49)
**High bias:** arrows tightly grouped but off to one side. Consistently wrong. **High variance:** arrows scattered all around the target. Inconsistent. **Wind** is the irreducible error.
::

Slide 56 lets you diagnose directly from two numbers. **A big training error means bias. A big gap between training and test means variance.**

| Train error | Test error | Diagnosis         | What to try                              |
| ----------- | ---------- | ----------------- | ---------------------------------------- |
| 1%          | 11%        | **High variance** | More data, simpler model, regularization |
| 15%         | 16%        | **High bias**     | More complex model, better features      |
| 15%         | 30%        | **Both**          | Fix the bias first                       |
| 0.5%        | 1%         | **Good**          | Ship it                                  |

::mnemonic Bias is Blind, Variance is Volatile
**Blind** models ignore the pattern. **Volatile** models react to everything. Match them to the row above.
::
::trap More data does not fix bias
A straight line stays a straight line however many examples it sees. More data helps **variance**. Bias needs a more capable model or better features.
::
::check Train 2%, test 3%, and the best human error on this task is 2%. Good or bad?
**Good.** The training error is close to what is achievable, and the gap between training and test is small. There is little reducible error left.
::
::key

- Bias comes from a model that is too simple
- Variance comes from sensitivity to the training set
- Irreducible error is a floor that no model can beat
- Large training error signals bias, large train-test gap signals variance
  ::

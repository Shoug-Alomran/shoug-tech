@head Chapter 3
@title Statistical Learning
@sources chapter-3-statistical-learning
@count 30
@tldr Every prediction problem can be written as Y = f(X) + noise, and the entire game is to learn f from a limited sample so that it still works on data you have never seen.
@why This chapter looks like a wall of Greek letters, but it only says a handful of ordinary things. Once you know that **risk means average mistake**, and that **a low training score proves nothing**, the symbols stop being scary. Chapter 4 and both classification decks are built on these exact definitions.
@connect Chapter 1 named "model building" and "model evaluation" as steps. This chapter defines precisely what a model is and what "good" means. Chapter 4 then shows how to actually find the good one.
@goals
- Explain Y = f(X) + ε and every part of it
- Tell apart error, loss, training loss, test loss and risk
- Say why the regression function is the best possible predictor
- Split error into reducible and irreducible parts
- Explain overfitting using training and test loss
@vocab
Y | The response or target: what you want to predict.
X | The features, inputs or predictors: what you know.
f | The true relationship between X and Y. Nobody gives it to you.
g | Your guess at f. Also called the prediction function.
ε (epsilon) | Noise: the part of Y that X cannot explain.
E(...) | Expected value. Read it as "the long-run average of".
argmin | "The input that makes this smallest."
@map
3-9 | What statistical learning is, Y = f(X) + ε | MEMORIZE | Every symbol in the equation
10-12 | Regression, classification, loss, error | MEMORIZE | Squared-error and zero-one loss
13-16 | Risk and the ideal predictor | MEMORIZE | Reducible and irreducible error
17-19 | Training set, supervised, unsupervised | MEMORIZE | The teacher analogy
20-23 | Training loss, the learner, overfitting | MEMORIZE | Why zero training loss is not the goal
24-27 | Generalization, test and validation sets | MEMORIZE | Slide 21's table sums everything up
28-30 | Notation, three pillars, an example | SKIM | Know the three pillars

## The one equation behind the whole course | Slides 4-9 | must
Look at the slides' advertising data: sales went up as TV, radio and newspaper budgets went up. We want a formula for sales given the budgets. Statistics writes that wish as:

::formula Slide 8
Y = f(X) + ε
::

Read it as a sentence: **what happens = the part you can explain + the part you cannot.**

| Symbol | Name on the slides | In the advertising example |
|---|---|---|
| Y | Response or target | Sales |
| X = (X<sub>1</sub>, X<sub>2</sub>, X<sub>3</sub>) | Features, inputs, predictors | TV, Radio, Newspaper budgets |
| f | The unknown true relationship | How budgets really drive sales |
| ε | Measurement errors and other discrepancies | A holiday nobody recorded, random shopper moods |

::analogy Baking the same cake twice
You follow the same recipe (X) twice and the cakes (Y) come out slightly different. The recipe's effect is **f**. The humidity that day and how you happened to stir is **ε**. Even a perfect baker cannot remove ε completely.
::

A model has **two goals**, and slide 5 makes them vivid.

::example Black box versus statistical learning (slides 5-6)
**A black box says:** "This house costs $450,000." It may be right, but it cannot say why or how sure it is.

**Statistical learning says:** "Each extra 100 sq ft is associated with about $15,000 more, holding bedrooms and neighbourhood fixed, and we are 95% confident that the true effect is between $12,000 and $18,000."

The second answer *interprets* the relationship and *quantifies uncertainty*. That is what makes it statistical learning.
::
::trap "Associated with", not "causes"
The slide is careful: extra square feet are *associated with* a higher price. A model finds a relationship. It does not prove a cause. Exam statements saying that a coefficient "proves" something are wrong.
::
::key
- The two goals are prediction and finding interesting patterns
- Statistical learning interprets the model and quantifies uncertainty
- Y = f(X) + ε: response = true relationship + noise
- A good f predicts at new points and shows which features matter
::

## Regression, classification and measuring a mistake | Slides 10-12 | must
The type of Y decides the type of problem.

| | Y can be | Example | Usual loss |
|---|---|---|---|
| **Regression** | Any real number | House price | Squared error: (y − ŷ)² |
| **Classification** | One of c categories | Sick or healthy | Zero-one: I{y ≠ ŷ} |

A **loss function** is simply *the price you pay for one wrong prediction*. (A little hat means "predicted", so ŷ is your guess.)

::example Scoring single predictions
**Squared error:** the true price is 100, you predict 90. Loss = (100 − 90)² = 100. If you predict 70, loss = 900. Being three times further away costs nine times as much, so squared loss really hates big misses.

**Zero-one loss:** I{...} means "1 if true, otherwise 0". Predict "sick" for a sick person: loss 0. Predict "healthy" for a sick person: loss 1. It does not matter how confident you were.
::
::mnemonic I for Incorrect
The indicator I{y ≠ ŷ} gives a **1 when Incorrect**. Read the curly braces as a yes-or-no question: "Was it wrong?"
::
::key
- Regression has a real-valued response, and classification has a finite set of classes
- A loss function prices one prediction
- Squared-error loss for regression, zero-one loss for classification
- Squared error is just one example of a loss function
::

## Risk, and the best prediction possible | Slides 13-16 | must
Loss judges a single prediction. We want to judge a *function* over everything it might ever face. That average is called the **risk**.

::formula Slide 13
ℓ(g) = E[ Loss(Y, g(X)) ]
::

**Risk = the average loss over all possible cases.** That's all the formula says.

Now ask: if you knew everything, what is the best possible prediction at X = 4? Several different Y values occur at X = 4, so you cannot be right every time. The best single guess, under squared-error loss, is their **average**:

::formula The regression function (slide 14)
f(x) = E(Y | X = x)
::

::example Why the average wins
Three past customers spent 3, 4 and 5 hundred riyals at the same income level. A guess of 4 has squared losses 1, 0 and 1, totalling 2. A guess of 5 has losses 4, 1 and 0, totalling 5. No other number beats the mean.
::

Even this perfect predictor still makes mistakes, because of ε. That splits every model's error into two parts.

::formula Slide 15
E[(Y − ĝ(X))² | X = x] = [f(x) − ĝ(x)]² + Var(ε)
Total error = Reducible + Irreducible
::

| Part | What it is | Can you lower it? |
|---|---|---|
| **Reducible** | How far your model is from the true f | Yes: better model, better features, more data |
| **Irreducible** | Var(ε), the randomness in Y itself | No. It is the floor that nobody can go below |

::analogy Darts in a windy room
Your aim can improve: that is reducible error. The wind pushes every dart a little however good you are: that is irreducible error.
::
::trap Optimal does not mean zero error
The regression function is the best *possible*, yet it still has error equal to Var(ε). If a question claims the ideal predictor makes no mistakes, it is false.
::
::key
- Risk is the expected loss over the true distribution
- Under squared error, the best predictor is E(Y | X = x)
- That ideal function is called the regression function
- Error = reducible + irreducible, and irreducible is Var(ε)
- g* minimizes the risk but depends on an unknown distribution
::

## Four words students mix up | Slide 21 | must
Slide 21 is the single best slide in the deck. All four terms measure mistakes, and they differ only in **how much data they cover**.

| Term | Covers | Averaged? | Formula |
|---|---|---|---|
| **Error** | A general distance | No | \|y − ŷ\| |
| **Loss** | One prediction | No | (y − ŷ)² |
| **Training or test loss** | A sample you hold | Average over the sample | (1/n) Σ Loss(y<sub>i</sub>, g(x<sub>i</sub>)) |
| **Risk** | Everything that could ever occur | Expectation over the true distribution | E Loss(Y, g(X)) |

::analogy One student's marks
**Loss** is your mark on one question. **Training loss** is your average on the practice exam you studied. **Test loss** is your average on a paper you have never seen. **Risk** is how you would average over every possible exam that could ever be written, which you can never actually sit.
::
::mnemonic Loss is one, risk is all
**One** prediction gives a loss. **All** possible data gives a risk. Train and test losses sit in between: a sample.
::
::example Compute a training loss by hand
True values: 3, 5, 7. Predictions: 2.5, 5.5, 6.

Errors: 0.5, −0.5, 1. Squared losses: 0.25, 0.25, 1. Training loss = (0.25 + 0.25 + 1) / 3 = **0.5**.
::
::key
- Error is a general distance between truth and approximation
- Loss scores one prediction
- Training and test loss are sample averages of the loss
- Risk is the expected loss over the true, unknown distribution
::

## Supervised and unsupervised learning | Slides 17-19 | must
The optimal g* needs the true distribution, which we don't have. All we ever have is a finite **training set** of examples.

| | Supervised | Unsupervised |
|---|---|---|
| Do we have answers? | Yes: x and y | No: only x |
| Goal | Learn x to y | Learn the structure of the data |
| Slide's analogy | A teacher gives exercises and the solutions | Nobody gives you the answers; you group things yourself |
| Methods | Regression, classification | Clustering, PCA, kernel density estimation |

::analogy Sorting a bag of fruit
**Supervised:** a parent names each fruit as you learn, and later you name a new one. **Unsupervised:** nobody says a word, yet you still pile the round orange ones together and the long yellow ones together.
::
::trap Learner versus optimal function
**g\*** is the unreachable best function. **g<sup>G</sup><sub>τ</sub>** (the learner) is the best you can get from *your* training set and *your* chosen family of functions. Different training set, different learner, so the slides call it a *random* function.
::
::key
- The training set is a finite sample of usually independent examples
- Supervised learning has a teacher providing responses
- Supervised methods are regression and classification
- Unsupervised methods include clustering, PCA and density estimation
::

## Why a perfect training score is a warning sign | Slides 20-23 | must
Risk can't be calculated, so we estimate it with the **training loss**. The learner is then found in two steps (slide 22):

::steps How a learner gets built
Choose a family of candidate functions G. The simplest is every straight line.
Pick the function in G with the smallest training loss.
::

Why not skip step 1 and consider *every possible function*? Because then a useless function wins.

::example The memorizer (slide 23)
Build a function that returns the exact right answer for every training point, and 0 for everything else. Its training loss is exactly **zero**. On any new input it returns 0, so it is worthless.
::

This failure has a name: **overfitting**. *Poor generalization to new data, despite excellent results on training data.*

::analogy The student who memorizes the answer key
They get 100% on last year's paper and fail the new one, because they learned the answers instead of the subject. Slide 23 sums it up: minimizing the training loss is not the ultimate goal.
::
::key
- Training loss is an unbiased estimator of the risk for a fixed function g
- The learner minimizes training loss within a chosen class G
- Linear functions are the simplest useful class
- Overfitting is poor generalization, and zero training loss can cause it
::

## Measuring what really matters | Slides 24-30 | must
**Generalization risk** is the true average loss of your learner on brand-new data. Averaging it across all possible training sets gives the **expected generalization risk**. Slide 25's own note admits that you would need the true distribution to compute these, which is what we are trying to learn. So there is a practical workaround.

**Test loss** is the same average as training loss, computed on a separate **test sample** that played no part in training. It gives an unbiased estimate of generalization risk.

| Set | Used for | Exam analogy |
|---|---|---|
| **Training** | Fitting the model | Practice problems with solutions |
| **Validation** | Choosing between models | A mock exam |
| **Test** | One final honest score | The real exam |

::trap Why you may need three sets
If you use the test set to *choose* your model, it has influenced the choice and is no longer independent. That is why slide 27 says that a third set is needed.
::
::tip The three pillars (slide 29)
Finding a good learner rests on **function approximation** (represent the relationship), **optimization** (search for the best one), and **probability and statistics** (judge how far to trust it).
::
::key
- Generalization risk is the loss of the learner on new data
- Test loss estimates generalization risk without bias
- The test sample must be independent of the training set
- Use a validation set for model selection and a test set for the final score
- Three pillars: function approximation, optimization, probability and statistics
::

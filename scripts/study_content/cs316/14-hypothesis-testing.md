@head Chapter 10
@title Hypothesis Testing
@sources chapter-10-hypothesis-testing
@count 15
@tldr Hypothesis testing asks a single question: if nothing interesting were really happening, how surprising would this result be?
@why Model B scored 2 points higher than Model A. Is that a real improvement, or luck? This chapter gives you a procedure for answering that. The t-test computations are worth several exam marks and follow the same five steps every time.
@connect It rests on the Central Limit Theorem from Chapter 9, and it's applied directly to cross-validation scores like those in Chapter 8.
@goals
- Distinguish a parameter from a statistic
- Interpret a confidence interval properly
- Define H0, H1, p-value and significance level
- Run an independent t-test and a paired t-test by hand
- Distinguish Type I and Type II errors
@vocab
Parameter | A fixed value that describes a population, such as the true mean μ.
Statistic | A value calculated from a sample, such as the sample mean x̄.
H0 | The null hypothesis: nothing interesting is happening.
H1 | The alternative hypothesis: there is a difference.
p-value | The probability of seeing a result at least this extreme if H0 is true.
α | The threshold for rejecting H0, usually 0.05.
@map
2-6 | Inference, estimation, confidence intervals | MEMORIZE | Parameter vs statistic
7-8 | Hypothesis testing concepts | MEMORIZE | H0, H1, p-value, alpha
9-11 | t-tests | WRITE | Follow the worked example
12-13 | Paired exercise | WRITE | Compute by hand
14 | Type I and II errors | MEMORIZE | Know the full table

## From a sample to the whole population | Slides 2-6 | must
**Statistical inference** means generalizing about a population using data from a sample. It has two components: estimating a parameter, and testing a hypothesis.

| Term | Describes | Symbol | Memory hook |
|---|---|---|---|
| **P**arameter | The **p**opulation | μ | P goes with P |
| **S**tatistic | The **s**ample | x̄ | S goes with S |

An estimate can be a **point** (one number: the sample mean is 161.5 cm) or an **interval** (95% CI = [160.2, 162.8]).

::trap What "95% confident" really means
The method produces intervals that capture the true mean 95% of the time. It isn't that the true mean is bouncing around with 95% probability. The mean is fixed, and the interval is what varies from sample to sample.
::
::key
- Parameters describe a population, and statistics come from a sample
- Inference has two parts: parameter estimation and hypothesis testing
- A confidence interval is a range likely to contain the true parameter
::

## The logic of a hypothesis test | Slides 7-8 | must
The procedure is like a court case. **Assume innocence, then see whether the evidence is too strong to fit that assumption.**

| Court | Hypothesis test |
|---|---|
| Innocent until proven guilty | H0: nothing interesting is happening |
| The prosecution's claim | H1: there is a difference |
| How damning the evidence is | The p-value |
| "Beyond reasonable doubt" | α, commonly 0.05 |
| Verdict: guilty | Reject H0 |
| Verdict: not guilty (never "innocent") | Fail to reject H0 |

::formula The decision rule
p-value &lt; α → reject H0
p-value ≥ α → fail to reject H0
::
::mnemonic If p is low, H0 must go
A small p-value means this result would be very surprising if H0 were true, so you reject H0.
::
::trap What a p-value is not
It is **not** the probability that H0 is true. It's the probability of seeing data at least this extreme *assuming* H0 is true. Also, "fail to reject" doesn't mean H0 is proven.
::
::key
- H0 is the default assumption, and H1 is the claim being tested
- The p-value is the probability of the observed result if H0 is true
- Reject H0 when the p-value is below α, commonly 0.05
::

## Independent two-sample t-test | Slides 9-11 | must
Use this when **two separate groups** are compared. Slide 10 compares active learning (Group A) with lectures (Group B).

| | Group A | Group B |
|---|---|---|
| Sample size | n<sub>1</sub> = 20 | n<sub>2</sub> = 22 |
| Mean | 78 | 72 |
| Standard deviation | 8 | 9 |

::steps Five steps, always in this order
**Hypotheses.** H0: μ<sub>1</sub> = μ<sub>2</sub>. H1: μ<sub>1</sub> ≠ μ<sub>2</sub>.
**Pooled variance.** s² = [(19)(64) + (21)(81)] / 40 = 2917 / 40 = **72.93**.
**t statistic.** SE = √(72.93 × (1/20 + 1/22)) = **2.64**, so t = (78 − 72) / 2.64 = **2.27**.
**Degrees of freedom.** df = n<sub>1</sub> + n<sub>2</sub> − 2 = **40**.
**Decision.** Critical value at α = 0.05 (two-sided) is about 2.021. Since 2.27 > 2.021, **reject H0**. The teaching methods differ.
::
::mnemonic Humans Prefer To Do Decisions
**H**ypotheses, **P**ooled variance, **T** statistic, **D**egrees of freedom, **D**ecision. In the order that you must do them.
::
::key
- Independent t-test compares two separate groups
- Pooled variance combines the two sample variances
- df = n1 + n2 − 2
- Reject H0 when the absolute t statistic exceeds the critical value
::

## Paired t-test: comparing two models | Slides 12-13 | must
Both models were scored on the **same 10 folds**, so the scores come in matched pairs. That calls for a paired test, which analyses the differences.

| Fold | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| A | .82 | .80 | .84 | .79 | .83 | .81 | .85 | .80 | .82 | .81 |
| B | .85 | .83 | .84 | .82 | .86 | .82 | .88 | .81 | .85 | .83 |
| B − A | .03 | .03 | .00 | .03 | .03 | .01 | .03 | .01 | .03 | .02 |

::steps Run it
Mean difference: 0.22 / 10 = **0.022**.
Standard deviation of the differences: about 0.01135, so SE = 0.01135 / √10 = **0.00359**.
t = 0.022 / 0.00359 = **6.13**, with df = 10 − 1 = **9**.
Critical value at α = 0.05 is 2.262. Since 6.13 > 2.262, **reject H0**: Model B really is better. The p-value is about 0.0002.
95% CI: 0.022 ± 2.262 × 0.00359 = **[0.014, 0.030]**. It excludes 0, which agrees with rejecting H0.
::
::trap Independent or paired?
The same subjects or folds measured twice: **paired**. Two separate groups: **independent**. On cross-validation scores, folds are shared, so choosing the independent test throws away information.
::
::tip Degrees of freedom
Paired: n − 1, where n is the number of pairs. Independent: n<sub>1</sub> + n<sub>2</sub> − 2.
::
::key
- Paired tests analyse the differences between matched scores
- df = number of pairs − 1
- Same folds for both models calls for a paired test
- A confidence interval that excludes 0 agrees with rejecting H0
::

## Type I and Type II errors | Slide 14 | must
| | Type I (false positive) | Type II (false negative) |
|---|---|---|
| Definition | Rejecting H0 when it's true | Failing to reject H0 when it's false |
| Notation | α | β |
| What you are claiming | "There is an effect" (there isn't) | "There is no effect" (there is) |
| Medical example | Healthy person told they have a disease | Real disease missed in a sick person |
| How to reduce | Lower α, say from 0.05 to 0.01 | Bigger sample or a more powerful test |

::mnemonic The boy who cried wolf
First, the villagers believed there was a wolf when there wasn't: **Type I**, a false alarm. Later, they ignored a real wolf: **Type II**, a miss. The story has them in the right order.
::
::trap Lowering α has a cost
Fewer false alarms, but more misses. Unless you also add data, reducing Type I errors raises Type II errors.
::
::key
- Type I: rejecting a true H0, false positive, probability α
- Type II: failing to reject a false H0, false negative, probability β
- Lower α to reduce Type I; increase the sample size to reduce Type II
::

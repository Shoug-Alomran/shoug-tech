@head Chapter 9
@title Fundamental Statistical Theorems
@sources chapter-9-fundamental-statistical-theorems
@count 20
@tldr Bayes tells you how to update a belief after seeing evidence, the Law of Large Numbers says averages settle down, and the Central Limit Theorem says averages form a bell curve.
@why These three ideas explain why data science works at all: why a sample can stand in for a population, and why a positive test result is often not what it seems. The disease example on slide 4 is a favourite, because almost everyone's first instinct is wrong.
@connect Chapter 10 uses the Central Limit Theorem directly, because t-tests rely on sample means being approximately normal. MLE returns from the logistic regression lecture.
@goals

- Apply Bayes' theorem to the medical example
- Explain the difference between MLE and MAP
- State the Law of Large Numbers and the Central Limit Theorem and tell them apart
- Say what high and low entropy mean
  @vocab
  Prior | What you believed before seeing evidence.
  Likelihood | How well the evidence fits a hypothesis.
  Posterior | Your updated belief after seeing the evidence.
  Sample mean | The average of the sample you actually collected.
  Population | Everyone or everything you care about.
  @map
  4-6 | Bayes' theorem and medical example | WRITE | Compute this by hand
  7-8 | MLE and MAP | MEMORIZE | The formulas and the difference
  10-12 | Law of Large Numbers | MEMORIZE | Definition and example
  14-16 | Central Limit Theorem | MEMORIZE | Conditions and meaning
  17-19 | Entropy | MEMORIZE | High vs low

## Bayes' theorem: updating beliefs | Slides 4-6 | must

::formula Bayes' theorem
P(A | B) = P(B | A) × P(A) / P(B)
Posterior = Likelihood × Prior / Evidence
::

The disease scenario: a rare disease affects **1 in 1,000** people, and the test is 99% accurate. You test positive. What is the chance you're actually sick? Most people say 99%. The real answer is about **9%**.

::steps Count 1,000 people
**1** person has the disease. They test positive with probability 0.99, so **0.99** true positives.
**999** people don't. 1% of them test positive anyway, giving **9.99** false positives.
Total positives: 0.99 + 9.99 = **10.98**.
Chance you are the real case: 0.99 / 10.98 = **0.09**, or about **9%**.
::
::analogy The fire alarm in a huge building
The alarm is very reliable. Still, there are so many more ordinary days than actual fires that most alarms turn out to be burnt toast. When a condition is rare, false alarms outnumber real cases.
::
::trap P(+ | disease) is not P(disease | +)
They look alike, and the first is 99% while the second is 9%. Students confuse them all the time, so always say out loud which comes first.
::
::tip Why it matters: the base rate
The answer is low because of the small prior. Change it to 1 in 10 and the same test gives a far higher posterior. Slide 4's handwriting makes this point: the result depends on the prior.
::
::key

- Posterior = likelihood × prior ÷ evidence
- With a rare disease, a positive test can still mean a low chance of being sick
- In the slide's example, 99% accurate gives about 9% posterior
- P(+ | disease) and P(disease | +) are different
  ::

## MLE and MAP: estimating a parameter | Slides 7-8 | must

Both ask "what's the best parameter value?" They differ in whether you have an opinion beforehand.

|              | MLE                                    | MAP                                                   |
| ------------ | -------------------------------------- | ----------------------------------------------------- |
| Full name    | Maximum likelihood estimation          | Maximum a posteriori                                  |
| Asks         | Which θ makes this data most probable? | Which θ is most probable given the data and my prior? |
| Formula      | argmax P(data given θ)                 | argmax P(θ given data)                                |
| Uses a prior | No                                     | **Yes**                                               |

::example Coin with 7 heads in 10 flips
**MLE:** pick the value that makes this outcome most likely: **θ = 0.7**.

**MAP:** if you strongly believe that coins are fair, a prior centred on 0.5 pulls the answer somewhere between 0.5 and 0.7. With more flips, the data dominates and the prior matters less.
::
::tip Flat prior
If the prior treats all values equally, then MAP and MLE give the same answer. Slide 8 is the reason to remember this: **MAP is MLE plus a prior.**
::
::key

- MLE finds the parameter that makes the observed data most probable
- MAP maximizes the posterior, so it adds a prior belief
- With a flat prior, MAP equals MLE
  ::

## The Law of Large Numbers | Slides 10-12 | must

**The more trials you run, the closer the average gets to the true mean.**

::formula Slide 12
lim<sub>n→∞</sub> P(|X̄ − μ| > ε) = 0
::

Read it as: _as the sample grows, the chance that the sample mean is far from the true mean goes to zero._

::example Coin tossing
10 flips might give 7 heads: 70%. 1,000 flips might give 508: 50.8%. 100,000 flips will be very close to 50%. Individual tosses are as random as ever, and only the average settles.
::
::trap The gambler's fallacy
After 10 tails in a row, a coin is _not_ "due" for heads. The LLN works because later flips swamp early ones, not because they balance them out.
::
::key

- The sample average converges to the expected mean as trials increase
- It is why sample statistics can estimate population parameters
- Individual outcomes remain random
  ::

## The Central Limit Theorem | Slides 14-16 | must

Take many random samples, compute each sample's mean, and plot those means. **They form a bell curve, whatever shape the original population had.**

Conditions: random samples, finite mean and variance, sufficiently large sample size. The larger the sample, the closer to normal.

::plot Skewed population on the left, and the means of samples from it form a bell on the right | value | frequency | 22 | 10
curve population 5: 1,9 2,8 3.5,5 5,3 7,1.5 10,0.4
fn sample means 2: 9*exp(-((x-16)/1.8)**2)
::
::analogy Cookie weights (slide 16)
Individual cookies might be weirdly distributed. But take the **average weight of a batch of 50**, repeat for many batches, and those averages line up as a bell curve.
::

|             | LLN                            | CLT                                        |
| ----------- | ------------------------------ | ------------------------------------------ |
| Talks about | **Where** the sample mean goes | **What shape** the sample means make       |
| Conclusion  | It approaches the true mean    | Their distribution is approximately normal |

::mnemonic LLN is a Location, CLT is a Curve
**L**LN tells you the **L**ocation the mean heads to. **C**LT tells you the **C**urve the means form.
::
::trap The data doesn't become normal
The CLT is about the **sample means**, not the data. The population stays as skewed as it was. Exams love this distinction.
::
::key

- CLT: the distribution of sample means is approximately normal
- This holds regardless of the population's shape
- Conditions: random samples, finite mean and variance, large enough sample
- LLN says where the mean goes, CLT says what shape the means make
  ::

## Entropy | Slides 17-19 | know

Slide 18's "Guess Who" game gives the intuition. "Has a computer" is a **rare** attribute: it identifies one character, so hearing it gives **a lot of information**. "Is a person" fits everyone, so it tells you nothing.

**Rare events carry more information.** Entropy is the _expected_ information, or surprise, in a distribution.

| Entropy  | Meaning                         | Example                                             |
| -------- | ------------------------------- | --------------------------------------------------- |
| **High** | Unpredictable, more uncertainty | A fair coin (1 bit)                                 |
| **Low**  | Predictable, less uncertainty   | A coin that lands heads 90% of the time (0.47 bits) |

::key

- Rare attributes carry more information
- Entropy measures expected information, uncertainty or surprise
- High entropy = more uncertainty, low entropy = more predictable
  ::

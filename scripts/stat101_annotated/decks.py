"""STAT101 annotated slides — every Introduction to Probability Theory and Statistics chapter (Groebner, Business Statistics).

The decks are loose PDFs in slides/ full of formulas, tables and Excel screenshots, so every slide is shown
as the original image (whole=True) and the notes, tips and practice questions sit beside it. Each deck is a
namespace class built by chapter(); see cs331_annotated/ch01_1_introduction.py for the ANN keys."""
from .common import DECKS, mcq, see, short, tf, tip, trap, trick


def chapter(key, count, lede, ann):
    slug, file, pdf, label = DECKS[key]
    head, title = label.split(': ', 1)
    return type(key, (), {
        'AUTO_SLIDES': True,
        'DECK': {'key': key, 'slug': slug, 'file': file, 'title': title, 'chapter': head,
                 'pdf': '/academics/math/stat101/slides/%s' % pdf, 'lede': lede},
        'ANN': {n: dict(ann.get(n, {}), whole=True) for n in range(1, count + 1)},
    })


collection = chapter('d01', 68, 'What business statistics is, descriptive vs. inferential procedures, data collection (experiments, telephone surveys, questionnaires, observation, interviews), populations and samples, parameters and statistics, statistical and nonstatistical sampling, and data types and levels of measurement.', {
    5: dict(notes=['Descriptive statistics summarize data (charts, tables, averages). Inferential statistics use a sample to draw conclusions about a population (estimation, hypothesis testing).'],
            exam=[mcq('Using a sample of 200 customers to estimate the average spending of all customers is:', ['Inferential statistics', 'Descriptive statistics', 'A census', 'A parameter'], 0, '')], weight=3),
    14: dict(notes=['Closed-end questions give fixed choices; open-end questions let respondents answer in their own words.']),
    35: dict(notes=['Population: all items of interest. Sample: a subset. Census: data from every item in the population.']),
    36: dict(notes=['Parameter: describes a POPULATION (μ, σ). Statistic: describes a SAMPLE (x̄, s).'],
             tips=[trick('Population–Parameter, Sample–Statistic (P with P, S with S).')],
             exam=[mcq('The average age of ALL employees of a company is a:', ['Parameter', 'Statistic', 'Sample', 'Variable'], 0, '')], weight=3),
    40: dict(notes=['Nonstatistical sampling: convenience, judgment, ratio (quota): not based on chance.']),
    46: dict(notes=['Simple random sampling: every possible sample of size n is equally likely.']),
    51: dict(notes=['Stratified: divide into homogeneous subgroups (strata), sample randomly from each. Systematic: every k-th item after a random start (k = N/n). Cluster: divide into clusters, randomly select whole clusters.'],
             exam=[mcq('Choosing every 10th invoice after a random start is:', ['Systematic sampling', 'Stratified sampling', 'Cluster sampling', 'Convenience sampling'], 0, ''),
                   mcq('Splitting students by year and randomly sampling within each year is:', ['Stratified sampling', 'Cluster sampling', 'Judgment sampling', 'Systematic sampling'], 0, '')], weight=3),
    59: dict(notes=['Quantitative (numbers: discrete or continuous) vs. qualitative (categories). Time-series vs. cross-sectional data.']),
    62: dict(notes=['Levels: nominal (labels only), ordinal (ranked), interval (equal intervals, no true zero: °C), ratio (true zero: weight, income).'],
             tips=[trap('Temperature in °C is interval, not ratio: 20 °C isn’t "twice as hot" as 10 °C.')],
             exam=[mcq('Customer satisfaction rated poor / fair / good / excellent is:', ['Ordinal', 'Nominal', 'Interval', 'Ratio'], 0, '')], weight=3),
})

graphs = chapter('d02', 69, 'Frequency and relative frequency distributions for discrete and grouped data (number of classes, class width, boundaries), histograms and ogives, joint frequency distributions, bar charts, pie charts, stem-and-leaf diagrams, line charts and scatter diagrams.', {
    4: dict(notes=['Frequency distribution: a table of values (or classes) and how often each occurs. Relative frequency = frequency / n.']),
    17: dict(notes=['Number of classes: rule of thumb 2ᵏ ≥ n (smallest k). Class width ≥ (max − min)/k, rounded up.'],
             tips=[tip('2ᵏ ≥ n rule: n = 50 → k = 6 (2⁶ = 64).')],
             exam=[short('A data set has n = 100 values from 12 to 95. How many classes and what class width?', '2⁷ = 128 ≥ 100, so k = 7 classes; width ≥ (95 − 12)/7 ≈ 11.9, round up to 12.')], weight=3),
    23: dict(notes=['Cumulative frequency: the running total; plotted as an ogive.']),
    25: dict(notes=['Histogram: bars touch, for quantitative data grouped into classes; shows the distribution’s shape.']),
    36: dict(notes=['Joint frequency distribution (cross-tab): two variables at once.']),
    41: dict(notes=['Bar chart: categorical data, bars separated. Pie chart: parts of a whole (percentages adding to 100%).'],
             exam=[mcq('Which chart suits the percentage share of each department in a budget?', ['Pie chart', 'Scatter diagram', 'Line chart', 'Ogive'], 0, '')], weight=3),
    52: dict(notes=['Stem-and-leaf: like a histogram that keeps the original values.']),
    55: dict(notes=['Line chart: a variable over time (time series). Scatter diagram: relationship between two quantitative variables.'],
             exam=[mcq('To see whether advertising spend relates to sales, use a:', ['Scatter diagram', 'Pie chart', 'Bar chart', 'Stem-and-leaf'], 0, '')], weight=3),
})

numerical = chapter('d03', 100, 'Measures of center (mean, median, mode, weighted mean), shapes of distributions, percentiles, quartiles and box plots, measures of variation (range, IQR, variance, standard deviation), the empirical rule, Tchebysheff, standardized z-scores and the coefficient of variation.', {
    8: dict(notes=['Mean μ = Σx/N (population), x̄ = Σx/n (sample). The deviations from the mean always sum to zero.']),
    19: dict(notes=['The mean is pulled by extreme values; the median (middle of the ordered data) is resistant to them.'],
             tips=[trick('Skewed data or outliers → report the median.')],
             exam=[mcq('House prices with a few very expensive homes are best summarized by the:', ['Median', 'Mean', 'Range', 'Mode'], 0, '')], weight=3),
    24: dict(notes=['Median position: (n + 1)/2 in the sorted data; for even n, average the two middle values.'],
             exam=[mcq('The median of 3, 9, 4, 7, 10, 2 is:', ['5.5', '4', '7', '5.83'], 0, 'Sorted: 2, 3, 4, 7, 9, 10 → (4 + 7)/2.')], weight=3),
    34: dict(notes=['Mode: the most frequent value; the only center measure for nominal data.']),
    39: dict(notes=['Shapes: symmetric (mean = median), right-skewed (mean > median), left-skewed (mean < median).'],
             exam=[mcq('If the mean is much larger than the median, the distribution is:', ['Right-skewed', 'Left-skewed', 'Symmetric', 'Uniform'], 0, '')], weight=3),
    41: dict(notes=['Weighted mean = Σwx / Σw (e.g. GPA, portfolio returns).'],
             exam=[short('Grades: 3 credits at 4.0 and 2 credits at 3.0. Find the GPA.', '(3·4 + 2·3)/5 = 18/5 = 3.6.')], weight=3),
    44: dict(notes=['Percentile location index i = (p/100)·n: if i is an integer, average the i-th and (i+1)-th values; otherwise round up.']),
    50: dict(notes=['Box and whisker: min, Q1, median, Q3, max; IQR = Q3 − Q1; outliers beyond 1.5·IQR from the box.']),
    72: dict(notes=['Variance: σ² = Σ(x − μ)²/N; sample s² = Σ(x − x̄)²/(n − 1). Standard deviation = √variance.'],
             tips=[trap('Divide by n − 1 for a SAMPLE variance.')], weight=3),
    89: dict(notes=['Empirical rule (bell-shaped): about 68% within 1σ, 95% within 2σ, 99.7% within 3σ. Tchebysheff (any shape): at least 1 − 1/k² within k standard deviations.'],
             exam=[mcq('For bell-shaped data with mean 50 and SD 5, about 95% of values lie between:', ['40 and 60', '45 and 55', '35 and 65', '30 and 70'], 0, '')], weight=3),
    92: dict(notes=['z = (x − μ)/σ: how many standard deviations x is from the mean. Coefficient of variation CV = (σ/μ)·100% compares spread across different scales.'],
             exam=[mcq('A score of 85 with mean 70 and SD 10 has z =', ['1.5', '−1.5', '15', '0.15'], 0, '')], weight=3),
})

probability = chapter('d04', 47, 'Experiments, outcomes, sample spaces and tree diagrams, events (mutually exclusive, independent, dependent), classical, relative-frequency and subjective probability, and the rules of probability: complement, addition, conditional probability and multiplication.', {
    8: dict(notes=['Sample space: all possible outcomes of an experiment; tree diagrams help list them.']),
    11: dict(notes=['Mutually exclusive: can’t happen together. Independent: one doesn’t change the other’s probability.'],
             tips=[trap('Mutually exclusive events (with positive probabilities) are NOT independent: if one happens the other can’t.')],
             exam=[tf('Two mutually exclusive events with positive probabilities are independent.', False, '')], weight=3),
    15: dict(notes=['Assignment methods: classical (equally likely outcomes), relative frequency (past data), subjective (judgment).']),
    31: dict(notes=['Complement: P(Ā) = 1 − P(A).']),
    33: dict(notes=['Addition rule: P(A or B) = P(A) + P(B) − P(A and B); for mutually exclusive events P(A or B) = P(A) + P(B).'],
             exam=[mcq('P(A) = 0.5, P(B) = 0.3, P(A and B) = 0.1. P(A or B) =', ['0.7', '0.8', '0.15', '0.9'], 0, '')], weight=3),
    37: dict(notes=['Conditional probability: P(A | B) = P(A and B) / P(B). Independent ⇔ P(A | B) = P(A).'],
             exam=[mcq('P(A and B) = 0.12, P(B) = 0.4. P(A | B) =', ['0.3', '0.048', '0.52', '0.12'], 0, '')], weight=3),
    42: dict(notes=['Multiplication rule: P(A and B) = P(A)·P(B | A); for independent events P(A)·P(B).'],
             exam=[mcq('Two independent machines fail with probabilities 0.1 and 0.2. Both fail with probability:', ['0.02', '0.3', '0.28', '0.15'], 0, '')], weight=3),
})

discrete = chapter('d05', 49, 'Discrete random variables and probability distributions, expected value and standard deviation, the binomial distribution (formula, tables, mean and SD), and the Poisson distribution.', {
    4: dict(notes=['Discrete random variable: takes countable values (number of defects, customers).']),
    8: dict(notes=['E(x) = Σ x·P(x); σ = √Σ (x − E(x))²·P(x).'],
            exam=[short('x = 0, 1, 2 with P = 0.2, 0.5, 0.3. Find E(x).', 'E(x) = 0·0.2 + 1·0.5 + 2·0.3 = 1.1.')], weight=3),
    20: dict(notes=['Binomial conditions: n fixed trials, two outcomes, constant p, independent trials.']),
    28: dict(notes=['P(x) = C(n, x)·pˣ·(1 − p)ⁿ⁻ˣ. Mean μ = np, σ = √(np(1 − p)).'],
             exam=[mcq('n = 10, p = 0.3. The mean of the binomial distribution is:', ['3', '0.3', '2.1', '7'], 0, ''),
                   short('n = 4, p = 0.5. Find P(x = 2).', 'C(4, 2)·0.5²·0.5² = 6 × 0.0625 = 0.375.')], weight=3),
    42: dict(notes=['Poisson: counts of events in a continuous interval (time, area), with mean λ; P(x) = λˣe^(−λ)/x!; mean = variance = λ.'],
             tips=[trick('Fixed number of trials → binomial. Events per interval → Poisson.')],
             exam=[mcq('The number of customers arriving per hour is best modeled by the:', ['Poisson distribution', 'Binomial distribution', 'Normal distribution', 'Uniform distribution'], 0, '')], weight=3),
})

normal = chapter('d06', 27, 'The normal distribution and its shape, areas under the curve, the standard normal distribution and z-scores, using the z-table for left, right and between probabilities, and Excel functions.', {
    4: dict(notes=['Normal: bell-shaped, symmetric, mean = median = mode, total area = 1; determined by μ and σ.']),
    9: dict(notes=['Standardize: z = (x − μ)/σ, then use the standard normal table (μ = 0, σ = 1).'],
            exam=[short('Gas usage is normal with μ = 50, σ = 10. Find P(x < 65).', 'z = (65 − 50)/10 = 1.5; P(z < 1.5) ≈ 0.9332.')], weight=3),
    19: dict(notes=['Negative z: use symmetry: P(z < −a) = P(z > a) = 1 − P(z < a).'],
             tips=[trap('Draw the curve and shade the area before reading the table.')],
             exam=[mcq('P(−1 < z < 1) is about:', ['0.6826', '0.95', '0.3413', '0.9974'], 0, '')], weight=3),
    27: dict(notes=['Excel: NORM.DIST(x, μ, σ, TRUE) for a cumulative probability; NORM.S.DIST(z, TRUE) for standard normal.']),
})

sampling = chapter('d07', 47, 'Sampling error, the sampling distribution of the mean and its theorems (mean and standard error), the Central Limit Theorem, z for sample means, and the sampling distribution of a proportion.', {
    3: dict(notes=['Sampling error = x̄ − μ: the difference due to chance because only a sample is observed.']),
    25: dict(notes=['Sampling distribution of x̄: mean μ_x̄ = μ, standard error σ_x̄ = σ/√n.'],
             exam=[mcq('σ = 20 and n = 100. The standard error of the mean is:', ['2', '20', '0.2', '200'], 0, '')], weight=3),
    32: dict(notes=['Central Limit Theorem: for large n (≥ 30) the sampling distribution of x̄ is approximately normal, whatever the population’s shape.'],
             exam=[tf('The Central Limit Theorem requires the population itself to be normal.', False, 'It applies for large samples from any population.')], weight=3),
    33: dict(notes=['z = (x̄ − μ)/(σ/√n).']),
    38: dict(notes=['Sample proportion p̄ = x/n; σ_p̄ = √(p(1 − p)/n); approximately normal when np ≥ 5 and n(1 − p) ≥ 5.']),
})

estimation = chapter('d08', 20, 'Point vs. interval estimates, confidence intervals for a mean, critical values, the margin of error, and how confidence level and sample size affect the interval.', {
    4: dict(notes=['Point estimate: a single value (x̄ estimates μ). Interval estimate: a range likely to contain the parameter.']),
    6: dict(notes=['Confidence interval: x̄ ± z·σ/√n (σ known). 90%: z = 1.645, 95%: z = 1.96, 99%: z = 2.575.'],
            exam=[short('x̄ = 80, σ = 10, n = 25. Find the 95% confidence interval for μ.', 'Margin = 1.96 × 10/5 = 3.92; interval 76.08 to 83.92.')], weight=3),
    13: dict(notes=['Margin of error e = z·σ/√n (half the interval width).']),
    17: dict(notes=['Higher confidence → wider interval. Larger sample → narrower interval.'],
             tips=[trick('More confidence costs width; more data buys precision.')],
             exam=[mcq('Increasing the sample size (same confidence) makes the confidence interval:', ['Narrower', 'Wider', 'Unchanged', 'Shifted up'], 0, '')], weight=3),
})

regression = chapter('d09', 68, 'Scatter plots and correlation (r), testing the significance of correlation, simple linear regression by least squares, interpreting the slope and intercept, R² and the standard error of the estimate.', {
    2: dict(notes=['Correlation coefficient r: strength and direction of a LINEAR relationship, −1 ≤ r ≤ 1.'],
            tips=[trap('Correlation does not imply causation.')],
            exam=[mcq('r = −0.9 indicates:', ['A strong negative linear relationship', 'A weak relationship', 'No relationship', 'A strong positive relationship'], 0, '')], weight=3),
    28: dict(notes=['Regression model: y = β₀ + β₁x + ε; least squares fits ŷ = b₀ + b₁x minimizing Σ(y − ŷ)².'],
             exam=[short('ŷ = 20 + 3x (sales in $1000s vs. ads). Interpret the slope and predict y at x = 10.', 'Each extra unit of advertising increases predicted sales by 3 ($3,000). ŷ = 20 + 30 = 50 ($50,000).')], weight=3),
    40: dict(notes=['R² (coefficient of determination): the share of the variation in y explained by x; in simple regression R² = r².'],
             exam=[mcq('If r = 0.8, R² =', ['0.64', '0.8', '0.89', '1.6'], 0, '')], weight=3),
    54: dict(notes=['Standard error of the estimate s_ε: the typical size of the residuals.']),
})

DECKS_HERE = [collection, graphs, numerical, probability, discrete, normal, sampling, estimation, regression]

@head Chapter 2.2
@title Importing, Summarizing and Visualizing Data
@sources chapter-2-2-importing-summarizing-and-visualizing-data
@count 33
@tldr Before you model anything, label each column with its true type, boil it down to a few summary numbers, and draw the right chart for it.
@why Python will happily compute the "average gender" if gender is stored as 1 and 2. This chapter teaches you to stop that. It also holds the two skills exams test most directly: reading the output of `describe()` and choosing the correct chart for a given question.
@connect Chapter 2.1 gave you the tools. This is the _exploration_ step of the data science process from Chapter 1. Chapter 2.3 then repairs the gaps you find here.
@goals

- Classify any column as quantitative or qualitative
- Recode wrongly typed columns with replace and astype
- Interpret describe(), value_counts() and crosstab()
- Calculate the mean, median, quartiles, variance and standard deviation by hand
- Choose the right plot for one or two variables
  @vocab
  Feature | A column of data, also called a variable.
  Quantile | A cut-off with a given share of data below it.
  Quartiles | The 25%, 50% and 75% cut-offs, written Q1, Q2 and Q3.
  Dispersion | How spread out the values are.
  Contingency table | A count of how two categories combine. Also called a cross-tabulation.
  @map
  3-4 | Rows, columns and three kinds of column | MEMORIZE | Identifier, design and measurement columns
  5-8 | Where data lives: UCI, Rdatasets | SKIM | Know `read_csv(..., header=None)`
  9-15 | Feature types and recoding | WRITE | Classify all of them and recode one
  16-19 | Summary tables | WRITE | Read `describe`, `value_counts`, `crosstab`
  20-23 | Mean, quantiles, spread | WRITE | Compute each by hand
  24-33 | Plots | MEMORIZE | The chart-choosing table below

## Rows, columns and the three kinds of column | Slides 3-4 | must

The slides define data as **the result of a random experiment**, whose outcome cannot be known in advance. In a table, the convention is:

- **Rows** are the individual items, or units. One row is one person.
- **Columns** are the variables, or features.

Columns come in three kinds:

| Column kind     | What it records                                        | Example in the nutrition data              |
| --------------- | ------------------------------------------------------ | ------------------------------------------ |
| **Identifier**  | Which row is which                                     | A person's ID number                       |
| **Design**      | Conditions fixed before measuring. They define groups. | `gender`, `situation`                      |
| **Measurement** | Observed results, which vary between people            | `height`, `weight`, `tea`, `coffee`, `age` |

::analogy A cooking competition
Each dish has a **ticket number** (identifier). The **rules** say whether it was cooked on gas or electric (design: set up before anyone tasted anything). The judges' **scores** are what you actually measure, and those vary.
::
::why Why the difference matters
Design columns tell you _how the data was collected and which groups you can compare_. Measurement columns are what you analyse. Mix them up and you could end up "predicting" something that was decided in advance.
::
::key

- Data is the result of a random experiment
- Rows are units, columns are features
- Three kinds of column: identifier, design, measurement
- Measurements vary, while design columns describe the setup
  ::

## Feature types, and fixing them in Python | Slides 9-15 | must

Every feature is one of two main types, and the quantitative type splits in two.

::graph Every feature fits one branch of this tree
n f 170 0 Feature
n qn 60 80 Quantitative\nreal numeric meaning
n ql 290 80 Qualitative\ncategories
n c 0 170 Continuous\nheight, voltage
n d 130 170 Discrete\ncount of births
n k 290 170 Also called\ncategorical or factors
e f qn
e f ql
e qn c
e qn d
e ql k
::

The test: **could you sensibly average it?** You can average heights. You cannot average eye colours. And discrete values you can _count_, whereas continuous values can fall anywhere in a range.

::trap Numbers can be qualitative
The nutrition data stores gender as 1 and 2, so Python treats all 13 features as integers. A code that happens to be a number is still a **category**. Ask what the number _means_, not what it looks like.
::

Fixing the types takes two methods: `replace` swaps the values and `astype` changes the type.

::code python
DICT = {1: 'Male', 2: 'Female'}
nutri['gender'] = nutri['gender'].replace(DICT).astype('category')
nutri['height'] = nutri['height'].astype(float)
::
::check Classify: shoe size, postal code, temperature, number of siblings, blood type.
Shoe size: quantitative discrete (sizes come in steps). Postal code: **qualitative**, because averaging postcodes is meaningless. Temperature: quantitative continuous. Siblings: quantitative discrete. Blood type: qualitative.
::
::key

- Quantitative features have numerical meaning; continuous or discrete
- Qualitative features are categories, also called categorical or factors
- A number used as a code is still qualitative
- Use replace to rename the values and astype to change the type
  ::

## Summary tables: describe, value_counts, crosstab | Slides 16-19 | must

Three commands compress a whole column into something readable.

**`describe()` changes its output depending on the column type.** For categories it gives:

::code text
nutri['fat'].describe()
count 226 # how many non-missing values
unique 8 # how many different categories
top sunflower # the most common category
freq 68 # how many times the top one appears
::

For numbers it gives count, mean, std, min, the three quartiles and max.

**`value_counts()`** gives a count for every category, from most to least common.

**`pd.crosstab(a, b)`** counts how two categories combine:

|            | Couple | Family | Single | All |
| ---------- | ------ | ------ | ------ | --- |
| **Female** | 56     | 7      | 78     | 141 |
| **Male**   | 63     | 2      | 20     | 85  |
| **All**    | 119    | 9      | 98     | 226 |

::example Reading a crosstab properly (slide 19)
The slide claims that the proportion of single men is much smaller than single women. Do not compare 78 and 20 directly, because the group sizes differ.

Single women: 78 / 141 = **55.3%**. Single men: 20 / 85 = **23.5%**. The claim holds, and now you can put a number on it.

`margins=True` adds the "All" row and column shown above.
::
::trap Comparing raw counts between unequal groups
Whenever groups are different sizes, convert to proportions first. The exam loves a table where the raw count points one way and the percentage points the other.
::
::key

- describe on a category gives count, unique, top and freq
- describe on a number gives count, mean, std, min, quartiles and max
- value_counts counts each category
- crosstab counts combinations of two categories, and margins=True adds totals
  ::

## The numbers that describe a column | Slides 20-23 | must

Use one small dataset for every formula: **2, 4, 4, 4, 5, 5, 7, 9** (n = 8, already sorted).

**Where is the centre?** The mean adds and divides. The median is the middle value.

::formula Sample mean
x̄ = (x<sub>1</sub> + x<sub>2</sub> + ... + x<sub>n</sub>) / n
::

Mean = 40 / 8 = **5**. The median is halfway between the 4th and 5th values: (4 + 5) / 2 = **4.5**.

**Quantiles** are cut-offs. The p-sample quantile has at least a fraction p of the data at or below it, and at least 1 − p at or above. The 0.25 quantile is also the 25th percentile and the first quartile.

| Name | Same as                         | Share of data below |
| ---- | ------------------------------- | ------------------- |
| Q1   | 25th percentile                 | 25%                 |
| Q2   | 50th percentile, the **median** | 50%                 |
| Q3   | 75th percentile                 | 75%                 |

**How spread out is it?**

::steps Sample variance and standard deviation of 2, 4, 4, 4, 5, 5, 7, 9
Find the mean: 5.
Subtract it from every value: −3, −1, −1, −1, 0, 0, 2, 4.
Square each one: 9, 1, 1, 1, 0, 0, 4, 16.
Add them: 32.
Divide by **n − 1**, which is 7: variance s² = 32 / 7 = **4.57**.
Square-root: standard deviation s = **2.14**.
::

The range is simply max − min = 9 − 2 = **7**.

::analogy Variance versus standard deviation
Heights in centimetres have a variance in _square centimetres_, which means nothing to anyone. Taking the square root brings the number back to centimetres, so you can say "people typically differ from the average by about 9 cm".
::
::example Reading the real describe() output (slide 23)
For `height`: count 226, mean 163.96, std 9.00, min 140, 25% is 157, 50% is 163, 75% is 170, max 188.

- Typical person is about 164 cm, give or take 9 cm.
- The middle half lies between 157 and 170, so the interquartile range is 170 − 157 = **13**.
- The mean is just above the median, so a very slight right skew.
- The range on slide 22 is 188 − 140 = **48**, which matches.
  ::
  ::trap Sample variance divides by n − 1
  Pandas `.var()` and `.std()` divide by n − 1 by default. NumPy's `np.var()` divides by n. The same data can therefore give two different answers, and an exam can ask why.
  ::
  ::tip Outliers pull the mean, not the median
  If one student in a class of ten scores 900 by a data entry error, the mean jumps and the median barely moves. This is why skewed data is summarized with the median, and why Chapter 2.3 fills skewed columns with the median.
  ::
  ::key
- The sample mean is the average, and the median is the 0.5 quantile
- Quartiles are the 25th, 50th and 75th percentiles
- Variance divides squared deviations by n − 1, and std is its square root
- Range = max − min; describe() gives all of these at once
  ::

## Choosing the right chart | Slides 24-33 | must

Do not memorize chart code first. Memorize **which chart answers which question**. It depends only on how many variables you have and what type they are.

| You have       | Question                       | Chart                      | Code from the slides      |
| -------------- | ------------------------------ | -------------------------- | ------------------------- |
| 1 qualitative  | How many in each group?        | **Bar plot**               | `plt.bar(...)`            |
| 1 quantitative | What is the shape?             | **Histogram**              | `plt.hist(...)`           |
| 1 quantitative | Centre, spread, outliers?      | **Box plot**               | `plt.boxplot(...)`        |
| 1 quantitative | What share is below x?         | **ECDF**                   | `plt.step(x, y)`          |
| 2 qualitative  | How do groups split?           | **Grouped bars**           | `sns.countplot(x=, hue=)` |
| 2 quantitative | How are they related?          | **Scatter plot**           | `plt.scatter(x, y)`       |
| 1 of each      | Does a number differ by group? | **Side-by-side box plots** | `plt.boxplot([a, b])`     |

::mnemonic One word for each
**Bar** for _counts_, **hist** for _shape_, **box** for _summary_, **scatter** for _relationship_. Whenever you are given a question, pick the matching word.
::

### How to read a box plot

Use the height data: Q1 is 157, the median is 163, and Q3 is 170.

::plot Height summarized as a box: the middle half of people sit inside it | height (cm) | | 70 | 10
line - 2: 10,5 27,5
line - 2: 40,5 58,5
line - 1: 27,2.5 40,2.5 40,7.5 27,7.5 27,2.5
line - 4: 33,2.5 33,7.5
ticks x: 10=140 27=Q1_157 40=Q3_170 58=188
text median 163: 33,8.6
::

- The **box** runs from Q1 to Q3 and holds the middle 50%.
- The **line inside** is the median.
- The **whiskers** reach out up to 1.5 × IQR past the box. Here that is 19.5 each way, so the fences are 137.5 and 189.5.
- Points **beyond the whiskers** are outliers. Height has none, since 140 and 188 are inside the fences.

### Making histograms comparable

The slide sets `weights = np.ones_like(nutri.age) / nutri.age.count()`. Each person then adds 1/n instead of 1, so the bars show **proportions** rather than counts, and groups of different size can be compared directly.

An **ECDF** (empirical cumulative distribution function) rises from 0 to 1. A height of 0.8 at age 75 means 80% of people are aged 75 or younger.

::check You want to know whether coffee consumption differs between men and women. Which chart?
Side-by-side box plots: one quantitative variable compared across one qualitative variable. That is slide 33.
::
::trap Bar plot or histogram?
A **bar** chart is for categories, and its bars can be reordered. A **histogram** is for numbers, its bars touch, and the order is fixed by the number line.
::
::key

- Bar for one category, histogram or box plot for one number
- Grouped bars for two categories, scatter for two numbers
- Side-by-side box plots for a number across categories
- A box shows Q1, median, Q3; whiskers extend up to 1.5 × IQR
- Weights of 1/n turn histogram counts into proportions
  ::

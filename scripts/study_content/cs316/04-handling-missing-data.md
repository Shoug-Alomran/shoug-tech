@head Chapter 2.3
@title Handling Missing Data
@sources chapter-2-3-handling-missing-data
@count 10
@tldr Before fixing an empty cell, ask why it is empty, because the reason decides whether dropping, filling or carrying a value forward is honest.
@why This deck has only 10 slides but it tests judgment rather than memory: you are given a column and asked what you would do with it. Real data always has holes, and a careless fix can make your results look fine while being quietly wrong.
@connect In Chapter 2.2 you found the gaps. Here you repair them. Every model in later chapters assumes this step has been done, since most algorithms cannot accept a blank.
@goals
- Count the missing values in each column
- Distinguish MCAR, MAR and MNAR
- Choose between dropping, filling and forward filling for a given column
- Use `isnull`, `fillna` and `dropna` with `axis`, `subset` and `thresh`
@vocab
NaN | Pandas' marker for an empty cell.
Impute | A statistician's word for filling in a missing value.
Skewed | Lopsided, with a long tail of extreme values on one side.
@map
2 | Why it matters, three options | MEMORIZE | Drop, fill, forward or backward fill
3-4 | Detecting missing values | WRITE | `isnull().sum()`
5 | MCAR, MAR, MNAR | MEMORIZE | The most conceptual slide of the deck
6-7 | fillna | WRITE | Constant, mean, median
8-10 | dropna | WRITE | Rows, columns, `subset`, `thresh`

## Detecting missing values | Slides 2-4 | must
Missing data can distort analysis and bias results. So the first job is simply to find it.

::code python
df.isnull()         # a True/False table, the same shape as df
df.isnull().sum()   # how many missing in each column
::

Why does `sum()` work on True and False? Because Python counts **True as 1 and False as 0**. Adding a column of them counts the Trues.

::example Reading the output
A gradebook of 40 students gives:

`name 3, major01 0, major02 8, project 5, final 12`

Now you know: everyone has a first major grade, while the final is missing for 12 of the 40 students, which is 30% of the class. A gap of that size deserves more thought than a gap of 3.
::
::key
- isnull gives a True or False table
- isnull().sum() counts missing values per column, since True counts as 1
- Your three options are to drop, fill, or forward and backward fill
::

## Why is it missing? MCAR, MAR and MNAR | Slide 5 | must
This is the heart of the deck. Three patterns exist, and they answer one question: **what does the chance of being blank depend on?**

| Pattern | Chance of being blank depends on | Gradebook example |
|---|---|---|
| **MCAR**: Missing Completely At Random | Nothing at all | A sync glitch randomly dropped a cell |
| **MAR**: Missing At Random | **Other** columns you can see | Late registrants have no Major 1, and registration date is in the data |
| **MNAR**: Missing Not At Random | **The missing value itself** | A student who failed did not submit the final |

::graph Ask these questions in order | directed
n q1 150 0 Does the blank depend on\nanything at all?
n a 0 100 MCAR\npure accident
n q2 310 100 Does it depend on\nanother column we can see?
n b 170 200 MAR\nexplained by other data
n c 440 200 MNAR\nthe value hides itself *
e q1 a no
e q1 q2 yes
e q2 b yes
e q2 c no
::

::analogy Three reasons a survey question about income is blank
**MCAR:** the printer smudged random lines. **MAR:** younger respondents skip it more often, and you know their ages. **MNAR:** people with very high incomes refuse to answer *because* their income is high.
::
::mnemonic MNAR hides itself
MNAR is the only pattern where the missing value is **N**ot just absent but is the very **R**eason it is absent. If the sentence uses words like "because their value was low", it is MNAR.
::
::trap The name "Missing At Random" is misleading
MAR is *not* random in the everyday sense. It has a pattern, explained by another observed column. Only MCAR is truly random. Note also that you usually cannot prove the pattern from the data alone: by definition, you cannot see what is missing.
::
::check People with severe depression are less likely to complete a depression questionnaire. Which pattern?
**MNAR.** The chance of the value being missing depends on the value itself, namely how severe the depression is.
::
::key
- MCAR: blank depends on nothing
- MAR: blank depends on other observed data
- MNAR: blank depends on the missing value itself
- The pattern often cannot be proven from the data alone
- Filling MNAR data with a mean can hide the very cases that need attention
::

## Filling gaps with fillna | Slides 6-7 | must
**Filling keeps every row, but it is a claim.** When you write a number in, you assert something about the world, so be sure that it is true.

| Fill with | Code | Use when | The claim you are making |
|---|---|---|---|
| Constant | `df.fillna(0)` | Blank really means zero | "Nothing happened here" |
| Mean | `df['A'].fillna(df['A'].mean())` | Roughly symmetric column | "This one is typical" |
| Median | `df['A'].fillna(df['A'].median())` | Skewed column | "This one is typical, ignoring outliers" |
| Forward or backward | `df.ffill()` or `df.bfill()` | Ordered data such as time series | "Same as its neighbour" |

::example Same column, three different fills
Column A is 1, 2, blank, 4.

- `fillna(0)` gives 1, 2, **0**, 4. The mean of the column drops to 1.75.
- Fill with the mean of the known values, (1 + 2 + 4) / 3, gives 1, 2, **2.33**, 4.
- `ffill` copies the value above, giving 1, 2, **2**, 4.
::
::example Choosing column by column, as on slide 5
- **Name is missing:** drop the row. No statistic can invent a person's identity.
- **Major 2, roughly bell-shaped:** the mean is reasonable.
- **Project, skewed by many zeros:** the median.
- **Final exam:** do not guess a high-stakes score.
::
::trap Filling with 0 is not neutral
If a blank means "the student did not sit the exam yet", a 0 tells the model they failed. It also drags the column mean down, which shifts everything calculated afterward.
::
::key
- fillna keeps every row but assumes something about the data
- Use the mean for symmetric columns and the median for skewed ones
- Forward and backward fill suit ordered data like time series
- Choose per column, based on what the column means
::

## Dropping gaps with dropna | Slides 8-10 | must
Drop when few values are missing, or when a value cannot reasonably be guessed. **The cost is losing data.**

Use this table:

| | A | B | C |
|---|---|---|---|
| **0** | 1 | 5 | 9 |
| **1** | 2 | blank | 10 |
| **2** | blank | blank | 11 |
| **3** | 4 | 8 | 12 |

| Code | Result | Why |
|---|---|---|
| `df.dropna()` | Keeps rows 0 and 3 | Default: drop a row with **any** blank |
| `df.dropna(axis=1)` | Keeps column C only | axis=1 drops **columns** with any blank |
| `df.dropna(subset=['A'])` | Keeps rows 0, 1, 3 | Only blanks in A count |
| `df.dropna(thresh=2)` | Keeps rows 0, 1, 3 | Keep rows with **at least 2 non-blank** values |

::steps Working out thresh=2 on the table above
Row 0 has 3 values, so it stays.
Row 1 has 2 values, so it stays.
Row 2 has only 1 value, so it goes.
Row 3 has 3 values, so it stays.
::
::mnemonic Zero goes down, One goes across
`axis=0` works **down** the table on rows and removes rows. `axis=1` works **across** and removes columns. Default is 0, so a plain dropna removes rows.
::
::trap `thresh` counts values that are present
`thresh=2` does not mean "drop if 2 are missing". It means "keep the row only if at least 2 values are present".
::
::check A column is 90% blank. dropna() would remove nearly all rows. What should you do instead?
Drop the **column**, with `axis=1`, or only that column by name. Row-dropping would throw away almost all your data because of one bad column.
::
::key
- dropna removes rows with any blank by default, and it shrinks the data
- axis=1 drops columns instead
- subset limits which columns are checked
- thresh keeps rows with at least that many non-null values
::

@head Chapter 2.1
@title Pandas for Data Analytics
@sources chapter-2-1-pandas-for-data-analytics
@count 61
@tldr Pandas gives you two objects, a labelled column called a Series and a labelled table called a DataFrame, plus tools to select from them and to move data in and out of files.
@why Everything practical in this course happens through Pandas, and the Python quiz leans on it heavily. Most lost marks here come from three tiny things: confusing `loc` with `iloc`, forgetting which slices include their end, and mixing up single and double brackets. This page makes those automatic.
@connect Chapter 1 said data science starts with collecting and cleaning. This chapter is the toolbox for doing that. Chapter 2.2 uses it to summarize data, and 2.3 uses it to repair missing values.
@goals
- Build a Series and a DataFrame in several ways
- Pick `loc` or `iloc` correctly every time
- Predict whether a slice includes its last element
- Filter rows with more than one condition
- Read and write CSV, Excel, SQL and JSON using the right parameters
@vocab
Index | The row labels. Think of it as the row's name tag. It does not have to be a number.
Series | One labelled column of data.
DataFrame | A table: several Series sharing one index.
Vectorized | An operation applied to every element at once, with no loop written by you.
NaN | "Not a Number": how Pandas marks an empty cell.
Delimiter | The character that separates values in a text file, usually a comma.
@map
2-5 | What Pandas is and how it compares | SKIM | Know Pandas vs Excel, SQL and NumPy in one line each
7-16 | Series: create, access, slice | WRITE | Practise every creation form and both slicing types
18-21 | DataFrame: create and access | WRITE | Single vs double brackets
23-26 | loc, iloc and filtering | WRITE | The highest-value slides in this deck
28-38 | Reading CSV, Excel, SQL, JSON | MEMORIZE | Know each function and its main parameters
40-56 | Exporting data | MEMORIZE | `index=False`, `if_exists`, `orient`, `chunksize`
58-61 | File paths and URLs | SKIM | Know `read_csv` accepts a URL and when you need `requests`

## What Pandas is, and its two building blocks | Slides 2-7, 18-19 | must
Pandas is a Python library for **data manipulation and analysis**, built on top of NumPy. If you have used Excel, you already understand the idea. Pandas is Excel you control with code, so the same cleaning steps can be re-run tomorrow on new data with one click.

It has exactly two objects worth knowing:

::graph Series stick together into a DataFrame, sharing the same index | directed
n s1 0 0 Series: Name\nAlice, Bob, Sara
n s2 240 0 Series: Age\n25, 30, 22
n df 120 110 DataFrame\nName + Age, one row per person *
e s1 df
e s2 df
::

A **Series** is one-dimensional: a single column where every value has a label. A **DataFrame** is two-dimensional: rows and columns, like a database table or a spreadsheet.

Three properties the slides stress:

- **The index aligns data.** When you add two Series, Pandas matches them by label, not by position.
- **Operations are vectorized.** `s * 2` doubles every element without a loop.
- **A DataFrame is size mutable and mixed-type.** You can add or delete rows and columns, and different columns can hold different types.

::analogy A class register
A **Series** is a single column of the register: marks, with each mark next to a student's name. A **DataFrame** is the whole register. The **index** is the student name printed on the left of every row: it travels with the data however you sort the page.
::
::tip Three one-line comparisons (slide 5)
**vs Excel:** better for automated, repeatable work and larger data. **vs SQL:** SQL queries databases, Pandas analyses in memory, and `pd.read_sql()` joins them. **vs NumPy:** Pandas is built on NumPy and adds labels for table work.
::
::key
- Pandas is built on NumPy for data manipulation and analysis
- Series = one-dimensional labelled array
- DataFrame = two-dimensional labelled table
- Data aligns by index label, and operations are vectorized
- DataFrames are size mutable and can mix column types
::

## Creating and reading a Series | Slides 7-16 | must
There are five ways to build a Series. They differ only in where the values and labels come from.

| Built from | Code | Index you get |
|---|---|---|
| List | `pd.Series([1, 2, 3, 4])` | Automatic: 0, 1, 2, 3 |
| List with labels | `pd.Series([1, 2], index=['a', 'b'])` | Your labels |
| Dictionary | `pd.Series({'a': 10, 'b': 20})` | The dictionary keys |
| NumPy array | `pd.Series(np.array([1, 2]))` | Automatic |
| Single value | `pd.Series(5, index=[0, 1, 2])` | Value is repeated for each label |

You can also pass an existing Series to copy it.

### The slicing rule that catches everyone
Take this Series:

::code python
s = pd.Series([10, 20, 30, 40, 50], index=['a', 'b', 'c', 'd', 'e'])
::

| You write | You get | Why |
|---|---|---|
| `s['a']` | 10 | Access by label |
| `s.iloc[0]` | 10 | Access by position |
| `s[1:3]` | 20, 30 | **By position: the end is excluded** |
| `s['a':'c']` | 10, 20, 30 | **By label: the end is included** |
| `s[0:5:2]` | 10, 30, 50 | Step of 2 |

::analogy Why labels include the end
Positions work like Python lists, where `1:3` means "start at 1, stop *before* 3". A label has no "one before it" you could reliably stop at, so if you ask for `'a'` to `'c'`, Pandas gives you everything up to and including `'c'`.
::
::mnemonic Names Include, Numbers Exclude
Slice by **n**ame and the end is **i**ncluded. Slice by **n**umber and the end is **e**xcluded.
::
::check `s = pd.Series([5, 6, 7, 8], index=['w', 'x', 'y', 'z'])`. What are `s[1:3]` and `s['x':'y']`?
Both give **6 and 7**. The first is positions 1 and 2, because 3 is excluded. The second is labels x through y, with y included.
::
::trap `s[0]` on a labelled Series
The slide shows `s[0]` for "access by position". In recent Pandas versions this is deprecated when the index is made of labels. Write `s.iloc[0]` in real code. In the exam, read it as "the first element".
::
::key
- Create from list, list with index, dictionary, NumPy array, scalar or another Series
- A dictionary's keys become the index
- A scalar value is repeated for every label in the index
- Slicing by position excludes the end, slicing by label includes it
::

## Creating and accessing a DataFrame | Slides 19-21 | must
The most common way to build one is a dictionary. **Keys become column names, and each value list becomes that column.**

::code python
data = {'Name': ['Alice', 'Bob'], 'Age': [25, 30]}
df = pd.DataFrame(data)
#     Name  Age
# 0  Alice   25
# 1    Bob   30
::

From a NumPy array you must supply column names yourself, because an array has no labels to offer: `pd.DataFrame(arr, columns=['x', 'y'])`.

**The number of brackets decides what comes back:**

| Code | Returns | Picture |
|---|---|---|
| `df['Name']` | A Series | One column on its own |
| `df[['Name']]` | A DataFrame | A table that happens to have one column |
| `df[['Name', 'Age']]` | A DataFrame | Several columns |

::analogy Double brackets are a list
The inner brackets are a Python **list of column names**. `df[ ['Name', 'Age'] ]` says "here is a list of the columns I want". A list asks for a table, even if the list has one item.
::
::trap `df['Name', 'Age']` fails
With one pair of brackets, Pandas looks for a single column whose name is the pair ('Name', 'Age'), and raises a KeyError. To select several columns, you need the inner list.
::
::key
- Dictionary keys become columns, and values become column data
- One bracket gives a Series, double brackets give a DataFrame
- Selecting several columns needs a list inside the brackets
- A DataFrame built from an array needs column names assigned
::

## loc, iloc and filtering rows | Slides 23-26 | must
This is the single most examined idea in the deck, and it has one simple rule:

::formula The rule
`.loc[rows, columns]` uses LABELS, end included
`.iloc[rows, columns]` uses POSITIONS, end excluded
::

Both take **rows first, then columns**. A lone `:` means "all".

::mnemonic iLoc = Integer location
The **i** stands for **integer**. No i means labels. If the code has numbers that mean position, you need the i.
::

Work through one table. Its index is the default 0, 1, 2, 3:

| | Name | Age | Salary |
|---|---|---|---|
| **0** | Alice | 25 | 40000 |
| **1** | Bob | 35 | 60000 |
| **2** | Carol | 42 | 45000 |
| **3** | Dan | 31 | 70000 |

::example Predict each result
- `df.iloc[0]` gives Alice's whole row.
- `df.iloc[:3, 1:3]` gives rows 0, 1, 2 and the columns at positions 1, 2, so **Age and Salary for Alice, Bob and Carol**.
- `df.loc[:, ['Name', 'Age']]` gives all rows, two named columns.
- `df.loc[0:2, 'Name']` gives **Alice, Bob and Carol**. Three rows, because with loc the end is included, even though these labels happen to be numbers.
- `df.iloc[0:2, 0]` gives **Alice and Bob**. Two rows, because iloc excludes the end.
::

### Filtering with conditions
A condition such as `df['Age'] > 30` produces a column of True and False. Passing it back into the table keeps only the True rows.

::steps How df[(df['Age'] > 30) & (df['Salary'] > 50000)] runs
Pandas computes `df['Age'] > 30`, giving False, True, True, True.
It computes `df['Salary'] > 50000`, giving False, True, False, True.
`&` combines them row by row, giving False, True, False, True.
Rows where the result is True are kept: **Bob and Dan**.
::
::trap Three filter errors
1. Use `&` and `|`, not the words `and` and `or`.
2. Put **parentheses around every condition**, because `&` binds more tightly than `>`.
3. For a condition inside loc, keep rows first: `df.loc[df['Age'] > 25]`.
::
::check Write the code to get the Name column of everyone under 30 using loc.
`df.loc[df['Age'] < 30, 'Name']`. The condition goes in the rows slot and the column label goes in the columns slot.
::
::key
- loc uses labels and includes the end
- iloc uses integer positions and excludes the end
- Both take rows first, then columns
- Filter with `&` for AND and `|` for OR, with parentheses around each condition
::

## Reading data into Pandas | Slides 28-38 | must
Every source has a function named `pd.read_something`. You learn one pattern and then just the special parameters.

| Source | Function | Parameters from the slides |
|---|---|---|
| CSV | `pd.read_csv('f.csv')` | `sep`, `header`, `index_col`, `usecols` |
| Excel | `pd.read_excel('f.xlsx')` | `sheet_name`, `skiprows`, `usecols`; needs `openpyxl` or `xlrd` |
| SQL | `pd.read_sql(query, conn)` | a connection, plus `params` for safe queries |
| JSON | `pd.read_json('f.json')` | `orient`, `lines` |

What each key parameter means:

- **`sep`** is the delimiter. Tab-separated file? `sep='\t'`.
- **`header`** says which row holds the column names. `header=None` means there is no header row.
- **`index_col`** turns a column into the row labels.
- **`usecols`** loads only the columns you name, which saves memory.
- **`sheet_name=None`** reads every sheet and returns a dictionary of DataFrames.

### JSON's three shapes
The `orient` parameter tells Pandas how the file is laid out. Look at the *outermost* symbol:

| Shape | The file looks like | Setting |
|---|---|---|
| List of rows | `[ {"a":1}, {"a":2} ]` | `orient='records'` |
| Dictionary of rows | `{ "row1": {"a":1} }` | `orient='index'` |
| One object per line | `{"a":1}` newline `{"a":2}` | `lines=True` |

::mnemonic Records are a list
A **record** collection is a **list** of rows, so it starts with a square bracket. An **index** is a lookup, so it starts with a curly brace, the same as a dictionary.
::
::says Slide 35 | "records: List of dictionaries (default format)"
Treat this as the slide's teaching default. In the real library, the default for a DataFrame is `orient='columns'`, which is also what slide 51 says for exporting. If a question quotes the slide, answer records. If you are writing code, set `orient` explicitly and the difference disappears.
::
::tip Reading from SQL safely
Pass user values through `params`, as in `pd.read_sql(query, conn, params=[30])`. Do not paste them into the query string. That habit prevents SQL injection, which you meet in security courses.
::
::key
- Each format has its own read function: read_csv, read_excel, read_sql, read_json
- sep sets the delimiter, header picks the header row, usecols limits columns
- sheet_name=None returns all sheets as a dictionary
- read_sql needs a database connection
- orient describes JSON's layout, and lines=True reads one object per line
::

## Exporting data | Slides 40-56 | know
Exporting mirrors reading: each `pd.read_x` has a `df.to_x`. Notice the difference: reading is called on `pd`, while writing is called on your DataFrame.

| Target | Call | Best for (slide 56) |
|---|---|---|
| CSV | `df.to_csv('out.csv', index=False)` | Sharing plain raw data |
| Excel | `df.to_excel('out.xlsx', sheet_name='S1')` | Reports with sheets and formats |
| SQL | `df.to_sql('table', conn, if_exists='append')` | Saving for later querying |
| JSON | `df.to_json('out.json', orient='records')` | Web and streaming use |

The one that matters most is **`index=False`**. Without it, the row numbers are saved as an extra column, and when you read the file back you get a mystery column called `Unnamed: 0`.

For SQL, `if_exists` answers "the table is already there, now what?":

| Value | Effect | Memory hook |
|---|---|---|
| `'fail'` | Raises an error (the default) | Stop and shout |
| `'replace'` | Drops the table, recreates it, inserts | Bulldoze and rebuild |
| `'append'` | Adds rows to the table | Add to the end |

`method='multi'` sends many rows in one INSERT instead of one statement per row. `chunksize=500` writes 500 rows at a time, so a huge table does not exhaust memory.

::trap `replace` deletes the old table
It is not "update matching rows". The old table is dropped entirely. If a question asks how to add this month's data to last month's, the answer is `append`.
::
::tip Small print worth one mark
`force_ascii=False` lets non-English characters such as Arabic appear as they are in the JSON. Otherwise they are escaped. `date_format='iso'` writes readable dates and `'epoch'` writes UNIX timestamps. Slide 42's `line_terminator` is spelled `lineterminator` in newer Pandas.
::
::key
- Reading is `pd.read_x`, writing is `df.to_x`
- index=False stops the row labels being saved as a column
- if_exists is fail, replace or append
- chunksize writes in batches for large data
- CSV for sharing, Excel for reports, SQL for querying
::

## File paths and URLs | Slides 58-61 | skim
A file location can be relative (from the current folder) or absolute (from the top of the disk). Use `os` or the more modern `pathlib` so your code works on Windows and Mac, since they write paths differently.

`read_csv`, `read_excel` and `read_json` all accept a **URL** directly. When a site needs a login, or for an API, fetch it first with `requests`, then build the DataFrame from the response: `pd.DataFrame(response.json())`. Cloud files such as S3 need extra libraries like `s3fs`.

::key
- Use os or pathlib for paths that work on every operating system
- read_csv, read_excel and read_json accept URLs
- Use requests first when a URL needs authentication or is an API
::

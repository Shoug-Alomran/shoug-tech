@head Chapter 7.2
@title Dimensionality Reduction with PCA
@sources chapter-7-2-dimensionality-reduction-with-pca
@count 39
@tldr PCA finds new axes that capture the most spread in the data, then keeps only the top few, so you lose many columns but little information.
@why PCA looks intimidating because it mentions eigenvectors, but it follows a fixed recipe of five steps. Learn the recipe and what each step is for and you can answer almost any question on it, including the numerical one on projecting a data point.
@connect It needs Chapter 7.1's dot products and Normalization's standardization. Chapter 7.3 introduces t-SNE as the non-linear alternative.
@goals
- Explain why fewer features can be better
- List the five steps of PCA in order
- Read a covariance matrix
- Explain what eigenvalues and eigenvectors mean here
- Project a point and calculate explained variance
@vocab
Variance | How spread out one feature is.
Covariance | How two features move together.
Eigenvector | A direction that a matrix only stretches, without turning.
Eigenvalue | How much that direction is stretched.
Principal component | One of the new axes.
Projection | A point's shadow on an axis.
@map
3-5 | Motivation | SKIM | The students example
6-9 | Standardize and covariance | WRITE | Formulas and meaning
11-16 | Eigen background | MEMORIZE | The four eigenvalue cases
17-23 | Decomposition and sorting | WRITE | argsort code and reading results
26-34 | Projection | WRITE | Compute one student's PC1
37-39 | Is it representative? | MEMORIZE | Variance as information

## Why reduce dimensions at all? | Slides 3-5 | know
Take students' scores in Maths, Physics and Chemistry. They tend to move together: strong in one usually means strong in the others. Three columns are carrying roughly **one** piece of information, general science ability. Why keep all three?

Dimensionality reduction creates **new features from the old ones**, keeping the most useful and discarding the rest.

::analogy Photographing a teapot
A photo turns a 3-D teapot into 2-D. Shoot it from the side and you can still see that it's a teapot. Shoot it from directly above and you see a circle. PCA finds **the best camera angle**: the direction that keeps the most detail.
::

As the handwriting on slide 3 puts it, choosing the most useful new axis means losing the least information.

::trap PCA doesn't pick existing columns
PCA does **not** select Maths and drop Physics. Each new component is a **blend** of all original features. Selecting columns is called feature selection, and it's different.
::
::key
- Dimensionality reduction builds a smaller set of new features
- Correlated columns carry overlapping information
- Each principal component is a combination of all original features
::

## The five-step recipe | Slides 6-33 | must
::steps PCA in order
**Standardize** each feature to mean 0 and standard deviation 1.
**Compute the covariance matrix** to see which features move together.
**Decompose** it into eigenvalues and eigenvectors.
**Sort** them by eigenvalue, largest first, and keep the top k.
**Project** the data onto those k eigenvectors.
::
::mnemonic Some Clever Dogs Sniff Paths
**S**tandardize, **C**ovariance, **D**ecompose, **S**ort, **P**roject. The order is fixed, so the sentence keeps it.
::

### Step 1: Standardize
z = (x − mean) / standard deviation. Without this, a column with large numbers would dominate the variance just because of its units.

### Step 2: The covariance matrix
::formula Covariance between X and Y
cov(X, Y) = Σ (x<sub>i</sub> − x̄)(y<sub>i</sub> − ȳ) / (n − 1)
::
::example Compute one covariance
X = 1, 2, 3 and Y = 2, 4, 6. Means are 2 and 4.

Products of deviations: (−1)(−2) + (0)(0) + (1)(2) = 4. Divide by n − 1 = 2: **cov = 2**. Positive, so they rise together.
::

The matrix is **square**, with one row and one column per feature. Its **diagonal holds each feature's variance**, and off-diagonal entries hold the covariances. On standardized data, values near 1 show strong relationships.

::trap `np.cov` expects variables in rows
Pandas stores features in columns. That's why the slide's code transposes first: `np.cov(X.T)`.
::

### Step 3: Eigenvalues and eigenvectors
Most vectors get rotated when a matrix multiplies them. An **eigenvector** only gets stretched, keeping its direction. The stretch factor is its **eigenvalue**.

::formula Defining equation
A v = λ v
::

| Eigenvalue λ | Effect on the vector |
|---|---|
| Above 1 | Stretches |
| Between 0 and 1 | Compresses |
| Negative | Flips |
| Zero | Collapses it |

::example A scaling matrix
S = diag(2, 3). Then S[1, 0] = [2, 0] and S[0, 1] = [0, 3]. Neither vector changes direction, so both are eigenvectors, with eigenvalues 2 and 3.
::

For a covariance matrix, the meaning is simple: **an eigenvector is a direction, and its eigenvalue is how much of the data's variance lies along it.**

### Step 4: Sort
::code python
idx = np.argsort(eigvals)[::-1]      # argsort is ascending, [::-1] reverses
eigvals = eigvals[idx]
eigvecs = eigvecs[:, idx]            # reorder the columns too
::

Slide 22: eigenvalues [1.01, 1.6, 3.61, 2.5] sorted descending give the index list **[2, 3, 1, 0]**, so the eigenvectors must be reordered to vect3, vect4, vect2, vect1.

### Step 5: Project
Each new coordinate is a dot product of the row with an eigenvector.

::example Projecting one student (illustrative numbers)
A standardized row is [1.2, 0.8, 1.0] and the first eigenvector is [0.58, 0.58, 0.57].

PC1 = 1.2(0.58) + 0.8(0.58) + 1.0(0.57) = 0.696 + 0.464 + 0.57 = **1.73**.

Three subject scores have become one number.
::
::key
- Five steps: standardize, covariance, decompose, sort, project
- Covariance matrix is square, and its diagonal holds the variances
- Eigenvectors give direction, and eigenvalues give the amount of variance
- argsort sorts ascending, so [::-1] reverses to descending
- Each principal component score is a dot product with an eigenvector
::

## How many components, and is it trustworthy? | Slides 37-39 | must
PCA treats **variance as information**. If a direction has almost no spread, every point looks the same along it, so dropping it costs little.

::formula Explained variance ratio
Share of component i = λ<sub>i</sub> / (λ<sub>1</sub> + λ<sub>2</sub> + ... + λ<sub>n</sub>)
::
::example Using slide 22's eigenvalues: 3.61, 2.5, 1.6, 1.01
Total = 8.72.

- PC1 explains 3.61 / 8.72 = **41.4%**
- PC1 and PC2 together: 6.11 / 8.72 = **70.1%**
- Adding PC3: 7.71 / 8.72 = **88.4%**

If you need at least 85%, keep three components.
::
::tip Components are uncorrelated
By construction, principal components share no covariance. That removes the overlap you started with.
::
::trap Largest variance isn't always what matters
PCA is unsupervised and ignores the target. A low-variance direction could still be the one that predicts your label. PCA also finds only straight-line structure, which is what motivates t-SNE.
::
::key
- PCA treats variance as information
- Explained variance ratio = eigenvalue ÷ sum of all eigenvalues
- Use the explained variance ratio to justify how many components to keep
- Principal components are uncorrelated with each other
::

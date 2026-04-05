# Expectation, Variance, Covariance, and Independence

This section groups the main summary statistics and dependence concepts into one coherent block.

## Expectation

The expectation is the probability-weighted average of the variable's possible values:

$$
\mathbb{E}[X]=\sum_x x\,p(x)
$$

for a discrete variable.

Expectation is **not** the most likely next outcome. It is the long-run average, or center of mass, of the distribution.

### Bernoulli example

If

$$
p(X=0)=0.7, \qquad p(X=1)=0.3,
$$

then

$$
\mathbb{E}[X]=0\cdot 0.7 + 1\cdot 0.3 = 0.3.
$$

### Die example

For a fair die,

$$
\mathbb{E}[X]=\sum_{x=1}^6 x\cdot \frac{1}{6}=\frac{1+2+3+4+5+6}{6}=3.5.
$$

A die never lands on `3.5`, but `3.5` is still the mean.

## Linearity of expectation

For constants `a, b, c`,

$$
\mathbb{E}[aX+bY+c]=a\mathbb{E}[X]+b\mathbb{E}[Y]+c.
$$

No independence assumption is required.

That point matters. Many later formulas do need independence, but linearity of expectation does not.

### Dependent example

Let `X` be Bernoulli with

$$
p(X=1)=0.3, \qquad p(X=0)=0.7,
$$

and define

$$
Y=1-X.
$$

Then `X` and `Y` are completely dependent. Once `X` is known, `Y` is forced.

Yet

$$
\mathbb{E}[X+Y]=\mathbb{E}[1]=1,
$$

and also

$$
\mathbb{E}[X]+\mathbb{E}[Y]=0.3+0.7=1.
$$

### Indicator counting trick

If `H_1, H_2, H_3` are indicator variables for whether three coin flips are heads, and

$$
N=H_1+H_2+H_3,
$$

then

$$
\mathbb{E}[N]=\mathbb{E}[H_1]+\mathbb{E}[H_2]+\mathbb{E}[H_3].
$$

If each flip has head probability `\rho`, then each indicator has mean `\rho`, so

$$
\mathbb{E}[N]=3\rho.
$$

This is why indicator decompositions are so powerful: they let you compute expectations of complicated counts by splitting them into simpler pieces.

## Variance

Variance measures spread around the mean:

$$
\mathrm{Var}(X)=\mathbb{E}[(X-\mathbb{E}[X])^2].
$$

Expanding the square gives the useful identity

$$
\mathrm{Var}(X)=\mathbb{E}[X^2]-\mathbb{E}[X]^2.
$$

### Bernoulli variance

If `X \in \{0,1\}` with `p(X=1)=\rho`, then `X^2=X`, so

$$
\mathbb{E}[X]=\rho, \qquad \mathbb{E}[X^2]=\rho.
$$

Therefore

$$
\mathrm{Var}(X)=\rho-\rho^2=\rho(1-\rho).
$$

The spread is largest near `\rho=1/2` and shrinks to zero near `0` or `1`.

## Covariance and correlation

For two variables,

$$
\mathrm{Cov}(X,Y)=\mathbb{E}[(X-\mathbb{E}[X])(Y-\mathbb{E}[Y])].
$$

The normalized version is correlation:

$$
\mathrm{Corr}(X,Y)=\frac{\mathrm{Cov}(X,Y)}{\sqrt{\mathrm{Var}(X)\mathrm{Var}(Y)}}.
$$

Under affine transformations,

$$
\mathrm{Var}(aX+b)=a^2\mathrm{Var}(X),
$$

and

$$
\mathrm{Cov}(aX+b,cY+d)=ac\,\mathrm{Cov}(X,Y).
$$

So:

- adding a constant shifts location but not spread;
- multiplying by `a` rescales spread by `a^2`;
- covariance tracks whether centered values tend to move together or in opposite directions.

## Mean and variance are different summaries

Let `X` be constant at `3`, and let `Y` equal `0` or `6` with probabilities `1/2` and `1/2`.

Then

$$
\mathbb{E}[X]=3, \qquad \mathbb{E}[Y]=3.
$$

But

$$
\mathrm{Var}(X)=0,
$$

while

$$
\mathrm{Var}(Y)=\left(0^2\cdot \frac12 + 6^2\cdot \frac12\right)-3^2 = 18-9=9.
$$

So two distributions can share the same mean and still differ sharply in spread.

## Zero covariance does not imply independence

Let `X` take values `-1, 0, 1` with equal probability and define

$$
Y=X^2.
$$

Then `Y` is completely determined by `X`, so the variables are dependent.

But

$$
\mathbb{E}[X]=0, \qquad \mathbb{E}[XY]=\mathbb{E}[X^3]=0,
$$

which gives

$$
\mathrm{Cov}(X,Y)=0.
$$

So covariance only captures linear dependence in centered variables. It does not detect every kind of dependence.

## Independence

Two random variables are independent if

$$
p(X=x,Y=y)=p(X=x)p(Y=y)
$$

for every pair of values `x,y`.

Equivalently,

$$
p(X=x \mid Y=y)=p(X=x)
$$

for every `y` with `p(Y=y)>0`.

These are the same statement written in two forms.

- The factorization form says the joint table splits into a product of marginals.
- The conditional form says observing `Y` does not change the distribution of `X`.

## Degrees of freedom under independence

Suppose `X` and `Y` are both `d`-ary.

A general joint table `p(X,Y)` has `d^2` entries subject to one normalization constraint, so it has

$$
d^2-1
$$

degrees of freedom.

Under independence,

$$
p(X,Y)=p(X)p(Y).
$$

Now only the two marginal tables need to be chosen. Each marginal has `d-1` degrees of freedom, so the independent model has

$$
(d-1)+(d-1)=2d-2
$$

degrees of freedom.

That reduction is one of the main reasons independence assumptions are attractive in AI and machine learning: they make the model smaller and easier to estimate. The cost is that independence is a strong structural claim.

## Small independence example

Let

$$
p(X=0)=0.7, \qquad p(X=1)=0.3,
$$

and

$$
p(Y=1)=0.2, \quad p(Y=2)=0.3, \quad p(Y=3)=0.4, \quad p(Y=4)=0.1.
$$

If `X` and `Y` are independent, then every joint entry is the product of one marginal from `X` and one marginal from `Y`.

For example,

$$
p(X=1,Y=2)=p(X=1)p(Y=2)=0.3\cdot 0.3=0.09.
$$

So independence is a precise table factorization rule, not just a vague statement that the variables are "unrelated."

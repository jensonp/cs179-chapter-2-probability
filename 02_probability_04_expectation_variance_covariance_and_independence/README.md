# Expectation, Variance, Covariance, and Independence

This section collects four ideas that are easy to memorize separately but much more useful when read as one chain.

- **Expectation** answers: where is the distribution centered on average?
- **Variance** answers: how concentrated or spread out is it around that center?
- **Covariance** answers: when two variables are viewed relative to their own means, do they tend to move together, in opposite directions, or with no clear linear pattern?
- **Independence** answers: does the full joint distribution really split into separate marginal pieces, or is there still interaction left after all?

That order matters. We usually ask first for a typical location, then for uncertainty around that location, then for how several variables move jointly, and finally for whether the joint law has a factorized structure that simplifies modeling.

## Expectation

For a discrete random variable, the expectation is the probability-weighted average of its possible values:

$$
\mathbb{E}[X] = \sum_x x\,p(x).
$$

This should not be read as “the next observed value.” It should be read as the long-run average or center of mass of the distribution. A random variable can easily have an expectation that is not itself a likely outcome, or even an attainable one.

### Bernoulli example

If

$$
p(X=0)=0.7,\qquad p(X=1)=0.3,
$$

then

$$
\mathbb{E}[X] = 0\cdot 0.7 + 1\cdot 0.3 = 0.3.
$$

This makes sense because a Bernoulli variable records success as $1$ and failure as $0$, so its mean is exactly the success probability.

### Die example

For a fair die,

$$
\mathbb{E}[X]=\sum_{x=1}^{6} x\cdot \frac16=\frac{1+2+3+4+5+6}{6}=3.5.
$$

A die never lands on $3.5$. The point of expectation is not to predict the next face exactly. The point is to summarize the balance point of the whole distribution. If you average many independent die rolls, that average drifts toward $3.5$.

## Linearity of expectation

One of the most useful identities in probability is

$$
\mathbb{E}[aX+bY+c]=a\mathbb{E}[X]+b\mathbb{E}[Y]+c.
$$

The key fact is that **no independence assumption is required**. That makes linearity of expectation unusually powerful. It lets us analyze totals, counts, and aggregate scores without first solving the full dependence structure.

### Dependent example

Let $X$ be Bernoulli with

$$
p(X=1)=0.3,\qquad p(X=0)=0.7,
$$

and define

$$
Y=1-X.
$$

Then $X$ and $Y$ are completely dependent: once one is known, the other is forced. But linearity still gives

$$
\mathbb{E}[X+Y]=\mathbb{E}[1]=1,
$$

while separately

$$
\mathbb{E}[X]+\mathbb{E}[Y]=0.3+0.7=1.
$$

So linearity is not a statement about independence. It is a structural property of expectation itself.

### Indicator counting trick

Indicator variables turn counting problems into expectation problems. If $H_1,H_2,H_3$ indicate whether three flips are heads, and

$$
N=H_1+H_2+H_3,
$$

then

$$
\mathbb{E}[N]=\mathbb{E}[H_1]+\mathbb{E}[H_2]+\mathbb{E}[H_3].
$$

If each flip has head probability $\rho$, then each indicator has mean $\rho$, so

$$
\mathbb{E}[N]=3\rho.
$$

This is the deeper reason indicator decompositions show up everywhere in probability and machine learning. Complicated counts are often easy to **expect**, even when their full distributions are hard to derive.

## Variance

Expectation tells us the center of a distribution, but it says nothing about how tightly values cluster around that center. Variance answers that second question:

$$
\mathrm{Var}(X)=\mathbb{E}\!\left[(X-\mathbb{E}[X])^2\right].
$$

The square matters. It makes all deviations nonnegative and penalizes larger deviations more heavily. Variance is therefore a summary of spread around the mean, not just another kind of average.

Expanding the square gives the useful identity

$$
\mathrm{Var}(X)=\mathbb{E}[X^2]-\mathbb{E}[X]^2.
$$

That identity is often much easier to compute from a table than the definition itself.

### Bernoulli variance

If $X\in\{0,1\}$ with $p(X=1)=\rho$, then $X^2=X$, so

$$
\mathbb{E}[X]=\rho,\qquad \mathbb{E}[X^2]=\rho.
$$

Therefore

$$
\mathrm{Var}(X)=\rho-\rho^2=\rho(1-\rho).
$$

This formula is worth interpreting, not just memorizing. The variance is largest near $\rho=\tfrac12$, where outcomes are most uncertain, and shrinks toward $0$ as $\rho$ approaches $0$ or $1$, where the variable becomes nearly deterministic.

## Mean and variance are different summaries

Two distributions can share the same expectation and still behave very differently. Let $X$ be constant at $3$, and let $Y$ equal $0$ or $6$ with probabilities $\tfrac12$ and $\tfrac12$. Then

$$
\mathbb{E}[X]=3,\qquad \mathbb{E}[Y]=3,
$$

but

$$
\mathrm{Var}(X)=0,
$$

while

$$
\mathrm{Var}(Y)=\left(0^2\cdot \frac12+6^2\cdot \frac12\right)-3^2=18-9=9.
$$

The two variables have the same center and very different spread. This is why mean and variance are paired so often: one measures location, the other measures dispersion.

## Covariance and correlation

Once we move from one variable to two, the next question is no longer just “where is each one centered?” It becomes “how do they vary together?”

Covariance answers that question by centering each variable first and then multiplying the deviations:

$$
\mathrm{Cov}(X,Y)=\mathbb{E}\!\left[(X-\mathbb{E}[X])(Y-\mathbb{E}[Y])\right].
$$

This is a statement about **joint movement relative to each variable’s own mean**.

- If $X$ tends to be above its mean when $Y$ is above its mean, and below when $Y$ is below, covariance is positive.
- If one tends to be above its mean when the other is below, covariance is negative.
- If those centered movements show no systematic linear pattern, covariance may be near zero.

A scale-free version is the correlation:

$$
\mathrm{Corr}(X,Y)=\frac{\mathrm{Cov}(X,Y)}{\sqrt{\mathrm{Var}(X)\mathrm{Var}(Y)}}.
$$

Correlation is useful because covariance depends on units, while correlation normalizes by the variables’ standard deviations and makes values comparable across scales.

### Affine transformations

Under affine transformations,

$$
\mathrm{Var}(aX+b)=a^2\mathrm{Var}(X),
$$

and

$$
\mathrm{Cov}(aX+b,cY+d)=ac\,\mathrm{Cov}(X,Y).
$$

These identities clarify the roles of shifting and scaling:

- adding a constant changes location but not spread;
- multiplying by $a$ rescales spread by $a^2$;
- covariance tracks joint variation after centering, and its sign flips if one variable is multiplied by a negative constant.

## Zero covariance does not imply independence

This is one of the most important conceptual warnings in the section.

Let $X$ take values $-1,0,1$ with equal probability and define

$$
Y=X^2.
$$

Then $Y$ is completely determined by $X$, so the variables are certainly dependent. But

$$
\mathbb{E}[X]=0,\qquad \mathbb{E}[XY]=\mathbb{E}[X^3]=0,
$$

so

$$
\mathrm{Cov}(X,Y)=0.
$$

What happened? Covariance only detects **linear dependence in centered variables**. The relationship $Y=X^2$ is nonlinear and symmetric around $0$, so the positive and negative contributions cancel. This is why “uncorrelated” is weaker than “independent.”

## Independence

Two random variables are independent if

$$
p(X=x,Y=y)=p(X=x)\,p(Y=y)
$$

for every pair of values $x,y$.

Equivalently,

$$
p(X=x\mid Y=y)=p(X=x)
$$

for every $y$ with $p(Y=y)>0$.

These are the same structural claim written in two different ways.

- The **factorization form** says the joint table splits into a product of marginals.
- The **conditional form** says learning $Y$ does not change the distribution of $X$.

The key point is that independence is not just “weak relationship.” It is a full statement that the joint distribution contains no interaction beyond the marginals.

### Small independence example

Let

$$
p(X=0)=0.7,\qquad p(X=1)=0.3,
$$

and

$$
p(Y=1)=0.2,\quad p(Y=2)=0.3,\quad p(Y=3)=0.4,\quad p(Y=4)=0.1.
$$

If $X$ and $Y$ are independent, then every joint entry is the product of one marginal from $X$ and one marginal from $Y$. For example,

$$
p(X=1,Y=2)=p(X=1)p(Y=2)=0.3\cdot 0.3=0.09.
$$

So independence is a precise table factorization rule, not a vague statement that variables are “unrelated.”

## Degrees of freedom under independence

Suppose $X$ and $Y$ are both $d$-ary.

A completely general joint table $p(X,Y)$ has $d^2$ entries, but one normalization constraint removes one degree of freedom, so the unrestricted joint model has

$$
d^2-1
$$

degrees of freedom.

Under independence,

$$
p(X,Y)=p(X)p(Y).
$$

Now we only need to specify the two marginals. Each marginal has $d-1$ degrees of freedom, so the independent model has

$$
(d-1)+(d-1)=2d-2
$$

degrees of freedom.

That reduction is why independence assumptions are so attractive in AI and machine learning: they can dramatically shrink the size of the model. But the price is that independence is a strong claim. If it is false, the simplification may destroy important structure.

## Conditional independence

Sometimes two variables are dependent marginally but become independent after conditioning on a third variable. We write

$$
X \perp Y \mid Z
$$

to mean that once $Z$ is known, the remaining uncertainty in $X$ and $Y$ factorizes:

$$
p(X,Y\mid Z)=p(X\mid Z)p(Y\mid Z).
$$

This idea is central in graphical models, Bayesian networks, hidden-variable models, and causal reasoning. It is often the real structural simplification used in practice: not total independence, but independence after the right latent or observed variable has been conditioned on.

## Retain from this section

- Expectation summarizes center, not the next realized outcome.
- Linearity of expectation does not require independence.
- Indicator variables turn counting problems into expectation problems.
- Variance measures spread around the mean.
- Covariance measures centered co-movement, but zero covariance does not imply independence.
- Independence is a factorization property of the full joint distribution.
- Conditional independence is often the structural simplification that matters in probabilistic models.

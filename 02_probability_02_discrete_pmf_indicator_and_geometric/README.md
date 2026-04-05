# Discrete PMFs, Indicator Notation, and the Geometric Distribution

This section rewrites the discrete-distribution portion of Part 1.1 so that each object is introduced in the order a beginner actually uses it.

## PMFs are tables written as functions

Suppose a variable `X` takes values in a finite set.
A PMF assigns a probability to each state:

$$
p(X=x)=\mathbb{P}(X=x).
$$

For a three-state weather variable,

$$
p(X=\text{sun})=0.5, \qquad p(X=\text{cloud})=0.3, \qquad p(X=\text{rain})=0.2.
$$

You can read that either as a table or as a function. It is the same object in two different formats.

## A tiny PMF-to-CDF example

Let `X` take values in `\{0,1,2\}` with

$$
p(X=0)=0.2, \qquad p(X=1)=0.5, \qquad p(X=2)=0.3.
$$

Then the CDF is the running total

$$
F_X(x)=\mathbb{P}(X \le x).
$$

So

- if `x < 0`, then `F_X(x)=0`;
- if `0 \le x < 1`, then `F_X(x)=0.2`;
- if `1 \le x < 2`, then `F_X(x)=0.7`;
- if `x \ge 2`, then `F_X(x)=1`.

Now subtraction gives interval probabilities. For example,

$$
\mathbb{P}(1 < X \le 2)=F_X(2)-F_X(1)=1-0.7=0.3.
$$

That matches the point mass at `2` because in the discrete case the CDF jumps by exactly the PMF value at each state.

## Indicator notation

The indicator

$$
\mathbf{1}[X=x]
$$

equals `1` when the statement inside the brackets is true and `0` otherwise.

Indicator notation is not a new probability concept. It is a bookkeeping device that turns a logical statement into a numerical selector.

## Bernoulli distribution

A Bernoulli variable has support

$$
X \in \{0,1\}.
$$

If

$$
\mathbb{P}(X=1)=\rho,
$$

then automatically

$$
\mathbb{P}(X=0)=1-\rho.
$$

The PMF can be written as

$$
p(X)=\rho^X(1-\rho)^{1-X}.
$$

Why does this work?

- If `X=1`, the expression becomes `\rho^1(1-\rho)^0=\rho`.
- If `X=0`, the expression becomes `\rho^0(1-\rho)^1=1-\rho`.

The exponents are acting as selectors.

An equivalent indicator form is

$$
p(X)=\rho\,\mathbf{1}[X=1] + (1-\rho)\,\mathbf{1}[X=0].
$$

## Categorical distribution

If `X` takes one of `d` states, a categorical PMF is

$$
\mathbb{P}(X=i)=\rho_i, \qquad \rho_i \ge 0, \qquad \sum_{i=1}^d \rho_i = 1.
$$

The normalization constraint means only `d-1` of the `\rho_i` values are free. Once the first `d-1` are chosen, the last one is forced.

A compact product form is

$$
p(X)=\prod_{i=1}^d \rho_i^{\mathbf{1}[X=i]}.
$$

If the realized state is `i`, then exactly one indicator exponent equals `1` and all the others equal `0`. So the product keeps the probability of the realized state and turns all non-realized factors into `1`.

For the weather example,

$$
\rho_{\text{sun}}=0.5, \qquad \rho_{\text{cloud}}=0.3, \qquad \rho_{\text{rain}}=0.2.
$$

If the realized state is rain, then

$$
\mathbf{1}[X=\text{sun}]=0, \qquad \mathbf{1}[X=\text{cloud}]=0, \qquad \mathbf{1}[X=\text{rain}]=1,
$$

and the product becomes

$$
0.5^0 \cdot 0.3^0 \cdot 0.2^1 = 0.2.
$$

So the table form and the indicator-product form describe the same PMF.

## Geometric distribution

The geometric distribution requires a convention choice.

In this rewrite, `X` counts the **number of failures before the first success** in repeated independent Bernoulli trials with success probability `\rho`.

So the support is

$$
X \in \{0,1,2,\dots\},
$$

and the PMF is

$$
p(X=x)=(1-\rho)^x\rho.
$$

The event `X=x` means:

- the first `x` trials fail,
- the next trial succeeds.

Because the trials are independent, the probability is the product of those pieces.

For example, if `\rho=0.2`, then

$$
p(X=0)=0.2, \qquad p(X=1)=0.8\cdot 0.2=0.16, \qquad p(X=2)=0.8^2\cdot 0.2=0.128.
$$

Each step to the right multiplies the previous probability by `1-\rho`, so the probabilities decay geometrically.

## Mean of the geometric distribution

For a discrete variable,

$$
\mathbb{E}[X]=\sum_x x\,p(X=x).
$$

For the geometric PMF above,

$$
\mathbb{E}[X]=\sum_{x=0}^{\infty} x(1-\rho)^x\rho.
$$

Let `r=1-\rho`. Then

$$
\mathbb{E}[X]=\rho\sum_{x=0}^{\infty} xr^x.
$$

Use the geometric-series identity

$$
\sum_{x=0}^{\infty} r^x = \frac{1}{1-r}, \qquad |r|<1.
$$

Differentiate with respect to `r`:

$$
\sum_{x=1}^{\infty} xr^{x-1} = \frac{1}{(1-r)^2}.
$$

Multiply by `r`:

$$
\sum_{x=0}^{\infty} xr^x = \frac{r}{(1-r)^2}.
$$

Substitute back:

$$
\mathbb{E}[X]=\rho\cdot \frac{1-\rho}{\rho^2}=\frac{1-\rho}{\rho}.
$$

So under the zero-based convention,

$$
\mathbb{E}[X]=\frac{1-\rho}{\rho}.
$$

If `\rho=0.2`, the expected number of failures before the first success is `4`.

## The other common convention

Some texts define a geometric variable `Y` as the **number of trials until the first success**.

Then

$$
Y \in \{1,2,3,\dots\}, \qquad p(Y=y)=(1-\rho)^{y-1}\rho,
$$

and

$$
\mathbb{E}[Y]=\frac{1}{\rho}.
$$

The difference is exactly one trial, so it is essential to check which convention a library, text, or homework problem is using.

# 2.5 Information Theory

This section adds a numerical language for uncertainty and information.  
Probability distributions tell us how mass is assigned across outcomes.  
Information theory asks what that distribution implies about:

- uncertainty before observation,
- uncertainty after observation,
- mismatch between two distributions,
- and dependence between variables.

This section is written in the **discrete** setting.  
That matters.  
The formulas below are sums over outcomes, and the objects are the discrete entropy, conditional entropy, mutual information, and KL divergence.  
Continuous differential entropy is a different object and is not developed here.

A second boundary should also be fixed immediately: the logarithm base changes the **unit**, not the concept.

- base $2$: bits;
- base $e$: nats.

Everything below is easiest to interpret in bits, so $\log_2$ is the default in examples.

## Surprise

For one specific outcome $x$, the surprise is

$$
-\log p(x).
$$

This quantity has the right direction:

- if $p(x)$ is large, the surprise is small;
- if $p(x)$ is small, the surprise is large.

So surprise is the information revealed by one realized outcome.

## Entropy

Entropy is the average surprise:

$$
H[X] = -\sum_x p(x)\log p(x).
$$

This is the expected information revealed by one observation of $X$.

Entropy is large when the distribution spreads mass across many comparably plausible outcomes.  
Entropy is small when the distribution is concentrated enough that outcomes are easy to predict.

### Boundary cases

- If $X$ is deterministic, then $H[X]=0$.
- On a fixed finite support, the uniform distribution has the largest entropy.

So entropy is not just “randomness” in a vague sense.  
It is a numerical measure of uncertainty built from the outcome probabilities themselves.

## Example: fair coin and biased coin

A fair coin has

$$
H[X]
=
-0.5\log_2 0.5 - 0.5\log_2 0.5
=
1 \text{ bit}.
$$

A biased coin with probabilities $(0.9, 0.1)$ has

$$
H[X]
=
-0.9\log_2 0.9 - 0.1\log_2 0.1
\approx 0.47 \text{ bits}.
$$

The biased coin is more predictable, so it carries less uncertainty per flip.

## Example: rare lottery notification

Suppose a binary variable equals $1$ only on a winning day and $0$ otherwise, with

$$
p(X=1)=0.001,
\qquad
p(X=0)=0.999.
$$

Then

$$
H[X]
=
-0.999\log_2 0.999
-
0.001\log_2 0.001
\approx 0.011 \text{ bits}.
$$

That number is tiny because almost every symbol is the same.  
This is the compression interpretation of entropy: long sequences generated from highly predictable sources can be encoded using much less than one bit per symbol on average.

## Conditional entropy

Conditional entropy measures the uncertainty left in one variable after another variable is revealed.

It can be written as

$$
H[X \mid Y]
=
\sum_y p(y)\,H[X \mid Y=y],
$$

or equivalently,

$$
H[X \mid Y]
=
H[X,Y]-H[Y].
$$

The average form should be read first.  
It says:

1. for each possible value $y$, compute the entropy of the conditional law of $X$;
2. average those entropies using $p(y)$.

So conditional entropy is not the uncertainty left after one particular observed value.  
It is the **average** uncertainty left after the conditioning variable is revealed.

A central theorem is

$$
H[X \mid Y] \le H[X].
$$

Observation cannot increase uncertainty on average.

## Mutual information

Mutual information measures how much uncertainty about one variable is removed by observing the other.

The cleanest operational identity is

$$
I[X;Y] = H[X] - H[X \mid Y].
$$

So mutual information is the reduction in uncertainty about $X$ caused by revealing $Y$.

It is symmetric, so the same quantity also equals

$$
I[X;Y] = H[Y] - H[Y \mid X].
$$

Another exact identity is

$$
I[X;Y] = H[X] + H[Y] - H[X,Y].
$$

This says the shared information is the amount by which the total separate uncertainty exceeds the joint uncertainty.

### KL interpretation of mutual information

Mutual information can also be written as a KL divergence:

$$
I[X;Y]
=
D\!\bigl(p(x,y)\,\|\,p(x)p(y)\bigr).
$$

This form says mutual information is the penalty for pretending the joint distribution factorizes when it actually does not.

That identity is powerful, but it should be read **after** the uncertainty-reduction identity, not before it.  
The uncertainty-reduction view is the clearer first-principles interpretation.

### Boundary cases

- If $X$ and $Y$ are independent, then $p(x,y)=p(x)p(y)$, so $I[X;Y]=0$.
- If $Y=X$ exactly, then $H[X \mid Y]=0$, so $I[X;Y]=H[X]$.

## Example: commute choice and weather

Let commute choice $C$ take values in $\{\text{walk}, \text{bike}, \text{drive}\}$, and let weather $R$ take values in $\{\text{clear}, \text{rain}\}$.

Assume

$$
p(R=\text{clear})=0.9,
\qquad
p(R=\text{rain})=0.1.
$$

Suppose the conditional commute distributions are:

- given clear weather: $(0.9, 0.1, 0)$ for walk, bike, drive;
- given rain: $(0.5, 0, 0.5)$.

The conditional entropies are

$$
H[C \mid R=\text{clear}]
=
-0.9\log_2 0.9 - 0.1\log_2 0.1
\approx 0.47,
$$

$$
H[C \mid R=\text{rain}]
=
-0.5\log_2 0.5 - 0.5\log_2 0.5
=
1.
$$

Averaging with the weather probabilities gives

$$
H[C \mid R]
=
0.9(0.47)+0.1(1)
\approx 0.52 \text{ bits}.
$$

From the marginal commute distribution one obtains

$$
H[C] \approx 0.72 \text{ bits}.
$$

So the mutual information is

$$
I[C;R]
=
H[C]-H[C \mid R]
\approx 0.72 - 0.52
\approx 0.20 \text{ bits}.
$$

Interpretation:

- weather is informative about commuting;
- but it does not determine commuting completely;
- so the mutual information is positive but modest.

## KL divergence

Entropy measures uncertainty inside one distribution.  
KL divergence measures mismatch between two distributions.

For discrete distributions $p$ and $q$,

$$
D(p \,\|\, q)
=
\sum_x p(x)\log\!\left(\frac{p(x)}{q(x)}\right).
$$

This should be read in order:

- $p$ is the reference or target distribution;
- $q$ is the approximating distribution;
- the log-ratio compares how the two distributions score the same outcome;
- the average is taken with respect to $p$, so outcomes important under $p$ receive the weight.

### The support condition comes first

Before numerical examples, the domain restriction must be fixed:

If there exists an outcome $x$ such that

$$
p(x)>0
\quad\text{and}\quad
q(x)=0,
$$

then

$$
D(p \,\|\, q)=\infty.
$$

This is not a technicality.  
It means the approximating distribution is declaring an actually possible event impossible.

### Core facts

KL divergence satisfies

$$
D(p \,\|\, q)\ge 0,
$$

with equality only when $p=q$.

But KL divergence is **not symmetric**:

$$
D(p \,\|\, q)\ne D(q \,\|\, p)
$$

in general.

So KL divergence is a directed discrepancy, not an ordinary distance.

Another subtle point is that the individual summands

$$
p(x)\log\!\left(\frac{p(x)}{q(x)}\right)
$$

need not all be positive.  
Nonnegativity appears only after the weighted sum is taken.

## Example: two-state KL divergence

Let

$$
p=(0.8,0.2),
\qquad
q=(0.5,0.5).
$$

Then

$$
D(p \,\|\, q)
=
0.8\log\!\left(\frac{0.8}{0.5}\right)
+
0.2\log\!\left(\frac{0.2}{0.5}\right).
$$

The first contribution is positive because $q$ underweights the more likely event under $p$.  
The second contribution is negative because $q$ overweights the less likely event.  
After summing, the total remains positive.

If the order is reversed, the answer changes.  
That is exactly what “directed discrepancy” means.

## Retain from 2.5

- Surprise is information in one realized outcome.
- Entropy is average surprise.
- Conditional entropy is average remaining uncertainty after observation.
- Mutual information is uncertainty reduction, and also the KL divergence from the true joint law to the independence model.
- KL divergence is a directed discrepancy with a support condition.

## Do not confuse in 2.5

- Do not confuse entropy with variance or geometric spread.
- Do not confuse conditional entropy at one value of $Y$ with the average quantity $H[X \mid Y]$.
- Do not confuse mutual information with a generic correlation score; it measures uncertainty reduction.
- Do not confuse KL divergence with a symmetric distance.

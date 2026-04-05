# 2.5 Information Theory

Probability tells us how mass is distributed over outcomes. Information theory asks what that distribution implies about uncertainty, informativeness, mismatch, and dependence.

This section is written in the **discrete** setting. That boundary matters.

All formulas here are sums over outcomes. Continuous differential entropy is a different object with different behavior and is not the topic of this section. A second boundary should also be fixed immediately: the logarithm base changes the **unit**, not the concept.

- base $2$: bits;
- base $e$: nats.

Everything below is easiest to interpret in bits, so $\log_2$ is the default in examples.

There are four main objects to keep straight:

- **entropy**: uncertainty inside one distribution;
- **conditional entropy**: uncertainty left after another variable is revealed;
- **mutual information**: uncertainty removed by that revelation;
- **KL divergence**: directed mismatch between two distributions.

That order is the cleanest first-principles order, because each object answers the next question raised by the one before it.

## Surprise

For one realized outcome $x$, the surprise is

$$
-\log p(x).
$$

This is the information revealed by that one event.

The direction is exactly what we want:

- if $p(x)$ is large, then $x$ was already expected, so the surprise is small;
- if $p(x)$ is small, then $x$ was hard to predict, so the surprise is large.

This is not just a mnemonic. The logarithm turns products of probabilities into sums, which is why information measures add naturally across independent observations.

### Tiny examples

If $p(x)=1/2$, then the surprise is

$$
-\log_2(1/2)=1
$$

bit.

If $p(x)=1/8$, then the surprise is

$$
-\log_2(1/8)=3
$$

bits.

So rarer events carry larger information content when they occur.

## Entropy

Entropy is the average surprise:

$$
H[X] = -\sum_x p(x)\log p(x).
$$

This is the expected information revealed by one observation of $X$.

That sentence should be read carefully. Entropy is not “how surprising one special event is.” It is the average uncertainty built from the whole distribution.

### What entropy measures

Entropy is large when mass is spread across many comparably plausible outcomes. Entropy is small when the distribution is concentrated enough that outcomes are fairly predictable.

So entropy is not vague “randomness.” It is a numerical summary of uncertainty derived from the probabilities themselves.

### Boundary cases

Two edge cases are worth fixing immediately.

- If $X$ is deterministic, then $H[X]=0$.
- On a fixed finite support, the uniform distribution has maximal entropy.

These are not separate facts to memorize. They are exactly what the “average surprise” interpretation predicts.

### Fair coin versus biased coin

A fair coin has

$$ H[X] = -0.5\log_2 0.5 - 0.5\log_2 0.5 = 1 \text{ bit}. $$

A biased coin with probabilities $(0.9,0.1)$ has

$$ H[X] = -0.9\log_2 0.9 - 0.1\log_2 0.1 \approx 0.47 \text{ bits}. $$

The biased coin is more predictable, so it carries less uncertainty per flip.

### Rare notification example

Suppose a binary variable equals $1$ only on a winning day and $0$ otherwise:

$$
p(X=1)=0.001,\qquad p(X=0)=0.999.
$$

Then

$$ H[X] = -0.999\log_2 0.999 - 0.001\log_2 0.001 \approx 0.011 \text{ bits}. $$

This is tiny because almost every symbol is the same. This is also the compression interpretation of entropy: highly predictable sources can be encoded with very few bits per symbol on average.

## Conditional entropy

Entropy asks how uncertain $X$ is before anything else is known. The next natural question is: how much uncertainty remains once another variable has been revealed?

That is exactly what conditional entropy measures.

It can be written as

$$ H[X\mid Y] = \sum_y p(y)\,H[X\mid Y=y], $$

or equivalently,

$$
H[X\mid Y]=H[X,Y]-H[Y].
$$

The average-over-$y$ form should be read first.

It says:

1. for each possible value $y$, compute the entropy of the conditional distribution of $X$;
2. average those entropies using the weights $p(y)$.

So conditional entropy is not the uncertainty left after one particular observed value. It is the **average** uncertainty left after the conditioning variable is revealed.

### Why it cannot increase uncertainty on average

A central fact is

$$
H[X\mid Y]\le H[X].
$$

Observation cannot increase uncertainty on average. Specific outcomes may behave in surprising ways, but once averaged over the distribution of $Y$, conditioning only helps or leaves uncertainty unchanged.

This is the right place to see why information theory is useful: it turns the informal phrase “$Y$ tells us something about $X$” into a precise inequality.

## Mutual information

Now ask the next question:

If observing $Y$ reduces uncertainty about $X$, how much reduction occurred?

That quantity is the mutual information:

$$
I[X;Y]=H[X]-H[X\mid Y].
$$

This is the cleanest operational definition. Mutual information is the uncertainty about $X$ removed by learning $Y$.

Because the same logic works in the other direction,

$$
I[X;Y]=H[Y]-H[Y\mid X].
$$

So mutual information is symmetric even though conditional entropies themselves are not.

### Equivalent identity

Another exact form is

$$
I[X;Y]=H[X]+H[Y]-H[X,Y].
$$

This says the total separate uncertainty exceeds the joint uncertainty by exactly the amount of shared information.

### Boundary cases

Two edge cases should be fixed immediately.

- If $X$ and $Y$ are independent, then observing one does not reduce uncertainty about the other, so

$$
I[X;Y]=0.
$$

- If $Y=X$ exactly, then $H[X\mid Y]=0$, so

$$
I[X;Y]=H[X].
$$

In that case, revealing $Y$ removes all uncertainty about $X$.

### Commute and weather example

Let commute choice $C$ take values in $\{\text{walk},\text{bike},\text{drive}\}$, and let weather $R$ take values in $\{\text{clear},\text{rain}\}$.

Assume

$$
p(R=\text{clear})=0.9,\qquad p(R=\text{rain})=0.1.
$$

Suppose the conditional commute distributions are

- given clear weather: $(0.9,0.1,0)$ for walk, bike, drive;
- given rain: $(0.5,0,0.5)$.

Then

$$ H[C\mid R=\text{clear}] = -0.9\log_2 0.9 - 0.1\log_2 0.1 \approx 0.47, $$

and

$$ H[C\mid R=\text{rain}] = -0.5\log_2 0.5 - 0.5\log_2 0.5 = 1. $$

Averaging with the weather probabilities gives

$$ H[C\mid R] = 0.9(0.47)+0.1(1) \approx 0.52\text{ bits}. $$

If the marginal commute entropy is about

$$
H[C]\approx 0.72\text{ bits},
$$

then

$$ I[C;R] = H[C]-H[C\mid R] \approx 0.20\text{ bits}. $$

This is the right qualitative interpretation:

- weather is informative about commuting;
- it does not determine commuting completely;
- so the shared information is positive but modest.

## KL divergence

Entropy, conditional entropy, and mutual information all live inside one or two joint distributions. KL divergence answers a different question:

How well does one distribution approximate another?

For discrete distributions $p$ and $q$,

$$ D(p\|q) = \sum_x p(x)\log\!\left(\frac{p(x)}{q(x)}\right). $$

This should be read in order:

- $p$ is the reference or target distribution;
- $q$ is the approximating distribution;
- the log-ratio compares how the two distributions score the same outcome;
- the average is taken with respect to $p$, so outcomes important under $p$ receive the weight.

### The support condition comes first

Before examples, the domain restriction must be fixed.

If there exists some outcome $x$ with

$$ p(x)>0 \qquad\text{and}\qquad q(x)=0, $$

then

$$
D(p\|q)=\infty.
$$

This is not a technical side remark. It means the approximating distribution assigns zero probability to something the target distribution says can actually happen.

### Core facts

KL divergence satisfies

$$
D(p\|q)\ge 0,
$$

with equality only when $p=q$.

But KL is **not symmetric**. In general,

$$
D(p\|q)\ne D(q\|p).
$$

So it is not a true metric.

This asymmetry matters because the direction tells you which distribution is being treated as the reference and which one is being judged as an approximation.

### Tiny asymmetric example

Let

$$
p=(0.9,0.1),\qquad q=(0.5,0.5).
$$

Then

$$ D(p\|q) = 0.9\log_2\frac{0.9}{0.5} + 0.1\log_2\frac{0.1}{0.5}. $$

If you reverse the order, you get

$$ D(q\|p) = 0.5\log_2\frac{0.5}{0.9} + 0.5\log_2\frac{0.5}{0.1}, $$

which is a different number.

The reason is structural: the average is taken under different weighting distributions in the two expressions.

## Mutual information as a KL divergence

Mutual information can also be written as

$$ I[X;Y] = D\!\bigl(p(x,y)\,\|\,p(x)p(y)\bigr). $$

This is a beautiful identity, but it should be read **after** the uncertainty-reduction interpretation, not before it.

This KL form says mutual information measures the penalty for pretending the joint distribution factorizes when it actually does not.

That immediately explains why:

- mutual information is always nonnegative;
- mutual information is zero exactly when the variables are independent.

So the KL form is powerful, but the first-principles interpretation remains the uncertainty-reduction form.

## How these objects fit together

The section becomes much easier to remember if each quantity is tied to one question.

- **Entropy**: How uncertain is one variable before observation?
- **Conditional entropy**: How much uncertainty remains after another variable is revealed?
- **Mutual information**: How much uncertainty was removed by that revelation?
- **KL divergence**: How badly does one distribution mismatch another?

That is the right conceptual chain. It is better than memorizing formulas in isolation because it makes the formulas answer specific questions.

## Retain from 2.5

- Surprise is the information content of one realized outcome.
- Entropy is average surprise.
- Conditional entropy is the average uncertainty left after conditioning.
- Mutual information is uncertainty reduction and is zero exactly under independence.
- KL divergence is a directed mismatch between two distributions.
- The logarithm base changes the unit, not the underlying concept.

## Do not confuse in 2.5

- Do not confuse discrete entropy with continuous differential entropy.
- Do not confuse one particular conditional distribution $p(x\mid y)$ with the averaged quantity $H[X\mid Y]$.
- Do not confuse mutual information with correlation; mutual information detects general dependence, not only linear dependence.
- Do not confuse KL divergence with a metric; it is directed and asymmetric.

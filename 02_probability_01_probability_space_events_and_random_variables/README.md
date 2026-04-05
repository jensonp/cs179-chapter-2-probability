# 2.1 Probability, Events, and Random Variables

Probability starts with **events**, not with tables of numbers attached directly to variable values.

A probabilistic model begins with a probability space

$$
(\Omega, \mathcal{F}, P).
$$

Here:

- `\Omega` is the sample space, the set of possible worlds or outcomes.
- `\mathcal{F}` is the collection of events to which probabilities are assigned.
- `P` is the probability measure.

The measure satisfies three axioms:

$$
0 \le \mathbb{P}(A) \quad \text{for every event } A \in \mathcal{F},
$$

$$
\mathbb{P}(\Omega)=1,
$$

and countable additivity:

$$
\mathbb{P}\!\left(\bigcup_{i=1}^{\infty} A_i\right)=\sum_{i=1}^{\infty} \mathbb{P}(A_i)
$$

whenever the events `A_1, A_2, ...` are pairwise disjoint.

## What pairwise disjoint means

The condition is

$$
A_i \cap A_j = \varnothing \qquad \text{whenever } i \ne j.
$$

That matters because additivity only works without overlap. If the same world sits in two sets, naive addition would count it twice.

For a fair die, let

$$
A_1=\{1\},\qquad A_2=\{2\},\qquad A_3=\{3\}.
$$

These events are pairwise disjoint, and

$$
A_1 \cup A_2 \cup A_3 = \{1,2,3\}.
$$

Therefore

$$
\mathbb{P}(A_1 \cup A_2 \cup A_3)=\frac{3}{6}
$$

and also

$$
\mathbb{P}(A_1)+\mathbb{P}(A_2)+\mathbb{P}(A_3)=\frac{1}{6}+\frac{1}{6}+\frac{1}{6}=\frac{3}{6}.
$$

The equality works because no outcome belongs to more than one of the three events.

## Consequences of the axioms

Two rules that students use constantly are **not** extra axioms.

First,

$$
\mathbb{P}(\varnothing)=0.
$$

Second, inclusion-exclusion follows from disjoint decomposition:

$$
\mathbb{P}(A \cup B)=\mathbb{P}(A)+\mathbb{P}(B)-\mathbb{P}(A \cap B).
$$

The correction term subtracts the overlap that would otherwise be counted twice.

A concrete die example makes the bookkeeping visible. Let

$$
A=\{1,3,5\}, \qquad B=\{4,5,6\}.
$$

Then

$$
\mathbb{P}(A)=\frac{3}{6},\qquad \mathbb{P}(B)=\frac{3}{6},\qquad \mathbb{P}(A \cap B)=\frac{1}{6},
$$

so

$$
\mathbb{P}(A \cup B)=\frac{3}{6}+\frac{3}{6}-\frac{1}{6}=\frac{5}{6}.
$$

## Random variables come after events

A random variable is a measurable function

$$
X: \Omega \to \mathbb{R}.
$$

This means `X` takes each world `\omega` and assigns it a numerical value `X(\omega)`.

That is the direction of construction:

1. Start with worlds in `\Omega`.
2. Define a variable `X` on those worlds.
3. Then events such as `\{X=x\}` and `\{X \le t\}` are induced automatically.

So the statement

$$
X=x
$$

is shorthand for the event

$$
\{\omega \in \Omega : X(\omega)=x\}.
$$

Likewise,

$$
X \le t
$$

means the event

$$
\{\omega \in \Omega : X(\omega) \le t\}.
$$

This matters because probabilities are assigned to events first. PMFs, CDFs, and later PDFs are derived ways of describing how event-level probability looks after the variable maps worlds to numerical values.

## Example: a parity variable on a die

Let the world be a die roll, and define

$$
X=0 \text{ if the roll is even}, \qquad X=1 \text{ if the roll is odd}.
$$

Then the six raw outcomes are compressed into two states:

- `\{2,4,6\}` map to `0`,
- `\{1,3,5\}` map to `1`.

So

$$
p(X=0)=\mathbb{P}(X=0)=\frac{3}{6}, \qquad p(X=1)=\mathbb{P}(X=1)=\frac{3}{6}.
$$

The random variable keeps only the feature of the world that we care about.

## PMFs, CDFs, and where they come from

For a discrete random variable, the probability mass function is

$$
p(X=x)=\mathbb{P}(X=x).
$$

That is not a second probability law. It is the same event probability, written as a function of the state `x`.

The cumulative distribution function exists in every setting and is always defined by

$$
F_X(x)=\mathbb{P}(X \le x).
$$

In the discrete case, interval probabilities can be recovered by subtraction of CDF values, and point probabilities appear as jump sizes in the CDF.

So the conceptual order is:

- event probability is primary;
- random variables induce events such as `\{X=x\}` and `\{X \le x\}`;
- PMFs and CDFs summarize those induced probabilities.

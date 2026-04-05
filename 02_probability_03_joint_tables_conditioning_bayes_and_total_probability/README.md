# Joint Tables, Conditioning, Bayes' Rule, and the Law of Total Probability

This rewrite treats the joint table as the central object and builds every later operation from it in a fixed order.

## The dentist joint table

Let the binary variables be:

- $C=1$: cavity,
- $T=1$: toothache,
- $D=1$: probe catches.

The joint distribution over $(T,D,C)$ is:

| T | D | C | p(T,D,C) |
|---|---|---|---|
| 0 | 0 | 0 | 0.576 |
| 0 | 0 | 1 | 0.008 |
| 0 | 1 | 0 | 0.144 |
| 0 | 1 | 1 | 0.072 |
| 1 | 0 | 0 | 0.064 |
| 1 | 0 | 1 | 0.012 |
| 1 | 1 | 0 | 0.016 |
| 1 | 1 | 1 | 0.108 |

Each row is a joint event. The eight rows are mutually exclusive and exhaustive, so their probabilities sum to one.

## Marginalization means summing out variables

To get a marginal, keep the value of interest fixed and sum over every compatible value of the hidden variables.

For example,

$$
p(T=0)=\sum_{d,c} p(T=0,D=d,C=c)=0.576+0.008+0.144+0.072=0.80.
$$

Likewise,

$$
p(C=1)=0.008+0.072+0.012+0.108=0.20.
$$

Operationally, marginalization means: hold one coordinate fixed and sum over the rest.

## Conditioning means restrict, then renormalize

The definition is

$$
p(D=d \mid T=t)=\frac{p(D=d,T=t)}{p(T=t)},
$$

provided $p(T=t) > 0$.

The most useful beginner rule is:

1. **Restrict** to worlds consistent with the evidence.
2. **Renormalize** so the remaining mass sums to one.

For $T=1$, keep only the rows with toothache:

| D | C | p(T=1,D,C) |
|---|---|---|
| 0 | 0 | 0.064 |
| 0 | 1 | 0.012 |
| 1 | 0 | 0.016 |
| 1 | 1 | 0.108 |

The total restricted mass is

$$
p(T=1)=0.064+0.012+0.016+0.108=0.20.
$$

Now the conditional probability of a probe catch is

$$
p(D=1 \mid T=1)=\frac{0.016+0.108}{0.20}=\frac{0.124}{0.20}=0.62.
$$

So conditioning is not "changing the world." It is keeping only the already-consistent rows and then renormalizing.

## Table pipeline for a posterior: restrict -> marginalize -> normalize

To compute $p(C \mid T=1)$ from the joint table, do the operations in this order.

### Step 1: restrict to the evidence

Keep only $T=1$ rows.

### Step 2: marginalize over the unused variable

Add over $D$ for each fixed value of $C$:

$$
p(T=1,C=0)=0.064+0.016=0.080,
$$

$$
p(T=1,C=1)=0.012+0.108=0.120.
$$

This gives the intermediate table:

| C | p(T=1,C) |
|---|---|
| 0 | 0.080 |
| 1 | 0.120 |

Notice that this still sums to $p(T=1)=0.20$, not to $1$.

### Step 3: normalize

Divide by the evidence total:

$$
p(C=0 \mid T=1)=\frac{0.080}{0.20}=0.40,
$$

$$
p(C=1 \mid T=1)=\frac{0.120}{0.20}=0.60.
$$

Now the posterior sums to one.

That three-step pipeline is the cleanest way to think about table-based inference.

## Bayes' rule

Bayes' rule is

$$
p(C=c \mid D=d)=\frac{p(D=d \mid C=c)p(C=c)}{p(D=d)}.
$$

The roles are:

- **prior**: $p(C=c)$,
- **likelihood**: $p(D=d \mid C=c)$,
- **evidence**: $p(D=d)$,
- **posterior**: $p(C=c \mid D=d)$.

Bayes' rule is not a new axiom. It is the definition of conditional probability plus the product rule written in a useful direction.

## Worked Bayes example

Suppose

$$
p(T=1 \mid C=0)=0.1, \qquad p(T=1 \mid C=1)=0.6,
$$

and

$$
p(C=0)=0.8, \qquad p(C=1)=0.2.
$$

We want $p(C=1 \mid T=1)$.

First compute the numerator:

$$
p(T=1 \mid C=1)p(C=1)=0.6\cdot 0.2=0.12.
$$

Then compute the evidence using the law of total probability:

$$
p(T=1)=p(T=1 \mid C=1)p(C=1)+p(T=1 \mid C=0)p(C=0)
$$

$$
=0.6\cdot 0.2 + 0.1\cdot 0.8 = 0.12 + 0.08 = 0.20.
$$

Now divide:

$$
p(C=1 \mid T=1)=\frac{0.12}{0.20}=0.60.
$$

So the toothache raises the cavity probability from the prior $0.20$ to the posterior $0.60$.

## Odds form

For two mutually exclusive hypotheses $H_1$ and $H_0$ and evidence $E$, Bayes' rule implies

$$
\frac{p(H_1 \mid E)}{p(H_0 \mid E)} = \frac{p(E \mid H_1)}{p(E \mid H_0)} \cdot \frac{p(H_1)}{p(H_0)}.
$$

This says:

- posterior odds = likelihood ratio x prior odds.

The evidence term cancels because it appears in both posterior probabilities.

## Law of total probability

If $B_1, \dots, B_k$ form a partition of the sample space, then

$$
p(A)=\sum_{i=1}^k p(A \mid B_i)p(B_i).
$$

This is a weighted average of conditional probabilities over disjoint, exhaustive cases.

The law follows from writing $A$ as the disjoint union

$$
A=(A \cap B_1) \cup \cdots \cup (A \cap B_k)
$$

and then applying additivity and the product rule.

## Screening and base rates

Suppose a disease has prevalence

$$
p(D=1)=0.01,
$$

a test has sensitivity

$$
p(T=+ \mid D=1)=0.95,
$$

and false-positive rate

$$
p(T=+ \mid D=0)=0.10.
$$

Then

$$
p(T=+)=0.95\cdot 0.01 + 0.10\cdot 0.99 = 0.1085.
$$

So

$$
p(D=1 \mid T=+)=\frac{0.95\cdot 0.01}{0.1085}\approx 0.0876.
$$

The positive test is informative because it raises the disease probability from $1\%$ to about $8.8\%$, but the disease still remains unlikely because the base rate was very small to begin with.

That is the core lesson behind base-rate neglect: a strong-looking test result does not erase the effect of a very rare prior condition.

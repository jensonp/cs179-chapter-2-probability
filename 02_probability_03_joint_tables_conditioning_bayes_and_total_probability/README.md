# 2.3 Joint Tables, Conditioning, Bayes' Rule, and the Law of Total Probability

The previous section introduced discrete probability laws one random variable at a time. That is enough when the question concerns a single quantity in isolation. But almost all real probabilistic reasoning begins when **several variables must be tracked together**.

That is the problem this section solves.

If one variable records disease status, another records a test outcome, and a third records symptoms, then the central question is no longer

> “What is the probability of one variable taking one value?”

It becomes

> “How are several variables distributed jointly, and how do we update one variable when another is observed?”

That shift introduces four foundational operations:

1. **joint distributions** describe several variables at once;
2. **marginalization** removes variables we do not currently care about;
3. **conditioning** updates the distribution after evidence is observed;
4. **Bayes’ rule** rewrites that update in a direction useful for inference.

The law of total probability then explains how unconditional probabilities can be rebuilt by averaging conditional probabilities over a partition.

This section is one of the most important in the whole chapter because it is the first place where probability becomes a real inference language rather than a collection of isolated distribution formulas.

---

## 1. Why the joint distribution is the central object

When several variables are present, the most complete discrete description is the **joint distribution**.

If $X$ and $Y$ are discrete random variables, then the joint PMF is

$$

p(x,y)=\mathbb{P}(X=x,Y=y).

$$

If there are three variables, say $X,Y,Z$, then the joint PMF is

$$

p(x,y,z)=\mathbb{P}(X=x,Y=y,Z=z).

$$

This object is central because every other distribution about these variables can be obtained from it.

- If you want a distribution for only one variable, you **sum out** the others.
- If you want a conditional distribution after seeing evidence, you **restrict and renormalize** the joint.
- If you want to test independence, you compare the joint to a product of marginals.
- If you want a posterior distribution, you begin from the joint and condition.

That is why mastery of this section starts with one structural fact:

**In the discrete setting, the joint table is the master object.**

Everything else is derived from it.

---

## 2. The dentist example: reading a joint table correctly

We will use the standard dentist-style example because it is small enough to compute exactly but rich enough to show all the operations.

Let the binary variables be:

- $C=1$: cavity,
- $T=1$: toothache,
- $D=1$: probe catches.

The joint distribution over $(T,D,C)$ is:

| T | D | C | $p(T,D,C)$ |
|---|---|---|---:|
| 0 | 0 | 0 | 0.576 |
| 0 | 0 | 1 | 0.008 |
| 0 | 1 | 0 | 0.144 |
| 0 | 1 | 1 | 0.072 |
| 1 | 0 | 0 | 0.064 |
| 1 | 0 | 1 | 0.012 |
| 1 | 1 | 0 | 0.016 |
| 1 | 1 | 1 | 0.108 |

Each row is one fully specified joint event.

That sentence matters. A row is not merely a combination of labels. It is an event saying:

- whether there is a toothache,
- whether the probe catches,
- whether there is a cavity,

all at once.

These eight rows are:

- **mutually exclusive**: no outcome can belong to two different rows at once;
- **exhaustive**: every possible joint state of the three binary variables appears.

So their probabilities must sum to 1. Indeed,

$$

0.576+0.008+0.144+0.072+0.064+0.012+0.016+0.108 = 1.

$$

### What this table is actually doing

The table is not yet answering one special question. It is storing the full probability law for the three variables jointly.

That is why this table is so powerful: the whole inference pipeline begins here.

### Why this example is worth using

This table is small enough that every operation can be carried out by hand. That is exactly why it is pedagogically useful. The reader can see the mechanics before later chapters compress the same operations into matrix notation, graphical models, or more abstract probabilistic identities.

---

## 3. Marginalization: summing out variables you are not asking about

The first derived operation from a joint table is **marginalization**.

If you want the distribution of one variable alone, you do not start over. You sum over all values of the variables you are not focusing on.

If the joint distribution is $p(x,y)$, then the marginal of $X$ is

$$

p_X(x)=\sum_y p(x,y).

$$

If the joint distribution is $p(x,y,z)$, then

$$

p_X(x)=\sum_{y,z} p(x,y,z).

$$

### What marginalization means conceptually

Marginalization means:

- keep the value of interest fixed,
- sum over every hidden value compatible with it.

This should not be memorized as a symbol rule only. It is a bookkeeping rule on the joint table.

### Worked example: marginal of $T$

To compute

$$

p(T=0),

$$

hold $T=0$ fixed and sum over all values of $D$ and $C$:

$$

p(T=0)=\sum_{d,c} p(T=0,D=d,C=c).

$$

Reading from the table,

$$

p(T=0)=0.576+0.008+0.144+0.072=0.80.

$$

Likewise,

$$

p(T=1)=0.064+0.012+0.016+0.108=0.20.

$$

Notice two things:

1. The marginal distribution for $T$ is

$$

   p(T=0)=0.80,\qquad p(T=1)=0.20.

$$

2. These values sum to 1, as a valid marginal must.

### Worked example: marginal of $C$

To compute

$$

p(C=1),

$$

hold $C=1$ fixed and sum over all values of $T$ and $D$:

$$

p(C=1)=0.008+0.072+0.012+0.108=0.20.

$$

Similarly,

$$

p(C=0)=0.576+0.144+0.064+0.016=0.80.

$$

### What the reader should learn from these examples

Marginalization is not “taking some subset of rows because they look relevant.” It is a disciplined operation:

- identify the variable you want to keep,
- identify the variables you are summing out,
- add all rows consistent with the kept value.

That is the pattern that will later reappear in probabilistic graphical models, latent-variable models, and Bayesian inference.

---

## 4. Conditioning: restrict, then renormalize

Conditioning is the next major operation.

If the event $B$ has positive probability, then

$$

\mathbb{P}(A\mid B)=\frac{\mathbb{P}(A\cap B)}{\mathbb{P}(B)}.

$$

When variables are involved, the same logic becomes

$$

p(D=d\mid T=t)=\frac{p(D=d,T=t)}{p(T=t)},
\qquad \text{provided } p(T=t)>0.

$$

### What conditioning is really doing

Conditioning does **not** mean “changing the world” or “changing what really happened.”

Conditioning means:

1. discard all rows inconsistent with the evidence;
2. keep only the rows still possible under that evidence;
3. renormalize the remaining mass so it sums to 1.

This “restrict, then renormalize” rule is the most important operational interpretation in the section.

### Worked example: $p(D=1\mid T=1)$

Restrict to rows where $T=1$:

| D | C | $p(T=1,D,C)$ |
|---|---|---:|
| 0 | 0 | 0.064 |
| 0 | 1 | 0.012 |
| 1 | 0 | 0.016 |
| 1 | 1 | 0.108 |

The total restricted mass is

$$

p(T=1)=0.064+0.012+0.016+0.108=0.20.

$$

Now within those rows, the rows with $D=1$ are:

- $(T,D,C)=(1,1,0)$ with mass $0.016$,
- $(T,D,C)=(1,1,1)$ with mass $0.108$.

So

$$

p(D=1\mid T=1)=\frac{0.016+0.108}{0.20}
=\frac{0.124}{0.20}
=0.62.

$$

### What this means

Before conditioning, the table describes all possible joint worlds. After conditioning on $T=1$, the distribution is restricted to the worlds where toothache is present. Within that restricted world, a probe catch occurs with probability $0.62$.

### Why renormalization is necessary

The restricted rows sum to $0.20$, not to 1. That is because before renormalization they are still carrying their original joint masses.

Conditioning does not merely select rows. It rescales the selected rows into a new probability distribution.

That is exactly what the denominator $p(T=1)$ is doing.

---

## 5. Posterior computation as a table pipeline

A high-quality way to organize table-based inference is as a fixed pipeline:

1. **restrict** to the evidence,
2. **marginalize** over variables no longer needed,
3. **normalize**.

This is the most useful mental model for discrete Bayesian inference.

### Worked example: $p(C\mid T=1)$

We want the posterior distribution of cavity status given toothache.

#### Step 1: restrict to the evidence

Keep only the rows with $T=1$:

| T | D | C | $p(T,D,C)$ |
|---|---|---|---:|
| 1 | 0 | 0 | 0.064 |
| 1 | 0 | 1 | 0.012 |
| 1 | 1 | 0 | 0.016 |
| 1 | 1 | 1 | 0.108 |

#### Step 2: marginalize over the unused variable

We do not want the probe variable in the final posterior, so sum over $D$ for each value of $C$:

For $C=0$,

$$

p(T=1,C=0)=0.064+0.016=0.080.

$$

For $C=1$,

$$

p(T=1,C=1)=0.012+0.108=0.120.

$$

So the intermediate two-row table is

| C | $p(T=1,C)$ |
|---|---:|
| 0 | 0.080 |
| 1 | 0.120 |

Notice that this still sums to

$$

0.080+0.120=0.20=p(T=1),

$$

not to 1.

#### Step 3: normalize

Divide by the evidence total:

$$

p(C=0\mid T=1)=\frac{0.080}{0.20}=0.40,

$$

$$

p(C=1\mid T=1)=\frac{0.120}{0.20}=0.60.

$$

So the posterior is

<table align="center">
  <thead>
    <tr><th>$C$</th><th>$p(C\mid T=1)$</th></tr>
  </thead>
  <tbody>
    <tr><td>$0$</td><td>$0.40$</td></tr>
    <tr><td>$1$</td><td>$0.60$</td></tr>
  </tbody>
</table>

### Why this example matters

This is the exact mechanics of posterior inference in a finite model. Later chapters will express the same idea using Bayes’ rule, factor graphs, variable elimination, or matrix notation, but the logic is already completely visible here.

### What changed

The prior cavity probability from the marginal table was

$$

p(C=1)=0.20.

$$

After seeing a toothache, the posterior becomes

$$

p(C=1\mid T=1)=0.60.

$$

So the evidence raises the probability of a cavity substantially.

This is what inference is: not computing a probability in isolation, but **updating a distribution when evidence arrives**.

---

## 6. Product rule: the algebra behind conditioning

Conditioning is often manipulated through the **product rule**.

From the definition of conditional probability,

$$

p(A\mid B)=\frac{p(A\cap B)}{p(B)},

$$

so equivalently

$$

p(A\cap B)=p(A\mid B)p(B).

$$

This is the product rule.

For variables, this becomes

$$

p(x,y)=p(x\mid y)p(y)=p(y\mid x)p(x).

$$

### Why this matters

The product rule is important because it lets you move between:

- a joint distribution,
- a conditional distribution,
- and a marginal.

It is the algebraic hinge connecting all three.

### Worked mini-example

From the dentist table,

$$

p(T=1,C=1)=0.120.

$$

Also,

$$

p(C=1)=0.20.

$$

So

$$

p(T=1\mid C=1)=\frac{0.120}{0.20}=0.60.

$$

This is exactly consistent with the product rule:

$$

p(T=1,C=1)=p(T=1\mid C=1)p(C=1)=0.60\cdot 0.20=0.12.

$$

So the product rule is not extra machinery. It is the same relationship seen from a different angle.

---

## 7. Bayes’ rule

Bayes’ rule is the product rule solved in the opposite direction.

Starting from

$$

p(A\cap B)=p(A\mid B)p(B)=p(B\mid A)p(A),

$$

we obtain

$$

p(A\mid B)=\frac{p(B\mid A)p(A)}{p(B)}.

$$

For variables, this often appears as

$$

p(C=c\mid D=d)=\frac{p(D=d\mid C=c)p(C=c)}{p(D=d)}.

$$

### What Bayes’ rule is really doing

Bayes’ rule is not a new axiom.

It is a bookkeeping identity that becomes powerful because it rewrites a posterior probability in terms of quantities that are often easier to model or elicit:

- **prior**:

$$

  p(C=c)

$$

- **likelihood**:

$$

  p(D=d\mid C=c)

$$

- **evidence**:

$$

  p(D=d)

$$

- **posterior**:

$$

  p(C=c\mid D=d)

$$

### Why this direction is useful

In many problems, it is easier to specify:

- how likely the evidence would be under each hypothesis,
- and how plausible the hypotheses are before observing the evidence,

than to directly specify the posterior.

Bayes’ rule turns those easier pieces into the posterior we want.

---

## 8. Worked Bayes example

Suppose

$$

p(T=1\mid C=0)=0.1,\qquad p(T=1\mid C=1)=0.6,

$$

and

$$

p(C=0)=0.8,\qquad p(C=1)=0.2.

$$

We want

$$

p(C=1\mid T=1).

$$

### Step 1: compute the numerator

The numerator is

$$

p(T=1\mid C=1)p(C=1)=0.6\cdot 0.2=0.12.

$$

This is the joint probability of “cavity and toothache.”

### Step 2: compute the evidence

The evidence is

$$

p(T=1).

$$

To get it, average over the two possible cavity states:

$$

p(T=1)=p(T=1\mid C=1)p(C=1)+p(T=1\mid C=0)p(C=0).

$$

Substitute the values:

$$

p(T=1)=0.6\cdot 0.2 + 0.1\cdot 0.8 = 0.12+0.08=0.20.

$$

### Step 3: divide

Now

$$

p(C=1\mid T=1)=\frac{0.12}{0.20}=0.60.

$$

### Interpretation

The prior cavity probability was

$$

p(C=1)=0.20.

$$

After observing a toothache, it becomes

$$

p(C=1\mid T=1)=0.60.

$$

So the toothache is strong positive evidence for a cavity.

### Why this example was chosen

This example is important because it shows the full Bayes pipeline without the clutter of a large table:

- prior,
- likelihood,
- evidence,
- posterior.

That four-part structure is the core of Bayesian updating.

---

## 9. The law of total probability

The evidence term in Bayes’ rule is often computed using the **law of total probability**.

If $B_1,\dots,B_k$ form a partition of the sample space — meaning they are disjoint and exhaustive — then

$$

p(A)=\sum_{i=1}^{k} p(A\mid B_i)p(B_i).

$$

### What this means

This formula says that the probability of $A$ can be recovered by splitting the world into disjoint cases, computing the conditional probability of $A$ in each case, and then taking the weighted average using the probabilities of those cases.

This is a weighted-average identity, not a mysterious new law.

### Why partitions matter

The sets $B_1,\dots,B_k$ must be:

- pairwise disjoint,
- and cover the whole sample space.

Otherwise the decomposition either double-counts or fails to account for all possibilities.

### Derivation

Write $A$ as

$$

A=(A\cap B_1)\cup \cdots \cup (A\cap B_k).

$$

These pieces are disjoint, so additivity gives

$$

p(A)=\sum_{i=1}^{k} p(A\cap B_i).

$$

Then apply the product rule to each term:

$$

p(A\cap B_i)=p(A\mid B_i)p(B_i).

$$

Substitute back to obtain

$$

p(A)=\sum_{i=1}^{k} p(A\mid B_i)p(B_i).

$$

### Why this matters for inference

The law of total probability is how hidden causes are “summed out.” It is the simplest finite version of the marginalization ideas that later appear in latent-variable models and Bayesian averaging.

---

## 10. Bayes’ rule and the law of total probability together

Bayes’ rule and the law of total probability are often used together because Bayes’ denominator is exactly the kind of unconditional probability the total-probability law computes.

That is why the two ideas belong in the same section.

The standard template is:

1. write the posterior with Bayes’ rule,
2. compute the numerator directly,
3. compute the denominator by averaging likelihood times prior over all competing hypotheses.

This is the standard finite inference pattern.

---

## 11. Odds form of Bayes’ rule

For two competing hypotheses $H_1$ and $H_0$ and evidence $E$, Bayes’ rule can be written in odds form:

$$

\frac{p(H_1\mid E)}{p(H_0\mid E)}
=
\frac{p(E\mid H_1)}{p(E\mid H_0)}
\cdot
\frac{p(H_1)}{p(H_0)}.

$$

### What each term means

- **prior odds**:

$$

  \frac{p(H_1)}{p(H_0)}

$$

- **likelihood ratio**:

$$

  \frac{p(E\mid H_1)}{p(E\mid H_0)}

$$

- **posterior odds**:

$$

  \frac{p(H_1\mid E)}{p(H_0\mid E)}

$$

So the rule says:

> posterior odds = likelihood ratio × prior odds.

### Why this form matters

The evidence term cancels because it appears in both posterior probabilities. The odds form therefore isolates what evidence does:

- it multiplies prior odds by a factor measuring how much more compatible the evidence is with one hypothesis than the other.

This form is especially useful in diagnostic reasoning, signal detection, and likelihood-ratio tests.

---

## 12. Screening example and base-rate neglect

A good mastery section should not stop at dentist tables. It should also show why the same algebra matters in real reasoning.

Suppose:

- disease prevalence:

$$

  p(D=1)=0.01,

$$

- test sensitivity:

$$

  p(T=+\mid D=1)=0.95,

$$

- false-positive rate:

$$

  p(T=+\mid D=0)=0.10.

$$

We want the posterior disease probability after a positive test:

$$

p(D=1\mid T=+).

$$

### Step 1: compute the evidence

Using the law of total probability over the partition $\{D=1,D=0\}$:

$$

p(T=+)=p(T=+\mid D=1)p(D=1)+p(T=+\mid D=0)p(D=0).

$$

Substitute the values:

$$

p(T=+)=0.95\cdot 0.01 + 0.10\cdot 0.99 = 0.0095+0.099 = 0.1085.

$$

### Step 2: apply Bayes’ rule

The numerator is

$$

p(T=+\mid D=1)p(D=1)=0.95\cdot 0.01=0.0095.

$$

So

$$

p(D=1\mid T=+)=\frac{0.0095}{0.1085}\approx 0.0876.

$$

### Interpretation

The test result is strongly informative:

- prior disease probability:

$$

  1\%

$$

- posterior disease probability after a positive test:

$$

  8.76\%

$$

So the positive test increases the disease probability a lot.

But the disease still remains unlikely.

### Why this surprises people

Many people focus on the test’s sensitivity and ignore the **base rate** of the disease. That is the base-rate neglect error.

The point is not that the test is weak. The point is that when the condition is very rare, false positives from the large healthy population can still dominate the posterior.

### Why this example matters

This is one of the best examples in the chapter because it shows that Bayes’ rule is not just algebra. It is the correction mechanism that prevents intuitive reasoning from overweighting vivid evidence and underweighting prior rarity.

---

## 13. Common confusions to eliminate now

### Confusion 1: the joint table is just a convenient display

No. In the discrete setting, the joint table is the master object from which marginals, conditionals, and posteriors are derived.

### Confusion 2: marginalization means “ignore a variable”

Not quite. Marginalization means **sum over all values** of the variable being removed.

### Confusion 3: conditioning means “change the world”

No. Conditioning means restrict to the rows consistent with the evidence and renormalize.

### Confusion 4: Bayes’ rule is a new probability axiom

No. Bayes’ rule follows from conditional probability and the product rule.

### Confusion 5: the denominator in Bayes’ rule is optional

No. The denominator is what normalizes the posterior. Without it, you only have an unnormalized numerator.

### Confusion 6: a strong test result guarantees a likely hypothesis

No. Posterior probability depends both on the likelihood and on the prior or base rate.

---

## 14. How this section connects to the rest of the chapter

This section is the first full inference section of the chapter.

- **Expectation and variance** later summarize distributions produced by these joint and conditional constructions.
- **Continuous probability** will use the same operations with sums replaced by integrals.
- **Parameter estimation** will reinterpret Bayes’ rule with hypotheses replaced by parameter values.
- **Information theory** will measure dependence and informativeness in terms of joint and conditional distributions.
- **Graphical models** and **latent-variable models** will automate the same restrict–marginalize–normalize logic in more structured settings.

So this section should not be read as a chapter of table tricks. It is the finite, visible form of the inference operations that dominate the rest of probability and machine learning.

---

## 15. Retain from 2.3

- The joint distribution is the central discrete object.
- Marginalization means summing out variables you are not asking about.
- Conditioning means restrict to evidence-consistent worlds and renormalize.
- Posterior computation in tables follows the pipeline:
  restrict -> marginalize -> normalize.
- Bayes’ rule rewrites a posterior in terms of prior, likelihood, and evidence.
- The law of total probability computes unconditional probabilities by averaging over a partition.
- Strong evidence does not erase base rates.

## 16. Do not confuse in 2.3

- Do not confuse a joint probability with a conditional probability.
- Do not confuse marginalization with selecting only one row; it requires summing all compatible rows.
- Do not confuse conditioning with changing the underlying data-generating world.
- Do not confuse Bayes’ numerator with the full posterior.
- Do not ignore the evidence term or the base rate in diagnostic reasoning.

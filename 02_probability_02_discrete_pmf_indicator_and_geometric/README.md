# 2.2 Discrete PMFs, Indicator Notation, and the Geometric Distribution

This section is the first place where the abstract machinery from probability spaces and random variables turns into concrete distributions you can compute with. The previous section established the architecture:

- outcomes live in a sample space,
- events are sets of outcomes,
- a probability measure assigns probabilities to those events,
- random variables convert outcomes into numerical values.

This section asks the next natural question:

> Once a random variable is defined, how do we describe the probability law of its values in a usable form?

For discrete variables, the answer is the **probability mass function**. That object is the main entry point of the section. Indicator notation is then introduced because it gives a compact and powerful way to write discrete distributions, especially when a variable chooses one state from a finite set. Finally, the geometric distribution is introduced because it is the first nontrivial infinite-support discrete law and the first place where a repeated-trials story produces a full distributional formula.

There are three layers to keep separate throughout:

1. the **random variable** itself,
2. the **support** of its possible values,
3. the **PMF** that assigns probability mass to those values.

If those layers stay distinct, then Bernoulli, categorical, and geometric distributions all become variations on one theme rather than isolated facts to memorize.

---

## 1. Why PMFs are needed

A random variable $X$ is a function from outcomes to numbers. But once the variable has been defined, we usually stop reasoning directly in terms of raw sample-space outcomes and instead reason in terms of the values the variable can take.

That shift creates a new question:

- not “which underlying outcome occurred?”
- but “with what probability does the variable take each of its possible values?”

A PMF answers exactly that question.

For a discrete random variable, probability is concentrated on isolated values. So instead of integrating over intervals or working with densities, we can list the probability attached to each attainable state directly.

That is why PMFs are the right next topic after random variables. They are the simplest way to move from the abstract definition of a variable to a concrete usable probability law.

---

## 2. Probability mass functions

A **probability mass function** for a discrete random variable $X$ is

$$
p_X(x)=\mathbb{P}(X=x).
$$

This is the first formal definition of the section, but the reader should immediately attach the right interpretation to it.

A PMF is a function on the possible values of the variable. For each value $x$, it returns the probability that the random variable equals that value exactly.

There are three structural requirements:

1. **Nonnegativity**

$$
p_X(x)\ge 0 \quad \text{for every } x.
$$

2. **Normalization**

$$
\sum_x p_X(x)=1,
$$

   where the sum runs over the support of $X$.

3. **Event probabilities are sums of point masses**
   for any set $A$ of values,

$$
\mathbb{P}(X\in A)=\sum_{x\in A} p_X(x).
$$

These are not independent facts. The PMF is just the distribution of a discrete random variable written value by value.

### What the PMF is really doing

A PMF is a table written as a function.

That is the right first intuition. You can display a PMF as a table, but mathematically it is cleaner to treat it as a function from values to probabilities.

### Example: weather state

Suppose a weather variable takes values in

$$
\{\text{sun},\text{cloud},\text{rain}\}
$$

with probabilities

$$ p_X(\text{sun})=0.5,\qquad p_X(\text{cloud})=0.3,\qquad p_X(\text{rain})=0.2. $$

This is a complete PMF because

- every mass is nonnegative,
- the masses sum to 1:

$$
0.5+0.3+0.2=1.
$$

From this PMF, any event probability can be computed by summing the relevant entries. For example,

$$
\mathbb{P}(X\in\{\text{cloud},\text{rain}\})=0.3+0.2=0.5.
$$

So a PMF is not merely a definition. It is already a computational object.

---

## 3. Support: what values are even possible?

Before doing calculations with a PMF, the support of the variable should always be identified.

The **support** of a discrete random variable is the set of values with positive probability mass.

This matters because the sum-to-one condition is not over all real numbers. It is over the values the variable can actually take.

### Example: support of a Bernoulli variable

If $X$ is Bernoulli, then the support is

$$
\{0,1\}.
$$

That fact does real work. It is the reason the PMF has only two masses, why one of them determines the other, and why compact forms like $\rho^x(1-\rho)^{1-x}$ are possible.

### Why support should be stated early

Many beginner mistakes come from skipping the support:

- summing over impossible values,
- forgetting boundary values,
- using the wrong convention for a count variable,
- or writing a formula that looks plausible but is defined on the wrong domain.

So for mastery, the habit should be:

1. identify the support,
2. write the PMF,
3. check normalization,
4. only then compute with it.

---

## 4. PMFs and CDFs in the discrete setting

The PMF is the natural object for exact-state probabilities. The cumulative distribution function is the natural object for threshold probabilities.

The CDF is

$$
F_X(x)=\mathbb{P}(X\le x).
$$

In the discrete setting, this is the running total of the PMF masses up to the threshold $x$.

### Why this matters

PMF and CDF are not competing definitions. They answer different kinds of questions.

- PMF:

$$
p_X(x)=\mathbb{P}(X=x)
$$

  answers exact-state questions.

- CDF:

$$
F_X(x)=\mathbb{P}(X\le x)
$$

  answers threshold questions.

The CDF is especially useful because interval probabilities can be obtained by subtraction.

### Worked example: from PMF to CDF

Let $X$ take values in $\{0,1,2\}$ with

$$
p_X(0)=0.2,\qquad p_X(1)=0.5,\qquad p_X(2)=0.3.
$$

Then the CDF is

<table align="center">
  <thead>
    <tr><th>$F_X(x)$</th><th>condition on $x$</th></tr>
  </thead>
  <tbody>
    <tr><td>$0$</td><td>$x \lt 0$</td></tr>
    <tr><td>$0.2$</td><td>$0 \le x \lt 1$</td></tr>
    <tr><td>$0.7$</td><td>$1 \le x \lt 2$</td></tr>
    <tr><td>$1$</td><td>$x \ge 2$</td></tr>
  </tbody>
</table>

Now consider the interval event

$$
1<X\le 2.
$$

Since only the value $2$ lies in that interval, we already know the answer should be $0.3$ from the PMF.

Using the CDF,

$$
\mathbb{P}(1<X\le 2)=F_X(2)-F_X(1)=1-0.7=0.3.
$$

This example teaches the right structural lesson:

- in the discrete case, the CDF is a step function,
- its jumps are exactly the PMF masses,
- interval probabilities come from differences of cumulative totals.

### Misconception to eliminate

Do not confuse

$$
F_X(x)
$$

with

$$
p_X(x).
$$

The PMF is the mass at one state.  
The CDF is the cumulative mass to the left of a threshold.

They are different objects and answer different questions.

---

## 5. Indicator notation

Indicator notation is introduced here because it is one of the cleanest ways to turn a logical condition into a numerical quantity.

For any statement $S$, the indicator

$$
\mathbf{1}[S]
$$

equals

<table align="center">
  <thead>
    <tr><th>$\mathbf{1}[S]$</th><th>condition</th></tr>
  </thead>
  <tbody>
    <tr><td>$1$</td><td>if $S$ is true</td></tr>
    <tr><td>$0$</td><td>if $S$ is false</td></tr>
  </tbody>
</table>

### What an indicator really does

An indicator is not a new probability concept. It is a selector.

It turns a condition into a number that can be multiplied, summed, or used as an exponent in a compact formula. That is why indicators appear constantly in probability, statistics, and machine learning.

### Example: exact-state selector

The indicator

$$
\mathbf{1}[X=x]
$$

is 1 exactly when the realized value of $X$ equals $x$, and 0 otherwise.

If you sum such indicators across candidate states, you can isolate exactly one active term.

This is the mechanism behind several compact PMF formulas.

### Why indicators matter beyond notation

Later in the chapter, indicators will become powerful because:

- they turn counts into sums,
- sums can be averaged using expectation,
- and that gives easy access to expected counts and sufficient statistics.

So indicator notation matters now as syntax, but later as a structural tool.

---

## 6. Bernoulli distribution

The Bernoulli distribution is the simplest nontrivial discrete distribution and the first one where indicator-style formulas become instructive rather than cosmetic.

A Bernoulli random variable has support

$$
X\in\{0,1\}.
$$

If

$$
\mathbb{P}(X=1)=\rho,
$$

then automatically

$$
\mathbb{P}(X=0)=1-\rho,
$$

because the two masses must sum to 1.

So the PMF is

<table align="center">
  <thead>
    <tr><th>$p_X(x)$</th><th>condition on $x$</th></tr>
  </thead>
  <tbody>
    <tr><td>$1-\rho$</td><td>$x=0$</td></tr>
    <tr><td>$\rho$</td><td>$x=1$</td></tr>
  </tbody>
</table>

### What the parameter means

The entire distribution is controlled by one number: the success probability $\rho$.

This already makes Bernoulli special. The support is fixed, so only the mass allocation matters. Because there are only two states, specifying one probability determines the other.

### Compact Bernoulli form

The PMF can be written as

$$ p_X(x)=\rho^x(1-\rho)^{1-x}, \qquad x\in\{0,1\}. $$

This formula should not be memorized blindly. It should be read as a selector.

- If $x=1$, then

$$
\rho^1(1-\rho)^0=\rho.
$$

- If $x=0$, then

$$
\rho^0(1-\rho)^1=1-\rho.
$$

So the exponents choose the correct probability automatically.

### Indicator form

An equivalent form is

$$
p_X(x)=\rho\,\mathbf{1}[x=1]+(1-\rho)\,\mathbf{1}[x=0].
$$

This is less elegant algebraically, but more transparent conceptually. It literally says:

- choose $\rho$ if the realized value is 1,
- choose $1-\rho$ if the realized value is 0.

### Worked Bernoulli example

Suppose a classifier outputs a binary correctness variable $X$ where

<table align="center">
  <thead>
    <tr><th>$X$</th><th>condition</th></tr>
  </thead>
  <tbody>
    <tr><td>$1$</td><td>correct prediction</td></tr>
    <tr><td>$0$</td><td>incorrect prediction</td></tr>
  </tbody>
</table>

If the classifier is correct with probability $\rho=0.8$, then

$$
p_X(1)=0.8,\qquad p_X(0)=0.2.
$$

Using the compact formula:

- for $x=1$,

$$
p_X(1)=0.8^1\cdot 0.2^0=0.8;
$$

- for $x=0$,

$$
p_X(0)=0.8^0\cdot 0.2^1=0.2.
$$

This example is worth noticing because Bernoulli variables appear everywhere:
- success/failure,
- correct/incorrect,
- yes/no,
- click/no click,
- accepted/rejected,
- present/absent.

Bernoulli is not a toy distribution. It is a building block.

### Misconception to eliminate

Do not confuse the variable $X$ with its parameter $\rho$.

- $X$ is random and takes values 0 or 1.
- $\rho$ is fixed for the model and determines the probabilities.

That distinction becomes crucial later in Bayesian models, where $\rho$ itself may become a random variable under a prior.

---

## 7. Categorical distribution

The categorical distribution generalizes Bernoulli from two states to $d$ states.

If $X$ takes values in

$$
\{1,2,\dots,d\},
$$

then a categorical distribution is specified by probabilities

$$ \mathbb{P}(X=i)=\rho_i, \qquad \rho_i\ge 0, \qquad \sum_{i=1}^{d}\rho_i=1. $$

### What changes from Bernoulli to categorical

Conceptually, not much changes.

- Bernoulli chooses between 2 states.
- Categorical chooses between $d$ states.

The same basic ideas remain:

- support comes first,
- masses are nonnegative,
- masses must sum to 1,
- event probabilities are sums of relevant masses.

### Degrees of freedom

Only $d-1$ of the parameters are free.

Once $\rho_1,\dots,\rho_{d-1}$ are chosen, the last one is forced by normalization:

$$
\rho_d=1-\sum_{i=1}^{d-1}\rho_i.
$$

This is a small but important structural fact. Normalization constraints reduce the number of independent parameters.

### Indicator-product form

A compact form for the categorical PMF is

$$
p_X(x)=\prod_{i=1}^{d}\rho_i^{\mathbf{1}[x=i]}.
$$

This works because exactly one indicator exponent equals 1 and all others equal 0.

So if the realized state is $k$, then the product becomes

$$
\rho_1^0\cdots \rho_k^1\cdots \rho_d^0=\rho_k.
$$

The product form is compact because indicators again act as selectors.

### Worked categorical example

Let a weather variable take values

$$
\{\text{sun},\text{cloud},\text{rain}\}
$$

with probabilities

$$ \rho_{\text{sun}}=0.5,\qquad \rho_{\text{cloud}}=0.3,\qquad \rho_{\text{rain}}=0.2. $$

If the realized state is rain, then

$$ \mathbf{1}[X=\text{sun}]=0,\qquad \mathbf{1}[X=\text{cloud}]=0,\qquad \mathbf{1}[X=\text{rain}]=1, $$

and the product form becomes

$$
0.5^0\cdot 0.3^0\cdot 0.2^1=0.2.
$$

So the table form and indicator-product form are not two different models. They are two different ways of writing the same PMF.

### Why this matters later

Categorical variables are central because:

- labels in classification are categorical,
- latent states in mixture models are categorical,
- multinomial count models are built from repeated categorical draws,
- one-hot encodings are just indicator representations of categorical states.

So this is not just a notation exercise. It is the prototype for many later modeling structures.

### Misconception to eliminate

Do not confuse a categorical variable with a numeric variable just because its states are labeled by integers.

If $X\in\{1,2,3\}$ is categorical, the labels are state names, not necessarily quantities with arithmetic meaning. Whether arithmetic on the labels is meaningful depends on the model, not on the notation.

---

## 8. Indicator vectors and one-hot form

Because categorical states are often encoded numerically in machine learning, it is worth making one extra connection explicit.

A categorical observation can be represented as a one-hot indicator vector. If $X$ takes one of $d$ states, define a vector

$$
z=(z_1,\dots,z_d)
$$

with

$$
z_i=\mathbf{1}[X=i].
$$

Then exactly one coordinate equals 1 and the rest equal 0.

The categorical PMF can then be written as

$$
p(X)=\prod_{i=1}^{d}\rho_i^{z_i}.
$$

This is the vectorized version of the indicator-product form.

### Why this matters

This is the bridge from probability notation to machine-learning data representations:

- one-hot label vectors,
- cross-entropy objectives,
- multinomial models,
- softmax outputs

all use this same structure.

So the indicator-product form is not an algebra trick. It is the probability-side expression of a representation that later appears everywhere in practice.

---

## 9. Geometric distribution: why it is introduced now

Bernoulli and categorical distributions live on finite supports. The geometric distribution is the first important example where:

- the support is infinite,
- the story comes from repeated trials,
- the PMF is derived from an event pattern,
- and the expected value requires a real series calculation.

That is why it belongs here. It is the first distribution that forces the reader to move beyond “small finite table” thinking while still remaining fully discrete and interpretable.

---

## 10. Geometric distribution: convention first

The geometric distribution has a notorious convention issue, so the convention must be stated before the formula.

In this section, the variable counts the **number of failures before the first success** in repeated independent Bernoulli trials with success probability $\rho$.

So the support is

$$
X\in\{0,1,2,\dots\}.
$$

That support should be noticed immediately. Zero is included because the very first trial might already be a success, in which case the number of failures before the first success is 0.

### Why the convention matters

Some texts instead count the number of trials until the first success. That produces a different support and a different mean. These are not contradictory distributions. They are two conventions for counting the same process.

For mastery, never write a geometric PMF before stating the convention.

---

## 11. Deriving the geometric PMF

Under the failures-before-success convention, the event

$$
X=x
$$

means:

- the first $x$ trials are failures,
- the next trial is the first success.

If the success probability on each independent trial is $\rho$, then failure probability is

$$
1-\rho.
$$

So the probability of exactly $x$ failures before the first success is

$$ p_X(x)=(1-\rho)^x\rho, \qquad x=0,1,2,\dots $$

### Why this formula has that shape

This formula should be read story-first, not symbol-first.

- $(1-\rho)^x$ accounts for the first $x$ failures;
- the final factor $\rho$ accounts for the first success;
- independence allows multiplication.

This is one of the earliest important examples of “translate an event story into a product probability formula.”

### Worked example with $\rho=0.2$

Let $\rho=0.2$. Then

$$
p_X(0)=0.2,
$$

because zero failures before the first success means immediate success on the first trial.

Also,

$$
p_X(1)=0.8\cdot 0.2=0.16,
$$

because one failure before the first success means:

- fail once,
- then succeed.

And

$$
p_X(2)=0.8^2\cdot 0.2=0.128.
$$

Each step to the right multiplies by another factor of $1-\rho=0.8$, so the masses decay geometrically. That decay pattern is exactly where the name comes from.

### Why the support is infinite

There is no fixed upper limit on how many failures can happen before the first success. Any nonnegative integer is possible, although long runs become increasingly unlikely.

This is the first important example of a count variable with infinite support.

---

## 12. Checking normalization of the geometric PMF

A proper PMF must sum to 1. This should be checked, not merely assumed.

We compute

$$ \sum_{x=0}^{\infty}(1-\rho)^x\rho = \rho\sum_{x=0}^{\infty}(1-\rho)^x. $$

Now use the geometric-series identity

$$ \sum_{x=0}^{\infty} r^x=\frac{1}{1-r}, \qquad |r|<1. $$

Here

$$
r=1-\rho,
$$

and since $0<\rho\le 1$, we have $|1-\rho|<1$ unless $\rho=0$, which would mean success never occurs and the model degenerates.

So

$$ \rho\sum_{x=0}^{\infty}(1-\rho)^x = \rho\cdot \frac{1}{1-(1-\rho)} = \rho\cdot \frac{1}{\rho} = 1. $$

So the PMF is properly normalized.

### Why this matters

This is the first time the reader has to see that an infinite-support PMF is still legitimate as long as the infinite sum converges to 1.

That is an important conceptual step beyond finite tables.

---

## 13. Mean of the geometric distribution

The geometric mean is worth deriving carefully because it illustrates a general pattern: sometimes discrete expectations are computed by transforming a familiar series.

For a discrete random variable,

$$
\mathbb{E}[X]=\sum_x x\,p_X(x).
$$

So for the geometric PMF,

$$ \mathbb{E}[X] = \sum_{x=0}^{\infty} x(1-\rho)^x\rho. $$

Let

$$
r=1-\rho.
$$

Then

$$ \mathbb{E}[X] = \rho\sum_{x=0}^{\infty} x r^x. $$

Now start from the standard geometric series

$$ \sum_{x=0}^{\infty} r^x = \frac{1}{1-r}, \qquad |r|<1. $$

Differentiate with respect to $r$:

$$
\sum_{x=1}^{\infty} x r^{x-1} = \frac{1}{(1-r)^2}.
$$

Multiply by $r$:

$$
\sum_{x=0}^{\infty} x r^x = \frac{r}{(1-r)^2}.
$$

Substitute back:

$$ \mathbb{E}[X] = \rho\cdot \frac{1-\rho}{\rho^2} = \frac{1-\rho}{\rho}. $$

So under the failures-before-success convention,

$$
\mathbb{E}[X]=\frac{1-\rho}{\rho}.
$$

### Interpretation

This formula should be interpreted, not just memorized.

- If $\rho$ is large, success comes quickly, so the expected number of failures is small.
- If $\rho$ is small, success is rare, so the expected number of failures is large.

For example, if $\rho=0.2$, then

$$
\mathbb{E}[X]=\frac{0.8}{0.2}=4.
$$

So on average, we expect 4 failures before the first success.

### What this derivation teaches

The important lesson is not only the final formula. It is also the method:

- write expectation as a sum against the PMF,
- identify a known series structure,
- manipulate the series into a usable form.

That pattern reappears throughout probability.

---

## 14. The other geometric convention

Some texts define a geometric variable $Y$ as the **number of trials until the first success**.

Then the support is

$$
Y\in\{1,2,3,\dots\},
$$

and the PMF is

$$
p_Y(y)=(1-\rho)^{y-1}\rho.
$$

Under that convention, the mean is

$$
\mathbb{E}[Y]=\frac{1}{\rho}.
$$

### Why the two formulas differ by exactly one

The variables are related by

$$
Y=X+1.
$$

So the difference in their means is also exactly one:

$$
\mathbb{E}[Y]=\mathbb{E}[X]+1.
$$

This is not a minor technicality. It is a major source of mistakes in homework, software libraries, and textbook comparisons.

### Mastery rule

For geometric distributions, always do these checks in order:

1. What is being counted?
2. Does support begin at 0 or at 1?
3. Is the variable counting failures before success or total trials until success?

Do not proceed until the convention is fixed.

---

## 15. Memorylessness: the special structural property

The geometric distribution is not only important because it models waiting time. It is also the first discrete distribution with a distinctive structural property called **memorylessness**.

For $m,n\ge 0$,

$$
\mathbb{P}(X>m+n\mid X>m)=\mathbb{P}(X>n).
$$

### What this means

Conditioning on already having waited through $m$ failures does not change the distribution of how many additional failures remain before the first success.

The process “starts fresh” after each failure because the Bernoulli trials are independent and the success probability stays the same.

### Why this matters

This is not true for most discrete waiting-time models. The geometric distribution is special.

That is why the geometric law is the discrete analogue of the exponential distribution, which has the corresponding continuous memoryless property.

### Why this belongs here

Even if later sections do not exploit memorylessness immediately, a mastery set of notes should mention it because it tells the reader what makes the geometric distribution structurally distinctive rather than just another PMF formula.

---

## 16. One full worked synthesis example

Suppose a website visitor clicks with probability $\rho=0.25$ on each page impression, independently from impression to impression.

Define $X$ as the number of non-click impressions before the first click.

### Step 1: identify the support

Because the first click may happen immediately or after any finite number of misses,

$$
X\in\{0,1,2,\dots\}.
$$

### Step 2: identify the distribution family

This is a geometric model under the failures-before-success convention.

### Step 3: write the PMF

$$
p_X(x)=(1-0.25)^x(0.25)=0.75^x\cdot 0.25.
$$

### Step 4: compute a few values

Immediate click:

$$
p_X(0)=0.25.
$$

One miss before first click:

$$
p_X(1)=0.75\cdot 0.25=0.1875.
$$

Two misses before first click:

$$
p_X(2)=0.75^2\cdot 0.25=0.140625.
$$

### Step 5: compute a cumulative probability

What is the probability the first click occurs within the first three impressions?

Under the failures-before-success convention, “within the first three impressions” means

$$
X\le 2.
$$

So

$$
\mathbb{P}(X\le 2)=p_X(0)+p_X(1)+p_X(2).
$$

That is

$$
0.25+0.1875+0.140625=0.578125.
$$

### Step 6: compute the mean

$$
\mathbb{E}[X]=\frac{1-\rho}{\rho}=\frac{0.75}{0.25}=3.
$$

So on average there are 3 misses before the first click.

### What this example was chosen to teach

This example ties together:

- support identification,
- convention choice,
- PMF construction from an event story,
- exact-state probabilities,
- cumulative probabilities,
- and the meaning of the expected value.

That is the right kind of synthesis example for mastery notes: one example, many structural lessons.

---

## 17. Common confusions to eliminate now

### Confusion 1: PMF versus random variable

A random variable is the object that takes values.  
The PMF is the probability law of those values.

Do not confuse the variable with the function that describes its distribution.

### Confusion 2: support versus PMF value

The support tells you which values are possible.  
The PMF tells you how much probability mass is attached to each possible value.

A value can be outside the support even before you ask what its mass is.

### Confusion 3: indicator notation as a probability concept

Indicators do not introduce randomness by themselves. They are selectors that turn conditions into 0–1 quantities.

### Confusion 4: Bernoulli variable versus Bernoulli parameter

The variable $X$ is random.  
The parameter $\rho$ is fixed for the model.

Later Bayesian sections may place a distribution on $\rho$, but that is a different modeling layer.

### Confusion 5: geometric convention

Geometric distributions are not fully specified until the counting convention is stated.

### Confusion 6: PMF versus CDF

The PMF is point mass.  
The CDF is cumulative mass.

Do not treat them as interchangeable.

---

## 18. How this section connects to the rest of the chapter

This section creates several tools that later chapters rely on directly.

- **Joint distributions and Bayes’ rule** will use discrete PMFs as the first concrete setting for conditioning and marginalization.
- **Expectation and variance** will summarize PMFs numerically.
- **Likelihood** will use indicator-product forms to write Bernoulli and categorical models compactly.
- **Exponential-family models** will use one-hot and indicator representations repeatedly.
- **Geometric and other count models** prepare the reader for waiting-time reasoning and infinite-support discrete distributions.

So the point of mastering this section is not just learning three named distributions. It is learning how discrete probabilistic models are built, written, and interpreted.

---

## 19. Retain from 2.2

- A PMF is the probability law of a discrete random variable written value by value.
- Support should be identified before writing or using a PMF.
- The PMF answers exact-state questions; the CDF answers threshold questions.
- Indicator notation is a selector device that becomes especially useful in Bernoulli and categorical models.
- Bernoulli is the two-state discrete model; categorical is its multi-state generalization.
- The geometric distribution is the first important infinite-support discrete waiting-time law.
- The geometric distribution must always be accompanied by its counting convention.
- The geometric law is special because of memorylessness.

## 20. Do not confuse in 2.2

- Do not confuse the variable with its PMF.
- Do not confuse the support with the probabilities.
- Do not confuse PMF and CDF.
- Do not confuse Bernoulli parameter $\rho$ with a Bernoulli outcome.
- Do not use a geometric formula before fixing the convention.
- Do not treat indicator notation as a new probability object rather than a numerical selector.

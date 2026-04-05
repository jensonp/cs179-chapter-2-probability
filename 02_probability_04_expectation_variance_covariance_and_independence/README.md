# Expectation, Variance, Covariance, and Independence

This section is not just a list of definitions. It is a chain of answers to four different questions:

- **Expectation** asks where a distribution is centered on average.
- **Variance** asks how tightly or loosely the distribution is spread around that center.
- **Covariance** asks how two variables move together relative to their own means.
- **Independence** asks whether the full joint distribution truly factorizes into separate marginal pieces.

That order matters. First we want a notion of center. Then we want a notion of spread around that center. Then, once more than one variable is present, we want a notion of joint movement. Finally, we want to know when the entire joint structure splits into simpler pieces. If those distinctions stay sharp, later sections on Gaussian models, likelihoods, entropy, and graphical models become much easier to understand.

## Why this section exists

Earlier sections introduced probability spaces, random variables, distributions, conditioning, and Bayes’ rule. Those tools describe what probabilities are assigned to events and variables. But many practical questions are not about full distributions directly. They are about summaries.

Examples:

- If a model predicts a distribution over outcomes, where is that distribution centered?
- If two distributions have the same center, how do we distinguish one that is concentrated from one that is diffuse?
- If two variables are observed together, how do we quantify whether high values of one tend to coincide with high values of the other?
- When can a joint model be simplified into separate pieces without losing information?

Expectation, variance, covariance, and independence answer those questions. They are not interchangeable, and one of the most common failure modes in probability is to treat them as if they were all versions of the same thing. They are not. Each one compresses a different feature of a distribution or joint distribution.

---

## 1. Expectation

### What expectation is trying to summarize

A probability distribution may assign mass to many different outcomes. The first natural summary question is: **where is the distribution located on average?**

Expectation answers that question by taking a weighted average of possible values, where the weights are the probabilities of those values.

For a discrete random variable,

$$
\mathbb{E}[X] = \sum_x x\,p(x).
$$

This formula is easy to memorize and easy to misuse. The expectation is **not** the most likely next value. It is **not** required to be a value the variable can actually take. It is the long-run average, or the center of mass, of the distribution.

### Bernoulli example

Suppose

$$
p(X=0)=0.7,\qquad p(X=1)=0.3.
$$

Then

$$ \mathbb{E}[X] = 0\cdot 0.7 + 1\cdot 0.3 = 0.3. $$

This is one of the cleanest examples because the expectation has a direct interpretation. A Bernoulli variable records success as $1$ and failure as $0$, so the average value is just the success probability.

### Fair die example

For a fair die,

$$ \mathbb{E}[X] = \sum_{x=1}^{6} x\cdot \frac{1}{6} = \frac{1+2+3+4+5+6}{6} = 3.5. $$

This example is important because it prevents a bad intuition from taking root. A die never lands on $3.5$, but $3.5$ is still its expectation. So expectation is not “the predicted next observation.” It is the balance point of the distribution.

A useful physical analogy is a weighted rod or a set of masses on a line. The expectation is where the system balances.

### What expectation does and does not capture

Expectation is a summary of **location** only. It does not tell us:

- how spread out the outcomes are,
- whether the distribution is symmetric or skewed,
- whether the variable is concentrated or diffuse.

Two variables can share the same expectation and still behave very differently. That is exactly why variance is introduced next.

---

## 2. Linearity of expectation

One of the most useful facts in all of probability is

$$ \mathbb{E}[aX+bY+c] = a\,\mathbb{E}[X] + b\,\mathbb{E}[Y] + c. $$

This is called linearity of expectation.

### Why linearity matters

This identity is powerful because it lets us analyze totals, sums, and counts without needing the full joint distribution first. In many problems, the hard part is figuring out the entire distribution of a complicated random quantity. But its expectation may still be easy because the quantity can be decomposed into simpler pieces.

That is why linearity is not just a convenient algebraic rule. It is one of the main tools for turning complicated probability questions into manageable ones.

### Independence is not required

A common mistake is to think linearity needs independence. It does not.

The identity

$$
\mathbb{E}[X+Y] = \mathbb{E}[X] + \mathbb{E}[Y]
$$

holds whether or not $X$ and $Y$ are independent. This is one of the most important distinctions in the section because later formulas, especially for variance, do depend on independence assumptions. Expectation does not.

### Dependent example

Let $X$ be Bernoulli with

$$
p(X=1)=0.3,\qquad p(X=0)=0.7,
$$

and define

$$
Y = 1-X.
$$

Then $X$ and $Y$ are completely dependent. If you know one, you know the other exactly.

But linearity still gives

$$ \mathbb{E}[X+Y] = \mathbb{E}[1] = 1. $$

Separately,

$$ \mathbb{E}[X] + \mathbb{E}[Y] = 0.3 + 0.7 = 1. $$

So dependence does not break linearity.

### Indicator variables and counting

The most useful application of linearity in elementary probability comes through indicator variables.

Suppose $H_1, H_2, H_3$ are indicators for whether the first, second, and third coin flips are heads. Let

$$
N = H_1 + H_2 + H_3.
$$

Then $N$ is the total number of heads.

Even if we do not derive the full distribution of $N$, linearity immediately gives

$$ \mathbb{E}[N] = \mathbb{E}[H_1] + \mathbb{E}[H_2] + \mathbb{E}[H_3]. $$

If each flip has head probability $\rho$, then each indicator has expectation $\rho$, so

$$
\mathbb{E}[N]=3\rho.
$$

This is the deeper pattern: complicated counts are often easy to **expect** even when they are not easy to **distribute**.

---

## 3. Variance

### Why expectation is not enough

Expectation tells us where a distribution is centered, but it says nothing about how tightly the mass sits around that center.

A variable that is almost always near its mean and a variable that swings wildly around the same mean have the same expectation but very different behavior. Variance is introduced to measure that difference.

### Definition

Variance is

$$ \mathrm{Var}(X) = \mathbb{E}\!\left[(X-\mathbb{E}[X])^2\right]. $$

The quantity inside the expectation is the squared deviation from the mean.

### Why the square appears

The square is doing two jobs at once:

1. it makes all deviations nonnegative, so positive and negative deviations do not cancel;
2. it penalizes large deviations more heavily than small ones.

So variance is not just “another average.” It is a summary of spread around the mean.

### Computational identity

Expanding the square gives

$$ \mathrm{Var}(X) = \mathbb{E}[X^2] - \mathbb{E}[X]^2. $$

This is usually the easier formula to compute from a probability table.

### Bernoulli variance

If $X\in\{0,1\}$ with

$$
p(X=1)=\rho,
$$

then $X^2=X$, so

$$ \mathbb{E}[X]=\rho, \qquad \mathbb{E}[X^2]=\rho. $$

Therefore

$$ \mathrm{Var}(X) = \rho-\rho^2 = \rho(1-\rho). $$

This formula is worth interpreting. The spread is largest near $\rho=\tfrac12$, where the outcomes are most uncertain, and shrinks toward $0$ as $\rho$ approaches $0$ or $1$, where the variable becomes nearly deterministic.

### Same mean, different variance

Let $X$ be constant at $3$, and let $Y$ equal $0$ or $6$ with probabilities $\tfrac12$ and $\tfrac12$.

Then

$$
\mathbb{E}[X]=3,\qquad \mathbb{E}[Y]=3.
$$

But

$$
\mathrm{Var}(X)=0
$$

because $X$ never deviates from its mean, while

$$ \mathrm{Var}(Y) = \left(0^2\cdot \tfrac12 + 6^2\cdot \tfrac12\right)-3^2 = 18-9 = 9. $$

This example shows exactly why mean and variance are different summaries. The center is the same. The spread is not.

### What variance does and does not tell us

Variance captures spread around the mean, but it does not tell us everything about a distribution. Two very different distributions may share the same mean and variance. So variance is extremely useful, but it is not a complete description of shape.

---

## 4. Covariance

### Why covariance is introduced

Once more than one random variable is present, there is a new question expectation and variance cannot answer:

**How do the variables move together?**

It is not enough to know each variable’s center and spread separately. We want to know whether values above the mean of one variable tend to occur with values above the mean of the other, or whether high values of one tend to occur with low values of the other.

### Definition

Covariance is

$$ \mathrm{Cov}(X,Y) = \mathbb{E}\!\left[(X-\mathbb{E}[X])(Y-\mathbb{E}[Y])\right]. $$

This should be read as a centered co-movement statistic.

- If both variables tend to be above their means together, or below their means together, the product tends to be positive.
- If one tends to be above its mean when the other is below, the product tends to be negative.
- If there is no consistent linear pattern in those centered movements, covariance may be near zero.

### Interpretation

Covariance is not about raw values. It is about **deviation from each variable’s own mean**.

That detail matters. Covariance is asking whether the variables move together relative to their typical levels. A variable can have a large mean and still have small covariance with another variable if their centered fluctuations do not line up.

### Affine transformations

Covariance interacts with shifts and scalings in predictable ways:

$$
\mathrm{Cov}(aX+b,cY+d)=ac\,\mathrm{Cov}(X,Y).
$$

This means:

- adding constants does not change covariance,
- multiplying by positive constants rescales its magnitude,
- multiplying one variable by a negative constant flips the sign.

Those facts are exactly what we should expect from a statistic measuring centered linear co-movement.

---

## 5. Correlation

Covariance depends on scale. If one variable is measured in dollars and another in cents, the covariance changes even if the dependence pattern is the same. Correlation corrects for that.

It is defined by

$$ \mathrm{Corr}(X,Y) = \frac{\mathrm{Cov}(X,Y)} {\sqrt{\mathrm{Var}(X)\mathrm{Var}(Y)}}. $$

This normalization divides out the variables’ standard deviations, producing a scale-free summary of linear association.

### Why correlation is useful

Correlation is useful when we want to compare relationships across different units or different variables. Covariance says how centered values move together in raw units. Correlation says how strong that co-movement is relative to each variable’s own scale.

### What correlation still does not do

Correlation is still a measure of linear association. It does not detect every kind of dependence. That limitation leads directly to the next key warning.

---

## 6. Zero covariance does not imply independence

This is one of the most important conceptual warnings in elementary probability.

Let $X$ take values $-1,0,1$ with equal probability, and define

$$
Y=X^2.
$$

Then $Y$ is completely determined by $X$, so the variables are obviously dependent.

But

$$ \mathbb{E}[X]=0, \qquad \mathbb{E}[XY]=\mathbb{E}[X^3]=0. $$

So

$$
\mathrm{Cov}(X,Y)=0.
$$

### What this teaches

Covariance only captures linear dependence in centered variables. The relationship $Y=X^2$ is nonlinear and symmetric around zero, so the positive and negative contributions cancel.

So:

- zero covariance means no linear centered association,
- it does **not** mean the variables are fully unrelated,
- it does **not** mean independence.

This distinction becomes extremely important later, especially when Gaussian models are introduced, because some families have special properties that make covariance more informative than it is in general. But in general probability theory, uncorrelated is strictly weaker than independent.

---

## 7. Independence

### What independence is really saying

Independence is a much stronger statement than zero covariance or small correlation.

It says the full joint distribution factorizes into separate marginal pieces:

$$
p(X=x,Y=y)=p(X=x)p(Y=y)
$$

for every pair of values $(x,y)$.

Equivalently,

$$
p(X=x\mid Y=y)=p(X=x)
$$

whenever $p(Y=y)>0$.

These two forms say the same thing, but from different angles:

- the factorization form says the joint table contains no interaction term beyond the marginals;
- the conditional form says observing $Y$ does not change the distribution of $X$.

That is why independence is a structural property of the whole joint distribution, not a vague statement that two variables seem only weakly related.

### Small discrete example

Suppose

$$
p(X=0)=0.7,\qquad p(X=1)=0.3,
$$

and

$$
p(Y=1)=0.2,\quad p(Y=2)=0.3,\quad p(Y=3)=0.4,\quad p(Y=4)=0.1.
$$

If $X$ and $Y$ are independent, then every joint entry is the product of one marginal from $X$ and one from $Y$.

For example,

$$
p(X=1,Y=2)=p(X=1)p(Y=2)=0.3\cdot 0.3=0.09.
$$

The entire joint table is built this way. That is what makes independent models so much simpler than arbitrary joint models.

---

## 8. Degrees of freedom under independence

This is where the simplification becomes quantitative.

Suppose $X$ and $Y$ are both $d$-ary.

A completely general joint table has $d^2$ entries. Because they must sum to one, the unrestricted model has

$$
d^2-1
$$

degrees of freedom.

If $X$ and $Y$ are independent, then

$$
p(X,Y)=p(X)p(Y).
$$

Now we only need to specify the two marginals. Each marginal has $d-1$ free parameters, so the independent model has

$$
(d-1)+(d-1)=2d-2
$$

degrees of freedom.

### Why this matters

This reduction is one of the main reasons independence assumptions are attractive in AI, statistics, and machine learning. They drastically simplify models and reduce parameter counts.

But that simplification comes at a price: independence is a strong claim. If the real joint distribution has structure that matters, forcing factorization may erase exactly the dependence pattern we need to learn.

---

## 9. Conditional independence

In practice, full independence is often too strong. But a weaker and more useful simplification often holds: two variables may become independent **after conditioning on a third variable**.

We write

$$
X \perp Y \mid Z
$$

to mean

$$
p(X,Y\mid Z)=p(X\mid Z)p(Y\mid Z).
$$

This says that once $Z$ is known, the remaining uncertainty in $X$ and $Y$ factorizes.

### Why this matters

Conditional independence is the real structural language behind Bayesian networks, graphical models, hidden-variable models, and many probabilistic learning systems.

So even though this section is about basic probability summaries, it is already pointing toward a much bigger modeling idea:

- unconditional independence is rare and strong,
- conditional independence is often the structural simplification that actually powers useful models.

---

## 10. What to retain

- Expectation summarizes center, not the next realized outcome.
- Linearity of expectation does not require independence.
- Indicator variables are a powerful way to turn counting problems into expectation problems.
- Variance measures spread around the mean.
- Covariance measures centered linear co-movement.
- Correlation rescales covariance into a unit-free measure.
- Zero covariance does not imply independence.
- Independence is a factorization property of the full joint distribution.
- Conditional independence is often the practically important simplification in probabilistic models.

## 11. Do not confuse

- Do not confuse expectation with the most likely value.
- Do not confuse same mean with same distribution.
- Do not assume linearity of expectation needs independence.
- Do not confuse covariance with general dependence.
- Do not confuse zero covariance with independence.
- Do not confuse correlation with causation.
- Do not confuse full independence with conditional independence.

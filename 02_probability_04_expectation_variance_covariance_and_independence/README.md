# 2.4 Expectation, Variance, Covariance, and Independence

This section answers four different questions about random variables.

1. Where is a distribution centered?
2. How spread out is it around that center?
3. If two variables are present, how do they move together?
4. When does the full joint distribution actually split into simpler pieces?

Those questions correspond to four major ideas:

- **expectation** measures center;
- **variance** measures spread around that center;
- **covariance** measures centered co-movement;
- **independence** is a structural factorization property of the joint distribution.

These ideas are related, but they are not interchangeable. One of the most common beginner mistakes is to treat them as if they were all versions of the same summary statistic. They are not. Each one compresses a different aspect of a distribution.

The goal of this section is not merely to list formulas. The goal is to explain what each object means, why the formula has that form, and what the formula can and cannot tell you.

---

## 1. Expectation

### What expectation is trying to summarize

Suppose a discrete random variable $X$ can take several possible values.

A natural question is:

**Where is the distribution located on average?**

Expectation answers that question by forming a weighted average of the possible values, where the weights are the probabilities of those values.

If $X$ has PMF $p_X(x)=\mathbb{P}(X=x)$, then its expectation is

$$
\mathbb{E}[X]=\sum_x x\,p_X(x).
$$

This is the direct probability analogue of an ordinary weighted average.

If one value of $X$ is very likely, it contributes more heavily to the average. If one value is very unlikely, it contributes less.

### Why this formula makes sense

The formula

$$
\mathbb{E}[X]=\sum_x x\,p_X(x)
$$

can be read term by term.

For each possible value $x$:

- the number $x$ tells you what value the variable contributes;
- the factor $p_X(x)$ tells you how often that value occurs in the long run;
- multiplying gives the value weighted by its frequency;
- summing over all possible values gives the long-run average.

So expectation is not a mysterious symbol. It is literally "value times probability, summed over possibilities."

### Bernoulli example

Suppose $X$ is a Bernoulli variable with

$$
\mathbb{P}(X=0)=0.7
$$

and

$$
\mathbb{P}(X=1)=0.3.
$$

Then the expectation is

$$
\mathbb{E}[X]=0\cdot 0.7+1\cdot 0.3.
$$

Now simplify step by step.

Because $0\cdot 0.7=0$, we get

$$
\mathbb{E}[X]=0+0.3.
$$

So

$$
\mathbb{E}[X]=0.3.
$$

This example is especially important because the expectation has a direct interpretation. A Bernoulli variable records failure as $0$ and success as $1$, so its average value is exactly its success probability.

### Fair die example

Let $X$ be the outcome of a fair six-sided die. Then

$$
\mathbb{P}(X=x)=\frac16
$$

for each $x\in\{1,2,3,4,5,6\}$.

Write the expectation formula:

$$
\mathbb{E}[X]=\sum_{x=1}^{6} x\cdot \frac16.
$$

Expand the sum explicitly:

$$
\mathbb{E}[X]=1\cdot \frac16+2\cdot \frac16+3\cdot \frac16+4\cdot \frac16+5\cdot \frac16+6\cdot \frac16.
$$

Factor out the common factor $1/6$:

$$
\mathbb{E}[X]=\frac16(1+2+3+4+5+6).
$$

Add the numbers inside the parentheses:

$$
1+2+3+4+5+6=21.
$$

So

$$
\mathbb{E}[X]=\frac{21}{6}=3.5.
$$

This example matters because a die never lands on $3.5$. So expectation is not "the next value we predict will appear." It is the balance point of the distribution, not necessarily one of the realized outcomes.

### What expectation is not

Expectation is often confused with several different ideas. Those confusions should be removed immediately.

Expectation is **not**:

- the most likely outcome;
- the next value that will be observed;
- a guarantee that the variable ever actually takes that value;
- a description of spread.

Expectation is only a summary of center.

That is why two variables can have the same expectation and still behave very differently. Variance will measure the part expectation cannot capture.

---

## 2. Linearity of expectation

One of the most useful facts in all of probability is

$$
\mathbb{E}[aX+bY+c]=a\,\mathbb{E}[X]+b\,\mathbb{E}[Y]+c.
$$

This is called **linearity of expectation**.

### Why linearity matters

Linearity matters because it lets us compute expectations of sums without first finding the full distribution of the sum.

That is a major simplification.

In many problems, the random quantity we care about can be written as a sum of simpler pieces. Even when the full distribution of that sum is hard to derive, the expectation is often easy because linearity lets us work term by term.

### Independence is not required

This point is important enough to say explicitly:

**Linearity of expectation does not require independence.**

Beginners often remember that products behave differently under dependence and then mistakenly think sums do too. For expectation, sums are always linear whether or not the variables are independent.

### Step-by-step derivation for two variables

Assume for now that $X$ and $Y$ are discrete. Let their joint PMF be $p(x,y)=\mathbb{P}(X=x,Y=y)$.

Then

$$
\mathbb{E}[aX+bY+c]=\sum_x\sum_y (ax+by+c)\,p(x,y).
$$

Distribute the sum across the three terms:

$$
\mathbb{E}[aX+bY+c]=a\sum_x\sum_y x\,p(x,y)+b\sum_x\sum_y y\,p(x,y)+c\sum_x\sum_y p(x,y).
$$

Now treat the three sums one at a time.

For the first sum,

$$
\sum_x\sum_y x\,p(x,y)=\sum_x x\left(\sum_y p(x,y)\right).
$$

But

$$
\sum_y p(x,y)=p_X(x),
$$

the marginal PMF of $X$. So

$$
\sum_x\sum_y x\,p(x,y)=\sum_x x\,p_X(x)=\mathbb{E}[X].
$$

Similarly,

$$
\sum_x\sum_y y\,p(x,y)=\sum_y y\,p_Y(y)=\mathbb{E}[Y].
$$

Finally,

$$
\sum_x\sum_y p(x,y)=1
$$

because the joint PMF sums to $1$.

Substituting those three results back in gives

$$
\mathbb{E}[aX+bY+c]=a\,\mathbb{E}[X]+b\,\mathbb{E}[Y]+c.
$$

Notice that no independence assumption appeared anywhere in the derivation.

### Dependent example

Let $X$ be Bernoulli with

$$
\mathbb{P}(X=1)=0.3
$$

and

$$
\mathbb{P}(X=0)=0.7.
$$

Now define

$$
Y=1-X.
$$

Then $X$ and $Y$ are completely dependent. If you know $X$, then you know $Y$ exactly.

Now compute

$$
X+Y=X+(1-X)=1.
$$

So

$$
\mathbb{E}[X+Y]=\mathbb{E}[1]=1.
$$

Separately,

$$
\mathbb{E}[X]=0.3
$$

and

$$
\mathbb{E}[Y]=\mathbb{E}[1-X]=1-\mathbb{E}[X]=0.7.
$$

Therefore

$$
\mathbb{E}[X]+\mathbb{E}[Y]=0.3+0.7=1.
$$

So linearity still holds even though the variables are fully dependent.

### Indicator variables

An **indicator variable** records whether an event happened.

It is defined by two rules:

- $\mathbf{1}_A=1$ if the event $A$ occurs;
- $\mathbf{1}_A=0$ if the event $A$ does not occur.

Indicator variables are extremely useful because their expectation is just the probability of the event.

To prove that, note that $\mathbf{1}_A$ can only take the values $1$ and $0$. Therefore

$$
\mathbb{E}[\mathbf{1}_A]=1\cdot \mathbb{P}(A)+0\cdot \mathbb{P}(A^c)=\mathbb{P}(A).
$$

This identity is one of the most useful small facts in the section.

### Counting example

Suppose three coin flips are made, and let $H_1,H_2,H_3$ be the indicators for whether the first, second, and third flips are heads.

Let

$$
N=H_1+H_2+H_3.
$$

Then $N$ is the total number of heads.

By linearity,

$$
\mathbb{E}[N]=\mathbb{E}[H_1]+\mathbb{E}[H_2]+\mathbb{E}[H_3].
$$

If each flip has head probability $\rho$, then

$$
\mathbb{E}[H_i]=\rho
$$

for each $i$, because each $H_i$ is an indicator of the event "flip $i$ is heads."

So

$$
\mathbb{E}[N]=\rho+\rho+\rho=3\rho.
$$

This is the deeper lesson:

complicated counts are often easy to take expectations of even when their full distributions are harder to derive.

---

## 3. Variance

### Why expectation is not enough

Expectation tells us where a distribution is centered, but it does not tell us how far typical values lie from that center.

Two variables can share the same expectation while having completely different spreads. Variance is introduced to measure that spread.

### Definition

The variance of $X$ is

$$
\mathrm{Var}(X)=\mathbb{E}\!\left[(X-\mathbb{E}[X])^2\right].
$$

This formula should be read literally:

1. subtract the mean from $X$ to measure deviation from center;
2. square that deviation so negative and positive deviations do not cancel;
3. average the squared deviations.

### Why the square appears

The square is doing two jobs at once.

First, it makes every contribution nonnegative. Without the square, deviations above the mean and below the mean would cancel.

Second, it penalizes large deviations more heavily than small ones.

So variance is not just "another average." It is a summary of spread around the mean.

### Computational identity

The definition

$$
\mathrm{Var}(X)=\mathbb{E}\!\left[(X-\mathbb{E}[X])^2\right]
$$

is conceptually clear, but there is a second formula that is often easier to compute. We now derive it step by step.

Start with the square:

$$
(X-\mathbb{E}[X])^2=X^2-2X\,\mathbb{E}[X]+\mathbb{E}[X]^2.
$$

Take expectations of both sides:

$$
\mathrm{Var}(X)=\mathbb{E}[X^2-2X\,\mathbb{E}[X]+\mathbb{E}[X]^2].
$$

Use linearity of expectation:

$$
\mathrm{Var}(X)=\mathbb{E}[X^2]-2\,\mathbb{E}[X\,\mathbb{E}[X]]+\mathbb{E}[\mathbb{E}[X]^2].
$$

Now use the fact that $\mathbb{E}[X]$ is a constant, not a random variable.

So

$$
\mathbb{E}[X\,\mathbb{E}[X]]=\mathbb{E}[X]\mathbb{E}[X]=\mathbb{E}[X]^2
$$

and

$$
\mathbb{E}[\mathbb{E}[X]^2]=\mathbb{E}[X]^2.
$$

Substitute those into the variance formula:

$$
\mathrm{Var}(X)=\mathbb{E}[X^2]-2\mathbb{E}[X]^2+\mathbb{E}[X]^2.
$$

Combine the last two terms:

$$
\mathrm{Var}(X)=\mathbb{E}[X^2]-\mathbb{E}[X]^2.
$$

This is the computational identity for variance.

### Bernoulli variance

Let $X\in\{0,1\}$ with

$$
\mathbb{P}(X=1)=\rho
$$

and

$$
\mathbb{P}(X=0)=1-\rho.
$$

First compute $\mathbb{E}[X]$:

$$
\mathbb{E}[X]=0\cdot (1-\rho)+1\cdot \rho=\rho.
$$

Now compute $X^2$. Since $0^2=0$ and $1^2=1$, we have

$$
X^2=X
$$

for every Bernoulli outcome.

So

$$
\mathbb{E}[X^2]=\mathbb{E}[X]=\rho.
$$

Now use the computational identity:

$$
\mathrm{Var}(X)=\mathbb{E}[X^2]-\mathbb{E}[X]^2=\rho-\rho^2.
$$

Factor out $\rho$:

$$
\mathrm{Var}(X)=\rho(1-\rho).
$$

This formula is worth interpreting.

- If $\rho$ is near $0$ or $1$, the variable is almost deterministic, so the variance is small.
- If $\rho=1/2$, the two outcomes are maximally uncertain, and the variance is largest.

### Same mean, different variance

Let $X$ be constant at $3$.

Then

$$
\mathbb{P}(X=3)=1.
$$

Let $Y$ take the values $0$ and $6$ with probabilities $1/2$ and $1/2$.

First compute the means.

For $X$,

$$
\mathbb{E}[X]=3.
$$

For $Y$,

$$
\mathbb{E}[Y]=0\cdot \frac12+6\cdot \frac12=3.
$$

So both variables have the same expectation.

Now compute the variances.

For $X$, because $X$ is always equal to its mean,

$$
X-\mathbb{E}[X]=3-3=0
$$

always, so

$$
\mathrm{Var}(X)=0.
$$

For $Y$, use the computational identity.

First compute $Y^2$:

If $Y=0$, then $Y^2=0^2=0$.

If $Y=6$, then $Y^2=6^2=36$.

So $Y^2$ takes the value $0$ with probability $1/2$ and the value $36$ with probability $1/2$.

So

$$
\mathbb{E}[Y^2]=0\cdot \frac12+36\cdot \frac12=18.
$$

Therefore

$$
\mathrm{Var}(Y)=\mathbb{E}[Y^2]-\mathbb{E}[Y]^2=18-3^2=18-9=9.
$$

This example shows why mean and variance are different summaries:

- both variables are centered at $3$;
- one is perfectly concentrated there;
- the other is spread widely around that same center.

### Standard deviation

The **standard deviation** of $X$ is the square root of the variance:

$$
\mathrm{sd}(X)=\sqrt{\mathrm{Var}(X)}.
$$

Variance uses squared units, but standard deviation returns to the same units as the variable itself. That is why standard deviation is often easier to interpret numerically.

### Variance under affine transformations

It is useful to know how variance changes when a variable is shifted or rescaled.

Let

$$
Y=aX+b.
$$

Then

$$
\mathbb{E}[Y]=a\,\mathbb{E}[X]+b
$$

by linearity of expectation.

Now compute the variance:

$$
\mathrm{Var}(Y)=\mathbb{E}\!\left[(Y-\mathbb{E}[Y])^2\right].
$$

Substitute $Y=aX+b$:

$$
\mathrm{Var}(Y)=\mathbb{E}\!\left[(aX+b-(a\,\mathbb{E}[X]+b))^2\right].
$$

The $b$ terms cancel:

$$
\mathrm{Var}(Y)=\mathbb{E}\!\left[(aX-a\,\mathbb{E}[X])^2\right].
$$

Factor out $a$:

$$
\mathrm{Var}(Y)=\mathbb{E}\!\left[a^2(X-\mathbb{E}[X])^2\right].
$$

Since $a^2$ is constant,

$$
\mathrm{Var}(Y)=a^2\,\mathbb{E}\!\left[(X-\mathbb{E}[X])^2\right]=a^2\mathrm{Var}(X).
$$

So:

- adding a constant does not change variance;
- multiplying by $a$ multiplies variance by $a^2$.

---

## 4. Covariance

### Why covariance is introduced

Expectation and variance describe one variable at a time.

Once two variables are present, a new question appears:

**Do the variables tend to rise and fall together, or does one tend to be high when the other is low?**

Covariance is introduced to answer that question.

### Definition

The covariance of $X$ and $Y$ is

$$
\mathrm{Cov}(X,Y)=\mathbb{E}\!\left[(X-\mathbb{E}[X])(Y-\mathbb{E}[Y])\right].
$$

This formula should be read as follows.

For each outcome:

1. measure how far $X$ is from its own mean;
2. measure how far $Y$ is from its own mean;
3. multiply those two centered deviations;
4. average the products.

### Sign interpretation

The sign of the product

$$
(X-\mathbb{E}[X])(Y-\mathbb{E}[Y])
$$

tells us how the two deviations align.

- If both deviations are positive, the product is positive.
- If both deviations are negative, the product is also positive.
- If one is positive and the other is negative, the product is negative.

So:

- positive covariance means the variables tend to be above their means together or below their means together;
- negative covariance means one tends to be above its mean when the other is below;
- covariance near zero means there is no consistent **linear centered** pattern.

### Computational identity

As with variance, there is a computational form that is often easier to use. We now derive it.

Start with the definition:

$$
\mathrm{Cov}(X,Y)=\mathbb{E}\!\left[(X-\mathbb{E}[X])(Y-\mathbb{E}[Y])\right].
$$

Expand the product:

$$
(X-\mathbb{E}[X])(Y-\mathbb{E}[Y])=XY-X\mathbb{E}[Y]-Y\mathbb{E}[X]+\mathbb{E}[X]\mathbb{E}[Y].
$$

Take expectations:

$$
\mathrm{Cov}(X,Y)=\mathbb{E}[XY]-\mathbb{E}[X\mathbb{E}[Y]]-\mathbb{E}[Y\mathbb{E}[X]]+\mathbb{E}[\mathbb{E}[X]\mathbb{E}[Y]].
$$

Now use the fact that $\mathbb{E}[X]$ and $\mathbb{E}[Y]$ are constants:

$$
\mathbb{E}[X\mathbb{E}[Y]]=\mathbb{E}[Y]\mathbb{E}[X],
$$

$$
\mathbb{E}[Y\mathbb{E}[X]]=\mathbb{E}[X]\mathbb{E}[Y],
$$

and

$$
\mathbb{E}[\mathbb{E}[X]\mathbb{E}[Y]]=\mathbb{E}[X]\mathbb{E}[Y].
$$

Substitute these back:

$$
\mathrm{Cov}(X,Y)=\mathbb{E}[XY]-\mathbb{E}[X]\mathbb{E}[Y]-\mathbb{E}[X]\mathbb{E}[Y]+\mathbb{E}[X]\mathbb{E}[Y].
$$

Combine the last three terms:

$$
\mathrm{Cov}(X,Y)=\mathbb{E}[XY]-\mathbb{E}[X]\mathbb{E}[Y].
$$

That is the main computational identity for covariance.

### Special case: covariance with itself

If $Y=X$, then

$$
\mathrm{Cov}(X,X)=\mathbb{E}\!\left[(X-\mathbb{E}[X])^2\right]=\mathrm{Var}(X).
$$

So variance is a special case of covariance.

### Covariance under affine transformations

Let

$$
U=aX+b
$$

and

$$
V=cY+d.
$$

Then

$$
\mathrm{Cov}(U,V)=ac\,\mathrm{Cov}(X,Y).
$$

We now derive it.

First compute the expectations:

$$
\mathbb{E}[U]=a\,\mathbb{E}[X]+b,
$$

$$
\mathbb{E}[V]=c\,\mathbb{E}[Y]+d.
$$

Now subtract the expectations:

$$
U-\mathbb{E}[U]=aX+b-(a\,\mathbb{E}[X]+b)=a(X-\mathbb{E}[X]),
$$

$$
V-\mathbb{E}[V]=cY+d-(c\,\mathbb{E}[Y]+d)=c(Y-\mathbb{E}[Y]).
$$

Multiply them:

$$
(U-\mathbb{E}[U])(V-\mathbb{E}[V])=ac(X-\mathbb{E}[X])(Y-\mathbb{E}[Y]).
$$

Take expectations:

$$
\mathrm{Cov}(U,V)=ac\,\mathbb{E}\!\left[(X-\mathbb{E}[X])(Y-\mathbb{E}[Y])\right].
$$

So

$$
\mathrm{Cov}(aX+b,cY+d)=ac\,\mathrm{Cov}(X,Y).
$$

This tells us:

- adding constants does not change covariance;
- scaling one variable rescales covariance by the same factor;
- a negative scaling flips the sign.

---

## 5. Correlation

Covariance depends on units.

If one variable is measured in dollars and then re-expressed in cents, the covariance changes numerically even if the underlying dependence pattern is the same.

Correlation corrects for this by dividing out the variables' standard deviations.

If $\mathrm{Var}(X)>0$ and $\mathrm{Var}(Y)>0$, the correlation is

$$
\mathrm{Corr}(X,Y)=\frac{\mathrm{Cov}(X,Y)}{\sqrt{\mathrm{Var}(X)\mathrm{Var}(Y)}}.
$$

### Why correlation is scale-free

Suppose we replace $X$ by $100X$. Then

$$
\mathrm{Cov}(100X,Y)=100\,\mathrm{Cov}(X,Y)
$$

and

$$
\sqrt{\mathrm{Var}(100X)\mathrm{Var}(Y)}=\sqrt{100^2\mathrm{Var}(X)\mathrm{Var}(Y)}=100\sqrt{\mathrm{Var}(X)\mathrm{Var}(Y)}.
$$

So the factor of $100$ cancels in the ratio, leaving correlation unchanged.

That is why correlation is a unit-free measure of linear association.

### Why correlation must lie between -1 and 1

This is a standard fact, and it can be proved with only variance algebra.

Define the standardized variables

$$
U=\frac{X-\mathbb{E}[X]}{\sqrt{\mathrm{Var}(X)}}
$$

and

$$
V=\frac{Y-\mathbb{E}[Y]}{\sqrt{\mathrm{Var}(Y)}}.
$$

Then

$$
\mathbb{E}[U]=0,\qquad \mathbb{E}[V]=0,
$$

and

$$
\mathrm{Var}(U)=1,\qquad \mathrm{Var}(V)=1.
$$

Also,

$$
\mathrm{Cov}(U,V)=\mathrm{Corr}(X,Y).
$$

Now consider the variance of $U+V$:

$$
\mathrm{Var}(U+V)=\mathrm{Var}(U)+\mathrm{Var}(V)+2\,\mathrm{Cov}(U,V).
$$

Substitute the known values:

$$
\mathrm{Var}(U+V)=1+1+2\,\mathrm{Corr}(X,Y)=2+2\,\mathrm{Corr}(X,Y).
$$

Variance is always nonnegative, so

$$
2+2\,\mathrm{Corr}(X,Y)\ge 0.
$$

Therefore

$$
\mathrm{Corr}(X,Y)\ge -1.
$$

Now consider the variance of $U-V$:

$$
\mathrm{Var}(U-V)=\mathrm{Var}(U)+\mathrm{Var}(V)-2\,\mathrm{Cov}(U,V)=2-2\,\mathrm{Corr}(X,Y).
$$

Again variance is nonnegative, so

$$
2-2\,\mathrm{Corr}(X,Y)\ge 0.
$$

Therefore

$$
\mathrm{Corr}(X,Y)\le 1.
$$

Combining the two inequalities gives

$$
-1\le \mathrm{Corr}(X,Y)\le 1.
$$

### What correlation still does not tell us

Correlation measures linear association only.

So even a correlation of zero does **not** imply full independence. That distinction is important enough to get its own section next.

---

## 6. Zero covariance does not imply independence

This is one of the most important warning statements in elementary probability.

Let $X$ take the values $-1,0,1$ with equal probabilities:

$$
\mathbb{P}(X=-1)=\mathbb{P}(X=0)=\mathbb{P}(X=1)=\frac13.
$$

Now define

$$
Y=X^2.
$$

Then $Y$ is completely determined by $X$. So $X$ and $Y$ are certainly dependent.

We now compute the covariance anyway.

### Step 1: compute $\mathbb{E}[X]$

$$
\mathbb{E}[X]=(-1)\cdot \frac13+0\cdot \frac13+1\cdot \frac13=0.
$$

### Step 2: compute $XY$

Because $Y=X^2$, we have

$$
XY=X\cdot X^2=X^3.
$$

So it is enough to compute $\mathbb{E}[X^3]$.

### Step 3: compute $\mathbb{E}[XY]$

$$
\mathbb{E}[XY]=\mathbb{E}[X^3]=(-1)^3\cdot \frac13+0^3\cdot \frac13+1^3\cdot \frac13=0.
$$

### Step 4: compute covariance

Use the computational identity:

$$
\mathrm{Cov}(X,Y)=\mathbb{E}[XY]-\mathbb{E}[X]\mathbb{E}[Y].
$$

We already know

$$
\mathbb{E}[XY]=0
$$

and

$$
\mathbb{E}[X]=0.
$$

Therefore

$$
\mathrm{Cov}(X,Y)=0-0\cdot \mathbb{E}[Y]=0.
$$

So the covariance is zero.

### Why the variables are still dependent

Even though the covariance is zero, the variables are not independent because $Y$ is determined by $X$.

For example, if $X=0$, then

$$
Y=0
$$

with probability $1$.

But marginally, $Y$ is not always $0$. In fact,

$$
\mathbb{P}(Y=0)=\mathbb{P}(X=0)=\frac13.
$$

So

$$
\mathbb{P}(Y=0\mid X=0)=1
$$

while

$$
\mathbb{P}(Y=0)=\frac13.
$$

These are not equal, so $Y$ depends on $X$.

This example teaches the exact boundary:

- zero covariance means no linear centered association;
- it does **not** mean no dependence;
- it does **not** mean independence.

The term **uncorrelated** means "covariance zero." Uncorrelated is weaker than independent.

---

## 7. Independence

### What independence is really saying

Independence is a much stronger statement than covariance zero.

For discrete variables, $X$ and $Y$ are independent if

$$
\mathbb{P}(X=x,Y=y)=\mathbb{P}(X=x)\mathbb{P}(Y=y)
$$

for every pair of values $(x,y)$.

This says the full joint distribution factorizes into separate marginal pieces.

### Equivalent conditional form

If $\mathbb{P}(Y=y)>0$, then the conditional probability formula gives

$$
\mathbb{P}(X=x\mid Y=y)=\frac{\mathbb{P}(X=x,Y=y)}{\mathbb{P}(Y=y)}.
$$

Now assume independence, so

$$
\mathbb{P}(X=x,Y=y)=\mathbb{P}(X=x)\mathbb{P}(Y=y).
$$

Substitute that into the conditional formula:

$$
\mathbb{P}(X=x\mid Y=y)=\frac{\mathbb{P}(X=x)\mathbb{P}(Y=y)}{\mathbb{P}(Y=y)}.
$$

Cancel the factor $\mathbb{P}(Y=y)$:

$$
\mathbb{P}(X=x\mid Y=y)=\mathbb{P}(X=x).
$$

So independence implies that observing $Y$ does not change the distribution of $X$.

Conversely, if

$$
\mathbb{P}(X=x\mid Y=y)=\mathbb{P}(X=x)
$$

for all $x,y$ with $\mathbb{P}(Y=y)>0$, then multiply both sides by $\mathbb{P}(Y=y)$:

$$
\mathbb{P}(X=x,Y=y)=\mathbb{P}(X=x)\mathbb{P}(Y=y).
$$

So the factorization form and the conditional form are equivalent.

### Small discrete example

Suppose

$$
\mathbb{P}(X=0)=0.7,\qquad \mathbb{P}(X=1)=0.3,
$$

and

$$
\mathbb{P}(Y=1)=0.2,\qquad \mathbb{P}(Y=2)=0.3,\qquad \mathbb{P}(Y=3)=0.4,\qquad \mathbb{P}(Y=4)=0.1.
$$

If $X$ and $Y$ are independent, then each joint entry is just a product.

For example,

$$
\mathbb{P}(X=1,Y=2)=\mathbb{P}(X=1)\mathbb{P}(Y=2)=0.3\cdot 0.3=0.09.
$$

Likewise,

$$
\mathbb{P}(X=0,Y=4)=0.7\cdot 0.1=0.07.
$$

That is what independence buys you: the entire joint table is determined by the marginals.

### Degrees of freedom under independence

This simplification can be counted explicitly.

Suppose $X$ and $Y$ are both **$d$-ary**, meaning each one has exactly $d$ possible values.

For example:

- a binary variable is $2$-ary;
- a weather variable with values {sun, cloud, rain} is $3$-ary.

Now define **degrees of freedom**.

Degrees of freedom means:

**How many numerical entries may be chosen freely before the normalization constraints determine the rest?**

For a completely general joint table of two $d$-ary variables:

- there are $d^2$ joint probabilities;
- they must sum to $1$;
- once $d^2-1$ of them are chosen, the last one is forced by the sum-to-one rule.

So the unrestricted joint model has

$$
d^2-1
$$

degrees of freedom.

If the variables are independent, we no longer choose a full joint table directly. We choose two marginals.

Each $d$-ary marginal has:

- $d$ entries,
- one sum-to-one constraint,
- therefore $d-1$ degrees of freedom.

Since there are two marginals, the independent model has

$$
(d-1)+(d-1)=2d-2
$$

degrees of freedom.

### Concrete example: $d=3$

If both variables are $3$-ary, then:

- a general joint table has $3^2=9$ entries and therefore $8$ degrees of freedom;
- an independent model has $2(3-1)=4$ degrees of freedom.

So independence cuts the parameter count in half in this example.

This is one major reason independence assumptions are attractive in probability, statistics, and machine learning: they simplify models dramatically.

But the simplification only helps if independence is actually a reasonable structural assumption.

---

## 8. Pairwise independence versus mutual independence

Another important misconception is the idea that if every pair of variables is independent, then the whole collection must be independent. That is false.

### Definitions

Three variables $A,B,C$ are **pairwise independent** if every pair is independent:

$$
A\perp B,\qquad A\perp C,\qquad B\perp C.
$$

They are **mutually independent** if every joint factorization also holds, in particular

$$
\mathbb{P}(A=a,B=b,C=c)=\mathbb{P}(A=a)\mathbb{P}(B=b)\mathbb{P}(C=c)
$$

for every triple $(a,b,c)$.

Mutual independence implies pairwise independence, but the converse is not true.

### Worked example

Let $U$ and $V$ be independent fair coin bits taking values in $\{0,1\}$, each with probability $1/2$ for each value.

Define

$$
A=U,
$$

$$
B=V,
$$

and

$$
C=U\oplus V,
$$

where $\oplus$ means exclusive OR: $C=1$ exactly when $U$ and $V$ are different.

The four equally likely outcomes are:

| $U$ | $V$ | $A$ | $B$ | $C$ | probability |
|---|---|---|---|---|---:|
| 0 | 0 | 0 | 0 | 0 | $1/4$ |
| 0 | 1 | 0 | 1 | 1 | $1/4$ |
| 1 | 0 | 1 | 0 | 1 | $1/4$ |
| 1 | 1 | 1 | 1 | 0 | $1/4$ |

Now check pairwise independence.

For $(A,B)$, all four pairs $(0,0),(0,1),(1,0),(1,1)$ occur with probability $1/4$, so $A$ and $B$ are independent.

For $(A,C)$, all four pairs again occur with probability $1/4$, so $A$ and $C$ are independent.

For $(B,C)$, the same is true, so $B$ and $C$ are independent.

Thus the variables are pairwise independent.

But they are not mutually independent, because

$$
C=A\oplus B
$$

holds exactly.

In particular,

$$
\mathbb{P}(A=1,B=1,C=1)=0
$$

since whenever $A=1$ and $B=1$, we must have $C=0$.

However, if the three variables were mutually independent, we would have

$$
\mathbb{P}(A=1,B=1,C=1)=\mathbb{P}(A=1)\mathbb{P}(B=1)\mathbb{P}(C=1)=\frac12\cdot\frac12\cdot\frac12=\frac18.
$$

Since $0\neq 1/8$, mutual independence fails.

So pairwise independence is weaker than mutual independence.

---

## 9. Conditional independence

Full independence is often too strong to be realistic. A weaker and more useful structure is **conditional independence**.

We write

$$
X\perp Y \mid Z
$$

to mean that once $Z$ is known, the remaining uncertainty in $X$ and $Y$ factorizes.

For discrete variables, the definition is:

$$
\mathbb{P}(X=x,Y=y\mid Z=z)=\mathbb{P}(X=x\mid Z=z)\mathbb{P}(Y=y\mid Z=z)
$$

for every $z$ with positive probability.

### What this means in words

Conditional independence says:

- before $Z$ is known, $X$ and $Y$ may be dependent;
- after $Z$ is fixed, the dependence disappears.

So the variable $Z$ explains the association.

### Worked example

Let $Z$ be a hidden binary state with

$$
\mathbb{P}(Z=0)=\frac12,\qquad \mathbb{P}(Z=1)=\frac12.
$$

Now define two binary observations $X$ and $Y$ as follows.

If $Z=0$, let

$$
\mathbb{P}(X=1\mid Z=0)=0.1,\qquad \mathbb{P}(Y=1\mid Z=0)=0.1.
$$

If $Z=1$, let

$$
\mathbb{P}(X=1\mid Z=1)=0.9,\qquad \mathbb{P}(Y=1\mid Z=1)=0.9.
$$

Assume that once $Z$ is fixed, the variables $X$ and $Y$ are generated independently.

That means, for example,

$$
\mathbb{P}(X=1,Y=1\mid Z=0)=0.1\cdot 0.1=0.01
$$

and

$$
\mathbb{P}(X=1,Y=1\mid Z=1)=0.9\cdot 0.9=0.81.
$$

So by construction,

$$
X\perp Y \mid Z.
$$

Now look at the variables marginally, without conditioning on $Z$.

First compute $\mathbb{P}(X=1)$:

$$
\mathbb{P}(X=1)=\mathbb{P}(X=1\mid Z=0)\mathbb{P}(Z=0)+\mathbb{P}(X=1\mid Z=1)\mathbb{P}(Z=1).
$$

Substitute the numbers:

$$
\mathbb{P}(X=1)=0.1\cdot \frac12+0.9\cdot \frac12=0.5.
$$

Similarly,

$$
\mathbb{P}(Y=1)=0.5.
$$

Now compute the joint probability:

$$
\mathbb{P}(X=1,Y=1)=\mathbb{P}(X=1,Y=1\mid Z=0)\mathbb{P}(Z=0)+\mathbb{P}(X=1,Y=1\mid Z=1)\mathbb{P}(Z=1).
$$

Substitute the numbers:

$$
\mathbb{P}(X=1,Y=1)=0.01\cdot \frac12+0.81\cdot \frac12=0.41.
$$

If $X$ and $Y$ were marginally independent, we would need

$$
\mathbb{P}(X=1,Y=1)=\mathbb{P}(X=1)\mathbb{P}(Y=1)=0.5\cdot 0.5=0.25.
$$

But

$$
0.41\neq 0.25.
$$

So $X$ and $Y$ are **not** marginally independent even though they **are** conditionally independent given $Z$.

This is the most important structural lesson of the section:

conditioning can remove dependence when the dependence is created by mixing over a hidden common cause.

---

## 10. What to retain

- Expectation measures center, not the most likely next value.
- Linearity of expectation does not require independence.
- Indicator variables turn probability questions into expectation questions.
- Variance measures spread around the mean.
- Covariance measures centered linear co-movement.
- Correlation is the scale-free version of covariance.
- Zero covariance does not imply independence.
- Independence is a factorization property of the full joint distribution.
- Pairwise independence is weaker than mutual independence.
- Conditional independence is often the practically useful structural simplification.

## 11. Do not confuse

- Do not confuse expectation with the most likely value.
- Do not confuse same mean with same distribution.
- Do not assume linearity of expectation requires independence.
- Do not confuse variance with general uncertainty about every aspect of shape.
- Do not confuse covariance with arbitrary dependence.
- Do not confuse zero covariance with independence.
- Do not confuse pairwise independence with mutual independence.
- Do not confuse independence with conditional independence.

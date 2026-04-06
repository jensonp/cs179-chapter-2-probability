# 2.5 Continuous Random Variables

This section rebuilds probability for variables that take values on a continuum rather than on a finite or countable list of isolated states.

The main beginner difficulty is not usually algebra. It is carrying a discrete mental model into a setting where that model is no longer correct. In the discrete setting, it makes sense to ask for the probability of one exact state. In the continuous setting, the central quantity is usually the probability of an interval or region, not of one single point.

So the section has one main job: replace the wrong intuition before later formulas are introduced.

We will proceed in the following order:

1. start from the universal object, the CDF;
2. define what a PDF is and what it is not;
3. contrast PMFs, PDFs, and CDFs using worked examples;
4. build the Gaussian from one dimension to many dimensions;
5. explain Beta and Dirichlet distributions as distributions over unknown parameters rather than over observed outcomes.

---

## 1. The universal starting point: the CDF

Before discussing discrete or continuous cases separately, it helps to start from the one object that always exists for a real-valued random variable.

For a real-valued random variable $X$, the cumulative distribution function is

$$
F_X(x)=P(X\le x).
$$

This definition makes sense whether $X$ is discrete, continuous, or mixed.

The CDF answers a threshold question:

- "How much total probability has accumulated by the time we reach the point $x$ on the number line?"

That is why the CDF is the safest object to begin with. Every real-valued random variable has a CDF. Not every real-valued random variable has a PMF. Not every real-valued random variable has a PDF. But every real-valued random variable has a CDF.

### Basic facts about CDFs

For every real-valued random variable:

1. $0\le F_X(x)\le 1$ for every $x$.
2. $F_X(x)$ is nondecreasing in $x$.
3. $\lim_{x\to -\infty}F_X(x)=0$.
4. $\lim_{x\to \infty}F_X(x)=1$.
5. $F_X(x)$ is right-continuous.

These facts are not arbitrary rules. They follow directly from the event definition $X\le x$:

- if $x$ increases, the event $\{X\le x\}$ can only get larger, so its probability cannot decrease;
- very far to the left, the event becomes impossible, so the probability tends to $0$;
- very far to the right, the event eventually contains all outcomes, so the probability tends to $1$.

### Interval probabilities from the CDF

The CDF is useful because interval probabilities can be recovered from it.

For $a<b$,

$$
P(a<X\le b)=F_X(b)-F_X(a).
$$

Why does this work? Because the event $\{X\le b\}$ can be decomposed into two disjoint pieces:

- the outcomes with $X\le a$;
- the outcomes with $a<X\le b$.

So

$$
P(X\le b)=P(X\le a)+P(a<X\le b).
$$

Subtracting $P(X\le a)$ from both sides gives the formula above.

This identity is universal. It works in discrete settings, continuous settings, and mixed settings.

---

## 2. Why the discrete picture stops working

In the discrete setting, a PMF directly answers questions of the form

$$
P(X=x).
$$

That works because an isolated state such as $x=0$ or $x=7$ can carry positive probability mass.

In a continuous setting, that logic fails. The probability is spread across infinitely many nearby values. An individual point usually carries no mass at all.

For a genuinely continuous variable with density $p(x)$,

$$
P(X=x)=0 \quad \text{for every single point } x.
$$

This sentence often feels wrong the first time one sees it, so it is worth explaining carefully.

Suppose $X$ is uniform on $[0,1]$. Intuitively, the variable can land anywhere in that interval. But if any single point, say $x=0.37$, had positive probability, then the infinitely many points in $[0,1]$ would force the total probability to exceed $1$. So the probability must be spread over intervals, not stored at points.

That is why continuous probability uses densities rather than point masses.

---

## 3. Probability density functions

A real-valued random variable $X$ has a probability density function, or PDF, if there exists a nonnegative function $p_X(x)$ such that

$$
P(X\in A)=\int_A p_X(x)\,dx
$$

for every interval or region $A$ on the real line.

Because the whole real line must carry total probability $1$, the density must satisfy

$$
\int_{-\infty}^{\infty} p_X(x)\,dx = 1.
$$

So a PDF is not a second random variable or a separate probabilistic object. It is the function that reproduces the probabilities of $X$ through integration.

### What a density is

A density is not itself a probability. A density is a quantity that must be integrated to produce a probability.

The best beginner interpretation is:

- a PMF gives probability at a point;
- a PDF gives probability per unit of horizontal distance near a point;
- an actual probability comes from accumulating that density over an interval.

That is why the PDF is called a density.

### How the PDF connects back to the CDF

If $X$ has density $p_X$, then its CDF can be written as

$$
F_X(x)=\int_{-\infty}^{x} p_X(t)\,dt.
$$

This formula matters because it reconnects the continuous story to the universal object from the start of the section. In the absolutely continuous case, the PDF is the local rate at which the CDF accumulates mass.

Where the derivative exists,

$$
F_X'(x)=p_X(x).
$$

That does not mean the CDF and PDF are interchangeable. It means the PDF is obtained by differentiating the CDF in the continuous case, while probabilities are still read from the CDF or from interval integrals.

### Small-interval approximation

If $p(x)$ is smooth near a point $x$, then for a very small interval of width $\Delta$,

$$
P(x\le X\le x+\Delta)\approx p(x)\Delta.
$$

This approximation explains the phrase "probability per unit $x$." The density value $p(x)$ behaves like a local height, and multiplying by a small width $\Delta$ produces a small area.

### Why a density may exceed 1

Because density is not the same as probability, a density value may be larger than $1$.

For example, on the interval $[0,\tfrac12]$, the uniform density is

$$
p(x)=2 \quad \text{for } 0\le x\le \tfrac12.
$$

This does not violate probability rules, because the total probability is the integral:

$$
\int_0^{1/2} 2\,dx = 2\cdot \frac12 = 1.
$$

So the requirement is not "height must be at most 1." The requirement is "total area must equal 1."

### What a PDF does not answer

A PDF does not answer the question

$$
P(X=x).
$$

For a continuous variable, that probability is $0$ no matter what the density height is.

That is the first major "do not confuse" boundary in the section.

---

## 4. Uniform density on an interval

The simplest continuous density is the uniform density on an interval.

Suppose $X$ is uniform on $[0,T]$. "Uniform" means that equal-length subintervals have equal probability. So the density should be constant on the interval.

Write that constant as $c$. Then the density must be

| $p(x)$ | condition on $x$ |
|---|---|
| $c$ | $0\le x\le T$ |
| $0$ | otherwise |

The constant $c$ is not arbitrary. It must be chosen so that the total area is $1$.

Step 1: write the normalization equation.

$$
\int_{-\infty}^{\infty} p(x)\,dx = 1.
$$

Step 2: use the fact that the density is $0$ outside $[0,T]$.

$$
\int_0^T c\,dx = 1.
$$

Step 3: integrate the constant.

$$
c\int_0^T 1\,dx = 1.
$$

Step 4: evaluate the interval length.

$$
c(T-0)=1.
$$

So

$$
cT=1.
$$

Finally,

$$
c=\frac1T.
$$

Therefore the uniform density on $[0,T]$ is

| $p(x)$ | condition on $x$ |
|---|---|
| $1/T$ | $0\le x\le T$ |
| $0$ | otherwise |

### Worked example: uniform on $[0,2]$

If $X\sim \mathrm{Unif}([0,2])$, then

$$
p(x)=\frac12 \quad \text{for } 0\le x\le 2.
$$

Now compute the probability of the interval $[0.3,0.9]$.

Step 1: start from the interval formula.

$$
P(0.3\le X\le 0.9)=\int_{0.3}^{0.9} p(x)\,dx.
$$

Step 2: substitute the density on that interval.

$$
P(0.3\le X\le 0.9)=\int_{0.3}^{0.9}\frac12\,dx.
$$

Step 3: pull out the constant.

$$
P(0.3\le X\le 0.9)=\frac12\int_{0.3}^{0.9} 1\,dx.
$$

Step 4: compute the interval length.

$$
P(0.3\le X\le 0.9)=\frac12(0.9-0.3).
$$

Step 5: simplify.

$$
P(0.3\le X\le 0.9)=\frac12(0.6)=0.3.
$$

The calculation is simple, but the concept is important: probability came from area, which here equals height times width.

---

## 5. PMF, PDF, and CDF: what each one answers

Many beginner confusions disappear if each object is tied to a question.

### PMF

A probability mass function belongs to a discrete random variable. It answers:

$$
\text{What probability is assigned to the exact value } x\text{?}
$$

Formally,

$$
p_X(x)=P(X=x).
$$

### PDF

A probability density function belongs to an absolutely continuous random variable. It answers:

$$
\text{How densely is probability packed near the location } x\text{?}
$$

Formally, probabilities come from integration:

$$
P(a\le X\le b)=\int_a^b p_X(x)\,dx.
$$

### CDF

A cumulative distribution function belongs to every real-valued random variable. It answers:

$$
\text{How much total probability lies to the left of } x\text{?}
$$

Formally,

$$
F_X(x)=P(X\le x).
$$

### Why the CDF is the universal object

Every real-valued random variable has left-of-threshold events such as $X\le x$, so every real-valued random variable has a CDF.

But:

- only discrete variables have PMFs in the usual sense;
- only absolutely continuous variables have PDFs;
- mixed variables may have neither a pure PMF nor a pure PDF that describes everything by itself.

So if you ever lose track of what object should be used, start from the CDF.

---

## 6. Discrete, continuous, and mixed CDFs

The CDF is easiest to understand when one sees the three main shapes side by side.

### Discrete example: Bernoulli

Suppose

$$
P(X=0)=0.7 \quad \text{and} \quad P(X=1)=0.3.
$$

We now compute the CDF directly from the definition $F_X(x)=P(X\le x)$.

#### Case 1: $x<0$

If $x<0$, then neither $0$ nor $1$ is less than or equal to $x$. So the event $X\le x$ is impossible.

Therefore

$$
F_X(x)=0 \quad \text{for } x<0.
$$

#### Case 2: $0\le x<1$

If $x$ lies between $0$ and $1$, then the value $0$ is included but the value $1$ is not.

So

$$
F_X(x)=P(X=0)=0.7 \quad \text{for } 0\le x<1.
$$

#### Case 3: $x\ge 1$

If $x\ge 1$, then both possible values are included.

So

$$
F_X(x)=P(X=0)+P(X=1)=0.7+0.3=1 \quad \text{for } x\ge 1.
$$

Putting the cases together:

| $F_X(x)$ | condition on $x$ |
|---|---|
| $0$ | $x<0$ |
| $0.7$ | $0\le x<1$ |
| $1$ | $x\ge 1$ |

The key visual feature is the jump. In a discrete CDF, jumps occur exactly where point masses are located.

### Continuous example: uniform on $[0,2]$

Now let $X\sim \mathrm{Unif}([0,2])$ with density $p(x)=\tfrac12$ on $[0,2]$.

Again compute the CDF from the definition.

#### Case 1: $x<0$

The variable cannot land below $0$, so

$$
F_X(x)=0 \quad \text{for } x<0.
$$

#### Case 2: $0\le x\le 2$

Now

$$
F_X(x)=P(X\le x)=\int_0^x \frac12\,dt.
$$

Pull out the constant:

$$
F_X(x)=\frac12\int_0^x 1\,dt.
$$

Evaluate the integral:

$$
F_X(x)=\frac12(x-0)=\frac{x}{2} \quad \text{for } 0\le x\le 2.
$$

#### Case 3: $x>2$

By the time the threshold passes $2$, all probability has already been accumulated, so

$$
F_X(x)=1 \quad \text{for } x>2.
$$

Putting the cases together:

| $F_X(x)$ | condition on $x$ |
|---|---|
| $0$ | $x<0$ |
| $x/2$ | $0\le x\le 2$ |
| $1$ | $x>2$ |

The key visual feature is that the CDF rises smoothly rather than jumping.

### Mixed example

A mixed distribution has both a point mass and a continuous part.

For example, suppose:

- with probability $0.7$, the variable equals exactly $0$;
- with probability $0.3$, the variable is uniform on $[0,1]$.

This means the continuous part contributes density

$$
0.3 \quad \text{on } [0,1],
$$

because a uniform density on $[0,1]$ has height $1$, and the total continuous mass is scaled down to $0.3$.

Now compute the CDF.

#### Case 1: $x<0$

Nothing has accumulated yet, so

$$
F_X(x)=0.
$$

#### Case 2: $x=0$

At $x=0$, the atom at $0$ is included. So

$$
F_X(0)=0.7.
$$

#### Case 3: $0<x<1$

Now the point mass at $0$ is still included, and the continuous part contributes the interval probability from $0$ to $x$:

$$
F_X(x)=0.7+\int_0^x 0.3\,dt.
$$

Compute the integral:

$$
F_X(x)=0.7+0.3x \quad \text{for } 0<x<1.
$$

#### Case 4: $x\ge 1$

All mass has accumulated, so

$$
F_X(x)=1 \quad \text{for } x\ge 1.
$$

This example shows why the CDF is universal: it can handle jumps and smooth accumulation in one object.

---

## 7. One-dimensional Gaussian distributions

The Gaussian family is the most important continuous family in elementary probability and in much of later machine learning.

### What object is being defined

A one-dimensional Gaussian is a density on the whole real line:

$$
p(x)=\mathcal{N}(x;\mu,\sigma^2)=\frac{1}{\sqrt{2\pi\sigma^2}}\exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right).
$$

Here:

- $\mu$ is the mean;
- $\sigma^2$ is the variance;
- $\sigma$ is the standard deviation.

### What each part of the formula does

The formula has two conceptually different parts.

#### The exponential term

The factor

$$
\exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)
$$

controls shape.

Read the exponent from the inside out:

1. compute the deviation from the mean, $x-\mu$;
2. square it, so positive and negative deviations are treated symmetrically;
3. divide by $2\sigma^2$, so larger variance makes the decay slower;
4. place a minus sign in front, so larger squared distance gives smaller density.

So points near $\mu$ get more density, and points far from $\mu$ get less density.

#### The normalization constant

The factor

$$
\frac{1}{\sqrt{2\pi\sigma^2}}
$$

does not determine the bell shape. Its job is to make the total area equal to $1$.

In other words:

- the exponential term says what shape we want;
- the prefactor rescales that shape into a valid density.

### Why Gaussians matter

Gaussians matter for two separate reasons:

1. they are mathematically tractable;
2. they often provide good models or approximations for noise and aggregate variation.

The second point is a modeling heuristic, not a universal law. It is common, not automatic.

---

## 8. Standardization and the standard normal

If

$$
X\sim \mathcal{N}(\mu,\sigma^2),
$$

define

$$
Z=\frac{X-\mu}{\sigma}.
$$

This transformation is called standardization.

### Why this transformation is used

Standardization does two jobs at once.

#### Step 1: subtract the mean

Subtracting $\mu$ moves the center to $0$.

#### Step 2: divide by the standard deviation

Dividing by $\sigma$ changes the unit of measurement from "raw units of $X$" to "number of standard deviations away from the mean."

After this transformation,

$$
Z\sim \mathcal{N}(0,1).
$$

This special Gaussian is called the standard normal.

One quick justification is to rewrite the Gaussian density at the point $x=\mu+\sigma z$. Then

$$
\frac{(x-\mu)^2}{2\sigma^2}=\frac{(\mu+\sigma z-\mu)^2}{2\sigma^2}=\frac{\sigma^2 z^2}{2\sigma^2}=\frac{z^2}{2}.
$$

so subtracting $\mu$ removes location and dividing by $\sigma$ removes scale. What remains is the standard bell curve centered at $0$ with unit variance.

### The standard normal CDF

The CDF of the standard normal is written

$$
\Phi(z)=P(Z\le z).
$$

The reason $\Phi$ matters is computational:

every Gaussian interval question can be turned into a standard-normal interval question.

### General Gaussian interval formula

Suppose $X\sim \mathcal{N}(\mu,\sigma^2)$. Then

$$
P(a\le X\le b)=P\!\left(\frac{a-\mu}{\sigma}\le Z\le \frac{b-\mu}{\sigma}\right).
$$

Using the CDF subtraction rule,

$$
P(a\le X\le b)=\Phi\!\left(\frac{b-\mu}{\sigma}\right)-\Phi\!\left(\frac{a-\mu}{\sigma}\right).
$$

That is the real point of standardization. It is not a decorative algebraic move. It is the bridge from an arbitrary Gaussian to the one standard table or software function $\Phi$.

### Worked example: $X\sim \mathcal{N}(2,9)$

Suppose

$$
X\sim \mathcal{N}(2,9).
$$

Then:

- $\mu=2$;
- $\sigma^2=9$;
- $\sigma=3$.

Now compute

$$
P(-1\le X\le 5).
$$

Step 1: standardize the left endpoint.

$$
\frac{-1-\mu}{\sigma}=\frac{-1-2}{3}=\frac{-3}{3}=-1.
$$

Step 2: standardize the right endpoint.

$$
\frac{5-\mu}{\sigma}=\frac{5-2}{3}=\frac{3}{3}=1.
$$

Step 3: rewrite the probability in terms of $Z$.

$$
P(-1\le X\le 5)=P(-1\le Z\le 1).
$$

Step 4: express it using the standard-normal CDF.

$$
P(-1\le X\le 5)=\Phi(1)-\Phi(-1).
$$

That is the complete computation pipeline:

1. identify $\mu$ and $\sigma$;
2. standardize endpoints;
3. rewrite as a standard-normal interval;
4. evaluate with $\Phi$.

### The 68-95-99.7 rule

For the standard normal,

$$
P(|Z|\le 1)\approx 0.68, \quad P(|Z|\le 2)\approx 0.95, \quad P(|Z|\le 3)\approx 0.997.
$$

Because every Gaussian standardizes to $Z$, this implies:

- about 68% of Gaussian mass lies within one standard deviation of the mean;
- about 95% lies within two standard deviations;
- about 99.7% lies within three standard deviations.

These are approximations, not exact identities, but they are useful sanity checks.

---

## 9. Multivariate Gaussian distributions

The one-dimensional Gaussian describes one number. A multivariate Gaussian describes several numbers observed together.

### The random vector

Instead of one scalar variable, write

$$
X=(X_1,\dots,X_n)^T.
$$

Now one outcome is not a single point on a line. It is a point in $n$-dimensional space.

### The mean vector

The center is now described coordinate by coordinate:

$$
\mu=\mathbb{E}[X]=\bigl(\mathbb{E}[X_1],\dots,\mathbb{E}[X_n]\bigr)^T.
$$

This means:

- the first component of $\mu$ is the average value of $X_1$;
- the second component is the average value of $X_2$;
- and so on.

### The covariance matrix

Spread and joint movement are summarized by the covariance matrix

$$
\Sigma=\mathbb{E}\!\left[(X-\mu)(X-\mu)^T\right].
$$

Its $(i,j)$ entry is

$$
\Sigma_{ij}=\mathrm{Cov}(X_i,X_j).
$$

This means:

- diagonal entry $\Sigma_{ii}$ is the variance of coordinate $i$;
- off-diagonal entry $\Sigma_{ij}$ tells how coordinates $i$ and $j$ move together.

So the covariance matrix combines two kinds of information:

1. how spread out each coordinate is by itself;
2. whether pairs of coordinates tend to rise and fall together.

Because covariance is symmetric, $\Sigma_{ij}=\Sigma_{ji}$, the covariance matrix is symmetric as well.

### Why covariance must be understood before the density formula

If the covariance matrix is just treated as a block of symbols, the multivariate Gaussian formula becomes meaningless.

So read the matrix first as geometry:

- large variance in one coordinate means more spread along that axis;
- positive covariance means two coordinates tend to move together;
- negative covariance means they tend to move in opposite directions;
- zero covariance means no linear co-movement.

### Two concrete covariance examples

#### Example 1: axis-aligned spread

Suppose

$$
\Sigma=\begin{pmatrix} 4 & 0 \\ 0 & 1 \end{pmatrix}.
$$

Interpret each entry:

- variance of the first coordinate is $4$;
- variance of the second coordinate is $1$;
- covariance is $0$.

So the cloud is more spread out horizontally than vertically, and there is no tilt caused by covariance.

#### Example 2: tilted contours

Now suppose

$$
\Sigma=\begin{pmatrix} 1 & 0.8 \\ 0.8 & 1 \end{pmatrix}.
$$

Interpret each entry:

- each coordinate has variance $1$;
- the positive off-diagonal value $0.8$ says the coordinates tend to increase together.

So the cloud is tilted along a positively sloped direction.

### The density formula

For a nonsingular multivariate Gaussian,

$$
p(x)=\mathcal{N}(x;\mu,\Sigma)=(2\pi)^{-n/2}|\Sigma|^{-1/2}\exp\!\left(-\frac12(x-\mu)^T\Sigma^{-1}(x-\mu)\right).
$$

For this formula as written, we assume $\Sigma$ is symmetric and positive definite. Those assumptions guarantee:

1. the inverse $\Sigma^{-1}$ exists;
2. the determinant $|\Sigma|$ is positive;
3. the quadratic form behaves like a covariance-aware squared distance.

### Mahalanobis distance

The quantity

$$
(x-\mu)^T\Sigma^{-1}(x-\mu)
$$

is the squared Mahalanobis distance from $x$ to the mean.

Why is this the right notion of distance here?

- it is small when $x$ lies in a direction where the distribution naturally has a lot of spread;
- it is large when $x$ lies far away in a direction where the distribution is tight.

So unlike ordinary Euclidean distance, it respects the covariance structure of the distribution.

### Geometry of equal-density contours

The exponential term depends only on the Mahalanobis distance. So points with the same Mahalanobis distance from $\mu$ have the same density.

That is why:

- in two dimensions, equal-density contours are ellipses;
- in higher dimensions, equal-density contours are ellipsoids.

Diagonal covariance gives axis-aligned ellipses. Off-diagonal covariance rotates them.

### A special Gaussian fact

In general probability theory,

$$
\mathrm{Cov}(X,Y)=0
$$

does not imply independence.

But in the jointly Gaussian family, zero covariance does imply independence of the corresponding coordinates.

This is a Gaussian-specific structural fact, and it is one of the reasons Gaussian models are unusually convenient.

---

## 10. Beta distributions

Up to now, most examples used random variables to represent observed outcomes. Beta distributions change the role of the random quantity.

### The underlying Bernoulli model

Suppose

$$
X\in\{0,1\}.
$$

Let

$$
\rho=P(X=1).
$$

Here:

- $X$ is the observed outcome;
- $\rho$ is the success probability parameter of the Bernoulli model.

The key role distinction is:

- the Bernoulli distribution is a distribution over $X$;
- the Beta distribution is a distribution over possible values of $\rho$.

### Beta density

A Beta distribution on $\rho\in[0,1]$ has density

$$
p(\rho)=\mathrm{Beta}(\rho;a,b)=\frac{\Gamma(a+b)}{\Gamma(a)\Gamma(b)}\rho^{a-1}(1-\rho)^{b-1}.
$$

The parameters must satisfy

$$
a>0 \quad \text{and} \quad b>0.
$$

The support condition is essential:

$$
0\le \rho \le 1.
$$

This must be true because $\rho$ itself is a probability parameter.

### What the normalization constant is doing

The factor

$$
\frac{\Gamma(a+b)}{\Gamma(a)\Gamma(b)}
$$

is the constant that forces the total area under the density on $[0,1]$ to equal $1$.

For beginner understanding, the crucial point is not memorizing Gamma functions. The crucial point is knowing that this constant exists so that the kernel

$$
\rho^{a-1}(1-\rho)^{b-1}
$$

becomes a valid probability density.

### Shape interpretation

The parameters $a$ and $b$ control shape.

#### Case 1: $a=b=1$

Then

$$
p(\rho)\propto \rho^0(1-\rho)^0=1.
$$

So the Beta density is uniform on $[0,1]$.

#### Case 2: $a>1$ and $b>1$

Both exponents are positive, so the density tends to be low near the boundaries and higher in the interior. This gives an interior peak.

#### Case 3: $a<b$

The density leans toward smaller $\rho$ values.

#### Case 4: $a>b$

The density leans toward larger $\rho$ values.

#### Case 5: one parameter below $1$

If either parameter is below $1$, the density may become very large near a boundary. That does not violate probability rules because the total integral remains finite.

### Mean of a Beta distribution

One useful summary is

$$
\mathbb{E}[\rho]=\frac{a}{a+b}.
$$

This formula is worth interpreting, not just storing:

- the ratio $a:b$ determines where the distribution is centered;
- the sum $a+b$ determines how concentrated or diffuse that distribution is.

So $\mathrm{Beta}(2,2)$ and $\mathrm{Beta}(20,20)$ are both centered at $0.5$, but the second is much more concentrated near $0.5$.

---

## 11. Dirichlet distributions

The Dirichlet distribution is the multi-category analogue of the Beta distribution.

### The parameter object

Suppose a categorical variable can take one of $K$ categories with parameter vector

$$
\pi=(\pi_1,\dots,\pi_K).
$$

Because these are probabilities, the vector must satisfy two constraints:

$$
\pi_k\ge 0 \quad \text{for every } k,
$$

and

$$
\sum_{k=1}^{K}\pi_k=1.
$$

So $\pi$ lives on the probability simplex.

### Dirichlet density

The Dirichlet distribution has density

$$
p(\pi)=\mathrm{Dir}(\pi;\alpha_1,\dots,\alpha_K)\propto \prod_{k=1}^{K}\pi_k^{\alpha_k-1}.
$$

Its parameters must satisfy

$$
\alpha_k>0 \quad \text{for every } k.
$$

Again, the proportionality sign means a normalization constant exists but is not written explicitly here.

### What this object is

This is not a distribution over observed category labels. It is a distribution over possible categorical parameter vectors.

That is exactly parallel to the Beta-Bernoulli relationship:

- Bernoulli outcome $X$ corresponds to Beta-distributed parameter $\rho$;
- categorical outcome corresponds to Dirichlet-distributed parameter vector $\pi$.

### Pseudo-count intuition

The parameters $\alpha_1,\dots,\alpha_K$ are often interpreted as pseudo-counts.

Why? Because later, when categorical data are observed, each observed count gets added to the corresponding $\alpha_k$. So the prior behaves algebraically as though it had already seen some imaginary counts before the real data arrived.

That is a structural preview for Bayesian learning in the next section.

---

## 12. What to retain

- The CDF is the universal object for real-valued random variables.
- A PDF is not a point probability. It must be integrated to produce probabilities.
- For a continuous variable, $P(X=x)=0$ at every point.
- PMFs, PDFs, and CDFs answer different questions.
- Standardization converts an arbitrary Gaussian probability problem into a standard-normal probability problem.
- In a multivariate Gaussian, the covariance matrix controls spread and geometric orientation.
- Beta and Dirichlet distributions are distributions over parameters, not over observed outcomes.

## 13. Do not confuse

- Do not confuse density height with probability.
- Do not confuse a smooth CDF with a PDF. They are different objects.
- Do not forget that CDFs work in discrete, continuous, and mixed settings.
- Do not treat the Gaussian formula as just symbols; the mean and covariance have direct geometric meaning.
- Do not confuse the Bernoulli outcome $X$ with the Bernoulli parameter $\rho$.
- Do not confuse a categorical observation with a Dirichlet-distributed parameter vector.

# 2.5 Continuous Random Variables

Up to now, the chapter has worked in the discrete setting, where probabilities are assigned directly to isolated states. The continuous setting changes that logic in a fundamental way.

For a continuous variable:

- probability is assigned to intervals or regions,
- not to single points,
- and the main descriptive object is a density rather than a mass function.

This is the point where many students start writing correct formulas but carrying the wrong discrete intuition. The purpose of this section is to remove that confusion carefully.

The section has four main goals:

1. explain what a density is and what it is not;
2. distinguish PMFs, PDFs, and CDFs cleanly;
3. introduce Gaussian models in one and several dimensions in a way that makes their geometry clear;
4. explain Beta and Dirichlet distributions as distributions over parameters rather than over observed outcomes.

---

## 1. Why continuous variables require a new object

In the discrete setting, a PMF directly answers

$$

P(X=x).

$$

That works because isolated states can have positive probability mass.

In the continuous setting, the logic changes. Probability is spread across a continuum of values, so an individual point typically carries probability zero. If a reader keeps the discrete intuition and treats a density value as a point probability, later reasoning will go wrong immediately.

So the first mastery-level distinction is:

- discrete: probabilities attach to exact states through a PMF;
- continuous: probabilities attach to intervals or sets through integration of a density;
- universal: the CDF still describes threshold probabilities in both settings.

---

## 2. Probability density functions

A probability density function is a nonnegative function $p(x)$ satisfying

$$

\int_{-\infty}^{\infty} p(x)\,dx = 1.

$$

For a set $A$,

$$

P(X\in A)=\int_A p(x)\,dx.

$$

### What a density is

A density is a **probability per unit of the variable’s scale**. It is not itself a probability. Probability arises only after integrating over an interval or region.

That is the key interpretation.

### Point probabilities

For a continuous variable,

$$

P(X=x)=0

$$

for every individual point $x$.

This is one of the first statements students often resist because the density at that point may be positive. But positive density height does not mean positive point probability. Probability comes from area, not height alone.

### Small-interval approximation

When a density exists,

$$

P(x\le X\le x+\Delta)\approx p(x)\,\Delta

$$

for small $\Delta$.

This is the precise sense in which a PDF acts like “probability per unit $x$.”

### Why a density may exceed 1

A density value can be larger than 1 if the support is narrow enough. This does not violate probability rules because the integral, not the pointwise height, must equal 1.

That is another place where discrete intuition fails if not corrected explicitly.

---

## 3. Uniform density on an interval

A uniform density on $[0,T]$ has the form

<table align="center">
  <thead>
    <tr><th>$p(x)$</th><th>condition on $x$</th></tr>
  </thead>
  <tbody>
    <tr><td>$c$</td><td>$x \in [0,T]$</td></tr>
    <tr><td>$0$</td><td>otherwise</td></tr>
  </tbody>
</table>

Normalization forces

$$

\int_0^T c\,dx = cT = 1,

$$

so

$$

c=\frac1T.

$$

Therefore

<table align="center">
  <thead>
    <tr><th>$p(x)$</th><th>condition on $x$</th></tr>
  </thead>
  <tbody>
    <tr><td>$1/T$</td><td>$x \in [0,T]$</td></tr>
    <tr><td>$0$</td><td>otherwise</td></tr>
  </tbody>
</table>

### What uniformity means

Uniformity on an interval means equal lengths receive equal probability. It is not merely “flat looking.” The exact content is:

$$

P(a\le X\le b)=\frac{b-a}{T}
\qquad\text{for }0\le a\le b\le T.

$$

### Worked example

If $X\sim \mathrm{Unif}([0,2])$, then

$$

p(x)=\frac12
\qquad\text{for }0\le x\le 2.

$$

So

$$

P(0.3\le X\le 0.9)
=
\int_{0.3}^{0.9}\frac12\,dx
=
\frac12(0.6)=0.3.

$$

The probability comes from interval length times density height.

---

## 4. PMF, PDF, and CDF

A high-quality note must separate these three objects by the question each answers.

- **PMF**: what probability is assigned to this exact discrete state?
- **PDF**: how densely is probability packed near this location?
- **CDF**: how much total probability lies to the left of this threshold?

The cumulative distribution function is

$$

F_X(x)=P(X\le x).

$$

### Why the CDF is the universal object

Every real-valued random variable has threshold events of the form $X\le x$, so every real-valued random variable has a CDF.

That is not true of PMFs or PDFs:

- PMFs belong to discrete variables,
- PDFs belong to absolutely continuous variables,
- CDFs work for discrete, continuous, and mixed cases.

So when in doubt, the CDF is the safest general object.

### Core facts about CDFs

For every CDF:

1. $0\le F_X(x)\le 1$
2. $F_X$ is nondecreasing
3. $\lim_{x\to-\infty}F_X(x)=0$
4. $\lim_{x\to\infty}F_X(x)=1$
5. $F_X$ is right-continuous

Also,

$$

P(a<X\le b)=F_X(b)-F_X(a).

$$

This subtraction rule works in all settings.

---

## 5. Discrete, continuous, and mixed CDFs

### Discrete example: Bernoulli

If

$$

P(X=1)=0.3,\qquad P(X=0)=0.7,

$$

then

<table align="center">
  <thead>
    <tr><th>$F_X(x)$</th><th>condition on $x$</th></tr>
  </thead>
  <tbody>
    <tr><td>$0$</td><td>$x \lt 0$</td></tr>
    <tr><td>$0.7$</td><td>$0\le x \lt 1$</td></tr>
    <tr><td>$1$</td><td>$x \ge 1$</td></tr>
  </tbody>
</table>

The jumps are exactly the point masses.

### Continuous example: uniform on $[0,2]$

If $X\sim \mathrm{Unif}([0,2])$, then

<table align="center">
  <thead>
    <tr><th>$F_X(x)$</th><th>condition on $x$</th></tr>
  </thead>
  <tbody>
    <tr><td>$0$</td><td>$x \lt 0$</td></tr>
    <tr><td>$x/2$</td><td>$0\le x\le 2$</td></tr>
    <tr><td>$1$</td><td>$x \gt 2$</td></tr>
  </tbody>
</table>

This rises smoothly because mass is spread continuously.

### Mixed example

A mixed distribution has both atoms and continuous spread. For example, a broken sensor might output exactly $0$ with positive probability but otherwise produce a continuous real measurement. In that case, the CDF has both jumps and smooth parts.

This is another reason the CDF is the cleanest universal description.

---

## 6. One-dimensional Gaussian distributions

A one-dimensional Gaussian is the continuous family that matters most in introductory probability, statistics, and machine learning.

Its density is

$$

p(x)=\mathcal{N}(x;\mu,\sigma^2)
=
\frac{1}{\sqrt{2\pi\sigma^2}}
\exp\!\left(
-\frac{(x-\mu)^2}{2\sigma^2}
\right).

$$

### What the parameters mean

- $\mu$ is the center or mean;
- $\sigma^2$ is the variance, which controls spread;
- $\sigma$ is the standard deviation.

### What the exponent is doing

The exponent is the most important part to interpret first. It says that density decays according to squared distance from the mean, measured in units scaled by the variance.

So:

- values near $\mu$ receive larger density,
- values far from $\mu$ receive smaller density,
- the rate of decay depends on the spread parameter.

### Why Gaussians matter

Gaussians are mathematically tractable and also arise naturally in many approximate models of noise and aggregate variation. They are not the answer to every modeling problem, but they are so central that deep familiarity is necessary.

---

## 7. Standardization and the standard normal

If

$$

X\sim \mathcal{N}(\mu,\sigma^2),

$$

then the standardized variable

$$

Z=\frac{X-\mu}{\sigma}

$$

satisfies

$$

Z\sim \mathcal{N}(0,1).

$$

This is not just a symbolic trick. It is the main computational bridge for Gaussian probabilities.

Let $\Phi$ denote the standard-normal CDF. Then

$$

P(a\le X\le b)
=
\Phi\!\left(\frac{b-\mu}{\sigma}\right)
-
\Phi\!\left(\frac{a-\mu}{\sigma}\right).

$$

### Why this matters

Standardization turns a whole family of Gaussian interval questions into one standard-normal question. That is the real reason the transformation is introduced.

### Worked example

Suppose

$$

X\sim \mathcal{N}(2,9),

$$

so $\mu=2$ and $\sigma=3$. Then

$$

P(-1\le X\le 5)
=
P\!\left(\frac{-1-2}{3}\le Z\le \frac{5-2}{3}\right)
=
P(-1\le Z\le 1).

$$

Therefore

$$

P(-1\le X\le 5)=\Phi(1)-\Phi(-1).

$$

The interval probability was reduced to a standard-normal CDF difference.

---

## 8. The 68–95–99.7 rule

Because the standard normal satisfies

$$

P(|Z|\le 1)\approx 0.68,\qquad
P(|Z|\le 2)\approx 0.95,\qquad
P(|Z|\le 3)\approx 0.997,

$$

a Gaussian with mean $\mu$ and standard deviation $\sigma$ places about

- 68% of its mass within $\mu\pm \sigma$,
- 95% within $\mu\pm 2\sigma$,
- 99.7% within $\mu\pm 3\sigma$.

These are not disconnected folklore facts. They are direct consequences of standardization and the standard-normal CDF.

### Why the normalization constant is there

The factor

$$

\frac{1}{\sqrt{2\pi\sigma^2}}

$$

ensures the total area under the Gaussian curve is 1. The exponential term shapes the curve. The prefactor rescales it into a valid density.

---

## 9. Multivariate Gaussian distributions

A multivariate Gaussian extends the same basic idea from one coordinate to many.

Let

$$

X=(X_1,\dots,X_n)^T.

$$

Now the center is a mean vector

$$

\mu=\mathbb{E}[X],

$$

and spread/dependence are encoded by the covariance matrix

$$

\Sigma_{ij}=\mathrm{Cov}(X_i,X_j).

$$

### Why covariance must be introduced first

A good mastery note does not start with the matrix formula alone. The reader must first understand what the covariance matrix means.

- diagonal entries tell the variance of each coordinate,
- off-diagonal entries tell how coordinates move together.

### Example covariance structures

If

$$

\Sigma=
\begin{pmatrix}
4 & 0\\
0 & 1
\end{pmatrix},

$$

then the distribution is more spread in the first direction than the second, and the contours are axis-aligned.

If instead

$$

\Sigma=
\begin{pmatrix}
1 & 0.8\\
0.8 & 1
\end{pmatrix},

$$

then the variables tend to move together and the contours are tilted.

### Density formula

The nonsingular multivariate Gaussian density is

$$

p(x)=\mathcal{N}(x;\mu,\Sigma)
=
(2\pi)^{-n/2}|\Sigma|^{-1/2}
\exp\!\left(
-\frac12 (x-\mu)^T\Sigma^{-1}(x-\mu)
\right).

$$

For this formula as written, we assume $\Sigma$ is symmetric and positive definite. That guarantees the inverse exists and the quadratic form behaves like a genuine squared distance.

### Mahalanobis distance

The quantity

$$

(x-\mu)^T\Sigma^{-1}(x-\mu)

$$

is the squared Mahalanobis distance. It is the covariance-aware notion of distance from the mean.

That gives the geometry:

- diagonal covariance gives axis-aligned ellipses or ellipsoids;
- larger variances stretch along the corresponding directions;
- off-diagonal covariance rotates the principal axes.

### Zero covariance in the Gaussian family

In general, zero covariance does not imply independence. But for jointly Gaussian variables, zero covariance does imply independence of the corresponding coordinates.

This is one of the reasons Gaussian models are so structurally special.

---

## 10. Beta distributions

Up to this point, most random variables represented observed outcomes. Beta changes the role of the random object.

For a Bernoulli model, the outcome variable is

$$

X\in\{0,1\},

$$

with success probability

$$

\rho=P(X=1).

$$

A Beta distribution is a distribution over possible values of that parameter:

$$

p(\rho)=\mathrm{Beta}(\rho;a,b)
=
\frac{\Gamma(a+b)}{\Gamma(a)\Gamma(b)}
\rho^{a-1}(1-\rho)^{b-1},
\qquad 0\le \rho\le 1.

$$

### Why this matters conceptually

This is the first place the chapter strongly separates:

- a distribution over outcomes,
- from a distribution over possible parameter values.

That distinction is essential for later Bayesian inference.

### Shape interpretation

The parameters $a$ and $b$ control whether the density is concentrated in the interior, skewed toward one boundary, or concentrated near both ends.

---

## 11. Dirichlet distributions

Dirichlet is the categorical analogue of Beta.

If

$$

\pi=(\pi_1,\dots,\pi_K),
\qquad \pi_k\ge 0,
\qquad \sum_{k=1}^{K}\pi_k=1,

$$

then the Dirichlet density is

$$

p(\pi)=\mathrm{Dir}(\pi;\alpha_1,\dots,\alpha_K)
\propto
\prod_{k=1}^{K}\pi_k^{\alpha_k-1}.

$$

### What object this is

Again, this is not a distribution over observed categories. It is a distribution over possible categorical parameter vectors.

That is why it matters later for Bayesian learning with categorical or multinomial data.

---

## 12. How this section connects forward

This section introduces the main descriptive language for continuous probability and the core Gaussian family that later dominates much of statistics and machine learning.

- Densities prepare the ground for continuous expectations and likelihoods.
- CDFs remain the universal description across discrete and continuous settings.
- Gaussian models become central in estimation, geometry, and latent-variable modeling.
- Beta and Dirichlet prepare the conceptual distinction between observed outcomes and distributions over parameters.

So the real mastery goal here is not merely learning a few formulas. It is learning the new logic of continuous probability and the new roles different families can play.

---

## 13. Retain from 2.5

- A density is not a point probability.
- Continuous probabilities come from integration over intervals or regions.
- The CDF is the universal object across discrete, continuous, and mixed cases.
- Standardization reduces arbitrary Gaussian interval questions to standard-normal ones.
- Multivariate Gaussian geometry is controlled by covariance.
- Beta and Dirichlet are distributions over parameters, not over observed outcomes.

## 14. Do not confuse in 2.5

- Do not confuse PDF values with probabilities at points.
- Do not confuse PMFs, PDFs, and CDFs.
- Do not forget support when interpreting any density.
- Do not treat standardization as symbolic decoration; it is a computational tool.
- Do not confuse a Bernoulli outcome distribution with a Beta prior over the Bernoulli parameter.

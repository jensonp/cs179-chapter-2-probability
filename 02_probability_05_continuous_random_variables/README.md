# 2.2 Continuous Random Variables

This section introduces continuous random variables, the distinction among PMFs, PDFs, and CDFs, Gaussian models in one and several dimensions, and the Beta and Dirichlet families.

The main conceptual shift from the discrete setting is simple but easy to mishandle:

- in the discrete setting, probabilities are attached directly to isolated states;
- in the continuous setting, probability is attached to intervals or regions;
- the cumulative distribution function is the most universal object because it works for discrete, continuous, and mixed cases.

Everything in this section becomes cleaner once that shift is kept explicit.

## Continuous variables and densities

Suppose $X$ is real-valued. A probability density function is a nonnegative function $p(x)$ satisfying

$$
\int_{-\infty}^{\infty} p(x)\,dx = 1.
$$

Probabilities are obtained by integrating over sets:

$$
\mathbb{P}(X\in A)=\int_A p(x)\,dx.
$$

This is the first place where beginners often carry over the wrong discrete intuition. For a continuous variable, the value $p(x)$ is **not** the probability that $X=x$. In fact,

$$
\mathbb{P}(X=x)=0
$$

for every individual point. A density becomes a probability only after integrating over an interval or region.

That is also why a density may exceed $1$ locally. Probability is determined by area, not by height alone.

### Small-interval intuition

When a density exists, probabilities over very short intervals are approximately density times width:

$$
\mathbb{P}(x\le X\le x+\Delta)\approx p(x)\,\Delta
\qquad\text{for small }\Delta.
$$

This is the precise sense in which a PDF is a “probability per unit $x$.”

### Uniform example on $[0,2]$

If $X\sim \mathrm{Unif}([0,2])$, then

$$
p(x)=\frac12\qquad\text{for }0\le x\le 2.
$$

The probability of falling between $0.3$ and $0.9$ is

$$
\mathbb{P}(0.3\le X\le 0.9)=\int_{0.3}^{0.9}\frac12\,dx
=\frac12(0.9-0.3)=0.3.
$$

The point $x=0.4$ itself still has probability zero. What matters is interval width.

## PMF, PDF, and CDF

A clean way to avoid confusion is to separate the three objects by the question they answer.

- A **PMF** answers: what probability is assigned to this exact discrete state?
- A **PDF** answers: how densely is probability packed near this location?
- A **CDF** answers: how much total probability lies to the left of this threshold?

The cumulative distribution function is

$$
F_X(x)=\mathbb{P}(X\le x).
$$

This is the most universal description because every real-valued random variable has threshold events of the form $X\le x$, even when a density does not exist.

### Structural facts about every CDF

Several properties follow directly from the definition.

1. $0\le F_X(x)\le 1$ because it is a probability.
2. $F_X$ is nondecreasing because larger thresholds contain more outcomes.
3. $\lim_{x\to -\infty}F_X(x)=0$ and $\lim_{x\to\infty}F_X(x)=1$.
4. A CDF is right-continuous.
5. Interval probabilities can be read from differences of CDF values:

$$
\mathbb{P}(a<X\le b)=F_X(b)-F_X(a).
$$

This subtraction rule works for discrete, continuous, and mixed distributions.

## Discrete, continuous, and mixed CDFs

### Discrete example: Bernoulli

Suppose

$$
p(X=1)=0.3,\qquad p(X=0)=0.7.
$$

Then the CDF is

<table align="center">
  <thead>
    <tr><th>$F_X(x)$</th><th>condition on $x$</th></tr>
  </thead>
  <tbody>
    <tr><td>$0$</td><td>$x \lt 0$</td></tr>
    <tr><td>$0.7$</td><td>$0 \le x \lt 1$</td></tr>
    <tr><td>$1$</td><td>$x \ge 1$</td></tr>
  </tbody>
</table>

The jumps are the point masses. The jump at $0$ is $0.7$, and the jump at $1$ adds the remaining $0.3$.

### Continuous example: uniform on $[0,2]$

If $X\sim \mathrm{Unif}([0,2])$, then

<table align="center">
  <thead>
    <tr><th>$F_X(x)$</th><th>condition on $x$</th></tr>
  </thead>
  <tbody>
    <tr><td>$0$</td><td>$x \lt 0$</td></tr>
    <tr><td>$x/2$</td><td>$0 \le x \le 2$</td></tr>
    <tr><td>$1$</td><td>$x \gt 2$</td></tr>
  </tbody>
</table>

This CDF rises smoothly because probability is spread continuously across the interval.

### Mixed example

A mixed distribution combines discrete atoms and continuous spread. For example, a sensor might fail and output exactly $0$ with some positive probability, while otherwise producing a continuous measurement. In that case, the CDF has both a jump and a smooth part.

This is why the CDF is the safest universal object: PMFs and PDFs each belong to restricted settings, but the CDF survives all of them.

## Uniform distributions

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

This means two things:

- the support is exactly the interval $[0,T]$;
- within that interval, equal lengths carry equal probability.

So if $0\le a\le b\le T$, then

$$
\mathbb{P}(a\le X\le b)=\int_a^b \frac1T\,dx=\frac{b-a}{T}.
$$

Uniformity is therefore a statement about **length**, not about location.

## One-dimensional Gaussian distributions

A one-dimensional Gaussian is a continuous distribution on all of $\mathbb{R}$ with density

$$
p(x)=\mathcal{N}(x;\mu,\sigma^2)=
\frac{1}{\sqrt{2\pi\sigma^2}}
\exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right).
$$

The parameters have direct roles:

- $\mu$ is the center;
- $\sigma^2$ is the variance, which controls spread;
- $\sigma$ is the standard deviation.

The exponent is the most important part to read first. It says the density decays according to **squared distance from the mean measured in variance-scaled units**. Values close to $\mu$ receive larger density. Values far away receive smaller density.

### Standardization

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

This matters because interval probabilities for any Gaussian can now be reduced to the standard normal. If $\Phi$ denotes the standard-normal CDF, then

$$
\mathbb{P}(a\le X\le b)
=
\Phi\!\left(\frac{b-\mu}{\sigma}\right)
-
\Phi\!\left(\frac{a-\mu}{\sigma}\right).
$$

That is the real computational purpose of standardization.

### Worked interval example

Suppose

$$
X\sim \mathcal{N}(2,9),
$$

so $\mu=2$ and $\sigma=3$. Then

$$
\mathbb{P}(-1\le X\le 5)
=
\mathbb{P}\!\left(\frac{-1-2}{3}\le Z\le \frac{5-2}{3}\right)
=
\mathbb{P}(-1\le Z\le 1).
$$

Therefore

$$
\mathbb{P}(-1\le X\le 5)=\Phi(1)-\Phi(-1).
$$

This is the bridge the reader needs: standardization turns an arbitrary Gaussian interval into a standard-normal interval.

### The 68–95–99.7 rule

Because

$$
\mathbb{P}(|Z|\le 1)\approx 0.68,\qquad
\mathbb{P}(|Z|\le 2)\approx 0.95,\qquad
\mathbb{P}(|Z|\le 3)\approx 0.997,
$$

a Gaussian with mean $\mu$ and standard deviation $\sigma$ places about

- 68% of its mass within $\mu\pm \sigma$,
- 95% within $\mu\pm 2\sigma$,
- 99.7% within $\mu\pm 3\sigma$.

These are not new facts disconnected from the CDF. They are direct consequences of standardization and the standard-normal CDF.

### Why the normalization constant is there

The factor

$$
\frac{1}{\sqrt{2\pi\sigma^2}}
$$

exists so that the total area under the Gaussian curve equals $1$. The exponential term controls shape. The prefactor rescales that shape into a valid density.

### Why Gaussians matter

Gaussians are popular not only because they are mathematically tractable, but also because they often model noise and aggregate variation well. When many small effects combine, Gaussian approximations arise naturally in many settings. This is a modeling heuristic, not a universal law, but it explains why Gaussian families appear everywhere.

## Multivariate Gaussian distributions

A multivariate Gaussian generalizes the same basic idea from one coordinate to many.

Let

$$
X=(X_1,\dots,X_n)^T.
$$

Now the center is a **mean vector**

$$
\mu=\mathbb{E}[X],
$$

and spread/dependence are encoded by the **covariance matrix**

$$
\Sigma_{ij}=\mathrm{Cov}(X_i,X_j).
$$

### Read covariance before the full formula

In two dimensions, the diagonal entries tell you variance along each coordinate direction, while the off-diagonal entries tell you how coordinates move together.

If

$$
\Sigma=
\begin{pmatrix}
4 & 0\\
0 & 1
\end{pmatrix},
$$

then the cloud is more spread in the first direction than the second, and the zero off-diagonal entries say there is no linear covariance. In the jointly Gaussian family, zero covariance is stronger than usual: it implies independence of the corresponding coordinates.

If instead

$$
\Sigma=
\begin{pmatrix}
1 & 0.8\\
0.8 & 1
\end{pmatrix},
$$

then the variables tend to move together, so the equal-density contours are tilted rather than axis-aligned.

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

For this formula as written, we assume $\Sigma$ is symmetric and positive definite. That guarantees the inverse exists, the determinant is positive, and the quadratic form behaves like a genuine squared distance.

### Mahalanobis distance

The quantity

$$
(x-\mu)^T\Sigma^{-1}(x-\mu)
$$

is the squared Mahalanobis distance. It is the covariance-aware notion of distance from the mean.

This gives the geometry:

- if $\Sigma$ is diagonal, equal-density contours are axis-aligned ellipses or ellipsoids;
- larger variances stretch those contours in the corresponding directions;
- off-diagonal covariance rotates the principal axes.

So the multivariate Gaussian is still the same story as the one-dimensional Gaussian: density decays with distance from the mean, except that now the geometry of “distance” is shaped by covariance.

## Beta distributions

Up to now, the random variable was usually an observed outcome. Beta changes the role of the random object.

For a Bernoulli model, the outcome variable is

$$
X\in\{0,1\},
$$

while the success probability is

$$
\rho=\mathbb{P}(X=1),
\qquad 0\le \rho\le 1.
$$

A Beta distribution is a density over possible values of $\rho$:

$$
p(\rho)=\mathrm{Beta}(\rho;a,b)
=
\frac{\Gamma(a+b)}{\Gamma(a)\Gamma(b)}
\rho^{a-1}(1-\rho)^{b-1},
\qquad 0\le \rho\le 1.
$$

The conceptual distinction is the important one:

- Bernoulli is a distribution over outcomes;
- Beta is a distribution over possible Bernoulli parameters.

The shape parameters $a$ and $b$ control where the density concentrates: near the interior, near one boundary, or near both boundaries.

## Dirichlet distributions

Dirichlet is the categorical analogue of Beta.

If

$$
\pi=(\pi_1,\dots,\pi_K),\qquad \pi_k\ge 0,\qquad \sum_{k=1}^K \pi_k=1,
$$

then a Dirichlet density is a distribution over possible categorical parameter vectors:

$$
p(\pi)=\mathrm{Dir}(\pi;\alpha_1,\dots,\alpha_K)
\propto
\prod_{k=1}^{K}\pi_k^{\alpha_k-1}.
$$

Again, the key distinction is not the formula first. It is the role of the object:

- the categorical distribution governs outcomes in one of $K$ categories;
- the Dirichlet distribution governs uncertainty about the categorical parameter vector itself.

## Retain from 2.2

- In the continuous setting, density is not the same thing as probability at a point.
- The CDF is the universal object across discrete, continuous, and mixed distributions.
- Standardization reduces arbitrary Gaussian interval probabilities to standard-normal probabilities.
- In the Gaussian family, covariance has a direct geometric interpretation.
- Beta and Dirichlet are distributions over parameters, not over the original observed outcomes.

# Problem 5 Fully Explained: Density Estimation with Normalizing Flows

## 1. What Problem 5 is trying to do

Earlier homework problems let you work with probability objects that are easy to write down directly:

- a finite probability table,
- a Bayesian network with a manageable number of variables,
- or a Markov chain with a finite transition matrix.

Problem 5 changes the setting.

Now each observation is a point in the plane, so the data live in $\mathbb{R}^2$. The homework gives you a way to **sample** from the target distribution, but it does not give you a simple closed-form density for that distribution.[^repo]

So the problem has two jobs:

1. understand the target data-generating process, and
2. build a model that can both sample new points and evaluate a density at a point.

The new idea is:

$$
\text{start with a simple distribution you understand exactly, then transform it into a more flexible one.}
$$

That transformed model is the normalizing flow.

---

## 2. Notation and object conventions

This section is here so later formulas do not silently switch meanings.

### 2.1 Random variable vs realized value

I will use uppercase letters for random objects and lowercase letters for specific realized values.

- $X$ means a random vector.
- $x$ means one realized point drawn from the distribution of $X$.
- $Z$ means a random latent vector.
- $z$ means one realized latent point.

So when you read

$$
X = f_\theta(Z),
$$

this means:

- first draw a random latent vector $Z$,
- then apply the map $f_\theta$,
- and the result is the random observed vector $X$.

When you read

$$
x = f_\theta(z),
$$

this means the same map is being applied to one particular point $z$.

### 2.2 What $\mathbb{R}^2$ means

$\mathbb{R}^2$ is the set of all ordered pairs of real numbers:

$$
\mathbb{R}^2 = \{(x_1, x_2) : x_1 \in \mathbb{R},\ x_2 \in \mathbb{R}\}.
$$

So a point in $\mathbb{R}^2$ is just a 2-dimensional vector with two coordinates.

### 2.3 Data space vs latent space

The problem uses two spaces:

- **data space**: the space where the observed 2D points live,
- **latent space**: the space where the simple base distribution lives.

In this homework both spaces are $\mathbb{R}^2$, but they play different roles.

- Data space contains the points you want to model.
- Latent space contains the simple random points you start from before transforming them.

### 2.4 What "latent" means here

A variable is **latent** if it is introduced by the model but is not directly observed in the dataset.

So the latent vector $Z$ is not a plotted data point from the homework generator. It is the model's internal source variable.

Do not confuse the model latent variable $Z$ with the generator's hidden variables $w$ and $i$ from the homework. Both are unobserved, but they are different objects with different roles.

### 2.5 What "parameterized by $\theta$" means

A map $f_\theta$ is **parameterized** if its exact shape depends on trainable numerical parameters $\theta$.

So $\theta$ is not one special variable in the data. It is the collection of numbers inside the transform that the optimizer updates during training.

---

## 3. The target generator, rewritten slowly

The homework generator is compact in code, but the code hides the probabilistic structure.[^repo]

The generator first draws two hidden variables:

$$
w \sim \mathrm{Uniform}(0,1),
\qquad
i \sim \mathrm{Bernoulli}(0.3).
$$

Here is what those words mean.

### 3.1 Uniform$(0,1)$

A random variable $w \sim \mathrm{Uniform}(0,1)$ is equally likely to land anywhere in the interval $[0,1]$.

So:

- $w$ varies continuously between $0$ and $1$,
- no sub-interval of the same length is preferred over another.

### 3.2 Bernoulli$(0.3)$

A Bernoulli random variable takes only two values, usually $0$ and $1$.

$$
i \sim \mathrm{Bernoulli}(0.3)
$$

means

$$
P(i = 1) = 0.3,
\qquad
P(i = 0) = 0.7.
$$

So $i$ acts like a binary switch that chooses between two regimes.

### 3.3 The deterministic mean location before noise

The generator then builds a mean location

$$
\mu(w,i)
=
\begin{bmatrix}
w \cdot 0.6^i + 0.2i - 0.5 \\
-2(1-i)(2w-1)^2 - i + 1
\end{bmatrix}.
$$

This is a 2-dimensional vector. Its first entry is the horizontal coordinate. Its second entry is the vertical coordinate.

The final observed point is

$$
X = 5\,\mu(w,i) + \varepsilon,
$$

where the noise term is Gaussian:

$$
\varepsilon \sim \mathcal{N}\!\left(0,\ (0.1(i+1))^2 I_2\right).
$$

This means $\varepsilon$ is a 2-dimensional normal random vector with mean vector $(0,0)$ and covariance matrix $(0.1(i+1))^2 I_2$, where

$$
I_2 =
\begin{bmatrix}
1 & 0 \\
0 & 1
\end{bmatrix}.
$$

So the noise is centered at zero, has the same variance in both coordinates, and has no cross-coordinate covariance.

### 3.4 Case analysis: what shape does the generator make?

This is the first place where the geometry of the problem becomes visible.

#### Case 1: $i = 0$

Then

$$
\mu(w,0)
=
\begin{bmatrix}
w - 0.5 \\
-2(2w-1)^2 + 1
\end{bmatrix}.
$$

Interpret this coordinate by coordinate.

- The first coordinate $w - 0.5$ changes linearly with $w$.
- The second coordinate $-2(2w-1)^2 + 1$ is a downward-opening quadratic curve.

So before noise and scaling, this branch traces a curved arc.

The noise scale is

$$
0.1(i+1) = 0.1.
$$

So this branch is the **less noisy curved branch**.

#### Case 2: $i = 1$

Then

$$
\mu(w,1)
=
\begin{bmatrix}
0.6w - 0.3 \\
0
\end{bmatrix}.
$$

Interpret this again coordinate by coordinate.

- The second coordinate is exactly $0$.
- The first coordinate moves linearly as $w$ changes.

So before noise and scaling, this branch lies on a horizontal line segment.

The noise scale is

$$
0.1(i+1) = 0.2.
$$

So this branch is the **noisier line-like branch**.

### 3.5 Why this matters

This local analysis already tells you something decisive:

the target distribution is not one simple round Gaussian blob.

It has:

- one curved component,
- one straighter component,
- and different noise levels in the two components.

That is the pressure that forces a more flexible density model.

---

## 4. Density: the first concept that must be clear

Many later formulas use the word "density" as if it were self-explanatory. It is not.

### 4.1 Probability at a point is not density

For a continuous random vector $X$, the probability of any exact point is zero:

$$
P(X = x) = 0.
$$

So when we say a point is "more likely" than another point, we do **not** mean it has positive point-mass probability.

We mean the density is larger there.

### 4.2 What a density does mean

A density tells you how probability is distributed over small regions.

If $A$ is a small region around $x$, then informally

$$
P(X \in A) \approx p_X(x)\cdot \mathrm{area}(A).
$$

In two dimensions, density is therefore "probability per unit area".

This is why later we care about local stretching and compression of area. If a transformation changes area, density must change in the opposite direction so total probability stays consistent.

---

## 5. The base distribution: unpack every word in $Z \sim \mathcal{N}(0, I_2)$

This expression is short, but it contains several separate definitions.

### 5.1 Gaussian and normal mean the same thing

"Gaussian distribution" and "normal distribution" are two names for the same family.

So "base Gaussian" just means "the base distribution is a normal distribution".

### 5.2 What a multivariate normal is

A multivariate normal distribution is a distribution on vectors, not on single scalars.

In two dimensions, it is specified by:

- a **mean vector** $\mu \in \mathbb{R}^2$,
- a **covariance matrix** $\Sigma \in \mathbb{R}^{2 \times 2}$.

PyTorch's `MultivariateNormal` is explicitly parameterized by a mean vector and a covariance matrix.[^mvn]

### 5.3 Mean vector

If

$$
Z =
\begin{bmatrix}
Z_1 \\
Z_2
\end{bmatrix},
$$

then the mean vector is

$$
\mathbb{E}[Z]
=
\begin{bmatrix}
\mathbb{E}[Z_1] \\
\mathbb{E}[Z_2]
\end{bmatrix}.
$$

So saying the mean is

$$
(0,0)
$$

means:

- the average horizontal coordinate is $0$,
- the average vertical coordinate is $0$.

It tells you where the Gaussian cloud is centered.

### 5.4 Covariance matrix

The covariance matrix records variances on the diagonal and cross-coordinate covariances off the diagonal:

$$
\Sigma
=
\begin{bmatrix}
\mathrm{Var}(Z_1) & \mathrm{Cov}(Z_1, Z_2) \\
\mathrm{Cov}(Z_2, Z_1) & \mathrm{Var}(Z_2)
\end{bmatrix}.
$$

Here:

- $\mathrm{Var}(Z_1)$ tells you how spread out the first coordinate is,
- $\mathrm{Var}(Z_2)$ tells you how spread out the second coordinate is,
- $\mathrm{Cov}(Z_1, Z_2)$ tells you whether the two coordinates tend to move together.

### 5.5 Identity matrix

The $2 \times 2$ identity matrix is

$$
I_2
=
\begin{bmatrix}
1 & 0 \\
0 & 1
\end{bmatrix}.
$$

PyTorch's `torch.eye(2)` returns a $2$-dimensional tensor with ones on the diagonal and zeros elsewhere.[^eye]

So if the covariance matrix is $I_2$, then:

- $\mathrm{Var}(Z_1) = 1$,
- $\mathrm{Var}(Z_2) = 1$,
- $\mathrm{Cov}(Z_1, Z_2) = 0$.

That means both coordinates have unit variance and zero covariance. For a Gaussian distribution, zero covariance here means the coordinates are independent.

### 5.6 What "standard 2D Gaussian" means

A **standard** 2D Gaussian means exactly this:

$$
Z \sim \mathcal{N}(0, I_2).
$$

The word "standard" means:

- zero mean,
- identity covariance.

So the cloud is centered at the origin and has equal unit scale in both coordinate directions.

### 5.7 Why it is called the base distribution

It is called the **base** distribution because it is the starting distribution before any transformation is applied.

So "base Gaussian" means:

- start with a simple Gaussian in latent space,
- then transform it,
- and the transformed distribution becomes the actual model for the data.

The base Gaussian is not supposed to match the homework data by itself. Its role is tractability:

- easy to sample from,
- easy to evaluate,
- easy to use as raw material for a more flexible model.

---

## 6. The model: introduce the transform before talking about flows

The model defines

$$
X = f_\theta(Z),
\qquad
Z \sim \mathcal{N}(0, I_2).
$$

This sentence introduces three objects:

- the latent random vector $Z$,
- the transform $f_\theta$,
- the observed random vector $X$.

### 6.1 What is fixed here?

At the level of model design, the following are fixed:

- the fact that latent points live in $\mathbb{R}^2$,
- the choice of base family $\mathcal{N}(0, I_2)$,
- the choice of transform family,
- the architecture of the transform.

### 6.2 What varies here?

The following vary:

- the sampled latent point $z$,
- the sampled observed point $x = f_\theta(z)$,
- and during training, the parameters $\theta$.

### 6.3 What problem this object solves

This construction solves a specific problem:

- a simple Gaussian is too rigid to match the target data,
- but a transformed Gaussian can be much more flexible,
- and if the transform is chosen carefully, the resulting density is still computable.

That last clause is the entire point. Many models can generate samples. Fewer models let you evaluate an exact density at a point.

---

## 7. Invertibility: what it means and what it buys you

Flow explanations often say "the transform must be invertible" and stop there. That is not enough.

### 7.1 Definition

A map

$$
f_\theta : \mathbb{R}^2 \to \mathbb{R}^2
$$

is **invertible** if every output comes from exactly one input.

Equivalently, there exists an inverse map

$$
f_\theta^{-1}
$$

such that

$$
f_\theta^{-1}(f_\theta(z)) = z
\quad\text{and}\quad
f_\theta(f_\theta^{-1}(x)) = x
$$

wherever the model is defined.

### 7.2 Why this matters for density evaluation

Suppose you observe a point $x$ and want to compute the model density at that point.

You need to answer:

> According to the model, which latent point produced this $x$?

If the map is invertible, the answer is unique:

$$
z = f_\theta^{-1}(x).
$$

That lets you score $x$ by:

1. moving it backward into latent space,
2. evaluating the simple base density there,
3. correcting for local area distortion.

If the map were not invertible, one observed point could come from multiple latent points, and the simple one-to-one density formula would break.

So invertibility is not cosmetic. It is the condition that makes the transformed model a tractable density model.

---

## 8. Neighborhoods, Jacobians, and local stretching

This is the place where explanations often become vague. So this section is explicit.

### 8.1 A neighborhood around a latent point

Fix a point $z_0 \in \mathbb{R}^2$.

A **neighborhood around $z_0$** means a set of points close to $z_0$.

The standard choice is an open ball of radius $\varepsilon > 0$:

$$
B_\varepsilon(z_0)
=
\{z \in \mathbb{R}^2 : \|z - z_0\| < \varepsilon\}.
$$

What is fixed here:

- the center point $z_0$,
- the radius $\varepsilon$.

What varies:

- the point $z$ inside that set.

This object matters because for continuous distributions, you reason about probabilities of **small regions**, not probabilities of exact points.

### 8.2 Density in terms of a small neighborhood

If $Z$ has density $p_Z$, then for a small neighborhood around $z_0$,

$$
P(Z \in B_\varepsilon(z_0))
\approx
p_Z(z_0)\,\mathrm{area}(B_\varepsilon(z_0)).
$$

That approximation says:

- for a small enough region, the density does not change much inside the region,
- so probability is approximately density times area.

### 8.3 Jacobian matrix

For a differentiable map

$$
f(z_1, z_2) =
\begin{bmatrix}
f_1(z_1, z_2) \\
f_2(z_1, z_2)
\end{bmatrix},
$$

the Jacobian matrix at a point $z$ is

$$
J_f(z)
=
\begin{bmatrix}
\frac{\partial f_1}{\partial z_1}(z) & \frac{\partial f_1}{\partial z_2}(z) \\
\frac{\partial f_2}{\partial z_1}(z) & \frac{\partial f_2}{\partial z_2}(z)
\end{bmatrix}.
$$

This matrix is the best linear approximation to $f$ near that point.

More precisely, near $z_0$,

$$
f(z) \approx f(z_0) + J_f(z_0)(z - z_0).
$$

So if you zoom in enough around one point, a smooth nonlinear map behaves approximately like a linear map.

### 8.4 What the determinant means

For a linear map in two dimensions, the absolute determinant gives the area-scaling factor.

So if

$$
A : \mathbb{R}^2 \to \mathbb{R}^2
$$

is linear, then small areas are multiplied by

$$
|\det A|.
$$

Therefore, for a smooth nonlinear map $f$, the local area scaling near $z_0$ is

$$
|\det J_f(z_0)|.
$$

Interpretation:

- if $|\det J_f(z_0)| > 1$, the map locally expands area,
- if $0 < |\det J_f(z_0)| < 1$, the map locally compresses area,
- if $|\det J_f(z_0)| = 1$, it locally preserves area.

This is the exact meaning of local stretching and compression.

### 8.5 A concrete linear example

Take the map

$$
f(z_1, z_2) = (2z_1, 3z_2).
$$

Its Jacobian is the constant matrix

$$
J_f =
\begin{bmatrix}
2 & 0 \\
0 & 3
\end{bmatrix}.
$$

So

$$
\det J_f = 6.
$$

That means any sufficiently small region has its area multiplied by about $6$ under the map.

So if probability mass is preserved, density at the image point must be divided by $6$.

This is the whole idea of the determinant correction in the change-of-variables formula.

---

## 9. The change-of-variables formula, derived from neighborhoods

Now we can derive the central formula instead of treating it as magic.

### 9.1 Start with one latent point and its image

Fix a latent point $z_0$ and define

$$
x_0 = f_\theta(z_0).
$$

Take a small neighborhood $B_\varepsilon(z_0)$ in latent space.

Its image in data space is

$$
f_\theta(B_\varepsilon(z_0))
=
\{f_\theta(z) : z \in B_\varepsilon(z_0)\}.
$$

### 9.2 Probability mass is preserved under relabeling by an invertible map

Because the transform just moves points, the probability mass of the latent neighborhood equals the probability mass of its image:

$$
P(Z \in B_\varepsilon(z_0))
=
P(X \in f_\theta(B_\varepsilon(z_0))).
$$

### 9.3 Approximate each side using density times area

For the latent side,

$$
P(Z \in B_\varepsilon(z_0))
\approx
p_Z(z_0)\,\mathrm{area}(B_\varepsilon(z_0)).
$$

For the observed side,

$$
P(X \in f_\theta(B_\varepsilon(z_0)))
\approx
p_X(x_0)\,\mathrm{area}(f_\theta(B_\varepsilon(z_0))).
$$

### 9.4 Use local area scaling

Near $z_0$,

$$
\mathrm{area}(f_\theta(B_\varepsilon(z_0)))
\approx
|\det J_{f_\theta}(z_0)|\,\mathrm{area}(B_\varepsilon(z_0)).
$$

Substitute this into the observed-side expression:

$$
P(X \in f_\theta(B_\varepsilon(z_0)))
\approx
p_X(x_0)\,|\det J_{f_\theta}(z_0)|\,\mathrm{area}(B_\varepsilon(z_0)).
$$

### 9.5 Set the two sides equal and cancel the common area term

So

$$
p_Z(z_0)\,\mathrm{area}(B_\varepsilon(z_0))
\approx
p_X(x_0)\,|\det J_{f_\theta}(z_0)|\,\mathrm{area}(B_\varepsilon(z_0)).
$$

Cancel the common factor:

$$
p_X(x_0)
=
\frac{p_Z(z_0)}{|\det J_{f_\theta}(z_0)|}.
$$

Since $z_0 = f_\theta^{-1}(x_0)$, we can rewrite this in terms of $x$:

$$
p_X(x)
=
p_Z\!\bigl(f_\theta^{-1}(x)\bigr)\,
\left|\det J_{f_\theta^{-1}}(x)\right|.
$$

That is the flow density formula.

### 9.6 Log form

Training uses log density, so the practical form is

$$
\log p_X(x)
=
\log p_Z\!\bigl(f_\theta^{-1}(x)\bigr)
+
\log \left|\det J_{f_\theta^{-1}}(x)\right|.
$$

This formula has two pieces:

1. **latent plausibility**:
   where does $x$ land after mapping backward to latent space, and how plausible is that latent point under the base Gaussian?

2. **local volume correction**:
   how much does the inverse transform expand or compress small areas near $x$?

### 9.7 Why the word "normalizing" appears

Without the determinant correction, transforming a density would generally produce a function that does not integrate to $1$.

The determinant term is the exact correction that keeps the transformed density properly normalized.

That is why the construction is called a **normalizing** flow.

---

## 10. One-dimensional sanity check

If the multidimensional formula feels abstract, reduce it to one dimension.

Suppose

$$
Y = 2X.
$$

Then intervals are stretched by a factor of $2$.

So density must be divided by $2$:

$$
p_Y(y) = p_X(y/2)\cdot \frac{1}{2}.
$$

The determinant term in higher dimensions is exactly the same idea, except now the scaling is by local area or volume rather than interval length.

---

## 11. Why a coupling transform is used

The transform must do two things at once:

- be flexible enough to reshape a Gaussian into a non-Gaussian target,
- still allow an inverse and a Jacobian determinant that are tractable.

A coupling layer is a design that balances those two goals.

### 11.1 Generic coupling idea

Split the input vector into two blocks.

In a 2-dimensional setting, the split is effectively one coordinate and one coordinate.

A simplified 2D coupling picture is:

$$
y_1 = g(x_1),
$$

$$
y_2 = h(x_2; x_1).
$$

Interpretation:

- the first coordinate is transformed by an invertible 1D map $g$,
- the second coordinate is transformed by another invertible 1D map $h$,
- but the parameters of that second transform depend on the first coordinate.

That dependency is the "coupling".

### 11.2 Why the Jacobian becomes easy

For the 2D form above,

$$
J =
\begin{bmatrix}
\frac{\partial y_1}{\partial x_1} & \frac{\partial y_1}{\partial x_2} \\
\frac{\partial y_2}{\partial x_1} & \frac{\partial y_2}{\partial x_2}
\end{bmatrix}
=
\begin{bmatrix}
\frac{\partial y_1}{\partial x_1} & 0 \\
\frac{\partial y_2}{\partial x_1} & \frac{\partial y_2}{\partial x_2}
\end{bmatrix}.
$$

The upper-right entry is zero because $y_1$ does not depend on $x_2$.

So the Jacobian is triangular, and its determinant is just the product of the diagonal terms:

$$
\det J
=
\frac{\partial y_1}{\partial x_1}
\cdot
\frac{\partial y_2}{\partial x_2}.
$$

That is much easier than taking the determinant of a fully dense, unconstrained Jacobian.

### 11.3 What Pyro's spline coupling helper does

Pyro's `spline_coupling` helper creates a `SplineCoupling` transform. The library implementation says one part of the input is put through an elementwise spline and the other part through a conditional spline that uses the first part as input.[^pyro_spline]

For this homework call,

```python
T.spline_coupling(2, count_bins=16, bound=6)
```

the input dimension is $2$, and if `split_dim` is not supplied, Pyro sets it to `input_dim // 2`, which is $1$ in this case.[^pyro_spline]

So the vector is split into:

- first coordinate,
- second coordinate.

That is why the 2D picture above is the right mental model.

---

## 12. What a spline is, and what `count_bins=16` means

### 12.1 Spline

A spline is a function defined piece by piece over sub-intervals of the input range.

Instead of one single formula over the whole line, you divide the input range into bins and assign a local curve on each bin.

### 12.2 Why splines are useful here

A simple affine map in one dimension has the form

$$
y = ax + b,
\qquad a > 0.
$$

That can only do uniform scaling and shifting.

A spline can do much more:

- stretch one interval strongly,
- compress another interval mildly,
- bend the distribution differently in different regions.

If the spline is constrained to be monotone increasing, then it remains invertible as a 1D map.

### 12.3 Bins and `count_bins=16`

A **bin** is one interval in the partition of the input range.

So `count_bins=16` means the spline uses $16$ intervals in its active region.[^pyro_spline]

More bins means the transform has more local freedom. Fewer bins means the transform is simpler and less flexible.

---

## 13. What `bound=6` means

Pyro's spline helper takes a `bound` parameter, and the spline implementation uses that value to define a bounded box such as $[-K, K] \times [-K, K]$ for the nontrivial spline action.[^pyro_bound]

The implementation also keeps the map equal to the identity outside the bounding box, with derivative matched continuously at the boundary.[^pyro_bound]

So in this homework:

- `bound=6` means the learned nonlinear warping happens inside a central region,
- and points outside that region are passed through unchanged by the spline part.

This is a real boundary condition, not a cosmetic tuning choice.

It prevents arbitrarily wild nonlinear tail behavior far from the region where the spline is meant to work.

---

## 14. What the library objects mean

The core code lines in the solution are short:

```python
base = dist.MultivariateNormal(torch.zeros(2), torch.eye(2))
xform = T.spline_coupling(2, count_bins=16, bound=6)
flow = dist.TransformedDistribution(base, [xform])
```

The point of this section is to unpack those three lines fully.

### 14.1 `base = dist.MultivariateNormal(torch.zeros(2), torch.eye(2))`

This creates the 2D standard Gaussian base distribution:

$$
Z \sim \mathcal{N}(0, I_2).
$$

- `torch.zeros(2)` is the vector $(0,0)$.
- `torch.eye(2)` is the $2 \times 2$ identity matrix.
- `MultivariateNormal` creates a Gaussian distribution object with that mean and covariance.[^mvn]

### 14.2 `xform = T.spline_coupling(2, count_bins=16, bound=6)`

This creates a learnable, invertible coupling transform in dimension $2$.[^pyro_spline]

So `xform` is not a distribution. It is a bijective map with trainable parameters.

### 14.3 `flow = dist.TransformedDistribution(base, [xform])`

PyTorch's `TransformedDistribution` is defined by starting from a base distribution and applying a sequence of transforms.[^td]

The official description is:

$$
X \sim \text{BaseDistribution},
\qquad
Y = f(X) \sim \text{TransformedDistribution}(\text{BaseDistribution}, f),
$$

with

$$
\log p(Y) = \log p(X) + \log |\det(dX/dY)|.
$$

So in this homework, `flow` is the actual model distribution:

- for sampling, draw from `base` and apply `xform`,
- for log density, invert `xform`, score under `base`, and add the log-Jacobian correction.[^td]

---

## 15. Sampling from the base and from the flow

### 15.1 Sampling from the base

When you call `base.sample([1000])`, you are drawing $1000$ independent samples from the 2D Gaussian.

Because each sample is a vector in $\mathbb{R}^2$, the result has shape `(1000, 2)`.

This plot is useful because it shows the raw latent cloud before any learned warping happens.

### 15.2 Sampling from the untrained flow

When you call `flow.sample([1000])` before training, the library samples from the base distribution and then applies the transform.[^td]

So the untrained flow plot answers a specific question:

> What shape does the chosen model architecture produce before data have changed the parameters?

This distinguishes three things that students often collapse together:

1. the target generator,
2. the base Gaussian,
3. the untrained flow model.

These are not the same object.

---

## 16. What `log_prob` is doing

PyTorch's `TransformedDistribution.log_prob(value)` is documented as scoring a sample by inverting the transforms and using the base distribution score together with the log absolute determinant of the Jacobian.[^td]

This sentence is dense. Here is the exact meaning.

Take one observed point $x$.

### Step 1: invert the transform

Compute

$$
z = f_\theta^{-1}(x).
$$

This moves the point backward into latent space.

### Step 2: score the latent point under the base Gaussian

Compute

$$
\log p_Z(z).
$$

This says how plausible that latent point is under the simple Gaussian.

### Step 3: correct for local area distortion

Compute

$$
\log \left|\det J_{f_\theta^{-1}}(x)\right|.
$$

This corrects for how the inverse transform expands or compresses tiny regions near $x$.

### Step 4: add the two pieces

The final result is

$$
\log p_\theta(x)
=
\log p_Z\!\bigl(f_\theta^{-1}(x)\bigr)
+
\log \left|\det J_{f_\theta^{-1}}(x)\right|.
$$

That is the number returned by `flow.log_prob(x)`.

---

## 17. The training objective

The solution uses

```python
loss = -flow.log_prob(data).mean()
```

This line deserves a full unpacking.

### 17.1 What `data` is

At each training step, `data` is a minibatch of observed 2D points sampled from the target generator.

If the minibatch has size $m$, then write it as

$$
x_1, x_2, \dots, x_m.
$$

### 17.2 What `flow.log_prob(data)` returns

This returns one log density value for each point:

$$
\log p_\theta(x_1),\ \log p_\theta(x_2),\ \dots,\ \log p_\theta(x_m).
$$

### 17.3 What `.mean()` does

Taking the mean gives the average log likelihood of the minibatch:

$$
\frac{1}{m}\sum_{j=1}^m \log p_\theta(x_j).
$$

### 17.4 Why the minus sign is there

Machine-learning optimizers are usually written as minimizers.

But statistically, we want to **maximize** average log likelihood.

So the code minimizes the negative average log likelihood:

$$
\mathcal{L}(\theta)
=
-\frac{1}{m}\sum_{j=1}^m \log p_\theta(x_j).
$$

### 17.5 What this objective is checking

Each term $\log p_\theta(x_j)$ checks:

> According to the current model, how plausible is this observed data point?

If the model assigns low density to points the generator often produces, those log densities become very negative, and the loss becomes large.

So minimizing the loss pushes the model to place more probability density on regions where the target data actually live.

### 17.6 Population interpretation

The ideal population objective is

$$
\mathbb{E}_{X \sim p_{\text{data}}}\bigl[-\log p_\theta(X)\bigr].
$$

The minibatch mean is a Monte Carlo approximation to that expectation.

---

## 18. Why drawing fresh data each step is legitimate

In many machine-learning problems you are given one fixed dataset.

Here the homework gives direct access to the generator itself.

So at each step you can draw a fresh minibatch from the target process.

That means the optimization is repeatedly seeing new samples from the same underlying population rather than trying to memorize one tiny fixed cloud.

This is statistically legitimate because the target generator itself is available.

---

## 19. What the rest of the training loop means

The remaining training lines are:

```python
params = xform.parameters()
optimizer = torch.optim.Adam(params, lr=1e-2)

optimizer.zero_grad()
loss.backward()
optimizer.step()
flow.clear_cache()
```

### 19.1 `xform.parameters()`

The transform contains trainable numerical parameters. In this case those parameters live inside the spline-coupling transform and its internal neural-network components.[^pyro_spline]

This call collects the numbers that training is allowed to update.

### 19.2 `optimizer = torch.optim.Adam(params, lr=1e-2)`

This creates the update rule. The optimizer will adjust the transform parameters using gradients of the loss.

### 19.3 `optimizer.zero_grad()`

Gradients from the previous step must be cleared before computing new ones.

### 19.4 `loss.backward()`

This computes derivatives of the loss with respect to the transform parameters.

In plain English:

- it measures how a small change in each parameter would change the loss.

### 19.5 `optimizer.step()`

This updates the parameters using those gradients.

So after this line, the transform $f_\theta$ has changed shape slightly.

### 19.6 `flow.clear_cache()`

Pyro's transform implementation caches intermediate forward and inverse values together with Jacobian information.[^pyro_spline]

That is useful only while the parameters are unchanged.

After `optimizer.step()`, the parameters have changed, so cached values computed under the old parameters are stale.

`flow.clear_cache()` enforces this rule:

> after the transform parameters change, future inverse and Jacobian computations must be recomputed under the new parameter values.

So the cache clear is not random ritual. It is a consistency step.

---

## 20. Deep trace 1: how one observed point is scored

Take one observed point $x$ from the minibatch.

### Step 1: start in data space

You begin with $x \in \mathbb{R}^2$.

At this stage, the model does not know the generator's hidden variables $w$ and $i$ that originally produced the point. Those variables are not part of the model.

### Step 2: move backward through the inverse transform

Compute

$$
z = f_\theta^{-1}(x).
$$

This asks:

> under the current model, which latent Gaussian point corresponds to this observed point?

### Step 3: evaluate latent plausibility

Compute

$$
\log p_Z(z).
$$

If $z$ lands near a high-density part of the Gaussian, this term is relatively large. If it lands deep in a tail, this term is much smaller.

### Step 4: compute the local volume correction

Compute

$$
\log \left|\det J_{f_\theta^{-1}}(x)\right|.
$$

This measures how the inverse map changes tiny areas near $x$.

### Step 5: add the two pieces

The model log density is

$$
\log p_\theta(x)
=
\log p_Z\!\bigl(f_\theta^{-1}(x)\bigr)
+
\log \left|\det J_{f_\theta^{-1}}(x)\right|.
$$

### Step 6: send it into the loss

That value is one term in the minibatch average.

If many observed points receive log densities that are too small, the loss becomes large, and training changes the transform parameters so those important regions are assigned higher density.

---

## 21. Deep trace 2: how one sample is generated after training

Now go in the forward direction.

### Step 1: draw one latent point

Sample

$$
z \sim \mathcal{N}(0, I_2).
$$

This is one simple random point from the base Gaussian.

### Step 2: apply the learned transform

Compute

$$
x = f_\theta(z).
$$

This pushes the latent point into data space.

### Step 3: interpret the geometry

If training succeeded, then the transform has learned how to send Gaussian mass into the curved and line-like regions where the target data tend to live.

So generation works because the learned warp reshapes the Gaussian cloud.

### Step 4: repeat

Repeating the same forward rule many times gives a sample cloud from the learned model distribution.

That cloud should visually resemble the target generator more than the raw Gaussian cloud does.

---

## 22. What "one coupling layer is enough" means here

The assignment says one spline coupling layer should be enough for this toy problem.[^repo]

This is not a universal theorem about flows.

It means only that for this specific problem:

- the data are 2-dimensional,
- the target geometry is not too complicated,
- and the chosen spline coupling layer is flexible enough to fit the main structure without stacking many layers.

So "enough" here is task-specific, not a claim about all flow problems.

---

## 23. Misconception blocks

### 23.1 Density is not probability at a point

Do not confuse

- "$p_X(x)$ is large"

with

- "$P(X = x)$ is large".

For continuous variables, $P(X = x) = 0$ for every exact point.

A large density means neighborhoods around that point receive more probability mass per unit area.

### 23.2 Base distribution is not target distribution

Do not confuse

- the base Gaussian,

with

- the target data distribution.

The base Gaussian is chosen for tractability, not realism.

### 23.3 Latent variable is not the generator's hidden variable

Do not confuse

- the model's latent variable $Z$,

with

- the generator's hidden variables $w$ and $i$.

The model is not required to recover $w$ and $i$. It is only required to learn a good density over the observed 2D points.

### 23.4 Invertible does not mean linear

Do not confuse

- "invertible"

with

- "linear".

A spline coupling transform is nonlinear and still invertible.

Invertibility only means every output corresponds to one input and vice versa.

### 23.5 Easy to sample is not the same as easy to score

Do not confuse

- "I can generate samples from this process"

with

- "I can evaluate a closed-form density for this process".

The homework target generator is easy to sample from, but its density is not presented in a simple explicit form. The flow model is useful because it gives both sampling and density evaluation.

### 23.6 A better-looking plot is not exact recovery

Do not confuse

- "the trained sample cloud looks more similar to the target cloud"

with

- "the model has exactly recovered the true target distribution".

The homework mainly checks qualitative fit through plots. Visual improvement is evidence of learning, not proof of exact equality.

---

## 24. Compact summary of the whole solution

Here is the full logic of Problem 5 in the order it becomes meaningful.

1. The homework generator makes a 2D target distribution with a curved branch and a noisier line-like branch.
2. A single Gaussian is too simple to match that target directly.
3. Choose a simple latent source:
   $$
   Z \sim \mathcal{N}(0, I_2).
   $$
4. Choose a learnable invertible transform $f_\theta$ implemented as a spline coupling map.
5. Define the model by
   $$
   X = f_\theta(Z).
   $$
6. Use the change-of-variables formula
   $$
   p_\theta(x)
   =
   p_Z\!\bigl(f_\theta^{-1}(x)\bigr)
   \left|\det J_{f_\theta^{-1}}(x)\right|.
   $$
7. Train $\theta$ by minimizing negative average log likelihood on samples from the target generator.
8. After training, sample from the model by drawing $z$ from the Gaussian and pushing it through the learned transform.

That is the entire statistical and geometric structure of the problem.

---

## 25. Final vocabulary checklist

If the document has done its job, each of the following should now have a local meaning.

- **data space**: the space where observed 2D points live.
- **latent space**: the space where the simple base variable lives.
- **latent point $z$**: one realized point in latent space.
- **base distribution / base Gaussian**: the starting simple distribution before transformation.
- **mean vector**: the coordinatewise expectation of a random vector.
- **covariance matrix**: the matrix of variances and pairwise covariances.
- **identity matrix $I_2$**: the $2 \times 2$ matrix with ones on the diagonal and zeros elsewhere.
- **standard 2D Gaussian**: $\mathcal{N}(0, I_2)$.
- **invertible / bijective**: every output corresponds to exactly one input.
- **Jacobian**: the matrix of first derivatives of a vector-valued map.
- **determinant of the Jacobian**: the local area-scaling factor, up to sign.
- **neighborhood around a point**: a small set such as $B_\varepsilon(z_0)$ around that point.
- **coupling layer**: a structured transform where one block conditions the transformation of another block.
- **spline**: a piecewise-defined curve used here to get flexible but invertible 1D transformations.
- **log likelihood**: the log density assigned by the model to observed data.
- **negative log likelihood**: the quantity minimized during training.
- **TransformedDistribution**: a distribution obtained by sampling from a base distribution and applying one or more transforms.[^td]

---

## Sources

[^repo]: Repository materials: [current walkthrough](https://github.com/jensonp/cs179-chapter-2-probability/tree/main/problem5_normalizing_flows_walkthrough) and [homework solution guide](https://raw.githubusercontent.com/jensonp/cs179-chapter-2-probability/main/hw2_solutions/README.md).
[^mvn]: PyTorch distributions documentation: [`MultivariateNormal`](https://docs.pytorch.org/docs/stable/distributions.html), described as a multivariate normal distribution parameterized by a mean vector and a covariance matrix.
[^eye]: PyTorch documentation: [`torch.eye`](https://docs.pytorch.org/docs/stable/generated/torch.eye.html), which returns a 2-D tensor with ones on the diagonal and zeros elsewhere.
[^td]: PyTorch distributions documentation: [`TransformedDistribution`](https://docs.pytorch.org/docs/stable/distributions.html), which samples from a base distribution, applies transforms, and computes `log_prob` by inverting the transforms and using the log absolute determinant Jacobian correction.
[^pyro_spline]: Pyro documentation for [`spline_coupling`](https://docs.pyro.ai/en/stable/_modules/pyro/distributions/transforms/spline_coupling.html). The helper creates a `SplineCoupling` transform; if `split_dim` is omitted it defaults to `input_dim // 2`, and the implementation uses one part of the input for an elementwise spline and the other part for a conditional spline.
[^pyro_bound]: Pyro spline implementation notes, including the bounded spline region and identity behavior outside the bounding box, are documented in the Pyro transform code and spline implementation: [`spline_coupling`](https://docs.pyro.ai/en/stable/_modules/pyro/distributions/transforms/spline_coupling.html) and the associated spline implementation described by the Pyro source linked there.

# 2.6 Change-of-Variable Models

The central principle of change-of-variable modeling is **probability conservation**.

A transformation may move probability mass from one region to another. It may stretch the space in some directions and compress it in others. But it cannot create or destroy total probability. The Jacobian term is exactly the correction factor that enforces that conservation.

Everything in this section becomes easier if one sequence is kept explicit:

1. start from a base variable whose density is easy to understand;
2. transform it through an invertible map;
3. compute the transformed density by correcting for local stretching or compression;
4. check the transformed support.

That is the whole logic of the section. The copula and normalizing-flow material at the end is not a new story. It is an extension of the same one.

## Why transformations appear in probabilistic modeling

The motivation is simple. Some variables are awkward to model directly in the space where they are observed.

Examples:

- a positive variable may be easier to model on a log scale;
- a heavy-tailed variable may become more regular after transformation;
- multivariate dependence may become easier to describe after mapping coordinates to percentile space;
- a complex observed distribution may become easier to represent as an invertible transform of a simple base Gaussian.

So change-of-variable modeling is not just a calculus trick. It is a modeling strategy: represent a difficult distribution as a transformed version of an easier one.

## Scalar change of variables

Let

$$
X=f(Z),
$$

and suppose the map is invertible on the region of interest with inverse

$$
g=f^{-1}.
$$

Then the density of $X$ is

$$
p_X(x)=p_Z(g(x))\,|g'(x)|.
$$

This formula says exactly two things:

1. evaluate the base density at the inverse point that maps to $x$;
2. multiply by the magnitude of the local inverse scaling.

The hidden structure here matters. The formula is not “density after plugging into a function.” It is “density after plugging into the inverse map and correcting for local width change.”

## Why the derivative appears

The derivative appears because a short interval in $x$-space maps back to a short interval in $z$-space of a different width.

- If the transformation doubles local width, the density height must be halved.
- If the transformation halves local width, the density height must be doubled.

That is the whole purpose of the Jacobian factor. Density is not preserved pointwise. Probability mass is preserved across corresponding intervals, so density must adjust when width changes.

## Case A: monotone invertible map

When $f$ is monotone and invertible on the support, the one-branch formula is valid directly.

### CDF derivation

If $f$ is increasing, then

$$
F_X(x)
=
\mathbb{P}(X\le x)
=
\mathbb{P}(f(Z)\le x)
=
\mathbb{P}(Z\le g(x))
=
F_Z(g(x)).
$$

Differentiating gives

$$
p_X(x)=p_Z(g(x))\,g'(x).
$$

If $f$ is decreasing, then the derivative is negative, so the absolute value is needed to keep the density nonnegative.

### Local-interval derivation

The same formula can be understood more geometrically.

A small interval near $x$ corresponds through the inverse map to a small interval near $z=g(x)$. The probability in those corresponding intervals must match. So the density changes by exactly the ratio of local widths.

This is often the more intuitive derivation because it makes the Jacobian look like what it is: a local width-conversion factor.

## Case B: non-monotone or multi-branch map

If the transformation is not globally invertible, then the one-branch formula is not valid by itself.

Instead, every inverse branch that maps to the same $x$ contributes probability mass, and all such contributions must be summed.

So the hidden assumption behind the simple scalar formula is not just differentiability. It is **invertibility on the support region being used**.

That boundary condition should never be left implicit. This is one of the most common failure points in change-of-variable calculations.

## Example: scaling a uniform variable

Let

$$
Z\sim \mathrm{Unif}[0,1],
\qquad
X=2Z.
$$

Then the inverse map is

$$
g(x)=x/2,
\qquad
g'(x)=1/2.
$$

Therefore

$$
p_X(x)=p_Z(x/2)\cdot \frac12.
$$

Now apply the support condition carefully:

$$
0\le x/2 \le 1
\quad\Longleftrightarrow\quad
0\le x\le 2.
$$

Since $p_Z(z)=1$ on $[0,1]$, we get

$$
p_X(x)=\frac12
\qquad\text{for }0\le x\le 2,
$$

and $p_X(x)=0$ elsewhere.

This is the simplest exact picture of probability conservation:

- the interval length doubled from $1$ to $2$;
- the density height dropped from $1$ to $1/2$;
- total probability remained equal to $1$.

## Example: why the absolute value is necessary

Let

$$
Z\sim \mathrm{Unif}[0,1],
\qquad
X=1-Z.
$$

Then

$$
g(x)=1-x,
\qquad
g'(x)=-1.
$$

So

$$
p_X(x)=p_Z(1-x)\,|-1|=p_Z(1-x).
$$

Because $1-x\in[0,1]$ exactly when $x\in[0,1]$, the transformed density is still uniform on $[0,1]$.

This example is not about generating a new family. Its job is narrower and more important: it validates the sign rule.

- the derivative can be negative;
- density cannot be negative;
- therefore the Jacobian correction must use an absolute value.

## Example: lognormal distribution

A lognormal distribution is the canonical first nontrivial transformed family.

Let

$$
Z\sim \mathcal{N}(\mu,\sigma^2),
\qquad
X=e^Z.
$$

Then the transformed support is

$$
x>0.
$$

The inverse map is

$$
z=\log x,
\qquad
\frac{dz}{dx}=\frac1x.
$$

Therefore

$$
p_X(x)
=
\frac{1}{x\sqrt{2\pi\sigma^2}}
\exp\!\left(
-\frac{(\log x-\mu)^2}{2\sigma^2}
\right),
\qquad x>0.
$$

The factor $1/x$ is the Jacobian correction. Without it, the transformed density would not integrate to one.

### Why the lognormal is skewed

The asymmetry comes from the exponential map.

Equal distances on the $Z$-axis become multiplicative, not additive, changes on the $X$-axis:

- moving from $Z=0$ to $Z=1$ sends $X$ from $1$ to $e$;
- moving from $Z=1$ to $Z=2$ sends $X$ from $e$ to $e^2$.

So the right side of the $X$-axis is stretched more aggressively than the left, creating a long right tail.

### Probability translation

If

$$
Z\sim \mathcal{N}(0,1),
$$

then

$$
\mathbb{P}(1\le X\le e)=\mathbb{P}(0\le Z\le 1).
$$

This is the clean operational lesson: transformed-variable probabilities are often easiest to compute by mapping the event back to the base variable.

## Multivariate change of variables

In several dimensions, the derivative is replaced by a Jacobian determinant.

Let

$$
X=f(Z),
$$

with inverse

$$
g=f^{-1}.
$$

Then

$$
p_X(x)=p_Z(g(x))\,\bigl|\det J_g(x)\bigr|,
$$

where $J_g(x)$ is the Jacobian matrix of the inverse map.

Its $(i,j)$ entry is

$$
\bigl(J_g(x)\bigr)_{ij}=\frac{\partial g_i}{\partial x_j}.
$$

The determinant is the local volume-scaling factor.

- In one dimension, local width changes by $|g'(x)|$.
- In several dimensions, local volume changes by $|\det J_g(x)|$.

That is the exact generalization. Width scaling becomes volume scaling.

## Geometric meaning of the determinant

The determinant tells you how a tiny box in data space maps back into latent space.

- If the map doubles local area, density must be halved.
- If the map compresses local volume by a factor of $10$, density must be multiplied by $10$.

The absolute value is still required. A negative determinant indicates orientation reversal, not negative probability.

So the determinant is not an arbitrary algebraic decoration. It is the local volume-conversion factor required by probability conservation.

## Example: anisotropic scaling

Let

$$
X_1=2Z_1,\qquad X_2=3Z_2.
$$

Then the inverse map is

$$
Z_1=X_1/2,\qquad Z_2=X_2/3.
$$

So the inverse Jacobian is

$$
J_g(x)=
\begin{pmatrix}
1/2 & 0\\
0 & 1/3
\end{pmatrix},
$$

and

$$
\det J_g(x)=\frac16.
$$

So a unit area in latent space becomes an area-$6$ rectangle in data space, and the density must be reduced by a factor of $6$.

This is the multivariate analogue of stretching a uniform interval. The same conservation law is operating, only now in area rather than length.

## Optional enrichment: copula models

Copulas separate two modeling tasks that are often mixed together:

1. the one-dimensional shape of each coordinate;
2. the dependence structure coupling the coordinates.

For two variables,

$$
\mathbb{P}(X_1\le x_1, X_2\le x_2)
=
C\bigl(F_1(x_1),F_2(x_2)\bigr),
$$

where $F_1$ and $F_2$ are marginal CDFs.

Define

$$
U_1=F_1(X_1),\qquad U_2=F_2(X_2).
$$

When the marginals are continuous, each $U_i$ is uniform on $[0,1]$. This is the probability integral transform.

The copula

$$
C(u_1,u_2)=\mathbb{P}(U_1\le u_1,U_2\le u_2)
$$

is then the joint CDF of those transformed uniform variables.

### Conceptual payoff

The marginal CDFs remove original units and marginal shape. What remains is an object that captures dependence only.

That is why copulas are useful: they let you model marginal behavior and dependence structure separately.

### Gaussian copula pipeline

A standard pipeline is:

1. estimate each marginal CDF;
2. map observations into percentile space using those marginals;
3. optionally move from uniform percentile space to Gaussian space using $\Phi^{-1}$;
4. fit a Gaussian dependence model in that transformed space.

This produces a dependence model that is separated from the original marginal shapes.

## Optional enrichment: normalizing flows

Normalizing flows extend the same change-of-variable principle to learned invertible maps.

Start with a simple base density $p_Z$, often Gaussian, and define

$$
X=f(Z),
$$

where $f$ is invertible. Then

$$
\log p_X(x)
=
\log p_Z(f^{-1}(x))
+
\log\bigl|\det J_{f^{-1}}(x)\bigr|.
$$

Flows are often built as compositions of simple invertible layers:

$$
f=f_T\circ\cdots\circ f_1.
$$

Because Jacobian determinants multiply under composition, the log-determinants add. That is the computational reason flows are practical.

The structural constraints are simple but strict:

- each layer must be invertible;
- each layer’s determinant must be cheap to compute.

So a normalizing flow should be viewed as a learned sequence of legal change-of-variable steps.

## Retain from 2.6

- Change-of-variable modeling is probability conservation plus a Jacobian correction.
- In one dimension the correction is $|g'(x)|$; in several dimensions it is $|\det J_g(x)|$.
- Support conditions must always be checked after transformation.
- The one-branch scalar formula requires invertibility on the region of interest.
- Lognormal, copulas, and normalizing flows are all instances of the same structural idea: start from a simpler representation, transform, and correct the density.

## Do not confuse in 2.6

- Do not forget the transformed support after mapping variables.
- Do not forget the absolute value in the Jacobian factor.
- Do not apply the one-branch scalar formula to a map with multiple inverse branches.
- Do not confuse a convenient base density with the transformed density actually seen in data space.

# 2.6 Change-of-Variable Models

The central principle of change-of-variable modeling is **probability conservation**.

A transformation can move probability mass and can stretch or compress the space in which the variable lives, but it cannot create or destroy total probability.  
The Jacobian term is the correction factor that enforces that conservation.

This section keeps one sequence explicit:

1. start from a base variable whose density is easy to understand;
2. transform that variable through an invertible map;
3. compute the transformed density by correcting for local stretching or compression.

The reach material on copulas and normalizing flows is included at the end as an extension of the same principle.

## Scalar change of variables

Let $X=f(Z)$, and suppose the map is invertible on the region of interest with inverse $g=f^{-1}$.

Then the density of $X$ is

$$
p_X(x)=p_Z(g(x))\,|g'(x)|.
$$

This formula says exactly two things:

- evaluate the base density at the corresponding inverse point;
- multiply by the magnitude of the local inverse scaling.

### Why the derivative appears

The derivative appears because a small interval in $x$-space corresponds to a small interval in $z$-space of different width.

- If the transformation doubles local width, the density height must be halved.
- If the transformation halves local width, the density height must be doubled.

That is the whole purpose of the Jacobian factor.

## Case A: monotone invertible map

When $f$ is monotone and invertible, the formula above is valid directly.

### CDF derivation

If $f$ is increasing, then

$$
F_X(x)
=
\mathbb{P}(X \le x)
=
\mathbb{P}(f(Z)\le x)
=
\mathbb{P}(Z \le g(x))
=
F_Z(g(x)).
$$

Differentiating gives

$$
p_X(x)
=
p_Z(g(x))\,g'(x).
$$

If $f$ is decreasing, the derivative is negative, so the absolute value is needed to keep the density nonnegative.

### Local-interval derivation

The same result can be read geometrically.  
A small interval near $x$ maps back to a small interval near $z=g(x)$.  
Probability mass in those corresponding intervals must match, so density must be corrected by the local width ratio.

## Case B: non-monotone or multi-branch map

If the transformation is not globally invertible, the one-branch formula is not valid by itself.  
Instead, each inverse branch that maps to the same $x$ contributes a term, and those contributions must be summed.

So the hidden assumption behind the scalar formula is not merely “differentiable.”  
It is **invertible on the support region being used**.

This boundary condition should never be left implicit.

## Example: scaling a uniform variable

Let

$$
Z \sim \mathrm{Unif}[0,1],
\qquad
X=2Z.
$$

Then the inverse map is

$$
g(x)=x/2,
\qquad
g'(x)=1/2.
$$

So

$$
p_X(x)=p_Z(x/2)\cdot \frac{1}{2}.
$$

Now apply the support condition:

$$
0 \le x/2 \le 1
\quad\Longleftrightarrow\quad
0 \le x \le 2.
$$

Since $p_Z(z)=1$ on $[0,1]$,

$$
p_X(x)=\frac{1}{2}
\qquad\text{for } 0\le x\le 2,
$$

and $p_X(x)=0$ elsewhere.

This is the simplest exact picture of probability conservation:

- the interval length doubled from $1$ to $2$;
- the density height dropped from $1$ to $1/2$;
- total probability stayed equal to $1$.

## Example: why the absolute value is necessary

Let

$$
Z \sim \mathrm{Unif}[0,1],
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

Because $1-x \in [0,1]$ exactly when $x \in [0,1]$, the transformed density is still uniform on $[0,1]$.

This example is not about a new family.  
Its only job is to validate the sign rule:

- the derivative can be negative;
- density cannot be negative;
- therefore the Jacobian factor must use absolute value.

## Example: lognormal distribution

A lognormal distribution is the canonical “first nontrivial” transformed family.

Let

$$
Z \sim \mathcal{N}(\mu,\sigma^2),
\qquad
X=e^Z.
$$

Then $X>0$, so the transformed support is

$$
x>0.
$$

The inverse map is

$$
z=\log x,
\qquad
\frac{dz}{dx}=\frac{1}{x}.
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

The extra factor $1/x$ is the Jacobian correction.  
Without it, the transformed density would not integrate to one.

### Why the lognormal is skewed

The asymmetry comes from the exponential map.

Equal distances on the $Z$-axis become multiplicative, not additive, changes on the $X$-axis:

- moving from $Z=0$ to $Z=1$ sends $X$ from $1$ to $e$;
- moving from $Z=1$ to $Z=2$ sends $X$ from $e$ to $e^2$.

So the right side of the $X$-axis gets stretched more strongly than the left side, creating the long right tail.

### Probability translation

If

$$
Z \sim \mathcal{N}(0,1),
$$

then

$$
\mathbb{P}(1 \le X \le e)
=
\mathbb{P}(0 \le Z \le 1).
$$

This is the clean operational lesson: transformed-variable probabilities are often easiest to compute by mapping the event back to the base variable.

## Multivariate change of variables

In multiple dimensions, the scalar derivative is replaced by a Jacobian determinant.

Let $X=f(Z)$, with inverse $g=f^{-1}$.  
Then

$$
p_X(x)
=
p_Z(g(x))\,\bigl|\det J_g(x)\bigr|,
$$

where $J_g(x)$ is the Jacobian matrix of the inverse map.

Its $(i,j)$ entry is

$$
\bigl(J_g(x)\bigr)_{ij}
=
\frac{\partial g_i}{\partial x_j}.
$$

The determinant is the local volume-scaling factor.

- In one dimension, local width changes by $|g'(x)|$.
- In several dimensions, local volume changes by $|\det J_g(x)|$.

If the map doubles area near a point, the density there must be halved.  
If it shrinks volume by a factor of $10$, the density must be multiplied by $10$.

### Example: anisotropic scaling

Let

$$
X_1=2Z_1,
\qquad
X_2=3Z_2.
$$

Then the inverse map is

$$
Z_1 = X_1/2,
\qquad
Z_2 = X_2/3.
$$

So the inverse Jacobian is

$$
J_g(x)
=
\begin{pmatrix}
1/2 & 0 \\
0 & 1/3
\end{pmatrix},
$$

and therefore

$$
\det J_g(x)=\frac{1}{6}.
$$

So a unit area in latent space becomes an area-$6$ rectangle in data space, and the density must be reduced by a factor of $6$.

The absolute value is still required.  
A negative determinant means orientation reversal, not negative probability.

## Optional enrichment: copula models

Copulas separate two modeling tasks that are often mixed together:

1. the one-dimensional shape of each coordinate;
2. the dependence structure coupling the coordinates.

For two variables,

$$
\mathbb{P}(X_1 \le x_1, X_2 \le x_2)
=
C\bigl(F_1(x_1), F_2(x_2)\bigr),
$$

where $F_1$ and $F_2$ are the marginal CDFs.

Define

$$
U_1 = F_1(X_1),
\qquad
U_2 = F_2(X_2).
$$

When the marginals are continuous, each $U_i$ is uniform on $[0,1]$.  
That is the probability integral transform.

The copula $C$ is then the joint CDF of the transformed uniform variables:

$$
C(u_1,u_2)=\mathbb{P}(U_1 \le u_1, U_2 \le u_2).
$$

This is the conceptual payoff:

- the marginal CDFs remove original units and marginal shape;
- the remaining object captures dependence only.

### Gaussian copula pipeline

A standard pipeline is:

1. estimate each marginal CDF;
2. map each observation to percentile space through the marginal CDF;
3. optionally map uniform percentiles to Gaussian scale through $\Phi^{-1}$;
4. fit a Gaussian dependence model in that transformed space.

This gives a dependence model that is separate from the marginal shapes.

## Optional enrichment: normalizing flows

Normalizing flows extend the same change-of-variables principle to learned invertible maps.

Start with a simple base density $p_Z$, often Gaussian, and define

$$
X=f(Z),
$$

where $f$ is invertible.

Then

$$
\log p_X(x)
=
\log p_Z(f^{-1}(x))
+
\log\bigl|\det J_{f^{-1}}(x)\bigr|.
$$

Flows are often built as compositions of simple invertible layers:

$$
f = f_T \circ \cdots \circ f_1.
$$

Because Jacobian determinants multiply under composition, the log-determinants add.  
That is the computational reason flows are practical.

The key constraints are:

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

- Do not forget the support restriction after transforming a variable.
- Do not forget the absolute value in the Jacobian factor.
- Do not apply the one-branch scalar formula to a map with multiple inverse branches.
- Do not confuse a convenient base density with the transformed density actually seen in data space.

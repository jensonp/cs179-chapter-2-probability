# 2.4 Convexity

This section is supporting background rather than core probability machinery, but it earns its place for a very practical reason. In Section 2.3, likelihoods, posteriors, and model-selection criteria were introduced as objects we might want to optimize. The natural next question is:

$$
\text{When does that optimization problem have clean global structure rather than a maze of bad local minima?}
$$

Convexity is one of the main answers.

The point of this section is not to turn convex analysis into a separate course. The point is to explain why some estimation objectives are globally well behaved, why some have unique solutions, and why exponential-family models so often lead to optimization problems that are easier to reason about than they initially look.

There are four ideas to keep separate and then connect:

- a **convex set** is a domain with no holes along line segments;
- a **convex function** bends upward in the right global sense;
- **Jensen’s inequality** is the probability version of that geometry;
- in canonical exponential-family models, the curvature of the negative log-likelihood is controlled by a covariance matrix, which is why convexity appears so naturally.

## Why convexity appears in an inference chapter

Optimization enters probability and statistics because many inferential tasks are phrased as “choose the parameter value that makes some criterion smallest or largest.”

Examples include:

- maximize likelihood;
- minimize negative log-likelihood;
- maximize posterior density;
- minimize regularized empirical risk.

The danger in optimization is not only computational cost. It is also structural ambiguity. If an objective has many local minima, then a solver may stop at a solution that is not globally best, and the mathematical interpretation of the estimate becomes harder to trust.

Convexity helps because it connects local and global structure. For convex functions, a point that looks locally optimal is already globally optimal. That is the real reason the topic belongs here.

## Convex sets

A set $S$ is **convex** if for any two points $x,x'\in S$ and any mixing weight $\alpha\in[0,1]$, the convex combination

$$
\alpha x + (1-\alpha)x'
$$

also belongs to $S$.

This is a geometric closure property. A convex set contains the entire line segment between any two of its points.

That condition matters because convexity of a function is only defined relative to a domain where these line segments stay inside the domain. If the domain itself has gaps, then statements comparing a function value at a midpoint to values at the endpoints stop making sense globally.

### Intuition

The simplest examples are worth holding onto:

- an interval on the real line is convex;
- a filled disk is convex;
- a triangle together with its interior is convex;
- a crescent shape or a ring is not convex, because some line segment between two interior points exits the set.

When optimization is restricted to a convex feasible set, “moving partway toward another feasible point” keeps you feasible. That is already a major structural convenience.

## Convex functions

A function $f$ defined on a convex domain is **convex** if

$$
f\bigl(\alpha x + (1-\alpha)x'\bigr)
\le
\alpha f(x) + (1-\alpha)f(x')
$$

for all $x,x'$ in the domain and all $\alpha\in[0,1]$.

This inequality should be read in the right order:

1. average the inputs;
2. evaluate the function at that averaged input;
3. compare with averaging the two function values.

Convexity says the function evaluated after averaging is never larger.

That sounds technical, but the picture is simple: the graph of a convex function lies below every secant line connecting two points on the graph.

### Why this definition matters

Convexity is not a statement about monotonicity. A convex function may increase, decrease, or do both. The defining property is about **curvature**, not direction.

It is also not the same thing as “looks bowl-shaped” in a casual sketch. The actual condition is global: the secant-line inequality must hold everywhere on the domain, not just near one point.

### Strict convexity

A function is **strictly convex** if

$$
f\bigl(\alpha x + (1-\alpha)x'\bigr)
<
\alpha f(x) + (1-\alpha)f(x')
$$

whenever $x\ne x'$ and $0<\alpha<1$.

Strict convexity rules out flat line segments on the graph. This is the condition that often upgrades “there may be many minimizers” to “the minimizer is unique.”

That distinction matters in estimation:

- convexity is enough to guarantee that every local minimum is global;
- strict convexity is what often guarantees that the estimator is unique.

## Three equivalent viewpoints

The defining inequality is important, but it becomes much easier to use once it is connected to equivalent first-order and second-order characterizations.

### 1. Secant-line view

A convex graph lies below every secant line connecting two of its points.

This is the direct geometric meaning of the definition.

### 2. First-order view

If $f$ is differentiable, convexity is equivalent to

$$
f(x') \ge f(x) + \nabla f(x)\cdot(x'-x).
$$

This means the tangent line or tangent plane at $x$ is a global lower bound on the function.

That is a remarkable statement. For a generic nonlinear function, a tangent approximation is only local. For a convex function, the tangent plane never overshoots the graph anywhere in the domain.

This is why first-order optimization methods have such a clean interpretation for convex objectives: the local slope points in a globally meaningful direction.

### 3. Second-order view

If second derivatives exist, convexity is equivalent to

$$
\nabla^2 f(x)\succeq 0.
$$

That means the Hessian is positive semidefinite. Equivalently, for every vector $v$,

$$
v^T\nabla^2 f(x)\,v\ge 0.
$$

So every directional second derivative is nonnegative. There are no directions of negative curvature.

This is the most useful viewpoint when analyzing statistical objectives, because many such objectives come with Hessians that can be written in a recognizable algebraic form.

## Why convexity matters for optimization

Now the payoff can be stated clearly.

If $f$ is convex, then every local minimum is a global minimum.

If $f$ is strictly convex, then there is at most one minimizer.

These are not cosmetic facts. They are exactly the structural guarantees that make an optimization problem well behaved from an inferential perspective.

### Positive semidefinite versus positive definite

This distinction should not be blurred.

- If the Hessian is **positive semidefinite**, flat directions may still exist.
- If the Hessian is **positive definite**, all nonzero directions curve upward strictly.

So positive semidefinite curvature is enough for convexity, but not enough for uniqueness. Positive definite curvature is the stronger condition that removes flat valleys.

## Fully explicit example: $f(x)=x^2$

The function

$$
f(x)=x^2
$$

is the canonical one-dimensional convex example. It is worth checking algebraically rather than only by picture.

Take any $x,x'$ and $\alpha\in[0,1]$. Then

$$
f\bigl(\alpha x + (1-\alpha)x'\bigr)
=
(\alpha x + (1-\alpha)x')^2.
$$

Expanding gives

$$
\alpha x^2 + (1-\alpha)x'^2 - \alpha(1-\alpha)(x-x')^2.
$$

Since

$$
-\alpha(1-\alpha)(x-x')^2 \le 0,
$$

we obtain

$$
(\alpha x + (1-\alpha)x')^2
\le
\alpha x^2 + (1-\alpha)x'^2.
$$

This is convexity in exact algebraic form.

The correction term

$$
-\alpha(1-\alpha)(x-x')^2
$$

is the whole story. It measures how far the parabola dips below the secant line.

This is a useful template: when a function is convex, “average first, then apply the function” produces something no larger than “apply the function first, then average.”

## Jensen’s inequality

Jensen’s inequality is the probability version of convexity:

$$
f(\mathbb{E}[X]) \le \mathbb{E}[f(X)]
$$

for convex $f$.

This is the same secant-line idea, except the averaging weights are now probabilities rather than deterministic mixing coefficients.

### What Jensen is really saying

Jensen compares two different procedures:

- compress the random variable to its average and then apply the function;
- apply the function to every outcome and then average.

For convex functions, the second procedure is never smaller.

This is why Jensen is not just a random inequality. It is the probabilistic form of “convex functions penalize spread.”

### Tiny explicit example

Let $f(x)=x^2$, and let $X$ take values $0$ and $2$ with probability $1/2$ each.

Then

$$
\mathbb{E}[X]=1,
\qquad
f(\mathbb{E}[X])=1.
$$

But

$$
\mathbb{E}[f(X)]
=
\frac12 f(0)+\frac12 f(2)
=
\frac12\cdot 0+\frac12\cdot 4
=
2.
$$

So indeed

$$
f(\mathbb{E}[X]) \le \mathbb{E}[f(X]).
$$

The inequality is strict because $x^2$ is strictly convex and $X$ is genuinely random rather than constant.

## Convexity and exponential families

Now return to the actual reason this section exists.

For a canonical exponential-family model,

$$
p_\theta(x)
=
h(x)\exp\!\bigl(\theta^\top\phi(x)-A(\theta)\bigr),
$$

the log-likelihood of i.i.d. data $x^{(1)},\dots,x^{(m)}$ is

$$
\ell(\theta)
=
\sum_{i=1}^{m}\log h(x^{(i)})
+
\theta^\top \sum_{i=1}^{m}\phi(x^{(i)})
-
mA(\theta).
$$

Therefore the negative log-likelihood is

$$
-\ell(\theta)
=
mA(\theta)
-
\theta^\top \sum_{i=1}^{m}\phi(x^{(i)})
-
\sum_{i=1}^{m}\log h(x^{(i)}).
$$

Now read the structure carefully:

- the last term is constant in $\theta$;
- the middle term is linear in $\theta$;
- all curvature comes from the log-partition function $A(\theta)$.

So if we understand the curvature of $A(\theta)$, we understand the curvature of the whole negative log-likelihood.

## Gradient and Hessian of the log-partition function

The log-partition function is special because its derivatives have probabilistic meaning.

For each component,

$$
\frac{\partial A(\theta)}{\partial \theta_j}
=
\mathbb{E}_\theta[\phi_j(X)].
$$

So the gradient of $A(\theta)$ gives model expectations of the sufficient statistics.

Differentiating again yields

$$
\frac{\partial^2 A(\theta)}{\partial \theta_j\partial \theta_k}
=
\mathrm{Cov}_\theta\!\bigl(\phi_j(X),\phi_k(X)\bigr).
$$

In matrix form,

$$
\nabla^2 A(\theta)=\mathrm{Cov}_\theta(\phi(X)).
$$

This is the key identity.

A covariance matrix is always positive semidefinite. Indeed, for any vector $v$,

$$
v^T\nabla^2 A(\theta)v
=
v^T\mathrm{Cov}_\theta(\phi(X))v
=
\mathrm{Var}_\theta\!\bigl(v^\top \phi(X)\bigr)
\ge 0.
$$

Variance can never be negative. Therefore the Hessian is positive semidefinite, so $A(\theta)$ is convex.

Since the negative log-likelihood differs from $mA(\theta)$ only by a linear term and a constant, it inherits that convexity.

## What this means for estimation

This is the real payoff.

In canonical exponential-family models, the negative log-likelihood often has clean global geometry because its curvature is controlled by a covariance matrix. Covariance matrices are positive semidefinite, so the objective cannot create arbitrary directions of negative curvature.

That does **not** mean every estimation problem is easy.

It means the landscape is structurally well behaved in a way that rules out many of the pathologies that make nonconvex optimization hard to interpret.

That is why convexity belongs here: it explains why some inference problems are not just computationally manageable, but also conceptually cleaner.

## Retain from 2.4

- A convex set contains the full line segment between any two of its points.
- A convex function lies below every secant line.
- The secant-line, tangent-plane, and Hessian characterizations are different views of the same property.
- Jensen’s inequality is the expectation version of convexity.
- In canonical exponential families, the Hessian of the log-partition function is a covariance matrix, which is why negative log-likelihoods often come out convex.

## Do not confuse in 2.4

- Do not confuse a convex **set** with a convex **function**.
- Do not confuse convexity with monotonicity.
- Do not confuse positive semidefinite with positive definite; flat directions can remain in the former case.
- Do not assume every optimization problem in statistics is convex just because many exponential-family examples are.

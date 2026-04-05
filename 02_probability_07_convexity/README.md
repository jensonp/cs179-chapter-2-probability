# 2.4 Convexity

This section is supporting background rather than core probability machinery, but that phrase can be misleading if it is read carelessly. “Supporting background” does **not** mean optional fluff. It means this section exists to explain why some of the optimization problems introduced in learning and parameter estimation are mathematically well behaved. The moment a chapter starts talking about maximizing likelihoods, minimizing negative log-likelihoods, or fitting models by solving optimization problems, the reader needs a way to reason about whether those objectives are globally safe or structurally dangerous. Convexity is one of the main tools for making that distinction.

So the real question of this section is not “what is a convex set?” in isolation. The real question is:

$$
\text{Why do some estimation objectives behave like clean bowls, while others behave like landscapes full of traps?}
$$

To answer that properly, the section must connect geometry, inequalities, and optimization.

There are four ideas to keep separate and then connect:

1. A **convex set** is a domain with no gaps along line segments.
2. A **convex function** bends upward in the global sense relevant for optimization.
3. **Jensen’s inequality** is the probabilistic form of that same geometric idea.
4. In canonical exponential-family models, the curvature of the negative log-likelihood is controlled by a covariance matrix, which is why convexity appears so naturally in statistical estimation.

The most important thing to remember from the start is this:

**Convexity matters because it lets local information control global conclusions.**

That is the link to learning.

---

## 1. Why convexity belongs in an inference chapter

Section 2.3 introduced objects such as likelihoods, posteriors, and model-comparison criteria. Many of those objects are used through optimization:

- maximize a likelihood,
- minimize a negative log-likelihood,
- maximize a posterior density,
- minimize a regularized objective,
- compare model classes through optimized criteria.

The danger is not merely computational cost. The deeper danger is structural ambiguity.

If an objective is nonconvex, then:
- local minima may not be globally optimal,
- different initializations may lead to different fitted parameters,
- and the inferential meaning of “the solution” becomes harder to interpret.

Convexity removes much of that ambiguity. For convex objectives, local optimality is enough to guarantee global optimality. For strictly convex objectives, the solution is often unique as well. That is why convexity is not just a side theorem. It is a structural guarantee about the geometry of the learning problem.

---

## 2. Convex sets

A set $S$ is **convex** if for any two points $x,x' \in S$ and any $\alpha \in [0,1]$, the convex combination

$$
\alpha x + (1-\alpha)x'
$$

also belongs to $S$.

This is the right place to slow down and interpret the definition.

- The points $x$ and $x'$ are two legal points in the domain.
- The number $\alpha$ chooses a weighted average between them.
- The condition says that every point on the line segment joining them must remain inside the set.

So a convex set contains the entire line segment between any two of its points.

### Why this matters

Convexity of functions is always defined relative to a domain. If the domain itself is not closed under line segments, then midpoint comparisons and tangent-line arguments break down globally. So convex sets are not a separate decorative notion. They are the natural stage on which convex functions live.

### Examples

- An interval on the real line is convex.
- A filled disk in the plane is convex.
- A triangle together with its interior is convex.
- A crescent, ring, or hollow shape is not convex, because some line segment between two allowed points leaves the set.

### What to notice

A convex set is a geometric feasibility condition. It says that averaging two allowed points does not push you outside the legal region.

That is exactly the kind of domain one wants in optimization, because moving partway from one feasible point toward another should not make the candidate invalid.

---

## 3. Convex functions

A function $f$ defined on a convex domain is **convex** if

$$
f\bigl(\alpha x + (1-\alpha)x'\bigr)
\le
\alpha f(x) + (1-\alpha)f(x')
$$

for all $x,x'$ in the domain and all $\alpha \in [0,1]$.

This inequality must be read in the right order.

1. First average the inputs.
2. Then evaluate the function at that averaged input.
3. Compare that with averaging the two function values.

Convexity says the function evaluated after averaging is never larger.

### What this means geometrically

The graph of a convex function lies below every secant line joining two points on the graph.

This is why people often describe convex functions as “bowl-shaped.” That picture is useful, but it is only a mnemonic. The real content is the global inequality above.

### What convexity does **not** mean

Convexity is not the same thing as monotonicity.

A convex function may increase everywhere, decrease everywhere, or decrease and then increase. The defining property is about curvature and global secant comparisons, not about whether the function slopes up or down.

### Strict convexity

A function is **strictly convex** if

$$
f\bigl(\alpha x + (1-\alpha)x'\bigr)
<
\alpha f(x) + (1-\alpha)f(x')
$$

whenever $x\neq x'$ and $0<\alpha<1$.

Strict convexity rules out flat line segments on the graph.

That distinction matters because:
- convexity is enough to make every local minimum global,
- strict convexity is what typically rules out multiple minimizers.

So strict convexity is the condition that upgrades clean geometry to uniqueness.

---

## 4. Three equivalent viewpoints

The secant-line definition is not the only way to recognize convexity. In smooth settings there are equivalent first-order and second-order tests, and these are often more useful in statistics and machine learning.

### 4.1 Secant-line view

A convex graph lies below every secant line joining two of its points.

This is the original definition in geometric language.

### 4.2 First-order view

If $f$ is differentiable, convexity is equivalent to

$$
f(x')
\ge
f(x) + \nabla f(x)\cdot(x'-x).
$$

This says the tangent line or tangent plane at $x$ is a global lower bound on the graph.

That is a remarkable fact. For a generic nonlinear function, a tangent approximation is only local. For a convex function, the tangent plane never overshoots the graph anywhere in the domain.

### Why this matters computationally

Optimization algorithms often use local information such as gradients. For general functions, local slope information can be misleading. For convex functions, that local information has genuine global meaning. The gradient is not just a local diagnostic. It is part of a global geometric structure.

### 4.3 Second-order view

If second derivatives exist, convexity is equivalent to

$$
\nabla^2 f(x)\succeq 0.
$$

That means the Hessian is positive semidefinite. Equivalently, for every vector $v$,

$$
v^T\nabla^2 f(x)\,v \ge 0.
$$

So every directional second derivative is nonnegative. There are no directions of negative curvature.

### Why this version matters most in statistics

Many statistical objectives come with natural Hessians. If that Hessian can be identified as positive semidefinite, convexity follows immediately. This is the version that later connects to covariance matrices in exponential-family models.

---

## 5. Positive semidefinite versus positive definite

This distinction should be explicit because it directly affects uniqueness.

If the Hessian is **positive semidefinite**, the function is convex, but flat directions may still exist.

If the Hessian is **positive definite**, then every nonzero direction curves upward strictly, and the function is locally bowl-shaped in every direction.

That difference translates into optimization as follows:

- positive semidefinite curvature gives convexity and therefore global optimality of local minima,
- positive definite curvature often gives a unique minimizer.

### Why flat directions matter

Flat directions are not just geometric curiosities. They often correspond to non-identifiability or redundant parametrizations. If moving in some direction changes the parameter without changing the objective, then the minimizer need not be unique even though the objective is convex.

So the PSD/PD distinction is really a distinction between “globally safe” and “globally safe plus unique.”

---

## 6. Why convexity matters for optimization

Now the main payoff can be stated cleanly.

If $f$ is convex, then every local minimum is a global minimum.

If $f$ is strictly convex, then there is at most one minimizer.

This is the true inferential value of convexity. It does **not** mean the problem is trivial, and it does **not** guarantee a closed-form solution. But it does mean the objective does not hide multiple qualitatively different local solutions in disconnected valleys.

That is why convexity is so prized. It aligns local search with global meaning.

---

## 7. Fully explicit example: $f(x)=x^2$

The function

$$
f(x)=x^2
$$

is the simplest exact example of convexity and is worth checking algebraically.

Take any $x,x'$ and $\alpha \in [0,1]$. Then

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

That is exactly the convexity inequality.

### What the extra term means

The correction term

$$
-\alpha(1-\alpha)(x-x')^2
$$

is the amount by which the parabola dips below the secant line. Because this term is nonpositive, the graph always lies below the secant line.

This example is worth keeping not because parabolas are deep, but because it makes the inequality concrete: convexity is secant-line geometry made algebraic.

---

## 8. Jensen’s inequality

Jensen’s inequality is the probabilistic form of convexity:

$$
f(\mathbb{E}[X]) \le \mathbb{E}[f(X)]
$$

for convex $f$.

This is not a random inequality appended to the section. It is the expectation version of the same secant-line idea.

### How to read Jensen properly

Jensen compares two different procedures:

- compress the random variable to its average and then apply the function;
- apply the function first to every outcome and then average.

For convex functions, the second quantity is never smaller.

### What Jensen is really saying

Convex functions penalize spread.

If the variable fluctuates, then applying a convex function before averaging exaggerates that spread relative to averaging first. This is why squared deviations, exponential penalties, and log-partition functions often appear in probabilistic inequalities and optimization arguments.

### Equality condition

If the function is strictly convex, equality holds only when the random variable is almost surely constant.

This is worth saying explicitly because it tells the reader what Jensen is detecting: real randomness plus real curvature creates a strict gap.

### Tiny example

Let $f(x)=x^2$ and let $X$ equal $0$ or $2$ with probability $1/2$ each.

Then

$$
\mathbb{E}[X]=1,
\qquad
f(\mathbb{E}[X])=1,
$$

while

$$
\mathbb{E}[f(X)]
=
\frac12 f(0)+\frac12 f(2)
=
\frac12\cdot 0+\frac12\cdot 4
=
2.
$$

So

$$
f(\mathbb{E}[X]) \le \mathbb{E}[f(X]).
$$

The inequality is strict because $x^2$ is strictly convex and $X$ is genuinely random.

---

## 9. Convexity and exponential families

Now return to the statistical reason this section exists.

For a canonical exponential-family model,

$$
p_\theta(x)
=
h(x)\exp\!\bigl(\theta^\top \phi(x) - A(\theta)\bigr),
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

Read the structure carefully:

- the last term is constant in $\theta$,
- the middle term is linear in $\theta$,
- all curvature comes from the log-partition function $A(\theta)$.

So if we understand the curvature of $A(\theta)$, we understand the curvature of the whole negative log-likelihood.

---

## 10. Gradient and Hessian of the log-partition function

The log-partition function is special because its derivatives have direct probabilistic meaning.

For each component,

$$
\frac{\partial A(\theta)}{\partial \theta_j}
=
\mathbb{E}_\theta[\phi_j(X)].
$$

So the gradient of $A(\theta)$ gives model expectations of the sufficient statistics.

Differentiating again gives

$$
\frac{\partial^2 A(\theta)}{\partial \theta_j\partial \theta_k}
=
\mathrm{Cov}_\theta\!\bigl(\phi_j(X),\phi_k(X)\bigr).
$$

In matrix form,

$$
\nabla^2 A(\theta)=\mathrm{Cov}_\theta(\phi(X)).
$$

This is the critical identity.

### Why this proves convexity

A covariance matrix is always positive semidefinite. For any vector $v$,

$$
v^\top \nabla^2 A(\theta) v
=
v^\top \mathrm{Cov}_\theta(\phi(X)) v
=
\mathrm{Var}_\theta\!\bigl(v^\top \phi(X)\bigr)
\ge 0.
$$

Variance can never be negative. Therefore the Hessian is positive semidefinite, so $A(\theta)$ is convex.

Since the negative log-likelihood differs from $mA(\theta)$ only by a linear term and a constant, it inherits that convexity.

This is not merely a formal trick. It says the curvature of the estimation objective is controlled by a covariance structure.

---

## 11. Worked estimation example: Bernoulli in canonical form

A full example makes the abstract argument easier to trust.

Let $X\in\{0,1\}$ and write the Bernoulli model in canonical exponential-family form using natural parameter

$$
\theta = \log\!\frac{\rho}{1-\rho}.
$$

Then the model can be written as

$$
p_\theta(x)=\exp\!\bigl(x\theta - A(\theta)\bigr),
$$

where

$$
A(\theta)=\log(1+e^\theta).
$$

The sufficient statistic is simply $\phi(x)=x$.

For i.i.d. data $x^{(1)},\dots,x^{(m)}$, the negative log-likelihood is

$$
-\ell(\theta)
=
mA(\theta)-\theta\sum_{i=1}^{m}x^{(i)}.
$$

The derivative is

$$
\frac{d}{d\theta}[-\ell(\theta)]
=
mA'(\theta)-\sum_{i=1}^{m}x^{(i)}.
$$

Since

$$
A'(\theta)=\frac{e^\theta}{1+e^\theta}=\rho,
$$

the first derivative becomes

$$
m\rho-\sum_{i=1}^{m}x^{(i)}.
$$

The second derivative is

$$
\frac{d^2}{d\theta^2}[-\ell(\theta)]
=
mA''(\theta).
$$

And

$$
A''(\theta)
=
\frac{e^\theta}{(1+e^\theta)^2}
=
\rho(1-\rho)\ge 0.
$$

Therefore

$$
\frac{d^2}{d\theta^2}[-\ell(\theta)]\ge 0.
$$

So the objective is convex.

### What this example teaches

This example shows the whole logic in one place:

- express the model in canonical exponential-family form,
- identify the log-partition function,
- differentiate,
- observe that the second derivative is a variance term,
- conclude convexity.

This is the pattern, not just the Bernoulli case.

---

## 12. What convexity does **not** give you

A mastery note should say what a theorem does **not** promise.

Convexity does **not** imply:
- closed-form solvability,
- easy algebra,
- fast computation in every dimension,
- or that every statistical objective is convex.

Convexity gives structural safety, not magic. A convex problem may still be large, constrained, numerically delicate, or require iterative algorithms. What convexity removes is the ambiguity of bad local minima and many disconnected solution basins.

That is already a huge gain.

---

## 13. How this connects to later material

Convexity matters later for several reasons.

- In learning, many standard objectives are written as negative log-likelihoods or regularized variants.
- In information theory, log-partition functions and KL-related objectives inherit curvature properties that matter for optimization.
- In machine learning, cross-entropy losses, generalized linear models, and some variational objectives depend heavily on convex or nearly convex structure.
- In statistics, uniqueness and stability of estimators often rest on curvature conditions.

So even though this section is “background” in one sense, it is part of the structural backbone of the chapter.

---

## 14. Retain from 2.4

- Convexity is what lets local optimality imply global optimality.
- A convex set contains the full line segment between any two of its points.
- A convex function lies below every secant line.
- The secant-line, tangent-plane, and Hessian viewpoints are equivalent characterizations of the same structure.
- Jensen’s inequality is the expectation form of convexity.
- In canonical exponential families, the Hessian of the log-partition function is a covariance matrix, which is why negative log-likelihoods often come out convex.

## 15. Do not confuse in 2.4

- Do not confuse a convex **set** with a convex **function**.
- Do not confuse convexity with monotonicity.
- Do not confuse positive semidefinite with positive definite.
- Do not assume every objective used in statistics or machine learning is convex.
- Do not think convexity guarantees a closed-form solution; it guarantees a globally coherent geometry.

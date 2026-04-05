# 2.4 Convexity

This section is supporting background rather than core probability machinery.  
Its purpose is to explain why some estimation objectives are well behaved and why optimization in exponential-family models often has a clean global structure.

The point of the section is not to turn convex analysis into a separate topic.  
It is to answer one practical question from Section 2.3:

$$
\text{“Why do some likelihood-based objectives have no bad local minima?”}
$$

## Convex sets

A set $S$ is **convex** if for any two points $x,x' \in S$ and any mixing weight $\alpha \in [0,1]$, the convex combination

$$
\alpha x + (1-\alpha)x'
$$

also lies in $S$.

So a convex set contains the entire line segment between any two of its points.

This condition matters because convexity of a function is only defined on a domain where those line segments stay inside the domain.

## Convex functions

A function $f$ defined on a convex domain is **convex** if

$$
f\bigl(\alpha x + (1-\alpha)x'\bigr)
\le
\alpha f(x) + (1-\alpha)f(x')
$$

for all $x,x'$ in the domain and all $\alpha \in [0,1]$.

Read the comparison carefully:

- first average the inputs and then evaluate the function;
- then compare that with averaging the function values.

Convexity says the function value after averaging the inputs is never larger.

A function is **strictly convex** if the inequality is strict whenever $x \ne x'$ and $0 < \alpha < 1$:

$$
f\bigl(\alpha x + (1-\alpha)x'\bigr)
<
\alpha f(x) + (1-\alpha)f(x').
$$

That rules out flat line segments on the graph.

## Equivalent viewpoints

Three equivalent viewpoints are worth keeping together.

### 1. Secant-line view

A convex graph lies below every secant line joining two of its points.

### 2. First-order view

If $f$ is differentiable, convexity is equivalent to

$$
f(x')
\ge
f(x) + \nabla f(x)\cdot(x'-x).
$$

This says the tangent line or tangent plane at $x$ lies below the graph everywhere else.

### 3. Second-order view

If second derivatives exist, convexity is equivalent to

$$
\nabla^2 f(x) \succeq 0.
$$

That means the Hessian is positive semidefinite: for every vector $v$,

$$
v^T \nabla^2 f(x)\,v \ge 0.
$$

So every directional second derivative is nonnegative.  
There are no directions of negative curvature.

## Why convexity matters for optimization

Convexity matters because it gives a global guarantee:

- every local minimum of a convex function is global;
- a strictly convex function has a unique minimizer.

Positive semidefinite curvature still allows flat directions, so multiple minimizers can remain.  
Positive definite curvature removes those flat directions and forces uniqueness.

This is the exact optimization-side payoff.  
Convexity does not mean the problem is trivial, but it does mean the objective does not hide extra local minima away from the global one.

## Example: $f(x)=x^2$

A fully explicit algebraic example is

$$
f(x)=x^2.
$$

For any $x,x'$ and $\alpha \in [0,1]$,

$$
f\bigl(\alpha x + (1-\alpha)x'\bigr) = (\alpha x + (1-\alpha)x')^2.
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

That is the convexity inequality in exact algebraic form.

The correction term

$$
-\alpha(1-\alpha)(x-x')^2
$$

is what pushes the parabola below the secant line.

## Jensen’s inequality

Jensen’s inequality is the probability version of convexity:

$$
\mathbb{E}[f(X)] \ge f(\mathbb{E}[X])
$$

for convex $f$.

This is the same idea with probability weights instead of deterministic weights.  
If $X$ takes values $x_1,\dots,x_k$ with probabilities $p_1,\dots,p_k$, then

$$
\mathbb{E}[X]=\sum_i p_i x_i,
\qquad
\mathbb{E}[f(X)]=\sum_i p_i f(x_i).
$$

So Jensen compares:

- the function of the average,
- with the average of the function.

For convex functions, averaging before applying $f$ gives a smaller result.

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
\mathbb{E}[f(X)] = \frac{1}{2}f(0)+\frac{1}{2}f(2) = 2.
$$

So indeed

$$
\mathbb{E}[f(X)] \ge f(\mathbb{E}[X]).
$$

## Convexity and exponential families

Now connect the abstract definitions back to estimation.

For a canonical exponential-family model,

$$
p_\theta(x)=h(x)\exp\!\bigl(\theta^\top \phi(x) - A(\theta)\bigr),
$$

the log-likelihood of i.i.d. data $x^{(1)},\dots,x^{(m)}$ is

$$
\ell(\theta)=\sum_{i=1}^{m}\log h(x^{(i)}) + \theta^\top \sum_{i=1}^{m}\phi(x^{(i)}) - mA(\theta).
$$

Therefore the negative log-likelihood is

$$
-\ell(\theta)=mA(\theta) - \theta^\top \sum_{i=1}^{m}\phi(x^{(i)}) - \sum_{i=1}^{m}\log h(x^{(i)}).
$$

The last term is constant in $\theta$.  
The middle term is linear in $\theta$.  
So all curvature comes from the log-partition function $A(\theta)$.

### Gradient and Hessian of the log-partition function

Differentiating $A(\theta)$ gives

$$
\frac{\partial A(\theta)}{\partial \theta_j} = \mathbb{E}_\theta[\phi_j(X)].
$$

Differentiating again gives

$$
\frac{\partial^2 A(\theta)}{\partial \theta_j \partial \theta_k} = \mathrm{Cov}_\theta\!\bigl(\phi_j(X),\phi_k(X)\bigr).
$$

In matrix form,

$$
\nabla^2 A(\theta)=\mathrm{Cov}_\theta(\phi(X)).
$$

Now apply the positive-semidefinite test.  
For any vector $v$,

$$
v^\top \nabla^2 A(\theta) v = v^\top \mathrm{Cov}_\theta(\phi(X)) v = \mathrm{Var}_\theta\!\bigl(v^\top \phi(X)\bigr) \ge 0.
$$

Variance is never negative, so the Hessian is positive semidefinite.  
Therefore $A(\theta)$ is convex.

Since the negative log-likelihood differs from $mA(\theta)$ only by a linear term and a constant, it inherits that convexity.

## What this means for estimation

This is the real takeaway.

In canonical exponential-family models, the negative log-likelihood often has clean global geometry because its curvature is controlled by a covariance matrix.  
Covariance matrices are positive semidefinite, so the objective cannot generate arbitrary nonconvex behavior.

That does **not** mean every estimation problem is easy.  
It means the optimization landscape is structurally well behaved.

## Retain from 2.4

- Convexity is what makes some estimation objectives globally well behaved.
- The secant-line, tangent-plane, and Hessian characterizations are three views of the same property.
- Jensen’s inequality is the expectation form of convexity.
- In exponential families, the Hessian of the log-partition function is a covariance matrix, which is why negative log-likelihoods often come out convex.

## Do not confuse in 2.4

- Do not confuse a convex **set** with a convex **function**.
- Do not assume every likelihood problem is convex just because many exponential-family examples are.
- Do not confuse positive semidefinite with positive definite; flat directions can remain in the former case.

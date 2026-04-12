# 2.6 Change-of-Variable Models

Change-of-variable modeling appears when a random quantity is easier to describe in one space than in another. Sometimes the observed variable is constrained, such as being always positive. Sometimes the observed distribution is strongly skewed, even though a transformed version looks regular. Sometimes dependence becomes easier to describe only after the coordinates are remapped. So this chapter is not mainly about a calculus trick. It is about a modeling strategy: begin with a variable whose distribution is easy to understand, transform it into the variable we actually care about, and then describe the resulting distribution correctly.

The central law behind the whole chapter is **probability conservation**. A deterministic transformation can move probability mass from one region of the line or space to another. It can stretch some neighborhoods and compress others. But it cannot create or destroy total probability. That is why transformed-density formulas always contain some local scaling factor. In one dimension that factor is an absolute derivative. In several dimensions it becomes an absolute determinant. These terms are not decorative corrections attached after the main idea. They are the mathematical expression of probability conservation under a change of coordinates.

Before any formula appears, it helps to separate the objects involved.

There is first the **base variable**, often written $Z$. This is the variable whose distribution we already know, or choose deliberately because it is simple.

There is next the **transformed variable**, often written $X$, defined by a deterministic map such as $X = f(Z)$. The transformation acts on the variable itself. It does not act directly on the density formula.

There is also the **support** of each variable. The support is the set of values the variable can actually take. Transformations often change support, and many algebraically tidy answers are wrong because they ignore that change.

Finally, there are **events**. A probability statement about $X$, such as $a \le X \le b$, can often be understood most easily by translating it back into an equivalent statement about $Z$.

That object separation is worth taking seriously, because most confusion in this topic comes from mixing these roles together. A good working discipline is this: start with the base variable and its known distribution; define the transformed variable by an explicit map; identify the transformed support; translate events in observed space back to the base space; and only then write the transformed density formula.

## Why transformations appear in probabilistic modeling

This topic has to appear once densities have been introduced, because a density by itself only describes a distribution in one coordinate system. It does not tell us automatically what happens if the variable is re-expressed.

Earlier chapters focused on describing random variables once the space and coordinates were fixed. But probabilistic modeling immediately asks a harder question. What if the quantity we observe is defined indirectly from another variable? What if we choose a different representation because it makes the model simpler? What if we want to start from a simple distribution and generate a more complicated one through transformation? At that point the question is no longer "what is the density of this variable?" It becomes "how does a density change when the variable itself is remapped?"

The wrong instinct is to think that we should simply substitute the transformation into the old density. That is not the right operation. The transformation changes not only where probability mass sits, but also how densely that mass is packed in the new coordinates. That is why the inverse map appears, and that is why the local scaling factor is unavoidable.

This idea matters later for at least three reasons. First, it explains transformed families such as the lognormal, where a simple latent variable produces a positively supported and skewed observed variable. Second, it supports constructions such as copulas, where variables are moved into percentile space so that marginal behavior and dependence can be separated. All of these reuse the same law. What changes is only the complexity of the transformation and the modeling goal.

## Scalar change of variables

The one-dimensional case is the right place to understand the mechanism before the notation becomes heavier.

Let $Z$ be a scalar random variable with known density $p_Z$, and let
$$
X = f(Z).
$$
We are trying to answer one specific question:

**What is the density of $X$?**

To answer that question cleanly, it helps to say exactly what is fixed and what is varying. The transformation $f$ is fixed. The base density $p_Z$ is fixed. The transformed variable $X$ is already defined by that map. What varies is the observed location $x$ where we want to evaluate the density of $X$.

That point matters because it prevents a common misunderstanding. We are not trying to "transform the graph of $p_Z$." We are asking a local question: if we look near one observed point $x$, which latent point or latent points in $Z$-space could have produced it, and how did the map change local width near those points?

That is the core mechanism of the scalar case. First identify the latent source of the observed point. Then correct for local stretching or compression. The inverse map appears because we must work backward from $x$ to the latent location that generated it. The derivative appears because density is measured per unit width, and the transformation changes local width.

### The object being introduced

The scalar change-of-variables rule is a rule for computing the density of a transformed random variable. The setup is simple but important: the base density $p_Z$ is already known, the transformation $f$ is already chosen, and the transformed variable is defined by $X = f(Z)$. The unknown object is the density $p_X$.

What varies in the rule is the observed point $x$. For each legal value of $x$, we want to know how much probability mass is concentrated near that point. In a transformed model, that concentration depends on two ingredients together. One ingredient is the latent point that maps to $x$. The other is the local scaling behavior of the transformation. Those two ingredients are exactly what the inverse and the derivative will encode.

### Formal definition: monotone invertible case

Suppose $f$ is differentiable and invertible on the support region being used, with inverse

$$
g = f^{-1}.
$$

Then the density of $X$ is

$$
p_X(x) = p_Z(g(x))\,|g'(x)|,
$$

for those $x$ that lie in the transformed support.

### Interpretation

This formula says two things, in this order.

First, to know the density at $x$, you must ask which latent point $z$ produced that $x$. That is why the inverse appears. The relevant latent point is not $f(x)$ but $g(x)$.

Second, once that latent point is found, the density must be corrected by a local width-conversion factor. If a short interval in $X$-space corresponds to a narrower interval in $Z$-space, then the density in $X$-space must be higher, because the same probability mass is now packed into less width. If the interval becomes wider, the density must be lower. The factor $|g'(x)|$ is exactly that local width ratio.

### Why the inverse appears

The inverse appears because the density at an observed point $x$ depends on the latent point that produced it. The forward map tells us how to move from latent space to observed space. But when we evaluate the transformed density at a particular observed point, we must work backward. We must ask: which value of $z$ satisfies $f(z) = x$? That is an inverse question.

The cleanest way to see this is to begin with an event rather than with a density formula. Suppose first that $f$ is increasing. Then the event $X \le x$ means exactly the same thing as the event $f(Z) \le x$, which in turn means $Z \le g(x)$ where $g = f^{-1}$. So

$$
F_X(x) = \mathbb{P}(X \le x) = \mathbb{P}(f(Z) \le x) = \mathbb{P}(Z \le g(x)) = F_Z(g(x)).
$$

Each equality has a job. The first merely rewrites $X$ as $f(Z)$. The second uses monotonicity to move from a statement about $f(Z)$ back to a statement about $Z$. The third says that once the event is written in terms of $Z$, the base CDF can evaluate it directly.

Only after that translation is complete do we differentiate with respect to $x$, giving

$$
p_X(x) = p_Z(g(x))\,g'(x).
$$

If $f$ is decreasing, the same event logic still works, but orientation reverses and the derivative becomes negative. Density cannot be negative, so the absolute value restores the correct local scaling factor. The lesson to retain is not merely that an inverse appears in the formula. The lesson is that transformed-variable questions are often easiest because they can be translated back into the variable whose distribution we already understand.

### Why the derivative appears

The derivative appears because density is measured per unit width. A transformation changes local width.

Suppose a tiny interval around $x$ has width $dx$. Under the inverse map, it corresponds to a tiny interval around $z = g(x)$ whose width is approximately

$$
|g'(x)|\,dx.
$$

Those two intervals carry the same probability mass, because they represent the same event described in different coordinates. So

$$
p_X(x)\,dx \approx p_Z(g(x))\,|g'(x)|\,dx,
$$

which gives the formula.

This is the right interpretation to retain. The derivative is not there because differentiation happened to appear in the derivation. It is there because local width changed.

### Boundary conditions and failure modes

The standard one-branch scalar formula has hidden assumptions, and students often use it outside its legal range.

The map must be invertible on the region of support being used. Global differentiability alone is not enough. If several distinct latent points map to the same observed point, then the single-inverse formula is incomplete.

The transformed support must also be checked explicitly. The formula can only be evaluated where the inverse point actually belongs to the support of the base variable. Ignoring support is one of the fastest ways to produce a density that looks algebraically plausible but is wrong.

Finally, the absolute value must not be dropped. A negative derivative indicates reversal of orientation, not negative probability.

## Case A: monotone invertible map

When $f$ is monotone and invertible on the relevant support region, the formula above applies directly. This is the clean case, and it should be mastered before moving to more complicated mappings.

### Worked example: scaling a uniform variable

This example is chosen because it exposes the entire mechanism without any distracting algebra.

Let

$$
Z \sim \mathrm{Unif}[0,1], \qquad X = 2Z.
$$

We identify the ingredients in order.

The map is $f(z) = 2z$. The inverse is

$$
g(x) = x/2,
$$

and its derivative is

$$
g'(x) = 1/2.
$$

Now evaluate the formula:

$$
p_X(x) = p_Z(x/2)\cdot \frac{1}{2}.
$$

At this point, the support check matters. The base density $p_Z(z)$ equals $1$ only when $z \in [0,1]$. So we must ask when $x/2 \in [0,1]$. That condition is

$$
0 \le x/2 \le 1
\quad \Longleftrightarrow \quad
0 \le x \le 2.
$$

Therefore

$$
p_X(x) = \frac{1}{2} \qquad \text{for } 0 \le x \le 2,
$$

and $p_X(x)=0$ elsewhere.

What was checked here, and why did each check matter?

First, we found the inverse because the density at $x$ depends on the latent point that generated it. Second, we computed the derivative because density must be corrected for local width change. Third, we checked the transformed support because the base density is only valid on $[0,1]$. The final answer makes the conservation law visible: the interval length doubled, the density height halved, and total probability stayed equal to one.

### Worked example: why the absolute value is necessary

This example is chosen because it isolates a narrow but important point: sign changes in derivatives do not correspond to negative density.

Let

$$
Z \sim \mathrm{Unif}[0,1], \qquad X = 1 - Z.
$$

Then

$$
g(x) = 1-x, \qquad g'(x) = -1.
$$

So the formula gives

$$
p_X(x) = p_Z(1-x)\,|-1| = p_Z(1-x).
$$

Now check the support: $1-x \in [0,1]$ exactly when $x \in [0,1]$. Hence

$$
p_X(x)=1 \qquad \text{for } x \in [0,1],
$$

and zero elsewhere.

The general lesson is that a negative derivative means the ordering of points has reversed, not that probability has become negative. That is why the Jacobian factor uses absolute value.

### Misconception block

Do not confuse “apply the function to the variable” with “apply the function to the density.”

If $X = f(Z)$, the transformed density is **not** obtained by replacing $z$ with $f(z)$ inside $p_Z$. The correct procedure is: identify which latent point maps to the observed point, then correct for local stretching or compression. The inverse map and the Jacobian are not optional clean-up steps. They are the whole content of the rule.

## Case B: non-monotone or multi-branch map

Now we can state the most important failure mode of the one-branch scalar rule.

In the monotone invertible case, each observed point $x$ comes from exactly one latent point $z$. That is why the density formula has one inverse point and one local scaling factor. But this structure can fail. A transformation may be smooth and perfectly well defined while still sending several different latent points to the same observed location.

When that happens, the density at $x$ cannot be computed from only one inverse point, because there is no longer only one latent neighborhood contributing probability mass near $x$. Several separated neighborhoods in latent space may all land near the same observed point. The correct density must account for **all** of them.

This is the key conceptual change. The law of probability conservation has not changed. What has changed is the geometry of the map. The observed point $x$ is now fed by several latent sources rather than one. So the transformed density must be built by adding the probability contributions from each legal inverse branch.

It is important to notice what did **not** go wrong. The one-branch formula did not fail because of algebra. It failed because its hidden assumption, one observed point and one latent source, no longer matches the transformation being used.

### Formal rule for the multi-branch case

If the equation $f(z)=x$ has several legal solutions on the relevant support, say
$$
z_1(x), \dots, z_k(x),
$$
then each of those branches contributes probability mass to the observed density at $x$. The correct transformed density is therefore
$$
p_X(x) = \sum_{i=1}^k p_Z(z_i(x))\left|\frac{dz_i}{dx}\right|.
$$

This formula should be read term by term. For each branch, locate the latent point $z_i(x)$ that maps to the observed point $x$. Evaluate the base density there. Then correct that branch's contribution by the local width-conversion factor attached to that inverse branch. After that, add the contributions across all legal branches. The sum appears because all of those latent neighborhoods contribute to the same observed neighborhood.

This is not a different law from the one-branch case. It is the same conservation principle, but now more than one latent region feeds the same observed location.

### Worked example: squaring a symmetric variable

This example is chosen because it makes the failure of the one-branch formula impossible to ignore.

Let

$$
Z \sim \mathrm{Unif}[-1,1], \qquad X = Z^2.
$$

We first identify the support of $X$. Because $Z^2$ ranges from $0$ to $1$, the support is $x \in [0,1]$.

Now solve the inverse relation. For a fixed $x$ in $(0,1]$, the equation $z^2 = x$ has two solutions:

$$
z_1(x) = \sqrt{x}, \qquad z_2(x) = -\sqrt{x}.
$$

Each branch has derivative magnitude

$$
\left|\frac{dz_i}{dx}\right| = \frac{1}{2\sqrt{x}}.
$$

The base density of $Z$ is $1/2$ on $[-1,1]$. Therefore each branch contributes

$$
\frac{1}{2}\cdot\frac{1}{2\sqrt{x}} = \frac{1}{4\sqrt{x}}.
$$

Since there are two branches, the total density is

$$
p_X(x) = \frac{1}{2\sqrt{x}} \qquad \text{for } 0 < x \le 1,
$$

and zero elsewhere.

The reason this example matters is not just the final formula. It teaches the general signature of a multi-branch problem. First, the transformation is not one-to-one on the relevant support. Second, the inverse relation produces more than one legal latent solution. Third, each legal branch contributes its own Jacobian-scaled piece of probability mass. Fourth, the total observed density is the sum of those contributions.

That pattern is the one to look for in future problems. Whenever a transformation folds the line, reflects part of it, or otherwise causes distinct latent values to land at the same observed point, you should expect a branch decomposition rather than a single inverse formula.

## Example: lognormal distribution

The lognormal is the first transformed family worth remembering because it shows how a familiar base distribution can generate a qualitatively different observed shape.

Let

$$
Z \sim \mathcal{N}(\mu,\sigma^2), \qquad X = e^Z.
$$

We identify the pieces carefully.

The map is increasing and invertible on all real numbers. The transformed support is

$$
x > 0,
$$

because exponentials are always positive. The inverse is

$$
z = \log x,
$$

and the inverse derivative is

$$
\frac{dz}{dx} = \frac{1}{x}.
$$

Now plug these into the scalar formula:

$$
p_X(x)
= p_Z(\log x)\cdot \frac{1}{x}
= \frac{1}{x\sqrt{2\pi\sigma^2}}
  \exp\!\left(-\frac{(\log x - \mu)^2}{2\sigma^2}\right),
\qquad x>0.
$$

The factor $1/x$ is not cosmetic. It is the Jacobian correction required because equal additive steps in $Z$ become unequal multiplicative steps in $X$.

### Why the lognormal is skewed

The skewness is best understood geometrically. Equal distances in $Z$ do not become equal distances in $X$.

Moving from $Z=0$ to $Z=1$ sends $X$ from $1$ to $e$. Moving from $Z=1$ to $Z=2$ sends $X$ from $e$ to $e^2$. The right side is stretched more aggressively than the left. So probability mass that was symmetrically arranged in Gaussian space becomes asymmetrically spread in observed space, creating the long right tail.

### Event translation lesson

A transformed-variable probability is often easiest to compute by moving the event back to the base space. For example, if $Z \sim \mathcal{N}(0,1)$ and $X=e^Z$, then

$$
\mathbb{P}(1 \le X \le e)
= \mathbb{P}(0 \le Z \le 1).
$$

This is a small calculation, but it teaches a large habit: transformed-variable events are often conceptually simpler than transformed-variable densities.

### Retain / Do not confuse for the scalar case

Retain the following.

A transformed density is determined by three things together: the inverse map, the Jacobian correction, and the transformed support. None of the three can be skipped.

Do not confuse monotonicity with differentiability. A smooth map can still fail to be globally invertible. Do not confuse a negative derivative with negative density. And do not use the one-branch formula in a multi-branch situation.



Up to this point, the local scaling question has been one-dimensional. A tiny neighborhood around an observed point had only one geometric feature to track: its width. That is why a single derivative was enough.

In several dimensions, the underlying law does not change, but the geometry becomes richer. A small neighborhood is no longer just an interval. It is a little rectangle, box, or higher-dimensional volume element. Under the inverse map, that neighborhood can be stretched, compressed, reflected, tilted, or sheared. So the question is no longer "how does local width change?" It becomes "how does local area or volume change?"

That is exactly why the determinant appears in the multivariate rule. It plays the same conceptual role the absolute derivative played in one dimension. It is the local scaling factor required by probability conservation, but now for area or volume rather than width.

So the correct way to experience the next section is not as a new law, but as the same law with more geometric bookkeeping.

## Multivariate change of variables

In several dimensions, the idea is unchanged but the bookkeeping becomes geometric rather than one-dimensional.

Let
$$
X = f(Z),
$$
where $Z$ and $X$ are now vectors, and suppose the map is invertible on the region of interest with inverse
$$
g = f^{-1}.
$$

### The object being introduced

The new object is the **Jacobian matrix of the inverse map**.

In one dimension, the inverse derivative tells us how local length changes. In several dimensions, a local neighborhood can change in more than one way at once. Different coordinates can stretch by different amounts, coordinates can interact, and a small square can become a slanted parallelogram or a small box can become a tilted volume element.

The Jacobian matrix records that local coordinate behavior. Its entries tell us how the components of the inverse map respond to changes in the observed coordinates. So the matrix is a local linear description of how the inverse transformation behaves near one observed point.

But the matrix itself is not yet the correction factor in the density formula. The density needs a single number that tells us how local volume changes. That number is the absolute value of the determinant of the Jacobian matrix.

So the multivariate question is the direct geometric upgrade of the scalar one: if we take a tiny observed neighborhood around $x$ and map it back into latent space, by what factor does its local volume change? That factor is what must multiply the base density evaluated at the inverse point.

### Formal definition

The density transformation rule is

$$
p_X(x) = p_Z(g(x))\,\bigl|\det J_g(x)\bigr|,
$$

where the Jacobian matrix of the inverse map is

$$
\bigl(J_g(x)\bigr)_{ij} = \frac{\partial g_i}{\partial x_j}.
$$

### Interpretation

The multivariate rule should be read in the same order as the scalar rule.

Start with an observed point $x$. Ask which latent point produced it. That is the inverse point $g(x)$. Evaluate the base density at that latent location, because that is where the relevant probability mass comes from.

Then apply the geometric correction. Imagine a tiny observed neighborhood around $x$. Under the inverse map, that neighborhood becomes a small region in latent space. The absolute determinant
$$
|\det J_g(x)|
$$
tells us, to first order, how much the local area or volume of that neighborhood changes under the inverse map.

If the inverse map makes the preimage region larger, then the observed density must be adjusted accordingly. If it makes the preimage region smaller, the correction goes in the other direction. The determinant therefore plays exactly the same role as $|g'(x)|$ did in one dimension. It is not a new principle. It is the same conservation law expressed in higher-dimensional geometry.

A negative determinant still does **not** mean negative probability. It only indicates orientation reversal, such as a reflection. Density uses the absolute value because the correction factor is about local volume, not orientation.

### Worked example: anisotropic scaling

This example is chosen because it is the cleanest multivariate analogue of the uniform-scaling example from the scalar case.

Let

$$
X_1 = 2Z_1,
\qquad
X_2 = 3Z_2.
$$

Then the inverse map is

$$
Z_1 = X_1/2,
\qquad
Z_2 = X_2/3.
$$

So the inverse Jacobian matrix is

$$
J_g(x) =
\begin{pmatrix}
1/2 & 0 \\
0 & 1/3
\end{pmatrix},
$$

and therefore

$$
\det J_g(x) = \frac{1}{6}.
$$

What does this mean? A small area element in observed space maps back to an area element in latent space that is six times smaller. Equivalently, the forward map expands area by a factor of six. So the density in observed space must be reduced by a factor of six to preserve total probability.

This is the same law as before, only now the conservation statement is about area rather than interval length.

### Misconception block

Do not think of the determinant as a purely algebraic side term. Its role is geometric and unavoidable.

Also do not confuse the Jacobian of the forward map with the Jacobian of the inverse map. Both formulations can be written, but they must be used consistently. In this section the formula is written in terms of the inverse map because it aligns directly with the scalar formula and with the question “which latent point produced this observed point?”

### Retain / Do not confuse for the multivariate case

Retain the structural analogy.

Derivative in one dimension means local width change. Determinant in several dimensions means local volume change. The principle is the same.

Do not confuse “density gets larger” with “more total probability was created.” A higher density may simply mean the same probability mass has been packed into a smaller local region.



The core change-of-variable law is complete at this point. The remaining sections are optional extensions that show how the same principle can be used in richer modeling settings. If the scalar and multivariate rules are not yet stable, it is reasonable to stop here and return later. If they are stable, the next sections show how the same transformation logic can be used not just to compute densities, but to redesign a modeling problem into a more convenient coordinate system.

## Optional enrichment: copula models

Copulas belong in this chapter because they reuse the same deep idea: sometimes a probabilistic problem becomes easier after a carefully chosen change of representation. Here the representation change is not introduced to produce a new marginal family such as the lognormal. It is introduced to separate two modeling questions that are easy to mix together in raw coordinates.

One question is: what does each variable look like by itself? That is a marginal-shape question. Another question is: how do the variables move together? That is a dependence question. In the original coordinates, those two questions are often entangled. A variable may look skewed, heavy-tailed, or differently scaled from another variable, and that can make dependence hard to describe cleanly.

The copula idea is to move each coordinate into **percentile space**. For a variable $X_i$ with continuous CDF $F_i$, define $U_i = F_i(X_i)$. The new variable $U_i$ records where $X_i$ sits in its own marginal distribution, not in its original physical units. After this transformation, each marginal becomes uniform on $[0,1]$, so the original marginal shapes have been factored out. What remains to model is how the percentile coordinates depend on one another.

### Why this matters

The transformation to $U_i$ removes the original units and marginal shape. Once each coordinate is converted into percentile space, what remains is dependence structure. That is the conceptual payoff of a copula: it is a joint distribution on percentile coordinates, so it describes how variables move together after the marginal behavior has been stripped away.

For two variables, the copula is defined by

$$
C(u_1,u_2) = \mathbb{P}(U_1 \le u_1, U_2 \le u_2).
$$

Equivalently,

$$
\mathbb{P}(X_1 \le x_1, X_2 \le x_2)
= C\bigl(F_1(x_1), F_2(x_2)\bigr).
$$

This equation should be read carefully. The marginal CDFs convert the original variables into percentile coordinates, and the copula then gives the joint CDF in that transformed space.

### Gaussian copula pipeline

A standard way to use a copula is to proceed in stages. First, each marginal distribution is estimated or specified in its own coordinates. Then each observed coordinate is moved into percentile space by applying its marginal CDF. At that point every coordinate lives on $[0,1]$, so the original units and marginal shape have been stripped away.

Sometimes the model then performs one more transformation, sending percentile coordinates into Gaussian latent coordinates through $\Phi^{-1}$. This step is not magic. It is another change of variables, chosen because Gaussian dependence is often easier to parameterize and reason about. Once the dependence has been modeled in that transformed space, the construction can be mapped back to the original coordinates.

The large lesson is not the pipeline itself. It is that a hard joint model can become easier once marginal behavior and dependence are separated by a representation change.

### Misconception block

Do not confuse a copula with a marginal distribution, and do not confuse dependence in raw units with dependence in percentile space. A copula does not tell you what each variable looks like by itself. It tells you how the coordinates are coupled once the marginals have been factored out.



## Optional enrichment: normalizing flows

Normalizing flows are best understood as a learned, model-building use of the exact same change-of-variable rule developed earlier in this chapter. The underlying probability law has not changed. We still begin with a base variable $Z$ whose density is simple and known. We still transform it into an observed variable $X$. And we still compute the resulting density by evaluating the base density at the inverse point and correcting by a Jacobian term.

What changes is the modeling goal. In the earlier examples, the transformation was chosen by hand and then analyzed. In a normalizing flow, the transformation itself is parameterized and learned from data. The point of the construction is to keep the density exactly computable while giving the model enough flexibility to represent complicated observed distributions.

So a flow is not "some new density trick after change of variables." It is a direct application of the same law, but with a learned invertible transformation instead of a fixed hand-designed one.

### Why flows are built from layers

In practice, flows are written as compositions

$$
f = f_T \circ \cdots \circ f_1.
$$

This factorization matters because Jacobian determinants multiply under composition, so log-determinants add. That makes density evaluation computationally manageable.

But the structure comes with strict constraints. Each layer must remain invertible, and its Jacobian determinant must be cheap enough to compute. Those are not implementation details. They are the price of retaining an exact density under transformation.

### Conceptual payoff

A normalizing flow should be viewed as a learned sequence of legal change-of-variable steps. Each step moves probability mass, stretches or compresses space, and updates the density by the corresponding Jacobian factor. So the conceptual content of flows is already contained in this section. The machine-learning application changes the scale, not the principle.

## Retain from 2.6

Retain the structural core.

A change-of-variable model is built from a known base distribution, an explicit transformation, a support map, and a Jacobian correction. The density changes because local width or volume changes, while total probability is conserved.

In one dimension, the correction is the absolute derivative of the inverse map. In several dimensions, it is the absolute determinant of the inverse Jacobian. If several latent points map to the same observed point, their contributions must be summed.

Lognormal models, copulas, and normalizing flows are not disconnected topics. They are all instances of the same idea: choose a representation in which the distribution is easier to describe, then transform back correctly.

## Do not confuse in 2.6

Do not confuse transforming a variable with transforming its density by direct substitution.

Do not forget that support changes under transformation.

Do not use a one-branch inverse formula when the map has multiple inverse branches on the relevant support.

Do not treat the Jacobian as an algebraic afterthought. It is the term that enforces probability conservation under local stretching and compression.

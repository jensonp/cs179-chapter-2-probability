# 2.6 Change-of-Variable Models

Change-of-variable modeling appears when a random variable is easier to understand in one space than in another. Sometimes the observed variable has awkward support, such as positivity. Sometimes the observed distribution is highly skewed, but becomes regular after a transformation. Sometimes the dependence structure of a multivariate distribution becomes easier to describe only after the coordinates are remapped. The central idea is therefore not a calculus trick. It is a modeling strategy: begin with a random variable or latent representation whose distribution is simple, transform it into the variable we care about, and then compute the resulting density correctly.

The core law behind the entire section is **probability conservation**. A transformation may move mass from one region to another. It may stretch the space in some directions and compress it in others. But it cannot create or destroy total probability. That is why a Jacobian term appears. The Jacobian is not extra decoration added after the “real” formula. It is the exact correction needed because density is height per unit length, area, or volume, and those units change under transformation.

Before writing formulas, it helps to keep the objects separate. There is a **base variable**, usually called `Z`, whose distribution we already know. There is a **transformed variable**, usually called `X`, defined by a map such as `X = f(Z)`. There is the **support** of each variable, which may also change under the map. And there are **events**, such as `a ≤ X ≤ b`, which are often easiest to compute by translating them back into statements about `Z`. Most confusion in this topic comes from mixing up those four things.

A useful mental sequence is:

1. start from a base variable whose density is known;
2. define the transformed variable by an explicit map;
3. identify the support of the transformed variable;
4. map events in `X`-space back into `Z`-space;
5. correct the density for local stretching or compression.

That sequence is the backbone of the whole section. The later discussions of lognormal variables, copulas, and normalizing flows are not new principles. They are more sophisticated uses of the same one.

## Why transformations appear in probabilistic modeling

This section must appear once densities have been introduced, because densities by themselves do not tell us how a distribution changes when the variable is re-expressed. Earlier sections teach us how to describe a distribution in a fixed coordinate system. But probabilistic modeling constantly asks a harder question: if a random quantity is defined indirectly, or if we choose a more convenient representation, how do we describe its distribution in the new space without losing mathematical correctness?

The answer is not “plug the transformation into the density.” That shortcut is one of the most common mistakes in the subject. The real answer is subtler: the transformation changes both *where* probability mass sits and *how densely* that mass is packed. That is why the inverse map appears, and that is why the Jacobian correction is unavoidable.

This point matters later for three different reasons. First, it explains transformed families such as the lognormal. Second, it supports dependence constructions such as copulas, where variables are moved into percentile space before dependence is modeled. Third, it underlies normalizing flows, where a complicated density is represented as an invertible transformation of a simple one. So this section is not isolated technique. It is the point where “a random variable with a density” becomes “a random variable that can be modeled through representation change.”



## Scalar change of variables

The one-dimensional case is the right place to understand the mechanism before the notation becomes heavier. Let `Z` be a scalar random variable with known density `p_Z`, and let

$$
X = f(Z).
$$

We are trying to answer a very specific question: **what is the density of `X`?**

The important thing to notice first is that the transformation acts on the variable, not directly on the density. We do not begin by manipulating the graph of `p_Z`. We begin by asking how intervals in `X`-space correspond to intervals in `Z`-space. Once that correspondence is clear, the density formula follows.

### The object being introduced

A scalar change-of-variables formula is a rule for converting a known density on one variable into the density of another variable obtained by a deterministic transformation. In the formula below, the map `f` is fixed, the base density `p_Z` is fixed, and the variable that ranges is the target point `x` in the transformed space.

The question the formula answers is not “what is the transformed graph?” but “how much probability lies near `x`, and how did that probability get there from the base variable?”

### Formal definition: monotone invertible case

Suppose `f` is differentiable and invertible on the support region being used, with inverse

$$
g = f^{-1}.
$$

Then the density of `X` is

$$
p_X(x) = p_Z(g(x))\,|g'(x)|,
$$

for those `x` that lie in the transformed support.

### Interpretation

This formula says two things, in this order.

First, to know the density at `x`, you must ask which latent point `z` produced that `x`. That is why the inverse appears. The relevant latent point is not `f(x)` but `g(x)`.

Second, once that latent point is found, the density must be corrected by a local width-conversion factor. If a short interval in `X`-space corresponds to a narrower interval in `Z`-space, then the density in `X`-space must be higher, because the same probability mass is now packed into less width. If the interval becomes wider, the density must be lower. The factor `|g'(x)|` is exactly that local width ratio.

### Why the inverse appears

The cleanest way to see the inverse is to think in terms of events rather than formulas. If `f` is increasing, then

$$
F_X(x) = \mathbb{P}(X \le x)
       = \mathbb{P}(f(Z) \le x)
       = \mathbb{P}(Z \le g(x))
       = F_Z(g(x)).
$$

Now differentiate with respect to `x`:

$$
p_X(x) = p_Z(g(x))\,g'(x).
$$

If `f` is decreasing, then the derivative is negative, but density must remain nonnegative, so we take absolute value.

The conceptual lesson is that transformed-variable questions are often easiest to answer by translating them back into the base variable. That is the same logic used later for transformed events and transformed densities.

### Why the derivative appears

The derivative appears because density is measured per unit width. A transformation changes local width.

Suppose a tiny interval around `x` has width `dx`. Under the inverse map, it corresponds to a tiny interval around `z = g(x)` whose width is approximately

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

When `f` is monotone and invertible on the relevant support region, the formula above applies directly. This is the clean case, and it should be mastered before moving to more complicated mappings.

### Worked example: scaling a uniform variable

This example is chosen because it exposes the entire mechanism without any distracting algebra.

Let

$$
Z \sim \mathrm{Unif}[0,1], \qquad X = 2Z.
$$

We identify the ingredients in order.

The map is `f(z) = 2z`. The inverse is

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

At this point, the support check matters. The base density `p_Z(z)` equals `1` only when `z \in [0,1]`. So we must ask when `x/2 \in [0,1]`. That condition is

$$
0 \le x/2 \le 1
\quad \Longleftrightarrow \quad
0 \le x \le 2.
$$

Therefore

$$
p_X(x) = \frac{1}{2} \qquad \text{for } 0 \le x \le 2,
$$

and `p_X(x)=0` elsewhere.

What was checked here, and why did each check matter?

First, we found the inverse because the density at `x` depends on the latent point that generated it. Second, we computed the derivative because density must be corrected for local width change. Third, we checked the transformed support because the base density is only valid on `[0,1]`. The final answer makes the conservation law visible: the interval length doubled, the density height halved, and total probability stayed equal to one.

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

Now check the support: `1-x \in [0,1]` exactly when `x \in [0,1]`. Hence

$$
p_X(x)=1 \qquad \text{for } x \in [0,1],
$$

and zero elsewhere.

The general lesson is that a negative derivative means the ordering of points has reversed, not that probability has become negative. That is why the Jacobian factor uses absolute value.

### Misconception block

Do not confuse “apply the function to the variable” with “apply the function to the density.”

If `X = f(Z)`, the transformed density is **not** obtained by replacing `z` with `f(z)` inside `p_Z`. The correct procedure is: identify which latent point maps to the observed point, then correct for local stretching or compression. The inverse map and the Jacobian are not optional clean-up steps. They are the whole content of the rule.

## Case B: non-monotone or multi-branch map

Now we can state the most important failure mode of the scalar formula.

If the transformation is not one-to-one on the relevant support, then several latent points may map to the same observed point. In that case, the density at `x` receives contributions from every inverse branch that reaches `x`. A one-branch formula misses probability mass.

### Formal rule for the multi-branch case

If the solutions to `f(z)=x` are `z_1(x), \dots, z_k(x)` on the relevant support, then

$$
p_X(x) = \sum_{i=1}^k p_Z(z_i(x))\left|\frac{dz_i}{dx}\right|.
$$

This is not a different principle. It is the same conservation law, but now several latent regions contribute to the same observed location.

### Worked example: squaring a symmetric variable

This example is chosen because it makes the failure of the one-branch formula impossible to ignore.

Let

$$
Z \sim \mathrm{Unif}[-1,1], \qquad X = Z^2.
$$

We first identify the support of `X`. Because `Z^2` ranges from `0` to `1`, the support is `x \in [0,1]`.

Now solve the inverse relation. For a fixed `x` in `(0,1]`, the equation `z^2 = x` has two solutions:

$$
z_1(x) = \sqrt{x}, \qquad z_2(x) = -\sqrt{x}.
$$

Each branch has derivative magnitude

$$
\left|\frac{dz_i}{dx}\right| = \frac{1}{2\sqrt{x}}.
$$

The base density of `Z` is `1/2` on `[-1,1]`. Therefore each branch contributes

$$
\frac{1}{2}\cdot\frac{1}{2\sqrt{x}} = \frac{1}{4\sqrt{x}}.
$$

Since there are two branches, the total density is

$$
p_X(x) = \frac{1}{2\sqrt{x}} \qquad \text{for } 0 < x \le 1,
$$

and zero elsewhere.

The reason this example matters is not just the final formula. It teaches the general pattern: when a map folds space, multiple latent locations can pile probability mass into the same observed location. The density must add all of those contributions.

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

The factor `1/x` is not cosmetic. It is the Jacobian correction required because equal additive steps in `Z` become unequal multiplicative steps in `X`.

### Why the lognormal is skewed

The skewness is best understood geometrically. Equal distances in `Z` do not become equal distances in `X`.

Moving from `Z=0` to `Z=1` sends `X` from `1` to `e`. Moving from `Z=1` to `Z=2` sends `X` from `e` to `e^2`. The right side is stretched more aggressively than the left. So probability mass that was symmetrically arranged in Gaussian space becomes asymmetrically spread in observed space, creating the long right tail.

### Event translation lesson

A transformed-variable probability is often easiest to compute by moving the event back to the base space. For example, if `Z \sim \mathcal{N}(0,1)` and `X=e^Z`, then

$$
\mathbb{P}(1 \le X \le e)
= \mathbb{P}(0 \le Z \le 1).
$$

This is a small calculation, but it teaches a large habit: transformed-variable events are often conceptually simpler than transformed-variable densities.

### Retain / Do not confuse for the scalar case

Retain the following.

A transformed density is determined by three things together: the inverse map, the Jacobian correction, and the transformed support. None of the three can be skipped.

Do not confuse monotonicity with differentiability. A smooth map can still fail to be globally invertible. Do not confuse a negative derivative with negative density. And do not use the one-branch formula in a multi-branch situation.



## Multivariate change of variables

In several dimensions, the idea is unchanged but the bookkeeping becomes geometric rather than one-dimensional. Instead of asking how a tiny interval changes width, we ask how a tiny box changes area or volume.

Let

$$
X = f(Z),
$$

where `Z` and `X` are now vectors, and suppose the map is invertible on the region of interest with inverse

$$
g = f^{-1}.
$$

### The object being introduced

The new object is the **Jacobian matrix** of the inverse map. It records how each output coordinate of `g` changes as each input coordinate changes. The determinant of that matrix is the local volume-scaling factor.

This is the exact multivariate analogue of the derivative in one dimension. In one dimension, the derivative tells us how lengths change locally. In several dimensions, the determinant tells us how volumes change locally.

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

The determinant answers a geometric question: if we take a tiny box around `x` in observed space and map it back into latent space, by what factor does its local volume change?

If the inverse map expands volume by a factor of `5`, then the density at `x` must be multiplied by `5`, because the same probability mass occupies a larger latent region. If the inverse map compresses volume by a factor of `5`, then the density must be divided accordingly when moving in the opposite direction. The determinant is therefore the local volume-conversion factor demanded by probability conservation.

The absolute value remains necessary. A negative determinant means orientation reversal, not negative probability.

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



## Optional enrichment: copula models

Copulas are worth introducing here because they are another representation-change idea. They are not a separate branch of probability dropped into the section without warning. Their purpose is to separate two modeling questions that are often entangled in raw coordinates:

1. what each individual variable looks like on its own;
2. how the variables depend on one another jointly.

The first step is to remove the marginal scales and shapes. For a random variable `X_i` with continuous CDF `F_i`, define

$$
U_i = F_i(X_i).
$$

When `F_i` is continuous, `U_i` is uniform on `[0,1]`. This fact is called the **probability integral transform**.

### Why this matters

The transformation to `U_i` removes the original units and marginal shape. Once each coordinate is converted into percentile space, what remains is dependence structure. That is the conceptual payoff of a copula: it is a joint distribution on percentile coordinates, so it describes how variables move together after the marginal behavior has been stripped away.

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

A standard modeling pipeline is:

1. estimate or specify each marginal CDF;
2. map data into percentile space using those marginals;
3. optionally map from uniform percentile space into Gaussian latent space using `\Phi^{-1}`;
4. model dependence in that transformed space.

The central lesson is not the pipeline itself. It is the idea that a hard joint model can become easier once marginal shape and dependence are separated by transformation.

### Misconception block

Do not confuse a copula with a marginal distribution, and do not confuse dependence in raw units with dependence in percentile space. A copula does not tell you what each variable looks like by itself. It tells you how the coordinates are coupled once the marginals have been factored out.



## Optional enrichment: normalizing flows

Normalizing flows are best understood as a modern reuse of the same law, not as a separate advanced topic with different foundations. A flow begins with a simple base density, often Gaussian, and then learns an invertible map that transforms that simple density into one that matches the observed data distribution.

Let

$$
X = f(Z),
$$

where `Z` has simple density `p_Z` and `f` is invertible. Then the transformed log-density is

$$
\log p_X(x)
= \log p_Z\bigl(f^{-1}(x)\bigr)
  + \log\bigl|\det J_{f^{-1}}(x)\bigr|.
$$

This is exactly the same change-of-variable rule already developed above. The only difference is that the transformation is no longer hand-chosen; it is parameterized and learned from data.

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

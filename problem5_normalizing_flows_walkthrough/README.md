# Problem 5 Walkthrough: Density Estimation with Normalizing Flows

Repository context: `jensonp/cs179-chapter-2-probability`, `hw2_solutions/README.md`.

This document is a self-contained rewrite of the **context**, **vocabulary**, and **solution logic** for Problem 5. The goal is not to repeat the code mechanically. The goal is to make every object in the problem intelligible **at the moment it appears**, with no hidden dependency on later explanation.

---

## 1. What Problem 5 is trying to teach

Earlier probability problems in the course live in settings where the probability object is easy to write down directly:

- a small probability table,
- a Bayesian network with a manageable set of variables,
- or a Markov chain with a finite transition matrix.

Problem 5 changes the setting.

Now the data are points in the plane, so each observation is a vector in $\mathbb{R}^2$. The target distribution is complicated enough that:

- it is easy to **sample from it**, because the homework gives a generator, but
- it is not easy to **write its density in a simple closed form**.

That is the pressure that forces the new idea.

The new idea is:

$$
\text{start with a simple density you know exactly, then warp it by an invertible map.}
$$

If the warp is chosen carefully, then the final model is flexible enough to fit complicated data **and** still has a tractable density.

That construction is called a **normalizing flow**.

---

## 2. The main question of the problem

The problem is asking for a model of a random vector $X \in \mathbb{R}^2$.

More specifically, it wants a model density $p_\theta(x)$ that can do two jobs:

1. **sample generation:** produce new points that look like the target data,
2. **density evaluation:** assign a numerical density value to any point $x$.

Those two goals are separate.

A model that can generate samples is not automatically a model whose density you can evaluate exactly.

A normalizing flow is introduced precisely because it gives both.

---

## 3. Vocabulary you need before the solution makes sense

### 3.1 Density

A **density** is not the same thing as a probability at a point.

For a continuous random vector $X$, the probability of seeing exactly one point is zero. What density does is tell you how probability is distributed over **small regions**.

If $A$ is a tiny region around $x$, then informally

$$
P(X \in A) \approx p(x) \cdot \text{area}(A).
$$

So density is “probability per unit area” in two dimensions.

This matters because the change-of-variables formula is really about how **small areas** are stretched or compressed.

### 3.2 Base distribution

The **base distribution** is the simple distribution you start from.

In this problem, the base distribution is the two-dimensional standard Gaussian:

$$
Z \sim \mathcal{N}(0, I_2).
$$

That means:

- the mean is $(0,0)$,
- the covariance matrix is the $2 \times 2$ identity,
- the two coordinates are independent standard normals before the transform is applied.

### 3.3 Target distribution

The **target distribution** is the unknown distribution that actually generates the homework data.

In this problem, you do not write that density directly. Instead, you only have a **sampling procedure** that produces points from it.

### 3.4 Transform

A **transform** is a function that maps one space into another.

Here the transform is a parameterized map

$$
f_\theta : \mathbb{R}^2 \to \mathbb{R}^2.
$$

It takes a latent point $z$ from the base Gaussian and sends it to an observed point

$$
X = f_\theta(Z).
$$

### 3.5 Invertible / bijective

A transform is **invertible** if every output comes from exactly one input.

So for each $x$ in the image of the map, there is one and only one latent point

$$
z = f_\theta^{-1}(x).
$$

This condition is non-negotiable for the simple flow formula. If two different latent points could collapse to the same observed point, then the clean one-to-one density formula would fail.

### 3.6 Jacobian

For a vector-valued map $f = (f_1, f_2)$ on $\mathbb{R}^2$, the **Jacobian matrix** at a point is the matrix of first derivatives:

$$
J_f(z) =
\begin{bmatrix}
\frac{\partial f_1}{\partial z_1} & \frac{\partial f_1}{\partial z_2} \\
\frac{\partial f_2}{\partial z_1} & \frac{\partial f_2}{\partial z_2}
\end{bmatrix}.
$$

This matrix is the best local linear approximation to the transform near that point.

### 3.7 Determinant of the Jacobian

The number

$$
\det J_f(z)
$$

describes local area scaling.

- If its absolute value is greater than $1$, the map locally expands area.
- If its absolute value is between $0$ and $1$, the map locally compresses area.
- If its absolute value is exactly $1$, it locally preserves area.

The absolute value is what matters for density, because density cares about the magnitude of the area change, not about whether orientation flips.

### 3.8 Coupling layer

A **coupling layer** splits the coordinates into two blocks and transforms one block using information from the other block.

In this problem the ambient dimension is only $2$, so the split is effectively “first coordinate” and “second coordinate.”

That structure is used because it keeps the transform expressive **and** keeps the inverse and determinant manageable.

### 3.9 Spline

A **spline** is a function built piece by piece across intervals or bins rather than by one global formula.

In flow models, the point of using a spline is that each coordinate transform can bend and reshape the distribution much more flexibly than a simple scale-and-shift map, while still remaining invertible.

### 3.10 Log likelihood

If the model density is $p_\theta(x)$ and the observed data are $x_1, \dots, x_m$, then the average log likelihood is

$$
\frac{1}{m} \sum_{j=1}^m \log p_\theta(x_j).
$$

Maximizing this means making the model assign high density to the observed data.

Equivalently, the training loop minimizes the negative average log likelihood:

$$
\mathcal{L}(\theta) = -\frac{1}{m} \sum_{j=1}^m \log p_\theta(x_j).
$$

---

## 4. What is fixed and what varies in Problem 5

This is the first check you should make before reading any solution.

### Fixed throughout the setup

The following are fixed before training begins:

- the target data generator,
- the fact that observations live in $\mathbb{R}^2$,
- the choice of base family $\mathcal{N}(0, I_2)$,
- the choice of transform family: a spline coupling flow,
- the number of spline bins,
- the spline bounding box,
- the optimizer family and learning rate.

### Varying during the procedure

The following vary:

- the sampled latent points $z$,
- the sampled target data points $x$,
- the minibatch drawn at each training step,
- the transform parameters $\theta$ during optimization.

### What the procedure is trying to conclude

By the end, the model should support the conclusion:

> a Gaussian base distribution, after being warped by the learned invertible map, gives a density and sample generator that approximate the target 2D distribution.

---

## 5. Step 1 of the homework: understand the target generator before fitting anything

The homework provides a generator that first draws two hidden variables and then builds a noisy point in the plane.

The hidden variables are:

$$
w \sim \mathrm{Uniform}(0,1),
\qquad
I \sim \mathrm{Bernoulli}(0.3).
$$

Here $I$ is a binary random variable taking values $0$ or $1$.

The mean location before the final noise is

$$
\mu(w, I) =
\begin{bmatrix}
w \cdot 0.6^I + 0.2I - 0.5 \\
-2(1-I)(2w-1)^2 - I + 1
\end{bmatrix}.
$$

Then the actual observation is

$$
X = 5\mu(w, I) + \varepsilon,
$$

with Gaussian noise

$$
\varepsilon \sim \mathcal{N}\left(0, \bigl(0.1(I+1)\bigr)^2 I_2\right).
$$

Now unpack the two cases separately.

### Case 1: $I = 0$

Then the mean becomes

$$
\mu(w, 0) =
\begin{bmatrix}
w - 0.5 \\
-2(2w-1)^2 + 1
\end{bmatrix}.
$$

So before scaling by $5$, the first coordinate moves linearly with $w$, while the second coordinate traces a downward-opening curved arc.

The noise scale is

$$
0.1(0+1) = 0.1.
$$

So this branch is the **curved, less noisy** component.

### Case 2: $I = 1$

Then the mean becomes

$$
\mu(w, 1) =
\begin{bmatrix}
0.6w - 0.3 \\
0
\end{bmatrix}.
$$

So before scaling by $5$, the second coordinate is exactly $0$, and the first coordinate varies along a horizontal line segment.

The noise scale is

$$
0.1(1+1) = 0.2.
$$

So this branch is the **straighter, noisier** component.

### Why this analysis matters

This local unpacking tells you immediately why one Gaussian is not enough.

The target is not one round blob. It is a mixed geometric structure:

- one curved component,
- one straighter component,
- different noise levels in the two regimes.

That is the exact reason a more flexible density model is needed.

---

## 6. Why the plot of generated data matters

When you plot samples from the target generator, that plot is not just a visualization requirement.

It serves as the reference answer to this question:

> What shape is the learned model trying to imitate?

Without that plot, the rest of the problem becomes abstract. With that plot, every later object has a concrete role:

- the base Gaussian is the simple starting cloud,
- the flow transform is the reshaping mechanism,
- the final trained samples are the attempt to match the target cloud.

---

## 7. Step 2 of the solution: define the base distribution

The base distribution is

$$
Z \sim \mathcal{N}(0, I_2).
$$

This should be interpreted carefully.

It does **not** mean the homework believes the data are Gaussian.

It means:

- the latent starting point is chosen to be simple,
- its density is known exactly,
- sampling from it is easy,
- and evaluating $\log p_Z(z)$ is easy.

That is why the Gaussian is chosen.

So the Gaussian solves the **tractability** problem, not the **realism** problem.

---

## 8. Step 3 of the solution: what the flow transform is supposed to do

The learned model defines

$$
X = f_\theta(Z), \qquad Z \sim \mathcal{N}(0, I_2).
$$

This means the final observed density is not written down directly. It is induced by sending latent Gaussian points through the map $f_\theta$.

The central idea is geometric:

- where the target data are dense, the transform should compress more Gaussian mass into that region,
- where the target data are sparse, the transform should spread mass out or avoid concentrating it there,
- and the transform must do this while remaining invertible.

So the transform is learning a **warp of space**, not merely a lookup table of probabilities.

---

## 9. Why invertibility matters

A lot of flow explanations say “the transform must be invertible” but never explain what that buys you. Here is the exact reason.

If a data point $x$ is observed, likelihood evaluation needs to answer:

> which latent point $z$ produced this $x$?

If the transform is invertible, then there is one unique answer:

$$
z = f_\theta^{-1}(x).
$$

That unique backward mapping lets you evaluate density by:

1. sending $x$ back to latent space,
2. evaluating the simple Gaussian density there,
3. correcting for how the transform stretched or compressed area near that point.

If the map were not invertible, then one observed point could come from multiple latent points. The clean formula would no longer hold in this simple form.

So invertibility is not cosmetic. It is exactly what turns “a geometric warp” into “a tractable density model.”

---

## 10. Local stretching, local compression, and why the determinant appears

This is the point where many notes get too compressed. Here is the full story.

### 10.1 A density is about probability in tiny regions

Take a tiny region around a latent point $z$.

Its probability mass is approximately

$$
p_Z(z) \, dz,
$$

where $dz$ stands for a tiny area element in latent space.

Now apply the transform $x = f_\theta(z)$. That tiny region moves to a tiny region around $x$.

The same probability mass must still be there, because the transform is only moving points around. It is not creating or destroying probability.

So

$$
p_X(x) \, dx = p_Z(z) \, dz.
$$

The only question is: how are $dx$ and $dz$ related?

### 10.2 The Jacobian gives the local linear approximation

Near a point, a smooth nonlinear map behaves approximately like a linear map.

That local linear map is the Jacobian matrix.

In two dimensions, a linear map sends tiny squares to tiny parallelograms. The absolute determinant of that linear map equals the area scaling factor.

So locally,

$$
dx \approx \left|\det J_{f_\theta}(z)\right| \, dz.
$$

This is what “local stretching” means.

- If the determinant magnitude is $2$, a tiny area doubles.
- If the determinant magnitude is $0.5$, a tiny area is halved.

### 10.3 Why density must compensate

Now substitute that area relation into probability conservation:

$$
p_X(x) \, dx = p_Z(z) \, dz.
$$

Since

$$
dx = \left|\det J_{f_\theta}(z)\right| \, dz,
$$

you get

$$
p_X(x)
=
\frac{p_Z(z)}{\left|\det J_{f_\theta}(z)\right|},
\qquad x = f_\theta(z).
$$

Equivalently, writing everything in terms of $x$ by substituting $z = f_\theta^{-1}(x)$,

$$
p_X(x)
=
p_Z\bigl(f_\theta^{-1}(x)\bigr)
\left|\det J_{f_\theta^{-1}}(x)\right|.
$$

That is the change-of-variables formula used in normalizing flows.

### 10.4 What the formula means in plain technical English

For a data point $x$:

1. map it backward to latent space,
2. ask how plausible that latent point is under the base Gaussian,
3. multiply by the area-correction factor that accounts for local distortion of space.

This is why the model can have a complicated density even though the base density is simple.

### 10.5 A one-dimensional sanity check

If $Y = 2X$ in one dimension, then intervals are stretched by a factor of $2$.

So density must be halved:

$$
p_Y(y) = p_X(y/2) \cdot \frac{1}{2}.
$$

The multidimensional determinant term is the exact generalization of that idea.

---

## 11. Why the word “normalizing” appears in “normalizing flow”

The determinant correction is what keeps the transformed density correctly normalized.

Without that correction, the warp would move points around but the resulting function would not generally integrate to $1$.

So the model is not just “a flexible transform.” It is a transform equipped with the exact correction needed to remain a valid probability density.

That is the sense in which the flow is “normalizing.”

---

## 12. What a transformed distribution object means in this problem

When the solution constructs a transformed distribution from the base Gaussian and the spline coupling transform, the object being created should be interpreted as follows.

### For sampling

To generate a sample:

1. draw a latent point $z$ from the base Gaussian,
2. apply the forward transform $x = f_\theta(z)$,
3. return $x$.

### For density evaluation

To evaluate the density at a point $x$:

1. apply the inverse transform to get $z = f_\theta^{-1}(x)$,
2. evaluate the Gaussian log density at $z$,
3. add the log absolute determinant correction.

So one object supports both directions:

- forward for sampling,
- backward for scoring.

---

## 13. What a coupling transform is doing here

A coupling transform splits the input vector into two parts. In dimension $D$, the generic form is

$$
y_{1:d} = g_\theta(x_{1:d}),
$$

$$
y_{d+1:D} = h_\phi(x_{d+1:D}; x_{1:d}).
$$

Now specialize to this homework.

The input dimension is $2$, so the split is effectively one coordinate and one coordinate. You should picture the transform as:

$$
y_1 = g(x_1),
$$

$$
y_2 = h(x_2; x_1).
$$

This means:

- the first coordinate is transformed by its own invertible 1D map,
- the second coordinate is transformed by another invertible 1D map whose parameters depend on the first coordinate.

That dependency is why it is called a **coupling** layer.

One part of the vector controls how the other part is transformed.

### Why this structure is useful

This design balances two goals that usually fight each other:

- expressive power,
- computational tractability.

It is expressive because the second coordinate can be transformed differently at different values of the first coordinate.

It is tractable because the Jacobian becomes triangular.

For the 2D form above,

$$
J =
\begin{bmatrix}
\frac{\partial y_1}{\partial x_1} & 0 \\
\frac{\partial y_2}{\partial x_1} & \frac{\partial y_2}{\partial x_2}
\end{bmatrix}.
$$

The upper-right entry is zero because $y_1$ does not depend on $x_2$.

So

$$
\det J
=
\frac{\partial y_1}{\partial x_1}
\cdot
\frac{\partial y_2}{\partial x_2}.
$$

That is much easier than computing the determinant of a fully dense Jacobian.

This is the exact reason coupling layers are popular in normalizing flows.

---

## 14. What a spline transform adds beyond a simple affine map

A simple affine 1D transform has the form

$$
y = ax + b,
$$

with $a > 0$ for invertibility.

That only allows uniform stretching and shifting.

A spline transform is much more flexible.

It divides the input range into bins and uses a separate simple formula on each bin, while ensuring that the full curve is:

- continuous,
- monotone,
- and invertible.

So a spline can:

- stretch one interval strongly,
- compress another interval mildly,
- bend density in different ways in different regions,
- while still having an analytically manageable inverse and derivative.

That extra regional flexibility is exactly what makes spline flows far more expressive than plain affine coupling.

---

## 15. What the homework call `spline_coupling(2, count_bins=16, bound=6)` means

This call introduces several pieces of vocabulary that should be explicit.

### Input dimension `2`

The ambient variable is two-dimensional. Each sample is a vector in $\mathbb{R}^2$.

### `count_bins = 16`

The spline is divided into $16$ segments.

This controls how much local freedom the 1D spline maps have.

- More bins usually mean more flexibility.
- Fewer bins mean a simpler, smoother, more restricted transform.

### `bound = 6`

The spline acts nontrivially inside a bounded box determined by the value $6$.

Pyro’s spline implementation uses the identity map outside the spline interval. So `bound=6` means the learned nonlinearity is concentrated inside a central region, and the tails outside that region are left unchanged.

This is a boundary condition, not a cosmetic parameter.

It means that extremely large inputs are not warped arbitrarily by the spline. They pass through as identity outside the bounded region.

### What the helper is hiding

The helper function creates not only the transform but also the internal neural network that outputs the spline parameters needed for the conditional part of the coupling layer.

So although the homework call looks compact, the object it produces is a full learnable bijection, not a fixed hand-coded curve.

---

## 16. Why the initial flow sample is worth plotting before training

Before optimization, the transform parameters exist but are still near their initialization.

The initial flow plot answers a specific question:

> If I take the chosen architecture seriously as a probabilistic model, what shape does it produce before data have influenced it?

This matters because it separates three different objects that students often collapse together:

1. the target generator,
2. the base Gaussian,
3. the untrained flow architecture.

Those are not the same thing.

The target generator is the distribution to imitate.

The base Gaussian is the raw latent source.

The untrained flow is the chosen model class before fitting.

---

## 17. Why the loss is the right statistical objective

The training objective is the negative average log likelihood:

$$
\mathcal{L}(\theta)
=
-\frac{1}{m}\sum_{j=1}^m \log p_\theta(x_j).
$$

This deserves a careful interpretation.

### What is fixed in this expression

- the observed minibatch points $x_1, \dots, x_m$ for the current step,
- the model family,
- the formula for $p_\theta(x)$.

### What varies

- only the parameters $\theta$ of the transform.

### What each term checks

Each term $\log p_\theta(x_j)$ checks:

> according to the current model, how plausible is this observed data point?

If the model places very low density on a point that the generator commonly produces, then that log density is very negative.

That makes the average log likelihood smaller, which makes the negative average log likelihood larger.

So minimizing the loss forces the model to move probability mass toward the regions where the data actually live.

### Population version of the same idea

The ideal objective is

$$
\mathbb{E}_{X \sim p_{\text{data}}}\left[-\log p_\theta(X)\right].
$$

The minibatch average is just a Monte Carlo approximation to that expectation.

---

## 18. Why drawing fresh data each training step is legitimate here

In many machine-learning settings, you are handed one fixed finite dataset.

Here the homework gives direct access to the generator itself. That means each training step can draw a fresh minibatch from the target distribution.

So the optimization is repeatedly seeing new samples from the same underlying population.

This matters because the loss is not merely trying to memorize one small cloud of points. It is trying to fit the actual sampling process.

---

## 19. What `log_prob` is really doing inside the flow

When the solution evaluates `flow.log_prob(data)`, the conceptual steps are:

1. take each observed point $x$ in the minibatch,
2. invert the flow to get the corresponding latent point $z$,
3. evaluate the base Gaussian log density at $z$,
4. add the log determinant correction from the inverse Jacobian,
5. return the resulting log density for each point.

So the model is not directly memorizing a histogram in data space.

It is scoring each observed point by asking:

- where does this point land when mapped back to latent space?
- how plausible is that latent point under the Gaussian?
- how much did the inverse transform compress or expand volume near this point?

---

## 20. Why the cache is cleared after each optimizer step

This is a local implementation detail that does deserve a conceptual explanation.

Flow transforms often cache forward/inverse information and determinant terms to avoid recomputing them unnecessarily.

That is safe only while the transform parameters remain unchanged.

After an optimizer step, the parameters have changed. So any cached forward/inverse relation or log-determinant value computed under the old parameters is stale.

Clearing the cache enforces this rule:

> after parameters change, future density and inverse computations must be recomputed using the new transform.

So the cache clear is not a random library ritual. It is a consistency requirement for stateful transform modules.

---

## 21. Full walkthrough of the solution, in the order the math becomes meaningful

This section rewrites the whole solution path without code.

### Step A: identify the target distribution

The first task is not fitting. The first task is understanding what kind of distribution must be modeled.

The generator produces a mixture-like 2D structure with:

- one curved component,
- one straighter component,
- different noise levels across the two components.

This immediately rules out the idea that a single isotropic Gaussian can represent the data well.

### Step B: choose a tractable latent distribution

A standard Gaussian in $\mathbb{R}^2$ is chosen as the latent source.

This choice is motivated by tractability:

- sampling is trivial,
- the log density is exact and easy to evaluate,
- it is smooth and supported on all of $\mathbb{R}^2$.

### Step C: choose a flexible but tractable transform family

A spline coupling flow is chosen because the problem needs a transform that is:

- invertible,
- differentiable,
- expressive enough to bend a Gaussian into a non-Gaussian shape,
- and structured enough that the Jacobian determinant stays tractable.

### Step D: define the model distribution

The model is the pushforward of the Gaussian under the transform:

$$
X = f_\theta(Z), \qquad Z \sim \mathcal{N}(0, I_2).
$$

This one line means that every feature of the final density is produced by the geometry of the warp.

### Step E: inspect the model before training

Sampling from the base Gaussian shows the raw latent shape.

Sampling from the untrained flow shows what the chosen architecture looks like before learning.

This creates the correct conceptual baseline before optimization begins.

### Step F: fit the transform by maximum likelihood

Training adjusts only the transform parameters $\theta$.

At each step:

- a fresh minibatch is drawn from the target generator,
- the model computes log densities for those points,
- the negative average log likelihood is formed,
- gradients move the transform parameters in the direction that increases density on the observed data.

The fixed point of that pressure, if optimization succeeds, is a transform whose warped Gaussian resembles the target distribution.

### Step G: sample from the trained model

After training, the sampling rule is unchanged:

1. draw from the Gaussian,
2. push through the transform.

What has changed is the parameter values inside the transform.

So if the model has learned well, the new samples should now resemble the target data cloud rather than the original round Gaussian cloud.

---

## 22. The deep trace that usually gets skipped: how one observed point is scored

Take one observed data point $x$ from the minibatch.

Here is the full scoring trace.

### Trace step 1: start in data space

You are given an observed point $x \in \mathbb{R}^2$.

At this stage, you do **not** ask how the target generator created it. The model does not know the hidden $w$ and $I$ used by the generator.

The model only knows its own transform and base distribution.

### Trace step 2: move backward through the inverse transform

Compute

$$
z = f_\theta^{-1}(x).
$$

This says: according to the current model, which latent Gaussian point corresponds to this observed point?

### Trace step 3: evaluate latent plausibility

Now evaluate the base Gaussian log density at $z$:

$$
\log p_Z(z).
$$

If $z$ lies near a high-density part of the Gaussian, this term is relatively large.

If $z$ lies far into a tail of the Gaussian, this term is much smaller.

### Trace step 4: compute the local volume correction

Now compute the log absolute determinant term for the inverse:

$$
\log \left| \det J_{f_\theta^{-1}}(x) \right|.
$$

This answers:

> near this observed point, how much does the inverse map expand or compress tiny areas?

If the inverse expands area strongly near $x$, the density contribution changes accordingly.

If the inverse compresses area, the density changes in the opposite direction.

### Trace step 5: add the two pieces

The final log density is

$$
\log p_\theta(x)
=
\log p_Z\bigl(f_\theta^{-1}(x)\bigr)
+
\log \left| \det J_{f_\theta^{-1}}(x) \right|.
$$

This is the number that enters the loss.

### Trace step 6: interpret the result

If this final log density is too small for many data points coming from the generator, then the loss is large. The optimizer then changes $\theta$ so that future backward-mapped points and local volume corrections produce higher density in the important regions.

That is the full statistical trace of one data point through the flow objective.

---

## 23. The deep trace that usually gets skipped: how one sample is generated after training

Now take the forward direction.

### Trace step 1: draw a latent point

Sample

$$
z \sim \mathcal{N}(0, I_2).
$$

This is a simple random point from the base Gaussian cloud.

### Trace step 2: apply the learned transform

Compute

$$
x = f_\theta(z).
$$

This moves the point into data space by the learned warp.

### Trace step 3: interpret what has happened geometrically

If the flow has learned well, then regions of latent Gaussian mass are sent into the curved and line-like regions where the target data tend to live.

So generation works because the transform has learned where to bend, stretch, and compress the Gaussian cloud.

### Trace step 4: repeat to get a sample cloud

Repeating the same forward rule many times produces a new cloud of points that can be compared visually with the target generator.

That is why the final scatterplot is the natural check for success in this homework.

---

## 24. What “one coupling layer is enough” means here

The assignment says one spline coupling layer should be enough for this toy problem.

This should not be interpreted as a universal theorem about flows.

It means only that for this specific 2D target distribution:

- the geometry is simple enough,
- the dimension is low enough,
- and the chosen spline coupling is flexible enough,

that one layer can already produce a reasonable fit.

In more complex or higher-dimensional settings, one coupling layer is often not enough. Multiple layers and permutations are commonly used so that all coordinates can influence one another more richly.

---

## 25. Boundary conditions and failure modes that belong in the explanation

### 25.1 If the transform is not invertible

Then the clean change-of-variables formula fails in this one-to-one form. The model would no longer have the simple exact density expression required by the homework.

### 25.2 If the determinant is hard to compute

Then exact likelihood-based training becomes impractical, because the whole objective depends on that term.

### 25.3 If the transform family is too weak

Then even perfect optimization cannot fit the target well, because the model class itself is not expressive enough.

### 25.4 If optimization is poor

Then the final samples may still look wrong even though the model class is in principle flexible enough.

### 25.5 If you confuse better-looking plots with exact recovery

Then you overclaim what the homework demonstrates. The scatterplots provide visual evidence of improvement, not a proof that the true target density has been recovered exactly.

### 25.6 If you forget that the spline acts as identity outside its bound

Then you misread what `bound=6` is doing. Outside the bounded spline interval, the transform is not learning arbitrary tail behavior through the spline itself.

---

## 26. Misconception blocks

### Do not confuse the base distribution with the final model

The base Gaussian is only the latent starting point. It is not intended to match the target data by itself.

### Do not confuse the target generator with the learned flow

The target generator is the source of truth producing training samples. The flow is the model trying to imitate that distribution.

### Do not confuse a transform with a density

The transform is a geometric map. The density arises only after combining the base density with the change-of-variables correction.

### Do not confuse high density with high probability at a point

For continuous variables, a point has probability zero. Density describes how probability is concentrated over small regions.

### Do not confuse local stretching with a global scale factor

The Jacobian determinant is usually different at different points. The map can expand one part of space and compress another.

### Do not confuse sampling with scoring

Sampling goes forward through the transform. Scoring goes backward through the inverse and includes the determinant correction.

### Do not confuse “one layer is enough here” with “one layer is always enough” 

The homework’s statement is task-specific, not a general principle of normalizing flows.

---

## 27. Compact glossary of the specific symbols and names used in the solution

### $w$
A scalar latent variable drawn uniformly from $[0,1]$. It moves the sample along one of the geometric components.

### $I$
A binary latent variable choosing between the two geometric regimes.

### $X$
The observed 2D random vector in data space.

### $Z$
The latent 2D Gaussian random vector in base space.

### $p_Z$
The base density, here the density of $\mathcal{N}(0, I_2)$.

### $f_\theta$
The learned invertible transform from latent space to data space.

### $f_\theta^{-1}$
The inverse map used when evaluating density at an observed point.

### $J_f$
The Jacobian matrix of first derivatives of the transform.

### $\det J_f$
The local area-scaling factor of the transform, up to sign.

### `count_bins`
The number of spline segments used in each 1D spline map.

### `bound`
The size of the bounded interval or box inside which the spline acts nontrivially; outside it, the transform acts as identity.

### Coupling layer
A transform that splits coordinates into two blocks and lets one block influence how the other is transformed.

### Spline
A piecewise-defined monotone curve used as an invertible 1D transformation.

### Log likelihood
The logarithm of the model density evaluated at observed data. Higher is better.

### Negative average log likelihood
The training loss minimized by the optimizer. Lower is better.

---

## 28. Final synthesis: the whole problem in one coherent picture

Problem 5 is a density-estimation problem in $\mathbb{R}^2$.

The target distribution is known only through a generator that produces a curved/noisy mixed geometric structure. A simple Gaussian cannot represent that shape directly.

So the model starts with a tractable latent Gaussian,

$$
Z \sim \mathcal{N}(0, I_2),
$$

then introduces a learned invertible warp,

$$
X = f_\theta(Z).
$$

Because the warp is invertible and has a tractable Jacobian determinant, the resulting density is exactly computable by

$$
p_X(x)
=
p_Z\bigl(f_\theta^{-1}(x)\bigr)
\left|\det J_{f_\theta^{-1}}(x)\right|.
$$

The transform family is a spline coupling layer, chosen because it is flexible enough to bend the Gaussian into a more complicated shape while still keeping inversion and determinant calculations manageable.

Training minimizes negative average log likelihood on samples from the target generator. That objective pushes the flow to assign high density to regions where the target generator places data.

After training, sampling still works in the same way as before:

1. draw a latent Gaussian point,
2. push it through the learned transform.

What changes is only the parameter values in the transform. If learning succeeds, the final sample cloud resembles the target generator much more closely than the original Gaussian cloud.

That is the full context and logic of the solution.

---

## 29. Sources

- Homework solution guide in the repository: <https://github.com/jensonp/cs179-chapter-2-probability/tree/main/hw2_solutions>
- Raw repository README used for Problem 5 wording and structure: <https://raw.githubusercontent.com/jensonp/cs179-chapter-2-probability/main/hw2_solutions/README.md>
- Pyro spline coupling documentation: <https://docs.pyro.ai/en/stable/_modules/pyro/distributions/transforms/spline_coupling.html>
- Pyro spline documentation: <https://docs.pyro.ai/en/stable/_modules/pyro/distributions/transforms/spline.html>
- PyTorch `TransformedDistribution` documentation/source summary: <https://github.com/pytorch/pytorch/blob/main/torch/distributions/transformed_distribution.py>
- Pyro normalizing flows tutorial: <https://pyro.ai/examples/normalizing_flows_i.html>
- Neural Spline Flows paper: <https://proceedings.neurips.cc/paper/2019/hash/7ac71d433f282034e088473244df8c02-Abstract.html>

# Probability and Inference: Computational Appendix

This appendix is a **workflow companion** to the main chapter. Its job is not to introduce the probability ideas for the first time, and it is not a programming-language tutorial. Its narrower purpose is to make the numerical structure of the chapter explicit enough that a reader can carry the mathematics into a spreadsheet, notebook, or ordinary programming language without turning important checks into guesswork.

The right way to use this appendix is after the conceptual lesson has already established what the object means. In the main text, the reader should learn what a conditional distribution is, why likelihood is not a posterior, why a Jacobian appears under a change of variables, and what Bayesian updating is doing. In this appendix, those same ideas are translated into workflows: what must be stored, what must be normalized, which quantity is being held fixed, what failure condition must be checked before proceeding, and what numerical pattern would signal that something has gone wrong.

That distinction matters. Many probability errors are not arithmetic errors. They are **object errors**. A student computes the value of a density and treats it as an event probability, or computes a likelihood and reads it as a distribution over parameters, or normalizes a vector whose denominator should actually have signaled an impossible conditioning event. The appendix is meant to prevent that kind of mistake by making the computational roles of the chapter's objects explicit.

## 1. Notation and Numerical Conventions

The chapter uses several objects that are numerically related but conceptually different, and computations go wrong most often when those roles are mixed.

An **event probability** such as $P(A)$ assigns a number to a set of outcomes. To compute it, one sums or integrates over all states inside that event. A **PMF or density value** such as $p(x)$ or $p(x,y)$ is a local quantity attached to a specific state. It is not, by itself, the probability of an interval or event. A **CDF** such as $F_X(x)$ is an accumulated quantity: it records the total probability up to a threshold. These are notationally close, but computationally they behave differently. A density can be larger than one, a CDF must be nondecreasing and stay between zero and one, and an event probability must come from aggregation rather than point evaluation.

Likelihood introduces a second role reversal that is easy to mishandle. For observed data $D$ and parameter $\theta$,

$$L(\theta)=p(D \mid \theta)$$

is read as a function of the parameter with the dataset held fixed. Numerically, this means the same algebraic expression can be read in two different ways depending on the question being asked. As a sampling model, $p(D\mid \theta)$ treats $\theta$ as fixed and the data as varying. As a likelihood, the data are the realized input and $\theta$ varies across candidate values. The formula may look identical, but the computational role is different.

Two numerical hazards recur across nearly every section. First, floating-point arithmetic introduces small normalization drift: quantities that should sum to one may come out as $0.999999$ or $1.000001$. Second, products of many small probabilities quickly underflow to zero even when the true mathematical value is positive. For that reason, one should explicitly renormalize probability vectors after accumulation steps and use log-likelihoods rather than raw likelihood products once the sample size is even moderately large.

The guiding rule for the entire appendix is therefore simple: before trusting a number, identify **what kind of probability object it is supposed to be**, **what is fixed**, **what is varying**, and **which invariants the object must satisfy**.

## 2. Finite Probability Tables

For finite discrete models, the most useful computational object is a table whose entries are nonnegative and whose total mass is one. That sounds elementary, but it is the concrete form in which much of discrete probability actually lives. Marginals, conditionals, posteriors, and evidence terms are not new mysterious objects in this setting. They are all obtained by a small number of table operations applied in the right order.

The key fact is that discrete inference is often simpler computationally than its notation suggests. Bayes' rule in a table is not a separate magical formula to memorize. It is a workflow. One first restricts attention to states compatible with the observed evidence. One then sums out coordinates that are not part of the query. Finally, one renormalizes what remains so that the resulting vector becomes a proper distribution. The conceptual version of this idea should appear in the conditioning lesson; the appendix records the operational version.

### Worked Example: Dentist Joint Table

Using the dentist example, the full joint table is

| $TDC$ | $p(T,D,C)$ |
|---|---:|
| 000 | 0.576 |
| 001 | 0.008 |
| 010 | 0.144 |
| 011 | 0.072 |
| 100 | 0.064 |
| 101 | 0.012 |
| 110 | 0.016 |
| 111 | 0.108 |

The first numerical audit is normalization:

$$0.576+0.008+0.144+0.072+0.064+0.012+0.016+0.108=1.$$

Without that check, every later conditional or marginal can inherit a silent error.

Now suppose the evidence is $T=1$. Restriction keeps only the rows with toothache:

| $DC$ | $p(T=1,D,C)$ |
|---|---:|
| 00 | 0.064 |
| 01 | 0.012 |
| 10 | 0.016 |
| 11 | 0.108 |

Marginalizing out $D$ gives the unnormalized vector over $C$:

| $C$ | $p(T=1,C)$ |
|---|---:|
| 0 | 0.064 + 0.016 = 0.080 |
| 1 | 0.012 + 0.108 = 0.120 |

The sum of that vector is

$$0.080+0.120=0.200.$$

That number is the evidence probability $p(T=1)$. After normalization,

| $C$ | $p(C \mid T=1)$ |
|---|---:|
| 0 | $0.080/0.200 = 0.40$ |
| 1 | $0.120/0.200 = 0.60$ |

The computational lesson is that Bayes' rule in table form is just the sequence restrict, sum, normalize.

### Audit Checklist for Discrete Tables

- every entry must be nonnegative
- the full joint table must sum to one
- every conditional table must sum to one across the conditioned variable
- if a denominator is zero, the requested conditional distribution is undefined and should not be silently normalized
- if an event is impossible under the model, its rows should contribute exact zeros rather than small negative numerical artifacts

## 3. Odds Updating and Base Rates

The ordinary Bayes formula is perfectly correct, but it can hide the structure of the update because the numerator and denominator are packed together. The odds form separates the update into two interpretable pieces: what you believed before the evidence arrived, and how strongly the evidence favors one hypothesis over the other. This makes the computation easier to debug because each piece can be inspected separately.

When this form is used numerically, the important point is not merely that odds can be converted back to probabilities. The deeper point is that evidence does not arrive in a vacuum. A large likelihood ratio can still leave the posterior probability small when the prior odds were extremely small to begin with. This is exactly the kind of base-rate effect that students often misread when they look only at test accuracy numbers.

For two hypotheses $H_1$ and $H_0$ and evidence $E$,

$$\frac{p(H_1 \mid E)}{p(H_0 \mid E)} = \frac{p(E \mid H_1)}{p(E \mid H_0)} \cdot \frac{p(H_1)}{p(H_0)}.$$

This should be computed as three separate pieces:

1. prior odds
2. likelihood ratio
3. posterior odds

### Worked Example: Medical Screening

Suppose

$$p(D=1)=0.01, \qquad p(T=+ \mid D=1)=0.95, \qquad p(T=+ \mid D=0)=0.10.$$

The prior odds of disease are

$$\frac{0.01}{0.99}\approx 0.0101.$$

The likelihood ratio of a positive test is

$$\frac{0.95}{0.10}=9.5.$$

So the posterior odds are

$$9.5 \times 0.0101 \approx 0.096.$$

Converting odds back to a probability gives

$$\frac{0.096}{1+0.096}\approx 0.0876.$$

This computation is the same as the direct posterior formula, but it makes the structure more explicit. The evidence is favorable, because the likelihood ratio is larger than one, yet the posterior remains small because the prior odds were extremely small.

## 4. Monte Carlo Estimation

Monte Carlo methods matter because many exact probabilistic quantities are expectations, and expectations are averages. Once that connection is understood, simulation stops looking like a separate numerical trick and starts looking like an empirical version of the same mathematical object. The computational question is no longer "Can I calculate the expectation symbolically?" but "If I can sample from the model, what average of those samples is estimating the quantity I care about?"

This is also why Monte Carlo can serve as a conceptual check, not only a numerical approximation. If a symbolic mean, posterior expectation, or transformed-distribution claim is correct, then repeated simulation should drift toward it. A simulation does not prove a theorem, but it is often the fastest way to discover that one has misunderstood the meaning of the exact expression.

### Worked Example: Bernoulli Mean

If $X \sim \mathrm{Bernoulli}(0.3)$, then the exact expectation is

$$\mathbb{E}[X]=0.3.$$

Suppose a small simulation produces the ten outcomes

$$1,0,0,1,0,0,0,1,0,0.$$

Then the empirical mean is

$$\hat{\mu}_{10}=\frac{3}{10}=0.3.$$

A different run might produce $0.2$ or $0.4$ instead, because ten samples is still small. The computational point is that the empirical frequency of ones is itself a Monte Carlo estimate of the Bernoulli mean. The exact expectation and the MLE are connected by the same averaging operation.

### Worked Example: Monte Carlo Expectation for a Die

For a fair die,

$$\mathbb{E}[X]=3.5.$$

If a simulation produces the six values

$$2,5,1,6,3,4,$$

then the empirical mean is

$$\hat{\mu}_6=\frac{2+5+1+6+3+4}{6}=3.5.$$

That exact match is accidental, not guaranteed. The important check is that as more rolls are accumulated, the running average should drift toward $3.5$ rather than away from it.

### Sampling and Plotting Workflow

Sampling is often treated as if it were separate from theory, but a plot is only useful if it is read against the theoretical structure of the distribution. A histogram is not just a picture of samples. It is an empirical approximation to a PMF or density, and the reader should therefore already know what broad shape is plausible before plotting anything.

That means the workflow should begin before the plot is drawn. First fix the random seed if reproducibility matters. Then identify the support of the distribution, because support determines the acceptable sample range and the correct visual style. Continuous distributions should usually be displayed with contiguous bins over an interval. Discrete integer-valued distributions should be plotted with bins aligned to integer locations so that separate mass points do not get blurred into a fake continuous shape.

After plotting, the first checks should be conceptual rather than cosmetic. Does the sample stay inside the support? Is the center roughly where the mean suggests it should be? Does the skewness match the theoretical shape? Is the plot jagged because the distribution is genuinely irregular, or because the bin choice is too aggressive for the sample size? When a histogram contradicts the basic theory, the usual causes are incorrect parameterization, mistaken support, an unsuitable plotting choice, or a misunderstanding of what was actually sampled.

### Worked Example: Beta$(3,2)$ Samples

The Beta$(3,2)$ law is continuous on the interval $[0,1]$. Its density is proportional to

$$x^2(1-x).$$

That immediately implies several qualitative facts. The support is only the unit interval, so no sampled value should fall below $0$ or above $1$. The density is zero at both boundaries, so the histogram should taper toward both ends rather than spike exactly at $0$ or $1$. The mean is

$$\frac{3}{3+2}=0.6,$$

and the mode is

$$\frac{3-1}{3+2-2}=\frac{2}{3},$$

so the histogram should peak somewhat to the right of the center, around $0.6$ to $0.7$.

For $1000$ samples, a moderate number of bins is usually best. Too few bins hide the shape, while too many bins make the plot look noisy and can suggest fake structure. A practical target is to choose enough bins to reveal the single interior peak while keeping adjacent bars reasonably smooth. If the histogram is wildly jagged, the bin count is probably too large for only $1000$ samples.

### Worked Example: Geometric$(0.2)$ Samples

Under the zero-based convention often used in probabilistic programming, the Geometric distribution uses the zero-based convention:

$$p(X=x)=(1-0.2)^x(0.2), \qquad x \in \{0,1,2,\dots\}.$$

So a sampled value of $0$ means success occurred on the first trial, a sampled value of $1$ means one failure occurred before the first success, and so on. The first few probabilities are

$$p(0)=0.2,\qquad p(1)=0.16,\qquad p(2)=0.128,\qquad p(3)=0.1024.$$

The histogram should therefore start high at zero and then decrease steadily as the value grows. It should be right-skewed with a visibly long tail.

The theoretical mean under this convention is

$$\frac{1-0.2}{0.2}=4.$$

So while many samples will be small integers, the average over $1000$ draws should be somewhere near $4$. That does not mean most samples equal $4$; it means the long right tail pulls the average to the right even though the most likely outcome is still $0$.

The histogram for a Geometric sample should use bins centered on the integers. If the plotting routine uses wide floating-point bins, the plot can blur together distinct mass points and make a discrete law look falsely continuous. The right visual target is a descending bar chart over the nonnegative integers, not a smooth bell-shaped curve.

### Sampling Audit for the Homework Plots

- check that the Beta samples all lie in $[0,1]$
- check that the Geometric samples are nonnegative integers
- check that the Beta histogram has one interior peak near $0.6$ to $0.7$
- check that the Geometric histogram is tallest at $0$ and decays to the right
- check that the plotted axes are labeled so the reader can see which distribution and which support is being shown

## 5. Likelihood and Log-Likelihood Sweeps

A likelihood sweep is one of the best numerical ways to make estimation concrete. Instead of jumping immediately to calculus, one evaluates the likelihood across a grid of parameter values and watches which values score the observed data more strongly. That turns estimation into a visible landscape rather than a symbolic derivation.

This is especially useful because the conceptual difficulty of likelihood is not the formula itself. It is the role reversal. The data are fixed because they have already been observed. The parameter varies because different candidate settings are being compared. A likelihood sweep makes that role reversal tangible: nothing about the dataset changes from row to row, and only the candidate parameter value changes.

The log-likelihood should usually be treated as the default computational form. It preserves the ranking of parameter values because the logarithm is monotone, but it turns products into sums, which makes both differentiation and numerical stability much better behaved. The mathematical content is unchanged. What changes is that the calculation no longer collapses when many small factors are multiplied together.

For Bernoulli data

$$D=\{1,0,1\},$$

the likelihood is

$$L(\rho)=\rho^2(1-\rho).$$

Evaluating a few candidate values gives

| $\rho$ | $L(\rho)$ | $\log L(\rho)$ |
|---|---:|---:|
| 0.2 | 0.032 | $-3.442$ |
| 0.5 | 0.125 | $-2.079$ |
| 0.8 | 0.128 | $-2.056$ |

The ranking is identical whether one compares likelihood or log-likelihood, because the logarithm is monotone. But the log version is numerically safer and algebraically easier to differentiate.

### Why Logs Matter

The point of taking logs is not stylistic elegance. It is to preserve information that ordinary floating-point arithmetic may otherwise erase. If $100$ independent terms each contribute a factor near $0.01$, the raw product is roughly $10^{-200}$, which is so small that a computer may treat it as zero. But the log-likelihood is roughly $100\log(0.01)$, which is a perfectly manageable negative number. The model has not become more probable or less probable because of the logarithm. The same comparison is being represented in a numerically safer language.

### Worked Example: Gaussian Mean Sweep

For Gaussian observations

$$D=\{-0.5,0.4,1.3\}$$

with variance fixed at one, the log-likelihood in $\mu$ differs from

$$-\frac{1}{2}\sum_i (x^{(i)}-\mu)^2$$

only by an additive constant. A parameter sweep over candidate means is therefore just a sweep over total squared error. The maximizing mean should coincide with the sample mean

$$\bar{x}=0.4.$$

That is the numerical reason the Gaussian MLE is the arithmetic average.

This section should remain in the appendix as a reusable workflow, but the core conceptual lesson about likelihood, log-likelihood, and what is held fixed should also appear in `02_probability_06_learning_and_parameter_estimation`. The appendix version is the operational summary; the main lesson should carry the first full explanation.

## 6. Sequential Bayesian Updating

Bayesian updating becomes computationally simple when the posterior remains in the same family as the prior. In that case, inference no longer requires recomputing everything from scratch or performing a difficult integral each time new data arrive. Instead, the update can often be recorded as parameter arithmetic. That simplicity is not a coincidence. It is the computational payoff of conjugacy.

The important conceptual point is that sequential updating and batch updating should agree whenever the model assumptions stay fixed. Learning from the first batch and then the second batch should lead to the same posterior as learning from the combined dataset in one step. If those two routes disagree, either the bookkeeping is wrong or the underlying model changed between updates.

### Worked Example: Beta-Bernoulli Updating

Start with

$$\rho \sim \mathrm{Beta}(2,2).$$

Interpret this as prior pseudo-counts of two heads and two tails. After observing

$$D_1=\{1,0,1\},$$

the posterior is

$$\mathrm{Beta}(4,3).$$

If a second batch

$$D_2=\{1,1\}$$

arrives, the update becomes

$$\mathrm{Beta}(6,3).$$

The entire computation can be recorded as a simple count table:

| stage | prior head count | prior tail count | observed heads | observed tails | updated state |
|---|---:|---:|---:|---:|---:|
| initial prior | 2 | 2 | 0 | 0 | $(2,2)$ |
| after $D_1$ | 2 | 2 | 2 | 1 | $(4,3)$ |
| after $D_2$ | 4 | 3 | 2 | 0 | $(6,3)$ |

This table view makes it obvious that sequential and batch updating agree whenever the model assumptions do not change.

### Worked Example: Dirichlet-Categorical Updating

Let the prior be

$$\theta \sim \mathrm{Dir}(2,2,2),$$

and suppose the observed class counts are

$$(3,1,0).$$

Then the posterior is

$$\mathrm{Dir}(5,3,2).$$

The corresponding posterior mean is

$$(\frac{5}{10},\frac{3}{10},\frac{2}{10})=(0.5,0.3,0.2).$$

The unobserved third category still keeps positive mass because the prior prevented the model from collapsing its probability to zero after only four observations.

## 7. Entropy and KL in Numerical Form

Entropy and KL divergence are easy to state and easy to miscompute. The formulas are short, but they are fragile with respect to support mismatches and zero entries, so the main computational difficulty is not algebraic complexity. It is respecting the conditions under which the formulas are meaningful.

Entropy measures uncertainty internal to a single distribution. KL divergence measures how badly one distribution would stand in for another. Those are different jobs, and the numerical checks should reflect that difference. Entropy only requires a valid normalized distribution. KL requires two distributions on a common support, and it is especially sensitive to cases where the reference distribution assigns zero mass to events that the target distribution considers possible.

For a discrete distribution $p$, entropy is

$$H(p)=-\sum_i p_i \log p_i.$$

For two distributions $p$ and $q$ on the same support, KL divergence is

$$D(p \,\|\, q)=\sum_i p_i \log \frac{p_i}{q_i}.$$

### Worked Example: Entropy

For

$$p=(0.9,0.1),$$

the entropy in bits is

$$H(p)= -0.9\log_2 0.9 - 0.1\log_2 0.1 \approx 0.469.$$

This is smaller than the fair-coin value of one bit because the outcome is more predictable.

### Worked Example: KL Asymmetry

Let

$$p=(0.8,0.2), \qquad q=(0.5,0.5).$$

Then

$$D(p \,\|\, q) = 0.8 \log \frac{0.8}{0.5} + 0.2 \log \frac{0.2}{0.5} \approx 0.193$$

when natural logarithms are used. Reversing the arguments gives

$$D(q \,\|\, p) = 0.5 \log \frac{0.5}{0.8} + 0.5 \log \frac{0.5}{0.2} \approx 0.223.$$

The two numbers differ, so KL divergence is not symmetric.

### Support Audit

Before evaluating KL divergence, check each state with $p_i>0$. If any corresponding $q_i=0$, then

$$D(p \,\|\, q)=\infty.$$

That is not a numerical nuisance but a mathematically meaningful statement: $q$ declared impossible an outcome that actually occurs under $p$.

## 8. Change of Variables and Jacobian Checks

The computational purpose of a change-of-variables formula is to preserve probability mass when the coordinate system has changed. A transformed density should not be thought of as the old density with symbols renamed. It must be corrected for the way the transformation locally stretches or compresses space. The Jacobian term is exactly that correction.

For scalar transforms, the workflow is best read as a sequence of conceptual checks.

First identify the region on which the transformation is being treated as invertible. This matters because the naive one-branch formula fails if several source points map to the same destination point.

Second write the inverse map on that region. The density at a destination point must be computed by tracing that point back to where it came from under the original variable.

Third differentiate the inverse map. This derivative measures how intervals in the transformed coordinate correspond to intervals in the original coordinate.

Fourth evaluate the base density at the inverse point and multiply by the absolute derivative. The absolute value is essential because density must stay nonnegative even when the transformation reverses orientation.

### Worked Example: Linear Rescaling

Let $Z$ be uniform on $[0,1]$ and define

$$X=3Z.$$

The inverse is

$$z=\frac{x}{3},$$

and the derivative of the inverse is

$$\frac{dz}{dx}=\frac{1}{3}.$$

Since the base density is $1$ on $[0,1]$, the transformed density is

$$p_X(x)=\frac{1}{3}$$

on $[0,3]$. Stretching the support by a factor of three compresses the density by the same factor.

### Worked Example: Triangular Jacobian in a Flow Layer

For the affine coupling layer

$$Z_1' = Z_1, \qquad Z_2' = \alpha_1(Z_1)Z_2 + \beta_1(Z_1),$$

the Jacobian matrix is triangular:

$$J_{11}=1,\qquad J_{12}=0,\qquad J_{21}=\frac{\partial Z_2'}{\partial Z_1},\qquad J_{22}=\alpha_1(Z_1).$$

Its determinant is therefore just

$$\det J = \alpha_1(Z_1).$$

The lower-left derivative may be algebraically messy, but it does not affect the determinant. This is the implementation reason triangular layers are popular: they preserve expressive transforms while keeping exact density evaluation cheap.

This section should remain in the appendix because the audit is reusable, but the first real conceptual explanation of why Jacobians appear should live in `02_probability_09_change_of_variable_models`. The appendix version is where the reader checks an implementation. The main lesson is where the reader should first understand why local stretching changes density values at all.

## 9. End-to-End Probability Audit

The most reliable way to catch probability bugs is not to rely on memory of formulas but to run a short object-level audit. Each item in the checklist below corresponds to a structural property that the quantity must satisfy if it has been computed correctly.

### Probability Objects

- does the full discrete table sum to one
- does every conditional distribution sum to one over the correct axis
- is every density nonnegative on its stated support
- is every support restriction stated explicitly

### Likelihood and Estimation

- is the likelihood treated as a function of the parameter rather than of the observed data
- are log-likelihoods used when products of many small numbers appear
- do the MLE or MAP candidates satisfy the relevant domain constraints

### Bayesian Updating

- does the evidence term equal the sum or integral of the unnormalized posterior kernel
- in conjugate models, do prior pseudo-counts and observed counts add coordinatewise
- do posterior means remain inside the valid parameter domain

### Information Theory

- are all probability vectors normalized before entropy or KL calculations
- are zero-probability states handled correctly
- is the support condition for KL checked before numeric evaluation

### Change of Variables

- is the transformation invertible on the modeled region
- is the Jacobian determinant nonzero on that region
- if the map is triangular, is the determinant computed from the diagonal entries only

This appendix is intentionally narrower than the main lessons. It is not the place where the reader should first struggle to understand conditioning, likelihood, Bayesian updating, entropy, or Jacobian correction. Those ideas need their own slower conceptual development in the lessons themselves.

Its job is different. Once the conceptual meaning of the object is known, the appendix makes the numerical structure explicit enough that the object can be computed, checked, and debugged systematically. In that sense, it is best read not as a second textbook chapter, but as a practical companion to one.

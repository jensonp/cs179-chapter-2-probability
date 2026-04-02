# Probability and Inference: Computational Appendix

Source: ../notes/02_probability_reconstructed/source/02_probability.pdf

This appendix translates the chapter into numerical workflows. It is not a programming-language tutorial, and it does not use code listings. Instead, it states the quantities to store, the checks to run, the formulas to evaluate, and the interpretation of the results. The goal is to make the chapter executable in a spreadsheet, numerical notebook, or ordinary programming language without leaving important implementation details implicit.

## 1. Notation and Numerical Conventions

The chapter uses three related but different kinds of objects:

- $P(A)$ for the probability of an event $A$
- $p(x)$ or $p(x,y)$ for a probability mass function or density evaluated at specific states
- $F_X(x)$ for a cumulative distribution function

These should not be conflated computationally. An event probability is a sum or integral over a set. A PMF or PDF is a local quantity attached to a state. A CDF is an accumulated probability. If an implementation mixes those roles, the numbers may still look plausible while meaning the wrong thing.

Likelihood notation has its own role. For observed data $D$ and parameter $\theta$,

$$ L(\theta)=p(D \mid \theta) $$

is treated as a function of $\theta$ with $D$ fixed. It is therefore a scoring function for parameter values, not a probability distribution over parameters.

Floating-point computations introduce two recurring issues. First, quantities that should sum to one may come out as $0.999999$ or $1.000001$ because of rounding. Second, products of many small probabilities can underflow to zero numerically even when the true value is positive. For that reason, one should explicitly normalize probability vectors after accumulation steps and use log-likelihoods rather than raw likelihood products when sample sizes become moderate or large.

## 2. Finite Probability Tables

For a finite discrete model, the computational primitive is usually a table of nonnegative numbers whose entries sum to one. If the model is joint over several variables, each axis corresponds to one variable. All marginal, conditional, and posterior quantities in the discrete part of the chapter are built from three operations:

1. Restrict to rows consistent with observed evidence.
2. Sum out hidden coordinates.
3. Renormalize the remaining vector so it sums to one.

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

$$ 0.576+0.008+0.144+0.072+0.064+0.012+0.016+0.108=1. $$

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

$$ 0.080+0.120=0.200. $$

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

The scalar Bayes formula is often numerically less transparent than the odds form. For two hypotheses $H_1$ and $H_0$ and evidence $E$,

$$ \frac{p(H_1 \mid E)}{p(H_0 \mid E)} = \frac{p(E \mid H_1)}{p(E \mid H_0)} \cdot \frac{p(H_1)}{p(H_0)}. $$

This should be computed as three separate pieces:

1. prior odds
2. likelihood ratio
3. posterior odds

### Worked Example: Medical Screening

Suppose

$$ p(D=1)=0.01, \qquad p(T=+ \mid D=1)=0.95, \qquad p(T=+ \mid D=0)=0.10. $$

The prior odds of disease are

$$ \frac{0.01}{0.99}\approx 0.0101. $$

The likelihood ratio of a positive test is

$$ \frac{0.95}{0.10}=9.5. $$

So the posterior odds are

$$ 9.5 \times 0.0101 \approx 0.096. $$

Converting odds back to a probability gives

$$ \frac{0.096}{1+0.096}\approx 0.0876. $$

This computation is the same as the direct posterior formula, but it makes the structure more explicit. The evidence is favorable, because the likelihood ratio is larger than one, yet the posterior remains small because the prior odds were extremely small.

## 4. Monte Carlo Estimation

Monte Carlo estimation replaces exact expectations by empirical averages from simulated samples. If

$$ X^{(1)},\dots,X^{(m)} $$

are samples from a model, then the empirical estimate of the mean is

$$ \hat{\mu}_m=\frac{1}{m}\sum_{i=1}^m X^{(i)}. $$

The law of large numbers says that this quantity should stabilize near $E[X]$ as $m$ grows. The practical purpose of the simulation is not merely to approximate a number, but to develop intuition for which exact formulas are averages in disguise.

### Worked Example: Bernoulli Mean

If $X \sim \mathrm{Bernoulli}(0.3)$, then the exact expectation is

$$ E[X]=0.3. $$

Suppose a small simulation produces the ten outcomes

$$ 1,0,0,1,0,0,0,1,0,0. $$

Then the empirical mean is

$$ \hat{\mu}_{10}=\frac{3}{10}=0.3. $$

A different run might produce $0.2$ or $0.4$ instead, because ten samples is still small. The computational point is that the empirical frequency of ones is itself a Monte Carlo estimate of the Bernoulli mean. The exact expectation and the MLE are connected by the same averaging operation.

### Worked Example: Monte Carlo Expectation for a Die

For a fair die,

$$ E[X]=3.5. $$

If a simulation produces the six values

$$ 2,5,1,6,3,4, $$

then the empirical mean is

$$ \hat{\mu}_6=\frac{2+5+1+6+3+4}{6}=3.5. $$

That exact match is accidental, not guaranteed. The important check is that as more rolls are accumulated, the running average should drift toward $3.5$ rather than away from it.

### Homework Workflow: Sampling and Plotting

The Chapter 2 homework asks for sampled histograms rather than symbolic derivations. The computational logic should therefore be stated explicitly.

First, fix the random seed before drawing any samples so that the results are reproducible. In the course notebook, the seed is $123$, and that fixed seed should be preserved. Second, choose the distribution parameters and draw the requested number of independent samples. Third, inspect the raw sample range before plotting, because the support determines the correct histogram style. Continuous samples should usually be plotted with contiguous bins over an interval. Discrete integer-valued samples should be plotted with bins aligned to integer locations rather than with arbitrary floating-point boundaries.

A histogram is not just a picture; it is an empirical approximation to a PMF or density. So after plotting, one should compare the histogram to basic theoretical checks such as support, center, skewness, and rough scale. If the picture contradicts those simple checks, the issue is usually a parameterization mistake, a sampling mistake, or an inappropriate bin choice.

### Worked Example: Beta$(3,2)$ Samples

The Beta$(3,2)$ law is continuous on the interval $[0,1]$. Its density is proportional to

$$ x^2(1-x). $$

That immediately implies several qualitative facts. The support is only the unit interval, so no sampled value should fall below $0$ or above $1$. The density is zero at both boundaries, so the histogram should taper toward both ends rather than spike exactly at $0$ or $1$. The mean is

$$ \frac{3}{3+2}=0.6, $$

and the mode is

$$ \frac{3-1}{3+2-2}=\frac{2}{3}, $$

so the histogram should peak somewhat to the right of the center, around $0.6$ to $0.7$.

For $1000$ samples, a moderate number of bins is usually best. Too few bins hide the shape, while too many bins make the plot look noisy and can suggest fake structure. A practical target is to choose enough bins to reveal the single interior peak while keeping adjacent bars reasonably smooth. If the histogram is wildly jagged, the bin count is probably too large for only $1000$ samples.

### Worked Example: Geometric$(0.2)$ Samples

For the homework's Pyro workflow, the Geometric distribution uses the zero-based convention:

$$ p(X=x)=(1-0.2)^x(0.2), \qquad x \in \{0,1,2,\dots\}. $$

So a sampled value of $0$ means success occurred on the first trial, a sampled value of $1$ means one failure occurred before the first success, and so on. The first few probabilities are

$$ p(0)=0.2,\qquad p(1)=0.16,\qquad p(2)=0.128,\qquad p(3)=0.1024. $$

The histogram should therefore start high at zero and then decrease steadily as the value grows. It should be right-skewed with a visibly long tail.

The theoretical mean under this convention is

$$ \frac{1-0.2}{0.2}=4. $$

So while many samples will be small integers, the average over $1000$ draws should be somewhere near $4$. That does not mean most samples equal $4$; it means the long right tail pulls the average to the right even though the most likely outcome is still $0$.

The histogram for a Geometric sample should use bins centered on the integers. If the plotting routine uses wide floating-point bins, the plot can blur together distinct mass points and make a discrete law look falsely continuous. The right visual target is a descending bar chart over the nonnegative integers, not a smooth bell-shaped curve.

### Sampling Audit for the Homework Plots

- check that the Beta samples all lie in $[0,1]$
- check that the Geometric samples are nonnegative integers
- check that the Beta histogram has one interior peak near $0.6$ to $0.7$
- check that the Geometric histogram is tallest at $0$ and decays to the right
- check that the plotted axes are labeled so the reader can see which distribution and which support is being shown

## 5. Likelihood and Log-Likelihood Sweeps

Likelihood surfaces are easiest to understand numerically by evaluating them on a parameter grid. For Bernoulli data

$$ D=\{1,0,1\}, $$

the likelihood is

$$ L(\rho)=\rho^2(1-\rho). $$

Evaluating a few candidate values gives

| $\rho$ | $L(\rho)$ | $\log L(\rho)$ |
|---|---:|---:|
| 0.2 | 0.032 | $-3.442$ |
| 0.5 | 0.125 | $-2.079$ |
| 0.8 | 0.128 | $-2.056$ |

The ranking is identical whether one compares likelihood or log-likelihood, because the logarithm is monotone. But the log version is numerically safer and algebraically easier to differentiate.

### Why Logs Matter

Suppose $m=100$ independent observations each contribute a factor near $0.01$. The raw product is roughly

$$ 10^{-200}, $$

which is numerically tiny. The corresponding log-likelihood is roughly

$$ 100 \log(0.01), $$

which is a moderate negative number rather than an underflowed zero. The computation is the same in mathematical content, but the log representation is far more stable.

### Worked Example: Gaussian Mean Sweep

For Gaussian observations

$$ D=\{-0.5,0.4,1.3\} $$

with variance fixed at one, the log-likelihood in $\mu$ differs from

$$ -\frac{1}{2}\sum_i (x^{(i)}-\mu)^2 $$

only by an additive constant. A parameter sweep over candidate means is therefore just a sweep over total squared error. The maximizing mean should coincide with the sample mean

$$ \bar{x}=0.4. $$

That is the numerical reason the Gaussian MLE is the arithmetic average.

## 6. Sequential Bayesian Updating

Bayesian updates are computationally attractive when the posterior stays in the same family as the prior. Then the update becomes simple parameter arithmetic rather than numerical integration.

### Worked Example: Beta-Bernoulli Updating

Start with

$$ \rho \sim \mathrm{Beta}(2,2). $$

Interpret this as prior pseudo-counts of two heads and two tails. After observing

$$ D_1=\{1,0,1\}, $$

the posterior is

$$ \mathrm{Beta}(4,3). $$

If a second batch

$$ D_2=\{1,1\} $$

arrives, the update becomes

$$ \mathrm{Beta}(6,3). $$

The entire computation can be recorded as a simple count table:

| stage | prior head count | prior tail count | observed heads | observed tails | updated state |
|---|---:|---:|---:|---:|---:|
| initial prior | 2 | 2 | 0 | 0 | $(2,2)$ |
| after $D_1$ | 2 | 2 | 2 | 1 | $(4,3)$ |
| after $D_2$ | 4 | 3 | 2 | 0 | $(6,3)$ |

This table view makes it obvious that sequential and batch updating agree whenever the model assumptions do not change.

### Worked Example: Dirichlet-Categorical Updating

Let the prior be

$$ \theta \sim \mathrm{Dir}(2,2,2), $$

and suppose the observed class counts are

$$ (3,1,0). $$

Then the posterior is

$$ \mathrm{Dir}(5,3,2). $$

The corresponding posterior mean is

$$ (\frac{5}{10},\frac{3}{10},\frac{2}{10})=(0.5,0.3,0.2). $$

The unobserved third category still keeps positive mass because the prior prevented the model from collapsing its probability to zero after only four observations.

## 7. Entropy and KL in Numerical Form

For a discrete distribution $p$, entropy is

$$ H(p)=-\sum_i p_i \log p_i. $$

For two distributions $p$ and $q$ on the same support, KL divergence is

$$ D(p \,\|\, q)=\sum_i p_i \log \frac{p_i}{q_i}. $$

The computational hazard is not the formula itself but support mismatches and zero entries.

### Worked Example: Entropy

For

$$ p=(0.9,0.1), $$

the entropy in bits is

$$ H(p)= -0.9\log_2 0.9 - 0.1\log_2 0.1 \approx 0.469. $$

This is smaller than the fair-coin value of one bit because the outcome is more predictable.

### Worked Example: KL Asymmetry

Let

$$ p=(0.8,0.2), \qquad q=(0.5,0.5). $$

Then

$$ D(p \,\|\, q) = 0.8 \log \frac{0.8}{0.5} + 0.2 \log \frac{0.2}{0.5} \approx 0.193 $$

when natural logarithms are used. Reversing the arguments gives

$$ D(q \,\|\, p) = 0.5 \log \frac{0.5}{0.8} + 0.5 \log \frac{0.5}{0.2} \approx 0.223. $$

The two numbers differ, so KL divergence is not symmetric.

### Support Audit

Before evaluating KL divergence, check each state with $p_i>0$. If any corresponding $q_i=0$, then

$$ D(p \,\|\, q)=\infty. $$

That is not a numerical nuisance but a mathematically meaningful statement: $q$ declared impossible an outcome that actually occurs under $p$.

## 8. Change of Variables and Jacobian Checks

For scalar transforms, the computational recipe is:

1. write the inverse map
2. differentiate the inverse
3. evaluate the base density at the inverse point
4. multiply by the absolute derivative

### Worked Example: Linear Rescaling

Let $Z$ be uniform on $[0,1]$ and define

$$ X=3Z. $$

The inverse is

$$ z=\frac{x}{3}, $$

and the derivative of the inverse is

$$ \frac{dz}{dx}=\frac{1}{3}. $$

Since the base density is $1$ on $[0,1]$, the transformed density is

$$ p_X(x)=\frac{1}{3} $$

on $[0,3]$. Stretching the support by a factor of three compresses the density by the same factor.

### Worked Example: Triangular Jacobian in a Flow Layer

For the affine coupling layer

$$ Z_1' = Z_1, \qquad Z_2' = \alpha_1(Z_1)Z_2 + \beta_1(Z_1), $$

the Jacobian matrix is triangular:

$$ J_{11}=1,\qquad J_{12}=0,\qquad J_{21}=\frac{\partial Z_2'}{\partial Z_1},\qquad J_{22}=\alpha_1(Z_1). $$

Its determinant is therefore just

$$ \det J = \alpha_1(Z_1). $$

The lower-left derivative may be algebraically messy, but it does not affect the determinant. This is the implementation reason triangular layers are popular: they preserve expressive transforms while keeping exact density evaluation cheap.

## 9. End-to-End Probability Audit

The most reliable way to catch model bugs is to use a short checklist on every example or implementation:

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

This appendix does not replace the theory in the main note or the proofs in the formal supplement. Its role is narrower and practical: it makes the numerical structure of the chapter explicit enough that each concept can be checked, implemented, and debugged systematically.

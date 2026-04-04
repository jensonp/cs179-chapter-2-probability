# 2.3 Learning and Parameter Estimation

Sections 2.1 and 2.2 asked **forward** probability questions: once a model is known, what probabilities or densities does it assign to events and outcomes?  
Section 2.3 asks the **inverse** question: after data have been observed, which parameter values or model classes are supported by the data?

That shift changes the role of the objects without changing their names.

- The **data** now serve as the fixed input.
- The **parameters** are the unknown quantities we want to estimate or infer.
- The **model class** may itself become an object of comparison if we are deciding between simpler and more flexible explanations.

The cleanest way to organize this section is to keep one checklist visible:

1. What is fixed?
2. What is allowed to vary?
3. What object are we computing?
4. What question does that object answer?

That checklist is what keeps probability, likelihood, posterior distributions, and model evidence from being blurred together.

## The sampling model and the role of i.i.d. data

Let the observed sample be

$$
D = \bigl(x^{(1)}, x^{(2)}, \dots, x^{(m)}\bigr).
$$

We use sequence notation rather than set notation because the sample may contain repeated values, and the analysis concerns the realized collection of observations rather than an unordered mathematical set.

Suppose the model is indexed by a parameter $\theta$.  
Under the i.i.d. assumption, the observations are:

- **independent** once $\theta$ is fixed, so learning one observation does not change the conditional law of the others;
- **identically distributed**, so each observation comes from the same distribution $p(x \mid \theta)$.

Under that assumption, the joint sampling law factorizes as

$$
p(D \mid \theta)
= \prod_{i=1}^{m} p\bigl(x^{(i)} \mid \theta\bigr).
$$

This factorization is the structural reason likelihood and log-likelihood are manageable.  
Without it, dependence terms would have to be modeled explicitly.

## Likelihood

The likelihood uses the same algebraic expression $p(D \mid \theta)$, but it answers a different question from forward probability.

- In the **sampling-model** view, $\theta$ is fixed and $D$ is the random object.
- In the **likelihood** view, the sample $D$ has already been observed and is now treated as fixed, while $\theta$ varies.

So likelihood should be read as a score over parameter values for one realized data set:

$$
L(\theta; D) = p(D \mid \theta).
$$

For i.i.d. data,

$$
L(\theta; D)
= \prod_{i=1}^{m} p\bigl(x^{(i)} \mid \theta\bigr).
$$

The log-likelihood is

$$
\ell(\theta)
= \log L(\theta; D)
= \sum_{i=1}^{m} \log p\bigl(x^{(i)} \mid \theta\bigr).
$$

Taking logs does **not** change which parameter value maximizes the objective, because the logarithm is strictly increasing.  
It only turns products into sums.

That matters for three reasons:

1. sums are easier to differentiate than products;
2. contributions from individual observations become explicit;
3. the large-sample structure becomes easier to interpret.

### What likelihood does and does not say

A large likelihood means the candidate parameter makes the observed sample comparatively less surprising under the model.  
A small likelihood means it makes the observed sample comparatively more surprising.

This is a **relative** statement.  
Likelihood ranks parameter values for the same observed sample under the same model.  
By itself it does not:

- prove that one parameter is the true one;
- quantify the uncertainty remaining after the sample is seen;
- define a probability distribution over parameter values.

Those last two tasks require additional structure such as confidence procedures, asymptotic theory, or a Bayesian posterior distribution.

## Probability versus likelihood

This distinction is one of the most important boundaries in the chapter.

Take a Bernoulli model with head probability $\rho$.  
For one observation $x \in \{0,1\}$,

$$
p(x \mid \rho) = \rho^x(1-\rho)^{1-x}.
$$

If $\rho$ is fixed and $x$ varies, this is an ordinary probability model over data.  
The two possible outcomes satisfy

$$
p(x=1 \mid \rho)=\rho,
\qquad
p(x=0 \mid \rho)=1-\rho,
$$

and these add to one.

If instead the observation is already fixed and $\rho$ varies, then the same formula is a likelihood function in $\rho$.  
For example, after observing $x=1$,

$$
L(\rho; x=1)=\rho.
$$

This does **not** define a probability density over $\rho$.  
Its role is only to compare candidate values of $\rho$ for the fixed observation.

The mental checklist is therefore:

- **probability mode**: parameter fixed, data vary;
- **likelihood mode**: data fixed, parameter varies.

## Example: Bernoulli likelihood

Suppose we observe the three-flip sample

$$
D=(1,0,1).
$$

Under a Bernoulli model with parameter $\rho$,

$$
L(\rho; D)
= \rho(1-\rho)\rho
= \rho^2(1-\rho).
$$

This factorization should be read mechanically:

- each observed success contributes a factor $\rho$;
- each observed failure contributes a factor $(1-\rho)$;
- the full likelihood is the product of those terms.

Compare three candidate values:

$$
L(0.2; D)=0.2^2(0.8)=0.032,
$$

$$
L(0.5; D)=0.5^2(0.5)=0.125,
$$

$$
L(0.8; D)=0.8^2(0.2)=0.128.
$$

The sample contains two successes in three trials, so values that make success reasonably common fit the observed sequence better than values that make success rare.

That comparison must still be interpreted carefully.  
The fact that $0.128 > 0.125 > 0.032$ means only that, **for this sample and this model**, $\rho=0.8$ makes the data more compatible than $\rho=0.5$, and much more compatible than $\rho=0.2$.  
It does not prove that the true parameter is exactly $0.8$.

### Why likelihood is not a probability distribution over parameters

For the same sample,

$$
L(\rho; D)=\rho^2(1-\rho).
$$

Integrating over $\rho \in [0,1]$ gives

$$
\int_0^1 \rho^2(1-\rho)\,d\rho
=
\int_0^1 (\rho^2-\rho^3)\,d\rho
=
\left[\frac{\rho^3}{3}-\frac{\rho^4}{4}\right]_0^1
=
\frac{1}{12},
$$

not $1$.

That is the exact check showing likelihood is not a probability density over the parameter space.  
It was never designed to answer

$$
\text{“What is the probability that the parameter lies near this value?”}
$$

It answers a different question:

$$
\text{“If this were the parameter value, how compatible would the observed data be with it?”}
$$

## Maximum likelihood estimation

Maximum likelihood estimation chooses the parameter value that maximizes the likelihood, or equivalently the log-likelihood:

$$
\hat{\theta}_{\mathrm{MLE}}
=
\arg\max_{\theta} L(\theta; D)
=
\arg\max_{\theta} \ell(\theta).
$$

This is a **point estimate**.  
It collapses the data-fit information to one selected parameter value.

The generic MLE pattern is always the same:

1. write the likelihood or log-likelihood;
2. simplify it using the model structure;
3. differentiate or otherwise optimize;
4. solve the stationary condition and check the domain;
5. interpret the result.

## Example: Bernoulli MLE

Suppose $D=(x^{(1)},\dots,x^{(m)})$ is a Bernoulli sample with

- $m_1$ observed ones,
- $m_0$ observed zeros,
- $m = m_1 + m_0$.

Then

$$
L(\rho; D)=\rho^{m_1}(1-\rho)^{m_0},
$$

and

$$
\ell(\rho)=m_1 \log \rho + m_0 \log(1-\rho).
$$

Differentiate:

$$
\frac{d\ell}{d\rho}
=
\frac{m_1}{\rho}
-
\frac{m_0}{1-\rho}.
$$

Set the derivative to zero:

$$
\frac{m_1}{\rho}
=
\frac{m_0}{1-\rho}.
$$

Rearranging gives

$$
m_1(1-\rho)=m_0\rho
\quad\Longrightarrow\quad
m_1 = (m_0+m_1)\rho = m\rho.
$$

So the MLE is

$$
\hat{\rho}_{\mathrm{MLE}}=\frac{m_1}{m}.
$$

This estimate says: under Bernoulli likelihood, the parameter that best fits the observed data is the empirical fraction of successes.

## Example: Gaussian MLE

Let $x^{(1)},\dots,x^{(m)}$ be i.i.d. Gaussian with mean $\mu$ and variance $\sigma^2$.

### Mean unknown, variance known

If $\sigma^2$ is known, the log-likelihood as a function of $\mu$ is

$$
\ell(\mu)
=
-\frac{m}{2}\log(2\pi\sigma^2)
-
\frac{1}{2\sigma^2}\sum_{i=1}^{m}(x^{(i)}-\mu)^2.
$$

Only the quadratic term depends on $\mu$, so maximizing the log-likelihood is equivalent to minimizing

$$
\sum_{i=1}^{m}(x^{(i)}-\mu)^2.
$$

Differentiating and setting the derivative to zero gives

$$
\hat{\mu}_{\mathrm{MLE}}
=
\frac{1}{m}\sum_{i=1}^{m}x^{(i)}.
$$

So the sample mean is the MLE for the Gaussian mean.

### Mean and variance both unknown

When both $\mu$ and $\sigma^2$ are unknown, the MLEs are

$$
\hat{\mu}_{\mathrm{MLE}}
=
\frac{1}{m}\sum_{i=1}^{m}x^{(i)},
$$

$$
\hat{\sigma}^2_{\mathrm{MLE}}
=
\frac{1}{m}\sum_{i=1}^{m}\bigl(x^{(i)}-\hat{\mu}_{\mathrm{MLE}}\bigr)^2.
$$

The denominator here is $m$, not $m-1$.  
That distinction matters.

- The MLE chooses the variance that maximizes the likelihood.
- The classical unbiased variance estimator uses $m-1$.

Those are different optimization targets, so they produce different formulas.

## Example: discrete MLE

Suppose a discrete variable takes values in $\{1,\dots,K\}$ with probabilities $\pi_1,\dots,\pi_K$, where

$$
\pi_k \ge 0,
\qquad
\sum_{k=1}^{K}\pi_k = 1.
$$

Let $n_k$ be the number of observations equal to category $k$, so $\sum_k n_k = m$.  
Then the likelihood is proportional to

$$
L(\pi; D) \propto \prod_{k=1}^{K} \pi_k^{n_k},
$$

and the log-likelihood is

$$
\ell(\pi)=\sum_{k=1}^{K} n_k \log \pi_k.
$$

Maximizing under the simplex constraint gives

$$
\hat{\pi}_k = \frac{n_k}{m}.
$$

So the discrete MLE assigns each category its empirical frequency.

## The moment-matching view for exponential families

The Bernoulli, Gaussian, and categorical examples all share one deeper pattern: in exponential-family models, MLE often sets model expectations equal to empirical averages.

That is the structural payoff of writing the model in exponential-family form.  
The sufficient statistics of the model become the quantities whose empirical averages are matched by the fitted parameter.

This perspective is more important than memorizing individual derivatives.  
It tells you what the estimation problem is trying to enforce.

## Overfitting: why pure likelihood is not enough

Maximum likelihood rewards fit to the observed sample.  
If model flexibility keeps increasing, the optimized likelihood can improve even when predictive quality gets worse.

That is the basic overfitting failure mode:

- the model starts fitting accidental quirks of the sample;
- the training objective improves;
- out-of-sample prediction deteriorates.

A histogram example makes this visible.  
If you keep adding bins, the model can eventually memorize the sample rather than estimate a stable underlying density.  
So a more flexible model is not automatically a better one, even when its optimized training likelihood is larger.

This is why statistical learning needs more than raw likelihood maximization.  
It needs one of the following:

- complexity control,
- regularization,
- priors,
- model comparison penalties,
- validation on held-out data.

## Frequentist and Bayesian perspectives

Once likelihood is defined, the difference between frequentist and Bayesian reasoning becomes much cleaner.

### Frequentist view

In the frequentist view:

- the parameter is fixed but unknown;
- the data are random because a new sample could have come out differently;
- an estimator is judged by its repeated-sampling behavior.

An MLE is therefore a rule that maps the realized sample to one estimated parameter value.

### Bayesian view

In the Bayesian view:

- probability is also used to represent uncertainty about parameters;
- the parameter is treated as uncertain before the data are seen;
- a prior distribution is specified over parameter values;
- the data update that prior to a posterior distribution.

The key difference is the object retained at the end.

- Frequentist MLE keeps one fitted value.
- Bayesian inference keeps a posterior distribution unless a later summary is requested.

## Posterior distributions

Let $\theta$ be the parameter and $D$ the observed sample.  
Bayes’ rule gives

$$
p(\theta \mid D)
=
\frac{p(D \mid \theta)\,p(\theta)}{p(D)}.
$$

Each factor has a separate role:

- $p(\theta)$: the **prior**, encoding uncertainty before the data;
- $p(D \mid \theta)$: the **likelihood**, carrying the data-fit information;
- $p(\theta \mid D)$: the **posterior**, representing uncertainty after seeing the data;
- $p(D)$: the **evidence** or marginal likelihood inside the fixed model, ensuring normalization.

Inside one fixed model, the evidence is

$$
p(D)=\int p(D \mid \theta)p(\theta)\,d\theta,
$$

or the analogous sum in discrete parameter spaces.

This integral averages the likelihood over the prior distribution.

## Example: Beta-Bernoulli conjugacy

Suppose we observe five coin flips:

$$
D=(1,1,0,1,0),
$$

so

$$
m_1=3,
\qquad
m_0=2.
$$

Assume the prior

$$
\rho \sim \mathrm{Beta}(2,2).
$$

Its density is proportional to

$$
\rho^{2-1}(1-\rho)^{2-1}
=
\rho(1-\rho).
$$

The Bernoulli likelihood is proportional to

$$
p(D \mid \rho)\propto \rho^3(1-\rho)^2.
$$

Multiplying prior and likelihood gives

$$
p(\rho \mid D)
\propto
\rho^3(1-\rho)^2 \cdot \rho(1-\rho)
=
\rho^4(1-\rho)^3.
$$

That is the kernel of a Beta density with parameters

$$
2+3=5,
\qquad
2+2=4.
$$

So

$$
\rho \mid D \sim \mathrm{Beta}(5,4).
$$

This is the cleanest first example of Bayesian updating because the prior and posterior stay in the same family.

### What the posterior means

The statement

$$
\rho \mid D \sim \mathrm{Beta}(5,4)
$$

does **not** mean the coin flips themselves became Beta-distributed.  
It means our uncertainty about the unknown Bernoulli parameter is now represented by a Beta density with updated shape parameters.

That posterior keeps more information than the MLE.  
It not only locates plausible values of $\rho$; it also quantifies how concentrated or diffuse the remaining uncertainty is.

## Example: Dirichlet-Categorical pseudo-counts

The categorical analogue of the Beta prior is the Dirichlet prior.

Let a $K$-category variable have parameter vector

$$
\pi=(\pi_1,\dots,\pi_K),
\qquad
\sum_{k=1}^{K}\pi_k=1.
$$

With Dirichlet prior

$$
\pi \sim \mathrm{Dir}(\alpha_1,\dots,\alpha_K),
$$

the density kernel is

$$
\prod_{k=1}^{K}\pi_k^{\alpha_k-1}.
$$

If the observed counts are $n_1,\dots,n_K$, the likelihood kernel is

$$
\prod_{k=1}^{K}\pi_k^{n_k}.
$$

The posterior kernel becomes

$$
\prod_{k=1}^{K}\pi_k^{\alpha_k+n_k-1},
$$

so

$$
\pi \mid D
\sim
\mathrm{Dir}(\alpha_1+n_1,\dots,\alpha_K+n_K).
$$

This is why $\alpha_k$ are often interpreted as **pseudo-counts**.  
They act like prior observations before the data arrive.

## Posterior summaries

The posterior distribution is the primary Bayesian object.  
A posterior summary is only needed when one number, one interval, or one decision must be extracted.

Three common summaries are:

- **posterior mean**: average under the posterior;
- **MAP estimate**: posterior mode;
- **MLE**: likelihood maximizer, which ignores the prior.

These are different objects and answer different questions.

### Posterior mean

The posterior mean minimizes squared-error loss and represents the center of mass of the posterior.

### MAP estimate

The MAP estimate maximizes the posterior density:

$$
\hat{\theta}_{\mathrm{MAP}}
=
\arg\max_{\theta} p(\theta \mid D).
$$

Since

$$
p(\theta \mid D)\propto p(D \mid \theta)p(\theta),
$$

the MAP estimate is the maximizer of likelihood times prior.

### MLE

The MLE uses only the likelihood and therefore ignores prior information.

When the prior is flat on the relevant region, MAP and MLE can coincide.  
When the prior is informative, they generally differ.

## Example: Bernoulli posterior summaries

For a Beta posterior

$$
\rho \mid D \sim \mathrm{Beta}(\alpha,\beta),
$$

the posterior mean is

$$
\mathbb{E}[\rho \mid D]
=
\frac{\alpha}{\alpha+\beta},
$$

and when $\alpha>1$ and $\beta>1$, the MAP estimate is

$$
\hat{\rho}_{\mathrm{MAP}}
=
\frac{\alpha-1}{\alpha+\beta-2}.
$$

For the earlier posterior $\mathrm{Beta}(5,4)$,

$$
\mathbb{E}[\rho \mid D] = \frac{5}{9},
\qquad
\hat{\rho}_{\mathrm{MAP}} = \frac{4}{7},
\qquad
\hat{\rho}_{\mathrm{MLE}} = \frac{3}{5}.
$$

These do not coincide because they summarize different objects:

- the posterior mean averages over uncertainty;
- the MAP chooses the posterior mode;
- the MLE ignores the prior.

## Sequential belief updating

Bayesian updating can be done sequentially.

If $D_1$ arrives first and $D_2$ arrives later, then

$$
p(\theta \mid D_1, D_2)
\propto
p(D_2 \mid \theta)\,p(\theta \mid D_1).
$$

So the posterior after the first batch becomes the prior for the second batch.

This is not a new rule.  
It is just Bayes’ rule applied twice.

The order of data arrival does not change the final posterior as long as the same prior and likelihood model are used.

## Hyper-priors and weakly informative priors

A hyper-prior is a prior placed on the parameters of a prior distribution.  
For example, in a Beta-Bernoulli model one might place a prior on the Beta shape parameters rather than fixing them by hand.

This adds flexibility, but it also adds another layer of modeling and another layer of uncertainty.

When strong prior information is unavailable, a common compromise is to use a **weakly informative prior**: one that rules out absurd parameter regions without forcing the posterior into a narrow shape before the data are seen.

The goal is not to pretend there is no prior information.  
The goal is to choose a prior that is mild, interpretable, and stable under the scale of the problem.

## Model comparison: evidence, Bayesian selection, and BIC

Parameter estimation asks:

$$
\text{“Within this model family, which parameter values fit the data?”}
$$

Model comparison asks a different question:

$$
\text{“Which model family is best supported by the data?”}
$$

Suppose $M$ indexes a model class.  
Then the **model evidence** is

$$
p(D \mid M)
=
\int p(D \mid \theta, M)\,p(\theta \mid M)\,d\theta.
$$

This quantity averages fit across the parameter space of model $M$.

That is the key difference from MLE:

- MLE asks for the best-fitting point in parameter space;
- evidence averages over parameter values, weighted by the prior.

So a flexible model does **not** automatically win just because it can achieve a high peak likelihood.  
If most of its parameter space fits poorly, the average can still be small.

### Histogram intuition

A very flexible histogram can fit sample quirks extremely well.  
Its maximum likelihood may be high.  
But if that flexibility requires many parameters, most parameter settings will not fit the data well, and the evidence can penalize that spread automatically.

### BIC

The Bayesian information criterion is a large-sample approximation to the log evidence:

$$
\mathrm{BIC} = \log p(D \mid \hat{\theta}_{\mathrm{MLE}}, M) - \frac{k}{2}\log m,
$$

up to sign and convention differences across texts.

The important structure is:

- the first term rewards fit;
- the second term penalizes complexity through the number of free parameters $k$;
- the sample size $m$ controls the strength of that penalty.

BIC should therefore be read as a rough score balancing fit and complexity, not as a replacement for understanding the model.

## Example: one coin versus two coins

Suppose we compare:

- **Model $M_1$**: one Bernoulli parameter $\rho$ explains all flips;
- **Model $M_2$**: two different Bernoulli parameters are used for two subgroups of flips.

The more flexible model can often fit the observed data better because it has more degrees of freedom.  
But that does not settle the comparison.

The comparison must check:

1. whether the extra fit is large enough to justify the extra parameters;
2. whether the increased flexibility generalizes or merely memorizes sample noise.

Evidence and BIC are tools for that tradeoff.

## Retain from 2.3

- Likelihood compares parameter values for a fixed observed sample.
- MLE is a point estimate obtained by maximizing likelihood.
- Posterior inference combines likelihood with a prior and keeps a full uncertainty distribution.
- Overfitting is the reason raw fit cannot be the only decision rule.
- Model evidence and BIC address model comparison, not just parameter estimation.

## Do not confuse in 2.3

- Do not confuse probability over data with likelihood over parameters.
- Do not treat likelihood as a normalized posterior distribution.
- Do not confuse MLE, MAP, and posterior mean; they answer different questions.
- Do not confuse estimating parameters within one model family with comparing different model families.

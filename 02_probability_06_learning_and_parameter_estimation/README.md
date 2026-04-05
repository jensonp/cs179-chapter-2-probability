# 2.6 Learning and Parameter Estimation

Sections 2.1–2.5 asked **forward** probability questions: once a model is given, what probabilities or densities does it assign to events and outcomes? This section asks the inverse question: after data have been observed, what parameter values or model classes are supported by those data?

The names of the mathematical objects often stay the same, but their roles change. To keep the section clear, it helps to keep one checklist visible:

1. What is fixed?
2. What is allowed to vary?
3. What object are we computing?
4. What question does that object answer?

That checklist is what prevents probability, likelihood, posterior, and evidence from blurring together.

## Data, parameters, and the sampling model

Let the observed sample be

$$
D=\bigl(x^{(1)},x^{(2)},\dots,x^{(m)}\bigr).
$$

Sequence notation matters here. We are working with a realized sample that may contain repeated values, not an unordered set.

Suppose the model is indexed by a parameter $\theta$. Under the i.i.d. assumption, the observations are independent once $\theta$ is fixed and are all drawn from the same conditional law $p(x\mid \theta)$. Then

$$
p(D\mid \theta)=\prod_{i=1}^{m} p\bigl(x^{(i)}\mid \theta\bigr).
$$

This factorization is what makes likelihood calculations manageable. It is also the reason log-likelihoods become sums rather than products.

## Likelihood

The likelihood is the sampling law viewed as a function of the parameter for a fixed observed sample:

$$
L(\theta;D)=p(D\mid \theta).
$$

This is one of the most important role reversals in the chapter.

- In the sampling-model view, $\theta$ is fixed and the data are random.
- In the likelihood view, the data are fixed and $\theta$ varies.

The algebraic expression is the same, but the question is different. Likelihood does **not** tell us the probability that a parameter value is true. It tells us how well different parameter values account for the data we actually observed.

Taking logs usually simplifies the optimization:

$$
\ell(\theta)=\log L(\theta;D)=\sum_{i=1}^{m}\log p\bigl(x^{(i)}\mid \theta\bigr).
$$

## Maximum likelihood estimation

The maximum likelihood estimator is

$$
\hat{\theta}_{\mathrm{MLE}}=\arg\max_{\theta} L(\theta;D)
=
\arg\max_{\theta}\ell(\theta).
$$

The pattern is always the same:

1. write the likelihood or log-likelihood;
2. simplify it using the model structure;
3. solve the maximizing condition;
4. interpret what the solution is matching in the data.

### Bernoulli MLE

Suppose $X\in\{0,1\}$ with parameter

$$
\rho=\mathbb{P}(X=1).
$$

Let the sample contain $m_1$ ones and $m_0$ zeros, so $m_1+m_0=m$. The likelihood is

$$
L(\rho;D)=\rho^{m_1}(1-\rho)^{m_0}.
$$

The log-likelihood is

$$
\ell(\rho)=m_1\log \rho + m_0\log(1-\rho).
$$

Maximizing this yields

$$
\hat{\rho}_{\mathrm{MLE}}=\frac{m_1}{m}.
$$

So the Bernoulli MLE is just the empirical success frequency.

### Gaussian MLE with known variance

Suppose

$$
X^{(i)}\sim \mathcal{N}(\mu,\sigma^2)
$$

with $\sigma^2$ known. Maximizing the Gaussian likelihood over $\mu$ yields

$$
\hat{\mu}_{\mathrm{MLE}}=\frac1m\sum_{i=1}^{m} x^{(i)}.
$$

So the sample mean is not just a familiar summary statistic. It is the maximum-likelihood estimate of the Gaussian mean.

### Gaussian MLE with unknown mean and variance

When both parameters are unknown,

$$
\hat{\mu}_{\mathrm{MLE}}=\frac1m\sum_{i=1}^{m}x^{(i)},
$$

and

$$
\hat{\sigma}^2_{\mathrm{MLE}}
=
\frac1m\sum_{i=1}^{m}
\bigl(x^{(i)}-\hat{\mu}_{\mathrm{MLE}}\bigr)^2.
$$

The denominator here is $m$, not $m-1$. That distinction matters because the MLE is optimizing likelihood, while the classical unbiased sample variance is optimizing a different criterion.

### Discrete categorical MLE

Suppose a variable takes values in $\{1,\dots,K\}$ with probabilities $\pi_1,\dots,\pi_K$, and let $n_k$ be the count of category $k$. Then

$$
L(\pi;D)\propto \prod_{k=1}^{K}\pi_k^{n_k},
$$

so

$$
\ell(\pi)=\sum_{k=1}^{K} n_k\log \pi_k.
$$

Maximizing under the simplex constraint gives

$$
\hat{\pi}_k=\frac{n_k}{m}.
$$

Again, the MLE sets the model’s category probabilities equal to empirical frequencies.

## The moment-matching view

The Bernoulli, Gaussian, and categorical cases all illustrate a deeper pattern. In exponential-family models, MLE often chooses parameters so that model expectations of sufficient statistics match empirical averages from the data.

That is the structural payoff, and it matters more than memorizing derivative manipulations. The fitted model is trying to reproduce the key averages the chosen family is capable of representing.

## Overfitting: why pure likelihood is not enough

Maximum likelihood rewards fit to the observed sample. If model flexibility keeps increasing, optimized training likelihood can keep improving even when predictive quality worsens.

That is the basic overfitting failure mode:

- the model begins fitting accidental quirks of the sample;
- the training objective improves;
- out-of-sample behavior deteriorates.

A flexible histogram makes this visible. With enough bins, the model can memorize the observed sample instead of estimating a stable underlying density.

This is why statistical learning needs more than raw likelihood maximization. It also needs one or more of the following:

- complexity control,
- regularization,
- priors,
- model-comparison penalties,
- held-out validation.

## Frequentist and Bayesian perspectives

Once likelihood is clear, the frequentist/Bayesian distinction becomes much easier to state cleanly.

### Frequentist view

In the frequentist view:

- the parameter is fixed but unknown;
- the data are random because another sample could have come out differently;
- an estimator is judged by its repeated-sampling behavior.

An MLE is therefore a rule that maps the realized sample to one fitted parameter value.

### Bayesian view

In the Bayesian view:

- probability is also used to represent uncertainty about parameters;
- the parameter is treated as uncertain before the data arrive;
- a prior distribution is specified over parameter values;
- the data update that prior to a posterior distribution.

The crucial difference is what object is retained at the end:

- frequentist MLE keeps one fitted value;
- Bayesian inference keeps a posterior distribution unless a later summary is requested.

## Posterior distributions

Let $\theta$ be the parameter and $D$ the observed data. Bayes’ rule gives

$$
p(\theta\mid D)=\frac{p(D\mid \theta)\,p(\theta)}{p(D)}.
$$

Each factor has its own job:

- $p(\theta)$ is the **prior**, representing uncertainty before the data;
- $p(D\mid \theta)$ is the **likelihood**, carrying the data-fit information;
- $p(\theta\mid D)$ is the **posterior**, representing uncertainty after seeing the data;
- $p(D)$ is the **evidence** inside a fixed model, ensuring normalization.

Inside one fixed model,

$$
p(D)=\int p(D\mid \theta)p(\theta)\,d\theta,
$$

or the analogous sum in a discrete parameter space. This averages the likelihood across parameter values under the prior.

## Beta–Bernoulli conjugacy

Suppose we observe

$$
D=(1,1,0,1,0),
$$

so $m_1=3$ and $m_0=2$. Let the Bernoulli parameter have prior

$$
\rho\sim \mathrm{Beta}(2,2).
$$

Its density kernel is

$$
\rho^{2-1}(1-\rho)^{2-1}=\rho(1-\rho).
$$

The Bernoulli likelihood is proportional to

$$
p(D\mid \rho)\propto \rho^3(1-\rho)^2.
$$

Multiplying prior and likelihood gives

$$
p(\rho\mid D)\propto \rho^4(1-\rho)^3,
$$

which is the kernel of

$$
\mathrm{Beta}(5,4).
$$

So

$$
\rho\mid D\sim \mathrm{Beta}(5,4).
$$

This is the cleanest first example of Bayesian updating because the prior and posterior stay in the same family.

### What the posterior means

The statement

$$
\rho\mid D\sim \mathrm{Beta}(5,4)
$$

does **not** mean the coin flips became Beta-distributed. It means our uncertainty about the unknown Bernoulli parameter is now represented by a Beta distribution with updated shape parameters.

The posterior therefore keeps more information than the MLE. It records not only where plausible parameter values sit, but also how concentrated or diffuse the remaining uncertainty is.

## Dirichlet–categorical updating

The categorical analogue of the Beta prior is the Dirichlet prior. If

$$
\pi=(\pi_1,\dots,\pi_K),
\qquad \sum_{k=1}^{K}\pi_k=1,
$$

and

$$
\pi\sim \mathrm{Dir}(\alpha_1,\dots,\alpha_K),
$$

then the prior kernel is

$$
\prod_{k=1}^{K}\pi_k^{\alpha_k-1}.
$$

If the observed category counts are $n_1,\dots,n_K$, then the likelihood kernel is

$$
\prod_{k=1}^{K}\pi_k^{n_k}.
$$

The posterior becomes

$$
\pi\mid D\sim \mathrm{Dir}(\alpha_1+n_1,\dots,\alpha_K+n_K).
$$

This is why the Dirichlet parameters are often interpreted as pseudo-counts.

## Posterior summaries

The posterior distribution is the primary Bayesian object. Posterior summaries are compressions of that full object for situations where one number or one decision is required.

Three common summaries are:

- **posterior mean**: average under the posterior;
- **MAP estimate**: posterior mode;
- **MLE**: likelihood maximizer, which ignores the prior.

These are different objects because they answer different questions.

### Posterior mean

The posterior mean minimizes squared-error loss. It is the center of mass of the posterior.

### MAP estimate

The MAP estimate is

$$
\hat{\theta}_{\mathrm{MAP}}=\arg\max_{\theta} p(\theta\mid D).
$$

Since

$$
p(\theta\mid D)\propto p(D\mid \theta)p(\theta),
$$

the MAP estimate maximizes likelihood times prior.

### MLE versus MAP

The MLE depends only on the likelihood. The MAP uses both likelihood and prior. If the prior is flat on the relevant region, MLE and MAP may coincide. If the prior is informative, they generally differ.

### Bernoulli posterior summaries

For a Beta posterior

$$
\rho\mid D\sim \mathrm{Beta}(\alpha,\beta),
$$

the posterior mean is

$$
\mathbb{E}[\rho\mid D]=\frac{\alpha}{\alpha+\beta},
$$

and when $\alpha>1$ and $\beta>1$, the MAP estimate is

$$
\hat{\rho}_{\mathrm{MAP}}=\frac{\alpha-1}{\alpha+\beta-2}.
$$

For the earlier posterior $\mathrm{Beta}(5,4)$,

$$
\mathbb{E}[\rho\mid D]=\frac59,\qquad
\hat{\rho}_{\mathrm{MAP}}=\frac47,\qquad
\hat{\rho}_{\mathrm{MLE}}=\frac35.
$$

These differ because they summarize different objects.

## Sequential updating

Bayesian updating can be performed in batches. If $D_1$ arrives first and $D_2$ arrives later, then

$$
p(\theta\mid D_1,D_2)\propto p(D_2\mid \theta)\,p(\theta\mid D_1).
$$

So the posterior after the first batch becomes the prior for the second batch. This is not a new rule. It is Bayes’ rule applied repeatedly.

## Hyper-priors and weakly informative priors

A hyper-prior is a prior on the parameters of a prior distribution. For example, in a Beta–Bernoulli model one may place a prior on the Beta shape parameters instead of fixing them.

This adds flexibility, but also adds another layer of modeling and uncertainty.

When strong prior information is unavailable, a common compromise is a **weakly informative prior**: one that rules out absurd parameter regions without forcing the posterior into an unrealistically narrow shape before the data arrive.

## Model comparison: evidence and BIC

Parameter estimation asks:

$$
\text{“Within this model family, which parameter values fit the data?”}
$$

Model comparison asks:

$$
\text{“Which model family is best supported by the data?”}
$$

Suppose $M$ indexes a model class. Then the model evidence is

$$
p(D\mid M)=\int p(D\mid \theta,M)\,p(\theta\mid M)\,d\theta.
$$

This quantity averages fit across the parameter space of the model.

That is the crucial difference from MLE:

- MLE asks for the best-fitting point;
- evidence averages fit over parameter values, weighted by the prior.

So a flexible model does **not** automatically win just because it has a higher peak likelihood.

### Histogram intuition

A very flexible histogram can fit sample quirks extremely well. Its maximum likelihood may be high. But if most of its parameter settings fit poorly, its average fit can still be low. Evidence captures that automatically.

### BIC

The Bayesian information criterion is a large-sample approximation to the log evidence:

$$
\mathrm{BIC}
=
\log p(D\mid \hat{\theta}_{\mathrm{MLE}},M)
-
\frac{k}{2}\log m,
$$

up to sign and convention differences across texts.

The important structure is simple:

- one term rewards fit;
- one term penalizes model complexity through the number of free parameters $k$;
- the sample size $m$ controls the strength of that penalty.

### Example: one coin versus two coins

Suppose $M_1$ uses one Bernoulli parameter for all flips, while $M_2$ uses two Bernoulli parameters for two subgroups. The more flexible model can fit the observed data better, but that alone does not settle the comparison. The real question is whether the additional fit justifies the extra parameters, or whether it is merely memorizing sample noise.

## Retain from 2.6

- Likelihood compares parameter values for a fixed observed sample.
- MLE is a point estimate obtained by maximizing likelihood.
- Posterior inference combines likelihood with a prior and keeps a full uncertainty distribution.
- Overfitting explains why raw fit cannot be the only decision rule.
- Model evidence compares whole model families by averaging fit over parameter space rather than taking only the best point.

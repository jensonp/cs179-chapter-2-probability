# 2.6 Learning and Parameter Estimation

Sections 2.1 through 2.5 asked forward questions:

- if the model is already known, what probabilities does it assign?
- if the parameters are already fixed, what outcomes are likely?

This section changes the direction of reasoning.

Now the data have already been observed, and the question becomes:

- what parameter values fit those observations well?
- how do we update uncertainty about parameters after data arrive?
- how do we compare one model family with another?

For beginners, the hardest part of this section is not the calculus. It is keeping track of which object is random, which object is fixed, and which question is currently being asked.

So keep this checklist visible:

1. What is fixed?
2. What is allowed to vary?
3. What function are we looking at?
4. What question does that function answer?

That checklist is what keeps probability, likelihood, posterior, evidence, MLE, and MAP from collapsing into one blur.

---

## 1. Data, parameters, and the sampling model

Suppose we observe a sample

$$
D=\bigl(x^{(1)},x^{(2)},\dots,x^{(m)}\bigr).
$$

This notation means:

- there are $m$ observations;
- the first observed value is $x^{(1)}$;
- the second observed value is $x^{(2)}$;
- and so on.

The parentheses in the superscripts indicate observation index, not exponentiation.

Now suppose the model is controlled by a parameter $\theta$.

Examples:

- in a Bernoulli model, $\theta$ may be the success probability $\rho$;
- in a Gaussian model, $\theta$ may be the mean $\mu$, or the pair $(\mu,\sigma^2)$;
- in a categorical model, $\theta$ may be the probability vector $\pi$.

### The i.i.d. assumption

Many introductory derivations assume the data are i.i.d. given $\theta$.

i.i.d. stands for:

- **independent**: once $\theta$ is fixed, one observation does not change the distribution of another;
- **identically distributed**: once $\theta$ is fixed, every observation is drawn from the same conditional law.

Under that assumption,

$$
p(D\mid \theta)=\prod_{i=1}^{m} p\bigl(x^{(i)}\mid \theta\bigr).
$$

This factorization is important enough to unpack carefully.

Step 1: write the joint conditional law of the whole sample.

$$
p\bigl(x^{(1)},x^{(2)},\dots,x^{(m)}\mid \theta\bigr).
$$

Step 2: independence given $\theta$ allows this joint probability or density to factor into a product of one-observation terms.

$$
p\bigl(x^{(1)},x^{(2)},\dots,x^{(m)}\mid \theta\bigr)=\prod_{i=1}^{m} p\bigl(x^{(i)}\mid \theta\bigr).
$$

Step 3: by definition, the left-hand side is exactly $p(D\mid \theta)$.

So we obtain the displayed factorization above.

This is the structural starting point for almost every likelihood calculation in the section.

---

## 2. Likelihood

The likelihood is the same algebraic expression as the sampling model, but viewed as a function of the parameter after the data have already been observed:

$$
L(\theta;D)=p(D\mid \theta).
$$

This is the first major role reversal.

### Sampling-model view versus likelihood view

In the sampling-model view:

- $\theta$ is fixed;
- the data are random because a different sample could have been observed.

In the likelihood view:

- the data $D$ are fixed at the values we actually observed;
- $\theta$ is allowed to vary;
- the goal is to compare how well different parameter values explain this realized sample.

The formula is the same. The question is different.

### What likelihood is not

Likelihood does **not** mean

$$
P(\theta\mid D).
$$

That would be a posterior distribution over parameter values, which requires Bayes' rule and a prior.

Likelihood means:

- fix the observed data;
- vary the parameter;
- ask which parameter values make the observed data more or less plausible under the model.

### Why log-likelihood is introduced

Products of many terms are awkward to differentiate and can become numerically tiny. Taking logs turns products into sums:

$$
\ell(\theta)=\log L(\theta;D)=\sum_{i=1}^{m}\log p\bigl(x^{(i)}\mid \theta\bigr).
$$

This works because:

$$
L(\theta;D)=\prod_{i=1}^{m} p\bigl(x^{(i)}\mid \theta\bigr),
$$

so applying $\log$ gives

$$
\log L(\theta;D)=\log \prod_{i=1}^{m} p\bigl(x^{(i)}\mid \theta\bigr).
$$

Using the logarithm identity $\log(ab)=\log a+\log b$, we obtain

$$
\log L(\theta;D)=\sum_{i=1}^{m}\log p\bigl(x^{(i)}\mid \theta\bigr).
$$

Because the logarithm is strictly increasing, maximizing $L(\theta;D)$ and maximizing $\ell(\theta)$ give the same parameter value.

---

## 3. Maximum likelihood estimation

The maximum likelihood estimator, or MLE, is the parameter value that maximizes the likelihood:

$$
\hat{\theta}_{\mathrm{MLE}}=\arg\max_{\theta} L(\theta;D)=\arg\max_{\theta}\ell(\theta).
$$

The word "argmax" means "the argument, or parameter value, at which the maximum occurs."

### The generic MLE workflow

Most textbook MLE derivations follow the same pattern:

1. write the likelihood;
2. take logs;
3. differentiate with respect to the parameter;
4. set the derivative equal to zero;
5. solve for the candidate maximizer;
6. check that it is actually a maximum;
7. interpret the answer.

The later examples are easier if that template is kept explicit.

---

## 4. Bernoulli MLE

Suppose $X\in\{0,1\}$ and

$$
\rho=P(X=1).
$$

Then

$$
P(X=0)=1-\rho.
$$

Now suppose the sample contains:

- $m_1$ ones;
- $m_0$ zeros;
- so the total sample size is $m=m_0+m_1$.

### Step 1: write the likelihood

Each observed $1$ contributes a factor of $\rho$. Each observed $0$ contributes a factor of $1-\rho$.

Therefore

$$
L(\rho;D)=\rho^{m_1}(1-\rho)^{m_0}.
$$

### Step 2: take logs

$$
\ell(\rho)=\log L(\rho;D)=\log\!\bigl(\rho^{m_1}(1-\rho)^{m_0}\bigr).
$$

Use the log rules $\log(ab)=\log a+\log b$ and $\log(a^k)=k\log a$:

$$
\ell(\rho)=m_1\log \rho+m_0\log(1-\rho).
$$

### Step 3: differentiate

Differentiate term by term.

For the first term:

$$
\frac{d}{d\rho}\bigl(m_1\log \rho\bigr)=\frac{m_1}{\rho}.
$$

For the second term, use the chain rule:

$$
\frac{d}{d\rho}\bigl(m_0\log(1-\rho)\bigr)=m_0\cdot \frac{1}{1-\rho}\cdot(-1)=-\frac{m_0}{1-\rho}.
$$

So

$$
\ell'(\rho)=\frac{m_1}{\rho}-\frac{m_0}{1-\rho}.
$$

### Step 4: set the derivative equal to zero

$$
\frac{m_1}{\rho}-\frac{m_0}{1-\rho}=0.
$$

Move one term to the other side:

$$
\frac{m_1}{\rho}=\frac{m_0}{1-\rho}.
$$

Cross-multiply:

$$
m_1(1-\rho)=m_0\rho.
$$

Expand the left-hand side:

$$
m_1-m_1\rho=m_0\rho.
$$

Move the $\rho$ terms to the same side:

$$
m_1=m_0\rho+m_1\rho.
$$

Factor out $\rho$:

$$
m_1=\rho(m_0+m_1).
$$

Since $m_0+m_1=m$, we get

$$
m_1=\rho m.
$$

So the maximizing candidate is

$$
\hat{\rho}_{\mathrm{MLE}}=\frac{m_1}{m}.
$$

### Step 5: check that it is a maximum

Differentiate once more:

$$
\ell''(\rho)=-\frac{m_1}{\rho^2}-\frac{m_0}{(1-\rho)^2}.
$$

Both terms are nonpositive for $0<\rho<1$, and unless the sample is degenerate they are strictly negative. So the log-likelihood is concave and the critical point is indeed the maximizer.

### Interpretation

The Bernoulli MLE is the empirical success frequency. The fitted model copies the observed fraction of ones into the Bernoulli parameter.

That is a deep pattern, not just a one-off trick: likelihood fitting often makes model summaries match empirical summaries.

### Concrete example

Suppose the observed sample is

$$
D=(1,0,1,1,0).
$$

Then:

- $m_1=3$;
- $m_0=2$;
- $m=5$.

So

$$
\hat{\rho}_{\mathrm{MLE}}=\frac35=0.6.
$$

---

## 5. Gaussian MLE with known variance

Now suppose

$$
X^{(i)}\sim \mathcal{N}(\mu,\sigma^2),
$$

where $\sigma^2$ is known and only $\mu$ is unknown.

### Step 1: write the likelihood

For one observation,

$$
p(x^{(i)}\mid \mu)=\frac{1}{\sqrt{2\pi\sigma^2}}\exp\!\left(-\frac{(x^{(i)}-\mu)^2}{2\sigma^2}\right).
$$

Because the observations are i.i.d.,

$$
L(\mu;D)=\prod_{i=1}^{m}\frac{1}{\sqrt{2\pi\sigma^2}}\exp\!\left(-\frac{(x^{(i)}-\mu)^2}{2\sigma^2}\right).
$$

### Step 2: take logs

The product of identical constants becomes a power, and the product of exponentials becomes the exponential of a sum. Taking logs gives

$$
\ell(\mu)=-\frac{m}{2}\log(2\pi\sigma^2)-\frac{1}{2\sigma^2}\sum_{i=1}^{m}(x^{(i)}-\mu)^2.
$$

The first term does not depend on $\mu$, so it will disappear when we differentiate.

### Step 3: differentiate with respect to $\mu$

Differentiate the sum term:

$$
\frac{d}{d\mu}(x^{(i)}-\mu)^2=2(x^{(i)}-\mu)(-1)=-2(x^{(i)}-\mu).
$$

So

$$
\frac{d}{d\mu}\sum_{i=1}^{m}(x^{(i)}-\mu)^2=-2\sum_{i=1}^{m}(x^{(i)}-\mu).
$$

Multiplying by the constant factor in front,

$$
\ell'(\mu)=-\frac{1}{2\sigma^2}\cdot \left[-2\sum_{i=1}^{m}(x^{(i)}-\mu)\right]=\frac{1}{\sigma^2}\sum_{i=1}^{m}(x^{(i)}-\mu).
$$

### Step 4: set the derivative equal to zero

$$
\frac{1}{\sigma^2}\sum_{i=1}^{m}(x^{(i)}-\mu)=0.
$$

Since $\sigma^2>0$, this is equivalent to

$$
\sum_{i=1}^{m}(x^{(i)}-\mu)=0.
$$

Expand the sum:

$$
\sum_{i=1}^{m}x^{(i)}-\sum_{i=1}^{m}\mu=0.
$$

Because $\mu$ is the same in every term,

$$
\sum_{i=1}^{m}\mu=m\mu.
$$

So

$$
\sum_{i=1}^{m}x^{(i)}-m\mu=0.
$$

Hence

$$
m\mu=\sum_{i=1}^{m}x^{(i)}.
$$

Divide by $m$:

$$
\hat{\mu}_{\mathrm{MLE}}=\frac1m\sum_{i=1}^{m}x^{(i)}.
$$

### Interpretation

The Gaussian mean MLE is the sample mean.

This is not a coincidence. The Gaussian family is built so that the center parameter is matched by the empirical center of the data.

---

## 6. Gaussian MLE with unknown mean and variance

Now suppose both $\mu$ and $\sigma^2$ are unknown.

The answer is familiar:

$$
\hat{\mu}_{\mathrm{MLE}}=\frac1m\sum_{i=1}^{m}x^{(i)},
$$

and

$$
\hat{\sigma}^2_{\mathrm{MLE}}=\frac1m\sum_{i=1}^{m}\bigl(x^{(i)}-\hat{\mu}_{\mathrm{MLE}}\bigr)^2.
$$

But for a beginner, the derivation matters more than the final formula.

### Step 1: write the log-likelihood

For one Gaussian observation,

$$
p(x^{(i)}\mid \mu,\sigma^2)=\frac{1}{\sqrt{2\pi\sigma^2}}\exp\!\left(-\frac{(x^{(i)}-\mu)^2}{2\sigma^2}\right).
$$

For the full sample,

$$
\ell(\mu,\sigma^2)=-\frac{m}{2}\log(2\pi)-\frac{m}{2}\log(\sigma^2)-\frac{1}{2\sigma^2}\sum_{i=1}^{m}(x^{(i)}-\mu)^2.
$$

### Step 2: maximize with respect to $\mu$

Holding $\sigma^2$ fixed, this is exactly the same calculation as before, so

$$
\hat{\mu}_{\mathrm{MLE}}=\frac1m\sum_{i=1}^{m}x^{(i)}.
$$

### Step 3: maximize with respect to $\sigma^2$

Now treat $\mu$ as fixed for the moment and differentiate with respect to $\sigma^2$.

Differentiate the term $-\frac{m}{2}\log(\sigma^2)$:

$$
\frac{d}{d(\sigma^2)}\left[-\frac{m}{2}\log(\sigma^2)\right]=-\frac{m}{2}\cdot \frac{1}{\sigma^2}.
$$

Differentiate the term $-\frac{1}{2\sigma^2}\sum (x^{(i)}-\mu)^2$.

First rewrite the prefactor:

$$
-\frac{1}{2\sigma^2}=-\frac12(\sigma^2)^{-1}.
$$

Differentiate:

$$
\frac{d}{d(\sigma^2)}\left[-\frac12(\sigma^2)^{-1}\right]=\frac12(\sigma^2)^{-2}.
$$

So

$$
\frac{d}{d(\sigma^2)}\left[-\frac{1}{2\sigma^2}\sum_{i=1}^{m}(x^{(i)}-\mu)^2\right]=\frac{1}{2(\sigma^2)^2}\sum_{i=1}^{m}(x^{(i)}-\mu)^2.
$$

Therefore

$$
\frac{\partial \ell}{\partial (\sigma^2)}=-\frac{m}{2\sigma^2}+\frac{1}{2(\sigma^2)^2}\sum_{i=1}^{m}(x^{(i)}-\mu)^2.
$$

### Step 4: set this derivative equal to zero

$$
-\frac{m}{2\sigma^2}+\frac{1}{2(\sigma^2)^2}\sum_{i=1}^{m}(x^{(i)}-\mu)^2=0.
$$

Multiply both sides by $2(\sigma^2)^2$:

$$
-m\sigma^2+\sum_{i=1}^{m}(x^{(i)}-\mu)^2=0.
$$

So

$$
m\sigma^2=\sum_{i=1}^{m}(x^{(i)}-\mu)^2.
$$

Divide by $m$:

$$
\sigma^2=\frac1m\sum_{i=1}^{m}(x^{(i)}-\mu)^2.
$$

Now substitute the maximizing value of $\mu$, namely $\hat{\mu}_{\mathrm{MLE}}$:

$$
\hat{\sigma}^2_{\mathrm{MLE}}=\frac1m\sum_{i=1}^{m}\bigl(x^{(i)}-\hat{\mu}_{\mathrm{MLE}}\bigr)^2.
$$

### Why the denominator is $m$, not $m-1$

The MLE is chosen to maximize likelihood. The unbiased sample variance from elementary statistics is chosen to correct expected bias under repeated sampling.

These are different goals, so the formulas differ.

That distinction matters. "MLE" and "unbiased estimator" are not synonyms.

---

## 7. Categorical MLE

Suppose the variable can take one of $K$ categories with parameter vector

$$
\pi=(\pi_1,\dots,\pi_K).
$$

The parameter must satisfy

$$
\pi_k\ge 0 \quad \text{for all } k,
$$

and

$$
\sum_{k=1}^{K}\pi_k=1.
$$

Let $n_k$ be the number of observed occurrences of category $k$.

### Step 1: write the likelihood

Up to the order of the sample, the likelihood is proportional to

$$
L(\pi;D)\propto \prod_{k=1}^{K}\pi_k^{n_k}.
$$

### Step 2: take logs

$$
\ell(\pi)=\sum_{k=1}^{K} n_k\log \pi_k.
$$

### Step 3: maximize under the constraint

We must maximize $\ell(\pi)$ subject to

$$
\sum_{k=1}^{K}\pi_k=1.
$$

Introduce a Lagrange multiplier $\lambda$ and define

$$
\mathcal{L}(\pi,\lambda)=\sum_{k=1}^{K} n_k\log \pi_k+\lambda\left(\sum_{k=1}^{K}\pi_k-1\right).
$$

Differentiate with respect to $\pi_k$:

$$
\frac{\partial \mathcal{L}}{\partial \pi_k}=\frac{n_k}{\pi_k}+\lambda.
$$

Set this equal to zero:

$$
\frac{n_k}{\pi_k}+\lambda=0.
$$

So

$$
\frac{n_k}{\pi_k}=-\lambda.
$$

Solve for $\pi_k$:

$$
\pi_k=-\frac{n_k}{\lambda}.
$$

Now impose the constraint:

$$
\sum_{k=1}^{K}\pi_k=1.
$$

Substitute the expression above:

$$
\sum_{k=1}^{K}\left(-\frac{n_k}{\lambda}\right)=1.
$$

Factor out $-\frac{1}{\lambda}$:

$$
-\frac{1}{\lambda}\sum_{k=1}^{K}n_k=1.
$$

But the counts sum to the total sample size:

$$
\sum_{k=1}^{K}n_k=m.
$$

So

$$
-\frac{m}{\lambda}=1.
$$

Hence

$$
\lambda=-m.
$$

Substitute back:

$$
\hat{\pi}_k=\frac{n_k}{m}.
$$

### Interpretation

Again the fitted categorical probabilities match the observed frequencies.

That is the categorical version of the Bernoulli result.

---

## 8. The moment-matching viewpoint

The Bernoulli, Gaussian, and categorical MLEs all share the same deeper pattern:

- the fitted parameter makes model summaries match empirical summaries.

Examples:

- Bernoulli MLE matches the model success probability to the observed success frequency;
- Gaussian mean MLE matches the model mean to the sample mean;
- categorical MLE matches the model category probabilities to empirical proportions.

This is why estimation is not just "differentiate and solve." The mathematics is forcing the model to reproduce the statistics that the family knows how to represent.

---

## 9. Overfitting: why pure likelihood is not enough

Likelihood rewards fit to the observed sample.

That is useful, but dangerous if model flexibility grows too large.

Imagine a histogram model with so many bins that each observed point can get its own narrow bin. Training likelihood may become very high, but the model may simply be memorizing accidental quirks of the sample rather than learning a stable underlying pattern.

This failure mode is called overfitting.

So a good learning procedure must care about more than in-sample fit alone. Common control mechanisms include:

- restricting model complexity;
- adding regularization penalties;
- using prior distributions;
- comparing models with complexity penalties;
- checking performance on held-out data.

---

## 10. Frequentist and Bayesian viewpoints

Likelihood by itself does not yet distinguish the frequentist and Bayesian viewpoints. It is used in both.

### Frequentist view

In the frequentist view:

- the parameter is fixed but unknown;
- the data are random because another sample could have been drawn;
- an estimator is judged by repeated-sampling behavior.

So an MLE is a rule that takes a realized dataset and returns one fitted parameter value.

### Bayesian view

In the Bayesian view:

- probability is also used to represent uncertainty about parameters;
- the parameter is not treated as known but hidden;
- a prior distribution is placed over parameter values;
- the data update that prior to a posterior distribution.

The most important difference is the final object retained:

- frequentist estimation often keeps one fitted value;
- Bayesian inference keeps a posterior distribution unless a later summary is requested.

---

## 11. Posterior distributions

Let $\theta$ be the parameter and $D$ the observed data. Bayes' rule gives

$$
p(\theta\mid D)=\frac{p(D\mid \theta)p(\theta)}{p(D)}.
$$

Each factor has a different role:

- $p(\theta)$ is the prior;
- $p(D\mid \theta)$ is the likelihood;
- $p(\theta\mid D)$ is the posterior;
- $p(D)$ is the evidence.

### Why the evidence appears

The numerator

$$
p(D\mid \theta)p(\theta)
$$

is usually only proportional to the posterior. To turn it into a proper probability distribution over $\theta$, we must divide by whatever constant makes the total integrate or sum to $1$.

That constant is exactly

$$
p(D)=\int p(D\mid \theta)p(\theta)\,d\theta,
$$

or the analogous sum in a discrete parameter space.

So the evidence is the normalization constant of the posterior inside a fixed model.

---

## 12. Beta-Bernoulli conjugacy

This is the cleanest first Bayesian updating example because every step can be seen directly.

Suppose the observed data are

$$
D=(1,1,0,1,0).
$$

So:

- number of ones is $m_1=3$;
- number of zeros is $m_0=2$.

Let the Bernoulli parameter have prior

$$
\rho\sim \mathrm{Beta}(2,2).
$$

### Step 1: write the prior density kernel

The $\mathrm{Beta}(a,b)$ density is proportional to

$$
\rho^{a-1}(1-\rho)^{b-1}.
$$

So for $a=2$ and $b=2$,

$$
p(\rho)\propto \rho^{2-1}(1-\rho)^{2-1}.
$$

Simplify the exponents:

$$
p(\rho)\propto \rho(1-\rho).
$$

### Step 2: write the likelihood kernel

For Bernoulli data with $m_1$ ones and $m_0$ zeros,

$$
p(D\mid \rho)\propto \rho^{m_1}(1-\rho)^{m_0}.
$$

Substitute $m_1=3$ and $m_0=2$:

$$
p(D\mid \rho)\propto \rho^3(1-\rho)^2.
$$

### Step 3: multiply prior and likelihood

Bayes' rule says

$$
p(\rho\mid D)\propto p(D\mid \rho)p(\rho).
$$

Substitute the two kernels:

$$
p(\rho\mid D)\propto \rho^3(1-\rho)^2 \cdot \rho(1-\rho).
$$

Combine like bases by adding exponents:

$$
p(\rho\mid D)\propto \rho^{3+1}(1-\rho)^{2+1}.
$$

So

$$
p(\rho\mid D)\propto \rho^4(1-\rho)^3.
$$

### Step 4: recognize the posterior family

A $\mathrm{Beta}(a',b')$ density has kernel

$$
\rho^{a'-1}(1-\rho)^{b'-1}.
$$

Match exponents:

- $a'-1=4$, so $a'=5$;
- $b'-1=3$, so $b'=4$.

Therefore

$$
\rho\mid D\sim \mathrm{Beta}(5,4).
$$

### What this means

This does **not** mean the coin flips became Beta-distributed.

It means our uncertainty about the Bernoulli parameter $\rho$ is now represented by a Beta distribution with updated parameters.

That is the crucial role distinction:

- Bernoulli describes outcomes;
- Beta describes uncertainty about the Bernoulli parameter.

---

## 13. Dirichlet-categorical updating

The Dirichlet distribution plays the same role for categorical models that the Beta distribution plays for Bernoulli models.

Suppose

$$
\pi=(\pi_1,\dots,\pi_K),
$$

with

$$
\sum_{k=1}^{K}\pi_k=1.
$$

Assume the prior is

$$
\pi\sim \mathrm{Dir}(\alpha_1,\dots,\alpha_K).
$$

Its kernel is

$$
p(\pi)\propto \prod_{k=1}^{K}\pi_k^{\alpha_k-1}.
$$

Now let the observed counts be $n_1,\dots,n_K$. The categorical likelihood kernel is

$$
p(D\mid \pi)\propto \prod_{k=1}^{K}\pi_k^{n_k}.
$$

Multiply prior and likelihood:

$$
p(\pi\mid D)\propto \left(\prod_{k=1}^{K}\pi_k^{n_k}\right)\left(\prod_{k=1}^{K}\pi_k^{\alpha_k-1}\right).
$$

Combine the factors category by category:

$$
p(\pi\mid D)\propto \prod_{k=1}^{K}\pi_k^{n_k+\alpha_k-1}.
$$

This is again the kernel of a Dirichlet distribution, so

$$
\pi\mid D\sim \mathrm{Dir}(\alpha_1+n_1,\dots,\alpha_K+n_K).
$$

That is why Dirichlet parameters are interpreted as pseudo-counts.

---

## 14. Posterior summaries

The posterior distribution is the primary Bayesian object. But sometimes a single number is needed for prediction, decision-making, or comparison.

Three common summaries are:

- posterior mean;
- MAP estimate;
- MLE.

They are not interchangeable because they summarize different objects.

### Posterior mean

The posterior mean is the average of the parameter under the posterior distribution.

For a posterior density $p(\theta\mid D)$,

$$
\mathbb{E}[\theta\mid D]=\int \theta\,p(\theta\mid D)\,d\theta,
$$

or the analogous sum for a discrete parameter space.

### MAP estimate

The MAP estimate is the posterior mode:

$$
\hat{\theta}_{\mathrm{MAP}}=\arg\max_{\theta} p(\theta\mid D).
$$

Because

$$
p(\theta\mid D)\propto p(D\mid \theta)p(\theta),
$$

the MAP estimate maximizes likelihood times prior.

### MLE versus MAP

The MLE ignores the prior. The MAP uses both likelihood and prior.

So:

- if the prior is flat on the relevant region, MAP and MLE may be similar or identical;
- if the prior is informative, MAP will generally differ from MLE.

### Beta posterior summaries

For

$$
\rho\mid D\sim \mathrm{Beta}(\alpha,\beta),
$$

the posterior mean is

$$
\mathbb{E}[\rho\mid D]=\frac{\alpha}{\alpha+\beta}.
$$

When $\alpha>1$ and $\beta>1$, the MAP estimate is

$$
\hat{\rho}_{\mathrm{MAP}}=\frac{\alpha-1}{\alpha+\beta-2}.
$$

For the earlier posterior $\mathrm{Beta}(5,4)$:

$$
\mathbb{E}[\rho\mid D]=\frac{5}{9}.
$$

Also,

$$
\hat{\rho}_{\mathrm{MAP}}=\frac{5-1}{5+4-2}=\frac47.
$$

And from the data alone,

$$
\hat{\rho}_{\mathrm{MLE}}=\frac35.
$$

These values differ because they answer different questions:

- MLE asks which parameter maximizes data fit;
- MAP asks which parameter maximizes posterior density;
- posterior mean asks for the average parameter value under the posterior.

---

## 15. Sequential updating

Bayesian updating can be done in stages.

Suppose one batch of data $D_1$ arrives first and another batch $D_2$ arrives later. Then

$$
p(\theta\mid D_1,D_2)\propto p(D_2\mid \theta,D_1)p(\theta\mid D_1).
$$

If the new data are conditionally independent of the old data given $\theta$, this simplifies to

$$
p(\theta\mid D_1,D_2)\propto p(D_2\mid \theta)p(\theta\mid D_1).
$$

So the posterior after seeing $D_1$ becomes the prior for the update using $D_2$.

This is not a new theorem. It is Bayes' rule applied repeatedly.

---

## 16. Hyper-priors and weakly informative priors

A hyper-prior is a prior placed on the parameters of another prior.

For example, in a Beta-Bernoulli model:

- $\rho$ is the Bernoulli parameter;
- $(a,b)$ are the Beta prior parameters;
- a hyper-prior would put a probability model on $(a,b)$ themselves instead of fixing them by hand.

This adds flexibility, but it also adds another layer of uncertainty and modeling decisions.

When strong prior information is unavailable, a common compromise is a weakly informative prior: a prior that rules out absurd parameter regions without forcing the posterior into an unrealistically narrow range before much data have been seen.

---

## 17. Model comparison: evidence and BIC

Parameter estimation asks:

$$
\text{Within one model family, which parameter values fit the data well?}
$$

Model comparison asks:

$$
\text{Which model family is best supported by the data?}
$$

Those are different questions.

### Model evidence

Let $M$ denote a model family. The model evidence is

$$
p(D\mid M)=\int p(D\mid \theta,M)p(\theta\mid M)\,d\theta.
$$

This quantity is easy to misread, so unpack it carefully.

Inside the integral:

- $p(D\mid \theta,M)$ measures how well one parameter value fits the data;
- $p(\theta\mid M)$ gives the prior weight of that parameter value inside the model.

The integral averages data fit across the whole parameter space of the model.

That is the crucial contrast with MLE:

- MLE looks only at the single best-fitting parameter value;
- evidence averages fit over all parameter values, weighted by the prior.

So a flexible model does not automatically win just because it can achieve a very high peak likelihood at one special parameter setting.

### Why evidence penalizes over-flexibility

If a model has many parameters, it may be able to fit the observed sample extremely well in a small region of parameter space. But if most parameter settings fit the data poorly, the average fit can still be low.

That is why evidence naturally includes a complexity penalty without adding one by hand.

### BIC

The Bayesian information criterion is a large-sample approximation to the log evidence:

$$
\mathrm{BIC}=\log p(D\mid \hat{\theta}_{\mathrm{MLE}},M)-\frac{k}{2}\log m,
$$

up to sign and convention choices across textbooks.

The important structure is:

- one term rewards fit at the best-fitting parameter;
- one term penalizes the number of free parameters $k$;
- the penalty becomes stronger as the sample size $m$ grows.

### Example: one coin versus two coins

Suppose model $M_1$ uses one Bernoulli parameter for all flips, while model $M_2$ uses two separate Bernoulli parameters for two subgroups of flips.

Then:

- $M_2$ is more flexible;
- $M_2$ can never fit worse at its best parameter value than $M_1$;
- but that does not automatically mean $M_2$ is better.

The real question is whether the extra fit is large enough to justify the extra parameter freedom.

That is exactly the kind of question evidence and BIC are designed to answer.

---

## 18. What to retain

- Likelihood is the sampling law viewed as a function of the parameter for fixed observed data.
- MLE chooses the parameter that maximizes likelihood.
- In standard families, MLE often matches model summaries to empirical summaries.
- Overfitting explains why likelihood alone is not always enough for model choice.
- Bayesian inference combines likelihood with a prior to produce a posterior distribution.
- Beta-Bernoulli and Dirichlet-categorical are the canonical first conjugate updates.
- Posterior mean, MAP, and MLE are different summaries with different meanings.
- Evidence compares whole model families by averaging fit over parameter space.

## 19. Do not confuse

- Do not confuse $p(D\mid \theta)$ with $p(\theta\mid D)$.
- Do not say likelihood is "the probability that the parameter is true."
- Do not confuse an estimator with the parameter it estimates.
- Do not confuse MLE with MAP.
- Do not confuse posterior mode with posterior mean.
- Do not confuse best fit at one parameter value with average support for a whole model family.

# 2.6 Learning and Parameter Estimation

Sections 2.1 through 2.5 mostly asked **forward** questions. A model was already specified, its parameters were already fixed, and the task was to work out what probabilities or expectations followed from that choice. This section changes the direction of reasoning. We are now in the more realistic scientific situation: the world has already produced some observations, and we want to use those observations to say something about the model that may have generated them.

That change sounds small, but conceptually it is one of the largest shifts in the course. Earlier, the model explained the data. Now the data are being used to evaluate, fit, or update the model. As soon as that reversal happens, several new objects appear: the **likelihood**, the **maximum likelihood estimator**, the **posterior distribution**, the **MAP estimate**, and the **model evidence**. These are closely related, and the mathematics often uses the same symbols in each case. That is exactly why this topic starts to feel slippery.

The main difficulty here is usually **not** the calculus. It is role confusion. The same expression can be read in different ways depending on what is fixed and what is varying. A beginner can look at the symbol

$$
p(D\mid \theta)
$$

and think it means the same thing in every context. It does not. Sometimes it is being read as a probability law for the data when the parameter is fixed. Sometimes it is being read as a function that scores parameter values after the data have already been observed. The algebra may be identical, but the question is not.

So the right way to enter this section is with a standing discipline. Every time a new formula appears, ask four questions:

1. **What object is being treated as fixed?**
2. **What object is being allowed to vary?**
3. **What function are we looking at?**
4. **What question is that function answering?**

That four-question checklist is not optional bookkeeping. It is the conceptual tool that prevents probability, likelihood, posterior, evidence, MLE, and MAP from collapsing into one undifferentiated mass of notation.

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

Before moving on, it helps to name the three layers that are already present in this apparently simple factorization.

First, there is the **data-generating layer**. The sample

$$
D = \bigl(x^{(1)},x^{(2)},\dots,x^{(m)}\bigr)
$$

is being treated as something that could in principle have turned out differently. At this stage, the observations are random because the experiment or sampling process could have produced another dataset.

Second, there is the **parameter layer**. The symbol $\theta$ is controlling the distribution from which the observations are drawn. In different model families, $\theta$ may be a single number, a vector, or even a more structured object, but its role is always the same: it specifies which member of the model family is being considered.

Third, there is the **factorization layer**. The i.i.d. assumption is not merely a convenience for shortening formulas. It tells us that once $\theta$ is fixed, the full sample contains no additional dependence structure that must be modeled. That is why the joint law of the dataset can be written as a product of one-observation terms. Nearly every likelihood in an introductory course is built by starting from this product and then deciding how to reinterpret it.

That last phrase matters: **reinterpret it**. The next subsection does not introduce a brand-new algebraic formula. It introduces a new way of reading the same one.

---

## 2. Likelihood

The likelihood is the first place in this chapter where the notation stays almost the same but the **question** changes completely. That is why students often feel that the topic becomes slippery here.

Start with the sampling model:

$$
p(D\mid \theta).
$$

If we are thinking in the ordinary data-generating direction, this expression tells us how probable or how dense different datasets are **when the parameter value is fixed**. In that reading, $\theta$ is held still and the data are the variable object.

Likelihood keeps the same algebraic expression but changes the viewpoint. Once the dataset has already been observed, we no longer ask, "What datasets might this parameter generate?" We ask, "For the dataset that actually occurred, which parameter values make it look more or less compatible with the model?" That is a different question, and the expression is now being read as a function of $\theta$:

$$
L(\theta;D)=p(D\mid \theta).
$$

This deserves to be read slowly. The semicolon in $L(\theta;D)$ is not decorative. It is there to remind you that the parameter is the variable argument and the dataset is being treated as fixed background information.

A useful way to say this in plain language is:

- the **sampling-model view** asks how random data behave when the parameter is fixed;
- the **likelihood view** asks how parameter values compare when the observed data are fixed.

The formula is the same. The meaning is not.

### A concrete role comparison

Suppose the observed sample is

$$
D=(1,0,1,1,0)
$$

from a Bernoulli model with success probability $\rho$. Then the expression

$$
\rho^3(1-\rho)^2
$$

can be read in two different but related ways.

In the sampling-model reading, if $\rho$ has already been fixed, this tells you the probability of observing exactly that particular sequence of five outcomes.

In the likelihood reading, the sequence has already happened. The sample is no longer the thing being varied. Now the expression is being used to compare candidate values of $\rho$. A value of $\rho$ that makes $\rho^3(1-\rho)^2$ larger is a value that gives the realized sample a better fit inside the Bernoulli family.

This is the first major conceptual distinction to retain: **probability distributes mass over possible data; likelihood scores parameter values using the data that were actually observed**.

### What likelihood is not

Likelihood is **not** the posterior probability of the parameter. It is not

$$
p(\theta\mid D).
$$

The posterior is a different object that appears only after a prior is introduced and Bayes' rule is applied. Likelihood by itself does not say how probable a parameter value is. It says how well that parameter value explains the observed sample **within the chosen model family**.

That qualification matters. Likelihood only compares parameter values **inside one model family at a time**. It is not yet a complete answer to model comparison, and it is not a probability distribution over parameters.

### Why likelihood usually does not normalize

A common beginner error is to think that because $p(D\mid \theta)$ is a probability law in $D$, it must also behave like a probability law in $\theta$. That is false. When we reinterpret the same expression as a function of $\theta$, there is usually no reason for it to integrate or sum to one across parameter values. In the likelihood reading, normalization is not the point. Relative comparison is the point.

So likelihood should be thought of as a **scoring surface over parameter space**, not as a distribution over parameter values.

### Why log-likelihood is introduced

Likelihoods under the i.i.d. assumption are usually products:

$$
L(\theta;D)=\prod_{i=1}^{m} p\bigl(x^{(i)}\mid \theta\bigr).
$$

Products are mathematically awkward for at least two reasons. First, they are harder to differentiate cleanly. Second, when many factors are multiplied together, the numerical values can become extremely small even when the model fit is perfectly reasonable.

The logarithm solves both issues at once. Define the log-likelihood by

$$
\ell(\theta)=\log L(\theta;D).
$$

Using the logarithm rule that turns products into sums, we get

$$
\ell(\theta)=\sum_{i=1}^{m}\log p\bigl(x^{(i)}\mid \theta\bigr).
$$

This is not a cosmetic rewrite. It changes the geometry of the optimization problem from "multiply many factors" to "add many contributions," which is easier to analyze and easier to compute with.

Just as importantly, maximizing the log-likelihood gives the same maximizing parameter value as maximizing the likelihood itself, because the logarithm is strictly increasing. The log does not change which parameter fits best. It changes only the scale on which that fit is measured.

---

## 3. Maximum likelihood estimation

The maximum likelihood estimator, or MLE, is the parameter value that maximizes the likelihood:

$$
\hat{\theta}_{\mathrm{MLE}}=\arg\max_{\theta} L(\theta;D)=\arg\max_{\theta}\ell(\theta).
$$

Before moving into examples, it helps to say exactly what this definition licenses and what it does **not** license.

The MLE is a **selection rule**. It takes the observed dataset as input and returns the parameter value at which the likelihood is largest. So the MLE is not the parameter itself. It is a rule for producing an estimate from data.

That distinction becomes important as soon as people start saying things like "the MLE is random." The fitted number you get after observing one particular dataset is just a number. But the **estimator as a rule** is random under repeated sampling, because a different dataset would generally produce a different fitted value.

It is also worth noticing what the MLE is optimizing. It is not optimizing truth. It is not optimizing future predictive performance directly. It is optimizing **fit to the observed sample within the chosen model family**. That is exactly why MLE is powerful and exactly why it can later overfit if the model family becomes too flexible.

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

This calculus derivation assumed an interior maximizer with $0<\rho<1$. That is the generic case in which the sample contains at least one $0$ and at least one $1$.

If the sample is degenerate, the maximum moves to the boundary:

- if every observation is $0$, then $L(\rho;D)=(1-\rho)^m$, which is maximized at $\rho=0$;
- if every observation is $1$, then $L(\rho;D)=\rho^m$, which is maximized at $\rho=1$.

So the formula $\hat{\rho}_{\mathrm{MLE}}=m_1/m$ still gives the right answer in the boundary cases, but the argument has to include that boundary check.

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

### Step 5: check that it is a maximum

Differentiate once more:

$$
\ell''(\mu)=-\frac{m}{\sigma^2}.
$$

Because $\sigma^2>0$, this second derivative is strictly negative. So the log-likelihood is concave in $\mu$, and the critical point above is indeed the unique maximizer.

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

At that critical point, the second derivative with respect to $\sigma^2$ is negative, so this candidate is the maximizing variance as well. The likelihood therefore chooses the empirical average squared deviation around the fitted mean.

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

The omitted proportionality constant is the multinomial counting factor. It depends on the observed counts, but not on $\pi$, so it does not affect which parameter value maximizes the likelihood.

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

At this point, it is easy to think that maximum likelihood estimation is mainly a calculus routine: write a product, take logs, differentiate, solve, and move on. That would miss the deeper pattern.

Across the Bernoulli, Gaussian, and categorical examples, the fitted parameter is not arbitrary. In each case, the optimization is pushing the model toward agreement with the empirical summaries that the model family is built to express.

In the Bernoulli case, the family has one central feature: the success probability. The MLE sets that feature equal to the observed fraction of successes.

In the Gaussian mean example with known variance, the family has a center parameter. The MLE sets that center equal to the observed sample mean.

In the categorical case, the family stores one probability for each category. The MLE sets those probabilities equal to the observed empirical proportions.

That is why these estimators feel so natural after the derivations are finished. The mathematics is not doing something mysterious. It is telling the model to reproduce, as closely as the family allows, the summaries of the data that the family was designed to encode.

This is an important general lesson. Estimation is not just an exercise in symbolic differentiation. The optimization is exposing what the model family "cares about." If a family is parameterized by a center, a spread, or category weights, likelihood fitting often pushes those parameters toward the corresponding empirical features of the sample.

That viewpoint is worth retaining because it makes later estimators easier to understand. Instead of seeing each MLE as an isolated trick, you begin to ask a more structural question: **which empirical features is this model trying to match?**

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

Up to this point, likelihood has been used in a way that both frequentists and Bayesians accept. That is why students sometimes wonder where the real split occurs. The answer is: the split is not in whether data are informative about parameters. The split is in **what kind of object the parameter is allowed to be** and **what object is retained at the end of inference**.

### Frequentist view

In the frequentist view, the parameter is fixed but unknown. It is part of the state of the world. Our uncertainty about it is epistemic--we do not know its value--but the framework does not represent that uncertainty by placing a probability distribution on the parameter itself.

What is random in the frequentist picture is the data. Another sample could have been drawn, and a different sample would generally produce a different estimate. So a frequentist estimator is judged by its repeated-sampling behavior: does it tend to be close to the true parameter, how variable is it across samples, is it biased, is it consistent, and so on.

In that language, the MLE is a rule that maps observed data to a fitted parameter value. Once the dataset is fixed, the output is just one estimate.

### Bayesian view

In the Bayesian view, uncertainty about the parameter is represented directly with probability. The parameter is not treated as "random because nature keeps resampling it," but as unknown in a way that is itself modeled probabilistically. This is done by placing a prior distribution on parameter values and then updating that prior after the data are observed.

The essential output of Bayesian inference is therefore not just one fitted number. It is a **posterior distribution** over parameter values:

$$
p(\theta\mid D).
$$

That posterior records not only which parameter values fit well, but also how uncertainty is distributed across them after the data and prior information have both been taken into account.

### The cleanest contrast

A good way to keep the two viewpoints straight is this:

- frequentist inference usually asks: **what rule should I use to estimate the fixed unknown parameter from random data?**
- Bayesian inference usually asks: **after seeing the data, how should my uncertainty about the parameter be updated?**

These viewpoints can produce similar numerical answers in some problems, but they are not conceptually interchangeable. One centers estimation rules and their repeated-sampling properties. The other centers probability distributions over uncertainty.

---

## 11. Posterior distributions

The posterior distribution is the central Bayesian answer to the learning problem. Once a prior has been specified and data have been observed, the posterior tells us how uncertainty about the parameter should now be distributed.

Bayes' rule says

$$
p(\theta\mid D)=\frac{p(D\mid \theta)p(\theta)}{p(D)}.
$$

This formula is familiar, but it becomes much easier to understand when each factor is assigned a job.

The prior $p(\theta)$ expresses what parameter values were considered more or less plausible **before** the current data were seen.

The likelihood $p(D\mid \theta)$ measures how well each parameter value fits the observed data **within the model family**.

The posterior $p(\theta\mid D)$ is the updated distribution that combines those two sources of information.

The evidence $p(D)$ is whatever normalizing constant is needed so that the posterior becomes a genuine probability distribution over the parameter space.

### Why the evidence must appear

Without the denominator, the product

$$
p(D\mid \theta)p(\theta)
$$

is usually only proportional to the posterior. It has the right shape, but not the right total mass. To turn that shape into a proper probability distribution over $\theta$, we divide by the total mass across all parameter values:

$$
p(D)=\int p(D\mid \theta)p(\theta)\,d\theta,
$$

or a sum in the discrete case.

This is one of the most important places to slow down conceptually. The evidence is not an arbitrary correction factor inserted by hand. It appears because the posterior must be a normalized distribution over parameter values.

### The posterior is not just "likelihood plus prior" in words

A common informal sentence is "the posterior is proportional to prior times likelihood." That sentence is useful, but incomplete. It tells you the **shape** of the posterior, not the fully normalized object.

That distinction matters for two reasons. First, if you want a proper distribution--something you can integrate against, take expectations under, or compare as a probability law--you need normalization. Second, later in the chapter the evidence itself becomes important for model comparison. So it is not merely a disposable constant.

A good mental picture is this: the prior tells you where you started, the likelihood tells you how the observed data reweight that picture, and the evidence rescales the result so the updated picture is again a valid probability distribution.

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

The proportionality sign means we have dropped factors that do not depend on $\rho$. For identifying the posterior family, only the $\rho$-dependent kernel matters.

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

As in the Bernoulli example, the omitted factors do not depend on $\pi$, so they do not matter for recognizing the posterior family.

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

The posterior distribution is the primary Bayesian object. In principle, once you have the posterior, you already have the full answer to the Bayesian learning problem. But in practice, people often ask for a single number. That is where summaries enter.

This is a dangerous point conceptually, because several different summaries can be extracted from the posterior, and they answer different questions. The three most common numbers that appear close together in this chapter are the **posterior mean**, the **MAP estimate**, and the **MLE**. They are often numerically similar in simple examples, but they should never be treated as synonymous.

### Posterior mean

The posterior mean is the average of the parameter under the posterior distribution:

$$
\mathbb{E}[\theta\mid D]=\int \theta\,p(\theta\mid D)\,d\theta,
$$

or a corresponding sum in a discrete parameter space.

This summary treats the posterior as a full distribution and averages across all parameter values, weighted by their posterior mass or density. It is therefore a "center of mass" type summary.

### MAP estimate

The MAP estimate is the parameter value at which the posterior density is largest:

$$
\hat{\theta}_{\mathrm{MAP}}=\arg\max_{\theta} p(\theta\mid D).
$$

Because the posterior is proportional to likelihood times prior,

$$
p(\theta\mid D)\propto p(D\mid \theta)p(\theta),
$$

MAP is the parameter value that maximizes the product of data fit and prior preference.

This is a mode, not an average. It identifies the highest point of the posterior surface. That is a very different operation from averaging over the whole surface.

### MLE

The MLE ignores the prior entirely and optimizes only the likelihood:

$$
\hat{\theta}_{\mathrm{MLE}}=\arg\max_{\theta} p(D\mid \theta).
$$

So if the prior is flat or weak over the relevant region, MAP and MLE may end up close. But conceptually they are still solving different problems. MLE asks for best data fit within the model family. MAP asks for the highest posterior point after prior information has been incorporated.

### Why these summaries differ

The easiest way to separate them is by the question each one answers.

- **MLE:** Which parameter value fits the observed data best?
- **MAP:** Which parameter value has the highest posterior density after combining prior and data?
- **Posterior mean:** If I average parameter values under the whole posterior distribution, where is the center?

These are not cosmetic differences. In skewed posteriors, multimodal posteriors, or strongly regularized settings, the three numbers can differ substantially.

So the correct learning order is: first understand the posterior as a distribution; only then ask which summary, if any, is appropriate for the decision you care about.

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

Up to now, the question has mostly been: **within one model family, which parameter values fit the observed data well?** Model comparison changes the level of the question. We are no longer choosing only a parameter value. We are choosing among whole model families.

That distinction is easy to overlook, but it matters. MLE answers an optimization question **inside** a model. Model evidence answers an averaging question **over** the parameter space of a model.

Let $M$ denote a model family. The model evidence is

$$
p(D\mid M)=\int p(D\mid \theta,M)p(\theta\mid M)\,d\theta,
$$

or a sum in a discrete parameter space.

This formula should be read as follows. For each possible parameter value $\theta$ inside model $M$, the likelihood says how well that parameter fits the observed data, and the prior says how much weight that parameter value receives inside the model. The evidence averages those likelihood values over the entire parameter space.

That is the central conceptual contrast with MLE. MLE asks only for the single best-fitting parameter value. Evidence asks how well the **model as a whole** supports the data after averaging across its admissible parameter values.

### Why evidence naturally penalizes excessive flexibility

A flexible model can often achieve a very high likelihood at one specially tuned parameter value. But that fact alone does not imply that the model family is broadly supported by the data. If most parameter values in that flexible family fit badly, then the average support can still be low.

This is why evidence contains a built-in complexity penalty. A model does not win merely because it has one sharp peak of excellent fit. It must devote a meaningful portion of its parameter space to fitting the data well. In that sense, evidence rewards models that fit well **robustly**, not just models that can fit well **somewhere**.

### BIC as an approximation

The Bayesian information criterion, or BIC, is a large-sample approximation related to log evidence. In one common convention,

$$
\mathrm{BIC}=\log p(D\mid \hat{\theta}_{\mathrm{MLE}},M)-\frac{k}{2}\log m,
$$

up to sign and convention differences across sources.

The structure matters more than the exact convention. One term rewards fit at the best-fitting parameter value. The other term penalizes the number of free parameters $k$, with a penalty that depends on sample size $m$.

So BIC is not trying to replace evidence philosophically. It is trying to cheaply mimic the key idea that better fit must be weighed against greater flexibility.

### The question evidence answers

Suppose one model uses one Bernoulli parameter for all coin flips, while another uses two Bernoulli parameters for two subgroups. The two-parameter model is more flexible, so its best possible likelihood cannot be worse. But that does not settle the comparison. The real issue is whether the extra flexibility earns enough additional explanatory power to justify the larger parameter space.

That is exactly the kind of question evidence and BIC are built to answer. They move the discussion from "which parameter fits best?" to "which model family deserves more support after accounting for both fit and flexibility?"

---

## 18. What to retain

The conceptual heart of this section is the distinction between objects that share notation but answer different questions. The sampling model tells you how data behave when the parameter is fixed. The likelihood reuses the same algebraic expression but turns it into a scoring function over parameter values once the data are fixed. The MLE selects the parameter that gives the observed sample the best in-family fit. Bayesian inference then adds a prior and returns a posterior distribution, not merely a point estimate.

The standard MLE examples are worth retaining not just for their formulas, but for the pattern they illustrate. In common model families, maximum likelihood often pushes the model to match the empirical summaries that the family is designed to encode. Bernoulli matches success frequency, Gaussian mean matches sample mean, and categorical probabilities match empirical proportions.

The second major lesson is that not all "best" notions mean the same thing. MLE, MAP, and posterior mean can all be reasonable summaries, but they summarize different objects and solve different problems. Likewise, best fit within a model family is not the same as best support for a model family as a whole. That is why evidence and BIC are needed.

## 19. Do not confuse

Do not confuse $p(D\mid \theta)$ with $p(\theta\mid D)$. The first is likelihood when read as a function of $\theta$ for fixed data; the second is a posterior distribution and requires a prior and normalization.

Do not describe likelihood as "the probability that the parameter is true." Likelihood is not a probability distribution over parameter values.

Do not confuse the estimator with the parameter being estimated. An estimator is a rule; its realized output on one dataset is an estimate.

Do not confuse MLE with MAP. MLE ignores the prior. MAP incorporates it.

Do not confuse posterior mode with posterior mean. A mode is the highest point of a distribution; a mean is an average over the whole distribution.

Do not confuse best fit at one parameter value with support for a model family as a whole. Evidence averages across parameter space; MLE does not.

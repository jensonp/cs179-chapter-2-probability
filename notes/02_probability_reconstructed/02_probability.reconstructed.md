# Probability and Inference

Source: source/02_probability.pdf

This is a full note-style reconstruction of Chapter 2. It keeps the chapter's section structure, worked examples, key tables, and core derivations, while normalizing some prose and keeping the main visuals in the local assets/ directory.

## 2.1 Probability, Events, Random Variables

Probability is the language we use when a system is uncertain or too complex to model exactly. In AI, the uncertainty often comes less from true randomness than from missing information and limited modeling power. A useful probabilistic model does two things: it describes our assumptions about the world, and it gives rules for combining evidence and updating those assumptions when observations arrive.

### Axioms of Probability

Let $S$ denote the event space, the set of all possible outcomes or possible worlds. A random event is any subset $A \subseteq S$. A probability measure assigns values to events and must satisfy:

$$
0 \le Pr[A] \le 1
$$

$$
Pr[S] = 1
$$

$$
Pr[\varnothing] = 0
$$

$$
Pr[A \cup B] = Pr[A] + Pr[B] - Pr[A \cap B]
$$

The last rule is inclusion-exclusion: add the worlds where $A$ happens and the worlds where $B$ happens, then subtract the overlap because it was counted twice.

### Example 2-1: Random Events

Suppose we roll a standard six-sided die. The event space is

$$
S = \{1,2,3,4,5,6\}.
$$

Two events are:

$$
A = \{\text{odd roll}\} = \{1,3,5\}
$$

$$
B = \{\text{roll is 4 or greater}\} = \{4,5,6\}.
$$

Then $Pr[A] = 3/6$, $Pr[B] = 3/6$, and $Pr[A \cap B] = 1/6$, so $Pr[A \cup B] = 5/6$.

### Random Variables

A random variable partitions the event space into disjoint and exhaustive cases and assigns each case a symbolic value. If

$$
X \in \{1,\dots,d\},
$$

then the events $X = 1, \dots, X = d$ are mutually exclusive and cover all outcomes, so

$$
\sum_{i=1}^d Pr[X=i] = 1.
$$

The possible values are called the states of the variable, and the set of all possible values is its domain. For discrete variables, the probability mass function is often written as $p(X=x)$ or simply $p(x)$ when the variable is clear from context.

### Example 2-2: Bernoulli Distribution

A Bernoulli random variable is binary:

$$
X \in \{0,1\}.
$$

If

$$
Pr[X=1] = \rho,
$$

then automatically

$$
Pr[X=0] = 1-\rho.
$$

We can write the distribution as

$$
p(X) = Ber(X;\rho) = \rho^X (1-\rho)^{1-X}.
$$

This evaluates to $\rho$ when $X = 1$ and to $1-\rho$ when $X = 0$.

An equivalent representation is

$$
p(X) = \rho \mathbf{1}[X=1] + (1-\rho)\mathbf{1}[X=0].
$$

### Example 2-3: Discrete Distribution

If $X \in \{1,\dots,d\}$, then a discrete distribution is just a probability table:

$$
Pr[X=i] = \rho_i, \qquad \rho_i \ge 0, \qquad \sum_{i=1}^d \rho_i = 1.
$$

Only $d-1$ of those values are free, because the last one is determined by normalization. One compact representation is

$$
p(X) = \prod_{i=1}^d \rho_i^{\mathbf{1}[X=i]}.
$$

This simply selects the probability attached to the realized state and turns the others off.

### Example 2-4: Dentist Example

The chapter uses three binary variables:

- $C = 1$ means cavity
- $T = 1$ means toothache
- $D = 1$ means the probe catches on the tooth

The joint distribution over $(T,D,C)$ is:

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

The eight rows are mutually exclusive and exhaustive, so their probabilities sum to one.

### Marginal Probabilities

To get the probability of one variable, add up all joint entries consistent with that value.

$$
p(T=0) = \sum_{d,c} p(T=0,D=d,C=c)
$$

$$
= 0.576 + 0.008 + 0.144 + 0.072 = 0.80.
$$

Marginalization is just "add all ways the event can happen."

### Conditional Probability

Conditioning means restricting attention to worlds where the condition holds:

$$
p(D=d \mid T=t) = \frac{p(D=d,T=t)}{p(T=t)}.
$$

The numerator is the probability that both things happen; the denominator is the total probability of the condition. The result is a normalized probability distribution over $D$ given $T=t$.

### Example 2-5: Bayes Rule

Bayes rule converts a forward model into a reverse one:

$$
p(C=c \mid D=d) = \frac{p(D=d \mid C=c)p(C=c)}{p(D=d)}.
$$

Read it as:

$$
\text{posterior} = \text{likelihood} \cdot \text{prior} / \text{evidence}.
$$

For the dentist example, suppose:

$$
p(T=1 \mid C=0) = 0.1, \qquad p(T=1 \mid C=1) = 0.6
$$

$$
p(C=0) = 0.8, \qquad p(C=1) = 0.2.
$$

Then

$$
p(C=1 \mid T=1)
= \frac{0.6 \cdot 0.2}{0.6 \cdot 0.2 + 0.1 \cdot 0.8}
= \frac{0.12}{0.20}
= 0.60.
$$

Observing a toothache raises the cavity probability from $0.20$ to $0.60$.

### Example 2-6: Table-Based Computation

The same Bayes update can be done by manipulating tables directly. Start with the full table of $p(T,D,C)$, extract the subtable where $T=1$, sum over $D$, then normalize.

<!-- table-stack:start -->
<table border="0" cellpadding="0" cellspacing="16">
  <tbody>
    <tr>
      <td valign="top">
        <p><strong>Restrict to <i>T</i> = 1</strong></p>
        <table>
          <thead>
            <tr>
              <th><i>DC</i></th>
              <th><i>p(T = 1, D, C)</i></th>
            </tr>
          </thead>
          <tbody>
            <tr><td>00</td><td>0.064</td></tr>
            <tr><td>01</td><td>0.012</td></tr>
            <tr><td>10</td><td>0.016</td></tr>
            <tr><td>11</td><td>0.108</td></tr>
          </tbody>
        </table>
      </td>
      <td valign="top">
        <p><strong>Marginalize over <i>D</i></strong></p>
        <table>
          <thead>
            <tr>
              <th><i>C</i></th>
              <th><i>p(T = 1, C)</i></th>
            </tr>
          </thead>
          <tbody>
            <tr><td>0</td><td>0.064 + 0.016 = 0.080</td></tr>
            <tr><td>1</td><td>0.012 + 0.108 = 0.120</td></tr>
          </tbody>
        </table>
      </td>
      <td valign="top">
        <p><strong>Normalize</strong></p>
        <table>
          <thead>
            <tr>
              <th><i>C</i></th>
              <th><i>p(C | T = 1)</i></th>
            </tr>
          </thead>
          <tbody>
            <tr><td>0</td><td>0.08 / 0.20 = 0.40</td></tr>
            <tr><td>1</td><td>0.12 / 0.20 = 0.60</td></tr>
          </tbody>
        </table>
      </td>
    </tr>
  </tbody>
</table>
<!-- table-stack:end -->

This is the same computation as Bayes rule, but expressed as table arithmetic.

### Expectation

The expectation of a discrete variable is a weighted average:

$$
E[X] = \sum_x x \, p(x).
$$

For a Bernoulli variable, $E[X] = \rho$, which is why the Bernoulli parameter is also the mean.

### Independence

Two random variables $X$ and $Y$ are independent if

$$
p(X,Y) = p(X)p(Y).
$$

Equivalently, observing one does not change the distribution of the other:

$$
p(X \mid Y) = p(X).
$$

Independence also simplifies the joint distribution. If $X$ and $Y$ are $d$-ary variables, the full joint has $d^2 - 1$ degrees of freedom, while independence reduces that to $2d - 2$.

### Example 2-7: Independence

Let $X$ be a biased coin and $Y$ a weighted four-sided die. If they are independent, then the joint is just the product of the marginals.

| $X$ | $p(X)$ |
|---|---:|
| 0 | 0.7 |
| 1 | 0.3 |

| $Y$ | $p(Y)$ |
|---|---:|
| 1 | 0.2 |
| 2 | 0.3 |
| 3 | 0.4 |
| 4 | 0.1 |

Representative joint entries:

| $X$ | $Y$ | $p(X,Y)$ |
|---|---|---:|
| 0 | 1 | 0.14 |
| 0 | 2 | 0.21 |
| 1 | 4 | 0.03 |

### Conditional Independence

It is rare for variables to be completely independent, but they are often conditionally independent given a mediating variable $Z$:

$$
p(X,Y \mid Z) = p(X \mid Z)p(Y \mid Z).
$$

Once $Z$ is known, $X$ and $Y$ stop giving extra information about each other.

### Example 2-8: Conditional Independence, Dentist

In the dentist model, the probe catches and toothache are not independent in general. But conditioned on cavity status, they become independent. The conditional table is:

| $T$ | $D$ | $C$ | $p(D \mid C,T)$ |
|---|---|---|---:|
| 0 | 0 | 0 | 0.800 |
| 0 | 0 | 1 | 0.100 |
| 0 | 1 | 0 | 0.200 |
| 0 | 1 | 1 | 0.900 |
| 1 | 0 | 0 | 0.800 |
| 1 | 0 | 1 | 0.100 |
| 1 | 1 | 0 | 0.200 |
| 1 | 1 | 1 | 0.900 |

The key point is that $p(D \mid C,T)$ does not actually depend on $T$.

## 2.2 Continuous Random Variables

Sometimes we model systems with real-valued random variables $X \in \mathbb{R}$. In that setting we define a probability density function $p(x)$ with $p(x) \ge 0$ for all $x$ and

$$
\int p(x)\,dx = 1.
$$

The density defines the probability of any event $X \in A \subseteq \mathbb{R}$ by

$$
Pr[X \in A] = \int_A p(x)\,dx.
$$

This is the first major structural difference from the discrete case. For a continuous variable, the number $p(x)$ is not the probability of the event $X=x$; in fact $Pr[X=x]=0$ for every individual point. A density only becomes a probability after integrating it over an interval or region. That is why a density is allowed to exceed one locally, provided the total area under the curve is still one.

### Example 2-9: Uniform Distribution

For a continuous-valued random variable $X$ defined on $[0,T]$, the uniform distribution is

$$
p(x) =
\begin{cases}
\frac{1}{T} & \text{if } x \in [0,T] \\
0 & \text{otherwise.}
\end{cases}
$$

Then

$$
\int_0^T p(x)\,dx = T \cdot \frac{1}{T} = 1.
$$

Unlike discrete distributions, the density value may be larger than one, as long as its integral over the support is one. The important normalization object is area, not height.

### Gaussian Distributions

The Gaussian distribution is one of the most important continuous families. In one dimension,

$$
p(x) = \mathcal{N}(x;\mu,\sigma^2)
= \frac{1}{\sqrt{2\pi\sigma^2}}
\exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right).
$$

In multiple dimensions,

$$
p(x) = \mathcal{N}(x;\mu,\Sigma)
= (2\pi)^{-n/2} |\Sigma|^{-1/2}
\exp\!\left(-\frac{1}{2}(x-\mu)^T \Sigma^{-1}(x-\mu)\right).
$$

The mean vector $\mu$ sets the center, and the covariance matrix $\Sigma$ sets the shape and spread. The quadratic term $(x-\mu)^T \Sigma^{-1}(x-\mu)$ is the squared Mahalanobis distance from $x$ to the mean, measured in the geometry induced by $\Sigma$. In two dimensions, the level sets of constant density are ellipses; in higher dimensions, they are ellipsoids. For this formula to define a proper density, $\Sigma$ must be symmetric and positive definite, so that the quadratic form is nonnegative, the inverse exists, and the determinant term $|\Sigma|^{-1/2}$ is well-defined.

![Gaussian distribution plots](assets/figure_2_1_gaussian.png)

The three panels show the same family viewed three ways. The one-dimensional curve emphasizes how the mean shifts location and the standard deviation changes spread. The surface plot shows the bivariate density as height over the plane. The contour plot removes the height dimension and keeps only level sets, which is often the most useful representation when reasoning about covariance structure.

### Example 2-10: Bernoulli Exponential Family Form

The Bernoulli distribution can be written in exponential-family form:

$$
\rho^X (1-\rho)^{1-X}
= \exp\!\Bigl(\log(\rho)X + \log(1-\rho)(1-X)\Bigr).
$$

This highlights the feature $\phi(X)=X$ and the natural parameter $\eta = \log(\rho/(1-\rho))$. Writing Bernoulli in this way makes the log-odds parameter explicit and shows how a nonlinear parameter such as $\rho$ becomes a linear coefficient in the exponent.

### Example 2-11: Bernoulli Two-Parameter Form

We can also write an over-parameterized Bernoulli distribution with two parameters:

$$
p(X;\eta_0,\eta_1)
= \frac{\exp\bigl(\eta_1 X + \eta_0(1-X)\bigr)}{\exp(\eta_0)+\exp(\eta_1)}.
$$

Only the difference $\eta_1 - \eta_0$ matters, so different parameter values can represent the same distribution. This is an explicit structural redundancy: the model has two coordinates, but the actual Bernoulli family still has only one degree of freedom.

### Beta and Dirichlet Distributions

Another important continuous distribution is the Beta distribution on $[0,1]$:

$$
p(x) = \mathrm{Beta}(x;a,b)
= \frac{\Gamma(a+b)}{\Gamma(a)\Gamma(b)} x^{a-1}(1-x)^{b-1}.
$$

The Gamma-function ratio is the normalization constant that forces the integral over $[0,1]$ to equal one. When $a=b=1$, the Beta distribution is uniform. When $a,b > 1$, it is unimodal and places most of its mass in the interior. When either parameter is less than one, the density can spike at the boundary. That does not violate probability rules, because the integral over any interval is still finite even if the pointwise density becomes very large near $0$ or $1$.

The Dirichlet distribution generalizes Beta to vectors on the simplex:

$$
p(x) = \mathrm{Dir}(x;\alpha)
= \frac{\Gamma(\sum_j \alpha_j)}{\prod_j \Gamma(\alpha_j)}
\prod_j x_j^{\alpha_j - 1},
$$

with $x_j \ge 0$ and $\sum_j x_j = 1$. The simplex constraint means the domain has one fewer free dimension than the number of coordinates: once $x_1,\dots,x_{d-1}$ are chosen, the last coordinate is fixed by normalization. When all concentration parameters are large and equal, the mass sits near the center of the simplex; when some coordinates of $\alpha$ are less than one, the density shifts toward edges or corners. For $d=2$, Dirichlet reduces exactly to Beta, so Beta is the one-dimensional simplex case.

![Beta distribution family](assets/figure_2_2_beta_grid.png)

![Dirichlet distribution family](assets/figure_2_3_dirichlet_simplex.png)

The Beta grid makes the parameter effects explicit: symmetric parameters above one create a peak in the middle, while parameters below one push mass toward the boundaries. The Dirichlet simplex panels show the same phenomenon in two free dimensions. Mass near the center means balanced proportions; mass near an edge or corner means one or more coordinates are favored strongly.

### The Exponential Family

The distributions discussed so far are examples of the exponential family:

$$
p(x;\theta) = h(x)\exp\!\bigl(\theta^T \phi(x) - A(\theta)\bigr).
$$

The vector $\phi(x)$ contains the sufficient statistics, $h(x)$ is the base measure, $\theta$ is the natural parameter, and $A(\theta)$ is the log-partition function

$$
A(\theta) = \log \int h(x)\exp\!\bigl(\theta^T\phi(x)\bigr)\,dx.
$$

Writing the model this way makes the structure explicit: the log-density is affine in the fixed feature vector $\phi(x)$, while all normalization is absorbed into $A(\theta)$. That structure is what gives exponential families their clean moment-matching and convexity properties. It is also a genuine limitation: only distributions whose log-density can be expressed using a fixed finite-dimensional feature map belong to a finite-dimensional exponential family.

## 2.3 Learning and Parameter Estimation

In practice, we often do not know the probabilities that govern a system. Instead, we observe data and estimate the model parameters from those observations.

### Frequentist Versus Bayesian Perspectives

From the frequentist perspective, probability is long-run frequency. The parameter is fixed but unknown, data are random, and learning means estimating the true parameter from samples.

From the Bayesian perspective, probability is degree of belief. The parameter itself is uncertain, so we place a prior distribution on it and update that prior after seeing data.

Both views use many of the same formulas, but they answer slightly different questions. A frequentist estimator asks, "if nature chose a fixed parameter, what rule should I use to estimate it?" A Bayesian posterior asks, "after observing this concrete data set, which parameter values remain plausible and how plausible are they relative to one another?" Maximum likelihood is the canonical frequentist estimator because it ignores prior beliefs and keeps only the data-fit term.

### Likelihood

For i.i.d. data $D = {x^{(1)}, \dots, x^{(m)}}$, the likelihood is

$$
p(D;\theta) = \prod_i p(x^{(i)};\theta)
$$

and the log-likelihood is

$$
L(\theta) = \sum_i \log p(x^{(i)};\theta).
$$

The principle of maximum likelihood says to choose the parameter value that makes the observed data look most probable. It is important to state explicitly what varies and what stays fixed: after we have observed $D$, the data are treated as fixed, and the likelihood is a function of $\theta$. It is not a probability distribution over $\theta$, and it does not have to integrate to one over parameter space.

### Example 2-12: Bernoulli Likelihood

Suppose we observe $m$ Bernoulli samples, with $m_1$ ones and $m_0$ zeros. Then

$$
L(\rho) = m_1 \log \rho + m_0 \log(1-\rho).
$$

The likelihood is maximized at the empirical frequency of ones. If the observed sample is all zeros or all ones, the maximizer lies on the boundary $\rho=0$ or $\rho=1$. Otherwise the unique optimum lies in the interior of the interval.

![Bernoulli likelihood curves](assets/figure_2_12_bernoulli_likelihood.png)

Each panel holds the observed data fixed and varies only the parameter $\rho$. The curve peaks where the model's predicted head probability best matches the observed proportion of heads. When the data rule out part of parameter space completely, the log-likelihood drops toward negative infinity at the incompatible boundary.

### Example 2-13: Gaussian Likelihood

For a one-dimensional Gaussian with variance fixed at one, the likelihood as a function of $\mu$ becomes more sharply peaked as the number of samples grows. That sharpening is the visual signature that more data reduce parameter uncertainty: many values of $\mu$ may explain three observations reasonably well, but far fewer values remain plausible once twenty observations cluster around the same region.

![Gaussian likelihood curves](assets/figure_2_13_gaussian_likelihood.png)

The dots along the top of each panel are the observed samples. The curve below them is the log-likelihood as a function of the Gaussian mean. As $m$ increases, the curve narrows and the maximizing value moves toward the visual center of the observed data cloud.

### Maximum Likelihood Estimation

For a Bernoulli distribution,

$$
L(\rho) = m_1 \log \rho + m_0 \log(1-\rho).
$$

Differentiating gives

$$
\frac{\partial L}{\partial \rho} = \frac{m_1}{\rho} - \frac{m_0}{1-\rho}.
$$

Setting this to zero yields

$$
\hat\rho_{\text{MLE}} = \frac{m_1}{m}.
$$

The algebra is worth writing out explicitly:

$$
\frac{m_1}{\rho} - \frac{m_0}{1-\rho} = 0
\quad \Longrightarrow \quad
m_1(1-\rho) = m_0\rho
\quad \Longrightarrow \quad
m_1 = (m_0+m_1)\rho.
$$

Since $m_0+m_1 = m$, we obtain $\hat\rho_{\text{MLE}} = m_1/m$. The second derivative is

$$
\frac{\partial^2 L}{\partial \rho^2}
= -\frac{m_1}{\rho^2} - \frac{m_0}{(1-\rho)^2} < 0,
$$

so the stationary point is a strict global maximum whenever it lies in the interior.

For a Gaussian with mean $\mu$ and variance $\nu = \sigma^2$,

$$
\hat\mu_{\text{MLE}} = \frac{1}{m}\sum_i x^{(i)}
$$

$$
\hat\nu_{\text{MLE}} = \frac{1}{m}\sum_i (x^{(i)} - \hat\mu)^2.
$$

For the mean parameter, the derivation comes from expanding the log-likelihood into a constant minus a squared-error term:

$$
L(\mu) = \text{const} - \frac{1}{2\nu}\sum_i (x^{(i)}-\mu)^2.
$$

Differentiating with respect to $\mu$ gives

$$
\frac{\partial L}{\partial \mu}
= \frac{1}{\nu}\sum_i (x^{(i)}-\mu),
$$

so setting the derivative to zero forces $\mu$ to equal the arithmetic average of the observations. The variance estimate is then the average squared deviation around that fitted mean. For a discrete distribution with probabilities $\rho_x$, the MLE is the empirical frequency of each state.

### Example 2-14: Bernoulli MLE

If $m_1$ of the $m$ observations are ones, then

$$
\hat\rho = \frac{m_1}{m}.
$$

### Example 2-15: Gaussian MLE

The Gaussian MLE is the sample mean and sample variance:

$$
\hat\mu = \frac{1}{m}\sum_i x^{(i)},
$$

$$
\hat\nu = \frac{1}{m}\sum_i (x^{(i)}-\hat\mu)^2.
$$

### Example 2-16: Discrete MLE

For a discrete distribution over states $x$, the MLE is

$$
\hat\rho_x = \frac{m_x}{m},
$$

where $m_x$ is the count of state $x$ in the data.

### Maximum Likelihood and Exponential Families

For a canonical exponential-family model

$$
p(x;\theta) = h(x)\exp\!\bigl(\theta^T \phi(x) - A(\theta)\bigr),
$$

the log-likelihood of i.i.d. data is

$$
L(\theta)
= \sum_i \log h(x^{(i)})
+ \theta^T \sum_i \phi(x^{(i)})
 - m A(\theta).
$$

Differentiating with respect to $\theta$ gives

$$
\nabla_\theta L(\theta)
= \sum_i \phi(x^{(i)}) - m \nabla_\theta A(\theta).
$$

For exponential families,

$$
\nabla_\theta A(\theta) = E_\theta[\phi(X)],
$$

so the first-order optimality condition becomes

$$
\frac{1}{m}\sum_i \phi(x^{(i)}) = E_\theta[\phi(X)].
$$

This is the explicit moment-matching statement: the fitted model reproduces the empirical averages of the sufficient statistics. That identity is one of the main reasons exponential families are so useful.

### Overfitting

Likelihood alone can overfit. If a model is too flexible and the data set is too small, the MLE may explain the training data perfectly while generalizing poorly. Histogram models make this especially clear: as the number of bins grows, the likelihood on the training data can keep increasing even when the estimate becomes a bad predictor. In the extreme limit where each observation gets its own tiny bin, the model can memorize the sample rather than discover a stable distributional pattern.

![Histogram likelihood progression](assets/figure_2_17_histograms.png)

The three histograms make the overfitting mechanism visible. With one bin the model is too coarse to capture any structure. With a moderate number of bins it starts to reflect the sample without becoming too brittle. With too many bins it effectively memorizes the observations, assigning high density exactly where data occurred and poor predictions everywhere else.

### Posterior Distributions

In the Bayesian view, we keep a distribution over parameters:

$$
p(\theta \mid D) \propto p(D \mid \theta)p(\theta).
$$

The missing normalization constant is the evidence

$$
p(D) = \int p(D \mid \theta)p(\theta)\,d\theta.
$$

So Bayes' rule in full form is

$$
p(\theta \mid D) = \frac{p(D \mid \theta)p(\theta)}{p(D)}.
$$

The posterior trades a point estimate for uncertainty about plausible parameter values. This is conceptually important and computationally consequential: exact inference is easy only when the evidence integral can be computed analytically or when the prior-likelihood pair has a conjugate form.

### Example 2-18: Beta-Bernoulli Conjugacy

If the likelihood is Bernoulli and the prior is $Beta(a,b)$, then the posterior is still Beta:

$$
\rho \mid D \sim Beta(a+m_1, b+m_0).
$$

The derivation is short enough to write explicitly. The prior contributes

$$
p(\rho) \propto \rho^{a-1}(1-\rho)^{b-1},
$$

and the Bernoulli likelihood contributes

$$
p(D \mid \rho) \propto \rho^{m_1}(1-\rho)^{m_0}.
$$

Multiplying them gives

$$
p(\rho \mid D) \propto \rho^{a+m_1-1}(1-\rho)^{b+m_0-1},
$$

which is exactly the kernel of another Beta density. This is the simplest example of conjugacy.

### Posterior Estimators

Two common point estimates derived from the posterior are the posterior mean and the MAP estimate:

$$
\hat\theta_{\text{PM}} = E_{p(\theta \mid D)}[\theta],
$$

$$
\hat\theta_{\text{MAP}} = \arg\max_\theta \log p(\theta \mid D).
$$

For Bernoulli/Beta,

$$
\hat\rho_{\text{PM}} = \frac{a+m_1}{a+b+m_1+m_0}
$$

and

$$
\hat\rho_{\text{MAP}} = \frac{a-1+m_1}{a+b-2+m_1+m_0}.
$$

The posterior mean averages with respect to the full posterior and therefore always exists for $a,b>0$. The MAP estimator is different: it looks for the mode of the posterior density, and if either updated shape parameter is at most one, the mode moves to the boundary rather than the interior. That boundary behavior is another structural feature that is easy to miss if one only memorizes the closed form.

### Example 2-19: Bernoulli Posterior Estimates

The posterior mean smooths the empirical frequency by the prior. The MAP estimate is a regularized version of MLE and matches MLE when $a=b=1$. In effect, the prior acts like pseudo-counts: $a-1$ prior successes and $b-1$ prior failures for the MAP formula, or $a$ and $b$ for the posterior mean formula.

### Sequential Belief Updating

Bayesian updating naturally supports sequential learning: after observing one batch of data, the posterior becomes the prior for the next batch.

![Sequential belief updating](assets/figure_2_4_sequential_updates.png)

The figure is deliberately procedural: first combine the prior with the first data batch, then treat the resulting posterior as the next prior before incorporating the second batch. Nothing conceptually new happens in the second step; Bayesian learning is the repeated application of the same update rule.

### Example 2-20: Coin Toss Hyper-Prior

Sometimes we are uncertain even about the prior. A mixture of a fair-coin prior and a trick-coin prior can be written as a hyper-prior over the Beta parameters. This adds one more layer to the model hierarchy: first choose which prior family is active, then draw the Bernoulli parameter from that prior, and only then generate the data.

![Mixture of Beta priors](assets/figure_2_20_beta_hyperprior.png)

The left and middle components encode two qualitatively different prior stories: one centered near a fair coin and one concentrated near the extremes. The mixture panel makes the uncertainty over priors visible by averaging those stories before any data are observed.

### Weakly Informative Priors

A prior is never literally uninformative, because any prior expresses some preference over parameter values. The choice of parameterization matters: a prior that is uniform in $\rho$ is not uniform in the natural parameter $\eta = \log(\rho/(1-\rho))$. So "uninformative" is not an intrinsic property of a density alone; it is a statement about a density together with the coordinate system in which it is declared flat.

### Example 2-21: Priors for the Bernoulli Likelihood

The uniform prior on $\rho$ is $Beta(\rho;1,1)$. Under a log-odds parameterization, the induced prior on $\eta$ is not uniform. This is one reason the notion of "uninformative prior" is parameterization-dependent.

### Bayesian Model Selection

The Bayesian marginal likelihood is

$$
\log p(D) = \log \int p(D \mid \theta)p(\theta)\,d\theta.
$$

It automatically penalizes overly flexible models that spread prior mass too thinly. This happens because the marginal likelihood averages $p(D \mid \theta)$ over the prior rather than looking only at the single best parameter value. A highly flexible model can fit some parameter settings extremely well, but if most of its prior mass corresponds to poor fits, the average score can still be small.

The BIC approximation is

$$
L_{\text{BIC}} = \max_\theta \log p(D \mid \theta) - \frac{d}{2}\log m,
$$

where $d$ is the number of parameters and $m$ is the number of observations.

### Example 2-22: Bayesian Histogram Estimator

For a histogram model with Dirichlet prior, the marginal likelihood and BIC penalized score can be compared across numbers of bins. Both typically favor a moderate number of bins rather than the most complex possible histogram. The explicit structural tradeoff is between approximation error and variance: too few bins smear away genuine structure, while too many bins spend parameters modeling sampling noise.

![Histogram model selection scores](assets/figure_2_22_histogram_model_scores.png)

The plotted curves separate three notions of fit. Raw maximum likelihood keeps rewarding additional flexibility. BIC and the marginal score include an explicit complexity penalty, so they flatten or decline once the extra bins stop being justified by the amount of data.

## 2.4 Convexity

A convex function satisfies

$$
f(\alpha x + (1-\alpha)x') \le \alpha f(x) + (1-\alpha)f(x')
$$

for all $\alpha \in [0,1]$. Strict convexity makes the inequality strict for distinct points.

Equivalent characterizations are:

$$
f(x') \ge f(x) + \nabla f(x)\cdot(x'-x)
$$

and, when second derivatives exist,

$$
\nabla^2 f(x) \succeq 0.
$$

Convex functions are useful because every local minimum is global, and a strictly convex function has a unique minimum. Positive semidefinite curvature allows flat directions, so multiple minimizers can still exist. Positive definite curvature removes those flat directions and forces uniqueness.

Jensen's inequality is the probability version of convexity:

$$
E[f(X)] \ge f(E[X])
$$

for convex $f$.

### Example 2-23: Convexity and the Exponential Family

The negative log-likelihood of a canonical exponential-family model is convex in its natural parameters. The reason is explicit:

$$
\frac{\partial A(\theta)}{\partial \theta_j} = E_\theta[\phi_j(X)],
\qquad
\frac{\partial^2 A(\theta)}{\partial \theta_j \partial \theta_k}
= \mathrm{Cov}_\theta(\phi_j(X), \phi_k(X)).
$$

The Hessian of the log-partition function is therefore a covariance matrix of the sufficient statistics, hence positive semidefinite. Once the terms that are constant or linear in $\theta$ are separated out, the remaining negative log-likelihood inherits that convexity.

![Convexity sketch](assets/figure_2_23_convexity_sketch.png)

The blue secant line lies above the black graph, which is the geometric definition of convexity. The red tangent line lies below the graph, which is the first-order equivalent statement. These are not separate ideas; they are two views of the same structural property.

## 2.5 Information Theory

Entropy measures uncertainty:

$$
H[X] = -\sum_x p(x)\log p(x).
$$

If the logarithm is base 2, entropy is measured in bits. A deterministic variable has entropy zero, and a uniform distribution maximizes entropy for a fixed finite support. Entropy is therefore not just "randomness" in an informal sense; it is the expected code length of the optimal lossless code and the expected information revealed by one observation.

### Example 2-24: Entropy

For a fair coin,

$$
H[X] = -0.5\log_2 0.5 - 0.5\log_2 0.5 = 1 \text{ bit}.
$$

For a fair die,

$$
H[X] = -6 \cdot \frac{1}{6}\log_2 \frac{1}{6} \approx 2.58 \text{ bits}.
$$

### Example 2-25: Lottery

Entropy also explains compression. If a yearly sequence is mostly zeros, we can encode it with far fewer bits than a naive one-bit-per-day representation, because the sequence is highly non-random.

### Kullback-Leibler Divergence

The KL divergence is

$$
D(p \,\|\, q) = \sum_x p(x)\log\frac{p(x)}{q(x)}.
$$

It is always nonnegative and zero only when $p=q$, but it is not symmetric. There is also an important support condition: if $q(x)=0$ for some $x$ with $p(x)>0$, then the divergence is infinite, because $q$ assigns impossible status to an outcome that actually occurs under $p$.

In learning, maximum likelihood can be viewed as minimizing the KL divergence from the empirical distribution to the model family.

### Mutual Information

Mutual information measures how much observing one variable tells us about another:

$$
I[X,Y] = D(p(X,Y) \,\|\, p(X)p(Y))
= H[X] + H[Y] - H[X,Y].
$$

If $X$ and $Y$ are independent, mutual information is zero.

### Conditional Entropy

Conditional entropy is

$$
H[X \mid Y] = H[X,Y] - H[Y].
$$

Equivalently,

$$
H[X \mid Y] = \sum_y p(y) H[X \mid Y=y],
$$

so it is the average remaining uncertainty in $X$ after the value of $Y$ is revealed. It satisfies

$$
I[X,Y] = H[X] - H[X \mid Y] \ge 0,
$$

so conditioning reduces uncertainty on average.

### Example 2-26: Information and Conditional Entropy

Suppose we model commuting behavior $C \in \{\text{walk}, \text{bike}, \text{drive}\}$ and weather $R \in \{\text{clear}, \text{rain}\}$. On rainy days we drive more often, so weather conveys information about commute choice.

| $R$ | $C$ | $p(C \mid R)$ |
|---|---|---:|
| clear | walk | 0.9 |
| clear | bike | 0.1 |
| clear | drive | 0.0 |
| rain | walk | 0.5 |
| rain | bike | 0.0 |
| rain | drive | 0.5 |

With $p(R=\text{rain}) = 0.1$, the marginals are

$$
p(C=\text{walk}) = 0.86, \quad p(C=\text{bike}) = 0.09, \quad p(C=\text{drive}) = 0.05.
$$

The entropy of the commute alone is about $0.72$ bits. Conditioning on weather gives a lower average entropy, around $0.52$ bits, so the mutual information is about $0.2$ bits. Writing the quantities this way makes the interpretation explicit: knowing the weather removes about two-tenths of a bit of uncertainty about how the commute will happen.

## 2.6 Change-of-Variable Models

The classical probability distributions above are useful, but many real data sets do not fit those forms directly. A common technique is to define a new variable as an invertible transformation of a simpler base variable.

### Scalar Change of Variables

If $X = f(Z)$ is invertible and $g = f^{-1}$, then

$$
p_X(x) = p_Z(g(x)) \lvert g'(x) \rvert.
$$

The derivative corrects for stretching or compression under the transformation. A small interval around $x$ corresponds to an interval around $z=g(x)$ of width approximately $|g'(x)|dx$, so probability conservation forces the density to scale by that same factor. This formula requires invertibility on the region of interest; if the map has multiple inverse branches, the correct density is a sum over branches rather than a single Jacobian term.

### Example: Lognormal Distribution

If $Z = \log X$ is Gaussian, then $X$ is lognormal. The density of $X$ is obtained from the Gaussian density of $Z$ plus the Jacobian factor $1/x$, because $z=\log x$ implies $dz/dx = 1/x$. This is a concrete example of the general rule that multiplicative stretching in variable space becomes additive correction in log-density space.

### Multivariate Change of Variables

In multiple dimensions,

$$
p_X(x) = p_Z(g(x)) \lvert \det J_g(x) \rvert,
$$

where $J_g$ is the Jacobian matrix of the inverse transformation. The determinant plays the same role as $|g'(x)|$ in one dimension: it is the local volume scaling factor. If the transformation doubles area near one point, the density there must be cut in half to preserve total probability.

### Copula Models

Copulas separate marginal distributions from dependence structure. For two variables,

$$
Pr[X_1 \le x_1, X_2 \le x_2] = C(P_1(x_1), P_2(x_2)),
$$

where $P_1$ and $P_2$ are the marginal CDFs. This is the content of Sklar's theorem in the two-variable case: once the marginals are pushed into the uniform scale, the remaining object $C$ captures only dependence.

![Copula transforms](assets/figure_2_5_copula_transforms.png)

The Gaussian copula is a special case in which the transformed variables are Gaussian. The visual sequence shows the separation explicitly: start with the original marginals, map each one to a uniform scale, then map those uniform variables to a Gaussian scale where the dependence is easy to model.

### Example 2-27: Copula Transforms

The chapter uses a KDD Cup data set to show the pipeline. First estimate the marginal CDFs $P_1$ and $P_2$. Then transform each coordinate into a uniform variable by applying its own CDF. Then apply $\Phi^{-1}$ to map those uniform variables into Gaussian marginals. Finally fit a Gaussian dependence model in that transformed space. The resulting model can express complicated non-Gaussian marginals while keeping the dependence structure manageable.

### Normalizing Flows

Normalizing flows define an invertible transform $X = f(Z)$ and use the change-of-variables formula to evaluate likelihoods. The transformation is often built as a composition of simple steps:

$$
f(Z) = f_T(f_{T-1}(\cdots f_1(Z)))
$$

with

$$
\log p_X(X) = \log p_Z(f^{-1}(X)) - \sum_t \log |\det J_{f_t}|.
$$

The computational reason this works is that the Jacobian determinant of a composition decomposes into a sum in log-space. A flow is therefore practical only when each layer is invertible and has a determinant that can be evaluated cheaply.

### Example 2-28: Copula-Like Normalizing Flow

One useful construction is to start with a Gaussian base distribution and parameterize one-dimensional monotone transforms for each feature. This is a flexible stand-in for explicit CDF modeling. The monotonicity constraint is not optional: without it, the map would stop being invertible and the simple change-of-variables formula would break.

### Example 2-29: Conditional Affine Normalizing Flows

A particularly convenient flow layer is conditional affine:

$$
Z_1' = Z_1, \qquad Z_2' = \alpha_1(Z_1)Z_2 + \beta_1(Z_1).
$$

Because the Jacobian is triangular, the determinant is easy to compute: for the first layer it is simply $\alpha_1(Z_1)$, so the log-determinant is $\log |\alpha_1(Z_1)|$. A second layer can then swap roles and transform the other coordinate:

$$
Z_1'' = \alpha_2(Z_2')Z_1' + \beta_2(Z_2'), \qquad Z_2'' = Z_2'.
$$

![Normalizing flow deformation panels](assets/figure_2_6_affine_flow_panels.png)

The deformation panels show what the algebra means geometrically. A rectangular grid in latent space is progressively bent and stretched into a curved mesh in data space. The main idea is that a sequence of simple invertible layers can produce a complex density while keeping likelihood evaluation tractable. The structural limit is equally important: each layer must preserve invertibility, and in practice the scale functions are parameterized so they never cross zero.

## Summary

The chapter can be compressed into one sentence:

Probability gives us a language for uncertainty, learning tells us how to fit that language to data, and information/change-of-variables tools tell us how to analyze and extend those models once the basics are in place.

If you remember only the essentials, remember them as one connected chain rather than as isolated formulas. Marginals add over hidden cases, conditionals restrict to a subset of worlds and then renormalize, and Bayes' rule combines prior belief with evidence. Expectation turns a distribution into a weighted average. Maximum likelihood fits parameters by matching model predictions to empirical structure, while Bayesian inference keeps uncertainty over parameters instead of collapsing immediately to a single point estimate. Entropy measures uncertainty, KL divergence measures mismatch, and change-of-variables models reweight density by a Jacobian so that complex distributions can be built from simpler ones without losing exact probability accounting.

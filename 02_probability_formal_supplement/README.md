# Probability and Inference: Formal Supplement

Source: ../notes/02_probability_reconstructed/source/02_probability.pdf

This supplement collects the theorem-style statements, formal definitions, and compact derivations that support the main Chapter 2 note. The main note is written to stay readable as a lesson. This companion document makes the logical spine explicit.

## 1. Probability Spaces and Induced Objects

### Definition: Probability Space

A probability space is a triple

$$(\Omega,\mathcal{F},P),$$

where $\Omega$ is the sample space, $\mathcal{F}$ is a $\sigma$-algebra of events, and $P:\mathcal{F}\to[0,1]$ is a probability measure satisfying

$$P(\Omega)=1$$

and countable additivity:

$$P\!\left(\bigcup_{i=1}^{\infty} A_i\right)=\sum_{i=1}^{\infty} P(A_i)$$

whenever the events $A_i$ are pairwise disjoint.

In finite elementary settings one usually takes $\mathcal{F}=2^\Omega$, the full power set. In that case countable additivity reduces to the familiar finite-additivity bookkeeping used in the main note.

### Definition: Random Variable

A real-valued random variable is a measurable function

$$X:\Omega \to \mathbb{R}.$$

Measurability is the technical condition that ensures sets of the form

$$\{\omega \in \Omega : X(\omega)\le t\}$$

belong to $\mathcal{F}$ for every threshold $t$. This is what makes probabilities such as $P(X \le t)$ well defined.

### Definition: Distribution Function

The cumulative distribution function of $X$ is

$$F_X(x)=P(X \le x).$$

This object exists for every real-valued random variable. A PMF and a PDF do not always exist, but a CDF always does.

### Remark: PMF, PDF, and Mixed Laws

If the distribution of $X$ is concentrated on countably many values, one can define a probability mass function

$$p_X(x)=P(X=x).$$

If the distribution is absolutely continuous with respect to Lebesgue measure, one can define a density $f_X$ satisfying

$$P(X \in A)=\int_A f_X(x)\,dx.$$

Some distributions are mixed and contain both atoms and a continuous part. For those variables, the CDF is still the clean universal description, while a single ordinary density no longer captures the whole law.

## 2. Core Probability Identities

### Proposition: Inclusion-Exclusion

For any two events $A$ and $B$,

$$P(A \cup B)=P(A)+P(B)-P(A \cap B).$$

Proof. Decompose the union into disjoint pieces:

$$A \cup B = A \cup (B \setminus A).$$

Because the two pieces are disjoint,

$$P(A \cup B)=P(A)+P(B \setminus A).$$

Also,

$$P(B)=P(B \setminus A)+P(A \cap B).$$

Substituting the second identity into the first yields the result.

### Proposition: Product Rule

Whenever $P(B)>0$,

$$P(A,B)=P(A \mid B)P(B).$$

Likewise, whenever $P(A)>0$,

$$P(A,B)=P(B \mid A)P(A).$$

Proof. This is an immediate rearrangement of the definition

$$P(A \mid B)=\frac{P(A,B)}{P(B)}.$$

### Proposition: Law of Total Probability

If $B_1,\dots,B_k$ form a partition of $\Omega$ and each $P(B_i)>0$, then

$$P(A)=\sum_{i=1}^k P(A \mid B_i)P(B_i).$$

Proof. Since the $B_i$ form a partition,

$$A=\bigcup_{i=1}^k (A \cap B_i),$$

and the sets on the right are disjoint. Therefore

$$P(A)=\sum_{i=1}^k P(A \cap B_i).$$

Apply the product rule to each term.

### Proposition: Bayes Rule

If $P(B)>0$ and $P(A)>0$, then

$$P(A \mid B)=\frac{P(B \mid A)P(A)}{P(B)}.$$

Proof. Write the joint probability in two ways:

$$P(A,B)=P(A \mid B)P(B)=P(B \mid A)P(A).$$

Divide by $P(B)$.

### Proposition: Odds Form of Bayes Rule

For two hypotheses $H_1$ and $H_0$ and evidence $E$,

$$\frac{P(H_1 \mid E)}{P(H_0 \mid E)} = \frac{P(E \mid H_1)}{P(E \mid H_0)} \cdot \frac{P(H_1)}{P(H_0)}.$$

Interpretation. Posterior odds equal likelihood ratio times prior odds. The ratio form is often the cleanest way to separate evidence strength from prior preference.

## 3. Expectation, Variance, and Dependence

### Proposition: Linearity of Expectation

For integrable random variables $X$ and $Y$ and constants $a$, $b$, and $c$,

$$\mathbb{E}[aX+bY+c]=a\mathbb{E}[X]+b\mathbb{E}[Y]+c.$$

Proof. In the discrete case,

$$\mathbb{E}[aX+bY+c]=\sum_{\omega}(aX(\omega)+bY(\omega)+c)P(\omega).$$

Distribute the sum and use

$$\sum_{\omega} P(\omega)=1.$$

The continuous case is the same calculation with integrals replacing sums. No independence assumption appears anywhere in the argument.

### Proposition: Variance Identity

If $\mathbb{E}[X^2]$ is finite, then

$$\mathrm{Var}(X)=\mathbb{E}[X^2]-\mathbb{E}[X]^2.$$

Proof. Expand the square:

$$\mathrm{Var}(X)=\mathbb{E}[(X-\mathbb{E}[X])^2] =\mathbb{E}[X^2-2X\mathbb{E}[X]+\mathbb{E}[X]^2].$$

Pull constants outside expectation and simplify.

### Proposition: Affine Transform Rules

For constants $a$, $b$, $c$, and $d$,

$$\mathrm{Var}(aX+b)=a^2 \mathrm{Var}(X),$$

and

$$\mathrm{Cov}(aX+b,cY+d)=ac\,\mathrm{Cov}(X,Y).$$

The proof is a direct substitution into the definitions of variance and covariance.

### Proposition: Independence Equivalence

If $P(Y=y)>0$, then the following are equivalent:

$$p(x,y)=p(x)p(y)$$

and

$$p(x \mid y)=p(x)$$

for all states $x$ and $y$.

Proof. If the joint factorizes, then

$$p(x \mid y)=\frac{p(x,y)}{p(y)}=\frac{p(x)p(y)}{p(y)}=p(x).$$

Conversely, if $p(x \mid y)=p(x)$ for all $x$ and $y$ with positive $p(y)$, multiply both sides by $p(y)$.

### Remark: Pairwise Versus Mutual Independence

Pairwise independence requires factorization for every pair. Mutual independence requires factorization for every finite subcollection. Pairwise independence therefore does not imply mutual independence. The exclusive-or example in the main note is the standard counterexample.

## 4. Continuous Models and Conjugacy

### Proposition: Density Rule

If $X$ has density $f_X$, then for any measurable set $A$,

$$P(X \in A)=\int_A f_X(x)\,dx.$$

Consequences:

- Point probabilities vanish: $P(X=x)=0$ for each fixed $x$.
- Density height is not itself probability.
- A density may exceed one on a short enough interval.

### Remark: Why Density Greater Than One Is Allowed

Probability is area or volume, not height. A uniform law on an interval of length $0.2$ has density $5$ and still integrates to one. The normalization requirement applies to the integral of the density over the support, not to the pointwise size of the density.

### Proposition: Bernoulli in Canonical Exponential-Family Form

For $x \in \{0,1\}$ and $\eta=\log(\rho/(1-\rho))$,

$$p(x)=\exp(\eta x-A(\eta))$$

with

$$A(\eta)=\log(1+e^\eta).$$

Proof. Start from

$$\rho^x(1-\rho)^{1-x}.$$

Write $\rho=e^\eta/(1+e^\eta)$ and $1-\rho=1/(1+e^\eta)$, then simplify.

### Proposition: Gradient and Hessian of the Log-Partition Function

For an exponential family

$$p(x;\theta)=h(x)\exp(\theta^T\phi(x)-A(\theta)),$$

one has

$$\nabla A(\theta)=\mathbb{E}_\theta[\phi(X)]$$

and

$$\nabla^2 A(\theta)=\mathrm{Cov}_\theta(\phi(X)).$$

Interpretation. The gradient gives model moments, and the Hessian is positive semidefinite because covariance matrices are positive semidefinite. This is the formal reason exponential-family negative log-likelihoods are convex in natural-parameter space.

### Proposition: Beta-Bernoulli Conjugacy

If

$$\rho \sim \mathrm{Beta}(a,b)$$

and the Bernoulli sample contains $m_1$ ones and $m_0$ zeros, then

$$\rho \mid D \sim \mathrm{Beta}(a+m_1,b+m_0).$$

Proof. Multiply the Beta prior kernel

$$\rho^{a-1}(1-\rho)^{b-1}$$

by the Bernoulli likelihood kernel

$$\rho^{m_1}(1-\rho)^{m_0}.$$

The exponents add.

### Proposition: Dirichlet-Categorical Conjugacy

If

$$\theta \sim \mathrm{Dir}(\alpha_1,\dots,\alpha_K)$$

and a categorical sample produces counts $m_1,\dots,m_K$, then

$$\theta \mid D \sim \mathrm{Dir}(\alpha_1+m_1,\dots,\alpha_K+m_K).$$

Interpretation. Each Dirichlet parameter acts like a pseudo-count. Posterior updating simply adds observed class counts to those prior pseudo-counts.

## 5. Information-Theoretic Identities

### Proposition: Gibbs Inequality

For distributions $p$ and $q$ on a common finite support,

$$D(p \,\|\, q)=\sum_x p(x)\log \frac{p(x)}{q(x)} \ge 0.$$

Equality holds if and only if $p=q$ on the support of $p$.

Interpretation. KL divergence is never negative, but it is not symmetric and therefore is not a metric.

### Proposition: Mutual Information Identity

Mutual information satisfies

$$I(X;Y)=H(X)-H(X \mid Y)=H(Y)-H(Y \mid X).$$

Proof. Start from

$$I(X;Y)=H(X)+H(Y)-H(X,Y).$$

Use

$$H(X \mid Y)=H(X,Y)-H(Y)$$

and rearrange.

## 6. Change of Variables and Structural Limits

### Proposition: Scalar Change of Variables

If $X=f(Z)$ and $f$ is differentiable and invertible on the relevant region with inverse $g=f^{-1}$, then

$$p_X(x)=p_Z(g(x))\lvert g'(x)\rvert.$$

The factor $\lvert g'(x)\rvert$ is the one-dimensional volume correction.

### Proposition: Multivariate Change of Variables

If $X=f(Z)$ with differentiable inverse $g$ between equal-dimensional spaces, then

$$p_X(x)=p_Z(g(x))\lvert \det J_g(x)\rvert.$$

The determinant is the local volume-scaling factor.

### Remark: Structural Limits

The simple Jacobian formula requires an invertible map on the region being modeled. If the map folds space over itself, a single inverse no longer exists and the density must instead sum contributions from all inverse branches. Normalizing flows enforce invertibility precisely so that this bookkeeping remains tractable.

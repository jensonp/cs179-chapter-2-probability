# Probability and Inference: Exercises

Source: ../notes/02_probability_reconstructed/source/02_probability.pdf

This exercise set is organized to match the reconstructed Chapter 2 note. Each section has three layers. Basic checks test direct computation. Conceptual questions test interpretation and diagnostic understanding. Proof-oriented questions test structural command of the identities used throughout the chapter.

## 2.1 Probability, Events, Random Variables

### Basic Checks

- A fair die is rolled once. Let $A=\{1,2,3\}$ and $B=\{3,4,5,6\}$. Compute $P(A)$, $P(B)$, $P(A \cap B)$, and $P(A \cup B)$.
- Let $X$ be the parity variable for a die roll, with $X=0$ for even and $X=1$ for odd. Write the full distribution of $X$ and verify normalization.
- In the dentist table from the main note, compute $p(C=1)$, $p(D=1)$, and $p(T=1,D=1)$ directly from the joint rows.
- Using the same table, compute $p(C=1 \mid T=1)$ by Bayes' rule and then again by restrict-marginalize-normalize table arithmetic.
- Let $X$ take values $\{1,2,3\}$ with probabilities $(0.2,0.5,0.3)$. Compute $E[X]$.

### Conceptual Questions

- Explain why a random variable is a function rather than a container of randomness.
- Explain why the statement $X=x$ should be read as an event.
- Give an example in which $E[X]$ is not one of the possible realized values of $X$, and explain why this is not a contradiction.
- Explain why conditioning is not the same as causal intervention.
- In the screening example from the main note, explain in words why a positive test result can still leave the disease probability relatively small.

### Proof-Oriented Exercises

- Prove inclusion-exclusion for two events using a disjoint decomposition.
- Prove the law of total probability for a finite partition.
- Derive Bayes' rule directly from the definition of conditional probability and the product rule.
- Prove that $p(x,y)=p(x)p(y)$ implies $p(x \mid y)=p(x)$ whenever $p(y)>0$, and prove the converse.
- Show that if $A \subseteq B$, then $P(A) \le P(B)$.

## 2.2 Continuous Random Variables

### Basic Checks

- Let $X$ be uniform on $[0,4]$. Compute $p(x)$ and $P(1 \le X \le 2.5)$.
- Let $X$ have density $p(x)=3x^2$ on $[0,1]$ and zero elsewhere. Verify normalization and compute $P(X \le 1/2)$.
- For $X \sim \mathcal{N}(2,9)$, state the mean and standard deviation and identify the interval within one standard deviation of the mean.
- For a mixed random variable with $P(X=0)=0.6$ and continuous part $0.4$ times Uniform$([0,1])$, write the CDF on the regions $x<0$, $0 \le x <1$, and $x \ge 1$.
- Let $\theta \sim \mathrm{Dir}(1,1,1)$. State the support of the distribution and explain how many free coordinates the simplex has.

### Conceptual Questions

- Explain why a density can be larger than one without violating any probability law.
- Explain why $P(X=x)=0$ for a continuous variable does not mean that the value $x$ is impossible.
- Contrast discrete, continuous, and mixed distributions using the CDF as the common object.
- Explain in words what the covariance matrix does geometrically in a multivariate Gaussian.
- Explain why the two-parameter Bernoulli representation is redundant even though it uses two numbers.

### Proof-Oriented Exercises

- Derive the normalization constant of the uniform density on $[0,T]$.
- Starting from the Bernoulli PMF, derive its canonical exponential-family form and identify $A(\eta)$.
- Show that $\mathrm{Beta}(1,1)$ is uniform on $[0,1]$.
- Show that a symmetric positive definite covariance matrix produces nonnegative quadratic form values $v^T \Sigma v$.
- Prove that the last coordinate of a Dirichlet random vector is determined once the first $d-1$ coordinates are known.

## 2.3 Learning and Parameter Estimation

### Basic Checks

- For Bernoulli data $D=\{1,0,1,1,0\}$, compute the likelihood $p(D \mid \rho)$ and the log-likelihood $L(\rho)$.
- For the same data, compute the Bernoulli MLE.
- For Gaussian data $D=\{-1,0,2,3\}$, compute the sample mean and the Gaussian variance MLE.
- Let $\rho \sim \mathrm{Beta}(2,3)$ and observe Bernoulli data with three ones and one zero. Write the posterior.
- Let $\theta \sim \mathrm{Dir}(2,2,2)$ and observe category counts $(4,1,0)$. Write the posterior and posterior mean.

### Conceptual Questions

- Explain the difference between probability and likelihood.
- Explain why maximum likelihood can overfit when the model class is too flexible.
- Explain why the evidence term in Bayes' rule is needed if the numerator already contains prior and likelihood.
- Compare the MLE, MAP estimate, and posterior mean in words.
- Explain why a highly flexible model can have larger maximum likelihood but smaller marginal likelihood.

### Proof-Oriented Exercises

- Derive the Bernoulli MLE by differentiating the log-likelihood and checking the second derivative.
- Derive the Gaussian mean MLE from the log-likelihood with fixed variance.
- Prove the moment-matching condition for a canonical exponential family:
$$ \frac{1}{m}\sum_i \phi(x^{(i)})=E_\theta[\phi(X)]. $$
- Derive the Beta-Bernoulli posterior by multiplying kernels and identifying the resulting family.
- Derive the Dirichlet-Categorical posterior by multiplying kernels and identifying the updated concentration parameters.

## 2.4 Convexity

### Basic Checks

- Verify the convexity inequality directly for $f(x)=x^2$ at the points $x=1$, $x'=3$, and $\alpha=1/4$.
- Compute the derivative and second derivative of $f(x)=e^x$ and use them to explain why it is convex.
- Let $f(x)=x^2$ and $X$ be a fair $\pm 1$ random variable. Compute $E[f(X)]$ and $f(E[X])$ to verify Jensen's inequality numerically.
- For a one-dimensional quadratic $f(x)=ax^2+bx+c$, identify the condition on $a$ that makes $f$ convex.
- If a Hessian matrix is positive definite everywhere, explain what that implies about local versus global minima.

### Conceptual Questions

- Explain geometrically what the secant-line definition of convexity means.
- Explain why a positive semidefinite Hessian allows flat directions while a positive definite Hessian rules them out.
- Explain why convexity is especially useful in optimization.
- Explain why the Hessian of the exponential-family log-partition function is a covariance matrix.
- Explain how Jensen's inequality is a probabilistic restatement of convexity.

### Proof-Oriented Exercises

- Prove the first-order characterization of convexity for differentiable functions.
- Prove Jensen's inequality for a finite discrete random variable by repeated use of the convexity inequality.
- Show that the sum of two convex functions is convex.
- Show that the negative log-likelihood of a canonical exponential family is convex in natural-parameter space.
- Give an example of a convex function that is not strictly convex, and explain why multiple minimizers can then exist.

## 2.5 Information Theory

### Basic Checks

- Compute the entropy of a Bernoulli variable with parameter $1/2$.
- Compute the entropy of a Bernoulli variable with parameter $0.9$.
- Let $p=(0.8,0.2)$ and $q=(0.5,0.5)$. Compute $D(p \,\|\, q)$.
- For the commute-weather example in the main note, recompute $H(C \mid R=\mathrm{clear})$ and $H(C \mid R=\mathrm{rain})$.
- If $Y=X$, compute $H(X \mid Y)$ and $I(X;Y)$ in terms of $H(X)$.

### Conceptual Questions

- Explain why entropy is larger for a fair coin than for a strongly biased coin.
- Explain why KL divergence is not symmetric and therefore is not a true distance metric.
- Explain why $D(p \,\|\, q)$ becomes infinite if $q$ assigns zero probability to an outcome that has positive probability under $p$.
- Explain in words what mutual information measures.
- Explain why conditioning reduces uncertainty on average, even though a particular conditioning event can sometimes make one branch look more uncertain than another.

### Proof-Oriented Exercises

- Prove that entropy is maximized by the uniform distribution on a finite support.
- Prove that mutual information is nonnegative by writing it as a KL divergence.
- Starting from the chain rule definitions, derive
$$ I(X;Y)=H(X)-H(X \mid Y). $$
- Prove that if $X$ and $Y$ are independent, then $I(X;Y)=0$.
- Give an example where $I(X;Y)=0$ but neither variable is deterministic.

## 2.6 Change-of-Variable Models

### Basic Checks

- Let $X=3Z$ where $Z$ is uniform on $[0,1]$. Derive the density of $X$.
- Let $X=e^Z$ where $Z \sim \mathcal{N}(0,1)$. Write the resulting density of $X$.
- For the linear map $X_1=2Z_1$ and $X_2=5Z_2$, compute the determinant of the inverse Jacobian.
- In a one-layer affine flow $X=aZ+b$, compute the log-density correction term.
- For a triangular Jacobian matrix, explain how the determinant is computed.

### Conceptual Questions

- Explain why invertibility is essential for the simple change-of-variables formula.
- Explain what the Jacobian determinant measures geometrically.
- Explain how copulas separate marginal behavior from dependence structure.
- Explain why CDF transforms are useful before fitting a Gaussian copula.
- Explain why affine coupling layers are popular in normalizing flows.

### Proof-Oriented Exercises

- Derive the scalar change-of-variables formula starting from probability conservation on a small interval.
- Derive the multivariate change-of-variables formula and explain the role of local volume scaling.
- Show that if a scalar transform is not one-to-one, the transformed density must sum over inverse branches.
- Derive the determinant of a conditional affine flow layer and show why the triangular structure makes it cheap.
- Explain why the log-determinant of a composition of invertible maps becomes a sum.

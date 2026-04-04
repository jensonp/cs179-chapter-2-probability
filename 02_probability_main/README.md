
For example, compare $\mathrm{Beta}(2,2)$ and $\mathrm{Beta}(20,20)$. They are both centered at $0.5$, because in both cases $\frac{a}{a+b}=0.5$.

But $\mathrm{Beta}(20,20)$ is much more concentrated near $0.5$. So the first distribution is broad around the center, while the second is sharply concentrated there. In later Bayesian sections this same difference will be interpreted as weak versus strong prior information, but the mathematical point here is simply how concentration changes the shape.

The Dirichlet distribution is the multi-state version of this same idea.

Suppose a categorical variable has $d$ possible outcomes. Then its parameter is not one number but a probability vector

$$
\theta = (\theta_1,\ldots,\theta_d)
$$

where $\theta_j \ge 0$ for all $j$ and $\sum_{j=1}^d \theta_j=1$.

So for a three-outcome variable, a legal parameter might be $\theta=(0.2,0.5,0.3)$.

The set of all such probability vectors is called the simplex. In the three-state case, the simplex is a filled triangle. Each point inside that triangle represents one legal categorical probability table.

The reason the simplex has one fewer free dimension than the number of coordinates is normalization. Once two coordinates are chosen, the last one is forced. In the example above, $\theta_3=1-0.2-0.5=0.3$.

So even though the vector has three entries, only two of them are independent.

The Dirichlet density is

$$
p(\theta)=\mathrm{Dir}(\theta;\alpha)=\frac{\Gamma(\alpha_0)}{\prod_{j=1}^d \Gamma(\alpha_j)}\prod_{j=1}^d \theta_j^{\alpha_j-1}
$$

where

$$
\alpha_0=\sum_{j=1}^d \alpha_j
$$

This looks more complicated than Beta only because there are more coordinates. Conceptually it plays the same role:

- it is a distribution over possible categorical probability tables;
- the relative sizes of the $\alpha_j$ values say which categories are favored;
- the total concentration $\alpha_0$ says how tightly the mass is pulled toward or away from the center.

The coordinate-wise mean is $\mathbb{E}[\theta_j]=\frac{\alpha_j}{\alpha_0}$.

So if $\alpha=(8,2,2)$, then $\mathbb{E}[\theta]=\left(\frac{8}{12},\frac{2}{12},\frac{2}{12}\right)=\left(\frac{2}{3},\frac{1}{6},\frac{1}{6}\right)$.

That Dirichlet distribution is centered much closer to the first category than to the other two.

If instead $\alpha=(2,2,2)$, then $\mathbb{E}[\theta]=\left(\frac{1}{3},\frac{1}{3},\frac{1}{3}\right)$.

So the distribution is symmetric across categories.

Now compare concentration while keeping the same proportions. If we increase to $\alpha=(20,20,20)$, the mean stays $\left(\frac{1}{3},\frac{1}{3},\frac{1}{3}\right)$, but the distribution becomes much more concentrated near the center of the simplex. If we decrease to $\alpha=(0.2,0.2,0.2)$, the mass is pushed toward corners and edges. A **sparse probability vector** means one in which most of the total mass is concentrated in only one or a few coordinates rather than being spread evenly across all categories. So in plain language, this distribution favors tables in which one category gets most of the mass.

For $d=2$, the Dirichlet distribution reduces exactly to the Beta distribution. So Beta is not a separate disconnected topic. It is the two-category version of the same family.

<table align="center" border="0" cellpadding="0" cellspacing="12">
  <tbody>
    <tr>
      <td align="center" valign="top">
        <img src="../notes/02_probability_reconstructed/assets/figure_2_2_beta_grid.png" alt="Beta distribution family" width="520">
      </td>
      <td align="center" valign="top">
        <img src="../notes/02_probability_reconstructed/assets/figure_2_3_dirichlet_simplex.png" alt="Dirichlet distribution family" width="380">
      </td>
    </tr>
  </tbody>
</table>

The Beta grid makes the parameter effects explicit. Curves with parameters above one usually have a single interior peak. Curves with parameters below one can pile up near the boundaries. The Dirichlet simplex panels show the same phenomenon in the multi-category setting: mass near the center means balanced proportions, while mass near an edge or corner means one or more categories dominate.

A final pair of coin examples fixes the interpretation. Suppose $\rho$ is the head probability of a coin. A Beta distribution

$$
\rho \sim \mathrm{Beta}(20,20)
$$

places most of its mass near $0.5$, so parameter values close to a fair coin receive much more weight than extreme values. By contrast,

$$
\rho \sim \mathrm{Beta}(0.3,0.3)
$$

places much more mass near $0$ and $1$, so strongly biased parameter values are favored over nearly fair ones. In the Dirichlet case, the same logic applies to a probability vector rather than a single number: large, balanced concentration parameters favor balanced interior probability tables, while small concentration parameters favor sparse near-corner tables. In later Bayesian sections these same distributions will often be used as priors, but the shape story comes first.

### The Exponential Family

The exponential family is a modeling template, not one specific distribution. Its purpose is to expose a shared algebraic structure that appears in Bernoulli, categorical, Gaussian, Poisson, Gamma, Beta, Dirichlet, and many other common models.

This is one of the chapter's more abstract sections. The right reading strategy is not "memorize one large formula." The right strategy is to keep asking three questions:

- what part of the model depends only on the observation,
- what part depends on the parameter,
- and what summary of the data the parameter actually interacts with.

The phrase "family" matters here. It means a collection of distributions indexed by parameters. The phrase "exponential family" means this collection can be written in a common exponential-shaped algebraic form. The value of that form is not aesthetic. It lets many different models share the same optimization and inference machinery.

The general form is

$$
p_{\theta}(x)=h(x)\exp\left(\theta^{\top}\phi(x)-A(\theta)\right).
$$


Before unpacking symbols, say what stays fixed and what changes.

- The observation $x$ is the realized data value.
- The model family fixes the functions $h(x)$ and $\phi(x)$ ahead of time.
- The parameter $\theta$ is what moves from one member of the family to another.

So the family is "all distributions obtained by varying $\theta$ while keeping the structural form fixed."

Every symbol in the expression has a specific role.

- $x$ is the observed value.
- $\phi(x)$ is a fixed feature vector computed from $x$. Its components are called **sufficient statistics**, meaning summary quantities that capture all the data information the parameter needs for likelihood-based inference in this family.
- $\theta$ is the **natural parameter**, meaning the coordinate system in which the log-density becomes linear in the sufficient statistics.
- $h(x)$ is the base measure, the part of the density or mass function that depends on $x$ but not on $\theta$.
- $A(\theta)$ is the log-partition function, chosen so that the distribution normalizes correctly.

The log-partition function is

$$
A(\theta)=\log \int h(x)\exp\left(\theta^{\top}\phi(x)\right)\,dx,
$$


with the integral replaced by a sum in discrete settings.

This definition is abstract, so the interpretation should be stated plainly. The log-density is linear in the fixed feature vector $\phi(x)$, while the function $A(\theta)$ is the correction term that makes the whole expression normalize properly. That is why exponential-family models are so tractable: all the nontrivial dependence on the parameter is concentrated into a relatively clean algebraic form.

Bernoulli is the simplest example. From the previous subsection,

$$
p(X=x)=\exp\left(\eta x-\log(1+e^{\eta})\right).
$$


Comparing with the template gives

$$
h(x)=1, \qquad \phi(x)=x, \qquad \theta=\eta, \qquad A(\theta)=\log(1+e^{\theta}).
$$


A second example is a one-dimensional Gaussian with known variance $\sigma^2$ and unknown mean $\mu$. Its density can also be rearranged into exponential-family form. The beginner-level point is not to memorize every algebraic coordinate. The point is to notice the same structural split again: one part of the expression depends only on the observation, one part is linear in a summary of the observation, and one part normalizes the distribution.

The term sufficient statistic becomes concrete when we look at independent and identically distributed data. Here independent means the observations do not probabilistically influence one another once the parameter is fixed, and identically distributed means each observation is governed by the same one-observation model. Suppose

$$
D=\{x^{(1)},\ldots,x^{(m)}\}
$$


are independent and identically distributed observations from an exponential-family model. Then

$$
p_{\theta}(D)=\prod_{i=1}^m h(x^{(i)})\exp\left(\theta^{\top}\phi(x^{(i)})-A(\theta)\right).
$$


Taking logarithms yields

$$
\log p_{\theta}(D)=\sum_{i=1}^m \log h(x^{(i)})+\theta^{\top}\left(\sum_{i=1}^m \phi(x^{(i)})\right)-mA(\theta).
$$


This expression shows exactly how the data enter the likelihood. The only data-dependent quantity coupled to $\theta$ is

$$
S(D)=\sum_{i=1}^m \phi(x^{(i)}).
$$


That is the operational meaning of sufficiency in this setting: once $S(D)$ is known, the likelihood as a function of $\theta$ no longer needs the full raw data sequence. The raw sample may be long, but from the parameter's point of view the relevant information has been compressed into that summary.

For Bernoulli, $\phi(x)=x$, so

$$
S(D)=\sum_{i=1}^m x^{(i)}
$$


is just the number of ones. The sequences

$$
D_1=\{1,0,1,0\} \qquad \text{and} \qquad D_2=\{0,1,0,1\}
$$


have the same sufficient statistic,

$$
S(D_1)=S(D_2)=2,
$$


so they induce the same likelihood function for the Bernoulli parameter. The order of the observations is irrelevant because the family compresses the data down to the total count of successes.

That compression is one reason exponential families appear so often in estimation theory. They let large data sets be summarized by a small set of aggregate quantities. But there is also a structural limit: not every distribution can be written with a fixed finite-dimensional feature vector $\phi(x)$. So exponential families are powerful, but they are still a special class rather than a universal description of all probability laws.

### Retain from 2.2

- Every real-valued random variable has a CDF, but not every one has a density.
- A density value is not a point probability; probabilities come from integrals over regions.
- In Gaussian models, the covariance structure controls geometry, not just scale.
- Beta and Dirichlet distributions live on constrained supports, so their formulas only make sense together with those support conditions.

### Do Not Confuse in 2.2

- Do not confuse PMFs, PDFs, and CDFs; they are related but not interchangeable objects.
- Do not conclude that $p(x)>1$ is invalid for a density; only the integral must equal one.
- Do not use a continuous density formula on a mixed distribution that has point masses.
- Do not treat exponential-family form as universal; it is a structural class, not every distribution.

## 2.3 Learning and Parameter Estimation

Sections `2.1` and `2.2` described what probability models look like once their parameters are known. The next question is the learning question: if the probabilities or densities are not given to us, how do we infer them from data?

That shift of emphasis is important. Earlier sections mostly asked forward questions such as "given the model, what is the probability of this event?" In this section we reverse direction and ask inverse questions such as "given these observations, which parameter values are plausible?" or "which model class is supported strongly enough by the data to justify its extra complexity?"

So the objects stay the same, but the role they play changes. The data set becomes the input, and the model parameters become the unknowns we want to estimate or infer.

### Frequentist Versus Bayesian Perspectives

Before comparing the two viewpoints, it helps to name the objects explicitly. A parameter is a numerical quantity inside the model, such as a Bernoulli head probability $\rho$ or a Gaussian mean $\mu$. The data are the observed sample values, such as a list of coin flips or a list of temperatures.

From the frequentist perspective, probability is interpreted through long-run frequency. The parameter is fixed but unknown, the data are random because a fresh sample could have come out differently, and learning means constructing an estimator that tries to recover the true parameter from the observed sample.

From the Bayesian perspective, probability is used to represent uncertainty itself. The parameter is therefore treated as uncertain before the data are seen, so we place a prior distribution on it and update that prior after observing data.

Both views often use the same data-fit quantity. The next subsection will define that quantity carefully and call it the **likelihood**. For now, the important point is only that both schools ask how well different parameter values account for the observed data, but they use that information in different ways. A frequentist estimator asks: if nature chose one fixed parameter value, what rule should I use to estimate it from repeated samples? A Bayesian posterior asks: after seeing this actual realized data set, which parameter values remain plausible, and how plausible are they relative to one another?

One frequentist strategy is **maximum likelihood estimation**: choose the parameter value that makes the observed data most compatible with the model. A Bayesian update keeps one more ingredient as well: how plausible the parameter looked before the data arrived.

The same coin-toss example makes the contrast concrete. Suppose we observe five flips with outcomes

$$
D=\{1,1,0,1,0\}.
$$


A frequentist summary is the single estimate

$$
\rho_{\mathrm{MLE}}=3/5=0.6.
$$


This answers the question "which one number best summarizes the data under the chosen estimation rule?"

A Bayesian analysis asks a different question, so it keeps a different object. Start from the prior

$$
\rho \sim \mathrm{Beta}(2,2).
$$


This means that before observing the five flips, the density over possible values of $\rho$ is proportional to

$$
\rho^{2-1}(1-\rho)^{2-1}=\rho(1-\rho).
$$


Now read the data explicitly. The sample

$$
D=\{1,1,0,1,0\}
$$


contains

$$
m_1=3 \quad \text{successes}, \qquad m_0=2 \quad \text{failures}.
$$


So the Bernoulli likelihood is proportional to

$$
p(D \mid \rho)\propto \rho^3(1-\rho)^2.
$$


Multiply prior and likelihood:

$$
p(\rho \mid D)\propto p(D \mid \rho)p(\rho)\propto \rho^3(1-\rho)^2 \cdot \rho(1-\rho)=\rho^4(1-\rho)^3.
$$


That is exactly the **unnormalized part** of a Beta density with updated parameters. Here "unnormalized part" means the factor that determines the shape of the density before we insert the constant that makes the total area equal to $1$:

$$
2+3=5 \qquad \text{and} \qquad 2+2=4.
$$


So the posterior is

$$
\rho \mid D \sim \mathrm{Beta}(5,4),
$$


which answers a different question: "after seeing the five flips, how is probability mass distributed over the possible values of $\rho$?"

This is worth interpreting explicitly. The notation

$$
\rho \mid D \sim \mathrm{Beta}(5,4)
$$


does **not** mean the coin suddenly became a Beta random variable in the same sense that a flip outcome is Bernoulli. It means our uncertainty about the unknown Bernoulli parameter is now described by a Beta density with updated shape parameters $5$ and $4$.

The posterior still centers near the empirical proportion, but it does not collapse everything to a single number. It quantifies uncertainty around that value. That distinction becomes important whenever the sample is small, the parameter lies near a boundary, or prior information matters.

### Likelihood

Likelihood answers a specific learning question:

If the data have already been observed, which parameter values make those observed data look more compatible with the model, and which make them look less compatible?

That is a different question from the forward probability question studied earlier. Earlier the model was known and we asked about possible observations. Now the observations are known and we are using them to compare possible parameter values.

For i.i.d. data

$$
D=\{x^{(1)},\dots,x^{(m)}\},
$$


the likelihood is

$$
p(D \mid \theta)=\prod_{i=1}^m p(x^{(i)} \mid \theta).
$$


The abbreviation i.i.d. stands for **independent and identically distributed**. Each word matters.

- **Independent** means that once the parameter $\theta$ is fixed, learning one sample value does not change the model probability assigned to the others.
- **Identically distributed** means each sample is generated from the same probability law $p_{\theta}(x)$, not from a different distribution at each time step.

So an i.i.d. sample is a collection of observations produced by repeatedly using the same model in the same way, with no extra dependence between draws after $\theta$ has been fixed.

A tiny coin-flip example makes this concrete. If we flip the same Bernoulli coin three times with head probability $\rho$, then

$$
D=\{1,0,1\}
$$


is i.i.d. because

- each flip uses the same Bernoulli law;
- and, once $\rho$ is fixed, the result of one flip does not alter the probability rule for the others.

By contrast, if the first observation came from one coin, the second from a different coin, and the third from a third coin, then the sample would not be identically distributed. If each observation depended on the previous one through a Markov rule, then the sample would not be independent.

The product form comes directly from the independence assumption. For two observations, independence gives

$$
p(x^{(1)},x^{(2)} \mid \theta)=p(x^{(1)} \mid \theta)p(x^{(2)} \mid \theta).
$$


Repeating that same rule for $m$ observations gives the full product

$$
p(D \mid \theta)=\prod_{i=1}^m p(x^{(i)} \mid \theta).
$$


The log-likelihood is

$$
\ell(\theta)=\log p(D \mid \theta)=\sum_{i=1}^m \log p(x^{(i)} \mid \theta).
$$


Taking logs does not change which parameter maximizes the objective, because the logarithm is strictly increasing. It only turns products into sums, which are easier to differentiate, plot, and reason about.

The most important conceptual rule is: after the sample has been observed, the data are treated as fixed and the parameter is allowed to vary. That is what makes the expression a likelihood rather than an ordinary probability model over data.

So likelihood should be read as a **score for parameter values given fixed data**. Large likelihood means "this parameter makes the observed sample look relatively compatible with the model." Small likelihood means "this parameter makes the observed sample look relatively incompatible with the model."

That wording matters because likelihood is comparative, not absolute. A likelihood value by itself does not certify truth. Its role is to compare one parameter value against other parameter values under the same model and the same observed data.

For the small Bernoulli sample

$$
D=\{1,0,1\},
$$


the likelihood is

$$
p(D \mid \rho)=\rho(1-\rho)\rho=\rho^2(1-\rho).
$$


This expression is worth unpacking mechanically. The first factor $\rho$ comes from the first success, the factor $(1-\rho)$ comes from the observed failure, and the final factor $\rho$ comes from the last success. So the whole product is literally "multiply the model probability of each observed outcome under the candidate parameter."

Now compare a few candidate values:

$$
p(D \mid 0.2)=0.2^2(0.8)=0.032,
$$


$$
p(D \mid 0.5)=0.5^2(0.5)=0.125,
$$


$$
p(D \mid 0.8)=0.8^2(0.2)=0.128.
$$


Now interpret these three numbers structurally rather than treating them as mysterious scores. The observed data contain two successes in three trials. A candidate such as $\rho=0.8$ says that success is common, so it assigns a reasonably large probability to a sequence with two successes. A candidate such as $\rho=0.2$ says that success is rare, so the same observed sequence receives much less probability under that parameter. The likelihood comparison is therefore answering a narrow question: **which parameter values make the observed sample less surprising?**

This comparison is relative, not absolute. The fact that $0.128 > 0.125 > 0.032$ does **not** prove that the true parameter is exactly $0.8$. It says only that, among these three candidates and for this fixed data set, the sample is more compatible with $\rho=0.8$ than with $\rho=0.5$, and much more compatible with $\rho=0.8$ than with $\rho=0.2$.

This also shows a structural limitation of likelihood by itself. Likelihood can rank parameter values for a fixed model and a fixed observed data set, but it does not by itself tell you how much uncertainty remains after seeing the data. To quantify uncertainty, you need an additional layer such as confidence sets, asymptotic theory, or a Bayesian posterior distribution over $\rho$.

A common wrong notion is to treat $p(D \mid \rho)$ as if it were a probability distribution over $\rho$. It is not. One concrete way to see this is that it does not normalize over parameter space. For this data,

$$
p(D \mid \rho)=\rho^2(1-\rho).
$$


If we integrate this function over $\rho \in [0,1]$, we get

$$
\int_0^1 \rho^2(1-\rho)\,d\rho=\int_0^1 (\rho^2-\rho^3)\,d\rho=\left[\frac{\rho^3}{3}-\frac{\rho^4}{4}\right]_0^1=\frac{1}{3}-\frac{1}{4}=\frac{1}{12},
$$


not $1$. That calculation tells us something precise: the function $\rho \mapsto p(D \mid \rho)$ is **not** a probability distribution over possible parameter values. A genuine probability density over $\rho$ would have to integrate to $1$ over the parameter space. The likelihood function does not do that, because it was never designed to answer the question

$$
\text{``What is the probability that the parameter lies near this value?''}
$$


Instead, likelihood answers a different question:

$$
\text{``If this were the parameter value, how compatible would the observed data be with it?''}
$$


So likelihood should be read as a **relative compatibility score** over parameter values for the fixed observed sample. Larger likelihood means the candidate parameter makes the actual sample less surprising under the model. Smaller likelihood means the candidate parameter makes the actual sample more surprising. This is why likelihood is used to rank or compare parameter values rather than to assign posterior probabilities to them.

Another boundary on the concept should be stated explicitly: likelihood values should only be compared when the observed data are being held fixed. Comparing $p(D_1 \mid \theta)$ and $p(D_2 \mid \theta)$ across two different data sets is usually not the question likelihood is designed to answer. The likelihood framework is primarily for comparing parameter values for the same observed sample, or for comparing models on the same observed sample with the right normalizations and complexity penalties.

To get a probability distribution over $\rho$, you must multiply by a prior and renormalize. For example, with a uniform prior

$$
\rho \sim \mathrm{Beta}(1,1),
$$


the posterior is $\mathrm{Beta}(3,2)$, whose normalized density is proportional to the same unnormalized shape function $\rho^2(1-\rho)$.

That last sentence is worth unpacking once, because this is exactly the step that converts a likelihood function into a probability distribution over $\rho$. A $\mathrm{Beta}(1,1)$ prior has density

$$
p(\rho)=1 \qquad \text{for } 0 \le \rho \le 1.
$$


So multiplying the likelihood function's unnormalized shape

$$
\rho^2(1-\rho)
$$


by the prior changes nothing except the eventual normalization, since multiplying by $1$ leaves that unnormalized shape unchanged. The exponents are still

$$
2 \quad \text{on } \rho \qquad \text{and} \qquad 1 \quad \text{on } (1-\rho),
$$


which is exactly the $\mathrm{Beta}(3,2)$ pattern. The posterior therefore has the same basic shape as the likelihood function, but now it is normalized so that the total area over $\rho \in [0,1]$ equals $1$. That normalization step is what changes the object from a compatibility score into a true probability density over parameter values.

The structural role of likelihood is now visible. It is the part of inference that comes directly from the observed data. Before we add priors, penalties, confidence sets, or posterior summaries, the likelihood tells us how the sample reweights the candidate parameter values. Everything else in statistical inference is built on top of that reweighting step.

### Probability Versus Likelihood

The same algebraic expression can play two different roles depending on what is held fixed. When $\theta$ is fixed and $x$ varies, the quantity $p(x \mid \theta)$ is a probability model over possible observations. When the observation $x$ has already been fixed and $\theta$ varies, the same expression is treated as a likelihood function of the parameter.

This distinction is one of the most important "do not blur these together" rules in the chapter. The formula may look identical on paper, but the question being asked is different.

For Bernoulli data, if we observe a single success $x=1$, then

$$
p(x=1 \mid \rho)=\rho.
$$


Viewed as a function of the data, this is a perfectly ordinary probability rule: for fixed $\rho$, the probabilities of the two possible observations are

$$
p(x=0 \mid \rho)=1-\rho,\qquad p(x=1 \mid \rho)=\rho,
$$


and those two numbers add to one.

But viewed as a function of $\rho$ after observing $x=1$, the same expression becomes the likelihood $L(\rho)=\rho$. That likelihood does not integrate to one over $\rho \in [0,1]$, nor is it supposed to. Its job is only to rank parameter values by how well they explain the observation.

So the right mental checklist is:

- probability mode: parameter fixed, data allowed to vary;
- likelihood mode: data fixed, parameter allowed to vary.

If that checklist is not kept explicit, later Bayesian formulas become much harder to interpret correctly.

### Example 2-12: Bernoulli Likelihood

Suppose we observe $m$ Bernoulli samples, with $m_1$ ones and $m_0$ zeros, so that $m=m_1+m_0$. Start from the Bernoulli PMF for one observation:

$$
p(x \mid \rho)=\rho^x(1-\rho)^{1-x}.
$$


For the full data set, multiply one factor for each observation:

$$
p(D \mid \rho)=\prod_{i=1}^m \rho^{x^{(i)}}(1-\rho)^{1-x^{(i)}}.
$$


Collecting exponents gives

$$
p(D \mid \rho)=\rho^{m_1}(1-\rho)^{m_0}.
$$


So the log-likelihood is

$$
\ell(\rho) = m_1 \log \rho + m_0 \log(1-\rho).
$$


This expression has a transparent interpretation. The term

$$
m_1 \log \rho
$$


rewards large $\rho$ when many ones were observed. The term

$$
m_0 \log(1-\rho)
$$


rewards small $\rho$ when many zeros were observed. The maximizing value of $\rho$ balances those two pressures and ends up at the empirical frequency of ones.

That is an important structural lesson. The log-likelihood separates the sample into only two summaries:

- how many successes were seen;
- how many failures were seen.

The exact order of the flips no longer matters. For Bernoulli likelihood, the data influence the fit only through the counts $m_1$ and $m_0$.

If the observed sample is all zeros or all ones, the maximizer lies on the boundary $\rho=0$ or $\rho=1$. Otherwise the unique optimum lies in the interior of the interval.

<p align="center">
  <img src="../notes/02_probability_reconstructed/assets/figure_2_12_bernoulli_likelihood.png" alt="Bernoulli likelihood curves" width="860">
</p>

Each panel holds the observed data fixed and varies only the parameter $\rho$. The curve peaks where the model's predicted head probability best matches the observed proportion of heads. When the data rule out part of parameter space completely, the log-likelihood drops toward negative infinity at the incompatible boundary.

For the data set $D=\{0,1\}$, the likelihood is

$$
p(D \mid \rho)=\rho(1-\rho),
$$


which is zero at $\rho=0$ and $\rho=1$ because either extreme makes one of the two observations impossible. The peak therefore occurs in the interior, specifically at $\rho=1/2$.

This example isolates the logic of likelihood fitting in the smallest possible nontrivial case. The sample contains one success and one failure, so any parameter far from $0.5$ makes one of those two observed outcomes much less plausible than the other. The balanced value $\rho=0.5$ is the point at which the model assigns equal probability to the two observed outcome types, which is exactly why the likelihood peaks there.

An implication worth remembering is that likelihood naturally pushes toward boundary values when the sample itself sits at a boundary. If every observed flip is heads, the Bernoulli likelihood is largest at $\rho=1$. That is mathematically correct for pure maximum likelihood, but it also hints at why regularization or priors may be useful: with very small samples, boundary-hugging estimates can be too brittle.

### Example 2-13: Gaussian Likelihood

For a one-dimensional Gaussian with variance fixed at one, the likelihood as a function of $\mu$ becomes more sharply peaked as the number of samples grows. That sharpening is the visual signature that more data constrain the mean more strongly: many values of $\mu$ may explain three observations reasonably well, but far fewer values remain compatible once twenty observations cluster around the same region.

The algebra behind that picture is worth stating. If

$$
x^{(i)} \sim \mathcal{N}(\mu,1),
$$


then the density of one sample is

$$
p(x^{(i)} \mid \mu)=\frac{1}{\sqrt{2\pi}}\exp\left(-\frac{(x^{(i)}-\mu)^2}{2}\right).
$$


For $m$ observations, the likelihood is the product of these terms, so the log-likelihood is

$$
\ell(\mu)= -\frac{m}{2}\log(2\pi)-\frac{1}{2}\sum_{i=1}^m (x^{(i)}-\mu)^2.
$$


Everything except the squared-error sum is constant in $\mu$. So maximizing the Gaussian likelihood in $\mu$ is exactly the same optimization problem as minimizing

$$
\sum_{i=1}^m (x^{(i)}-\mu)^2.
$$


<p align="center">
  <img src="../notes/02_probability_reconstructed/assets/figure_2_13_gaussian_likelihood.png" alt="Gaussian likelihood curves" width="860">
</p>

The dots along the top of each panel are the observed samples. The curve below them is the log-likelihood as a function of the Gaussian mean. As $m$ increases, the curve narrows and the maximizing value moves toward the visual center of the observed data cloud.

If the observed values are $-0.5$, $0.4$, and $1.3$, then the Gaussian likelihood in $\mu$ is largest near the arithmetic average

$$
\bar x = \frac{-0.5+0.4+1.3}{3}=0.4.
$$


The entire curve can be read as a squared-error landscape written in likelihood language. When $\mu$ moves away from $0.4$, every term of the form $(x^{(i)}-\mu)^2$ becomes larger in aggregate, so the sum of squared deviations increases. Because the Gaussian log-likelihood is a constant minus one-half that sum, the log-likelihood must decrease when the squared-error total increases. This is the geometric reason the sample mean appears as the Gaussian MLE.

It helps to check one comparison numerically. At $\mu=0.4$ the squared-error total is

$$
(-0.5-0.4)^2+(0.4-0.4)^2+(1.3-0.4)^2=0.81+0+0.81=1.62.
$$


At $\mu=1.0$ the squared-error total is

$$
(-0.5-1.0)^2+(0.4-1.0)^2+(1.3-1.0)^2=2.25+0.36+0.09=2.70.
$$


Because the second total is larger, the log-likelihood at $\mu=1.0$ is smaller. In other words, the Gaussian-likelihood curve is a re-expression of the same optimization problem: parameter values that increase total squared deviation are penalized, and the unique minimizer of squared deviation becomes the unique maximizer of the Gaussian likelihood.

This example exposes an important connection that reappears throughout statistics: for Gaussian models, maximizing likelihood is the same as minimizing squared error. That is why least squares appears so often. It is not a disconnected optimization trick. It is the Gaussian likelihood principle written in another form.

### Maximum Likelihood Estimation

Maximum likelihood estimation, or MLE, means choosing the parameter value that maximizes the likelihood of the observed data:

$$
\theta_{\mathrm{MLE}}=\arg\max_\theta p(D \mid \theta).
$$


These notes write fitted estimates with an explicit subscript such as $\theta_{\mathrm{MLE}}$ rather than a hat such as $\hat{\theta}$. The meaning is the same: this symbol denotes the parameter value selected by the estimation rule.

Because the logarithm is strictly increasing, this is equivalent to

$$
\theta_{\mathrm{MLE}}=\arg\max_\theta \ell(\theta),
$$


where $\ell(\theta)$ denotes the log-likelihood. In practice one almost always works with the log-likelihood because products become sums and derivatives become manageable.

For a Bernoulli distribution,

$$
\ell(\rho) = m_1 \log \rho + m_0 \log(1-\rho).
$$


Differentiating gives

$$
\frac{\partial \ell}{\partial \rho} = \frac{m_1}{\rho} - \frac{m_0}{1-\rho}.
$$


Setting this to zero yields

$$
\rho_{\mathrm{MLE}} = \frac{m_1}{m}.
$$


The algebra is worth writing out explicitly:

$$
\frac{m_1}{\rho} - \frac{m_0}{1-\rho} = 0 \quad \Longrightarrow \quad m_1(1-\rho) = m_0\rho \quad \Longrightarrow \quad m_1 = (m_0+m_1)\rho.
$$


Since $m_0+m_1 = m$, we obtain $\rho_{\mathrm{MLE}} = m_1/m$. The second derivative is

$$
\frac{\partial^2 \ell}{\partial \rho^2} = -\frac{m_1}{\rho^2} - \frac{m_0}{(1-\rho)^2} < 0,
$$


so the stationary point is a strict global maximum whenever it lies in the interior.

This result has a clear interpretation. The model parameter $\rho$ is the probability of seeing a $1$, so the likelihood is maximized when the model's success probability matches the observed success frequency.

For a Gaussian with mean $\mu$ and variance $\nu = \sigma^2$,

$$
\mu_{\mathrm{MLE}} = \frac{1}{m}\sum_i x^{(i)}
$$


$$
\nu_{\mathrm{MLE}} = \frac{1}{m}\sum_i \left(x^{(i)} - \mu_{\mathrm{MLE}}\right)^2.
$$


For the mean parameter, the derivation comes from expanding the log-likelihood into a constant minus a squared-error term:

$$
\ell(\mu) = \text{const} - \frac{1}{2\nu}\sum_i (x^{(i)}-\mu)^2.
$$


Differentiating with respect to $\mu$ gives

$$
\frac{\partial \ell}{\partial \mu} = \frac{1}{\nu}\sum_i (x^{(i)}-\mu),
$$


so setting the derivative to zero forces $\mu$ to equal the arithmetic average of the observations. The variance estimate is then the average squared deviation around that fitted mean. For a discrete distribution with probabilities $\rho_x$, the MLE is the empirical frequency of each state.

The variance formula often causes confusion because many statistics courses also teach

$$
\frac{1}{m-1}\sum_i \left(x^{(i)}-\mu_{\mathrm{MLE}}\right)^2.
$$


That is the unbiased sample-variance estimator. It is not the Gaussian maximum-likelihood estimator. The MLE uses $1/m$ because it is chosen to maximize the likelihood, not to make the estimator unbiased across repeated samples. These are different optimization goals, so they produce different formulas.

So the three flagship MLE examples all follow the same pattern:

- Bernoulli: match the model mean to the sample proportion;
- Gaussian mean: match the model center to the sample average;
- discrete categorical table: copy empirical frequencies into the parameter table.

The general lesson is that MLE tries to make the model imitate the observed sample as closely as the model family allows.

An explicit discrete example makes the frequency rule concrete. Suppose the data over states $\{a,b,c\}$ are

$$
D=\{a,c,a,b,a,c\}.
$$


Then the counts are $m_a=3$, $m_b=1$, and $m_c=2$, so the MLE is

$$
\rho_{a,\mathrm{MLE}}=3/6,\qquad \rho_{b,\mathrm{MLE}}=1/6,\qquad \rho_{c,\mathrm{MLE}}=2/6
$$


The estimate is obtained by normalizing the observed counts so they sum to one. Nothing more complicated is happening in this discrete MLE: each row of the fitted probability table is the observed relative frequency of that state in the sample.

### Example 2-14: Bernoulli MLE

This example should be read as the most basic MLE computation in the chapter.

Suppose we observe Bernoulli data with

$$
m_1 \quad \text{ones}, \qquad m_0 \quad \text{zeros}, \qquad m=m_1+m_0.
$$


From the earlier likelihood derivation,

$$
p(D \mid \rho)=\rho^{m_1}(1-\rho)^{m_0}.
$$


The maximizer is

$$
\rho_{\mathrm{MLE}} = \frac{m_1}{m}
$$


because the model fits best when its predicted success probability matches the observed success frequency.

Now do one concrete sample slowly. Let

$$
D=\{1,1,0,1,0\}.
$$


Then

$$
m_1=3,\qquad m_0=2,\qquad m=5.
$$


So the likelihood is

$$
p(D \mid \rho)=\rho^3(1-\rho)^2.
$$


The MLE is therefore

$$
\rho_{\mathrm{MLE}}=\frac{3}{5}=0.6
$$


The interpretation is immediate: the fitted Bernoulli model predicts success with probability $0.6$ on future draws, because $60\%$ of the observed sample consisted of successes.

It is worth checking the logic against two nearby parameter values. At $\rho=0.6$, the model agrees with the sample proportion exactly. At $\rho=0.2$, the model says successes are rare, which clashes with the data because the sample contains three successes out of five. At $\rho=0.9$, the model says failures are rare, which also clashes with the data because the sample contains two failures. The MLE sits between those extremes at the value that best balances both kinds of observations.

### Example 2-15: Gaussian MLE

For a one-dimensional Gaussian with both mean and variance unknown, the MLEs are the sample mean and the average squared deviation around that mean:

$$
\mu_{\mathrm{MLE}} = \frac{1}{m}\sum_i x^{(i)}
$$


$$
\nu_{\mathrm{MLE}} = \frac{1}{m}\sum_i \left(x^{(i)}-\mu_{\mathrm{MLE}}\right)^2
$$


Now compute them explicitly for the sample

$$
D=\{2,4,7\}.
$$


There are

$$
m=3
$$


observations, so the fitted mean is

$$
\mu_{\mathrm{MLE}}=\frac{2+4+7}{3}=\frac{13}{3}
$$


This number is about $4.33$, which sits near the visual center of the three observations.

Next compute the squared deviations from that fitted center:

$$
2-\frac{13}{3}=-\frac{7}{3},\qquad 4-\frac{13}{3}=-\frac{1}{3},\qquad 7-\frac{13}{3}=\frac{8}{3}.
$$


Square them:

$$
\left(-\frac{7}{3}\right)^2=\frac{49}{9},\qquad \left(-\frac{1}{3}\right)^2=\frac{1}{9},\qquad \left(\frac{8}{3}\right)^2=\frac{64}{9}.
$$


Add them:

$$
\frac{49}{9}+\frac{1}{9}+\frac{64}{9}=\frac{114}{9}=\frac{38}{3}.
$$


Now divide by $m=3$ to get the Gaussian MLE for the variance:

$$
\nu_{\mathrm{MLE}}=\frac{1}{3}\left[\left(2-\frac{13}{3}\right)^2+\left(4-\frac{13}{3}\right)^2+\left(7-\frac{13}{3}\right)^2\right]
$$


which simplifies to

$$
\nu_{\mathrm{MLE}}=\frac{1}{3}\cdot \frac{38}{3}=\frac{38}{9}\approx 4.22.
$$


So the Gaussian fit is built in two explicit stages:

1. choose the center that minimizes total squared error;
2. measure the average squared residual size around that fitted center.

That second number is not the unbiased sample variance from introductory statistics. It is the Gaussian maximum-likelihood variance, which uses division by $m$ because it comes from maximizing the likelihood.

### Example 2-16: Discrete MLE

For a discrete distribution over states $x$, the MLE copies empirical frequencies into the probability table:

$$
\rho_{x,\mathrm{MLE}} = \frac{m_x}{m}
$$


where $m_x$ is the count of state $x$ in the data.

Work through the concrete sample

$$
D=\{a,c,a,b,a,c\}.
$$


There are

$$
m=6
$$


observations. Count each state:

$$
m_a=3,\qquad m_b=1,\qquad m_c=2
$$


Now divide each count by the total sample size:

$$
\rho_{a,\mathrm{MLE}}=\frac{3}{6},\qquad \rho_{b,\mathrm{MLE}}=\frac{1}{6},\qquad \rho_{c,\mathrm{MLE}}=\frac{2}{6}
$$


so the fitted PMF is

<table align="center">
  <thead>
    <tr><th>state</th><th>count</th><th>MLE probability</th></tr>
  </thead>
  <tbody>
    <tr><td>$a$</td><td>$3$</td><td>$3/6=0.5$</td></tr>
    <tr><td>$b$</td><td>$1$</td><td>$1/6 \approx 0.167$</td></tr>
    <tr><td>$c$</td><td>$2$</td><td>$2/6 \approx 0.333$</td></tr>
  </tbody>
</table>

This example is the direct multi-state analogue of the Bernoulli MLE. In the Bernoulli case, we copy the fraction of ones into the single success-probability parameter. In the multi-state case, we copy each observed relative frequency into the corresponding row of the probability table.

### Maximum Likelihood and Exponential Families

This subsection answers a natural structural question: why do exponential families keep reappearing in estimation? The reason is that their likelihoods collapse the data into a small set of summary statistics, and the MLE is determined by matching those summaries.

For a canonical exponential-family model

$$
p_{\theta}(x) = h(x)\exp\left(\theta^{\top}\phi(x) - A(\theta)\right)
$$


the log-likelihood of independent and identically distributed data is

$$
\ell(\theta) = \sum_i \log h(x^{(i)}) + \theta^{\top} \sum_i \phi(x^{(i)}) - m A(\theta)
$$


The phrase **independent and identically distributed** should be read one word at a time.

- **Independent** means that once the parameter $\theta$ is fixed, the observations do not probabilistically influence one another, so their joint probability factors into a product.
- **Identically distributed** means each observation is governed by the same one-observation model form and the same parameter value $\theta$.

Those two assumptions are exactly what allow one repeated one-observation formula to become a product over samples and then a sum in the log-likelihood.

Differentiating with respect to $\theta$ gives

$$
\nabla_\theta \ell(\theta) = \sum_i \phi(x^{(i)}) - m \nabla_\theta A(\theta).
$$


For exponential families,

$$
\nabla_\theta A(\theta) = \mathbb{E}_\theta[\phi(X)],
$$


so the first-order optimality condition becomes

$$
\frac{1}{m}\sum_i \phi(x^{(i)}) = \mathbb{E}_\theta[\phi(X)].
$$


This is the explicit moment-matching statement: the fitted model reproduces the empirical averages of the sufficient statistics. That fact matters because it reduces parameter fitting to a comparison between two summaries of the same features: what the data average says, and what the model average says. In many exponential-family models, that comparison leads to clean optimization problems and interpretable estimators.

The phrase moment matching should be read literally. The left-hand side is the empirical average of the sufficient statistics computed from the observed sample. The right-hand side is the model's expected value of those same statistics under parameter $\theta$. At the optimum, those two objects agree.

For Bernoulli, the sufficient statistic is the observed variable $X$ itself, so moment matching says

$$
\mathbb{E}_\theta[X] = \frac{1}{m}\sum_i x^{(i)}.
$$


But the model expectation of $X$ is exactly $\rho$, so the condition reduces to

$$
\rho = \text{sample mean},
$$


which reproduces the familiar Bernoulli MLE immediately. So the Bernoulli success frequency is not an isolated trick; it is the simplest case of a general exponential-family principle.

### Overfitting

Likelihood alone can overfit. If a model is too flexible and the data set is too small, the MLE may explain the training data perfectly while generalizing poorly. Histogram models make this especially clear: as the number of bins grows, the likelihood on the training data can keep increasing even when the estimate assigns unrealistic probability mass to new observations. In the extreme limit where each observation gets its own tiny bin, the model can memorize the sample rather than discover a stable distributional pattern.

The core reason is that pure likelihood asks only, "how well can this model explain the data already seen?" It does not ask whether the fitted pattern is robust enough to predict new data. A model with many parameters can exploit accidental quirks of a small sample and thereby earn a high training score for the wrong reason.

A toy example is enough to show the mechanism. If eight data points occupy eight distinct locations and we fit a histogram with sixty-four bins, most bins are empty and a few bins receive all the mass. The training likelihood becomes large because each observed sample falls into a narrow high-density bin. But a new sample landing between those bins receives nearly zero support, even if it comes from the same underlying process that generated the training sample. So the fitted histogram is representing the accidental placement of the observed points more strongly than the stable shape of the underlying distribution.

<p align="center">
  <img src="../notes/02_probability_reconstructed/assets/figure_2_17_histograms.png" alt="Histogram likelihood progression" width="860">
</p>

The three histograms make the overfitting mechanism visible in a concrete way. With one bin, the model forces the entire support to have one constant density value, so it cannot represent any local variation in the sample. With a moderate number of bins, the model can respond to broad changes in where observations are concentrated while still averaging over nearby points. With too many bins, each bin is supported by too little data. The fitted density then becomes extremely sensitive to the accidental placement of the observed sample, assigning very high density in bins that happened to contain points and very low density in neighboring bins that happened to be empty.

The key lesson is that "higher likelihood" is incomplete unless we also specify **on which data** that likelihood is being measured. Training likelihood can keep increasing because a flexible model can adapt itself more and more closely to the particular sample it already saw. But predictive performance depends on how well the fitted structure matches the underlying data-generating pattern rather than the idiosyncrasies of one finite sample. Overfitting is exactly this mismatch: the model becomes better at describing the observed sample and worse at predicting fresh data from the same source.

### Posterior Distributions

In the Bayesian view, we keep a distribution over parameters:

$$
p(\theta \mid D) \propto p(D \mid \theta)p(\theta).
$$


The notation

$$
p(\theta \mid D)
$$


should be read in the most literal possible way: it is the conditional distribution of the parameter $\theta$ given the observed data $D$. So the posterior is not a brand-new kind of mathematical object. It is the ordinary conditional-probability idea from earlier in the chapter, now applied to parameter uncertainty instead of ordinary events.

The missing normalization constant is the evidence

$$
p(D) = \int p(D \mid \theta)p(\theta)\,d\theta.
$$


So Bayes' rule in full form is

$$
p(\theta \mid D) = \frac{p(D \mid \theta)p(\theta)}{p(D)}.
$$


Each term has a separate role.

- The prior $p(\theta)$ encodes what looked plausible before the data arrived.
- The likelihood $p(D \mid \theta)$ measures how well each parameter explains the observed data.
- The evidence $p(D)$ is the total probability of the data after averaging over all parameter values allowed by the prior.
- The posterior $p(\theta \mid D)$ is the normalized result after combining the first two pieces.

The posterior therefore does something different from point estimation. A point estimator returns one preferred number, such as $\rho_{\mathrm{MLE}}=0.6$. A posterior returns a whole distribution over $\rho$, which tells us not only where the plausible values are centered but also how spread out that uncertainty still is after observing the data. This matters conceptually because it keeps uncertainty visible rather than hiding it inside one summary number, and it matters computationally because such full updates are easy to compute exactly only in special cases, such as conjugate prior-likelihood pairs.

For a concrete update, start with

$$
\rho \sim \mathrm{Beta}(2,2)
$$


and observe

$$
D=\{1,0,1\}.
$$


Now spell out the pieces instead of jumping directly to the answer. The prior density is

$$
p(\rho)=6\rho(1-\rho),
$$


because $\mathrm{Beta}(2,2)$ has normalization constant

$$
\frac{\Gamma(4)}{\Gamma(2)\Gamma(2)}=6.
$$


The data contain

$$
m_1=2 \quad \text{ones}, \qquad m_0=1 \quad \text{zero},
$$


so the Bernoulli likelihood is

$$
p(D \mid \rho)=\rho^2(1-\rho).
$$


Multiply prior and likelihood:

$$
p(\rho \mid D)\propto p(D \mid \rho)p(\rho)\propto \rho^2(1-\rho)\cdot \rho(1-\rho)=\rho^3(1-\rho)^2.
$$


This unnormalized posterior expression has exponent

$$
3
$$


on $\rho$ and exponent

$$
2
$$


on $(1-\rho)$. Since a $\mathrm{Beta}(a,b)$ density has the form

$$
\rho^{a-1}(1-\rho)^{b-1},
$$


we identify

$$
a-1=3,\qquad b-1=2,
$$


so

$$
a=4,\qquad b=3.
$$


Therefore the posterior is

$$
\rho \mid D \sim \mathrm{Beta}(4,3).
$$


Now the pseudo-count interpretation can be stated cleanly. The prior $\mathrm{Beta}(2,2)$ contributes one exponent to $\rho$ and one exponent to $(1-\rho)$ before any real data are observed. The actual sample contributes two more powers of $\rho$ and one more power of $(1-\rho)$. After multiplication, the exponents add. That is why the posterior behaves as if prior information and observed counts have been combined.

That pseudo-count language is an interpretation of the algebra, not a literal story that extra coin flips physically occurred. What is literally true is simpler: the prior contributes exponents, the data contribute exponents, and multiplication adds those exponents. The pseudo-count mnemonic is useful only because it mirrors that exponent bookkeeping.

It is also worth computing the evidence term once, because students often see the symbol $p(D)$ and are told that it is "just a normalization constant" without ever seeing where it comes from. Here the likelihood contributes the unnormalized factor

$$
p(D \mid \rho)=\rho^2(1-\rho),
$$


and the $\mathrm{Beta}(2,2)$ prior density is

$$
p(\rho)=6\rho(1-\rho).
$$


So the unnormalized posterior is

$$
p(D \mid \rho)p(\rho)=6\rho^3(1-\rho)^2.
$$


The evidence is the integral of this quantity:

$$
p(D)=\int_0^1 6\rho^3(1-\rho)^2\,d\rho.
$$


Expand the polynomial and integrate term by term:

$$
\int_0^1 \rho^3(1-\rho)^2\,d\rho=\int_0^1 (\rho^3-2\rho^4+\rho^5)\,d\rho=\left[\frac{1}{4}-\frac{2}{5}+\frac{1}{6}\right]=\frac{1}{60}.
$$


Therefore

$$
p(D)=6\cdot \frac{1}{60}=\frac{1}{10}.
$$


Dividing the unnormalized posterior by $p(D)$ gives the normalized posterior density:

$$
p(\rho \mid D)=\frac{6\rho^3(1-\rho)^2}{1/10}=60\rho^3(1-\rho)^2,
$$


which is exactly the $\mathrm{Beta}(4,3)$ density. In this example, the evidence plays a precise role: it is the number obtained by integrating the unnormalized posterior over all possible values of $\rho$, and dividing by that number forces the posterior density to have total area one. That is why $p(D)$ functions as the normalization constant.

### Example 2-18: Beta-Bernoulli Conjugacy

If the likelihood is Bernoulli and the prior is $\mathrm{Beta}(a,b)$, then the posterior is still Beta:

$$
\rho \mid D \sim \mathrm{Beta}(a+m_1, b+m_0).
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


which is exactly the unnormalized part of another Beta density. This is the simplest example of conjugacy.

The structural reason conjugacy works is that the prior and the likelihood are built from the same two algebraic pieces, $\rho$ and $(1-\rho)$. Multiplying them merely adds exponents, so the posterior stays in the same family. That is the general pattern behind conjugate priors: family-preserving algebra.

If we plug in $a=b=2$ and observe $m_1=3$, $m_0=1$, then

$$
\rho \mid D \sim \mathrm{Beta}(5,3).
$$


The arithmetic should be read explicitly:

$$
a+m_1=2+3=5,\qquad b+m_0=2+1=3.
$$


The posterior is more concentrated than the prior because more information has been accumulated, and it is shifted toward heads because the data contain more ones than zeros. This can be read numerically as well. The prior $\mathrm{Beta}(2,2)$ has total concentration

$$
2+2=4,
$$


while the posterior $\mathrm{Beta}(5,3)$ has total concentration

$$
5+3=8.
$$


So the posterior carries more total mass and is therefore narrower. At the same time, its center moves toward heads because the first shape parameter increased by more than the second. In other words, the update changes both location and confidence: the center moves toward the evidence, and the distribution narrows because the effective sample size has increased.

### Worked Example: Dirichlet-Categorical Pseudo-Counts

The categorical analogue of Beta-Bernoulli conjugacy is Dirichlet-Categorical conjugacy. Let a three-class probability vector satisfy

$$
\theta=(\theta_1,\theta_2,\theta_3) \sim \mathrm{Dir}(2,2,2).
$$


Now observe four class labels with counts

$$
m=(3,1,0).
$$


Spell out what the count vector means before doing the update:

- class $1$ was observed $3$ times,
- class $2$ was observed $1$ time,
- class $3$ was observed $0$ times.

The prior Dirichlet parameters are

$$
(2,2,2),
$$


so the coordinatewise update is

$$
2+3=5,\qquad 2+1=3,\qquad 2+0=2.
$$


Therefore

$$
\theta \mid D \sim \mathrm{Dir}(5,3,2).
$$


This is the multi-class pseudo-count interpretation in explicit form. The prior behaves like two virtual observations in each class. The data then add three more observations to class $1$, one to class $2$, and none to class $3$.

The posterior mean is

$$
\mathbb{E}[\theta \mid D] = ( \frac{5}{10}, \frac{3}{10}, \frac{2}{10} ) =(0.5,0.3,0.2).
$$


The denominator

$$
10
$$


comes from the total posterior concentration:

$$
5+3+2=10.
$$


So the posterior mean is not arbitrary componentwise division. Each coordinate is being divided by the sum of all updated Dirichlet parameters.

The posterior mean for class $3$ is still positive even though class $3$ was never observed. The reason is explicit in the numbers: the posterior parameter for that class is

$$
2+0=2,
$$


so the posterior mean becomes

$$
\frac{2}{5+3+2}=\frac{2}{10}=0.2.
$$


Compare that with pure MLE. Using only the observed counts would give

$$
\left(\frac{3}{4},\frac{1}{4},0\right),
$$


so the unseen class would receive probability zero. The Dirichlet prior prevents that collapse by keeping some prior mass on every class. That is the smoothing effect: "not yet seen" is treated as weaker information than "known to be impossible."

### Posterior Estimators

After computing a posterior distribution, we still face a practical question: do we keep the full posterior, or do we compress it to one representative number?

When a single number is required, two common choices are the posterior mean and the MAP estimate.

The posterior mean is

$$
\theta_{\mathrm{PM}}=\mathbb{E}_{p(\theta \mid D)}[\theta].
$$


Here $\theta_{\mathrm{PM}}$ means posterior mean and $\theta_{\mathrm{MAP}}$ below means maximum a posteriori. This is only a notation choice. Many books would write the same estimators with hats.

This is literally the average of $\theta$ under the posterior distribution. It uses the entire posterior shape, not just one high-density point.

The MAP estimate is

$$
\theta_{\mathrm{MAP}}=\arg\max_{\theta} p(\theta \mid D).
$$


This is the mode of the posterior: the single parameter value at which the posterior density is largest.

These two estimators answer different questions.

- The posterior mean asks: if we average over posterior uncertainty, where is the center of mass?
- The MAP asks: which single parameter value is most favored locally by the posterior density?

Because those questions are different, the answers generally differ.

For the Beta-Bernoulli model, if the prior is $\mathrm{Beta}(a,b)$ and the data contain $m_1$ ones and $m_0$ zeros, then the posterior is

$$
\mathrm{Beta}(a+m_1,b+m_0).
$$


The posterior mean is therefore

$$
\rho_{\mathrm{PM}}=\frac{a+m_1}{a+b+m_1+m_0}.
$$


If the updated Beta parameters are both greater than $1$, the interior MAP estimate is

$$
\rho_{\mathrm{MAP}}=\frac{a+m_1-1}{a+b+m_1+m_0-2}.
$$


The condition matters. If either updated shape parameter is at most $1$, then the posterior mode moves to a boundary point, so the simple interior formula no longer applies. That is a structural limit, not a cosmetic detail.

Consider the posterior

$$
\rho \mid D \sim \mathrm{Beta}(5,3).
$$


Then

$$
\rho_{\mathrm{PM}}=\frac{5}{8}=0.625
$$


and

$$
\rho_{\mathrm{MAP}}=\frac{5-1}{5+3-2}=\frac{4}{6}\approx 0.667.
$$


The MAP is larger because it selects the peak of the density, while the posterior mean averages over all values of $\rho$ weighted by posterior mass. If the distribution is asymmetric, those two operations do not coincide.

It is helpful to place MLE next to them conceptually. MLE ignores the prior and keeps only the parameter value that maximizes the likelihood. MAP adds the prior before maximizing. The posterior mean goes one step further and averages instead of maximizing. So the three estimators compress information differently:

- MLE keeps only the likelihood peak.
- MAP keeps only the posterior peak.
- Posterior mean keeps the whole posterior and then averages.

### Example 2-19: Bernoulli Posterior Estimates

Work through one small data set completely. Let

$$
D=\{1,1,0\}.
$$


So the data contain

$$
m_1=2 \quad \text{successes}, \qquad m_0=1 \quad \text{failure}.
$$


The Bernoulli likelihood is therefore

$$
p(D \mid \rho)=\rho^2(1-\rho)^1.
$$


If we ignore the prior and compute MLE, we maximize this likelihood over $\rho$. For Bernoulli data, the MLE is the empirical fraction of ones:

$$
\rho_{\mathrm{MLE}}=\frac{2}{3}\approx 0.667.
$$


Now include the prior

$$
\rho \sim \mathrm{Beta}(2,2).
$$


The prior density is proportional to

$$
\rho^{2-1}(1-\rho)^{2-1}=\rho(1-\rho).
$$


Multiply prior and likelihood:

$$
p(\rho \mid D) \propto \rho^2(1-\rho)^1 \cdot \rho^1(1-\rho)^1=\rho^3(1-\rho)^2.
$$


So the posterior is

$$
\rho \mid D \sim \mathrm{Beta}(4,3).
$$


Now compute three different point summaries.

The posterior mean is

$$
\rho_{\mathrm{PM}}=\frac{4}{4+3}=\frac{4}{7}\approx 0.571.
$$


The MAP estimate is

$$
\rho_{\mathrm{MAP}}=\frac{4-1}{4+3-2}=\frac{3}{5}=0.6.
$$


The MLE, from above, is

$$
\rho_{\mathrm{MLE}}=\frac{2}{3}\approx 0.667.
$$


Putting them side by side,

$$
\rho_{\mathrm{PM}} \approx 0.571, \qquad \rho_{\mathrm{MAP}}=0.6, \qquad \rho_{\mathrm{MLE}}\approx 0.667.
$$


This ordering makes the prior effect visible. The prior $\mathrm{Beta}(2,2)$ is centered at $0.5$, so both Bayesian estimators are pulled back toward $0.5$ relative to MLE. The posterior mean moves farther because it averages over the whole posterior. The MAP moves less because it only tracks the posterior peak.

This is why the pseudo-count language is helpful. In the posterior-mean formula, the prior behaves like two prior units of mass, one on each side. In the MAP formula, the effective interior adjustment is smaller because the mode calculation subtracts one from each updated shape parameter. The important point is not memorizing that wording, but seeing the mechanism: Bayesian estimates combine observed counts with prior shape before reporting a single number.

### Sequential Belief Updating

Bayesian updating naturally supports sequential learning: after observing one batch of data, the posterior becomes the prior for the next batch.

<p align="center">
  <img src="../notes/02_probability_reconstructed/assets/figure_2_4_sequential_updates.png" alt="Sequential belief updating" width="860">
</p>

The figure is deliberately procedural: first combine the prior with the first data batch, then treat the resulting posterior as the next prior before incorporating the second batch. Nothing conceptually new happens in the second step; Bayesian learning is the repeated application of the same update rule.

This matters operationally because many real systems receive data over time rather than in one batch. Sequential updating says you do not need to restart the whole calculation from scratch each time. You can carry forward the posterior as the complete current summary of past information.

For example, begin with $\mathrm{Beta}(2,2)$. After the first batch $D_1=\{1,0,1\}$, the posterior is $\mathrm{Beta}(4,3)$. If a second batch $D_2=\{1,1\}$ arrives later, the new posterior is

$$
\mathrm{Beta}(6,3).
$$


If we had processed all five observations at once, we would obtain exactly the same answer. Sequential updating is therefore not an approximation; it is algebraically equivalent to batch updating when the model assumptions are unchanged.

### Example 2-20: Coin Toss Hyper-Prior

Sometimes we are uncertain not only about the parameter $\rho$, but also about which prior story is appropriate. A hyper-prior keeps that higher-level uncertainty explicit.

One simple construction is a mixture of two Beta priors:

- a "fair-coin-like" prior, concentrated near $0.5$;
- an "extreme-coin" prior, concentrated near $0$ and $1$.

Introduce a latent variable

$$
H \in \{\mathrm{fair},\mathrm{extreme}\}.
$$


Then the model can be written as

$$
H \sim \mathrm{Bernoulli}(\pi),
$$


$$
\rho \mid H=\mathrm{fair} \sim \mathrm{Beta}(20,20),
$$


$$
\rho \mid H=\mathrm{extreme} \sim \mathrm{Beta}(0.3,0.3),
$$


and finally

$$
X_i \mid \rho \sim \mathrm{Bernoulli}(\rho).
$$


This is a full generative story. First choose which prior regime is active. Then draw the coin bias $\rho$ from that regime. Then generate observations from that coin.

<p align="center">
  <img src="../notes/02_probability_reconstructed/assets/figure_2_20_beta_hyperprior.png" alt="Mixture of Beta priors" width="860">
</p>

The left and middle panels represent two qualitatively different prior beliefs. The mixture panel averages them according to the hyper-prior on $H$. So before any data are seen, the model already says: "I am not fully committed to one prior story."

It helps to imagine one sample path. Suppose the latent draw is

$$
H=\mathrm{fair}.
$$


Then the model might draw

$$
\rho=0.47
$$


from the fair-coin prior, and the observed tosses could be

$$
1,0,1,1,0,\ldots
$$


By contrast, if

$$
H=\mathrm{extreme},
$$


the model might draw

$$
\rho=0.94,
$$


which would make long runs of heads much more plausible. So there are really two uncertainty layers in the model. First, we are uncertain about which regime is active:

- is this an ordinary nearly fair coin regime?
- or is this an extreme-bias regime?

Only after that regime is chosen do we ask for the exact value of $\rho$. That is why the hyper-prior lives one level above the Beta prior: it governs uncertainty about the kind of prior story, not just the parameter value inside one fixed story.

That is the motivation for hierarchical modeling in one sentence: sometimes the difficult uncertainty is not only "what is the parameter value?" but also "which parameter regime am I in?" A hyper-prior gives the model a place to represent that second layer explicitly.

### Weakly Informative Priors

A prior is never literally uninformative, because any prior expresses some preference over parameter values. The choice of parameterization matters: a prior that is uniform in $\rho$ is not uniform in the natural parameter $\eta = \log(\rho/(1-\rho))$. So "uninformative" is not an intrinsic property of a density alone; it is a statement about a density together with the coordinate system in which it is declared flat.

The practical goal is therefore usually not "make the prior say absolutely nothing," because that is not genuinely achievable. The practical goal is to choose a weakly informative prior: strong enough to prevent pathological estimates when the sample is tiny, but weak enough that reasonable amounts of data can dominate it.

A weakly informative prior tries to do something more modest and more realistic. Instead of pretending to encode no information at all, it encodes only broad structural knowledge, such as "extreme probabilities are possible but should not be overwhelmingly favored before data arrive." The goal is to stabilize inference without forcing a narrow prior story that the analyst cannot justify.

### Example 2-21: Priors for the Bernoulli Likelihood

The simplest Beta prior is

$$
\rho \sim \mathrm{Beta}(1,1).
$$


Because $\mathrm{Beta}(1,1)$ is uniform on $[0,1]$, this means

$$
p_{\rho}(\rho)=1, \qquad 0 \le \rho \le 1.
$$


It is tempting to call this "uninformative." The problem is that flatness depends on the coordinate system.

Rewrite the same Bernoulli model in the natural parameter

$$
\eta=\log\left(\frac{\rho}{1-\rho}\right).
$$


From the earlier derivation,

$$
\rho=\frac{e^{\eta}}{1+e^{\eta}}.
$$


Differentiate:

$$
\frac{d\rho}{d\eta}=\frac{e^{\eta}}{(1+e^{\eta})^2}=\rho(1-\rho).
$$


Now transform the prior from the $\rho$ scale to the $\eta$ scale:

$$
p_{\eta}(\eta)=p_{\rho}(\rho(\eta))\left|\frac{d\rho}{d\eta}\right|.
$$


Since $p_{\rho}(\rho)=1$ on $[0,1]$, this becomes

$$
p_{\eta}(\eta)=\frac{e^{\eta}}{(1+e^{\eta})^2}.
$$


That density is not constant in $\eta$. It is largest near $\eta=0$ and decays in both tails. So a prior that is flat in probability space is not flat in log-odds space.

This is the real lesson. The phrase "uninformative prior" is incomplete unless you also specify the coordinate system. Uniform in $\rho$ means equal prior mass for equal-width intervals of probability. It does not mean equal prior mass for equal-width intervals of log-odds.

### Bayesian Model Selection

Suppose we are comparing whole models, not just parameters inside one model. Then the key quantity is the model evidence, also called the marginal likelihood:

$$
p(D \mid M)=\int p(D \mid \theta,M)p(\theta \mid M)\,d\theta.
$$


Taking logarithms gives

$$
\log p(D \mid M)=\log \int p(D \mid \theta,M)p(\theta \mid M)\,d\theta.
$$


Read this formula carefully. For a fixed model $M$:

- $\theta$ ranges over the parameter space of that model;
- $p(D \mid \theta,M)$ measures fit at one parameter value;
- $p(\theta \mid M)$ weights parameter values by the prior;
- the integral averages fit over the whole parameter space.

That averaging is the key difference from maximum likelihood. Maximum likelihood asks only for the single best parameter value. Model evidence asks how well the model performs on average under its prior.

This is why evidence automatically penalizes excessive flexibility. A very flexible model may contain a few isolated parameter settings that match the data extremely well, but if most of its parameter space gives poor fit, then the prior-weighted average can still be small. By contrast, a simpler model may never reach such a dramatic peak, yet many of its parameter values may give consistently decent fit. Evidence therefore rewards a model whose prior mass is concentrated on parameter regions that make the observed data plausible, rather than a model that succeeds only after careful parameter tuning.

It helps to compare two stylized likelihood landscapes.

- In Model A, the likelihood is extremely high inside a tiny region of parameter space and very low almost everywhere else.
- In Model B, the likelihood never reaches such a dramatic maximum, but it stays moderately high across a broad region of parameter space.

Maximum likelihood looks only at the single highest point, so it would choose Model A if that sharp peak is taller. Evidence instead integrates over the full parameter space. If the high-likelihood region in Model A is too small, then its average can be lower than Model B's broader plateau. That is the mechanism behind the complexity penalty: the penalty is not added by hand; it appears because averaging over many weakly performing parameter settings dilutes the contribution of a few exceptional ones.

The BIC score is a large-sample approximation to the log evidence:

$$
\mathrm{BIC}=\max_{\theta}\log p(D \mid \theta,M)-\frac{d}{2}\log m,
$$


where $d$ is the number of free parameters and $m$ is the number of observations.

The first term rewards fit. The second term penalizes complexity. So BIC should be read as a cheaper approximation to the same basic tradeoff that exact evidence captures: fit versus flexibility.

The important conceptual distinction is this:

- maximum likelihood asks, "How well can this model fit if I tune it as well as possible?"
- evidence asks, "How much probability mass does this model devote to parameter settings that explain the data well?"

Those are not the same question, and model selection changes depending on which one you ask.

### Example 2-22: Bayesian Histogram Estimator

In a histogram model, the number of bins controls model complexity. With few bins, the model is rigid and smooth. With many bins, the model is flexible but can overfit the sample.

If we place a Dirichlet prior on the bin probabilities, then each bin count becomes one component of a categorical-count model, and we can compare different choices of bin count using either exact marginal likelihood or BIC.

The structural tradeoff is explicit:

- too few bins produce high bias, because real structure is averaged away;
- too many bins produce high variance, because the model spends parameters fitting random fluctuations.

<p align="center">
  <img src="../notes/02_probability_reconstructed/assets/figure_2_22_histogram_model_scores.png" alt="Histogram model selection scores" width="860">
</p>

Read the figure from left to right as a complexity sweep. Moving right means using more bins and therefore more free probabilities to estimate.

The maximum-likelihood curve usually keeps improving because extra bins let the model chase the observed data more closely. But the evidence and BIC curves do not ask only about best fit. They ask whether that extra flexibility is justified by the amount of data available. Once the added bins mostly fit noise rather than stable structure, the penalized scores flatten or decline.

So the message of the figure is not "there is always one magical best number of bins." The deeper message is that Bayesian scoring and BIC operationalize the same principle: complexity must earn its keep.

### Worked Example: One Coin Versus Two Coin Model Selection

Suppose a first batch of flips is

$$
D_A=\{H,T,T\},
$$


and a second batch is

$$
D_B=\{T,H,H\}.
$$


We will compare two models.

- Model $M_1$: one shared coin with parameter $\rho$.
- Model $M_2$: two different coins with parameters $\rho_A$ and $\rho_B$.

If there is only one coin, all six flips share the same head probability $\rho$. Across both batches there are three heads out of six observations, so

$$
\rho_{\mathrm{MLE}}=\frac{3}{6}=0.5.
$$


If there are two different coins, the first batch gets parameter $\rho_A$ and the second gets parameter $\rho_B$. Their MLEs are the within-batch head frequencies:

$$
\rho_{A,\mathrm{MLE}}=\frac{1}{3},\qquad \rho_{B,\mathrm{MLE}}=\frac{2}{3}.
$$


Now compute the maximized average log-likelihood under each model.

Under the one-coin model, the fitted probability of both heads and tails is $0.5$, so every flip contributes $\log 0.5$. Therefore

$$
\text{one-coin average log-likelihood} = (3 \log 0.5 + 3 \log 0.5)/6 = \log 0.5 \approx -0.693.
$$


Under the two-coin model, batch $A$ has one head and two tails, while batch $B$ has two heads and one tail. So the maximized average log-likelihood is

$$
\text{two-coin average log-likelihood} = \bigl(2 \log(1/3)+4 \log(2/3)\bigr)/6 \approx -0.637.
$$


So raw fit prefers the two-coin model. That is not surprising: extra parameters make it easier to fit the observed sample.

BIC now adds a complexity penalty. The one-coin model has

$$
d=1,
$$


while the two-coin model has

$$
d=2.
$$


With

$$
m=6
$$


observations, the penalized average scores are

$$
\text{one-coin BIC average} = -0.693-(\log 6)/12 \approx -0.842,
$$


$$
\text{two-coin BIC average} = -0.637-(\log 6)/6 \approx -0.935.
$$


So BIC prefers the one-coin model, because the improvement in fit is not large enough to justify the extra parameter.

That is the central model-selection lesson. The two-coin model achieves a higher raw training fit because it has an extra degree of freedom. But the numerical improvement in average log-likelihood is smaller than the BIC complexity penalty charged for that extra parameter. Once complexity is priced in explicitly, the simpler explanation wins. This is exactly the kind of situation where maximum likelihood alone can overstate the case for a more flexible model.

After penalization, the one-coin model wins. The extra flexibility of the two-coin model is not justified by only six flips.

Now increase the data while keeping the same qualitative split:

$$
D_A=\{H,T,T,T,T\},\qquad D_B=\{T,H,H,H,H\}.
$$


The one-coin MLE is still

$$
\rho_{\mathrm{MLE}}=0.5,
$$


while the two-coin MLEs become

$$
\rho_{A,\mathrm{MLE}}=0.2,\qquad \rho_{B,\mathrm{MLE}}=0.8.
$$


The one-coin penalized average score is now

$$
\text{one-coin BIC average} \approx -0.808,
$$


while the two-coin penalized average score is

$$
\text{two-coin BIC average} \approx -0.731.
$$


Now the two-coin model wins even after the penalty. The lesson is structural: with small data, the simpler model is often preferred because complexity costs dominate. With more data, a genuine difference between the two batches can become strong enough that the richer model earns back its penalty.

### Retain from 2.3

- Likelihood is a function of parameters with the data held fixed; it is not itself a probability distribution over parameters.
- MLE fits the data as well as possible inside the chosen model class but does not by itself control overfitting.
- Conjugate Bayesian updates preserve uncertainty and make pseudo-count interpretations explicit.
- Model selection is not just about best fit; it is about fit relative to complexity.
- This whole section reuses the same normalization and expectation ideas from `2.1` and `2.2`, but now with the parameters treated as the unknown objects.

### Do Not Confuse in 2.3

- Do not confuse probability with likelihood; they are the same algebraic expression used in different roles.
- Do not confuse posterior mean, MAP, and MLE; they agree only in special cases.
- Do not treat a prior declared "flat" in one parameterization as uninformative in every parameterization.
- Do not assume a richer model is better just because its training likelihood is higher.
- Do not forget what is fixed and what is varying in each expression; most learning confusions begin there.

## 2.4 Convexity

This section is supporting background rather than core probability machinery. It appears here because `2.3` introduced optimization problems such as MLE, MAP, and model comparison, and those problems depend heavily on the shape of the objective function. For the course, the main reason to read it is to understand why some likelihood objectives are well behaved and why exponential-family optimization often has a clean global structure.

A convex function is defined on a **convex domain**, meaning a set of points with the property that whenever $x$ and $x'$ lie in the domain, the whole line segment between them also lies in the domain. That condition matters because the definition compares the function value at the weighted average

$$
\alpha x + (1-\alpha)x'.
$$


The number $\alpha \in [0,1]$ is a mixing weight, so $\alpha x + (1-\alpha)x'$ is called a convex combination of $x$ and $x'$. A function $f$ is convex if

$$
f(\alpha x + (1-\alpha)x') \le \alpha f(x) + (1-\alpha)f(x')
$$


for all $\alpha \in [0,1]$ and all domain points $x,x'$. In words: evaluate the function after averaging the inputs, and compare that with averaging the function values. Convexity says the first quantity is never larger.

Strict convexity makes the inequality strict for distinct points when $0<\alpha<1$:

$$
f(\alpha x + (1-\alpha)x') < \alpha f(x) + (1-\alpha)f(x').
$$


So a strictly convex function cannot contain a flat line segment.

Equivalent characterizations are:

$$
f(x') \ge f(x) + \nabla f(x)\cdot(x'-x)
$$


and, when second derivatives exist,

$$
\nabla^2 f(x) \succeq 0.
$$


These characterizations are compact, so it is worth unpacking them. The first-order statement says that the tangent line or tangent plane at $x$ lies below the graph everywhere else. The second-order statement says the Hessian has no negative curvature directions. Positive semidefinite means

$$
v^T \nabla^2 f(x)\,v \ge 0 \qquad \text{for every vector } v,
$$


so every directional second derivative is nonnegative.

Convex functions are useful because every local minimum is global, and a strictly convex function has a unique minimum. Positive semidefinite curvature allows flat directions, so multiple minimizers can still exist. Positive definite curvature removes those flat directions and forces uniqueness.

A full worked example is $f(x)=x^2$. For any $x$ and $x'$ and any $\alpha \in [0,1]$,

$$
f(\alpha x + (1-\alpha)x') = (\alpha x + (1-\alpha)x')^2
$$


expands to

$$
\alpha x^2 + (1-\alpha)x'^2 - \alpha(1-\alpha)(x-x')^2.
$$


Since the last term is nonpositive, we obtain

$$
(\alpha x + (1-\alpha)x')^2 \le \alpha x^2 + (1-\alpha)x'^2.
$$


That is the convexity inequality in explicit algebraic form. The term

$$
-\alpha(1-\alpha)(x-x')^2
$$


is the correction term that makes the left-hand side smaller than the weighted average on the right. Geometrically, it says the parabola lies below every secant line connecting two points on its graph.

Jensen's inequality is the probability version of convexity:

$$
\mathbb{E}[f(X)] \ge f(\mathbb{E}[X])
$$


for convex $f$.

It is the same idea with probability weights. If $X$ takes values $x_1,\dots,x_k$ with probabilities $p_1,\dots,p_k$, then

$$
\mathbb{E}[X]=\sum_i p_i x_i,\qquad \mathbb{E}[f(X)]=\sum_i p_i f(x_i).
$$


So Jensen compares the function of the average with the average of the function. A concrete example is $f(x)=x^2$ and a random variable that equals $0$ or $2$ with equal probability. Then

$$
\mathbb{E}[X]=1,\qquad f(\mathbb{E}[X])=1,
$$


while

$$
\mathbb{E}[f(X)] = \frac{1}{2}f(0)+\frac{1}{2}f(2)=2.
$$


So indeed $\mathbb{E}[f(X)] \ge f(\mathbb{E}[X])$.

### Example 2-23: Convexity and the Exponential Family

The negative log-likelihood of a canonical exponential-family model is convex in its natural parameters. The reason is explicit, but it helps to write the logic in full rather than jumping directly to the Hessian formula.

For the canonical form

$$
p_{\theta}(x)=h(x)\exp\left(\theta^{\top}\phi(x)-A(\theta)\right)
$$


the log-likelihood of i.i.d. data $x^{(1)},\dots,x^{(m)}$ is

$$
\ell(\theta)=\sum_{i=1}^m \log h(x^{(i)}) + \theta^{\top} \sum_{i=1}^m \phi(x^{(i)}) - mA(\theta)
$$


Therefore the negative log-likelihood is

$$
-\ell(\theta)=mA(\theta)-\theta^{\top}\sum_{i=1}^m \phi(x^{(i)})-\sum_{i=1}^m \log h(x^{(i)})
$$


The last term is constant in $\theta$, and the middle term is linear in $\theta$. So all curvature comes from the log-partition function $A(\theta)$.

Differentiate $A(\theta)$:

$$
\frac{\partial A(\theta)}{\partial \theta_j} = \mathbb{E}_\theta[\phi_j(X)], \qquad \frac{\partial^2 A(\theta)}{\partial \theta_j \partial \theta_k} = \mathrm{Cov}_\theta(\phi_j(X), \phi_k(X)).
$$


The first identity comes from differentiating

$$
A(\theta)=\log \int h(x)\exp\left(\theta^{\top}\phi(x)\right)\,dx
$$


which yields a ratio of two integrals:

$$\frac{\partial A(\theta)}{\partial \theta_j}
=
\frac{\int h(x)\phi_j(x)\exp\left(\theta^{\top}\phi(x)\right)\,dx}{\int h(x)\exp\left(\theta^{\top}\phi(x)\right)\,dx}.$$

That ratio is exactly the expectation of $\phi_j(X)$ under the model indexed by $\theta$. Differentiating once more gives the covariance formula, so in matrix form

$$
\nabla^2 A(\theta)=\mathrm{Cov}_\theta(\phi(X)).
$$


Now the key convexity fact becomes transparent. For every vector $v$,

$$
v^T \nabla^2 A(\theta) v = v^T \mathrm{Cov}_\theta(\phi(X)) v = \mathrm{Var}_\theta(v^T\phi(X)) \ge 0.
$$


Variance is never negative, so the Hessian is positive semidefinite. Therefore $A(\theta)$ is convex. Once the constant and linear terms are separated out, the negative log-likelihood inherits that convexity.

<p align="center">
  <img src="../notes/02_probability_reconstructed/assets/figure_2_23_convexity_sketch.png" alt="Convexity sketch" width="860">
</p>

The blue secant line lies above the black graph, which is the geometric definition of convexity. The red tangent line lies below the graph, which is the first-order equivalent statement. These are not separate ideas; they are two views of the same structural property.

For exponential families, the most concrete beginner-to-expert takeaway is that optimization is well behaved in natural-parameter space because the curvature comes from a covariance matrix. Covariances cannot be negative in the matrix sense, so the Hessian cannot create spurious local minima. That does not mean every numerical optimization problem is easy, but it does mean the objective has a clean global geometry rather than an arbitrary nonconvex landscape.

### Retain from 2.4

- Convexity is the structural reason some estimation problems avoid bad local minima.
- First-order and second-order convexity tests are equivalent viewpoints on the same property.
- In exponential families, covariance structure is what drives the positive-semidefinite Hessian.
- This is the optimization-side explanation for why some of the estimation formulas from `2.3` behave so cleanly.

### Do Not Confuse in 2.4

- Do not confuse convexity of a function with convexity of a set.
- Do not assume every likelihood problem is convex just because some exponential-family examples are.
- Do not read positive semidefinite Hessian as meaning "strictly" convex; flat directions can remain.

## 2.5 Information Theory

This section is worth reading for conceptual maturity, but it is partly second-pass material if your immediate goal is to stay on top of the course core. The required ideas are what entropy, KL divergence, and mutual information mean and how they differ from one another.

The bridge from the earlier sections is this: probability tables and densities tell us how mass is distributed, while information theory gives numerical language for how uncertain that distribution is and how informative one variable is about another. So the chapter now moves from "what is the probability?" to "how much uncertainty is present?" and "how much does observation reduce that uncertainty?"

Entropy measures uncertainty, but the cleanest way to understand it is as an **average surprise**. For one specific outcome $x$, the surprise is

$$
-\log p(x).
$$


Rare outcomes have larger surprise because $p(x)$ is small. Entropy averages that surprise over all possible outcomes, weighted by how often those outcomes actually occur:

$$
H[X] = -\sum_x p(x)\log p(x).
$$


If the logarithm is base $2$, entropy is measured in bits. If the natural logarithm is used, entropy is measured in nats. The choice of base changes only the unit, not the underlying concept.

A deterministic variable has entropy zero, because there is no uncertainty to average over. At the other extreme, a uniform distribution on a fixed finite support has the largest entropy, because it spreads probability as evenly as possible and therefore makes each observation comparatively hard to predict. Entropy is therefore not just "randomness" in an informal sense; it is the expected code length of the optimal lossless code and the expected information revealed by one observation.

A concrete comparison is between a fair coin and a biased coin with probabilities $(0.9,0.1)$. The fair coin has entropy $1$ bit, while the biased coin has

$$
H[X] = -0.9\log_2 0.9 - 0.1\log_2 0.1 \approx 0.47 \text{ bits}.
$$


The biased coin is more predictable, so it carries less uncertainty and requires fewer average bits to encode. That is the operational content of entropy: predictable sources are cheaper to describe on average.

### Example 2-24: Entropy

Start with the simplest nontrivial case: a fair coin. The two outcomes are equally likely, so each carries one bit of surprise:

$$
H[X] = -0.5\log_2 0.5 - 0.5\log_2 0.5 = 1 \text{ bit}.
$$


This can be unpacked one step further. Because

$$
\log_2 0.5 = -1,
$$


each term is

$$
-0.5(-1)=0.5,
$$


and the two equal contributions add to

$$
0.5+0.5=1.
$$


So one fair coin flip carries one bit of uncertainty. In coding language, it takes one yes/no choice to specify the outcome.

Now compare that with a fair die:

$$
H[X] = -6 \cdot \frac{1}{6}\log_2 \frac{1}{6} \approx 2.58 \text{ bits}.
$$


The die formula is worth unpacking. A fair die has six equally likely outcomes, each with probability $1/6$. So the entropy sum contains six identical terms:

$$H[X]=-\sum_{x=1}^6 \frac{1}{6}\log_2\frac{1}{6}
=-6\cdot \frac{1}{6}\log_2\frac{1}{6}
=-\log_2\frac{1}{6}
=\log_2 6.$$

That is why the answer is about $2.58$ bits. The die has larger entropy than the coin because it has more equally plausible outcomes and therefore more uncertainty before observation.

The important comparison is not merely "six is bigger than two." The deeper point is that entropy grows when the outcome remains hard to predict. A fair die spreads its probability mass across six equally plausible states, so observing the result resolves more uncertainty than observing one fair coin flip.

### Example 2-25: Lottery

Entropy also explains compression. If a yearly sequence is mostly zeros, we can encode it with far fewer bits than a naive one-bit-per-day representation, because the sequence is highly non-random.

To make that explicit, imagine a lottery-notification variable that is $1$ only on a winning day and $0$ otherwise. If the event occurs once in a thousand days, then almost every symbol is zero. A code that assigns a very short description to $0$ and a longer one to $1$ achieves far better compression than a fixed one-bit code, precisely because the entropy is low.

The underlying Bernoulli parameter here is approximately

$$
p(X=1)=0.001,\qquad p(X=0)=0.999.
$$


So the entropy is

$$
H[X] = -0.999\log_2 0.999 - 0.001\log_2 0.001 \approx 0.011 \text{ bits}.
$$


It helps to understand why this number is so small. The outcome $X=0$ is almost certain, so seeing another zero reveals almost no new information. The rare event $X=1$ is very surprising when it happens, but it happens so infrequently that its contribution to the average remains small.

So the average uncertainty per symbol is only about

$$
0.011
$$


bits, far below the one-bit cost of a naive fixed code. This does not mean any single day can literally be encoded in $0.011$ bits. It means that over long sequences, the average cost per day can approach that number when the code is designed well.

That is the real compression lesson. A source with highly unequal probabilities carries very little uncertainty per symbol, and entropy measures exactly how little.

### Kullback-Leibler Divergence

Entropy measured uncertainty inside one distribution. KL divergence measures mismatch between two distributions.

For discrete variables,

$$
D(p \,\|\, q)=\sum_x p(x)\log\left(\frac{p(x)}{q(x)}\right).
$$


Read the ingredients in order.

- $p$ is the reference distribution, often interpreted as the true or target distribution.
- $q$ is the approximating distribution.
- The ratio $p(x)/q(x)$ compares how the two distributions score the same outcome.
- The weighting by $p(x)$ means the average is taken over outcomes that actually matter under $p$.

So KL divergence asks: if the world behaves like $p$, how costly is it to use $q$ in its place?

The logarithmic ratio

$$
\log\left(\frac{p(x)}{q(x)}\right)
$$


is positive when $q(x)$ is too small relative to $p(x)$, and negative when $q(x)$ is too large. After averaging under $p$, the total discrepancy is always nonnegative:

$$
D(p \,\|\, q)\ge 0,
$$


with equality only when

$$
p=q.
$$


But KL divergence is not symmetric. In general,

$$
D(p \,\|\, q)\ne D(q \,\|\, p).
$$


There is also an essential support condition. If some outcome satisfies

$$
p(x)>0 \qquad \text{and} \qquad q(x)=0,
$$


then

$$
D(p \,\|\, q)=\infty.
$$


That is because $q$ is declaring an actually possible event to be impossible.

One subtle point is easy to miss. The individual summands

$$
p(x)\log\left(\frac{p(x)}{q(x)}\right)
$$


need not all be positive. KL divergence is not nonnegative term by term. It is nonnegative only after the weighted average is taken.

A two-state example makes this visible. Let

$$
p=(0.8,0.2), \qquad q=(0.5,0.5).
$$


Then

$$
D(p \,\|\, q)=0.8\log\left(\frac{0.8}{0.5}\right)+0.2\log\left(\frac{0.2}{0.5}\right).
$$


Compute the two contributions separately:

$$
0.8\log\left(\frac{0.8}{0.5}\right)=0.8\log(1.6)\approx 0.376,
$$


$$
0.2\log\left(\frac{0.2}{0.5}\right)=0.2\log(0.4)\approx -0.183.
$$


Adding them gives

$$
D(p \,\|\, q)\approx 0.376-0.183=0.193.
$$


Reverse the order and the answer changes:

$$
D(q \,\|\, p)=0.5\log\left(\frac{0.5}{0.8}\right)+0.5\log\left(\frac{0.5}{0.2}\right)\approx 0.223.
$$


So KL divergence is a directed discrepancy, not an ordinary symmetric distance. The first argument tells you which outcomes are being treated as important, because the expectation is taken with respect to that distribution.

### Mutual Information

Mutual information asks a more specific question than "are these variables related?"

It asks: how much does observing one variable reduce uncertainty about the other?

Its structural definition is

$$
I[X,Y]=D(p(x,y)\,\|\,p(x)p(y)).
$$


The product

$$
p(x)p(y)
$$


is the joint distribution we would have if $X$ and $Y$ were independent. So mutual information is the KL penalty for pretending the true joint distribution factorizes when it actually does not.

If $X$ and $Y$ are independent, then

$$
p(x,y)=p(x)p(y),
$$


so

$$
I[X,Y]=0.
$$


Write the definition out in full:

$$
I[X,Y]=\sum_{x,y} p(x,y)\log\left(\frac{p(x,y)}{p(x)p(y)}\right).
$$


Now derive the entropy identity carefully. Split the logarithm:

$$
I[X,Y]=\sum_{x,y} p(x,y)\log p(x,y)-\sum_{x,y} p(x,y)\log p(x)-\sum_{x,y} p(x,y)\log p(y).
$$


For the second sum, use

$$
\sum_y p(x,y)=p(x),
$$


to obtain

$$
\sum_{x,y} p(x,y)\log p(x)=\sum_x p(x)\log p(x).
$$


Similarly,

$$
\sum_{x,y} p(x,y)\log p(y)=\sum_y p(y)\log p(y).
$$


Substituting back gives

$$
I[X,Y]=-H[X,Y]+H[X]+H[Y].
$$


So

$$
I[X,Y]=H[X]+H[Y]-H[X,Y].
$$


Because

$$
H[X \mid Y]=H[X,Y]-H[Y],
$$


we also obtain

$$
I[X,Y]=H[X]-H[X \mid Y].
$$


This second identity is often the clearest operational reading. It says mutual information is the amount of uncertainty in $X$ that disappears, on average, after the value of $Y$ is revealed.

Two extreme cases fix the interpretation.

- If $X$ and $Y$ are independent, then observing $Y$ tells us nothing about $X$, so $I[X,Y]=0$.
- If $Y=X$ exactly, then observing $Y$ reveals $X$ completely, so $H[X \mid Y]=0$ and therefore $I[X,Y]=H[X]$.

So mutual information is not merely a generic dependence score. It measures a specific quantity: the average reduction in uncertainty caused by observation.

### Conditional Entropy

Conditional entropy measures the uncertainty left in one variable after another variable is revealed.

It can be written as

$$
H[X \mid Y]=H[X,Y]-H[Y],
$$


or, more explicitly,

$$
H[X \mid Y]=\sum_y p(y)H[X \mid Y=y].
$$


The second form is the most direct interpretation formula. It says:

1. For each possible value $y$, compute the entropy of the conditional distribution of $X$ given $Y=y$.
2. Average those entropies using the probabilities $p(y)$.

So conditional entropy is not "the uncertainty after one particular observed value." It is the average remaining uncertainty over all possible revealed values of $Y$.

That average matters. For one unusual value of $Y$, uncertainty about $X$ can even increase compared with the unconditional case. The theorem is only that uncertainty cannot increase on average:

$$
H[X \mid Y]\le H[X].
$$


Equivalently,

$$
I[X,Y]=H[X]-H[X \mid Y]\ge 0.
$$


So the correct reading is:

- $H[X]$ is uncertainty before seeing $Y$;
- $H[X \mid Y]$ is average uncertainty after seeing $Y$;
- the difference is the information supplied by $Y$.

### Example 2-26: Information and Conditional Entropy

Suppose we model commuting behavior $C \in \{\text{walk}, \text{bike}, \text{drive}\}$ and weather $R \in \{\text{clear}, \text{rain}\}$. On rainy days we drive more often, so weather conveys information about commute choice.

<table align="center">
  <thead>
    <tr><th>$R$</th><th>$C$</th><th>$p(C \mid R)$</th></tr>
  </thead>
  <tbody>
    <tr><td>clear</td><td>walk</td><td>$0.9$</td></tr>
    <tr><td>clear</td><td>bike</td><td>$0.1$</td></tr>
    <tr><td>clear</td><td>drive</td><td>$0.0$</td></tr>
    <tr><td>rain</td><td>walk</td><td>$0.5$</td></tr>
    <tr><td>rain</td><td>bike</td><td>$0.0$</td></tr>
    <tr><td>rain</td><td>drive</td><td>$0.5$</td></tr>
  </tbody>
</table>

The conditional table is not yet the full joint distribution. To get the joint distribution, multiply each conditional probability by the corresponding weather probability.

Assume

$$
p(R=\text{clear})=0.9, \qquad p(R=\text{rain})=0.1.
$$


Then

<table align="center">
  <thead>
    <tr><th>$R$</th><th>$C$</th><th>$p(R,C)$</th></tr>
  </thead>
  <tbody>
    <tr><td>clear</td><td>walk</td><td>$0.9 \cdot 0.9 = 0.81$</td></tr>
    <tr><td>clear</td><td>bike</td><td>$0.9 \cdot 0.1 = 0.09$</td></tr>
    <tr><td>clear</td><td>drive</td><td>$0.9 \cdot 0 = 0$</td></tr>
    <tr><td>rain</td><td>walk</td><td>$0.1 \cdot 0.5 = 0.05$</td></tr>
    <tr><td>rain</td><td>bike</td><td>$0.1 \cdot 0 = 0$</td></tr>
    <tr><td>rain</td><td>drive</td><td>$0.1 \cdot 0.5 = 0.05$</td></tr>
  </tbody>
</table>

With $p(R=\text{rain}) = 0.1$, the marginals are

$$
p(C=\text{walk}) = 0.86, \quad p(C=\text{bike}) = 0.09, \quad p(C=\text{drive}) = 0.05.
$$


These marginals come from the law of total probability. For example,

$$
p(C=\text{walk}) = p(C=\text{walk}\mid R=\text{clear})p(R=\text{clear}) + p(C=\text{walk}\mid R=\text{rain})p(R=\text{rain})
$$


$$
=0.9\cdot 0.9 + 0.5\cdot 0.1 = 0.81 + 0.05 = 0.86.
$$


The other commute marginals are obtained the same way:

$$
p(C=\text{bike}) = 0.1\cdot 0.9 + 0\cdot 0.1 = 0.09,
$$


$$
p(C=\text{drive}) = 0\cdot 0.9 + 0.5\cdot 0.1 = 0.05.
$$


Now compute the unconditional entropy of the commute explicitly:

$$
H[C] = -0.86\log_2 0.86 - 0.09\log_2 0.09 - 0.05\log_2 0.05 \approx 0.72 \text{ bits}.
$$


So before observing the weather, the commute carries about $0.72$ bits of uncertainty.

Now compute the entropy after the weather is revealed.

$$
H[C \mid R=\text{clear}] = -0.9\log_2 0.9 - 0.1\log_2 0.1 \approx 0.47,
$$


because the zero-probability drive term contributes nothing.

$$
H[C \mid R=\text{rain}] = -0.5\log_2 0.5 - 0.5\log_2 0.5 = 1.
$$


Average these conditional entropies using the weather probabilities:

$$
H[C \mid R] = 0.9 \cdot 0.47 + 0.1 \cdot 1 \approx 0.52.
$$


The unconditional commute entropy is larger, so the difference between them is exactly the information weather provides:

$$
I[C,R] = H[C]-H[C \mid R] \approx 0.72 - 0.52 = 0.20 \text{ bits}.
$$


That number is not huge, and that interpretation matters. Weather is informative about commuting, but it does not determine commuting completely. Most days are clear, and even on clear days there is still some uncertainty between walking and biking. So this is an example of partial information, not perfect prediction.

### Retain from 2.5

- Entropy measures uncertainty, KL divergence measures directed discrepancy, and mutual information measures departure from independence.
- Mutual information can be read either as a KL divergence or as reduction in uncertainty after observation.
- Conditional entropy is an average over the conditioning variable, not a single conditional calculation at one value.
- These are expectation-style quantities, so the averaging intuition from `2.1` still applies even though the thing being averaged is now a logarithmic information term.

### Do Not Confuse in 2.5

- Do not confuse entropy with variance or spread; it is a distributional uncertainty measure, not a geometric one.
- Do not confuse KL divergence with a symmetric distance.
- Do not forget the support condition in KL; assigning zero probability where the data distribution has mass makes the divergence infinite.

## 2.6 Change-of-Variable Models

The classical probability distributions above are important, but many real data sets do not fit those forms directly. A common technique is to define a new variable as an invertible transformation of a simpler base variable.

The modeling motive is the following. Simple base distributions, such as Gaussians, are mathematically convenient but often too rigid to fit real data directly. Change-of-variables methods let us start from a simple distribution we understand well and then warp it into a more realistic one. The price of that warping is the Jacobian correction, meaning the derivative-based factor that compensates for how the transformation stretches or compresses space.

For the course core, the main required idea is the Jacobian correction in scalar and multivariate change of variables. The copula subsections and normalizing-flow subsections are explicit reach material: copulas separate marginal shape from dependence structure, while normalizing flows learn invertible transformations of a simple base density. Both are modern extensions of the same change-of-variables principle.

### Scalar Change of Variables

If $X = f(Z)$ is invertible and $g = f^{-1}$, then

$$
p_X(x) = p_Z(g(x)) \lvert g'(x) \rvert.
$$


This formula is a density version of probability conservation. The transformed variable cannot create or destroy probability mass. It can only move that mass around and locally stretch or compress the axis.

There are two derivations worth knowing.

First derivation: the exact CDF argument for a monotone increasing map. If $f$ is increasing, then

$$
F_X(x)=\mathbb{P}(X \le x)=\mathbb{P}(f(Z)\le x)=\mathbb{P}(Z \le g(x))=F_Z(g(x)).
$$


Differentiate both sides with respect to $x$:

$$
p_X(x)=\frac{d}{dx}F_Z(g(x))=p_Z(g(x))g'(x).
$$


If $f$ is decreasing, the same logic introduces a minus sign, and taking absolute values combines the two cases into the single formula

$$
p_X(x)=p_Z(g(x))|g'(x)|.
$$


Second derivation: the local-interval intuition. A tiny interval around $x$ corresponds to a tiny interval around $z=g(x)$. If the transformation stretches widths by a factor of $2$, then the density height must drop by a factor of $2$ so that probability mass is preserved. That is why the derivative appears.

This formula requires invertibility on the region of interest. If the map has multiple inverse branches, the correct density is a sum over branches rather than a single Jacobian term. The absolute value is not optional either. If the inverse map decreases rather than increases, the raw derivative is negative, but a density must remain nonnegative, so the local scaling factor must be taken in magnitude.

So the mental model should be: move probability mass with the transformation, then compensate for local stretching or compression. That is the whole purpose of the derivative term.

A minimal worked example is $X=2Z$ with $Z$ uniform on $[0,1]$. Then $g(x)=x/2$ and $g'(x)=1/2$, so

$$
p_X(x)=p_Z(x/2)\cdot \frac{1}{2}.
$$


Now state the support condition explicitly. The argument $x/2$ must lie in the support of $Z$, namely $[0,1]$. So

$$
0 \le x/2 \le 1 \qquad \Longleftrightarrow \qquad 0 \le x \le 2.
$$


Since $p_Z(z)=1$ on $[0,1]$, we get

$$
p_X(x)=\frac{1}{2}
$$


on $[0,2]$ and zero elsewhere. Stretching the variable by a factor of $2$ cuts the density height by a factor of $2$. For example,

$$
\mathbb{P}(0.4 \le X \le 1.0)=\int_{0.4}^{1.0}\frac{1}{2}\,dx=0.3,
$$


which matches the equivalent $Z$-space calculation

$$
\mathbb{P}(0.2 \le Z \le 0.5)=0.3.
$$


One more tiny example explains why the absolute value is necessary. Let

$$
X=1-Z
$$


with the same base distribution

$$
Z \sim \mathrm{Unif}[0,1].
$$


Then

$$
g(x)=1-x, \qquad g'(x)=-1.
$$


So

$$
p_X(x)=p_Z(1-x)\lvert -1 \rvert = p_Z(1-x).
$$


Because $1-x \in [0,1]$ exactly when $x \in [0,1]$, the transformed density is still uniform on $[0,1]$. The derivative is negative, but the density does not become negative. That is exactly why the absolute value is required.

### Example: Lognormal Distribution

If $Z = \log X$ is Gaussian, then $X$ is lognormal. This example matters because it shows explicitly how exponentiating a variable that is symmetric on the log scale produces a variable that is asymmetric on the original scale.

Start with

$$
Z \sim \mathcal{N}(\mu,\sigma^2).
$$


Define

$$
X=e^Z.
$$


Because the exponential is always positive, the support of $X$ is

$$
x>0.
$$


The inverse transformation is

$$
z=\log x,
$$


and its derivative is

$$
\frac{dz}{dx}=\frac{1}{x}.
$$


So the change-of-variables formula gives the full lognormal density

$$
p_X(x)=\frac{1}{x \sqrt{2\pi\sigma^2}} \exp\left(-\frac{(\log x-\mu)^2}{2\sigma^2}\right), \qquad x>0.
$$


The extra factor

$$
\frac{1}{x}
$$


is exactly the Jacobian term. Without it, the transformed density would no longer integrate to one.

The asymmetry is worth explaining carefully. Equal distances on the $Z$ scale correspond to multiplicative, not additive, changes on the $X$ scale:

- moving from $Z=0$ to $Z=1$ means moving from $X=1$ to $X=e$;
- moving from $Z=1$ to $Z=2$ means moving from $X=e$ to $X=e^2$.

So the right side of the $X$ axis gets stretched more and more strongly. That stretching is what creates the long right tail of the lognormal density.

A concrete probability statement helps fix the translation rule. If

$$
Z \sim \mathcal{N}(0,1),
$$


then

$$
\mathbb{P}(1 \le X \le e)=\mathbb{P}(0 \le Z \le 1).
$$


So lognormal probabilities are often easiest to reason about by taking logarithms and reducing the question back to an ordinary Gaussian calculation.

### Multivariate Change of Variables

In multiple dimensions,

$$
p_X(x) = p_Z(g(x)) \lvert \det J_g(x) \rvert,
$$


where $J_g$ is the Jacobian matrix of the inverse transformation. Its $(i,j)$ entry is

$$
\bigl(J_g(x)\bigr)_{ij}=\frac{\partial g_i}{\partial x_j}.
$$


The determinant plays the same role as $|g'(x)|$ in one dimension: it is the local volume scaling factor. If the transformation doubles area near one point, the density there must be cut in half to preserve total probability. If the determinant is zero somewhere, the map locally collapses volume and is not invertible there, so the simple formula breaks down.

An explicit two-dimensional example is

$$
X_1=2Z_1, \qquad X_2=3Z_2.
$$


The inverse map is

$$
Z_1=\frac{X_1}{2},\qquad Z_2=\frac{X_2}{3},
$$


so the inverse Jacobian matrix has entries

$$
\bigl(J_g(x)\bigr)_{11}=1/2, \qquad \bigl(J_g(x)\bigr)_{12}=0, \qquad \bigl(J_g(x)\bigr)_{21}=0, \qquad \bigl(J_g(x)\bigr)_{22}=1/3.
$$


Its determinant is

$$
\det J_g(x)=\frac{1}{6}.
$$


So every small area element is expanded by a factor of $6$ in data space, and the density must shrink by the same factor. For example, a unit square in latent space becomes a rectangle of area $6$ in data space. Probability mass is preserved, so density height must be divided by $6$.

The absolute value is still essential in multiple dimensions. A negative determinant means the map reverses orientation locally, not that probability becomes negative. Density only cares about the magnitude of the local volume change.

### Copula Models

Copulas separate marginal distributions from dependence structure. For two variables,

$$
\mathbb{P}(X_1 \le x_1, X_2 \le x_2) = C(F_1(x_1), F_2(x_2)),
$$


where $F_1$ and $F_2$ are the marginal CDFs. The key construction is to define

$$
U_1=F_1(X_1),\qquad U_2=F_2(X_2).
$$


When the marginals are continuous, each $U_i$ is uniformly distributed on $[0,1]$. This is the probability integral transform. The copula $C$ is therefore the joint CDF of these transformed uniform variables:

$$
C(u_1,u_2)=\mathbb{P}(U_1 \le u_1, U_2 \le u_2).
$$


This is the content of Sklar's theorem in the two-variable case: once the marginals are pushed onto a common uniform scale, the remaining object $C$ captures only dependence.

The conceptual reason this is valuable is that multivariate modeling actually mixes two different tasks:

- choosing the marginal shape of each coordinate;
- choosing the dependence pattern that couples the coordinates.

Copulas separate those tasks explicitly instead of forcing one model family to handle both at once.

A plain-language example helps. Suppose $X_1$ is height and $X_2$ is weight. They are measured in different units and have different one-dimensional shapes. A copula says:

- first convert height into a percentile;
- convert weight into a percentile;
- then model how those percentiles move together.

So the dependence model is built on rank-like information rather than on the original physical units.

<p align="center">
  <img src="../notes/02_probability_reconstructed/assets/figure_2_5_copula_transforms.png" alt="Copula transforms" width="860">
</p>

The Gaussian copula is a special case in which the transformed variables are then pushed from uniform scale into Gaussian scale using $\Phi^{-1}$. The visual sequence shows the separation explicitly: start with the original marginals, map each one to a uniform scale, then map those uniform variables to a Gaussian scale where the dependence is easy to model.

This gives a clean division of labor. The marginal CDFs control one-dimensional shape, skewness, and heavy tails. The copula controls only how coordinates move together after those marginal effects have been removed.

That separation is the main modeling advantage of copulas. They let us answer two different questions separately instead of forcing one model component to answer both at once: "what does each variable look like on its own?" and "how do the variables depend on one another?"

<p align="center">
  <img src="../notes/02_probability_reconstructed/assets/figure_2_copula_flow_pipeline.png" alt="Copula and flow transformation pipeline" width="860">
</p>

### Example 2-27: Copula Transforms

The chapter uses a KDD Cup data set to show the pipeline. The procedure is worth spelling out as four separate steps.

Step 1: estimate each marginal distribution separately. From the raw data, estimate $F_1$ for the first coordinate and $F_2$ for the second.

Step 2: remove the original units by mapping into percentile space:

$$
U_1=F_1(X_1),\qquad U_2=F_2(X_2).
$$


At this stage each coordinate is uniform on $[0,1]$. So an observation at the $80$th percentile becomes $0.8$ regardless of whether the original variable measured time, length, or counts.

Step 3: map the uniform variables into Gaussian marginals:

$$
Y_1=\Phi^{-1}(U_1),\qquad Y_2=\Phi^{-1}(U_2).
$$


Now the one-dimensional marginals are Gaussian by construction.

Step 4: fit a Gaussian dependence model to $(Y_1,Y_2)$. That dependence model is the Gaussian copula.

The resulting model can express complicated non-Gaussian marginals while keeping the dependence structure manageable.

The step-by-step reason this works is that CDF transforms preserve order. If an observation is at the $80$th percentile of its own marginal distribution, its transformed value is $0.8$ regardless of the original physical units. After both coordinates are mapped into percentile space, the dependence structure can be modeled in a unit-free way.

Make one observation explicit. Suppose a data point lands at the $80$th percentile of the first marginal and the $25$th percentile of the second. Then

$$
U_1=0.8, \qquad U_2=0.25.
$$


After the Gaussian transform,

$$
Y_1=\Phi^{-1}(0.8)\approx 0.84, \qquad Y_2=\Phi^{-1}(0.25)\approx -0.67.
$$


So the original units are gone, but the relative standing inside each marginal distribution is preserved.

So the copula trick is fundamentally a change-of-coordinates trick: strip away marginal units and shapes first, then model only the remaining dependence.

### Normalizing Flows

Normalizing flows start with a simple base variable

$$
Z \sim p_Z,
$$


often Gaussian, and then define the observed variable by an invertible map

$$
X=f(Z).
$$


The density of $X$ is computed by the change-of-variables formula. The practical idea is simple: sampling and density evaluation are easy in the base space, while the learned transformation bends that simple density into a more realistic one in data space.

The transformation is often built as a composition of simple steps:

$$
f(Z) = f_T(f_{T-1}(\cdots f_1(Z)))
$$


with

$$
\log p_X(X) = \log p_Z(f^{-1}(X)) - \sum_t \log |\det J_{f_t}|.
$$


There are two points to make explicit here.

First, the map is a composition:

$$
f = f_T \circ \cdots \circ f_1.
$$


So the inverse is

$$
f^{-1}=f_1^{-1}\circ \cdots \circ f_T^{-1}.
$$


Second, Jacobian determinants multiply under composition. Therefore the log-determinants add. That is the whole computational reason flows are practical: a complicated global transformation can be assembled from simple local pieces whose determinants are easy to evaluate.

A flow is therefore practical only when each layer is invertible and has a determinant that can be evaluated cheaply. If either condition fails, likelihood evaluation becomes intractable or ill-defined.

The modeling motivation is parallel to the copula idea but more flexible. Instead of choosing one fixed transformation by hand, a flow learns a sequence of simple invertible maps whose composition can bend a simple base density into a complicated observed density.

This is the long-term modeling idea behind flows. Start with a base density that is easy to sample from and evaluate, such as a Gaussian. Then learn an invertible map that bends that simple density into a complex one that matches the data. The density becomes complicated in data space, but it stays tractable because the transformation remains invertible and the Jacobian terms are computable.

A one-layer sanity check is the scaling flow

$$
X = aZ + b
$$


with $a \neq 0$. Then the inverse is $(X-b)/a$ and

$$
\log p_X(X)=\log p_Z\left(\frac{X-b}{a}\right)-\log |a|.
$$


That tiny example already contains the entire logic of a flow:

- invert the transformation to locate the corresponding latent point;
- evaluate the simple base density there;
- subtract the log-volume expansion.

Normalizing flows repeat this same accounting rule layer after layer. Each layer contributes one inverse transformation step and one Jacobian term, and composing many such layers produces a flexible global density while preserving exact likelihood evaluation.

So a flow should be read as repeated change-of-variables bookkeeping, not as a fundamentally different probability law.

### Example 2-28: Copula-Like Normalizing Flow

One common construction is to start with a Gaussian base distribution and parameterize one-dimensional monotone transforms for each feature. This plays the same role as explicit marginal CDF transforms, but the transforms are learned from data rather than written down analytically. The monotonicity constraint is not optional: without it, the map would stop being invertible and the change-of-variables formula would no longer have a single valid inverse branch.

At the beginner level, this means "bend each axis without folding it over itself." At the expert level, it means each scalar transform must remain strictly monotone so that the inverse exists and the Jacobian diagonal stays nonzero everywhere.

Why is this copula-like? Because each coordinate gets its own monotone warp, which is playing the same role that a marginal CDF transform would play in an explicit copula pipeline. The difference is that here the warp is learned rather than supplied analytically.

Why does folding break the model? Because once two different latent values are mapped to the same observed value, the inverse is no longer unique. Then the one-branch flow formula is invalid and one must sum over inverse branches, exactly as in the noninvertible scalar case.

So the design rule is strict: flexibility is allowed, but only in ways that preserve a single well-defined inverse.

### Example 2-29: Conditional Affine Normalizing Flows

A particularly convenient flow layer is conditional affine:

$$
Z_1' = Z_1, \qquad Z_2' = \alpha_1(Z_1)Z_2 + \beta_1(Z_1).
$$


The structure of this layer should be read literally. The first coordinate is copied unchanged, while the second coordinate is shifted and rescaled using functions of the first coordinate. This makes the layer expressive but still easy to invert.

Why keep one coordinate unchanged? Because that design makes the Jacobian triangular. A triangular Jacobian has a determinant equal to the product of its diagonal entries, which is why this layer stays computationally cheap even though it couples the coordinates.

Indeed, if $\alpha_1(Z_1)\neq 0$, then the inverse is

$$
Z_1 = Z_1', \qquad Z_2 = \frac{Z_2' - \beta_1(Z_1')}{\alpha_1(Z_1')}.
$$


So invertibility requires the scale factor never to cross zero.

Because the Jacobian is triangular, the determinant is easy to compute: for the first layer the diagonal entries are $1$ and $\alpha_1(Z_1)$, so the determinant is their product,

$$
\det J = 1 \cdot \alpha_1(Z_1)=\alpha_1(Z_1),
$$


and therefore the log-determinant is $\log |\alpha_1(Z_1)|$. A second layer can then swap roles and transform the other coordinate:

$$
Z_1'' = \alpha_2(Z_2')Z_1' + \beta_2(Z_2'), \qquad Z_2'' = Z_2'.
$$


<p align="center">
  <img src="../notes/02_probability_reconstructed/assets/figure_2_6_affine_flow_panels.png" alt="Normalizing flow deformation panels" width="860">
</p>

The deformation panels show what the algebra means geometrically. A rectangular grid in latent space is progressively bent and stretched into a curved mesh in data space. The main idea is that a sequence of simple invertible layers can produce a complex density while keeping likelihood evaluation tractable. The structural limit is equally important: each layer must preserve invertibility, and in practice the scale functions are parameterized so they never cross zero.

A full worked determinant calculation makes the affine layer concrete. For

$$
Z_1' = Z_1, \qquad Z_2' = \alpha_1(Z_1)Z_2 + \beta_1(Z_1),
$$


the forward Jacobian matrix is

$$
J_{11}=1,\qquad J_{12}=0,\qquad J_{21}=\frac{\partial Z_2'}{\partial Z_1},\qquad J_{22}=\alpha_1(Z_1),
$$


so

$$
\det J = \alpha_1(Z_1).
$$


The lower-left derivative can be complicated:

$$
\frac{\partial Z_2'}{\partial Z_1}=\alpha_1'(Z_1)Z_2+\beta_1'(Z_1),
$$


but the determinant ignores it because the matrix is triangular. That is the key design principle: choose transformations that are expressive enough to bend the density, yet structured enough that the determinant remains cheap to evaluate exactly.

A tiny numerical snapshot makes the layer concrete. Suppose at one particular input we have

$$
Z_1=1, \qquad Z_2=3, \qquad \alpha_1(Z_1)=2, \qquad \beta_1(Z_1)=-1.
$$


Then

$$
Z_1'=1, \qquad Z_2'=2 \cdot 3 - 1 = 5.
$$


To invert, use the same $Z_1'=1$ and solve

$$
Z_2=\frac{Z_2'-\beta_1(Z_1')}{\alpha_1(Z_1')}=\frac{5-(-1)}{2}=3.
$$


The determinant at that point is

$$
\det J = 2,
$$


so local area is doubled there and the log-density must decrease by

$$
\log 2.
$$


That is the core philosophy of coupling layers: let one part of the vector control how another part is stretched, but do it in a way that keeps inversion and determinant evaluation simple.

### Retain from 2.6

- Change of variables is probability conservation plus a local stretching factor.
- Invertibility is the structural condition that makes the simple Jacobian formula valid.
- Copulas separate marginals from dependence, while flows compose simple invertible maps into flexible densities.
- This is the continuous-transform analogue of the normalization logic used much earlier in the table and density sections.

### Do Not Confuse in 2.6

- Do not forget the absolute value on the Jacobian determinant.
- Do not use the one-branch formula when the transformation has multiple inverse branches; then contributions must be summed.
- Do not treat copulas or normalizing flows as core required course material unless your instructor says so; they are here as enrichment built from the same change-of-variables principle.

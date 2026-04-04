# Probability and Inference (Part 1.1)

Source: ../notes/02_probability_reconstructed/source/02_probability.pdf

This is Part 1.1 of the Chapter 2 main note split. It covers the front matter and Section 2.1. Continue with [Part 1.2](../02_probability_main_part_1_2/) for Section 2.2.

This is a full note-style reconstruction of Chapter 2. It keeps the chapter's section structure, worked examples, key tables, and core derivations, while normalizing some prose and keeping the main visuals in the chapter assets directory under ../notes/02_probability_reconstructed/assets/.

## How to Use This Chapter

This main note is the readable core of the chapter. Read it first if you want definitions, intuition, worked examples, and the minimum formal structure needed to use the material correctly without turning the chapter into a proof-only reference.

- [Formal supplement](../02_probability_formal_supplement/): use this if you want theorem-style statements, tighter derivations, and the parts of the logical scaffolding that would otherwise slow down the narrative.
- [Exercises](../02_probability_exercises/): use this if you want direct computation drills, conceptual checks, and proof-style practice after reading the main note.
- [Computational appendix](../02_probability_computational_appendix/): use this if you want sampling, plotting, histogram workflows, and numerical sanity checks that support the theory.

## Scope Guide

Use this table as a reading filter. "Required" means material a student should be comfortable using for the course's core probability work. "Reach" means enrichment: useful, interesting, and connected to the course, but not first-pass material if the goal is simply to stay on pace.

| Area | Required for the course | Reach / enrichment |
|---|---|---|
| `2.1` events, Bayes, table operations, expectation, independence | all of it | the measure-theoretic framing is useful rigor, but not first-pass exam material |
| Geometric distribution | yes | none; this is directly homework-relevant |
| `2.2` continuous variables, CDF/PDF distinction, Gaussian, Beta/Dirichlet basics | yes | exponential-family parameterization details and two-parameter Bernoulli redundancy |
| `2.3` likelihood, maximum likelihood estimation (MLE), Beta-Bernoulli updates, basic model selection | yes | hyper-priors, weakly informative priors, and some of the broader Bayesian-model-selection discussion |
| `2.4` convexity | supporting background only | full optimization interpretation and Hessian viewpoint |
| `2.5` entropy, KL, mutual information | conceptually useful and worth reading | derivation-heavy identities beyond the main examples |
| `2.6` scalar and multivariate Jacobians | useful background | copulas and normalizing flows are the clearest "beyond the course core" topics in this chapter |

If time is short, read `2.1`, the Geometric section, the core parts of `2.2`, and the likelihood / maximum likelihood estimation (MLE) / conjugate-prior / Bayesian information criterion (BIC) parts of `2.3` first. Then return to `2.4`-`2.6` as second-pass material.

## Notation Policy

Throughout the note, $\mathbb{P}(A)$ denotes the probability of an event $A$, while $p(x)$ denotes a PMF or PDF value when such an object exists. Random variables are written with uppercase letters, realized values with lowercase letters, $F_X(x)$ denotes a CDF, and $\Omega$ denotes the sample space. When a formula is valid only in a discrete setting, only for densities, only for invertible maps, or only away from a boundary case, that restriction is stated explicitly rather than left implicit.

## 2.1 Probability, Events, Random Variables

Probability is the language we use when a system is uncertain or too complex to model exactly. In AI, the uncertainty often comes less from true randomness than from missing information and limited modeling power. A useful probabilistic model does two things: it describes our assumptions about the world, and it gives rules for combining evidence and updating those assumptions when observations arrive.

### Formal Foundations

At a more formal level, a probabilistic model starts with a probability space

$$
(\Omega,\mathcal{F},P).
$$


Here $\Omega$ is the sample space of possible outcomes, $\mathcal{F}$ is the collection of events on which probabilities are defined, and $P$ is the probability measure. The measure assigns a number to each event and satisfies nonnegativity, normalization, and countable additivity.

In elementary finite examples, one usually suppresses $\mathcal{F}$ because every subset of $\Omega$ can be treated as an event. In that case the abstract measure language reduces to ordinary bookkeeping over subsets. But the more formal notation matters because later concepts such as densities, cumulative distribution functions, and random variables are induced from this underlying structure rather than being primitive objects in every setting.

A random variable is a measurable function

$$
X:\Omega \to \mathbb{R}.
$$


This explains an important notation point. A statement such as $X=x$ is not a mysterious new kind of object; it is shorthand for the event

$$
\{\omega \in \Omega : X(\omega)=x\}.
$$


Likewise, the statement $X \le t$ is shorthand for the event

$$
\{\omega \in \Omega : X(\omega)\le t\}.
$$


In words: it is the set of all worlds whose value under $X$ is at most $t$. For example, if $X$ is the outcome of a die roll and $t=3$, then the event $X \le 3$ is the subset of worlds $\{1,2,3\}$. The notation looks like an ordinary numerical inequality, but probabilistically it is still an event in the sample space. Probabilities are attached to events first; PMFs, PDFs, and CDFs are derived descriptions of how that event-level probability structure appears after the random variable has mapped worlds into numerical values.

### Probability Axioms and First Consequences

Now fix a probability space $(\Omega,\mathcal{F},P)$. The actual axioms are:

$$
0 \le \mathbb{P}(A)
$$


for every event $A \in \mathcal{F}$,

$$
\mathbb{P}(\Omega) = 1,
$$


and countable additivity:

$$
\mathbb{P}\left(\bigcup_{i=1}^{\infty} A_i\right) = \sum_{i=1}^{\infty} \mathbb{P}(A_i)
$$


whenever the events $A_1,A_2,\dots$ are pairwise disjoint.

Pairwise disjoint means that every pair of distinct events in the collection is disjoint. In other words, if you choose any two different indices $i$ and $j$, the corresponding events do not share any worlds. Formally,

$$
A_i \cap A_j = \varnothing \qquad \text{whenever } i \ne j.
$$


So countable additivity applies only when the events do not overlap. In that case there is no double counting, so the probability of the union is exactly the sum of the individual probabilities. The phrase pairwise disjoint is stronger than saying only that the whole collection has empty total intersection. It requires every two-event overlap to be empty, because any such overlap would otherwise be counted twice in the sum.

An inline finite example confirms the meaning. For a fair die, let

$$
A_1=\{1\},\qquad A_2=\{2\},\qquad A_3=\{3\}.
$$


These events are pairwise disjoint because no die outcome can be both $1$ and $2$, etc. Their union is the event "roll at most $3$":

$$
A_1 \cup A_2 \cup A_3 = \{1,2,3\}.
$$


So

$$
\mathbb{P}(A_1 \cup A_2 \cup A_3)=3/6=0.5,
$$


while the sum of individual probabilities is

$$
\mathbb{P}(A_1)+\mathbb{P}(A_2)+\mathbb{P}(A_3)=1/6+1/6+1/6=3/6=0.5.
$$


The equality holds because the three events do not overlap.

Several familiar rules are consequences of these axioms rather than additional axioms. For example,

$$
\mathbb{P}(\varnothing)=0
$$


follows because $\Omega$ and $\Omega \cup \varnothing$ are the same event, while finite additivity for disjoint sets is the finite case of countable additivity.

Inclusion-exclusion is also derived, not assumed. The clean way to derive it is to decompose the union into pieces that do not overlap. Write

$$
A \cup B = A \cup (B \setminus A),
$$


where the two pieces are disjoint. The reason is simple: every world in $A$ is, by definition, in $A$, while every world in $B \setminus A$ is in $B$ but explicitly not in $A$. So no world can belong to both pieces at once. Then

$$
\mathbb{P}(A \cup B) = \mathbb{P}(A) + \mathbb{P}(B \setminus A).
$$


But $B$ itself decomposes as the disjoint union

$$
B = (B \setminus A) \cup (A \cap B),
$$


because every world in $B$ falls into exactly one of two cases. Either it is not in $A$, in which case it lies in $B \setminus A$, or it is also in $A$, in which case it lies in $A \cap B$. These two cases cannot happen simultaneously, so they are disjoint. Therefore

$$
\mathbb{P}(B) = \mathbb{P}(B \setminus A) + \mathbb{P}(A \cap B).
$$


Now solve the second equation for $\mathbb{P}(B \setminus A)$ and substitute the result into the first equation. That removes the intermediate term and leaves the familiar correction formula

$$
\mathbb{P}(A \cup B) = \mathbb{P}(A) + \mathbb{P}(B) - \mathbb{P}(A \cap B).
$$


The logical status matters: normalization and additivity are the assumptions, while empty-set probability and inclusion-exclusion are useful consequences.

For a beginner, the safest way to use these axioms is to think in terms of bookkeeping over possible worlds. First list the worlds that belong to the event. Then check whether those worlds overlap with the worlds of another event. If they do, inclusion-exclusion is the correction term that prevents double counting. For a die roll, if $A=\{1,3,5\}$ and $B=\{4,5,6\}$, the union is not six outcomes but five, because the world $5$ sits in both sets.

### Example 2-1: Random Events

Suppose we roll a standard six-sided die. The event space is

$$
\Omega = \{1,2,3,4,5,6\}.
$$


Two events are:

$$
A = \{\text{odd roll}\} = \{1,3,5\}
$$


$$
B = \{\text{roll is 4 or greater}\} = \{4,5,6\}.
$$


Then $\mathbb{P}(A) = 3/6$, $\mathbb{P}(B) = 3/6$, and $\mathbb{P}(A \cap B) = 1/6$, so $\mathbb{P}(A \cup B) = 5/6$.

The step-by-step computation is worth stating explicitly. Event $A$ contains three elementary outcomes, so $\mathbb{P}(A)=3/6$. Event $B$ also contains three elementary outcomes, so $\mathbb{P}(B)=3/6$. Their intersection is the single outcome $\{5\}$, so $\mathbb{P}(A \cap B)=1/6$. If we simply added $3/6+3/6$, we would count outcome $5$ twice, so we subtract $1/6$ and obtain $5/6$.

### Random Variables

A random variable should be introduced in the right direction. First, it is a rule that takes each world $\omega \in \Omega$ and assigns it a value $X(\omega)$. Once that assignment exists, the events of the form $\{X=x\}$ are induced automatically as the sets of worlds that map to the value $x$. If

$$
X \in \{1,\dots,d\},
$$


then the events $\{X=1\},\dots,\{X=d\}$ are mutually exclusive and exhaustive: no world can make $X$ equal to two different values at once, and every world must place $X$ in one of its allowed states. Therefore

$$
\sum_{i=1}^d \mathbb{P}(X=i) = 1.
$$


The possible values are called the states of the variable, and the set of all possible values is its domain. For discrete variables, the probability mass function is often written as $p(X=x)$ or simply $p(x)$ when the variable is clear from context.

A full beginner-to-expert way to read this is the following. At the beginner level, a random variable is a label attached to each outcome. At the intermediate level, that labeling induces a partition of the event space into mutually exclusive cases. At the expert level, it is a measurable map from worlds in $\Omega$ to values in a codomain, and the induced distribution on those values is obtained by pushing probability mass through that map.

A concrete example helps. Let the world be a die roll and define

$$
X=0 \text{ if the roll is even}, \qquad X=1 \text{ if the roll is odd.}
$$


Then the six raw outcomes collapse into only two states. Since $\{2,4,6\}$ map to $0$ and $\{1,3,5\}$ map to $1$,

$$
p(X=0)=3/6, \qquad p(X=1)=3/6.
$$


The random variable therefore compresses a detailed world description into the part of the world we care about.

### PMFs and Indicator Notation

Before writing down specific discrete distributions, it helps to define two pieces of notation that will be used repeatedly.

For a discrete random variable, the probability mass function, or PMF, is the function that assigns a probability to each possible state:

$$
p(X=x)=\mathbb{P}(X=x).
$$


So a PMF is not a second probability law layered on top of ordinary probability. It is the same event probability $\mathbb{P}(X=x)$, written in a way that emphasizes how the value changes as the state $x$ changes.

#### One Diagram That Connects PMFs, PDFs, and CDFs

If you feel confused by PMFs, PDFs, and CDFs, the most common reason is that the same letter $p$ is used for two different kinds of objects:

- For a **discrete** variable, $p(x)$ literally *is* a probability: $p(x)=\mathbb{P}(X=x)$ and $\sum_x p(x)=1$.
- For a **continuous** variable, $p(x)$ is a **density**, not a point probability. You only get probabilities after integrating: $\mathbb{P}(a \le X \le b)=\int_a^b p(t)\,dt$ and $\int p(t)\,dt=1$. In particular, $\mathbb{P}(X=x)=0$ for every single point $x$.

The CDF is the object that exists in both worlds. It is always a probability:

$$
F_X(x)=\mathbb{P}(X \le x).
$$

Once you have $F_X$, you can recover interval probabilities by subtraction:

$$
\mathbb{P}(a < X \le b)=F_X(b)-F_X(a).
$$

The diagram below summarizes how PMFs, PDFs, and CDFs relate.

<p align="center">
  <img src="assets/pmf_pdf_cdf_mental_model.png" alt="PMF vs PDF vs CDF mental model" width="860">
</p>

Two final translation rules help when you move between representations.

- In the discrete case, the PMF value at $x$ is the size of the CDF jump at $x$.
- In the smooth continuous case, the PDF is the derivative of the CDF: $p(x)=\frac{d}{dx}F_X(x)$ at points where that derivative exists.

To make those rules concrete, it helps to work through one tiny discrete example. Suppose $X$ takes values in $\{0,1,2\}$ with PMF

<table align="center">
  <thead>
    <tr><th>$x$</th><th>$p(X=x)$</th></tr>
  </thead>
  <tbody>
    <tr><td>$0$</td><td>$0.2$</td></tr>
    <tr><td>$1$</td><td>$0.5$</td></tr>
    <tr><td>$2$</td><td>$0.3$</td></tr>
  </tbody>
</table>

The CDF is a running total of probability up to a threshold $x$:

$$
F_X(x)=\mathbb{P}(X \le x).
$$

So in this example

<table align="center">
  <thead>
    <tr><th>condition on $x$</th><th>$F_X(x)$</th><th>reason</th></tr>
  </thead>
  <tbody>
    <tr><td>$x<0$</td><td>$0$</td><td>no states are $\le x$</td></tr>
    <tr><td>$0 \le x < 1$</td><td>$0.2$</td><td>only the state $0$ is counted</td></tr>
    <tr><td>$1 \le x < 2$</td><td>$0.2+0.5=0.7$</td><td>states $0$ and $1$ are counted</td></tr>
    <tr><td>$x \ge 2$</td><td>$1$</td><td>all probability has accumulated</td></tr>
  </tbody>
</table>

Now interval probabilities come from subtraction. For example,

$$
\mathbb{P}(1 < X \le 2)=F_X(2)-F_X(1)=1-0.7=0.3,
$$

which matches the PMF value $p(X=2)=0.3$. This is exactly the "jump size equals point probability" rule in action.

In beginner language, a PMF can be viewed as a probability table written in function form. For example, if a three-state weather variable has

$$
p(X=\text{sun})=0.5,\qquad p(X=\text{cloud})=0.3,\qquad p(X=\text{rain})=0.2,
$$


then the PMF is the rule that returns $0.5$ at sun, $0.3$ at cloud, and $0.2$ at rain. The table view and the function view are the same object described in two different ways.

The second piece of notation is the indicator function

$$
\mathbf{1}[X=x],
$$


which equals $1$ when the statement inside the brackets is true and equals $0$ when it is false. Indicator notation matters because it turns a logical statement such as "the realized state is rain" into a numerical exponent or coefficient. That is exactly what happens in the Bernoulli and categorical product forms below.

For example, if the realized weather state is rain, then

$$
\mathbf{1}[X=\text{sun}]=0,\qquad \mathbf{1}[X=\text{cloud}]=0,\qquad \mathbf{1}[X=\text{rain}]=1.
$$


So indicator notation is not a separate probabilistic concept. It is a bookkeeping device that converts a yes-or-no statement into the numbers $1$ or $0$, which lets one formula select the correct term automatically.

### Example 2-2: Bernoulli Distribution

A Bernoulli random variable is binary:

$$
X \in \{0,1\}.
$$


If

$$
\mathbb{P}(X=1) = \rho,
$$


then automatically

$$
\mathbb{P}(X=0) = 1-\rho.
$$


We can write the distribution as

$$
p(X) = \mathrm{Ber}(X;\rho) = \rho^X (1-\rho)^{1-X}.
$$


This evaluates to $\rho$ when $X = 1$ and to $1-\rho$ when $X = 0$.

An equivalent representation is

$$
p(X) = \rho \mathbf{1}[X=1] + (1-\rho)\mathbf{1}[X=0].
$$


To see this mechanically, plug in the only two possible values. If $X=1$, then

$$
\rho^X(1-\rho)^{1-X} = \rho^1(1-\rho)^0 = \rho.
$$


If $X=0$, then

$$
\rho^X(1-\rho)^{1-X} = \rho^0(1-\rho)^1 = 1-\rho.
$$


So the compact formula is not hiding any extra mechanism. The exponents are acting as selectors: the factor attached to the realized state is kept with exponent $1$, while the factor attached to the unrealized state is neutralized by exponent $0$.

### Example 2-3: Discrete Distribution

If $X \in \{1,\dots,d\}$, then a discrete distribution can be represented by a probability table:

$$
\mathbb{P}(X=i) = \rho_i, \qquad \rho_i \ge 0, \qquad \sum_{i=1}^d \rho_i = 1.
$$


This table is the PMF of the variable. For each possible state $i$, the number $\rho_i$ is the probability that $X$ takes that state. Only $d-1$ of those values are free, because the last one is determined by normalization. If the first $d-1$ probabilities are already fixed, the final one must be whatever value makes the whole table sum to one.

Two vocabulary items make that sentence precise. First, a discrete variable with exactly $d$ possible states is sometimes called $d$-ary. For example, a die-outcome variable with support $\{1,2,3,4,5,6\}$ is $6$-ary, while the weather variable with states $\{\text{sun},\text{cloud},\text{rain}\}$ is $3$-ary.

Second, degrees of freedom means the number of independent numerical choices you can make after all required constraints are enforced. Here we have $d$ nonnegative numbers $\rho_1,\dots,\rho_d$, but they must satisfy the single normalization constraint $\sum_{i=1}^d \rho_i=1$. That one constraint removes one free choice, so the PMF has $d-1$ degrees of freedom.

An explicit three-state check: if $d=3$ and you choose $\rho_1=0.5$ and $\rho_2=0.3$, then normalization forces

$$
\rho_3 = 1-\rho_1-\rho_2 = 1-0.5-0.3=0.2.
$$


So you only had two independent choices, which matches $d-1=2$. This same "number of table entries minus normalization constraints" logic is what drives the parameter-count statements later in the chapter.

One compact representation is

$$
p(X) = \prod_{i=1}^d \rho_i^{\mathbf{1}[X=i]}.
$$


This product form is compact, but it should not be read too quickly. The indicator in the exponent decides which factor stays active. If the realized state is $i$, then $\mathbf{1}[X=i]=1$ for that one state and $\mathbf{1}[X=j]=0$ for every other state $j \ne i$. So the factor corresponding to the realized state contributes its probability, while every non-realized factor becomes a zero-th power and therefore contributes the multiplicative identity $1$.

A concrete three-state example makes the structure explicit. Suppose weather tomorrow is modeled as

$$
X \in \{\text{sun}, \text{cloud}, \text{rain}\}
$$


with

$$
\rho_{\text{sun}}=0.5,\qquad \rho_{\text{cloud}}=0.3,\qquad \rho_{\text{rain}}=0.2.
$$


Suppose the realized state is rain. Then the three indicator exponents are

$$
\mathbf{1}[X=\text{sun}]=0,\qquad \mathbf{1}[X=\text{cloud}]=0,\qquad \mathbf{1}[X=\text{rain}]=1.
$$


Substituting those values into the product form gives

$$
p(X)=\rho_{\text{sun}}^{0}\rho_{\text{cloud}}^{0}\rho_{\text{rain}}^{1}.
$$


Now evaluate each factor separately. The first two factors are

$$
\rho_{\text{sun}}^{0}=1,\qquad \rho_{\text{cloud}}^{0}=1,
$$


not because sun or cloud have probability zero, but because those states were not realized in this particular outcome. The final factor is

$$
\rho_{\text{rain}}^{1}=\rho_{\text{rain}}=0.2.
$$


So the whole product reduces to

$$
\rho_{\text{sun}}^0 \rho_{\text{cloud}}^0 \rho_{\text{rain}}^1 = 0.2.
$$


That is why the exponents look like $0,0,1$: they are not probabilities, they are indicator values saying which state actually occurred. If the realized state had been cloud instead, the exponents would have been $0,1,0$ and the same product would have selected $\rho_{\text{cloud}}=0.3$ instead.

<p align="center">
  <img src="../notes/02_probability_reconstructed/assets/figure_2_indicator_product_selector.png" alt="Indicator exponents select the realized state" width="860">
</p>

The main structural idea is that a categorical PMF can be written either as an explicit table or as a product that automatically selects the row corresponding to the realized state. The table form is easier to read at first; the product form becomes useful later when we write more complicated models compactly.

It is helpful to keep one explicit table in mind while reading the formulas. For the three-state weather example,

<table align="center">
  <thead>
    <tr><th>state</th><th>$p(X=\text{state})$</th></tr>
  </thead>
  <tbody>
    <tr><td>sun</td><td>$0.5$</td></tr>
    <tr><td>cloud</td><td>$0.3$</td></tr>
    <tr><td>rain</td><td>$0.2$</td></tr>
  </tbody>
</table>

Here **absolutely continuous** means that probabilities come entirely from interval area under a density function. Such a variable has no isolated point masses: every single exact value has probability zero, and probabilities are recovered by integrating the density over sets.

The PMF notation, the table notation, and the indicator-product notation are all describing this same distribution. The only difference is the representation. The table is easiest for direct reading, while the product form is easier for algebraic manipulation.

### Geometric Distribution

Another basic discrete family is the Geometric distribution. It models repeated independent Bernoulli trials with success probability $\rho$ until the first success occurs. One must be careful about conventions, because two closely related definitions are common in textbooks and software.

In these notes, and in the course homework workflow built around Pyro, the random variable counts the number of failures before the first success. Its support is therefore

$$
X \in \{0,1,2,\dots\},
$$


and its PMF is

$$
p(X=x)=(1-\rho)^x\rho.
$$


The formula is easy to derive once the event is stated explicitly. The event $X=x$ means the first $x$ trials fail and the next trial succeeds. Because the trials are independent, we multiply the probabilities of those pieces: $x$ failures contribute $(1-\rho)^x$ and the final success contributes $\rho$.

For example, if $\rho=0.2$, then

$$
p(X=0)=0.2,\qquad p(X=1)=0.8 \cdot 0.2=0.16,\qquad p(X=2)=0.8^2 \cdot 0.2=0.128.
$$


The key numerical pattern is that each step to the right multiplies the previous probability by another factor of $(1-\rho)$. When $\rho=0.2$, that factor is $0.8$, so each bar is $80\%$ of the bar immediately before it. Concretely, the first few probabilities are $0.2$, $0.16$, $0.128$, and so on. That is what "decays geometrically to the right" means: the bars do not decrease by subtracting a fixed amount; they decrease by repeated multiplication by the same ratio.

So a histogram of this distribution has a tallest bar at $x=0$, then progressively smaller bars as $x$ increases. The right tail is long because there is always some chance that many failures occur before the first success, but the probability of those larger counts drops off by repeated multiplication.

Expected value (mean). For a discrete variable, the expected value is defined as the probability-weighted average

$$
\mathbb{E}[X]=\sum_{x} x\,p(X=x).
$$


For the Geometric distribution with $p(X=x)=(1-\rho)^x\rho$ on $\{0,1,2,\dots\}$, this sum can be evaluated in closed form. Let $r=1-\rho$. Then

$$
\mathbb{E}[X]=\sum_{x=0}^\infty x\,r^x\,\rho=\rho\sum_{x=0}^\infty x r^x.
$$


At this point a nontrivial series identity appears, so it should be derived instead of treated as magic. Start from the ordinary geometric series

$$
\sum_{x=0}^\infty r^x=\frac{1}{1-r}, \qquad |r|<1.
$$


Differentiate both sides with respect to $r$:

$$
\sum_{x=1}^\infty x r^{x-1}=\frac{1}{(1-r)^2}.
$$


Now multiply both sides by $r$:

$$
\sum_{x=1}^\infty x r^x=\frac{r}{(1-r)^2}.
$$


Adding the $x=0$ term changes nothing because it contributes $0$, so

$$
\sum_{x=0}^\infty x r^x=\frac{r}{(1-r)^2}.
$$


Here $r=1-\rho \in (0,1)$, so the identity applies, and we obtain

$$
\mathbb{E}[X]=\rho\cdot \frac{r}{(1-r)^2}=\rho\cdot \frac{1-\rho}{\rho^2}=\frac{1-\rho}{\rho}.
$$


So the mean under this zero-based convention is

$$
\mathbb{E}[X]=\frac{1-\rho}{\rho}.
$$


If $\rho=0.2$, the expected number of failures before the first success is therefore $4$. A different but equally common convention counts the total number of trials until the first success. Under that one-based convention the support starts at $1$ instead of $0$, the PMF becomes $p(Y=y)=(1-\rho)^{y-1}\rho$, and the mean becomes $1/\rho$. When using a software library, one should always check which convention the library adopts before interpreting the samples.

### Example 2-4: Dentist Example

The chapter uses three binary variables:

- $C = 1$ means cavity
- $T = 1$ means toothache
- $D = 1$ means the probe catches on the tooth

The joint distribution over $(T,D,C)$ is:

<table align="center">
  <thead>
    <tr><th>$(T,D,C)$</th><th>$p(T,D,C)$</th></tr>
  </thead>
  <tbody>
    <tr><td>$(0,0,0)$</td><td>$0.576$</td></tr>
    <tr><td>$(0,0,1)$</td><td>$0.008$</td></tr>
    <tr><td>$(0,1,0)$</td><td>$0.144$</td></tr>
    <tr><td>$(0,1,1)$</td><td>$0.072$</td></tr>
    <tr><td>$(1,0,0)$</td><td>$0.064$</td></tr>
    <tr><td>$(1,0,1)$</td><td>$0.012$</td></tr>
    <tr><td>$(1,1,0)$</td><td>$0.016$</td></tr>
    <tr><td>$(1,1,1)$</td><td>$0.108$</td></tr>
  </tbody>
</table>

The eight rows are mutually exclusive and exhaustive, so their probabilities sum to one.

It is useful to say exactly how to read one row. The row $111$ means toothache, probe catch, and cavity all occur together. Its probability $0.108$ is not a conditional number and not a marginal number; it is the probability of that whole conjunction. Every later marginal or conditional calculation in this section will be built by summing or renormalizing rows from this joint table.

### Marginal Probabilities

To get the probability of one variable, add up all joint entries consistent with that value.

$$
p(T=0) = \sum_{d,c} p(T=0,D=d,C=c)
$$


$$
= 0.576 + 0.008 + 0.144 + 0.072 = 0.80.
$$


This is the operational meaning of marginalization: keep the value of interest fixed, and sum over every possible value of the hidden variables that could accompany it.

A second marginal shows the same procedure from another angle. To compute the chance of a cavity, sum every row with $C=1$:

$$
p(C=1)=0.008+0.072+0.012+0.108=0.20.
$$


This explains why a marginal is called a marginal: it is what remains after the other coordinates have been summed away.

### Conditional Probability

Conditioning means restricting attention to worlds where the condition holds:

$$
p(D=d \mid T=t) = \frac{p(D=d,T=t)}{p(T=t)}.
$$


The numerator is the probability that both things happen; the denominator is the total probability of the condition. The result is a normalized probability distribution over $D$ given $T=t$.

For the dentist table, conditioning on $T=1$ means we throw away every row with $T=0$ and keep only the four rows with toothache. Inside that restricted world, the total probability mass is

$$
p(T=1)=0.064+0.012+0.016+0.108=0.20.
$$


Now the conditional probability of a probe catch becomes

$$
p(D=1 \mid T=1)=\frac{0.016+0.108}{0.20}=\frac{0.124}{0.20}=0.62.
$$


The key beginner intuition is "restrict first, renormalize second."

It is also important to separate conditioning from intervention. The conditional distribution $p(D \mid T=1)$ is obtained by taking the original joint distribution, keeping only the worlds in which toothache has already been observed, and renormalizing the remaining probabilities so they sum to one. So this conditional answers an informational question: among the worlds where $T=1$ is already true, how does the probe variable $D$ behave?

That is different from an intervention. An intervention would mean externally forcing $T$ to equal $1$ and then asking how $D$ changes under that manipulated system. In the dentist story, observing a toothache gives information about whether a cavity is present, and that information changes the distribution of $D$. But physically causing a toothache would not automatically carry the same information about the cavity state. A plain joint distribution supports conditioning; it does not, by itself, tell us the effect of interventions. For intervention questions, one needs extra causal structure beyond ordinary probability tables.

### Example 2-5: Bayes Rule

Bayes rule starts from a model of how likely an observation is under each hypothesis, such as $p(D=d \mid C=c)$, and turns it into a model of how likely each hypothesis is after the observation has been seen, namely $p(C=c \mid D=d)$:

$$
p(C=c \mid D=d) = \frac{p(D=d \mid C=c)p(C=c)}{p(D=d)}.
$$


In this formula, the hypothesis is the value of $C$, meaning the statement "the cavity variable equals $c$." The observation is the value of $D$, meaning the statement "the probe variable equals $d$." So this example is not talking about an abstract unnamed hypothesis. It is specifically asking how probable each cavity state is after we observe the probe outcome.

Before using shorthand language, it helps to name each term explicitly. The prior is $p(C=c)$, which is the probability assigned to the cavity-state hypothesis before seeing the probe observation. The likelihood is $p(D=d \mid C=c)$, which measures how compatible the observed probe result is with that cavity state. The evidence is $p(D=d)$, which is the total probability of seeing that probe result after averaging over every cavity case. The posterior is $p(C=c \mid D=d)$, which is the updated probability of the cavity state after the probe result has been taken into account.

The word posterior does not name a new kind of probability rule. It is an ordinary conditional probability, using the same conditioning idea introduced earlier in the chapter. The only difference is the roles of the events. Earlier we conditioned one observable event on another observable event. Here we condition a hypothesis about the cavity state on the observed probe result. So "posterior" means the probability of the hypothesis after the observation has been taken into account.

With those names in place, the formula can be read as the sentence

$$
\text{posterior} = \text{likelihood} \cdot \text{prior} / \text{evidence}.
$$


This sentence is only a mnemonic for the roles played by the four terms. It is not a second formula that must be memorized separately. What it means operationally is: start from the old hypothesis probability, multiply by how compatible the observation is with that hypothesis, and then divide by the total probability of the observation so the final answers across all hypotheses sum to one.

To describe the odds form, suppose $H_1$ and $H_0$ are two mutually exclusive hypotheses, meaning two competing explanations that cannot both be true at the same time. Let $E$ denote the observed evidence. Bayes' rule then implies

$$
\frac{p(H_1 \mid E)}{p(H_0 \mid E)} = \frac{p(E \mid H_1)}{p(E \mid H_0)} \cdot \frac{p(H_1)}{p(H_0)}.
$$


This odds form is often more informative than the scalar formula because each ratio has a distinct interpretation. The prior odds

$$
\frac{p(H_1)}{p(H_0)}
$$


compare the plausibility of the two hypotheses before any new evidence is observed. The likelihood ratio

$$
\frac{p(E \mid H_1)}{p(E \mid H_0)}
$$


measures how much more strongly the evidence supports $H_1$ than $H_0$. The posterior odds

$$
\frac{p(H_1 \mid E)}{p(H_0 \mid E)}
$$


are the updated comparison after the evidence has been incorporated. The evidence term does not appear explicitly in this ratio form because the same normalizing constant $p(E)$ appears in both posterior probabilities and cancels when the quotient is taken.

For the dentist example, suppose:

$$
p(T=1 \mid C=0) = 0.1, \qquad p(T=1 \mid C=1) = 0.6
$$


$$
p(C=0) = 0.8, \qquad p(C=1) = 0.2.
$$


Here the hypothesis of interest is $C=1$, meaning "the patient has a cavity," and the observation is $T=1$, meaning "the patient has a toothache." We now apply Bayes' rule with those two specific events:

$$
p(C=1 \mid T=1)=\frac{p(T=1 \mid C=1)p(C=1)}{p(T=1)}.
$$


Now fill in each term one at a time. The likelihood term

$$
p(T=1 \mid C=1)=0.6
$$


means that among the worlds where a cavity is present, toothache occurs with probability $0.6$. The prior term

$$
p(C=1)=0.2
$$


means that before observing any toothache, the cavity probability is $0.2$. Multiplying these two quantities uses the product rule and gives the joint probability that both events occur:

$$
p(T=1,C=1)=p(T=1 \mid C=1)p(C=1)=0.6 \cdot 0.2 = 0.12.
$$


So the numerator $0.12$ is not an arbitrary number. It is the probability of the conjunction "toothache and cavity."

Next compute the denominator $p(T=1)$, which is the total probability of observing a toothache. There are two mutually exclusive ways for toothache to occur in this model: either there is a cavity or there is not. So we apply the law of total probability over the two cavity cases:

$$
p(T=1)=p(T=1 \mid C=1)p(C=1)+p(T=1 \mid C=0)p(C=0).
$$


Now substitute the given numbers:

$$
p(T=1)=0.6 \cdot 0.2 + 0.1 \cdot 0.8 = 0.12 + 0.08 = 0.20.
$$


The second term $0.1 \cdot 0.8 = 0.08$ is the probability of "toothache and no cavity." Adding $0.12$ and $0.08$ gives the full toothache probability $0.20$.

Now divide the numerator by the denominator:

$$
p(C=1 \mid T=1)=\frac{0.12}{0.20}=0.60.
$$


This final number means that after observing a toothache, the probability of a cavity rises to $0.60$. So the observation has changed the cavity probability from the prior value $0.20$ to the posterior value $0.60$.

The derivation can also be unpacked from the definition of conditional probability itself. Start with

$$
p(C=1 \mid T=1)=\frac{p(C=1,T=1)}{p(T=1)}.
$$


Then factor the numerator using the product rule:

$$
p(C=1,T=1)=p(T=1 \mid C=1)p(C=1).
$$


Substituting this into the conditional formula gives Bayes' rule. So Bayes' rule is not an extra axiom; it is the conditional-probability definition plus the product rule written in a convenient direction.

### Law of Total Probability

If $B_1,\dots,B_k$ form a partition of the sample space, then any event $A$ satisfies

$$
p(A)=\sum_{i=1}^k p(A \mid B_i)p(B_i).
$$


The law is simple but foundational. It says that if the worlds are first split into mutually exclusive and exhaustive cases, then the total probability of $A$ is the weighted average of its conditional probabilities inside those cases. Here mutually exclusive means at most one case can hold at a time, and exhaustive means at least one case must hold. So exactly one of the $B_i$ happens in every world.

An inline numerical example makes the averaging interpretation concrete. Suppose the hidden situation has three cases:

$$
B_1=\{\text{route 1}\},\qquad B_2=\{\text{route 2}\},\qquad B_3=\{\text{route 3}\},
$$


with

$$
p(B_1)=0.5,\qquad p(B_2)=0.3,\qquad p(B_3)=0.2.
$$


Let the event $A$ be "arrive within 30 minutes." Suppose the on-time probabilities depend on the route:

$$
p(A \mid B_1)=0.9,\qquad p(A \mid B_2)=0.6,\qquad p(A \mid B_3)=0.4.
$$


Then the law of total probability says

$$
p(A)=p(A \mid B_1)p(B_1)+p(A \mid B_2)p(B_2)+p(A \mid B_3)p(B_3).
$$


Substituting the numbers gives

$$
p(A)=0.9 \cdot 0.5 + 0.6 \cdot 0.3 + 0.4 \cdot 0.2 = 0.45 + 0.18 + 0.08 = 0.71.
$$


Each product $p(A \mid B_i)p(B_i)$ is the probability that both "case $B_i$ happens" and "event $A$ happens" occur together. The sum adds those disjoint ways for $A$ to happen.

The formula follows directly from disjoint decomposition. Because the sets $B_1,\dots,B_k$ form a partition, the event $A$ can be written as the disjoint union

$$
A=(A \cap B_1)\cup \cdots \cup (A \cap B_k).
$$


Therefore additivity gives

$$
p(A)=\sum_{i=1}^k p(A \cap B_i).
$$


Applying the product rule to each summand yields

$$
p(A \cap B_i)=p(A \mid B_i)p(B_i),
$$


and substituting those terms back into the sum gives the law of total probability. So the law is not an extra identity to memorize; it is the ordinary additivity axiom plus the product rule applied to a partition.

In the dentist example, the evidence term $p(T=1)$ is exactly a law-of-total-probability computation over the cavity cases. The two cases $C=1$ and $C=0$ form a partition, so

$$
p(T=1)=p(T=1 \mid C=1)p(C=1)+p(T=1 \mid C=0)p(C=0).
$$


Plugging in the numbers gives

$$
p(T=1)=0.6 \cdot 0.2 + 0.1 \cdot 0.8 = 0.20.
$$


So the evidence term is not mysterious. It is the ordinary total probability of the observation, computed by averaging over the hidden hypothesis cases.

### Worked Example: Base Rates and Screening

Suppose a rare disease has prevalence

$$
p(D=1)=0.01.
$$


A screening test has sensitivity

$$
p(T=+ \mid D=1)=0.95
$$


and false-positive rate

$$
p(T=+ \mid D=0)=0.10.
$$


If a patient tests positive, the posterior disease probability is

$$
p(D=1 \mid T=+)=\frac{p(T=+ \mid D=1)p(D=1)}{p(T=+)}.
$$


The denominator comes from the law of total probability:

$$
p(T=+)=0.95 \cdot 0.01 + 0.10 \cdot 0.99 = 0.1085.
$$


Therefore

$$
p(D=1 \mid T=+)=\frac{0.95 \cdot 0.01}{0.1085}\approx 0.0876.
$$


Here is what those numbers mean in both probability and percentage form. Probabilities are numbers between $0$ and $1$. To convert a probability to a percentage, multiply by $100$.

In this example, the prior disease probability is $p(D=1)=0.01$, which is $1\%$. After observing a positive test, the posterior is $p(D=1 \mid T=+)\approx 0.0876$, which is about $8.76\%$ (rounded to $8.8\%$). So the test is informative because it raises the disease probability from $0.01$ to about $0.088$, but the disease still remains unlikely (well under $10\%$) because the base rate was extremely small to begin with. This is exactly the setting in which **base-rate neglect** causes intuitive mistakes: one focuses on the dramatic positive test result and forgets that the event was already very rare before the test was observed.

### Example 2-6: Table-Based Computation

The same Bayes update can be done by manipulating tables directly. The goal is to compute the posterior distribution $p(C \mid T=1)$, meaning "how likely is a cavity after we observe toothache."

The table view is easiest to understand if we write the target posterior in a way that matches the three operations we will perform:

$$
p(C=c \mid T=1)=\frac{\sum_d p(T=1,d,c)}{\sum_{c',d} p(T=1,d,c')}.
$$


This formula is meant pointwise. For each specific cavity value $c$, the numerator sums over every probe value $d$ that is compatible with that cavity value. The denominator then sums over every cavity value and every probe value, so it is the total probability of the evidence $T=1$. Dividing by that denominator turns the remaining nonnegative entries into a proper posterior distribution over the cavity states.

<p align="center">
  <img src="../notes/02_probability_reconstructed/assets/figure_2_table_update_pipeline.png" alt="Restriction, marginalization, and normalization pipeline" width="860">
</p>

<!-- table-stack:start -->
<table align="center" border="0" cellpadding="0" cellspacing="16">
  <tbody>
    <tr>
      <td valign="top">
        <p><strong>Restrict to $T=1$</strong></p>
        <table>
          <thead>
            <tr>
              <th>$D$</th>
              <th>$C$</th>
              <th>$p(T=1,D,C)$</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>$0$</td><td>$0$</td><td>$0.064$</td></tr>
            <tr><td>$0$</td><td>$1$</td><td>$0.012$</td></tr>
            <tr><td>$1$</td><td>$0$</td><td>$0.016$</td></tr>
            <tr><td>$1$</td><td>$1$</td><td>$0.108$</td></tr>
          </tbody>
        </table>
      </td>
      <td valign="top">
        <p><strong>Marginalize over $D$</strong></p>
        <table>
          <thead>
            <tr>
              <th>$C$</th>
              <th>$p(T=1,C)$</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>$0$</td><td>$0.064 + 0.016 = 0.080$</td></tr>
            <tr><td>$1$</td><td>$0.012 + 0.108 = 0.120$</td></tr>
          </tbody>
        </table>
      </td>
      <td valign="top">
        <p><strong>Normalize</strong></p>
        <table>
          <thead>
            <tr>
              <th>$C$</th>
              <th>$p(C \mid T=1)$</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>$0$</td><td>$0.08 / 0.20 = 0.40$</td></tr>
            <tr><td>$1$</td><td>$0.12 / 0.20 = 0.60$</td></tr>
          </tbody>
        </table>
      </td>
    </tr>
  </tbody>
</table>
<!-- table-stack:end -->

The three tables correspond exactly to three conceptual operations, and every number in them comes from one of three formulas: restriction (copy the consistent rows), marginalization (sum out $D$), and normalization (divide by the evidence total).

Step 1 (restrict to $T=1$). The first table is the $T=1$ slice of the full joint table $p(T,D,C)$. Each entry is copied directly from the original joint table by keeping only the rows with $T=1$. The total mass of this restricted slice is

$$
p(T=1,D=0,C=0)=0.064,\qquad p(T=1,D=0,C=1)=0.012,
$$


$$
p(T=1,D=1,C=0)=0.016,\qquad p(T=1,D=1,C=1)=0.108,
$$


and summing them gives

$$
p(T=1)=0.064+0.012+0.016+0.108=0.20.
$$


This $0.20$ is the probability that a toothache occurs under the model, before conditioning on anything else. It is also the normalizing constant we will divide by at the end.

Step 2 (marginalize out $D$). To obtain $p(T=1,C)$, add over the two possible values of $D$ for each fixed cavity state:

$$
p(T=1,C=0)=p(T=1,D=0,C=0)+p(T=1,D=1,C=0)=0.064+0.016=0.080,
$$


$$
p(T=1,C=1)=p(T=1,D=0,C=1)+p(T=1,D=1,C=1)=0.012+0.108=0.120.
$$


Notice that this intermediate table is still not a conditional distribution over $C$. It is a joint table with $T=1$ fixed, so it sums to $p(T=1)$:

$$
0.080+0.120=0.20.
$$


Step 3 (normalize). Finally divide by the evidence total $p(T=1)=0.20$ to turn $p(T=1,C)$ into a posterior distribution over $C$:

$$
p(C=0 \mid T=1)=\frac{0.080}{0.20}=0.40,\qquad p(C=1 \mid T=1)=\frac{0.120}{0.20}=0.60.
$$


Now the two posterior probabilities sum to $1$, as they must. Interpreting the result: after observing toothache, the cavity probability rises from the prior $p(C=1)=0.20$ to the posterior $p(C=1 \mid T=1)=0.60$.

### Expectation

The expectation, or expected value, is the long-run average value of the variable if the same random experiment were repeated many times and the outcomes were averaged. In a discrete model, that long-run average is computed by weighting each possible value by the probability of seeing it. So the expectation is a probability-weighted average, not a guess about the single next outcome.

The word expected can be misleading in ordinary English. In probability, it does not mean "what I predict will happen next" or "the most likely outcome." It means the center of mass of the distribution. That is why an expectation can be a number the variable never literally takes.

For a discrete variable, the definition is:

$$
\mathbb{E}[X] = \sum_x x \, p(x).
$$


Each term in the sum has a clear meaning. The value $x$ tells us what the outcome contributes if it occurs, and the factor $p(x)$ tells us how often it occurs in the long run. Multiplying and summing therefore averages the possible outcomes according to how likely they are.

For a Bernoulli variable, $\mathbb{E}[X] = \rho$, which is why the Bernoulli parameter is also the mean.

A full worked example shows why expectation is called a weighted average. Suppose

$$
\mathbb{P}(X=0)=0.7, \qquad \mathbb{P}(X=1)=0.3.
$$


Then

$$
\mathbb{E}[X]=0 \cdot 0.7 + 1 \cdot 0.3 = 0.3.
$$


For a die roll with values $1$ through $6$,

$$
\mathbb{E}[X] = \sum_{x=1}^6 x \cdot \frac{1}{6} = \frac{1+2+3+4+5+6}{6}=3.5.
$$


So expectation is not required to be a value the variable actually takes. A fair die never lands on $3.5$, but $3.5$ is still the mean location of the distribution.

### Linearity of Expectation

Expectation is linear:

$$
\mathbb{E}[aX+bY+c]=a\mathbb{E}[X]+b\mathbb{E}[Y]+c.
$$


No independence assumption is required. That point is easy to miss because many later formulas do require independence, but linearity of expectation does not. The rule holds even when $X$ and $Y$ are strongly dependent.

It is worth checking that claim with a dependent example. Let $X$ be Bernoulli with

$$
\mathbb{P}(X=1)=0.3,\qquad \mathbb{P}(X=0)=0.7,
$$


and define

$$
Y=1-X.
$$


Then $X$ and $Y$ are completely dependent: once $X$ is known, $Y$ is forced. But linearity still works:

$$
\mathbb{E}[X+Y]=\mathbb{E}[1]=1,
$$


while

$$
\mathbb{E}[X]+\mathbb{E}[Y]=0.3+0.7=1.
$$


So dependence does not break linearity. That is exactly why indicator decompositions are so powerful later in probability and machine learning.

For a concrete example, suppose three coin flips have indicator variables $H_1,H_2,H_3$, where $H_i=1$ if flip $i$ is heads and $0$ otherwise. Let

$$
N=H_1+H_2+H_3
$$


denote the total number of heads. Then

$$
\mathbb{E}[N]=\mathbb{E}[H_1]+\mathbb{E}[H_2]+\mathbb{E}[H_3].
$$


If each flip has head probability $\rho$, then $\mathbb{E}[H_i]=\rho$ for every $i$, so

$$
\mathbb{E}[N]=3\rho.
$$


This conclusion does not require us to enumerate all eight outcomes explicitly. Linearity lets us decompose a complicated count into simple indicator expectations and add them back together.

### Variance, Covariance, and Correlation

Expectation gives the center of a distribution, but it does not describe spread. The basic spread measure is variance:

$$
\mathrm{Var}(X)=\mathbb{E}[(X-\mathbb{E}[X])^2].
$$


Expanding the square gives the useful identity

$$
\mathrm{Var}(X)=\mathbb{E}[X^2]-\mathbb{E}[X]^2.
$$


An inline Bernoulli example shows how to use the identity mechanically. If $X \in \{0,1\}$ with $p(X=1)=\rho$, then $X^2=X$ for both possible values, so

$$
\mathbb{E}[X]=\rho,
$$


and

$$
\mathbb{E}[X^2]=\mathbb{E}[X]=\rho.
$$


Therefore

$$
\mathrm{Var}(X)=\rho-\rho^2=\rho(1-\rho).
$$


So for a Bernoulli random variable, the spread is largest near $\rho=1/2$ and shrinks to zero as $\rho$ approaches $0$ or $1$.

For two variables, covariance is

$$
\mathrm{Cov}(X,Y)=\mathbb{E}[(X-\mathbb{E}[X])(Y-\mathbb{E}[Y])].
$$


The normalized version is correlation:

$$
\mathrm{Corr}(X,Y)=\frac{\mathrm{Cov}(X,Y)}{\sqrt{\mathrm{Var}(X)\mathrm{Var}(Y)}}.
$$


Variance reacts predictably to affine transformations:

$$
\mathrm{Var}(aX+b)=a^2 \mathrm{Var}(X), \qquad \mathrm{Cov}(aX+b,cY+d)=ac\,\mathrm{Cov}(X,Y).
$$


These formulas show what each quantity measures. Adding a constant shifts the location but does not change spread. Multiplying by $a$ rescales the spread by $a^2$. Covariance records whether large values of one variable tend to occur with large or small values of the other.

A diagnostic example shows why mean and variance are genuinely different summaries. Let $X$ be constant at $3$, and let $Y$ equal $0$ or $6$ with probabilities $1/2$ and $1/2$. Then

$$
\mathbb{E}[X]=3, \qquad \mathbb{E}[Y]=0 \cdot \frac{1}{2}+6 \cdot \frac{1}{2}=3,
$$


so both variables have the same mean. But

$$
\mathrm{Var}(X)=0
$$


because $X$ never moves, while

$$
\mathrm{Var}(Y)=\mathbb{E}[Y^2]-\mathbb{E}[Y]^2 =\left(0^2 \cdot \frac{1}{2}+6^2 \cdot \frac{1}{2}\right)-3^2 =18-9=9.
$$


So two distributions can agree perfectly on their center and still differ sharply in uncertainty.

Covariance also does not capture every form of dependence. Let $X$ take values $-1$, $0$, and $1$ with equal probability, and define

$$
Y=X^2.
$$


Then $Y$ is completely determined by $X$, so the variables are dependent. But

$$
\mathbb{E}[X]=0, \qquad \mathbb{E}[XY]=\mathbb{E}[X^3]=0,
$$


which gives

$$
\mathrm{Cov}(X,Y)=\mathbb{E}[XY]-\mathbb{E}[X]\mathbb{E}[Y]=0.
$$


So zero covariance does not imply independence. It only rules out linear dependence in the centered variables.

### Independence

Two random variables $X$ and $Y$ are independent if

$$
p(X=x,Y=y) = p(X=x)p(Y=y)\qquad \text{for every pair of values }x,y.
$$


Equivalently, observing one does not change the distribution of the other:

$$
p(X=x \mid Y=y) = p(X=x)\qquad \text{for every }y\text{ with }p(Y=y)>0.
$$


The equivalence between these two definitions is worth writing out because it gets used constantly. If

$$
p(X=x,Y=y)=p(X=x)p(Y=y),
$$


then for any value $y$ of $Y$ with positive probability,

$$
p(X=x \mid Y=y)=\frac{p(X=x,Y=y)}{p(Y=y)}=\frac{p(X=x)p(Y=y)}{p(Y=y)}=p(X=x).
$$


Conversely, if

$$
p(X=x \mid Y=y)=p(X=x)
$$


for every value $y$ with $p(Y=y)>0$, then multiplying both sides by $p(Y=y)$ gives

$$
p(X=x,Y=y)=p(X=x \mid Y=y)p(Y=y)=p(X=x)p(Y=y).
$$


So the factorization view and the "observing $Y$ changes nothing" view are two algebraically equivalent ways to state the same independence claim. The caveat about $p(Y)>0$ is important: conditional probability is only defined when the conditioning event has nonzero probability.

Independence also simplifies the joint distribution by reducing how many numbers must be specified. Suppose $X$ and $Y$ are both $d$-ary, meaning each takes one of $d$ states. A general joint distribution $p(X,Y)$ is a $d \times d$ probability table with $d^2$ entries. Those entries must be nonnegative and must satisfy exactly one normalization constraint:

$$
\sum_{x}\sum_{y} p(X=x,Y=y)=1.
$$


So, in the degrees-of-freedom sense, a full unconstrained joint table has $d^2-1$ free parameters: you can choose $d^2-1$ of the entries arbitrarily (subject to nonnegativity), and the final entry is forced by the requirement that the whole table sums to $1$.

Under independence, the joint factorizes as

$$
p(X,Y)=p(X)p(Y).
$$


Now you do not need to choose $d^2$ unrelated entries. You only choose the two marginal tables. The marginal $p(X)$ has $d$ entries summing to $1$, so it has $d-1$ degrees of freedom. The marginal $p(Y)$ also has $d-1$ degrees of freedom. Therefore the independent model has $(d-1)+(d-1)=2d-2$ degrees of freedom. Once those marginal numbers are chosen, every joint entry is determined by multiplication.

An explicit $d=3$ example shows the reduction mechanically. Let

$$
p(X)=(0.5,0.3,0.2),\qquad p(Y)=(0.1,0.6,0.3).
$$


Independence implies, for example,

$$
p(X=1,Y=2)=p(X=1)p(Y=2)=0.5\cdot 0.6=0.30,
$$


and similarly every other joint entry is a product of one $X$-marginal number and one $Y$-marginal number. In this $3 \times 3$ case, an unconstrained joint distribution would have $3^2-1=8$ degrees of freedom, while independence uses only $2\cdot 3-2=4$ degrees of freedom (two independent choices for $p(X)$ and two for $p(Y)$).

This reduction is the main motive for using independence or conditional independence assumptions in AI models: fewer degrees of freedom means fewer parameters to estimate from data and a simpler structure for inference. The tradeoff is that independence is a strong modeling claim. It restricts which joint distributions are representable, so it should only be used when it is substantively justified (or when it is a deliberate approximation).

### Example 2-7: Independence

Let $X$ be a biased coin and $Y$ a weighted four-sided die. If they are independent, then every joint entry is obtained by multiplying one marginal probability from $X$ with one marginal probability from $Y$. Independence means the probability assigned to a pair $(x,y)$ factors into the probability of $x$ alone and the probability of $y$ alone.

<table align="center" border="0" cellpadding="0" cellspacing="16">
  <tbody>
    <tr>
      <td valign="top" align="center">
        <table>
          <thead>
            <tr><th>$X$</th><th>$p(X)$</th></tr>
          </thead>
          <tbody>
            <tr><td>$0$</td><td>$0.7$</td></tr>
            <tr><td>$1$</td><td>$0.3$</td></tr>
          </tbody>
        </table>
      </td>
      <td valign="top" align="center">
        <table>
          <thead>
            <tr><th>$Y$</th><th>$p(Y)$</th></tr>
          </thead>
          <tbody>
            <tr><td>$1$</td><td>$0.2$</td></tr>
            <tr><td>$2$</td><td>$0.3$</td></tr>
            <tr><td>$3$</td><td>$0.4$</td></tr>
            <tr><td>$4$</td><td>$0.1$</td></tr>
          </tbody>
        </table>
      </td>
      <td valign="top" align="center">
        <table>
          <thead>
            <tr><th>$X$</th><th>$Y$</th><th>$p(X,Y)$</th></tr>
          </thead>
          <tbody>
            <tr><td>$0$</td><td>$1$</td><td>$0.7 \cdot 0.2 = 0.14$</td></tr>
            <tr><td>$0$</td><td>$2$</td><td>$0.7 \cdot 0.3 = 0.21$</td></tr>
            <tr><td>$0$</td><td>$3$</td><td>$0.7 \cdot 0.4 = 0.28$</td></tr>
            <tr><td>$0$</td><td>$4$</td><td>$0.7 \cdot 0.1 = 0.07$</td></tr>
            <tr><td>$1$</td><td>$1$</td><td>$0.3 \cdot 0.2 = 0.06$</td></tr>
            <tr><td>$1$</td><td>$2$</td><td>$0.3 \cdot 0.3 = 0.09$</td></tr>
            <tr><td>$1$</td><td>$3$</td><td>$0.3 \cdot 0.4 = 0.12$</td></tr>
            <tr><td>$1$</td><td>$4$</td><td>$0.3 \cdot 0.1 = 0.03$</td></tr>
          </tbody>
        </table>
        <p><strong>Full joint table obtained by multiplying marginals entry by entry</strong></p>
      </td>
    </tr>
  </tbody>
</table>

To verify independence explicitly, check one conditional. Since

$$
p(X=1,Y=4)=0.03
$$


and

$$
p(Y=4)=0.1,
$$


we have

$$
p(X=1 \mid Y=4)=\frac{0.03}{0.1}=0.3=p(X=1).
$$


The observation of $Y$ leaves the distribution of $X$ unchanged, which is the operational meaning of independence.

### Pairwise Versus Mutual Independence

Independence among more than two variables needs careful wording, because there are multiple strength levels that sound similar but are not equivalent.

Variables $X_1,\dots,X_n$ are mutually independent if every subcollection factorizes:

$$
p(X_{i_1},\dots,X_{i_k})=\prod_{j=1}^k p(X_{i_j})
$$


for every subset of indices $\{i_1,\dots,i_k\}$. In words: no matter which subset of variables you look at, their joint distribution is the product of their marginals.

Pairwise independence is weaker. It only requires that every pair factorizes:

$$
p(X_i,X_j)=p(X_i)p(X_j)\qquad \text{for every } i \ne j.
$$


In words: looking at any single pair, observing one variable does not change the distribution of the other. But pairwise independence does not say anything about three-way or higher-order structure.

For three variables, it is worth spelling out the difference explicitly, because this is where many wrong intuitions arise. Mutual independence of $(X_1,X_2,X_3)$ includes the pairwise factorizations

$$
p(X_1,X_2)=p(X_1)p(X_2),\qquad p(X_1,X_3)=p(X_1)p(X_3),\qquad p(X_2,X_3)=p(X_2)p(X_3),
$$


but it also includes the genuinely stronger triple factorization

$$
p(X_1,X_2,X_3)=p(X_1)p(X_2)p(X_3).
$$


Pairwise independence only demands the first three equations. It does not constrain $p(X_1,X_2,X_3)$ beyond what is forced by those pairwise marginals.

Mutual independence always implies pairwise independence. The reason is that if the joint factorizes, then any lower-dimensional joint is obtained by summing out the remaining variables and the product structure is preserved. For example, if

$$
p(X_1,X_2,X_3)=p(X_1)p(X_2)p(X_3),
$$


then marginalizing out $X_3$ gives

$$
p(X_1,X_2)=\sum_{x_3} p(X_1,X_2,X_3=x_3)=p(X_1)p(X_2)\sum_{x_3}p(X_3=x_3)=p(X_1)p(X_2),
$$


because $\sum_{x_3}p(X_3=x_3)=1$. So mutual independence is strictly stronger: it contains extra content beyond the pairwise statements.

A clean motive for caring about the distinction is that mutual independence is strong enough to reconstruct the full joint distribution from the marginals, while pairwise independence is not. This matters any time you need the probability of a three-way conjunction such as $\mathbb{P}(X_1=a,X_2=b,X_3=c)$. Under mutual independence you multiply three one-variable probabilities. Under pairwise independence alone, that multiplication is not justified.

If each $X_i$ is $d$-ary, then an unconstrained full joint table over $(X_1,\dots,X_n)$ has $d^n$ entries and one normalization constraint, so it has $d^n-1$ degrees of freedom. Under mutual independence, you only specify the $n$ marginal tables. Each marginal has $d-1$ degrees of freedom, so mutual independence reduces the parameter count to $n(d-1)$. Pairwise independence does not lead to an equally clean reduction, because it does not force a single global factorized form.

An explicit parameter-count example makes the abstraction tangible. Suppose $n=3$ and $d=2$ (three binary variables). Then the full joint distribution has $2^3=8$ table entries. Normalization forces those eight probabilities to sum to $1$, so the joint has $8-1=7$ degrees of freedom. Under mutual independence, each variable is determined by a single number, such as $\rho_i=p(X_i=1)$, so the whole model uses only $3$ degrees of freedom. For example, if

$$
p(X_1=1)=0.6,\qquad p(X_2=1)=0.2,\qquad p(X_3=1)=0.5,
$$


then mutual independence forces

$$
p(X_1=1,X_2=0,X_3=1)=p(X_1=1)p(X_2=0)p(X_3=1)=0.6\cdot(1-0.2)\cdot 0.5=0.24.
$$


So a single triple probability is determined mechanically from the three one-variable probabilities.

Two explicit examples anchor the definitions.

Example A (mutual independence). Let $H_1,H_2,H_3$ be three independent fair coin-flip indicators, where $H_i=1$ means heads and $H_i=0$ means tails. Because each flip is fair,

$$
p(H_i=1)=\frac{1}{2},\qquad p(H_i=0)=\frac{1}{2}.
$$


Mutual independence says the probability of any triple is the product of the three one-flip probabilities. For example,

$$
p(H_1=1,H_2=0,H_3=1)=p(H_1=1)p(H_2=0)p(H_3=1)=\frac{1}{2}\cdot\frac{1}{2}\cdot\frac{1}{2}=\frac{1}{8}.
$$


It also implies every subcollection factorizes. For instance,

$$
p(H_1=1,H_2=0)=\frac{1}{4}=\frac{1}{2}\cdot\frac{1}{2}=p(H_1=1)p(H_2=0).
$$


Example B (pairwise independent but not mutually independent). Let $U$ and $V$ be independent fair bits:

$$
p(U=0)=p(U=1)=\frac{1}{2},\qquad p(V=0)=p(V=1)=\frac{1}{2},
$$


and define a third bit

$$
W = U \oplus V,
$$


where $\oplus$ is exclusive-or: $W=1$ when the bits differ and $W=0$ when the bits are equal. The truth table is:

<table align="center">
  <thead>
    <tr><th>$U$</th><th>$V$</th><th>$W = U \oplus V$</th></tr>
  </thead>
  <tbody>
    <tr><td>$0$</td><td>$0$</td><td>$0$</td></tr>
    <tr><td>$0$</td><td>$1$</td><td>$1$</td></tr>
    <tr><td>$1$</td><td>$0$</td><td>$1$</td></tr>
    <tr><td>$1$</td><td>$1$</td><td>$0$</td></tr>
  </tbody>
</table>

Because $(U,V)$ is uniform over its four possibilities, each triple row above occurs with probability $1/4$. So the joint distribution of $(U,V,W)$ is supported on exactly these four states, each with probability $1/4$.

First compute the marginals. For $U$ and $V$, the marginals are still uniform by construction. For $W$, two of the four states have $W=0$ and two have $W=1$, so

$$
p(W=0)=\frac{1}{2},\qquad p(W=1)=\frac{1}{2}.
$$


Now check pairwise independence explicitly.

For the pair $(U,V)$, we have

$$
p(U=0,V=0)=\frac{1}{4}=\frac{1}{2}\cdot\frac{1}{2}=p(U=0)p(V=0),
$$


and the same factorization holds for the other three pairs of values, so $U$ and $V$ are independent.

For the pair $(U,W)$, list the four joint outcomes of $(U,W)$ and their probabilities. From the truth table:

- $(U,W)=(0,0)$ occurs in row $(U,V,W)=(0,0,0)$, so $p(U=0,W=0)=1/4$.
- $(U,W)=(0,1)$ occurs in row $(0,1,1)$, so $p(U=0,W=1)=1/4$.
- $(U,W)=(1,1)$ occurs in row $(1,0,1)$, so $p(U=1,W=1)=1/4$.
- $(U,W)=(1,0)$ occurs in row $(1,1,0)$, so $p(U=1,W=0)=1/4$.

So the $(U,W)$ joint table is

<table align="center">
  <thead>
    <tr><th>$U$</th><th>$W$</th><th>$p(U,W)$</th></tr>
  </thead>
  <tbody>
    <tr><td>$0$</td><td>$0$</td><td>$1/4$</td></tr>
    <tr><td>$0$</td><td>$1$</td><td>$1/4$</td></tr>
    <tr><td>$1$</td><td>$0$</td><td>$1/4$</td></tr>
    <tr><td>$1$</td><td>$1$</td><td>$1/4$</td></tr>
  </tbody>
</table>

Since $p(U=u)=1/2$ and $p(W=w)=1/2$, every entry factorizes as

$$
p(U=u,W=w)=\frac{1}{4}=\frac{1}{2}\cdot\frac{1}{2}=p(U=u)p(W=w).
$$


So $U$ and $W$ are independent. By symmetry, the same is true for the pair $(V,W)$. Therefore $(U,V,W)$ are pairwise independent.

However, they are not mutually independent, because the triple distribution does not factorize. For example,

$$
p(U=0,V=0,W=0)=\frac{1}{4},
$$


but the product of marginals would be

$$
p(U=0)p(V=0)p(W=0)=\frac{1}{2}\cdot\frac{1}{2}\cdot\frac{1}{2}=\frac{1}{8}.
$$


So the equality required by mutual independence fails. The structural reason is that $W$ is a deterministic function of $(U,V)$: once you know $U$ and $V$, the value of $W$ is forced. This creates a three-way constraint that is invisible to any single pairwise marginal.

There is an even sharper way to state what went wrong. Example A (three independent fair bits) and Example B (the XOR construction) have the same pairwise distributions: every pair is uniform over its four outcomes and therefore looks completely independent. So if you only ever inspect two-variable tables, you cannot tell these two very different three-variable models apart. The difference lives entirely in the three-way structure.

Two common wrong notions are worth stating explicitly. First, "pairwise independent" does not mean "no dependence remains." It only rules out dependence that can be detected by looking at any one pair in isolation. Second, pairwise independence is not strong enough to justify multiplying three marginals to get a triple probability. The XOR example is exactly the case in which that intuition fails.

### Conditional Independence

It is rare for variables to be completely independent, but they are often conditionally independent given a mediating variable $Z$:

$$
p(X=x,Y=y \mid Z=z) = p(X=x \mid Z=z)p(Y=y \mid Z=z)
$$


for every triple of values $(x,y,z)$ with $p(Z=z)>0$.

Once $Z$ is known, $X$ and $Y$ stop giving extra information about each other.

A good way to read this is as a statement about information flow. Before conditioning, $X$ and $Y$ may be correlated because they both respond to the hidden cause $Z$. After conditioning on $Z$, that common cause has been fixed, so the leftover association disappears. Conditional independence is therefore weaker than independence in general but often much more realistic in structured probabilistic models.

An explicit numeric check shows what the factorization means mechanically. In the dentist model, let $Z=C$ (cavity), $X=T$ (toothache), and $Y=D$ (probe catch). The model claims

$$
p(T,D \mid C)=p(T \mid C)p(D \mid C).
$$


To check one entry, compute the left-hand side for the case $T=1$, $D=1$, and $C=1$ using the joint table:

$$
p(T=1,D=1 \mid C=1)=\frac{p(T=1,D=1,C=1)}{p(C=1)}=\frac{0.108}{0.20}=0.54.
$$


Now compute the two right-hand-side factors. From the same model,

$$
p(T=1 \mid C=1)=0.6,\qquad p(D=1 \mid C=1)=0.9.
$$


So the factorized right-hand side is

$$
p(T=1 \mid C=1)p(D=1 \mid C=1)=0.6\cdot 0.9=0.54,
$$


which matches the left-hand side exactly. A similar calculation holds for $C=0$:

$$
p(T=1,D=1 \mid C=0)=\frac{0.016}{0.80}=0.02,\qquad p(T=1 \mid C=0)p(D=1 \mid C=0)=0.1\cdot 0.2=0.02.
$$


This is the core meaning of conditional independence: once $C$ is fixed, the toothache information is already accounted for, so it does not further change the distribution of the probe outcome.

<p align="center">
  <img src="../notes/02_probability_reconstructed/assets/figure_2_conditional_independence_structures.png" alt="Common-cause and explaining-away structures" width="860">
</p>

### Example 2-8: Conditional Independence, Dentist

The dentist model is the cleanest place to see the difference between:

- marginal dependence (two variables are associated when we do *not* condition), and
- conditional independence (the association disappears once we condition on a third variable).

In this model, $T$ (toothache) and $D$ (probe catch) are not independent in general, because both are influenced by the hidden cause $C$ (cavity). But they *are* conditionally independent given $C$. Formally, the claim is

$$
D \perp T \mid C.
$$


There are two equivalent ways to read this statement, and it helps to see both.

Definition via factorization. Conditional independence means that for every cavity value $c$ with $p(C=c)>0$,

$$
p(D,T \mid C=c)=p(D \mid C=c)\,p(T \mid C=c).
$$


Definition via “conditioning adds no extra information.” The same claim can be written as: for every $c,t$ with $p(C=c,T=t)>0$,

$$
p(D \mid C=c,T=t)=p(D \mid C=c).
$$


So once we fix $C$, learning $T$ does not further change the distribution of $D$.

Before showing the conditional-independence check, it is worth confirming that $T$ and $D$ are in fact dependent marginally. Using the joint table from Example 2-4:

$$
p(D=1 \mid T=1)=\frac{p(D=1,T=1)}{p(T=1)}=\frac{0.016+0.108}{0.20}=\frac{0.124}{0.20}=0.62,
$$


while

$$
p(D=1 \mid T=0)=\frac{p(D=1,T=0)}{p(T=0)}=\frac{0.144+0.072}{0.80}=\frac{0.216}{0.80}=0.27.
$$


These are different, so $D$ and $T$ are *not* independent.

Now check the conditional-independence claim. The most direct mechanical check is to compute $p(D \mid C,T)$ from the joint table and see whether it depends on $T$. The conditional table is:

<table align="center">
  <thead>
    <tr><th>$T$</th><th>$D$</th><th>$C$</th><th>$p(D \mid C,T)$</th></tr>
  </thead>
  <tbody>
    <tr><td>$0$</td><td>$0$</td><td>$0$</td><td>$0.800$</td></tr>
    <tr><td>$0$</td><td>$0$</td><td>$1$</td><td>$0.100$</td></tr>
    <tr><td>$0$</td><td>$1$</td><td>$0$</td><td>$0.200$</td></tr>
    <tr><td>$0$</td><td>$1$</td><td>$1$</td><td>$0.900$</td></tr>
    <tr><td>$1$</td><td>$0$</td><td>$0$</td><td>$0.800$</td></tr>
    <tr><td>$1$</td><td>$0$</td><td>$1$</td><td>$0.100$</td></tr>
    <tr><td>$1$</td><td>$1$</td><td>$0$</td><td>$0.200$</td></tr>
    <tr><td>$1$</td><td>$1$</td><td>$1$</td><td>$0.900$</td></tr>
  </tbody>
</table>

The key structural point is that the rightmost column does not actually depend on $T$. But to avoid treating the table as a magic lookup, compute two rows explicitly.

Case 1: cavity present ($C=1$). First compute the denominator probabilities (the mass of the two relevant rows):

$$
p(C=1,T=0)=p(0,0,1)+p(0,1,1)=0.008+0.072=0.080,
$$


$$
p(C=1,T=1)=p(1,0,1)+p(1,1,1)=0.012+0.108=0.120.
$$


Now compute the conditional probe-catch probabilities:

$$
p(D=1 \mid C=1,T=0)=\frac{p(D=1,C=1,T=0)}{p(C=1,T=0)}=\frac{0.072}{0.080}=0.9,
$$


$$
p(D=1 \mid C=1,T=1)=\frac{p(D=1,C=1,T=1)}{p(C=1,T=1)}=\frac{0.108}{0.120}=0.9.
$$


So once we fix $C=1$, the probability of $D=1$ is $0.9$ regardless of the toothache value.

Case 2: no cavity ($C=0$). Repeat the same computation:

$$
p(C=0,T=0)=p(0,0,0)+p(0,1,0)=0.576+0.144=0.720,
$$


$$
p(C=0,T=1)=p(1,0,0)+p(1,1,0)=0.064+0.016=0.080.
$$


Then

$$
p(D=1 \mid C=0,T=0)=\frac{0.144}{0.720}=0.2,\qquad p(D=1 \mid C=0,T=1)=\frac{0.016}{0.080}=0.2.
$$


Again, after fixing $C$, the distribution of $D$ does not depend on $T$.

So once the cavity variable is fixed, knowing the toothache value adds no further information about the probe outcome. That is precisely what conditional independence means in this example.

Two easy wrong notions are worth ruling out explicitly.

First, conditional independence is not the same as independence. Here $D$ and $T$ are dependent marginally (we computed $0.62$ versus $0.27$), but conditionally independent once we fix $C$. The dependence exists because mixing over the unknown $C$ value creates association.

Second, conditional independence does not mean that $D$ and $T$ are unrelated in the real world. It means that in the model, any relationship between them is fully explained by the mediating variable $C$. If the model is missing a cause that affects both $D$ and $T$, then the conditional-independence claim may be false in reality even if it holds in a simplified model.

### Worked Example: Auto Warning Light

The conditional-independence ideas above show up immediately in diagnostic models. This worked example also introduces a second important phenomenon: *conditioning on a shared effect can create dependence between causes*, which is the pattern called explaining away.

To avoid confusing the coolant variable with the cavity variable $C$ used earlier, we use $L$ for "low coolant." Define three binary variables:

- $H=1$ means the engine is too hot (a possible cause)
- $L=1$ means the coolant level is too low (another possible cause)
- $W=1$ means the warning light is on (an observed effect)

Step 1: specify the priors. Assume

$$
p(H=1)=0.1,\qquad p(L=1)=0.1,
$$


so

$$
p(H=0)=0.9,\qquad p(L=0)=0.9.
$$


Assume the two causes are independent *before* we observe anything:

$$
H \perp L \qquad \Longleftrightarrow \qquad p(H,L)=p(H)p(L).
$$


Step 2: specify the sensor model. The warning light is a noisy sensor whose behavior depends on which hidden causes are present. Suppose

$$
p(W=1 \mid H=0,L=0)=0.1,
$$


$$
p(W=1 \mid H=1,L=0)=0.8,\qquad p(W=1 \mid H=0,L=1)=0.8,
$$


$$
p(W=1 \mid H=1,L=1)=0.9.
$$


These numbers encode the idea "either problem tends to trigger the light; both problems together trigger it even more reliably; but the light can also turn on by accident."

Step 3: compute the prior joint over the causes. Because we assumed $H \perp L$,

$$
p(H=h,L=l)=p(H=h)p(L=l).
$$


So the four prior joint probabilities are:

$$
p(H=0,L=0)=0.9\cdot 0.9=0.81,
$$


$$
p(H=0,L=1)=0.9\cdot 0.1=0.09,
$$


$$
p(H=1,L=0)=0.1\cdot 0.9=0.09,
$$


$$
p(H=1,L=1)=0.1\cdot 0.1=0.01.
$$


Step 4: compute the joint probabilities with $W=1$. The key identity is the product rule:

$$
p(H,L,W=1)=p(W=1 \mid H,L)\,p(H,L)=p(W=1 \mid H,L)\,p(H)\,p(L),
$$


where the last equality uses the independence assumption $p(H,L)=p(H)p(L)$.

Compute each of the four cases explicitly:

$$
p(H=0,L=0,W=1)=0.1\cdot 0.9\cdot 0.9=0.081,
$$


$$
p(H=0,L=1,W=1)=0.8\cdot 0.9\cdot 0.1=0.072,
$$


$$
p(H=1,L=0,W=1)=0.8\cdot 0.1\cdot 0.9=0.072,
$$


$$
p(H=1,L=1,W=1)=0.9\cdot 0.1\cdot 0.1=0.009.
$$


These are summarized here:

<table align="center">
  <thead>
    <tr><th>$H$</th><th>$L$</th><th>$p(H,L)$</th><th>$p(W=1 \mid H,L)$</th><th>$p(H,L,W=1)$</th></tr>
  </thead>
  <tbody>
    <tr><td>$0$</td><td>$0$</td><td>$0.81$</td><td>$0.1$</td><td>$0.081$</td></tr>
    <tr><td>$0$</td><td>$1$</td><td>$0.09$</td><td>$0.8$</td><td>$0.072$</td></tr>
    <tr><td>$1$</td><td>$0$</td><td>$0.09$</td><td>$0.8$</td><td>$0.072$</td></tr>
    <tr><td>$1$</td><td>$1$</td><td>$0.01$</td><td>$0.9$</td><td>$0.009$</td></tr>
  </tbody>
</table>

Step 5: compute the evidence probability $p(W=1)$. Since the four $(H,L)$ cases form a partition,

$$
p(W=1)=\sum_{h,l} p(H=h,L=l,W=1)=0.081+0.072+0.072+0.009=0.234.
$$


Step 6: posterior query 1, probability of low coolant after seeing the warning light. By the definition of conditional probability,

$$
p(L=1 \mid W=1)=\frac{p(L=1,W=1)}{p(W=1)}.
$$


Compute the numerator by summing the two rows with $L=1$:

$$
p(L=1,W=1)=p(H=0,L=1,W=1)+p(H=1,L=1,W=1)=0.072+0.009=0.081.
$$


Therefore

$$
p(L=1 \mid W=1)=\frac{0.081}{0.234}=\frac{9}{26}\approx 0.346.
$$


Interpretation: the warning light increases the coolant-low probability from the prior $0.1$ to about $0.35$.

Step 7: posterior query 2, probability of low coolant after seeing the warning light *and* learning the engine is hot. Again use conditional probability:

$$
p(L=1 \mid W=1,H=1)=\frac{p(L=1,W=1,H=1)}{p(W=1,H=1)}.
$$


The numerator is the single row $(H,L)=(1,1)$:

$$
p(L=1,W=1,H=1)=0.009.
$$


The denominator sums the two rows with $H=1$:

$$
p(W=1,H=1)=p(H=1,L=0,W=1)+p(H=1,L=1,W=1)=0.072+0.009=0.081.
$$


So

$$
p(L=1 \mid W=1,H=1)=\frac{0.009}{0.081}=\frac{1}{9}\approx 0.111.
$$


This value is much smaller than $p(L=1 \mid W=1)\approx 0.346$ because $W=1$ could be explained by either hidden cause. Once we learn $H=1$, the event $W=1$ is no longer strong evidence for $L=1$.

A final computation makes the explaining-away effect even more explicit. If instead we learn that the engine is *not* hot, then

$$
p(L=1 \mid W=1,H=0)=\frac{p(H=0,L=1,W=1)}{p(H=0,W=1)}=\frac{0.072}{0.081+0.072}=\frac{0.072}{0.153}\approx 0.471.
$$


So after observing $W=1$, learning $H=0$ pushes $L$ upward to about $0.47$, while learning $H=1$ pushes $L$ downward to about $0.11$. This is the key structural lesson: $H$ and $L$ are independent in the prior, but after conditioning on their common effect $W=1$, they become dependent.

You can see the dependence-creation cleanly by comparing two conditional probabilities. Before observing $W$, independence means

$$
p(L=1 \mid H=1)=p(L=1)=0.1.
$$


After observing $W=1$, we found

$$
p(L=1 \mid W=1,H=1)\approx 0.111 \qquad \text{and} \qquad p(L=1 \mid W=1,H=0)\approx 0.471.
$$


These are different, so $L$ and $H$ are no longer independent once we condition on the shared effect $W=1$. That is the precise algebraic meaning of explaining away in this example.

### Worked Example: Information Sufficiency for Posterior Queries

Suppose $A$, $B$, and $C$ are binary variables and we want to compute

$$
p(A=1 \mid B=1,C=1).
$$


Bayes' rule exposes the information requirement immediately:

$$
p(A=1 \mid B=1,C=1) = \frac{p(B=1,C=1 \mid A=1)p(A=1)}{p(B=1,C=1)}.
$$


So, with no conditional independence assumptions, three ingredients are needed:

- the prior $p(A=1)$
- the likelihood term $p(B=1,C=1 \mid A=1)$
- the evidence term $p(B=1,C=1)$

That is the cleanest way to judge whether a proposed set of numbers is sufficient. We do not ask whether the numbers "feel related." We ask whether they determine the numerator and denominator in the displayed formula.

Now consider three candidate information sets.

Set 1 gives

$$
p(B=1,C=1),\qquad p(A=1),\qquad p(B=1 \mid A=1),\qquad p(C=1 \mid A=1).
$$


Without further assumptions, this set is not sufficient. The separate conditionals $p(B=1 \mid A=1)$ and $p(C=1 \mid A=1)$ do not determine the joint conditional probability $p(B=1,C=1 \mid A=1)$. Many different joint distributions of $(B,C)$ given $A=1$ can share the same one-variable conditionals.

Set 2 gives

$$
p(B=1,C=1),\qquad p(A=1),\qquad p(B=1,C=1 \mid A=1).
$$


This set is sufficient, because it contains exactly the three ingredients needed by Bayes' rule.

Set 3 gives

$$
p(A=1),\qquad p(B=1 \mid A=1),\qquad p(C=1 \mid A=1).
$$


This set is not sufficient. Even if one somehow recovered the numerator, the denominator $p(B=1,C=1)$ is still missing, so the posterior cannot be normalized.

Now suppose we are also told that

$$
p(B \mid A,C)=p(B \mid A)
$$


for all values of the variables, which is the conditional independence statement

$$
B \perp C \mid A.
$$


Then Set 1 becomes sufficient, because the missing joint conditional factor can now be reconstructed as

$$
p(B=1,C=1 \mid A=1)=p(B=1 \mid A=1)p(C=1 \mid A=1).
$$


Set 2 remains sufficient for the same reason as before: it already contained the full joint conditional term. Set 3 is still not sufficient, because the marginal evidence probability $p(B=1,C=1)$ is still absent. Conditional independence can reduce the amount of information needed to specify a numerator, but it does not make the denominator appear by magic.

### Retain from 2.1

- Probability is defined on events first; random-variable formulas are induced from that event structure.
- Bayes updates can be read either as algebra on conditional probabilities or as the operational sequence restrict, marginalize, normalize.
- Independence means factorization or, equivalently, that conditioning on one variable leaves the other unchanged.
- Conditional independence is weaker than independence and is the key structural simplification behind diagnostic models.

### Do Not Confuse in 2.1

- Do not confuse an event such as $X=x$ with the random variable $X$ itself.
- Do not confuse conditioning with intervention; $p(Y \mid X=x)$ is not automatically a causal statement.
- Do not confuse pairwise independence with mutual independence.
- Do not assume a set of conditional probabilities is sufficient for a posterior unless the required numerator and denominator are actually determined.

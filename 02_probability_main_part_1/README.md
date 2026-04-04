# Probability and Inference (Part 1)

Source: ../notes/02_probability_reconstructed/source/02_probability.pdf

This is Part 1 of the full Chapter 2 main note. It covers the front half of the chapter through Section 2.2. Continue with [Part 2](../02_probability_main_part_2/).

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

## 2.2 Continuous Random Variables

Sometimes we model systems with real-valued random variables $X \in \mathbb{R}$. In that setting we define a probability density function $p(x)$ with $p(x) \ge 0$ for all $x$ and

$$
\int p(x)\,dx = 1.
$$


The density defines the probability of any event $X \in A \subseteq \mathbb{R}$ by

$$
\mathbb{P}(X \in A) = \int_A p(x)\,dx.
$$


This is the first major structural difference from the discrete case. For a continuous variable, the number $p(x)$ is not the probability of the event $X=x$; in fact $\mathbb{P}(X=x)=0$ for every individual point. A density only becomes a probability after integrating it over an interval or region. That is why a density is allowed to exceed one locally, provided the total area under the curve is still one.

A concrete interval computation makes this precise. If $X$ is uniform on $[0,2]$, then $p(x)=1/2$ on that interval. The probability that $X$ falls between $0.3$ and $0.9$ is

$$
\mathbb{P}(0.3 \le X \le 0.9) = \int_{0.3}^{0.9} \frac{1}{2}\,dx = \frac{1}{2}(0.9-0.3)=0.3.
$$


The point $x=0.4$ itself still has probability zero. What matters is the width of the interval, not the existence of an individual point.

### CDFs and Types of Distributions

The cumulative distribution function, or CDF, is the most universal way to describe a real-valued random variable:

$$
F_X(x)=\mathbb{P}(X \le x).
$$


This definition should be read operationally. You pick a threshold $x$, ask for the event "the realized value of $X$ is at most that threshold," and then assign the probability of that event. So a CDF is not a density curve and not a table of point masses. It is the running total of probability mass accumulated from the far left up to the cutoff value $x$.

That running-total viewpoint explains why the CDF is so general. Every real-valued random variable has events of the form $X \le x$, so every real-valued random variable has a CDF. By contrast, PMFs and PDFs exist only in special settings:

<table align="center">
  <thead>
    <tr><th>object</th><th>definition</th><th>when it exists</th><th>how to read it</th></tr>
  </thead>
  <tbody>
    <tr><td>$\mathrm{PMF}$</td><td>$p(X=x)=\mathbb{P}(X=x)$</td><td>discrete variables</td><td>probability assigned to one exact state</td></tr>
    <tr><td>$\mathrm{PDF}$</td><td>$\mathbb{P}(X \in A)=\int_A p(x)\,dx$</td><td>absolutely continuous variables</td><td>density height; probability comes from area, not point value</td></tr>
    <tr><td>$\mathrm{CDF}$</td><td>$F_X(x)=\mathbb{P}(X \le x)$</td><td>every real-valued variable</td><td>total probability accumulated up to threshold $x$</td></tr>
  </tbody>
</table>

The safest mental model is:

- a PMF answers "what is the probability of this exact isolated state?"
- a PDF answers "how densely is probability packed near this location?"
- a CDF answers "how much total probability lies to the left of this threshold?"

Several structural facts follow directly from the definition of a CDF.

First, $F_X(x)$ must always lie between $0$ and $1$ because it is a probability.

Second, $F_X(x)$ is nondecreasing: if $x_1 \le x_2$, then the event $\{X \le x_1\}$ is contained inside the event $\{X \le x_2\}$, so

$$
F_X(x_1)\le F_X(x_2).
$$


Third, the far-left limit is $0$ and the far-right limit is $1$:

$$
\lim_{x\to -\infty} F_X(x)=0,\qquad \lim_{x\to \infty} F_X(x)=1.
$$


Fourth, a CDF is right-continuous, meaning

$$
\lim_{h \downarrow 0} F_X(x+h)=F_X(x).
$$


This matters because CDFs can have jumps. When a variable has positive point mass at a value $x$, the CDF jumps upward at that exact location, and the value $F_X(x)$ already includes the mass sitting at $x$. So a CDF always starts near $0$, climbs as probability accumulates, and eventually levels off at $1$.

One more operational formula is worth stating early because it is how CDFs are actually used:

$$
\mathbb{P}(a < X \le b)=F_X(b)-F_X(a).
$$


This works because the event $\{X \le b\}$ contains all mass up to $b$, while $\{X \le a\}$ contains all mass up to $a$. Subtracting removes the left part and leaves only the probability in the interval $(a,b]$. This formula is valid whether the variable is discrete, continuous, or mixed.

Now examine the three main types of distributions one by one.

Discrete case. Suppose $X$ is Bernoulli with

$$
p(X=1)=0.3,\qquad p(X=0)=0.7.
$$


Then the CDF is obtained by asking what probability has accumulated by each threshold.

If $x<0$, then neither state $0$ nor state $1$ is less than or equal to $x$, so

$$
F_X(x)=0.
$$


If $0 \le x < 1$, then the state $0$ is included but the state $1$ is not, so

$$
F_X(x)=\mathbb{P}(X=0)=0.7.
$$


If $x \ge 1$, then both states are included, so

$$
F_X(x)=\mathbb{P}(X=0)+\mathbb{P}(X=1)=1.
$$


That gives the step-function description:

<table align="center">
  <thead>
    <tr><th>$F_X(x)$</th><th>condition on $x$</th></tr>
  </thead>
  <tbody>
    <tr><td>$0$</td><td>$x<0$</td></tr>
    <tr><td>$0.7$</td><td>$0 \le x < 1$</td></tr>
    <tr><td>$1$</td><td>$x \ge 1$</td></tr>
  </tbody>
</table>

The jump at $x=0$ has size $0.7$, which is exactly the point mass at $0$. The jump at $x=1$ adds the remaining $0.3$, which is exactly the point mass at $1$. This is the general rule in the discrete case: jumps in the CDF correspond to point probabilities.

An interval example makes the subtraction rule concrete. For the Bernoulli variable above,

$$
\mathbb{P}(0 < X \le 1)=F_X(1)-F_X(0)=1-0.7=0.3,
$$


which is exactly the probability that $X=1$.

Continuous case. Now suppose $X$ is uniform on $[0,2]$, so the density is

<table align="center">
  <thead>
    <tr><th>$p(x)$</th><th>condition on $x$</th></tr>
  </thead>
  <tbody>
    <tr><td>$1/2$</td><td>$0 \le x \le 2$</td></tr>
    <tr><td>$0$</td><td>otherwise</td></tr>
  </tbody>
</table>

The CDF is found by integrating the density from the far left up to the threshold.

If $x<0$, then no support has been reached yet, so

$$
F_X(x)=0.
$$


If $0 \le x \le 2$, then we integrate only over the part of the support from $0$ to $x$:

$$
F_X(x)=\int_0^x \frac{1}{2}\,dt=\frac{x}{2}.
$$


If $x>2$, then the full support has already been accumulated, so

$$
F_X(x)=1.
$$


So

<table align="center">
  <thead>
    <tr><th>$F_X(x)$</th><th>condition on $x$</th></tr>
  </thead>
  <tbody>
    <tr><td>$0$</td><td>$x<0$</td></tr>
    <tr><td>$x/2$</td><td>$0 \le x \le 2$</td></tr>
    <tr><td>$1$</td><td>$x>2$</td></tr>
  </tbody>
</table>

Unlike the discrete Bernoulli example, this CDF has no jumps. It rises smoothly because probability is spread continuously across an interval rather than concentrated at isolated points.

The interval-probability formula still works the same way:

$$
\mathbb{P}(0.3 \le X \le 0.9)=F_X(0.9)-F_X(0.3)=0.45-0.15=0.30.
$$


So the CDF is not a separate theory from the PDF. It is another way of packaging the same distribution. When a density exists and is sufficiently regular, the derivative of the CDF recovers the density:

$$
\frac{d}{dx}F_X(x)=p(x)
$$


at points where that derivative exists.

Mixed case. This distinction matters because not every distribution is purely discrete or purely continuous. A mixed distribution contains both an atom and a continuous part. For example, suppose

$$
\mathbb{P}(X=0)=0.7,
$$


and with the remaining probability $0.3$ we draw $X$ uniformly from $[0,1]$.

Now compute the CDF carefully.

If $x<0$, then no mass has been accumulated:

$$
F_X(x)=0.
$$


At the exact point $x=0$, the atom at zero is included, so

$$
F_X(0)=0.7.
$$


If $0<x<1$, then we have already collected the point mass $0.7$, and we also collect the fraction of the continuous part that lies in $[0,x]$. Since that continuous part is uniform on $[0,1]$ and has total weight $0.3$, the additional contribution is $0.3x$. Therefore

$$
F_X(x)=0.7+0.3x \qquad \text{for } 0<x<1.
$$


Finally, if $x \ge 1$, all probability has been accumulated, so

$$
F_X(x)=1.
$$


So the mixed-distribution CDF is

<table align="center">
  <thead>
    <tr><th>$F_X(x)$</th><th>condition on $x$</th></tr>
  </thead>
  <tbody>
    <tr><td>$0$</td><td>$x<0$</td></tr>
    <tr><td>$0.7$</td><td>$x=0$</td></tr>
    <tr><td>$0.7 + 0.3x$</td><td>$0<x<1$</td></tr>
    <tr><td>$1$</td><td>$x \ge 1$</td></tr>
  </tbody>
</table>

This example is important because it shows exactly why the CDF is the most universal description. A PMF alone would miss the continuous part. A PDF alone would miss the atom at zero. The CDF captures both with one object: jumps record point masses, and smooth increases record continuous accumulation.

Two common confusions are worth ruling out explicitly.

First, $F_X(x)$ is not the same thing as $p(x)$. The CDF is a probability between $0$ and $1$, while the PDF is a density value that may exceed $1$ locally.

Second, $\mathbb{P}(X=x)=0$ for a continuous variable does not mean the value $x$ is impossible. It means only that a single point has zero width, so it contributes zero area under the density. Intervals, not isolated points, carry positive probability in the continuous case.

### Example 2-9: Uniform Distribution

The word uniform needs to be interpreted carefully in the continuous setting. It does **not** mean that each individual point has the same positive probability, because every single point has probability zero for a continuous variable. Instead, it means that the density is constant across the allowed interval, so intervals of the same length receive the same probability mass.

Suppose $X$ is known to lie somewhere between $0$ and $T$, and suppose we want a model that treats all locations inside that interval symmetrically. The natural way to express that idea is to assign one constant density value on the whole interval and zero density outside it. So we write

<table align="center">
  <thead>
    <tr><th>support condition for $x$</th><th>$p(x)$</th></tr>
  </thead>
  <tbody>
    <tr><td>$x \in [0,T]$</td><td>$c$</td></tr>
    <tr><td>otherwise</td><td>$0$</td></tr>
  </tbody>
</table>

The constant $c$ cannot be chosen arbitrarily. A density must integrate to $1$, so we impose the normalization condition

$$
\int_{-\infty}^{\infty} p(x)\,dx = 1.
$$


Because $p(x)=0$ outside $[0,T]$, this reduces to

$$
\int_0^T c\,dx = 1.
$$


Now compute the integral:

$$
c \int_0^T 1\,dx = cT = 1.
$$


Therefore

$$
c=\frac{1}{T}.
$$


So the uniform density on $[0,T]$ is

<table align="center">
  <thead>
    <tr><th>support condition for $x$</th><th>$p(x)$</th></tr>
  </thead>
  <tbody>
    <tr><td>$x \in [0,T]$</td><td>$1/T$</td></tr>
    <tr><td>otherwise</td><td>$0$</td></tr>
  </tbody>
</table>

This formula says two things at once. First, the support of the distribution is the interval $[0,T]$: values outside that interval are impossible under the model because their density is zero. Second, inside the interval the density is flat, so no region is favored over any other region of the same length.

The normalization check is now immediate:

$$
\int_0^T p(x)\,dx = T \cdot \frac{1}{T} = 1.
$$


The most important operational consequence is that probability depends only on interval length. If $0 \le a \le b \le T$, then

$$
\mathbb{P}(a \le X \le b)=\int_a^b \frac{1}{T}\,dx=\frac{b-a}{T}.
$$


So under a uniform model:

- an interval of length $0.1T$ has probability $0.1$,
- an interval of length $0.25T$ has probability $0.25$,
- and two intervals with the same length always have the same probability, no matter where they sit inside $[0,T]$.

This is the precise mathematical meaning of "uniform."

A concrete example makes the geometry clearer. Suppose $X \sim \mathrm{Unif}[0,10]$. Then

$$
p(x)=\frac{1}{10}\qquad \text{for } 0 \le x \le 10.
$$


Now compute a few interval probabilities:

$$
\mathbb{P}(2 \le X \le 5)=\int_2^5 \frac{1}{10}\,dx=\frac{5-2}{10}=0.3,
$$


$$
\mathbb{P}(7 \le X \le 8)=\int_7^8 \frac{1}{10}\,dx=\frac{8-7}{10}=0.1.
$$


The first interval is three times as long as the second, so it has three times as much probability. Location does not matter; length does.

This also clarifies why point probabilities vanish. Even though the density is positive at every point of $[0,T]$, we still have

$$
\mathbb{P}(X=4)=0,
$$


because a single point has zero width and therefore contributes zero area under the density.

Unlike discrete distributions, the density value itself may be larger than one, as long as the total area under the curve is one. The object that must equal one is the integral, not the height of the graph.

For example, if $X$ is uniform on the very short interval $[0,0.2]$, then

$$
p(x)=5
$$


on that interval. The density value exceeds one, but the total probability is still

$$
\int_0^{0.2} 5\,dx = 1.
$$


So there is no contradiction between a large density and a valid probability model. The interval is very short, so the density must be tall in order for the total area to remain one.

One structural limit should also be stated explicitly: a continuous uniform distribution must live on a **finite-length** interval if we want a constant density. There is no valid density that is "uniform over the entire real line," because no positive constant can integrate to one over an infinite interval. So the uniform model is appropriate when the possible values are bounded and all equal-length subintervals are meant to be treated symmetrically.

### Gaussian Distributions

The Gaussian distribution is one of the most important continuous families because it appears whenever many small effects combine, whenever measurement noise is modeled, and whenever we want a smooth bell-shaped distribution controlled by a center and a spread.

Before writing the formula, it helps to say what kind of object we are describing. A one-dimensional Gaussian is a continuous distribution on the whole real line. So:

- the variable can in principle take any real value $x \in \mathbb{R}$,
- single points still have probability zero,
- and probabilities come from integrating the density over intervals.

What makes the Gaussian special is its shape: it is symmetric around a central value, highest at the center, and decreases smoothly as we move away from that center.

In one dimension, the density is

$$
p(x) = \mathcal{N}(x;\mu,\sigma^2) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right).
$$


Every symbol should be read explicitly:

- $x$ is the location where we evaluate the density,
- $\mu$ is the mean, which sets the center of the bell curve,
- $\sigma^2$ is the variance, which measures spread,
- $\sigma$ is the standard deviation, so $\sigma=\sqrt{\sigma^2}$,
- the prefactor $\frac{1}{\sqrt{2\pi\sigma^2}}$ is the normalization constant,
- and the exponential term controls how fast the density decays as $x$ moves away from $\mu$.

The formula becomes much easier to interpret if we read the exponent first:

$$
-\frac{(x-\mu)^2}{2\sigma^2}.
$$


The numerator $(x-\mu)^2$ is the squared distance from $x$ to the mean. So the farther $x$ is from $\mu$, the more negative the exponent becomes, and the smaller the density becomes. The denominator $2\sigma^2$ controls how quickly that decay happens. Large $\sigma^2$ means the penalty for being far from the mean is weaker, so the curve is wider. Small $\sigma^2$ means the penalty is stronger, so the curve is narrower.

Three basic facts follow immediately from the formula.

First, the density is symmetric around $\mu$, because replacing $(x-\mu)$ by $-(x-\mu)$ does not change the square:

$$
p(\mu+a)=p(\mu-a).
$$


Second, the density is largest at $x=\mu$, because that is where the squared term is smallest, namely zero:

$$
p(\mu)=\frac{1}{\sqrt{2\pi\sigma^2}}.
$$


Third, two values that are the same number of standard deviations away from the mean have the same density. This is easiest to see by standardizing:

$$
z=\frac{x-\mu}{\sigma}.
$$


Then the exponent becomes $-z^2/2$, so the Gaussian really depends on distance from the mean measured in standard-deviation units.

It is also important not to misread the density value. Even though $p(\mu)$ is the highest point on the curve, it is **not** the probability that $X=\mu$. For a continuous Gaussian,

$$
\mathbb{P}(X=\mu)=0.
$$


The height of the curve tells us relative density, not point probability.

A full one-dimensional example makes the parameters concrete. Suppose

$$
X \sim \mathcal{N}(2,9).
$$


Then

- the mean is $\mu=2$,
- the variance is $\sigma^2=9$,
- and the standard deviation is $\sigma=3$.

So the curve is centered at $2$, and one standard deviation corresponds to moving $3$ units left or right. The interval within one standard deviation of the mean is therefore

$$
[\mu-\sigma,\mu+\sigma]=[2-3,2+3]=[-1,5].
$$


For a Gaussian, about $68\%$ of the total probability lies in that interval. About $95\%$ lies within two standard deviations, namely in

$$
[2-6,2+6]=[-4,8],
$$


and about $99.7\%$ lies within three standard deviations, namely in

$$
[2-9,2+9]=[-7,11].
$$


These are approximation rules rather than exact identities, but they are fundamental for intuition. They say that the standard deviation is not just an abstract parameter; it gives a direct spatial scale for where most of the probability mass sits.

The normalization constant also deserves a brief explanation. The exponential term by itself gives the bell shape, but it does not automatically integrate to one. The factor

$$
\frac{1}{\sqrt{2\pi\sigma^2}}
$$


rescales the curve so that the total area under it over the whole real line is exactly one:

$$
\int_{-\infty}^{\infty} p(x)\,dx=1.
$$


So the Gaussian formula should be read as "bell-shaped decay" multiplied by "whatever constant is needed to make this a valid density."

Before moving to the multivariate case, it helps to say what actually changes.

In one dimension, the random outcome is a single number such as a height, temperature, or measurement error. In multiple dimensions, the random outcome is a list of numbers observed together. For example, one observation might be the two-dimensional vector $x=(x_1,x_2)^T$, where $x_1$ is height and $x_2$ is weight. Or it might be the three-dimensional vector $x=(x_1,x_2,x_3)^T$, where the coordinates are exam 1, exam 2, and exam 3.

So a multivariate random variable is really a random vector: one draw produces several coordinates at once.

The mean therefore becomes a mean vector

$$
\mu=\mathbb{E}[X]=(\mathbb{E}[X_1],\ldots,\mathbb{E}[X_n])^T.
$$


This means each coordinate has its own average value. In two dimensions, for example,

$$
\mu=(\mu_1,\mu_2)^T
$$


simply says the cloud of points is centered at horizontal coordinate $\mu_1$ and vertical coordinate $\mu_2$.

The next new object is the covariance matrix. Before giving its formula, it helps to say what problem it solves. In one dimension, one variance number was enough to describe spread. In several dimensions, that is no longer sufficient, because we must describe

- how much each coordinate varies on its own;
- and how pairs of coordinates move together.

The covariance matrix collects both kinds of information into one table. Its entry in row $i$ and column $j$ is

$$
\Sigma_{ij}=\mathrm{Cov}(X_i,X_j).
$$


So the diagonal entries are variances, and the off-diagonal entries are covariances between different coordinates.

So the diagonal entries are ordinary variances:

$$
\Sigma_{11}=\mathrm{Var}(X_1), \qquad \Sigma_{22}=\mathrm{Var}(X_2), \qquad \text{and so on.}
$$


The off-diagonal entries are covariances:

$$
\Sigma_{12}=\mathrm{Cov}(X_1,X_2).
$$


Those covariances answer a new question that does not exist in one dimension: when one coordinate is above its mean, does the other coordinate also tend to be above its mean, below its mean, or unrelated?

It helps to make that concrete before introducing the multivariate Gaussian formula.

- If $\Sigma_{12}>0$, the two coordinates tend to move together. Large values of one coordinate tend to appear with large values of the other.
- If $\Sigma_{12}<0$, the two coordinates tend to move in opposite directions. Large values of one coordinate tend to appear with small values of the other.
- If $\Sigma_{12}=0$, there is no linear covariance between the coordinates.

An explicit $2 \times 2$ example makes the matrix readable. Suppose

$$
\Sigma_{11}=4, \qquad \Sigma_{22}=1, \qquad \Sigma_{12}=\Sigma_{21}=0.
$$


Then

- the first coordinate has variance $4$, so its standard deviation is $2$;
- the second coordinate has variance $1$, so its standard deviation is $1$;
- and the zero off-diagonal terms say there is no linear covariance between the two coordinates.

So a cloud with this covariance matrix is spread out more in the first direction than in the second. Even before seeing the multivariate Gaussian formula, that tells us the equal-density contours should be stretched horizontally more than vertically.

Now consider

$$
\Sigma_{11}=1, \qquad \Sigma_{22}=1, \qquad \Sigma_{12}=\Sigma_{21}=0.8.
$$


The diagonal entries still say each coordinate has variance $1$, but now the positive off-diagonal entries say the coordinates tend to move together. So the cloud is no longer aligned with the coordinate axes. It is elongated along a diagonal direction. That is the geometric meaning of covariance in the Gaussian setting.

Only after those objects are clear does the multivariate formula become readable.

If $X$ is an $n$-dimensional Gaussian random vector, then its density is

$$
p(x) = \mathcal{N}(x;\mu,\Sigma) = (2\pi)^{-n/2} |\Sigma|^{-1/2} \exp\left(-\frac{1}{2}(x-\mu)^T \Sigma^{-1}(x-\mu)\right).
$$


Every object now has a specific role:

- $x$ is now an $n$-dimensional vector,
- $\mu$ is the mean vector, which sets the center of the cloud,
- $\Sigma$ is the covariance matrix, which sets spread and dependence,
- $|\Sigma|$ is the determinant of the covariance matrix, meaning the single number that records how covariance rescales local volume,
- and the quadratic term

$$
(x-\mu)^T \Sigma^{-1}(x-\mu)
$$

is the squared Mahalanobis distance from $x$ to the mean.

Mahalanobis distance means distance measured in the geometry of the covariance structure rather than ordinary Euclidean distance. This phrase is easy to state and easy to leave opaque, so spell it out.

In ordinary Euclidean distance, moving one unit horizontally and moving one unit vertically are treated the same way. In Mahalanobis distance, the covariance matrix tells us which directions are naturally more variable. If a direction has large variance, then moving in that direction is less surprising, so the density decays more slowly there. If a direction has small variance, moving the same Euclidean amount is more surprising, so the density decays more quickly there.

So the multivariate Gaussian is still doing exactly what the one-dimensional Gaussian did: it penalizes distance from the mean. The only difference is that in several dimensions, "distance" must now respect the spread and dependence encoded by $\Sigma$.

One explicit diagonal example keeps the matrix notation grounded. If

$$
\Sigma_{11}=\sigma_1^2, \qquad \Sigma_{22}=\sigma_2^2, \qquad \Sigma_{12}=\Sigma_{21}=0,
$$


then

$$
\Sigma^{-1}_{11}=1/\sigma_1^2, \qquad \Sigma^{-1}_{22}=1/\sigma_2^2, \qquad \Sigma^{-1}_{12}=\Sigma^{-1}_{21}=0,
$$


so the quadratic term becomes

$$
(x-\mu)^T\Sigma^{-1}(x-\mu)=\frac{(x_1-\mu_1)^2}{\sigma_1^2}+\frac{(x_2-\mu_2)^2}{\sigma_2^2}.
$$

This is the direct multivariate analogue of the one-dimensional Gaussian penalty. Each coordinate contributes its own squared deviation, scaled by its own variance. Off-diagonal covariance terms are what introduce cross-terms and rotate the geometry away from this axis-aligned form.

In two dimensions, the sets of points with equal density are ellipses. In higher dimensions, they are ellipsoids. So the multivariate Gaussian is still a bell-shaped distribution, but now the bell can be stretched, compressed, and rotated.

The covariance matrix $\Sigma$ therefore contains two kinds of information:

- diagonal entries such as $\Sigma_{11}$ and $\Sigma_{22}$ are variances of individual coordinates,
- off-diagonal entries such as $\Sigma_{12}$ are covariances that describe how coordinates move together.

For this formula to define a proper density, $\Sigma$ must be symmetric and positive definite. Each condition matters:

- symmetric means $\Sigma_{ij}=\Sigma_{ji}$, which is required of covariance matrices,
- positive definite means $v^T\Sigma v > 0$ for every nonzero vector $v$,
- that guarantees the inverse $\Sigma^{-1}$ exists,
- and it guarantees the quadratic form is positive, so the exponential decays rather than exploding.

<p align="center">
  <img src="../notes/02_probability_reconstructed/assets/figure_2_1_gaussian.png" alt="Gaussian distribution plots" width="860">
</p>

The three panels show the same family viewed three ways. The one-dimensional curve emphasizes how the mean shifts location and the standard deviation changes spread. The surface plot shows the bivariate density as height over the plane. The contour plot removes the height dimension and keeps only level sets, which is often the most useful representation when reasoning about covariance structure.

A concrete one-dimensional example is

$$
X \sim \mathcal{N}(2, 9),
$$


so the mean is $2$ and the standard deviation is $3$. About two-thirds of the mass lies within one standard deviation of the mean, namely in the interval $[-1,5]$, and almost all of the mass lies within a few standard deviations.

Now move to two dimensions very concretely. If

$$
\mu=(0,0)^T, \qquad \Sigma_{11}=4,\qquad \Sigma_{22}=1,\qquad \Sigma_{12}=\Sigma_{21}=0,
$$


then the mean vector says the cloud is centered at the origin, the first coordinate has variance $4$, and the second coordinate has variance $1$. So the spread in the first direction is larger than the spread in the second direction. That is why the contours are ellipses stretched more strongly along the first coordinate than along the second.

Because the off-diagonal terms are zero in this example, there is no rotational tilt. The **principal axes** of the ellipse, meaning the main directions along which the cloud is stretched, line up with the coordinate axes.

Now change only the off-diagonal entries. Let $\Sigma$ be the $2\times 2$ covariance matrix with

$$
\Sigma_{11}=1,\qquad \Sigma_{22}=1,\qquad \Sigma_{12}=\Sigma_{21}=0.8.
$$


The correlation coefficient between coordinates is

$$
\mathrm{Corr}(X_1,X_2)=\frac{\Sigma_{12}}{\sqrt{\Sigma_{11}\Sigma_{22}}}=\frac{0.8}{\sqrt{1\cdot 1}}=0.8.
$$


This means the two coordinates tend to move together. So large values of $X_1$ tend to appear with large values of $X_2$, and small values of $X_1$ tend to appear with small values of $X_2$. Geometrically, the Gaussian contours are elongated along the diagonal direction

$$
x_1 \approx x_2.
$$


So the correct mental build-up is:

1. one-dimensional Gaussian: center plus spread;
2. random vector: several coordinates observed together;
3. mean vector: center of the cloud in multiple coordinates;
4. covariance matrix: individual spreads plus how coordinates move together;
5. multivariate Gaussian density: the same bell-shaped idea, but now in the geometry determined by that covariance matrix.

If instead $\Sigma_{12}$ were negative, then large values of one coordinate would tend to appear with small values of the other, and the elongation would run along

$$
x_1 \approx -x_2.
$$


This is the geometric meaning of off-diagonal covariance: it couples the coordinates and rotates the main stretching directions of the density away from the coordinate axes.

The main mastery-level takeaway is that a Gaussian is not just "the bell curve formula." It is a model whose parameters have direct geometric meaning:

- the mean says where the mass is centered,
- the variance says how widely the mass is spread,
- and the covariance matrix says how the cloud is stretched and rotated in multiple dimensions.

That is why Gaussians appear everywhere in probability, statistics, and AI. They are mathematically tractable, but they are also unusually interpretable.

### Example 2-10: Bernoulli Exponential Family Form

This example is not introducing a new distribution. It is taking the ordinary Bernoulli model and rewriting it in a form whose algebra will reappear throughout statistics and machine learning.

Start with a Bernoulli random variable $X \in \{0,1\}$ and parameter

$$
\rho = \mathbb{P}(X=1).
$$


Then automatically

$$
\mathbb{P}(X=0)=1-\rho.
$$


The Bernoulli PMF can be written compactly as

$$
p(X=x)=\rho^x(1-\rho)^{1-x}, \qquad x \in \{0,1\}.
$$


This notation is worth unpacking slowly because it is easy to read it too quickly. If $x=1$, then

$$
p(X=1)=\rho^1(1-\rho)^0=\rho.
$$


If $x=0$, then

$$
p(X=0)=\rho^0(1-\rho)^1=1-\rho.
$$


So the exponents do not encode new probabilities. They are indicator exponents: they switch on the factor corresponding to the realized state and switch off the other one.

Now rewrite the same expression using logarithms:

$$
p(X=x)=\exp\left(\log(\rho)x+\log(1-\rho)(1-x)\right).
$$


Expand the exponent:

$$
\log(\rho)x+\log(1-\rho)(1-x)=x\log\left(\frac{\rho}{1-\rho}\right)+\log(1-\rho).
$$


This suggests defining the natural parameter

$$
\eta=\log\left(\frac{\rho}{1-\rho}\right).
$$


That quantity is the log-odds. It is not itself a probability. It ranges over the whole real line, whereas $\rho$ is restricted to the interval $(0,1)$.

Solve this definition for $\rho$:

$$
e^{\eta}=\frac{\rho}{1-\rho}.
$$


Multiply both sides by $(1-\rho)$:

$$
e^{\eta}(1-\rho)=\rho.
$$


Collect the $\rho$ terms:

$$
e^{\eta}=\rho(1+e^{\eta}),
$$


so

$$
\rho=\frac{e^{\eta}}{1+e^{\eta}}, \qquad 1-\rho=\frac{1}{1+e^{\eta}}.
$$


Substitute these into the PMF:

$$
p(X=x)=\left(\frac{e^{\eta}}{1+e^{\eta}}\right)^x\left(\frac{1}{1+e^{\eta}}\right)^{1-x}.
$$


Collect powers of $e^{\eta}$ and $(1+e^{\eta})$:

$$
p(X=x)=\frac{e^{\eta x}}{(1+e^{\eta})^{x+(1-x)}}.
$$


The denominator exponent is

$$
x+(1-x)=1,
$$


so the denominator collapses to just one copy of $(1+e^{\eta})$. Therefore

$$
p(X=x)=\frac{e^{\eta x}}{1+e^{\eta}}=\exp(\eta x)\exp\left(-\log(1+e^{\eta})\right).
$$


So the **canonical** exponential-family form, meaning the form written directly in the natural-parameter coordinate $\eta$, is

$$
p(X=x)=\exp\left(\eta x-A(\eta)\right),
$$


where

$$
A(\eta)=\log(1+e^{\eta}).
$$


The conceptual payoff is now visible. The original probability parameter $\rho$ appears nonlinearly in the ordinary Bernoulli formula, but after the reparameterization the observation $x$ appears linearly in the exponent. That is the structural pattern the exponential-family formalism is designed to expose.

A numerical example helps. If $\rho=0.8$, then the odds are $0.8/0.2=4$, so

$$
\eta=\log 4.
$$


Then

$$
A(\eta)=\log(1+e^{\eta})=\log(1+4)=\log 5.
$$


Therefore

$$
p(X=1)=\exp(\eta-A(\eta))=\exp(\log 4-\log 5)=\frac{4}{5}=0.8,
$$


and

$$
p(X=0)=\exp(0-A(\eta))=\exp(-\log 5)=\frac{1}{5}=0.2.
$$


So nothing about the Bernoulli law changed. We only changed coordinates on the parameter. The structural limit is important: this rewrite does not create a richer model. It is still the same one-parameter Bernoulli family, now written in coordinates that are convenient for optimization and theory.

### Example 2-11: Bernoulli Two-Parameter Form

The Bernoulli family can also be written with two numbers instead of one:

$$
p(X=x;\eta_0,\eta_1)=\frac{\exp\left(\eta_1 x+\eta_0(1-x)\right)}{\exp(\eta_0)+\exp(\eta_1)}, \qquad x \in \{0,1\}.
$$


This looks like a two-parameter model, but it is not actually a larger family. It is an over-parameterized way of writing the same one-parameter Bernoulli distribution.

Read the numerator by cases. If $x=1$, then

$$
p(X=1)=\frac{e^{\eta_1}}{e^{\eta_0}+e^{\eta_1}}.
$$


If $x=0$, then

$$
p(X=0)=\frac{e^{\eta_0}}{e^{\eta_0}+e^{\eta_1}}.
$$


So $\eta_1$ is the unnormalized log-weight attached to state $1$, and $\eta_0$ is the unnormalized log-weight attached to state $0$. Exponentiating those numbers produces positive weights, and the denominator normalizes those weights into valid probabilities.

Now divide numerator and denominator by $e^{\eta_0}$:

$$
p(X=1)=\frac{e^{\eta_1-\eta_0}}{1+e^{\eta_1-\eta_0}}, \qquad p(X=0)=\frac{1}{1+e^{\eta_1-\eta_0}}.
$$


Only the difference

$$
\delta=\eta_1-\eta_0
$$


matters. Once the difference is fixed, the probabilities are fixed.

That is why this representation is redundant. The parameter pair has two coordinates, but the actual Bernoulli distribution still has only one degree of freedom. Here "degree of freedom" means "number of independent numerical choices needed to determine the distribution." For Bernoulli, one number is enough, because once $\mathbb{P}(X=1)$ is chosen, $\mathbb{P}(X=0)$ is forced to be its complement.

An explicit example makes the redundancy concrete. Compare

$$
(\eta_0,\eta_1)=(0,2) \qquad \text{and} \qquad (\eta_0,\eta_1)=(5,7).
$$


In both cases the difference is $2$. Therefore both produce

$$
p(X=1)=\frac{e^2}{1+e^2}, \qquad p(X=0)=\frac{1}{1+e^2}.
$$


Adding the same constant to both coordinates changes the raw scores by the same multiplicative factor, and normalization cancels that factor out. So this notation is useful for algebra, but it should not mislead you into thinking the Bernoulli family suddenly became two-dimensional.

### Beta and Dirichlet Distributions

The next question is different from all the examples so far. Up to this point, the random variable was usually an observed outcome such as a coin flip, a die roll, or a measurement. Now we want a distribution over a **parameter**.

For a Bernoulli model, the parameter is

$$
\rho=\mathbb{P}(X=1).
$$


This number is itself constrained:

$$
0 \le \rho \le 1.
$$


So if we want a probability distribution over possible values of $\rho$, we need a density whose support is the interval $[0,1]$. The standard family for that job is the Beta distribution.

That is the first conceptual point to keep explicit:

- Bernoulli is a distribution over outcomes $X \in \{0,1\}$.
- Beta is a distribution over possible Bernoulli parameters $\rho \in [0,1]$.

So Beta is not a new model for coin-flip outcomes themselves. It is a model for uncertainty about the coin's success probability.

The Beta density is

$$
p(\rho)=\mathrm{Beta}(\rho;a,b)=\frac{\Gamma(a+b)}{\Gamma(a)\Gamma(b)}\rho^{a-1}(1-\rho)^{b-1}.
$$


This formula applies on the interval from $0$ to $1$, and the shape parameters satisfy $a>0$ and $b>0$.

The symbol $\Gamma$ is the Gamma function. For positive integers it satisfies

$$
\Gamma(n)=(n-1)!,
$$


so it extends the factorial function to non-integer arguments. In the Beta density, the Gamma-function ratio is the constant that makes the total area equal to one:

$$
\int_0^1 p(\rho)\,d\rho=1.
$$


For understanding the shape of the distribution, the most important part is the factor

$$
\rho^{a-1}(1-\rho)^{b-1}.
$$


That factor tells us how the density behaves near $0$, near $1$, and in between.

Several vocabulary words need to be made explicit before going further.

- The **interior** of $[0,1]$ means the values strictly between $0$ and $1$.
- The **boundaries** are the endpoints $0$ and $1$.
- **Unimodal** means the density has one main peak.
- The **mode** is the point where the density is largest.

So if someone says "the Beta density is unimodal and places mass in the interior," they mean the curve has one peak somewhere between $0$ and $1$, rather than piling up at one or both endpoints.

Before the general formulas, it is best to build intuition from concrete examples.

First example: uniform uncertainty.

If $a=b=1$, then $p(\rho)=1$ for $0 \le \rho \le 1$.

So $\mathrm{Beta}(1,1)$ is the uniform distribution on $[0,1]$. This means equal-length intervals of possible parameter values receive equal probability mass under this Beta distribution. It does **not** mean that a single exact value of $\rho$ has positive probability as a point event, because continuous distributions assign probability through interval area rather than point mass.

Second example: one interior peak.

If $\rho \sim \mathrm{Beta}(5,5)$, then the density is symmetric around $0.5$ and has a single peak near the center. This is what "unimodal" means in this context: there is one bell-like high region rather than two separated spikes. In geometric terms, the distribution places more of its mass near $0.5$ than near $0$ or $1$.

Third example: favoring one side.

If $\rho \sim \mathrm{Beta}(2,5)$, then the mean is $\mathbb{E}[\rho]=\frac{2}{7}\approx 0.286$.

So this distribution leans toward smaller probabilities. In plain language, it places more mass on success probabilities below one-half than on success probabilities above one-half.

Fourth example: favoring extremes.

If $\rho \sim \mathrm{Beta}(0.3,0.3)$, then the density is high near $0$ and near $1$, and relatively low in the middle. So this distribution favors strongly biased parameter values more than nearly fair ones.

This is also the place to explain why boundary spikes are not a paradox. When either shape parameter is below $1$, the density can become very large near $0$ or $1$. That does not violate probability rules, because a density value is not itself a probability. What matters is the area under the curve over an interval, and that total area remains finite and equal to one.

Two summary formulas are useful after the intuition is in place.

The mean is

$$
\mathbb{E}[\rho]=\frac{a}{a+b}
$$

So the ratio $a:b$ controls which side of the interval is favored.

When both shape parameters are greater than $1$, the mode is

$$
\rho_{\mathrm{mode}}=\frac{a-1}{a+b-2}
$$

This is the location of the peak when the density has a genuine interior maximum. The condition matters: if one of the parameters is at most $1$, the density may peak at a boundary instead, so the interior mode formula no longer applies.

The second structural quantity is the total concentration

$$
a+b
$$

Here the two parameters play two different roles, and it is worth separating them carefully.

- The **ratio** of the two parameters controls which success probabilities are favored relative to each other. If the parameters are equal, the distribution is symmetric around $0.5$. If the first parameter is larger, values closer to $1$ receive more weight than values closer to $0$. If the second parameter is larger, the situation reverses.
- The **sum** of the two parameters controls how strongly that preference is enforced. Increasing the sum while keeping the ratio fixed makes the density more concentrated around its central region. Decreasing the sum while keeping the ratio fixed makes the density more spread out.

One way to see this is through the mean formula $\mathbb{E}[\rho]=\frac{a}{a+b}$.

If we multiply both parameters by the same constant, this mean stays fixed, because the ratio $\frac{a}{a+b}$ does not change. But the exponents in the density become larger, so the density rises more sharply around the preferred region and falls off more quickly away from it.

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

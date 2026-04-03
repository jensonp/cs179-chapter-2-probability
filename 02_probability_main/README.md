# Probability and Inference

Source: ../notes/02_probability_reconstructed/source/02_probability.pdf

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
| `2.3` likelihood, MLE, Beta-Bernoulli updates, basic model selection | yes | hyper-priors, weakly informative priors, and some of the broader Bayesian-model-selection discussion |
| `2.4` convexity | supporting background only | full optimization interpretation and Hessian viewpoint |
| `2.5` entropy, KL, mutual information | conceptually useful and worth reading | derivation-heavy identities beyond the main examples |
| `2.6` scalar and multivariate Jacobians | useful background | copulas and normalizing flows are the clearest "beyond the course core" topics in this chapter |

If time is short, read `2.1`, the Geometric section, the core parts of `2.2`, and the likelihood / MLE / conjugacy / BIC parts of `2.3` first. Then return to `2.4`-`2.6` as second-pass material.

## Notation Policy

Throughout the note, $\mathbb{P}(A)$ denotes the probability of an event $A$, while $p(x)$ denotes a PMF or PDF value when such an object exists. Random variables are written with uppercase letters, realized values with lowercase letters, $F_X(x)$ denotes a CDF, and $\Omega$ denotes the sample space. When a formula is valid only in a discrete setting, only for densities, only for invertible maps, or only away from a boundary case, that restriction is stated explicitly rather than left implicit.

## 2.1 Probability, Events, Random Variables

Probability is the language we use when a system is uncertain or too complex to model exactly. In AI, the uncertainty often comes less from true randomness than from missing information and limited modeling power. A useful probabilistic model does two things: it describes our assumptions about the world, and it gives rules for combining evidence and updating those assumptions when observations arrive.

### Formal Foundations

At a more formal level, a probabilistic model starts with a probability space

$$(\Omega,\mathcal{F},P).$$

Here $\Omega$ is the sample space of possible outcomes, $\mathcal{F}$ is the collection of events on which probabilities are defined, and $P$ is the probability measure. The measure assigns a number to each event and satisfies nonnegativity, normalization, and countable additivity.

In elementary finite examples, one usually suppresses $\mathcal{F}$ because every subset of $\Omega$ can be treated as an event. In that case the abstract measure language reduces to ordinary bookkeeping over subsets. But the more formal notation matters because later concepts such as densities, cumulative distribution functions, and random variables are induced from this underlying structure rather than being primitive objects in every setting.

A random variable is a measurable function

$$X:\Omega \to \mathbb{R}.$$

This explains an important notation point. A statement such as $X=x$ is not a mysterious new kind of object; it is shorthand for the event

$$\{\omega \in \Omega : X(\omega)=x\}.$$

Likewise, the statement $X \le t$ is shorthand for the event

$$\{\omega \in \Omega : X(\omega)\le t\}.$$

In words: it is the set of all worlds whose value under $X$ is at most $t$. For example, if $X$ is the outcome of a die roll and $t=3$, then the event $X \le 3$ is the subset of worlds $\{1,2,3\}$. The notation looks like an ordinary numerical inequality, but probabilistically it is still an event in the sample space. Probabilities are attached to events first; PMFs, PDFs, and CDFs are derived descriptions of how that event-level probability structure appears after the random variable has mapped worlds into numerical values.

### Probability Axioms and First Consequences

Now fix a probability space $(\Omega,\mathcal{F},P)$. The actual axioms are:

$$0 \le \mathbb{P}(A)$$

for every event $A \in \mathcal{F}$,

$$\mathbb{P}(\Omega) = 1,$$

and countable additivity:

$$\mathbb{P}\left(\bigcup_{i=1}^{\infty} A_i\right) = \sum_{i=1}^{\infty} \mathbb{P}(A_i)$$

whenever the events $A_1,A_2,\dots$ are pairwise disjoint.

Pairwise disjoint means that every pair of distinct events in the collection is disjoint. In other words, if you choose any two different indices $i$ and $j$, the corresponding events do not share any worlds. Formally,

$$A_i \cap A_j = \varnothing \qquad \text{whenever } i \ne j.$$

So countable additivity applies only when the events do not overlap. In that case there is no double counting, so the probability of the union is exactly the sum of the individual probabilities. The phrase pairwise disjoint is stronger than saying only that the whole collection has empty total intersection. It requires every two-event overlap to be empty, because any such overlap would otherwise be counted twice in the sum.

An inline finite example confirms the meaning. For a fair die, let

$$A_1=\{1\},\qquad A_2=\{2\},\qquad A_3=\{3\}.$$

These events are pairwise disjoint because no die outcome can be both $1$ and $2$, etc. Their union is the event "roll at most $3$":

$$A_1 \cup A_2 \cup A_3 = \{1,2,3\}.$$

So

$$\mathbb{P}(A_1 \cup A_2 \cup A_3)=3/6=0.5,$$

while the sum of individual probabilities is

$$\mathbb{P}(A_1)+\mathbb{P}(A_2)+\mathbb{P}(A_3)=1/6+1/6+1/6=3/6=0.5.$$

The equality holds because the three events do not overlap.

Several familiar rules are consequences of these axioms rather than additional axioms. For example,

$$\mathbb{P}(\varnothing)=0$$

follows because $\Omega$ and $\Omega \cup \varnothing$ are the same event, while finite additivity for disjoint sets is the finite case of countable additivity.

Inclusion-exclusion is also derived, not assumed. The clean way to derive it is to decompose the union into pieces that do not overlap. Write

$$A \cup B = A \cup (B \setminus A),$$

where the two pieces are disjoint. The reason is simple: every world in $A$ is, by definition, in $A$, while every world in $B \setminus A$ is in $B$ but explicitly not in $A$. So no world can belong to both pieces at once. Then

$$\mathbb{P}(A \cup B) = \mathbb{P}(A) + \mathbb{P}(B \setminus A).$$

But $B$ itself decomposes as the disjoint union

$$B = (B \setminus A) \cup (A \cap B),$$

because every world in $B$ falls into exactly one of two cases. Either it is not in $A$, in which case it lies in $B \setminus A$, or it is also in $A$, in which case it lies in $A \cap B$. These two cases cannot happen simultaneously, so they are disjoint. Therefore

$$\mathbb{P}(B) = \mathbb{P}(B \setminus A) + \mathbb{P}(A \cap B).$$

Now solve the second equation for $\mathbb{P}(B \setminus A)$ and substitute the result into the first equation. That removes the intermediate term and leaves the familiar correction formula

$$\mathbb{P}(A \cup B) = \mathbb{P}(A) + \mathbb{P}(B) - \mathbb{P}(A \cap B).$$

The logical status matters: normalization and additivity are the assumptions, while empty-set probability and inclusion-exclusion are useful consequences.

For a beginner, the safest way to use these axioms is to think in terms of bookkeeping over possible worlds. First list the worlds that belong to the event. Then check whether those worlds overlap with the worlds of another event. If they do, inclusion-exclusion is the correction term that prevents double counting. For a die roll, if $A=\{1,3,5\}$ and $B=\{4,5,6\}$, the union is not six outcomes but five, because the world $5$ sits in both sets.

### Example 2-1: Random Events

Suppose we roll a standard six-sided die. The event space is

$$\Omega = \{1,2,3,4,5,6\}.$$

Two events are:

$$A = \{\text{odd roll}\} = \{1,3,5\}$$

$$B = \{\text{roll is 4 or greater}\} = \{4,5,6\}.$$

Then $\mathbb{P}(A) = 3/6$, $\mathbb{P}(B) = 3/6$, and $\mathbb{P}(A \cap B) = 1/6$, so $\mathbb{P}(A \cup B) = 5/6$.

The step-by-step computation is worth stating explicitly. Event $A$ contains three elementary outcomes, so $\mathbb{P}(A)=3/6$. Event $B$ also contains three elementary outcomes, so $\mathbb{P}(B)=3/6$. Their intersection is the single outcome $\{5\}$, so $\mathbb{P}(A \cap B)=1/6$. If we simply added $3/6+3/6$, we would count outcome $5$ twice, so we subtract $1/6$ and obtain $5/6$.

### Random Variables

A random variable partitions the event space into disjoint and exhaustive cases and assigns each case a symbolic value. If

$$X \in \{1,\dots,d\},$$

then the events $X = 1, \dots, X = d$ are mutually exclusive and cover all outcomes, so

$$\sum_{i=1}^d \mathbb{P}(X=i) = 1.$$

The possible values are called the states of the variable, and the set of all possible values is its domain. For discrete variables, the probability mass function is often written as $p(X=x)$ or simply $p(x)$ when the variable is clear from context.

A full beginner-to-expert way to read this is the following. At the beginner level, a random variable is a label attached to each outcome. At the intermediate level, it is a partition of the event space into mutually exclusive cases. At the expert level, it is a measurable map from worlds in $\Omega$ to values in a codomain, and the induced distribution on those values is obtained by pushing probability mass through that map.

A concrete example helps. Let the world be a die roll and define

$$X=0 \text{ if the roll is even}, \qquad X=1 \text{ if the roll is odd.}$$

Then the six raw outcomes collapse into only two states. Since $\{2,4,6\}$ map to $0$ and $\{1,3,5\}$ map to $1$,

$$p(X=0)=3/6, \qquad p(X=1)=3/6.$$

The random variable therefore compresses a detailed world description into the part of the world we care about.

### PMFs and Indicator Notation

Before writing down specific discrete distributions, it helps to define two pieces of notation that will be used repeatedly.

For a discrete random variable, the probability mass function, or PMF, is the function that assigns a probability to each possible state:

$$p(X=x)=\mathbb{P}(X=x).$$

So a PMF is not a new kind of probability. It is simply the probability of the event $X=x$, viewed as a function of the value $x$.

In beginner language, a PMF is just a probability table written as a function. For example, if a three-state weather variable has

$$p(X=\text{sun})=0.5,\qquad p(X=\text{cloud})=0.3,\qquad p(X=\text{rain})=0.2,$$

then the PMF is the rule that returns $0.5$ at sun, $0.3$ at cloud, and $0.2$ at rain. The table view and the function view are the same object described in two different ways.

The second piece of notation is the indicator function

$$\mathbf{1}[X=x],$$

which equals $1$ when the statement inside the brackets is true and equals $0$ when it is false. Indicator notation is useful because it turns a logical statement such as "the realized state is rain" into a numerical exponent or coefficient. That is exactly what happens in the Bernoulli and categorical product forms below.

For example, if the realized weather state is rain, then

$$\mathbf{1}[X=\text{sun}]=0,\qquad \mathbf{1}[X=\text{cloud}]=0,\qquad \mathbf{1}[X=\text{rain}]=1.$$

So indicator notation is not mysterious symbolism. It is just a numerical way to mark which statement is true in the realized outcome.

### Example 2-2: Bernoulli Distribution

A Bernoulli random variable is binary:

$$X \in \{0,1\}.$$

If

$$\mathbb{P}(X=1) = \rho,$$

then automatically

$$\mathbb{P}(X=0) = 1-\rho.$$

We can write the distribution as

$$p(X) = \mathrm{Ber}(X;\rho) = \rho^X (1-\rho)^{1-X}.$$

This evaluates to $\rho$ when $X = 1$ and to $1-\rho$ when $X = 0$.

An equivalent representation is

$$p(X) = \rho \mathbf{1}[X=1] + (1-\rho)\mathbf{1}[X=0].$$

To see this mechanically, plug in the only two possible values. If $X=1$, then

$$\rho^X(1-\rho)^{1-X} = \rho^1(1-\rho)^0 = \rho.$$

If $X=0$, then

$$\rho^X(1-\rho)^{1-X} = \rho^0(1-\rho)^1 = 1-\rho.$$

So the compact formula is not magic notation; it is just a switch that selects the correct probability for the realized binary outcome.

### Example 2-3: Discrete Distribution

If $X \in \{1,\dots,d\}$, then a discrete distribution is just a probability table:

$$\mathbb{P}(X=i) = \rho_i, \qquad \rho_i \ge 0, \qquad \sum_{i=1}^d \rho_i = 1.$$

This table is the PMF of the variable. For each possible state $i$, the number $\rho_i$ is the probability that $X$ takes that state. Only $d-1$ of those values are free, because the last one is determined by normalization. If the first $d-1$ probabilities are already fixed, the final one must be whatever value makes the whole table sum to one.

Two vocabulary items make that sentence precise. First, a discrete variable with exactly $d$ possible states is sometimes called $d$-ary. For example, a die-outcome variable with support $\{1,2,3,4,5,6\}$ is $6$-ary, while the weather variable with states $\{\text{sun},\text{cloud},\text{rain}\}$ is $3$-ary.

Second, degrees of freedom means the number of independent numerical choices you can make after all required constraints are enforced. Here we have $d$ nonnegative numbers $\rho_1,\dots,\rho_d$, but they must satisfy the single normalization constraint $\sum_{i=1}^d \rho_i=1$. That one constraint removes one free choice, so the PMF has $d-1$ degrees of freedom.

An explicit three-state check: if $d=3$ and you choose $\rho_1=0.5$ and $\rho_2=0.3$, then normalization forces

$$\rho_3 = 1-\rho_1-\rho_2 = 1-0.5-0.3=0.2.$$

So you only had two independent choices, which matches $d-1=2$. This same "number of table entries minus normalization constraints" logic is what drives the parameter-count statements later in the chapter.

One compact representation is

$$p(X) = \prod_{i=1}^d \rho_i^{\mathbf{1}[X=i]}.$$

This product form is compact, but it should not be read too quickly. The indicator in the exponent decides which factor stays active. If the realized state is $i$, then $\mathbf{1}[X=i]=1$ for that one state and $\mathbf{1}[X=j]=0$ for every other state $j \ne i$. So the factor corresponding to the realized state contributes its probability, while every non-realized factor becomes a zero-th power and therefore contributes the multiplicative identity $1$.

A concrete three-state example makes the structure explicit. Suppose weather tomorrow is modeled as

$$X \in \{\text{sun}, \text{cloud}, \text{rain}\}$$

with

$$\rho_{\text{sun}}=0.5,\qquad \rho_{\text{cloud}}=0.3,\qquad \rho_{\text{rain}}=0.2.$$

Suppose the realized state is rain. Then the three indicator exponents are

$$\mathbf{1}[X=\text{sun}]=0,\qquad \mathbf{1}[X=\text{cloud}]=0,\qquad \mathbf{1}[X=\text{rain}]=1.$$

Substituting those values into the product form gives

$$p(X)=\rho_{\text{sun}}^{0}\rho_{\text{cloud}}^{0}\rho_{\text{rain}}^{1}.$$

Now evaluate each factor separately. The first two factors are

$$\rho_{\text{sun}}^{0}=1,\qquad \rho_{\text{cloud}}^{0}=1,$$

not because sun or cloud have probability zero, but because those states were not realized in this particular outcome. The final factor is

$$\rho_{\text{rain}}^{1}=\rho_{\text{rain}}=0.2.$$

So the whole product reduces to

$$\rho_{\text{sun}}^0 \rho_{\text{cloud}}^0 \rho_{\text{rain}}^1 = 0.2.$$

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

The PMF notation, the table notation, and the indicator-product notation are all describing this same distribution. The only difference is the representation. The table is easiest for direct reading, while the product form is easier for algebraic manipulation.

### Geometric Distribution

Another basic discrete family is the Geometric distribution. It models repeated independent Bernoulli trials with success probability $\rho$ until the first success occurs. One must be careful about conventions, because two closely related definitions are common in textbooks and software.

In these notes, and in the course homework workflow built around Pyro, the random variable counts the number of failures before the first success. Its support is therefore

$$X \in \{0,1,2,\dots\},$$

and its PMF is

$$p(X=x)=(1-\rho)^x\rho.$$

The formula is easy to derive once the event is stated explicitly. The event $X=x$ means the first $x$ trials fail and the next trial succeeds. Because the trials are independent, we multiply the probabilities of those pieces: $x$ failures contribute $(1-\rho)^x$ and the final success contributes $\rho$.

For example, if $\rho=0.2$, then

$$p(X=0)=0.2,\qquad p(X=1)=0.8 \cdot 0.2=0.16,\qquad p(X=2)=0.8^2 \cdot 0.2=0.128.$$

The key numerical pattern is that each step to the right multiplies the previous probability by another factor of $(1-\rho)$. When $\rho=0.2$, that factor is $0.8$, so each bar is $80\%$ of the bar immediately before it. Concretely, the first few probabilities are $0.2$, $0.16$, $0.128$, and so on. That is what "decays geometrically to the right" means: the bars do not decrease by subtracting a fixed amount; they decrease by repeated multiplication by the same ratio.

So a histogram of this distribution has a tallest bar at $x=0$, then progressively smaller bars as $x$ increases. The right tail is long because there is always some chance that many failures occur before the first success, but the probability of those larger counts drops off by repeated multiplication.

Expected value (mean). For a discrete variable, the expected value is defined as the probability-weighted average

$$\mathbb{E}[X]=\sum_{x} x\,p(X=x).$$

For the Geometric distribution with $p(X=x)=(1-\rho)^x\rho$ on $\{0,1,2,\dots\}$, this sum can be evaluated in closed form. Let $r=1-\rho$. Then

$$\mathbb{E}[X]=\sum_{x=0}^\infty x\,r^x\,\rho=\rho\sum_{x=0}^\infty x r^x.$$

For $|r|<1$, the geometric-series identity is

$$\sum_{x=0}^\infty x r^x=\frac{r}{(1-r)^2}.$$

Here $r=1-\rho \in (0,1)$, so the identity applies, and we obtain

$$\mathbb{E}[X]=\rho\cdot \frac{r}{(1-r)^2}=\rho\cdot \frac{1-\rho}{\rho^2}=\frac{1-\rho}{\rho}.$$

So the mean under this zero-based convention is

$$\mathbb{E}[X]=\frac{1-\rho}{\rho}.$$

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

$$p(T=0) = \sum_{d,c} p(T=0,D=d,C=c)$$

$$= 0.576 + 0.008 + 0.144 + 0.072 = 0.80.$$

Marginalization is just "add all ways the event can happen."

A second marginal shows the same procedure from another angle. To compute the chance of a cavity, sum every row with $C=1$:

$$p(C=1)=0.008+0.072+0.012+0.108=0.20.$$

This explains why a marginal is called a marginal: it is what remains after the other coordinates have been summed away.

### Conditional Probability

Conditioning means restricting attention to worlds where the condition holds:

$$p(D=d \mid T=t) = \frac{p(D=d,T=t)}{p(T=t)}.$$

The numerator is the probability that both things happen; the denominator is the total probability of the condition. The result is a normalized probability distribution over $D$ given $T=t$.

For the dentist table, conditioning on $T=1$ means we throw away every row with $T=0$ and keep only the four rows with toothache. Inside that restricted world, the total probability mass is

$$p(T=1)=0.064+0.012+0.016+0.108=0.20.$$

Now the conditional probability of a probe catch becomes

$$p(D=1 \mid T=1)=\frac{0.016+0.108}{0.20}=\frac{0.124}{0.20}=0.62.$$

The key beginner intuition is "restrict first, renormalize second."

It is also important to separate conditioning from intervention. The conditional distribution $p(D \mid T=1)$ is obtained by taking the original joint distribution, keeping only the worlds in which toothache has already been observed, and renormalizing the remaining probabilities so they sum to one. So this conditional answers an informational question: among the worlds where $T=1$ is already true, how does the probe variable $D$ behave?

That is different from an intervention. An intervention would mean externally forcing $T$ to equal $1$ and then asking how $D$ changes under that manipulated system. In the dentist story, observing a toothache gives information about whether a cavity is present, and that information changes the distribution of $D$. But physically causing a toothache would not automatically carry the same information about the cavity state. A plain joint distribution supports conditioning; it does not, by itself, tell us the effect of interventions. For intervention questions, one needs extra causal structure beyond ordinary probability tables.

### Example 2-5: Bayes Rule

Bayes rule starts from a model of how likely an observation is under each hypothesis, such as $p(D=d \mid C=c)$, and turns it into a model of how likely each hypothesis is after the observation has been seen, namely $p(C=c \mid D=d)$:

$$p(C=c \mid D=d) = \frac{p(D=d \mid C=c)p(C=c)}{p(D=d)}.$$

In this formula, the hypothesis is the value of $C$, meaning the statement "the cavity variable equals $c$." The observation is the value of $D$, meaning the statement "the probe variable equals $d$." So this example is not talking about an abstract unnamed hypothesis. It is specifically asking how probable each cavity state is after we observe the probe outcome.

Before using shorthand language, it helps to name each term explicitly. The prior is $p(C=c)$, which is the probability assigned to the cavity-state hypothesis before seeing the probe observation. The likelihood is $p(D=d \mid C=c)$, which measures how compatible the observed probe result is with that cavity state. The evidence is $p(D=d)$, which is the total probability of seeing that probe result after averaging over every cavity case. The posterior is $p(C=c \mid D=d)$, which is the updated probability of the cavity state after the probe result has been taken into account.

The word posterior should not feel like a new mysterious object. It is just a conditional probability, using the same conditioning idea introduced earlier in the chapter. The only difference is what is being conditioned on. Earlier we conditioned one ordinary event on another ordinary event. Here we are conditioning a hypothesis about the cavity state on observed evidence from the probe result. So "posterior" means "the probability after the observation has been incorporated."

With those names in place, the formula can be read as the sentence

$$\text{posterior} = \text{likelihood} \cdot \text{prior} / \text{evidence}.$$

This sentence is only a mnemonic for the roles played by the four terms. It is not a second formula that must be memorized separately. It simply says that the updated belief equals the old belief, reweighted by how strongly the data supports that hypothesis, and then normalized by the total probability of the observation.

To describe the odds form, suppose $H_1$ and $H_0$ are two mutually exclusive hypotheses, meaning two competing explanations that cannot both be true at the same time. Let $E$ denote the observed evidence. Bayes' rule then implies

$$\frac{p(H_1 \mid E)}{p(H_0 \mid E)} = \frac{p(E \mid H_1)}{p(E \mid H_0)} \cdot \frac{p(H_1)}{p(H_0)}.$$

This odds form is often more informative than the scalar formula because each ratio has a distinct interpretation. The prior odds

$$\frac{p(H_1)}{p(H_0)}$$

compare the plausibility of the two hypotheses before any new evidence is observed. The likelihood ratio

$$\frac{p(E \mid H_1)}{p(E \mid H_0)}$$

measures how much more strongly the evidence supports $H_1$ than $H_0$. The posterior odds

$$\frac{p(H_1 \mid E)}{p(H_0 \mid E)}$$

are the updated comparison after the evidence has been incorporated. The evidence term does not appear explicitly in this ratio form because the same normalizing constant $p(E)$ appears in both posterior probabilities and cancels when the quotient is taken.

For the dentist example, suppose:

$$p(T=1 \mid C=0) = 0.1, \qquad p(T=1 \mid C=1) = 0.6$$

$$p(C=0) = 0.8, \qquad p(C=1) = 0.2.$$

Here the hypothesis of interest is $C=1$, meaning "the patient has a cavity," and the observation is $T=1$, meaning "the patient has a toothache." We now apply Bayes' rule with those two specific events:

$$p(C=1 \mid T=1)=\frac{p(T=1 \mid C=1)p(C=1)}{p(T=1)}.$$

Now fill in each term one at a time. The likelihood term

$$p(T=1 \mid C=1)=0.6$$

means that among the worlds where a cavity is present, toothache occurs with probability $0.6$. The prior term

$$p(C=1)=0.2$$

means that before observing any toothache, the cavity probability is $0.2$. Multiplying these two quantities uses the product rule and gives the joint probability that both events occur:

$$p(T=1,C=1)=p(T=1 \mid C=1)p(C=1)=0.6 \cdot 0.2 = 0.12.$$

So the numerator $0.12$ is not an arbitrary number. It is the probability of the conjunction "toothache and cavity."

Next compute the denominator $p(T=1)$, which is the total probability of observing a toothache. There are two mutually exclusive ways for toothache to occur in this model: either there is a cavity or there is not. So we apply the law of total probability over the two cavity cases:

$$p(T=1)=p(T=1 \mid C=1)p(C=1)+p(T=1 \mid C=0)p(C=0).$$

Now substitute the given numbers:

$$p(T=1)=0.6 \cdot 0.2 + 0.1 \cdot 0.8 = 0.12 + 0.08 = 0.20.$$

The second term $0.1 \cdot 0.8 = 0.08$ is the probability of "toothache and no cavity." Adding $0.12$ and $0.08$ gives the full toothache probability $0.20$.

Now divide the numerator by the denominator:

$$p(C=1 \mid T=1)=\frac{0.12}{0.20}=0.60.$$

This final number means that after observing a toothache, the probability of a cavity rises to $0.60$. So the observation has changed the cavity probability from the prior value $0.20$ to the posterior value $0.60$.

The derivation can also be unpacked from the definition of conditional probability itself. Start with

$$p(C=1 \mid T=1)=\frac{p(C=1,T=1)}{p(T=1)}.$$

Then factor the numerator using the product rule:

$$p(C=1,T=1)=p(T=1 \mid C=1)p(C=1).$$

Substituting this into the conditional formula gives Bayes' rule. So Bayes' rule is not an extra axiom; it is the conditional-probability definition plus the product rule written in a convenient direction.

### Law of Total Probability

If $B_1,\dots,B_k$ form a partition of the sample space, then any event $A$ satisfies

$$p(A)=\sum_{i=1}^k p(A \mid B_i)p(B_i).$$

The law is simple but foundational. It says that if the worlds are first split into mutually exclusive and exhaustive cases, then the total probability of $A$ is the weighted average of its conditional probabilities inside those cases. Here mutually exclusive means at most one case can hold at a time, and exhaustive means at least one case must hold. So exactly one of the $B_i$ happens in every world.

An inline numerical example makes the averaging interpretation concrete. Suppose the hidden situation has three cases:

$$B_1=\{\text{route 1}\},\qquad B_2=\{\text{route 2}\},\qquad B_3=\{\text{route 3}\},$$

with

$$p(B_1)=0.5,\qquad p(B_2)=0.3,\qquad p(B_3)=0.2.$$

Let the event $A$ be "arrive within 30 minutes." Suppose the on-time probabilities depend on the route:

$$p(A \mid B_1)=0.9,\qquad p(A \mid B_2)=0.6,\qquad p(A \mid B_3)=0.4.$$

Then the law of total probability says

$$p(A)=p(A \mid B_1)p(B_1)+p(A \mid B_2)p(B_2)+p(A \mid B_3)p(B_3).$$

Substituting the numbers gives

$$p(A)=0.9 \cdot 0.5 + 0.6 \cdot 0.3 + 0.4 \cdot 0.2 = 0.45 + 0.18 + 0.08 = 0.71.$$

Each product $p(A \mid B_i)p(B_i)$ is the probability that both "case $B_i$ happens" and "event $A$ happens" occur together. The sum adds those disjoint ways for $A$ to happen.

The formula follows directly from disjoint decomposition. Because the sets $B_1,\dots,B_k$ form a partition, the event $A$ can be written as the disjoint union

$$A=(A \cap B_1)\cup \cdots \cup (A \cap B_k).$$

Therefore additivity gives

$$p(A)=\sum_{i=1}^k p(A \cap B_i).$$

Applying the product rule to each summand yields

$$p(A \cap B_i)=p(A \mid B_i)p(B_i),$$

and substituting those terms back into the sum gives the law of total probability. So the law is not an extra identity to memorize; it is the ordinary additivity axiom plus the product rule applied to a partition.

In the dentist example, the evidence term $p(T=1)$ is exactly a law-of-total-probability computation over the cavity cases. The two cases $C=1$ and $C=0$ form a partition, so

$$p(T=1)=p(T=1 \mid C=1)p(C=1)+p(T=1 \mid C=0)p(C=0).$$

Plugging in the numbers gives

$$p(T=1)=0.6 \cdot 0.2 + 0.1 \cdot 0.8 = 0.20.$$

So the evidence term is not mysterious. It is the ordinary total probability of the observation, computed by averaging over the hidden hypothesis cases.

### Worked Example: Base Rates and Screening

Suppose a rare disease has prevalence

$$p(D=1)=0.01.$$

A screening test has sensitivity

$$p(T=+ \mid D=1)=0.95$$

and false-positive rate

$$p(T=+ \mid D=0)=0.10.$$

If a patient tests positive, the posterior disease probability is

$$p(D=1 \mid T=+)=\frac{p(T=+ \mid D=1)p(D=1)}{p(T=+)}.$$

The denominator comes from the law of total probability:

$$p(T=+)=0.95 \cdot 0.01 + 0.10 \cdot 0.99 = 0.1085.$$

Therefore

$$p(D=1 \mid T=+)=\frac{0.95 \cdot 0.01}{0.1085}\approx 0.0876.$$

Here is what those numbers mean in both probability and percentage form. Probabilities are numbers between $0$ and $1$. To convert a probability to a percentage, multiply by $100$.

In this example, the prior disease probability is $p(D=1)=0.01$, which is $1\%$. After observing a positive test, the posterior is $p(D=1 \mid T=+)\approx 0.0876$, which is about $8.76\%$ (rounded to $8.8\%$). So the test is informative because it raises the disease probability from $0.01$ to about $0.088$, but the disease still remains unlikely (well under $10\%$) because the base rate was extremely small to begin with. This is exactly the setting in which base-rate neglect causes intuitive mistakes.

### Example 2-6: Table-Based Computation

The same Bayes update can be done by manipulating tables directly. The goal is to compute the posterior distribution $p(C \mid T=1)$, meaning "how likely is a cavity after we observe toothache."

The table view is easiest to understand if we write the target posterior in a way that matches the three operations we will perform:

$$p(C \mid T=1)=\frac{\sum_d p(T=1,d,C)}{\sum_{c,d} p(T=1,d,c)}.$$

The numerator $\sum_d p(T=1,d,C)$ means: fix the evidence $T=1$, then sum out the hidden variable $D$ to obtain a joint table over $(T=1,C)$. The denominator $\sum_{c,d} p(T=1,d,c)$ is the total probability of the evidence $T=1$, also called the evidence or normalization constant. Dividing by that constant is what turns the remaining nonnegative numbers into a proper posterior distribution that sums to $1$ over the possible cavity states.

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

$$p(T=1,D=0,C=0)=0.064,\qquad p(T=1,D=0,C=1)=0.012,$$

$$p(T=1,D=1,C=0)=0.016,\qquad p(T=1,D=1,C=1)=0.108,$$

and summing them gives

$$p(T=1)=0.064+0.012+0.016+0.108=0.20.$$

This $0.20$ is the probability that a toothache occurs under the model, before conditioning on anything else. It is also the normalizing constant we will divide by at the end.

Step 2 (marginalize out $D$). To obtain $p(T=1,C)$, add over the two possible values of $D$ for each fixed cavity state:

$$p(T=1,C=0)=p(T=1,D=0,C=0)+p(T=1,D=1,C=0)=0.064+0.016=0.080,$$

$$p(T=1,C=1)=p(T=1,D=0,C=1)+p(T=1,D=1,C=1)=0.012+0.108=0.120.$$

Notice that this intermediate table is still not a conditional distribution over $C$. It is a joint table with $T=1$ fixed, so it sums to $p(T=1)$:

$$0.080+0.120=0.20.$$

Step 3 (normalize). Finally divide by the evidence total $p(T=1)=0.20$ to turn $p(T=1,C)$ into a posterior distribution over $C$:

$$p(C=0 \mid T=1)=\frac{0.080}{0.20}=0.40,\qquad p(C=1 \mid T=1)=\frac{0.120}{0.20}=0.60.$$

Now the two posterior probabilities sum to $1$, as they must. Interpreting the result: after observing toothache, the cavity probability rises from the prior $p(C=1)=0.20$ to the posterior $p(C=1 \mid T=1)=0.60$.

### Expectation

The expectation, or expected value, is the long-run average value of the variable if the same random experiment were repeated many times and the outcomes were averaged. In a discrete model, that long-run average is computed by weighting each possible value by the probability of seeing it. So the expectation is a probability-weighted average, not a guess about the single next outcome.

The word expected can be misleading in ordinary English. In probability, it does not mean "what I predict will happen next" or "the most likely outcome." It means the center of mass of the distribution. That is why an expectation can be a number the variable never literally takes.

For a discrete variable, the definition is:

$$\mathbb{E}[X] = \sum_x x \, p(x).$$

Each term in the sum has a clear meaning. The value $x$ tells us what the outcome contributes if it occurs, and the factor $p(x)$ tells us how often it occurs in the long run. Multiplying and summing therefore averages the possible outcomes according to how likely they are.

For a Bernoulli variable, $\mathbb{E}[X] = \rho$, which is why the Bernoulli parameter is also the mean.

A full worked example shows why expectation is called a weighted average. Suppose

$$\mathbb{P}(X=0)=0.7, \qquad \mathbb{P}(X=1)=0.3.$$

Then

$$\mathbb{E}[X]=0 \cdot 0.7 + 1 \cdot 0.3 = 0.3.$$

For a die roll with values $1$ through $6$,

$$\mathbb{E}[X] = \sum_{x=1}^6 x \cdot \frac{1}{6} = \frac{1+2+3+4+5+6}{6}=3.5.$$

So expectation is not required to be a value the variable actually takes. A fair die never lands on $3.5$, but $3.5$ is still the mean location of the distribution.

### Linearity of Expectation

Expectation is linear:

$$\mathbb{E}[aX+bY+c]=a\mathbb{E}[X]+b\mathbb{E}[Y]+c.$$

No independence assumption is required. That point is easy to miss because many later formulas do require independence, but linearity of expectation does not. The rule holds even when $X$ and $Y$ are strongly dependent.

It is worth checking that claim with a dependent example. Let $X$ be Bernoulli with

$$\mathbb{P}(X=1)=0.3,\qquad \mathbb{P}(X=0)=0.7,$$

and define

$$Y=1-X.$$

Then $X$ and $Y$ are completely dependent: once $X$ is known, $Y$ is forced. But linearity still works:

$$\mathbb{E}[X+Y]=\mathbb{E}[1]=1,$$

while

$$\mathbb{E}[X]+\mathbb{E}[Y]=0.3+0.7=1.$$

So dependence does not break linearity. That is exactly why indicator decompositions are so powerful later in probability and machine learning.

For a concrete example, suppose three coin flips have indicator variables $H_1,H_2,H_3$, where $H_i=1$ if flip $i$ is heads and $0$ otherwise. Let

$$N=H_1+H_2+H_3$$

denote the total number of heads. Then

$$\mathbb{E}[N]=\mathbb{E}[H_1]+\mathbb{E}[H_2]+\mathbb{E}[H_3].$$

If each flip has head probability $\rho$, then $\mathbb{E}[H_i]=\rho$ for every $i$, so

$$\mathbb{E}[N]=3\rho.$$

This conclusion does not require us to enumerate all eight outcomes explicitly. Linearity lets us decompose a complicated count into simple indicator expectations and add them back together.

### Variance, Covariance, and Correlation

Expectation gives the center of a distribution, but it does not describe spread. The basic spread measure is variance:

$$\mathrm{Var}(X)=\mathbb{E}[(X-\mathbb{E}[X])^2].$$

Expanding the square gives the useful identity

$$\mathrm{Var}(X)=\mathbb{E}[X^2]-\mathbb{E}[X]^2.$$

An inline Bernoulli example shows how to use the identity mechanically. If $X \in \{0,1\}$ with $p(X=1)=\rho$, then $X^2=X$ for both possible values, so

$$\mathbb{E}[X]=\rho,$$

and

$$\mathbb{E}[X^2]=\mathbb{E}[X]=\rho.$$

Therefore

$$\mathrm{Var}(X)=\rho-\rho^2=\rho(1-\rho).$$

So for a Bernoulli random variable, the spread is largest near $\rho=1/2$ and shrinks to zero as $\rho$ approaches $0$ or $1$.

For two variables, covariance is

$$\mathrm{Cov}(X,Y)=\mathbb{E}[(X-\mathbb{E}[X])(Y-\mathbb{E}[Y])].$$

The normalized version is correlation:

$$\mathrm{Corr}(X,Y)=\frac{\mathrm{Cov}(X,Y)}{\sqrt{\mathrm{Var}(X)\mathrm{Var}(Y)}}.$$

Variance reacts predictably to affine transformations:

$$\mathrm{Var}(aX+b)=a^2 \mathrm{Var}(X), \qquad \mathrm{Cov}(aX+b,cY+d)=ac\,\mathrm{Cov}(X,Y).$$

These formulas show what each quantity measures. Adding a constant shifts the location but does not change spread. Multiplying by $a$ rescales the spread by $a^2$. Covariance records whether large values of one variable tend to occur with large or small values of the other.

A diagnostic example shows why mean and variance are genuinely different summaries. Let $X$ be constant at $3$, and let $Y$ equal $0$ or $6$ with probabilities $1/2$ and $1/2$. Then

$$\mathbb{E}[X]=3, \qquad \mathbb{E}[Y]=0 \cdot \frac{1}{2}+6 \cdot \frac{1}{2}=3,$$

so both variables have the same mean. But

$$\mathrm{Var}(X)=0$$

because $X$ never moves, while

$$\mathrm{Var}(Y)=\mathbb{E}[Y^2]-\mathbb{E}[Y]^2 =\left(0^2 \cdot \frac{1}{2}+6^2 \cdot \frac{1}{2}\right)-3^2 =18-9=9.$$

So two distributions can agree perfectly on their center and still differ sharply in uncertainty.

Covariance also does not capture every form of dependence. Let $X$ take values $-1$, $0$, and $1$ with equal probability, and define

$$Y=X^2.$$

Then $Y$ is completely determined by $X$, so the variables are dependent. But

$$\mathbb{E}[X]=0, \qquad \mathbb{E}[XY]=\mathbb{E}[X^3]=0,$$

which gives

$$\mathrm{Cov}(X,Y)=\mathbb{E}[XY]-\mathbb{E}[X]\mathbb{E}[Y]=0.$$

So zero covariance does not imply independence. It only rules out linear dependence in the centered variables.

### Independence

Two random variables $X$ and $Y$ are independent if

$$p(X,Y) = p(X)p(Y).$$

Equivalently, observing one does not change the distribution of the other:

$$p(X \mid Y) = p(X).$$

The equivalence between these two definitions is worth writing out because it gets used constantly. If

$$p(X,Y)=p(X)p(Y),$$

then for any value of $Y$ with positive probability,

$$p(X \mid Y)=\frac{p(X,Y)}{p(Y)}=\frac{p(X)p(Y)}{p(Y)}=p(X).$$

Conversely, if

$$p(X \mid Y)=p(X)$$

for every value of $Y$ with $p(Y)>0$, then multiplying both sides by $p(Y)$ gives

$$p(X,Y)=p(X \mid Y)p(Y)=p(X)p(Y).$$

So the factorization view and the "observing $Y$ changes nothing" view are two algebraically equivalent ways to state the same independence claim. The caveat about $p(Y)>0$ is important: conditional probability is only defined when the conditioning event has nonzero probability.

Independence also simplifies the joint distribution by reducing how many numbers must be specified. Suppose $X$ and $Y$ are both $d$-ary, meaning each takes one of $d$ states. A general joint distribution $p(X,Y)$ is a $d \times d$ probability table with $d^2$ entries. Those entries must be nonnegative and must satisfy exactly one normalization constraint:

$$\sum_{x}\sum_{y} p(X=x,Y=y)=1.$$

So, in the degrees-of-freedom sense, a full unconstrained joint table has $d^2-1$ free parameters: you can choose $d^2-1$ of the entries arbitrarily (subject to nonnegativity), and the final entry is forced by the requirement that the whole table sums to $1$.

Under independence, the joint factorizes as

$$p(X,Y)=p(X)p(Y).$$

Now you do not need to choose $d^2$ unrelated entries. You only choose the two marginal tables. The marginal $p(X)$ has $d$ entries summing to $1$, so it has $d-1$ degrees of freedom. The marginal $p(Y)$ also has $d-1$ degrees of freedom. Therefore the independent model has $(d-1)+(d-1)=2d-2$ degrees of freedom. Once those marginal numbers are chosen, every joint entry is determined by multiplication.

An explicit $d=3$ example shows the reduction mechanically. Let

$$p(X)=(0.5,0.3,0.2),\qquad p(Y)=(0.1,0.6,0.3).$$

Independence implies, for example,

$$p(X=1,Y=2)=p(X=1)p(Y=2)=0.5\cdot 0.6=0.30,$$

and similarly every other joint entry is a product of one $X$-marginal number and one $Y$-marginal number. In this $3 \times 3$ case, an unconstrained joint distribution would have $3^2-1=8$ degrees of freedom, while independence uses only $2\cdot 3-2=4$ degrees of freedom (two independent choices for $p(X)$ and two for $p(Y)$).

This reduction is the main motive for using independence or conditional independence assumptions in AI models: fewer degrees of freedom means fewer parameters to estimate from data and a simpler structure for inference. The tradeoff is that independence is a strong modeling claim. It restricts which joint distributions are representable, so it should only be used when it is substantively justified (or when it is a deliberate approximation).

### Example 2-7: Independence

Let $X$ be a biased coin and $Y$ a weighted four-sided die. If they are independent, then the joint is just the product of the marginals.

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
            <tr><td>$0$</td><td>$1$</td><td>$0.14$</td></tr>
            <tr><td>$0$</td><td>$2$</td><td>$0.21$</td></tr>
            <tr><td>$1$</td><td>$4$</td><td>$0.03$</td></tr>
          </tbody>
        </table>
        <p><strong>Representative joint entries</strong></p>
      </td>
    </tr>
  </tbody>
</table>

To verify independence explicitly, check one conditional. Since

$$p(X=1,Y=4)=0.03$$

and

$$p(Y=4)=0.1,$$

we have

$$p(X=1 \mid Y=4)=\frac{0.03}{0.1}=0.3=p(X=1).$$

The observation of $Y$ leaves the distribution of $X$ unchanged, which is the operational meaning of independence.

### Pairwise Versus Mutual Independence

Independence among more than two variables needs careful wording, because there are multiple strength levels that sound similar but are not equivalent.

Variables $X_1,\dots,X_n$ are mutually independent if every subcollection factorizes:

$$p(X_{i_1},\dots,X_{i_k})=\prod_{j=1}^k p(X_{i_j})$$

for every subset of indices $\{i_1,\dots,i_k\}$. In words: no matter which subset of variables you look at, their joint distribution is the product of their marginals.

Pairwise independence is weaker. It only requires that every pair factorizes:

$$p(X_i,X_j)=p(X_i)p(X_j)\qquad \text{for every } i \ne j.$$

In words: looking at any single pair, observing one variable does not change the distribution of the other. But pairwise independence does not say anything about three-way or higher-order structure.

For three variables, it is worth spelling out the difference explicitly, because this is where many wrong intuitions arise. Mutual independence of $(X_1,X_2,X_3)$ includes the pairwise factorizations

$$p(X_1,X_2)=p(X_1)p(X_2),\qquad p(X_1,X_3)=p(X_1)p(X_3),\qquad p(X_2,X_3)=p(X_2)p(X_3),$$

but it also includes the genuinely stronger triple factorization

$$p(X_1,X_2,X_3)=p(X_1)p(X_2)p(X_3).$$

Pairwise independence only demands the first three equations. It does not constrain $p(X_1,X_2,X_3)$ beyond what is forced by those pairwise marginals.

Mutual independence always implies pairwise independence. The reason is that if the joint factorizes, then any lower-dimensional joint is obtained by summing out the remaining variables and the product structure is preserved. For example, if

$$p(X_1,X_2,X_3)=p(X_1)p(X_2)p(X_3),$$

then marginalizing out $X_3$ gives

$$p(X_1,X_2)=\sum_{x_3} p(X_1,X_2,X_3=x_3)=p(X_1)p(X_2)\sum_{x_3}p(X_3=x_3)=p(X_1)p(X_2),$$

because $\sum_{x_3}p(X_3=x_3)=1$. So mutual independence is strictly stronger: it contains extra content beyond the pairwise statements.

A clean motive for caring about the distinction is that mutual independence is strong enough to reconstruct the full joint distribution from the marginals, while pairwise independence is not. This matters any time you need the probability of a three-way conjunction such as $\mathbb{P}(X_1=a,X_2=b,X_3=c)$. Under mutual independence you multiply three one-variable probabilities. Under pairwise independence alone, that multiplication is not justified.

If each $X_i$ is $d$-ary, then an unconstrained full joint table over $(X_1,\dots,X_n)$ has $d^n$ entries and one normalization constraint, so it has $d^n-1$ degrees of freedom. Under mutual independence, you only specify the $n$ marginal tables. Each marginal has $d-1$ degrees of freedom, so mutual independence reduces the parameter count to $n(d-1)$. Pairwise independence does not lead to an equally clean reduction, because it does not force a single global factorized form.

An explicit parameter-count example makes the abstraction tangible. Suppose $n=3$ and $d=2$ (three binary variables). Then the full joint distribution has $2^3=8$ table entries. Normalization forces those eight probabilities to sum to $1$, so the joint has $8-1=7$ degrees of freedom. Under mutual independence, each variable is determined by a single number, such as $\rho_i=p(X_i=1)$, so the whole model uses only $3$ degrees of freedom. For example, if

$$p(X_1=1)=0.6,\qquad p(X_2=1)=0.2,\qquad p(X_3=1)=0.5,$$

then mutual independence forces

$$p(X_1=1,X_2=0,X_3=1)=p(X_1=1)p(X_2=0)p(X_3=1)=0.6\cdot(1-0.2)\cdot 0.5=0.24.$$

So a single triple probability is determined mechanically from the three one-variable probabilities.

Two explicit examples anchor the definitions.

Example A (mutual independence). Let $H_1,H_2,H_3$ be three independent fair coin-flip indicators, where $H_i=1$ means heads and $H_i=0$ means tails. Because each flip is fair,

$$p(H_i=1)=\frac{1}{2},\qquad p(H_i=0)=\frac{1}{2}.$$

Mutual independence says the probability of any triple is the product of the three one-flip probabilities. For example,

$$p(H_1=1,H_2=0,H_3=1)=p(H_1=1)p(H_2=0)p(H_3=1)=\frac{1}{2}\cdot\frac{1}{2}\cdot\frac{1}{2}=\frac{1}{8}.$$

It also implies every subcollection factorizes. For instance,

$$p(H_1=1,H_2=0)=\frac{1}{4}=\frac{1}{2}\cdot\frac{1}{2}=p(H_1=1)p(H_2=0).$$

Example B (pairwise independent but not mutually independent). Let $U$ and $V$ be independent fair bits:

$$p(U=0)=p(U=1)=\frac{1}{2},\qquad p(V=0)=p(V=1)=\frac{1}{2},$$

and define a third bit

$$W = U \oplus V,$$

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

$$p(W=0)=\frac{1}{2},\qquad p(W=1)=\frac{1}{2}.$$

Now check pairwise independence explicitly.

For the pair $(U,V)$, we have

$$p(U=0,V=0)=\frac{1}{4}=\frac{1}{2}\cdot\frac{1}{2}=p(U=0)p(V=0),$$

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

$$p(U=u,W=w)=\frac{1}{4}=\frac{1}{2}\cdot\frac{1}{2}=p(U=u)p(W=w).$$

So $U$ and $W$ are independent. By symmetry, the same is true for the pair $(V,W)$. Therefore $(U,V,W)$ are pairwise independent.

However, they are not mutually independent, because the triple distribution does not factorize. For example,

$$p(U=0,V=0,W=0)=\frac{1}{4},$$

but the product of marginals would be

$$p(U=0)p(V=0)p(W=0)=\frac{1}{2}\cdot\frac{1}{2}\cdot\frac{1}{2}=\frac{1}{8}.$$

So the equality required by mutual independence fails. The structural reason is that $W$ is a deterministic function of $(U,V)$: once you know $U$ and $V$, the value of $W$ is forced. This creates a three-way constraint that is invisible to any single pairwise marginal.

There is an even sharper way to state what went wrong. Example A (three independent fair bits) and Example B (the XOR construction) have the same pairwise distributions: every pair is uniform over its four outcomes and therefore looks completely independent. So if you only ever inspect two-variable tables, you cannot tell these two very different three-variable models apart. The difference lives entirely in the three-way structure.

Two common wrong notions are worth stating explicitly. First, "pairwise independent" does not mean "no dependence remains." It only rules out dependence that can be detected by looking at any one pair in isolation. Second, pairwise independence is not strong enough to justify multiplying three marginals to get a triple probability. The XOR example is exactly the case in which that intuition fails.

### Conditional Independence

It is rare for variables to be completely independent, but they are often conditionally independent given a mediating variable $Z$:

$$p(X,Y \mid Z) = p(X \mid Z)p(Y \mid Z).$$

Once $Z$ is known, $X$ and $Y$ stop giving extra information about each other.

A good way to read this is as a statement about information flow. Before conditioning, $X$ and $Y$ may be correlated because they both respond to the hidden cause $Z$. After conditioning on $Z$, that common cause has been fixed, so the leftover association disappears. Conditional independence is therefore weaker than independence in general but often much more realistic in structured probabilistic models.

An explicit numeric check shows what the factorization means mechanically. In the dentist model, let $Z=C$ (cavity), $X=T$ (toothache), and $Y=D$ (probe catch). The model claims

$$p(T,D \mid C)=p(T \mid C)p(D \mid C).$$

To check one entry, compute the left-hand side for the case $T=1$, $D=1$, and $C=1$ using the joint table:

$$p(T=1,D=1 \mid C=1)=\frac{p(T=1,D=1,C=1)}{p(C=1)}=\frac{0.108}{0.20}=0.54.$$

Now compute the two right-hand-side factors. From the same model,

$$p(T=1 \mid C=1)=0.6,\qquad p(D=1 \mid C=1)=0.9.$$

So the factorized right-hand side is

$$p(T=1 \mid C=1)p(D=1 \mid C=1)=0.6\cdot 0.9=0.54,$$

which matches the left-hand side exactly. A similar calculation holds for $C=0$:

$$p(T=1,D=1 \mid C=0)=\frac{0.016}{0.80}=0.02,\qquad p(T=1 \mid C=0)p(D=1 \mid C=0)=0.1\cdot 0.2=0.02.$$

This is the core meaning of conditional independence: once $C$ is fixed, the toothache information is already accounted for, so it does not further change the distribution of the probe outcome.

<p align="center">
  <img src="../notes/02_probability_reconstructed/assets/figure_2_conditional_independence_structures.png" alt="Common-cause and explaining-away structures" width="860">
</p>

### Example 2-8: Conditional Independence, Dentist

The dentist model is the cleanest place to see the difference between:

- marginal dependence (two variables are associated when we do *not* condition), and
- conditional independence (the association disappears once we condition on a third variable).

In this model, $T$ (toothache) and $D$ (probe catch) are not independent in general, because both are influenced by the hidden cause $C$ (cavity). But they *are* conditionally independent given $C$. Formally, the claim is

$$D \perp T \mid C.$$

There are two equivalent ways to read this statement, and it helps to see both.

Definition via factorization. Conditional independence means that for every cavity value $c$ with $p(C=c)>0$,

$$p(D,T \mid C=c)=p(D \mid C=c)\,p(T \mid C=c).$$

Definition via “conditioning adds no extra information.” The same claim can be written as: for every $c,t$ with $p(C=c,T=t)>0$,

$$p(D \mid C=c,T=t)=p(D \mid C=c).$$

So once we fix $C$, learning $T$ does not further change the distribution of $D$.

Before showing the conditional-independence check, it is worth confirming that $T$ and $D$ are in fact dependent marginally. Using the joint table from Example 2-4:

$$p(D=1 \mid T=1)=\frac{p(D=1,T=1)}{p(T=1)}=\frac{0.016+0.108}{0.20}=\frac{0.124}{0.20}=0.62,$$

while

$$p(D=1 \mid T=0)=\frac{p(D=1,T=0)}{p(T=0)}=\frac{0.144+0.072}{0.80}=\frac{0.216}{0.80}=0.27.$$

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

$$p(C=1,T=0)=p(0,0,1)+p(0,1,1)=0.008+0.072=0.080,$$

$$p(C=1,T=1)=p(1,0,1)+p(1,1,1)=0.012+0.108=0.120.$$

Now compute the conditional probe-catch probabilities:

$$p(D=1 \mid C=1,T=0)=\frac{p(D=1,C=1,T=0)}{p(C=1,T=0)}=\frac{0.072}{0.080}=0.9,$$

$$p(D=1 \mid C=1,T=1)=\frac{p(D=1,C=1,T=1)}{p(C=1,T=1)}=\frac{0.108}{0.120}=0.9.$$

So once we fix $C=1$, the probability of $D=1$ is $0.9$ regardless of the toothache value.

Case 2: no cavity ($C=0$). Repeat the same computation:

$$p(C=0,T=0)=p(0,0,0)+p(0,1,0)=0.576+0.144=0.720,$$

$$p(C=0,T=1)=p(1,0,0)+p(1,1,0)=0.064+0.016=0.080.$$

Then

$$p(D=1 \mid C=0,T=0)=\frac{0.144}{0.720}=0.2,\qquad p(D=1 \mid C=0,T=1)=\frac{0.016}{0.080}=0.2.$$

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

$$p(H=1)=0.1,\qquad p(L=1)=0.1,$$

so

$$p(H=0)=0.9,\qquad p(L=0)=0.9.$$

Assume the two causes are independent *before* we observe anything:

$$H \perp L \qquad \Longleftrightarrow \qquad p(H,L)=p(H)p(L).$$

Step 2: specify the sensor model. The warning light is a noisy sensor whose behavior depends on which hidden causes are present. Suppose

$$p(W=1 \mid H=0,L=0)=0.1,$$

$$p(W=1 \mid H=1,L=0)=0.8,\qquad p(W=1 \mid H=0,L=1)=0.8,$$

$$p(W=1 \mid H=1,L=1)=0.9.$$

These numbers encode the idea "either problem tends to trigger the light; both problems together trigger it even more reliably; but the light can also turn on by accident."

Step 3: compute the prior joint over the causes. Because we assumed $H \perp L$,

$$p(H=h,L=l)=p(H=h)p(L=l).$$

So the four prior joint probabilities are:

$$p(H=0,L=0)=0.9\cdot 0.9=0.81,$$

$$p(H=0,L=1)=0.9\cdot 0.1=0.09,$$

$$p(H=1,L=0)=0.1\cdot 0.9=0.09,$$

$$p(H=1,L=1)=0.1\cdot 0.1=0.01.$$

Step 4: compute the joint probabilities with $W=1$. The key identity is the product rule:

$$p(H,L,W=1)=p(W=1 \mid H,L)\,p(H,L)=p(W=1 \mid H,L)\,p(H)\,p(L),$$

where the last equality uses the independence assumption $p(H,L)=p(H)p(L)$.

Compute each of the four cases explicitly:

$$p(H=0,L=0,W=1)=0.1\cdot 0.9\cdot 0.9=0.081,$$

$$p(H=0,L=1,W=1)=0.8\cdot 0.9\cdot 0.1=0.072,$$

$$p(H=1,L=0,W=1)=0.8\cdot 0.1\cdot 0.9=0.072,$$

$$p(H=1,L=1,W=1)=0.9\cdot 0.1\cdot 0.1=0.009.$$

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

$$p(W=1)=\sum_{h,l} p(H=h,L=l,W=1)=0.081+0.072+0.072+0.009=0.234.$$

Step 6: posterior query 1, probability of low coolant after seeing the warning light. By the definition of conditional probability,

$$p(L=1 \mid W=1)=\frac{p(L=1,W=1)}{p(W=1)}.$$

Compute the numerator by summing the two rows with $L=1$:

$$p(L=1,W=1)=p(H=0,L=1,W=1)+p(H=1,L=1,W=1)=0.072+0.009=0.081.$$

Therefore

$$p(L=1 \mid W=1)=\frac{0.081}{0.234}=\frac{9}{26}\approx 0.346.$$

Interpretation: the warning light increases the coolant-low probability from the prior $0.1$ to about $0.35$.

Step 7: posterior query 2, probability of low coolant after seeing the warning light *and* learning the engine is hot. Again use conditional probability:

$$p(L=1 \mid W=1,H=1)=\frac{p(L=1,W=1,H=1)}{p(W=1,H=1)}.$$

The numerator is the single row $(H,L)=(1,1)$:

$$p(L=1,W=1,H=1)=0.009.$$

The denominator sums the two rows with $H=1$:

$$p(W=1,H=1)=p(H=1,L=0,W=1)+p(H=1,L=1,W=1)=0.072+0.009=0.081.$$

So

$$p(L=1 \mid W=1,H=1)=\frac{0.009}{0.081}=\frac{1}{9}\approx 0.111.$$

This value is much smaller than $p(L=1 \mid W=1)\approx 0.346$ because $W=1$ could be explained by either hidden cause. Once we learn $H=1$, the event $W=1$ is no longer strong evidence for $L=1$.

A final computation makes the explaining-away effect even more explicit. If instead we learn that the engine is *not* hot, then

$$p(L=1 \mid W=1,H=0)=\frac{p(H=0,L=1,W=1)}{p(H=0,W=1)}=\frac{0.072}{0.081+0.072}=\frac{0.072}{0.153}\approx 0.471.$$

So after observing $W=1$, learning $H=0$ pushes $L$ upward to about $0.47$, while learning $H=1$ pushes $L$ downward to about $0.11$. This is the key structural lesson: $H$ and $L$ are independent in the prior, but after conditioning on their common effect $W=1$, they become dependent.

You can see the dependence-creation cleanly by comparing two conditional probabilities. Before observing $W$, independence means

$$p(L=1 \mid H=1)=p(L=1)=0.1.$$

After observing $W=1$, we found

$$p(L=1 \mid W=1,H=1)\approx 0.111 \qquad \text{and} \qquad p(L=1 \mid W=1,H=0)\approx 0.471.$$

These are different, so $L$ and $H$ are no longer independent once we condition on the shared effect $W=1$. That is the precise algebraic meaning of explaining away in this example.

### Worked Example: Information Sufficiency for Posterior Queries

Suppose $A$, $B$, and $C$ are binary variables and we want to compute

$$p(A=1 \mid B=1,C=1).$$

Bayes' rule exposes the information requirement immediately:

$$p(A=1 \mid B=1,C=1) = \frac{p(B=1,C=1 \mid A=1)p(A=1)}{p(B=1,C=1)}.$$

So, with no conditional independence assumptions, three ingredients are needed:

- the prior $p(A=1)$
- the likelihood term $p(B=1,C=1 \mid A=1)$
- the evidence term $p(B=1,C=1)$

That is the cleanest way to judge whether a proposed set of numbers is sufficient. We do not ask whether the numbers "feel related." We ask whether they determine the numerator and denominator in the displayed formula.

Now consider three candidate information sets.

Set 1 gives

$$p(B=1,C=1),\qquad p(A=1),\qquad p(B=1 \mid A=1),\qquad p(C=1 \mid A=1).$$

Without further assumptions, this set is not sufficient. The separate conditionals $p(B=1 \mid A=1)$ and $p(C=1 \mid A=1)$ do not determine the joint conditional probability $p(B=1,C=1 \mid A=1)$. Many different joint distributions of $(B,C)$ given $A=1$ can share the same one-variable conditionals.

Set 2 gives

$$p(B=1,C=1),\qquad p(A=1),\qquad p(B=1,C=1 \mid A=1).$$

This set is sufficient, because it contains exactly the three ingredients needed by Bayes' rule.

Set 3 gives

$$p(A=1),\qquad p(B=1 \mid A=1),\qquad p(C=1 \mid A=1).$$

This set is not sufficient. Even if one somehow recovered the numerator, the denominator $p(B=1,C=1)$ is still missing, so the posterior cannot be normalized.

Now suppose we are also told that

$$p(B \mid A,C)=p(B \mid A)$$

for all values of the variables, which is the conditional independence statement

$$B \perp C \mid A.$$

Then Set 1 becomes sufficient, because the missing joint conditional factor can now be reconstructed as

$$p(B=1,C=1 \mid A=1)=p(B=1 \mid A=1)p(C=1 \mid A=1).$$

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

$$\int p(x)\,dx = 1.$$

The density defines the probability of any event $X \in A \subseteq \mathbb{R}$ by

$$\mathbb{P}(X \in A) = \int_A p(x)\,dx.$$

This is the first major structural difference from the discrete case. For a continuous variable, the number $p(x)$ is not the probability of the event $X=x$; in fact $\mathbb{P}(X=x)=0$ for every individual point. A density only becomes a probability after integrating it over an interval or region. That is why a density is allowed to exceed one locally, provided the total area under the curve is still one.

A concrete interval computation makes this precise. If $X$ is uniform on $[0,2]$, then $p(x)=1/2$ on that interval. The probability that $X$ falls between $0.3$ and $0.9$ is

$$\mathbb{P}(0.3 \le X \le 0.9) = \int_{0.3}^{0.9} \frac{1}{2}\,dx = \frac{1}{2}(0.9-0.3)=0.3.$$

The point $x=0.4$ itself still has probability zero. What matters is the width of the interval, not the existence of an individual point.

### CDFs and Types of Distributions

The cumulative distribution function, or CDF, is the most universal way to describe a real-valued random variable:

$$F_X(x)=\mathbb{P}(X \le x).$$

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

$$F_X(x_1)\le F_X(x_2).$$

Third, the far-left limit is $0$ and the far-right limit is $1$:

$$\lim_{x\to -\infty} F_X(x)=0,\qquad \lim_{x\to \infty} F_X(x)=1.$$

So a CDF always starts near $0$, climbs as probability accumulates, and eventually levels off at $1$.

One more operational formula is worth stating early because it is how CDFs are actually used:

$$\mathbb{P}(a < X \le b)=F_X(b)-F_X(a).$$

This works because the event $\{X \le b\}$ contains all mass up to $b$, while $\{X \le a\}$ contains all mass up to $a$. Subtracting removes the left part and leaves only the probability in the interval $(a,b]$. This formula is valid whether the variable is discrete, continuous, or mixed.

Now examine the three main types of distributions one by one.

Discrete case. Suppose $X$ is Bernoulli with

$$p(X=1)=0.3,\qquad p(X=0)=0.7.$$

Then the CDF is obtained by asking what probability has accumulated by each threshold.

If $x<0$, then neither state $0$ nor state $1$ is less than or equal to $x$, so

$$F_X(x)=0.$$

If $0 \le x < 1$, then the state $0$ is included but the state $1$ is not, so

$$F_X(x)=\mathbb{P}(X=0)=0.7.$$

If $x \ge 1$, then both states are included, so

$$F_X(x)=\mathbb{P}(X=0)+\mathbb{P}(X=1)=1.$$

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

$$\mathbb{P}(0 < X \le 1)=F_X(1)-F_X(0)=1-0.7=0.3,$$

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

$$F_X(x)=0.$$

If $0 \le x \le 2$, then we integrate only over the part of the support from $0$ to $x$:

$$F_X(x)=\int_0^x \frac{1}{2}\,dt=\frac{x}{2}.$$

If $x>2$, then the full support has already been accumulated, so

$$F_X(x)=1.$$

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

$$\mathbb{P}(0.3 \le X \le 0.9)=F_X(0.9)-F_X(0.3)=0.45-0.15=0.30.$$

So the CDF is not a separate theory from the PDF. It is another way of packaging the same distribution. When a density exists and is sufficiently regular, the derivative of the CDF recovers the density:

$$\frac{d}{dx}F_X(x)=p(x)$$

at points where that derivative exists.

Mixed case. This distinction matters because not every distribution is purely discrete or purely continuous. A mixed distribution contains both an atom and a continuous part. For example, suppose

$$\mathbb{P}(X=0)=0.7,$$

and with the remaining probability $0.3$ we draw $X$ uniformly from $[0,1]$.

Now compute the CDF carefully.

If $x<0$, then no mass has been accumulated:

$$F_X(x)=0.$$

At the exact point $x=0$, the atom at zero is included, so

$$F_X(0)=0.7.$$

If $0<x<1$, then we have already collected the point mass $0.7$, and we also collect the fraction of the continuous part that lies in $[0,x]$. Since that continuous part is uniform on $[0,1]$ and has total weight $0.3$, the additional contribution is $0.3x$. Therefore

$$F_X(x)=0.7+0.3x \qquad \text{for } 0<x<1.$$

Finally, if $x \ge 1$, all probability has been accumulated, so

$$F_X(x)=1.$$

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

$$\int_{-\infty}^{\infty} p(x)\,dx = 1.$$

Because $p(x)=0$ outside $[0,T]$, this reduces to

$$\int_0^T c\,dx = 1.$$

Now compute the integral:

$$c \int_0^T 1\,dx = cT = 1.$$

Therefore

$$c=\frac{1}{T}.$$

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

$$\int_0^T p(x)\,dx = T \cdot \frac{1}{T} = 1.$$

The most important operational consequence is that probability depends only on interval length. If $0 \le a \le b \le T$, then

$$\mathbb{P}(a \le X \le b)=\int_a^b \frac{1}{T}\,dx=\frac{b-a}{T}.$$

So under a uniform model:

- an interval of length $0.1T$ has probability $0.1$,
- an interval of length $0.25T$ has probability $0.25$,
- and two intervals with the same length always have the same probability, no matter where they sit inside $[0,T]$.

This is the precise mathematical meaning of "uniform."

A concrete example makes the geometry clearer. Suppose $X \sim \mathrm{Unif}[0,10]$. Then

$$p(x)=\frac{1}{10}\qquad \text{for } 0 \le x \le 10.$$

Now compute a few interval probabilities:

$$\mathbb{P}(2 \le X \le 5)=\int_2^5 \frac{1}{10}\,dx=\frac{5-2}{10}=0.3,$$

$$\mathbb{P}(7 \le X \le 8)=\int_7^8 \frac{1}{10}\,dx=\frac{8-7}{10}=0.1.$$

The first interval is three times as long as the second, so it has three times as much probability. Location does not matter; length does.

This also clarifies why point probabilities vanish. Even though the density is positive at every point of $[0,T]$, we still have

$$\mathbb{P}(X=4)=0,$$

because a single point has zero width and therefore contributes zero area under the density.

Unlike discrete distributions, the density value itself may be larger than one, as long as the total area under the curve is one. The object that must equal one is the integral, not the height of the graph.

For example, if $X$ is uniform on the very short interval $[0,0.2]$, then

$$p(x)=5$$

on that interval. The density value exceeds one, but the total probability is still

$$\int_0^{0.2} 5\,dx = 1.$$

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

$$p(x) = \mathcal{N}(x;\mu,\sigma^2) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right).$$

Every symbol should be read explicitly:

- $x$ is the location where we evaluate the density,
- $\mu$ is the mean, which sets the center of the bell curve,
- $\sigma^2$ is the variance, which measures spread,
- $\sigma$ is the standard deviation, so $\sigma=\sqrt{\sigma^2}$,
- the prefactor $\frac{1}{\sqrt{2\pi\sigma^2}}$ is the normalization constant,
- and the exponential term controls how fast the density decays as $x$ moves away from $\mu$.

The formula becomes much easier to interpret if we read the exponent first:

$$-\frac{(x-\mu)^2}{2\sigma^2}.$$

The numerator $(x-\mu)^2$ is the squared distance from $x$ to the mean. So the farther $x$ is from $\mu$, the more negative the exponent becomes, and the smaller the density becomes. The denominator $2\sigma^2$ controls how quickly that decay happens. Large $\sigma^2$ means the penalty for being far from the mean is weaker, so the curve is wider. Small $\sigma^2$ means the penalty is stronger, so the curve is narrower.

Three basic facts follow immediately from the formula.

First, the density is symmetric around $\mu$, because replacing $(x-\mu)$ by $-(x-\mu)$ does not change the square:

$$p(\mu+a)=p(\mu-a).$$

Second, the density is largest at $x=\mu$, because that is where the squared term is smallest, namely zero:

$$p(\mu)=\frac{1}{\sqrt{2\pi\sigma^2}}.$$

Third, two values that are the same number of standard deviations away from the mean have the same density. This is easiest to see by standardizing:

$$z=\frac{x-\mu}{\sigma}.$$

Then the exponent becomes $-z^2/2$, so the Gaussian really depends on distance from the mean measured in standard-deviation units.

It is also important not to misread the density value. Even though $p(\mu)$ is the highest point on the curve, it is **not** the probability that $X=\mu$. For a continuous Gaussian,

$$\mathbb{P}(X=\mu)=0.$$

The height of the curve tells us relative density, not point probability.

A full one-dimensional example makes the parameters concrete. Suppose

$$X \sim \mathcal{N}(2,9).$$

Then

- the mean is $\mu=2$,
- the variance is $\sigma^2=9$,
- and the standard deviation is $\sigma=3$.

So the curve is centered at $2$, and one standard deviation corresponds to moving $3$ units left or right. The interval within one standard deviation of the mean is therefore

$$[\mu-\sigma,\mu+\sigma]=[2-3,2+3]=[-1,5].$$

For a Gaussian, about $68\%$ of the total probability lies in that interval. About $95\%$ lies within two standard deviations, namely in

$$[2-6,2+6]=[-4,8],$$

and about $99.7\%$ lies within three standard deviations, namely in

$$[2-9,2+9]=[-7,11].$$

These are approximation rules rather than exact identities, but they are fundamental for intuition. They say that the standard deviation is not just an abstract parameter; it gives a direct spatial scale for where most of the probability mass sits.

The normalization constant also deserves a brief explanation. The exponential term by itself gives the bell shape, but it does not automatically integrate to one. The factor

$$\frac{1}{\sqrt{2\pi\sigma^2}}$$

rescales the curve so that the total area under it over the whole real line is exactly one:

$$\int_{-\infty}^{\infty} p(x)\,dx=1.$$

So the Gaussian formula should be read as "bell-shaped decay" multiplied by "whatever constant is needed to make this a valid density."

Before moving to the multivariate case, it helps to say what actually changes.

In one dimension, the random outcome is a single number such as a height, temperature, or measurement error. In multiple dimensions, the random outcome is a list of numbers observed together. For example, one observation might be

$$x=\begin{bmatrix}x_1\\x_2\end{bmatrix}=\begin{bmatrix}\text{height}\\\text{weight}\end{bmatrix},$$

or

$$x=\begin{bmatrix}x_1\\x_2\\x_3\end{bmatrix}=\begin{bmatrix}\text{exam 1}\\\text{exam 2}\\\text{exam 3}\end{bmatrix}.$$

So a multivariate random variable is really a random vector: one draw produces several coordinates at once.

The mean therefore becomes a mean vector

$$\mu=\mathbb{E}[X]=\begin{bmatrix}\mathbb{E}[X_1]\\ \vdots \\ \mathbb{E}[X_n]\end{bmatrix}.$$

This means each coordinate has its own average value. In two dimensions, for example,

$$\mu=\begin{bmatrix}\mu_1\\\mu_2\end{bmatrix}$$

simply says the cloud of points is centered at horizontal coordinate $\mu_1$ and vertical coordinate $\mu_2$.

The next new object is the covariance matrix. Before giving its formula, it helps to say what problem it solves. In one dimension, one variance number was enough to describe spread. In several dimensions, that is no longer sufficient, because we must describe

- how much each coordinate varies on its own;
- and how pairs of coordinates move together.

The covariance matrix collects both kinds of information into one table:

$$\Sigma=\mathrm{Cov}(X)=
\begin{bmatrix}
\mathrm{Var}(X_1) & \mathrm{Cov}(X_1,X_2) & \cdots \\
\mathrm{Cov}(X_2,X_1) & \mathrm{Var}(X_2) & \cdots \\
\vdots & \vdots & \ddots
\end{bmatrix}.$$

So the diagonal entries are ordinary variances:

$$\Sigma_{11}=\mathrm{Var}(X_1), \qquad \Sigma_{22}=\mathrm{Var}(X_2), \qquad \text{and so on.}$$

The off-diagonal entries are covariances:

$$\Sigma_{12}=\mathrm{Cov}(X_1,X_2).$$

Those covariances answer a new question that does not exist in one dimension: when one coordinate is above its mean, does the other coordinate also tend to be above its mean, below its mean, or unrelated?

It helps to make that concrete before introducing the multivariate Gaussian formula.

- If $\Sigma_{12}>0$, the two coordinates tend to move together. Large values of one coordinate tend to appear with large values of the other.
- If $\Sigma_{12}<0$, the two coordinates tend to move in opposite directions. Large values of one coordinate tend to appear with small values of the other.
- If $\Sigma_{12}=0$, there is no linear covariance between the coordinates.

An explicit $2 \times 2$ example makes the matrix readable. Suppose

$$\Sigma=
\begin{bmatrix}
4 & 0\\
0 & 1
\end{bmatrix}.$$

Then

- the first coordinate has variance $4$, so its standard deviation is $2$;
- the second coordinate has variance $1$, so its standard deviation is $1$;
- and the zero off-diagonal terms say there is no linear covariance between the two coordinates.

So a cloud with this covariance matrix is spread out more in the first direction than in the second. Even before seeing the multivariate Gaussian formula, that tells us the equal-density contours should be stretched horizontally more than vertically.

Now consider

$$\Sigma=
\begin{bmatrix}
1 & 0.8\\
0.8 & 1
\end{bmatrix}.$$

The diagonal entries still say each coordinate has variance $1$, but now the positive off-diagonal entries say the coordinates tend to move together. So the cloud is no longer aligned with the coordinate axes. It is elongated along a diagonal direction. That is the geometric meaning of covariance in the Gaussian setting.

Only after those objects are clear does the multivariate formula become readable.

If $X$ is an $n$-dimensional Gaussian random vector, then its density is

$$p(x) = \mathcal{N}(x;\mu,\Sigma) = (2\pi)^{-n/2} |\Sigma|^{-1/2} \exp\left(-\frac{1}{2}(x-\mu)^T \Sigma^{-1}(x-\mu)\right).$$

Every object now has a specific role:

- $x$ is now an $n$-dimensional vector,
- $\mu$ is the mean vector, which sets the center of the cloud,
- $\Sigma$ is the covariance matrix, which sets spread and dependence,
- $|\Sigma|$ is the determinant of the covariance matrix,
- and the quadratic term

$$
(x-\mu)^T \Sigma^{-1}(x-\mu)
$$

is the squared Mahalanobis distance from $x$ to the mean.

Mahalanobis distance means distance measured in the geometry of the covariance structure rather than ordinary Euclidean distance. This phrase is easy to state and easy to leave opaque, so spell it out.

In ordinary Euclidean distance, moving one unit horizontally and moving one unit vertically are treated the same way. In Mahalanobis distance, the covariance matrix tells us which directions are naturally more variable. If a direction has large variance, then moving in that direction is less surprising, so the density decays more slowly there. If a direction has small variance, moving the same Euclidean amount is more surprising, so the density decays more quickly there.

So the multivariate Gaussian is still doing exactly what the one-dimensional Gaussian did: it penalizes distance from the mean. The only difference is that in several dimensions, "distance" must now respect the spread and dependence encoded by $\Sigma$.

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

$$X \sim \mathcal{N}(2, 9),$$

so the mean is $2$ and the standard deviation is $3$. About two-thirds of the mass lies within one standard deviation of the mean, namely in the interval $[-1,5]$, and almost all of the mass lies within a few standard deviations.

Now move to two dimensions very concretely. If

$$\mu=(0,0)^T, \qquad \Sigma_{11}=4,\qquad \Sigma_{22}=1,\qquad \Sigma_{12}=\Sigma_{21}=0,$$

then the mean vector says the cloud is centered at the origin, the first coordinate has variance $4$, and the second coordinate has variance $1$. So the spread in the first direction is larger than the spread in the second direction. That is why the contours are ellipses stretched more strongly along the first coordinate than along the second.

Because the off-diagonal terms are zero in this example, there is no rotational tilt. The principal axes of the ellipse line up with the coordinate axes.

Now change only the off-diagonal entries. Let $\Sigma$ be the $2\times 2$ covariance matrix with

$$\Sigma_{11}=1,\qquad \Sigma_{22}=1,\qquad \Sigma_{12}=\Sigma_{21}=0.8.$$

The correlation coefficient between coordinates is

$$\mathrm{Corr}(X_1,X_2)=\frac{\Sigma_{12}}{\sqrt{\Sigma_{11}\Sigma_{22}}}=\frac{0.8}{\sqrt{1\cdot 1}}=0.8.$$

This means the two coordinates tend to move together. So large values of $X_1$ tend to appear with large values of $X_2$, and small values of $X_1$ tend to appear with small values of $X_2$. Geometrically, the Gaussian contours are elongated along the diagonal direction

$$x_1 \approx x_2.$$

So the correct mental build-up is:

1. one-dimensional Gaussian: center plus spread;
2. random vector: several coordinates observed together;
3. mean vector: center of the cloud in multiple coordinates;
4. covariance matrix: individual spreads plus how coordinates move together;
5. multivariate Gaussian density: the same bell-shaped idea, but now in the geometry determined by that covariance matrix.

If instead $\Sigma_{12}$ were negative, then large values of one coordinate would tend to appear with small values of the other, and the elongation would run along

$$x_1 \approx -x_2.$$

This is the geometric meaning of off-diagonal covariance: it couples the coordinates and rotates the principal axes of the density.

The main mastery-level takeaway is that a Gaussian is not just "the bell curve formula." It is a model whose parameters have direct geometric meaning:

- the mean says where the mass is centered,
- the variance says how widely the mass is spread,
- and the covariance matrix says how the cloud is stretched and rotated in multiple dimensions.

That is why Gaussians appear everywhere in probability, statistics, and AI. They are mathematically tractable, but they are also unusually interpretable.

### Example 2-10: Bernoulli Exponential Family Form

This example is not introducing a new distribution. It is taking the ordinary Bernoulli model and rewriting it in a form whose algebra will reappear throughout statistics and machine learning.

Start with a Bernoulli random variable $X \in \{0,1\}$ and parameter

$$\rho = \mathbb{P}(X=1).$$

Then automatically

$$\mathbb{P}(X=0)=1-\rho.$$

The Bernoulli PMF can be written compactly as

$$p(X=x)=\rho^x(1-\rho)^{1-x}, \qquad x \in \{0,1\}.$$

This notation is worth unpacking slowly because it is easy to read it too quickly. If $x=1$, then

$$p(X=1)=\rho^1(1-\rho)^0=\rho.$$

If $x=0$, then

$$p(X=0)=\rho^0(1-\rho)^1=1-\rho.$$

So the exponents do not encode new probabilities. They are indicator exponents: they switch on the factor corresponding to the realized state and switch off the other one.

Now rewrite the same expression using logarithms:

$$p(X=x)=\exp\left(\log(\rho)x+\log(1-\rho)(1-x)\right).$$

Expand the exponent:

$$\log(\rho)x+\log(1-\rho)(1-x)=x\log\left(\frac{\rho}{1-\rho}\right)+\log(1-\rho).$$

This suggests defining the natural parameter

$$\eta=\log\left(\frac{\rho}{1-\rho}\right).$$

That quantity is the log-odds. It is not itself a probability. It ranges over the whole real line, whereas $\rho$ is restricted to the interval $(0,1)$.

Solve this definition for $\rho$:

$$e^{\eta}=\frac{\rho}{1-\rho}.$$

Multiply both sides by $(1-\rho)$:

$$e^{\eta}(1-\rho)=\rho.$$

Collect the $\rho$ terms:

$$e^{\eta}=\rho(1+e^{\eta}),$$

so

$$\rho=\frac{e^{\eta}}{1+e^{\eta}}, \qquad 1-\rho=\frac{1}{1+e^{\eta}}.$$

Substitute these into the PMF:

$$p(X=x)=\left(\frac{e^{\eta}}{1+e^{\eta}}\right)^x\left(\frac{1}{1+e^{\eta}}\right)^{1-x}.$$

Collect powers of $e^{\eta}$ and $(1+e^{\eta})$:

$$p(X=x)=\exp(\eta x)\exp\left(-\log(1+e^{\eta})\right).$$

So the canonical exponential-family form is

$$p(X=x)=\exp\left(\eta x-A(\eta)\right),$$

where

$$A(\eta)=\log(1+e^{\eta}).$$

The conceptual payoff is now visible. The original probability parameter $\rho$ appears nonlinearly in the ordinary Bernoulli formula, but after the reparameterization the observation $x$ appears linearly in the exponent. That is the structural pattern the exponential-family formalism is designed to expose.

A numerical example helps. If $\rho=0.8$, then the odds are $0.8/0.2=4$, so

$$\eta=\log 4.$$

Then

$$A(\eta)=\log(1+e^{\eta})=\log(1+4)=\log 5.$$

Therefore

$$p(X=1)=\exp(\eta-A(\eta))=\exp(\log 4-\log 5)=\frac{4}{5}=0.8,$$

and

$$p(X=0)=\exp(0-A(\eta))=\exp(-\log 5)=\frac{1}{5}=0.2.$$

So nothing about the Bernoulli law changed. We only changed coordinates on the parameter. The structural limit is important: this rewrite does not create a richer model. It is still the same one-parameter Bernoulli family, now written in coordinates that are convenient for optimization and theory.

### Example 2-11: Bernoulli Two-Parameter Form

The Bernoulli family can also be written with two numbers instead of one:

$$p(X=x;\eta_0,\eta_1)=\frac{\exp\left(\eta_1 x+\eta_0(1-x)\right)}{\exp(\eta_0)+\exp(\eta_1)}, \qquad x \in \{0,1\}.$$

This looks like a two-parameter model, but it is not actually a larger family. It is an over-parameterized way of writing the same one-parameter Bernoulli distribution.

Read the numerator by cases. If $x=1$, then

$$p(X=1)=\frac{e^{\eta_1}}{e^{\eta_0}+e^{\eta_1}}.$$

If $x=0$, then

$$p(X=0)=\frac{e^{\eta_0}}{e^{\eta_0}+e^{\eta_1}}.$$

So $\eta_1$ is the score attached to state $1$, and $\eta_0$ is the score attached to state $0$. The denominator normalizes those scores into valid probabilities.

Now divide numerator and denominator by $e^{\eta_0}$:

$$p(X=1)=\frac{e^{\eta_1-\eta_0}}{1+e^{\eta_1-\eta_0}}, \qquad p(X=0)=\frac{1}{1+e^{\eta_1-\eta_0}}.$$

Only the difference

$$\delta=\eta_1-\eta_0$$

matters. Once the difference is fixed, the probabilities are fixed.

That is why this representation is redundant. The parameter pair has two coordinates, but the actual Bernoulli distribution still has only one degree of freedom. Here "degree of freedom" means "number of independent numerical choices needed to determine the distribution." For Bernoulli, one number is enough, because once $\mathbb{P}(X=1)$ is chosen, $\mathbb{P}(X=0)$ is forced to be its complement.

An explicit example makes the redundancy concrete. Compare

$$ (\eta_0,\eta_1)=(0,2) \qquad \text{and} \qquad (\eta_0,\eta_1)=(5,7). $$

In both cases the difference is $2$. Therefore both produce

$$p(X=1)=\frac{e^2}{1+e^2}, \qquad p(X=0)=\frac{1}{1+e^2}.$$

Adding the same constant to both coordinates changes the raw scores by the same multiplicative factor, and normalization cancels that factor out. So this notation is useful for algebra, but it should not mislead you into thinking the Bernoulli family suddenly became two-dimensional.

### Beta and Dirichlet Distributions

The next question is different from all the examples so far. Up to this point, the random variable was usually an observed outcome such as a coin flip, a die roll, or a measurement. Now we want a distribution over a **parameter**.

For a Bernoulli model, the parameter is

$$\rho=\mathbb{P}(X=1).$$

This number is itself constrained:

$$0 \le \rho \le 1.$$

So if we want a probability distribution over possible values of $\rho$, we need a density whose support is the interval $[0,1]$. The standard family for that job is the Beta distribution.

That is the first conceptual point to keep explicit:

- Bernoulli is a distribution over outcomes $X \in \{0,1\}$.
- Beta is a distribution over possible Bernoulli parameters $\rho \in [0,1]$.

So Beta is not a new model for coin-flip outcomes themselves. It is a model for uncertainty about the coin's success probability.

The Beta density is

$$p(\rho)=\mathrm{Beta}(\rho;a,b)=\frac{\Gamma(a+b)}{\Gamma(a)\Gamma(b)}\rho^{a-1}(1-\rho)^{b-1}, \qquad 0 \le \rho \le 1,$$

where $a>0$ and $b>0$ are shape parameters.

The Gamma-function ratio is only a normalization constant. Its job is to make the total area equal to one:

$$\int_0^1 p(\rho)\,d\rho=1.$$

For understanding the shape of the distribution, the most important part is the factor

$$\rho^{a-1}(1-\rho)^{b-1}.$$

That factor tells us how the density behaves near $0$, near $1$, and in between.

Several vocabulary words need to be made explicit before going further.

- The **interior** of $[0,1]$ means the values strictly between $0$ and $1$.
- The **boundaries** are the endpoints $0$ and $1$.
- **Unimodal** means the density has one main peak.
- The **mode** is the point where the density is largest.

So if someone says "the Beta density is unimodal and places mass in the interior," they mean the curve has one peak somewhere between $0$ and $1$, rather than piling up at one or both endpoints.

Before the general formulas, it is best to build intuition from concrete examples.

First example: uniform uncertainty.

If

$$a=b=1,$$

then

$$p(\rho)=1 \qquad \text{for } 0 \le \rho \le 1.$$

So Beta$(1,1)$ is just the uniform distribution on $[0,1]$. This says every equal-length interval of possible probabilities receives the same prior mass. It does **not** say every exact value of $\rho$ is equally likely as a point event, because point probabilities are zero in continuous distributions.

Second example: one interior peak.

If

$$\rho \sim \mathrm{Beta}(5,5),$$

then the density is symmetric around $0.5$ and has a single peak near the center. This is what "unimodal" means in this context: there is one bell-like high region rather than two separated spikes. This prior expresses the belief that values near $0.5$ are more plausible than values near $0$ or $1$.

Third example: favoring one side.

If

$$\rho \sim \mathrm{Beta}(2,5),$$

then the mean is

$$\mathbb{E}[\rho]=\frac{2}{7}\approx 0.286.$$

So this prior leans toward smaller probabilities. In plain language, it says "before seeing data, I regard success probabilities below one-half as more plausible than success probabilities above one-half."

Fourth example: favoring extremes.

If

$$\rho \sim \mathrm{Beta}(0.3,0.3),$$

then the density is high near $0$ and near $1$, and relatively low in the middle. This says the coin is believed to be more likely strongly biased than close to fair.

This is also the place to explain why boundary spikes are not a paradox. When either shape parameter is below $1$, the density can become very large near $0$ or $1$. That does not violate probability rules, because a density value is not itself a probability. What matters is the area under the curve over an interval, and that total area remains finite and equal to one.

Two summary formulas are useful after the intuition is in place.

The mean is

$$\mathbb{E}[\rho]=\frac{a}{a+b}.$$

So the ratio $a:b$ controls which side of the interval is favored.

When

$$a>1 \qquad \text{and} \qquad b>1,$$

the mode is

$$\rho_{\mathrm{mode}}=\frac{a-1}{a+b-2}.$$

This is the location of the peak when the density has a genuine interior maximum. The condition matters: if one of the parameters is at most $1$, the density may peak at a boundary instead, so the interior mode formula no longer applies.

The second structural quantity is the total concentration

$$a+b.$$

Roughly speaking:

- the ratio $a:b$ says **where** the distribution is centered;
- the sum $a+b$ says **how tightly** it is concentrated around that preference.

For example,

$$\mathrm{Beta}(2,2) \qquad \text{and} \qquad \mathrm{Beta}(20,20)$$

are both centered at $0.5$, because in both cases

$$\frac{a}{a+b}=0.5.$$

But Beta$(20,20)$ is much more concentrated near $0.5$. So the first prior says "probably around fair, but with a lot of uncertainty," while the second says "strongly concentrated near fair."

The Dirichlet distribution is the multi-state version of this same idea.

Suppose a categorical variable has $d$ possible outcomes. Then its parameter is not one number but a probability vector

$$\theta=(\theta_1,\ldots,\theta_d),$$

where each coordinate is nonnegative and all coordinates sum to one:

$$\theta_j \ge 0 \quad \text{for all } j, \qquad \sum_{j=1}^d \theta_j=1.$$

So for a three-outcome variable, a legal parameter might be

$$\theta=(0.2,0.5,0.3).$$

The set of all such probability vectors is called the simplex. In the three-state case, the simplex is a filled triangle. Each point inside that triangle represents one legal categorical probability table.

The reason the simplex has one fewer free dimension than the number of coordinates is normalization. Once two coordinates are chosen, the last one is forced. In the example above,

$$\theta_3=1-0.2-0.5=0.3.$$

So even though the vector has three entries, only two of them are independent.

The Dirichlet density is

$$p(\theta)=\mathrm{Dir}(\theta;\alpha)=\frac{\Gamma(\alpha_0)}{\prod_{j=1}^d \Gamma(\alpha_j)}\prod_{j=1}^d \theta_j^{\alpha_j-1},$$

where

$$\alpha_0=\sum_{j=1}^d \alpha_j.$$

This looks more complicated than Beta only because there are more coordinates. Conceptually it plays the same role:

- it is a distribution over possible categorical probability tables;
- the relative sizes of the $\alpha_j$ values say which categories are favored;
- the total concentration $\alpha_0$ says how tightly the mass is pulled toward or away from the center.

The coordinate-wise mean is

$$\mathbb{E}[\theta_j]=\frac{\alpha_j}{\alpha_0}.$$

So if

$$\alpha=(8,2,2),$$

then

$$\mathbb{E}[\theta]=\left(\frac{8}{12},\frac{2}{12},\frac{2}{12}\right)=\left(\frac{2}{3},\frac{1}{6},\frac{1}{6}\right).$$

That prior says the first category is expected to be much more common than the other two.

If instead

$$\alpha=(2,2,2),$$

then

$$\mathbb{E}[\theta]=\left(\frac{1}{3},\frac{1}{3},\frac{1}{3}\right).$$

So the prior is symmetric across categories.

Now compare concentration while keeping the same proportions. If we increase to

$$\alpha=(20,20,20),$$

the mean stays

$$\left(\frac{1}{3},\frac{1}{3},\frac{1}{3}\right),$$

but the distribution becomes much more concentrated near the center of the simplex. If we decrease to

$$\alpha=(0.2,0.2,0.2),$$

the mass is pushed toward corners and edges. In plain language, that means the prior prefers sparse probability vectors in which one category gets most of the mass.

For $d=2$, the Dirichlet distribution reduces exactly to the Beta distribution. So Beta is not a separate disconnected topic. It is simply the two-category version of the same family.

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

A final pair of coin examples fixes the interpretation. Suppose $\rho$ is the head probability of a coin. A prior

$$\rho \sim \mathrm{Beta}(20,20)$$

encodes a strong belief that the coin is close to fair, because the mass is tightly concentrated around $0.5$. By contrast,

$$\rho \sim \mathrm{Beta}(0.3,0.3)$$

puts much more mass near $0$ and $1$, expressing the belief that the coin is likely to be strongly biased in one direction or the other. In the Dirichlet case, the same logic applies to a probability vector rather than a single number: large, balanced concentration parameters favor balanced interior probability tables, while small concentration parameters favor sparse near-corner tables.

### The Exponential Family

The exponential family is a modeling template, not one specific distribution. Its purpose is to expose a shared algebraic structure that appears in Bernoulli, categorical, Gaussian, Poisson, Gamma, Beta, Dirichlet, and many other common models.

The phrase "family" matters here. It means a collection of distributions indexed by parameters. The phrase "exponential family" means this collection can be written in a common exponential-shaped algebraic form. The value of that form is not aesthetic. It lets many different models share the same optimization and inference machinery.

The general form is

$$p_{\theta}(x)=h(x)\exp\left(\theta^{\top}\phi(x)-A(\theta)\right).$$

Before unpacking symbols, say what stays fixed and what changes.

- The observation $x$ is the realized data value.
- The model family fixes the functions $h(x)$ and $\phi(x)$ ahead of time.
- The parameter $\theta$ is what moves from one member of the family to another.

So the family is "all distributions obtained by varying $\theta$ while keeping the structural form fixed."

Every symbol in the expression has a specific role.

- $x$ is the observed value.
- $\phi(x)$ is a fixed feature vector computed from $x$. Its components are called sufficient statistics.
- $\theta$ is the natural parameter.
- $h(x)$ is the base measure, the part of the density or mass function that depends on $x$ but not on $\theta$.
- $A(\theta)$ is the log-partition function, chosen so that the distribution normalizes correctly.

The log-partition function is

$$A(\theta)=\log \int h(x)\exp\left(\theta^{\top}\phi(x)\right)\,dx,$$

with the integral replaced by a sum in discrete settings.

This definition is abstract, so the interpretation should be stated plainly. The log-density is linear in the fixed feature vector $\phi(x)$, while the function $A(\theta)$ is the correction term that makes the whole expression normalize properly. That is why exponential-family models are so tractable: all the nontrivial dependence on the parameter is concentrated into a relatively clean algebraic form.

Bernoulli is the simplest example. From the previous subsection,

$$p(X=x)=\exp\left(\eta x-\log(1+e^{\eta})\right).$$

Comparing with the template gives

$$h(x)=1, \qquad \phi(x)=x, \qquad \theta=\eta, \qquad A(\theta)=\log(1+e^{\theta}).$$

A second example is a one-dimensional Gaussian with known variance $\sigma^2$ and unknown mean $\mu$. Its density can be rearranged into exponential-family form with sufficient statistics $x$ and $x^2$. The exact coordinates are less important than the pattern: once the density is written as "fixed function of $x$" times "exponential of parameter times sufficient statistics," the same optimization and moment arguments apply.

The term sufficient statistic becomes concrete when we look at i.i.d. data. Suppose

$$D=\{x^{(1)},\ldots,x^{(m)}\}$$

are i.i.d. observations from an exponential-family model. Then

$$p_{\theta}(D)=\prod_{i=1}^m h(x^{(i)})\exp\left(\theta^{\top}\phi(x^{(i)})-A(\theta)\right).$$

Taking logarithms yields

$$\log p_{\theta}(D)=\sum_{i=1}^m \log h(x^{(i)})+\theta^{\top}\left(\sum_{i=1}^m \phi(x^{(i)})\right)-mA(\theta).$$

This expression shows exactly how the data enter the likelihood. The only data-dependent quantity coupled to $\theta$ is

$$S(D)=\sum_{i=1}^m \phi(x^{(i)}).$$

That is the operational meaning of sufficiency in this setting: once $S(D)$ is known, the likelihood as a function of $\theta$ no longer needs the full raw data sequence.

For Bernoulli, $\phi(x)=x$, so

$$S(D)=\sum_{i=1}^m x^{(i)}$$

is just the number of ones. The sequences

$$D_1=\{1,0,1,0\} \qquad \text{and} \qquad D_2=\{0,1,0,1\}$$

have the same sufficient statistic,

$$S(D_1)=S(D_2)=2,$$

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

Both views often use the same likelihood function, but they ask different questions. A frequentist estimator asks: if nature chose one fixed parameter value, what rule should I use to estimate it from repeated samples? A Bayesian posterior asks: after seeing this actual realized data set, which parameter values remain plausible, and how plausible are they relative to one another?

Maximum likelihood is the canonical frequentist estimate because it keeps only the data-fit term and ignores prior beliefs. A Bayesian update keeps both pieces: how well the parameter explains the data and how plausible the parameter looked before the data arrived.

The same coin-toss example makes the contrast concrete. Suppose we observe five flips with outcomes

$$D=\{1,1,0,1,0\}.$$

A frequentist summary is the single estimate

$$\hat{\rho}=3/5=0.6.$$

This answers the question "which one number best summarizes the data under the chosen estimation rule?"

A Bayesian analysis asks a different question, so it keeps a different object. Start from the prior

$$\rho \sim \mathrm{Beta}(2,2).$$

This means that before observing the five flips, the density over possible values of $\rho$ is proportional to

$$\rho^{2-1}(1-\rho)^{2-1}=\rho(1-\rho).$$

Now read the data explicitly. The sample

$$D=\{1,1,0,1,0\}$$

contains

$$m_1=3 \quad \text{successes}, \qquad m_0=2 \quad \text{failures}.$$

So the Bernoulli likelihood is proportional to

$$p(D \mid \rho)\propto \rho^3(1-\rho)^2.$$

Multiply prior and likelihood:

$$p(\rho \mid D)\propto p(D \mid \rho)p(\rho)\propto \rho^3(1-\rho)^2 \cdot \rho(1-\rho)=\rho^4(1-\rho)^3.$$

That is exactly the kernel of a Beta density with updated parameters

$$2+3=5 \qquad \text{and} \qquad 2+2=4.$$

So the posterior is

$$\rho \mid D \sim \mathrm{Beta}(5,4),$$

which answers a different question: "after seeing the five flips, how is probability mass distributed over the possible values of $\rho$?"

This is worth interpreting explicitly. The notation

$$\rho \mid D \sim \mathrm{Beta}(5,4)$$

does **not** mean the coin suddenly became a Beta random variable in the same sense that a flip outcome is Bernoulli. It means our uncertainty about the unknown Bernoulli parameter is now described by a Beta density with updated shape parameters $5$ and $4$.

The posterior still centers near the empirical proportion, but it does not collapse everything to a single number. It quantifies uncertainty around that value. That distinction becomes important whenever the sample is small, the parameter lies near a boundary, or prior information matters.

### Likelihood

For i.i.d. data $D = \{x^{(1)}, \dots, x^{(m)}\}$, the likelihood is

$$p(D \mid \theta) = \prod_i p(x^{(i)} \mid \theta)$$

The abbreviation i.i.d. stands for **independent and identically distributed**. Each word matters.

- **Independent** means that once the parameter $\theta$ is fixed, learning one sample value does not change the model probability assigned to the others.
- **Identically distributed** means each sample is generated from the same probability law $p_{\theta}(x)$, not from a different distribution at each time step.

So an i.i.d. sample is a collection of observations produced by repeatedly using the same model in the same way, with no extra dependence between draws after $\theta$ has been fixed.

A tiny coin-flip example makes this concrete. If we flip the same Bernoulli coin three times with head probability $\rho$, then

$$D=\{1,0,1\}$$

is i.i.d. because

- each flip uses the same Bernoulli law;
- and, once $\rho$ is fixed, the result of one flip does not alter the probability rule for the others.

By contrast, if the first observation came from one coin, the second from a different coin, and the third from a third coin, then the sample would not be identically distributed. If each observation depended on the previous one through a Markov rule, then the sample would not be independent.

The product form comes directly from the independence assumption. If the $m$ observations are conditionally independent given $\theta$, then the probability of observing the entire data set is the product of the per-observation probabilities.

The log-likelihood is

$$\ell(\theta) = \sum_i \log p(x^{(i)} \mid \theta).$$

Taking logs does not change which parameter maximizes the objective, because the logarithm is strictly increasing. It only turns products into sums, which are easier to differentiate and reason about.

The principle of maximum likelihood says to choose the parameter value that makes the observed data look most probable under the model. It is important to state explicitly what varies and what stays fixed: after we have observed $D$, the data are treated as fixed, and the likelihood is a function of $\theta$. It is not a probability distribution over $\theta$, and it does not have to integrate to one over parameter space.

For the small Bernoulli sample

$$D=\{1,0,1\},$$

the likelihood is

$$p(D \mid \rho)=\rho(1-\rho)\rho=\rho^2(1-\rho).$$

This expression is worth unpacking mechanically. The first factor $\rho$ comes from the first success, the factor $(1-\rho)$ comes from the observed failure, and the final factor $\rho$ comes from the last success. The whole product is therefore "multiply the probability of each observed outcome under the candidate parameter."

If we try three candidate parameters, we get

$$p(D \mid 0.2)=0.032,\qquad p(D \mid 0.5)=0.125,\qquad p(D \mid 0.8)=0.128.$$

So among those candidates, $\rho=0.8$ explains the observed data slightly better than $\rho=0.5$, while $\rho=0.2$ fits badly. That does not mean the true parameter is definitely $0.8$; it means only that, within this comparison, the observed sample looks more compatible with $\rho=0.8$ than with the other two candidates.

A common wrong notion is to treat $p(D \mid \rho)$ as if it were a probability distribution over $\rho$. It is not. One concrete way to see this is that it does not normalize over parameter space. For this data,

$$p(D \mid \rho)=\rho^2(1-\rho).$$

If we integrate this function over $\rho \in [0,1]$, we get

$$\int_0^1 \rho^2(1-\rho)\,d\rho=\int_0^1 (\rho^2-\rho^3)\,d\rho=\left[\frac{\rho^3}{3}-\frac{\rho^4}{4}\right]_0^1=\frac{1}{3}-\frac{1}{4}=\frac{1}{12},$$

not $1$. So likelihood is not meant to be "the probability that $\rho$ equals a value." Likelihood ranks parameters by data fit. To get a probability distribution over $\rho$, you must multiply by a prior and renormalize. For example, with a uniform prior $\rho \sim \mathrm{Beta}(1,1)$, the posterior is $\mathrm{Beta}(3,2)$, whose (normalized) density is proportional to the same kernel $\rho^2(1-\rho)$.

That last sentence is worth unpacking once. A $\mathrm{Beta}(1,1)$ prior has density

$$p(\rho)=1 \qquad \text{for } 0 \le \rho \le 1.$$

So multiplying the likelihood kernel

$$\rho^2(1-\rho)$$

by the prior changes nothing except the eventual normalization. The exponents are still

$$2 \quad \text{on } \rho \qquad \text{and} \qquad 1 \quad \text{on } (1-\rho),$$

which is exactly the Beta$(3,2)$ pattern. So the posterior family label is not magic notation; it is just the normalized version of the same kernel.

### Probability Versus Likelihood

The same algebraic expression can play two different roles depending on what is held fixed. When $\theta$ is fixed and $x$ varies, the quantity $p(x \mid \theta)$ is a probability model over possible observations. When the observation $x$ has already been fixed and $\theta$ varies, the same expression is treated as a likelihood function of the parameter.

This distinction is one of the most important "do not blur these together" rules in the chapter. The formula may look identical on paper, but the question being asked is different.

For Bernoulli data, if we observe a single success $x=1$, then

$$p(x=1 \mid \rho)=\rho.$$

Viewed as a function of the data, this is a perfectly ordinary probability rule: for fixed $\rho$, the probabilities of the two possible observations are

$$p(x=0 \mid \rho)=1-\rho,\qquad p(x=1 \mid \rho)=\rho,$$

and those two numbers add to one.

But viewed as a function of $\rho$ after observing $x=1$, the same expression becomes the likelihood $L(\rho)=\rho$. That likelihood does not integrate to one over $\rho \in [0,1]$, nor is it supposed to. Its job is only to rank parameter values by how well they explain the observation.

So the right mental checklist is:

- probability mode: parameter fixed, data allowed to vary;
- likelihood mode: data fixed, parameter allowed to vary.

If that checklist is not kept explicit, later Bayesian formulas become much harder to interpret correctly.

### Example 2-12: Bernoulli Likelihood

Suppose we observe $m$ Bernoulli samples, with $m_1$ ones and $m_0$ zeros, so that $m=m_1+m_0$. Start from the Bernoulli PMF for one observation:

$$p(x \mid \rho)=\rho^x(1-\rho)^{1-x}.$$

For the full data set, multiply one factor for each observation:

$$p(D \mid \rho)=\prod_{i=1}^m \rho^{x^{(i)}}(1-\rho)^{1-x^{(i)}}.$$

Collecting exponents gives

$$p(D \mid \rho)=\rho^{m_1}(1-\rho)^{m_0}.$$

So the log-likelihood is

$$\ell(\rho) = m_1 \log \rho + m_0 \log(1-\rho).$$

This expression has a transparent interpretation. The term $m_1 \log \rho$ rewards large $\rho$ when many ones were observed. The term $m_0 \log(1-\rho)$ rewards small $\rho$ when many zeros were observed. The maximizing value of $\rho$ balances those two pressures and ends up at the empirical frequency of ones.

If the observed sample is all zeros or all ones, the maximizer lies on the boundary $\rho=0$ or $\rho=1$. Otherwise the unique optimum lies in the interior of the interval.

<p align="center">
  <img src="../notes/02_probability_reconstructed/assets/figure_2_12_bernoulli_likelihood.png" alt="Bernoulli likelihood curves" width="860">
</p>

Each panel holds the observed data fixed and varies only the parameter $\rho$. The curve peaks where the model's predicted head probability best matches the observed proportion of heads. When the data rule out part of parameter space completely, the log-likelihood drops toward negative infinity at the incompatible boundary.

For the data set $D=\{0,1\}$, the likelihood is

$$p(D \mid \rho)=\rho(1-\rho),$$

which is zero at $\rho=0$ and $\rho=1$ because either extreme makes one of the two observations impossible. The peak therefore occurs in the interior, specifically at $\rho=1/2$.

This example is useful because it isolates the logic of likelihood fitting. The sample contains one success and one failure, so the best-fitting Bernoulli parameter is exactly the balanced value that makes both outcomes equally plausible.

### Example 2-13: Gaussian Likelihood

For a one-dimensional Gaussian with variance fixed at one, the likelihood as a function of $\mu$ becomes more sharply peaked as the number of samples grows. That sharpening is the visual signature that more data reduce parameter uncertainty: many values of $\mu$ may explain three observations reasonably well, but far fewer values remain plausible once twenty observations cluster around the same region.

The algebra behind that picture is worth stating. If

$$x^{(i)} \sim \mathcal{N}(\mu,1),$$

then the density of one sample is

$$p(x^{(i)} \mid \mu)=\frac{1}{\sqrt{2\pi}}\exp\left(-\frac{(x^{(i)}-\mu)^2}{2}\right).$$

For $m$ observations, the likelihood is the product of these terms, so the log-likelihood is

$$\ell(\mu)= -\frac{m}{2}\log(2\pi)-\frac{1}{2}\sum_{i=1}^m (x^{(i)}-\mu)^2.$$

Everything except the squared-error sum is constant in $\mu$. So maximizing the Gaussian likelihood in $\mu$ is exactly the same optimization problem as minimizing

$$\sum_{i=1}^m (x^{(i)}-\mu)^2.$$

<p align="center">
  <img src="../notes/02_probability_reconstructed/assets/figure_2_13_gaussian_likelihood.png" alt="Gaussian likelihood curves" width="860">
</p>

The dots along the top of each panel are the observed samples. The curve below them is the log-likelihood as a function of the Gaussian mean. As $m$ increases, the curve narrows and the maximizing value moves toward the visual center of the observed data cloud.

If the observed values are $-0.5$, $0.4$, and $1.3$, then the Gaussian likelihood in $\mu$ is largest near the arithmetic average

$$\bar x = \frac{-0.5+0.4+1.3}{3}=0.4.$$

The entire curve is simply another way of visualizing how much squared-error penalty is paid for choosing a mean away from that center. Values of $\mu$ far from $0.4$ make all three squared deviations larger, so the log-likelihood drops. This is the geometric reason the sample mean appears as the Gaussian MLE.

It helps to check one comparison numerically. At $\mu=0.4$ the squared-error total is

$$(-0.5-0.4)^2+(0.4-0.4)^2+(1.3-0.4)^2=0.81+0+0.81=1.62.$$

At $\mu=1.0$ the squared-error total is

$$(-0.5-1.0)^2+(0.4-1.0)^2+(1.3-1.0)^2=2.25+0.36+0.09=2.70.$$

Because the second total is larger, the log-likelihood at $\mu=1.0$ is smaller. So the Gaussian-likelihood picture is just another way of seeing the penalty for choosing a mean too far from the data cloud.

### Maximum Likelihood Estimation

Maximum likelihood estimation, or MLE, means choosing the parameter value that maximizes the likelihood of the observed data:

$$\hat{\theta}_{\text{MLE}}=\arg\max_\theta p(D \mid \theta).$$

Because the logarithm is strictly increasing, this is equivalent to

$$\hat{\theta}_{\text{MLE}}=\arg\max_\theta \ell(\theta),$$

where $\ell(\theta)$ denotes the log-likelihood. In practice one almost always works with the log-likelihood because products become sums and derivatives become manageable.

For a Bernoulli distribution,

$$\ell(\rho) = m_1 \log \rho + m_0 \log(1-\rho).$$

Differentiating gives

$$\frac{\partial \ell}{\partial \rho} = \frac{m_1}{\rho} - \frac{m_0}{1-\rho}.$$

Setting this to zero yields

$$\hat{\rho}_{\text{MLE}} = \frac{m_1}{m}.$$

The algebra is worth writing out explicitly:

$$\frac{m_1}{\rho} - \frac{m_0}{1-\rho} = 0 \quad \Longrightarrow \quad m_1(1-\rho) = m_0\rho \quad \Longrightarrow \quad m_1 = (m_0+m_1)\rho.$$

Since $m_0+m_1 = m$, we obtain $\hat{\rho}_{\text{MLE}} = m_1/m$. The second derivative is

$$\frac{\partial^2 \ell}{\partial \rho^2} = -\frac{m_1}{\rho^2} - \frac{m_0}{(1-\rho)^2} < 0,$$

so the stationary point is a strict global maximum whenever it lies in the interior.

This result has a clear interpretation. The model parameter $\rho$ is the probability of seeing a $1$, so the likelihood is maximized when the model's success probability matches the observed success frequency.

For a Gaussian with mean $\mu$ and variance $\nu = \sigma^2$,

$$\hat{\mu}_{\text{MLE}} = \frac{1}{m}\sum_i x^{(i)}$$

$$\hat{\nu}_{\text{MLE}} = \frac{1}{m}\sum_i (x^{(i)} - \hat{\mu})^2.$$

For the mean parameter, the derivation comes from expanding the log-likelihood into a constant minus a squared-error term:

$$\ell(\mu) = \text{const} - \frac{1}{2\nu}\sum_i (x^{(i)}-\mu)^2.$$

Differentiating with respect to $\mu$ gives

$$\frac{\partial \ell}{\partial \mu} = \frac{1}{\nu}\sum_i (x^{(i)}-\mu),$$

so setting the derivative to zero forces $\mu$ to equal the arithmetic average of the observations. The variance estimate is then the average squared deviation around that fitted mean. For a discrete distribution with probabilities $\rho_x$, the MLE is the empirical frequency of each state.

The variance formula often causes confusion because many statistics courses also teach

$$\frac{1}{m-1}\sum_i (x^{(i)}-\hat{\mu})^2.$$

That is the unbiased sample-variance estimator. It is not the Gaussian maximum-likelihood estimator. The MLE uses $1/m$ because it is chosen to maximize the likelihood, not to make the estimator unbiased across repeated samples. These are different optimization goals, so they produce different formulas.

So the three flagship MLE examples all follow the same pattern:

- Bernoulli: match the model mean to the sample proportion;
- Gaussian mean: match the model center to the sample average;
- discrete categorical table: copy empirical frequencies into the parameter table.

The general lesson is that MLE tries to make the model imitate the observed sample as closely as the model family allows.

An explicit discrete example makes the frequency rule concrete. Suppose the data over states $\{a,b,c\}$ are

$$D=\{a,c,a,b,a,c\}.$$

Then the counts are $m_a=3$, $m_b=1$, and $m_c=2$, so the MLE is

$$\hat{\rho}_a=3/6,\qquad \hat{\rho}_b=1/6,\qquad \hat{\rho}_c=2/6$$

The estimate simply copies empirical proportions into the model.

### Example 2-14: Bernoulli MLE

This example should be read as the most basic MLE computation in the chapter.

Suppose we observe Bernoulli data with

$$m_1 \quad \text{ones}, \qquad m_0 \quad \text{zeros}, \qquad m=m_1+m_0.$$

From the earlier likelihood derivation,

$$p(D \mid \rho)=\rho^{m_1}(1-\rho)^{m_0}.$$

The maximizer is

$$\hat{\rho} = \frac{m_1}{m}$$

because the model fits best when its predicted success probability matches the observed success frequency.

Now do one concrete sample slowly. Let

$$D=\{1,1,0,1,0\}.$$

Then

$$m_1=3,\qquad m_0=2,\qquad m=5.$$

So the likelihood is

$$p(D \mid \rho)=\rho^3(1-\rho)^2.$$

The MLE is therefore

$$\hat{\rho}=\frac{3}{5}=0.6$$

The interpretation is immediate: the fitted Bernoulli model predicts success with probability $0.6$ on future draws, because $60\%$ of the observed sample consisted of successes.

It is worth checking the logic against two nearby parameter values. At $\rho=0.6$, the model agrees with the sample proportion exactly. At $\rho=0.2$, the model says successes are rare, which clashes with the data because the sample contains three successes out of five. At $\rho=0.9$, the model says failures are rare, which also clashes with the data because the sample contains two failures. The MLE sits between those extremes at the value that best balances both kinds of observations.

### Example 2-15: Gaussian MLE

For a one-dimensional Gaussian with both mean and variance unknown, the MLEs are the sample mean and the average squared deviation around that mean:

$$\hat{\mu} = \frac{1}{m}\sum_i x^{(i)}$$

$$\hat{\nu} = \frac{1}{m}\sum_i (x^{(i)}-\hat{\mu})^2$$

Now compute them explicitly for the sample

$$D=\{2,4,7\}.$$

There are

$$m=3$$

observations, so the fitted mean is

$$\hat{\mu}=\frac{2+4+7}{3}=\frac{13}{3}$$

This number is about $4.33$, which sits near the visual center of the three observations.

Next compute the squared deviations from that fitted center:

$$2-\frac{13}{3}=-\frac{7}{3},\qquad 4-\frac{13}{3}=-\frac{1}{3},\qquad 7-\frac{13}{3}=\frac{8}{3}.$$

Square them:

$$\left(-\frac{7}{3}\right)^2=\frac{49}{9},\qquad \left(-\frac{1}{3}\right)^2=\frac{1}{9},\qquad \left(\frac{8}{3}\right)^2=\frac{64}{9}.$$

Add them:

$$\frac{49}{9}+\frac{1}{9}+\frac{64}{9}=\frac{114}{9}=\frac{38}{3}.$$

Now divide by $m=3$ to get the Gaussian MLE for the variance:

$$\hat{\nu}=\frac{1}{3}\left[\left(2-\frac{13}{3}\right)^2+\left(4-\frac{13}{3}\right)^2+\left(7-\frac{13}{3}\right)^2\right]$$

which simplifies to

$$\hat{\nu}=\frac{1}{3}\cdot \frac{38}{3}=\frac{38}{9}\approx 4.22.$$

So the Gaussian fit is built in two explicit stages:

1. choose the center that minimizes total squared error;
2. measure the average squared residual size around that fitted center.

That second number is not the unbiased sample variance from introductory statistics. It is the Gaussian maximum-likelihood variance, which uses division by $m$ because it comes from maximizing the likelihood.

### Example 2-16: Discrete MLE

For a discrete distribution over states $x$, the MLE copies empirical frequencies into the probability table:

$$\hat{\rho}_x = \frac{m_x}{m}$$

where $m_x$ is the count of state $x$ in the data.

Work through the concrete sample

$$D=\{a,c,a,b,a,c\}.$$

There are

$$m=6$$

observations. Count each state:

$$m_a=3,\qquad m_b=1,\qquad m_c=2$$

Now divide each count by the total sample size:

$$\hat{\rho}_a=\frac{3}{6},\qquad \hat{\rho}_b=\frac{1}{6},\qquad \hat{\rho}_c=\frac{2}{6}$$

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

$$p_{\theta}(x) = h(x)\exp\left(\theta^{\top}\phi(x) - A(\theta)\right)$$

the log-likelihood of i.i.d. data is

$$\ell(\theta) = \sum_i \log h(x^{(i)}) + \theta^{\top} \sum_i \phi(x^{(i)}) - m A(\theta)$$

Differentiating with respect to $\theta$ gives

$$\nabla_\theta \ell(\theta) = \sum_i \phi(x^{(i)}) - m \nabla_\theta A(\theta).$$

For exponential families,

$$\nabla_\theta A(\theta) = \mathbb{E}_\theta[\phi(X)],$$

so the first-order optimality condition becomes

$$\frac{1}{m}\sum_i \phi(x^{(i)}) = \mathbb{E}_\theta[\phi(X)].$$

This is the explicit moment-matching statement: the fitted model reproduces the empirical averages of the sufficient statistics. That identity is one of the main reasons exponential families are so useful.

The phrase moment matching should be read literally. The left-hand side is the empirical average of the sufficient statistics computed from the observed sample. The right-hand side is the model's expected value of those same statistics under parameter $\theta$. At the optimum, those two objects agree.

For Bernoulli, the sufficient statistic is just $X$, so moment matching says

$$\mathbb{E}_\theta[X] = \frac{1}{m}\sum_i x^{(i)}.$$

But the model expectation of $X$ is exactly $\rho$, so the condition reduces to

$$\rho = \text{sample mean},$$

which reproduces the familiar Bernoulli MLE immediately. So the Bernoulli success frequency is not an isolated trick; it is the simplest case of a general exponential-family principle.

### Overfitting

Likelihood alone can overfit. If a model is too flexible and the data set is too small, the MLE may explain the training data perfectly while generalizing poorly. Histogram models make this especially clear: as the number of bins grows, the likelihood on the training data can keep increasing even when the estimate becomes a bad predictor. In the extreme limit where each observation gets its own tiny bin, the model can memorize the sample rather than discover a stable distributional pattern.

The core reason is that pure likelihood asks only, "how well can this model explain the data already seen?" It does not ask whether the fitted pattern is robust enough to predict new data. A model with many parameters can exploit accidental quirks of a small sample and thereby earn a high training score for the wrong reason.

A toy example is enough to show the mechanism. If eight data points occupy eight distinct locations and we fit a histogram with sixty-four bins, most bins are empty and a few bins receive all the mass. The training likelihood becomes large because each observed sample falls into a narrow high-density bin, but a new sample landing between those bins receives nearly zero support. The model has learned the sample, not the underlying distribution.

<p align="center">
  <img src="../notes/02_probability_reconstructed/assets/figure_2_17_histograms.png" alt="Histogram likelihood progression" width="860">
</p>

The three histograms make the overfitting mechanism visible. With one bin the model is too coarse to capture any structure. With a moderate number of bins it starts to reflect the sample without becoming too brittle. With too many bins it effectively memorizes the observations, assigning high density exactly where data occurred and poor predictions everywhere else.

The key lesson is that "higher likelihood" is not enough unless we specify on which data that likelihood is measured. Training likelihood can keep improving while predictive performance on new data gets worse. Overfitting is exactly that mismatch between memorizing the observed sample and learning a pattern that transfers.

### Posterior Distributions

In the Bayesian view, we keep a distribution over parameters:

$$p(\theta \mid D) \propto p(D \mid \theta)p(\theta).$$

The notation

$$p(\theta \mid D)$$

should be read in the most literal possible way: it is the conditional distribution of the parameter $\theta$ given the observed data $D$. So the posterior is not a brand-new kind of mathematical object. It is the ordinary conditional-probability idea from earlier in the chapter, now applied to parameter uncertainty instead of ordinary events.

The missing normalization constant is the evidence

$$p(D) = \int p(D \mid \theta)p(\theta)\,d\theta.$$

So Bayes' rule in full form is

$$p(\theta \mid D) = \frac{p(D \mid \theta)p(\theta)}{p(D)}.$$

Each term has a separate role.

- The prior $p(\theta)$ encodes what looked plausible before the data arrived.
- The likelihood $p(D \mid \theta)$ measures how well each parameter explains the observed data.
- The evidence $p(D)$ is the total probability of the data after averaging over all parameter values allowed by the prior.
- The posterior $p(\theta \mid D)$ is the normalized result after combining the first two pieces.

The posterior therefore does something different from point estimation. A point estimator returns one preferred number, such as $\hat{\rho}=0.6$. A posterior returns a whole distribution over $\rho$, which tells us not only where the plausible values are centered but also how spread out that uncertainty still is after observing the data. This matters conceptually because it keeps uncertainty visible rather than hiding it inside one summary number, and it matters computationally because such full updates are easy to compute exactly only in special cases, such as conjugate prior-likelihood pairs.

For a concrete update, start with

$$\rho \sim \mathrm{Beta}(2,2)$$

and observe

$$D=\{1,0,1\}.$$

Now spell out the pieces instead of jumping directly to the answer. The prior density is

$$p(\rho)=6\rho(1-\rho),$$

because Beta$(2,2)$ has normalization constant

$$\frac{\Gamma(4)}{\Gamma(2)\Gamma(2)}=6.$$

The data contain

$$m_1=2 \quad \text{ones}, \qquad m_0=1 \quad \text{zero},$$

so the Bernoulli likelihood is

$$p(D \mid \rho)=\rho^2(1-\rho).$$

Multiply prior and likelihood:

$$p(\rho \mid D)\propto p(D \mid \rho)p(\rho)\propto \rho^2(1-\rho)\cdot \rho(1-\rho)=\rho^3(1-\rho)^2.$$

That kernel has exponent

$$3$$

on $\rho$ and exponent

$$2$$

on $(1-\rho)$. Since a Beta$(a,b)$ density has the form

$$\rho^{a-1}(1-\rho)^{b-1},$$

we identify

$$a-1=3,\qquad b-1=2,$$

so

$$a=4,\qquad b=3.$$

Therefore the posterior is

$$\rho \mid D \sim \mathrm{Beta}(4,3).$$

Now the pseudo-count interpretation can be stated cleanly. The prior Beta$(2,2)$ contributes one exponent to $\rho$ and one exponent to $(1-\rho)$ before any real data are observed. The actual sample contributes two more powers of $\rho$ and one more power of $(1-\rho)$. After multiplication, the exponents add. That is why the posterior behaves as if prior information and observed counts have been combined.

That pseudo-count language is an interpretation of the algebra, not a literal story that extra coin flips physically occurred. What is literally true is simpler: the prior contributes exponents, the data contribute exponents, and multiplication adds those exponents. The pseudo-count mnemonic is useful only because it mirrors that exponent bookkeeping.

It is also worth computing the evidence term once, because it is often treated as mysterious. Here the likelihood kernel is

$$p(D \mid \rho)=\rho^2(1-\rho),$$

and the $\mathrm{Beta}(2,2)$ prior density is

$$p(\rho)=6\rho(1-\rho).$$

So the unnormalized posterior is

$$p(D \mid \rho)p(\rho)=6\rho^3(1-\rho)^2.$$

The evidence is the integral of this quantity:

$$p(D)=\int_0^1 6\rho^3(1-\rho)^2\,d\rho.$$

Expand the polynomial and integrate term by term:

$$\int_0^1 \rho^3(1-\rho)^2\,d\rho=\int_0^1 (\rho^3-2\rho^4+\rho^5)\,d\rho=\left[\frac{1}{4}-\frac{2}{5}+\frac{1}{6}\right]=\frac{1}{60}.$$

Therefore

$$p(D)=6\cdot \frac{1}{60}=\frac{1}{10}.$$

Dividing the unnormalized posterior by $p(D)$ gives the normalized posterior density:

$$p(\rho \mid D)=\frac{6\rho^3(1-\rho)^2}{1/10}=60\rho^3(1-\rho)^2,$$

which is exactly the $\mathrm{Beta}(4,3)$ density. So the evidence is simply the normalization constant that makes the posterior integrate to one.

### Example 2-18: Beta-Bernoulli Conjugacy

If the likelihood is Bernoulli and the prior is $\mathrm{Beta}(a,b)$, then the posterior is still Beta:

$$\rho \mid D \sim \mathrm{Beta}(a+m_1, b+m_0).$$

The derivation is short enough to write explicitly. The prior contributes

$$p(\rho) \propto \rho^{a-1}(1-\rho)^{b-1},$$

and the Bernoulli likelihood contributes

$$p(D \mid \rho) \propto \rho^{m_1}(1-\rho)^{m_0}.$$

Multiplying them gives

$$p(\rho \mid D) \propto \rho^{a+m_1-1}(1-\rho)^{b+m_0-1},$$

which is exactly the kernel of another Beta density. This is the simplest example of conjugacy.

The structural reason conjugacy works is that the prior and the likelihood are built from the same two algebraic pieces, $\rho$ and $(1-\rho)$. Multiplying them merely adds exponents, so the posterior stays in the same family. That is the general pattern behind conjugate priors: family-preserving algebra.

If we plug in $a=b=2$ and observe $m_1=3$, $m_0=1$, then

$$\rho \mid D \sim \mathrm{Beta}(5,3).$$

The arithmetic should be read explicitly:

$$a+m_1=2+3=5,\qquad b+m_0=2+1=3.$$

The posterior is more concentrated than the prior because more information has been accumulated, and it is shifted toward heads because the data contain more ones than zeros. This can be read numerically as well. The prior Beta$(2,2)$ has total concentration

$$2+2=4,$$

while the posterior Beta$(5,3)$ has total concentration

$$5+3=8.$$

So the posterior carries more total mass and is therefore narrower. At the same time, its center moves toward heads because the first shape parameter increased by more than the second. In other words, the update changes both location and confidence: the center moves toward the evidence, and the distribution narrows because the effective sample size has increased.

### Worked Example: Dirichlet-Categorical Pseudo-Counts

The categorical analogue of Beta-Bernoulli conjugacy is Dirichlet-Categorical conjugacy. Let a three-class probability vector satisfy

$$\theta=(\theta_1,\theta_2,\theta_3) \sim \mathrm{Dir}(2,2,2).$$

Now observe four class labels with counts

$$m=(3,1,0).$$

Spell out what the count vector means before doing the update:

- class $1$ was observed $3$ times,
- class $2$ was observed $1$ time,
- class $3$ was observed $0$ times.

The prior Dirichlet parameters are

$$ (2,2,2), $$

so the coordinatewise update is

$$2+3=5,\qquad 2+1=3,\qquad 2+0=2.$$

Therefore

$$\theta \mid D \sim \mathrm{Dir}(5,3,2).$$

This is the multi-class pseudo-count interpretation in explicit form. The prior behaves like two virtual observations in each class. The data then add three more observations to class $1$, one to class $2$, and none to class $3$.

The posterior mean is

$$\mathbb{E}[\theta \mid D] = ( \frac{5}{10}, \frac{3}{10}, \frac{2}{10} ) =(0.5,0.3,0.2).$$

The denominator

$$10$$

comes from the total posterior concentration:

$$5+3+2=10.$$

So the posterior mean is not arbitrary componentwise division. Each coordinate is being divided by the sum of all updated Dirichlet parameters.

The posterior mean for class $3$ is still positive even though class $3$ was never observed. The reason is explicit in the numbers: the posterior parameter for that class is

$$2+0=2,$$

so the posterior mean becomes

$$\frac{2}{5+3+2}=\frac{2}{10}=0.2.$$

Compare that with pure MLE. Using only the observed counts would give

$$\left(\frac{3}{4},\frac{1}{4},0\right),$$

so the unseen class would receive probability zero. The Dirichlet prior prevents that collapse by keeping some prior mass on every class. That is the smoothing effect: "not yet seen" is treated as weaker information than "known to be impossible."

### Posterior Estimators

After computing a posterior distribution, we still face a practical question: do we keep the full posterior, or do we compress it to one representative number?

When a single number is required, two common choices are the posterior mean and the MAP estimate.

The posterior mean is

$$\hat{\theta}_{\mathrm{PM}}=\mathbb{E}_{p(\theta \mid D)}[\theta].$$

This is literally the average of $\theta$ under the posterior distribution. It uses the entire posterior shape, not just one high-density point.

The MAP estimate is

$$\hat{\theta}_{\mathrm{MAP}}=\arg\max_{\theta} p(\theta \mid D).$$

This is the mode of the posterior: the single parameter value at which the posterior density is largest.

These two estimators answer different questions.

- The posterior mean asks: if we average over posterior uncertainty, where is the center of mass?
- The MAP asks: which single parameter value is most favored locally by the posterior density?

Because those questions are different, the answers generally differ.

For the Beta-Bernoulli model, if the prior is $\mathrm{Beta}(a,b)$ and the data contain $m_1$ ones and $m_0$ zeros, then the posterior is

$$\mathrm{Beta}(a+m_1,b+m_0).$$

The posterior mean is therefore

$$\hat{\rho}_{\mathrm{PM}}=\frac{a+m_1}{a+b+m_1+m_0}.$$

If the updated Beta parameters are both greater than $1$, the interior MAP estimate is

$$\hat{\rho}_{\mathrm{MAP}}=\frac{a+m_1-1}{a+b+m_1+m_0-2}.$$

The condition matters. If either updated shape parameter is at most $1$, then the posterior mode moves to a boundary point, so the simple interior formula no longer applies. That is a structural limit, not a cosmetic detail.

Consider the posterior

$$\rho \mid D \sim \mathrm{Beta}(5,3).$$

Then

$$\hat{\rho}_{\mathrm{PM}}=\frac{5}{8}=0.625$$

and

$$\hat{\rho}_{\mathrm{MAP}}=\frac{5-1}{5+3-2}=\frac{4}{6}\approx 0.667.$$

The MAP is larger because it selects the peak of the density, while the posterior mean averages over all values of $\rho$ weighted by posterior mass. If the distribution is asymmetric, those two operations do not coincide.

It is helpful to place MLE next to them conceptually. MLE ignores the prior and keeps only the parameter value that maximizes the likelihood. MAP adds the prior before maximizing. The posterior mean goes one step further and averages instead of maximizing. So the three estimators compress information differently:

- MLE keeps only the likelihood peak.
- MAP keeps only the posterior peak.
- Posterior mean keeps the whole posterior and then averages.

### Example 2-19: Bernoulli Posterior Estimates

Work through one small data set completely. Let

$$D=\{1,1,0\}.$$

So the data contain

$$m_1=2 \quad \text{successes}, \qquad m_0=1 \quad \text{failure}.$$

The Bernoulli likelihood is therefore

$$p(D \mid \rho)=\rho^2(1-\rho)^1.$$

If we ignore the prior and compute MLE, we maximize this likelihood over $\rho$. For Bernoulli data, the MLE is the empirical fraction of ones:

$$\hat{\rho}_{\mathrm{MLE}}=\frac{2}{3}\approx 0.667.$$

Now include the prior

$$\rho \sim \mathrm{Beta}(2,2).$$

The prior density is proportional to

$$\rho^{2-1}(1-\rho)^{2-1}=\rho(1-\rho).$$

Multiply prior and likelihood:

$$p(\rho \mid D) \propto \rho^2(1-\rho)^1 \cdot \rho^1(1-\rho)^1=\rho^3(1-\rho)^2.$$

So the posterior is

$$\rho \mid D \sim \mathrm{Beta}(4,3).$$

Now compute three different point summaries.

The posterior mean is

$$\hat{\rho}_{\mathrm{PM}}=\frac{4}{4+3}=\frac{4}{7}\approx 0.571.$$

The MAP estimate is

$$\hat{\rho}_{\mathrm{MAP}}=\frac{4-1}{4+3-2}=\frac{3}{5}=0.6.$$

The MLE, from above, is

$$\hat{\rho}_{\mathrm{MLE}}=\frac{2}{3}\approx 0.667.$$

Putting them side by side,

$$\hat{\rho}_{\mathrm{PM}} \approx 0.571, \qquad \hat{\rho}_{\mathrm{MAP}}=0.6, \qquad \hat{\rho}_{\mathrm{MLE}}\approx 0.667.$$

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

$$\mathrm{Beta}(6,3).$$

If we had processed all five observations at once, we would obtain exactly the same answer. Sequential updating is therefore not an approximation; it is algebraically equivalent to batch updating when the model assumptions are unchanged.

### Example 2-20: Coin Toss Hyper-Prior

Sometimes we are uncertain not only about the parameter $\rho$, but also about which prior story is appropriate. A hyper-prior keeps that higher-level uncertainty explicit.

One simple construction is a mixture of two Beta priors:

- a "fair-coin-like" prior, concentrated near $0.5$;
- an "extreme-coin" prior, concentrated near $0$ and $1$.

Introduce a latent variable

$$H \in \{\mathrm{fair},\mathrm{extreme}\}.$$

Then the model can be written as

$$H \sim \mathrm{Bernoulli}(\pi),$$

$$\rho \mid H=\mathrm{fair} \sim \mathrm{Beta}(20,20),$$

$$\rho \mid H=\mathrm{extreme} \sim \mathrm{Beta}(0.3,0.3),$$

and finally

$$X_i \mid \rho \sim \mathrm{Bernoulli}(\rho).$$

This is a full generative story. First choose which prior regime is active. Then draw the coin bias $\rho$ from that regime. Then generate observations from that coin.

<p align="center">
  <img src="../notes/02_probability_reconstructed/assets/figure_2_20_beta_hyperprior.png" alt="Mixture of Beta priors" width="860">
</p>

The left and middle panels represent two qualitatively different prior beliefs. The mixture panel averages them according to the hyper-prior on $H$. So before any data are seen, the model already says: "I am not fully committed to one prior story."

It helps to imagine one sample path. Suppose the latent draw is

$$H=\mathrm{fair}.$$

Then the model might draw

$$\rho=0.47$$

from the fair-coin prior, and the observed tosses could be

$$1,0,1,1,0,\ldots$$

By contrast, if

$$H=\mathrm{extreme},$$

the model might draw

$$\rho=0.94,$$

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

$$\rho \sim \mathrm{Beta}(1,1).$$

Because Beta$(1,1)$ is uniform on $[0,1]$, this means

$$p_{\rho}(\rho)=1, \qquad 0 \le \rho \le 1.$$

It is tempting to call this "uninformative." The problem is that flatness depends on the coordinate system.

Rewrite the same Bernoulli model in the natural parameter

$$\eta=\log\left(\frac{\rho}{1-\rho}\right).$$

From the earlier derivation,

$$\rho=\frac{e^{\eta}}{1+e^{\eta}}.$$

Differentiate:

$$\frac{d\rho}{d\eta}=\frac{e^{\eta}}{(1+e^{\eta})^2}=\rho(1-\rho).$$

Now transform the prior from the $\rho$ scale to the $\eta$ scale:

$$p_{\eta}(\eta)=p_{\rho}(\rho(\eta))\left|\frac{d\rho}{d\eta}\right|.$$

Since $p_{\rho}(\rho)=1$ on $[0,1]$, this becomes

$$p_{\eta}(\eta)=\frac{e^{\eta}}{(1+e^{\eta})^2}.$$

That density is not constant in $\eta$. It is largest near $\eta=0$ and decays in both tails. So a prior that is flat in probability space is not flat in log-odds space.

This is the real lesson. The phrase "uninformative prior" is incomplete unless you also specify the coordinate system. Uniform in $\rho$ means equal prior mass for equal-width intervals of probability. It does not mean equal prior mass for equal-width intervals of log-odds.

### Bayesian Model Selection

Suppose we are comparing whole models, not just parameters inside one model. Then the key quantity is the model evidence, also called the marginal likelihood:

$$p(D \mid M)=\int p(D \mid \theta,M)p(\theta \mid M)\,d\theta.$$

Taking logarithms gives

$$\log p(D \mid M)=\log \int p(D \mid \theta,M)p(\theta \mid M)\,d\theta.$$

Read this formula carefully. For a fixed model $M$:

- $\theta$ ranges over the parameter space of that model;
- $p(D \mid \theta,M)$ measures fit at one parameter value;
- $p(\theta \mid M)$ weights parameter values by the prior;
- the integral averages fit over the whole parameter space.

That averaging is the key difference from maximum likelihood. Maximum likelihood asks only for the single best parameter value. Model evidence asks how well the model performs on average under its prior.

This is why evidence automatically penalizes excessive flexibility. A very flexible model may achieve an excellent fit at a few special parameter values, but if most parameter settings fit the data poorly, the average can still be small. So evidence rewards models that place substantial prior mass on parameter values that fit the data reasonably well.

A simple verbal contrast is useful.

- Model A has one very sharp peak and poor fit almost everywhere else.
- Model B has no spectacular peak, but a broad region of decent fit.

Maximum likelihood prefers whichever model has the higher peak. Evidence can prefer Model B because it averages over the whole landscape rather than looking only at the top point.

The BIC score is a large-sample approximation to the log evidence:

$$\mathrm{BIC}=\max_{\theta}\log p(D \mid \theta,M)-\frac{d}{2}\log m,$$

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

$$D_A=\{H,T,T\},$$

and a second batch is

$$D_B=\{T,H,H\}.$$

We will compare two models.

- Model $M_1$: one shared coin with parameter $\rho$.
- Model $M_2$: two different coins with parameters $\rho_A$ and $\rho_B$.

If there is only one coin, all six flips share the same head probability $\rho$. Across both batches there are three heads out of six observations, so

$$\hat{\rho}=\frac{3}{6}=0.5.$$

If there are two different coins, the first batch gets parameter $\rho_A$ and the second gets parameter $\rho_B$. Their MLEs are the within-batch head frequencies:

$$\hat{\rho}_A=\frac{1}{3},\qquad \hat{\rho}_B=\frac{2}{3}.$$

Now compute the maximized average log-likelihood under each model.

Under the one-coin model, the fitted probability of both heads and tails is $0.5$, so every flip contributes $\log 0.5$. Therefore

$$\text{one-coin average log-likelihood} = (3 \log 0.5 + 3 \log 0.5)/6 = \log 0.5 \approx -0.693.$$

Under the two-coin model, batch $A$ has one head and two tails, while batch $B$ has two heads and one tail. So the maximized average log-likelihood is

$$\text{two-coin average log-likelihood} = \bigl(2 \log(1/3)+4 \log(2/3)\bigr)/6 \approx -0.637.$$

So raw fit prefers the two-coin model. That is not surprising: extra parameters make it easier to fit the observed sample.

BIC now adds a complexity penalty. The one-coin model has

$$d=1,$$

while the two-coin model has

$$d=2.$$

With

$$m=6$$

observations, the penalized average scores are

$$\text{one-coin BIC average} = -0.693-(\log 6)/12 \approx -0.842,$$

$$\text{two-coin BIC average} = -0.637-(\log 6)/6 \approx -0.935.$$

So BIC prefers the one-coin model, because the improvement in fit is not large enough to justify the extra parameter.

That is the central model-selection lesson. The two-coin model fits the training data better, but not by enough. Once complexity is priced in, the simpler explanation wins. This is exactly the kind of situation where maximum likelihood alone can overstate the case for a more flexible model.

After penalization, the one-coin model wins. The extra flexibility of the two-coin model is not justified by only six flips.

Now increase the data while keeping the same qualitative split:

$$D_A=\{H,T,T,T,T\},\qquad D_B=\{T,H,H,H,H\}.$$

The one-coin MLE is still

$$\hat{\rho}=0.5,$$

while the two-coin MLEs become

$$\hat{\rho}_A=0.2,\qquad \hat{\rho}_B=0.8.$$

The one-coin penalized average score is now

$$\text{one-coin BIC average} \approx -0.808,$$

while the two-coin penalized average score is

$$\text{two-coin BIC average} \approx -0.731.$$

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

$$\alpha x + (1-\alpha)x'.$$

The number $\alpha \in [0,1]$ is a mixing weight, so $\alpha x + (1-\alpha)x'$ is called a convex combination of $x$ and $x'$. A function $f$ is convex if

$$f(\alpha x + (1-\alpha)x') \le \alpha f(x) + (1-\alpha)f(x')$$

for all $\alpha \in [0,1]$ and all domain points $x,x'$. In words: evaluate the function after averaging the inputs, and compare that with averaging the function values. Convexity says the first quantity is never larger.

Strict convexity makes the inequality strict for distinct points when $0<\alpha<1$:

$$f(\alpha x + (1-\alpha)x') < \alpha f(x) + (1-\alpha)f(x').$$

So a strictly convex function cannot contain a flat line segment.

Equivalent characterizations are:

$$f(x') \ge f(x) + \nabla f(x)\cdot(x'-x)$$

and, when second derivatives exist,

$$\nabla^2 f(x) \succeq 0.$$

These characterizations are compact, so it is worth unpacking them. The first-order statement says that the tangent line or tangent plane at $x$ lies below the graph everywhere else. The second-order statement says the Hessian has no negative curvature directions. Positive semidefinite means

$$v^T \nabla^2 f(x)\,v \ge 0 \qquad \text{for every vector } v,$$

so every directional second derivative is nonnegative.

Convex functions are useful because every local minimum is global, and a strictly convex function has a unique minimum. Positive semidefinite curvature allows flat directions, so multiple minimizers can still exist. Positive definite curvature removes those flat directions and forces uniqueness.

A full worked example is $f(x)=x^2$. For any $x$ and $x'$ and any $\alpha \in [0,1]$,

$$f(\alpha x + (1-\alpha)x') = (\alpha x + (1-\alpha)x')^2$$

expands to

$$\alpha x^2 + (1-\alpha)x'^2 - \alpha(1-\alpha)(x-x')^2.$$

Since the last term is nonpositive, we obtain

$$(\alpha x + (1-\alpha)x')^2 \le \alpha x^2 + (1-\alpha)x'^2.$$

That is the convexity inequality in explicit algebraic form. The term

$$-\alpha(1-\alpha)(x-x')^2$$

is the correction term that makes the left-hand side smaller than the weighted average on the right. Geometrically, it says the parabola lies below every secant line connecting two points on its graph.

Jensen's inequality is the probability version of convexity:

$$\mathbb{E}[f(X)] \ge f(\mathbb{E}[X])$$

for convex $f$.

It is the same idea with probability weights. If $X$ takes values $x_1,\dots,x_k$ with probabilities $p_1,\dots,p_k$, then

$$\mathbb{E}[X]=\sum_i p_i x_i,\qquad \mathbb{E}[f(X)]=\sum_i p_i f(x_i).$$

So Jensen compares the function of the average with the average of the function. A concrete example is $f(x)=x^2$ and a random variable that equals $0$ or $2$ with equal probability. Then

$$\mathbb{E}[X]=1,\qquad f(\mathbb{E}[X])=1,$$

while

$$\mathbb{E}[f(X)] = \frac{1}{2}f(0)+\frac{1}{2}f(2)=2.$$

So indeed $\mathbb{E}[f(X)] \ge f(\mathbb{E}[X])$.

### Example 2-23: Convexity and the Exponential Family

The negative log-likelihood of a canonical exponential-family model is convex in its natural parameters. The reason is explicit, but it helps to write the logic in full rather than jumping directly to the Hessian formula.

For the canonical form

$$p_{\theta}(x)=h(x)\exp\left(\theta^{\top}\phi(x)-A(\theta)\right)$$

the log-likelihood of i.i.d. data $x^{(1)},\dots,x^{(m)}$ is

$$\ell(\theta)=\sum_{i=1}^m \log h(x^{(i)}) + \theta^{\top} \sum_{i=1}^m \phi(x^{(i)}) - mA(\theta)$$

Therefore the negative log-likelihood is

$$-\ell(\theta)=mA(\theta)-\theta^{\top}\sum_{i=1}^m \phi(x^{(i)})-\sum_{i=1}^m \log h(x^{(i)})$$

The last term is constant in $\theta$, and the middle term is linear in $\theta$. So all curvature comes from the log-partition function $A(\theta)$.

Differentiate $A(\theta)$:

$$\frac{\partial A(\theta)}{\partial \theta_j} = \mathbb{E}_\theta[\phi_j(X)], \qquad \frac{\partial^2 A(\theta)}{\partial \theta_j \partial \theta_k} = \mathrm{Cov}_\theta(\phi_j(X), \phi_k(X)).$$

The first identity comes from differentiating

$$A(\theta)=\log \int h(x)\exp\left(\theta^{\top}\phi(x)\right)\,dx$$

which yields a ratio of two integrals:

$$\frac{\partial A(\theta)}{\partial \theta_j}
=
\frac{\int h(x)\phi_j(x)\exp\left(\theta^{\top}\phi(x)\right)\,dx}{\int h(x)\exp\left(\theta^{\top}\phi(x)\right)\,dx}.$$

That ratio is exactly the expectation of $\phi_j(X)$ under the model indexed by $\theta$. Differentiating once more gives the covariance formula, so in matrix form

$$\nabla^2 A(\theta)=\mathrm{Cov}_\theta(\phi(X)).$$

Now the key convexity fact becomes transparent. For every vector $v$,

$$v^T \nabla^2 A(\theta) v = v^T \mathrm{Cov}_\theta(\phi(X)) v = \mathrm{Var}_\theta(v^T\phi(X)) \ge 0.$$

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

$$-\log p(x).$$

Rare outcomes have larger surprise because $p(x)$ is small. Entropy averages that surprise over all possible outcomes, weighted by how often those outcomes actually occur:

$$H[X] = -\sum_x p(x)\log p(x).$$

If the logarithm is base $2$, entropy is measured in bits. If the natural logarithm is used, entropy is measured in nats. The choice of base changes only the unit, not the underlying concept.

A deterministic variable has entropy zero, because there is no uncertainty to average over. At the other extreme, a uniform distribution on a fixed finite support has the largest entropy, because it spreads probability as evenly as possible and therefore makes each observation comparatively hard to predict. Entropy is therefore not just "randomness" in an informal sense; it is the expected code length of the optimal lossless code and the expected information revealed by one observation.

A useful comparison is between a fair coin and a biased coin with probabilities $(0.9,0.1)$. The fair coin has entropy $1$ bit, while the biased coin has

$$H[X] = -0.9\log_2 0.9 - 0.1\log_2 0.1 \approx 0.47 \text{ bits}.$$

The biased coin is more predictable, so it carries less uncertainty and requires fewer average bits to encode. That is the operational content of entropy: predictable sources are cheaper to describe on average.

### Example 2-24: Entropy

Start with the simplest nontrivial case: a fair coin. The two outcomes are equally likely, so each carries one bit of surprise:

$$H[X] = -0.5\log_2 0.5 - 0.5\log_2 0.5 = 1 \text{ bit}.$$

This can be unpacked one step further. Because

$$\log_2 0.5 = -1,$$

each term is

$$-0.5(-1)=0.5,$$

and the two equal contributions add to

$$0.5+0.5=1.$$

So one fair coin flip carries one bit of uncertainty. In coding language, it takes one yes/no choice to specify the outcome.

Now compare that with a fair die:

$$H[X] = -6 \cdot \frac{1}{6}\log_2 \frac{1}{6} \approx 2.58 \text{ bits}.$$

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

$$p(X=1)=0.001,\qquad p(X=0)=0.999.$$

So the entropy is

$$H[X] = -0.999\log_2 0.999 - 0.001\log_2 0.001 \approx 0.011 \text{ bits}.$$

It helps to understand why this number is so small. The outcome $X=0$ is almost certain, so seeing another zero reveals almost no new information. The rare event $X=1$ is very surprising when it happens, but it happens so infrequently that its contribution to the average remains small.

So the average uncertainty per symbol is only about

$$0.011$$

bits, far below the one-bit cost of a naive fixed code. This does not mean any single day can literally be encoded in $0.011$ bits. It means that over long sequences, the average cost per day can approach that number when the code is designed well.

That is the real compression lesson. A source with highly unequal probabilities carries very little uncertainty per symbol, and entropy measures exactly how little.

### Kullback-Leibler Divergence

Entropy measured uncertainty inside one distribution. KL divergence measures mismatch between two distributions.

For discrete variables,

$$D(p \,\|\, q)=\sum_x p(x)\log\left(\frac{p(x)}{q(x)}\right).$$

Read the ingredients in order.

- $p$ is the reference distribution, often interpreted as the true or target distribution.
- $q$ is the approximating distribution.
- The ratio $p(x)/q(x)$ compares how the two distributions score the same outcome.
- The weighting by $p(x)$ means the average is taken over outcomes that actually matter under $p$.

So KL divergence asks: if the world behaves like $p$, how costly is it to use $q$ in its place?

The logarithmic ratio

$$\log\left(\frac{p(x)}{q(x)}\right)$$

is positive when $q(x)$ is too small relative to $p(x)$, and negative when $q(x)$ is too large. After averaging under $p$, the total discrepancy is always nonnegative:

$$D(p \,\|\, q)\ge 0,$$

with equality only when

$$p=q.$$

But KL divergence is not symmetric. In general,

$$D(p \,\|\, q)\ne D(q \,\|\, p).$$

There is also an essential support condition. If some outcome satisfies

$$p(x)>0 \qquad \text{and} \qquad q(x)=0,$$

then

$$D(p \,\|\, q)=\infty.$$

That is because $q$ is declaring an actually possible event to be impossible.

One subtle point is easy to miss. The individual summands

$$p(x)\log\left(\frac{p(x)}{q(x)}\right)$$

need not all be positive. KL divergence is not nonnegative term by term. It is nonnegative only after the weighted average is taken.

A two-state example makes this visible. Let

$$p=(0.8,0.2), \qquad q=(0.5,0.5).$$

Then

$$D(p \,\|\, q)=0.8\log\left(\frac{0.8}{0.5}\right)+0.2\log\left(\frac{0.2}{0.5}\right).$$

Compute the two contributions separately:

$$0.8\log\left(\frac{0.8}{0.5}\right)=0.8\log(1.6)\approx 0.376,$$

$$0.2\log\left(\frac{0.2}{0.5}\right)=0.2\log(0.4)\approx -0.183.$$

Adding them gives

$$D(p \,\|\, q)\approx 0.376-0.183=0.193.$$

Reverse the order and the answer changes:

$$D(q \,\|\, p)=0.5\log\left(\frac{0.5}{0.8}\right)+0.5\log\left(\frac{0.5}{0.2}\right)\approx 0.223.$$

So KL divergence is a directed discrepancy, not an ordinary symmetric distance. The first argument tells you which outcomes are being treated as important, because the expectation is taken with respect to that distribution.

### Mutual Information

Mutual information asks a more specific question than "are these variables related?"

It asks: how much does observing one variable reduce uncertainty about the other?

Its structural definition is

$$I[X,Y]=D(p(x,y)\,\|\,p(x)p(y)).$$

The product

$$p(x)p(y)$$

is the joint distribution we would have if $X$ and $Y$ were independent. So mutual information is the KL penalty for pretending the true joint distribution factorizes when it actually does not.

If $X$ and $Y$ are independent, then

$$p(x,y)=p(x)p(y),$$

so

$$I[X,Y]=0.$$

Write the definition out in full:

$$I[X,Y]=\sum_{x,y} p(x,y)\log\left(\frac{p(x,y)}{p(x)p(y)}\right).$$

Now derive the entropy identity carefully. Split the logarithm:

$$I[X,Y]=\sum_{x,y} p(x,y)\log p(x,y)-\sum_{x,y} p(x,y)\log p(x)-\sum_{x,y} p(x,y)\log p(y).$$

For the second sum, use

$$\sum_y p(x,y)=p(x),$$

to obtain

$$\sum_{x,y} p(x,y)\log p(x)=\sum_x p(x)\log p(x).$$

Similarly,

$$\sum_{x,y} p(x,y)\log p(y)=\sum_y p(y)\log p(y).$$

Substituting back gives

$$I[X,Y]=-H[X,Y]+H[X]+H[Y].$$

So

$$I[X,Y]=H[X]+H[Y]-H[X,Y].$$

Because

$$H[X \mid Y]=H[X,Y]-H[Y],$$

we also obtain

$$I[X,Y]=H[X]-H[X \mid Y].$$

This second identity is often the most intuitive reading. It says mutual information is the amount of uncertainty in $X$ that disappears after $Y$ is revealed.

Two extreme cases fix the interpretation.

- If $X$ and $Y$ are independent, then observing $Y$ tells us nothing about $X$, so $I[X,Y]=0$.
- If $Y=X$ exactly, then observing $Y$ reveals $X$ completely, so $H[X \mid Y]=0$ and therefore $I[X,Y]=H[X]$.

So mutual information is not just a generic dependence score. It measures the reduction in uncertainty caused by observation.

### Conditional Entropy

Conditional entropy measures the uncertainty left in one variable after another variable is revealed.

It can be written as

$$H[X \mid Y]=H[X,Y]-H[Y],$$

or, more explicitly,

$$H[X \mid Y]=\sum_y p(y)H[X \mid Y=y].$$

The second form is the most useful for interpretation. It says:

1. For each possible value $y$, compute the entropy of the conditional distribution of $X$ given $Y=y$.
2. Average those entropies using the probabilities $p(y)$.

So conditional entropy is not "the uncertainty after one particular observed value." It is the average remaining uncertainty over all possible revealed values of $Y$.

That average matters. For one unusual value of $Y$, uncertainty about $X$ can even increase compared with the unconditional case. The theorem is only that uncertainty cannot increase on average:

$$H[X \mid Y]\le H[X].$$

Equivalently,

$$I[X,Y]=H[X]-H[X \mid Y]\ge 0.$$

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

$$p(R=\text{clear})=0.9, \qquad p(R=\text{rain})=0.1.$$

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

$$p(C=\text{walk}) = 0.86, \quad p(C=\text{bike}) = 0.09, \quad p(C=\text{drive}) = 0.05.$$

These marginals come from the law of total probability. For example,

$$p(C=\text{walk}) = p(C=\text{walk}\mid R=\text{clear})p(R=\text{clear}) + p(C=\text{walk}\mid R=\text{rain})p(R=\text{rain})$$

$$=0.9\cdot 0.9 + 0.5\cdot 0.1 = 0.81 + 0.05 = 0.86.$$

The other commute marginals are obtained the same way:

$$p(C=\text{bike}) = 0.1\cdot 0.9 + 0\cdot 0.1 = 0.09,$$

$$p(C=\text{drive}) = 0\cdot 0.9 + 0.5\cdot 0.1 = 0.05.$$

Now compute the unconditional entropy of the commute explicitly:

$$H[C] = -0.86\log_2 0.86 - 0.09\log_2 0.09 - 0.05\log_2 0.05 \approx 0.72 \text{ bits}.$$

So before observing the weather, the commute carries about $0.72$ bits of uncertainty.

Now compute the entropy after the weather is revealed.

$$H[C \mid R=\text{clear}] = -0.9\log_2 0.9 - 0.1\log_2 0.1 \approx 0.47,$$

because the zero-probability drive term contributes nothing.

$$H[C \mid R=\text{rain}] = -0.5\log_2 0.5 - 0.5\log_2 0.5 = 1.$$

Average these conditional entropies using the weather probabilities:

$$H[C \mid R] = 0.9 \cdot 0.47 + 0.1 \cdot 1 \approx 0.52.$$

The unconditional commute entropy is larger, so the difference between them is exactly the information weather provides:

$$I[C,R] = H[C]-H[C \mid R] \approx 0.72 - 0.52 = 0.20 \text{ bits}.$$

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

The classical probability distributions above are useful, but many real data sets do not fit those forms directly. A common technique is to define a new variable as an invertible transformation of a simpler base variable.

The modeling motive is the following. Simple base distributions, such as Gaussians, are mathematically convenient but often too rigid to fit real data directly. Change-of-variables methods let us start from a simple distribution we understand well and then warp it into a more realistic one. The price of that warping is the Jacobian correction.

For the course core, the main required idea is the Jacobian correction in scalar and multivariate change of variables. The copula and normalizing-flow subsections are explicit reach material: they show how the same principle scales into more modern modeling constructions.

### Scalar Change of Variables

If $X = f(Z)$ is invertible and $g = f^{-1}$, then

$$p_X(x) = p_Z(g(x)) \lvert g'(x) \rvert.$$

This formula is a density version of probability conservation. The transformed variable cannot create or destroy probability mass. It can only move that mass around and locally stretch or compress the axis.

There are two derivations worth knowing.

First derivation: the exact CDF argument for a monotone increasing map. If $f$ is increasing, then

$$F_X(x)=\mathbb{P}(X \le x)=\mathbb{P}(f(Z)\le x)=\mathbb{P}(Z \le g(x))=F_Z(g(x)).$$

Differentiate both sides with respect to $x$:

$$p_X(x)=\frac{d}{dx}F_Z(g(x))=p_Z(g(x))g'(x).$$

If $f$ is decreasing, the same logic introduces a minus sign, and taking absolute values combines the two cases into the single formula

$$p_X(x)=p_Z(g(x))|g'(x)|.$$

Second derivation: the local-interval intuition. A tiny interval around $x$ corresponds to a tiny interval around $z=g(x)$. If the transformation stretches widths by a factor of $2$, then the density height must drop by a factor of $2$ so that probability mass is preserved. That is why the derivative appears.

This formula requires invertibility on the region of interest. If the map has multiple inverse branches, the correct density is a sum over branches rather than a single Jacobian term. The absolute value is not optional either. If the inverse map decreases rather than increases, the raw derivative is negative, but a density must remain nonnegative, so the local scaling factor must be taken in magnitude.

So the mental model should be: move probability mass with the transformation, then compensate for local stretching or compression. That is the whole purpose of the derivative term.

A minimal worked example is $X=2Z$ with $Z$ uniform on $[0,1]$. Then $g(x)=x/2$ and $g'(x)=1/2$, so

$$p_X(x)=p_Z(x/2)\cdot \frac{1}{2}.$$

Now state the support condition explicitly. The argument $x/2$ must lie in the support of $Z$, namely $[0,1]$. So

$$0 \le x/2 \le 1 \qquad \Longleftrightarrow \qquad 0 \le x \le 2.$$

Since $p_Z(z)=1$ on $[0,1]$, we get

$$p_X(x)=\frac{1}{2}$$

on $[0,2]$ and zero elsewhere. Stretching the variable by a factor of $2$ cuts the density height by a factor of $2$. For example,

$$\mathbb{P}(0.4 \le X \le 1.0)=\int_{0.4}^{1.0}\frac{1}{2}\,dx=0.3,$$

which matches the equivalent $Z$-space calculation

$$\mathbb{P}(0.2 \le Z \le 0.5)=0.3.$$

One more tiny example explains why the absolute value is necessary. Let

$$X=1-Z$$

with the same base distribution

$$Z \sim \mathrm{Unif}[0,1].$$

Then

$$g(x)=1-x, \qquad g'(x)=-1.$$

So

$$p_X(x)=p_Z(1-x)\lvert -1 \rvert = p_Z(1-x).$$

Because $1-x \in [0,1]$ exactly when $x \in [0,1]$, the transformed density is still uniform on $[0,1]$. The derivative is negative, but the density does not become negative. That is exactly why the absolute value is required.

### Example: Lognormal Distribution

If $Z = \log X$ is Gaussian, then $X$ is lognormal. This example is useful because it shows exactly how exponentiating a symmetric variable produces an asymmetric one.

Start with

$$Z \sim \mathcal{N}(\mu,\sigma^2).$$

Define

$$X=e^Z.$$

Because the exponential is always positive, the support of $X$ is

$$x>0.$$

The inverse transformation is

$$z=\log x,$$

and its derivative is

$$\frac{dz}{dx}=\frac{1}{x}.$$

So the change-of-variables formula gives the full lognormal density

$$p_X(x)=\frac{1}{x \sqrt{2\pi\sigma^2}} \exp\left(-\frac{(\log x-\mu)^2}{2\sigma^2}\right), \qquad x>0.$$

The extra factor

$$\frac{1}{x}$$

is exactly the Jacobian term. Without it, the transformed density would no longer integrate to one.

The asymmetry is worth explaining carefully. Equal distances on the $Z$ scale correspond to multiplicative, not additive, changes on the $X$ scale:

- moving from $Z=0$ to $Z=1$ means moving from $X=1$ to $X=e$;
- moving from $Z=1$ to $Z=2$ means moving from $X=e$ to $X=e^2$.

So the right side of the $X$ axis gets stretched more and more strongly. That stretching is what creates the long right tail of the lognormal density.

A concrete probability statement helps fix the translation rule. If

$$Z \sim \mathcal{N}(0,1),$$

then

$$\mathbb{P}(1 \le X \le e)=\mathbb{P}(0 \le Z \le 1).$$

So lognormal probabilities are often easiest to reason about by taking logarithms and reducing the question back to an ordinary Gaussian calculation.

### Multivariate Change of Variables

In multiple dimensions,

$$p_X(x) = p_Z(g(x)) \lvert \det J_g(x) \rvert,$$

where $J_g$ is the Jacobian matrix of the inverse transformation:

$$J_g(x)=
\begin{bmatrix}
\frac{\partial g_1}{\partial x_1} & \cdots & \frac{\partial g_1}{\partial x_d}\\
\vdots & \ddots & \vdots\\
\frac{\partial g_d}{\partial x_1} & \cdots & \frac{\partial g_d}{\partial x_d}
\end{bmatrix}.
$$

The determinant plays the same role as $|g'(x)|$ in one dimension: it is the local volume scaling factor. If the transformation doubles area near one point, the density there must be cut in half to preserve total probability. If the determinant is zero somewhere, the map locally collapses volume and is not invertible there, so the simple formula breaks down.

An explicit two-dimensional example is

$$X_1=2Z_1, \qquad X_2=3Z_2.$$

The inverse map is

$$Z_1=\frac{X_1}{2},\qquad Z_2=\frac{X_2}{3},$$

so the inverse Jacobian matrix is

$$J_g(x)=
\begin{bmatrix}
1/2 & 0\\
0 & 1/3
\end{bmatrix}.
$$

Its determinant is

$$\det J_g(x)=\frac{1}{6}.$$

So every small area element is expanded by a factor of $6$ in data space, and the density must shrink by the same factor. For example, a unit square in latent space becomes a rectangle of area $6$ in data space. Probability mass is preserved, so density height must be divided by $6$.

The absolute value is still essential in multiple dimensions. A negative determinant means the map reverses orientation locally, not that probability becomes negative. Density only cares about the magnitude of the local volume change.

### Copula Models

Copulas separate marginal distributions from dependence structure. For two variables,

$$\mathbb{P}(X_1 \le x_1, X_2 \le x_2) = C(F_1(x_1), F_2(x_2)),$$

where $F_1$ and $F_2$ are the marginal CDFs. The key construction is to define

$$U_1=F_1(X_1),\qquad U_2=F_2(X_2).$$

When the marginals are continuous, each $U_i$ is uniformly distributed on $[0,1]$. This is the probability integral transform. So the copula is simply the joint CDF of these transformed uniform variables:

$$C(u_1,u_2)=\mathbb{P}(U_1 \le u_1, U_2 \le u_2).$$

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

That separation is the main reason copulas are useful. They let us answer two modeling questions separately instead of mixing them together: "what does each variable look like on its own?" and "how do the variables depend on one another?"

<p align="center">
  <img src="../notes/02_probability_reconstructed/assets/figure_2_copula_flow_pipeline.png" alt="Copula and flow transformation pipeline" width="860">
</p>

### Example 2-27: Copula Transforms

The chapter uses a KDD Cup data set to show the pipeline. The procedure is worth spelling out as four separate steps.

Step 1: estimate each marginal distribution separately. From the raw data, estimate $F_1$ for the first coordinate and $F_2$ for the second.

Step 2: remove the original units by mapping into percentile space:

$$U_1=F_1(X_1),\qquad U_2=F_2(X_2).$$

At this stage each coordinate is uniform on $[0,1]$. So an observation at the $80$th percentile becomes $0.8$ regardless of whether the original variable measured time, length, or counts.

Step 3: map the uniform variables into Gaussian marginals:

$$Y_1=\Phi^{-1}(U_1),\qquad Y_2=\Phi^{-1}(U_2).$$

Now the one-dimensional marginals are Gaussian by construction.

Step 4: fit a Gaussian dependence model to $(Y_1,Y_2)$. That dependence model is the Gaussian copula.

The resulting model can express complicated non-Gaussian marginals while keeping the dependence structure manageable.

The step-by-step reason this works is that CDF transforms preserve order. If an observation is at the $80$th percentile of its own marginal distribution, its transformed value is $0.8$ regardless of the original physical units. After both coordinates are mapped into percentile space, the dependence structure can be modeled in a unit-free way.

Make one observation explicit. Suppose a data point lands at the $80$th percentile of the first marginal and the $25$th percentile of the second. Then

$$U_1=0.8, \qquad U_2=0.25.$$

After the Gaussian transform,

$$Y_1=\Phi^{-1}(0.8)\approx 0.84, \qquad Y_2=\Phi^{-1}(0.25)\approx -0.67.$$

So the original units are gone, but the relative standing inside each marginal distribution is preserved.

So the copula trick is fundamentally a change-of-coordinates trick: strip away marginal units and shapes first, then model only the remaining dependence.

### Normalizing Flows

Normalizing flows start with a simple base variable

$$Z \sim p_Z,$$

often Gaussian, and then define the observed variable by an invertible map

$$X=f(Z).$$

The density of $X$ is computed by the change-of-variables formula. The practical idea is simple: sampling and density evaluation are easy in the base space, while the learned transformation bends that simple density into a more realistic one in data space.

The transformation is often built as a composition of simple steps:

$$f(Z) = f_T(f_{T-1}(\cdots f_1(Z)))$$

with

$$\log p_X(X) = \log p_Z(f^{-1}(X)) - \sum_t \log |\det J_{f_t}|.$$

There are two points to make explicit here.

First, the map is a composition:

$$f = f_T \circ \cdots \circ f_1.$$

So the inverse is

$$f^{-1}=f_1^{-1}\circ \cdots \circ f_T^{-1}.$$

Second, Jacobian determinants multiply under composition. Therefore the log-determinants add. That is the whole computational reason flows are practical: a complicated global transformation can be assembled from simple local pieces whose determinants are easy to evaluate.

A flow is therefore practical only when each layer is invertible and has a determinant that can be evaluated cheaply. If either condition fails, likelihood evaluation becomes intractable or ill-defined.

The modeling motivation is parallel to the copula idea but more flexible. Instead of choosing one fixed transformation by hand, a flow learns a sequence of simple invertible maps whose composition can bend a simple base density into a complicated observed density.

This is the long-term modeling idea behind flows. Start with a base density that is easy to sample from and evaluate, such as a Gaussian. Then learn an invertible map that bends that simple density into a complex one that matches the data. The density becomes complicated in data space, but it stays tractable because the transformation remains invertible and the Jacobian terms are computable.

A one-layer sanity check is the scaling flow

$$X = aZ + b$$

with $a \neq 0$. Then the inverse is $(X-b)/a$ and

$$\log p_X(X)=\log p_Z\left(\frac{X-b}{a}\right)-\log |a|.$$

That tiny example already contains the entire logic of a flow:

- invert the transformation to locate the corresponding latent point;
- evaluate the simple base density there;
- subtract the log-volume expansion.

Normalizing flows are just more elaborate versions of this same accounting rule, composed many times.

So a flow should be read as repeated change-of-variables bookkeeping, not as a fundamentally different probability law.

### Example 2-28: Copula-Like Normalizing Flow

One useful construction is to start with a Gaussian base distribution and parameterize one-dimensional monotone transforms for each feature. This is a flexible stand-in for explicit CDF modeling. The monotonicity constraint is not optional: without it, the map would stop being invertible and the simple change-of-variables formula would break.

At the beginner level, this means "bend each axis without folding it over itself." At the expert level, it means each scalar transform must remain strictly monotone so that the inverse exists and the Jacobian diagonal stays nonzero everywhere.

Why is this copula-like? Because each coordinate gets its own monotone warp, which is playing the same role that a marginal CDF transform would play in an explicit copula pipeline. The difference is that here the warp is learned rather than supplied analytically.

Why does folding break the model? Because once two different latent values are mapped to the same observed value, the inverse is no longer unique. Then the one-branch flow formula is invalid and one must sum over inverse branches, exactly as in the noninvertible scalar case.

So the design rule is strict: flexibility is allowed, but only in ways that preserve a single well-defined inverse.

### Example 2-29: Conditional Affine Normalizing Flows

A particularly convenient flow layer is conditional affine:

$$Z_1' = Z_1, \qquad Z_2' = \alpha_1(Z_1)Z_2 + \beta_1(Z_1).$$

The structure of this layer should be read literally. The first coordinate is copied unchanged, while the second coordinate is shifted and rescaled using functions of the first coordinate. This makes the layer expressive but still easy to invert.

Why keep one coordinate unchanged? Because that design makes the Jacobian triangular. A triangular Jacobian has a determinant equal to the product of its diagonal entries, which is why this layer stays computationally cheap even though it couples the coordinates.

Indeed, if $\alpha_1(Z_1)\neq 0$, then the inverse is

$$Z_1 = Z_1', \qquad Z_2 = \frac{Z_2' - \beta_1(Z_1')}{\alpha_1(Z_1')}.$$

So invertibility requires the scale factor never to cross zero.

Because the Jacobian is triangular, the determinant is easy to compute: for the first layer it is simply $\alpha_1(Z_1)$, so the log-determinant is $\log |\alpha_1(Z_1)|$. A second layer can then swap roles and transform the other coordinate:

$$Z_1'' = \alpha_2(Z_2')Z_1' + \beta_2(Z_2'), \qquad Z_2'' = Z_2'.$$

<p align="center">
  <img src="../notes/02_probability_reconstructed/assets/figure_2_6_affine_flow_panels.png" alt="Normalizing flow deformation panels" width="860">
</p>

The deformation panels show what the algebra means geometrically. A rectangular grid in latent space is progressively bent and stretched into a curved mesh in data space. The main idea is that a sequence of simple invertible layers can produce a complex density while keeping likelihood evaluation tractable. The structural limit is equally important: each layer must preserve invertibility, and in practice the scale functions are parameterized so they never cross zero.

A full worked determinant calculation makes the affine layer concrete. For

$$Z_1' = Z_1, \qquad Z_2' = \alpha_1(Z_1)Z_2 + \beta_1(Z_1),$$

the forward Jacobian matrix is

$$J_{11}=1,\qquad J_{12}=0,\qquad J_{21}=\frac{\partial Z_2'}{\partial Z_1},\qquad J_{22}=\alpha_1(Z_1),$$

so

$$\det J = \alpha_1(Z_1).$$

The lower-left derivative can be complicated:

$$\frac{\partial Z_2'}{\partial Z_1}=\alpha_1'(Z_1)Z_2+\beta_1'(Z_1),$$

but the determinant ignores it because the matrix is triangular. That is the key design principle: choose transformations that are expressive enough to bend the density, yet structured enough that the determinant remains cheap to evaluate exactly.

A tiny numerical snapshot makes the layer concrete. Suppose at one particular input we have

$$Z_1=1, \qquad Z_2=3, \qquad \alpha_1(Z_1)=2, \qquad \beta_1(Z_1)=-1.$$

Then

$$Z_1'=1, \qquad Z_2'=2 \cdot 3 - 1 = 5.$$

To invert, use the same $Z_1'=1$ and solve

$$Z_2=\frac{Z_2'-\beta_1(Z_1')}{\alpha_1(Z_1')}=\frac{5-(-1)}{2}=3.$$

The determinant at that point is simply

$$\det J = 2,$$

so local area is doubled there and the log-density must decrease by

$$\log 2.$$

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

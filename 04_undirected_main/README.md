# Chapter 4: Undirected Models

## Chapter overview

Directed graphical models describe a joint distribution by expanding it into conditional probabilities along a directed acyclic graph. That is one very powerful way to organize dependence, but it is not the only one. In many problems, especially those centered on compatibility, symmetry, local constraints, or spatial smoothness, a directed causal story is not the most natural description. What we need instead is a way to say that certain collections of variable values fit together well, or poorly, without committing to one variable being generated first and another second. That is the role of undirected graphical models.

This chapter introduces the undirected viewpoint through two closely related representations: Markov random fields and factor graphs. Both are built around the same basic mathematical idea. We begin with a nonnegative function on the full state space and write it as a product of smaller local factors. After normalizing, that product becomes a probability distribution. The graph records which variables appear together in those local factors.

This chapter matters for three reasons. First, it broadens the student's understanding of what a graphical model is. A graph can encode probabilistic structure even when there is no conditional-probability semantics attached to individual edges. Second, undirected models are especially natural for constraint systems, spatial models, pairwise preference models, and continuous Gaussian models. Third, the chapter prepares later work on inference and learning, where the partition function and local marginals become central computational objects.

The chapter proceeds in seven stages. Section 4.1 introduces factorization, partition functions, Markov random fields, and factor graphs. Section 4.2 develops several important model families, including constraint networks, Boltzmann and Ising models, and probabilistic logic. Section 4.3 explains conditioning and conditional independence in undirected graphs, including the Hammersley-Clifford theorem. Section 4.4 studies how different graphical-model representations can be converted into one another. Section 4.5 connects undirected models to the overcomplete exponential family. Section 4.6 shows how Gaussian distributions fit naturally into an undirected graphical framework. Section 4.7 turns to parameter estimation and explains why learning is harder here than in Bayesian networks.

---

## 4.1 Factorization and graphs

### Why this section exists

Before we can reason with undirected models, we need a new semantic foundation. In a Bayesian network, each local factor is a conditional probability, so the graph comes with a built-in meaning: arrows indicate conditioning structure. In an undirected model, that story disappears. There are still local factors, but they are not required to be normalized conditional distributions, and there are no arrows telling us which variable depends on which. So the first task is to answer a basic question: if the factors are not conditional probabilities, what exactly are they, and how does the graph represent them?

This section exists to fill that gap. It introduces the core object of the chapter: a nonnegative function that factorizes over small subsets of variables. Once that idea is clear, Markov random fields and factor graphs become two ways of drawing the same underlying factorization.

### The object being introduced

Let

$$
X = (X_1, X_2, \dots, X_n)
$$

be a collection of random variables. For now, think mainly of the discrete case, although the same ideas extend beyond it. What is fixed is the variable collection and the set of local factor scopes. What varies are the values taken by the factors and therefore the resulting probability distribution.

The key object is not initially a probability distribution but a nonnegative function

$$
f(X).
$$

We assume this function can be written as a product of smaller terms,

$$
f(X) = \prod_{\alpha \in I} f_\alpha(X_\alpha),
$$

where each index set $\alpha \subseteq [n] = \{1,\dots,n\}$ specifies a subset of variables, and $X_\alpha$ denotes the variables whose indices lie in $\alpha$. The subset of variables that a factor actually depends on is called its **scope**.

This factorization answers the modeling question,

> Can the global compatibility of a full configuration be described by multiplying together many local compatibility terms?

That is the right question for undirected models. Each factor scores or weights local patterns. If a full configuration agrees well with many local preferences, its product value is large. If it violates a hard constraint, some factor may be zero, making the entire configuration impossible.

### Formal definition

An **undirected graphical model** begins with a factorization

$$
p(X) = \frac{1}{Z} f(X), \qquad f(X) = \prod_{\alpha \in I} f_\alpha(X_\alpha),
$$

where each factor satisfies

$$
f_\alpha(X_\alpha) \ge 0,
$$

and the normalization constant

$$
Z = \sum_x f(x)
$$

in the discrete case is called the **partition function**.

The factorization yields two common graph representations.

A **Markov random field** (MRF) uses one node per variable and places an undirected edge between $i$ and $j$ whenever $X_i$ and $X_j$ appear together in the scope of at least one factor. Equivalently, if there exists some $\alpha$ with $\{i,j\} \subseteq \alpha$, then $(i,j)$ is an edge.

A **factor graph** is a bipartite undirected graph with variable nodes $i$ and factor nodes $\alpha$. Variable node $i$ is connected to factor node $\alpha$ if and only if $i \in \alpha$, meaning that $X_i$ is an argument of factor $f_\alpha$.

### Interpretation paragraph

The probability distribution is not built by multiplying probabilities, as in a Bayesian network. It is built by multiplying **local nonnegative weights** and then normalizing the result. That difference matters. A factor can be a true probability table, but it does not have to be. It may instead encode a soft preference, a penalty, a constraint, a similarity score, or any other nonnegative compatibility function.

The partition function $Z$ is what turns the raw product into a legitimate probability distribution. Without $Z$, the product is only an unnormalized score. With $Z$, the scores are rescaled so that the probabilities sum to one.

The first thing to notice is that the graph records **which variables interact locally**, not how the model was generated. The second thing to notice is that a Markov graph hides some information: it tells us which variables appear together somewhere, but not exactly how the factorization is broken into factors. A factor graph preserves that finer structure.

### Boundary conditions, assumptions, and failure modes

Several points are easy to miss.

First, the factors need only be **nonnegative**, not normalized. If some factors are zero on some configurations, then those configurations are impossible under the model.

Second, the partition function must be finite. In the discrete finite-state case this is automatic as long as the factors are finite. In continuous or more general settings, one must check integrability explicitly.

Third, the Markov graph is a coarser summary than the factor graph. Different factor graphs can induce the same Markov graph. So if the precise decomposition of a clique into smaller factors matters, the factor graph is the more informative representation.

Fourth, a large clique can still make the model expensive. Undirected factorization helps only when the scopes stay small enough to be handled computationally.

Finally, undirected edges do not mean causation, temporal order, or directional influence. They mean only that the model includes local interactions that involve the connected variables.

### Fully worked example: why factor graphs can say more than Markov graphs

Suppose we have variables $A,B,C,D,E,F$. Consider two different factorizations.

In the first,

$$
f(x) = f_{AB}(A,B)\,f_{AE}(A,E)\,f_{BE}(B,E)\,f_{BCD}(B,C,D)\,f_{DEF}(D,E,F).
$$

In the second, replace the three pairwise factors involving $A,B,E$ by one three-variable factor,

$$
f(x) = f_{ABE}(A,B,E)\,f_{BCD}(B,C,D)\,f_{DEF}(D,E,F).
$$

Now ask what the Markov graph sees. In either factorization, variables $A,B,E$ all appear together pairwise inside some factor scope, so the Markov graph draws the triangle among $A,B,E$. The rest of the graph is the same as well. Therefore both factorizations lead to the same Markov random field.

But the factor graph distinguishes them immediately.

- In the first factorization, the relationship among $A,B,E$ is assembled from three smaller pairwise pieces.
- In the second, it is expressed by one joint three-variable factor.

Why does that matter? Because a general factor $f_{ABE}$ can represent interactions that cannot be decomposed into a product of pairwise terms. The first factorization can always be folded into the second by defining

$$
f_{ABE}(A,B,E) = f_{AB}(A,B)f_{AE}(A,E)f_{BE}(B,E),
$$

but the reverse is not true in general. A truly three-way interaction may not split into pairwise parts.

So the reasoning proceeds in a definite order.

1. Check which variables co-occur in some factor. That determines the Markov graph edges.
2. Notice that both candidate factorizations create exactly the same pairwise co-occurrences.
3. Conclude that the Markov graph cannot distinguish them.
4. Inspect the factor scopes themselves. Only the factor graph preserves that information.
5. Conclude that factor graphs are strictly more expressive as drawings of a given factorization, even when the induced MRF is the same.

### Misconception or counterexample block

**Do not confuse a factor with a probability.**  
A factor may be larger than one, smaller than one, or fail to sum to one over anything. Only the normalized product gives a probability distribution.

**Do not confuse the Markov graph with the factor graph.**  
A Markov graph says which variables are locally tied together. A factor graph says exactly which factors exist and which variables each factor touches.

**Do not assume that an edge means “direct dependence” in the same sense as in a Bayesian network.**  
In undirected models, the local semantics are compatibility-based, not conditional-probability-based.

### Connection to later material

Everything that follows depends on this factorization viewpoint. Constraint networks, Boltzmann machines, Ising models, Gaussian models, and pseudo-likelihood learning are all specific ways of choosing the factors. The partition function introduced here will also become the central computational bottleneck in inference and learning.

### Retain / do not confuse

Retain these points:

- An undirected model is built from nonnegative local factors multiplied together and then normalized.
- The partition function $Z$ converts unnormalized scores into probabilities.
- Factor scopes tell us which variables interact locally.
- Factor graphs preserve the actual decomposition into factors; Markov graphs do not.

Do not confuse:

- local factor values with probabilities,
- Markov graphs with factor graphs,
- undirected interaction with causal direction.

---

## 4.2 Examples of undirected graphs

### Why this section exists

A definition becomes useful only when the student can see the kinds of systems it is meant to describe. Undirected models are broad, and without examples the framework can feel too abstract. This section exists to answer the practical question: what kinds of problems naturally lead to undirected factorizations rather than directed ones?

The answer is that undirected models appear whenever local compatibility matters more than directional generation. Constraint satisfaction, pairwise agreement, spatial smoothness, and weighted logical rules are all examples.

---

### Constraint networks

#### Why this subsection exists

The simplest undirected models are deterministic ones. They do not assign nuanced probabilities at first; they simply declare some configurations allowed and others forbidden. Constraint networks are important because they show that the factor-product form is already useful even before we bring in smooth probabilistic preferences.

#### The object being introduced

A constraint network uses factors that take values in $\{0,1\}$. A factor equals zero when a local constraint is violated and one when it is satisfied. The global product therefore equals one exactly when all constraints are satisfied and zero otherwise.

What is fixed is the set of variables and the local constraints. What varies is the candidate configuration of all variables. The model answers the question,

> Does this global assignment satisfy every local rule simultaneously?

#### Formal definition

If $E$ is a collection of constrained pairs, define for each $(i,j) \in E$ a factor

$$
f_{ij}(X_i,X_j) =
\begin{cases}
0 & \text{if the local constraint is violated},\\
1 & \text{otherwise.}
\end{cases}
$$

Then

$$
f(X) = \prod_{(i,j)\in E} f_{ij}(X_i,X_j)
$$

returns

$$
f(X)=1 \text{ if all constraints are satisfied, and } 0 \text{ otherwise.}
$$

If we normalize this function, $p(X) \propto f(X)$, the resulting probability distribution is uniform over all satisfying assignments.

#### Interpretation paragraph

This factorization is not interesting because of the probabilities alone. Its value is that it converts a global feasibility question into a product of local tests. A single violated constraint sets one factor to zero and therefore annihilates the whole configuration.

#### Fully worked example: map coloring

Consider the map-coloring problem with regions $X_0,\dots,X_6$, each taking values in the color set

$$
\mathcal C = \{\text{red},\text{green},\text{blue}\}.
$$

If two regions share a border, they cannot receive the same color. For each adjacent pair $(i,j)$, define

$$
f_{ij}(X_i,X_j) =
\begin{cases}
0 & \text{if } X_i = X_j,\\
1 & \text{if } X_i \ne X_j.
\end{cases}
$$

Now evaluate two assignments.

Take first

$$
X = [r,g,b,r,g,r,b].
$$

To decide whether this is valid, we check each neighboring pair. At every edge, the two colors differ. Therefore every factor equals one, so

$$
f(X)=1.
$$

This assignment satisfies all constraints.

Now take

$$
X = [r,g,b,r,g,b,r].
$$

Suppose regions 2 and 5 are neighbors. Then $X_2=b$ and $X_5=b$, so the edge factor for that pair is

$$
f_{25}(X_2=b,X_5=b)=0.
$$

At that moment the whole product becomes zero, regardless of every other factor. Therefore

$$
f(X)=0.
$$

This assignment is invalid.

The general lesson is the same in every constraint network: the global decision is made by local checks, and the first violated local check is enough to rule out the full assignment.

#### Misconception block

**Do not think of $f(X)=1$ as “high probability” in a graded sense.**  
In a pure constraint network, all satisfying assignments receive the same unnormalized weight. The model distinguishes only allowed from forbidden.

#### Connection to later material

Constraint factors are the limiting case of softer probabilistic factors. Later models will assign graded preferences instead of only zeros and ones, but the graphical logic is the same.

---

### Independent sets and weighted preferences

#### Why this subsection exists

The previous example showed how to represent feasibility. A closely related idea is to combine hard constraints with a soft preference over feasible solutions. That move is important because many optimization problems ask not merely for any satisfying assignment, but for the best one according to some score.

#### The object being introduced

In the independent-set problem, each node of a graph gets a binary indicator variable. The hard constraint is that neighboring nodes cannot both be selected. The soft preference is that selecting more nodes should be rewarded.

#### Formal definition

Let $X_i \in \{0,1\}$ indicate whether vertex $i$ belongs to the set. For each edge $(i,j)$, define

$$
f_{ij}(X_i,X_j) = 1 - 1[X_i=1 \ \& \ X_j=1].
$$

So $f_{ij}=0$ exactly when adjacent vertices are both chosen.

To prefer larger independent sets, include unary factors

$$
f_i(X_i) = a^{1[X_i=1]}, \qquad a>1.
$$

Then

$$
f(X)=\left(\prod_{(i,j)\in E} f_{ij}(X_i,X_j)\right)\left(\prod_i f_i(X_i)\right).
$$

#### Interpretation paragraph

The pairwise factors enforce feasibility. The unary factors reward choosing vertices. So among feasible independent sets, those with more selected nodes receive larger weight. Maximizing $f(X)$ therefore corresponds to finding a maximum independent set.

#### Fully worked example

Suppose a graph has three vertices in a line: 1-2-3. Then the feasible independent sets are

$$
\varnothing, \{1\}, \{2\}, \{3\}, \{1,3\}.
$$

Set $a=2$. Then:

- For $X=(0,0,0)$, all pairwise constraints are satisfied and the unary contribution is $2^0=1$.
- For $X=(1,0,1)$, all pairwise constraints are satisfied and the unary contribution is $2^2=4$.
- For $X=(1,1,0)$, the edge $(1,2)$ violates the constraint, so the product is zero regardless of the unary terms.

Hence the maximum is attained at $(1,0,1)$, the largest independent set.

The important pattern is that a hard combinatorial structure can be represented as an undirected model, and then modified smoothly by adding preference factors.

---

### Propositional logic and satisfiability

#### Why this subsection exists

Many constraint systems are easier to describe in logical language than directly as tables. This subsection exists to connect undirected models to logical formulas, especially conjunctive normal form, which is one of the standard languages of satisfiability and discrete reasoning.

#### The object being introduced

A logical clause can be treated as a local factor. The variables of the clause are Boolean atoms, and the factor equals zero exactly when the clause evaluates to false. A conjunction of clauses becomes a product of factors.

#### Formal definition

If a clause $c_\alpha(x_\alpha)$ depends on a subset of Boolean variables $X_\alpha$, define

$$
f_\alpha(X_\alpha)=
\begin{cases}
1 & \text{if the clause is true},\\
0 & \text{if the clause is false}.
\end{cases}
$$

Then a CNF formula,

$$
\bigwedge_\alpha c_\alpha(X_\alpha),
$$

corresponds to the factor product

$$
f(X)=\prod_\alpha f_\alpha(X_\alpha).
$$

#### Interpretation paragraph

This is the same idea as the earlier constraint networks, but now the local constraints are written as logical statements rather than directly as table entries. The graphical model viewpoint does not replace logic; it provides a probabilistic and factorized way to manipulate it.

#### Worked example: coloring as logic

For map coloring, introduce atoms such as $R_0,G_0,B_0$, where $R_0$ means “region 0 is red,” and similarly for the other colors and regions.

A statement like

$$
R_0 \vee G_0 \vee B_0
$$

forces region 0 to take at least one color. A statement like

$$
R_0 \Rightarrow \neg R_1
$$

means that neighboring regions 0 and 1 cannot both be red. In CNF form this becomes

$$
\neg R_0 \vee \neg R_1.
$$

Each such clause becomes a factor that is one unless the clause is violated.

The logic-to-factor translation proceeds in a fixed order.

1. Identify the Boolean atoms.
2. Express each rule as a clause or conjunction of clauses.
3. For each clause, build a factor that is zero on the falsifying assignment and one otherwise.
4. Multiply those factors.
5. The global product is nonzero exactly on assignments satisfying all rules.

#### Connection to later material

This logical perspective will reappear when we move from deterministic satisfiability to weighted logical preferences in probabilistic logic and Markov logic networks.

---

### Boltzmann machines and Ising models

#### Why this subsection exists

Constraint networks show how undirected models represent hard local rules. But many real systems are not purely hard or purely deterministic. They exhibit graded preferences: neighboring pixels usually like to match, friends usually behave similarly, a spin system usually prefers alignment under certain conditions. Boltzmann and Ising models are canonical examples of positive pairwise undirected models that capture such preferences.

#### The object being introduced

These models describe strictly positive distributions over binary variables using pairwise and unary terms inside an exponential. The model does not say that one variable generates another. It says that certain configurations are more compatible than others.

What is fixed is the graph structure and the parameterization. What varies are the binary states and the numerical parameter values.

#### Formal definition: Boltzmann machine

For binary variables $X_i \in \{0,1\}$, a pairwise Boltzmann machine has the form

$$
p(X=x) \propto f(x) = \exp\left(\sum_{i<j} \theta_{ij}x_ix_j + \sum_i \theta_i x_i\right).
$$

Equivalently, this is a product of unary and pairwise factors,

$$
f(x)=\prod_{i<j} f_{ij}(x_i,x_j) \prod_i f_i(x_i),
$$

where

$$
f_{ij}(x_i,x_j)=\exp(\theta_{ij}x_ix_j), \qquad f_i(x_i)=\exp(\theta_i x_i).
$$

#### Interpretation paragraph

The unary term $\theta_i$ rewards or penalizes the state $X_i=1$. The pairwise term $\theta_{ij}$ matters only when both $x_i=x_j=1$, because in the $\{0,1\}$ encoding the product $x_ix_j$ is one only in that case. So the parameters describe relative preference among joint states, not marginal probabilities directly.

That last point is crucial. In a Bayesian network, a local conditional table has direct probability meaning. In a Boltzmann machine, $\theta_i$ and $\theta_{ij}$ are energy-like or score-like parameters. The actual marginal probability of $X_i=1$ depends on the whole model through normalization.

#### Fully worked example: a three-variable Boltzmann machine

Let $X_1,X_2,X_3 \in \{0,1\}$, and define

$$
f(x)=\exp(\theta_{12}x_1x_2 + \theta_{13}x_1x_3 + \theta_{23}x_2x_3 + \theta_1x_1 + \theta_2x_2 + \theta_3x_3).
$$

To understand what this means, inspect the eight configurations.

- If $x=(0,0,0)$, every term is zero, so $f(x)=1$.
- If $x=(1,0,0)$, only the unary term for $X_1$ contributes, so $f(x)=\exp(\theta_1)$.
- If $x=(1,1,0)$, the contribution is $\exp(\theta_1+\theta_2+\theta_{12})$.
- If $x=(1,1,1)$, every unary and every pairwise term appears, giving

$$
f(1,1,1)=\exp(\theta_1+\theta_2+\theta_3+\theta_{12}+\theta_{13}+\theta_{23}).
$$

Now interpret one parameter at a time.

If $\theta_1>0$, then any configuration with $X_1=1$ is multiplied by $\exp(\theta_1)>1$ relative to the same configuration with $X_1=0$, all else fixed. So $\theta_1$ pushes the model toward configurations where $X_1=1$.

If $\theta_{12}>0$, then configurations with $X_1=X_2=1$ receive a boost relative to those where at least one of them is zero. If $\theta_{12}<0$, that joint activation is penalized.

To find a genuine probability, we must compute

$$
p(x)=\frac{f(x)}{Z}, \qquad Z=\sum_{x_1,x_2,x_3} f(x_1,x_2,x_3).
$$

For example,

$$
\Pr[X_1=1] = \frac{\sum_{x_2,x_3} f(1,x_2,x_3)}{\sum_{x_1,x_2,x_3} f(x_1,x_2,x_3)}.
$$

This shows exactly why the parameters are not marginals: even $\Pr[X_1=1]$ depends on all unary and pairwise terms through the partition function.

The graph associated with the model includes an edge $(i,j)$ precisely when $\theta_{ij}\ne 0$. If $\theta_{ij}=0$, then $f_{ij}(x_i,x_j)=1$ is a constant factor and has no effect on the distribution.

#### Formal definition: Ising model

For spin variables $X_i \in \{-1,+1\}$, the Ising model uses

$$
p(X=x) \propto \exp\left(\sum_{i<j} \theta_{ij}x_ix_j + \sum_i \theta_i x_i\right).
$$

The algebra looks similar, but the interpretation of pairwise terms is cleaner than in the $\{0,1\}$ encoding.

- If $x_i=x_j$, then $x_ix_j=+1$.
- If $x_i\ne x_j$, then $x_ix_j=-1$.

So:

- $\theta_{ij}>0$ rewards agreement,
- $\theta_{ij}<0$ rewards disagreement.

The unary term $\theta_i x_i$ pushes spin $i$ toward $+1$ when $\theta_i>0$ and toward $-1$ when $\theta_i<0$.

#### Fully worked example: reading the Ising parameters

Consider two spins $X_1,X_2 \in \{-1,+1\}$ with no unary terms and one interaction $\theta_{12}$.
Then

$$
p(x_1,x_2) \propto \exp(\theta_{12}x_1x_2).
$$

There are four states.

- $(+1,+1)$ and $(-1,-1)$ have product $+1$, so each gets weight $\exp(\theta_{12})$.
- $(+1,-1)$ and $(-1,+1)$ have product $-1$, so each gets weight $\exp(-\theta_{12})$.

If $\theta_{12}>0$, the aligned states are preferred. If $\theta_{12}<0$, the anti-aligned states are preferred. The conclusion follows directly from the sign of $\theta_{12}$.

#### Spatial intuition: the 2D Ising grid

On a two-dimensional grid, each variable interacts only with its neighbors. This produces a good mental picture of how local pairwise preferences create global structure.

- When the pairwise couplings are near zero, neighboring pixels hardly influence one another, so a sampled image looks like noise.
- For moderate positive couplings, clusters begin to form because neighbors tend to align.
- For large positive couplings, large coherent regions appear because disagreement across edges becomes expensive.

The lesson is general: undirected local interactions can create long-range visible structure even when each factor involves only a very small scope.

#### Misconception block

**Do not read $\theta_i$ or $\theta_{ij}$ as direct probabilities.**  
They are parameters of an unnormalized score. Marginal probabilities emerge only after summing over other variables and dividing by $Z$.

**Do not confuse the $\{0,1\}$ and $\{-1,+1\}$ encodings.**  
They represent essentially the same family of positive pairwise binary distributions, but the interpretation of pairwise interaction is different in the two parameterizations.

#### Connection to later material

Boltzmann and Ising models are the most important concrete examples for later discussions of partition functions, pseudo-likelihood, and pairwise learning. They are also the bridge between machine learning language and statistical-physics language.

---

### Probabilistic logic

#### Why this subsection exists

Constraint satisfaction used logic to encode hard rules. The next step is to allow logic to express **soft rules**: statements that are usually true or whose violation should incur a penalty, but not statements that must hold absolutely. This is the core idea behind probabilistic logic and Markov logic networks.

#### The object being introduced

A logical clause now contributes a multiplicative weight rather than a hard zero-one constraint. Configurations that satisfy the clause receive a boost relative to those that do not.

#### Formal definition

If $c_\alpha(x_\alpha)\in\{0,1\}$ indicates whether a clause is true, and $\theta_\alpha$ is the weight of that clause, define

$$
f(x)=\prod_\alpha \exp\big(\theta_\alpha c_\alpha(x_\alpha)\big).
$$

Equivalently,

$$
f(x)=\exp\left(\sum_\alpha \theta_\alpha c_\alpha(x_\alpha)\right).
$$

If a clause is true, it contributes a factor of $\exp(\theta_\alpha)$; if false, it contributes $1$.

#### Interpretation paragraph

This is best understood as preference rather than certainty. A large positive weight says, “all else equal, worlds satisfying this rule are much more plausible.” A negative weight would say the opposite.

#### Fully worked example: friends and smokers

Suppose we use two weighted first-order rules:

1. $\text{Smokes}(x) \Rightarrow \text{Cancer}(x)$ with weight 1.5.
2. $\text{Friends}(x,y) \Rightarrow (\text{Smokes}(x) \Leftrightarrow \text{Smokes}(y))$ with weight 1.1.

Instantiate the domain to two people, Alice $(A)$ and Bob $(B)$. Then the model contains Boolean variables such as

$$
S_A, S_B, C_A, C_B, F_{AB}, F_{BA}, F_{AA}, F_{BB}.
$$

Now consider just one grounded factor from the first rule,

$$
S_A \Rightarrow C_A.
$$

This clause is false only when $S_A=1$ and $C_A=0$. So its factor is

$$
f(S_A,C_A)=
\begin{cases}
1 & \text{if } (S_A,C_A)=(1,0),\\
\exp(1.5) & \text{otherwise.}
\end{cases}
$$

Thus smoking without cancer is not impossible, but it is downweighted relative to the cases that satisfy the rule.

Now consider one grounded friendship rule for Alice and Bob. If $F_{AB}=0$, then the implication is automatically satisfied, so the factor always contributes $\exp(1.1)$. If $F_{AB}=1$, then the rule prefers $S_A=S_B$. In particular,

- if $F_{AB}=1$ and $S_A=S_B$, the factor contributes $\exp(1.1)$,
- if $F_{AB}=1$ and $S_A\ne S_B$, the factor contributes $1$.

So the model softly encourages friends to have matching smoking behavior.

The general lesson is that logic supplies the language of the model, while the undirected exponential weighting supplies the probabilistic semantics.

### Retain / do not confuse

Retain these patterns from the examples:

- hard constraints use zeros to rule out assignments;
- soft preferences use positive weights to prefer some assignments over others;
- Boltzmann and Ising models are positive pairwise models;
- weighted logical clauses are factors just like numeric compatibility tables.

Do not confuse:

- satisfying a clause with having probability one,
- parameter weights with marginal probabilities,
- pairwise locality with global simplicity.

---

## 4.3 Conditioning and conditional independence

### Why this section exists

A graphical model is useful only if the graph lets us reason about probabilities without expanding the full distribution every time. In Bayesian networks, that role was played by d-separation. In undirected models, the corresponding rule is simpler, but to understand why it is simpler, we first need to know what conditioning does to the factorization itself.

This section exists to make two ideas precise. First, observing a variable has a clean graph-theoretic effect in an undirected model: it removes that variable from the random system. Second, ordinary graph separation in the remaining graph exactly characterizes conditional independence. The section then culminates in the Hammersley-Clifford theorem, which explains when Markov properties and factorization are equivalent.

---

### Conditioning as a graph operation

#### The object being introduced

Conditioning means fixing the value of one or more variables and asking for the induced distribution over the remaining unknown variables. In an undirected model, because the factors are unnormalized already, this operation can be represented directly by substituting the observed value into each factor.

#### Formal statement

Suppose

$$
p(X)=\frac{1}{Z}\prod_\alpha f_\alpha(X_\alpha).
$$

If variable $X_i$ is observed to equal $x_i$, then every factor involving $X_i$ becomes a smaller factor obtained by plugging in that value. The conditional distribution over the unobserved variables is again proportional to a product of factors, now defined only on the unobserved variables.

Graphically, the conditioned variable is removed from the graph, together with all incident edges.

#### Interpretation paragraph

This is one of the main conceptual differences from Bayesian networks. In a directed model, conditioning on a child can create a new induced dependence among its parents, and the conditioned model may not be represented by simply deleting the child. In an undirected model, the factors never needed to be normalized in the first place, so after plugging in an observed value we still have a perfectly valid unnormalized product representation.

#### Fully worked example

Suppose

$$
p(A,B,C,D,E,F)=\frac{1}{Z}f_1(A,B,C)f_2(B,D,E,F).
$$

Now observe $B=b$. Substituting into the factors gives

$$
p(A,B=b,C,D,E,F)=\frac{1}{Z}f_1(A,b,C)f_2(b,D,E,F).
$$

Define the reduced factors

$$
f_1'(A,C)=f_1(A,b,C), \qquad f_2'(D,E,F)=f_2(b,D,E,F).
$$

Then the conditional distribution becomes

$$
p(A,C,D,E,F\mid B=b)=\frac{1}{Z'}f_1'(A,C)f_2'(D,E,F).
$$

The reasoning is straightforward.

1. Identify every factor that depends on the observed variable $B$.
2. Replace $B$ by the observed value $b$ inside each such factor.
3. Notice that the resulting factors no longer contain $B$ as an argument.
4. Therefore $B$ is no longer a random node in the remaining model.
5. The conditioned graph is obtained by deleting node $B$ and its incident edges.

In the resulting graph, $A$ and $C$ remain connected to one another through $f_1'$, and $D,E,F$ remain mutually tied through $f_2'$, but there is no path from $\{A,C\}$ to $\{D,E,F\}$. So these sets are conditionally independent given $B=b$.

#### Misconception block

**Do not say that conditioning “removes information.”**  
It removes a variable from the list of unknowns, but it also changes the distribution of the remaining variables by changing the factors.

**Do not assume the conditioned factors must still look like probabilities.**  
They are typically just smaller unnormalized factors.

---

### Conditional independence by graph separation

#### Why this subsection exists

Once we know that conditioning removes observed nodes, the independence rule becomes almost visually obvious. This subsection states that rule precisely.

#### Formal definition

Let $A,B,E$ be three sets of nodes in an undirected graph $G$. Then $X_A$ and $X_B$ are conditionally independent given $X_E$ if every path from any node in $A$ to any node in $B$ passes through at least one node in $E$.

Equivalently, after removing the nodes in $E$, there is no remaining path from $A$ to $B$.

#### Interpretation paragraph

Undirected conditional independence is literally graph separation. Unlike d-separation, there are no special collider rules, no active versus inactive path types, and no descendant caveats. If the observed set blocks all paths, then dependence cannot flow from one side to the other.

#### Fully worked example: Markov blanket intuition

Suppose a graph contains node $E$ with neighbors $B,D,F,H$. Then any path from $E$ to the rest of the graph must first pass through one of these neighbors. Therefore once $B,D,F,H$ are observed, $E$ is separated from all other variables. This set is called the **Markov blanket** of $E$.

The reasoning is:

1. Any path leaving $E$ must go through one of its immediate neighbors.
2. If all immediate neighbors are conditioned on, then every such path is blocked immediately.
3. Therefore $E$ is independent of every non-neighbor given its Markov blanket.

This statement is one of the most practically useful local independence facts in undirected models.

#### Fully worked example: separation of sets

Suppose an undirected graph has a left cluster $\{A,B,C,D,G\}$, a middle separator $\{E,F\}$, and a right cluster $\{H,J,K,L,M\}$, with all paths from left to right passing through either $E$ or $F$. Then conditioning on $E$ and $F$ makes the left and right clusters independent.

What is being checked is not pairwise adjacency but path existence. One must examine every route from one set to the other. If all such routes hit the separator, independence follows.

#### Connection to later material

This separation rule is the undirected counterpart of d-separation, and it underlies later local conditionals, pseudo-likelihood, and message-passing intuition.

---

### Hammersley-Clifford theorem

#### Why this subsection exists

So far the direction “factorization implies Markov properties” is clear: if the distribution is a product over local factors, then graph separation should imply conditional independence. But one naturally asks whether the converse holds. If a distribution satisfies the conditional independencies implied by a graph, must it factor over that graph? The answer is yes under a crucial positivity assumption. This is the content of Hammersley-Clifford.

#### Formal statement

**Theorem (Hammersley-Clifford).** If a distribution $p(X)$ is strictly positive,

$$
p(x)>0 \quad \text{for all } x,
$$

and is Markov with respect to an undirected graph $G$, then $p$ factorizes over the cliques of $G$:

$$
p(X) \propto \prod_{\alpha \in \mathcal C} f_\alpha(X_\alpha),
$$

where $\mathcal C$ is the set of cliques, typically taken to mean maximal cliques for a compact representation.

#### Interpretation paragraph

The theorem says that for strictly positive distributions, graph separation is not merely a consequence of factorization; it characterizes factorization. If the graph really captures all the Markov properties and no state has probability zero, then the distribution can be written as a product of clique factors.

#### Fully worked example

Consider a graph with maximal cliques

$$
\{A,B,C\},\ \{B,D,E,F\},\ \{D,F,G\},\ \{E,F,H\},\ \{H,J\},\ \{F,H,K\},\ \{K,L,M\}.
$$

If a strictly positive distribution is Markov with respect to this graph, then it must admit a factorization of the form

$$
p(X)=\frac{1}{Z}
 f_1(A,B,C)
 f_2(B,D,E,F)
 f_3(D,F,G)
 f_4(E,F,H)
 f_5(H,J)
 f_6(F,H,K)
 f_7(K,L,M).
$$

A smaller clique factor such as one on $\{B,D,F\}$ is not needed explicitly, because it can be absorbed into any maximal-clique factor that contains it, here $f_2$.

So the theorem tells us exactly what factor scopes are sufficient: clique scopes.

#### Boundary conditions and failure mode

The positivity assumption is not optional. If the distribution has zeros, the equivalence can fail.

#### Counterexample block: why positivity matters

The chapter gives a four-node cycle example in which a distribution is Markov with respect to the graph but cannot be written as a product of clique factors because some configurations have zero probability in a way that no positive edge-factorization can reproduce.

The logic of the contradiction is worth understanding.

1. Assume the distribution factors over edge cliques.
2. Look at all configurations that have positive probability.
3. From those configurations, deduce that every edge-factor table entry must itself be positive.
4. But then the product of those positive entries could never yield zero for any full configuration.
5. This contradicts the observed zero-probability states.

Therefore the supposed clique factorization cannot exist.

This is exactly what the strict-positivity hypothesis rules out.

### Retain / do not confuse

Retain these points:

- conditioning in an undirected model means substituting observed values into factors;
- graph separation after removing the observed nodes gives conditional independence;
- the Markov blanket of a node is its immediate neighbor set;
- under strict positivity, Markov properties imply clique factorization.

Do not confuse:

- local Markov properties with an actual displayed factorization,
- absence of paths after conditioning with absence of edges before conditioning,
- Hammersley-Clifford with a statement that holds for all distributions regardless of zeros.

---

## 4.4 Converting between different model types

### Why this section exists

Graphical-model ideas are shared across several representational languages, but software, derivations, and intuitions often live in only one of them. A practitioner may have a model written as a Bayesian network but need to run it in an undirected modeling library, or may want to convert a higher-order factor graph into a pairwise model because a later algorithm assumes pairwise interactions. This section exists to answer the practical question: what is preserved, and what is lost, when we move between different representation styles?

The main lesson is that many transformations are possible, but they often trade off compactness, positivity, interpretability, or visible conditional-independence structure.

---

### Converting undirected models to pairwise models

#### The object being introduced

A **pairwise** model is one in which every factor touches at most two variables. Pairwise models are convenient because their graphs are easy to draw and many algorithms are described for them specifically.

#### Method

If a factor $f_\alpha(X_\alpha)$ involves more than two variables, introduce a new auxiliary variable $Y_\alpha$ whose values encode full configurations of $X_\alpha$. Then replace the high-order factor by a unary factor on $Y_\alpha$, together with pairwise consistency constraints connecting $Y_\alpha$ to each original variable in its scope.

#### Fully worked example

Suppose we have a three-variable factor $f_{ABE}(A,B,E)$. Introduce a new variable $X$ whose domain consists of tuples $(a,b,e)$. Replace the original factor by a unary factor $f_{ABE}(X)$. Then add pairwise consistency factors such as

$$
f_{AX}(A=a, X=(a',b',e'))=
\begin{cases}
1 & \text{if } a=a',\\
0 & \text{otherwise.}
\end{cases}
$$

Similarly define $f_{BX}$ and $f_{EX}$.

Now every factor is unary or pairwise.

What is being checked at each consistency factor is simple: does the corresponding coordinate of the auxiliary variable agree with the original variable? If yes, the factor allows the configuration; if not, it forbids it.

#### What this buys and what it costs

This transformation always produces a pairwise model, but it introduces extra variables and often introduces zero-probability inconsistent states. So pairwise structure is gained at the cost of a larger state space and often loss of strict positivity.

---

### Converting to binary models

#### Why this subsection exists

Some logical or combinatorial frameworks insist on Boolean variables only. So it is useful to know that a discrete model with multi-valued variables can be converted into a binary one.

#### Method

For each variable-value pair, create a binary indicator variable

$$
X_{i;x}=1[X_i=x].
$$

Then represent the original factors in terms of these indicators, together with constraints enforcing that exactly one indicator is on for each original variable.

#### Interpretation paragraph

This is effectively a one-hot encoding of the state space. The conversion is conceptually straightforward, but the exact-one constraints are themselves not naturally pairwise. That is why making a model binary is easy, making it pairwise is easy, but making it simultaneously binary and pairwise is more delicate.

#### Failure mode to remember

The simple binary conversion produces nonpositive constraints. Those “one-hot” constraints are not easy to express directly as a strictly positive pairwise model. More elaborate constructions can approximate or reproduce the effect, but not as cheaply as the basic conversion.

---

### Directed to undirected: moralization

#### Why this subsection exists

Bayesian networks and undirected models often represent related independence structures. A common need is to convert a directed model into an undirected one. The mechanics are simple, but some visible independencies are lost in the process.

#### Formal procedure

Start from a Bayesian network with factors $p(X_i\mid X_{\mathrm{pa}(i)})$. For each node $i$, connect all variables in the set

$$
\{X_i\} \cup X_{\mathrm{pa}(i)}
$$

into a clique. Equivalently, take the original directed edges, drop the arrowheads, and add extra undirected edges between any two parents that share a child. This process is called **moralization**.

#### Fully worked example: burglar alarm

The burglary model has

$$
B \to A \leftarrow E, \qquad A \to W, \qquad A \to H.
$$

The factor graph representation is immediate: one factor for each conditional probability table,

$$
p(B),\ p(E),\ p(A\mid B,E),\ p(W\mid A),\ p(H\mid A).
$$

To form the Markov graph, we connect variables appearing in each factor. The factor $p(A\mid B,E)$ depends jointly on $A,B,E$, so the undirected graph must contain edges among all three. In particular, even though $B$ and $E$ had no directed edge between them, they become neighbors in the moralized graph.

#### What is lost

In the original Bayesian network, $B$ and $E$ are marginally independent when $A$ and its descendants are unobserved. In the moralized undirected graph, that independence is no longer visible from separation because $B$ and $E$ are connected by an edge.

The reason is that the independence in the directed model depends on the normalization of the conditional distribution $p(A\mid B,E)$. When $A$ is summed out, that factor contributes 1 regardless of $B,E$. The undirected graph, which sees only a generic factor over $A,B,E$, cannot know that such cancellation will occur.

So directed-to-undirected conversion is easy, but it may erase some conditional-independence information.

---

### Undirected to directed

#### Why this subsection exists

Converting the other way is harder. An undirected graph captures symmetric local compatibility, but a Bayesian network needs an ordering and conditional-probability semantics. This subsection explains the two main strategies.

#### Strategy 1: choose an order and build a Bayes net on the original variables

Pick an ordering of the variables. Then, for each variable $X_i$, choose as parents a sufficient subset of earlier variables that separates $X_i$ from all remaining earlier variables in the undirected graph.

#### Fully worked example: a 2x2 grid

Suppose the undirected graph is a 2x2 grid on variables $X_1,X_2,X_3,X_4$, ordered as $X_1,X_2,X_3,X_4$.

- $X_1$ is first, so it has no parents.
- $X_2$ is adjacent to $X_1$, so it is not independent of earlier variables; parent set $\{X_1\}$.
- $X_3$ is not independent of $X_1$ given only $X_2$, nor independent of $X_2$ given only $X_1$, so both earlier variables are needed; parent set $\{X_1,X_2\}$.
- $X_4$ is conditionally independent of $X_1$ given $X_2,X_3$, so parent set $\{X_2,X_3\}$.

This produces a valid directed model, but not all independencies visible in the undirected graph remain visible in the directed graph.

#### Strategy 2: introduce observed auxiliary variables for factors

For each factor $f_\alpha(X_\alpha)$, introduce a binary auxiliary variable $Z_\alpha$ with conditional distribution

$$
p(Z_\alpha=0\mid X_\alpha)=\frac{f_\alpha(X_\alpha)}{f^*_\alpha},
\qquad
f^*_\alpha = \max_{x_\alpha} f_\alpha(x_\alpha).
$$

Set the $X_i$ to have some simple prior, for example uniform. Then condition on all $Z_\alpha=0$. Up to an overall constant, the resulting directed model reproduces the original undirected factor product.

#### Interpretation paragraph

This second approach preserves the original undirected distribution more faithfully, but it does so by introducing variables whose only purpose is representational. The resulting arrows no longer carry any meaningful causal interpretation.

### Retain / do not confuse

Retain these points:

- high-order undirected factors can be converted to pairwise form with auxiliary variables;
- multi-valued variables can be converted to binary indicators;
- directed-to-undirected conversion moralizes the graph by connecting co-parents;
- undirected-to-directed conversion usually sacrifices either compactness or interpretability.

Do not confuse:

- representational equivalence with preservation of visible graph-separation properties,
- a conversion that preserves the distribution with one that preserves intuitive meaning.

---

## 4.5 The overcomplete exponential family

### Why this section exists

Earlier chapters introduced the exponential family as a unifying language for probability distributions. Many undirected models are not merely similar to exponential-family distributions; they are exponential-family models once their factors are written in the right coordinates. This section exists to make that connection explicit.

The connection matters because exponential-family theory gives immediate access to convexity, sufficient statistics, gradients of the log-partition function, and moment-matching conditions for learning.

### The object being introduced

We consider discrete undirected models whose factors are table-based. Every table entry can be turned into an indicator feature for one particular local configuration. The log of the factor product then becomes a linear function of those indicators. This is the **overcomplete exponential-family representation**.

What is fixed is the set of local configurations that define features. What varies are the parameter values attached to those features.

### Formal definition

Suppose

$$
p(X) \propto \prod_\alpha f_\alpha(X_\alpha).
$$

For each factor scope $\alpha$ and each local configuration $x'_{\alpha}$, define the feature

$$
\phi_{x'_{\alpha}}(X_\alpha)=1[X_\alpha=x'_{\alpha}].
$$

Then write

$$
f_\alpha(X_\alpha)=\exp\left(\sum_{x'_{\alpha}} \theta_{x'_{\alpha}} 1[X_\alpha=x'_{\alpha}]\right).
$$

Multiplying factors and collecting exponents gives

$$
p(X) \propto \exp\big(\theta \cdot \phi(X)\big).
$$

This is canonical exponential-family form.

### Interpretation paragraph

Each feature asks a very specific yes-or-no question about the configuration, such as “Are $X_1=2$ and $X_3=0$ simultaneously true?” The model assigns a parameter to every such local event. Because exactly one configuration occurs within each factor scope at a time, the factor value is recovered by selecting the corresponding parameter and exponentiating it.

### Fully worked example

Suppose the model is

$$
f(X)=f_{12}(X_1,X_2)f_{13}(X_1,X_3)f_{23}(X_2,X_3),
$$

with each variable taking values in $\{0,1,2\}$. Focus on just one factor, say $f_{12}$. For each pair $(a,b)\in\{0,1,2\}^2$, define the feature

$$
\phi_{12;ab}(X)=1[(X_1,X_2)=(a,b)].
$$

Then

$$
f_{12}(X_1,X_2)=\exp\left(\sum_{a,b} \theta_{12;ab}\, \phi_{12;ab}(X)\right).
$$

Now do the same for $f_{13}$ and $f_{23}$. The log-score becomes

$$
\log f(X)= \sum_{a,b}\theta_{12;ab}\phi_{12;ab}(X)
+ \sum_{a,c}\theta_{13;ac}\phi_{13;ac}(X)
+ \sum_{b,c}\theta_{23;bc}\phi_{23;bc}(X).
$$

This is linear in the feature vector.

What does one parameter mean? Suppose $\theta_{12;01}=\log 3$. Then whenever $(X_1,X_2)=(0,1)$, the factor $f_{12}$ contributes a multiplicative weight of 3 from that entry.

### Why the representation is called overcomplete

The features are not linearly independent. For example,

$$
1[(X_1,X_2)=(0,0)] + 1[(X_1,X_2)=(0,1)] + 1[(X_1,X_2)=(0,2)] = 1[X_1=0],
$$

and the same unary event can also be written using the $(X_1,X_3)$ features:

$$
1[(X_1,X_3)=(0,0)] + 1[(X_1,X_3)=(0,1)] + 1[(X_1,X_3)=(0,2)] = 1[X_1=0].
$$

So different parameter changes can cancel out and leave the overall distribution unchanged. Such changes are called **reparameterizations**.

### Misconception block

**Do not think that exponential-family coordinates are unique.**  
In overcomplete representations they are not. Different parameter vectors can define the same probability distribution.

**Do not confuse non-uniqueness of parameters with ambiguity of the model distribution.**  
The distribution itself is still well-defined; only its coordinate representation has redundancy.

### Connection to later material

This representation is the bridge to likelihood gradients and convex optimization in Section 4.7. It explains why learning in undirected models often becomes moment matching between empirical feature counts and model expectations.

### Retain / do not confuse

Retain these points:

- table-based undirected models are exponential-family models;
- local configuration indicators are the sufficient statistics;
- the representation is overcomplete because the features are linearly dependent;
- reparameterization changes parameters without changing the distribution.

Do not confuse:

- exponential-family representation with uniqueness of parameters,
- more parameters with more distinct distributions.

---

## 4.6 Gaussian models

### Why this section exists

Up to this point, most examples have involved discrete variables. But undirected graphical ideas also apply naturally to continuous models, and the most important example is the multivariate Gaussian. This section exists to show that Gaussian distributions have an undirected graph semantics in which sparsity of the **precision matrix** corresponds exactly to sparsity of the graph.

This is a major conceptual payoff. It reveals that graphical-model structure is not limited to factor tables or binary variables; it can also live inside familiar linear-algebraic objects.

### The object being introduced

A multivariate Gaussian over $X=(X_1,\dots,X_n)$ is usually written in terms of its mean vector $\mu$ and covariance matrix $\Sigma$. That is the moment form. The same distribution can be reparameterized in terms of the precision matrix

$$
J = \Sigma^{-1}
$$

and the information vector

$$
h = \mu \Sigma^{-1}.
$$

In information form, the exponent is quadratic and visibly pairwise in the coordinates of $X$.

### Formal definition

The moment form is

$$
p(X)=\mathcal N(X;\mu,\Sigma)
= (2\pi)^{-n/2}|\Sigma|^{-1/2}
\exp\left(-\frac12 (X-\mu)\Sigma^{-1}(X-\mu)^T\right).
$$

Define

$$
J=\Sigma^{-1}, \qquad h=\mu\Sigma^{-1}.
$$

Then the information form is

$$
p(X)=\mathcal N^{-1}(X;h,J)
=(2\pi)^{-n/2}|J|^{1/2}
\exp\left(-\frac12 XJX^T + hX - \frac12 hJ^{-1}h\right).
$$

### Interpretation paragraph

The quadratic term

$$
-\frac12 XJX^T
$$

contains terms of the form $J_{ij}X_iX_j$. So if $J_{ij}=0$, there is no pairwise interaction term between $X_i$ and $X_j$ in the exponent. This is why the Gaussian graphical model places an edge between $i$ and $j$ exactly when $J_{ij}\ne 0$.

The striking conclusion is:

> sparsity of the graph is the same thing as sparsity of the inverse covariance matrix.

That is one of the most important facts in Gaussian graphical modeling.

### Marginalization and conditioning

The two parameterizations make different operations easy.

If we partition variables into $X_A$ and $X_B$, then in moment form,

$$
p(X_A,X_B)=\mathcal N([X_A,X_B];\mu,\Sigma)
\quad \Rightarrow \quad
p(X_A)=\mathcal N(X_A;\mu_A,\Sigma_{AA}).
$$

So marginalization is easy in covariance form: keep the relevant subvectors and submatrices.

In information form, conditioning is easy:

$$
p(X_A\mid X_B=x_B)=\mathcal N^{-1}(X_A; h_A - J_{AB}x_B, J_{AA}).
$$

So when some variables are observed, the precision matrix of the remaining variables is just the corresponding principal submatrix. This matches the graphical intuition that conditioning removes observed nodes and leaves the remaining adjacency pattern among the unobserved variables.

### Fully worked example: Gaussian Markov chain

Consider the chain

$$
X_1 \sim \mathcal N(0,1),
\qquad
X_2 \mid X_1 \sim \mathcal N\left(\frac12 X_1, 0.5\right),
\qquad
X_3 \mid X_2 \sim \mathcal N(X_2,1).
$$

We want to see whether the undirected graphical interpretation recovers the chain structure.

First compute the mean. Since $E[X_1]=0$,

$$
E[X_2]=\frac12 E[X_1]=0,
\qquad
E[X_3]=E[X_2]=0.
$$

So the mean vector is zero.

Next compute the covariances.

- $E[X_1^2]=1$.
- Since $X_2=\frac12 X_1+\varepsilon_2$ with independent $\varepsilon_2\sim\mathcal N(0,0.5)$,

$$
  E[X_1X_2]=E\left[X_1\cdot \frac12 X_1\right]=\frac12.
$$

- Since $X_3=X_2+\varepsilon_3$ with independent $\varepsilon_3\sim\mathcal N(0,1)$,

$$
  E[X_1X_3]=E[X_1X_2]=\frac12.
$$

- Also,

$$
  E[X_2^2]=E\left[\left(\frac12 X_1\right)^2\right]+0.5 = \frac14 + 0.5 = \frac34.
$$

- Then

$$
  E[X_2X_3]=E[X_2^2]=\frac34,
  \qquad
  E[X_3^2]=E[X_2^2]+1=\frac74.
$$

So

$$
\Sigma=
\begin{bmatrix}
1 & 0.5 & 0.5 \\
0.5 & 0.75 & 0.75 \\
0.5 & 0.75 & 1.75
\end{bmatrix}.
$$

Now invert it. The chapter gives

$$
J=\Sigma^{-1}=
\begin{bmatrix}
1.5 & -1 & 0 \\
-1 & 3 & -1 \\
0 & -1 & 1
\end{bmatrix}.
$$

Now inspect the off-diagonal pattern.

- $J_{12}\ne 0$: edge between $X_1$ and $X_2$.
- $J_{23}\ne 0$: edge between $X_2$ and $X_3$.
- $J_{13}=0$: no edge between $X_1$ and $X_3$.

Therefore the undirected graph is exactly the chain $X_1 - X_2 - X_3$, and the zero entry $J_{13}=0$ expresses the conditional independence

$$
X_1 \perp X_3 \mid X_2.
$$

### Misconception block

**Do not confuse a zero covariance entry with a missing edge in a Gaussian graphical model.**  
Edges are controlled by the precision matrix $J=\Sigma^{-1}$, not by the covariance matrix itself.

**Do not confuse marginal independence with conditional independence.**  
In the Gaussian chain above, $X_1$ and $X_3$ are correlated marginally, but conditionally independent given $X_2$.

### Connection to later material

Gaussian models show that graphical sparsity and computational convenience are tightly linked. They also foreshadow later algorithms where solving linear systems and exploiting sparse precision matrices become central.

### Retain / do not confuse

Retain these points:

- multivariate Gaussians admit an undirected graphical interpretation;
- the precision matrix $J$ determines graph edges;
- covariance form makes marginalization easy;
- information form makes conditioning easy.

Do not confuse:

- covariance sparsity with graph sparsity,
- zero marginal correlation with conditional independence.

---

## 4.7 Learning from data

### Why this section exists

A graphical model is useful only if we can fit it to data. In Bayesian networks with known structure and complete data, the local conditional-probability parameterization led to simple closed-form maximum-likelihood estimates. In undirected models, the situation is harder because the parameters jointly determine the normalization constant. This section exists to explain exactly where that extra difficulty comes from and what tools are used to handle it.

The key conceptual shift is this: in an undirected model, changing one factor changes the partition function, and therefore changes the normalized probabilities everywhere.

---

### Maximum likelihood learning

#### The object being introduced

Suppose the graph structure is fixed and we want to estimate the factor parameters from data $D=\{x^{(1)},\dots,x^{(m)}\}$. For a table-based undirected model with log-factors $\theta_\alpha(X_\alpha)$, the log-likelihood must balance two opposing terms:

- a data-fit term that rewards configurations appearing in the data,
- a log-partition term that penalizes overall mass assignment and enforces normalization.

#### Formal definition

For a model

$$
p_\theta(X)=\frac{1}{Z(\theta)}\exp\left(\sum_\alpha \theta_\alpha(X_\alpha)\right),
$$

the log-likelihood of the data is

$$
L(\theta)=\sum_{s=1}^m \sum_\alpha \theta_\alpha(x_\alpha^{(s)}) - m\log Z(\theta).
$$

Its gradient with respect to one local table entry $\theta_\alpha(x_\alpha)$ is

$$
\frac{\partial L}{\partial \theta_\alpha(x_\alpha)}
= \sum_{s=1}^m 1[x_\alpha^{(s)}=x_\alpha] - m\,E_\theta[1[X_\alpha=x_\alpha]].
$$

#### Interpretation paragraph

This is the same moment-matching structure seen in exponential families. The first term is the empirical count of how often the local configuration $x_\alpha$ appears in the data. The second term is how often the current model expects to see it. At the maximum-likelihood solution, these match.

The problem is that the model expectation requires either the partition function or local marginals under the current model, both of which may be expensive to compute.

#### Why learning is harder than in Bayesian networks

In a Bayesian network, each local conditional table can be estimated independently because normalization is enforced locally, row by row. In an undirected model, there is one global normalization constant $Z(\theta)$. Changing one factor changes that constant and therefore changes the normalized distribution everywhere. That is why the parameters are coupled.

---

### Tree-structured graphs

#### Why this subsection exists

Not all undirected models are equally hard to learn. Trees are special because a tree-structured MRF is equivalent, in its conditional-independence structure, to a suitably oriented Bayesian network. This restores the possibility of closed-form maximum-likelihood estimation.

#### The object being introduced

If the undirected graph is pairwise and acyclic, choose any root and orient the edges away from it. The resulting directed tree defines an equivalent Bayesian network. Its conditional probabilities can be estimated empirically, and those estimates induce a maximum-likelihood estimate for the original undirected model.

#### Symmetric closed-form expression

For a tree-structured undirected model, one convenient estimator is

$$
\hat p(X) = \left(\prod_i \hat p_i(X_i)\right)
\left(\prod_{(i,j)\in E}
\frac{\hat p_{ij}(X_i,X_j)}{\hat p_i(X_i)\hat p_j(X_j)}
\right).
$$

This formula multiplies the empirical unary marginals and then corrects them using pairwise dependence ratios along the edges.

#### Fully worked example

Using the same three-variable chain as in the earlier Bayesian-network chapter, with graph

$$
X_1 - X_2 - X_3,
$$

suppose the data produce empirical marginals

$$
\hat p_1(X_1=0)=2/10, \quad \hat p_1(X_1=1)=8/10,
$$

$$
\hat p_2(X_2=0)=4/10, \quad \hat p_2(X_2=1)=6/10,
$$

$$
\hat p_3(X_3=0)=4/10, \quad \hat p_3(X_3=1)=6/10,
$$

and empirical pairwise marginals that imply

$$
\hat p_{12}(0,0)=1/10, \qquad \hat p_{23}(0,0)=2/10.
$$

We want $\hat p(0,0,0)$.

Apply the tree formula in a careful order.

1. Start with the unary product:

$$
   \hat p_1(0)\hat p_2(0)\hat p_3(0)
   = (2/10)(4/10)(4/10).
$$

2. Correct for the edge $(1,2)$:

$$
   \frac{\hat p_{12}(0,0)}{\hat p_1(0)\hat p_2(0)}
   = \frac{1/10}{(2/10)(4/10)}.
$$

3. Correct for the edge $(2,3)$:

$$
   \frac{\hat p_{23}(0,0)}{\hat p_2(0)\hat p_3(0)}
   = \frac{2/10}{(4/10)(4/10)}.
$$

4. Multiply everything:

$$
   \hat p(0,0,0)
   = (2/10)(4/10)(4/10)
     \cdot \frac{1/10}{(2/10)(4/10)}
     \cdot \frac{2/10}{(4/10)(4/10)}
   = 0.05.
$$

This is exactly the same value obtained from any equivalent directed tree representation. The different parameterizations change the local pieces, but not the final joint distribution.

#### Misconception block

**Do not think every undirected model can be learned this way.**  
The closed-form trick depends critically on tree structure. Cycles destroy the local decoupling.

---

### Iterative proportional fitting

#### Why this subsection exists

For models with cycles, closed forms usually disappear. But the gradient condition still says that the fitted model should match the empirical clique marginals on the factors present in the model. Iterative proportional fitting, or IPF, exploits exactly that insight.

#### The object being introduced

IPF is a block-coordinate ascent method. One factor at a time, it updates the factor so that the model's marginal on that factor scope matches the desired empirical marginal, while holding the other factors fixed.

#### Update rule

If the current model marginal on scope $\alpha$ is $p(X_\alpha)$ and the target empirical marginal is $\hat p_D(X_\alpha)$, then update

$$
f_\alpha(X_\alpha) \leftarrow f_\alpha(X_\alpha)
\frac{\hat p_D(X_\alpha)}{p(X_\alpha)}.
$$

One typically rescales the factor afterward for numerical stability.

#### Why this update makes sense

Hold all factors except $f_\alpha$ fixed. Then the current marginal on $X_\alpha$ is proportional to

$$
f_\alpha(X_\alpha) g(X_\alpha),
$$

where $g$ summarizes the rest of the model. Multiplying $f_\alpha$ by the ratio $\hat p_D/p$ forces the resulting marginal on $X_\alpha$ to equal the target marginal exactly. The catch is that this update perturbs other marginals, so the process must cycle until convergence.

#### Fully worked example

Suppose $X=(A,B,C)$ is binary and we want to fit the pairwise model

$$
p(X) \propto f_{AB}(A,B)f_{BC}(B,C)f_{AC}(A,C)
$$

to an empirical distribution in which

$$
\hat p_{AB}(0,0)=0.4,\quad \hat p_{AB}(0,1)=0.3,\quad \hat p_{AB}(1,0)=0.1,\quad \hat p_{AB}(1,1)=0.2.
$$

Assume our current model has marginal

$$
p_{AB}(0,0)=0.047,\quad p_{AB}(0,1)=0.163,\quad p_{AB}(1,0)=0.279,\quad p_{AB}(1,1)=0.512.
$$

The model is clearly mismatched to the data on this pair. To update $f_{AB}$, multiply each entry by the ratio of target to current:

$$
\frac{0.4}{0.047},\quad \frac{0.3}{0.163},\quad \frac{0.1}{0.279},\quad \frac{0.2}{0.512}.
$$

After this update and renormalization, the model's new $AB$ marginal matches the empirical $AB$ marginal exactly.

But now the $AC$ and $BC$ marginals may have moved away from their targets. So:

1. compute current $p_{BC}$,
2. update $f_{BC}$ by the corresponding ratio,
3. compute current $p_{AC}$,
4. update $f_{AC}$,
5. repeat the cycle.

Each update improves the likelihood with respect to that block of parameters, and the overall likelihood rises until convergence.

#### Interpretation paragraph

IPF is a clean example of how factorization acts as regularization. The fitted model is not trying to reproduce every entry of the empirical joint distribution unless the factorization is rich enough to do so. It is only trying to match the marginals associated with the chosen factor scopes.

That is why, in the chapter's example, the fitted pairwise model remains strictly positive even for a configuration that was never observed in the data. The model class does not permit an arbitrary full joint table; it permits only distributions that factor pairwise.

---

### Pseudo-likelihood

#### Why this subsection exists

Even IPF may be costly because it still requires computing marginals under the current model, and exact marginalization is hard in large cyclic graphs. Pseudo-likelihood solves a simpler optimization problem that avoids the global partition function entirely.

#### Formal definition

The pseudo-log-likelihood is

$$
PL = \sum_{s=1}^m \sum_i \log p(X_i=x_i^{(s)} \mid X_{\neg i}=x_{\neg i}^{(s)}),
$$

where $X_{\neg i}$ denotes all variables except $X_i$.

#### Interpretation paragraph

Instead of asking the model to assign high joint probability to the full data vector, pseudo-likelihood asks the model to predict each variable from the rest of the variables, one conditional at a time. Each term is easy to normalize because it is only a distribution over a single variable.

The price is conceptual: the objective double-counts dependence information. In a two-variable model, both terms use the full value of the other variable as context, whereas the true chain-rule likelihood would only get that information once.

#### Fully worked contrast with ordinary likelihood

For a single observation $(A=a,B=b)$, the true log-likelihood can be written as

$$
L = \log p(A=a) + \log p(B=b\mid A=a).
$$

The pseudo-log-likelihood is instead

$$
PL = \log p(A=a\mid B=b) + \log p(B=b\mid A=a).
$$

The second term is the same in both. The first differs. In the true likelihood, the model must explain $A=a$ without already knowing $B=b$. In pseudo-likelihood, it gets to use $B=b$ as conditioning information. That is why pseudo-likelihood is not itself a genuine joint-probability score.

#### Example: Boltzmann pseudo-likelihood as coupled logistic regressions

For the Boltzmann model with $X_i\in\{0,1\}$, the conditional distribution of a single variable has the form

$$
p(X_i\mid X_{\neg i}=x_{\neg i}) \propto
\exp\left(X_i\left(b_i + \sum_{j\ne i}\theta_{ij}x_j\right)\right).
$$

Since $X_i$ is binary,

$$
p(X_i=1\mid X_{\neg i}=x_{\neg i})
= \left(1+\exp\left(-b_i-\sum_{j\ne i}\theta_{ij}x_j\right)\right)^{-1}.
$$

So each local conditional is a logistic-regression-style probability.

This is extremely useful computationally. It means pseudo-likelihood optimization in a Boltzmann machine resembles training a collection of linked logistic regression models, one for each node.

#### Misconception block

**Do not say pseudo-likelihood is “the same as” likelihood.**  
It is a surrogate objective. It may have similar maximizers in favorable settings, but the objectives are not identical.

**Do not say pseudo-likelihood ignores the graph.**  
Each local conditional depends only on the Markov blanket, so the graph structure is still central.

### Connection to later material

Learning in undirected models is where inference and estimation become inseparable. Exact maximum likelihood needs partition functions or marginals; IPF needs repeated marginal computations; pseudo-likelihood avoids global normalization by replacing the objective. These are the first signs of the computational complexity that becomes central in the next chapter.

### Retain / do not confuse

Retain these points:

- maximum likelihood in undirected models matches empirical and model feature expectations;
- the partition function couples all parameters and makes learning hard;
- tree-structured models are special and admit closed-form estimation;
- IPF repeatedly forces local marginals to match empirical ones;
- pseudo-likelihood replaces the global objective by a sum of local conditionals.

Do not confuse:

- local factor updates with independence of parameters,
- pseudo-likelihood with true likelihood,
- empirical joint frequencies with what a restricted factorization can represent.

---

## Chapter synthesis

Undirected graphical models replace the directed semantics of conditional probabilities with a more general factorization semantics. A global configuration receives a score from the product of local nonnegative factors, and normalization via the partition function turns those scores into probabilities. That simple change makes the framework flexible enough to cover deterministic constraints, soft local preferences, pairwise binary models such as Boltzmann and Ising systems, weighted logical formulas, Gaussian graphical models, and many others.

The graph has a clean meaning: it records local interaction structure. In a factor graph, that meaning is explicit through factor scopes. In a Markov random field, it is summarized by variable adjacency. Conditioning is simpler than in Bayesian networks because observed variables can be substituted directly into unnormalized factors, so graph separation immediately gives conditional independence. Under strict positivity, Hammersley-Clifford tells us that this separation structure is not merely a consequence of factorization but is equivalent to factorization over cliques.

The chapter also makes clear why undirected learning is harder than directed learning. The partition function is global, so parameters cannot usually be fit independently. Maximum likelihood becomes a moment-matching problem, trees form a tractable special case, iterative proportional fitting performs repeated local corrections, and pseudo-likelihood offers a computationally cheaper surrogate objective.

The enduring lesson is that undirected models are not just “Bayesian networks without arrows.” They are a different probabilistic language, designed for systems where local compatibility, symmetry, and mutual interaction are the natural primitives. Understanding that language is essential for later work on inference, optimization, statistical physics models, structured prediction, and modern probabilistic machine learning.

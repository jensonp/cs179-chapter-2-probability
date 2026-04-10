# Bayesian Networks

Source: `../notes/03_bayesnet_reconstructed/source/03_bayesnet.original.pdf`

This chapter rebuilds Bayesian networks from first principles, with the goal of making the representation usable rather than merely recognizable. A Bayesian network (BN) is not “a graph with probabilities on it.” It is a disciplined way to:

1) **represent** a high-dimensional joint distribution compactly using conditional independence, and  
2) **reason** about what information can and cannot flow through a model when you condition on observations.

The payoff comes later: once you can factor a joint distribution correctly and read conditional independence off a graph, you can design inference algorithms (e.g., variable elimination), learn parameters from data, and—when additional assumptions are justified—reason about interventions.

Throughout, we assume a reader who is comfortable with Chapter 2 basics: random variables, joint distributions, conditioning, Bayes’ rule, and conditional independence.

## 3.0 Orientation: What Problem Are We Solving?

### WHY THIS SECTION EXISTS

Probability theory lets you talk about uncertainty over one or a few variables with tables (discrete) or densities (continuous). But real models in AI and statistics almost never involve “one variable.” They involve many interacting variables: symptoms, diseases, tests; words in a sentence; hidden states in time; user attributes and actions. The joint space is enormous, and the naive representation of a joint distribution becomes computationally and statistically impossible.

This section exists to make the core pressure explicit: **the joint distribution is the object we want**, but it is usually far too large to store or learn directly. Bayesian networks are introduced exactly to bridge that gap.

### THE OBJECT BEING INTRODUCED

The object we are trying to control is a **joint distribution** over a tuple of random variables

$$
X = (X_1,\dots,X_n).
$$

What is fixed and what varies depends on the task:

- In **model specification**, the variables and their domains are fixed; we choose a representation for the family of joint distributions we will allow.
- In **inference**, the model is fixed and we vary the evidence (observations) and the query (what probability we want).
- In **learning**, the graph structure may be fixed (parameter learning) or may vary (structure learning), and the conditional probability parameters vary to fit data.

The key question is: How can we represent and manipulate $p(x_1,\dots,x_n)$ without writing a table with one entry per configuration?

### BOUNDARY CONDITIONS / ASSUMPTIONS / FAILURE MODES

Bayesian networks do not magically make “hard problems easy.” They trade one kind of difficulty for another:

- They make the model compact **only when** the world exhibits conditional independence structure that matches a sparse graph.
- They make many inferences tractable **only when** the graph has favorable structure (e.g., small treewidth). Otherwise exact inference can still be exponential.
- They can be interpreted causally **only with extra assumptions** (and sometimes extra variables). The directed edges alone do not guarantee causality.

### CONNECTION TO LATER MATERIAL

This chapter is the representation layer. Later chapters can then treat inference (how to answer queries), learning (how to fit parameters/structure), and causal reasoning (how to talk about interventions) as operations on this representation rather than starting from scratch each time.

### RETAIN / DO NOT CONFUSE

- Retain: the target object is the **joint distribution**; Bayesian networks are a **structured factorization** of it.
- Do not confuse: “graphical model” (a representation) with “graph algorithm” (a procedure); the graph constrains factorization and independence, not an algorithm by itself.

## 3.1 Bayesian Networks as Factorizations of a Joint Distribution

### WHY THIS SECTION EXISTS

If we cannot store a full joint distribution table, we need another representation. The only representation that is always available, without assumptions, is the chain rule (repeated conditioning). But the chain rule alone does not reduce complexity: it merely reorganizes it. This section exists to show what extra ingredient creates compression:

**conditional independence**, encoded by a directed acyclic graph (DAG).

### THE OBJECT BEING INTRODUCED

The new object is a **Bayesian network**, which is a pair:

1) a directed acyclic graph $G$ whose nodes are the variables, and  
2) a collection of conditional probability distributions (CPDs), one per variable, that specify how each variable depends on its parents in $G$.

The role of this object is precise: it defines a joint distribution by multiplying local conditionals. The graph tells you which conditionals you are allowed to use (and therefore which conditional independence assumptions you are asserting).

What is fixed:

- the variable set $\{X_1,\dots,X_n\}$ and their domains,
- the graph $G$ (for a fixed model family),
- the meaning of “parents” and “children” in that graph.

What varies:

- the CPD parameters (when learning),
- the evidence values (when doing inference),
- sometimes the structure $G$ (when doing structure learning).

### FORMAL DEFINITION

A **Bayesian network** over variables $X_1,\dots,X_n$ consists of:

1) a directed acyclic graph (DAG) $G=(V,E)$ with one node per variable, and  
2) for each node $i$, a conditional distribution $p(x_i \mid x_{\mathrm{pa}(i)})$ where $\mathrm{pa}(i)$ is the set of parents of $i$ in $G$.

It defines a joint distribution by the **BN factorization**

$$
p(x_1,\dots,x_n) \;=\; \prod_{i=1}^n p(x_i \mid x_{\mathrm{pa}(i)}).
$$

### INTERPRETATION PARAGRAPH

Read the factorization left-to-right as: “to compute the probability of a full assignment $x$, compute each variable’s probability conditioned only on its parents, then multiply.” The parent set is the model’s claim about which variables are directly relevant when predicting $X_i$ inside the joint. If the graph is sparse, each factor is small, so the whole product can be specified with far fewer numbers than a full joint table.

This is not a statement about time or causality yet. It is a statement about which conditionals are used to build the joint.

### BOUNDARY CONDITIONS / ASSUMPTIONS / FAILURE MODES

1) **Acyclicity matters.** If $G$ has a directed cycle, you cannot order the product in a way that defines a proper joint distribution by the BN factorization. (There are other models for cycles, but they are not Bayesian networks in this sense.)

2) **The factorization is an assumption.** Not every real-world joint distribution matches a sparse BN. If the true distribution has “dense” dependencies, a sparse BN will be misspecified; it may still be useful, but it is an approximation.

3) **Discrete vs continuous.** The definition works for continuous variables too, but you must interpret $p(x_i \mid x_{\mathrm{pa}(i)})$ as a conditional density when appropriate. You do not get to mix PMF and PDF semantics casually; you must keep track of what kind of object each factor is.

4) **Do not overread direction.** The arrow $X \to Y$ does not automatically mean “$X$ causes $Y$.” It means “$Y$’s CPD is indexed by $X$,” i.e., $Y$ is conditioned on $X$ in the factorization.

### FULLY WORKED EXAMPLE: The Burglar Alarm Network

We build a small BN to see exactly what is being specified.

**Setup (variables).** Let the variables be binary:

- $B \in \{0,1\}$: burglary occurs,
- $E \in \{0,1\}$: earthquake occurs,
- $A \in \{0,1\}$: alarm rings,
- $W \in \{0,1\}$: Watson calls,
- $H \in \{0,1\}$: Hudson calls.

**Graph (structure).** Suppose we choose edges

- $B \to A$, $E \to A$ (alarm depends on burglary and earthquake),
- $A \to W$, $A \to H$ (calls depend on alarm).

In parent notation:

$$
\mathrm{pa}(B)=\varnothing,\quad \mathrm{pa}(E)=\varnothing,\quad \mathrm{pa}(A)=\{B,E\},\quad \mathrm{pa}(W)=\{A\},\quad \mathrm{pa}(H)=\{A\}.
$$

**CPDs (numbers).** A BN is incomplete until you supply CPDs. For example, pick:

| $p(B)$ | value |
|---|---|
| $p(B=1)$ | $0.001$ |
| $p(B=0)$ | $0.999$ |

| $p(E)$ | value |
|---|---|
| $p(E=1)$ | $0.002$ |
| $p(E=0)$ | $0.998$ |

| $p(W=1\mid A)$ | $A=0$ | $A=1$ |
|---|---:|---:|
| value | $0.05$ | $0.90$ |

| $p(H=1\mid A)$ | $A=0$ | $A=1$ |
|---|---:|---:|
| value | $0.01$ | $0.70$ |

| $p(A=1\mid B,E)$ | $B=0,E=0$ | $B=0,E=1$ | $B=1,E=0$ | $B=1,E=1$ |
|---|---:|---:|---:|---:|
| value | $0.001$ | $0.75$ | $0.95$ | $0.98$ |

These tables are the entire model.

**Reasoning step (identify the joint).** The BN factorization says:

$$
p(b,e,a,w,h) = p(b)\,p(e)\,p(a\mid b,e)\,p(w\mid a)\,p(h\mid a).
$$

**Compute one joint probability.** Consider the configuration $(B,E,A,W,H)=(0,1,1,1,0)$. We compute:

1) choose the right entry from each CPD row/column,  
2) multiply them.

Concretely:

$$
p(0,1,1,1,0)
=
p(B=0)\,p(E=1)\,p(A=1\mid B=0,E=1)\,p(W=1\mid A=1)\,p(H=0\mid A=1).
$$

Using the chosen values:

$$
0.999 \times 0.002 \times 0.75 \times 0.90 \times (1-0.70)
=
0.999 \times 0.002 \times 0.75 \times 0.90 \times 0.30
\approx 0.000405.
$$

**Interpretation.** The number is small because it includes a rare earthquake and multiple dependent events. The important lesson is structural: the BN tells you which local probabilities you multiply.

**Why this is compact.** A full joint over five binary variables has $2^5=32$ entries (31 degrees of freedom). The BN needs only:

- $p(B)$: 1 free parameter,
- $p(E)$: 1 free parameter,
- $p(A\mid B,E)$: 4 free parameters (one per parent configuration, since binary child),
- $p(W\mid A)$: 2 free parameters,
- $p(H\mid A)$: 2 free parameters,

for a total of 10 free parameters. The savings come from the assumption that each variable depends only on its parents, not on all earlier variables.

### MISCONCEPTION OR COUNTEREXAMPLE BLOCK

**Misconception: “The factorization is always true by the chain rule.”**  
The chain rule always gives

$$
p(x_1,\dots,x_n) = \prod_{i=1}^n p(x_i \mid x_1,\dots,x_{i-1}).
$$

The BN factorization replaces the full history $(x_1,\dots,x_{i-1})$ with only the parent set $x_{\mathrm{pa}(i)}$. That replacement is not automatic; it is exactly the conditional independence claim

$$
X_i \perp \{X_1,\dots,X_{i-1}\}\setminus \mathrm{pa}(i)\;\mid\; X_{\mathrm{pa}(i)}.
$$

If this conditional independence fails in the true distribution, the BN factorization is wrong for that distribution.

### CONNECTION TO LATER MATERIAL

The BN factorization is the gateway to:

- **Inference:** computing $p(\text{query}\mid \text{evidence})$ without summing over all $2^n$ states (later: variable elimination and message passing).
- **Learning:** estimating each CPD from data using counts (discrete) or regression-like models (continuous).
- **Model design:** encoding assumptions in structure rather than hiding them in an opaque joint table.

### RETAIN / DO NOT CONFUSE

- Retain: a BN is a **DAG + CPDs**; the DAG determines a product factorization of the joint.
- Do not confuse: the BN factorization with “causal mechanisms.” Direction is a modeling choice unless extra causal assumptions are stated.

### GRAPH VOCABULARY YOU MUST CONTROL (AND WHY IT MATTERS)

#### WHY THIS SUBSECTION EXISTS

Bayesian networks are simple enough that people often “read the picture” without controlling the definitions. That works until you need to prove an independence claim, debug an inference computation, or compare two candidate structures. This subsection exists to pin down the basic graph objects you will use repeatedly.

#### THE OBJECT BEING INTRODUCED

The object is a set of graph-theoretic definitions attached to a BN graph $G$. Each definition answers a different “who can influence whom?” question.

#### FORMAL DEFINITIONS

Let $G=(V,E)$ be a DAG with one node per variable.

- **Parents.** $\mathrm{pa}(i) = \{j : (j \to i)\in E\}$.
- **Children.** $\mathrm{ch}(i) = \{j : (i \to j)\in E\}$.
- **Root.** A node with $\mathrm{pa}(i)=\varnothing$.
- **Leaf.** A node with $\mathrm{ch}(i)=\varnothing$.
- **Directed path.** A sequence $i_1 \to i_2 \to \cdots \to i_k$ following arrow directions.
- **Ancestor / descendant.** $a$ is an ancestor of $i$ if there is a directed path $a \to \cdots \to i$. $d$ is a descendant of $i$ if there is a directed path $i \to \cdots \to d$.
- **Undirected path.** A sequence of nodes connected by edges ignoring arrow direction.

#### INTERPRETATION PARAGRAPH

Parents are not “everything that influences $X_i$.” They are the variables you condition on in $X_i$’s CPD inside the factorization. Ancestors are “everything that could influence $X_i$ through directed flow,” but they are not the same as parents: ancestors can act indirectly through intermediate variables.

Undirected paths matter because d-separation is about the existence of **any** path that can transmit dependence once conditioning is taken into account, regardless of arrow direction.

#### FULLY WORKED EXAMPLE (BURGlar GRAPH NAVIGATION)

In the burglar alarm BN:

$$
B \to A \leftarrow E,\qquad A \to W,\qquad A \to H,
$$

we have:

- roots: $B$ and $E$ (no parents),
- leaves: $W$ and $H$ (no children),
- descendants of $B$: $\{A,W,H\}$ (paths $B\to A\to W$ and $B\to A\to H$),
- ancestors of $W$: $\{A,B,E\}$ (paths $B\to A\to W$ and $E\to A\to W$).

This is not just terminology: when we say “conditioning on a collider or its descendant opens a path,” the word descendant is doing real work.

#### MISCONCEPTION OR COUNTEREXAMPLE BLOCK

**Misconception: “If there is an undirected path between $X$ and $Y$, then they are dependent.”**  
Undirected connectivity alone is not enough. In a BN, whether a path transmits dependence depends on collider/non-collider status and the evidence set. That is exactly why d-separation exists.

#### CONNECTION TO LATER MATERIAL

These definitions are the atoms used in:

- d-separation proofs (“descendant in evidence opens collider”),
- local inference updates (Markov blankets),
- causal discussions (“cut incoming edges” is defined in terms of parents).

#### RETAIN / DO NOT CONFUSE

- Retain: parents (conditioning set in CPD) are not the same as ancestors (all upstream nodes).
- Do not confuse: directed paths (ancestry) with undirected paths (potential dependence flow under conditioning).

### WHY THE CONDITIONING ORDER MATTERS (AND WHY “CAUSAL” ORDERINGS TEND TO BE SPARSE)

#### WHY THIS SUBSECTION EXISTS

At first glance, BNs can look arbitrary: why choose one arrow direction over another? One answer is computational or statistical (“this direction makes CPDs simple”). Another is causal (when justified). This subsection exists to explain a foundational fact:

> Any joint distribution can be written as a BN over some ordering, but the resulting graph can be extremely dense unless conditional independences align with the ordering.

#### THE OBJECT BEING INTRODUCED

The object is a **topological ordering** of the variables and the chain-rule expansion it induces. The ordering is fixed; the question is whether conditional independence lets you shrink parent sets in that ordering.

#### FORMAL DEFINITION (CHAIN RULE OVER AN ORDER)

Fix an ordering $(X_{\pi(1)},\dots,X_{\pi(n)})$. The chain rule gives:

$$
p(x_{\pi(1)},\dots,x_{\pi(n)}) = \prod_{k=1}^n p(x_{\pi(k)} \mid x_{\pi(1)},\dots,x_{\pi(k-1)}).
$$

This always defines a valid BN if you set $\mathrm{pa}(\pi(k))=\{\pi(1),\dots,\pi(k-1)\}$, i.e., connect each node to all earlier nodes.

#### INTERPRETATION PARAGRAPH

So a BN is not “more expressive” than ordinary probability. Its value is that, if the world has conditional independence, many of those edges are unnecessary: you can replace the full history with a smaller parent set without changing the joint. Sparse graphs are therefore not a mystery; they are the graph’s way of recording which conditionals actually matter.

Why do “causal” orderings often help? Because physical or logical causation tends to be local: effects often depend directly on a few causes, not on everything that happened earlier. If you order causes before effects, many CPDs naturally simplify.

#### FULLY WORKED EXAMPLE (A BAD ORDER CREATES DENSITY)

In the burglar setting, the “intuitive” ordering is $(B,E,A,W,H)$, giving a sparse BN:

$$
p(b,e,a,w,h)=p(b)\,p(e)\,p(a\mid b,e)\,p(w\mid a)\,p(h\mid a).
$$

Now consider the reversed-feeling ordering $(H,W,A,B,E)$. The chain rule gives:

$$
p(h,w,a,b,e)=p(h)\,p(w\mid h)\,p(a\mid h,w)\,p(b\mid h,w,a)\,p(e\mid h,w,a,b).
$$

Even if the true joint is the same, the CPDs in this order are typically “fatter”:

- $W$ and $H$ are not independent (they share cause $A$), so $p(w\mid h)$ cannot simplify to $p(w)$.
- $A$ is not independent of $W$ or $H$ given the other; two calls together are stronger evidence about $A$ than either alone.

Some later conditionals can simplify (e.g., once you know $A$, the calls add little about $B$), but the general lesson is: a poor ordering hides conditional independences and produces larger CPDs.

#### MISCONCEPTION OR COUNTEREXAMPLE BLOCK

**Misconception: “The graph is unique for a given distribution.”**  
Different orderings yield different DAGs that can represent the same joint distribution. The graph is part of the modeler’s representation choice; it is not uniquely determined by the joint.

#### CONNECTION TO LATER MATERIAL

Ordering sensitivity shows up in:

- inference algorithms (elimination order controls complexity),
- structure learning (many graphs can explain the same data),
- causality (direction is meaningful only with extra assumptions).

#### RETAIN / DO NOT CONFUSE

- Retain: chain rule always works, but sparsity comes from conditional independence.
- Do not confuse: “sparser” with “truer.” Sparsity is useful, but it is still an assumption about the world.

## 3.2 Graph Semantics: Independence, Information Flow, and d-Separation

### WHY THIS SECTION EXISTS

The whole point of a Bayesian network is not merely to store a joint distribution compactly, but to make **conditional independence** easy to reason about. Independence is the lever that makes inference algorithms and learning decompositions work.

However, conditional independence behaves in ways that often surprise students—especially the fact that conditioning can create dependence. This section exists to make the graph-to-independence connection precise and to build reliable intuition for when information can flow through a BN.

### THE OBJECT BEING INTRODUCED

The object here is a **graph criterion** that answers a probabilistic question:

> Given three sets of variables $A$, $B$, and evidence $E$, can the graph certify that $X_A$ is conditionally independent of $X_B$ given $X_E$?

What is fixed:

- the graph $G$,
- the evidence set $E$ (which variables are conditioned on).

What varies:

- which two sets $A$ and $B$ you are asking about,
- which conditioning set you choose (changing $E$ can change dependence dramatically).

The key conclusion the criterion licenses is: “for every distribution that factors over $G$, this conditional independence must hold.”

### FORMAL DEFINITION (d-Separation)

Let $G$ be a DAG. Consider an undirected path between two nodes. A node on the path is a **collider** on that path if the arrows meet head-to-head at that node (pattern $\to Z \leftarrow$ along the path).

A path is **active** (or “open”) given evidence set $E$ if:

1) every **non-collider** on the path is not in $E$, and  
2) every **collider** on the path has **itself or at least one descendant** in $E$.

Two sets of nodes $A$ and $B$ are **d-separated** by $E$ if **every** path between a node in $A$ and a node in $B$ is inactive given $E$.

### INTERPRETATION PARAGRAPH

d-Separation is a graph-language way to talk about which conditional independences are forced by the factorization. You can think of it as “information flow” under conditioning, but the rule has one central twist:

- Conditioning on a **non-collider** blocks a path.
- Conditioning on a **collider** (or a collider’s descendant) opens a path.

The most important way to make this reliable is to study the three canonical local patterns. Nearly every “why did dependence appear/disappear?” question reduces to one of these.

### THE THREE CANONICAL PATTERNS (CHAIN, FORK, COLLIDER)

#### WHY THIS SUBSECTION EXISTS

Many students memorize d-separation as a rule and then forget it under pressure. The three patterns below are the usable mental model. Once you can recognize them inside a larger graph, you can reason correctly about conditional independence without re-deriving probability identities from scratch.

#### THE OBJECT BEING INTRODUCED

The object is a path segment with three variables. The question it answers is: “Does observing the middle variable block or open the flow of dependence between the endpoints?”

#### FORMAL DEFINITIONS (LOCAL PATTERNS)

1) **Chain:** $X \to Z \to Y$ (or $X \leftarrow Z \leftarrow Y$).  
2) **Fork:** $X \leftarrow Z \to Y$.  
3) **Collider (vee-structure):** $X \to Z \leftarrow Y$.

#### INTERPRETATION PARAGRAPH

All three patterns can produce marginal dependence between $X$ and $Y$. The difference is what happens when you condition.

- In a **chain** or **fork**, conditioning on the middle variable $Z$ removes the dependence between $X$ and $Y$ (it blocks the path).
- In a **collider**, conditioning on the middle variable $Z$ (or anything downstream of it) creates dependence between $X$ and $Y$ (it opens the path).

This is the point where “conditioning = controlling for a variable” intuition can break. Conditioning is not always “removing noise”; it can be “selecting” a subset of worlds, and selection can couple variables that were previously independent.

#### BOUNDARY CONDITIONS / ASSUMPTIONS / FAILURE MODES

The statements above are about **graph-implied** conditional independence: they hold for every distribution that factors according to the BN as long as the only paths between $X$ and $Y$ are the ones you are analyzing. In a larger graph, $X$ and $Y$ can still be dependent given $Z$ if there is a different active path between them.

#### FULLY WORKED EXAMPLE (COLLIDER EXPLAINS “EXPLAINING AWAY”)

Consider the collider structure from the burglar alarm network:

$$
B \to A \leftarrow E.
$$

**Step 1 (marginal independence).** If $B$ and $E$ are independent causes, then before observing anything about $A$, we typically have $B \perp E$. In the BN, $B$ and $E$ are d-separated by the empty evidence set because the only path between them is through the collider $A$, and $A$ (and its descendants) are not conditioned on.

**Step 2 (conditioning opens dependence).** Now suppose we learn $A=1$ (the alarm rang). In words: “something happened that needs an explanation.” If $B$ is true, that makes $E$ less necessary to explain $A=1$; if $B$ is false, that makes $E$ more necessary. This is dependence created by conditioning:

$$
B \not\!\perp E \mid A.
$$

Graphically: conditioning on the collider opens the path.

**Step 3 (what the dependence means).** This is not merely a slogan. It changes rational inference. If a neighbor says the alarm rang, the posterior probability of an earthquake increases; but if you then learn there was a burglary, the posterior probability of an earthquake decreases relative to the “alarm-only” posterior. The causes “compete” to explain the effect.

#### MISCONCEPTION OR COUNTEREXAMPLE BLOCK

**Misconception: “Conditioning always makes variables more independent.”**  
Chain and fork reinforce that intuition, but collider breaks it. Conditioning is not a magical decorrelator; it is restricting the probability space to an event (e.g., $A=1$), and restriction can couple variables.

#### CONNECTION TO LATER MATERIAL

The chain/fork/collider patterns are the local building blocks for:

- **Markov blankets** (what you need to condition on to isolate a variable),
- **structure learning** (colliders are the key non-equivalence pattern),
- **causal reasoning** (colliders are where selection bias and “conditioning on a common effect” confounding appear).

#### RETAIN / DO NOT CONFUSE

- Retain: chain/fork block when conditioning on the middle; collider opens when conditioning on the middle (or its descendants).
- Do not confuse: “conditioning” with “intervening.” Conditioning on $A$ is learning information; intervening on $A$ would change the mechanism for $A$.

### FORMAL CONSEQUENCE: D-SEPARATION IMPLIES CONDITIONAL INDEPENDENCE

#### WHY THIS SUBSECTION EXISTS

Intuition is useful, but you need to know what is guaranteed. Otherwise you will treat d-separation like a heuristic rather than a theorem.

#### THE OBJECT BEING INTRODUCED

The object is a guarantee connecting a graph property (d-separation) to a distributional property (conditional independence) across the entire family of distributions that factor according to the graph.

#### FORMAL STATEMENT

If $A$ and $B$ are d-separated by $E$ in $G$, then for every distribution $p$ that factors according to $G$,

$$
X_A \perp X_B \mid X_E.
$$

Conversely, if $A$ and $B$ are **not** d-separated by $E$, then there exists at least one distribution that factors according to $G$ for which the conditional independence fails.

#### INTERPRETATION PARAGRAPH

The first direction is the one you use operationally: the graph lets you certify independence without doing algebra on the joint. The second direction prevents overconfidence: if the graph does not separate two sets, then the factorization alone does not force them to be independent; they might be independent for special parameter values, but you cannot rely on it as a structural property.

#### CONNECTION TO LATER MATERIAL

This is what makes graphical models a language: you can read guaranteed independences directly from the graph, which is crucial for designing efficient inference and learning procedures.

### FULLY WORKED EXAMPLE: d-Separation in the Burglar Alarm Graph

#### WHY THIS SUBSECTION EXISTS

Students often know the collider story but fail on mixed evidence (“observe the alarm” versus “observe a phone call”). We work through the full reasoning in the exact graph you will see again and again.

#### SETUP

Use the same graph:

$$
B \to A \leftarrow E,\qquad A \to W,\qquad A \to H.
$$

#### EXAMPLE 1: $W \perp H \mid A$

**Claim.** Watson’s call and Hudson’s call are conditionally independent given whether the alarm rang.

**Graph reasoning.** The only path between $W$ and $H$ is $W \leftarrow A \to H$, a fork with middle node $A$. Conditioning on $A$ blocks a fork. Therefore $W$ and $H$ are d-separated by $\{A\}$, hence $W \perp H \mid A$ in every distribution that factors over this graph.

**Interpretation.** If you already know whether the alarm is ringing, then Watson’s calling gives you no additional information about whether Hudson calls; their correlation is explained entirely by the shared cause $A$.

#### EXAMPLE 2: $B \perp E$ but $B \not\!\perp E \mid W$

**Claim 1 (marginal independence).** $B$ and $E$ are d-separated by $\varnothing$ because the only path between them is through the collider $A$, which is not conditioned on. Hence $B \perp E$.

**Claim 2 (conditioning on a descendant opens a collider).** If we condition on $W$, then we have conditioned on a descendant of the collider $A$ (since $A \to W$). Conditioning on a collider’s descendant activates the collider path. Therefore the path $B \to A \leftarrow E$ becomes active, and $B$ and $E$ are not d-separated given $W$. Hence, in general,

$$
B \not\!\perp E \mid W.
$$

**Interpretation.** Hearing Watson call makes “alarm rang” more likely, which triggers explaining-away competition between $B$ and $E$ even if you never observe $A$ directly.

### MARKOV BLANKETS: WHAT “SHIELDS” A VARIABLE

#### WHY THIS SUBSECTION EXISTS

In inference and learning, you repeatedly need to answer: “What part of the graph do I need to look at to predict $X_i$?” The Markov blanket makes this precise: it is the minimal neighborhood that screens off a variable from the rest.

#### THE OBJECT BEING INTRODUCED

The object is a set of nodes associated with a target node $i$ such that, once you condition on that set, the variable $X_i$ becomes independent of all other variables in the network.

#### FORMAL DEFINITION

The **Markov blanket** of node $i$ is:

$$
\mathrm{MB}(i) = \mathrm{pa}(i)\ \cup\ \mathrm{ch}(i)\ \cup\ \bigcup_{c \in \mathrm{ch}(i)} \mathrm{pa}(c)\setminus\{i\},
$$

that is: parents, children, and the other parents of its children (“co-parents”).

#### INTERPRETATION PARAGRAPH

Why these three groups?

- Parents influence $X_i$ directly (by definition of the factorization).
- Children carry information about $X_i$ (because $X_i$ influences them).
- Co-parents matter because conditioning on a child can open a collider path between $X_i$ and the child’s other parents.

The Markov blanket is exactly the set you must condition on to block every path from $i$ to the rest of the graph.

#### CONNECTION TO LATER MATERIAL

Markov blankets appear in:

- Gibbs sampling (a variable’s conditional depends only on its blanket),
- local structure learning,
- designing features for prediction and debugging dependencies in a model.

#### RETAIN / DO NOT CONFUSE

- Retain: “parents + children + co-parents” is the blanket.
- Do not confuse: the Markov blanket (a graph property) with “causes of $X_i$” (a causal claim that may not be justified).

### MARKOV EQUIVALENCE: WHAT THE GRAPH CAN’T IDENTIFY FROM OBSERVATIONS ALONE

#### WHY THIS SUBSECTION EXISTS

If you learn a BN structure from data, you are implicitly trying to read conditional independence patterns out of observations. But different DAGs can encode the same set of conditional independences. This subsection exists to explain the identifiability limit: even with infinite data, observational evidence may not tell you which way certain arrows point.

#### THE OBJECT BEING INTRODUCED

The object is an equivalence relation on DAGs: “two graphs are the same for purposes of independence reasoning.” The question it answers is: what aspects of a BN structure are determined by the independence relations, and what aspects are not?

#### FORMAL DEFINITION

Two DAGs $G_1$ and $G_2$ over the same variables are **Markov equivalent** (also called independence-equivalent) if they entail exactly the same set of conditional independence statements via d-separation.

#### INTERPRETATION PARAGRAPH

Markov equivalence means: as far as observational conditional independence is concerned, the graphs are indistinguishable. If your learning criterion is based only on how well the model matches the observed joint distribution (or its implied independences), then any graph in the equivalence class can fit equally well with appropriate parameters.

One practical characterization (worth remembering) is:

- Markov-equivalent DAGs have the same **skeleton** (the underlying undirected edges), and
- they have the same set of **v-structures** (colliders $X\to Z \leftarrow Y$ where $X$ and $Y$ are not adjacent).

#### BOUNDARY CONDITIONS / ASSUMPTIONS / FAILURE MODES

Markov equivalence is an observational statement. It does not say the graphs represent the same causal story; it says only that they encode the same conditional independences. Distinguishing directions typically requires:

- interventional data (experiments),
- time ordering assumptions,
- or domain knowledge that rules out certain directions.

#### FULLY WORKED EXAMPLE (3-NODE CASE)

Consider three variables $A,B,C$ with edges forming a chain-like skeleton $A-B-C$.

The three DAGs

$$
A\to B\to C,\qquad A\leftarrow B\to C,\qquad A\leftarrow B\leftarrow C
$$

all imply the same key conditional independence:

$$
A \perp C \mid B,
$$

and they imply no marginal independence between $A$ and $C$ (there is an active path through $B$ when unconditioned).

In contrast, the collider DAG

$$
A \to B \leftarrow C
$$

implies a different independence pattern: $A \perp C$ marginally, but $A \not\!\perp C \mid B$.

This is why colliders are special: they are the feature that breaks equivalence classes and can be identified from conditional independence tests (in idealized settings).

#### MISCONCEPTION OR COUNTEREXAMPLE BLOCK

**Misconception: “If the data says $A$ and $B$ are correlated, then $A\to B$.”**  
Correlation alone never orients an edge. Even conditional independence patterns often leave multiple orientations possible inside a Markov equivalence class.

#### CONNECTION TO LATER MATERIAL

Markov equivalence sits at the center of:

- structure learning algorithms (what they can recover from observational data),
- causal discovery (what extra assumptions are needed to orient edges),
- and why “causal interpretation of BNs” is not automatic.

#### RETAIN / DO NOT CONFUSE

- Retain: observational data often identifies an equivalence class, not a unique DAG.
- Do not confuse: “same independences” with “same causality.”

## 3.3 What Bayesian Networks Let You Do: Queries and Inference as an Operation

### WHY THIS SECTION EXISTS

A representation only matters if it supports operations. In practice, you build a BN because you want to answer questions like:

- What is $p(\text{burglary}=1 \mid \text{Watson called}=1)$?
- What is $p(A)$ (the alarm’s marginal probability)?
- If I observe some variables, how do my beliefs about others change?

This section exists to connect the factorization and d-separation to the computational question: how to compute marginals and conditionals, and why structure matters.

### THE OBJECT BEING INTRODUCED

The object here is an **inference query**, typically of the form

$$
p(X_Q \mid X_E = x_E),
$$

where:

- $Q$ is a set of query variables we care about,
- $E$ is a set of evidence variables we condition on (with observed value $x_E$),
- everything else $H = \{1,\dots,n\}\setminus(Q\cup E)$ is hidden and must be summed/integrated out.

### FORMAL DEFINITION (BASIC INFERENCE BY MARGINALIZATION)

For discrete variables, the fundamental identity is:

$$
p(x_Q \mid x_E) \;=\; \frac{\sum_{x_H} p(x_Q, x_H, x_E)}{\sum_{x_Q}\sum_{x_H} p(x_Q, x_H, x_E)}.
$$

Using the BN factorization, the joint inside the sum is a product of local CPDs.

### INTERPRETATION PARAGRAPH

The formula says: “take the joint probability of everything consistent with the evidence, add up the mass for the configurations where the query takes the value you want, then renormalize.” The difficulty is the sum over $x_H$: it is exponentially large in the number of hidden variables if done naively.

The point of the BN is that the joint is a product of small factors. Good inference algorithms exploit this product structure to reorder computations and reuse partial sums, often reducing the effective cost dramatically.

### BOUNDARY CONDITIONS / ASSUMPTIONS / FAILURE MODES

1) **Exact inference can still be exponential.** If the graph is “dense” in the wrong way, eliminating variables creates large intermediate factors. The right complexity notion is treewidth (introduced later).

2) **Graph structure matters more than direction alone.** Two Markov-equivalent DAGs encode the same independences, but they can have different computational costs for a given inference algorithm depending on how elimination proceeds.

### FULLY WORKED EXAMPLE: Writing the Posterior $p(B\mid W=1)$

We do not compute a final number here; the goal is to practice translating a question into the correct sum-product expression.

**Step 1 (name query and evidence).** Query $Q=\{B\}$, evidence $E=\{W\}$ with $W=1$. Hidden variables are $H=\{E,A,H\}$ (earthquake, alarm, Hudson call).

**Step 2 (write the posterior by marginalization).**

$$
p(B=b \mid W=1)
=
\frac{\sum_{e,a,h} p(B=b,E=e,A=a,W=1,H=h)}{\sum_{b'}\sum_{e,a,h} p(B=b',E=e,A=a,W=1,H=h)}.
$$

**Step 3 (expand the joint by the BN factorization).**

$$
p(b,e,a,w,h)=p(b)\,p(e)\,p(a\mid b,e)\,p(w\mid a)\,p(h\mid a).
$$

Plugging $w=1$:

$$
p(B=b \mid W=1)
=
\frac{\sum_{e,a,h} p(b)\,p(e)\,p(a\mid b,e)\,p(W=1\mid a)\,p(h\mid a)}{\sum_{b'}\sum_{e,a,h} p(b')\,p(e)\,p(a\mid b',e)\,p(W=1\mid a)\,p(h\mid a)}.
$$

**Step 4 (notice simplifications you are allowed to make).** Because $\sum_h p(h\mid a)=1$, the sum over $h$ disappears:

$$
\sum_h p(h\mid a)=1.
$$

So the computation reduces to summing over only $e$ and $a$.

**Interpretation.** This is already a small example of what inference algorithms do: they identify factors that can be summed out locally and reduce the dimension of the hard part.

### MISCONCEPTION OR COUNTEREXAMPLE BLOCK

**Misconception: “Inference is just plugging into Bayes’ rule.”**  
Bayes’ rule is correct but incomplete guidance. In a multi-variable model, the hard part is computing the normalization constant (a marginal likelihood) and managing large sums/integrals. Graphical structure is what makes this manageable.

### CONNECTION TO LATER MATERIAL

Later, inference becomes algorithmic:

- **Variable elimination** formalizes reordering and factor reuse.
- **Belief propagation** (on trees) explains when local message passing gives exact marginals.
- Approximate methods (sampling, variational) become necessary when exact inference is too expensive.

### RETAIN / DO NOT CONFUSE

- Retain: inference queries are “sum out hidden variables, then normalize.”
- Do not confuse: conditioning on evidence (an observation) with intervention (changing the mechanism).

## 3.4 Learning BN Parameters from Complete Data (Discrete Case)

### WHY THIS SECTION EXISTS

A BN’s graph structure tells you which conditional probabilities you need, but you still need their numerical values. In many real tasks, you do not hand-author CPDs; you learn them from data. This section exists to show the crucial simplification that BNs buy you in learning:

**the likelihood decomposes into independent pieces, one per node and parent-configuration.**

That decomposition is the practical reason BNs are learnable at scale.

### THE OBJECT BEING INTRODUCED

The object is a parameterization of a BN’s CPDs and a dataset of complete observations.

What is fixed:

- the graph $G$ (we are not doing structure learning yet),
- the variable domains.

What varies:

- the CPD parameters $\theta$,
- the dataset $D$.

The question is: how do we estimate $\theta$ from $D$?

### FORMAL DEFINITION (PARAMETERS AND LIKELIHOOD)

Assume each $X_i$ is discrete. For each $i$ and each parent configuration $u$ (a value assignment to $X_{\mathrm{pa}(i)}$), define parameters

$$
\theta_{i,x\mid u} = p(X_i=x \mid X_{\mathrm{pa}(i)}=u),
$$

with constraints $\sum_x \theta_{i,x\mid u}=1$ for every $(i,u)$.

Given a complete dataset $D=\{x^{(1)},\dots,x^{(m)}\}$ of $m$ i.i.d. samples, the log-likelihood under the BN is

$$
\ell(\theta)
=
\sum_{j=1}^m \log p(x^{(j)};\theta)
=
\sum_{j=1}^m \sum_{i=1}^n \log p(x^{(j)}_i \mid x^{(j)}_{\mathrm{pa}(i)};\theta).
$$

### INTERPRETATION PARAGRAPH

The key move is the second equality: the BN factorization turns a log of a product into a sum of local log-terms. Then the dataset sum lets you group terms by which parent configuration occurred. That means you can optimize each conditional table row independently: learning a BN with fixed structure becomes learning many small multinomial distributions rather than one massive joint.

### BOUNDARY CONDITIONS / ASSUMPTIONS / FAILURE MODES

1) **Complete data assumption.** Every sample must contain all variables’ values. Missingness breaks the simple count-based MLE and leads to latent-variable learning (e.g., EM).

2) **I.I.D. assumption.** The formula assumes samples are independent draws from the same distribution. Time series violates this; Markov models handle dependence differently.

3) **Zero counts cause brittleness.** If a parent configuration $u$ never occurs in data, the MLE for that row is undefined (division by zero). Even when $u$ occurs rarely, MLE can overfit. This motivates smoothing / priors.

### FULLY WORKED EXAMPLE: MLE IN A 3-NODE CHAIN

Consider a BN with three binary variables in a chain:

$$
X_1 \to X_2 \to X_3.
$$

So the factorization is

$$
p(x_1,x_2,x_3)=p(x_1)\,p(x_2\mid x_1)\,p(x_3\mid x_2).
$$

Suppose we observe $m=10$ complete samples:

| sample | $X_1$ | $X_2$ | $X_3$ |
|---:|---:|---:|---:|
| 1 | 1 | 0 | 0 |
| 2 | 1 | 1 | 1 |
| 3 | 1 | 1 | 1 |
| 4 | 1 | 1 | 1 |
| 5 | 1 | 1 | 0 |
| 6 | 1 | 0 | 1 |
| 7 | 1 | 1 | 1 |
| 8 | 1 | 0 | 0 |
| 9 | 0 | 1 | 0 |
| 10 | 0 | 0 | 1 |

**Step 1 (estimate $p(X_1)$).** Count how often $X_1=1$:

- $X_1=1$ occurs 8 times, $X_1=0$ occurs 2 times.

So the MLE is:

$$
\hat p(X_1=1)=8/10,\qquad \hat p(X_1=0)=2/10.
$$

**Step 2 (estimate $p(X_2\mid X_1)$).** Split the data by $X_1$.

- When $X_1=0$ (2 samples): $X_2=0$ once, $X_2=1$ once.  
  So $\hat p(X_2=1\mid X_1=0)=1/2$.
- When $X_1=1$ (8 samples): $X_2=1$ occurs 5 times, $X_2=0$ occurs 3 times.  
  So $\hat p(X_2=1\mid X_1=1)=5/8$.

**Step 3 (estimate $p(X_3\mid X_2)$).** Split the data by $X_2$.

- When $X_2=0$ (4 samples): $X_3=1$ occurs 2 times, $X_3=0$ occurs 2 times.  
  So $\hat p(X_3=1\mid X_2=0)=2/4$.
- When $X_2=1$ (6 samples): $X_3=1$ occurs 4 times, $X_3=0$ occurs 2 times.  
  So $\hat p(X_3=1\mid X_2=1)=4/6$.

**Step 4 (interpret what the BN learned).** Even if a particular full configuration never appears, the BN can still assign it nonzero probability as long as each local conditional event has support. For instance, if $X=(0,0,0)$ never appears above, the BN still gives:

$$
\hat p(0,0,0) = \hat p(X_1=0)\,\hat p(X_2=0\mid X_1=0)\,\hat p(X_3=0\mid X_2=0).
$$

This is not “hallucination”; it is the model using its independence assumptions to generalize from partial evidence.

### MISCONCEPTION OR COUNTEREXAMPLE BLOCK

**Misconception: “The best model is always the empirical joint distribution.”**  
The empirical joint fits the observed configurations perfectly, but it often assigns zero probability to unobserved configurations (even if they are plausible) and has huge variance in high dimension. A BN trades bias (independence assumptions) for variance reduction (fewer parameters), which can improve generalization.

### CONNECTION TO LATER MATERIAL

When data is incomplete or variables are latent, parameter learning becomes an inference problem itself (you must infer missing values under the model while learning). This is where EM, variational methods, and sampling enter.

### RETAIN / DO NOT CONFUSE

- Retain: with fixed structure and complete discrete data, MLE is **counts divided by parent-configuration counts** (one row at a time).
- Do not confuse: MLE (no prior) with MAP / smoothing (with a Dirichlet prior).

## 3.5 Common BN Families and Why They Exist

### WHY THIS SECTION EXISTS

In principle you can write any DAG you like. In practice, a few motifs show up repeatedly because they solve recurring modeling problems: classification with many features (naive Bayes), sequential data (Markov chains), and “many causes, one effect” with limited parameters (noisy-OR).

The goal of this section is not to give a catalog. It is to teach you how to recognize which modeling pressure each family addresses and what assumptions it is silently making.

### 3.5.1 Naive Bayes (One Label, Many Features)

#### WHY THIS SUBSECTION EXISTS

Suppose you want to predict a class label $Y$ from a large feature vector $X=(X_1,\dots,X_n)$, where $n$ can be hundreds or thousands. A full conditional model $p(Y\mid X)$ can be learned discriminatively (e.g., logistic regression), but naive Bayes is introduced because it gives a generative story and an extremely simple parameter-learning and inference pipeline, even when $n$ is huge.

#### THE OBJECT BEING INTRODUCED

The object is a BN with a single parent $Y$ and many children $X_i$. The BN asserts that the features are conditionally independent given the label.

#### FORMAL DEFINITION

Naive Bayes uses the factorization

$$
p(y,x_1,\dots,x_n) = p(y)\,\prod_{i=1}^n p(x_i\mid y).
$$

Equivalently, it assumes

$$
X_i \perp X_j \mid Y \qquad \text{for all } i\neq j.
$$

#### INTERPRETATION PARAGRAPH

The model is “naive” because the conditional independence assumption is usually false: features are often correlated even after conditioning on $Y$. But the model can still perform well for prediction because classification depends primarily on relative likelihood ratios, and naive Bayes often gets the sign of those ratios right even when it misestimates their magnitude.

#### BOUNDARY CONDITIONS / ASSUMPTIONS / FAILURE MODES

1) If features are strongly correlated in a way that differs across classes, naive Bayes can be poorly calibrated.
2) If some feature values never appear in a class, unsmoothed MLE yields zero probabilities and can dominate posteriors. Smoothing is essential.

#### FULLY WORKED EXAMPLE (LOG-ODDS FORM FOR PREDICTION)

For binary classification $Y\in\{0,1\}$ with observed feature vector $x$, naive Bayes gives:

$$
\log \frac{p(Y=1\mid x)}{p(Y=0\mid x)}
=
\log \frac{p(Y=1)}{p(Y=0)} + \sum_{i=1}^n \log \frac{p(x_i\mid Y=1)}{p(x_i\mid Y=0)}.
$$

Each feature contributes additively to the log-odds. This is one reason naive Bayes is easy to interpret and debug: you can see which features push toward which label.

#### MISCONCEPTION OR COUNTEREXAMPLE BLOCK

**Misconception: “Naive Bayes assumes the features are independent.”**  
It assumes **conditional** independence given $Y$, not marginal independence. In fact, in naive Bayes the features are often strongly marginally dependent because they share a common cause $Y$ (a fork).

#### CONNECTION TO LATER MATERIAL

Naive Bayes is a baseline that highlights a recurring theme: a wrong model can still be useful if its errors do not destroy the query you care about (here, predicting $Y$). It also connects directly to exponential family models and to discriminative classifiers via its log-odds form.

#### RETAIN / DO NOT CONFUSE

- Retain: naive Bayes is “one parent $Y$, many independent children given $Y$.”
- Do not confuse: conditional independence given $Y$ with unconditional independence.

### 3.5.2 Markov Chains (Sequential Dependence)

#### WHY THIS SUBSECTION EXISTS

For time series and sequences (text, clicks, sensor readings), the defining feature is that the variables are ordered and adjacent variables tend to be more directly related than distant ones. Markov chains are introduced as the simplest BN that captures sequential dependence with a small number of parameters.

#### THE OBJECT BEING INTRODUCED

The object is a BN on a line:

$$
X_1 \to X_2 \to \cdots \to X_T,
$$

where each state depends only on the previous state.

#### FORMAL DEFINITION

A first-order Markov chain asserts:

$$
p(x_1,\dots,x_T) = p(x_1)\,\prod_{t=2}^T p(x_t\mid x_{t-1}).
$$

In a **homogeneous** Markov chain, the conditional $p(x_t\mid x_{t-1})$ does not depend on $t$.

#### INTERPRETATION PARAGRAPH

The Markov property is a conditional independence claim:

$$
X_{t+1:T} \perp X_{1:t-1} \mid X_t.
$$

Once you know the present state, the future is independent of the past. In d-separation language, $X_t$ blocks every path from earlier variables to later variables in the chain.

#### BOUNDARY CONDITIONS / ASSUMPTIONS / FAILURE MODES

1) Real sequences often have long-range dependence that a first-order chain cannot represent.
2) Raising the order (n-grams) increases parameter count rapidly and demands smoothing.

#### FULLY WORKED EXAMPLE (BIGRAM LANGUAGE MODEL AS A BN)

Let $X_t$ be the $t$-th word in a sentence (from a vocabulary of size $d$). A bigram model estimates:

$$
\hat p(x_t \mid x_{t-1}) = \frac{\#(x_{t-1}\to x_t)}{\#(x_{t-1})},
$$

where $\#(x_{t-1}\to x_t)$ counts adjacent occurrences in a corpus.

If $\#(x_{t-1}\to x_t)=0$ for many transitions (which is common), naive MLE makes those transitions impossible, producing brittle models. A simple Dirichlet prior yields smoothing:

$$
\hat p_{\text{MAP}}(x_t \mid x_{t-1})
=
\frac{\#(x_{t-1}\to x_t) + \alpha(x_t)}{\#(x_{t-1}) + \sum_{x'} \alpha(x')}.
$$

Choosing $\alpha(x_t)$ to reflect unigram frequencies is a principled way to encode “common words are more likely as unseen next words than rare words.”

#### MISCONCEPTION OR COUNTEREXAMPLE BLOCK

**Misconception: “A higher-order Markov chain is a fundamentally different model.”**  
It is different in parameters, but not in principle: an n-gram model can be represented as a first-order Markov chain by redefining the state to be the previous $n-1$ tokens. The challenge is computational and statistical: the state space becomes huge.

#### CONNECTION TO LATER MATERIAL

Markov chains lead naturally to hidden Markov models (introducing latent states) and to modern sequence models. They are also a clean setting to practice inference, learning, and smoothing.

#### RETAIN / DO NOT CONFUSE

- Retain: Markov = “future independent of past given present.”
- Do not confuse: “independence” with “no influence.” The present state carries influence from the past; it just summarizes it.

### 3.5.3 Noisy-OR (Many Causes, One Effect, Few Parameters)

#### WHY THIS SUBSECTION EXISTS

BNs are compact when parent sets are small. But sometimes you truly have a variable with many plausible causes (symptom caused by many diseases; system failure caused by many component faults). A full conditional probability table for a binary effect with $k$ binary causes has $2^k$ rows—too large. Noisy-OR is introduced as a **canonical CPD** that captures a common causal pattern with only $k$ (or $k+1$) parameters.

#### THE OBJECT BEING INTRODUCED

The object is a parametric conditional distribution $p(Y\mid X_1,\dots,X_k)$ with binary variables, designed to model “independent causal contributions.”

#### FORMAL DEFINITION

Let $Y\in\{0,1\}$ be an effect and $X_i\in\{0,1\}$ causes. The noisy-OR model uses parameters $\rho_i \in [0,1]$ and sets

$$
p(Y=0\mid X_1,\dots,X_k) = \prod_{i=1}^k \rho_i^{\mathbf{1}[X_i=1]},
$$

so

$$
p(Y=1\mid X_1,\dots,X_k) = 1 - \prod_{i=1}^k \rho_i^{\mathbf{1}[X_i=1]}.
$$

Often a “leak” parameter $\rho_0$ is included to allow $Y=1$ even when all $X_i=0$.

#### INTERPRETATION PARAGRAPH

When $X_i=0$, cause $i$ is “inactive” and contributes nothing to the product. When $X_i=1$, the parameter $\rho_i$ is the probability that cause $i$ fails to trigger the effect. The product means the effect stays off only if **all active causes fail**. This encodes a specific independence assumption: different causes act independently in their attempts to trigger $Y$.

#### BOUNDARY CONDITIONS / ASSUMPTIONS / FAILURE MODES

Noisy-OR is wrong when causes interact synergistically or antagonistically (e.g., two drugs together have a different effect than either alone). In that case the “independent failure” product structure is misspecified.

#### FULLY WORKED EXAMPLE

Let $H$ denote “headache” and causes $C$ (cold), $F$ (flu), $D$ (dehydration), all binary. Choose:

$$
\rho_C=0.2,\quad \rho_F=0.1,\quad \rho_D=0.5.
$$

Then:

- If $(C,F,D)=(0,0,0)$, the product is empty and equals 1, so $p(H=1\mid 0,0,0)=0$ (unless you include a leak).
- If $(1,0,0)$, then $p(H=0\mid 1,0,0)=\rho_C=0.2$, so $p(H=1\mid 1,0,0)=0.8$.
- If $(1,1,0)$, then $p(H=0\mid 1,1,0)=\rho_C\rho_F=0.02$, so $p(H=1\mid 1,1,0)=0.98$.

The probability of headache increases as more causes are active, without enumerating $2^3$ independent parameters.

#### MISCONCEPTION OR COUNTEREXAMPLE BLOCK

**Misconception: “Noisy-OR says causes are independent.”**  
It says the mechanisms by which active causes trigger the effect fail independently. The causes $X_i$ themselves can be statistically dependent in the population.

#### CONNECTION TO LATER MATERIAL

Canonical CPDs like noisy-OR appear in larger models (medical diagnosis, reliability), and they connect directly to parameter tying and to learning with fewer degrees of freedom.

#### RETAIN / DO NOT CONFUSE

- Retain: noisy-OR reduces exponential CPDs to linear parameters by assuming independent triggering failures.
- Do not confuse: independence of causal mechanisms with independence of cause variables.

## 3.6 When (and Only When) Bayesian Networks Support Causal Reasoning

### WHY THIS SECTION EXISTS

Because BNs use directed graphs, it is tempting to interpret arrows causally. Sometimes that interpretation is justified and extremely powerful: it lets you reason about interventions (what happens if we force a variable to a value), not merely observations. But it is also easy to misuse and to reach false conclusions by “reading causality off the arrows.”

This section exists to draw a sharp line between:

- **observational conditioning** ($p(Y\mid X=x)$): learning that $X=x$ happened, and  
- **intervention** ($p(Y\mid do(X=x))$): forcing $X$ to be $x$ by changing the system.

### THE OBJECT BEING INTRODUCED

The object is an **interventional distribution**, typically written using the do-operator:

$$
p(Y \mid do(X=x)).
$$

What is fixed:

- a causal model (a stronger object than an ordinary BN).

What varies:

- which variable you intervene on and what value you force,
- which outcome you care about.

### FORMAL DEFINITION (INTERVENTION AS MECHANISM REPLACEMENT)

In a causal BN interpretation, each node $X_i$ is generated by a mechanism (a conditional distribution) $p(x_i\mid x_{\mathrm{pa}(i)})$. An intervention $do(X=x)$ means:

- remove the dependence of $X$ on its parents (cut incoming edges to $X$), and  
- replace the conditional $p(x\mid x_{\mathrm{pa}(X)})$ with a degenerate distribution that sets $X=x$ with probability 1.

The resulting modified model defines $p(\cdot\mid do(X=x))$.

### INTERPRETATION PARAGRAPH

Conditioning and intervention both mention “$X=x$,” but they answer different questions.

- Conditioning asks: among worlds where $X=x$ happened naturally, what is the distribution of $Y$?
- Intervention asks: if we make $X=x$ happen, what is the distribution of $Y$?

They differ when $X$ is correlated with $Y$ due to common causes (confounding) or selection effects.

### BOUNDARY CONDITIONS / ASSUMPTIONS / FAILURE MODES

1) A plain BN does not guarantee causality. To interpret a BN causally, you need assumptions such as “the graph is the correct causal DAG” and “all common causes of included variables are either included or handled appropriately.”

2) Hidden confounders can make $p(Y\mid X)$ a misleading estimate of the intervention effect.

### FULLY WORKED EXAMPLE: CONFOUNDING MAKES $p(Y\mid X)$ DIFFER FROM $p(Y\mid do(X))$

Consider three variables:

- $Z$: a confounder (e.g., “health consciousness”),
- $X$: a treatment/action (e.g., “takes a supplement”),
- $Y$: an outcome (e.g., “is healthy later”).

Suppose the true causal graph is:

$$
Z \to X,\qquad Z \to Y,\qquad X \to Y.
$$

**Observation.** If you condition on $X=1$ (people who chose the supplement), you are selecting a group that likely has higher $Z$ than average, which boosts $Y$ regardless of the supplement’s causal effect. Therefore $p(Y\mid X=1)$ can be larger than $p(Y\mid do(X=1))$.

**Intervention.** If you intervene and force $X=1$ uniformly across people, you do not get the same selection on $Z$. The incoming edge $Z\to X$ is cut, so the distribution of $Z$ in the intervened population is the baseline one.

The moral is that $p(Y\mid X)$ answers an observational question; it does not automatically estimate the causal effect.

### MISCONCEPTION OR COUNTEREXAMPLE BLOCK

**Misconception: “If the graph has an arrow $X\to Y$, then $p(Y\mid X)$ is the causal effect.”**  
Even with a true arrow $X\to Y$, confounding paths (like $X\leftarrow Z \to Y$) can bias observational comparisons. You need identification logic (e.g., adjustment) to connect observation to intervention.

### CONNECTION TO LATER MATERIAL

Causal reasoning becomes precise with additional machinery (structural causal models, adjustment criteria, do-calculus). Bayesian networks provide the graph language; causal theory explains when and how interventions can be computed from observational data.

### RETAIN / DO NOT CONFUSE

- Retain: $p(Y\mid X=x)$ (observe) and $p(Y\mid do(X=x))$ (intervene) are different objects.
- Do not confuse: “directed edge” with “causal effect without assumptions.”


# Chapter 3: Bayesian Networks

## Chapter overview

A Bayesian network is a way to describe a joint probability distribution over many random variables without writing the full joint table explicitly. The central idea is simple but powerful: instead of assigning one number to every complete configuration of all variables, we describe how each variable depends only on a small set of other variables. The resulting representation is both mathematical and graphical. Mathematically, it is a factorization of a joint distribution into conditional distributions. Graphically, it is a directed acyclic graph whose edges record which variables are treated as direct inputs to which others.

This chapter matters because high-dimensional probability becomes unmanageable very quickly if we insist on full tabular representations. Even when every variable is binary, a model over $n$ variables has $2^n$ entries. The only way to scale is to exploit structure. Bayesian networks do exactly that: they turn conditional independence assumptions into a compact representation, and they let us reason about how information and dependence move through a system.

The chapter has five jobs. First, it explains what a Bayesian network is and why its factorization is more efficient than an unrestricted joint table. Second, it shows how to read conditional independence from the graph using d-separation. Third, it shows how to estimate the conditional probability tables when the graph is known and the data are complete. Fourth, it studies several important special cases, including naive Bayes, Markov chains, and noisy-OR models. Finally, it gives a forward-looking preview of the distinction between ordinary conditioning and causal intervention.

---

## 3.1 Basic semantics

### Why this section exists

Before we can use Bayesian networks for inference, learning, or modeling, we need a precise answer to a basic question: what does the graph actually mean? A picture with arrows is not yet a probability model. We need to know what object is being represented, how the graph determines a factorization of the joint distribution, what assumptions are being imposed, and how that factorization reduces complexity.

Without this section, the graph would be only a mnemonic. With it, the graph becomes a disciplined way of encoding conditional independence. That is the conceptual bridge from "a collection of variables" to "a usable model."

### The object being introduced

The object of interest is a probability distribution over many random variables,

$$
X = (X_1, X_2, \dots, X_n).
$$

For most of this chapter, we assume the variables are discrete and each $X_i$ takes values in a finite set $\mathcal X_i$. What is fixed is the set of variables and the state space of each variable. What varies are the probabilities assigned to the possible configurations of those variables.

A Bayesian network answers the following modeling question:

> How can we represent the joint distribution $p(X_1,\dots,X_n)$ in a way that uses local conditional distributions instead of one enormous global table?

The graph does not replace the probability distribution. It organizes it. Each node stands for a random variable, and each node is equipped with a conditional distribution given its parent variables. The graph tells us which conditionals are needed and which variables can be omitted from each conditioning set.

### The difficulty with an unrestricted joint distribution

Suppose, for simplicity, that each variable has the same number of possible values, say $|\mathcal X_i| = d$. Then the joint table for $p(X_1,\dots,X_n)$ has $d^n$ entries. Since the probabilities must sum to one, the number of free parameters is

$$
d^n - 1.
$$

This exponential growth is the first major pressure that forces Bayesian networks to appear. The problem is not that probability theory is wrong. The problem is that a correct but unstructured representation becomes unusable as $n$ grows.

### A first step: the chain rule

Before introducing graphs, recall that any joint distribution can always be expanded by repeated conditioning:

$$
p(X_1,\dots,X_n)
=
p(X_1)\,p(X_2\mid X_1)\,p(X_3\mid X_1,X_2)\cdots p(X_n\mid X_1,\dots,X_{n-1}).
$$

This identity is always true. It requires no independence assumptions. It is just the chain rule of probability.

But the chain rule alone does **not** solve the complexity problem. It only rewrites the same joint distribution in a different form. To see that, notice how the number of parameters grows:

- $p(X_1)$ needs $d-1$ free parameters.
- $p(X_2\mid X_1)$ needs $d(d-1)$ free parameters because for each of the $d$ values of $X_1$, we must specify a distribution over $X_2$.
- $p(X_3\mid X_1,X_2)$ needs $d^2(d-1)$ free parameters.
- Continuing this way, the total is

$$
(d-1) + d(d-1) + d^2(d-1) + \cdots + d^{n-1}(d-1)
=
d^n - 1.
$$

So the chain rule changes the shape of the representation, but not its raw complexity.

### Why conditional independence changes everything

The real simplification appears when some of those conditionals do not actually depend on every variable that comes earlier in the ordering. For example, if

$$
p(X_3\mid X_1,X_2) = p(X_3\mid X_2),
$$

then once $X_2$ is known, the value of $X_1$ no longer matters for predicting $X_3$. In probabilistic language, $X_3$ is conditionally independent of $X_1$ given $X_2$.

This is the central idea of Bayesian networks: if the true dependence structure is sparse, we should represent only the dependencies that actually matter.

### Formal definition

A **Bayesian network** for random variables $X_1,\dots,X_n$ consists of:

1. A directed acyclic graph $G = (V,E)$ with one node for each random variable.
2. For each node $i$, a conditional distribution

$$
   p(X_i \mid X_{\mathrm{pa}(i)}),
$$

   where $\mathrm{pa}(i)$ denotes the set of parent nodes of $i$ in the graph.

The joint distribution is then defined by the factorization

$$
p(X_1,\dots,X_n) = \prod_{i=1}^n p(X_i \mid X_{\mathrm{pa}(i)}).
$$

If a node has no parents, its factor is just a marginal distribution $p(X_i)$.

### Interpretation paragraph

This definition says that each variable is modeled locally: to evaluate the probability of a full configuration $x = (x_1,\dots,x_n)$, we multiply one factor per node, and each factor looks only at that node's value and the values of its parents. The graph therefore encodes a claim about which variables are directly relevant to each local prediction.

The first thing to notice is that the graph is not the probability distribution itself. The graph gives the pattern of factorization; the conditional probability tables supply the numerical values.

The second thing to notice is that the graph must be acyclic. If cycles were allowed, the product formula would no longer define a standard feed-forward factorization of the joint distribution.

### Boundary conditions, assumptions, and failure modes

Several assumptions are easy to overlook here.

First, the graph is a **DAG**. Cycles are not allowed. That means there must exist at least one ordering of the variables in which every node appears after its parents.

Second, this chapter mainly uses **discrete variables** so that local factors can be written as conditional probability tables. Bayesian networks also exist for continuous variables, but the parameterization is then different.

Third, an edge means "appears as a direct input in the factorization," not automatically "causes." Causal interpretation requires extra assumptions that are not yet part of the definition.

Fourth, the factorization implied by the graph guarantees some conditional independencies, but a particular numerical parameter choice can create additional accidental independencies that are not structurally forced by the graph. The graph tells us what must hold for every distribution that factors that way, not everything that happens to hold for one special parameter setting.

Finally, the compactness of the representation depends on the parent sets being small. If one node has many parents, its conditional probability table can still become exponentially large in the number of parents.

### Fully worked example: the burglar alarm network

Consider five binary variables:

- $B \in \{0,1\}$: burglary
- $E \in \{0,1\}$: earthquake
- $A \in \{0,1\}$: alarm
- $W \in \{0,1\}$: Watson calls
- $H \in \{0,1\}$: Hudson calls

The qualitative assumptions are:

- burglaries and earthquakes are independent root causes;
- either can trigger the alarm;
- Watson's call depends only on whether the alarm is sounding;
- Hudson's call also depends only on whether the alarm is sounding.

Those assumptions lead to the graph

$$
B \to A \leftarrow E,\qquad A \to W,\qquad A \to H.
$$

So the joint distribution factors as

$$
p(B,E,A,W,H)
=
p(B)\,p(E)\,p(A\mid B,E)\,p(W\mid A)\,p(H\mid A).
$$

Now specify the local probabilities.

For burglary:
| $B$ | 0 | 1 |
|---|---:|---:|
| $p(B)$ | 0.999 | 0.001 |

For earthquake:
| $E$ | 0 | 1 |
|---|---:|---:|
| $p(E)$ | 0.998 | 0.002 |

For Watson's call:
| $A$ | $W=0$ | $W=1$ |
|---|---:|---:|
| 0 | 0.95 | 0.05 |
| 1 | 0.10 | 0.90 |

For Hudson's call:
| $A$ | $H=0$ | $H=1$ |
|---|---:|---:|
| 0 | 0.99 | 0.01 |
| 1 | 0.30 | 0.70 |

For the alarm:
| $B,E$ | $A=0$ | $A=1$ |
|---|---:|---:|
| 0,0 | 0.999 | 0.001 |
| 0,1 | 0.25 | 0.75 |
| 1,0 | 0.05 | 0.95 |
| 1,1 | 0.02 | 0.98 |

Now compute one joint probability:

$$
p(B=0,E=1,A=1,W=1,H=0).
$$

The graph tells us exactly which factors to multiply. We check each variable in the order prescribed by the factorization:

1. For $B=0$, the needed factor is $p(B=0)=0.999$.
2. For $E=1$, the needed factor is $p(E=1)=0.002$.
3. For $A=1$ given $B=0,E=1$, the needed factor is $p(A=1\mid B=0,E=1)=0.75$.
4. For $W=1$ given $A=1$, the needed factor is $p(W=1\mid A=1)=0.90$.
5. For $H=0$ given $A=1$, the needed factor is $p(H=0\mid A=1)=0.30$.

Multiplying,

$$
0.999 \times 0.002 \times 0.75 \times 0.90 \times 0.30 \approx 0.0004046.
$$

Each step uses only one local table lookup. We never needed the full $2^5 = 32$-entry joint table explicitly.

Now check the representation size. A full joint distribution over five binary variables needs $2^5 - 1 = 31$ free parameters. By contrast, this Bayesian network uses:

- $1$ parameter for $p(B)$,
- $1$ parameter for $p(E)$,
- $4$ parameters for $p(A\mid B,E)$,
- $2$ parameters for $p(W\mid A)$,
- $2$ parameters for $p(H\mid A)$.

That is only $10$ independent values. The savings come entirely from the independence assumptions encoded by the graph.

### Misconception or counterexample block

**Do not confuse "factorized representation" with "approximation."**  
If the graph and local tables are chosen so that their product equals the true joint distribution, then the Bayesian network is an exact representation of that distribution. The compactness does not automatically mean approximation. The approximation enters only if the independence assumptions are not actually true for the system being modeled.

**Do not confuse "missing edge" with "no relationship at all."**  
If there is no edge between two variables, they may still be dependent through indirect paths. In the burglar alarm network, $W$ and $H$ have no direct edge, but they are dependent because both are influenced by $A$.

**Do not confuse edges with causality.**  
In this example the causal reading is natural, but the mathematical definition of a Bayesian network does not require that interpretation.

### Connection to later material

This section gives the semantic foundation for everything that follows. Once we know how the joint distribution is built from local factors, we can ask three deeper questions:

1. Which conditional independencies are implied by the graph?
2. How can we estimate the local factors from data?
3. How can we exploit special graph structures, such as classifier models or sequential models?

Those are exactly the next steps in the chapter.

### Retain / do not confuse

Retain these points:

- A Bayesian network is a DAG plus one conditional distribution per node.
- The joint distribution factors as a product of local conditionals.
- The compactness comes from conditional independence, not from the chain rule alone.
- Parent sets determine which variables each local factor may depend on.

Do not confuse these points:

- Missing edge $\neq$ unconditional independence.
- Edge $\neq$ automatic causal claim.
- Chain-rule factorization $\neq$ compact representation unless conditional independencies simplify the factors.

---

## 3.1.1 Graph terminology

### Why this subsection exists

Once the graph has semantic meaning, we need a precise vocabulary for talking about local and global graph structure. Terms like parent, child, ancestor, and descendant are not decorative. They are the language in which factorization, independence, and later algorithms are all expressed.

### The object being introduced

The new objects are graph-theoretic relations among nodes in the DAG. These relations tell us which variables are directly connected, which are upstream causes or informational predecessors, and which lie downstream.

### Formal definitions

For a node $i$:

- The **parents** of $i$, denoted $\mathrm{pa}(i)$, are the nodes $j$ such that $j \to i$.
- The **children** of $i$ are the nodes $c$ such that $i \to c$.
- A **root** is a node with no parents.
- A **leaf** is a node with no children.
- The **ancestors** of $i$, denoted $\mathrm{an}(i)$, are all nodes from which there is a directed path to $i$.
- The **descendants** of $i$, denoted $\mathrm{de}(i)$, are all nodes reachable by a directed path starting at $i$.

An **undirected path** is any sequence of nodes connected by edges if we ignore arrow direction.

### Interpretation paragraph

Parents are the variables that appear directly in a node's factor. Ancestors are the variables that can influence that node through some directed chain. Descendants are the variables that can be influenced by it. Undirected paths matter because information flow for independence reasoning is not restricted to following arrows only; what matters is whether a path becomes active or blocked under conditioning.

### Fully worked example

Return to the burglar alarm graph:

$$
B \to A \leftarrow E,\qquad A \to W,\qquad A \to H.
$$

Check the structural roles one by one.

- $B$ has no parents, so $B$ is a root.
- $E$ also has no parents, so $E$ is a root.
- $W$ has no children, so $W$ is a leaf.
- $H$ has no children, so $H$ is a leaf.

Now find descendants of $B$. Starting at $B$, there is a directed edge to $A$, and from $A$ directed edges to $W$ and $H$. Therefore

$$
\mathrm{de}(B) = \{A,W,H\}.
$$

Now find ancestors of $W$. The directed paths ending at $W$ come from $A$, and upstream of $A$ from both $B$ and $E$. Therefore

$$
\mathrm{an}(W) = \{A,B,E\}.
$$

Finally, note two different notions of path:

- $B \to A \to H$ is both a directed path and an undirected path.
- $B \to A \leftarrow E$ is an undirected path from $B$ to $E$, but it is not a directed path because the arrows do not all point in the same travel direction.

This distinction becomes crucial for d-separation.

### Misconception block

**Do not confuse ancestors with parents.**  
Every parent is an ancestor, but not every ancestor is a parent. In the burglar alarm network, $B$ is an ancestor of $W$ but not a parent of $W$.

**Do not ignore undirected paths when reasoning about dependence.**  
Dependence can be transmitted along paths whose arrows do not all point in one direction.

### Connection to later material

The terms introduced here will be used repeatedly in d-separation, in causal reasoning, and in algorithms that traverse the graph to perform inference or learning.

### Retain / do not confuse

Retain:

- parents are direct inputs;
- ancestors and descendants are multi-step directed relations;
- undirected paths matter for independence.

Do not confuse:

- root with leaf;
- parent with ancestor;
- directed path with undirected path.

---

## 3.1.2 Why the expansion order matters

### Why this subsection exists

The chain rule lets us factor any joint distribution in any ordering of the variables. But different orderings expose different conditional independencies. Since the efficiency of a Bayesian network depends on those simplifications, the order used to build the factorization can make a major difference.

### The object being introduced

The object here is not a new probability model but a modeling choice: the order in which we expand the joint distribution. What is fixed is the underlying joint distribution. What varies is the conditional expansion and therefore the resulting graph and parameter count.

### Interpretation before formula

A good ordering places likely causes before their effects. In that case, many variables can often be conditioned on a small, natural parent set. A poor ordering forces us to condition on observations that are only indirectly informative, and the resulting conditionals often fail to simplify.

### Worked comparison using the alarm example

Using the natural order

$$
B, E, A, W, H,
$$

the factorization is

$$
p(B,E,A,W,H)=p(B)\,p(E)\,p(A\mid B,E)\,p(W\mid A)\,p(H\mid A).
$$

This is compact. The parent sets are small and intuitive.

Now reverse the perspective and consider the order

$$
H, W, A, B, E.
$$

The chain rule gives

$$
p(B,E,A,W,H)=p(H)\,p(W\mid H)\,p(A\mid H,W)\,p(B\mid A,W,H)\,p(E\mid A,B,W,H).
$$

Now ask, step by step, which factors simplify.

1. Does $p(W\mid H)$ simplify to $p(W)$?  
   No. If Hudson calls, that makes the alarm more likely, which in turn makes Watson's call more likely. So $W$ and $H$ are not marginally independent.

2. Does $p(A\mid H,W)$ simplify to a function of only one of those variables?  
   No. If both neighbors call, that is stronger evidence for the alarm than if only one calls. So both $H$ and $W$ matter.

3. Does $p(B\mid A,W,H)$ simplify?  
   Yes. Once the alarm state $A$ is known, the calls $W$ and $H$ add no further information about burglary. So this reduces to $p(B\mid A)$.

4. Does $p(E\mid A,B,W,H)$ simplify?  
   Yes. Once $A$ and $B$ are known, the calls still add no further information about earthquake, so this reduces to $p(E\mid A,B)$.

So the resulting factorization becomes

$$
p(B,E,A,W,H)=p(H)\,p(W\mid H)\,p(A\mid H,W)\,p(B\mid A)\,p(E\mid A,B).
$$

This representation is valid, but it is less compact. In the source chapter, the natural ordering needs $10$ parameters, while this alternative ordering needs $13$.

The general lesson is not that one ordering is universally correct. The lesson is that order affects which conditional independencies are easy to express. Causal orderings often, though not always, align well with sparse factorization.

### Boundary conditions and failure modes

A change of ordering does not change the underlying joint distribution if the factors are chosen consistently. What it changes is the form of the factorization and the visible local independencies.

Some orderings are so poor that no simplification occurs at all. In that case the graph becomes complete with respect to predecessors: each variable depends on all earlier ones, and the Bayesian network loses its practical advantage.

### Misconception block

**Do not think the graph is unique for a distribution.**  
The same joint distribution can usually be represented by many different Bayesian networks.

**Do not assume a more complicated graph means a different underlying probability law.**  
Sometimes it is just a less efficient factorization of the same law.

### Connection to later material

This subsection prepares the ground for the later discussion of equivalent graphs and structure learning. If many graphs can represent the same distributional information, then choosing a graph from data becomes a subtler problem than merely looking for the best fit.

### Retain / do not confuse

Retain:

- the chain rule allows many orderings;
- ordering affects which local conditionals simplify;
- causal orderings often yield smaller parent sets.

Do not confuse:

- different factorization with different underlying distribution;
- compactness with correctness.

---

## 3.1.3 Observations and influence

### Why this subsection exists

A Bayesian network is not only a compact representation. It also supports reasoning about how evidence changes beliefs. To prepare for formal independence analysis, we need an intuitive picture of how observation at one node influences probabilities elsewhere in the graph.

### The object being introduced

The object here is belief update under observation. What is fixed is the graph and the local conditional tables. What varies is the set of observed variables and the resulting posterior probabilities of unobserved variables.

### Interpretation paragraph

If one variable directly influences another in the graph, then observing the downstream variable often changes our belief about the upstream variable, and vice versa. But this influence is not unrestricted. Sometimes it propagates, sometimes it is blocked, and sometimes observing a variable can create a dependence that was absent before. The next section formalizes exactly when each of those cases occurs.

### Fully worked example

In the alarm model, the marginal probability of an earthquake is easy to read off:

$$
p(E=1)=0.002.
$$

The marginal probability that the alarm is on, $p(A=1)$, is larger than either root probability because it can be triggered by burglary or earthquake. It can be computed by summing over the four $(B,E)$ configurations.

Now suppose Watson calls, so we observe $W=1$.

Check the implications in order:

1. $W$ depends directly on $A$.  
   Since $p(W=1\mid A=1)=0.9$ and $p(W=1\mid A=0)=0.05$, observing $W=1$ makes $A=1$ more plausible.

2. $A$ depends on both $B$ and $E$.  
   If $A=1$ becomes more plausible, then both burglary and earthquake become more plausible than before.

3. Therefore observing an effect can raise the posterior probability of its possible causes.  
   In the source text, $p(E=1\mid W=1)$ is much larger than the prior $p(E=1)$.

This is not yet the full theory of independence, but it gives the right intuition: evidence propagates along graph structure. The next section explains when that propagation is active and when it is blocked.

### Misconception block

**Do not think arrows only transmit influence in the arrow direction.**  
In probabilistic inference, observing an effect can change beliefs about its causes. The arrow direction describes factorization, not one-way information flow under conditioning.

### Connection to later material

This intuition is the bridge to d-separation. The next section turns the informal idea of "influence moving through the graph" into a precise graph criterion for conditional independence.

### Retain / do not confuse

Retain:

- observations can change beliefs both downstream and upstream;
- graph structure controls which updates are possible.

Do not confuse:

- arrow direction with the direction of posterior influence.

---

## 3.2 Independence relations

### Why this section exists

Once a Bayesian network has been built, one of its greatest advantages is that we can often read off independence relationships directly from the graph without computing probabilities numerically. That is enormously valuable. It tells us which variables matter for which predictions, which observations are redundant once other variables are known, and which structures can be simplified or learned from data.

But to do that correctly, we need a precise graphical criterion. That criterion is d-separation.

### The object being introduced

The key object is an **active path** given a set of observed variables. An active path is a path along which probabilistic dependence can still pass once we condition on the evidence. If every path between two sets of variables is blocked, then those sets are conditionally independent given the evidence.

What is fixed is the graph and the evidence set $E$. What varies is the status of each path: active or inactive.

### Three local path patterns to understand first

Before stating the formal definition, it helps to isolate the three local path motifs that can occur at an interior node on a path.

#### 1. Chain

$$
X \to Z \to Y
\quad\text{or}\quad
X \leftarrow Z \leftarrow Y
$$

Here $Z$ lies on a transmitting chain between $X$ and $Y$. If $Z$ is unobserved, the path can remain active. If $Z$ is observed, the path is blocked.

#### 2. Fork

$$
X \leftarrow Z \to Y
$$

Here $Z$ is a common cause of $X$ and $Y$. Again, if $Z$ is unobserved, the path can remain active. If $Z$ is observed, the path is blocked because conditioning on the common cause explains away the dependence.

#### 3. Collider

$$
X \to Z \leftarrow Y
$$

Here $Z$ is a common effect. This case is the opposite of the first two. If neither $Z$ nor any descendant of $Z$ is observed, the path is blocked. If $Z$ itself is observed, or any descendant of $Z$ is observed, the path becomes active.

That last rule is the one most readers initially find counterintuitive. It is also the most important one to master.

### Formal definition

Let $G$ be a Bayesian network graph, and let $E$ be a set of observed nodes. An undirected path

$$
i_1 - i_2 - \cdots - i_L
$$

is **active given $E$** if for every interior node $i_\ell$ on the path, one of the following holds:

1. If the local pattern at $i_\ell$ is a collider,

$$
   i_{\ell-1} \to i_\ell \leftarrow i_{\ell+1},
$$

   then either $i_\ell \in E$ or some descendant of $i_\ell$ is in $E$.

2. If the local pattern at $i_\ell$ is not a collider, then $i_\ell \notin E$.

Given disjoint node sets $A$, $B$, and $E$, we say that $A$ and $B$ are **d-separated by $E$** if there is no active path between any node in $A$ and any node in $B$ given $E$.

### Interpretation paragraph

D-separation is a purely graphical test. It does not require plugging in numerical probabilities. It asks: after we account for the observed variables, is there any path left along which dependence could in principle flow?

The collider rule deserves special emphasis. A collider blocks a path by default. Observing it opens the path. This is the opposite of what happens with chains and forks, where observing the middle node blocks the path. That contrast is the heart of d-separation.

### What d-separation guarantees

If $A$ and $B$ are d-separated by $E$ in a Bayesian network graph $G$, then for **every** probability distribution that factors according to $G$,

$$
X_A \perp X_B \mid X_E.
$$

This is a guarantee from graph structure alone.

The converse must be stated carefully. If $A$ and $B$ are **not** d-separated by $E$, then the graph does not guarantee independence. In fact, there exists at least one distribution consistent with the graph in which $X_A$ and $X_B$ are dependent given $X_E$. However, a special parameter choice can sometimes create accidental independence even when the graph does not force it. So d-separation captures structural independencies, not every numerical coincidence.

### Boundary conditions, assumptions, and failure modes

A few boundaries matter here.

First, d-separation is about the graph of a Bayesian network, so the factorization assumptions of the Bayesian network must hold.

Second, d-separation gives independencies that are true for all parameterizations compatible with the graph. It does not say that every dependence suggested by an active path must show up numerically in every parameter choice.

Third, when checking whether a path is active, every interior node on the path must be examined. A single blocking node makes the whole path inactive.

Fourth, if there are multiple paths between two variables, one active path is enough to make the variables not d-separated. To establish d-separation, every path must be blocked.

### Fully worked example: d-separation in the alarm network

Use the graph

$$
B \to A \leftarrow E,\qquad A \to W,\qquad A \to H.
$$

#### Example 1: Are $B$ and $E$ independent with no observations?

The only path between $B$ and $E$ is

$$
B \to A \leftarrow E.
$$

The middle node $A$ is a collider. No node is observed, and no descendant of $A$ is observed either. Therefore the path is blocked. Since there is no other path, $B$ and $E$ are d-separated given the empty evidence set.

Conclusion:

$$
B \perp E.
$$

#### Example 2: Are $B$ and $E$ independent given $A$?

The same path still connects them:

$$
B \to A \leftarrow E.
$$

Now $A$ is observed. Since $A$ is a collider and it is observed, the path becomes active.

Conclusion:

$$
B \not\!\perp E \mid A.
$$

This is the classic "explaining away" effect. If we learn that the alarm has sounded, then evidence for one cause makes the other cause less necessary, so the two causes become dependent conditional on the effect.

#### Example 3: Are $W$ and $H$ independent with no observations?

The path is

$$
W \leftarrow A \to H.
$$

This is a fork. The middle node $A$ is unobserved, so the path is active. Therefore $W$ and $H$ are not marginally independent.

Conclusion:

$$
W \not\!\perp H.
$$

#### Example 4: Are $W$ and $H$ independent given $A$?

The same path is a fork through $A$, but now $A$ is observed. Observing the middle node in a fork blocks the path.

Conclusion:

$$
W \perp H \mid A.
$$

#### Example 5: Are $E$ and $W$ independent given $A$?

The path is

$$
E \to A \to W.
$$

This is a chain through $A$. Once $A$ is observed, the chain is blocked.

Conclusion:

$$
E \perp W \mid A.
$$

The pattern is worth retaining: once the alarm state is known, Watson's call carries no extra information about earthquake.

### A larger worked example: checking several paths

Suppose we have a larger graph in which there are several undirected paths between two nodes $B$ and $E$. To decide whether $B$ and $E$ are d-separated given some evidence set, we do not try to reason globally all at once. Instead we check each path one by one and ask whether some interior node blocks it.

The procedure is conceptually simple:

1. List a path from $B$ to $E$.
2. For each interior node on that path, decide whether it is acting as a collider or non-collider along that particular path.
3. Check whether the observed set opens or blocks that node.
4. If any interior node blocks the path, the whole path is inactive.
5. Repeat for the remaining paths.
6. If every path is inactive, then the variables are d-separated.
7. If even one path remains active, they are not d-separated.

This path-by-path discipline matters because the same node can behave differently on different paths depending on local arrow orientation.

### Misconception or counterexample block

**Most important misconception: observing a collider opens a path.**  
Many readers initially expect observation always to block dependence. That is false. In

$$
X \to Z \leftarrow Y,
$$

the path between $X$ and $Y$ is blocked when $Z$ is unobserved, and opened when $Z$ or a descendant of $Z$ is observed.

**Do not forget descendants of colliders.**  
Even if the collider itself is not observed, observing one of its descendants can activate the path. That detail is easy to miss and often changes the answer.

**Zero covariance is not the same as conditional independence.**  
D-separation is a statement about conditional independence structure, not about one particular summary statistic such as covariance.

### Connection to later material

D-separation is one of the foundational tools of graphical models. It lets us answer independence questions graphically, motivates algorithms for probabilistic inference, and underlies structure learning and causal reasoning. If this section is not mastered, later topics tend to feel like disconnected rules. If it is mastered, much of the later theory becomes a direct extension of one clear principle: dependence moves only along active paths.

### Retain / do not confuse

Retain:

- chain and fork are blocked by observing the middle node;
- collider is blocked by default and opened by observing the collider or its descendant;
- d-separation means every path is blocked.

Do not confuse:

- active path with directed path;
- graphical non-separation with guaranteed dependence in every parameterization;
- observed collider with observed chain or fork.

---

## 3.2.1 Equivalent graphs

### Why this subsection exists

If d-separation tells us what independencies a graph implies, the next natural question is whether two different graphs can imply exactly the same independencies. The answer is yes. This matters because it limits what we can learn from purely observational data.

### The object being introduced

The object here is **independence equivalence**, also called **Markov equivalence**. What is fixed is the set of variables and the collection of conditional independence relations. What varies is the graph used to encode them.

### Formal definition

Two Bayesian network graphs are **Markov equivalent** if they encode exactly the same set of independence and conditional independence relations.

### Interpretation paragraph

Markov equivalent graphs may look different as directed graphs, but they are indistinguishable if all we are allowed to inspect is the independence structure of the distributions they represent. In other words, the graphs differ in factorization form, but not in the set of distributional constraints implied by d-separation.

There is also a very useful structural characterization to retain because it tells you exactly what data (in the idealized infinite-data limit, with perfect independence tests) can and cannot determine:

- Markov equivalent DAGs have the same **skeleton**, meaning the same underlying undirected edges when you ignore arrow directions.
- Markov equivalent DAGs have the same set of **v-structures** (colliders) of the form $X \to Z \leftarrow Y$ in which $X$ and $Y$ are not adjacent.

This is why colliders are special. Ordinary chains and forks can often be reoriented without changing the implied independencies, but a v-structure changes which pairs are marginally independent and which become dependent after conditioning.

### Fully worked example

Consider three variables $A,B,C$.

The following three graphs are Markov equivalent:

1. $A \to B \to C$
2. $A \leftarrow B \leftarrow C$
3. $A \leftarrow B \to C$

In each graph, the key structural statement is the same:

$$
A \perp C \mid B,
$$

and there is no marginal independence between $A$ and $C$.

Now compare them with the collider graph

$$
A \to B \leftarrow C.
$$

This graph is different. Here the path between $A$ and $C$ goes through a collider, so

$$
A \perp C
$$

marginally, but

$$
A \not\!\perp C \mid B.
$$

So the collider graph is **not** Markov equivalent to the previous three.

This example illustrates an important structural lesson: colliders change independence patterns in a way that cannot be reproduced by simply reversing ordinary chain or fork edges.

### Boundary conditions and failure modes

Markov equivalence is about independence structure, not about causal meaning. Two equivalent graphs can support exactly the same observational distributions even if their arrows suggest different stories.

This means that observational data alone cannot always identify edge directions. If two graphs are Markov equivalent, then any distribution representable by one is also representable by the other, with suitable conditional tables.

### Misconception block

**Do not infer causal direction from observational fit alone.**  
If $A \to B$ and $B \to A$ are Markov equivalent in a two-variable system, then data showing that $A$ and $B$ are associated do not tell us which one causes the other.

**Do not think a unique best-scoring graph from finite data automatically reveals the true mechanism.**  
Often multiple graphs fit nearly equally well because they belong to the same equivalence class.

### Connection to later material

This subsection prepares directly for structure learning and causal inference. In structure learning, Markov equivalence explains why the graph cannot always be recovered uniquely from data. In causal reasoning, it explains why extra assumptions or interventions are needed to orient edges reliably.

### Retain / do not confuse

Retain:

- different DAGs can encode the same independence structure;
- collider patterns are especially important for distinguishing equivalence classes.

Do not confuse:

- different arrow directions with different observational implications in every case;
- Markov equivalence with causal equivalence.

---

## 3.2.2 Markov blankets

### Why this subsection exists

D-separation is the general tool: it answers arbitrary conditional independence questions by analyzing paths. But in practice, we often need a *local* answer to a recurring question:

> If I want to predict or update beliefs about one variable $X_i$, what is the smallest set of variables I must look at?

This question arises in inference algorithms, in sampling methods, and in model debugging. The answer is the Markov blanket: a minimal “shield” around a node that screens it off from the rest of the network.

### The object being introduced

The object is a set of nodes associated with a target node $i$, denoted $\mathrm{MB}(i)$, with the property that once we condition on those nodes, $X_i$ becomes independent of every other variable in the model.

What is fixed is the graph and the choice of the target node $i$. What varies is the evidence: conditioning on the blanket has a special role because it blocks every path from $i$ to the outside.

### Formal definition

Let $G$ be a Bayesian network graph. The **Markov blanket** of node $i$ is the set

$$
\mathrm{MB}(i)
=
\mathrm{pa}(i)
\;\cup\;
\mathrm{ch}(i)
\;\cup\;
\bigcup_{c \in \mathrm{ch}(i)} \Bigl(\mathrm{pa}(c)\setminus\{i\}\Bigr),
$$

that is:

- the parents of $i$,
- the children of $i$,
- and the other parents of $i$'s children (often called co-parents or “spouses”).

### Interpretation paragraph

Each of these groups is forced on us by d-separation logic.

- Parents matter because the factorization tells us $X_i$ is generated conditional on its parents.
- Children matter because they carry information about $X_i$: observing a child updates beliefs about the parent.
- Co-parents matter because conditioning on a child can open a collider path between $X_i$ and the child’s other parent(s). If you omit co-parents, you can mistakenly think you have screened off $X_i$ when you have not.

The blanket is “minimal” in the sense that every path from $i$ to a node outside the blanket must pass through the blanket in a way that becomes blocked once the blanket is observed.

### Boundary conditions, assumptions, and failure modes

The Markov blanket statement is a structural one: it is guaranteed for every distribution that factors according to the BN.

However, it does not say that conditioning on $\mathrm{MB}(i)$ makes $X_i$ numerically independent of the outside for *every* parameterization in a way you can detect with small samples. It says the conditional independence holds as a distributional identity.

Also, remember that “blanket” is a probabilistic statement, not a causal one. It does not mean these variables are the only *causes* of $X_i$. It means they are the only variables that matter once you condition appropriately.

### Fully worked example: the Markov blanket in the burglar alarm network

Use the burglar network

$$
B \to A \leftarrow E,\qquad A \to W,\qquad A \to H.
$$

Consider the blanket of the alarm $A$.

- $\mathrm{pa}(A)=\{B,E\}$.
- $\mathrm{ch}(A)=\{W,H\}$.
- The children $W$ and $H$ have no other parents besides $A$, so there are no co-parents to add.

Therefore

$$
\mathrm{MB}(A)=\{B,E,W,H\}.
$$

The Markov blanket claim is:

$$
A \perp \{ \text{every other variable} \} \mid (B,E,W,H).
$$

In this tiny model there are no other variables, so the statement is trivial, but the structure is the point: if this network were embedded in a much larger model, conditioning on burglary, earthquake, and the two calls would screen the alarm off from everything else.

Now consider the blanket of $B$ (burglary).

- $\mathrm{pa}(B)=\varnothing$.
- $\mathrm{ch}(B)=\{A\}$.
- The other parent of $A$ is $E$, so $E$ is a co-parent of $B$ through child $A$.

Therefore

$$
\mathrm{MB}(B)=\{A,E\}.
$$

This is a good place to see why co-parents are required. If you condition on the child $A$ alone, you open the collider structure $B \to A \leftarrow E$, which makes $B$ and $E$ dependent given $A$. The blanket includes $E$ because once you condition on both $A$ and $E$, you have “accounted for” the alternative explanation of $A$, and the remaining paths from $B$ to the rest of the graph are blocked.

### Misconception block

**Do not confuse the Markov blanket with “neighbors in the undirected graph.”**  
The blanket is not just “everything adjacent.” It has a specific composition (parents, children, co-parents) because those are the nodes that can keep paths active after conditioning.

**Do not confuse Markov blanket with causal parents.**  
Blanket membership is about probabilistic screening-off, not causal ancestry.

### Connection to later material

The Markov blanket is the key locality principle used by many inference procedures. For example, in Gibbs sampling, the conditional distribution of a node given all others depends only on its Markov blanket. In structure learning, blanket ideas can be used to narrow candidate dependencies.

### Retain / do not confuse

Retain:

- $\mathrm{MB}(i)$ is “parents + children + co-parents”;
- conditioning on the blanket screens the node off from the rest.

Do not confuse:

- probabilistic screening with causal explanation.

---

## 3.2.3 Inference queries: how a Bayesian network answers questions

### Why this subsection exists

So far we have used Bayesian networks to (i) represent a joint distribution compactly and (ii) read off conditional independence relationships from the graph. But the most common reason to build a Bayesian network is more direct:

> We want to compute probabilities of interest given observations.

For example, in the burglary network we want $P(B=1\mid W=1)$: how likely is a burglary if Watson calls? This subsection exists to connect the representation to the basic inference operation and to make clear where the computational difficulty lives.

### The object being introduced

The object is an **inference query** of the form

$$
p(X_Q \mid X_E = x_E),
$$

where:

- $Q$ is a set of query variables whose distribution we want,
- $E$ is a set of evidence variables we have observed (with values $x_E$),
- and the remaining variables $H$ are hidden and must be summed (or integrated) out.

What is fixed is the model $p$ (equivalently, the BN structure and its CPDs). What varies is the evidence $x_E$ and the query set $Q$.

### Formal definition

For a discrete model, the fundamental identity is:

$$
p(x_Q \mid x_E)
=
\frac{\sum_{x_H} p(x_Q, x_H, x_E)}{\sum_{x_Q}\sum_{x_H} p(x_Q, x_H, x_E)}.
$$

The Bayesian network factorization tells us how to compute $p(x_Q, x_H, x_E)$ as a product of local conditionals, but the summation over $x_H$ can still be exponentially large if done naively.

### Interpretation paragraph

This formula says: collect all full assignments consistent with the evidence, add up their joint probabilities, and renormalize. The BN does not eliminate the need to sum over hidden variables. What it does is factor the joint probability into small pieces so that algorithms can reuse partial computations.

In other words: **Bayesian networks turn inference into a structured sum-product problem.**

### Boundary conditions, assumptions, and failure modes

Even with a sparse Bayesian network, exact inference can be computationally hard. The worst-case cost depends not on the number of nodes alone, but on how the graph “fills in” when you eliminate hidden variables (a phenomenon later captured by treewidth).

So the right mental model is:

- BNs make inference *possible to express cleanly*.
- They often make it *possible to compute efficiently* when the graph has favorable structure (trees, polytrees, small treewidth).
- But they do not guarantee tractability in every graph.

### Fully worked example: writing $P(B\mid W=1)$ in the burglar network

We will not compute a final number here; the goal is to practice translating a question into the correct sum-product expression and simplifying legally.

**Step 1: identify query, evidence, and hidden variables.**

- Query: $Q=\{B\}$.
- Evidence: $E=\{W\}$ with observed value $W=1$.
- Hidden variables: $H=\{E,A,H\}$ (earthquake, alarm, Hudson call).

**Step 2: write the posterior as “joint over evidence, summed over hidden, normalized.”**

$$
P(B=b\mid W=1)
=
\frac{\sum_{e,a,h} P(B=b,E=e,A=a,W=1,H=h)}{\sum_{b'}\sum_{e,a,h} P(B=b',E=e,A=a,W=1,H=h)}.
$$

**Step 3: expand the joint using the BN factorization.**

The model factorizes as

$$
P(b,e,a,w,h)=P(b)\,P(e)\,P(a\mid b,e)\,P(w\mid a)\,P(h\mid a).
$$

Plugging $w=1$,

$$
P(B=b\mid W=1)
=
\frac{\sum_{e,a,h} P(b)\,P(e)\,P(a\mid b,e)\,P(W=1\mid a)\,P(h\mid a)}{\sum_{b'}\sum_{e,a,h} P(b')\,P(e)\,P(a\mid b',e)\,P(W=1\mid a)\,P(h\mid a)}.
$$

**Step 4: simplify by summing out a factor that normalizes.**

Because $P(h\mid a)$ is a conditional distribution over $h$, we always have

$$
\sum_h P(h\mid a) = 1.
$$

So the sum over $h$ disappears, leaving a sum only over $e$ and $a$.

This step illustrates the general pattern: inference is hard when hidden variables connect many factors, and easy when you can sum out a variable locally without creating large intermediate dependencies.

### Misconception block

**Do not think inference is “just Bayes’ rule.”**  
Bayes’ rule is correct, but in multi-variable models the hard part is computing the normalizing constant and managing the sum over hidden variables. Graph structure exists to make that manageable, not to avoid it entirely.

### Connection to later material

This subsection is a bridge to inference algorithms. Variable elimination and belief propagation are systematic ways to perform the sums in the definition of $p(x_Q\mid x_E)$ without enumerating every hidden configuration. Approximate inference methods (sampling, variational inference) become necessary when the graph structure makes exact inference too expensive.

### Retain / do not confuse

Retain:

- inference is “sum out hidden variables, then normalize”;
- the BN factorization turns the joint into a product of small factors.

Do not confuse:

- observation (conditioning) with intervention (changing the model mechanism);
- compact representation with guaranteed tractable inference in every graph.

---

## 3.3 Learning from complete data

### Why this section exists

So far the graph and the conditional probabilities have been treated as given. In practice, the numerical parameters are rarely known in advance. We observe data and need to estimate those local conditional distributions.

This section fills that gap. It shows how the structure of a Bayesian network makes parameter learning simple when the graph is known and every variable is observed in every data point.

### The object being introduced

The object is a parameterized Bayesian network together with a complete dataset

$$
D = \{x^{(1)}, x^{(2)}, \dots, x^{(m)}\}.
$$

Here:

- $m$ is the number of data points;
- each data point $x^{(j)}$ contains one observed value for every variable $X_1,\dots,X_n$;
- the graph structure is fixed and known;
- the unknowns are the entries of the conditional probability tables.

The question is:

> Given a known DAG and complete observations, how do we estimate each local conditional distribution?

### Formal parameterization

For each node $i$, each state $x_i$, and each parent configuration $x_{\mathrm{pa}(i)}$, define a parameter

$$
\rho_{i,x_i,x_{\mathrm{pa}(i)}} = p(X_i = x_i \mid X_{\mathrm{pa}(i)} = x_{\mathrm{pa}(i)}).
$$

These parameters must satisfy the usual probability constraints. For each fixed node $i$ and each fixed parent configuration $x_{\mathrm{pa}(i)}$,

$$
\sum_{x_i} \rho_{i,x_i,x_{\mathrm{pa}(i)}} = 1,
\qquad
\rho_{i,x_i,x_{\mathrm{pa}(i)}} \ge 0.
$$

### Interpretation paragraph

Each row of a conditional probability table is a separate discrete distribution. The parent configuration is fixed within that row, and the child variable value is what varies across the entries. Learning the full Bayesian network therefore amounts to learning one multinomial distribution for each row of each node's CPT.

The structure of the graph is what makes this manageable. It breaks a large joint estimation problem into many small local ones.

### The log-likelihood and why it decomposes

The likelihood of the dataset under parameters $\rho$ is

$$
p(D;\rho)=\prod_{j=1}^m p(x^{(j)};\rho).
$$

Taking logs,

$$
\ell(\rho)
=
\sum_{j=1}^m \log p(x^{(j)};\rho).
$$

Now use the Bayesian network factorization for each data point:

$$
p(x^{(j)};\rho)=\prod_{i=1}^n p(x_i^{(j)} \mid x_{\mathrm{pa}(i)}^{(j)};\rho).
$$

So

$$
\ell(\rho)
=
\sum_{j=1}^m \sum_{i=1}^n \log p(x_i^{(j)} \mid x_{\mathrm{pa}(i)}^{(j)};\rho).
$$

At this step, each term corresponds to one node $i$ in one data point $j$. Now reverse the order of summation:

$$
\ell(\rho)
=
\sum_{i=1}^n \sum_{j=1}^m \log p(x_i^{(j)} \mid x_{\mathrm{pa}(i)}^{(j)};\rho).
$$

This is already informative: the full log-likelihood is a sum of node-specific contributions. But we can go one step further and group data points according to the parent configuration they present for node $i$:

$$
\ell(\rho)
=
\sum_{i=1}^n \sum_{x_{\mathrm{pa}(i)}} \sum_{j: \, x_{\mathrm{pa}(i)}^{(j)} = x_{\mathrm{pa}(i)}} \log p(x_i^{(j)} \mid x_{\mathrm{pa}(i)};\rho).
$$

Now the decomposition becomes conceptually clear. Fix a node $i$ and fix one parent configuration $x_{\mathrm{pa}(i)}$. The inner sum uses exactly those data points in which the parents of $X_i$ took that configuration. Within that subset of the data, we are simply estimating a discrete distribution over the possible values of $X_i$.

So each CPT row can be optimized independently.

### Formal maximum likelihood estimate

Let

$$
N_i(x, x') = \#\{j : x_i^{(j)} = x,\; x_{\mathrm{pa}(i)}^{(j)} = x'\}
$$

be the count of data points in which node $i$ takes value $x$ and its parents take configuration $x'$.

Let

$$
N_i(x') = \#\{j : x_{\mathrm{pa}(i)}^{(j)} = x'\}
$$

be the number of data points in which the parents of node $i$ take configuration $x'$, regardless of the child's value.

Then the maximum likelihood estimate is

$$
\widehat p(X_i = x \mid X_{\mathrm{pa}(i)} = x')
=
\frac{N_i(x,x')}{N_i(x')}.
$$

### Interpretation paragraph

This estimator is exactly what it looks like: within the subset of data where the parent configuration equals $x'$, the estimated conditional probability of $X_i=x$ is just the empirical fraction of times that value occurs.

So parameter learning in a Bayesian network with complete discrete data is not mysterious. It is local counting.

### Boundary conditions, assumptions, and failure modes

This clean estimator depends on several conditions.

1. **The structure is assumed known.**  
   We are not yet learning the graph itself.

2. **The data are complete.**  
   Every training case must include all node values needed to decide which CPT row the case belongs to and which child value occurred there.

3. **The variables are discrete.**  
   Otherwise the row-wise multinomial counting argument changes form.

4. **Zero counts can be a problem.**  
   If a parent configuration $x'$ never appears in the data, then $N_i(x')=0$, and the raw empirical conditional probability for that row is undefined.

5. **Even when defined, MLE can overfit.**  
   If a child value never appears in a particular row, the MLE assigns probability $0$ to it, which may be too extreme for small samples.

The standard remedy is regularization or Bayesian smoothing. For example, with pseudo-counts $\alpha_{x,x'} > 0$,

$$
\widehat p(X_i=x \mid X_{\mathrm{pa}(i)}=x')
=
\frac{N_i(x,x') + \alpha_{x,x'}}{N_i(x') + \sum_x \alpha_{x,x'}}.
$$

This corresponds to a Dirichlet prior over each CPT row.

### Fully worked example: fitting a small network

Consider the three-node chain

$$
X_1 \to X_2 \to X_3
$$

and the following dataset of $m=10$ complete observations:

| Case | $X_1$ | $X_2$ | $X_3$ |
|---|---:|---:|---:|
| 1 | 1 | 0 | 0 |
| 2 | 1 | 1 | 1 |
| 3 | 1 | 1 | 1 |
| 4 | 1 | 0 | 1 |
| 5 | 1 | 1 | 1 |
| 6 | 1 | 1 | 0 |
| 7 | 0 | 1 | 0 |
| 8 | 1 | 1 | 1 |
| 9 | 1 | 0 | 0 |
| 10 | 0 | 0 | 1 |

We estimate each factor separately.

#### Step 1: estimate $p(X_1)$

Since $X_1$ has no parents, this is just its empirical marginal distribution.

Count the number of zeros and ones:

- $X_1=0$ appears in cases 7 and 10, so count $2$.
- $X_1=1$ appears in the remaining $8$ cases.

Therefore

$$
\widehat p(X_1=0)=\frac{2}{10},\qquad
\widehat p(X_1=1)=\frac{8}{10}.
$$

#### Step 2: estimate $p(X_2\mid X_1)$

Now the parent is $X_1$, so we split the data by the value of $X_1$.

When $X_1=0$, the relevant cases are 7 and 10.

- In case 7, $X_2=1$.
- In case 10, $X_2=0$.

So among the two cases with $X_1=0$,

$$
\widehat p(X_2=0\mid X_1=0)=\frac{1}{2},\qquad
\widehat p(X_2=1\mid X_1=0)=\frac{1}{2}.
$$

When $X_1=1$, the relevant cases are 1,2,3,4,5,6,8,9.

Among these eight cases:

- $X_2=0$ occurs in cases 1,4,9, so count $3$.
- $X_2=1$ occurs in cases 2,3,5,6,8, so count $5$.

Thus

$$
\widehat p(X_2=0\mid X_1=1)=\frac{3}{8},\qquad
\widehat p(X_2=1\mid X_1=1)=\frac{5}{8}.
$$

#### Step 3: estimate $p(X_3\mid X_2)$

Now the parent is $X_2$, so we split by $X_2$.

When $X_2=0$, the relevant cases are 1,4,9,10.

Their $X_3$ values are $0,1,0,1$, so:

- $X_3=0$ occurs $2$ times;
- $X_3=1$ occurs $2$ times.

Therefore

$$
\widehat p(X_3=0\mid X_2=0)=\frac{2}{4},\qquad
\widehat p(X_3=1\mid X_2=0)=\frac{2}{4}.
$$

When $X_2=1$, the relevant cases are 2,3,5,6,7,8.

Their $X_3$ values are $1,1,1,0,0,1$, so:

- $X_3=0$ occurs $2$ times;
- $X_3=1$ occurs $4$ times.

Hence

$$
\widehat p(X_3=0\mid X_2=1)=\frac{2}{6},\qquad
\widehat p(X_3=1\mid X_2=1)=\frac{4}{6}.
$$

We can summarize the learned tables:

For $X_1$:
| $X_1$ | 0 | 1 |
|---|---:|---:|
| $\widehat p(X_1)$ | 2/10 | 8/10 |

For $X_2 \mid X_1$:
| $X_1$ | $X_2=0$ | $X_2=1$ |
|---|---:|---:|
| 0 | 1/2 | 1/2 |
| 1 | 3/8 | 5/8 |

For $X_3 \mid X_2$:
| $X_2$ | $X_3=0$ | $X_3=1$ |
|---|---:|---:|
| 0 | 2/4 | 2/4 |
| 1 | 2/6 | 4/6 |

Now compute the probability of a configuration that was never observed directly, say

$$
X=(0,0,0).
$$

Check the relevant local factors:

- $\widehat p(X_1=0)=2/10$,
- $\widehat p(X_2=0\mid X_1=0)=1/2$,
- $\widehat p(X_3=0\mid X_2=0)=2/4$.

So

$$
\widehat p(0,0,0)=\frac{2}{10}\cdot\frac{1}{2}\cdot\frac{2}{4}=0.05.
$$

This is a very important modeling lesson. Even though the exact triple $(0,0,0)$ was never observed in the sample, the Bayesian network assigns it positive probability because each local event needed for that configuration has been observed in the relevant local context.

### Misconception or counterexample block

**Do not think MLE for a Bayesian network requires optimizing a giant global objective numerically.**  
With known structure and complete discrete data, the optimization decomposes into row-wise counting problems.

**Do not think "unseen full configuration" implies probability zero.**  
In a factorized model, a joint configuration can receive positive probability as long as its local pieces receive positive probability.

**Do not think MLE is always safe.**  
If some row counts are small, MLE can produce unstable or zero estimates. Smoothing matters.

### Connection to later material

This section is the learning counterpart of the semantics section. The graph that gave us local factorization now gives us local estimation. Later, when missing data or latent variables appear, this easy decomposition breaks down and more sophisticated methods are required. That contrast is easier to understand if the complete-data case is clear first.

### Retain / do not confuse

Retain:

- with known structure and complete discrete data, CPT rows are estimated by empirical conditional frequencies;
- the log-likelihood decomposes by node and by parent configuration;
- smoothing is often needed in small samples.

Do not confuse:

- complete-data parameter learning with structure learning;
- unseen joint configuration with impossible event;
- raw MLE with regularized estimation.

---

## 3.4 Example Bayesian networks

### Why this section exists

The abstract definition of a Bayesian network is broad. To use it well, it helps to study recurring graph patterns that appear again and again in practice. Each pattern expresses a distinctive modeling idea: many features pointing to one label, one state depending on the previous state, or many possible causes acting on one effect.

This section therefore shifts from general theory to recurring model families.

---

## 3.4.1 Naive Bayes

### Why this subsection exists

Classification problems often involve one target variable and many observed features. A full joint model over all features is usually too large to estimate well, especially when the number of features is in the hundreds or thousands. Naive Bayes exists to make that problem tractable by imposing a strong but useful conditional independence assumption.

### The object being introduced

The model contains:

- a discrete class label $Y$,
- observed features $X_1,\dots,X_n$.

What is fixed is that $Y$ is the quantity we want to infer after observing feature values. What varies across data points are the realized feature values $x_1,\dots,x_n$ and the class label.

The question the model answers is:

> After observing the feature vector $x$, what is $p(Y \mid x_1,\dots,x_n)$?

### Formal definition

A **naive Bayes model** assumes that the features are conditionally independent given the class label:

$$
p(Y,X_1,\dots,X_n)=p(Y)\prod_{i=1}^n p(X_i \mid Y).
$$

Equivalently, in graph form, $Y$ is a parent of every feature $X_i$, and there are no edges among the features.

### Interpretation paragraph

The model says that once the class $Y$ is known, the remaining dependence among the features is ignored. That is the "naive" part. The features may be strongly dependent marginally, but the model treats them as separate pieces of evidence whose relationship is mediated only through the class label.

This can be a crude approximation. But it has two major advantages. First, the number of parameters scales linearly in the number of features rather than exponentially. Second, for classification, the posterior $p(Y\mid x)$ often works surprisingly well even when the conditional independence assumption is not literally true.

### Boundary conditions, assumptions, and failure modes

Several cautions matter.

1. The conditional independence assumption is usually false in real data. Words in text are not independent given topic; medical symptoms are not independent given disease; sensor readings are not independent given system state.

2. The model is often used for prediction rather than realistic generative modeling. So the right question is not "Is the assumption perfectly true?" but "Is the resulting classifier useful?"

3. Highly redundant features can cause overcounting of evidence. If two features are near-duplicates, naive Bayes may treat them as two independent confirmations of the same signal.

4. Zero counts for feature values within a class create zero probabilities unless smoothing is used.

### Posterior form and log-odds interpretation

For binary classification with classes $y \in \{\text{spam}, \text{ham}\}$, the posterior odds satisfy

$$
\frac{p(\text{spam}\mid x)}{p(\text{ham}\mid x)}
=
\frac{p(\text{spam})}{p(\text{ham})}
\prod_{i=1}^n
\frac{p(x_i\mid \text{spam})}{p(x_i\mid \text{ham})}.
$$

Taking logs,

$$
\eta
=
\log \frac{p(\text{spam}\mid x)}{p(\text{ham}\mid x)}
=
\log \frac{p(\text{spam})}{p(\text{ham})}
+
\sum_{i=1}^n
\log \frac{p(x_i\mid \text{spam})}{p(x_i\mid \text{ham})}.
$$

This form is extremely interpretable. The prior contributes one term, and each feature contributes an additive amount to the score. Positive terms support spam, negative terms support ham, and near-zero terms provide little discrimination.

### Fully worked example: SMS spam filtering

Suppose we build a naive Bayes spam classifier from SMS messages. Let $Y$ indicate whether a message is spam or ham, and let the features encode the presence or count of words.

From the dataset, estimate the class prior. In the source example,

$$
\widehat p(Y=\text{spam}) \approx 0.134.
$$

So before seeing the words, spam is already the less likely class.

Now estimate word probabilities within each class using smoothed counts. The source text gives examples such as:

$$
\widehat p(\text{prize}\mid \text{spam}) = 0.00623,\qquad
\widehat p(\text{prize}\mid \text{ham}) = 0.00002,
$$

$$
\widehat p(\text{the}\mid \text{spam}) = 0.01386,\qquad
\widehat p(\text{the}\mid \text{ham}) = 0.01788,
$$

$$
\widehat p(\text{later}\mid \text{spam}) = 0.00007,\qquad
\widehat p(\text{later}\mid \text{ham}) = 0.00215.
$$

Interpret these one at a time.

- The word "prize" is far more common in spam than in ham, so its log-ratio contribution is strongly positive.
- The word "the" is common in both classes, so its contribution is small.
- The word "later" is more common in ordinary personal messages than in spam, so it contributes evidence against spam.

Now consider the message:

> WINNER!! As a valued network customer you have been selected to receive a 900 pound prize reward!

To score this message, we proceed term by term.

1. Start with the prior log-odds. Since spam is less common overall, the prior term is negative.
2. For each word in the message, look up its class-conditional probabilities.
3. Compute the log-ratio contribution of that word.
4. Add all contributions.

Words such as "winner," "selected," "prize," and "reward" contribute large positive values because they are much more probable in spam than in ham. Function words and uninformative tokens contribute little. If some word is rare or omitted from the model vocabulary, its contribution may be negligible or handled through smoothing.

In the source example, the total score is strongly positive, around $\eta \approx 16$. Converting log-odds to probability,

$$
p(\text{spam}\mid x)=\frac{1}{1+e^{-\eta}}.
$$

With $\eta \approx 16$, this posterior probability is extremely close to $1$, so the message is classified as spam.

Now consider a much more ordinary message:

> Almost there, see u in a sec

This message contains everyday conversational words that are common in ham and not especially associated with spam. The word contributions are mostly negative or near zero. In the source example, the total score is around $\eta \approx -5.7$, which yields a posterior spam probability near $0.003$. So the model classifies it as non-spam.

The general lesson is not merely that some words are "spammy." It is that naive Bayes turns classification into an additive evidence accounting problem.

### Misconception or counterexample block

**Do not think naive Bayes assumes the features are marginally independent.**  
The assumption is conditional independence **given the class**.

**Do not think the model must be literally true to classify well.**  
Naive Bayes often performs well even when the independence assumption is only approximately valid.

**Do not confuse probability with contribution to log-odds.**  
A common word can have high probability in both classes and therefore be a weak discriminator.

### Connection to later material

Naive Bayes is one of the simplest examples of how graph structure turns a large probability problem into a practical model. It also previews later ideas in machine learning: linear scoring functions, regularization through pseudo-counts, and the difference between accurate class prediction and realistic generative structure.

### Retain / do not confuse

Retain:

- naive Bayes factors as $p(Y)\prod_i p(X_i\mid Y)$;
- the model assumes feature independence only after conditioning on $Y$;
- posterior log-odds become a sum of feature-wise contributions.

Do not confuse:

- large probability with strong discriminative value;
- conditional independence with actual causal independence.

---

## 3.4.2 Markov chains

### Why this subsection exists

Many datasets are inherently sequential: words in a sentence, states over time, clicks in a browsing session, weather on consecutive days. In such problems, a variable is often most strongly related to the recent past, not to every earlier state. Markov chains formalize that idea in Bayesian network language.

### The object being introduced

We introduce a sequence of random variables

$$
X_1, X_2, \dots, X_n,
$$

where $X_t$ is the state at time or position $t$.

What is fixed is the sequence length $n$ and the state space of each $X_t$. What varies is the realized sequence $x_1,\dots,x_n$.

The modeling question is:

> How can we represent sequential dependence compactly when the present state summarizes the relevant past?

### Formal definition

A first-order **Markov chain** assumes

$$
p(X_1,\dots,X_n)=p(X_1)\prod_{t=2}^n p(X_t \mid X_{t-1}).
$$

If the transition distribution is the same for every time $t$, so that the same table $p(X_t \mid X_{t-1})$ is reused across positions, the chain is called **homogeneous**.

### Interpretation paragraph

The Markov assumption says that once the present state $X_{t-1}$ is known, earlier history is no longer needed for predicting the next state $X_t$. In probabilistic terms, the current state is a sufficient summary of the past for the purpose of forecasting the immediate future.

This is a modeling statement, not a logical truth. In some systems it is a good approximation; in others it is too short-range.

### Boundary conditions, assumptions, and failure modes

1. The first-order Markov property is an assumption. It may fail when long-range history matters.

2. Homogeneity is also an assumption. Some sequential systems change their transition law over time.

3. Even when local transitions are modeled correctly, global coherence may still be poor. A model that only captures adjacent dependencies can generate locally plausible but globally awkward sequences.

4. State-space size matters. If there are many possible states, transition estimation can be data-hungry, and smoothing becomes essential.

### Why every node separates past from future

In the graph

$$
X_1 \to X_2 \to X_3 \to \cdots \to X_n,
$$

pick an index $t$ with $1 < t < n$. The only paths from a node on the left of $X_t$ to a node on the right pass through $X_t$ as a chain node. If $X_t$ is observed, those paths are blocked. Therefore

$$
(X_1,\dots,X_{t-1}) \perp (X_{t+1},\dots,X_n) \mid X_t.
$$

This is the graphical expression of the Markov property: once the present is known, the future is conditionally independent of the past.

### Fully worked example: bigram language model

Let $X_t$ denote the $t$-th word in a review. A bigram model is just a Markov chain whose states are words. The transition distribution $p(X_t \mid X_{t-1})$ records which words tend to follow which other words.

Suppose we estimate the model from a large collection of positive restaurant reviews. After counting adjacent word pairs and normalizing, we might obtain transitions such as:

- after "great," common next words include "place" and "food";
- after "ordered," very common next words include "the" and "a".

Interpret this carefully. The model is not claiming that "great" causes "place." It is claiming that in the observed corpus, the distribution of the next word depends strongly on the current word.

Now consider how the model generates text.

1. Sample the first word $x_1$ from the initial distribution $p(X_1)$.
2. Given that word, sample $x_2$ from $p(X_2\mid X_1=x_1)$.
3. Continue, each time sampling the next word from the transition distribution conditioned on the current word.
4. Optionally stop when an end-of-sequence token is produced.

Because the model only checks one-word context, each adjacent pair may sound plausible even if the whole sentence drifts. This is exactly what the source example illustrates with generated text that contains locally sensible fragments but poor global coherence.

That is not a bug in the theory. It is the direct consequence of the model's boundary condition: only the immediately previous word is allowed to matter.

### Higher-order $n$-gram models

A trigram model allows

$$
p(X_t \mid X_{t-1},X_{t-2}),
$$

and more generally an $n$-gram model conditions on the previous $n-1$ words.

Conceptually, such a model is still a Markov chain if we redefine the state to include the recent history. For example, in a trigram model we can define a new state

$$
\widetilde X_t = (X_t, X_{t-1}).
$$

Then the process becomes first-order in the enlarged state space. This is conceptually useful because it shows that higher-order temporal dependence can be absorbed into the definition of the state.

But the practical cost is severe: if each word can take $d$ values, the state space grows rapidly, and sparse counts become a major problem.

### Why smoothing matters in sequence models

If a particular word transition never appears in the training corpus, raw MLE assigns it probability zero. That is often too harsh, especially in language data, because many reasonable transitions are merely rare, not impossible.

Smoothing addresses this by redistributing some probability mass to unseen transitions. The simplest version is Laplace smoothing, which adds the same pseudo-count to every possible next word. More sophisticated methods use lower-order statistics to decide where unseen mass should go. For example, if a word is common overall, an unseen transition into that word may deserve more prior mass than a transition into an extremely rare word.

The source text discusses Jelinek-Mercer and Kneser-Ney style ideas precisely because smoothing quality has a large impact on sequence modeling performance.

### Misconception or counterexample block

**Do not think the Markov property means the future is independent of the past unconditionally.**  
It means independence holds **given the present state**.

**Do not think a bigram model understands full sentence meaning.**  
It captures local adjacency, not global semantics or long-range structure.

**Do not think higher-order $n$-grams are fundamentally different in kind.**  
They are still Markov models after an appropriate state redefinition, though often impractical because the state space becomes large.

### Connection to later material

Markov chains are one of the core model families in probability and machine learning. They lead naturally to hidden Markov models, state-space models, and modern sequence models. The source chapter also points forward to transformers and large language models, whose key advance is that they model dependence on much longer histories more flexibly than fixed-order Markov assumptions allow.

### Retain / do not confuse

Retain:

- a first-order Markov chain factors as $p(X_1)\prod_{t=2}^n p(X_t\mid X_{t-1})$;
- conditioning on the present blocks dependence between past and future;
- higher-order $n$-grams enlarge the conditioning context but keep the same core idea.

Do not confuse:

- first-order dependence with global coherence;
- homogeneity with the Markov property itself.

---

## 3.4.3 Noisy-OR models

### Why this subsection exists

Bayesian networks are compact when each node has only a few parents. But some effects can have many possible causes: a car failing to start, a symptom produced by many diseases, an alarm triggered by many sensors. In such cases, the standard conditional probability table for the child grows exponentially with the number of parents. Noisy-OR exists to control that explosion.

### The object being introduced

We consider one binary child variable $Y$ and many binary parent variables

$$
X_1,\dots,X_n.
$$

What is fixed is that each $X_i$ is a possible cause and $Y$ is an effect that can be triggered by one or more of them. What varies is which causes are present in a given case.

The model answers the question:

> How can we define $p(Y\mid X_1,\dots,X_n)$ using only a small number of parameters when each active cause can independently trigger the effect?

### Formal definition

In a **noisy-OR** model, each cause $X_i$ has an associated parameter $\rho_i \in [0,1]$, interpreted as the probability that cause $i$ fails to trigger the effect when it is active.

The conditional probability of the effect is

$$
p(Y=1 \mid X_1,\dots,X_n)
=
1 - \prod_{i=1}^n \rho_i^{\mathbf 1[X_i=1]}.
$$

Equivalently,

$$
p(Y=0 \mid X_1,\dots,X_n)
=
\prod_{i=1}^n \rho_i^{\mathbf 1[X_i=1]}.
$$

If all $X_i=0$, then the empty product equals $1$, so $p(Y=0)=1$ and $p(Y=1)=0$, unless a separate leak parameter is added.

### Interpretation paragraph

This formula says that each active cause gets an independent chance to produce the effect. The parameter $\rho_i$ is not the probability that the cause occurs. It is the probability that the cause, **if present**, fails to activate the effect. Therefore $1-\rho_i$ is the success probability for that cause.

The product form for $p(Y=0\mid X)$ reflects the idea that the effect stays absent only if every active cause fails. As more causes become active, the chance that all of them fail decreases, so $p(Y=1\mid X)$ increases.

### Boundary conditions, assumptions, and failure modes

Noisy-OR is compact because it is restrictive.

1. All variables are binary.
2. Causes act independently in their attempts to trigger the effect.
3. Causes combine through OR-like logic: any successful cause is enough.
4. The model does not capture arbitrary interactions, such as strong synergy or inhibition between causes.
5. Without a leak term, the model says the effect cannot occur if all modeled causes are absent.

So noisy-OR is appropriate when many causes contribute in roughly alternative, independent ways. It is not a generic replacement for every large CPT.

### Fully worked example: headache from several causes

Let $H$ indicate whether a person has a headache. Let the possible causes be:

- $C$: cold,
- $F$: flu,
- $D$: dehydration.

Suppose the noisy-OR parameters are

$$
\rho_C = 0.2,\qquad
\rho_F = 0.1,\qquad
\rho_D = 0.5.
$$

Interpret these before computing anything:

- If cold is present alone, it fails to trigger headache with probability $0.2$, so it triggers headache with probability $0.8$.
- If flu is present alone, it triggers headache with probability $0.9$.
- If dehydration is present alone, it triggers headache with probability $0.5$.

Now compute the conditional probabilities row by row.

#### Case 1: no causes present
If $C=F=D=0$, there are no active causes. Therefore

$$
p(H=0\mid 0,0,0)=1,\qquad p(H=1\mid 0,0,0)=0.
$$

#### Case 2: only dehydration present
If $C=0,F=0,D=1$, then only $D$ can trigger headache:

$$
p(H=0\mid 0,0,1)=\rho_D=0.5,
$$

so

$$
p(H=1\mid 0,0,1)=1-0.5=0.5.
$$

#### Case 3: only flu present
If $C=0,F=1,D=0$,

$$
p(H=0\mid 0,1,0)=\rho_F=0.1,
$$

so

$$
p(H=1\mid 0,1,0)=0.9.
$$

#### Case 4: cold and flu both present
If $C=1,F=1,D=0$, the effect stays off only if **both** active causes fail:

$$
p(H=0\mid 1,1,0)=\rho_C \rho_F = 0.2\times 0.1 = 0.02.
$$

Therefore

$$
p(H=1\mid 1,1,0)=1-0.02=0.98.
$$

#### Case 5: all three causes present
If $C=F=D=1$,

$$
p(H=0\mid 1,1,1)=\rho_C\rho_F\rho_D = 0.2\times 0.1 \times 0.5 = 0.01,
$$

so

$$
p(H=1\mid 1,1,1)=0.99.
$$

The entire table is generated from only three parameters. By contrast, an unrestricted CPT for three binary parents would need one probability for each of the $2^3=8$ parent configurations.

The general pattern is clear: as the number of active causes increases, the chance of the effect generally rises because it becomes harder for every active cause to fail simultaneously.

### Misconception or counterexample block

**Do not misread $\rho_i$.**  
It is the probability that cause $i$ fails to trigger the effect when active, not the probability that the cause occurs and not directly the probability of the effect.

**Do not think noisy-OR can represent every many-parent CPT.**  
It only captures a specific independence-of-failures structure.

**Do not forget the leak issue.**  
Without a leak term, the model forces $Y=0$ whenever all causes are absent.

### Connection to later material

Noisy-OR is an example of a broader modeling strategy: when a generic CPT is too large, replace it with a structured conditional family that has a more interpretable and more scalable parameterization. This idea appears repeatedly in probabilistic modeling and machine learning.

### Retain / do not confuse

Retain:

- noisy-OR is a compact many-causes one-effect model;
- $p(Y=0\mid X)$ is the product of failure probabilities of active causes;
- the model scales linearly in the number of causes.

Do not confuse:

- cause presence with cause success;
- noisy-OR with a generic arbitrary CPT.

---

## 3.4.4 Rewriting noisy-OR with auxiliary variables

### Why this subsection exists

The noisy-OR formula is compact, but sometimes we want to express the same model using a graph in which every node has only a small number of parents. This can help clarify the mechanism and connect the model to a broader theme in graphical modeling: introducing extra variables to simplify structure.

### The object being introduced

The new objects are **auxiliary variables** representing whether each cause successfully transmits its effect. These variables are not part of the original observable problem statement. They are introduced to rewrite the model.

### Construction

For each cause $X_i$, introduce an auxiliary binary variable $\widetilde X_i$ that indicates whether cause $i$ actually succeeds in transmitting activation.

For example, for cause $C$, define

$$
p(\widetilde C = 1 \mid C=0)=0,\qquad
p(\widetilde C = 1 \mid C=1)=1-\rho_C.
$$

So if the cause is absent, its auxiliary activation must be $0$. If the cause is present, the auxiliary variable turns on with the success probability of that cause.

Do the same for $F$ and $D$, producing $\widetilde F$ and $\widetilde D$.

Next, combine these auxiliary activations through deterministic OR operations. For instance, one can define intermediate variables so that no node ever has more than two parents, such as

$$
\widetilde X = \widetilde C \lor \widetilde F,
\qquad
H = \widetilde X \lor \widetilde D.
$$

### Interpretation paragraph

This construction separates two ideas that were implicit in the original noisy-OR formula:

1. each cause independently tries to activate the effect;
2. the effect occurs if any activation succeeds.

The auxiliary variables make those two stages explicit. They also show why the noisy-OR probability formula has the form it does.

### Boundary conditions and learning implications

This rewriting preserves the distribution over the original observable variables, but it introduces latent variables if the auxiliaries are not observed in the dataset. That changes the learning problem. A model that was simple to specify may become harder to fit from data if the extra variables are hidden.

This is an important modeling tradeoff: a structural simplification in the graph can create statistical complexity in learning.

### Misconception block

**Do not think auxiliary-variable expansions are free.**  
They may simplify graph degree, but they often introduce latent variables.

**Do not think two graph representations with different hidden variables are equivalent as learning problems.**  
They may represent the same observable distribution family while differing substantially in estimation difficulty.

### Connection to later material

This subsection points toward latent-variable models and incomplete-data learning. It also reinforces the broader lesson that graphical models can often be transformed in multiple ways, each with different representational and computational consequences.

### Retain / do not confuse

Retain:

- noisy-OR can be rewritten using auxiliary success variables and deterministic OR nodes;
- the observable distribution can stay the same under such a rewrite;
- latent variables can make learning harder.

Do not confuse:

- compact specification with easy parameter estimation in the presence of unobserved variables.

---

## 3.5 Reasoning about causality (preview)

### Why this section exists

Throughout the chapter, causal language has been a useful intuition. We naturally say burglary causes alarm, alarm causes calls, and so on. But the mathematics of Bayesian networks up to this point has only required a factorization of a joint distribution. That is not yet enough to justify intervention reasoning.

This section exists to mark the boundary clearly. Ordinary probabilistic conditioning and genuine causal intervention are different operations. If we do not distinguish them, we will misread associations as effects.

### The object being introduced

The new object is an **intervention**, written conceptually as $\mathrm{do}(X=x)$. What is fixed is a graph being interpreted causally, not merely probabilistically. What varies is whether a variable is merely observed to take a value or externally forced to take that value.

The question is:

> What is the effect on other variables if we set $X$ to a chosen value, rather than merely observing that $X$ happened to equal that value?

### Formal idea

In a causal reading of a Bayesian network, intervening on $X$ means replacing the usual conditional mechanism

$$
p(X \mid X_{\mathrm{pa}(X)})
$$

with a degenerate distribution that forces $X$ to the chosen value. Graphically, this is often described as removing the incoming edges into $X$, because under intervention, $X$ no longer responds to its usual causes.

The resulting interventional distribution is different from the ordinary conditional distribution in general.

### Interpretation paragraph

Conditioning on $X=x$ restricts attention to cases in which $X$ naturally took value $x$. Those cases may be unusual in systematic ways because the causes of $X$ may also affect other variables.

Intervening with $\mathrm{do}(X=x)$, by contrast, breaks the normal causal mechanism that determines $X$. The rest of the system then evolves from that forced value. So intervention changes the data-generating process, while conditioning only filters the existing process.

### Boundary conditions, assumptions, and failure modes

This distinction only becomes meaningful if the graph is being given a causal interpretation. A generic Bayesian network as a factorized probability model does not automatically support valid intervention claims.

In addition, hidden confounders can make $p(Y\mid X)$ very different from $p(Y\mid \mathrm{do}(X))$. If some unobserved variable influences both $X$ and $Y$, then observing $X$ changes what we believe about that confounder, while intervening on $X$ need not.

### Fully worked example: confounding makes conditioning differ from intervention

Consider three binary variables:

- $U$: unobserved risk type,
- $X$: treatment decision,
- $Y$: outcome.

Assume the true causal structure is

$$
U \to X,\qquad U \to Y,
$$

and there is **no** arrow from $X$ to $Y$. So treatment has no causal effect; both treatment and outcome are driven by the hidden risk variable $U$.

Now choose a very simple parameterization:

- $P(U=1)=0.5$,
- $X=U$ deterministically,
- $Y=U$ deterministically.

Read this carefully. High-risk individuals ($U=1$) always receive treatment ($X=1$) and always have bad outcome ($Y=1$). Low-risk individuals ($U=0$) never receive treatment and never have bad outcome.

Now compare conditioning and intervention.

#### Step 1: ordinary conditioning

Compute $P(Y=1\mid X=1)$.

If $X=1$, then because $X=U$ deterministically, we know $U=1$. Since $Y=U$, this implies $Y=1$ with probability $1$. Therefore

$$
P(Y=1\mid X=1)=1.
$$

Similarly,

$$
P(Y=1\mid X=0)=0.
$$

From observational data alone, treatment and bad outcome appear perfectly associated.

#### Step 2: intervention

Now compute $P(Y=1\mid \mathrm{do}(X=1))$.

Under intervention, we force $X=1$, but we do **not** alter the distribution of $U$, and $Y$ still depends only on $U$. Since $U$ remains $1$ with probability $0.5$,

$$
P(Y=1\mid \mathrm{do}(X=1)) = P(U=1)=0.5.
$$

Likewise,

$$
P(Y=1\mid \mathrm{do}(X=0)) = 0.5.
$$

So the intervention has no effect, exactly as the graph says. The strong observational association came entirely from confounding through $U$.

This example illustrates the core lesson:

- $P(Y\mid X)$ answers: among cases where $X$ happened naturally, how often do we see $Y$?
- $P(Y\mid \mathrm{do}(X))$ answers: if we force $X$, what happens to $Y$?

Those are different questions.

### Misconception or counterexample block

**Do not equate conditioning with intervention.**  
In the presence of confounding, $P(Y\mid X)$ can differ sharply from $P(Y\mid \mathrm{do}(X))$.

**Do not think every Bayesian network is automatically causal.**  
Causal reasoning requires extra assumptions about what the arrows mean and about which confounders have been modeled.

### Connection to later material

This section is only a preview, but it sets an essential conceptual boundary. Bayesian networks provide the language of directed dependence structure. Causal reasoning builds on that language by adding intervention semantics. Once that step is taken, tools such as do-calculus become relevant.

### Retain / do not confuse

Retain:

- probabilistic factorization alone is not the same as causal semantics;
- conditioning filters observations, intervention changes the mechanism;
- hidden confounding can make observational association differ from causal effect.

Do not confuse:

- $P(Y\mid X)$ with $P(Y\mid \mathrm{do}(X))$;
- useful causal intuition with a justified causal model.

---

## Chapter conclusion

The point of Bayesian networks is not merely to draw arrows between variables. Their value lies in the disciplined interplay between probability, graph structure, and statistical learning.

This chapter built that interplay in layers.

First, it showed why high-dimensional probability needs structure and how conditional independence turns the chain rule into a compact factorization. Second, it showed how the graph can be used to read conditional independencies through d-separation, including the especially important collider phenomenon. Third, it showed how a known graph converts parameter learning with complete data into a collection of local counting problems. Fourth, it studied several canonical model families that demonstrate different uses of the framework: naive Bayes for classification, Markov chains for sequences, and noisy-OR for many-cause systems. Finally, it previewed the distinction between observational conditioning and causal intervention.

The unifying theme is that graphical structure is never decoration. It determines what may depend on what, what can be estimated locally, what independencies can be trusted, and what kinds of questions the model can and cannot answer.

For mastery, the reader should now be able to do four things without hesitation:

1. read a DAG and write the associated factorization;
2. decide whether two variables are d-separated given evidence by checking paths carefully;
3. estimate CPT entries from complete data by conditional counting;
4. recognize when a modeling problem has the shape of a standard Bayesian network family.

Those abilities are the foundation on which later work in inference, structure learning, latent-variable models, and causal reasoning is built.

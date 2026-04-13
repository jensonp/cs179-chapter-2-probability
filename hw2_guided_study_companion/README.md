# hw2_guided_study_companion.md

# CS 179 HW2 Guided Study Companion

This document is designed to help you learn your way through Homework 2 rather than hand you a finished answer key. It is built as a study companion: first the library catch-up you need, then each problem restated in a cleaner form, then the reasoning path you should follow to reach the result yourself.

The organizing idea is simple. For each problem, do not ask “what command do I use?” first. Ask:

- what mathematical object am I holding,
- what operation is the problem asking for,
- what has to stay fixed,
- what has to be summed out, conditioned on, or estimated,
- and what would count as a correct check of the result?

---

# Part I. pyGMs mini-lecture for HW2

## Why pyGMs is being used here

pyGMs is not the topic of the course. It is a medium for expressing things you already know from probability. In this homework it is mainly being used to make discrete probability tables concrete. That means the most important thing is not memorizing library names. The most important thing is understanding what mathematical object each library object stands for.

For Homework 2, the core pyGMs idea is that a discrete probability law can be represented as a factor, meaning a function over one or more discrete random variables. If the variables are finite, the factor can be stored as a table.

So when you use pyGMs, always keep this picture in mind:

- a variable says which random quantity you are talking about and how many states it has,
- a factor is a table over one or more variables,
- and most operations are just table manipulations with probabilistic meaning.

## Variables

A pyGMs variable has two pieces of information:

- an integer ID,
- and a number of possible states.

The integer ID is not decoration. It is how pyGMs identifies the variable internally. Your Python name for that variable is only your local label.

So if you call something `T`, that is for your convenience. pyGMs cares about the variable’s internal ID and number of states.

This matters because factor tables are organized by variable IDs, not by the order you happened to type things in casual code.

## Factors

A factor is a function over a scope of variables. If the variables are discrete, that function can be written as a table.

Examples:

- a factor over one binary variable is a length-2 table,
- a factor over two binary variables is a 2 by 2 table,
- a factor over three binary variables is a 2 by 2 by 2 table.

A factor is not automatically a probability distribution. It is simply a table of values indexed by assignments. It becomes a joint probability distribution only if the entries are nonnegative and sum to one over the whole table. It becomes a conditional probability table only if the correct normalization condition holds for each fixed conditioning assignment.

That distinction matters because many homework steps involve intermediate factors that are not yet normalized as probabilities until the final division or normalization step.

## Scope

The scope of a factor is the set of variables it depends on.

This is the first thing to track in every problem. If a factor has scope `(T, D, C)`, then every table entry corresponds to one assignment of those three variables. If you condition on `T = 1`, then the resulting object is now effectively a factor over the remaining variables. If you sum out `D`, then the scope shrinks accordingly.

So many pyGMs operations can be understood as “change the scope in a mathematically meaningful way.”

## The three factor operations that matter most for HW2

### Conditioning or slicing

Conditioning means fixing one or more variables to observed values and looking only at the entries consistent with that evidence.

If you start with a factor over `(T, D, C)` and fix `T = 1`, then you are no longer looking at the full table. You are looking at the subtable compatible with `T = 1`.

This is not yet the same thing as a normalized conditional probability unless you later normalize. At the moment of restriction, you are only selecting the relevant part of the joint table.

### Summing out variables

Summing out is marginalization.

If you have a factor over `(T, D, C)` and you sum out `D`, then for each fixed `(T, C)` pair you add over both possible values of `D`. The resulting factor has smaller scope because `D` no longer appears as an argument.

This is the central operation behind marginals and also behind exact inference more broadly.

### Normalizing or dividing

A conditional probability is usually built by taking a joint-like factor and dividing by the right marginal.

So if you want something like `p(C | T = 1)`, the natural reasoning path is:

- restrict to `T = 1`,
- sum out nuisance variables if needed,
- then divide by the total mass so the result sums to one over `C`.

The deep lesson is that a conditional is not a new magical object. It is a correctly normalized factor derived from a joint factor.

## Factor arithmetic

When you multiply factors, you are forming a new function over the union of their scopes.

When you divide factors, you are comparing assignments across matching scopes in a way that often produces a conditional-like object when the denominator is the right marginal.

The important thing is not the syntax. The important thing is to know whether the arithmetic you are doing matches the probability identity you are trying to express.

## What can go wrong in pyGMs

There are four common mistakes worth killing early.

First, do not forget that factors are stored according to variable ID order, not casual typing order.

Second, do not confuse restriction with normalization. A restricted subtable is often not yet a conditional probability.

Third, do not sum out the wrong variable. Each summation changes the scope, so always pause and ask what variables should remain at the end of the operation.

Fourth, do not forget what each resulting factor is supposed to mean probabilistically. Keep naming the object in words as you go.

---

# Part II. Pyro mini-lecture for HW2

## Why Pyro appears in this homework

Pyro is being used here as a way to express generative probabilistic models. In this homework you do not need most of Pyro. You only need the basic idea that a model is a sequence of random draws whose distributions can depend on earlier draws.

So the key mental model is:

- a Pyro model is a generative story,
- each draw corresponds to one random variable,
- dependencies are expressed by making the distribution of a later variable depend on the already drawn values of earlier ones.

That is exactly what a Bayesian network means operationally.

## Sampling order

In a Bayesian network, a node can only depend on its parents. So when you write the generative process, you must sample in an order where parents appear before children.

For the Wet Grass model, that means:

- draw whether it is cloudy,
- then draw sprinkler given cloudy,
- then draw rain given cloudy,
- then draw wet grass given sprinkler and rain.

The point is not to memorize the sequence as code. The point is to see that the sequence is just the graph turned into a sampling story.

## What a sample means

One full run of the model produces one joint configuration of all the random variables.

If the variables are binary, one run gives you one tuple of zeros and ones.

If you run the model many times, you get an empirical dataset sampled from the joint distribution defined by the model.

That is why empirical probabilities in Problem 2 are estimated by repeated samples and counting how often each event occurs.

## Distribution parameters versus observed values

Pyro forces you to think clearly about this distinction.

The distribution parameters are the probabilities that define how a variable is sampled.

The observed sample values are the actual zeros or ones produced on a given run.

These are different objects. The model parameters stay fixed while the sampled values change from run to run.

## Why the ordering in Problem 5 matters

In the normalizing-flow problem, Pyro is not being used mainly for a directed graph. It is being used to represent a transformed continuous distribution.

The core structure there is:

- start from a simple base distribution,
- apply an invertible transformation,
- get a richer transformed distribution,
- then train the transformation parameters by maximizing log probability on data.

So Pyro serves two different roles in this homework:

- in Problem 2, it is a convenient way to express a directed generative model,
- in Problem 5, it is a convenient way to express a transformed continuous distribution whose density remains computable.

---

# Part III. Problem-by-problem guided study path

---

# Problem 1. Factor tables in Python

## Clean restatement

You are given a full joint distribution over three binary variables in the Dentist example. The problem asks you to treat that joint distribution as a factor table and use factor operations to produce:

- subtables obtained by fixing evidence,
- marginals obtained by summing out variables,
- conditionals obtained by dividing by the right marginal,
- and a conditional-independence check by comparing the original joint to a product of smaller factors.

Then you repeat the same kind of reasoning using an empirical estimate from sampled data.

## What mathematical object you start with

You start with a joint probability distribution over three discrete variables. In pyGMs this is represented as one factor over the scope `(T, D, C)`.

Because it is a full joint distribution, every table entry has a direct probabilistic meaning: for each full assignment of the three variables, the entry gives the probability of that assignment.

So before doing anything else, treat this factor as the truth table for the whole model.

## Problem 1.1: Table manipulations

### What the problem is asking in probabilistic language

The question asks you to compute `p(C | T = 1)` in stages, not all at once.

It wants you to explicitly expose three objects:

1. the restricted subtable corresponding to `T = 1`,
2. the smaller factor obtained after summing out `D`,
3. the normalized conditional distribution over `C`.

This is good pedagogy because it forces you to see that a conditional distribution is built from simpler operations.

### Reasoning path

First, fix `T = 1`.

This does not yet produce a conditional distribution. It produces the part of the joint table that remains when only assignments with `T = 1` are kept.

At that point, the active uncertainty is still over `D` and `C`. So you should conceptually view the result as a factor over `(D, C)` that still carries the joint mass associated with `T = 1`.

Second, sum out `D`.

The question asks for `p(T = 1, C)` before normalization. That means for each value of `C`, you add together the entries for all possible values of `D` while keeping `T = 1` fixed.

This removes `D` from the scope and leaves you with a smaller factor over `C` that tells you the joint mass of `T = 1` together with each value of `C`.

Third, normalize over `C`.

Once you have the factor giving `p(T = 1, C)`, divide by the total mass associated with `T = 1`. That produces `p(C | T = 1)`.

The thing to check at the end is simple: the resulting table over `C` must sum to one.

### What to write in your solution

When you explain this in your PDF, say explicitly:

- what was fixed,
- what was summed out,
- what remained in scope at each stage,
- and why the last step is normalization rather than another marginalization.

That is the conceptual heart of the problem.

## Problem 1.2: Checking conditional independence

### What the problem is asking

You are being asked to verify the conditional-independence claim

`D` is independent of `T` given `C`.

This means that once `C` is known, learning `D` should not give additional information about `T`, and learning `T` should not give additional information about `D`.

The factorization corresponding to that claim is:

`p(T, D, C) = p(C) p(D | C) p(T | C)`.

So the problem is asking you to build the right-hand side from factor operations and compare it numerically to the original joint factor.

### Reasoning path

First compute `p(C)`.

That means sum out both `T` and `D` from the original joint factor. The resulting factor has scope only `C`.

Second compute `p(D | C)`.

You need the joint factor over `(D, C)` and then the marginal over `C`. Divide the joint by the marginal in the correct scope-aware way so that for each fixed `C`, the values over `D` form a conditional distribution.

Third compute `p(T | C)` in the same style.

Now multiply the three resulting factors:

- `p(C)`,
- `p(D | C)`,
- `p(T | C)`.

That gives you a new factor over `(T, D, C)`.

The independence claim predicts that this reconstructed factor should match the original joint factor very closely.

Finally, compare them numerically.

The conceptual meaning is: if the conditional-independence factorization is exactly correct, the two factors represent the same joint distribution, so the error measures should be zero up to numerical precision.

### What to pay attention to

Do not treat this as a blind numerical exercise.

The real point is that conditional independence is being turned into a testable factorization identity.

You are learning to go back and forth between:

- a probabilistic statement in words,
- a factorization formula,
- and an actual numerical table comparison.

## Problem 1.3: Empirical probability estimates

### What the problem is asking

Now the true joint distribution is no longer assumed to be known directly. Instead you are given synthetic data drawn from it, and you build an empirical estimate from counts.

Then you repeat the same kind of conditional-independence factorization using the empirical estimate and compare two candidate approximations to the true joint:

- the raw empirical estimate,
- and the factorized estimate that enforces conditional independence through `C`.

### Reasoning path

First, count occurrences of each `(T, D, C)` configuration in the sampled dataset.

That gives you raw counts.

Second, convert counts into a normalized empirical factor.

If smoothing or regularization is added, understand why: it prevents exact zeros for rare or unseen outcomes, which is especially important when later divisions or KL divergences are involved.

Third, compute the empirical versions of:

- `p_hat(C)`,
- `p_hat(D | C)`,
- `p_hat(T | C)`.

Fourth, build the factorized approximation

`q(T, D, C) = p_hat(C) p_hat(D | C) p_hat(T | C)`.

Now compare both candidate approximations against the true joint:

- `p_hat` compared to the true joint,
- `q` compared to the true joint.

### What the real lesson is

This problem is not just asking “which number is smaller?”

It is asking you to see a modeling tradeoff.

The raw empirical estimate has more flexibility because it keeps the full table structure, but with limited data it may be noisy.

The factorized estimate imposes structural assumptions, which reduces flexibility but can improve generalization if the structural assumption is approximately correct.

---

# Problem 2. Expressing a model in Pyro

## Clean restatement

You are given a four-variable Wet Grass Bayesian network with specified Bernoulli probabilities. Your task is to express the generative story in Pyro, sample from it repeatedly, and estimate several marginal probabilities and one joint event probability from the samples.

## What mathematical object you start with

You start with a Bayesian network. A Bayesian network is not yet code. It is a factorization of a joint distribution according to a directed acyclic graph.

The graph says:

- `C` is a parent of `S`,
- `C` is a parent of `R`,
- `S` and `R` are both parents of `W`.

So the joint factorization is:

`p(C, S, R, W) = p(C) p(S | C) p(R | C) p(W | R, S)`.

The Pyro model is just a generative implementation of this factorization.

## How to reason through the model

The order matters because parents must be sampled before children.

So the reasoning sequence is:

1. draw `C`,
2. using that value, draw `S`,
3. using that value, draw `R`,
4. using both `S` and `R`, draw `W`.

At each step, the only thing that matters is the parent configuration that determines the distribution for the child.

## How to reason through the empirical estimates

Once you draw many full samples from the model, you have an empirical dataset of joint assignments.

Then each probability estimate is simply a frequency:

- `p_hat(C = 1)` is the fraction of samples with `C = 1`,
- `p_hat(S = 1)` is the fraction of samples with `S = 1`,
- and so on.

For the joint event `p_hat(S = 1, R = 1)`, count how many full samples satisfy both conditions simultaneously and divide by the total number of samples.

## What to check

The homework itself gives you useful sanity checks for two marginals. Your empirical estimates should be close to those values, not exactly equal, because you are using finite random samples.

So if a number is wildly off, do not first suspect probability theory. First suspect the generative structure or the parent-conditioned probabilities you used when defining the model.

## What the real lesson is

The point of this problem is not just to write a Pyro function. It is to feel the equivalence between:

- a graph,
- a factorization,
- a generative story,
- and a sampling procedure.

---

# Problem 3. Building Power Bayes net

## Clean restatement

You are given a polytree describing variables related to power in a building, people’s states, projector behavior, and observational statements. You are asked whether observing one variable can affect your belief about another, either with or without additional evidence.

This is a pure conditional-independence and active-path problem.

## What mathematical object you start with

You start with a directed acyclic graph, not with numbers.

That means you are not being asked to compute probabilities numerically. You are being asked to decide whether information can flow from one variable to another under specified evidence conditions.

Because the graph is a polytree, there is only one undirected path between any two nodes. This is extremely important because it simplifies the task: to decide whether one node can affect another, you only need to inspect that one path and determine whether it is active or blocked.

## The only method you need

Take the unique undirected path between the source variable and the target variable.

Then inspect each local three-node pattern along the path.

There are only three patterns that matter:

- chain,
- fork,
- collider.

For a chain or a fork:
- the path is active if the middle node is unobserved,
- the path is blocked if the middle node is observed.

For a collider:
- the path is blocked if neither the collider nor any descendant of the collider is observed,
- the path becomes active if the collider or one of its descendants is observed.

That is the entire method.

## How to approach each question

For each yes-or-no question in Problem 3:

1. find the unique path,
2. identify each intermediate node’s local role,
3. check whether any observed variable blocks or opens the path,
4. conclude whether influence can flow.

If the answer is yes, name the active path.

If the answer is no, identify exactly where the path is blocked and by what type of local structure.

## Why this problem matters

This is where graphical models stop being “tables and formulas” and become reasoning tools.

---

# Problem 4. Bigram text models

## Clean restatement

You are given a text corpus. You preprocess it into tokens, limit the vocabulary to the most frequent words, replace rare words by a special token, estimate a first-order Markov transition matrix over the reduced vocabulary, answer a next-word query, and then generate sample sequences from the model.

## What mathematical object you start with

You start with a single long observed sequence of words.

After preprocessing and vocabulary restriction, each word is turned into an index.

At that point the model is a first-order Markov chain over a finite state space of word indices.

That means the key object is a transition matrix `T` where entry `(i, j)` gives the probability that the next token is `j` when the current token is `i`.

## Reasoning path

First preprocess the text.

This step is not trivial bookkeeping. It defines the state space of the model. Removing punctuation, lowercasing, and replacing rare words all change what counts as a state and therefore change the transition structure you are estimating.

Second build the reduced vocabulary.

The most frequent words stay as individual states. Rare words are collapsed into the single unknown-token state.

Third count adjacent pairs.

For every consecutive pair in the index sequence, add one count to the corresponding transition entry.

This produces raw transition counts.

Fourth normalize each row.

Each row corresponds to a current word. Each row must become a conditional distribution over the next word. So the row sum must become one.

Now you can answer the question about the most probable followers of the word `miss` by looking at the row corresponding to the token `miss` and finding the largest probabilities.

Finally, generate sequences.

Pick a starting word, then repeatedly sample the next token according to the row corresponding to the current token. Each new token becomes the current token for the next step.

## What to pay attention to

The modeling assumption is that the next token depends only on the current token.

Also be careful about what exactly is being counted. You want transitions in the final indexed sequence, not a mismatch between preprocessed and postprocessed token collections.

## What the real lesson is

This problem is teaching you how probabilistic structure emerges from counts.

A transition matrix is just empirical conditional probability estimated from sequential data.

---

# Problem 5. Density estimation with normalizing flows

## Clean restatement

You are given a data-generating process in two dimensions. Your task is to:

- sample data from it and visualize the shape,
- define a simple two-dimensional base distribution,
- define an invertible transformation,
- build the transformed distribution,
- train the transformation parameters by maximizing log probability on sampled data,
- and compare the initial and trained flow samples to the target data.

## What mathematical object you start with

You start with samples from an unknown target distribution in two dimensions.

The goal is density modeling.

A normalizing flow approaches this by starting from a simple base distribution, such as a standard Gaussian, and then applying a flexible invertible transformation so that the transformed density can match the target data distribution more closely.

## Reasoning path

First inspect the target data visually.

This matters because the whole point of the problem is to learn a distributional shape. The scatterplot tells you what kinds of geometric features the model needs to capture.

Second define the base distribution.

The base should be simple and known. The point is not to match the target immediately. The point is to give the model an easy starting density that the transformation can warp.

Third define the transformation and combine it with the base into a transformed distribution.

At this stage, before training, the transformed distribution is just whatever shape the initial parameters imply. So the initial sample plot is not expected to match the target data.

Fourth train by maximizing log probability on fresh samples from the target generator.

The negative mean log probability is the loss. Minimizing it means making the model assign higher probability to the observed data.

Fifth sample from the trained model and compare the scatterplot to the target data.

The goal is not perfect visual identity. The goal is whether the trained flow captures the main geometric structure of the target distribution substantially better than the base distribution and the untrained flow.

## Why log probability appears

A density model is trained by maximizing likelihood or log likelihood because that is the natural way to prefer parameter settings that make the observed data more plausible under the model.

The logarithm is used because products over many data points become sums, which are easier to optimize and interpret numerically.

## What the real lesson is

This problem is where several strands of the course come together:

- density modeling,
- change of variables,
- parameterized transformations,
- and probabilistic training objectives.

---

# Part IV. How to use this document without turning it into passive reading

For each problem, do not move on until you can answer these questions in your own words.

## Problem 1 self-checks

- What is the scope of the current factor?
- Which variable am I fixing?
- Which variable am I summing out?
- At which step does normalization happen?
- What probabilistic identity am I testing when I compare the original joint to the product factorization?

## Problem 2 self-checks

- What is the parent set of each variable?
- Why must the sampling order follow the graph?
- What does one full sample represent?
- Why should empirical frequencies approximate the target probabilities?

## Problem 3 self-checks

- What is the unique path between the two variables?
- Which three-node patterns appear on that path?
- Which observed variables block or open the path?
- Why is a collider different from a chain or fork?

## Problem 4 self-checks

- What is the state space of the Markov chain after preprocessing?
- What exactly does one row of the transition matrix mean?
- Why must each row sum to one?
- Why does sequence generation become repeated conditional sampling?

## Problem 5 self-checks

- What is the role of the base distribution?
- What is the role of the invertible transformation?
- Why is the transformed density still computable?
- What exactly is the loss trying to improve?

---

# Part V. Suggested study order from here

1. Read the pyGMs lecture section in this document.
2. Do Problem 1 first.
3. Read the Pyro lecture section in this document.
4. Do Problem 2 and then Problem 3.
5. Do Problem 4.
6. Only after that, revisit transformed densities and then do Problem 5.

This order works because it moves from the most concrete discrete table manipulations to the heaviest continuous density-modeling problem.

If you get stuck, return to the question:
What mathematical object do I currently have, and what operation is the problem actually asking me to perform on it?

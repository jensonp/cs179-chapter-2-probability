# HW2 Master Study Guide

This is the one document to read for Homework 2.

It replaces the scattered notes, bridge files, and catch-up files with one study path. It is designed to help you understand and complete the homework, not to function as a copy-paste answer key.

The guiding question for the entire homework is:

**What mathematical object do I have right now, and what operation is the problem asking me to perform on it?**

If you keep that question in front of you, the homework becomes much more manageable.

---

# 1. What to do first

Do the homework in this order:

1. Problem 1
2. Problem 2
3. Problem 3
4. Problem 4
5. Problem 5

That order is not arbitrary.

Problem 1 teaches you how to manipulate discrete probability tables in pyGMs.  
Problem 2 turns a Bayesian network into a generative story in Pyro.  
Problem 3 teaches you how to reason about influence in a Bayes net from the graph alone.  
Problem 4 turns counts into a Markov model.  
Problem 5 is the heaviest problem because it combines transformed densities, Pyro, and training.

So the right strategy is to move from the most concrete table manipulations to the most abstract density-modeling task.

---

# 2. What you actually need from pyGMs

## Why pyGMs is in this homework

pyGMs is not a separate subject you need to master before starting the homework. In Homework 2, pyGMs is mainly a way to represent and manipulate discrete probability tables.

The clean mental model is:

- a variable tells you which random quantity you are talking about and how many states it has,
- a factor is a table over one or more variables,
- and most operations are just table manipulations with probabilistic meaning.

## Variables

A pyGMs variable has:

- an integer ID,
- and a number of possible values.

This matters because the library tracks variables by ID, not by your Python nickname for them.

If you call a variable `T`, that name is for you.  
Inside pyGMs, the variable is identified by its numeric ID.

You should also know that factors are organized according to variable IDs, not according to the casual order you happened to type things.

That is one of the easiest places to make a mistake.

## Factors

A factor is a function over a scope of variables.

Examples:

- one binary variable -> a length-2 table
- two binary variables -> a 2 x 2 table
- three binary variables -> a 2 x 2 x 2 table

A factor is not automatically a probability distribution. It is just a table of values indexed by assignments.

It becomes a joint probability distribution only if the whole table sums to one.  
It becomes a conditional probability table only if the right normalization condition holds for each fixed conditioning assignment.

That distinction matters because in the homework you will often create intermediate factors that are not yet final probability distributions.

## Scope

The scope of a factor is the set of variables it depends on.

This is one of the most important ideas in the homework.

If a factor has scope `(T, D, C)`, then every entry refers to one assignment of those variables.

When you:
- condition on one variable,
- sum out one variable,
- or divide by a marginal,

you are changing either the scope or the interpretation of the factor.

Always ask:
1. What variables are in scope?
2. What does this factor mean probabilistically?

## The three operations you need most

### Conditioning or slicing

Conditioning means fixing some variable values and keeping only the entries consistent with that evidence.

If you fix `T = 1` in a factor over `(T, D, C)`, you are keeping only the entries where `T = 1`.

This does not automatically mean you have a normalized conditional probability.  
At this point, you have only restricted the table.

### Summing out variables

Summing out is marginalization.

If you sum out `D` from a factor over `(T, D, C)`, you are adding over the possible values of `D` and producing a smaller factor over the remaining variables.

This is the central operation behind marginals.

### Normalizing or dividing

A conditional distribution is usually built by taking a joint-like factor and dividing by the right marginal.

So if you want `p(C | T = 1)`, the natural path is:

- restrict to `T = 1`,
- sum out variables you do not want,
- divide by the total mass so the result sums to one over `C`.

That is the deep point:
a conditional is not a magical new object. It is a correctly normalized factor derived from a joint factor.

## Factor arithmetic

When you multiply factors, you are forming a new function over the union of their scopes.

When you divide factors, you are comparing assignments across matching scopes in a way that often produces a conditional-like object when the denominator is the right marginal.

The important thing is not the syntax. The important thing is to know whether the arithmetic you are doing matches the probability identity you are trying to express.

## The most common pyGMs mistakes

### Mistake 1: forgetting internal ordering
Factors are organized by variable IDs, not the order you casually typed.

### Mistake 2: confusing restriction with normalization
A restricted table is usually not yet a proper conditional distribution.

### Mistake 3: summing out the wrong variable
Always stop and ask which variables should remain in the scope when you are done.

### Mistake 4: forgetting what the factor means
Do not just push operations through. Keep naming the factor in words:
“this is a joint,” “this is a restricted subtable,” “this is a marginal,” “this is a conditional.”

---

# 3. What you actually need from Pyro

## Why Pyro is in this homework

Pyro is being used in two different ways.

In Problem 2, it expresses a generative Bayesian network.  
In Problem 5, it expresses a transformed continuous distribution.

So the right mindset is not “I need to learn a large framework.” The right mindset is:

- in Problem 2, Pyro lets me write the generative story directly,
- in Problem 5, Pyro lets me define a base distribution, a transformation, and a trainable transformed density.

## Problem 2 use: sampling from a graph

In a Bayesian network, children depend on parents.

So if the graph says:
- `C` influences `S`,
- `C` influences `R`,
- and `R` and `S` jointly influence `W`,

then the sampling order must be:

1. sample `C`,
2. sample `S` given `C`,
3. sample `R` given `C`,
4. sample `W` given `R` and `S`.

One full run gives one full joint sample.

If you repeat the model many times, you get empirical frequencies that approximate the model’s probabilities.

## Problem 5 use: transformed distributions

In the flow problem, the structure is:

- start with a simple base distribution,
- apply an invertible transformation,
- get a richer transformed distribution,
- train the transformation so the resulting density better matches the target data.

So in Problem 5, Pyro is not mainly about a graph. It is about a change-of-variables model whose density stays computable.

---

# 4. One conceptual warning before Problem 5

Problem 5 sits on top of one difficult idea: change of variables for densities.

If this feels slippery, the main thing to remember is this:

A transformation acts on the variable values, not directly on the old density formula.

If `X = f(Z)`, then the map sends values of `Z` to values of `X`.

The density of `X` has to be recomputed because the transformation can stretch or compress neighborhoods of the space.

The key principle is probability conservation:
the same small probability is being described in two coordinate systems, so the density has to adjust when local widths or volumes change.

In one dimension, that correction shows up as an absolute derivative.  
In several dimensions, it becomes a determinant.

If that still feels abstract, do not panic. For Homework 2, the most important practical takeaway is:

- the base distribution is simple,
- the transform makes it more flexible,
- and the resulting density remains trainable because the change-of-variables correction is computable.

---

# 5. Problem 1 study path: Factor tables in Python

## Clean restatement

You are given a full joint distribution over three binary variables in the Dentist example.

You must:

- extract subtables by fixing evidence,
- compute marginals by summing out variables,
- form conditionals by normalization,
- and test a conditional-independence factorization numerically.

Then you repeat the same kind of work using an empirical estimate from sampled data.

## What object you start with

You start with a full joint distribution over `(T, D, C)`.

In pyGMs, that is one factor over the scope `(T, D, C)`.

Each table entry means:
the probability of one full assignment of all three variables.

So treat the original factor as the truth table for the whole model.

## Problem 1.1

### What is being asked

You are not being asked to jump directly to `p(C | T = 1)`.  
You are being asked to expose the intermediate objects.

That means:

1. restrict to `T = 1`,
2. sum out `D`,
3. normalize over `C`.

### Reasoning path

First, fix `T = 1`.

At this point, you have not yet formed a conditional probability. You have only restricted the full joint table to assignments consistent with `T = 1`.

Second, sum out `D`.

Now you are removing the variable you no longer care about. This produces a factor over `C` that still represents joint mass involving `T = 1`.

Third, normalize.

Now divide by the total mass associated with `T = 1` so the resulting factor over `C` sums to one.

That gives `p(C | T = 1)`.

### What to check

At the end, the values over `C` must sum to one.

If they do not, you either normalized incorrectly or summed out the wrong variable.

## Problem 1.2

### What is being asked

You are being asked to verify the conditional-independence claim

`D` is independent of `T` given `C`.

The corresponding factorization is:

`p(T, D, C) = p(C) p(D | C) p(T | C)`.

The question is asking you to build the right-hand side and compare it to the original joint.

### Reasoning path

Compute:

- `p(C)` by summing out `T` and `D`,
- `p(D | C)` from the joint over `(D, C)` divided by `p(C)`,
- `p(T | C)` from the joint over `(T, C)` divided by `p(C)`.

Multiply those factors.

Now compare the product factor to the original joint factor.

If conditional independence really holds, the reconstructed factor and the original joint should match up to numerical precision.

### What the comparison means

The error is not just a number to report.

It is testing whether a statement in words
“independent given”
really corresponds to a factorization identity at the table level.

That is a major theme in graphical models.

## Problem 1.3

### What is being asked

Now you estimate the joint from sampled data instead of taking the true joint as directly known.

Then you compare two approximations to the true joint:

- the raw empirical estimate,
- the structured factorized estimate built from `p_hat(C)`, `p_hat(D | C)`, and `p_hat(T | C)`.

### Reasoning path

First count occurrences of each full assignment.

That gives raw counts.

Second convert counts into an empirical factor.

If smoothing is used, understand why: it prevents zero-probability issues that can break later calculations, especially KL divergence.

Third compute the empirical marginals and conditionals.

Fourth build the factorized approximation.

Then compare both:
- raw empirical estimate versus true joint,
- factorized estimate versus true joint.

### What the real lesson is

This is a model-structure lesson.

The raw empirical estimate is more flexible but noisier.  
The factorized estimate is more constrained but can generalize better if the structural assumption is good.

---

# 6. Problem 2 study path: Wet Grass model in Pyro

## Clean restatement

You are given a four-variable Wet Grass Bayesian network and explicit Bernoulli probabilities.

You must:

- express the generative model,
- draw many samples,
- estimate some marginal probabilities,
- and estimate one joint event probability.

## What object you start with

You start with a graph and its factorization:

`p(C, S, R, W) = p(C) p(S | C) p(R | C) p(W | R, S)`.

The Pyro model is just the graph written as a sampling story.

## Reasoning path

Parents must be sampled before children.

So the logical order is:

1. sample `C`,
2. sample `S` using the probability appropriate for that sampled value of `C`,
3. sample `R` using the probability appropriate for that sampled value of `C`,
4. sample `W` using the probability appropriate for the sampled pair `(R, S)`.

Once you have many samples, every requested probability becomes an empirical frequency.

### Example of the logic

To estimate `p(S = 1, R = 1)`:
count how many samples satisfy both conditions at once, then divide by the total number of samples.

## What to check

Your estimates should be close to the target probabilities, but not exactly equal because sampling is finite.

If one is wildly wrong, suspect the generative structure first.

---

# 7. Problem 3 study path: Building Power Bayes net

## Clean restatement

You are given a polytree and asked whether observing one variable can affect your belief about another.

This is a graph-reasoning problem, not a numerical probability-computation problem.

## What object you start with

You start with a directed acyclic graph.

Because it is a polytree, any two nodes are connected by exactly one undirected path.

That simplifies everything.

To decide whether information can flow, inspect that one path.

## The only method you need

Look at the unique path.

Then inspect each local three-node pattern:

- chain,
- fork,
- collider.

Rules:

- chain or fork: observed middle node blocks, unobserved middle node leaves path open
- collider: unobserved collider blocks, but observing the collider or one of its descendants opens the path

That is the whole method.

## How to answer each question

1. Find the unique path.
2. Label each three-node pattern.
3. Check which nodes are observed.
4. Decide whether the full path is active or blocked.

If active, say yes and name the path.  
If blocked, say no and identify the blocking point.

## What the real lesson is

A Bayesian network is not only a factorization device. It is also a reasoning device.

The graph itself tells you what kinds of informational influence are possible.

---

# 8. Problem 4 study path: Bigram text models

## Clean restatement

You are given a text corpus.

You must:

- preprocess it,
- reduce the vocabulary,
- estimate a transition matrix,
- answer a next-word question,
- and generate sample sequences.

## What object you start with

You start with one long sequence of words.

After preprocessing and vocabulary restriction, that becomes one long sequence of integer states.

At that point the model is a first-order Markov chain.

The key object is the transition matrix `T`, where `T[i, j]` is the probability of going from word `i` to word `j`.

## Reasoning path

First preprocess the corpus.

This defines the state space. Lowercasing, punctuation removal, and rare-word replacement are not just data cleaning. They define what the model’s states are.

Second build the reduced vocabulary.

Frequent words stay separate. Rare words are merged into the `?` token.

That is a modeling choice: less detail, more stability.

Third count adjacent pairs.

Each consecutive pair of tokens increments one transition count.

Fourth normalize rows.

Each row corresponds to a current word, so each row must become a conditional distribution over the next word.

Once the rows are normalized, you can:
- answer the “most likely followers of `miss`” question by inspecting the relevant row,
- and generate sequences by repeated conditional sampling.

## What to pay attention to

Be careful that the counts come from the final indexed token sequence, not from an earlier inconsistent token list.

## What the real lesson is

A Markov model is just conditional probability over transitions estimated from sequential counts.

---

# 9. Problem 5 study path: Density estimation with normalizing flows

## Clean restatement

You are given a synthetic two-dimensional data generator.

You must:

- sample from it and plot the result,
- define a simple base distribution,
- define an invertible transformation,
- form the transformed distribution,
- train the transform parameters by maximizing log probability,
- and compare the trained model visually to the target data.

## What object you start with

You start with samples from an unknown target distribution.

The goal is to build a density model.

A normalizing flow does this by:

- starting from a simple base density,
- applying an invertible transformation,
- and using the transformed density as the model.

## Reasoning path

First inspect the data scatterplot.

This tells you what geometric features the model needs to capture.

Second define the base distribution.

The base is intentionally simple. Its job is not to match the target immediately.

Third define the transformation and combine it with the base.

Before training, the transformed distribution is just the initial model, not yet a good fit.

Fourth train by maximizing log probability on sampled data.

The negative mean log probability is the loss.

Minimizing it means making the model assign higher density to the observed data.

Fifth sample from the trained model and compare the scatterplot to the target.

The goal is not perfect visual identity. The goal is whether the trained flow captures the major structure substantially better than the base and the untrained flow.

## Why log probability appears

Likelihood is the natural objective because it prefers parameter settings that make the observed data more plausible under the model.

The logarithm turns products into sums and is numerically easier to work with.

In flow models, the log density is especially natural because it combines the base log density and the Jacobian correction cleanly.

## What the real lesson is

Problem 5 is where density modeling, change of variables, parametrized transformations, and probabilistic training all come together.

It is the heaviest problem in the homework. Treat it that way.

---

# 10. What to do when stuck

If you get stuck on any problem, do not immediately ask “what line of code am I missing?”

Ask these questions first:

1. What mathematical object do I have right now?
2. What variables are in scope?
3. Is this a joint, a restricted table, a marginal, a conditional, a graph, a transition matrix, or a transformed density?
4. What operation is the problem asking for?
5. What should the result mean when I am done?
6. What basic sanity check should the result satisfy?

That habit will save you more time than memorizing syntax.

---

# 11. The shortest practical reading plan

Read this document in pieces, not all at once.

Right now:
- read sections 2 and 5,
- then do Problem 1.

After that:
- read section 3 and section 6,
- then do Problem 2.

Then:
- read section 7,
- then do Problem 3.

Then:
- read section 8,
- then do Problem 4.

Finally:
- read section 4 and section 9,
- then do Problem 5.

This is the fastest route with the least wasted reading.

---

# 12. Final advice

This homework is very manageable if you keep the object-level view clear.

Problem 1 is table manipulation.  
Problem 2 is graph-as-generative-story.  
Problem 3 is active-path reasoning.  
Problem 4 is empirical conditional probability from sequential counts.  
Problem 5 is transformed-density modeling with training.

If you keep translating each library step back into probability language, the homework stops feeling like five unrelated tasks and becomes one coherent sequence.

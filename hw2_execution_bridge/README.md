# HW2 Execution Bridge

## What this document is for

This file is the front-door document for Homework 2. It is not another theory chapter. It is the bridge between:

- the repo's theory notes,
- the HW2 PDF and code template,
- and the extra library-specific knowledge the homework silently expects.

Use it to decide:

- what to read first,
- what the repo does not fully teach,
- what external resources matter,
- what files are worth patching,
- and what failure points to watch for while implementing the problems.

---

## The shortest reading order that supports the homework

Do **not** read the repo straight through. Read only the pieces that directly support the five problems.

### Phase 1: support Problem 1 first

1. `02_probability_03_joint_tables_conditioning_bayes_and_total_probability`
2. `02_probability_04_expectation_variance_covariance_and_independence`

Why this comes first:

Problem 1 is about finite discrete tables, restricting to evidence, summing out variables, normalizing, and checking conditional independence. Those are exactly the ideas you need before touching `pyGMs` factors.

### Phase 2: support Problems 2 and 3

Read `03_bayesnet_main`, but not in a single uninterrupted pass. Read it in this order:

1. `3.1 Basic semantics`
2. `3.2 Independence relations`
3. `Three local path patterns to understand first`
4. `3.2.2 Markov blankets`
5. `3.2.3 Inference queries`

On a first pass, **skip `3.2.1 Equivalent graphs`**.

Why this order is better:

Problems 2 and 3 need you to understand what a Bayes net means, when information can flow, how observation changes relevance, and how conditional independence becomes a path question. `Equivalent graphs` is not the most urgent concept for HW2 and tends to interrupt the more important reasoning chain.

### Phase 3: support Problem 4

Still inside `03_bayesnet_main`, read:

- `3.4.2 Markov chains`

Why this belongs here:

Problem 4 is a bigram model, which is a first-order Markov chain over words. You need the conceptual model before you worry about frequency counts and sampling.

### Phase 4: support Problem 5

Read in this order:

1. `02_probability_09_change_of_variable_models`
2. the opening object map and likelihood/log-likelihood parts of `02_probability_06_learning_and_parameter_estimation`

Read `02_probability_05_continuous_random_variables` **only if** density language still feels unstable.

Why this order is better:

Problem 5 is really about one core idea: start with a simple base density, apply an invertible transformation, account for the Jacobian, and train the transformation by maximizing log-likelihood. `02_probability_09` gives the conceptual model. `02_probability_06` tells you how to think about training and log-likelihood. You do not need the whole estimation chapter before you start HW2.

### Phase 5: use the computational appendix only as needed

Use `02_probability_computational_appendix` surgically:

- finite probability tables alongside Problem 1,
- likelihood / log-likelihood alongside Problem 5,
- Jacobian and numerical checks only if change-of-variable reasoning still feels slippery.

Do **not** treat the appendix as the main conceptual lesson.

---

## Problem-by-problem dependency map

### Problem 1: Factor tables in Python

Primary repo sections:

- `02_probability_03_*`
- `02_probability_04_*`

Additional knowledge the repo does not fully supply:

- what a `pyGMs` `Factor` object is,
- how factor scope is defined by variable identity,
- how restriction, summation, multiplication, and division act on factor tables,
- why variable order and variable IDs matter when indexing or counting samples.

External resource that really helps:

- the `pyGMs` notebooks linked in the HW2 PDF.

### Problem 2: Bayesian network in Pyro

Primary repo sections:

- `03_bayesnet_main` through `3.2.3`

Additional knowledge the repo does not fully supply:

- what a Pyro model is as a stochastic program,
- what one execution of a model means,
- why sample order follows DAG parent structure,
- how repeated runs produce empirical probability estimates.

### Problem 3: Building Power Bayes net

Primary repo sections:

- `3.2 Independence relations`
- `Three local path patterns`
- `3.2.2 Markov blankets`
- `3.2.3 Inference queries`

Additional knowledge the repo does not fully supply:

- how to slow down d-separation reasoning into one-path-at-a-time checks,
- how to explain why a path is blocked rather than just naming the rule.

Important reminder:

This problem is fundamentally graphical reasoning, not a coding problem.

### Problem 4: Bigram text models

Primary repo sections:

- `3.4.2 Markov chains`
- optionally the categorical-estimation pieces of `02_probability_06`

Additional knowledge the repo does not fully supply:

- how to turn a token stream into a count matrix,
- how row-normalization converts counts into conditional probabilities,
- how to interpret `T[w_{t-1}, w_t]` as “next word given previous word.”

### Problem 5: Normalizing flows

Primary repo sections:

- `02_probability_09_*`
- the likelihood/log-likelihood parts of `02_probability_06_*`

Additional knowledge the repo does not fully supply:

- what a Pyro `TransformedDistribution` represents,
- the difference between a base distribution and a learned transform,
- why `log_prob` is the training objective,
- how two-dimensional event shapes differ from batches of samples,
- why the assignment only wants the four scatterplots rather than a symbolic density derivation.

External resource that really helps:

- the Pyro normalizing flows example linked by the HW2 PDF.

---

## What the repo does not teach clearly enough for HW2

This is the true “gap” list.

### 1. `pyGMs` execution semantics

The repo explains table operations mathematically. HW2 expects you to perform those operations inside `Factor` objects. The missing bridge is not new probability theory. It is the meaning of the software object carrying that theory.

The key missing ideas are:

- a factor is a table-valued function over a variable scope,
- variable identity matters more than the order in which you casually write names,
- conditioning means restricting a table to the evidence slice,
- marginalization means summing out dimensions corresponding to variables,
- factor products align on shared variables automatically by scope.

### 2. Pyro as a generative-program object

The repo explains Bayesian networks and change-of-variable models conceptually, but HW2 uses Pyro to realize both.

The key missing ideas are:

- one model execution produces one joint sample,
- later random choices may depend on earlier sampled values,
- repeated model executions estimate marginals and joint events empirically,
- transformed distributions are still probability distributions, not just ad hoc samplers.

### 3. Shape and representation issues

The repo does not need to dwell on tensor semantics. HW2 does.

You need to keep straight:

- a single 2D flow sample is one event with two coordinates,
- many such samples form a batch,
- `log_prob(data)` evaluates one log density per sampled event,
- Pyro and PyTorch often return tensor scalars rather than plain Python numbers.

### 4. Homework-specific success criteria

The repo is about understanding. The assignment is about deliverables.

Important consequences:

- the submission is a PDF,
- code is support work, not the final artifact,
- Problem 3 does not need code,
- Problem 5 only requires the four scatterplots,
- the code template is incomplete on purpose, so not every needed object is spelled out.

### 5. Template and convention hazards

Watch for these:

- factor-table indexing assumes variable IDs and tuple order agree,
- empirical counting can go wrong if you forget which coordinate is which variable,
- the bigram preprocessing block should be read carefully rather than copied blindly,
- density-language mistakes in Problem 5 often come from weak support / Jacobian intuition rather than from coding syntax alone.

---

## External resources you should actually use

Use these exactly when they become relevant.

### Use during Problem 1

- the `pyGMs` notebooks linked in the HW2 PDF.

Why:

They show what a factor object looks like in practice, how printed tables are displayed, and how basic factor operations are expressed in that library.

### Use during Problem 5

- the Pyro normalizing flows example linked in the HW2 PDF.

Why:

It shows the exact object pattern the homework is asking you to instantiate:
base distribution -> transform -> transformed distribution -> training by negative log-likelihood.

Do not use those resources as substitutes for the repo theory. Use them as the missing execution layer.

---

## Which repo files are most worth patching

If you are improving the repo itself for future study, these are the high-value targets.

### 1. `03_bayesnet_main/README.md`

This is still the biggest conceptual bottleneck for HW2. It supports Problems 2, 3, and part of 4. It needs the most careful bridge paragraphs and ordering cleanup, especially in `3.2`.

### 2. `02_probability_09_change_of_variable_models/README.md`

This is the main support file for Problem 5. It compresses several conceptual jumps too tightly and benefits from slower scalar-to-multivariate-to-flow bridges.

### 3. `02_probability_06_learning_and_parameter_estimation/README.md`

This matters mostly for Problem 5, but it also matters because terms like parameter, estimate, fitted value, likelihood, and posterior are easy to carry vaguely. Those terms should be stabilized earlier and more clearly.

### 4. `02_probability_computational_appendix/README.md`

Keep it, but demote it into a workflow companion. The computational pieces that perform core conceptual work should be partially baked back into the lessons.

### 5. `02_probability_03_joint_tables_conditioning_bayes_and_total_probability/README.md`

This is the extra file most worth patching for HW2 Problem 1. The theory is there, but one bridge paragraph should connect the math to the actual discrete factor workflow the homework uses.

### 6. Add a new `hw2_reading_guide` or equivalent front-door file

The repo currently needs a homework-specific bridge. This document can play that role, but if the repo itself is being improved, a dedicated `hw2_reading_guide` or `hw2_execution_bridge` file would be ideal.

---

## Which homework workspace files deserve extra attention

### `cs179-hw2-code.py` and the notebook template

These are incomplete by design. Treat them as scaffolds, not as authoritative completed references.

### The Bigram block

Read the preprocessing and counting logic carefully. Make sure the token sequence being counted is actually the one you intend to count.

### The flow block

Focus on what object each line is creating:

- data distribution from `sample_data`,
- simple base distribution,
- trainable transform,
- transformed distribution,
- optimization loop over negative log-likelihood.

---

## How to actually use this document while doing HW2

Use this as a quick routing sheet.

1. Read this file first.
2. Open the exact repo sections for the current problem only.
3. When the repo gives the concept but not the software object, switch to the relevant external library example.
4. Return to the homework template and implement the minimum needed object.
5. Only open the computational appendix if a numerical workflow itself is the confusing part.

This keeps you from over-reading and losing the dependency chain.

---

## Final recommendation

Treat this file as the **front door** for Homework 2.

The repo remains the main source for conceptual understanding.
The HW2 PDF and template define the task.
The external `pyGMs` and Pyro examples supply the missing execution semantics.

That division of labor is the cleanest way to finish the assignment without getting buried in material that is real but not currently necessary.

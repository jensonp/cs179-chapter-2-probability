# Probability and Inference: Front Matter and Scope

This file rewrites the front matter and Section 2.1 into a tighter first-principles sequence.

This opening block should do one job well: teach the event-level foundations of probability, then show how random variables, discrete distributions, table operations, and basic summaries arise from those foundations.

## How to Use This Chapter

Read this main note first if you want the core concepts in a form that is operational and exam-usable. The emphasis is on what each object means, what it computes, and what assumptions are required before a formula is valid.

Use the supporting materials afterward:

- **Formal supplement** for theorem-style statements and tighter derivations.
- **Exercises** for direct computation drills and proof-style checks.
- **Computational appendix** for sampling, plotting, and numerical sanity checks.

## Scope Guide

The Chapter 2 material falls into three layers.

### Core probability language

You should be comfortable with:

- sample spaces, events, and random variables;
- unions, intersections, complements, and inclusion-exclusion;
- conditional probability and Bayes' rule;
- marginalization and joint tables;
- expectation, variance, covariance, and independence.

### Important distribution families

You should also know the Bernoulli, categorical, and geometric distributions well enough to read their PMFs, interpret their parameters, and use them in simple derivations.

### Later material in the chapter

Continuous variables, Gaussian models, Beta and Dirichlet distributions, likelihood, MLE, entropy, KL divergence, and Jacobians matter, but they belong to later sections. The goal of this opening block is to make the event-level and discrete foundations solid first.

## Notation Policy

Throughout the rewrite:

- `P(A)` or `\mathbb{P}(A)` means the probability of an event `A`.
- `X, Y, Z` denote random variables.
- `x, y, z` denote realized values.
- `p(X=x)` or `p(x)` denotes a PMF value when a discrete PMF exists.
- `F_X(x)` denotes a cumulative distribution function.
- `\Omega` denotes the sample space.

A formula is always interpreted together with its domain restrictions. If a formula only applies in the discrete setting, or only when a conditioning event has positive probability, or only under independence, that condition is stated explicitly.

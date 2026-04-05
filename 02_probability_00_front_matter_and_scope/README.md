# 00. Front Matter and Scope

This opening section is not filler. Its job is to tell the reader what kind of document this chapter is, how it should be studied, what the internal structure is, and what kind of mathematical maturity it expects.

A good front matter section does not merely announce topics. It gives the reader a map, a pace, and a method. That matters because probability and inference are easy to study badly. A student can memorize formulas, recognize a few patterns, and still never develop stable reasoning. This chapter is written against that failure mode. The goal is not fast recognition. The goal is durable understanding.

The notes are therefore organized as a layered chapter rather than a compressed reference. The chapter is meant to be read in order, because later sections depend on distinctions established earlier. If those earlier distinctions are skipped, later material can still look familiar, but it will remain fragile.

---

## 1. What this chapter is trying to do

Chapter 2 is about **probability and inference**. Those two words should not be collapsed too early.

- **Probability** studies how uncertainty is represented within a mathematical model once the model has been specified.
- **Inference** studies how observations update, constrain, or select models and parameters.

The first half of the chapter therefore builds the language of probability:
- sample spaces,
- events,
- random variables,
- distributions,
- conditioning,
- expectations,
- continuous models.

The second half moves toward inference:
- likelihood,
- estimation,
- Bayesian updating,
- model comparison,
- convexity as optimization background,
- information-theoretic quantities,
- and change-of-variable modeling.

That is the governing logic of the chapter. It is not a random list of topics. Each later section depends on the reader knowing what kind of object the earlier sections introduced.

---

## 2. How the chapter is organized

The chapter exists in two reading forms:

- a **one-file main note**, which presents the chapter as one continuous document;
- a **section-by-section version**, which exposes the same content as separate topic folders.

The section-by-section order is:

1. front matter and scope
2. probability spaces, events, and random variables
3. discrete PMFs, indicators, and geometric/Bernoulli/categorical models
4. joint tables, conditioning, Bayes’ rule, and total probability
5. expectation, variance, covariance, independence
6. continuous random variables, CDF/PDF distinctions, Gaussian families, Beta and Dirichlet
7. learning and parameter estimation
8. convexity
9. information theory
10. change-of-variable models

This order should be respected unless the reader is using a homework-specific guide. The chapter is cumulative.

### Why the order matters

Probability notes often become hard to learn from when they mix three levels without warning:

- event-level reasoning,
- distribution-level reasoning,
- and model/inference-level reasoning.

This chapter tries to prevent that by introducing one layer at a time. If the reader skips ahead, it is very easy to confuse:

- an outcome with an event,
- a random variable with a distribution,
- a probability with a likelihood,
- a density with a probability,
- a prior with a posterior,
- correlation with independence.

The section order is designed to keep those distinctions stable.

---

## 3. What kind of notes these are

These are not intended as:

- exam cram notes,
- a minimal formula sheet,
- compressed lecture bullets,
- or a quick review guide.

They are intended as **study notes for mastery**.

That means the notes should do several jobs at once:

- state formal definitions and correct formulas,
- explain what each object means,
- say what is fixed and what varies,
- identify hidden assumptions,
- warn about common confusions,
- and connect each section to later modeling or inference use.

If a reader wants only a quick checklist for review, these notes will feel too long. That is acceptable. The chapter is optimized for understanding, not compression.

---

## 4. How to read the chapter

A good way to study these notes is to separate three passes.

### First pass: structure and objects

On the first pass, the goal is not to memorize formulas. The goal is to identify the main objects of each section.

For each section, ask:
- What kind of object is being introduced?
- What question does it answer?
- What does it act on?
- What is fixed and what is varying?
- What later section will use it?

On this pass, it is fine if some derivations are not yet automatic. The important thing is to know what each construction is for.

### Second pass: formal relationships

On the second pass, the reader should tighten the mathematical relationships:
- how a probability measure acts on events,
- how a random variable induces a distribution,
- how conditioning changes a distribution,
- how expectations and variances summarize it,
- how likelihood differs from probability,
- how KL differs from entropy,
- and how Jacobians preserve mass.

This is the pass where formulas should become structurally meaningful rather than just familiar.

### Third pass: worked problems and transfer

On the third pass, the reader should test whether the concepts transfer:
- Can I set up the right probability space?
- Can I translate a verbal claim into an event?
- Can I identify whether I need Bayes, total probability, or conditioning?
- Can I tell whether a quantity is a probability, density, likelihood, posterior, or divergence?
- Can I detect hidden assumptions?
- Can I explain why a formula is valid, not just use it?

That is the pass where exercises and computational checks become most valuable.

---

## 5. How to use the companion materials

The repository includes three companion documents besides the main note.

### Formal supplement

The formal supplement is for:
- concise theorem statements,
- definitions in more distilled form,
- proof skeletons,
- and the logical spine behind the main text.

It should **not** be the first document a student reads unless the student already understands the chapter conceptually. It is best used after the corresponding main section has been read carefully.

### Exercises

The exercises are where understanding is tested. They should be used shortly after reading each section, not only at the very end of the chapter.

Exercises are especially important for checking whether the reader can:
- set up events correctly,
- move between tables and formulas,
- perform conditioning in the right order,
- and interpret model assumptions correctly.

### Computational appendix

The computational appendix is for numerical workflows, sanity checks, simulations, and plotting. It is not a replacement for the main note. Its job is to make the mathematics operational:
- sampling,
- table calculations,
- numerical verification,
- visualization,
- and computational translation of formulas.

That appendix is most useful after the reader already understands what quantity is being computed and why.

---

## 6. Notation policy

One of the easiest ways to lose clarity in probability is to let notation drift. These notes keep the following conventions stable.

### Probability of events

Probability of an event is written as

$$
P(A)
\quad\text{or}\quad
\mathbb{P}(A).
$$

Here, $A$ is an event — a set of outcomes.

### Random variables and realized values

Random variables are written with uppercase letters such as

$$
X,\;Y,\;Z.
$$

Realized values are written with lowercase letters such as

$$
x,\;y,\;z.
$$

So

$$
P(X=x)
$$

means the probability of the event that the random variable $X$ takes the value $x$.

### PMFs, PDFs, and CDFs

When appropriate:

- $p(x)$ denotes a probability mass function or density, depending on context;
- $F_X(x)$ denotes a cumulative distribution function.

These are **not** interchangeable objects. A PMF gives probabilities of exact values in the discrete setting. A PDF gives density, not point probability, in the continuous setting. A CDF gives cumulative probability and exists much more generally.

### Parameters

Model parameters are usually written as symbols such as

$$
\theta,\;\rho,\;\mu,\;\sigma^2,\;\pi.
$$

The notes will always try to say explicitly whether a parameter is being treated as:
- fixed but unknown,
- varying under likelihood,
- or random under a Bayesian model.

This distinction is crucial for later sections.

---

## 7. Expected background

The chapter assumes the reader is comfortable with:
- basic algebra,
- functions and inverses,
- finite sums,
- the idea of derivatives and integrals,
- and matrix notation at an introductory level.

The chapter does **not** assume prior mastery of probability. But it does expect the reader to tolerate formal structure and to distinguish carefully among several kinds of mathematical objects.

That is why the notes sometimes spend substantial space on distinctions that may look obvious at first glance. In probability, those distinctions are often what prevent later mistakes.

---

## 8. Common failure modes the reader should avoid from the start

A serious front matter section should warn about the mistakes that cause trouble later.

### Failure mode 1: treating all formulas as if they mean the same kind of thing

A student may see
- a PMF,
- a density,
- a likelihood,
- a posterior,
- a KL divergence,

and treat them all as “some probability expression.” This is fatal for real understanding. Each object answers a different question.

### Failure mode 2: skipping object-level meaning

Many students try to learn probability by memorizing manipulations:
- condition here,
- sum there,
- apply Bayes here,
- differentiate there.

This works briefly, then fails. The chapter should always be read by asking what kind of object is on the page and what operation is being performed on it.

### Failure mode 3: confusing notation compactness with understanding

A small formula is not necessarily an easy concept. For example,
- $P(A\mid B)$,
- $\mathbb{E}[X]$,
- $\nabla^2 f(x)\succeq 0$,
- $D(p\|q)$,

are all compact notations for ideas that need careful interpretation. These notes aim to slow that process down enough for real comprehension.

---

## 9. What “mastery” means in this chapter

A mastery-level reader of this chapter should eventually be able to do all of the following.

### Structural understanding
- identify the correct underlying space,
- translate verbal claims into events,
- distinguish random variables from their distributions,
- recognize what object is being computed in each formula.

### Computational understanding
- compute probabilities, marginals, conditionals, expectations, variances, and posterior updates correctly,
- move between event definitions, tables, and formulas,
- handle continuous integrals and Jacobian corrections correctly.

### Conceptual understanding
- explain why a formula is valid,
- state what assumptions are needed,
- identify when common shortcuts fail,
- compare neighboring ideas without confusion.

### Transfer
- reuse the ideas in later machine learning contexts,
- understand why likelihood and posterior are different,
- understand why entropy and KL are different,
- understand how Gaussian geometry and change-of-variable models matter for real modeling.

That is the standard these notes are aiming at.

---

## 10. How to use this front matter correctly

This section should not be memorized. It should be used as a standing reference for how to study the rest of the chapter.

A good habit is to keep asking, in every later section:

- What is the object here?
- What problem is it solving?
- What assumptions are active?
- What is the most common confusion?
- What later sections will rely on this?

If the reader studies with those questions in mind, the chapter becomes much more coherent.

---

## 11. Retain from 00

- The chapter is structured cumulatively, not as a bag of independent topics.
- The notes are written for mastery, not compressed review.
- The main note should be read first; the supplement, exercises, and computational appendix have different roles.
- Stable notation and object-level distinctions matter from the start.
- A reader should always ask what kind of object is being introduced and why.

## 12. Do not confuse in 00

- Do not confuse the main note with the formal supplement.
- Do not treat the computational appendix as the primary teaching document.
- Do not use the chapter as if it were a cheat sheet.
- Do not skip foundational sections just because later formulas look familiar.

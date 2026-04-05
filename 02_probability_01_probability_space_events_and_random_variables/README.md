# 2.1 Probability Spaces, Events, and Random Variables

This section is the real foundation of the chapter. Everything that comes later — Bayes’ rule, expectation, densities, likelihood, entropy, and inference — silently depends on a small collection of ideas introduced here. If these ideas stay blurry, later formulas can still be manipulated, but the reasoning will remain brittle. The goal of this section is therefore not just to state the formal definitions. The goal is to make clear what problem each definition solves, what each object is allowed to contain, and what conclusions each definition licenses.

There are four layers to keep distinct:

1. **The outcome space** tells us what can happen at the most concrete level.
2. **Events** are the collections of outcomes whose probabilities we ask about.
3. **The probability measure** assigns consistent probabilities to those events.
4. **Random variables** are functions that turn complicated outcomes into numerical quantities we actually want to analyze.

That order matters. A random variable is not the starting point. It is built on top of a probability space. Probability is not attached directly to arbitrary English-language claims. It is attached to events, and events are sets of outcomes inside a probability space. Once those boundaries are fixed, later reasoning becomes much cleaner.

---

## 1. Why probability spaces exist

Probability theory is often introduced through examples like coin flips, dice, cards, medical tests, or weather. Those examples are helpful, but they hide the structural issue probability spaces are designed to solve.

Whenever we speak probabilistically, we are doing three things at once:

- specifying what outcomes are possible,
- deciding which collections of outcomes are meaningful questions,
- and assigning numbers to those collections in a way that is globally consistent.

Without a formal structure, those three jobs blur together. The outcome “the die lands on 4,” the event “the die lands on an even number,” and the probability statement “the probability of an even number is 1/2” are different kinds of objects. A probability space exists to separate them cleanly.

A probability space is written as

$$
(\Omega,\mathcal{F},P).
$$

Each symbol plays a different role:

- $\Omega$ is the **sample space** or **outcome space**;
- $\mathcal{F}$ is the **collection of events** we allow ourselves to talk about;
- $P$ is the **probability measure** assigning probabilities to those events.

The rest of this section explains why all three pieces are needed.

---

## 2. The sample space $\Omega$

The sample space is the set of all possible elementary outcomes.

This definition is simple, but it does real work. It fixes the most detailed resolution at which the experiment is being described.

### Example: one die roll

If one fair six-sided die is rolled once, the natural sample space is

$$
\Omega = \{1,2,3,4,5,6\}.
$$

Each outcome names one fully resolved result of the experiment.

### Example: two coin flips

If a coin is flipped twice and order matters, then the sample space is not

$$
\{H,T\},
$$

because that ignores which flip occurred first. The right sample space is

$$
\Omega = \{HH, HT, TH, TT\}.
$$

This is an important early lesson: the sample space must be chosen at the level of detail required by the questions you plan to ask.

### Example: choosing the right level of detail

Suppose you only care how many heads occur in two flips. Then the variable of interest takes values in $\{0,1,2\}$. But that is **not** usually the sample space of the underlying experiment. It is the image of a random variable defined on the more detailed space

$$
\{HH,HT,TH,TT\}.
$$

This distinction matters because the random variable “number of heads” compresses several outcomes into one value. The underlying space and the derived numerical quantity are not the same object.

### What the sample space does and does not do

The sample space says what can happen. It does **not** yet say which groupings of outcomes will count as events, and it does **not** yet assign probabilities. Those are separate steps.

---

## 3. Events and the event collection $\mathcal{F}$

An **event** is a set of outcomes.

This is one of the most important conceptual shifts in the whole chapter. Probability is assigned to sets of outcomes, not directly to English sentences and not directly to random variables. A verbal claim becomes probabilistic only after it is translated into a set of outcomes.

### Example: die roll

Let

$$
\Omega = \{1,2,3,4,5,6\}.
$$

Then the statement “the die lands on an even number” corresponds to the event

$$
E = \{2,4,6\}.
$$

The statement “the die lands on a value at least 5” corresponds to

$$
A = \{5,6\}.
$$

The event “the die lands on 4” is the singleton set $\{4\}$.

So an event is not necessarily a single outcome. It can be any collection of outcomes for which we want to ask a probability question.

### Why not allow every possible subset automatically?

In finite examples like dice and cards, it is harmless to let the event collection be the full power set of $\Omega$. But in more general spaces, especially continuous ones, this needs care. Probability theory therefore isolates an event collection $\mathcal{F}$ that is closed under the operations required for consistent reasoning.

That closure is why the second component of a probability space is not merely “some events we happen to like.” It has to be a structured collection.

### The event collection must support complements and unions

If an event is meaningful, then its complement should also be meaningful. If two events are meaningful, their union should be meaningful. Otherwise probability identities such as

$$
P(A^c)=1-P(A)
$$

or inclusion-exclusion would have nowhere to live.

That is why $\mathcal{F}$ is chosen to satisfy closure properties.

---

## 4. Sigma-algebras: what $\mathcal{F}$ must contain

The event collection $\mathcal{F}$ is a **sigma-algebra** on $\Omega$. This means it satisfies three conditions:

1. $\Omega\in\mathcal{F}$.
2. If $A\in\mathcal{F}$, then $A^c\in\mathcal{F}$.
3. If $A_1,A_2,\dots\in\mathcal{F}$, then

$$
\bigcup_{n=1}^{\infty} A_n \in \mathcal{F}.
$$

From these three properties, many others follow automatically, including closure under countable intersections and finite unions.

### What each condition means

The first condition says the “certain event” is an allowed event.

The second says if a claim is measurable, then its negation is measurable.

The third says if we can speak probabilistically about each event in a countable family, then we can also speak about the event that at least one of them occurs.

These are not arbitrary technicalities. They are the exact closure rules needed so the usual algebra of probability is well defined.

### Finite spaces versus general spaces

In finite examples, the most common choice is

$$
\mathcal{F}=2^\Omega,
$$

the full power set of $\Omega$.

In continuous settings such as $\Omega=\mathbb{R}$, one usually does **not** take “every subset of $\mathbb{R}$” as an event. Instead one works with a carefully chosen sigma-algebra, most commonly the Borel sigma-algebra generated by intervals. That issue will matter more when continuous random variables and densities appear later, but this is where the reason first appears.

### What mastery requires here

You do not need to obsess over pathological set theory at this stage. But you do need to internalize one structural fact:

**Probability needs an event collection closed under the operations used in probability identities.**  
That is the real purpose of $\mathcal{F}$.

---

## 5. The probability measure $P$

Once the outcome space and event collection are fixed, a probability measure assigns probabilities to events.

Formally, a probability measure is a function

$$
P:\mathcal{F}\to[0,1]
$$

satisfying the Kolmogorov axioms:

1. **Nonnegativity**:

$$
P(A)\ge 0 \quad \text{for all } A\in\mathcal{F}.
$$

2. **Normalization**:

$$
P(\Omega)=1.
$$

3. **Countable additivity**: if $A_1,A_2,\dots$ are pairwise disjoint events, then

$$
P\!\left(\bigcup_{n=1}^{\infty} A_n\right)=\sum_{n=1}^{\infty} P(A_n).
$$

These three axioms are the whole formal foundation of probability.

### Why these axioms are the right ones

Nonnegativity says probabilities cannot be negative.

Normalization says the total probability of all possible outcomes is 1.

Countable additivity says if events are disjoint, then the probability that one of them occurs is the sum of their probabilities.

That third axiom is the engine behind almost every later identity. Without it, probability would not behave like “mass” spread across disjoint pieces of the space.

---

## 6. Immediate consequences of the axioms

A good mastery note should not merely list the axioms and move on. The first important consequences should be derived and interpreted.

### Probability of the empty event

Because

$$
\Omega = \Omega \cup \varnothing
$$

and the union is disjoint, countable additivity gives

$$
P(\Omega)=P(\Omega)+P(\varnothing).
$$

Therefore

$$
P(\varnothing)=0.
$$

So the impossible event has probability zero.

### Complement rule

If $A\in\mathcal{F}$, then $A$ and $A^c$ are disjoint and satisfy

$$
A\cup A^c=\Omega.
$$

So

$$
P(A)+P(A^c)=P(\Omega)=1,
$$

hence

$$
P(A^c)=1-P(A).
$$

This is the first example of why closure under complements matters.

### Monotonicity

If $A\subseteq B$, then $B$ can be written as the disjoint union

$$
B = A \cup (B\setminus A).
$$

So

$$
P(B)=P(A)+P(B\setminus A)\ge P(A).
$$

Thus larger events cannot have smaller probability.

### Inclusion-exclusion for two events

Any two events satisfy

$$
P(A\cup B)=P(A)+P(B)-P(A\cap B).
$$

The subtraction is necessary because outcomes in the overlap are counted twice in the raw sum.

This formula is the first place where event algebra matters directly. Probability identities are really set identities plus additivity.

---

## 7. Finite probability spaces

In finite settings, probability measures are especially concrete.

Suppose

$$
\Omega=\{\omega_1,\dots,\omega_n\}.
$$

To define a probability measure, it is enough to assign numbers

$$
p_i = P(\{\omega_i\})
$$

such that

$$ p_i\ge 0 \qquad\text{and}\qquad \sum_{i=1}^{n} p_i = 1. $$

Then every event $A\subseteq\Omega$ has probability

$$
P(A)=\sum_{\omega_i\in A} p_i.
$$

### Example: biased die

Let

$$
\Omega=\{1,2,3,4,5,6\}
$$

with

$$ P(\{1\})=0.10,\; P(\{2\})=0.10,\; P(\{3\})=0.15,\; P(\{4\})=0.15,\; P(\{5\})=0.20,\; P(\{6\})=0.30. $$

Then the event “roll at least 5” is

$$
A=\{5,6\},
$$

so

$$
P(A)=0.20+0.30=0.50.
$$

This is the concrete finite model behind the general axioms.

### Uniform finite spaces

A finite sample space is uniform if all singletons receive equal probability. If $|\Omega|=n$, then

$$
P(\{\omega\})=\frac1n
$$

for every outcome $\omega$, and therefore

$$
P(A)=\frac{|A|}{|\Omega|}.
$$

This counting rule is valid only because all elementary outcomes are equally likely. Students often overgeneralize this. It is a special case, not the general definition of probability.

---

## 8. Random variables

A random variable is a function

$$
X:\Omega\to\mathbb{R}.
$$

This definition looks innocent, but it solves a major practical problem. Real experiments often produce structured outcomes — sequences, configurations, paths, tables, assignments, graphs — while most statistical questions are about numerical summaries of those outcomes. A random variable is the device that turns the former into the latter.

### Example: number of heads in two flips

Let

$$
\Omega=\{HH,HT,TH,TT\}.
$$

Define the random variable $X$ by

$$ X(HH)=2,\qquad X(HT)=1,\qquad X(TH)=1,\qquad X(TT)=0. $$

Then $X$ is the “number of heads” random variable.

Notice what just happened:

- the sample space still contains four ordered outcomes;
- the random variable compresses them into the numerical values $0,1,2$;
- several distinct outcomes can map to the same number.

That is why a random variable is not the same as the sample space. It is a function defined **on** the sample space.

### Why the word “random” is slightly misleading

The function itself is not random in the usual sense. Once the experiment outcome $\omega$ is known, the value $X(\omega)$ is fixed. The randomness comes from the randomness of the underlying outcome. The variable is “random” only because its input is random.

---

## 9. Measurability: why random variables need a condition

A random variable is not just any function from $\Omega$ to $\mathbb{R}$. It must be **measurable**.

For this level of notes, the key condition is:

For every threshold $a$, the set

$$
\{\omega\in\Omega: X(\omega)\le a\}
$$

must be an event in $\mathcal{F}$.

This condition ensures that probability questions about $X$ can be translated back into probability questions about events in the underlying space.

### Why this condition is necessary

When we ask

$$
P(X\le a),
$$

we are really asking for the probability of the event

$$
\{\omega: X(\omega)\le a\}.
$$

If that set were not in $\mathcal{F}$, the question would not even be legally posed inside the probability space.

So measurability is not technical decoration. It is what makes random variables compatible with the underlying event system.

### What to remember

At this stage, the right mastery takeaway is:

**A random variable must turn numerical questions back into valid events.**

That is the operational content of measurability.

---

## 10. Events induced by random variables

Once a random variable is measurable, it generates new events automatically.

If $X$ is a random variable, then statements such as

- $X\le a$,
- $X=a$,
- $X\in B$,

all correspond to events in the underlying space.

### Example: parity of a die roll

Let $X(\omega)=\omega$ on

$$
\Omega=\{1,2,3,4,5,6\}.
$$

Then the event “$X$ is even” is

$$
\{\omega:X(\omega)\in\{2,4,6\}\}=\{2,4,6\}.
$$

This example looks trivial, but it shows the core mechanism: numerical claims about the random variable are really set claims about the underlying outcomes.

That mechanism becomes even more important when several random variables are defined on the same space, because joint statements such as

$$
X+Y\ge 3
$$

are also events in the background space.

---

## 11. Distribution induced by a random variable

A random variable pushes the probability measure on $\Omega$ forward to a probability distribution on the real line.

For a discrete random variable, the induced distribution is given by

$$
P(X=x)=P(\{\omega:X(\omega)=x\}).
$$

This is the probability mass function of $X$.

### Example: number of heads in two fair flips

Using

$$
\Omega=\{HH,HT,TH,TT\},
$$

with each outcome having probability $1/4$, and the random variable

$$
X(HH)=2,\quad X(HT)=1,\quad X(TH)=1,\quad X(TT)=0,
$$

we obtain

$$
P(X=0)=P(\{TT\})=\frac14,
$$

$$
P(X=1)=P(\{HT,TH\})=\frac12,
$$

$$
P(X=2)=P(\{HH\})=\frac14.
$$

This is the first full example of a random variable compressing multiple outcomes into one numerical distribution.

### What this shows

The distribution of a random variable is **derived** from the underlying probability space. It is not primitive. This matters because different probability spaces can induce the same marginal distribution for a variable, while supporting very different joint structures once more variables are added.

That is why probability spaces come first and distributions of random variables come second.

---

## 12. Multiple random variables on one probability space

The real power of probability spaces appears when several random variables are defined on the same underlying outcome space.

Suppose $\Omega$ is the set of all possible underlying outcomes, and define two random variables

$$ X:\Omega\to\mathbb{R}, \qquad Y:\Omega\to\mathbb{R}. $$

Then both variables are functions of the same underlying outcome. This is how dependence enters probability theory.

### Example: two flips

Let $\Omega=\{HH,HT,TH,TT\}$.

Define

- $X$ = indicator that the first flip is heads,
- $Y$ = indicator that the second flip is heads.

Then

$$
X(HH)=1,\; X(HT)=1,\; X(TH)=0,\; X(TT)=0,
$$

and

$$
Y(HH)=1,\; Y(HT)=0,\; Y(TH)=1,\; Y(TT)=0.
$$

Because $X$ and $Y$ are defined on the same underlying space, we can ask joint questions such as

$$
P(X=1,Y=0)=P(\{HT\})=\frac14.
$$

This is the structural source of joint distributions. They come from several measurable functions sharing one probability space.

---

## 13. Common confusions to eliminate now

### Confusion 1: outcome versus event

An outcome is a single elementary possibility. An event is a set of outcomes.

For a die roll:

- outcome: $4$,
- event: “even” = $\{2,4,6\}$.

Probability is assigned to events.

### Confusion 2: sample space versus random variable values

The sample space for two coin flips may be

$$
\{HH,HT,TH,TT\},
$$

while the random variable “number of heads” takes values in

$$
\{0,1,2\}.
$$

These are not the same object.

### Confusion 3: random variable versus event

A random variable is a function.  
An event is a set.

The statement “$X\le 1$” is an event induced by the variable $X$.

### Confusion 4: uniform counting formula versus general probability

The rule

$$
P(A)=\frac{|A|}{|\Omega|}
$$

holds only when the space is finite and all elementary outcomes are equally likely.

### Confusion 5: measurability as a useless technicality

Measurability is what guarantees that numerical questions about a variable correspond to valid events in the probability space.

If that translation fails, the probability question is not well posed.

---

## 14. A full worked example tying everything together

Consider the experiment “flip a fair coin twice.”

### Step 1: choose the sample space

Because order matters, set

$$
\Omega=\{HH,HT,TH,TT\}.
$$

### Step 2: choose the event collection

Since the space is finite, take

$$
\mathcal{F}=2^\Omega.
$$

So every subset is an event.

### Step 3: assign probabilities

Because the flips are fair and the four ordered outcomes are equally likely,

$$ P(\{\omega\})=\frac14 \qquad\text{for each }\omega\in\Omega. $$

### Step 4: define events

Let

$$
A=\{\text{at least one head}\}=\{HH,HT,TH\}.
$$

Then

$$
P(A)=\frac34.
$$

Let

$$
B=\{\text{exactly one head}\}=\{HT,TH\}.
$$

Then

$$
P(B)=\frac12.
$$

### Step 5: define a random variable

Let $X$ be the number of heads:

$$
X(HH)=2,\quad X(HT)=1,\quad X(TH)=1,\quad X(TT)=0.
$$

### Step 6: recover probabilities of the variable from events

Now

$$
P(X=0)=P(\{TT\})=\frac14,
$$

$$
P(X=1)=P(\{HT,TH\})=\frac12,
$$

$$
P(X=2)=P(\{HH\})=\frac14.
$$

### What this one example contains

This example already contains the whole architecture:

- a sample space,
- a sigma-algebra,
- a probability measure,
- events,
- a measurable random variable,
- and a derived distribution for that variable.

That is why this section is foundational. Every later construction is built by repeating this architecture in richer spaces.

---

## 15. How this section connects to the rest of the chapter

This section is not just formal setup. Each later section uses one of its pieces directly.

- **Discrete distributions** rely on random variables and induced probability mass functions.
- **Conditioning and Bayes’ rule** rely on event algebra and probability measures.
- **Expectation and variance** are summaries of random variables and their induced distributions.
- **Continuous variables and densities** rely on measurable spaces and event collections rich enough for intervals.
- **Likelihood and inference** treat observed data as realizations of random variables generated under probabilistic models.
- **Information theory** compares distributions induced by random variables.
- **Change-of-variable models** depend on measurable mappings between spaces.

So mastery here is not optional. If the difference among outcomes, events, variables, and distributions is not sharp now, later sections will feel like symbol manipulation instead of reasoning.

---

## 16. Retain from 2.1

- A probability space is a triple $(\Omega,\mathcal{F},P)$.
- $\Omega$ contains elementary outcomes.
- Events are sets of outcomes.
- $\mathcal{F}$ is a sigma-algebra so event operations stay inside the allowed event collection.
- $P$ assigns consistent probabilities through the Kolmogorov axioms.
- A random variable is a measurable function from outcomes to numbers.
- Numerical statements about a random variable correspond to events in the underlying space.
- The distribution of a random variable is induced from the probability space rather than assumed independently.

## 17. Do not confuse in 2.1

- Do not confuse an outcome with an event.
- Do not confuse the sample space with the value set of a random variable.
- Do not confuse a random variable with the event produced by a statement about it.
- Do not assume counting formulas apply outside uniform finite spaces.
- Do not treat measurability as optional; it is what makes probability statements about a variable legitimate.

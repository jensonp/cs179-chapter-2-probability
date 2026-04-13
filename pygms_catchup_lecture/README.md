# pyGMs Catch-Up Lecture for CS 179 HW2

## Why you are learning pyGMs at all

pyGMs is not mainly a “coding library” in the sense of hiding the probability ideas from you. It is closer to a structured way of manipulating the exact mathematical objects you have already seen in the notes: variables, joint tables, factors, conditionals, marginals, and products of smaller pieces.

So the right way to learn pyGMs is not to memorize commands. The right way is to keep one question in mind:

**What mathematical object am I holding right now, and what operation do I want to perform on it?**

If you keep that question in front of you, pyGMs becomes much easier.

For HW2, especially Problem 1, pyGMs is being used as a table-manipulation language. You are not yet being asked to master all of graphical-model inference. You mainly need to become comfortable with discrete variables, factors as tables over those variables, conditioning by fixing some variables, summing out variables to form marginals, and combining factors by arithmetic.

---

## The big mental model

pyGMs is built around one central idea:

A large probabilistic object can often be represented as a collection of smaller functions over smaller groups of variables.

Those smaller functions are called **factors**.

A factor does not have to be a normalized probability distribution. It is simply a function of one or more discrete variables. Sometimes that function is a joint distribution. Sometimes it is a conditional probability table. Sometimes it is just an unnormalized score function. The point is that it is a table indexed by variable assignments.

So when you use pyGMs, the most important shift is this:

- stop thinking “I have a magical model object”
- start thinking “I have functions over variables, represented as tables, and I am manipulating them carefully”

That is why the first notebook is called “Variables and Factors.” That is the true foundation.

---

## The first object: a variable

A pyGMs variable is not a Python variable name. It is a mathematical random variable together with two pieces of information:

- a unique global ID
- a number of states

This is the first thing to internalize.

When you write a Python name like $T$ or $C$, that is just your local handle for referring to the pyGMs variable object. The actual identity of the variable inside pyGMs is its integer label.

So there are really two layers:

- your local Python name, which is for your convenience
- the variable’s pyGMs identity, which is its global ID

That is why a variable can be printed as just a number. The number is the identity pyGMs actually uses.

The number of states matters because pyGMs assumes each variable takes values from a finite set, usually written like ${0, 1, ..., d-1}$.

For HW2 Problem 1, this is exactly what happens in the Dentist example. The variables are binary, so each one has two states.

### What you should retain

A pyGMs variable is not “the value of a variable.” It is the symbolic object that names one random variable in the model and tells pyGMs how many values that variable can take.

---

## The second object: a factor

A factor is the core object you will actually manipulate.

A factor is a function over one or more variables. Because the variables are discrete, the function can be represented as a table.

For example:

- a factor over one variable is just a vector
- a factor over two variables is a matrix
- a factor over three variables is a three-dimensional table
- and so on

The **scope** of the factor is the set of variables it depends on.

This idea matters because almost every pyGMs operation is really a statement about the scope of a factor:

- conditioning removes fixed variables from the active scope
- summing out removes variables by aggregation
- multiplying factors produces a factor over the union of their scopes
- dividing can produce a conditional-like object if the denominator is the right marginal

So when you hold a factor, always ask two things:

1. What variables are in its scope?
2. What does the table mean numerically?

That question is more important than the exact syntax.

---

## A factor is not automatically a probability distribution

This is a crucial point.

A factor is just a function table. It becomes a probability distribution only if its values satisfy the right normalization conditions for the context.

For example:

- a joint probability factor over variables $X, Y$ must sum to 1 over all joint assignments
- a conditional factor for $p(Y \mid X)$ must sum to 1 over $Y$ separately for each fixed value of $X$
- an arbitrary factor used inside an inference calculation may not be normalized at all

So do not confuse “factor” with “probability distribution.” Some factors are probabilities. Some are not. pyGMs is happy to manipulate either kind.

This matters in HW2 because you start with a joint factor that really is a probability distribution, then you create subtables, marginals, and normalized conditionals from it.

---

## The hidden pitfall: factor argument order

This is one of the most important practical points in the whole library.

Even if you create a factor by listing variables in some order, pyGMs stores factor arguments internally in **sorted order by variable ID**, not by the order you happened to type them.

This means the table axes follow variable ID order.

If you do not internalize this, you can end up reading or filling a table incorrectly even though your code runs.

That is why the dictionary-style indexing is so conceptually safe. When you specify a value using “variable equals state,” you are naming the assignment directly instead of relying on remembering axis order.

For learning, the safest mental rule is:

**The table belongs to the variables in sorted ID order, not in the order I happened to mention them.**

This single point is worth rereading until it feels obvious.

---

## How to think about indexing

There are two conceptually different ways to access a factor entry.

### Tuple-style indexing

Tuple indexing is positional. It assumes you know the order of the factor’s variables and provide one state value per variable in that order.

This is compact, but it is easy to make mistakes if you forget the internal sorting rule.

### Dictionary-style indexing

Dictionary-style indexing is semantic. You specify assignments like “this variable has this value” rather than relying on position.

This is slower to write but much safer conceptually, especially while learning.

For homework and debugging, dictionary-style access is often the best way to keep your reasoning aligned with the math.

---

## The three fundamental operations you need for HW2

For Problem 1, most of pyGMs reduces to three operations.

### 1. Conditioning or slicing

Conditioning means fixing one or more variables to specific values and looking only at the remaining subtable.

Mathematically, if you have a factor $F(T, D, C)$ and fix $T = 1$, you get a smaller factor over the remaining variables $D$ and $C$.

Conceptually, nothing mysterious is happening. You are saying:

“Out of this full table, keep only the entries consistent with this evidence.”

This is exactly how you should think about the homework request to extract the $T=1$ subtable corresponding to $p(T=1, D, C)$.

The important thing to notice is that conditioning does **not** automatically normalize the result. It only restricts the table.

So a conditioned subtable is typically still an unnormalized function unless you later divide by an appropriate marginal.

### 2. Summing out variables

Summing out means aggregating over all values of one or more variables to produce a factor over the remaining variables.

This is marginalization.

If you sum out $D$ from a factor over $(T, D, C)$, you get a factor over $(T, C)$.

The conceptual rule is:

- variables kept in the scope remain as arguments
- variables eliminated are aggregated away

When you read “sum” or “marginal” in pyGMs, do not think of them as two unrelated commands. Think:

“I am reducing the scope by integrating out, or in the discrete case summing out, variables I no longer want to track explicitly.”

### 3. Normalizing or dividing to form conditionals

A conditional probability is usually obtained in pyGMs by taking a restricted or joint factor and dividing it by the appropriate marginal.

For example, if you want $p(C \mid T=1)$, you can proceed conceptually like this:

- start from the joint factor
- condition on $T=1$
- sum out any remaining nuisance variables you do not want
- divide by the appropriate normalizing quantity so the result sums to 1 over the target variable

The deep lesson is that a conditional is not a new magical object. It is a derived factor obtained by taking a joint-like object and renormalizing it correctly.

That is why the homework asks for conditioning, summing, and then algebraic division in sequence.

---

## What arithmetic on factors means

pyGMs lets you add, multiply, divide, maximize, and otherwise manipulate factors.

The right mental model is this:

When two factors involve different scopes, pyGMs conceptually expands them onto the union of their variables and then combines values assignment-by-assignment.

So multiplication of factors means:

“For each joint assignment that is relevant to both scopes, multiply the two function values.”

If the factors correspond to probability pieces, this can represent product factorizations such as graphical models.

If the factors are not normalized probabilities, the arithmetic still makes sense as function arithmetic.

This matters because it keeps you from over-mystifying GraphModels later. A graphical model in pyGMs is basically a structured product of factors.

---

## What a GraphModel is

Once you have variables and factors, a GraphModel is a way of packaging a collection of factors together as one model.

The conceptual point is not the class name. The conceptual point is that the full joint object is represented by the product of the model’s factors.

This is the graphical-model mindset:

- do not store the giant joint table directly if you can avoid it
- store smaller local pieces whose product defines the full model

For HW2 Problem 1, you mostly do not need to think in GraphModel terms yet. You can work directly with a joint factor.

But it is still worth understanding the bridge:

- a single full joint table is one valid factor representation
- a collection of smaller factors is a structured factorization of the same kind of object
- GraphModel is how pyGMs represents that structured collection

So GraphModel is the “many small factors together” view, while the joint table in Problem 1 is the “one big factor” view.

---

## What inference means in pyGMs

Inference means reasoning about the combined function defined by all factors.

That can mean different tasks:

- computing marginals
- conditioning on evidence
- eliminating nuisance variables
- finding likely assignments
- approximating distributions when exact calculation is hard

For your current purposes, the most important inference idea is **variable elimination**.

Variable elimination means removing variables you do not care about while preserving the quantity you do care about.

Conceptually, you repeatedly:
- gather the factors involving a variable
- combine them
- eliminate that variable by summing or maximizing
- pass the resulting smaller factor forward

You do not need to master this yet for HW2 Problem 1, but you do want to recognize that “sum out a variable” is not just a local factor-table trick. It is also the core step in exact inference.

This helps unify the library in your head.

---

## The pyGMs notebook path that actually matters for you now

The repository’s notebooks directory includes introductory notebooks on variables/factors, GraphModel, variable elimination, message passing, Monte Carlo, and learning from data, plus several demos and special-topic notebooks.

For catching up on HW2, do **not** read everything in order as if each notebook is equally urgent.

Use this reading order instead.

### First: 01 Variables and Factors

This is the most important notebook for you right now.

It teaches:
- what a variable object is
- what a factor is
- how scopes work
- how factor tables are indexed
- how conditioning and marginalization work
- the warning about internal variable sorting

That is the notebook most directly tied to HW2 Problem 1.

### Second: 02 The GraphModel Object

Read this after the first notebook, but only to understand the idea that a graphical model is the product of a set of factors.

You do not need to become fluent in all model operations right away. The main point is conceptual: the joint distribution can be represented by multiplying smaller local functions.

### Third: 03 Variable Elimination

Read this lightly after the first two.

Its main value for you now is to unify the idea that summing out variables is both:
- a table operation
- and the core engine of exact inference

That gives you context, even if HW2 Problem 1 only needs the basic table view.

### Later, not now

The other notebooks are not useless. They are just not the best first investment for your current homework bottleneck.

- Message Passing: later
- Monte Carlo: later
- Learning from Data: later
- demos and topic notebooks: only if relevant

---

## How this maps onto HW2 Problem 1

Problem 1 is the perfect pyGMs warm-up because it is mostly discrete probability written as factor operations.

What you need to know to finish it cleanly is this:

1. A joint distribution can be stored as a factor.
2. Conditioning means extracting the entries consistent with evidence.
3. Summing out variables means forming marginals.
4. A conditional is obtained by dividing by the right marginal normalization.
5. If you want to compare two factorizations of the same joint, you can build them as factors and compare the resulting functions numerically.

That is exactly why the homework asks you to:
- extract the $T=1$ subtable,
- sum to obtain $p(T=1, C)$,
- divide to obtain $p(C \mid T=1)$,
- compute marginals like $p(C)$,
- build $p(C)p(D\mid C)p(T\mid C)$,
- and compare it to the original joint.

So if you understand the factor view, the homework becomes a sequence of mathematically familiar operations rather than a library-specific mystery.

---

## Common pyGMs confusions to kill early

### Confusion 1: “Factor” means “probability distribution”

No. A factor is just a function over variables. It might be normalized, but it does not have to be.

### Confusion 2: the order I typed variables is the table order

No. pyGMs stores variables in sorted order by ID.

### Confusion 3: conditioning automatically gives a conditional distribution

No. Conditioning in the table-extraction sense usually just restricts the table. You often still need normalization.

### Confusion 4: marginalization is a special pyGMs trick

No. It is just summing out variables from discrete probability, written as a factor operation.

### Confusion 5: GraphModel is a totally new concept beyond factors

No. It is the “product of many factors” organization of the same underlying idea.

### Confusion 6: tuple indexing and dictionary indexing mean different mathematics

No. They are two ways of referring to the same table entries. The difference is mainly safety and readability.

---

## What you should know well before moving on

Before you leave the pyGMs catch-up phase, make sure you can explain the following in words, without code.

You should be able to say what a pyGMs variable is and why its ID matters.

You should be able to say what a factor is, what its scope is, and why a factor is not automatically a probability distribution.

You should be able to explain the difference between:
- restricting a factor by evidence,
- summing out a variable,
- and renormalizing to form a conditional.

You should be able to explain why internal variable sorting can make tuple indexing dangerous if you are not careful.

And you should be able to say why a GraphModel is conceptually just a structured product of factors.

If those ideas are clear, you are caught up enough for the pyGMs part of HW2.

---

## A practical reading plan for today

1. Read the “Variables and Factors” notebook carefully.
2. As you read it, translate every operation back into probability language:
   “This is a table,” “this is conditioning,” “this is a marginal,” “this is normalization.”
3. Then read the opening of “The GraphModel Object” notebook to understand factor products.
4. Then skim the beginning of “Variable Elimination” so summing out variables becomes part of one bigger picture.
5. Then return to HW2 Problem 1 and treat each step as a factor operation over a table you already understand.

That is the cleanest catch-up path.

# HW2 Gap Information: What the Repo Does Not Give You, but the Homework Prompt Requires

## Why this document exists

The repository you pointed me to is strong on **probability theory** and **Bayesian-network structure**, but Homework 2 is not asking only for theory. It is asking you to *execute* that theory inside two concrete software systems: **pyGMs** for finite discrete factor tables and **Pyro** for stochastic programs and normalizing flows. The homework PDF is explicit about that split: Problem 1 is about factor operations in `pyGMs`, Problem 2 is about expressing a Bayesian network in `Pyro`, and Problem 5 is about fitting a normalizing flow in `Pyro`. The code template also leaves important operations unstated, so the conceptual bridge between “I understand the notes” and “I know what object to build and how to manipulate it” is missing. fileciteturn4file1 fileciteturn4file7 fileciteturn4file11 fileciteturn4file12

This document fills exactly that gap. It is not a solution sheet. It is a **homework-execution gap chapter**: a self-contained teaching note that explains what additional knowledge the prompt assumes, why that knowledge is needed, what objects the libraries are manipulating, what the most important conventions are, where students usually get confused, and what details matter specifically for this homework.

There is also a second purpose. Your uploaded writing instructions demand a document that does not merely summarize, but instead teaches from the ground up, makes assumptions explicit, surfaces misconceptions, and explains how the pieces connect. So this note is not just “the answer to your prompt.” It is the **reflected version** of that answer: the version you would want if your goal is not only to finish the assignment, but to understand why the prompt is written the way it is and what invisible knowledge it is presupposing. fileciteturn4file14 fileciteturn4file15

## The two versions of the task: prompt version and reflected version

The **prompt version** of the task is narrow: “What information am I missing from the repo in order to do HW2?” That question can be answered as a list. One can say: you are missing `pyGMs` mechanics, `Pyro` mechanics, shape conventions, a few problem-specific coding expectations, and some homework logistics.

The **reflected version** is more useful. It asks a stronger question:

> If a student already has the repo’s theory, what additional conceptual and operational knowledge must be added so that the homework prompt becomes fully executable and no longer hides assumptions?

That reflected version changes the document in an important way. It forces the note to include not just “extra topics,” but also:

- the *role* each library object plays;
- the difference between theory-level and API-level reasoning;
- the order in which the homework expects operations to happen;
- the boundary conditions that make a method valid;
- the common failure points that come from software conventions rather than from probability mistakes;
- prompt-specific details that you would not include in a purely theoretical set of notes.

That is the correct approach for this assignment. The repo already gives you the conceptual backbone. What you need now is the **theory-to-execution bridge**.

## What I would add only after reading the homework prompt

If I had only the repo, I would write about joint distributions, conditional independence, likelihood, and change-of-variable models. After reading the homework prompt and template, I would add several things that are clearly prompt-driven rather than repo-driven.

First, I would add a section on **deliverable format**. The homework is a PDF submission, not a notebook or `.py` submission. That means code is instrumental, not the final artifact. In practical terms, your output must be figures, tables, numerical summaries, and explanations that can be pasted into the PDF template. This matters especially for Problems 1 and 5, where the prompt explicitly asks you to print factor tables and paste generated figures into the PDF. fileciteturn4file1 fileciteturn4file6

Second, I would add a section on **library conventions that the repo never needed to mention**. The repo can explain conditioning abstractly; the homework needs you to know that in `pyGMs` a factor is indexed by variables with integer IDs, that factors align by variable identity rather than by how you casually wrote them, and that the returned sample tuples must match the variable order assumed by your counting logic. The homework itself warns you about this when it says that `joint` only knows variable IDs and that empirical counting assumes the data tuple order matches `(X0, X1, X2)`. fileciteturn4file0 fileciteturn4file7

Third, I would add a section on **shape semantics in Pyro and PyTorch**. A two-dimensional normalizing-flow model is not just a “distribution over two numbers.” It has an event dimension of size two, and batch dimensions appear when you sample many points or pass many data points to `log_prob`. The prompt never says this in so many words, but the code template assumes you can infer it from the call pattern involving `MultivariateNormal`, `flow.sample(...)`, and `flow.log_prob(data)`. Without this idea, students often produce shape mismatches or misunderstand what a row of data represents. fileciteturn4file5 fileciteturn4file12

Fourth, I would add a **prompt-trap section**. One especially relevant example is the bigram-model preprocessing block. The prompt says to count frequencies from the cleaned token sequence before replacement, which conceptually means counting from `tok_all`, but the visible template line shows `word_count = collections.Counter(tok)` before `tok` has been defined. That is exactly the sort of thing you would mention only after reading the prompt and template, because it is not a theory gap at all; it is an execution hazard. fileciteturn4file2 fileciteturn4file13

Fifth, I would add **problem-by-problem success criteria**. For example: Problem 3 is purely graphical reasoning and does not need code; Problem 5 only requires four scatterplots in the PDF, not a full proof or analytic density calculation; Problem 2 expects empirical estimates from 1000 model draws, not exact symbolic inference. Those expectations come from the assignment prompt, not from the repo’s notes. fileciteturn4file4 fileciteturn4file11 fileciteturn4file12

## How the repo and the homework divide the work

The repo gives you the **mathematical meaning** of the operations. It explains that a joint distribution is the master object, that marginalization removes variables by summing them out, that conditioning restricts and renormalizes, that likelihood evaluates parameter fit to observed data, and that change-of-variable models preserve probability mass through a Jacobian correction. It also gives the semantics of Bayesian networks: a DAG plus one local conditional distribution per node, factorized into a joint distribution. citeturn765142view0turn269458view0turn269458view1turn269458view2turn379262view0

The homework adds the **operational layer**. It says, in effect: now instantiate those abstractions inside specific computational objects. For discrete finite models, use `pyGMs` factor objects. For stochastic generative models and flows, use `Pyro` distributions, sample sites, and transformed distributions. So the missing information is not “more probability theory of the same kind.” It is **the meaning of the software objects that carry out that theory**.

That distinction is worth retaining because students often misdiagnose their difficulty. They think they do not understand probability, when in fact they mostly do understand the probability and are missing the computational representation.

# Part I. The pyGMs gap

## Why this section exists

Problem 1 is phrased as if conditioning, marginalization, conditional independence, and empirical estimation are already familiar from the notes. That part is true. But the prompt is not asking you to do those operations in the abstract. It is asking you to do them as **member functions and algebraic operations on factor objects**. So the missing question is:

> What exactly is a `pyGMs` factor, what does it store, and how do abstract probability operations become manipulations of that object?

Without that bridge, the student knows what marginalization means mathematically but does not know what object is being summed, what variable is being removed, or how factor multiplication and division behave when scopes differ.

## The object being introduced

A `pyGMs` factor is a **table-valued function over a finite set of discrete random variables**. In Homework 2, the factor entries are probabilities, but conceptually a factor is slightly more general than a probability table. It is best to think of it as follows.

There is a fixed set of variables in its scope. Each variable has a finite number of states. For every joint state of those variables, the factor stores one number. If the factor happens to be normalized and nonnegative, it can be a probability distribution or conditional distribution. If not, it is still a legal factor, but not yet a probability law.

That distinction matters because the homework makes you do both kinds of things. The original `joint` factor is a normalized probability distribution over `(T, D, C)`. A restricted table such as the slice corresponding to `T = 1` is not, by itself, a conditional distribution over `(D, C)` yet; it is the subtable corresponding to the event `T = 1`, and it must still be interpreted correctly. Similarly, a product of factors may need normalization before it becomes a probability distribution.

## Formal definition

In the homework, the variables are created as discrete variables with IDs and cardinalities. A factor is then built on a scope such as `(T, D, C)`, and entries are assigned by mapping joint assignments of those variables to numbers. The prompt uses exactly this construction for the dentist example. fileciteturn4file1

## Interpretation paragraph

The key thing to notice is that `pyGMs` does not care about your convenient Python variable names in the human sense. It cares about the **variable identities**. The homework states this directly: the factor does not know the names `T`, `D`, and `C`; it knows only variable IDs and their numbers of states. It also says that the factor keeps track of variables in order of their ID numbers rather than in whatever superficial order you feel like remembering. fileciteturn4file0

That one point explains many later behaviors. When you multiply factors, the software aligns them by variable identity. When you index with a tuple, the positions correspond to the factor’s internal variable ordering. When you sample, the resulting tuple is understood relative to variable order. So the question “what does this entry mean?” is never just about position. It is position *relative to variable IDs in the factor scope*.

## Boundary conditions, assumptions, and failure modes

Several assumptions are easy to miss.

First, Homework 2 uses **finite discrete variables**. A factor table only makes sense because each variable has finitely many possible values. This is why `gm.Var(0,2)` means a variable with ID `0` and two states.

Second, **scope alignment matters**. If two factors involve overlapping but nonidentical variable sets, factor multiplication is not a pointwise multiply over raw arrays in the naive sense. It is a multiply after aligning joint assignments over the union of scopes.

Third, **normalization is not automatic**. If you condition by restricting to an event, the result is not automatically a proper conditional distribution until the appropriate normalization is carried out.

Fourth, **sample tuples must match variable order**. The homework explicitly warns that empirical counting with `phat[x] += 1` assumes the sample tuple order agrees with `(X0, X1, X2)`. If not, you must build the index using variable-value dictionaries rather than positional assumptions. fileciteturn4file7

Fifth, there is a subtle prompt-level issue in the empirical-estimation section. The PDF regularizes first and then normalizes, which makes the table a proper smoothed distribution. In the visible code template, one snippet shows normalization before adding the small constant, which would leave the final displayed table not exactly normalized unless one normalizes again. For homework understanding, the right conceptual order is: count, smooth, then renormalize. fileciteturn4file10 fileciteturn4file3

## Fully worked example: what `p(C | T = 1)` means as a factor computation

The prompt asks you to compute three related objects in sequence: the `T = 1` subtable, then the marginal over `(T, C)` restricted to that event, then the conditional distribution `p(C | T = 1)`. fileciteturn4file0

The right way to understand that sequence is not as three unrelated commands, but as three different probabilistic objects.

Start with the joint table over `(T, D, C)`. This is the master object. Every row says how probable one complete joint assignment is.

Now restrict to the event `T = 1`. This does **not** mean “you have already computed the conditional probability.” It means you have kept only the rows compatible with `T = 1`. In probabilistic terms, you are looking at the function that assigns `p(T = 1, D, C)` to each pair `(D, C)`. The evidence variable has been fixed, but the resulting values still contain the total probability weight of the event `T = 1`.

Next, sum out `D`. This produces a smaller table over `C`, but it still represents `p(T = 1, C)`, not yet `p(C | T = 1)`. Why? Because marginalization removed the nuisance variable `D`, but no normalization has happened yet.

Finally, divide by the total probability of the event `T = 1`. This converts the remaining table into a conditional distribution over `C`. After this step, the entries sum to one across the remaining variable states.

The general lesson is this: when the homework asks for a posterior from a joint table, the pipeline is always **restrict, eliminate irrelevant variables, normalize**. The mathematical object changes at each step, and understanding that change is more important than memorizing the method name.

## What the main pyGMs operations mean in Homework 2

### Conditioning or slicing

This operation fixes one or more variables to observed values and produces the remaining subtable consistent with that evidence. In the homework, conditioning on `T = 1` means all rows with `T = 0` are excluded, and the factor is now interpreted over the remaining free variables. The point to notice is that the evidence variable is not random inside the resulting object anymore; it has become part of the conditioning context. fileciteturn4file0

### Summing or marginalizing

This operation removes variables from the scope by summing over all their possible values. What remains is the total probability assigned to the retained variables after averaging over, or forgetting, the eliminated ones. If the object started as a joint table, the result is a marginal. If the object started as a restricted table, the result is a restricted marginal. The key is always to ask: **what variables are still varying after the sum, and what object does the resulting table now represent?**

### Factor multiplication

Multiplication combines local pieces into a joint-style object over the union of their variables. In Homework 2, the test of conditional independence compares the original joint distribution `p(T, D, C)` against the product `p(C) p(D | C) p(T | C)`. That product is meaningful because the shared variable `C` aligns the factors consistently. The software handles the variable matching, but your interpretation must still be probabilistic: the product is asserting a specific factorization structure. fileciteturn4file7

### Factor division

Division is used when a conditional distribution is created from a joint or partially marginalized table. The conceptual meaning is not “divide because the library says so.” The meaning is: we are renormalizing relative to the conditioning event so that the remaining free variable becomes distributed conditionally on that event.

### Distance and KL divergence

The prompt asks you to compare the original joint to the factorized approximation by total squared error and by KL divergence. The squared error is a raw numerical closeness measure. KL divergence is probabilistic: it measures how much information is lost when one distribution is used in place of another. The prompt expects both to be near zero if the conditional-independence factorization is correct. fileciteturn4file0

What should you notice? Squared error is symmetric as a raw arithmetic comparison, but KL divergence is directional. `D(p || q)` is asking how badly `q` serves as a substitute for `p`, not vice versa. That direction matters later in probabilistic modeling.

## Misconception block: a factor is not automatically a probability distribution

Students often overread the word “factor.” In this homework, many factors do represent normalized probabilities, but the software object itself is more general. A restricted subtable, an unnormalized count table, or a product of local tables before normalization can all be legal factors. The question “is this object a probability distribution?” is separate from the question “is this object a factor?”

A second confusion is to think that conditioning is merely deleting rows. Deleting incompatible rows is only the first part. A conditional probability distribution must also be normalized over the remaining variable states.

A third confusion is to believe that variable order is cosmetic. In this homework it is not. The prompt explicitly warns that the library tracks variables by ID, and the empirical-counting section explicitly warns that tuple positions must match the variable ordering assumption. fileciteturn4file0 fileciteturn4file7

## Connection to later material

The pyGMs material is not an isolated library tutorial. It teaches the computational form of three ideas that reappear throughout graphical models: local factor manipulation, elimination of nuisance variables, and structure-based factorization. If you understand why Homework 2 Problem 1 is written this way, then Bayesian-network inference, variable elimination, and even message passing will feel like natural extensions rather than new worlds.

## Retain / do not confuse

Retain these points.

A factor is a table-valued function over discrete variables. Conditioning fixes variables but does not by itself complete normalization. Marginalization removes variables by summing them out. Factor multiplication asserts a joint-style combination over aligned scopes. Variable IDs, not casual naming, determine alignment and indexing. 

Do not confuse these points.

Do not confuse a factor with a normalized probability distribution. Do not confuse a restricted table with a conditional distribution before normalization. Do not confuse tuple position with variable meaning independent of the factor’s variable ordering.

# Part II. The Pyro gap for Problem 2

## Why this section exists

Problem 2 asks you to define the Wet Grass Bayesian network in Pyro using `sample()` statements and then estimate probabilities by Monte Carlo sampling. That sounds simple, but it silently assumes you know what a Pyro model is, what a sample site represents, how conditional dependence is encoded inside the generative program, and what the output of repeated model calls should be interpreted as. The repo’s Bayes-net notes explain the factorization, but not the software object that realizes it. fileciteturn4file9 fileciteturn4file11

## The object being introduced

A Pyro model is a **stochastic generative program**. It is not merely a function that returns numbers. It is a procedure that, when run once, samples one joint outcome from a probability law. In Homework 2, one run of the model should generate one quadruple `(C, S, R, W)` from the Wet Grass network.

What is fixed is the model structure and the conditional probabilities specified in the prompt. What varies from one execution to the next are the sampled random values. The point of writing the model this way is that repeated execution gives empirical access to the distribution: marginals can be estimated from frequencies, and joint probabilities can be estimated from co-occurrence counts.

## Formal definition

The homework tells you to define the model using Pyro `sample()` statements, one for each random variable, respecting the parent-child structure of the Wet Grass network. It also indicates that returning the tuple is convenient even though the return value is not formally required for the stochastic semantics. fileciteturn4file11

## Interpretation paragraph

The right conceptual picture is this. Each `pyro.sample(name, distribution)` call creates a random choice at a named site. If the distribution depends on previously sampled variables, that dependence is encoded directly in how you choose the distribution object for the later variable.

So the model order is not arbitrary. You first sample `C` because it has no parents. Then you sample `S` and `R` because each depends on `C`. Then you sample `W` because it depends on both `S` and `R`. That is the Bayes-net factorization turned into a forward simulator.

The names given to sample sites matter operationally because they identify the random choices inside the trace of the stochastic program. The values returned by those sites are typically PyTorch tensor scalars rather than bare Python booleans. That is an implementation fact, but it matters when you interpret or manipulate the samples.

## Boundary conditions, assumptions, and failure modes

The most important hidden assumption is that the program must be a **correct generative order for the DAG**. If you try to define `W` before `S` and `R` exist, you do not just have a coding inconvenience; you have failed to mirror the factorization structure.

A second assumption is that the Bernoulli parameters must always be valid probabilities between zero and one, chosen according to the relevant parent configuration.

A third issue is representational. In Pyro and PyTorch, discrete sample values are usually tensors. That means you should conceptually treat them as scalar random outcomes, but be aware that they carry tensor semantics. The homework does not ask you to perform advanced tensor manipulations here, but the fact is important when moving from scalar logic to batched or transformed models later.

A fourth issue is sampling interpretation. Drawing 1000 samples does not produce the exact marginal probabilities; it produces **empirical estimates** of them. The prompt even gives a few theoretical target values as sanity checks, such as `p(C = 1) ≈ 0.5` and `p(S = 1) ≈ 0.3`. Those are there so you can check whether your generative logic is plausibly correct. fileciteturn4file9

## Fully worked example: what one execution of the Wet Grass model means

The Wet Grass network in the prompt has the following structure. `C` is cloudy. `S` depends on `C`. `R` depends on `C`. `W` depends jointly on `R` and `S`. fileciteturn4file9

One execution of the Pyro model should be read as follows.

First, a single value of `C` is drawn. This represents whether the world in this simulated run is cloudy.

Second, given that realized cloudiness value, a single value of `S` is drawn. The probability that the sprinkler is on changes depending on whether `C` came out as `0` or `1`.

Third, given that same cloudiness value, a single value of `R` is drawn.

Fourth, given the realized pair `(R, S)`, a single value of `W` is drawn from the corresponding conditional probability.

At the end of that run, you do not have four unrelated Bernoulli draws. You have one **joint sample from the entire Bayesian network**. That is the point. If you repeat the run 1000 times, you get 1000 i.i.d. draws from the model, and sample averages estimate the model’s marginals and selected joint events.

The general lesson is that Pyro is not replacing the Bayesian-network factorization. It is implementing the factorization as a simulator.

## What empirical estimation means in Problem 2

The prompt asks for estimates of `p(C = 1)`, `p(S = 1)`, `p(R = 1)`, `p(W = 1)`, and `p(S = 1, R = 1)` from 1000 draws. fileciteturn4file11

The meaning of each estimate is straightforward once the model semantics are clear.

The estimate of `p(C = 1)` is the fraction of model executions in which the sampled cloudiness variable equals one. The estimate of `p(S = 1)` is the fraction of executions with sprinkler on. The estimate of `p(S = 1, R = 1)` is the fraction of executions in which both events happen together in the same run.

Notice the distinction between a marginal event and a joint event. For the joint probability, you are not averaging two separate marginal indicators independently; you are counting runs in which both conditions hold simultaneously.

For a theoretical self-check, the prompt already reveals two values. From the given conditionals, `p(C = 1) = 0.5` and `p(S = 1) = 0.5 · 0.5 + 0.5 · 0.1 = 0.3`. By the same logic, `p(R = 1) = 0.5 · 0.2 + 0.5 · 0.8 = 0.5`, and `p(S = 1, R = 1) = 0.5 · (0.5 · 0.2) + 0.5 · (0.1 · 0.8) = 0.09`. These are not required symbolic answers, but they are extremely useful sanity checks. fileciteturn4file9

## Misconception block: Pyro is not “doing inference for you” in Problem 2

A common misconception is to think that writing a Pyro model automatically gives exact inferred probabilities. That is not what Homework 2 is using Pyro for here. In Problem 2, you are using it as a **forward simulator**. The estimates come from repeated sampling, not from invoking an exact inference algorithm.

A second misconception is to confuse “one run of the model” with “one distribution object.” One run returns one joint sample. The model itself encodes the whole distribution.

A third misconception is to think the sample-site names are mathematically decorative. In Pyro they are operational markers for stochastic choices inside the program trace.

## Connection to later material

This way of thinking about Pyro is the entry point to probabilistic programming more broadly. A Bayesian network becomes a generative program, and later an unnormalized density model becomes a trainable transformed distribution. Once you understand that a model execution corresponds to a draw from a joint law, later Monte Carlo methods, variational ideas, and flow-based models become much less mysterious.

## Retain / do not confuse

Retain these points.

A Pyro model is a stochastic procedure whose one execution generates one joint sample. The sample order should respect the DAG. Repeated executions produce empirical estimates of marginal and joint probabilities.

Do not confuse these points.

Do not confuse forward sampling with exact inference. Do not confuse one run of the model with the distribution itself. Do not confuse a marginal estimate with a joint co-occurrence estimate.

# Part III. The Pyro gap for Problem 5: normalizing flows

## Why this section exists

The repo explains change-of-variable models and says that normalizing flows are an extension of that same idea. That is the correct theory. But Homework 2 asks you to instantiate the idea in Pyro using a multivariate normal base distribution, a `spline_coupling` transform, a `TransformedDistribution`, and a training loop based on `log_prob`. That requires a second layer of understanding:

> What is the computational object called a normalizing flow, and how do base distribution, invertible transform, sample shape, event shape, and log-likelihood fit together inside Pyro?

Without that, the student knows what the Jacobian formula means in principle but does not know what the Pyro objects are representing. fileciteturn4file5 citeturn269458view2

## The object being introduced

A normalizing flow is a **trainable probability distribution obtained by transforming a simple base distribution through an invertible map**. In this homework, the base is a two-dimensional standard Gaussian, and the transform is a spline coupling map.

What is fixed conceptually is the model family: “start from a simple base law and transform it.” What varies during training are the parameters of the transformation. The reason this matters is that a complicated observed distribution can be modeled indirectly. Instead of specifying the complicated density by hand, you learn an invertible transformation that warps a simple density into one that matches the data.

## Formal definition

The prompt tells you to create a two-dimensional standard normal base distribution, define a spline coupling transformation, combine them into a `TransformedDistribution`, sample from the untrained model, optimize the transform parameters by minimizing negative log-likelihood, clear the flow cache after each update, and then sample from the trained model for the final scatterplot comparison. fileciteturn4file5 fileciteturn4file12

## Interpretation paragraph

The model is doing exactly what the repo’s change-of-variable section says. There is a base variable `Z` whose density is easy. There is an invertible map `f` with trainable parameters. The observed-space variable is `X = f(Z)`. Sampling works by first drawing `Z` and then pushing it through the transform. Density evaluation works by taking an observed `x`, mapping it back through the inverse transform, evaluating the base density there, and correcting by the Jacobian determinant. That is why the transformed distribution can both sample and assign log-densities. citeturn269458view2

The Pyro object `TransformedDistribution(base, [xform])` packages that logic into one distribution object. It is not merely storing transformed samples. It is representing the full probability law implied by the base distribution and the invertible transformation.

## Boundary conditions, assumptions, and failure modes

The most important hidden assumption is **invertibility**. The whole density-transformation logic depends on the map being invertible on the relevant support region. That is why coupling transforms are used: they are designed so that sampling and density evaluation remain tractable.

The second critical issue is **shape semantics**.

A two-dimensional multivariate normal has event dimension two. One sampled point is therefore a length-two vector, not two independent scalar events living in unrelated slots. If you draw many points, you introduce a batch dimension on top of that event dimension. So 1000 samples from a 2D base or flow distribution should conceptually be a collection of 1000 vectors in two-dimensional space.

The same is true when evaluating `log_prob(data)`. The input `data` should be a batch of 2D observations, one row per observation. The output is one log-density value per observation, which can then be averaged to form the mean negative log-likelihood used in training. This is one of the main bits of missing knowledge when students read the prompt: the mathematical density is over one 2D vector, but training uses batches of many such vectors at once. fileciteturn4file5 fileciteturn4file12

The third issue is **cache invalidation**. The prompt includes `flow.clear_cache()` after each optimizer step. That is not decorative. Some transformed-distribution implementations cache intermediate transform information, and after parameter updates that cache can become stale. Clearing it keeps the distribution state consistent with the new parameters. The prompt signals that this detail matters operationally. fileciteturn4file12

The fourth issue is to distinguish **sample generation** from **density fitting**. The generative process `sample_data(m)` creates data, but it is not itself a normalized tractable density model you can easily score new points under. The flow is being fit precisely to turn that data-generating pattern into a learned density model. The prompt says this explicitly when it contrasts a generative process with a probability distribution that can judge whether a point is typical or unusual. fileciteturn4file5

## Fully worked conceptual example: what the four scatterplots are doing

Problem 5 asks for four scatterplots: samples from the generative process, samples from the base distribution, samples from the initial untrained flow, and samples from the trained flow. fileciteturn4file6

These four plots are not redundant. They answer four distinct questions.

The **generative-process plot** shows the target geometry in data space. This is what the learned density should approximate.

The **base-distribution plot** shows the geometry before any transformation. Because the base is a standard 2D Gaussian, you should expect a roughly centered cloud with ordinary elliptical shape. This plot is a baseline, not an attempted fit.

The **initial-flow plot** shows what the transformed model looks like before learning. The transform has the right architectural flexibility, but its parameters have not yet been adapted to the data. So this plot separates “expressive model family” from “trained fit.”

The **trained-flow plot** shows what happens after optimization pushes the transformed distribution toward higher likelihood on the observed data. If training has worked, the cloud should look qualitatively more like the generative-process samples than the base or initial-flow samples did.

The general lesson is that a normalizing flow is best understood both algebraically and geometrically. Algebraically it is a change-of-variable density model. Geometrically it is a trainable warping of space.

## Why `log_prob` is the right training objective

The repo’s estimation notes explain why log-likelihood is introduced: it turns products into sums, is easier to optimize numerically, and has the same maximizer as likelihood. In the flow setting, `flow.log_prob(data)` returns the log-density assigned by the current transformed model to each observed point. Taking the negative mean turns “fit the data well” into a minimization objective suitable for gradient descent. citeturn269458view1turn269458view2

What is fixed and what varies here must be kept straight. The observed batch of data points is fixed for one gradient step. The transform parameters are the variables being optimized. The objective measures how much probability mass the current model places near those observations, corrected properly through the inverse transform and Jacobian structure.

## Misconception block: a flow is not just “a neural net that outputs points” 

A common misconception is to think that a normalizing flow is only a generator. It is more than that. A generator that only produces samples is not enough for density estimation. A flow is valuable because it gives both **sampling** and **tractable density evaluation** through an invertible transformation.

A second misconception is to think that the Jacobian term is an optional correction. It is the entire reason transformed densities remain valid probability distributions. The repo’s change-of-variable notes are clear that the Jacobian is enforcing probability conservation under stretching and compression. citeturn269458view2

A third misconception is to confuse “a point in two-dimensional space” with “a batch of size two.” Event dimensions and batch dimensions play different roles. The point dimension belongs to the modeled random variable itself; the batch dimension counts how many observations or samples you are processing together.

## Connection to later material

This is where probability, optimization, geometry, and machine learning visibly meet. The probability side gives densities and likelihood. The geometry side gives invertible warps and Jacobians. The optimization side gives gradient-based fitting. The machine-learning side gives a flexible parametric family that can match complicated data distributions. Once you see that these are the same object from four viewpoints, normalizing flows stop looking like a bag of tricks.

## Retain / do not confuse

Retain these points.

A flow is a transformed distribution, not just a sampler. The base distribution is simple; the transform is trainable and invertible. `log_prob` is evaluated on batches of 2D observations. Batch dimension and event dimension are different. The four plots each answer a different diagnostic question.

Do not confuse these points.

Do not confuse a data-generating simulator with a tractable density model. Do not confuse transformed samples with a full transformed distribution. Do not confuse Jacobian correction with an implementation detail that can be ignored.

# Part IV. Prompt-specific issues beyond pyGMs and Pyro

## Why this section exists

Some missing information is not about either library. It comes from the homework prompt itself. These are the details that often cost points not because the underlying mathematics is hard, but because the task structure was misread.

## Deliverable format and what counts as a finished answer

The homework is a **PDF submission only**. You are told to fill in the provided PDF template, keep the pages in original order, show the work needed to produce final answers, and paste generated results such as figures into the PDF. This means that “I have working code” and “I have a complete homework submission” are different achievements. Your code must generate interpretable artifacts for the PDF. fileciteturn4file1

For Problem 1, that means factor tables and numerical summaries should be shown in readable form. For Problem 5, it means the scatterplots themselves are the required output. The prompt explicitly says that for the flow problem you only need to submit the four scatterplots. fileciteturn4file6

## Problem 3 is about graph activation, not arithmetic

The repo’s Bayesian-network notes are relevant here because the problem asks which observations can affect beliefs and reminds you that the graph is a polytree, so there is exactly one undirected path between any two nodes. That means each yes-or-no question is fundamentally asking whether that unique path is active or blocked under the observed evidence pattern. You do not need numeric tables for this problem. You need correct d-separation reasoning using chain, fork, and collider logic. fileciteturn4file4 citeturn379262view0

## Problem 4 has a likely template hazard

The bigram section in the PDF says to count token frequencies after cleaning and lowercasing, keep the top `nKeep = 1000` words, replace the rest by `?`, convert to indices, estimate the transition matrix, and sample two sequences of length 50. In the visible code template snippet, however, the line counting words uses `Counter(tok)` before `tok` has been defined. Conceptually, the counts must come from the pre-replacement token list, which the PDF names `tok_all`. This is exactly the kind of detail you would only catch by reading the prompt and template carefully together. fileciteturn4file2 fileciteturn4file13

## Sanity-check targets are part of the prompt’s teaching design

The Wet Grass problem gives you theoretical target values for some marginals. The flow problem tells you the purpose of each plot. The factor-table problem names the exact sequence of operations expected. These are not filler sentences. They are the prompt’s built-in scaffolding. When a homework prompt offers these cues, it is usually signaling what kind of internal check you should perform before trusting your final outputs. fileciteturn4file0 fileciteturn4file9

# Final synthesis: what information you were missing

You were not mainly missing more probability notes. You were missing a **bridge layer**.

That bridge layer has five parts.

First, you needed the semantics of `pyGMs` factors: what they store, how variable IDs determine ordering and alignment, how conditioning differs from normalization, how multiplication and division build probabilistic objects, and why the empirical-counting section cares about tuple order. fileciteturn4file0 fileciteturn4file7

Second, you needed the semantics of a `Pyro` model as a stochastic generative program: one execution equals one joint draw, later sample sites depend on earlier values according to the DAG, and empirical probabilities are estimated from repeated simulation rather than exact inference in Problem 2. fileciteturn4file11

Third, you needed the shape and object semantics of `Pyro` flow models: base distribution versus transformed distribution, event dimension versus batch dimension, why `log_prob(data)` is the right objective, and why `clear_cache()` appears after parameter updates. fileciteturn4file5 fileciteturn4file12

Fourth, you needed prompt-specific execution details: PDF-only submission, factor tables and figures as the final outputs, Problem 3 as d-separation reasoning rather than computation, and the bigram-template hazard in preprocessing. fileciteturn4file1 fileciteturn4file4 fileciteturn4file2

Fifth, you needed the reflected version of the task: not just “fill the gaps,” but “identify what the prompt assumes silently and make that knowledge explicit enough that the homework becomes executable without guesswork.” That is the version of the task this note was designed to satisfy.

## Retain / do not confuse

Retain this summary.

The repo gives the theory. The homework demands the theory expressed inside concrete software objects and concrete submission constraints. The missing information is therefore not merely new theory; it is theory-plus-representation-plus-execution discipline.

Do not confuse these three layers.

Do not confuse understanding a probabilistic idea with knowing how a library represents it. Do not confuse a working notebook with a finished PDF submission. Do not confuse the direct prompt with the more useful reflected version, which turns invisible assumptions into explicit teaching.

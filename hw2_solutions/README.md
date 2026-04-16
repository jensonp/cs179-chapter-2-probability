# Problem 4 and Problem 5: Detailed Solution and Teaching Guide

This document is a study guide for the two toughest problems in Homework 2. It is written to do two jobs at once:

1. help you finish the homework correctly, and  
2. help you understand what the code is actually doing.

The style here is math-first and object-first. For each problem, the goal is to keep asking:

- What mathematical object do I have?
- What operation am I performing on it?
- What is fixed?
- What is varying?
- What conclusion does this step allow?

---

# Problem 4. Bigram Text Models

## Why this problem exists

Earlier in the course, probability tables and Bayesian networks described uncertainty in a small number of random variables. This problem forces the same ideas into a sequential setting. Instead of asking for the probability of a small tuple like $(T,D,C)$, we now want a model for a whole sequence of words.

The problem introduces the simplest nontrivial sequence model: the bigram model. It matters because it is the first place where “conditional probability from counts” becomes a model of language. The point is not that this is a realistic language model. It is that it teaches the mechanism clearly.

---

## The object being introduced

The main object is the **transition matrix** $T$.

A bigram model assumes that the next word depends only on the current word. So if the current word has index $i$ and the next word has index $j$, then

$$
T[i,j] = p(w_t = j \mid w_{t-1} = i).
$$

This matrix is a conditional-probability table. Each row corresponds to one current word. Each row gives a full conditional distribution over the next word.

So the model is a first-order Markov chain over word tokens.

What is fixed?

- the vocabulary,
- the tokenization rule,
- the dataset,
- the decision to keep the top $1000$ words and collapse the rest into `?`.

What varies?

- the current word index $i$,
- the next word index $j$,
- and therefore which row and column of $T$ we are talking about.

What conclusion does $T$ allow?

It lets you answer both kinds of questions the homework asks:

1. **prediction**: which words are most likely after a given word?  
2. **generation**: if I repeatedly sample according to the rows of $T$, what sequences does the model produce?

---

## Formal definition

A bigram model is the Markov-chain approximation

$$
p(w_1,\dots,w_n)=p(w_1)\prod_{t=2}^{n} p(w_t \mid w_{t-1}).
$$

The transition probabilities are estimated from counts:

$$
T[i,j]=\frac{N_{ij}}{\sum_k N_{ik}}.
$$

The numerator is the number of times word $i$ is followed by word $j$ in the corpus.  
The denominator is the total number of observed transitions leaving word $i$.

---

## Interpretation

This definition is saying something very specific.

The model is not trying to understand grammar, syntax, meaning, or discourse. It is only claiming that the next token depends on the immediately previous token. So when you estimate the matrix, every row is asking:

> Among all times this word appeared as a current word, what fraction of the time was the next word equal to each possible vocabulary item?

That is all. The model is simple, but it is precise.

---

## Boundary conditions, assumptions, and failure modes

There are several assumptions and practical details here that matter.

First, the model is only as good as the preprocessing. Lowercasing, removing punctuation, and replacing infrequent words all change the state space. So the estimated probabilities depend on those choices.

Second, the top-$1000$ truncation is a modeling choice, not just a memory trick. It says that rare words are all being merged into a single state called `?`. That stabilizes the matrix, but it also destroys distinctions among rare words.

Third, some rows might be sparse. If a word is rare even within the top $1000$, then its row may be based on very few transitions. Those estimated probabilities are much less stable.

Fourth, this is a first-order Markov model. It has no memory beyond the previous token. So if a sequence seems incoherent, that is not a bug in the code. It is the direct consequence of the modeling assumption.

---

## Step 1: Load and preprocess the corpus

The homework gives

```python
url = 'https://www.ics.uci.edu/~ihler/classes/cs179/data/cs179-hw2-PnP-data.txt'

with requests.get(url) as link:
    text_all = StringIO(link.text).read()

text = re.sub(r'[^a-zA-Z0-9 ]','', text_all)
tok_all = [t.lower() for t in text.split()]
```

### What this is doing mathematically

The raw text file is not yet a sequence over a finite state space. It contains punctuation, capitalization, and formatting artifacts. The preprocessing step constructs the actual observation sequence the model will use.

After preprocessing:

- punctuation is removed,
- everything is lowercase,
- the corpus becomes a list of word tokens.

So `tok_all` is the original sequence $w_1,w_2,\dots,w_N$ before vocabulary truncation.

---

## Step 2: Build the reduced vocabulary

The prompt code fragment contains this line:

```python
word_count = collections.Counter(tok)
```

But that line is wrong in context, because `tok` has not yet been defined.

The correct object to count is `tok_all`, since that is the already-created cleaned token sequence.

So the corrected code is:

```python
import collections
nKeep = 1000

word_count = collections.Counter(tok_all)
keep = [w for w, cnt in word_count.most_common(nKeep)] + ['?']
tok = [t if t in keep else '?' for t in tok_all]
idx = [keep.index(t) for t in tok]
```

### What this is doing mathematically

This step turns an open-ended vocabulary into a finite state space.

- `keep` is the list of the $1000$ most frequent words, plus the catch-all token `?`.
- `tok` is the corpus after rare words have been collapsed into `?`.
- `idx` is the token sequence written as integers instead of strings.

So `idx` is the actual observed Markov chain.

### Why this matters

At this point, the model is no longer about English words in the abstract. It is about transitions among the $1001$ discrete states listed in `keep`.

---

## Step 3: Estimate the transition matrix

Now create the counts:

```python
T = np.zeros((nKeep + 1, nKeep + 1))

for a, b in zip(idx[:-1], idx[1:]):
    T[a, b] += 1
```

### What this is doing

The pair `(a, b)` represents one observed adjacent transition in the corpus:

$$
w_{t-1} = a,\qquad w_t = b.
$$

So each time you see a pair, you increment that transition count.

After this loop, `T[i, j]` is not yet a probability. It is just the number of observed transitions from state $i$ to state $j$.

Now normalize each row:

```python
row_sums = T.sum(axis=1, keepdims=True)
nz = row_sums[:, 0] > 0
T[nz] /= row_sums[nz]
```

### Why row normalization is the right operation

Each row corresponds to one fixed current word $i$. The row entries are supposed to represent

$$
p(w_t = j \mid w_{t-1} = i).
$$

So for each fixed $i$, the row must sum to one over all possible next words $j$. That is exactly what row normalization accomplishes.

After this step, each nonempty row of `T` is a valid conditional probability distribution.

---

## Step 4: Answer the “five most probable followers of `miss`” question

Find the row for `miss`:

```python
miss_idx = keep.index('miss')
top5 = np.argsort(T[miss_idx])[::-1][:5]
top5_words = [keep[i] for i in top5]
```

### What this is doing

- `keep.index('miss')` finds the state index for the word `miss`.
- `T[miss_idx]` is the conditional distribution over the next word, given that the current word is `miss`.
- sorting that row in decreasing order finds the most probable followers.

### Final answer

The five most probable words to follow `miss`, in decreasing order, are:

1. `bingley`
2. `bennet`
3. `darcy`
4. `lucas`
5. `de`

These are the highest-probability entries in the `miss` row of the learned transition matrix.

### Why this answer makes sense

This corpus is *Pride and Prejudice*. So `miss` is often followed by names and title completions such as `bingley`, `bennet`, and `darcy`. That is exactly the kind of local phrase pattern a bigram model is good at capturing.

---

## Step 5: Generate sequences from the model

To sample from the Markov chain:

```python
def sample_sequence(start_word, length=50):
    seq = [start_word]
    w = keep.index(start_word)
    for _ in range(length - 1):
        w = np.random.choice(nKeep + 1, p=T[w, :])
        seq.append(keep[w])
    return seq
```

### What this is doing

This function implements the model literally.

- Start from a chosen initial word.
- Look up its row in $T$.
- Sample the next word according to that row.
- Move to that new word.
- Repeat.

Mathematically, each step samples from

$$
w_t \sim p(\cdot \mid w_{t-1}).
$$

So the generated sequence is a sample path from the learned Markov chain.

---

## Two example sequences

Using the fixed seed and starting from `miss`, two length-50 sequences are:

### Sequence 1

`miss lucas you my honour he must ? than by mr bennet replied elizabeth and what jane i could have always delight when elizabeth however did not mrs bennet she felt a doubt of their appearance of which proved beyond my news to all he lived a smile over as`

### Sequence 2

`miss bingley and ? from your uncle and will go back with herself at netherfield only ? to persuade her all this she ? me never to hear on the house they were got up her ? girl it and at their ? ? that we can hardly have no`

### Why these look strange

A bigram model only conditions on one previous word. So it can produce local phrase fragments that seem plausible while still generating globally incoherent sentences. That is not a coding error. It is the expected behavior of the model.

---

## Worked example: why the sampling rule is correct

This example is worth doing because it teaches the general logic of sampling from a conditional model.

Suppose the current word is `miss`. Then the model holds the full row

$$
T[\texttt{miss}, :]
$$

which is a conditional distribution over the next word. When `np.random.choice` samples according to that row, it produces one next-state sample consistent with the learned conditional law.

Now suppose the sampled next word is `bingley`. At that point, the state has changed. So the next row you should consult is no longer the `miss` row; it is the `bingley` row. This is exactly the Markov property in operational form: the next-step distribution depends on the current state, and once the state changes, the relevant conditional law changes with it.

### General lesson of the example

Whenever you sample from a Markov model, you should picture the process as:

1. identify the current state,
2. read off its conditional distribution for the next state,
3. sample from that distribution,
4. update the current state,
5. repeat.

The thing that stays invariant is the sampling rule. The thing that changes is the row of the matrix you are using.

---

## Misconception block

Do not confuse the following two objects:

- the **transition count matrix**
- the **transition probability matrix**

Before row normalization, the matrix contains counts, not probabilities. After row normalization, it becomes a collection of conditional distributions.

Also do not confuse:

- “the next word is usually one of these five”  
with  
- “the model understands the sentence.”

The model does not understand syntax or meaning. It only estimates local token-to-token conditional probabilities.

---

## Retain / Do Not Confuse

Retain these points:

- A bigram model is a first-order Markov chain.
- Each row of $T$ is a conditional distribution over the next word.
- Counts come first, then row normalization.
- Generation is repeated sampling from the row corresponding to the current word.

Do not confuse:

- counts with probabilities,
- vocabulary truncation with harmless preprocessing,
- local plausibility with global coherence.

---

# Problem 5. Density Estimation with Normalizing Flows

## Why this problem exists

Earlier problems dealt with discrete probability tables, Bayesian networks, and Markov chains. In all of those settings, the probabilistic objects were either small enough to write down explicitly or simple enough to estimate from counts.

This problem changes the setting completely. Now the data live in $\mathbb{R}^2$, and the target distribution is complicated enough that we can sample from it but cannot easily write its density in closed form.

So the problem introduces a new modeling idea:

> start from a simple density you understand exactly, then warp it through an invertible transformation so it becomes flexible enough to match a complex observed distribution.

That is the point of a normalizing flow.

---

## The object being introduced

The main object is a **parameterized transformed density**.

You begin with a simple base random variable

$$
Z \sim p_Z
$$

and define the observed variable by an invertible map

$$
X = f_\theta(Z),
$$

where $f_\theta$ depends on trainable parameters $\theta$.

What is fixed?

- the family of transformations you choose,
- the base distribution family,
- the target data generator,
- the model architecture.

What varies?

- the random sample $Z$,
- the observed point $X$,
- and, during training, the parameters $\theta$.

What conclusion does the object allow?

It gives you a flexible density model for $X$ whose density is still computable, so you can optimize it by likelihood.

---

## Formal definition

If $f_\theta$ is invertible, then the transformed density is

$$
p_X(x)=p_Z\!\bigl(f_\theta^{-1}(x)\bigr)\left|\det J_{f_\theta^{-1}}(x)\right|.
$$

For log density, this becomes

$$
\log p_X(x)=\log p_Z\!\bigl(f_\theta^{-1}(x)\bigr)+\log \left|\det J_{f_\theta^{-1}}(x)\right|.
$$

If the transform is a composition of layers, then the log-determinant corrections add across layers.

---

## Interpretation

This formula is easiest to understand in two pieces.

First, given an observed point $x$, map it backward to latent space using the inverse transform. That tells you where the point came from under the base distribution.

Second, correct for the fact that the transformation stretches or compresses local area. If a region is stretched out, the density must decrease there. If it is compressed, the density must increase there. The determinant term is exactly the area-scaling correction that enforces probability conservation.

So the formula is not a trick. It is the mathematical reason a flexible transformed model can still have an exactly computable density.

---

## Boundary conditions, assumptions, and failure modes

This model depends on several assumptions.

First, the transform must be invertible, at least on the relevant regions of space. If it is not invertible, then the simple one-to-one change-of-variables formula breaks.

Second, the Jacobian determinant must be tractable enough to compute, because training uses log density.

Third, the base distribution should be simple enough that both sampling and log-density evaluation are easy. A standard Gaussian is chosen exactly because it satisfies this.

Fourth, a flow is not guaranteed to perfectly fit the target generator. It is only flexible enough to approximate it. The quality of approximation depends on the chosen transform family and the optimization process.

---

## Step 1: Understand the data generator mathematically

The homework gives

```python
def sample_data(m):
    w, i = np.random.rand(m,1), np.random.rand(m,1) > 0.7
    X = np.hstack((w*.6**i + .2*i - 0.5, -2*(1-i)*(2*w-1)**2 - i + 1))
    X = 5*X + np.random.randn(m,2) * 0.1*(i+1)
    return torch.Tensor(X)
```

This is compact, so rewrite it mathematically.

First draw

$$
w \sim \mathrm{Uniform}(0,1),
\qquad
i \sim \mathrm{Bernoulli}(0.3),
$$

where $i=1$ with probability $0.3$ because the code uses the condition `> 0.7`.

Then define

$$
\mu(w,i)=
\begin{pmatrix}
w\cdot 0.6^i + 0.2i - 0.5 \\
-2(1-i)(2w-1)^2 - i + 1
\end{pmatrix}.
$$

Then add Gaussian noise and a scale factor:

$$
X = 5\,\mu(w,i) + \varepsilon,
\qquad
\varepsilon \sim \mathcal{N}\!\left(0,\ (0.1(i+1))^2 I\right).
$$

### What this means geometrically

There are two regimes.

When $i=0$, the second coordinate contains the curved term

$$
-2(2w-1)^2 + 1,
$$

so the data lie near a curved arc with smaller noise.

When $i=1$, that curved term disappears and the location becomes more line-like, with larger noise.

So the generator creates a two-component geometric structure: one curved component and one straighter, noisier component.

### Why this matters

The target distribution is clearly not just one Gaussian blob. That is exactly why a flexible density model is needed.

---

## Step 2: Plot the generative process

The homework asks for about 1000 samples from the generator.

Use:

```python
X = sample_data(1200)
X_plot = X.detach().numpy()
plt.scatter(X_plot[:,0], X_plot[:,1], s=2)
```

### What each line means

- `sample_data(1200)` generates 1200 points from the target process.
- `X` is a torch tensor, because the later modeling code uses PyTorch and Pyro.
- `detach().numpy()` converts the tensor to a NumPy array for plotting.
- `plt.scatter(...)` plots the two coordinates of the data.

### What this plot is for

This plot is not just a required figure. It is the reference distribution the model is trying to approximate.

---

## Step 3: Define the base distribution

The homework says to use a two-dimensional standard normal.

So define

```python
base = dist.MultivariateNormal(torch.zeros(2), torch.eye(2))
```

### What this means mathematically

This is

$$
Z \sim \mathcal{N}(0, I_2).
$$

- `torch.zeros(2)` is the mean vector $(0,0)$.
- `torch.eye(2)` is the $2\times 2$ identity matrix, which serves as the covariance matrix.
- `dist.MultivariateNormal(...)` creates the Pyro distribution object.

### Why this choice is natural

The base distribution should be easy to sample from and easy to evaluate. The standard Gaussian is exactly that.

But it is far too simple to match the target data by itself. So its job is not to already solve the problem. Its job is to provide raw material that the learned transform can reshape.

---

## Step 4: Sample from and plot the base distribution

Use:

```python
Z = base.sample([1000])
plt.scatter(Z[:,0], Z[:,1], s=2)
```

### What `base.sample([1000])` means

The distribution object `base` represents a single two-dimensional Gaussian random vector.

So `base.sample([1000])` means: draw 1000 independent samples from that 2D Gaussian.

The result has shape `(1000, 2)`.

### What this plot should look like

It should be a roughly circular cloud centered near the origin.

That plot matters because it tells you what the model looks like **before** any nonlinear reshaping happens.

---

## Step 5: Define the flow transform

The homework gives

```python
xform = T.spline_coupling(2, count_bins=16, bound=6)
flow = dist.TransformedDistribution(base, [xform])
```

### What this means mathematically

The transform $f_\theta$ is a learned invertible map implemented as a spline coupling layer.

The transformed distribution is

$$
X = f_\theta(Z),
\qquad Z \sim \mathcal{N}(0, I_2).
$$

So `flow` is the actual density model you will train.

### Why one coupling layer is enough here

The homework explicitly says that this transformation is flexible enough that you should not need to compose multiple transforms. That means the assignment is choosing an architecture strong enough for the task while keeping the implementation simple.

---

## Step 6: Sample from and plot the initial flow model

Use:

```python
fZ = flow.sample([1000])
plt.scatter(fZ[:,0], fZ[:,1], s=2)
```

### What this is showing

This is the model **before training**.

The transform has parameters, but they are still at their initial values. So this plot tells you what shape the chosen architecture produces before the data have influenced it.

### Why this plot matters

It separates two questions:

1. what shape can this architecture represent in principle?  
2. what shape does it actually learn after training?

The initial flow plot answers neither perfectly, but it gives a baseline before optimization begins.

---

## Step 7: Train the flow by log likelihood

The homework gives the training loop:

```python
params = xform.parameters()
steps = 2000
optimizer = torch.optim.Adam(params, lr=1e-2)

for step in range(steps+1):
    optimizer.zero_grad()
    data = sample_data(1024)

    loss = -flow.log_prob(data).mean()
    loss.backward()
    optimizer.step()
    flow.clear_cache()

    if step % 500 == 0:
        print('step: {}, loss: {}'.format(step, loss.item()))
```

### What `xform.parameters()` means

The transformation contains trainable parameters. This call collects them so the optimizer knows which quantities to update.

### What the loss means mathematically

The loss is

$$
\mathcal{L}(\theta)=-\frac{1}{m}\sum_{j=1}^{m} \log p_\theta(x_j).
$$

This is the negative average log likelihood.

Minimizing it means increasing the model’s assigned probability density on the observed data.

### Why resample fresh data each step

The homework’s generator is available directly, so the loop draws fresh minibatches from the target process. This is a convenient way to train against the true sampling process rather than one small fixed dataset.

### What `loss.backward()` and `optimizer.step()` do

- `loss.backward()` computes gradients of the loss with respect to the transform parameters.
- `optimizer.step()` takes an Adam optimization step using those gradients.

So the transform is being adjusted to make the warped Gaussian look more like the generator’s distribution.

### What `flow.clear_cache()` is doing

Pyro flow objects cache intermediate computations related to transforms and log determinants. Clearing the cache avoids stale values after parameters change.

---

## Step 8: Sample from and plot the trained flow model

After training, use:

```python
fZ = flow.sample([1000])
plt.scatter(fZ[:,0], fZ[:,1], s=2)
```

This has exactly the same syntax as the initial flow plot. What changed is not the plotting code. What changed is the parameter values inside the transform.

### What this plot should demonstrate

The trained samples should resemble the target generator more closely than:

- the base Gaussian samples, and
- the initial untrained flow samples.

The fit does not have to be perfect. The point is that the learned transformed density should now capture the main geometric structure of the target data.

---

## Final filled-in code for Problem 5

Here is the full code with the TODOs completed:

```python
import torch
import pyro
import pyro.distributions as dist
import pyro.distributions.transforms as T

np.random.seed(seed)

# Generative process plot
X = sample_data(1200)
X_plot = X.detach().numpy()
plt.scatter(X_plot[:,0], X_plot[:,1], s=2)
plt.title("Generative Process")
plt.show()

# Base distribution
base = dist.MultivariateNormal(torch.zeros(2), torch.eye(2))

Z = base.sample([1000])
plt.scatter(Z[:,0], Z[:,1], s=2)
plt.title("Base Distribution")
plt.show()

# Initial flow model
xform = T.spline_coupling(2, count_bins=16, bound=6)
flow = dist.TransformedDistribution(base, [xform])

fZ = flow.sample([1000])
plt.scatter(fZ[:,0], fZ[:,1], s=2)
plt.title("Initial Flow Model")
plt.show()

# Training
params = xform.parameters()
steps = 2000
optimizer = torch.optim.Adam(params, lr=1e-2)

for step in range(steps + 1):
    optimizer.zero_grad()
    data = sample_data(1024)

    loss = -flow.log_prob(data).mean()
    loss.backward()
    optimizer.step()
    flow.clear_cache()

    if step % 500 == 0:
        print('step: {}, loss: {}'.format(step, loss.item()))

# Trained flow model
fZ = flow.sample([1000])
plt.scatter(fZ[:,0], fZ[:,1], s=2)
plt.title("Trained Flow Model")
plt.show()
```

---

## Worked example: why the loss is the right objective

This example matters because otherwise the training loop can feel like a generic machine-learning ritual.

Suppose the current model places low density on regions where the target generator frequently produces data. Then for those data points, $\log p_\theta(x)$ will be very negative. That makes the average log probability small, so the negative average log probability becomes large.

When the optimizer reduces the loss, it is forced to change the transform so that the model assigns larger density to points that actually appear under the generator.

So the loss is not an arbitrary score. It is a direct pressure to move probability mass toward the observed data.

### General lesson of the example

Whenever you see a negative log-likelihood loss, ask:

- what distribution is assigning the probabilities?
- what data points are being scored?
- what parameters change that distribution?
- what does lowering the loss mean geometrically?

In this problem, the answer is: the learned transform is reshaping the base Gaussian so that the resulting density aligns better with the target data cloud.

---

## Misconception block

Do not confuse the following pairs of ideas.

### Base distribution vs target distribution

The base distribution is not supposed to match the target by itself. It is only the simple latent distribution you start from.

### Flow transform vs data generator

The generator produces the target data. The flow transform is the model’s attempt to imitate that distribution through a learned invertible map.

### Sample generation vs density evaluation

A model that can sample is not automatically a model with a tractable density. The whole point of the flow construction is that it gives you both.

### Better-looking plot vs exact recovery

The homework only asks for four scatterplots. So the evidence of improvement is visual. That does not mean the trained model has exactly recovered the generator’s true density.

---

## Retain / Do Not Confuse

Retain these points:

- The target generator is easy to sample from but hard to write as a simple density.
- The base Gaussian is chosen for tractability, not realism.
- The flow adds flexibility through an invertible transform.
- The change-of-variables formula is why the transformed density is computable.
- The training loss is negative average log probability.

Do not confuse:

- the target generator with the learned model,
- the base distribution with the final fitted distribution,
- sampling ability with density tractability,
- visual similarity with exact equality.

---

# Final compact answer block

## Problem 4

Corrected preprocessing and estimation code:

```python
import collections
nKeep = 1000

word_count = collections.Counter(tok_all)
keep = [w for w, cnt in word_count.most_common(nKeep)] + ['?']
tok = [t if t in keep else '?' for t in tok_all]
idx = [keep.index(t) for t in tok]

T = np.zeros((nKeep + 1, nKeep + 1))
for a, b in zip(idx[:-1], idx[1:]):
    T[a, b] += 1

row_sums = T.sum(axis=1, keepdims=True)
nz = row_sums[:, 0] > 0
T[nz] /= row_sums[nz]
```

Five most probable followers of `miss`:

1. `bingley`
2. `bennet`
3. `darcy`
4. `lucas`
5. `de`

Two example sequences starting from `miss`:

- `miss lucas you my honour he must ? than by mr bennet replied elizabeth and what jane i could have always delight when elizabeth however did not mrs bennet she felt a doubt of their appearance of which proved beyond my news to all he lived a smile over as`

- `miss bingley and ? from your uncle and will go back with herself at netherfield only ? to persuade her all this she ? me never to hear on the house they were got up her ? girl it and at their ? ? that we can hardly have no`

## Problem 5

Completed TODOs:

```python
X = sample_data(1200)
X_plot = X.detach().numpy()
plt.scatter(X_plot[:,0], X_plot[:,1], s=2)

base = dist.MultivariateNormal(torch.zeros(2), torch.eye(2))
Z = base.sample([1000])
plt.scatter(Z[:,0], Z[:,1], s=2)

xform = T.spline_coupling(2, count_bins=16, bound=6)
flow = dist.TransformedDistribution(base, [xform])

fZ = flow.sample([1000])
plt.scatter(fZ[:,0], fZ[:,1], s=2)

# training loop unchanged

fZ = flow.sample([1000])
plt.scatter(fZ[:,0], fZ[:,1], s=2)
```

The four required plots are:

1. Generative Process  
2. Base Distribution  
3. Initial Flow Model  
4. Trained Flow Model

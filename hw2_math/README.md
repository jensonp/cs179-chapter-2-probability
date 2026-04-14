# hw2_math.md

# HW2 Math-First Reconstruction

This document turns Homework 2 into a math-first workflow.

For each problem, the structure is:

1. **What the question is really asking mathematically**
2. **The math solution or derivation**
3. **The syntax that implements that math**
4. **What output the homework expects**

The goal is that you can read the math first, understand the object being manipulated, and then see the code as a direct translation.

---

# Problem 1. Factor Tables in Python

## Problem 1.1: Compute $p(T=1,D,C)$, $p(T=1,C)$, and $p(C\mid T=1)$

## Mathematical object

You begin with the full joint distribution

$$
p(T,D,C),
$$

given explicitly by the table

$$
\begin{array}{c|c|c|c}
T&D&C&p(T,D,C)\\ \hline
0&0&0&0.576\\
0&0&1&0.008\\
0&1&0&0.144\\
0&1&1&0.072\\
1&0&0&0.064\\
1&0&1&0.012\\
1&1&0&0.016\\
1&1&1&0.108
\end{array}
$$

The problem wants you to reach $p(C\mid T=1)$ in stages.

---

## Step 1: Restrict to $T=1$

Fixing $T=1$ gives the subtable

$$
p(T=1,D,C).
$$

As a $D \times C$ table:

$$
\begin{array}{c|cc}
 & C=0 & C=1\\ \hline
D=0 & 0.064 & 0.012\\
D=1 & 0.016 & 0.108
\end{array}
$$

This is **not yet** a conditional distribution. It is only the $T=1$ slice of the joint table.

---

## Step 2: Sum out $D$

Now compute

$$
p(T=1,C)=\sum_D p(T=1,D,C).
$$

So

$$
p(T=1,C=0)=0.064+0.016=0.080,
$$

$$
p(T=1,C=1)=0.012+0.108=0.120.
$$

Thus

$$
p(T=1,C)=
\begin{bmatrix}
0.080 & 0.120
\end{bmatrix}.
$$

---

## Step 3: Normalize over $C$

Now

$$
p(C\mid T=1)=\frac{p(T=1,C)}{p(T=1)}.
$$

Since

$$
p(T=1)=0.080+0.120=0.200,
$$

we get

$$
p(C=0\mid T=1)=\frac{0.080}{0.200}=0.4,
$$

$$
p(C=1\mid T=1)=\frac{0.120}{0.200}=0.6.
$$

So

$$
p(C\mid T=1)=
\begin{bmatrix}
0.4 & 0.6
\end{bmatrix}.
$$

---

## Syntax translation (pyGMs)

```python
# T=1 slice
p_T1_DC = joint.condition({T:1})      # or joint.slice({T:1})

# sum out D
p_T1_C = p_T1_DC.sum([D])             # or p_T1_DC.marginal([C])

# normalize to get p(C | T=1)
p_C_given_T1 = p_T1_C / p_T1_C.sum()
```

If your local pyGMs version prefers passing a single variable rather than a list, the mathematically intended operation is still the same:
sum over $D$, keep $C$.

---

# Problem 1.2: Verify $D \perp T \mid C$

## Mathematical statement

Conditional independence here means

$$
p(T,D,C)=p(C)\,p(D\mid C)\,p(T\mid C).
$$

So the task is to compute the three smaller factors and compare their product to the original joint table.

---

## Step 1: Compute $p(C)$

$$
p(C=0)=0.576+0.144+0.064+0.016=0.8,
$$

$$
p(C=1)=0.008+0.072+0.012+0.108=0.2.
$$

So

$$
p(C)=
\begin{bmatrix}
0.8 & 0.2
\end{bmatrix}.
$$

---

## Step 2: Compute $p(D\mid C)$

First compute $p(D,C)$.

For $C=0$:

$$
p(D=0,C=0)=0.576+0.064=0.640,\qquad
p(D=1,C=0)=0.144+0.016=0.160.
$$

For $C=1$:

$$
p(D=0,C=1)=0.008+0.012=0.020,\qquad
p(D=1,C=1)=0.072+0.108=0.180.
$$

Now divide by $p(C)$:

$$
p(D\mid C=0)=
\begin{bmatrix}
0.640/0.8\\
0.160/0.8
\end{bmatrix}
=
\begin{bmatrix}
0.8\\
0.2
\end{bmatrix},
$$

$$
p(D\mid C=1)=
\begin{bmatrix}
0.020/0.2\\
0.180/0.2
\end{bmatrix}
=
\begin{bmatrix}
0.1\\
0.9
\end{bmatrix}.
$$

So

$$
p(D\mid C)=
\begin{array}{c|cc}
 & C=0 & C=1\\ \hline
D=0 & 0.8 & 0.1\\
D=1 & 0.2 & 0.9
\end{array}
$$

---

## Step 3: Compute $p(T\mid C)$

First compute $p(T,C)$.

For $C=0$:

$$
p(T=0,C=0)=0.576+0.144=0.720,\qquad
p(T=1,C=0)=0.064+0.016=0.080.
$$

For $C=1$:

$$
p(T=0,C=1)=0.008+0.072=0.080,\qquad
p(T=1,C=1)=0.012+0.108=0.120.
$$

Now divide by $p(C)$:

$$
p(T\mid C=0)=
\begin{bmatrix}
0.720/0.8\\
0.080/0.8
\end{bmatrix}
=
\begin{bmatrix}
0.9\\
0.1
\end{bmatrix},
$$

$$
p(T\mid C=1)=
\begin{bmatrix}
0.080/0.2\\
0.120/0.2
\end{bmatrix}
=
\begin{bmatrix}
0.4\\
0.6
\end{bmatrix}.
$$

So

$$
p(T\mid C)=
\begin{array}{c|cc}
 & C=0 & C=1\\ \hline
T=0 & 0.9 & 0.4\\
T=1 & 0.1 & 0.6
\end{array}
$$

---

## Step 4: Reconstruct the joint

Now define

$$
q(T,D,C)=p(C)\,p(D\mid C)\,p(T\mid C).
$$

Because the original table was generated from exactly this structure, $q$ should match the original joint exactly.

Indeed, for example:

$$
q(1,1,1)=p(C=1)\,p(D=1\mid C=1)\,p(T=1\mid C=1)
=0.2\cdot 0.9\cdot 0.6=0.108,
$$

which matches the original table.

The same happens for every entry.

So:

- total squared error is essentially $0$,
- KL divergence is essentially $0$.

Numerically:

$$
\text{Total Sq. Err} \approx 1.33\times 10^{-32},
\qquad
\mathrm{KL}(p\|q)\approx 1.78\times 10^{-16}.
$$

These are zero up to floating-point precision.

---

## Syntax translation (pyGMs)

```python
p_C = joint.sum([T, D])

p_DC = joint.sum([T])
p_D_given_C = p_DC / p_C

p_TC = joint.sum([D])
p_T_given_C = p_TC / p_C

q = p_C * p_D_given_C * p_T_given_C

sq_err = ((joint - q)**2).sum()
kl_div = joint.distance(q, 'kl')
```

---

# Problem 1.3: Empirical estimate and structured approximation

The homework generates 50 samples from the joint, constructs an empirical estimate $\hat{p}$, then compares:

- the raw empirical estimate $\hat{p}$,
- the structured estimate

$$
  q(T,D,C)=\hat{p}(C)\hat{p}(D\mid C)\hat{p}(T\mid C).
$$

Using the fixed seed in the template, the first few samples begin:

$$
(0,1,0),\ (0,0,0),\ (0,0,0),\ (0,0,0),\ (0,1,0),\ (0,0,0),\dots
$$

Following the PDF’s stated order — **add smoothing first, then normalize** — the resulting empirical quantities are:

$$
\hat{p}(C)=
\begin{bmatrix}
0.85928144 & 0.14071856
\end{bmatrix}
$$

$$
\hat{p}(D\mid C)=
\begin{array}{c|cc}
 & C=0 & C=1\\ \hline
D=0 & 0.76713124 & 0.14539007\\
D=1 & 0.23286876 & 0.85460993
\end{array}
$$

$$
\hat{p}(T\mid C)=
\begin{array}{c|cc}
 & C=0 & C=1\\ \hline
T=0 & 0.97619048 & 0.28723404\\
T=1 & 0.02380952 & 0.71276596
\end{array}
$$

Comparing to the true joint:

$$
D(p\|\hat{p})\approx 0.12918,
\qquad
D(p\|q)\approx 0.07958.
$$

So for this sampled dataset, the **conditionally independent structured estimate $q$** is closer to the true distribution than the raw empirical estimate $\hat{p}$.

---

## Syntax translation (pyGMs)

```python
phat = gm.Factor([T,D,C], 0.)
for x in Data:
    phat[x] += 1.

# smooth, then normalize
phat += 0.1 / phat.numel()
phat /= phat.sum()

ph_C = phat.sum([T, D])

ph_DC = phat.sum([T])
ph_D_given_C = ph_DC / ph_C

ph_TC = phat.sum([D])
ph_T_given_C = ph_TC / ph_C

q = ph_C * ph_D_given_C * ph_T_given_C

kl_p_phat = joint.distance(phat, 'kl')
kl_p_q    = joint.distance(q, 'kl')
```

---

# Problem 2. Expressing a Model in Pyro

## Mathematical model

The Wet Grass Bayesian network factorizes as

$$
p(C,S,R,W)=p(C)\,p(S\mid C)\,p(R\mid C)\,p(W\mid R,S).
$$

Given in the prompt:

$$
p(C=1)=0.5.
$$

$$
p(S=1\mid C=0)=0.5,\qquad p(S=1\mid C=1)=0.1.
$$

$$
p(R=1\mid C=0)=0.2,\qquad p(R=1\mid C=1)=0.8.
$$

$$
p(W=1\mid R=S=0)=0,\qquad
p(W=1\mid R=1,S=0)=0.9,
$$

$$
p(W=1\mid R=0,S=1)=0.9,\qquad
p(W=1\mid R=S=1)=0.99.
$$

---

## Exact marginals from math

The exact target values are:

$$
p(C=1)=0.5
$$

$$
p(S=1)=0.5\cdot 0.5 + 0.5\cdot 0.1 = 0.3
$$

$$
p(R=1)=0.5\cdot 0.2 + 0.5\cdot 0.8 = 0.5
$$

$$
p(S=1,R=1)=0.5\cdot(0.5)(0.2)+0.5\cdot(0.1)(0.8)=0.09
$$

For $p(W=1)$, sum over all values of $C,S,R$:

$$
p(W=1)=0.6471.
$$

So the empirical estimates from 1000 samples should be near:

$$
\hat{p}(C=1)\approx 0.5,\quad
\hat{p}(S=1)\approx 0.3,\quad
\hat{p}(R=1)\approx 0.5,\quad
\hat{p}(W=1)\approx 0.6471,
$$

$$
\hat{p}(S=1,R=1)\approx 0.09.
$$

---

## Syntax translation (Pyro)

```python
import pyro
import pyro.distributions as dist
import torch

def model():
    c = pyro.sample("C", dist.Bernoulli(torch.tensor(0.5)))

    p_s = 0.1 if c.item() == 1 else 0.5
    s = pyro.sample("S", dist.Bernoulli(torch.tensor(p_s)))

    p_r = 0.8 if c.item() == 1 else 0.2
    r = pyro.sample("R", dist.Bernoulli(torch.tensor(p_r)))

    if r.item() == 0 and s.item() == 0:
        p_w = 0.0
    elif r.item() == 1 and s.item() == 0:
        p_w = 0.9
    elif r.item() == 0 and s.item() == 1:
        p_w = 0.9
    else:
        p_w = 0.99

    w = pyro.sample("W", dist.Bernoulli(torch.tensor(p_w)))
    return (c, s, r, w)
```

Then draw samples and estimate probabilities:

```python
D = [model() for _ in range(1000)]

p_C = np.mean([d[0].item() for d in D])
p_S = np.mean([d[1].item() for d in D])
p_R = np.mean([d[2].item() for d in D])
p_W = np.mean([d[3].item() for d in D])

p_SR = np.mean([(d[1].item() == 1) and (d[2].item() == 1) for d in D])
```

---

# Problem 3. Building Power Bayes Net

This is a **graph reasoning** problem, not a numerical table problem.

The key rule is d-separation.

Because the graph is a **polytree**, there is exactly one undirected path between any two nodes. So for each yes/no question, you only need to inspect that one path and decide whether it is blocked or active.

---

## (a) Can projector_plugged_in affect sam_reading_book?

### Answer
**No.**

### Why
The only path is blocked at the **collider** $power\_in\_wire$:

$$
projector\_plugged\_in \rightarrow power\_in\_wire \leftarrow power\_in\_building \rightarrow light\_switch\_on \rightarrow room\_light\_on \rightarrow sam\_reading\_book.
$$

Since neither the collider nor one of its descendants is observed, the path is blocked.

---

## (b) Can screen_lit_up affect sam_reading_book?

### Answer
**Yes.**

### Why
There is an active path:

$$
screen\_lit\_up \leftarrow projector\_lamp\_on \leftarrow power\_in\_projector
\leftarrow power\_in\_wire \leftarrow power\_in\_building
\rightarrow light\_switch\_on \rightarrow room\_light\_on \rightarrow sam\_reading\_book.
$$

This path consists of serial and diverging connections with no blocking evidence on the intermediate nodes.

---

## (c) Can projector_plugged_in affect sam_reading_book given screen_lit_up observed?

### Answer
**Yes.**

### Why
The same path from part (a) becomes active because $screen\_lit\_up$ is a **descendant** of the collider $power\_in\_wire$, and observing a descendant of a collider opens the path:

$$
projector\_plugged\_in \rightarrow power\_in\_wire \leftarrow power\_in\_building
\rightarrow light\_switch\_on \rightarrow room\_light\_on \rightarrow sam\_reading\_book.
$$

---

## (d) Which variables could change if just lamp_works is observed?

### Answer
The variables whose probabilities could change are:

- $projector\_lamp\_on$
- $screen\_lit\_up$
- $ray\_says\_screen\_is\_dark$

This follows the active downstream path from the observed node.

---

## (e) Which variables could change if just power_in_projector is observed?

### Answer
Observing $power\_in\_projector$ can affect **all variables except**:

- $light\_switch\_on$
- $lamp\_works$
- $mirror\_working$
- $ray\_is\_awake$

So, equivalently, it can affect the rest of the graph.

There is no code required here. The output is your yes/no choices and path explanations.

---

# Problem 4. Bigram Text Models

## Mathematical model

A bigram model is a first-order Markov chain:

$$
p(w_1,\dots,w_n)=p(w_1)\prod_{t=2}^n p(w_t\mid w_{t-1}).
$$

The core object is the transition matrix

$$
T[i,j]=p(w_t=j\mid w_{t-1}=i).
$$

You estimate it from counts:

$$
T[i,j]=\frac{\#(i\to j)}{\sum_k \#(i\to k)}.
$$

---

## Important template fix

In the visible code template, this line appears:
```python
word_count = collections.Counter(tok)
```

But at that point, `tok` has not yet been defined.

The mathematically correct thing is to count from the cleaned full token list:
```python
word_count = collections.Counter(tok_all)
```

Then define `keep`, then define `tok`, then define `idx`.

---

## Actual transition answer for the word `miss`

Using the provided text file, keeping the top 1000 words and replacing the rest with `?`, the five most probable followers of `miss` are:

1. `bingley`
2. `bennet`
3. `darcy`
4. `lucas`
5. `de`

These come from the largest probabilities in the row corresponding to `miss`.

---

## Syntax translation (NumPy)

```python
import collections
nKeep = 1000

word_count = collections.Counter(tok_all)
keep = [w for w,cnt in word_count.most_common(nKeep)] + ['?']
tok = [t if t in keep else '?' for t in tok_all]
idx = [keep.index(t) for t in tok]

T = np.zeros((nKeep+1, nKeep+1))
for a, b in zip(idx[:-1], idx[1:]):
    T[a, b] += 1

row_sums = T.sum(axis=1, keepdims=True)
nz = row_sums[:,0] > 0
T[nz] /= row_sums[nz]
```

To get the five most likely followers of `miss`:

```python
miss_idx = keep.index('miss')
top5 = np.argsort(T[miss_idx])[::-1][:5]
top5_words = [keep[i] for i in top5]
```

---

## Two example generated sequences

The homework says you may choose the starting word yourself.

If we choose `miss` and use the fixed seed, two sample 50-word sequences are:

### Sequence 1
`miss bennet you must immediately and a moment or ? by receiving his going to be ? she might do you the ? ? and with their ? ? her behaviour there for good time when first ? to herself and if you that it likewise seen him without ?`

### Sequence 2
`miss elizabeth still ? of doing it you may not help ? know mr bingley himself on the superior ? she ? about as well and ? why come to her as he must give her so ? for our time they ? which was prevented his affectionate and aunt`

Because the model is stochastic, any correct implementation can generate different sequences.

To generate sequences:

```python
def sample_sequence(start_word, length=50):
    seq = [start_word]
    w = keep.index(start_word)
    for _ in range(length-1):
        w = np.random.choice(nKeep+1, p=T[w,:])
        seq.append(keep[w])
    return seq

seq1 = sample_sequence('miss', 50)
seq2 = sample_sequence('miss', 50)
```

---

# Problem 5. Density Estimation with Normalizing Flows

This problem is easiest if you separate three levels:

1. the **data generator**
2. the **base distribution**
3. the **invertible flow transform**

---

## Step 1: Mathemize the generative process

The data come from a two-component mixture-like latent mechanism.

Let

$$
i \sim \text{Bernoulli}(0.3),
\qquad
w \sim \text{Uniform}(0,1).
$$

Define the mean curve

$$
\mu(w,i)=
\begin{pmatrix}
w\cdot 0.6^i + 0.2i - 0.5\\\
-2(1-i)(2w-1)^2 - i + 1
\end{pmatrix}.
$$

Then

$$
X = 5\mu(w,i) + \varepsilon,
\qquad
\varepsilon \sim \mathcal N\!\left(0,\ (0.1(i+1))^2 I\right).
$$

Interpretation:

- when $i=0$ (probability $0.7$), the mean trace is parabolic with smaller noise,
- when $i=1$ (probability $0.3$), the mean trace is more linear with larger noise.

The point is that we can **sample** from this process, but we do not have an easy analytic density formula for the resulting $X$. That is why we fit a flexible density model instead.

---

## Step 2: Base distribution

Choose a simple 2D isotropic Gaussian:

$$
Z \sim \mathcal N(0, I_2).
$$

Its density is

$$
p_Z(z)=\frac{1}{2\pi}\exp\!\left(-\frac12 \|z\|^2\right).
$$

### Syntax

```python
base = dist.MultivariateNormal(torch.zeros(2), torch.eye(2))
Z = base.sample([1000])
plt.scatter(Z[:,0], Z[:,1], s=2)
```

---

## Step 3: Flow model as change of variables

Define an invertible learned transform

$$
x = f_\theta(z).
$$

Then the transformed density is

$$
p_X(x) = p_Z(f_\theta^{-1}(x))
\left|\det J_{f_\theta^{-1}}(x)\right|.
$$

This is the exact mathematical reason the model remains trainable: the transformed density is still computable.

In the homework, the transform is a spline coupling layer.

### Syntax

```python
xform = T.spline_coupling(2, count_bins=16, bound=6)
flow = dist.TransformedDistribution(base, [xform])

fZ = flow.sample([1000])
plt.scatter(fZ[:,0], fZ[:,1], s=2)
```

This gives the **initial, untrained flow model**.

---

## Step 4: Data plot

### Syntax

```python
X = sample_data(1200)
X_plot = X.detach().numpy()
plt.scatter(X_plot[:,0], X_plot[:,1], s=2)
```

This gives the **Generative Process** plot.

---

## Step 5: Training objective

The training loop is already given:

$$
\mathcal L(\theta)
=
-\frac{1}{m}\sum_{j=1}^m \log p_{X,\theta}(x_j).
$$

In code:
```python
loss = -flow.log_prob(data).mean()
```

Minimizing this means making the flow assign higher probability to data coming from the generator.

---

## Step 6: Post-training samples

After training, sample from the trained flow:

```python
fZ = flow.sample([1000])
plt.scatter(fZ[:,0], fZ[:,1], s=2)
```

This gives the **Trained Flow Model** plot.

---

## The four required outputs for Problem 5

The homework wants four scatterplots:

1. **Generative Process**
2. **Base Distribution**
3. **Initial Flow Model**
4. **Trained Flow Model**

So the “answer” here is not a single scalar. The answer is the completed syntax that generates those four figures, together with the mathematical interpretation above.

---

# Final compact answer map

## Problem 1 final quantitative answers

$$
p(T=1,D,C)=
\begin{array}{c|cc}
 & C=0 & C=1\\ \hline
D=0 & 0.064 & 0.012\\
D=1 & 0.016 & 0.108
\end{array}
$$

$$
p(T=1,C)=
\begin{bmatrix}
0.080 & 0.120
\end{bmatrix}
$$

$$
p(C\mid T=1)=
\begin{bmatrix}
0.4 & 0.6
\end{bmatrix}
$$

$$
p(C)=
\begin{bmatrix}
0.8 & 0.2
\end{bmatrix}
$$

$$
p(D\mid C)=
\begin{array}{c|cc}
 & C=0 & C=1\\ \hline
D=0 & 0.8 & 0.1\\
D=1 & 0.2 & 0.9
\end{array}
$$

$$
p(T\mid C)=
\begin{array}{c|cc}
 & C=0 & C=1\\ \hline
T=0 & 0.9 & 0.4\\
T=1 & 0.1 & 0.6
\end{array}
$$

$$
\text{Total Sq. Err}\approx 1.33\times 10^{-32},
\qquad
\mathrm{KL}\approx 1.78\times 10^{-16}.
$$

Empirical comparison:

$$
D(p\|\hat{p})\approx 0.12918,
\qquad
D(p\|q)\approx 0.07958.
$$

So $q$ is closer.

---

## Problem 2 target values

$$
p(C=1)=0.5,\quad
p(S=1)=0.3,\quad
p(R=1)=0.5,\quad
p(W=1)=0.6471,
$$

$$
p(S=1,R=1)=0.09.
$$

---

## Problem 3 answers

- (a) **No**
- (b) **Yes**
- (c) **Yes**
- (d) affected: $projector\_lamp\_on,\ screen\_lit\_up,\ ray\_says\_screen\_is\_dark$
- (e) affected: all except $light\_switch\_on,\ lamp\_works,\ mirror\_working,\ ray\_is\_awake$

---

## Problem 4 answer

Top five followers of `miss`:

1. `bingley`
2. `bennet`
3. `darcy`
4. `lucas`
5. `de`

---

## Problem 5 answer

Complete the TODOs so the code generates the four scatterplots. The mathematically essential completions are:

```python
# target data
X = sample_data(1200)
X_plot = X.detach().numpy()
plt.scatter(X_plot[:,0], X_plot[:,1], s=2)

# base distribution
base = dist.MultivariateNormal(torch.zeros(2), torch.eye(2))
Z = base.sample([1000])
plt.scatter(Z[:,0], Z[:,1], s=2)

# flow
xform = T.spline_coupling(2, count_bins=16, bound=6)
flow = dist.TransformedDistribution(base, [xform])

# untrained samples
fZ = flow.sample([1000])
plt.scatter(fZ[:,0], fZ[:,1], s=2)

# trained samples
fZ = flow.sample([1000])
plt.scatter(fZ[:,0], fZ[:,1], s=2)
```

The training loop already supplies the optimization logic.

---

# How to use this file

If you want the fastest working path:

- read the math block first,
- then copy only the **syntax translation** block for that problem,
- then run it,
- then compare your output to the “final compact answer map” at the end.

This keeps the code tied to the probability meaning the whole way through.

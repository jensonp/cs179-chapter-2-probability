# Chapter 3 Graphs (Graphviz DOT)

This folder contains one DOT file per distinct graphical-structure example/pattern in `../README.md`.

Each DOT graph preserves the original variable symbols (or the closest ASCII-safe identifier when the text uses tildes) and keeps edge directions exactly as stated.

## 1) Burglar alarm network (`burglar_alarm.dot`)

Parents / children:

- Parents of `A`: `B`, `E`
- Parent of `W`: `A`
- Parent of `H`: `A`

Key probabilistic point:

- Encodes the factorization `p(B,E,A,W,H)=p(B)p(E)p(A|B,E)p(W|A)p(H|A)`.
- Illustrates fork vs collider behavior: `B ⟂ E` marginally (collider at `A`), but typically `B` and `E` become dependent given `A` (or a descendant like `W`).
- Illustrates screening-off: `W ⟂ H | A`.

## 2) Chain / fork / collider motifs (`motif_chain.dot`, `motif_fork.dot`, `motif_collider.dot`)

Key probabilistic point:

- Chain `X → Z → Y`: path active unless you condition on `Z`; implies `X ⟂ Y | Z` (when this is the only connecting path).
- Fork `X ← Z → Y`: common-cause dependence; conditioning on `Z` blocks; implies `X ⟂ Y | Z` (when this is the only connecting path).
- Collider `X → Z ← Y`: blocked by default; conditioning on `Z` (or a descendant) opens; often `X ⟂ Y` but `X ⟂̸ Y | Z`.

## 3) Markov-equivalence 3-node graphs (`markov_equiv_chain.dot`, `markov_equiv_fork.dot`, `markov_equiv_reverse_chain.dot`, `markov_non_equiv_collider.dot`)

Key probabilistic point:

- The first three graphs are Markov equivalent: they all imply `A ⟂ C | B` and do not imply marginal independence of `A` and `C`.
- The collider `A → B ← C` is not equivalent: it implies `A ⟂ C` marginally but (typically) `A ⟂̸ C | B`.

## 4) Naive Bayes template (`naive_bayes_4_features.dot`)

Key probabilistic point:

- One class label `Y` is a parent of all features `X_i`.
- Features are conditionally independent given `Y`: `X_i ⟂ X_j | Y` for `i≠j` (as a modeling assumption).

This DOT instantiates a small concrete example with four features to make the pattern explicit.

## 5) Markov chain template (`markov_chain_5.dot`)

Key probabilistic point:

- First-order dependence along a sequence: `X_{t-1} → X_t`.
- Encodes `p(X_1,…,X_n)=p(X_1)∏_{t=2}^n p(X_t|X_{t-1})`.

This DOT instantiates a 5-node chain as an illustrative expansion of the general form.

## 6) Noisy-OR headache example (`noisy_or_headache.dot`)

Key probabilistic point:

- Many causes (`C`, `F`, `D`) point to one effect (`H`).
- The intended semantics is a structured CPT (noisy-OR), not an arbitrary full table.

## 7) Noisy-OR auxiliary-variable rewrite (`noisy_or_auxiliary.dot`)

Key probabilistic point:

- Introduces auxiliary success variables (written as `C̃`, `F̃`, `D̃`) and intermediate OR nodes to ensure no node has more than two parents.
- This rewrite can preserve the observable conditional `p(H|C,F,D)` while changing the graph by adding latent intermediates.

## 8) Confounding (causality preview) (`confounding_U_X_Y.dot`)

Key probabilistic point:

- Shows the structural reason `p(Y|X)` can differ from `p(Y|do(X))` when there is a hidden common cause `U` of both `X` and `Y`.


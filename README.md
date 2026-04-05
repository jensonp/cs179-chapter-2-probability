# Chapter 2 Probability Reconstruction

This repository publishes a layered reconstruction of Chapter 2, "Probability and Inference", from the local course notes workspace.

The tracked content is intentionally limited to the Chapter 2 reconstruction bundle. The rest of the original `cs179` workspace remains local and is excluded from version control by default.

## Main Note Table of Contents

The chapter is now available both as one long note and as root-level rendered subsection folders.

One-file version:

- [`02_probability_main/`](./02_probability_main/): full monolithic chapter

Section-by-section version:

1. [`02_probability_00_front_matter_and_scope/`](./02_probability_00_front_matter_and_scope/): front matter, scope, notation, and how to use the chapter
2. [`02_probability_01_probability_space_events_and_random_variables/`](./02_probability_01_probability_space_events_and_random_variables/): probability spaces, events, axioms, and random variables
3. [`02_probability_02_discrete_pmf_indicator_and_geometric/`](./02_probability_02_discrete_pmf_indicator_and_geometric/): PMFs, indicator notation, Bernoulli, categorical, and geometric distributions
4. [`02_probability_03_joint_tables_conditioning_bayes_and_total_probability/`](./02_probability_03_joint_tables_conditioning_bayes_and_total_probability/): joint tables, marginalization, conditioning, Bayes, and total probability
5. [`02_probability_04_expectation_variance_covariance_and_independence/`](./02_probability_04_expectation_variance_covariance_and_independence/): expectation, variance, covariance, independence, and conditional independence
6. [`02_probability_05_continuous_random_variables/`](./02_probability_05_continuous_random_variables/): CDF/PDF distinctions, Gaussian models, Beta, and Dirichlet
7. [`02_probability_06_learning_and_parameter_estimation/`](./02_probability_06_learning_and_parameter_estimation/): likelihood, MLE, Bayesian posteriors, and model selection
8. [`02_probability_07_convexity/`](./02_probability_07_convexity/): convexity background for estimation objectives
9. [`02_probability_08_information_theory/`](./02_probability_08_information_theory/): entropy, conditional entropy, mutual information, and KL divergence
10. [`02_probability_09_change_of_variable_models/`](./02_probability_09_change_of_variable_models/): scalar and multivariate Jacobians, copulas, and normalizing flows

Companion materials:

- [`02_probability_formal_supplement/`](./02_probability_formal_supplement/): formal supplement
- [`02_probability_exercises/`](./02_probability_exercises/): exercises
- [`02_probability_computational_appendix/`](./02_probability_computational_appendix/): computational appendix
- [`hw1_reading_guide/`](./hw1_reading_guide/): explicit reading instructions for Homework 1

## HW1 LaTeX Preview

To set up the Homework 1 LaTeX live-preview workspace in VS Code, run from the repository root:

- macOS / Linux: `python3 scripts/setup_hw1_latex_workspace.py`
- Windows: `py -3 scripts\\setup_hw1_latex_workspace.py`

That writes a dedicated `hw1-latex.code-workspace` plus the `.vscode` build settings inside `output/overleaf/cs179-hw1-project/`.
The HW1 project is organized into `source/` for editable files and `build/` for generated PDFs/logs.

## Source Layout

- `02_probability_main/README.md`: main reconstructed chapter source
- `02_probability_00_front_matter_and_scope/README.md` through `02_probability_09_change_of_variable_models/README.md`: section-by-section GitHub-rendered chapter reads
- `02_probability_formal_supplement/README.md`: formal definitions and proof spine
- `02_probability_exercises/README.md`: layered exercise bank
- `02_probability_computational_appendix/README.md`: numerical workflows and implementation checks
- `notes/02_probability_reconstructed/source/02_probability.pdf`: source notes PDF used for clipping figures
- `notes/02_probability_reconstructed/assets/`: extracted figures and native diagram assets
- `scripts/notes/build_02_probability_reconstructed.py`: chapter build script

## Build

Run from the repository root.

- Full local PDF build: `python3 scripts/notes/build_02_probability_bundle.py`
- Main note: `python3 scripts/notes/build_02_probability_reconstructed.py`
- Formal supplement: `python3 scripts/notes/build_02_probability_reconstructed.py --markdown 02_probability_formal_supplement/README.md --output-pdf notes/02_probability_reconstructed/dist/02_probability.formal_supplement.pdf --subtitle "Formal Supplement"`
- Exercises: `python3 scripts/notes/build_02_probability_reconstructed.py --markdown 02_probability_exercises/README.md --output-pdf notes/02_probability_reconstructed/dist/02_probability.exercises.pdf --subtitle "Exercises"`
- Computational appendix: `python3 scripts/notes/build_02_probability_reconstructed.py --markdown 02_probability_computational_appendix/README.md --output-pdf notes/02_probability_reconstructed/dist/02_probability.computational_appendix.pdf --subtitle "Computational Appendix"`

The bundle build script regenerates local PDFs in `notes/02_probability_reconstructed/dist/`. Those PDFs are build artifacts and are no longer committed to the repository.

The renderer uses PyMuPDF to clip figures from the source PDF, regenerate native assets for the sequential-updating figure, and render any of the chapter markdown companions into PDF.

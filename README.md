# Chapter 2 Probability Reconstruction

This repository publishes a layered reconstruction of Chapter 2, "Probability and Inference", from the local course notes workspace.

The tracked content is intentionally limited to the Chapter 2 reconstruction bundle. The rest of the original `cs179` workspace remains local and is excluded from version control by default.

## Read These On GitHub

If you want GitHub to render each note automatically, open:

- `02_probability_main/`: rendered main note
- `02_probability_formal_supplement/`: rendered formal supplement
- `02_probability_exercises/`: rendered exercises
- `02_probability_computational_appendix/`: rendered computational appendix
- `hw1_reading_guide/`: explicit reading instructions for Homework 1

If you only want one file, start with `02_probability_main/`.
If you want the homework-specific reading flow, start with `hw1_reading_guide/`.

## HW1 LaTeX Preview

To set up the Homework 1 LaTeX live-preview workspace in VS Code, run from the repository root:

- macOS / Linux: `python3 scripts/setup_hw1_latex_workspace.py`
- Windows: `py -3 scripts\\setup_hw1_latex_workspace.py`

That writes a dedicated `hw1-latex.code-workspace` plus the `.vscode` build settings inside `output/overleaf/cs179-hw1-project/`.
The HW1 project is organized into `source/` for editable files and `build/` for generated PDFs/logs.

## Source Layout

- `02_probability_main/README.md`: main reconstructed chapter source
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

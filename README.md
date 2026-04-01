# Chapter 2 Probability Reconstruction

This repository publishes a layered reconstruction of Chapter 2, "Probability and Inference", from the local course notes workspace.

The tracked content is intentionally limited to the Chapter 2 reconstruction bundle. The rest of the original `cs179` workspace remains local and is excluded from version control by default.

## Layout

- `notes/02_probability_reconstructed/02_probability.reconstructed.md`: main reconstructed chapter source
- `notes/02_probability_reconstructed/02_probability.formal_supplement.md`: formal definitions and proof spine
- `notes/02_probability_reconstructed/02_probability.exercises.md`: layered exercise bank
- `notes/02_probability_reconstructed/02_probability.computational_appendix.md`: numerical workflows and implementation checks
- `notes/02_probability_reconstructed/source/02_probability.pdf`: source notes PDF used for clipping figures
- `notes/02_probability_reconstructed/assets/`: extracted figures and native diagram assets
- `notes/02_probability_reconstructed/dist/02_probability.reconstructed.pdf`: rendered output
- `notes/02_probability_reconstructed/dist/02_probability.formal_supplement.pdf`: rendered formal supplement
- `notes/02_probability_reconstructed/dist/02_probability.exercises.pdf`: rendered exercises
- `notes/02_probability_reconstructed/dist/02_probability.computational_appendix.pdf`: rendered computational appendix
- `scripts/notes/build_02_probability_reconstructed.py`: chapter build script

## Build

Run from the repository root.

- Main note: `python3 scripts/notes/build_02_probability_reconstructed.py`
- Formal supplement: `python3 scripts/notes/build_02_probability_reconstructed.py --markdown notes/02_probability_reconstructed/02_probability.formal_supplement.md --output-pdf notes/02_probability_reconstructed/dist/02_probability.formal_supplement.pdf --subtitle "Formal Supplement"`
- Exercises: `python3 scripts/notes/build_02_probability_reconstructed.py --markdown notes/02_probability_reconstructed/02_probability.exercises.md --output-pdf notes/02_probability_reconstructed/dist/02_probability.exercises.pdf --subtitle "Exercises"`
- Computational appendix: `python3 scripts/notes/build_02_probability_reconstructed.py --markdown notes/02_probability_reconstructed/02_probability.computational_appendix.md --output-pdf notes/02_probability_reconstructed/dist/02_probability.computational_appendix.pdf --subtitle "Computational Appendix"`

The build script uses PyMuPDF to clip figures from the source PDF, regenerate native assets for the sequential-updating figure, and render any of the chapter markdown companions into PDF.

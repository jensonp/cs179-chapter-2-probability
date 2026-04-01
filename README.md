# Chapter 2 Probability Reconstruction

This repository publishes a self-contained reconstruction of Chapter 2, "Probability and Inference", from the local course notes workspace.

The tracked content is intentionally limited to the Chapter 2 reconstruction bundle. The rest of the original `cs179` workspace remains local and is excluded from version control by default.

## Layout

- `notes/02_probability_reconstructed/02_probability.reconstructed.md`: reconstructed chapter source
- `notes/02_probability_reconstructed/source/02_probability.pdf`: source notes PDF used for clipping figures
- `notes/02_probability_reconstructed/assets/`: extracted figures and native diagram assets
- `notes/02_probability_reconstructed/dist/02_probability.reconstructed.pdf`: rendered output
- `scripts/notes/build_02_probability_reconstructed.py`: chapter build script

## Build

Run from the repository root:

```bash
python3 scripts/notes/build_02_probability_reconstructed.py
```

The build script uses PyMuPDF to clip figures from the source PDF, regenerate native assets for the sequential-updating figure, and render the reconstructed markdown into the final PDF.

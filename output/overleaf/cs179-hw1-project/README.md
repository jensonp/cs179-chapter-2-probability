# CS179 HW1 Overleaf Project

Layout:
- `source/main.tex`: entry point for TeX compilation.
- `source/answers.toml`: source of truth for the local deterministic workflow.
- `source/answers.tex`: generated answer placements that get placed into the original homework boxes.
- `source/cs179-hw1.pdf`: original homework PDF used as the exact page background.
- `build/`: generated PDF/log/intermediate files.

Workflow options:
1. Local deterministic workflow: edit `source/answers.toml`, then run
   `python3 /Users/jensonphan/cs179/output/overleaf/cs179-hw1-project/.vscode/build_hw1.py /Users/jensonphan/cs179/output/overleaf/cs179-hw1-project/source/main.tex`
   to regenerate `source/answers.tex` and compile the PDF into `build/`.
2. Overleaf-only/manual debugging: edit `answers.tex` directly, but local builds will overwrite it unless
   `build_hw1.py` is run with `--no-regenerate`.

Notes:
- Answer content is raw LaTeX, so math, aligned equations, and `\includegraphics` all work.
- Keep short answer fields inline. Use `*_work`, `*_reasoning`, and notes fields for multi-line derivations or `$$...$$`.
- Checkbox markers accept `\Checkmark` in `source/answers.tex`, or `true` / `false` in `source/answers.toml`.
- The layout is faithful because the original `source/cs179-hw1.pdf` is embedded page-for-page.

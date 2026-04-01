#!/usr/bin/env python3

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BUILD_SCRIPT = ROOT / "scripts/notes/build_02_probability_reconstructed.py"

DOCS = [
    {
        "markdown": ROOT / "notes/02_probability_reconstructed/02_probability.reconstructed.md",
        "output": ROOT / "notes/02_probability_reconstructed/dist/02_probability.reconstructed.pdf",
        "root_pdf": ROOT / "02_probability_main.pdf",
        "subtitle": None,
    },
    {
        "markdown": ROOT / "notes/02_probability_reconstructed/02_probability.formal_supplement.md",
        "output": ROOT / "notes/02_probability_reconstructed/dist/02_probability.formal_supplement.pdf",
        "root_pdf": ROOT / "02_probability_formal_supplement.pdf",
        "subtitle": "Formal Supplement",
    },
    {
        "markdown": ROOT / "notes/02_probability_reconstructed/02_probability.exercises.md",
        "output": ROOT / "notes/02_probability_reconstructed/dist/02_probability.exercises.pdf",
        "root_pdf": ROOT / "02_probability_exercises.pdf",
        "subtitle": "Exercises",
    },
    {
        "markdown": ROOT / "notes/02_probability_reconstructed/02_probability.computational_appendix.md",
        "output": ROOT / "notes/02_probability_reconstructed/dist/02_probability.computational_appendix.pdf",
        "root_pdf": ROOT / "02_probability_computational_appendix.pdf",
        "subtitle": "Computational Appendix",
    },
]


def run_build(markdown: Path, output: Path, subtitle: str | None) -> None:
    cmd = [
        sys.executable,
        str(BUILD_SCRIPT),
        "--markdown",
        str(markdown.relative_to(ROOT)),
        "--output-pdf",
        str(output.relative_to(ROOT)),
    ]
    if subtitle is not None:
        cmd.extend(["--subtitle", subtitle])
    subprocess.run(cmd, check=True, cwd=ROOT)


def main() -> None:
    for doc in DOCS:
        run_build(doc["markdown"], doc["output"], doc["subtitle"])
        shutil.copy2(doc["output"], doc["root_pdf"])
        print(doc["root_pdf"].relative_to(ROOT))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BUILD_SCRIPT = ROOT / "scripts/notes/build_02_probability_reconstructed.py"

DOCS = [
    {
        "markdown": ROOT / "02_probability_main/README.md",
        "output": ROOT / "notes/02_probability_reconstructed/dist/02_probability.reconstructed.pdf",
        "subtitle": None,
    },
    {
        "markdown": ROOT / "02_probability_formal_supplement/README.md",
        "output": ROOT / "notes/02_probability_reconstructed/dist/02_probability.formal_supplement.pdf",
        "subtitle": "Formal Supplement",
    },
    {
        "markdown": ROOT / "02_probability_exercises/README.md",
        "output": ROOT / "notes/02_probability_reconstructed/dist/02_probability.exercises.pdf",
        "subtitle": "Exercises",
    },
    {
        "markdown": ROOT / "02_probability_computational_appendix/README.md",
        "output": ROOT / "notes/02_probability_reconstructed/dist/02_probability.computational_appendix.pdf",
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
        print(doc["output"].relative_to(ROOT))


if __name__ == "__main__":
    main()

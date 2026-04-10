#!/usr/bin/env python3

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BUILD_SCRIPT = ROOT / "scripts/notes/build_02_probability_reconstructed.py"

MARKDOWN = ROOT / "03_bayesnet_main/README.md"
SOURCE_PDF = ROOT / "notes/03_bayesnet_reconstructed/source/03_bayesnet.original.pdf"
ASSETS_DIR = ROOT / "notes/03_bayesnet_reconstructed/assets"
OUTPUT_PDF = ROOT / "notes/03_bayesnet_reconstructed/dist/03_bayesnet.reconstructed.pdf"


def main() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable,
        str(BUILD_SCRIPT),
        "--markdown",
        str(MARKDOWN.relative_to(ROOT)),
        "--source-pdf",
        str(SOURCE_PDF.relative_to(ROOT)),
        "--assets-dir",
        str(ASSETS_DIR.relative_to(ROOT)),
        "--output-pdf",
        str(OUTPUT_PDF.relative_to(ROOT)),
        "--title",
        "Bayesian Networks",
        "--subtitle",
        "Reconstructed Chapter",
    ]
    subprocess.run(cmd, check=True, cwd=ROOT)
    print(OUTPUT_PDF.relative_to(ROOT))


if __name__ == "__main__":
    main()


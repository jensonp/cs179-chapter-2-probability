#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path("/Users/jensonphan/cs179")
DEFAULT_PATHS = [
    ROOT / "02_probability_main" / "README.md",
]


ERROR_PATTERNS = [
    (
        "raw render error marker",
        re.compile(r"Unable to render expression"),
        "Remove the broken-render marker and fix the source math.",
    ),
    (
        "unsupported cases environment",
        re.compile(r"\\begin\{cases\}|\\end\{cases\}"),
        "Rewrite piecewise definitions as prose, inline math, or HTML tables.",
    ),
    (
        "unbraced hat command",
        re.compile(r"\\hat(?!\{)"),
        "Use braced form like \\hat{\\theta}, or safer renderer-stable notation.",
    ),
    (
        "plain text glued to math",
        re.compile(r"\b[A-Za-z]+[$][(]"),
        "Write the whole expression in math mode, for example $\\mathrm{Beta}(2,2)$.",
    ),
    (
        "unsupported latex math delimiters",
        re.compile(r"\\\(|\\\)|\\\[|\\\]"),
        "Use only $...$ for inline math and $$...$$ for display math in GitHub markdown.",
    ),
]

ADVISORY_PATTERNS = [
    (
        "display math uses text command",
        re.compile(r"^\s*\$\$.*\\text\{.*\}\s*\$\$\s*$"),
        "GitHub usually handles this, but short expressions are safer as inline math or prose.",
    ),
    (
        "display math uses qquad spacing",
        re.compile(r"^\s*\$\$.*\\qquad.*\$\$\s*$"),
        "Wide spacing inside a short display block can be fragile on GitHub. Prefer inline math or separate formulas.",
    ),
]


def iter_lines(path: Path):
    text = path.read_text()
    lines = text.splitlines()
    return text, lines


def check_dollar_balance(path: Path, text: str):
    if text.count("$$") % 2 != 0:
        return [
            (
                "unmatched display-math delimiter",
                0,
                "The file has an odd number of '$$' delimiters.",
            )
        ]
    return []


def find_matches(lines, patterns):
    findings = []
    for lineno, line in enumerate(lines, 1):
        for label, pattern, guidance in patterns:
            if pattern.search(line):
                findings.append((label, lineno, guidance, line.strip()))
    return findings


INLINE_MATH_PATTERN = re.compile(r"(?<!\$)\$([^$\n]+)\$(?!\$)")


def check_inline_math_spacing(lines):
    findings = []
    guidance = (
        "GitHub inline math should not have a space immediately inside the dollar delimiters. "
        "Use $0.5$ or $\\frac{a}{a+b}$, not $ 0.5 $."
    )
    for lineno, line in enumerate(lines, 1):
        for match in INLINE_MATH_PATTERN.finditer(line):
            content = match.group(1)
            if content.startswith(" ") or content.endswith(" "):
                findings.append(
                    (
                        "inline math has spaces immediately inside dollar delimiters",
                        lineno,
                        guidance,
                        match.group(0),
                    )
                )
    return findings


def check_display_math_layout(lines):
    findings = []
    guidance_single = (
        "Put display math on its own lines using a multiline block: blank line, $$, "
        "math content, $$, blank line."
    )
    guidance_blank = (
        "Display-math delimiter lines should be surrounded by blank lines in prose: "
        "blank line before the opening $$ and blank line after the closing $$."
    )

    in_display = False
    opening_lineno = None

    for lineno, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("$$") and stripped.endswith("$$") and len(stripped) > 4:
            findings.append(
                (
                    "single-line display math",
                    lineno,
                    guidance_single,
                    stripped,
                )
            )
            continue

        if stripped != "$$":
            continue

        prev_line = lines[lineno - 2].strip() if lineno >= 2 else ""
        next_line = lines[lineno].strip() if lineno < len(lines) else ""

        if not in_display:
            if prev_line != "":
                findings.append(
                    (
                        "display math opening delimiter lacks preceding blank line",
                        lineno,
                        guidance_blank,
                        stripped,
                    )
                )
            if next_line == "":
                findings.append(
                    (
                        "display math opening delimiter lacks content line after it",
                        lineno,
                        guidance_single,
                        stripped,
                    )
                )
            in_display = True
            opening_lineno = lineno
        else:
            if next_line != "":
                findings.append(
                    (
                        "display math closing delimiter lacks following blank line",
                        lineno,
                        guidance_blank,
                        stripped,
                    )
                )
            if prev_line == "":
                findings.append(
                    (
                        "display math closing delimiter lacks content line before it",
                        lineno,
                        guidance_single,
                        stripped,
                    )
                )
            in_display = False
            opening_lineno = None

    if in_display and opening_lineno is not None:
        findings.append(
            (
                "unclosed display math block",
                opening_lineno,
                "A display-math block was opened with $$ and never closed.",
                "$$",
            )
        )

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit markdown for GitHub math/rendering problems before push."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=DEFAULT_PATHS,
        help="Markdown files to audit. Defaults to 02_probability_main/README.md.",
    )
    parser.add_argument(
        "--fail-on-advisory",
        action="store_true",
        help="Exit nonzero when advisory findings are present.",
    )
    args = parser.parse_args()

    total_errors = 0
    total_advisories = 0

    for raw_path in args.paths:
        path = raw_path if raw_path.is_absolute() else ROOT / raw_path
        if not path.exists():
            print(f"[ERROR] missing file: {path}")
            total_errors += 1
            continue

        text, lines = iter_lines(path)
        errors = check_dollar_balance(path, text)
        pattern_errors = find_matches(lines, ERROR_PATTERNS)
        spacing_errors = check_inline_math_spacing(lines)
        display_layout_errors = check_display_math_layout(lines)
        advisories = find_matches(lines, ADVISORY_PATTERNS)

        if errors or pattern_errors or spacing_errors or display_layout_errors or advisories:
            print(f"\n== {path} ==")

        for label, lineno, guidance in errors:
            location = f"{path}:{lineno}" if lineno else str(path)
            print(f"[ERROR] {location} {label}")
            print(f"        {guidance}")
            total_errors += 1

        for label, lineno, guidance, line in pattern_errors:
            print(f"[ERROR] {path}:{lineno} {label}")
            print(f"        {guidance}")
            print(f"        source: {line}")
            total_errors += 1

        for label, lineno, guidance, line in spacing_errors:
            print(f"[ERROR] {path}:{lineno} {label}")
            print(f"        {guidance}")
            print(f"        source: {line}")
            total_errors += 1

        for label, lineno, guidance, line in display_layout_errors:
            print(f"[ERROR] {path}:{lineno} {label}")
            print(f"        {guidance}")
            print(f"        source: {line}")
            total_errors += 1

        for label, lineno, guidance, line in advisories:
            print(f"[ADVISORY] {path}:{lineno} {label}")
            print(f"           {guidance}")
            print(f"           source: {line}")
            total_advisories += 1

    if total_errors == 0 and total_advisories == 0:
        print("PASS: no GitHub math/render audit findings.")
        return 0

    summary = f"Summary: {total_errors} error(s), {total_advisories} advisory finding(s)."
    print(f"\n{summary}")

    if total_errors > 0:
        return 1
    if args.fail_on_advisory and total_advisories > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

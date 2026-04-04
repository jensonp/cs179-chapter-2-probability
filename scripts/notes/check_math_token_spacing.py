#!/usr/bin/env python3
from __future__ import annotations

import argparse
import bisect
import sys
from pathlib import Path


ROOT = Path("/Users/jensonphan/cs179")
DEFAULT_PATHS = [
    ROOT / "02_probability_main" / "README.md",
]

OPEN_PUNCTUATION = set("([{\"'`")
CLOSE_PUNCTUATION = set(".,;:!?)]}\"'`")


def is_escaped(text: str, index: int) -> bool:
    backslashes = 0
    i = index - 1
    while i >= 0 and text[i] == "\\":
        backslashes += 1
        i -= 1
    return backslashes % 2 == 1


def iter_math_spans(text: str):
    i = 0
    n = len(text)
    while i < n:
        if text[i] != "$" or is_escaped(text, i):
            i += 1
            continue

        delimiter = "$$" if i + 1 < n and text[i + 1] == "$" else "$"
        start = i
        i += len(delimiter)

        while i < n:
            if text[i] == "\\":
                i += 2
                continue

            if delimiter == "$$":
                if i + 1 < n and text[i] == "$" and text[i + 1] == "$" and not is_escaped(text, i):
                    end = i + 2
                    yield delimiter, start, end, text[start:end]
                    i = end
                    break
            else:
                if text[i] == "$" and not is_escaped(text, i):
                    end = i + 1
                    yield delimiter, start, end, text[start:end]
                    i = end
                    break

            i += 1
        else:
            return


def build_line_starts(text: str):
    starts = [0]
    for idx, char in enumerate(text):
        if char == "\n":
            starts.append(idx + 1)
    return starts


def locate(line_starts, index: int):
    line_index = bisect.bisect_right(line_starts, index) - 1
    line_no = line_index + 1
    col_no = index - line_starts[line_index] + 1
    return line_no, col_no


def token_preview(token: str, limit: int = 80) -> str:
    compact = token.replace("\n", "\\n")
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."


def boundary_ok(char: str | None, *, side: str, strict_spaces: bool) -> bool:
    if char is None:
        return True
    if char.isspace():
        return True
    if side == "before" and char == ">":
        return True
    if side == "after" and char == "<":
        return True
    if strict_spaces:
        return False
    if side == "before":
        return char in OPEN_PUNCTUATION
    return char in CLOSE_PUNCTUATION


def audit_path(path: Path, strict_spaces: bool):
    text = path.read_text()
    line_starts = build_line_starts(text)
    findings = []

    for delimiter, start, end, token in iter_math_spans(text):
        before = text[start - 1] if start > 0 else None
        after = text[end] if end < len(text) else None

        before_ok = boundary_ok(before, side="before", strict_spaces=strict_spaces)
        after_ok = boundary_ok(after, side="after", strict_spaces=strict_spaces)

        if before_ok and after_ok:
            continue

        line_no, col_no = locate(line_starts, start)
        reasons = []
        if not before_ok:
            reasons.append(
                f"missing separator before token; found {repr(before)} instead of whitespace"
                + ("" if strict_spaces else " or opening punctuation")
            )
        if not after_ok:
            reasons.append(
                f"missing separator after token; found {repr(after)} instead of whitespace"
                + ("" if strict_spaces else " or closing punctuation")
            )

        findings.append((line_no, col_no, delimiter, token_preview(token), reasons))

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Check that inline/display math tokens are separated from surrounding prose. "
            "By default, punctuation like '(' before and ',' after is allowed."
        )
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=DEFAULT_PATHS,
        help="Markdown files to audit. Defaults to 02_probability_main/README.md.",
    )
    parser.add_argument(
        "--strict-spaces",
        action="store_true",
        help="Require literal whitespace or line boundaries around each math token.",
    )
    args = parser.parse_args()

    total_findings = 0

    for raw_path in args.paths:
        path = raw_path if raw_path.is_absolute() else ROOT / raw_path
        if not path.exists():
            print(f"[ERROR] missing file: {path}")
            total_findings += 1
            continue

        findings = audit_path(path, args.strict_spaces)
        if not findings:
            print(f"[PASS] {path}")
            continue

        print(f"\n== {path} ==")
        for line_no, col_no, delimiter, preview, reasons in findings:
            print(f"[ERROR] {path}:{line_no}:{col_no} math token spacing")
            print(f"        token: {preview}")
            print(f"        delimiter: {delimiter}")
            for reason in reasons:
                print(f"        {reason}")
            total_findings += 1

    if total_findings == 0:
        print("PASS: all math tokens have acceptable surrounding separation.")
        return 0

    print(f"\nSummary: {total_findings} spacing issue(s) found.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

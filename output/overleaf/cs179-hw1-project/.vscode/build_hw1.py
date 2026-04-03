#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import platform
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
import zipfile
from pathlib import Path

TECTONIC_VERSION = "0.15.0"
SCRIPT_DIR = Path(__file__).resolve().parent
SOURCE_DIR_NAME = "source"
BUILD_DIR_NAME = "build"
REPO_ROOT = SCRIPT_DIR.parents[3]

sys.path.insert(0, str(REPO_ROOT / "scripts"))
from hw1_layout import ALL_FIELD_NAMES, validate_layout_specs  # noqa: E402
from render_hw1_latex_answers import load_answers, render_answers_tex  # noqa: E402


def release_target() -> tuple[str, str]:
    system = platform.system()
    machine = platform.machine().lower()

    if system == "Darwin":
        if machine in {"arm64", "aarch64"}:
            return "aarch64-apple-darwin", f"tectonic-{TECTONIC_VERSION}-aarch64-apple-darwin.tar.gz"
        if machine in {"x86_64", "amd64"}:
            return "x86_64-apple-darwin", f"tectonic-{TECTONIC_VERSION}-x86_64-apple-darwin.tar.gz"
    elif system == "Windows":
        if machine in {"x86_64", "amd64"}:
            return "x86_64-pc-windows-msvc", f"tectonic-{TECTONIC_VERSION}-x86_64-pc-windows-msvc.zip"
    elif system == "Linux":
        if machine in {"arm64", "aarch64"}:
            return "aarch64-unknown-linux-musl", f"tectonic-{TECTONIC_VERSION}-aarch64-unknown-linux-musl.tar.gz"
        if machine in {"x86_64", "amd64"}:
            return "x86_64-unknown-linux-gnu", f"tectonic-{TECTONIC_VERSION}-x86_64-unknown-linux-gnu.tar.gz"

    raise RuntimeError(f"Unsupported platform for Tectonic bootstrap: {system} {machine}")


def executable_name() -> str:
    return "tectonic.exe" if os.name == "nt" else "tectonic"


def tools_dir() -> Path:
    target, _ = release_target()
    return SCRIPT_DIR / "tools" / "tectonic" / TECTONIC_VERSION / target


def repo_local_tectonic() -> Path:
    return tools_dir() / executable_name()


def legacy_repo_local_tectonic() -> Path:
    return SCRIPT_DIR / "tools" / "tectonic" / TECTONIC_VERSION / executable_name()


def normalize_executable(path: Path) -> Path:
    expected = repo_local_tectonic()
    candidates = sorted(path.rglob(executable_name()))
    if not candidates:
        raise RuntimeError(f"Tectonic archive did not contain {executable_name()}")

    source = candidates[0]
    expected.parent.mkdir(parents=True, exist_ok=True)
    if source.resolve() != expected.resolve():
        shutil.move(str(source), str(expected))

    if os.name != "nt":
        expected.chmod(expected.stat().st_mode | 0o111)
    return expected


def bootstrap_tectonic() -> Path:
    binary = repo_local_tectonic()
    if binary.exists():
        if os.name != "nt":
            binary.chmod(binary.stat().st_mode | 0o111)
        return binary

    legacy_binary = legacy_repo_local_tectonic()
    if legacy_binary.exists():
        if os.name != "nt":
            legacy_binary.chmod(legacy_binary.stat().st_mode | 0o111)
        return legacy_binary

    target, asset = release_target()
    url = f"https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%40{TECTONIC_VERSION}/{asset}"
    destination = SCRIPT_DIR / "tools" / "tectonic" / TECTONIC_VERSION / target
    destination.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="hw1-tectonic-") as temp_dir:
        temp_root = Path(temp_dir)
        archive_path = temp_root / asset
        urllib.request.urlretrieve(url, archive_path)

        if asset.endswith(".zip"):
            with zipfile.ZipFile(archive_path) as archive:
                archive.extractall(destination)
        else:
            with tarfile.open(archive_path, "r:gz") as archive:
                archive.extractall(destination)

    return normalize_executable(destination)


def compiler_command(kind: str, executable: str, doc_path: Path) -> tuple[list[str], Path]:
    doc_dir = doc_path.parent
    build_dir = doc_dir.parent / BUILD_DIR_NAME
    build_dir.mkdir(parents=True, exist_ok=True)
    if kind == "tectonic":
        return (
            [
                executable,
                "-X",
                "compile",
                "--synctex",
                "--keep-logs",
                "--keep-intermediates",
                "--outdir",
                str(build_dir),
                str(doc_path),
            ],
            doc_dir,
        )
    if kind == "latexmk":
        return (
            [
                executable,
                "-pdf",
                "-synctex=1",
                "-interaction=nonstopmode",
                "-file-line-error",
                f"-outdir={build_dir}",
                str(doc_path),
            ],
            doc_dir,
        )
    if kind == "pdflatex":
        return (
            [
                executable,
                "-synctex=1",
                "-interaction=nonstopmode",
                "-file-line-error",
                f"-output-directory={build_dir}",
                doc_path.name,
            ],
            doc_dir,
        )
    raise RuntimeError(f"Unsupported compiler kind: {kind}")


def first_available_compiler() -> tuple[str, str] | None:
    latexmk = shutil.which("latexmk")
    if latexmk:
        return "latexmk", latexmk

    local_binary = repo_local_tectonic()
    if local_binary.exists():
        if os.name != "nt":
            local_binary.chmod(local_binary.stat().st_mode | 0o111)
        return "tectonic", str(local_binary)

    legacy_binary = legacy_repo_local_tectonic()
    if legacy_binary.exists():
        if os.name != "nt":
            legacy_binary.chmod(legacy_binary.stat().st_mode | 0o111)
        return "tectonic", str(legacy_binary)

    for name in ("tectonic", "pdflatex"):
        executable = shutil.which(name)
        if executable:
            kind = "tectonic" if name == "tectonic" else name
            return kind, executable

    return None


def resolve_compiler() -> tuple[str, str]:
    compiler = first_available_compiler()
    if compiler is not None:
        return compiler

    try:
        return "tectonic", str(bootstrap_tectonic())
    except Exception as exc:
        raise RuntimeError(
            "No LaTeX compiler is available. Tried repo-local Tectonic, PATH Tectonic, latexmk, "
            "pdflatex, and Tectonic bootstrap."
        ) from exc


SET_ANSWER_RE = re.compile(r"\\SetAnswer\{([^}]+)\}\{")


def _line_number_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _is_escaped(text: str, offset: int) -> bool:
    backslashes = 0
    cursor = offset - 1
    while cursor >= 0 and text[cursor] == "\\":
        backslashes += 1
        cursor -= 1
    return backslashes % 2 == 1


def _parse_set_answer_block(text: str, offset: int) -> tuple[str, int]:
    match = SET_ANSWER_RE.match(text, offset)
    if not match:
        raise ValueError("Expected \\SetAnswer{...}{ at command start")

    key = match.group(1)
    cursor = match.end()
    brace_depth = 1

    while cursor < len(text):
        char = text[cursor]
        if char == "{" and not _is_escaped(text, cursor):
            brace_depth += 1
        elif char == "}" and not _is_escaped(text, cursor):
            brace_depth -= 1
            if brace_depth == 0:
                return key, cursor + 1
        cursor += 1

    raise ValueError(f"Unterminated \\SetAnswer body for key '{key}'")


def validate_answers_tex(doc_path: Path) -> None:
    answers_path = doc_path.parent / "answers.tex"
    if not answers_path.exists():
        return

    text = answers_path.read_text(encoding="utf-8")
    expected = set(ALL_FIELD_NAMES)
    seen: list[str] = []
    unknown: list[tuple[int, str]] = []
    invalid_lines: list[tuple[int, str]] = []

    cursor = 0
    while cursor < len(text):
        if text[cursor].isspace():
            cursor += 1
            continue

        if text[cursor] == "%":
            newline_index = text.find("\n", cursor)
            cursor = len(text) if newline_index == -1 else newline_index + 1
            continue

        if text.startswith("\\SetAnswer{", cursor):
            try:
                key, cursor = _parse_set_answer_block(text, cursor)
            except ValueError as exc:
                invalid_lines.append((_line_number_for_offset(text, cursor), str(exc)))
                break
        else:
            line_end = text.find("\n", cursor)
            if line_end == -1:
                line_end = len(text)
            stripped = text[cursor:line_end].strip()
            preview = stripped if len(stripped) <= 80 else f"{stripped[:77]}..."
            invalid_lines.append((_line_number_for_offset(text, cursor), preview))
            cursor = line_end + 1
            continue

        seen.append(key)
        if key not in expected:
            unknown.append((_line_number_for_offset(text, cursor), key))

    duplicates = sorted({key for key in seen if seen.count(key) > 1})
    missing = sorted(expected - set(seen))

    errors: list[str] = []
    if unknown:
        bad = ", ".join(f"{key} (line {line_number})" for line_number, key in unknown)
        errors.append(f"Unknown \\SetAnswer keys in {answers_path}: {bad}")
    if invalid_lines:
        bad = ", ".join(f"line {line_number}: {content}" for line_number, content in invalid_lines[:8])
        suffix = "" if len(invalid_lines) <= 8 else f", ... ({len(invalid_lines)} invalid lines total)"
        errors.append(
            "Invalid non-comment content in "
            f"{answers_path}: {bad}{suffix}. "
            "Only % comments, blank lines, and \\SetAnswer{...}{...} lines are allowed."
        )
    if duplicates:
        errors.append(f"Duplicate \\SetAnswer keys in {answers_path}: {', '.join(duplicates)}")
    if missing:
        preview = ", ".join(missing[:8])
        suffix = "" if len(missing) <= 8 else f", ... ({len(missing)} missing total)"
        errors.append(f"Missing \\SetAnswer keys in {answers_path}: {preview}{suffix}")

    if errors:
        raise RuntimeError("\n".join(errors))


def warn_if_answers_sources_diverge(doc_path: Path) -> None:
    answers_path = doc_path.parent / "answers.tex"
    answers_toml_path = doc_path.parent / "answers.toml"
    if not answers_path.exists() or not answers_toml_path.exists():
        return

    try:
        rendered_from_toml = render_answers_tex(load_answers(answers_toml_path))
        current_answers_tex = answers_path.read_text(encoding="utf-8")
    except Exception:
        return

    if current_answers_tex == rendered_from_toml:
        return

    print(
        "note: answers.tex differs from answers.toml; this build compiles answers.tex as-is. "
        "Run scripts/render_hw1_latex_answers.py if you want answers.toml to regenerate answers.tex.",
        file=sys.stderr,
    )


def regenerate_answers_tex_from_toml(doc_path: Path) -> None:
    validate_layout_specs()
    answers_path = doc_path.parent / "answers.tex"
    answers_toml_path = doc_path.parent / "answers.toml"
    if not answers_toml_path.exists():
        raise RuntimeError(
            f"Missing answers.toml at {answers_toml_path}. "
            "Create it or pass --no-regenerate to compile an existing answers.tex."
        )

    rendered_from_toml = render_answers_tex(load_answers(answers_toml_path))
    existing = answers_path.read_text(encoding="utf-8") if answers_path.exists() else None
    if existing != rendered_from_toml:
        answers_path.write_text(rendered_from_toml, encoding="utf-8")
        print(f"note: Regenerated {answers_path.name} from {answers_toml_path.name}", file=sys.stderr)


OVERFULL_RE = re.compile(r"^(Overfull \\\\[hv]box .*?)$", re.MULTILINE)
UNDERFULL_RE = re.compile(r"^(Underfull \\\\[hv]box .*?)$", re.MULTILINE)


def check_log_for_layout_issues(doc_path: Path) -> None:
    log_path = doc_path.parent.parent / BUILD_DIR_NAME / "main.log"
    if not log_path.exists():
        return

    log_text = log_path.read_text(encoding="utf-8", errors="replace")
    overfull = OVERFULL_RE.findall(log_text)
    underfull = UNDERFULL_RE.findall(log_text)

    if underfull:
        preview = "; ".join(underfull[:3])
        suffix = "" if len(underfull) <= 3 else f"; ... ({len(underfull)} underfull warnings total)"
        print(f"note: LaTeX underfull box warnings detected: {preview}{suffix}", file=sys.stderr)

    if overfull:
        preview = "; ".join(overfull[:3])
        suffix = "" if len(overfull) <= 3 else f"; ... ({len(overfull)} overfull warnings total)"
        raise RuntimeError(
            "Detected rendered content overflow in build/main.log: "
            f"{preview}{suffix}. Shorten the content, move work into a larger field, "
            "or adjust the layout/font settings."
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the CS179 HW1 LaTeX project.")
    parser.add_argument(
        "tex_entry",
        type=Path,
        help="Absolute path to main.tex (or any .tex file in the same source directory).",
    )
    parser.add_argument(
        "--no-regenerate",
        action="store_true",
        help="Skip regenerating answers.tex from answers.toml before compile.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    doc_path = args.tex_entry.resolve()
    if not doc_path.exists():
        print(f"TeX entry point not found: {doc_path}", file=sys.stderr)
        raise SystemExit(1)
    if doc_path.name != "main.tex":
        candidate = doc_path.parent / "main.tex"
        if candidate.exists():
            print(f"note: Active file is {doc_path.name}; compiling {candidate}", file=sys.stderr)
            doc_path = candidate

    if args.no_regenerate:
        warn_if_answers_sources_diverge(doc_path)
    else:
        regenerate_answers_tex_from_toml(doc_path)

    validate_answers_tex(doc_path)

    kind, executable = resolve_compiler()
    if kind != "latexmk":
        print("note: latexmk not found; install it for faster incremental builds", file=sys.stderr)
    print(f"note: Using compiler {kind} ({executable})", file=sys.stderr)
    command, cwd = compiler_command(kind, executable, doc_path)
    result = subprocess.run(command, cwd=cwd, check=False)
    if result.returncode == 0:
        check_log_for_layout_issues(doc_path)
    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()

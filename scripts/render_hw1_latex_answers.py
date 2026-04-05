#!/usr/bin/env python3
"""Generate an Overleaf-ready CS179 HW1 project and optionally compile it."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import textwrap
import zipfile
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11
    tomllib = None

from hw1_layout import (
    ALL_FIELD_NAMES,
    CHECKBOX_FIELDS,
    LATEX_OUTPUT_PDF,
    OVERLEAF_PROJECT_DIR,
    SOURCE_PDF,
    TEXT_FIELDS,
    CheckboxSpec,
    TextFieldSpec,
    validate_layout_specs,
)


CHECKBOX_NAMES = {field.name for field in CHECKBOX_FIELDS}
TEXT_FIELDS_BY_NAME = {field.name: field for field in TEXT_FIELDS}
SOURCE_DIR_NAME = "source"
BUILD_DIR_NAME = "build"
BLOCK_MATH_MARKERS = (
    "$$",
    r"\[",
    r"\begin{equation",
    r"\begin{align",
    r"\begin{gather",
    r"\begin{multline",
    r"\begin{cases",
    r"\begin{array",
)
DISPLAY_WRAPPER_PATTERNS = (
    (re.compile(r"^\s*\$\$(?P<body>.*)\$\$\s*$", re.DOTALL), "$", "$"),
    (re.compile(r"^\s*\\\\\[(?P<body>.*)\\\\\]\s*$", re.DOTALL), "$", "$"),
    (re.compile(r"^\s*\\begin\{equation\*?\}(?P<body>.*)\\end\{equation\*?\}\s*$", re.DOTALL), "$", "$"),
    (re.compile(r"^\s*\\begin\{gather\*?\}(?P<body>.*)\\end\{gather\*?\}\s*$", re.DOTALL), "$", "$"),
    (re.compile(r"^\s*\\begin\{multline\*?\}(?P<body>.*)\\end\{multline\*?\}\s*$", re.DOTALL), "$", "$"),
)
RAW_BLOCK_HINTS = BLOCK_MATH_MARKERS + (
    r"\begin{",
    r"\item",
    r"\includegraphics",
    r"\tikz",
    r"\par",
    r"\vspace",
    r"\medskip",
    r"\smallskip",
)


def source_dir(project_dir: Path) -> Path:
    return project_dir / SOURCE_DIR_NAME


def build_dir(project_dir: Path) -> Path:
    return project_dir / BUILD_DIR_NAME


def fields_by_page() -> dict[int, list[TextFieldSpec | CheckboxSpec]]:
    grouped: dict[int, list[TextFieldSpec | CheckboxSpec]] = {}
    for field in TEXT_FIELDS:
        grouped.setdefault(field.page, []).append(field)
    for field in CHECKBOX_FIELDS:
        grouped.setdefault(field.page, []).append(field)
    return grouped


def parse_fallback_toml(text: str) -> dict[str, object]:
    data: dict[str, object] = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.strip()
        i += 1

        if not line or line.startswith("#"):
            continue

        if "=" not in raw:
            raise SystemExit(f"Unsupported TOML line: {raw}")

        key, value = raw.split("=", 1)
        key = key.strip()
        value = value.strip()

        if value.startswith("'''"):
            if value == "''''''":
                data[key] = ""
                continue

            parts = [value[3:]]
            while True:
                if parts[-1].endswith("'''"):
                    parts[-1] = parts[-1][:-3]
                    break
                if i >= len(lines):
                    raise SystemExit(f"Unterminated triple-quoted string for key {key}")
                parts.append(lines[i])
                i += 1
            data[key] = "\n".join(parts)
            continue

        if value in {"true", "false"}:
            data[key] = value == "true"
            continue

        if value.startswith("'") and value.endswith("'"):
            data[key] = value[1:-1]
            continue

        try:
            data[key] = int(value)
            continue
        except ValueError:
            pass

        try:
            data[key] = float(value)
            continue
        except ValueError:
            pass

        data[key] = value
    return data


def load_answers(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    with path.open("rb") as handle:
        if tomllib is not None:
            data = tomllib.load(handle)
        else:
            data = parse_fallback_toml(handle.read().decode("utf-8"))
    unknown = sorted(set(data) - set(ALL_FIELD_NAMES))
    if unknown:
        names = ", ".join(unknown)
        raise SystemExit(f"Unknown answer keys in {path}: {names}")
    return data


def default_toml_template() -> str:
    return render_answers_toml({})


def is_blank_text_value(value: object) -> bool:
    if not isinstance(value, str):
        return False

    stripped = value.strip()
    if not stripped:
        return True

    wrapped_body = unwrap_display_math_body(stripped)
    if wrapped_body is None:
        return False

    return not collapse_inline_whitespace(wrapped_body)


def _looks_like_raw_latex_block(text: str) -> bool:
    stripped = text.lstrip()
    return any(marker in stripped for marker in RAW_BLOCK_HINTS)


def unwrap_display_math_body(text: str) -> str | None:
    stripped = text.strip()
    if not stripped:
        return None

    for pattern, _, _ in DISPLAY_WRAPPER_PATTERNS:
        match = pattern.match(stripped)
        if match:
            return match.group("body")

    return None


def preserve_user_linebreaks(text: str) -> str:
    if is_blank_text_value(text):
        return ""

    stripped_text = text.strip()
    if stripped_text and _looks_like_raw_latex_block(stripped_text):
        return stripped_text

    paragraphs: list[str] = []
    current_lines: list[str] = []

    def flush_current_lines() -> None:
        if not current_lines:
            return
        paragraph = "\n".join(current_lines).strip("\n")
        current_lines.clear()
        if not paragraph:
            return
        if _looks_like_raw_latex_block(paragraph):
            paragraphs.append(paragraph)
            return
        paragraph_lines = [line.rstrip() for line in paragraph.splitlines() if line.strip()]
        paragraphs.append(r"\\ ".join(paragraph_lines))

    for raw_line in text.splitlines():
        if raw_line.strip():
            current_lines.append(raw_line)
            continue
        flush_current_lines()

    flush_current_lines()
    return "\n\\par\n".join(paragraphs)


def collapse_inline_whitespace(text: str) -> str:
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def coerce_inline_field_text(text: str) -> str:
    if is_blank_text_value(text):
        return ""

    stripped = text.strip()

    wrapped_body = unwrap_display_math_body(stripped)
    if wrapped_body is not None:
        body = collapse_inline_whitespace(wrapped_body)
        body = body.replace(r"\\", " ")
        body = re.sub(r"\s+", " ", body).strip()
        return f"${body}$" if body else ""

    if "\n" in stripped:
        return collapse_inline_whitespace(stripped)

    return text


def answer_to_tex(field: TextFieldSpec | CheckboxSpec, value: object) -> str:
    if value is None or is_blank_text_value(value):
        return ""
    if field.name in CHECKBOX_NAMES and isinstance(value, bool):
        return r"\Checkmark" if value else ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if is_blank_text_value(text):
        return ""
    if isinstance(field, TextFieldSpec) and field.content_mode == "inline":
        return coerce_inline_field_text(text)
    if isinstance(field, TextFieldSpec) and field.preserve_linebreaks:
        return preserve_user_linebreaks(text)
    return text


def collect_answers_content_issues(answers: dict[str, object]) -> list[str]:
    issues: list[str] = []

    for name, value in answers.items():
        if value is None or value == "" or is_blank_text_value(value):
            continue

        if name in CHECKBOX_NAMES:
            continue

        if isinstance(value, bool):
            issues.append(
                f"{name}: boolean values are only valid for checkbox fields; use quoted text or raw LaTeX here."
            )
            continue

        field = TEXT_FIELDS_BY_NAME.get(name)
        if field is None or field.content_mode != "inline":
            continue

        text = str(value)
        has_newlines = "\n" in text
        has_block_math = any(marker in text for marker in BLOCK_MATH_MARKERS)
        if has_newlines or has_block_math:
            issues.append(
                f"{name}: short answer slots only support inline/final answers. "
                "Move derivations, display math, or multi-line work into the corresponding "
                "`*_work`, `*_reasoning`, or notes field."
            )

    return issues


def validate_answers_content(answers: dict[str, object]) -> None:
    issues = collect_answers_content_issues(answers)
    if issues:
        raise SystemExit("Invalid answers.toml content:\n" + "\n".join(issues))


def render_answers_tex(answers: dict[str, object]) -> str:
    validate_layout_specs()
    pages = fields_by_page()
    lines = [
        "% !TEX root = main.tex",
        "% Auto-generated by scripts/render_hw1_latex_answers.py",
        "% Local builds regenerate this file from answers.toml unless build_hw1.py is run with --no-regenerate.",
        "% For Overleaf-only workflows you can edit this file directly, but local deterministic builds overwrite it.",
        "% Checkbox fields: put \\Checkmark in the selected slot and leave the opposite slot empty.",
        "% Example: \\SetAnswer{problem3_q1_yes}{\\Checkmark}",
        "",
    ]
    for page in range(1, 10):
        lines.append(f"% Page {page}")
        page_fields = pages.get(page, [])
        if not page_fields:
            lines.append("% No mapped fields on this page.")
        for field in page_fields:
            value = answer_to_tex(field, answers.get(field.name, False if field.name in CHECKBOX_NAMES else ""))
            lines.append(rf"\SetAnswer{{{field.name}}}{{{value}}}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def toml_literal(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if value is None or value == "" or is_blank_text_value(value):
        return "'''\n\n'''"
    text = str(value)
    return "'''" + text + "'''"


def render_answers_toml(answers: dict[str, object]) -> str:
    pages = fields_by_page()
    page_notes = {
        3: "# `problem1_p_*` fields are the small answer boxes; put derivations and $$...$$ in `problem1_work*`.",
        4: "# `problem2_*` answer fields are short boxes; use `problem2_work*` for derivations and block math.",
        5: "# `problem3_q*_reasoning` fields are the large reasoning boxes; the yes/no fields are booleans.",
        7: "# `problem5_*_rho/loglik/bic` fields are short answers; use `problem5_*_work*` for derivations.",
        8: "# `problem5_long_*` answer fields are short boxes; use `problem5_long_work*` for derivations.",
    }
    lines = [
        "# Raw LaTeX mapped to the original homework boxes.",
        "# Use triple single quotes for multi-line content so backslashes stay literal.",
        "# Checkbox fields can be either false/true or raw LaTeX like '$\\\\checkmark$'.",
        "# Short answer fields should stay inline; reserve $$...$$ blocks and multi-line derivations for work/reasoning fields.",
        "",
    ]
    for page in range(1, 10):
        lines.append(f"# Page {page}")
        note = page_notes.get(page)
        if note:
            lines.append(note)
        page_fields = pages.get(page, [])
        if not page_fields:
            lines.append("# No mapped fields on this page.")
        for field in page_fields:
            default = False if field.name in CHECKBOX_NAMES else ""
            lines.append(f"{field.name} = {toml_literal(answers.get(field.name, default))}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_readme() -> str:
    return textwrap.dedent(
        """
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
        - Answer content is raw LaTeX, so math, aligned equations, and `\\includegraphics` all work.
        - Keep short answer fields inline. Use `*_work`, `*_reasoning`, and notes fields for multi-line derivations or `$$...$$`.
        - If a short answer field receives display math or multi-line content, local builds warn and coerce it to the safest inline form they can render.
        - Empty display-math placeholders like `$$ ... $$` with no body are treated as blank so they do not break the build.
        - Block/work fields preserve manual line breaks for plain text and auto-scale content down to fit their boxes.
        - Overfull LaTeX boxes are still surfaced during build so layout collisions/overflow remain visible.
        - Checkbox markers accept `\\Checkmark` in `source/answers.tex`, or `true` / `false` in `source/answers.toml`.
        - The layout is faithful because the original `source/cs179-hw1.pdf` is embedded page-for-page.
        """
    ).strip() + "\n"


def render_overlay_command(field: TextFieldSpec | CheckboxSpec) -> str:
    if isinstance(field, CheckboxSpec):
        x0, y0, x1, y1 = field.rect
        cx = (x0 + x1) / 2
        cy = (y0 + y1) / 2
        return rf"\PlaceCheckboxAnswer{{{cx:.2f}}}{{{cy:.2f}}}{{\Answer{{{field.name}}}}}"

    x0, y0, _, _ = field.rect
    content_x = x0 + field.box_padding
    content_y = y0 + field.box_padding
    width = field.width - 2 * field.box_padding
    height = field.height - 2 * field.box_padding
    return (
        rf"\PlaceTextAnswer{{{content_x:.2f}}}{{{content_y:.2f}}}{{{width:.2f}}}"
        rf"{{{height:.2f}}}{{{field.font_size:.2f}}}{{\Answer{{{field.name}}}}}"
    )


def render_box_command(field: TextFieldSpec | CheckboxSpec) -> str | None:
    if not isinstance(field, TextFieldSpec) or not field.draw_box:
        return None

    x0, y0, x1, y1 = field.rect
    return rf"\PlaceTextBox{{{x0:.2f}}}{{{y0:.2f}}}{{{x1:.2f}}}{{{y1:.2f}}}{{{field.box_line_width:.2f}}}"


def render_main_tex() -> str:
    validate_layout_specs()
    page_commands = []
    pages = fields_by_page()
    for page in range(1, 10):
        commands = ["\\thispagestyle{empty}"]
        for field in pages.get(page, []):
            box_command = render_box_command(field)
            if box_command:
                commands.append(box_command)
            commands.append(render_overlay_command(field))
        page_body = "\n".join(commands)
        page_commands.append(
            rf"\includepdf[pages={page},pagecommand={{{page_body}}}]{{cs179-hw1.pdf}}"
        )

    joined_pages = "\n".join(page_commands)
    return textwrap.dedent(
        rf"""
        \documentclass[letterpaper]{{article}}
        \usepackage[margin=0in]{{geometry}}
        \usepackage{{amsmath,amssymb}}
        \usepackage{{graphicx}}
        \usepackage{{tikz}}
        \usepackage{{pdfpages}}
        \usetikzlibrary{{calc}}
        \pagestyle{{empty}}
        \setlength{{\parindent}}{{0pt}}

        \long\def\SetAnswer#1#2{{\expandafter\gdef\csname answer@#1\endcsname{{#2}}}}
        \def\Answer#1{{\ifcsname answer@#1\endcsname\csname answer@#1\endcsname\fi}}
        \newcommand{{\Checkmark}}{{%
          \tikz[baseline=-0.65ex,x=1pt,y=1pt]{{%
            \draw[line width=0.9pt,line cap=round,line join=round]
              (0,2.3) -- (2.4,0) -- (6.1,6.1);
          }}%
        }}
        \ExplSyntaxOn
        \box_new:N \l__hw_answer_box
        \fp_new:N \l__hw_answer_scale_fp
        \cs_new_protected:Npn \__hw_answer_fit:nnnn #1#2#3#4
          {{
            \exp_args:Ne \tl_if_blank:nTF {{#4}}
              {{}}
              {{
                \hbox_set:Nn \l__hw_answer_box
                  {{
                    \begin{{minipage}}[t]{{#1pt}}
                    \raggedright
                    \setlength{{\parskip}}{{0.25em}}
                    \fontsize{{#3}}{{\fp_eval:n {{ round(#3 + 2, 2) }} }}\selectfont
                    #4
                    \end{{minipage}}
                  }}
                \fp_set:Nn \l__hw_answer_scale_fp {{ 1 }}
                \dim_compare:nNnT {{ \box_wd:N \l__hw_answer_box }} > {{ #1pt }}
                  {{
                    \fp_set:Nn \l__hw_answer_scale_fp
                      {{
                        min(
                          \l__hw_answer_scale_fp,
                          \dim_to_fp:n {{ #1pt }} / \dim_to_fp:n {{ \box_wd:N \l__hw_answer_box }}
                        )
                      }}
                  }}
                \dim_compare:nNnT {{ \box_ht:N \l__hw_answer_box + \box_dp:N \l__hw_answer_box }} > {{ #2pt }}
                  {{
                    \fp_set:Nn \l__hw_answer_scale_fp
                      {{
                        min(
                          \l__hw_answer_scale_fp,
                          \dim_to_fp:n {{ #2pt }} /
                          \dim_to_fp:n {{ \box_ht:N \l__hw_answer_box + \box_dp:N \l__hw_answer_box }}
                        )
                      }}
                  }}
                \scalebox{{\fp_eval:n {{ round(\l__hw_answer_scale_fp, 5) }} }}{{\box_use:N \l__hw_answer_box}}
              }}
          }}
        \cs_new_eq:NN \HWAnswerFit \__hw_answer_fit:nnnn
        \ExplSyntaxOff
        \newcommand{{\PlaceTextAnswer}}[6]{{%
          \begin{{tikzpicture}}[remember picture,overlay]
            \node[anchor=north west,inner sep=0pt,outer sep=0pt] at
              ([xshift=#1pt,yshift=-#2pt]current page.north west) {{%
                \HWAnswerFit{{#3}}{{#4}}{{#5}}{{#6}}%
              }};
          \end{{tikzpicture}}%
        }}
        \newcommand{{\PlaceTextBox}}[5]{{%
          \begin{{tikzpicture}}[remember picture,overlay]
            \draw[line width=#5pt]
              ([xshift=#1pt,yshift=-#2pt]current page.north west) rectangle
              ([xshift=#3pt,yshift=-#4pt]current page.north west);
          \end{{tikzpicture}}%
        }}
        \newcommand{{\PlaceCheckboxAnswer}}[3]{{%
          \begin{{tikzpicture}}[remember picture,overlay]
            \node[anchor=center,inner sep=0pt,outer sep=0pt] at
              ([xshift=#1pt,yshift=-#2pt]current page.north west) {{#3}};
          \end{{tikzpicture}}%
        }}

        \input{{answers.tex}}

        \begin{{document}}
        {joined_pages}
        \end{{document}}
        """
    ).strip() + "\n"


def ensure_project_files(project_dir: Path, answers: dict[str, object]) -> None:
    project_dir.mkdir(parents=True, exist_ok=True)
    src_dir = source_dir(project_dir)
    src_dir.mkdir(parents=True, exist_ok=True)
    build_dir(project_dir).mkdir(parents=True, exist_ok=True)

    shutil.copy2(SOURCE_PDF, src_dir / SOURCE_PDF.name)
    (src_dir / "answers.toml").write_text(render_answers_toml(answers), encoding="utf-8")
    (src_dir / "answers.tex").write_text(render_answers_tex(answers), encoding="utf-8")
    (src_dir / "main.tex").write_text(render_main_tex(), encoding="utf-8")
    (project_dir / "README.md").write_text(render_readme(), encoding="utf-8")


def compile_project(project_dir: Path) -> Path:
    src_dir = source_dir(project_dir)
    out_dir = build_dir(project_dir)
    subprocess.run(
        ["tectonic", "-X", "compile", str(src_dir / "main.tex"), "--keep-logs", "--keep-intermediates", "--outdir", str(out_dir)],
        check=True,
    )
    pdf_path = out_dir / "main.pdf"
    LATEX_OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(pdf_path, LATEX_OUTPUT_PDF)
    return pdf_path


def zip_project(project_dir: Path) -> Path:
    zip_path = project_dir.with_suffix(".zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(project_dir.rglob("*")):
            archive.write(path, path.relative_to(project_dir))
    return zip_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-dir",
        type=Path,
        default=OVERLEAF_PROJECT_DIR,
        help="Directory containing the generated Overleaf project.",
    )
    parser.add_argument(
        "--answers",
        type=Path,
        default=None,
        help="TOML file with raw LaTeX answers. Defaults to <project-dir>/answers.toml.",
    )
    parser.add_argument(
        "--compile",
        action="store_true",
        help="Compile main.tex with tectonic after regenerating the project files.",
    )
    parser.add_argument(
        "--zip",
        action="store_true",
        help="Create a zip archive next to the generated Overleaf project.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    project_dir = args.project_dir.resolve()
    answers_path = (args.answers.resolve() if args.answers else source_dir(project_dir) / "answers.toml")

    if not answers_path.exists():
        answers_path.parent.mkdir(parents=True, exist_ok=True)
        answers_path.write_text(default_toml_template(), encoding="utf-8")

    answers = load_answers(answers_path)
    ensure_project_files(project_dir, answers)

    print(f"Wrote Overleaf project to {project_dir}")

    if args.compile:
        pdf_path = compile_project(project_dir)
        print(f"Compiled {pdf_path}")
        print(f"Copied {LATEX_OUTPUT_PDF}")

    if args.zip:
        zip_path = zip_project(project_dir)
        print(f"Wrote {zip_path}")


if __name__ == "__main__":
    main()

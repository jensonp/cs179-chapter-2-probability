#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

import fitz


PAGE_WIDTH = 612
PAGE_HEIGHT = 792
MARGIN_X = 54
MARGIN_TOP = 50
MARGIN_BOTTOM = 42
LINE_GAP = 8
IMAGE_GAP = 12
TABLE_CELL_PAD_X = 6
TABLE_CELL_PAD_Y = 5
MAX_IMAGE_HEIGHT = 290
TABLE_GROUP_GAP = 16

TITLE = "Probability and Inference"
SUBTITLE = "Reconstructed Chapter"
SUBJECT = ""
FONT_ARCHIVE_DIR = Path("/System/Library/Fonts/Supplemental")
FONT_FILES = {
    "body": FONT_ARCHIVE_DIR / "Times New Roman.ttf",
    "bodybold": FONT_ARCHIVE_DIR / "Times New Roman Bold.ttf",
    "math": FONT_ARCHIVE_DIR / "Arial Unicode.ttf",
}
FONT_METRICS = {name: fitz.Font(fontfile=str(path)) for name, path in FONT_FILES.items()}

INLINE_MATH_RE = re.compile(r"\$(.+?)\$")
IMAGE_RE = re.compile(r"^!\[(?P<alt>[^\]]*)\]\((?P<path>[^)]+)\)\s*$")
TABLE_DIVIDER_RE = re.compile(r"^\|\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|$")
TEXT_BRACE_RE = re.compile(r"\\text\{([^}]*)\}")
FRAC_RE = re.compile(r"\\frac\{([^{}]+)\}\{([^{}]+)\}")
SQRT_RE = re.compile(r"\\sqrt\{([^{}]+)\}")
BAR_BRACE_RE = re.compile(r"\\bar\{([^{}]+)\}")
BAR_TOKEN_RE = re.compile(r"\\bar\s+([A-Za-z])")
HAT_BRACE_RE = re.compile(r"\\hat\{([^{}]+)\}")
HAT_TOKEN_RE = re.compile(r"\\hat\s+([A-Za-zα-ωΑ-Ω])")
BAR_SYMBOL_RE = re.compile(r"\\bar([A-Za-zα-ωΑ-Ω])")
HAT_SYMBOL_RE = re.compile(r"\\hat([A-Za-zα-ωΑ-Ω])")


@dataclass
class Block:
    kind: str
    text: str = ""
    lines: list[str] | None = None
    rows: list[list[str]] | None = None
    tables: list[list[list[str]]] | None = None
    titles: list[str] | None = None
    image_path: Path | None = None
    alt: str = ""


@dataclass(frozen=True)
class FigureSpec:
    filename: str
    page_index: int
    clip: tuple[float, float, float, float]
    scale: float = 2.8


FIGURE_SPECS = [
    FigureSpec("figure_2_1_gaussian.png", 8, (82, 70, 527, 196)),
    FigureSpec("figure_2_2_beta_grid.png", 9, (80, 70, 540, 191)),
    FigureSpec("figure_2_3_dirichlet_simplex.png", 9, (120, 245, 486, 356)),
    FigureSpec("figure_2_12_bernoulli_likelihood.png", 12, (68, 170, 515, 265)),
    FigureSpec("figure_2_13_gaussian_likelihood.png", 12, (68, 545, 525, 662)),
    FigureSpec("figure_2_17_histograms.png", 17, (60, 160, 535, 260)),
    FigureSpec("figure_2_20_beta_hyperprior.png", 20, (95, 338, 502, 460)),
    FigureSpec("figure_2_22_histogram_model_scores.png", 22, (332, 423, 538, 534), scale=4.0),
    FigureSpec("figure_2_23_convexity_sketch.png", 23, (360, 205, 523, 314), scale=3.2),
    FigureSpec("figure_2_5_copula_transforms.png", 29, (80, 74, 524, 198)),
    FigureSpec("figure_2_6_affine_flow_panels.png", 31, (84, 72, 520, 176)),
]


def normalize_text(text: str) -> str:
    text = text.replace("`", "")
    text = text.replace("–", "-").replace("—", "-")
    text = text.replace("\xa0", " ")
    return " ".join(text.split())


def latexish_to_text(text: str) -> str:
    text = normalize_text(text)
    text = TEXT_BRACE_RE.sub(r"\1", text)
    previous = None
    while previous != text:
        previous = text
        text = FRAC_RE.sub(r"(\1)/(\2)", text)
        text = SQRT_RE.sub(r"sqrt(\1)", text)
    text = BAR_BRACE_RE.sub(r"\1-bar", text)
    text = BAR_TOKEN_RE.sub(r"\1-bar", text)
    text = HAT_BRACE_RE.sub(r"\1-hat", text)
    text = HAT_TOKEN_RE.sub(r"\1-hat", text)

    replacements = {
        r"\mathbb{R}": "R",
        r"\Longrightarrow": "⇒",
        r"\Rightarrow": "⇒",
        r"\leftarrow": "←",
        r"\begin{cases}": "",
        r"\end{cases}": "",
        r"\begincases": "",
        r"\endcases": "",
        r"\subseteq": "⊆",
        r"\setminus": "∖",
        r"\varnothing": "∅",
        r"\infty": "∞",
        r"\approx": "≈",
        r"\neq": "≠",
        r"\geq": "≥",
        r"\leq": "≤",
        r"\ge": "≥",
        r"\le": "≤",
        r"\quad": "  ",
        r"\qquad": "  ",
        r"\sim": "~",
        r"\to": "→",
        r"\iff": "⇔",
        r"\cup": "∪",
        r"\cap": "∩",
        r"\oplus": "⊕",
        r"\times": "×",
        r"\cdot": "·",
        r"\mid": "|",
        r"\|": "|",
        r"\perp": "⊥",
        r"\alpha": "α",
        r"\beta": "β",
        r"\gamma": "γ",
        r"\Gamma": "Γ",
        r"\delta": "δ",
        r"\Delta": "Δ",
        r"\nabla": "∇",
        r"\epsilon": "ϵ",
        r"\eta": "η",
        r"\theta": "θ",
        r"\Theta": "Θ",
        r"\lambda": "λ",
        r"\mu": "μ",
        r"\nu": "ν",
        r"\Omega": "Ω",
        r"\pi": "π",
        r"\rho": "ρ",
        r"\sigma": "σ",
        r"\Sigma": "Σ",
        r"\tau": "τ",
        r"\phi": "φ",
        r"\Phi": "Φ",
        r"\psi": "ψ",
        r"\zeta": "ζ",
        r"\partial": "∂",
        r"\propto": "∝",
        r"\det": "det",
        r"\arg\max": "argmax",
        r"\arg\min": "argmin",
        r"\arg": "arg",
        r"\log": "log",
        r"\exp": "exp",
        r"\max": "max",
        r"\min": "min",
        r"\dots": "...",
        r"\cdots": "...",
        r"\prod": "∏",
        r"\sum": "Σ",
        r"\int": "∫",
        r"\lvert": "|",
        r"\rvert": "|",
        r"\succeq": "⪰",
        r"\mathbf": "",
        r"\mathbb": "",
        r"\mathcal": "",
        r"\mathrm": "",
        r"\left": "",
        r"\right": "",
        r"\bigl": "",
        r"\bigr": "",
        r"\big": "",
        r"\Bigl": "",
        r"\Bigr": "",
        r"\Big": "",
        r"\,": " ",
        r"\;": " ",
        r"\!": "",
        r"\\": "\n",
    }

    for src in sorted(replacements, key=len, reverse=True):
        dst = replacements[src]
        text = text.replace(src, dst)

    text = BAR_SYMBOL_RE.sub(r"\1-bar", text)
    text = HAT_SYMBOL_RE.sub(r"\1-hat", text)
    text = text.replace("&", " ")
    text = text.replace("{", "").replace("}", "")
    return normalize_text(text)


def replace_inline_math(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        return latexish_to_text(match.group(1))

    text = INLINE_MATH_RE.sub(repl, text)
    text = text.replace("**", "")
    return latexish_to_text(text)


def split_table_row(line: str) -> list[str]:
    parts = [replace_inline_math(part.strip()) for part in line.strip().strip("|").split("|")]
    return [part for part in parts]


def normalize_html_text(element: ET.Element | None) -> str:
    if element is None:
        return ""
    return normalize_text(" ".join(element.itertext()))


def parse_table_stack(html_lines: list[str]) -> Block:
    root = ET.fromstring("\n".join(html_lines))
    tables: list[list[list[str]]] = []
    titles: list[str] = []

    outer_row = root.find("./tbody/tr")
    if outer_row is None:
        raise ValueError("table-stack block is missing an outer table row")

    for cell in outer_row.findall("td"):
        inner_table = cell.find("table")
        if inner_table is None:
            continue

        rows: list[list[str]] = []
        header = inner_table.find("thead")
        if header is not None:
            for row in header.findall("tr"):
                rows.append([normalize_html_text(item) for item in row if item.tag in {"th", "td"}])

        body = inner_table.find("tbody")
        if body is not None:
            for row in body.findall("tr"):
                rows.append([normalize_html_text(item) for item in row if item.tag in {"th", "td"}])

        if rows:
            tables.append(rows)
            titles.append(normalize_html_text(cell.find("p")))

    return Block(kind="table_group", tables=tables, titles=titles)


def parse_markdown(markdown_path: Path) -> list[Block]:
    blocks: list[Block] = []
    paragraph: list[str] = []
    table_lines: list[str] = []
    math_lines: list[str] = []
    table_stack_lines: list[str] = []
    in_math = False
    in_table_stack = False

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            text = " ".join(replace_inline_math(line.strip()) for line in paragraph if line.strip())
            if text:
                blocks.append(Block(kind="p", text=text))
            paragraph = []

    def flush_table() -> None:
        nonlocal table_lines
        if not table_lines:
            return
        rows = [split_table_row(line) for line in table_lines if line.strip()]
        if len(rows) >= 2 and TABLE_DIVIDER_RE.match(table_lines[1]):
            rows = [rows[0], *rows[2:]]
        blocks.append(Block(kind="table", rows=rows))
        table_lines = []

    for raw in markdown_path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()

        if in_table_stack:
            if line.strip() == "<!-- table-stack:end -->":
                blocks.append(parse_table_stack(table_stack_lines))
                table_stack_lines = []
                in_table_stack = False
            else:
                table_stack_lines.append(line)
            continue

        if in_math:
            if line.strip() == "$$":
                blocks.append(Block(kind="math", lines=[latexish_to_text(item) for item in math_lines if item.strip()]))
                math_lines = []
                in_math = False
            else:
                math_lines.append(line)
            continue

        if table_lines and not line.lstrip().startswith("|"):
            flush_table()

        if not line.strip():
            flush_paragraph()
            continue

        if line.strip() == "$$":
            flush_paragraph()
            in_math = True
            continue

        if line.strip() == "<!-- table-stack:start -->":
            flush_paragraph()
            flush_table()
            in_table_stack = True
            table_stack_lines = []
            continue

        image_match = IMAGE_RE.match(line.strip())
        if image_match:
            flush_paragraph()
            raw_path = image_match.group("path")
            resolved = (markdown_path.parent / raw_path).resolve()
            if not resolved.exists():
                resolved = (markdown_path.parent.parent / raw_path).resolve()
            blocks.append(
                Block(
                    kind="image",
                    image_path=resolved,
                    alt=image_match.group("alt").strip(),
                )
            )
            continue

        if line.startswith("# "):
            flush_paragraph()
            blocks.append(Block(kind="h1", text=replace_inline_math(line[2:].strip())))
            continue

        if line.startswith("## "):
            flush_paragraph()
            blocks.append(Block(kind="h2", text=replace_inline_math(line[3:].strip())))
            continue

        if line.startswith("### "):
            flush_paragraph()
            blocks.append(Block(kind="h3", text=replace_inline_math(line[4:].strip())))
            continue

        if line.lstrip().startswith("|"):
            flush_paragraph()
            table_lines.append(line)
            continue

        if line.startswith("- "):
            flush_paragraph()
            blocks.append(Block(kind="bullet", text=replace_inline_math(line[2:].strip())))
            continue

        paragraph.append(line)

    flush_paragraph()
    flush_table()
    return blocks


def markdown_uses_images(markdown_path: Path) -> bool:
    for raw in markdown_path.read_text(encoding="utf-8").splitlines():
        if IMAGE_RE.match(raw.strip()):
            return True
    return False


def measure_text(text: str, fontname: str, fontsize: float) -> float:
    if fontname in FONT_METRICS:
        return FONT_METRICS[fontname].text_length(text, fontsize=fontsize)
    return fitz.get_text_length(text, fontname=fontname, fontsize=fontsize)


def split_token_to_fit(token: str, fontname: str, fontsize: float, width: float) -> list[str]:
    pieces: list[str] = []
    chunk = ""
    for char in token:
        candidate = f"{chunk}{char}"
        if not chunk or measure_text(candidate, fontname, fontsize) <= width:
            chunk = candidate
        else:
            pieces.append(chunk)
            chunk = char
    if chunk:
        pieces.append(chunk)
    return pieces


def wrap_text(text: str, fontname: str, fontsize: float, width: float) -> list[str]:
    wrapped: list[str] = []
    for paragraph in text.split("\n"):
        words: list[str] = []
        for raw_word in paragraph.split():
            if measure_text(raw_word, fontname, fontsize) <= width:
                words.append(raw_word)
            else:
                words.extend(split_token_to_fit(raw_word, fontname, fontsize, width))
        if not words:
            wrapped.append("")
            continue
        line = words[0]
        for word in words[1:]:
            candidate = f"{line} {word}"
            if measure_text(candidate, fontname, fontsize) <= width:
                line = candidate
            else:
                wrapped.append(line)
                line = word
        wrapped.append(line)
    return wrapped


def style_for(kind: str) -> tuple[str, float, float]:
    if kind == "h1":
        return ("bodybold", 22, 16)
    if kind == "h2":
        return ("bodybold", 16, 12)
    if kind == "h3":
        return ("bodybold", 12.5, 8)
    if kind == "bullet":
        return ("body", 11, 4)
    if kind == "math":
        return ("math", 11.2, 8)
    if kind == "caption":
        return ("body", 9.2, 6)
    return ("body", 11, 7)


def new_page(doc: fitz.Document, page_num: int) -> fitz.Page:
    page = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
    page.draw_rect(page.rect, fill=(1, 1, 1))
    for alias, path in FONT_FILES.items():
        page.insert_font(fontname=alias, fontfile=str(path))
    page.insert_text(
        fitz.Point(MARGIN_X, 28),
        f"{TITLE} ({SUBTITLE}) - page {page_num}",
        fontname="body",
        fontfile=str(FONT_FILES["body"]),
        fontsize=8.4,
        color=(0.42, 0.48, 0.56),
    )
    return page


def add_page(doc: fitz.Document, page_num: int) -> tuple[fitz.Page, float]:
    page = new_page(doc, page_num)
    return page, MARGIN_TOP


def draw_wrapped_lines(
    page: fitz.Page,
    y: float,
    lines: list[str],
    x: float,
    fontname: str,
    fontsize: float,
    color: tuple[float, float, float],
    lineheight: float = 1.33,
    center: bool = False,
) -> float:
    step = fontsize * lineheight
    for line in lines:
        if center:
            width = measure_text(line, fontname, fontsize)
            page.insert_text(
                fitz.Point((PAGE_WIDTH - width) / 2, y + fontsize),
                line,
                fontname=fontname,
                fontfile=str(FONT_FILES[fontname]) if fontname in FONT_FILES else None,
                fontsize=fontsize,
                color=color,
            )
        else:
            page.insert_text(
                fitz.Point(x, y + fontsize),
                line,
                fontname=fontname,
                fontfile=str(FONT_FILES[fontname]) if fontname in FONT_FILES else None,
                fontsize=fontsize,
                color=color,
            )
        y += step
    return y


def render_text_block(
    doc: fitz.Document,
    page: fitz.Page,
    page_num: int,
    y: float,
    block: Block,
) -> tuple[fitz.Page, int, float]:
    fontname, fontsize, gap_after = style_for(block.kind)
    width = PAGE_WIDTH - 2 * MARGIN_X
    x = MARGIN_X
    prefix = ""
    if block.kind == "bullet":
        width -= 16
        x += 16
        prefix = "- "

    lines = wrap_text(prefix + block.text, fontname, fontsize, width)
    needed = len(lines) * fontsize * 1.33 + gap_after + LINE_GAP

    if y + needed > PAGE_HEIGHT - MARGIN_BOTTOM:
        page_num += 1
        page, y = add_page(doc, page_num)

    color = (0.08, 0.1, 0.12)
    if block.kind.startswith("h"):
        color = (0.07, 0.14, 0.24)

    y = draw_wrapped_lines(page, y, lines, x, fontname, fontsize, color)
    y += gap_after
    return page, page_num, y


def render_math_block(
    doc: fitz.Document,
    page: fitz.Page,
    page_num: int,
    y: float,
    block: Block,
) -> tuple[fitz.Page, int, float]:
    fontname, fontsize, gap_after = style_for("math")
    lines = block.lines or []
    if not lines:
        return page, page_num, y

    max_width = PAGE_WIDTH - 2 * MARGIN_X - 18
    wrapped_lines: list[str] = []
    for line in lines:
        wrapped_lines.extend(wrap_text(line, fontname, fontsize, max_width))

    needed = len(wrapped_lines) * fontsize * 1.38 + 18 + gap_after + LINE_GAP
    if y + needed > PAGE_HEIGHT - MARGIN_BOTTOM:
        page_num += 1
        page, y = add_page(doc, page_num)

    box = fitz.Rect(MARGIN_X, y, PAGE_WIDTH - MARGIN_X, y + needed - gap_after - LINE_GAP)
    page.draw_rect(box, fill=(0.97, 0.98, 1.0), color=(0.86, 0.89, 0.94), width=0.7)
    y = draw_wrapped_lines(
        page,
        y + 8,
        wrapped_lines,
        MARGIN_X + 10,
        fontname,
        fontsize,
        (0.14, 0.19, 0.25),
        lineheight=1.38,
        center=True,
    )
    y += gap_after
    return page, page_num, y


def render_image_block(
    doc: fitz.Document,
    page: fitz.Page,
    page_num: int,
    y: float,
    block: Block,
) -> tuple[fitz.Page, int, float]:
    if block.image_path is None or not block.image_path.exists():
        return render_text_block(doc, page, page_num, y, Block(kind="p", text=f"[missing image] {block.alt}"))

    pix = fitz.Pixmap(str(block.image_path))
    available_width = PAGE_WIDTH - 2 * MARGIN_X
    available_height = PAGE_HEIGHT - MARGIN_BOTTOM - y - IMAGE_GAP
    scale = min(available_width / pix.width, MAX_IMAGE_HEIGHT / pix.height)

    target_w = pix.width * scale
    target_h = pix.height * scale

    if target_h > available_height and y > MARGIN_TOP + 40:
        page_num += 1
        page, y = add_page(doc, page_num)
        available_height = PAGE_HEIGHT - MARGIN_BOTTOM - y - IMAGE_GAP
        scale = min(available_width / pix.width, MAX_IMAGE_HEIGHT / pix.height, available_height / pix.height)
        target_w = pix.width * scale
        target_h = pix.height * scale

    x0 = (PAGE_WIDTH - target_w) / 2
    rect = fitz.Rect(x0, y, x0 + target_w, y + target_h)
    page.insert_image(rect, filename=str(block.image_path))
    page.draw_rect(rect, color=(0.82, 0.86, 0.91), width=0.8)
    y = rect.y1 + IMAGE_GAP
    return page, page_num, y


def render_table_block(
    doc: fitz.Document,
    page: fitz.Page,
    page_num: int,
    y: float,
    block: Block,
) -> tuple[fitz.Page, int, float]:
    rows = block.rows or []
    if not rows:
        return page, page_num, y

    width = PAGE_WIDTH - 2 * MARGIN_X
    needed = estimate_table_height(rows, width, fontsize=10.2, min_row_height=22) + 10
    if y + needed > PAGE_HEIGHT - MARGIN_BOTTOM:
        page_num += 1
        page, y = add_page(doc, page_num)
    y = render_table_at(page, MARGIN_X, y, width, rows, fontsize=10.2, row_height=22)
    y += 10
    return page, page_num, y


def compute_table_widths(rows: list[list[str]], width: float, fontsize: float, *, fill_available: bool = False) -> list[float]:
    col_count = max(len(row) for row in rows)
    col_weights: list[float] = []
    for col_idx in range(col_count):
        longest = 0.0
        for row in rows:
            if col_idx < len(row):
                longest = max(longest, measure_text(row[col_idx], "body", fontsize))
        col_weights.append(max(longest + 2 * TABLE_CELL_PAD_X, 70.0))

    total_weight = sum(col_weights)
    scale = min(1.0, width / total_weight)
    col_widths = [item * scale for item in col_weights]
    extra = width - sum(col_widths)
    if fill_available and extra > 0:
        col_widths[-1] += extra
    return col_widths


def render_table_at(
    page: fitz.Page,
    x0: float,
    y: float,
    width: float,
    rows: list[list[str]],
    *,
    fontsize: float,
    row_height: float,
) -> float:
    col_count = max(len(row) for row in rows)
    col_widths = compute_table_widths(rows, width, fontsize, fill_available=False)
    actual_width = sum(col_widths)
    table_x0 = x0 + max(0.0, (width - actual_width) / 2)

    for row_idx, row in enumerate(rows):
        is_header = row_idx == 0
        fontname = "bodybold" if is_header else "body"
        cell_lines_per_col: list[list[str]] = []
        max_lines = 1
        for col_idx in range(col_count):
            cell = row[col_idx] if col_idx < len(row) else ""
            wrap_width = max(24.0, col_widths[col_idx] - 2 * TABLE_CELL_PAD_X)
            lines = wrap_text(cell, fontname, fontsize, wrap_width) or [""]
            cell_lines_per_col.append(lines)
            max_lines = max(max_lines, len(lines))

        line_step = fontsize * 1.18
        content_height = max_lines * line_step
        effective_row_height = max(row_height, content_height + 2 * TABLE_CELL_PAD_Y + 2)
        x = table_x0
        for col_idx in range(col_count):
            cell_rect = fitz.Rect(x, y, x + col_widths[col_idx], y + effective_row_height)
            if is_header:
                page.draw_rect(cell_rect, fill=(0.93, 0.96, 0.99), color=(0.77, 0.83, 0.9), width=0.7)
            else:
                page.draw_rect(cell_rect, color=(0.83, 0.86, 0.9), width=0.6)
            lines = cell_lines_per_col[col_idx]
            block_height = len(lines) * line_step
            baseline_y = cell_rect.y0 + (effective_row_height - block_height) / 2 + fontsize
            for line_idx, line in enumerate(lines):
                line_width = measure_text(line, fontname, fontsize)
                text_x = max(cell_rect.x0 + TABLE_CELL_PAD_X, cell_rect.x0 + (col_widths[col_idx] - line_width) / 2)
                page.insert_text(
                    fitz.Point(text_x, baseline_y + line_idx * line_step),
                    line,
                    fontname=fontname,
                    fontfile=str(FONT_FILES[fontname]),
                    fontsize=fontsize,
                    color=(0.1, 0.12, 0.16),
                )
            x += col_widths[col_idx]
        y += effective_row_height

    return y


def estimate_table_height(rows: list[list[str]], width: float, fontsize: float, min_row_height: float) -> float:
    col_count = max(len(row) for row in rows)
    col_widths = compute_table_widths(rows, width, fontsize, fill_available=False)
    total = 0.0
    for row_idx, row in enumerate(rows):
        fontname = "bodybold" if row_idx == 0 else "body"
        max_lines = 1
        for col_idx in range(col_count):
            cell = row[col_idx] if col_idx < len(row) else ""
            wrap_width = max(24.0, col_widths[col_idx] - 2 * TABLE_CELL_PAD_X)
            lines = wrap_text(cell, fontname, fontsize, wrap_width) or [""]
            max_lines = max(max_lines, len(lines))
        content_height = max_lines * fontsize * 1.18
        total += max(min_row_height, content_height + 2 * TABLE_CELL_PAD_Y + 2)
    return total


def render_table_group_block(
    doc: fitz.Document,
    page: fitz.Page,
    page_num: int,
    y: float,
    block: Block,
) -> tuple[fitz.Page, int, float]:
    tables = block.tables or []
    titles = block.titles or []
    if not tables:
        return page, page_num, y

    count = len(tables)
    available_width = PAGE_WIDTH - 2 * MARGIN_X
    section_width = (available_width - TABLE_GROUP_GAP * (count - 1)) / count
    title_font = "bodybold"
    title_size = 10.4
    title_lineheight = 1.24
    title_gap = 6
    row_height = 21
    body_fontsize = 9.6

    section_heights: list[float] = []
    for idx, rows in enumerate(tables):
        title = titles[idx] if idx < len(titles) else ""
        title_lines = wrap_text(title, title_font, title_size, section_width) if title else []
        title_height = len(title_lines) * title_size * title_lineheight + (title_gap if title else 0)
        table_height = estimate_table_height(rows, section_width, fontsize=body_fontsize, min_row_height=row_height)
        section_heights.append(title_height + table_height)

    needed = max(section_heights, default=0.0) + 10
    if y + needed > PAGE_HEIGHT - MARGIN_BOTTOM:
        page_num += 1
        page, y = add_page(doc, page_num)

    x = MARGIN_X
    for idx, rows in enumerate(tables):
        title = titles[idx] if idx < len(titles) else ""
        current_y = y
        col_widths = compute_table_widths(rows, section_width, body_fontsize, fill_available=False)
        actual_width = sum(col_widths)
        table_x = x + max(0.0, (section_width - actual_width) / 2)
        if title:
            title_lines = wrap_text(title, title_font, title_size, section_width)
            title_width = max((measure_text(line, title_font, title_size) for line in title_lines), default=0.0)
            title_x = x + max(0.0, (section_width - title_width) / 2)
            current_y = draw_wrapped_lines(
                page,
                current_y,
                title_lines,
                title_x,
                title_font,
                title_size,
                (0.07, 0.14, 0.24),
                lineheight=title_lineheight,
            )
            current_y += title_gap
        render_table_at(page, table_x, current_y, actual_width, rows, fontsize=body_fontsize, row_height=row_height)
        x += section_width + TABLE_GROUP_GAP

    y += needed
    return page, page_num, y


def render_blocks(blocks: list[Block], output_pdf: Path) -> None:
    doc = fitz.open()
    page_num = 1
    page, y = add_page(doc, page_num)

    for block in blocks:
        if block.kind in {"h1", "h2", "h3", "p", "bullet"}:
            page, page_num, y = render_text_block(doc, page, page_num, y, block)
        elif block.kind == "math":
            page, page_num, y = render_math_block(doc, page, page_num, y, block)
        elif block.kind == "table":
            page, page_num, y = render_table_block(doc, page, page_num, y, block)
        elif block.kind == "table_group":
            page, page_num, y = render_table_group_block(doc, page, page_num, y, block)
        elif block.kind == "image":
            page, page_num, y = render_image_block(doc, page, page_num, y, block)
        else:
            page, page_num, y = render_text_block(doc, page, page_num, y, Block(kind="p", text=block.text))

        y += LINE_GAP

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    doc.set_metadata(
        {
            "title": f"{TITLE} ({SUBTITLE})",
            "author": "OpenAI Codex",
            "subject": SUBJECT or f"{TITLE} ({SUBTITLE})",
        }
    )
    doc.save(
        output_pdf,
        garbage=4,
        deflate=True,
        deflate_images=True,
        deflate_fonts=True,
        use_objstms=1,
        compression_effort=100,
    )
    doc.close()


def extract_figures(source_pdf: Path, assets_dir: Path) -> None:
    assets_dir.mkdir(parents=True, exist_ok=True)
    stale_assets = {
        "example_2_12_bernoulli_likelihood.png",
        "example_2_13_gaussian_likelihood.png",
        "example_2_17_histograms.png",
        "example_2_20_hyperprior_mixture.png",
        "example_2_22_model_scores.png",
        "example_2_28_copula_like_flow.png",
        "example_2_29_affine_flow_panels.png",
        "figure_2_2_beta_curves.png",
        "figure_2_4_convexity_sketch.png",
    }
    for name in stale_assets:
        path = assets_dir / name
        if path.exists():
            path.unlink()
    doc = fitz.open(source_pdf)
    for spec in FIGURE_SPECS:
        page = doc[spec.page_index]
        clip = fitz.Rect(*spec.clip)
        pix = page.get_pixmap(matrix=fitz.Matrix(spec.scale, spec.scale), clip=clip, alpha=False)
        target = assets_dir / spec.filename
        if target.exists():
            target.unlink()
        pix.save(target)
    doc.close()


def write_sequential_update_assets(assets_dir: Path) -> None:
    dot_path = assets_dir / "figure_2_4_sequential_updates.dot"
    dot_path.write_text(
        "\n".join(
            [
                "digraph SequentialUpdates {",
                '  rankdir=LR;',
                '  node [shape=box, style="rounded,filled", fillcolor="#f6f8fc", color="#8ea1c2", fontname="Helvetica"];',
                '  edge [color="#7d8fb2", penwidth=1.2, arrowsize=0.8];',
                '  prior [label="Prior\\np(θ)"];',
                '  like1 [label="Data 1\\np(D₁ | θ)"];',
                '  post1 [label="Posterior\\np(θ | D₁)"];',
                '  like2 [label="Data 2\\np(D₂ | θ, D₁)"];',
                '  post2 [label="Updated posterior\\np(θ | D₁, D₂)"];',
                '  prior -> like1 -> post1 -> like2 -> post2;',
                "}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    svg_path = assets_dir / "figure_2_4_sequential_updates.svg"
    svg_path.write_text(
        """<svg xmlns="http://www.w3.org/2000/svg" width="820" height="220" viewBox="0 0 820 220">
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#7d8fb2"/>
    </marker>
  </defs>
  <rect x="24" y="0" width="772" height="220" rx="14" fill="#ffffff"/>
  <g font-family="Helvetica, Arial, sans-serif" text-anchor="middle">
    <rect x="36" y="56" width="132" height="72" rx="12" fill="#f6f8fc" stroke="#8ea1c2" stroke-width="2"/>
    <text x="102" y="82" font-size="18" fill="#2f3b52">Prior</text>
    <rect x="194" y="56" width="132" height="72" rx="12" fill="#fdf8f0" stroke="#c5a16a" stroke-width="2"/>
    <text x="260" y="82" font-size="18" fill="#4e412c">Data 1</text>

    <rect x="352" y="56" width="132" height="72" rx="12" fill="#f6f8fc" stroke="#8ea1c2" stroke-width="2"/>
    <text x="418" y="82" font-size="18" fill="#2f3b52">Posterior</text>

    <rect x="510" y="56" width="132" height="72" rx="12" fill="#fdf8f0" stroke="#c5a16a" stroke-width="2"/>
    <text x="576" y="82" font-size="18" fill="#4e412c">Data 2</text>

    <rect x="668" y="56" width="132" height="72" rx="12" fill="#eef7f3" stroke="#7ea78f" stroke-width="2"/>
    <text x="734" y="82" font-size="18" fill="#2c5041">Updated belief</text>

    <line x1="168" y1="92" x2="194" y2="92" stroke="#7d8fb2" stroke-width="3" marker-end="url(#arrow)"/>
    <line x1="326" y1="92" x2="352" y2="92" stroke="#7d8fb2" stroke-width="3" marker-end="url(#arrow)"/>
    <line x1="484" y1="92" x2="510" y2="92" stroke="#7d8fb2" stroke-width="3" marker-end="url(#arrow)"/>
    <line x1="642" y1="92" x2="668" y2="92" stroke="#7d8fb2" stroke-width="3" marker-end="url(#arrow)"/>
  </g>
  <text x="410" y="178" font-family="Helvetica, Arial, sans-serif" font-size="15" text-anchor="middle" fill="#556274">
    Bayesian learning reuses the posterior after D1 as the new prior before incorporating D2.
  </text>
</svg>
""",
        encoding="utf-8",
    )

    png_path = assets_dir / "figure_2_4_sequential_updates.png"
    doc = fitz.open()
    page = doc.new_page(width=820, height=220)
    page.draw_rect(page.rect, fill=(1, 1, 1))
    for alias, path in FONT_FILES.items():
        page.insert_font(fontname=alias, fontfile=str(path))

    boxes = [
        (36, 56, 168, 128, (0.965, 0.973, 0.988), (0.556, 0.631, 0.761), "Prior"),
        (194, 56, 326, 128, (0.992, 0.973, 0.941), (0.773, 0.631, 0.416), "Data 1"),
        (352, 56, 484, 128, (0.965, 0.973, 0.988), (0.556, 0.631, 0.761), "Posterior"),
        (510, 56, 642, 128, (0.992, 0.973, 0.941), (0.773, 0.631, 0.416), "Data 2"),
        (668, 56, 800, 128, (0.933, 0.969, 0.953), (0.494, 0.655, 0.561), "Updated belief"),
    ]
    for x0, y0, x1, y1, fill, stroke, title in boxes:
        page.draw_rect(fitz.Rect(x0, y0, x1, y1), fill=fill, color=stroke, width=2)
        page.insert_textbox(
            fitz.Rect(x0, y0 + 12, x1, y1 - 10),
            title,
            fontname="bodybold",
            fontfile=str(FONT_FILES["bodybold"]),
            fontsize=18,
            color=(0.2, 0.24, 0.33),
            align=1,
        )

    arrow_y = 92
    for start_x, end_x in [(168, 194), (326, 352), (484, 510), (642, 668)]:
        page.draw_line(fitz.Point(start_x, arrow_y), fitz.Point(end_x - 6, arrow_y), color=(0.49, 0.56, 0.7), width=3)
        page.draw_line(fitz.Point(end_x - 12, arrow_y - 6), fitz.Point(end_x, arrow_y), color=(0.49, 0.56, 0.7), width=3)
        page.draw_line(fitz.Point(end_x - 12, arrow_y + 6), fitz.Point(end_x, arrow_y), color=(0.49, 0.56, 0.7), width=3)

    page.insert_textbox(
        fitz.Rect(40, 162, 780, 194),
        "Bayesian updating treats the posterior after D1 as the prior before incorporating D2.",
        fontname="body",
        fontfile=str(FONT_FILES["body"]),
        fontsize=14,
        color=(0.33, 0.39, 0.46),
        align=1,
    )

    pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0), alpha=False)
    pix.save(png_path)
    doc.close()


def build(markdown_path: Path, source_pdf: Path, assets_dir: Path, output_pdf: Path) -> None:
    if markdown_uses_images(markdown_path):
        extract_figures(source_pdf, assets_dir)
        write_sequential_update_assets(assets_dir)
    blocks = parse_markdown(markdown_path)
    render_blocks(blocks, output_pdf)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the reconstructed Chapter 2 notes artifact.")
    parser.add_argument(
        "--markdown",
        default="02_probability_main/README.md",
        help="Path to the reconstructed markdown source",
    )
    parser.add_argument(
        "--source-pdf",
        default="notes/02_probability_reconstructed/source/02_probability.pdf",
        help="Path to the source PDF used for figure clipping",
    )
    parser.add_argument(
        "--assets-dir",
        default="notes/02_probability_reconstructed/assets",
        help="Directory for extracted assets",
    )
    parser.add_argument(
        "--output-pdf",
        default="notes/02_probability_reconstructed/dist/02_probability.reconstructed.pdf",
        help="Path to the rendered PDF output",
    )
    parser.add_argument(
        "--title",
        default=TITLE,
        help="Title used in the page header and PDF metadata",
    )
    parser.add_argument(
        "--subtitle",
        default=SUBTITLE,
        help="Subtitle used in the page header and PDF metadata",
    )
    parser.add_argument(
        "--subject",
        default="",
        help="Optional PDF metadata subject",
    )
    return parser.parse_args()


def main() -> None:
    global TITLE, SUBTITLE, SUBJECT
    args = parse_args()
    TITLE = args.title
    SUBTITLE = args.subtitle
    root = Path(__file__).resolve().parents[2]
    markdown_path = (root / args.markdown).resolve()
    source_pdf = (root / args.source_pdf).resolve()
    assets_dir = (root / args.assets_dir).resolve()
    output_pdf = (root / args.output_pdf).resolve()
    SUBJECT = args.subject or f"Rendered from {markdown_path.name} using {source_pdf.name}"
    build(markdown_path, source_pdf, assets_dir, output_pdf)


if __name__ == "__main__":
    main()

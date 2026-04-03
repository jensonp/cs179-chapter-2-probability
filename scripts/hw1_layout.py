#!/usr/bin/env python3
"""Shared layout metadata for the CS179 homework 1 template."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PDF = ROOT / "cs179-hw1.pdf"
FILLABLE_OUTPUT_PDF = ROOT / "output" / "pdf" / "cs179-hw1-fillable.pdf"
LATEX_OUTPUT_PDF = ROOT / "output" / "pdf" / "cs179-hw1-latex-template.pdf"
OVERLEAF_PROJECT_DIR = ROOT / "output" / "overleaf" / "cs179-hw1-project"
PAGE_WIDTH_PT = 612.0
PAGE_HEIGHT_PT = 792.0


@dataclass(frozen=True)
class TextFieldSpec:
    page: int
    name: str
    rect: tuple[float, float, float, float]
    multiline: bool = False
    font_size: float = 11
    draw_box: bool = False
    box_padding: float = 0.0
    box_line_width: float = 0.75
    content_mode: str = "inline"
    preserve_linebreaks: bool = False

    @property
    def width(self) -> float:
        return self.rect[2] - self.rect[0]

    @property
    def height(self) -> float:
        return self.rect[3] - self.rect[1]


@dataclass(frozen=True)
class CheckboxSpec:
    page: int
    name: str
    rect: tuple[float, float, float, float]
    font_size: float = 10

    @property
    def width(self) -> float:
        return self.rect[2] - self.rect[0]

    @property
    def height(self) -> float:
        return self.rect[3] - self.rect[1]


def inset(rect: tuple[float, float, float, float], dx: float, dy: float) -> tuple[float, float, float, float]:
    x0, y0, x1, y1 = rect
    return (x0 + dx, y0 + dy, x1 - dx, y1 - dy)


TEXT_FIELDS = [
    TextFieldSpec(1, "student_name", inset((393.53, 66.92, 539.52, 95.61), 4, 4)),
    TextFieldSpec(1, "student_ucinetid", inset((393.53, 110.44, 539.52, 139.13), 4, 4)),
    TextFieldSpec(3, "problem1_p_d_eq_1", inset((396.20, 262.70, 542.19, 300.96), 4, 4), multiline=True),
    TextFieldSpec(3, "problem1_p_c_eq_1_d_eq_1", inset((396.20, 377.10, 542.19, 415.36), 4, 4), multiline=True),
    TextFieldSpec(3, "problem1_p_d_eq_1_given_c_eq_1", inset((396.20, 491.50, 542.19, 529.75), 4, 4), multiline=True),
    TextFieldSpec(3, "problem1_p_c_eq_1_given_t_eq_1_d_eq_0", inset((396.20, 617.85, 542.19, 656.11), 4, 4), multiline=True),
    TextFieldSpec(4, "problem2_p_coolant_low_given_warning", inset((396.20, 272.94, 542.19, 311.20), 4, 4), multiline=True),
    TextFieldSpec(4, "problem2_p_coolant_low_given_warning_and_hot", inset((396.20, 422.38, 542.19, 460.63), 4, 4), multiline=True),
    TextFieldSpec(4, "problem2_state_count", inset((147.91, 585.55, 293.91, 623.80), 4, 4), multiline=True),
    TextFieldSpec(4, "problem2_parameter_count", inset((345.39, 587.88, 491.38, 626.14), 4, 4), multiline=True),
    # Page 5 reasoning boxes are drawn by the template; keep them below the Yes/No circles.
    TextFieldSpec(5, "problem3_q1_reasoning", (125.0, 210.5, 540.0, 284.0), multiline=True, font_size=10, draw_box=True, box_padding=4.0, content_mode="block", preserve_linebreaks=True),
    TextFieldSpec(5, "problem3_q2_reasoning", (125.0, 333.0, 540.0, 406.0), multiline=True, font_size=10, draw_box=True, box_padding=4.0, content_mode="block", preserve_linebreaks=True),
    TextFieldSpec(5, "problem3_q3_reasoning", (125.0, 455.0, 540.0, 529.0), multiline=True, font_size=10, draw_box=True, box_padding=4.0, content_mode="block", preserve_linebreaks=True),
    TextFieldSpec(5, "problem3_q4_reasoning", (125.0, 602.0, 540.0, 742.0), multiline=True, font_size=10, draw_box=True, box_padding=4.0, content_mode="block", preserve_linebreaks=True),
    TextFieldSpec(6, "problem4_beta_histogram_notes", inset((324.20, 206.69, 542.19, 422.70), 5, 5), multiline=True, font_size=10, content_mode="block", preserve_linebreaks=True),
    TextFieldSpec(6, "problem4_geometric_histogram_notes", inset((324.20, 487.48, 542.19, 703.48), 5, 5), multiline=True, font_size=10, content_mode="block", preserve_linebreaks=True),
    TextFieldSpec(7, "problem5_short_one_coin_rho", inset((97.10, 224.25, 243.10, 262.50), 4, 4), multiline=True),
    TextFieldSpec(7, "problem5_short_two_coin_rhos", inset((332.89, 224.44, 478.89, 262.70), 4, 4), multiline=True),
    TextFieldSpec(7, "problem5_short_one_coin_loglik", inset((97.10, 397.26, 243.10, 435.52), 4, 4), multiline=True),
    TextFieldSpec(7, "problem5_short_two_coin_loglik", inset((332.89, 397.26, 478.89, 435.52), 4, 4), multiline=True),
    TextFieldSpec(7, "problem5_short_one_coin_bic", inset((97.10, 582.04, 243.10, 620.30), 4, 4), multiline=True),
    TextFieldSpec(7, "problem5_short_two_coin_bic", inset((332.89, 582.04, 478.89, 620.30), 4, 4), multiline=True),
    TextFieldSpec(8, "problem5_long_one_coin_rho", inset((97.10, 141.53, 243.10, 179.78), 4, 4), multiline=True),
    TextFieldSpec(8, "problem5_long_two_coin_rhos", inset((332.89, 141.72, 478.89, 179.98), 4, 4), multiline=True),
    TextFieldSpec(8, "problem5_long_one_coin_bic", inset((97.10, 403.20, 243.10, 441.46), 4, 4), multiline=True),
    TextFieldSpec(8, "problem5_long_two_coin_bic", inset((332.89, 403.20, 478.89, 441.46), 4, 4), multiline=True),
    # Extra work areas (answer boxes already exist on the original PDF).
    # Problem 1: one work box per bullet (left side, below each answer blank).
    TextFieldSpec(3, "problem1_work", (72.0, 270.0, 392.0, 340.0), multiline=True, font_size=10, draw_box=True, box_padding=6.0, content_mode="block", preserve_linebreaks=True),
    TextFieldSpec(3, "problem1_work2", (72.0, 385.0, 392.0, 455.0), multiline=True, font_size=10, draw_box=True, box_padding=6.0, content_mode="block", preserve_linebreaks=True),
    TextFieldSpec(3, "problem1_work3", (72.0, 506.0, 392.0, 570.0), multiline=True, font_size=10, draw_box=True, box_padding=6.0, content_mode="block", preserve_linebreaks=True),
    TextFieldSpec(3, "problem1_work4", (72.0, 635.0, 392.0, 760.0), multiline=True, font_size=10, draw_box=True, box_padding=6.0, content_mode="block", preserve_linebreaks=True),
    # Problem 2: work boxes to the left of each answer blank.
    TextFieldSpec(4, "problem2_work", (72.0, 255.0, 392.0, 360.0), multiline=True, font_size=10, draw_box=True, box_padding=6.0, content_mode="block", preserve_linebreaks=True),
    TextFieldSpec(4, "problem2_work2", (72.0, 405.0, 392.0, 515.0), multiline=True, font_size=10, draw_box=True, box_padding=6.0, content_mode="block", preserve_linebreaks=True),
    # Problem 5: work areas under each bullet question.
    TextFieldSpec(7, "problem5_short_work_mle", (72.0, 270.0, 540.0, 332.0), multiline=True, font_size=10, draw_box=True, box_padding=6.0, content_mode="block", preserve_linebreaks=True),
    TextFieldSpec(7, "problem5_short_work_loglik", (72.0, 440.0, 540.0, 505.0), multiline=True, font_size=10, draw_box=True, box_padding=6.0, content_mode="block", preserve_linebreaks=True),
    TextFieldSpec(7, "problem5_short_work", (72.0, 625.0, 540.0, 758.0), multiline=True, font_size=10, draw_box=True, box_padding=6.0, content_mode="block", preserve_linebreaks=True),
    TextFieldSpec(8, "problem5_long_work_mle", (72.0, 190.0, 540.0, 335.0), multiline=True, font_size=10, draw_box=True, box_padding=6.0, content_mode="block", preserve_linebreaks=True),
    TextFieldSpec(8, "problem5_long_work", (72.0, 450.0, 540.0, 758.0), multiline=True, font_size=10, draw_box=True, box_padding=6.0, content_mode="block", preserve_linebreaks=True),
    TextFieldSpec(9, "statement_of_collaboration", inset((73.98, 238.30, 543.98, 382.30), 6, 6), multiline=True, font_size=11, content_mode="block", preserve_linebreaks=True),
]


CHECKBOX_FIELDS = [
    CheckboxSpec(5, "problem3_q1_yes", (141.4, 184.5, 153.8, 194.1)),
    CheckboxSpec(5, "problem3_q1_no", (191.3, 184.5, 203.7, 194.1)),
    CheckboxSpec(5, "problem3_q2_yes", (141.4, 306.7, 153.8, 316.2)),
    CheckboxSpec(5, "problem3_q2_no", (191.3, 306.7, 203.7, 316.2)),
    CheckboxSpec(5, "problem3_q3_yes", (141.4, 428.8, 153.8, 438.4)),
    CheckboxSpec(5, "problem3_q3_no", (191.3, 428.8, 203.7, 438.4)),
    CheckboxSpec(5, "problem3_q4_set1_yes", (97.1, 575.0, 109.5, 584.6)),
    CheckboxSpec(5, "problem3_q4_set1_no", (147.0, 575.0, 159.4, 584.6)),
    CheckboxSpec(5, "problem3_q4_set2_yes", (236.2, 575.0, 248.5, 584.6)),
    CheckboxSpec(5, "problem3_q4_set2_no", (286.1, 575.0, 298.5, 584.6)),
    CheckboxSpec(5, "problem3_q4_set3_yes", (375.3, 575.0, 387.6, 584.6)),
    CheckboxSpec(5, "problem3_q4_set3_no", (425.2, 575.0, 437.5, 584.6)),
]


ALL_FIELD_NAMES = [field.name for field in TEXT_FIELDS] + [field.name for field in CHECKBOX_FIELDS]


def rectangles_overlap(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> bool:
    ax0, ay0, ax1, ay1 = a
    bx0, by0, bx1, by1 = b
    overlap_width = min(ax1, bx1) - max(ax0, bx0)
    overlap_height = min(ay1, by1) - max(ay0, by0)
    return overlap_width > 0 and overlap_height > 0


def validate_layout_specs(
    text_fields: list[TextFieldSpec] | None = None,
    checkbox_fields: list[CheckboxSpec] | None = None,
) -> None:
    text_fields = TEXT_FIELDS if text_fields is None else text_fields
    checkbox_fields = CHECKBOX_FIELDS if checkbox_fields is None else checkbox_fields

    all_fields: list[TextFieldSpec | CheckboxSpec] = [*text_fields, *checkbox_fields]
    errors: list[str] = []

    for field in all_fields:
        x0, y0, x1, y1 = field.rect
        if not (0 <= x0 < x1 <= PAGE_WIDTH_PT):
            errors.append(f"{field.name}: x-range {field.rect} is outside page width {PAGE_WIDTH_PT}.")
        if not (0 <= y0 < y1 <= PAGE_HEIGHT_PT):
            errors.append(f"{field.name}: y-range {field.rect} is outside page height {PAGE_HEIGHT_PT}.")

        if isinstance(field, TextFieldSpec):
            if field.box_padding < 0:
                errors.append(f"{field.name}: box_padding must be non-negative.")
            if field.box_padding * 2 >= field.width:
                errors.append(f"{field.name}: box_padding consumes the entire field width.")
            if field.box_padding * 2 >= field.height:
                errors.append(f"{field.name}: box_padding consumes the entire field height.")
            if field.font_size <= 0:
                errors.append(f"{field.name}: font_size must be positive.")

    by_page: dict[int, list[TextFieldSpec | CheckboxSpec]] = {}
    for field in all_fields:
        by_page.setdefault(field.page, []).append(field)

    for page, page_fields in sorted(by_page.items()):
        for left, right in combinations(page_fields, 2):
            if rectangles_overlap(left.rect, right.rect):
                errors.append(
                    f"Page {page}: {left.name} at {left.rect} overlaps {right.name} at {right.rect}."
                )

    if errors:
        raise ValueError("Invalid HW1 layout metadata:\n" + "\n".join(errors))

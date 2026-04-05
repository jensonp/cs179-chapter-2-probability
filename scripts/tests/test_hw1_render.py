import unittest

from hw1_layout import TextFieldSpec, validate_layout_specs
from render_hw1_latex_answers import (
    coerce_inline_field_text,
    collect_answers_content_issues,
    preserve_user_linebreaks,
    render_answers_tex,
    render_answers_toml,
    validate_answers_content,
)


class Hw1RenderTests(unittest.TestCase):
    def test_layout_validation_rejects_overlap(self) -> None:
        left = TextFieldSpec(1, "left", (0.0, 0.0, 20.0, 20.0))
        right = TextFieldSpec(1, "right", (10.0, 10.0, 30.0, 30.0))
        with self.assertRaisesRegex(ValueError, "overlaps"):
            validate_layout_specs([left, right], [])

    def test_preserve_user_linebreaks_formats_plain_text(self) -> None:
        text = "first line\nsecond line\n\nthird line"
        self.assertEqual(
            preserve_user_linebreaks(text),
            "first line\\\\ second line\n\\par\nthird line",
        )

    def test_preserve_user_linebreaks_leaves_block_math_unchanged(self) -> None:
        text = "$$\na+b\n$$"
        self.assertEqual(preserve_user_linebreaks(text), text)

    def test_preserve_user_linebreaks_keeps_entire_block_math_with_blank_lines(self) -> None:
        text = "$$\n\na+b\n\n$$"
        self.assertEqual(preserve_user_linebreaks(text), text.strip())

    def test_preserve_user_linebreaks_drops_empty_block_math_placeholder(self) -> None:
        self.assertEqual(preserve_user_linebreaks("$$\n\n$$"), "")

    def test_inline_field_reports_display_math_issue(self) -> None:
        issues = collect_answers_content_issues({"problem1_p_d_eq_1": "$$\n1+1\n$$"})
        self.assertEqual(len(issues), 1)
        self.assertIn("short answer slots only support inline/final answers", issues[0])

    def test_inline_field_display_math_is_coerced_for_rendering(self) -> None:
        self.assertEqual(coerce_inline_field_text("$$\n1 + 1\n$$"), "$1 + 1$")

    def test_inline_field_empty_display_math_is_treated_as_blank(self) -> None:
        rendered = render_answers_tex({"problem1_p_d_eq_1": "$$\n\n$$"})
        self.assertIn(r"\SetAnswer{problem1_p_d_eq_1}{}", rendered)

    def test_block_field_empty_display_math_is_treated_as_blank(self) -> None:
        rendered = render_answers_tex({"problem1_work": "$$\n\n$$"})
        self.assertIn(r"\SetAnswer{problem1_work}{}", rendered)

    def test_strict_validation_still_available(self) -> None:
        with self.assertRaisesRegex(SystemExit, "short answer slots only support inline/final answers"):
            validate_answers_content({"problem1_p_d_eq_1": "$$\n1+1\n$$"})

    def test_blank_whitespace_only_value_is_treated_as_empty(self) -> None:
        rendered = render_answers_tex({"problem1_p_d_eq_1": "\n"})
        self.assertIn(r"\SetAnswer{problem1_p_d_eq_1}{}", rendered)

    def test_empty_text_fields_render_as_multiline_triple_quotes(self) -> None:
        rendered = render_answers_toml({})
        self.assertIn("problem1_p_d_eq_1 = '''\n\n'''", rendered)


if __name__ == "__main__":
    unittest.main()

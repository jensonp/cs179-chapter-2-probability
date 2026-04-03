import unittest

from hw1_layout import TextFieldSpec, validate_layout_specs
from render_hw1_latex_answers import preserve_user_linebreaks, render_answers_tex


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

    def test_inline_field_rejects_display_math(self) -> None:
        with self.assertRaisesRegex(SystemExit, "short answer slots only support inline/final answers"):
            render_answers_tex({"problem1_p_d_eq_1": "$$\n1+1\n$$"})


if __name__ == "__main__":
    unittest.main()

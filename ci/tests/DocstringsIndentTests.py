"""Regression tests: `:examples:` / `Examples:` bodies keep their relative indentation when parsed."""

import ast
import types
import unittest

from McUtils.Docs.Docstrings import SPHINX, GOOGLE

NODE = ast.parse("def f(x): pass").body[0]

CODE = (
    "```python\n"
    "if x:\n"
    "    y = [\n"
    "        1,\n"
    "    ]\n"
    "\n"
    "print(y)\n"
    "```"
)


class SphinxExamplesIndentTests(unittest.TestCase):
    def extract(self, raw):
        return SPHINX.extract(raw, NODE)

    def test_relative_indentation_is_kept(self):
        raw = "Does a thing.\n\n:param x: a value\n:examples:\nShow it\n\n" + CODE + "\n:related: .g\n"
        data = self.extract(raw)
        self.assertEqual(data["examples"], ["Show it\n\n" + CODE])
        self.assertEqual(data["related"], [".g"])

    def test_common_indentation_is_removed(self):
        body = "\n".join(("    " + l) if l else "" for l in ("Show it\n\n" + CODE).split("\n"))
        raw = "Does a thing.\n\n:examples:\n" + body + "\n:related: .g\n"
        self.assertEqual(self.extract(raw)["examples"], ["Show it\n\n" + CODE])

    def test_text_on_the_tag_line(self):
        raw = "Summary.\n\n:examples: x = 1\n    if x:\n        y\n"
        # the tag-line text is its own line; the continuation lines are dedented together
        self.assertEqual(self.extract(raw)["examples"], ["x = 1\nif x:\n    y"])

    def test_leading_and_trailing_blank_lines_trimmed_inner_blank_lines_kept(self):
        raw = "Summary.\n\n:examples:\n\n    a = 1\n\n    b = 2\n\n:related: .g\n"
        self.assertEqual(self.extract(raw)["examples"], ["a = 1\n\nb = 2"])

    def test_first_line_may_be_more_indented_than_later_lines(self):
        raw = "Summary.\n\n:examples:\n    indented first\nplain after\n"
        self.assertEqual(self.extract(raw)["examples"], ["    indented first\nplain after"])

    def test_related_and_links_still_parse(self):
        raw = "Summary.\n\n:related: .a, .b\n:links:\n    - one\n    - two\n"
        data = self.extract(raw)
        self.assertEqual(data["related"], [".a", ".b"])
        self.assertEqual(data["links"], ["one", "two"])

    def test_render_round_trip_preserves_examples(self):
        raw = "Summary.\n\n:examples:\n" + "\n".join("    " + l if l else "" for l in CODE.split("\n")) + "\n"
        data = self.extract(raw)
        self.assertEqual(data["examples"], [CODE])
        record = types.SimpleNamespace(
            short_description=data["short_description"], details=data["details"],
            type_info=data["type_info"], examples=data["examples"],
            related=data["related"], links=data["links"],
        )
        again = self.extract(SPHINX.render(record))
        self.assertEqual(again["examples"], [CODE])


class GoogleExamplesIndentTests(unittest.TestCase):
    def test_section_indentation_is_removed_and_relative_indentation_kept(self):
        raw = (
            "Does a thing.\n\nArgs:\n    x (int): a value\n\nExamples:\n    Show it\n\n"
            + "\n".join("    " + l if l else "" for l in CODE.split("\n")) + "\n"
        )
        data = GOOGLE.extract(raw, NODE)
        # the fence must end up at column 0, otherwise Markdown treats it as an indented code block
        self.assertEqual(data["examples"], ["Show it\n\n" + CODE])

    def test_doctest_not_duplicated(self):
        raw = "Summary.\n\nExamples:\n    >>> 1 + 1\n    2\n"
        data = GOOGLE.extract(raw, NODE)
        self.assertEqual(len(data["examples"]), 1)
        self.assertIn(">>> 1 + 1", data["examples"][0])


if __name__ == "__main__":
    unittest.main()

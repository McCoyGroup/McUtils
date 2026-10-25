"""Regression tests for extracting documentation examples from test source."""

import ast
import unittest

from McUtils.Docs.DocWalker import TestExamplesFormatter


class DocsExamplesTests(unittest.TestCase):
    def test_class_base_expressions(self):
        for bases in (
            "TestCase",
            "unittest.TestCase",
            "package.testing.TestCase",
            "Generic[T]",
            "base_factory()",
            "unittest.TestCase, Mixin[T], base_factory()",
            "\n    unittest.TestCase,\n    Generic[\n        T\n    ],\n",
            "",
        ):
            with self.subTest(bases=bases):
                source = (
                    "import unittest\n"
                    "class ExampleTests(" + bases + "):\n"
                    "    marker = 42\n"
                    "    def test_example(self):\n"
                    "        self.assertTrue(True)\n"
                )
                params = TestExamplesFormatter(source).get_template_parameters()
                original_class = ast.parse(source).body[1]
                rendered_class = ast.parse(params["class_setup"]).body[0]
                self.assertEqual(rendered_class.name, original_class.name)
                self.assertEqual(
                    [ast.dump(base) for base in rendered_class.bases],
                    [ast.dump(base) for base in original_class.bases],
                )
                self.assertEqual(params["setup"], "import unittest")
                self.assertIn("    marker = 42", params["class_setup"])
                self.assertEqual(params["names"], ["example"])
                self.assertEqual(
                    params["tests"],
                    ["    def test_example(self):\n        self.assertTrue(True)"],
                )


if __name__ == "__main__":
    unittest.main()

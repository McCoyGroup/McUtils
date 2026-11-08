"""`McUtils.Docs.static_markdown`: Markdown (+ stored readouts) -> one self-contained page, and `static_doc`'s shared page assembly."""

import os as _test_os
import unittest as _test_unittest
_RUN_EXTRAS = _test_os.environ.get("MCUTILS_TEST_EXTRAS") == "1"


import os
import tempfile
import textwrap
import unittest

from McUtils.Docs import static_markdown
from McUtils.Docs.Examples import ExampleRunner, ReadoutStore


def block(id, code):
    return '<!-- readout(id={!r}) -->\n```python\n{}\n```\n\n'.format(id, textwrap.dedent(code).strip("\n"))


class StaticMarkdownTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.store = ReadoutStore(os.path.join(self._tmp.name, "readouts"))

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_plain_markdown_without_markers(self):
        html = static_markdown("# Heading\n\nSome *emphasis* and `code`.\n\n```python\nx = 1\n```\n", title="Plain")
        self.assertTrue(html.startswith("<!DOCTYPE html>"))
        self.assertIn("<title>Plain</title>", html)
        self.assertIn("<h1>Heading</h1>", html)
        self.assertIn("<em>emphasis</em>", html)
        self.assertIn('class="language-python"', html)
        self.assertIn('class="main-content"', html)

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_default_title_and_return_forms(self):
        self.assertIn("<title>Document</title>", static_markdown("text"))
        page = static_markdown("text", return_string=False)
        self.assertNotIsInstance(page, str)
        path = os.path.join(self._tmp.name, "out.html")
        self.assertEqual(static_markdown("text", out_file=path), path)
        with open(path, encoding="utf-8") as f:
            self.assertIn("<!DOCTYPE html>", f.read())

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_stored_readouts_are_inlined(self):
        text = "# Report\n\n" + block("water", "{'energy': -76.0266}") + "After.\n"
        ExampleRunner(self.store, timeout=20).run_text(text, owner="doc")
        html = static_markdown(text, readouts=self.store, strict_readouts=True, owner="doc")
        self.assertNotIn("readout(", html)
        self.assertIn("mcr-root", html)
        self.assertIn("-76.0266", html)
        self.assertNotIn("data-src=", html)       # inline, not a lazy placeholder
        self.assertNotIn("Open readout", html)

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_missing_output_is_flagged_and_strict_raises(self):
        text = block("never_run", "{'k': 1}")
        html = static_markdown(text, readouts=self.store, owner="doc")
        self.assertIn("mcr-missing", html)
        with self.assertRaises(Exception):
            static_markdown(text, readouts=self.store, strict_readouts=True, owner="doc")


if __name__ == "__main__":
    unittest.main()

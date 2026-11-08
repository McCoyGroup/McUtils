"""The ``show_code`` and ``header`` readout-marker options."""

import os as _test_os
import unittest as _test_unittest
_RUN_EXTRAS = _test_os.environ.get("MCUTILS_TEST_EXTRAS") == "1"


import os
import tempfile
import unittest

from McUtils.Docs import static_markdown
from McUtils.Docs.Examples import ExampleParser, ExampleMarkerError, ExampleRunner, ReadoutStore, ExampleEmbedder

CODE = "{'energy': -76.0267, 'n_atoms': 3}"


def page(**options):
    opts = "".join(", {}={!r}".format(k, v) for k, v in options.items())
    return "# Page\n\n<!-- readout(id='ex'{}) -->\n```python\n{}\n```\n\nAfter.\n".format(opts, CODE)


class MarkerOptionTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.store = ReadoutStore(os.path.join(self._tmp.name, "readouts"))

    def html(self, **options):
        text = page(**options)
        ExampleRunner(self.store, timeout=20).run_text(text, owner="doc")
        return static_markdown(text, readouts=self.store, strict_readouts=True, owner="doc")

    def test_options_are_parsed_and_must_be_booleans(self):
        block = ExampleParser.parse(page(show_code=False, header=False), owner="doc").blocks[0]
        self.assertIs(block.options["show_code"], False)
        self.assertIs(block.options["header"], False)
        for bad in ({"show_code": "no"}, {"header": 0}):
            with self.assertRaises(ExampleMarkerError):
                ExampleParser.parse(page(**bad), owner="doc")

    def test_keys_ignore_show_code_but_not_header(self):
        key = lambda **o: ExampleParser.parse(page(**o), owner="doc").blocks[0].key
        self.assertEqual(key(), key(show_code=False))      # hiding the code doesn't invalidate the stored output
        self.assertEqual(key(show_code=True), key(show_code=False))
        self.assertNotEqual(key(), key(header=False))      # hiding the title block changes the stored fragment

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_the_code_is_shown_by_default_and_hidden_on_request(self):
        shown = self.html()
        self.assertIn("n_atoms", shown.split("mcr-root")[0])         # the fence comes before the fragment
        hidden = self.html(show_code=False)
        self.assertNotIn(CODE, hidden)
        self.assertNotIn("<pre><code", hidden.split("<body")[1])
        self.assertIn("mcr-root", hidden)                            # the output is still there
        self.assertIn("-76.0267", hidden)
        self.assertIn("After.", hidden)

    def test_hidden_code_with_no_output_leaves_nothing(self):
        text = page(show_code=False, display="none")
        ExampleRunner(self.store, timeout=20).run_text(text, owner="doc")
        out = ExampleEmbedder(self.store, inline=True, warn=None)(text, owner="doc")
        self.assertNotIn("```", out)
        self.assertNotIn("readout(", out)
        self.assertIn("After.", out)

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_header_option(self):
        code = ("from McUtils.Readouts import Readout, ReadoutText\n"
                "Readout(ReadoutText('body text'), title='My Title', subtitle='my subtitle')")
        def render(**options):
            opts = "".join(", {}={!r}".format(k, v) for k, v in options.items())
            text = "<!-- readout(id='t'{}) -->\n```python\n{}\n```\n".format(opts, code)
            ExampleRunner(self.store, timeout=20).run_text(text, owner="doc", refresh=True)
            return static_markdown(text, readouts=self.store, strict_readouts=True, owner="doc")
        title_div, subtitle_div = '<div class="mcr-title">My Title</div>', '<div class="mcr-subtitle">my subtitle</div>'
        for html in (render(), render(header=True)):
            self.assertIn(title_div, html)
            self.assertIn(subtitle_div, html)
        hidden = render(header=False)
        self.assertNotIn(title_div, hidden)
        self.assertNotIn(subtitle_div, hidden)
        self.assertIn("body text", hidden)                            # only the title block goes


if __name__ == "__main__":
    unittest.main()

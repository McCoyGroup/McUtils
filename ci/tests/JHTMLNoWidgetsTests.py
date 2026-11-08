"""JHTML parsing (`JHTML.Markdown`, `JHTML.parse`) must not need ipywidgets unless a widget is actually used."""

import os as _test_os
import unittest as _test_unittest
_RUN_EXTRAS = _test_os.environ.get("MCUTILS_TEST_EXTRAS") == "1"


import unittest
from unittest import mock

import importlib.util

HAVE_MARKDOWN = _RUN_EXTRAS and importlib.util.find_spec("markdown") is not None


class JHTMLNoWidgetsTests(unittest.TestCase):
    def setUp(self):
        from McUtils.Jupyter.JHTML import JHTML
        from McUtils.Jupyter.JHTML.WidgetTools import JupyterAPIs
        self.JHTML = JHTML
        patcher = mock.patch.object(JupyterAPIs, "get_widgets_api", return_value=None)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_parse_without_widgets(self):
        element = self.JHTML.parse("<div><p>one</p><p>two <b>bold</b></p></div>")
        text = element.tostring()
        self.assertIn("<b>bold</b>", text)
        self.assertIn("two", text)

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    @unittest.skipUnless(HAVE_MARKDOWN, "markdown not installed")
    def test_markdown_without_widgets(self):
        element = self.JHTML.Markdown("# Title\n\nSome *emphasis* and `code`.\n\n```python\nx = 1\n```\n")
        text = element.tostring() if hasattr(element, "tostring") else str(element)
        self.assertIn("<em>emphasis</em>", text)
        self.assertIn("Title", text)

    def test_widget_tag_still_needs_widgets(self):
        # a <jwidget> reference can only be resolved with a widgets API, so that is where the error belongs
        with self.assertRaises(Exception):
            self.JHTML.parse('<div><jwidget id="not-a-real-widget"></jwidget></div>')


if __name__ == "__main__":
    unittest.main()

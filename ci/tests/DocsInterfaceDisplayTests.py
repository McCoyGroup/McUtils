"""Displaying an Apps interface (jdoc results, Button, Flex, ...) runs the ActiveHTMLWidget extension check."""

import os as _test_os
import unittest as _test_unittest
_RUN_EXTRAS = _test_os.environ.get("MCUTILS_TEST_EXTRAS") == "1"


import types
import unittest
from unittest import mock


def have_widgets():
    if not _RUN_EXTRAS:
        return False
    try:
        import importlib.util
        return all(importlib.util.find_spec(name) is not None
                   for name in ("ipywidgets", "markdown"))
    except ImportError:
        return False
    return True


@unittest.skipUnless(have_widgets(), "ipywidgets/markdown not installed")
class InterfaceDisplayTests(unittest.TestCase):
    def setUp(self):
        from McUtils.Jupyter.JHTML.WidgetTools import JupyterAPIs
        self.shown = []
        fake = types.SimpleNamespace(display=lambda *a, **k: self.shown.extend(a), HTML=lambda s: ("html", s))
        patcher = mock.patch.object(JupyterAPIs, "get_display_api", classmethod(lambda cls: fake))
        patcher.start()
        self.addCleanup(patcher.stop)

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_displaying_an_interface_runs_the_extension_check(self):
        from McUtils.Jupyter import Button
        from McUtils.Jupyter.JHTML.HTMLWidgets import HTMLWidgets
        with mock.patch.object(HTMLWidgets, "check_extension") as check:
            Button("x")._ipython_display_()
        check.assert_called_once_with()
        self.assertEqual(len(self.shown), 1)             # the interface itself is still displayed

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_a_composite_interface_displays(self):
        from McUtils.Jupyter import Button, Flex
        Flex([Button("a"), Button("b")], direction="column")._ipython_display_()
        self.assertGreaterEqual(len(self.shown), 1)


if __name__ == "__main__":
    unittest.main()

"""Telling an outdated ActiveHTMLWidget extension from a current one, and replacing it with JHTML.load."""

import json
import os
import shutil
import sys
import tempfile
import types
import unittest
from unittest import mock


def have_widgets():
    try:
        import ipywidgets, markdown  # noqa: F401
    except ImportError:
        return False
    return True


class ExtensionTestBase(unittest.TestCase):
    def setUp(self):
        from McUtils.Jupyter.JHTML.HTMLWidgets import HTMLWidgets
        self.W = HTMLWidgets
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.prefix = os.path.join(self._tmp.name, "env")
        patcher = mock.patch.object(sys, "exec_prefix", self.prefix)
        patcher.start()
        self.addCleanup(patcher.stop)
        patcher = mock.patch.object(
            HTMLWidgets, "server_environment",
            classmethod(lambda cls, refresh=False: {"python": sys.executable, "how": "test", "prefix": None,
                                                    "labextension": None, "nbextension": None}))
        patcher.start()
        self.addCleanup(patcher.stop)
        try:
            patcher = mock.patch("jupyter_core.paths.jupyter_path", lambda *a: [])
            patcher.start()
            self.addCleanup(patcher.stop)
        except ImportError:
            pass

    def dir_for(self, kind, prefix=None):
        return os.path.join(prefix or self.prefix, "share", "jupyter", kind + "s", self.W.extension_name)

    def install(self, kind, prefix=None):
        target = self.dir_for(kind, prefix)
        shutil.copytree(self.W.extension_source(kind), target)
        return target

    def make_old_lab(self, target, version="0.1.0"):
        path = os.path.join(target, "package.json")
        with open(path) as f:
            meta = json.load(f)
        meta["version"] = version
        with open(path, "w") as f:
            json.dump(meta, f)

    def make_other_build_lab(self, target):
        static = os.path.join(target, "static")
        for name in os.listdir(static):
            if name.startswith("remoteEntry.") and name.endswith(".js"):
                os.rename(os.path.join(static, name), os.path.join(static, "remoteEntry.0123456789abcdef0123.js"))


class VersionTests(unittest.TestCase):
    def test_caret_ranges(self):
        from McUtils.Jupyter.JHTML.HTMLWidgets import HTMLWidgets as W
        ok = W._version_satisfies
        self.assertTrue(ok("0.2.0", "^0.2.0"))
        self.assertTrue(ok("0.2.5", "^0.2.0"))
        self.assertFalse(ok("0.1.0", "^0.2.0"))      # the case that stops the model loading
        self.assertFalse(ok("0.3.0", "^0.2.0"))      # for 0.y.z the minor version has to match
        self.assertTrue(ok("1.4.0", "^1.2.0"))
        self.assertFalse(ok("2.0.0", "^1.2.0"))
        self.assertFalse(ok("1.1.0", "^1.2.0"))
        self.assertTrue(ok("0.2.0", "^0.2.0-dev"))
        self.assertTrue(ok("weird", "^0.2.0"))       # unreadable ranges are not a reason to complain


class StatusTests(ExtensionTestBase):
    def test_nothing_installed_is_missing(self):
        self.assertEqual(self.W.extension_state(), "missing")

    def test_a_copy_of_the_shipped_extension_is_current(self):
        self.install("labextension")
        self.install("nbextension")
        self.assertEqual(self.W.extension_state(), "current")
        (copy,) = self.W.extension_status()["labextension"]
        self.assertTrue(copy["current"])
        self.assertIsNone(copy["reason"])

    def test_an_old_version_is_outdated(self):
        self.make_old_lab(self.install("labextension"))
        self.assertEqual(self.W.extension_state(), "outdated")
        (copy,) = self.W.extension_status()["labextension"]
        self.assertIn("0.1.0", copy["reason"])
        self.assertIn("^0.2.0", copy["reason"])

    def test_the_same_version_with_another_build_is_outdated(self):
        self.make_other_build_lab(self.install("labextension"))
        self.assertEqual(self.W.extension_state(), "outdated")
        self.assertIn("different build", self.W.extension_status()["labextension"][0]["reason"])

    def test_a_changed_notebook_extension_is_outdated(self):
        target = self.install("nbextension")
        with open(os.path.join(target, "index.js"), "a") as f:
            f.write("\n// old\n")
        self.assertEqual(self.W.extension_state(), "outdated")

    def test_an_unreadable_copy_is_outdated(self):
        os.makedirs(self.dir_for("labextension"))
        self.assertEqual(self.W.extension_state(), "outdated")
        self.assertIn("can't be read", self.W.extension_status()["labextension"][0]["reason"])

    def test_either_kind_being_stale_counts(self):
        self.install("labextension")
        target = self.install("nbextension")
        with open(os.path.join(target, "index.js"), "a") as f:
            f.write("//")
        self.assertEqual(self.W.extension_state(), "outdated")

    def test_the_first_copy_in_search_order_is_the_one_that_counts(self):
        stale = self.install("labextension", os.path.join(self._tmp.name, "stale"))
        self.make_old_lab(stale)
        good = self.install("labextension", os.path.join(self._tmp.name, "good"))
        for order, expected in (((stale, good), "outdated"), ((good, stale), "current")):
            dirs = [os.path.dirname(d) for d in order]
            with mock.patch.object(self.W, "extension_locations",
                                   classmethod(lambda cls, dirs=dirs: {"labextension": dirs, "nbextension": []})):
                self.assertEqual(self.W.extension_state(), expected)

    def test_install_prefix_comes_from_the_path(self):
        self.assertEqual(self.W._install_prefix("/a/env/share/jupyter/labextensions/ActiveHTMLWidget"), "/a/env")
        self.assertIsNone(self.W._install_prefix("/somewhere/else"))


@unittest.skipUnless(have_widgets(), "ipywidgets/markdown not installed")
class NoticeAndCheckTests(ExtensionTestBase):
    def setUp(self):
        super().setUp()
        from McUtils.Jupyter.JHTML.WidgetTools import JupyterAPIs
        self.shown = []
        fake = types.SimpleNamespace(display=lambda *a, **k: self.shown.extend(a))
        patcher = mock.patch.object(JupyterAPIs, "get_display_api", classmethod(lambda cls: fake))
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_an_outdated_copy_gets_a_reinstall_notice_naming_it(self):
        target = self.install("labextension")
        self.make_old_lab(target)
        self.assertIs(self.W.check_extension(force=True), False)
        (notice,) = self.shown
        text = notice.tostring()
        self.assertIn("out of date", text)
        self.assertIn(target, text)
        self.assertIn("0.1.0", text)
        self.assertIn("<pre><code>", text)
        self.assertIn("JHTML.load(exec_prefix={!r}, overwrite=True)".format(self.prefix).replace("'", "&#39;"), text.replace("'", "&#39;"))
        self.assertIn("Hard-reload", text)

    def test_a_current_copy_shows_nothing(self):
        self.install("labextension")
        self.assertIs(self.W.check_extension(force=True), True)
        self.assertEqual(self.shown, [])

    def test_a_missing_copy_still_gets_the_install_notice(self):
        self.assertIs(self.W.check_extension(force=True), False)
        self.assertIn("not installed", self.shown[0].tostring())


@unittest.skipUnless(have_widgets(), "ipywidgets/markdown not installed")
class LoadTests(ExtensionTestBase):
    def setUp(self):
        super().setUp()
        self.shown = []
        patcher = mock.patch("IPython.core.display.display", lambda *a, **k: self.shown.extend(a))
        patcher.start()
        self.addCleanup(patcher.stop)

    def text(self):
        return " ".join(x.tostring() if hasattr(x, "tostring") else getattr(x, "data", str(x)) for x in self.shown)

    def test_load_installs_both_kinds_when_nothing_is_there(self):
        self.W.load(exec_prefix=self.prefix)
        self.assertEqual(self.W.extension_state(), "current")
        self.assertTrue(os.path.isdir(self.dir_for("labextension")))
        self.assertTrue(os.path.isdir(self.dir_for("nbextension")))

    def test_load_replaces_an_outdated_copy_without_overwrite(self):
        target = self.install("labextension")
        self.install("nbextension")
        self.make_old_lab(target)
        self.W.load(exec_prefix=self.prefix)
        self.assertEqual(self.W.extension_state(), "current")
        self.assertIn("Replaced the outdated labextension", self.text())
        self.assertIn("0.1.0", self.text())

    def test_load_leaves_a_current_copy_alone(self):
        target = self.install("labextension")
        self.install("nbextension")
        marker = os.path.join(target, "marker.txt")
        open(marker, "w").close()
        self.W.load(exec_prefix=self.prefix)
        self.assertTrue(os.path.exists(marker))             # not replaced
        self.assertIn("already installed and current", self.text())
        self.W.load(exec_prefix=self.prefix, overwrite=True)
        self.assertFalse(os.path.exists(marker))            # replaced on request

    def test_load_warns_about_an_outdated_copy_elsewhere_that_would_still_be_used(self):
        stale = self.install("labextension", os.path.join(self._tmp.name, "other"))
        self.make_old_lab(stale)
        both = [os.path.dirname(stale), os.path.dirname(self.dir_for("labextension"))]
        with mock.patch.object(self.W, "extension_locations",
                               classmethod(lambda cls: {"labextension": both, "nbextension": []})):
            self.W.load(exec_prefix=self.prefix)
        self.assertIn("still use an outdated copy", self.text())
        self.assertIn(stale, self.text())


if __name__ == "__main__":
    unittest.main()

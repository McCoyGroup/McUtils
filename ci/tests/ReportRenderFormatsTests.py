"""`ReportRenderer.render` writes each requested format independently, and HTML needs no network (vendored finx)."""

import os as _test_os
import unittest as _test_unittest
_RUN_EXTRAS = _test_os.environ.get("MCUTILS_TEST_EXTRAS") == "1"


import os
import tempfile
import unittest
import urllib.request
from unittest import mock

import McUtils.Readouts.Reports.Render as R
from McUtils.Readouts.Reports import ReportDocument, ReportRenderer, ReportRenderError, report_toolset

from ReportFixtures import ToyResult, toy_catalog


def build(cat):
    doc = ReportDocument("Toy Report", cat)
    doc.add_heading("Structure")
    doc.add_readout("water", include=["summary"], caption="The energy of water.")
    return doc


def _offline(*args, **kwargs):
    raise OSError("[Errno -3] Temporary failure in name resolution")


@_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
class RenderFormatsTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.out = os.path.join(self._tmp.name, "out")
        self.cat = toy_catalog(water=ToyResult("water"))
        self.doc = build(self.cat)

    def exists(self, name):
        return os.path.exists(os.path.join(self.out, name))

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_offline_render_writes_everything(self):
        with mock.patch.object(urllib.request, "urlopen", _offline):
            res = ReportRenderer(self.cat).render(self.doc, self.out)
        self.assertTrue(res.ok, res.problems)
        self.assertEqual(set(res.paths), {"md", "html", "pptx"})
        self.assertEqual(res.failed, {})
        with open(res.paths["html"], encoding="utf-8") as f:
            self.assertIn(".main-content", f.read())

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_link_mode_is_passed_through(self):
        res = ReportRenderer(self.cat, finx_assets="link").render(self.doc, self.out, formats=("html",))
        with open(res.paths["html"], encoding="utf-8") as f:
            self.assertIn("cdn.jsdelivr.net/gh/McCoyGroup/finx@", f.read())

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_html_failure_still_writes_pptx_non_strict(self):
        with mock.patch.object(R.ReportRenderer, "render_html", side_effect=OSError("network is unreachable")):
            res = ReportRenderer(self.cat, strict=False).render(self.doc, self.out)
        self.assertFalse(res.ok)
        self.assertEqual(set(res.paths), {"md", "pptx"})
        self.assertEqual(res.failed, {"html": "render_failed"})
        self.assertIn("network is unreachable", res.problems[0])
        self.assertTrue(self.exists("report.pptx"))

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_html_failure_strict_raises_after_the_other_formats(self):
        with mock.patch.object(R.ReportRenderer, "render_html", side_effect=OSError("network is unreachable")):
            with self.assertRaises(ReportRenderError) as cm:
                ReportRenderer(self.cat).render(self.doc, self.out)
        self.assertTrue(self.exists("report.pptx"))
        self.assertTrue(self.exists("report.md"))
        self.assertEqual(cm.exception.code, "render_failed")
        self.assertEqual(set(cm.exception.result.paths), {"md", "pptx"})
        d = cm.exception.to_dict()
        self.assertEqual(set(d["written"]), {"md", "pptx"})
        self.assertEqual(d["failed"], {"html": "render_failed"})

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_pptx_failure_still_writes_html(self):
        with mock.patch.object(ReportDocument, "to_readout", side_effect=RuntimeError("deck broke")):
            res = ReportRenderer(self.cat, strict=False).render(self.doc, self.out)
            self.assertEqual(set(res.paths), {"md", "html"})
            self.assertEqual(res.failed, {"pptx": "render_failed"})
            with self.assertRaises(ReportRenderError) as cm:
                ReportRenderer(self.cat).render(self.doc, self.out)
        self.assertIn("html", cm.exception.result.paths)
        self.assertIn("deck broke", str(cm.exception))

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_failed_readout_blocks_keep_strict_html_unwritten_but_pptx_is_attempted(self):
        cat2 = toy_catalog(water=ToyResult("water", energy=-70.5))
        stale = ReportDocument.from_markdown(self.doc.to_markdown(), cat2)       # digest no longer matches
        with self.assertRaises(ReportRenderError) as cm:
            ReportRenderer(cat2).render(stale, self.out, formats=("html", "pptx"))
        self.assertFalse(self.exists("report.html"))
        self.assertEqual(cm.exception.result.failed.get("html"), "render_failed")
        self.assertEqual(cm.exception.result.statuses["r1"], "error")

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_unknown_format(self):
        with self.assertRaises(ValueError):
            ReportRenderer(self.cat).render(self.doc, self.out, formats=("pdf",))

    def test_render_tool_reports_what_was_written(self):
        tools = report_toolset(self.doc, self.cat, renderer=ReportRenderer(self.cat), out_dir=self.out)
        with mock.patch.object(R.ReportRenderer, "render_html", side_effect=OSError("network is unreachable")):
            r = tools.call("render", {})
        self.assertFalse(r.ok)
        self.assertEqual(r.error["code"], "render_failed")
        self.assertEqual(set(r.error["written"]), {"md", "pptx"})
        self.assertEqual(r.error["failed"], {"html": "render_failed"})


if __name__ == "__main__":
    unittest.main()

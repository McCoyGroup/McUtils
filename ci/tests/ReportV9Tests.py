"""
V9: a long numeric column is summarised (min, max, last as placeholders) in `peek`, `values` and the receipts, `values`
lists it in pages, selectors refuse a column the evidence cut short, and a section that holds only arrays that are not
displayed shows a one-line stub in HTML and PowerPoint (and a warning) instead of nothing.
"""
import numpy as np
import unittest

from McUtils.Readouts import (ReadoutAdapter, ReadoutArray, ReadoutTable, ReadoutText, ReadoutSection, Readout,
                              ArrayData, Column, TabularData, readout_section, register_readout)
from McUtils.Readouts.Builders import line_chart
from McUtils.Readouts.Reports import ReportDocument, report_toolset, fill_text
from McUtils.Readouts.Reports.Grounding import evidence_items
from McUtils.Readouts.Reports import Advice as adv
from ReportFillTests import ok
from ReportFixtures import toy_catalog, ToyResult


class Series(ToyResult):
    """A toy with a 40-point series (a sine), a section of only a hidden array and a line plot of the series."""
    N = 40

    def __init__(self, name="series"):
        super().__init__(name)
        self.t = np.linspace(0.0, 4.0, self.N)
        self.y = np.round(np.sin(self.t) * 2.5, 4)


@register_readout(Series)
class SeriesReadout(ReadoutAdapter):
    readout_id = "series"

    @readout_section(description="The series.")
    def readout_series(self, ctx):
        return ReadoutTable(TabularData([Column("time", self.obj.t, unit="ps"),
                                         Column("signal", self.obj.y, unit="eV")], title="Series"))

    @readout_section(default=False, description="Displacements, export only.")
    def readout_displacements(self, ctx):
        return ReadoutSection([ReadoutArray(ArrayData("disp", np.arange(24.0).reshape(2, 4, 3), label="Displacements"),
                                            id="disp")], title="Displacements", id="displacements")

    @readout_section(default=False, description="A line plot of the series.")
    def readout_plot(self, ctx):
        return line_chart(self.obj.t, self.obj.y, x_label="Time", y_label="Signal", x_unit="ps", y_unit="eV",
                          caption="Signal against time", id="plot")


def make(**kw):
    cat = toy_catalog(sig=Series())
    doc = ReportDocument("V9", cat)
    tools = report_toolset(doc, cat, **kw)
    return doc, cat, tools


class SummaryTests(unittest.TestCase):
    def setUp(self):
        self.doc, self.cat, self.tools = make()
        self.bid = ok(self.tools.call("add_readout", {"handle": "sig", "include": ["series"]}))["block_id"]

    def test_receipt_line_has_extremes_and_last(self):
        rec = ok(self.tools.call("add_readout", {"handle": "sig", "include": ["series"]}))
        line = [ln for ln in rec["placeholders"] if "signal" in ln][0]
        for which in ("min", "max", "last"):
            self.assertIn(f"[{which}]", line)
        self.assertIn("(row ", line)

    def test_short_columns_are_unchanged(self):
        cat = toy_catalog(w=ToyResult("w"))
        doc = ReportDocument("S", cat)
        tools = report_toolset(doc, cat)
        rec = ok(tools.call("add_readout", {"handle": "w", "include": ["frequencies"]}))
        self.assertTrue(all("[min]" not in ln for ln in rec["placeholders"]), rec["placeholders"])

    def test_summary_values_are_the_data(self):
        y = np.round(np.sin(np.linspace(0, 4, 40)) * 2.5, 4)
        items = self.doc.evidence([self.bid])
        st = adv.column_stats(items, self.bid, "signal")
        by = {s["which"]: s for s in st["stats"]}
        self.assertEqual(by["max"]["row"], int(np.argmax(y)) + 1)
        self.assertEqual(by["min"]["row"], int(np.argmin(y)) + 1)
        self.assertEqual(by["last"]["row"], 40)
        self.assertIn(f"{y.max():.4f}", by["max"]["value"])

    def test_selector_placeholders_in_the_summary_resolve(self):
        items = self.doc.evidence([self.bid])
        for s in adv.column_stats(items, self.bid, "signal")["stats"]:
            text, fills = fill_text(s["use"], items)[:2]
            self.assertEqual(text, s["value"])

    def test_times_column_is_summarised_too(self):
        self.assertIsNotNone(adv.column_stats(self.doc.evidence([self.bid]), self.bid, "time"))

    def test_peek_shows_the_summary_at_every_level(self):
        for level in (1, 2, 3):
            doc, cat, tools = make(context_level=level)
            out = ok(tools.call("peek", {"handle": "sig", "section": "series"}))
            text = out if isinstance(out, str) else str(out)
            self.assertIn("[max]", text, level)

    def test_values_summary_and_paging(self):
        out = ok(self.tools.call("values", {"block_id": self.bid, "column": "signal", "limit": 15}))
        self.assertEqual(out["n_rows"], 40)
        self.assertEqual(len(out["rows"]), 15)
        self.assertEqual({s["which"] for s in out["summary"]}, {"min", "max", "last"})
        self.assertIn("start=16", out["next"])
        page = ok(self.tools.call("values", {"block_id": self.bid, "column": "signal", "start": 16, "limit": 15}))
        self.assertEqual([r["row"] for r in page["rows"]][:2], [16, 17])
        self.assertIn("start=31", page["next"])
        last = ok(self.tools.call("values", {"block_id": self.bid, "column": "signal", "start": 31, "limit": 15}))
        self.assertEqual(len(last["rows"]), 10)
        self.assertNotIn("next", last)

    def test_values_without_a_column_carries_the_summary(self):
        out = ok(self.tools.call("values", {"block_id": self.bid}))
        self.assertTrue(any("[max]" in ln for ln in out["placeholders"]))


class TruncationTests(unittest.TestCase):
    def setUp(self):
        self.doc, self.cat, self.tools = make()
        self.bid = ok(self.tools.call("add_readout", {"handle": "sig", "include": ["series"]}))["block_id"]
        ro = self.cat.get("sig").readout(include=["series"])
        self.items = evidence_items([], [(self.bid, ro)], cap=25)      # 40-row columns: the first keeps 25, the second 0

    def test_the_cut_is_recorded(self):
        self.assertTrue(self.items.truncated)
        self.assertTrue(all(k[0] == self.bid for k in self.items.truncated))

    def test_uncut_evidence_records_nothing(self):
        self.assertEqual(self.doc.evidence([self.bid]).truncated, {})

    def test_min_max_last_are_refused_on_a_cut_column(self):
        for how in ("min", "max", "last"):
            with self.assertRaises(Exception) as cm:
                fill_text("{" + f"{self.bid}.time[{how}]" + "}", self.items)
            self.assertIn("not available", str(cm.exception))

    def test_first_and_rows_inside_the_cut_still_work(self):
        text = fill_text("{" + f"{self.bid}.time[first]" + "}", self.items)[0]
        self.assertTrue(text)
        self.assertTrue(fill_text("{" + f"{self.bid}.time[3]" + "}", self.items)[0])

    def test_row_past_the_cut_says_the_data_was_cut(self):
        with self.assertRaises(Exception) as cm:
            fill_text("{" + f"{self.bid}.time[30]" + "}", self.items)
        self.assertIn("loaded", str(cm.exception))

    def test_summary_says_it_is_unavailable(self):
        st = adv.column_stats(self.items, self.bid, "time")
        self.assertEqual(st["stats"], [])
        self.assertIsNotNone(st["truncated"])
        line = [c["line"] for c in adv.column_summary(self.items, self.bid)][0]
        self.assertIn("not available", line)


STUB = {"stub_hidden": True}


class StubTests(unittest.TestCase):
    def setUp(self):
        self.cat = toy_catalog(sig=Series())
        self.ro = self.cat.get("sig").readout(include=["displacements"])

    def test_html_shows_a_stub_when_asked(self):
        html = self.ro.to_html_fragment(style=STUB).html
        self.assertIn("Not displayed (data only)", html)
        self.assertIn("Displacements", html)
        self.assertIn("shape (2, 4, 3)", html)

    def test_plain_readouts_keep_export_only_arrays_out_of_sight(self):
        self.assertNotIn("Not displayed", self.ro.to_html_fragment().html)

    def test_text_names_the_array(self):
        self.assertIn("array of shape (2, 4, 3)", self.ro.to_text())

    def test_pptx_shows_a_stub(self):
        import os
        import tempfile
        import zipfile
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "x.pptx")
            self.ro.to_pptx(path, style=STUB)
            with zipfile.ZipFile(path) as z:
                xml = " ".join(z.read(n).decode("utf-8", "ignore") for n in z.namelist() if n.startswith("ppt/slides/slide"))
        self.assertIn("Not displayed (data only)", xml)

    def test_a_section_with_visible_content_has_no_stub(self):
        ro = self.cat.get("sig").readout(include=["series"])
        self.assertNotIn("Not displayed", ro.to_html_fragment(style=STUB).html)

    def test_a_visible_array_next_to_a_hidden_one_is_not_stubbed(self):
        sec = ReadoutSection([ReadoutArray(ArrayData("a", np.arange(6.0), label="A"), display=True, id="a"),
                              ReadoutArray(ArrayData("b", np.arange(6.0), label="B"), id="b")], title="Mixed", id="mixed")
        html = Readout([sec], title="t").to_html_fragment(style=STUB).html
        self.assertNotIn("Not displayed", html)

    def test_plot_text_describes_what_is_plotted(self):
        text = self.cat.get("sig").readout(include=["plot"]).to_text()
        self.assertIn("40 points of", text)
        self.assertIn("Signal against time", text)

    def test_stub_warning_in_compile_and_receipt(self):
        doc = ReportDocument("V9", self.cat)
        tools = report_toolset(doc, self.cat)
        rec = ok(tools.call("add_readout", {"handle": "sig", "include": ["displacements"]}))
        self.assertTrue(any("data only" in n for n in rec.get("notes", [])), rec)
        comp = ok(tools.call("compile", {}))
        self.assertIn("not_displayed", [w["code"] for w in comp["warnings"]])

    def test_no_warning_for_a_shown_section(self):
        doc = ReportDocument("V9", self.cat)
        tools = report_toolset(doc, self.cat)
        ok(tools.call("add_readout", {"handle": "sig", "include": ["series"]}))
        comp = ok(tools.call("compile", {}))
        self.assertNotIn("not_displayed", [w["code"] for w in comp["warnings"]])

    def test_report_style_turns_the_stub_on(self):
        from McUtils.Readouts.Reports.Render import report_style
        from McUtils.Readouts.Styles import ReadoutTheme
        self.assertTrue(report_style(None)["stub_hidden"])
        self.assertTrue(report_style("default")["stub_hidden"])
        self.assertEqual(report_style({"stub_hidden": False})["stub_hidden"], False)
        self.assertTrue(ReadoutTheme.resolve(report_style({"sizes": {}})).get("stub_hidden"))
        self.assertTrue(report_style(ReadoutTheme.resolve("default")).get("stub_hidden"))

    def test_rendered_report_shows_the_stub(self):
        import os
        import tempfile
        from McUtils.Readouts.Reports import ReportRenderer
        doc = ReportDocument("V9", self.cat)
        tools = report_toolset(doc, self.cat)
        ok(tools.call("add_heading", {"text": "Displacements", "level": 2}))
        ok(tools.call("add_readout", {"handle": "sig", "include": ["displacements"]}))
        with tempfile.TemporaryDirectory() as d:
            try:
                res = ReportRenderer(self.cat, strict=False).render(doc, d, formats=("html", "pptx"))
            except ImportError:
                self.skipTest("an optional package for the HTML report is missing")
            if "html" in res.paths:
                self.assertIn("Not displayed (data only)", open(res.paths["html"], encoding="utf-8").read())
            self.assertIn("pptx", res.paths, res.problems)

    def test_report_html_and_data_export_both_keep_the_array(self):
        flat = self.ro.to_flat_data()[0]
        self.assertTrue(any(np.asarray(v).size == 24 for v in flat.values()))


if __name__ == "__main__":
    unittest.main()

"""
V10: a catalog entry's ``readout_options`` (section options a report block cannot carry) and the `level_chart` ladder.
"""
import numpy as np
import unittest

from McUtils.Readouts import (ReadoutAdapter, ReadoutTable, TabularData, Column, readout_section, register_readout,
                              to_readout)
from McUtils.Readouts.Builders import level_chart
from McUtils.Readouts.Reports import ReportDocument, SourceCatalog, report_toolset, fill_text
from McUtils.Readouts.Reports.Sources import ConfiguredSource, merge_readout_options, source_digest
from ReportFillTests import ok


class Curve:
    """A source whose section ``series`` has the option ``n`` (the number of points)."""


@register_readout(Curve)
class CurveReadout(ReadoutAdapter):
    readout_id = "curve"

    @readout_section("series", title="Series", description="A sine curve of n points.")
    def readout_series(self, ctx, n=20, amplitude=2.0):
        t = np.linspace(0.0, 6.0, int(n))
        return ReadoutTable(TabularData([Column("t", t, unit="ps"), Column("y", amplitude * np.sin(t))],
                                        name="series", title="Series"))

    @readout_section("ladder", title="Levels", default=False, description="A level ladder.")
    def readout_ladder(self, ctx):
        return level_chart([100.0, 250.0, 420.0], y_label="Energy", y_unit="Wavenumbers", value_name="energy",
                           caption="Levels", id="ladder")


def cat(**opts):
    c = SourceCatalog()
    c.add("curve", Curve(), readout_options=opts or None)
    return c


def rows(ro, name="y"):
    d = ro.to_flat_data()[0]
    return np.asarray(d[[k for k in d if k.endswith("/" + name)][0]])


class MergeTests(unittest.TestCase):
    def test_section_options_merge_and_the_call_wins(self):
        out = merge_readout_options({"series": {"n": 30, "amplitude": 1.0}}, {"series": {"n": 5}, "include": ["series"]})
        self.assertEqual(out, {"series": {"n": 5, "amplitude": 1.0}, "include": ["series"]})

    def test_call_options_are_not_merged(self):
        self.assertEqual(merge_readout_options({"include": ["a"]}, {"include": ["b"]}), {"include": ["b"]})

    def test_no_defaults(self):
        self.assertEqual(merge_readout_options(None, {"x": 1}), {"x": 1})


class ReadoutOptionsTests(unittest.TestCase):
    def test_options_shape_the_sources_readout(self):
        c = cat(series={"n": 45})
        self.assertEqual(len(rows(c.get("curve").readout(include=["series"]))), 45)

    def test_without_options_the_default(self):
        self.assertEqual(len(rows(cat().get("curve").readout(include=["series"]))), 20)

    def test_options_change_the_digest(self):
        self.assertNotEqual(cat(series={"n": 45}).get("curve").digest, cat().get("curve").digest)
        self.assertEqual(cat(series={"n": 45}).get("curve").digest, cat(series={"n": 45}).get("curve").digest)
        self.assertNotEqual(source_digest(Curve(), {"series": {"n": 3}}), source_digest(Curve()))

    def test_describe_states_them(self):
        d = cat(series={"n": 45}).describe("curve")
        self.assertEqual(d["readout_options"], {"series": {"n": 45}})
        self.assertNotIn("readout_options", cat().describe("curve"))

    def test_load_returns_the_object_or_a_configured_wrapper(self):
        plain = cat()
        self.assertIsInstance(plain.load("curve"), Curve)
        wrapped = cat(series={"n": 45}).load("curve")
        self.assertIsInstance(wrapped, ConfiguredSource)
        self.assertEqual(len(rows(wrapped.to_readout(include=["series"]))), 45)
        self.assertEqual(len(rows(wrapped.to_readout(include=["series"], series={"n": 7}))), 7)

    def test_the_docs_path_uses_them(self):
        from McUtils.Docs.Examples import value_to_readout
        c = cat(series={"n": 45})
        ro = value_to_readout(c.load("curve"), {"include": ["series"]})
        self.assertEqual(len(rows(ro)), 45)

    def test_tools_see_them(self):
        c = cat(series={"n": 45})
        doc = ReportDocument("t", c)
        tools = report_toolset(doc, c)
        rec = ok(tools.call("add_readout", {"handle": "curve", "include": ["series"]}))
        self.assertTrue(any("rows 1-45" in ln for ln in rec["placeholders"]), rec["placeholders"])
        self.assertTrue(any("[max]" in ln for ln in rec["placeholders"]))

    def test_the_section_kind_uses_them(self):
        self.assertEqual(cat(series={"n": 45}).get("curve").section_kind("series"), "table")

    def test_a_block_over_the_evidence_cap_refuses_extremes(self):
        c = cat(series={"n": 25000})
        doc = ReportDocument("t", c)
        tools = report_toolset(doc, c)
        r = ok(tools.call("add_readout", {"handle": "curve", "include": ["series"]}))["block_id"]
        res = tools.call("add_text", {"text": "The peak is {%s.y[max]}." % r})
        self.assertFalse(res.ok)
        self.assertIn("not available", str(res.error))
        res = tools.call("add_text", {"text": "It starts at {%s.y[first]}." % r})
        self.assertTrue(res.ok, res.error)

    def test_unknown_section_options_are_an_error_not_silently_dropped(self):
        c = SourceCatalog()
        with self.assertRaises(Exception):
            c.add("bad", Curve(), readout_options={"nosuch": {"n": 3}})


class LevelChartTests(unittest.TestCase):
    def test_data_is_the_levels(self):
        ro = to_readout(Curve(), include=["ladder"])
        np.testing.assert_allclose(rows(ro, "energy"), [100.0, 250.0, 420.0])
        np.testing.assert_allclose(rows(ro, "level"), [1, 2, 3])

    def test_text_and_html(self):
        ro = to_readout(Curve(), include=["ladder"])
        self.assertIn("3 points of", ro.to_text())
        self.assertIn("<svg", ro.to_html_fragment().html)

    def test_labels_add_a_column(self):
        node = level_chart([1.0, 2.0], labels=["a", "b"], value_name="e")
        names = [c.name for c in node.data.columns]
        self.assertEqual(names, ["level", "label", "e"])

    def test_peek_lists_the_placeholders(self):
        c = cat()
        doc = ReportDocument("t", c)
        tools = report_toolset(doc, c)
        r = ok(tools.call("add_readout", {"handle": "curve", "include": ["ladder"]}))["block_id"]
        ok(tools.call("add_text", {"text": "The top level is {%s.energy[max]}." % r}))
        self.assertIn("420", doc.get(doc.blocks[-1].id).text)


if __name__ == "__main__":
    unittest.main()

"""Readout trees, section selection, units, renderers and poster rasterizers."""
import io
import json
import os
import sys
import tempfile
import unittest
import warnings
import zipfile

import numpy as np

from McUtils.Jupyter import (
    Readout, ReadoutSection, ReadoutFields, ReadoutTable, ReadoutText, ReadoutScene, ReadoutGallery,
    ReadoutArray, ReadoutAdapter, readout_section, ReadoutSectionUnavailable, ReadoutUnits, ReadoutTheme,
    Field, FieldSet, Column, TabularData, ArrayData, SceneView, PosterRequest, MeshSceneSource,
    ReadoutRasterizer, SoftwareRasterizer, PlaceholderRasterizer, RasterizerChain,
)
from McUtils.Plots.PowerPoint import PowerPointPresentation, PresentationML


class _Record:
    def __init__(self, bond=1.8897261246, angle=np.pi / 2, broken=False):
        self.bond, self.angle, self.broken = bond, angle, broken


class _RecordReadout(ReadoutAdapter):
    readout_id = "record"
    readout_title = "Record"

    @readout_section("summary", title="Summary")
    def readout_summary(self, ctx, label="test"):
        return ReadoutFields(FieldSet([
            ctx.field("label", label),
            ctx.field("bond", self.obj.bond, quantity="length", unit="BohrRadius", label="Bond"),
        ], name="summary"))

    @readout_section("geometry", title="Geometry")
    def readout_geometry(self, ctx):
        return ReadoutTable(TabularData([
            Column("name", np.array(["r", "a"])),
            ctx.column("bond", np.array([self.obj.bond, 2 * self.obj.bond]), quantity="length", unit="BohrRadius"),
        ], name="table"))

    @readout_section("hidden", title="Hidden", default=False)
    def readout_hidden(self, ctx):
        return ReadoutArray(ArrayData("matrix", np.eye(3)))

    @readout_section("never", title="Never", default=False, available=lambda self: (False, "no data"))
    def readout_never(self, ctx):
        return ReadoutText("unreachable")

    @readout_section("fragile", title="Fragile", default=False)
    def readout_fragile(self, ctx):
        if self.obj.broken:
            raise RuntimeError("boom")
        return ReadoutText("fine")

    @readout_section("nested", title="Nested", default=False)
    def readout_nested(self, ctx, include=None, exclude=None, **opts):
        sub = _RecordReadout(self.obj)
        return ReadoutSection(*sub.get_readout_sections(include=include or ["summary"], exclude=exclude,
                                                        ctx=ctx, **opts))


def _triangle_source():
    from McUtils.Plots.Backends import Mesh3DFigure, MeshInformation
    fig = Mesh3DFigure()
    fig.create_axes()
    fig.axes[0].meshes = [MeshInformation(
        np.array([[0, -1, -1], [0, 1, -1], [0, 0, 1.]]), np.array([[0, 1, 2]]),
        material={"base_color": [1, 0, 0, 1]})]
    return MeshSceneSource(fig)


class ReadoutInterfaceTests(unittest.TestCase):
    def test_default_sections_and_registry(self):
        ro = _RecordReadout(_Record()).to_readout()
        self.assertEqual([c.id for c in ro.children], ["summary", "geometry"])
        names = [r["name"] for r in _RecordReadout.list_readout_sections(_Record())]
        self.assertEqual(names, ["summary", "geometry", "hidden", "never", "fragile", "nested"])

    def test_include_exclude_options_and_errors(self):
        iface = _RecordReadout(_Record())
        ro = iface.to_readout(include=["geometry", "summary"], summary={"label": "x"})
        self.assertEqual([c.id for c in ro.children], ["geometry", "summary"])
        self.assertEqual(ro["summary/summary"].data["label"].value, "x")
        ro = iface.to_readout(include="all", exclude=["hidden", "never", "fragile", "nested"])
        self.assertEqual([c.id for c in ro.children], ["summary", "geometry"])
        with self.assertRaises(ValueError):
            iface.to_readout(include=["nope"])
        with self.assertRaises(TypeError):
            iface.to_readout(summary={"bad_option": 1})

    def test_dotted_include_reaches_nested_sections(self):
        ro = _RecordReadout(_Record()).to_readout(include=["nested.geometry"])
        self.assertEqual([c.id for c in ro["nested"].children], ["geometry"])

    def test_unavailable_and_failed_sections(self):
        iface = _RecordReadout(_Record(broken=True))
        ro = iface.to_readout(include=["never"])
        self.assertEqual(ro["never"].meta["unavailable"], "no data")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            ro = iface.to_readout(include=["fragile"])
        self.assertIn("boom", ro["fragile"].meta["error"])
        with self.assertRaises(Exception):
            iface.to_readout(include=["never"], strict=True)
        # unavailable sections that weren't asked for are skipped silently
        self.assertNotIn("never", [c.id for c in iface.to_readout(include="all", exclude=["fragile"]).children])


class ReadoutUnitsTests(unittest.TestCase):
    def test_values_are_converted_once_and_exports_match_display(self):
        ro = _RecordReadout(_Record(bond=1.8897261246)).to_readout()
        field = ro["summary/summary"].data["bond"]
        self.assertAlmostEqual(field.value, 1.0, places=6)
        self.assertEqual((field.unit, field.source_unit), ("Angstroms", "BohrRadius"))
        flat, meta = ro.to_flat_data()
        self.assertAlmostEqual(float(flat["record/summary/bond"]), 1.0, places=6)
        np.testing.assert_allclose(flat["record/geometry/bond"], [1.0, 2.0], atol=1e-6)
        self.assertEqual(meta["record/geometry/bond"]["unit"], "Angstroms")
        self.assertIn("1.00000 Å", ro.to_text())
        html = ro.to_html()
        self.assertIn("2.00000", html)
        ro = _RecordReadout(_Record()).to_readout(units={"length": "BohrRadius"})
        self.assertAlmostEqual(ro["summary/summary"].data["bond"].value, 1.8897261246)

    def test_angle_conversion_falls_back_to_local_factors(self):
        vals, unit = ReadoutUnits().convert(np.pi, "angle", "Radians")
        self.assertAlmostEqual(vals, 180.0)
        self.assertEqual(unit, "Degrees")


class ReadoutExportTests(unittest.TestCase):
    def setUp(self):
        self.readout = _RecordReadout(_Record()).to_readout(include=["summary", "geometry", "hidden"])

    def test_npz_json_pandas(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = os.path.join(tmp, "r.npz")
            self.readout.to_npz(f)
            data = np.load(f, allow_pickle=False)
            # single-child levels are collapsed: geometry/table/bond -> geometry/bond
            self.assertIn("record/geometry/bond", data.files)
            self.assertIn("record/hidden", data.files)
            meta = json.loads(str(data["__meta__"]))
            self.assertEqual(meta["record/geometry/bond"]["unit"], "Angstroms")
        doc = json.loads(self.readout.to_json())
        self.assertEqual(doc["data"]["summary"]["label"], "test")
        frames = self.readout.to_pandas()
        self.assertEqual(frames["record/geometry"].attrs["units"]["bond"], "Angstroms")

    def test_export_only_arrays_are_not_displayed(self):
        html = self.readout.to_html()
        self.assertNotIn("Hidden", html)
        pres = self.readout.to_powerpoint(title_slide=False)
        titles = [p.text for s in pres.slides for p in s.children if hasattr(p, "text")]
        self.assertFalse(any("Hidden" in t for t in titles))

    def test_html_has_real_table_structure(self):
        html = self.readout.to_html()
        self.assertIn("<thead><tr><th", html)
        self.assertIn("<tbody><tr><td", html)

    def test_powerpoint_tables_and_packing(self):
        pres = self.readout.to_powerpoint()
        self.assertEqual(len(pres.slides), 2)  # title slide + both small sections packed together
        data = pres.to_bytes()
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            slide = z.read("ppt/slides/slide2.xml").decode()
            self.assertIn("<a:tbl>", slide)
            self.assertIn("Summary  ·  Geometry", slide)
            # relationship parts use the default namespace (LibreOffice rejects prefixed ones)
            self.assertTrue(z.read("_rels/.rels").decode().split("?>", 1)[1].lstrip().startswith("<Relationships "))
        PresentationML.from_file(io.BytesIO(data))

    def test_long_tables_are_paginated_with_repeated_headers(self):
        rows = 60
        table = ReadoutTable(TabularData([Column("i", np.arange(rows)), Column("v", np.linspace(0, 1, rows))]))
        ro = Readout(ReadoutSection(table, id="big", title="Big"), title="Big")
        pres = ro.to_powerpoint(title_slide=False)
        self.assertGreater(len(pres.slides), 2)
        from McUtils.Plots.PowerPoint import PresentationMLTable
        tables = [p for s in pres.slides for p in s.children if isinstance(p, PresentationMLTable)]
        self.assertEqual(sum(len(t.rows) - 1 for t in tables), rows)
        self.assertTrue(all(t.rows[0][0] == "i" for t in tables))


class SceneTests(unittest.TestCase):
    def test_fit_looks_along_thinnest_axis(self):
        verts = np.array([[0, -2, -1], [0, 2, 1], [.1, 0, 0]])
        view = SceneView.fit(verts, aspect=4 / 3)
        np.testing.assert_allclose(view.forward, [-1, 0, 0])
        np.testing.assert_allclose(view.up, [0, 0, 1])
        axis_angle = view.x3d_viewpoint()["orientation"]
        np.testing.assert_allclose(axis_angle[:3], np.ones(3) / np.sqrt(3), atol=1e-6)
        self.assertAlmostEqual(axis_angle[3], 2 * np.pi / 3)

    def test_software_and_placeholder_posters(self):
        src = _triangle_source()
        view = SceneView.fit(src.vertices(), aspect=2)
        req = PosterRequest(src, view, 200, 100)
        png = SoftwareRasterizer(validate=True).rasterize(req)
        self.assertTrue(png.startswith(b"\x89PNG"))
        blank = PlaceholderRasterizer().rasterize(req)
        self.assertFalse(PlaceholderRasterizer(validate=True).check_poster(blank, req))

    def test_rasterizer_resolution_does_not_import_playwright(self):
        before = "playwright" in sys.modules
        self.assertIsInstance(ReadoutRasterizer.resolve(None), SoftwareRasterizer)
        self.assertIsInstance(ReadoutRasterizer.resolve(("x3d", "software")), RasterizerChain)
        self.assertEqual(ReadoutRasterizer.resolve("x3d", {"timeout": 5}).timeout, 5)
        self.assertEqual("playwright" in sys.modules, before)

    def test_chain_falls_back(self):
        def fail(req):
            raise RuntimeError("nope")
        src = _triangle_source()
        req = PosterRequest(src, SceneView.fit(src.vertices()), 40, 30)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            png = ReadoutRasterizer.resolve((fail, "placeholder")).rasterize(req)
        self.assertTrue(png.startswith(b"\x89PNG"))

    def test_static_scene_exports_model_and_poster(self):
        src = _triangle_source()
        ro = Readout(ReadoutSection(ReadoutScene(model=lambda: src.figure, caption="tri"), id="s", title="S"))
        data = ro.to_pptx()
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            names = z.namelist()
        self.assertTrue(any(n.endswith(".glb") for n in names))
        self.assertTrue(any(n.endswith(".png") for n in names))


if __name__ == "__main__":
    unittest.main()

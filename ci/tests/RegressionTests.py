"""Regressions for small bugs found while building readouts (2026-10)."""
import io
import os
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile

import numpy as np


class OpenXMLRelationshipNamespaceTests(unittest.TestCase):
    def test_relationship_parts_use_the_default_namespace(self):
        # LibreOffice refuses to open packages whose .rels parts use a `rel:` prefix
        from McUtils.Plots.PowerPoint import PowerPointPresentation
        pres = PowerPointPresentation()
        pres.add_slide().draw_text("x", layout={"position": (10, 10), "size": (100, 20)})
        with zipfile.ZipFile(io.BytesIO(pres.to_bytes())) as z:
            rels = [n for n in z.namelist() if n.endswith(".rels")]
            self.assertTrue(rels)
            for name in rels:
                root = ET.fromstring(z.read(name))
                self.assertEqual(root.tag, "{http://schemas.openxmlformats.org/package/2006/relationships}Relationships")
                text = z.read(name).decode()
                self.assertNotIn("<rel:", text, name)


class Mesh3DToX3DScaleTests(unittest.TestCase):
    def test_x3d_preview_keeps_mesh_coordinates(self):
        # SphereUnionSurfaceMesh.plot treated the (already final) vertices as Bohr -> scaled by 0.529
        from McUtils.Plots.Backends import Mesh3DFigure, MeshInformation
        verts = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0.]])
        fig = Mesh3DFigure()
        fig.create_axes()
        fig.axes[0].meshes = [MeshInformation(verts, np.array([[0, 1, 2]]), normals=np.tile([0, 0, 1.], (3, 1)),
                                              material={"base_color": [1, 0, 0, 1]})]
        xml = fig.to_x3d().figure.to_x3d().to_x3d().tostring()
        import re
        point = re.search(r'<Coordinate[^>]*point="([^"]*)"', xml).group(1)
        coords = np.array(point.replace(",", " ").split(), dtype=float).reshape(-1, 3)
        np.testing.assert_allclose(np.ptp(coords, axis=0)[:2], [1, 1], atol=1e-3)


class NumpyTreeArchiveSmallTreeTests(unittest.TestCase):
    def test_small_trees_round_trip(self):
        # _downcast_uint crashed on the empty block-pointer arrays of small trees
        from McUtils.Scaffolding import NumpyTreeArchive
        trees = [
            {"a": 1},
            {"a": {"b": np.ones(2)}},
            {"molecule": {"cartesians": {"x": np.arange(3.)}, "charge": 0, "name": "w"}},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            for i, tree in enumerate(trees):
                f = os.path.join(tmp, f"t{i}.npz")
                NumpyTreeArchive.from_tree(tree).save(f)
                out = NumpyTreeArchive.load(f).unpack()
                self.assertEqual(set(map(str, out)), set(tree))


class JHTMLMarkupTests(unittest.TestCase):
    def test_boolean_attributes(self):
        # booleans used to raise TypeError in ElementTree; now True -> "true", False/None drop the attribute
        from McUtils.Jupyter import JHTML
        H = JHTML.HTML
        self.assertEqual(H.Details(H.Summary("s"), open=True, hidden=False, title=None).tostring(),
                         '<details open="true"><summary>s</summary></details>')
        self.assertEqual(H.Input(type="checkbox", checked=True, disabled=False).tostring(),
                         '<input type="checkbox" checked="true">')

    def test_none_class_is_dropped(self):
        from McUtils.Jupyter import JHTML
        H = JHTML.HTML
        self.assertEqual(H.Dd("x", cls=None).tostring(), "<dd>x</dd>")
        self.assertEqual(H.Dd("x", cls=False).tostring(), "<dd>x</dd>")
        self.assertEqual(H.Dd("x", cls=["a", "b"]).tostring(), '<dd class="a b">x</dd>')

    def test_xml_booleans_are_unchanged(self):
        from McUtils.Jupyter.OpenXML import OpenXML
        self.assertIn('saveSubsetFonts="0"', OpenXML.p.presentation(saveSubsetFonts=False).tostring())

    def test_table_sections_are_not_rewrapped(self):
        from McUtils.Jupyter import JHTML
        H = JHTML.HTML
        html = H.Table(H.Thead(H.Tr(H.Th("a"))), H.Tbody(H.Tr(H.Td("1")))).tostring()
        self.assertEqual(html, "<table><thead><tr><th>a</th></tr></thead><tbody><tr><td>1</td></tr></tbody></table>")
        # the convenience forms still work
        self.assertEqual(H.Table([[1, 2]], headers=["a", "b"]).tostring(),
                         "<table><tr><th>a</th><th>b</th></tr><tr><td>1</td><td>2</td></tr></table>")
        self.assertEqual(H.Table([[H.Th("r"), 2]]).tostring(), "<table><tr><th>r</th><td>2</td></tr></table>")


if __name__ == "__main__":
    unittest.main()

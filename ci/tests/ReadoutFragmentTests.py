"""Embeddable HTML fragments from readouts: css modes, header handling, runtime requirements."""

import unittest

import numpy as np

from McUtils.Readouts import Readout, ReadoutSection, ReadoutText, ReadoutScene, MeshSceneSource
from McUtils.Readouts.Interface import to_readout


def _titled():
    return to_readout({"energy": -76.02, "n": 3, "freqs": np.array([1600., 3700., 3800.])}, title="Water")


def _untitled():
    ro = to_readout({"a": 1})
    ro.title = None
    return ro


def _scene_readout():
    from McUtils.Plots.Backends import Mesh3DFigure, MeshInformation
    fig = Mesh3DFigure()
    fig.create_axes()
    fig.axes[0].meshes = [MeshInformation(
        np.array([[0, -1, -1], [0, 1, -1], [0, 0, 1.]]), np.array([[0, 1, 2]]),
        material={"base_color": [1, 0, 0, 1]})]
    src = MeshSceneSource(fig)
    return Readout(ReadoutSection(ReadoutScene(model=lambda: src.figure, caption="tri"), id="s", title="S"))


TITLE = 'class="mcr-title"'


class FragmentTests(unittest.TestCase):
    def test_inline_fragment_is_a_single_root_without_document_scaffolding(self):
        f = _titled().to_html_fragment()
        self.assertTrue(f.html.startswith("<div"))
        self.assertEqual(f.html.count('class="mcr-root"'), 1)
        self.assertIn("<style", f.html)
        for scaffolding in ("<!DOCTYPE", "<html", "<head", "<body"):
            self.assertNotIn(scaffolding, f.html)
        self.assertIsNone(f.css)
        self.assertEqual(f.needs, frozenset())
        self.assertEqual(f.runtime, {})
        self.assertEqual(f.to_dict()["css"], "inline")

    def test_stylesheet_mode_omits_the_style_element_and_returns_the_css(self):
        f = _titled().to_html_fragment(css="stylesheet")
        self.assertNotIn("<style", f.html)
        self.assertIn(".mcr-root", f.css)
        self.assertEqual(f.to_dict()["css"], "stylesheet")
        inline = _titled().to_html_fragment()
        self.assertIn(f.css.strip(), inline.html.replace("&gt;", ">"))  # same rules, just hosted elsewhere
        self.assertLess(len(f.html), len(inline.html))

    def test_header_auto_follows_the_title(self):
        self.assertIn(TITLE, _titled().to_html_fragment().html)
        self.assertNotIn(TITLE, _untitled().to_html_fragment().html)
        self.assertIn(TITLE, _untitled().to_html_fragment(header=True).html)
        self.assertNotIn(TITLE, _titled().to_html_fragment(header=False).html)

    def test_document_export_is_unchanged(self):
        doc = _titled().to_html()
        self.assertTrue(doc.startswith("<!DOCTYPE html>"))
        self.assertIn(TITLE, doc)
        self.assertIn("<style", doc)
        # a title-less readout still shows the default header in documents
        self.assertIn(TITLE, _untitled().to_html())

    def test_bad_options(self):
        with self.assertRaises(ValueError):
            _titled().to_html_fragment(css="external")
        with self.assertRaises(ValueError):
            _titled().to_html_fragment(header="sometimes")

    def test_scene_fragments_report_the_x3dom_requirement(self):
        f = _scene_readout().to_html_fragment()
        self.assertEqual(f.needs, frozenset({"x3dom"}))
        runtime = f.runtime["x3dom"]
        self.assertTrue(runtime["script"].startswith("http"))
        self.assertTrue(runtime["stylesheet"].startswith("http"))
        self.assertIn("x3d", f.html.lower())
        self.assertNotIn("<script", f.html)  # the host page loads the runtime, once

    def test_custom_x3dom_url_and_unusable_paths(self):
        f = _scene_readout().to_html_fragment(x3dom_path="https://example.org/x3dom.js")
        self.assertEqual(f.runtime["x3dom"], {"script": "https://example.org/x3dom.js", "stylesheet": None})
        for bad in ("local", "inline"):
            with self.subTest(bad):
                with self.assertRaises(ValueError):
                    _scene_readout().to_html_fragment(x3dom_path=bad)

    def test_widget_renderer_cannot_make_fragments(self):
        from McUtils.Readouts.Renderers.HTML import HTMLReadoutRenderer
        with self.assertRaises(ValueError):
            HTMLReadoutRenderer(mode="widget").render_fragment_result(_titled())


if __name__ == "__main__":
    unittest.main()

"""Public-API regression tests for backend-neutral McUtils axes_scales.

Run against the isolated candidate, never by patching imported classes:
  MCUTILS_AXES_SOURCE=/private/tmp/mcutils-axes-scales-20261026/work \
    <native ARM Python> -B -m unittest discover -s <this directory> -p test_axes_scales.py -v

The numerical assertions inspect actual Matplotlib transforms and serialized
Plotly layout/data, rather than trusting only McUtils's cached property value.
Plotly tests use native dictionary serialization; no browser, renderer, network,
Kaleido or image-export dependency is required.
"""
import os
from pathlib import Path
import platform
import re
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
configured_source = os.environ.get("MCUTILS_AXES_SOURCE")
SOURCE = (Path(configured_source).resolve() if configured_source else
          ((HERE / "work").resolve() if (HERE / "work" / "McUtils").is_dir() else None))
CACHE = Path(os.environ.get("MCUTILS_AXES_CACHE", tempfile.mkdtemp(prefix="mcutils-axes-scales-tests-")))
for name, leaf in (("NUMBA_CACHE_DIR", "numba"), ("MPLCONFIGDIR", "matplotlib"),
                   ("XDG_CACHE_HOME", "xdg")):
    target = CACHE / leaf
    target.mkdir(parents=True, exist_ok=True)
    os.environ[name] = str(target)
os.environ["MPLBACKEND"] = "Agg"
if SOURCE is not None:
    sys.path.insert(0, str(SOURCE))
DEPS = Path(os.environ.get("MCUTILS_AXES_DEPENDENCIES", str(HERE / "test-deps"))).resolve()
if DEPS.is_dir():
    if os.environ.get("MCUTILS_AXES_MPL", "base") == "new":
        sys.path.insert(1, str(DEPS))
    else:
        sys.path.append(str(DEPS))

import matplotlib
import numpy as np
import McUtils
from McUtils.Plots import Graphics, Graphics3D, GraphicsGrid, Plot, Plot3D, Styled


def mpl_supports_nonlinear_3d():
    major, minor = (int(v) for v in re.match(r"(\d+)\.(\d+)", matplotlib.__version__).groups())
    return (major, minor) >= (3, 11)


class AxesScalesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.environ.get("MCUTILS_AXES_REQUIRE_ARM") == "1" and platform.machine() != "arm64":
            raise RuntimeError("Use the native ARM Python environment")
        if SOURCE is not None and SOURCE not in Path(McUtils.__file__).resolve().parents:
            raise RuntimeError("Tests must import the isolated candidate package")

    def tearDown(self):
        # Failed constructors can create a native figure before validation.
        import matplotlib.pyplot as plt
        plt.close("all")

    def new(self, cls=Graphics, *args, **kwargs):
        result = cls(*args, **kwargs)
        self.addCleanup(result.close)
        return result

    def actual_scales(self, graphics, dimension):
        if hasattr(graphics.figure, "prep_dict"):
            layout = graphics.figure.prep_dict()["layout"]
            axes = layout["scene"] if dimension == 3 else layout
            return tuple(axes.get(axis + "axis", {}).get("type", "linear")
                         for axis in "xyz"[:dimension])
        native = graphics.axes.obj
        return tuple(getattr(native, "get_" + axis + "scale")() for axis in "xyz"[:dimension])

    def assert_scales(self, graphics, expected):
        self.assertEqual(self.actual_scales(graphics, len(expected)), tuple(expected))
        self.assertEqual(tuple(graphics.axes_scales), tuple(expected))

    def surface(self):
        x, y = np.meshgrid([1., 2., 10.], [1., 3., 10.])
        return x, y, x + y

    def test_graphics_keyword_string_broadcasts_2d(self):
        for backend in ("matplotlib", "plotly"):
            with self.subTest(backend=backend):
                g = self.new(backend=backend, axes_scales="log")
                self.assert_scales(g, ("log", "log"))
                self.assertIn("axes_scales", g.opts)
                self.assertEqual(tuple(g.opts["axes_scales"]), ("log", "log"))

    def test_property_updates_only_requested_axis_and_resets_linear_2d(self):
        for backend in ("matplotlib", "plotly"):
            with self.subTest(backend=backend):
                g = self.new(backend=backend, axes_scales=("log", "linear"))
                g.axes_scales = (None, "log")
                self.assert_scales(g, ("log", "log"))
                g.set_options(axes_scales=["linear", None])
                self.assert_scales(g, ("linear", "log"))
                g.axes_scales = "linear"
                self.assert_scales(g, ("linear", "linear"))

    def test_plot_keyword_has_real_axis_transform_and_unchanged_data(self):
        x, y = np.array([1., 2., 4.]), np.array([1., 4., 16.])
        for backend in ("matplotlib", "plotly"):
            with self.subTest(backend=backend):
                g = self.new(Plot, x, y, backend=backend, axes_scales=("log", "log"))
                self.assert_scales(g, ("log", "log"))
                if backend == "matplotlib":
                    line = g.axes.obj.get_lines()[0]
                    np.testing.assert_array_equal(line.get_xdata(), x)
                    np.testing.assert_array_equal(line.get_ydata(), y)
                    np.testing.assert_allclose(g.axes.obj.xaxis.get_transform().transform([1., 10., 100.]),
                                               [0., 1., 2.], atol=1e-14)
                else:
                    trace = g.figure.prep_dict()["data"][0]
                    np.testing.assert_array_equal(trace["x"], x)
                    np.testing.assert_array_equal(trace["y"], y)

    def test_mpl_styled_log_base_changes_actual_transform(self):
        g = self.new(axes_scales=(Styled("log", base=2), "linear"))
        self.assertEqual(g.axes.obj.get_xscale(), "log")
        np.testing.assert_allclose(g.axes.obj.xaxis.get_transform().transform([1., 2., 4., 8.]),
                                   [0., 1., 2., 3.], atol=1e-14)
        copied = g.copy()
        self.addCleanup(copied.close)
        np.testing.assert_allclose(copied.axes.obj.xaxis.get_transform().transform([1., 2., 4., 8.]),
                                   [0., 1., 2., 3.], atol=1e-14)
        g.axes_scales = ("linear", Styled("log", base=4))
        np.testing.assert_allclose(g.axes.obj.yaxis.get_transform().transform([1., 4., 16.]),
                                   [0., 1., 2.], atol=1e-14)
        g.axes_scales = "linear"
        self.assert_scales(g, ("linear", "linear"))

    def test_mpl_styled_tuple_form(self):
        g = self.new(axes_scales=(("log", {"base": 2}), "linear"))
        np.testing.assert_allclose(g.axes.obj.xaxis.get_transform().transform([1., 2., 4.]),
                                   [0., 1., 2.], atol=1e-14)

    def test_legacy_scalar_scale_remains_y_only_2d(self):
        for backend in ("matplotlib", "plotly"):
            with self.subTest(backend=backend):
                g = self.new(backend=backend, scale="log")
                self.assert_scales(g, ("linear", "log"))
                g.scale = "linear"
                self.assert_scales(g, ("linear", "linear"))
                g.set_options(scale=("log", "linear"))
                self.assert_scales(g, ("log", "linear"))

    def test_alias_update_replaces_copy_state_in_both_directions(self):
        for backend in ("matplotlib", "plotly"):
            with self.subTest(backend=backend, order="canonical_then_alias"):
                g = self.new(backend=backend, axes_scales=("log", "linear"))
                g.scale = ("linear", "log")
                copied = g.copy()
                self.addCleanup(copied.close)
                self.assertIsNot(copied.axes, g.axes)
                self.assert_scales(copied, ("linear", "log"))
            with self.subTest(backend=backend, order="alias_then_canonical"):
                g = self.new(backend=backend, scale="log")
                g.axes_scales = ("log", "linear")
                copied = g.copy()
                self.addCleanup(copied.close)
                self.assert_scales(copied, ("log", "linear"))

    def test_both_non_none_keywords_conflict_constructor_and_updates(self):
        for backend in ("matplotlib", "plotly"):
            with self.subTest(backend=backend):
                with self.assertRaises(ValueError):
                    Graphics(backend=backend, axes_scales=("linear", "log"), scale="log")
                g = self.new(backend=backend)
                with self.assertRaises(ValueError):
                    g.set_options(axes_scales=("log", "linear"), scale=("log", "linear"))
                self.assert_scales(g, ("linear", "linear"))
                self.assert_scales(self.new(backend=backend, axes_scales=None, scale="log"),
                                   ("linear", "log"))

    def test_invalid_sequence_lengths_are_rejected_before_mutation_2d(self):
        for backend in ("matplotlib", "plotly"):
            for invalid in ([], ["log"], ["linear", "log", "linear"]):
                with self.subTest(backend=backend, invalid=invalid):
                    g = self.new(backend=backend, axes_scales=("linear", "log"))
                    with self.assertRaises(ValueError):
                        g.axes_scales = invalid
                    self.assert_scales(g, ("linear", "log"))

    def test_invalid_types_and_entries_are_rejected_before_mutation(self):
        invalids = (True, 3, 1.5, b"log", {"x": "log"}, ("log", 3), ("log", ["linear"]))
        for backend in ("matplotlib", "plotly"):
            for invalid in invalids:
                with self.subTest(backend=backend, invalid=repr(invalid)):
                    g = self.new(backend=backend)
                    with self.assertRaises((ValueError, TypeError)):
                        g.axes_scales = invalid
                    self.assert_scales(g, ("linear", "linear"))

    def test_unknown_scale_name_does_not_partially_update_other_axis(self):
        for backend in ("matplotlib", "plotly"):
            with self.subTest(backend=backend):
                g = self.new(backend=backend)
                with self.assertRaises(ValueError):
                    g.axes_scales = ("log", "not-a-scale")
                self.assert_scales(g, ("linear", "linear"))
                # A failed update must not leak into a later copied figure.
                copied = g.copy()
                self.addCleanup(copied.close)
                self.assert_scales(copied, ("linear", "linear"))

    def test_plotly_2d_axis_serialization_and_independent_figures(self):
        first = self.new(backend="plotly", axes_scales=("log", "linear"))
        second = self.new(backend="plotly", axes_scales=("linear", "log"))
        self.assert_scales(first, ("log", "linear"))
        self.assert_scales(second, ("linear", "log"))
        first.axes_scales = "linear"
        self.assert_scales(first, ("linear", "linear"))
        self.assert_scales(second, ("linear", "log"))
        self.assertNotIn("scene", second.figure.prep_dict()["layout"])

    def test_plotly_default_categorical_and_date_axes_stay_automatic_after_prep_and_copy(self):
        for x in (["alpha", "beta", "gamma"], ["2026-10-01", "2026-10-02", "2026-10-03"]):
            with self.subTest(x=x):
                g = self.new(Plot, x, [1., 10., 100.], backend="plotly")
                self.assertNotIn("axes_scales", g.opts)
                self.assertNotIn("type", g.figure.prep_dict()["layout"].get("xaxis", {}))
                g.prep_show()
                self.assertNotIn("type", g.figure.prep_dict()["layout"].get("xaxis", {}))
                copied = g.copy()
                self.addCleanup(copied.close)
                copied.prep_show()
                layout = copied.figure.prep_dict()["layout"]
                self.assertNotIn("type", layout.get("xaxis", {}))
                self.assertNotIn("type", layout.get("yaxis", {}))
                np.testing.assert_array_equal(copied.figure.prep_dict()["data"][0]["x"], x)

    def test_plotly_partial_y_log_never_forces_unconfigured_x_linear(self):
        for x in (["alpha", "beta", "gamma"], ["2026-10-01", "2026-10-02", "2026-10-03"]):
            with self.subTest(x=x):
                g = self.new(Plot, x, [1., 10., 100.], backend="plotly", axes_scales=(None, "log"))
                self.assertEqual(tuple(g.opts["axes_scales"]), (None, "log"))
                g.prep_show()
                layout = g.figure.prep_dict()["layout"]
                self.assertNotIn("type", layout.get("xaxis", {}))
                self.assertEqual(layout["yaxis"]["type"], "log")
                copied = g.copy()
                self.addCleanup(copied.close)
                copied.prep_show()
                layout = copied.figure.prep_dict()["layout"]
                self.assertNotIn("type", layout.get("xaxis", {}))
                self.assertEqual(layout["yaxis"]["type"], "log")

    def test_plotly_all_none_noop_does_not_convert_default_axis_types(self):
        for cls, backend, none_values in ((Graphics, "plotly", (None, None)),
                                          (Graphics3D, "plotly3D", (None, None, None))):
            with self.subTest(backend=backend):
                g = self.new(cls, backend=backend)
                g.axes_scales = none_values
                self.assertNotIn("axes_scales", g.opts)
                g.prep_show()
                copied = g.copy()
                self.addCleanup(copied.close)
                copied.prep_show()
                for value in (g, copied):
                    layout = value.figure.prep_dict()["layout"]
                    axes = layout.get("scene", layout)
                    for axis in "xyz"[:len(none_values)]:
                        self.assertNotIn("type", axes.get(axis + "axis", {}))

    def test_mpl_managed_grid_panels_preserve_independent_options_through_prep(self):
        g = self.new(GraphicsGrid, nrows=1, ncols=2)
        Plot([1., 2., 4.], [1., 4., 16.], figure=g[0, 0], axes_scales=("log", "linear"))
        Plot([1., 2., 4.], [1., 4., 16.], figure=g[0, 1], axes_scales=("linear", "log"))
        g.prep_show()
        self.assert_scales(g[0, 0], ("log", "linear"))
        self.assert_scales(g[0, 1], ("linear", "log"))
        g[0, 0].scale = "log"
        g.prep_show()
        self.assert_scales(g[0, 0], ("log", "log"))
        self.assert_scales(g[0, 1], ("linear", "log"))
        # Full GraphicsGrid.copy has an independent pre-existing nrows-forwarding
        # failure, reproduced on the untouched baseline without any scales.
        # Standalone Graphics/Plot copying is covered separately above.

    def test_plotly_log_limits_roundtrip_in_data_units_2d(self):
        g = self.new(Plot, [1., 10., 100.], [1., 100., 10000.], backend="plotly",
                     axes_scales=("log", "log"), plot_range=((1., 100.), (1., 10000.)))
        layout = g.figure.prep_dict()["layout"]
        np.testing.assert_allclose(layout["xaxis"]["range"], [0., 2.], atol=1e-14)
        np.testing.assert_allclose(layout["yaxis"]["range"], [0., 4.], atol=1e-14)
        np.testing.assert_allclose(g.plot_range, [[1., 100.], [1., 10000.]], atol=1e-12)
        g.axes_scales = ("linear", "log")
        layout = g.figure.prep_dict()["layout"]
        np.testing.assert_allclose(layout["xaxis"]["range"], [1., 100.], atol=1e-12)
        np.testing.assert_allclose(layout["yaxis"]["range"], [0., 4.], atol=1e-14)
        g.axes_scales = "linear"
        np.testing.assert_allclose(g.figure.prep_dict()["layout"]["yaxis"]["range"], [1., 10000.], atol=1e-10)

    def test_plotly_rejects_unsupported_scale_names_and_keywords(self):
        for spec in ("symlog", "logit", Styled("log", base=2), ("log", {"base": 2})):
            with self.subTest(spec=repr(spec)):
                g = self.new(backend="plotly")
                with self.assertRaises((ValueError, TypeError, NotImplementedError)):
                    g.axes_scales = ("log", spec)
                self.assert_scales(g, ("linear", "linear"))

    def test_graphics3d_default_and_explicit_linear_option_roundtrip(self):
        for backend in ("matplotlib3D", "plotly3D"):
            with self.subTest(backend=backend):
                g = self.new(Graphics3D, backend=backend, axes_scales=["linear", "linear", "linear"])
                self.assert_scales(g, ("linear", "linear", "linear"))
                self.assertIn("axes_scales", g.opts)
                copied = g.copy()
                self.addCleanup(copied.close)
                self.assert_scales(copied, ("linear", "linear", "linear"))

    def test_mpl3d_nonlinear_capability_is_explicit(self):
        g = self.new(Graphics3D, axes_scales="linear")
        if mpl_supports_nonlinear_3d():
            g.axes_scales = ("log", "linear", "log")
            self.assert_scales(g, ("log", "linear", "log"))
            g.axes_scales = (None, "log", None)
            self.assert_scales(g, ("log", "log", "log"))
            g.axes_scales = "linear"
            self.assert_scales(g, ("linear", "linear", "linear"))
        else:
            with self.assertRaisesRegex(NotImplementedError, "3[.]11"):
                g.axes_scales = ("linear", "linear", "log")
            self.assert_scales(g, ("linear", "linear", "linear"))

    def test_graphics3d_string_broadcast_and_legacy_y_only(self):
        for backend in ("plotly3D",) + (("matplotlib3D",) if mpl_supports_nonlinear_3d() else ()):
            with self.subTest(backend=backend):
                g = self.new(Graphics3D, backend=backend, axes_scales="log")
                self.assert_scales(g, ("log", "log", "log"))
                g.scale = "linear"
                self.assert_scales(g, ("log", "linear", "log"))
                g.scale = ("linear", "log")
                self.assert_scales(g, ("linear", "log", "log"))
                g.scale = ("log", "linear", "linear")
                self.assert_scales(g, ("log", "linear", "linear"))
                g.set_options(axes_scales=[None, None, "log"])
                self.assert_scales(g, ("log", "linear", "log"))

    def test_graphics3d_rejects_wrong_canonical_lengths(self):
        for backend in ("matplotlib3D", "plotly3D"):
            for invalid in ([], ["linear"], ["linear", "linear"], ["linear"] * 4):
                with self.subTest(backend=backend, invalid=invalid):
                    g = self.new(Graphics3D, backend=backend)
                    with self.assertRaises(ValueError):
                        g.axes_scales = invalid
                    self.assert_scales(g, ("linear", "linear", "linear"))

    def test_plotly_scene_serializes_three_independent_axes(self):
        g = self.new(Graphics3D, backend="plotly3D", axes_scales=("log", "linear", "log"))
        self.assert_scales(g, ("log", "linear", "log"))
        layout = g.figure.prep_dict()["layout"]
        for key in ("xaxis", "yaxis", "zaxis"):
            self.assertNotIn(key, layout)
        self.assertEqual(layout["scene"]["xaxis"]["type"], "log")
        self.assertEqual(layout["scene"]["zaxis"]["type"], "log")
        g.axes_scales = ("linear", "log", None)
        self.assert_scales(g, ("linear", "log", "log"))
        copied = g.copy()
        self.addCleanup(copied.close)
        self.assert_scales(copied, ("linear", "log", "log"))

    def test_plotly_native_dict_accepts_real_plotly_serialization_2d_and_3d(self):
        for cls, backend, scales in ((Graphics, "plotly", ("log", "linear")),
                                     (Graphics3D, "plotly3D", ("linear", "log", "log"))):
            with self.subTest(backend=backend):
                g = self.new(cls, backend=backend, axes_scales=scales)
                native = g.figure.to_plotly().to_plotly_json()["layout"]
                axes = native["scene"] if len(scales) == 3 else native
                for axis, scale in zip("xyz", scales):
                    self.assertEqual(axes.get(axis + "axis", {}).get("type", "linear"), scale)

    def test_plotly_scene_log_ranges_keep_data_unit_roundtrip(self):
        ranges = ((1., 100.), (1., 10.), (10., 1000.))
        g = self.new(Graphics3D, backend="plotly3D", axes_scales=("log", "linear", "log"), plot_range=ranges)
        scene = g.figure.prep_dict()["layout"]["scene"]
        for axis, expected in (("xaxis", [0., 2.]), ("yaxis", [1., 10.]), ("zaxis", [1., 3.])):
            np.testing.assert_allclose(scene[axis]["range"], expected, atol=1e-14)
        np.testing.assert_allclose(g.plot_range, ranges, atol=1e-12)
        g.axes_scales = ("linear", "log", "linear")
        scene = g.figure.prep_dict()["layout"]["scene"]
        for axis, expected in (("xaxis", [1., 100.]), ("yaxis", [0., 1.]), ("zaxis", [10., 1000.])):
            np.testing.assert_allclose(scene[axis]["range"], expected, atol=1e-12)

    def test_plotly3d_rejects_unsupported_without_partial_scene_update(self):
        g = self.new(Graphics3D, backend="plotly3D")
        with self.assertRaises((ValueError, NotImplementedError)):
            g.axes_scales = ("log", "linear", "symlog")
        self.assert_scales(g, ("linear", "linear", "linear"))

    def test_plot3d_real_surface_keyword_options_and_backend(self):
        for backend in ("matplotlib3D", "plotly3D"):
            with self.subTest(backend=backend):
                scales = ("log", "linear", "log") if (backend == "plotly3D" or mpl_supports_nonlinear_3d()) else ("linear",) * 3
                g = self.new(Plot3D, *self.surface(), backend=backend, axes_scales=scales)
                self.assert_scales(g, scales)
                if backend == "plotly3D":
                    dictionary = g.figure.prep_dict()
                    self.assertEqual(dictionary["data"][0]["type"], "surface")
                    np.testing.assert_array_equal(dictionary["data"][0]["z"], self.surface()[2])
                else:
                    self.assertTrue(g.axes.obj.collections)
                    with tempfile.TemporaryDirectory(prefix="axes-scales-render-") as tmp:
                        path = Path(tmp) / "surface.png"
                        g.savefig(str(path))
                        self.assertGreater(path.stat().st_size, 500)

    def test_plot3d_delayed_surface_preserves_preplot_property_update(self):
        for backend in ("matplotlib3D", "plotly3D"):
            for alias in ("axes_scales", "scale"):
                with self.subTest(backend=backend, alias=alias):
                    nonlinear = backend == "plotly3D" or mpl_supports_nonlinear_3d()
                    g = self.new(Plot3D, backend=backend, axes_scales="linear")
                    if alias == "axes_scales":
                        scales = ("log", "linear", "linear") if nonlinear else ("linear",) * 3
                        g.axes_scales = scales
                    else:
                        g.scale = "log" if nonlinear else "linear"
                        scales = ("linear", "log", "linear") if nonlinear else ("linear",) * 3
                    g.plot(*self.surface())
                    self.assert_scales(g, scales)

    def test_plot_delayed_preserves_canonical_and_legacy_property_updates(self):
        for backend in ("matplotlib", "plotly"):
            for alias in ("axes_scales", "scale"):
                with self.subTest(backend=backend, alias=alias):
                    g = self.new(Plot, backend=backend, axes_scales="linear")
                    if alias == "axes_scales":
                        g.axes_scales = ("log", "linear")
                        expected = ("log", "linear")
                    else:
                        g.scale = "log"
                        expected = ("linear", "log")
                    g.plot([1., 2., 4.], [1., 4., 16.])
                    self.assert_scales(g, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)

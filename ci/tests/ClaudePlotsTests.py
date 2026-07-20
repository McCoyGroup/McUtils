"""
Tests for `McUtils.Plots`, paralleling the style of the other `ci/tests/*.py`
modules in the McUtils repository (one `TestCase` per package, one `test_`
method per feature).

Drafted from the stub docstrings under `McUtils/stubs/McUtils/Plots` (the
`Plots`, `Graphics`, `Backends`, `Colors`, and `Properties` modules) plus the
`Plots` usages already present in `ci/tests/NumputilsTests.py` and
`ci/tests/ZacharyTests.py`. Every McUtils object used here (`Plot`,
`ScatterPlot`, `ArrayPlot`, `GraphicsGrid`, `Plot3D`, `prep_color`, the
`Numputils` geometry helpers, etc.) comes straight out of the package; the
only non-McUtils dependency is `matplotlib`, which is the `Plots` package's
own declared backend dependency in `dependency_graph.json` (no extra
third-party packages are introduced).

Unlike the repo's real test suite, this module does not depend on
`Peeves.TestUtils` (`validationTest`/`debugTest`/`TestManager`) since `Peeves`
is an internal McCoy Group testing harness, not a module of McUtils itself.
Plain `unittest` is used instead, and the matplotlib backend is forced to the
non-interactive `Agg` backend so the whole suite can run headless (`.show()`
is never called; figures are instead rendered with `.savefig`/`.to_image`
into a scratch directory and then closed).
"""

import os
import shutil
import tempfile
import unittest

import matplotlib
matplotlib.use("Agg")  # headless: no display is available in this environment

import numpy as np

import McUtils.Numputils as nput
import McUtils.Plots as plt


class ClaudePlotsTests(unittest.TestCase):
    """
    Exercises the `McUtils.Plots` plotting classes: the 1D `Plot` family,
    the 2D `Plot2D`/`ArrayPlot` family, the 3D `Plot3D` family, layout via
    `GraphicsGrid`/`CompositePlot`, and the `Colors` helpers.
    """

    out_dir = None

    @classmethod
    def setUpClass(cls):
        cls.out_dir = tempfile.mkdtemp(prefix="McUtils_PlotsTests_")

    @classmethod
    def tearDownClass(cls):
        if cls.out_dir is not None:
            shutil.rmtree(cls.out_dir, ignore_errors=True)

    def out_path(self, name):
        """
        Build a scratch output path for a rendered figure.

        :param name: the file name (with extension)
        :type name: str
        :return: the absolute path under this test class' temp directory
        :rtype: str
        """
        return os.path.join(self.out_dir, name)

    def save_and_close(self, fig, name):
        """
        Render a `Graphics`/`Plot` object to a file and close it, the
        headless stand-in for `fig.show()`.

        :param fig: the graphics object to render
        :param name: the output file name
        :type name: str
        """
        path = self.out_path(name)
        fig.savefig(path)
        self.assertTrue(os.path.exists(path))
        self.assertGreater(os.path.getsize(path), 0)
        fig.close()

    # region 1D `Plot` family

    def test_BasicLinePlot(self):
        """A minimal `Plot(x, y)` line plot renders and saves cleanly."""
        x = np.linspace(0, 2 * np.pi, 100)
        y = np.sin(x)
        fig = plt.Plot(x, y,
                        plot_range=[[0, 2 * np.pi], [-1.5, 1.5]],
                        image_size=400,
                        aspect_ratio=1)
        self.save_and_close(fig, "line_plot.png")

    def test_FunctionPlot(self):
        """`Plot` also accepts a callable plus an `x` range, sampling it internally."""
        fig = plt.Plot(np.cos, [0, 2 * np.pi])
        self.save_and_close(fig, "function_plot.png")

    def test_ScatterPlot(self):
        """`ScatterPlot(x, y)` draws points via the backend `scatter` method."""
        np.random.seed(0)
        x = np.random.uniform(-1, 1, 50)
        y = np.random.uniform(-1, 1, 50)
        fig = plt.ScatterPlot(x, y, plot_range=[[-1, 1], [-1, 1]])
        self.save_and_close(fig, "scatter_plot.png")

    def test_ListScatterPlot(self):
        """`ListScatterPlot` builds a scatter plot straight from an `(n, 2)` point array."""
        np.random.seed(1)
        pts = np.random.uniform(-1, 1, (30, 2))
        fig = plt.ListScatterPlot(pts)
        self.save_and_close(fig, "list_scatter_plot.png")

    def test_ListScatterPlot_viaSubmodule(self):
        """
        `ListScatterPlot` is not registered into the `McUtils.Plots` namespace (no
        `@Plot.register` and no `__all__` entry), only the `McUtils.Plots.Plots`
        submodule; imported that way it works exactly like `test_ListScatterPlot`
        expects. This isolates "the class isn't exported" from "the class is broken".
        """
        from McUtils.Plots.Plots import ListScatterPlot
        np.random.seed(1)
        pts = np.random.uniform(-1, 1, (30, 2))
        fig = ListScatterPlot(pts)
        self.save_and_close(fig, "list_scatter_plot_submodule.png")

    def test_ScatterPlotWithColorPalette(self):
        """`prep_color` resolves a named palette against a blending array for per-point colors."""
        np.random.seed(2)
        x = np.linspace(0, 1, 40)
        y = np.sin(2 * np.pi * x)
        colors = plt.prep_color(palette="viridis", blending=x)
        fig = plt.ScatterPlot(x, y, color=colors)
        self.save_and_close(fig, "scatter_palette_plot.png")

    def test_ErrorBarPlot(self):
        """`ErrorBarPlot` draws error bars via the backend `errorbar` method."""
        x = np.linspace(0, 10, 12)
        y = np.sin(x)
        yerr = 0.1 * np.ones_like(x)
        fig = plt.ErrorBarPlot(x, y, plot_style=dict(yerr=yerr))
        self.save_and_close(fig, "errorbar_plot.png")

    def test_ListErrorBarPlot(self):
        """`ListErrorBarPlot` pulls its `(x, y)` data from an `(n, 2)` array."""
        pts = np.column_stack([np.linspace(0, 5, 10), np.linspace(0, 5, 10) ** 2])
        fig = plt.ListErrorBarPlot(pts, plot_style=dict(yerr=1.0))
        self.save_and_close(fig, "list_errorbar_plot.png")

    def test_ListErrorBarPlot_viaSubmodule(self):
        """
        Like `ListScatterPlot`, `ListErrorBarPlot` exists in `McUtils.Plots.Plots` but
        isn't registered/exported to `McUtils.Plots`; imported directly it works fine.
        """
        from McUtils.Plots.Plots import ListErrorBarPlot
        pts = np.column_stack([np.linspace(0, 5, 10), np.linspace(0, 5, 10) ** 2])
        fig = ListErrorBarPlot(pts, plot_style=dict(yerr=1.0))
        self.save_and_close(fig, "list_errorbar_plot_submodule.png")

    def test_StickPlot(self):
        """`StickPlot` (stem plot) renders a set of `(x, y)` sticks."""
        x = np.arange(10)
        y = np.random.RandomState(3).rand(10)
        fig = plt.StickPlot(x, y)
        self.save_and_close(fig, "stick_plot.png")

    def test_HistogramPlot(self):
        """`HistogramPlot` wraps the backend `hist` method for arbitrary 1D data."""
        data = np.random.RandomState(4).normal(size=500)
        fig = plt.HistogramPlot(data, plot_style=dict(bins=20))
        self.save_and_close(fig, "histogram_plot.png")

    def test_BarPlot(self):
        """`BarPlot` draws a categorical bar chart."""
        x = np.arange(5)
        heights = np.array([3, 7, 2, 5, 4])
        fig = plt.BarPlot(x, heights)
        self.save_and_close(fig, "bar_plot.png")

    def test_PiePlot(self):
        """`PiePlot` draws a pie chart from a set of wedge sizes."""
        sizes = [15, 30, 45, 10]
        fig = plt.PiePlot(sizes)
        self.save_and_close(fig, "pie_plot.png")

    def test_LogLogPlot(self):
        """`LogLogPlot` is a `Plot` variant using log-log axis scaling."""
        x = np.linspace(1, 100, 50)
        y = x ** 2
        fig = plt.LogLogPlot(x, y)
        self.save_and_close(fig, "loglog_plot.png")

    def test_QuiverPlot(self):
        """`QuiverPlot` renders a 2D vector field from `(x, y, u, v)` data."""
        x, y = np.meshgrid(np.linspace(-1, 1, 8), np.linspace(-1, 1, 8))
        u, v = -y, x
        fig = plt.QuiverPlot(x, y, u, v)
        self.save_and_close(fig, "quiver_plot.png")

    # endregion

    # region 2D data (`ArrayPlot`/`Plot2D`) family

    def test_ArrayPlot(self):
        """`ArrayPlot` shows a 2D array as an image via `imshow`."""
        arr = np.random.RandomState(5).rand(20, 20)
        fig = plt.ArrayPlot(arr)
        self.save_and_close(fig, "array_plot.png")

    def test_MatrixPlot(self):
        """`MatrixPlot` is the `matshow`-based `ArrayPlot` variant."""
        arr = np.eye(10) + 0.1 * np.random.RandomState(6).rand(10, 10)
        fig = plt.MatrixPlot(arr)
        self.save_and_close(fig, "matrix_plot.png")

    def test_SparsityPlot(self):
        """`SparsityPlot` renders the nonzero structure of a matrix via `spy`."""
        arr = np.zeros((15, 15))
        idx = np.random.RandomState(7).choice(15 * 15, 30, replace=False)
        arr.flat[idx] = 1
        fig = plt.SparsityPlot(arr)
        self.save_and_close(fig, "sparsity_plot.png")

    def test_ContourPlot(self):
        """`ContourPlot` draws filled contours of gridded `(x, y, z)` data."""
        x = np.linspace(-2, 2, 40)
        y = np.linspace(-2, 2, 40)
        X, Y = np.meshgrid(x, y)
        Z = np.exp(-(X ** 2 + Y ** 2))
        fig = plt.ContourPlot(X, Y, Z)
        self.save_and_close(fig, "contour_plot.png")

    def test_DensityPlot(self):
        """`DensityPlot` shades gridded `(x, y, z)` data as a continuous density."""
        x = np.linspace(-2, 2, 40)
        y = np.linspace(-2, 2, 40)
        X, Y = np.meshgrid(x, y)
        Z = np.exp(-(X ** 2 + Y ** 2))
        fig = plt.DensityPlot(X, Y, Z)
        self.save_and_close(fig, "density_plot.png")

    def test_HeatmapPlot(self):
        """`HeatmapPlot` combines `ArrayPlot`-style coloring with `Plot2D` axes."""
        x = np.linspace(-2, 2, 30)
        y = np.linspace(-2, 2, 30)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(X) * np.cos(Y)
        fig = plt.HeatmapPlot(X, Y, Z)
        self.save_and_close(fig, "heatmap_plot.png")

    def test_ListContourPlot(self):
        """`ListContourPlot` interpolates scattered `(x, y, z)` points onto a contour grid."""
        np.random.seed(8)
        pts = np.random.uniform(-2, 2, (200, 2))
        z = np.exp(-(pts[:, 0] ** 2 + pts[:, 1] ** 2))
        griddata = np.column_stack([pts, z])
        fig = plt.ListContourPlot(griddata)
        self.save_and_close(fig, "list_contour_plot.png")

    def test_ListDensityPlot(self):
        """`ListDensityPlot` interpolates scattered `(x, y, z)` points onto a density grid."""
        np.random.seed(9)
        pts = np.random.uniform(-2, 2, (200, 2))
        z = np.sin(pts[:, 0]) * np.cos(pts[:, 1])
        griddata = np.column_stack([pts, z])
        fig = plt.ListDensityPlot(griddata)
        self.save_and_close(fig, "list_density_plot.png")

    def test_TensorPlot(self):
        """`TensorPlot` lays out the 2D slices of a higher-rank tensor as an array-plot grid."""
        tensor = np.random.RandomState(10).rand(2, 3, 8, 8)
        fig = plt.TensorPlot(tensor)
        fig.savefig(self.out_path("tensor_plot.png"))
        self.assertTrue(os.path.exists(self.out_path("tensor_plot.png")))

    # endregion

    # region 3D (`Plot3D`) family

    def test_Plot3DSurface(self):
        """`Plot3D` draws a 3D surface from a `(func, xrange, yrange)` or gridded `(x, y, z)` spec."""
        x = np.linspace(-2, 2, 25)
        y = np.linspace(-2, 2, 25)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(X) * np.cos(Y)
        fig = plt.Plot3D(X, Y, Z)
        self.save_and_close(fig, "plot3d_surface.png")

    def test_ScatterPlot3D(self):
        """`ScatterPlot3D` scatters 3D `(x, y, z)` points."""
        np.random.seed(11)
        pts = np.random.uniform(-1, 1, (60, 3))
        fig = plt.ScatterPlot3D(*pts.T)
        self.save_and_close(fig, "scatter_plot3d.png")

    def test_WireframePlot3D(self):
        """`WireframePlot3D` draws a wireframe mesh of gridded 3D data."""
        x = np.linspace(-2, 2, 15)
        y = np.linspace(-2, 2, 15)
        X, Y = np.meshgrid(x, y)
        Z = X ** 2 - Y ** 2
        fig = plt.WireframePlot3D(X, Y, Z)
        self.save_and_close(fig, "wireframe_plot3d.png")

    def test_ContourPlot3D(self):
        """`ContourPlot3D` draws filled 3D contours (`contourf`) of gridded data."""
        x = np.linspace(-2, 2, 20)
        y = np.linspace(-2, 2, 20)
        X, Y = np.meshgrid(x, y)
        Z = np.exp(-(X ** 2 + Y ** 2))
        fig = plt.ContourPlot3D(X, Y, Z)
        self.save_and_close(fig, "contour_plot3d.png")

    def test_ListPlot3D(self):
        """`ListPlot3D` interpolates a scattered `(x, y, z)` point array onto a mesh before plotting."""
        np.random.seed(12)
        pts = np.random.uniform(-2, 2, (150, 2))
        z = np.sin(pts[:, 0]) * np.cos(pts[:, 1])
        griddata = np.column_stack([pts, z])
        fig = plt.ListPlot3D(griddata)
        self.save_and_close(fig, "list_plot3d.png")

    # endregion

    # region layout: `GraphicsGrid` / `CompositePlot`

    def test_GraphicsGrid(self):
        """A `GraphicsGrid` hosts independent subplots addressed by `grid[row, col]`."""
        grid = plt.GraphicsGrid(nrows=1, ncols=2)
        x = np.linspace(0, 2 * np.pi, 100)
        plt.Plot(x, np.sin(x), figure=grid[0, 0])
        plt.Plot(x, np.cos(x), figure=grid[0, 1])
        self.save_and_close(grid, "graphics_grid.png")

    def test_CompositePlotMerge(self):
        """Overlaying a second `Plot` on an existing `figure=` merges both series onto one axes."""
        x = np.linspace(0, 2 * np.pi, 100)
        fig = plt.Plot(x, np.sin(x))
        plt.Plot(x, np.cos(x), figure=fig, plot_style=dict(linestyle="dashed"))
        self.save_and_close(fig, "composite_plot.png")

    # endregion

    # region `Numputils` geometry helpers feeding `Plot`
    # (mirrors ci/tests/NumputilsTests.py::test_Arc / test_ParametricPath)

    def test_ArcPlot(self):
        """`nput.arc_points_from_endpoints` feeds directly into a `Plot` of the arc."""
        points, arc = nput.arc_points_from_endpoints(
            [.8, 0],
            [-.8, 0],
            radius=nput.vec_normalize([1, 2]) * 2,
            return_arc=True,
            clockwise=True,
            use_major_rotation=False,
            rotation=np.pi / 3
        )
        fig = plt.Plot(*points.T,
                        plot_range=[[-2, 2], [-2, 2]],
                        padding=[[0, 0], [0, 0]],
                        image_size=300,
                        aspect_ratio=1)
        self.save_and_close(fig, "arc_plot.png")

    def test_ParametricPathPlot(self):
        """`nput.parametric_path_points` stitches together Bezier/line/spline segments for `Plot`."""
        point = nput.parametric_path_points([
            ["BEZIER", [(0, 5), (5, 10), (10, 10)]],
            ["line", [(-5, 0), (-10, -5), (-10, -10)]],
            ["interp", [(0, 5), (5, 10), (10, 10)], {'k': 2}]
        ])
        fig = plt.Plot(*point.T)
        self.save_and_close(fig, "parametric_path_plot.png")

    def test_BezierCurvatureScatter(self):
        """`nput.bezier_eval`/`bezier_curvature` feed a curvature-colored `ScatterPlot`."""
        knots = np.array([
            [0, 0], [.1, 1], [.5, 2], [.8, 0], [1, 0], [1.2, 0], [2, 2]
        ])
        points, t = nput.bezier_eval(knots, 5, max_arc_len=.05, return_points=True)
        fig = plt.Plot(*points.T,
                        plot_range=[[0, 2], [0, 2]],
                        padding=[[0, 0], [0, 0]],
                        image_size=300,
                        aspect_ratio=1)
        plt.ScatterPlot(
            *points.T,
            color=plt.prep_color(
                palette="viridis",
                blending=nput.vec_rescale(nput.bezier_curvature(knots, t))
            ),
            figure=fig
        )
        self.save_and_close(fig, "bezier_curvature_scatter.png")

    # endregion


if __name__ == '__main__':
    unittest.main(verbosity=2)

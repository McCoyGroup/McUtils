"""Extracted from ZacharyTests.test_FD2D via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ZacharyTests.test_FD2D"""

try:
    from Peeves.TestUtils import *
    from Peeves import BlockProfiler, Timer
except:
    pass
from unittest import TestCase
from McUtils.Zachary import *
try:
    from McUtils.Zachary.Taylor.ZachLib import *
except ModuleNotFoundError:
    from McUtils.McUtils.Zachary.Taylor.ZachLib import *
from McUtils.Plots import *
import McUtils.Plots as plt
from McUtils.Data import *
import McUtils.Numputils as nput
from McUtils.Parallelizers import *
from McUtils.Scaffolding import Logger
import numpy.testing
import sys, h5py, math, numpy as np, itertools

class ZacharyTests(TestCase):

    def setUp(self):
        self.save_data = TestManager.data_gen_tests

    def __getstate__(self):
        return {}

    def __setstate__(self, state):
        pass

    def get_error(self, ref_vals, vals):
        err = np.abs(vals - ref_vals)
        cum_err = np.linalg.norm(err.flatten())
        max_err = np.max(err.flatten())
        mean_err = np.average(err.flatten())
        return (err, cum_err, max_err, mean_err)

    def plot_err(self, grid, ref_vals, vals, errs):
        if grid.ndim == 1:
            Plot(grid, ref_vals, figure=Plot(grid, vals))
            Plot(grid, errs[0]).show()
        elif grid.ndim == 3:
            g = (grid[:, :, 0], grid[:, :, 1])
            gg = GraphicsGrid(nrows=2, ncols=2)
            gg[0, 0] = ContourPlot(*g, ref_vals, figure=gg[0, 0])
            gg[1, 0] = ContourPlot(*g, vals, figure=gg[1, 0])
            gg[1, 1] = ContourPlot(*g, errs[0], figure=gg[1, 1])
            gg[0, 0].tight_layout()
            gg.show()

    def print_error(self, n, order, errs):
        print('Order: {}.{}\nCumulative Error: {}\nMax Error: {}\nMean Error: {}'.format(n, order, *errs[1:]))

    class harmonically_coupled_morse:

        def __init__(self, De_1, a_1, re_1, De_2, a_2, re_2, kb, b_e):
            self.De_1 = De_1
            self.a_1 = a_1
            self.re_1 = re_1
            self.De_2 = De_2
            self.a_2 = a_2
            self.re_2 = re_2
            self.kb = kb
            self.b_e = b_e

        def __call__(self, carts):
            v1 = carts[..., 1, :] - carts[..., 0, :]
            v2 = carts[..., 2, :] - carts[..., 0, :]
            r1 = nput.vec_norms(v1) - self.re_1
            r2 = nput.vec_norms(v2) - self.re_2
            bend, _ = nput.vec_angles(v1, v2)
            bend = bend - self.b_e
            return self.De_1 * (1 - np.exp(-self.a_1 * r1)) ** 2 + self.De_2 * (1 - np.exp(-self.a_2 * r2)) ** 2 + self.kb * bend ** 2

    @classmethod
    def constructSparseArray(cls, shape, n_els):
        from McUtils.Numputils import SparseArray
        np.random.seed(1)
        inds = np.unique(np.array([np.random.choice(x, n_els) for x in shape]).T, axis=0)
        vals = np.random.rand(len(inds))
        inds = inds.T
        return SparseArray.from_data((vals, inds), shape=shape)

    @validationTest
    def test_FD2D(self):
        print_error = False
        plot_error = False
        x_grid = np.linspace(0, np.pi, 200, dtype=np.longdouble)
        y_grid = np.linspace(0, np.pi, 100, dtype=np.longdouble)
        sin_x_vals = np.sin(x_grid)
        sin_y_vals = np.sin(y_grid)
        cos_x_vals = np.cos(x_grid)
        cos_y_vals = np.cos(y_grid)
        vals_2D = np.outer(sin_x_vals, sin_y_vals)
        grid_2D = np.array(np.meshgrid(x_grid, y_grid)).T
        test_11 = True
        if test_11:
            ref_vals = np.outer(cos_x_vals, cos_y_vals)
            for ord in range(3, 7, 2):
                n = (1, 1)
                vals = finite_difference(grid_2D, vals_2D, n, stencil=ord, end_point_accuracy=1)
                errs = self.get_error(ref_vals, vals)
                if plot_error:
                    self.plot_err(grid_2D, ref_vals, vals, errs)
                if print_error:
                    self.print_error(n, ord, errs)
                self.assertLess(errs[1], 0.1 / ord)
        test_12 = True
        if test_12:
            ref_vals = -np.outer(cos_x_vals, sin_y_vals)
            for ord in range(3, 7, 2):
                n = (1, 2)
                vals = finite_difference(grid_2D, vals_2D, n, stencil=ord, end_point_accuracy=1)
                errs = self.get_error(ref_vals, vals)
                if plot_error:
                    self.plot_err(grid_2D, ref_vals, vals, errs)
                if print_error:
                    self.print_error(n, ord, errs)
                self.assertLess(errs[1], 0.05 / ord)
        test_23 = True
        if test_23:
            only_core = True
            ref_vals = np.outer(sin_x_vals, cos_y_vals)
            for ord in range(5, 10):
                n = (2, 3)
                vals = finite_difference(grid_2D, vals_2D, n, stencil=ord, end_point_accuracy=2, only_core=True)
                floop = np.math.floor(ord / 2)
                if only_core:
                    refs = ref_vals[floop:-floop, floop:-floop]
                    grfs = grid_2D[floop:-floop, floop:-floop]
                else:
                    refs = ref_vals
                    grfs = grid_2D
                errs = self.get_error(refs, vals)
                if plot_error:
                    self.plot_err(grfs, refs, vals, errs)
                if print_error:
                    self.print_error(n, ord, errs)
                self.assertLess(errs[1], 0.05)
        test_14 = True
        if test_14:
            ref_vals = np.outer(cos_x_vals, sin_y_vals)
            only_core = True
            for ord in range(6, 8):
                n = (1, 4)
                vals = finite_difference(grid_2D, vals_2D, n, stencil=ord, end_point_accuracy=2, only_core=only_core)
                floop = np.math.floor(ord / 2)
                if only_core:
                    refs = ref_vals[floop:-floop, floop:-floop]
                    grfs = grid_2D[floop:-floop, floop:-floop]
                else:
                    refs = ref_vals
                    grfs = grid_2D
                errs = self.get_error(refs, vals)
                if plot_error:
                    self.plot_err(grfs, refs, vals, errs)
                if print_error:
                    self.print_error(n, ord, errs)
                self.assertLess(errs[1], 0.5)

"""Extracted from ZacharyTests.test_RBFForms via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ZacharyTests.test_RBFForms"""

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
    def test_RBFForms(self):

        def test_1D(fn, pts):
            base_interp = RBFDInterpolator.create_function_interpolation(pts.reshape((-1, 1)), lambda p, f=fn: f(p).flatten())
            g = np.linspace(np.min(pts) - 0.3, np.max(pts) + 0.3, 50)
            cp = plt.CompositePlot(plt.Plot(g, base_interp(g.reshape(-1, 1)), color='red'), plt.Plot(g, fn(g), color='green', linestyle='-'), plt.ScatterPlot(pts, fn(pts))).show(interactive=False)
            dinterp = RBFDInterpolator.create_function_interpolation(pts, lambda p, f=fn: f(p).reshape(-1), lambda p, f=fn.deriv(1): f(p).reshape(-1, 1), lambda p, f=fn.deriv(2): f(p).reshape(-1, 1, 1))
            itp = dinterp
            g = np.linspace(np.min(itp.grid) - 0.3, np.max(itp.grid) + 0.3, 50)
            cp = plt.CompositePlot(plt.Plot(g, itp(g.reshape(-1, 1)), color='red'), plt.Plot(g, fn(g), color='green', linestyle='dashed'), plt.ScatterPlot(pts, fn(pts))).show(interactive=False)
        sym = Symbols('xyz')
        np.random.seed(3)
        ndim = 2
        pts = np.random.uniform(low=-0.5, high=1.2, size=(10000, ndim))
        np.random.seed(3)
        new = np.random.uniform(low=-0.6, high=1.3, size=(500, ndim))
        for fn in [sym.morse(sym.x) * sym.morse(sym.y), sym.morse(sym.x) * sym.morse(sym.y) - sym.morse(sym.x) - sym.morse(sym.y)]:
            dinterp = RBFDInterpolator.create_function_interpolation(pts, fn, lambda p, f=fn.deriv(order=1): f(p).transpose(), lambda p, f=fn.deriv(order=2): f(p).transpose(2, 0, 1), clustering_radius=1e-05)
            vals = dinterp(new, deriv_order=2)
            print_errors = True
            val_diff = vals[0] - fn(new)
            if print_errors:
                print('avg diff:', np.average(val_diff))
                print('median diff:', np.median(val_diff))
                print('std diff:', np.std(val_diff))
            self.assertLess(np.abs(np.average(val_diff)), 0.01, msg='failed for {}'.format(fn))
            self.assertLess(np.std(val_diff), 0.05, msg='failed for {}'.format(fn))
            grad_diff = vals[1] - fn.deriv(order=1)(new).T
            if print_errors:
                print('avg grad diff:', np.average(grad_diff))
                print('median grad diff:', np.median(grad_diff))
                print('std grad diff:', np.std(grad_diff))
            self.assertLess(np.abs(np.average(grad_diff)), 0.05, msg='failed for {}'.format(fn))
            self.assertLess(np.std(grad_diff), 0.2, msg='failed for {}'.format(fn))
            hess_diff = vals[2] - fn.deriv(order=2)(new).transpose(2, 0, 1)
            if print_errors:
                print('avg hess diff:', np.average(hess_diff))
                print('median hess diff:', np.median(hess_diff))
                print('std hess diff:', np.std(hess_diff))
            self.assertLess(np.abs(np.average(hess_diff)), 0.2, msg='failed for {}'.format(fn))
            self.assertLess(np.std(hess_diff), 0.8, msg='failed for {}'.format(fn))

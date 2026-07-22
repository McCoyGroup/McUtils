"""Extracted from ZacharyTests.test_RBFInterpolatorResiliance via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ZacharyTests.test_RBFInterpolatorResiliance"""

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
    def test_RBFInterpolatorResiliance(self):
        np.random.seed(1)
        npts = 1000
        ndim = 2
        pts = np.random.uniform(low=-np.pi / 2, high=np.pi / 2, size=(npts, ndim))
        og = pts
        vals = og_vals = np.product(np.sin(pts), axis=1)
        dvals_x = np.sin(pts[:, 1]) * np.cos(pts[:, 0])
        dvals_y = np.sin(pts[:, 0]) * np.cos(pts[:, 1])
        dvals = np.array([dvals_x, dvals_y]).T
        og_d = dvals
        dvals_xx = -np.sin(pts[:, 0]) * np.sin(pts[:, 1])
        dvals_xy = np.cos(pts[:, 1]) * np.cos(pts[:, 0])
        dvals_yy = -np.sin(pts[:, 1]) * np.sin(pts[:, 0])
        d2vals = np.moveaxis(np.array([[dvals_xx, dvals_xy], [dvals_xy, dvals_yy]]), -1, 0)
        og_dd = d2vals
        interp = RBFDInterpolator(pts, vals, dvals, d2vals, kernel='thin_plate_spline', clustering_radius=0.01, multicenter_monomials=True)
        test_vals = interp(pts, neighbors=15, zero_tol=-1, resiliance_test_options={})

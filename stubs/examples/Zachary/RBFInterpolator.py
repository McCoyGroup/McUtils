"""Extracted from ZacharyTests.test_RBFInterpolator via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ZacharyTests.test_RBFInterpolator"""

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
    def test_RBFInterpolator(self):
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
        pts = interp.grid
        vals = np.product(np.sin(pts), axis=1)
        dvals_x = np.sin(pts[:, 1]) * np.cos(pts[:, 0])
        dvals_y = np.sin(pts[:, 0]) * np.cos(pts[:, 1])
        dvals = np.array([dvals_x, dvals_y]).T
        dvals_xx = -np.sin(pts[:, 0]) * np.sin(pts[:, 1])
        dvals_xy = np.cos(pts[:, 1]) * np.cos(pts[:, 0])
        dvals_yy = -np.sin(pts[:, 1]) * np.sin(pts[:, 0])
        d2vals = np.moveaxis(np.array([[dvals_xx, dvals_xy], [dvals_xy, dvals_yy]]), -1, 0)
        test_vals = interp(pts[:2], neighbors=15)
        real = np.product(np.sin(pts[:2]), axis=1)
        self.assertTrue(np.allclose(test_vals, real, atol=0.001, rtol=0.01), msg='bad interpolation at interpolation points \n {} \nvs\n {}'.format(test_vals, real))
        h = 0.001
        test_pts = pts[:3] + np.array([[0, h]] * 3)
        extrap = interp(test_pts, neighbors=15, zero_tol=-1)
        true = np.product(np.sin(test_pts), axis=1)
        self.assertTrue(np.allclose(extrap, true, atol=h), msg='bad extrapolation at pts: {} \nerr: {} in \n{} \nvs\n {}'.format(test_pts, extrap - true, extrap, true))
        test_pts = pts[:10]
        dervs = interp(test_pts, neighbors=15, deriv_order=1, zero_tol=-1)[1]
        reals = np.array([dvals_x, dvals_y]).T[:10]
        test_vals = vals[:10]
        self.assertTrue(np.allclose(dervs, reals, atol=0.1), msg='bad deriv interpolation at interpolation points \nerror: {} in\n{} \nvs\n {}'.format(dervs - reals, dervs, reals))
        np.random.seed(0)
        test_vals = np.unique(np.random.randint(0, len(pts) - 1, size=200))
        errors = [[], [], []]
        print_errors = False
        h = 0.1
        for ifun in [lambda x, **kw: interp(x, neighbors=25, **kw)]:
            for n, p in enumerate(pts[test_vals]):
                c = p[np.newaxis] + h
                test = ifun(c, reshape_derivatives=False, deriv_order=2)
                real = [np.sin(c[:, 0]) * np.sin(c[:, 1]), np.array([np.sin(c[:, 1]) * np.cos(c[:, 0]), np.sin(c[:, 0]) * np.cos(c[:, 1])]).T, np.array([-np.sin(c[:, 0]) * np.sin(c[:, 1]), np.cos(c[:, 1]) * np.cos(c[:, 0]), -np.sin(c[:, 1]) * np.sin(c[:, 0])]).T]
                if print_errors:
                    print('-' * 20 + '  ', n, ': ', c, '  ' + '-' * 20)
                for n, (t, r) in enumerate(zip(test, real)):
                    rel_error = 2 * (t - r) / (np.abs(t) + np.abs(r))
                    if print_errors:
                        print(t, r, t - r)
                        print('>', rel_error)
                    errors[n].append(rel_error)
            maes = [np.average(np.abs(x), axis=None) for x in errors]
            tols = [h, 3 * h, 10 * h]
            for n, (t, e) in enumerate(zip(tols, maes)):
                self.assertLess(e, t, msg='at order {} MRE {} > {}'.format(n, e, t))

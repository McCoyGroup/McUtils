"""Extracted from ZacharyTests.test_TensorDerivatives via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ZacharyTests.test_TensorDerivatives"""

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
    def test_TensorDerivatives(self):

        def plus_1(x):
            return x + 1
        crds = TensorExpression.ScalarFunctionTerm(TensorExpression.CoordinateVector(2, name='coord_vec'), f={'function': plus_1, 'derivatives': lambda inds: (lambda *_: 1) if isinstance(inds, int) or len(inds) == 1 else lambda *_: 0})
        expr = TensorExpression.OuterPowerTerm(crds, 2)
        e2 = TensorExpression.OuterPowerTerm(TensorExpression.ScalarFunctionTerm(TensorExpression.CoordinateVector([1, 2], name='coord_vec'), f={'function': plus_1, 'derivatives': lambda inds: (lambda *_: 1) if isinstance(inds, int) or len(inds) == 1 else lambda *_: 0}), 2)
        self.assertTrue(np.allclose(TensorExpression(expr.dQ(), coord_vec=np.array([1, 2])).eval(), e2.dQ().array))
        nv = TensorExpression.VectorNormTerm(TensorExpression.CoordinateVector(2, name='coord_vec'))
        self.assertEquals(TensorExpression(nv, coord_vec=np.array([1, 2])).eval(), np.linalg.norm([1, 2]))
        self.assertTrue(np.allclose(TensorExpression(nv.dQ().dQ(), coord_vec=np.array([1, 2])).eval(), [[0.357771, -0.178885], [-0.178885, 0.0894427]]))
        np.random.seed(0)
        crd = np.random.rand(5)
        wat = TensorExpression.VectorNormTerm(TensorExpression.CoordinateVector(5, name='coord_vec'))
        crd_vals = TensorExpression.ArrayStack((3,), np.array([crd, crd, crd]))
        res = TensorExpression(wat, coord_vec=crd_vals).eval()
        self.assertEquals(res.shape, (3,))
        wat_d = wat.dQ()
        dq_res = TensorExpression(wat_d, coord_vec=crd_vals).eval()
        self.assertEquals(dq_res.shape, (3, 5))
        slow_mode = np.array([TensorExpression(wat_d, coord_vec=x).eval() for x in crd_vals.array])
        self.assertTrue(np.allclose(dq_res, slow_mode))
        wat_dd = wat.dQ().dQ()
        dqq_res = TensorExpression(wat_dd, coord_vec=crd_vals).eval()
        self.assertEquals(dqq_res.shape, (3, 5, 5))
        slow_mode = np.array([TensorExpression(wat_dd, coord_vec=x).eval() for x in crd_vals.array])
        self.assertTrue(np.allclose(dqq_res, slow_mode))
        pts = np.array([[-0.32498609, -0.29857954], [-0.29112237, -0.48247142], [-0.19237367, -0.28342343], [-0.40490118, -0.2155546], [-0.31110323, -0.10724408]])
        pts = TensorExpression.ArrayStack((5,), pts)
        term = TensorExpression.OuterPowerTerm(TensorExpression.CoordinateVector(2, name='pts'), 2)
        self.assertEquals(TensorExpression(term.dQ(), pts=pts).eval().shape, (5, 2, 2, 2))
        pts = np.array([[-0.32498609, -0.29857954], [-0.29112237, -0.48247142], [-0.19237367, -0.28342343], [-0.40490118, -0.2155546], [-0.31110323, -0.10724408]])
        pts = TensorExpression.ArrayStack((5,), pts)
        term = TensorExpression.OuterPowerTerm(TensorExpression.CoordinateVector(2, name='pts'), 3)
        self.assertEquals(TensorExpression(term, pts=pts).eval().shape, (5, 2, 2, 2))

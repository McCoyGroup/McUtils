"""Extracted from ZacharyTests.test_PseudopotentialTerms via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ZacharyTests.test_PseudopotentialTerms"""

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
    def test_PseudopotentialTerms(self):
        n_Q = 10
        np.random.seed(1)
        n_X = 3
        i_derivs = [np.random.rand(n_X, n_X), np.random.rand(n_Q, n_X, n_X), np.random.rand(n_Q, n_Q, n_X, n_X), np.random.rand(n_Q, n_Q, n_Q, n_X, n_X)]
        i_terms = TensorExpansionTerms(i_derivs[1:], None, base_qx=i_derivs[0], q_name='I')
        detI = i_terms.QX(0).det()
        g_derivs = [np.random.rand(n_Q, n_Q), np.random.rand(n_Q, n_Q, n_Q), np.random.rand(n_Q, n_Q, n_Q, n_Q), np.random.rand(n_Q, n_Q, n_Q, n_Q, n_Q)]
        g_terms = TensorExpansionTerms(g_derivs[1:], None, base_qx=g_derivs[0], q_name='G')
        detG = g_terms.QX(0).det()
        self.assertIsInstance(detG.array, float)
        self.assertEquals(detG.array, np.linalg.det(g_derivs[0]))
        new_tr = g_terms.QX(0).tr()
        self.assertEquals(new_tr.array.shape, ())
        self.assertTrue(np.allclose(new_tr.array, np.trace(g_derivs[0])))
        new_inv = ~g_terms.QX(0)
        self.assertTrue(np.allclose(new_inv.array, np.linalg.inv(g_derivs[0])))
        newdQ = detG.dQ()
        self.assertEquals(newdQ.array.shape, (n_Q,))
        i_derivs = [np.random.rand(n_X, n_X), np.random.rand(n_Q, n_X, n_X), np.random.rand(n_Q, n_Q, n_X, n_X), np.random.rand(n_Q, n_Q, n_Q, n_X, n_X)]
        i_terms = TensorExpansionTerms(i_derivs[1:], None, base_qx=i_derivs[0], q_name='I')
        detI = i_terms.QX(0).det()
        gam = detG / detI
        self.assertEquals(gam.array.shape, ())
        self.assertTrue(np.allclose(gam.array, detG.array / detI.array))
        self.assertTrue(np.allclose(gam.array, np.linalg.det(g_derivs[0]) / np.linalg.det(i_derivs[0])))
        five_gam = 5 * detG / detI
        self.assertAlmostEquals(five_gam.array, 5 * detG.array / detI.array, 8)
        inv_gam = 1 / gam
        self.assertEquals(inv_gam.array.shape, ())
        self.assertTrue(np.allclose(inv_gam.array, detI.array / detG.array))
        self.assertEquals(inv_gam.array, 1 / gam.array)
        gamdQ = gam.dQ().simplify(check_arrays=True)
        self.assertEquals(gamdQ.array.shape, (n_Q,))
        wat_2 = g_terms.QX(1).dot(gamdQ, 3, 1).tr()
        self.assertEquals(wat_2.array.shape, ())
        wat_21 = g_terms.QX(2).tr(axis1=1, axis2=4)
        self.assertEquals(wat_21.array.shape, (n_Q, n_Q))
        self.assertTrue(np.allclose(wat_21.array, np.trace(g_derivs[2], axis1=0, axis2=3)))
        doot = gamdQ.dot(g_terms.QX(0), 1, 1)
        self.assertEquals(doot.array.shape, (n_Q,))
        wat_3 = -3 / 4 * gamdQ.dot(doot, 1, 1)
        self.assertEquals(wat_3.array.shape, ())
        wat_4 = -3 / 4 * inv_gam * gamdQ.dot(doot, 1, 1)
        self.assertEquals(wat_4.array.shape, ())
        wat_5 = inv_gam * wat_3
        self.assertTrue(np.allclose(wat_4.array, wat_5.array))
        I0, I0Q, I0QQ = i_derivs[:3]
        G, GQ, GQQ = g_derivs[:3]
        detI = np.linalg.det(I0)
        invI = np.linalg.inv(I0)
        adjI = invI * detI
        detG = np.linalg.det(G)
        invG = np.linalg.inv(G)
        adjG = invG * detG
        invIdQ_new = i_terms.QX(0).inverse().dQ()
        invIdQ = -np.tensordot(np.tensordot(invI, I0Q, axes=[-1, 1]), invI, axes=[-1, 0]).transpose(1, 0, 2)
        self.assertEquals(invIdQ_new.array.shape, invIdQ.shape)
        self.assertTrue(np.allclose(invIdQ_new.array, invIdQ))
        invGdQ = -np.tensordot(np.tensordot(invG, GQ, axes=[-1, 1]), invG, axes=[-1, 0]).transpose(1, 0, 2)
        nQ = GQ.shape[0]
        detIdQ = np.array([np.trace(np.dot(adjI, I0Q[i])) for i in range(nQ)])
        detIdQ2 = np.trace(np.tensordot(adjI, I0Q, axes=[1, 1]), axis1=0, axis2=2)
        detI_new = i_terms.QX(0).det()
        detIdQ_new = detI_new.dQ()
        self.assertTrue(np.allclose(detIdQ2, detIdQ))
        self.assertEquals(detIdQ_new.array.shape, detIdQ.shape)
        self.assertTrue(np.allclose(detIdQ_new.array, detIdQ))
        detGdQ = np.array([np.trace(np.dot(adjG, GQ[i])) for i in range(nQ)])
        detG_new = g_terms.QX(0).det()
        detGdQ_new = detG_new.dQ()
        self.assertEquals(detGdQ_new.array.shape, detGdQ.shape)
        self.assertTrue(np.allclose(detGdQ_new.array, detGdQ))
        gamdQ = (detI_new.dQ() / detI_new + -1 * detG_new.dQ() / detG_new).simplify(check_arrays=True)
        detI_new.name = '|I|'
        gamdQ_I_new = (detI_new.dQ() / detI_new).simplify(check_arrays=True)
        gamdQ_I = 1 / detI * detIdQ
        gamdQ_G = 1 / detG * detGdQ
        gamdQ_og = gamdQ_I - gamdQ_G
        self.assertTrue(np.allclose(gamdQ.array, gamdQ_og))
        adjIdQ = detI * invIdQ + detIdQ[:, np.newaxis, np.newaxis] * invI[np.newaxis, :, :]
        np.array([np.trace(np.dot(adjI, I0Q[i])) for i in range(nQ)])
        detIdQQ = np.array([[np.tensordot(I0Q[i], adjIdQ[j].T, axes=2) + np.tensordot(adjI, I0QQ[i, j].T, axes=2) for i in range(nQ)] for j in range(nQ)])
        detIdQQ_real = np.array([[np.trace(np.dot(I0Q[i], adjIdQ[j])) + np.trace(np.dot(adjI, I0QQ[i, j])) for i in range(nQ)] for j in range(nQ)])
        detIdQQ2_terms = [np.tensordot(I0Q, adjIdQ, axes=[[1, 2], [2, 1]]).T, np.tensordot(adjI, I0QQ, axes=[[1, 0], [2, 3]]).T]
        detIdQQ2 = np.sum(detIdQQ2_terms, axis=0)
        detIdQQ_new = detIdQ_new.dQ().simplify(check_arrays=True)
        adjI_new = i_terms.QX(0).det() * i_terms.QX(0).inverse()
        self.assertTrue(np.allclose(adjI_new.array, adjI))
        adjIdQ_new = adjI_new.dQ().simplify()
        self.assertTrue(np.allclose(adjIdQ_new.array, adjIdQ))
        self.assertTrue(np.allclose(detIdQQ2, detIdQQ))
        self.assertEquals(detIdQQ_new.array.shape, detIdQQ.shape)
        self.assertTrue(np.allclose(detIdQQ_new.array.T, detIdQQ))
        gamdQQ_I = -1 / detI ** 2 * np.outer(detIdQ, detIdQ) + 1 / detI * detIdQQ
        gamdQQ_I_new = gamdQ_I_new.dQ().simplify(check_arrays=True)
        self.assertTrue(np.allclose(gamdQQ_I_new.array.T, gamdQQ_I))

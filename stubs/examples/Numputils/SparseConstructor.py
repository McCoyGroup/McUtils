"""Extracted from NumputilsTests.test_SparseConstructor via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest NumputilsTests.test_SparseConstructor"""

import collections
import itertools
import math
import os.path
from Peeves.TestUtils import *
from Peeves import BlockProfiler
import McUtils.Numputils as nput
from McUtils.Numputils import *
from McUtils.Zachary import FiniteDifferenceDerivative
from unittest import TestCase
import numpy as np, scipy, functools as ft

class NumputilsTests(TestCase):
    problem_coords = np.array([[-1.86403557e-17, -0.076046524, 0.0462443228], [6.70904773e-17, -0.076046524, -0.953755677], [0.929682337, 0.292315732, 0.0462443228], [2.46519033e-32, -1.38777878e-17, 0.225076602], [-1.97215226e-31, 1.4371441, -0.90030641], [-1.75999392e-16, -1.4371441, -0.90030641]])

    @classmethod
    def setUp(self):
        np.set_printoptions(linewidth=100000000.0)

    @validationTest
    def test_SparseConstructor(self):
        shape = (1000, 100, 50)
        n_els = 100
        np.random.seed(1)
        inds = np.unique(np.array([np.random.choice(x, n_els) for x in shape]).T, axis=0)
        vals = np.random.rand(len(inds))
        inds = inds.T
        array = SparseArray.from_data((vals, inds), shape=shape)
        self.assertEquals(array.shape, shape)
        block_vals, block_inds = array.block_data
        self.assertEquals(len(block_vals), len(vals))
        self.assertEquals(np.sort(block_vals).tolist(), np.sort(vals).tolist())
        for i in range(len(shape)):
            self.assertEquals(np.sort(block_inds[i]).tolist(), np.sort(inds[i]).tolist())
        woof = array[:, 1, 1]
        self.assertIs(type(woof), type(array))
        self.assertEquals(woof.shape, (shape[0],))
        block_vals, block_inds = woof.block_data
        filt_pos = np.where(np.logical_and(inds[1] == 1, inds[2] == 1))
        if len(filt_pos) > 0:
            self.assertEquals(np.sort(block_vals).tolist(), np.sort(vals[filt_pos]).tolist())
        shape = (28, 3003)
        n_els = 10000
        np.random.seed(1)
        inds = np.unique(np.array([np.random.choice(x, n_els) for x in shape]).T, axis=0)
        vals = np.random.rand(len(inds))
        inds = inds.T
        array = SparseArray.from_data((vals, inds), shape=shape)
        woof = array[0, :]
        self.assertIs(type(woof), type(array))
        self.assertEquals(woof.shape, (shape[1],))
        block_vals, block_inds = woof.block_data
        filt_pos = np.where(inds[0] == 0)
        if len(filt_pos) > 0:
            self.assertEquals(np.sort(block_vals).tolist(), np.sort(vals[filt_pos]).tolist())
        woof = array[(0, 2), :]
        self.assertEquals(woof.shape, (2, shape[1]))
        block_vals, block_inds = woof.block_data
        filt_pos = np.where(np.logical_or(inds[0] == 0, inds[0] == 2))
        if len(filt_pos) > 0:
            self.assertEquals(np.sort(block_vals).tolist(), np.sort(vals[filt_pos]).tolist())
            self.assertEquals(block_vals[:10].tolist(), [0.26762682146970584, 0.3742446513095977, 0.11369722324344822, 0.4860704109280778, 0.09299008335958303, 0.11229999691948178, 0.0005348158154161453, 0.7711636892670307, 0.6573053253883241, 0.39084691369185387])
        n_els = 1000
        inds_2 = np.unique(np.array([np.random.choice(x, n_els) for x in shape]).T, axis=0)
        vals_2 = np.random.rand(len(inds_2))
        inds_2 = inds_2.T
        array_2 = SparseArray.from_data((vals_2, inds_2), shape=shape)
        meh = array.dot(array_2.transpose((1, 0)))
        self.assertTrue(np.allclose(meh.asarray(), np.dot(array.asarray(), array_2.asarray().T), 3))
        n_els = 1000
        inds_3 = np.unique(np.array([np.random.choice(x, n_els) for x in shape]).T, axis=0)
        vals_3 = np.random.rand(len(inds_3))
        inds_3 = inds_3.T
        array_3 = SparseArray.from_data((vals_3, inds_3), shape=shape)
        new2 = array_2.concatenate(array_3)
        meh = np.concatenate([array_2.asarray(), array_3.asarray()], axis=0)
        self.assertEquals(new2.shape, meh.shape)
        self.assertTrue(np.allclose(new2.asarray(), meh), msg='concat failed: (ref) {} vs {}'.format(meh, new2.asarray()))
        new2 = array_2.concatenate(array_3, array_2)
        meh = np.concatenate([array_2.asarray(), array_3.asarray(), array_2.asarray()], axis=0)
        self.assertEquals(new2.shape, meh.shape)
        self.assertTrue(np.allclose(new2.asarray(), meh), msg='concat many failed: (ref) {} vs {}'.format(meh, new2.asarray()))
        new3 = array_2.concatenate(array_2, array_3, axis=1)
        meh = np.concatenate([array_2.asarray(), array_2.asarray(), array_3.asarray()], axis=1)
        self.assertEquals(new3.shape, meh.shape)
        self.assertTrue(np.allclose(new3.asarray(), meh), msg='concat along 1 failed: (ref) {} vs {}'.format(meh, new3.asarray()))
        new_shape = [1, shape[1]]
        n_els = 1000
        inds_3 = np.unique(np.array([np.random.choice(x, n_els) for x in new_shape]).T, axis=0)
        vals_3 = np.random.rand(len(inds_3))
        inds_3 = inds_3.T
        array_3 = SparseArray.from_data((vals_3, inds_3), shape=new_shape)
        new2 = array_3.concatenate(array_2)
        meh = np.concatenate([array_3.asarray(), array_2.asarray()], axis=0)
        self.assertEquals(new2.shape, meh.shape)
        self.assertTrue(np.allclose(new2.asarray(), meh), msg='concat failed: (ref) {} vs {}'.format(meh, new2.asarray()))
        new2 = array_2.concatenate(array_3)
        meh = np.concatenate([array_2.asarray(), array_3.asarray()], axis=0)
        self.assertEquals(new2.shape, meh.shape)
        self.assertTrue(np.allclose(new2.asarray(), meh), msg='concat failed: (ref) {} vs {}'.format(meh, new2.asarray()))
        new2 = array_2.concatenate(array_3, array_2)
        meh = np.concatenate([array_2.asarray(), array_3.asarray(), array_2.asarray()], axis=0)
        self.assertEquals(new2.shape, meh.shape)
        self.assertTrue(np.allclose(new2.asarray(), meh), msg='concat many failed: (ref) {} vs {}'.format(meh, new2.asarray()))
        array_3 = array_3[:, :2500].reshape((1, 2500))
        array_3 = array_3.reshape((array_3.shape[1] // 2, 2))
        new2 = array_3.concatenate(array_3)
        meh = np.concatenate([array_3.asarray(), array_3.asarray()], axis=0)
        self.assertEquals(new2.shape, meh.shape)
        self.assertTrue(np.allclose(new2.asarray(), meh), msg='concat failed: (ref) {} vs {}'.format(meh, new2.asarray()))
        new2 = array_3.concatenate(array_3, axis=1)
        meh = np.concatenate([array_3.asarray(), array_3.asarray()], axis=1)
        self.assertEquals(new2.shape, meh.shape)
        self.assertTrue(np.allclose(new2.asarray(), meh), msg='concat failed: (ref) {} vs {}'.format(meh, new2.asarray()))
        new_shape = [shape[1]]
        n_els = 1000
        inds_3 = np.unique(np.array([np.random.choice(x, n_els) for x in new_shape]).T, axis=0)
        vals_3 = np.random.rand(len(inds_3))
        inds_3 = inds_3.T
        array_3 = SparseArray.from_data((vals_3, inds_3), shape=new_shape)
        new2 = array_3.concatenate(array_3)
        meh = np.concatenate([array_3.asarray(), array_3.asarray()], axis=0)
        self.assertEquals(new2.shape, meh.shape)
        self.assertTrue(np.allclose(new2.asarray(), meh), msg='concat failed: (ref) {} vs {}'.format(meh, new2.asarray()))
        wtf_array1 = SparseArray.from_data(([-0.00045906, -0.00045906, -0.00045906, -0.00045906, -0.00045906, -0.00045906], ((0, 24, 51, 78, 109, 140),)), shape=(155,))
        wtf_array2 = SparseArray.from_data(([-0.00045906, -0.00045906, -0.00045906, -0.00045906], ([16, 53, 88, 123],)), shape=(155,))
        new2 = wtf_array1.concatenate(wtf_array2)
        meh = np.concatenate([wtf_array1.asarray(), wtf_array2.asarray()])
        self.assertTrue(np.allclose(new2.asarray(), meh), msg='concat failed: (ref) {} vs {}'.format(meh, new2.asarray()))

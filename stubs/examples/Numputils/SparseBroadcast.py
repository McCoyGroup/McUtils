"""Extracted from NumputilsTests.test_SparseBroadcast via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest NumputilsTests.test_SparseBroadcast"""

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
    def test_SparseBroadcast(self):
        shape = (10, 100, 50)
        n_els = 8
        np.random.seed(1)
        inds = np.unique(np.array([np.random.choice(x, n_els) for x in shape]).T, axis=0)
        vals = np.random.rand(len(inds))
        inds = inds.T
        array = SparseArray.from_data((vals, inds), shape=shape)
        darr = array.asarray()
        exp_a = array.expand_dims([1, 2])
        self.assertTrue(np.allclose(exp_a.asarray(), np.expand_dims(darr, [1, 2])))
        parr = array.pad_right((0, 3, 0))
        self.assertTrue(np.allclose(parr.block_data[0], array.block_data[0]))
        self.assertTrue(np.allclose(parr.block_data[1], array.block_data[1]), msg='inds broken')
        self.assertTrue(np.allclose(parr.asarray(), np.pad(darr, [[0, 0], [0, 3], [0, 0]])), msg='padding broken')
        exp_a = array.expand_and_pad([1, 2], [0, 4, 4, 0, 0])
        self.assertTrue(np.allclose(exp_a.asarray(), np.pad(np.expand_dims(darr, [1, 2]), [[0, 0], [0, 4], [0, 4], [0, 0], [0, 0]])))
        for j in range(3):
            dense = np.broadcast_to(np.expand_dims(darr, j), shape[:j] + (100,) + shape[j:])
            sparse = array.reshape(shape[:j] + (1,) + shape[j:]).broadcast_to(shape[:j] + (100,) + shape[j:])
            self.assertTrue(np.allclose(dense, sparse.asarray()))

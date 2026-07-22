"""Extracted from NumputilsTests.test_SparseArray via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest NumputilsTests.test_SparseArray"""

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
    def test_SparseArray(self):
        array = SparseArray([[[1, 0, 0], [0, 0, 1], [0, 1, 0]], [[0, 0, 1], [0, 1, 0], [1, 0, 0]], [[0, 1, 0], [1, 0, 1], [0, 0, 1]], [[1, 1, 0], [1, 0, 1], [0, 1, 1]]])
        self.assertEquals(array.shape, (4, 3, 3))
        tp = array.transpose((1, 0, 2))
        self.assertEquals(tp.shape, (3, 4, 3))
        self.assertLess(np.linalg.norm((tp.asarray() - array.asarray().transpose((1, 0, 2))).flatten()), 1e-08)
        self.assertEquals(array[2, :, 2].shape, (3,))
        td = array.tensordot(array, axes=[1, 1])
        self.assertEquals(td.shape, (4, 3, 4, 3))
        self.assertEquals(array.tensordot(array, axes=[[1, 2], [1, 2]]).shape, (4, 4))

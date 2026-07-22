"""Extracted from NumputilsTests.test_SetOps via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest NumputilsTests.test_SetOps"""

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
    def test_SetOps(self):
        unums, sorting = unique([1, 2, 3, 4, 5])
        self.assertEquals(unums.tolist(), [1, 2, 3, 4, 5])
        self.assertEquals(sorting.tolist(), [0, 1, 2, 3, 4])
        unums, sorting = unique([1, 1, 3, 4, 5])
        self.assertEquals(unums.tolist(), [1, 3, 4, 5])
        self.assertEquals(sorting.tolist(), [0, 1, 2, 3, 4])
        unums, sorting = unique([1, 3, 1, 1, 1])
        self.assertEquals(unums.tolist(), [1, 3])
        self.assertEquals(sorting.tolist(), [0, 2, 3, 4, 1])
        unums, sorting = unique([[1, 3], [1, 1], [1, 3]])
        self.assertEquals(unums.tolist(), [[1, 1], [1, 3]])
        self.assertEquals(sorting.tolist(), [1, 0, 2])
        inters, sortings, merge = intersection([1, 1, 3, 2, 5], [0, 0, 0, 5, 1])
        self.assertEquals(inters.tolist(), [1, 5])
        self.assertEquals(sortings[0].tolist(), [0, 1, 3, 2, 4])
        self.assertEquals(sortings[1].tolist(), [0, 1, 2, 4, 3])
        inters, sortings, merge = intersection([[1, 3], [1, 1]], [[1, 3], [0, 0]])
        self.assertEquals(inters.tolist(), [[1, 3]])
        self.assertEquals(sortings[0].tolist(), [1, 0])
        self.assertEquals(sortings[1].tolist(), [1, 0])
        diffs, sortings, merge = difference([1, 1, 3, 2, 5], [0, 0, 0, 5, 1])
        self.assertEquals(diffs.tolist(), [2, 3])
        self.assertEquals(sortings[0].tolist(), [0, 1, 3, 2, 4])
        self.assertEquals(sortings[1].tolist(), [0, 1, 2, 4, 3])
        diffs, sortings, merge = contained([1, 1, 3, 2, 5], [0, 0, 0, 5, 1])
        self.assertEquals(diffs.tolist(), [True, True, False, False, True])
        ugh = np.arange(1000)
        bleh = np.random.choice(1000, size=100)
        diffs, sortings, merge = contained(bleh, ugh)
        self.assertEquals(diffs.tolist(), np.isin(bleh, ugh).tolist())
        diffs2, sortings, merge = contained(bleh, ugh, method='find')
        self.assertEquals(diffs.tolist(), diffs2.tolist())

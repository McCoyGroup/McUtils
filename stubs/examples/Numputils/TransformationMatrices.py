"""Extracted from NumputilsTests.test_TransformationMatrices via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest NumputilsTests.test_TransformationMatrices"""

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
    def test_TransformationMatrices(self):
        ax = vec_normalize(np.random.rand(3))
        test_rot = rotation_matrix(ax, np.pi / 7)
        purrf = reflection_matrix(ax)
        refl = test_rot @ purrf
        scalings, types, axes, roots, orders = identify_cartesian_transformation_type([test_rot, purrf, refl])
        self.assertEquals(types.tolist(), [2, 3, 4])
        rax = np.random.rand(4, 3, 3)
        scalings, types, axes, roots, orders = identify_cartesian_transformation_type(rax)
        tf = cartesian_transformation_from_data(scalings, types, axes, roots, orders)
        self.assertLess(np.max(np.abs(tf - rax)), 0.01)

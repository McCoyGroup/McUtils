"""Extracted from NumputilsTests.test_skewRotationMatrix via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest NumputilsTests.test_skewRotationMatrix"""

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
    def test_skewRotationMatrix(self):
        for _ in range(10):
            ut = np.random.rand(3)
            U1 = rotation_matrix_skew(ut)
            U2 = scipy.linalg.expm(skew_symmetric_matrix(ut))
            self.assertTrue(np.allclose(U1, U2))
        ut = np.random.rand(3)
        reference_rotation = rotation_matrix_skew(ut)
        ref_struct = np.array([[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]])
        rot_struct = ref_struct @ reference_rotation

        def mat_fun(upper_triangle):
            test_rot = rotation_matrix_skew(upper_triangle)
            test_struct = rot_struct @ test_rot
            return np.linalg.norm(ref_struct - test_struct)
        x = np.random.rand(3)
        for _ in range(10):
            opt = scipy.optimize.minimize(mat_fun, x, method='Nelder-Mead', tol=1e-08)
            x = opt.x
        print(opt)
        print('-' * 20)
        print('Upper Triangle:', ut)
        print(reference_rotation.T)
        print('-' * 20)
        test_rot = rotation_matrix_skew(opt.x)
        print('Upper Triangle:', opt.x)
        print(test_rot)
        print('-' * 20)
        print(ref_struct)
        print(rot_struct @ test_rot)
        self.assertLess(opt.fun, 1e-06)

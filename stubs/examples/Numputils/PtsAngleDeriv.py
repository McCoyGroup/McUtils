"""Extracted from NumputilsTests.test_PtsAngleDeriv via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest NumputilsTests.test_PtsAngleDeriv"""

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
    def test_PtsAngleDeriv(self):
        np.random.seed(0)
        coords = np.random.rand(16, 3)
        angs, derivs, derivs_2 = angle_deriv(coords, [5, 5], [4, 6], [6, 4], order=2)
        ang = angs[0]
        deriv = derivs[:, 0, :]
        deriv_2 = derivs_2[:, :, 0, :, :]
        ang2 = vec_angles(coords[4] - coords[5], coords[6] - coords[5])[0]
        self.assertEquals(ang2, ang)
        fd = FiniteDifferenceDerivative(lambda pt: vec_angles(pt[..., 1, :] - pt[..., 0, :], pt[..., 2, :] - pt[..., 0, :])[0], function_shape=((None, 3), 0), mesh_spacing=1e-05)
        fd1, fd2 = fd(coords[(5, 4, 6),]).derivative_tensor([1, 2])
        self.assertTrue(np.allclose(deriv.flatten(), fd1.flatten()), msg="{} and {} aren't close".format(deriv.flatten(), fd1.flatten()))
        d2_flat = np.concatenate([np.concatenate([deriv_2[0, 0], deriv_2[0, 1], deriv_2[0, 2]], axis=1), np.concatenate([deriv_2[1, 0], deriv_2[1, 1], deriv_2[1, 2]], axis=1), np.concatenate([deriv_2[2, 0], deriv_2[2, 1], deriv_2[2, 2]], axis=1)], axis=0)
        self.assertTrue(np.allclose(d2_flat.flatten(), fd2.flatten(), atol=0.001), msg='d2: {} and {} differ'.format(d2_flat.flatten(), fd2.flatten()))

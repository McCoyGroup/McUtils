"""Extracted from NumputilsTests.test_AngleDerivs via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest NumputilsTests.test_AngleDerivs"""

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
    def test_AngleDerivs(self):
        np.random.seed(0)
        coords = np.random.rand(16, 3)
        a = coords[4] - coords[5]
        b = coords[6] - coords[5]
        ang, dang, ddang = vec_angle_derivs(np.array([a, b]), np.array([b, a]), order=2)
        ang_2 = vec_angles(a, b)[0]
        self.assertEquals(ang_2, ang.flatten()[0])
        ang_fd = FiniteDifferenceDerivative(lambda vecs: vec_angles(vecs[..., 0, :], vecs[..., 1, :])[0], function_shape=((None, 2, 3), 0), mesh_spacing=0.0001)
        fd_ang_1, fd_dang_1 = ang_fd([a, b]).derivative_tensor([1, 2])
        fd_ang_2, fd_dang_2 = ang_fd([b, a]).derivative_tensor([1, 2])
        fd_ang = np.array([fd_ang_1, fd_ang_2])
        fd_dang = np.array([fd_dang_1, fd_dang_2])
        self.assertTrue(np.allclose(dang.flatten(), fd_ang.flatten()), msg='ang d1: {} and {} differ'.format(fd_ang.flatten(), fd_ang.flatten()))
        d2_flat = np.concatenate([np.concatenate([ddang[:, 0, 0], ddang[:, 0, 1]], axis=2), np.concatenate([ddang[:, 1, 0], ddang[:, 1, 1]], axis=2)], axis=1)
        self.assertTrue(np.allclose(d2_flat.flatten(), fd_dang.flatten(), atol=0.01), msg='ang d2: {} and {} differ ({})'.format(d2_flat.flatten(), fd_dang.flatten(), d2_flat.flatten() - fd_dang.flatten()))

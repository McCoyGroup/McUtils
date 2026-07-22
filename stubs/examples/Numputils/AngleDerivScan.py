"""Extracted from NumputilsTests.test_AngleDerivScan via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest NumputilsTests.test_AngleDerivScan"""

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

    @inactiveTest
    def test_AngleDerivScan(self):
        np.random.seed(0)
        a = np.array([1, 0, 0])
        fd = FiniteDifferenceDerivative(lambda vecs: vec_angle_derivs(vecs[..., 0, :], vecs[..., 1, :], up_vectors=up)[1], function_shape=((None, 2, 3), 0), mesh_spacing=0.0001)
        data = {'rotations': [], 'real_angles': [], 'angles': [], 'derivs': [], 'derivs2': [], 'derivs_num2': []}
        for q in np.linspace(-np.pi, np.pi, 601):
            up = np.array([0, 0, 1])
            r = rotation_matrix(up, q)
            b = np.dot(r, a)
            ang, deriv, deriv_2 = vec_angle_derivs(a, b, up_vectors=up, order=2)
            data['rotations'].append(q)
            data['real_angles'].append(vec_angles(a, b, up_vectors=up)[0])
            data['angles'].append(ang.tolist())
            data['derivs'].append(deriv.tolist())
            data['derivs2'].append(deriv_2.tolist())
            data['derivs_num2'].append(fd(np.array([a, b])).derivative_tensor(1).tolist())

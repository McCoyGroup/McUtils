"""Extracted from NumputilsTests.test_RotDerivs via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest NumputilsTests.test_RotDerivs"""

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
    def test_RotDerivs(self):
        np.random.seed(2123)
        coords = np.random.rand(15, 3)
        axis = nput.vec_normalize(np.random.rand(3))
        rot_gen = nput.axis_rot_gen_deriv(np.deg2rad(15), axis, 1)
        print(rot_gen[0])
        print(np.deg2rad(15), axis)
        print(rotation_matrix(axis, np.deg2rad(15)))
        rot_exp = nput.rotation_expansion_from_axis_angle(coords, axis)
        coords = np.array([[0.03741612, -0.01751408, 0.48282824], [1.871758, -0.33360481, -0.16993489], [-1.25575486, -1.37259928, -0.15862522], [-0.65341925, 1.72371818, -0.15426813]])
        import McUtils.Zachary as zach
        i, j, k, l = (0, 1, 3, 2)
        coords = coords[(i, j, k, l), :]
        rot_exp2 = np.array([nput.dist_expansion(coords, j, k, left_atoms=[i, j], right_atoms=[k, l])[1], nput.angle_expansion(coords, i, j, k, left_atoms=[i, j], right_atoms=[k, l])[1], nput.dihed_expansion(coords, i, j, k, l, left_atoms=[i, j], right_atoms=[k, l])[1]])
        rot_der2, _ = nput.internal_coordinate_tensors(coords, [(i, j), (j, k), (k, l), (i, j, k), (j, k, l), (i, j, k, l)], order=1, angle_ordering='ijk', return_inverse=True)
        print()
        print(np.round(rot_exp2 @ rot_der2[1], 8))

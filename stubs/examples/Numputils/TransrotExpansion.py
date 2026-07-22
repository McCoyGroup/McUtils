"""Extracted from NumputilsTests.test_TransrotExpansion via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest NumputilsTests.test_TransrotExpansion"""

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
    def test_TransrotExpansion(self):
        np.random.seed(2123)
        coords = np.random.rand(15, 3)
        masses = 1 + 2 * np.random.rand(15)
        _, exp = nput.internal_coordinate_tensors(coords, [{'orientation': ((0, 1, 2, 3), (5, 6, 7)), 'masses': masses}], return_inverse=True, masses=masses, remove_inverse_translation_rotation=True)
        rot_exp = nput.transrot_expansion(coords, 0, 1, 2, 3, extra_atoms=[5, 6, 7], masses=masses)
        rot_der = nput.transrot_deriv(coords, 0, 1, 2, 3, masses=masses)
        print()
        print(np.round(nput.tensor_reexpand(rot_exp[1:], rot_der[1:])[0], 8))
        rot_exp = nput.orientation_expansion(coords, (0, 1, 2, 3), (5, 6, 7), masses=masses)
        rot_der = nput.orientation_deriv(coords, (0, 1, 2, 3), (5, 6, 7), masses=masses)
        print(np.round(nput.tensor_reexpand(rot_exp[1:], rot_der[1:])[0], 8))
        i, j, k, l = (0, 1, 3, 2)
        rot_exp2 = [None, np.array([nput.dist_expansion(coords, j, k, left_atoms=[i, j], right_atoms=[k, l])[1], nput.angle_expansion(coords, i, j, k, left_atoms=[i, j], right_atoms=[k, l])[1], nput.dihed_expansion(coords, i, j, k, l, left_atoms=[i, j], right_atoms=[k, l])[1]])]
        rot_der2, _ = nput.internal_coordinate_tensors(coords, [(i, j), (j, k), (k, l), (i, j, k), (j, k, l), (i, j, k, l)], order=1, angle_ordering='ijk', return_inverse=True)
        concat_exp = [np.concatenate(p, axis=0) for p in zip(rot_exp[1:], rot_exp2[1:])]
        concat_der = [np.concatenate(p, axis=-1) for p in zip(rot_der[1:], rot_der2[1:])]
        print(np.round(nput.tensor_reexpand(concat_exp, concat_der)[0], 8).shape)
        print(np.round(nput.tensor_reexpand(concat_exp, concat_der)[0], 8))

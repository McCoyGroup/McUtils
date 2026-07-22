"""Extracted from NumputilsTests.test_EigenvectroDerivs via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest NumputilsTests.test_EigenvectroDerivs"""

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
    def test_EigenvectroDerivs(self):
        np.random.seed(2123)
        coords = np.random.rand(15, 3)
        masses = 1 + 2 * np.random.rand(15)
        inertia_base = nput.inertia_tensors(coords, masses=masses)
        inertia_higher = nput.inertial_frame_derivatives(coords, masses=masses, mass_weighted=False)
        inertia_expansion = [inertia_base] + inertia_higher

        def inert_t(coords):
            return nput.inertia_tensors(coords, masses=masses)
        dt = FiniteDifferenceDerivative(inert_t, ((15, 3), (3, 3)), mesh_spacing=0.001).derivatives(coords)
        val_exp, vec_exp = nput.mateigh_deriv(inertia_expansion, 1)
        nput.frac_powh([[1], [0], [0]], -1, nonzero_cutoff=0.01)

        def mom_i(coords):
            return moments_of_inertia(coords, masses=masses)[0]
        dt = FiniteDifferenceDerivative(mom_i, ((15, 3), (3,)), mesh_spacing=0.0001).derivatives(coords)

        def mom_ax(coords):
            return moments_of_inertia(coords, masses=masses)[1]
        dt = FiniteDifferenceDerivative(mom_ax, ((15, 3), (3, 3)), mesh_spacing=0.0001).derivatives(coords)
        a_exp, b_exp, c_exp = nput.orientation_angle_deriv(coords, (0, 1, 2, 3), (4, 5, 6), masses=masses, order=1)
        _ = nput.com_dist_deriv(coords, (0, 1, 2, 3), (4, 5, 6), masses=masses, order=1)

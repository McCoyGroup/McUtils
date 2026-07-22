"""Extracted from NumputilsTests.test_DerivPerf via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest NumputilsTests.test_DerivPerf"""

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
    def test_DerivPerf(self):
        from Psience.Molecools import Molecule
        import McUtils.Coordinerds as coordops
        test3 = Molecule.from_string('CC1(C)C(/C=C/C2=C(O)C=CC3=C2C=CC=C3)=[N+](CCCS(=O)([O-])=O)C4=CC=CC=C41')
        internal_set = coordops.extract_zmatrix_internals(test3.get_bond_zmatrix())
        internal_set = internal_set + internal_set + internal_set + internal_set
        with BlockProfiler():
            woof2 = nput.internal_coordinate_tensors(test3.coords, internal_set, masses=test3.masses, use_cache=False, reproject=True, order=1)
        with BlockProfiler():
            woof2 = nput.internal_coordinate_tensors(test3.coords, internal_set, masses=test3.masses, use_cache=False, reproject=False, order=1)
        with BlockProfiler():
            woof3 = nput.internal_coordinate_tensors(test3.coords, internal_set, masses=test3.masses, order=1)
        print(woof2[1] - woof3[1])

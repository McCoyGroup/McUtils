"""Extracted from ConverterTest.test_PsiAnglesToZMatrixAndBack via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ConverterTest.test_PsiAnglesToZMatrixAndBack"""

from Peeves.TestUtils import *
from Peeves.Timer import Timer
from Peeves import BlockProfiler
from unittest import TestCase
from McUtils.Coordinerds import *
import McUtils.Coordinerds as coordops
from McUtils.Plots import *
from McUtils.Numputils import *
import McUtils.Numputils as nput
import sys, numpy as np, os
import pprint

class ConverterTest(TestCase):

    def setUp(self):
        np.set_printoptions(linewidth=100000000.0)
        super().setUp()
        self.initialize_data()
        self.load()

    @property
    def loaded(self):
        return hasattr(self, 'cases')

    def load(self, n=10):
        if not self.loaded:
            self.cases = n
            self.transforms = DataGenerator.mats(n)
            self.shifts = DataGenerator.vecs(n)
            self.mats = affine_matrix(self.transforms, self.shifts)

    def initialize_data(self):
        self.n = 10
        self.test_zmats = CoordinateSet(DataGenerator.zmats(self.n, 15), system=ZMatrixCoordinates)
        self.test_carts = CoordinateSet(DataGenerator.multicoords(self.n, 10))
        self.test_structure = [[0.0, 0.0, 0.0], [0.5312106220949451, 0.0, 0.0], [0.054908987527698905, 0.5746865893353914, 0.0], [-0.06188515885294378, -0.024189926062338385, 0.4721688095375285], [0.0153308938205413, 0.3833690190410768, 0.23086294551212294], [0.1310095622893345, 0.30435650497612, 0.5316931774973834]]
        self.dihed_test_structure = np.array([[0.0, 0.0, 0.0], [-0.8247121421923925, -0.629530611338456, 1.775332267901544], [0.1318851447521099, 2.088940054609643, 0.0], [1.786540362044548, -1.386051328559878, 0.0], [2.233806981137821, 0.3567096955165336, 0.0], [-0.8247121421923925, -0.629530611338456, -1.775332267901544]])
        self.zm_conv_test_structure = np.array([[1.0, 0.0, 1.0], [-0.8247121421923925, -0.629530611338456, 1.775332267901544], [0.1318851447521099, 2.088940054609643, 0.0], [1.786540362044548, -1.386051328559878, 0.0], [2.233806981137821, 0.3567096955165336, 0.0], [-0.8247121421923925, -0.629530611338456, -1.775332267901544]])

    @inactiveTest
    def test_PsiAnglesToZMatrixAndBack(self):
        carts_OCHH = CoordinateSet([[[0.0, 0.0, 0.0], [0.0, 0.0, 1.22], [0.926647, 0.0, 1.755], [-0.926647, 0.0, 1.755]]] * 2, system=CartesianCoordinates3D)
        O1 = 0
        C1 = 1
        H1 = 2
        H2 = 3
        _ = -1
        zm_ochh = [[O1, _, _, _], [C1, O1, _, _], [H1, O1, C1, _], [H2, O1, C1, H1]]
        O1 = 1
        H1 = 0
        H2 = 2
        O2 = 3
        H3 = 4
        H4 = 5
        _ = -1
        zm_old = [[H1, _, _, _], [O1, H1, _, _], [H2, O1, H1, _], [O2, O1, H2, H1], [H3, O2, H2, H1], [H4, O2, H2, H1]]
        carts_old = CoordinateSet([[[0.89989, 1.851024, 0.0], [-0.000214, 1.516013, 0.0], [0.099753, 0.55259, 0.0], [-0.000214, -1.390289, -0.0], [-0.498111, -1.704705, 0.761032], [-0.498111, -1.704705, -0.761032]]] * 2, system=CartesianCoordinates3D)
        carts_new = CoordinateSet([[[0.0, 0.0, 0.0], [0.0, 0.0, 0.962259], [0.931459, 0.0, -0.241467], [-1.297691, -2.406089, -0.989477], [-2.033248, -2.168659, -1.55952], [-0.925486, -1.557192, -0.708516]]] * 2, system=CartesianCoordinates3D)
        O1 = 1
        H1 = 0
        H2 = 2
        O2 = 3
        H3 = 4
        H4 = 5
        _ = -1
        zm_old = [[H1, _, _, _], [O1, H1, _, _], [H2, O1, H1, _], [O2, O1, H2, H1], [H3, O2, H2, H1], [H4, O2, H2, H1]]
        O1 = 0
        H1 = 1
        H2 = 2
        O2 = 3
        H3 = 4
        H4 = 5
        _ = -1
        zm_new = [[O1, _, _, _], [H1, O1, _, _], [H2, O1, H1, _], [O2, O1, H1, H2], [H3, O2, O1, H2], [H4, O2, H3, O1]]
        carts = carts_new
        zm = zm_new
        zmat_system = ZMatrixCoordinateSystem(ordering=[x + [1] for x in zm])
        internals2 = carts.convert(zmat_system)
        carts2 = internals2.convert(CartesianCoordinates3D)
        print('<<<', np.round(carts[0], 3))
        print('<<<', np.round(carts2[0], 3))
        print('<==', np.round(np.rad2deg(internals2[0][:, 1:]), 3))
        carts2 = CoordinateSet(carts2, system=CartesianCoordinates3D)
        zmat_system = ZMatrixCoordinateSystem(ordering=[x + [1] for x in zm])
        internals3 = carts2.convert(zmat_system)
        print('<==', np.round(np.rad2deg(internals3[0][:, 1:]), 3))
        self.assertEqual(round(np.linalg.norm(carts - carts2), 8), 0.0)

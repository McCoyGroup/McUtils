"""Extracted from ConverterTest.test_ExpansionCoordinates via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ConverterTest.test_ExpansionCoordinates"""

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

    @validationTest
    def test_ExpansionCoordinates(self):
        np.random.seed(0)
        coord_set = CoordinateSet([self.test_structure] * 2)
        expansion_1 = np.random.rand(len(self.test_structure) * 3, len(self.test_structure) * 3)
        expansion_1 = expansion_1 / np.broadcast_to(np.linalg.norm(expansion_1, axis=0), expansion_1.shape)
        cs1 = CoordinateSystem('CartesianExpanded', basis=CartesianCoordinates3D, matrix=expansion_1)
        expansion_2 = np.random.rand((len(self.test_structure) - 1) * 3, (len(self.test_structure) - 1) * 3)
        expansion_2 = expansion_2 / np.broadcast_to(np.linalg.norm(expansion_2, axis=0), expansion_2.shape)
        cs2 = CoordinateSystem('ZMatrixExpanded', basis=ZMatrixCoordinates, matrix=expansion_2)
        coord_set2 = coord_set.convert(cs1)
        coord_set2 = coord_set2.convert(cs2)
        coord_set2 = coord_set2.convert(CartesianCoordinates3D)
        self.assertEqual(round(np.linalg.norm(coord_set2 - coord_set), 8), 0.0)

"""Extracted from ConverterTest.test_NewZMatConversions via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ConverterTest.test_NewZMatConversions"""

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
    def test_NewZMatConversions(self):
        from McUtils.ExternalPrograms import RDMolecule
        rdmol = RDMolecule.from_xyz(TestManager.test_data('bzpo.xyz'))
        zmat = [[11, -1, -2, -3], [10, 11, -1, -2], [9, 10, 11, -1], [8, 9, 10, 11], [7, 8, 9, 10], [6, 7, 8, 9], [4, 6, 7, 8], [3, 4, 6, 7], [2, 3, 4, 6], [1, 2, 3, 4], [12, 1, 2, 3], [17, 12, 1, 2], [16, 17, 12, 1], [15, 16, 17, 12], [14, 15, 16, 17], [13, 14, 15, 16], [0, 1, 2, 3], [5, 4, 6, 7], [18, 7, 8, 9], [19, 8, 9, 10], [20, 9, 10, 11], [21, 10, 11, 9], [22, 11, 10, 9], [23, 13, 14, 15], [24, 14, 15, 16], [25, 15, 16, 17], [26, 16, 17, 12], [27, 17, 12, 1]]
        zm, opts = coordops.convert_cartesian_to_zmatrix(rdmol.coords, ordering=zmat, order=1)
        subopts = opts.copy()
        del subopts['derivs']
        _, opts2 = coordops.convert_zmatrix_to_cartesians(zm, order=2, **subopts)
        print(subopts['derivs'][0])

"""Extracted from ConverterTest.test_DistsFromInternals via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ConverterTest.test_DistsFromInternals"""

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
    def test_DistsFromInternals(self):
        import McUtils.Numputils as nput
        from McUtils.Data import UnitsData
        specs = [(0, 1), (1, 2), (0, 1, 2), (1, 3), (0, 1, 3), (2, 0, 1, 3)]
        coords = np.array([[-0.6536668184, 0.1833576293, 0.0], [0.6547582273, -0.184570919, 0.0], [-1.4819024331, -0.5299427478, 0.0], [1.4831016243, 0.5285859096, 0.0]]) / UnitsData.bohr_to_angstroms
        dists = nput.distance_matrix(coords, return_triu=True)
        ints = nput.internal_coordinate_tensors(coords, specs, order=0)[0]
        print()
        print('Internals:', ints)
        print('Distances:', dists)
        dinds, dists2 = internal_distance_convert(ints, specs, shift_dihedrals=True)
        print('Int Dists:', dists2)
        return
        conv = get_internal_distance_conversion([(0, 1), (0, 2), (0, 3), (1, 0, 2), (1, 0, 3), (2, 0, 3)])
        pprint.pprint(conv)

"""Extracted from ConverterTest.test_InternalInterConversion via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ConverterTest.test_InternalInterConversion"""

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
    def test_InternalInterConversion(self):
        import warnings
        warnings.filterwarnings('error')
        print()
        import McUtils.Coordinerds as coordops
        import McUtils.Numputils as nput
        spec = [(0, 1), (0, 2), (0, 3), (1, 0, 2), (1, 0, 3), (2, 0, 3)]
        new_spec = [(0, 1), (0, 2), (0, 3), (1, 0, 2), (1, 0, 3), (3, 0, 1, 2)]
        new_spec2 = [(0, 1), (0, 2), (0, 3), (1, 0, 2), (1, 0, 3), (0, 1, 2, 3)]
        coordops.validate_internals(spec)
        coordops.validate_internals(new_spec)
        self.assertIs(coordops.validate_internals(new_spec2, raise_on_failure=False)[0], False)
        conv = coordops.find_internal_conversion(spec, new_spec)
        pts = np.random.rand(4, 3)
        base = nput.internal_coordinate_tensors(pts, spec, order=0)[0]
        new_coords = conv(base)
        print(...)
        print(new_coords, nput.internal_coordinate_tensors(pts, new_spec, order=0)[0], nput.pts_dihedrals(*[pts[i] for i in new_spec[-1]]))
        ix1, distance_rep1 = coordops.get_internal_distance_conversion(spec)
        ix2, distance_rep2 = coordops.get_internal_distance_conversion(new_spec)
        print(distance_rep1(base), distance_rep2(new_coords))
        carts = get_internal_cartesian_conversion(new_spec)
        print(carts(new_coords))
        carts = get_internal_cartesian_conversion(spec)
        print(carts(base))

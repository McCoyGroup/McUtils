"""Extracted from ConverterTest.test_CartesianToZMatrixJacobian2Planar via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ConverterTest.test_CartesianToZMatrixJacobian2Planar"""

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
    def test_CartesianToZMatrixJacobian2Planar(self):
        coord_set = CoordinateSet(np.array([[-9.84847483e-18, -1.38777878e-17, 0.0991295048], [-9.84847483e-18, -1.38777878e-17, 1.0991295], [1.0, 9.71445147e-17, 0.0991295048], [2.46519033e-32, -1.38777878e-17, 0.225076602], [-1.97215226e-31, 1.4371441, -0.90030641], [-1.75999392e-16, -1.4371441, -0.90030641]]))
        coord_set_2 = CoordinateSet(np.array([[-1.86403557e-17, -0.076046524, 0.0462443228], [6.70904773e-17, -0.076046524, -0.953755677], [0.929682337, 0.292315732, 0.0462443228], [2.46519033e-32, -1.38777878e-17, 0.225076602], [-1.97215226e-31, 1.4371441, -0.90030641], [-1.75999392e-16, -1.4371441, -0.90030641]]))
        internal_ordering = [[0, -1, -1, -1], [1, 0, -1, -1], [2, 0, 1, -1], [3, 0, 2, 1], [4, 3, 1, 2], [5, 3, 4, 1]]
        coord_set.converter_options = {'ordering': internal_ordering}
        njacob = coord_set.jacobian(ZMatrixCoordinates, 2, stencil=5, analytic_deriv_order=1)
        self.assertEquals(njacob.shape, (6 * 3, 6, 3, 6 - 1, 3))
        jacob = coord_set.jacobian(ZMatrixCoordinates, 2, stencil=5)
        self.assertEquals(jacob.shape, (6, 3, 6, 3, 6 - 1, 3))
        njacob = njacob.reshape((6, 3, 6, 3, 6 - 1, 3))
        diffs = njacob - jacob
        ehhh = np.round(diffs, 3)
        print(np.array(np.where(np.abs(jacob) > 100)).T)
        print(np.max(np.abs(njacob)), np.max(np.abs(jacob)))
        self.assertTrue(np.allclose(diffs, 0.0, atol=0.0001), msg='wat: {}'.format(np.max(np.abs(np.round(diffs, 6)))))

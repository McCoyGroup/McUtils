"""Extracted from ConverterTest.test_CartesianToZMatrixJacobian via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ConverterTest.test_CartesianToZMatrixJacobian"""

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
    def test_CartesianToZMatrixJacobian(self):
        n = 10
        test_coords = DataGenerator.coords(n)
        coord_set = CoordinateSet(test_coords)
        icrds = coord_set.convert(ZMatrixCoordinates)
        internals = ZMatrixCoordinateSystem(**icrds.converter_options)
        ijacob = icrds.jacobian(CartesianCoordinates3D).reshape((n - 1) * 3, n * 3)
        nijacob = icrds.jacobian(CartesianCoordinates3D, all_numerical=True, stencil=3).reshape((n - 1) * 3, n * 3)
        jacob = coord_set.jacobian(internals, stencil=3).reshape(n * 3, (n - 1) * 3)
        njacob = coord_set.jacobian(internals, all_numerical=True).reshape(n * 3, (n - 1) * 3)
        vmax = np.max(np.abs(jacob))
        g = GraphicsGrid(ncols=2, nrows=2, image_size=(600, 600))
        ArrayPlot(jacob, figure=g[0, 0], vmin=-vmax, vmax=vmax)
        ArrayPlot(njacob, figure=g[0, 1], vmin=-vmax, vmax=vmax)
        ArrayPlot(np.round(njacob - jacob, 4), figure=g[1, 0], vmin=-vmax, vmax=vmax)
        ArrayPlot(np.round(njacob + jacob, 4), figure=g[1, 1], vmin=-vmax, vmax=vmax)
        g.padding = 0.05
        g.padding_top = 0.5
        g.show()
        self.assertTrue(np.allclose(jacob, njacob), msg='{} too large'.format(np.sum(np.abs(jacob - njacob))))
        self.assertTrue(np.allclose(ijacob, nijacob))
        self.assertEquals(jacob.shape, (n * 3, (n - 1) * 3))
        self.assertAlmostEqual(np.sum(ijacob @ jacob), 3 * n - 6, 3)

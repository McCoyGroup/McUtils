"""Extracted from ConverterTest.test_SmoothCoordinateInterpolation via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ConverterTest.test_SmoothCoordinateInterpolation"""

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
    def test_SmoothCoordinateInterpolation(self):
        minimum_1 = [[0.0, -1e-08, -1.22523364], [0.0, 2e-08, 1.22523343], [0.0, 3e-08, -3.61388469], [0.0, -5e-08, 3.61388491]]
        zm_1 = coordops.functionalized_zmatrix(2, single_atoms=[0, 1])
        specs_1 = coordops.extract_zmatrix_internals(zm_1)
        print(specs_1)
        specs_1 = [(0, 1), (0, 2), (1, 3), (1, 0, 2), (0, 1, 3), (2, 0, 1, 3)]
        minimum_2 = [[0.0, 0.0, 1.53899513], [0.0, 0.0, -0.89818466], [-1.78011952, 0.0, -1.92243141], [1.78011952, 0.0, -1.92243141]]
        specs_2 = [(0, 1), (1, 2), (1, 3), (0, 1, 2), (0, 1, 3), (2, 0, 1, 3)]
        ics_11 = nput.internal_coordinate_tensors(minimum_1, specs_1, order=0)[0]
        ics_21 = nput.internal_coordinate_tensors(minimum_2, specs_1, order=0)[0]
        ics_22 = nput.internal_coordinate_tensors(minimum_2, specs_2, order=0)[0]
        ics_12 = nput.internal_coordinate_tensors(minimum_1, specs_2, order=0)[0]
        specs_3 = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 0, 1, 3)]
        ics_23 = nput.internal_coordinate_tensors(minimum_2, specs_3, order=0)[0]
        ics_13 = nput.internal_coordinate_tensors(minimum_1, specs_3, order=0)[0]
        iterp_x = np.linspace(0, 1, 100)
        ic_interp_1 = ics_11[np.newaxis, :] * (1 - iterp_x[:, np.newaxis]) + ics_21[np.newaxis, :] * iterp_x[:, np.newaxis]
        ic_interp_2 = ics_12[np.newaxis, :] * (1 - iterp_x[:, np.newaxis]) + ics_22[np.newaxis, :] * iterp_x[:, np.newaxis]
        ic_interp_3 = ics_13[np.newaxis, :] * (1 - iterp_x[:, np.newaxis]) + ics_23[np.newaxis, :] * iterp_x[:, np.newaxis]
        d_ic_1 = ic_interp_1 - ics_11[np.newaxis, :]
        d_ic_2 = ic_interp_2 - ics_22[np.newaxis, :]
        interp_norms = np.array([np.linalg.norm(d_ic_1, axis=1), np.linalg.norm(d_ic_2, axis=1)])
        percentages = np.exp(-interp_norms[0] / (interp_norms[1] + 1e-12))
        dist_specs, conv_1 = coordops.get_internal_distance_conversion(specs_1)
        _, conv_2 = coordops.get_internal_distance_conversion(specs_2)
        _, conv_3 = coordops.get_internal_distance_conversion(specs_3)
        dists1 = conv_1(ic_interp_1)
        dists2 = conv_2(ic_interp_2)
        dists3 = conv_3(ic_interp_3)
        dists12 = percentages[:, np.newaxis] * dists1 + (1 - percentages[:, np.newaxis]) * dists2
        geoms1 = nput.points_from_distance_matrix(dists1, use_triu=True, target_dim=3)
        geoms2 = nput.points_from_distance_matrix(dists2, use_triu=True, target_dim=3)
        geoms3 = nput.points_from_distance_matrix(dists3, use_triu=True, target_dim=3)
        geoms12 = nput.points_from_distance_matrix(dists12, use_triu=True, target_dim=3)
        from McUtils.Data import AtomData, UnitsData
        d_1 = nput.internal_coordinate_tensors(geoms1, dist_specs, order=1)[1:]
        d_2 = nput.internal_coordinate_tensors(geoms2, dist_specs, order=1)[1:]
        d_13 = nput.internal_coordinate_tensors(geoms1, specs_3, order=1)[1:]
        d_23 = nput.internal_coordinate_tensors(geoms2, specs_3, order=1)[1:]
        d_3 = nput.internal_coordinate_tensors(geoms3, specs_3, order=1)[1:]
        d_12 = nput.internal_coordinate_tensors(geoms12, dist_specs, order=1)[1:]
        d_123 = nput.internal_coordinate_tensors(geoms12, specs_3, order=1)[1:]
        m_h = np.array([AtomData[a, 'Mass'] for a in ['C', 'C', 'H', 'H']]) * UnitsData.convert('AtomicMassUnits', 'ElectronMass')
        m_d = np.array([AtomData[a, 'Mass'] for a in ['C', 'C', 'D', 'H']]) * UnitsData.convert('AtomicMassUnits', 'ElectronMass')
        print(m_h, m_d)
        g12_h = nput.metric_tensor(d_12, m_h)
        g12_d = nput.metric_tensor(d_12, m_d)
        g123_d = nput.metric_tensor(d_123, m_d)
        g123_h = nput.metric_tensor(d_123, m_h)
        g2_d = nput.metric_tensor(d_2, m_d)
        g2_3_d = nput.metric_tensor(d_23, m_d)
        g1_d = nput.metric_tensor(d_1, m_d)
        g1_3_d = nput.metric_tensor(d_13, m_d)
        g3_d = nput.metric_tensor(d_3, m_d)
        g2_h = nput.metric_tensor(d_2, m_h)
        g2_3_h = nput.metric_tensor(d_23, m_h)
        g1_3_h = nput.metric_tensor(d_13, m_h)
        g3_h = nput.metric_tensor(d_3, m_h)
        g1_h = nput.metric_tensor(d_1, m_h)
        import McUtils.Devutils as dev
        dev.write_json(os.path.expanduser('~/Desktop/geom_interp_test.json'), {'smooth': geoms12.tolist(), 'acet': geoms1.tolist(), 'vinny': geoms2.tolist(), 'merge': geoms3.tolist(), 'perc': percentages.tolist(), 'g12': g12_h.tolist(), 'g12_CCHD': g12_d.tolist(), 'g123_CCHD': g123_d.tolist(), 'g123': g123_h.tolist(), 'g1_CCHD': g1_d.tolist(), 'g1': g1_h.tolist(), 'g1_3_CCHD': g1_3_d.tolist(), 'g1_3': g1_3_h.tolist(), 'g2_CCHD': g2_d.tolist(), 'g2_3_CCHD': g2_3_d.tolist(), 'g3_CCHD': g3_d.tolist(), 'g2': g2_h.tolist(), 'g2_3': g2_3_h.tolist(), 'g3': g3_h.tolist()})

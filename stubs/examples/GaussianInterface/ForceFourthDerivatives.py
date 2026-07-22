"""Extracted from GaussianInterfaceTests.test_ForceFourthDerivatives via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest GaussianInterfaceTests.test_ForceFourthDerivatives"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.GaussianInterface import *
import sys, os, numpy as np

class GaussianInterfaceTests(TestCase):

    def setUp(self):
        self.test_log_water = TestManager.test_data('water_OH_scan.log')
        self.test_log_freq = TestManager.test_data('water_freq.log')
        self.test_log_opt = TestManager.test_data('water_dimer_test.log')
        self.test_fchk = TestManager.test_data('water_freq.fchk')
        self.test_log_h2 = TestManager.test_data('outer_H2_scan_new.log')
        self.test_scan = TestManager.test_data('water_OH_scan.log')
        self.test_rel_scan = TestManager.test_data('tbhp_030.log')

    @validationTest
    def test_ForceFourthDerivatives(self):
        n = 3
        with GaussianFChkReader(self.test_fchk) as reader:
            parse = reader.parse('ForceDerivatives')
        fcs = parse['ForceDerivatives']
        tds = fcs.fourth_deriv_array
        self.assertEquals(fcs.n, n)
        self.assertEquals(tds.shape, (3 * n - 6, 3 * n - 6, 3 * n, 3 * n))
        slice_0 = tds[0, 0].toarray()
        slice_1 = tds[1, 1].toarray()
        slice_2 = tds[2, 2].toarray()
        self.assertTrue(np.allclose(slice_0, slice_0.T, rtol=1e-08, atol=1e-08))
        self.assertTrue(np.allclose(slice_1, slice_1.T, rtol=1e-08, atol=1e-08))
        self.assertTrue(np.allclose(slice_2, slice_2.T, rtol=1e-08, atol=1e-08))

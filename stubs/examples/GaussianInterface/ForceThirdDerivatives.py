"""Extracted from GaussianInterfaceTests.test_ForceThirdDerivatives via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest GaussianInterfaceTests.test_ForceThirdDerivatives"""

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
    def test_ForceThirdDerivatives(self):
        n = 3
        with GaussianFChkReader(self.test_fchk) as reader:
            parse = reader.parse('ForceDerivatives')
        fcs = parse['ForceDerivatives']
        tds = fcs.third_deriv_array
        self.assertEquals(fcs.n, n)
        self.assertEquals(tds.shape, (3 * n - 6, 3 * n, 3 * n))
        a = tds[0]
        self.assertTrue(np.allclose(tds[0], tds[0].T, rtol=1e-08, atol=1e-08))
        self.assertTrue(np.allclose(tds[1], tds[1].T, rtol=1e-08, atol=1e-08))
        self.assertTrue(np.allclose(tds[2], tds[2].T, rtol=1e-08, atol=1e-08))

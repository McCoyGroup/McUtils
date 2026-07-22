"""Extracted from GaussianInterfaceTests.test_XMatrix via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest GaussianInterfaceTests.test_XMatrix"""

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
    def test_XMatrix(self):
        file = TestManager.test_data('qooh1.log')
        with GaussianLogReader(file) as reader:
            parse = reader.parse('XMatrix')
        X = np.array(parse['XMatrix'])
        self.assertIsInstance(X, np.ndarray)
        self.assertEquals(X.shape, (39, 39))
        self.assertEquals(X[0, 10], -0.126703)
        self.assertEquals(X[33, 26], -0.0642702)

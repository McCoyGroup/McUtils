"""Extracted from GaussianInterfaceTests.test_OptScanEnergies via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest GaussianInterfaceTests.test_OptScanEnergies"""

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
    def test_OptScanEnergies(self):
        with GaussianLogReader(self.test_log_opt) as reader:
            parse = reader.parse('OptimizedScanEnergies')
        e, c = parse['OptimizedScanEnergies']
        self.assertIsInstance(e, np.ndarray)
        self.assertEquals(e.shape, (9,))
        self.assertEquals(len(c.keys()), 14)
        self.assertEquals(list(c.values())[0].shape, (9,))

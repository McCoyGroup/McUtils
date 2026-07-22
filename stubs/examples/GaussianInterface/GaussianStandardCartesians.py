"""Extracted from GaussianInterfaceTests.test_GaussianStandardCartesians via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest GaussianInterfaceTests.test_GaussianStandardCartesians"""

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
    def test_GaussianStandardCartesians(self):
        with GaussianLogReader(self.test_log_water) as reader:
            parse = reader.parse('StandardCartesianCoordinates', num=15)
        carts = parse['StandardCartesianCoordinates']
        self.assertIsInstance(carts[1], np.ndarray)
        self.assertEquals(carts[1].shape, (15, 3, 3))

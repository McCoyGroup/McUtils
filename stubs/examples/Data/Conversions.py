"""Extracted from DataTests.test_Conversions via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest DataTests.test_Conversions"""

import numpy as np
from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Data import *

class DataTests(TestCase):

    @validationTest
    def test_Conversions(self):
        self.assertGreater(UnitsData.data['Hartrees', 'InverseMeters']['Value'], 21947463.13)
        self.assertLess(UnitsData.data['Hartrees', 'InverseMeters']['Value'], 21947463.14)
        self.assertAlmostEqual(UnitsData.convert('Hartrees', 'Wavenumbers'), UnitsData.convert('Hartrees', 'InverseMeters') / 100)
        self.assertAlmostEqual(UnitsData.convert('Hartrees', 'Wavenumbers'), UnitsData.convert('Centihartrees', 'InverseMeters'))

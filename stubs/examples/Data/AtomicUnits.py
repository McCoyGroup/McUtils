"""Extracted from DataTests.test_AtomicUnits via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest DataTests.test_AtomicUnits"""

import numpy as np
from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Data import *

class DataTests(TestCase):

    @validationTest
    def test_AtomicUnits(self):
        self.assertAlmostEqual(UnitsData.convert('AtomicMassUnits', 'AtomicUnitOfMass'), 1822.888486217313)

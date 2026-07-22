"""Extracted from ParserTests.test_XYZ via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ParserTests.test_XYZ"""

from McUtils.McUtils.Parsers.TeXParser import BibItemParser
from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Parsers import *
import sys, os, numpy as np

class ParserTests(TestCase):

    @validationTest
    def test_XYZ(self):
        with open(TestManager.test_data('test_100.xyz')) as test:
            test_str = test.read()
        res = XYZParser.parse_all(test_str)
        atom_coords = res['Atoms'].array[1].array
        self.assertIsInstance(atom_coords, np.ndarray)
        self.assertEquals(atom_coords.shape, (100, 13, 3))

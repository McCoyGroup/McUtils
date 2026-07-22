"""Extracted from ParserTests.test_OptScan via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ParserTests.test_OptScan"""

from McUtils.McUtils.Parsers.TeXParser import BibItemParser
from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Parsers import *
import sys, os, numpy as np

class ParserTests(TestCase):

    @validationTest
    def test_OptScan(self):
        eigsPattern = RegexPattern(('Eigenvalues --', Repeating(Capturing(Number), suffix=Optional(Whitespace))), joiner=Whitespace)
        coordsPattern = RegexPattern((Capturing(VariableName), Repeating(Capturing(Number), suffix=Optional(Whitespace))), prefix=Whitespace, joiner=Whitespace)
        full_pattern = RegexPattern((Named(eigsPattern, 'Eigenvalues'), Named(Repeating(coordsPattern, suffix=Optional(Newline)), 'Coordinates')), joiner=Newline)
        with open(TestManager.test_data('scan_params_test.txt')) as test:
            test_str = test.read()
        parser = StringParser(full_pattern)
        parse_res = parser.parse_all(test_str)
        parse_single = parser.parse(test_str)
        parse_its = list(parser.parse_iter(test_str))
        self.assertEquals(parse_res.shape, [(4, 5), [(4, 32), (4, 32, 5)]])
        self.assertIsInstance(parse_res['Coordinates'][1].array, np.ndarray)
        self.assertEquals(int(parse_res['Coordinates'][1, 0].sum()), 3230)

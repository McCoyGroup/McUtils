"""Extracted from ParserTests.test_RegexGroups via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ParserTests.test_RegexGroups"""

from McUtils.McUtils.Parsers.TeXParser import BibItemParser
from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Parsers import *
import sys, os, numpy as np

class ParserTests(TestCase):

    @validationTest
    def test_RegexGroups(self):
        test_str = '1 2 3 4 a b c d '
        pattern = RegexPattern((Capturing(Repeating(Capturing(Repeating(PositiveInteger, 2, 2, suffix=Optional(Whitespace))))), Repeating(Capturing(ASCIILetter), suffix=Whitespace)))
        self.assertEquals(len(pattern.search(test_str).groups()), 2)

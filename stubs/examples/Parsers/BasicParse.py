"""Extracted from ParserTests.test_BasicParse via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ParserTests.test_BasicParse"""

from McUtils.McUtils.Parsers.TeXParser import BibItemParser
from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Parsers import *
import sys, os, numpy as np

class ParserTests(TestCase):

    @validationTest
    def test_BasicParse(self):
        regex = RegexPattern((Named(PositiveInteger, 'NumAtoms'), Named(Repeating(Any, min=None), 'Comment', dtype=str), Named(Repeating(Capturing(Repeating(Capturing(Number), 3, 3, prefix=Whitespace, suffix=Optional(Whitespace)), handler=StringParser.array_handler(shape=(None, 3))), suffix=Optional(Newline)), 'Atoms')), 'XYZ', joiner=Newline)
        with open(TestManager.test_data('coord_parse.txt')) as test:
            test_str = test.read()
        res = StringParser(regex).parse(test_str)
        comment_string = res['Comment'].array[0]
        self.assertTrue('comment' in comment_string)
        self.assertEquals(res['Atoms'].array.shape, (4, 3))

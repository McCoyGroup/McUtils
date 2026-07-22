"""Extracted from ParserTests.test_ParseTex via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ParserTests.test_ParseTex"""

from McUtils.McUtils.Parsers.TeXParser import BibItemParser
from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Parsers import *
import sys, os, numpy as np

class ParserTests(TestCase):

    @validationTest
    def test_ParseTex(self):
        import McUtils.Devutils as dev
        root_text = dev.read_file(TestManager.test_data('samp.tex'))
        with TeXParser(TestManager.test_data('samp.tex')) as parser:
            print()
            for i in range(6):
                (s, e), text = parser.parse_tex_call(return_end_points=True)
                print((s, e), text)
                if e > 0:
                    print(root_text[s:e])
                else:
                    print(root_text[s:])
        with TeXParser(TestManager.test_data('samp.tex')) as parser:
            print()
            (s, e), text = parser.parse_tex_environment(return_end_points=True)
            print((s, e), text)
            if e > 0:
                print(root_text[s:e])
            else:
                print(root_text[s:])

"""Extracted from ParserTests.test_ParseBib via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ParserTests.test_ParseBib"""

from McUtils.McUtils.Parsers.TeXParser import BibItemParser
from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Parsers import *
import sys, os, numpy as np

class ParserTests(TestCase):

    @debugTest
    def test_ParseBib(self):
        import McUtils.Devutils as dev
        bib_file = TestManager.test_data('TeXPaper/bibliography/alt.bib')
        root_text = dev.read_file(bib_file)
        samp_bib = '\n@article{Goodfellow2014,\n   author = {Ian J. Goodfellow and Jean Pouget-Abadie and Mehdi Mirza and Bing Xu and David Warde-Farley and Sherjil Ozair and Aaron Courville and Yoshua Bengio},\n   journal = {arXiv e-prints},\n   month = {6},\n   title = {Generative Adversarial Networks},\n   url = {http://arxiv.org/abs/1406.2661},\n   year = {2014},\n}\n'
        import pprint
        with BibTeXParser(bib_file) as parser:
            print()
            for i in range(6):
                (s, e), text = parser.parse_bib_item(return_end_points=True)
                if text is not None:
                    print('=' * 100)
                    print((s, e), text)
                    pprint.pprint(parser.parse_bib_body(text))

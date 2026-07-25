"""Extracted from DocsTests.test_DocstringParser via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest DocsTests.test_DocstringParser"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Docs import *
import os, inspect, sys

class DocsTests(TestCase):
    """
    Sample documentation generator tests
    """

    @debugTest
    def test_DocstringParser(self):
        docfile = sys.modules[DocstringParser.__module__].__file__
        docs = DocstringParser().parse_file(docfile)
        for doc in docs:
            probs, score = DocstringDataAnalyzer(doc).analyze_docstring_quality()
            print(score, doc)

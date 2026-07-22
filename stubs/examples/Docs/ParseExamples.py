"""Extracted from DocsTests.test_ParseExamples via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest DocsTests.test_ParseExamples"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Docs import *
import os, inspect

class DocsTests(TestCase):
    """
    Sample documentation generator tests
    """

    @validationTest
    def test_ParseExamples(self):
        parser = ExamplesParser.from_file(os.path.abspath(__file__))
        self.assertTrue(hasattr(parser.functions, 'items'))

"""Extracted from DocsTests.test_FormatSpec via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest DocsTests.test_FormatSpec"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Docs import *
import os, inspect

class DocsTests(TestCase):
    """
    Sample documentation generator tests
    """

    @validationTest
    def test_FormatSpec(self):
        from McUtils.Formatters import TemplateFormatter
        fmt = inspect.cleandoc("\n        ### My Data\n\n        {$:b=loop(add_temp, l1, l2, slots=['l1', 'l2'])}\n        {$:len(b) ** 2}\n\n\n        ")
        print('', TemplateFormatter([]).format(fmt, param=2, l1=[1, 2, 3], l2=[4, 5, 6], add_temp='{l1} + {l2}', p1=1, p2=0), sep='\n')

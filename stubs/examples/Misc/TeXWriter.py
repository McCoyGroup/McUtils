"""Extracted from MiscTests.test_TeXWriter via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest MiscTests.test_TeXWriter"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Misc import *
import numpy

class MiscTests(TestCase):

    @debugTest
    def test_TeXWriter(self):
        array = [[1, 2, 3], [4, 500000, 6]]
        arr_tex = TeX.wrap_parens(TeX.Array(array))
        print(arr_tex.format_tex())
        o = TeX.Symbol('omega')
        i = TeX.Symbol('i')
        f = TeX.Symbol(TeX.bold('f'))
        sum = TeX.Symbol('sum')
        expr = sum[i:0:5] | o ** 2
        expr = f.Eq(arr_tex)
        print(TeX.Equation(expr, label='fmat').format_tex())

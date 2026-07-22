"""Extracted from MiscTests.test_Symbolics via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest MiscTests.test_Symbolics"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Misc import *
import numpy

class MiscTests(TestCase):

    @validationTest
    def test_Symbolics(self):
        x, y, z, some = Abstract.vars('x', 'y', 'z', 'some')
        lexpr = Abstract.Lambda(x, *y, some=1, **z)(x * some)
        lfun = lexpr.compile()
        self.assertEquals([1, 2, 3] * 3, lfun([1, 2, 3], this=1, has=0, some=3, effect=4))
        x, np = Abstract.vars('x', 'np')
        npexpr = Abstract.Lambda(x)(np.array(x)[..., 0] + 1)
        self.assertTrue(numpy.all(npexpr.compile({'np': numpy})([[1], [2], [3]]) == numpy.array([[1], [2], [3]])[..., 0] + 1))

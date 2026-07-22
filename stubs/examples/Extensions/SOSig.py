"""Extracted from ExtensionsTests.test_SOSig via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ExtensionsTests.test_SOSig"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Extensions import *
from McUtils.Data import *
import sys, os, numpy as np

class ExtensionsTests(TestCase):

    @validationTest
    def test_SOSig(self):
        lib_file = TestManager.test_data('libmbpol.so')
        mbpol = SharedLibraryFunction(lib_file, FunctionSignature('calcpot_', Argument('nw', PointerType(IntType)), Argument('energy', PointerType(RealType)), Argument('coords', ArrayType(RealType))))
        self.assertTrue("SharedLibraryFunction(FunctionSignature(calcpot_(Argument('nw', PointerType(PrimitiveType(int)))" in repr(mbpol))

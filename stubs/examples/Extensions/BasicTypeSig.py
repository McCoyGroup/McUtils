"""Extracted from ExtensionsTests.test_BasicTypeSig via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ExtensionsTests.test_BasicTypeSig"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Extensions import *
from McUtils.Data import *
import sys, os, numpy as np

class ExtensionsTests(TestCase):

    @validationTest
    def test_BasicTypeSig(self):
        sig = FunctionSignature('my_func', Argument('num_1', RealType), Argument('num_2', RealType, default=5), Argument('some_int', IntType))
        self.assertEquals(sig.cpp_signature, 'void my_func(double num_1, double num_2, int some_int)')

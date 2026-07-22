"""Extracted from ScaffoldingTests.test_JSONPseudoPickleSerialization via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ScaffoldingTests.test_JSONPseudoPickleSerialization"""

from Peeves.TestUtils import *
import McUtils.Devutils as dev
from McUtils.Scaffolding import *
import McUtils.Parsers as parsers
from unittest import TestCase
import numpy as np, io, os, sys, tempfile as tmpf

class ScaffoldingTests(TestCase):

    class DataHolderClass:

        def __init__(self, **keys):
            self.data = keys

        def to_state(self, serializer=None):
            return self.data

        @classmethod
        def from_state(cls, state, serializer=None):
            return cls(**state)

    @validationTest
    def test_JSONPseudoPickleSerialization(self):
        from McUtils.Numputils import SparseArray
        tmp = io.StringIO()
        serializer = JSONSerializer()
        data = SparseArray.from_diag([1, 2, 3, 4])
        serializer.serialize(tmp, data)
        tmp.seek(0)
        loaded = serializer.deserialize(tmp)
        self.assertTrue(np.allclose(loaded.asarray(), data.asarray()))

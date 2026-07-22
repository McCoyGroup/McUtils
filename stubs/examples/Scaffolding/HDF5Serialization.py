"""Extracted from ScaffoldingTests.test_HDF5Serialization via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ScaffoldingTests.test_HDF5Serialization"""

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
    def test_HDF5Serialization(self):
        tmp = io.BytesIO()
        serializer = HDF5Serializer()
        data = [1, 2, 3]
        serializer.serialize(tmp, data)
        loaded = serializer.deserialize(tmp)
        self.assertEquals(loaded.tolist(), data)
        serializer.serialize(tmp, {'blebby': {'frebby': {'clebby': data}}})
        loaded = serializer.deserialize(tmp, key='blebby')
        self.assertEquals(loaded['frebby']['clebby'].tolist(), data)
        mixed_data = [[1, 2, 3], 'garbage', {'temps': [1.0, 2.0, 3.0]}]
        serializer.serialize(tmp, dict(mixed_data=mixed_data))
        loaded = serializer.deserialize(tmp, key='mixed_data')
        self.assertEquals(mixed_data, [loaded[0].tolist(), loaded[1].tolist().decode('utf-8'), {k: v.tolist() for k, v in loaded[2].items()}])

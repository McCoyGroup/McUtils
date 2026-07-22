"""Extracted from ScaffoldingTests.test_JSONSerialization via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ScaffoldingTests.test_JSONSerialization"""

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
    def test_JSONSerialization(self):
        tmp = io.StringIO()
        serializer = JSONSerializer()
        data = [1, 2, 3]
        serializer.serialize(tmp, data)
        tmp.seek(0)
        loaded = serializer.deserialize(tmp)
        self.assertEquals(loaded, data)
        tmp = io.StringIO()
        serializer.serialize(tmp, {'blebby': {'frebby': {'clebby': data}}})
        tmp.seek(0)
        loaded = serializer.deserialize(tmp, key='blebby')
        self.assertEquals(loaded['frebby']['clebby'], data)
        tmp = io.StringIO()
        mixed_data = [[1, 2, 3], 'garbage', {'temps': [1.0, 2.0, 3.0]}]
        serializer.serialize(tmp, dict(mixed_data=mixed_data))
        tmp.seek(0)
        loaded = serializer.deserialize(tmp, key='mixed_data')
        self.assertEquals(mixed_data, loaded)

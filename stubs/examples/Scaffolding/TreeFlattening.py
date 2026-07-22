"""Extracted from ScaffoldingTests.test_TreeFlattening via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ScaffoldingTests.test_TreeFlattening"""

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

    @debugTest
    def test_TreeFlattening(self):
        data = {'file': 'test.txt', 'filesystem': {'file': [['a'], ['b', 'c']]}, 'coords': 123, 'initial': {'coords': np.random.rand(5, 3)}, 'final': {'coords': np.random.rand(1, 2)}, 'a': {'thing': {'b': 1, 'c': 2, '_type': 'A', 'other': None}, 'other': None}, 'c': {'thing': None, 'other': 9.1}, 'g': {'c': np.full(5, None)}}
        flat = flatten_tree(data)
        print(flat)
        rev = unflatten_tree(flat)
        print(rev)
        buf = io.BytesIO()
        write_flat_tree(buf, data)
        buf.seek(0)
        rev2 = read_flat_tree(buf)
        print(rev2)

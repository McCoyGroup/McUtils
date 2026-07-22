"""Extracted from ScaffoldingTests.test_HDF5Problems via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ScaffoldingTests.test_HDF5Problems"""

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
    def test_HDF5Problems(self):
        test = os.path.expanduser('~/Desktop/woof.hdf5')
        os.remove(test)
        checkpointer = Checkpointer.from_file(test)
        with checkpointer:
            checkpointer['why'] = [np.random.rand(1000, 5, 5), np.array(0), np.array(0)]
        with checkpointer:
            checkpointer['why'] = [np.random.rand(1001, 5, 5), np.array(0), np.array(0)]
        with checkpointer:
            checkpointer['why2'] = [np.random.rand(1001, 5, 5), np.array(0), np.array(0)]
        with checkpointer as chk:
            self.assertEquals(list(chk.keys()), ['why', 'why2'])

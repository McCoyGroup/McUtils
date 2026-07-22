"""Extracted from ScaffoldingTests.test_JSONCheckpointing via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ScaffoldingTests.test_JSONCheckpointing"""

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
    def test_JSONCheckpointing(self):
        with tmpf.NamedTemporaryFile() as chk_file:
            my_file = chk_file.name
        try:
            with JSONCheckpointer(my_file) as chk:
                data = [1, 2, 3]
                chk['step_1'] = data
                chk['step_2_params'] = {'steps': 500, 'step_size': 0.1, 'method': 'implicit euler'}
                data_2 = np.random.rand(100)
                chk['step_2'] = data_2
            with JSONCheckpointer(my_file) as chk:
                self.assertEquals(len(chk['step_2']), 100)
        finally:
            os.remove(my_file)

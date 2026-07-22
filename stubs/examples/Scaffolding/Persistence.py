"""Extracted from ScaffoldingTests.test_Persistence via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ScaffoldingTests.test_Persistence"""

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
    def test_Persistence(self):
        persist_dir = TestManager.test_data('persistence_tests')

        class PersistentMock:
            """
            A fake object that supports the persistence interface we defined
            """

            def __init__(self, name, sample_val):
                self.name = name
                self.val = sample_val

            @classmethod
            def from_config(cls, name='wat', sample_val=None):
                return cls(name, sample_val)
        manager = PersistenceManager(PersistentMock, persist_dir)
        obj = manager.load('obj1', strict=False)
        self.assertEquals(obj.val, 'test_val')

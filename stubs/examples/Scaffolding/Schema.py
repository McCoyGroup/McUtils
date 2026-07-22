"""Extracted from ScaffoldingTests.test_Schema via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ScaffoldingTests.test_Schema"""

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
    def test_Schema(self):
        data = {'file': 'test.txt', 'filesystem': {'os': 'macOS'}}
        schema = dev.Schema({'file': 'str'}, {'filesystem': str})
        self.assertFalse(schema.validate(data, throw=False))
        schema = dev.Schema({'file': 'str'}, {'filesystem': {'os': {'type': 'str', 'enum': ['macOS', 'linux', 'windows']}}})
        self.assertTrue(schema.validate(data))
        data = {'file': 'test.txt', 'filesystem': {'os': 'OSX'}}
        self.assertFalse(schema.validate(data, throw=False))

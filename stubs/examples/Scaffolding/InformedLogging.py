"""Extracted from ScaffoldingTests.test_InformedLogging via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ScaffoldingTests.test_InformedLogging"""

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
    def test_InformedLogging(self):
        import random
        with tmpf.NamedTemporaryFile(mode='w+b') as temp:
            log_dump = temp.name
        try:
            logger = Logger(log_dump)
            for i in range(100):
                with logger.block(tag='Step {}'.format(i)):
                    logger.log_print('Did X')
                    logger.log_print('Did Y')
                    with logger.block(tag='Fake Call'.format(i)):
                        logger.log_print('Took {timing:.5f}s', timing=random.random())
            number_puller = parsers.StringParser(parsers.Capturing(parsers.Number))
            with LogParser(log_dump) as parser:
                time_str = ''
                for block in parser.get_blocks(tag='Fake Call', level=1):
                    time_str += block.lines[0]
                timings = number_puller.parse_all(time_str).array
                self.assertEquals(len(timings), 100)
                self.assertGreater(np.average(timings), 0.35)
                self.assertLess(np.average(timings), 0.65)
            with LogParser(log_dump) as parser:
                time_str = ''
                for line in parser.get_lines(tag='Took ', level=1):
                    time_str += line
                timings = number_puller.parse_all(time_str).array
                self.assertEquals(len(timings), 100)
                self.assertGreater(np.average(timings), 0.35)
                self.assertLess(np.average(timings), 0.65)
        finally:
            os.remove(log_dump)

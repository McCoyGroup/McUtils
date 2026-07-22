"""Extracted from ScaffoldingTests.test_BasicLogging via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ScaffoldingTests.test_BasicLogging"""

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
    def test_BasicLogging(self):
        stdout = io.StringIO()
        logger = Logger(stdout)
        with logger.block(tag='Womp Womp'):
            logger.log_print('wompy dompy domp')
            logger.log_print('Some other useful info?')
            with logger.block(tag='Calling into subprogram'):
                logger.log_print('actually this is fake -_-')
                logger.log_print('took {timing:.5f}s', timing=121.01234)
            logger.log_print('I guess following up on that?')
            with logger.block(tag='Calling into subprogram'):
                logger.log_print('this is also fake! :yay:')
                logger.log_print('took {timing:.5f}s', timing=212.01234)
            logger.log_print('done for now; took {timing:.5f}s', timing=-1)
        with logger.block(tag='Surprise second block!'):
            logger.log_print('just kidding')
            with logger.block(tag='JK on that JK'):
                with logger.block(tag='Doubly nested block!'):
                    logger.log_print('woopy doopy doo bitchez')
                logger.log_print('(all views are entirely my own and do not reflect on my employer in any way)')
            logger.log_print('okay done for real; took {timing:.0f} years', timing=10000)
        with tmpf.NamedTemporaryFile(mode='w+b') as temp:
            log_dump = temp.name
        try:
            with open(log_dump, 'w+') as dump:
                dump.write(stdout.getvalue())
            with LogParser(log_dump) as parser:
                blocks = list(parser.get_blocks())
                self.assertEquals(blocks[1].lines[1].lines[1], ' (all views are entirely my own and do not reflect on my employer in any way)')
                self.assertEquals(blocks[1].lines[1].lines[0].tag, 'Doubly nested block!')
        finally:
            os.remove(log_dump)

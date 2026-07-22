"""Extracted from ScaffoldingTests.test_Jobbing via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ScaffoldingTests.test_Jobbing"""

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
    def test_Jobbing(self):
        import time
        with tmpf.TemporaryDirectory() as temp_dir:
            manager = JobManager(temp_dir)
            with manager.job('test') as job:
                logger = job.logger
                with logger.block(tag='Sleeping'):
                    logger.log_print('Goodnight!')
                    time.sleep(0.2)
                    logger.log_print("Okee I'm back up")
            self.assertEquals(os.path.basename(job.dir), 'test')
            self.assertEquals(set(job.checkpoint.backend.keys()), {'start', 'runtime'})
            with open(job.logger.log_file) as doopy:
                doop_str = doopy.read()
                self.assertNotEqual('', doop_str)

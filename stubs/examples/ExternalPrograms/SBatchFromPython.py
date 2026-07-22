"""Extracted from ExternalProgramsTest.test_SBatchFromPython via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ExternalProgramsTest.test_SBatchFromPython"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.ExternalPrograms import *
from McUtils.Data import UnitsData
from McUtils.Profilers import Timer
import sys, os, numpy as np, pprint

class ExternalProgramsTest(TestCase):

    class BoringEvaluators(EvaluationHandler):

        def add_vals(cls, coords, **kwargs):
            return np.sum(coords, axis=0)

        def get_evaluators(self) -> 'dict[str,method]':
            return {'add': self.add_vals}

    @staticmethod
    def _echo(arg):
        return arg

    @validationTest
    def test_SBatchFromPython(self):
        import os
        os.chdir('/Users/Mark/Desktop')
        woof, script_file = sbatch_python_job(print, 1, 2, 3)
        print(woof.format())
        print(script_file.resolve_buffer())

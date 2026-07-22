"""Extracted from ExternalProgramsTest.test_SingularityRun via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ExternalProgramsTest.test_SingularityRun"""

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
    def test_SingularityRun(self):
        import shlex
        sing = SingularityLauncher('/scratch/images/myapp.sif', 'python', '-m', 'myapp', mode='exec', env={'PYTHONPATH': '/work/src:/work/libs', 'PYTHONUNBUFFERED': '1'}, bind={'/home/me/project/src': '/work/src', '/home/me/project/libs': '/work/libs', '/home/me/project/out': '/work/out'}, bind_sources=['Psience'], pwd='/work', cleanenv=True)
        print(shlex.join(sing.get_launch_command()))

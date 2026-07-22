"""Extracted from ExternalProgramsTest.test_DockerRun via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ExternalProgramsTest.test_DockerRun"""

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
    def test_DockerRun(self):
        import shlex
        docker = DockerLauncher('python:3.12-slim', 'python', '-m', 'myapp', rm=True, env={'PYTHONPATH': '/work/src:/work/libs', 'PYTHONUNBUFFERED': '1'}, volume={'/home/me/project/src': '/work/src:ro', '/home/me/project/libs': '/work/libs:ro', '/home/me/project/out': '/work/out'}, workdir='/work')
        print(shlex.join(docker.get_launch_command()))

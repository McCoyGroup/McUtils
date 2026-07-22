"""Extracted from ExternalProgramsTest.test_EvaluationServer via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ExternalProgramsTest.test_EvaluationServer"""

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
    def test_EvaluationServer(self):
        connection = ('localhost', 12345)
        with GitHandler.start_multiprocessing_server(connection=connection, timeout=2):
            client = NodeCommClient(connection)
            res = client.call('pwd')
            client.print_response(res)
            res = client.call('git', 'status')
            client.print_response(res)
        with self.BoringEvaluators.start_multiprocessing_server(connection=connection, timeout=2):
            client = EvaluationClient(connection)
            res = client.call('add', np.array([[1, 2], [3, 4]]))
            if isinstance(res, dict):
                client.print_response(res)
            else:
                pprint.pprint(res)

"""Extracted from ExternalProgramsTest.test_CRESTParse via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ExternalProgramsTest.test_CRESTParse"""

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
    def test_CRESTParse(self):
        parser = CRESTParser(TestManager.test_data_dir)
        structs = parser.parse_optimized_structures()
        print(len(structs))
        print(structs[-1].energy)
        print(len(structs[-1].atoms))
        print(len(structs[-1].coords))
        log_info = parser.parse_log()
        print(log_info['FinalEnsembleInfo'].weights.shape)
        print(parser.parse_conformers().coords[0].shape)
        rotamers = parser.parse_rotamers()
        print(np.sum(rotamers.weights))

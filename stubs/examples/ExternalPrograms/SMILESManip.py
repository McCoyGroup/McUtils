"""Extracted from ExternalProgramsTest.test_SMILESManip via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ExternalProgramsTest.test_SMILESManip"""

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

    @debugTest
    def test_SMILESManip(self):
        from Psience.Molecools import Molecule
        from McUtils.Data import SMILESData
        from McUtils.ExternalPrograms import build_templated_smiles
        prod = build_templated_smiles(SMILESData.functional_group('carbamate'), {'functional_group': SMILESData.functional_group('imine'), 'new_bonds': [[0, 1], [1, 0]], 'push_bonds': True})
        print(prod)
        Molecule.from_string(prod).plot().show()

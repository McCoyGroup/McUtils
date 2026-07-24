"""Extracted from ExternalProgramsTest.test_RandomSMILESManip via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ExternalProgramsTest.test_RandomSMILESManip"""

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
    def test_RandomSMILESManip(self):
        from Psience.Molecools import Molecule
        from McUtils.Data import SMILESData
        scaff = SMILESData.random_scaffold()
        fg = SMILESData.random_functional_group()
        smi = join_smiles_fragments(scaff, fg)
        print(scaff)
        print(fg)
        print(smi)
        Molecule.from_string(smi).plot(highlight_atoms=[0, 1]).show()
        return

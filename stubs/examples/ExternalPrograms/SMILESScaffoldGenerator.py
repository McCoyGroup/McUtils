"""Extracted from ExternalProgramsTest.test_SMILESScaffoldGenerator via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ExternalProgramsTest.test_SMILESScaffoldGenerator"""

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
    def test_SMILESScaffoldGenerator(self):
        from Psience.Molecools import Molecule
        prod = build_templated_smiles('C1CCCC=1', {'functional_group': '[O:1]', 'bond_order': 2}, {'functional_group': '[S:1]', 'bond_order': 2}, active_sites={1: 0, 2: 2, 3: 1}, atom_replacements={2: 'N'}, remove_sites=True)
        print(prod)
        Molecule.from_string(prod).plot().show()

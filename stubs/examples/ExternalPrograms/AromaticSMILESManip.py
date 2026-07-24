"""Extracted from ExternalProgramsTest.test_AromaticSMILESManip via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ExternalProgramsTest.test_AromaticSMILESManip"""

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
    def test_AromaticSMILESManip(self):
        from Psience.Molecools import Molecule
        diene = '[C:1]([C:5]2)[C:3]=[C:4][C:2]2'
        dienophile = 'O=C1NC(=O)[C:2]=[C:1]1'
        cache = {}
        dienophile = set_smiles_bond_order(dienophile, 0, 1, 1, cache=cache)
        template = join_smiles_fragments(diene, dienophile, [[0, 0], [1, 1]], cache=cache, add_implicit_hydrogens='full', push_bonds=True)
        map_data1 = parse_smiles_and_atom_map(diene, cache=cache, add_implicit_hydrogens='full')
        offset = len(map_data1['map'])
        template = renumber_smiles_atom_map(template, {offset: 2, offset + 1: 3}, cache=cache, add_implicit_hydrogens='full')
        Molecule.from_string(template).plot(highlight_atoms=[0, 1, 2, 3]).show()

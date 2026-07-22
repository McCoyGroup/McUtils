"""Extracted from ExternalProgramsTest.test_OBGen3D via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ExternalProgramsTest.test_OBGen3D"""

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
    def test_OBGen3D(self):
        from Psience.Molecools import Molecule
        mol = OBMolecule.from_string('CO[C]12C[C@@](C=C1)(c1ccc(F)cc1)CC2', 'smi')
        mol.draw(use_coords=True).show()

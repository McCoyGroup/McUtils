"""Extracted from ExternalProgramsTest.test_CubeParser via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ExternalProgramsTest.test_CubeParser"""

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
    def test_CubeParser(self):
        from Psience.Molecools import Molecule
        eval = CubePropEvaluator.from_file(TestManager.test_data('samp.cube'))
        surf = eval.get_isosurface(0.2)
        surf2 = eval.get_isosurface(-0.2)
        mol = Molecule(eval.base_data.atoms.numbers, eval.base_data.atoms.positions)
        fig = mol.plot(backend='x3d')
        surf.plot(figure=fig, transparency=0.4, line_color=None)
        surf2.plot(figure=fig, color='yellow', transparency=0.4, line_color=None)
        fig.show()
        return
        eval = CubePropEvaluator.from_file('/Users/Mark/Downloads/h2o.mol2.cube')
        mol = Molecule(eval.base_data.atoms.numbers, eval.base_data.atoms.positions)
        fig = mol.plot(backend='x3d')
        surf = mol.get_surface(samples=200)
        tri = surf.get_triangulation()
        tri.plot(solid=False, figure=fig, vertex_values=eval.evaluate(tri.verts), transparency=0.5)
        fig.show()

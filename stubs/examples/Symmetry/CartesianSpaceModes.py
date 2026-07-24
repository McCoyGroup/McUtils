"""Extracted from SymmetryTests.test_CartesianSpaceModes via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest SymmetryTests.test_CartesianSpaceModes"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Symmetry import *
import numpy as np
import McUtils.Numputils as nput

class SymmetryTests(TestCase):

    @debugTest
    def test_CartesianSpaceModes(self):
        import numpy as np
        from McUtils.Data import AtomData
        from McUtils.Symmetry import identify_point_group, symmetrized_coordinate_coefficients
        from McUtils.Plots import Plot
        atoms = ['O', 'H', 'H']
        eq = np.array([[0.0, 0.0, 0.0], [0.758, 0.0, 0.504], [-0.758, 0.0, 0.504]])
        masses = np.array([AtomData[a, 'Mass'] for a in atoms])
        pg0 = identify_point_group(eq, masses=masses, tol=0.001)[1]
        print(pg0.character_table.format())
        symms = symmetrized_coordinate_coefficients(pg0, eq, merge_equivalents=True, as_characters=False)
        print(symms.shape)

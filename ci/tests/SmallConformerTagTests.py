"""
Conformer tags (`RDMolecule.to_inchi/to_smiles(include_tag=True)`) for molecules where the Z-matrix
is degenerate: a single heavy atom (water, methane), a heavy-atom pair, and disconnected heavy atoms
(ion pairs, mixtures)
"""

import os as _test_os
import unittest as _test_unittest
_RUN_EXTRAS = _test_os.environ.get("MCUTILS_TEST_EXTRAS") == "1"

import unittest

import numpy as np

from McUtils.ExternalPrograms import RDMolecule


def embedded(smiles):
    from rdkit import Chem
    from rdkit.Chem import AllChem
    rd = Chem.AddHs(Chem.MolFromSmiles(smiles))
    AllChem.EmbedMolecule(rd, randomSeed=7)
    return rd


def tagged(rd, **opts):
    return RDMolecule(rd.GetConformer()).to_inchi(include_tag=True, **opts).partition("_")[2]


@_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
class SmallConformerTagTests(unittest.TestCase):
    def test_tags_exist(self):
        for smiles in ["O", "C", "N#N", "CO", "C=C", "[Na+].[Cl-]", "CC.O", "CCO"]:
            with self.subTest(smiles):
                self.assertIsInstance(tagged(embedded(smiles)), str)

    def test_single_heavy_atom_tag_is_empty(self):
        for smiles in ["O", "C"]:
            self.assertEqual(tagged(embedded(smiles)), "")

    def test_pair_tag_follows_distance(self):
        rd = embedded("N#N")
        t0 = tagged(rd)
        conf = rd.GetConformer()
        pos = np.array(conf.GetPositions())
        pos[1] += [0, 0, .3]
        conf.SetAtomPosition(1, pos[1].tolist())
        self.assertNotEqual(t0, tagged(rd))

    def test_disconnected_fragments_follow_geometry(self):
        for smiles in ["[Na+].[Cl-]", "CC.O"]:
            rd = embedded(smiles)
            t0 = tagged(rd)
            self.assertEqual(t0, tagged(rd))
            conf = rd.GetConformer()
            p = conf.GetAtomPosition(0)
            conf.SetAtomPosition(0, [p.x, p.y, p.z + .5])
            self.assertNotEqual(t0, tagged(rd), smiles)

    def test_larger_molecules_unchanged(self):
        # the fix must not alter existing tags
        self.assertEqual(tagged(embedded("CCO")), "ikA+OeeZ")


if __name__ == "__main__":
    unittest.main()

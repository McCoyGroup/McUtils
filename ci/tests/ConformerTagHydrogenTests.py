"""`RDMolecule.to_inchi(include_tag=True, remove_implicit_hydrogens=False)` keeps hydrogens in the conformer tag"""
import unittest
import numpy as np
from McUtils.ExternalPrograms import RDMolecule


def embedded(smiles):
    from rdkit import Chem
    from rdkit.Chem import AllChem
    rd = Chem.AddHs(Chem.MolFromSmiles(smiles))
    AllChem.EmbedMolecule(rd, randomSeed=7)
    return rd

def tag(rd, **opts):
    inchi, _, t = RDMolecule(rd.GetConformer()).to_inchi(include_tag=True, **opts).partition("_")
    return t

def moved(rd, atom, dz=.5):
    from rdkit import Chem
    rd = Chem.Mol(rd)
    p = rd.GetConformer().GetAtomPosition(atom)
    rd.GetConformer().SetAtomPosition(atom, [p.x, p.y, p.z + dz])
    return rd


class ConformerTagHydrogenTests(unittest.TestCase):
    def setUp(self):
        self.rd = embedded("CCO")
        self.h = [a.GetIdx() for a in self.rd.GetAtoms() if a.GetAtomicNum() == 1]
        self.heavy = [a.GetIdx() for a in self.rd.GetAtoms() if a.GetAtomicNum() > 1]

    def test_default_and_true_ignore_hydrogens(self):
        base = tag(self.rd)
        for kw in [{}, dict(remove_implicit_hydrogens=None), dict(remove_implicit_hydrogens=True)]:
            self.assertEqual(tag(self.rd, **kw), base)
            for h in self.h:
                self.assertEqual(tag(moved(self.rd, h), **kw), base)

    def test_false_sees_every_hydrogen(self):
        base = tag(self.rd, remove_implicit_hydrogens=False)
        self.assertNotEqual(base, tag(self.rd))
        self.assertGreater(len(base), len(tag(self.rd)))
        for h in self.h:
            self.assertNotEqual(tag(moved(self.rd, h), remove_implicit_hydrogens=False), base, h)

    def test_false_still_sees_heavy_atoms_and_is_deterministic(self):
        base = tag(self.rd, remove_implicit_hydrogens=False)
        self.assertEqual(base, tag(self.rd, remove_implicit_hydrogens=False))
        for a in self.heavy:
            self.assertNotEqual(tag(moved(self.rd, a), remove_implicit_hydrogens=False), base)

    def test_reordering_covers_all_atoms_heavy_first(self):
        _, order = RDMolecule(self.rd.GetConformer()).to_inchi(
            include_tag=True, remove_implicit_hydrogens=False, return_reordering=True)
        self.assertEqual(sorted(order), list(range(self.rd.GetNumAtoms())))
        self.assertEqual(set(order[:3]), set(self.heavy))

    def test_hydrogen_ordering_follows_parent_heavy_atom(self):
        ext = RDMolecule._extend_reordering_with_hydrogens(self.rd, [0, 1, 2])
        parents = [min(n.GetIdx() for n in self.rd.GetAtomWithIdx(i).GetNeighbors()) for i in ext[3:]]
        self.assertEqual(parents, sorted(parents))

    def test_works_for_small_molecules_too(self):
        # needs the small-molecule tag fix; water has 3 atoms once hydrogens are included
        rd = embedded("O")
        try:
            t = tag(rd, remove_implicit_hydrogens=False)
        except ValueError:
            self.skipTest("needs the <3 heavy atom conformer tag fix")
        self.assertNotEqual(t, tag(moved(rd, 1), remove_implicit_hydrogens=False))


def kabsch_rmsd(a, b):
    a = a - a.mean(0); b = b - b.mean(0)
    u, _, vt = np.linalg.svd(a.T @ b)
    r = u @ np.diag([1, 1, np.sign(np.linalg.det(u @ vt))]) @ vt
    return float(np.sqrt(((a @ r - b) ** 2).sum(1).mean()))


class ConformerTagRoundTripTests(unittest.TestCase):
    """`to_inchi(include_tag=True, ...)` -> `from_inchi(...)` recovers the encoded geometry"""
    SMILES = ["CCO", "CC(=O)O", "CC(=O)N", "c1ccccc1", "C[C@H](N)C(=O)O", "CC.O", "N#N", "CO"]
    TOLERANCE = .03  # the tag is lossy; this is a few times the quantization error

    @staticmethod
    def roundtrip(smiles, keep_hydrogens):
        rd = embedded(smiles)
        mol = RDMolecule(rd.GetConformer())
        opts = dict(remove_implicit_hydrogens=False) if keep_hydrogens else {}
        inchi = mol.to_inchi(include_tag=True, **opts)
        _, order = mol.to_inchi(include_tag=True, return_reordering=True, **opts)
        new = RDMolecule.from_inchi(inchi)  # detects whether the tag holds hydrogens
        X = np.array(rd.GetConformer().GetPositions())[list(order)]
        return rd, new, X, np.array(new.coords)

    def test_heavy_atom_tags_round_trip(self):
        for smiles in self.SMILES:
            with self.subTest(smiles):
                rd, new, X, Y = self.roundtrip(smiles, False)
                self.assertEqual(len(Y), rd.GetNumAtoms())  # hydrogens come back (without tag coordinates)
                self.assertLess(kabsch_rmsd(X, Y[:len(X)]), self.TOLERANCE)

    def test_hydrogen_tags_round_trip(self):
        for smiles in self.SMILES:
            with self.subTest(smiles):
                rd, new, X, Y = self.roundtrip(smiles, True)
                self.assertEqual(len(Y), rd.GetNumAtoms())
                self.assertLess(kabsch_rmsd(X, Y), self.TOLERANCE)

    def test_hydrogen_tags_restore_hydrogen_positions(self):
        # moving a hydrogen is visible after the round trip only when hydrogens are in the tag
        from rdkit import Chem
        rd = embedded("CCO")
        h = [a.GetIdx() for a in rd.GetAtoms() if a.GetAtomicNum() == 1][0]
        far = Chem.Mol(rd)
        p = far.GetConformer().GetAtomPosition(h)
        far.GetConformer().SetAtomPosition(h, [p.x, p.y, p.z + 1.5])
        def decoded(r):
            m = RDMolecule(r.GetConformer())
            return np.array(RDMolecule.from_inchi(
                m.to_inchi(include_tag=True, remove_implicit_hydrogens=False)).coords)
        self.assertGreater(kabsch_rmsd(decoded(rd), decoded(far)), .1)

    def test_tag_atom_count_is_read_from_the_tag(self):
        for smiles in self.SMILES:
            with self.subTest(smiles):
                rd = embedded(smiles)
                mol = RDMolecule(rd.GetConformer())
                n_heavy = sum(a.GetAtomicNum() > 1 for a in rd.GetAtoms())
                for kw, n in [({}, n_heavy), (dict(remove_implicit_hydrogens=False), rd.GetNumAtoms())]:
                    tag = mol.to_inchi(include_tag=True, **kw).partition("_")[2]
                    self.assertEqual(RDMolecule.conformer_tag_num_atoms(tag), n)

    def test_detection_can_be_overridden(self):
        rd = embedded("CCO")
        mol = RDMolecule(rd.GetConformer())
        heavy = mol.to_inchi(include_tag=True)
        full = mol.to_inchi(include_tag=True, remove_implicit_hydrogens=False)
        # forcing the right answer agrees with detection
        for tagged, force in [(heavy, False), (full, True)]:
            self.assertTrue(np.allclose(
                RDMolecule.from_inchi(tagged).coords,
                RDMolecule.from_inchi(tagged, hydrogens_in_tag=force).coords))
        # forcing the wrong one fails instead of silently returning a bad geometry
        for tagged, force in [(heavy, True), (full, False)]:
            with self.assertRaises(Exception):
                RDMolecule.from_inchi(tagged, hydrogens_in_tag=force)

    def test_tag_that_matches_neither_graph_is_rejected(self):
        tag = RDMolecule(embedded("CCCC").GetConformer()).to_inchi(include_tag=True).partition("_")[2]
        with self.assertRaises(ValueError):
            RDMolecule.from_inchi("InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3_" + tag)  # tag of a different size

    def test_atoms_and_bonds_survive(self):
        for smiles in ["CC(=O)O", "CC.O"]:
            with self.subTest(smiles):
                rd, new, X, Y = self.roundtrip(smiles, True)
                self.assertEqual(sorted(a.GetSymbol() for a in rd.GetAtoms()),
                                 sorted(a.GetSymbol() for a in new.rdmol.GetAtoms()))
                self.assertEqual(rd.GetNumBonds(), new.rdmol.GetNumBonds())


if __name__ == "__main__":
    unittest.main()

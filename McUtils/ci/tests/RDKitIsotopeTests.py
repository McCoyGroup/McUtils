"""Element/isotope conversion at the RDMolecule boundary."""
import unittest

import numpy as np
from rdkit import Chem

from McUtils.Data import AtomData
from McUtils.ExternalPrograms import RDMolecule


class RDKitIsotopeTests(unittest.TestCase):
    coords = np.array([[0., 0., 0.], [.96, 0., 0.], [-.24, .93, 0.]])
    bonds = [[0, 1, 1], [0, 2, 1]]

    def molecule(self, atoms=('O', 'D', 'T'), **opts):
        return RDMolecule.from_coords(atoms, self.coords, bonds=self.bonds, **opts)

    def test_label_conversion_and_back_conversion(self):
        for label, symbol, isotope, canonical in [
            ('H', 'H', 0, 'H'), ('D', 'H', 2, 'D'), ('T', 'H', 3, 'T'),
            ('H2', 'H', 2, 'D'), ('H3', 'H', 3, 'T'), ('C13', 'C', 13, 'C13'),
            ('O18', 'O', 18, 'O18'), ('C12', 'C', 12, 'C12'), ('H1', 'H', 1, 'H1'),
            ('Carbon', 'C', 0, 'C'), ('Deuterium', 'H', 2, 'D'),
        ]:
            with self.subTest(label=label):
                atom = RDMolecule.to_rdkit_atom(label)
                self.assertEqual((atom.GetSymbol(), atom.GetIsotope()), (symbol, isotope))
                self.assertEqual(RDMolecule.from_rdkit_atom(atom), canonical)

    def test_atomic_numbers_numpy_and_dummy_atoms(self):
        for label, number in [(1, 1), (np.int64(6), 6), (0, 0), ('*', 0), ('X', 0), ('x', 0)]:
            with self.subTest(label=label):
                atom = RDMolecule.to_rdkit_atom(label)
                self.assertEqual(atom.GetAtomicNum(), number)
                self.assertEqual(atom.GetIsotope(), 0)
                if number == 0:
                    self.assertEqual(RDMolecule.from_rdkit_atom(atom), 'X')
        atom = RDMolecule.to_rdkit_atom(np.str_('D'))
        self.assertEqual(atom.GetIsotope(), 2)

    def test_atoms_isotopes_and_labels_are_parallel(self):
        mol = self.molecule()
        self.assertEqual(mol.atoms, ['O', 'H', 'H'])
        self.assertEqual(mol.isotopes, [0, 2, 3])
        self.assertEqual(mol.atom_labels, ['O', 'D', 'T'])
        mol.rdmol.GetAtomWithIdx(1).SetIsotope(3)
        self.assertEqual(mol.isotopes, [0, 3, 3])
        self.assertEqual(mol.atom_labels, ['O', 'T', 'T'])

    def test_parallel_isotopes_inference_and_overrides(self):
        self.assertEqual(self.molecule(('O', 'H', 'H'), isotopes=[18, 2, np.int64(3)]).isotopes, [18, 2, 3])
        mol = self.molecule(isotopes=[None, 3, 0])
        self.assertEqual(mol.isotopes, [0, 3, 0])
        self.assertEqual(mol.atom_labels, ['O', 'T', 'H'])

    def test_parallel_lengths_and_isotope_values_are_validated(self):
        for isotopes in [[], [2], [0, 2, 3, 0]]:
            with self.subTest(isotopes=isotopes), self.assertRaisesRegex(ValueError, 'one entry per atom'):
                self.molecule(isotopes=isotopes)
        for value in [-1, 2.0, '2', True, np.bool_(False)]:
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, 'nonnegative integers'):
                self.molecule(isotopes=[0, value, 3])
        with self.assertRaisesRegex(ValueError, 'formal_charges'):
            self.molecule(formal_charges=[0])

    def test_isotope_masses_and_unlabeled_mass_convention(self):
        mol = self.molecule()
        np.testing.assert_array_equal(mol.masses, [AtomData[a, 'Mass'] for a in ('O', 'D', 'T')])
        mol = self.molecule(('O', 'H', 'H'))
        np.testing.assert_array_equal(mol.masses, [AtomData[a, 'Mass'] for a in ('O', 'H', 'H')])

    def test_from_mol_preserves_explicit_isotope_numbers(self):
        mol = self.molecule(('O16', 'H1', 'H2'))
        copied = RDMolecule.from_mol(mol)
        self.assertEqual(copied.isotopes, [16, 1, 2])
        np.testing.assert_array_equal(copied.coords, mol.coords)

    def test_template_accepts_aliases_and_preserves_unspecified_isotopes(self):
        original = self.molecule()
        for atoms in [('O', 'D', 'H3'), ('O', 'H', 'H')]:
            with self.subTest(atoms=atoms):
                copied = self.molecule(atoms, rdmol=original.rdmol)
                self.assertEqual(copied.isotopes, [0, 2, 3])
                self.assertIsNot(copied.rdmol, original.rdmol)

    def test_template_rejects_conflicting_isotopes_without_mutation(self):
        original = self.molecule()
        for atoms, isotopes in [(('O', 'T', 'T'), None), (('O', 'H', 'H'), [0, 0, 3]),
                                 (('O', 'H', 'H'), [0, 3, 2])]:
            with self.subTest(atoms=atoms, isotopes=isotopes), self.assertRaisesRegex(ValueError, 'isotopes disagree'):
                self.molecule(atoms, isotopes=isotopes, rdmol=original.rdmol)
        self.assertEqual(original.isotopes, [0, 2, 3])
        np.testing.assert_array_equal(original.coords, self.coords)

    def test_atom_objects_keep_metadata_and_are_copied(self):
        original = Chem.Atom(6)
        original.SetIsotope(13)
        original.SetFormalCharge(-1)
        original.SetAtomMapNum(7)
        original.SetProp('example', 'preserved')
        copied = RDMolecule.to_rdkit_atom(original)
        self.assertEqual((copied.GetIsotope(), copied.GetFormalCharge(), copied.GetAtomMapNum()), (13, -1, 7))
        self.assertEqual(copied.GetProp('example'), 'preserved')
        RDMolecule.to_rdkit_atom(original, isotope=12)
        self.assertEqual(original.GetIsotope(), 13)

    def test_copy_preserves_isotopes_and_geometry(self):
        original = self.molecule()
        copied = original.copy()
        self.assertEqual(copied.isotopes, original.isotopes)
        np.testing.assert_array_equal(copied.coords, original.coords)

    def test_smiles_with_supplied_geometry_preserves_isotopes(self):
        mol = RDMolecule.from_smiles('[2H]O[3H]', coords=self.coords, add_implicit_hydrogens=False)
        self.assertEqual(mol.isotopes, [2, 0, 3])
        self.assertEqual(mol.atom_labels, ['D', 'O', 'T'])
        np.testing.assert_array_equal(mol.coords, self.coords)
        serialized = mol.to_smiles()
        self.assertIn('[2H]', serialized)
        self.assertIn('[3H]', serialized)

    def test_hydrogen_tag_graph_keeps_isotope_labels(self):
        parsed = Chem.MolFromSmiles('[13CH3]O[2H]')
        symbols, bonds = RDMolecule._inchi_hydrogen_tag_graph(parsed)
        self.assertEqual(symbols[:3], ['C13', 'O', 'D'])
        self.assertEqual(len(symbols), 6)
        self.assertEqual(len(bonds), 5)

    def test_inchi_with_hydrogen_tag_round_trips_isotopes(self):
        source = RDMolecule.from_smiles('[13CH3]O[2H]', add_implicit_hydrogens=True, num_confs=1)
        inchi = source.to_inchi(include_tag=True, remove_implicit_hydrogens=False)
        restored = RDMolecule.from_inchi(inchi)
        self.assertEqual(sorted(i for i in restored.isotopes if i), [2, 13])
        self.assertEqual(restored.to_smiles(canonical=True), source.to_smiles(canonical=True))


if __name__ == '__main__':
    unittest.main()



__all__ = [
    "OBMolecule"
]

import tempfile

import numpy as np, io, os

from .. import Devutils as dev
from ..Data import AtomData
from ..Jupyter import DisplayImage
from .. import Numputils as nput

from .ChemToolkits import OpenBabelInterface
from .ExternalMolecule import ExternalMolecule

class OBMolecule(ExternalMolecule):
    """
    A simple interchange format for OB molecules
    """

    def __init__(self, obmol, charge=None):
        super().__init__(obmol)
        self._pbmol = None
        self.charge = charge

    @property
    def pbmol(self):
        if self._pbmol is None:
            from openbabel import pybel
            self._pbmol = pybel.Molecule(self.mol)
        return self._pbmol

    @classmethod
    def get_api(cls):
        return OpenBabelInterface()
    @property
    def atoms(self):
        ob = self.get_api()
        return [a.GetAtomicNum() for a in ob.OBMolAtomIter(self.mol)]
    @property
    def bonds(self):
        ob = self.get_api()
        return [
            [b.GetBeginAtomIdx()-1 , b.GetEndAtomIdx()-1, b.GetBondOrder()]
            for b in ob.OBMolBondIter(self.mol)
        ]
    @property
    def coords(self):
        ob = self.get_api()
        return np.array([
            [a.GetX(), a.GetY(), a.GetZ()]
            for a in ob.OBMolAtomIter(self.mol)
        ])
    def set_coords(self, coords):
        ob = self.get_api()
        self.mol.BeginModify()
        for coord, atom in zip(coords, self.atom_iter()):
            atom.SetVector(*coord)
    @coords.setter
    def coords(self, coords):
        self.set_coords(coords)

    def atom_iter(self):
        ob = self.get_api()
        return ob.OBMolAtomIter(self.mol)

    @classmethod
    def from_obmol(cls, obmol, charge=None, guess_bonds=False):
        if guess_bonds:
            obmol.ConnectTheDots()  # guess connectivity from atomic distances
            obmol.PerceiveBondOrders()  # guess bond orders / aromaticity from geometry
        return cls(obmol, charge=charge)

    @classmethod
    def get_obmol_from_conversion(cls, data, fmt=None, add_implicit_hydrogens=False, target_fmt="mol2"):
        ob = cls.get_api()
        obConversion = ob.OBConversion()
        obConversion.SetInAndOutFormats(fmt, target_fmt)

        mol = ob.OBMol()
        obConversion.ReadString(mol, data)
        if add_implicit_hydrogens:
            mol.AddHydrogens()
        return mol

    @classmethod
    def get_obmol_from_gen3d(cls, data, fmt=None, add_implicit_hydrogens=False, method='gen3D', target='best'):
        ob = cls.get_api()
        mol = ob.OBMol()
        conv = ob.OBConversion()
        if fmt is not None:
            conv.SetInFormat(fmt)
        conv.ReadString(mol, data)
        if add_implicit_hydrogens:
            mol.AddHydrogens()

        # will need to adapt
        gen3d = ob.OBOp.FindType(method)
        if target is not None:
            gen3d.Do(mol, target)
        return mol

    default_conformer_generator = 'convert'
    @classmethod
    def from_string(cls, data, fmt=None,
                    conformer_generator=None,
                    add_implicit_hydrogens=False, charge=None, guess_bonds=False,
                    **confgen_opts):
        if conformer_generator is None:
            conformer_generator = cls.default_conformer_generator
            if dev.str_is(fmt, 'smi') and dev.str_is(conformer_generator, 'convert'):
                conformer_generator = 'gen3d'
        if dev.str_is(conformer_generator, 'convert'):
            mol = cls.get_obmol_from_conversion(data, fmt, add_implicit_hydrogens=add_implicit_hydrogens, **confgen_opts)
        elif dev.str_is(conformer_generator, 'gen3d'):
            mol = cls.get_obmol_from_gen3d(data, fmt, add_implicit_hydrogens=add_implicit_hydrogens, **confgen_opts)
        else:
            raise NotImplementedError(f"conformer generator {conformer_generator} not supported")
        return cls.from_obmol(mol,
                              charge=charge,
                              guess_bonds=guess_bonds)

    @classmethod
    def from_file(cls, file, fmt=None, target_fmt="mol2",
                  add_implicit_hydrogens=False, charge=None, guess_bonds=False):
        ob = cls.get_api()
        if fmt is None:
            _, fmt = os.path.splitext(file)
            fmt = fmt.strip(".")
        obConversion = ob.OBConversion()
        obConversion.SetInAndOutFormats(fmt, target_fmt)

        mol = ob.OBMol()
        obConversion.ReadFile(mol, file)
        return cls.from_obmol(mol,
                              charge=charge,
                              guess_bonds=guess_bonds)

    default_output_format = "mol2"
    def to_file(self, file, fmt=None, base_fmt="mol2"):
        ob = self.get_api()
        if fmt is None:
            _, fmt = os.path.splitext(file)
            fmt = fmt.strip(".")
            if len(fmt) == 0: fmt = self.default_output_format
        obConversion = ob.OBConversion()
        obConversion.SetInAndOutFormats(base_fmt, fmt)

        obConversion.WriteFile(self.mol, file)
        return file

    def to_string(self, fmt, base_fmt="mol2"):
        ob = self.get_api()
        obConversion = ob.OBConversion()
        obConversion.SetInAndOutFormats(base_fmt, fmt)

        return obConversion.WriteString(self.mol)

    @classmethod
    def from_coords(cls, atoms, coords, bonds=None, add_implicit_hydrogens=False, charge=None, guess_bonds=False):
        ob = cls.get_api()

        mol = ob.OBMol()
        for elem, crd in zip(atoms, coords):
            a = mol.NewAtom()
            a.SetAtomicNum(AtomData[elem]["Number"])  # carbon atom
            a.SetVector(*(float(c) for c in crd))  # coordinates

        if bonds is not None:
            for b in bonds:
                i, j = int(b[0])+1, int(b[1])+1   # atoms indexed from 1
                bt = b[2] if len(b) > 2 else 1
                if bt - int(bt) > .05:
                    # aromatic
                    mol.AddBond(i, j, bt, ob.OB_AROMATIC_BOND)
                else:
                    mol.AddBond(i, j, bt)

        return cls.from_obmol(mol,
                              charge=charge,
                              guess_bonds=guess_bonds)

    @classmethod
    def from_mol(cls, mol, coord_unit="Angstroms", guess_bonds=False):
        from ..Data import UnitsData

        return cls.from_coords(
            mol.atoms,
            mol.coords * UnitsData.convert(coord_unit, "Angstroms"),
            bonds=mol.bonds,
            charge=mol.charge,
            guess_bonds=guess_bonds
        )

    def copy(self):
        ob = self.get_api()
        return type(self)(
            ob.OBMol(self.mol),
            charge=self.charge
        )

    def remove_hydrogens(self, copy=True):
        if copy: self = self.copy()
        self.pbmol.removeh()
        return self

    def make_2d(self, copy=True):
        if copy: self = self.copy()
        coords = self.coords.copy()
        self.mol.SetDimension(0)
        self.pbmol.make2D()
        if np.any(np.isnan(self.coords)):
            masses = [AtomData[a, "Mass"] for a in self.atoms]
            _, emb = nput.moments_of_inertia(coords, masses)
            coords = coords @ emb
            coords[:, 2] = 0
            self.coords = coords
            self.mol.SetDimension(2)
        return self

    def draw(self,
             fmt='svg',
             remove_hydrogens=True,
             plot_range=None,
             postdraw=None,
             scaling_factor=None,
             splits=None,
             include_save_buttons=False,
             use_smiles=False,
             use_coords=False):
        if use_smiles:
            from openbabel import pybel
            pbmol = pybel.readstring("smi", self.to_string('smi'))
        else:
            if remove_hydrogens:
                self = self.remove_hydrogens()
            if not use_coords:
                self = self.make_2d()
            else:
                self = self.copy()
                c = self.coords
                c[:, 2] = 0
                self.coords = c
            pbmol = self.pbmol
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.' + fmt) as tf:
            pbmol.write(fmt, tf.name, overwrite=True)
            with open(tf.name) as f:
                txt = f.read()
        return DisplayImage(txt, fmt,
                            plot_range=plot_range,
                            postdraw=postdraw,
                            scaling_factor=scaling_factor,
                            splits=splits,
                            include_save_buttons=include_save_buttons)

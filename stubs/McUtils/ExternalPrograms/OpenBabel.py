__all__ = ['OBMolecule']
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
        """
        **LLM Docstring**

        Wrap an OpenBabel `OBMol` as an `OBMolecule`.

        :param obmol: the OpenBabel mol
        :param charge: the molecular charge
        :type charge: int | None
        """
        ...

    @property
    def pbmol(self):
        """
        **LLM Docstring**

        The Pybel wrapper around the underlying `OBMol` (built lazily).

        :return: the Pybel molecule
        :rtype: object
        """
        ...

    @classmethod
    def get_api(cls):
        """
        **LLM Docstring**

        Return the OpenBabel API interface.

        :return: the OpenBabel interface
        :rtype: OpenBabelInterface
        """
        ...

    @property
    def atoms(self):
        """
        **LLM Docstring**

        The atomic numbers of the atoms, in order.

        :return: the atomic numbers
        :rtype: list[int]
        """
        ...

    @property
    def bonds(self):
        """
        **LLM Docstring**

        The bonds as `[begin_atom, end_atom, order]` triples (0-indexed atoms).

        :return: the bond list
        :rtype: list[list]
        """
        ...

    @property
    def coords(self):
        """
        **LLM Docstring**

        The atomic Cartesian coordinates. Setting this writes new positions onto the
        atoms.

        :return: the coordinates
        :rtype: np.ndarray
        """
        ...

    def set_coords(self, coords):
        """
        **LLM Docstring**

        Write new Cartesian coordinates onto the molecule's atoms.

        :param coords: the new coordinates
        :type coords: np.ndarray
        """
        ...

    @coords.setter
    def coords(self, coords):
        """
        **LLM Docstring**

        The atomic Cartesian coordinates. Setting this writes new positions onto the
        atoms.

        :return: the coordinates
        :rtype: np.ndarray
        """
        ...

    def atom_iter(self):
        """
        **LLM Docstring**

        Return an iterator over the molecule's OpenBabel atoms.

        :return: the atom iterator
        :rtype: Iterator
        """
        ...

    @classmethod
    def from_obmol(cls, obmol, charge=None, guess_bonds=False):
        """
        **LLM Docstring**

        Wrap an `OBMol` as an `OBMolecule`, optionally perceiving connectivity and bond
        orders from the geometry.

        :param obmol: the OpenBabel mol
        :param charge: the molecular charge
        :type charge: int | None
        :param guess_bonds: perceive bonds/orders from geometry
        :type guess_bonds: bool
        :return: the wrapped molecule
        :rtype: OBMolecule
        """
        ...

    @classmethod
    def get_obmol_from_conversion(cls, data, fmt=None, add_implicit_hydrogens=False, target_fmt='mol2'):
        """
        **LLM Docstring**

        Read an `OBMol` from a string by converting from the input format to an
        intermediate format via OpenBabel's converter.

        :param data: the input molecule string
        :type data: str
        :param fmt: the input format (e.g. `'smi'`)
        :type fmt: str | None
        :param add_implicit_hydrogens: add hydrogens after reading
        :type add_implicit_hydrogens: bool
        :param target_fmt: the intermediate conversion format
        :type target_fmt: str
        :return: the OpenBabel mol
        """
        ...

    @classmethod
    def get_obmol_from_gen3d(cls, data, fmt=None, add_implicit_hydrogens=False, method='gen3D', target='best'):
        """
        **LLM Docstring**

        Read an `OBMol` from a string and generate a 3D structure for it via OpenBabel's
        `gen3D` operation.

        :param data: the input molecule string
        :type data: str
        :param fmt: the input format
        :type fmt: str | None
        :param add_implicit_hydrogens: add hydrogens after reading
        :type add_implicit_hydrogens: bool
        :param method: the 3D-generation operation name
        :type method: str
        :param target: the gen3D quality target (e.g. `'best'`)
        :type target: str | None
        :return: the OpenBabel mol
        """
        ...
    default_conformer_generator = 'convert'

    @classmethod
    def from_string(cls, data, fmt=None, conformer_generator=None, add_implicit_hydrogens=False, charge=None, guess_bonds=False, **confgen_opts):
        """
        **LLM Docstring**

        Build an `OBMolecule` from a molecule string, choosing between plain conversion
        and 3D generation (defaulting to `gen3d` for SMILES input).

        :param data: the input molecule string
        :type data: str
        :param fmt: the input format
        :type fmt: str | None
        :param conformer_generator: `'convert'` or `'gen3d'` (auto-chosen if omitted)
        :type conformer_generator: str | None
        :param add_implicit_hydrogens: add hydrogens after reading
        :type add_implicit_hydrogens: bool
        :param charge: the molecular charge
        :type charge: int | None
        :param guess_bonds: perceive bonds/orders from geometry
        :type guess_bonds: bool
        :param confgen_opts: extra options for the chosen reader
        :return: the wrapped molecule
        :rtype: OBMolecule
        """
        ...

    @classmethod
    def from_file(cls, file, fmt=None, target_fmt='mol2', add_implicit_hydrogens=False, charge=None, guess_bonds=False):
        """
        **LLM Docstring**

        Build an `OBMolecule` from a file, inferring the format from the extension when
        not given.

        :param file: the input file path
        :type file: str
        :param fmt: the input format (inferred from the extension if omitted)
        :type fmt: str | None
        :param target_fmt: the intermediate conversion format
        :type target_fmt: str
        :param add_implicit_hydrogens: add hydrogens after reading
        :type add_implicit_hydrogens: bool
        :param charge: the molecular charge
        :type charge: int | None
        :param guess_bonds: perceive bonds/orders from geometry
        :type guess_bonds: bool
        :return: the wrapped molecule
        :rtype: OBMolecule
        """
        ...
    default_output_format = 'mol2'

    def to_file(self, file, fmt=None, base_fmt='mol2'):
        """
        **LLM Docstring**

        Write the molecule to a file, inferring the output format from the extension
        when not given.

        :param file: the output file path
        :type file: str
        :param fmt: the output format (inferred from the extension if omitted)
        :type fmt: str | None
        :param base_fmt: the intermediate conversion format
        :type base_fmt: str
        :return: the file path
        :rtype: str
        """
        ...

    def to_string(self, fmt, base_fmt='mol2'):
        """
        **LLM Docstring**

        Serialize the molecule to a string in the requested format.

        :param fmt: the output format
        :type fmt: str
        :param base_fmt: the intermediate conversion format
        :type base_fmt: str
        :return: the serialized molecule
        :rtype: str
        """
        ...

    @classmethod
    def from_coords(cls, atoms, coords, bonds=None, add_implicit_hydrogens=False, charge=None, guess_bonds=False):
        """
        **LLM Docstring**

        Build an `OBMolecule` from atoms, coordinates, and (optional) bonds.

        :param atoms: the element symbols
        :type atoms: Sequence[str]
        :param coords: the Cartesian coordinates
        :type coords: np.ndarray
        :param bonds: the bonds as `[i, j(, order)]` (0-indexed)
        :type bonds: Sequence | None
        :param add_implicit_hydrogens: unused flag
        :type add_implicit_hydrogens: bool
        :param charge: the molecular charge
        :type charge: int | None
        :param guess_bonds: perceive bonds/orders from geometry
        :type guess_bonds: bool
        :return: the wrapped molecule
        :rtype: OBMolecule
        """
        ...

    @classmethod
    def from_mol(cls, mol, coord_unit='Angstroms', guess_bonds=False):
        """
        **LLM Docstring**

        Build an `OBMolecule` from a generic molecule object, converting its coordinates
        to Angstroms.

        :param mol: the source molecule
        :param coord_unit: the source coordinate unit
        :type coord_unit: str
        :param guess_bonds: perceive bonds/orders from geometry
        :type guess_bonds: bool
        :return: the wrapped molecule
        :rtype: OBMolecule
        """
        ...

    def copy(self):
        """
        **LLM Docstring**

        Return a copy of this molecule (copying the underlying `OBMol` and charge).

        :return: the copied molecule
        :rtype: OBMolecule
        """
        ...

    def remove_hydrogens(self, copy=True):
        """
        **LLM Docstring**

        Remove the molecule's hydrogens (on a copy by default).

        :param copy: operate on a copy rather than in place
        :type copy: bool
        :return: the molecule without hydrogens
        :rtype: OBMolecule
        """
        ...

    def make_2d(self, copy=True):
        """
        **LLM Docstring**

        Generate a 2D depiction of the molecule (on a copy by default), falling back to
        an inertial-frame projection when OpenBabel's 2D coordinates come out invalid.

        :param copy: operate on a copy rather than in place
        :type copy: bool
        :return: the 2D molecule
        :rtype: OBMolecule
        """
        ...

    def draw(self, fmt='svg', remove_hydrogens=True, plot_range=None, postdraw=None, scaling_factor=None, splits=None, include_save_buttons=False, use_smiles=False, use_coords=False):
        """
        **LLM Docstring**

        Render the molecule to an image (SVG/PNG), optionally from its SMILES or its own
        (flattened) coordinates, with hydrogen removal and 2D-depiction generation.

        :param fmt: the output image format
        :type fmt: str
        :param remove_hydrogens: hide hydrogens
        :type remove_hydrogens: bool
        :param plot_range: a fixed drawing range
        :type plot_range: tuple | None
        :param postdraw: a callback invoked after drawing
        :type postdraw: Callable | None
        :param scaling_factor: an image scaling factor
        :param splits: drawing element split metadata
        :param include_save_buttons: include save buttons in the output
        :type include_save_buttons: bool
        :param use_smiles: depict from the SMILES rather than the current structure
        :type use_smiles: bool
        :param use_coords: use the molecule's own coordinates (projected to 2D)
        :type use_coords: bool
        :return: the rendered image
        :rtype: DisplayImage
        """
        ...
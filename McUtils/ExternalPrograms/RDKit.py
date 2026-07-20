__all__ = [
    "RDMolecule"
]

import base64
import itertools
import functools
import tempfile as tf
import numpy as np, io, os
from .. import Numputils as nput
from .. import Devutils as dev
from ..Data import AtomData

from .ChemToolkits import RDKitInterface
from .ExternalMolecule import ExternalMolecule
from .. import Coordinerds as coordops
from ..Jupyter import DisplayImage

class RDMolecule(ExternalMolecule):
    """
    A simple interchange format for RDKit molecules
    """

    def __init__(self, rdconf, charge=None):
        """
        **LLM Docstring**

        Wrap an RDKit conformer (and its owning mol) as an `RDMolecule`.

        :param rdconf: the RDKit conformer
        :type rdconf: Chem.Conformer
        :param charge: the molecular charge
        :type charge: int | None
        """
        #atoms, coords, bonds):
        self._rdmol = rdconf.GetOwningMol()
        super().__init__(rdconf)
        self.charge = charge

    @property
    def rdmol(self):
        """
        **LLM Docstring**

        The underlying RDKit `Mol` object (recovered from the conformer if needed).

        :return: the RDKit mol
        :rtype: Chem.Mol
        """
        if self._rdmol is None:
            self._rdmol = self.mol.GetOwningMol()
        return self._rdmol
    @property
    def atoms(self):
        """
        **LLM Docstring**

        The element symbols of the atoms, in order.

        :return: the atom symbols
        :rtype: list[str]
        """
        mol = self.rdmol
        return [atom.GetSymbol() for atom in mol.GetAtoms()]
    @property
    def bonds(self):
        """
        **LLM Docstring**

        The bonds as `[begin_atom, end_atom, order]` triples.

        :return: the bond list
        :rtype: list[list]
        """
        mol = self.rdmol
        return [
            [b.GetBeginAtomIdx(), b.GetEndAtomIdx(), b.GetBondTypeAsDouble()]
            for b in mol.GetBonds()
        ]
    @property
    def coords(self):
        """
        **LLM Docstring**

        The atomic Cartesian coordinates (Angstroms). Setting this writes new positions
        onto the conformer.

        :return: the coordinates
        :rtype: np.ndarray
        """
        return self.mol.GetPositions()
    @coords.setter
    def coords(self, coords):
        """
        **LLM Docstring**

        The atomic Cartesian coordinates (Angstroms). Setting this writes new positions
        onto the conformer.

        :return: the coordinates
        :rtype: np.ndarray
        """
        coords = np.asanyarray(coords)
        self.mol.SetPositions(coords)
    @property
    def rings(self):
        """
        **LLM Docstring**

        The atom-index tuples of the rings found by RDKit's ring perception.

        :return: the ring atom indices
        :rtype: tuple
        """
        return self.rdmol.GetRingInfo().AtomRings()
    @property
    def meta(self):
        """
        **LLM Docstring**

        The molecule's RDKit properties as a dict.

        :return: the property dict
        :rtype: dict
        """
        return self.rdmol.GetPropsAsDict()

    def copy(self):
        """
        **LLM Docstring**

        Return a copy of this molecule, carrying over the current conformer and charge.

        :return: the copied molecule
        :rtype: RDMolecule
        """
        Chem = self.chem_api()
        conf = self.mol
        new_mol = Chem.AddHs(Chem.Mol(self.rdmol), explicitOnly=True)
        new_mol.AddConformer(conf)
        return type(self).from_rdmol(new_mol,
                                     conf_id=conf.GetId(),
                                     charge=self.charge, sanitize=False,
                                     guess_bonds=False,
                                     add_implicit_hydrogens=False
                                     )
    @property
    def charges(self):
        """
        **LLM Docstring**

        The per-atom Gasteiger partial charges (computed on access).

        :return: the partial charges
        :rtype: list[float]
        """
        from rdkit.Chem import AllChem
        AllChem.ComputeGasteigerCharges(self.rdmol)
        return [
            at.GetDoubleProp('_GasteigerCharge')
            for at in self.rdmol.GetAtoms()
        ]

    @property
    def formal_charges(self):
        """
        **LLM Docstring**

        The per-atom formal charges.

        :return: the formal charges
        :rtype: list[int]
        """
        return [
            at.GetFormalCharge()
            for at in self.rdmol.GetAtoms()
        ]

    class NullContext:
        def __enter__(self):
            """
            **LLM Docstring**

            Enter the no-op context (used when error suppression is disabled).

            :return: None
            """
            ...
        def __exit__(self, exc_type, exc_val, exc_tb):
            """
            **LLM Docstring**

            Exit the no-op context.

            :param exc_type: the exception type, if any
            :param exc_val: the exception value, if any
            :param exc_tb: the traceback, if any
            """
            ...
    @classmethod
    def quiet_errors(cls, verbose=False):
        """
        **LLM Docstring**

        Return a context manager that suppresses RDKit's C++ log output, unless
        `verbose` is set (in which case a no-op context is returned).

        :param verbose: don't suppress logging
        :type verbose: bool
        :return: the (log-blocking or no-op) context manager
        :rtype: object
        """
        from rdkit.rdBase import BlockLogs
        if verbose:
            return cls.NullContext()
        else:
            return BlockLogs()

    @classmethod
    def chem_api(cls):
        """
        **LLM Docstring**

        Return the RDKit `Chem` submodule.

        :return: the `Chem` module
        :rtype: module
        """
        return RDKitInterface.submodule("Chem")

    @classmethod
    def _prep_mol(cls, rdkit_mol):
        """
        **LLM Docstring**

        Do the minimal ring/hybridization/property-cache setup needed to work with a
        mol that hasn't been fully sanitized.

        :param rdkit_mol: the mol to prepare (modified in place)
        :type rdkit_mol: Chem.Mol
        """
        Chem = cls.allchem_api()
        rdkit_mol.UpdatePropertyCache(strict=False)
        _ = Chem.GetSymmSSSR(rdkit_mol)
        Chem.SetHybridization(rdkit_mol)
    @classmethod
    def guess_rdmol_bonds(cls, rdmol, charge=None, determine_orders=True, in_place=False):
        """
        **LLM Docstring**

        Perceive the bonds (and, optionally, bond orders) of a mol from its atomic
        coordinates, falling back to connectivity-only perception when order
        determination fails.

        :param rdmol: the mol
        :type rdmol: Chem.Mol
        :param charge: the molecular charge (inferred if omitted)
        :type charge: int | None
        :param determine_orders: also perceive bond orders
        :type determine_orders: bool
        :param in_place: modify the mol in place rather than copying
        :type in_place: bool
        :return: the mol with perceived bonds
        :rtype: Chem.Mol
        """
        Chem = cls.chem_api()
        if not in_place:
            rdmol = Chem.Mol(rdmol)
        if charge is None:
            charge = Chem.GetFormalCharge(rdmol)
        rdDetermineBonds = RDKitInterface.submodule("Chem.rdDetermineBonds")
        if determine_orders:
            #TODO: allow a fallback to `DetermineConnectivity`
            try:
                rdDetermineBonds.DetermineBonds(rdmol, charge=charge)
            except ValueError:
                rdDetermineBonds.DetermineConnectivity(rdmol, charge=charge)
        else:
            rdDetermineBonds.DetermineConnectivity(rdmol, charge=charge)
        return rdmol
    @classmethod
    def from_rdmol(cls, rdmol, conf_id=0, charge=None, guess_bonds=False, sanitize=True,
                   add_implicit_hydrogens=False,
                   sanitize_ops=None,
                   allow_generate_conformers=False,
                   num_confs=1,
                   optimize=False,
                   take_min=True,
                   force_field_type='mmff'):
        """
        **LLM Docstring**

        Build an `RDMolecule` from an RDKit mol, adding hydrogens and optionally guessing
        bonds, sanitizing, and generating conformers.

        :param rdmol: the source mol
        :type rdmol: Chem.Mol
        :param conf_id: the conformer id to use
        :type conf_id: int
        :param charge: the molecular charge (inferred if omitted)
        :type charge: int | None
        :param guess_bonds: perceive bonds from geometry
        :type guess_bonds: bool
        :param sanitize: run RDKit sanitization
        :type sanitize: bool
        :param add_implicit_hydrogens: add implicit (not just explicit) hydrogens
        :type add_implicit_hydrogens: bool
        :param sanitize_ops: sanitization operation flags
        :param allow_generate_conformers: generate conformers if none exist
        :type allow_generate_conformers: bool
        :param num_confs: number of conformers to generate
        :type num_confs: int
        :param optimize: force-field optimize generated conformers
        :type optimize: bool
        :param take_min: keep only the lowest-energy generated conformer
        :type take_min: bool
        :param force_field_type: the force field for optimization
        :type force_field_type: str
        :return: the wrapped molecule
        :rtype: RDMolecule
        """
        Chem = cls.chem_api() # to get nice errors
        rdmol = Chem.AddHs(rdmol, explicitOnly=not add_implicit_hydrogens)
        if charge is None:
            charge = Chem.GetFormalCharge(rdmol)
        if guess_bonds:
            rdmol = cls.guess_rdmol_bonds(rdmol, charge, determine_orders=True, in_place=True)
        if sanitize:
            rdmolops = RDKitInterface.submodule("Chem.rdmolops")
            if sanitize_ops is None:
                sanitize_ops = (
                        rdmolops.SANITIZE_ALL
                        ^rdmolops.SANITIZE_PROPERTIES
                        # ^rdmolops.SANITIZE_ADJUSTHS
                        # ^rdmolops.SANITIZE_CLEANUP
                        ^rdmolops.SANITIZE_CLEANUP_ORGANOMETALLICS
                )

            rdmol = Chem.Mol(rdmol)
            try:
                Chem.SanitizeMol(rdmol, sanitize_ops)
            except Chem.rdchem.MolSanitizeException:
                cls._prep_mol(rdmol)

        no_confs = False
        try:
            conf = rdmol.GetConformer(conf_id)
        except ValueError:
            no_confs = True

        if no_confs:
            if allow_generate_conformers:
                conf_id = cls.generate_conformers_for_mol(rdmol,
                                                          num_confs=num_confs,
                                                          optimize=optimize,
                                                          take_min=take_min,
                                                          force_field_type=force_field_type)
            else:
                raise ValueError(f"{rdmol} has no conformers")

            conf = rdmol.GetConformer(conf_id)
        return cls(conf, charge=charge)

    @classmethod
    def resolve_bond_type(cls, t):
        """
        **LLM Docstring**

        Map a numeric bond order to the corresponding RDKit `BondType` (handling the
        aromatic/half-integer cases).

        :param t: the numeric bond order
        :type t: float
        :return: the RDKit bond type
        :rtype: Chem.BondType
        """
        Chem = cls.chem_api()

        if abs(t - 1.5) < 1e-2:
            t = Chem.BondType.names["AROMATIC"]
        elif abs(t - 2.5) < 1e-2:
            t = Chem.BondType.names["TWOANDAHALF"]
        elif abs(t - 3.5) < 1e-2:
            t = Chem.BondType.names["TWOANDAHALF"]
        else:
            t = Chem.BondType.values[int(t)]

        return t

    default_new_coord_alignment_method = 'rigid'
    @classmethod
    def _align_new_conf_coords(cls, mol, coords, coords2, method=None):
        """
        **LLM Docstring**

        Align a freshly generated conformer's coordinates back onto a set of reference
        coordinates (e.g. after adding implicit hydrogens), placing the new atoms via a
        local rigid frame or a global Eckart embedding.

        :param mol: the mol (for connectivity)
        :type mol: Chem.Mol
        :param coords: the reference coordinates (heavy atoms)
        :type coords: np.ndarray
        :param coords2: the full generated coordinates
        :type coords2: np.ndarray
        :param method: `'rigid'`, `'eckart'`, or otherwise pass through
        :type method: str | None
        :return: the aligned coordinates
        :rtype: np.ndarray
        """

        if method is None:
            method = cls.default_new_coord_alignment_method

        if method == 'rigid':
            new_pos = len(coords2) - len(coords)
            if new_pos == 0:
                coords3 = coords
            else:
                new_coords = []
                bond_map = {}
                for b in mol.GetBonds():
                    i = b.GetBeginAtomIdx()
                    j = b.GetEndAtomIdx()
                    if i not in bond_map: bond_map[i] = set()
                    if j not in bond_map: bond_map[j] = set()
                    bond_map[i].add(j)
                    bond_map[j].add(i)
                nog = len(coords)
                atoms = [a.GetSymbol() for a in mol.GetAtoms()]
                for i in range(new_pos):
                    i += nog
                    if len(bond_map[i]) == 0:
                        new_coords.append(coords2[i])
                    else:
                        j = list(bond_map[i])[0]
                        partners = [f for f in bond_map[j] if f < nog]
                        if len(partners) == 0:
                            z = coords[i] - coords2[j]
                            new_coords.append(z + coords[j])
                        else:
                            k = partners[0]
                            l = None
                            m = None
                            if len(partners) == 1:
                                partners2 = [f for f in bond_map[k] if f < nog and f != j]
                                if len(partners2) > 0:
                                    l = partners2[0]
                                if len(partners2) > 1:
                                    m = partners2[1]
                            else:
                                l = partners[1]
                                if len(partners) > 2:
                                    m = partners[2]

                            if m is None:
                                r = nput.rotation_matrix(coords2[k] - coords2[j], coords[k] - coords[j])
                                if l is not None:
                                    x = nput.vec_normalize(coords[k] - coords[j])
                                    v2 = (coords2[l] - coords2[j]) @ r
                                    v2 = v2 - (np.dot(v2, x)) * x
                                    y = coords[l] - coords[j]
                                    y =  y - (np.dot(y, x)) * x
                                    r2 = nput.rotation_matrix(v2, y)
                                    r = r @ r2
                                z = (coords2[i] - coords2[j]) @ r
                                new_coords.append(z + coords[j])
                            else:
                                alignment = nput.eckart_embedding(
                                    coords[(j, k, l, m),], coords2[(j, k, l, m),]
                                )
                                new_pos = (
                                    # embed new coords in the original frame
                                        (coords2[[i],] - alignment.coord_data.com[np.newaxis])
                                        @ alignment.coord_data.axes
                                        @ alignment.rotations
                                        @ alignment.reference_data.axes.T
                                        + alignment.reference_data.com[np.newaxis]
                                )
                                new_coords.append(new_pos[0])
                coords3 = np.concatenate([coords, new_coords], axis=0)
        elif method == 'eckart':
            alignment = nput.eckart_embedding(
                coords, coords2[:len(coords)]
            )
            coords3 = (
                # embed new coords in the original frame
                    (coords2 - alignment.coord_data.com[np.newaxis])
                    @ alignment.coord_data.axes
                    @ alignment.rotations
                    @ alignment.reference_data.axes.T
                    + alignment.reference_data.com[np.newaxis]
            )
        else:
            coords3 = coords2

        return coords3

    implicit_hydrogen_to_conformer_method = 'builtin'
    @classmethod
    def from_coords(cls, atoms, coords, bonds=None,
                    charge=None,
                    formal_charges=None,
                    guess_bonds=None,
                    add_implicit_hydrogens=False,
                    implicit_hydrogen_method=None,
                    distance_matrix_tol=0.05,
                    num_confs=None,
                    optimize=False,
                    take_min=None,
                    force_field_type='mmff',
                    confgen_opts=None,
                    sanitize=False,
                    **opts
                    ):
        """
        **LLM Docstring**

        Build an `RDMolecule` from atoms, coordinates, and (optional) bonds, optionally
        adding implicit hydrogens (placed by conformer generation) and guessing bonds.

        :param atoms: the element symbols
        :type atoms: Sequence[str]
        :param coords: the Cartesian coordinates
        :type coords: np.ndarray
        :param bonds: the bonds as `[i, j(, order)]`
        :type bonds: Sequence | None
        :param charge: the molecular charge
        :type charge: int | None
        :param formal_charges: per-atom formal charges
        :type formal_charges: Sequence | None
        :param guess_bonds: perceive bonds from geometry (defaults to when no bonds given)
        :type guess_bonds: bool | None
        :param add_implicit_hydrogens: add implicit hydrogens
        :type add_implicit_hydrogens: bool
        :param implicit_hydrogen_method: how to place added hydrogens (`'align'`/`'initial'`/`'builtin'`)
        :type implicit_hydrogen_method: str | None
        :param distance_matrix_tol: tolerance for distance constraints when aligning
        :type distance_matrix_tol: float
        :param num_confs: number of conformers to generate
        :type num_confs: int | None
        :param optimize: force-field optimize generated conformers
        :type optimize: bool
        :param take_min: keep only the lowest-energy conformer
        :type take_min: bool | None
        :param force_field_type: the force field for optimization
        :type force_field_type: str
        :param confgen_opts: extra conformer-generation options
        :type confgen_opts: dict | None
        :param sanitize: run sanitization
        :type sanitize: bool
        :return: the wrapped molecule (or a list, when multiple conformers are kept)
        :rtype: RDMolecule | list
        """
        Chem = cls.allchem_api()
        mol = Chem.EditableMol(Chem.Mol())
        mol.BeginBatchEdit()
        if formal_charges is None:
            formal_charges = [None] * len(atoms)
        for a,fc in zip(atoms, formal_charges):
            a = Chem.Atom(a)
            if fc is not None:
                if nput.is_int(fc):
                    fc = int(fc)
                else:
                    fc = float(fc)
                a.SetFormalCharge(fc)
            mol.AddAtom(a)
        if bonds is not None:
            for b in bonds:
                if len(b) == 2:
                    i,j = b
                    t = 1
                else:
                    i,j,t = b
                if nput.is_numeric(t):
                    t = cls.resolve_bond_type(t)
                else:
                    t = Chem.BondType.names[t]
                mol.AddBond(int(i), int(j), t)
        mol.CommitBatchEdit()

        mol = mol.GetMol()
        cls._prep_mol(mol)
        if implicit_hydrogen_method is None:
            implicit_hydrogen_method = cls.implicit_hydrogen_to_conformer_method
            if (
                    implicit_hydrogen_method != "initial"
                    and num_confs is not None
            ):
                implicit_hydrogen_method = 'align'
        if add_implicit_hydrogens and implicit_hydrogen_method != "builtin":
            old_pos = {}
            cur_map_nums = [a.GetAtomMapNum() for a in mol.GetAtoms()]
            for i,a in enumerate(mol.GetAtoms()):
                a.SetAtomMapNum(i+1)
            mol = Chem.AddHs(mol, explicitOnly=False)
            for n,a in enumerate(mol.GetAtoms()):
                i = a.GetAtomMapNum()
                if i > 0:
                    a.SetAtomMapNum(cur_map_nums[i-1])
                    old_pos[n] = i - 1

            if confgen_opts is None:
                confgen_opts = {}
            if take_min is None:
                take_min = num_confs is None
            if num_confs is None:
                num_confs = 1
            base_opts = dict(
                num_confs=num_confs,
                optimize=optimize,
                take_min=take_min,
                force_field_type=force_field_type
            ) | opts | confgen_opts
            if implicit_hydrogen_method == 'align':
                dm = nput.distance_matrix(coords)
                distance_constraints = {
                    (old_pos[i], old_pos[j]): (dm[i, j] - distance_matrix_tol, dm[i, j] + distance_matrix_tol)
                    for i in range(len(coords))
                    for j in range(i + 1, len(coords))
                }
                base_opts["distance_constraints"] = distance_constraints
            elif implicit_hydrogen_method == "initial":
                base_opts["initial_coordinates"] = {
                    old_pos[i]:c
                    for i,c in enumerate(coords)
                }
            else:
                raise NotImplementedError(f"unknown initial hydrogen method {implicit_hydrogen_method}")

            conf_ids = cls.generate_conformers_for_mol(
                mol,
                **base_opts
            )
            if nput.is_int(conf_ids):
                try:
                    conf = mol.GetConformer(conf_ids)
                except ValueError:
                    import pprint
                    settings = pprint.pformat(base_opts)
                    smi = Chem.MolToSmiles(mol, canonical=False)
                    raise ValueError(f"failed to build conformer {conf_ids} for {smi} with settings {settings}")
                if implicit_hydrogen_method == 'align':
                    coords2 = conf.GetPositions()
                    coords3 = cls._align_new_conf_coords(mol, coords, coords2)
                    conf.SetPositions(coords3)
                return cls.from_rdmol(mol, conf_id=conf_ids, charge=charge, guess_bonds=guess_bonds,
                                      sanitize=sanitize)
            else:
                mols = []
                for i in conf_ids:
                    if implicit_hydrogen_method == 'align':
                        try:
                            conf = mol.GetConformer(i)
                        except ValueError:
                            continue
                        coords2 = conf.GetPositions()
                        conf.SetPositions(cls._align_new_conf_coords(mol, coords, coords2))
                    mols.append(
                        cls.from_rdmol(mol, conf_id=i, charge=charge, guess_bonds=guess_bonds,
                                       sanitize=sanitize)
                    )
                if len(mols) == 0:
                    import pprint
                    settings = pprint.pformat(dict(base_opts))
                    smi = Chem.MolToSmiles(mol, canonical=False)
                    raise ValueError(f"failed to build conformers {conf_ids} for {smi} with settings {settings}")
                return mols
        else:
            coords = np.asanyarray(coords)
            mol = Chem.AddHs(mol, explicitOnly=(len(atoms) == len(coords)))
            conf = Chem.Conformer(mol.GetNumAtoms())
            conf.SetPositions(coords)
            conf.SetId(0)
            mol.AddConformer(conf)
            if add_implicit_hydrogens:
                mol = Chem.AddHs(mol, explicitOnly=False, addCoords=True)

            if guess_bonds is None:
                guess_bonds = bonds is None

            return cls.from_rdmol(mol, conf_id=0, charge=charge, guess_bonds=guess_bonds, sanitize=sanitize)

    @classmethod
    def from_mol(cls, mol, coord_unit="Angstroms", guess_bonds=None):
        """
        **LLM Docstring**

        Build an `RDMolecule` from a generic molecule object, converting its coordinates
        to Angstroms.

        :param mol: the source molecule
        :param coord_unit: the source coordinate unit
        :type coord_unit: str
        :param guess_bonds: perceive bonds from geometry
        :type guess_bonds: bool | None
        :return: the wrapped molecule
        :rtype: RDMolecule
        """
        from ..Data import UnitsData

        return cls.from_coords(
            mol.atoms,
            mol.coords * UnitsData.convert(coord_unit, "Angstroms"),
            bonds=mol.bonds,
            charge=mol.charge,
            formal_charges=mol.formal_charges,
            guess_bonds=guess_bonds
        )

    @classmethod
    def _load_sdf_conf(cls, stream, which=0):
        """
        **LLM Docstring**

        Read the `which`-th molecule from an SDF stream.

        :param stream: the SDF byte stream
        :param which: the index of the entry to read
        :type which: int
        :return: the RDKit mol
        :rtype: Chem.Mol
        """
        Chem = cls.chem_api()
        mol = None
        for i in range(which+1):
            mol = next(Chem.ForwardSDMolSupplier(stream, sanitize=False, removeHs=False))
        return mol
    @classmethod
    def from_sdf(cls, sdf_string, which=0):
        """
        **LLM Docstring**

        Build an `RDMolecule` from an SDF file path or string.

        :param sdf_string: the SDF file path or content
        :type sdf_string: str
        :param which: the index of the entry to read
        :type which: int
        :return: the wrapped molecule
        :rtype: RDMolecule
        """
        if os.path.isfile(sdf_string):
            with open(sdf_string, 'rb') as stream:
                mol = cls._load_sdf_conf(stream, which=which)
        else:
            mol = cls._load_sdf_conf(io.BytesIO(sdf_string.encode()), which=which)
        return cls.from_rdmol(mol)

    @classmethod
    def get_confgen_opts(cls,
                         version='v3',
                         use_experimental_torsion_angle_prefs=True,
                         use_basic_knowledge=True,
                         **opts
                         ):
        """
        **LLM Docstring**

        Build an RDKit ETKDG conformer-generation parameter object of the requested
        version, applying the torsion/knowledge flags and any extra options.

        :param version: the ETKDG version (`'v1'`/`'v2'`/`'v3'`)
        :type version: str
        :param use_experimental_torsion_angle_prefs: use experimental torsion prefs
        :type use_experimental_torsion_angle_prefs: bool
        :param use_basic_knowledge: use basic chemical knowledge
        :type use_basic_knowledge: bool
        :param opts: extra parameters set on the params object (camel-cased)
        :return: the parameter object
        :rtype: object
        """
        AllChem = cls.allchem_api()
        version = version.lower()
        if version == 'v3':
            params = AllChem.ETKDGv3()
        elif version == 'v2':
            params = AllChem.ETKDGv2()
        elif version == 'v1':
            params = AllChem.ETKDG()
        else:
            raise ValueError(f"unknown ETKDG version {version}")
        params.useExpTorsionAnglePrefs = use_experimental_torsion_angle_prefs
        params.useBasicKnowledge = use_basic_knowledge
        for o,v in opts.items():
            o = "".join(b.capitalize() if i > 0 else b for i,b in enumerate(o.split("_")))
            setattr(params, o, v)
        return params
    @classmethod
    def parse_smiles(cls,
                     smiles,
                     sanitize=False,
                     parse_name=True,
                     allow_cxsmiles=True,
                     strict_cxsmiles=True,
                     remove_hydrogens=False,
                     add_implicit_hydrogens=None,
                     reorder_from_atom_map=False,
                     replacements=None,
                     quiet=False,
                     **opts
                     ):
        """
        **LLM Docstring**

        Parse a SMILES (or CXSMILES) string into an RDKit mol, with control over
        sanitization, hydrogen handling, and atom-map-based reordering.

        :param smiles: the SMILES string
        :type smiles: str
        :param sanitize: run sanitization
        :type sanitize: bool
        :param parse_name: parse a trailing molecule name
        :type parse_name: bool
        :param allow_cxsmiles: allow CXSMILES extensions
        :type allow_cxsmiles: bool
        :param strict_cxsmiles: fail on bad CXSMILES rather than ignoring
        :type strict_cxsmiles: bool
        :param remove_hydrogens: remove explicit hydrogens
        :type remove_hydrogens: bool
        :param add_implicit_hydrogens: add hydrogens (or `'full'` to also re-enable implicit Hs)
        :type add_implicit_hydrogens: bool | str | None
        :param reorder_from_atom_map: renumber atoms by their atom-map numbers
        :type reorder_from_atom_map: bool
        :param replacements: SMILES token replacements
        :type replacements: dict | None
        :param quiet: suppress RDKit logging
        :type quiet: bool
        :return: the parsed mol, or `None` on failure
        :rtype: Chem.Mol | None
        """
        Chem = cls.chem_api()
        if quiet:
            from rdkit.rdBase import BlockLogs
            with BlockLogs():
                return cls.parse_smiles(
                    smiles,
                    sanitize=sanitize,
                    parse_name=parse_name,
                    allow_cxsmiles=allow_cxsmiles,
                    strict_cxsmiles=strict_cxsmiles,
                    remove_hydrogens=remove_hydrogens,
                    replacements=replacements,
                    quiet=False,
                    **opts
                )

        params = Chem.SmilesParserParams()
        params.removeHs = remove_hydrogens
        params.sanitize = sanitize
        if replacements is not None:
            params.replacements = replacements
        params.parseName = parse_name
        params.allowCXSMILES = allow_cxsmiles
        params.strictCXSMILES = strict_cxsmiles
        for k, v in opts.items():
            setattr(params, k, v)

        rdkit_mol = Chem.MolFromSmiles(smiles, params)
        if rdkit_mol is None:
            return None
        if not sanitize:
            try:
                rdkit_mol.UpdatePropertyCache()
            except Chem.rdchem.MolSanitizeException:
                rdkit_mol.UpdatePropertyCache(strict=False)
                _ = Chem.GetSymmSSSR(rdkit_mol)
                Chem.SetHybridization(rdkit_mol)
        if add_implicit_hydrogens is not None:
            if dev.str_is(add_implicit_hydrogens, 'full'):
                add_implicit_hydrogens = True
                for atom in rdkit_mol.GetAtoms():
                    if atom.GetAtomMapNum() != 0:  # only fix mapped atoms
                        atom.SetNoImplicit(False)  # allow implicit Hs again
                        atom.SetNumExplicitHs(0)  # clear any explicit H count
            rdkit_mol = Chem.AddHs(rdkit_mol, explicitOnly=not add_implicit_hydrogens)

        if reorder_from_atom_map:
            base_map = [a.GetAtomMapNum() for a in rdkit_mol.GetAtoms()]
            base_map = [len(base_map)+1 if a == 0 else a for a in base_map]
            # need to use a stable sort
            rdkit_mol = Chem.RenumberAtoms(rdkit_mol, np.argsort(base_map, kind='merge').tolist())

        return rdkit_mol
    @classmethod
    def from_smiles(cls, smiles,
                    sanitize=False,
                    parse_name=True,
                    allow_cxsmiles=True,
                    strict_cxsmiles=True,
                    remove_hydrogens=False,
                    replacements=None,
                    add_implicit_hydrogens=False,
                    call_add_hydrogens=True,
                    conf_id=None,
                    num_confs=None,
                    optimize=False,
                    take_min=True,
                    force_field_type='mmff',
                    reorder_from_atom_map=True,
                    confgen_opts=None,
                    check_tag=True,
                    coords=None,
                    conf_tag=None,
                    **opts):
        """
        **LLM Docstring**

        Build an `RDMolecule` from a SMILES string (or file), embedding a conformer
        (generated, or decoded from a conformer tag / supplied coordinates).

        :param smiles: the SMILES string or file path
        :type smiles: str
        :param sanitize: run sanitization
        :type sanitize: bool
        :param parse_name: parse a trailing molecule name
        :type parse_name: bool
        :param allow_cxsmiles: allow CXSMILES extensions
        :type allow_cxsmiles: bool
        :param strict_cxsmiles: fail on bad CXSMILES
        :type strict_cxsmiles: bool
        :param remove_hydrogens: remove explicit hydrogens
        :type remove_hydrogens: bool
        :param replacements: SMILES token replacements
        :type replacements: dict | None
        :param add_implicit_hydrogens: add implicit hydrogens
        :type add_implicit_hydrogens: bool
        :param call_add_hydrogens: call `AddHs` before embedding
        :type call_add_hydrogens: bool
        :param conf_id: the conformer id to use
        :type conf_id: int | None
        :param num_confs: number of conformers to generate
        :type num_confs: int | None
        :param optimize: force-field optimize generated conformers
        :type optimize: bool
        :param take_min: keep only the lowest-energy conformer
        :type take_min: bool
        :param force_field_type: the force field for optimization
        :type force_field_type: str
        :param reorder_from_atom_map: renumber atoms by atom-map number
        :type reorder_from_atom_map: bool
        :param confgen_opts: extra conformer-generation options
        :type confgen_opts: dict | None
        :param check_tag: split off a trailing `_`-delimited conformer tag
        :type check_tag: bool
        :param coords: explicit coordinates to use instead of generating a conformer
        :type coords: np.ndarray | None
        :param conf_tag: an explicit conformer tag to decode
        :type conf_tag: str | None
        :return: the wrapped molecule (or list, for multiple conformers)
        :rtype: RDMolecule | list
        """

        if os.path.isfile(smiles):
            with open(smiles) as f:
                smiles = f.read()
        Chem = cls.chem_api()

        if check_tag and conf_tag is None:
            smiles, _, conf_tag = smiles.partition("_")
            if len(conf_tag) == 0: conf_tag = None

        rdkit_mol = cls.parse_smiles(
            smiles,
            sanitize=sanitize,
            parse_name=parse_name,
            allow_cxsmiles=allow_cxsmiles,
            strict_cxsmiles=strict_cxsmiles,
            remove_hydrogens=remove_hydrogens,
            replacements=replacements,
            add_implicit_hydrogens=add_implicit_hydrogens,
            reorder_from_atom_map=reorder_from_atom_map,
            **opts
        )

        if coords is None and conf_tag is not None:
            #TODO: add precision support
            graph = cls.get_mol_edge_graph(rdkit_mol)
            coords = cls.conformer_from_smiles_tag(conf_tag, graph)

        if coords is None:
            if call_add_hydrogens: # RDKit is super borked for most molecules
                mol = Chem.AddHs(rdkit_mol, explicitOnly=not add_implicit_hydrogens)
            else:
                mol = rdkit_mol

            return cls.from_base_mol(mol,
                                     conf_id=conf_id,
                                     num_confs=num_confs, optimize=optimize, take_min=take_min,
                                     force_field_type=force_field_type,
                                     confgen_opts=confgen_opts
                                     )
        else:
            return cls.from_coords(
                [a.GetSymbol() for a in rdkit_mol.GetAtoms()],
                coords,
                bonds=[
                    [b.GetBeginAtomIdx(), b.GetEndAtomIdx(), b.GetBondTypeAsDouble()]
                    for b in rdkit_mol.GetBonds()
                ],
                add_implicit_hydrogens=add_implicit_hydrogens,
                num_confs=num_confs, optimize=optimize, take_min=take_min,
                force_field_type=force_field_type,
                confgen_opts=confgen_opts
            )

        # rdDistGeom = RDKitInterface.submodule("Chem.rdDistGeom")
        # rdDistGeom.EmbedMolecule(mol, num_confs, **cls.get_confgen_opts())

    @classmethod
    def from_base_mol(cls,
                      mol,
                      conf_id=None,
                      num_confs=None,
                      optimize=False,
                      take_min=None,
                      force_field_type='mmff',
                      confgen_opts=None,
                      **mol_opts):
        """
        **LLM Docstring**

        Build an `RDMolecule` from an RDKit mol, using an existing conformer when
        available and otherwise generating one.

        :param mol: the source mol
        :type mol: Chem.Mol
        :param conf_id: the conformer id to use
        :type conf_id: int | None
        :param num_confs: number of conformers to generate
        :type num_confs: int | None
        :param optimize: force-field optimize generated conformers
        :type optimize: bool
        :param take_min: keep only the lowest-energy conformer
        :type take_min: bool | None
        :param force_field_type: the force field for optimization
        :type force_field_type: str
        :param confgen_opts: extra conformer-generation options
        :type confgen_opts: dict | None
        :param mol_opts: extra options forwarded to `from_rdmol`
        :return: the wrapped molecule (or list)
        :rtype: RDMolecule | list
        """
        conf = None
        if conf_id is not None:
            try:
                conf = mol.GetConformer(conf_id)
            except ValueError:
                ...
        if conf:
            return cls.from_rdmol(mol, conf_id, **mol_opts)
        else:
            if (
                    conf_id is not None
                    and num_confs is not None
                    and conf_id > num_confs + 1
            ):
                num_confs = conf_id
            if take_min is None:
                take_min = num_confs is None or conf_id is not None
            if num_confs is None:
                num_confs = 1
            return cls.from_no_conformer_molecule(mol,
                                                  conf_id=conf_id,
                                                  num_confs=num_confs,
                                                  optimize=optimize,
                                                  take_min=take_min,
                                                  force_field_type=force_field_type,
                                                  confgen_opts=confgen_opts,
                                                  **mol_opts
                                                  )

    default_fragment_placement_method = 'centroid'
    different_fragment_embedding_distance = 5
    @classmethod
    def _set_fragment_centroids(cls, frag_inds, frag_atoms, frag_bonds, frag_coord_sets, frag_positions, min_dist=None):
        """
        **LLM Docstring**

        Place disconnected fragments relative to one another by offsetting each
        fragment's inertial frame along a fixed displacement, returning the combined
        per-conformer coordinate sets.

        :param frag_inds: the original atom indices of each fragment
        :type frag_inds: list
        :param frag_atoms: the element symbols of each fragment
        :type frag_atoms: list
        :param frag_bonds: the bonds of each fragment
        :type frag_bonds: list
        :param frag_coord_sets: the per-conformer coordinates of each fragment
        :type frag_coord_sets: list
        :param frag_positions: optional target positions per fragment
        :type frag_positions: list
        :param min_dist: the inter-fragment separation
        :type min_dist: float | None
        :return: the combined coordinate sets
        :rtype: list
        """
        if min_dist is None:
            min_dist = cls.different_fragment_embedding_distance
        masses = [[AtomData[a, "Mass"] for a in fa] for fa in frag_atoms]
        # align axes by default
        conf_sets = []
        disp_vec = np.array([[0, 0, min_dist]])
        remapping = np.argsort(np.concatenate(frag_inds))
        for frag_coords in frag_coord_sets:
            cur_mass = masses[0]
            cur_coords = frag_coords[0]
            for m,c in zip(masses[1:], frag_coords[1:]):
                if len(cur_coords) == 1:
                    cur_com = cur_coords[0]
                    cur_axes = np.eye(3)
                else:
                    (_, cur_axes), cur_com = nput.moments_of_inertia(cur_coords, cur_mass, return_com=True)
                if len(frag_coords) == 1:
                    f_com = frag_coords[0]
                    f_axes = np.eye(3)
                else:
                    (_, f_axes), f_com = nput.moments_of_inertia(c, m, return_com=True)
                new_coords = (
                        (c - f_com[np.newaxis]) @ f_axes
                        + disp_vec
                ) @ cur_axes.T + cur_com[np.newaxis]
                cur_mass = np.concatenate([cur_mass, m])
                cur_coords = np.concatenate([cur_coords, new_coords], axis=0)
            conf_sets.append(cur_coords[remapping, :])
        return conf_sets
    @classmethod
    def _set_fragment_positions(cls, frag_inds, frag_atoms, frag_bonds,
                                frag_coord_sets,
                                frag_positions,
                                use_actual=False):
        """
        **LLM Docstring**

        Place disconnected fragments by aligning each onto supplied target positions
        (via a shift for one point or an Eckart embedding for several), returning the
        combined per-conformer coordinate sets.

        :param frag_inds: the original atom indices of each fragment
        :type frag_inds: list
        :param frag_atoms: the element symbols of each fragment
        :type frag_atoms: list
        :param frag_bonds: the bonds of each fragment
        :type frag_bonds: list
        :param frag_coord_sets: the per-conformer coordinates of each fragment
        :type frag_coord_sets: list
        :param frag_positions: the target positions (per fragment, keyed by atom)
        :type frag_positions: list
        :param use_actual: pin the mapped atoms exactly to their targets
        :type use_actual: bool
        :return: the combined coordinate sets
        :rtype: list
        """
        # align axes by default
        conf_sets = []
        remapping = np.argsort(np.concatenate(frag_inds))
        masses = [[AtomData[a, "Mass"] for a in fa] for fa in frag_atoms]
        for frag_coords in frag_coord_sets:
            cur_coords = None
            # ref = list(frag_positions[0].values())[0]
            for m,x,c in zip(masses, frag_positions, frag_coords):
                subc = [c[og] for og in x.keys()]
                m = [m[og] for og in x.keys()]
                targ = list(x.values())
                if len(targ) == 1:
                    dx = targ[0] - subc[0]
                    new_coords = c + dx[np.newaxis]
                else:
                    alignment = nput.eckart_embedding(
                        targ, subc, m
                    )
                    new_coords = (
                        # embed new coords in the original frame
                            (c - alignment.coord_data.com[np.newaxis])
                            @ alignment.coord_data.axes
                            @ alignment.rotations
                            @ alignment.reference_data.axes.T
                            + alignment.reference_data.com[np.newaxis]
                    )
                    if use_actual:
                        for og, pos in x.items():
                            new_coords[og] = pos
                if cur_coords is None:
                    cur_coords = new_coords
                else:
                    cur_coords = np.concatenate([cur_coords, new_coords], axis=0)
            conf_sets.append(cur_coords[remapping, :])
        return conf_sets

    @classmethod
    def _centroid_frag_dists(cls, mol, graph, fragments, min_dist=None):
        """
        **LLM Docstring**

        Compute the inter-fragment distance constraints between the fragments' graph
        centroids.

        :param mol: the mol
        :type mol: Chem.Mol
        :param graph: the molecular edge graph
        :param fragments: the fragment atom-index groups
        :type fragments: list
        :param min_dist: the minimum separation
        :type min_dist: float | None
        :return: the distance constraints between centroid atoms
        :rtype: object
        """
        from ..Graphs import EdgeGraph
        graph: EdgeGraph
        centroids = [
            graph.take(f).get_centroid(check_fragments=False)
            for f in fragments
        ]
        points = [
            (fragments[i][centroids[i]], fragments[j][centroids[j]])
            for i,j in itertools.combinations(range(len(centroids)), 2)
        ]
        return cls._connection_point_frag_distances(
            mol,
            points,
            min_dist=min_dist
        )
    @classmethod
    def _take_submol(cls, atoms, bonds, inds):
        """
        **LLM Docstring**

        Build a sub-mol containing only the given atom indices and the bonds among them.

        :param atoms: the full atom list
        :type atoms: list
        :param bonds: the full bond list
        :type bonds: list
        :param inds: the atom indices to keep
        :type inds: Sequence[int]
        :return: the sub-mol
        :rtype: Chem.Mol
        """
        Chem = cls.allchem_api()
        mol = Chem.EditableMol(Chem.Mol())
        bond_map = {}
        for b in bonds:
            i, j = (b.GetBeginAtomIdx(), b.GetEndAtomIdx())
            if i not in bond_map:
                bond_map[i] = {}
            bond_map[i][j] = b
            # if j not in bond_map:
            #     bond_map[j] = {}
            # bond_map[j][i] = b
        remapping = {i:j for j,i in enumerate(inds)}
        for i in inds:
            mol.AddAtom(atoms[i])
        for i in inds:
            for j,b in bond_map.get(i, {}).items():
                if j in inds:
                    mol.AddBond(remapping[b.GetBeginAtomIdx()], remapping[b.GetEndAtomIdx()], b.GetBondType())
        mol.CommitBatchEdit()
        return mol.GetMol()
    @classmethod
    def generate_conformers_for_mol(cls, mol,
                                    *,
                                    num_confs=1,
                                    optimize=False,
                                    take_min=True,
                                    force_field_type='mmff',
                                    add_implicit_hydrogens=False,
                                    distance_constraints=None,
                                    initial_coordinates=None,
                                    fragment_placement_method=None,
                                    fragments=None,
                                    embedding_mol=None,
                                    verbose=False,
                                    **opts
                                    ):
        """
        **LLM Docstring**

        Generate one or more conformers for a mol via RDKit's ETKDG embedding,
        handling disconnected fragments (embedded separately and placed), distance
        constraints, fixed initial coordinates, optional force-field optimization, and
        lowest-energy selection.

        :param mol: the mol to embed (modified in place; conformers are added)
        :type mol: Chem.Mol
        :param num_confs: number of conformers to generate
        :type num_confs: int
        :param optimize: force-field optimize the conformers
        :type optimize: bool
        :param take_min: return only the lowest-energy conformer id
        :type take_min: bool
        :param force_field_type: the force field for optimization/selection
        :type force_field_type: str
        :param add_implicit_hydrogens: add implicit hydrogens before embedding
        :type add_implicit_hydrogens: bool
        :param distance_constraints: pairwise distance bounds (or a full bounds matrix)
        :type distance_constraints: dict | list | None
        :param initial_coordinates: fixed starting coordinates for some/all atoms
        :type initial_coordinates: dict | Sequence | None
        :param fragment_placement_method: how to place disconnected fragments
        :type fragment_placement_method: str | Callable | None
        :param fragments: precomputed fragment atom groups
        :type fragments: list | None
        :param embedding_mol: a hydrogen-added mol to embed into
        :type embedding_mol: Chem.Mol | None
        :param verbose: don't suppress RDKit logging
        :type verbose: bool
        :return: the generated conformer id (or list of ids)
        :rtype: int | list
        """

        AllChem = cls.allchem_api()
        if embedding_mol is None:
            embedding_mol = AllChem.AddHs(mol, explicitOnly=not add_implicit_hydrogens)

        if fragments is None:
            fragments = cls.get_mol_edge_graph(mol).get_fragments()

        if len(fragments) > 1:
            if fragment_placement_method is None:
                if initial_coordinates is None:
                    fragment_placement_method = cls.default_fragment_placement_method
                else:
                    fragment_placement_method = cls._set_fragment_positions
            if fragment_placement_method == "centroid":
                fragment_placement_method = cls._set_fragment_centroids
            elif not callable(fragment_placement_method):
                raise NotImplementedError(
                    f"unhandled fragment embedding method {fragment_placement_method}")
            subatoms = []
            subbonds = []
            subconfs = []
            subpos = []
            single = False
            mol_atoms = list(mol.GetAtoms())
            mol_bonds = list(mol.GetBonds())
            for frag in fragments:
                frag_mol = cls._take_submol(mol_atoms, mol_bonds, frag)
                cls._prep_mol(frag_mol)
                if distance_constraints is not None:
                    raise NotImplementedError("adding per fragment distance constraints still required")
                if initial_coordinates is not None:
                    frag_coords = {
                        n: initial_coordinates[i]
                        for n, i in enumerate(frag)
                        if i in initial_coordinates
                    }
                else:
                    frag_coords = None
                subpos.append(frag_coords)
                frag_set = cls.generate_conformers_for_mol(
                    frag_mol,
                    num_confs=num_confs,
                    optimize=optimize,
                    take_min=take_min,
                    force_field_type=force_field_type,
                    add_implicit_hydrogens=False,
                    verbose=verbose,
                    fragments=[list(range(len(frag)))],
                    embedding_mol=frag_mol,
                    embed_fragments_separately=False,
                    initial_coordinates=frag_coords,
                    **opts
                )
                single = nput.is_int(frag_set)
                if single:
                    frag_set = [frag_set]
                subatoms.append(
                    [a.GetSymbol() for a in frag_mol.GetAtoms()]
                )
                subbonds.append(
                    [
                        (bond.GetBeginAtomIdx(), bond.GetEndAtomIdx())
                        for bond in frag_mol.GetBonds()
                    ]
                )
                subconfs.append(
                    [
                        frag_mol.GetConformer(i).GetPositions()
                        for i in frag_set
                    ]
                )

            coords = fragment_placement_method(
                fragments,
                subatoms,
                subbonds,
                list(zip(*subconfs)),
                subpos
            )

            conf_ids = list(range(len(coords)))
            for i,c in enumerate(coords):
                conf = AllChem.Conformer(len(c))
                conf.SetPositions(np.asanyarray(c))
                conf.SetId(i)
                mol.AddConformer(conf)
            if single:
                conf_ids = conf_ids[0]
            return conf_ids

        if embedding_mol is None:
            embedding_mol = mol


        params = cls.get_confgen_opts(**opts)
        if distance_constraints is not None:
            if hasattr(distance_constraints, 'items'):
                distance_constraints = list(distance_constraints.items())
            if len(distance_constraints) > 0:
                if (
                        len(distance_constraints) == len(mol.GetAtoms())
                        and nput.is_numeric_array_like(distance_constraints, 2)
                        and len(distance_constraints[0]) == len(distance_constraints)
                ):
                    bmat = np.array(distance_constraints)
                else:
                    cls._prep_mol(mol)
                    bmat = AllChem.GetMoleculeBoundsMatrix(mol)
                    for (i, j), (min_dist, max_dist) in distance_constraints:
                        if j > i: i,j = j,i
                        if max_dist is None or max_dist < 0:
                            bmat[i, j] = min_dist
                            if bmat[j, i] < min_dist:
                                bmat[j, i] += min_dist
                        elif min_dist is None or min_dist < 0:
                            bmat[j, i] = max_dist
                            if bmat[i, j] > max_dist:
                                bmat[i, j] = max_dist - .05
                        else:
                            if max_dist < min_dist: min_dist, max_dist = max_dist, min_dist
                            bmat[i, j] = min_dist
                            bmat[j, i] = max_dist
                params.SetBoundsMat(bmat)

        if initial_coordinates is not None:
            from rdkit.Geometry.rdGeometry import Point3D
            if not isinstance(initial_coordinates, dict):
                initial_coordinates = {
                    i:Point3D(*c)
                    for i,c in enumerate(initial_coordinates)
                }
            else:
                initial_coordinates = {
                    i: Point3D(*c)
                    for i, c in initial_coordinates.items()
                }
            params.SetCoordMap(initial_coordinates)

        if "embed_fragments_separately" in opts: # let this just error out
            cls._prep_mol(embedding_mol)
            conformer_set = AllChem.EmbedMultipleConfs(embedding_mol, numConfs=num_confs, params=params)
        else:
            try:
                # with OutputRedirect():
                with cls.quiet_errors(verbose=verbose):
                    conformer_set = AllChem.EmbedMultipleConfs(embedding_mol, numConfs=num_confs, params=params)
            except AllChem.rdchem.MolSanitizeException:
                conformer_set = None
                cls._prep_mol(embedding_mol)
            if conformer_set is None:
                params.embedFragmentsSeparately = False
                # with OutputRedirect():
                with cls.quiet_errors(verbose=verbose):
                    conformer_set = AllChem.EmbedMultipleConfs(embedding_mol, numConfs=num_confs, params=params)
        if len(conformer_set) == 0:
            conf_opts = opts | {
                "distance_constraints":distance_constraints,
                "initial_coordinates":initial_coordinates
            }
            raise ValueError(f"failed to generate conformers for {embedding_mol} with settings {conf_opts}")
        if optimize:
            rdForceFieldHelpers = RDKitInterface.submodule("Chem.rdForceFieldHelpers")
            if force_field_type == 'mmff':
                rdForceFieldHelpers.MMFFOptimizeMoleculeConfs(embedding_mol)
            elif force_field_type == 'uff':
                rdForceFieldHelpers.UFFOptimizeMoleculeConfs(embedding_mol)
            else:
                raise NotImplementedError(f"no basic preoptimization support for {force_field_type}")

        if take_min:
            if num_confs > 1:
                conf_ids = list(conformer_set)
                force_field_type = cls.get_force_field_type(force_field_type)
                if isinstance(force_field_type, (list, tuple)):
                    force_field_type, prop_gen = force_field_type
                else:
                    prop_gen = None

                if prop_gen is not None:
                    props = prop_gen(embedding_mol)
                else:
                    props = None

                engs = [
                    force_field_type(embedding_mol, props, confId=conf_id).CalcEnergy()
                    for conf_id in conf_ids
                ]

                conf_id = conf_ids[np.argmin(engs)]
            else:
                conf_id = 0
        else:
            conf_id = list(conformer_set)

        if embedding_mol is not mol and conf_id is not None:
            # copy conformers back to mol
            emb_ids = conf_id
            if nput.is_int(emb_ids): emb_ids = [emb_ids]
            for i in emb_ids:
                conf = embedding_mol.GetConformer(i)
                mol.AddConformer(conf)

        return conf_id

    @classmethod
    def from_no_conformer_molecule(cls,
                                   mol,
                                   *,
                                   conf_id=None,
                                   num_confs=1,
                                   optimize=False,
                                   take_min=True,
                                   force_field_type='mmff',
                                   add_implicit_hydrogens=False,
                                   confgen_opts=None,
                                   **etc
                                   ):
        """
        **LLM Docstring**

        Generate conformer(s) for a mol that has none, then wrap the result(s) as
        `RDMolecule`(s).

        :param mol: the source mol
        :type mol: Chem.Mol
        :param conf_id: a specific conformer id to keep (disables optimization)
        :type conf_id: int | None
        :param num_confs: number of conformers to generate
        :type num_confs: int
        :param optimize: force-field optimize the conformers
        :type optimize: bool
        :param take_min: keep only the lowest-energy conformer
        :type take_min: bool
        :param force_field_type: the force field for optimization
        :type force_field_type: str
        :param add_implicit_hydrogens: add implicit hydrogens
        :type add_implicit_hydrogens: bool
        :param confgen_opts: extra conformer-generation options
        :type confgen_opts: dict | None
        :param etc: extra options forwarded to `from_rdmol`
        :return: the wrapped molecule (or list)
        :rtype: RDMolecule | list
        """
        if confgen_opts is None:
            confgen_opts = {}
        if conf_id is not None and conf_id >= 0:
            optimize = False
        else:
            conf_id = None
        ci = cls.generate_conformers_for_mol(mol,
                                             num_confs=num_confs,
                                             optimize=optimize,
                                             take_min=take_min,
                                             force_field_type=force_field_type,
                                             **confgen_opts)
        if conf_id is None:
            conf_id = ci
        if isinstance(conf_id, list):
            return [
                cls.from_rdmol(mol, conf_id=c, add_implicit_hydrogens=add_implicit_hydrogens, **etc)
                for c in conf_id
            ]
        else:
            return cls.from_rdmol(mol, conf_id=conf_id, add_implicit_hydrogens=add_implicit_hydrogens, **etc)

    @staticmethod
    def _camel_case(o, caps_all=False):
        """
        **LLM Docstring**

        Convert a snake_case string to camelCase (or PascalCase when `caps_all` is set),
        for mapping option names onto RDKit's API.

        :param o: the snake_case string
        :type o: str
        :param caps_all: capitalize the first word too
        :type caps_all: bool
        :return: the camel-cased string
        :rtype: str
        """
        if caps_all:
            return "".join(b.capitalize() for b in o.split("_"))
        else:
            return "".join(b.capitalize() if i > 0 else b for i,b in enumerate(o.split("_")))
    def to_smiles(self,
                  remove_hydrogens=None,
                  remove_implicit_hydrogens=None,
                  include_tag=False, canonical=False,
                  compute_stereo=False,
                  remove_stereo=False,
                  preserve_atom_order=False,
                  binary=False,
                  coords=None,
                  mol=None,
                  **opts):
        """
        **LLM Docstring**

        Serialize the molecule to a SMILES string, with options for hydrogen/stereo
        handling, atom-order preservation, and appending a conformer tag encoding the
        3D geometry.

        :param remove_hydrogens: remove explicit hydrogens
        :type remove_hydrogens: bool | None
        :param remove_implicit_hydrogens: remove only implicit hydrogens
        :type remove_implicit_hydrogens: bool | None
        :param include_tag: append a `_`-delimited conformer tag
        :type include_tag: bool
        :param canonical: emit canonical SMILES
        :type canonical: bool
        :param compute_stereo: assign stereochemistry from the 3D coordinates first
        :type compute_stereo: bool
        :param remove_stereo: strip stereochemistry
        :type remove_stereo: bool
        :param preserve_atom_order: keep the current atom ordering
        :type preserve_atom_order: bool
        :param binary: return/encode the tag in binary form
        :type binary: bool
        :param coords: coordinates to encode in the tag (defaults to the current ones)
        :type coords: np.ndarray | None
        :param mol: an explicit mol to serialize (defaults to this one)
        :type mol: Chem.Mol | None
        :return: the SMILES string (optionally with a conformer tag)
        :rtype: str | bytes
        """
        Chem = self.allchem_api()
        if mol is None:
            mol = self.rdmol
        if compute_stereo:
            mol = Chem.Mol(mol)
            if coords is None:
                coords = self.coords
            conf = Chem.Conformer(len(coords))
            conf.SetPositions(np.asanyarray(coords))
            conf.SetId(0)
            mol.AddConformer(conf)
            Chem.AssignStereochemistryFrom3D(mol, confId=0)
        elif remove_stereo:
            mol = Chem.Mol(mol)
            Chem.RemoveStereochemistry(mol)
        if preserve_atom_order:
            og_atom_map = list(range(mol.GetNumAtoms()))
            for atom in mol.GetAtoms():
                atom.SetAtomMapNum(atom.GetIdx() + 1)
        else:
            og_atom_map = [
                atom.GetAtomMapNum()
                for atom in mol.GetAtoms()
            ]
        if remove_hydrogens is None:
            remove_hydrogens = remove_implicit_hydrogens
        if remove_hydrogens:
            if remove_implicit_hydrogens is None: remove_implicit_hydrogens = False
            mol = Chem.Mol(mol)
            if include_tag and not preserve_atom_order:
                for atom in mol.GetAtoms():
                    atom.SetAtomMapNum(atom.GetIdx()+1)
            mol = Chem.RemoveHs(mol, implicitOnly=remove_implicit_hydrogens, sanitize=False, updateExplicitCount=False)
        new_opts = {
            self._camel_case(k):v for k,v in opts.items()
        }
        if include_tag:
            if coords is None:
                coords = self.coords
            if remove_hydrogens:
                if not preserve_atom_order:
                    coords = [
                        coords[atom.GetAtomMapNum() - 1] for atom in mol.GetAtoms()
                    ]
                    for atom in mol.GetAtoms():
                        atom.SetAtomMapNum(og_atom_map[atom.GetAtomMapNum() - 1])
                else:
                    remapping = np.array([
                        atom.GetAtomMapNum() - 1
                        for atom in mol.GetAtoms()
                    ])
                    suborder = np.argsort(remapping, kind='merge')
                    coords = [
                        coords[o]
                        for o in remapping[suborder]
                    ]
                    for atom,o in zip(mol.GetAtoms(), suborder):
                        atom.SetAtomMapNum(int(o+1))
            smi = Chem.MolToSmiles(mol, canonical=canonical, **new_opts)
            # track coordinates into new Mol
            if not preserve_atom_order:
                mol = Chem.Mol(mol)
                for atom in mol.GetAtoms():
                    atom.SetAtomMapNum(atom.GetIdx()+1)
                ord_smi = Chem.MolToSmiles(mol, canonical=canonical, **new_opts)
                ord_mol = self.parse_smiles(ord_smi, remove_hydrogens=False)
                coords = [
                    coords[atom.GetAtomMapNum()-1]
                    for atom in ord_mol.GetAtoms()
                ]
            else:
                ord_mol = self.parse_smiles(smi, remove_hydrogens=remove_hydrogens)
                base_map = [a.GetAtomMapNum() for a in ord_mol.GetAtoms()]
                base_map = [len(base_map) + 1 if a == 0 else a for a in base_map]
                # need to use a stable sort
                ord_mol = Chem.RenumberAtoms(ord_mol, np.argsort(base_map, kind='merge').tolist())
            graph = self.get_edge_graph(ord_mol)
            tag = self.conformer_smiles_tag(coords=coords, graph=graph, binary=binary)
            if binary:
                smi = smi.encode()
                smi = smi + b"_" + tag
            else:
                smi = smi+"_"+tag
        else:
            smi = Chem.MolToSmiles(mol, canonical=canonical, **new_opts)
        return smi

    draw_options_mapping = {

    }
    drawing_defaults = {
        # dispatched by format
        None: {'image_size':[500, 200]}
    }
    @classmethod
    def _draw_ipython(cls, mol, format='svg', **opts):
        """
        **LLM Docstring**

        Configure RDKit's IPython console drawing options and display the mol inline.

        :param mol: the mol to display
        :type mol: Chem.Mol
        :param format: `'svg'` or `'png'`
        :type format: str
        :param opts: drawing options (camel-cased onto the RDKit draw options)
        :return: the display result
        :rtype: object
        """
        from rdkit.Chem.Draw import IPythonConsole
        from ..Jupyter.JHTML.WidgetTools import JupyterAPIs
        if format == 'svg':
            IPythonConsole.ipython_useSVG = True
        elif format == 'png':
            IPythonConsole.ipython_useSVG = False

        draw_opts = IPythonConsole.drawOptions
        for  k, v in opts.items():
            setattr(draw_opts, cls._camel_case(k), v)
        return JupyterAPIs.get_display_api().display(mol)

    @classmethod
    def _drawer_png(cls, *, image_size, plot_range=None, no_free_type=None, **opts):
        """
        **LLM Docstring**

        Build a PNG (raster) RDKit 2D drawer at the given image size, optionally with a
        fixed plot range/scale.

        :param image_size: the `(width, height)` of the image
        :type image_size: Sequence[int]
        :param plot_range: `((min_x, max_x), (min_y, max_y))` to fix the scale
        :type plot_range: tuple | None
        :param no_free_type: disable FreeType font rendering
        :type no_free_type: bool | None
        :param opts: remaining (unconsumed) options
        :return: `(drawer, remaining_opts)`
        :rtype: tuple
        """
        Chem = cls.chem_api()
        import rdkit.Geometry as Geom
        rdMolDraw2D = Chem.Draw.rdMolDraw2D
        # from rdkit.Chem.Draw import rdMolDraw2D
        if no_free_type is not None:
            drawer = rdMolDraw2D.MolDraw2DSVG(*image_size, noFreetype=no_free_type)
        else:
            drawer = rdMolDraw2D.MolDraw2DSVG(*image_size)
        if plot_range is not None:
            (min_x, max_x), (min_y, max_y) = plot_range
            scale = tuple(image_size) + (
                Geom.Point2D(min_x, min_y),
                Geom.Point2D(max_x, max_y)
            )
            drawer.SetScale(*scale)
        return drawer, opts
    @classmethod
    def _drawer_svg(cls, *, image_size, plot_range=None, no_free_type=None, **opts):
        """
        **LLM Docstring**

        Build an SVG RDKit 2D drawer at the given image size, optionally with a fixed
        plot range/scale.

        :param image_size: the image size (a scalar is squared)
        :type image_size: Sequence[int] | int
        :param plot_range: `((min_x, max_x), (min_y, max_y))` to fix the scale
        :type plot_range: tuple | None
        :param no_free_type: disable FreeType font rendering
        :type no_free_type: bool | None
        :param opts: remaining (unconsumed) options
        :return: `(drawer, remaining_opts)`
        :rtype: tuple
        """
        Chem = cls.chem_api()
        import rdkit.Geometry as Geom
        rdMolDraw2D = Chem.Draw.rdMolDraw2D
        # from rdkit.Chem.Draw import rdMolDraw2D
        if nput.is_numeric(image_size):
            image_size = [image_size, image_size]
        if no_free_type is not None:
            drawer = rdMolDraw2D.MolDraw2DSVG(*image_size, noFreetype=no_free_type)
        else:
            drawer = rdMolDraw2D.MolDraw2DSVG(*image_size)
        if plot_range is not None:
            (min_x, max_x), (min_y, max_y) = plot_range
            scale = tuple(image_size) + (
                Geom.Point2D(min_x, min_y),
                Geom.Point2D(max_x, max_y)
            )
            drawer.SetScale(*scale)
        return drawer, opts

    @classmethod
    def _prep_draw_opts(cls, format, opts):
        """
        **LLM Docstring**

        Merge the default drawing options (global and per-format) with the supplied
        options, dropping any `None` values.

        :param format: the output format
        :type format: str
        :param opts: the user-supplied options
        :type opts: dict
        :return: the merged options
        :rtype: dict
        """
        return {
            k:v
            for k,v in (
                cls.drawing_defaults.get(None, {})
                | cls.drawing_defaults.get(format, {})
                | opts
            ).items()
            if v is not None
        }

    @classmethod
    def _manage_draw_opts(cls,
                          label_style=None,
                          **etc
                          ):
        """
        **LLM Docstring**

        Translate high-level label-style options (font size, color) into the low-level
        RDKit annotation-scale/color options, returning the RDKit options plus the
        deferred style values.

        :param label_style: a `{font_size, color}` style dict
        :type label_style: dict | None
        :param etc: the remaining options
        :return: `(rdkit_options, deferred_style)`
        :rtype: tuple
        """
        deferred = {}
        if label_style is not None:
            font_size = label_style.get('font_size')
            if font_size is not None:
                etc['annotation_font_scale'] = 1.0/28 * font_size
                deferred['font_size'] = font_size
            color = label_style.get('color')
            if color is not None:
                etc['atom_note_color'] = color
                etc['bond_note_color'] = color
                etc['annotation_color'] = color
                # etc['color'] = color
                deferred['color'] = color

        return etc, deferred

    @staticmethod
    def _set_font_file(draw_opts, font_name):
        """
        **LLM Docstring**

        Set the drawer's font file, resolving a font *name* to a file path via
        matplotlib's font manager when needed.

        :param draw_opts: the RDKit draw-options object (modified in place)
        :param font_name: a font file path or font family name
        :type font_name: str
        """
        if len(font_name) > 0 and not os.path.isfile(font_name):
            from matplotlib import font_manager
            font_file = font_manager.findfont(font_name)
        else:
            font_file = font_name
        draw_opts.fontFile = font_file
    @staticmethod
    def _get_font_file(draw_opts):
        """
        **LLM Docstring**

        Return the drawer's currently configured font file.

        :param draw_opts: the RDKit draw-options object
        :return: the font file path
        :rtype: str
        """
        return draw_opts.fontFile
    _drawer_opts = {
        'fill_polys':'fill_polys',
        'color':(None, 'set_colour', 'black'),
        'font_size':'font_size'
    }
    _getter_draw_opts = {
        'background':'background_colour',
        'annotation_color':'annotation_colour',
        'atom_note_color':'atom_note_colour',
        'bond_note_color':'atom_note_colour',
        'query_color':'query_colour',
        'font_family':(_get_font_file, _set_font_file)
    }
    @classmethod
    def _handle_color(cls, v):
        """
        **LLM Docstring**

        Normalize a color (name/string or RGB sequence) into an RDKit `(r, g, b)` tuple
        in `[0, 1]`.

        :param v: the color specification
        :type v: str | Sequence | None
        :return: the normalized color tuple, or `None`
        :rtype: tuple | None
        """
        from ..Plots import ColorPalette
        if v is None: return None
        if isinstance(v, str):
            v = np.array(ColorPalette.parse_color_string(v))
            v = tuple(v/255)
        return tuple(float(vv) for vv in v)
    @classmethod
    def _handle_draw_elements(cls, elements):
        """
        **LLM Docstring**

        Resolve a draw-element specification (names or flags) into the combined RDKit
        `DrawElement` bit mask.

        :param elements: the element name(s)/flag(s)
        :type elements: list | tuple | object
        :return: the element mask
        :rtype: object
        """
        import rdkit.Chem.Draw.rdMolDraw2D as Draw
        if isinstance(elements, (list, tuple)):
            elements = [
                getattr(Draw.DrawElement, cls._camel_case(k).upper())
                    if isinstance(k, str) else
                k
                for k in elements
            ]
            if len(elements) == 1:
                element_mask = elements[0]
            else:
                element_mask = Draw.DrawElement.ALL
                for k in elements:
                    element_mask = element_mask ^ k
        else:
            element_mask = elements
        return element_mask
    @classmethod
    def _get_draw_opt(cls, drawer, draw_options, k):
        """
        **LLM Docstring**

        Read a drawing option, dispatching to the drawer method, the draw-options
        getter, or a plain attribute depending on where the option lives.

        :param drawer: the RDKit drawer
        :param draw_options: the drawer's options object
        :param k: the option name
        :type k: str
        :return: the option value
        :rtype: Any
        """
        if k in cls._drawer_opts:
            k = cls._drawer_opts[k]
            if isinstance(k, str):
                return getattr(drawer, cls._camel_case(k, caps_all=True))()
            else:
                if k[0] is not None:
                    if not isinstance(k[0], str):
                        return k[0](drawer)
                    else:
                        return getattr(drawer, cls._camel_case(k[0], caps_all=True))()
                elif hasattr(drawer, '_'+k[1]):
                    return getattr(drawer, "_"+k[1])
                elif len(k) > 2:
                    return k[2]
        elif k in cls._getter_draw_opts:
            k = cls._getter_draw_opts[k]
            if isinstance(k, str):
                return getattr(draw_options, cls._camel_case("get_"+k))()
            else:
                if not isinstance(k[0], str):
                    return k[0](draw_options)
                else:
                    return getattr(draw_options, cls._camel_case(k[0]))()
        else:
            return getattr(draw_options, cls._camel_case(k))
    @classmethod
    def _set_draw_opt(cls, drawer, draw_options, k, v):
        """
        **LLM Docstring**

        Set a drawing option, dispatching to the drawer method, the draw-options setter,
        or a plain attribute, and normalizing colors/element masks as needed.

        :param drawer: the RDKit drawer
        :param draw_options: the drawer's options object
        :param k: the option name
        :type k: str
        :param v: the value to set (ignored if `None`)
        :return: the setter's return value, if any
        :rtype: Any
        """
        if v is not None:
            if k in cls._drawer_opts:
                k = cls._drawer_opts[k]
                if isinstance(k, str):
                    if k.endswith('colour'):
                        v = cls._handle_color(v)
                    return getattr(drawer, cls._camel_case('set_'+k, caps_all=True))(v)
                else:
                    if k[1] is not None:
                        if not isinstance(k[1], str):
                            return k[1](drawer, v)
                        else:
                            if k[0] is None:
                                setattr(drawer, "_"+k[1], v)
                            if k[1].endswith('colour'):
                                v = cls._handle_color(v)
                            return getattr(drawer, cls._camel_case(k[1], caps_all=True))(v)
            elif k in cls._getter_draw_opts:
                k = cls._getter_draw_opts[k]
                if isinstance(k, str):
                    if k.endswith('colour'):
                        v = cls._handle_color(v)
                    return getattr(draw_options, cls._camel_case("set_"+k))(v)
                else:
                    if not isinstance(k[1], str):
                        return k[1](draw_options, v)
                    else:
                        if k[1].endswith('colour'):
                            v = cls._handle_color(v)
                        return getattr(draw_options, cls._camel_case(k[1]))(v)
            else:
                if k in {
                    'enabled_elements',
                    'drawing_extents_include'
                }:
                    v = cls._handle_draw_elements(v)
                return setattr(draw_options, cls._camel_case(k), v)
    @classmethod
    def _handle_annotation_draw(cls, caller, drawer, draw_options, *args, styles:dict, **kwargs):
        """
        **LLM Docstring**

        Temporarily apply a set of drawing-option overrides, invoke a draw callback, then
        restore the original options.

        :param caller: the draw callback to invoke
        :type caller: Callable
        :param drawer: the RDKit drawer
        :param draw_options: the drawer's options object
        :param args: positional arguments for the callback
        :param styles: the option overrides to apply during the call
        :type styles: dict
        :param kwargs: keyword arguments for the callback
        """
        cur_draw_options = {
            k: cls._get_draw_opt(drawer, draw_options, k)
            for k in styles
        }
        for k, v in styles.items():
            cls._set_draw_opt(drawer, draw_options, k, v)
        # try:
        #     annotations = drawer.annotations
        # except AttributeError:
        #     annotations = []
        #     drawer.annotations = annotations
        # annotations.append()
        caller(*args, **kwargs)
        for k, v in cur_draw_options.items():
            cls._set_draw_opt(drawer, draw_options, k, v)

    @classmethod
    def _prep_draw_coords(cls, draw_coords):
        """
        **LLM Docstring**

        Normalize the various accepted `draw_coords` forms (dict, list of keys, list of
        dicts) into a uniform list of `{key, ...}` annotation dicts.

        :param draw_coords: the annotation coordinate specifications
        :type draw_coords: dict | list | None
        :return: the normalized annotation dicts
        :rtype: list[dict]
        """
        if draw_coords is None:
            return []
        if isinstance(draw_coords, dict):
            _ = []
            for k, v in draw_coords.items():
                if isinstance(v, str):
                    v = {'label':v}
                v = v.copy()
                v['key'] = k
                _.append(v)
            draw_coords = _
        draw_coords = [
            {'key': d}
            if not isinstance(d, dict) else
            d
            for d in draw_coords
        ]

        return draw_coords

    default_draw_options = {
        'annotation_font_scale':1
    }
    @classmethod
    def _draw_non_interactive(cls,
                              mol,
                              figure=None,
                              format='svg',
                              drawer=None,
                              drawer_options=None,
                              legend=None,
                              highlight_atoms=None,
                              highlight_bonds=None,
                              highlight_atom_colors=None,
                              highlight_bond_colors=None,
                              highlight_atom_radii=None,
                              highlight_bond_radii=None,
                              coords=None,
                              draw_coords=None,
                              plot_range=None,
                              conf_id=None,
                              predraw=None,
                              return_splits=False,
                              no_free_type=None,
                              **opts
                              ):
        """
        **LLM Docstring**

        Render a mol to a static SVG/PNG with RDKit's 2D drawer, applying highlights,
        legends, coordinate annotations, a fixed plot range, and optional pre-draw
        callbacks.

        :param mol: the mol to draw
        :type mol: Chem.Mol
        :param figure: an existing figure/drawer to draw into
        :param format: `'svg'` or `'png'`
        :type format: str
        :param drawer: an explicit drawer to use
        :param drawer_options: extra drawer construction options
        :type drawer_options: dict | None
        :param legend: a legend string
        :type legend: str | None
        :param highlight_atoms: atoms to highlight
        :param highlight_bonds: bonds to highlight
        :param highlight_atom_colors: per-atom highlight colors
        :param highlight_bond_colors: per-bond highlight colors
        :param highlight_atom_radii: per-atom highlight radii
        :param highlight_bond_radii: per-bond highlight radii
        :param coords: 2D coordinates to draw at (defaults to the conformer's)
        :type coords: np.ndarray | None
        :param draw_coords: extra coordinate annotations
        :param plot_range: a fixed drawing range
        :type plot_range: tuple | None
        :param conf_id: the conformer id
        :type conf_id: int | None
        :param predraw: a callback invoked before finishing the drawing
        :type predraw: Callable | None
        :param return_splits: also return the drawing element split metadata
        :type return_splits: bool
        :param no_free_type: disable FreeType font rendering
        :type no_free_type: bool | None
        :return: the rendered image (and split metadata if requested)
        :rtype: object
        """
        Draw = RDKitInterface.submodule("Chem.Draw")
        import rdkit.Chem.Draw.rdMolDraw2D as rdMolDraw2D

        splits = None
        split_start = None
        if return_splits:
            splits = {
                'mol':[],
                'annotations':[],
                'labels':[]
            }

        if drawer is None:
            if figure is not None:
                if hasattr(figure, 'figure'):
                    drawer = figure.figure
                else:
                    drawer = figure
            if drawer_options is None:
                drawer_options = {}
            draw_opts = cls._prep_draw_opts(format,
                                            opts
                                                | dict(no_free_type=no_free_type, plot_range=plot_range)
                                                | drawer_options
                                            )
            if format == 'svg':
                _, opts = cls._drawer_svg(**draw_opts)
            else:
                _, opts = cls._drawer_png(**draw_opts)
            if drawer is None:
                drawer = _
        opts, deferred = cls._manage_draw_opts(**(cls.default_draw_options | opts))
        if len(opts) > 0:
            dops = drawer.drawOptions()
            for k,v in opts.items():
                cls._set_draw_opt(drawer, dops, k, v)
        if coords is None:
            coords = mol.GetConformer(conf_id).GetPositions()
        _coords = coords
        opts = {
            cls._camel_case(k): v for k, v in dict(
                legend=legend,
                # conf_id=conf_id,
                highlight_atoms=highlight_atoms,
                highlight_bonds=highlight_bonds,
                highlight_atom_colors=highlight_atom_colors,
                highlight_bond_colors=highlight_bond_colors,
                highlight_atom_radii=highlight_atom_radii,
                highlight_bond_radii=highlight_bond_radii
                ).items()
            if v is not None
        }
        if predraw is not None:
            drawer = predraw(drawer)
        if splits is not None:
            split_start = len(drawer.GetDrawingText())
        if "highlightBondRadii" in opts:
            mol = rdMolDraw2D.PrepareMolForDrawing(mol, kekulize=False, addChiralHs=False)
            conf = mol.GetConformer()
            conf.SetPositions(_coords)
            opts['confId'] = conf.GetId()
            drawer.DrawMoleculeWithHighlights(mol,
                                              opts.get("legend", ""),
                                              {k:[tuple(float(cc) for cc in c)] for k,c in opts.get("highlightAtomColors", {}).items()},
                                              {k:[tuple(float(cc) for cc in c)] for k,c in opts.get("highlightBondColors", {}).items()},
                                              opts.get("highlightAtomRadii", {}),
                                              opts.get("highlightBondRadii", {}),
                                              )
        else:
            mol = rdMolDraw2D.PrepareMolForDrawing(mol, kekulize=False, addChiralHs=False)
            conf = mol.GetConformer()
            conf.SetPositions(_coords)
            opts['confId'] = conf.GetId()
            drawer.DrawMolecule(mol, **opts)
        if splits is not None:
            split_end = len(drawer.GetDrawingText())
            splits['mol'].append([split_start, split_end])
            split_start = split_end
        if len(deferred) > 0:
            dops = drawer.drawOptions()
            for k,v in deferred.items():
                cls._set_draw_opt(drawer, dops, k, v)
        if draw_coords is not None:
            import rdkit.Chem.Draw as Draw
            import rdkit.Geometry as Geom
            drawer: Draw.MolDraw2D
            draw_options = drawer.drawOptions()
            draw_coords = cls._prep_draw_coords(draw_coords)
            all_coords = coords
            if plot_range is None:
                plot_range = [
                    [
                        np.min(all_coords[..., i]) - .1,
                        np.max(all_coords[..., i]) + .1,
                    ]
                    for i in range(2)
                ]
            x_range, y_range = plot_range
            x_span = x_range[1] - x_range[0]
            y_span = y_range[1] - y_range[0]
            for v in draw_coords:
                v = v.copy()
                k = v.pop('key', None)
                type = v.get("type")
                if type is None:
                    if isinstance(k, str):
                        type = k
                    elif len(k) == 1:
                        type = 'label'
                    elif len(k) == 2:
                        type = 'line'
                    elif len(k) == 3:
                        type = 'arc'
                    else:
                        type = 'polygon'

                label_style = None
                label_position = None
                label_text = None
                if type in {'line', 'arrow'}:
                    coords = v.get('coords')
                    if coords is None:
                        coords = all_coords[k, :2]
                    scaling = v.get('scaling', .9)
                    if scaling is not None:
                        u = (coords[1] - coords[0])
                        coords = [
                            coords[0] + (1 - scaling) * u,
                            coords[0] + scaling * u
                        ]
                    offset = v.get('offset')
                    if offset is not None:
                        u = nput.rotation_matrix('2d', np.pi/2) @ nput.vec_normalize(coords[1] - coords[0])
                        coords = [
                            coords[0] + offset * u,
                            coords[1] + offset * u
                        ]

                    label = v.get('label')
                    if label is not None:
                        if isinstance(label, str):
                            label = {'text': label}
                        label_text = label['text']
                        pos = label.get('position')
                        if pos is None:
                            offset = label.get('offset', .1)
                            scaled_offset = label.get('offset_scaled', 'absolute')
                            if nput.is_numeric(offset):
                                offset = [offset, 0]
                            if dev.str_is(scaled_offset, 'absolute'):
                                y = nput.vec_normalize(coords[0] - coords[1])
                                total_span = np.dot(y, [x_span, y_span])
                                y *= total_span
                            elif scaled_offset:
                                y = (coords[0] - coords[1])
                            else:
                                y = nput.vec_normalize(coords[0] - coords[1])
                            x = nput.rotation_matrix('2d', np.pi / 2) @ y
                            pos = (coords[0] + coords[1])/2 + np.dot(offset, [x, y])
                        label_position = pos
                        label_style = label.copy()
                        label_style = label_style | v.pop('label_style', {})
                        for k in (
                                'text', 'offset', 'position', 'offset_scaled'
                        ): label_style.pop(k, None)

                    styles = v.get('styles')
                    if styles is None:
                        styles = v.copy()
                        for k in ('type', 'coords', 'scaling', 'offset', 'label', 'label_style'): styles.pop(k, None)
                    if (
                            label_style is not None
                            and 'color' not in label_style
                    ):
                        test_color = styles.get('color')
                        if test_color is not None:
                            label_style['color'] = test_color
                    test_color = styles.get('color', True)
                    if test_color is not None:
                        if splits is not None:
                            split_start = len(drawer.GetDrawingText())
                        cls._handle_annotation_draw(
                            drawer.DrawLine
                                if type == 'line' else
                            drawer.DrawArrow,
                            drawer,
                            draw_options,
                            Geom.Point2D(*coords[0]), Geom.Point2D(*coords[1]),
                            styles=styles
                        )
                        if splits is not None:
                            split_end = len(drawer.GetDrawingText())
                            splits['annotations'].append([split_start, split_end])
                            split_start = split_end
                elif type == 'arc':
                    center = v.get('center')
                    angle = v.get('angle')
                    radius = v.get('radius')
                    start_angle = v.get('start_angle')
                    coords = v.get('coords')
                    if coords is None:
                        coords = all_coords[k, :2]
                    if center is None:
                        center = coords[1]
                    refs = v.get('refs', [])
                    if len(refs) > 0:
                        x = (
                                    nput.vec_normalize(coords[0] - coords[1])
                                    + nput.vec_normalize(coords[2] - coords[1])
                            ) / 2
                        if np.linalg.norm(x) < .05:
                            coords = [coords[0], coords[1], all_coords[refs[0], :2]]
                    offset = v.get('offset')
                    if offset is not None:
                        x = (
                                nput.vec_normalize(coords[0] - coords[1])
                                + nput.vec_normalize(coords[2] - coords[1])
                        ) / 2
                        coords = [
                            coords[0] + offset * x,
                            coords[1] + offset * x
                        ]
                    if angle is None:
                        u = nput.vec_normalize(coords[0] - coords[1])
                        x = nput.vec_normalize(coords[2] - coords[1])
                        angle = np.arccos(np.dot(u, x))
                    if start_angle is None:
                        u = nput.vec_normalize(coords[0] - coords[1])
                        start_angle = np.arctan2(u[1], u[0])
                        yy = nput.vec_normalize(coords[2] - coords[1])
                        det = u[0] * yy[1] - u[1] * yy[0]
                        if det < 0:
                            start_angle = np.arctan2(yy[1], yy[0])
                    scaling = v.get('scaling', .85)
                    if scaling is not None:
                        start_angle = start_angle + (1-scaling) * angle/2
                        angle = (scaling) * angle
                    if radius is None:
                        radius = .8 * np.min([
                            nput.vec_norms(coords[0] - coords[1]),
                            nput.vec_norms(coords[2] - coords[1]),
                        ])

                    label = v.get('label')
                    if label is not None:
                        if isinstance(label, str):
                            label = {'text':label}
                        label_text = label['text']
                        pos = label.get('position')
                        label_style = label.copy()
                        label_style = label_style | v.pop('label_style', {})
                        if pos is None:
                            offset = label_style.get('offset', 1.2)
                            scaled_offset = label_style.get('offset_scaled', True)
                            if nput.is_numeric(offset):
                                offset = [offset, 0]
                            x = nput.vec_normalize(
                                        nput.vec_normalize(coords[0] - coords[1])
                                        + nput.vec_normalize(coords[2] - coords[1])
                                )
                            if scaled_offset:
                                x = radius * x
                            y = nput.rotation_matrix('2d', -np.pi/2) @ x
                            ov = np.dot(offset, [x, y])
                            nn = nput.vec_normalize(ov)
                            for r in refs:
                                if np.dot(nn, nput.vec_normalize(all_coords[r, :2] - coords[1])) > .9:
                                    ov = -ov
                                    break
                            pos = center + ov
                        label_position = pos
                        for k in (
                                'text', 'offset', 'position', 'offset_scaled'
                        ): label_style.pop(k, None)

                    styles = v.get('styles')
                    if styles is None:
                        styles = v.copy()
                        for k in (
                                'type', 'coords', 'scaling', 'offset',
                                'label', 'center', 'refs',
                                'angle', 'radius', 'start_angle'
                        ): styles.pop(k, None)
                    if (
                            label_style is not None
                            and 'color' not in label_style
                    ):
                        test_color = styles.get('color')
                        if test_color is not None:
                            label_style['color'] = test_color
                    if 'fill_polys' not in styles:
                        styles['fill_polys'] = False

                    test_color = styles.get('color', True)
                    if test_color is not None:
                        if splits is not None:
                            split_start = len(drawer.GetDrawingText())
                        cls._handle_annotation_draw(
                            drawer.DrawArc,
                            drawer,
                            draw_options,
                            Geom.Point2D(*center), radius, np.rad2deg(start_angle), np.rad2deg(start_angle + angle),
                            styles=styles
                        )
                        if splits is not None:
                            split_end = len(drawer.GetDrawingText())
                            splits['annotations'].append([split_start, split_end])
                            split_start = split_end
                elif type == 'label':
                    center = v.get('center')
                    if center is None:
                        center = all_coords[k[0], :2]
                    offset = v.get('offset', np.array([.5, .3]))
                    label_position = center + offset
                    label_text = v.get('text')
                    if label_text is None:
                        label_text = str(k[0])
                    label_style = v.copy()
                    for k in (
                            'text', 'offset', 'center'
                    ): label_style.pop(k, None)

                else:
                    raise NotImplementedError(f"drawing coordinate type {type} not supported")

                if label_text is not None:
                    if label_style is None:
                        label_style = {}
                    if 'font_size' in label_style:
                        label_style['fixed_font_size'] = label_style['font_size']
                    if splits is not None:
                        split_start = len(drawer.GetDrawingText())
                    cls._handle_annotation_draw(
                        drawer.DrawString,
                        drawer,
                        draw_options,
                        label_text,
                        Geom.Point2D(*label_position),
                        styles=label_style
                    )
                    if splits is not None:
                        split_end = len(drawer.GetDrawingText())
                        splits['labels'].append([split_start, split_end])
                        split_start = split_end
        if return_splits:
            return drawer, splits
        else:
            return drawer

    def find_substructure(self, query):
        """
        **LLM Docstring**

        Return all substructure matches of a SMARTS query in the molecule.

        :param query: the SMARTS query
        :type query: str
        :return: the matching atom-index tuples
        :rtype: tuple
        """
        Chem = self.chem_api()
        query = Chem.MolFromSmarts(query)
        return self.rdmol.GetSubstructMatches(query)

    @classmethod
    def apply_smarts_to_mol(cls, mol, pattern,
                            remove_hydrogens=True,
                            readd_hydrogens=True):#, remove_intermediate_hydrogens=True):
        """
        **LLM Docstring**

        Apply a SMARTS reaction transform to a mol, running the reaction and
        reassembling the products while preserving atom mapping and re-adding
        hydrogens consistently.

        :param mol: the reactant mol
        :type mol: Chem.Mol
        :param pattern: the SMARTS reaction (string or reaction object)
        :type pattern: str | object
        :param remove_hydrogens: strip hydrogens before reacting
        :type remove_hydrogens: bool
        :param readd_hydrogens: re-add hydrogens to the products
        :type readd_hydrogens: bool
        :return: the product mols
        :rtype: list[Chem.Mol]
        :raises ValueError: if the pattern doesn't map all atoms
        """
        # import rdkit.Chem as Chem
        Chem = cls.allchem_api()
        if isinstance(pattern, str):
            smarts_tf = Chem.ReactionFromSmarts(pattern)
        else:
            smarts_tf = pattern

        cur_atom_map_indices = [
            a.GetAtomMapNum()
            for r in smarts_tf.GetReactants()
            for a in r.GetAtoms()
        ]
        if 0 in cur_atom_map_indices:
            raise ValueError(f"SMARTS pattern {pattern} must map all atoms")

        # rem_atoms = list(reversed([
        #     i
        #     for i in range(1, len(cur_atom_map_indices)+1)
        #     if i not in cur_atom_map_indices
        # ]))
        # for r in smarts_tf.GetReactants():
        #     for a in r.GetAtoms():
        #         if a.GetAtomMapNum() == 0:
        #             i = rem_atoms.pop()
        #             a.SetAtomMapNum(i)

        mol = Chem.Mol(mol)
        cur_map_no = [
            a.GetAtomMapNum()
            for a in mol.GetAtoms()
        ]
        for i,a in enumerate(mol.GetAtoms()):
            a.SetIntProp('react_atom_idx', i)
            a.SetAtomMapNum(i+1)
        # map_ord = list(range(1, len(cur_map_no)+1))
        # # we create an initial map of hydrogen positions and their bonds so we can add them back in
        # # later and reorder consistently
        # if remove_intermediate_hydrogens:
        #     hydrogen_map = {
        #
        #     }

        hydrogen_map = {}
        for a in mol.GetAtoms():
            if a.GetSymbol() in ['H', 'D', 'T']:
                i = a.GetIdx()
                key = tuple(sorted(b.GetIdx() for b in a.GetNeighbors()))
                if key not in hydrogen_map: hydrogen_map[key] = []
                hydrogen_map[key].append(i)

        if remove_hydrogens:
            mol = Chem.RemoveHs(mol)

        perm_prods = smarts_tf.RunReactants((mol,))
        # atomMapToReactantMap = {}
        # for ri in range(smarts_tf.GetNumReactantTemplates()):
        #     rt = smarts_tf.GetReactantTemplate(ri)
        #     for atom in rt.GetAtoms():
        #         if atom.GetAtomMapNum():
        #             atomMapToReactantMap[atom.GetAtomMapNum()] = ri

        prods = []
        for p_group in perm_prods:
            perm = []
            add_h_p = []
            h_map = {k:l.copy() for k,l in hydrogen_map.items()}
            for p in p_group:
                if readd_hydrogens:
                    p = Chem.AddHs(p, explicitOnly=False)
                    # RDKit will destroy hydrogens sometimes in "RunReactants"
                    # we just need to ensure this doesn't reorder anything...
                # for a in p.GetAtoms():
                #     x = a.GetPropsAsDict().get('react_atom_idx', a.GetAtomMapNum())
                #     print(x, a.GetSymbol(), a.GetPropsAsDict())
                for a in p.GetAtoms():
                    x = a.GetPropsAsDict().get('react_atom_idx', a.GetAtomMapNum())
                    if x == 0 and a.GetSymbol() in ['H', 'D', 'T']:
                        bond_atoms = []
                        for b in a.GetNeighbors():
                            bond_atoms.append(
                                b.GetPropsAsDict().get('react_atom_idx', b.GetAtomMapNum())
                            )
                        key = tuple(sorted(bond_atoms))
                        # print("!", key, [b.GetSymbol() for b in a.GetNeighbors()])
                        x = h_map[key].pop()
                    # a.SetAtomMapNum(x)
                    perm.append(x)
                add_h_p.append(p)
            # print(perm)
            # print(*[Chem.MolToSmiles(i) for i in p_group])

            p = functools.reduce(Chem.CombineMols, add_h_p)
            p = Chem.RenumberAtoms(p, np.argsort(perm, kind='merge').tolist())
            for a,cn in zip(p.GetAtoms(), cur_map_no):
                a.SetAtomMapNum(cn)
            prods.append(p)

        return prods

    def apply_smarts(self, tf):
        """
        **LLM Docstring**

        Apply a SMARTS reaction transform to this molecule, returning the products as
        `RDMolecule`s carrying the current coordinates.

        :param tf: the SMARTS reaction
        :type tf: str | object
        :return: the product molecules
        :rtype: list[RDMolecule]
        """
        Chem = self.chem_api()
        base_products = self.apply_smarts_to_mol(self.rdmol, tf)

        conf_id = self.mol.GetId()
        nats = self.coords.shape[0]

        new_mols = []
        for p in base_products:
            p.RemoveAllConformers()
            conf = Chem.Conformer(nats)
            copy_coords = self.coords.copy()
            conf.SetPositions(copy_coords)
            conf.SetId(conf_id)
            p.AddConformer(conf)
            conf = p.GetConformer(conf_id)
            new_mols.append(type(self)(conf, charge=self.charge))
        return new_mols

    # @classmethod
    # def break_mol_bonds_and_fragment(cls, mol, bonds):
    #     Chem = cls.allchem_api()
    #     if len(bonds) == 0:
    #         return {tuple(i for i, a in enumerate(mol.GetAtoms())): mol}
    #
    #     bond_indices = []
    #     no_map = {a.GetAtomMapNum(): i for i, a in enumerate(mol.GetAtoms())}
    #     no_map.pop(0, None)
    #     for i, j in bonds:
    #         i, j = no_map[i + 1], no_map[j + 1]
    #         bond_indices.append(mol.GetBondBetweenAtoms(i, j).GetIdx())
    #     broke_mol = Chem.FragmentOnBonds(mol, bond_indices, addDummies=False)
    #     for a in broke_mol.GetAtoms(): a.SetAtomMapNum(0)
    #     frags = Chem.GetMolFrags(broke_mol)
    #     new_mols = {}
    #     inv_map = {i: n for n, i in no_map.items()}
    #     for f in frags:
    #         submol = cls.take_mol_fragment(broke_mol, f)
    #         for a, i in zip(submol.GetAtoms(), f):
    #             a.SetAtomMapNum(inv_map.get(i, 0))
    #         new_mols[f] = submol
    #     return new_mols

    @classmethod
    def take_mol_fragment(cls, mol, inds, conf_id=None):
        """
        **LLM Docstring**

        Build a sub-mol from the given atom indices (with the bonds among them),
        optionally carrying over a conformer's coordinates.

        :param mol: the source mol
        :type mol: Chem.Mol
        :param inds: the atom indices to keep
        :type inds: Sequence[int]
        :param conf_id: a conformer id whose coordinates to copy
        :type conf_id: int | None
        :return: the sub-mol
        :rtype: Chem.Mol
        """
        Chem = cls.allchem_api()
        submol = Chem.EditableMol(Chem.Mol())
        if conf_id is not None:
            coords = mol.GetConformer(conf_id).GetPositions()
        else:
            coords = None
        submol.BeginBatchEdit()
        atom_list = list(mol.GetAtoms())
        for i in inds:
            submol.AddAtom(atom_list[i])
        for i, j in itertools.combinations(range(len(inds)), 2):
            b = mol.GetBondBetweenAtoms(inds[i], inds[j])
            if b is not None:
                submol.AddBond(i, j, b.GetBondType())
        submol.CommitBatchEdit()
        mol = submol.GetMol()
        if coords is not None:
            conf = Chem.Conformer(len(inds))
            copy_coords = coords[inds,].copy()
            conf.SetPositions(copy_coords)
            conf.SetId(conf_id)
            mol.AddConformer(conf)
        return mol

    def break_bonds(self,
                    bonds,
                    add_dummies=False,
                    reguess_bonds=True,
                    return_fragments=False):
        """
        **LLM Docstring**

        Break the given bonds and return the resulting (fragmented) molecule, carrying
        over coordinates and optionally re-perceiving bond orders.

        :param bonds: the `(i, j)` bonds to break
        :type bonds: Sequence
        :param add_dummies: add dummy atoms at the broken bonds
        :type add_dummies: bool
        :param reguess_bonds: re-perceive bond orders afterward
        :type reguess_bonds: bool
        :param return_fragments: unused flag
        :type return_fragments: bool
        :return: the fragmented molecule
        :rtype: RDMolecule
        """
        Chem = self.chem_api()
        from rdkit.Chem.rdmolops import FragmentOnBonds

        nats = self.coords.shape[0]
        conf_id = self.mol.GetId()
        bond_indices = []
        mol = self.rdmol
        for i,j in bonds:
            bond_indices.append(mol.GetBondBetweenAtoms(i,j).GetIdx())
        broke_mol = FragmentOnBonds(mol, bond_indices,
                                    addDummies=add_dummies)
        Chem.AddHs(broke_mol, explicitOnly=True)
        conf = Chem.Conformer(nats)
        copy_coords = self.coords.copy()
        conf.SetPositions(copy_coords)
        conf.SetId(conf_id)
        broke_mol.AddConformer(conf)
        conf = broke_mol.GetConformer(conf_id)

        if reguess_bonds:
            import rdkit.Chem.rdDetermineBonds as rdDetermineBonds
            rdDetermineBonds.DetermineBondOrders(broke_mol, charge=self.charge, embedChiral=False)

        return type(self)(conf, charge=self.charge)

    @classmethod
    def fragment_rdmol(cls, mol, inds):
        """
        **LLM Docstring**

        Build a sub-mol from the given atom indices and the bonds among them.

        :param mol: the source mol
        :type mol: Chem.Mol
        :param inds: the atom indices to keep
        :type inds: Sequence[int]
        :return: the sub-mol
        :rtype: Chem.Mol
        """
        Chem = cls.allchem_api()
        submol = Chem.EditableMol(Chem.Mol())
        submol.BeginBatchEdit()
        atom_list = list(mol.GetAtoms())
        for i in inds:
            submol.AddAtom(atom_list[i])
        for i, j in itertools.combinations(range(len(inds)), 2):
            b = mol.GetBondBetweenAtoms(inds[i], inds[j])
            if b is not None:
                submol.AddBond(i, j, b.GetBondType())
        submol.CommitBatchEdit()
        return submol.GetMol()

    @classmethod
    def fragment_rdmol_on_bonds(cls, mol, bonds, addDummies=True):
        """
        **LLM Docstring**

        Fragment a mol by breaking the given bonds, returning a mapping from each
        fragment's atom-index tuple to its sub-mol (with atom maps restored).

        :param mol: the source mol
        :type mol: Chem.Mol
        :param bonds: the `(i, j)` bonds to break (by atom-map number)
        :type bonds: Sequence
        :param addDummies: add dummy atoms at the broken bonds
        :type addDummies: bool
        :return: the `{fragment_indices: sub_mol}` mapping
        :rtype: dict
        """
        Chem = cls.allchem_api()
        bond_indices = []
        no_map = {a.GetAtomMapNum(): i for i, a in enumerate(mol.GetAtoms())}
        no_map.pop(0, None)
        for i, j in bonds:
            i, j = no_map[i + 1], no_map[j + 1]
            bond_indices.append(mol.GetBondBetweenAtoms(i, j).GetIdx())
        broke_mol = Chem.FragmentOnBonds(mol, bond_indices, addDummies=addDummies)
        for a in broke_mol.GetAtoms(): a.SetAtomMapNum(0)
        Chem.AddHs(broke_mol, explicitOnly=True)
        frags = Chem.GetMolFrags(broke_mol)
        new_mols = {}
        inv_map = {i: n for n, i in no_map.items()}
        for f in frags:
            submol = cls.fragment_rdmol(broke_mol, f)
            for a, i in zip(submol.GetAtoms(), f):
                a.SetAtomMapNum(inv_map.get(i, 0))
            new_mols[f] = submol
        return new_mols

    def get_atom_neighbors(self, i, n=1, mol=None, graph=None):
        """
        **LLM Docstring**

        Return the labels of the atoms within `n` bonds of a given atom.

        :param i: the central atom index
        :type i: int
        :param n: the neighborhood radius (in bonds)
        :type n: int
        :param mol: an explicit mol (defaults to this one)
        :type mol: Chem.Mol | None
        :param graph: a precomputed edge graph
        :return: the neighbor atom labels
        :rtype: list
        """
        if graph is None:
            graph = self.get_edge_graph(mol=mol)
        neighbor_graph = graph.neighbor_graph(i, num=n)
        return neighbor_graph.labels

    default_up_vector = (0, 1, 0)
    default_right_vector = (1, 0, 0)
    default_view_vector = (0, 0, 1)
    def _get_view_settings(self,
                         up_vector=None, right_vector=None, view_vector=None,
                         view_matrix=None, view_distance=None, view_center=None):
            """
            **LLM Docstring**

            Build a 3D view specification (rotation matrix, distance, center) from any
            combination of up/right/view vectors, filling in the missing axes by cross
            products.

            :param up_vector: the up direction
            :param right_vector: the right direction
            :param view_vector: the view/forward direction
            :param view_matrix: an explicit view rotation matrix
            :param view_distance: the camera distance
            :param view_center: the view center
            :return: the `{matrix, distance, center}` view settings
            :rtype: dict
            """
            if view_matrix is None and (
                    view_vector is not None
                    or right_vector is not None
                    or up_vector is not None
            ):
                if view_vector is None:
                    if (
                            up_vector is not None and right_vector is not None
                    ):
                        view_vector = nput.vec_crosses(up_vector, right_vector, normalize=True)
                    elif right_vector is not None:
                        view_vector = nput.vec_crosses(self.default_up_vector, right_vector, normalize=True)
                    elif up_vector is not None:
                        view_vector = nput.vec_crosses(up_vector, self.default_right_vector, normalize=True)

                if view_vector is not None:
                    m = nput.rotation_matrix(
                        view_vector,
                        self.default_view_vector
                    )
                else:
                    m = np.eye(3)

                if up_vector is None and right_vector is not None:
                    if view_vector is None:
                        view_vector = self.default_view_vector
                    up_vector = nput.vec_normalize(
                        nput.vec_crosses(right_vector, view_vector)
                    )
                elif up_vector is not None and view_vector is not None:
                    up_vector = nput.vec_crosses(
                        view_vector,
                        nput.vec_crosses(view_vector, up_vector),
                        normalize=True
                    )
                if up_vector is not None:
                    m = m @ nput.rotation_matrix(
                        m.T @ up_vector,
                        self.default_up_vector
                    )
                view_matrix = m
            return {
                'matrix':view_matrix,
                'distance':view_distance,
                'center':view_center
            }
    def draw(self,
             figure=None,
             background=None,
             remove_atom_numbers=None,
             remove_hydrogens=True,
             display_atom_numbers=False,
             format='svg',
             drawer=None,
             coords=None,
             use_coords=False,
             align_2d=None,
             view_settings=None,
             plot_range=None,
             atom_labels=None,
             bond_labels=None,
             blend_mixed_bonds=True,
             highlight_atoms=None,
             highlight_bonds=None,
             highlight_atom_colors=None,
             highlight_bond_colors=None,
             highlight_atom_radii=None,
             highlight_bond_radii=None,
             highlight_bond_width_multiplier=None,
             atom_radii=None,
             bond_radius=None,
             allow_radius_rescaling=True,
             draw_coords=None,
             highlight_rings=None,
             label_offset=1,
             conf_id=None,
             include_save_buttons=False,
             no_free_type=None,
             postdraw=None,
             return_splits=None,
             radius_to_range_scaling=None,
             **draw_opts):
        """
        **LLM Docstring**

        Draw the molecule in 2D (SVG/PNG), with extensive control over hydrogen removal,
        2D-coordinate generation and alignment, atom/bond labels and highlights, ring
        highlighting, and save buttons.

        :param figure: an existing figure/drawer to draw into
        :param background: the background color
        :param remove_atom_numbers: strip atom-map numbers from the drawing
        :type remove_atom_numbers: bool | None
        :param remove_hydrogens: hide hydrogens
        :type remove_hydrogens: bool
        :param display_atom_numbers: annotate atoms with their indices
        :type display_atom_numbers: bool
        :param format: `'svg'` or `'png'`
        :type format: str
        :param drawer: an explicit drawing function
        :param coords: explicit 2D coordinates to draw at
        :type coords: np.ndarray | None
        :param use_coords: draw using the molecule's own coordinates (projected)
        :type use_coords: bool
        :param align_2d: align the generated 2D coordinates to the view
        :type align_2d: bool | None
        :param view_settings: 3D view settings for coordinate alignment
        :type view_settings: dict | None
        :param plot_range: a fixed drawing range
        :type plot_range: tuple | None
        :param atom_labels: per-atom label overrides
        :param bond_labels: per-bond label overrides
        :param blend_mixed_bonds: blend colors on bonds between differently colored atoms
        :type blend_mixed_bonds: bool
        :param highlight_atoms: atoms to highlight
        :param highlight_bonds: bonds to highlight
        :param highlight_atom_colors: per-atom highlight colors
        :param highlight_bond_colors: per-bond highlight colors
        :param highlight_atom_radii: per-atom highlight radii
        :param highlight_bond_radii: per-bond highlight radii
        :param highlight_bond_width_multiplier: highlight bond-width multiplier
        :param atom_radii: per-atom radii
        :param bond_radius: the bond radius
        :param allow_radius_rescaling: allow radii to rescale with the plot range
        :type allow_radius_rescaling: bool
        :param draw_coords: extra coordinate annotations
        :param highlight_rings: rings to highlight
        :param label_offset: the annotation label offset
        :param conf_id: the conformer id
        :type conf_id: int | None
        :param include_save_buttons: include save buttons in the output
        :type include_save_buttons: bool
        :param no_free_type: disable FreeType font rendering
        :type no_free_type: bool | None
        :param postdraw: a callback invoked after drawing
        :type postdraw: Callable | None
        :param return_splits: also return drawing element split metadata
        :type return_splits: bool | None
        :param radius_to_range_scaling: radius-to-range scaling factor
        :param draw_opts: extra drawing options
        :return: the rendered drawing
        :rtype: object
        """
        from ..Plots import ColorPalette

        if drawer is None:
            drawer = self._draw_non_interactive

        if conf_id is None:
            conf_id = self.mol.GetId()

        Chem = self.allchem_api()
        mol = self.rdmol
        modified = False
        non_h_atoms = None
        if remove_hydrogens:
            modified = True
            non_h_atoms = []
            non_h_remapping = {k:i for i,k in enumerate(non_h_atoms)}
            og_map = []
            for a in mol.GetAtoms():
                og_map.append(a.GetAtomMapNum())
                a.SetAtomMapNum(a.GetIdx() + 1)
            old = mol
            new = Chem.RemoveHs(mol)
            for i,a in zip(og_map, mol.GetAtoms()):
                a.SetAtomMapNum(i)
            mol = new
            for a in mol.GetAtoms():
                i = a.GetAtomMapNum() - 1
                non_h_atoms.append(i)
                a.SetAtomMapNum(og_map[i])
            if highlight_bonds is not None:
                _ = []
                for b in highlight_bonds:
                    if nput.is_int(b):
                        b = old.GetBondGetBondWithIdx(b)
                        i = b.GetBeginAtomIdx()
                        j = b.GetEndAtomIdx()
                    else:
                        i, j = b
                    if i in non_h_remapping and j in non_h_remapping:
                        _.append((non_h_remapping[i], non_h_remapping[j]))
                highlight_bonds = _
            if highlight_bond_colors is not None:
                _ = {}
                for b,c in highlight_bond_colors.items():
                    if nput.is_int(b):
                        b = old.GetBondGetBondWithIdx(b)
                        i = b.GetBeginAtomIdx()
                        j = b.GetEndAtomIdx()
                    else:
                        i, j = b
                    if i in non_h_remapping and j in non_h_remapping:
                        _[(non_h_remapping[i], non_h_remapping[j])] = c
                highlight_bond_colors = _
            if highlight_bond_radii is not None:
                _ = {}
                for b,c in highlight_bond_radii.items():
                    if nput.is_int(b):
                        b = old.GetBondGetBondWithIdx(b)
                        i = b.GetBeginAtomIdx()
                        j = b.GetEndAtomIdx()
                    else:
                        i, j = b
                    if i in non_h_remapping and j in non_h_remapping:
                        _[(non_h_remapping[i], non_h_remapping[j])] = c
                highlight_bond_radii = _

        if coords is None:
            if not use_coords:
                if not modified:
                    mol = Chem.Mol(mol)
                    modified = True
                Chem.Compute2DCoords(mol)
                if align_2d is None:
                    align_2d = view_settings is not None
                if align_2d:
                    conf = mol.GetConformer()
                    coords_2d = conf.GetPositions()
                    coords_3d = self.coords
                    if non_h_atoms is not None:
                        coords_3d = coords_3d[non_h_atoms, :]
                    if view_settings is not None:
                        view_settings = self._get_view_settings(**view_settings)
                    else:
                        view_settings = {
                            'matrix':None,
                            'distance':None,
                            'center':None
                        }
                    mat = view_settings.get('matrix')
                    center = view_settings.get('center')
                    if center is not None:
                        center = np.asanyarray(center)
                        coords_3d = coords_3d - center[np.newaxis]
                        coords_2d = coords_2d - np.array([center[0], center[1], 0])[np.newaxis]
                    if mat is not None:
                        if plot_range is not None:
                            plot_range = (np.asanyarray(plot_range).T @ mat).T
                        coords_3d = coords_3d @ mat
                        coords_3d[..., 2] = 0
                        coords_2d = nput.eckart_embedding(coords_3d, coords_2d).coordinates
                    dist = view_settings.get('distance')
                    if dist is not None:
                        default_view_distance = np.max([
                            np.max(coords_2d[..., i]) - np.min(coords_2d[..., i]) + .2
                            for i in range(2)
                        ])
                        if plot_range is None:
                            plot_range = [
                                [
                                    np.min(coords_2d[..., i]) - .1,
                                    np.max(coords_2d[..., i]) + .1
                                ]
                                for i in range(2)
                            ]
                        coords_2d = coords_2d * (default_view_distance / dist)
                    coords = coords_2d
                conf_id = -1

            elif view_settings is not None:
                coords_3d = self.coords
                if non_h_atoms is not None:
                    coords_3d = coords_3d[non_h_atoms, :]
                if not modified:
                    mol = Chem.Mol(mol)
                    modified = True
                # conf = mol.GetConformer()
                if view_settings is not None:
                    view_settings = self._get_view_settings(**view_settings)
                else:
                    view_settings = {
                        'matrix': None,
                        'distance': None,
                        'center': None
                    }
                mat = view_settings.get('matrix')
                center = view_settings.get('center')
                if center is not None:
                    center = np.asanyarray(center)
                    coords_3d = coords_3d - center[np.newaxis]
                if mat is not None:
                    coords_3d = coords_3d @ mat
                    if plot_range is not None:
                        plot_range = (np.asanyarray(plot_range).T @ mat).T
                dist = view_settings.get('distance')
                if dist is not None:
                    default_view_distance = np.max([
                        np.max(coords_3d[..., i]) - np.min(coords_3d[..., i]) + .2
                        for i in range(2)
                    ])
                    if plot_range is None:
                        plot_range = [
                            [
                                np.min(coords_3d[..., i]) - .1,
                                np.max(coords_3d[..., i]) + .1
                            ]
                            for i in range(2)
                        ]
                    coords_3d = coords_3d * (default_view_distance / dist)
                coords = coords_3d

        if plot_range is not None:
            plot_range = plot_range[:2]

        if display_atom_numbers:
            if not modified:
                if coords is None:
                    conf = mol.GetConformer(conf_id)
                    coords = conf.GetPositions().copy()
                mol = Chem.Mol(mol)
                modified = True
            if dev.str_is(display_atom_numbers, 'inline'):
                for atom in mol.GetAtoms():
                    atom.SetAtomMapNum(atom.GetIdx()+1)
            else:
                if display_atom_numbers is True:
                    draw_opts['add_atom_indices'] = True
                    display_atom_numbers = []
                if remove_atom_numbers or remove_atom_numbers is None:
                    for atom in mol.GetAtoms():
                        atom.SetAtomMapNum(0)
                        if atom.GetIdx() in display_atom_numbers:
                            atom.SetProp("atomNote", str(atom.GetIdx()))
        elif remove_atom_numbers:
            if not modified:
                if coords is None:
                    conf = mol.GetConformer(conf_id)
                    coords = conf.GetPositions().copy()
                mol = Chem.Mol(mol)
                modified = True
            for atom in mol.GetAtoms():
                atom.SetAtomMapNum(0)
        if atom_labels is not None:
            if not modified:
                if coords is None:
                    conf = mol.GetConformer(conf_id)
                    coords = conf.GetPositions().copy()
                mol = Chem.Mol(mol)
                modified = True
            if isinstance(atom_labels, dict):
                atom_labels = [atom_labels.get(atom.GetIdx()) for atom in mol.GetAtoms()]
            graph = self.get_edge_graph(mol)
            for atom,label in zip(mol.GetAtoms(), atom_labels):
                if label is not None:
                    if isinstance(label, str):
                        atom.SetProp("atomNote", label)
                    else:
                        draw_coords = self._prep_draw_coords(draw_coords)
                        label = label.copy()
                        key = label.pop('key', None)
                        if key is None:
                            i = atom.GetIdx()
                            neighbors = self.get_atom_neighbors(i, 2, graph=graph)
                            neighbors = sorted(set(neighbors) - {i})
                            if len(neighbors) == 0:
                                key = (i,)
                            elif len(neighbors) == 1:
                                key = (i, neighbors[0])
                            else:
                                key = (neighbors[0], i, neighbors[1])
                                label['refs'] = neighbors[2:]
                        if 'offset' not in label:
                            if len(key) == 2:
                                label['offset'] = [0, 1.2 * label_offset]
                            elif len(key) == 3:
                                label['offset'] = [-label_offset, 0]
                        if 'text' not in label:
                            i = atom.GetIdx()
                            label['text'] = str(i)
                        spec = {
                            'key':key,
                            'color':None,
                            'label':label
                        }
                        refs = label.pop('refs', None)
                        if refs is not None:
                            spec['refs'] = refs
                        draw_coords.append(spec)

        if bond_labels is not None:
            if not modified:
                if coords is None:
                    conf = mol.GetConformer(conf_id)
                    coords = conf.GetPositions().copy()
                mol = Chem.Mol(mol)
                modified = True
            if isinstance(bond_labels, dict):
                for bond in mol.GetBonds():
                    i,j = bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()
                    label = bond_labels.get(bond.GetIdx(),
                                            bond_labels.get((i,j),
                                                            bond_labels.get((j, i))
                                                            )
                                            )
                    if label is not None:
                        bond.SetProp("bondNote", label)
            else:
                for bond,label in zip(mol.GetBonds(), bond_labels):
                    if label is not None:
                        bond.SetProp("bondNote", label)

        if highlight_atoms is not None:
            bond_set = {}
            for i,b in enumerate(self.bonds):
                if b[0] not in bond_set:
                    bond_set[b[0]] = {}
                bond_set[b[0]][b[1]] = i

            if highlight_bonds is None:
                highlight_bonds = []
            else:
                highlight_bonds = list(highlight_bonds)
            hats = set(highlight_atoms)
            for a in hats:
                for b,i in bond_set.get(a, {}).items():
                    if b in hats:
                        if blend_mixed_bonds or highlight_atom_colors is None:
                            highlight_bonds.append(i)
                        else:
                            c1 = highlight_atom_colors.get(a)
                            c2 = highlight_atom_colors.get(b)
                            if c1 is None or c2 is None:
                                highlight_bonds.append(i)
                            else:
                                if isinstance(c1, str):
                                    if not isinstance(c2, str):
                                        c1 = ColorPalette.parse_color_string(c1)
                                elif isinstance(c2, str):
                                    c2 = ColorPalette.parse_color_string(c2)
                                if (
                                        (isinstance(c1, str) and isinstance(c2, str) and c1 == c2)
                                        or (not isinstance(c1, str) and np.allclose(c1, c2))
                                ):
                                    highlight_bonds.append(i)

        if highlight_bonds is not None:
            _ = []
            for b in highlight_bonds:
                if not nput.is_int(b):
                    i,j = b
                    _.append(mol.GetBondBetweenAtoms(int(i),int(j)).GetIdx())
                else:
                    _.append(b)
            highlight_bonds = _

        if highlight_bonds is not None:
            _ = {}
            if highlight_atom_colors is not None:
                atom_colors = highlight_atom_colors
            else:
                atom_colors = {}
            if highlight_bond_colors is None:
                highlight_bond_colors = {}
            for b in highlight_bonds:
                if b not in highlight_bond_colors:
                    if not nput.is_int(b):
                        i, j = b
                    else:
                        bb = mol.GetBondWithIdx(b)
                        i = bb.GetBeginAtomIdx()
                        j = bb.GetEndAtomIdx()
                    if (i, j) not in highlight_bond_colors and (j, i) not in highlight_bond_colors:
                        c1 = atom_colors.get(i)
                        c2 = atom_colors.get(j)
                        if c1 is None:
                            if c2 is None:
                                highlight_bond_colors[(i, j)] = (.5, .7, .5)
                            else:
                                highlight_bond_colors[(i, j)] = c2
                        elif c2 is None:
                            highlight_bond_colors[(i, j)] = c1
                        else:
                            if isinstance(c1, str):
                                if not isinstance(c2, str):
                                    c1 = self._handle_color(c1)
                            elif isinstance(c2, str):
                                c2 = self._handle_color(c2)
                            if (
                                    (isinstance(c1, str) and isinstance(c2, str) and c1 == c2)
                                    or (not isinstance(c1, str) and np.allclose(c1, c2))
                            ):
                                highlight_bond_colors[(i, j)] = c1
                            elif blend_mixed_bonds:
                                highlight_bond_colors[(i, j)] = ColorPalette.prep_color(
                                    palette=[c1, c2],
                                    blending=.5,
                                    return_color_code=False
                                )
        if highlight_bond_colors is not None:
            _ = {}
            for b,v in highlight_bond_colors.items():
                if not nput.is_int(b):
                    i,j = b
                    x = mol.GetBondBetweenAtoms(int(i),int(j)).GetIdx()
                    _[x] = v
                else:
                    _[b] = v
            highlight_bond_colors = _

            _ = {}
            for b,c in highlight_bond_colors.items():
                _[b] = self._handle_color(c)
            highlight_bond_colors = _
        if highlight_atom_colors is not None:
            _ = {}
            for b, c in highlight_atom_colors.items():
                _[b] = self._handle_color(c)
            highlight_atom_colors = _

        if conf_id is None:
            conf_id = self.mol.GetId()
        if coords is None:
            conf = mol.GetConformer(conf_id)
            coords = conf.GetPositions().copy()
        if allow_radius_rescaling:
            if figure is not None:
                try:
                    radius_to_range_scaling = figure.scaling_factor
                except AttributeError:
                    ...
            if radius_to_range_scaling is None:
                if plot_range is not None:
                    x_range, y_range = plot_range
                    x_span = x_range[1] - x_range[0]
                    y_span = y_range[1] - y_range[0]
                    ox_range, oy_range = [
                        [
                            np.min(coords[..., i]) - .1,
                            np.max(coords[..., i]) + .1
                        ]
                        for i in range(2)
                    ]
                    ox_span = ox_range[1] - ox_range[0]
                    oy_span = oy_range[1] - oy_range[0]
                    radius_to_range_scaling = np.linalg.norm([ox_span, oy_span]) / np.linalg.norm([x_span, y_span])
                else:
                    radius_to_range_scaling = 1
        else:
            radius_to_range_scaling = 1

        if atom_radii is not None and highlight_atoms is not None:
            if highlight_atom_radii is None:
                highlight_atom_radii = {}
            for a in highlight_atoms:
                if a not in highlight_atom_radii:
                    highlight_atom_radii[a] = atom_radii[a] * radius_to_range_scaling
        # if highlight_bond_radii is not None:
        #     _ = {}
        #     for b,v in highlight_bond_radii.items():
        #         if not nput.is_int(b):
        #             i, j = b
        #             _[mol.GetBondBetweenAtoms(int(i), int(j)).GetIdx()] = v
        #         else:
        #             _[b] = v
        #     highlight_bond_radii = _
        # if bond_radius is not None and highlight_bonds is not None:
        #     if highlight_bond_radii is None:
        #         highlight_bond_radii = {}
        #     for b in highlight_bonds:
        #         if b not in highlight_bond_radii:
        #             highlight_bond_radii[b] = bond_radius * radius_to_range_scaling

        if highlight_atom_radii is not None:
            highlight_atom_radii = {b:float(v) for b,v in highlight_atom_radii.items()}

        # if highlight_bond_radii is not None:
        #     highlight_bond_radii = {b:int(v*line_width_scaling) for b,v in highlight_bond_radii.items()}

        # if highlight_bond_radii is not None:
        #     draw_opts['fill_highlights'] = draw_opts.get('fill_highlights', True)

        if highlight_bond_width_multiplier is None and bond_radius is not None:
            highlight_bond_width_multiplier = int(np.ceil(radius_to_range_scaling * 7 * bond_radius / .2))

        if background is not None:
            background = self._handle_color(background)

        if figure is not None:
            try:
                pr = figure.plot_range
            except AttributeError:
                ...
            else:
                if pr is not None:
                    plot_range = pr
        if return_splits is None:
            return_splits = postdraw is not None
        draw_fig = drawer(mol,
                          figure=figure,
                          background=background,
                          format=format,
                          highlight_atoms=highlight_atoms,
                          highlight_bonds=highlight_bonds,
                          highlight_atom_colors=highlight_atom_colors,
                          highlight_bond_colors=highlight_bond_colors,
                          highlight_atom_radii=highlight_atom_radii,
                          highlight_bond_radii=highlight_bond_radii,
                          highlight_bond_width_multiplier=highlight_bond_width_multiplier,
                          draw_coords=draw_coords,
                          coords=coords,
                          conf_id=conf_id,
                          plot_range=plot_range[:2] if plot_range is not None else plot_range,
                          no_free_type=no_free_type,
                          return_splits=return_splits,
                          **draw_opts)
        if return_splits:
            draw_fig, splits = draw_fig
        else:
            splits = None
        try:
            base_splits = figure.splits
        except AttributeError:
            ...
        else:
            if base_splits is not None:
                if splits is None:
                    splits = {}
                splits = dev.merge_dicts(base_splits, splits, merge_iterables=True)
        try:
            base_postdraw = figure.postdraw
        except AttributeError:
            ...
        else:
            if base_postdraw is not None:
                if postdraw is None:
                    postdraw = base_postdraw
                else:
                    if not dev.is_list_like(postdraw):
                        postdraw = [postdraw]
                    if not dev.is_list_like(base_postdraw):
                        base_postdraw = [base_postdraw]
                    postdraw = postdraw + base_postdraw

        return DisplayImage(draw_fig, format,
                            plot_range=plot_range,
                            postdraw=postdraw,
                            scaling_factor=radius_to_range_scaling,
                            splits=splits,
                            include_save_buttons=include_save_buttons)

    def plot(self,
             conf_id=None,
             image_size=(450, 450),
             **opts):
        """
        **LLM Docstring**

        Display an interactive 3D rendering of the molecule (via RDKit's IPython 3D
        console).

        :param conf_id: the conformer id (defaults to the current one)
        :type conf_id: int | None
        :param image_size: the `(width, height)` of the view
        :type image_size: tuple
        :param opts: extra drawing options
        :return: the 3D display
        :rtype: object
        """
        # import py3Dmol
        from rdkit.Chem.Draw import IPythonConsole

        if conf_id is None:
            conf_id = self.mol.GetId()

        opts = dict(dict(confId=conf_id, size=image_size),
                    **{self._camel_case(k): v for k, v in opts.items()})
        return IPythonConsole.drawMol3D(self.rdmol, confId=self.mol, **opts)

    @classmethod
    def _plain_encode(cls, flat_z, byte_size):
        """
        **LLM Docstring**

        Encode a flat coordinate array as raw bytes of the given float precision.

        :param flat_z: the flat values
        :type flat_z: Sequence[float]
        :param byte_size: the float bit width (16/32/64/128)
        :type byte_size: int
        :return: the encoded array
        :rtype: np.ndarray
        """
        if byte_size == 16:
            dtype = np.float16
        elif byte_size == 32:
            dtype = np.float32
        elif byte_size == 64:
            dtype = np.float64
        elif byte_size == 128:
            dtype = np.float128
        else:
            raise ValueError(f"unhandled byte size {byte_size}")
        return np.array(flat_z).astype(dtype)

    @classmethod
    def _plain_decode(cls, buffer, byte_size):
        """
        **LLM Docstring**

        Decode a raw-bytes buffer back into a float array of the given precision.

        :param buffer: the byte buffer
        :type buffer: bytes
        :param byte_size: the float bit width (16/32/64/128)
        :type byte_size: int
        :return: the decoded values
        :rtype: np.ndarray
        """
        if byte_size == 16:
            dtype = np.float16
        elif byte_size == 32:
            dtype = np.float32
        elif byte_size == 64:
            dtype = np.float64
        elif byte_size == 128:
            dtype = np.float128
        else:
            raise ValueError(f"unhandled byte size {byte_size}")
        return np.frombuffer(buffer, dtype)

    @classmethod
    def _compressed_encode(cls, flat_z, byte_size, primary_bond_range=(.5, 2.5), pack_angles=True):
        """
        Compress distances such that if they are between 1 and 2 angstroms, we get
        an extra digit of precision
        :param flat_z:
        :param dtype:
        :return:
        """
        if byte_size == 16:
            base_type = np.uint16
            float_type = np.float16
            if pack_angles:
                pack_type = np.uint8
            else:
                pack_type = np.uint16
        elif byte_size == 32:
            base_type = np.uint32
            float_type = np.float32
            if pack_angles:
                pack_type = np.uint16
            else:
                pack_type = np.uint32
        elif byte_size == 64:
            base_type = np.uint64
            float_type = np.float64
            if pack_angles:
                pack_type = np.uint32
            else:
                pack_type = np.uint64
        else:
            raise ValueError(f"can't pack into byte size {byte_size}")

        flat_z = np.asanyarray(flat_z)
        dists = np.concatenate([flat_z[:2], flat_z[3::3]])
        compressed = (dists >= primary_bond_range[0]) & (dists < primary_bond_range[1])
        comp_vals = dists[compressed]

        step_max = 2**(byte_size-1) - 1
        total_bond_range =  primary_bond_range[1] -  primary_bond_range[0]
        comp_vals = np.round(step_max * (comp_vals - primary_bond_range[0]) / total_bond_range).astype(base_type)
        packaged_dists = np.zeros(len(dists), dtype=base_type)
        packaged_dists[compressed] = comp_vals
        # takes advantage of the fact that we are never negative to use that
        # bit for this encoding
        dx = dists[~compressed].astype(float_type)
        packaged_dists[~compressed] = dx.view(base_type) + step_max

        full_max = 2 ** byte_size - 1
        if pack_angles:
            pack_max = 2 ** (byte_size//2) - 1
        else:
            pack_max = full_max
        angles = np.concatenate([flat_z[[2],], flat_z[4::3]])
        first_angle = np.round(full_max * angles[0] / np.pi).astype(base_type)
        scaled_angles = np.round(pack_max * angles[1:] / np.pi).astype(base_type)
        dihedrals = flat_z[5::3].copy()
        mask = dihedrals < 0
        dihedrals[mask] = 2*np.pi + dihedrals[mask]
        scaled_dihedrals = np.round(pack_max * dihedrals / (2*np.pi)).astype(base_type)

        if pack_angles:
            full_pack = np.zeros(len(dists) + len(angles), dtype=base_type)
        else:
            full_pack = np.zeros(len(flat_z), dtype=base_type)

        full_pack[:2] = packaged_dists[:2]
        full_pack[2] = first_angle

        packaged_angles = np.zeros(len(angles), dtype=base_type)
        if pack_angles:
            full_pack[3::2] = packaged_dists[2:]
            packaged_angles[1:] = (scaled_angles << (byte_size // 2) | scaled_dihedrals)
            full_pack[4::2] = packaged_angles[1:]
        else:
            full_pack[3::3] = packaged_dists[2:]
            full_pack[4::3] = scaled_angles
            full_pack[5::3] = scaled_dihedrals

        return full_pack

    @classmethod
    def _compressed_decode(cls, buffer, byte_size, primary_bond_range=(.5, 2.5), pack_angles=True):
        """
        Compress distances such that if they are between 1 and 2 angstroms, we get
        an extra digit of precision
        :param flat_z:
        :param dtype:
        :return:
        """
        if byte_size == 16:
            base_type = np.uint16
            float_type = np.float16
            if pack_angles:
                pack_type = np.uint8
            else:
                pack_type = np.uint16
        elif byte_size == 32:
            base_type = np.uint32
            float_type = np.float32
            if pack_angles:
                pack_type = np.uint16
            else:
                pack_type = np.uint32
        elif byte_size == 64:
            base_type = np.uint64
            float_type = np.float64
            if pack_angles:
                pack_type = np.uint32
            else:
                pack_type = np.uint64
        else:
            raise ValueError(f"can't pack into byte size {byte_size}")

        uint_stream = np.frombuffer(buffer, base_type)
        if pack_angles:
            dists = np.concatenate([uint_stream[:2], uint_stream[3::2]])
        else:
            dists = np.concatenate([uint_stream[:2], uint_stream[3::3]])

        step_max = 2 ** (byte_size - 1) - 1
        compressed = dists < step_max
        decompressed_dists = np.zeros(len(dists), dtype=float)

        total_bond_range = primary_bond_range[1] - primary_bond_range[0]
        decompressed_dists[compressed] = (total_bond_range *  dists[compressed] / step_max) + primary_bond_range[0]
        decompressed_dists[~compressed] = (dists[~compressed] - step_max).view(float_type)

        full_max = 2 ** byte_size - 1
        if pack_angles:
            pack_max = 2 ** (byte_size // 2) - 1
        else:
            pack_max = full_max

        if pack_angles:
            full_pack = np.zeros(3*(len(dists) - 1) , dtype=float)
            packed_angles = np.concatenate([uint_stream[[2],], uint_stream[4::2]])
            angles = np.concatenate([packed_angles[[0],], packed_angles[1:] >> (byte_size // 2)])
            dihedrals = packed_angles[1:] & (2**(byte_size // 2) - 1)
        else:
            full_pack = np.zeros(len(uint_stream) , dtype=float)
            angles = np.concatenate([uint_stream[[2],], uint_stream[4::3]])
            dihedrals = uint_stream[5::3]

        full_angles = np.pi*np.concatenate([angles[:1] / full_max, angles[1:] / pack_max])
        full_dihedrals = (2*np.pi * dihedrals / pack_max)

        full_pack[:2] = decompressed_dists[:2]
        full_pack[2] = full_angles[0]
        full_pack[3::3] = decompressed_dists[2:]
        full_pack[4::3] = full_angles[1:]
        full_pack[5::3] = full_dihedrals

        return full_pack

    defaul_conformer_compression = 'compressed'
    default_tag_byte_size = 16
    default_tag_byte_encoding = 64
    def conformer_smiles_tag(self,
                             coords=None, graph=None, zmatrix=None,
                             encoder=None, byte_size=None, byte_encoding=None,
                             binary=False, include_zmatrix=False):
        """
        **LLM Docstring**

        Encode the molecule's 3D geometry into a compact string tag (a Z-matrix of the
        canonical-fragment internal coordinates, packed and base-N encoded) suitable for
        appending to a SMILES string.

        :param coords: the coordinates to encode (defaults to the current ones)
        :type coords: np.ndarray | None
        :param graph: the molecular edge graph (built if omitted)
        :param zmatrix: an explicit Z-matrix connectivity (built if omitted)
        :param encoder: the value encoder (`'plain'`/`'compressed'`/`'precision'` or a callable)
        :type encoder: str | Callable | None
        :param byte_size: the per-value bit width
        :type byte_size: int | None
        :param byte_encoding: the base-N text encoding (16/32/64/85)
        :type byte_encoding: int | Callable | None
        :param binary: return raw bytes rather than text
        :type binary: bool
        :param include_zmatrix: also return the encoded Z-matrix connectivity
        :type include_zmatrix: bool
        :return: the conformer tag (and Z-matrix data if requested)
        :rtype: str | bytes | tuple
        """
        if zmatrix is None:
            if graph is None:
                graph = self.get_edge_graph()
            frags = graph.get_canonical_fragments()
            zmatrix = coordops.canonical_fragment_zmatrix(frags, validate_additions=True)
        if coords is None:
            coords = self.coords

        if byte_size is None:
            byte_size = self.default_tag_byte_size
        if byte_encoding is None:
            byte_encoding = self.default_tag_byte_encoding

        zdata = coordops.cartesian_to_zmatrix(coords, zmatrix)
        flat_z = coordops.extract_zmatrix_values(zdata.coords, partial_embedding=True)
        if encoder is None:
            encoder = self.defaul_conformer_compression
        if dev.str_is(encoder, 'plain'):
            zmat_coords = self._plain_encode(flat_z, byte_size)
        elif encoder == 'compressed':
            zmat_coords = self._compressed_encode(flat_z, byte_size)
        elif encoder == 'precision':
            zmat_coords = self._compressed_encode(flat_z, byte_size, pack_angles=False)
        else:
            zmat_coords = encoder(flat_z, byte_size)

        if nput.is_int(byte_encoding):
            if byte_encoding == 16:
                byte_encoding = base64.b16encode
            elif byte_encoding == 32:
                byte_encoding = base64.b32encode
            elif byte_encoding == 64:
                byte_encoding = base64.b64encode
            elif byte_encoding == 85:
                byte_encoding = base64.b85encode
            else:
                raise ValueError(f"don't know byte encoding {byte_encoding}")

        if binary:
            tag = zmat_coords.data
        else:
            tag = byte_encoding(zmat_coords.data)
            if isinstance(tag, bytes):
                tag = tag.decode()
        if include_zmatrix:
            zz = np.array([z[1:] for z in zmatrix])
            zinds = np.array(coordops.extract_zmatrix_values(zz))
            zinds = zinds.astype(nput.infer_inds_dtype(np.max(zinds)))
            if binary:
                ztag = zinds.data
            else:

                ztag = byte_encoding(zinds.data)
                if isinstance(ztag, bytes):
                    ztag = ztag.decode()
            return ztag, zinds
        else:
            return tag

    @classmethod
    def conformer_from_smiles_tag(cls, tag, graph, decoder=None, byte_size=None, byte_encoding=None, zmatrix=None):
        """
        **LLM Docstring**

        Decode a conformer tag back into Cartesian coordinates, using the molecular graph
        to reconstruct the canonical-fragment Z-matrix.

        :param tag: the conformer tag
        :type tag: str
        :param graph: the molecular edge graph
        :param decoder: the value decoder (`'plain'`/`'compressed'`/`'precision'` or a callable)
        :type decoder: str | Callable | None
        :param byte_size: the per-value bit width
        :type byte_size: int | None
        :param byte_encoding: the base-N text encoding
        :type byte_encoding: int | Callable | None
        :param zmatrix: an explicit Z-matrix connectivity (built if omitted)
        :return: the decoded Cartesian coordinates
        :rtype: np.ndarray
        """
        if zmatrix is None:
            frags = graph.get_canonical_fragments()
            zmatrix = coordops.canonical_fragment_zmatrix(frags, validate_additions=True)

        if byte_size is None:
            byte_size = cls.default_tag_byte_size
        if byte_encoding is None:
            byte_encoding = cls.default_tag_byte_encoding
        if nput.is_int(byte_encoding):
            if byte_encoding == 16:
                byte_encoding = base64.b16decode
            elif byte_encoding == 32:
                byte_encoding = base64.b32decode
            elif byte_encoding == 64:
                byte_encoding = base64.b64decode
            elif byte_encoding == 85:
                byte_encoding = base64.b85decode
            else:
                raise ValueError(f"don't know byte encoding {byte_encoding}")

        buffer = byte_encoding(tag.encode())
        if decoder is None:
            decoder = cls.defaul_conformer_compression
        if dev.str_is(decoder, 'plain'):
            flat_z = cls._plain_decode(buffer, byte_size)
        elif decoder == 'compressed':
            flat_z = cls._compressed_decode(buffer, byte_size)
        elif decoder == 'precision':
            flat_z = cls._compressed_decode(buffer, byte_size, pack_angles=False)
        else:
            flat_z = decoder(buffer, byte_size)
        zcoords = coordops.zmatrix_from_values(flat_z, partial_embedding=True)
        coords = coordops.zmatrix_to_cartesian(zcoords, np.array(zmatrix)) # very borked
        return coords

    @classmethod
    def get_mol_edge_graph(cls, mol):
        """
        **LLM Docstring**

        Build an `EdgeGraph` of a mol's atom/bond connectivity.

        :param mol: the mol
        :type mol: Chem.Mol
        :return: the edge graph
        :rtype: EdgeGraph
        """
        from .. import Graphs
        atoms = np.arange(len(mol.GetAtoms()))
        bonds = [
            [b.GetBeginAtomIdx(), b.GetEndAtomIdx()]
            for b in mol.GetBonds()
        ]
        return Graphs.EdgeGraph(atoms, bonds)
    def get_edge_graph(self, mol=None):
        """
        **LLM Docstring**

        Build an `EdgeGraph` of this molecule's connectivity (or of a supplied mol).

        :param mol: an explicit mol (defaults to this one)
        :type mol: Chem.Mol | None
        :return: the edge graph
        :rtype: EdgeGraph
        """
        from .. import Graphs
        if mol is None:
            atoms, bonds = np.arange(len(self.atoms)), [b[:2] for b in self.bonds]
            return Graphs.EdgeGraph(atoms, bonds)
        else:
            return self.get_mol_edge_graph(mol)

    def _ipython_display_(self):
        """
        **LLM Docstring**

        Display the molecule inline in IPython (delegates to `draw`).
        """
        self.draw()._ipython_display_()

    @classmethod
    def _from_file_reader(cls,
                          file_reader,
                          block_reader,
                          block,
                          binary=False,
                          add_implicit_hydrogens=False,
                          guess_bonds=False,
                          conf_id=0,
                          charge=None,
                          sanitize_ops=None,
                          post_sanitize=True,
                          allow_generate_conformers=False,
                          num_confs=1,
                          optimize=False,
                          take_min=True,
                          force_field_type='mmff',
                          **kwargs
                          ):
        """
        **LLM Docstring**

        Shared helper for the `from_*` format importers: read a mol from a file path or
        an in-memory block using the supplied file/block reader functions, then wrap it
        via `from_rdmol`.

        :param file_reader: the file-reading function (or `None`)
        :type file_reader: Callable | None
        :param block_reader: the string/block-reading function
        :type block_reader: Callable
        :param block: the file path or block content
        :type block: str | bytes
        :param binary: treat the content as binary
        :type binary: bool
        :param add_implicit_hydrogens: add implicit hydrogens
        :type add_implicit_hydrogens: bool
        :param guess_bonds: perceive bonds from geometry
        :type guess_bonds: bool
        :param conf_id: the conformer id
        :type conf_id: int
        :param charge: the molecular charge
        :type charge: int | None
        :param sanitize_ops: sanitization flags
        :param post_sanitize: sanitize after reading
        :type post_sanitize: bool
        :param allow_generate_conformers: generate conformers if none exist
        :type allow_generate_conformers: bool
        :param num_confs: number of conformers to generate
        :type num_confs: int
        :param optimize: force-field optimize generated conformers
        :type optimize: bool
        :param take_min: keep only the lowest-energy conformer
        :type take_min: bool
        :param force_field_type: the force field for optimization
        :type force_field_type: str
        :return: the wrapped molecule
        :rtype: RDMolecule
        """
        if os.path.isfile(block):
            if file_reader is None:
                return cls._from_file_reader(
                    file_reader,
                    block_reader,
                    dev.read_file(block, mode='rb' if binary else 'r'),
                    add_implicit_hydrogens=add_implicit_hydrogens,
                    **kwargs
                )
            else:
                if binary and isinstance(block, str):
                    block = block.encode('utf-8')
                mol = file_reader(block, **kwargs)
        else:
            if binary and isinstance(block, str):
                block = block.encode('utf-8')
            mol = block_reader(block, **kwargs)
        return cls.from_rdmol(mol,
                              charge=charge,
                              conf_id=conf_id,
                              sanitize_ops=sanitize_ops,
                              sanitize=post_sanitize,
                              add_implicit_hydrogens=add_implicit_hydrogens,
                              guess_bonds=guess_bonds,
                              allow_generate_conformers=allow_generate_conformers,
                              num_confs=num_confs,
                              optimize=optimize,
                              take_min=take_min,
                              force_field_type=force_field_type)

    @classmethod
    def from_molblock(cls,
                      molblock,
                      add_implicit_hydrogens=False,
                      sanitize=False, remove_hydrogens=False,
                      **mol_opts
                      ):
        """
        **LLM Docstring**

        Build an `RDMolecule` from a MDL molblock/`.mol` file or string.

        :param molblock: the molblock file path or content
        :type molblock: str
        :param add_implicit_hydrogens: add implicit hydrogens
        :type add_implicit_hydrogens: bool
        :param sanitize: run sanitization
        :type sanitize: bool
        :param remove_hydrogens: remove explicit hydrogens
        :type remove_hydrogens: bool
        :param mol_opts: extra options forwarded to the reader
        :return: the wrapped molecule
        :rtype: RDMolecule
        """
        Chem = cls.chem_api()
        return cls._from_file_reader(
            Chem.MolFromMolFile,
            Chem.MolFromMolBlock,
            molblock,
            sanitize=sanitize, removeHs=remove_hydrogens,
            add_implicit_hydrogens=add_implicit_hydrogens,
            **mol_opts
        )

    @classmethod
    def from_mrv(cls,
                 molblock,
                 add_implicit_hydrogens=False,
                 sanitize=False, remove_hydrogens=False,
                 **mol_opts
                 ):
        """
        **LLM Docstring**

        Build an `RDMolecule` from a Marvin `.mrv` file or string.

        :param molblock: the MRV file path or content
        :type molblock: str
        :param add_implicit_hydrogens: add implicit hydrogens
        :type add_implicit_hydrogens: bool
        :param sanitize: run sanitization
        :type sanitize: bool
        :param remove_hydrogens: remove explicit hydrogens
        :type remove_hydrogens: bool
        :param mol_opts: extra options forwarded to the reader
        :return: the wrapped molecule
        :rtype: RDMolecule
        """
        Chem = cls.chem_api()
        return cls._from_file_reader(
            Chem.MolFromMrvFile,
            Chem.MolFromMrvBlock,
            molblock,
            sanitize=sanitize, removeHs=remove_hydrogens,
            add_implicit_hydrogens=add_implicit_hydrogens,
            **mol_opts
        )

    @classmethod
    def from_xyz(cls,
                 molblock,
                 add_implicit_hydrogens=False,
                 guess_bonds=True,
                 **mol_opts
                 ):
        """
        **LLM Docstring**

        Build an `RDMolecule` from an XYZ file or string (perceiving bonds by default).

        :param molblock: the XYZ file path or content
        :type molblock: str
        :param add_implicit_hydrogens: add implicit hydrogens
        :type add_implicit_hydrogens: bool
        :param guess_bonds: perceive bonds from geometry
        :type guess_bonds: bool
        :param mol_opts: extra options forwarded to the reader
        :return: the wrapped molecule
        :rtype: RDMolecule
        """
        Chem = cls.chem_api()
        return cls._from_file_reader(
            Chem.MolFromXYZFile,
            Chem.MolFromXYZBlock,
            molblock,
            add_implicit_hydrogens=add_implicit_hydrogens,
            guess_bonds=guess_bonds,
            **mol_opts
        )

    @classmethod
    def from_mol2(cls,
                  molblock,
                  add_implicit_hydrogens=False,
                  sanitize=False, remove_hydrogens=False,
                  **mol_opts
                  ):
        """
        **LLM Docstring**

        Build an `RDMolecule` from a Tripos `.mol2` file or string.

        :param molblock: the mol2 file path or content
        :type molblock: str
        :param add_implicit_hydrogens: add implicit hydrogens
        :type add_implicit_hydrogens: bool
        :param sanitize: run sanitization
        :type sanitize: bool
        :param remove_hydrogens: remove explicit hydrogens
        :type remove_hydrogens: bool
        :param mol_opts: extra options forwarded to the reader
        :return: the wrapped molecule
        :rtype: RDMolecule
        """
        Chem = cls.chem_api()
        return cls._from_file_reader(
            Chem.MolFromMol2File,
            Chem.MolFromMol2Block,
            molblock,
            add_implicit_hydrogens=add_implicit_hydrogens,
            sanitize=sanitize, removeHs=remove_hydrogens,
            **mol_opts
        )

    @classmethod
    def from_cdxml(cls,
                   molblock,
                   add_implicit_hydrogens=True,
                   **mol_opts
                   ):
        """
        **LLM Docstring**

        Build an `RDMolecule` from a ChemDraw `.cdxml` file or string.

        :param molblock: the CDXML file path or content
        :type molblock: str
        :param add_implicit_hydrogens: add implicit hydrogens
        :type add_implicit_hydrogens: bool
        :param mol_opts: extra options forwarded to the reader
        :return: the wrapped molecule
        :rtype: RDMolecule
        """
        Chem = cls.chem_api()
        return cls._from_file_reader(
            Chem.MolsFromCDXMLFile,
            Chem.MolsFromCDXML,
            molblock,
            add_implicit_hydrogens=add_implicit_hydrogens,
            **mol_opts
        )

    @classmethod
    def from_pdb(cls,
                 molblock,
                 add_implicit_hydrogens=True,
                 **mol_opts
                 ):
        """
        **LLM Docstring**

        Build an `RDMolecule` from a PDB file or string.

        :param molblock: the PDB file path or content
        :type molblock: str
        :param add_implicit_hydrogens: add implicit hydrogens
        :type add_implicit_hydrogens: bool
        :param mol_opts: extra options forwarded to the reader
        :return: the wrapped molecule
        :rtype: RDMolecule
        """
        Chem = cls.chem_api()
        return cls._from_file_reader(
            Chem.MolFromPDBFile,
            Chem.MolFromPDBString,
            molblock,
            add_implicit_hydrogens=add_implicit_hydrogens,
            **mol_opts
        )

    @classmethod
    def from_png(cls,
                 molblock,
                 add_implicit_hydrogens=False,
                 **mol_opts
                 ):
        """
        **LLM Docstring**

        Build an `RDMolecule` from an RDKit-metadata-bearing PNG file or string.

        :param molblock: the PNG file path or content
        :type molblock: str
        :param add_implicit_hydrogens: add implicit hydrogens
        :type add_implicit_hydrogens: bool
        :param mol_opts: extra options forwarded to the reader
        :return: the wrapped molecule
        :rtype: RDMolecule
        """
        Chem = cls.chem_api()
        return cls._from_file_reader(
            Chem.MolFromPNGFile,
            Chem.MolFromPNGString,
            molblock,
            add_implicit_hydrogens=add_implicit_hydrogens,
            **mol_opts
        )

    @classmethod
    def from_fasta(cls,
                   molblock,
                   add_implicit_hydrogens=True,
                   allow_generate_conformers=True,
                   **mol_opts
                   ):
        """
        **LLM Docstring**

        Build an `RDMolecule` from a FASTA sequence (generating a conformer by default).

        :param molblock: the FASTA content
        :type molblock: str
        :param add_implicit_hydrogens: add implicit hydrogens
        :type add_implicit_hydrogens: bool
        :param allow_generate_conformers: generate a conformer
        :type allow_generate_conformers: bool
        :param mol_opts: extra options forwarded to the reader
        :return: the wrapped molecule
        :rtype: RDMolecule
        """
        Chem = cls.chem_api()
        return cls._from_file_reader(
            None,
            Chem.MolFromFASTA,
            molblock,
            add_implicit_hydrogens=add_implicit_hydrogens,
            allow_generate_conformers=allow_generate_conformers,
            **mol_opts
        )

    @classmethod
    def from_inchi(cls,
                   molblock,
                   add_implicit_hydrogens=True,
                   allow_generate_conformers=True,
                   **mol_opts
                   ):
        """
        **LLM Docstring**

        Build an `RDMolecule` from an InChI string (generating a conformer by default).

        :param molblock: the InChI string
        :type molblock: str
        :param add_implicit_hydrogens: add implicit hydrogens
        :type add_implicit_hydrogens: bool
        :param allow_generate_conformers: generate a conformer
        :type allow_generate_conformers: bool
        :param mol_opts: extra options forwarded to the reader
        :return: the wrapped molecule
        :rtype: RDMolecule
        """
        Chem = cls.chem_api()
        return cls._from_file_reader(
            None,
            Chem.MolFromInChi,
            molblock,
            add_implicit_hydrogens=add_implicit_hydrogens,
            allow_generate_conformers=allow_generate_conformers,
            **mol_opts
        )

    @classmethod
    def from_helm(cls,
                   molblock,
                   add_implicit_hydrogens=True,
                   allow_generate_conformers=True,
                   **mol_opts
                   ):
        """
        **LLM Docstring**

        Build an `RDMolecule` from a HELM (macromolecule) string (generating a conformer
        by default).

        :param molblock: the HELM string
        :type molblock: str
        :param add_implicit_hydrogens: add implicit hydrogens
        :type add_implicit_hydrogens: bool
        :param allow_generate_conformers: generate a conformer
        :type allow_generate_conformers: bool
        :param mol_opts: extra options forwarded to the reader
        :return: the wrapped molecule
        :rtype: RDMolecule
        """
        Chem = cls.chem_api()
        return cls._from_file_reader(
            None,
            Chem.MolFromHELM,
            molblock,
            add_implicit_hydrogens=add_implicit_hydrogens,
            allow_generate_conformers=allow_generate_conformers,
            **mol_opts
        )

    def _to_file_or_string(self,
                           file_writer,
                           string_writer,
                           filename=None,
                           mode='w+',
                           binary=False,
                           **converter_opts):
        """
        **LLM Docstring**

        Shared helper for the `to_*` exporters: write the mol either to a file (via a
        file writer) or to a returned string (via a string writer), synthesizing the
        missing path through a temporary file when only one writer is available.

        :param file_writer: the file-writing function (or `None`)
        :type file_writer: Callable | None
        :param string_writer: the string-writing function (or `None`)
        :type string_writer: Callable | None
        :param filename: the output file path (or `None` to return a string)
        :type filename: str | None
        :param mode: the file open mode
        :type mode: str
        :param binary: treat the content as binary
        :type binary: bool
        :param converter_opts: extra options for the writer
        :return: the file path, or the serialized string
        :rtype: str | bytes
        """
        if filename is None:
            if string_writer is None:
                if binary:
                    mode = mode.replace('b', '')+"b"
                with tf.NamedTemporaryFile(mode=mode) as file:
                    res = self._to_file_or_string(file_writer, None,
                                                  filename=file.name,
                                                  mode=mode,
                                                  binary=binary,
                                                  **converter_opts)
                    if binary:
                        res = dev.read_file(file.name, mode='rb')
                    else:
                        res = dev.read_file(file.name, mode='r')
                    return res
            else:
                return string_writer(self.rdmol, **converter_opts)
        else:
            if file_writer is None:
                string = string_writer(self.rdmol, **converter_opts)
                if binary:
                    string = string.encode('utf-8')
                    mode = mode.replace('b', '')+"b"

                return dev.write_file(filename,
                               string,
                               mode=mode)
            else:
                return file_writer(self.rdmol, filename, **converter_opts)

    def to_xyz(self, filename=None, conf_id=None, **opts):
        """
        **LLM Docstring**

        Serialize the molecule to XYZ (returned as a string, or written to a file).

        :param filename: the output file path (or `None` to return a string)
        :type filename: str | None
        :param conf_id: the conformer id
        :type conf_id: int | None
        :param opts: extra writer options
        :return: the file path or XYZ string
        :rtype: str
        """
        Chem = self.chem_api()
        if conf_id is None:
            conf_id = self.mol.GetId()
        return self._to_file_or_string(
            Chem.MolToXYZFile,
            Chem.MolToXYZBlock,
            filename=filename,
            confId=conf_id,
            **opts
        )

    def to_molblock(self, filename=None, conf_id=None, **opts):
        """
        **LLM Docstring**

        Serialize the molecule to an MDL molblock (returned as a string, or written to a
        file).

        :param filename: the output file path (or `None` to return a string)
        :type filename: str | None
        :param conf_id: the conformer id
        :type conf_id: int | None
        :param opts: extra writer options
        :return: the file path or molblock string
        :rtype: str
        """
        Chem = self.chem_api()
        if conf_id is None:
            conf_id = self.mol.GetId()
        return self._to_file_or_string(
            Chem.MolToMolFile,
            Chem.MolToMolBlock,
            filename=filename,
            confId=conf_id,
            **opts
        )

    def to_mrv(self, filename=None, conf_id=None, **opts):
        """
        **LLM Docstring**

        Serialize the molecule to Marvin MRV (returned as a string, or written to a
        file).

        :param filename: the output file path (or `None` to return a string)
        :type filename: str | None
        :param conf_id: the conformer id
        :type conf_id: int | None
        :param opts: extra writer options
        :return: the file path or MRV string
        :rtype: str
        """
        Chem = self.chem_api()
        if conf_id is None:
            conf_id = self.mol.GetId()
        return self._to_file_or_string(
            Chem.MolToMrvFile,
            Chem.MolToMrvBlock,
            filename=filename,
            confId=conf_id,
            **opts
        )

    def to_pdb(self, filename=None, conf_id=None, **opts):
        """
        **LLM Docstring**

        Serialize the molecule to PDB (returned as a string, or written to a file).

        :param filename: the output file path (or `None` to return a string)
        :type filename: str | None
        :param conf_id: the conformer id
        :type conf_id: int | None
        :param opts: extra writer options
        :return: the file path or PDB string
        :rtype: str
        """
        Chem = self.chem_api()
        if conf_id is None:
            conf_id = self.mol.GetId()
        return self._to_file_or_string(
            Chem.MolToPDBFile,
            Chem.MolToPDBBlock,
            filename=filename,
            confId=conf_id,
            **opts
        )

    def to_cml(self, filename=None, **opts):
        """
        **LLM Docstring**

        Serialize the molecule to CML (returned as a string, or written to a file).

        :param filename: the output file path (or `None` to return a string)
        :type filename: str | None
        :param opts: extra writer options
        :return: the file path or CML string
        :rtype: str
        """
        Chem = self.chem_api()
        return self._to_file_or_string(
            Chem.MolToCMLFile,
            Chem.MolToCMLBlock,
            filename=filename,
            **opts
        )

    def _write_sdf(self,
                   mol,
                   file,
                   base_writer=None,
                   id_col=None,
                   conf_ids=None
                   ):
        """
        **LLM Docstring**

        Write the mol (optionally multiple conformers) to an SDF stream, creating an
        `SDWriter` when one isn't supplied.

        :param mol: the mol to write
        :type mol: Chem.Mol
        :param file: the output file/stream
        :param base_writer: an existing SD writer to reuse
        :param id_col: the id column for the writer
        :param conf_ids: the conformer ids to write (all in one record if omitted)
        :type conf_ids: Sequence | None
        :return: the file that was written
        :rtype: object
        """
        import rdkit.Chem.AllChem as Chem
        if base_writer is None:
            base_writer = Chem.SDWriter(file, idCol=id_col) if id_col is not None else Chem.SDWriter(file)
            with base_writer as w:
                if conf_ids is None:
                    w.write(mol)
                else:
                    for c in conf_ids:
                        w.write(mol, confId=c)
        else:
            if conf_ids is None:
                base_writer.write(mol)
            else:
                for c in conf_ids:
                    base_writer.write(mol, confId=c)
        return file

    def to_sdf(self, filename=None, **opts):
        """
        **LLM Docstring**

        Serialize the molecule to SDF (returned as a string, or written to a file).

        :param filename: the output file path (or `None` to return a string)
        :type filename: str | None
        :param opts: extra writer options (e.g. `conf_ids`)
        :return: the file path or SDF string
        :rtype: str
        """
        return self._to_file_or_string(
            self._write_sdf,
            None,
            filename=filename,
            **opts
        )

    @classmethod
    def allchem_api(cls):
        """
        **LLM Docstring**

        Return the RDKit `Chem.AllChem` submodule.

        :return: the `AllChem` module
        :rtype: module
        """
        return RDKitInterface.submodule("Chem.AllChem")
    @classmethod
    def get_force_field_type(cls, ff_type):
        """
        **LLM Docstring**

        Resolve a force-field name to the RDKit `(force_field_getter, property_generator)`
        pair.

        :param ff_type: the force-field name (`'mmff'`/`'uff'`) or an existing pair
        :type ff_type: str | tuple
        :return: the force-field getter (and property generator)
        :rtype: tuple
        """
        AllChem = cls.allchem_api()

        if isinstance(ff_type, str):
            if ff_type == 'mmff':
                ff_type = (AllChem.MMFFGetMoleculeForceField, AllChem.MMFFGetMoleculeProperties)
            elif ff_type == 'uff':
                ff_type = (AllChem.UFFGetMoleculeForceField, None)
            else:
                raise ValueError(f"can't get RDKit force field type from '{ff_type}")

        return ff_type

    def get_force_field(self, force_field_type='mmff', conf=None, mol=None, conf_id=None, **extra_props):
        """
        **LLM Docstring**

        Build an RDKit force-field object for a conformer, computing any needed
        force-field properties.

        :param force_field_type: the force-field name or getter pair
        :type force_field_type: str | tuple
        :param conf: an explicit conformer
        :param mol: an explicit mol
        :param conf_id: the conformer id
        :type conf_id: int | None
        :param extra_props: extra keyword arguments for the force-field getter
        :return: the force-field object
        :rtype: object
        """
        if conf is None:
            if mol is None:
                mol = self
            if conf_id is None:
                conf_id = mol.mol.GetId()
            mol = mol.rdmol
        else:
            if mol is None:
                mol = conf.GetOwningMol()
            if conf_id is None:
                conf_id = conf.GetId()
            if np.sum(np.abs(conf.GetPositions() - mol.GetConformer(conf_id).GetPositions())) > 1e-6:
                raise ValueError(
                    conf, mol.GetConformer(conf_id)
                )

        force_field_type = self.get_force_field_type(force_field_type)
        if isinstance(force_field_type, (list, tuple)):
            force_field_type, prop_gen = force_field_type
        else:
            prop_gen = None

        if prop_gen is not None:
            props = prop_gen(mol)
        else:
            props = None

        if props is not None:
            return force_field_type(mol, props, confId=conf_id, **extra_props)
        else:
            return force_field_type(mol, confId=conf_id, **extra_props)

    def evaluate_charges(self, coords, model='gasteiger'):
        """
        **LLM Docstring**

        Compute the per-atom partial charges for a set of coordinates (currently only
        the Gasteiger model).

        :param coords: the coordinates (used to set the conformer)
        :type coords: np.ndarray
        :param model: the charge model
        :type model: str
        :return: the partial charges
        :rtype: list[float]
        :raises ValueError: for an unsupported charge model
        """
        if model == 'gasteiger':
            from rdkit.Chem import AllChem
            AllChem.ComputeGasteigerCharges(self.rdmol)
            return [
                at.GetDoubleProp('_GasteigerCharge')
                for at in self.rdmol.GetAtoms()
            ]
        else:
            raise ValueError(f"charge model {model} not supported in RDKit")

    def calculate_energy(self, geoms=None, force_field_generator=None, force_field_type='mmff', conf_id=None):
        """
        **LLM Docstring**

        Compute the force-field energy of the current geometry, or of each geometry in a
        batch.

        :param geoms: a batch of geometries (or `None` for the current one)
        :type geoms: np.ndarray | None
        :param force_field_generator: a force-field factory (defaults to `get_force_field`)
        :type force_field_generator: Callable | None
        :param force_field_type: the force-field name
        :type force_field_type: str
        :param conf_id: the conformer id
        :type conf_id: int | None
        :return: the energy (or array of energies)
        :rtype: float | np.ndarray
        """
        Chem = self.chem_api()
        if conf_id is None:
            conf_id = self.mol.GetId()
        mol = Chem.Mol(self.rdmol, confId=conf_id)
        conf = mol.GetConformer(conf_id)

        if force_field_generator is None:
            force_field_generator = self.get_force_field

        with self.quiet_errors():
            if geoms is not None:
                cur_geom = np.array(self.mol.GetPositions()).reshape(-1, 3)
                geoms = np.asanyarray(geoms)
                base_shape = geoms.shape[:-2]
                geoms = geoms.reshape((-1,) + cur_geom.shape)
                vals = np.empty(len(geoms), dtype=float)
                try:
                    for i,g in enumerate(geoms):
                        conf.SetPositions(g.copy())
                        ff = force_field_generator(force_field_type, conf=conf, mol=mol)
                        vals[i] = ff.CalcEnergy()
                finally:
                    conf.SetPositions(cur_geom)
                return vals.reshape(base_shape)
            else:
                ff = force_field_generator(force_field_type, conf_id=conf_id)
                return ff.CalcEnergy()

    def calculate_gradient(self, geoms=None, force_field_generator=None, force_field_type='mmff', conf_id=None):
        """
        **LLM Docstring**

        Compute the force-field energy gradient of the current geometry, or of each
        geometry in a batch.

        :param geoms: a batch of geometries (or `None` for the current one)
        :type geoms: np.ndarray | None
        :param force_field_generator: a force-field factory (defaults to `get_force_field`)
        :type force_field_generator: Callable | None
        :param force_field_type: the force-field name
        :type force_field_type: str
        :param conf_id: the conformer id
        :type conf_id: int | None
        :return: the gradient (or batch of gradients)
        :rtype: np.ndarray
        """
        if force_field_generator is None:
            force_field_generator = self.get_force_field

        Chem = self.chem_api()
        if conf_id is None:
            conf_id = self.mol.GetId()
        mol = Chem.Mol(self.rdmol, confId=conf_id)
        conf = mol.GetConformer(0)

        with self.quiet_errors():
            cur_geom = np.array(conf.GetPositions()).reshape(-1, 3)
            if geoms is not None:
                geoms = np.asanyarray(geoms)
                base_shape = geoms.shape[:-2]
                geoms = geoms.reshape((-1,) + cur_geom.shape)
                vals = np.empty((len(geoms), np.prod(cur_geom.shape, dtype=int)), dtype=float)
                try:
                    for i, g in enumerate(geoms):
                        new_geom = g.copy().view(np.ndarray)
                        conf.SetPositions(new_geom)
                        ff = force_field_generator(force_field_type, conf=conf, mol=mol)
                        vals[i] = ff.CalcGrad()
                finally:
                    conf.SetPositions(cur_geom)
                return vals.reshape(base_shape + (-1,))
            else:
                ff = force_field_generator(force_field_type, conf_id=conf_id, conf=conf, mol=mol)
                return np.array(ff.CalcGrad()).reshape(-1)

    def calculate_hessian(self, force_field_generator=None, force_field_type='mmff', stencil=5, mesh_spacing=.01, **fd_opts):
        """
        **LLM Docstring**

        Compute the force-field Hessian at the current geometry by finite-differencing
        the analytic gradient.

        :param force_field_generator: a force-field factory
        :type force_field_generator: Callable | None
        :param force_field_type: the force-field name
        :type force_field_type: str
        :param stencil: the finite-difference stencil size
        :type stencil: int
        :param mesh_spacing: the finite-difference step
        :type mesh_spacing: float
        :param fd_opts: extra finite-difference options
        :return: the Hessian tensor
        :rtype: np.ndarray
        """
        from ..Zachary import FiniteDifferenceDerivative

        cur_geom = np.array(self.mol.GetPositions()).reshape(-1, 3)

        # if force_field_generator is None:
        #     force_field_generator = self.get_force_field(force_field_type)

        # def eng(structs):
        #     structs = structs.reshape(structs.shape[:-1] + (-1, 3))
        #     new_grad = self.calculate_energy(structs, ff=ff)
        #     return new_grad
        # der = FiniteDifferenceDerivative(eng, function_shape=((0,), (0,)), stencil=stencil, mesh_spacing=mesh_spacing, **fd_opts)
        # return der.derivatives(cur_geom.flatten()).derivative_tensor(2)

        def jac(structs):
            """
            **LLM Docstring**

            Gradient function passed to the finite-difference differentiator: reshape the
            flattened structures and return their force-field gradients.

            :param structs: the flattened structures
            :type structs: np.ndarray
            :return: the gradients
            :rtype: np.ndarray
            """
            structs = structs.reshape(structs.shape[:-1] + (-1, 3))
            new_grad = self.calculate_gradient(structs,
                                               force_field_generator=force_field_generator,
                                               force_field_type=force_field_type
                                               )
            return new_grad
        der = FiniteDifferenceDerivative(jac, function_shape=((0,), (0,)), stencil=stencil, mesh_spacing=mesh_spacing, **fd_opts)
        return der.derivatives(cur_geom.flatten()).derivative_tensor(1)

    def get_optimizer_params(self, maxAttempts=1000, useExpTorsionAnglePrefs=True, useBasicKnowledge=True, **etc):
        """
        **LLM Docstring**

        Build an RDKit ETKDGv3 parameter object for structure optimization/embedding.

        :param maxAttempts: the maximum embedding attempts
        :type maxAttempts: int
        :param useExpTorsionAnglePrefs: use experimental torsion prefs
        :type useExpTorsionAnglePrefs: bool
        :param useBasicKnowledge: use basic chemical knowledge
        :type useBasicKnowledge: bool
        :param etc: extra parameters set on the params object
        :return: the parameter object
        :rtype: object
        """
        AllChem = self.allchem_api()

        params = AllChem.ETKDGv3()
        params.maxAttempts = maxAttempts  # Increase the number of attempts
        params.useExpTorsionAnglePrefs = useExpTorsionAnglePrefs
        params.useBasicKnowledge = useBasicKnowledge
        for k,v in etc.items():
            setattr(params, k, v)

        return params

    def optimize_structure(self, geoms=None, force_field_type='mmff', optimizer=None, maxIters=1000, **opts):
        """
        **LLM Docstring**

        Force-field optimize the current geometry, or each geometry in a batch, returning
        the optimizer status and optimized coordinates.

        :param geoms: a batch of geometries (or `None` for the current one)
        :type geoms: np.ndarray | None
        :param force_field_type: the force-field name
        :type force_field_type: str
        :param optimizer: a custom optimizer callable
        :type optimizer: Callable | None
        :param maxIters: the maximum optimization iterations
        :type maxIters: int
        :param opts: extra optimizer options
        :return: `(status, optimized_coords, extra)`
        :rtype: tuple
        """

        if optimizer is None:
            ff_helpers = RDKitInterface.submodule("Chem.rdForceFieldHelpers")
            def optimizer(mol, **etc):
                """
                **LLM Docstring**

                Default optimizer: build the force field for the mol and run RDKit's
                force-field minimization.

                :param mol: the molecule to optimize
                :type mol: RDMolecule
                :param etc: extra options (e.g. `maxIters`)
                :return: the optimization status code
                :rtype: int
                """
                ff = mol.get_force_field(force_field_type)
                return ff_helpers.OptimizeMolecule(ff)

        maxIters = int(maxIters)
        if geoms is not None:
            cur_geom = np.array(self.mol.GetPositions()).reshape(-1, 3)
            geoms = np.asanyarray(geoms, dtype=float)
            base_shape = geoms.shape[:-2]
            geoms = geoms.reshape((-1,) + cur_geom.shape)
            opt_vals = np.empty((len(geoms),), dtype=int)
            opt_geoms = np.empty_like(geoms)
            try:
                for i, g in enumerate(geoms):
                    self.mol.SetPositions(g)
                    opt_vals[i] = optimizer(self, maxIters=maxIters, **opts)
                    opt_geoms[i] = self.mol.GetPositions()
            finally:
                self.mol.SetPositions(cur_geom)
            return opt_vals.reshape(base_shape), opt_geoms.reshape(base_shape + opt_geoms.shape[1:]), {}
        else:
            opt = optimizer(self, maxIters=maxIters, **opts)
            return opt, self.mol.GetPositions(), {}

    def show(self):
        """
        **LLM Docstring**

        Display an interactive 3D rendering of the current conformer (via RDKit's
        IPython 3D console).

        :return: the 3D display
        :rtype: object
        """
        return RDKitInterface.submodule('Chem.Draw.IPythonConsole').drawMol3D(
            self.mol.GetOwningMol(),
            confId=self.mol.GetId()
            # view=None, confId=-1, drawAs=None, bgColor=None, size=None
        )
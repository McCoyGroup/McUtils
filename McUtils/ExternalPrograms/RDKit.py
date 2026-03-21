

__all__ = [
    "RDMolecule"
]

import base64
import itertools
import re
import functools
import uuid

import numpy as np, io, os
from .. import Numputils as nput
from .. import Devutils as dev
from ..Data import AtomData

from .ChemToolkits import RDKitInterface
from .ExternalMolecule import ExternalMolecule
from .. import Coordinerds as coordops
from ..Jupyter import JHTML


class RDMolecule(ExternalMolecule):
    """
    A simple interchange format for RDKit molecules
    """

    def __init__(self, rdconf, charge=None):
        #atoms, coords, bonds):
        self._rdmol = rdconf.GetOwningMol()
        super().__init__(rdconf)
        self.charge = charge

    @property
    def rdmol(self):
        if self._rdmol is None:
            self._rdmol = self.mol.GetOwningMol()
        return self._rdmol
    @property
    def atoms(self):
        mol = self.rdmol
        return [atom.GetSymbol() for atom in mol.GetAtoms()]
    @property
    def bonds(self):
        mol = self.rdmol
        return [
            [b.GetBeginAtomIdx(), b.GetEndAtomIdx(), b.GetBondTypeAsDouble()]
            for b in mol.GetBonds()
        ]
    @property
    def coords(self):
        return self.mol.GetPositions()
    @coords.setter
    def coords(self, coords):
        coords = np.asanyarray(coords)
        self.mol.SetPositions(coords)
    @property
    def rings(self):
        return self.rdmol.GetRingInfo().AtomRings()
    @property
    def meta(self):
        return self.rdmol.GetPropsAsDict()

    def copy(self):
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
        from rdkit.Chem import AllChem
        AllChem.ComputeGasteigerCharges(self.rdmol)
        return [
            at.GetDoubleProp('_GasteigerCharge')
            for at in self.rdmol.GetAtoms()
        ]

    @property
    def formal_charges(self):
        return [
            at.GetFormalCharge()
            for at in self.rdmol.GetAtoms()
        ]

    class NullContext:
        def __enter__(self):
            ...
        def __exit__(self, exc_type, exc_val, exc_tb):
            ...
    @classmethod
    def quiet_errors(cls, verbose=False):
        from rdkit.rdBase import BlockLogs
        if verbose:
            return cls.NullContext()
        else:
            return BlockLogs()

    @classmethod
    def chem_api(cls):
        return RDKitInterface.submodule("Chem")

    @classmethod
    def _prep_mol(cls, rdkit_mol):
        Chem = cls.allchem_api()
        rdkit_mol.UpdatePropertyCache(strict=False)
        _ = Chem.GetSymmSSSR(rdkit_mol)
        Chem.SetHybridization(rdkit_mol)
    @classmethod
    def from_rdmol(cls, rdmol, conf_id=0, charge=None, guess_bonds=False, sanitize=True,
                   add_implicit_hydrogens=False,
                   sanitize_ops=None,
                   allow_generate_conformers=False,
                   num_confs=1,
                   optimize=False,
                   take_min=True,
                   force_field_type='mmff'):
        Chem = cls.chem_api() # to get nice errors
        rdmol = Chem.AddHs(rdmol, explicitOnly=not add_implicit_hydrogens)
        if charge is None:
            charge = Chem.GetFormalCharge(rdmol)
        if guess_bonds:
            rdDetermineBonds = RDKitInterface.submodule("Chem.rdDetermineBonds")
            rdmol = Chem.Mol(rdmol)
            rdDetermineBonds.DetermineConnectivity(rdmol, charge=charge)
            # return cls.from_rdmol(rdmol, conf_id=conf_id, guess_bonds=False, charge=charge)
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
            conf_0 = rdmol.GetConformer(conf_id)
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
            mol = Chem.AddHs(mol, explicitOnly=True)
            conf = Chem.Conformer(len(atoms))
            conf.SetPositions(np.asanyarray(coords))
            conf.SetId(0)
            mol.AddConformer(conf)
            if add_implicit_hydrogens:
                mol = Chem.AddHs(mol, explicitOnly=False, addCoords=True)

            if guess_bonds is None:
                guess_bonds = bonds is None

            return cls.from_rdmol(mol, conf_id=0, charge=charge, guess_bonds=guess_bonds, sanitize=sanitize)

    @classmethod
    def from_mol(cls, mol, coord_unit="Angstroms", guess_bonds=None):
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
        Chem = cls.chem_api()
        mol = None
        for i in range(which+1):
            mol = next(Chem.ForwardSDMolSupplier(stream, sanitize=False, removeHs=False))
        return mol
    @classmethod
    def from_sdf(cls, sdf_string, which=0):
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
        AllChem = cls.allchem_api()
        version = version.lower()
        if version == 'v3':
            params = AllChem.ETKDGv3()
        elif version == 'v2':
            params = AllChem.ETKDGv3()
        elif version == 'v1':
            params = AllChem.ETKDGv3()
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
                  replacements=None,
                  **opts
                  ):
        Chem = cls.chem_api()
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
        if not sanitize:
            try:
                rdkit_mol.UpdatePropertyCache()
            except Chem.rdchem.MolSanitizeException:
                rdkit_mol.UpdatePropertyCache(strict=False)
                _ = Chem.GetSymmSSSR(rdkit_mol)
                Chem.SetHybridization(rdkit_mol)

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
            **opts
        )

        if reorder_from_atom_map:
            base_map = [a.GetAtomMapNum() for a in rdkit_mol.GetAtoms()]
            base_map = [len(base_map)+1 if a == 0 else a for a in base_map]
            # need to use a stable sort
            rdkit_mol = Chem.RenumberAtoms(rdkit_mol, np.argsort(base_map, kind='merge').tolist())

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
                  **opts):
        Chem = self.allchem_api()
        mol = self.rdmol
        if compute_stereo:
            mol = Chem.Mol(mol)
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
            og_atom_map = list(range(len(self.atoms)))
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
    def _prep_draw_opts(cls, format, opts):
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
        if len(font_name) > 0 and not os.path.isfile(font_name):
            from matplotlib import font_manager
            font_file = font_manager.findfont(font_name)
        else:
            font_file = font_name
        draw_opts.fontFile = font_file
    @staticmethod
    def _get_font_file(draw_opts):
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
        from ..Plots import ColorPalette
        if v is None: return None
        if isinstance(v, str):
            v = np.array(ColorPalette.parse_color_string(v))
            v = tuple(v/255)
        return tuple(float(vv) for vv in v)
    @classmethod
    def _handle_draw_elements(cls, elements):
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
        Draw = RDKitInterface.submodule("Chem.Draw")
        rdMolDraw2D = Draw.rdMolDraw2D

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
            mol = rdMolDraw2D.PrepareMolForDrawing(mol)
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
            mol = rdMolDraw2D.PrepareMolForDrawing(mol)
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
        Chem = self.chem_api()
        query = Chem.MolFromSmarts(query)
        return self.rdmol.GetSubstructMatches(query)

    def get_atom_neighbors(self, i, n=1, mol=None, graph=None):
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

            elif view_settings is not None:
                coords_3d = self.coords
                if non_h_atoms is not None:
                    coords_3d = coords_3d[non_h_atoms, :]
                if not modified:
                    mol = Chem.Mol(mol)
                    modified = True
                conf = mol.GetConformer()
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
            if radius_to_range_scaling is None and plot_range is not None:
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

        return self.DisplayImage(draw_fig, format,
                                 plot_range=plot_range,
                                 postdraw=postdraw,
                                 scaling_factor=radius_to_range_scaling,
                                 splits=splits,
                                 include_save_buttons=include_save_buttons)

    def plot(self,
             conf_id=None,
             image_size=(450, 450),
             **opts):
        # import py3Dmol
        from rdkit.Chem.Draw import IPythonConsole

        if conf_id is None:
            conf_id = self.mol.GetId()

        opts = dict(dict(confId=conf_id, size=image_size),
                    **{self._camel_case(k): v for k, v in opts.items()})
        return IPythonConsole.drawMol3D(self.rdmol, confId=self.mol, **opts)

    @classmethod
    def _plain_encode(cls, flat_z, byte_size):
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
        from .. import Graphs
        atoms = np.arange(len(mol.GetAtoms()))
        bonds = [
            [b.GetBeginAtomIdx(), b.GetEndAtomIdx()]
            for b in mol.GetBonds()
        ]
        return Graphs.EdgeGraph(atoms, bonds)
    def get_edge_graph(self, mol=None):
        from .. import Graphs
        if mol is None:
            atoms, bonds = np.arange(len(self.atoms)), [b[:2] for b in self.bonds]
            return Graphs.EdgeGraph(atoms, bonds)
        else:
            return self.get_mol_edge_graph(mol)

    class DisplayImage:
        def __init__(self, figure, format,
                     plot_range=None, scaling_factor=None,
                     splits=None, postdraw=None,
                     include_save_buttons=False, id=None):
            self.figure = figure
            self.plot_range = plot_range
            self.scaling_factor = scaling_factor
            self.splits = splits
            self.postdraw = postdraw
            self.fmt = format
            if id is None:
                id = "rdkit-" + str(uuid.uuid4())[:6]
            self.id = id
            self._raw_text = None
            self._text = None
            self.include_save_buttons = include_save_buttons

        @classmethod
        def split_string_by_segments(cls, text, split_dict):
            chunk_iter = 0
            chunks = []
            flat_splits = []
            for key, splits in sorted(split_dict.items()):
                for i, p in enumerate(splits):
                    flat_splits.append((f"{key}_{i}", p))
            for lab, (start, end) in sorted(flat_splits, key=lambda ks:ks[1][0]):
                chunks.append((None, text[chunk_iter:start]))
                chunks.append((lab, text[start:end]))
                chunk_iter = end
            if chunk_iter > 0 and chunk_iter < len(text):
                chunks.append((None, text[chunk_iter:]))
            return chunks

        @classmethod
        def _path_addition_function(cls, xml_modifier):
            from ...Jupyter import JHTML
            def create_new_element(t):
                uuh = JHTML.HTML.parse(t)
                new_mod = xml_modifier(uuh)
                if not isinstance(new_mod, str):
                    new_mod = new_mod.tostring()
                return new_mod

            return create_new_element

        @classmethod
        def _text_addition_function(cls, text, mode='text', font_options=None, **modifiers):
            if mode == 'text':
                def modify_text_element(parsed_elem):
                    opts = parsed_elem.attrs | modifiers
                    path: str = opts.pop('d', None)
                    path = path.replace("M", "").replace("Q", "").replace("L", "").replace(",", "")
                    centroid = np.average(np.array(path.split()).astype(float).reshape(-1, 2), axis=0)
                    x, y = centroid
                    return JHTML.HTML.XMLElement("text", text, x=f"{x:.1f}", y=f"{y:.1f}", **opts)
            else:
                if font_options is None:
                    font_options = {}
                text_path = cls._text_to_path(text, **font_options)

                def modify_text_element(parsed_elem):
                    opts = parsed_elem.attrs | modifiers
                    path: str = opts.pop('d', None)
                    path = path.replace("M", "").replace("Q", "").replace("L", "").replace(",", "")
                    verts = np.array(path.split()).astype(float).reshape(-1, 2)
                    bbox = (
                        (np.min(verts[:, 0]), np.max(verts[:, 0])),
                        (np.min(verts[:, 1]), np.max(verts[:, 1]))
                    )
                    d = cls._path_to_svg(text_path, bbox)
                    return JHTML.HTML.XMLElement("path", d=d, **opts)
            return cls._path_addition_function(modify_text_element)
        @classmethod
        def _text_to_path(cls, text, **font_opts):
            from matplotlib.textpath import TextPath
            from matplotlib.font_manager import FontProperties
            fp = FontProperties(**font_opts)
            return TextPath((0, 0), text, prop=fp)
        @classmethod
        def _path_to_svg(cls, path,
                         target_bbox: tuple[tuple[float, float], tuple[float, float]],
                         base_height=None,
                         y_flip: bool = True):
            from matplotlib.path import Path
            # Matplotlib path code → SVG command mapping
            _CMD_MAP = {
                Path.MOVETO: "M",
                Path.LINETO: "L",
                Path.CURVE3: "Q",  # quadratic Bézier
                Path.CURVE4: "C",  # cubic Bézier
                Path.CLOSEPOLY: "Z",
            }
            # Number of vertices consumed by each code (including the "current" vertex)
            _VERT_COUNT = {
                Path.MOVETO: 1,
                Path.LINETO: 1,
                Path.CURVE3: 2,  # 1 control + 1 end
                Path.CURVE4: 3,  # 2 controls + 1 end
                Path.CLOSEPOLY: 0,  # vertex is ignored
            }

            verts = np.asarray(path.vertices, dtype=float)
            bbox_init = (
                (np.min(verts[:, 0]), np.max(verts[:, 0])),
                (np.min(verts[:, 1]), np.max(verts[:, 1]))
            )
            dims_init = (
                bbox_init[0][1] - bbox_init[0][0],
                bbox_init[1][1] - bbox_init[1][0],
            )
            codes = path.codes if path.codes is not None else (
                    [Path.MOVETO] + [Path.LINETO] * (len(verts) - 1)
            )

            if y_flip:
                h = dims_init[1] if base_height is None else base_height
                verts = verts.copy()
                verts[:, 1] = h - verts[:, 1]

            dims_target = (
                target_bbox[0][1] - target_bbox[0][0],
                target_bbox[1][1] - target_bbox[1][0],
            )
            scaling = max(np.array(dims_target) / np.array(dims_init))

            verts = (
                    (verts - np.array([[bbox_init[0][0], bbox_init[1][0]]])) * scaling
                    + np.array([[target_bbox[0][0], target_bbox[1][0]]])
            )

            parts = []
            i = 0
            while i < len(codes):
                code = codes[i]

                if code == Path.STOP:
                    i += 1
                    continue

                cmd = _CMD_MAP.get(code)
                if cmd is None:
                    i += 1
                    continue

                if code == Path.CLOSEPOLY:
                    parts.append("Z")
                    i += 1
                    continue

                n = _VERT_COUNT[code]
                seg_verts = verts[i: i + n]
                coord_str = " ".join(f"{x:.6g},{y:.6g}" for x, y in seg_verts)
                parts.append(f"{cmd} {coord_str}")
                i += n

            return " ".join(parts)

        multivalue_attrs = {'class'}
        @classmethod
        def _prep_svg_val(cls, attr, old, val):
            from ..Jupyter.JHTML import CSS
            #TODO: handle styles
            if attr == 'style':
                if len(old) > 0:
                    if isinstance(val, str):
                        val = CSS.parse(val)
                    else:
                        val = CSS(**val)
                    old = CSS.parse(old)
                    val = CSS(**(old.props|val.props)).tostring()
                elif isinstance(val, dict):
                    val = CSS(**val).tostring()
            else:
                if isinstance(val, str):
                    if attr in cls.multivalue_attrs:
                        if len(old) > 0:
                            val = old + " " + val
                else:
                    val = val(old)
            return val
        @classmethod
        def _apply_attr_tf(cls, attr, rest, value):
            if rest[1] == "'":
                val_bits = rest[2:].split("'", 1)  # always `'` from rdkit
                if len(val_bits) == 1:
                    old, rest = val_bits
                else:
                    old = val_bits[0]
                    rest = ""
                val = cls._prep_svg_val(attr, old, value)
                rest = f"='{val}'{rest}"
            else:
                val_bits = rest[1:].split(" ", 1)
                if len(val_bits) == 1:
                    old = val_bits[0]
                    rest = ""
                else:
                    old, rest = val_bits
                    rest = " " + rest
                val = cls._prep_svg_val(attr, old, value)
                rest = f'={val}{rest}'
            return rest
        @classmethod
        def _inject_attr(cls, tag, body, attr, value):
            header, csep, rest = tag.partition(attr)
            if len(rest) == 0 or (len(rest) == 1 and rest[0] == "="):
                value = cls._prep_svg_val(attr, "", value)
                header += f" {attr}='{value}'"
            else:
                if (header[-1] == " " or header[-1] == "<") and rest[0] == "=":
                    rest = cls._apply_attr_tf(attr, rest, value)
                else:
                    if attr+"=" in rest:
                        oh, oc = header, csep
                        header, csep, subrest = rest.partition(attr+"=")
                        header = oh+oc+header
                        csep = attr
                        rest = "="+subrest
                        if header[-1] == " ":
                            rest = cls._apply_attr_tf(attr, rest, value)
                    else:
                        header = header + csep + rest
                        csep = " "
                        rest = f"{attr}='{value}'"

            tag = header + csep + rest
            return tag, body
        @classmethod
        def _find_end_tag(cls, text, tag_start, end_tag1, end_tag2, closer_tag):
            tag_end1 = text.find(end_tag1, tag_start)
            tag_end2 = text.find(end_tag2, tag_start)
            which_int = None
            if tag_end1 < 0:
                if tag_end2 < 0:
                    return -1, None
                else:
                    tag_end = tag_end2
                    which = end_tag2
                    which_int = 1
            elif tag_end2 < 0:
                tag_end = tag_end1
                which = end_tag1
                which_int = 0
            elif tag_end1 <= tag_end2:
                tag_end = tag_end1
                which = end_tag1
                which_int = 0
            else:
                tag_end = tag_end2
                which = end_tag2
                which_int = 1
            tag_end = text.find(closer_tag, tag_end + 1)
            if tag_end < 0:
                return -1, None
            tag_end = tag_end + 1
            return tag_end, which
        @classmethod
        def _iter_xml_chunk(cls, text:str):
            end_tag1 = "/>"
            end_tag2 = "</"
            open_tag = "<"
            closer_tag = ">"
            cur_l = -1
            end_l = len(text)
            stack = []
            while cur_l < end_l:
                tag_start = text.find(open_tag, cur_l+1)
                if tag_start < 0:
                    break
                cur_l += 1
                tag_end, end_tag = cls._find_end_tag(text, tag_start, end_tag1, end_tag2, closer_tag)
                if tag_end < 0:
                    break
                tag_end += len(closer_tag)
                sub_chunk = text[cur_l:tag_end]
                opener_counts = sub_chunk.count(open_tag)
                closer_counts = sub_chunk.count(closer_tag)
                if opener_counts == closer_counts:
                    yield sub_chunk
                else:
                    for diff in range(closer_counts - opener_counts):
                        tag_start = text.find(closer_tag, tag_start+1)
                        tag_start = text.find(open_tag, tag_start+1)
                        stack.append(tag_start)
                    sub_chunk = text[tag_start:tag_end]
                    children = [sub_chunk]
                    for ts in reversed(stack):
                        te, end_tag = cls._find_end_tag(text, tag_start, end_tag1, end_tag2, closer_tag)
                        if te < 0:
                            raise ValueError("unclosed XML")
                        te += len(closer_tag)
                        children.append((text[ts:tag_start], text[tag_end:te]))
                        tag_start = ts
                        tag_end = te
                    yield children
                cur_l += tag_end - cur_l
        @classmethod
        def _tranform_single(cls, t, transformation):
            if len(t.strip()) > 0:
                # we assume no nesting
                tag, sep, body = t.partition(">")
                if tag[-1] == "/":
                    tag = tag[:-1]
                    sep = "/" + sep
                if "</" not in tag:
                    tag, body = transformation(tag, body)
                body = cls._transform_svg(body, transformation)
                t = tag + sep + body
            return t
        @classmethod
        def _transform_svg(cls, text, transformation):
            chunks = []
            for t in cls._iter_xml_chunk(text):
                if isinstance(t, str):
                    if len(t.strip()) > 0:
                        t = cls._tranform_single(t, transformation)
                else:
                    # only transform top-level element by default
                    # requires constructing, TODO: allow nested tfs
                    body = t[-1]
                    for header, footer in reversed(t[-1]):
                        body = header + body + footer
                    t = cls._tranform_single(body, transformation)
                chunks.append(t)
            return "".join(chunks)
        @classmethod
        def add_classes(cls, label, text):
            if label is not None and len(text) > 0:
                label = label.replace("_", "-")
                text =  f"<g class='{label}'>\n{text}</g>"
            return text
        @classmethod
        def _attr_annotation_function(cls, attr, value):
            def annotate(tag, body):
                return cls._inject_attr(tag, body, attr, value)
            return annotate
        default_annotation_pattern = None
        default_annotation_exclude = 'mol-\w+'
        @classmethod
        def _prep_annotation_function(cls, attrs_dict):
            if dev.is_list_like(attrs_dict):
                subfuncs = [
                    cls._prep_annotation_function(d)
                    for d in attrs_dict
                ]
                def transform(label, text, return_applied=False):
                    applied = False
                    for f in subfuncs:
                        text, applied = f(label, text, return_applied=True)
                        if applied:
                            break
                    if return_applied:
                        return text, applied
                    else:
                        return text
            else:
                funcs = []
                if attrs_dict is None:
                    attrs_dict = {'classes':True}
                cls_prep = attrs_dict.pop('classes', None)
                matches = attrs_dict.pop('pattern', None)
                excludes = attrs_dict.pop('exclude', cls.default_annotation_exclude)
                rep = attrs_dict.pop('replacement', None)
                if isinstance(rep, dict):
                    text = rep.pop('text')
                    rep = cls._text_addition_function(text, **rep)
                for k,v in attrs_dict.items():
                    f = cls._attr_annotation_function(k, v)
                    funcs.append(f)
                def transform(label, text, return_applied=False):
                    apply_tf = True
                    if apply_tf and matches is not None:
                        if isinstance(matches, (str, re.Pattern)):
                            apply_tf = label is not None and bool(re.match(matches, label))
                        else:
                            apply_tf = matches(label)
                    if apply_tf and excludes is not None:
                        if isinstance(excludes, (str, re.Pattern)):
                            apply_tf = label is not None and not bool(re.match(excludes, label))
                        else:
                            apply_tf = not excludes(label)
                    if apply_tf:
                        if rep is not None:
                            text = rep(text)
                        text = cls._transform_svg(
                            text,
                            lambda tag,body:functools.reduce(lambda x, y: y(*x), funcs, (tag, body))
                        )
                        if cls_prep is True:
                            k = label
                        elif cls_prep:
                            k = cls_prep(label)
                        else:
                            k = None
                        if k is not None:
                            text = cls.add_classes(k, text)
                    if return_applied:
                        return text, apply_tf
                    else:
                        return text
            return transform
        @classmethod
        def annotate_text(cls, text, splits, annotation_map=None):
            bits = []
            samp = ""
            if callable(annotation_map):
                function = annotation_map
            else:
                function = cls._prep_annotation_function(annotation_map)
            for label, c in cls.split_string_by_segments(text, splits):
                samp += c
                c = function(label, c)
                bits.append(c)
            return "".join(bits)
        def postprocess(self, text):
            #TODO: set up options dispatch for this
            postdraw = self.postdraw
            if dev.str_is(self.postdraw, 'annotate'):
                postdraw = {'annotate':{}}
            if postdraw is not None:
                if not callable(postdraw):
                    if 'annotate' not in postdraw:
                        annotation_function = postdraw
                    else:
                        annotation_function = postdraw['annotate']
                    postdraw = functools.partial(self.annotate_text, annotation_map=annotation_function)
                text = postdraw(text, self.splits)
            # print(text)
            # raise Exception(...)
            return text
        @property
        def text(self):
            if self._text is None:
                self.figure.FinishDrawing()
                self._raw_text = self.figure.GetDrawingText()
                self._text = self.postprocess(self._raw_text)
            return self._text

        @classmethod
        def get_svg_script(self, id):
            return f"""
        (function(){{
          let link = document.createElement('a');
          let base_name = '{id}';
          link.download = base_name + '.svg';
          let serializer = new XMLSerializer();
          let svg = document.getElementById('{id}').getElementsByTagName('svg')[0]
          let source = serializer.serializeToString(svg);
          link.href = "data:image/svg+xml;charset=utf-8,"+encodeURIComponent(source);
          link.click();
        }})()"""

        @classmethod
        def get_png_from_svg_script(self, id):
            return f"""
                (function(){{
                  let base_name = '{id}';
                  let serializer = new XMLSerializer();
                  let svg = document.getElementById('{id}').getElementsByTagName('svg')[0]
                  let source = serializer.serializeToString(svg);
                    
                  // https://stackoverflow.com/a/28226736  
                  const svgBlob = new Blob([source], {{type: 'image/svg+xml;charset=utf-8'}});
                  const url = window.URL.createObjectURL(svgBlob);

                  const image = new Image();
                  image.width = svg.width.baseVal.value;
                  image.height = svg.height.baseVal.value;
                  image.src = url;
                  image.onload = function () {{
                    const canvas = document.createElement('canvas');
                    canvas.width = image.width;
                    canvas.height = image.height;
                
                    const ctx = canvas.getContext('2d');
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    ctx.drawImage(image, 0, 0);
                    window.URL.revokeObjectURL(url);
                
                    const imgURI = canvas
                      .toDataURL('image/png')
                      .replace('image/png', 'image/octet-stream');
                    
                    let link = document.createElement('a');
                    link.download = base_name + '.png';
                    link.target = '_blank';
                    link.href = imgURI;
                
                    link.click()    
                  }};
                }})()"""

        @classmethod
        def get_png_script(self, id):
            return f"""
        (function(){{
          let link = document.createElement('a');
          let base_name = '{id}';
          link.download = base_name + '.png';
          link.href = document.getElementById('{id}').getElementsByTagName('img')[0].src
          link.click();
        }})()"""

        def to_widget(self):
            from ..Jupyter.JHTML import HTML
            if self.fmt == 'svg':
                obj = HTML.parse(self.text, namespace='http://www.w3.org/2000/svg')
                if self.include_save_buttons:
                    obj = JHTML.Div(
                        obj,
                        JHTML.Div(
                            JHTML.Button("Download SVG", onclick=self.get_svg_script(self.id)),
                            JHTML.Button("Download PNG", onclick=self.get_png_from_svg_script(self.id)),
                            display='flex'
                        ),
                        id=self.id,
                        display='block'
                    )
            else:
                b64_url = base64.b64encode(self.text.encode())
                data_url = "data:image/png;base64," + b64_url.decode('utf-8')
                obj = HTML.Image(src=data_url)
                if self.include_save_buttons:
                    obj = JHTML.Div(
                        obj,
                        JHTML.Button("Download", onclick=self.get_png_script(self.id)),
                        id=self.id,
                        display='block'
                    )
            return obj

        def _ipython_display_(self):
            self.to_widget()._ipython_display_()

        def show(self):
            self.to_widget().display()

        def save(self, file):
            if self.fmt == 'svg':
                with open(file, 'w+') as out:
                    out.write(self.text)
            else:
                from PIL import Image
                obj = Image.open(io.BytesIO(self.text))
                obj.save(file, format=self.fmt)

    def _ipython_display_(self):
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
        if filename is None:
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
        Chem = self.chem_api()
        return self._to_file_or_string(
            Chem.MolToCMLFile,
            Chem.MolToCMLBlock,
            filename=filename,
            **opts
        )


    @classmethod
    def allchem_api(cls):
        return RDKitInterface.submodule("Chem.AllChem")
    @classmethod
    def get_force_field_type(cls, ff_type):
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
        Chem = self.chem_api()
        if conf_id is None:
            conf_id = self.mol.GetId()
        mol = Chem.Mol(self.rdmol, confId=conf_id)
        conf = mol.GetConformer(0)

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
            structs = structs.reshape(structs.shape[:-1] + (-1, 3))
            new_grad = self.calculate_gradient(structs,
                                               force_field_generator=force_field_generator,
                                               force_field_type=force_field_type
                                               )
            return new_grad
        der = FiniteDifferenceDerivative(jac, function_shape=((0,), (0,)), stencil=stencil, mesh_spacing=mesh_spacing, **fd_opts)
        return der.derivatives(cur_geom.flatten()).derivative_tensor(1)

    def get_optimizer_params(self, maxAttempts=1000, useExpTorsionAnglePrefs=True, useBasicKnowledge=True, **etc):
        AllChem = self.allchem_api()

        params = AllChem.ETKDGv3()
        params.maxAttempts = maxAttempts  # Increase the number of attempts
        params.useExpTorsionAnglePrefs = useExpTorsionAnglePrefs
        params.useBasicKnowledge = useBasicKnowledge
        for k,v in etc.items():
            setattr(params, k, v)

        return params

    def optimize_structure(self, geoms=None, force_field_type='mmff', optimizer=None, maxIters=1000, **opts):

        if optimizer is None:
            ff_helpers = RDKitInterface.submodule("Chem.rdForceFieldHelpers")
            def optimizer(mol, **etc):
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
        return RDKitInterface.submodule('Chem.Draw.IPythonConsole').drawMol3D(
            self.mol.GetOwningMol(),
            confId=self.mol.GetId()
            # view=None, confId=-1, drawAs=None, bgColor=None, size=None
        )

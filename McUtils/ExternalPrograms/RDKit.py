

__all__ = [
    "RDMolecule"
]

import base64
import uuid

import numpy as np, io, os
from .. import Numputils as nput
from .. import Devutils as dev

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

    @classmethod
    def quiet_errors(cls):
        from rdkit.rdBase import BlockLogs
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
            conf_0 = rdmol.GetConformer(0)
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
            implicit_hydrogen_method = 'align' if num_confs is not None else 'builtin'
        if add_implicit_hydrogens and implicit_hydrogen_method == 'align':
            mol = Chem.AddHs(mol, explicitOnly=False)
            dm = nput.distance_matrix(coords)
            if confgen_opts is None:
                confgen_opts = {}
            if take_min is None:
                take_min = num_confs is None
            if num_confs is None:
                num_confs = 1

            conf_ids = cls.generate_conformers_for_mol(
                mol,
                distance_constraints={
                    (i, j): (dm[i, j]-distance_matrix_tol, dm[i, j]+distance_matrix_tol)
                    for i in range(len(coords))
                    for j in range(i + 1, len(coords))
                },
                num_confs=num_confs,
                optimize=optimize,
                take_min=take_min,
                force_field_type=force_field_type,
                **dict(opts, **confgen_opts)
            )
            if nput.is_int(conf_ids):
                try:
                    conf = mol.GetConformer(conf_ids)
                except ValueError:
                    import pprint
                    settings = pprint.pformat(dict(
                        distance_constraints={
                            (i, j): round(float(dm[i, j]), 3)
                            for i in range(len(coords))
                            for j in range(i + 1, len(coords))
                        },
                        num_confs=num_confs,
                        optimize=optimize,
                        take_min=take_min,
                        force_field_type=force_field_type,
                        **dict(opts, **confgen_opts)
                    ))
                    smi = Chem.MolToSmiles(mol, canonical=False)
                    raise ValueError(f"failed to build conformer {conf_ids} for {smi} with settings {settings}")
                coords2 = conf.GetPositions()
                coords3 = cls._align_new_conf_coords(mol, coords, coords2)
                print(coords[:5])
                print(coords3[:5])
                conf.SetPositions(coords3)
                return cls.from_rdmol(mol, conf_id=conf_ids, charge=charge, guess_bonds=guess_bonds,
                                      sanitize=sanitize)
            else:
                mols = []
                for i in conf_ids:
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
                    settings = pprint.pformat(dict(
                        distance_constraints={
                            (i, j): round(float(dm[i, j]), 3)
                            for i in range(len(coords))
                            for j in range(i + 1, len(coords))
                        },
                        num_confs=num_confs,
                        optimize=optimize,
                        take_min=take_min,
                        force_field_type=force_field_type,
                        **dict(opts, **confgen_opts)
                    ))
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

    @classmethod
    def generate_conformers_for_mol(cls, mol,
                                    *,
                                    num_confs=1,
                                    optimize=False,
                                    take_min=True,
                                    force_field_type='mmff',
                                    add_implicit_hydrogens=False,
                                    distance_constraints=None,
                                    **opts
                                    ):

        AllChem = cls.allchem_api()

        AllChem.AddHs(mol, explicitOnly=not add_implicit_hydrogens)

        params = cls.get_confgen_opts(**opts)
        if distance_constraints is not None:
            if hasattr(distance_constraints, 'items'):
                distance_constraints = distance_constraints.items()
            if nput.is_numeric_array_like(distance_constraints):
                bmat = np.array(distance_constraints)
            else:
                cls._prep_mol(mol)
                bmat = AllChem.GetMoleculeBoundsMatrix(mol)
                for (i, j), (min_dist, max_dist) in distance_constraints:
                    if j > i: i,j = j,i
                    if max_dist < min_dist: min_dist, max_dist = max_dist, min_dist
                    bmat[i, j] = min_dist
                    bmat[j, i] = max_dist
            params.SetBoundsMat(bmat)
        try:
            # with OutputRedirect():
            with cls.quiet_errors():
                conformer_set = AllChem.EmbedMultipleConfs(mol, numConfs=num_confs, params=params)
        except AllChem.rdchem.MolSanitizeException:
            conformer_set = None
            cls._prep_mol(mol)
        if conformer_set is None:
            params.embedFragmentsSeparately = False
            # with OutputRedirect():
            with cls.quiet_errors():
                conformer_set = AllChem.EmbedMultipleConfs(mol, numConfs=num_confs, params=params)
        if optimize:
            rdForceFieldHelpers = RDKitInterface.submodule("Chem.rdForceFieldHelpers")
            if force_field_type == 'mmff':
                rdForceFieldHelpers.MMFFOptimizeMoleculeConfs(mol)
            elif force_field_type == 'uff':
                rdForceFieldHelpers.UFFOptimizeMoleculeConfs(mol)
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
                    props = prop_gen(mol)
                else:
                    props = None

                engs = [
                    force_field_type(mol, props, confId=conf_id).CalcEnergy()
                    for conf_id in conf_ids
                ]

                conf_id = conf_ids[np.argmin(engs)]
            else:
                conf_id = 0
        else:
            conf_id = list(conformer_set)

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
    def _camel_case(o):
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
    def _drawer_png(cls, *, image_size, **opts):
        Chem = cls.chem_api()
        rdMolDraw2D = Chem.Draw.rdMolDraw2D
        # from rdkit.Chem.Draw import rdMolDraw2D
        drawer = rdMolDraw2D.MolDraw2DCairo(*image_size)
        return drawer, opts
    @classmethod
    def _drawer_svg(cls, *, image_size, **opts):
        Chem = cls.chem_api()
        rdMolDraw2D = Chem.Draw.rdMolDraw2D
        # from rdkit.Chem.Draw import rdMolDraw2D
        drawer = rdMolDraw2D.MolDraw2DSVG(*image_size)
        return drawer, opts

    @classmethod
    def _prep_draw_opts(cls, format, opts):
        return dict(
            dict(
                cls.drawing_defaults.get(None, {}),
                **cls.drawing_defaults.get(format, {})
            ),
            **opts
        )

    @classmethod
    def _draw_non_interactive(cls,
                              mol,
                              figure=None,
                              background=None,
                              format='svg',
                              drawer=None,
                              drawer_options=None,
                              **opts
                              ):
        Draw = RDKitInterface.submodule("Chem.Draw")
        rdMolDraw2D = Draw.rdMolDraw2D

        if drawer is None:
            if figure is not None:
                if hasattr(figure, 'figure'):
                    drawer = figure.figure
                else:
                    drawer = figure
            else:
                if drawer_options is None:
                    drawer_options = {}
                draw_opts = cls._prep_draw_opts(format, dict(opts, **drawer_options))
                if format == 'svg':
                    drawer, opts = cls._drawer_svg(**draw_opts)
                else:
                    drawer, opts = cls._drawer_png(**draw_opts)
        if background is not None:
            dops = drawer.drawOptions()
            dops.setBackgroundColour(background)
        opts = {
            cls._camel_case(k): v for k, v in opts.items()
            if v is not None
        }
        rdMolDraw2D.PrepareAndDrawMolecule(drawer, mol, **opts)
        return drawer

    def find_substructure(self, query):
        Chem = self.chem_api()
        query = Chem.MolFromSmarts(query)
        return self.rdmol.GetSubstructMatches(query)

    def draw(self,
             figure=None,
             background=None,
             remove_atom_numbers=False,
             remove_hydrogens=True,
             display_atom_numbers=False,
             format='svg',
             drawer=None,
             use_coords=False,
             atom_labels=None,
             highlight_atoms=None,
             highlight_bonds=None,
             highlight_atom_colors=None,
             highlight_bond_colors=None,
             conf_id=None,
             include_save_buttons=False,
             **draw_opts):
        from ..Plots import ColorPalette

        if drawer is None:
            drawer = self._draw_non_interactive

        Chem = self.allchem_api()
        mol = self.rdmol
        modified = False
        if remove_hydrogens:
            modified = True
            mol = Chem.RemoveHs(mol)
        if not use_coords:
            if not modified:
                mol = Chem.Mol(mol)
                modified = True
            Chem.Compute2DCoords(mol)
        if display_atom_numbers:
            if not modified:
                mol = Chem.Mol(mol)
                modified = True
            for atom in mol.GetAtoms():
                atom.SetAtomMapNum(atom.GetIdx()+1)
        elif remove_atom_numbers:
            if not modified:
                mol = Chem.Mol(mol)
                modified = True
            for atom in mol.GetAtoms():
                atom.SetAtomMapNum(0)
        if atom_labels is not None:
            if not modified:
                mol = Chem.Mol(mol)
                modified = True
            for atom,label in zip(mol.GetAtoms(), atom_labels):
                atom.SetProp("atomNote", label)

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

        if highlight_bond_colors is not None:
            _ = {}
            if highlight_atom_colors is not None:
                atom_colors = highlight_atom_colors
            else:
                atom_colors = {}
            for b in highlight_bonds:
                if b not in highlight_bond_colors:
                    if not nput.is_int(b):
                        i, j = b
                    else:
                        bb = mol.GetBondWithIdx(b)
                        i = bb.GetBeginAtomIdx()
                        j = bb.GetEndAtomIdx()
                    if (i,j) not in highlight_bond_colors and (j,i) not in highlight_bond_colors:
                        c1 = atom_colors.get(i)
                        c2 = atom_colors.get(j)
                        if c1 is None:
                            if c2 is None:
                                highlight_bond_colors[(i,j)] = (.5, .7, .5)
                            else:
                                highlight_bond_colors[(i,j)] = c2
                        elif c2 is None:
                            highlight_bond_colors[(i,j)] = c1
                        else:
                            if isinstance(c1, str):
                                if not isinstance(c2, str):
                                    c1 = ColorPalette.parse_color_string(c1)
                            elif isinstance(c2, str):
                                c2 = ColorPalette.parse_color_string(c2)
                            if  (
                                    (isinstance(c1, str) and isinstance(c2, str) and c1 == c2)
                                    or np.allclose(c1, c2)
                            ):
                                highlight_bond_colors[(i, j)] = c1
                            else:
                                highlight_bond_colors[(i,j)] = ColorPalette.prep_color(
                                    palette=[c1, c2],
                                    blending=.5,
                                    return_color_code=False
                                )

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
                if isinstance(c, str):
                    c = np.array(ColorPalette.parse_color_string(c)) / 255
                _[b] = tuple(c)
            highlight_bond_colors = _
        if highlight_atom_colors is not None:
            _ = {}
            for b, c in highlight_atom_colors.items():
                if isinstance(c, str):
                    c = np.array(ColorPalette.parse_color_string(c)) / 255
                _[b] = tuple(c)
            highlight_atom_colors = _

        if background is not None:
            if isinstance(background, str):
                background = np.array(ColorPalette.parse_color_string(background))
                background = tuple(background[:3]/255) + tuple(background[3:])

        if conf_id is None:
            conf_id = self.mol.GetId()
        figure = drawer(mol,
                        figure=figure,
                        background=background,
                        format=format,
                        highlight_atoms=highlight_atoms,
                        highlight_bonds=highlight_bonds,
                        highlight_atom_colors=highlight_atom_colors,
                        highlight_bond_colors=highlight_bond_colors,
                        conf_id=conf_id,
                        **draw_opts)
        return self.DisplayImage(figure, format, include_save_buttons=include_save_buttons)

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
            # float_type = np.float16
            if pack_angles:
                pack_type = np.uint8
            else:
                pack_type = np.uint16
        elif byte_size == 32:
            base_type = np.uint32
            # float_type = np.float32
            if pack_angles:
                pack_type = np.uint16
            else:
                pack_type = np.uint32
        elif byte_size == 64:
            base_type = np.uint64
            # float_type = np.float64
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
        packaged_dists[~compressed] = dists[~compressed].view(base_type) + step_max

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
        atoms = [a.GetSymbol() for a in mol.GetAtoms()]
        bonds = [
            [b.GetBeginAtomIdx(), b.GetEndAtomIdx()]
            for b in mol.GetBonds()
        ]
        return Graphs.EdgeGraph(atoms, bonds)
    def get_edge_graph(self, mol=None):
        from .. import Graphs
        if mol is None:
            atoms, bonds = self.atoms, [b[:2] for b in self.bonds]
            return Graphs.EdgeGraph(atoms, bonds)
        else:
            return self.get_mol_edge_graph(mol)

    class DisplayImage:
        def __init__(self, figure, format, include_save_buttons=False, id=None):
            self.figure = figure
            self.fmt = format
            if id is None:
                id = "rdkit-" + str(uuid.uuid4())[:6]
            self.id = id
            self._text = None
            self.include_save_buttons = include_save_buttons

        @property
        def text(self):
            if self._text is None:
                self.figure.FinishDrawing()
                self._text = self.figure.GetDrawingText()
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
                print(mol)
                print(self.rdmol)
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

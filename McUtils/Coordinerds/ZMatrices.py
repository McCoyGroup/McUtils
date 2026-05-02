import collections

import numpy as np
import scipy.sparse as spg
import itertools
from .. import Numputils as nput
from .. import Iterators as itut
from ..Graphs import EdgeGraph

from .Internals import canonicalize_internal

__all__ = [
    "zmatrix_unit_convert",
    "zmatrix_indices",
    "num_zmatrix_coords",
    "zmatrix_embedding_coords",
    "set_zmatrix_embedding",
    "enumerate_zmatrices",
    "extract_zmatrix_internals",
    "extract_zmatrix_values",
    "zmatrix_from_values",
    "parse_zmatrix_string",
    "format_zmatrix_string",
    "validate_zmatrix",
    "chain_zmatrix",
    "center_bound_zmatrix",
    "spoke_zmatrix",
    # "methyl_zmatrix",
    # "ethyl_zmatrix",
    "attached_zmatrix_fragment",
    "functionalized_zmatrix",
    "add_missing_zmatrix_bonds",
    "bond_graph_zmatrix",
    "canonical_fragment_zmatrix",
    "reindex_zmatrix",
    "sort_complex_attachment_points",
    "complex_zmatrix",
    "graph_backbone_zmatrix",
    "segmented_complex_backbone_zmatrix"
]


def zmatrix_unit_convert(zmat, distance_conversion, angle_conversion=None, rad2deg=False, deg2rad=False):
    zm2 = np.asanyarray(zmat)
    if zm2 is zmat: zm2 = zm2.copy()

    zm2[..., :, 0] *= distance_conversion
    if angle_conversion is None:
        if deg2rad:
            zm2[..., :, 1] = np.deg2rad(zm2[..., :, 1])
            zm2[..., :, 2] = np.deg2rad(zm2[..., :, 2])
        elif rad2deg:
            zm2[..., :, 1] = np.rad2deg(zm2[..., :, 1])
            zm2[..., :, 2] = np.rad2deg(zm2[..., :, 2])
    else:
        zm2[..., :, 1] *= angle_conversion
        zm2[..., :, 2] *= angle_conversion

    return zm2

def zmatrix_indices(zmat, coords, strip_embedding=True):
    base_coords = [canonicalize_internal(c) for c in extract_zmatrix_internals(zmat, strip_embedding=strip_embedding)]
    return [
        base_coords.index(canonicalize_internal(c))
        for c in coords
    ]

emb_pos_map = [
    (0,1),
    (0,2),
    (0,3),
    None,
    (1,2),
    (1,3),
    None,
    None,
    (2,3)
]
emb_partial_pos_map = [
    None,
    (0,2),
    (0,3),
    None,
    None,
    (1,3)
]
def zmatrix_embedding_coords(zmat_or_num_atoms, partial_embedding=False, array_inds=False):
    if array_inds:
        if not nput.is_int(zmat_or_num_atoms):
            dim_shift = (1 if len(zmat_or_num_atoms[0]) == 3 else 0)
        else:
            dim_shift = 0
        base_inds = zmatrix_embedding_coords(zmat_or_num_atoms, array_inds=False, partial_embedding=partial_embedding)
        if partial_embedding:
            map = emb_partial_pos_map
        else:
            map = emb_pos_map
        return [(map[n][0], map[n][1]-dim_shift) for n in base_inds]
    else:
        if not nput.is_int(zmat_or_num_atoms):
            zmat_or_num_atoms = len(zmat_or_num_atoms) + (1 if len(zmat_or_num_atoms[0]) == 3 else 0)
        n: int = zmat_or_num_atoms

        if partial_embedding:
            if n < 1:
                return []
            elif n == 1:
                return [1, 2]
            else:
                return [1, 2, 5]
        else:
            if n < 1:
                return []
            elif n == 1:
                return [0, 1, 2]
            elif n == 2:
                return [0, 1, 2, 4, 5]
            else:
                return [0, 1, 2, 4, 5, 8]

def num_zmatrix_coords(zmat_or_num_atoms, strip_embedding=True):
    if not nput.is_int(zmat_or_num_atoms):
        zmat_or_num_atoms = len(zmat_or_num_atoms) + (1 if len(zmat_or_num_atoms[0]) == 3 else 0)
    n: int = zmat_or_num_atoms

    return (n*3) - (
        0
            if not strip_embedding else
        len(zmatrix_embedding_coords(n))
    )

def _zmatrix_iterate(coords, natoms=None,
                     include_origins=False,
                     canonicalize=True,
                     deduplicate=True,
                     allow_completions=False
                     ):
    # TODO: this fixes an atom ordering, to change that up we'd need to permute the initial coords...
    if canonicalize:
        coords = [tuple(reversed(canonicalize_internal(s))) for s in coords]

    if deduplicate:
        dupes = set()
        _ = []
        for c in coords:
            if c in dupes: continue
            _.append(c)
            dupes.add(c)
        coords = _

    if include_origins:
        if (1, 0) not in coords:
            coords = [(1, 0)] + coords
        if (2, 1) not in coords and (2, 0) not in coords:
            if (2, 1, 0) in coords:
                coords = [(2, 1)] + coords
            else:
                coords = [(2, 0)] + coords
        if (2, 0) in coords and (2, 0, 1) not in coords: # can this happen?
            coords.append((2,1,0))

    if natoms is None:
        all_atoms = {i for s in coords for i in s}
        natoms = len(all_atoms)

    dihedrals = [k for k in coords if len(k) == 4]
    all_dihedrals = [
        (i, j, k, l)
        for (i, j, k, l) in dihedrals
        if i > j and i > k and i > l
    ]

    # need to iterate over all N-2 choices of dihedrals (in principle)...
    # should first reduce over consistent sets
    if not allow_completions:
        dihedrals = [
            (i,j,k,l) for i,j,k,l in dihedrals
            if (i,j) in coords and (i,j,k) in coords
            # if (
            #         any(x in coords or tuple(reversed(x)) in coords for x in [(i,j), (l,k)])
            #         and any(x in coords or tuple(reversed(x)) in coords for x in [(i,j,k), (l,k,j)])
            # )
        ]

    embedding = [
        x for x in [(2, 0, 1), (2, 1, 0)]
        if x in coords
    ]

    # we also will want to sample from dihedrals that provide individual atoms
    atom_diheds = [[] for _ in range(natoms)]
    for n,(i,j,k,l) in enumerate(dihedrals):
        atom_diheds[i].append((i,j,k,l))

    # completions = []
    # if allow_completions:
    #     for d in all_dihedrals:
    #         if d in dihedrals: continue
    #         completions.extend([d[:2], d[:3]])
    #
    #     c_set = set()
    #     for d in dihedrals:
    #         c_set.add(d[:2])
    #         c_set.add(d[:3])
    #     coord_pairs = [
    #         (c[:2],c[:3])
    #         for
    #     ]
    #     for d in all_dihedrals:
    #         if d in dihedrals: continue
    #         completions.extend([d[:2], d[:3]])

    for dihed_choice in itertools.product(embedding, *atom_diheds[3:]):
        emb, dis = dihed_choice[0], dihed_choice[1:]
        yield (
            (0, -1, -1, -1),
            (1, 0, -1, -1),
            emb + (-1,)
        ) + dis

def enumerate_zmatrices(coords, natoms=None,
                        allow_permutation=True,
                        include_origins=False,
                        canonicalize=True,
                        deduplicate=True,
                        preorder_atoms=True,
                        allow_completions=False
                        ):
    if canonicalize:
        coords = [tuple(reversed(canonicalize_internal(s))) for s in coords]

    if deduplicate:
        dupes = set()
        _ = []
        for c in coords:
            if c in dupes: continue
            _.append(c)
            dupes.add(c)
        coords = _

    if natoms is None:
        all_atoms = {i for s in coords for i in s}
        natoms = len(all_atoms)

    if preorder_atoms:
        counts = itut.counts(itertools.chain(*coords))
        max_order = list(sorted(range(natoms), key=lambda k:-counts[k]))
    else:
        max_order = np.arange(natoms)

    for atoms in (
            itertools.permutations(max_order)
                if allow_permutation else
            [max_order]
    ):
        atom_perm = np.argsort(atoms)
        perm_coords = [
            tuple(reversed(canonicalize_internal([atom_perm[c] for c in crd])))
            for crd in coords
        ]
        for zm in _zmatrix_iterate(perm_coords,
                                   natoms=natoms,
                                   include_origins=include_origins,
                                   canonicalize=False,
                                   deduplicate=False,
                                   allow_completions=allow_completions
                                   ):
            yield [
                [atoms[c] if c >= 0 else c for c in z]
                for z in zm
            ]

def extract_zmatrix_internals(zmat, strip_embedding=True, canonicalize=True):
    specs = []
    if len(zmat[0]) == 3:
        return extract_zmatrix_internals(
            [[0, -1, -1, -1]]
            + [
                [i + 1] + list(z)
                for i, z in enumerate(zmat)
            ],
            strip_embedding=strip_embedding,
            canonicalize=canonicalize
        )
        # zmat = np.asanyarray(zmat)
        # return np.delete(zmat.flatten(), zmatrix_embedding_coords(len(zmat)))
    else:
        for n,row in enumerate(zmat):
            if strip_embedding and n == 0: continue
            if canonicalize:
                coord = canonicalize_internal(row[:2])
            else:
                coord = tuple(row[:2])
            specs.append(coord)
            if strip_embedding and n == 1: continue
            if canonicalize:
                coord = canonicalize_internal(row[:3])
            else:
                coord = tuple(row[:3])
            specs.append(coord)
            if strip_embedding and n == 2: continue
            if canonicalize:
                coord = canonicalize_internal(row[:4])
            else:
                coord = tuple(row[:4])
            specs.append(coord)
    return specs

def extract_zmatrix_values(zmat, inds=None, partial_embedding=False, strip_embedding=True):
    zmat = np.asanyarray(zmat)
    if zmat.shape[-1] == 4:
        zmat = zmat[1:, 1:]
    if inds is None:
        n = zmat.shape[-1]*zmat.shape[-2]
        inds = np.arange(n)
        if strip_embedding:
            inds = np.delete(inds, zmatrix_embedding_coords(zmat, partial_embedding=partial_embedding))
    elif strip_embedding:
        real_coords = np.delete(
            np.arange(zmat.shape[-1]*zmat.shape[-2]),
            zmatrix_embedding_coords(zmat)
        )
        inds = real_coords[inds,]
    flat_mat = np.reshape(zmat, zmat.shape[:-2] + (zmat.shape[-1]*zmat.shape[-2],))
    return flat_mat[..., inds]
def zmatrix_from_values(flat_z, strip_embedding=True, partial_embedding=False):
    flat_z = np.asanyarray(flat_z)
    base_shape = flat_z.shape[:-1]
    if not strip_embedding:
        return np.asanyarray(flat_z).reshape(base_shape + (-1, 3))
    elif partial_embedding:
        nats = (flat_z.shape[-1] + 3) // 3
        zcoords = np.zeros(base_shape + (nats, 3))
        zcoords[..., 0, 0] = flat_z[..., 0]
        if nats > 1:
            zcoords[..., 1, :2] = flat_z[..., 1:3]
        if nats > 2:
            zcoords[..., 2:, :] = flat_z[..., 3:].reshape(base_shape + (-1, 3))
        return zcoords
    else:
        nats = (flat_z.shape[-1] + 6) // 3
        zcoords = np.zeros(base_shape +  (nats, 3))
        zcoords[..., 1, 0] = flat_z[..., 0]
        if nats > 1:
            zcoords[..., 2, :2] = flat_z[..., 1:3]
        if nats > 2:
            zcoords[..., 3:, :] = flat_z[..., 3:].reshape(-1, 3)
        return zcoords

scan_spec = collections.namedtuple('scan_spec', ['value', 'steps', 'amount'])
def _prep_var_spec(v):
    if len(v) == 1:
        return float(v[0])
    elif len(v) == 2 and v[1] in {'f', 'F'}:
        return scan_spec(float(v[0]), -1, 0)
    elif len(v) == 3:
        return scan_spec(float(v[0]), int(v[1]), float(v[2]))
    else:
        raise ValueError(f"can't parse var spec {v}")
def parse_zmatrix_string(zmat, units="Angstroms", in_radians=False,
                         has_values=True,
                         atoms_are_order=False,
                         keep_variables=False,
                         variables=None,
                         dialect='gaussian'):
    from ..Data import AtomData, UnitsData
    # we have to reparse the Gaussian Z-matrix...

    possible_atoms = {d["Symbol"][:2] for d in AtomData.data.values()}

    atoms = []
    ordering = []
    coords = []
    # vars = {}

    if "Variables:" in zmat:
        zmat, vars_block = zmat.split("Variables:", 1)
    else:
        zmat = zmat.split("\n\n", 1)
        if len(zmat) == 1:
            zmat = zmat[0]
            vars_block = ""
        else:
            zmat, vars_block = zmat
    bits = [b.strip() for b in zmat.split() if len(b.strip()) > 0]

    coord = []
    ord = []
    complete = False
    last_complete = -1
    last_idx = len(bits) - 1
    for i, b in enumerate(bits):
        d = (i - last_complete) - 1
        if has_values:
            m = d % 2
            if d == 0:
                atoms.append(b)
            elif m == 1:
                b = int(b)
                if b > 0: b = b - 1
                ord.append(b)
            elif m == 0:
                coord.append(b)

            terminal = (
                    i == last_idx
                    or i in {0, 3, 8}
                    or (i > 8 and (i - 9) % 7 == 6)
            )
        else:
            if d == 0:
                atoms.append(b)
            else:
                b = int(b)
                if b > 0: b = b - 1
                ord.append(b)

            terminal = (
                    i == last_idx
                    or i in {0, 2, 5}
                    or (i > 5 and d == 3)
            )


        # atom_q = bits[i + 1][:2] in possible_atoms
        if terminal:
            last_complete = i
            ord = [len(ordering)] + ord + [-1] * (3 - len(ord))
            coord = coord + [0] * (3 - len(coord))
            ordering.append(ord)
            coords.append(coord)
            ord = []
            coord = []

    if atoms_are_order:
        atom_ord = np.array(atoms).astype(int) - 1
        ordering = np.asanyarray(ordering)
        ordering[:, 0] = atom_ord
        atoms = None


    split_vars = [
        vb.strip().replace("=", " ").split()
        for vb in vars_block.split("\n")
    ]
    # split_pairs = [s for s in split_pairs if len(s) == 2]

    if dialect != "gaussian":
        raise NotImplementedError(f"unsupported z-matrix dialect '{dialect}'")
    vars = {
        v[0]:_prep_var_spec(v[1:])
        for v in split_vars
        if len(v) > 0
    }
    if variables is not None:
        vars.update(variables)

    # ordering = [
    #     [i] + o
    #     for i, o in enumerate(ordering)
    # ]

    if not keep_variables:
        vals = {
            k:(
                v.value
                    if not nput.is_numeric(v) else
                v
            )
            for k, v in vars.items()
        }
        coords = [
            [
                vals[x] if x in vals else float(x)
                for x in c
            ]
            for c in coords
        ]

        # convert book angles into sensible dihedrals...
        # actually...I think I don't need to do anything for this?
        ordering = np.array(ordering)[:, :4]

        coords = np.array(coords)
        coords[:, 0] *= UnitsData.convert(units, "BohrRadius")
        coords[:, 1] = coords[:, 1] if in_radians else np.deg2rad(coords[:, 1])
        coords[:, 2] = coords[:, 2] if in_radians else np.deg2rad(coords[:, 2])
        return (atoms, ordering, coords)
    else:
        return (atoms, ordering, coords), vars

def format_zmatrix_string(atoms, zmat, ordering=None, units="Angstroms",
                          in_radians=False,
                          float_fmt="{:11.8f}",
                          index_padding=1,
                          variables=None,
                          variable_modifications=None,
                          distance_variable_format="r{i}",
                          angle_variable_format="a{i}",
                          dihedral_variable_format="d{i}"
                          ):
    from ..Data import UnitsData
    if ordering is None:
        if len(zmat) == len(atoms):
            zmat = zmat[1:]
        ordering = [
            [z[0], z[2], z[4]]
            if i > 1 else
            [z[0], z[2], -1]
            if i > 0 else
            [z[0], -1, -1]
            for i, z in enumerate(zmat)
        ]
        zmat = [
            [z[1], z[3], z[5]]
            if i > 1 else
            [z[1], z[3], -1]
            if i > 0 else
            [z[1], -1, -1]
            for i, z in enumerate(zmat)
        ]

    if isinstance(zmat, np.ndarray):
        zmat = zmat.copy()
        zmat[:, 0] *= UnitsData.convert("BohrRadius", units)
        zmat[:, 1] = zmat[:, 1] if in_radians else np.rad2deg(zmat[:, 1])
        zmat[:, 2] = zmat[:, 2] if in_radians else np.rad2deg(zmat[:, 2])
        zmat = zmat.tolist()
    else:
        cr = UnitsData.convert("BohrRadius", units)
        zmat = [
            [
                r * cr if nput.is_numeric(r) else r,
                np.rad2deg(a) if not in_radians and nput.is_numeric(a) else a,
                np.rad2deg(d) if not in_radians and nput.is_numeric(d) else d
            ]
            for r, a, d in zmat
        ]

    if variables is True:
        variables = {}
        _ = []
        for i,(r,a,d) in enumerate(zmat):
            s = []
            if i > 0:
                vr = distance_variable_format.format(i=i)
                variables[vr] = r
                s.append(vr)
            else:
                s.append("")
            if i > 1:
                va = angle_variable_format.format(i=i)
                variables[va] = a
                s.append(va)
            else:
                s.append("")
            if i > 2:
                vd = dihedral_variable_format.format(i=i)
                variables[vd] = d
                s.append(vd)
            else:
                s.append("")
            _.append(s)
        zmat = _

    includes_atom_list = len(ordering[0]) == 4
    if not includes_atom_list:
        if len(ordering) < len(atoms):
            ordering = [[-1, -1, -1, -1]] + list(ordering)
        if len(zmat) < len(atoms):
            zmat = [[-1, -1, -1]] + list(zmat)

    if variable_modifications is not None:
        if variables is None:
            variables = {}
        includes_atom_list = len(ordering[0]) == 4
        for i,(x,r,a,d) in enumerate(ordering):
            for k,fmt,j in [
                [(x, r), distance_variable_format, 0],
                [(r, x), distance_variable_format, 0],
                [(x, r, a), angle_variable_format, 1],
                [(a, r, x), angle_variable_format, 1],
                [(x, r, a, d), dihedral_variable_format, 2],
                [(d, a, r, x), dihedral_variable_format, 2],
            ]:
                if k in variable_modifications:
                    vr = fmt.format(i=i)
                    val = variables.get(vr, zmat[i][j])
                    if not isinstance(val, str):
                        val = float_fmt.format(val)
                    variables[vr] = val + " " + variable_modifications[k]
                    zmat[i][j] = vr
                    break

    zmat = [
        ["", "", ""]
        if i == 0 else
        [z[0], "", ""]
        if i == 1 else
        [z[0], z[1], ""]
        if i == 2 else
        [z[0], z[1], z[2]]
        for i, z in enumerate(zmat)
    ]
    zmat = [
        [
            float_fmt.format(x)
                if not isinstance(x, str) else
            x
            for x in zz
        ]
        for zz in zmat
    ]
    if includes_atom_list:
        ord_list = [o[0] for o in ordering]
        atom_order = np.argsort(ord_list)
        atoms = [atoms[o] for o in ord_list]
        ordering = [
            ["", "", ""]
              if i == 0 else
            [atom_order[z[1]], "", ""]
              if i == 1 else
            [atom_order[z[1]], atom_order[z[2]], ""]
              if i == 2 else
            [atom_order[z[1]], atom_order[z[2]], atom_order[z[3]]]
              for i, z in enumerate(ordering)
        ]
    else:
        ordering = [
            ["", "", ""]
            if i == 0 else
                [z[0], "", ""]
            if i == 1 else
                [z[0], z[1], ""]
            if i == 2 else
                [z[0], z[1], z[2]]
            for i, z in enumerate(ordering)
        ]
    ordering = [
        ["{:.0f}".format(x + index_padding) if not isinstance(x, str) else x for x in zz]
        for zz in ordering
    ]

    max_at_len = max(len(a) for a in atoms)

    nls = [
        max([len(xyz[i]) for xyz in ordering])
        for i in range(3)
    ]
    zls = [
        max([len(xyz[i]) for xyz in zmat])
        for i in range(3)
    ]

    fmt_string = f"{{a:<{max_at_len}}} {{n[0]:>{nls[0]}}} {{r[0]:>{zls[0]}}} {{n[1]:>{nls[1]}}} {{r[1]:>{zls[1]}}} {{n[2]:>{nls[2]}}} {{r[2]:>{zls[2]}}}"
    zm = "\n".join(
        fmt_string.format(
            a=a,
            n=n,
            r=r
        )
        for a, n, r in zip(atoms, ordering, zmat)
    )
    if variables is not None:
        max_symbol_len = max(len(s.split()[0]) for s in variables)
        variables = {
            k: v if isinstance(v, str) else float_fmt.format(v)
            for k, v in variables.items()
        }
        max_v_len = max(len(s) for s in variables.values())
        variables_fmt = f" {{:<{max_symbol_len}}} = {{:>{max_v_len}}}"
        variables_block = "\n".join(
            variables_fmt.format(k, v if isinstance(v, str) else float_fmt.format(v))
            for k,v in variables.items()
        )
        zm = zm + "\nVariables:\n" + variables_block

    return zm


def validate_zmatrix(ordering,
                     allow_reordering=True,
                     ensure_nonnegative=True,
                     raise_exception=False,
                     return_reason=False
                     ):
    ordering = set_zmatrix_embedding(ordering)
    proxy_order = np.array([o[0] for o in ordering])
    all_rem = np.setdiff1d(np.unique(ordering), proxy_order)
    all_rem = all_rem[all_rem >= 0]
    if len(all_rem) > 0:
        reason = f"Z-matrix contains indices {all_rem} not defined in the atom list {proxy_order}"
        if raise_exception:
            raise ValueError(reason)
        if return_reason:
            return False, reason
        else:
            return False
    if allow_reordering:
        reindexing = dict(zip(proxy_order, np.arange(len(proxy_order))))
        if ensure_nonnegative and np.min(proxy_order) < 0:
            reason = f"atom indices not all nonnegative {proxy_order}"
            if raise_exception:
                raise ValueError(reason)
            if return_reason:
                return False, reason
            else:
                return False
        new_order = [
            [reindexing[i] if i >= 0 else i for i in row]
            for row in ordering
        ]
        return validate_zmatrix(new_order,
                                allow_reordering=False,
                                raise_exception=raise_exception,
                                return_reason=return_reason
                                )
    if ensure_nonnegative and proxy_order[0] < 0:
        reason = f"atom indices not all nonnegative {proxy_order}"
        if raise_exception:
            raise ValueError(reason)
        if return_reason:
            return False, reason
        else:
            return False

    for n,row in enumerate(ordering):
        if (
                any(i > n for i in row)
                or any(i > row[0] for i in row[1:])
                or len(set(row)) < len(row)
                or (
                    ensure_nonnegative and (
                        (n > 3 and any(i < 0 for i in row[1:]))
                        or (n > 2 and any(i < 0 for i in row[1:2]))
                        or (n > 1 and any(i < 0 for i in row[1:3]))
                    )
                )
        ):
            reason = f"Z-matrix line {n} invalid: {row}"
            if raise_exception:
                raise ValueError(reason)
            if return_reason:
                return False, reason
            else:
                return False

    if return_reason:
        return True, None
    else:
        return True

def chain_zmatrix(n):
    if isinstance(n, int):
        return [
            list(range(i, i-4, -1))
            for i in range(n)
        ]
    else:
        return [
            [n[i], n[i-1] if i > 0 else i - 1, n[i-2] if i > 1 else i - 2, n[i-3] if i > 2 else i - 3]
            for i in range(len(n))
        ]

def center_bound_zmatrix(n, center=-1):
    return [
        [
            i,
            center,
            (
                (i - 2)
                if i > 1 else
                0
                if i == 1 else
                -2
            ),
            (
                (i - 1)
                if i > 1 else
                -3 + i
            ),
        ]
        for i in range(n)
    ]

def attached_zmatrix_fragment(n, zm, fragment, attachment_points):
    _ = []
    order = [f[0] for f in zm]
    main_ref = None
    for a in attachment_points:
        if a < 0:
            if main_ref is None:
                if len(order) >= (-a):
                    a = order[a]
                    for m,z in enumerate(zm):
                        if z[0] == a:
                            _ = []
                            for zz in z:
                                if zz < 0:
                                    clip_i = max([m + zz, 0])
                                    if order[clip_i] not in _:
                                        zz = order[clip_i]
                                    if zz < 0:
                                        clip_i = (m - zz) % len(order)
                                        for j in range(clip_i, len(order)):
                                            if order[j] not in _:
                                                zz = order[j]
                                                break
                                        # else:
                                        #     raise ValueError(f"couldn't get attachment point for {attachment_points} in {zm}")
                                _.append(zz)
                            main_ref = _
                            break
            else:
                a = main_ref[(-a) - 1]
        elif main_ref is None:
            for m,z in enumerate(zm):
                if z[0] == a:
                    _ = []
                    for zz in z:
                        if zz < 0:
                            clip_i = max([m + zz, 0])
                            if order[clip_i] not in _:
                                zz = order[clip_i]
                            if zz < 0:
                                clip_i = (m - zz) % len(order)
                                for j in range(clip_i, len(order)):
                                    if order[j] not in _:
                                        zz = order[j]
                                        break
                                # else:
                                #     raise ValueError(f"couldn't get attachment point for {attachment_points} in {zm}")
                        _.append(zz)
                    main_ref = _
                    break
        _.append(a)
    attachment_points = _
    return [
        [attachment_points[-r-1] if r < 0 else n+r for r in row]
        for row in fragment
    ]

def set_zmatrix_embedding(zmat, embedding=None, partial_embedding=False):
    zmat = np.array(zmat)
    if embedding is None:
        if partial_embedding:
            embedding = [-1, -2, -1]
        else:
            embedding = [-1, -2, -3, -1, -2, -1]
    emb_pos = zmatrix_embedding_coords(zmat, array_inds=True, partial_embedding=partial_embedding)
    for (i,j),v in zip(emb_pos, embedding):
        zmat[..., i,j] = v
    return zmat

# ethyl_zmatrix = [
#     [0, -1, -2, -3],
#     [1,  0, -1, -2],
#     [2,  0,  1, -1]
# ]
#
# methyl_zmatrix = [
#     [0, -1, -2, -3],
#     [1,  0, -1, -2],
#     [2,  0,  1, -1],
#     [3,  0,  2,  1]
# ]


def functionalized_zmatrix(
        base_zm,
        attachments:'dict|list[list[int], list[int]]'=None,
        single_atoms:list[int]=None, # individual components, embedding doesn't matter
        methyl_positions:list[int]=None, # all bonds attached to central atom, angles relative to eachother
        ethyl_positions:list[int]=None, # all bonds attached to central atom, angles relative to eachother
        validate=False
):
    if nput.is_numeric(base_zm):
        zm = chain_zmatrix(base_zm)
    else:
        zm = [
            list(x) for x in base_zm
        ]
    if attachments is None:
        attachments = {}
    if hasattr(attachments, 'items'):
        attachments = attachments.items()
    for attachment_points, fragment in attachments:
        if nput.is_numeric(fragment):
            fragment = chain_zmatrix(fragment)
        prev_atoms = [z[0] for z in zm]
        bad_attach = [
            b for b in attachment_points
            if b not in prev_atoms and b > 0 and b < len(prev_atoms)
        ]
        if len(bad_attach) > 0:
            raise ValueError(f"error attaching at {attachment_points} with previous atoms {prev_atoms}")
        zm = zm + attached_zmatrix_fragment(
            len(zm),
            zm,
            fragment,
            attachment_points
        )
        if validate:
            is_valid, reason = validate_zmatrix(zm, return_reason=True)
            if not is_valid:
                raise ValueError(f"attached zmatrix invalid after adding to {attachment_points} with {fragment} ({reason}) in {zm}")
    if single_atoms is not None:
        #TODO: make this bond graph relevant
        for atom in single_atoms:
            key = [z for z in zm if z[0] == atom]
            bonds = [z[0] for z in zm if z[1] == atom]
            if len(key) > 0:
                key = key[0]
                # worth speeding this up I think...
                adj_bonds = [
                    z[0] for z in zm
                    if (
                            z[0] != atom
                            and z[0] not in bonds
                            and z[0] not in key
                            and (z[1] in bonds or z[1] in key)
                    )
                ]
                # remz = np.setdiff1d([z[0] for z in zm], list(key) + bonds + adj_bonds)
                key = [
                    bonds[-(k+1)]
                        if k < 0 and abs(k) <= len(bonds) else
                    adj_bonds[0] # we only have four positions to try, gotta terminate here I think...
                        if k < 0 and len(adj_bonds) > 0 else
                    # remz[0]
                    #     if k < 0 and len(remz) > 0 else
                    k
                    for k in key[:-1]
                ]
                zm = zm + [
                    [len(zm)] + key
                ]
            else:
                zm = zm + attached_zmatrix_fragment(
                    len(zm),
                    zm,
                    [[0, -1, -2, -3]],
                    [
                        (
                            (
                                (atom - i)
                                    if atom - i < len(zm) else
                                i + len(zm) - 1
                            ) if i < 0 else
                            i
                        )
                        for i in range(atom, atom - 4, -1)
                    ]
                )
    if methyl_positions is not None:
        for atom in methyl_positions:
            zm = zm + attached_zmatrix_fragment(
                len(zm),
                zm,
                [
                    [0, -1, -2, -3],
                    [1, -1,  0, -2],
                    [2, -1,  0,  1],
                ],
                [
                    (
                        (
                            (atom - i)
                                if atom - i < len(zm) else
                            i + len(zm) - 1
                        ) if i < 0 else
                        i
                    )
                    for i in range(atom, atom - 4, -1)
                ]
            )
    if ethyl_positions is not None:
        for atom in ethyl_positions:
            zm = zm + attached_zmatrix_fragment(
                len(zm),
                zm,
                [
                    [0, -1, -2, -3],
                    [1, -1,  0, -2]
                ],
                [
                    (
                        (
                            (atom - i)
                                if atom - i < len(zm) else
                            i + len(zm) - 1
                        ) if i < 0 else
                        i
                    )
                    for i in range(atom, atom - 4, -1)
                ]
            )
    return zm


def spoke_zmatrix(m, spoke=1, root=1):
    if nput.is_int(spoke):
        spoke = chain_zmatrix(spoke)

    if nput.is_int(root):
        root = chain_zmatrix(root)

    nroot = len(root) - 1
    if len(root) < 3:
        nrem = (3 - len(root))
        # no need for any moduli or floors, we just know
        if len(spoke) == 1:
            nspoke = nrem
        else:
            nspoke = 1

        for i in range(nspoke):
            if len(root) > 1:
                mroot = nroot + 1
            else:
                mroot = -1

            if len(root) > 2:
                proot = nroot + 2
            elif len(root) > 1:
                proot = nroot - 1
            else:
                proot = nroot - 2
            root = functionalized_zmatrix(
                root,
                [
                    [_attachment_point([
                        nroot,
                        mroot,
                        proot
                    ]), spoke]
                ]
            )
        if nspoke == 1:
            if nrem == 1:
                a = nroot - 1
                b = nroot + 1
            else:
                a = nroot + 1
                b = nroot + 2
        else:
            a = nroot + 1
            b = nroot + 2
        m = m - nspoke
    else:
        a = nroot - 1
        b = nroot - 2



    return functionalized_zmatrix(
        root,
        [
            [_attachment_point([nroot, a, b]), spoke]
            for _ in range(m)
        ]
    )


def reindex_zmatrix(zm, perm):
    return [
        [perm[r] if r >= 0 else r for r in row]
        for row in zm
    ]

def canonicalize_zmatrix(zm):
    if len(zm[0]) == 3:
        zm = [
            [0, -1, -2, -3]
        ] + [
            [i+1] + z
            for i,z in enumerate(zm)
        ]

    z_vec = np.array([z[0] for z in zm])
    perm = {z:i for i,z in enumerate(z_vec)}
    return z_vec, reindex_zmatrix(zm, perm)

def _attachment_point(i_pos, graph=None, ind_mapping=None):
    r = None
    a = None
    d = None
    graph_mapped = [False, False, False]
    if nput.is_int(i_pos):
        i_pos = [i_pos]

    if len(i_pos) > 0:
        r = i_pos[0]
    if len(i_pos) > 1:
        a = i_pos[1]
    if len(i_pos) > 2:
        d = i_pos[2]

    if r is None:
        if a is not None:
            if d is not None:
                if graph is not None:
                    neighbors = np.setdiff1d(list(graph.map.get(a, [])), [d])
                    if len(neighbors) > 0:
                        r = neighbors[0]
                        graph_mapped[0] = True
                if r is None:
                    if a > 0:
                        r = a - 1
                        if r == d: r = a + 1
                    else:
                        r = a + 1
                        if r == d: r = a + 2
            else:
                if graph is not None:
                    neighbors = list(graph.map.get(a, []))
                    if len(neighbors) > 0:
                        r = neighbors[0]
                        graph_mapped[0] = True
                if r is None:
                   r = (a - 1) if a > 0 else (a + 1)
        elif d is not None:
            if graph is not None:
                neighbors = list(graph.map.get(d, []))
                if len(neighbors) > 0:
                    r = neighbors[0]
                    graph_mapped[0] = True
            if r is None:
                if d > 1:
                    r = d - 2
                elif d > 0:
                    r = d - 1
                else:
                    r = d + 1
        else:
            r = 0
    if a is None:
        if graph is not None:
            neighbors = list(graph.map.get(r, []))
            if d is not None:
                neighbors = np.setdiff1d(neighbors, [d])
                if len(neighbors) == 0:
                    neighbors = list(graph.map.get(d, []))
                    if r is not None:
                        neighbors = np.setdiff1d(neighbors, [r])
            if len(neighbors) > 0:
                a = neighbors[0]
                graph_mapped[1] = True
        if a is None:
            if r > 0:
                a = r - 1
                if d is not None and a == d:
                    if r > 1:
                        a = r - 2
                    else:
                        a = r + 1
            else:
                a = r + 1
                if d is not None and a == d:
                    a = r + 2
    if d is None:
        if graph is not None:
            neighbors = list(graph.map.get(r, []))
            if a is not None:
                neighbors = np.setdiff1d(neighbors, [a])
                if len(neighbors) == 0:
                    neighbors = list(graph.map.get(a, []))
                    if r is not None:
                        neighbors = np.setdiff1d(neighbors, [r])
            if len(neighbors) > 0:
                d = neighbors[0]
                graph_mapped[2] = True
        if d is None:
            if r > 1:
                d = r - 2
                if a is not None and a == d:
                    d = r - 1
            elif r > 0:
                d = r - 1
                if a is not None and a == d:
                    d = r + 1
            else:
                d = r + 1
                if a is not None and a == d:
                    d = r + 2
    if ind_mapping is not None:
        if graph_mapped[0]:
            r = ind_mapping[r]
        if graph_mapped[1]:
            a = ind_mapping[a]
        if graph_mapped[2]:
            d = ind_mapping[d]
    return (r, a, d)
def add_missing_zmatrix_bonds(
        base_zmat,
        bonds,
        max_iterations=None,
        validate_additions=True
):
    atoms, zm = canonicalize_zmatrix(base_zmat)
    new_bonds = {}
    reindexing = list(atoms)
    for bi, be in bonds:
        if bi in atoms and be in atoms: continue
        if bi not in atoms and be not in atoms: continue
        if bi in atoms:
            # bi_pos = np.where(atoms == bi)[0][0]
            if bi not in new_bonds: new_bonds[bi] = []
            new_bonds[bi].append(be)
        if be in atoms:
            if be not in new_bonds: new_bonds[be] = []
            new_bonds[be].append(bi)

    if len(new_bonds) == 0:
        return base_zmat, new_bonds
    else:
        mods = []
        for i,v in new_bonds.items():
            v = [vv for vv in v if vv not in reindexing]
            if len(v) > 0:
                i_pos = np.where(atoms == i)[0][0]
                reindexing.extend(v)
                # ix = _attachment_point(i_pos)
                ix = (i_pos, -1, -2)
                mods.append([ix, center_bound_zmatrix(len(v))])

        new_zm = functionalized_zmatrix(
                zm,
                mods
            )
        if validate_additions and not validate_zmatrix(new_zm):
            raise ValueError(f"invalid zmatrix after functionalization, {new_zm}")
        new_zm = reindex_zmatrix(new_zm, reindexing)
        if validate_additions:
            is_valid, reason = validate_zmatrix(new_zm, return_reason=True)
            if not is_valid:
                raise ValueError(f"invalid zmatrix after reindexing ({reason}) in {reindexing} to {new_zm}")

        if max_iterations is None or max_iterations > 0:
            new_zm, new_new_bonds = add_missing_zmatrix_bonds(
                new_zm,
                bonds,
                max_iterations=max_iterations-1 if max_iterations is not None else max_iterations,
                validate_additions=validate_additions
            )

            new_bonds.update(new_new_bonds)

        return new_zm, new_bonds

def make_zmatrix_tree(zm):
    graph = {}
    for n,(i,j,k,l) in enumerate(zm):
        parents = tuple(x for x in (j, k, l)[:n] if x >= 0)
        if i not in graph:
            graph[i] = {
                # 'parents': [], # ordered
                'children': set() # unordered
            }
        graph[i]['parents'] = parents
        for x in parents:
            if x >= 0:
                graph[x]['children'].add(i)
    return graph

def zmatrix_adjacency_matrix(zm, child_type='multi'):
    adj_mat = np.zeros((len(zm),len(zm)), dtype=bool)
    if not isinstance(zm, dict):
        zm = make_zmatrix_tree(zm)
    zm_atoms = sorted(zm.keys(), key=lambda x: len(zm[x]['parents']))
    ord = {a:i for i,a in enumerate(zm_atoms)}
    for entry in zm_atoms:
        i = ord[entry]
        if child_type == 'single':
            for c in zm[entry]['children']:
                if zm[c]['parents'][0] == entry:
                    j = ord[c]
                    adj_mat[i][j] = True
        else:
            for c in zm[entry]['children']:
                j = ord[c]
                adj_mat[i][j] = True
    return zm_atoms, adj_mat

def zmatrix_from_tree(zm, check_cycles=True, chain_order=None, check_unique_root=True):
    if check_unique_root:
        zm_atoms = sorted(zm.keys(), key=lambda x: len(zm[x]['parents']))
        if len(zm[zm_atoms[0]]['parents']) != 0:
            raise ValueError(f"root atom has wrong number of parents in {zm_atoms}")
        if len(zm) > 1 and len(zm[zm_atoms[1]]['parents']) != 1:
            raise ValueError(f"first child atom has wrong number of parents in {zm_atoms}")
        if len(zm) > 2 and len(zm[zm_atoms[2]]['parents']) != 2:
            raise ValueError(f"second child atom has wrong number of parents in {zm_atoms}")

    if chain_order is None:
        if check_cycles:
            zm_atoms, zm_adj_mat = zmatrix_adjacency_matrix(zm, child_type='multi')
            g = spg.csr_matrix(zm_adj_mat)
            comps, groups = spg.csgraph.connected_components(g, connection='strong')
            has_cycles = comps < len(zm_atoms)
            if has_cycles:
                # import pprint
                # pprint.pprint(zm)
                # print(groups)
                # print(zm_atoms)
                raise ValueError(f"Z-matrix tree invalid as it has cycles (groups: {groups} for atoms: {zm_atoms} in {zm})")

        #TODO: ensure this is the longest chain
        zm_atoms, zm_adj_mat = zmatrix_adjacency_matrix(zm, child_type='single')
        g = spg.csr_matrix(zm_adj_mat)
        chain_order, _ = spg.csgraph.depth_first_order(g, 0)
        chain_order = [zm_atoms[c] for c in chain_order]

    rows = []
    for c in chain_order:
        parents = zm[c]['parents']
        if len(parents) == 0:
            parents = [-1, -2, -3]
        elif len(parents) == 1:
            parents = parents + (-1, -2)
        elif len(parents) == 2:
            parents = parents + (-1,)
        rows.append([c] + list(parents))

    return rows

def check_zmatrix_coordinate_constraint(zm, coord):
    # if not isinstance(zm, dict): zm = make_zmatrix_tree(zm)
    # coord = tuple(coord)

    n = len(coord) - 1
    p1 = zm[coord[0]]['parents']
    if (coord[0],) + p1[:n] == coord:
        return (coord[0], p1)

    p2 = zm[coord[-1]]['parents']
    p2 = tuple(reversed(p2)) #TODO: use direct indexing
    if p2[:n] + (coord[-1],) == coord:
        return (coord[-1], p2)

    return False

def _adjust_zm_parents(zm, i, new, constraint_map):
    p1 = zm[i]['parents']
    zm[i]['parents'] = new
    if all(
            check_zmatrix_coordinate_constraint(zm, c)
            for c in constraint_map.keys()
    ):
        for o in p1:
            zm[o]['children'].remove(i)
        for o in new:
            zm[o]['children'].add(i)

        # determine how chain order has changed and re-parent
        # anything that needs tweaks
        zm_atoms, zm_adj_mat = zmatrix_adjacency_matrix(zm, child_type='single')
        g = spg.csr_matrix(zm_adj_mat)
        chain_order, _ = spg.csgraph.depth_first_order(g, 0)
        chain_order: list[int] = [zm_atoms[c] for c in chain_order]
        ord_map = {o: i for i, o in enumerate(chain_order)}
        backup = {
            o: {'parents':d['parents'], 'children':d['children'].copy()}
            for o, d in zm.items()
        }
        # recompute parents for the modified Z-matrix
        zm = {
            o: {'parents':d['parents'], 'children':set()}
            for o, d in zm.items()
        }
        for n, o in enumerate(chain_order):
            zd = zm[o]
            new_parents = [
                p
                for p in zd['parents']
                if ord_map[p] < n
            ]
            if n == 1 and len(new_parents) == 0:
                new_parents = [chain_order[0]]
            elif n == 2:
                if len(new_parents) == 0:
                    new_parents = [chain_order[0], chain_order[1]]
                elif len(new_parents) == 1:
                    if chain_order[0] in new_parents:
                        new_parents.append(chain_order[1])
                    else:
                        new_parents.append(chain_order[0])
            elif n > 2 and len(new_parents) < 3:
                # find previous chain entries that
                # have one of the active parents as children
                for p in tuple(new_parents):
                    nd = zm[p]
                    add_parents = [
                        pp
                        for pp in nd['parents']
                        if ord_map[pp] < n
                    ]
                    new_parents.extend(add_parents)
                    new_parents = new_parents[:3]
                    if len(new_parents) == 3:
                        break
                else:
                    new_parents.extend(chain_order[:n + 1])
                    new_parents = new_parents[:3]
            for p in new_parents:
                zm[p]['children'].add(o)
            zd['parents'] = tuple(new_parents)

        if all(
                check_zmatrix_coordinate_constraint(zm, c)
                for c in constraint_map.keys()
        ):
            return True, zm
        else:
            for o, d in backup.items():
                zm[o] = d
            for o in p1:
                zm[o]['children'].add(i)
            for o in new:
                zm[o]['children'].remove(i)
            zm[i]['parents'] = p1
    else:
        zm[i]['parents'] = p1
    return False, zm

def enforce_required_zmatrix_coordinates(zm, coords):#, chain_order=None):
    zm_og = zm
    if not isinstance(zm, dict):
        zm = make_zmatrix_tree(zm)
    # else:
    #     if chain_order is None:
    #         zm_atoms, zm_adj_mat = zmatrix_adjacency_matrix(zm)
    #         g = spg.csr_matrix(zm_adj_mat)
    #         # TODO: ensure this is the longest chain
    #         chain_order, _ = spg.csgraph.depth_first_order(g, zm_atoms[0])
    #         chain_order = [zm_atoms[c] for c in chain_order]

    constraint_map = {
        c: check_zmatrix_coordinate_constraint(zm, c)
        for c in coords
    }
    missing_constraints = [
        c for c,v in constraint_map.items()
        if not v
    ]
    if len(missing_constraints) == 0: return zm_og

    constraint_map = {
        c:v
        for c, v in constraint_map.items()
        if v
    }
    modified = False
    for m in missing_constraints:
        # handle cases differently
        i, j = m[0], m[-1]
        # we may have to shuffle one of these atoms, but we first check if the constraint
        # is satisfiable by just permuting the referents
        p1 = zm[i]['parents']
        if (
                all(x in p1 for x in m[1:])
                and not any(
                    # this might be the same as v? Need to check
                    c == (i,) + p1[:len(c)-1]
                    or c == tuple(reversed(p1))[:len(c)-1] + (i,)
                    for c in constraint_map.keys()
                )
        ):
            if not modified:
                zm = zm.copy()
                modified = True

            x = [p1.index(y) for y in m[1:]]
            rem = np.setdiff1d(np.arange(3), x)
            p1 = tuple(p1[z] for z in np.concatenate([x, rem]))
            zm[i]['parents'] = p1
            constraint_map[m] = p1
            continue
        del p1

        p2 = zm[j]['parents']
        if (
                all(x in p2 for x in m[:-1])
                and not any(
                    # this might be the same as v? Need to check
                    c == (j,) + tuple(reversed(p2))[-len(c):]
                    or c == p2[-len(c):] + (j,)
                    for c in constraint_map.keys()
                )
        ):
            # do minimal permutation
            x = [p2.index(y) for y in reversed(m[:-1])]
            rem = np.setdiff1d(np.arange(3), x)
            p2 = tuple(p2[z] for z in np.concatenate([x, rem]))
            zm[j]['parents'] = p2
            constraint_map[m] = p2
            continue
        del p2

        # check to see if modifying the parents of `i` or `j` would
        # violate a different constraint
        if not modified:
            zm = zm.copy()
            modified = True

        if len(m) == 2:
            refs = zm[j]['parents'][:2]
            p1 = zm[i]['parents']
            new = (j,) + refs
            if len(new) < len(p1):
                new = new + p1[:len(p1) - len(new)]
            # check that we haven't broken any constraints
            # TODO: write targeted loops
            success, zm = _adjust_zm_parents(zm, i, new, constraint_map)
            if success:
                constraint_map[m] = new
                continue
            del p1

            # if len(zm[j]['parents']) > 0:
            refs = zm[i]['parents'][:2]
            p2 = zm[j]['parents']
            new = (j,) + refs
            if len(new) < len(p2):
                new = new + p2[:len(p2) - len(new)]
            # check that we haven't broken any constraints
            # TODO: write targeted loops
            zm[j]['parents'] = new
            if all(
                    check_zmatrix_coordinate_constraint(zm, c)
                    for c in constraint_map.keys()
            ):
                for o in p2:
                    zm[o]['children'].remove(j)
                for o in new:
                    zm[o]['children'].add(j)
                constraint_map[m] = new
                continue
            else:
                zm[j]['parents'] = p2

            raise ValueError(f"couldn't satisfy constraint {m} in {coords}")
        elif len(m) == 3:
            raise NotImplementedError(...)
        else:
            raise NotImplementedError(...)
            p1 = ...
            old = zm[i]['parents']




        raise Exception("?")

    if not isinstance(zm_og, dict):
        zm = zmatrix_from_tree(zm)

    return zm


def bond_graph_zmatrix(
        bonds,
        fragments,
        edge_map=None,
        reindex=True,
        validate_additions=True,
        required_coordinates=None
):
    submats = []
    backbone = fragments[0]
    if edge_map is None:
        edge_map = EdgeGraph.get_edge_map(bonds)
    for frag in fragments[1:]:
        if nput.is_int(frag[0]):
            submats.append(
                chain_zmatrix(len(frag))
            )
        else:
            submats.append(
                bond_graph_zmatrix(
                    bonds,
                    frag,
                    edge_map=edge_map,
                    reindex=False
                )
            )

    fragments = fragments[1:]
    fused = chain_zmatrix(len(backbone))
    backbone = list(backbone)
    while len(fragments) > 0:
        attachment_points = {}
        missing_frags = []
        missing_mats = []
        added_frags = []
        for frag,mat in zip(fragments, submats):
            base_frag = frag
            if not nput.is_int(frag[0]):
                frag = frag[0]

            for f in frag:
                attach = None
                submap = edge_map.get(f)

                if nput.is_int(submap):
                    if submap in backbone:
                        attach = submap
                else:
                    for s in submap:
                        if s in backbone:
                            attach = s
                            break

                if attach is not None:
                    added_frags.append(base_frag)
                    attachment_points[backbone.index(attach)] = mat
                    break
            else:
                missing_frags.append(frag)
                missing_mats.append(mat)

        if len(missing_frags) == len(fragments):
            raise ValueError(
                f"can't attach fragments {fragments} to backbone {backbone}, no connections"
            )

        fused = functionalized_zmatrix(
            fused,
            {
                _attachment_point(ap):zmat
                for ap,zmat in attachment_points.items()
            }
        )
        if validate_additions:
            is_valid, reason = validate_zmatrix(fused, return_reason=True)
            if not is_valid:
                raise ValueError(f"base graph zmatrix invalid ({reason}) in {fused}")

        backbone = backbone + list(itut.flatten(added_frags))
        fragments = missing_frags
        submats = missing_mats

    # if len(fragments) == 1:
    #     raise ValueError(f"can't attach fragment {fragments[0]} to backbone {backbone}, no connections")

    if reindex:
        flat_frags = backbone
        if validate_additions:
            frag_counts = itut.counts(flat_frags)
            bad_frags = {k:v for k,v in frag_counts.items() if v > 1}
            if len(bad_frags) > 0:
                raise ValueError(f"duplicate atoms {list(bad_frags.keys())} encountered in {fragments}")
        fused = reindex_zmatrix(fused, flat_frags)
        if validate_additions:
            is_valid, reason = validate_zmatrix(fused, return_reason=True)
            if not is_valid:
                raise ValueError(f"after reindexing zmatrix invalid ({reason}) in {fused}")

    if required_coordinates is not None:
        print(np.array(fused))
        # graph = make_zmatrix_tree(fused)
        # we rearrange nodes in the tree
        # appropriately
        # new = zmatrix_from_tree(graph)
        new = enforce_required_zmatrix_coordinates(fused, required_coordinates)
        # new = zmatrix_from_tree(forced)
        print(np.array(new))
        raise Exception()
        import pprint
        pprint.pprint(graph)
        raise Exception()
        # figure out how fragments must be ordered
        fragment_sorting_map = []
        for c in required_coordinates:
            submap = {}
            for i in c:
                for j, f in enumerate(fragments):
                    try:
                        x = f.index(i)
                    except ValueError:
                        continue
                    else:
                        submap[i] = (j, x)
                        break
            fragment_sorting_map.append(submap)
        # then find a consistent sorting for the fragments included in the map
        # each coordinate has multiple possible orderings so we first take all included
        # fragments and then try to find a consistent ordering
        all_frags = np.unique([
            f[0]
            for submap in fragment_sorting_map
            for f in submap.values()
        ])

        raise Exception(all_frags)

    return fused

def canonical_fragment_zmatrix(canonical_framents, validate_additions=False):
    atom_ordering = []
    for _, f in canonical_framents:
        atom_ordering.extend(f)
    atom_ordering = np.argsort(atom_ordering)
    inv_order = np.argsort(atom_ordering)
    backbone = chain_zmatrix(len(canonical_framents[0][1]))
    attachment_points = []
    for bb,frag in canonical_framents[1:]:
        submat = chain_zmatrix(len(frag))
        if bb is None:
            if len(attachment_points) > 0:
                backbone = functionalized_zmatrix(
                    backbone,
                    attachment_points,
                    validate=validate_additions
                )
                attachment_points = []
            n = len(backbone)
            backbone = backbone + [
                [i + n for i in z]
                for z in submat
            ]
        else:
            bb = [inv_order[i] if i >= 0 else i for i in bb]
            attachment_points.append(
                (bb, submat)
            )
    if len(attachment_points) > 0:
        # for a in attachment_points:
        #     print("???", a)
        backbone = functionalized_zmatrix(
            backbone,
            attachment_points,
            validate=validate_additions
        )

    if validate_additions:
        is_valid, reason = validate_zmatrix(backbone, return_reason=True)
        if not is_valid:
            raise ValueError(f"base canonical zmatrix invalid ({reason}) in {backbone}")

    # print(np.array(backbone))
    # print(atom_ordering)
    backbone = reindex_zmatrix(backbone, atom_ordering)
    if validate_additions:
        is_valid, reason = validate_zmatrix(backbone, return_reason=True)
        if not is_valid:
            raise ValueError(f"post reindexing zmatrix invalid ({reason}) in {backbone}")
    return backbone

def sort_complex_attachment_points(
        fragment_inds,
        attachment_points: 'dict|tuple[tuple[int], list[list[int]]]'
):
    new_attachments = [None] * len(fragment_inds)
    fragment_inds = list(fragment_inds)
    if hasattr(attachment_points, 'items'):
        attachment_points = attachment_points.items()
    for start, end in attachment_points:
        if nput.is_int(start):
            start = [start]
        if nput.is_int(end):
            end = [end]

        start_frag = None
        for i, f in enumerate(fragment_inds):
            if start[0] in f:
                start_frag = i
                break
        else:
            raise ValueError(f"index {start[0]} not in fragments {fragment_inds}")

        end_frag = None
        for i, f in enumerate(fragment_inds):
            if end[0] in f:
                end_frag = i
                break
        else:
            raise ValueError(f"index {start[0]} not in fragments {fragment_inds}")

        if end_frag < start_frag:
            start, end = end, start
            start_frag, end_frag = end_frag, start_frag
        elif end_frag == start_frag:
            raise ValueError(f"root index {start[0]} and end index {end[0]} in same fragment")

        fragment_inds[start_frag] = tuple(sorted(
            fragment_inds[start_frag],
            key=lambda i: start.index(i) if i in start else len(start)
        ))
        fragment_inds[end_frag] = tuple(sorted(
            fragment_inds[end_frag],
            key=lambda i: end.index(i) if i in end else len(end)
        ))

        new_attachments[end_frag] = start

    return fragment_inds, new_attachments

def complex_zmatrix(
        bonds,
        fragment_inds=None,
        fragment_zmats=None,
        distance_matrix=None,
        attachment_points=None,
        check_attachment_points=True,
        graph=None,
        reindex=True,
        validate_additions=True
):
    if fragment_inds is None:
        if fragment_zmats is not None:
            raise ValueError("can't supply just Z-mats, unclear which fragments they come from...")
        all_inds = np.unique(np.concatenate(bonds))
        if graph is None:
            graph = EdgeGraph(all_inds, bonds)

        fragment_inds = graph.get_fragments()

    all_inds = np.concatenate(fragment_inds)
    if graph is None:
        graph = EdgeGraph(all_inds, bonds)

    if fragment_zmats is None:
        if isinstance(attachment_points, dict):
            fragment_inds, attachment_points = sort_complex_attachment_points(
                fragment_inds,
                attachment_points
            )

        fragment_zmats = [
            bond_graph_zmatrix(bonds, f, edge_map=graph.map)
            for f in fragment_inds
        ]
    elif isinstance(attachment_points, dict) and check_attachment_points:
        raise ValueError("can't supply Z-mats and dict of attachment points, can't be sure attachments are right")

    inds = np.asanyarray(fragment_inds[0])
    zm = fragment_zmats[0]
    if validate_additions:
        is_valid, reason = validate_zmatrix(zm, return_reason=True)
        if not is_valid:
            raise ValueError(f"base zmatrix invalid ({reason}) in {zm}")
    if attachment_points is None:
        attachment_points = [None] * len(fragment_inds)
    if len(attachment_points) < len(fragment_inds):
        raise ValueError("too few attachment points specified")
    for inds_2, zm_2, root in zip(fragment_inds[1:], fragment_zmats[1:], attachment_points[1:]):
        if validate_additions:
            is_valid, reason = validate_zmatrix(zm_2, return_reason=True)
            if not is_valid:
                raise ValueError(f"fragment invalid ({reason}) in {zm_2} with attachement point {inds_2}")
        if root is None:
            if distance_matrix is None:
                subgraph = graph.take(inds)
                min_row = subgraph.get_centroid(check_fragments=False) #TODO: see if I need to add a row check to this...
            else:
                # distance_matrix = np.asanyarray(distance_matrix)
                dm_row = distance_matrix[zm_2[0][0]]
                min_row = np.argmin(dm_row[inds,], axis=0)
                # dm = distance_matrix[np.ix_(inds, inds_2)]
                # min_cols = np.argmin(dm, axis=1)
                # min_row = np.argmin(dm[np.arange(len(inds)), min_cols], axis=0)
                # min_row = inds[min_row]
                # min_cols = inds_2[min_cols[min_row]]
                # min_row = np.where(inds == min_row)[0][0]
                # root = zm[min_row][0]
        else:
            if nput.is_int(root):
                min_row = np.where(inds == root)[0][0]
            else:
                min_row = [np.where(inds == r)[0][0] for r in root]
            # root = zm[min_row][0]

        ind_mapping = {k:i for i,k in enumerate(inds)}
        ap = tuple(ind_mapping[x] for x in _attachment_point(inds[min_row], graph))
        inds = np.concatenate([inds, inds_2])
        zm = functionalized_zmatrix(
            zm,
            {
                ap : set_zmatrix_embedding(zm_2)
            }
        )
        if validate_additions:
            is_valid, reason = validate_zmatrix(zm, return_reason=True)
            if not is_valid:
                raise ValueError(f"new zmatrix after attachment invalid ({reason}) at {ap} in {zm}")

    if reindex:
        zm = reindex_zmatrix(zm, inds)
        if validate_additions:
            is_valid, reason = validate_zmatrix(zm, return_reason=True)
            if not is_valid:
                raise ValueError(f"new zmatrix after reindexing invalid ({reason}) in {zm}")

    return zm

def graph_backbone_zmatrix(bond_graph: EdgeGraph,
                     root=None, segments=None, return_remainder=False, return_segments=False,
                     validate=True
                     ):
    if segments is None:
        segments = bond_graph.segment_by_chains(root=root)
        if validate:
            flat_frags = list(itut.flatten(segments))
            frag_counts = itut.counts(flat_frags)
            bad_frags = {k: v for k, v in frag_counts.items() if v > 1}
            if len(bad_frags) > 0:
                raise ValueError(f"diplicate atoms {list(bad_frags.keys())} encountered in {segments}")

    bond_list = bond_graph.edges
    base_graph = bond_graph_zmatrix(
        bond_list,
        segments,
        validate_additions=validate
    )
    zmat, new_bonds = add_missing_zmatrix_bonds(
        base_graph,
        bond_list,
        validate_additions=validate
    )

    if return_segments or return_remainder:
        res = (zmat,)
        if return_segments:
            res = res + (segments,)
        if return_remainder:
            res = res + (new_bonds,)

        return res
    else:
        return zmat

def segmented_complex_backbone_zmatrix(bond_graph: EdgeGraph,
                                       fragments=None, segments=None, root=None,
                                       attachment_points=None,
                                       check_attachment_points=True,
                                       validate=True,
                                       for_fragment=None,
                                       fragment_ordering=None,
                                       distance_matrix=None):
    no_frag = fragments is None
    if fragments is None:
        fragments = bond_graph.get_fragments()
    if for_fragment is not None:
        if nput.is_int(for_fragment):
            for_fragment = fragments[for_fragment]
        if attachment_points is not None:
            frag_map = dict(zip(for_fragment, np.arange(len(for_fragment))))
            if hasattr(attachment_points, 'items'):
                attachment_points = {
                    frag_map[i]: (frag_map[k] if nput.is_numeric(k) else tuple(frag_map[kk] for kk in k))
                    for i,k in attachment_points.items()
                }
            else:
                attachment_points = [
                    frag_map[i] for i in attachment_points
                ]

        if distance_matrix is not None:
            distance_matrix = distance_matrix[np.ix_(for_fragment, for_fragment)]
        base_ints = segmented_complex_backbone_zmatrix(
            bond_graph.take(for_fragment),
            fragments=fragments, segments=segments, root=root,
            attachment_points=attachment_points,
            check_attachment_points=check_attachment_points,
            fragment_ordering=fragment_ordering,
            distance_matrix=distance_matrix,
            validate=validate
        )
        return reindex_zmatrix(base_ints, for_fragment)
    else:

        if len(fragments) == 1:
            if segments is not None and len(segments) == 1:
                segments = segments[0]
            return graph_backbone_zmatrix(
                bond_graph,
                root=root, segments=segments,
                validate=validate
                )
        else:
            inds = fragments
            if no_frag:
                if fragment_ordering is None:
                    fragment_ordering = np.argsort([-len(x) for x in inds])
                inds = [inds[i] for i in fragment_ordering]
            if root is not None:
                if nput.is_numeric(root):
                    inds = list(sorted(inds, key=lambda x:root not in x))
                else:
                    inds = list(
                        sorted(inds,
                               key=lambda x:sum(i if r is not None and r in x else len(inds) for i,r in enumerate(root))
                               )
                    )

            sort_attch = isinstance(attachment_points, dict)
            if sort_attch:
                check_attachment_points = False
                inds, attachment_points = sort_complex_attachment_points(
                    inds,
                    attachment_points
                )

            frags = [bond_graph.take(ix) for ix in inds]
            if root is None and sort_attch:
                root = [ix[0] for ix in inds]
            if root is None:
                root = [root]

            root = list(root) + [None] * (len(inds) - len(root))
            zmats = [
                graph_backbone_zmatrix(f, root=r)
                for r,f in zip(root, frags)
            ]

            return complex_zmatrix(
                bond_graph.edges,
                inds,
                zmats,
                distance_matrix=distance_matrix,
                attachment_points=attachment_points,
                check_attachment_points=check_attachment_points,
                validate_additions=validate
            )
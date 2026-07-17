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
    "segmented_complex_backbone_zmatrix",
    "enforce_required_zmatrix_coordinates"
]


def zmatrix_unit_convert(zmat, distance_conversion, angle_conversion=None, rad2deg=False, deg2rad=False):
    """
    **LLM Docstring**

    Scale the distance and angular columns of a Z-matrix value array.

    A copy is made when `np.asanyarray` returns the original object. Column 0 is multiplied by `distance_conversion`. Columns 1 and 2 are multiplied by `angle_conversion` when supplied; otherwise they are optionally converted between degrees and radians.

    :param zmat: Z-matrix values whose final two axes are atoms by `(distance, angle, dihedral)`.
    :type zmat: array-like
    :param distance_conversion: Multiplicative factor applied to all distances.
    :type distance_conversion: float
    :param angle_conversion: Multiplicative factor applied to bends and dihedrals. When omitted, `rad2deg` or `deg2rad` controls angular conversion.
    :type angle_conversion: float | None
    :param rad2deg: Convert angular columns from radians to degrees when `angle_conversion` is omitted.
    :type rad2deg: bool
    :param deg2rad: Convert angular columns from degrees to radians when `angle_conversion` is omitted.
    :type deg2rad: bool
    :return: Converted Z-matrix values, without modifying the input array in place.
    :rtype: np.ndarray
    """
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
    """
    **LLM Docstring**

    Locate internal coordinates within the ordered coordinate list represented by a Z-matrix.

    The Z-matrix is expanded into its bond, angle, and dihedral tuples, optionally excluding embedding coordinates. Both the extracted coordinates and requested coordinates are canonicalized before list lookup. A single coordinate returns one integer; a sequence returns a list.

    :param zmat: Four-column or reference-only Z-matrix ordering.
    :type zmat: Sequence[Sequence[int]]
    :param coords: One internal-coordinate tuple or a sequence of tuples.
    :type coords: Sequence[int] | Sequence[Sequence[int]]
    :param strip_embedding: Exclude the translational and rotational embedding entries from the searchable coordinate list.
    :type strip_embedding: bool
    :return: Position or positions of the requested coordinates.
    :rtype: int | list[int]
    """
    smol = nput.is_int(coords[0])
    if smol: coords = [coords]
    base_coords = [canonicalize_internal(c) for c in extract_zmatrix_internals(zmat, strip_embedding=strip_embedding)]
    res = [
        base_coords.index(canonicalize_internal(c))
        for c in coords
    ]
    if smol: res = res[0]
    return res

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
    """
    **LLM Docstring**

    Return the flattened entries occupied by Z-matrix embedding coordinates.

    For a molecule with zero, one, two, or at least three atoms, this selects the distance/angle/dihedral entries used to fix overall translation and rotation. With `partial_embedding`, only the three coordinates required by the partially embedded representation are selected. With `array_inds`, flattened positions are converted to `(row, column)` pairs and adjusted for three-column orderings.

    :param zmat_or_num_atoms: Atom count or a Z-matrix-like ordering from which the atom count and column convention are inferred.
    :type zmat_or_num_atoms: int | Sequence[Sequence[int]]
    :param partial_embedding: Select the reduced embedding used by `zmatrix_from_values(..., partial_embedding=True)`.
    :type partial_embedding: bool
    :param array_inds: Return two-dimensional array indices instead of flattened indices.
    :type array_inds: bool
    :return: Embedding positions in flattened or `(row, column)` form.
    :rtype: list[int] | list[tuple[int, int]]
    """
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
    """
    **LLM Docstring**

    Count scalar Z-matrix coordinates for a molecule or ordering.

    The full representation contains three values per atom. When `strip_embedding` is true, the entries identified by `zmatrix_embedding_coords` are subtracted, giving the number of internal degrees represented after removing global translation and rotation.

    :param zmat_or_num_atoms: Atom count or Z-matrix ordering.
    :type zmat_or_num_atoms: int | Sequence[Sequence[int]]
    :param strip_embedding: Remove embedding coordinates from the count.
    :type strip_embedding: bool
    :return: Number of scalar Z-matrix values.
    :rtype: int
    """
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
    """
    **LLM Docstring**

    Yield complete Z-matrix orderings consistent with a set of internal coordinates.

    Coordinates are optionally canonicalized into the orientation expected by a Z-matrix and deduplicated. Optional origin rows for atoms 0–2 are inserted. Candidate dihedrals are grouped by the atom they introduce; only dihedrals whose bond and angle prefixes are available are retained unless completions are allowed. The function then takes the Cartesian product of the admissible embedding angle and one introducing dihedral for every atom from index 3 onward, yielding four-column rows with standard negative embedding references.

    :param coords: Bond, angle, and dihedral tuples available for constructing rows.
    :type coords: Sequence[Sequence[int]]
    :param natoms: Number of atoms. Inferred from unique coordinate indices when omitted.
    :type natoms: int | None
    :param include_origins: Insert the bond and angle coordinates needed for the first three atoms.
    :type include_origins: bool
    :param canonicalize: Canonicalize coordinate orientation before matching prefixes.
    :type canonicalize: bool
    :param deduplicate: Remove repeated coordinate tuples while preserving order.
    :type deduplicate: bool
    :param allow_completions: Permit dihedrals whose bond or angle prefix is not explicitly present.
    :type allow_completions: bool
    :return: An iterator of complete four-column Z-matrix orderings.
    :rtype: Iterator[tuple[tuple[int, int, int, int], ...]]
    """
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
    """
    **LLM Docstring**

    Enumerate Z-matrix orderings compatible with supplied internal coordinates.

    The coordinate set is canonicalized and deduplicated. When `preorder_atoms` is enabled, atoms are ranked by how often they occur in the coordinate set so highly connected atoms are tried first. The function then considers every allowed atom permutation, rewrites each coordinate into that permutation's index space, asks `_zmatrix_iterate` for every complete choice of introducing dihedrals, and maps each yielded row back to the original atom labels.

    :param coords: Available bond, angle, and dihedral coordinate tuples.
    :type coords: Sequence[Sequence[int]]
    :param natoms: Number of atoms; inferred from coordinate indices when omitted.
    :type natoms: int | None
    :param allow_permutation: Try all atom order permutations rather than only the preordered sequence.
    :type allow_permutation: bool
    :param include_origins: Add the coordinates needed to define the first three atoms.
    :type include_origins: bool
    :param canonicalize: Canonicalize coordinate directions before enumeration.
    :type canonicalize: bool
    :param deduplicate: Remove duplicate coordinate tuples.
    :type deduplicate: bool
    :param preorder_atoms: Start permutations from atoms sorted by coordinate participation count.
    :type preorder_atoms: bool
    :param allow_completions: Allow rows whose bond or angle prefixes were not explicitly supplied.
    :type allow_completions: bool
    :return: Z-matrix orderings in original atom-index space.
    :rtype: Iterator[list[list[int]]]
    """
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
    """
    **LLM Docstring**

    Expand a Z-matrix ordering into its bond, angle, and dihedral coordinate tuples.

    Three-column orderings are first promoted to four columns by adding the implicit atom index and embedding row. For each row the function emits the bond prefix, then the angle prefix, then the dihedral prefix, skipping the undefined embedding entries for the first three atoms when requested. Returned tuples may be canonicalized to make reversed coordinates equivalent.

    :param zmat: Three- or four-column Z-matrix ordering.
    :type zmat: Sequence[Sequence[int]]
    :param strip_embedding: Omit coordinates that only establish the external frame.
    :type strip_embedding: bool
    :param canonicalize: Canonicalize each emitted coordinate tuple.
    :type canonicalize: bool
    :return: Ordered list of internal-coordinate tuples represented by the Z-matrix.
    :rtype: list[tuple[int, ...]]
    """
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
    """
    **LLM Docstring**

    Flatten Z-matrix values and select internal-coordinate entries.

    A four-column array is interpreted as containing atom indices in column 0, which are removed before flattening. When no explicit indices are supplied, all values are selected and embedding entries are deleted if requested. Explicit indices are interpreted in the stripped coordinate space when `strip_embedding` is true.

    :param zmat: Z-matrix value array with shape `(..., n_atoms, 3)` or a four-column combined array.
    :type zmat: array-like
    :param inds: Coordinate positions to extract, or all positions when omitted.
    :type inds: Sequence[int] | None
    :param partial_embedding: Use the reduced embedding mask when automatically selecting coordinates.
    :type partial_embedding: bool
    :param strip_embedding: Exclude embedding entries and interpret `inds` relative to the remaining coordinates.
    :type strip_embedding: bool
    :return: Selected values with the atom/value axes flattened into one final axis.
    :rtype: np.ndarray
    """
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
    """
    **LLM Docstring**

    Reconstruct an atom-by-three Z-matrix value array from flattened values.

    Unstripped data is reshaped directly. For partial embedding, the first atom's distance and the second atom's distance/angle are restored before remaining triples are filled. For full embedding, the first three atoms receive the conventional zero-valued undefined entries, and the supplied values begin with atom 1's distance, atom 2's distance/angle, then complete triples.

    :param flat_z: Flattened Z-matrix values with optional leading batch dimensions.
    :type flat_z: array-like
    :param strip_embedding: Whether embedding entries are absent from `flat_z`.
    :type strip_embedding: bool
    :param partial_embedding: Interpret `flat_z` using the reduced three-coordinate embedding convention.
    :type partial_embedding: bool
    :return: Z-matrix values with shape `(..., n_atoms, 3)`.
    :rtype: np.ndarray
    """
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
    """
    **LLM Docstring**

    Parse one tokenized Z-matrix variable specification.

    A single token becomes a floating-point constant. A value followed by `F` becomes a frozen `scan_spec` with `steps=-1`. Three tokens become `scan_spec(value, steps, amount)`. Other lengths are rejected.

    :param v: Tokens following a variable name.
    :type v: Sequence[str]
    :return: Numeric value or parsed scan specification.
    :rtype: float | scan_spec
    """
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
    """
    **LLM Docstring**

    Parse a Gaussian-style textual Z-matrix into atoms, ordering, and coordinate values.

    The atom/reference/value token stream is split into rows of increasing width for the first three atoms and seven fields thereafter. Positive one-based references are converted to zero-based indices. A `Variables:` block is parsed into constants or scan specifications. Unless variables are retained, symbols are replaced by numeric values, distances are converted from `units` to Bohr, and angles and dihedrals are converted to radians unless already supplied in radians.

    :param zmat: Gaussian-style Z-matrix text, optionally followed by a `Variables:` block.
    :type zmat: str
    :param units: Distance unit used by numeric values.
    :type units: str
    :param in_radians: Treat angular values as radians instead of degrees.
    :type in_radians: bool
    :param has_values: Whether coordinate values alternate with reference indices in each row.
    :type has_values: bool
    :param atoms_are_order: Interpret the atom column as an explicit one-based atom permutation rather than element symbols.
    :type atoms_are_order: bool
    :param keep_variables: Return unresolved coordinate tokens and the variable table instead of numeric arrays.
    :type keep_variables: bool
    :param variables: Additional or overriding variable definitions.
    :type variables: dict | None
    :param dialect: Input dialect; only `gaussian` is implemented.
    :type dialect: str
    :return: Numeric `(atoms, ordering, coords)`, or `((atoms, ordering, token_coords), variables)` when variables are retained.
    :rtype: tuple
    """
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
    """
    **LLM Docstring**

    Format atoms, references, and values as a Gaussian-style Z-matrix string.

    Combined alternating reference/value rows are separated when `ordering` is omitted. Distances are converted from Bohr to `units`; angles are converted from radians to degrees unless requested otherwise. Optional generated variable names replace numeric values, coordinate-specific modifications can append scan/freeze suffixes, indices receive `index_padding`, and all columns are width-aligned. A `Variables:` block is appended when variables are present.

    :param atoms: Atom labels in output order.
    :type atoms: Sequence[str]
    :param zmat: Z-matrix values or alternating reference/value rows.
    :type zmat: array-like | Sequence
    :param ordering: Reference-index rows, optionally including explicit atom indices.
    :type ordering: Sequence[Sequence[int]] | None
    :param units: Distance unit for formatted output.
    :type units: str
    :param in_radians: Keep angular values in radians instead of converting to degrees.
    :type in_radians: bool
    :param float_fmt: Format string used for numeric values.
    :type float_fmt: str
    :param index_padding: Offset added to nonnegative atom references, normally 1 for Gaussian indexing.
    :type index_padding: int
    :param variables: Existing variable mapping, `True` to generate one variable per defined coordinate, or `None` for inline values.
    :type variables: dict | bool | None
    :param variable_modifications: Mapping from coordinate tuples to suffix text appended to variable definitions.
    :type variable_modifications: dict | None
    :param distance_variable_format: Template for generated distance symbols.
    :type distance_variable_format: str
    :param angle_variable_format: Template for generated angle symbols.
    :type angle_variable_format: str
    :param dihedral_variable_format: Template for generated dihedral symbols.
    :type dihedral_variable_format: str
    :return: Aligned Z-matrix text with an optional variable block.
    :rtype: str
    """
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
    """
    **LLM Docstring**

    Check that a Z-matrix ordering defines atoms before they are referenced and contains valid row references.

    Embedding entries are normalized first. With reordering allowed, explicit atom labels are mapped to row positions and validation is repeated. The check rejects undefined atom labels, negative atom labels when prohibited, forward references, references larger than the row atom, duplicate indices within a row, and missing nonnegative references beyond the embedding rows.

    :param ordering: Z-matrix ordering rows.
    :type ordering: Sequence[Sequence[int]]
    :param allow_reordering: Permit arbitrary explicit atom labels by remapping them to row order.
    :type allow_reordering: bool
    :param ensure_nonnegative: Require all real atom labels and required references to be nonnegative.
    :type ensure_nonnegative: bool
    :param raise_exception: Raise `ValueError` at the first failed check.
    :type raise_exception: bool
    :param return_reason: Return `(valid, reason)` rather than only a Boolean.
    :type return_reason: bool
    :return: Validation status, optionally paired with the failure explanation.
    :rtype: bool | tuple[bool, str | None]
    """
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
    """
    **LLM Docstring**

    Construct a linear-chain Z-matrix ordering.

    Each atom references the immediately preceding atom for distance, the atom two positions back for angle, and the atom three positions back for dihedral. Negative references naturally provide embedding placeholders for the first rows. An explicit atom sequence is preserved in column 0 while references use earlier entries from that sequence.

    :param n: Number of atoms or explicit atom ordering.
    :type n: int | Sequence[int]
    :return: Four-column chain Z-matrix rows.
    :rtype: list[list[int]]
    """
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
    """
    **LLM Docstring**

    Construct rows whose bond reference is a common center.

    Each generated atom uses `center` as its distance reference. Angle and dihedral references are chosen from earlier generated atoms, with negative embedding placeholders in the first rows.

    :param n: Number of rows to generate.
    :type n: int
    :param center: Common bond-reference index, often a negative attachment placeholder.
    :type center: int
    :return: Four-column center-bound fragment ordering.
    :rtype: list[list[int]]
    """
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

def _get_clean_attachment_refs(attachment_points, zm, order, a):
    """
    **LLM Docstring**

    Find usable external references for attaching a fragment at atom `a`.

    The row for `a` is located in `zm`. Negative references are resolved against nearby entries of `order`; references that are themselves attachment points or already selected are skipped. The resulting list preserves the row's reference priority.

    :param attachment_points: Atom labels reserved as attachment placeholders.
    :type attachment_points: Sequence[int]
    :param zm: Existing Z-matrix rows.
    :type zm: Sequence[Sequence[int]]
    :param order: Atom labels in Z-matrix row order.
    :type order: Sequence[int]
    :param a: Attachment atom whose row supplies candidate references.
    :type a: int
    :return: Distinct non-attachment reference atoms.
    :rtype: list[int]
    """
    main_ref = []
    for m, z in enumerate(zm):
        if z[0] == a:
            _ = []
            for zz in z[1:]:
                if zz < 0:
                    clip_i = max([m + zz, 0])
                    if (
                            (order[clip_i] not in _)
                            and (order[clip_i] not in attachment_points)
                    ):
                        zz = order[clip_i]
                    if zz < 0:
                        clip_i = (m - zz) % len(order)
                        for j in range(clip_i, len(order)):
                            if (
                                    (order[j] not in _)
                                    and (order[j] not in attachment_points)
                            ):
                                zz = order[j]
                                break
                        # else:
                        #     raise ValueError(f"couldn't get attachment point for {attachment_points} in {zm}")
                if zz not in attachment_points:
                    _.append(zz)
            main_ref = _
            break
    return main_ref

def attached_zmatrix_fragment(n, zm, fragment, attachment_points):
    """
    **LLM Docstring**

    Translate a fragment Z-matrix from local indices and negative placeholders into a larger Z-matrix.

    Negative entries index backward through `attachment_points`; nonnegative fragment-local indices are shifted by `n`. Before substitution, negative attachment points are resolved to clean references from the existing Z-matrix when possible.

    :param n: Number of atoms already present; used as the local-index offset.
    :type n: int
    :param zm: Existing Z-matrix used to resolve attachment references.
    :type zm: Sequence[Sequence[int]]
    :param fragment: Fragment rows in local index space.
    :type fragment: Sequence[Sequence[int]]
    :param attachment_points: External atoms replacing `-1`, `-2`, and `-3` placeholders.
    :type attachment_points: Sequence[int]
    :return: Fragment rows expressed in the combined Z-matrix index space.
    :rtype: list[list[int]]
    """
    new_aps = []
    order = [f[0] for f in zm]
    main_ref = None
    for a in attachment_points:
        if a < 0:
            if main_ref is None:
                if len(order) >= (-a):
                    main_ref = _get_clean_attachment_refs(attachment_points, zm, order, a)
            if len(main_ref) > (-a) - 1:
                a = main_ref[(-a) - 1]
        elif main_ref is None:
            main_ref = _get_clean_attachment_refs(attachment_points, zm, order, a)
        new_aps.append(a)
    attachment_points = new_aps
    return [
        [attachment_points[-r-1] if r < 0 else n+r for r in row]
        for row in fragment
    ]

def set_zmatrix_embedding(zmat, embedding=None, partial_embedding=False):
    """
    **LLM Docstring**

    Write standard embedding reference values into a Z-matrix ordering.

    The positions are obtained from `zmatrix_embedding_coords(..., array_inds=True)`. Full embedding writes six conventional negative references; partial embedding writes three.

    :param zmat: Z-matrix ordering to copy and modify.
    :type zmat: array-like
    :param embedding: Replacement values in embedding-position order, or standard defaults.
    :type embedding: Sequence[int] | None
    :param partial_embedding: Use the reduced three-entry embedding convention.
    :type partial_embedding: bool
    :return: Integer array with embedding references assigned.
    :rtype: np.ndarray
    """
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
    """
    **LLM Docstring**

    Build a larger Z-matrix by attaching fragments and optional standard substituent patterns.

    `base_zm` and numeric fragment sizes are converted to chain Z-matrices. Each attachment replaces a fragment's negative placeholders with the supplied external references and shifts its local indices. Additional single atoms are attached using available neighboring references; methyl and ethyl positions append fixed three-atom and two-atom patterns. Optional validation is performed after every fragment addition.

    :param base_zm: Existing Z-matrix or atom count for a chain base.
    :type base_zm: int | Sequence[Sequence[int]]
    :param attachments: Mapping or iterable of `(attachment_points, fragment)` pairs.
    :type attachments: dict | Iterable | None
    :param single_atoms: Existing atom labels at which to append individual atoms.
    :type single_atoms: Sequence[int] | None
    :param methyl_positions: Existing atom labels at which to append the implemented three-row methyl pattern.
    :type methyl_positions: Sequence[int] | None
    :param ethyl_positions: Existing atom labels at which to append the implemented two-row ethyl pattern.
    :type ethyl_positions: Sequence[int] | None
    :param validate: Validate the ordering after each explicit fragment attachment.
    :type validate: bool
    :return: Combined four-column Z-matrix ordering.
    :rtype: list[list[int]]
    """
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
        frag = attached_zmatrix_fragment(
            len(zm),
            zm,
            fragment,
            attachment_points
        )
        zm = zm + frag
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
    """
    **LLM Docstring**

    Construct a root fragment with `m` copies of a spoke fragment attached to its terminal atom.

    Integer `root` and `spoke` arguments are expanded as chain Z-matrices. If the root has fewer than three atoms, enough spoke atoms are first incorporated to establish three usable references. Remaining spokes are attached through the root terminal and two selected neighboring references.

    :param m: Number of spoke copies to attach, reduced by any copies consumed to complete a short root.
    :type m: int
    :param spoke: Spoke fragment ordering or atom count for a chain spoke.
    :type spoke: int | Sequence[Sequence[int]]
    :param root: Root fragment ordering or atom count for a chain root.
    :type root: int | Sequence[Sequence[int]]
    :return: Combined spoke-style Z-matrix.
    :rtype: list[list[int]]
    """
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
    """
    **LLM Docstring**

    Replace every nonnegative atom index in a Z-matrix using `perm`.

    Negative embedding and attachment placeholders are preserved unchanged.

    :param zm: Z-matrix rows to remap.
    :type zm: Sequence[Sequence[int]]
    :param perm: Indexable mapping from old labels to new labels.
    :type perm: Mapping | Sequence[int]
    :return: Reindexed rows.
    :rtype: list[list[int]]
    """
    return [
        [perm[r] if r >= 0 else r for r in row]
        for row in zm
    ]

def canonicalize_zmatrix(zm):
    """
    **LLM Docstring**

    Convert a Z-matrix to row-index space while preserving its explicit atom ordering.

    A three-column ordering is promoted to four columns with an implicit atom column. The original atom labels are returned as `z_vec`; all nonnegative entries are then replaced by their row positions.

    :param zm: Three- or four-column Z-matrix ordering.
    :type zm: Sequence[Sequence[int]]
    :return: Original atom-label vector and equivalent row-indexed Z-matrix.
    :rtype: tuple[np.ndarray, list[list[int]]]
    """
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
    """
    **LLM Docstring**

    Complete a three-reference attachment specification `(bond, angle, dihedral)`.

    Supplied positions are retained. Missing positions are chosen from graph neighbors while avoiding already selected references; when no suitable graph neighbor exists, nearby numeric indices are used as deterministic fallbacks. References selected through the graph are translated through `ind_mapping` when provided.

    :param i_pos: One to three known attachment references, or a single bond reference.
    :type i_pos: int | Sequence[int | None]
    :param graph: Optional graph whose adjacency map is used to choose chemically connected references.
    :type graph: EdgeGraph | None
    :param ind_mapping: Mapping applied only to references selected from `graph`.
    :type ind_mapping: Mapping | None
    :return: Complete `(bond_reference, angle_reference, dihedral_reference)` tuple.
    :rtype: tuple[int, int, int]
    """
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
    """
    **LLM Docstring**

    Recursively add atoms connected by `bonds` but absent from a partial Z-matrix.

    The input is canonicalized to row-index space. For each bond crossing from an included atom to an excluded atom, all newly reachable atoms are appended as a center-bound fragment attached to the included atom. The combined ordering is mapped back to original atom labels and the procedure repeats until no crossing bonds remain or `max_iterations` is exhausted.

    :param base_zmat: Partial Z-matrix ordering.
    :type base_zmat: Sequence[Sequence[int]]
    :param bonds: Full bond list in original atom-label space.
    :type bonds: Sequence[tuple[int, int]]
    :param max_iterations: Maximum recursive expansion depth, or no limit.
    :type max_iterations: int | None
    :param validate_additions: Validate before canonicalization, after attachment, and after reindexing.
    :type validate_additions: bool
    :return: Expanded Z-matrix and a mapping from included attachment atoms to atoms discovered from them.
    :rtype: tuple[list[list[int]], dict[int, list[int]]]
    """
    if validate_additions and not validate_zmatrix(base_zmat):
        is_valid, reason = validate_zmatrix(base_zmat, return_reason=True)
        if not is_valid:
            raise ValueError(f"invalid initial zmat ({reason} in {base_zmat})")
    atoms, zm = canonicalize_zmatrix(base_zmat)
    if validate_additions and not validate_zmatrix(zm):
        is_valid, reason = validate_zmatrix(zm, return_reason=True)
        if not is_valid:
            raise ValueError(f"invalid after canonicalization zmat ({reason} in {zm})")
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
            mods,
            validate=validate_additions
        )
        if validate_additions and not validate_zmatrix(new_zm):
            is_valid, reason = validate_zmatrix(new_zm, return_reason=True)
            if not is_valid:
                raise ValueError(f"invalid zmatrix after functionalization ({reason}) in adding {mods} to {new_zm}")
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
    """
    **LLM Docstring**

    Represent Z-matrix parent references as a bidirectional tree-like mapping.

    For row `n`, only the first `n` nonnegative reference columns are considered defined. Each atom records its ordered parent tuple, and every parent records the atom in an unordered `children` set.

    :param zm: Four-column Z-matrix ordering.
    :type zm: Sequence[Sequence[int]]
    :return: Mapping from atom label to `{'parents': tuple, 'children': set}`.
    :rtype: dict[int, dict]
    """
    graph = {}
    for n,(i,j,k,l) in enumerate(zm):
        i = int(i)
        parents = tuple(int(x) for x in (j, k, l)[:n] if x >= 0)
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

def zmatrix_adjacency_matrix(zm, child_type='multi', penalty_atoms=None):
    """
    **LLM Docstring**

    Build a directed parent-to-child adjacency matrix from a Z-matrix tree.

    Atoms are ordered by parent count, except `penalty_atoms`, which are sorted as though they had six parents. In `single` mode only the first, bond-defining parent creates an edge; in `multi` mode every parent-child relationship does.

    :param zm: Z-matrix rows or a mapping produced by `make_zmatrix_tree`.
    :type zm: Sequence | dict
    :param child_type: `single` for bond-parent edges only, otherwise all parent edges.
    :type child_type: str
    :param penalty_atoms: Atoms forced toward the end of the matrix ordering.
    :type penalty_atoms: Collection[int] | None
    :return: Atom labels in matrix order and their Boolean adjacency matrix.
    :rtype: tuple[list[int], np.ndarray]
    """
    adj_mat = np.zeros((len(zm),len(zm)), dtype=bool)
    if not isinstance(zm, dict):
        zm = make_zmatrix_tree(zm)
    zm_atoms = sorted(zm.keys(),
                      key=lambda x: len(zm[x]['parents']) if penalty_atoms is None or x not in penalty_atoms else 6)
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

def zmatrix_from_tree(zm, check_cycles=True, chain_order=None, check_unique_root=True, base_order=None):
    """
    **LLM Docstring**

    Convert a parent/children mapping back into ordered four-column Z-matrix rows.

    The optional checks require one root, then rows with one and two parents, and reject strongly connected components that indicate parent cycles. Without an explicit order, depth-first traversals of the bond-parent graph score atoms so the root and first two embedding atoms appear first. With `base_order`, atoms are appended only after all their parents have appeared. Missing parent columns are filled with standard negative placeholders.

    :param zm: Mapping from atom labels to ordered parents and children.
    :type zm: dict
    :param check_cycles: Reject cycles in the full parent graph.
    :type check_cycles: bool
    :param chain_order: Explicit output atom order.
    :type chain_order: Sequence[int] | None
    :param check_unique_root: Validate the zero-, one-, and two-parent embedding rows.
    :type check_unique_root: bool
    :param base_order: Preferred atom order constrained so parents precede children.
    :type base_order: Sequence[int] | None
    :return: Four-column Z-matrix rows.
    :rtype: list[list[int]]
    """
    if check_unique_root:
        zm_atoms = sorted(zm.keys(), key=lambda x: len(zm[x]['parents']))
        if len(zm[zm_atoms[0]]['parents']) != 0:
            raise ValueError(f"root atom ({zm_atoms[0]}) has wrong number of parents in {zm_atoms}, got {len(zm[zm_atoms[0]]['parents'])}")
        if len(zm) > 1 and len(zm[zm_atoms[1]]['parents']) != 1:
            raise ValueError(f"first child atom ({zm_atoms[1]}) has wrong number of parents in {zm_atoms}, got {len(zm[zm_atoms[1]]['parents'])}")
        if len(zm) > 2 and len(zm[zm_atoms[2]]['parents']) != 2:
            raise ValueError(f"second child atom ({zm_atoms[2]}) has wrong number of parents in {zm_atoms}, got {len(zm[zm_atoms[2]]['parents'])}")

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

        if base_order is None:
            #TODO: try to ensure this is the longest chain
            zm_atoms, zm_adj_mat = zmatrix_adjacency_matrix(zm, child_type='single')
            g = spg.csr_matrix(zm_adj_mat)
            chain_order, _ = spg.csgraph.depth_first_order(g, 0)
            chain_order:list[int] = [zm_atoms[c] for c in chain_order]
            scores = {a:2 for a in chain_order}
            scores[chain_order[0]] = -3
            if len(zm_atoms) > 1:
                g = g[1:, 1:]
                chain_order1, _ = spg.csgraph.depth_first_order(g, 0)
                chain_order1 = [zm_atoms[c + 1] for c in chain_order1]
                for a in chain_order1:
                    scores[a] = 1
                scores[chain_order1[0]] = -2

                if len(zm_atoms) > 2:
                    g = g[1:, 1:]
                    chain_order2, _ = spg.csgraph.depth_first_order(g, 0)
                    chain_order2 = [zm_atoms[c + 2] for c in chain_order2]
                    for a in chain_order2:
                        scores[a] = 0
                    scores[chain_order2[0]] = -1
            chain_order = sorted(chain_order, key=lambda x: scores[x])

        else:
            zm_atoms0 = sorted(zm.keys(), key=lambda x: len(zm[x]['parents']))
            chain_order = [zm_atoms0[0]]
            rem = list(base_order)
            rem.remove(chain_order[0])
            while rem:
                for i,a in enumerate(rem):
                    p = zm[a]['parents']
                    if all(pp in chain_order for pp in p):
                        break
                else:
                    print(chain_order)
                    print(
                        {a:zm[a]['parents'] for a in rem}
                    )
                    raise ValueError("couldn't add any atoms to tree based on base order?")
                chain_order.append(a)
                rem.pop(i)

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
    """
    **LLM Docstring**

    Test whether an internal coordinate appears as a contiguous parent prefix in a Z-matrix tree.

    The coordinate is accepted when it starts at its first atom and follows that atom's first `len(coord)-1` parents, or when the reversed coordinate follows the final atom's parent prefix.

    :param zm: Tree mapping produced by `make_zmatrix_tree`.
    :type zm: dict
    :param coord: Bond, angle, or dihedral tuple to require.
    :type coord: Sequence[int]
    :return: `(row_atom, full_parent_tuple)` for the matching orientation, otherwise `False`.
    :rtype: tuple | bool
    """
    # if not isinstance(zm, dict): zm = make_zmatrix_tree(zm)
    # coord = tuple(coord)

    n = len(coord) - 1
    p1 = zm[coord[0]]['parents']
    if (coord[0],) + p1[:n] == coord:
        return (coord[0], p1)

    p1 = zm[coord[-1]]['parents']
    if tuple(reversed(p1[:n])) + (coord[-1],) == coord:
        return (coord[-1], p1)

    return False

def _adjust_zm_parents(zm, i, new, constraint_map, validate=False):
    """
    **LLM Docstring**

    Attempt to replace one atom's parent tuple while preserving all registered coordinate constraints.

    The candidate parents are installed, child sets are updated, and a new bond-parent depth-first order is computed. Parents that would occur after their child are removed and replenished from earlier ancestors or earlier chain atoms until each row has the required number. The change is committed only if every constraint still matches; otherwise the original tree is restored.

    :param zm: Mutable Z-matrix tree mapping.
    :type zm: dict
    :param i: Atom whose parents are being replaced.
    :type i: int
    :param new: Candidate ordered parent tuple.
    :type new: tuple[int, ...]
    :param constraint_map: Existing coordinate constraints that must remain representable.
    :type constraint_map: dict
    :param validate: Check generated parent tuples for duplicate atoms.
    :type validate: bool
    :return: Success flag and the committed or restored tree.
    :rtype: tuple[bool, dict]
    """
    backup = {
        o: {'parents':d['parents'], 'children':d['children'].copy()}
        for o, d in zm.items()
    }

    p1 = zm[i]['parents']
    zm[i]['parents'] = new
    if all(
            check_zmatrix_coordinate_constraint(zm, c)
            for c in constraint_map.keys()
    ):
        for o in p1:
            try:
                zm[o]['children'].remove(i)
            except KeyError:
                ...
        for o in new:
            zm[o]['children'].add(i)

        # determine how chain order has changed and re-parent
        # anything that needs tweaks
        zm_atoms, zm_adj_mat = zmatrix_adjacency_matrix(zm, child_type='single')
        g = spg.csr_matrix(zm_adj_mat)
        chain_order, _ = spg.csgraph.depth_first_order(g, 0)
        chain_order: list[int] = [zm_atoms[c] for c in chain_order]
        ord_map = {o: i for i, o in enumerate(chain_order)}
        for z in zm:
            if z not in ord_map: ord_map[z] = len(ord_map)
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
                        if ord_map[pp] < n and pp not in new_parents
                    ]
                    new_parents.extend(add_parents)
                    new_parents = new_parents[:3]
                    if len(new_parents) == 3:
                        break
                else:
                    new_parents.extend(c for c in chain_order[:n + 1] if c not in new_parents)
                    new_parents = new_parents[:3]
            if validate:
                if len(np.unique(new_parents)) < len(new_parents):
                    raise ValueError(o, new_parents)
            for p in new_parents:
                zm[p]['children'].add(o)
            zd['parents'] = tuple(new_parents)

        if all(
                check_zmatrix_coordinate_constraint(zm, c)
                for c in constraint_map.keys()
        ):
            for z,d in zm.items():
                for p in d['parents']:
                    zm[p]['children'].add(z)
            if validate:
                for z, d in zm.items():
                    if len(np.unique(d['parents'])) < len(d['parents']):
                        raise ValueError(z, d)
            return True, zm
        else:
            for o, d in backup.items():
                zm[o] = d
            for o in p1:
                zm[o]['children'].add(i)
            for o in new:
                zm[o]['children'].discard(i)
            zm[i]['parents'] = p1
    else:
        zm[i]['parents'] = p1
    return False, zm

def enforce_required_zmatrix_coordinates(zm,
                                         required_coordinates=None,
                                         root_coordinates=None,
                                         isolated_coordinates=None,
                                         reparent_isolated_coordinates=True,
                                         reparent_root_coordinates=True,
                                         validate=False):  # , chain_order=None):
    """
    **LLM Docstring**

    Reparent a Z-matrix tree so requested bonds, angles, and dihedrals occur as row parent prefixes.

    Already satisfied constraints are retained. Isolated coordinates can first be prevented from serving as references for unrelated rows, and root coordinates can be promoted into the initial embedding chain. Missing required coordinates are then tried in both orientations by replacing candidate parent prefixes through `_adjust_zm_parents`; all previously accepted constraints must remain valid. The result is returned in the same row representation as the input.

    :param zm: Z-matrix rows or tree mapping.
    :type zm: Sequence[Sequence[int]] | dict
    :param required_coordinates: Coordinates that must appear in either orientation.
    :type required_coordinates: Sequence[Sequence[int]] | None
    :param root_coordinates: Coordinates preferentially incorporated into the initial chain.
    :type root_coordinates: Sequence[Sequence[int]] | None
    :param isolated_coordinates: Coordinates whose endpoint atoms should not become unrelated parents.
    :type isolated_coordinates: Sequence[Sequence[int]] | None
    :param reparent_isolated_coordinates: Remove isolated-coordinate endpoints as references where alternatives exist.
    :type reparent_isolated_coordinates: bool
    :param reparent_root_coordinates: Attempt to move root coordinates into the root chain.
    :type reparent_root_coordinates: bool
    :param validate: Enable duplicate-parent and intermediate-tree checks.
    :type validate: bool
    :return: Reparented Z-matrix in the original input representation.
    :rtype: list[list[int]] | dict
    """
    if (
            required_coordinates is None
            and root_coordinates is None
            and isolated_coordinates is None
    ):
        raise ValueError('at least one of `required_coordinates`, `root_coordinates`, and `isolated_coordinates` must not be None')

    coords = []
    if required_coordinates is not None:
        coords.extend(required_coordinates)
    if root_coordinates is not None:
        coords.extend(root_coordinates)
    if isolated_coordinates is not None:
        coords.extend(isolated_coordinates)
    zm_og = zm
    if not isinstance(zm, dict):
        zm = make_zmatrix_tree(zm)
    if validate:
        for z,d in zm.items():
            if len(np.unique(d['parents'])) < len(d['parents']):
                raise ValueError(z, d)

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

    # for all isolated coordinates, we modify the base tree to remove them as parents
    # whenever possible
    if reparent_isolated_coordinates and isolated_coordinates is not None:
        all_ij = set()
        ref_coords = [
            (c[0], c[-1])
            for c in isolated_coordinates
        ]
        # sort isolated coordinates so they share `i` as often as possible
        ref_counts = itut.counts(itertools.chain.from_iterable(ref_coords))
        # we have to ensure that all interior refs are ordered properly
        for n,c in enumerate(isolated_coordinates):
            i, j = c[0], c[-1]
            if ref_counts[i] < ref_counts[j]:
                c = tuple(reversed(c))
                i, j = c[0], c[-1]
            follow_refs = set(sum(ref_coords[n+1:], ())) - {i, j}
            # print(i, j, follow_refs)
            if i not in all_ij:
                p1 = zm[i]['parents']
                c1 = zm[i]['children']
                all_ij.add(i)
                for z, d in zm.items():
                    if z in all_ij: continue
                    pd = d['parents']
                    try:
                        x = pd.index(i)
                    except ValueError:
                        ...
                    else:
                        pp = tuple(
                            p for p in p1 if p not in pd
                        ) + tuple(
                            p for p in c1
                            if p not in pd and p != z
                        )
                        pd = pd[:x] + pp[:1] + pd[x+1:]
                    success, zm = _adjust_zm_parents(zm, z, pd, constraint_map, validate=validate)
                zm_atoms, zm_adj_mat = zmatrix_adjacency_matrix(zm, child_type='single', penalty_atoms=(i, j))
                p1 = c[1:]
                if len(p1) < 3:
                    p1 = p1 + tuple(x for x in reversed(zm_atoms)
                                    if x not in all_ij and x not in c and x not in follow_refs)[:(3 - len(p1))]
                success, zm = _adjust_zm_parents(zm, i, p1, constraint_map, validate=validate)
            if j not in all_ij:
                p2 = zm[j]['parents']
                c2 = zm[j]['children']
                all_ij.add(j)
                for z, d in zm.items():
                    if z in all_ij: continue
                    pd = d['parents']
                    try:
                        x = pd.index(i)
                    except ValueError:
                        ...
                    else:
                        pp = tuple(
                            p for p in p2 if p not in pd
                        ) + tuple(
                            p for p in c2
                            if p not in pd and p != z
                        )
                        pd = pd[:x] + pp[:1] + pd[x + 1:]
                    success, zm = _adjust_zm_parents(zm, z, pd, constraint_map, validate=validate)
                zm_atoms, zm_adj_mat = zmatrix_adjacency_matrix(zm, child_type='single', penalty_atoms=(i, j))
                p2 = c[-2:0:-1]
                if len(p2) < 3:
                    p2 = p2 + tuple(x for x in reversed(zm_atoms)
                                    if x not in all_ij and x not in c and x not in follow_refs)[:(3 - len(p2))]
                success, zm = _adjust_zm_parents(zm, j, p2, constraint_map, validate=validate)

        zm_atoms, zm_adj_mat = zmatrix_adjacency_matrix(zm, child_type='single', penalty_atoms=all_ij)
        success, zm = _adjust_zm_parents(zm, zm_atoms[0], (), constraint_map, validate=validate)
        success, zm = _adjust_zm_parents(zm, zm_atoms[1], (zm_atoms[0],), constraint_map, validate=validate)
        success, zm = _adjust_zm_parents(zm, zm_atoms[2], (zm_atoms[0], zm_atoms[1]), constraint_map, validate=validate)

        # print(zm_atoms)
        # import pprint
        # pprint.pprint(zm)
    if reparent_root_coordinates and root_coordinates is not None:
        all_ij = set()
        ref_coords = [
            (c[0], c[-1])
            for c in root_coordinates
        ]
        # sort coordinates so they share `i` as often as possible
        ref_counts = itut.counts(itertools.chain.from_iterable(ref_coords))
        # find the root ordering by incidence within this group
        root_counts = itut.counts(itertools.chain.from_iterable(c[1:-1] for c in root_coordinates))
        root_ord = sorted(root_counts.keys(), key=lambda x:root_counts[x], reverse=True)
        for n,o in enumerate(root_ord):
            ref_counts[o] = -100 + n

        if len(root_ord) > 0:
            success, zm = _adjust_zm_parents(zm, root_ord[0], (), constraint_map, validate=validate)
        if len(root_ord) > 1:
            success, zm = _adjust_zm_parents(zm, root_ord[1], (root_ord[0],), constraint_map, validate=validate)
        if len(root_ord) > 2:
            success, zm = _adjust_zm_parents(zm, root_ord[2], (root_ord[0], root_ord[1]), constraint_map, validate=validate)

        for n,c in enumerate(root_coordinates):
            i, j = c[0], c[-1]
            if ref_counts[i] < ref_counts[j]:
                c = tuple(reversed(c))
                i, j = c[0], c[-1]
            follow_refs = set(sum(ref_coords[n+1:], ())) - {i, j}
            if i not in all_ij:
                all_ij.add(i)
                p1 = c[1:]
                if len(p1) < 3:
                    p1 = p1 + tuple(x for x in reversed(root_ord)
                                    if x not in all_ij and x not in c and x not in follow_refs)[:(3 - len(p1))]
                success, zm = _adjust_zm_parents(zm, i, p1, constraint_map, validate=validate)
            if j not in all_ij:
                all_ij.add(j)
                p2 = c[-2:0:-1]
                if len(p2) < 3:
                    p2 = p2 + tuple(x for x in reversed(root_ord)
                                    if x not in all_ij and x not in c and x not in follow_refs)[:(3 - len(p2))]
                success, zm = _adjust_zm_parents(zm, j, p2, constraint_map, validate=validate)

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
            rem = np.setdiff1d(np.arange(len(p1)), x)
            p1 = tuple(p1[z] for z in np.concatenate([x, rem]))
            zm[i]['parents'] = p1
            if validate and len(np.unique(p1)) < len(p1): raise ValueError(p1)
            constraint_map[m] = (i, p1)
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
            rem = np.setdiff1d(np.arange(len(p2)), x)
            p2 = tuple(p2[z] for z in np.concatenate([x, rem]))
            if validate and len(np.unique(p2)) < len(p2): raise ValueError(p2)
            zm[j]['parents'] = p2
            constraint_map[m] = (j, p2)
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
            new1 = (j,) + refs
            if len(new1) < len(p1):
                new1 = new1 + p1[:len(p1) - len(new1)]

            refs = zm[i]['parents'][:2]
            p2 = zm[j]['parents']
            new2 = (i,) + refs
            if len(new2) < len(p2):
                new2 = new2 + p2[:len(p2) - len(new2)]

            ref_choices = [new1, new2]
        elif len(m) == 3:
            parents = [x for x in zm[j]['parents'] if x not in m]
            p1 = [p for p in zm[i]['parents'] if p not in m]
            if len(parents) > 0:
                new1 = list(m[1:]) + parents[-1:]
            else:
                new1 = list(m[1:]) + p1[:1]


            parents = [x for x in zm[i]['parents'] if x not in m]
            p2 = [p for p in zm[j]['parents'] if p not in m]
            if len(parents) > 0:
                new2 = parents[-1:] + list(reversed(m[:-1]))
            else:
                new2 = p2[:1] + list(reversed(m[:-1]))

            ref_choices = [tuple(new1), tuple(new2)]
        else:
            ref_choices = [m[1:], tuple(reversed(m[:-1]))]

        # check that we haven't broken any constraints
        # TODO: write targeted loops
        success, zm = _adjust_zm_parents(zm, i, ref_choices[0], constraint_map, validate=validate)
        if success:
            if validate:
                d = zm[i]
                if len(np.unique(d['parents'])) < len(d['parents']):
                    raise ValueError(i, d)
            if (i in ref_choices[0]): raise ValueError(i, ref_choices[0])
            constraint_map[m] = (i, ref_choices[0])
            continue

        success, zm = _adjust_zm_parents(zm, j, ref_choices[1], constraint_map, validate=validate)
        if success:
            if validate:
                d = zm[j]
                if len(np.unique(d['parents'])) < len(d['parents']):
                    raise ValueError(j, d)
            if (j in ref_choices[1]): raise ValueError(j, ref_choices[1])
            constraint_map[m] = (j, ref_choices[1])
            continue

        raise ValueError(f"couldn't satisfy constraint {m} in {coords}")

    if validate:
        for c, (u,v) in constraint_map.items():
            v = (u,) + v
            if len(np.unique(v)) < len(v):
                raise ValueError(c, v)

    if not isinstance(zm_og, dict):
        base_order = [z[0] for z in zm_og]
        scores = {z:0 for z in base_order}
        if isolated_coordinates is not None: # sort base order to isolate key terms
            for c in isolated_coordinates:
                for z,d in zm.items():
                    if (
                            (z == c[0] and all(cc in d['parents'] for cc in c[1:]))
                            or (z == c[-1] and all(cc in d['parents'] for cc in c[:-1]))
                    ):
                        scores[z] += 1
        if root_coordinates is not None: # sort base order to isolate key terms
            for c in root_coordinates:
                for z,d in zm.items():
                    if (
                            (z == c[0] and all(cc in d['parents'] for cc in c[1:]))
                            or (z == c[-1] and all(cc in d['parents'] for cc in c[:-1]))
                    ):
                        scores[z] -= 1
        base_order = sorted(base_order, key=lambda x: scores[x])
        if validate:
            for z, d in zm.items():
                if len(np.unique(d['parents'])) < len(d['parents']):
                    raise ValueError(z, d)
        zm = zmatrix_from_tree(zm, base_order=base_order)
        if validate:
            is_valid, reason = validate_zmatrix(zm, return_reason=True)
            if not is_valid:
                zm = np.array(zm)
                raise ValueError(f"after coordinate enforcement zmatrix invalid ({reason}) in {zm}")

            zcs = zmatrix_indices(zm, coords)

    return zm


def bond_graph_zmatrix(
        bonds,
        fragments,
        edge_map=None,
        reindex=True,
        validate_additions=True,
        required_coordinates=None,
        isolated_coordinates=None,
        root_coordinates=None,
        enforce_requirements=True
):
    """
    **LLM Docstring**

    Construct a Z-matrix spanning a bonded graph, including disconnected or fused fragments.

    Fragments and an edge map are obtained from the supplied `EdgeGraph` or bond list. Provided backbone fragments are fused first; missing graph fragments receive submatrices and are attached through graph edges. The combined local ordering is reindexed to original atom labels. Optional required, root, and isolated coordinates are enforced after assembly.

    :param bonds: Bond pairs or an `EdgeGraph` describing molecular connectivity.
    :type bonds: Sequence[tuple[int, int]] | EdgeGraph
    :param fragments: Optional atom-index fragments; inferred from the graph when omitted.
    :type fragments: Sequence[Sequence[int]] | None
    :param submats: Optional Z-matrix ordering for each fragment.
    :type submats: Sequence[Sequence[Sequence[int]]] | None
    :param backbone: Optional initial atom ordering or fragment backbone.
    :type backbone: Sequence | None
    :param edge_map: Precomputed adjacency mapping.
    :type edge_map: dict | None
    :param reindex: Map the assembled local ordering back to original atom labels.
    :type reindex: bool
    :param validate_additions: Validate intermediate fragment attachments.
    :type validate_additions: bool
    :param required_coordinates: Coordinates that must be represented after assembly.
    :type required_coordinates: Sequence | None
    :param isolated_coordinates: Coordinates to keep isolated from unrelated parent references.
    :type isolated_coordinates: Sequence | None
    :param root_coordinates: Coordinates to place near the root chain.
    :type root_coordinates: Sequence | None
    :param enforce_requirements: Apply coordinate reparenting after graph assembly.
    :type enforce_requirements: bool
    :return: Z-matrix ordering spanning the graph.
    :rtype: list[list[int]]
    """
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
    fragment_scoring = {}
    if isolated_coordinates is not None:
        for c in isolated_coordinates:
            i,j = c[0], c[-1]
            fragment_scoring[i] = fragment_scoring.get(i, 0) + 1
            fragment_scoring[j] = fragment_scoring.get(j, 0) + 1
            for x in c[1:-1]:
                fragment_scoring[x] = fragment_scoring.get(x, 0) + .1


    if root_coordinates is not None:
        for c in root_coordinates:
            i,j = c[0], c[-1]
            fragment_scoring[i] = fragment_scoring.get(i, 0) - 1
            fragment_scoring[j] = fragment_scoring.get(j, 0) - 1
            for x in c[1:-1]:
                fragment_scoring[x] = fragment_scoring.get(x, 0) - .1

    backbone = sorted(backbone, key=lambda x: fragment_scoring.get(x, 0))
    while len(fragments) > 0:
        attachment_points = {}
        missing_frags = []
        missing_mats = []
        added_frags = []
        for frag,mat in zip(fragments, submats):
            base_frag = frag
            if not nput.is_int(frag[0]):
                frag = frag[0]

            frag = sorted(frag, key=lambda x: fragment_scoring.get(x, 0))
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

    if (
            enforce_requirements and
            (required_coordinates is not None
             or isolated_coordinates is not None
             or root_coordinates is not None)
    ):
        fused = enforce_required_zmatrix_coordinates(fused,
                                                     required_coordinates,
                                                     isolated_coordinates=isolated_coordinates,
                                                     root_coordinates=root_coordinates,
                                                     validate=validate_additions)
    return fused

def canonical_fragment_zmatrix(canonical_framents, validate_additions=False):
    """
    **LLM Docstring**

    Join preordered atom fragments into one canonical Z-matrix.

    Each fragment is represented by a chain Z-matrix. The first fragment becomes the backbone; every later fragment is attached to the previous combined ordering using up to the last three existing atom positions as external references. The final local rows are reindexed to the concatenated original fragment labels.

    :param canonical_framents: Atom-index fragments in the desired fragment and intra-fragment order.
    :type canonical_framents: Sequence[Sequence[int]]
    :param validate_additions: Validate the local and reindexed combined ordering.
    :type validate_additions: bool
    :return: Combined Z-matrix in original atom-label space.
    :rtype: list[list[int]]
    """
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
    """
    **LLM Docstring**

    Orient and order complex-fragment attachment records into a connected fragment traversal.

    Attachment endpoints are associated with the fragments containing them. Starting from `start_frag` when supplied, the routine repeatedly selects attachments that connect the current fragment to an unvisited fragment, reversing endpoint order when necessary. It returns fragments in traversal order together with attachment references keyed by the newly reached fragment.

    :param fragment_inds: Atom indices for each disconnected fragment.
    :type fragment_inds: Sequence[Sequence[int]]
    :param attachment_points: Mapping or iterable describing atom-level links between fragments.
    :type attachment_points: dict | Iterable
    :param start_frag: Optional fragment index from which to begin traversal.
    :type start_frag: int | None
    :return: Reordered fragments and attachment specifications for joining them.
    :rtype: tuple[list[tuple[int, ...]], dict]
    """
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
        required_coordinates=None,
        isolated_coordinates=None,
        root_coordinates=None,
        validate_additions=True
):
    """
    **LLM Docstring**

    Assemble a Z-matrix for multiple disconnected fragments using explicit or distance-derived attachment points.

    Fragments are inferred from the bond graph when needed and each receives a supplied or generated Z-matrix. Attachments are sorted into a connected traversal. When an attachment is absent, the closest interfragment atom pair is selected from `distance_matrix`; `_attachment_point` supplies the remaining angle and dihedral references from the graph. Fragments are appended with `functionalized_zmatrix`, optionally reindexed to original atoms, validated, and reparented to satisfy requested coordinates.

    :param bonds: Bond list used to construct the graph when `graph` is omitted.
    :type bonds: Sequence[tuple[int, int]] | None
    :param fragment_inds: Atom indices for each fragment.
    :type fragment_inds: Sequence[Sequence[int]] | None
    :param fragment_zmats: Z-matrix ordering for each fragment.
    :type fragment_zmats: Sequence | None
    :param distance_matrix: Pairwise distances used to choose closest attachment atoms.
    :type distance_matrix: np.ndarray | None
    :param attachment_points: Explicit interfragment attachment specifications.
    :type attachment_points: dict | Sequence | None
    :param check_attachment_points: Validate that attachment references belong to the appropriate fragments.
    :type check_attachment_points: bool
    :param graph: Connectivity graph used for fragments and neighboring references.
    :type graph: EdgeGraph | None
    :param reindex: Return rows in original atom-label space.
    :type reindex: bool
    :param required_coordinates: Coordinates required in the final ordering.
    :type required_coordinates: Sequence | None
    :param isolated_coordinates: Coordinates protected from unrelated parent usage.
    :type isolated_coordinates: Sequence | None
    :param root_coordinates: Coordinates preferentially placed at the root.
    :type root_coordinates: Sequence | None
    :param validate_additions: Validate fragment assembly and final ordering.
    :type validate_additions: bool
    :return: Combined complex Z-matrix.
    :rtype: list[list[int]]
    """
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

    if (
            required_coordinates is not None
            or isolated_coordinates is not None
            or root_coordinates is not None
    ):
        zm = enforce_required_zmatrix_coordinates(zm,
                                                  required_coordinates,
                                                  isolated_coordinates=isolated_coordinates,
                                                  root_coordinates=root_coordinates,
                                                  validate=validate_additions)

    return zm

def graph_backbone_zmatrix(bond_graph: EdgeGraph,
                     root=None, segments=None, return_remainder=False, return_segments=False,
                     validate=True
                     ):
    """
    **LLM Docstring**

    Create a Z-matrix backbone from chain segments of a connectivity graph.

    The graph is segmented into chains, optionally relative to a chosen root. Each segment is converted to a chain Z-matrix and the segments are joined through `canonical_fragment_zmatrix` or `complex_zmatrix` according to the available connectivity. Depending on requested flags, the function also returns segment or graph metadata alongside the ordering.

    :param bond_graph: Connectivity graph to segment.
    :type bond_graph: EdgeGraph
    :param root: Preferred root atom for chain segmentation.
    :type root: int | None
    :param validate: Validate fragment joins.
    :type validate: bool
    :param return_segments: Include the chain segments in the result.
    :type return_segments: bool
    :param return_graph: Include the graph in the result.
    :type return_graph: bool
    :return: Z-matrix, optionally followed by segments and graph metadata.
    :rtype: tuple | list[list[int]]
    """
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
    """
    **LLM Docstring**

    Construct a complex Z-matrix by building graph-based backbones for each disconnected fragment.

    Disconnected graph fragments are identified first. A single fragment is delegated to `graph_backbone_zmatrix`; multiple fragments are processed recursively to obtain local backbones, then joined with `complex_zmatrix` using graph connectivity, optional distances, and attachment specifications. Optional metadata is propagated with the final ordering.

    :param bond_graph: Connectivity graph, possibly containing multiple fragments.
    :type bond_graph: EdgeGraph
    :param root: Preferred root atom or fragment root.
    :type root: int | None
    :param distance_matrix: Pairwise distances used to connect disconnected fragments.
    :type distance_matrix: np.ndarray | None
    :param attachment_points: Explicit links between fragments.
    :type attachment_points: dict | Sequence | None
    :param validate: Validate each local and combined ordering.
    :type validate: bool
    :param return_segments: Include segment information in the result.
    :type return_segments: bool
    :param return_graph: Include graph metadata in the result.
    :type return_graph: bool
    :return: Combined Z-matrix, optionally with segment and graph metadata.
    :rtype: tuple | list[list[int]]
    """
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
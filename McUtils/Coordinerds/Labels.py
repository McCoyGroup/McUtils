import numpy as np
import itertools
from collections import namedtuple
from ..Data import UnitsData
from .. import Numputils as nput
from .. import Devutils as dev
from .Internals import InternalCoordinateType

__all__ = [
    "coordinate_label",
    "get_coordinate_label",
    "mode_label",
    "get_mode_labels",
    "coordinate_sorting_key",
    "sort_internal_coordinates",
    # "print_mode_labels"
]

atom_sort_order = ['C', 'O', 'N', 'H', 'D', 'F', 'Cl', 'Br', 'I']
coordinate_label = namedtuple('coordinate_label', ['ring', 'group', 'atoms', 'type'])
def get_coordinate_label(coord, atom_labels, atom_order=None):
    """
    **LLM Docstring**

    Build a structured label describing the chemical motif and optional ring/group membership of an internal coordinate.

    Distance, bend, and dihedral coordinates are recognized either from an explicit tag or from integer tuples of length two, three, or four. Endpoint atom symbols are oriented canonically according to `atom_order`; bends and dihedrals may therefore be reversed. A ring or group label is retained only when the participating atoms satisfy the function's shared-membership rules. Unrecognized coordinates are labeled by concatenating the atom symbols in their supplied order (or across nested coordinate tuples).

    :param coord: Coordinate specification. It may be an atom-index tuple, a one-entry `{coordinate: tag}` mapping, or a string tag paired through the function's string-swapping convention.
    :type coord: tuple | dict | str
    :param atom_labels: Per-atom records exposing `atom`, `ring`, and `group` attributes.
    :type atom_labels: collections.abc.Sequence
    :param atom_order: Atom-symbol precedence used to orient endpoint-equivalent coordinates. A sequence is converted to a symbol-to-rank mapping.
    :type atom_order: collections.abc.Sequence[str] | dict[str, int] | None
    :return: `(ring, group, atoms, type)` label for the coordinate.
    :rtype: coordinate_label
    """
    ring_lab = None
    group_lab = None
    # motif_lab = ""
    tag = None
    if atom_order is None:
        atom_order = atom_sort_order
    if not isinstance(atom_order, dict):
        atom_order = {a:i for i,a in enumerate(atom_order)}

    ## TODO: use new infrastrcture for labels
    # coord = InternalCoordinateType.resolve(coord)
    if isinstance(coord, dict):
        coord, tag = next(iter(coord.items()))
    if isinstance(coord, str):
        tag, coord = coord, tag
    if dev.str_is(tag, 'dist') or (tag is None and nput.is_int(coord[0]) and len(coord) == 2):
        if tag is None:
            tag = "stretch"

        a,b = coord
        atom_1 = atom_labels[a]
        atom_2 = atom_labels[b]
        r1 = atom_1.ring
        r2 = atom_2.ring
        if r1 is not None:
            if r2 is None or r1 == r2:
                ring_lab = r1
        elif r2 is not None:
            if r1 is None:
                ring_lab = r2

        g1 = atom_1.group
        g2 = atom_2.group
        if g1 is not None:
            if g2 is None or g1 == g2:
                group_lab = g1
        elif g2 is not None:
            if g1 is None:
                ring_lab = g2

        a1 = atom_1.atom
        a2 = atom_2.atom
        a,b = sorted([a1,a2], key=lambda c:atom_order.get(c, len(atom_order)))
        motif_lab = a+b

    elif dev.str_is(tag, 'bend') or (tag is None and nput.is_int(coord[0]) and len(coord) == 3):
        if tag is None:
            tag = "bend"

        a,b,c = coord
        atom_1 = atom_labels[a]
        atom_2 = atom_labels[b]
        atom_3 = atom_labels[c]

        r1 = atom_1.ring
        r2 = atom_2.ring
        r3 = atom_3.ring
        if (
                r1 is not None and r2 is not None and r3 is not None
                and r1 == r2 and r1 == r3 and r2 == r3
        ):
            ring_lab = r1

        g1 = atom_1.group
        g2 = atom_2.group
        g3 = atom_3.group
        if (
                g1 is not None and g2 is not None and g3 is not None
                and g1 == g2 and g1 == g3 and g2 == g3
        ):
            group_lab = g1

        a1 = atom_1.atom
        a2 = atom_2.atom
        a3 = atom_3.atom
        if atom_order.get(a1, len(atom_order)) > atom_order.get(a3, len(atom_order)):
            a1, a2, a3 = a3, a2, a1
        motif_lab = a1 + a2 + a3
    elif dev.str_is(tag, 'dihed') or (tag is None and nput.is_int(coord[0]) and len(coord) == 4):
        if tag is None:
            tag = "dihedral"

        a, b, c, d = coord
        atom_1 = atom_labels[a]
        atom_2 = atom_labels[b]
        atom_3 = atom_labels[c]
        atom_4 = atom_labels[d]

        rings = [atom_1.ring, atom_2.ring, atom_3.ring, atom_4.ring]
        if (
            all(r is not None for r in rings)
            and all(r1 == r2 for r1,r2 in itertools.combinations(rings, 2))
        ):
            ring_lab = rings[0]

        groups = [atom_1.group, atom_2.group, atom_3.group, atom_4.group]
        if (
                all(r is not None for r in groups)
                and all(r1 == r2 for r1, r2 in itertools.combinations(groups, 2))
        ):
            group_lab = groups[0]

        a1 = atom_1.atom
        a2 = atom_2.atom
        a3 = atom_3.atom
        a4 = atom_4.atom
        if atom_order.get(a1, len(atom_order)) > atom_order.get(a4, len(atom_order)):
            a1, a2, a3, a4 = a4, a3, a2, a1
        motif_lab = a1 + a2 + a3 + a4
    else:
        if nput.is_int(coord[0]):
            motif_lab = "".join(atom_labels[i].atom for i in coord)
        else:
            motif_lab = "".join(atom_labels[i].atom for c in coord for i in c)

    return coordinate_label(ring_lab, group_lab, motif_lab, tag)

coord_type_ordering = {'stretch': 0, 'bend': 1, 'dihedral': 2}
atom_coordinate_sort_order = ['H', 'D', 'O', 'N', 'F', 'Cl', 'Br', 'I', 'C']
def coordinate_sorting_key(label, type_ordering=None, atom_ordering=None):
    """
    **LLM Docstring**

    Construct a sortable tuple that orders coordinates first by type and then by their constituent atom symbols.

    Plain strings are interpreted as atom-symbol motifs and sorted first by motif length. Structured labels use `label.type` and `label.atoms`; unknown coordinate types receive rank `3`, and unknown atoms receive rank `-1`. Atom ranks are sorted internally, so endpoint orientation does not affect the key.

    :param label: Atom-symbol string or structured coordinate label with `type` and `atoms` fields.
    :type label: str | coordinate_label
    :param type_ordering: Mapping from coordinate type names to primary sort ranks.
    :type type_ordering: dict[str, int] | None
    :param atom_ordering: Atom-symbol order, supplied as either a sequence or a rank mapping.
    :type atom_ordering: collections.abc.Sequence[str] | dict[str, int] | None
    :return: Tuple suitable for use as a sorting key.
    :rtype: tuple[int, ...]
    """
    if type_ordering is None:
        type_ordering = coord_type_ordering

    if atom_ordering is None:
        atom_ordering = atom_coordinate_sort_order
    if not hasattr(atom_ordering, 'items'):
        atom_ordering = {a:i for i,a in enumerate(atom_ordering)}

    if isinstance(label, str): # assume it's just atoms
        return (len(label),) + tuple(sorted(atom_ordering.get(a, -1) for a in label))
    else:
        return (type_ordering.get(label.type, 3),) + tuple(sorted(atom_ordering.get(a, -1) for a in label.atoms))
def sort_internal_coordinates(coords, atoms=None, sort_key=None):
    """
    **LLM Docstring**

    Sort internal coordinates or a coordinate-label mapping using a coordinate-aware key.

    When `atoms` is supplied, integer index tuples are converted to concatenated atom-symbol strings before sorting. For mappings, values are sorted and a new insertion-ordered `dict` with the original keys is returned. For other iterables, the sorted coordinates are returned as a tuple.

    :param coords: Coordinate iterable, or mapping whose values are coordinate labels.
    :type coords: collections.abc.Iterable | dict
    :param atoms: Optional atom-symbol sequence used to translate integer coordinate indices.
    :type atoms: collections.abc.Sequence[str] | None
    :param sort_key: Key function; defaults to `coordinate_sorting_key`.
    :type sort_key: collections.abc.Callable | None
    :return: Sorted mapping when `coords` is a dictionary, otherwise a sorted tuple.
    :rtype: dict | tuple
    """
    if sort_key is None:
        sort_key = coordinate_sorting_key
    if atoms is not None:
        sort_key = lambda s: sort_key(
            s
                if not nput.is_int(s[0]) else
            "".join(atoms[i] for i in s)
        )
    if isinstance(coords, dict):
        return dict(
            sorted(coords.items(), key=lambda kv: sort_key(kv[1]))
        )
    else:
        return tuple(
            sorted(coords, key=sort_key)
        )

mode_label = namedtuple("mode_type", ["coefficients", "indices", "labels", "type"])
def get_mode_labels(
        internals,
        internal_modes_by_coords: np.ndarray,
        norm_cutoff=.8
):
    """
    **LLM Docstring**

    Identify the internal coordinates that carry each normal mode and infer their common coordinate type.

    Each column of `internal_modes_by_coords` is treated as one mode. Coordinate contributions are ranked by squared coefficient magnitude, and the shortest leading subset whose coefficient norm exceeds `norm_cutoff` is retained (or all coordinates if the threshold is never reached). The function then compares the retained tags component-by-component and keeps only type fields shared by every contributing coordinate; incompatible fields become `None`, and a fully incompatible mode receives no inferred type.

    :param internals: Coordinate labels, or a mapping from externally meaningful coordinate indices to labels.
    :type internals: collections.abc.Sequence | dict
    :param internal_modes_by_coords: Matrix with coordinates along rows and modes along columns.
    :type internal_modes_by_coords: np.ndarray
    :param norm_cutoff: Euclidean norm threshold used to select the dominant coordinate subset for each mode.
    :type norm_cutoff: float
    :return: One `mode_label(coefficients, indices, labels, type)` record per mode column.
    :rtype: list[mode_label]
    """
    mode_coords = []
    if isinstance(internals, dict):
        indices = list(internals.keys())
        tags = list(internals.values())
    else:
        indices = list(range(len(internals)))
        tags = internals

    tags = [
        t.type
            if (
                hasattr(t, 'type')
                and t.type is not None
                and not isinstance(t.type, str)
            ) else
        t
        for t in tags
    ]

    for mode in internal_modes_by_coords.T:
        ord = np.argsort(-(mode**2))
        sort_mode = mode[ord]
        for i in range(len(mode)):
            sub_mode = sort_mode[:i+1]
            norm = np.linalg.norm(sub_mode)
            if norm > norm_cutoff:
                mode_coords.append(
                    [
                        sub_mode,
                        None if indices is None else [indices[j] for j in ord[:i+1]],
                        [tags[j] for j in ord[:i+1]]
                    ]
                )
                break
        else:
            mode_coords.append([
                sort_mode,
                None
                    if indices is None else
                [indices[j] for j in ord],
                [tags[j] for j in ord]
            ])

    types = []
    for coeffs, inds, tags in mode_coords:
        base_tags = tags[0]
        if isinstance(base_tags, str):
            base_tags = [base_tags]
        # check that no other modes have intruded
        keep = [True] * len(base_tags)
        for t in tags[1:]:
            if isinstance(t, str):
                t = [t]
            s = len(base_tags) - len(t)
            for k in range(s):
                keep[k] = False
            for i in range(len(t)):
                a = base_tags[s+i]
                b = t[i]
                if a is None or b is None or a != b:
                    keep[s+i] = False
        if any(
            kept and (bt is not None)
            for kept, bt in zip(keep, base_tags)
        ):
            subvec = [
                None if not kept else bt
                for kept, bt in zip(keep, base_tags)
            ]
            type_vec = type(base_tags)(*subvec)
        else:
            type_vec = None

        types.append(
            mode_label(coeffs, inds, tags, type_vec)
        )

    return types

# def print_mode_labels(modes, labels):
#     for i, (freq, lab) in enumerate(zip(reversed(modes.freqs), reversed(labels))):
#         print(
#             "Mode {} ({}): {:.0f} {}".format(i + 1,
#                                              len(modes.freqs) - (i+1),
#                                              freq * UnitsData.hartrees_to_wavenumbers,
#                                              "mixed"
#                                              if lab.type is None else
#                                              lab.type
#                                              )
#         )
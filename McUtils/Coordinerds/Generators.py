import numpy as np
import itertools
import collections
from .. import Numputils as nput
from ..Graphs import EdgeGraph
from . import Internals as ints

__all__ = [
    "get_stretch_angles",
    "get_angle_dihedrals",
    "get_angle_stretches",
    "get_dihedral_stretches",
    "get_stretch_angle_dihedrals",
    "get_stretch_coordinate_system",
    "get_fragment_coordinate_system",
    "PrimitiveCoordinatePicker",
    "enumerate_coordinate_sets"
]


def get_stretch_angles(stretches):
    """
    **LLM Docstring**

    Generate every bond angle implied by pairs of stretches that share one atom.

    For each pair of bonds, the shared atom becomes the angle vertex and the two nonshared atoms become the endpoints. Identical stretches are skipped, but the result is not otherwise canonicalized or deduplicated.

    :param stretches: Bond coordinates represented as `(atom_i, atom_j)` pairs.
    :type stretches: collections.abc.Sequence[tuple[int, int]]
    :return: Angle triples `(endpoint_1, vertex, endpoint_2)` implied by the bond list.
    :rtype: list[tuple[int, int, int]]
    """
    angles = []
    for i,(sa,sb) in enumerate(stretches):
        for sc,sd in stretches[i+1:]:
            if sa == sc:
                if sb == sd: continue
                angles.append((sb, sa, sd))
            elif sa == sd:
                if sb == sc: continue
                angles.append((sb, sa, sc))
            elif sb == sc:
                angles.append((sa, sb, sd))
            elif sb == sd:
                angles.append((sa, sb, sc))
    return angles
def get_stretch_angle_dihedrals(stretches, angles):
    """
    **LLM Docstring**

    Extend an angle by a bonded atom to form candidate dihedral coordinates.

    Each stretch is compared with each angle. If both stretch atoms already occur in the angle, it is ignored. If exactly one stretch atom matches any angle position, the other atom is inserted at the corresponding end or adjacent position so the angle remains a contiguous three-atom segment of the resulting four-atom coordinate.

    :param stretches: Bond coordinates as atom-index pairs.
    :type stretches: collections.abc.Iterable[tuple[int, int]]
    :param angles: Angle coordinates as `(a, b, c)` triples.
    :type angles: collections.abc.Iterable[tuple[int, int, int]]
    :return: Candidate four-atom dihedral coordinates.
    :rtype: list[tuple[int, int, int, int]]
    """
    dihedrals = []
    for sa,sb in stretches:
        for ba,bc,bd in angles:
            if sa in (ba,bc,bd) and sb in (ba,bc,bd): continue
            # enumerate for simplicity & avoiding try/except
            if sa == ba:
                dihedrals.append(
                    (sb, ba, bc, bd)
                )
            elif sa == bc:
                dihedrals.append(
                    (ba, sb, bc, bd)
                )
            elif sa == bd:
                dihedrals.append(
                    (ba, bc, bd, sb)
                )
            elif sb == ba:
                dihedrals.append(
                    (sa, ba, bc, bd)
                )
            elif sb == bc:
                dihedrals.append(
                    (ba, sa, bc, bd)
                )
            elif sb == bd:
                dihedrals.append(
                    (ba, bc, bd, sa)
                )
    return dihedrals
def get_angle_stretches(angles):
    """
    **LLM Docstring**

    Expand each angle into its two adjacent bond coordinates.

    :param angles: Angle triples `(a, b, c)`.
    :type angles: collections.abc.Iterable[tuple[int, int, int]]
    :return: Flattened bond list containing `(a, b)` and `(b, c)` for every angle, including duplicates.
    :rtype: list[tuple[int, int]]
    """
    return [
        s
        for a,b,c in angles
        for s in [(a, b), (b, c)]
    ]
def get_dihedral_stretches(dihedrals):
    """
    **LLM Docstring**

    Expand each dihedral into its three adjacent bond coordinates.

    :param dihedrals: Dihedral quadruples `(a, b, c, d)`.
    :type dihedrals: collections.abc.Iterable[tuple[int, int, int, int]]
    :return: Flattened bond list containing `(a, b)`, `(b, c)`, and `(c, d)` for every dihedral, including duplicates.
    :rtype: list[tuple[int, int]]
    """
    return [
        s
        for a,b,c,d in dihedrals
        for s in [(a, b), (b, c), (c,d)]
    ]
def get_angle_dihedrals(angles):
    """
    **LLM Docstring**

    Join compatible pairs of angles across a shared bond to form dihedrals.

    The function recognizes angle pairs whose central bonds coincide after either endpoint orientation. It appends the nonshared endpoint from the second angle to the first angle, or prepends it when the shared bond is reversed. Cases that would repeat the first angle's remaining endpoint are skipped.

    :param angles: Angle triples `(endpoint_1, vertex, endpoint_2)`.
    :type angles: collections.abc.Sequence[tuple[int, int, int]]
    :return: Four-atom dihedral coordinates assembled from compatible angle pairs.
    :rtype: list[tuple[int, int, int, int]]
    """
    dihedrals = []
    for i, (aa, ab, ac) in enumerate(angles):
        for ad, ae, af in angles[i + 1:]:
            if ae == ac:
                if ad == ab:
                    if af == aa: continue
                    dihedrals.append((aa, ab, ac, af))
                elif af == ab:
                    if ad == aa: continue
                    dihedrals.append((aa, ab, ac, ad))
            elif ae == aa:
                if ad == ab:
                    if af == ac: continue
                    dihedrals.append((af, aa, ab, ac))
                elif af == ab:
                    if ad == ac: continue
                    dihedrals.append((ad, aa, ab, ac))
    return dihedrals

def get_stretch_coordinate_system(stretches,
                                  include_bends=True,
                                  include_dihedrals=True):
    """
    **LLM Docstring**

    Construct bends and dihedrals implied by a set of stretches.

    Bends are generated from shared-atom stretch pairs whenever either bends or dihedrals are requested. Dihedrals are then generated by joining the resulting bends. Disabled coordinate classes are represented by `None`, while the original `stretches` object is returned unchanged.

    :param stretches: Bond coordinates used as the connectivity graph.
    :type stretches: collections.abc.Sequence[tuple[int, int]]
    :param include_bends: Whether to include the generated angle list in the result.
    :type include_bends: bool
    :param include_dihedrals: Whether to generate and include dihedral coordinates.
    :type include_dihedrals: bool
    :return: `(stretches, angles, dihedrals)`, with disabled components set to `None`.
    :rtype: tuple
    """
    if include_bends or include_dihedrals:
        angles = get_stretch_angles(stretches)
    else:
        angles = None
    if include_dihedrals:
        dihedrals = get_angle_dihedrals(angles)
    else:
        dihedrals = None
    return stretches,angles,dihedrals

def get_fragment_coordinate_system(bond_graph:EdgeGraph,
                                   fragments=None,
                                   masses=None,
                                   distance_matrix=None):
    """
    **LLM Docstring**

    Choose fragment pairs and describe intermolecular orientation coordinates between them.

    Fragments default to the connected components of `bond_graph`. A single fragment produces no coordinates. With more than two fragments and a distance matrix, each fragment is paired with its nearest other fragment using the minimum inter-fragment atom distance; reciprocal pairs are collapsed. Otherwise adjacent fragments in the supplied order are paired. Each pair is returned as an `orientation` specification, optionally carrying the same `masses` object.

    :param bond_graph: Molecular connectivity graph used to obtain fragments when none are supplied.
    :type bond_graph: EdgeGraph
    :param fragments: Atom-index groups representing disconnected fragments.
    :type fragments: collections.abc.Sequence[collections.abc.Sequence[int]] | None
    :param masses: Optional masses attached to every generated orientation specification.
    :type masses: np.ndarray | None
    :param distance_matrix: Pairwise atom-distance matrix used to connect each fragment to its nearest neighbor when there are more than two fragments.
    :type distance_matrix: np.ndarray | None
    :return: Orientation-coordinate specification dictionaries for selected fragment pairs.
    :rtype: list[dict]
    """
    if fragments is None:
        fragments = bond_graph.get_fragments()
    if len(fragments) == 1: return []
    if len(fragments) > 2 and distance_matrix is not None:
        distance_matrix = np.array(distance_matrix)
        max_dist = np.max(distance_matrix)+1
        np.fill_diagonal(distance_matrix, max_dist)
        intra_frag_dists = {
            (i,j):np.min(distance_matrix[np.ix_(fragments[i], fragments[j])])
            for i,j in itertools.combinations(range(len(fragments)), 2)
        }
        neighbors = [
            min(
                range(len(fragments)),
                key=lambda j:(
                    max_dist
                        if i == j else
                    intra_frag_dists.get((i,j), intra_frag_dists.get((j,i)))
                )
            )
            for i in range(len(fragments))
        ]
        added = set()
        for i,j in enumerate(neighbors):
            if (j,i) in added: continue
            added.add((i,j))
        fragment_pairs = list(added)
    else:
        fragment_pairs = [
            (i,i+1)
            for i in range(len(fragments)-1)
        ]

    return [
        {'orientation':(fragments[i], fragments[j]), 'masses':masses}
            if masses is not None else
        {'orientation':(fragments[i], fragments[j])}
        for i,j in fragment_pairs
    ]


class PrimitiveCoordinatePicker:

    light_atom_types = {"H", "D"}
    def __init__(self, atoms, bonds, base_coords=None, rings=None, fragments=None, light_atoms=None, backbone=None, neighbor_count=3):
        """
        **LLM Docstring**

        Initialize a primitive-coordinate picker from atom labels and molecular connectivity.

        The constructor builds an `EdgeGraph`, discovers rings and connected fragments when they are not supplied, records the ring containing each ring atom, identifies light atoms from `light_atom_types` unless explicitly provided, and stores base coordinates and neighborhood depth. Coordinate generation is deferred until the `coords` property is accessed.

        :param atoms: Atom labels passed to `EdgeGraph`.
        :type atoms: collections.abc.Sequence
        :param bonds: Graph edges passed to `EdgeGraph`.
        :type bonds: collections.abc.Iterable[tuple[int, int]]
        :param base_coords: Coordinates prepended to the automatically generated set.
        :type base_coords: collections.abc.Iterable[tuple[int, ...]] | None
        :param rings: Ordered atom-index cycles; discovered from the graph when omitted.
        :type rings: collections.abc.Sequence | None
        :param fragments: Connected atom-index groups; discovered from the graph when omitted.
        :type fragments: collections.abc.Sequence | None
        :param light_atoms: Explicit light-atom indices. Defaults to graph labels matching `light_atom_types`.
        :type light_atoms: collections.abc.Sequence[int] | None
        :param backbone: Optional preferred backbone passed to chain searches.
        :type backbone: collections.abc.Collection[int] | None
        :param neighbor_count: Neighborhood depth supplied to symmetry-coordinate generation.
        :type neighbor_count: int
        :return: None.
        :rtype: None
        """
        self.graph = EdgeGraph(atoms, bonds)
        if rings is None:
            rings = self.graph.get_rings()
        self.rings = rings
        self.ring_atoms = {k:n for n,rats in enumerate(rings) for k in rats}
        if fragments is None:
            fragments = self.graph.get_fragments()
        self.fragments = fragments
        self.backbone = backbone
        self.light_atoms = (
            [
                i for i, l in enumerate(self.graph.labels)
                if l in self.light_atom_types
            ]
                if light_atoms is None else
            light_atoms
        )
        self.base_coords = list(base_coords) if base_coords is not None else []
        self.neighbors = neighbor_count
        self._coords = None
    @property
    def coords(self):
        """
        **LLM Docstring**

        Return the cached primitive coordinate set, generating it on first access.

        The first call evaluates `generate_coords`, materializes its result as a tuple, and stores it in `_coords`; later calls return the same tuple without regenerating coordinates.

        :return: Cached primitive internal-coordinate specifications.
        :rtype: tuple[tuple[int, ...], ...]
        """
        if self._coords is None:
            self._coords = tuple(self.generate_coords())
        return self._coords
    def generate_coords(self):
        """
        **LLM Docstring**

        Assemble primitive coordinates for rings, fused rings, fragment connections, and non-ring atoms.

        Ring-local bonds, angles, and dihedrals are generated first. Additional coordinates connect every pair of rings and every pair of fragments. For atoms not belonging to any ring, chain-based coordinates are generated from precedent paths. User-supplied base coordinates are prepended, then the combined list is canonicalized and pruned by `prune_excess_coords`.

        :return: Canonicalized primitive coordinate list with duplicate and selected overcomplete coordinates removed.
        :rtype: list[tuple[int, ...]]
        """
        coords = []
        for ring in self.rings:
            coords.extend(self.ring_coordinates(ring))
        for i,r1 in enumerate(self.rings):
            for r2 in self.rings[i+1:]:
                coords.extend(self.fused_ring_coordinates(r1, r2))
        for i,r1 in enumerate(self.fragments):
            for r2 in self.fragments[i+1:]:
                coords.extend(self.fragment_connection_coords(r1, r2))
        for a in range(len(self.graph.labels)):
            if a not in self.ring_atoms:
                symm_c = self.symmetry_coords(a, neighborhood=self.neighbors, backbone=self.backbone)
                coords.extend(symm_c)
        coords = self.base_coords + coords
        return self.prune_excess_coords(coords)

    @classmethod
    def canonicalize_coord(cls, coord):
        """
        **LLM Docstring**

        Normalize an internal coordinate so reversal-equivalent tuples have one orientation.

        Coordinates containing a repeated atom are rejected with `None`. Bonds are ordered by ascending endpoints; angles place the smaller endpoint first; dihedrals are reversed when the first atom exceeds the last; longer tuples use the same endpoint comparison and full reversal.

        :param coord: Internal coordinate atom-index sequence.
        :type coord: collections.abc.Sequence[int]
        :return: Canonical tuple, or `None` when an atom index is repeated.
        :rtype: tuple[int, ...] | None
        """
        dupes = len(np.unique(coord)) < len(coord)
        if dupes: return None
        if len(coord) == 2:
            i,j = coord
            if i > j:
                coord = (j, i)
        elif len(coord) == 3:
            i,j,k = coord
            if i > k:
                coord = (k, j, i)
        elif len(coord) == 4:
            i, j, k, l = coord
            if i > l:
                coord = (l, k, j, i)
        elif coord[0] > coord[-1]:
            coord = tuple(reversed(coord))
        return coord

    @classmethod
    def prep_unique_coords(cls, coords):
        """
        **LLM Docstring**

        Canonicalize coordinates and identify first occurrences, but currently return the original input.

        The method builds `_coords` and `_cache` containing unique canonical coordinates. Those local results are never used in the return statement; as implemented, callers receive `coords` unchanged. This appears inconsistent with the method name and is documented rather than corrected here.

        :param coords: Coordinate iterable to inspect.
        :type coords: collections.abc.Iterable
        :return: The original `coords` object, unchanged.
        :rtype: collections.abc.Iterable
        """
        _coords = []
        _cache = set()
        for x in coords:
            x = cls.canonicalize_coord(x)
            if x not in _cache:
                _coords.append(x)
                _cache.add(x)
        return coords

    @classmethod
    def prune_excess_coords(cls, coord_set, canonicalized=False):
        """
        **LLM Docstring**

        Canonicalize a coordinate set and remove duplicates plus selected redundant angle/dihedral orderings.

        Repeated-atom coordinates are discarded. Exact duplicate tuples are skipped. For four-atom coordinates, only one ordering around a shared central bond is kept when the alternate `(i, k, j, l)` has already appeared. For three-atom coordinates, explicit index-order tests suppress configurations that would retain all three angles among the same atom triple.

        :param coord_set: Candidate internal coordinates.
        :type coord_set: collections.abc.Iterable[collections.abc.Sequence[int]]
        :param canonicalized: Whether every input has already been normalized by `canonicalize_coord`.
        :type canonicalized: bool
        :return: Coordinates retained in first-occurrence order.
        :rtype: list[tuple[int, ...]]
        """
        if not canonicalized:
            coord_set = [cls.canonicalize_coord(c) for c in coord_set]
            coord_set = [c for c in coord_set if c is not None]
        dupe_set = set()
        coords = []
        coord_counts = {}
        for coord in coord_set:
            if coord in dupe_set: continue
            dupe_set.add(coord)
            if len(coord) == 4:
                i,j,k,l = coord
                if (i, k, j, l) in dupe_set: continue
                # only one choice of ordering for shared bond, even though implies different exterior bonds
            elif len(coord) == 3:
                i,j,k = coord
                if ( # can't have all three angles, dealing with the ordering manually
                    (k < j and (i, k, j) in dupe_set and (k, i, j) in dupe_set)
                    or (k > j and (j, i, k) in dupe_set) and ((i, k, j) in dupe_set or (j, k, i) in dupe_set)
                ): continue
            coords.append(coord)
            # key = tuple(sorted(coord))
            # coord_counts[key] = coord_counts.get(key, 0) + 1
            # if len(coord_counts)

        return coords

    @classmethod
    def ring_coordinates(cls, ring_atoms):
        """
        **LLM Docstring**

        Generate cyclic bonds, angles, and dihedrals around an ordered ring.

        The atom list is wrapped at the end. Each atom starts one adjacent bond, one three-consecutive-atom angle, and one four-consecutive-atom dihedral, so a ring of size `n` contributes `3n` coordinates before later pruning.

        :param ring_atoms: Atom indices ordered consecutively around the ring.
        :type ring_atoms: list[int]
        :return: Ring bonds followed by ring angles and ring dihedrals.
        :rtype: list[tuple[int, ...]]
        """
        # ordered as pair-wise bonded

        bonds = list(zip(
            ring_atoms, ring_atoms[1:] + ring_atoms[:1]
        ))
        angles = list(zip(
            ring_atoms, ring_atoms[1:] + ring_atoms[:1], ring_atoms[2:] + ring_atoms[:2]
        ))
        dihedrals = list(zip(
            ring_atoms, ring_atoms[1:] + ring_atoms[:1],
                        ring_atoms[2:] + ring_atoms[:2],
                        ring_atoms[3:] + ring_atoms[:3],
        ))

        return bonds + angles + dihedrals

    fused_ring_dispatch_table = {

    }
    @classmethod
    def _fused_dispatch(cls):
        """
        **LLM Docstring**

        Build the dispatch table for coordinates between rings sharing zero, one, or two atoms.

        Entries in `fused_ring_dispatch_table` are merged over the built-in handlers, allowing subclasses to replace or extend behavior for a given number of shared atoms.

        :return: Mapping from shared-atom count to fused-ring coordinate generator.
        :rtype: dict[int, collections.abc.Callable]
        """
        return dict({
            0:cls.unfused_ring_coordinates,
            1:cls.pivot_fused_ring_coordinates,
            2:cls.simple_fused_ring_coordinates
        }, **cls.fused_ring_dispatch_table)
    @classmethod
    def unfused_ring_coordinates(cls, ring_atoms1, ring_atoms2, shared_atoms, shared_indices1, shared_indices2):
        """
        **LLM Docstring**

        Return no additional coordinates for two rings that share no atoms.

        All arguments are accepted to match the fused-ring dispatch signature and are otherwise unused.

        :param ring_atoms1: First ring's ordered atoms.
        :type ring_atoms1: collections.abc.Sequence[int]
        :param ring_atoms2: Second ring's ordered atoms.
        :type ring_atoms2: collections.abc.Sequence[int]
        :param shared_atoms: Empty shared-atom collection.
        :type shared_atoms: collections.abc.Sequence[int]
        :param shared_indices1: Shared positions in the first ring.
        :type shared_indices1: collections.abc.Sequence[int]
        :param shared_indices2: Shared positions in the second ring.
        :type shared_indices2: collections.abc.Sequence[int]
        :return: Empty coordinate list.
        :rtype: list
        """
        return []
    @classmethod
    def pivot_fused_ring_coordinates(cls, ring_atoms1, ring_atoms2, shared_atoms, shared_indices1, shared_indices2):
        """
        **LLM Docstring**

        Generate four cross-ring angles for rings fused at a single pivot atom.

        For each ring, the atoms immediately before and after the shared pivot are found with cyclic indexing. The Cartesian product of those two neighbor pairs gives four angles centered on the pivot, describing the relative directions of the rings.

        :param ring_atoms1: First ring in cyclic order.
        :type ring_atoms1: collections.abc.Sequence[int]
        :param ring_atoms2: Second ring in cyclic order.
        :type ring_atoms2: collections.abc.Sequence[int]
        :param shared_atoms: One-element sequence containing the pivot atom.
        :type shared_atoms: collections.abc.Sequence[int]
        :param shared_indices1: Pivot position in the first ring.
        :type shared_indices1: collections.abc.Sequence[int]
        :param shared_indices2: Pivot position in the second ring.
        :type shared_indices2: collections.abc.Sequence[int]
        :return: Four cross-ring angle triples centered on the shared atom.
        :rtype: list[tuple[int, int, int]]
        """
        p = shared_atoms[0]
        i = shared_indices1[0]
        n = len(ring_atoms1)
        j = shared_indices2[0]
        m = len(ring_atoms2)

        # add in all relative angles
        ip1 = (i+1) % n
        jp1 = (j+1) % m
        return [
            (ring_atoms1[i-1], p, ring_atoms2[j-1]),
            (ring_atoms1[ip1], p, ring_atoms2[j-1]),
            (ring_atoms1[i-1], p, ring_atoms2[jp1]),
            (ring_atoms1[ip1], p, ring_atoms2[jp1])
        ]

    @classmethod
    def simple_fused_ring_coordinates(cls, ring_atoms1, ring_atoms2, shared_atoms, shared_indices1, shared_indices2):
        """
        **LLM Docstring**

        Generate two cross-ring dihedrals for rings sharing one bond.

        The two shared atoms define the central bond. For each ring, the atom preceding the first shared position and the atom following the second are found after ordering the shared positions. Two dihedrals are returned, each using an exterior atom from one ring and an exterior atom from the other.

        :param ring_atoms1: First ring in cyclic order.
        :type ring_atoms1: collections.abc.Sequence[int]
        :param ring_atoms2: Second ring in cyclic order.
        :type ring_atoms2: collections.abc.Sequence[int]
        :param shared_atoms: The two atoms forming the fused bond.
        :type shared_atoms: collections.abc.Sequence[int]
        :param shared_indices1: Positions of the shared atoms in the first ring.
        :type shared_indices1: collections.abc.Sequence[int]
        :param shared_indices2: Positions of the shared atoms in the second ring.
        :type shared_indices2: collections.abc.Sequence[int]
        :return: Two dihedrals spanning the fused bond and both ring exteriors.
        :rtype: list[tuple[int, int, int, int]]
        """
        j, k = shared_atoms
        j1, k1 = shared_indices1
        j2, k2 = shared_indices2
        # we want relative orientation indices for both rings
        inds = []
        if j1 > k1:
            j1, k1 = k1, j1
        if j2 > k2:
            j2, k2 = k2, j2
        i1 = ring_atoms1[j1 - 1]; l1 = ring_atoms1[(k1 + 1) % len(ring_atoms1)]
        i2 = ring_atoms2[j2 - 1]; l2 = ring_atoms2[(k2 + 1) % len(ring_atoms2)]

        return [
            (i1, j, k, l2),
            (i2, j, k, l1)
        ]

    @classmethod
    def fused_ring_coordinates(cls, ring_atoms1, ring_atoms2):
        """
        **LLM Docstring**

        Dispatch fused-ring coordinate generation according to the number of shared atoms.

        The intersection of the two ordered ring lists is computed together with each ring's shared positions. Disjoint rings return no coordinates. One- and two-atom fusions use the registered handlers; any unsupported shared-atom count raises an error.

        :param ring_atoms1: First ring's ordered atom indices.
        :type ring_atoms1: collections.abc.Sequence[int]
        :param ring_atoms2: Second ring's ordered atom indices.
        :type ring_atoms2: collections.abc.Sequence[int]
        :return: Additional angles or dihedrals describing the rings' relative orientation.
        :rtype: list[tuple[int, ...]]
        :raises ValueError: If no handler exists for the number of shared atoms.
        """
        shared_atoms, _, _, r1_indices, r2_indices = nput.intersection(ring_atoms1, ring_atoms2, return_indices=True)
        if len(shared_atoms) == 0:
            return []
        else:
            n = len(shared_atoms)
            coord_func = cls._fused_dispatch().get(n)
            if coord_func is None:
                raise ValueError(f"can't deal with fused rings with {n} shared atoms")
            return coord_func(ring_atoms1, ring_atoms2, shared_atoms, r1_indices, r2_indices)

    def fragment_connection_coords(self, frag_1, frag_2):
        """
        **LLM Docstring**

        Construct up to six primitive coordinates connecting two disconnected fragments.

        When a fragment contains more than two heavy atoms, light atoms are removed and the remaining indices are sorted; otherwise its original ordering is retained. The first atoms define an inter-fragment stretch. Available second and third atoms add two orientation angles and up to three dihedrals, yielding the standard distance/orientation coordinate pattern for two fragments.

        :param frag_1: Atom indices in the first fragment.
        :type frag_1: collections.abc.Sequence[int]
        :param frag_2: Atom indices in the second fragment.
        :type frag_2: collections.abc.Sequence[int]
        :return: Inter-fragment stretch, orientation angles, and available dihedrals.
        :rtype: list[tuple[int, ...]]
        """
        heavy_frag1 = set(frag_1) - set(self.light_atoms)
        if len(heavy_frag1) > 2:
            frag_1 = list(sorted(heavy_frag1))
        heavy_frag2 = set(frag_2) - set(self.light_atoms)
        if len(heavy_frag2) > 2:
            frag_2 = list(sorted(heavy_frag2))

        coords = []
        coords.append((frag_1[0], frag_2[0]))
        if len(frag_2) > 1:
            coords.append((frag_1[0], frag_2[0], frag_2[1]))
        if len(frag_1) > 1:
            coords.append((frag_1[1], frag_1[0], frag_2[0]))
        if len(frag_2) > 1 and len(frag_1) > 1:
            coords.append((frag_1[1], frag_1[0], frag_2[0], frag_2[1]))
        if len(frag_1) > 2:
            coords.append((frag_1[2], frag_1[1], frag_1[0], frag_2[0]))
        if len(frag_2) > 2:
            coords.append((frag_1[0], frag_2[0], frag_2[1], frag_2[2]))

        return coords

    def get_neighborhood_symmetries(self, atoms, ignored=None, neighborhood=3):
        """
        **LLM Docstring**

        Compare local neighbor graphs for every unordered pair of atoms.

        A `neighbor_graph` of the requested depth is constructed for each atom, respecting `ignored`. The returned Boolean list follows upper-triangular pair order `(0,1), (0,2), ..., (n-2,n-1)` and records graph equality for each pair.

        :param atoms: Atom indices whose neighborhoods are compared.
        :type atoms: collections.abc.Sequence[int]
        :param ignored: Atom indices omitted while constructing each neighborhood graph.
        :type ignored: collections.abc.Collection[int] | None
        :param neighborhood: Number of graph shells included in each neighborhood.
        :type neighborhood: int
        :return: Pairwise neighborhood-equivalence flags in upper-triangular order.
        :rtype: list[bool]
        """
        graphs = [
            self.graph.neighbor_graph(a, ignored=ignored, num=neighborhood)
            for a in atoms
        ]
        rows, cols = np.triu_indices(len(graphs), k=1)
        return [graphs[r] == graphs[c] for r,c in zip(rows, cols)]

    def chain_coords(self, R, y):
        """
        **LLM Docstring**

        Attach an atom to the tail of a precedent chain with one stretch, one angle, and one dihedral when possible.

        For a nonempty chain `R`, the new atom `y` is bonded to `R[-1]`. The preceding one or two chain atoms extend that bond into an angle and dihedral respectively.

        :param R: Precedent atom chain ordered from oldest to nearest atom.
        :type R: collections.abc.Sequence[int]
        :param y: Atom to attach to the chain.
        :type y: int
        :return: Zero to three coordinates ending at `y`.
        :rtype: list[tuple[int, ...]]
        """
        coords = []
        if len(R) > 0:
            coords.append((y, R[-1]))
        if len(R) > 1:
            coords.append((y, R[-1], R[-2]))
        if len(R) > 2:
            coords.append((y, R[-1], R[-2], R[-3]))
        return coords

    def RYX2_coords(self, R, y, X):
        """
        **LLM Docstring**

        Generate coordinates for a center atom with a three-member neighbor group and an optional precedent chain.

        The routine adds stretches from `y` to every atom in `X`, all three pairwise `X-y-X` angles, and—when `R` is present—the stretch and three angles joining the nearest precedent atom to `y`. Additional precedent atoms supply one `R-R-y` angle and one `R-R-R-y` dihedral. Despite the name, the implementation indexes the first three entries of `X` and therefore expects at least three neighbors.

        :param R: Precedent chain ending at the atom nearest `y`.
        :type R: collections.abc.Sequence[int]
        :param y: Central atom.
        :type y: int
        :param X: Neighbor atoms; at least three entries are required by the pair-generation loop.
        :type X: collections.abc.Sequence[int]
        :return: Stretches, angles, and optional chain dihedral around `y`.
        :rtype: list[tuple[int, ...]]
        """
        coords = []
        coords.extend((y, x) for x in X)
        coords.extend(
            (X[i], y, X[j])
            for i, j in itertools.combinations(range(3), 2)
        )
        if len(R) > 0:
            coords.append((R[-1], y))
            # add in RYX angles
            coords.extend(
                (R[-1], y, x)
                for x in X
            )
        if len(R) > 1:
            # add in RRY angle
            coords.append(
                (R[-2], R[-1], y)
            )
        if len(R) > 2:
            # add in RRRY dihedral
            coords.append(
                (R[-3], R[-2], R[-1], y)
            )

        return coords

    def RYX3_coords(self, R, y, X):
        """
        **LLM Docstring**

        Generate coordinates for a center atom with three neighbors and an optional precedent chain.

        The implementation is identical to `RYX2_coords`: it creates three `y-X` stretches, the three pairwise `X-y-X` angles, and coordinates linking `y` to up to three atoms from `R`.

        :param R: Precedent chain ending at the atom nearest `y`.
        :type R: collections.abc.Sequence[int]
        :param y: Central atom.
        :type y: int
        :param X: Three or more neighbor atom indices.
        :type X: collections.abc.Sequence[int]
        :return: Stretches, angles, and optional chain dihedral around `y`.
        :rtype: list[tuple[int, ...]]
        """
        coords = []
        coords.extend((y, x) for x in X)
        coords.extend(
            (X[i], y, X[j])
            for i, j in itertools.combinations(range(3), 2)
        )
        if len(R) > 0:
            coords.append((R[-1], y))
            # add in RYX angles
            coords.extend(
                (R[-1], y, x) for x in X
            )
        if len(R) > 1:
            # add in RRY angle
            coords.append(
                (R[-2], R[-1], y)
            )
        if len(R) > 2:
            # add in RRRY dihedral
            coords.append(
                (R[-3], R[-2], R[-1], y)
            )

        return coords

    def get_precedent_chains(self, atom, num_precs=2, ring_atoms=None, light_atoms=None, ignored=None, backbone=None):
        """
        **LLM Docstring**

        Enumerate graph paths leading away from an atom up to a requested predecessor depth.

        A depth-first search starts at `atom`, shares one global visited set across branches, and expands unvisited graph neighbors. Paths terminate at dead ends or after `num_precs` atoms have been collected. Each stored path is reversed before return so it runs from the farthest predecessor toward the atom. `ring_atoms`, `light_atoms`, and `backbone` are normalized but do not currently affect branch selection.

        :param atom: Root atom from which predecessor paths are explored.
        :type atom: int
        :param num_precs: Maximum number of predecessor atoms in each path.
        :type num_precs: int
        :param ring_atoms: Optional ring-atom set; currently not used after normalization.
        :type ring_atoms: collections.abc.Collection[int] | None
        :param light_atoms: Optional light-atom set; currently not used after normalization.
        :type light_atoms: collections.abc.Collection[int] | None
        :param ignored: Atom indices considered visited before traversal.
        :type ignored: collections.abc.Collection[int] | None
        :param backbone: Optional backbone set; currently not used by the active traversal.
        :type backbone: collections.abc.Collection[int] | None
        :return: Predecessor chains ordered from farthest atom to nearest atom.
        :rtype: list[list[int]]
        """
        chains = []
        visited = set([] if ignored is None else ignored)
        ring_atoms = set(self.ring_atoms if ring_atoms is None else ring_atoms)
        light_atoms = set(self.light_atoms if light_atoms is None else light_atoms)
        if backbone is not None:
            backbone = set(backbone)

        visited = visited #| ring_atoms # | light_atoms

        # do a dfs exploration up to the given depth over non-ring, heavy atoms
        queue = collections.deque([[[], 0, atom]])
        while queue:
            chain, depth, root = queue.pop()
            neighbors = self.graph.map[root]
            visited.add(root)
            branches = neighbors - visited
            if len(branches) == 0:
                chains.append(chain)
            elif depth == num_precs - 1:
                chains.extend(chain + [n] for n in branches)
            else:
                queue.extend([chain + [n], depth+1, n] for n in branches)

            #
            # queue.extend(rem)
            # while len(rem) == 0 and queue:
            #     # walk up dfs tree until we find a branch with nodes that work
            #     root = queue.pop()
            #     if root not in visited:
            #         rem = {root}
            # else:
            #     if len(rem) == 0: rem = neighbors - visited - light_atoms
            #     # if len(rem) == 0: rem = neighbors - visited
            #     if len(rem) == 0: break
            #
            #     if backbone is not None:
            #         bb_chain = rem & backbone
            #     else:
            #         bb_chain = []
            #     if len(bb_chain) > 0:
            #         atom = min(bb_chain)
            #     else:
            #         atom = min(rem)
            #     chain.append(atom)

        # chain = list(reversed(chain))

        return [list(reversed(c)) for c in chains]

    symmetry_type_dispatch = {}
    def _symmetry_dispatch(self):
        """
        **LLM Docstring**

        Return handlers for the supported neighbor symmetry-group size patterns.

        Patterns `(3,)`, `(2, 1)`, and `(3, 1)` map to the corresponding coordinate constructors.

        :return: Symmetry-pattern dispatch mapping.
        :rtype: dict[tuple[int, ...], collections.abc.Callable]
        """
        return dict({
            (3,):self._3_coords,
            (2,1):self._2_1_coords,
            (3,1):self._3_1_coords
        })
    def _2_1_coords(self, atom, neighbors, X, R, backbone=None):
        """
        **LLM Docstring**

        Generate coordinates for a `(2, 1)` neighbor partition using the singleton as the precedent direction.

        The first atom in `R` is treated as the neighbor leading away from `atom`. One-step predecessor chains are sought beyond it while excluding the center and all immediate neighbors. For every chain (or an empty fallback), `RYX2_coords` is called with the chain plus `R` and the symmetric group `X`.

        :param atom: Central atom.
        :type atom: int
        :param neighbors: All immediate neighbors, used only to exclude them from chain search.
        :type neighbors: collections.abc.Sequence[int]
        :param X: Symmetric neighbor group passed to `RYX2_coords`.
        :type X: collections.abc.Sequence[int]
        :param R: Singleton neighbor group.
        :type R: collections.abc.Sequence[int]
        :param backbone: Optional backbone forwarded to predecessor-chain search.
        :type backbone: collections.abc.Collection[int] | None
        :return: Coordinates generated for each available precedent chain.
        :rtype: list[tuple[int, ...]]
        """
        coords = []
        R = R[0]
        chains = self.get_precedent_chains(R, 1, ignored=[atom] + neighbors, backbone=backbone)
        if len(chains) == 0: chains = [[]]
        for c in chains:
            coords.extend(self.RYX2_coords(c + [R], atom, X))
        return coords
    def _3_coords(self, atom, neighbors, X, backbone=None):
        """
        **LLM Docstring**

        Generate coordinates for three equivalent neighbors without a precedent chain.

        :param atom: Central atom.
        :type atom: int
        :param neighbors: Immediate-neighbor list; unused by this handler.
        :type neighbors: collections.abc.Sequence[int]
        :param X: Three-neighbor symmetry group.
        :type X: collections.abc.Sequence[int]
        :param backbone: Unused compatibility argument.
        :type backbone: collections.abc.Collection[int] | None
        :return: Coordinates produced by `RYX3_coords([], atom, X)`.
        :rtype: list[tuple[int, ...]]
        """
        return self.RYX3_coords([], atom, X)
    def _3_1_coords(self, atom, neighbors, X, R, backbone=None):
        """
        **LLM Docstring**

        Generate coordinates for a `(3, 1)` neighbor partition using the singleton as a precedent direction.

        The method mirrors `_2_1_coords` but delegates each discovered one-step predecessor chain to `RYX3_coords` for the three-member group `X`.

        :param atom: Central atom.
        :type atom: int
        :param neighbors: Immediate neighbors excluded from predecessor search.
        :type neighbors: collections.abc.Sequence[int]
        :param X: Three-member symmetric neighbor group.
        :type X: collections.abc.Sequence[int]
        :param R: Singleton neighbor group.
        :type R: collections.abc.Sequence[int]
        :param backbone: Optional backbone forwarded to chain search.
        :type backbone: collections.abc.Collection[int] | None
        :return: Coordinates generated for each available precedent chain.
        :rtype: list[tuple[int, ...]]
        """
        coords = []
        R = R[0]
        chains = self.get_precedent_chains(R, 1, ignored=[atom] + neighbors, backbone=backbone)
        if len(chains) == 0: chains = [[]]
        for c in chains:
            coords.extend(self.RYX3_coords(c + [R], atom, X))
        return coords

    # def _2_2_coords(self, atom, neighbors, X, R, backbone=None):
    #     coords = []
    #     R = R[0]
    #     # chains = self.get_precedent_chains(R, 1, ignored=[atom] + neighbors, backbone=backbone)
    #     if len(chains) == 0: chains = [[]]
    #     for c in chains:
    #         coords.extend(self.R2YX2_coords(c + [R], atom, X))
    #     return coords


    @classmethod
    def get_symmetry_groups(cls, neighbors, matches):
        """
        **LLM Docstring**

        Convert pairwise equality flags into groups of equivalent neighbors.

        `matches` is consumed in upper-triangular pair order. Equal pairs share the same mutable index set, causing connected equality relationships to merge. Duplicate set objects are removed by identity, groups are sorted largest first, and index groups are translated back to neighbor atom indices.

        :param neighbors: Neighbor atom indices in the order used to compute `matches`.
        :type neighbors: collections.abc.Sequence[int]
        :param matches: Equality flags for every unordered neighbor pair in upper-triangular order.
        :type matches: collections.abc.Sequence[bool]
        :return: Neighbor groups ordered from largest to smallest.
        :rtype: list[list[int]]
        """
        groups = {}
        n = len(neighbors)
        k = 0
        for i in range(n):
            if i not in groups:
                groups[i] = {i}
            for j in range(i+1, n):
                eq = matches[k]
                k += 1
                if eq:
                    groups[j] = groups[i]
                    groups[i].add(j)
        groups = {id(g):g for g in groups.values()}
        groups = list(reversed(sorted(groups.values(), key=lambda g:len(g))))
        return [
            [neighbors[i] for i in g]
            for g in groups
        ]

    def symmetry_coords(self, atom, neighborhood=3, backbone=None):
        """
        **LLM Docstring**

        Generate chain-based coordinates for a non-ring atom.

        The previously intended neighborhood-symmetry dispatch is currently commented out. The active code finds predecessor chains of length up to three from `atom`; for each chain, it adds the stretch, angle, and dihedral that connect `atom` to the chain tail. If no chain is found, an empty chain contributes no coordinates. `neighborhood` is therefore currently unused.

        :param atom: Atom for which primitive coordinates are generated.
        :type atom: int
        :param neighborhood: Reserved neighborhood depth; unused by the active implementation.
        :type neighborhood: int
        :param backbone: Optional backbone forwarded to `get_precedent_chains`.
        :type backbone: collections.abc.Collection[int] | None
        :return: Chain-derived coordinates ending at `atom`.
        :rtype: list[tuple[int, ...]]
        """
        # neighbors = list(self.graph.map[atom])
        coords = []
        # dispatch = self._symmetry_dispatch()
        # neighbor_counts = {sum(k) for k in dispatch.keys()}
        # if len(neighbors) in neighbor_counts:
        #     symms = self.get_neighborhood_symmetries(neighbors, ignored=[atom], neighborhood=neighborhood)
        #     groups = self.get_symmetry_groups(neighbors, symms)
        #     key = tuple(len(g) for g in groups)
        #     dfunc = dispatch.get(key)
        #     if dfunc is not None:
        #         coords = dfunc(atom, neighbors, *groups, backbone=backbone)
        chains = self.get_precedent_chains(atom, 3, backbone=backbone)
        if len(chains) == 0: chains = [[]]
        for R in chains:
            coords.extend(self.chain_coords(R, atom))

        # if coords is None:
        #     R = self.get_precedent_chain(atom, 3, backbone=backbone)
        #     coords = self.chain_coords(R, atom)

        return coords

def enumerate_coordinate_completions_line(indices, coords, canonicalize=False):
    """
    **LLM Docstring**

    Enumerate the missing internal coordinates needed to complete a one- through four-atom geometric template.

    For three atoms, existing bonds/angles are marked on a symbolic triangle and `enumerate_triangle_completions` supplies every valid missing-field combination. Four or more atoms use a symbolic dihedron and `enumerate_dihedron_completions`; only the template fields represented by that dihedron are considered. With one atom, the sole completion is empty. The two-atom branch is implemented with `i, j = num_atoms`, which attempts to unpack an integer and will raise `TypeError` if reached.

    :param indices: Atom indices defining the line/template.
    :type indices: collections.abc.Sequence[int]
    :param coords: Existing internal coordinates.
    :type coords: collections.abc.Collection[tuple[int, ...]]
    :param canonicalize: Whether to canonicalize the existing coordinate list before testing membership.
    :type canonicalize: bool
    :return: Generator of tuples containing the additional coordinates for each valid completion.
    :rtype: collections.abc.Iterator[tuple[tuple[int, ...], ...]]
    """
    num_atoms = len(indices)
    if canonicalize:
        coords = ints.get_canonical_internal_list(coords)
    if num_atoms == 1:
        yield ()
    elif num_atoms == 2:
        i,j = num_atoms
        crd = ints.canonicalize_internal(i,j)
        if crd in coords:
            yield ()
        else:
            yield (crd,)
    elif num_atoms == 3:
        template = nput.make_symbolic_triangle(indices=indices)
        res_map = template._asdict()
        test_tri = nput.make_triangle(**{
            key:(True if val in coords else None)
            for key, val in res_map.items()
        })
        for comp in nput.enumerate_triangle_completions(test_tri):
            # map backwards
            yield tuple(res_map[name] for name in comp)
    else:
        template = nput.make_symbolic_dihedron(indices=indices)
        res_map = template._asdict()
        test_tri = nput.make_dihedron(**{
            key: (True if val in coords else None)
            for key, val in res_map.items()
        })
        for comp in nput.enumerate_dihedron_completions(test_tri):
            # map backwards
            yield tuple(res_map[name] for name in comp)

def enumerate_coordinate_sets(groups, coords, canonicalize=True):
    """
    **LLM Docstring**

    Recursively enumerate coordinate sets that complete each supplied atom group.

    Existing coordinates are canonicalized into a set by default. For each group, negative padding indices are removed, every completion from `enumerate_coordinate_completions_line` is merged into the current set, and recursion continues through the remaining groups. The outer loop also starts recursion at each group position, so overlapping suffix traversals may yield duplicate sets.

    :param groups: Sequence of atom-index groups; negative entries are ignored as padding.
    :type groups: collections.abc.Sequence[collections.abc.Sequence[int]]
    :param coords: Existing internal coordinates.
    :type coords: collections.abc.Iterable[tuple[int, ...]]
    :param canonicalize: Whether to canonicalize `coords` on the initial call.
    :type canonicalize: bool
    :return: Generator yielding completed coordinate sets.
    :rtype: collections.abc.Iterator[set[tuple[int, ...]]]
    """
    #TODO: add in BFS enumeration
    if canonicalize:
        coords = set(ints.get_canonical_internal_list(coords))
    for n,subinds in enumerate(groups):
        subsubinds = [g for g in subinds if g >= 0]
        for comp in enumerate_coordinate_completions_line(subsubinds, coords, canonicalize=False):
            merge_coords = coords|set(comp)
            if len(groups) == 1:
                yield merge_coords
            else:
                for subcomp in enumerate_coordinate_sets(
                        groups[n + 1:],
                        merge_coords,
                        canonicalize=False
                ):
                    yield subcomp

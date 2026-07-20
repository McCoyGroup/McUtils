from __future__ import annotations
from typing import *
import abc
import collections
import itertools
import numpy as np
from .. import Devutils as dev
from .. import Numputils as nput
from .. import Iterators as itut
from ..Graphs import EdgeGraph, pebble_rigidity, statistically_rigid, uniquely_rigid
__all__ = ['canonicalize_internal', 'get_canonical_internal_list', 'is_coordinate_list_like', 'is_valid_coordinate', 'permute_internals', 'find_internal', 'coordinate_sign', 'coordinate_indices', 'get_internal_distance_conversion', 'internal_distance_convert', 'get_internal_triangles_and_dihedrons', 'find_internal_conversion', 'get_internal_cartesian_conversion', 'validate_internals', 'InternalCoordinateType', 'InternalSpec', 'InternalCoordinateGraph']

class InternalCoordinateType(metaclass=abc.ABCMeta):
    registry = {}

    @classmethod
    def register(cls, type, typename=None):
        """
        **LLM Docstring**

        Register an `InternalCoordinateType` subclass under a dispatch name. Called with a string alone, this returns a decorator that assigns that name to the decorated class; otherwise it invalidates the cached dispatcher, stores the class in `registry`, and returns the class unchanged.

        :param type: A coordinate class, or a registration name when using decorator form.
        :type type: Any
        :param typename: The registry key to assign to the coordinate class.
        :type typename: Any
        :return: The registered class, or a decorator awaiting the class.
        :rtype: type | Callable[[type], type]
        """
        ...
    _dispatch = dev.uninitialized

    @classmethod
    def get_dispatch(cls) -> dev.OptionsMethodDispatch:
        """
        **LLM Docstring**

        Return the lazily constructed options dispatcher used to turn dictionaries containing a `type` key into registered coordinate classes and their constructor options.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: dev.OptionsMethodDispatch
        """
        ...

    @classmethod
    def resolve(cls, input):
        """
        **LLM Docstring**

        Convert either a typed option dictionary or a bare index sequence into an instantiated coordinate object. Dictionary inputs are dispatched by `type`; bare sequences are tested against each registered class with `could_be`, and an unmatched input raises `ValueError`.

        :param input: A typed option mapping or bare coordinate-index sequence.
        :type input: Any
        :return: An instantiated registered coordinate object.
        :rtype: InternalCoordinateType
        """
        ...

    @classmethod
    def could_be(cls, input):
        """
        **LLM Docstring**

        Report whether an input can represent this coordinate type. The base implementation always returns `False` and is intended to be overridden.

        :param input: A typed option mapping or bare coordinate-index sequence.
        :type input: Any
        :return: Whether the tested condition is satisfied.
        :rtype: bool
        """
        ...

    def equivalent_to(self, other):
        """
        **LLM Docstring**

        Test whether two coordinates have the same concrete type and the same indices after each is put in canonical orientation.

        :param other: The coordinate to compare against.
        :type other: Any
        :return: Whether the tested condition is satisfied.
        :rtype: bool
        """
        ...

    def __eq__(self, other):
        """
        **LLM Docstring**

        Compare coordinates using canonical coordinate equivalence rather than object identity.

        :param other: The coordinate to compare against.
        :type other: Any
        :return: Whether the tested condition is satisfied.
        :rtype: bool
        """
        ...

    @abc.abstractmethod
    def canonicalize(self):
        """
        **LLM Docstring**

        Return an equivalent coordinate in the canonical index orientation defined by the concrete coordinate type.

        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

    @abc.abstractmethod
    def get_indices(self) -> Tuple[int, ...]:
        """
        **LLM Docstring**

        Return the atom indices that define this internal coordinate, in the type-specific ordering.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Tuple[int, ...]
        """
        ...

    def __hash__(self):
        """
        **LLM Docstring**

        Hash the coordinate from its concrete class and stored index tuple so it can be used as a dictionary key or set member.

        :return: The coordinate hash value.
        :rtype: int
        """
        ...

    @abc.abstractmethod
    def reindex(self, reindexing):
        """
        **LLM Docstring**

        Return the same coordinate expressed under a supplied old-index to new-index mapping.

        :param reindexing: A mapping from existing atom indices to replacement indices.
        :type reindexing: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

    @abc.abstractmethod
    def get_carried_atoms(self, context: InternalSpec):
        """
        **LLM Docstring**

        Determine the atom groups displaced on the two sides of this coordinate when it is varied in an `InternalSpec`.

        :param context: The surrounding coordinate specification used to infer connectivity and moved fragments.
        :type context: InternalSpec
        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

    @abc.abstractmethod
    def get_constraint_rads(self) -> list[Distance | Angle | Dihedral]:
        """
        **LLM Docstring**

        Return the primitive distance, angle, or dihedral coordinates that must remain available to constrain this coordinate.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: list[Distance | Angle | Dihedral]
        """
        ...

    @abc.abstractmethod
    def get_expansion(self, coords, order=None, **opts) -> List[np.ndarray]:
        """
        **LLM Docstring**

        Evaluate Cartesian derivatives of this internal coordinate through the requested order.

        :param coords: Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
        :type coords: Any
        :param order: Highest derivative order to compute.
        :type order: Any
        :param opts: Additional options forwarded to the numerical conversion routine.
        :type opts: Any
        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: List[np.ndarray]
        """
        ...

    @abc.abstractmethod
    def get_inverse_expansion(self, coords, order=None, moved_indices=None, **opts) -> List[np.ndarray]:
        """
        **LLM Docstring**

        Evaluate derivatives of the Cartesian displacement generated by changing this internal coordinate, optionally restricted to selected moved atoms.

        :param coords: Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
        :type coords: Any
        :param order: Highest derivative order to compute.
        :type order: Any
        :param moved_indices: Explicit pair of atom groups moved on the two sides of a coordinate.
        :type moved_indices: Any
        :param opts: Additional options forwarded to the numerical conversion routine.
        :type opts: Any
        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: List[np.ndarray]
        """
        ...

    def _prep_left_right_atoms(self, context, moved_indices, left_atoms, right_atoms):
        """
        **LLM Docstring**

        Resolve the two moved-atom groups used by inverse expansions. Explicit `left_atoms` and `right_atoms` take precedence; otherwise `moved_indices` is unpacked, or the groups are inferred from the coordinate graph in `context`.

        :param context: The surrounding coordinate specification used to infer connectivity and moved fragments.
        :type context: Any
        :param moved_indices: Explicit pair of atom groups moved on the two sides of a coordinate.
        :type moved_indices: Any
        :param left_atoms: Atoms assigned to the first side of the displacement.
        :type left_atoms: Any
        :param right_atoms: Atoms assigned to the second side of the displacement.
        :type right_atoms: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

class BasicInternalType(InternalCoordinateType):
    forward_conversion: Callable[[np.ndarray, ParamSpec('P')], List[np.ndarray]]
    inverse_conversion: Callable[[np.ndarray, ParamSpec('P')], List[np.ndarray]]

    def __init__(self, indices: Sequence[int]):
        """
        **LLM Docstring**

        Store the defining atom indices as an immutable tuple and bind the class-level forward and inverse conversion functions onto the instance.

        :param indices: Atom indices defining the coordinate, or a restricted search index set.
        :type indices: Sequence[int]
        :return: None.
        :rtype: None
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Format the coordinate as its class name followed by its defining index tuple.

        :return: A concise representation of the object.
        :rtype: str
        """
        ...

    def reindex(self, reindexing):
        """
        **LLM Docstring**

        Apply an index lookup to every defining atom and construct a coordinate of the same type with the mapped indices.

        :param reindexing: A mapping from existing atom indices to replacement indices.
        :type reindexing: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

    def canonicalize(self):
        """
        **LLM Docstring**

        Orient a reversible coordinate so that its final atom index is not smaller than its first; reverse the full index tuple when necessary.

        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

    def get_indices(self):
        """
        **LLM Docstring**

        Return the stored tuple of defining atom indices.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

    def get_dropped_internals(self):
        """
        **LLM Docstring**

        Return the set of coordinates removed from the bond graph when determining which atoms move with this coordinate; the default removes only the coordinate itself.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

    def get_carried_atoms(self, context: InternalSpec, max_branching=5):
        """
        **LLM Docstring**

        Split the internal-coordinate bond graph into fragments associated with the first and last atoms. If dropping the coordinate does not separate them, repeatedly break the midpoint bond on their connecting path until distinct carried-atom groups are obtained.

        :param context: The surrounding coordinate specification used to infer connectivity and moved fragments.
        :type context: InternalSpec
        :param max_branching: Maximum repeated graph-splitting attempts before declaring the carried fragments ambiguous.
        :type max_branching: Any
        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

    def get_expansion(self, coords, *, order=None, masses=None, **opts):
        """
        **LLM Docstring**

        Call the coordinate type’s forward derivative routine with the stored atom indices to obtain derivatives of the internal value with respect to Cartesian coordinates.

        :param coords: Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
        :type coords: Any
        :param order: Highest derivative order to compute.
        :type order: Any
        :param masses: Atomic masses used for mass weighting or rigid-body modes.
        :type masses: Any
        :param opts: Additional options forwarded to the numerical conversion routine.
        :type opts: Any
        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

    def get_inverse_expansion(self, coords, *, order=None, moved_indices=None, context=None, left_atoms=None, right_atoms=None, masses=None, **opts):
        """
        **LLM Docstring**

        Resolve the atoms moved on each side of the coordinate and call the type’s inverse derivative routine to obtain Cartesian response tensors.

        :param coords: Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
        :type coords: Any
        :param order: Highest derivative order to compute.
        :type order: Any
        :param moved_indices: Explicit pair of atom groups moved on the two sides of a coordinate.
        :type moved_indices: Any
        :param context: The surrounding coordinate specification used to infer connectivity and moved fragments.
        :type context: Any
        :param left_atoms: Atoms assigned to the first side of the displacement.
        :type left_atoms: Any
        :param right_atoms: Atoms assigned to the second side of the displacement.
        :type right_atoms: Any
        :param masses: Atomic masses used for mass weighting or rigid-body modes.
        :type masses: Any
        :param opts: Additional options forwarded to the numerical conversion routine.
        :type opts: Any
        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

@InternalCoordinateType.register('dist')
class Distance(BasicInternalType):
    forward_conversion = nput.dist_vec
    inverse_conversion = nput.dist_expansion

    @classmethod
    def could_be(cls, input):
        """
        **LLM Docstring**

        Recognize a distance specification as a two-element integer index sequence.

        :param input: A typed option mapping or bare coordinate-index sequence.
        :type input: Any
        :return: Whether the tested condition is satisfied.
        :rtype: bool
        """
        ...

    def get_constraint_rads(self):
        """
        **LLM Docstring**

        Return the distance itself as the sole primitive coordinate required to constrain it.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

@InternalCoordinateType.register('bend')
class Angle(BasicInternalType):
    forward_conversion = nput.angle_vec
    inverse_conversion = nput.angle_expansion

    @classmethod
    def could_be(cls, input):
        """
        **LLM Docstring**

        Recognize an angle specification as a three-element integer index sequence.

        :param input: A typed option mapping or bare coordinate-index sequence.
        :type input: Any
        :return: Whether the tested condition is satisfied.
        :rtype: bool
        """
        ...

    def get_constraint_rads(self):
        """
        **LLM Docstring**

        Return the angle itself as the primitive coordinate required to constrain it.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

    def get_dropped_internals(self):
        """
        **LLM Docstring**

        Remove the angle and its two adjacent bond distances when finding the atom groups carried by an angle displacement.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

@InternalCoordinateType.register('dihedral')
class Dihedral(BasicInternalType):
    forward_conversion = nput.dihed_vec
    inverse_conversion = nput.dihed_expansion

    @classmethod
    def could_be(cls, input):
        """
        **LLM Docstring**

        Recognize a dihedral specification as a four-element integer index sequence.

        :param input: A typed option mapping or bare coordinate-index sequence.
        :type input: Any
        :return: Whether the tested condition is satisfied.
        :rtype: bool
        """
        ...

    def get_constraint_rads(self):
        """
        **LLM Docstring**

        Return the dihedral itself as the primitive coordinate required to constrain it.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

    def get_dropped_internals(self):
        """
        **LLM Docstring**

        Remove the dihedral, its central angle pair, and the three chain bond distances when separating the two sides of a torsional displacement.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

@InternalCoordinateType.register('wag')
class Wag(BasicInternalType):
    forward_conversion = nput.wag_vec
    inverse_conversion = nput.wag_expansion

    def get_constraint_rads(self):
        """
        **LLM Docstring**

        Represent a wagging coordinate by the three dihedrals formed by the central atom and each choice of three surrounding atoms.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

@InternalCoordinateType.register('oop')
class OutOfPlane(BasicInternalType):
    forward_conversion = nput.oop_vec
    inverse_conversion = nput.oop_expansion

@InternalCoordinateType.register('transrot')
class TranslatonRotation(BasicInternalType):
    forward_conversion = nput.transrot_vecs
    inverse_conversion = nput.transrot_expansion

    def __init__(self, indices: Sequence[int], masses=None):
        """
        **LLM Docstring**

        Store the atoms participating in a rigid translation/rotation coordinate and optional masses used to define the rigid-body modes.

        :param indices: Atom indices defining the coordinate, or a restricted search index set.
        :type indices: Sequence[int]
        :param masses: Atomic masses used for mass weighting or rigid-body modes.
        :type masses: Any
        :return: None.
        :rtype: None
        """
        ...

    def canonicalize(self):
        """
        **LLM Docstring**

        Return the rigid-body coordinate unchanged because its atom set has no reversible endpoint orientation.

        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

    def get_carried_atoms(self, context: InternalSpec):
        """
        **LLM Docstring**

        Treat all atoms in the rigid-body coordinate as the moved group and return no opposing group.

        :param context: The surrounding coordinate specification used to infer connectivity and moved fragments.
        :type context: InternalSpec
        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

    def get_inverse_expansion(self, coords, *, order=None, context=None, moved_indices=None, extra_atoms=None, masses=None, **opts):
        """
        **LLM Docstring**

        Build the translation/rotation inverse expansion for the selected atoms using the stored or supplied masses and requested derivative order.

        :param coords: Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
        :type coords: Any
        :param order: Highest derivative order to compute.
        :type order: Any
        :param context: The surrounding coordinate specification used to infer connectivity and moved fragments.
        :type context: Any
        :param moved_indices: Explicit pair of atom groups moved on the two sides of a coordinate.
        :type moved_indices: Any
        :param extra_atoms: Additional atom indices to include in the assembled derivative or graph even when they do not appear in a coordinate.
        :type extra_atoms: Any
        :param masses: Atomic masses used for mass weighting or rigid-body modes.
        :type masses: Any
        :param opts: Additional options forwarded to the numerical conversion routine.
        :type opts: Any
        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

@InternalCoordinateType.register('orientation')
class Orientation(BasicInternalType):
    forward_conversion = nput.orientation_vecs
    inverse_conversion = nput.orientation_expansion

    def __init__(self, indices: Sequence[int], masses=None):
        """
        **LLM Docstring**

        Store the oriented atom pair and optional masses used to define an orientation coordinate.

        :param indices: Atom indices defining the coordinate, or a restricted search index set.
        :type indices: Sequence[int]
        :param masses: Atomic masses used for mass weighting or rigid-body modes.
        :type masses: Any
        :return: None.
        :rtype: None
        """
        ...

    def canonicalize(self):
        """
        **LLM Docstring**

        Return the orientation unchanged because reversing its atom order changes the directed orientation.

        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

    def get_indices(self):
        """
        **LLM Docstring**

        Return the stored atom indices defining the orientation.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

    def reindex(self, reindexing):
        """
        **LLM Docstring**

        Map the orientation’s atoms through a supplied reindexing and preserve its mass data.

        :param reindexing: A mapping from existing atom indices to replacement indices.
        :type reindexing: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

    def get_carried_atoms(self, context: InternalSpec):
        """
        **LLM Docstring**

        Return the orientation atoms as the moved group and no atoms on the opposite side.

        :param context: The surrounding coordinate specification used to infer connectivity and moved fragments.
        :type context: InternalSpec
        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

    def get_inverse_expansion(self, coords, *, order=None, moved_indices=None, context=None, left_extra_atoms=None, right_extra_atoms=None, masses=None, **opts):
        """
        **LLM Docstring**

        Construct the Cartesian inverse expansion for changing the orientation of the selected atoms, using optional masses and moved-atom overrides.

        :param coords: Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
        :type coords: Any
        :param order: Highest derivative order to compute.
        :type order: Any
        :param moved_indices: Explicit pair of atom groups moved on the two sides of a coordinate.
        :type moved_indices: Any
        :param context: The surrounding coordinate specification used to infer connectivity and moved fragments.
        :type context: Any
        :param left_extra_atoms: Additional atoms to assign to the left moved fragment.
        :type left_extra_atoms: Any
        :param right_extra_atoms: Additional atoms to assign to the right moved fragment.
        :type right_extra_atoms: Any
        :param masses: Atomic masses used for mass weighting or rigid-body modes.
        :type masses: Any
        :param opts: Additional options forwarded to the numerical conversion routine.
        :type opts: Any
        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

class InternalSpec:

    def __init__(self, coords, canonicalize=True, bond_graph=None, triangulation=None, masses=None, ungraphed_internals=None, distance_conversions=None):
        """
        **LLM Docstring**

        Normalize a collection of coordinate specifications into `InternalCoordinateType` objects, optionally canonicalize and deduplicate them, collect the participating atoms, and initialize cached triangulations, bond graphs, masses, and conversion data.

        :param coords: Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
        :type coords: Any
        :param canonicalize: Whether to put coordinates in canonical orientation before comparison or storage.
        :type canonicalize: Any
        :param bond_graph: Optional precomputed connectivity graph.
        :type bond_graph: Any
        :param triangulation: Optional precomputed triangle/dihedron representation.
        :type triangulation: Any
        :param masses: Atomic masses used for mass weighting or rigid-body modes.
        :type masses: Any
        :param ungraphed_internals: Coordinates that cannot be represented directly as edges in the bond graph and therefore require separate handling.
        :type ungraphed_internals: Any
        :param distance_conversions: Precomputed recipes for reconstructing pair distances from the available internal coordinates.
        :type distance_conversions: Any
        :return: None.
        :rtype: None
        """
        ...

    @classmethod
    def from_zmatrix(cls, *zmats, additions=None, **opts):
        """
        **LLM Docstring**

        Create an `InternalSpec` from one or more Z-matrix index arrays by collecting each row’s distance, angle, and dihedral definitions, then appending any explicitly requested coordinates.

        :param additions: Additional coordinates to append to those extracted from the Z-matrix.
        :type additions: Any
        :param zmats: One or more Z-matrix index arrays.
        :type zmats: Any
        :param opts: Additional options forwarded to the numerical conversion routine.
        :type opts: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

    @property
    def atom_sets(self) -> Tuple[Tuple[int]]:
        """
        **LLM Docstring**

        Return the defining atom tuple for every coordinate in the specification.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Tuple[Tuple[int]]
        """
        ...

    @property
    def atoms(self) -> Tuple[int]:
        """
        **LLM Docstring**

        Return the sorted unique atom indices appearing in any coordinate.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Tuple[int]
        """
        ...

    def get_triangulation(self):
        """
        **LLM Docstring**

        Lazily derive and cache the triangle and dihedron sets that express the specification as connected distance geometry.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

    def get_pruned_rads(self):
        """
        **LLM Docstring**

        Return the subset of primitive coordinates retained after removing redundancies implied by the triangulation.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

    def get_pruned_triangulation(self):
        """
        **LLM Docstring**

        Return a triangulation rebuilt from the nonredundant primitive coordinates.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

    def get_bond_graph(self) -> EdgeGraph:
        """
        **LLM Docstring**

        Lazily construct an `EdgeGraph` whose edges are the bond distances represented by the coordinate set.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: EdgeGraph
        """
        ...

    @property
    def graph(self):
        """
        **LLM Docstring**

        Expose the cached or newly constructed bond graph for the specification.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

    def get_distance_conversions(self):
        """
        **LLM Docstring**

        Build and cache the conversion specification and callable that reconstruct all triangulation distances from the stored internal coordinates.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

    def get_zmat_conv(self, raise_on_incomplete=True):
        """
        **LLM Docstring**

        Find and cache a conversion from this coordinate set to a Z-matrix ordering. Optionally raise when no complete Z-matrix can be constructed.

        :param raise_on_incomplete: Whether failure to build a complete conversion raises instead of returning an incomplete result.
        :type raise_on_incomplete: Any
        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

    def get_dmat_conv(self):
        """
        **LLM Docstring**

        Build and cache a converter from internal-coordinate values to the condensed or square distance-matrix representation required by the triangulation.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...
    graph_split_method = 'dists'

    def get_dropped_internal_bond_graph(self, internals, method=None):
        """
        **LLM Docstring**

        Return a copy of the bond graph with the bonds implied by selected coordinates removed, using either direct coordinate decomposition or the requested removal method.

        :param internals: Available internal-coordinate specifications or their numerical values.
        :type internals: Any
        :param method: Strategy used to remove coordinate-implied bonds.
        :type method: Any
        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

    def get_direct_derivatives(self, coords, order=1, cache=True, reproject=False, base_transformation=None, reference_internals=None, combine_expansions=True, terms=None, **opts):
        """
        **LLM Docstring**

        Evaluate direct Cartesian derivatives for every coordinate, pad them to the full atom set, and stack like derivative orders into coordinate-by-Cartesian tensors.

        :param coords: Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
        :type coords: Any
        :param order: Highest derivative order to compute.
        :type order: Any
        :param cache: Optional mutable cache of triangulation or conversion results.
        :type cache: Any
        :param reproject: Whether to project the orthogonalized transformations back into the original coordinate basis.
        :type reproject: Any
        :param base_transformation: Optional transformation used as the starting basis before orthogonalization.
        :type base_transformation: Any
        :param reference_internals: Reference internal-coordinate values used to select the periodic branch or initialize reconstruction.
        :type reference_internals: Any
        :param combine_expansions: Whether per-coordinate inverse derivatives are assembled into global tensors.
        :type combine_expansions: Any
        :param terms: Triangle or dihedron conversion metadata to permute.
        :type terms: Any
        :param opts: Additional options forwarded to the numerical conversion routine.
        :type opts: Any
        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

    def orthogonalize_transformations(cls, expansion, inverse, coords=None, masses=None, order=None, remove_translation_rotations=False):
        """
        **LLM Docstring**

        Mass-weight and orthogonalize forward and inverse transformation matrices with an SVD-based pseudoinverse, optionally removing translational/rotational null modes and returning the retained singular subspace.

        :param expansion: Forward internal-to-Cartesian derivative tensors to orthogonalize.
        :type expansion: Any
        :param inverse: Inverse Cartesian-to-internal derivative tensors paired with `expansion`.
        :type inverse: Any
        :param coords: Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
        :type coords: Any
        :param masses: Atomic masses used for mass weighting or rigid-body modes.
        :type masses: Any
        :param order: Highest derivative order to compute.
        :type order: Any
        :param remove_translation_rotations: Whether rigid translations and rotations are removed from the retained Cartesian subspace.
        :type remove_translation_rotations: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

    def get_expansion(self, coords, order=1, return_inverse=False, remove_translation_rotations=True, orthogonalize=True, **opts) -> List[np.ndarray]:
        """
        **LLM Docstring**

        Assemble derivatives of the complete internal-coordinate vector with respect to Cartesian coordinates. It combines each coordinate’s expansion, optionally applies mass weighting or orthogonalization, and can return the associated inverse transformations.

        :param coords: Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
        :type coords: Any
        :param order: Highest derivative order to compute.
        :type order: Any
        :param return_inverse: Whether to return inverse transformation data in addition to the primary result.
        :type return_inverse: Any
        :param remove_translation_rotations: Whether rigid translations and rotations are removed from the retained Cartesian subspace.
        :type remove_translation_rotations: Any
        :param orthogonalize: Whether to replace raw derivative transformations with an orthogonalized pair.
        :type orthogonalize: Any
        :param opts: Additional options forwarded to the numerical conversion routine.
        :type opts: Any
        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: List[np.ndarray]
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Format the specification as the class name containing its normalized coordinate list.

        :return: A concise representation of the object.
        :rtype: str
        """
        ...

    def get_direct_inverses(self, coords, order=1, terms=None, combine_expansions=True, **opts) -> List[np.ndarray]:
        """
        **LLM Docstring**

        Evaluate each coordinate’s inverse Cartesian expansion and combine the per-coordinate tensors into global inverse transformation derivatives when requested.

        :param coords: Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
        :type coords: Any
        :param order: Highest derivative order to compute.
        :type order: Any
        :param terms: Triangle or dihedron conversion metadata to permute.
        :type terms: Any
        :param combine_expansions: Whether per-coordinate inverse derivatives are assembled into global tensors.
        :type combine_expansions: Any
        :param opts: Additional options forwarded to the numerical conversion routine.
        :type opts: Any
        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: List[np.ndarray]
        """
        ...

    def cartesians_to_internals(self, coords, order=None, **opts):
        """
        **LLM Docstring**

        Evaluate every stored coordinate on Cartesian geometries and optionally return its Cartesian derivative expansion.

        :param coords: Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
        :type coords: Any
        :param order: Highest derivative order to compute.
        :type order: Any
        :param opts: Additional options forwarded to the numerical conversion routine.
        :type opts: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

    def internals_to_cartesians(self, coords, order=None, reference_cartesians=None, return_fragments=False, return_inverse=True, transformations=None, reference_internals=None, use_distance_matrix_fallback=False, **deriv_opts):
        """
        **LLM Docstring**

        Recover Cartesian geometries from internal values using either the cached Z-matrix route or distance-geometry route, applying reference coordinates, embedding options, and optional derivative information.

        :param coords: Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
        :type coords: Any
        :param order: Highest derivative order to compute.
        :type order: Any
        :param reference_cartesians: Reference Cartesian geometry used to align or initialize reconstructed structures.
        :type reference_cartesians: Any
        :param return_fragments: Whether disconnected fragment geometries are returned separately instead of as one assembled structure.
        :type return_fragments: Any
        :param return_inverse: Whether to return inverse transformation data in addition to the primary result.
        :type return_inverse: Any
        :param transformations: Optional precomputed coordinate transformations used during reconstruction.
        :type transformations: Any
        :param reference_internals: Reference internal-coordinate values used to select the periodic branch or initialize reconstruction.
        :type reference_internals: Any
        :param use_distance_matrix_fallback: Whether to fall back to distance-matrix embedding when a direct Z-matrix conversion is unavailable.
        :type use_distance_matrix_fallback: Any
        :param deriv_opts: Options forwarded specifically to derivative and inverse-expansion calculations.
        :type deriv_opts: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

    def _novel_distance(self, rad, tris, diheds):
        """
        **LLM Docstring**

        For a primitive coordinate, identify a distance introduced by that coordinate that is not already fixed by the supplied triangle and dihedron sets.

        :param rad: Primitive distance, angle, or dihedral coordinate being analyzed.
        :type rad: Any
        :param tris: Triangle triangulation records.
        :type tris: Any
        :param diheds: Dihedron triangulation records.
        :type diheds: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

    def get_triangulation_novel_internals(self, rads=None, triangulation=None):
        """
        **LLM Docstring**

        Return coordinates that contribute distances not already represented by a triangulation, together with the corresponding novel distance pairs.

        :param rads: Primitive coordinate subset to analyze.
        :type rads: Any
        :param triangulation: Optional precomputed triangle/dihedron representation.
        :type triangulation: Any
        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

    def _tri_dists(self, rad, tris, diheds):
        """
        **LLM Docstring**

        List the pair distances required to represent one primitive coordinate within the current triangle and dihedron triangulation.

        :param rad: Primitive distance, angle, or dihedral coordinate being analyzed.
        :type rad: Any
        :param tris: Triangle triangulation records.
        :type tris: Any
        :param diheds: Dihedron triangulation records.
        :type diheds: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

    def get_triangulation_distances(self, rads=None, triangulation=None):
        """
        **LLM Docstring**

        Collect and deduplicate all pair distances required by the triangulation and optionally by an explicit coordinate subset.

        :param rads: Primitive coordinate subset to analyze.
        :type rads: Any
        :param triangulation: Optional precomputed triangle/dihedron representation.
        :type triangulation: Any
        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

    def check_redundancy(self):
        """
        **LLM Docstring**

        Check whether the coordinate set contains more independent constraints than its atom count permits, using the triangulation rigidity test.

        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

def canonicalize_internal(coord, return_sign=False, check_invalid=True):
    """
    **LLM Docstring**

    Put a distance, angle, or dihedral index sequence into its canonical orientation. Distances and angles are reversed when their last index is smaller than the first; dihedrals also track the sign change caused by equivalent permutations.

    :param coord: A single coordinate specification or target coordinate.
    :type coord: Any
    :param return_sign: Whether to return the orientation sign together with the canonical coordinate.
    :type return_sign: Any
    :param check_invalid: Whether invalid coordinate lengths or repeated indices raise an error.
    :type check_invalid: Any
    :return: The canonical coordinate, optionally paired with its orientation sign.
    :rtype: tuple[int, ...] | tuple[tuple[int, ...], int]
    """
    ...

def is_valid_coordinate(coord):
    """
    **LLM Docstring**

    Return whether a value is an integer index sequence of length two, three, or four.

    :param coord: A single coordinate specification or target coordinate.
    :type coord: Any
    :return: Whether the tested condition is satisfied.
    :rtype: bool
    """
    ...

def is_coordinate_list_like(clist):
    """
    **LLM Docstring**

    Return whether every element of a sequence is a valid distance, angle, or dihedral specification.

    :param clist: Sequence to test as a coordinate list.
    :type clist: Any
    :return: Whether the tested condition is satisfied.
    :rtype: bool
    """
    ...

class RADInternalCoordinateSet:

    def __init__(self, coord_specs: 'list[tuple[int]]', prepped_data=None, triangulation=None):
        """
        **LLM Docstring**

        Preprocess coordinate specifications into canonical coordinate and index maps, retain the normalized coordinate list, and optionally store or derive triangulation data.

        :param coord_specs: Coordinate specifications to normalize and index.
        :type coord_specs: 'list[tuple[int]]'
        :param prepped_data: Previously prepared coordinate maps, used to avoid recomputation.
        :type prepped_data: Any
        :param triangulation: Optional precomputed triangle/dihedron representation.
        :type triangulation: Any
        :return: None.
        :rtype: None
        """
        ...

    @property
    def specs(self):
        """
        **LLM Docstring**

        Return the normalized coordinate specifications in their original coordinate-type grouping.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...
    IndicatorMap = collections.namedtuple('IndicatorMap', ['primary', 'child'])
    IndsMap = collections.namedtuple('IndsMap', ['dists', 'angles', 'diheds'])
    InternalsMap = collections.namedtuple('InternalsMap', ['dists', 'angles', 'diheds'])

    @classmethod
    def prep_coords(cls, coord_specs):
        """
        **LLM Docstring**

        Canonicalize input coordinates, group them by arity, deduplicate equivalent entries, and build maps between user coordinates, canonical coordinates, and flattened integer indices.

        :param coord_specs: Coordinate specifications to normalize and index.
        :type coord_specs: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

    @classmethod
    def _map_dispatch(cls, map, coord):
        """
        **LLM Docstring**

        Apply either a callable map or a lookup mapping to a coordinate, preserving coordinates not present in a partial mapping.

        :param map: Callable or mapping applied to a coordinate.
        :type map: Any
        :param coord: A single coordinate specification or target coordinate.
        :type coord: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

    def _coord_map_dispatch(self, coord):
        """
        **LLM Docstring**

        Map a coordinate through the set’s coordinate-level lookup.

        :param coord: A single coordinate specification or target coordinate.
        :type coord: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

    def _ind_map_dispatch(self, i):
        """
        **LLM Docstring**

        Map a flattened coordinate index through the set’s index-level lookup.

        :param i: An atom or flattened-coordinate index, depending on the helper.
        :type i: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

    def find(self, coord, missing_val='raise'):
        """
        **LLM Docstring**

        Locate a coordinate in the canonical coordinate map, respecting the requested value for missing coordinates.

        :param coord: A single coordinate specification or target coordinate.
        :type coord: Any
        :param missing_val: Value to return for a missing coordinate, or `"raise"` to raise.
        :type missing_val: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

    @classmethod
    def get_coord_from_maps(cls, item, indicator: IndicatorMap, ind_map, coord_map):
        """
        **LLM Docstring**

        Resolve an indexed selection through the indicator, flattened-index, and coordinate maps to recover the corresponding canonical coordinate specification.

        :param item: Index, slice, or coordinate selection to resolve.
        :type item: Any
        :param indicator: Coordinate-arity indicator array.
        :type indicator: IndicatorMap
        :param ind_map: Mapping from flattened coordinate positions to canonical coordinate indices.
        :type ind_map: Any
        :param coord_map: Mapping from canonical coordinate tuples to stored coordinate positions.
        :type coord_map: Any
        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

    def __getitem__(self, item):
        """
        **LLM Docstring**

        Support coordinate lookup and indexed/sliced selection through the precomputed coordinate maps.

        :param item: Index, slice, or coordinate selection to resolve.
        :type item: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

    @classmethod
    def _create_coord_list(cls, indicator, inds, vals: InternalsMap):
        """
        **LLM Docstring**

        Reconstruct coordinate tuples from a coordinate-type indicator array, flattened index data, and mapped coordinate values.

        :param indicator: Coordinate-arity indicator array.
        :type indicator: Any
        :param inds: Flattened coordinate index data.
        :type inds: Any
        :param vals: Mapped coordinate values used to reconstruct tuples.
        :type vals: InternalsMap
        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

    def permute(self, perm, canonicalize=True):
        """
        **LLM Docstring**

        Apply an atom permutation to every coordinate and return a new coordinate set, optionally canonicalizing the permuted coordinates.

        :param perm: Atom-index permutation or vertex permutation.
        :type perm: Any
        :param canonicalize: Whether to put coordinates in canonical orientation before comparison or storage.
        :type canonicalize: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

    def get_triangulation(self):
        """
        **LLM Docstring**

        Compute triangle and dihedron sets from the stored coordinates and cache the result.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

    @property
    def triangulation(self):
        """
        **LLM Docstring**

        Return the cached triangulation, computing it on first access.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

def get_canonical_internal_list(coords):
    """
    **LLM Docstring**

    Canonicalize every coordinate in a sequence and remove duplicates while preserving first-occurrence order.

    :param coords: Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
    :type coords: Any
    :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
    :rtype: Any
    """
    ...

def find_internal(coords, coord, missing_val: 'Any'='raise', canonicalize=True, allow_negation=False, indices=None):
    """
    **LLM Docstring**

    Find a coordinate in a coordinate list after optional canonicalization. The search can accept the sign-reversed equivalent of directed coordinates and can restrict matching to a supplied index subset.

    :param coords: Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
    :type coords: Any
    :param coord: A single coordinate specification or target coordinate.
    :type coord: Any
    :param missing_val: Value to return for a missing coordinate, or `"raise"` to raise.
    :type missing_val: 'Any'
    :param canonicalize: Whether to put coordinates in canonical orientation before comparison or storage.
    :type canonicalize: Any
    :param allow_negation: Whether sign-reversed directed coordinates count as matches.
    :type allow_negation: Any
    :param indices: Atom indices defining the coordinate, or a restricted search index set.
    :type indices: Any
    :return: The value or updated object described above.
    :rtype: Any
    """
    ...

def permute_internals(coords, perm, canonicalize=True):
    """
    **LLM Docstring**

    Apply an atom-index permutation to each coordinate and optionally canonicalize the resulting coordinate orientations.

    :param coords: Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
    :type coords: Any
    :param perm: Atom-index permutation or vertex permutation.
    :type perm: Any
    :param canonicalize: Whether to put coordinates in canonical orientation before comparison or storage.
    :type canonicalize: Any
    :return: The value or updated object described above.
    :rtype: Any
    """
    ...

def coordinate_sign(old, new, canonicalize=True):
    """
    **LLM Docstring**

    Determine whether two equivalent coordinate specifications have the same or opposite orientation, returning `1`, `-1`, or `0` when they are not equivalent.

    :param old: Original coordinate orientation used as the sign reference.
    :type old: Any
    :param new: Coordinates newly added to the graph.
    :type new: Any
    :param canonicalize: Whether to put coordinates in canonical orientation before comparison or storage.
    :type canonicalize: Any
    :return: `1` for equal orientation, `-1` for reversed orientation, or `0` for nonequivalent coordinates.
    :rtype: int
    """
    ...

def coordinate_indices(coords):
    """
    **LLM Docstring**

    Flatten a coordinate list into an integer array and return the per-coordinate arity indicators needed to reconstruct the original tuples.

    :param coords: Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
    :type coords: Any
    :return: The flattened coordinate indices and per-coordinate arity indicators.
    :rtype: tuple[np.ndarray, np.ndarray]
    """
    ...
dm_conv_data = collections.namedtuple('dm_conv_data', ['input_indices', 'pregen_indices', 'conversion', 'mapped_pos'])
tri_conv = collections.namedtuple('tri_conv', ['type', 'coords', 'val'])
dihed_conv = collections.namedtuple('dihed_conv', ['type', 'coords'])

def _get_input_ind(dm_data):
    """
    **LLM Docstring**

    Return the stored index selecting an original internal-coordinate value from a distance-conversion record.

    :param dm_data: Distance-conversion record containing source-index metadata.
    :type dm_data: Any
    :return: The value or updated object described above.
    :rtype: Any
    """
    ...

def _get_pregen_ind(dm_data):
    """
    **LLM Docstring**

    Return the stored index selecting a previously generated distance from a distance-conversion record.

    :param dm_data: Distance-conversion record containing source-index metadata.
    :type dm_data: Any
    :return: The value or updated object described above.
    :rtype: Any
    """
    ...

def get_internal_distance_conversion_spec(internals, canonicalize=True, cache=None):
    """
    **LLM Docstring**

    Analyze distances, angles, and dihedrals to produce an ordered recipe for reconstructing every required pair distance. Each recipe entry records whether its inputs come directly from the internal vector or from distances generated by earlier entries.

    :param internals: Available internal-coordinate specifications or their numerical values.
    :type internals: Any
    :param canonicalize: Whether to put coordinates in canonical orientation before comparison or storage.
    :type canonicalize: Any
    :param cache: Optional mutable cache of triangulation or conversion results.
    :type cache: Any
    :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
    :rtype: Any
    """
    ...

def _prep_interal_distance_conversion(conversion_spec: dm_conv_data):
    """
    **LLM Docstring**

    Compile a distance-conversion specification into a callable specialized for direct distances, law-of-cosines triangle completion, or dihedral tetrahedron completion.

    :param conversion_spec: Ordered recipe describing how each distance is obtained.
    :type conversion_spec: dm_conv_data
    :return: The value or updated object described above.
    :rtype: Any
    """
    ...

def _get_internal_distance_conversion(internals, canonicalize=True, shift_dihedrals=True, abs_dihedrals=True):
    """
    **LLM Docstring**

    Return the conversion specification together with a callable that evaluates it sequentially, optionally normalizing dihedral signs and absolute values before tetrahedral reconstruction.

    :param internals: Available internal-coordinate specifications or their numerical values.
    :type internals: Any
    :param canonicalize: Whether to put coordinates in canonical orientation before comparison or storage.
    :type canonicalize: Any
    :param shift_dihedrals: Whether periodic dihedral values are shifted to the expected reconstruction branch.
    :type shift_dihedrals: Any
    :param abs_dihedrals: Whether dihedral magnitudes are used for distance reconstruction.
    :type abs_dihedrals: Any
    :return: The value or updated object described above.
    :rtype: Any
    """
    ...

def _check_complete_distances(final_dists):
    """
    **LLM Docstring**

    Verify that a generated distance set contains every pair needed for the inferred atom range; raise an error listing missing pairs when it does not.

    :param final_dists: Generated pair-distance mapping or sequence to validate.
    :type final_dists: Any
    :return: The value or updated object described above.
    :rtype: Any
    """
    ...

def internal_distance_convert(coords, specs, canonicalize=True, shift_dihedrals=True, abs_dihedrals=True, check_distance_spec=True):
    """
    **LLM Docstring**

    Convert internal-coordinate values to pair distances using a precomputed or newly generated conversion specification, optionally returning only generated values or validating distance completeness.

    :param coords: Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
    :type coords: Any
    :param specs: Coordinate specifications associated with the numerical values.
    :type specs: Any
    :param canonicalize: Whether to put coordinates in canonical orientation before comparison or storage.
    :type canonicalize: Any
    :param shift_dihedrals: Whether periodic dihedral values are shifted to the expected reconstruction branch.
    :type shift_dihedrals: Any
    :param abs_dihedrals: Whether dihedral magnitudes are used for distance reconstruction.
    :type abs_dihedrals: Any
    :param check_distance_spec: Whether the supplied distance-conversion specification is checked for completeness.
    :type check_distance_spec: Any
    :return: The value or updated object described above.
    :rtype: Any
    """
    ...

def _find_coord_comp(coord, a, internals, prior_coords, missing_val):
    """
    **LLM Docstring**

    Find a coordinate containing a requested atom combination and return the matching coordinate plus its position, consulting prior-coordinate aliases before applying the requested missing-value behavior.

    :param coord: A single coordinate specification or target coordinate.
    :type coord: Any
    :param a: Atom whose containing coordinate or attachment is being sought.
    :type a: Any
    :param internals: Available internal-coordinate specifications or their numerical values.
    :type internals: Any
    :param prior_coords: Aliases for coordinates generated earlier in the dependency chain.
    :type prior_coords: Any
    :param missing_val: Value to return for a missing coordinate, or `"raise"` to raise.
    :type missing_val: Any
    :return: The value or updated object described above.
    :rtype: Any
    """
    ...
_tri_perms = [(0, 1, 2), (0, 2, 1), (1, 0, 2)]
_tri_perm_inv = _tri_perms

def _get_tri_bond_key_name(mod_sets, a, b, c, i, j):
    """
    **LLM Docstring**

    Classify one triangle edge as an existing internal, a prior generated distance, or a newly generated distance, and return the key/index metadata used in the triangle conversion recipe.

    :param mod_sets: Mutable triangulation-term sets used while classifying an edge or angular term.
    :type mod_sets: Any
    :param a: Atom whose containing coordinate or attachment is being sought.
    :type a: Any
    :param b: Second atom in the local triangle or tetrahedron.
    :type b: Any
    :param c: Third atom in the local triangle or tetrahedron.
    :type c: Any
    :param i: An atom or flattened-coordinate index, depending on the helper.
    :type i: Any
    :param j: Second local vertex or coordinate index.
    :type j: Any
    :return: The value or updated object described above.
    :rtype: Any
    """
    ...

def _permute_tri_data(terms, perm):
    """
    **LLM Docstring**

    Permute triangle recipe terms into a new vertex ordering while updating edge labels and orientation-dependent angle data.

    :param terms: Triangle or dihedron conversion metadata to permute.
    :type terms: Any
    :param perm: Atom-index permutation or vertex permutation.
    :type perm: Any
    :return: The value or updated object described above.
    :rtype: Any
    """
    ...

def _get_dihedron_bond_key_name(mod_sets, a, b, c, d, i, j):
    """
    **LLM Docstring**

    Classify one tetrahedron edge as an input distance, prior generated distance, or new generated distance for a dihedron recipe.

    :param mod_sets: Mutable triangulation-term sets used while classifying an edge or angular term.
    :type mod_sets: Any
    :param a: Atom whose containing coordinate or attachment is being sought.
    :type a: Any
    :param b: Second atom in the local triangle or tetrahedron.
    :type b: Any
    :param c: Third atom in the local triangle or tetrahedron.
    :type c: Any
    :param d: Fourth atom in the local tetrahedron.
    :type d: Any
    :param i: An atom or flattened-coordinate index, depending on the helper.
    :type i: Any
    :param j: Second local vertex or coordinate index.
    :type j: Any
    :return: The value or updated object described above.
    :rtype: Any
    """
    ...

def _get_dihedron_angle_key_name(mod_sets, a, b, c, d, i, j, k):
    """
    **LLM Docstring**

    Classify a tetrahedral face angle as an input angle or a value derivable from its three surrounding distances.

    :param mod_sets: Mutable triangulation-term sets used while classifying an edge or angular term.
    :type mod_sets: Any
    :param a: Atom whose containing coordinate or attachment is being sought.
    :type a: Any
    :param b: Second atom in the local triangle or tetrahedron.
    :type b: Any
    :param c: Third atom in the local triangle or tetrahedron.
    :type c: Any
    :param d: Fourth atom in the local tetrahedron.
    :type d: Any
    :param i: An atom or flattened-coordinate index, depending on the helper.
    :type i: Any
    :param j: Second local vertex or coordinate index.
    :type j: Any
    :param k: Third local vertex or candidate dihedron key.
    :type k: Any
    :return: The value or updated object described above.
    :rtype: Any
    """
    ...

def _get_dihedron_dihed_key_name(mod_sets, a, b, c, d, i, j, k, l):
    """
    **LLM Docstring**

    Classify a torsion around a tetrahedral edge as an input dihedral or as a value reconstructable from the tetrahedron’s distances.

    :param mod_sets: Mutable triangulation-term sets used while classifying an edge or angular term.
    :type mod_sets: Any
    :param a: Atom whose containing coordinate or attachment is being sought.
    :type a: Any
    :param b: Second atom in the local triangle or tetrahedron.
    :type b: Any
    :param c: Third atom in the local triangle or tetrahedron.
    :type c: Any
    :param d: Fourth atom in the local tetrahedron.
    :type d: Any
    :param i: An atom or flattened-coordinate index, depending on the helper.
    :type i: Any
    :param j: Second local vertex or coordinate index.
    :type j: Any
    :param k: Third local vertex or candidate dihedron key.
    :type k: Any
    :param l: Fourth local vertex index.
    :type l: Any
    :return: The value or updated object described above.
    :rtype: Any
    """
    ...

def _permute_dihed_data(terms, perm):
    """
    **LLM Docstring**

    Apply a four-vertex permutation to all bond, angle, and dihedral terms in a dihedron recipe and update orientation signs.

    :param terms: Triangle or dihedron conversion metadata to permute.
    :type terms: Any
    :param perm: Atom-index permutation or vertex permutation.
    :type perm: Any
    :return: The value or updated object described above.
    :rtype: Any
    """
    ...

def _validate_dihed_triangulation(mod_sets, key, internals, adding=None):
    """
    **LLM Docstring**

    Check that a proposed dihedron has enough known coordinate information to be completed and optionally account for terms being added in the current step.

    :param mod_sets: Mutable triangulation-term sets used while classifying an edge or angular term.
    :type mod_sets: Any
    :param key: Triangulation record key being validated.
    :type key: Any
    :param internals: Available internal-coordinate specifications or their numerical values.
    :type internals: Any
    :param adding: Terms treated as available during the current update.
    :type adding: Any
    :return: The value or updated object described above.
    :rtype: Any
    """
    ...

def _check_tri_coords(internals, tri_sets):
    """
    **LLM Docstring**

    Validate that each triangle set is supported by the required distances and angle coordinate information.

    :param internals: Available internal-coordinate specifications or their numerical values.
    :type internals: Any
    :param tri_sets: Triangle records to validate.
    :type tri_sets: Any
    :return: The value or updated object described above.
    :rtype: Any
    """
    ...

def _check_dihed_coords(internals, dihed_sets):
    """
    **LLM Docstring**

    Validate that each dihedron set is supported by enough bond, angle, and torsional information for tetrahedral reconstruction.

    :param internals: Available internal-coordinate specifications or their numerical values.
    :type internals: Any
    :param dihed_sets: Dihedron records to validate.
    :type dihed_sets: Any
    :return: The value or updated object described above.
    :rtype: Any
    """
    ...

def get_internal_triangles_and_dihedrons(internals, canonicalize=True, base=None, base_internals=None, construct_shapes=True, prune_incomplete=True, validate=False, allow_partially_defined=True, create_compound_dihedra=True, add_dihedron_triangles=False, create_dihedra=True) -> tuple[dict[tuple[int, int, int], nput.TriangleData], dict[tuple[int, int, int, int], nput.DihedralTetrahedronData]]:
    """
    **LLM Docstring**

    Construct a dependency-ordered triangulation of an internal-coordinate set. It identifies complete triangles and tetrahedra, records how missing pair distances are generated from angles or dihedrals, and can return auxiliary maps describing coordinate provenance and unresolved terms.

    :param internals: Available internal-coordinate specifications or their numerical values.
    :type internals: Any
    :param canonicalize: Whether to put coordinates in canonical orientation before comparison or storage.
    :type canonicalize: Any
    :param base: Existing triangulation data used as the starting point for adding new coordinates.
    :type base: Any
    :param base_internals: Coordinates already accepted by the nonredundancy checker.
    :type base_internals: Any
    :param construct_shapes: Whether explicit triangle and dihedron shape records are constructed rather than only dependency metadata.
    :type construct_shapes: Any
    :param prune_incomplete: Whether triangle or dihedron candidates lacking enough defining information are discarded.
    :type prune_incomplete: Any
    :param validate: Whether the resulting triangulation is checked for consistency before being returned.
    :type validate: Any
    :param allow_partially_defined: Whether shapes with unresolved terms are retained for later completion.
    :type allow_partially_defined: Any
    :param create_compound_dihedra: Whether overlapping dihedrons may be combined into compound conversion records.
    :type create_compound_dihedra: Any
    :param add_dihedron_triangles: Whether triangular faces implied by accepted dihedrons are inserted into the triangle set.
    :type add_dihedron_triangles: Any
    :param create_dihedra: Whether four-atom dihedron records are generated at all.
    :type create_dihedra: Any
    :return: Triangle and dihedron triangulation records, with optional auxiliary conversion data selected by the function options.
    :rtype: tuple
    """
    ...

def get_triangulation_internals(triangulation: tuple[dict[tuple[int, int, int], nput.TriangleData], dict[tuple[int, int, int, int], nput.DihedralTetrahedronData]]):
    """
    **LLM Docstring**

    Extract the primitive distance, angle, and dihedral coordinates represented by triangle and dihedron triangulation records.

    :param triangulation: Optional precomputed triangle/dihedron representation.
    :type triangulation: tuple[dict[tuple[int, int, int], nput.TriangleData], dict[tuple[int, int, int, int], nput.DihedralTetrahedronData]]
    :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
    :rtype: Any
    """
    ...

def get_core_triangulation(internal_bag, targets, intersection='partial', cache=None, **kwargs):
    """
    **LLM Docstring**

    Reduce a triangulation to the connected subset needed to support target coordinates, retaining records that fully or partially intersect the target atom sets according to `intersection`.

    :param internal_bag: Available triangulation records or coordinates.
    :type internal_bag: Any
    :param targets: Coordinates or atom sets whose supporting triangulation is requested.
    :type targets: Any
    :param intersection: Rule controlling whether partial or complete atom-set overlap retains a record.
    :type intersection: Any
    :param cache: Optional mutable cache of triangulation or conversion results.
    :type cache: Any
    :param kwargs: Additional options forwarded to the triangulation reduction or merge routine.
    :type kwargs: Any
    :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
    :rtype: Any
    """
    ...

def _merge_shapes(new_shapes, old_shapes, perms, perm_invs, prop_func, in_place=False, merge_strategy='both'):
    """
    **LLM Docstring**

    Merge permuted triangle or dihedron records with an existing set, reconcile shape/broadcast dimensions, and update property caches for records that become equivalent after permutation.

    :param new_shapes: Modified triangle or dihedron records to merge.
    :type new_shapes: Any
    :param old_shapes: Existing records into which modified records are merged.
    :type old_shapes: Any
    :param perms: Allowed vertex permutations for each record type.
    :type perms: Any
    :param perm_invs: Inverse permutations used to restore canonical metadata ordering.
    :type perm_invs: Any
    :param prop_func: Function that computes record properties used during merging.
    :type prop_func: Any
    :param in_place: Whether the supplied triangulation containers are mutated instead of copied.
    :type in_place: Any
    :param merge_strategy: Policy used to reconcile equivalent records and conflicting conversion metadata.
    :type merge_strategy: Any
    :return: The value or updated object described above.
    :rtype: Any
    """
    ...

def merge_dihedral_sets(sub_diheds, unmodified_diheds, in_place=False, merge_strategy='both'):
    """
    **LLM Docstring**

    Merge modified dihedron records back into unmodified records while canonicalizing equivalent vertex permutations and preserving conversion metadata.

    :param sub_diheds: Modified dihedron records.
    :type sub_diheds: Any
    :param unmodified_diheds: Dihedron records unaffected by the update.
    :type unmodified_diheds: Any
    :param in_place: Whether the supplied triangulation containers are mutated instead of copied.
    :type in_place: Any
    :param merge_strategy: Policy used to reconcile equivalent records and conflicting conversion metadata.
    :type merge_strategy: Any
    :return: The value or updated object described above.
    :rtype: Any
    """
    ...

def merge_triangle_sets(sub_tris, unmodified_tris, in_place=False, merge_strategy='both'):
    """
    **LLM Docstring**

    Merge modified triangle records back into unmodified records while canonicalizing equivalent vertex permutations and preserving conversion metadata.

    :param sub_tris: Modified triangle records.
    :type sub_tris: Any
    :param unmodified_tris: Triangle records unaffected by the update.
    :type unmodified_tris: Any
    :param in_place: Whether the supplied triangulation containers are mutated instead of copied.
    :type in_place: Any
    :param merge_strategy: Policy used to reconcile equivalent records and conflicting conversion metadata.
    :type merge_strategy: Any
    :return: The value or updated object described above.
    :rtype: Any
    """
    ...

def update_triangulation(triangulation: tuple[dict[tuple[int, int, int], nput.TriangleData], dict[tuple[int, int, int, int], nput.DihedralTetrahedronData]], added_internals, removed_internals, triangulation_internals=None, return_split=False, validate=False):
    """
    **LLM Docstring**

    Update triangle and dihedron records after coordinates are added, removed, or replaced. The routine rewrites affected terms, generates newly completable shapes, merges equivalent records, and returns the updated triangulation plus optional bookkeeping.

    :param triangulation: Optional precomputed triangle/dihedron representation.
    :type triangulation: tuple[dict[tuple[int, int, int], nput.TriangleData], dict[tuple[int, int, int, int], nput.DihedralTetrahedronData]]
    :param added_internals: Coordinates being introduced into the triangulation.
    :type added_internals: Any
    :param removed_internals: Coordinates being deleted from the triangulation.
    :type removed_internals: Any
    :param triangulation_internals: Cached primitive coordinates represented by the existing triangulation.
    :type triangulation_internals: Any
    :param return_split: Whether updated and untouched triangulation subsets are returned separately.
    :type return_split: Any
    :param validate: Whether the resulting triangulation is checked for consistency before being returned.
    :type validate: Any
    :return: The value or updated object described above.
    :rtype: Any
    """
    ...

def _triangle_conversion_function(inds, tri, coord):
    """
    **LLM Docstring**

    Create a callable that computes a requested triangle coordinate or missing edge from the triangle’s three pair distances.

    :param inds: Flattened coordinate index data.
    :type inds: Any
    :param tri: Triangle record supplying the three pair distances used by the conversion.
    :type tri: Any
    :param coord: A single coordinate specification or target coordinate.
    :type coord: Any
    :return: The value or updated object described above.
    :rtype: Any
    """
    ...

def _dihedral_conversion_function(inds, dihed, coord, allow_completion=True, cache=None, completion_handler=None, disallowed_conversions=None, allow_ambiguous_completions=False, verbose=False):
    """
    **LLM Docstring**

    Create a callable that evaluates a requested bond, angle, or dihedral from one tetrahedron’s six pair distances, optionally completing missing terms and reporting completion provenance.

    :param inds: Flattened coordinate index data.
    :type inds: Any
    :param dihed: Dihedron record supplying the six tetrahedral pair distances used by the conversion.
    :type dihed: Any
    :param coord: A single coordinate specification or target coordinate.
    :type coord: Any
    :param allow_completion: Whether missing intermediate coordinates may be reconstructed.
    :type allow_completion: Any
    :param cache: Optional mutable cache of triangulation or conversion results.
    :type cache: Any
    :param completion_handler: Callback that records completed intermediate coordinates.
    :type completion_handler: Any
    :param disallowed_conversions: Coordinate conversions that must not be used while searching for a target conversion.
    :type disallowed_conversions: Any
    :param allow_ambiguous_completions: Whether a missing intermediate may be accepted when more than one completion path exists.
    :type allow_ambiguous_completions: Any
    :param verbose: Whether diagnostic information is emitted during the search.
    :type verbose: Any
    :return: The value or updated object described above.
    :rtype: Any
    """
    ...

def _pair_dihedral_conversion_function(inds1, dihed1, inds2, dihed2, coord, raise_on_invalid=True, cache=None):
    """
    **LLM Docstring**

    Create a callable that evaluates a target coordinate using two overlapping tetrahedra when no single dihedron record contains all required atoms.

    :param inds1: Distance indices for the first tetrahedron.
    :type inds1: Any
    :param dihed1: First tetrahedron conversion record.
    :type dihed1: Any
    :param inds2: Distance indices for the second tetrahedron.
    :type inds2: Any
    :param dihed2: Second tetrahedron conversion record.
    :type dihed2: Any
    :param coord: A single coordinate specification or target coordinate.
    :type coord: Any
    :param raise_on_invalid: Whether an invalid or unsupported target conversion raises instead of returning the missing value.
    :type raise_on_invalid: Any
    :param cache: Optional mutable cache of triangulation or conversion results.
    :type cache: Any
    :return: The value or updated object described above.
    :rtype: Any
    """
    ...

class InternalCoordinateConversion:

    def __init__(self, caller, provenance, name=None):
        """
        **LLM Docstring**

        Store a conversion callable together with provenance describing which triangulation records and source coordinates support it.

        :param caller: Callable that evaluates the conversion.
        :type caller: Any
        :param provenance: Metadata describing the source records and coordinates used by the conversion.
        :type provenance: Any
        :param name: Optional display name for the conversion.
        :type name: Any
        :return: None.
        :rtype: None
        """
        ...

    def __call__(self, internals, **opts):
        """
        **LLM Docstring**

        Evaluate the stored conversion callable on an internal-coordinate value array.

        :param internals: Available internal-coordinate specifications or their numerical values.
        :type internals: Any
        :param opts: Additional options forwarded to the numerical conversion routine.
        :type opts: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Format the conversion using its assigned name and provenance description.

        :return: A concise representation of the object.
        :rtype: str
        """
        ...
int_conv_data = collections.namedtuple('int_conv_data', ['input_indices', 'pregen_indices', 'conversion'])

def find_internal_conversion(internals, targets, triangles_and_dihedrons=None, canonicalize=True, allow_completion=True, return_conversions=False, prep_conversions=True, include_shapes=False, indices=None, cache=None, disallowed_conversions=None, update_triangles_and_dihedrons=False, return_completions=False, allow_recursive_completions=None, allow_ambiguous_completions=False, dihedral_intersections=None, index_mapping=None, verbose=False, missing_val='raise'):
    """
    **LLM Docstring**

    Build a conversion from an available internal-coordinate set to requested target coordinates. It first reuses direct coordinates, then searches triangle and dihedron records, completion relations, and paired tetrahedra, returning conversion callables with provenance for each target.

    :param internals: Available internal-coordinate specifications or their numerical values.
    :type internals: Any
    :param targets: Coordinates or atom sets whose supporting triangulation is requested.
    :type targets: Any
    :param triangles_and_dihedrons: Precomputed triangle and dihedron records used instead of rebuilding the triangulation.
    :type triangles_and_dihedrons: Any
    :param canonicalize: Whether to put coordinates in canonical orientation before comparison or storage.
    :type canonicalize: Any
    :param allow_completion: Whether missing intermediate coordinates may be reconstructed.
    :type allow_completion: Any
    :param return_conversions: Whether conversion objects and provenance are returned rather than only converted values.
    :type return_conversions: Any
    :param prep_conversions: Whether returned conversion specifications are wrapped as directly callable objects.
    :type prep_conversions: Any
    :param include_shapes: Whether shape records supporting each conversion are included in the result metadata.
    :type include_shapes: Any
    :param indices: Atom indices defining the coordinate, or a restricted search index set.
    :type indices: Any
    :param cache: Optional mutable cache of triangulation or conversion results.
    :type cache: Any
    :param disallowed_conversions: Coordinate conversions that must not be used while searching for a target conversion.
    :type disallowed_conversions: Any
    :param update_triangles_and_dihedrons: Whether completed intermediate coordinates are inserted back into the working triangulation.
    :type update_triangles_and_dihedrons: Any
    :param return_completions: Whether conversions for newly reconstructed intermediate coordinates are returned.
    :type return_completions: Any
    :param allow_recursive_completions: Whether completing one coordinate may recursively request additional intermediate completions.
    :type allow_recursive_completions: Any
    :param allow_ambiguous_completions: Whether a missing intermediate may be accepted when more than one completion path exists.
    :type allow_ambiguous_completions: Any
    :param dihedral_intersections: Allowed overlap rules when combining multiple dihedron records for a conversion.
    :type dihedral_intersections: Any
    :param index_mapping: Optional mapping from canonical coordinate indices to columns in the supplied value array.
    :type index_mapping: Any
    :param verbose: Whether diagnostic information is emitted during the search.
    :type verbose: Any
    :param missing_val: Value to return for a missing coordinate, or `"raise"` to raise.
    :type missing_val: Any
    :return: Conversion objects or a combined callable that produces the requested target coordinates.
    :rtype: Any
    """
    ...

def _enumerate_dists(internals):
    """
    **LLM Docstring**

    Return the canonical set of explicit distance pairs present in an internal-coordinate list.

    :param internals: Available internal-coordinate specifications or their numerical values.
    :type internals: Any
    :return: An iterator yielding the candidates described above.
    :rtype: Iterator
    """
    ...
_dihed_check_sets = []

def _get_dihedron_checks():
    """
    **LLM Docstring**

    Return cached atom-position combinations used to test whether a tetrahedron can attach a new atom to an existing Z-matrix tree.

    :return: The value or updated object described above.
    :rtype: Any
    """
    ...
_dihedron_index_props = {}

def _get_dihedron_index_props():
    """
    **LLM Docstring**

    Return cached lookup data describing the root, attachment, and new-atom positions for each dihedron attachment permutation.

    :return: The value or updated object described above.
    :rtype: Any
    """
    ...

def _dihedron_completable(k, dihed_data, known_atom_graph, max_comps=5):
    """
    **LLM Docstring**

    Test whether a dihedron record has a permutation whose attachment atoms are already connected and whose remaining atom can be introduced, subject to a maximum number of disconnected components.

    :param k: Third local vertex or candidate dihedron key.
    :type k: Any
    :param dihed_data: Dihedron triangulation record being tested.
    :type dihed_data: Any
    :param known_atom_graph: Connectivity graph of atoms already placed in the partial Z-matrix.
    :type known_atom_graph: Any
    :param max_comps: Maximum disconnected components allowed after attachment.
    :type max_comps: Any
    :return: Whether the tested condition is satisfied.
    :rtype: bool
    """
    ...

def _get_matching_dihedrals(a, dihedral_set, internals, *, check_complete=False, d_prop_cache=[None]):
    """
    **LLM Docstring**

    Find dihedron records containing a specified atom, optionally requiring each record to be complete, and return their matching attachment permutations.

    :param a: Atom whose containing coordinate or attachment is being sought.
    :type a: Any
    :param dihedral_set: Available dihedron records.
    :type dihedral_set: Any
    :param internals: Available internal-coordinate specifications or their numerical values.
    :type internals: Any
    :param check_complete: Whether a candidate shape or distance set must be fully populated before acceptance.
    :type check_complete: Any
    :param d_prop_cache: Cache of dihedron attachment properties.
    :type d_prop_cache: Any
    :return: The value or updated object described above.
    :rtype: Any
    """
    ...

def enumarate_zmatrix_roots_from_triangles(atoms, tris, connectivity_graph):
    """
    **LLM Docstring**

    Enumerate three-atom Z-matrix roots from complete triangles whose atoms satisfy the connectivity graph, yielding root orderings and the triangle record supporting each root.

    :param atoms: Atoms to include or place.
    :type atoms: Any
    :param tris: Triangle triangulation records.
    :type tris: Any
    :param connectivity_graph: Graph restricting admissible root and attachment orderings.
    :type connectivity_graph: Any
    :return: An iterator yielding the candidates described above.
    :rtype: Iterator
    """
    ...

def construct_atom_connection_graph_from_triangulation(internals, tris, dihedrons):
    """
    **LLM Docstring**

    Build an atom adjacency graph from explicit distances and from edges implied by triangle and dihedron records, and return lookup maps from atoms or edges to supporting triangulation records.

    :param internals: Available internal-coordinate specifications or their numerical values.
    :type internals: Any
    :param tris: Triangle triangulation records.
    :type tris: Any
    :param dihedrons: Available dihedron triangulation records.
    :type dihedrons: Any
    :return: The value or updated object described above.
    :rtype: Any
    """
    ...

def _check_populated_dihedral_complete(k, dihed_data, known_atoms, choice, *, cached_data=[None]):
    """
    **LLM Docstring**

    Check whether a candidate dihedron attachment has all required populated terms for the chosen atom ordering, caching invariant lookup information.

    :param k: Third local vertex or candidate dihedron key.
    :type k: Any
    :param dihed_data: Dihedron triangulation record being tested.
    :type dihed_data: Any
    :param known_atoms: Atoms already placed in the current partial ordering.
    :type known_atoms: Any
    :param choice: Candidate attachment permutation.
    :type choice: Any
    :param cached_data: Reusable attachment-position data cached across repeated completeness checks.
    :type cached_data: Any
    :return: Whether the tested condition is satisfied.
    :rtype: bool
    """
    ...

def _grow_dihedral_trees(root, atoms, top_dihedral_choices, secondary_dihedral_choices, incomplete_dihedrals=None, internals=None, *, traversal='dfs'):
    """
    **LLM Docstring**

    Recursively extend a Z-matrix atom ordering from a three-atom root by attaching atoms through compatible complete dihedrons, tracking used records, connectivity, branch limits, and optional filters.

    :param root: Three-atom root ordering for Z-matrix growth.
    :type root: Any
    :param atoms: Atoms to include or place.
    :type atoms: Any
    :param top_dihedral_choices: Primary dihedron attachments available from the current tree frontier.
    :type top_dihedral_choices: Any
    :param secondary_dihedral_choices: Fallback dihedron attachments considered when primary choices cannot extend the tree.
    :type secondary_dihedral_choices: Any
    :param incomplete_dihedrals: Dihedron records retained for later completion but not currently usable for attachment.
    :type incomplete_dihedrals: Any
    :param internals: Available internal-coordinate specifications or their numerical values.
    :type internals: Any
    :param traversal: Current ordered atom traversal and its supporting attachment records.
    :type traversal: Any
    :return: An iterator yielding the candidates described above.
    :rtype: Iterator
    """
    ...

def get_fragments_from_internals(internals, triangles_and_dihedrons=None):
    """
    **LLM Docstring**

    Construct the bond graph implied by internal coordinates and return its connected atom fragments, with optional atom inclusion and triangulation-derived edges.

    :param internals: Available internal-coordinate specifications or their numerical values.
    :type internals: Any
    :param triangles_and_dihedrons: Precomputed triangle and dihedron records used instead of rebuilding the triangulation.
    :type triangles_and_dihedrons: Any
    :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
    :rtype: Any
    """
    ...

def enumerate_zmatrices_from_internals(internals, triangles_and_dihedrons=None, atoms=None, ordering=None, graph=None, build_conversion=True, max_ordering_passes=1, **conversion_options):
    """
    **LLM Docstring**

    Enumerate Z-matrix index arrays compatible with an internal-coordinate set. It builds triangulation and connectivity data, chooses triangle roots, grows valid dihedral attachment trees, filters duplicates or user-rejected candidates, and can return supporting conversion metadata.

    :param internals: Available internal-coordinate specifications or their numerical values.
    :type internals: Any
    :param triangles_and_dihedrons: Precomputed triangle and dihedron records used instead of rebuilding the triangulation.
    :type triangles_and_dihedrons: Any
    :param atoms: Atoms to include or place.
    :type atoms: Any
    :param ordering: Optional preferred atom ordering used to seed or constrain Z-matrix enumeration.
    :type ordering: Any
    :param graph: Connectivity graph used to test distance inference.
    :type graph: Any
    :param build_conversion: Whether each enumerated Z-matrix is accompanied by a conversion from the source internals.
    :type build_conversion: Any
    :param max_ordering_passes: Maximum number of attempts to extend or revise a candidate atom ordering.
    :type max_ordering_passes: Any
    :param conversion_options: Options forwarded when constructing conversions for enumerated Z-matrices.
    :type conversion_options: Any
    :return: An iterator over compatible Z-matrix index arrays, optionally paired with supporting metadata.
    :rtype: Iterator
    """
    ...

def get_internal_distance_conversion(internals, triangles_and_dihedrons=None, dist_set=None, canonicalize=True, allow_completion=True, missing_val='raise', include_shapes=False, return_conversions=False, prep_conversions=True, cache=None):
    """
    **LLM Docstring**

    Return a callable that transforms internal-coordinate values into the pair distances required by their triangulation, along with optional conversion metadata.

    :param internals: Available internal-coordinate specifications or their numerical values.
    :type internals: Any
    :param triangles_and_dihedrons: Precomputed triangle and dihedron records used instead of rebuilding the triangulation.
    :type triangles_and_dihedrons: Any
    :param dist_set: Optional known canonical distance set.
    :type dist_set: Any
    :param canonicalize: Whether to put coordinates in canonical orientation before comparison or storage.
    :type canonicalize: Any
    :param allow_completion: Whether missing intermediate coordinates may be reconstructed.
    :type allow_completion: Any
    :param missing_val: Value to return for a missing coordinate, or `"raise"` to raise.
    :type missing_val: Any
    :param include_shapes: Whether shape records supporting each conversion are included in the result metadata.
    :type include_shapes: Any
    :param return_conversions: Whether conversion objects and provenance are returned rather than only converted values.
    :type return_conversions: Any
    :param prep_conversions: Whether returned conversion specifications are wrapped as directly callable objects.
    :type prep_conversions: Any
    :param cache: Optional mutable cache of triangulation or conversion results.
    :type cache: Any
    :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
    :rtype: Any
    """
    ...

def get_internal_cartesian_conversion(internals, triangles_and_dihedrons=None, canonicalize=True, missing_val='raise'):
    """
    **LLM Docstring**

    Construct a converter from internal-coordinate values to Cartesian geometries by composing internal-to-distance conversion with distance-geometry embedding.

    :param internals: Available internal-coordinate specifications or their numerical values.
    :type internals: Any
    :param triangles_and_dihedrons: Precomputed triangle and dihedron records used instead of rebuilding the triangulation.
    :type triangles_and_dihedrons: Any
    :param canonicalize: Whether to put coordinates in canonical orientation before comparison or storage.
    :type canonicalize: Any
    :param missing_val: Value to return for a missing coordinate, or `"raise"` to raise.
    :type missing_val: Any
    :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
    :rtype: Any
    """
    ...

def validate_internals(internals, triangles_and_dihedrons=None, raise_on_failure=True):
    """
    **LLM Docstring**

    Validate that an internal-coordinate set can produce a complete, consistent triangulation and optionally raise an exception containing the unresolved coordinates.

    :param internals: Available internal-coordinate specifications or their numerical values.
    :type internals: Any
    :param triangles_and_dihedrons: Precomputed triangle and dihedron records used instead of rebuilding the triangulation.
    :type triangles_and_dihedrons: Any
    :param raise_on_failure: Whether unresolved triangulation or conversion terms raise an exception.
    :type raise_on_failure: Any
    :return: Whether the coordinate set passes triangulation validation.
    :rtype: bool
    """
    ...

def get_internal_bond_graph(internals, atoms=None, triangles_and_dihedrons=None, dist_set=None, return_conversions=False, complete_graph=False):
    """
    **LLM Docstring**

    Build an `EdgeGraph` from explicit and triangulation-implied bond distances, optionally including isolated atoms and returning supporting edge metadata.

    :param internals: Available internal-coordinate specifications or their numerical values.
    :type internals: Any
    :param atoms: Atoms to include or place.
    :type atoms: Any
    :param triangles_and_dihedrons: Precomputed triangle and dihedron records used instead of rebuilding the triangulation.
    :type triangles_and_dihedrons: Any
    :param dist_set: Optional known canonical distance set.
    :type dist_set: Any
    :param return_conversions: Whether conversion objects and provenance are returned rather than only converted values.
    :type return_conversions: Any
    :param complete_graph: Whether the bond graph should be completed with all triangulation-implied edges.
    :type complete_graph: Any
    :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
    :rtype: Any
    """
    ...

def _update_cache_based_on_dists(extra_dists, cache, inverse_triangulation):
    """
    **LLM Docstring**

    Add newly known distances to a conversion cache and update inverse triangulation lookups that depend on those pairs.

    :param extra_dists: Newly available pair distances.
    :type extra_dists: Any
    :param cache: Optional mutable cache of triangulation or conversion results.
    :type cache: Any
    :param inverse_triangulation: Lookup from pair distances to triangulation records that depend on them.
    :type inverse_triangulation: Any
    :return: The value or updated object described above.
    :rtype: Any
    """
    ...

class NonredundantInternalsChecker:

    def __init__(self, base_internals, natoms, dist_set=None):
        """
        **LLM Docstring**

        Initialize a mutable nonredundancy checker from base coordinates, atom count, and an optional precomputed distance set, including rigidity and conversion caches.

        :param base_internals: Coordinates already accepted by the nonredundancy checker.
        :type base_internals: Any
        :param natoms: Number of atoms in the system.
        :type natoms: Any
        :param dist_set: Optional known canonical distance set.
        :type dist_set: Any
        :return: None.
        :rtype: None
        """
        ...

    @property
    def dists(self):
        """
        **LLM Docstring**

        Return the current canonical distance set represented by the accepted coordinates.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

    def check_rigidty(self, dists):
        """
        **LLM Docstring**

        Test whether a proposed distance graph is minimally rigid for the checker’s atom count using the configured rigidity criterion.

        :param dists: Candidate or current pair-distance set.
        :type dists: Any
        :return: Whether the tested condition is satisfied.
        :rtype: bool
        """
        ...

    @classmethod
    def from_initial_internals(cls, internals):
        """
        **LLM Docstring**

        Construct a checker from an existing coordinate list after deriving its atoms, distance set, and initial rigidity/conversion state.

        :param internals: Available internal-coordinate specifications or their numerical values.
        :type internals: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

    @classmethod
    def check_trilateratable_distance(self, i, j, dists):
        """
        **LLM Docstring**

        Determine whether a new distance can be inferred by trilateration from already known distances to sufficiently many common reference atoms.

        :param i: An atom or flattened-coordinate index, depending on the helper.
        :type i: Any
        :param j: Second local vertex or coordinate index.
        :type j: Any
        :param dists: Candidate or current pair-distance set.
        :type dists: Any
        :return: Whether the tested condition is satisfied.
        :rtype: bool
        """
        ...

    def check_distances_convertable(self, new_coords, dists, graph, allow_recursive_completions=False, filter_by_new=True):
        """
        **LLM Docstring**

        Determine whether all pair distances introduced by candidate coordinates are already known or reconstructable from the current graph and triangulation cache.

        :param new_coords: Candidate coordinates whose distances are tested for convertibility.
        :type new_coords: Any
        :param dists: Candidate or current pair-distance set.
        :type dists: Any
        :param graph: Connectivity graph used to test distance inference.
        :type graph: Any
        :param allow_recursive_completions: Whether completing one coordinate may recursively request additional intermediate completions.
        :type allow_recursive_completions: Any
        :param filter_by_new: Whether conversion-cache updates are restricted to records affected by newly added coordinates.
        :type filter_by_new: Any
        :return: Whether the tested condition is satisfied.
        :rtype: bool
        """
        ...

    def add_internal(self, c, keep_bonds=True, keep_angles=True):
        """
        **LLM Docstring**

        Attempt to add one coordinate without introducing redundant constraints. It updates known distances and rigidity state only when the coordinate contributes an independent bond, angle, or dihedral relation, with options to preserve prerequisite bonds and angles.

        :param c: Third atom in the local triangle or tetrahedron.
        :type c: Any
        :param keep_bonds: Whether prerequisite bond distances should be retained when accepting a higher-order coordinate.
        :type keep_bonds: Any
        :param keep_angles: Whether prerequisite angles should be retained when accepting a dihedral.
        :type keep_angles: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

class InternalCoordinateGraph:
    """
    A graph mapping out the connections between a set of atoms based on the given set of internals
    """
    __slots__ = ['internals', 'atoms', 'triangulation', '_completion_cache', '_conversions', '_unreachable', '_expanded_internals', '_tri_cache']

    def __init__(self, internals, atoms=None, triangles_and_dihedrons=None):
        """
        **LLM Docstring**

        Initialize a mutable graph of internal coordinates, derive its triangulation and bond graph, and create caches for target conversions, expanded coordinates, and completed intermediates.

        :param internals: Available internal-coordinate specifications or their numerical values.
        :type internals: Any
        :param atoms: Atoms to include or place.
        :type atoms: Any
        :param triangles_and_dihedrons: Precomputed triangle and dihedron records used instead of rebuilding the triangulation.
        :type triangles_and_dihedrons: Any
        :return: None.
        :rtype: None
        """
        ...

    def get_target_triangulation(self, internals, target):
        """
        **LLM Docstring**

        Return the subset of the current triangulation needed to support a target coordinate.

        :param internals: Available internal-coordinate specifications or their numerical values.
        :type internals: Any
        :param target: Target coordinate whose supporting records are requested.
        :type target: Any
        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        ...

    def enumerate_matching_dihedrons(self, target_coord):
        """
        **LLM Docstring**

        Yield dihedron records and permutations that contain the target coordinate’s atoms in a usable arrangement.

        :param target_coord: Coordinate for which matching dihedrons are sought.
        :type target_coord: Any
        :return: An iterator yielding the candidates described above.
        :rtype: Iterator
        """
        ...

    def _get_expanded_internals(self, update_triangulation=True):
        """
        **LLM Docstring**

        Return the current coordinates plus intermediate coordinates completed by triangulation, optionally refreshing the triangulation first.

        :param update_triangulation: Whether to refresh triangulation data before using expanded coordinates or conversions.
        :type update_triangulation: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

    def _update_conversions(self, new, update_triangulation=True):
        """
        **LLM Docstring**

        Update cached target conversions after coordinates change, invalidating conversions that depend on removed data and resolving conversions enabled by newly added data.

        :param new: Coordinates newly added to the graph.
        :type new: Any
        :param update_triangulation: Whether to refresh triangulation data before using expanded coordinates or conversions.
        :type update_triangulation: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

    def find_conversions(self, target_internals, unconvertable_atoms=None, allow_recursive_completions=False, allow_ambiguous_completions=False, find_unreachable=True, verbose=False, create_single=False, missing_val=None, depth=0, max_depth=5, **etc):
        """
        **LLM Docstring**

        Find or construct conversions from the graph’s current coordinates to one or more target coordinates, reusing cached direct, triangle, dihedron, paired-dihedron, and completion conversions where possible.

        :param target_internals: Coordinates for which conversions are requested from the mutable graph.
        :type target_internals: Any
        :param unconvertable_atoms: Atoms that may not participate in inferred or completed conversion paths.
        :type unconvertable_atoms: Any
        :param allow_recursive_completions: Whether completing one coordinate may recursively request additional intermediate completions.
        :type allow_recursive_completions: Any
        :param allow_ambiguous_completions: Whether a missing intermediate may be accepted when more than one completion path exists.
        :type allow_ambiguous_completions: Any
        :param find_unreachable: Whether the search also identifies targets that cannot be reached from current coordinates.
        :type find_unreachable: Any
        :param verbose: Whether diagnostic information is emitted during the search.
        :type verbose: Any
        :param create_single: Whether a single requested target is returned as one callable instead of a list.
        :type create_single: Any
        :param missing_val: Value to return for a missing coordinate, or `"raise"` to raise.
        :type missing_val: Any
        :param depth: Current recursive search depth.
        :type depth: Any
        :param max_depth: Maximum recursive completion depth before the target is declared unreachable.
        :type max_depth: Any
        :param etc: Additional conversion-search options forwarded to nested searches.
        :type etc: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

    def _make_conversion(self, conv):
        """
        **LLM Docstring**

        Wrap a conversion specification as a callable that first computes any required intermediate completions.

        :param conv: Conversion specification to wrap.
        :type conv: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

    def get_bond_graph(self, dist_set=None, return_conversions=True):
        """
            **LLM Docstring**

            Return the bond graph implied by the graph’s current coordinates and triangulation, optionally rebuilding it or including metadata.

            :param dist_set: Optional known canonical distance set.
            :type dist_set: Any
            :param return_conversions: Whether conversion objects and provenance are returned rather than only converted values.
            :type return_conversions: Any
            :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
            :rtype: Any
            """
        ...

    class GraphCheckpoint:

        def __init__(self, g, reset=True):
            """
            **LLM Docstring**

            Capture the graph object and whether its mutable coordinate, triangulation, and conversion state should be restored when leaving the checkpoint.

            :param g: Graph whose state is checkpointed.
            :type g: Any
            :param reset: Whether graph state is restored on context exit.
            :type reset: Any
            :return: None.
            :rtype: None
            """
            ...

        def __enter__(self):
            """
            **LLM Docstring**

            Snapshot the graph’s mutable state and return the graph for temporary edits inside a context manager.

            :return: The checkpointed internal-coordinate graph.
            :rtype: InternalCoordinateGraph
            """
            ...

        def __exit__(self, exc_type, exc_val, exc_tb):
            """
            **LLM Docstring**

            Restore the saved graph state when reset is enabled, regardless of whether the context exits normally or through an exception.

            :param exc_type: Exception type raised in the checkpointed block, if any.
            :type exc_type: Any
            :param exc_val: Exception value raised in the checkpointed block, if any.
            :type exc_val: Any
            :param exc_tb: Exception traceback raised in the checkpointed block, if any.
            :type exc_tb: Any
            :return: `None`; exceptions are not suppressed.
            :rtype: None
            """
            ...

    def checkpoint(self):
        """
        **LLM Docstring**

        Return a context manager for making temporary changes to the internal-coordinate graph.

        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

    def add_internals(self, internals):
        """
        **LLM Docstring**

        Add coordinates to the graph, update triangulation and bond data, and refresh conversion caches for targets that become directly or indirectly available.

        :param internals: Available internal-coordinate specifications or their numerical values.
        :type internals: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        ...

    def remove_internals(self, internals):
        """
        **LLM Docstring**

        A non-implemented stub for future development.

        Remove coordinates from the graph, rebuild affected triangulation data, and invalidate cached conversions that depended on the removed coordinates.

        :param internals: Available internal-coordinate specifications or their numerical values.
        :type internals: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        ...
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

__all__ = [
    "canonicalize_internal",
    "get_canonical_internal_list",
    "is_coordinate_list_like",
    "is_valid_coordinate",
    "permute_internals",
    "find_internal",
    "coordinate_sign",
    "coordinate_indices",
    "get_internal_distance_conversion",
    "internal_distance_convert",
    "get_internal_triangles_and_dihedrons",
    "find_internal_conversion",
    "get_internal_cartesian_conversion",
    "validate_internals",
    # "RADInternalCoordinateSet"
    'InternalCoordinateType',
    'InternalSpec',
    "InternalCoordinateGraph"
]

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
        if typename is None and isinstance(type, str):
            typename = type
            def register(type, typename=typename):
                """
                **LLM Docstring**

                Assign the captured coordinate-type name to the decorated class and register that class with `InternalCoordinateType`.

                :param type: A coordinate class, or a registration name when using decorator form.
                :type type: Any
                :param typename: The registry key to assign to the coordinate class.
                :type typename: Any
                :return: The registered coordinate class.
                :rtype: type
                """
                type.name = typename
                return cls.register(type, typename)
            return register
        else:
            if typename is None:
                typename = type.name
            cls._dispatch = dev.uninitialized
            cls.registry[typename] = type
            return type

    _dispatch = dev.uninitialized
    @classmethod
    def get_dispatch(cls) -> dev.OptionsMethodDispatch:
        """
        **LLM Docstring**

        Return the lazily constructed options dispatcher used to turn dictionaries containing a `type` key into registered coordinate classes and their constructor options.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: dev.OptionsMethodDispatch
        """
        cls._dispatch = dev.handle_uninitialized(
            cls._dispatch,
            dev.OptionsMethodDispatch,
            args=(cls.registry,),
            kwargs=dict(
                method_key='type',
                attributes_map=cls.registry,
                allow_custom_methods=False
            )
        )
        return cls._dispatch

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
        if isinstance(input, dict):
            type, opts = cls.get_dispatch().resolve(input)
            inds = opts.pop(type.name, None)
            if inds is not None:
                opts['indices'] = inds
        else:
            for v in cls.registry.values():
                if v.could_be(input):
                    opts = {'indices':input}
                    type = v
                    break
            else:
                raise ValueError(f"couldn't match input {input} to internal coordinate types {cls.registry}")
        return type(**opts)

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
        return False

    def equivalent_to(self, other):
        """
        **LLM Docstring**

        Test whether two coordinates have the same concrete type and the same indices after each is put in canonical orientation.

        :param other: The coordinate to compare against.
        :type other: Any
        :return: Whether the tested condition is satisfied.
        :rtype: bool
        """
        return (
                type(self) is type(other)
                and self.canonicalize().get_indices() == other.canonicalize().get_indices()
        )
    def __eq__(self, other):
        """
        **LLM Docstring**

        Compare coordinates using canonical coordinate equivalence rather than object identity.

        :param other: The coordinate to compare against.
        :type other: Any
        :return: Whether the tested condition is satisfied.
        :rtype: bool
        """
        return self.equivalent_to(other)

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
        return hash((type(self), self.get_indices()))
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
    def get_carried_atoms(self, context:InternalSpec):
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
    def get_constraint_rads(self) -> list[Distance|Angle|Dihedral]:
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
        if moved_indices is not None:
            left_ats, right_ats = moved_indices
        else:
            if context is not None and (left_atoms is None or right_atoms is None):
                left_ats, right_ats = self.get_carried_atoms(context)
            else:
                left_ats = right_ats = None
        if left_atoms is None:
            left_atoms = left_ats
        if right_atoms is None:
            right_atoms = right_ats
        return left_atoms, right_atoms

class BasicInternalType(InternalCoordinateType):
    forward_conversion: Callable[[np.ndarray, ParamSpec("P")], List[np.ndarray]]
    inverse_conversion: Callable[[np.ndarray, ParamSpec("P")], List[np.ndarray]]
    def __init__(self, indices: Sequence[int]):
        """
        **LLM Docstring**

        Store the defining atom indices as an immutable tuple and bind the class-level forward and inverse conversion functions onto the instance.

        :param indices: Atom indices defining the coordinate, or a restricted search index set.
        :type indices: Sequence[int]
        :return: None.
        :rtype: None
        """
        self.inds = tuple(indices)
        # a hack to make these classes easier to work with
        self.forward_conversion = type(self).forward_conversion
        self.inverse_conversion = type(self).inverse_conversion
    def __repr__(self):
        """
        **LLM Docstring**

        Format the coordinate as its class name followed by its defining index tuple.

        :return: A concise representation of the object.
        :rtype: str
        """
        cls = type(self)
        return f"{cls.__name__}{self.inds}"
    def reindex(self, reindexing):
        """
        **LLM Docstring**

        Apply an index lookup to every defining atom and construct a coordinate of the same type with the mapped indices.

        :param reindexing: A mapping from existing atom indices to replacement indices.
        :type reindexing: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        return type(self)([reindexing[i] for i in self.inds])
    def canonicalize(self):
        """
        **LLM Docstring**

        Orient a reversible coordinate so that its final atom index is not smaller than its first; reverse the full index tuple when necessary.

        :return: The value or updated object described above.
        :rtype: Any
        """
        if self.inds[-1] < self.inds[0]:
            return type(self)(tuple(self.inds[::-1]))
        else:
            return self
    def get_indices(self):
        """
        **LLM Docstring**

        Return the stored tuple of defining atom indices.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        return self.inds
    def get_dropped_internals(self):
        """
        **LLM Docstring**

        Return the set of coordinates removed from the bond graph when determining which atoms move with this coordinate; the default removes only the coordinate itself.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        return [self]
    def get_carried_atoms(self, context:InternalSpec, max_branching=5):
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
        subgraph:EdgeGraph = context.get_dropped_internal_bond_graph(self.get_dropped_internals())
        left_atoms = None
        right_atoms = None
        atom_mapping = {a:i for i,a in enumerate(context.atoms)}
        inv_mapping = {i:a for a,i in atom_mapping.items()}
        prev_left = None
        m = 0
        start = atom_mapping[self.inds[0]]
        end = atom_mapping[self.inds[-1]]
        while left_atoms is right_atoms:
            groups = subgraph.get_fragments()
            for g in groups:
                if start in g:
                    left_atoms = g
                    break
            for g in groups:
                if end in g:
                    right_atoms = g
                    break
            if left_atoms is right_atoms:
                subpath = subgraph.get_path(start, end)
                if subpath is None:
                    raise ValueError(
                        f"no path between {start} and {end}, but frags are {groups}"
                    )
                n = len(subpath) // 2
                subgraph = subgraph.break_bonds([(subpath[n], subpath[n-1])], return_single_graph=True)
            if (
                    prev_left is not None
                    and left_atoms is not None
                    and len(left_atoms) == len(prev_left)
                    and np.allclose(left_atoms, prev_left)
            ):
                m += 1
            else:
                m = 0
            if m > max_branching:
                raise ValueError(f"can't resolve carried atoms on {left_atoms} between {self.inds[0], self.inds[-1]}...")
            prev_left = left_atoms
        left_atoms = [inv_mapping[i] for i in left_atoms]
        right_atoms = [inv_mapping[i] for i in right_atoms]
        return left_atoms, right_atoms
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
        return self.forward_conversion(coords, *self.inds, order=order, **opts)
    def get_inverse_expansion(self, coords, *, order=None, moved_indices=None,
                              context=None,
                              left_atoms=None, right_atoms=None, masses=None, **opts):
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
        left_atoms, right_atoms = self._prep_left_right_atoms(context, moved_indices, left_atoms, right_atoms)
        return self.inverse_conversion(coords, *self.inds,
                                   order=order, left_atoms=left_atoms, right_atoms=right_atoms,
                                   **opts)


@InternalCoordinateType.register("dist")
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
        return (
            dev.is_list_like(input)
            and len(input) == 2
            and nput.is_int(input[0])
            and nput.is_int(input[1])
        )
    def get_constraint_rads(self):
        """
        **LLM Docstring**

        Return the distance itself as the sole primitive coordinate required to constrain it.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        return [self]

@InternalCoordinateType.register("bend")
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
        return (
            dev.is_list_like(input)
            and len(input) == 3
            and nput.is_int(input[0])
            and nput.is_int(input[1])
        )
    def get_constraint_rads(self):
        """
        **LLM Docstring**

        Return the angle itself as the primitive coordinate required to constrain it.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        return [self]
    def get_dropped_internals(self):
        """
        **LLM Docstring**

        Remove the angle and its two adjacent bond distances when finding the atom groups carried by an angle displacement.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        i,j,k = self.get_indices()
        return [self, Distance((i, j)), Distance((j, k))]

@InternalCoordinateType.register("dihedral")
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
        return (
            dev.is_list_like(input)
            and len(input) == 4
            and nput.is_int(input[0])
            and nput.is_int(input[1])
        )
    def get_constraint_rads(self):
        """
        **LLM Docstring**

        Return the dihedral itself as the primitive coordinate required to constrain it.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        return [self]
    def get_dropped_internals(self):
        """
        **LLM Docstring**

        Remove the dihedral, its central angle pair, and the three chain bond distances when separating the two sides of a torsional displacement.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        i,j,k,l = self.get_indices()
        return [self, Distance((i, j)), Distance((j, k)), Distance((k, l))]

@InternalCoordinateType.register("wag")
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
        return [Dihedral()]

@InternalCoordinateType.register("oop")
class OutOfPlane(BasicInternalType):
    forward_conversion = nput.oop_vec
    inverse_conversion = nput.oop_expansion

@InternalCoordinateType.register("transrot")
class TranslatonRotation(BasicInternalType):
    forward_conversion = nput.transrot_vecs
    inverse_conversion = nput.transrot_expansion
    def __init__(self,  indices: Sequence[int], masses=None):
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
        super().__init__(indices)
        self.masses = masses
    def canonicalize(self):
        """
        **LLM Docstring**

        Return the rigid-body coordinate unchanged because its atom set has no reversible endpoint orientation.

        :return: The value or updated object described above.
        :rtype: Any
        """
        return type(self)(np.sort(self.inds))
    def get_carried_atoms(self, context:InternalSpec):
        """
        **LLM Docstring**

        Treat all atoms in the rigid-body coordinate as the moved group and return no opposing group.

        :param context: The surrounding coordinate specification used to infer connectivity and moved fragments.
        :type context: InternalSpec
        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        moved_indices = None
        groups = context.get_bond_graph().get_fragments()
        for g in groups:
            if len(np.intersect1d(g, self.inds)) > 0:
                moved_indices = g
                break
        return moved_indices
    def get_inverse_expansion(self, coords, *, order=None,
                              context=None, moved_indices=None, extra_atoms=None,
                              masses=None,
                              **opts):
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
        if extra_atoms is None:
            if moved_indices is None and context is not None:
                moved_indices = self.get_carried_atoms(context)
            if moved_indices is not None:
                extra_atoms = np.setdiff1d(moved_indices, self.inds)
        if masses is None:
            masses = self.masses
        return self.inverse_conversion(coords, *self.inds,
                                       order=order,
                                       extra_atoms=extra_atoms,
                                       masses=masses,
                                       **opts)

@InternalCoordinateType.register("orientation")
class Orientation(BasicInternalType):
    forward_conversion = nput.orientation_vecs
    inverse_conversion = nput.orientation_expansion
    def __init__(self,  indices: Sequence[int], masses=None):
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
        super().__init__(indices)
        self.masses = masses
    def canonicalize(self):
        """
        **LLM Docstring**

        Return the orientation unchanged because reversing its atom order changes the directed orientation.

        :return: The value or updated object described above.
        :rtype: Any
        """
        return type(self)((np.sort(self.inds[0]), np.sort(self.inds[1])))
    def get_indices(self):
        """
        **LLM Docstring**

        Return the stored atom indices defining the orientation.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        return tuple(self.inds[0]) + tuple(self.inds[1])
    def reindex(self, reindexing):
        """
        **LLM Docstring**

        Map the orientation’s atoms through a supplied reindexing and preserve its mass data.

        :param reindexing: A mapping from existing atom indices to replacement indices.
        :type reindexing: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        return type(self)([
            [reindexing[i] for i in self.inds[0]],
            [reindexing[i] for i in self.inds[1]]
        ])
    def get_carried_atoms(self, context:InternalSpec):
        """
        **LLM Docstring**

        Return the orientation atoms as the moved group and no atoms on the opposite side.

        :param context: The surrounding coordinate specification used to infer connectivity and moved fragments.
        :type context: InternalSpec
        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        moved_indices_left = None
        moved_indices_right = None
        groups = context.get_bond_graph().get_fragments()
        for g in groups:
            if len(np.intersect1d(g, self.inds[0])) > 0:
                moved_indices_left = g
                break
        for g in groups:
            if len(np.intersect1d(g, self.inds[1])) > 0:
                moved_indices_right = g
                break
        return moved_indices_left, moved_indices_right
    def get_inverse_expansion(self, coords, *, order=None, moved_indices=None, context=None,
                              left_extra_atoms=None, right_extra_atoms=None, masses=None, **opts):
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
        left_extra_atoms, right_extra_atoms = self._prep_left_right_atoms(context, moved_indices, left_extra_atoms, right_extra_atoms)
        if left_extra_atoms is not None:
            left_extra_atoms = np.setdiff1d(left_extra_atoms, self.inds[0])
        if right_extra_atoms is not None:
            right_extra_atoms = np.setdiff1d(right_extra_atoms, self.inds[1])
        if masses is None:
            masses = self.masses
        return self.inverse_conversion(coords, *self.inds,
                                       order=order,
                                       left_extra_atoms=left_extra_atoms, right_extra_atoms=right_extra_atoms,
                                       masses=masses,
                                       **opts)

class InternalSpec:
    def __init__(self, coords, canonicalize=True, bond_graph=None, triangulation=None, masses=None,
                 ungraphed_internals=None,
                 distance_conversions=None
                 ):
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
        self.coords:tuple[InternalCoordinateType] = tuple(
            InternalCoordinateType.resolve(c)
                if not isinstance(c, InternalCoordinateType) else
            c
            for c in coords
        )

        if ungraphed_internals is not None:
            ungraphed_internals = tuple(
                InternalCoordinateType.resolve(c)
                    if not isinstance(c, InternalCoordinateType) else
                c
                for c in ungraphed_internals
            )
        self.ungraphed_internals = ungraphed_internals

        if canonicalize:
            self.coords = tuple(c.canonicalize() for c in self.coords)
            if self.ungraphed_internals is not None:
                self.ungraphed_internals = tuple(c.canonicalize() for c in self.ungraphed_internals)

        self.rad_set = [
            c.inds for c in self.coords
            if isinstance(c, (Distance, Angle, Dihedral))
            if (
                    self.ungraphed_internals is None
                    or c not in self.ungraphed_internals
            )
        ]
        self.masses = masses
        self._atom_lists = None
        self._atoms = None
        self._bond_graph = bond_graph
        self._dist_convs = distance_conversions
        self._tri_di = triangulation
        self._rad_conv = None
        self._zm_conv = None
        self._dm_conv = None
        self._pruned_rads = None
        self._pruned_tri_di = None
        self._carried_atoms = [None] * len(coords)
        self._graph = None

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
        from .ZMatrices import extract_zmatrix_internals
        vars = [
            extract_zmatrix_internals(z)
            for z in zmats
        ]
        return cls(
            (sum(vars, []) + ([] if additions is None else list(additions))),
            **opts
        )

    @property
    def atom_sets(self) -> Tuple[Tuple[int]]:
        """
        **LLM Docstring**

        Return the defining atom tuple for every coordinate in the specification.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Tuple[Tuple[int]]
        """
        if self._atom_lists is None:
            self._atom_lists = tuple(a.get_indices() for a in self.coords)
        return self._atom_lists
    @property
    def atoms(self) -> Tuple[int]:
        """
        **LLM Docstring**

        Return the sorted unique atom indices appearing in any coordinate.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Tuple[int]
        """
        if self._atoms is None:
            self._atoms = tuple(itut.delete_duplicates(c for a in self.atom_sets for c in a))
        return self._atoms

    def get_triangulation(self):
        """
        **LLM Docstring**

        Lazily derive and cache the triangle and dihedron sets that express the specification as connected distance geometry.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        if self._tri_di is None:
            # print(self.rad_set)
            self._tri_di = get_internal_triangles_and_dihedrons(self.rad_set)
        return self._tri_di
    def get_pruned_rads(self):
        """
        **LLM Docstring**

        Return the subset of primitive coordinates retained after removing redundancies implied by the triangulation.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        if self._pruned_rads is None:
            self._pruned_rads = self.non_redundant_rads()
        return self._pruned_rads
    def get_pruned_triangulation(self):
        """
        **LLM Docstring**

        Return a triangulation rebuilt from the nonredundant primitive coordinates.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        if self._pruned_tri_di is None:
            # print(self.rad_set)
            self._pruned_tri_di = get_internal_triangles_and_dihedrons(self.get_pruned_rads()[0])
        return self._pruned_tri_di
    def get_bond_graph(self) -> EdgeGraph:
        """
        **LLM Docstring**

        Lazily construct an `EdgeGraph` whose edges are the bond distances represented by the coordinate set.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: EdgeGraph
        """
        if self._bond_graph is None:
            self._bond_graph = get_internal_bond_graph(self.rad_set, self.atoms,
                                                                         triangles_and_dihedrons=self.get_triangulation(),
                                                                         return_conversions=False)
        return self._bond_graph
    @property
    def graph(self):
        """
        **LLM Docstring**

        Expose the cached or newly constructed bond graph for the specification.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        if self._graph is None:
            self._graph = InternalCoordinateGraph(self.rad_set, atoms=self.atoms)
        return self._graph
    def get_distance_conversions(self):
        """
        **LLM Docstring**

        Build and cache the conversion specification and callable that reconstruct all triangulation distances from the stored internal coordinates.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        if self._dist_convs is None:
            self._dist_convs = self.graph.get_bond_graph()
            # self._dist_convs = get_internal_bond_graph(self.rad_set, self.atoms,
            #                                            triangles_and_dihedrons=self.get_triangulation(),
            #                                            return_conversions=True,
            #                                            complete_graph=True)
        return self._dist_convs
    # def get_rad_conversion(self):
    #     if self._rad_conv is None:
    #         tri = self.get_triangulation()
    #         self._rad_conv = get_internal_distance_conversion(self.rad_set,
    #                                                           allow_completion=True,
    #                                                           missing_val=None,
    #                                                           triangles_and_dihedrons=tri,
    #                                                           return_conversions=True,
    #                                                           include_shapes=True)
    #
    #     return self._rad_conv
    def get_zmat_conv(self, raise_on_incomplete=True):
        """
        **LLM Docstring**

        Find and cache a conversion from this coordinate set to a Z-matrix ordering. Optionally raise when no complete Z-matrix can be constructed.

        :param raise_on_incomplete: Whether failure to build a complete conversion raises instead of returning an incomplete result.
        :type raise_on_incomplete: Any
        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        if self._zm_conv is None:
            # pruned_rads, indices = self.get_pruned_rads()
            # tri = self.get_pruned_triangulation()
            pruned_rads = self.rad_set
            indices = None
            tri = self.get_triangulation()

            for zm_conv in enumerate_zmatrices_from_internals(pruned_rads, tri,
                                                              atoms=self.atoms,
                                                              graph=self.graph,
                                                              indices=indices):
                self._zm_conv = zm_conv
                break
            else:
                if raise_on_incomplete:
                    raise ValueError("couldn't construct Z-matrix transformation")
                else:
                    self._zm_conv = (None, None)
        return self._zm_conv
    def get_dmat_conv(self):
        """
        **LLM Docstring**

        Build and cache a converter from internal-coordinate values to the condensed or square distance-matrix representation required by the triangulation.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        if self._dm_conv is None:
            bg, dist_stuff = self.get_distance_conversions()
            funs = dict(zip(*dist_stuff))
            groups = bg.get_fragments(return_labels=True)
            convs = []
            for g in groups:
                blocks = []
                for i,j in itertools.combinations(g, 2):
                    blocks.append(funs[(i,j)])
                edges = []
                for i,j in itertools.combinations(g, 2):
                    if funs[(i,j)] is not None:
                        edges.append((i,j))
                g_map = dict(zip(g, range(len(g))))
                e_test = [(g_map[i], g_map[j]) for i, j in edges]
                is_ridig, (comp, rank), _ = uniquely_rigid(e_test, 3, natoms=len(g), return_components=True)
                if not is_ridig:
                    return None, None
                else:
                    def prep(internals, blocks=blocks):
                        """
                        **LLM Docstring**

                        Reorder and broadcast converted distance values into the distance-matrix index layout expected by the cached distance conversion.

                        :param internals: Available internal-coordinate specifications or their numerical values.
                        :type internals: Any
                        :param blocks: Index blocks identifying grouped Cartesian degrees of freedom.
                        :type blocks: Any
                        :return: The value or updated object described above.
                        :rtype: Any
                        """
                        return np.moveaxis([
                            f(internals) for f in blocks
                        ], 0, -1)
                    convs.append(prep)
            self._dm_conv = groups, convs
        return self._dm_conv

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
        if method is None:
            method = self.graph_split_method
        bg = self.get_bond_graph()
        cur_bonds = [
            (bg.labels[i], bg.labels[j])
            for i,j in bg.edges
        ]
        mapping = {a: i for i, a in enumerate(bg.labels)}
        if method == 'dists':
            internals = [
                i for i in internals
                if isinstance(i, Distance)
            ]
            definite_edges = {
                i.get_indices()
                for i in self.coords
                if isinstance(i, Distance) and i not in internals
            }
            dropped_atoms = {
                i
                for d in internals
                for i in d.get_indices()
            }
            dropped_bonds = [
                (i,j)
                for (i,j) in cur_bonds
                if (i,j) not in definite_edges and (j,i) not in definite_edges
                    and (i in dropped_atoms or j in dropped_atoms)
            ]

            wtf = bg.break_bonds(
                [
                    (mapping[i], mapping[j])
                    for i,j in dropped_bonds
                ],
                return_single_graph=True
            )
            return wtf
        else:
            core_atoms, sub_triangulation, _ = update_triangulation(
                self.get_triangulation(),
                [],
                [
                    i.get_indices() for i in internals
                    if isinstance(i, (Distance, Angle, Dihedral))
                ],
                triangulation_internals=[
                    canonicalize_internal(i)
                    for i in self.rad_set
                ],
                return_split=True
            )

            target_bonds = [b for b in cur_bonds if all(i in core_atoms for i in b)]
            kept_bonds = [b for b in cur_bonds if any(i not in core_atoms for i in b)]

            if len(target_bonds) == 0:
                return bg

            _, (funs, shapes) = get_internal_distance_conversion(internals,
                                                                 allow_completion=False,
                                                                 missing_val=None,
                                                                 triangles_and_dihedrons=sub_triangulation,
                                                                 return_conversions=True,
                                                                 include_shapes=True,
                                                                 dist_set=target_bonds)
            target_bonds = [d for d, f in zip(target_bonds, funs) if f is not None]
            # target_shapes = [d for d, f in zip(shapes, funs) if f is not None]
            target_bonds = [(mapping[i], mapping[j]) for i, j in target_bonds]
            kept_bonds = [(mapping[i], mapping[j]) for i, j in kept_bonds]

            return EdgeGraph(
                bg.labels,
                target_bonds + kept_bonds
            )


    def get_direct_derivatives(self, coords, order=1,
                               cache=True,
                               reproject=False, # used to accelerate base derivs
                               base_transformation=None,
                               reference_internals=None,
                               combine_expansions=True,
                               terms=None,
                               **opts):
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
        coords = np.asanyarray(coords)
        if cache is False:
            cache = None
        elif cache is True:
            cache = {}
        subexpansions = [
            c.get_expansion(coords, order=order, cache=cache, reproject=reproject, **opts)
            for i, c in enumerate(self.coords)
            if (terms is None or i in terms)
        ]

        if combine_expansions:
            base_dim = coords.ndim - 2
            return nput.combine_coordinate_deriv_expansions(
                subexpansions,
                order=order,
                base_dim=base_dim,
                base_transformation=base_transformation,
                reference_internals=reference_internals
            )
        else:
            return subexpansions

    def orthogonalize_transformations(cls,
                                      expansion, inverse,
                                      coords=None,
                                      masses=None,
                                      order=None,
                                      remove_translation_rotations=False):
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
        if coords is not None:
            coords = np.asanyarray(coords)
            base_dim = coords.ndim - 2
        else:
            base_dim = max([expansion[0].ndim - 1, inverse[0].ndim - 2])
        expansion = [
            [
                np.expand_dims(t, -1)
                    if t.ndim - i == base_dim else
                t
                for i, t in enumerate(subt)
            ]
            for subt in expansion
        ]
        vals = [e[0] for e in expansion]
        expansion = [e[1:] for e in expansion]

        inverses = [i[1:] for i in inverse]
        inverses = [
            [
                np.expand_dims(t, list(range(base_dim, base_dim + i + 1)))
                if t.ndim - 1 == base_dim else
                t
                for i, t in enumerate(subt)
            ]
            for subt in inverses
        ]

        if remove_translation_rotations:
            transrot_deriv = nput.transrot_deriv(
                coords,
                masses=masses,
                order=order
            )
            transrot_inv = nput.transrot_expansion(
                coords,
                masses=masses,
                order=1
            )
            expansion = [transrot_deriv[1:]] + expansion
            inverses = [transrot_inv[1:]] + inverses
            inverses, expansion = nput.orthogonalize_transformations(zip(inverses, expansion), concatenate=False)
            expansion = nput.concatenate_expansions(expansion, concatenate_values=True)
            inverses = nput.concatenate_expansions(inverses, concatenate_values=False)
            full_inverses = nput.inverse_transformation(expansion, order,
                                                        reverse_expansion=inverses[:1],
                                                        allow_pseudoinverse=True
                                                        )
            expansion = [e[..., 6:] for e in expansion]
            _ = []
            for i, e in enumerate(full_inverses):
                sel = (...,) + (slice(6, None),) * (i + 1) + (slice(None),)
                _.append(e[sel])
            full_inverses = _

        else:
            inverses, expansion = nput.orthogonalize_transformations(zip(inverses, expansion))
            full_inverses = nput.inverse_transformation(expansion, order,
                                                        reverse_expansion=inverses[:1],
                                                        allow_pseudoinverse=True
                                                        )
        expansion = [np.concatenate(vals, axis=-1)] + expansion
        return expansion, full_inverses

    def get_expansion(self, coords, order=1,
                      return_inverse=False,
                      remove_translation_rotations=True,
                      orthogonalize=True,
                      # mass_weighted=True,
                      **opts) -> List[np.ndarray]:
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
        coords = np.asanyarray(coords)
        # base_dim = coords.ndim - 2
        expansion = self.get_direct_derivatives(coords, order=order,
                                                combine_expansions=(
                                                    not return_inverse
                                                    or not orthogonalize
                                                ),
                                                **opts)
        if return_inverse:
            if order == 0:
                raise ValueError("order > 0 required for inverses")
            if dev.is_list_like(return_inverse):
                terms = return_inverse
            else:
                terms = None
            # if mass_weighted and self.masses is not None:
            #     g_matrix = np.diag(np.sqrt(self.masses))
            #     coords = np.moveaxis(
            #         np.tensordot(coords, g_matrix, axes=[-2, 0]),
            #         -1, -2
            #     )
            base_inverses = self.get_direct_inverses(coords,
                                                     order=1,
                                                     combine_expansions=not orthogonalize,
                                                     terms=terms,
                                                     **opts)
            # if mass_weighted and self.masses is not None:
            #     g_matrix = np.diag(np.repeat(1/np.sqrt(self.masses), 3))
            #     #TODO: if we ever return base_inverses[0] we need to remove mass weighting
            #     base_inverses = [base_inverses[0]] + [
            #         np.tensordot(b, g_matrix, axes=[-1, 0])
            #         for b in base_inverses[1:]
            #     ]
            if orthogonalize:
                return self.orthogonalize_transformations(
                    expansion, base_inverses,
                    coords=coords,
                    masses=self.masses,
                    remove_translation_rotations=remove_translation_rotations,
                    order=order
                )
            else:
                return expansion, base_inverses[1:]

        return expansion
    def __repr__(self):
        """
        **LLM Docstring**

        Format the specification as the class name containing its normalized coordinate list.

        :return: A concise representation of the object.
        :rtype: str
        """
        cls = type(self)
        return f"{cls.__name__}({self.coords})"

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
        coords = np.asanyarray(coords)

        expansions = []
        for i, c in enumerate(self.coords):
            if (terms is None or i in terms):
                if self._carried_atoms[i] is None:
                    self._carried_atoms[i] = c.get_carried_atoms(self)
                exp = c.get_inverse_expansion(coords, order=order, moved_indices=self._carried_atoms[i], **opts)
                coords = exp[0]
                expansions.append(exp)
        if combine_expansions:
            expansions = nput.combine_coordinate_inverse_expansions(expansions, order=order)
        return expansions

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
        just_coords = order is None
        if just_coords: order = 0
        expansions = self.get_direct_derivatives(coords, order=order, **opts)
        if just_coords:
            return expansions[0]
        else:
            return expansions[0], expansions[1:]

    def internals_to_cartesians(self, coords, order=None,
                                reference_cartesians=None,
                                return_fragments=False,
                                return_inverse=True,
                                transformations=None,
                                reference_internals=None,
                                use_distance_matrix_fallback=False,
                                **deriv_opts):
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
        from .ZMatrices import zmatrix_from_values, canonicalize_zmatrix
        from .Conveniences import zmatrix_to_cartesian#, cartesian_to_zmatrix
        # if order is None:
        #     use_zmat = False
        #     conv = self.get_dmat_conv()
        # else:
        use_zmat = True
        conv = self.get_zmat_conv(raise_on_incomplete=False)
        if conv[0] is None:
            if use_distance_matrix_fallback:
                dm = self.get_dmat_conv()
                conv = dm
            use_zmat = False
        if conv[0] is None:
            raise ValueError(f"insufficient to build Z-matrix or distance matrix fragments: {self.coords}")

        if transformations is not None:
            base_shape = coords.shape[:-1]
            tfs = [
                nput.broadcast_constant(t, base_shape, pad_base=True)
                for t in transformations[1]
            ]
            coords = nput.tensor_reexpand(tfs, [coords], axes=[-1, -1])[0]
            if reference_internals is None:
                if reference_cartesians is not None:
                    reference_internals = self.cartesians_to_internals(reference_cartesians)
            if reference_internals is not None:
                reference_internals = np.asanyarray(reference_internals)
                reference_internals = nput.broadcast_constant(reference_internals, base_shape, pad_base=True)
                coords = coords + reference_internals
        unified = callable(conv[1])
        if unified:
            if use_zmat:
                (zmatrix, prep) = conv
                flat_z = prep(coords)
                zcoords = zmatrix_from_values(flat_z, partial_embedding=True)
                perm, zmatrix = canonicalize_zmatrix(zmatrix)
                blocks = [[zmatrix_to_cartesian(zcoords, zmatrix), perm]]
            else:
                (perm, prep) = conv
                dists = prep(coords)
                blocks = [[nput.points_from_distance_matrix(dists, use_triu=True), perm]]
        else:
            blocks = []
            if use_zmat:
                for zmatrix, prep in zip(*conv):
                    flat_z = prep(coords)
                    zcoords = zmatrix_from_values(flat_z, partial_embedding=True)
                    perm, zmatrix = canonicalize_zmatrix(zmatrix)
                    blocks.append([zmatrix_to_cartesian(zcoords, zmatrix), perm])
            else:
                for perm, prep in zip(*conv):
                    dists = prep(coords)
                    blocks.append([nput.points_from_distance_matrix(dists, use_triu=True), perm])

        if return_fragments:
            if order is not None: raise NotImplementedError("can't return derivatives of fragments alone")
            return blocks

        if reference_cartesians is None:
            all_atoms = np.concatenate([p for c,p in blocks])
            reference_cartesians = np.zeros((len(all_atoms), 3))

        carts = np.array(reference_cartesians)
        for i,(coord, perm) in enumerate(blocks):
            # have to shift and realign fragments if possible...
            if i == 0:
                base_shape = coord.shape[:-2]
                if carts.ndim == 2:
                    carts = nput.broadcast_constant(carts, base_shape, pad_base=True).copy()
            if len(perm) > 2:
                x, y, z = np.moveaxis(carts[..., perm[:3], :], -2, 0)
                u = y - x
                v = z - x
                norms = nput.vec_norms([u, v])
                mod_locs = np.all(norms > 1e-8, axis=0)
                coord = coord - coord[..., (0,), :]
                if np.any(mod_locs):
                    # set up a consistent coordinate frame by taking
                    # the embedding matrix of the first 3 new coords and putting
                    # it in the u,v frame
                    u, v = nput.vec_normalize([u[mod_locs, :], v[mod_locs, :]], norms=norms[:, mod_locs])
                    a = nput.vec_normalize(coord[mod_locs, 1, :] - coord[mod_locs, 0, :])
                    b = nput.vec_crosses(
                        a,
                        nput.vec_normalize(coord[mod_locs, 2, :] - coord[mod_locs, 0, :]),
                        normalize=True
                    )
                    r1 = nput.rotation_matrix(a, u)
                    z = np.reshape(b[..., np.newaxis, :] @ r1, u.shape)
                    normal = np.cross(u, v)
                    ang, cross = nput.vec_angles(normal, z, return_crosses=True)
                    frame = r1 @ nput.rotation_matrix(cross, ang)
                    coord[mod_locs] = coord[mod_locs] @ frame
                coord = coord + x[..., np.newaxis, :]
            elif len(perm) == 2:
                x, y = np.moveaxis(carts[..., perm[:2], :], -2, 0)
                u = y - x
                norms = nput.vec_norms(u)
                mod_locs = norms > 1e-8
                coords = coords - coords[..., (0,), :]
                if np.any(mod_locs):
                    u = nput.vec_normalize(u[mod_locs, :], norms=norms[mod_locs])
                    a = nput.vec_normalize(coords[mod_locs, 1, :] - coords[mod_locs, 0, :])
                    r1 = nput.rotation_matrix(a, u)
                    coords[mod_locs] = coords @ r1
                coord = coord + x[..., np.newaxis, :]
            else:
                x = np.moveaxis(carts[..., perm[:1], :], -2, 0)
                coords = coords - coords[..., (0,), :]
                coord = coord + x[..., np.newaxis, :]

            carts[..., perm, :] = coord

        if order is None:
            return carts
        else:
            if order == 0:
                return carts, []
            else:
                expansion = self.get_expansion(
                    carts,
                    order=order,
                    return_inverse=return_inverse,
                    **deriv_opts
                )
                return carts, expansion

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
        if len(rad) == 2:
            return rad
        elif len(rad) == 3:
            idx = nput.triangle_property_specifiers()
            for p in itertools.permutations(rad):
                if p in tris:
                    t = tris[p]
                    a, b, c = [
                        tuple(p[i] for i in idx[j]['coord'])
                        for j in ['a', 'b', 'c']
                    ]
                    if t.a is not None:
                        if t.b is not None:
                            return c
                        elif t.c is not None:
                            return b
                        else:
                            return c
                    elif t.b is not None:
                        if t.c is not None:
                            return a
                        else:
                            return c
                    else:
                        return a
            else:
                raise ValueError(f"failed to find a matching triangle to {rad}")
        else:
            idx = nput.dihedron_property_specifiers ()
            for p in itertools.permutations(rad):
                if p in diheds:
                    dd = diheds[p]
                    a, b, c, x, y, z = [
                        tuple(p[i] for i in idx[j]['coord'])
                        for j in ['a', 'b', 'c', 'x', 'y', 'z']
                    ]
                    tris = [
                        nput.dihedron_triangle(dd, i)
                        for i in range(4)
                    ]
                    completions = [ nput.triangle_is_complete(t) for t in tris ]

                    checks = [ # from dihedron_triangle_pair_dihedrals
                        (0, 1, (dd.z, z)),
                        (0, 2, (dd.c, c)),
                        (0, 3, (dd.y, y)),
                        (1, 2, (dd.x, x)),
                        (1, 3, (dd.a, a)),
                        (2, 3, (dd.b, b)),
                    ]
                    for i,j,(z,v) in checks:
                        if completions[i] and completions[j]:
                            if z is None:
                                return v
                            else:
                                raise NotImplementedError("ugh")
                    else:
                        for i,j,(z,v) in checks:
                            if completions[i] or completions[j]:
                                if z is None:
                                    return v
                                else:
                                    raise NotImplementedError("ugh")
            else:
                raise ValueError(f"failed to find a matching dihedral to {rad}")
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
        if triangulation is None:
            triangulation = self.get_triangulation()
        if rads is None:
            rads = self.rad_set
        tris, diheds = triangulation
        tris = {k: v for k, v in tris.items() if nput.triangle_is_complete(v)}
        diheds = {k: v for k, v in diheds.items() if nput.dihedron_is_complete(v)}
        return [
            self._novel_distance(r, tris, diheds)
            for r in rads
        ]
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
        if len(rad) == 2:
            return [rad]
        elif len(rad) == 3:
            for p in itertools.permutations(rad):
                if p in tris:
                    return list(itertools.combinations(rad, 2))
            else:
                raise ValueError(f"failed to find a matching triangle to {rad}")
        else:
            for p in itertools.permutations(rad):
                if p in diheds:
                    return list(itertools.combinations(rad, 2))
            else:
                raise ValueError(f"failed to find a matching dihedron to {rad}")
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
        if triangulation is None:
            triangulation = self.get_triangulation()
        if rads is None:
            rads = self.rad_set
        tris, diheds = triangulation
        tris = {k: v for k, v in tris.items() if nput.triangle_is_complete(v)}
        diheds = {k: v for k, v in diheds.items() if nput.dihedron_is_complete(v)}
        return [
            self._tri_dists(r, tris, diheds)
            for r in rads
        ]
    def check_redundancy(self):
        """
        **LLM Docstring**

        Check whether the coordinate set contains more independent constraints than its atom count permits, using the triangulation rigidity test.

        :return: The value or updated object described above.
        :rtype: Any
        """
        return pebble_rigidity(
            # self.get_triangulation_distances(),
            self.get_triangulation_novel_internals(),
            3
        )

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
    sign = 1
    if not check_invalid:
        if coord[-1] < coord[0]:
            coord = tuple(reversed(coord))
            sign = -1
        else:
            coord = tuple(coord)
    else:
        if len(coord) == 2:
            i, j = coord
            if i == j: return None # faster to just do the cases
            if i > j:
                j, i = i, j
                sign = -1
            coord = (i, j)
        elif len(coord) == 3:
            i, j, k = coord
            if i == j or j == k or i == k: return None
            if i > k:
                i, j, k = k, j, i
                sign = -1
            coord = (i, j, k)
        elif len(coord) == 4:
            i, j, k, l = coord
            if (
                    i == j or j == k or i == k
                    or i == l or j == l or k == l
            ): return None
            if i > l:
                i, j, k, l = l, k, j, i
                sign = -1
            coord = (i, j, k, l)
        else:
            if len(np.unique(coord)) < len(coord): return None
            if coord[0] > coord[-1]:
                coord = tuple(reversed(coord))
                sign = -1
            else:
                coord = tuple(coord)
    if return_sign:
        return coord, sign
    else:
        return coord

def is_valid_coordinate(coord):
    """
    **LLM Docstring**

    Return whether a value is an integer index sequence of length two, three, or four.

    :param coord: A single coordinate specification or target coordinate.
    :type coord: Any
    :return: Whether the tested condition is satisfied.
    :rtype: bool
    """
    return (
        len(coord) > 1 and len(coord) < 5
        and all(nput.is_int(c) for c in coord)
    )

def is_coordinate_list_like(clist):
    """
    **LLM Docstring**

    Return whether every element of a sequence is a valid distance, angle, or dihedral specification.

    :param clist: Sequence to test as a coordinate list.
    :type clist: Any
    :return: Whether the tested condition is satisfied.
    :rtype: bool
    """
    return dev.is_list_like(clist) and all(
        is_valid_coordinate(c) for c in clist
    )

class RADInternalCoordinateSet:
    def __init__(self, coord_specs:'list[tuple[int]]', prepped_data=None, triangulation=None):
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
        self._specs = tuple(coord_specs) if coord_specs is not None else coord_specs
        if prepped_data is not None:
            self._indicator, self.coordinate_indices, self.ind_map, self.coord_map = prepped_data
        else:
            self._indicator, self.coordinate_indices, self.ind_map, self.coord_map = self.prep_coords(coord_specs)
        self._triangulation = triangulation

    @property
    def specs(self):
        """
        **LLM Docstring**

        Return the normalized coordinate specifications in their original coordinate-type grouping.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        if self._specs is None:
            self._specs = tuple(self._create_coord_list(self._indicator, self.ind_map, self.coord_map))
        return self._specs

    IndicatorMap = collections.namedtuple("IndicatorMap", ['primary', 'child'])
    IndsMap = collections.namedtuple("IndsMap", ['dists', 'angles', 'diheds'])
    InternalsMap = collections.namedtuple("InternalsMap", ['dists', 'angles', 'diheds'])
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
        dist_inds = []
        dists = []
        angle_inds = []
        angles = []
        dihed_inds = []
        diheds = []
        indicator = []
        subindicator = []
        atoms = {}

        for i,c in coord_specs:
            c = canonicalize_internal(c)
            if c is None: raise ValueError(f"invalid internal coordinate {c}")
            atoms.update(c)
            if len(c) == 2:
                indicator.append(0)
                subindicator.append(len(dists))
                dist_inds.append(i)
                dists.append(c)
            elif len(c) == 2:
                indicator.append(1)
                angle_inds.append(i)
                subindicator.append(len(angles))
                angles.append(c)
            elif len(c) == 4:
                indicator.append(2)
                subindicator.append(len(diheds))
                dihed_inds.append(i)
                diheds.append(c)
            else:
                raise ValueError(f"don't know what to do with coord spec {c}")

        return (
            cls.IndicatorMap(np.array(indicator), np.array(subindicator)),
            tuple(sorted(atoms)),
            cls.IndsMap(np.array(dist_inds), np.array(angle_inds), np.array(dihed_inds)),
            cls.InternalsMap(np.array(dists), np.array(angles), np.array(diheds))
        )

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
        if nput.is_int(coord):
            if coord == 0:
                return map.dists
            elif coord == 1:
                return map.angles
            else:
                return map.diheds
        else:
            if len(coord) == 2:
                return map.dists
            elif len(coord) == 3:
                return map.dists
            elif len(coord) == 4:
                return map.diheds
            else:
                raise ValueError(f"don't know what to do with coord spec {coord}")

    def _coord_map_dispatch(self, coord):
        """
        **LLM Docstring**

        Map a coordinate through the set’s coordinate-level lookup.

        :param coord: A single coordinate specification or target coordinate.
        :type coord: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        return self._map_dispatch(self.coord_map, coord)
    def _ind_map_dispatch(self, i):
        """
        **LLM Docstring**

        Map a flattened coordinate index through the set’s index-level lookup.

        :param i: An atom or flattened-coordinate index, depending on the helper.
        :type i: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        return self._map_dispatch(self.ind_map, i)
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
        return nput.find(self._coord_map_dispatch(coord), coord, missing_val=missing_val)

    @classmethod
    def get_coord_from_maps(cls, item, indicator:IndicatorMap, ind_map, coord_map):
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
        if nput.is_int(item):
            map = indicator.primary[item]
            subloc = indicator.child[item]
            c_map = cls._map_dispatch(coord_map, map)
            return c_map[subloc,]
        else:
            map = indicator.primary[item,]
            uinds = np.unique(map)
            if len(uinds) > 1:
                return [
                    cls.get_coord_from_maps(i, indicator, ind_map, coord_map)
                    for i in item
                ]
            else:
                subloc = indicator.child[item,]
                c_map = cls._map_dispatch(coord_map, uinds[0])
                return c_map[subloc,]

    def __getitem__(self, item):
        """
        **LLM Docstring**

        Support coordinate lookup and indexed/sliced selection through the precomputed coordinate maps.

        :param item: Index, slice, or coordinate selection to resolve.
        :type item: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        return self.get_coord_from_maps(item, self._indicator, self.ind_map, self.coord_map)

    @classmethod
    def _create_coord_list(cls, indicator, inds, vals:InternalsMap):
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
        #TODO: make this more efficient, just concat the sub
        map = np.argsort(indicator.child)
        full = vals.diheds.tolist() + vals.angles.tolist() + vals.diheds.tolist()
        return [ tuple(full[i]) for i in map ]
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
        #TODO: handle padding this
        inv = np.argsort(perm)
        dists = self.coord_map.dists
        if len(dists) > 0:
            dists = inv[dists]
        angles = self.coord_map.angles
        if len(angles) > 0:
            angles = inv[angles]
        diheds = self.coord_map.diheds
        if len(diheds) > 0:
            diheds = inv[diheds]

        cls = type(self)
        int_map = self.InternalsMap(dists, angles, diheds)
        if canonicalize:
            return cls(self._create_coord_list(self._indicator, self.ind_map, int_map))
        else:
            return cls(None, prepped_data=[self._indicator, self.coordinate_indices, self.ind_map, int_map])

    def get_triangulation(self):
        """
        **LLM Docstring**

        Compute triangle and dihedron sets from the stored coordinates and cache the result.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        return get_internal_triangles_and_dihedrons(self.specs, canonicalize=False)
    @property
    def triangulation(self):
        """
        **LLM Docstring**

        Return the cached triangulation, computing it on first access.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        if self._triangulation is None:
            self._triangulation = self.get_triangulation()
        return self._triangulation


def get_canonical_internal_list(coords):
    """
    **LLM Docstring**

    Canonicalize every coordinate in a sequence and remove duplicates while preserving first-occurrence order.

    :param coords: Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
    :type coords: Any
    :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
    :rtype: Any
    """
    if isinstance(coords, RADInternalCoordinateSet):
        return coords.specs
    else:
        return [canonicalize_internal(c) for c in coords]

def find_internal(coords, coord, missing_val:'Any'='raise', canonicalize=True, allow_negation=False, indices=None):
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
    if canonicalize:
        coord = canonicalize_internal(coord)
        if coord is None: raise ValueError(f"invalid internal coordinate {coord}")
    if isinstance(coords, RADInternalCoordinateSet):
        return coords.find(coord, allow_negation=allow_negation)
    else:
        try:
            idx = coords.index(coord)
        except ValueError:
            idx = None

        sign = 1
        if idx is None and allow_negation and len(coord) == 4:
            test = (coord[0],coord[2],coord[1],coord[3])
            idx = find_internal(coords, test, missing_val=None, canonicalize=False, allow_negation=False)
            if idx is not None:
                sign = -1

        if idx is None:
            if dev.str_is(missing_val, 'raise'):
                raise ValueError("{} not in coordinate set".format(coord))
            else:
                idx = missing_val
        elif indices is not None:
            idx = indices[idx]
        if allow_negation:
            return idx, sign
        else:
            return idx

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
    if isinstance(coords, RADInternalCoordinateSet):
        return coords.permute(perm, canonicalize=canonicalize)
    else:
        return [
            canonicalize_internal([perm[c] if c < len(perm) else c for c in coord], check_invalid=False)
                if canonicalize else
            tuple(perm[c] if c < len(perm) else c for c in coord)
            for coord in coords
        ]

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
    if len(old) != len(new): return 0
    if len(old) == 2:
        i,j = old
        m,n = new
        if i == n:
            return int(j == m)
        elif i == m:
            return int(i == n)
        else:
            return 0
    elif len(old) == 3:
        i,j,k = old
        m,n,o = new
        if j != n:
            return 0
        elif i == m:
            return int(k == o)
        elif i == o:
            return int(k == m)
        else:
            return 0
    elif len(old) == 4:
        # all pairwise comparisons now too slow
        if canonicalize:
            old = canonicalize_internal(old, check_invalid=False)
            new = canonicalize_internal(new, check_invalid=False)

        i,j,k,l = old
        m,n,o,p = new

        if i != m or l != p:
            return 0
        elif j == n:
            return int(k == o)
        elif j == o:
            return -int(k == n)
        else:
            return 0
    else:
        raise ValueError(f"can't compare coordinates {old} and {new}")

def coordinate_indices(coords):
    """
    **LLM Docstring**

    Flatten a coordinate list into an integer array and return the per-coordinate arity indicators needed to reconstruct the original tuples.

    :param coords: Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
    :type coords: Any
    :return: The flattened coordinate indices and per-coordinate arity indicators.
    :rtype: tuple[np.ndarray, np.ndarray]
    """
    if isinstance(coords, RADInternalCoordinateSet):
        return coords.coordinate_indices
    else:
        return tuple(sorted(
            {x for c in coords for x in c}
        ))

dm_conv_data = collections.namedtuple("dm_conv_data",
                                      ['input_indices', 'pregen_indices', 'conversion', 'mapped_pos'])
tri_conv = collections.namedtuple("tri_conv", ['type', 'coords', 'val'])
dihed_conv = collections.namedtuple("dihed_conv", ['type', 'coords'])
def _get_input_ind(dm_data):
    """
    **LLM Docstring**

    Return the stored index selecting an original internal-coordinate value from a distance-conversion record.

    :param dm_data: Distance-conversion record containing source-index metadata.
    :type dm_data: Any
    :return: The value or updated object described above.
    :rtype: Any
    """
    return (
        dm_data.input_indices[0]
            if dm_data.conversion is None else
        None
    )
def _get_pregen_ind(dm_data):
    """
    **LLM Docstring**

    Return the stored index selecting a previously generated distance from a distance-conversion record.

    :param dm_data: Distance-conversion record containing source-index metadata.
    :type dm_data: Any
    :return: The value or updated object described above.
    :rtype: Any
    """
    return (
        None
            if dm_data.conversion is None else
        dm_data.mapped_pos
    )
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
    if isinstance(internals, RADInternalCoordinateSet):
        internals = internals.specs
    dists:dict[tuple[int,int], dm_conv_data] = {}
    # we do an initial pass to separate out dists, angles, and dihedrals
    # for checking
    angles:list[tuple[tuple[int,int,int], int]] = []
    dihedrals:list[tuple[tuple[int,int,int,int], int]] = []
    if cache is None: cache = {}
    for n,coord in enumerate(internals):
        if canonicalize:
            coord = canonicalize_internal(coord)
            if coord is None: continue
        if len(coord) == 2:
            coord:tuple[int,int]
            dists[coord] = dm_conv_data([n], [None], None, len(dists))
        elif len(coord) == 3:
            coord:tuple[int,int,int]
            angles.append((coord, n))
        else:
            coord:tuple[int,int,int,int]
            dihedrals.append((coord, n))

    #TODO: add in multiple passes until we stop picking up new distances
    #TODO: prune out ssa rules...these are ambiguous
    for n,((i,j,k),m) in enumerate(angles):
        a = canonicalize_internal((i,j))
        b = canonicalize_internal((j,k))
        c = (i,k)
        if a in dists and b in dists:
            if c not in dists:
                C = (i,j,k)
                d1 = dists[a]
                d2 = dists[b]
                # sas triangle
                dists[c] = dm_conv_data(
                    (_get_input_ind(d1), m, _get_input_ind(d2)),
                    (_get_pregen_ind(d1), None, _get_pregen_ind(d2)),
                    tri_conv('sas', (a, C, b), 2),
                    len(dists)
                )
        # elif a in dists and c in dists:
        #     # ssa triangle, angle at `i`
        #     if b not in dists:
        #         C = (i,j,k)
        #         d1 = dists[c]
        #         d2 = dists[a]
        #         # sas triangle
        #         dists[b] = dm_conv_data(
        #             (_get_input_ind(d1), _get_input_ind(d2), m),
        #             (_get_pregen_ind(d1), _get_pregen_ind(d2), None),
        #             tri_conv('ssa', (c, a, C), 2),
        #             len(dists)
        #         )
        # elif b in dists and c in dists:
        #     # ssa triangle, angle at `k`
        #     if a not in dists:
        #         B = (i,j,k)
        #         d1 = dists[b]
        #         d2 = dists[c]
        #         # sas triangle
        #         dists[a] = dm_conv_data(
        #             (_get_input_ind(d1), _get_input_ind(d2), m),
        #             (_get_pregen_ind(d1), _get_pregen_ind(d2), None),
        #             tri_conv('ssa', (b, c, B), 2),
        #             len(dists)
        #         )
        else:
            # try to another angle triangle coordinates that can be converted back to sss form
            for (ii,jj,kk),m2 in angles[n+1:]:
                # all points must be shared
                if k == jj and (
                        i == ii and j == kk
                        or i == kk and j == ii
                ):
                    C = (i, j, k)
                    A = (i, k, j)
                    if a in dists: # (i,j)
                        # we have saa
                        d = dists[a]
                        if b not in dists:
                            dists[b] = dm_conv_data(
                                (_get_input_ind(d), m, m2),
                                (_get_pregen_ind(d), None, None),
                                tri_conv('saa', (a, C, A), 2),
                                len(dists)
                            )
                        if c not in dists:
                            dists[c] = dm_conv_data(
                                (_get_input_ind(d), m, m2),
                                (_get_pregen_ind(d), None, None),
                                tri_conv('saa', (a, C, A), 1),
                                len(dists)
                            )
                    elif b in dists: # (k, j)
                        d = dists[b]
                        if a not in dists:
                            dists[a] = dm_conv_data(
                                (m, _get_input_ind(d), m2),
                                (None, _get_pregen_ind(d), None),
                                tri_conv('asa', (C, b, A), 1),
                                len(dists)
                            )
                        if c not in dists:
                            dists[c] = dm_conv_data(
                                (m, _get_input_ind(d), m2),
                                (None, _get_pregen_ind(d), None),
                                tri_conv('asa', (C, b, A), 2),
                                len(dists)
                            )
                    elif c in dists: # (i, k)
                        d = dists[c]
                        if b not in dists:
                            dists[b] = dm_conv_data(
                                (_get_input_ind(d), m2, m),
                                (_get_pregen_ind(d), None, None),
                                tri_conv('saa', (c, A, C), 2),
                                len(dists)
                            )
                        if c not in dists:
                            dists[a] = dm_conv_data(
                                (_get_input_ind(d), m2, m),
                                (_get_pregen_ind(d), None, None),
                                tri_conv('saa', (c, A, C), 1),
                                len(dists)
                            )
                elif i == jj and (
                        k == ii and j == kk
                        or k == kk and j == ii
                ):
                    C = (i, j, k)
                    B = (j, i, k)
                    if a in dists: # (i,j)
                        d = dists[a]
                        if b not in dists:
                            dists[b] = dm_conv_data(
                                (m, _get_input_ind(d), m2),
                                (None, _get_pregen_ind(d), None),
                                tri_conv('asa', (C, a, B), 1),
                                len(dists)
                            )
                        if c not in dists:
                            dists[c] = dm_conv_data(
                                (m, _get_input_ind(d), m2),
                                (None, _get_pregen_ind(d), None),
                                tri_conv('asa', (C, a, B), 2),
                                len(dists)
                            )
                    elif b in dists: # (k, j)
                        d = dists[b]
                        if a not in dists:
                            dists[a] = dm_conv_data(
                                (_get_input_ind(d), m, m2),
                                (_get_pregen_ind(d), None, None),
                                tri_conv('saa', (b, C, B), 2),
                                len(dists)
                            )
                        if c not in dists:
                            dists[c] =  dm_conv_data(
                                (_get_input_ind(d), m, m2),
                                (_get_pregen_ind(d), None, None),
                                tri_conv('saa', (b, C, B), 1),
                                len(dists)
                            )
                    elif c in dists: # (i, k)
                        d = dists[c]
                        if a not in dists:
                            dists[a] = dm_conv_data(
                                (_get_input_ind(d), m2, m),
                                (_get_pregen_ind(d), None, None),
                                tri_conv('saa', (c, B, C), 2),
                                len(dists)
                            )
                        if b not in dists:
                            dists[b] = dm_conv_data(
                                (_get_input_ind(d), m2, m),
                                (_get_pregen_ind(d), None, None),
                                tri_conv('saa', (c, B, C), 1),
                                len(dists)
                            )
                # x = canonicalize_internal((ii, jj))
                # y = canonicalize_internal((jj, kk))
                # z = (ii, kk)
                # if x == a:
                #     ...

    angle_dict = dict(angles)
    for n,((i,j,k,l),m) in enumerate(dihedrals):
        d = canonicalize_internal((i,l))
        if d not in dists:
            a = canonicalize_internal((i,j))
            b = canonicalize_internal((j,k))
            c = canonicalize_internal((k,l))
            x = canonicalize_internal((i,k))
            y = canonicalize_internal((j,l))
            if (
                    a in dists
                    and b in dists
                    and c in dists
            ):
                A = canonicalize_internal((i,j,k))
                B = canonicalize_internal((j,k,l))
                if A in angle_dict:
                    if B in angle_dict:
                        d1 = dists[a]
                        d2 = dists[b]
                        d3 = dists[c]
                        m1 = angle_dict[A]
                        m2 = angle_dict[B]
                        dists[d] = dm_conv_data(
                            (_get_input_ind(d1), _get_input_ind(d2), _get_input_ind(d3), m1, m2, m),
                            (_get_pregen_ind(d1), _get_pregen_ind(d2), _get_pregen_ind(d3), None, None, None),
                            dihed_conv('sssaat', (a, b, c, A, B, (i,j,k,l))),
                            len(dists)
                        )
                    elif y in dists:
                        d1 = dists[c]
                        d2 = dists[b]
                        d3 = dists[a]
                        d4 = dists[y]
                        m1 = angle_dict[A]
                        dists[d] = dm_conv_data(
                            (_get_input_ind(d1), _get_input_ind(d2), _get_input_ind(d3), _get_input_ind(d4), m1, m),
                            (_get_pregen_ind(d1), _get_pregen_ind(d2), _get_pregen_ind(d3), _get_pregen_ind(d4), None, None, None),
                            dihed_conv('ssssat', (c, b, a, y, A, (i,j,k,l))),
                            len(dists)
                        )
                elif B in angle_dict:
                    if x in dists:
                        d1 = dists[a]
                        d2 = dists[b]
                        d3 = dists[c]
                        d4 = dists[x]
                        m1 = angle_dict[B]
                        dists[d] = dm_conv_data(
                            (_get_input_ind(d1), _get_input_ind(d2), _get_input_ind(d3), _get_input_ind(d4), m1, m),
                            (_get_pregen_ind(d1), _get_pregen_ind(d2), _get_pregen_ind(d3), _get_pregen_ind(d4), None, None),
                            dihed_conv('ssssat', (a, b, c, x, B, (i,j,k,l))),
                            len(dists)
                        )
                elif x in dists and y in dists:
                    d1 = dists[a]
                    d2 = dists[b]
                    d3 = dists[c]
                    d4 = dists[x]
                    d5 = dists[y]
                    dists[d] = dm_conv_data(
                        (_get_input_ind(d1), _get_input_ind(d2), _get_input_ind(d3), _get_input_ind(d4), _get_input_ind(d5), m),
                        (_get_pregen_ind(d1), _get_pregen_ind(d2), _get_pregen_ind(d3), _get_pregen_ind(d4), _get_pregen_ind(d5), None,
                         None),
                        dihed_conv('ssssst', (a, b, c, x, y, (i, j, k, l))),
                        len(dists)
                    )


    return dists

def _prep_interal_distance_conversion(conversion_spec:dm_conv_data):
    """
    **LLM Docstring**

    Compile a distance-conversion specification into a callable specialized for direct distances, law-of-cosines triangle completion, or dihedral tetrahedron completion.

    :param conversion_spec: Ordered recipe describing how each distance is obtained.
    :type conversion_spec: dm_conv_data
    :return: The value or updated object described above.
    :rtype: Any
    """
    if conversion_spec.conversion is None:
        def convert(internal_values, _, n=conversion_spec.input_indices[0]):
            """
            **LLM Docstring**

            Evaluate the specialized conversion step: either select an existing internal distance, compute a missing triangle edge from two edges and an angle, or compute the remaining tetrahedral edge from five distances and a dihedral.

            :param internal_values: Numerical values of the source internal coordinates.
            :type internal_values: Any
            :param _: Unused positional argument retained to match the common conversion-callable interface.
            :type _: Any
            :param n: Source column index captured when the specialized conversion callable is created.
            :type n: Any
            :return: The value or updated object described above.
            :rtype: Any
            """
            return internal_values[..., n]
    elif hasattr(conversion_spec.conversion, 'val'):
        # a triangle to convert
        #TODO: allow triangle conversions to share context
        conversion:tri_conv = conversion_spec.conversion
        triangle_converter = nput.triangle_converter(conversion.type, 'sss')
        val = conversion.val
        int_args = conversion_spec.input_indices
        dist_args = conversion_spec.pregen_indices
        def convert(internal_values, distance_values,
                    order=None,
                    int_args=int_args,
                    dist_args=dist_args,
                    converter=triangle_converter,
                    val=val,
                    **kwargs):
            """
            **LLM Docstring**

            Evaluate the specialized conversion step: either select an existing internal distance, compute a missing triangle edge from two edges and an angle, or compute the remaining tetrahedral edge from five distances and a dihedral.

            :param internal_values: Numerical values of the source internal coordinates.
            :type internal_values: Any
            :param _: Unused positional argument retained to match the common conversion-callable interface.
            :type _: Any
            :param n: Source column index captured when the specialized conversion callable is created.
            :type n: Any
            :return: The value or updated object described above.
            :rtype: Any
            """
            args = [
                internal_values[..., n]
                    if n is not None else
                distance_values[..., m]
                for n,m in zip(int_args, dist_args)
            ]
            if order is None:
                return converter[0](*args)[val]
            else:
                return converter[1](*args, order=order, **kwargs)[val]
    else:
        # a dihedral to convert
        conversion:dihed_conv = conversion_spec.conversion
        dist_converter = nput.dihedral_distance_converter(conversion.type)
        int_args = conversion_spec.input_indices
        dist_args = conversion_spec.pregen_indices
        def convert(internal_values, distance_values,
                    order=None,
                    *,
                    int_args=int_args,
                    dist_args=dist_args,
                    converter=dist_converter,
                    **kwargs):
            """
            **LLM Docstring**

            Evaluate the specialized conversion step: either select an existing internal distance, compute a missing triangle edge from two edges and an angle, or compute the remaining tetrahedral edge from five distances and a dihedral.

            :param internal_values: Numerical values of the source internal coordinates.
            :type internal_values: Any
            :param _: Unused positional argument retained to match the common conversion-callable interface.
            :type _: Any
            :param n: Source column index captured when the specialized conversion callable is created.
            :type n: Any
            :return: The value or updated object described above.
            :rtype: Any
            """
            args = [
                internal_values[..., n]
                    if n is not None else
                distance_values[..., m]
                for n,m in zip(int_args, dist_args)
            ]
            if order is None:
                return converter[0](*args)[val]
            else:
                return converter[1](*args, order=order, **kwargs)[val]
    return convert
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
    base_conv = get_internal_distance_conversion_spec(internals, canonicalize=canonicalize)
    final_inds = list(sorted(base_conv.keys(), key=lambda k:base_conv[k].mapped_pos))
    rordered_conversion = list(sorted(base_conv.values(), key=lambda v:v.mapped_pos))
    convs = [
        _prep_interal_distance_conversion(v) for v in rordered_conversion
    ]
    dihedral_pos = [i for i,v in enumerate(internals) if len(v) == 4]
    def convert(internal_values,
                inds=final_inds, convs=convs,
                dihedral_pos=dihedral_pos,
                shift_dihedrals=shift_dihedrals):
        """
        **LLM Docstring**

        Evaluate all generated-distance steps in dependency order and concatenate the original distance values with the newly reconstructed pair distances.

        :param internal_values: Numerical values of the source internal coordinates.
        :type internal_values: Any
        :param inds: Flattened coordinate index data.
        :type inds: Any
        :param convs: Previously compiled distance-conversion callables evaluated before this step.
        :type convs: Any
        :param dihedral_pos: Positions of dihedral values in the source internal-coordinate vector.
        :type dihedral_pos: Any
        :param shift_dihedrals: Whether periodic dihedral values are shifted to the expected reconstruction branch.
        :type shift_dihedrals: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        internal_values = np.asanyarray(internal_values)
        if shift_dihedrals:
            internal_values = internal_values.copy()
            # force to be positive, push back onto appro
            internal_values[..., dihedral_pos] = np.pi - np.abs(internal_values[..., dihedral_pos])
        elif abs_dihedrals:
            internal_values = internal_values.copy()
            # force to be positive, push back onto appro
            internal_values[..., dihedral_pos] = np.abs(internal_values[..., dihedral_pos])
        dists = np.zeros(internal_values.shape[:-1] + (len(convs),))
        for n,c in enumerate(convs):
            dists[..., n] = c(internal_values, dists)

        return dists

    return final_inds, convert
def _check_complete_distances(final_dists):
    """
    **LLM Docstring**

    Verify that a generated distance set contains every pair needed for the inferred atom range; raise an error listing missing pairs when it does not.

    :param final_dists: Generated pair-distance mapping or sequence to validate.
    :type final_dists: Any
    :return: The value or updated object described above.
    :rtype: Any
    """
    ds = set(final_dists)
    final_dists = list(final_dists)
    inds = np.unique([x for y in final_dists for x in y])
    targs = list(itertools.combinations(inds, 2))
    missing = []
    ord = []
    for i,j in targs:
        if (i,j) in ds:
            ord.append(final_dists.index((i,j)))
        elif (j,i) in ds:
            ord.append(final_dists.index((j,i)))
        else:
            missing.append((i,j))

    if len(missing) > 0:
        raise ValueError(f"distance set missing: {missing}")

    return ord
def internal_distance_convert(coords, specs,
                              canonicalize=True,
                              shift_dihedrals=True,
                              abs_dihedrals=True,
                              check_distance_spec=True):
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
    final_dists, converter = get_internal_distance_conversion(specs,
                                                              canonicalize=canonicalize,
                                                              shift_dihedrals=shift_dihedrals,
                                                              abs_dihedrals=abs_dihedrals
                                                              )
    if check_distance_spec:
        ord = _check_complete_distances(final_dists)
    else:
        ord = None
    conv = converter(coords)
    if ord is not None:
        conv = conv[..., ord]
        final_dists = [final_dists[i] for i in ord]
    return final_dists, conv

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
    a_idx = find_internal(internals, a, missing_val=None)
    found_main = True
    if a_idx is None:
        found_main = False
        a_idx = find_internal(prior_coords, a, missing_val=None)
    if a_idx is None:
        if dev.str_is(missing_val, 'raise'):
            raise ValueError(f"can't construct {coord} from internals (requires {a})")
    return a_idx, found_main
_tri_perms = [
        (0, 1, 2),
        (0, 2, 1),
        (1, 0, 2)
    ]
_tri_perm_inv = _tri_perms
def _get_tri_bond_key_name(mod_sets, a,b,c, i, j):
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
    base = (a, b, c)
    for perm in _tri_perms:
        key = [base[_] for _ in perm]
        key, sign = canonicalize_internal(key, return_sign=True, check_invalid=False)
        if key in mod_sets:
            break
    else:
        perm = (0, 1, 2)
        key, sign = canonicalize_internal((a, b, c), return_sign=True, check_invalid=False)
    if sign == -1:
        perm = list(reversed(perm))
    perm = np.argsort(perm)

    b = tuple(sorted(key.index(_) for _ in [i,j]))
    return key, nput.triangle_property_specifiers(b)["name"], perm
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
    new = set()
    for t in terms:
        x = nput.triangle_property_specifiers(t)["coord"]
        y = canonicalize_internal([perm[i] for i in x])
        new.add(nput.triangle_property_specifiers(y)["name"])
    return new
_dihedron_perms = [
        (0, 1, 2, 3),
        (0, 2, 1, 3),
        (0, 2, 3, 1),
        (0, 3, 2, 1),
        (0, 1, 3, 2),
        (0, 3, 1, 2),
        (1, 0, 2, 3),
        (1, 2, 0, 3),
        (1, 0, 3, 2),
        (1, 3, 0, 2),
        (2, 0, 1, 3),
        (2, 1, 0, 3)
    ]
_dihedron_perm_inv = [
    (0, 1, 2, 3),
    (0, 2, 1, 3),
    (0, 3, 1, 2),
    (0, 3, 2, 1),
    (0, 1, 3, 2),
    (0, 2, 3, 1),
    (1, 0, 2, 3),
    (2, 0, 1, 3),
    (1, 0, 3, 2),
    (2, 0, 3, 1),
    (1, 2, 0, 3),
    (2, 1, 0, 3)
]
def _get_dihedron_bond_key_name(mod_sets, a,b,c,d, i, j):
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
    base = (a, b, c, d)
    for perm in _dihedron_perms:
        key = [base[_] for _ in perm]
        key, sign = canonicalize_internal(key, return_sign=True, check_invalid=False)
        if key in mod_sets:
            break
    else:
        perm = (0, 1, 2, 3)
        key, sign = canonicalize_internal((a, b, c, d), return_sign=True, check_invalid=False)
    if sign == -1:
        perm = list(reversed(perm))
    perm = np.argsort(perm)

    b = tuple(sorted(key.index(_) for _ in [i,j]))
    return key, nput.dihedron_property_specifiers(b)["name"], perm
def _get_dihedron_angle_key_name(mod_sets, a,b,c,d, i, j, k):
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
    base = (a, b, c, d)
    for perm in _dihedron_perms:
        key = [base[_] for _ in perm]
        key, sign = canonicalize_internal(key, return_sign=True, check_invalid=False)
        if key in mod_sets:
            break
    else:
        perm = (0, 1, 2, 3)
        key, sign = canonicalize_internal((a, b, c, d), return_sign=True, check_invalid=False)
    if sign == -1:
        perm = list(reversed(perm))
    perm = np.argsort(perm)

    b = canonicalize_internal(tuple(key.index(_) for _ in [i,j,k]))
    z = nput.dihedron_property_specifiers(b)["name"]
    return key, z, perm
def _get_dihedron_dihed_key_name(mod_sets, a,b,c,d, i, j, k, l):
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
    base = (a, b, c, d)
    for perm in _dihedron_perms:
        key = [base[_] for _ in perm]
        key, sign = canonicalize_internal(key, return_sign=True, check_invalid=False)
        if key in mod_sets:
            break
    else:
        perm = (0, 1, 2, 3)
        key, sign = canonicalize_internal((a, b, c, d), return_sign=True, check_invalid=False)
    if sign == -1:
        perm = list(reversed(perm))
    perm = np.argsort(perm)

    key_pos = tuple(key.index(_) for _ in [i,j,k,l])
    x = canonicalize_internal(key_pos)
    z = nput.dihedron_property_specifiers(x)["name"]
    return key, z, perm
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
    new = set()
    for t in terms:
        x = nput.dihedron_property_specifiers(t)["coord"]
        y = canonicalize_internal([perm[i] for i in x])
        new.add(nput.dihedron_property_specifiers(y)["name"])
    return new
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
    for k in mod_sets.keys():
        if None in k: continue
        if canonicalize_internal(k, check_invalid=False) != k:
            raise ValueError(f"non-canonical key {k}")
    if None not in key:
        for p in itertools.permutations(key):
            if p != key and p in mod_sets:
                raise ValueError(f"key {key} is duped as {p} ({mod_sets[p]})")
    for a in mod_sets.get(key, []):
        idx = nput.dihedron_property_specifiers(a)["coord"]
        c = canonicalize_internal(tuple(key[i] for i in idx))
        if len(c) == 4 and c not in internals: # check the inverse too
            c = canonicalize_internal([c[0], c[2], c[1], c[3]])
        if c not in internals:
            if adding is None:
                raise ValueError(f"internal list doesn't contain {c} (from '{a}' on {key}) : {internals} ")
            else:
                raise ValueError(f"internal list doesn't contain {c} (from '{a}' on {key}, adding '{adding}') : {internals} ")
    _check_dihed_coords(internals, mod_sets)
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
    for k, v in tri_sets.items():
        if None not in k:
            for c in v:
                if c is None: continue
                if isinstance(c, str):
                    c = tuple(k[i] for i in nput.triangle_property_specifiers(c)['coord'])
                if c not in internals and tuple(reversed(c)) not in internals:
                    raise ValueError(f"triangle {k} has invalid coordinate {c}")
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
    for k, v in dihed_sets.items():
        if None not in k:
            if canonicalize_internal(k, check_invalid=False) != k:
                raise ValueError(f"non-canonical key {k}")
            for c in v:
                if c is None: continue
                if isinstance(c, str):
                    c = tuple(k[i] for i in nput.dihedron_property_specifiers(c)['coord'])
                if (
                        c not in internals
                        and tuple(reversed(c)) not in internals
                        and not (
                        len(c) == 4 and (
                            (c[0], c[2], c[1], c[3]) in internals
                            or (c[3], c[1], c[2], c[0]) in internals
                        )
                    )
                ):
                    raise ValueError(f"dihedron {k} has invalid coordinate {c}")
def get_internal_triangles_and_dihedrons(internals,
                                         canonicalize=True,
                                         base=None,
                                         base_internals=None,
                                         construct_shapes=True,
                                         prune_incomplete=True,
                                         validate=False,
                                         allow_partially_defined=True,
                                         create_compound_dihedra=True,
                                         add_dihedron_triangles=False,
                                         create_dihedra=True) -> tuple[
    dict[tuple[int, int, int], nput.TriangleData],
    dict[tuple[int, int, int, int], nput.DihedralTetrahedronData]
]:
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
    if base is None:
        tri_sets:dict[tuple[int],set] = {}
        dihed_sets:dict[tuple[int],set] = {}
        base_internals = []
    else:
        tri_sets, dihed_sets = base
        if len(dihed_sets) > 100: raise Exception(f"too many dihered sets : {len(dihed_sets)}")
        if base_internals is None:
            base_internals = list(itut.delete_duplicates(itertools.chain(
                (
                    c
                    for k, v in tri_sets.items()
                    for s, c in
                        (v._asdict().items() if hasattr(v, "_asdict") else [])
                    if c is not None
                ),
                (
                    c
                    for k, v in dihed_sets.items()
                    for s, c in
                        (v._asdict().items() if hasattr(v, "_asdict") else [])
                    if c is not None
                )
            )))
        tri_sets = {
            k: (
                {s for s, c in v._asdict().items() if c is not None}
                    if hasattr(v, "_asdict") else
                v
            )
            for k, v in tri_sets.items()
        }
        if validate: _check_tri_coords(base_internals, tri_sets)
        dihed_sets = {
            k: (
                {s for s, c in v._asdict().items() if c is not None}
                    if hasattr(v, "_asdict") else
                v
            )
            for k, v in dihed_sets.items()
        }
    update_ds = set()
    updat_ts = set()
    for coord in internals:
        if canonicalize:
            coord = canonicalize_internal(coord)
        if len(coord) == 2:
            i,j = coord
            mod_tris = tri_sets.copy()
            for (k,l,m),v in tri_sets.items():
                key = (k, l, m)
                if i == k:
                    if j == l:
                        v.add("a")
                        if validate: _check_tri_coords(base_internals + internals, mod_tris)
                    elif j == m:
                        v.add("c")
                        if validate: _check_tri_coords(base_internals + internals, mod_tris)
                    elif m is None:
                        key, z, perm = _get_tri_bond_key_name(mod_tris, k, l, j, i, j)
                        v = _permute_tri_data(v, perm)
                        mod_tris[key] = mod_tris.get(key, set()) | v | {z}
                        if validate: _check_tri_coords(base_internals + internals, mod_tris)
                elif i == l:
                    if j == k:
                        v.add("a")
                        if validate: _check_tri_coords(base_internals + internals, mod_tris)
                    elif j == m:
                        v.add("b")
                        if validate: _check_tri_coords(base_internals + internals, mod_tris)
                    elif m is None:
                        key, z, perm = _get_tri_bond_key_name(mod_tris, k, l, j, i, j)
                        v = _permute_tri_data(v, perm)
                        mod_tris[key] = mod_tris.get(key, set()) | v | {z}
                        if validate: _check_tri_coords(base_internals + internals, mod_tris)
                elif i == m:
                    if j == l:
                        mod_tris[(k,l,m)].add("b")
                        if validate: _check_tri_coords(base_internals + internals, mod_tris)
                    elif j == k:
                        mod_tris[(k,l,m)].add("c")
                        if validate: _check_tri_coords(base_internals + internals, mod_tris)
                elif m is None and j in (k, l):
                    key, z, perm = _get_tri_bond_key_name(mod_tris, k, l, i, i, j)
                    v = _permute_tri_data(v, perm)
                    mod_tris[key] = mod_tris.get(key, set()) | v | {z}
                    if validate: _check_tri_coords(base_internals + internals, mod_tris)
                if None not in key:
                    updat_ts.add(key)
            else:
                mod_tris[(i,j,None)] = {"a"}
            tri_sets = mod_tris

            if create_dihedra:
                mod_sets = dihed_sets.copy()
                for (k, l, m, n), v in dihed_sets.items():
                    key = None
                    # if j in (k,l,m,n):
                    #     i,j = j,i
                    if i == k:
                        if j == l:
                            v.add("a")
                            key = (k, l, m, n)
                            if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                        elif j == m:
                            v.add("x")
                            key = (k, l, m, n)
                            if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                        elif j == n:
                            v.add("z")
                            key = (k, l, m, n)
                            if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                        elif m is None:
                            key = (k, l, j, None)
                            mod_sets[key] = mod_sets.get(key, set()) | v | {"x"}
                            if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                        elif n is None:
                            key, z, perm = _get_dihedron_bond_key_name(mod_sets, k,l,m,j, i, j)
                            v = _permute_dihed_data(v, perm)
                            mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                            if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                    elif i == l:
                        if j == k:
                            v.add("a")
                            key = (k, l, m, n)
                            if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                        elif j == m:
                            v.add("b")
                            key = (k, l, m, n)
                            if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                        elif j == n:
                            v.add("y")
                            key = (k, l, m, n)
                            if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                        elif m is None:
                            key = (k,l,j,n)
                            mod_sets[key] = mod_sets.get(key, set()) | v | {"b"}
                            if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                        elif n is None:
                            key, z, perm = _get_dihedron_bond_key_name(mod_sets, k,l,m,j, i, j)
                            v = _permute_dihed_data(v, perm)
                            mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                            if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                    elif i == m:
                        if j == k:
                            #TODO: double check this doesn't duplicate somehow
                            key = (k,l,m,n)
                            mod_sets[key].add("x")
                            if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                        elif j == l:
                            key = (k,l,m,n)
                            mod_sets[key].add("b")
                            if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                        elif j == n:
                            key = (k,l,m,n)
                            mod_sets[key].add("c")
                            if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                        elif n is None:
                            key, z, perm = _get_dihedron_bond_key_name(mod_sets, k, l, m, j, i, j)
                            v = _permute_dihed_data(v, perm)
                            mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                            if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                    elif i == n:
                        # j can't be k by sorting
                        if j == l:
                            key = (k,l,m,n)
                            mod_sets[key].add("y")
                            if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                        elif j == m:
                            key = (k,l,m,n)
                            mod_sets[key].add("c")
                            if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                    elif m is None:
                        if j == k:
                            key = (k,l,i,n)
                            mod_sets[key] = mod_sets.get(key, set()) | v | {"x"}
                            if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                        elif j == l:
                            key = (k,l,i,n)
                            mod_sets[key] = mod_sets.get(key, set()) | v | {"b"}
                            if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                        else:
                            key, z, perm = _get_dihedron_bond_key_name(mod_sets, k, l, i, j, i, j)
                            v = _permute_dihed_data(v, perm)
                            mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                            if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                    elif n is None:
                        if j in (k,l,m):
                            key, z, perm = _get_dihedron_bond_key_name(mod_sets, k, l, m, i, i, j)
                            v = _permute_dihed_data(v, perm)
                            mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                            if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals, z)
                    if key is not None:
                        if None not in key: update_ds.add(key)
                        if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                else:
                    if (i, j, None, None) not in mod_sets:
                        mod_sets[(i, j, None, None)] = {"a"}
                dihed_sets = mod_sets
        elif len(coord) == 3:
            i,j,k = coord
            C = i,j,k
            A, sA = canonicalize_internal((i,k,j), return_sign=True, check_invalid=False)
            B, sB = canonicalize_internal((j,i,k), return_sign=True, check_invalid=False)
            if C in tri_sets:
                tri_sets[C].add("C")
                updat_ts.add(C)
                if validate: _check_tri_coords(base_internals + internals, tri_sets)
            elif A in tri_sets:
                # (i,k,j), (i,j,k)
                tri_sets[A].add("A" if i < j else "B")
                updat_ts.add(A)
                if validate: _check_tri_coords(base_internals + internals, tri_sets)
            elif B in tri_sets:
                # (j,i,k), (i,j,k)
                tri_sets[B].add("B" if j < k else "A")
                updat_ts.add(B)
                if validate: _check_tri_coords(base_internals + internals, tri_sets)
            elif (A[0],A[2], None) in tri_sets:
                if j == A[2]:
                    # centered on "j" -> C
                    tri_sets[C] = {"a" if i < k else "b", "C"}
                    updat_ts.add(C)
                    if validate: _check_tri_coords(base_internals + internals, tri_sets)
                else:
                    # (j,i,k), (i,j,k): centered on "i" -> B or (k,j,i): "k" -> A
                    tri_sets[B] = {"a" if j < k else "b", "B" if j < k else "A"}
                    updat_ts.add(B)
                    if validate: _check_tri_coords(base_internals + internals, tri_sets)
            elif (B[0],B[2], None) in tri_sets:
                if k == B[2]:
                    # (i,k,j), (i,j,k): centered on "k" -> A or (k,j,i): "i" -> B
                    tri_sets[A] = {"b" if i < j else "a", "A" if i < j else "B"}
                    updat_ts.add(A)
                    if validate: _check_tri_coords(base_internals + internals, tri_sets)
                else:
                    # (i,j,k), (i,j,k): centered on "j" -> C
                    tri_sets[C] = {"b" if i < k else "a", "C"}
                    updat_ts.add(C)
                    if validate: _check_tri_coords(base_internals + internals, tri_sets)
            elif (C[0],C[2], None) in tri_sets:
                if k == C[2]:
                    # (i,k,j), (i,j,k): centered on "k" -> A or (k,j,i): "i" -> B
                    tri_sets[A] = {"a" if i < j else "b", "A" if i < j else "B"}
                    updat_ts.add(A)
                    if validate: _check_tri_coords(base_internals + internals, tri_sets)
                else:
                    # (j,i,k), (i,j,k): centered on "i" -> B or (k,j,i): "k" -> A
                    tri_sets[B] = {"a" if j < k else "b", "B" if j < k else "A"}
                    updat_ts.add(B)
                    if validate: _check_tri_coords(base_internals + internals, tri_sets)

            if create_dihedra:
                mod_sets = dihed_sets.copy()
                for (a, l, m, n), v in dihed_sets.items():
                    key = None
                    if m is None:
                        if i == a:
                            if j == l:
                                key = (a, l, k, n)
                                mod_sets[key] = mod_sets.get(key, set()) | v | {"X"}
                                if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                            elif k == l:
                                key = (a, l, j, n)
                                mod_sets[key] = mod_sets.get(key, set()) | v | {"A"}
                                if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                            else:
                                key, z, perm = _get_dihedron_angle_key_name(mod_sets, a,l,j,k, i, j, k)
                                v = _permute_dihed_data(v, perm)
                                mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                                if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                        elif i == l:
                            if j == a:
                                key = (a, l, k, n)
                                mod_sets[key] = mod_sets.get(key, set()) | v | {"B1"}
                                if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                            elif k == a:
                                key = (a, l, j, n)
                                mod_sets[key] = mod_sets.get(key, set()) | v | {"A"}
                                if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                            else:
                                key, z, perm = _get_dihedron_angle_key_name(mod_sets, a,l,j,k, i, j, k)
                                v = _permute_dihed_data(v, perm)
                                mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                                if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                        elif j == a:
                            if k == l:
                                key = (a, l, i, n)
                                mod_sets[key] = mod_sets.get(key, set()) | v | {"B1"}
                                if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                            else:
                                key, z, perm = _get_dihedron_angle_key_name(mod_sets, a,l,i,k, i, j, k)
                                v = _permute_dihed_data(v, perm)
                                mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                        elif j == l:
                            if k == a:
                                key = (a, l, i, n)
                                mod_sets[key] = mod_sets.get(key, set()) | v | {"X"}
                                if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                            else:
                                key, z, perm = _get_dihedron_angle_key_name(mod_sets, a,l,i,k, i, j, k)
                                v = _permute_dihed_data(v, perm)
                                mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                                if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                        elif k in {a,l}:
                            key, z, perm = _get_dihedron_angle_key_name(mod_sets, a,l,i,j, i, j, k)
                            v = _permute_dihed_data(v, perm)
                            mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                            if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                    elif n is None:
                        C1, s = canonicalize_internal((a, l, m), return_sign=True, check_invalid=False)
                        if C == C1:
                            key = (a, l, m, n)
                            mod_sets[key].add("X")
                            if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                        elif A == C1: # i,k,j == (a,l,m)
                            key = (a, l, m, n)
                            mod_sets[key].add("A" if (sA * s) > 0 else "B1")
                            if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                        elif B == C1: # k,i,j == (a,l,m)
                            key = (a, l, m, n)
                            mod_sets[key].add("B1" if (sB * s) > 0 else "A")
                            if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals)
                        else:
                            if i in (a,l,m):
                                if j in (a,l,m):
                                    key, z, perm = _get_dihedron_angle_key_name(mod_sets, a, l, m, k, i, j, k)
                                    v = _permute_dihed_data(v, perm)
                                    mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                                    if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals, (a, l, m, n))
                                elif k in (a,l,m):
                                    key, z, perm = _get_dihedron_angle_key_name(mod_sets, a, l, m, j, i, j, k)
                                    v = _permute_dihed_data(v, perm)
                                    mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                                    if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals, (a, l, m, n))
                            elif j in (a,l,m) and k in (a,l,m):
                                key, z, perm = _get_dihedron_angle_key_name(mod_sets, a, l, m, i, i, j, k)
                                # u = v
                                v = _permute_dihed_data(v, perm)
                                # print("???", u, v, perm, z)
                                mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                                if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals, (a, l, m, n))
                            # for (aa,ll) in itertools.combinations([a, l, m], 2):
                            #     if i == aa:
                            #         if j == ll:
                            #             key, z = _get_dihedron_angle_key_name(mod_sets, a, l, m, k, i, j, k)
                            #             mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                            #             break
                            #         elif k == ll:
                            #             key, z = _get_dihedron_angle_key_name(mod_sets, a, l, m, j, i, j, k)
                            #             mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                            #             break
                            #     elif i == ll:
                            #         if j == a:
                            #             key, z = _get_dihedron_angle_key_name(mod_sets, a, l, m, k, i, j, k)
                            #             mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                            #             break
                            #         elif k == a:
                            #             key, z = _get_dihedron_angle_key_name(mod_sets, a, l, m, j, i, j, k)
                            #             mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                            #             break
                            #     elif j == a and k == l:
                            #         key, z = _get_dihedron_angle_key_name(mod_sets, a, l, m, i, i, j, k)
                            #         mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                            #         break
                            #     elif j == l and k == a:
                            #         key, z = _get_dihedron_angle_key_name(mod_sets, a, l, m, i, i, j, k)
                            #         mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                            #         break
                            # print("~~~", (aa,ll), (i,j,k))
                    else:
                        for (x, y, z), (_, _, _, X, Y, Z) in [
                            [(a, l, m), ("a", "b", "x", "A", "B1", "X")],
                            [(l, m, n), ("b", "c", "y", "B2", "C", "Y")],
                            [(a, l, n), ("a", "y", "z", "A3", "Y3", "Z")],
                            [(a, m, n), ("x", "c", "z", "X4", "C4", "Z2")]
                        ]:
                            C1 = canonicalize_internal((x, y, z), check_invalid=False)
                            A1 = canonicalize_internal((x, z, y), check_invalid=False)
                            B1 = canonicalize_internal((y, x, z), check_invalid=False)
                            if C == C1:
                                key = (a, l, m, n)
                                mod_sets[key].add(Z)
                            elif C == A1:
                                key = (a, l, m, n)
                                mod_sets[key].add(X)
                            elif C == B1:
                                key = (a, l, m, n)
                                mod_sets[key].add(Y)

                    if key is not None:
                        if None not in key: update_ds.add(key)
                        if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals, (a, l, m, n))
                else:
                    if (i, j, k, None) not in mod_sets:
                        mod_sets[(i, j, k, None)] = {"X"}
                dihed_sets = mod_sets
        elif create_dihedra and len(coord) == 4:
            mod_sets = dihed_sets.copy()
            skey = tuple(sorted(coord))
            for (a, l, m, n),v in dihed_sets.items():
                key = None
                if m is None:
                    try:
                        ix = coord.index(a)
                    except:
                        continue
                    try:
                        jx = coord.index(l)
                    except:
                        continue
                    rem = np.setdiff1d([0, 1, 2, 3], [ix, jx])
                    key, z, perm = _get_dihedron_dihed_key_name(mod_sets, a, l, coord[rem[0]], coord[rem[1]], *coord)
                    v = _permute_dihed_data(v, perm)
                    mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                    if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals, coord)
                elif n is None:
                    try:
                        ix = coord.index(a)
                    except:
                        continue
                    try:
                        jx = coord.index(l)
                    except:
                        continue
                    try:
                        kx = coord.index(m)
                    except:
                        continue
                    rem = np.setdiff1d([0, 1, 2, 3], [ix, jx, kx])
                    key, z, perm = _get_dihedron_dihed_key_name(mod_sets, a, l, m, coord[rem[0]], *coord)
                    v = _permute_dihed_data(v, perm)
                    mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                    if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals, coord)
                elif skey == tuple(sorted([a, l, m, n])):
                    key, z, perm = _get_dihedron_dihed_key_name(mod_sets, a, l, m, n, *coord)
                    v = _permute_dihed_data(v, perm)
                    mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                    if validate: _validate_dihed_triangulation(mod_sets, key, base_internals + internals, coord)
            if key is not None and None not in key: update_ds.add(key)
            dihed_sets = mod_sets
        #
        # for (a, l, m, n),v in dihed_sets.items():
        #     if m is None and n is not None:
        #         raise ValueError(coord)

    if create_compound_dihedra:
        usets = {k:set(k) for k in update_ds}
        dsets = {k:set(k) for k in dihed_sets.keys() if None not in k}
        for k1,s1 in usets.items():
            for k2,s2 in dsets.items():
                inter = s1 & s2
                if len(inter) == 3:
                    u1 = list(s1 - inter)[0]
                    u2 = list(s2 - inter)[0]
                    # take all pairs from the intersection and include
                    # all apparent dihedrals
                    for a,b in itertools.combinations(inter, 2):
                        new = canonicalize_internal((u1,) + (a, b) + (u2,), check_invalid=False)
                        for p in itertools.permutations(new):
                            if p in dihed_sets:
                                new = p
                                break
                        # TODO: create composite dihedral elements by adding in coordinates
                        #      for any shared faces
                        d1 = dihed_sets[k1]
                        c1 = {s:tuple(k1[i] for i in nput.dihedron_property_specifiers(s)['coord']) for s in d1}
                        ds1 = {
                            c
                            for c in c1.values()
                            if all(i in new for i in c)
                        }
                        d2 = dihed_sets[k2]
                        c2 = {s: tuple(k2[i] for i in nput.dihedron_property_specifiers(s)['coord']) for s in d2}
                        ds2 = {
                            c
                            for c in c2.values()
                            if all(i in new for i in c)
                        }
                        ds = ds1 | ds2
                        idx = {
                            nput.dihedron_property_specifiers(
                                canonicalize_internal(tuple(new.index(i) for i in c), check_invalid=False)
                            )['name']
                            for c in ds
                        }
                        dihed_sets[new] = dihed_sets.get(new, set()) | idx
                        _check_dihed_coords(base_internals + internals, dihed_sets)

                        if add_dihedron_triangles:
                            tmap = ['a', 'b', 'c', 'A', 'B', 'C']
                            for idx, terms in [
                                [(0, 1, 2), ['a', 'b', 'x', 'A', 'B1', 'X']],
                                [(1, 2, 3), ['b', 'c', 'y', 'B2', 'C', 'Y']],
                                [(0, 1, 3), ['a', 'y', 'z', 'A3', 'Y3', 'Z']],
                                [(0, 2, 3), ['x', 'c', 'z', 'X4', 'C4', 'Z2']]
                            ]:
                                new_k = tuple(new[i] for i in idx)
                                face_terms = set()
                                for tv, nm in zip(tmap, terms):
                                    if nm in dihed_sets[new]:
                                        face_terms.add(tv)
                                found = False
                                for perm in itertools.permutations(range(3)):
                                    test_k = tuple(new_k[x] for x in perm)
                                    if test_k in tri_sets:
                                        new_k = test_k
                                        found = True
                                        break
                                else:
                                    new_k, s = canonicalize_internal(new_k, check_invalid=False, return_sign=True)
                                    if s < 0:
                                        perm = (2, 1, 0)
                                    else:
                                        perm = None
                                if found or nput.triangle_is_complete(nput.make_triangle(**{k:True for k in face_terms})):
                                    if perm is not None:
                                        face_terms = _permute_tri_data(face_terms, np.argsort(perm))
                                    tri_sets[new_k] = tri_sets.get(new_k, set()) | face_terms
                                    _check_tri_coords(base_internals + internals, tri_sets)

    if validate:
        for k in tri_sets:
            if not all(nput.is_int(i) or i is None for i in k):
                raise ValueError(f"triangle {k} malformed")
            if None not in k:
                for p in itertools.permutations(k):
                    if p != k and p in tri_sets:
                        raise ValueError(f"triangle {k} duped by {p}")
        for k in dihed_sets:
            if not all(nput.is_int(i) or i is None for i in k):
                raise ValueError(f"dihedron {k} malformed")
            if None not in k:
                for p in itertools.permutations(k):
                    if p != k and p in dihed_sets:
                        raise ValueError(f"dihedron {k} duped by {p}")



    if prune_incomplete:
        tri_sets, dihed_sets = (
                {k:v for k,v in tri_sets.items() if None not in k},
                # dihed_sets
                {k:v for k,v in dihed_sets.items() if None not in k}
            )
        if construct_shapes:
            _ = {}
            for k,s in tri_sets.items():
                vals = {}
                for a in s:
                    idx = nput.triangle_property_specifiers(a)["coord"]
                    vals[a] = tuple(k[i] for i in idx)
                _[k] = nput.make_triangle(**vals)
            tri_sets = _

            _ = {}
            for k,s in dihed_sets.items():
                vals = {}
                for a in s:
                    idx = nput.dihedron_property_specifiers(a)["coord"]
                    vals[a] = tuple(k[i] for i in idx)
                _[k] = nput.make_dihedron(**vals)
            dihed_sets = _

            if not allow_partially_defined:
                tri_sets = {
                    k: v
                    for k, v in tri_sets.items()
                    if nput.triangle_is_complete(v)
                }
                dihed_sets = {
                    k: v
                    for k, v in dihed_sets.items()
                    if nput.dihedron_is_complete(v)
                }
            if validate:
                _check_tri_coords(base_internals + internals, tri_sets)
                _check_dihed_coords(base_internals + internals, dihed_sets)
                for k,v in dihed_sets.items():
                    for i in range(4):
                        t = nput.dihedron_triangle(v, i)
                        if nput.triangle_is_complete(t):
                            inds = np.unique(
                                np.concatenate(
                                    [x for x in [t.a, t.b, t.c, t.A, t.B, t.C] if x is not None]
                                )
                            )
                            if all(p not in tri_sets for p in itertools.permutations(inds)):
                                raise ValueError(f"dihedron has triangle {inds}:{t} but triangulation didn't find it")
    return tri_sets, dihed_sets
def get_triangulation_internals(
    triangulation:tuple[dict[tuple[int, int, int], nput.TriangleData], dict[tuple[int, int, int, int], nput.DihedralTetrahedronData]]
):
    """
    **LLM Docstring**

    Extract the primitive distance, angle, and dihedral coordinates represented by triangle and dihedron triangulation records.

    :param triangulation: Optional precomputed triangle/dihedron representation.
    :type triangulation: tuple[dict[tuple[int, int, int], nput.TriangleData], dict[tuple[int, int, int, int], nput.DihedralTetrahedronData]]
    :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
    :rtype: Any
    """
    tri_sets, dihed_sets = triangulation
    return itut.delete_duplicates(
            v
            for tv in [tri_sets, dihed_sets]
            for t in tv.values()
            for v in t if v is not None
        )

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
    if cache is None:
        cache = {}
    target_set = frozenset(a for t in targets for a in t)
    if dev.str_in(intersection, 'partial'):
        subinternals = [i for i in internal_bag if any(ii in target_set for ii in i)]
    else:
        subinternals = [i for i in internal_bag if all(ii in target_set for ii in i)]
    key = (intersection, target_set)
    if key not in cache:
        cache[key] = {}
    subache = cache[key]
    n = len(subinternals)
    if n not in subache:
        if len(subache) == 0:
            tri = get_internal_triangles_and_dihedrons(subinternals, **kwargs)
        else:
            nearest = max(subache.keys())
            extra = subinternals[-(n-nearest):]
            cur, crds = subache[nearest]
            tri = get_internal_triangles_and_dihedrons(extra, base=cur, base_internals=crds, **kwargs)
        subache[n] = (tri, internal_bag)
    return subache[n][0]

def _merge_shapes(new_shapes, old_shapes, perms, perm_invs, prop_func,
                  in_place=False,
                  merge_strategy='both'):
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
    if not in_place:
        new_shapes = new_shapes.copy()
        old_shapes = old_shapes.copy()
    use_new = dev.str_in(merge_strategy, 'new')
    use_old = dev.str_in(merge_strategy, 'old')
    merge_inds_old = []
    merge_inds_new = []
    for k, t in new_shapes.items():
        for p, pi in zip(perms, perm_invs):
            k2 = tuple(k[i] for i in p)
            if k2 not in old_shapes:
                k2 = tuple(reversed(k2))
            if k2 in old_shapes:
                if use_new:
                    merge_inds_old.append(k2)
                    break
                elif use_old:
                    merge_inds_new.append(k)
                    break
                else:
                    uv = old_shapes[k2]
                    if k == k2:
                        d2 = t._asdict()
                    else:
                        d2 = {}
                        t_dict = {k: v for k, v in t._asdict().items() if v is not None}
                        for term, val in t_dict.items():
                            x = prop_func(term)["coord"]
                            y = canonicalize_internal([pi[i] for i in x], check_invalid=False)
                            d2[prop_func(y)["name"]] = val
                    uv_dict = uv._asdict()
                    requires_merge = False
                    for name,val in d2.items():
                        val2 = uv_dict[name]
                        if val != val2:
                            if not (
                                isinstance(val, tuple) and isinstance(val2, tuple)
                                and (
                                        canonicalize_internal(val, check_invalid=False)
                                        == canonicalize_internal(val2, check_invalid=False)
                                )
                            ):
                                requires_merge = True
                                break
                    if requires_merge:
                        d2 = dev.merge_dicts(uv_dict, d2, merge_iterables=False)
                        new_shapes[k] = uv._replace(**d2)
                        merge_inds_old.append(k2)
                    else:
                        merge_inds_new.append(k)
                break
    for k in merge_inds_new: del new_shapes[k]
    for k in merge_inds_old: del old_shapes[k]
    return new_shapes, old_shapes
def merge_dihedral_sets(sub_diheds, unmodified_diheds,
                        in_place=False,
                        merge_strategy='both'):
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
    return _merge_shapes(
        sub_diheds,
        unmodified_diheds,
        _dihedron_perms,
        _dihedron_perm_inv,
        nput.dihedron_property_specifiers,
        in_place=in_place,
        merge_strategy=merge_strategy
    )
def merge_triangle_sets(sub_tris, unmodified_tris,
                        in_place=False,
                        merge_strategy='both'):
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
    return _merge_shapes(
        sub_tris,
        unmodified_tris,
        _tri_perms,
        _tri_perm_inv,
        nput.triangle_property_specifiers,
        in_place=in_place,
        merge_strategy=merge_strategy
    )

def update_triangulation(
        triangulation: tuple[dict[tuple[int, int, int], nput.TriangleData], dict[tuple[int, int, int, int], nput.DihedralTetrahedronData]],
        added_internals,
        removed_internals,
        triangulation_internals=None,
        return_split=False,
        validate=False
):
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
    raise NotImplementedError("a little bit broken")
    if triangulation_internals is None:
        triangulation_internals = [canonicalize_internal(c, check_invalid=False) for c in get_triangulation_internals(triangulation)]
    added_internals = [canonicalize_internal(a) for a in added_internals]
    added_internals = [a for a in added_internals if a not in triangulation_internals and a not in removed_internals]
    removed_internals = [canonicalize_internal(r) for r in removed_internals]
    removed_internals = [r for r in removed_internals if r in triangulation_internals and r not in added_internals]

    mod_internals = added_internals + removed_internals
    test_internals = triangulation_internals + added_internals

    # test_dists = [i for i in test_internals if len(i) == 2]
    # test_angles = [i for i in test_internals if len(i) == 3]
    # test_dihedrals = [i for i in test_internals if len(i) == 4]

    # core_internals = []
    # core_atoms = set()
    # n_added = len(added_internals)
    # for d in test_dihedrals:
    #     # test intersection with any modified coordinates, has to intersect fully
    #     # to me included
    #     for n,t in enumerate(mod_internals):
    #         if all(i in d for i in t):
    #             if n < n_added:
    #                 core_internals.append(d)
    #             core_atoms.update(d)
    #             break
    #
    # for d in test_angles:
    #     # test intersection with any modified coordinates, has to intersect with
    #     # n-1 atoms to be included
    #     for n,t in enumerate(mod_internals):
    #         if len([i in d for i in t]) == len(t) - 1:
    #             if n < n_added: core_internals.append(d)
    #             core_atoms.update(d)
    #             core_atoms.update(t)
    #             break
    #
    # for d in test_dists:
    #     # test intersection with any modified coordinates, has to intersect with
    #     # any atom to be included
    #     for n,t in enumerate(mod_internals):
    #         if any(i in t for i in d):
    #             if n < n_added: core_internals.append(d)
    #             core_atoms.update(d)
    #             core_atoms.update(t)
    #             break
    #

    tri_set, dihed_set = triangulation

    mod_dists = {i:frozenset(i) for i in mod_internals if len(i) == 2}
    mod_angles = {i:frozenset(i) for i in mod_internals if len(i) == 3}
    mod_dihedrals = {i:frozenset(i) for i in mod_internals if len(i) == 4}
    core_atoms = {a for d in mod_internals for a in d}

    unmodified_tris = {}
    unmodified_diheds = {}
    check_internals = set()
    for k,v in tri_set.items():
        core_intersection = core_atoms & set(k)
        # we check if there is a complete intersection with
        # any of the "mod_internals"
        checks = []
        if len(core_intersection) >= 2:
            if len(mod_dists) > 0: checks.append([2, mod_dists])
        if len(core_intersection) >= 3:
            if len(mod_angles) > 0: checks.append([3, mod_angles])
        added = True
        for n,block in checks:
            for d,s in block.items():
                if len(s & core_intersection) == n:
                    # this triangle needs an update
                    # we store the internal for later checks
                    check_internals.add(d)
                    added = False
        if added:
            unmodified_tris[k] = v
    for k,v in dihed_set.items():
        core_intersection = core_atoms & set(k)
        checks = []
        if len(core_intersection) >= 2:
            if len(mod_dists) > 0: checks.append([2, mod_dists])
        if len(core_intersection) >= 3:
            if len(mod_angles) > 0: checks.append([3, mod_angles])
        if len(core_intersection) == 4:
            if len(mod_dihedrals) > 0: checks.append([4, mod_dihedrals])
        added = True
        for n,block in checks:
            for d, s in block.items():
                if len(s & core_intersection) == n:
                    # this triangle needs an update
                    # we store the internal for later checks
                    check_internals.add(d)
                    for e in v:
                        if isinstance(e, tuple): check_internals.add(e)
                    added = False
        if added:
            unmodified_diheds[k] = v

    removed_internals = set(removed_internals)
    check_internals = check_internals - removed_internals
    core_internals = []
    test_internals_map = {i:frozenset(i) for i in test_internals}
    for t,s in test_internals_map.items():
        if (
            t in check_internals
            or (
                len(core_atoms & s) >= len(s) - 1
                and t not in removed_internals
        )):
            core_internals.append(t)

    second_shell_atoms = {a for d in core_internals for a in d}
    for t,s in test_internals_map.items():
        if (
            len(second_shell_atoms & s) >= len(s) - 1
            and t not in removed_internals
            and t not in core_internals
        ):
            core_internals.append(t)

    sub_tris, sub_diheds = get_internal_triangles_and_dihedrons(core_internals)
    # for each of these terms, we now need to add in anything
    # that would have been in there but didn't survive the pruning step
    tri_keys_map = {k:frozenset(k) for k in sub_tris.keys()}
    for k,s1 in tri_keys_map.items():
        mods = {}
        for t,s2 in test_internals_map.items():
            if len(s1 & s2) == len(s2):
                # included, just need to figure out which key
                key = tuple(k.index(i) for i in t)
                if key[-1] < key[0]:
                    key = tuple(reversed(key))
                name = nput.triangle_property_specifiers(key)['name']
                mods[name] = t
        if len(mods) > 0:
            sub_tris[k] = sub_tris[k]._replace(**mods)
    dihed_keys_map = {k:frozenset(k) for k in sub_diheds.keys()}
    for k,s1 in dihed_keys_map.items():
        mods = {}
        for t,s2 in test_internals_map.items():
            if len(s1 & s2) == len(s2):
                # included, just need to figure out which key
                key = tuple(k.index(i) for i in t)
                if key[-1] < key[0]:
                    key = tuple(reversed(key))
                name = nput.dihedron_property_specifiers(key)['name']
                mods[name] = t
        if len(mods) > 0:
            sub_diheds[k] = sub_diheds[k]._replace(**mods)

    # print(len(sub_tris), len(unmodified_tris), len([x for x in unmodified_tris.values() if nput.triangle_is_complete(x)]))
    merge_triangle_sets(sub_tris, unmodified_tris, in_place=True, merge_strategy='old')
    merge_dihedral_sets(sub_diheds, unmodified_diheds, in_place=True, merge_strategy='old')
    # print(len(sub_tris), len(unmodified_tris), len([x for x in unmodified_tris.values() if nput.triangle_is_complete(x)]))

    if validate:
        test_internals = [t for t in test_internals if t not in removed_internals]
        missing = [c for c in core_internals if c not in test_internals]
        if len(missing) > 0:
            raise ValueError("???", missing)

        for (sub, unmod) in [
            [sub_tris, unmodified_tris],
            [sub_diheds, unmodified_diheds],
        ]:
            for k,t in sub.items():
                if k in unmod:
                    raise ValueError(f"duplicated {k}")
                for n,k2 in enumerate(itertools.permutations(k)):
                    if n > 0:
                        if k2 in sub:
                            raise ValueError(f"duplicated in retriangulation {k}, {k2}")
                        elif k2 in unmod:
                            raise ValueError(f"duplicated in leftovers {k}, {k2}")

        test_tris, test_diheds = get_internal_triangles_and_dihedrons(test_internals)
        tri_set = {
            k: v
            for ts in [sub_tris, unmodified_tris]
            for k, v in ts.items()
        }
        dihed_set = {
            k: v
            for ts in [sub_diheds, unmodified_diheds]
            for k, v in ts.items()
        }
        for t1,v1 in test_tris.items():
            if all(p not in tri_set for p in itertools.permutations(t1)):
                print("=1=>", t1)
                import pprint
                print(v1)
                pprint.pprint(test_internals)
                pprint.pprint(core_internals)
                pprint.pprint(mod_internals)
                pprint.pprint(core_atoms)
                raise ValueError(f"{t1} from default triangles not in retriangulation")
        for d1,v1 in test_diheds.items():
            if all(p not in dihed_set for p in itertools.permutations(d1)):
                print("=1=>", d1)
                import pprint
                print(v1)
                pprint.pprint(test_internals)
                pprint.pprint(core_internals)
                pprint.pprint(mod_internals)
                pprint.pprint(core_atoms)
                raise ValueError(f"{d1} from default dihedrals not in retriangulation")
        for t1,v1 in tri_set.items():
            if all(p not in test_tris for p in itertools.permutations(t1)):
                print("=2=>", t1)
                import pprint
                import pprint
                print(v1)
                pprint.pprint(test_internals)
                pprint.pprint(core_internals)
                pprint.pprint(mod_internals)
                pprint.pprint(core_atoms)
                if t1 in sub_tris:
                    raise ValueError(f"{t1} from retriangulation not in default triangles")
                else:
                    raise ValueError(f"{t1} from leftovers not in default triangles")
        for d1,v1 in dihed_set.items():
            if all(p not in test_diheds for p in itertools.permutations(d1)):
                print("=2=>", d1)
                import pprint
                print(v1)
                pprint.pprint(test_internals)
                pprint.pprint(core_internals)
                pprint.pprint(mod_internals)
                pprint.pprint(core_atoms)
                if d1 in sub_tris:
                    raise ValueError(f"{d1} from retriangulation not in default dihedrals")
                else:
                    raise ValueError(f"{d1} from leftovers not in default dihedrals")


    if return_split:
        return core_atoms, (sub_tris, sub_diheds), (unmodified_tris, unmodified_diheds)
    else:
        tri_set = {
            k:v
            for ts in [sub_tris, unmodified_tris]
            for k, v in ts.items()
        }
        dihed_set = {
            k:v
            for ts in [sub_diheds, unmodified_diheds]
            for k, v in ts.items()
        }

        return tri_set, dihed_set

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
    idx = []
    for i in coord:
        try:
            ix = inds.index(i)
        except:
            return None
        else:
            idx.append(ix)
    b = canonicalize_internal(idx)
    target = nput.triangle_property_specifiers(b)
    return nput.triangle_property_function(tri, target['name'], raise_on_missing=False)
def _dihedral_conversion_function(inds, dihed, coord, allow_completion=True, cache=None, completion_handler=None,
                                  disallowed_conversions=None, allow_ambiguous_completions=False, verbose=False):
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
    idx = []
    for i in coord:
        try:
            ix = inds.index(i)
        except:
            return None
        else:
            idx.append(ix)
    b = canonicalize_internal(idx)
    return nput.dihedron_property_function(dihed, b,
                                           allow_completion=allow_completion,
                                           allow_ambiguous_completions=allow_ambiguous_completions,
                                           raise_on_missing=False,
                                           completion_handler=completion_handler,
                                           disallowed_conversions=disallowed_conversions,
                                           cache=cache,
                                           verbose=verbose)
def _pair_dihedral_conversion_function(inds1, dihed1, inds2, dihed2, coord,
                                       raise_on_invalid=True,
                                       cache=None):
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
    # to get (3, 1, 2, 4), given (0, 1, 2, 3) and (0, 1, 2, 4)
    # I need (0, 1, 2, 3) - (0, 1, 2, 4)
    # so I find the three overlap positions between `inds1` and `inds2` and then
    # I find a pair of dihedrals in `dihed1` and `dihed2` over the shared face that
    # can together give coord
    shared, sorting, _, pos1, pos2 = nput.intersection(inds1, inds2, return_indices=True)
    diff_pos = np.setdiff1d(coord, shared)
    if (
            (diff_pos[0], diff_pos[1]) != (coord[0], coord[3])
            and (diff_pos[1], diff_pos[0]) != (coord[0], coord[3])
    ):
        if raise_on_invalid:
            raise ValueError(f"can't build dihedral for {coord} from {inds1} and {inds2}")
        else:
            return None, None
    # now sort `pos1` and `pos2` so the middle atoms are the bond
    pos1 = sorted(pos1, key=lambda x:inds1[x] in coord)
    if inds1[pos1[2]] == coord[1]:
        pos1 = [pos1[0], pos1[2], pos1[1]]

    pos2 = sorted(pos2, key=lambda x:inds2[x] in coord)
    if inds2[pos2[2]] == coord[1]:
        pos2 = [pos2[0], pos2[2], pos2[1]]

    if coord[0] in inds2:
        pos1, dihed1, pos2, dihed2 = pos2, dihed2, pos1, dihed1

    idx1 = pos1 # canonicalize_internal(pos1, check_invalid=False)
    idx2 = pos2 #canonicalize_internal(pos2, check_invalid=False)
    # print(inds1, inds2)
    # print(pos1, pos2)
    # rem_pos = np.setdiff1d(pos1, 3)
    # raise Exception('ooo')
    # idx1 = []
    # for i in coord:
    #     try:
    #         ix = inds1.index(i)
    #     except ValueError:
    #         continue
    #     else:
    #         idx1.append(ix)
    # idx2 = []
    # for i in coord:
    #     try:
    #         ix = inds2.index(i)
    #     except ValueError:
    #         continue
    #     else:
    #         idx2.append(ix)
    # idx1 = canonicalize_internal(idx1)
    # idx2 = canonicalize_internal(idx2)
    rem1 = np.setdiff1d(np.arange(4), idx1)
    rem2 = np.setdiff1d(np.arange(4), idx2)
    # print(dihed1)
    # print(dihed2)
    # print("dd", coord, np.array(idx1), np.array(idx2),
    #       tuple(inds1[i] for i in np.concatenate([idx1, rem1])),
    #       tuple(inds2[i] for i in np.concatenate([idx2, rem2]))
    #       )
    conv = nput.dihedron_pair_dihedral_angle_function(
        idx1, dihed1,
        idx2, dihed2,
        raise_on_missing=False,
        cache=cache
    )
    return (dihed1, dihed2), conv

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
        self.caller = caller
        if name is None:
            name = self.caller.__name__
        self.__name__ = name
        self.provenance = provenance
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
        try:
            return self.caller(internals, **opts)
        except:
            ints = np.asanyarray(internals)
            raise ValueError(f"caller error in calling {self} on internals of shape {ints.shape}")
    def __repr__(self):
        """
        **LLM Docstring**

        Format the conversion using its assigned name and provenance description.

        :return: A concise representation of the object.
        :rtype: str
        """
        return f"{type(self).__name__}<{self.__name__}>"

int_conv_data = collections.namedtuple("int_conv_data",
                                      ['input_indices', 'pregen_indices', 'conversion'])
def find_internal_conversion(internals, targets,
                             triangles_and_dihedrons=None,
                             # prior_coords=None,
                             canonicalize=True,
                             allow_completion=True,
                             return_conversions=False,
                             prep_conversions=True,
                             include_shapes=False,
                             indices=None,
                             cache=None,
                             disallowed_conversions=None,
                             update_triangles_and_dihedrons=False,
                             return_completions=False,
                             allow_recursive_completions=None,
                             allow_ambiguous_completions=False,
                             dihedral_intersections=None,
                             index_mapping=None,
                             verbose=False,
                             missing_val='raise'):
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
    smol = nput.is_int(targets[0])
    if smol: targets = [targets]
    if triangles_and_dihedrons is None:
        if isinstance(internals, RADInternalCoordinateSet):
            triangles_and_dihedrons = internals.triangulation
            internals = internals.specs
        else:
            if canonicalize:
                internals = [canonicalize_internal(c) for c in internals]
            triangles_and_dihedrons = get_internal_triangles_and_dihedrons(internals, canonicalize=False)
    if callable(triangles_and_dihedrons):
        triangles, dihedrals = triangles_and_dihedrons(internals, targets)
    else:
        triangles, dihedrals = triangles_and_dihedrons
    conversions = []
    shapes = []
    if cache is None:
        cache = {}
    idx_data = nput.dihedron_property_specifiers()
    convertable = True
    conversion_mapping = {}
    extra_coordinates = {}
    if allow_recursive_completions is None:
        allow_recursive_completions = allow_completion
    # completable_dihedrons = {}
    dihedral_sets = {k:set(k) for k in dihedrals.keys()}
    if dihedral_intersections is None:
        base_intersections = {
            k:{
                b:len(dihedral_sets[k] & dihedral_sets[b])
                for b in dihedrals.keys()
            }
            for k in dihedrals.keys()
        }
        pruned_intersections = {
            k:{b:v for b,v in di.items() if v > 2}
            for k,di in base_intersections.items()
        }
        dihedral_intersections = (base_intersections, pruned_intersections)
    dihedral_intersections, pruned_dihedral_intersections = dihedral_intersections
    for target_coord in targets:
        if verbose: print("======>", target_coord)
        if canonicalize:
            target_coord = canonicalize_internal(target_coord)
        idx = find_internal(internals, target_coord, missing_val=None, canonicalize=False, indices=indices)
        if verbose: print("  idx:", idx)
        conv = None
        tri = None
        dihed = None
        shape = None

        if idx is None:
            n = len(target_coord)
            ts = set(target_coord)
            if n < 2 or n > 4:
                raise ValueError(f"can't understand coordinate {target_coord}")
            if n in {2, 3}:
                for a, v in triangles.items():
                    tri = v
                    conv = _triangle_conversion_function(a, v, target_coord)
                    if conv is not None:
                        break
                    else:
                        tri = None

            if verbose: print("  tri:", tri)

            if conv is None and (
                    n in {2, 3}
                    or allow_ambiguous_completions
            ):
                if allow_ambiguous_completions:
                    raise ValueError("!")
                for a, v in dihedrals.items():
                    dihed = v
                    completion_handler = None
                    conv = _dihedral_conversion_function(a, v, target_coord, allow_completion=allow_completion,
                                                         cache=cache, completion_handler=completion_handler,
                                                         allow_ambiguous_completions=allow_ambiguous_completions,
                                                         disallowed_conversions=disallowed_conversions,
                                                         verbose=verbose)
                    if conv is not None:
                        break
                    else:
                        dihed = None

            if conv is None and n == 4:
                # we search for a pair of dihedrals we can complete
                # to get (i,j,k,l) we need (i,j,k,a) and (b,j,k,l)
                for a, v in dihedrals.items():
                    if len(dihedral_sets[a] & ts) == 3:
                        for b, l2 in pruned_dihedral_intersections[a].items():
                            if (
                                    b in dihedral_sets
                                    and len(dihedral_sets[b] & ts) == 3
                                    and len((dihedral_sets[b] | dihedral_sets[a]) & ts) == 4
                            ):
                                v2 = dihedrals[b]
                                s, conv = _pair_dihedral_conversion_function(a, v, b, v2, target_coord,
                                                                             raise_on_invalid=False,
                                                                             cache=cache)
                                if conv is not None:
                                    shape = s
                                    break
                        if conv is not None:
                            break

            if conv is None and allow_recursive_completions:
                for a, v in dihedrals.items():
                    dihed = v
                    completion_handler = None
                    if all(t in a for t in target_coord):
                        dihedrals = dihedrals.copy()
                        triangles = triangles.copy()
                        def completion_handler(
                                og_dihed, k,
                                *,
                                disallowed_conversions,
                                allow_completion,
                                raise_on_missing,
                                return_depth,
                                cache,
                                depth=0,
                                key=a,
                                base=v
                        ):
                            """
                            **LLM Docstring**

                            Record a newly completed intermediate coordinate and its conversion so later target conversions can reuse it.

                            :param og_dihed: Original dihedron record from which the recursive completion search began.
                            :type og_dihed: Any
                            :param k: Third local vertex or candidate dihedron key.
                            :type k: Any
                            :param disallowed_conversions: Coordinate conversions that must not be used while searching for a target conversion.
                            :type disallowed_conversions: Any
                            :param allow_completion: Whether missing intermediate coordinates may be reconstructed.
                            :type allow_completion: Any
                            :param raise_on_missing: Whether a failed recursive completion raises rather than returning the configured missing value.
                            :type raise_on_missing: Any
                            :param return_depth: Whether the recursion depth used to find a completion is included in the result.
                            :type return_depth: Any
                            :param cache: Optional mutable cache of triangulation or conversion results.
                            :type cache: Any
                            :param depth: Current recursive search depth.
                            :type depth: Any
                            :param key: Triangulation record key being validated.
                            :type key: Any
                            :param base: Existing triangulation data used as the starting point for adding new coordinates.
                            :type base: Any
                            :return: The value or updated object described above.
                            :rtype: Any
                            """
                            if allow_completion is True:
                                allow_completion = 2
                            oc = tuple(key[x] for x in idx_data[k]['coord'])
                            # print("=="*100)
                            # print(">", oc, k)
                            conv, (t2, d2) = find_internal_conversion(
                                internals, [oc],
                                triangles_and_dihedrons=triangles_and_dihedrons,
                                # prior_coords=None,
                                canonicalize=True,
                                allow_completion=allow_completion,
                                return_conversions=True,
                                prep_conversions=prep_conversions,
                                include_shapes=False,
                                indices=indices,
                                cache=cache,
                                missing_val=None,
                                disallowed_conversions=disallowed_conversions,
                                update_triangles_and_dihedrons=True
                            )
                            conv = conv[0]
                            if conv is None: return None
                            triangles.update(t2)
                            dihedrals.update(d2)
                            dihedrals[key] = base._replace(**{idx_data[k]['name']:conv})
                            extra_coordinates[key] = conv
                            if return_depth:
                                return depth + 1, conv
                            else:
                                return conv
                    conv = _dihedral_conversion_function(a, v, target_coord, allow_completion=allow_completion,
                                                         cache=cache, completion_handler=completion_handler,
                                                         disallowed_conversions=disallowed_conversions)
                    if conv is not None:
                        break
                    else:
                        dihed = None

            if verbose: print("dihed:", dihed)
        else:
            conv = f'item_{idx}'

        if verbose: print(" conv:", conv.__name__ if hasattr(conv, '__name__') else conv)
        if conv is None:
            if dev.str_is(missing_val, "raise"):
                raise ValueError(f"can't find conversion for {target_coord} from {internals}")
            else:
                convertable = False
                conversions.append(missing_val)
                if include_shapes: shapes.append(None)
        else:
            # prep conversion based on internal indices
            if idx is not None:
                if prep_conversions:
                    def select_internal_index(internal_list, idx=idx):
                        """
                        **LLM Docstring**

                        Resolve a triangulation term to the corresponding source-internal or completed-coordinate index, including orientation sign where required.

                        :param internal_list: Working list of source and completed internal coordinates used during recursive conversion search.
                        :type internal_list: Any
                        :param idx: Index of the coordinate or conversion entry selected from the working list.
                        :type idx: Any
                        :return: The value or updated object described above.
                        :rtype: Any
                        """
                        internal_list = np.asanyarray(internal_list)
                        if index_mapping is not None:
                            subconv = index_mapping[idx]
                        else:
                            subconv = None
                        if subconv is None:
                            return internal_list[..., idx]
                        else:
                            return subconv(internal_list)
                    convert = InternalCoordinateConversion(
                        select_internal_index,
                        idx,
                        name=conv
                    )
                    # convert.__name__ = conv
                else:
                    convert = True
                if include_shapes: shapes.append(idx)
            elif tri is not None:
                if prep_conversions:
                    args = {
                        k: find_internal(internals, v, missing_val=missing_val, indices=indices)
                            for k, v in tri._asdict().items()
                        if v is not None
                    }
                    if any(v is None for k,v in args.items()):
                        print(internals)
                        print({
                            k: v
                            for k, v in tri._asdict().items()
                            if v is not None
                        })
                        raise ValueError(args)
                    args = {k:v for k,v in args.items() if v is not None}
                    def convert(internal_list, args=args, conv=conv,  **kwargs):
                        """
                        **LLM Docstring**

                        Evaluate the selected direct, triangle, dihedron, paired-dihedron, or completion-based conversion and place the results in target-coordinate order.

                        :param internal_list: Working list of source and completed internal coordinates used during recursive conversion search.
                        :type internal_list: Any
                        :param args: Additional positional values captured by the nested conversion wrapper.
                        :type args: Any
                        :param conv: Conversion specification to wrap.
                        :type conv: Any
                        :param kwargs: Additional options forwarded to the triangulation reduction or merge routine.
                        :type kwargs: Any
                        :return: The value or updated object described above.
                        :rtype: Any
                        """
                        internal_list = np.asanyarray(internal_list)
                        subargs = {}
                        for k, idx in args.items():
                            if not nput.is_int(idx):
                                idx = idx[0]
                            if index_mapping is not None:
                                subconv = index_mapping[idx]
                            else:
                                subconv = None
                            if subconv is None:
                                subargs[k] = internal_list[..., idx]
                            else:
                                subargs[k] = subconv(internal_list)
                        subtri = nput.make_triangle(**subargs)
                        return conv(subtri)
                    convert = InternalCoordinateConversion(
                        convert,
                        tri,
                        name='convert_' + conv.__name__
                    )
                else:
                    convert = True
                if include_shapes: shapes.append(tri)
            elif dihed is not None:
                if prep_conversions:
                    args = {
                        k:(
                            find_internal(internals, v, allow_negation=True, missing_val=missing_val, indices=indices)
                                if not callable(v) else
                            v #TODO: make this work properly
                        )
                            for k,v in dihed._asdict().items()
                        if v is not None
                    }
                    def convert(internal_list, args=args, conv=conv, **kwargs):
                        """
                        **LLM Docstring**

                        Evaluate the selected direct, triangle, dihedron, paired-dihedron, or completion-based conversion and place the results in target-coordinate order.

                        :param internal_list: Working list of source and completed internal coordinates used during recursive conversion search.
                        :type internal_list: Any
                        :param args: Additional positional values captured by the nested conversion wrapper.
                        :type args: Any
                        :param conv: Conversion specification to wrap.
                        :type conv: Any
                        :param kwargs: Additional options forwarded to the triangulation reduction or merge routine.
                        :type kwargs: Any
                        :return: The value or updated object described above.
                        :rtype: Any
                        """
                        internal_list = np.asanyarray(internal_list)
                        subargs = {}
                        for k,(idx,s) in args.items():
                            if index_mapping is not None:
                                subconv = index_mapping[idx]
                            else:
                                subconv = None
                            if subconv is None:
                                subargs[k] = internal_list[..., idx]
                            else:
                                subargs[k] = subconv(internal_list)
                        subdihed = nput.make_dihedron(**subargs)
                        return conv(subdihed)
                    convert = InternalCoordinateConversion(
                        convert,
                        dihed,
                        name='convert_' + conv.__name__
                    )
                else:
                    convert = True
                if include_shapes: shapes.append(dihed)
            else:
                if shape is None:
                    raise ValueError(f"don't know how to prep conversion without supplied shape")
                #TODO: support other shapes if necessary
                if prep_conversions:
                    dihed1, dihed2 = shape
                    args1 = {
                        k: (
                            find_internal(internals, v, allow_negation=True, missing_val=missing_val, indices=indices)
                            if not callable(v) else
                            v  # TODO: make this work properly
                        )
                            for k, v in dihed1._asdict().items()
                        if v is not None
                    }
                    args2 = {
                        k: (
                            find_internal(internals, v, allow_negation=True, missing_val=missing_val, indices=indices)
                                if not callable(v) else
                            v  # TODO: make this work properly
                        )
                            for k, v in dihed2._asdict().items()
                        if v is not None
                    }
                    def convert(internal_list, args1=args1, args2=args2, conv=conv, **kwargs):
                        """
                        **LLM Docstring**

                        Evaluate the selected direct, triangle, dihedron, paired-dihedron, or completion-based conversion and place the results in target-coordinate order.

                        :param internal_list: Working list of source and completed internal coordinates used during recursive conversion search.
                        :type internal_list: Any
                        :param args: Additional positional values captured by the nested conversion wrapper.
                        :type args: Any
                        :param conv: Conversion specification to wrap.
                        :type conv: Any
                        :param kwargs: Additional options forwarded to the triangulation reduction or merge routine.
                        :type kwargs: Any
                        :return: The value or updated object described above.
                        :rtype: Any
                        """
                        internal_list = np.asanyarray(internal_list)
                        subargs1 = {}
                        for k, (idx, s) in args1.items():
                            if index_mapping is not None:
                                subconv = index_mapping[idx]
                            else:
                                subconv = None
                            if subconv is None:
                                subargs1[k] = internal_list[..., idx]
                            else:
                                subargs1[k] = subconv(internal_list)
                        subdihed1 = nput.make_dihedron(**subargs1)
                        subargs2 = {}
                        for k, (idx, s) in args2.items():
                            if index_mapping is not None:
                                subconv = index_mapping[idx]
                            else:
                                subconv = None
                            if subconv is None:
                                subargs2[k] = internal_list[..., idx]
                            else:
                                subargs2[k] = subconv(internal_list)
                        subdihed2 = nput.make_dihedron(**subargs2)
                        return conv(subdihed1, subdihed2)
                    convert = InternalCoordinateConversion(
                        convert,
                        shape,
                        name='convert_' + conv.__name__
                    )
                else:
                    convert = True
                if include_shapes: shapes.append(shape)
            conversions.append(convert)

            if update_triangles_and_dihedrons:
                conversion_mapping[target_coord] = convert
                triangles, dihedrals = get_internal_triangles_and_dihedrons(
                    internals + [target_coord]
                )
                # tris, diheds = update_triangulation(
                #     triangles_and_dihedrons,
                #     [target_coord],
                #     [],
                #     triangulation_internals=internals
                # )

    if smol:
        convert = conversions[0]
        if include_shapes:
            shapes = shapes[0]
    else:
        if return_conversions or not convertable:
            convert = conversions
        else:
            def convert(internal_spec, order=None, conversions=conversions, **kwargs):
                """
                **LLM Docstring**

                Evaluate the selected direct, triangle, dihedron, paired-dihedron, or completion-based conversion and place the results in target-coordinate order.

                :param internal_list: Working list of source and completed internal coordinates used during recursive conversion search.
                :type internal_list: Any
                :param args: Additional positional values captured by the nested conversion wrapper.
                :type args: Any
                :param conv: Conversion specification to wrap.
                :type conv: Any
                :param kwargs: Additional options forwarded to the triangulation reduction or merge routine.
                :type kwargs: Any
                :return: The value or updated object described above.
                :rtype: Any
                """
                convs = [
                    c(internal_spec)
                    for c in conversions
                ]
                if order is None:
                    return np.moveaxis(np.array(convs), 0, -1)
                else:
                    return [
                        np.moveaxis(np.array([c[i] for c in convs]), 0, -1)
                        for i in range(order + 1)
                    ]

    res = (convert,)
    if include_shapes:
        res = res + (shapes,)
    if update_triangles_and_dihedrons:
        res = res + ((triangles, dihedrals),)
    if return_completions:
        res = res + (extra_coordinates,)
    if len(res) == 1:
        res = res[0]
    return res
def _enumerate_dists(internals):
    """
    **LLM Docstring**

    Return the canonical set of explicit distance pairs present in an internal-coordinate list.

    :param internals: Available internal-coordinate specifications or their numerical values.
    :type internals: Any
    :return: An iterator yielding the candidates described above.
    :rtype: Iterator
    """
    for coord in internals:
        for c in itertools.combinations(coord, 2):
            yield canonicalize_internal(c)

_dihed_check_sets = []
def _get_dihedron_checks():
    """
    **LLM Docstring**

    Return cached atom-position combinations used to test whether a tetrahedron can attach a new atom to an existing Z-matrix tree.

    :return: The value or updated object described above.
    :rtype: Any
    """
    if len(_dihed_check_sets) == 0:
        base = ('Tb', 'a', 'b', 'c', 'X', 'Y')
        for p in itertools.permutations([0, 1, 2, 3]):
            perm = np.argsort(p)
            new = []
            for t in base:
                x = nput.dihedron_property_specifiers(t)["coord"]
                y = canonicalize_internal([perm[i] for i in x])
                new.append(nput.dihedron_property_specifiers(y)["index"])
            _dihed_check_sets.append([perm, new])
    return _dihed_check_sets

_dihedron_index_props = {}
def _get_dihedron_index_props():
    """
    **LLM Docstring**

    Return cached lookup data describing the root, attachment, and new-atom positions for each dihedron attachment permutation.

    :return: The value or updated object described above.
    :rtype: Any
    """
    if len(_dihedron_index_props) == 0:
        for k,v in nput.dihedron_property_specifiers().items():
            _dihedron_index_props[v["coord"]] = v
    return _dihedron_index_props

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
    if nput.dihedron_is_complete(dihed_data):
        return True
    else:
        dips = _get_dihedron_index_props()
        extra_completions = {}
        for m in [2, 3]:
            for p in itertools.combinations(range(4), m):
                a = tuple(k[i] for i in p)
                if all(b in known_atom_graph for b in a):
                    n = dips[p]["index"]
                    if dihed_data[n] is None:
                        extra_completions[dips[p]["name"]] = a
        dihed_data = dihed_data._replace(**extra_completions)
        for p in nput.enumerate_dihedron_completions(dihed_data):
            if len(p) <= max_comps:
                target_coords = [
                    nput.dihedron_property_specifiers(pp)["coord"]
                    for pp in p
                ]
                target_coords = [[k[i] for i in c] for c in target_coords]
                if all(
                    all(i in known_atom_graph.get(c[0], ()) for i in c[1:])
                    for c in target_coords
                ):
                    return True
        return False

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
    dihed_choices = []
    dihed_props = d_prop_cache[0]
    if dihed_props is None:
        idx_props = _get_dihedron_index_props()
        dihed_props = [
            (p, v) for p, v in idx_props.items()
            if (
                    len(v['coord']) == 4
                # and d[v['index']] is not None
            )
        ]
        d_prop_cache[0] = dihed_props
    for k, d in dihedral_set.items():
        if a in k:
            for p, v in dihed_props:
                if not check_complete or d[v['index']] is not None:
                    if (a == k[p[0]] or a == k[p[-1]]):
                        k = tuple(k[i] for i in p)
                        if k not in internals:
                            x, y, z, w = k
                            k2 = (x, z, y, w)
                            if k2 in internals:
                                k = k2
                        if a == k[-1]: k = tuple(reversed(k))
                        dihed_choices.append(k)
    return dihed_choices
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
    combs = list(itertools.combinations(atoms, 3))
    combs = combs[:1] + sorted(combs[1:],
                               key=lambda x: np.max([len(connectivity_graph[k]) for k in x]),
                               reverse=True)
    for p in combs:
        proper_tri = None
        for pp in itertools.permutations(p):
            proper_tri = tris.get(pp)
            if proper_tri is not None:
                proper_tri = pp, proper_tri
                break
        if proper_tri is not None:
            (i, j, k), proper_tri = proper_tri
            # order groups by minimal completions to make a Z-matrix
            groups = {
                (i, j, k): [proper_tri.a, proper_tri.b, proper_tri.C],
                (j, i, k): [proper_tri.a, proper_tri.c, proper_tri.B],
                (i, k, j): [proper_tri.c, proper_tri.b, proper_tri.A]
            }
            groups = sorted(groups.keys(), key=lambda k: len([a for a in groups[k] if a is not None]))
            groups = sum((
                [
                    p for p in
                    [(i, j, k), (k, j, i)]
                    # both versions work,
                    # but one might be more complete-able than the other?
                ]
                for (i, j, k) in groups
            ),
                []
            )
            groups = [
                g for g in groups
                if (
                        len(connectivity_graph[g[-1]]) > 4
                        or len(connectivity_graph[g[-1]]) == len(atoms) - 1
                )
            ] # if only 4 we can't actually connect to anything else
            yield groups
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
    #TODO: support passing t2 and d2 directly
    t2 = {k:t for k,t in tris.items() if nput.triangle_is_complete(t)}
    d2 = {k:d for k,d in dihedrons.items() if nput.dihedron_is_complete(d)}
    known_atom_graph = {}
    for k in t2.keys():
        k = list(k)
        for n,a in enumerate(k):
            if a not in known_atom_graph:
                known_atom_graph[a] = set()
            for b in k[n+1:]:
                # if b == a: raise ValueError(k)
                known_atom_graph[a].add(b)
                if b not in known_atom_graph:
                    known_atom_graph[b] = set()
                known_atom_graph[b].add(a)

    tups = [set(k) for k, _ in d2.items()]
    for i, k in enumerate(tups):
        for a in k:
            if a not in known_atom_graph:
                known_atom_graph[a] = set()
            for b in k - {a}:
                # if b == a: raise ValueError(k)
                known_atom_graph[a].add(b)
                if b not in known_atom_graph:
                    known_atom_graph[b] = set()
                known_atom_graph[b].add(a)
        for j, k2 in enumerate(tups[i + 1:]):
            if len(k & k2) == 3: # i,j,k shared implies remaining two are connected
                for a in k:
                    if a not in known_atom_graph:
                        known_atom_graph[a] = set()
                    for b in k2 - {a}:
                        # if b == a: raise ValueError(k2)
                        known_atom_graph[a].add(b)
                        if b not in known_atom_graph:
                            known_atom_graph[b] = set()
                        known_atom_graph[b].add(a)
    complete_dihedrals = {}
    for k in internals:
        if len(k) == 4:
            for p in itertools.permutations(k):
                if p in d2:
                    # TODO: is this sufficient for completability?
                    complete_dihedrals[p] = d2[p]
                    for n,a in enumerate(k):
                        if a not in known_atom_graph:
                            known_atom_graph[a] = set()
                        for b in k[n+1:]:
                            if b not in known_atom_graph:
                                known_atom_graph[b] = set()
                            known_atom_graph[a].add(b)
                            known_atom_graph[b].add(a)
                    break
                elif p in dihedrons: # not definitely completable until we add in prior knowledge
                    d = dihedrons[p]
                    if _dihedron_completable(p, d, known_atom_graph):
                        complete_dihedrals[p] = d
                        # d2[p] = d
                        for n, a in enumerate(k):
                            if a not in known_atom_graph:
                                known_atom_graph[a] = set()
                            for b in k[n + 1:]:
                                if b not in known_atom_graph:
                                    known_atom_graph[b] = set()
                                known_atom_graph[a].add(b)
                                known_atom_graph[b].add(a)
                        break
            else:
                raise ValueError(f"can't complete {k}")

    return known_atom_graph, complete_dihedrals
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
    idx_data = cached_data[0]
    if idx_data is None:
        idx_data = nput.dihedron_property_specifiers()
        cached_data[0] = idx_data
    cache = {}
    # print(k, dihed_data)
    # print(choice, known_atoms)
    # print(list(itut.delete_duplicates(tuple(sorted(x)) for x in nput.enumerate_dihedron_completions(dihed_data))))
    for comp in nput.enumerate_dihedron_completions(dihed_data):
        for a in comp:
            if a not in cache:
                # print(a, [k[v] for v in idx_data[a]['coord']])
                cache[a] = all(k[v] in known_atoms for v in idx_data[a]['coord'])
            if not cache[a]:
                break
        else:
            # possible to complete this term
            return True
    return False
def _grow_dihedral_trees(root, atoms,
                         top_dihedral_choices,
                         secondary_dihedral_choices,
                         incomplete_dihedrals=None,
                         internals=None,
                         *, traversal='dfs'):
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
    #TODO: consider caching these for a given root ordering...
    visited = frozenset(root)
    queue = collections.deque([
        [visited, [], list(atoms)],
    ])
    if dev.str_is(traversal, 'bfs'):
        raise NotImplementedError("bfs with counting is tricky")
        pop = queue.popleft
        extend = queue.extend
    else:
        # TODO: control how I want the children to be added...FIFO or LIFO
        pop = queue.popleft
        extend = lambda children: queue.extendleft(reversed(list(children)))
    counts_cache = {}
    subpaths_cache = {}
    fallbacks = {}
    dihed_list = [
        top_dihedral_choices,
        secondary_dihedral_choices
    ]
    if incomplete_dihedrals is not None:
        dihed_list.append(None)
    while queue:
        visited, path, choices = pop()
        if len(choices) == 0:
            counts_cache[visited] = {
                "children":[],
                "count":1
            }
            yield path
            continue
        if visited not in counts_cache:
            counts_cache[visited] = {
                "children":[],
                "count":None
            }
        elif counts_cache[visited]["count"] is None:
            # we have processed all of the child trees so now we can add up their counts
            counts_cache[visited]["count"] = sum(
                counts_cache[c]["count"]
                for c in counts_cache[visited]["children"]
                if counts_cache[c]["count"] is not None
            )

        if (
                counts_cache[visited]["count"] is None
                or counts_cache[visited]["count"] > 0
        ):
            some_good_choice = False
            for n,dihedral_choices in enumerate(dihed_list):
                for i,choice in enumerate(choices):
                    if dihedral_choices is None:
                        if incomplete_dihedrals is not None:
                            # really this is a fallback but it
                            # was easier to write it this way given what I had
                            if (visited, choice) not in fallbacks:
                                fallbacks[(visited, choice)] = _get_matching_dihedrals(
                                    choice,
                                    {
                                        k: v
                                        for k, v in incomplete_dihedrals.items()
                                        if (choice in k) and all(
                                            x == choice or x
                                            in visited for x in k
                                        ) and _check_populated_dihedral_complete(k, v, visited, choice)
                                    },
                                    internals=internals
                                )
                            diheds = fallbacks[(visited, choice)]
                        else:
                            continue
                    else:
                        diheds = dihedral_choices[choice]
                    if (visited, choice, n) not in subpaths_cache:
                        subpaths_cache[(visited, choice, n)] = [
                            d for d in diheds
                            if all(dd in visited for dd in d[1:])
                        ]
                    subpaths = subpaths_cache[(visited, choice, n)]
                    if len(subpaths) > 0:
                        some_good_choice = True
                        subvisited = visited | {choice}
                        counts_cache[visited]['children'].append(subvisited)
                        extend([
                            [
                                visited | {choice},
                                path + [subpaths],
                                choices[:i] + choices[i+1:],
                            ]
                        ])
                if some_good_choice:
                    break
        # # this will terminate on its own
        # if not some_good_choice:
        #     raise ValueError()
        ...

def get_fragments_from_internals(
        internals,
        triangles_and_dihedrons=None
):
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
    if triangles_and_dihedrons is None:
        triangles_and_dihedrons = get_internal_triangles_and_dihedrons(internals)

    td, dd = triangles_and_dihedrons
    known_atom_graph, complete_dihedrals = construct_atom_connection_graph_from_triangulation(
        internals, td, dd
    )

    comps = EdgeGraph.from_map(known_atom_graph)
    sels = comps.get_fragments(return_labels=True)

    return sels
def enumerate_zmatrices_from_internals(internals,
                                       triangles_and_dihedrons=None,
                                       atoms=None,
                                       # roots=None,
                                       ordering=None,
                                       graph=None,
                                       build_conversion=True,
                                       max_ordering_passes=1,
                                       **conversion_options
                                       ):
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
    from .ZMatrices import extract_zmatrix_internals

    if triangles_and_dihedrons is None:
        triangles_and_dihedrons = get_internal_triangles_and_dihedrons(internals)

    td, dd = triangles_and_dihedrons
    if atoms is None:
        atoms, idx = np.unique(np.concatenate(internals), return_index=True)
        atoms = atoms[np.argsort(idx)]

    known_atom_graph, complete_dihedrals = construct_atom_connection_graph_from_triangulation(
        internals, td, dd
    )

    t2 = {k:t for k,t in td.items() if nput.triangle_is_complete(t)}
    d2 = {k:t for k,t in dd.items() if nput.dihedron_is_complete(t)}
    d3 = {k:t for k,t in dd.items() if k not in d2 and len([tt for tt in t if tt is not None]) > 3}

    comps = EdgeGraph.from_map(known_atom_graph)
    zm_generators = []
    sels = comps.get_fragments(return_labels=True)
    ord, idx = np.unique(atoms, return_index=True)
    ord_map = dict(zip(ord, idx))
    comp_filts = {} # caching for speed
    d2_filts = {}
    d3_filts = {}
    label_mapping = {l:i for i,l in enumerate(comps.labels)}
    for atoms in sels:
        # if roots is None:
        atoms = sorted(atoms, key=lambda a:ord_map[a])
        #TODO: add canonicalization to cut down on comps
        generator = None
        # subgraph = comps.take([label_mapping[a] for a in atoms])
        # sublabel_mapping = {l:i for i,l in enumerate(subgraph.labels)}
        atom_ord = {a:i for i,a in enumerate(atoms)}
        sorted_atom_graph = {
            k: sorted([x for x in v if x in atom_ord], key=lambda a: atom_ord[a])
            for k, v in known_atom_graph.items()
            if k in atom_ord
        }
        if ordering is not None:
            subordering = [o for o in ordering if o in atom_ord]
            root_generators = [[subordering[:3]]]
        else:
            subordering = None
            root_generators = enumarate_zmatrix_roots_from_triangles(atoms, t2, known_atom_graph)

        for a in atoms:
            if a not in comp_filts:
                comp_filts[a] = _get_matching_dihedrals(a, complete_dihedrals, internals, check_complete=True)
            if a not in d2_filts:
                d2_filts[a] = _get_matching_dihedrals(a, d2, internals, check_complete=False)
            # if a not in d3_filts:
            #     d3_filts[a] = _get_matching_dihedrals(a, d3, internals, check_complete=False)

        def _filter(p, v):
            """
            **LLM Docstring**

            Apply the user-supplied candidate filter to a partial or complete atom ordering while preserving candidates when no filter is supplied.

            :param p: Candidate atom ordering passed to the enumeration filter.
            :type p: Any
            :param v: Metadata associated with the candidate ordering passed to the filter.
            :type v: Any
            :return: The value or updated object described above.
            :rtype: Any
            """
            p_set = {pp[0] for pp in p}
            for i in v[1:]:
                if i > 0 and i not in p_set:
                    return False
            return True

        if any(len(x) < 3 for x in sorted_atom_graph.values()):
            return None # don't even bother

        checked_roots = set()
        for root_groups in root_generators:
            for i, j, k in root_groups:
                root_key = tuple(sorted([i,j,k]))
                if root_key in checked_roots: continue
                root_blocks = [
                    [(i, -1, -2, -3)],
                    [(j, i, -1, -2)],
                    [
                        (k, j, i, -1)
                            if (k, j) in internals or (j, k) in internals else
                        (k, i, j, -1)
                    ]
                ]
                if subordering is not None:
                    rem_choices = [[
                        comp_filts.get(a, d2_filts.get(a, []))
                        for a in subordering[3:]
                    ]]
                else:
                    rem_choices = _grow_dihedral_trees(
                        (i, j, k),
                        [a for a in atoms if a not in {i, j, k}],
                        comp_filts,
                        d2_filts,
                        incomplete_dihedrals=d3,
                        internals=internals,
                    )
                for passes,follows in enumerate(rem_choices):
                    d_blocks = root_blocks + follows
                    possible_mats = itut.unique_product(
                        *d_blocks,
                        filter=_filter
                    )
                    try:
                        non_zero = next(possible_mats)
                    except StopIteration:
                        if max_ordering_passes >= 0 and passes + 1 >= max_ordering_passes:
                            break
                    else:
                        generator = itut.unique_product(
                            *d_blocks,
                            filter=_filter
                        )
                        break
                if generator is not None: #TODO: allow chaining for full enumeration
                    break
                else:
                    checked_roots.add(root_key) # if root perm doesn't work, the next ordering won't either
            if generator is not None:
                zm_generators.append(generator)
                break
        # for root_groups in root_generators:
        #     for i,j,k in root_groups:
        #         d_blocks = [
        #             [(i, -1, -2, -3)],
        #             [(j, i, -1, -2)],
        #             [
        #                 (k, j, i, -1)
        #                     if (k,j) in internals or (j, k) in internals else
        #                 (k, i, j, -1)
        #             ],
        #         ]
        #         root = [i, j, k]
        #         nreq = len(atoms) - 2
        #         if subordering is not None:
        #             rem_choices = [
        #                 [subordering[3:]]
        #             ]
        #         else:
        #             rem_choices = [
        #                 [[a for a in atoms if a not in {i, j, k}]],
        #                 order_fallback
        #             ]
        #         for rem_generators in rem_choices:
        #             (i, j, k) = root
        #             if dev.str_is(rem_generators, 'segment'):
        #                 rem_map:EdgeGraph = subgraph.take([sublabel_mapping[a] for a in atoms if a not in {i,j}])
        #                 sublabels = rem_map.labels
        #                 segments = rem_map.segment_by_chains(root=sublabels.index(k))
        #                 rem_generators = [[sublabels[i] for i in itut.flatten(segments)][1:]]
        #             elif dev.str_is(rem_generators, 'graph'):
        #                 git = graph_iter(sorted_atom_graph,
        #                                  root=k,
        #                                  visited={i, j},
        #                                  traversal_ordering='dfs',
        #                                  yield_paths='terminal',
        #                                  enable_disconnectivity=True)
        #                 rem_generators = (
        #                     tree[1:]
        #                     for tree, terminal in git
        #                     if len(tree) == nreq
        #                 )
        #             for passes, rem in enumerate(rem_generators):
        #                 for a in rem:
        #                     d_choices = comp_filts.get(a)
        #                     if d_choices is None:
        #                         d_choices = _get_matching_dihedrals(a, complete_dihedrals, internals,
        #                                                                 check_complete=True)
        #                         comp_filts[a] = d_choices
        #
        #                     if len(d_choices) == 0:
        #                         d_choices = d2_filts.get(a)
        #                         if d_choices is None:
        #                             d_choices = _get_matching_dihedrals(a, d2, internals, check_complete=False)
        #                             d2_filts[a] = d_choices
        #
        #                     if len(d_choices) == 0:
        #                         # import pprint
        #                         # pprint.pprint(d2)
        #                         raise ValueError(f"can't find dihedral choices for {a}")
        #                     d_blocks.append(d_choices)
        #
        #                 def _filter(p, v):
        #                     p_set = {pp[0] for pp in p}
        #                     for i in v[1:]:
        #                         if i > 0 and i not in p_set:
        #                             return False
        #                     return True
        #                 possible_mats = itut.unique_product(
        #                     *d_blocks,
        #                     filter=_filter
        #                 )
        #                 try:
        #                     non_zero = next(possible_mats)
        #                 except StopIteration:
        #                     # import pprint
        #                     # print("failed...", *root)
        #                     # pprint.pprint([np.array(d) for d in d_blocks])
        #                     # if root == (6, 5, 4):
        #                     #     raise ValueError(...)
        #                     # print(rem)
        #                     if max_ordering_passes >= 0 and passes+1 >= max_ordering_passes:
        #                         break
        #                 else:
        #                     generator = itut.unique_product(
        #                         *d_blocks,
        #                         filter=_filter
        #                     )
        #                     break
        #             if generator is not None:
        #                 break
        #         if generator is not None:
        #             break
        #     if generator is not None:
        #         zm_generators.append(generator)
        #         break
        # else:
        #     atoms = np.array(atoms)
        #     raise ValueError(f"can't find three atoms to serve as root that will generate a Z-matrix for {atoms}")

    if len(zm_generators) == 0:
        if build_conversion:
            yield None, None
        else:
            yield None
    elif len(zm_generators) == 1:
        possible_mats = zm_generators[0]
        for zm in possible_mats:
            if build_conversion:
                targets = extract_zmatrix_internals(zm)
                # print(np.array(zm))
                # print(targets)
                # import inspect
                # conv = find_internal_conversion(internals, targets[-1:],
                #                              triangles_and_dihedrons=triangles_and_dihedrons,
                #                                 verbose=True,
                #                              **conversion_options)
                # raise Exception()
                if graph is None:
                    conv = find_internal_conversion(internals, targets,
                                                    triangles_and_dihedrons=triangles_and_dihedrons,
                                                    missing_val=None,
                                                    **conversion_options)
                    if conv is not None:
                        yield zm, conv
                else:
                    conv = graph.find_conversions(targets,
                                                     create_single=True,
                                                     missing_val=None,
                                                     **conversion_options)
                    if conv is not None:
                        yield zm, conv
            else:
                yield zm
    else:
        for zm_list in itertools.product(*zm_generators):
            if build_conversion:
                if graph is None:
                    convs = [
                        find_internal_conversion(internals, extract_zmatrix_internals(zm),
                                                 triangles_and_dihedrons=triangles_and_dihedrons,
                                                 **conversion_options)
                        for zm in zm_list
                    ]
                else:
                    convs = [
                        graph.find_conversions(internals, extract_zmatrix_internals(zm),
                                               create_single=True,
                                               # missing_val='raise',
                                               **conversion_options)
                        for zm in zm_list
                    ]
                if all(c is not None for c in convs):
                    yield zm_list, convs
            else:
                yield zm_list



def get_internal_distance_conversion(
        internals,
        triangles_and_dihedrons=None,
        dist_set=None,
        # prior_coords=None,
        canonicalize=True,
        allow_completion=True,
        missing_val='raise',
        include_shapes=False,
        return_conversions=False,
        prep_conversions=True,
        cache=None
):
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
    if dist_set is None:
        dist_set = list(sorted(set(_enumerate_dists(internals)))) # remove dupes, sort
    if cache is None: cache = {}
    return dist_set, find_internal_conversion(internals, dist_set,
                                              canonicalize=canonicalize,
                                              triangles_and_dihedrons=triangles_and_dihedrons,
                                              missing_val=missing_val,
                                              allow_completion=allow_completion,
                                              return_conversions=return_conversions,
                                              prep_conversions=prep_conversions,
                                              include_shapes=include_shapes,
                                              cache=cache
                                              )

def get_internal_cartesian_conversion(
        internals,
        triangles_and_dihedrons=None,
        # prior_coords=None,
        canonicalize=True,
        missing_val='raise'
):
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
    #TODO: add direct conversion through Z-matrix if can be enumerated
    dists, dist_conv = get_internal_distance_conversion(internals,
                                                        triangles_and_dihedrons=triangles_and_dihedrons,
                                                        canonicalize=canonicalize,
                                                        missing_val=missing_val)
    n = (1 + np.sqrt(1 + 8 * len(dists))) / 2
    if int(n) != n:
        raise ValueError("fbad number of distances {len(dists)}")
    n = int(n)
    rows, cols = np.triu_indices(n, k=1)
    def convert(internals):
        """
        **LLM Docstring**

        Convert one internal-coordinate array to distances, embed those distances in Cartesian space, and apply optional reference alignment or embedding settings.

        :param internals: Available internal-coordinate specifications or their numerical values.
        :type internals: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        internals = np.asanyarray(internals)
        base_shape = internals.shape[:-1]
        internal_dists = dist_conv(internals)
        dm = np.zeros(base_shape + (n, n))
        dm[..., rows, cols] = internal_dists
        dm[..., cols, rows] = internal_dists
        new_points = nput.points_from_distance_matrix(dm)
        if new_points.shape[-1] < 3:
            pad_shape = new_points.shape[:-1] + (3-new_points.shape[-1],)
            new_points = np.concatenate([new_points, np.zeros(pad_shape, dtype=new_points.dtype)], axis=-1)
        return new_points
    return convert

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
    # detect whether or not they may be interconverted freely
    if triangles_and_dihedrons is None:
        if isinstance(internals, RADInternalCoordinateSet):
            triangles_and_dihedrons = internals.triangulation
            internals = internals.specs
        else:
            triangles_and_dihedrons = get_internal_triangles_and_dihedrons(internals, canonicalize=False)
    triangle, dihedrons = triangles_and_dihedrons
    for k,t in triangle.items():
        if not nput.triangle_is_complete(t):
            if raise_on_failure:
                raise ValueError(f"triangle cannot be completed, {k}:{t}")
            else:
                return False, (k,t)
    for k,t in dihedrons.items():
        if not nput.dihedron_is_complete(t):
            if raise_on_failure:
                raise ValueError(f"dihedral tetrahedron cannot be completed, {k}:{t}")
            else:
                return False, (k,t)
    return True, None

def get_internal_bond_graph(internals, atoms=None, triangles_and_dihedrons=None,
                            dist_set=None,
                            return_conversions=False,
                            complete_graph=False):
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
    if complete_graph:
        if dist_set is None:
            if atoms is None:
                atoms, idx = np.unique(np.concatenate(internals), return_index=True)
                atoms = atoms[np.argsort(idx)]
            dist_set = list(itertools.combinations(atoms, 2))
    dist_set, funs = get_internal_distance_conversion(internals,
                                                      allow_completion=complete_graph,
                                                      missing_val=None,
                                                      triangles_and_dihedrons=triangles_and_dihedrons,
                                                      return_conversions=True,
                                                      dist_set=dist_set)
    edges = [d for d, f in zip(dist_set, funs) if f is not None]
    if atoms is None:
        atoms = np.unique(np.concatenate(internals))

    mapping = {a:i for i,a in enumerate(atoms)}
    edges = [(mapping[i], mapping[j]) for i,j in edges]

    graph = EdgeGraph(atoms, edges)
    if return_conversions:
        return graph, (dist_set, funs)
    else:
        return graph

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
    # invalidate cache information for `dihedron_property_function`
    # from `find_internal_conversion`
    conversion_cache = cache.setdefault('disallowed_conversions', {})
    _, shape_index_map = inverse_triangulation
    for dihed in conversion_cache.keys():
        inds = shape_index_map[dihed]
        if any(all(d) in inds for d in extra_dists):
            conversion_cache[dihed] = set()
    return

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
        self.graph = InternalCoordinateGraph(base_internals, atoms=natoms)
        self.natoms = natoms
        if dist_set is None:
            if nput.is_int(natoms):
                natoms = np.arange(natoms)
            dist_set = list(itertools.combinations(natoms, 2))
        self.dist_set = dist_set
        self._all_dists = None
        self._stress_rank = None
        self._local_rank = None

    @property
    def dists(self):
        """
        **LLM Docstring**

        Return the current canonical distance set represented by the accepted coordinates.

        :return: The requested coordinate, graph, triangulation, derivative, or conversion data described above.
        :rtype: Any
        """
        if self._all_dists is None:
            checks = self.graph.find_conversions(self.dist_set, find_unreachable=False)
            self._all_dists = tuple(d for d,c in zip(self.dist_set, checks) if c is not None)
        return self._all_dists
    def check_rigidty(self, dists):
        """
        **LLM Docstring**

        Test whether a proposed distance graph is minimally rigid for the checker’s atom count using the configured rigidity criterion.

        :param dists: Candidate or current pair-distance set.
        :type dists: Any
        :return: Whether the tested condition is satisfied.
        :rtype: bool
        """
        rigid, (_, local_rank), stress = uniquely_rigid(
            dists, 3, natoms=self.natoms,
            return_components=True,
            # return_rigid_subgraphs=True
        )
        return rigid, local_rank, stress

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
        dist_pos = [n for n, i in enumerate(internals) if len(i) == 2]
        coords = [internals[n] for n in dist_pos]

        natoms = max(max(i) for i in internals) + 1
        # check rigidity
        rigid, (_, local_rank), stress = uniquely_rigid(
            coords, 3, natoms=natoms,
            return_components=True,
            return_rigid_subgraphs=True
        )

        if rigid:
            #TODO: prune overcomplete distance sets
            return coords, None

        rem_pos = [n for n, i in enumerate(internals) if len(i) > 2]
        rem = [internals[n] for n in rem_pos]

        return cls(coords, natoms), rem

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
        # if we have at least 3 shared distances we can figure this out...
        neighbors_i = set()
        neighbors_j = set()
        for a,b in dists:
            if a == i:
                if b == j: return True
                neighbors_i.add(b)
            elif a == j:
                if b == i: return True
                neighbors_j.add(b)
            elif b == i:
                neighbors_i.add(a)
            elif b == j:
                neighbors_j.add(a)
        return len(neighbors_i & neighbors_j) >= 3

    def check_distances_convertable(self, new_coords, dists, graph,
                                    allow_recursive_completions=False,
                                    filter_by_new=True
                                    ):
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
        main_checks = np.full(len(dists), False)
        for n,(i,j) in enumerate(dists):
            check = self.check_trilateratable_distance(i, j, self.dists)
            if check:
                main_checks[n] = True
        subchecks = np.where(~main_checks)[0]
        if filter_by_new:
            subchecks = [
                i for i in subchecks if
                any(all(dd in c for dd in dists[i]) for c in new_coords)
            ]
        check_dists = [dists[i] for i in subchecks]
        found = graph.find_conversions(check_dists,
                                       find_unreachable=False,
                                       allow_recursive_completions=allow_recursive_completions)
        for n,f in zip(subchecks, found):
            if f is not None:
                main_checks[n] = True
        return main_checks

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
        # if self._local_rank is None:
        rigid, local_rank, stress_rank = self.check_rigidty(self.dists)
        self._local_rank = local_rank

        graph = self.graph
        base_dists = self.dists
        check_dists = [d for d in self.dist_set if d not in base_dists]
        with graph.checkpoint() as checkpoint:
            # print("???", len(graph._unreachable))
            new_coords = graph.add_internals([c])
            # print("  >", len(graph._conversions), len(graph._unreachable), len(new_coords))
            # print("  >", len(graph.internals))

            checks = self.check_distances_convertable(new_coords, check_dists, graph)
            added_dists = tuple(
                i for i,c in zip(check_dists, checks)
                if c
            )

            if len(added_dists) > 0:
                test_dists = self._all_dists + added_dists
                rigid, local_rank, stress_rank = self.check_rigidty(test_dists)

                extend = True
                if rigid:
                    # coords = test
                    ...
                elif stress_rank is not None:
                    _, test_rank = stress_rank
                    extend = self._stress_rank is None or test_rank > self._stress_rank
                    if extend:
                        self._stress_rank = test_rank
                else:
                    extend = local_rank > self._local_rank
                    if extend:
                        self._local_rank = local_rank
                if (
                        (keep_bonds and len(c) == 2)
                        or (keep_angles and len(c) == 3)
                ):
                    extend = True
                if extend:
                    # print(added_dists)
                    # print(">>>", stress_rank, local_rank)
                    checkpoint.reset = False
                    # added_coords.append(c)
                    for c in added_dists: check_dists.remove(c)
                    self._all_dists = test_dists
                    # incl_coords.append(n)
                rigidity_data = rigid, local_rank, stress_rank
            else:
                extend = False
                rigidity_data = None
        return extend, (rigid, local_rank, stress_rank)

class InternalCoordinateGraph:
    """
    A graph mapping out the connections between a set of atoms based on the given set of internals
    """
    __slots__ = ['internals', 'atoms', 'triangulation',
                 '_completion_cache', '_conversions', '_unreachable', '_expanded_internals', '_tri_cache']
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
        self.internals = internals
        if atoms is None:
            atoms = max(max(i) for i in internals) + 1
        self.atoms = atoms
        if triangles_and_dihedrons is None:
            triangles_and_dihedrons = get_internal_triangles_and_dihedrons(internals)
        self.triangulation = triangles_and_dihedrons
        self._completion_cache = {}
        self._conversions = {}
        self._unreachable = {}
        self._expanded_internals = None
        self._tri_cache = {}
        # we map the unreachable set to the possible completions that _could_ have completed it
        # this way when we add an internal, we can check to see if there are any previously unreachable
        # coordinates that need an update, and then if those need an upd

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
        return get_core_triangulation(internals, target, cache=self._tri_cache)
    def enumerate_matching_dihedrons(self, target_coord):
        """
        **LLM Docstring**

        Yield dihedron records and permutations that contain the target coordinate’s atoms in a usable arrangement.

        :param target_coord: Coordinate for which matching dihedrons are sought.
        :type target_coord: Any
        :return: An iterator yielding the candidates described above.
        :rtype: Iterator
        """
        if self._expanded_internals is None:
            tri = self.triangulation
        else:
            tri = self._expanded_internals[1]
        if tri is None:
            ints, _, _ = self._get_expanded_internals(update_triangulation=False)
            tri = self.get_target_triangulation(ints, [target_coord])
        for i,d in tri[1].items():
            pos = []
            for x in target_coord:
                try:
                    xx = i.index(x)
                except ValueError:
                    break
                else:
                    pos.append(xx)
            else:
                if pos[-1] < pos[0]: pos = reversed(pos)
                yield tuple(pos), i, d
    def _get_expanded_internals(self, update_triangulation=True):
        """
        **LLM Docstring**

        Return the current coordinates plus intermediate coordinates completed by triangulation, optionally refreshing the triangulation first.

        :param update_triangulation: Whether to refresh triangulation data before using expanded coordinates or conversions.
        :type update_triangulation: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        if self._expanded_internals is None:
            ints = list(itut.delete_duplicates(
                canonicalize_internal(k) for k in (
                        list(self.internals)
                        + list(self._conversions.keys())
                )))
            if update_triangulation:
                tri = get_internal_triangles_and_dihedrons(ints)
                dihedrals = tri[1]
                dihedral_sets = {k: set(k) for k in dihedrals.keys()}
                base_intersections = {
                    k: {
                        b: len(dihedral_sets[k] & dihedral_sets[b])
                        for b in dihedrals.keys()
                    }
                    for k in dihedrals.keys()
                }
                pruned_intersections = {
                    k: {b: v for b, v in di.items() if v > 2}
                    for k, di in base_intersections.items()
                }
                dihedral_intersections = (base_intersections, pruned_intersections)
            else:
                tri = None
                dihedral_intersections = None
            self._expanded_internals = (ints, tri, dihedral_intersections)
        return self._expanded_internals
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
        self._conversions.update(new)
        if self._expanded_internals is not None:
            old_ints, old_tri, cur_int = self._expanded_internals
            new_internals = [
                canonicalize_internal(i) for i in new.keys()
                if canonicalize_internal(i) not in old_ints
            ]
            ints = old_ints + new_internals
            if update_triangulation:
                # tri = update_triangulation(
                #     old_tri,
                #     new_internals,
                #     [],
                #     triangulation_internals=old_ints
                # )
                tri = get_internal_triangles_and_dihedrons(ints)
                dihedrals = tri[1]
                new_di = [k for k in dihedrals if k not in old_tri[1]]
                dihedral_sets = {k: set(k) for k in dihedrals.keys()}
                base_intersections = {
                    k: {
                        b: len(dihedral_sets[k] & dihedral_sets[b])
                        for b in dihedrals.keys()
                    }
                    for k in new_di
                }
                pruned_intersections = {
                    k: {b: v for b, v in di.items() if v > 2}
                    for k, di in base_intersections.items()
                }
                dihedral_intersections = cur_int[0] | base_intersections
                pruned_dihedral_intersections = cur_int[1] | pruned_intersections
                dihedral_intersections = (dihedral_intersections, pruned_dihedral_intersections)
            else:
                tri = None
                dihedral_intersections = None
            self._expanded_internals = (ints, tri, dihedral_intersections)

    def find_conversions(self,
                         target_internals,
                         unconvertable_atoms=None,
                         allow_recursive_completions=False,
                         allow_ambiguous_completions=False,
                         find_unreachable=True,
                         verbose=False,
                         create_single=False,
                         missing_val=None,
                         depth=0,
                         max_depth=5,
                         **etc):
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
        initial_set = target_internals

        target_internals = [
            i for i in target_internals
            if i not in self._conversions
               and i not in self._unreachable
        ]
        if len(target_internals) > 0:
            expanded_internals, expanded_triangulation, expanded_intersections = self._get_expanded_internals(update_triangulation=False)
            index_mapping = [self._make_conversion(self._conversions.get(i)) for i in expanded_internals]
            conversions = []
            shapes = []
            for t in target_internals:
                c, s = find_internal_conversion(expanded_internals,
                                                t,
                                                triangles_and_dihedrons=self.get_target_triangulation,
                                                include_shapes=True,
                                                allow_completion=True,
                                                return_conversions=True,
                                                index_mapping=index_mapping,
                                                allow_recursive_completions=allow_recursive_completions,
                                                # dihedral_intersections=expanded_intersections,
                                                allow_ambiguous_completions=allow_ambiguous_completions,
                                                missing_val=None,
                                                cache=self._completion_cache,
                                                verbose=verbose,
                                                **etc)
                conversions.append(c)
                shapes.append(s)

            # this gives us the basic completeable set of coordinates
            new_conv = {i:c for i,c in zip(target_internals, conversions) if c is not None}
            if len(new_conv) > 0:
                self._update_conversions(new_conv, update_triangulation=False)


            # if a coordinate _wasn't_ possible to complete, we want to
            # walk through the possible completions by going through
            # the current triangulation and finding the coordinates we are missing
            incomplete = [i for i,c in zip(target_internals, conversions) if c is None]
            cache = self._completion_cache.setdefault('trie_expansions', {})
            spec_data = nput.dihedron_property_specifiers()
            if unconvertable_atoms is None:
                unconvertable_atoms = set()
            if max_depth is not None and depth > max_depth:
                find_unreachable = False
            if find_unreachable and not allow_recursive_completions:
                for n,target in enumerate(incomplete):
                    # if n > mn or depth > mn: raise Exception()
                    if target in self._conversions: continue # this can be completed within the loop
                    if target not in self._unreachable: self._unreachable[target] = []
                    # print("???", n, depth, target, len(self._unreachable))
                    if (not allow_ambiguous_completions) and len(target) == 4: continue
                    for x,d,s in self.enumerate_matching_dihedrons(target):
                        name = nput.dihedron_property_specifiers(x)['name']
                        pref_keys, possible_conversions = nput.sorted_dihedron_completions(s, name, cache=cache)
                        key_map = {}

                        # this gives us a set of coordinates to complete the dihedron
                        # we check to see if we have determined if any of them are reachable or not
                        # if they have been checked we short circuit
                        # otherwise we traverse depth first
                        pref_coords = []
                        for kl in pref_keys:
                            coord_keys = []
                            full_args = possible_conversions[kl][0]
                            for k in full_args:
                                if k not in key_map:
                                    key_map[k] = canonicalize_internal([d[i] for i in spec_data[k]['coord']], check_invalid=False)
                                coord_keys.append(key_map[k])
                            pref_coords.append(coord_keys)
                        self._unreachable[target] = sorted(
                            {
                                tuple(t)
                                for t in itertools.chain(self._unreachable[target], pref_coords)
                            },
                            key=len
                        )
                        if verbose:
                            print()
                        for kl,coord_keys in zip(pref_keys, pref_coords):
                            # if not allow_ambiguous_completions and any(len(k) == 4 for k in coord_keys): continue
                            if any(k in self._unreachable for k in coord_keys): continue
                            if any(len(set(k) & unconvertable_atoms) == len(k) for k in coord_keys): continue
                            unconverted_k = [k for k in coord_keys if k not in self._conversions]
                            if verbose:
                                print()
                            if len(unconverted_k) > 0:
                                #TODO: expand the graph _before_ applying this search
                                #      to speed up retrieval? -> already cached in `_conversions`
                                #TODO: try a BFS? would give the minimal conversion at the cost of more code
                                subs = self.find_conversions(unconverted_k,
                                                             unconvertable_atoms=unconvertable_atoms,
                                                             depth=depth+1,
                                                             verbose=verbose,
                                                             **etc)
                                unreachable_edits = {}
                                for s,k in zip(subs, unconverted_k):
                                    if s is not None and k in self._unreachable: # can be removed inside the loop
                                        unreachable_edits[k] = self._unreachable.pop(k)
                                if all(s is not None for s in subs):
                                    self._update_conversions({
                                        target:([key_map[x] for x in possible_conversions[kl][0]],
                                                kl, unconverted_k,
                                                possible_conversions[kl])
                                    }, update_triangulation=False)
                                    break
                                else:
                                    self._unreachable.update(unreachable_edits)

                        # unconvertable_atoms.update(d)
        conversions = [self._make_conversion(self._conversions.get(i)) for i in initial_set]
        c2 = []
        raise_on_missing = dev.str_is(missing_val, 'raise')
        for t,c in zip(target_internals, conversions):
            if c is None:
                if raise_on_missing:
                    raise ValueError(f"can't find conversion for {t} from {self}")
                else:
                    c = missing_val
            c2.append(c)
        if create_single:
            if any(c is None for c in conversions): return None
            def convert(internal_spec, order=None, conversions=conversions, **kwargs):
                """
                **LLM Docstring**

                Evaluate the resolved graph conversions and assemble target values in the requested order, applying stored orientation signs and completion dependencies.

                :param internal_spec: Coordinate specification associated with a cached graph conversion.
                :type internal_spec: Any
                :param order: Highest derivative order to compute.
                :type order: Any
                :param conversions: Conversion objects associated with the cached target coordinates.
                :type conversions: Any
                :param kwargs: Additional options forwarded to the triangulation reduction or merge routine.
                :type kwargs: Any
                :return: The value or updated object described above.
                :rtype: Any
                """
                convs = [
                    c(internal_spec)
                    for c in conversions
                ]
                if order is None:
                    res = np.moveaxis(np.array(convs), 0, -1)
                else:
                    res = [
                        np.moveaxis(np.array([c[i] for c in convs]), 0, -1)
                        for i in range(order + 1)
                    ]
                return res
            return InternalCoordinateConversion(
                convert,
                conversions,
                name="aggregate"
            )
        else:
            return conversions

    def _make_conversion(self, conv):
        """
        **LLM Docstring**

        Wrap a conversion specification as a callable that first computes any required intermediate completions.

        :param conv: Conversion specification to wrap.
        :type conv: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        if isinstance(conv, InternalCoordinateConversion) or conv is None:
            return conv
        coord_keys, kl, unconverted_k, possible_convs = conv

        full_args, base_args, rem_inds, base_inds, func = possible_convs
        completions = [self._make_conversion(self._conversions.get(k)) for k in coord_keys]
        if len(completions) < len(full_args):
            raise ValueError(kl, coord_keys, full_args)

        if any(isinstance(comp, tuple) for comp in completions):
            raise Exception(completions)

        def convert(internal_values, completions=completions):
            """
            **LLM Docstring**

            Evaluate prerequisite completion conversions, append those values to the input vector, and then evaluate the requested target conversion.

            :param internal_values: Numerical values of the source internal coordinates.
            :type internal_values: Any
            :param completions: Intermediate conversion callables required before the target conversion.
            :type completions: Any
            :return: The value or updated object described above.
            :rtype: Any
            """
            base_args = [
                f(internal_values) for f in completions
            ]
            # print(">>", conv[0])
            # print(completions[-1])
            # print("v:", base_args)
            return func(*base_args)
        return InternalCoordinateConversion(
            convert,
            conv,
            name="convert_multi_" + func.__name__
        )

    def get_bond_graph(self,
                       dist_set=None,
                       return_conversions=True):
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
            atoms = self.atoms
            if nput.is_int(atoms):
                atoms = np.arange(atoms)
            if dist_set is None:
                dist_set = list(itertools.combinations(atoms, 2))

            # print(
            #     self.find_conversions([(3, 4)], verbose=True, allow_recursive_completions=False)
            # )
            # raise Exception(...)

            funs = self.find_conversions(dist_set)
            edges = [d for d, f in zip(dist_set, funs) if f is not None]
            #
            # import pprint
            # pprint.pprint(edges)

            # print(res:=self.find_conversions(
            #     [(3, 4)],
            #     allow_recursive_completions=False,
            #     verbose=True
            # ))
            # raise Exception(res)

            mapping = {a: i for i, a in enumerate(atoms)}
            edges = [(mapping[i], mapping[j]) for i, j in edges]

            graph = EdgeGraph(self.atoms, edges)
            if return_conversions:
                return graph, (dist_set, funs)
            else:
                return graph

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
            self.graph = g
            self.reset = reset
            self._internals = None
            self._triangulation = None
            self._conversions = None
            self._unreachable = None
            self._exp_int = None
        def __enter__(self):
            """
            **LLM Docstring**

            Snapshot the graph’s mutable state and return the graph for temporary edits inside a context manager.

            :return: The checkpointed internal-coordinate graph.
            :rtype: InternalCoordinateGraph
            """
            self._internals = self.graph.internals.copy()
            self._triangulation = tuple(t.copy() for t in self.graph.triangulation)
            self._conversions = self.graph._conversions.copy()
            self._unreachable = self.graph._unreachable.copy()
            self._exp_int = self.graph._expanded_internals
            return self
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
            if self.reset:
                self.graph.internals = self._internals
                self.graph.triangulation = self._triangulation
                self.graph._conversions = self._conversions
                self.graph._unreachable = self._unreachable
                self.graph._expanded_internals = self._exp_int

    def checkpoint(self):
        """
        **LLM Docstring**

        Return a context manager for making temporary changes to the internal-coordinate graph.

        :return: The value or updated object described above.
        :rtype: Any
        """
        return self.GraphCheckpoint(self)

    def add_internals(self, internals):
        """
        **LLM Docstring**

        Add coordinates to the graph, update triangulation and bond data, and refresh conversion caches for targets that become directly or indirectly available.

        :param internals: Available internal-coordinate specifications or their numerical values.
        :type internals: Any
        :return: The value or updated object described above.
        :rtype: Any
        """
        # update triangulation
        # determine which distances could have been impacted by this change
        # check if any of those are completable
        if nput.is_int(internals[0]):
            internals = [internals]
        internals = [i for i in internals if i not in self.internals]
        if self.triangulation is None:
            self.internals = list(self.internals) + list(internals)
            self.triangulation = get_internal_triangles_and_dihedrons(self.internals)
        else:
            self.triangulation = update_triangulation(
                self.triangulation,
                list(internals),
                [],
                triangulation_internals=self.internals
            )
            self.internals = list(self.internals) + list(internals)
        if self._expanded_internals is not None:
            exp_int, t, d = self._expanded_internals
            actually_new = {
                i:m for m,i in enumerate(internals)
                if canonicalize_internal(i) not in exp_int
            }
            if len(actually_new) > 0:
                self._update_conversions(actually_new)

        # all unreachable coordinates now need to be checked to see if they are potentially
        # reachable now
        newly_reachable = {canonicalize_internal(i) for i in internals}
        old_newly_reachable = -1
        check_opts = {
            canonicalize_internal(c):[
                [canonicalize_internal(s) for s in subopt if s not in self._conversions]
                for subopt in subopts
            ]
            for c,subopts in self._unreachable.items()
        }

        mod_atoms = {a for i in newly_reachable for a in i}
        for i in newly_reachable:
            if i in check_opts:
                del check_opts[i]
        # ml = 15
        while len(newly_reachable) > old_newly_reachable:
            # if old_newly_reachable > ml: raise Exception(...)
            old_newly_reachable = len(newly_reachable)
            prunes = []
            for coord, subopts in check_opts.items():
                if len(mod_atoms & set(coord)) < 2: continue # not enough has changed
                if any(
                    all(s in newly_reachable for s in subopt)
                    for subopt in subopts
                ):
                    mod_atoms.update(coord)
                    newly_reachable.add(coord)
                    prunes.append(coord)
                    break
            for i in prunes:
                if i in check_opts:
                    del check_opts[i]


        for i in newly_reachable:
            for j in [i, tuple(reversed(i))]:
                if j in self._unreachable:
                    del self._unreachable[j]
                    break

        # self._unreachable = {}
        # self._conversions = {}

        return newly_reachable

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
        raise NotImplementedError("need to cache more information to remove an element")
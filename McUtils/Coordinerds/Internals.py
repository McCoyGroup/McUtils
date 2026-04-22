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
        if typename is None and isinstance(type, str):
            typename = type
            def register(type, typename=typename):
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
        return False

    def equivalent_to(self, other):
        return (
                type(self) is type(other)
                and self.canonicalize().get_indices() == other.canonicalize().get_indices()
        )
    def __eq__(self, other):
        return self.equivalent_to(other)

    @abc.abstractmethod
    def canonicalize(self):
        ...

    @abc.abstractmethod
    def get_indices(self) -> Tuple[int, ...]:
        ...

    def __hash__(self):
        return hash((type(self), self.get_indices()))
    @abc.abstractmethod
    def reindex(self, reindexing):
        ...

    @abc.abstractmethod
    def get_carried_atoms(self, context:InternalSpec):
        ...

    @abc.abstractmethod
    def get_constraint_rads(self) -> list[Distance|Angle|Dihedral]:
        ...

    @abc.abstractmethod
    def get_expansion(self, coords, order=None, **opts) -> List[np.ndarray]:
        ...

    @abc.abstractmethod
    def get_inverse_expansion(self, coords, order=None, moved_indices=None, **opts) -> List[np.ndarray]:
        ...

    def _prep_left_right_atoms(self, context, moved_indices, left_atoms, right_atoms):
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
        self.inds = tuple(indices)
        # a hack to make these classes easier to work with
        self.forward_conversion = type(self).forward_conversion
        self.inverse_conversion = type(self).inverse_conversion
    def __repr__(self):
        cls = type(self)
        return f"{cls.__name__}{self.inds}"
    def reindex(self, reindexing):
        return type(self)([reindexing[i] for i in self.inds])
    def canonicalize(self):
        if self.inds[-1] < self.inds[0]:
            return type(self)(tuple(self.inds[::-1]))
        else:
            return self
    def get_indices(self):
        return self.inds
    def get_dropped_internals(self):
        return [self]
    def get_carried_atoms(self, context:InternalSpec, max_branching=5):
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
        return self.forward_conversion(coords, *self.inds, order=order, **opts)
    def get_inverse_expansion(self, coords, *, order=None, moved_indices=None,
                              context=None,
                              left_atoms=None, right_atoms=None, masses=None, **opts):
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
        return (
            dev.is_list_like(input)
            and len(input) == 2
            and nput.is_int(input[0])
            and nput.is_int(input[1])
        )
    def get_constraint_rads(self):
        return [self]

@InternalCoordinateType.register("bend")
class Angle(BasicInternalType):
    forward_conversion = nput.angle_vec
    inverse_conversion = nput.angle_expansion
    @classmethod
    def could_be(cls, input):
        return (
            dev.is_list_like(input)
            and len(input) == 3
            and nput.is_int(input[0])
            and nput.is_int(input[1])
        )
    def get_constraint_rads(self):
        return [self]
    def get_dropped_internals(self):
        i,j,k = self.get_indices()
        return [self, Distance((i, j)), Distance((j, k))]

@InternalCoordinateType.register("dihedral")
class Dihedral(BasicInternalType):
    forward_conversion = nput.dihed_vec
    inverse_conversion = nput.dihed_expansion
    @classmethod
    def could_be(cls, input):
        return (
            dev.is_list_like(input)
            and len(input) == 4
            and nput.is_int(input[0])
            and nput.is_int(input[1])
        )
    def get_constraint_rads(self):
        return [self]
    def get_dropped_internals(self):
        i,j,k,l = self.get_indices()
        return [self, Distance((i, j)), Distance((j, k)), Distance((k, l))]

@InternalCoordinateType.register("wag")
class Wag(BasicInternalType):
    forward_conversion = nput.wag_vec
    inverse_conversion = nput.wag_expansion
    def get_constraint_rads(self):
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
        super().__init__(indices)
        self.masses = masses
    def canonicalize(self):
        return type(self)(np.sort(self.inds))
    def get_carried_atoms(self, context:InternalSpec):
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
        super().__init__(indices)
        self.masses = masses
    def canonicalize(self):
        return type(self)((np.sort(self.inds[0]), np.sort(self.inds[1])))
    def get_indices(self):
        return tuple(self.inds[0]) + tuple(self.inds[1])
    def reindex(self, reindexing):
        return type(self)([
            [reindexing[i] for i in self.inds[0]],
            [reindexing[i] for i in self.inds[1]]
        ])
    def get_carried_atoms(self, context:InternalSpec):
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
    @classmethod
    def from_zmatrix(cls, *zmats, additions=None, **opts):
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
        if self._atom_lists is None:
            self._atom_lists = tuple(a.get_indices() for a in self.coords)
        return self._atom_lists
    @property
    def atoms(self) -> Tuple[int]:
        if self._atoms is None:
            self._atoms = tuple(itut.delete_duplicates(c for a in self.atom_sets for c in a))
        return self._atoms

    def get_triangulation(self):
        if self._tri_di is None:
            # print(self.rad_set)
            self._tri_di = get_internal_triangles_and_dihedrons(self.rad_set)
        return self._tri_di
    def get_pruned_rads(self):
        if self._pruned_rads is None:
            self._pruned_rads = self.non_redundant_rads()
        return self._pruned_rads
    def get_pruned_triangulation(self):
        if self._pruned_tri_di is None:
            # print(self.rad_set)
            self._pruned_tri_di = get_internal_triangles_and_dihedrons(self.get_pruned_rads()[0])
        return self._pruned_tri_di
    def get_bond_graph(self) -> EdgeGraph:
        if self._bond_graph is None:
            self._bond_graph = get_internal_bond_graph(self.rad_set, self.atoms,
                                                                         triangles_and_dihedrons=self.get_triangulation(),
                                                                         return_conversions=False)
        return self._bond_graph
    def get_distance_conversions(self):
        if self._dist_convs is None:
            self._dist_convs = get_internal_bond_graph(self.rad_set, self.atoms,
                                                       triangles_and_dihedrons=self.get_triangulation(),
                                                       return_conversions=True,
                                                       complete_graph=True)
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
        if self._zm_conv is None:
            # pruned_rads, indices = self.get_pruned_rads()
            # tri = self.get_pruned_triangulation()
            pruned_rads = self.rad_set
            indices = None
            tri = self.get_triangulation()
            for zm_conv in enumerate_zmatrices_from_internals(pruned_rads, tri,
                                                              atoms=self.atoms,
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
        if self._dm_conv is None:
            bg, dist_stuff = self.get_distance_conversions()
            funs = dict(zip(*dist_stuff))
            groups = bg.get_fragments(return_labels=True)
            convs = []
            for g in groups:
                blocks = []
                for i,j in itertools.combinations(g, 2):
                    blocks.append(funs[(i,j)])
                if any(b is None for b in blocks):
                    return None, None
                    #convs.append(None)
                else:
                    def prep(internals, blocks=blocks):
                        return np.moveaxis([
                            f(internals) for f in blocks
                        ], 0, -1)
                    convs.append(prep)
            self._dm_conv = groups, convs
        return self._dm_conv

    graph_split_method = 'dists'
    def get_dropped_internal_bond_graph(self, internals, method=None):
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
            # print([e.shape for e in nput.concatenate_expansions(expansion, concatenate_values=True)],
            #       [i.shape for i in nput.concatenate_expansions(inverses, concatenate_values=False)])
            # for f,r in zip(inverses, expansion):
            #     print([ff.shape for ff in f], [rr.shape for rr in r])
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
        cls = type(self)
        return f"{cls.__name__}({self.coords})"

    def get_direct_inverses(self, coords, order=1, terms=None, combine_expansions=True, **opts) -> List[np.ndarray]:
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
                                **deriv_opts):
        from .ZMatrices import zmatrix_from_values, canonicalize_zmatrix
        from .Conveniences import zmatrix_to_cartesian#, cartesian_to_zmatrix
        use_zmat = True
        conv = self.get_zmat_conv(raise_on_incomplete=False)
        if conv[0] is None:
            conv = self.get_dmat_conv()
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
                    blocks.append([[nput.points_from_distance_matrix(dists, use_triu=True), perm]])

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
            x, y, z = np.moveaxis(carts[..., perm[:3], :], -2, 0)
            u = y - x
            v = z - x
            norms = nput.vec_norms([u, v])
            mod_locs = np.all(norms > 1e-8, axis=0)
            if np.any(mod_locs):
                u, v = nput.vec_normalize([u[mod_locs, :], v[mod_locs, :]], norms=norms[:, mod_locs])
                a = nput.broadcast_constant([1, 0, 0], u.shape)
                b = nput.broadcast_constant([0, 0, 1], u.shape)
                r1 = nput.rotation_matrix(a, u)
                z = np.reshape(b[..., np.newaxis, :] @ r1, u.shape)
                normal = np.cross(u, v)
                ang, cross = nput.vec_angles(normal, z, return_crosses=True)
                frame = r1 @ nput.rotation_matrix(cross, ang)
                coord[mod_locs] = coord[mod_locs] @ frame
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
        return pebble_rigidity(
            # self.get_triangulation_distances(),
            self.get_triangulation_novel_internals(),
            3
        )
    def non_redundant_rads(self):
        print(len(self.rad_set))
        (internals, dropped_coordinates), triangles_and_dihedrons = get_non_redundant_internals(
            self.rad_set,
            triangles_and_dihedrons=self.get_triangulation(),
            return_indices=True
        )
        dropped_coordinates, dropped_inds = dropped_coordinates
        map = np.setdiff1d(np.arange(len(self.rad_set)), dropped_inds)
        return internals, map

        # (internals, dropped_coordinates), triangles_and_dihedrons
        # raise Exception(uuuh)
        distance_map = get_internal_shape_map()
        prunes = self.check_redundancy()
        map = np.where(prunes)[0]
        return [self.rad_set[i] for i in map], map

def canonicalize_internal(coord, return_sign=False):
    sign = 1
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
    return (
        len(coord) > 1 and len(coord) < 5
        and all(nput.is_int(c) for c in coord)
    )

def is_coordinate_list_like(clist):
    return dev.is_list_like(clist) and all(
        is_valid_coordinate(c) for c in clist
    )

class RADInternalCoordinateSet:
    def __init__(self, coord_specs:'list[tuple[int]]', prepped_data=None, triangulation=None):
        self._specs = tuple(coord_specs) if coord_specs is not None else coord_specs
        if prepped_data is not None:
            self._indicator, self.coordinate_indices, self.ind_map, self.coord_map = prepped_data
        else:
            self._indicator, self.coordinate_indices, self.ind_map, self.coord_map = self.prep_coords(coord_specs)
        self._triangulation = triangulation

    @property
    def specs(self):
        if self._specs is None:
            self._specs = tuple(self._create_coord_list(self._indicator, self.ind_map, self.coord_map))
        return self._specs

    IndicatorMap = collections.namedtuple("IndicatorMap", ['primary', 'child'])
    IndsMap = collections.namedtuple("IndsMap", ['dists', 'angles', 'diheds'])
    InternalsMap = collections.namedtuple("InternalsMap", ['dists', 'angles', 'diheds'])
    @classmethod
    def prep_coords(cls, coord_specs):
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
        return self._map_dispatch(self.coord_map, coord)
    def _ind_map_dispatch(self, i):
        return self._map_dispatch(self.ind_map, i)
    def find(self, coord, missing_val='raise'):
        return nput.find(self._coord_map_dispatch(coord), coord, missing_val=missing_val)

    @classmethod
    def get_coord_from_maps(cls, item, indicator:IndicatorMap, ind_map, coord_map):
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
        return self.get_coord_from_maps(item, self._indicator, self.ind_map, self.coord_map)

    @classmethod
    def _create_coord_list(cls, indicator, inds, vals:InternalsMap):
        #TODO: make this more efficient, just concat the sub
        map = np.argsort(indicator.child)
        full = vals.diheds.tolist() + vals.angles.tolist() + vals.diheds.tolist()
        return [ tuple(full[i]) for i in map ]
    def permute(self, perm, canonicalize=True):
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
        return get_internal_triangles_and_dihedrons(self.specs, canonicalize=False)
    @property
    def triangulation(self):
        if self._triangulation is None:
            self._triangulation = self.get_triangulation()
        return self._triangulation


def get_canonical_internal_list(coords):
    if isinstance(coords, RADInternalCoordinateSet):
        return coords.specs
    else:
        return [canonicalize_internal(c) for c in coords]

def find_internal(coords, coord, missing_val:'Any'='raise', canonicalize=True, allow_negation=False, indices=None):
    if canonicalize:
        coord = canonicalize_internal(coord)
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
    if isinstance(coords, RADInternalCoordinateSet):
        return coords.permute(perm, canonicalize=canonicalize)
    else:
        return [
            canonicalize_internal([perm[c] if c < len(perm) else c for c in coord])
                if canonicalize else
            tuple(perm[c] if c < len(perm) else c for c in coord)
            for coord in coords
        ]

def coordinate_sign(old, new, canonicalize=True):
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
            old = canonicalize_internal(old)
            new = canonicalize_internal(new)

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
    return (
        dm_data.input_indices[0]
            if dm_data.conversion is None else
        None
    )
def _get_pregen_ind(dm_data):
    return (
        None
            if dm_data.conversion is None else
        dm_data.mapped_pos
    )
def get_internal_distance_conversion_spec(internals, canonicalize=True, cache=None):
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
    if conversion_spec.conversion is None:
        def convert(internal_values, _, n=conversion_spec.input_indices[0]):
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
    base = (a, b, c)
    for perm in _tri_perms:
        key = [base[_] for _ in perm]
        key, sign = canonicalize_internal(key, return_sign=True)
        if key in mod_sets:
            break
    else:
        perm = (0, 1, 2)
        key, sign = canonicalize_internal((a, b, c), return_sign=True)
    if sign == -1:
        perm = list(reversed(perm))
    perm = np.argsort(perm)

    b = tuple(sorted(key.index(_) for _ in [i,j]))
    return key, nput.triangle_property_specifiers(b)["name"], perm
def _permute_tri_data(terms, perm):
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
    base = (a, b, c, d)
    for perm in _dihedron_perms:
        key = [base[_] for _ in perm]
        key, sign = canonicalize_internal(key, return_sign=True)
        if key in mod_sets:
            break
    else:
        perm = (0, 1, 2, 3)
        key, sign = canonicalize_internal((a, b, c, d), return_sign=True)
    if sign == -1:
        perm = list(reversed(perm))
    perm = np.argsort(perm)

    b = tuple(sorted(key.index(_) for _ in [i,j]))
    return key, nput.dihedron_property_specifiers(b)["name"], perm
def _get_dihedron_angle_key_name(mod_sets, a,b,c,d, i, j, k):
    base = (a, b, c, d)
    for perm in _dihedron_perms:
        key = [base[_] for _ in perm]
        key, sign = canonicalize_internal(key, return_sign=True)
        if key in mod_sets:
            break
    else:
        perm = (0, 1, 2, 3)
        key, sign = canonicalize_internal((a, b, c, d), return_sign=True)
    if sign == -1:
        perm = list(reversed(perm))
    perm = np.argsort(perm)

    b = canonicalize_internal(tuple(key.index(_) for _ in [i,j,k]))
    z = nput.dihedron_property_specifiers(b)["name"]
    return key, z, perm
def _get_dihedron_dihed_key_name(mod_sets, a,b,c,d, i, j, k, l):
    base = (a, b, c, d)
    for perm in _dihedron_perms:
        key = [base[_] for _ in perm]
        key, sign = canonicalize_internal(key, return_sign=True)
        if key in mod_sets:
            break
    else:
        perm = (0, 1, 2, 3)
        key, sign = canonicalize_internal((a, b, c, d), return_sign=True)
    if sign == -1:
        perm = list(reversed(perm))
    perm = np.argsort(perm)

    key_pos = tuple(key.index(_) for _ in [i,j,k,l])
    x = canonicalize_internal(key_pos)
    z = nput.dihedron_property_specifiers(x)["name"]
    return key, z, perm
def _permute_dihed_data(terms, perm):
    new = set()
    for t in terms:
        x = nput.dihedron_property_specifiers(t)["coord"]
        y = canonicalize_internal([perm[i] for i in x])
        new.add(nput.dihedron_property_specifiers(y)["name"])
    return new
def _validate_dihed_triangulation(mod_sets, key, internals, adding=None):
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

def get_internal_triangles_and_dihedrons(internals,
                                         canonicalize=True,
                                         construct_shapes=True,
                                         prune_incomplete=True,
                                         validate=False,
                                         allow_partially_defined=True,
                                         create_dihedra=True) -> tuple[
    dict[tuple[int, int, int], nput.TriangleData],
    dict[tuple[int, int, int, int], nput.DihedralTetrahedronData]
]:
    tri_sets:dict[tuple[int],set] = {}
    dihed_sets:dict[tuple[int],set] = {}
    for coord in internals:
        if canonicalize:
            coord = canonicalize_internal(coord)
        if len(coord) == 2:
            i,j = coord
            mod_tris = tri_sets.copy()
            for (k,l,m),v in tri_sets.items():
                if i == k:
                    if j == l:
                        v.add("a")
                    elif j == m:
                        v.add("c")
                    elif m is None:
                        key, z, perm = _get_tri_bond_key_name(mod_tris, k, l, j, i, j)
                        v = _permute_tri_data(v, perm)
                        mod_tris[key] = mod_tris.get(key, set()) | v | {z}
                elif i == l:
                    if j == k:
                        v.add("a")
                    elif j == m:
                        v.add("b")
                    elif m is None:
                        key, z, perm = _get_tri_bond_key_name(mod_tris, k, l, j, i, j)
                        v = _permute_tri_data(v, perm)
                        mod_tris[key] = mod_tris.get(key, set()) | v | {z}
                elif i == m:
                    if j == l:
                        mod_tris[(k,l,m)].add("b")
                    elif j == k:
                        mod_tris[(k,l,m)].add("c")
                elif m is None and j in (k, l):
                    key, z, perm = _get_tri_bond_key_name(mod_tris, k, l, i, i, j)
                    v = _permute_tri_data(v, perm)
                    mod_tris[key] = mod_tris.get(key, set()) | v | {z}
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
                            if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                        elif j == m:
                            v.add("x")
                            key = (k, l, m, n)
                            if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                        elif j == n:
                            v.add("z")
                            key = (k, l, m, n)
                            if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                        elif m is None:
                            key = (k, l, j, None)
                            mod_sets[key] = mod_sets.get(key, set()) | v | {"x"}
                            if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                        elif n is None:
                            key, z, perm = _get_dihedron_bond_key_name(mod_sets, k,l,m,j, i, j)
                            v = _permute_dihed_data(v, perm)
                            mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                            if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                    elif i == l:
                        if j == k:
                            v.add("a")
                            key = (k, l, m, n)
                            if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                        elif j == m:
                            v.add("b")
                            key = (k, l, m, n)
                            if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                        elif j == n:
                            v.add("y")
                            key = (k, l, m, n)
                            if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                        elif m is None:
                            key = (k,l,j,n)
                            mod_sets[key] = mod_sets.get(key, set()) | v | {"b"}
                            if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                        elif n is None:
                            key, z, perm = _get_dihedron_bond_key_name(mod_sets, k,l,m,j, i, j)
                            v = _permute_dihed_data(v, perm)
                            mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                            if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                    elif i == m:
                        if j == k:
                            #TODO: double check this doesn't duplicate somehow
                            key = (k,l,m,n)
                            mod_sets[key].add("a")
                            if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                        elif j == l:
                            key = (k,l,m,n)
                            mod_sets[key].add("b")
                            if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                        elif j == n:
                            key = (k,l,m,n)
                            mod_sets[key].add("c")
                            if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                        elif n is None:
                            key, z, perm = _get_dihedron_bond_key_name(mod_sets, k, l, m, j, i, j)
                            v = _permute_dihed_data(v, perm)
                            mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                            if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                    elif i == n:
                        if j == l:
                            key = (k,l,m,n)
                            mod_sets[key].add("y")
                            if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                        elif j == m:
                            key = (k,l,m,n)
                            mod_sets[key].add("c")
                            if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                    elif m is None:
                        if j == k:
                            key = (k,l,i,n)
                            mod_sets[key] = mod_sets.get(key, set()) | v | {"x"}
                            if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                        elif j == l:
                            key = (k,l,i,n)
                            mod_sets[key] = mod_sets.get(key, set()) | v | {"b"}
                            if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                        else:
                            key, z, perm = _get_dihedron_bond_key_name(mod_sets, k, l, i, j, i, j)
                            v = _permute_dihed_data(v, perm)
                            mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                            if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                    elif n is None:
                        if j in (k,l,m):
                            key, z, perm = _get_dihedron_bond_key_name(mod_sets, k, l, m, i, i, j)
                            v = _permute_dihed_data(v, perm)
                            mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                            if validate: _validate_dihed_triangulation(mod_sets, key, internals, z)
                    if key is not None:
                        if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                else:
                    if (i, j, None, None) not in mod_sets:
                        mod_sets[(i, j, None, None)] = {"a"}
                dihed_sets = mod_sets
        elif len(coord) == 3:
            i,j,k = coord
            C = i,j,k
            A, sA = canonicalize_internal((i,k,j), return_sign=True)
            B, sB = canonicalize_internal((j,i,k), return_sign=True)
            if C in tri_sets:
                tri_sets[C].add("C")
            elif A in tri_sets:
                tri_sets[A].add("A")
            elif B in tri_sets:
                tri_sets[B].add("B")
            elif (A[0],A[2], None) in tri_sets:
                if i < j:
                    tri_sets[C] = tri_sets.get(C, set()) | {"a" if i < k else "b", "C"}
                else:
                    tri_sets[B] = tri_sets.get(B, set()) | {"a" if j < k else "b", "C"}
            elif (B[0],B[2], None) in tri_sets:
                if j < k:
                    tri_sets[A] = tri_sets.get(A, set()) | {"b" if i < j else "a", "C"}
                else:
                    tri_sets[C] = tri_sets.get(C, set()) | {"b" if i < k else "a", "C"}
            elif (C[0],C[2], None) in tri_sets:
                if i < k:
                    tri_sets[A] = tri_sets.get(A, set()) | {"a" if i < j else "b", "C"}
                else:
                    tri_sets[B] = tri_sets.get(B, set()) | {"a" if j < k else "b", "C"}

            if create_dihedra:
                mod_sets = dihed_sets.copy()
                for (a, l, m, n), v in dihed_sets.items():
                    key = None
                    if m is None:
                        if i == a:
                            if j == l:
                                key = (a, l, k, n)
                                mod_sets[key] = mod_sets.get(key, set()) | v | {"X"}
                                if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                            elif k == l:
                                key = (a, l, j, n)
                                mod_sets[key] = mod_sets.get(key, set()) | v | {"A"}
                                if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                            else:
                                key, z, perm = _get_dihedron_angle_key_name(mod_sets, a,l,j,k, i, j, k)
                                v = _permute_dihed_data(v, perm)
                                mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                                if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                        elif i == l:
                            if j == a:
                                key = (a, l, k, n)
                                mod_sets[key] = mod_sets.get(key, set()) | v | {"B1"}
                                if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                            elif k == a:
                                key = (a, l, j, n)
                                mod_sets[key] = mod_sets.get(key, set()) | v | {"A"}
                                if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                            else:
                                key, z, perm = _get_dihedron_angle_key_name(mod_sets, a,l,j,k, i, j, k)
                                v = _permute_dihed_data(v, perm)
                                mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                                if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                        elif j == a:
                            if k == l:
                                key = (a, l, i, n)
                                mod_sets[key] = mod_sets.get(key, set()) | v | {"B1"}
                                if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                            else:
                                key, z, perm = _get_dihedron_angle_key_name(mod_sets, a,l,i,k, i, j, k)
                                v = _permute_dihed_data(v, perm)
                                mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                        elif j == l:
                            if k == a:
                                key = (a, l, i, n)
                                mod_sets[key] = mod_sets.get(key, set()) | v | {"X"}
                                if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                            else:
                                key, z, perm = _get_dihedron_angle_key_name(mod_sets, a,l,i,k, i, j, k)
                                v = _permute_dihed_data(v, perm)
                                mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                                if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                        elif k in {a,l}:
                            key, z, perm = _get_dihedron_angle_key_name(mod_sets, a,l,i,j, i, j, k)
                            v = _permute_dihed_data(v, perm)
                            mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                            if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                    elif n is None:
                        C1, s = canonicalize_internal((a, l, m), return_sign=True)
                        if C == C1:
                            key = (a, l, m, n)
                            mod_sets[key].add("X")
                            if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                        elif A == C1: # i,k,j == (a,l,m)
                            key = (a, l, m, n)
                            mod_sets[key].add("A" if (sA * s) > 0 else "B1")
                            if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                        elif B == C1: # k,i,j == (a,l,m)
                            key = (a, l, m, n)
                            mod_sets[key].add("B1" if (sB * s) > 0 else "A")
                            if validate: _validate_dihed_triangulation(mod_sets, key, internals)
                        else:
                            if i in (a,l,m):
                                if j in (a,l,m):
                                    key, z, perm = _get_dihedron_angle_key_name(mod_sets, a, l, m, k, i, j, k)
                                    v = _permute_dihed_data(v, perm)
                                    mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                                    if validate: _validate_dihed_triangulation(mod_sets, key, internals, (a, l, m, n))
                                elif k in (a,l,m):
                                    key, z, perm = _get_dihedron_angle_key_name(mod_sets, a, l, m, j, i, j, k)
                                    v = _permute_dihed_data(v, perm)
                                    mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                                    if validate: _validate_dihed_triangulation(mod_sets, key, internals, (a, l, m, n))
                            elif j in (a,l,m) and k in (a,l,m):
                                key, z, perm = _get_dihedron_angle_key_name(mod_sets, a, l, m, i, i, j, k)
                                # u = v
                                v = _permute_dihed_data(v, perm)
                                # print("???", u, v, perm, z)
                                mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                                if validate: _validate_dihed_triangulation(mod_sets, key, internals, (a, l, m, n))
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
                            C1 = canonicalize_internal((x, y, z))
                            A1 = canonicalize_internal((x, z, y))
                            B1 = canonicalize_internal((y, x, z))
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
                        if validate: _validate_dihed_triangulation(mod_sets, key, internals, (a, l, m, n))
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
                    if validate: _validate_dihed_triangulation(mod_sets, key, internals, coord)
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
                    if validate: _validate_dihed_triangulation(mod_sets, key, internals, coord)
                elif skey == tuple(sorted([a, l, m, n])):
                    key, z, perm = _get_dihedron_dihed_key_name(mod_sets, a, l, m, n, *coord)
                    v = _permute_dihed_data(v, perm)
                    mod_sets[key] = mod_sets.get(key, set()) | v | {z}
                    if validate: _validate_dihed_triangulation(mod_sets, key, internals, coord)
            dihed_sets = mod_sets
        #
        # for (a, l, m, n),v in dihed_sets.items():
        #     if m is None and n is not None:
        #         raise ValueError(coord)

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
                for k,v in dihed_sets.items():
                    for i in range(4):
                        t = nput.dihedron_triangle(v, i)
                        if nput.triangle_is_complete(t):
                            inds = np.unique(np.concatenate([x for x in [t.a, t.b, t.c] if x is not None]))
                            if all(p not in tri_sets for p in itertools.permutations(inds)):
                                raise ValueError(f"dihedron has triangle {inds}:{t} but triangulation didn't find it")
    return tri_sets, dihed_sets
def get_triangulation_internals(
    triangulation:tuple[dict[tuple[int, int, int], nput.TriangleData], dict[tuple[int, int, int, int], nput.DihedralTetrahedronData]]
):
    tri_sets, dihed_sets = triangulation
    return itut.delete_duplicates(
            v
            for tv in [tri_sets, dihed_sets]
            for t in tv.values()
            for v in t if v is not None
        )

def _merge_shapes(new_shapes, old_shapes, perms, perm_invs, prop_func,
                  in_place=False,
                  merge_strategy='both'):
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
                            y = canonicalize_internal([pi[i] for i in x])
                            d2[prop_func(y)["name"]] = val
                    uv_dict = uv._asdict()
                    requires_merge = False
                    for name,val in d2.items():
                        val2 = uv_dict[name]
                        if val != val2:
                            if not (
                                isinstance(val, tuple) and isinstance(val2, tuple)
                                and canonicalize_internal(val) == canonicalize_internal(val2)
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
    if triangulation_internals is None:
        triangulation_internals = [canonicalize_internal(c) for c in get_triangulation_internals(triangulation)]
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


# def extend_triangles_and_dihedrons(triangulation:tuple[dict[Tuple[int],collections.namedtuple], dict[Tuple[int],collections.namedtuple]],
#                                    new_internals,
#                                    prune_incomplete=True
#                                    ):
#     tri_sets, dihed_sets = triangulation
#     new_dists = [i for i in new_internals if len(i) == 2]
#     new_angles = [i for i in new_internals if len(i) == 3]
#     new_diheds = [i for i in new_internals if len(i) == 4]
#
#     updated_triangles = {}
#     updated_dihedrons = {}
#
#     use_angles = set()
#     for t,tri in tri_sets:
#         t0 = tri
#         updated = False
#         for i,j in new_dists:
#             try:
#                 x = t.index(i)
#             except IndexError:
#                 continue
#             try:
#                 y = t.index(j)
#             except IndexError:
#                 continue
#             if y < x:
#                 x,y = y,x
#                 i,j = j,i
#             if (x,y) == (0, 1):
#                 if tri.a is None:
#                     updated = True
#                     tri = tri._replace(a=(i,j))
#             elif (x,y) == (0,2):
#                 if tri.c is None:
#                     updated = True
#                     tri = tri._replace(c=(i,j))
#             else:
#                 if tri.b is None:
#                     updated = True
#                     tri = tri._replace(b=(i,j))
#
#         for a in new_angles:
#             if a in use_angles: continue
#             i,j,k = a
#             try:
#                 x = t.index(i)
#             except IndexError:
#                 continue
#             try:
#                 y = t.index(j)
#             except IndexError:
#                 continue
#             try:
#                 z = t.index(k)
#             except IndexError:
#                 continue
#             use_angles.add(a)
#             if z < x:
#                 x,y,z = z,y,x
#                 i,j,k = k,j,i
#             if (x,y,z) == (0, 1, 2):
#                 if tri.C is None:
#                     updated = True
#                     tri = tri._replace(C=(i,j,k))
#             elif (x,y,z) == (0, 2, 1):
#                 if tri.A is None:
#                     updated = True
#                     tri = tri._replace(A=(i,j,k))
#             else:
#                 if tri.B is None:
#                     updated = True
#                     tri = tri._replace(B=(i,j,k))
#
#         if updated:
#             tri_sets[t] = tri
#             updated_triangles[t] = (t0, tri)
#
#     for d, dihed in dihed_sets:
#         d0 = dihed
#         updated = False
#         for i, j in new_dists:
#             try:
#                 x = d.index(i)
#             except IndexError:
#                 continue
#             try:
#                 y = d.index(j)
#             except IndexError:
#                 continue
#             if y < x:
#                 x, y = y, x
#                 i, j = j, i
#             mod_pos = ...
#             if (x, y) == (0, 1):
#                 if tri.a is None:
#                     updated = True
#                     tri = tri._replace(a=(i, j))
#             elif (x, y) == (0, 2):
#                 if tri.c is None:
#                     updated = True
#                     tri = tri._replace(c=(i, j))
#             else:
#                 if tri.b is None:
#                     updated = True
#                     tri = tri._replace(b=(i, j))
#
#         for a in new_angles:
#             if a in use_angles: continue
#             i, j, k = a
#             try:
#                 x = t.index(i)
#             except IndexError:
#                 continue
#             try:
#                 y = t.index(j)
#             except IndexError:
#                 continue
#             try:
#                 z = t.index(k)
#             except IndexError:
#                 continue
#             use_angles.add(a)
#             if z < x:
#                 x, y, z = z, y, x
#                 i, j, k = k, j, i
#             if (x, y, z) == (0, 1, 2):
#                 if tri.C is None:
#                     updated = True
#                     tri = tri._replace(C=(i, j, k))
#             elif (x, y, z) == (0, 2, 1):
#                 if tri.A is None:
#                     updated = True
#                     tri = tri._replace(A=(i, j, k))
#             else:
#                 if tri.B is None:
#                     updated = True
#                     tri = tri._replace(B=(i, j, k))
#
#         if updated:
#             tri_sets[t] = tri
#             updated_triangles[t] = (t0, tri)
#     return (tri_sets, dihed_sets), (updated_triangles, updated_dihedrons)

def _triangle_conversion_function(inds, tri, coord):
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
                                  disallowed_conversions=None):
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
                                           raise_on_missing=False,
                                           completion_handler=completion_handler,
                                           disallowed_conversions=disallowed_conversions,
                                           cache=cache)

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
                             verbose=False,
                             missing_val='raise'):
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
    for target_coord in targets:
        if verbose: print("======>", target_coord)
        if canonicalize:
            target_coord = canonicalize_internal(target_coord)
        idx = find_internal(internals, target_coord, missing_val=None, canonicalize=False, indices=indices)
        if verbose: print("  idx:", idx)
        if idx is not None:
            def convert(internal_list, idx=idx):
                internal_list = np.asanyarray(internal_list)
                return internal_list[..., idx]
            conversions.append(convert)
            if include_shapes: shapes.append(idx)
            continue

        conv = None
        tri = None
        dihed = None
        n = len(target_coord)
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

        if conv is None and n in {2, 3, 4}:
            for a, v in dihedrals.items():
                dihed = v
                completion_handler = None
                if (
                        allow_recursive_completions
                        and all(t in a for t in target_coord)
                ):
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

        if verbose: print(" conv:", conv)
        if conv is None:
            if dev.str_is(missing_val, "raise"):
                raise ValueError(f"can't find conversion for {target_coord} from {internals}")
            else:
                convertable = False
                conversions.append(missing_val)
                if include_shapes: shapes.append(None)
        else:
            # prep conversion based on internal indices
            if tri is not None:
                if prep_conversions:
                    args = {
                        k: find_internal(internals, v, missing_val=missing_val, indices=indices)
                            for k, v in tri._asdict().items()
                        if v is not None
                    }
                    def convert(internal_list, args=args, conv=conv,  **kwargs):
                        internal_list = np.asanyarray(internal_list)
                        subtri = nput.make_triangle(
                            **{k:internal_list[..., i] for k,i in args.items()}
                        )
                        return conv(subtri)
                    convert.__name__ = 'convert_' + conv.__name__
                else:
                    convert = True
                if include_shapes: shapes.append(tri)
            else:
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
                        internal_list = np.asanyarray(internal_list)
                        subargs = {k:s*internal_list[..., i] for k,(i,s) in args.items()}
                        subdihed = nput.make_dihedron(**subargs)
                        return conv(subdihed)
                    convert.__name__ = 'convert_' + conv.__name__
                else:
                    convert = True
                if include_shapes: shapes.append(dihed)
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
    for coord in internals:
        for c in itertools.combinations(coord, 2):
            yield canonicalize_internal(c)

_dihed_check_sets = []
def _get_dihedron_checks():
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
    if len(_dihed_check_sets) == 0:
        for k,v in nput.dihedron_property_specifiers().items():
            _dihedron_index_props[v["coord"]] = v
    return _dihedron_index_props

def _dihedron_completable(k, dihed_data, known_atom_graph, max_comps=5):
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
                if len(connectivity_graph[g[-1]]) > 4
            ] # if only 4 we can't actually connect to anything else
            yield groups
def construct_atom_connection_graph_from_triangulation(internals, tris, dihedrons):
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
                                       build_conversion=True,
                                       max_ordering_passes=1,
                                       **conversion_options
                                       ):
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
                print(np.array(zm))
                yield zm, find_internal_conversion(internals, targets,
                                                    triangles_and_dihedrons=triangles_and_dihedrons,
                                                    **conversion_options)
            else:
                yield zm
    else:
        for zm_list in itertools.product(*zm_generators):
            if build_conversion:
                convs = [
                    find_internal_conversion(internals, extract_zmatrix_internals(zm),
                                             triangles_and_dihedrons=triangles_and_dihedrons,
                                             **conversion_options)
                    for zm in zm_list
                ]
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
    # invalidate cache information for `dihedron_property_function`
    # from `find_internal_conversion`
    conversion_cache = cache.setdefault('disallowed_conversions', {})
    _, shape_index_map = inverse_triangulation
    for dihed in conversion_cache.keys():
        inds = shape_index_map[dihed]
        if any(all(d) in inds for d in extra_dists):
            conversion_cache[dihed] = set()
    return
def get_non_redundant_internals(internals, triangles_and_dihedrons=None,
                                check_distances=True, check_angles=True, check_dihedrals=True,
                                return_indices=False, natoms=None, validate=False):

    all_dists = []
    dist_pos = [n for n,i in enumerate(internals) if len(i) == 2]
    coords = [internals[n] for n in dist_pos]
    triangulation = get_internal_triangles_and_dihedrons(coords)
    inverse_triangulation = tuple({v:k for k,v in shapes.items()} for shapes in triangulation)
    rem_pos = [n for n,i in enumerate(internals) if len(i) > 2]
    rem = [internals[n] for n in rem_pos]

    dist_set = list(sorted(set(_enumerate_dists(internals))))

    graph = InternalCoordinateGraph(coords, triangles_and_dihedrons=triangulation)
    conversions = graph.find_conversions(dist_set)

    # dist_set, (conversions, shapes) = get_internal_distance_conversion(
    #     coords,
    #     triangles_and_dihedrons=triangulation,
    #     include_shapes=True,
    #     return_conversions=True,
    #     dist_set=dist_set,
    #     missing_val=None
    # )

    for d,c in zip(dist_set, conversions):
        if c is not None:
            if d not in all_dists:
                all_dists.append(d)

    natoms = max(max(i) for i in internals) + 1
    rigid, (_, local_rank), stress = uniquely_rigid(all_dists, 3, natoms=natoms, return_components=True)
    if rigid:
        return coords

    if stress is None:
        stress_rank = None
    else:
        _, stress_rank = stress

    added_coords = []
    incl_coords = []
    for n,c in enumerate(rem):
        with graph.checkpoint() as checkpoint:
            print(c)
            # print("???", len(graph._unreachable))
            new_coords = graph.add_internals([c])
            print("  >", len(graph._conversions), len(graph._unreachable), len(new_coords))
            print("  >", len(graph.internals))

            checks = graph.find_conversions(dist_set)
            added_dists = [i for i,c in zip(dist_set, checks) if c is not None and i not in all_dists]
            print("  =", len(added_dists))
            print(all_dists + added_dists)

            if len(added_dists) > 0:
                test_dists = all_dists + added_dists
                rigid, (_, test_rank), stress = uniquely_rigid(test_dists, 3, natoms=natoms, return_components=True)

                extend = True
                if rigid:
                    # coords = test
                    break
                elif stress is not None:
                    _, test_rank = stress
                    extend = stress_rank is None or test_rank > stress_rank
                    if extend:
                        stress_rank = test_rank
                else:
                    extend = test_rank > local_rank
                    if extend:
                        local_rank = test_rank
                if extend:
                    print(added_dists)
                    print(">>>", stress_rank, local_rank)
                    checkpoint.reset = False
                    added_coords.append(c)
                    all_dists = test_dists
                    incl_coords.append(n)

    # print(rigid)
    coords = graph.internals
    # import pprint
    # pprint.pprint(coords)
    # raise Exception(len(coords), len(added_coords))

    all_pos = dist_pos + [rem_pos[i] for i in incl_coords]
    dropped_pos = np.setdiff1d(np.arange(len(internals)), all_pos)
    rem_diff = np.setdiff1d(np.arange(len(rem)), rem_pos)
    dropped_coords = [rem[i] for i in rem_diff]
    return (coords, (dropped_coords, dropped_pos)), triangles_and_dihedrons


def get_non_redundant_internals_old_incremental(internals, triangles_and_dihedrons=None,
                                check_distances=True, check_angles=True, check_dihedrals=True,
                                return_indices=False, natoms=None, validate=False):

    all_dists = []
    dist_pos = [n for n,i in enumerate(internals) if len(i) == 2]
    coords = [internals[n] for n in dist_pos]
    triangulation = get_internal_triangles_and_dihedrons(coords)
    inverse_triangulation = tuple({v:k for k,v in shapes.items()} for shapes in triangulation)
    rem_pos = [n for n,i in enumerate(internals) if len(i) > 2]
    rem = [internals[n] for n in rem_pos]

    dist_set = list(sorted(set(_enumerate_dists(internals))))

    # graph = InternalCoordinateGraph(coords, triangles_and_dihedrons=triangulation)
    # conversions = graph.find_conversions(dist_set)

    dist_set, (conversions, shapes) = get_internal_distance_conversion(
        coords,
        triangles_and_dihedrons=triangulation,
        include_shapes=True,
        return_conversions=True,
        dist_set=dist_set,
        missing_val=None
    )

    for d,c in zip(dist_set, conversions):
        if c is not None:
            if d not in all_dists:
                all_dists.append(d)

    natoms = max(max(i) for i in internals) + 1
    rigid, (_, local_rank), stress = uniquely_rigid(all_dists, 3, natoms=natoms, return_components=True)
    if rigid:
        return coords

    if stress is None:
        stress_rank = None
    else:
        _, stress_rank = stress


    distance_map = {
        d:s
        for d,s,c in zip(dist_set, shapes, conversions)
        if c is None
    }
    extra_dists = []
    cache = {}
    for c in rem:
        test = coords + [c]
        added_dists, new_map, new_triangulation = get_distance_addition_edits(coords,
                                                                              distance_map,
                                                                              [c],
                                                                              triangulation,
                                                                              cache=cache)
        added_dists = [i for i in added_dists if i not in all_dists]

        if len(added_dists) > 0:
            test_dists = all_dists + added_dists
            rigid, (_, test_rank), stress = uniquely_rigid(test_dists, 3, natoms=natoms, return_components=True)

            extend = True
            if rigid:
                # coords = test
                break
            elif stress is not None:
                _, test_rank = stress
                extend = stress_rank is None or test_rank > stress_rank
                if extend:
                    stress_rank = test_rank
            else:
                extend = test_rank > local_rank
                if extend:
                    local_rank = test_rank
            if extend:
                print(">>>", stress_rank, local_rank)
                triangulation = new_triangulation
                distance_map = new_map
                coords = test
                new_additions = [i for i in added_dists if i not in coords]
                extra_dists = extra_dists + new_additions
                all_dists = test_dists
                # inverse_triangulation = tuple({v:k for k,v in shapes.items()} for shapes in triangulation)
                # _update_cache_based_on_dists(new_additions, cache, inverse_triangulation)
                for d in added_dists:
                    del distance_map[d]

    print(rigid)
    import pprint
    pprint.pprint(coords)
    raise Exception(len(coords))

def get_non_redundant_internals_pruned(internals, triangles_and_dihedrons=None,
                                check_distances=True, check_angles=True, check_dihedrals=True,
                                return_indices=False, natoms=None, validate=False):
    #TODO: supply multiple rigidity methods
    if triangles_and_dihedrons is None:
        triangles_and_dihedrons = get_internal_triangles_and_dihedrons(internals)
    for thing in triangles_and_dihedrons:
        for d,v in thing.items():
            for vv in v:
                if vv is not None and not isinstance(vv, tuple) and all(nput.is_int(vvv) for vvv in vv):
                    raise ValueError(d, v)

    dist_set, (conversions, shapes) = get_internal_distance_conversion(
        internals,
        triangles_and_dihedrons=triangles_and_dihedrons,
        include_shapes=True,
        return_conversions=True,
        missing_val=None
    )
    distance_map = {
        d:s
        for d,s,c in zip(dist_set, shapes, conversions)
        if c is not None
    }
    dropped_coordinates = []
    dropped_indices = []
    internals = list(internals)
    pops = 0
    m = len(internals)
    skip_dists = not check_distances
    skip_angles = not check_angles
    skip_dihedrals = not check_dihedrals
    rem_edges = list(dist_set)
    if natoms is None:
        natoms = np.max(dist_set) + 1
    for i,c in enumerate(list(reversed(internals))):
        n = len(c)
        if skip_dists and n == 2: continue
        if skip_angles and n == 3: continue
        if skip_dihedrals and n == 4: continue
        if i - pops == 0:
            subinternals = internals[:-1]
        else:
            subinternals = internals[:-(i-pops+1)] + internals[-(i-pops):]
        removed_distances, new_map, new_triangulation = get_distance_prune_edits(internals,
                                                                                 distance_map,
                                                                                 c,
                                                                                 triangles_and_dihedrons)
        likely_rigid = len(removed_distances) == 0
        test_edges = list(rem_edges)
        for d in removed_distances:
            try:
                test_edges.remove(d)
            except ValueError:
                ...
        if not likely_rigid:
            # we'll do a statistical rigidity check
            likely_rigid = uniquely_rigid(
                rem_edges,
                3,
                natoms=natoms
            )
        print(f"{i!s:>3} {c!s:<16} {likely_rigid!s:<5}")
        if likely_rigid:
            rem_edges = test_edges
            pops += 1
            dropped_coordinates.append(c)
            if return_indices:
                dropped_indices.append(m - i - 1)
            triangles_and_dihedrons = new_triangulation
            internals = subinternals
            if validate:
                dists1 = get_internal_distance_conversion(internals, triangles_and_dihedrons=triangles_and_dihedrons, return_conversions=True, missing_val=None)
                dists2 = get_internal_distance_conversion(internals, return_conversions=True, missing_val=None)
                c1 = any(d is None for d in dists1)
                c2 = any(d is None for d in dists2)
                if c1 or c2:
                    raise ValueError(c1, c2)
            distance_map = new_map

    raise Exception(m, len(internals), len(dropped_coordinates))
    if return_indices:
        dropped_coordinates = (dropped_coordinates, dropped_indices)

    return (internals, dropped_coordinates), triangles_and_dihedrons

def get_distance_prune_edits(internals,
                             distance_map: dict[tuple[int, int], nput.TriangleData | nput.DihedralTetrahedronData],
                             target_internals,
                             triangles_and_dihedrons,
                             inverse_triangulation=None,
                             only_subchecks=False,
                             full_retriangulation=True,
                             verbose=False,
                             validate=False):
    if nput.is_int(target_internals[0]):
        target_internals = [target_internals]

    if inverse_triangulation is None:
        inverse_triangulation = [
            {v:k for k,v in tri.items()}
            for tri in triangles_and_dihedrons
        ]

    # for t,v in triangles_and_dihedrons[0].items():
    #     if any(vv is not None and not isinstance(vv, tuple) for vv in v):
    #         raise ValueError(t, v)
    if verbose:
        print("pruned:", target_internals)
    if full_retriangulation:
        pruned_internals = [i for i in internals if i not in target_internals]
        tri_set, dihed_set = get_internal_triangles_and_dihedrons(pruned_internals)
        check_distances = list(distance_map.keys())
    else:
        core_atoms, (mod_tri, mod_di), (rem_tri, rem_di) = update_triangulation(
            triangles_and_dihedrons,
            [],
            target_internals,
            return_split=True,
            triangulation_internals=internals
        )

        if only_subchecks:
            check_distances = []
            for (i,j), shape in distance_map.items():
                if nput.is_int(shape):
                    if (len(internals) <= shape or internals[shape] != (i,j)):
                        print(">>>", (i,j), shape, internals[shape])
                        check_distances.append((i, j))
                else:
                    block, target, perms, perm_invs, prop_func = (
                        (inverse_triangulation[0], rem_tri, _tri_perms, _tri_perm_inv, nput.triangle_property_specifiers)
                            if isinstance(shape, nput.TriangleData) else
                        (inverse_triangulation[1], rem_di, _dihedron_perms, _dihedron_perm_inv, nput.dihedron_property_specifiers)
                    )
                    key = block[shape]
                    for p, pi in zip(perms, perm_invs):
                        k2 = tuple(key[i] for i in p)
                        test_shape = target.get(k2)
                        if test_shape is not None:
                            if shape is test_shape:
                                break
                            elif key == k2:
                                test_keys = {k:v for k,v in test_shape._asdict().items() if v is not None}
                                t_dict = {k: v for k, v in shape._asdict().items() if v is not None}
                                if set(t_dict.keys()) == set(test_keys.keys()):
                                    break
                            else:
                                # check if they're equivalent under the perm
                                test_keys = {k:v for k,v in test_shape._asdict().items() if v is not None}
                                t_dict = {k: v for k, v in shape._asdict().items() if v is not None}
                                d2 = {}
                                if len(t_dict) == len(test_keys):
                                    for term, val in t_dict.items():
                                        x = prop_func(term)["coord"]
                                        y = canonicalize_internal([pi[i] for i in x])
                                        d2[prop_func(y)["name"]] = val
                                    if set(d2.keys()) == set(test_keys.keys()):
                                        break
                    else:
                        check_distances.append((i, j))
        else:
            check_distances = list(distance_map.keys())

        tri_set = {
            k: v
            for ts in merge_triangle_sets(mod_tri, rem_tri, merge_strategy='old')
            for k, v in ts.items()
        }
        dihed_set = {
            k: v
            for ts in merge_triangle_sets(mod_di, rem_di, merge_strategy='old')
            for k, v in ts.items()
        }

        if verbose:
            ts1, ds1 = triangles_and_dihedrons
            import hashlib
            print("initial:", len(ts1),
                  len([t for t in ts1.values() if nput.triangle_is_complete(t)]),
                  len(ds1),
                  len([t for t in ds1.values() if nput.dihedron_is_complete(t)]),
                  hashlib.sha256(str({k:ts1[k] for k in sorted(ts1.keys())}).encode()).hexdigest(),
                  hashlib.sha256(str({k:ds1[k] for k in sorted(ds1.keys())}).encode()).hexdigest()
                  )
            print("final:", len(tri_set),
                  len([t for t in tri_set.values() if nput.triangle_is_complete(t)]),
                  len(dihed_set),
                  len([t for t in dihed_set.values() if nput.dihedron_is_complete(t)]),
                  hashlib.sha256(str({k:tri_set[k] for k in sorted(tri_set.keys())}).encode()).hexdigest(),
                  hashlib.sha256(str({k:dihed_set[k] for k in sorted(dihed_set.keys())}).encode()).hexdigest())
        if validate:
            ts1, ds1 = triangles_and_dihedrons
            initial_tri = len([t for t in ts1.values() if nput.triangle_is_complete(t)])
            initial_di = len([t for t in ds1.values() if nput.dihedron_is_complete(t)])
            final_tri = len([t for t in tri_set.values() if nput.triangle_is_complete(t)])
            final_di = len([t for t in dihed_set.values() if nput.dihedron_is_complete(t)])
            if initial_tri < final_tri or initial_di < final_di:
                for k, t in tri_set.items():
                    v1 = ts1.get(k)
                    if (
                            v1 is not None
                            and (not nput.triangle_is_complete(t))
                            and nput.triangle_is_complete(v1)
                    ):
                        print(v1)
                        print(t)
                for k, t in dihed_set.items():
                    v1 = ds1.get(k)
                    if v1 is not None:
                        if (
                                (not nput.dihedron_is_complete(t))
                                and nput.dihedron_is_complete(v1)
                        ):
                            print(v1)
                            print(t)
                    elif nput.dihedron_is_complete(t):
                        for k2 in itertools.permutations(k):
                            if k2 in ds1 and k2 in dihed_set:
                                raise ValueError(f"duplicated: {k} and {k2}")
                        print(k)
                        print(t)


                raise ValueError(initial_tri, initial_di, final_tri, final_di)

    new_triangulation = (tri_set, dihed_set)
    if verbose:
        print("checks:", check_distances)
    if len(check_distances) > 0:
        pruned_internals = [i for i in internals if i not in target_internals]
        new_map = distance_map.copy()
        # (shapes, conversions1) = find_internal_conversion(internals, check_distances,
        #                                                  triangles_and_dihedrons=triangles_and_dihedrons,
        #                                                  missing_val=None,
        #                                                  allow_completion=False,
        #                                                  return_conversions=True,
        #                                                  include_shapes=True,
        #                                                  verbose=True)
        if verbose:
            import hashlib
            print(hashlib.sha256(str(sorted(pruned_internals)).encode()).hexdigest())
        (conversions, shapes) = find_internal_conversion(pruned_internals, check_distances,
                                                         triangles_and_dihedrons=new_triangulation,
                                                         missing_val=None,
                                                         allow_completion=False,
                                                         return_conversions=True,
                                                         prep_conversions=False,
                                                         include_shapes=True,
                                                         verbose=False)
        dead_dists = []
        for d,s,c in zip(check_distances, shapes, conversions):
            if c is None:
                dead_dists.append(d)
            else:
                new_map[d] = s
        # dead_old = []
        # for d,s,c in zip(check_distances, shapes, conversions1):
        #     if c is None:
        #         dead_old.append(d)
        if verbose:
            print("incomplete:", dead_dists, [c.__name__ if c is not None else c for c in conversions])

        # if target_internals[0] == (1, 9, 8, 21):
        #     raise Exception(...)
        return dead_dists, new_map, new_triangulation
    else:
        # if target_internals[0] == (1, 9, 8, 21):
        #     raise Exception(...)
        return [], distance_map, new_triangulation

def get_distance_addition_edits(internals,
                                distance_map: dict[tuple[int, int], nput.TriangleData | nput.DihedralTetrahedronData],
                                target_internals,
                                triangles_and_dihedrons,
                                inverse_triangulation=None,
                                only_subchecks=False,
                                full_retriangulation=True,
                                verbose=False,
                                cache=None,
                                validate=False):
    #TODO: currently a direct copy, clean this up
    if nput.is_int(target_internals[0]):
        target_internals = [target_internals]

    if inverse_triangulation is None:
        inverse_triangulation = [
            {v:k for k,v in tri.items()}
            for tri in triangles_and_dihedrons
        ]

    # for t,v in triangles_and_dihedrons[0].items():
    #     if any(vv is not None and not isinstance(vv, tuple) for vv in v):
    #         raise ValueError(t, v)
    if verbose:
        print("added:", target_internals)
    if full_retriangulation:
        extended_internals = internals + target_internals
        tri_set, dihed_set = get_internal_triangles_and_dihedrons(extended_internals)
        check_distances = list(distance_map.keys())
    else:
        core_atoms, (mod_tri, mod_di), (rem_tri, rem_di) = update_triangulation(
            triangles_and_dihedrons,
            target_internals,
            [],
            return_split=True,
            triangulation_internals=internals
        )

        if only_subchecks:
            check_distances = []
            for (i,j), shape in distance_map.items():
                if nput.is_int(shape):
                    if (len(internals) <= shape or internals[shape] != (i,j)):
                        check_distances.append((i, j))
                else:
                    block, target, perms, perm_invs, prop_func = (
                        (inverse_triangulation[0], rem_tri, _tri_perms, _tri_perm_inv, nput.triangle_property_specifiers)
                            if isinstance(shape, nput.TriangleData) else
                        (inverse_triangulation[1], rem_di, _dihedron_perms, _dihedron_perm_inv, nput.dihedron_property_specifiers)
                    )
                    key = block[shape]
                    for p, pi in zip(perms, perm_invs):
                        k2 = tuple(key[i] for i in p)
                        test_shape = target.get(k2)
                        if test_shape is not None:
                            if shape is test_shape:
                                break
                            elif key == k2:
                                test_keys = {k:v for k,v in test_shape._asdict().items() if v is not None}
                                t_dict = {k: v for k, v in shape._asdict().items() if v is not None}
                                if set(t_dict.keys()) == set(test_keys.keys()):
                                    break
                            else:
                                # check if they're equivalent under the perm
                                test_keys = {k:v for k,v in test_shape._asdict().items() if v is not None}
                                t_dict = {k: v for k, v in shape._asdict().items() if v is not None}
                                d2 = {}
                                if len(t_dict) == len(test_keys):
                                    for term, val in t_dict.items():
                                        x = prop_func(term)["coord"]
                                        y = canonicalize_internal([pi[i] for i in x])
                                        d2[prop_func(y)["name"]] = val
                                    if set(d2.keys()) == set(test_keys.keys()):
                                        break
                    else:
                        check_distances.append((i, j))
        else:
            check_distances = list(distance_map.keys())

        tri_set = {
            k: v
            for ts in merge_triangle_sets(mod_tri, rem_tri, merge_strategy='old')
            for k, v in ts.items()
        }
        dihed_set = {
            k: v
            for ts in merge_triangle_sets(mod_di, rem_di, merge_strategy='old')
            for k, v in ts.items()
        }

        if verbose:
            ts1, ds1 = triangles_and_dihedrons
            import hashlib
            print("initial:", len(ts1),
                  len([t for t in ts1.values() if nput.triangle_is_complete(t)]),
                  len(ds1),
                  len([t for t in ds1.values() if nput.dihedron_is_complete(t)]),
                  hashlib.sha256(str({k:ts1[k] for k in sorted(ts1.keys())}).encode()).hexdigest(),
                  hashlib.sha256(str({k:ds1[k] for k in sorted(ds1.keys())}).encode()).hexdigest()
                  )
            print("final:", len(tri_set),
                  len([t for t in tri_set.values() if nput.triangle_is_complete(t)]),
                  len(dihed_set),
                  len([t for t in dihed_set.values() if nput.dihedron_is_complete(t)]),
                  hashlib.sha256(str({k:tri_set[k] for k in sorted(tri_set.keys())}).encode()).hexdigest(),
                  hashlib.sha256(str({k:dihed_set[k] for k in sorted(dihed_set.keys())}).encode()).hexdigest())
        if validate:
            ts1, ds1 = triangles_and_dihedrons
            initial_tri = len([t for t in ts1.values() if nput.triangle_is_complete(t)])
            initial_di = len([t for t in ds1.values() if nput.dihedron_is_complete(t)])
            final_tri = len([t for t in tri_set.values() if nput.triangle_is_complete(t)])
            final_di = len([t for t in dihed_set.values() if nput.dihedron_is_complete(t)])
            if initial_tri < final_tri or initial_di < final_di:
                for k, t in tri_set.items():
                    v1 = ts1.get(k)
                    if (
                            v1 is not None
                            and (not nput.triangle_is_complete(t))
                            and nput.triangle_is_complete(v1)
                    ):
                        print(v1)
                        print(t)
                for k, t in dihed_set.items():
                    v1 = ds1.get(k)
                    if v1 is not None:
                        if (
                                (not nput.dihedron_is_complete(t))
                                and nput.dihedron_is_complete(v1)
                        ):
                            print(v1)
                            print(t)
                    elif nput.dihedron_is_complete(t):
                        for k2 in itertools.permutations(k):
                            if k2 in ds1 and k2 in dihed_set:
                                raise ValueError(f"duplicated: {k} and {k2}")
                        print(k)
                        print(t)


                raise ValueError(initial_tri, initial_di, final_tri, final_di)

    new_triangulation = (tri_set, dihed_set)
    if verbose:
        print("checks:", check_distances)
    if len(check_distances) > 0:
        extended_internals = internals + target_internals
        new_map = distance_map.copy()
        # (shapes, conversions1) = find_internal_conversion(internals, check_distances,
        #                                                  triangles_and_dihedrons=triangles_and_dihedrons,
        #                                                  missing_val=None,
        #                                                  allow_completion=False,
        #                                                  return_conversions=True,
        #                                                  include_shapes=True,
        #                                                  verbose=True)
        conversions, shapes, completions = find_internal_conversion(extended_internals, check_distances,
                                                                    triangles_and_dihedrons=new_triangulation,
                                                                    missing_val=None,
                                                                    allow_completion=True,
                                                                    return_conversions=True,
                                                                    prep_conversions=False,
                                                                    include_shapes=True,
                                                                    update_triangles_and_dihedrons=False,
                                                                    return_completions=True,
                                                                    # cache=cache,
                                                                    verbose=False)
        print(completions)
        live_dists = []
        for d,s,c in zip(check_distances, shapes, conversions):
            if c is not None:
                live_dists.append(d)
            else:
                new_map[d] = s
        # dead_old = []
        # for d,s,c in zip(check_distances, shapes, conversions1):
        #     if c is None:
        #         dead_old.append(d)
        if verbose:
            print("complete:", live_dists, [c.__name__ if c is not None else c for c in conversions])

        # if target_internals[0] == (1, 9, 8, 21):
        #     raise Exception(...)
        return live_dists, new_map, new_triangulation
    else:
        # if target_internals[0] == (1, 9, 8, 21):
        #     raise Exception(...)
        return [], distance_map, new_triangulation

class InternalCoordinateGraph:
    """
    A graph mapping out the connections between a set of atoms based on the given set of internals
    """
    __slots__ = ['internals', 'atoms', 'triangulation', '_completion_cache', '_conversions', '_unreachable']
    def __init__(self, internals, atoms=None, triangles_and_dihedrons=None):
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
        # we map the unreachable set to the possible completions that _could_ have completed it
        # this way when we add an internal, we can check to see if there are any previously unreachable
        # coordinates that need an update, and then if those need an upd

    def enumerate_matching_dihedrons(self, target_coord):
        for i,d in self.triangulation[1].items():
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
    def find_conversions(self,
                         target_internals,
                         unconvertable_atoms=None,
                         allow_recursive_completions=False,
                         verbose=False,
                         **etc):
        initial_set = target_internals

        target_internals = [
            i for i in target_internals
            if i not in self._conversions
               and i not in self._unreachable
        ]
        # if verbose:
        #     print("..."*30)
        #     print(target_internals)
        #     print(self.internals)
        #     print(self.triangulation[0])
        if len(target_internals) > 0:
            expanded_internals = list(itut.delete_duplicates(
                canonicalize_internal(k) for k in (
                list(self.internals)
                + list(self._conversions.keys())
            )))
            conversions, shapes = find_internal_conversion(expanded_internals,
                                                           target_internals,
                                                           # triangles_and_dihedrons=self.triangulation,
                                                           include_shapes=True,
                                                           allow_completion=True,
                                                           return_conversions=True,
                                                           allow_recursive_completions=allow_recursive_completions,
                                                           missing_val=None,
                                                           cache=self._completion_cache,
                                                           **etc)

            # this gives us the basic completeable set of coordinates
            self._conversions.update({i:c for i,c in zip(target_internals, conversions) if c is not None})

            # if a coordinate _wasn't_ possible to complete, we want to
            # walk through the possible completions by going through
            # the current triangulation and finding the coordinates we are missing
            incomplete = [i for i,c in zip(target_internals, conversions) if c is None]
            cache = self._completion_cache.setdefault('trie_expansions', {})
            spec_data = nput.dihedron_property_specifiers()
            if unconvertable_atoms is None:
                unconvertable_atoms = set()
            if not allow_recursive_completions:
                for target in incomplete:
                    # print("???", target)
                    if target in self._conversions: continue # this can be completed within the loop
                    if target not in self._unreachable: self._unreachable[target] = []
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
                            for k in kl:
                                if k not in key_map:
                                    key_map[k] = canonicalize_internal([d[i] for i in spec_data[k]['coord']])
                                coord_keys.append(key_map[k])
                            pref_coords.append(coord_keys)
                        self._unreachable[target] = sorted({tuple(t) for t in itertools.chain(self._unreachable[target], pref_coords)}, key=len)
                        for coord_keys in pref_coords:
                            if any(k in self._unreachable for k in coord_keys): continue
                            if any(len(set(k) & unconvertable_atoms) == len(k) for k in coord_keys): continue
                            unconverted_k = [k for k in coord_keys if k not in self._conversions]
                            if len(unconverted_k) > 0:
                                #TODO: expand the graph _before_ applying this search
                                #      to speed up retrieval? -> already cached in `_conversions`
                                #TODO: try a BFS? would give the minimal conversion at the cost of more code
                                subs = self.find_conversions(unconverted_k, unconvertable_atoms=unconvertable_atoms, **etc)
                                for s,k in zip(subs, unconverted_k):
                                    if s is not None and k in self._unreachable: # can be removed inside the loop
                                        del self._unreachable[k]
                                if all(s is not None for s in subs):
                                    self._conversions[target] = (coord_keys, kl, possible_conversions[kl])
                                    break
                        unconvertable_atoms.update(d)
        return [self._conversions.get(i) for i in initial_set]

    class GraphCheckpoint:
        def __init__(self, g, reset=True):
            self.graph = g
            self.reset = reset
            self._internals = None
            self._triangulation = None
            self._conversions = None
            self._unreachable = None
        def __enter__(self):
            self._internals = self.graph.internals.copy()
            self._triangulation = tuple(t.copy() for t in self.graph.triangulation)
            self._conversions = self.graph._conversions.copy()
            self._unreachable = self.graph._unreachable.copy()
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            if self.reset:
                self.graph.internals = self._internals
                self.graph.triangulation = self._triangulation
                self.graph._conversions = self._conversions
                self.graph._unreachable = self._unreachable

    def checkpoint(self):
        return self.GraphCheckpoint(self)

    def add_internals(self, internals):
        # update triangulation
        # determine which distances could have been impacted by this change
        # check if any of those are completable
        if nput.is_int(internals[0]):
            internals = [internals]
        internals = [i for i in internals if i not in self.internals]
        self.internals = list(self.internals) + list(internals)
        #TODO: use a proper update
        self.triangulation = get_internal_triangles_and_dihedrons(self.internals)

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
        raise NotImplementedError("need to cache more information to remove an element")
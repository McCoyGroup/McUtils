import abc

import numpy as np
from .. import Devutils as dev
from .. import Numputils as nput

from .Internals import canonicalize_internal

__all__ = [
    "prune_internal_coordinates"
]

class InternalCoordinatePruner:
    def pruning_iterator(self, coords, *args, **kwargs):
        """
        **LLM Docstring**

        Yield every candidate coordinate in its original order.

        The value sent back after each yield is accepted but ignored. Subclasses override this generator to choose a more selective candidate order or to react to the caller's keep/reject decision.

        :param coords: Candidate internal coordinates.
        :type coords: collections.abc.Sequence
        :param args: Unused positional extension arguments.
        :type args: tuple
        :param kwargs: Unused keyword extension arguments.
        :type kwargs: dict
        :return: Generator yielding each coordinate once.
        :rtype: collections.abc.Generator
        """
        for p in range(len(coords)):
            kept = yield coords[p]
    def prune_coordinates(self, coords, *args, base_internals=None, check_rigidity=True, natoms=None, **kwargs):
        """
        **LLM Docstring**

        Drive a pruning generator while optionally rejecting coordinates that do not increase the nonredundant internal-coordinate rank.

        If no base set is supplied, all two-atom coordinates are made mandatory and only longer coordinates are tested. With `check_rigidity=False`, the method simply appends every coordinate yielded by `pruning_iterator`. Otherwise, each candidate is passed to `NonredundantInternalsChecker.add_internal`; the resulting keep flag is sent back into the generator and only accepted coordinates are appended. The current implementation prints each test and raises `ValueError` if the checker reports that the system has become rigid.

        :param coords: Candidate coordinate specifications.
        :type coords: collections.abc.Sequence[tuple[int, ...]]
        :param args: Positional arguments forwarded to `pruning_iterator`.
        :type args: tuple
        :param base_internals: Coordinates that are always retained. Defaults to the stretches extracted from `coords`.
        :type base_internals: collections.abc.Sequence | None
        :param check_rigidity: Whether to use `NonredundantInternalsChecker` to decide which yielded coordinates are retained.
        :type check_rigidity: bool
        :param natoms: Number of atoms; inferred as one plus the largest coordinate index when omitted.
        :type natoms: int | None
        :param kwargs: Keyword arguments forwarded to `pruning_iterator`.
        :type kwargs: dict
        :return: Base coordinates followed by the accepted candidates.
        :rtype: list
        :raises ValueError: If the checker reports a rigid coordinate set.
        """
        from .Internals import NonredundantInternalsChecker
        if natoms is None:
            natoms = max(max(i) for i in coords) + 1
        if base_internals is None:
            base_internals = [c for c in coords if len(c) == 2]
            coords = [c for c in coords if len(c) > 2]
        coord_set = list(base_internals)
        iterator = self.pruning_iterator(coords, *args, base_internals=coord_set, **kwargs)
        if not check_rigidity:
            return coord_set + list(iterator)
        else:
            checker = NonredundantInternalsChecker(base_internals, natoms)
            kept = None
            for _ in range(len(coords)):
                try:
                    new = iterator.send(kept)
                except StopIteration:
                    break
                kept, (rigid, local_rank, stress_rank) = checker.add_internal(new)
                print(new, kept, rigid)
                if rigid: raise ValueError(new)
                if kept: coord_set.append(new)
                if rigid: break

            return coord_set

class UniqueInternalCoordinatePruner(InternalCoordinatePruner):
    def pruning_iterator(cls, coords):
        """
        **LLM Docstring**

        Yield the first occurrence of each canonical internal coordinate.

        Every candidate is normalized with `canonicalize_internal`; reverse-equivalent coordinates therefore share one cache entry. The value sent back by the caller is ignored. Although the generator's terminal return value is the original `coords` object, normal iteration exposes only the yielded unique coordinates.

        :param coords: Candidate internal coordinates.
        :type coords: collections.abc.Iterable
        :return: Generator yielding canonical coordinates not seen previously.
        :rtype: collections.abc.Generator
        """
        _coords = []
        _cache = set()
        for x in coords:
            x = canonicalize_internal(x)
            if x not in _cache:
                yield x
                _cache.add(x)
        return coords

class GeometricInternalCoordinatePruner(InternalCoordinatePruner):

    def pruning_iterator(cls,
                         coords, b_matrix,
                         max_coords=None,
                         base_internals=None,
                         small_value_cutoff=1e-4,
                         max_contrib_cutoff=5e-2,
                         return_positions=False
                         ):
        """
        **LLM Docstring**

        Yield a subset of coordinates whose B-matrix columns remain linearly independent above an SVD threshold.

        The routine starts from up to `max_coords` leading candidates, shrinking that prefix until its smallest singular value exceeds `small_value_cutoff`. The caller can reject any initially yielded coordinate by sending `False`. Remaining coordinates are tested one at a time by appending their B-matrix column; candidates are yielded only when the augmented matrix stays above the singular-value cutoff, and accepted candidates update the working subspace. `max_contrib_cutoff` is currently unused.

        :param coords: Candidate coordinate specifications, excluding any mandatory `base_internals`.
        :type coords: collections.abc.Sequence
        :param b_matrix: Full B matrix with coordinate columns, or callable `(positions, coordinates) -> columns`.
        :type b_matrix: np.ndarray | collections.abc.Callable
        :param max_coords: Maximum number of retained coordinates. Defaults to the smaller of `len(coords)` and one less than the B-matrix row count.
        :type max_coords: int | None
        :param base_internals: Mandatory coordinates whose columns seed the working subspace.
        :type base_internals: collections.abc.Sequence | None
        :param small_value_cutoff: Minimum allowed smallest singular value.
        :type small_value_cutoff: float
        :param max_contrib_cutoff: Reserved option; not used by the implementation.
        :type max_contrib_cutoff: float
        :param return_positions: Whether the generator's terminal value includes retained positions as well as coordinates.
        :type return_positions: bool
        :return: Generator yielding testable coordinates; its `StopIteration.value` is either the retained coordinate list or `(positions, coordinates)`.
        :rtype: collections.abc.Generator
        """
        if base_internals is None:
            base_internals = []
        if not nput.is_numeric_array_like(b_matrix):
            b_matrix_generator = b_matrix
        else:
            b_matrix_generator = lambda pos, coords: b_matrix[:, pos]

        if max_coords is None:
            max_coords = min([
                b_matrix_generator([0], [coords[0]]).shape[0] - 1,
                len(coords)
            ])
        subspace = max_coords

        if len(base_internals) > 0:
            base_b = b_matrix_generator(np.arange(len(base_internals)), base_internals)
        else:
            base_b = None

        sub_b = b_matrix_generator(np.arange(subspace), coords[:subspace])
        if base_b is not None:
            sub_b = np.concatenate([base_b, sub_b], axis=1)
        _, s, Q = np.linalg.svd(sub_b)
        min_comp = np.min(s)
        while min_comp < small_value_cutoff and subspace > 0:
            subspace = subspace - 1
            sub_b = sub_b[:, :-1]
            _, s, Q = np.linalg.svd(sub_b)
            min_comp = np.min(s)


        coords = list(base_internals) + list(coords)
        coord_pos = np.arange(subspace + len(base_internals))
        test_pos = []
        for p in coord_pos[len(base_internals):]:
            kept = yield coords[p]
            if kept or (kept is None): test_pos.append(p)

        coord_pos = np.array(test_pos)
        rem_coords = np.setdiff1d(np.arange(len(coords)), coord_pos)
        for test_coord in rem_coords:
            b_vec = b_matrix_generator((test_coord,), [coords[test_coord]])
            b_test = np.concatenate([sub_b, b_vec], axis=1)
            min_comp = np.min(np.linalg.svd(b_test)[1])
            if min_comp > small_value_cutoff:
                kept = yield coords[test_coord]
                if kept or (kept is None):
                    coord_pos = np.concatenate([coord_pos, [test_coord]])
                    if len(coord_pos) >= max_coords:
                        break
                    sub_b = b_test

        coords = [coords[p] for p in coord_pos]
        if return_positions:
            return coord_pos, coords
        else:
            return coords


pruner_dispatch = dev.OptionsMethodDispatch(
    {
        'unique':UniqueInternalCoordinatePruner,
        'basic':InternalCoordinatePruner,
        'b_matrix':GeometricInternalCoordinatePruner
    }
)


def prune_internal_coordinates(coords, *args, method='basic', **kwargs):
    """
    **LLM Docstring**

    Resolve a pruning strategy and apply it to a coordinate collection.

    `method` is dispatched through `pruner_dispatch`: `"basic"` yields candidates unchanged, `"unique"` canonicalizes and removes duplicates, and `"b_matrix"` performs geometric/SVD pruning. Options registered with the dispatch entry are merged with `kwargs`, with explicit keyword arguments taking precedence.

    :param coords: Coordinate specifications to prune.
    :type coords: collections.abc.Sequence
    :param args: Additional positional arguments passed to the selected pruner.
    :type args: tuple
    :param method: Registered pruning method or other value understood by `OptionsMethodDispatch.resolve`.
    :type method: str
    :param kwargs: Options passed to the selected pruner's `prune_coordinates` method.
    :type kwargs: dict
    :return: Coordinates retained by the selected pruning strategy.
    :rtype: list
    """
    pruner:'type[InternalCoordinatePruner]'
    pruner, subopts = pruner_dispatch.resolve(method)
    return pruner().prune_coordinates(coords, *args, **dict(subopts, **kwargs))
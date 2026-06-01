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
        for p in range(len(coords)):
            kept = yield coords[p]
    def prune_coordinates(self, coords, *args, base_internals=None, check_rigidity=True, natoms=None, **kwargs):
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
    pruner:'type[InternalCoordinatePruner]'
    pruner, subopts = pruner_dispatch.resolve(method)
    return pruner().prune_coordinates(coords, *args, **dict(subopts, **kwargs))

import numpy as np
from .Internals import canonicalize_internal, permute_internals
# from ..Numputils import permutation_cycles

__all__ = [
    "get_internal_permutation_symmetry_matrices",
    "symmetrize_internals"
]

def get_internal_permutation_symmetry_matrices(internals, permutations):
    map = {
        canonicalize_internal(i): n
        for n, i in enumerate(internals)
    }
    internals = list(map.keys())
    basis = []
    for p in permutations:
        subbasis = [
            [0] * len(internals)
            for _ in range(len(internals))
        ]
        p_coords = internals
        while len(p_coords) > 0:
            new_coords = []
            new_ints = permute_internals(p_coords, p, canonicalize=True)
            for old,new in zip(p_coords, new_ints):
                j = map[old]
                if new == old:
                    subbasis[j][j] = 1
                else:
                    if (i := map.get(new)) is None:
                        i = len(internals)
                        map[new] = i
                        internals.append(new)
                        new_coords.append(new)
                        for b in subbasis[j:]:
                            b.append(0)
                        subbasis.append([0] * len(internals))
                    subbasis[j][i] = 1 if len(old) < 3 else -1
            p_coords = new_coords
        basis.append(subbasis)

    #TODO: handle newly add internals, we need their permutation symmetries too

    full_basis = []
    for subbasis in basis:
        if len(subbasis) < len(internals):
            subbasis.extend(
                [[0]*len(internals)]
                * (len(internals) - len(subbasis))
            )

        full_basis.append([
            s + [0]*(len(internals) - len(s))
            for s in subbasis
        ])

    return np.moveaxis(np.array(full_basis, dtype=int), 0, -1), internals

def symmetrize_internals(point_group, internals,
                         cartesians=None, *,
                         as_characters=True,
                         normalize=False,
                         perms=None,
                         ops=None):
    storage = []
    symm = lambda p: (
        storage.extend(get_internal_permutation_symmetry_matrices(internals, p)),
        storage[0]
    )[1]
    if perms is None and cartesians is None:
        raise ValueError("either Cartesians or explicit set of atom permutations required")
    symm_coeffs = point_group.symmetrized_coordinate_coefficients(
                                            cartesians,
                                            permutation_basis=symm,
                                            as_characters=as_characters,
                                            normalize=normalize,
                                            perms=perms,
                                            ops=ops
                                            )
    return symm_coeffs, storage[1]
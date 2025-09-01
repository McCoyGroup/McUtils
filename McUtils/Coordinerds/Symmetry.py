
import numpy as np
from .Internals import canonicalize_internal, permute_internals, coordinate_indices
from .. import Numputils as nput

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
    p_coords = internals
    while len(p_coords) > 0:
        new_coords = []
        for n,p in enumerate(permutations):
            if len(basis) < n+1:
                subbasis = [
                    [0] * len(internals)
                    for _ in range(len(internals))
                ]
                basis.append(subbasis) # take advantage of mutability
            else:
                subbasis = basis[n]
            new_ints = permute_internals(p_coords, p, canonicalize=True)
            for old,new in zip(p_coords, new_ints):
                j = map[old]
                if new == old:
                    subbasis[j][j] = 1
                elif (
                        len(new) == 4
                        and new[0] == old[0] and new[3] == old[3]
                        and new[1] == old[2] and new[2] == old[1]
                ):
                    subbasis[j][j] = 1
                else:
                    if len(old) < 4:
                        sign = 1
                    else:
                        sign = 1

                    if (i := map.get(new)) is None:
                        if len(new) == 4:
                            for o,k in map.items():
                                if (
                                        len(o) == 4
                                        and new[0] == o[0] and o[3] == o[3]
                                        and new[1] == o[2] and new[2] == o[1]
                                ):
                                    i = k
                                    # sign *= -1
                        if i is None:
                            for sb in basis:
                                sb.append([0] * (len(internals)))
                                for b in sb: b.append(0)
                            i = len(internals)
                            map[new] = i
                            internals.append(new)
                            new_coords.append(new)
                    subbasis[j][i] = sign
        p_coords = new_coords

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

def symmetrize_internals(point_group,
                         internals,
                         cartesians=None,
                         *,
                         as_characters=True,
                         normalize=None,
                         perms=None,
                         return_expansions=False,
                         return_base_expansion=False,
                         ops=None):
    symm = lambda p: get_internal_permutation_symmetry_matrices(internals, p)
    if cartesians is not None:
        cartesians = np.asanyarray(cartesians)
        if np.issubdtype(cartesians.dtype, np.integer):
            # we'll support permutations as Cartesians even if it feels like a bad idea
            # it's just so convenient...
            atom_list = coordinate_indices(internals)
            nats = len(atom_list)
            if cartesians.shape != (nats, 3):
                if nats == 3:
                    # we'll check to see if we have permutations...
                    test = np.sort(cartesians, axis=0)
                    if np.sum(np.abs(test - np.arange(nats)[:, np.newaxis])) < 1e-8:
                        perms, cartesians = cartesians, None
            elif cartesians.shape[-1] == nats:
                perms, cartesians = cartesians, None
        # if cartesians.shape ==
    if perms is None and cartesians is None:
        raise ValueError("either Cartesians or explicit set of atom permutations required")

    if return_expansions and cartesians is None:
        raise ValueError("Cartesians are required to return coordinate expansions")

    if normalize is None:
        normalize = return_expansions

    coeffs, full_basis = point_group.symmetrized_coordinate_coefficients(
        cartesians,
        permutation_basis=symm,
        as_characters=as_characters,
        normalize=normalize,
        perms=perms,
        ops=ops
    )

    res = (coeffs, full_basis)
    if return_expansions:
        if return_expansions is True: return_expansions = 1
        exp, inv = nput.internal_coordinate_tensors(cartesians, full_basis,
                                                    return_inverse=True,
                                                    order=return_expansions
                                                    )

        coeff_inv = [
            c.T
                if (normalize is not False and (as_characters or normalize)) else
            np.linalg.pinv(c)
            for c in coeffs
        ]

        expansions = [
            (
                [np.dot(exp[0], c)] + nput.tensor_reexpand(exp[1:], [c]),
                nput.tensor_reexpand([ci], inv)
            )
            for c,ci in zip(coeffs, coeff_inv)
        ]

        res = res + (expansions,)
        if return_base_expansion:
            res = res + ((exp, inv),)

    return res

    # return symm_coeffs, storage[1]
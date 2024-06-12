
import itertools, numpy as np
from .VectorOps import vec_tensordot, vec_outer
from ..Combinatorics import IntegerPartitioner, UniquePermutations

__all__ = [
    "nca_op_deriv",
    "tensordot_deriv",
    "tensorprod_deriv",
    "scalarprod_deriv",
    "matinv_deriv",
    "matdet_deriv",
    "scalarinv_deriv",
    "tensor_reexpand"
]

def get_nca_shifts(order, k):
    permute_pos = np.arange(k)
    ncombs = np.math.comb(order, k)
    shifts = np.broadcast_to(np.arange(order)[np.newaxis], (ncombs, order)).copy()
    for i,pos in enumerate(itertools.combinations(range(order), r=k)):
        shifts[i, pos] = permute_pos
    return shifts
def apply_nca_op(op, order, k, A_expansion, B_expansion, deriv_axis, a, b, contract, shared, identical):
    s = order - k
    if s >= len(A_expansion) or k >= len(B_expansion):
        return 0

    A = A_expansion[s]
    B = B_expansion[k]
    for T in [A, B]:
        if (
                (isinstance(T, (int, np.integer, float, np.floating)) and T == 0)
            or (T.shape == () and T == 0)
        ):
            return 0
    if shared is None:
        shared = 0
    if contract: # axes disappear, so we just account for the shifts
        axes = [[x+s for x in a], [x+k for x in b]]
    else: # axes appeared, so we need to include those in the product
          # we _forced_ axes to be at the end of the arrays since it was too hard
          # to keep track of them otherwise...
          # actually I guess I could have put the derivative axes at the end...
          # and then the axes would never change...but that has other complications
        axes = [
            [shared + i for i in range(s)] + [x+s for x in a],
            [shared + i for i in range(k)] + [x+k for x in b]
        ]

    if shared == 0:
        base = op(A, B, axes=axes)
    else:
        base = op(A, B, axes=axes, shared=shared)

    # next we need to move all of the derivative axes in the second tensor to the beginning
    # so we can symmetrize
    d = deriv_axis + s
    for i in range(k):
        base = np.moveaxis(base, d+i, shared)
    part = [x for x in reversed(sorted([s,k])) if x > 0]
    if len(part) > 1:
        base = nca_symmetrize(base, part, shared=shared, identical=identical)
    return base
def nca_op_order_deriv(op, order, A_expansion, B_expansion, deriv_axis, a, b, contract, shared, identical):
    full = None
    for k in range(order+1):
        term = apply_nca_op(op, order, k, A_expansion, B_expansion, deriv_axis, a, b, contract, shared, identical)
        if full is None:
            full = term
        else:
            full = full + term
    return full
def nca_op_deriv(op,
                 A_expansion,
                 B_expansion,
                 order,
                 axes,
                 contract,
                 shared=None,
                 identical=False
                 ):
    A_expansion = [np.asanyarray(A) for A in A_expansion]
    B_expansion = [np.asanyarray(B) for B in B_expansion]

    a_ax, b_ax = axes
    if isinstance(a_ax, int): a_ax = [a_ax]
    if isinstance(b_ax, int): b_ax = [b_ax]
    a_ax = [ a if a >= 0 else A_expansion[0].ndim + a for a in a_ax ]
    b_ax = [ b if b >= 0 else B_expansion[0].ndim + b for b in b_ax ]

    if contract: # the derivative axis will always be at nA + 1 - num_contracted - the shared axes
        deriv_axis = A_expansion[0].ndim - len(a_ax)
    else:
        # we require that the outer product be ordered
        # so we now which axes to move around
        a_ax = np.sort(a_ax)
        a_dim = A_expansion[0].ndim
        if np.any(a_ax != np.arange(a_dim - len(a_ax), a_dim)):
            raise ValueError("axes {} must be the final axes of A".format(a_ax))
        b_ax = np.sort(b_ax)
        b_dim = B_expansion[0].ndim
        if np.any(b_ax != np.arange(b_dim - len(b_ax), b_dim)):
            raise ValueError("axes {} must be the final axes of B".format(b_ax))
        deriv_axis = a_dim

    if isinstance(order, int):
        order = list(range(1, order+1))

    # if shared is not None:
    #     deriv_axis = deriv_axis - shared

    derivs = [
        nca_op_order_deriv(op, o, A_expansion, B_expansion, deriv_axis, a_ax, b_ax, contract, shared,
                           identical
                           )
        for o in order
    ]

    return derivs

def tensordot_deriv(A_expansion, B_expansion,
                    order,
                    axes=None,
                    shared=None,
                    identical=False
                    ):

    if axes is None: axes = [-1, 0]
    if shared is not None:
        op = vec_tensordot
    else:
        op = lambda a,b,axes=None,shared=None:np.tensordot(a, b, axes=axes)

    return [op(A_expansion[0], B_expansion[0], axes=axes, shared=shared)] + nca_op_deriv(op,
                                                                                         A_expansion, B_expansion,
                                                                                         order,
                                                                                         axes=axes,
                                                                                         contract=True,
                                                                                         shared=shared,
                                                                                         identical=identical
                                                                                         )

def tensorprod_deriv(
        A_expansion, B_expansion,
        order,
        axes=None,
        identical=False
):
    if axes is None:
        axes = [-1, -1]
    a_ax, b_ax = axes
    if isinstance(a_ax, int): a_ax = [a_ax]
    if isinstance(b_ax, int): b_ax = [b_ax]

    shared = A_expansion[0].ndim - len(a_ax)
    if len(a_ax) == 0:
        # scalar product
        return scalarprod_deriv(A_expansion, B_expansion, order, identical=identical)

    op = lambda left, right, axes=None, shared=None: vec_outer(left, right, axes=axes)
    return [op(A_expansion[0], B_expansion[0], axes=axes, shared=shared)] + nca_op_deriv(op,
                                                                                         A_expansion, B_expansion,
                                                                                         order,
                                                                                         axes=[a_ax, b_ax],
                                                                                         contract=False,
                                                                                         shared=shared,
                                                                                         identical=identical
                                                                                         )

def scalarprod_deriv(s_expansion, A_expansion,
                     order,
                     identical=False
                     ):
    subexpansion = tensorprod_deriv(s_expansion[1:], A_expansion, order - 1, identical=identical)
    rem_expansion = [s_expansion[0] * A for A in A_expansion[:order]]
    return [rem_expansion[0]] + [x + y for x, y in zip(subexpansion, rem_expansion[1:])]


def matinv_deriv(forward_expansion, order):
    B = np.linalg.inv(forward_expansion[0])
    reverse_expansion = [B]
    for o in range(1, order):
        new_B = -tensordot_deriv(forward_expansion, reverse_expansion + [0], o)[-1]
        # need to multiply enough inverses in too now
        for _ in range(new_B.ndim):
            new_B = np.tensordot(B, new_B, axes=[1, -1])
        reverse_expansion = reverse_expansion + [new_B]
    return reverse_expansion

def matdet_deriv(forward_expansion, order):
    reverse_expansion = matinv_deriv(forward_expansion, order)
    tr_inner_exp = tensorprod_deriv(reverse_expansion, forward_expansion[1:],
                                 order-1,
                                 axes=[1, 1]
                                 )
    det_exp = [np.linalg.det(forward_expansion[0])]
    for o in range(0, order-1):
        det_exp = det_exp + [scalarprod_deriv(det_exp, tr_inner_exp, o)[-1]]
    return [det_exp[0]] + [np.trace(a, axis1=-2, axis2=-1) for a in det_exp[1:]]

def scalarinv_deriv(scalar_expansion, order):
    s = scalar_expansion[0]
    scalar_exp = [1/s]
    for o in range(1, order):
        term = 0
        for parts in IntegerPartitioner.partitions(o):
            l = len(parts[0])
            scaling = ((-1)**l) * np.math.factorial(l) / (s**(l+1))
            term += sum(scaling*nca_partition_prod(p, scalar_expansion) for p in parts)
        scalar_exp.append(term)
    return scalar_exp

def nca_partition_terms(partition):
    """
    Computes the number of permutations for the non-commutative operation
    corresponding to the given partition

    :param cls:
    :param partition:
    :return:
    """
    _, counts = np.unique(partition, return_counts=True)

    # compute the reduced multinomial coefficient in stable (enough) form
    multinomial_num = np.flip(np.arange(1, 1 + np.sum(partition)))
    multinomial_denum = np.concatenate([
        np.arange(1, 1 + j)
        for j in partition
    ])
    multi_redux_terms = np.concatenate([
        np.arange(1, 1 + j)
        for j in counts
    ])
    full_denom = np.flip(np.sort(np.concatenate([multinomial_denum, multi_redux_terms])))
    numl = len(multinomial_num)
    denl = len(full_denom)
    if numl > denl:
        full_denom = np.concatenate([full_denom, np.ones(numl - denl, dtype=full_denom.dtype)])
    elif denl > numl:
        multinomial_num = np.concatenate([multinomial_num, np.ones(denl - numl, dtype=multinomial_num.dtype)])

    return np.prod(multinomial_num / full_denom)

def nca_symmetrize(tensor, partition, shared=None, identical=True):
    perm_counter = len(partition)
    perm_idx = []  # to establish the set of necessary permutations to make things symmetric
    for i in partition:
        if (not identical) or i > 1:
            perm_idx.extend([perm_counter] * i)
            perm_counter -= 1
        else:
            perm_idx.append(perm_counter)

    # sometimes we overcount, so we factor that out here
    perm_inds, _ = UniquePermutations(perm_idx).permutations(return_indices=True)
    if identical:
        nterms = nca_partition_terms(partition)
        overcount = len(perm_inds) / nterms
        tensor = tensor / overcount

    if shared is None:
        perm_inds = [
            list(p) + list(range(len(p), tensor.ndim))
            for p in perm_inds
        ]
    else:
        l = list(range(shared))
        perm_inds = [
            l + [shared + pp for pp in p] + list(range(len(p), tensor.ndim))
            for p in perm_inds
        ]

    return sum(
        tensor.transpose(p)
        for p in perm_inds
    )

def nca_partition_dot(partition, A_expansion, B_expansion, axes=None, shared=None, symmetrize=True):
    if axes is None:
        axes = [-1, 0]
    if len(B_expansion) <= len(partition) - 1:
        return 0
    B = B_expansion[len(partition) - 1]
    if isinstance(B, (int, float, np.integer, np.floating)) and B == 0:
        return 0
    a_ax, b_ax = [[x] if isinstance(x, (int, np.integer)) else x for x in axes]
    b_ax = [B.ndim + b if b < 0 else b for b in b_ax]
    for i in partition:
        if len(A_expansion) <= i - 1:
            return 0
        A = A_expansion[i - 1]
        if isinstance(A, (int, float, np.integer, np.floating)) and A == 0:
            return 0
        if shared is None:
            B = np.tensordot(A, B, axes=[a_ax, b_ax])
        else:
            B = vec_tensordot(A, B, axes=[a_ax, b_ax], shared=shared)
        b_ax = [min(B.ndim - 1, b + A.ndim - 1) for b in b_ax]

    if symmetrize:
        B = nca_symmetrize(B, partition, shared=shared)
    return B

def nca_partition_prod(partition, A_expansion, shared=None, symmetrize=True):
    B = 1
    for i in partition:
        if len(A_expansion) <= i - 1:
            return 0
        A = A_expansion[i - 1]
        if isinstance(A, (int, float, np.integer, np.floating)) and A == 0:
            return 0
        if shared is not None:
            axes = [list(range(shared, A.ndim)), list(range(shared, B.ndim))]
        else:
            axes = [list(range(A.ndim)), list(range(B.ndim))]
        B = vec_outer(A, B, axes=axes)

    if symmetrize:
        B = nca_symmetrize(B, partition, shared=shared)
    return B

def tensor_reexpand(derivs, vals, order=None, axes=None):
    terms = []
    if order is None:
        order = len(vals)

    for o in range(1, order+1):
        term = sum(
            nca_partition_dot(p, derivs, vals, axes=axes)
            for parts in IntegerPartitioner.partitions(o)
            for p in parts
        )
        terms.append(term)

    return terms
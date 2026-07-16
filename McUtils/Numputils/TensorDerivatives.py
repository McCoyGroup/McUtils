import collections
import itertools, numpy as np, math
# import uuid

from .. import Devutils as dev

from . import PermutationOps as perms, vec_tensordiag, identity_tensors
from . import VectorOps as vec_ops
from . import SetOps as set_ops
from .Misc import is_numeric, is_zero, is_numeric_array_like
from .Options import Options

__all__ = [
    "nca_op_deriv",
    "tensordot_deriv",
    "tensorprod_deriv",
    "scalarprod_deriv",
    "inverse_transformation",
    "optimizing_transformation",
    "matinv_deriv",
    "matdet_deriv",
    "matsqrt_deriv",
    "mateigh_deriv",
    "scalarinv_deriv",
    "scalarpow_deriv",
    "tensor_reexpand",
    "tensorops_deriv",
    "vec_norm_unit_deriv",
    "vec_angle_deriv",
    "vec_cross_deriv",
    "vec_anglecos_deriv",
    "vec_anglesin_deriv",
    "vec_normal_deriv",
    "vec_dihed_deriv",
    "vec_plane_angle_deriv",
    "shift_expansion",
    "scale_expansion",
    "add_expansions",
    "subtract_expansions",
    "concatenate_expansions",
    "renormalize_transformation",
    "orthogonalize_transformations"
]

# levi_cevita3.__name__ = "levi_cevita3"
# levi_cevita3.__doc__ = """
#     The 3D Levi-Cevita tensor.
#     Used to turn cross products into matmuls
#     """



def get_nca_shifts(order, k):
    """
    **LLM Docstring**

    Enumerate the derivative-axis placements for splitting `order` derivatives
    between the two operands of a binary operation.

    For each way of choosing which `k` of the `order` derivative slots belong to the
    second operand, a shift row is produced; used to line up the derivative axes
    before symmetrization.

    :param order: total derivative order
    :type order: int
    :param k: number of derivatives assigned to the second operand
    :type k: int
    :return: the array of axis-shift rows, one per combination
    :rtype: np.ndarray
    """
    permute_pos = np.arange(k)
    ncombs = math.comb(order, k)
    shifts = np.broadcast_to(np.arange(order)[np.newaxis], (ncombs, order)).copy()
    for i,pos in enumerate(itertools.combinations(range(order), r=k)):
        shifts[i, pos] = permute_pos
    return shifts
def apply_nca_op(op, order, k,
                 A_expansion, B_expansion, deriv_axis,
                 a, b, contract, shared, identical,
                 root_dim=2
                 ):
    """
    **LLM Docstring**

    Compute a single term of the order-`order` derivative of a binary tensor
    operation, in which the second operand contributes `k` derivatives and the first
    `order - k`.

    Applies `op` to the two expansion terms (contracting or outer-producting per
    `contract`), moves the freshly created derivative axes to the front, and (when
    both operands carry derivatives) symmetrizes over them. This is one term of the
    generalized Leibniz rule.

    :param op: the binary operation (e.g. a cleaned `tensordot`/`outer`)
    :type op: Callable
    :param order: total derivative order of the term
    :type order: int
    :param k: number of derivatives taken on the second operand
    :type k: int
    :param A_expansion: expansion of the first operand
    :type A_expansion: list
    :param B_expansion: expansion of the second operand
    :type B_expansion: list
    :param deriv_axis: axis at which the new derivative axes appear
    :type deriv_axis: int
    :param a: contraction/product axes of the first operand
    :type a: list[int]
    :param b: contraction/product axes of the second operand
    :type b: list[int]
    :param contract: whether the operation contracts (vs. outer-products) the axes
    :type contract: bool
    :param shared: number of shared leading batch axes
    :type shared: int | None
    :param identical: whether the two operands are the same expansion
    :type identical: bool
    :param root_dim: number of trailing (non-derivative) core axes
    :type root_dim: int
    :return: the term (or `0` when an operand order is out of range/zero)
    :rtype: np.ndarray | int
    """
    s = order - k
    if s >= len(A_expansion) or k >= len(B_expansion):
        return 0

    A = A_expansion[s]
    B = B_expansion[k]
    for T in [A, B]:
        if (
            is_zero(T)
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
    sa = (A.ndim - len(axes[0]) if contract else A.ndim)
    #TODO: figure out why this wasn't _shared_ since the idea is the same?
    for i in range(k):
        base = np.moveaxis(base, d+i, shared)
    part = [x for x in [s, k] if x > 0]
    if len(part) > 1:
        base = nca_symmetrize(base, part, contract=contract, shared=shared, identical=identical)
    return base
def nca_op_order_deriv(op, order, A_expansion, B_expansion, deriv_axis, a, b, contract, shared, identical):
    """
    **LLM Docstring**

    Assemble the full order-`order` derivative of a binary operation by summing the
    Leibniz terms over all splits of the derivatives between the two operands.

    :param op: the binary operation
    :type op: Callable
    :param order: the derivative order
    :type order: int
    :param A_expansion: expansion of the first operand
    :type A_expansion: list
    :param B_expansion: expansion of the second operand
    :type B_expansion: list
    :param deriv_axis: axis at which the new derivative axes appear
    :type deriv_axis: int
    :param a: contraction/product axes of the first operand
    :type a: list[int]
    :param b: contraction/product axes of the second operand
    :type b: list[int]
    :param contract: whether the operation contracts the axes
    :type contract: bool
    :param shared: number of shared leading batch axes
    :type shared: int | None
    :param identical: whether the two operands are the same expansion
    :type identical: bool
    :return: the order-`order` derivative tensor
    :rtype: np.ndarray | int
    """
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
    """
    **LLM Docstring**

    Compute the derivative expansion of a binary tensor operation (a contraction
    or an outer product) applied to two expansions, via the generalized Leibniz
    rule.

    Normalizes the operand axes, determines where the new derivative axes will
    appear, and sums the Leibniz terms at each requested order. For outer products
    the operated axes are required to be the trailing axes of each operand.

    :param op: the binary operation
    :type op: Callable
    :param A_expansion: expansion of the first operand
    :type A_expansion: list
    :param B_expansion: expansion of the second operand
    :type B_expansion: list
    :param order: derivative order(s) to compute
    :type order: int | list[int]
    :param axes: `(a_axes, b_axes)` operated on
    :type axes: tuple
    :param contract: whether the operation contracts (vs. outer-products) the axes
    :type contract: bool
    :param shared: number of shared leading batch axes
    :type shared: int | None
    :param identical: whether the two operands are the same expansion
    :type identical: bool
    :return: the list of derivative tensors, one per requested order
    :rtype: list
    """
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
        nca_op_order_deriv(op, o, A_expansion, B_expansion, deriv_axis, a_ax, b_ax,
                           contract, shared, identical
                           )
        for o in order
    ]

    return derivs

def _deriv_construct(zero_order_handler, expansion_generator, order):
    """
    **LLM Docstring**

    Assemble a full expansion list from a zeroth-order handler and a generator for
    the higher orders, allowing specific (non-contiguous) orders to be requested.

    The zeroth order is produced by `zero_order_handler`; the positive orders are
    drawn in sequence from `expansion_generator`.

    :param zero_order_handler: callable producing the value (zeroth-order) term
    :type zero_order_handler: Callable
    :param expansion_generator: callable producing the higher-order terms
    :type expansion_generator: Callable
    :param order: the order(s) to produce
    :type order: int | list[int]
    :return: the assembled expansion
    :rtype: list
    """
    if is_numeric(order):
        order = list(range(order+1))
    high_order_expansion = expansion_generator([o for o in order if o > 0])

    # a lot of work to make sure we can do derivatives at a specifically targeted order
    n = 0
    final_expansion = []
    for o in order:
        if o == 0:
            final_expansion.append(
                zero_order_handler()
            )
        else:
            final_expansion.append(high_order_expansion[n])
            n += 1
    return final_expansion

def _clean_vdot(a, b, *, axes, shared=None):
    """
    **LLM Docstring**

    Shared-axis tensor contraction (`vec_tensordot`) that short-circuits to `0`
    when either operand is zero.

    :param a: the first operand
    :type a: np.ndarray | int
    :param b: the second operand
    :type b: np.ndarray | int
    :param axes: the contraction axes
    :type axes: list
    :param shared: number of shared leading batch axes
    :type shared: int | None
    :return: the contraction, or `0`
    :rtype: np.ndarray | int
    """
    return (
        0
            if is_zero(a) or is_zero(b) else
        vec_ops.vec_tensordot(a, b, axes=axes, shared=shared)
    )
def _clean_tdot(a, b, *, axes, shared=None):
    """
    **LLM Docstring**

    Plain tensor contraction (`np.tensordot`) that short-circuits to `0` when
    either operand is zero.

    :param a: the first operand
    :type a: np.ndarray | int
    :param b: the second operand
    :type b: np.ndarray | int
    :param axes: the contraction axes
    :type axes: list
    :param shared: unused (kept for signature parity)
    :type shared: int | None
    :return: the contraction, or `0`
    :rtype: np.ndarray | int
    """
    return (
        0
            if is_zero(a) or is_zero(b) else
        np.tensordot(a, b, axes=axes)
    )
def tensordot_deriv(A_expansion, B_expansion,
                    order,
                    axes=None,
                    shared=None,
                    identical=False
                    ):
    """
    **LLM Docstring**

    Compute the derivative expansion of a tensor contraction between two
    expansions.

    Selects the shared-axis or plain contraction depending on `shared` and builds
    the expansion via the generalized Leibniz rule.

    :param A_expansion: expansion of the first operand
    :type A_expansion: list
    :param B_expansion: expansion of the second operand
    :type B_expansion: list
    :param order: derivative order(s) to compute
    :type order: int | list[int]
    :param axes: the contraction axes (defaults to `[-1, 0]`)
    :type axes: list | None
    :param shared: number of shared leading batch axes
    :type shared: int | None
    :param identical: whether the two operands are the same expansion
    :type identical: bool
    :return: the contracted derivative expansion
    :rtype: list
    """

    if len(A_expansion) == 0 or len(B_expansion) == 0:
        return [0]*((order+1) if is_numeric(order) else len(order))

    if axes is None: axes = [-1, 0]
    if shared is not None and shared > 0:
        base_op = _clean_vdot
    else:
        base_op = _clean_tdot
    op = base_op
    return _deriv_construct(
        lambda : op(A_expansion[0], B_expansion[0], axes=axes, shared=shared),
        lambda ords: nca_op_deriv(op,
                     A_expansion, B_expansion,
                     ords,
                     axes=axes,
                     contract=True,
                     shared=shared,
                     identical=identical
                     ),
        order
    )

def prep_prod_arrays(A_expansion, a_ax):
    """
    **LLM Docstring**

    Move the product axes to the end of each tensor in an expansion, accounting for
    the extra derivative axes carried at each order.

    Used to set up operands for an outer-product derivative so the product axes stay
    in a predictable trailing position.

    :param A_expansion: the expansion to reshape
    :type A_expansion: list
    :param a_ax: the product axes
    :type a_ax: list[int]
    :return: the reshaped expansion
    :rtype: list[np.ndarray]
    """
    _ = []
    for n,a in enumerate(A_expansion):
        a = np.asanyarray(a)
        for x in a_ax:
            x = (a.ndim + x) if x < 0 else (x + n)
            a = np.moveaxis(a, x, -1)
        _.append(a)
    return _
def pre_broadcast_prod(A_expansion, B_expansion, axes):
    """
    **LLM Docstring**

    Prepare two operand expansions for a broadcasted product by moving their
    product axes to the end (via `prep_prod_arrays`).

    This is a partial/work-in-progress helper: it normalizes the axis specifications
    and reorders the operands but does not itself perform the broadcast.

    :param A_expansion: expansion of the first operand
    :type A_expansion: list
    :param B_expansion: expansion of the second operand
    :type B_expansion: list
    :param axes: `(a_axes, b_axes)` product axes
    :type axes: tuple
    :return: None
    :rtype: None
    """

    a_ax, b_ax = axes
    if isinstance(a_ax, int): a_ax = [a_ax]
    if isinstance(b_ax, int): b_ax = [b_ax]

    A_expansion = prep_prod_arrays(A_expansion, a_ax)
    B_expansion = prep_prod_arrays(B_expansion, b_ax)

    expand_dims = ...

def _clean_outer(left, right, *, axes, shared=None):
    """
    **LLM Docstring**

    Outer product (`vec_outer`) of two operands that short-circuits to `0` when
    either is zero.

    :param left: the first operand
    :type left: np.ndarray | int
    :param right: the second operand
    :type right: np.ndarray | int
    :param axes: the product axes
    :type axes: list
    :param shared: unused (kept for signature parity)
    :type shared: int | None
    :return: the outer product, or `0`
    :rtype: np.ndarray | int
    """
    return (
        0
            if is_zero(left) or is_zero(right) else
        vec_ops.vec_outer(left, right, axes=axes, order=0)
    )
def tensorprod_deriv(
        A_expansion, B_expansion,
        order,
        axes=None,
        identical=False
):
    """
    **LLM Docstring**

    Compute the derivative expansion of an outer/tensor product between two
    expansions.

    Resolves the product axes (`'all'` selects every non-shared axis), infers the
    shared batch dimension, and builds the expansion via the generalized Leibniz
    rule with a non-contracting operation.

    :param A_expansion: expansion of the first operand
    :type A_expansion: list
    :param B_expansion: expansion of the second operand
    :type B_expansion: list
    :param order: derivative order(s) to compute
    :type order: int | list[int]
    :param axes: the product axes (defaults to `[-1, -1]`; `'all'` for every axis)
    :type axes: list | str | None
    :param identical: whether the two operands are the same expansion
    :type identical: bool
    :return: the outer-product derivative expansion
    :rtype: list
    """
    if len(A_expansion) == 0 or len(B_expansion) == 0:
        return [0]*((order+1) if is_numeric(order) else len(order))
    if axes is None:
        axes = [-1, -1]
    elif isinstance(axes, str) and axes == 'all':
        axes = [np.arange(A_expansion[0].ndim), np.arange(B_expansion[0].ndim)]
    a_ax, b_ax = axes
    if isinstance(a_ax, int): a_ax = [a_ax]
    if isinstance(b_ax, int): b_ax = [b_ax]
    # a_ax, b_ax = pre_broadcast_prod(A_expansion, B_expansion, axes)

    shared = A_expansion[0].ndim - len(a_ax)
    # if is_numeric(A_expansion[0]) or is_numeric(B_expansion[0]):
    #     # scalar product
    #     return scalarprod_deriv(A_expansion, B_expansion, order, identical=identical)

    A_expansion = [np.asanyarray(a) for a in A_expansion]
    B_expansion = [np.asanyarray(b) for b in B_expansion]
    op = _clean_outer
    return _deriv_construct(
        lambda: op(A_expansion[0], B_expansion[0], axes=axes, shared=shared),
        lambda ords: nca_op_deriv(op,
                                  A_expansion, B_expansion,
                                  ords,
                                  axes=[a_ax, b_ax],
                                  contract=False,
                                  shared=shared,
                                  identical=identical
                                  ),
        order
    )

def _scalar_prod(a, b, axes=None, shared=None):
    """
    **LLM Docstring**

    Multiply a scalar expansion term by a tensor (or two scalars), short-circuiting
    zeros.

    When either operand is a scalar the plain product is used; otherwise the two
    tensors are combined with an outer product over their non-shared axes.

    :param a: the first operand
    :type a: np.ndarray | int
    :param b: the second operand
    :type b: np.ndarray | int
    :param axes: unused (kept for signature parity)
    :type axes: list | None
    :param shared: number of shared leading batch axes
    :type shared: int | None
    :return: the product, or `0`
    :rtype: np.ndarray | int
    """
    if is_numeric(a) or is_numeric(b):
        if is_zero(a) or is_zero(b):
            return 0
        else:
            return a * b
    else:
        if shared is None:
            shared = 0
        return vec_ops.vec_outer(a, b, axes=[list(range(shared, a.ndim)), list(range(shared, b.ndim))], order=0)

def scalarprod_deriv(s_expansion, A_expansion,
                     order,
                     identical=False
                     ):
    """
    **LLM Docstring**

    Compute the derivative expansion of a scalar-times-tensor product.

    Infers the shared batch dimension and defers to `tensorprod_deriv` over the two
    operands' non-shared axes. (The routine returns immediately after that call; the
    remaining code is a retained earlier implementation.)

    :param s_expansion: the scalar (or lower-rank) expansion
    :type s_expansion: list
    :param A_expansion: the tensor expansion
    :type A_expansion: list
    :param order: derivative order(s) to compute
    :type order: int | list[int]
    :param identical: whether the two operands are the same expansion
    :type identical: bool
    :return: the scalar-product derivative expansion
    :rtype: list
    """
    s_expansion = [np.asarray(s) for s in s_expansion]
    A_expansion = [np.asarray(a) for a in A_expansion]
    s0_shape = s_expansion[0].shape if len(s_expansion) > 0 else ()
    A0_shape = A_expansion[0].shape if len(A_expansion) > 0 else ()
    shared = min([len(s0_shape), len(A0_shape)])
    terms = tensorprod_deriv(
        s_expansion,
        A_expansion,
        order=order,
        identical=identical,
        axes=[
            np.arange(shared, s_expansion[0].ndim),
            np.arange(shared, A_expansion[0].ndim)
        ]
    )
    return terms

    if is_numeric(order):
        order = list(range(order+1))
    suborder = [o for o in order if o > 0]
    # s_expansion, A_expansion = pre_broadcast_scalar_mult(s_expansion, A_expansion)
    if is_numeric(A_expansion[0]):
        if is_numeric(s_expansion[0]):
            base_expansion = scalarprod_deriv(s_expansion, A_expansion[1:],
                                              [o - 1 for o in suborder],
                                              identical=identical)
        else:
            shared = min([s_expansion[0].ndim, A_expansion[0].ndim])
            base_expansion = tensorprod_deriv(s_expansion, A_expansion[1:],
                                              [o - 1 for o in suborder],
                                              identical=identical,
                                              axes=[
                                                  np.arange(shared, s_expansion[0].ndim),
                                                  np.arange(shared, A_expansion[0].ndim)
                                              ])
        rem_expansion = [
            _scalar_prod(s_expansion[o], A_expansion[0])
                if len(s_expansion) > o else 0
            for o in suborder
        ]
    elif not is_numeric(s_expansion[0]):
        shared = min([s_expansion[0].ndim, A_expansion[0].ndim])
        return tensorprod_deriv(s_expansion, A_expansion,
                                order,
                                identical=identical,
                                axes=[
                                    np.arange(shared, s_expansion[0].ndim),
                                    np.arange(shared, A_expansion[0].ndim)
                                ])
    else:
        base_expansion = tensorprod_deriv(s_expansion[1:], A_expansion,
                                          order=[o - 1 for o in suborder],
                                          axes=[
                                              np.arange(s_expansion[1].ndim),
                                              np.arange(A_expansion[0].ndim)
                                          ],
                                          identical=identical)
        rem_expansion = [
            _scalar_prod(s_expansion[0], A_expansion[o]) if len(A_expansion) > o else 0
            for o in suborder
        ]
    high_order_expansion = [x + y for x, y in zip(base_expansion, rem_expansion)]

    # a lot of work to make sure we can do derivatives at a specifically targeted order
    n = 0
    final_expansion = []
    for o in order:
        if o == 0:
            final_expansion.append(_scalar_prod(s_expansion[0], A_expansion[0]))
        else:
            final_expansion.append(high_order_expansion[n])
            n += 1
    return final_expansion

def scalarfunc_deriv(scalar_func, arg_expansion, order):
    """
    **LLM Docstring**

    Compute the derivative expansion of applying a scalar function to a scalar
    argument expansion, via the chain rule.

    `scalar_func(value, i)` must return the `i`-th Taylor coefficient of the outer
    function at the argument value; those are combined with the argument's own
    derivatives through `scalarprod_deriv`.

    :param scalar_func: callable returning the outer function's Taylor coefficients
    :type scalar_func: Callable
    :param arg_expansion: expansion of the scalar argument
    :type arg_expansion: list
    :param order: the derivative order
    :type order: int
    :return: the composed scalar-function expansion
    :rtype: list
    """
    scalar_expansion = [scalar_func(arg_expansion[0], i) for i in range(order+1)]
    return [scalar_expansion[0]] + scalarprod_deriv(scalar_expansion[1:], arg_expansion[1:], order)

def shift_expansion(expansion, scalar):
    """
    **LLM Docstring**

    Add a constant to the value (zeroth-order) term of an expansion, leaving the
    derivatives unchanged.

    :param expansion: the expansion to shift
    :type expansion: list
    :param scalar: the constant to add
    :type scalar: float | np.ndarray
    :return: the shifted expansion
    :rtype: list
    """
    return [expansion[0] + scalar] + list(expansion[1:])

def scale_expansion(expansion, scalar):
    """
    **LLM Docstring**

    Multiply every term of an expansion by a scalar.

    The `-1` and `0` cases are handled specially for efficiency.

    :param expansion: the expansion to scale
    :type expansion: list
    :param scalar: the scaling factor
    :type scalar: float
    :return: the scaled expansion
    :rtype: list
    """
    if scalar == -1:
        return [-e for e in expansion] # can be faster
    elif is_zero(scalar):
        return [0 for e in expansion]
    else:
        return [scalar * e for e in expansion]

def add_expansions(*expansions, order=None):
    """
    **LLM Docstring**

    Add any number of expansions together term by term, zero-padding shorter
    expansions up to the requested order.

    :param expansions: the expansions to add
    :type expansions: list
    :param order: the order to pad to (inferred from the longest input if omitted)
    :type order: int | None
    :return: the summed expansion
    :rtype: list
    """
    if order is None:
        order = max(len(e) for e in expansions) - 1
    o = order + 1
    pad_expansions = [
        list(e) + [0]*(o - len(e))
        for e in expansions
    ]
    return [
        sum(x for x in e if not is_zero(x))
        for e in zip(*pad_expansions)
    ]

def subtract_expansions(a_expansion, b_expansion, order=None):
    """
    **LLM Docstring**

    Subtract one expansion from another term by term, zero-padding to the requested
    order.

    :param a_expansion: the expansion to subtract from
    :type a_expansion: list
    :param b_expansion: the expansion to subtract
    :type b_expansion: list
    :param order: the order to pad to (inferred from the inputs if omitted)
    :type order: int | None
    :return: the difference expansion
    :rtype: list
    """
    if order is None:
        order = max([len(a_expansion), len(b_expansion)]) - 1
    o = order + 1
    a_expansion, b_expansion = [
        list(e) + [0]*(o - len(e))
        for e in [a_expansion, b_expansion]
    ]
    return [
        a - b
        for a,b in zip(a_expansion, b_expansion)
    ]

def concatenate_expansions(a_expansion_or_expansion_list, b_expansion=None, concatenate_values=True):
    """
    **LLM Docstring**

    Concatenate expansions, either along the value axis or along the derivative
    (coordinate) axes.

    With a single list argument the expansions are concatenated pairwise. With
    `concatenate_values` set the value axis is joined; otherwise the derivative axes
    are joined into block-diagonal form. Missing/zero terms are filled with
    appropriately shaped zeros.

    :param a_expansion_or_expansion_list: the first expansion, or a list of expansions
    :type a_expansion_or_expansion_list: list
    :param b_expansion: the second expansion (omit to pass a list as the first arg)
    :type b_expansion: list | None
    :param concatenate_values: join along the value axis (vs. the derivative axes)
    :type concatenate_values: bool
    :return: the concatenated expansion
    :rtype: list
    """
    if b_expansion is None:
        expansion_list = a_expansion_or_expansion_list
        _ = expansion_list[0]
        for e in expansion_list[1:]:
            _ = concatenate_expansions(_, e, concatenate_values=concatenate_values)
        return _
    else:
        a_expansion = a_expansion_or_expansion_list
        a_expansion = [np.asanyarray(a) if not is_zero(a) else 0 for a in a_expansion]
        b_expansion = [np.asanyarray(b) if not is_zero(b) else 0 for b in b_expansion]
        if len(a_expansion) < len(b_expansion):
            a_expansion = a_expansion + [0] * (len(b_expansion) - len(a_expansion))
        elif len(b_expansion) < len(a_expansion):
            b_expansion = b_expansion + [0] * (len(a_expansion) - len(b_expansion))

        base_shape = None
        for n,a in enumerate(a_expansion):
            if not is_zero(a):
                base_shape = a.shape[:-(2+n)]
                break
        else:
            for n,b in enumerate(b_expansion):
                if not is_zero(b):
                    base_shape = b.shape[:-(2 + n)]
                    break
            else:
                raise ValueError("can't concatenate two entirely zero expansions")

        a_nder = None
        a_nvals = None
        for n,a in enumerate(a_expansion):
            if not is_zero(a):
                a_nder, a_nvals = a.shape[-2:]
                break

        b_nder = None
        b_nvals = None
        for n,b in enumerate(b_expansion):
            if not is_zero(b):
                b_nder, b_nvals = b.shape[-2:]
                break

        if b_nder is None:
            b_nder, b_nvals = a_nder, a_nvals
        elif a_nder is None:
            a_nder, a_nvals = b_nder, b_nvals

        expansion = []
        for n,(a,b) in enumerate(zip(a_expansion, b_expansion)):
            if is_zero(a):
                if is_zero(b):
                    expansion.append(0)
                    continue
                a = np.zeros(base_shape + (a_nder,)*(n+1) + (a_nvals,))
            elif is_zero(b):
                b = np.zeros(base_shape + (b_nder,)*(n+1) + (b_nvals,))

            if concatenate_values:
                c = np.concatenate([a, b], axis=-1)
            else:
                if a_nvals != b_nvals:
                    raise ValueError(f"can't concatenate expansions along the derivative axes with different value shapes "
                                     f"(ncoord: {a_nder},{b_nder}, nvals:{a_nvals},{b_nvals})")
                c = np.zeros(base_shape + (a_nder + b_nder,)*(n+1) + (a_nvals,))
                # TODO: add small optimization for zero cases
                sel_a = (...,) + (slice(0, a_nder),) * (n+1) + (slice(None),)
                sel_b = (...,) + (slice(a_nder, None),) * (n+1) + (slice(None),)
                c[sel_a] = a
                c[sel_b] = b
            expansion.append(c)
    return expansion

#TODO: add a DifferentiableExpansion class so I can have nicer overloads on all of this...

def inverse_transformation(forward_expansion, order, reverse_expansion=None,
                           allow_pseudoinverse=False,
                           nonzero_cutoff=None
                           ):
    """
    **LLM Docstring**

    Compute the derivative expansion of the inverse of a transformation from its
    forward expansion (i.e. invert a Jacobian-and-higher-derivatives series).

    The zeroth-order inverse is the (pseudo)inverse of the leading Jacobian; each
    higher order is obtained by re-expanding the current inverse through the forward
    expansion and contracting back in the leading inverse.

    :param forward_expansion: the forward transformation expansion
    :type forward_expansion: list
    :param order: the derivative order
    :type order: int | list[int]
    :param reverse_expansion: a precomputed inverse expansion to extend
    :type reverse_expansion: list | None
    :param allow_pseudoinverse: use the pseudoinverse for non-square leading terms
    :type allow_pseudoinverse: bool
    :param nonzero_cutoff: singular-value cutoff for a regularized inverse
    :type nonzero_cutoff: float | None
    :return: the inverse transformation expansion
    :rtype: list
    """
    if reverse_expansion is None:
        if nonzero_cutoff is None:
            if allow_pseudoinverse and forward_expansion[0].shape[0] != forward_expansion[0].shape[1]:
                B = np.linalg.pinv(forward_expansion[0])
            else:
                B = np.linalg.inv(forward_expansion[0])
        else:
            f0 = forward_expansion[0]
            B = vec_ops.frac_powh(f0, -1, nonzero_cutoff=nonzero_cutoff)
            B = B[..., :, :f0.shape[-2]]
        reverse_expansion = [B]
    else:
        reverse_expansion = list(reverse_expansion)
        B = reverse_expansion[0]

    if not is_numeric(order): order = np.max(order)
    order = list(range(2, order+1))
    shared = B.ndim - 2

    for o in order:
        new_B = -tensor_reexpand(reverse_expansion, forward_expansion, [o])[-1]
        if isinstance(new_B, np.ndarray):
            # need to multiply in the inverse now, too
            new_B = vec_ops.vec_tensordot(new_B, B, axes=[-1, shared], shared=shared)
            # for _ in range(new_B.ndim - 1):
            #     new_B = np.tensordot(B, new_B, axes=[1, -2])
        reverse_expansion = reverse_expansion + [new_B]
    return reverse_expansion


def renormalize_transformation(forward_transformation, reverse_transformation, nonzero_cutoff=None):
    """
    **LLM Docstring**

    Rescale a forward/reverse transformation pair so that the singular values of
    their product are normalized, keeping the pair mutually consistent.

    Uses the SVD of `forward[0] @ reverse[0]` to build symmetric scaling factors
    that are folded into the forward expansion from the left and the reverse
    expansion from the right.

    :param forward_transformation: the forward transformation expansion
    :type forward_transformation: list
    :param reverse_transformation: the reverse transformation expansion
    :type reverse_transformation: list
    :param nonzero_cutoff: singular-value cutoff below which directions are dropped
    :type nonzero_cutoff: float | None
    :return: the renormalized `(forward, reverse)` pair
    :rtype: tuple[list, list]
    """
    u, s, v = np.linalg.svd(forward_transformation[0] @ reverse_transformation[0])
    sq_eval = np.sqrt(s)
    if nonzero_cutoff is not None:
        mask = np.abs(s) < nonzero_cutoff
        sq_eval[mask] = 1
        vals = s/sq_eval
        vals[mask] = 0
    else:
        vals = 1/sq_eval
    scaling = vec_tensordiag(vals)
    tf_left = scaling @ np.moveaxis(u, -2, -1)
    tf_right = np.moveaxis(v, -2, -1) @ scaling

    forward_transformation = tensor_reexpand([tf_left], forward_transformation)
    reverse_transformation = tensor_reexpand(reverse_transformation, [tf_right])

    return forward_transformation, reverse_transformation

def orthogonalize_transformations(transformation_pairs,
                                  order=None,
                                  orthonormalize=True,
                                  assume_prenormalized=True,
                                  first_order_projector=True,
                                  nonzero_cutoff=None,
                                  concatenate=True):
    """
    **LLM Docstring**

    Orthogonalize a sequence of forward/reverse transformation pairs against one
    another, building a combined (block) transformation.

    Each successive pair is projected against the accumulated complement projector
    (Gram-Schmidt style) and optionally renormalized; the projector is updated after
    each step. The per-pair results are optionally concatenated into a single
    forward/reverse expansion.

    :param transformation_pairs: the `(forward, reverse)` expansion pairs
    :type transformation_pairs: Iterable[tuple]
    :param order: the derivative order (inferred from the inputs if omitted)
    :type order: int | None
    :param orthonormalize: renormalize each projected pair
    :type orthonormalize: bool
    :param assume_prenormalized: skip the initial renormalization of each pair
    :type assume_prenormalized: bool
    :param first_order_projector: use only the leading-order projector
    :type first_order_projector: bool
    :param nonzero_cutoff: singular-value cutoff used during renormalization
    :type nonzero_cutoff: float | None
    :param concatenate: concatenate the results into a single transformation
    :type concatenate: bool
    :return: the orthogonalized `(forward, reverse)` transformations
    :rtype: tuple
    """
    projector = None
    forward_transformations = []
    reverse_transformations = []
    if order is None:
        transformation_pairs = list(transformation_pairs)
        order = max(max([len(f), len(r)]) for f,r in transformation_pairs)
    for forward, reverse in transformation_pairs:
        if not assume_prenormalized:
            forward, reverse = renormalize_transformation(forward, reverse, nonzero_cutoff=nonzero_cutoff)
        if projector is None:
            forward_transformations.append(forward)
            reverse_transformations.append(reverse)
            if first_order_projector:
                projector = [identity_tensors(reverse[0].shape[:-2], reverse[0].shape[-2]) - reverse[0]@forward[0]]
            else:
                I_expansion = [identity_tensors(reverse[0].shape[:-2], reverse[0].shape[-2])]
                projector = subtract_expansions(I_expansion, tensor_reexpand(reverse, forward))
        else:
            forward = tensor_reexpand(forward, projector, order=order)
            reverse = tensor_reexpand(projector, reverse, order=order)
            if orthonormalize:
                forward, reverse = renormalize_transformation(forward, reverse, nonzero_cutoff=nonzero_cutoff)

            forward_transformations.append(forward)
            reverse_transformations.append(reverse)
            if first_order_projector:
                subprojector = identity_tensors(reverse[0].shape[:-2], reverse[0].shape[-2]) - reverse[0]@forward[0]
                projector = [projector[0] @ subprojector]
            else:
                I_expansion = [identity_tensors(reverse[0].shape[:-2], reverse[0].shape[-2])]
                subprojector = subtract_expansions(I_expansion, tensor_reexpand(reverse, forward))
                projector = tensor_reexpand(projector, subprojector)

    if concatenate:
        _ = forward_transformations[0]
        for f in forward_transformations[1:]:
            _ = concatenate_expansions(_, f, concatenate_values=True)
        forward_transformations = _
        _ = reverse_transformations[0]
        for f in reverse_transformations[1:]:
            _ = concatenate_expansions(_, f, concatenate_values=False)
        reverse_transformations = _
    return forward_transformations, reverse_transformations

def kron_prod_derivs(A_expansion, B_expansion, order):
    """
    **LLM Docstring**

    Compute the derivative expansion of the Kronecker product of two matrix
    expansions.

    Builds the outer product over the matrix row/column axes and reshapes each order
    into the flattened Kronecker layout.

    :param A_expansion: expansion of the first matrix
    :type A_expansion: list
    :param B_expansion: expansion of the second matrix
    :type B_expansion: list
    :param order: derivative order(s) to compute
    :type order: int | list[int]
    :return: the Kronecker-product derivative expansion
    :rtype: list
    """
    # s = A_expansion[0].ndim - 2
    C_expansion = tensorprod_deriv(A_expansion, B_expansion, order,
                                   axes=[[-1, -2], [-1, -2]]
                                   )
    # now we need to reshape based on the fact that we end up with nnxmm
    return [
        c.reshape(c.shape[:-4] + (c.shape[-4]*c.shape[-3], c.shape[-2]*c.shape[-1]))
        for c in C_expansion
    ]

def kron_sum_derivs(A_expansion, B_expansion, order):
    """
    **LLM Docstring**

    Compute the derivative expansion of the Kronecker sum `A ⊗ I + I ⊗ B` of two
    matrix expansions.

    Assembles the two Kronecker products against appropriately sized identities and
    adds them term by term.

    :param A_expansion: expansion of the first matrix
    :type A_expansion: list
    :param B_expansion: expansion of the second matrix
    :type B_expansion: list
    :param order: derivative order(s) to compute
    :type order: int | list[int]
    :return: the Kronecker-sum derivative expansion
    :rtype: list
    """
    base_shape = B_expansion[0].shape[:-2]
    ns = len(base_shape)
    m = B_expansion[0].shape[-1]
    if ns > 0:
        I_expansion = np.expand_dims(np.eye(m), list(range(ns)))
        I_expansion = np.broadcast_to(I_expansion, base_shape + (m, m))
    else:
        I_expansion = np.eye(m)
    I_expansion = [I_expansion]
    left_expansion = kron_prod_derivs(A_expansion, I_expansion, order)

    n = A_expansion[0].shape[-1]
    if ns > 0:
        I_expansion = np.expand_dims(np.eye(n), list(range(ns)))
        I_expansion = np.broadcast_to(I_expansion, base_shape + (n, n))
    else:
        I_expansion = np.eye(n)
    I_expansion = [I_expansion]
    right_expansion = kron_prod_derivs(I_expansion, B_expansion, order)

    return [l+r for l,r in zip(left_expansion, right_expansion)]

def sylv_derivs(A_expansion, B_expansion, C_expansion, order, shared=None, ks_expansion=None, inv_expansion=None):
    """
    **LLM Docstring**

    Compute the derivative expansion of the solution `X` to the Sylvester equation
    `A X + X B = C`.

    Vectorizes the equation via the Kronecker sum of `A` and `Bᵀ`, inverts that
    expansion, contracts against the (flattened) `C` expansion, and reshapes back to
    matrix form. The Kronecker-sum and inverse expansions are returned for reuse.

    :param A_expansion: expansion of the left coefficient
    :type A_expansion: list
    :param B_expansion: expansion of the right coefficient
    :type B_expansion: list
    :param C_expansion: expansion of the right-hand side
    :type C_expansion: list
    :param order: derivative order(s) to compute
    :type order: int | list[int]
    :param shared: number of shared leading batch axes
    :type shared: int | None
    :param ks_expansion: a cached Kronecker-sum expansion to extend
    :type ks_expansion: list | None
    :param inv_expansion: a cached inverse expansion to extend
    :type inv_expansion: list | None
    :return: `(X_expansion, (kron_sum_expansion, inverse_expansion))`
    :rtype: tuple
    """
    n = A_expansion[0].shape[-1]
    m = B_expansion[0].shape[-1]
    B_expansion = [np.moveaxis(b, -1, -2) for b in B_expansion]
    if ks_expansion is not None:
        ks_expansion = list(ks_expansion) + kron_sum_derivs(A_expansion, B_expansion, order)
    else:
        ks_expansion = kron_sum_derivs(A_expansion, B_expansion, order)
    if isinstance(order, list):
        inv_expansion = matinv_deriv(ks_expansion, order[0], base_expansion=inv_expansion)
    else:
        inv_expansion = matinv_deriv(ks_expansion, order, base_expansion=inv_expansion)
    C_expansion = [np.reshape(c, c.shape[:-2] + (c.shape[-1] * c.shape[-2],)) for c in C_expansion]
    X_expansion = tensordot_deriv(C_expansion, inv_expansion, order,
                                  axes=[-1, -1],
                                  shared=shared
                                  )

    return [np.reshape(x, x.shape[:-1] + (n,m)) for x in X_expansion], (ks_expansion, inv_expansion)

def matsqrt_deriv(A_expansion, order):
    """
    **LLM Docstring**

    Compute the derivative expansion of the (symmetric) matrix square root.

    The leading term is the eigen-based square root of `A[0]`; each higher order is
    obtained by solving the Sylvester equation `B X + X B = dA` with `sylv_derivs`,
    reusing the cached Kronecker-sum/inverse expansions.

    :param A_expansion: expansion of the matrix
    :type A_expansion: list
    :param order: the derivative order
    :type order: int
    :return: the matrix-square-root expansion
    :rtype: list
    """
    shared = A_expansion[0].ndim - 2
    if shared == 0: shared = None
    B_expansion = [
        vec_ops.frac_powh(A_expansion[0], 1/2, pow=lambda evals,_:np.sqrt(evals))
        # sqrt maybe faster than pow(..., 1/2)
    ]
    inv_expansion = None
    ks_expansion = None
    for o in range(1, order+1):
        new_expansion, (ks_expansion, inv_expansion) = sylv_derivs(B_expansion, B_expansion, A_expansion[1:],
                                                                   ks_expansion=ks_expansion,
                                                                   inv_expansion=inv_expansion,
                                                                   shared=shared,
                                                                   order=[o - 1])
        B_expansion = B_expansion + new_expansion

    return B_expansion

def matinv_deriv(A_expansion, order, base_expansion=None):
    """
    **LLM Docstring**

    Compute the derivative expansion of the matrix inverse.

    The leading term is `inv(A[0])`; each higher order follows from the identity
    `d(A⁻¹) = -A⁻¹ (dA) A⁻¹`, evaluated through `tensorops_deriv`.

    :param A_expansion: expansion of the matrix
    :type A_expansion: list
    :param order: the derivative order
    :type order: int
    :param base_expansion: a precomputed inverse expansion to extend
    :type base_expansion: list | None
    :return: the matrix-inverse expansion
    :rtype: list
    """
    shared = s = A_expansion[0].ndim - 2
    if shared == 0: shared = None
    if base_expansion is None:
        B = np.linalg.inv(A_expansion[0])
        base_expansion = [B]
    inverse_expansion = list(base_expansion)

    for o in range(len(inverse_expansion), order+1):
        expansion = tensorops_deriv(
            A_expansion[1:],
                [s+1, s + 1],
            inverse_expansion,
                [s+2, s + 0],
            inverse_expansion,
            order=[o - 1],
            shared=shared
        )
        inverse_expansion = inverse_expansion + [-expansion[-1]]
    return inverse_expansion

def matdet_deriv(forward_expansion, order):
    """
    **LLM Docstring**

    Compute the derivative expansion of the matrix determinant.

    Uses the inverse expansion and Jacobi's formula (`d(det)/det = tr(A⁻¹ dA)`),
    integrating the trace expansion against the determinant via `scalarprod_deriv`.

    :param forward_expansion: expansion of the matrix
    :type forward_expansion: list
    :param order: the derivative order
    :type order: int
    :return: the determinant expansion
    :rtype: list
    """
    shared = forward_expansion[0].ndim - 2
    reverse_expansion = matinv_deriv(forward_expansion, order)
    tr_inner_exp = tensordot_deriv(forward_expansion[1:], reverse_expansion,
                                   order - 1,
                                   axes=[1+shared, 1+shared],
                                   shared=shared
                                   )
    tr_exp = [np.trace(a, axis1=-2, axis2=-1) for a in tr_inner_exp]
    det_exp = [np.linalg.det(forward_expansion[0])]
    for o in range(0, order):
        det_exp = det_exp + [scalarprod_deriv(det_exp, tr_exp, [o])[-1]]
    return det_exp

def mateigh_deriv(mat_exp, order, *, diagonal_only=True, base_expansion=None):
    """
    **LLM Docstring**

    Compute the derivative expansion of the symmetric eigen-decomposition
    (eigenvalues and eigenvectors) of a matrix expansion.

    Applies degenerate perturbation-theory-style recurrences: eigenvalue derivatives
    come from the diagonal of the transformed matrix derivative, and eigenvector
    derivatives from contracting the matrix derivative against the (regularized)
    inverse of the eigenvalue-difference matrix. With `diagonal_only` set only the
    diagonal eigenvalue block is tracked.

    :param mat_exp: expansion of the (symmetric) matrix
    :type mat_exp: list
    :param order: the derivative order
    :type order: int
    :param diagonal_only: track only the diagonal eigenvalue contributions
    :type diagonal_only: bool
    :param base_expansion: precomputed `(eigenvalue_expansion, eigenvector_expansion)`
    :type base_expansion: tuple | None
    :return: `(eigenvalue_expansion, eigenvector_expansion)`
    :rtype: tuple[list, list]
    """
    # I don't know if `diagonal_only=False` is meaningful in any way but I also
    # don't know if any of this is right yet, so I'll leave it until I'm sure
    if base_expansion is None:
        vals, vecs = np.linalg.eigh(mat_exp[0])
        vals = vec_ops.vec_tensordiag(vals)
        base_expansion = [vals], [vecs]
    val_exp, vec_exp = base_expansion
    mat_diff_exp = [[] for _ in range(val_exp[0].shape[-1])] if diagonal_only else []
    mat_diff_inv_exp = [None for _ in range(val_exp[0].shape[-1])] if diagonal_only else None
    shared = mat_exp[0].ndim - 2
    if len(mat_exp) > 1:
        nc = mat_exp[1].shape[-3]
        for o in range(1, order+1):
            if diagonal_only:
                new_diag = np.zeros(val_exp[-1].shape[:-2] + (nc,) + val_exp[-1].shape[-2:])
                for i in range(vec_exp[0].shape[-1]):
                    subvec_exp = [v[..., (i,)] for v in vec_exp]
                    new_diag[..., i, i] = tensorops_deriv(
                            mat_exp[1:],
                                [-2, -2],
                            subvec_exp,
                                [-2, -2],
                            subvec_exp,
                            order=[o - 1],
                            shared=shared
                        )[-1][..., 0, 0]
                val_exp.append(new_diag)
            else:
                val_exp.append(
                    tensorops_deriv(
                        mat_exp[1:],
                            [-2, -2],
                        vec_exp,
                            [-2, -2],
                        vec_exp,
                        order=[o-1],
                        shared=shared
                    )[-1]
                )

            # add one order as we expand the difference expansion
            if diagonal_only:
                new_diag = np.zeros(vec_exp[-1].shape[:-2] + (nc,) + vec_exp[-1].shape[-2:])
                i_mat = np.eye(val_exp[-1].shape[-1])
                for i in range(vec_exp[0].shape[-1]):
                    v_I = val_exp[o - 1][..., i, i] * i_mat
                    mat_diff_exp[i].append(v_I - (mat_exp[o - 1] if o < len(mat_exp) else 0))
                    if mat_diff_inv_exp[i] is None:
                        mat_diff_inv_exp[i] = [
                            vec_ops.frac_powh(mat_diff_exp[i][0], -1, nonzero_cutoff=1e-12)
                        ]
                    else:
                        mat_diff_inv_exp[i] = matinv_deriv(mat_diff_exp[i], o-1, base_expansion=mat_diff_inv_exp[i])
                    subvec_exp = [v[..., (i,)] for v in vec_exp]
                    new_diag[..., i] = tensorops_deriv(
                        mat_exp[1:],
                            [-2, -1],
                        mat_diff_inv_exp[i],
                            [-2, -2],
                        subvec_exp,
                        order=[o-1],
                        shared=shared
                    )[-1][..., 0]
                vec_exp.append(new_diag)
            else:
                mat_diff_exp.append(val_exp[o-1] - (mat_exp[o-1] if o < len(mat_exp) else 0))
                mat_diff_inv_exp = matinv_deriv(mat_diff_exp, o-1, base_expansion=mat_diff_inv_exp)
                vec_exp.append(
                    tensorops_deriv(
                        mat_exp[1:],
                            [-2, -1],
                        mat_diff_inv_exp,
                            [-2, -2],
                        vec_exp,
                        order=[o-1],
                        shared=shared
                    )[-1]
                )

    return val_exp, vec_exp

def _broadcast_mul(scalar, other):
    """
    **LLM Docstring**

    Multiply two arrays, broadcasting a lower-rank scalar factor up to the rank of
    the other operand.

    :param scalar: the (possibly lower-rank) scalar factor
    :type scalar: np.ndarray | float
    :param other: the other operand
    :type other: np.ndarray | float
    :return: the broadcast product
    :rtype: np.ndarray | float
    """
    if (
            isinstance(scalar, np.ndarray)
            and isinstance(other, np.ndarray)
            and scalar.ndim < other.ndim
    ):
        return np.expand_dims(scalar, list(range(scalar.ndim, other.ndim))) * other
    else:
        return scalar * other

_integer_partition_cache = {}
def get_integer_partitions(o):
    """
    **LLM Docstring**

    Return the integer partitions of `o`, cached across calls.

    :param o: the integer to partition
    :type o: int
    :return: the integer partitions of `o`
    :rtype: list
    """
    from ..Combinatorics import IntegerPartitioner

    return dev.cached_eval(
        _integer_partition_cache,
        o,
        IntegerPartitioner.partitions,
        args=(o,)
    )
def _scalarinv_deriv(scalar_expansion, o):
    """
    **LLM Docstring**

    Compute the single order-`o` derivative of the reciprocal `1 / scalar` via the
    Faà di Bruno formula over integer partitions.

    Each partition contributes `(-1)^l l! / scalar^(l+1)` times the symmetrized
    product of the corresponding argument derivatives.

    :param scalar_expansion: expansion of the scalar
    :type scalar_expansion: list
    :param o: the derivative order
    :type o: int
    :return: the order-`o` reciprocal derivative
    :rtype: np.ndarray | int
    """

    shared = scalar_expansion[0].ndim
    term = 0
    for parts in get_integer_partitions(o):
        l = len(parts[0])
        scaling = ((-1) ** l) * math.factorial(l) / (scalar_expansion[0] ** (l + 1))
        # term = 0
        # for p in parts:
        #     nca_term = nca_partition_prod(p, scalar_expansion[1:], shared=shared)
        #     b_term = _broadcast_mul(scaling, nca_term)
        #     term += b_term
        term = sum(
            _broadcast_mul(scaling, nca_partition_prod(p, scalar_expansion[1:], shared=shared))
            for p in parts
        )
    return term

def scalarinv_deriv(scalar_expansion, order):
    """
    **LLM Docstring**

    Compute the derivative expansion of the reciprocal `1 / scalar` of a scalar
    expansion.

    :param scalar_expansion: expansion of the scalar
    :type scalar_expansion: list
    :param order: the derivative order(s)
    :type order: int | list[int]
    :return: the reciprocal expansion
    :rtype: list
    """
    return _deriv_construct(
        lambda : 1/scalar_expansion[0],
        lambda ords: [_scalarinv_deriv(scalar_expansion, o) for o in ords],
        order
    )

def _scalarpow_deriv(scalar_expansion, exp, o):
    """
    **LLM Docstring**

    Compute the single order-`o` derivative of `scalar ** exp` via the Faà di Bruno
    formula over integer partitions.

    Each partition contributes the falling-factorial coefficient
    `exp (exp-1) ... (exp-l+1)` times `scalar^(exp-l)` times the symmetrized product
    of argument derivatives.

    :param scalar_expansion: expansion of the scalar
    :type scalar_expansion: list
    :param exp: the exponent
    :type exp: float
    :param o: the derivative order
    :type o: int
    :return: the order-`o` power derivative
    :rtype: np.ndarray | int
    """
    shared = scalar_expansion[0].ndim

    term = 0
    for parts in get_integer_partitions(o):
        l = len(parts[0])
        factorial_terms = np.prod(exp - np.arange(l))
        if factorial_terms == 0:
            continue
        scaling = factorial_terms * (scalar_expansion[0] ** (exp - l))
        term += sum(
            _broadcast_mul(scaling, nca_partition_prod(p, scalar_expansion[1:], shared=shared))
            for p in parts
        )
    return term

def scalarpow_deriv(scalar_expansion, exp, order):
    """
    **LLM Docstring**

    Compute the derivative expansion of `scalar ** exp` for a scalar expansion.

    :param scalar_expansion: expansion of the scalar
    :type scalar_expansion: list
    :param exp: the exponent
    :type exp: float
    :param order: the derivative order(s)
    :type order: int | list[int]
    :return: the power expansion
    :rtype: list
    """
    scalar_expansion = [np.asanyarray(s) for s in scalar_expansion]
    return _deriv_construct(
        lambda : np.power(scalar_expansion[0], exp),
        lambda ords: [_scalarpow_deriv(scalar_expansion, exp, o) for o in ords],
        order
    )

def odd_fac(x):
    """
    **LLM Docstring**

    Return the product of the first odd numbers `1 * 3 * 5 * ...` up to the count
    implied by `x` (a double-factorial-style helper for the norm derivatives).

    :param x: controls how many odd factors to include
    :type x: int
    :return: the product of odd numbers
    :rtype: int
    """
    return np.prod([2*o+1 for o in range((x-1)//2)])
def vec_norm_unit_deriv(vec_expansion, order, base_expansion=None, raise_on_failure=True):
    """
    **LLM Docstring**

    Compute the derivative expansions of both the norm and the unit vector of a
    vector expansion.

    Builds the norm-derivative series in closed form using integer partitions
    (restricted to first/second powers of the base vector) and then re-expands both
    the norm and the unit vector in terms of the original vector's derivatives. A
    zero-length vector raises (or returns `(None, None)` when `raise_on_failure` is
    off).

    :param vec_expansion: expansion of the vector
    :type vec_expansion: list
    :param order: the derivative order(s)
    :type order: int | list[int]
    :param base_expansion: unused placeholder (kept for signature parity)
    :type base_expansion: list | None
    :param raise_on_failure: raise on a zero-length vector rather than returning None
    :type raise_on_failure: bool
    :return: `(norm_expansion, unit_vector_expansion)`
    :rtype: tuple
    """
    from ..Combinatorics import IntegerPartitioner

    a = vec_expansion[0]
    r = np.linalg.norm(a, axis=-1)
    if r < Options.zero_threshold:
        if raise_on_failure:
            raise ValueError("can't get derivatives of zero vector")
        else:
            return None, None
    a_expansion = [a, vec_ops.identity_tensors(a.shape[:-1], a.shape[-1])]

    if not is_numeric(order):
        order = max(order)

    base_expansion = []
    shared = len(a.shape[:-1])
    for o in range(order + 2):
        if o == 0:
            base_expansion.append(r)
            continue

        t = 0
        rr = np.expand_dims(r, [-(i+1) for i in range(o)])
        # print("->"*20, o, "<-"*20)
        for k in itertools.chain(*IntegerPartitioner.partitions(o)):
            if max(k) > 2: continue
            factor = a_expansion[k[0]-1]
            for p in k[1:]:
                factor = _scalar_prod(factor, a_expansion[p-1], shared=shared)
            factor = nca_symmetrize(factor, k, shared=shared, identical=True)

            # compute powers
            e = (o + 1) // 2
            n = len(k)
            s = o - (1 - o%2)
            x = s + 2*(n - e)
            pref = ((-1)**(s+n)) * odd_fac(x) / (rr**x)
            # print("!", n//2, odd_fac(n//2), e, k, x)
            t += factor * pref
        base_expansion.append(t)

    # if base_expansion is None:
    #     a = vec_expansion[0]
    #     r = np.linalg.norm(a, axis=-1)
    #     if a.ndim > 1:
    #         u = a / r[..., np.newaxis]
    #     else:
    #         u = a / r
    #     base_expansion = [r, u]
    # base_expansion = list(base_expansion)
    # norm_inv_expansion = scalarinv_deriv(base_expansion, order=len(base_expansion)-2)
    #
    # a_expansion = [vec_expansion[0], vec_ops.identity_tensors(base_expansion[1].shape[:-1], 3)]
    #
    # if not is_numeric(order):
    #     order = max(order)
    #
    # for o in range(len(base_expansion), order+2):
    #     norm_inv_expansion = norm_inv_expansion + scalarinv_deriv(base_expansion, order=[o-1])
    #     base_expansion = base_expansion + scalarprod_deriv(
    #         norm_inv_expansion,
    #         a_expansion,
    #         order=[o - 1],
    #         identical=True
    #     )

    # print([b.shape for b in base_expansion])
    # print([v.shape for v in vec_expansion])

    # reexpand in terms of original vectors
    norm_expansion = [base_expansion[0]] + (
        tensor_reexpand(
            vec_expansion[1:],
            base_expansion[1:],
            order + 1
            # shared=vec_expansion[0].ndim - 1
        ) if order > 0 else []
    )

    unit_expansion = [base_expansion[1]] + (
        tensor_reexpand(
            vec_expansion[1:],
            base_expansion[2:],
            order
            # shared=vec_expansion[0].ndim - 1
        ) if order > 0 else []
    )

    return norm_expansion, unit_expansion

def vec_anglecos_deriv(A_expansion, B_expansion, order, unitized=False):
    """
    **LLM Docstring**

    Compute the derivative expansion of the cosine of the angle between two
    vectors (the dot product of their unit vectors).

    Unless the inputs are already unitized, each vector is first replaced by its
    unit-vector expansion.

    :param A_expansion: expansion of the first vector
    :type A_expansion: list
    :param B_expansion: expansion of the second vector
    :type B_expansion: list
    :param order: the derivative order(s)
    :type order: int | list[int]
    :param unitized: whether the inputs are already unit vectors
    :type unitized: bool
    :return: the cosine expansion
    :rtype: list
    """
    if not unitized:
        A_expansion = vec_norm_unit_deriv(A_expansion, order)[1]
        B_expansion = vec_norm_unit_deriv(B_expansion, order)[1]
    shared = A_expansion[0].ndim - 1
    ugh = tensordot_deriv(A_expansion, B_expansion, order=order, axes=[-1, -1], shared=shared)
    return ugh
    # n = A_expansion[0].shape[-1] # should be 3
    # z = np.zeros(A_expansion[0].shape[:-1] + (n, n))
    # I = vec_ops.identity_tensors(A_expansion[0].shape[:-1], n)
    # vec_expansion = [
    #     vec_ops.vec_tensordot(A_expansion[0], B_expansion[0], axes=[-1, -1], shared=shared),
    #     np.concatenate([B_expansion[0], A_expansion[0]], axis=-1),
    #     np.concatenate([
    #         np.concatenate([z, I], axis=-1),
    #         np.concatenate([I, z], axis=-1)
    #     ],
    #         axis=-2
    #     )
    # ]
    # cat_expansion = [
    #     np.concatenate([a, b], axis=-1)
    #     for a, b in zip(A_expansion[1:], B_expansion[1:])
    # ]
    # return [vec_expansion[0]] + tensor_reexpand(
    #     cat_expansion,
    #     vec_expansion[1:],
    #     order
    # )

def vec_cross_deriv(A_expansion, B_expansion, order):
    """
    **LLM Docstring**

    Compute the derivative expansion of the cross product of two vectors.

    Contracts the two vector expansions against the Levi-Civita tensor through the
    multi-operand derivative machinery.

    :param A_expansion: expansion of the first vector
    :type A_expansion: list
    :param B_expansion: expansion of the second vector
    :type B_expansion: list
    :param order: the derivative order(s)
    :type order: int | list[int]
    :return: the cross-product expansion
    :rtype: list
    """
    shared = A_expansion[0].ndim - 1
    base_shape = A_expansion[0].shape[:-1]
    e3 = np.broadcast_to(
        np.expand_dims(perms.levi_cevita3, list(range(shared))),
        base_shape + (3, 3, 3)
    )
    res = tensorops_deriv(
        B_expansion,
            [-1, shared],
        [e3],
            [-1, -1],
        A_expansion,
        order=order,
        shared=shared
    )
    return res

def vec_parallel_cross_norm_deriv(axb_expansion, bxc_expansion, order, *,
                                  component_vectors=None,
                                  up_vector_expansion=None,
                                  unit_expansions=None
                                  ):
    """
    **LLM Docstring**

    Compute the derivative expansion of the signed cross-product-norm term used for
    the (near-)parallel dihedral limit.

    Combines the cross products of the surrounding component vectors and their unit
    norms into the limiting sine-of-dihedral expansion, so that dihedrals remain
    well-defined as the two normal vectors become parallel.

    :param axb_expansion: expansion of the first normal (`a x b`)
    :type axb_expansion: list
    :param bxc_expansion: expansion of the second normal (`b x c`)
    :type bxc_expansion: list
    :param order: the derivative order(s)
    :type order: int | list[int]
    :param component_vectors: the `[A, B, C]` edge-vector expansions
    :type component_vectors: list | None
    :param up_vector_expansion: an up-vector expansion (if component vectors omitted)
    :type up_vector_expansion: list | None
    :param unit_expansions: precomputed unit-norm expansions `[B, axb, bxc]`
    :type unit_expansions: list | None
    :return: the parallel-limit sine expansion
    :rtype: list
    """
    base_shape = axb_expansion[0].shape[:-1]
    shared = len(base_shape)

    if component_vectors is None:
        if up_vector_expansion is None:
            raise ValueError("an up vector expansion or component vectors must be provided")
        component_vectors = [axb_expansion, up_vector_expansion, bxc_expansion]

    A_expansion, B_expansion, C_expansion = component_vectors
    if unit_expansions is None:
        axb_unit_expansion, _ = vec_norm_unit_deriv(axb_expansion, order)
        bxc_unit_expansion, _ = vec_norm_unit_deriv(bxc_expansion, order)
        B_unit_expansion, _ = vec_norm_unit_deriv(B_expansion, order)
    else:
        B_unit_expansion, axb_unit_expansion, bxc_unit_expansion = unit_expansions
    axc_expansion = vec_cross_deriv(A_expansion, C_expansion, order)

    # print([b.shape for b in B_expansion])
    # print([a.shape for a in axc_expansion])
    # print(order)
    base_expansion = tensordot_deriv(
        B_expansion,
        axc_expansion,
        order,
        axes=[-1, -1],
        shared=shared
    )
    axb_inv_expansion = scalarinv_deriv(axb_unit_expansion, order)
    bxc_inv_expansion = scalarinv_deriv(bxc_unit_expansion, order)
    # print("B", [b.shape for b in B_unit_expansion])
    # print("axb", [b.shape for b in axb_inv_expansion])
    # print("bxc", [b.shape for b in bxc_inv_expansion])
    scalar_term = scalarprod_deriv(
        B_unit_expansion,
        axb_inv_expansion,
        order
    )
    scalar_term = scalarprod_deriv(
        scalar_term,
        bxc_inv_expansion,
        order
    )
    woof = scalarprod_deriv(scalar_term, base_expansion, order)
    # print("woof", [w.shape for w in woof])
    return [-w for w in woof]

    # i3 = np.broadcast_to(np.eye(3)[np.newaxis], (3, 3, 3)).copy()
    # for i in range(3):
    #     i3[i, i, i] = 0
    #
    # base_shape = axb_expansion[0].shape[:-1]
    # shared = len(base_shape)
    # i3 = np.broadcast_to(np.expand_dims(i3, list(range(shared))), base_shape + (3, 3, 3))
    # overlaps = axb_expansion[0][..., np.newaxis, :] @ bxc_expansion[0][..., :, np.newaxis]
    # signs = np.reshape(np.sign(overlaps), base_shape)
    # B_exp = [
    #     # force parallel
    #     np.expand_dims(signs, list(range(-(o+1), 0))) * b
    #     for o,b in enumerate(bxc_expansion)
    # ]
    #
    # pseudo_norm = tensorops_deriv(
    #     B_exp,
    #         [-1, -1],
    #     [i3],
    #         [-1, -1],
    #     axb_expansion,
    #     order=0,
    #     shared=shared
    # )[0]
    # pseudo_norm_2 = np.sqrt(np.abs(pseudo_norm))
    #
    # if is_numeric(order):
    #     order = np.arange(order+1)
    #
    # A_exp = [
    #     vec_ops.vec_tensordot(axb_expansion[o], pseudo_norm_2, axes=[-1, -1], shared=shared)
    #         if len(axb_expansion) > o and not is_zero(axb_expansion[o])  else
    #     0
    #     for o in order
    # ]
    # B_exp = [
    #     vec_ops.vec_tensordot(B_exp[o], pseudo_norm_2, axes=[-1, -1], shared=shared)
    #         if len(B_exp) > o and not is_zero(B_exp[o]) else
    #     0
    #     for o in order
    # ]
    # pseudonorm_expansion = [
    #     a-b
    #     for a,b in zip(A_exp, B_exp)
    # ]
    #
    # return pseudonorm_expansion
def is_expansion_like(expansion):
    """
    **LLM Docstring**

    Test whether an object looks like an expansion (a sequence of numeric arrays)
    rather than a single array or scalar.

    :param expansion: the object to test
    :type expansion: Any
    :return: whether the object is expansion-like
    :rtype: bool
    """
    #TODO: make this check shapes too
    return (
        not isinstance(expansion, np.ndarray)
        and not is_numeric(expansion[0])
        and not is_numeric_array_like(expansion)
    ) and all(is_numeric_array_like(a) for a in expansion)
def vec_anglesin_deriv(A_expansion, B_expansion, order, unitized=False, return_unit_vectors=True, planar=None,
                       up_vector=None,
                       component_vectors=None,
                       unit_expansions=None,
                       planar_threshold=None):
    """
    **LLM Docstring**

    Compute the derivative expansion of the sine of the angle between two vectors
    (the norm of the cross product of their unit vectors), with sign and planar
    handling.

    Non-planar structures use the cross-product norm directly; planar (parallel)
    structures fall back to `vec_parallel_cross_norm_deriv`; mixed batches are
    computed separately and merged. An `up_vector` supplies the sign convention, and
    the unit normal vectors can optionally be returned.

    :param A_expansion: expansion of the first vector
    :type A_expansion: list
    :param B_expansion: expansion of the second vector
    :type B_expansion: list
    :param order: the derivative order(s)
    :type order: int | list[int]
    :param unitized: whether the inputs are already unit vectors
    :type unitized: bool
    :param return_unit_vectors: also return the unit normal expansion
    :type return_unit_vectors: bool
    :param planar: force (or disable) the planar branch (auto-detected if `None`)
    :type planar: bool | np.ndarray | None
    :param up_vector: up vector defining the sign convention
    :type up_vector: np.ndarray | list | None
    :param component_vectors: the surrounding edge-vector expansions (planar case)
    :type component_vectors: list | None
    :param unit_expansions: precomputed unit-norm expansions (planar case)
    :type unit_expansions: list | None
    :param planar_threshold: cross-norm threshold for detecting planarity
    :type planar_threshold: float | None
    :return: the sine expansion (and unit normals if requested)
    :rtype: list | tuple
    """
    if is_numeric(order):
        max_order = order
    else:
        max_order = max(order)
    if not unitized:
        A_expansion = vec_norm_unit_deriv(A_expansion, max_order)[1]
        B_expansion = vec_norm_unit_deriv(B_expansion, max_order)[1]

    if planar_threshold is None:
        planar_threshold = Options.zero_threshold
    if not planar:
        vec_cross = vec_cross_deriv(A_expansion, B_expansion, order=max_order)
        if planar is None:
            planar = np.linalg.norm(vec_cross[0], axis=-1) <= planar_threshold
    else:
        vec_cross = None

    if up_vector is not None:
        if not is_expansion_like(up_vector):
            up_vector = [up_vector]
        up_vector = [np.asanyarray(u) for u in up_vector]
        up_vector = [
            np.broadcast_to(
                np.expand_dims(
                    u,
                    list(range(v.ndim - u.ndim))
                ),
                v.shape
            )
            for u,v in zip(up_vector, vec_cross)
        ]

    if np.all(planar):
        if component_vectors is not None or up_vector is not None:
            expansion = vec_parallel_cross_norm_deriv(A_expansion, B_expansion, order,
                                                      component_vectors=component_vectors,
                                                      up_vector_expansion=up_vector,
                                                      unit_expansions=unit_expansions
                                                      )
        else:
            raise ValueError("parallel vector angle derivative only supported for dihedrals")
        norms = expansion
        units = A_expansion
    elif np.any(planar):
        # gotta compute planar and nonplanar separately then remerge the tensors

        base_shape = A_expansion[0].shape[:-1]
        planar_pos = np.where(planar)
        nonplanar_pos = np.where(np.logical_not(planar))
        planar_A = [a[planar_pos] for a in A_expansion]
        planar_B = [b[planar_pos] for b in B_expansion]
        parallel_uv = None
        if component_vectors is not None:
            component_vectors = [
                [s[planar_pos] for s in S_expansion]
                for S_expansion in component_vectors
            ]
        elif up_vector is not None:
            parallel_uv = [u[planar_pos] for u in up_vector]
        if unit_expansions is not None:
            unit_expansions = [
                [s[planar_pos] for s in S_expansion]
                for S_expansion in unit_expansions
            ]
        expansion = vec_parallel_cross_norm_deriv(planar_A, planar_B, order,
                                                  component_vectors=component_vectors,
                                                  unit_expansions=unit_expansions,
                                                  up_vector_expansion=parallel_uv)
        planar_units = planar_A
        nonplanar_geoms = [v[nonplanar_pos] for v in vec_cross]
        norms, units = vec_norm_unit_deriv(nonplanar_geoms, order)
        if up_vector is not None:
            up_vector = up_vector[0]
            signs = np.sign(
                vec_ops.vec_tensordot(
                    nonplanar_geoms[0][..., np.newaxis, :],
                    up_vector[nonplanar_pos][..., :, np.newaxis],
                    axes=[-1, -2]
                )
            )
            signs = signs.reshape(signs.shape[:-2])
            norms = [v * np.expand_dims(signs, [-(x+1) for x in range(o)]) for o, v in enumerate(norms)]
            units = [v * np.expand_dims(signs, [-(x+1) for x in range(o+1)]) for o, v in enumerate(units)]

        final_tensors = [
            np.zeros(base_shape + e.shape[1:])
            for e in expansion
        ]
        for e,n,f in zip(expansion, norms, final_tensors):
            f[planar_pos] = e#[planar_pos]
            f[nonplanar_pos] = n#[nonplanar_pos]
        if return_unit_vectors:
            final_units = [
                np.zeros(base_shape + u.shape[1:])
                for u in units
            ]
            for e, n, f in zip(planar_units, units, final_units):
                f[planar_pos] = e#[planar_pos]
                f[nonplanar_pos] = n#[nonplanar_pos]

            units = final_units
        else:
            units = None
        norms = final_tensors
    else:
        norms, units = vec_norm_unit_deriv(vec_cross, order)
        if up_vector is not None:
            up_vector = np.asanyarray(up_vector)
            up_vector = np.expand_dims(
                up_vector,
                list(range((vec_cross[0].ndim - up_vector.ndim)))
            )
            signs = np.sign(
                vec_ops.vec_tensordot(
                    vec_cross[0][..., np.newaxis, :],
                    up_vector[..., :, np.newaxis],
                    axes=[-1, -2]
                )
            )
            signs = signs.reshape(signs.shape[:-2])
            norms = [v * np.expand_dims(signs, [-(x+1) for x in range(o)]) for o, v in enumerate(norms)]
            units = [v * np.expand_dims(signs, [-(x+1) for x in range(o+1)]) for o, v in enumerate(units)]

    if return_unit_vectors:
        return norms, units
    else:
        return norms

def arctan_expansion_term(angle, order):
    """
    **LLM Docstring**

    Build the order-`order` derivative tensor of `arctan2` viewed as a function of
    its `(cos, sin)` arguments, evaluated at a given angle.

    The entries are populated from the appropriate sine/cosine of `order * angle`
    with the correct factorial and sign per index pattern, over the unique
    permutations of each argument combination.

    :param angle: the angle at which to evaluate
    :type angle: np.ndarray
    :param order: the derivative order
    :type order: int
    :return: the arctan derivative-coefficient tensor
    :rtype: np.ndarray
    """
    e = np.asanyarray(np.sin(order*angle))
    o = np.asanyarray(np.cos(order*angle))
    if order%2 == 1:
        e, o = o, e
        c_nums = {0, 3}
    else:
        c_nums = {1, 2}
    array = np.empty(e.shape + (2,)*order, dtype=float)
    f = math.factorial(order-1)
    for combo in itertools.combinations_with_replacement(range(2), order):
        two_count = np.sum(combo)
        t = (e if (two_count % 2) == 1 else o) * f
        if two_count % 4 in c_nums:
            t = -t
        for p in get_unique_permutations(combo)[1]:
            i = (...,) + tuple(p)
            array[i] = t
    return array

def vec_angle_deriv(A_expansion, B_expansion, order, up_vector=None,
                    component_vectors=None,
                    unit_expansions=None,
                    unitized=False,
                    planar=None,
                    planar_threshold=None):
    """
    **LLM Docstring**

    Compute the derivative expansion of the angle between two vectors.

    Builds the cosine and sine expansions (`vec_anglecos_deriv`,
    `vec_anglesin_deriv`), takes the leading angle from `arctan2`, and forms the
    higher orders from `d(atan2) = cos*d(sin) - sin*d(cos)` via `scalarprod_deriv`.

    :param A_expansion: expansion of the first vector
    :type A_expansion: list
    :param B_expansion: expansion of the second vector
    :type B_expansion: list
    :param order: the derivative order(s)
    :type order: int | list[int]
    :param up_vector: up vector defining the sign convention
    :type up_vector: np.ndarray | None
    :param component_vectors: surrounding edge-vector expansions (planar case)
    :type component_vectors: list | None
    :param unit_expansions: precomputed unit-norm expansions (planar case)
    :type unit_expansions: list | None
    :param unitized: whether the inputs are already unit vectors
    :type unitized: bool
    :param planar: force (or disable) the planar branch
    :type planar: bool | np.ndarray | None
    :param planar_threshold: cross-norm threshold for detecting planarity
    :type planar_threshold: float | None
    :return: the angle expansion
    :rtype: list
    """
    if not unitized:
        units_A, A_expansion = vec_norm_unit_deriv(A_expansion, order)
        units_B, B_expansion = vec_norm_unit_deriv(B_expansion, order)
    cos_expansion = vec_anglecos_deriv(A_expansion, B_expansion, order, unitized=True)
    sin_expansion = vec_anglesin_deriv(A_expansion, B_expansion, order, unitized=True,
                                       up_vector=up_vector,
                                       component_vectors=component_vectors,
                                       unit_expansions=unit_expansions,
                                       return_unit_vectors=False,
                                       planar=planar,
                                       planar_threshold=planar_threshold)

    # for i in range(3):
    #     for j in range(i+1, 3):
    #         cos_expansion[2][3*i:3*(i+1), 3*j:3*(j+1)] = cos_expansion[2][3*i:3*(i+1), 3*j:3*(j+1)].T
    #         cos_expansion[2][3*j:3*(j+1), 3*i:3*(i+1)] = cos_expansion[2][3*j:3*(j+1), 3*i:3*(i+1)].T
    #         sin_expansion[2][3*i:3*(i+1), 3*j:3*(j+1)] = sin_expansion[2][3*i:3*(i+1), 3*j:3*(j+1)].T
    #         sin_expansion[2][3*j:3*(j+1), 3*i:3*(i+1)] = sin_expansion[2][3*j:3*(j+1), 3*i:3*(i+1)].T
    # print(cos_expansion[2])

    ang = np.arctan2(sin_expansion[0], cos_expansion[0])

    # cos_sin_expansion = [
    #     np.moveaxis(np.array([c, s]), 0, -1)
    #     for c, s in zip(cos_expansion, sin_expansion)
    # ]
    # angle_derivs = [ang] + (tensor_reexpand(
    #     cos_sin_expansion[1:],
    #     [arctan_expansion_term(ang, 1)],
    #     axes=[-1, -1],
    #     order=order,
    #     # shared=arctan_expansion[0].ndim - 1
    # ) if order > 0 else [])
    # return angle_derivs

    # print("???")
    # print(
    #     np.sum(np.abs(
    #         cos_expansion[2] - cos_expansion[2].T
    #     ))
    # )
    # print(
    #     (cos_expansion[0] * sin_expansion[3])[2][:3, :3]
    #     - (sin_expansion[0] * cos_expansion[3])[2][:3, :3]
    #     + nca_symmetrize(cos_expansion[1][:, np.newaxis, np.newaxis] * sin_expansion[2][np.newaxis, :, :], (1, 1))[2][:3, :3]
    #     # + (cos_expansion[1][:, np.newaxis, np.newaxis] * sin_expansion[2][np.newaxis, :, :])[2][:3, :3]
    #     - nca_symmetrize(sin_expansion[1][:, np.newaxis, np.newaxis] * cos_expansion[2][np.newaxis, :, :], (1, 1))[2][:3, :3]
    #     # - (sin_expansion[1][:, np.newaxis, np.newaxis] * cos_expansion[2][np.newaxis, :, :])[2][:3, :3]
    # )
    #
    # print(
    #     (cos_expansion[0] * sin_expansion[3])[2][:3, :3]
    #     - (sin_expansion[0] * cos_expansion[3])[2][:3, :3]
    #     + (cos_expansion[1][:, np.newaxis, np.newaxis] * sin_expansion[2][np.newaxis, :, :])[2][:3, :3]
    #     - (sin_expansion[1][:, np.newaxis, np.newaxis] * cos_expansion[2][np.newaxis, :, :])[2][:3, :3]
    # )

    # print("=oooo"*50)
    if order > 0:
        sc_expansion = scalarprod_deriv(cos_expansion, sin_expansion[1:], order-1)
        # print("=bbbb"*50)
        cs_expansion = scalarprod_deriv(sin_expansion, cos_expansion[1:], order-1)
    else:
        sc_expansion = []
        cs_expansion = []
    return [ang] + [
        s - c
        for s,c in zip(sc_expansion, cs_expansion)
    ]

    # huh_1 = angle_derivs
    #
    # print([h.shape for h in huh])
    # print([h1.shape for h1 in huh_1])

def vec_normal_deriv(A_expansion, B_expansion, order, up_vector=None,
                     component_vectors=None,
                     unit_expansions=None,
                     unitized=False,
                     planar=None,
                     planar_threshold=None,
                     normalize=True):
    """
    **LLM Docstring**

    Compute the derivative expansion of the normal vector to two vectors (the
    direction of their cross product), optionally normalized.

    When `normalize` is set the unit normal from `vec_anglesin_deriv` is returned;
    otherwise the raw cross-product expansion is returned.

    :param A_expansion: expansion of the first vector
    :type A_expansion: list
    :param B_expansion: expansion of the second vector
    :type B_expansion: list
    :param order: the derivative order(s)
    :type order: int | list[int]
    :param up_vector: up vector defining the sign convention
    :type up_vector: np.ndarray | None
    :param component_vectors: surrounding edge-vector expansions
    :type component_vectors: list | None
    :param unit_expansions: precomputed unit-norm expansions
    :type unit_expansions: list | None
    :param unitized: whether the inputs are already unit vectors
    :type unitized: bool
    :param planar: force (or disable) the planar branch
    :type planar: bool | np.ndarray | None
    :param planar_threshold: cross-norm threshold for detecting planarity
    :type planar_threshold: float | None
    :param normalize: return the unit normal rather than the raw cross product
    :type normalize: bool
    :return: the normal-vector expansion
    :rtype: list
    """

    if normalize:
        _, units = vec_anglesin_deriv(A_expansion, B_expansion, order,
                                      up_vector=up_vector,
                                      component_vectors=component_vectors,
                                      unit_expansions=unit_expansions,
                                      unitized=unitized,
                                      planar=planar,
                                      planar_threshold=planar_threshold,
                                      return_unit_vectors=True)
        return units
    else:
        if is_numeric(order):
            max_order = order
        else:
            max_order = max(order)
        if not unitized:
            A_expansion = vec_norm_unit_deriv(A_expansion, max_order)[1]
            B_expansion = vec_norm_unit_deriv(B_expansion, max_order)[1]

        vec_cross = vec_cross_deriv(A_expansion, B_expansion, order=max_order)
        return vec_cross

def vec_dihed_deriv(A_expansion, B_expansion, C_expansion, order,
                    B_norms=None, planar=None, planar_threshold=None, up_vector=None):
    """
    **LLM Docstring**

    Compute the derivative expansion of a dihedral angle from the three edge-vector
    expansions that define it.

    Forms the two plane normals (`b x a`, `b x c`), unitizes them, handles colinear
    degeneracies by perturbing along an up vector, and takes the signed angle
    between the normals with `vec_angle_deriv`. A `pi` shift is applied to match the
    Gaussian sign convention.

    :param A_expansion: expansion of the first edge vector
    :type A_expansion: list
    :param B_expansion: expansion of the central edge vector
    :type B_expansion: list
    :param C_expansion: expansion of the third edge vector
    :type C_expansion: list
    :param order: the derivative order(s)
    :type order: int | list[int]
    :param B_norms: precomputed norm expansion of the central vector
    :type B_norms: list | None
    :param planar: force (or disable) the planar branch
    :type planar: bool | np.ndarray | None
    :param planar_threshold: cross-norm threshold for detecting planarity
    :type planar_threshold: float | None
    :param up_vector: up vector for resolving fully colinear inputs
    :type up_vector: np.ndarray | None
    :return: the dihedral-angle expansion
    :rtype: list
    """
    # quick check

    if is_numeric(order):
        max_order = order
    else:
        max_order = max(order)

    if B_norms is None:
        B_norms, B_expansion = vec_norm_unit_deriv(B_expansion, len(B_expansion))
    # if not unitized:
    #     _, A_expansion = vec_norm_unit_deriv(A_expansion, len(A_expansion))
    #     _, B_expansion = vec_norm_unit_deriv(B_expansion, len(B_expansion))
    #     _, C_expansion = vec_norm_unit_deriv(C_expansion, len(C_expansion))
    n1_expansion = vec_cross_deriv(B_expansion, A_expansion, max_order)
    n2_expansion = vec_cross_deriv(B_expansion, C_expansion, max_order)
    # print("..."*10, "axb")
    # print(n1_expansion[0])
    n1_norms, axb_expansion = vec_norm_unit_deriv(n1_expansion, order, raise_on_failure=False)
    n2_norms, bxc_expansion = vec_norm_unit_deriv(n2_expansion, order, raise_on_failure=False)
    if n1_norms is None:
        zt = Options.zero_threshold + 1e-12
        if n2_norms is None:
            # they're all parallel, we have not up vector
            if up_vector is None:
                raise ValueError("can't get a dihedral for four points in a line without an `up_vector`")
            A_expansion[0] = A_expansion[0] + 2*zt * vec_ops.vec_crosses(up_vector, A_expansion[0], normalize=True)
            n1_expansion = vec_cross_deriv(B_expansion, A_expansion, max_order)
            n1_norms, axb_expansion = vec_norm_unit_deriv(n1_expansion, order)
            C_expansion[0] = C_expansion[0] - 2*zt * vec_ops.vec_crosses(up_vector, A_expansion[0], normalize=True)
            n2_expansion = vec_cross_deriv(B_expansion, C_expansion, max_order)
            n2_norms, bxc_expansion = vec_norm_unit_deriv(n2_expansion, order)
        else:
            # A and B are parallel, we add just enough noise to break the colinearity
            A_expansion[0] = A_expansion[0] + 2*zt * vec_ops.vec_normalize(C_expansion[0])
            n1_expansion = vec_cross_deriv(B_expansion, A_expansion, max_order)
            n1_norms, axb_expansion = vec_norm_unit_deriv(n1_expansion, order)
    if n2_norms is None:
        zt = Options.zero_threshold + 1e-12
        # C and B are parallel, we add just enough noise to break the colinearity
        C_expansion[0] = C_expansion[0] + 2 * zt * vec_ops.vec_normalize(A_expansion[0])
        n2_expansion = vec_cross_deriv(B_expansion, C_expansion, max_order)
        n2_norms, bxc_expansion = vec_norm_unit_deriv(n2_expansion, order)


    # B_norms, up_expansion = vec_norm_unit_deriv(B_expansion, len(B_expansion))
    base_derivs = vec_angle_deriv(axb_expansion, bxc_expansion, order, unitized=True,
                                  # up_vector=None
                                  up_vector=B_expansion[0],
                                  unit_expansions=[B_norms, n1_norms, n2_norms],
                                  component_vectors=[A_expansion, B_expansion, C_expansion],
                                  planar=planar,
                                  planar_threshold=planar_threshold
                                  )
    # add in the np.pi shift to account for imposed sign flip in standard imp. to match Gaussian
    base_derivs[0] = np.pi - base_derivs[0]
    return base_derivs
    # return [-x for x in base_derivs]

def vec_plane_angle_deriv(A_expansion, B_expansion, C_expansion, D_expansion, order, planar=None, planar_threshold=None):
    """
    **LLM Docstring**

    Compute the derivative expansion of the angle between two planes, each defined
    by a pair of vector expansions.

    Forms the two plane normals via cross products and takes the angle between them
    with `vec_angle_deriv`.

    :param A_expansion: first vector of plane 1
    :type A_expansion: list
    :param B_expansion: second vector of plane 1
    :type B_expansion: list
    :param C_expansion: first vector of plane 2
    :type C_expansion: list
    :param D_expansion: second vector of plane 2
    :type D_expansion: list
    :param order: the derivative order(s)
    :type order: int | list[int]
    :param planar: force (or disable) the planar branch
    :type planar: bool | np.ndarray | None
    :param planar_threshold: cross-norm threshold for detecting planarity
    :type planar_threshold: float | None
    :return: the plane-angle expansion
    :rtype: list
    """
    # quick check

    if is_numeric(order):
        max_order = order
    else:
        max_order = max(order)

    axb_expansion = vec_cross_deriv(A_expansion, B_expansion, max_order)
    cxd_expansion = vec_cross_deriv(C_expansion, D_expansion, max_order)

    return vec_angle_deriv(axb_expansion, cxd_expansion, order, unitized=False,
                           planar=planar,
                           planar_threshold=planar_threshold
                           # planar_threshold=planar_threshold
                           )


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

    return np.round(np.prod(multinomial_num / full_denom))

max_symm_perm_order = 4
unique_permutation_cache = {}
def get_unique_permutations(perm_idx):
    """
    **LLM Docstring**

    Return the unique permutations of an index multiset (with their indices),
    cached across calls for small multisets.

    :param perm_idx: the index multiset to permute
    :type perm_idx: Sequence[int]
    :return: the unique permutations and their indices
    :rtype: tuple
    """
    from ..Combinatorics import UniquePermutations
    key = tuple(perm_idx) if len(perm_idx) <= max_symm_perm_order else None

    return dev.cached_eval(
        unique_permutation_cache,
        key,
        lambda perm_idx:UniquePermutations(perm_idx).permutations(return_indices=True),
        condition=lambda k:k is not None and len(k) <= max_symm_perm_order,
        args=(perm_idx,)
    )
def get_nca_perm_iter(partition, identical=True):
    """
    **LLM Docstring**

    Generate the reduced set of symmetrizing permutations for an integer partition
    (the identical-operand case).

    Builds the block permutation from the partition's repeated blocks and yields the
    distinct orderings needed to symmetrize a partition term without overcounting.

    :param partition: the integer partition
    :type partition: Sequence[int]
    :param identical: whether the operands are identical (only case implemented)
    :type identical: bool
    :return: a generator of permutation-index arrays
    :rtype: Iterator[np.ndarray]
    """
    if identical:
        blocks, counts = np.unique(partition, return_counts=True)
        base_perm = sum([(b,) * (b*c) for b,c in zip(blocks, counts)], ())
        inv_perm = np.argsort(sum([(b,) * b for b in partition], ()))
    else:
        raise NotImplementedError("just use unique perms")
    base_perm_inds, _ = get_unique_permutations(base_perm)
    sub_ind_blocks = []
    padding = 0
    for b,c in zip(blocks, counts):
        if c == 1 or b == 1:
            sub_perm_inds = np.arange(b*c)[np.newaxis]
        else:
            # if len(c)
            sub_perm = sum([(c-i,) * b for i in range(c)], ())
            sub_perm_inds, _ = get_unique_permutations(sub_perm)
            inv_inds = np.argsort(sub_perm_inds, axis=1)
            filter_inds = [
                np.min(inv_inds[:, b*i:b*(i+1)], axis=1)
                for i in range(c)
            ]
            ord_filter = np.all(np.diff(filter_inds, axis=0) > 0, axis=0)
            sub_perm_inds = sub_perm_inds[ord_filter,]
        sub_ind_blocks.append(padding+sub_perm_inds)
        padding += b*c

    for block_list in itertools.product(*sub_ind_blocks):
        sublist = np.concatenate(block_list)
        p = set_ops.vector_take(sublist[inv_perm], base_perm_inds)
        yield p
def check_perm_sorting(block_counts, partition_inverse):
    """
    **LLM Docstring**

    Predicate testing whether a permutation respects the canonical ordering of a
    partition's repeated blocks.

    Used to filter permutations so that interchangeable blocks appear in a fixed
    canonical order, avoiding double counting during symmetrization.

    :param block_counts: the `(blocks, counts)` describing the partition
    :type block_counts: tuple
    :param partition_inverse: the inverse permutation to test
    :type partition_inverse: np.ndarray
    :return: whether the permutation is canonically sorted
    :rtype: bool
    """
    p = 0
    for b,c in zip(*block_counts):
        if c > 1:
            if any(
                    np.min(partition_inverse[p+b*i:p+b*(i+1)]) <
                    np.min(partition_inverse[p+b*(i+1):p+b*(i+2)])
                for i in range(c - 1)
            ):
                return False

        p += b*c

    return True

def get_nca_perm_idx(partition, contract=True, identical=False):
    """
    **LLM Docstring**

    Build the permutation-index label list for an integer partition, marking which
    derivative axes are interchangeable.

    Axes belonging to blocks of size greater than one (or, when operands are not
    identical, every block) share a label so the symmetrizer knows which axes to
    permute together.

    :param partition: the integer partition
    :type partition: Sequence[int]
    :param contract: whether the operation contracts axes
    :type contract: bool
    :param identical: whether the operands are identical
    :type identical: bool
    :return: the permutation-index label list
    :rtype: list[int]
    """
    perm_counter = len(partition)
    perm_idx = []  # to establish the set of necessary permutations to make things symmetric
    for i in partition:
        if (not identical) or i > 1:
            perm_idx.extend([perm_counter] * i)
            perm_counter -= 1
        else:
            perm_idx.append(perm_counter)
    return perm_idx
def get_nca_symmetrizing_perms(partition,
                               perm_idx=None,
                               use_base_perms=True,
                               filter_unique=False,
                               contract=True,
                               identical=False):
    """
    **LLM Docstring**

    Return the set of permutations (and any compensating scaling) used to symmetrize
    a partition term over its derivative axes.

    By default uses the reduced base-permutation set from `get_nca_perm_iter`; the
    alternative branches (unique-permutation filtering) are retained but disabled.

    :param partition: the integer partition
    :type partition: Sequence[int]
    :param perm_idx: the permutation-index labels (computed if omitted)
    :type perm_idx: list[int] | None
    :param use_base_perms: use the reduced base-permutation generator
    :type use_base_perms: bool
    :param filter_unique: (disabled) filter unique permutations by canonical sorting
    :type filter_unique: bool
    :param contract: whether the operation contracts axes
    :type contract: bool
    :param identical: whether the operands are identical
    :type identical: bool
    :return: `(permutation_indices, scaling)`
    :rtype: tuple
    """
    if perm_idx is None:
        perm_idx = get_nca_perm_idx(partition, contract=contract, identical=identical)

    nterms = nca_partition_terms(partition)
    if use_base_perms:
        perm_inds = np.concatenate(list(get_nca_perm_iter(partition, identical=identical)), axis=0)
        scaling = 1
        if len(perm_inds) != nterms:
            raise ValueError(f"mismatch between reduced perms and actual number, expected {nterms}, got {len(perm_inds)} for partition {partition}")
    elif filter_unique:
        raise Exception("?")
        all_perm_inds, _ = get_unique_permutations(perm_idx)
        counts = np.unique(partition, return_counts=True)
        inv_perms = np.argsort(all_perm_inds, axis=1)
        perm_inds = np.array([
            p
            for p, i in zip(all_perm_inds, inv_perms)
            if check_perm_sorting(counts, i)
        ])
        scaling = 1
        if len(perm_inds) != nterms:
            raise ValueError(f"mismatch between reduced perms and actual number, expected {nterms}, got {len(perm_inds)} for partition {partition}")
    else:
        raise Exception("?")
        perm_inds, _ = get_unique_permutations(perm_idx)
        overcount = len(perm_inds) / nterms
        scaling = 1 / overcount

    return perm_inds, scaling

def nca_symmetrize(tensor, partition,
                   shared=None,
                   identical=False,
                   contract=True,
                   use_base_perms=True,
                   filter_unique=False,
                   check_symmetry=False,
                   reweight=None):
    """
    **LLM Docstring**

    Symmetrize a tensor over its derivative axes according to an integer
    partition.

    Sums the tensor over the permutations of the interchangeable derivative axes
    (from `get_nca_symmetrizing_perms` or the full unique-permutation set), applying
    any compensating reweighting; the leading `shared` batch axes are held fixed. An
    optional `check_symmetry` pass verifies the result.

    :param tensor: the tensor to symmetrize
    :type tensor: np.ndarray
    :param partition: the integer partition describing the derivative-axis blocks
    :type partition: Sequence[int]
    :param shared: number of shared leading batch axes
    :type shared: int | None
    :param identical: whether the contributing operands are identical
    :type identical: bool
    :param contract: whether the underlying operation contracts axes
    :type contract: bool
    :param use_base_perms: use the reduced base-permutation generator
    :type use_base_perms: bool
    :param filter_unique: (disabled) filter unique permutations
    :type filter_unique: bool
    :param check_symmetry: verify the symmetrized result
    :type check_symmetry: bool
    :param reweight: force (or disable) the overcount reweighting
    :type reweight: bool | None
    :return: the symmetrized tensor
    :rtype: np.ndarray
    """

    perm_idx = get_nca_perm_idx(partition, contract=contract, identical=identical)
    # sometimes we overcount, so we factor that out here
    if reweight or (reweight is None and identical):
        perm_inds, scaling = get_nca_symmetrizing_perms(partition, perm_idx,
                                                        filter_unique=filter_unique,
                                                        use_base_perms=use_base_perms,
                                                        identical=identical)
        tensor = tensor * scaling
    else:
        perm_inds, _ = get_unique_permutations(perm_idx)
        inv_perm = np.argsort(np.argsort(perm_idx))
        # perm_inds = inv_perm[perm_inds]

    if shared is None:
        shared = 0
        perm_inds = [
            list(p) + list(range(len(p), tensor.ndim))
            for p in perm_inds
        ]
    else:
        l = list(range(shared))
        perm_inds = [
            l + [shared + pp for pp in p] + list(range(shared+len(p), tensor.ndim))
            for p in perm_inds
        ]

    t = sum(
        tensor.transpose(p)
        for p in perm_inds
    )

    if check_symmetry:
        for p in itertools.permutations(
                range(shared, shared + sum(partition)),
                int(sum(partition))
        ):
            p = tuple(range(shared)) + p + tuple(range(shared + sum(partition), t.ndim))
            diff = t - np.transpose(t, p)
            m = np.max(np.abs(diff))
            # r = m / np.max(np.abs(t))
            if m > 1e-8 and np.max(np.abs(t)) < 1e6:
                # with np.printoptions(suppress=True, linewidth=1e8):
                #     print(tensor)
                #     print("   ", "."*20)
                #     print(t)
                print("|", t.shape)
                print("|", partition, p, perm_idx)
                print("|", perm_inds)
                raise ValueError("symmetry error")

    return t

def nca_partition_dot(partition, A_expansion, B_expansion, axes=None, shared=None, identical=False, symmetrize=True):
    """
    **LLM Docstring**

    Contract the chain of first-operand derivative terms selected by an integer
    partition into the matching second-operand derivative term.

    Implements one Faà di Bruno chain-rule term: a `B` derivative of order
    `len(partition)` is contracted successively against the `A` derivatives whose
    orders are given by the partition entries, then symmetrized.

    :param partition: the integer partition selecting the derivative orders
    :type partition: Sequence[int]
    :param A_expansion: the inner (chained) expansion
    :type A_expansion: list
    :param B_expansion: the outer expansion
    :type B_expansion: list
    :param axes: the contraction axes
    :type axes: list | None
    :param shared: number of shared leading batch axes
    :type shared: int | None
    :param identical: whether the operands are identical
    :type identical: bool
    :param symmetrize: whether to symmetrize the result
    :type symmetrize: bool
    :return: the partition term (or `0` when out of range/zero)
    :rtype: np.ndarray | int
    """
    if axes is None:
        axes = [-1, (0 if shared is None else shared)]
    if len(B_expansion) <= len(partition) - 1:
        return 0
    B = B_expansion[len(partition) - 1]
    if is_numeric(B) and B == 0:
        return 0
    a_ax, b_ax = [[x] if is_numeric(x) else x for x in axes]
    b_ax = [
        (B.ndim + b - (len(partition) - 1))
            if b < 0 else
        b #+ (len(partition) - 1)
        for b in b_ax
    ]
    # account for increasing dimension with longer partitions
    for i in reversed(partition):
        if len(A_expansion) <= i - 1:
            return 0
        A = A_expansion[i - 1]
        if is_numeric(A) and A == 0:
            return 0
        if shared is None:
            B = np.tensordot(A, B, axes=[a_ax, b_ax])
        else:
            B = vec_ops.vec_tensordot(A, B, axes=[a_ax, b_ax], shared=shared)
        b_ax = [min(B.ndim - 1, b + A.ndim - 1 - shared) for b in b_ax]

    if symmetrize is not None:
        symmetrize = len(A_expansion) > 1 and len(B_expansion) > 1

    if symmetrize:
        B = nca_symmetrize(B, partition, identical=identical, shared=shared)
    return B

def nca_partition_prod(partition, A_expansion, shared=None, symmetrize=True):
    """
    **LLM Docstring**

    Form the symmetrized outer product of the first-operand derivative terms
    selected by an integer partition.

    The outer-product analogue of `nca_partition_dot`, used by the scalar
    power/reciprocal derivatives.

    :param partition: the integer partition selecting the derivative orders
    :type partition: Sequence[int]
    :param A_expansion: the expansion to draw terms from
    :type A_expansion: list
    :param shared: number of shared leading batch axes
    :type shared: int | None
    :param symmetrize: whether to symmetrize the result
    :type symmetrize: bool
    :return: the partition product term (or `0` when out of range/zero)
    :rtype: np.ndarray | int
    """
    i = partition[0]
    if len(A_expansion) <= i - 1:
        return 0
    A = A_expansion[i - 1]
    if is_numeric(A) and A == 0:
        return 0

    B = A
    for i in partition[1:]:
        if len(A_expansion) <= i - 1:
            return 0
        A = A_expansion[i - 1]
        if is_numeric(A) and A == 0:
            return 0
        if shared is not None:
            axes = [list(range(shared, B.ndim)), list(range(shared, A.ndim))]
        else:
            axes = [list(range(B.ndim)), list(range(A.ndim))]

        B = vec_ops.vec_outer(B, A, axes=axes, order=0)
    if symmetrize:
        B = nca_symmetrize(B, partition, shared=shared)
    return B

def tensor_reexpand(derivs, vals, order=None, axes=None):
    """
    **LLM Docstring**

    Re-express one derivative expansion through another via the Faà di Bruno chain
    rule.

    Given the outer expansion `derivs` (derivatives with respect to an intermediate
    quantity) and the inner expansion `vals` (derivatives of that quantity with
    respect to the true variables), returns the expansion of the composition by
    summing the partition terms at each order.

    :param derivs: the outer (to-be-re-expanded) expansion
    :type derivs: list
    :param vals: the inner expansion supplying the new variables
    :type vals: list
    :param order: the derivative order(s) (defaults to `len(vals)`)
    :type order: int | list[int] | None
    :param axes: the contraction axes for the chain-rule products
    :type axes: list | None
    :return: the re-expanded expansion
    :rtype: list
    """
    terms = []
    if order is None:
        order = len(vals)

    derivs = [
        np.asanyarray(d) if not is_zero(d) else d
        for d in derivs
    ]
    shared = 0
    for i,d in enumerate(derivs):
        if not is_zero(d):
            shared = d.ndim - (i + 2)
            break

    vals = [
        np.asanyarray(d) if not is_zero(d) else d
        for d in vals
    ]

    if is_numeric(order): order = list(range(1, order+1))

    for o in order:
        term = sum(
            nca_partition_dot(p, derivs, vals, axes=axes, identical=True, shared=shared)
            for parts in get_integer_partitions(o)
            for p in parts
        )
        if not is_zero(term):
            # if we are transforming beyond axis zero in the target array, need
            # to shift the new axes back
            if axes is not None:
                target = axes[-1]
                if target > 0:
                    target = target + (o - 1) # indexes past end of array otherwise
                for i in range(o):
                    term = np.moveaxis(term, shared, target)
        terms.append(term)

    return terms

def optimizing_transformation(expansion, order):
    """
    **LLM Docstring**

    Build, order by order, the transformation that brings an expansion to a
    normal (optimizing) form.

    Uses the leading gradient/Hessian to set the zeroth-order transform, then
    Newton-style recurrences that re-expand the remaining terms and cancel them at
    each order. Requires at least a gradient or Hessian.

    :param expansion: the expansion to optimize
    :type expansion: list
    :param order: the derivative order
    :type order: int
    :return: the optimizing transformation expansion
    :rtype: list
    """
    V = expansion

    zero_order = 0
    for v in V:
        if is_zero(v):
            zero_order += 1
        else:
            break

    if zero_order > 2:
        raise ValueError("can't optimize without gradient or Hessian (tensor inverses not implemented)")

    W = V[zero_order]
    if zero_order == 0:
        w = W
        Q = [np.eye(V[1].shape[0])]
    elif zero_order == 1 and np.allclose(np.diag(np.diag(W)), W):
        Q = [np.eye(V[1].shape[0])]
        w = np.diag(W)
    else:
        Q = [np.linalg.inv(W)]
        w = np.ones(len(W))

    for o in range(1, order + 1):
        V_rem = tensor_reexpand(Q, V, [o], axes=[-1, 0])[-1]
        w = w[np.newaxis]
        new_Q = -V_rem / ((o + 2) * w)
        Q = Q + [new_Q]

    return Q

def apply_nca_multi_ops(partition, expansions, ops, shared, root_dim=2):
    """
    **LLM Docstring**

    Evaluate a single partition term of a chained multi-operand tensor operation
    (the generalized Leibniz rule over more than two operands).

    Walks the chain of operands, applying each operation (contraction or product)
    at the derivative orders given by the partition, moving new derivative axes into
    place, and symmetrizing over the non-trivial blocks at the end.

    :param partition: the per-operand derivative orders
    :type partition: Sequence[int]
    :param expansions: the operand expansions
    :type expansions: list[list]
    :param ops: the `[op, axes, contract]` specifications between operands
    :type ops: list
    :param shared: number of shared leading batch axes
    :type shared: int | None
    :param root_dim: number of trailing (non-derivative) core axes of the first operand
    :type root_dim: int
    :return: the partition term (or `0` when out of range/zero)
    :rtype: np.ndarray | int
    """
    terms = [
        e[p] if len(e) > p else 0
        for e,p in zip(expansions, partition)
    ]
    if any(is_numeric(t) and t == 0 for t in terms): return 0

    if shared is None: shared = 0

    A = terms[0]
    d0 = expansions[0][0].ndim
    d = A.ndim - root_dim - shared
    scaling = 2 if len(partition) == 3 and tuple(partition) == (1, 0, 1) else 1
    for B,p,(op, axes, contract) in zip(terms[1:], partition[1:], ops):
        a_ax, b_ax = [[x] if is_numeric(x) else x for x in axes]
        a_ax = [a if a >= 0 else (A.ndim + a - d) for a in a_ax]
        b_ax = [b if b >= 0 else (B.ndim + b - p) for b in b_ax]
        if contract: # axes disappear, so we just account for the shifts
            axes = [
                [x+d for x in a_ax],
                [x+p for x in b_ax]
            ]
            deriv_axis = A.ndim - len(a_ax)
        else: # axes appeared, so we need to include those in the product
              # we _forced_ axes to be at the end of the arrays since it was too hard
              # to keep track of them otherwise...
              # actually I guess I could have put the derivative axes at the end...
              # and then the axes would never change...but that has other complications
            axes = [
                [shared + i for i in range(d)] + [x+d for x in a_ax],
                [shared + i for i in range(p)] + [x+p for x in b_ax]
            ]
            # if B.ndim < A.ndim:
            #     B = np.expand_dims(B, list(range(B.ndim - A.ndim, 0, 1)))
            # elif A.ndim < B.ndim:
            #     A = np.expand_dims(A, list(range(A.ndim - B.ndim, 0, 1)))
            deriv_axis = A.ndim
        _as = A.shape
        if shared == 0:
            A = op(A, B, axes=axes)
        else:
            A = op(A, B, axes=axes, shared=shared)
        # next we need to move all of the derivative axes in the second tensor to the beginning
        # so we can symmetrize

        for i in range(p):
            A = np.moveaxis(A, deriv_axis+i, deriv_axis - root_dim)
        d += B.ndim - root_dim - shared
    partition = [p for p in partition if p > 0]
    if len(partition) > 1:
        A = nca_symmetrize(A, partition, shared=shared, identical=False)
    return A
def nca_multi_op_order_deriv(partition_generator, order, expansions, ops, shared, root_dim):
    """
    **LLM Docstring**

    Assemble the full order-`order` derivative of a chained multi-operand operation
    by summing over all partitions of `order`.

    :param partition_generator: generator of the partitions (symmetric-group terms)
    :type partition_generator: caching_perm_generator
    :param order: the derivative order
    :type order: int
    :param expansions: the operand expansions
    :type expansions: list[list]
    :param ops: the `[op, axes, contract]` specifications
    :type ops: list
    :param shared: number of shared leading batch axes
    :type shared: int | None
    :param root_dim: number of trailing core axes of the first operand
    :type root_dim: int
    :return: the order-`order` derivative tensor
    :rtype: np.ndarray | int
    """
    full = None
    for part in partition_generator.get_terms(order):
        term = apply_nca_multi_ops(part, expansions, ops, shared, root_dim)
        if full is None:
            full = term
        else:
            full = full + term
    return full

def nca_canonicalize_multiops(expansion_op_pairs):
    """
    **LLM Docstring**

    Parse an alternating `(expansion, op, expansion, op, ..., expansion)` argument
    sequence into canonical operand and operation lists.

    Each operation may be given as a string (`'.'`/`'dot'`/`'x'`/`'prod'`, ...), an
    axes specification, a dict, or an `[op, axes, contract]` tuple; this normalizes
    them all into `[callable, axes, contract]` triples.

    :param expansion_op_pairs: the alternating expansions and operation specs
    :type expansion_op_pairs: Sequence
    :return: `(expansions, ops)`
    :rtype: tuple[list, list]
    """
    if len(expansion_op_pairs) % 2 == 0: raise ValueError("invalid number of operations/expansions")

    expansions = []
    ops = []
    for i, t in enumerate(expansion_op_pairs):
        if i % 2 == 0:
            expansions.append([np.asanyarray(A) for A in t])
        else:
            op = None
            axes = None
            contract = None
            if isinstance(t, dict):
                op = t.get('op', None)
                axes = t.get('axes', None)
                contract = t.get('contract', None)
            elif isinstance(t, str):
                op = t
            elif is_numeric(t[0]) or is_numeric(t[0][0]):
                axes = t
            else:
                op = t[0]
                if len(t) > 1: axes = t[1]
                if len(t) > 2: contract = t[2]

            if op is None and axes is not None:
                op = '.'

            if isinstance(op, str):
                if op in {'.', 'dot', 'contract', 'inner'}:
                    op = _contract
                    if axes is None: axes = [-1, 0]
                    if contract is None: contract = True
                elif op in {'x', 'prod', 'product', 'outer'}:
                    op = _product
                    if axes is None: axes = 'all'
                    if contract is None: contract = False
                # elif op in {'*', 'sprod', 'scalar_product'}:
                #     op = _scalar_prod
                #     if axes is None: axes = 'all'
                #     if contract is None: contract = False
                else:
                    raise ValueError(f"can't canonicalize operation {op}")

            if contract is None:
                contract = op is _contract

            ops.append([op, axes, contract])

    return expansions, ops

def _contract(a, b, axes=None, shared=None):
    """
    **LLM Docstring**

    Contraction operation used by the multi-operand machinery — a shared-axis
    `vec_tensordot` when `shared` is given, else a plain `np.tensordot`.

    :param a: the first operand
    :type a: np.ndarray
    :param b: the second operand
    :type b: np.ndarray
    :param axes: the contraction axes
    :type axes: list | None
    :param shared: number of shared leading batch axes
    :type shared: int | None
    :return: the contracted tensor
    :rtype: np.ndarray
    """
    if shared is not None:
        res = vec_ops.vec_tensordot(a, b, axes=axes, shared=shared)
    else:
        res = np.tensordot(a, b, axes=axes)
    return res
def _product(a, b, axes=None, shared=None):
    """
    **LLM Docstring**

    Outer-product operation used by the multi-operand machinery (a `vec_outer`).

    :param a: the first operand
    :type a: np.ndarray
    :param b: the second operand
    :type b: np.ndarray
    :param axes: the product axes
    :type axes: list | None
    :param shared: unused (kept for signature parity)
    :type shared: int | None
    :return: the outer-product tensor
    :rtype: np.ndarray
    """
    return vec_ops.vec_outer(a, b, axes=axes, order=0)

generator_max_caching_order = 4
term_generator_caches = {}
class caching_perm_generator:
    def __init__(self, o):
        """
        **LLM Docstring**

        Set up a symmetric-group term generator for `o` operands, backed by a per-order
        cache.

        :param o: the number of operands (symmetric-group order)
        :type o: int
        """
        from ..Combinatorics import SymmetricGroupGenerator
        self.gen = SymmetricGroupGenerator(o)
        self._term_cache = {}

    def get_terms(self, order):
        """
        **LLM Docstring**

        Return the partition/permutation terms for a given derivative order, caching the
        result.

        :param order: the derivative order
        :type order: int
        :return: the terms for that order
        :rtype: list
        """
        return dev.cached_eval(
            self._term_cache,
            order,
            self.gen.get_terms,
            args=(order,)
        )

def get_term_generator(k):
    """
    **LLM Docstring**

    Return a `caching_perm_generator` for `k` operands, cached for small `k`.

    :param k: the number of operands
    :type k: int
    :return: the (cached) term generator
    :rtype: caching_perm_generator
    """

    return dev.cached_eval(
        term_generator_caches,
        k,
        caching_perm_generator,
        condition=lambda k:k<generator_max_caching_order,
        args=(k,)
    )

def tensorops_deriv(
        *expansion_op_pairs,
        order,
        shared=None
):
    """
    **LLM Docstring**

    Compute the derivative expansion of an arbitrary chain of tensor operations
    applied to several expansions.

    Canonicalizes the alternating `(expansion, op, expansion, ...)` arguments,
    resolves any symbolic axis specifications, and sums the multi-operand Leibniz
    terms over all partitions at each requested order.

    :param expansion_op_pairs: alternating expansions and operation specs
    :type expansion_op_pairs: Sequence
    :param order: the derivative order(s)
    :type order: int | list[int]
    :param shared: number of shared leading batch axes
    :type shared: int | None
    :return: the chained-operation derivative expansion
    :rtype: list
    """
    expansions, ops = nca_canonicalize_multiops(expansion_op_pairs)
    _ = []
    for i,(op, axes, contract) in enumerate(ops):
        if isinstance(axes, str): axes = [axes, axes]
        a_ax, b_ax = axes
        A = expansions[i][0]
        B = expansions[i+1][0]
        if isinstance(a_ax, str):
            if a_ax == 'all':
                a_ax = list(range(shared, A.ndim))
            else:
                raise ValueError(f"bad axes spec '{a_ax}'")
        if isinstance(b_ax, str):
            if b_ax == 'all':
                b_ax = list(range(shared, B.ndim))
            else:
                raise ValueError(f"bad axes spec '{b_ax}'")
        _.append([op, [a_ax, b_ax], contract])
    ops = _


    if isinstance(order, int):
        order = list(range(order+1))

    partition_generator = get_term_generator(len(expansions))
    derivs = [
        nca_multi_op_order_deriv(partition_generator, o, expansions, ops, shared,
                                 root_dim=expansions[0][0].ndim - (0 if shared is None else shared)
                                 )
        for o in order
    ]

    return derivs
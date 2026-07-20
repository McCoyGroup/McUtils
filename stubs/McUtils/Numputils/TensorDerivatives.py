import collections
import itertools, numpy as np, math
from .. import Devutils as dev
from . import PermutationOps as perms, vec_tensordiag, identity_tensors
from . import VectorOps as vec_ops
from . import SetOps as set_ops
from .Misc import is_numeric, is_zero, is_numeric_array_like
from .Options import Options
__all__ = ['nca_op_deriv', 'tensordot_deriv', 'tensorprod_deriv', 'scalarprod_deriv', 'inverse_transformation', 'optimizing_transformation', 'matinv_deriv', 'matdet_deriv', 'matsqrt_deriv', 'mateigh_deriv', 'scalarinv_deriv', 'scalarpow_deriv', 'tensor_reexpand', 'tensorops_deriv', 'vec_norm_unit_deriv', 'vec_angle_deriv', 'vec_cross_deriv', 'vec_anglecos_deriv', 'vec_anglesin_deriv', 'vec_normal_deriv', 'vec_dihed_deriv', 'vec_plane_angle_deriv', 'shift_expansion', 'scale_expansion', 'add_expansions', 'subtract_expansions', 'concatenate_expansions', 'renormalize_transformation', 'orthogonalize_transformations']

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
    ...

def apply_nca_op(op, order, k, A_expansion, B_expansion, deriv_axis, a, b, contract, shared, identical, root_dim=2):
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
    ...

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
    ...

def nca_op_deriv(op, A_expansion, B_expansion, order, axes, contract, shared=None, identical=False):
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
    ...

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
    ...

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
    ...

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
    ...

def tensordot_deriv(A_expansion, B_expansion, order, axes=None, shared=None, identical=False):
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
    ...

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
    ...

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
    ...

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
    ...

def tensorprod_deriv(A_expansion, B_expansion, order, axes=None, identical=False):
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
    ...

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
    ...

def scalarprod_deriv(s_expansion, A_expansion, order, identical=False):
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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

def inverse_transformation(forward_expansion, order, reverse_expansion=None, allow_pseudoinverse=False, nonzero_cutoff=None):
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
    ...

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
    ...

def orthogonalize_transformations(transformation_pairs, order=None, orthonormalize=True, assume_prenormalized=True, first_order_projector=True, nonzero_cutoff=None, concatenate=True):
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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...
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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

def vec_parallel_cross_norm_deriv(axb_expansion, bxc_expansion, order, *, component_vectors=None, up_vector_expansion=None, unit_expansions=None):
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
    ...

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
    ...

def vec_anglesin_deriv(A_expansion, B_expansion, order, unitized=False, return_unit_vectors=True, planar=None, up_vector=None, component_vectors=None, unit_expansions=None, planar_threshold=None):
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
    ...

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
    ...

def vec_angle_deriv(A_expansion, B_expansion, order, up_vector=None, component_vectors=None, unit_expansions=None, unitized=False, planar=None, planar_threshold=None):
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
    ...

def vec_normal_deriv(A_expansion, B_expansion, order, up_vector=None, component_vectors=None, unit_expansions=None, unitized=False, planar=None, planar_threshold=None, normalize=True):
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
    ...

def vec_dihed_deriv(A_expansion, B_expansion, C_expansion, order, B_norms=None, planar=None, planar_threshold=None, up_vector=None):
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
    ...

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
    ...

def nca_partition_terms(partition):
    """
    Computes the number of permutations for the non-commutative operation
    corresponding to the given partition

    :param cls:
    :param partition:
    :return:
    """
    ...
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
    ...

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
    ...

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
    ...

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
    ...

def get_nca_symmetrizing_perms(partition, perm_idx=None, use_base_perms=True, filter_unique=False, contract=True, identical=False):
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
    ...

def nca_symmetrize(tensor, partition, shared=None, identical=False, contract=True, use_base_perms=True, filter_unique=False, check_symmetry=False, reweight=None):
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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...
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
        ...

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
        ...

def get_term_generator(k):
    """
    **LLM Docstring**

    Return a `caching_perm_generator` for `k` operands, cached for small `k`.

    :param k: the number of operands
    :type k: int
    :return: the (cached) term generator
    :rtype: caching_perm_generator
    """
    ...

def tensorops_deriv(*expansion_op_pairs, order, shared=None):
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
    ...
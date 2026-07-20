import collections
import numpy as np
from . import Misc as misc
from . import SetOps as sets
from . import VectorOps as vec_ops
__all__ = ['permutation_sign', 'levi_cevita_maps', 'levi_cevita_tensor', 'levi_cevita3', 'levi_cevita_dot', 'normalize_commutators', 'commutator_terms', 'commutator_evaluate', 'permutation_cycles', 'enumerate_permutations']

def permutation_sign(perm, check=True):
    """
    **LLM Docstring**

    Compute the sign (parity) of a permutation via a swap sort.

    Counts the transpositions needed to sort the permutation; an even count gives
    `+1`, odd gives `-1`. When `check` is set the input is first normalized to a
    proper `0..n-1` permutation with a double `argsort`.

    :param perm: the permutation
    :type perm: np.ndarray
    :param check: normalize the input to a rank permutation first
    :type check: bool
    :return: the permutation sign (`+1` or `-1`)
    :rtype: int
    """
    ...

def levi_cevita_maps(k):
    """
    **LLM Docstring**

    Return the nonzero index tuples and their signs for the rank-`k` Levi-Civita
    symbol.

    The nonzero entries sit at the permutations of `0..k-1`, each carrying the sign
    of that permutation.

    :param k: the tensor rank
    :type k: int
    :return: `(permutation_indices, signs)`
    :rtype: tuple[np.ndarray, np.ndarray]
    """
    ...

def levi_cevita_tensor(k, sparse=False):
    """
    **LLM Docstring**

    Build the rank-`k` Levi-Civita (permutation) tensor, dense or sparse.

    Uses `levi_cevita_maps` to place `±1` at the permutation positions; a
    `SparseArray` is returned when `sparse` is set, otherwise a dense integer array.

    :param k: the tensor rank
    :type k: int
    :param sparse: return a `SparseArray` instead of a dense array
    :type sparse: bool
    :return: the Levi-Civita tensor
    :rtype: np.ndarray | SparseArray
    """
    ...
levi_cevita3 = np.array([[[0, 0, 0], [0, 0, 1], [0, -1, 0]], [[0, 0, -1], [0, 0, 0], [1, 0, 0]], [[0, 1, 0], [-1, 0, 0], [0, 0, 0]]])

def levi_cevita_dot(k, a, /, axes, shared=None):
    """
    **LLM Docstring**

    Contract the rank-`k` Levi-Civita tensor with an array along the given axes,
    exploiting its sparsity.

    Delegates to `VectorOps.semisparse_tensordot` with the Levi-Civita nonzeros.

    :param k: the Levi-Civita rank
    :type k: int
    :param a: the array to contract against
    :type a: np.ndarray
    :param axes: `(levi_civita_axes, array_axes)` to contract
    :type axes: tuple
    :param shared: number of shared leading batch axes
    :type shared: int | None
    :return: the contracted result
    :rtype: np.ndarray
    """
    ...

def _flatten_comstr(cs):
    """
    **LLM Docstring**

    Recursively flatten a nested commutator string into a stream of its integer
    operator labels.

    :param cs: the (possibly nested) commutator specification
    :type cs: Iterable
    :return: a generator yielding the integer labels in order
    :rtype: Iterator[int]
    """
    ...

def normalize_commutators(commutator_string):
    """
    **LLM Docstring**

    Rewrite a nested commutator specification into a canonical sum of nested
    commutators over ordered operator labels.

    Recursively applies commutator identities (antisymmetry and the Jacobi-style
    regroupings) so that the result is expressed as a list of phases, a list of
    normalized nested-commutator forms, and the ordered list of operator symbols
    involved.

    :param commutator_string: the `[a, b]` commutator specification (nesting allowed)
    :type commutator_string: Sequence
    :return: `(phases, normal_forms, symbols)`
    :rtype: tuple[list, list, list]
    """
    ...

def _setup_com_terms(full_phases, storage, i0, idx, j0, j, term):
    """
    **LLM Docstring**

    Recursively expand a normalized commutator term into its signed sequence of
    operator-product permutations, writing them into a preallocated buffer.

    Each nesting level doubles the number of stored product orderings (the two
    sides of the commutator) and flips the phase of the newly added half; the
    `storage`/`full_phases` buffers are filled in place.

    :param full_phases: phase buffer (modified in place)
    :type full_phases: np.ndarray
    :param storage: operator-ordering buffer (modified in place)
    :type storage: np.ndarray
    :param i0: starting row offset into the buffers
    :type i0: int
    :param idx: number of orderings written so far for this term
    :type idx: int
    :param j0: starting column offset for this sub-term
    :type j0: int
    :param j: number of columns written so far for this sub-term
    :type j: int
    :param term: the normalized (nested) commutator term
    :type term: Sequence
    :return: `(n_orderings, n_columns)` produced
    :rtype: tuple[int, int]
    """
    ...

def commutator_terms(commutator_strings):
    """
    **LLM Docstring**

    Expand a commutator specification into all signed operator-product terms.

    Normalizes the commutator (`normalize_commutators`) and then materializes every
    product ordering with its phase via `_setup_com_terms`.

    :param commutator_strings: the commutator specification
    :type commutator_strings: Sequence
    :return: `(phases, operator_orderings)`
    :rtype: tuple[np.ndarray, np.ndarray]
    """
    ...

def commutator_evaluate(commutator, expansion_terms, normalized=False, direct=None, recursive=False):
    """
    **LLM Docstring**

    Evaluate a nested operator commutator given the matrices for the individual
    operators.

    Three strategies are available: a `recursive` direct evaluation of `a @ b - b @
    a`; a `direct` stack-based evaluation that memoizes sub-expressions; and an
    expanded evaluation that sums the signed operator products from
    `commutator_terms`. The strategy is auto-detected from the input shape when not
    forced.

    :param commutator: the commutator specification (or precomputed term data)
    :type commutator: Sequence
    :param expansion_terms: the operator matrices indexed by label
    :type expansion_terms: Sequence[np.ndarray]
    :param normalized: whether `commutator` is already expanded into terms
    :type normalized: bool
    :param direct: force (or disable) the stack-based direct evaluation
    :type direct: bool | None
    :param recursive: force the recursive evaluation
    :type recursive: bool
    :return: the evaluated commutator matrix
    :rtype: np.ndarray
    """
    ...

def permutation_cycles(perms, return_groups=False):
    """
    **LLM Docstring**

    Decompose permutations into their disjoint cycles.

    Assigns each position a cycle label (an integer group id); with
    `return_groups` set, the actual cycle index lists are returned instead. Cannot
    be vectorized past 2D, so batched inputs beyond a single stack are rejected when
    groups are requested.

    :param perms: the permutation(s)
    :type perms: np.ndarray
    :param return_groups: return explicit cycle index lists rather than labels
    :type return_groups: bool
    :return: per-position cycle labels, or the cycle groups
    :rtype: np.ndarray | list
    """
    ...

def permutation_from_cycles(cycle):
    """
    **LLM Docstring**

    Reconstruct a permutation array from its cycle decomposition.

    Each cycle maps every element to the next (a roll by one); the elements are
    gathered back into position order.

    :param cycle: the cycles (each a sequence of indices)
    :type cycle: Sequence[np.ndarray]
    :return: the reconstructed permutation
    :rtype: np.ndarray
    """
    ...

def compute_cycle_orders(perms):
    """
    **LLM Docstring**

    Compute the order (LCM-style product of cycle lengths) of each permutation.

    For a single permutation the cycle groups are enumerated directly; for a batch
    the cycle labels are counted per structure without materializing the groups.

    :param perms: the permutation(s)
    :type perms: np.ndarray
    :return: the order of each permutation
    :rtype: np.ndarray | int
    """
    ...

def enumerate_permutations(perm, cycle_orders=None):
    """
    **LLM Docstring**

    Enumerate the cyclic powers of a permutation (the subgroup it generates).

    Repeatedly composes the permutation with itself, producing one array per power
    up to its order. Batched inputs are handled per structure.

    :param perm: the permutation(s)
    :type perm: np.ndarray
    :param cycle_orders: precomputed order(s) (computed if omitted)
    :type cycle_orders: int | np.ndarray | None
    :return: the generated permutations (a stack, or a per-structure list)
    :rtype: np.ndarray | list
    """
    ...
"""Function-oriented exact delta/epsilon contraction kernels.

Semi-symbolic tensor and invariant-basis classes live in Zachary.Symbolic.
Terms are dictionaries mapping (delta_pairs,epsilon_triple) to rationals.
"""
from fractions import Fraction
from functools import lru_cache
from itertools import permutations
import operator
import numpy as np

__all__ = ['kronecker_delta_product_evaluate', 'isotropic_tensor_reduce',
           'isotropic_tensor_permute', 'isotropic_tensor_outer', 'isotropic_tensor_trace',
           'isotropic_tensor_inner', 'isotropic_tensor_evaluate', 'isotropic_tensor_array',
           'rational_matrix_pivots', 'rational_matrix_inverse']


def _sign(p):
    return (-1) ** sum(a > b for i, a in enumerate(p) for b in p[i+1:])


def _components(labels, pairs):
    """Connected-component map for a delta network."""
    parent = {i: i for i in labels}
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for i, j in pairs:
        parent[find(i)] = find(j)
    return {i: find(i) for i in parent}


def kronecker_delta_product_evaluate(pairs, fixed_indices=None, dimension=3):
    """Sum a delta network over every distinct unfixed index label.

    Labels may be any hashable objects. fixed_indices maps labels to Cartesian
    components. Each connected unfixed component contributes dimension;
    inconsistent fixed components contribute zero. No index enumeration.
    """
    dimension = operator.index(dimension)
    if dimension < 1:
        raise ValueError('dimension must be positive')
    pairs = tuple(tuple(p) for p in pairs)
    if any(len(p) != 2 for p in pairs):
        raise ValueError('each delta must have two index labels')
    fixed_indices = {} if fixed_indices is None else dict(fixed_indices)
    labels = set(i for p in pairs for i in p) | set(fixed_indices)
    graph = _components(labels, pairs)
    fixed = {}
    for label, value in fixed_indices.items():
        value = operator.index(value)
        if not 0 <= value < dimension:
            raise ValueError('fixed component is outside the dimension')
        root = graph[label]
        if root in fixed and fixed[root] != value:
            return 0
        fixed[root] = value
    return dimension ** (len({graph[i] for i in labels}) - len(fixed))


def _canonical(rank, pairs, epsilon):
    pairs = tuple(sorted(tuple(sorted(map(operator.index, pair))) for pair in pairs))
    epsilon = tuple(map(operator.index, epsilon))
    if len(epsilon) not in (0, 3) or any(len(p) != 2 for p in pairs):
        raise ValueError('terms contain delta pairs and at most one epsilon triple')
    slots = [i for p in pairs for i in p] + list(epsilon)
    if sorted(slots) != list(range(rank)):
        raise ValueError('every free slot must occur exactly once in each monomial')
    return (pairs, tuple(sorted(epsilon))), _sign(epsilon)


def _contract_term(rank, key, contractions):
    """Trace a monomial using graph components, with at most one epsilon."""
    pairs, epsilon = key
    removed = {i for p in contractions for i in p}
    remaining = [i for i in range(rank) if i not in removed]
    graph = _components(range(rank), pairs+contractions)
    roots = {graph[i] for i in range(rank)}
    eps_roots = [graph[i] for i in epsilon]
    if len(set(eps_roots)) != len(eps_roots):
        return None, 0
    open_slots = {r: [] for r in roots}
    for new, old in enumerate(remaining):
        open_slots[graph[old]].append(new)
    out_pairs, out_eps, coefficient = [], [], 1
    for root, slots in open_slots.items():
        if root in eps_roots:
            if len(slots) != 1:
                raise ValueError('malformed epsilon contraction')
        elif len(slots) == 0:
            coefficient *= 3
        elif len(slots) == 2:
            out_pairs.append(tuple(slots))
        else:
            raise ValueError('malformed delta contraction')
    out_eps = tuple(open_slots[r][0] for r in eps_roots)
    key, sign = _canonical(len(remaining), out_pairs, out_eps)
    return key, coefficient * sign


def isotropic_tensor_reduce(rank, terms):
    """Canonicalize and combine rational delta/epsilon monomials."""
    rank = operator.index(rank)
    if rank < 0:
        raise ValueError('rank must be nonnegative')
    reduced = {}
    for (pairs, epsilon), coefficient in terms.items():
        key, sign = _canonical(rank, pairs, epsilon)
        reduced[key] = reduced.get(key, Fraction(0)) + sign*Fraction(coefficient)
    return {k: c for k, c in reduced.items() if c}


def isotropic_tensor_permute(rank, tensor_terms, permutation):
    permutation = tuple(operator.index(i) for i in permutation)
    if sorted(permutation) != list(range(rank)):
        raise ValueError('permutation must include every tensor slot')
    inverse = {old: new for new, old in enumerate(permutation)}
    terms = {}
    for (pairs, eps), c in tensor_terms.items():
        key, sign = _canonical(rank,
            [(inverse[i], inverse[j]) for i, j in pairs], [inverse[i] for i in eps])
        terms[key] = terms.get(key, Fraction(0)) + c*sign
    return isotropic_tensor_reduce(rank, terms)


def isotropic_tensor_outer(left_rank, left_terms, right_rank, right_terms):
    terms = {}
    for (pa, ea), ca in left_terms.items():
        for (pb, eb), cb in right_terms.items():
            pb = tuple((i+left_rank, j+left_rank) for i, j in pb)
            eb = tuple(i+left_rank for i in eb)
            if ea and eb:
                expansions = [(pa+pb+tuple(zip(ea, p)), (), _sign(p)) for p in permutations(eb)]
            else:
                expansions = [(pa+pb, ea or eb, 1)]
            for pairs, eps, sign in expansions:
                key, phase = _canonical(left_rank+right_rank, pairs, eps)
                terms[key] = terms.get(key, Fraction(0)) + ca*cb*sign*phase
    return isotropic_tensor_reduce(left_rank+right_rank, terms)


def isotropic_tensor_trace(rank, tensor_terms, pairs):
    pairs = tuple(tuple(operator.index(i) for i in p) for p in pairs)
    used = [i for p in pairs for i in p]
    if (any(len(p) != 2 for p in pairs) or len(set(used)) != len(used)
            or any(i < 0 or i >= rank for i in used)):
        raise ValueError('traces must pair distinct valid slots')
    terms = {}
    for key, coefficient in tensor_terms.items():
        out, factor = _contract_term(rank, key, pairs)
        if factor:
            terms[out] = terms.get(out, Fraction(0)) + factor*coefficient
    return rank-len(used), isotropic_tensor_reduce(rank-len(used), terms)


def isotropic_tensor_inner(rank, left_terms, right_terms):
    """Exact bilinear full contraction of two rank-n invariant polynomials."""
    return sum((a*b*_monomial_inner(rank, ka, kb)
                for ka, a in left_terms.items() for kb, b in right_terms.items()), Fraction(0))


@lru_cache(8192)
def _monomial_inner(rank, a, b):
    terms = isotropic_tensor_outer(rank, {a: 1}, rank, {b: 1})
    _, scalar = isotropic_tensor_trace(2*rank, terms, tuple((i, i+rank) for i in range(rank)))
    return scalar.get(((), ()), Fraction(0))


def isotropic_tensor_evaluate(rank, tensor_terms, vectors):
    """Contract all slots with vectors of shape (...,rank,3), bilinearly."""
    vectors = np.asarray(vectors)
    if vectors.ndim < 2 or vectors.shape[-2:] != (rank, 3):
        raise ValueError('expected vectors of shape (...,rank,3)')
    vectors = vectors.astype(np.result_type(vectors.dtype, float), copy=False)
    result = np.zeros(vectors.shape[:-2], dtype=np.result_type(vectors.dtype, float))
    for (pairs, eps), coefficient in tensor_terms.items():
        value = float(coefficient)
        for i, j in pairs:
            value = value * np.sum(vectors[..., i, :]*vectors[..., j, :], axis=-1)
        if eps:
            i, j, k = eps
            value = value * np.sum(vectors[..., i, :]*np.cross(vectors[..., j, :], vectors[..., k, :]), axis=-1)
        result += value
    return result


def isotropic_tensor_array(rank, tensor_terms, dtype=float):
    """Explicit dense tensor, costing 3**rank storage; intended for low ranks."""
    result = np.zeros((3,)*rank, dtype=dtype)
    for component in np.ndindex(result.shape):
        value = Fraction(0)
        for (pairs, eps), c in tensor_terms.items():
            if any(component[i] != component[j] for i, j in pairs):
                continue
            if eps:
                e = tuple(component[i] for i in eps)
                if len(set(e)) != 3:
                    continue
                c *= _sign(e)
            value += c
        result[component] = value if dtype is object else float(value)
    return result


def rational_matrix_pivots(matrix):
    a = [list(map(Fraction, row)) for row in matrix]
    pivot_row, pivots = 0, []
    for col in range(len(a[0]) if a else 0):
        pivot = next((i for i in range(pivot_row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        scale = a[pivot_row][col]
        a[pivot_row] = [v/scale for v in a[pivot_row]]
        for i in range(pivot_row+1, len(a)):
            scale = a[i][col]
            if scale:
                a[i] = [v-scale*w for v, w in zip(a[i], a[pivot_row])]
        pivots.append(col)
        pivot_row += 1
        if pivot_row == len(a):
            break
    return pivots


def rational_matrix_inverse(matrix):
    n = len(matrix)
    a = [list(map(Fraction, row)) + [Fraction(i == j) for j in range(n)] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next((i for i in range(col, n) if a[i][col]), None)
        if pivot is None:
            raise ValueError('the proposed invariant basis is linearly dependent')
        a[col], a[pivot] = a[pivot], a[col]
        scale = a[col][col]
        a[col] = [v/scale for v in a[col]]
        for i in range(n):
            scale = a[i][col]
            if i != col and scale:
                a[i] = [v-scale*w for v, w in zip(a[i], a[col])]
    return tuple(tuple(row[n:]) for row in a)

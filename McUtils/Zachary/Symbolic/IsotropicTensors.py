"""Semi-symbolic invariant tensors and exact Bonvicini/Smith bases.

Bonvicini & Champagne (2023), doi:10.1021/acs.jctc.3c00878: FICT/RREF.
Andrews & Thirunamachandran (1977), doi:10.1063/1.434725: tableau basis.
The numerical/exact contraction kernels are in McUtils.Numputils.
"""
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations
from types import MappingProxyType
import operator
import numpy as np
from ... import Numputils as nput
from ...Numputils.IsotropicTensors import _sign

__all__ = ['IsotropicTensor', 'IsotropicTensorBasis', 'isotropic_tensor_basis',
           'rotational_averaging_tensor']


class IsotropicTensor:
    """Exact delta/epsilon tensor polynomial backed by Numputils kernels.

    Its shape/ndim protocol also lets existing TensorExpression terms evaluate
    on this representation without materializing dense Cartesian components.
    """
    def __init__(self, rank, terms=None):
        self.rank = operator.index(rank)
        self.terms = MappingProxyType(nput.isotropic_tensor_reduce(self.rank, terms or {}))

    @property
    def ndim(self):
        return self.rank

    @property
    def shape(self):
        return (3,)*self.rank

    @classmethod
    def monomial(cls, rank, pairs=(), epsilon=()):
        return cls(rank, {(tuple(map(tuple, pairs)), tuple(epsilon)): 1})

    def __add__(self, other):
        if not isinstance(other, type(self)) or self.rank != other.rank:
            return NotImplemented
        terms = dict(self.terms)
        for key, c in other.terms.items():
            terms[key] = terms.get(key, Fraction(0)) + c
        return type(self)(self.rank, terms)

    def __neg__(self):
        return self * -1

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, scalar):
        scalar = Fraction(scalar)
        return type(self)(self.rank, {key: c*scalar for key, c in self.terms.items()})

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        return self * (1/Fraction(scalar))

    def permute(self, permutation):
        return type(self)(self.rank, nput.isotropic_tensor_permute(self.rank, self.terms, permutation))

    def outer(self, other):
        return type(self)(self.rank+other.rank,
                          nput.isotropic_tensor_outer(self.rank, self.terms, other.rank, other.terms))

    def trace(self, pairs):
        rank, terms = nput.isotropic_tensor_trace(self.rank, self.terms, pairs)
        return type(self)(rank, terms)

    def inner(self, other):
        if self.rank != other.rank:
            raise ValueError('full contraction requires equal ranks')
        return nput.isotropic_tensor_inner(self.rank, self.terms, other.terms)

    def values(self, vectors):
        return nput.isotropic_tensor_evaluate(self.rank, self.terms, vectors)

    def as_array(self, dtype=float):
        return nput.isotropic_tensor_array(self.rank, self.terms, dtype=dtype)


def _pairings(slots):
    if not slots:
        yield ()
    else:
        for p in range(1, len(slots)):
            for rest in _pairings(slots[1:p]+slots[p+1:]):
                yield ((slots[0], slots[p]),) + rest


def _bonvicini_isomers(rank):
    for eps in combinations(range(rank), 3) if rank % 2 else [()]:
        for pairs in _pairings(tuple(i for i in range(rank) if i not in eps)):
            yield IsotropicTensor.monomial(rank, pairs, eps)


def _young_basis(rank):
    from ...Combinatorics import IntegerPartitioner, YoungTableauxGenerator
    if rank == 0:
        yield IsotropicTensor.monomial(0)
        return
    parts = IntegerPartitioner.partitions(rank, pad=False, max_len=3)
    generator = YoungTableauxGenerator(rank)
    for group in parts:
        for part in group:
            shape = tuple(int(i) for i in part if i)
            if not (all(i % 2 == 0 for i in shape) if rank % 2 == 0
                    else len(shape) == 3 and all(i % 2 == 1 for i in shape)):
                continue
            rows = generator.get_standard_tableaux(shape)
            for tableau in zip(*rows):
                columns = [tuple(int(row[c]) for row in tableau if c < len(row)) for c in range(shape[0])]
                eps = columns[0] if rank % 2 else ()
                terms = {((), eps): Fraction(1)}
                start = 1 if eps else 0
                for c in range(start, len(columns), 2):
                    left, right = columns[c:c+2]
                    expanded = {}
                    for (pairs, e), value in terms.items():
                        for p in permutations(right):
                            key = (pairs + tuple(zip(left, p)), e)
                            expanded[key] = expanded.get(key, Fraction(0)) + value*_sign(p)*_sign(right)
                    terms = expanded
                yield IsotropicTensor(rank, terms)


class IsotropicTensorBasis:
    """Exact independent invariant basis and its inverse contraction matrix.

    This is the scalar (j=0) projection infrastructure. Young operators can
    separately represent arbitrary permutation symmetries, but a full all-j
    irreducible Cartesian decomposition additionally needs trace removal and
    multiplicity labels and is not implied by this class.
    """
    def __init__(self, rank, method='bonvicini'):
        self.rank = operator.index(rank)
        if self.rank < 0 or method not in ('bonvicini', 'young'):
            raise ValueError('expected nonnegative rank and bonvicini or young method')
        self.method = method
        candidates = tuple(_bonvicini_isomers(rank) if method == 'bonvicini' else _young_basis(rank))
        self.candidate_count = len(candidates)
        gram = [[Fraction(0) for _ in candidates] for _ in candidates]
        for i, a in enumerate(candidates):
            for j in range(i+1):
                gram[i][j] = gram[j][i] = a.inner(candidates[j])
        self.pivots = tuple(nput.rational_matrix_pivots(gram) if method == 'bonvicini' else range(len(candidates)))
        self.tensors = tuple(candidates[i] for i in self.pivots)
        self.gram = tuple(tuple(gram[i][j] for j in self.pivots) for i in self.pivots)
        self.inverse = nput.rational_matrix_inverse(self.gram)
        self._numeric_inverse = np.array(self.inverse, dtype=float).reshape((len(self.tensors),)*2)
        self._numeric_inverse.flags.writeable = False

    def __len__(self):
        return len(self.tensors)

    def values(self, vectors):
        vectors = np.asarray(vectors)
        if vectors.ndim < 2 or vectors.shape[-2:] != (self.rank, 3):
            raise ValueError('expected vectors of shape (...,rank,3)')
        if not self.tensors:
            return np.empty(vectors.shape[:-2]+(0,), dtype=np.result_type(vectors.dtype, float))
        return np.stack([t.values(vectors) for t in self.tensors], axis=-1)

    def average_values(self, left, right):
        return np.einsum('...i,ij,...j->...', left, self._numeric_inverse, right)

    def average(self, polarizations, moments):
        return self.average_values(self.values(polarizations), self.values(moments))

    def projector(self):
        """Semi-symbolic rank-2n Haar projector, lab slots followed by mol slots."""
        terms = {}
        for i, a in enumerate(self.tensors):
            for j, b in enumerate(self.tensors):
                if self.inverse[i][j]:
                    for key, c in a.outer(b).terms.items():
                        terms[key] = terms.get(key, Fraction(0)) + c*self.inverse[i][j]
        return IsotropicTensor(2*self.rank, terms)

    def project(self, tensor):
        """Numerical projection of an arbitrary dense rank-n Cartesian tensor."""
        tensor = np.asarray(tensor)
        if tensor.shape != (3,)*self.rank:
            raise ValueError('dense tensor must have one dimension of length 3 per slot')
        basis = [t.as_array() for t in self.tensors]
        contractions = np.array([np.sum(tensor*b) for b in basis])
        coefficients = self._numeric_inverse @ contractions
        return sum((c*b for c, b in zip(coefficients, basis)), np.zeros_like(tensor, dtype=np.result_type(tensor.dtype, float)))


@lru_cache(16)
def isotropic_tensor_basis(rank, method='bonvicini'):
    return IsotropicTensorBasis(rank, method)


def rotational_averaging_tensor(rank, method='young'):
    return isotropic_tensor_basis(rank, method).projector()

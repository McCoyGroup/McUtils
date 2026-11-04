"""Exact permutation algebra acting on arrays or semi-symbolic tensors.

Young symmetrizers describe permutation symmetry. They are not, by themselves,
traceless SO(3) irreducible projectors. Full column antisymmetrizers contain
every signed permutation; a nested commutator is a different operator.
"""
from fractions import Fraction
from itertools import permutations
from math import factorial, prod
from types import MappingProxyType
import operator
import numpy as np

__all__ = ['TensorPermutationOperator']


def _sign(permutation):
    return (-1) ** sum(a > b for i, a in enumerate(permutation) for b in permutation[i+1:])


class TensorPermutationOperator:
    """A rational linear combination of NumPy-transpose permutations.

    A @ B means apply B, then A. The same expression can be evaluated on
    dense tensors or on any object exposing permute(permutation), +, and *.
    """
    def __init__(self, rank, terms=None):
        self.rank = operator.index(rank)
        if self.rank < 0:
            raise ValueError('rank must be nonnegative')
        if terms is None:
            terms = {tuple(range(self.rank)): 1}
        reduced = {}
        for p, coefficient in terms.items():
            p = tuple(operator.index(i) for i in p)
            if sorted(p) != list(range(self.rank)):
                raise ValueError('each term must be a permutation of all tensor slots')
            reduced[p] = reduced.get(p, Fraction(0)) + Fraction(coefficient)
        self.terms = MappingProxyType({p: c for p, c in reduced.items() if c})

    def __add__(self, other):
        if not isinstance(other, type(self)) or self.rank != other.rank:
            return NotImplemented
        terms = dict(self.terms)
        for p, c in other.terms.items():
            terms[p] = terms.get(p, Fraction(0)) + c
        return type(self)(self.rank, terms)

    def __neg__(self):
        return self * -1

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, scalar):
        scalar = Fraction(scalar)
        return type(self)(self.rank, {p: scalar*c for p, c in self.terms.items()})

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        return self * (1 / Fraction(scalar))

    def __matmul__(self, other):
        if not isinstance(other, type(self)) or self.rank != other.rank:
            return NotImplemented
        terms = {}
        for p, a in self.terms.items():
            for q, b in other.terms.items():
                composition = tuple(q[i] for i in p)
                terms[composition] = terms.get(composition, Fraction(0)) + a*b
        return type(self)(self.rank, terms)

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.rank == other.rank and self.terms == other.terms

    @classmethod
    def symmetrizer(cls, rank, slots=None, antisymmetric=False, normalized=True):
        rank = operator.index(rank)
        slots = tuple(range(rank)) if slots is None else tuple(operator.index(i) for i in slots)
        if len(set(slots)) != len(slots) or any(i < 0 or i >= rank for i in slots):
            raise ValueError('slots must be distinct valid tensor indices')
        terms = {}
        for perm in permutations(range(len(slots))):
            full = list(range(rank))
            for i, p in enumerate(perm):
                full[slots[i]] = slots[p]
            terms[tuple(full)] = Fraction(_sign(perm) if antisymmetric else 1,
                                          factorial(len(slots)) if normalized else 1)
        return cls(rank, terms)

    @classmethod
    def from_tableau(cls, tableau, normalized=True):
        """Row symmetrizer @ column antisymmetrizer, divided by hook product.

        The normalized operator is idempotent but generally not orthogonal.
        Entries must be the zero-based slots, each occurring exactly once.
        """
        from ...Combinatorics import YoungTableauxGenerator
        rows = [tuple(operator.index(i) for i in row) for row in tableau]
        shape = tuple(map(len, rows))
        if not rows or min(shape) == 0 or sorted(shape, reverse=True) != list(shape):
            raise ValueError('tableau must have nonempty, nonincreasing row lengths')
        rank = sum(shape)
        if sorted(i for row in rows for i in row) != list(range(rank)):
            raise ValueError('tableau entries must contain every zero-based slot once')
        row_op, col_op = cls(rank), cls(rank)
        for row in rows:
            row_op = row_op @ cls.symmetrizer(rank, row, normalized=False)
        for c in range(shape[0]):
            column = [row[c] for row in rows if c < len(row)]
            col_op = col_op @ cls.symmetrizer(rank, column, antisymmetric=True, normalized=False)
        result = row_op @ col_op
        if normalized:
            result = result / prod(int(h) for h in YoungTableauxGenerator.hook_numbers(shape))
        return result

    @classmethod
    def from_commutator(cls, commutator, operators):
        """Use McUtils' commutator evaluator in this exact operator algebra."""
        from ...Numputils.PermutationOps import commutator_evaluate
        operators = tuple(operators)
        if not operators or any(not isinstance(op, cls) or op.rank != operators[0].rank for op in operators):
            raise ValueError('commutator leaves must be operators of one common rank')
        return commutator_evaluate(commutator, operators, recursive=True)

    def apply(self, tensor, axes=None):
        from .TensorExpressions import TensorExpression
        if isinstance(tensor, TensorExpression):
            return TensorExpression(self.apply(tensor.expr, axes=axes), **tensor.vars)
        if isinstance(tensor, TensorExpression.Term):
            if axes is not None:
                raise ValueError('explicit array axes are only supported for numerical arrays')
            if tensor.ndim != self.rank:
                raise ValueError('operator and tensor ranks differ')
            terms = [TensorExpression.ScalingTerm(tensor.permute(p), c) for p, c in self.terms.items()]
            # Use the native n-ary sum, avoiding a deeply nested binary graph.
            return TensorExpression.SumTerm(*terms) if terms else TensorExpression.ScalingTerm(tensor, 0)
        if hasattr(tensor, 'permute') and axes is None:
            if tensor.ndim != self.rank:
                raise ValueError('operator and tensor ranks differ')
            result = tensor * 0
            for p, c in self.terms.items():
                result = result + tensor.permute(p) * c
            return result
        tensor = np.asarray(tensor)
        if axes is None:
            axes = tuple(range(tensor.ndim-self.rank, tensor.ndim))
        axes = tuple(operator.index(i) for i in axes)
        if any(i < -tensor.ndim or i >= tensor.ndim for i in axes):
            raise ValueError('tensor axis is out of bounds')
        axes = tuple(i % tensor.ndim for i in axes)
        if len(axes) != self.rank or len(set(axes)) != self.rank or tensor.ndim < self.rank:
            raise ValueError('one distinct array axis is required per tensor slot')
        if len({tensor.shape[i] for i in axes}) > 1:
            raise ValueError('permuted tensor axes must have equal dimensions')
        result = np.zeros_like(tensor, dtype=np.result_type(tensor.dtype, float))
        for p, c in self.terms.items():
            transpose = list(range(tensor.ndim))
            for i, k in enumerate(axes):
                transpose[k] = axes[p[i]]
            result += float(c) * tensor.transpose(transpose)
        return result

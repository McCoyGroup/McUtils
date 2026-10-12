"""Check direct tensor derivatives against independent Taylor-polynomial algebra."""
import itertools
import math
import unittest

import numpy as np
from McUtils import Numputils as nput


def indices(ncoords, order):
    return [a for a in itertools.product(range(order+1), repeat=ncoords) if sum(a) <= order]


def expansion(poly, order, ncoords=2):
    base = next(iter(poly.values()))
    result = []
    for o in range(order+1):
        t = np.zeros((ncoords,)*o + base.shape,
                     dtype=np.result_type(*[np.asarray(v).dtype for v in poly.values()]))
        for axes in itertools.product(range(ncoords), repeat=o):
            alpha = tuple(axes.count(i) for i in range(ncoords))
            t[axes] = poly.get(alpha, 0) * math.prod(math.factorial(a) for a in alpha)
        result.append(t)
    return result


def multiply(a, b, operation, order=4):
    result = {}
    for i, x in a.items():
        for j, y in b.items():
            alpha = tuple(u+v for u, v in zip(i, j))
            if sum(alpha) <= order:
                result[alpha] = result.get(alpha, 0) + operation(x, y)
    return result


def random_poly(rng, shape, order=4, ncoords=2):
    return {a: rng.normal(size=shape)*.1 for a in indices(ncoords, order)}


def power(poly, exponent, order=4):
    zero = (0,)*len(next(iter(poly)))
    base = poly[zero]
    delta = {a:t/base for a,t in poly.items() if a != zero}
    result = {zero:base**exponent}
    term = {zero:np.ones_like(base)}
    coefficient = 1
    for k in range(1, order+1):
        term = multiply(term, delta, lambda x,y:x*y, order)
        coefficient *= (exponent-k+1)/k
        for a,t in term.items():
            result[a] = result.get(a, 0) + base**exponent*coefficient*t
    return result


def batched(exp, batch_shape):
    # Put batch axes before derivative axes, with different coefficients per batch.
    offsets = np.arange(math.prod(batch_shape)).reshape(batch_shape) + 1
    return [offsets.reshape(batch_shape+(1,)*t.ndim)*t for t in exp]


class TensorDerivativeRegressionTests(unittest.TestCase):
    def setUp(self):
        self.rng = np.random.default_rng(192)

    def assertExpansion(self, actual, expected):
        self.assertEqual(len(actual), len(expected))
        for a, b in zip(actual, expected):
            np.testing.assert_allclose(a, b, atol=2e-12, rtol=2e-12)

    def test_contraction_and_outer_product(self):
        a = random_poly(self.rng, (3, 4))
        b = random_poly(self.rng, (4, 5))
        ae, be = expansion(a, 4), expansion(b, 4)
        expected = expansion(multiply(a, b, lambda x, y: x@y), 4)
        self.assertExpansion(nput.tensordot_deriv(ae, be, 4), expected)
        self.assertExpansion(nput.tensordot_deriv(ae, be, [4, 0, 2]), [expected[o] for o in (4, 0, 2)])
        expected = expansion(multiply(a, b, lambda x, y: np.tensordot(x, y, axes=0)), 4)
        self.assertExpansion(nput.tensorprod_deriv(ae, be, 4, axes='all'), expected)
        for shape in ((2,), (2, 3)):
            s = len(shape)
            ab, bb = batched(ae, shape), batched(be, shape)
            factors = (np.arange(math.prod(shape)).reshape(shape)+1)**2
            ref = [factors.reshape(shape+(1,)*t.ndim)*t for t in expected]
            self.assertExpansion(nput.tensorprod_deriv(ab, bb, 4,
                axes=[list(range(s, s+2))]*2), ref)

    def test_noncommuting_matrix_inverse(self):
        a = random_poly(self.rng, (3, 3))
        a[(0, 0)] += 2*np.eye(3)
        b = {(0, 0): np.linalg.inv(a[(0, 0)])}
        for alpha in sorted(indices(2, 4), key=sum)[1:]:
            total = sum(value@b[tuple(u-v for u, v in zip(alpha, beta))]
                for beta, value in a.items()
                if sum(beta) > 0 and all(v <= u for u, v in zip(alpha, beta)))
            b[alpha] = -b[(0, 0)]@total
        ae, expected = expansion(a, 4), expansion(b, 4)
        self.assertExpansion(nput.matinv_deriv(ae, 4), expected)
        self.assertExpansion(nput.matinv_deriv(ae, 4, base_expansion=expected[:2]), expected)
        for shape in ((2,), (2, 3)):
            ab = batched(ae, shape)
            factors = 1/(np.arange(math.prod(shape)).reshape(shape)+1)
            ref = [factors.reshape(shape+(1,)*t.ndim)*t for t in expected]
            self.assertExpansion(nput.matinv_deriv(ab, 4), ref)

    def test_chained_operations_with_different_core_ranks(self):
        a = random_poly(self.rng, (3, 4))
        b = random_poly(self.rng, (4,))
        c = random_poly(self.rng, (5,))
        expected = expansion(multiply(multiply(a, b, lambda x, y:x@y), c,
            lambda x, y:np.outer(x, y)), 4)
        ae, be, ce = [expansion(p, 4) for p in (a, b, c)]
        self.assertExpansion(nput.tensorops_deriv(ae, [-1, 0], be, 'x', ce, order=4), expected)
        for shape in ((2,), (2, 3)):
            s = len(shape)
            ab, bb, cb = [batched(e, shape) for e in (ae, be, ce)]
            factors = (np.arange(math.prod(shape)).reshape(shape)+1)**3
            ref = [factors.reshape(shape+(1,)*t.ndim)*t for t in expected]
            self.assertExpansion(nput.tensorops_deriv(ab, [-1, s], bb, 'x', cb, order=4, shared=s), ref)

    def test_nonlinear_reexpansion(self):
        inner = random_poly(self.rng, (3,))
        inner[(0, 0)] = np.zeros(3)
        outer = random_poly(self.rng, (2,), ncoords=3)
        # Substitute each component of the inner polynomial into the outer one.
        composed = {}
        for powers, value in outer.items():
            term = {(0, 0): np.ones(())}
            for k, power in enumerate(powers):
                component = {a:t[k] for a, t in inner.items()}
                for _ in range(power):
                    term = multiply(term, component, lambda x,y:x*y)
            for alpha, coeff in term.items():
                composed[alpha] = composed.get(alpha, 0) + coeff*value
        expected = expansion(composed, 4)
        ie = expansion(inner, 4)[1:]
        oe = expansion(outer, 4, ncoords=3)[1:]
        self.assertExpansion(nput.tensor_reexpand(ie, oe, 4), expected[1:])
        for shape in ((2,), (2, 3)):
            ib, ob = [batched(e, shape) for e in (ie, oe)]
            # Each inner and outer coefficient is independently scaled per batch.
            ref = []
            for batch in itertools.product(*[range(n) for n in shape]):
                ref.append(nput.tensor_reexpand([e[batch] for e in ib], [e[batch] for e in ob], 4))
            reference = [np.stack([r[o] for r in ref]).reshape(shape + expected[o+1].shape) for o in range(4)]
            self.assertExpansion(nput.tensor_reexpand(ib, ob, 4), reference)

    def test_vector_norm_and_normalization(self):
        a = random_poly(self.rng, (3,))
        a[(0, 0)] += np.array([1., 2., -1.])
        squared = multiply(a, a, lambda x,y:np.dot(x,y))
        norm = power(squared, .5)
        inverse_norm = power(squared, -.5)
        unit = multiply(a, inverse_norm, lambda x,y:x*y)
        actual_norm, actual_unit = nput.vec_norm_unit_deriv(expansion(a, 4), 4)
        self.assertExpansion(actual_norm, expansion(norm, 4))
        self.assertExpansion(actual_unit, expansion(unit, 4))

    def test_scalar_powers_and_reciprocal(self):
        a = random_poly(self.rng, ())
        a[(0,0)] += 2.
        ae = expansion(a, 4)
        for exponent in (-1., -.5, .5, 2.):
            self.assertExpansion(nput.scalarpow_deriv(ae, exponent, 4), expansion(power(a, exponent), 4))
        self.assertExpansion(nput.scalarinv_deriv(ae, 4), expansion(power(a, -1.), 4))

    def test_constant_and_linear_expansions(self):
        matrix = np.array([[2., .3], [-.1, 1.]])
        inverse = nput.matinv_deriv([matrix, 0, 0, 0, 0], 4)
        self.assertExpansion(inverse, [np.linalg.inv(matrix), 0, 0, 0, 0])
        # Sparse expansions must give the same result as explicitly padded ones.
        a = [np.eye(2), np.ones((2, 2, 2))*.01]
        self.assertExpansion(nput.matinv_deriv(a, 4), nput.matinv_deriv(a+[0]*3, 4))


if __name__ == '__main__':
    unittest.main()

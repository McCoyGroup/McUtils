"""Independent checks of Wigner, FICT and Smith/Young averages."""

import os as _test_os
import unittest as _test_unittest
_RUN_EXTRAS = _test_os.environ.get("MCUTILS_TEST_EXTRAS") == "1"

import itertools
from fractions import Fraction
import unittest
import numpy as np
import McUtils.Numputils as nput
import McUtils.Zachary as zach
from McUtils.Zachary.Symbolic import TensorPermutationOperator


def quadrature(lab, mol):
    """Exact-degree SO(3) product rule: Fourier x Gauss--Legendre x Fourier."""
    rank = lab.shape[-2]
    count = rank+1
    nodes, weights = np.polynomial.legendre.leggauss((rank+2)//2)
    rz = [nput.rotation_matrix(np.array([0., 0., 1.]), float(angle))
          for angle in np.arange(count)*2*np.pi/count]
    result = 0j
    for node, weight in zip(nodes, weights):
        ry = nput.rotation_matrix(np.array([0., 1., 0.]), float(np.arccos(node)))
        for a in rz:
            for b in rz:
                factors = np.einsum('ki,ij,kj->k', lab, a@ry@b, mol)
                result += weight*np.prod(factors)/(2*count**2)
    return result


class RotationalAveragingTests(unittest.TestCase):
    methods = ('wigner', 'bonvicini', 'young')

    def test_independent_quadrature_real_and_complex(self):
        rng = np.random.default_rng(2122)
        for rank in (2, 3, 4, 5, 6, 7, 8, 9, 12, 20):
            lab = nput.vec_normalize(rng.normal(size=(rank, 3)))
            mol = nput.vec_normalize(rng.normal(size=(rank, 3)))
            expected = quadrature(lab, mol)
            for method in self.methods if rank <= 8 else ('wigner',):
                with self.subTest(rank=rank, method=method):
                    np.testing.assert_allclose(zach.rotational_average(lab, mol, method), expected, atol=3e-14, rtol=1e-11)
        lab = rng.normal(size=(6, 3)) + 1j*rng.normal(size=(6, 3))
        mol = rng.normal(size=(6, 3)) + 1j*rng.normal(size=(6, 3))
        for method in self.methods:
            np.testing.assert_allclose(zach.rotational_average(lab, mol, method), quadrature(lab, mol), atol=3e-12)

    def test_parallel_arbitrary_order_and_empty_product(self):
        for rank in (0, 1, 2, 3, 4, 6, 12, 20, 40, 60, 61):
            vectors = np.tile([0., 0., 1.], (rank, 1))
            expected = 0 if rank % 2 else 1/(rank+1)
            np.testing.assert_allclose(zach.rotational_average(vectors, vectors), expected, atol=3e-14)
        empty = np.empty((2, 0, 3))
        for method in self.methods:
            np.testing.assert_equal(zach.rotational_average(empty, empty, method), np.ones(2))

    def test_so3_odd_rank_orientation_and_scaling(self):
        eye = np.eye(3)
        for method in self.methods:
            self.assertAlmostEqual(zach.rotational_average(eye, eye, method), 1/6)
            self.assertAlmostEqual(zach.rotational_average(eye, eye[[1, 0, 2]], method), -1/6)
            self.assertAlmostEqual(zach.rotational_average(2*eye, 3*eye, method), 36)
            np.testing.assert_equal(zach.rotational_average(np.zeros_like(eye), eye, method), 0)

    def test_batch_conjugation_and_rotation_invariance(self):
        rng = np.random.default_rng(931)
        lab = rng.normal(size=(2, 1, 6, 3)) + 1j*rng.normal(size=(2, 1, 6, 3))
        mol = rng.normal(size=(3, 6, 3)) + 1j*rng.normal(size=(3, 6, 3))
        mask = [True, False, True, False, False, True]
        expected = np.array([[quadrature(np.where(np.array(mask)[:, None], lab[i, 0].conj(), lab[i, 0]), mol[j])
                              for j in range(3)] for i in range(2)])
        rotation = nput.rotation_matrix(np.array([0., 1., 0.]), .271)
        for method in self.methods:
            actual = zach.rotational_average(lab, mol, method, conjugate_polarizations=mask)
            np.testing.assert_allclose(actual, expected, atol=1e-12)
            np.testing.assert_allclose(zach.rotational_average(lab@rotation, mol, method, conjugate_polarizations=mask), expected, atol=1e-12)
            np.testing.assert_allclose(zach.rotational_average(lab, mol, method, conjugate_moments=True),
                                       zach.rotational_average(lab, mol.conj(), method), atol=1e-12)
        # Public Fourier expansions may have differently shaped block batches.
        state = zach.WignerDExpansion({0: np.ones((3, 1, 1)), 2: np.zeros((2, 1, 5, 5))})
        result = state.multiply_vector(np.ones((3, 3)))
        self.assertEqual(result.coefficients[1].shape, (2, 3, 3, 3))

    def test_exact_basis_counts_and_contraction_matrices(self):
        expected = [1, 0, 1, 1, 3, 6, 15, 36, 91]
        for rank, count in enumerate(expected):
            for method in ('bonvicini', 'young'):
                basis = zach.isotropic_tensor_basis(rank, method)
                self.assertEqual(len(basis), count)
                if rank <= 6:
                    for i in range(count):
                        for j in range(count):
                            self.assertEqual(sum(basis.gram[i][k]*basis.inverse[k][j] for k in range(count)), int(i == j))
        self.assertEqual(zach.isotropic_tensor_basis(8).candidate_count, 105)
        self.assertEqual(zach.isotropic_tensor_basis(7).candidate_count, 105)

    def test_symbolic_delta_epsilon_and_projector(self):
        delta = zach.IsotropicTensor.monomial(2, [(0, 1)])
        epsilon = zach.IsotropicTensor.monomial(3, epsilon=(0, 1, 2))
        self.assertEqual(delta.inner(delta), 3)
        self.assertEqual(epsilon.inner(epsilon), 6)
        self.assertEqual(epsilon.permute((1, 0, 2)).inner(epsilon), -6)
        self.assertFalse(epsilon.trace([(0, 1)]).terms)
        np.testing.assert_allclose(epsilon.outer(epsilon).as_array(), np.multiply.outer(epsilon.as_array(), epsilon.as_array()))
        network = nput.kronecker_delta_product_evaluate
        self.assertEqual(network([('a', 'b'), ('b', 'c'), ('c', 'a')]), 3)
        self.assertEqual(network([('a', 'b')], {'a': 0, 'b': 1}), 0)
        self.assertEqual(network([('a', 'b'), ('c', 'd')], dimension=4), 16)
        rng = np.random.default_rng(122)
        for rank in (0, 2, 3, 4, 5):
            basis = zach.isotropic_tensor_basis(rank, 'young')
            projector = basis.projector()
            dense = projector.as_array()
            matrix = dense.reshape((3**rank,)*2)
            np.testing.assert_allclose(matrix@matrix, matrix, atol=2e-15)
            np.testing.assert_allclose(matrix.T, matrix, atol=2e-15)
            tensor = rng.normal(size=(3,)*rank)
            np.testing.assert_allclose(basis.project(tensor).ravel(), matrix@tensor.ravel(), atol=1e-14)

    def test_young_permutations_commutators_and_lazy_traces(self):
        P = TensorPermutationOperator
        rng = np.random.default_rng(786)
        array = rng.normal(size=(3,)*4)
        young = P.from_tableau([[0, 1], [2, 3]])
        self.assertEqual(young@young, young)
        a, b = P(4, {(1, 0, 2, 3): 1}), P(4, {(0, 2, 1, 3): 1})
        comm = P.from_commutator([[0, 1], 0], [a, b])
        np.testing.assert_allclose(comm.apply(array), (a@(b@a) - b@(a@a) - a@(a@b) + a@(b@a)).apply(array))
        np.testing.assert_allclose((a@b).apply(array), a.apply(b.apply(array)))
        symbol = zach.TensorExpression.symbol('T', 4)
        expr = young.apply(symbol).trace([(0, 2)])
        np.testing.assert_allclose(zach.TensorExpression(expr).eval({'T': array}), np.trace(young.apply(array), axis1=0, axis2=2))
        tensor = zach.IsotropicTensor.monomial(4, [(0, 1), (2, 3)])
        exact = zach.TensorExpression(expr).eval({'T': tensor})
        np.testing.assert_allclose(exact.as_array(), zach.TensorExpression(expr).eval({'T': tensor.as_array()}))
        self.assertTrue(all(isinstance(c, Fraction) for c in exact.terms.values()))
        product = symbol.contract(symbol, [(0, 1), (3, 2)])
        np.testing.assert_allclose(zach.TensorExpression(product).eval({'T': array}), np.tensordot(array, array, axes=([0, 3], [1, 2])))
        anti = P.symmetrizer(3, antisymmetric=True)
        self.assertEqual(len(anti.terms), 6)
        self.assertEqual(anti@anti, anti)
        np.testing.assert_allclose(anti.apply(rng.normal(size=(2,)*3)), 0, atol=1e-15)

    def test_validation(self):
        z = np.tile([0., 0., 1.], (6, 1))
        for method in self.methods:
            with self.assertRaises(ValueError):
                zach.rotational_average(z, z[:4], method)
            with self.assertRaises(ValueError):
                zach.rotational_average(z, z*np.nan, method)
            with self.assertRaises(ValueError):
                zach.rotational_average(z, z, method, conjugate_polarizations=[True])
        with self.assertRaises(ValueError):
            zach.rotational_average(z, z, 'unknown')
        with self.assertRaises(ValueError):
            zach.OrientationalAverager(np.ones(3))
        eye = np.eye(3, dtype=np.uint8)
        for method in self.methods:
            self.assertAlmostEqual(zach.rotational_average(eye, eye[[1, 0, 2]], method), -1/6)
        with self.assertRaises(ValueError):
            TensorPermutationOperator(2).apply(np.ones((3, 3)), axes=(0, 7))

    def test_hrs_irreducible_normalization_counterexamples(self):
        # Independent known STF and J=2 cases; do not encode the inconsistent
        # prefactors in Ziadi et al. (2026), printed Eqs. (5) and (6).
        pure3 = np.zeros((3,)*3)
        pure3[2, 2, 2] = 2
        for transverse in (0, 1):
            for index in set(itertools.permutations((2, transverse, transverse))):
                pure3[index] = -1
        q = np.diag([1., -1., 0.])
        eps = nput.levi_cevita3
        pure2 = np.einsum('ija,ak->ijk', eps, q) + np.einsum('ika,aj->ijk', eps, q)
        def intensity(beta, channel, method):
            lab = np.eye(3)[list(channel)*2]
            entries = [(index, beta[index]) for index in np.ndindex(beta.shape) if beta[index]]
            average = zach.OrientationalAverager(lab, method)
            return sum(a*b*average(np.eye(3)[list(i+j)]) for i, a in entries for j, b in entries)
        for method in self.methods:
            self.assertAlmostEqual(intensity(pure3, (2, 2, 2), method), 4/7)
            self.assertAlmostEqual(intensity(pure3, (2, 0, 0), method), 8/21)
            self.assertAlmostEqual(intensity(pure2, (2, 0, 0), method), 4/5)

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_clebsch_gordan_spin1_coefficients_against_symbolic_oracle(self):
        try:
            from sympy.physics.wigner import clebsch_gordan
        except ImportError:
            self.skipTest('optional SymPy coefficient oracle')
        from McUtils.Numputils.RotationalAveraging import _U
        from McUtils.Numputils import clebsch_gordan_spin1_couplings
        angle = .371
        rotation = nput.rotation_matrix(np.array([0., 0., 1.]), angle)
        np.testing.assert_allclose(_U@rotation@_U.conj().T,
                                   np.diag(np.exp(1j*angle*np.arange(-1, 2))), atol=1e-15)
        for j in range(21):
            for ell in range(abs(j-1), j+2):
                for q in (-1, 0, 1):
                    src, _, values = clebsch_gordan_spin1_couplings(j, ell, q)
                    expected = [float(clebsch_gordan(j, 1, ell, int(m), q, int(m)+q)) for m in src-j]
                    np.testing.assert_allclose(values, expected, atol=5e-16)

    def test_layering_and_function_kernels(self):
        import ast
        import importlib
        from pathlib import Path
        import McUtils.Combinatorics as comb
        from McUtils.Zachary.Symbolic import TensorExpression
        self.assertIs(TensorExpression, zach.TensorExpression)
        for name in ('TensorExpression', 'OrientationalAverager', 'WignerDExpansion', 'IsotropicTensor', 'IsotropicTensorBasis'):
            self.assertFalse(hasattr(nput, name), name)
        self.assertFalse(hasattr(comb, 'TensorPermutationOperator'))
        for module_name in ('AngularMomentum', 'RotationalAveraging', 'IsotropicTensors'):
            module = importlib.import_module('McUtils.Numputils.'+module_name)
            tree = ast.parse(Path(module.__file__).read_text())
            self.assertFalse(any(isinstance(node, ast.ClassDef) for node in ast.walk(tree)))
        rng = np.random.default_rng(410)
        lab, mol = rng.normal(size=(7, 3)), rng.normal(size=(7, 3))
        np.testing.assert_allclose(nput.rotational_average(lab, mol), zach.rotational_average(lab, mol), atol=1e-14)
        terms = {(((0, 1),), ()): Fraction(1)}
        self.assertEqual(nput.isotropic_tensor_inner(2, terms, terms), 3)

    def test_native_tensor_expression_terms_and_rebinding(self):
        T = zach.TensorExpression
        rng = np.random.default_rng(522)
        a, b = rng.normal(size=(3,)*4), rng.normal(size=(3,)*4)
        symbol = T.symbol('A', 4)
        young = TensorPermutationOperator.from_tableau([[0, 1], [2, 3]])
        term = young.apply(symbol)
        self.assertIsInstance(symbol, T.Term)
        self.assertIsInstance(term, T.SumTerm)
        expression = T(term, A=a)
        np.testing.assert_allclose(expression.eval(), young.apply(a), atol=1e-14)
        np.testing.assert_allclose(expression.eval({'A': b}), young.apply(b), atol=1e-14)
        constant_expr = T(young.apply(T.ConstantArray(a)))
        np.testing.assert_allclose(constant_expr.eval(), young.apply(a), atol=1e-14)
        wrapped = young.apply(T(symbol, A=a))
        self.assertIsInstance(wrapped, T)
        np.testing.assert_allclose(wrapped.eval(), young.apply(a), atol=1e-14)
        cache = T.Term._array_cache
        with self.assertRaises(ValueError):
            expression.eval({'A': np.ones((3, 3))})
        self.assertIs(T.Term._array_cache, cache)
        np.testing.assert_allclose(expression.eval({'A': b}), young.apply(b), atol=1e-14)

    def test_native_array_stacks_and_permuted_derivatives(self):
        T = zach.TensorExpression
        rng = np.random.default_rng(414)
        a = rng.normal(size=(2, 4, 3, 3, 3, 3))
        young = TensorPermutationOperator.from_tableau([[0, 1], [2, 3]])
        term = young.apply(T.symbol('A', 4)).trace([(0, 2)])
        value = T(term).eval({'A': T.ArrayStack((2, 4), a)})
        expected = np.trace(young.apply(a), axis1=2, axis2=4)
        np.testing.assert_allclose(value, expected, atol=1e-14)
        x, y = T.symbol('X', 3), T.symbol('Y', 3)
        contraction = x.contract(y, [(0, 2), (2, 0)])
        self.assertIsInstance(contraction, T.ContractionTerm)
        self.assertEqual(contraction.ndim, 2)
        av, bv = rng.normal(size=(2, 3, 3, 3)), rng.normal(size=(3, 3, 3))
        actual = T(contraction).eval({'X': T.ArrayStack((2,), av), 'Y': bv})
        expected = np.array([np.tensordot(v, bv, axes=([0, 2], [2, 0])) for v in av])
        np.testing.assert_allclose(actual, expected, atol=1e-14)
        derivative = x.permute((2, 0, 1)).dQ()
        dv = rng.normal(size=(5, 3, 3, 3))
        np.testing.assert_allclose(T(derivative).eval({'dQ(X)': dv}), dv.transpose(0, 3, 1, 2))

    def test_existing_terms_with_exact_isotropic_values(self):
        T = zach.TensorExpression
        a, b = T.symbol('A', 2), T.symbol('B', 3)
        delta = zach.IsotropicTensor.monomial(2, [(0, 1)])
        eps = zach.IsotropicTensor.monomial(3, epsilon=(0, 1, 2))
        for term in (a.contract(b, []), a.contract(b, [(0, 1)]), a.outer(b)):
            exact = T(term).eval({'A': delta, 'B': eps})
            dense = T(term).eval({'A': delta.as_array(), 'B': eps.as_array()})
            np.testing.assert_allclose(exact.as_array(), dense, atol=1e-14)
            self.assertTrue(all(isinstance(c, Fraction) for c in exact.terms.values()))
        scalar = a.contract(a, [(0, 0), (1, 1)])
        self.assertEqual(scalar.ndim, 0)
        self.assertEqual(T(scalar).eval({'A': delta}).terms[((), ())], 3)


if __name__ == '__main__':
    unittest.main()

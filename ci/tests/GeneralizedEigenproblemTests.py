import unittest
import numpy as np
from scipy.linalg import eigh, eig, block_diag
from McUtils.Numputils.GeneralizedEigenproblems import (
    generalized_eigh, fix_heiberger, robust_lobpcg, pivoted_cholesky,
    cholesky_orthogonalize, shifted_preconditioner, SingularPencilError,
    rank_projection_eigh, rank_completion_eigh, eigenpair_residuals
)


class GeneralizedEigenproblemTests(unittest.TestCase):
    def pencil(self, n=36, complex=False):
        random = np.random.default_rng(831)
        x = random.normal(size=(n, n))
        if complex:
            x = x + 1j * random.normal(size=(n, n))
        q = np.linalg.qr(x)[0]
        b = (q * np.geomspace(.2, 2, n)) @ q.conj().T
        a = (q * np.linspace(-3, 6, n)) @ q.conj().T
        return a, b

    def check(self, a, b, e, c, reference, atol=1e-8):
        np.testing.assert_allclose(e, reference[:len(e)], atol=atol, rtol=atol)
        np.testing.assert_allclose(c.conj().T @ (c if b is None else b @ c), np.eye(len(e)), atol=atol)
        self.assertLess(np.max(eigenpair_residuals(a, b, e, c), initial=0), atol * 10)

    def test_spd_solvers(self):
        for complex in [False, True]:
            a, b = self.pencil(complex=complex)
            reference = eigh(a, b, eigvals_only=True)
            for method in ['dense', 'cholesky', 'random-cholesky', 'accelerated-cholesky',
                           'fix-heiberger', 'rank-projection', 'rank-completion', 'lobpcg']:
                with self.subTest(method=method, complex=complex):
                    options = {'normal_rank': len(a)} if method.startswith('rank-') else {}
                    if method == 'lobpcg':
                        options.update(preconditioner='shifted', tolerance=1e-9, seed=4)
                    e, c = generalized_eigh(a, b, method=method, states=4, **options)
                    self.check(a, b, e, c, reference)
                    self.assertEqual(len(e), 4)

    def test_cholesky_factor_and_coverage(self):
        x = np.linspace(-2, 2, 80)
        b = np.exp(-.4 * (x[:, None] - x[None, :])**2)
        for method in ['greedy', 'random', 'accelerated']:
            with self.subTest(method=method):
                f, pivots, info = pivoted_cholesky(b, tolerance=1e-10, method=method,
                                                  seed=41, block_size=16, return_info=True)
                self.assertEqual(len(pivots), len(np.unique(pivots)))
                self.assertTrue(info['converged'])
                actual = np.diag(b - f @ f.conj().T)
                self.assertLess(actual.max(), 1.01e-10)
                np.testing.assert_allclose(actual, info['residual_diagonal'], atol=2e-14)
                np.testing.assert_allclose((f @ f.T)[pivots], b[pivots], atol=2e-11)

    def test_rank_limit(self):
        for method in ['greedy', 'random', 'accelerated']:
            f, pivots, info = pivoted_cholesky(np.eye(20), max_rank=3, method=method,
                                              seed=3, return_info=True)
            self.assertEqual(f.shape, (20, 3))
            self.assertFalse(info['converged'])

    def test_random_reproducibility(self):
        _, b = self.pencil()
        for method in ['random', 'accelerated']:
            first = pivoted_cholesky(b, max_rank=8, method=method, seed=10)
            second = pivoted_cholesky(b, max_rank=8, method=method, seed=10)
            np.testing.assert_array_equal(first[1], second[1])
            np.testing.assert_array_equal(first[0], second[0])

    def test_duplicate_padding(self):
        for copies in [1, 10, 100]:
            transform = np.zeros((2, copies + 1))
            transform[0, :copies], transform[1, -1] = 1, 1
            b = transform.T @ transform
            a = transform.T @ np.diag([2., 5.]) @ transform
            for method in ['cholesky', 'random-cholesky', 'accelerated-cholesky']:
                e, c, info = generalized_eigh(a, b, method=method, seed=12,
                                              return_info=True) if method != 'cholesky' else generalized_eigh(a, b, return_info=True)
                self.check(a, b, e, c, [2., 5.])
                self.assertEqual(info['rank'], 2)

    def test_weak_direction_with_duplicate_padding(self):
        for copies in [1, 10, 100, 1000]:
            transform = np.zeros((2, copies + 1))
            transform[0, :copies] = 1
            transform[:, -1] = [np.sqrt(1-1e-5), np.sqrt(1e-5)]
            b = transform.T @ transform
            a = transform.T @ np.diag([2., 5.]) @ transform
            for method in ['cholesky', 'random-cholesky', 'accelerated-cholesky']:
                options = {} if method=='cholesky' else {'seed':18}
                e, c, info = generalized_eigh(a, b, method=method, tolerance=1e-7,
                                              return_info=True, **options)
                self.assertEqual(info['rank'], 2)
                self.check(a, b, e, c, [2., 5.], atol=1e-7)

    def test_origin_and_scaling(self):
        a, b = self.pencil()
        for method in ['cholesky', 'random-cholesky', 'accelerated-cholesky', 'lobpcg',
                       'rank-projection', 'rank-completion']:
            options = {'normal_rank': len(a)} if method.startswith('rank-') else {}
            if method == 'lobpcg':
                options.update(preconditioner='shifted', tolerance=1e-8)
            if method != 'cholesky':
                options['seed'] = 16
            e, _ = generalized_eigh(a, b, method=method, states=3, **options)
            for shift in [-30., 100.]:
                en, cn = generalized_eigh(a + shift * b, b, method=method, states=3, **options)
                self.check(a, b, en - shift, cn, e, atol=2e-7)
            scales = np.geomspace(.1, 10, len(b))
            es, cs = generalized_eigh(a * scales[:, None] * scales[None, :],
                                      b * scales[:, None] * scales[None, :],
                                      method=method, states=3, **options)
            self.check(a, b, es, cs * scales[:, None], e, atol=2e-7)

    def test_shifted_cholesky_qr(self):
        random = np.random.default_rng(17)
        q = np.linalg.qr(random.normal(size=(80, 8)))[0]
        v = np.linalg.qr(random.normal(size=(8, 8)))[0]
        x = (q * np.geomspace(1, 1e-10, 8)) @ v.T
        u = cholesky_orthogonalize(x)
        np.testing.assert_allclose(u.T @ u, np.eye(8), atol=2e-12)
        np.testing.assert_allclose(q @ q.T @ u, u, atol=2e-6)

    def test_reprojection(self):
        random = np.random.default_rng(61)
        q = np.linalg.qr(random.normal(size=(60, 10)))[0]
        x = q[:, :5] + 1e-8 * q[:, 5:]
        u = cholesky_orthogonalize(x, against=q[:, :5])
        self.assertLess(np.max(abs(q[:, :5].T @ u)), 2e-12)
        np.testing.assert_allclose(u.T @ u, np.eye(5), atol=2e-12)

    def test_dependent_orthogonalization(self):
        with self.assertRaises(np.linalg.LinAlgError):
            cholesky_orthogonalize(np.zeros((8, 2)))

    def test_direct_generalized_lobpcg(self):
        a, b = self.pencil(n=80, complex=True)
        e, c, info = robust_lobpcg(a, b, states=4, block_size=8, seed=17,
                                  tolerance=1e-8, preconditioner='shifted', return_info=True)
        self.assertTrue(info['converged'])
        self.assertGreater(info['iterations'], 0)
        self.check(a, b, e, c, eigh(a, b, eigvals_only=True), atol=2e-8)

    def test_callable_lobpcg(self):
        a, b = self.pencil(n=70)
        initial = np.random.default_rng(71).normal(size=(70, 7))
        preconditioner, _ = shifted_preconditioner(a, b)
        e, c, info = robust_lobpcg(lambda x: a @ x, lambda x: b @ x, states=3,
            initial=initial, preconditioner=preconditioner, tolerance=1e-8, return_info=True)
        self.assertTrue(info['converged'])
        self.check(a, b, e, c, eigh(a, b, eigvals_only=True), atol=2e-8)

    def test_sparse_lobpcg(self):
        from scipy.sparse import diags
        diagonal = np.arange(1., 101.)
        a = diags(diagonal)
        e, c, info = robust_lobpcg(a, states=3, seed=75, tolerance=1e-8,
            preconditioner=lambda x:x/diagonal[:,None], return_info=True)
        self.assertTrue(info['converged'])
        self.check(a, None, e, c, [1., 2., 3.])

    def test_lobpcg_nonconvergence(self):
        a, _ = self.pencil(n=100)
        _, _, info = robust_lobpcg(a, states=3, seed=71, max_iterations=1,
                                   tolerance=1e-14, return_info=True)
        self.assertFalse(info['converged'])
        self.assertEqual(info['iterations'], 1)

    def test_preconditioner_origin(self):
        a, b = self.pencil()
        first, shift = shifted_preconditioner(a, b)
        second, shifted = shifted_preconditioner(a + 25 * b, b)
        self.assertAlmostEqual(shifted - shift, 25)
        np.testing.assert_allclose(first(np.eye(len(a))), second(np.eye(len(a))), atol=1e-12)

    def test_fix_heiberger_branches(self):
        cases = [
            (np.diag([3., 5., -2.]), np.diag([1., 1., 0.])),
            (np.array([[3., 0, 1], [0, 5, 0], [1, 0, 0]]), np.diag([1., 1., 0.])),
            (np.array([[3., 0, 0, 1], [0, 5, 0, 0], [0, 0, -2, 1], [1, 0, 1, 0]]), np.diag([1., 1., 0., 0.])),
            (np.array([[1., 2], [2, 0]]), np.diag([1., 0.])),
            (np.diag([3., -2.]), np.zeros((2, 2)))
        ]
        random = np.random.default_rng(772)
        for a, b in cases:
            q = np.linalg.qr(random.normal(size=a.shape))[0]
            a, b = q.T @ a @ q, q.T @ b @ q
            roots = eig(a, b, homogeneous_eigvals=True)[0]
            finite = abs(roots[1]) > 1e-8
            reference = np.sort((roots[0, finite] / roots[1, finite]).real)
            e, c = fix_heiberger(a, b, epsilon=1e-8, hamiltonian_tolerance=1e-10)
            self.assertEqual(len(e), len(reference))
            self.check(a, b, e, c, reference)

    def test_fix_heiberger_authors_example(self):
        a = np.diag(np.arange(6, 0, -1.).tolist() + [0., 0.])
        a[0, 6] = a[6, 0] = a[1, 7] = a[7, 1] = 1
        b = np.diag([1.] * 4 + [1e-15] * 4)
        e, _ = fix_heiberger(a, b, epsilon=1e-8)
        np.testing.assert_allclose(e, [3., 4.], atol=1e-12)

    def test_fix_heiberger_common_null(self):
        with self.assertRaises(SingularPencilError):
            fix_heiberger(np.diag([2., 0.]), np.diag([1., 0.]))

    def test_fix_heiberger_constraint_pivoting(self):
        a = np.diag([3., 5., 7., 0., 0.])
        coupling = np.array([[.01, 2.], [1., 0.], [0., 0.]])
        a[:3, 3:], a[3:, :3] = coupling, coupling.T
        b = np.diag([1., 1., 1., 0., 0.])
        e, c = fix_heiberger(a, b)
        self.check(a, b, e, c, [7.])

    def test_fix_heiberger_refinement(self):
        a = np.array([[2., .01], [.01, 3.]])
        b = np.diag([1., 1e-7])
        e, c = fix_heiberger(a, b, epsilon=1e-5, refine_metric=True)
        np.testing.assert_allclose(c.T @ b @ c, np.eye(1), atol=1e-12)
        self.assertAlmostEqual(e[0], (c.T @ a @ c).item(), places=12)

    def test_random_singular_pencils(self):
        random = np.random.default_rng(42)
        transform = random.normal(size=(4, 20))
        b = transform.T @ transform
        a = transform.T @ np.diag([-2., 1., 3., 6.]) @ transform
        for solver in [rank_projection_eigh, rank_completion_eigh]:
            for seed in [3, 12, 48]:
                e, c = solver(a, b, normal_rank=4, seed=seed)
                self.assertEqual(len(e), 4)
                self.check(a, b, e, c, [-2., 1., 3., 6.], atol=2e-8)
                en, cn = solver(a + 50 * b, b, normal_rank=4, seed=seed)
                self.check(a, b, en - 50, cn, e, atol=2e-7)

    def test_input_errors(self):
        with self.assertRaises(ValueError):
            generalized_eigh(np.eye(2), np.eye(2), method='missing')
        with self.assertRaises(ValueError):
            generalized_eigh(np.eye(2), np.eye(3))
        with self.assertRaises(ValueError):
            rank_projection_eigh(np.eye(2), np.eye(2), normal_rank=3)
        with self.assertRaises(np.linalg.LinAlgError):
            pivoted_cholesky(np.array([[1., 2.], [2., 1.]]))

    def test_random_pencils_nonzero_minimal_index(self):
        singular_a = np.array([[0., 0, 1], [0, 0, 0], [1, 0, 0]])
        singular_b = np.array([[0., 0, 0], [0, 0, -1], [0, -1, 0]])
        a, b = block_diag([[2.]], singular_a), block_diag([[1.]], singular_b)
        for solver in [rank_projection_eigh, rank_completion_eigh]:
            for seed in [3, 12]:
                e, c = solver(a, b, normal_rank=3, seed=seed, equilibrate=False)
                self.assertEqual(len(e), 1)
                self.check(a, b, e, c, [2.], atol=2e-8)


if __name__ == '__main__':
    unittest.main()

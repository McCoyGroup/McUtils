"""Independent quadrature and Taylor-order checks for Gaussian polynomial averages."""
import itertools
import unittest
import numpy as np
from McUtils.Numputils import gaussian_polynomial_integral


def quadrature(powers, coefficients, mean, covariance):
    nodes, weights = np.polynomial.hermite.hermgauss(1 + int(np.max(np.sum(powers, axis=-1))) // 2)
    indices = np.array(list(itertools.product(range(len(nodes)), repeat=len(mean))))
    coords = mean + np.sqrt(2) * nodes[indices] @ np.linalg.cholesky(covariance).T
    values = np.prod(coords[:, None, :] ** powers, axis=-1) @ coefficients
    return np.sum(np.prod(weights[indices] / np.sqrt(np.pi), axis=-1) * values)


class GaussianIntegralTests(unittest.TestCase):
    def test_quartic_groups_and_partial_sums(self):
        terms = gaussian_polynomial_integral([[4]], [1], [2.], [[3.]], return_expansion=True)
        np.testing.assert_allclose(terms, [16, 0, 72, 0, 27])
        self.assertEqual(gaussian_polynomial_integral([[4]], [1], [2.], [[3.]], expansion_degree=2), 88)

    def test_correlated_quadrature_and_sparse_dependencies(self):
        rng = np.random.default_rng(713)
        for ndim in (1, 2, 3, 6):
            powers = np.zeros((5, ndim), dtype=int)
            powers[1, 0] = 8
            powers[2, -1] = 4
            powers[3, 0] = 3; powers[3, -1] += 3
            powers[4] = powers[3]  # duplicate terms need not be combined
            matrix = rng.normal(size=(ndim, ndim)) / ndim
            covariance = matrix @ matrix.T + np.eye(ndim) * .1
            mean = rng.normal(size=ndim) / 3
            coefficients = rng.normal(size=5)
            # Use only active dimensions, so the independent tensor quadrature stays small.
            active = np.flatnonzero(np.any(powers, axis=0))
            expected = quadrature(powers[:, active], coefficients, mean[active],
                                  covariance[np.ix_(active, active)])
            with self.subTest(ndim=ndim):
                np.testing.assert_allclose(gaussian_polynomial_integral(powers, coefficients, mean, covariance),
                                           expected, atol=1e-11, rtol=1e-12)

    def test_batch_and_operator_axes(self):
        means = np.array([[.2, -.5], [.1, .7]])
        covariance = np.array([[.3, .1], [.1, .4]])
        coefficients = np.arange(12).reshape(2, 3, 2) + 1j
        powers = np.array([[2, 0], [1, 1]])
        observed = gaussian_polynomial_integral(powers, coefficients, means[:, None], covariance)
        for i in range(2):
            for j in range(3):
                np.testing.assert_allclose(observed[i, j], quadrature(powers, coefficients[i, j], means[i], covariance),
                                           atol=1e-13)

    def test_six_coupled_coordinates(self):
        rng = np.random.default_rng(892)
        matrix = rng.normal(size=(6, 6)) / 6
        covariance = matrix @ matrix.T + np.eye(6) * .1
        powers = np.array([[1, 1, 2, 1, 1, 2], [2, 0, 1, 1, 1, 1]])
        mean = rng.normal(size=6) / 3
        np.testing.assert_allclose(gaussian_polynomial_integral(powers, [1, -.4], mean, covariance),
                                   quadrature(powers, np.array([1, -.4]), mean, covariance), atol=1e-13)

    def test_complex_shift_keeps_odd_taylor_orders(self):
        center, shift, variance = 2., .3j, .7
        expected = np.array([center**4, 4 * center**3 * shift,
                             6 * center**2 * (shift**2 + variance),
                             4 * center * (shift**3 + 3 * shift * variance),
                             shift**4 + 6 * shift**2 * variance + 3 * variance**2])
        groups = gaussian_polynomial_integral([[4]], [1], [center + shift], [[variance]],
                                              expansion_center=[center], return_expansion=True)
        np.testing.assert_allclose(groups, expected, atol=1e-13)
        np.testing.assert_allclose(groups.sum(), quadrature(np.array([[4]]), np.array([1.]),
                                                           np.array([center + shift]), np.array([[variance]])))
        for order in range(5):
            np.testing.assert_allclose(gaussian_polynomial_integral(
                [[4]], [1], [center + shift], [[variance]], expansion_center=[center], expansion_degree=order),
                expected[:order + 1].sum())

    def test_empty_constant_and_zero_batch(self):
        np.testing.assert_array_equal(gaussian_polynomial_integral(np.empty((0, 2), dtype=int), [], [0, 0], np.eye(2)), 0)
        np.testing.assert_array_equal(gaussian_polynomial_integral([[0, 0]], [3], [0, 0], np.eye(2),
                                                                 expansion_degree=4, return_expansion=True), [3, 0, 0, 0, 0])
        self.assertEqual(gaussian_polynomial_integral([[1]], [2], np.empty((0, 1)), [[1]]).shape, (0,))

    def test_python_and_compiled_recurrences(self):
        import McUtils.Numputils.GaussianIntegrals as module
        compiled = module._gaussian_polynomial_integral
        if not hasattr(compiled, 'py_func'):
            self.skipTest('Numba is unavailable; other tests exercise the Python fallback')
        args = (np.array([[1., 2.]]), np.array([[.4, -.2]]), np.array([[.1, .3]]),
                np.array([[[.7, .1], [.1, .6]]]),
                *module._gaussian_polynomial_layout(((4, 2), (1, 3))), 6)
        np.testing.assert_allclose(compiled(*args), compiled.py_func(*args), atol=1e-13)

    def test_validation(self):
        for powers, coefficients, mean, covariance, options in (
            ([[-1]], [1], [0], [[1]], {}),
            ([[1.5]], [1], [0], [[1]], {}),
            ([[1]], [1, 2], [0], [[1]], {}),
            ([[1]], [1], [0, 1], [[1]], {}),
            ([[1]], [1], [0], [[1]], {'expansion_degree': -1}),
            ([[1]], [1], [0], [[1]], {'expansion_degree': 1.5}),
            ([[1]], [1], [0], [[1]], {'expansion_center': [0, 1]})
        ):
            with self.subTest(powers=powers, options=options), self.assertRaises(ValueError):
                gaussian_polynomial_integral(powers, coefficients, mean, covariance, **options)


if __name__ == '__main__':
    unittest.main()

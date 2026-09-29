"""Small, analytic systems for McUtils' iterative optimizer step finders.

Ready to place in McUtils/ci/tests once the suite path is writable. The Morse
systems are deliberately inexpensive and deterministic, so failures reflect
the optimizer rather than an external electronic-structure calculation.
"""

import unittest

import numpy as np
from numpy.testing import assert_allclose

from McUtils.Numputils.Optimization import (
    BofillApproximator,
    ConjugateGradientStepFinder,
    EigenvalueFollowingStepFinder,
    GradientDescentStepFinder,
    NewtonStepFinder,
    QuasiNewtonStepFinder,
    iterative_step_minimize,
)
from McUtils.Zachary.DifferentiableFunctions import MorseFunction


def morse_well():
    """Minimum at x = 1 with curvature 4."""
    return MorseFunction(de=2.0, a=1.0, re=1.0)


def two_dimensional_well():
    """Separable minimum at (1, -0.5), with unequal curvatures."""
    return (
        MorseFunction(de=2.0, a=1.0, re=1.0, inds=[0])
        + MorseFunction(de=1.0, a=1.2, re=-0.5, inds=[1])
    )


def index_one_saddle():
    """Stationary point at the origin with one negative Hessian eigenvalue."""
    return (
        -MorseFunction(de=1.0, a=1.0, re=0.0, inds=[0])
        + MorseFunction(de=1.0, a=1.2, re=0.0, inds=[1])
    )


def optimizer_callbacks(system):
    """Adapt a DifferentiableFunction to the optimizer's batch/mask API."""
    def value(guess, mask=None):
        return system(guess, order=0)[0]

    def gradient(guess, mask=None):
        return system(guess, order=1)[1]

    def hessian(guess, mask=None):
        return system(guess, order=2)[2]

    return value, gradient, hessian


class OptimizerFrameworkTests(unittest.TestCase):
    def assert_minimum(self, result, expected, tolerance=1e-6):
        point, converged, (error, iterations) = result
        self.assertTrue(converged)
        assert_allclose(point, expected, atol=tolerance, rtol=0)
        self.assertTrue(np.all(np.asarray(error) < tolerance))
        self.assertTrue(np.all(np.asarray(iterations) > 0))

    def test_morse_derivatives_and_shapes(self):
        system = two_dimensional_well()
        points = np.array([[0.8, -0.4], [1.2, -0.6]])
        value, gradient, hessian = optimizer_callbacks(system)
        self.assertEqual(value(points).shape, (2,))
        self.assertEqual(gradient(points).shape, (2, 2))
        self.assertEqual(hessian(points).shape, (2, 2, 2))

        step = 1e-5
        for axis in range(2):
            displacement = np.eye(2)[axis] * step
            finite_gradient = (
                value(points + displacement) - value(points - displacement)
            ) / (2 * step)
            finite_hessian = (
                gradient(points + displacement) - gradient(points - displacement)
            ) / (2 * step)
            assert_allclose(gradient(points)[:, axis], finite_gradient, atol=1e-8)
            assert_allclose(hessian(points)[:, :, axis], finite_hessian, atol=1e-8)

    def test_gradient_descent_morse_minimum(self):
        value, gradient, _ = optimizer_callbacks(morse_well())
        finder = GradientDescentStepFinder(value, gradient)
        result = iterative_step_minimize(
            np.array([0.8]), finder, tol=1e-6,
            max_iterations=60, logger=False,
        )
        self.assert_minimum(result, [1.0])

    def test_conjugate_gradient_morse_minimum(self):
        value, gradient, _ = optimizer_callbacks(morse_well())
        finder = ConjugateGradientStepFinder(value, gradient)
        result = iterative_step_minimize(
            np.array([0.8]), finder, tol=1e-6,
            max_iterations=60, logger=False,
        )
        self.assert_minimum(result, [1.0])

    def test_newton_batched_minima(self):
        value, gradient, hessian = optimizer_callbacks(two_dimensional_well())
        starts = np.array([[0.8, -0.4], [1.2, -0.6]])
        finder = NewtonStepFinder(value, gradient, hessian, line_search=False)
        result = iterative_step_minimize(
            starts, finder, max_displacement=0.05,
            tol=1e-6, max_iterations=60, logger=False,
        )
        self.assert_minimum(result, [[1.0, -0.5], [1.0, -0.5]])

    def test_newton_batch_with_already_converged_member(self):
        # A member that starts at the minimum must leave the active mask.
        value, gradient, hessian = optimizer_callbacks(two_dimensional_well())
        starts = np.array([[1.0, -0.5], [0.8, -0.4]])
        finder = NewtonStepFinder(value, gradient, hessian, line_search=False)
        result = iterative_step_minimize(
            starts, finder, max_displacement=0.05,
            tol=1e-6, max_iterations=60, logger=False,
        )
        point, converged, (error, iterations) = result
        self.assertTrue(converged)
        assert_allclose(point, [[1.0, -0.5], [1.0, -0.5]], atol=1e-6)
        self.assertTrue(np.all(error < 1e-6))
        self.assertEqual(iterations[0], 0)
        self.assertGreater(iterations[1], 0)

    def test_newton_method_resolution(self):
        value, gradient, hessian = optimizer_callbacks(two_dimensional_well())
        result = iterative_step_minimize(
            np.array([0.8, -0.4]),
            value, jacobian=gradient, hessian=hessian, method="newton",
            tol=1e-6, max_iterations=60, logger=False,
        )
        self.assert_minimum(result, [1.0, -0.5])

    def test_quasi_newton_batched_minima(self):
        value, gradient, _ = optimizer_callbacks(two_dimensional_well())
        starts = np.array([[0.8, -0.4], [1.2, -0.6]])
        finder = QuasiNewtonStepFinder(value, gradient, line_search=False)
        result = iterative_step_minimize(
            starts, finder, max_displacement=0.05,
            tol=1e-6, max_iterations=60, logger=False,
        )
        self.assert_minimum(result, [[1.0, -0.5], [1.0, -0.5]])

    def test_quasi_newton_direct_bofill_minimum(self):
        value, gradient, _ = optimizer_callbacks(two_dimensional_well())
        finder = QuasiNewtonStepFinder(
            value, gradient, approximation_type='bofill',
            approximation_mode='direct', line_search=False,
        )
        result = iterative_step_minimize(
            np.array([[0.8, -0.4], [1.2, -0.6]]), finder,
            max_displacement=0.05, tol=1e-6,
            max_iterations=80, logger=False,
        )
        self.assert_minimum(result, [[1.0, -0.5], [1.0, -0.5]])

    def test_saddle_hessian_identifies_followed_mode(self):
        _, gradient, hessian = optimizer_callbacks(index_one_saddle())
        origin = np.zeros((1, 2))
        assert_allclose(gradient(origin), np.zeros((1, 2)), atol=1e-12)
        rotation = np.array([[1.0, -1.0], [1.0, 1.0]]) / np.sqrt(2.0)
        rotated_hessian = rotation @ hessian(origin)[0] @ rotation.T
        eigenvalues, eigenvectors = np.linalg.eigh(rotated_hessian)
        assert_allclose(eigenvalues, [-2.0, 2.88], atol=1e-12)
        self.assertEqual(np.count_nonzero(eigenvalues < 0), 1)
        assert_allclose(
            np.abs(eigenvectors[:, 0]), np.abs(rotation[:, 0]), atol=1e-12
        )

    def test_bofill_secant_update_on_saddle(self):
        _, gradient, hessian = optimizer_callbacks(index_one_saddle())
        initial = np.array([[0.1, 0.1], [-0.1, -0.1], [0.0, 0.0]])
        moved = np.array([[0.06, 0.05], [-0.05, -0.06], [0.0, 0.0]])
        displacement = moved - initial
        gradient_change = gradient(moved) - gradient(initial)
        exact_hessian = hessian(initial)
        identities = np.broadcast_to(np.eye(2), exact_hessian.shape)

        for mode in ('direct', 'inverse'):
            with self.subTest(mode=mode):
                initial_matrix = (
                    exact_hessian if mode == 'direct'
                    else np.linalg.inv(exact_hessian)
                )
                original = initial_matrix.copy()
                approximator = BofillApproximator(
                    None, None, line_search=False, approximation_mode=mode
                )
                updated = approximator.get_hessian_update(
                    identities, gradient_change, displacement, initial_matrix
                )
                self.assertEqual(updated.shape, initial_matrix.shape)
                assert_allclose(updated, np.swapaxes(updated, -1, -2), atol=1e-12)
                assert_allclose(initial_matrix, original)
                assert_allclose(updated[-1], initial_matrix[-1])
                product = (
                    np.einsum('bij,bj->bi', updated, displacement)
                    if mode == 'direct' else
                    np.einsum('bij,bj->bi', updated, gradient_change)
                )
                target = gradient_change if mode == 'direct' else displacement
                assert_allclose(product, target, atol=1e-10)

    def test_eigenvalue_following_targets_negative_hessian_mode(self):
        value, gradient, hessian = optimizer_callbacks(index_one_saddle())

        def masked_hessian(guess, mask):
            assert_allclose(mask, [0])
            return hessian(guess)

        finder = EigenvalueFollowingStepFinder(
            value, gradient, masked_hessian, target_mode=np.array([1.0, 0.0]),
            line_search=False,
        )
        point = np.array([[0.1, 0.1]])
        step, evaluated_gradient = finder(point, np.array([0]))
        self.assertEqual(step.shape, point.shape)
        assert_allclose(evaluated_gradient, gradient(point))
        self.assertTrue(np.all(np.isfinite(step)))
        self.assertLess(abs(point[0, 0] + step[0, 0]), abs(point[0, 0]))
        self.assertLess(abs(point[0, 1] + step[0, 1]), abs(point[0, 1]))

    def test_eigenvalue_following_selects_requested_mode(self):
        value, gradient, hessian = optimizer_callbacks(index_one_saddle())
        point = np.array([[0.1, 0.1]])
        finder = EigenvalueFollowingStepFinder(
            value, gradient, hessian, target_mode=1
        )
        step, _ = finder(point, np.array([0]))
        # Following the positive mode ascends along y and descends along the
        # negative x mode, so both coordinates move away from this saddle.
        self.assertGreater(step[0, 0], 0)
        self.assertGreater(step[0, 1], 0)

    def test_eigenvalue_following_tracks_mode_across_eigenvalue_reordering(self):
        value, gradient, hessian = optimizer_callbacks(index_one_saddle())
        finder = EigenvalueFollowingStepFinder(value, gradient, hessian)
        first_values, first_vectors = np.linalg.eigh(
            np.array([[[-2.0, 0.0], [0.0, 3.0]]])
        )
        _, selected_vector = finder.get_shift(first_values, first_vectors, 0)
        later_values, later_vectors = np.linalg.eigh(
            np.array([[[4.0, 0.0], [0.0, -1.0]]])
        )
        shifts, tracked_vector = finder.get_shift(
            later_values, later_vectors, selected_vector
        )
        assert_allclose(np.abs(tracked_vector), [[1.0, 0.0]])
        effective_curvatures = later_values + shifts
        self.assertLess(effective_curvatures[0, 1], 0)
        self.assertGreater(effective_curvatures[0, 0], 0)

    def test_eigenvalue_following_batched_saddles(self):
        value, gradient, hessian = optimizer_callbacks(index_one_saddle())
        starts = np.array([[0.1, 0.1], [-0.1, -0.1]])
        targets = (None, 0, np.array([[1.0, 0.0], [-1.0, 0.0]]))
        for target in targets:
            with self.subTest(target=target):
                finder = EigenvalueFollowingStepFinder(
                    value, gradient, hessian, target_mode=target
                )
                point, converged, (error, iterations) = iterative_step_minimize(
                    starts, finder, max_displacement=0.05, tol=1e-6,
                    max_iterations=80, logger=False,
                )
                self.assertTrue(converged)
                assert_allclose(point, np.zeros_like(point), atol=1e-5)
                self.assertTrue(np.all(error < 1e-6))
                self.assertTrue(np.all(iterations > 1))

    def test_eigenvalue_following_rotated_saddle(self):
        base_value, base_gradient, base_hessian = optimizer_callbacks(index_one_saddle())
        rotation = np.array([[1.0, -1.0], [1.0, 1.0]]) / np.sqrt(2.0)

        def value(guess, mask=None):
            return base_value(guess @ rotation)

        def gradient(guess, mask=None):
            return base_gradient(guess @ rotation) @ rotation.T

        def hessian(guess, mask=None):
            return rotation @ base_hessian(guess @ rotation) @ rotation.T

        finder = EigenvalueFollowingStepFinder(
            value, gradient, hessian, target_mode=rotation[:, 0]
        )
        point, converged, (error, _) = iterative_step_minimize(
            np.array([0.1, -0.1]), finder, max_displacement=0.05,
            tol=1e-6, max_iterations=80, logger=False,
        )
        self.assertTrue(converged)
        assert_allclose(point, [0.0, 0.0], atol=1e-5)
        self.assertLess(error, 1e-6)

    def test_eigenvalue_following_method_resolution(self):
        value, gradient, hessian = optimizer_callbacks(index_one_saddle())
        point, converged, (error, _) = iterative_step_minimize(
            np.array([0.1, 0.1]), value,
            jacobian=gradient, hessian=hessian, method='eigenvalue-following',
            max_displacement=0.05, tol=1e-6, max_iterations=80,
            logger=False,
        )
        self.assertTrue(converged)
        assert_allclose(point, [0.0, 0.0], atol=1e-5)
        self.assertLess(error, 1e-6)

    def test_eigenvalue_following_updates_with_actual_step(self):
        value, gradient, hessian = optimizer_callbacks(index_one_saddle())
        finder = EigenvalueFollowingStepFinder(value, gradient, hessian)
        point = np.array([[0.1, 0.1]])
        step, _ = finder(point, np.array([0]))
        actual_step = step / 2
        next_point = point + actual_step
        finder(next_point, np.array([0]))
        gradient_change = gradient(next_point) - gradient(point)
        assert_allclose(
            finder.prev_hess[0] @ actual_step[0], gradient_change[0],
            atol=1e-10,
        )


if __name__ == "__main__":
    unittest.main()

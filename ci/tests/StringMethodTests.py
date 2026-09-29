"""Analytic and path-level checks for the reparameterized string optimizer."""

import unittest

import numpy as np
from numpy.testing import assert_allclose

from McUtils.Numputils.Optimization import (
    InterpolatingReparametrizer,
    StringMethodStepFinder,
    string_method_minimize,
)
from McUtils.Zachary.DifferentiableFunctions import GaussianFunction


def muller_brown():
    amplitudes = [-200, -100, -170, 15]
    a = [-1, -1, -6.5, .7]
    b = [0, 0, 11, .6]
    c = [-10, -10, -6.5, .7]
    centers = [[1, 0], [0, .5], [-.5, 1.5], [-1, 1]]
    return sum(
        GaussianFunction(amplitude, center, [[ai, bi / 2], [bi / 2, ci]])
        for amplitude, ai, bi, ci, center in zip(amplitudes, a, b, c, centers)
    )


def callbacks(system):
    def value(points, mask=None):
        return system(points, order=0)[0]

    def gradient(points, mask=None):
        return system(points, order=1)[1]

    return value, gradient


class StringMethodTests(unittest.TestCase):
    def test_gaussian_derivatives_on_muller_brown(self):
        system = muller_brown()
        points = np.array([[-.3, 1.1], [.3, .2], [.1, .7]])
        energy, gradient, hessian = system(points, order=2)
        self.assertEqual(energy.shape, (3,))
        self.assertEqual(gradient.shape, (3, 2))
        self.assertEqual(hessian.shape, (3, 2, 2))
        for axis in range(2):
            displacement = np.eye(2)[axis] * 1e-5
            plus = system(points + displacement, order=1)
            minus = system(points - displacement, order=1)
            assert_allclose(gradient[:, axis], (plus[0] - minus[0]) / 2e-5,
                            atol=1e-6, rtol=1e-7)
            assert_allclose(hessian[:, :, axis], (plus[1] - minus[1]) / 2e-5,
                            atol=2e-5, rtol=1e-6)

    def test_arc_length_reparameterization_keeps_anchors(self):
        paths = np.array([
            [[0., 0.], [.1, 0.], [1., 0.], [1.1, 0.], [3., 0.]],
            [[0., 0.], [0., .1], [0., 1.], [0., 1.1], [0., 3.]],
        ])
        new_paths, moved, fixed = InterpolatingReparametrizer()(paths, [0, 2, 4])
        assert_allclose(new_paths[:, [0, 2, 4]], paths[:, [0, 2, 4]])
        assert_allclose(new_paths[0, :, 0], [0, .5, 1, 2, 3])
        assert_allclose(new_paths[1, :, 1], [0, .5, 1, 2, 3])
        self.assertEqual(fixed, [0, 2, 4])
        self.assertTrue(np.all(moved[:, [1, 3]]))
        self.assertFalse(np.any(moved[:, [0, 2, 4]]))

    def test_muller_brown_string_relaxes_and_reparameterizes(self):
        value, gradient = callbacks(muller_brown())
        start = np.array([-.558, 1.442])
        end = np.array([.623, .028])
        (images, image_counts), converged, (_, iterations) = string_method_minimize(
            start, end, value, gradient, n_images=16, step_size=.0003,
            max_iterations=250, max_displacement_norm=.05, tol=.03,
        )
        self.assertTrue(converged)
        self.assertGreater(iterations, 0)
        self.assertEqual(image_counts.item(), 16)
        assert_allclose(images[[0, -1]], [start, end], atol=1e-12)
        distances = np.linalg.norm(np.diff(images, axis=0), axis=1)
        self.assertLess(np.ptp(distances), 1e-4)
        self.assertLess(np.max(value(images)), -40.)
        self.assertGreater(np.max(value(images)), -50.)
        finder = StringMethodStepFinder(value, gradient, step_size=.0003)
        projected = [
            finder.adjust_jacobian(gradient(images[j:j + 1]),
                                   images[np.newaxis], np.array([0]),
                                   j, j - 1, j + 1)[0]
            for j in range(1, len(images) - 1)
        ]
        self.assertLess(np.max(np.abs(projected)), .04)

    def test_batch_skips_an_already_stationary_string(self):
        value, gradient = callbacks(
            GaussianFunction(-1., [0., 0.], [[-1., 0.], [0., -1.]])
        )
        initial = np.broadcast_to(
            np.stack([np.linspace(-1, 1, 7), np.zeros(7)], axis=-1),
            (2, 7, 2)
        ).copy()
        initial[1, 1:-1, 1] = .1
        (images, counts), _, (_, iterations) = string_method_minimize(
            initial[:, 0], initial[:, -1], value, gradient,
            initial_images=initial, step_size=.05, max_iterations=5, tol=1e-5,
        )
        self.assertEqual(images.shape, (2, 7, 2))
        assert_allclose(images[:, [0, -1]], initial[:, [0, -1]])
        assert_allclose(images[0], initial[0])
        self.assertEqual(iterations[0], 0)
        self.assertGreater(iterations[1], 0)
        assert_allclose(counts, [7, 7])

    def test_reembedding_skips_converged_images(self):
        value = lambda points, mask=None: np.zeros(points.shape[0])
        gradient = lambda points, mask=None: np.zeros_like(points)
        (images, _), converged, _ = string_method_minimize(
            [0., 0., 0.], [1., 0., 0.], value, gradient,
            n_images=5, embedding_options={}, reembed=True,
            max_iterations=2,
        )
        self.assertTrue(converged)
        assert_allclose(images[:, 0], np.linspace(0., 1., 5))


if __name__ == '__main__':
    unittest.main()

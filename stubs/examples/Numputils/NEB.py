"""Extracted from NumputilsTests.test_NEB via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest NumputilsTests.test_NEB"""

import collections
import itertools
import math
import os.path
from Peeves.TestUtils import *
from Peeves import BlockProfiler
import McUtils.Numputils as nput
from McUtils.Numputils import *
from McUtils.Zachary import FiniteDifferenceDerivative
from unittest import TestCase
import numpy as np, scipy, functools as ft

class NumputilsTests(TestCase):
    problem_coords = np.array([[-1.86403557e-17, -0.076046524, 0.0462443228], [6.70904773e-17, -0.076046524, -0.953755677], [0.929682337, 0.292315732, 0.0462443228], [2.46519033e-32, -1.38777878e-17, 0.225076602], [-1.97215226e-31, 1.4371441, -0.90030641], [-1.75999392e-16, -1.4371441, -0.90030641]])

    @classmethod
    def setUp(self):
        np.set_printoptions(linewidth=100000000.0)

    @validationTest
    def test_NEB(self):
        ndim = 1
        np.random.seed(1)
        if ndim == 1:
            rot = np.array([[1]])
        else:
            rot = rotation_matrix_skew(np.random.rand(math.comb(ndim, 2)))

        def f(guess, *_):
            guess = (rot[np.newaxis] @ guess[:, :, np.newaxis]).reshape(guess.shape)
            return np.sum(np.sin(guess), axis=-1) + 1 / 2 * np.sum(guess ** 2, axis=-1)

        def fjac(guess, *_):
            guess = (rot[np.newaxis] @ guess[:, :, np.newaxis]).reshape(guess.shape)
            return (rot.T[np.newaxis] @ (np.cos(guess) + guess)[:, :, np.newaxis]).reshape(guess.shape)

        def fhess(guess, *_):
            guess = (rot[np.newaxis] @ guess[:, :, np.newaxis]).reshape(guess.shape)
            h = -vec_tensordiag(np.sin(guess)) + identity_tensors(guess.shape[:-1], guess.shape[-1])
            return rot.T[np.newaxis] @ h @ rot[np.newaxis]
        np.random.seed(1)
        guess = vec_normalize(np.random.uniform(-np.pi / 2, np.pi / 2, ndim))
        minimum, convd, (error, its) = iterative_step_minimize(guess, [NewtonStepFinder(f, fjac, fhess)], max_displacement=0.1, max_iterations=50, unitary=True, tol=1e-15)
        print()
        print(error, its)
        print(guess, np.linalg.norm(guess, axis=-1))
        print(minimum, np.linalg.norm(minimum, axis=-1))

"""
Tests for the drafted `McUtils.Numputils.Multipoles` module.

Until the patch is applied, the draft is loaded from `claude_drafts/multipoles`
into the `McUtils.Numputils` package namespace so its relative imports resolve.
Once merged, the loader block reduces to `import McUtils.Numputils as mp`.
"""

import importlib.util
import itertools
import math
import os
import sys
import unittest

import numpy as np
import scipy.special

import McUtils.Numputils as nput

if hasattr(nput, "multipole_moments"):
    mp = nput
else:
    # the dev-tree shim (`McUtils/Numputils.py`) re-exports `McUtils.McUtils.Numputils`
    _pkg = getattr(nput, "__identifier__", nput.__name__)
    _path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Multipoles.py")
    _spec = importlib.util.spec_from_file_location(_pkg + ".Multipoles", _path)
    mp = importlib.util.module_from_spec(_spec)
    mp.__package__ = _pkg
    sys.modules[_spec.name] = mp
    _spec.loader.exec_module(mp)


def direct_potential(src, q, pts):
    d = pts[..., :, np.newaxis, :] - src[..., np.newaxis, :, :]
    return np.sum(q[..., np.newaxis, :] / np.linalg.norm(d, axis=-1), axis=-1)

def direct_derivs(src, q, pts):
    d = pts[:, None, :] - src[None, :, :]
    r = np.linalg.norm(d, axis=-1)
    grad = -np.sum(q[None, :, None] * d / r[..., None] ** 3, axis=1)
    eye = np.eye(3)
    hess = np.sum(
        q[None, :, None, None] * (3 * d[..., :, None] * d[..., None, :] - (r ** 2)[..., None, None] * eye)
        / r[..., None, None] ** 5,
        axis=1
    )
    return grad, hess


class MultipoleTests(unittest.TestCase):

    def setUp(self):
        self.rng = np.random.default_rng(1234)
        self.src = self.rng.uniform(-.5, .5, (40, 3))
        self.q = self.rng.normal(size=40)
        self.far = self.rng.normal(size=(25, 3))
        self.far = 6 * self.far / np.linalg.norm(self.far, axis=-1)[:, None]

    def test_HarmonicsVsScipy(self):
        L = 9
        pts = self.rng.normal(size=(30, 3))
        r = np.linalg.norm(pts, axis=-1)
        theta = np.arccos(pts[:, 2] / r)
        phi = np.arctan2(pts[:, 1], pts[:, 0])
        R = mp.solid_harmonics(pts, L, kind='regular')
        I = mp.solid_harmonics(pts, L, kind='irregular')
        for l in range(L + 1):
            for m in range(l + 1):
                Y = scipy.special.sph_harm_y(l, m, theta, phi)
                norm = math.sqrt((2 * l + 1) / (4 * np.pi) * math.factorial(l - m) / math.factorial(l + m))
                Pe = Y / norm
                p = l * (l + 1) // 2 + m
                self.assertTrue(np.allclose(R[:, p], r ** l * Pe / math.factorial(l + m)), (l, m))
                self.assertTrue(np.allclose(I[:, p], math.factorial(l - m) * Pe / r ** (l + 1)), (l, m))

    def test_RealLayout(self):
        pts = self.rng.normal(size=(5, 3))
        x, y, z = pts.T
        r2 = np.sum(pts ** 2, axis=-1)
        S = mp.solid_harmonics(pts, 4, real=True)
        self.assertEqual(S.shape, (5, 25))
        # l = 1 is (y, z, x); l = 2 in Racah normalization
        self.assertTrue(np.allclose(S[:, 1:4], pts[:, [1, 2, 0]]))
        s3 = np.sqrt(3)
        l2 = np.stack([s3 * x * y, s3 * y * z, (3 * z ** 2 - r2) / 2, s3 * x * z, s3 / 2 * (x ** 2 - y ** 2)], axis=-1)
        self.assertTrue(np.allclose(S[:, 4:9], l2))
        # against scipy for all l, both kinds
        r = np.sqrt(r2)
        theta = np.arccos(z / r)
        phi = np.arctan2(y, x)
        Si = mp.solid_harmonics(pts, 4, kind='irregular', real=True)
        for l in range(5):
            for m in range(-l, l + 1):
                Y = scipy.special.sph_harm_y(l, abs(m), theta, phi)
                Yr = Y.real if m == 0 else np.sqrt(2) * (-1) ** abs(m) * (Y.real if m > 0 else Y.imag)
                C = np.sqrt(4 * np.pi / (2 * l + 1)) * Yr
                self.assertTrue(np.allclose(S[:, l * l + l + m], r ** l * C), (l, m))
                self.assertTrue(np.allclose(Si[:, l * l + l + m], C / r ** (l + 1)), (l, m))

    def test_RealMultipoleConversion(self):
        L = 6
        M = mp.multipole_moments(self.src, self.q, L)
        real = mp.multipoles_to_real_spherical(M)
        self.assertTrue(np.allclose(real, self.q @ mp.solid_harmonics(self.src, L, real=True)))
        self.assertTrue(np.allclose(real[1:4], (self.q @ self.src)[[1, 2, 0]]))
        self.assertTrue(np.allclose(mp.real_spherical_to_multipoles(real), M))

    def test_MultipolePotential(self):
        errs = []
        exact = direct_potential(self.src, self.q, self.far)
        for L in (2, 6, 12):
            M = mp.multipole_moments(self.src, self.q, L)
            errs.append(np.max(np.abs(mp.multipole_potential(M, self.far) - exact)))
        self.assertTrue(errs[0] > errs[1] > errs[2])
        self.assertLess(errs[-1], 1e-10)

    def test_TranslateMultipoles(self):
        L = 7
        c0 = np.array([.1, -.2, .3])
        c1 = np.array([-.4, .25, .05])
        M0 = mp.multipole_moments(self.src, self.q, L, center=c0)
        M1 = mp.multipole_moments(self.src, self.q, L, center=c1)
        self.assertTrue(np.allclose(mp.translate_multipoles(M0, c1 - c0), M1))

    def test_LocalExpansions(self):
        L = 10
        cM = np.zeros(3)
        cL = np.array([5., 1., -2.])
        tgt = cL + self.rng.uniform(-.4, .4, (20, 3))
        exact = direct_potential(self.src, self.q, tgt)
        M = mp.multipole_moments(self.src, self.q, L, center=cM)
        F = mp.multipoles_to_local_multipoles(M, cL - cM)
        self.assertLess(np.max(np.abs(mp.local_multipole_potential(F, tgt, center=cL) - exact)), 1e-6)
        # P2L agrees with the direct sum, L2L is exact
        F_direct = mp.local_multipole_expansion(self.src, self.q, L, center=cL)
        self.assertLess(np.max(np.abs(mp.local_multipole_potential(F_direct, tgt, center=cL) - exact)), 1e-6)
        cL2 = cL + np.array([.1, -.15, .2])
        F2 = mp.translate_local_multipoles(F_direct, cL2 - cL)
        # a truncated local expansion is a polynomial; L2L re-centers it exactly
        self.assertTrue(np.allclose(
            mp.local_multipole_potential(F2, tgt, center=cL2),
            mp.local_multipole_potential(F_direct, tgt, center=cL),
            rtol=1e-12, atol=1e-12
        ))
        # and converges to the directly built expansion at the new center
        F2_direct = mp.local_multipole_expansion(self.src, self.q, L, center=cL2)
        self.assertLess(np.max(np.abs(F2 - F2_direct)[:3]), 1e-6)

    def test_MultipoleDerivatives(self):
        M = mp.multipole_moments(self.src, self.q, 14)
        V, dV, d2V = mp.multipole_potential(M, self.far, deriv_order=2)
        grad, hess = direct_derivs(self.src, self.q, self.far)
        self.assertTrue(np.allclose(V, direct_potential(self.src, self.q, self.far)))
        self.assertTrue(np.allclose(dV, grad, atol=1e-10))
        self.assertTrue(np.allclose(d2V, hess, atol=1e-10))

    def test_LocalDerivatives(self):
        cL = np.array([5., 1., -2.])
        tgt = cL + self.rng.uniform(-.3, .3, (10, 3))
        F = mp.local_multipole_expansion(self.src, self.q, 14, center=cL)
        V, dV, d2V = mp.local_multipole_potential(F, tgt, center=cL, deriv_order=2)
        grad, hess = direct_derivs(self.src, self.q, tgt)
        self.assertTrue(np.allclose(dV, grad, atol=1e-8))
        self.assertTrue(np.allclose(d2V, hess, atol=1e-8))

    def test_Batching(self):
        src = self.rng.uniform(-.5, .5, (4, 30, 3))
        q = self.rng.normal(size=(4, 30))
        centers = self.rng.normal(size=(4, 3)) * .1
        M = mp.multipole_moments(src, q, 5, center=centers)
        self.assertEqual(M.shape, (4, 21))
        for i in range(4):
            self.assertTrue(np.allclose(M[i], mp.multipole_moments(src[i], q[i], 5, center=centers[i])))
        shifts = self.rng.normal(size=(4, 3))
        T = mp.translate_multipoles(M, shifts)
        for i in range(4):
            self.assertTrue(np.allclose(T[i], mp.translate_multipoles(M[i], shifts[i])))
        V = mp.multipole_potential(M, self.far[np.newaxis] * 2, center=centers)
        self.assertEqual(V.shape, (4, 25))

    def test_CartesianConversions(self):
        L = 5
        raw = mp.cartesian_multipole_moments(self.src, self.q, L)
        self.assertTrue(np.allclose(raw[1], self.q @ self.src))
        self.assertTrue(np.allclose(raw[2], np.einsum('i,ia,ib->ab', self.q, self.src, self.src)))
        M = mp.multipole_moments(self.src, self.q, L)
        self.assertTrue(np.allclose(mp.cartesian_to_spherical_multipoles(raw), M))
        # dipole components: M_10 = mu_z, M_11 = -(mu_x + i mu_y)/2
        self.assertTrue(np.isclose(M[1], raw[1][2]))
        self.assertTrue(np.isclose(M[2], -(raw[1][0] + 1j * raw[1][1]) / 2))
        tl = mp.cartesian_multipole_moments(self.src, self.q, L, convention='traceless')
        Q = raw[2] - np.eye(3) * np.trace(raw[2]) / 3
        self.assertTrue(np.allclose(tl[2], Q))
        bk = mp.cartesian_multipole_moments(self.src, self.q, L, convention='buckingham')
        self.assertTrue(np.allclose(bk[2], 1.5 * Q))
        for l in range(2, L + 1):
            t = tl[l]
            self.assertTrue(np.allclose(np.trace(t, axis1=0, axis2=1), 0), l)
            for p in itertools.permutations(range(l)):
                self.assertTrue(np.allclose(t, t.transpose(p)))
        self.assertTrue(np.allclose(mp.cartesian_to_spherical_multipoles(tl, convention='traceless'), M))
        self.assertTrue(np.allclose(mp.cartesian_to_spherical_multipoles(bk, convention='buckingham'), M))

    # region rotations

    @staticmethod
    def random_rotations(rng, n):
        Q, _ = np.linalg.qr(rng.normal(size=(n, 3, 3)))
        return Q * np.sign(np.linalg.det(Q))[:, None, None]

    def test_RotateMultipoles(self):
        L = 9
        Qs = self.random_rotations(self.rng, 4)
        Qs = np.concatenate([Qs, -Qs[:1], np.eye(3)[None]])  # include an improper rotation and the identity
        M = mp.multipole_moments(self.src, self.q, L)
        rot = mp.rotate_multipoles(np.broadcast_to(M, (len(Qs), M.shape[-1])), Qs)
        for Q, Mr in zip(Qs, rot):
            self.assertTrue(np.allclose(Mr, mp.multipole_moments(self.src @ Q.T, self.q, L)))
        # rotation about a nonzero center
        c = np.array([.3, -.2, .5])
        Mc = mp.multipole_moments(self.src, self.q, L, center=c)
        Q = Qs[0]
        moved = (self.src - c) @ Q.T + c
        self.assertTrue(np.allclose(mp.rotate_multipoles(Mc, Q), mp.multipole_moments(moved, self.q, L, center=c)))
        # composition
        T12 = mp.rotate_multipoles(M, Qs[0] @ Qs[1])
        self.assertTrue(np.allclose(T12, mp.rotate_multipoles(mp.rotate_multipoles(M, Qs[1]), Qs[0])))

    def test_RotateLocalMultipoles(self):
        L = 8
        cL = np.array([5., 1., -2.])
        Q = self.random_rotations(self.rng, 1)[0]
        F = mp.local_multipole_expansion(self.src, self.q, L, center=cL)
        moved = (self.src - cL) @ Q.T + cL
        self.assertTrue(np.allclose(
            mp.rotate_local_multipoles(F, Q),
            mp.local_multipole_expansion(moved, self.q, L, center=cL)
        ))

    # endregion

    # region smearing

    def test_SmearedMonopole(self):
        sigma = .7
        M = mp.multipole_moments(np.zeros((1, 3)), np.array([1.3]), 0)
        pts = self.rng.normal(size=(20, 3)) * 1.5
        r = np.linalg.norm(pts, axis=-1)
        V = mp.multipole_potential(M, pts, smearing=sigma)
        self.assertTrue(np.allclose(V, 1.3 * scipy.special.erf(r / (np.sqrt(2) * sigma)) / r))
        V0 = mp.multipole_potential(M, np.zeros((1, 3)), smearing=sigma)
        self.assertTrue(np.allclose(V0, 1.3 * np.sqrt(2 / np.pi) / sigma))

    def test_SmearedDipole(self):
        # an l = 1 GTO density is -p . grad of a unit Gaussian, so V_1 = -p . grad V_0
        sigma = .6
        p = np.array([.3, -.8, .5])
        M = mp.real_spherical_to_multipoles(np.concatenate([[0.], p[[1, 2, 0]]]))
        unit = mp.multipole_moments(np.zeros((1, 3)), np.ones(1), 1)
        pts = self.rng.normal(size=(20, 3))
        V, dV, d2V = mp.multipole_potential(M, pts, smearing=sigma, deriv_order=2)
        V0, dV0, d2V0 = mp.multipole_potential(unit, pts, smearing=sigma, deriv_order=2)
        self.assertTrue(np.allclose(V, -dV0 @ p))
        self.assertTrue(np.allclose(dV, -d2V0 @ p))

    def test_SmearedPoisson(self):
        # lap V = -4 pi rho for the GTO density, checks every l and the second derivatives
        L = 3
        sigma = .8
        real = self.rng.normal(size=(L + 1) ** 2)
        M = mp.real_spherical_to_multipoles(real)
        pts = self.rng.normal(size=(15, 3)) * .9
        _, _, d2V = mp.multipole_potential(M, pts, smearing=sigma, deriv_order=2)
        S = mp.solid_harmonics(pts, L, real=True)
        r2 = np.sum(pts ** 2, axis=-1)
        rho = 0
        for l in range(L + 1):
            Cl = 1 / (np.sqrt(4 * np.pi / (2 * l + 1)) * 2 ** ((2 * l + 1) / 2)
                      * scipy.special.gamma((2 * l + 3) / 2) * sigma ** (2 * l + 3))
            # C_l r^l Y_lm = C_l sqrt((2l+1)/4pi) S_lm
            rho = rho + Cl * np.sqrt((2 * l + 1) / (4 * np.pi)) * np.exp(-r2 / (2 * sigma ** 2)) * (
                    S[:, l * l:(l + 1) ** 2] @ real[l * l:(l + 1) ** 2])
        self.assertTrue(np.allclose(np.trace(d2V, axis1=-2, axis2=-1), -4 * np.pi * rho))

    def test_SmearedFarField(self):
        L = 3
        M = mp.real_spherical_to_multipoles(self.rng.normal(size=(L + 1) ** 2))
        far = self.far * 3
        self.assertTrue(np.allclose(
            mp.multipole_potential(M, far, smearing=.5),
            mp.multipole_potential(M, far)
        ))

    def test_SmearedDensity(self):
        sigma = .7
        # l = 0: a normalized Gaussian carrying the monopole
        M0 = mp.multipole_moments(np.zeros((1, 3)), np.array([1.3]), 0)
        pts = self.rng.normal(size=(10, 3))
        r2 = np.sum(pts ** 2, axis=-1)
        rho = mp.smeared_multipole_density(M0, pts, smearing=sigma)
        self.assertTrue(np.allclose(rho, 1.3 * np.exp(-r2 / (2 * sigma ** 2)) / (2 * np.pi * sigma ** 2) ** 1.5))
        # consistency with the smeared potential: -lap V / 4 pi = rho, all l
        L = 3
        real = self.rng.normal(size=(L + 1) ** 2)
        M = mp.real_spherical_to_multipoles(real)
        _, _, d2V = mp.multipole_potential(M, pts, smearing=sigma, deriv_order=2)
        self.assertTrue(np.allclose(-np.trace(d2V, axis1=-2, axis2=-1) / (4 * np.pi),
                                    mp.smeared_multipole_density(M, pts, smearing=sigma)))
        # the moments of the evaluated density are the input moments (grid quadrature)
        g = np.linspace(-6, 6, 61)
        grid = np.stack(np.meshgrid(g, g, g, indexing='ij'), axis=-1).reshape(-1, 3)
        dV = (g[1] - g[0]) ** 3
        rho = mp.smeared_multipole_density(M, grid, smearing=sigma) * dV
        self.assertTrue(np.allclose(rho @ mp.solid_harmonics(grid, L, real=True), real, atol=1e-6))

    # endregion


if __name__ == '__main__':
    unittest.main()

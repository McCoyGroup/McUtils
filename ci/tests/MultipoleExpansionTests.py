"""
Tests for `McUtils.Zachary.MultipoleExpansion`.
"""

import unittest

import numpy as np
import scipy.special

from McUtils.Zachary import MultipoleExpansion


def direct_potential(src, q, pts):
    d = pts[..., :, np.newaxis, :] - src[..., np.newaxis, :, :]
    return np.sum(q[..., np.newaxis, :] / np.linalg.norm(d, axis=-1), axis=-1)

def direct_field(src, q, pts):
    d = pts[:, None, :] - src[None, :, :]
    r = np.linalg.norm(d, axis=-1)
    return np.sum(q[None, :, None] * d / r[..., None] ** 3, axis=1)

def random_rotation(rng):
    Q, _ = np.linalg.qr(rng.normal(size=(3, 3)))
    return Q * np.sign(np.linalg.det(Q))


class MultipoleExpansionTests(unittest.TestCase):

    def setUp(self):
        self.rng = np.random.default_rng(7)
        self.src = self.rng.uniform(-.5, .5, (30, 3))
        self.q = self.rng.normal(size=30)
        far = self.rng.normal(size=(20, 3))
        self.far = 6 * far / np.linalg.norm(far, axis=-1)[:, None]

    def test_Evaluate(self):
        mp = MultipoleExpansion.from_charges(self.src, self.q, 12)
        self.assertEqual(mp.order, 12)
        self.assertEqual(mp.shape, ())
        self.assertTrue(np.allclose(mp(self.far), direct_potential(self.src, self.q, self.far)))
        self.assertTrue(np.allclose(mp.field(self.far), direct_field(self.src, self.q, self.far)))
        self.assertTrue(np.isclose(mp.charge, np.sum(self.q)))
        self.assertTrue(np.allclose(mp.dipole, self.q @ self.src))

    def test_ShiftAndTranslate(self):
        c = np.array([.2, -.1, .3])
        mp = MultipoleExpansion.from_charges(self.src, self.q, 8)
        shifted = mp.shift(c)
        ref = MultipoleExpansion.from_charges(self.src, self.q, 8, center=c)
        self.assertTrue(np.allclose(shifted.coefficients, ref.coefficients))
        self.assertTrue(np.allclose(shifted.center, c))
        d = np.array([1., 2., -1.])
        moved = MultipoleExpansion.from_charges(self.src, self.q, 12).translate(d)
        self.assertTrue(np.allclose(moved(self.far + d), direct_potential(self.src, self.q, self.far)))

    def test_Rotate(self):
        Q = random_rotation(self.rng)
        o = np.array([.4, .1, -.3])
        mp = MultipoleExpansion.from_charges(self.src, self.q, 12, center=np.array([.1, .1, .1]))
        rot = mp.rotate(Q, origin=o)
        moved = (self.src - o) @ Q.T + o
        pts = (self.far - o) @ Q.T + o
        self.assertTrue(np.allclose(rot(pts), direct_potential(moved, self.q, pts)))
        self.assertTrue(np.allclose(rot.center, (mp.center - o) @ Q.T + o))
        # about its own center
        rot_self = mp.rotate(Q)
        ref = MultipoleExpansion.from_charges((self.src - mp.center) @ Q.T + mp.center, self.q, 12, center=mp.center)
        self.assertTrue(np.allclose(rot_self.coefficients, ref.coefficients))

    def test_LocalExpansions(self):
        cL = np.array([5., 1., -2.])
        tgt = cL + self.rng.uniform(-.4, .4, (15, 3))
        mp = MultipoleExpansion.from_charges(self.src, self.q, 10)
        loc = mp.to_local(cL)
        self.assertEqual(loc.kind, 'local')
        exact = direct_potential(self.src, self.q, tgt)
        self.assertLess(np.max(np.abs(loc(tgt) - exact)), 1e-6)
        loc2 = loc.shift(cL + .1)
        self.assertTrue(np.allclose(loc2(tgt), loc(tgt)))
        Q = random_rotation(self.rng)
        rot = loc.rotate(Q)
        self.assertTrue(np.allclose(rot((tgt - cL) @ Q.T + cL), loc(tgt)))

    def test_DistributedSites(self):
        # per-atom charges + dipoles, evaluated as a distributed expansion and as one summed expansion
        n = 6
        sites = self.rng.uniform(-1, 1, (n, 3))
        charges = self.rng.normal(size=n)
        dipoles = self.rng.normal(size=(n, 3)) * .2
        real = np.concatenate([charges[:, None], dipoles[:, [1, 2, 0]]], axis=-1)
        dist = MultipoleExpansion.from_real(real, center=sites)
        self.assertEqual(dist.shape, (n,))
        d = self.far[None, :, :] - sites[:, None, :]
        r = np.linalg.norm(d, axis=-1)
        exact = np.sum(charges[:, None] / r + np.einsum('ia,ina->in', dipoles, d) / r ** 3, axis=0)
        self.assertTrue(np.allclose(dist(self.far, sum_axis=0), exact))
        total = dist.sum(axis=0, center=np.zeros(3), order=10)
        self.assertTrue(np.allclose(total.charge, charges.sum()))
        self.assertTrue(np.allclose(total.dipole, dipoles.sum(0) + charges @ sites))
        far = self.far * 5
        d = far[None, :, :] - sites[:, None, :]
        r = np.linalg.norm(d, axis=-1)
        exact_far = np.sum(charges[:, None] / r + np.einsum('ia,ina->in', dipoles, d) / r ** 3, axis=0)
        self.assertLess(np.max(np.abs(total(far) - exact_far)), 1e-10)
        self.assertEqual(dist.sum(axis=0).order, 1)

    def test_BatchedSumAxis(self):
        nstruct, n = 3, 5
        sites = self.rng.uniform(-1, 1, (nstruct, n, 3))
        charges = self.rng.normal(size=(nstruct, n))
        dist = MultipoleExpansion(charges[..., None], center=sites)
        pts = self.rng.normal(size=(nstruct, 7, 3)) * 4
        V = dist(pts, sum_axis=1)
        self.assertEqual(V.shape, (nstruct, 7))
        for i in range(nstruct):
            self.assertTrue(np.allclose(V[i], direct_potential(sites[i], charges[i], pts[i])))

    def test_Smeared(self):
        sigma = np.array([.5, .8])
        sites = np.array([[0., 0., 0.], [1., .5, -.2]])
        charges = np.array([.7, -.4])
        dist = MultipoleExpansion.from_real(charges[:, None], center=sites, smearing=sigma)
        pts = self.rng.normal(size=(10, 3))
        r = np.linalg.norm(pts[None] - sites[:, None], axis=-1)
        exact = np.sum(charges[:, None] * scipy.special.erf(r / (np.sqrt(2) * sigma[:, None])) / r, axis=0)
        self.assertTrue(np.allclose(dist(pts, sum_axis=0), exact))
        self.assertTrue(np.allclose(dist.rotate(np.eye(3))(pts, sum_axis=0), exact))
        with self.assertRaises(ValueError):
            dist.shift(np.zeros(3))
        with self.assertRaises(ValueError):
            dist.sum()
        self.assertTrue(np.allclose(dist.modify(drop_smearing=True)(self.far * 10, sum_axis=0),
                                    dist(self.far * 10, sum_axis=0)))

    def test_InteractionEnergy(self):
        srcB = self.rng.uniform(-.5, .5, (20, 3)) + np.array([8., -3., 2.])
        qB = self.rng.normal(size=20)
        A = MultipoleExpansion.from_charges(self.src, self.q, 10)
        B = MultipoleExpansion.from_charges(srcB, qB, 10, center=np.array([8., -3., 2.]))
        exact = np.sum(qB * direct_potential(self.src, self.q, srcB))
        self.assertLess(abs(A.interaction_energy(B) - exact), 1e-8)

    def test_Arithmetic(self):
        a = MultipoleExpansion.from_charges(self.src[:15], self.q[:15], 10)
        b = MultipoleExpansion.from_charges(self.src[15:], self.q[15:], 6, center=np.array([.1, 0., 0.]))
        c = a + b
        self.assertEqual(c.order, 10)
        self.assertLess(np.max(np.abs(c(self.far) - direct_potential(self.src, self.q, self.far))), 1e-6)
        self.assertTrue(np.allclose((2 * a)(self.far), 2 * a(self.far)))
        self.assertTrue(np.allclose((a - a).coefficients, 0))
        trunc = a.truncate(2)
        self.assertEqual(trunc.order, 2)

    def test_Cartesian(self):
        mp = MultipoleExpansion.from_charges(self.src, self.q, 4)
        cart = mp.to_cartesian()
        back = MultipoleExpansion.from_cartesian(cart, convention='traceless')
        self.assertTrue(np.allclose(back.coefficients, mp.coefficients))
        self.assertTrue(np.allclose(cart[1], self.q @ self.src))

    def test_Indexing(self):
        sites = self.rng.uniform(-1, 1, (4, 3))
        dist = MultipoleExpansion(self.rng.normal(size=(4, 1)), center=sites, smearing=.5)
        sub = dist[1:3]
        self.assertEqual(sub.shape, (2,))
        self.assertTrue(np.allclose(sub.center, sites[1:3]))
        self.assertEqual(sub.smearing.shape, (2,))

    def test_Density(self):
        sigma = np.array([.5, .8])
        sites = np.array([[0., 0., 0.], [1., .5, -.2]])
        q = np.array([.7, -.4])
        dist = MultipoleExpansion.from_real(q[:, None], center=sites, smearing=sigma)
        pts = self.rng.normal(size=(10, 3))
        r2 = np.sum((pts[None] - sites[:, None]) ** 2, axis=-1)
        g = np.exp(-r2 / (2 * sigma[:, None] ** 2)) / (2 * np.pi * sigma[:, None] ** 2) ** 1.5
        self.assertTrue(np.allclose(dist.density(pts, sum_axis=0), q @ g))
        with self.assertRaises(ValueError):
            dist.modify(drop_smearing=True).density(pts)


if __name__ == '__main__':
    unittest.main()

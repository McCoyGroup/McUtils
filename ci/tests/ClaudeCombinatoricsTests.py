"""
Tests for the `Sequences.py` prime-factorization/prime-list fixes (originally
drafted as `claude_drafts/prime_factorize_fixes/{prime_factorize_fixes,prime_list_fix}.patch`)
against `McUtils.Combinatorics.Sequences`:

- `_prime_check`'s sqrt short-circuit, `prime_iter`'s restart-from-2 fix,
  `prime_factorize`'s early-exit-on-provable-primality and its
  ran-out-of-primes `ValueError` (committed as `1a1e03b1`).
- `prime_list`'s `None`-defaulted `base_primes`/`piter`, backed by
  module-level `default_base_prime_list`/`default_prime_iter`, replacing the
  old mutable-default-argument cache -- fixing the footgun where a custom
  `base_primes` without a matching `piter` was silently ignored in favor of
  the (unrelated) global cache. Applied locally (uncommitted at the time this
  file was written), with the globals named without a leading underscore and
  `prime_iter`'s own default seed also wired through `default_base_prime_list`,
  slightly different from the originally drafted patch text -- this file
  matches whatever is actually on disk, not the original patch.

This parallels `CombinatoricsTests.test_PrimeFactorization` in both style
(`Peeves.TestUtils`, `@validationTest`) and in reusing its random-batch
reconstruction approach, but is scoped specifically to what changed: each
fix gets its own direct regression test (including a timing assertion for
the two cases that used to hang), rather than only the general batch check.

One deliberate deviation from `CombinatoricsTests.setUp`: `np.VisibleDeprecationWarning`
was removed in numpy 2.0, so guarding that `filterwarnings` call keeps this
file running under either a pre- or post-2.0 numpy instead of failing at
import time on newer installs (this mirrors the same guard now also present
in `CombinatoricsTests.setUp`).
"""

import time
import warnings

import numpy as np

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Combinatorics import *
#TODO: get rid of dirty check
import McUtils.McUtils.Combinatorics.Sequences as _Sequences


class ClaudeCombinatoricsTests(TestCase):

    def setUp(self):
        np.seterr(all='raise')
        vdw = getattr(np, 'VisibleDeprecationWarning', None)
        if vdw is not None:
            warnings.filterwarnings('error', category=vdw)
        np.set_printoptions(linewidth=1e8)

    # region _prime_check / prime_iter

    @validationTest
    def test_PrimeCheckSqrtShortcut(self):
        """`_prime_check`'s sqrt-bounded loop must agree with brute-force
        divisibility against every supplied prime, for both prime and
        composite candidates, and regardless of where the true factor
        falls relative to sqrt(candidate)."""
        primes_seen = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        for candidate in range(4, 2000):
            expected = all(candidate % pp != 0 for pp in primes_seen if pp < candidate)
            got = _Sequences._prime_check(candidate, primes_seen)
            self.assertEquals(got, expected, msg="mismatch at candidate={}".format(candidate))

    @validationTest
    def test_PrimeIterRestartFromTwo(self):
        """`prime_iter(primes=[2])` used to raise `ValueError("math broke")`
        because `range(p+2, 2*p, 2)` is empty for `p == 2`; it must now
        continue correctly straight through the small primes."""
        it = prime_iter(primes=[2])
        seqs = [next(it) for _ in range(6)]
        self.assertEquals(seqs[-1], [2, 3, 5, 7, 11, 13])

    @validationTest
    def test_PrimeIterMatchesKnownPrimes(self):
        """`prime_iter()`'s default (2,3,5,7,11,13,17-seeded) sequence must
        match the true primes, cross-checked against a dependency-free
        brute-force sieve, well past the length of the seed list."""
        def is_prime(n):
            if n < 2:
                return False
            i = 2
            while i * i <= n:
                if n % i == 0:
                    return False
                i += 1
            return True

        true_primes = [n for n in range(2, 2000) if is_prime(n)]

        it = prime_iter()
        last = None
        for _ in range(len(true_primes)):
            last = next(it)
        self.assertEquals(last, true_primes)

    # endregion

    # region prime_factorize

    @validationTest
    def test_PrimeFactorizeLargePrimeIsFast(self):
        """Before the early-exit fix, factoring a single large prime never
        finished in practice (trial division kept generating candidate
        primes almost up to the value itself). It must now resolve almost
        immediately, and reconstruct correctly."""
        n = 100000007  # prime
        t0 = time.time()
        primes, counts = prime_factorize(n)
        dt = time.time() - t0
        self.assertLess(dt, 5, msg="prime_factorize(100000007) took {:.2f}s".format(dt))
        self.assertEquals(int(np.prod(primes ** np.array(counts))), n)

    @validationTest
    def test_PrimeFactorizeLargeSemiprimeIsFast(self):
        """Same early-exit fix, exercised on a product of two ~100,000-sized
        primes rather than a single bare large prime."""
        n = 100003 * 100019
        t0 = time.time()
        primes, counts = prime_factorize(n)
        dt = time.time() - t0
        self.assertLess(dt, 5, msg="prime_factorize({}) took {:.2f}s".format(n, dt))
        self.assertEquals(int(np.prod(primes ** np.array(counts))), n)
        nonzero = {int(p): int(c) for p, c in zip(primes, counts) if c > 0}
        self.assertEquals(nonzero, {100003: 1, 100019: 1})

    @validationTest
    def test_PrimeFactorizeInsufficientCustomPrimesRaises(self):
        """A custom, incomplete `primes=` sequence must raise instead of
        silently returning a wrong/partial factorization. 204 = 2**2 * 3 * 17
        needs 17, which is deliberately withheld here."""
        with self.assertRaises(ValueError):
            prime_factorize(204, primes=[2, 3, 5, 7])

    @validationTest
    def test_PrimeFactorizeEdgeCases(self):
        """Scalar edge cases, including the `sel`-becomes-empty-immediately
        path (bare `1`, and every-input-is-1) that a naive fix for the
        `max_its` bound could regress (it did, during development, before
        the `if len(sel) > 0:` guard was added)."""
        p0, c0 = prime_factorize(1)
        self.assertEquals(len(p0), 0)
        self.assertEquals(len(c0), 0)

        p1, c1 = prime_factorize(2)
        self.assertEquals(int(np.prod(p1 ** np.array(c1))), 2)

        p2, c2 = prime_factorize(13)
        self.assertEquals(int(np.prod(p2 ** np.array(c2))), 13)

        # a batch mixing already-resolved (<=1) entries with a large prime
        mix = np.array([1, 1, 100000007, 6])
        pm, cm = prime_factorize(mix)
        cm = np.array(cm)
        recon = np.prod(pm[:, None] ** cm, axis=0)
        self.assertEquals(recon.tolist(), mix.tolist())

    @validationTest
    def test_PrimeFactorizeRandomBatchReconstructs(self):
        """Parallels `CombinatoricsTests.test_PrimeFactorization`'s random
        batch construction/reconstruction check, run here specifically
        against the patched `prime_factorize` (same seed, same shape)."""
        plist = prime_list(20)
        np.random.seed(1232232)
        mod_pos = np.sort(np.random.choice(np.arange(20), (100, 3)), axis=1)
        res = np.random.randint(1, 4, size=(100, 3))
        ints = np.prod(np.array(plist)[mod_pos] ** res, axis=1, dtype=int)

        primes, facs = prime_factorize(ints)
        facs = np.array(facs)
        recon = np.prod(primes[:, None] ** facs, axis=0)
        self.assertEquals(recon.tolist(), ints.tolist())

    # endregion

    # region prime_list

    @validationTest
    def test_PrimeListDefaultCacheUnchanged(self):
        """The fully-default call (`piter=None`, `base_primes=None`) must
        still return correct primes and still share the module-level cache
        across calls, exactly as the old mutable-default-argument version did."""
        p20 = prime_list(20)
        self.assertEquals(
            p20,
            [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
        )
        p5_again = prime_list(5)
        self.assertEquals(p5_again, p20[:5])

    @validationTest
    def test_PrimeListCustomBaseUsesOwnSeed(self):
        """The footgun this patch fixes: supplying a custom `base_primes`
        without a matching `piter` must extend *that* list via a fresh
        `prime_iter(base_primes)`, not silently defer to the unrelated
        global cache -- and the global cache must be left untouched."""
        before = list(_Sequences.default_base_prime_list)

        custom = [2, 3, 5]
        out = prime_list(7, base_primes=custom)
        self.assertEquals(out, [2, 3, 5, 7, 11, 13, 17])
        # base_primes is extended (and possibly overshoots n by one, same as
        # the original cache-extension behavior) rather than left alone
        self.assertEquals(out, custom[:7])

        self.assertEquals(_Sequences.default_base_prime_list, before)

    @validationTest
    def test_PrimeListCustomPiterOnlyUsesFreshList(self):
        """Supplying only `piter` (no `base_primes`) must populate a fresh
        empty list, not the global cache."""
        before = list(_Sequences.default_base_prime_list)

        my_iter = prime_iter([2, 3, 5])
        out = prime_list(6, piter=my_iter)
        self.assertEquals(out, [2, 3, 5, 7, 11, 13])

        self.assertEquals(_Sequences.default_base_prime_list, before)

    @validationTest
    def test_PrimeListExplicitBothMutatesGivenList(self):
        """Supplying both `base_primes` and a matching `piter` explicitly
        must use them exactly as given, mutating the caller's own list object."""
        my_list = [2, 3]
        my_iter = prime_iter(my_list)
        out = prime_list(5, base_primes=my_list, piter=my_iter)
        self.assertEquals(out, [2, 3, 5, 7, 11])
        self.assertEquals(out, my_list[:5])

    @validationTest
    def test_PrimeListIndependentCustomCachesDontInterfere(self):
        """Two separate custom `base_primes` caches must extend independently
        of each other and of the global default cache."""
        before = list(_Sequences.default_base_prime_list)

        cache_a = [2, 3]
        cache_b = [2, 3, 5, 7]
        result_a = prime_list(4, base_primes=cache_a)
        result_b = prime_list(4, base_primes=cache_b)

        self.assertEquals(result_a, [2, 3, 5, 7])
        self.assertEquals(result_b, [2, 3, 5, 7])
        self.assertEquals(_Sequences.default_base_prime_list, before)

    @validationTest
    def test_HaltonSequenceStillWorks(self):
        """`halton_sequence` is the one in-repo consumer of `prime_list`'s
        default (no-argument) path; it must still produce finite,
        correctly-shaped output after the `prime_list` rewrite."""
        h = halton_sequence(5, 3)
        self.assertEquals(h.shape, (5, 3))
        self.assertEquals(bool(np.all(np.isfinite(h))), True)

    # endregion

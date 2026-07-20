"""
Sequences lifted from finite difference weight calculation in
ZachLib to serve more general purposes
"""
import numpy as np, math
import functools
__all__ = ['StirlingS1', 'Binomial', 'GammaBinomial', 'Factorial', 'prime_sieve', 'prime_factorize', 'prime_iter', 'prime_list', 'stable_factorial_ratio', 'halton_sequence', 'sobol_sequence']

def StirlingS1(n):
    """Computes the Stirling numbers

    :param n:
    :type n:
    :return:
    :rtype:
    """
    ...

def Binomial(n, dtype=None):
    """
    Fast recursion to calculate all
    binomial coefficients up to binom(n, n)

    :param n:
    :type n:
    :return:
    :rtype:
    """
    ...

def GammaBinomial(s, n):
    """Generalized binomial gamma function

    :param s:
    :type s:
    :param n:
    :type n:
    :return:
    :rtype:
    """
    ...

def Factorial(n):
    """I was hoping to do this in some built in way with numpy...but I guess it's not possible?
    looks like by default things don't vectorize and just call math.factorial

    :param n:
    :type n:
    :return:
    :rtype:
    """
    ...

def _sieve_core(ints, k, max_its):
    """
    **LLM Docstring**

    Repeatedly divide selected integers by a candidate factor and count its multiplicity.

    The input array is modified in place. At each iteration, only entries still divisible by `k` remain selected, so `counts[i]` records how many factors of `k` were removed from `ints[i]`, up to `max_its`.

    :param ints: flattened integer values to reduce in place
    :type ints: numpy.ndarray
    :param k: candidate factor to remove
    :type k: int
    :param max_its: maximum number of division passes
    :type max_its: int
    :return: the reduced integer array and the per-entry factor counts
    :rtype: tuple[numpy.ndarray, numpy.ndarray]
    """
    ...

def prime_sieve(ints, k, max_its=None):
    """
    **LLM Docstring**

    Remove repeated factors of `k` from one or more integers.

    Scalar inputs are temporarily promoted to length-one arrays and converted back before returning. When `max_its` is omitted, the function derives an upper bound from `log(max(ints)) / log(k)`.

    :param ints: scalar or array of integers to factor by `k`
    :type ints: int | array-like
    :param k: factor to divide out repeatedly
    :type k: int
    :param max_its: optional cap on the number of divisions
    :type max_its: int | None
    :return: a pair containing the residual integers and multiplicities of `k`, with the input shape preserved
    :rtype: tuple[int | numpy.ndarray, int | numpy.ndarray]
    """
    ...

def _prime_check(p2, prev_primes):
    """
    **LLM Docstring**

    Test whether a candidate is indivisible by all supplied prior primes.

    :param p2: candidate integer
    :type p2: int
    :param prev_primes: previously generated prime divisors to test
    :type prev_primes: iterable[int]
    :return: `True` when no supplied prime divides `p2`
    :rtype: bool
    """
    ...

def prime_iter(primes=None):
    """
    **LLM Docstring**

    Yield progressively longer lists of prime numbers.

    The generator first yields prefixes of the provided seed list. It then searches odd candidates between the current largest prime and twice that value, accepting the first candidate not divisible by the existing primes other than `2`. Each yield is the full prime list accumulated so far.

    :param primes: optional initial ordered prime sequence
    :type primes: iterable[int] | None
    :return: an iterator yielding cumulative prime lists
    :rtype: collections.abc.Iterator[list[int]]
    """
    ...

def prime_list(n, base_primes=[], piter=prime_iter()):
    """
    **LLM Docstring**

    Return the first `n` primes using a shared incremental cache.

    The default `base_primes` list and `piter` generator are intentionally persistent across calls. The cache is extended until the iterator yields more than `n` entries, then the first `n` values are returned.

    :param n: number of primes requested
    :type n: int
    :param base_primes: mutable cache populated in place
    :type base_primes: list[int]
    :param piter: cumulative prime-list iterator used to extend the cache
    :type piter: collections.abc.Iterator[list[int]]
    :return: the first `n` cached primes
    :rtype: list[int]
    """
    ...

def prime_factorize(ints, primes=None):
    """
    **LLM Docstring**

    Compute prime-exponent arrays for one or more positive integers.

    The function repeatedly applies `_sieve_core` to entries whose residual value exceeds `1`. It accepts either an iterator of individual primes or an iterator of cumulative prime lists, as produced by `prime_iter`. The returned count list contains one array per tested prime and preserves the original input shape.

    :param ints: positive integer scalar or array to factor
    :type ints: int | array-like
    :param primes: optional prime or cumulative-prime iterator
    :type primes: iterable[int | list[int]] | None
    :return: the generated prime array and a list of exponent arrays for those primes
    :rtype: tuple[numpy.ndarray, list[int | numpy.ndarray]]
    """
    ...

def stable_factorial_ratio(num_terms, denom_terms, counts=None):
    """
    **LLM Docstring**

    Evaluate a ratio of products using prime exponents.

    Without precomputed `counts`, numerator and denominator terms are deduplicated, factorized, and weighted by their multiplicities. The two prime-count vectors are padded to equal length, subtracted, and exponentiated. Negative exponents trigger floating-point evaluation. Despite its name, the inputs are treated as explicit multiplicative terms rather than factorial arguments.

    :param num_terms: factors in the numerator
    :type num_terms: array-like
    :param denom_terms: factors in the denominator
    :type denom_terms: array-like
    :param counts: optional pair of precomputed numerator and denominator prime-exponent arrays; when supplied, `num_terms` and `denom_terms` are treated as the corresponding prime lists
    :type counts: tuple[array-like, array-like] | None
    :return: product of the aligned primes raised to the net exponent vector
    :rtype: int | float | numpy.number
    """
    ...
'\nHalton and Sobol low-discrepancy sequences, pure numpy/scipy.\n\nHalton needs no external data beyond a list of primes. Sobol needs a table\nof primitive polynomials (mod 2) and initial direction numbers -- there is\nno way to derive these at runtime, they come from an offline search (Joe &\nKuo; originally Bratley & Fox). The table below is the classic Bratley-Fox\n/ Numerical-Recipes table (dimensions 1-40), the same one used by John\nBurkardt\'s public-domain reference implementation. The *data* is that\npublished table; the generation algorithm here (direction-number\nrecurrence + Gray-code point formula) is my own vectorized implementation,\nvalidated against Burkardt\'s reference output bit-for-bit (see __main__).\n\nReferences\n----------\nP. Bratley and B.L. Fox, "Algorithm 659: Implementing Sobol\'s Quasirandom\nSequence Generator", ACM TOMS 14 (1988).\nI.M. Sobol\', "The distribution of points in a cube and the approximate\nevaluation of integrals", Zh. Vych. Mat. Mat. Fiz. 7 (1967).\nJ.H. Halton, "On the efficiency of certain quasi-random sequences of\npoints in evaluating multi-dimensional integrals", Numer. Math. 2 (1960).\n'

def _van_der_corput(n, base):
    """
    Radical-inverse (van der Corput) sequence in the given base, vectorized
    over an integer array n. van_der_corput(n, 2) is the classic base-2
    bit-reversal sequence.
    """
    ...

@functools.lru_cache(maxsize=100)
def halton_sequence(N, d, start=1):
    """
    First N points of the d-dimensional Halton sequence, one prime base
    per dimension (2, 3, 5, 7, 11, ...). `start` skips the first `start`
    indices (default 1, to skip the degenerate all-zero point at index 0).
    """
    ...
_DIM_MAX = 40

def _degree(poly_code):
    """Degree m of the primitive polynomial from its encoded middle bits."""
    ...

def _direction_numbers(dim_num, n_bits=30):
    """
    Build the (dim_num, n_bits) integer direction-number matrix V, following
    the classic Bratley-Fox recurrence:

        v_j = 2 a_1 v_{j-1} XOR 2^2 a_2 v_{j-2} XOR ... XOR 2^{m-1} a_{m-1} v_{j-m+1}
              XOR 2^m v_{j-m} XOR v_{j-m}

    for j > m, where m is the polynomial degree and a_1..a_{m-1} are its
    middle coefficients. Row 0 (dimension 1) is trivial: it just reproduces
    the base-2 van der Corput sequence. Returned columns are pre-scaled by
    the appropriate power of two so that V / 2**n_bits gives values in [0,1).
    """
    ...

@functools.lru_cache(maxsize=100)
def sobol_sequence(N, d, n_bits=30):
    """
    First N points of the d-dimensional Sobol sequence (Bratley-Fox
    direction numbers), via the direct formula

        x_n = XOR_{c : bit c of gray(n+1) is set} V[:, c]     (n = 0..N-1)

    where gray(k) = k XOR (k >> 1). This 0-indexed convention matches the
    classic Fortran/MATLAB/Python reference implementations (Burkardt et
    al.) exactly -- validated against that reference in __main__ below.
    """
    ...
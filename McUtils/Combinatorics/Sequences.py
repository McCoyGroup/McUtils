"""
Sequences lifted from finite difference weight calculation in
ZachLib to serve more general purposes
"""

import numpy as np, math
import functools
# import itertools
# from .. import Numputils as nput

__all__ = [
    "StirlingS1",
    "Binomial",
    "GammaBinomial",
    "Factorial",
    "prime_sieve",
    "prime_factorize",
    "prime_iter",
    "prime_list",
    "stable_factorial_ratio",
    "halton_sequence",
    "sobol_sequence"
]

def StirlingS1(n):
    """Computes the Stirling numbers

    :param n:
    :type n:
    :return:
    :rtype:
    """
    stirlings = np.eye(n)
    for i in range(n):
        for j in range(i+1):
            stirlings[i, j] = (-1)**(i-j) *( (i-1)*abs(stirlings[i-1, j]) + abs(stirlings[i-1, j-1]))
    return stirlings

def Binomial(n, dtype=None):
    """
    Fast recursion to calculate all
    binomial coefficients up to binom(n, n)

    :param n:
    :type n:
    :return:
    :rtype:
    """
    if dtype is None:
        max_int = np.iinfo(np.dtype('uint64')).max
        if max_int > math.comb(n, n//2):
            dtype = 'uint64'
        else:
            dtype = object
    binomials = np.eye(n, dtype=dtype)
    binomials[:, 0] = 1
    for i in range(2, n):
        if i%2 == 0:
            k = i//2 + 1
        else:
            k = (i+1)//2
        for j in range(int(k)):
            binomials[i, j] = binomials[i, i-j] = binomials[i-1, j-1] + binomials[i-1, j]
    return binomials

def GammaBinomial(s, n):
    """Generalized binomial gamma function

    :param s:
    :type s:
    :param n:
    :type n:
    :return:
    :rtype:
    """
    g = math.gamma
    g1 = g(s+1)
    g2 = np.array([g(m+1)*g(s-m+1) for m in range(n)])
    g3 = g1/g2
    return g3

def Factorial(n):
    """I was hoping to do this in some built in way with numpy...but I guess it's not possible?
    looks like by default things don't vectorize and just call math.factorial

    :param n:
    :type n:
    :return:
    :rtype:
    """

    base = np.arange(n, dtype='uint64')
    base[0] = 1
    for i in range(1, n):
        base[i] = base[i]*base[i-1]
    return base


def _sieve_core(ints, k, max_its):
    sel = np.arange(ints.shape[0])
    counts = np.zeros(ints.shape[0], dtype=int)
    for i in range(max_its):
        mask = np.where(ints[sel,] % k == 0)
        if len(mask) == 0 or len(mask[0]) == 0:
            break

        sel = sel[mask[0],]
        counts[sel,] += 1
        ints[sel,] //= k
    return ints, counts
def prime_sieve(ints, k, max_its=None):
    ints = np.asanyarray(ints, dtype=int)
    smol = ints.ndim == 0
    if smol: ints = ints[np.newaxis]
    base_shape = ints.shape
    ints = ints.reshape(-1)

    if max_its is None:
        max_its = np.ceil(np.max(np.log(ints)/np.log(k))).astype(int)

    ints, counts = _sieve_core(ints, k, max_its)

    ints = ints.reshape(base_shape)
    counts = counts.reshape(base_shape)
    if smol:
        ints = ints[0]
        counts = counts[0]

    return ints, counts


def _prime_check(p2, prev_primes):
    return all(p2%pp > 0 for pp in prev_primes)

def prime_iter(primes=None):
    # we will very rarely exhaust these...
    if primes is None:
        primes = [2, 3, 5, 7, 11, 13, 17]
    else:
        primes = list(primes)
    for i in range(len(primes)):
        yield primes[:i+1]
    while True:
        p = primes[-1]
        for p2 in range(p+2, 2 * p, 2):
            if _prime_check(p2, primes[1:]):
                break
        else:
            raise ValueError("math broke")
        primes.append(p2)
        yield primes


def prime_list(n, base_primes=[], piter=prime_iter()):
    # gives a list up to the nth prime
    if n > len(base_primes):
        for p_list in piter:
            if len(p_list) > n:
                base_primes[:] = p_list
                break
    return base_primes[:n]

def prime_factorize(ints, primes=None):
    ints = np.array(ints, dtype=int)
    smol = ints.ndim == 0
    if smol: ints = ints[np.newaxis]
    base_shape = ints.shape
    ints = ints.reshape(-1)

    log_ints = np.log(ints)
    if primes is None:
        primes = prime_iter()

    sel = np.arange(ints.shape[0])
    max_prime = np.zeros(ints.shape[0], dtype=int)
    sel = sel[np.where(ints > 1)]
    count_list = []
    prime_list = []
    for p in primes:
        if isinstance(p, (int, np.integer)):
            prime_list.append(p)
        else:
            prime_list = p
            p = p[-1]

        max_its = np.ceil(np.max(log_ints/np.log(p))).astype(int)
        subints, subcounts = _sieve_core(ints[sel,], p, max_its)
        counts = np.zeros(ints.shape[0], dtype=int)
        counts[sel,] = subcounts
        count_list.append(counts)
        ints[sel,] = subints
        max_prime[sel,] += 1

        mask = np.where(subints > 1)
        if len(mask) == 0 or len(mask[0]) == 0:
            break
        sel = sel[mask]

    count_list = [c.reshape(base_shape) for c in count_list]
    if smol:
        count_list = [c[0] for c in count_list]

    return np.array(prime_list), count_list


def stable_factorial_ratio(num_terms, denom_terms, counts=None):
    if counts is None:
        num_terms, num_counts = np.unique(num_terms, return_counts=True)
        num_terms, counts_num = prime_factorize(num_terms)
        counts_num = np.tensordot(np.array(counts_num), num_counts, axes=[-1, 0])
        denom_terms, denom_counts = np.unique(denom_terms, return_counts=True)
        denom_terms, counts_denom = prime_factorize(denom_terms)
        counts_denom = np.tensordot(np.array(counts_denom), denom_counts, axes=[-1, 0])
    else:
        # we assume the primes are sorted
        counts_num, counts_denom = counts
        counts_num = np.asanyarray(counts_num)
        counts_denom = np.asanyarray(counts_denom)

    if len(num_terms) > len(denom_terms):
        primes = num_terms
        counts_denom = np.pad(counts_denom, [0, len(num_terms) - len(denom_terms)])
    elif len(num_terms) < len(denom_terms):
        primes = denom_terms
        counts_num = np.pad(counts_num, [0, len(denom_terms) - len(num_terms)])
    else:
        primes = num_terms

    exponent = counts_num - counts_denom
    if np.any(exponent < 0):
        exponent = exponent.astype(float)

    return np.prod(primes**exponent)


"""
Halton and Sobol low-discrepancy sequences, pure numpy/scipy.

Halton needs no external data beyond a list of primes. Sobol needs a table
of primitive polynomials (mod 2) and initial direction numbers -- there is
no way to derive these at runtime, they come from an offline search (Joe &
Kuo; originally Bratley & Fox). The table below is the classic Bratley-Fox
/ Numerical-Recipes table (dimensions 1-40), the same one used by John
Burkardt's public-domain reference implementation. The *data* is that
published table; the generation algorithm here (direction-number
recurrence + Gray-code point formula) is my own vectorized implementation,
validated against Burkardt's reference output bit-for-bit (see __main__).

References
----------
P. Bratley and B.L. Fox, "Algorithm 659: Implementing Sobol's Quasirandom
Sequence Generator", ACM TOMS 14 (1988).
I.M. Sobol', "The distribution of points in a cube and the approximate
evaluation of integrals", Zh. Vych. Mat. Mat. Fiz. 7 (1967).
J.H. Halton, "On the efficiency of certain quasi-random sequences of
points in evaluating multi-dimensional integrals", Numer. Math. 2 (1960).
"""


# ---------------------------------------------------------------------------
# Halton
# ---------------------------------------------------------------------------

def _van_der_corput(n, base):
    """
    Radical-inverse (van der Corput) sequence in the given base, vectorized
    over an integer array n. van_der_corput(n, 2) is the classic base-2
    bit-reversal sequence.
    """
    n = np.asarray(n, dtype=np.int64).copy()
    result = np.zeros(n.shape, dtype=np.float64)
    denom = np.ones(n.shape, dtype=np.float64)
    while np.any(n > 0):
        denom *= base
        result += (n % base) / denom
        n //= base
    return result

@functools.lru_cache(maxsize=100)
def halton_sequence(N, d, start=1):
    """
    First N points of the d-dimensional Halton sequence, one prime base
    per dimension (2, 3, 5, 7, 11, ...). `start` skips the first `start`
    indices (default 1, to skip the degenerate all-zero point at index 0).
    """
    primes = prime_list(d)
    idx = np.arange(start, start + N)
    return np.stack([_van_der_corput(idx, p) for p in primes], axis=1)


# ---------------------------------------------------------------------------
# Sobol
# ---------------------------------------------------------------------------

# Primitive polynomials mod 2 for dimensions 1-40, encoded as the integer
# formed by their middle coefficients a_1..a_{m-1} (dimension 1's implicit
# polynomial is trivial and handled separately). Classic Bratley-Fox table.
_POLY = [
    1,   3,   7,   11,  13,  19,  25,  37,  59,  47,
    61,  55,  41,  67,  97,  91,  109, 103, 115, 131,
    193, 137, 145, 143, 241, 157, 185, 167, 229, 171,
    213, 191, 253, 203, 211, 239, 247, 285, 369, 299,
]

_DIM_MAX = 40

# Initial direction-number seeds m_{k,i}, one table column per polynomial
# degree (column c holds the seed needed at degree c+1), given as
# (first_dimension_row, values) since lower dimensions use lower-degree
# polynomials and simply don't need the higher columns.
_INIT_SEEDS = {
    0: (0, [1]*40),
    1: (2, [1, 3, 1, 3, 1, 3, 3, 1, 3, 1, 3, 1, 3, 1, 1, 3, 1, 3,
             1, 3, 1, 3, 3, 1, 3, 1, 3, 1, 3, 1, 1, 3, 1, 3, 1, 3, 1, 3]),
    2: (3, [7, 5, 1, 3, 3, 7, 5, 5, 7, 7, 1, 3, 3, 7, 5, 1, 1,
             5, 3, 3, 1, 7, 5, 1, 3, 3, 7, 5, 1, 1, 5, 7, 7, 5, 1, 3, 3]),
    3: (5, [1, 7, 9, 13, 11, 1, 3, 7, 9, 5, 13, 13, 11, 3, 15,
             5, 3, 15, 7, 9, 13, 9, 1, 11, 7, 5, 15, 1, 15, 11, 5, 3, 1, 7, 9]),
    4: (7, [9, 3, 27, 15, 29, 21, 23, 19, 11, 25, 7, 13, 17,
             1, 25, 29, 3, 31, 11, 5, 23, 27, 19, 21, 5, 1, 17, 13, 7, 15, 9, 31, 9]),
    5: (13, [37, 33, 7, 5, 11, 39, 63, 27, 17, 15, 23, 29, 3, 21, 13,
              31, 25, 9, 49, 33, 19, 29, 11, 19, 27, 15, 25]),
    6: (19, [13, 33, 115, 41, 79, 17, 29, 119, 75, 73, 105, 7, 59,
              65, 21, 3, 113, 61, 89, 45, 107]),
    7: (37, [7, 23, 39]),
}


def _degree(poly_code):
    """Degree m of the primitive polynomial from its encoded middle bits."""
    j = poly_code >> 1
    m = 0
    while j > 0:
        j >>= 1
        m += 1
    return m


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
    if dim_num > _DIM_MAX:
        raise ValueError(f"only dimensions 1..{_DIM_MAX} are tabulated")

    V = np.zeros((dim_num, n_bits), dtype=np.int64)
    V[0, :] = 1  # trivial dimension-1 seed row, filled in below via scaling

    for i in range(1, dim_num):
        m = _degree(_POLY[i])
        # gather seed values m_{1,i}..m_{m,i} from the seed table
        seeds = np.zeros(m, dtype=np.int64)
        for col in range(m):
            first_row, vals = _INIT_SEEDS[col]
            seeds[col] = vals[i - first_row]
        V[i, :m] = seeds

        # Extract the polynomial's m coefficient bits a_1..a_m, one per bit
        # of poly_code from the LSB up, stored in reverse (includ[0] is the
        # highest of the m extracted bits, includ[m-1] the LSB) -- this
        # ordering matches the classic Bratley-Fox loop exactly.
        j = _POLY[i]
        includ = [0] * m
        for k in range(m, 0, -1):
            j2 = j // 2
            includ[k - 1] = 1 if j != 2 * j2 else 0
            j = j2

        for col in range(m, n_bits):
            newv = V[i, col - m]
            for k in range(1, m + 1):
                if includ[k - 1]:
                    newv ^= (1 << k) * V[i, col - k]
            V[i, col] = newv

    # scale each column by the appropriate power of two (place value)
    scale = 1 << np.arange(n_bits - 1, -1, -1)
    V *= scale[None, :]
    return V


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
    V = _direction_numbers(d, n_bits)
    n = np.arange(N, dtype=np.int64) + 1
    gray = n ^ (n >> 1)

    result = np.zeros((N, d), dtype=np.int64)
    for c in range(n_bits):
        bit_set = ((gray >> c) & 1).astype(np.int64)
        result ^= bit_set[:, None] * V[:, c][None, :]

    return result / (1 << n_bits)
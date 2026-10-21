"""
Spherical multipole expansions built on complex solid harmonics.

Conventions
-----------
Regular and irregular solid harmonics are normalized so that every
addition theorem is prefactor-free (the "Racah-like" convention used in
the fast-multipole literature, e.g. W. Dehnen, Comput. Astrophys. Cosmol. 1, 1 (2014)):

    R_lm(r) = r^l     P_l^m(cos t) e^{i m p} / (l+m)!
    I_lm(r) = (l-m)!  P_l^m(cos t) e^{i m p} / r^{l+1}

with the Condon-Shortley phase inside `P_l^m`. Both satisfy
`X_{l,-m} = (-1)^m conj(X_lm)`, so only `m >= 0` is stored, in the *packed*
layout `index(l, m) = l(l+1)/2 + m`, i.e. `(L+1)(L+2)/2` complex values per
expansion (equivalent to `(L+1)^2` real numbers).

With charges `q_i` at `x_i` and an expansion center `c`

    multipole moments   M_lm = sum_i q_i R_lm(x_i - c)
    potential (far)     V(r) = sum_{l,|m|<=l} conj(M_lm) I_lm(r - c)
    local coefficients  F_lm = sum_i q_i I_lm(x_i - c)
    potential (near)    V(r) = sum_{l,|m|<=l} F_lm conj(R_lm(r - c))

Real coefficients (`real=True`, `real_spherical_to_multipoles`, ...) use the standard real
solid harmonics with Racah normalization, `S_lm = r^l sqrt(4 pi/(2l+1)) Y^real_lm`, ordered
`m = -l..l` within each `l`, with `Y^real_{l,m>0} = sqrt(2) (-1)^m Re Y_lm` and
`Y^real_{l,-m} = sqrt(2) (-1)^m Im Y_lm`. For `l = 1` this is `(y, z, x)`. It is the convention of
`e3nn` (applied to `(y, z, x)`-permuted inputs, as `graph_longrange`/MACE-POLAR do), so MACE-POLAR
`density_coefficients` are exactly real multipole moments in this layout.

All functions broadcast over arbitrary leading axes. Points are `(..., N, 3)`,
charges `(..., N)`, centers/shifts `(..., 3)`, expansions `(..., P)`.

Every operation is a short `O(L)` Python loop of vectorized recurrences or a
cached integer gather followed by a single `einsum`, so cost is dominated by
BLAS-level work over the batch axes.
"""

import functools
import itertools
import math

import numpy as np
import scipy.special

from .VectorOps import vec_dots
from .Lebedev import lebedev_grid, _LEBEDEV_DEGREES

__all__ = [
    "solid_harmonics",
    "multipole_moments",
    "multipole_potential",
    "translate_multipoles",
    "multipoles_to_local_multipoles",
    "local_multipole_expansion",
    "translate_local_multipoles",
    "local_multipole_potential",
    "cartesian_multipole_moments",
    "cartesian_to_spherical_multipoles",
    "spherical_to_cartesian_multipoles",
    "multipole_expansion_order",
    "multipole_rotation_matrices",
    "rotate_multipoles",
    "rotate_local_multipoles",
    "real_spherical_to_multipoles",
    "multipoles_to_real_spherical",
    "smeared_multipole_density",
]


# ---------------------------------------------------------------------------
# layout helpers

def _packed_size(L):
    return (L + 1) * (L + 2) // 2

def _full_size(L):
    return (L + 1) ** 2

def _pidx(l, m):
    return l * (l + 1) // 2 + m

def _fidx(l, m):
    return l * l + l + m

def multipole_expansion_order(expansion):
    """
    Infers the order `L` of a packed expansion from its trailing dimension.

    :param expansion: packed expansion (or its trailing size as an `int`)
    :type expansion: np.ndarray | int
    :return: the expansion order
    :rtype: int
    """
    P = expansion if isinstance(expansion, (int, np.integer)) else np.shape(expansion)[-1]
    L = int(round((math.sqrt(8 * P + 1) - 3) / 2))
    if _packed_size(L) != P:
        raise ValueError(f"trailing dimension {P} is not a packed (L+1)(L+2)/2 expansion size")
    return L

@functools.lru_cache(maxsize=None)
def _packed_lm(L):
    l = np.concatenate([np.full(l + 1, l) for l in range(L + 1)])
    m = np.concatenate([np.arange(l + 1) for l in range(L + 1)])
    return l, m

@functools.lru_cache(maxsize=None)
def _real_weights(L):
    # sum over m=-l..l of X_{l,-m} Y_{l,-m} = conj(X_lm Y_lm) for the products used here
    _, m = _packed_lm(L)
    return np.where(m == 0, 1., 2.)

@functools.lru_cache(maxsize=None)
def _full_spec(L):
    src = []
    neg = []
    sign = []
    for l in range(L + 1):
        for m in range(-l, l + 1):
            src.append(_pidx(l, abs(m)))
            neg.append(m < 0)
            sign.append(-1 if (m < 0 and m % 2 == 1) else 1)
    return np.array(src), np.array(neg), np.array(sign)

def _to_full(packed, L, pad=False):
    """packed (..., P) -> full (..., (L+1)^2 [+1 zero pad slot]), index l^2 + l + m"""
    src, neg, sign = _full_spec(L)
    v = packed[..., src]
    v = np.where(neg, sign * np.conj(v), v)
    if pad:
        v = np.concatenate([v, np.zeros(v.shape[:-1] + (1,), dtype=v.dtype)], axis=-1)
    return v

def _pad_packed(packed, L_target):
    P = _packed_size(L_target)
    n = packed.shape[-1]
    if n == P:
        return packed
    if n > P:
        return packed[..., :P]
    out = np.zeros(packed.shape[:-1] + (P,), dtype=packed.dtype)
    out[..., :n] = packed
    return out

@functools.lru_cache(maxsize=None)
def _real_spec(L, kind):
    """
    index/scale data for packed complex (m >= 0) <-> real (m = -l..l) conversion;
    `scale` maps the packed complex values onto Racah-normalized complex values
    (`sqrt((l+m)!(l-m)!)` for regular, its inverse for irregular)
    """
    src = []
    part = []  # 0: m == 0 (real), 1: Re, 2: Im
    coef = []
    for l in range(L + 1):
        for m in range(-l, l + 1):
            am = abs(m)
            f = math.sqrt(math.factorial(l + am) * math.factorial(l - am))
            f = f if kind == 'regular' else 1 / f
            src.append(_pidx(l, am))
            if m == 0:
                part.append(0); coef.append(f)
            else:
                part.append(2 if m < 0 else 1); coef.append(math.sqrt(2) * (-1) ** am * f)
    return np.array(src), np.array(part), np.array(coef)

def _complex_to_real(packed, L, kind='regular'):
    src, part, coef = _real_spec(L, kind)
    v = packed[..., src]
    return coef * np.where(part == 2, v.imag, v.real)

def _real_to_complex(real, L, kind='regular'):
    real = np.asanyarray(real, dtype=float)
    out = np.zeros(real.shape[:-1] + (_packed_size(L),), dtype=complex)
    for l in range(L + 1):
        base = l * l + l
        for m in range(l + 1):
            f = math.sqrt(math.factorial(l + m) * math.factorial(l - m))
            f = f if kind == 'regular' else 1 / f
            if m == 0:
                out[..., _pidx(l, 0)] = real[..., base] / f
            else:
                out[..., _pidx(l, m)] = (
                        (-1) ** m * (real[..., base + m] + 1j * real[..., base - m])
                        / (math.sqrt(2) * f)
                )
    return out

@functools.lru_cache(maxsize=None)
def _reim_spec(L):
    # internal layout used by the Cartesian synthesis: [Re m=0, Re m=1, Im m=1, ..., Re m=l, Im m=l]
    src = []
    imag = []
    for l in range(L + 1):
        src.append(_pidx(l, 0)); imag.append(False)
        for m in range(1, l + 1):
            src.extend([_pidx(l, m), _pidx(l, m)])
            imag.extend([False, True])
    return np.array(src), np.array(imag)

def _to_reim_layout(packed, L):
    src, imag = _reim_spec(L)
    v = packed[..., src]
    return np.where(imag, v.imag, v.real)

def real_spherical_to_multipoles(coefficients):
    """
    Converts real Racah-normalized multipole moments (layout `m = -l..l` per `l`, see the module
    docstring; e.g. MACE-POLAR `density_coefficients`) to packed complex moments.

    :param coefficients: real moments, `(..., (L+1)^2)`
    :type coefficients: np.ndarray
    :return: packed complex moments, `(..., (L+1)(L+2)/2)`
    :rtype: np.ndarray
    """
    coefficients = np.asanyarray(coefficients)
    n = coefficients.shape[-1]
    L = int(round(math.sqrt(n))) - 1
    if (L + 1) ** 2 != n:
        raise ValueError(f"trailing dimension {n} is not a real (L+1)^2 expansion size")
    return _real_to_complex(coefficients, L)

def multipoles_to_real_spherical(moments):
    """
    Converts packed complex moments to real Racah-normalized moments
    (layout `m = -l..l` per `l`, see the module docstring).

    :param moments: packed complex moments, `(..., (L+1)(L+2)/2)`
    :type moments: np.ndarray
    :return: real moments, `(..., (L+1)^2)`
    :rtype: np.ndarray
    """
    moments = np.asanyarray(moments)
    return _complex_to_real(moments, multipole_expansion_order(moments))


# ---------------------------------------------------------------------------
# solid harmonics

def _split_coords(disp):
    disp = np.asanyarray(disp, dtype=float)
    if disp.shape[-1] != 3:
        raise ValueError(f"expected trailing dimension 3, got shape {disp.shape}")
    x = disp[..., 0]
    y = disp[..., 1]
    z = disp[..., 2]
    r2 = vec_dots(disp, disp)
    return x, y, z, np.reshape(r2, x.shape)

def _regular_harmonics(disp, L):
    x, y, z, r2 = _split_coords(disp)
    out = np.empty(x.shape + (_packed_size(L),), dtype=complex)
    out[..., 0] = 1.
    rp = x + 1j * y
    zc = z[..., np.newaxis]
    r2c = r2[..., np.newaxis]
    for l in range(1, L + 1):
        s0 = _pidx(l, 0)
        p1 = _pidx(l - 1, 0)
        # m = 0 .. l-1 from l-1 (and l-2 for m <= l-2)
        m = np.arange(l)
        term = (2 * l - 1) * zc * out[..., p1:p1 + l]
        if l > 1:
            p2 = _pidx(l - 2, 0)
            term[..., :l - 1] -= r2c * out[..., p2:p2 + l - 1]
        out[..., s0:s0 + l] = term / ((l + m) * (l - m))
        # diagonal
        out[..., s0 + l] = (-rp / (2 * l)) * out[..., p1 + l - 1]
    return out

def _irregular_harmonics(disp, L):
    x, y, z, r2 = _split_coords(disp)
    inv_r2 = 1 / r2
    out = np.empty(x.shape + (_packed_size(L),), dtype=complex)
    out[..., 0] = np.sqrt(inv_r2)
    rp = (x + 1j * y) * inv_r2
    zc = (z * inv_r2)[..., np.newaxis]
    ir2c = inv_r2[..., np.newaxis]
    for l in range(1, L + 1):
        s0 = _pidx(l, 0)
        p1 = _pidx(l - 1, 0)
        m = np.arange(l)
        term = (2 * l - 1) * zc * out[..., p1:p1 + l]
        if l > 1:
            p2 = _pidx(l - 2, 0)
            mm = m[:l - 1]
            term[..., :l - 1] -= ((l - 1) ** 2 - mm ** 2) * ir2c * out[..., p2:p2 + l - 1]
        out[..., s0:s0 + l] = term
        out[..., s0 + l] = (-(2 * l - 1) * rp) * out[..., p1 + l - 1]
    return out

def _displace(pts, center):
    pts = np.asanyarray(pts, dtype=float)
    if center is None:
        return pts
    center = np.asanyarray(center, dtype=float)
    return pts - center[..., np.newaxis, :] if pts.ndim > 1 else pts - center

def solid_harmonics(pts, L, kind='regular', center=None, real=False):
    """
    Evaluates solid harmonics up to order `L` by stable recurrences
    (no trig functions, no Legendre polynomials).

    :param pts: points, `(..., 3)`
    :type pts: np.ndarray
    :param L: maximum order
    :type L: int
    :param kind: `'regular'` (`R_lm`) or `'irregular'` (`I_lm`)
    :type kind: str
    :param center: optional center subtracted from `pts` (`(..., 3)` broadcast against `(..., N, 3)`)
    :type center: np.ndarray | None
    :param real: if `True` return the real Racah-normalized solid harmonics, `(L+1)^2` values
        ordered `m = -l..l` per `l` (`r^l C^real_lm` / `C^real_lm / r^(l+1)`, see the module docstring)
        instead of the packed complex ones
    :type real: bool
    :return: `(..., (L+1)(L+2)/2)` complex or `(..., (L+1)^2)` real
    :rtype: np.ndarray
    """
    disp = _displace(pts, center)
    kind = kind.lower()
    if kind == 'regular':
        vals = _regular_harmonics(disp, L)
    elif kind == 'irregular':
        vals = _irregular_harmonics(disp, L)
    else:
        raise ValueError(f"unknown solid harmonic kind '{kind}'")
    if real:
        vals = _complex_to_real(vals, L, kind=kind)
    return vals


# ---------------------------------------------------------------------------
# point -> expansion

def _prep_charges(charges, disp):
    if charges is None:
        return np.ones(disp.shape[:-1])
    return np.asanyarray(charges, dtype=float)

def multipole_moments(pts, charges, L, center=None):
    """
    Spherical multipole moments `M_lm = sum_i q_i R_lm(x_i - c)` (P2M).

    :param pts: source positions, `(..., N, 3)`
    :type pts: np.ndarray
    :param charges: source charges, `(..., N)` (`None` for unit charges)
    :type charges: np.ndarray | None
    :param L: expansion order
    :type L: int
    :param center: expansion center, `(..., 3)` (origin if `None`)
    :type center: np.ndarray | None
    :return: packed moments, `(..., (L+1)(L+2)/2)`
    :rtype: np.ndarray
    """
    disp = _displace(pts, center)
    q = _prep_charges(charges, disp)
    R = _regular_harmonics(disp, L)
    return np.matmul(q[..., np.newaxis, :], R)[..., 0, :]

def local_multipole_expansion(pts, charges, L, center=None):
    """
    Local (inner) expansion coefficients `F_lm = sum_i q_i I_lm(x_i - c)` (P2L)
    for sources outside the sphere of evaluation.

    :param pts: source positions, `(..., N, 3)`
    :type pts: np.ndarray
    :param charges: source charges, `(..., N)` (`None` for unit charges)
    :type charges: np.ndarray | None
    :param L: expansion order
    :type L: int
    :param center: expansion center, `(..., 3)`
    :type center: np.ndarray | None
    :return: packed local coefficients, `(..., (L+1)(L+2)/2)`
    :rtype: np.ndarray
    """
    disp = _displace(pts, center)
    q = _prep_charges(charges, disp)
    I = _irregular_harmonics(disp, L)
    return np.matmul(q[..., np.newaxis, :], I)[..., 0, :]


# ---------------------------------------------------------------------------
# translations (one cached gather + one einsum each)

@functools.lru_cache(maxsize=None)
def _m2m_table(L):
    # M'_lm = sum_{l'm'} M_{l'm'} R_{l-l', m-m'}(b)
    pad = _full_size(L)
    tab = np.full((_packed_size(L), _full_size(L)), pad, dtype=int)
    for l in range(L + 1):
        for m in range(l + 1):
            row = _pidx(l, m)
            for lp in range(l + 1):
                dl = l - lp
                for mp in range(-lp, lp + 1):
                    dm = m - mp
                    if abs(dm) <= dl:
                        tab[row, _fidx(lp, mp)] = _fidx(dl, dm)
    return tab

@functools.lru_cache(maxsize=None)
def _m2l_table(Lm, Ll):
    # F_jk = (-1)^j sum_{lm} conj(M_lm) I_{l+j, m+k}(s)
    tab = np.empty((_packed_size(Ll), _full_size(Lm)), dtype=int)
    sign = np.empty(_packed_size(Ll))
    for j in range(Ll + 1):
        for k in range(j + 1):
            row = _pidx(j, k)
            sign[row] = (-1) ** j
            for l in range(Lm + 1):
                for m in range(-l, l + 1):
                    tab[row, _fidx(l, m)] = _fidx(l + j, m + k)
    return tab, sign

@functools.lru_cache(maxsize=None)
def _l2l_table(L):
    # F'_pq = sum_{jk} F_jk conj(R_{j-p, k-q}(t))
    pad = _full_size(L)
    tab = np.full((_packed_size(L), _full_size(L)), pad, dtype=int)
    for p in range(L + 1):
        for q in range(p + 1):
            row = _pidx(p, q)
            for j in range(p, L + 1):
                dl = j - p
                for k in range(-j, j + 1):
                    dk = k - q
                    if abs(dk) <= dl:
                        tab[row, _fidx(j, k)] = _fidx(dl, dk)
    return tab

def translate_multipoles(moments, shift):
    """
    Moves a multipole expansion from center `c` to `c + shift` (M2M).
    Exact for a truncated expansion (no new truncation error).

    :param moments: packed moments, `(..., P)`
    :type moments: np.ndarray
    :param shift: displacement of the new center from the old, `(..., 3)`
    :type shift: np.ndarray
    :return: packed moments about the new center
    :rtype: np.ndarray
    """
    moments = np.asanyarray(moments)
    L = multipole_expansion_order(moments)
    R = _to_full(_regular_harmonics(-np.asanyarray(shift, dtype=float), L), L, pad=True)
    T = R[..., _m2m_table(L)]
    return np.einsum('...pk,...k->...p', T, _to_full(moments, L))

def multipoles_to_local_multipoles(moments, shift, local_order=None):
    """
    Converts a multipole expansion about `c` into a local expansion about
    `c + shift` (M2L). Valid when all sources are well separated from the
    local expansion region.

    :param moments: packed moments, `(..., P)`
    :type moments: np.ndarray
    :param shift: displacement of the local center from the multipole center, `(..., 3)`
    :type shift: np.ndarray
    :param local_order: order of the local expansion (defaults to the multipole order)
    :type local_order: int | None
    :return: packed local coefficients
    :rtype: np.ndarray
    """
    moments = np.asanyarray(moments)
    Lm = multipole_expansion_order(moments)
    Ll = Lm if local_order is None else local_order
    tab, sign = _m2l_table(Lm, Ll)
    I = _to_full(_irregular_harmonics(np.asanyarray(shift, dtype=float), Lm + Ll), Lm + Ll)
    T = I[..., tab]
    return sign * np.einsum('...pk,...k->...p', T, np.conj(_to_full(moments, Lm)))

def translate_local_multipoles(local, shift):
    """
    Moves a local expansion from center `c` to `c + shift` (L2L).
    Exact for a truncated expansion.

    :param local: packed local coefficients, `(..., P)`
    :type local: np.ndarray
    :param shift: displacement of the new center from the old, `(..., 3)`
    :type shift: np.ndarray
    :return: packed local coefficients about the new center
    :rtype: np.ndarray
    """
    local = np.asanyarray(local)
    L = multipole_expansion_order(local)
    R = np.conj(_to_full(_regular_harmonics(np.asanyarray(shift, dtype=float), L), L, pad=True))
    T = R[..., _l2l_table(L)]
    return np.einsum('...pk,...k->...p', T, _to_full(local, L))


# ---------------------------------------------------------------------------
# derivatives: d/dx_a of an expansion is another expansion (pure index shifts)
#
#   multipole (I-side):  dx I_lm = (I_{l+1,m+1} - I_{l+1,m-1})/2
#                        dy I_lm = (I_{l+1,m+1} + I_{l+1,m-1})/(2i)
#                        dz I_lm = -I_{l+1,m}
#   local (R-side):      dx R_lm = (R_{l-1,m+1} - R_{l-1,m-1})/2
#                        dy R_lm = (R_{l-1,m+1} + R_{l-1,m-1})/(2i)
#                        dz R_lm = R_{l-1,m}

@functools.lru_cache(maxsize=None)
def _deriv_table(kind, axis, L_in):
    if kind == 'multipole':
        L_out = L_in + 1
        dl = -1
        terms = {
            0: [(-1, .5), (1, -.5)],
            1: [(-1, .5j), (1, .5j)],
            2: [(0, -1.)]
        }[axis]
    else:
        L_out = max(L_in - 1, 0)
        dl = 1
        terms = {
            0: [(-1, .5), (1, -.5)],
            1: [(-1, .5j), (1, .5j)],
            2: [(0, 1.)]
        }[axis]
    pad = _full_size(L_in)
    idx = np.full((_packed_size(L_out), len(terms)), pad, dtype=int)
    wts = np.zeros((_packed_size(L_out), len(terms)), dtype=complex)
    for l in range(L_out + 1):
        ls = l + dl
        if ls < 0 or ls > L_in:
            continue
        for m in range(l + 1):
            for t, (dm, w) in enumerate(terms):
                ms = m + dm
                if abs(ms) <= ls:
                    idx[_pidx(l, m), t] = _fidx(ls, ms)
                    wts[_pidx(l, m), t] = w
    return idx, wts, L_out

def _apply_deriv(kind, axis, coeffs, L_in):
    idx, wts, L_out = _deriv_table(kind, axis, L_in)
    full = _to_full(coeffs, L_in, pad=True)
    return np.sum(full[..., idx] * wts, axis=-1), L_out

@functools.lru_cache(maxsize=None)
def _sym_tensor_map(k):
    """unique index combos for a symmetric rank-k 3-tensor and the full -> combo gather map"""
    combos = list(itertools.combinations_with_replacement(range(3), k))
    lookup = {c: i for i, c in enumerate(combos)}
    full = np.array([lookup[tuple(sorted(p))] for p in itertools.product(range(3), repeat=k)], dtype=int)
    return combos, full

def _fill_symmetric(unique_vals, k):
    """(..., n_combo) unique elements -> (..., 3, ..., 3) symmetric tensor via one gather"""
    _, full = _sym_tensor_map(k)
    return unique_vals[..., full].reshape(unique_vals.shape[:-1] + (3,) * k)

def _derivative_expansions(kind, coeffs, L, deriv_order, L_pad):
    """returns [(..., n_combo_k, P(L_pad)) for k in 0..deriv_order]"""
    cache = {(): (coeffs, L)}
    stacks = []
    for k in range(deriv_order + 1):
        combos, _ = _sym_tensor_map(k)
        terms = []
        for c in combos:
            if c not in cache:
                base, Lb = cache[c[:-1]]
                cache[c] = _apply_deriv(kind, c[-1], base, Lb)
            terms.append(_pad_packed(cache[c][0], L_pad))
        stacks.append(np.stack(terms, axis=-2))
    return stacks

def _evaluate_expansion_derivs(stacks, harmonics, L_pad, conj_coeffs):
    w = _real_weights(L_pad)
    res = []
    for k, C in enumerate(stacks):
        C = np.conj(C) if conj_coeffs else C
        vals = np.einsum('...cp,...np->...nc', w * C, harmonics).real
        res.append(_fill_symmetric(vals, k) if k > 0 else vals[..., 0])
    return res

def multipole_potential(moments, eval_pts, center=None, deriv_order=0, smearing=None):
    """
    Evaluates `V(r) = sum conj(M_lm) I_lm(r - c)` (M2P) and optionally its
    Cartesian derivatives, which are themselves multipole expansions obtained
    by index shifts.

    With `smearing = sigma` the moments are taken to be those of a Gaussian-smeared density
    `sum_lm p_lm C_l |r|^l exp(-|r|^2 / 2 sigma^2) Y_lm` (normalized so `p_lm` are its multipole
    moments, the GTO convention of `graph_longrange`/MACE-POLAR), whose exact potential is the point
    potential with each `l` component damped by `P(l + 1/2, |r - c|^2 / 2 sigma^2)` (regularized lower
    incomplete gamma). This only makes sense for a single smeared site per expansion, e.g. atomic
    multipoles; derivatives are supported up to second order.

    :param moments: packed moments, `(..., P)`
    :type moments: np.ndarray
    :param eval_pts: evaluation points, `(..., N, 3)`
    :type eval_pts: np.ndarray
    :param center: expansion center, `(..., 3)`
    :type center: np.ndarray | None
    :param deriv_order: number of Cartesian derivatives to return
    :type deriv_order: int
    :param smearing: Gaussian width(s) `sigma`, broadcast against the leading axes of `moments`
    :type smearing: float | np.ndarray | None
    :return: `V` with shape `(..., N)` if `deriv_order == 0`, else the expansion list
        `[V, dV (..., N, 3), d2V (..., N, 3, 3), ...]`
    :rtype: np.ndarray | list[np.ndarray]
    """
    moments = np.asanyarray(moments)
    if smearing is not None:
        return _smeared_multipole_potential(moments, eval_pts, center, smearing, deriv_order)
    L = multipole_expansion_order(moments)
    L_pad = L + deriv_order
    I = _irregular_harmonics(_displace(eval_pts, center), L_pad)
    stacks = _derivative_expansions('multipole', moments, L, deriv_order, L_pad)
    res = _evaluate_expansion_derivs(stacks, I, L_pad, conj_coeffs=True)
    return res[0] if deriv_order == 0 else res

def local_multipole_potential(local, eval_pts, center=None, deriv_order=0):
    """
    Evaluates `V(r) = sum F_lm conj(R_lm(r - c))` (L2P) and optionally its
    Cartesian derivatives.

    :param local: packed local coefficients, `(..., P)`
    :type local: np.ndarray
    :param eval_pts: evaluation points, `(..., N, 3)`
    :type eval_pts: np.ndarray
    :param center: expansion center, `(..., 3)`
    :type center: np.ndarray | None
    :param deriv_order: number of Cartesian derivatives to return
    :type deriv_order: int
    :return: `V` with shape `(..., N)` if `deriv_order == 0`, else the expansion list
        `[V, dV (..., N, 3), d2V (..., N, 3, 3), ...]`
    :rtype: np.ndarray | list[np.ndarray]
    """
    local = np.asanyarray(local)
    L = multipole_expansion_order(local)
    R = np.conj(_regular_harmonics(_displace(eval_pts, center), L))
    stacks = _derivative_expansions('local', local, L, deriv_order, L)
    res = _evaluate_expansion_derivs(stacks, R, L, conj_coeffs=False)
    return res[0] if deriv_order == 0 else res


def _smeared_radial_factors(r, sigma, l, deriv_order):
    """`g(r) = P(l + 1/2, r^2 / 2 sigma^2)` and its first two radial derivatives"""
    a = l + .5
    x = r ** 2 / (2 * sigma ** 2)
    res = [scipy.special.gammainc(a, x)]
    if deriv_order > 0:
        # h = x^(a-1) e^-x / Gamma(a), g' = h dx/dr, g'' = h (2l/sigma^2 - r^2/sigma^4)
        h = np.exp((a - 1) * np.log(x) - x - scipy.special.gammaln(a))
        res.append(h * r / sigma ** 2)
        if deriv_order > 1:
            res.append(h * (2 * l / sigma ** 2 - r ** 2 / sigma ** 4))
    return res

def _smeared_multipole_potential(moments, eval_pts, center, smearing, deriv_order):
    if deriv_order > 2:
        raise NotImplementedError("smeared multipole potentials support at most second derivatives")
    L = multipole_expansion_order(moments)
    sigma = np.asanyarray(smearing, dtype=float)[..., np.newaxis]  # broadcast over the N axis
    eval_pts = np.asanyarray(eval_pts, dtype=float)
    disp = _displace(eval_pts, center)
    r = np.sqrt(np.reshape(vec_dots(disp, disp), disp.shape[:-1]))
    # the smeared potential is smooth at the center, but the point harmonics are not;
    # nudge exact hits off the center (error O(eps^2) in V)
    eps = 1e-7 * np.min(sigma)
    hit = r < eps
    if np.any(hit):
        disp = np.where(hit[..., np.newaxis], np.array([0., 0., eps]), disp)
        r = np.where(hit, eps, r)
    u = disp / r[..., np.newaxis]
    eye = np.eye(3)
    uu = u[..., :, np.newaxis] * u[..., np.newaxis, :]
    res = None
    for l in range(L + 1):
        Ml = moments[..., :_packed_size(l)].copy()
        if l > 0:
            Ml[..., :_packed_size(l - 1)] = 0
        Vp = multipole_potential(Ml, disp, deriv_order=deriv_order)
        if deriv_order == 0:
            Vp = [Vp]
        g = _smeared_radial_factors(r, sigma, l, deriv_order)
        terms = [g[0] * Vp[0]]
        if deriv_order > 0:
            dg = g[1][..., np.newaxis] * u
            terms.append(g[0][..., np.newaxis] * Vp[1] + dg * Vp[0][..., np.newaxis])
        if deriv_order > 1:
            d2g = (
                    g[2][..., np.newaxis, np.newaxis] * uu
                    + (g[1] / r)[..., np.newaxis, np.newaxis] * (eye - uu)
            )
            terms.append(
                g[0][..., np.newaxis, np.newaxis] * Vp[2]
                + dg[..., :, np.newaxis] * Vp[1][..., np.newaxis, :]
                + Vp[1][..., :, np.newaxis] * dg[..., np.newaxis, :]
                + Vp[0][..., np.newaxis, np.newaxis] * d2g
            )
        res = terms if res is None else [a + b for a, b in zip(res, terms)]
    return res[0] if deriv_order == 0 else res


def smeared_multipole_density(moments, eval_pts, center=None, smearing=1.):
    """
    Evaluates the Gaussian-smeared (GTO) density whose exact multipole moments are `moments`,
    in the basis used by `multipole_potential(..., smearing=...)` (`graph_longrange`/MACE-POLAR):

        rho(r) = sum_lm p_lm C_l sqrt((2l+1)/4pi) S_lm(r - c) exp(-|r - c|^2 / 2 sigma^2),
        C_l = 1 / (sqrt(4pi/(2l+1)) 2^(l+1/2) Gamma(l+3/2) sigma^(2l+3))

    with `S_lm` the real Racah-normalized solid harmonics and `p_lm` the real moments. The
    `l = 0` term is a normalized Gaussian carrying the monopole.

    :param moments: packed moments, `(..., P)`
    :type moments: np.ndarray
    :param eval_pts: evaluation points, `(..., N, 3)`
    :type eval_pts: np.ndarray
    :param center: expansion center, `(..., 3)`
    :type center: np.ndarray | None
    :param smearing: Gaussian width(s) `sigma`, broadcast against the leading axes of `moments`
    :type smearing: float | np.ndarray
    :return: the density, `(..., N)`
    :rtype: np.ndarray
    """
    moments = np.asanyarray(moments)
    L = multipole_expansion_order(moments)
    real = _complex_to_real(moments, L)  # (..., K)
    disp = _displace(eval_pts, center)
    S = solid_harmonics(disp, L, real=True)  # (..., N, K)
    sigma = np.asanyarray(smearing, dtype=float)[..., np.newaxis]
    ls = np.concatenate([np.full(2 * l + 1, l) for l in range(L + 1)])
    pref = (2 * ls + 1) / (4 * np.pi) / (2 ** (ls + .5) * scipy.special.gamma(ls + 1.5))
    coeffs = real * pref * sigma ** (-(2 * ls + 3))  # (..., K)
    r2 = np.reshape(vec_dots(disp, disp), disp.shape[:-1])
    return np.einsum('...nk,...k->...n', S, coeffs) * np.exp(-r2 / (2 * sigma ** 2))


# ---------------------------------------------------------------------------
# rotations
#
# For a rotation (or any orthogonal map) Q, R_lm(Q x) = sum_m' T(Q)_mm' R_lm'(x) within each l.
# Since the R_l. restricted to the unit sphere are orthogonal, T is obtained exactly from a
# Lebedev rule of degree >= 2l:  T_mm' = <R_lm(Q .), R_lm'> / <R_lm', R_lm'>.
# That is one batched einsum per call, has no Euler-angle singularities, and handles
# improper rotations. Irregular harmonics transform with T_mm' f_m / f_m', f_m = (l+m)!(l-m)!.

@functools.lru_cache(maxsize=None)
def _rotation_quadrature(L):
    degs = [d for d in sorted(_LEBEDEV_DEGREES) if d >= 2 * L]
    if len(degs) == 0:
        raise ValueError(f"no tabulated Lebedev rule is exact to degree {2 * L}")
    pts, w = lebedev_grid(degs[0], use_degree=True, return_weights=True)
    R = _to_full(_regular_harmonics(pts, L), L)  # (npts, F)
    norms = np.concatenate([
        [4 * np.pi / (2 * l + 1) / (math.factorial(l + m) * math.factorial(l - m)) for m in range(-l, l + 1)]
        for l in range(L + 1)
    ])
    proj = np.conj(R) * (4 * np.pi * w)[:, np.newaxis] / norms[np.newaxis, :]
    return pts, proj

def multipole_rotation_matrices(rotations, L, kind='multipole'):
    """
    Per-`l` transformation matrices for rotating a multipole (or local) expansion, i.e. the
    expansion of the rotated source distribution `x_i -> Q x_i` about the same center.

    :param rotations: orthogonal matrices, `(..., 3, 3)`
    :type rotations: np.ndarray
    :param L: expansion order
    :type L: int
    :param kind: `'multipole'` (regular harmonics) or `'local'` (irregular harmonics)
    :type kind: str
    :return: list over `l` of complex `(..., 2l+1, 2l+1)` blocks acting on `m = -l..l`
    :rtype: list[np.ndarray]
    """
    Q = np.asanyarray(rotations, dtype=float)
    pts, proj = _rotation_quadrature(L)
    rot_pts = np.einsum('...ij,kj->...ki', Q, pts)
    RQ = _to_full(_regular_harmonics(rot_pts, L), L)  # (..., npts, F)
    blocks = []
    for l in range(L + 1):
        sl = slice(l * l, (l + 1) ** 2)
        T = np.einsum('...km,kn->...mn', RQ[..., sl], proj[:, sl])
        if kind == 'local':
            f = np.array([math.factorial(l + m) * math.factorial(l - m) for m in range(-l, l + 1)], dtype=float)
            T = T * (f[:, np.newaxis] / f[np.newaxis, :])
        elif kind != 'multipole':
            raise ValueError(f"unknown expansion kind '{kind}'")
        blocks.append(T)
    return blocks

def _apply_rotation(coeffs, rotations, kind):
    coeffs = np.asanyarray(coeffs)
    L = multipole_expansion_order(coeffs)
    blocks = multipole_rotation_matrices(rotations, L, kind=kind)
    full = _to_full(coeffs, L)
    out = []
    for l, T in enumerate(blocks):
        # only the m >= 0 rows are needed for the packed result
        out.append(np.einsum('...mn,...n->...m', T[..., l:, :], full[..., l * l:(l + 1) ** 2]))
    return np.concatenate(out, axis=-1)

def rotate_multipoles(moments, rotations):
    """
    Rotates multipole moments: returns the moments of the source distribution mapped by
    `x -> Q (x - c) + c` about the expansion center `c`.

    :param moments: packed moments, `(..., P)`
    :type moments: np.ndarray
    :param rotations: orthogonal matrices, `(..., 3, 3)` (improper rotations are allowed)
    :type rotations: np.ndarray
    :return: rotated packed moments
    :rtype: np.ndarray
    """
    return _apply_rotation(moments, rotations, 'multipole')

def rotate_local_multipoles(local, rotations):
    """
    Rotates a local expansion: returns the expansion, about the same center, of the sources
    mapped by `x -> Q (x - c) + c`.

    :param local: packed local coefficients, `(..., P)`
    :type local: np.ndarray
    :param rotations: orthogonal matrices, `(..., 3, 3)`
    :type rotations: np.ndarray
    :return: rotated packed local coefficients
    :rtype: np.ndarray
    """
    return _apply_rotation(local, rotations, 'local')


# ---------------------------------------------------------------------------
# Cartesian <-> spherical

def _combo_counts(combo):
    return tuple(combo.count(i) for i in range(3))

@functools.lru_cache(maxsize=None)
def _harmonic_polynomials(L):
    """
    Monomial coefficients of R_lm: list over l of complex (l+1, n_combo_l)
    arrays, `R_lm(r) = sum_c C[m, c] x^a y^b z^c` with `(a, b, c)` the counts of combo `c`.
    Built with the same recurrence as `_regular_harmonics`, acting on coefficient cubes.
    """
    n = L + 3
    def zmul(p): out = np.zeros_like(p); out[:, :, 1:] = p[:, :, :-1]; return out
    def xmul(p): out = np.zeros_like(p); out[1:] = p[:-1]; return out
    def ymul(p): out = np.zeros_like(p); out[:, 1:] = p[:, :-1]; return out
    def r2mul(p): return xmul(xmul(p)) + ymul(ymul(p)) + zmul(zmul(p))
    polys = {}
    one = np.zeros((n, n, n), dtype=complex); one[0, 0, 0] = 1
    polys[(0, 0)] = one
    for l in range(1, L + 1):
        for m in range(l):
            t = (2 * l - 1) * zmul(polys[(l - 1, m)])
            if m <= l - 2:
                t = t - r2mul(polys[(l - 2, m)])
            polys[(l, m)] = t / ((l + m) * (l - m))
        p = polys[(l - 1, l - 1)]
        polys[(l, l)] = -(xmul(p) + 1j * ymul(p)) / (2 * l)
    mats = []
    for l in range(L + 1):
        combos, _ = _sym_tensor_map(l)
        C = np.zeros((l + 1, len(combos)), dtype=complex)
        for i, c in enumerate(combos):
            a, b, cc = _combo_counts(c)
            for m in range(l + 1):
                C[m, i] = polys[(l, m)][a, b, cc]
        mats.append(C)
    return mats

@functools.lru_cache(maxsize=None)
def _traceless_synthesis(l):
    """(n_combo, 2l+1) real map from real-layout spherical moments to traceless tensor elements"""
    C = _harmonic_polynomials(l)[l]
    combos, _ = _sym_tensor_map(l)
    mult = np.array([
        math.factorial(l) / np.prod([math.factorial(k) for k in _combo_counts(c)])
        for c in combos
    ])
    # analysis map A: tensor unique elements -> real layout [Re m0, Re m1, Im m1, ...]
    rows = [C[0].real]
    for m in range(1, l + 1):
        rows.extend([C[m].real, C[m].imag])
    A = np.array(rows)
    # harmonic (traceless) tensors spanning the image: P = C / multinomial
    B = (A / mult[np.newaxis, :]).T
    return B @ np.linalg.inv(A @ B)

def _cart_scale(l, convention):
    convention = convention.lower()
    if convention in ('raw', 'traceless'):
        return 1.
    elif convention == 'buckingham':
        return math.prod(range(1, 2 * l, 2)) / math.factorial(l)
    raise ValueError(f"unknown Cartesian multipole convention '{convention}'")

def cartesian_to_spherical_multipoles(tensors, convention='raw'):
    """
    Converts Cartesian multipole tensors `[M0, M1 (...,3), M2 (...,3,3), ...]`
    to packed spherical moments. Only the traceless part of each tensor
    contributes, so `'raw'` and `'traceless'` inputs give identical results.

    :param tensors: Cartesian moments by order
    :type tensors: list[np.ndarray]
    :param convention: `'raw'` (`sum q x_a x_b ...`), `'traceless'` (detraced raw, e.g. Gaussian's
        "Traceless Quadrupole"), or `'buckingham'` (`(2l-1)!!/l!` times detraced)
    :type convention: str
    :return: packed spherical moments
    :rtype: np.ndarray
    """
    L = len(tensors) - 1
    C = _harmonic_polynomials(L)
    blocks = []
    for l, t in enumerate(tensors):
        t = np.asanyarray(t, dtype=float)
        if l == 0:
            blocks.append(t[..., np.newaxis].astype(complex))
            continue
        combos, _ = _sym_tensor_map(l)
        flat = t.reshape(t.shape[:t.ndim - l] + (3 ** l,))
        canon = [int(np.ravel_multi_index(c, (3,) * l)) for c in combos]
        vals = flat[..., canon] / _cart_scale(l, convention)
        blocks.append(np.einsum('mc,...c->...m', C[l], vals))
    return np.concatenate(blocks, axis=-1)

def spherical_to_cartesian_multipoles(moments, convention='traceless'):
    """
    Converts packed spherical moments to traceless Cartesian tensors
    `[M0, M1 (...,3), M2 (...,3,3), ...]`.

    :param moments: packed spherical moments
    :type moments: np.ndarray
    :param convention: `'traceless'` (detraced raw) or `'buckingham'`
    :type convention: str
    :return: Cartesian moments by order
    :rtype: list[np.ndarray]
    """
    moments = np.asanyarray(moments)
    L = multipole_expansion_order(moments)
    if convention.lower() == 'raw':
        raise ValueError("spherical moments only determine the traceless part; use 'traceless' or 'buckingham'")
    real = _to_reim_layout(moments, L)
    res = [real[..., 0]]
    for l in range(1, L + 1):
        S = _traceless_synthesis(l)
        q = real[..., l * l:(l + 1) ** 2]
        vals = np.einsum('cm,...m->...c', S, q) * _cart_scale(l, convention)
        res.append(_fill_symmetric(vals, l))
    return res

def cartesian_multipole_moments(pts, charges, L, center=None, convention='raw'):
    """
    Cartesian multipole tensors `[M0, M1 (...,3), ..., ML (...,3,...,3)]`.
    Raw moments are built from the unique monomials only and expanded with a
    single gather per order.

    :param pts: source positions, `(..., N, 3)`
    :type pts: np.ndarray
    :param charges: source charges, `(..., N)` (`None` for unit charges)
    :type charges: np.ndarray | None
    :param L: maximum order
    :type L: int
    :param center: expansion center, `(..., 3)`
    :type center: np.ndarray | None
    :param convention: `'raw'`, `'traceless'`, or `'buckingham'`
    :type convention: str
    :return: Cartesian moments by order
    :rtype: list[np.ndarray]
    """
    convention = convention.lower()
    if convention != 'raw':
        return spherical_to_cartesian_multipoles(
            multipole_moments(pts, charges, L, center=center),
            convention=convention
        )
    disp = _displace(pts, center)
    q = _prep_charges(charges, disp)
    res = [np.sum(q, axis=-1)]
    for l in range(1, L + 1):
        combos, _ = _sym_tensor_map(l)
        mono = np.prod(disp[..., np.array(combos)], axis=-1)  # (..., N, n_combo)
        vals = np.matmul(q[..., np.newaxis, :], mono)[..., 0, :]
        res.append(_fill_symmetric(vals, l))
    return res

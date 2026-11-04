"""Haar SO(3) averages of Cartesian vector products of arbitrary order.

The default algorithm multiplies Wigner D expansions by spin-one factors.
Only Fourier coefficients are retained, not individual coupling paths. The
Bonvicini and Smith/Young contraction bases provide independent references.
All vector contractions are bilinear; physical complex conjugations are
explicit. This is one common, static orientation for all factors.
"""
import operator
import numpy as np
from .AngularMomentum import clebsch_gordan_spin1_couplings



__all__ = ['wigner_d_coefficients',
           'wigner_d_multiply_vector', 'wigner_d_haar_average', 'rotational_average']


# Spherical order -1, 0, +1; our D^1(R) = U R U^dagger.
# For active z-y-z R and the convention D_std = exp(-im*a)d(b)exp(-in*g),
# this is D_std.conj(). The CG coefficients are real, so the product rule
# is unchanged. In particular D^1(Rz(a)) = diag(exp(-ia), 1, exp(ia)).
_U = np.array([[1, -1j, 0], [0, 0, np.sqrt(2)], [-1, -1j, 0]]) / np.sqrt(2)
_U.flags.writeable = False








def wigner_d_coefficients(coefficients=None):
    """Validate and broadcast Fourier coefficient blocks; no wrapper objects."""
    if coefficients is None:
        return {0: np.ones((1, 1), dtype=complex)}
    blocks = {}
    for j, block in coefficients.items():
        j = operator.index(j)
        block = np.asarray(block, dtype=complex)
        if j < 0 or block.shape[-2:] != (2*j+1, 2*j+1):
            raise ValueError('a spin-j block must have shape (...,2*j+1,2*j+1)')
        blocks[j] = block
    batch = np.broadcast_shapes(*[b.shape[:-2] for b in blocks.values()])
    return {j: np.broadcast_to(b, batch+b.shape[-2:]) for j, b in blocks.items()}


def wigner_d_multiply_vector(coefficients, factor, max_j=None):
    """Multiply by sum(factor[s,t] D^1_st), optionally truncating spin.

    A truncation is exact for a final scalar when max_j equals the number
    of remaining vector factors: larger j cannot return to zero.
    """
    coefficients = wigner_d_coefficients(coefficients)
    factor = np.asarray(factor, dtype=complex)
    if factor.shape[-2:] != (3, 3):
        raise ValueError('spin-one coefficients must have shape (...,3,3)')
    if max_j is not None:
        max_j = operator.index(max_j)
        if max_j < 0:
            raise ValueError('max_j must be nonnegative')
    updated = {}
    for j, block in coefficients.items():
        batch = np.broadcast_shapes(block.shape[:-2], factor.shape[:-2])
        for ell in range(abs(j-1), j+2):
            if max_j is not None and ell > max_j:
                continue
            if ell not in updated:
                updated[ell] = np.zeros(batch + (2*ell+1, 2*ell+1), complex)
            out = updated[ell]
            for q in (-1, 0, 1):
                src_m, dst_m, cg_m = clebsch_gordan_spin1_couplings(j, ell, q)
                for r in (-1, 0, 1):
                    src_n, dst_n, cg_n = clebsch_gordan_spin1_couplings(j, ell, r)
                    out[..., dst_m[:, None], dst_n] += (
                        block[..., src_m[:, None], src_n]
                        * (cg_m[:, None] * cg_n)
                        * factor[..., q+1, r+1, None, None]
                    )
    return updated


def wigner_d_haar_average(coefficients):
    """Normalized Haar projection of unnormalized Wigner coefficient blocks."""
    if 0 in coefficients:
        return coefficients[0][..., 0, 0]
    shapes = [b.shape[:-2] for b in coefficients.values()]
    return np.zeros(np.broadcast_shapes(*shapes), dtype=complex)


def _vectors(vectors, name):
    vectors = np.asarray(vectors)
    if vectors.ndim < 2 or vectors.shape[-1] != 3:
        raise ValueError(name + ' must have shape (...,number_of_factors,3)')
    if vectors.dtype.kind not in 'buifc' or not np.all(np.isfinite(vectors)):
        raise ValueError(name + ' must contain finite numerical vectors')
    return vectors.astype(np.result_type(vectors.dtype, float), copy=False)


def _conjugate(vectors, mask):
    if mask is None:
        return vectors
    mask = np.asarray(mask, dtype=bool)
    if mask.ndim > 1 or (mask.ndim == 1 and mask.shape != (vectors.shape[-2],)):
        raise ValueError('conjugations must be a bool or one bool per factor')
    return np.where(mask[..., None], vectors.conj(), vectors)


def rotational_average(polarizations, moments, *,
                       conjugate_polarizations=None, conjugate_moments=None):
    """Numerical Wigner average of prod(e[k].T @ R @ mu[k]) over Haar SO(3).

    Inputs have shape (...,K,3). Contractions are bilinear; conjugations are
    explicit. For reusable averagers and reference bases use McUtils.Zachary.
    """
    lab = _conjugate(_vectors(polarizations, 'polarizations'), conjugate_polarizations)
    mol = _conjugate(_vectors(moments, 'moments'), conjugate_moments)
    if lab.shape[-2] != mol.shape[-2]:
        raise ValueError('one polarization is required per interaction/detection factor')
    batch = np.broadcast_shapes(lab.shape[:-2], mol.shape[:-2])
    order = lab.shape[-2]
    if not order:
        return np.ones(batch)
    real = not np.iscomplexobj(lab) and not np.iscomplexobj(mol)
    lab, mol = lab @ _U.conj().T, mol @ _U.T
    coefficients = wigner_d_coefficients()
    for k in range(order):
        factor = lab[..., k, :, None] * mol[..., k, None, :]
        coefficients = wigner_d_multiply_vector(coefficients, factor, max_j=order-k-1)
    result = np.broadcast_to(wigner_d_haar_average(coefficients), batch)
    return result.real if real else result

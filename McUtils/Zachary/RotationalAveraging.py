"""Reusable orientational averages and Fourier expansions over SO(3).

Numerical coefficient updates live in Numputils; symbolic reference bases
live alongside the tensor expression architecture in Zachary.Symbolic.
"""
import numpy as np
from .. import Numputils as nput
from ..Numputils.RotationalAveraging import _vectors, _conjugate, _U

__all__ = ['WignerDExpansion', 'OrientationalAverager', 'rotational_average']


class WignerDExpansion:
    """Reusable Wigner expansion wrapping Numputils' coefficient kernels."""
    def __init__(self, coefficients=None):
        self.coefficients = nput.wigner_d_coefficients(coefficients)

    def multiply_vector(self, factor, max_j=None):
        return type(self)(nput.wigner_d_multiply_vector(self.coefficients, factor, max_j=max_j))

    def haar_average(self):
        return nput.wigner_d_haar_average(self.coefficients)


class OrientationalAverager:
    """Reusable average prod_k(e_k^T R mu_k), with normalized Haar SO(3).

    Polarizations and moments have shape (..., K, 3), with broadcast batches.
    No normalization or automatic conjugation is performed. K includes any
    detection factor. Methods: 'wigner' (default), 'bonvicini', and 'young'.
    The reference methods grow combinatorially; no order cap is imposed.
    """
    def __init__(self, polarizations, method='wigner', conjugations=None):
        self.polarizations = _conjugate(_vectors(polarizations, 'polarizations'), conjugations).copy()
        self.polarizations.flags.writeable = False
        self.order = self.polarizations.shape[-2]
        if method not in ('wigner', 'bonvicini', 'young'):
            raise ValueError('unknown orientational averaging method: ' + str(method))
        self.method = method
        self._real = not np.iscomplexobj(self.polarizations)
        if method == 'wigner':
            self._lab = self.polarizations @ _U.conj().T
        else:
            from .Symbolic.IsotropicTensors import isotropic_tensor_basis
            self.basis = isotropic_tensor_basis(self.order, method=method)
            self._lab = self.basis.values(self.polarizations)

    def __call__(self, moments, conjugations=None):
        moments = _conjugate(_vectors(moments, 'moments'), conjugations)
        if moments.shape[-2] != self.order:
            raise ValueError('one polarization is required for every interaction/detection factor')
        batch = np.broadcast_shapes(self.polarizations.shape[:-2], moments.shape[:-2])
        if self.order == 0:
            return np.ones(batch)
        if self.method == 'wigner':
            mol = moments @ _U.T
            state = WignerDExpansion()
            for k in range(self.order):
                factor = self._lab[..., k, :, None] * mol[..., k, None, :]
                state = state.multiply_vector(factor, max_j=self.order-k-1)
            result = np.broadcast_to(state.haar_average(), batch)
        else:
            result = self.basis.average_values(self._lab, self.basis.values(moments))
        return result.real if self._real and not np.iscomplexobj(moments) else result


def rotational_average(polarizations, moments, method='wigner', *,
                       conjugate_polarizations=None, conjugate_moments=None):
    """Average a finite vector product; see OrientationalAverager."""
    return OrientationalAverager(polarizations, method, conjugate_polarizations)(
        moments, conjugations=conjugate_moments
    )

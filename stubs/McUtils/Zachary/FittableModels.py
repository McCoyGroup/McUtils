"""
Defines classes for providing different approaches to fitting.
For the most part, the idea is to use `scipy.optimize` to do the actual fitting process,
but we layer on conveniences w.r.t. specification of bases and automation of the actual fitting process
"""
import abc
from .. import Devutils as dev
import numpy as np, scipy.optimize as opt, enum
from collections import OrderedDict as odict
__all__ = ['FittedModel']

class FittedModel:

    def __init__(self, fit_basis, expansion_coeffs=None, basis_parameters=None, **kwargs):
        ...

    @classmethod
    def canonicalize_basis(cls, fit_basis, basis_parameters):
        ...

    def __call__(self, pts, order=None, **opts):
        ...

    @classmethod
    def evaluate_kernel(cls, fit_basis, basis_parameters, pts, coeffs=None, order=None, **opts):
        ...

    @classmethod
    def _handle_nl_fit_params(cls, params, kernels, param_names, include_expansion_coefficients=True):
        ...

    @classmethod
    def get_kernel_and_opts(cls, k):
        ...

    @classmethod
    def parse_kernel_specs(cls, kernels):
        ...

    @classmethod
    def nonlinear_fit(cls, kernel_specs, pts, observations, include_expansion_coefficients=True, **fit_params):
        ...

    @classmethod
    def get_fit_methods(cls):
        ...
    _fit_dispatch = dev.uninitialized
    default_fit_method = 'nonlinear_fit'

    @classmethod
    def get_fit_dispatch(cls):
        ...

    @classmethod
    def fit(cls, kernels, pts, observations, method=None, **opts):
        ...
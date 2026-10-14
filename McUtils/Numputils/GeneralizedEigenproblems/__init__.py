"""Stable symmetric/Hermitian generalized eigenproblem tools.

All eigensolvers return (values, column vectors); return_info=True appends a
diagnostic dictionary. Geometric Cholesky and absolute iterative tolerances
are independent of matrix dimension and Hamiltonian energy origin. FH retains
its original relative spectral perturbation model. Singular-pencil random
methods require an explicit normal rank; they do not infer it from A's zero.
"""
import numpy as np
from scipy.linalg import eigh, solve_triangular
from .Common import *; from .Common import __all__ as _all
__all__ = list(_all)
from .Cholesky import *; from .Cholesky import __all__ as _all
__all__ += _all
from .Iterative import *; from .Iterative import __all__ as _all
__all__ += _all
from .Pencils import *; from .Pencils import __all__ as _all
__all__ += _all
__all__ += ["generalized_eigh"]
from .Common import _adjoint, _pencil, _whiten, _subset, _result


def generalized_eigh(a, b, method="cholesky", states=None, return_info=False, **options):
    """Dispatch a solver using the same (A, B) argument order as scipy.linalg.eigh.

    For near-singular B, method='lobpcg' selects functions before iterating in a
    Cholesky-whitened space; overlap_tolerance controls geometric selection and
    tolerance controls iterative residuals. robust_lobpcg exposes direct SPD-B
    iterations separately. Other methods expose their own explicit tolerances.
    """
    if method == "dense":
        a, b = _pencil(a, b)
        e, c = eigh(a, b, subset_by_index=_subset(states, len(a)), **options)
        return _result(e, c, dict(rank=len(a)), return_info)
    if method in {"cholesky", "random-cholesky", "accelerated-cholesky"}:
        variant = {"cholesky": "greedy", "random-cholesky": "random",
                   "accelerated-cholesky": "accelerated"}[method]
        return cholesky_eigh(a, b, states=states, method=variant,
                             return_info=return_info, **options)
    if method == "fix-heiberger":
        return fix_heiberger(a, b, states=states, return_info=return_info, **options)
    if method in {"rank-projection", "rank-completion"}:
        solver = rank_projection_eigh if method == "rank-projection" else rank_completion_eigh
        return solver(a, b, states=states, return_info=return_info, **options)
    if method == "lobpcg":
        if states is None:
            raise ValueError("states is required for LOBPCG")
        a, b = _pencil(a, b)
        diagonal = b.diagonal().real
        if np.any(diagonal <= 0):
            raise ValueError("positive basis-function norms required")
        scale = 1 / np.sqrt(diagonal)
        _, pivots, info = pivoted_cholesky(b * scale[:, None] * scale[None, :],
            tolerance=options.pop("overlap_tolerance", 1e-10), return_info=True)
        selected = np.ix_(pivots, pivots)
        h, l = _whiten(a[selected], b[selected])
        e, u, iteration = robust_lobpcg(h, states=states, return_info=True, **options)
        c = np.zeros((len(a), len(e)), dtype=u.dtype)
        c[pivots] = solve_triangular(_adjoint(l), u, lower=False)
        info.update(iteration)
        return _result(e, c, info, return_info)
    raise ValueError(f"unknown generalized eigensolver {method!r}")

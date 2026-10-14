"""Shared metric and Ritz operations for symmetric/Hermitian pencils."""
import numpy as np
from scipy.linalg import cholesky, eigh, solve_triangular
from ..VectorOps import vec_norms

__all__ = ["eigenpair_residuals", "ritz_eigh", "cholesky_orthogonalize",
           "shifted_preconditioner"]


def _adjoint(a):
    return a.conj().T


def _hermitian(a):
    return (a + _adjoint(a)) / 2


def _apply(a, x):
    return x if a is None else (a(x) if callable(a) else a @ x)


def _pencil(a, b):
    a, b = np.asarray(a), np.asarray(b)
    if a.ndim != 2 or a.shape != b.shape or a.shape[0] != a.shape[1] or not len(a):
        raise ValueError("A and B must be nonempty square matrices of equal shape")
    if not np.isfinite(a).all() or not np.isfinite(b).all():
        raise ValueError("A and B must be finite")
    return _hermitian(a), _hermitian(b)


def _equilibrate(a, b, enabled):
    scale = np.ones(len(b))
    if enabled:
        diagonal = b.diagonal().real
        if np.any(diagonal < 0):
            raise ValueError("negative metric diagonal")
        positive = diagonal > 0
        scale[positive] = 1 / np.sqrt(diagonal[positive])
    return a * scale[:, None] * scale[None, :], b * scale[:, None] * scale[None, :], scale


def _subset(states, dimension):
    if states is None:
        return None
    if states < 1 or int(states) != states:
        raise ValueError("states must be a positive integer")
    return (0, min(states, dimension) - 1)


def _result(e, c, info, return_info):
    return (e, c, info) if return_info else (e, c)


def eigenpair_residuals(a, b, values, vectors):
    """Absolute column residual norms; invariant under A -> A + shift*B."""
    return vec_norms(_apply(a, vectors) - _apply(b, vectors) * values[None, :], axis=0)


def _whiten(a, b):
    l = cholesky(_hermitian(b), lower=True)
    h = solve_triangular(l, a, lower=True)
    h = _adjoint(solve_triangular(l, _adjoint(h), lower=True))
    return _hermitian(h), l


def ritz_eigh(a, b, basis, states=None):
    """Solve in the supplied trial span using its original positive metric."""
    basis = np.asarray(basis)
    if basis.shape[1] == 0:
        return np.empty(0), np.empty_like(basis)
    h, l = _whiten(_adjoint(basis) @ _apply(a, basis),
                   _adjoint(basis) @ _apply(b, basis))
    e, u = eigh(h, subset_by_index=_subset(states, len(h)))
    return e, basis @ solve_triangular(_adjoint(l), u, lower=False)


def cholesky_orthogonalize(x, against=None, metric=None, tolerance=1e-12, max_iterations=12):
    """Repeated/shifted Cholesky QR and re-projection (Nottoli et al., 2023).

    Columns of `against` must be metric-orthonormal. Temporary shifts stabilize
    factorization only; the returned Gram matrix is checked without a shift.
    No directions are discarded. Exactly dependent input columns are an error.
    """
    x = np.asarray(x)
    x = np.array(x, dtype=np.result_type(x.dtype, float), copy=True)
    if x.ndim != 2 or x.shape[1] > x.shape[0]:
        raise ValueError("x must have no more columns than rows")
    if tolerance <= 0 or max_iterations < 1:
        raise ValueError("positive tolerance and iteration limit required")
    if x.shape[1] == 0:
        return x
    y = against
    if y is not None and y.shape[1] + x.shape[1] > x.shape[0]:
        raise np.linalg.LinAlgError("insufficient orthogonal complement")
    by = None if y is None else _apply(metric, y)
    identity = np.eye(x.shape[1])
    eps = np.finfo(x.real.dtype).eps
    for _ in range(max_iterations):
        if y is not None:
            x -= y @ (_adjoint(by) @ x)
        gram = _hermitian(_adjoint(x) @ _apply(metric, x))
        shift = 0.
        for attempt in range(8):
            try:
                l = cholesky(gram + shift * identity, lower=True)
                break
            except np.linalg.LinAlgError:
                shift = (100 * eps * np.max(np.abs(gram.diagonal()))
                         if attempt == 0 else 10 * shift)
                if shift == 0:
                    raise np.linalg.LinAlgError("dependent orthogonalization block")
        else:
            raise np.linalg.LinAlgError("metric is not positive on the block")
        x = _adjoint(solve_triangular(l, _adjoint(x), lower=True))
        error = np.max(np.abs(_adjoint(x) @ _apply(metric, x) - identity))
        if y is not None:
            error = max(error, np.max(np.abs(_adjoint(by) @ x)))
        if error <= tolerance:
            return x
    raise np.linalg.LinAlgError("Cholesky orthogonalization did not converge")


def shifted_preconditioner(a, b=None, margin=.01, max_iterations=32):
    """Return (inverse action, shift) for an SPD A-shift*B factorization.

    Start below a diagonal Rayleigh upper bound and expand the margin until
    Cholesky succeeds. The shift follows an additive change of energy origin.
    This dense reference preconditioner makes no claim of iterative cost savings.
    """
    a = np.asarray(a)
    b = np.eye(len(a)) if b is None else np.asarray(b)
    if margin <= 0 or np.any(b.diagonal().real <= 0):
        raise ValueError("positive margin and metric diagonal required")
    upper = np.min(a.diagonal().real / b.diagonal().real)
    for _ in range(max_iterations):
        shift = float(upper - margin)
        try:
            l = cholesky(_hermitian(a - shift * b), lower=True)
            def apply(x):
                y = solve_triangular(l, x, lower=True)
                return solve_triangular(_adjoint(l), y, lower=False)
            return apply, shift
        except np.linalg.LinAlgError:
            margin *= 2
    raise np.linalg.LinAlgError("failed to obtain an SPD preconditioner")

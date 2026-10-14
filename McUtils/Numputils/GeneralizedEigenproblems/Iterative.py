"""LOBPCG with repeated/shifted Cholesky QR and stable coefficient updates."""
import numpy as np
from scipy.linalg import eigh
from ..VectorOps import vec_norms
from .Common import (_adjoint, _hermitian, _apply, _result, eigenpair_residuals,
                     cholesky_orthogonalize, shifted_preconditioner)

__all__ = ["robust_lobpcg"]


def robust_lobpcg(a, b=None, states=6, initial=None, preconditioner=None,
                  block_size=None, tolerance=1e-8, orthogonalization_tolerance=1e-12,
                  max_iterations=200, seed=None, return_info=False):
    """Smallest eigenpairs using the implementation structure of Nottoli et al.

    A and B may be matrices or callable block actions; callable A requires initial.
    B must be positive definite on the search space. Only requested roots enter
    convergence; a larger block can improve spectral separation. No directions
    are dropped on orthogonalization failures. The default residual tolerance is
    absolute and does not scale with dimension or Hamiltonian energy origin.
    Cached A/B products are transformed only by orthonormal coefficients.
    """
    if states < 1 or tolerance <= 0 or max_iterations < 1:
        raise ValueError("positive states, tolerance, and iteration limit required")
    if initial is None:
        if callable(a):
            raise ValueError("initial vectors required for callable A")
        n = np.shape(a)[0]
        width = min(n, max(states, states + 4 if block_size is None else block_size))
        random = np.random.default_rng(seed)
        initial = random.normal(size=(n, width))
        if np.iscomplexobj(a) or np.iscomplexobj(b):
            initial = initial + 1j * random.normal(size=(n, width))
    initial = np.asarray(initial)
    width = initial.shape[1]
    if width < states:
        raise ValueError("initial block must contain at least states columns")
    if initial.shape[0] <= 3 * width:
        identity = np.eye(initial.shape[0])
        e, x = eigh(_apply(a, identity), None if b is None else _apply(b, identity),
                    subset_by_index=(0, states - 1))
        info = dict(iterations=0, dense_fallback=True, converged=True,
                    residual_norms=eigenpair_residuals(a, b, e, x))
        return _result(e, x, info, return_info)
    if isinstance(preconditioner, str):
        if preconditioner != "shifted":
            raise ValueError(f"unknown preconditioner {preconditioner!r}")
        preconditioner, shift = shifted_preconditioner(a, b)
    else:
        shift = None
    ortho = lambda x, y=None, metric=b: cholesky_orthogonalize(
        x, against=y, metric=metric, tolerance=orthogonalization_tolerance)
    x = ortho(initial)
    ax, bx = _apply(a, x), _apply(b, x)
    e, u = eigh(_hermitian(_adjoint(x) @ ax))
    x, ax, bx = x @ u, ax @ u, bx @ u
    p = ap = bp = None
    history = []
    for iteration in range(max_iterations + 1):
        residual = ax - bx * e[None, :]
        norms = vec_norms(residual, axis=0)
        history.append(norms.copy())
        if np.max(norms[:states]) <= tolerance or iteration == max_iterations:
            break
        active = np.flatnonzero(norms > tolerance)
        if p is not None:
            p, ap, bp = p[:, active], ap[:, active], bp[:, active]
        against = x if p is None else np.column_stack([x, p])
        w = ortho(_apply(preconditioner, residual[:, active]), against)
        aw, bw = _apply(a, w), _apply(b, w)
        v = np.column_stack([x, w] if p is None else [x, w, p])
        av = np.column_stack([ax, aw] if p is None else [ax, aw, ap])
        bv = np.column_stack([bx, bw] if p is None else [bx, bw, bp])
        e, u = eigh(_hermitian(_adjoint(v) @ av), subset_by_index=(0, width - 1))
        x, ax, bx = v @ u, av @ u, bv @ u
        next_norms = eigenpair_residuals(a, b, e, x)
        next_active = np.flatnonzero(next_norms > tolerance)
        p = np.zeros_like(x)
        ap, bp = np.zeros_like(ax), np.zeros_like(bx)
        if len(next_active) and np.max(next_norms[:states]) > tolerance:
            # Project old-X coefficients out of new Ritz coefficients. This is
            # the increment span, without subtracting nearly equal large vectors.
            coefficients = np.eye(v.shape[1], width, dtype=v.dtype)[:, next_active]
            coefficients = ortho(coefficients, u, metric=None)
            p[:, next_active] = v @ coefficients
            ap[:, next_active] = av @ coefficients
            bp[:, next_active] = bv @ coefficients
    e, x = e[:states], x[:, :states]
    actual = eigenpair_residuals(a, b, e, x)
    info = dict(iterations=iteration, residual_history=np.array(history),
                residual_norms=actual, converged=bool(np.max(actual) <= tolerance),
                tolerance=tolerance, preconditioner_shift=shift,
                metric_error=float(np.max(np.abs(_adjoint(x) @ _apply(b, x) - np.eye(states)))))
    return _result(e, x, info, return_info)

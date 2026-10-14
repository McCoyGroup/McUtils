"""Fix--Heiberger and structure-preserving singular-pencil reductions."""
import numpy as np
from scipy.linalg import eigh, eig, qr, solve_triangular
from ..VectorOps import vec_norms
from .Common import (_adjoint, _hermitian, _pencil, _equilibrate, _subset,
                     _result, ritz_eigh, eigenpair_residuals)

__all__ = ["SingularPencilError", "fix_heiberger", "rank_projection_eigh",
           "rank_completion_eigh"]


class SingularPencilError(np.linalg.LinAlgError):
    """The thresholded pencil has a common numerical null space."""


def fix_heiberger(a, b, epsilon=1e-10, states=None, equilibrate=False,
                  hamiltonian_tolerance=None, constraint_tolerance=None,
                  refine_metric=False, return_info=False):
    """Finite epsilon-stable roots of a PSD pencil (Jiang/Bai's DSYGVIC).

    Small B eigenvalues are zeroed relative to its largest eigenvalue. Invertible
    null-B A directions are eliminated; remaining directions impose constraints.
    The output is normalized in the truncated metric. `refine_metric` explicitly
    performs a separate Ritz solve in the original metric. FH thresholds are
    relative spectral thresholds, not per-function geometric tolerances.
    """
    if not 0 < epsilon < 1:
        raise ValueError("epsilon must lie between zero and one")
    a, b = _pencil(a, b)
    an, bn, scale = _equilibrate(a, b, equilibrate)
    d, q = eigh(bn)
    d, q = d[::-1], q[:, ::-1]
    if d[-1] < -epsilon * max(d[0], 0):
        raise np.linalg.LinAlgError("B is not positive semidefinite")
    positive = np.count_nonzero(d > epsilon * d[0]) if d[0] > 0 else 0
    null = len(d) - positive
    h = _hermitian(_adjoint(q) @ an @ q)
    eps = np.finfo(d.dtype).eps
    if hamiltonian_tolerance is None:
        hamiltonian_tolerance = eps * np.linalg.norm(an, np.inf)
    if constraint_tolerance is None:
        constraint_tolerance = eps
    if hamiltonian_tolerance < 0 or constraint_tolerance < 0:
        raise ValueError("nonnegative rank thresholds required")
    info = dict(overlap_rank=int(positive), dimension=len(d), epsilon=epsilon,
                metric_refinement=refine_metric)
    if positive == 0:
        if np.min(np.abs(eigh(h, eigvals_only=True))) <= hamiltonian_tolerance:
            raise SingularPencilError("common null space with zero overlap")
        return _result(np.empty(0), np.empty((len(d), 0)), info, return_info)
    r = 1 / np.sqrt(d[:positive])
    h11 = h[:positive, :positive] * r[:, None] * r[None, :]
    if not null:
        reduced, y = h11, np.diag(r)
        info.update(null_hamiltonian_rank=0, constraint_rank=0)
    else:
        h12 = h[:positive, positive:] * r[:, None]
        f, v = eigh(h[positive:, positive:])
        order = np.argsort(np.abs(f))[::-1]
        f, v = f[order], v[:, order]
        maximum = np.max(np.abs(f))
        invertible = (np.count_nonzero(np.abs(f) > epsilon * maximum)
                      if maximum > hamiltonian_tolerance else 0)
        constraints = null - invertible
        f, v3, v4 = f[:invertible], v[:, :invertible], v[:, invertible:]
        coupling, constraint = h12 @ v3, h12 @ v4
        reduced = h11 - (coupling / f[None, :]) @ _adjoint(coupling)
        info.update(null_hamiltonian_rank=int(invertible), constraint_rank=int(constraints))
        if constraints:
            if constraints > positive:
                raise SingularPencilError("too many null-H constraints")
            u, triangular, pivots = qr(constraint, mode="full", pivoting=True)
            t = triangular[:constraints, :constraints]
            if np.any(np.abs(t.diagonal()) <= constraint_tolerance):
                raise SingularPencilError("common null space of A and thresholded B")
            w = u[:, constraints:]
            if not w.shape[1]:
                return _result(np.empty(0), np.empty((len(d), 0)), info, return_info)
            z3 = -(_adjoint(coupling) @ w) / f[:, None]
            rhs = _adjoint(u[:, :constraints]) @ (h11 @ w + coupling @ z3)
            z4 = -solve_triangular(t, rhs, lower=False)
            bottom = v3 @ z3 + v4[:, pivots] @ z4
            reduced, y = _adjoint(w) @ reduced @ w, np.vstack([r[:, None] * w, bottom])
        else:
            bottom = -v3 @ (_adjoint(coupling) / f[:, None])
            y = np.vstack([np.diag(r), bottom])
    trial = (q @ y) * scale[:, None]
    if refine_metric:
        e, c = ritz_eigh(a, b, trial, states=states)
    else:
        e, u = eigh(_hermitian(reduced), subset_by_index=_subset(states, len(reduced)))
        c = trial @ u
    info.update(rank=trial.shape[1], residual_norms=eigenpair_residuals(a, b, e, c),
                metric_error=float(np.max(np.abs(_adjoint(c) @ b @ c - np.eye(len(e))))))
    return _result(e, c, info, return_info)


def _random_basis(n, rank, seed):
    random = np.random.default_rng(seed)
    # Complex Hermitian perturbations cover general real symmetric pencils too.
    z = random.normal(size=(n, rank)) + 1j * random.normal(size=(n, rank))
    return qr(z, mode="economic")[0]


def _physical_roots(a, b, roots, left, right, residual_tolerance, metric_tolerance):
    finite = roots[1] != 0
    values = np.full(len(finite), complex(np.inf), dtype=complex)
    values[finite] = roots[0, finite] / roots[1, finite]
    residual = np.full(len(finite), np.inf)
    left_residual = residual.copy()
    residual[finite] = eigenpair_residuals(a, b, values[finite], right[:, finite])
    left_residual[finite] = eigenpair_residuals(a, b, values[finite].conj(), left[:, finite])
    norms = np.sum(right.conj() * (b @ right), axis=0).real
    # These absolute filters deliberately contain no |lambda| or ||A|| scaling.
    keep = (finite & (np.abs(values.imag) <= residual_tolerance)
            & (residual <= residual_tolerance * vec_norms(right, axis=0))
            & (left_residual <= residual_tolerance * vec_norms(left, axis=0))
            & (norms > metric_tolerance))
    return values.real, keep, residual, norms


def _regular_eigh(a, b):
    try:
        e, c = eigh(_hermitian(a), _hermitian(b))
        c = c / vec_norms(c, axis=0)[None, :]
        return np.vstack([e, np.ones_like(e)]), c, c
    except np.linalg.LinAlgError:
        return eig(a, b, left=True, right=True, homogeneous_eigvals=True)


def _rank_eigh(a, b, normal_rank, method, states, seed, equilibrate,
               residual_tolerance, metric_tolerance, perturbation_scale,
               prescribed_values, return_info):
    a, b = _pencil(a, b)
    an, bn, scale = _equilibrate(a, b, equilibrate)
    n = len(b)
    if not 0 < normal_rank <= n or int(normal_rank) != normal_rank:
        raise ValueError("normal_rank must be a positive integer <= dimension")
    if residual_tolerance <= 0 or metric_tolerance < 0:
        raise ValueError("positive residual tolerance and nonnegative metric tolerance required")
    if method == "projection":
        w = _random_basis(n, normal_rank, seed)
        roots, left, right = _regular_eigh(_adjoint(w) @ an @ w, _adjoint(w) @ bn @ w)
        left, right = w @ left, w @ right
        u = None
    else:
        nullity = n - normal_rank
        u = _random_basis(n, nullity, seed)
        if perturbation_scale <= 0:
            raise ValueError("positive perturbation scale required")
        positive = bn.diagonal().real > 0
        anchor = (np.min(an.diagonal().real[positive] / bn.diagonal().real[positive])
                  if np.any(positive) else 0.)
        prescribed = (anchor + np.random.default_rng(seed).normal(size=nullity)
                      if prescribed_values is None else np.asarray(prescribed_values))
        if prescribed.shape != (nullity,):
            raise ValueError("one prescribed root per missing rank required")
        roots, left, right = _regular_eigh(an + perturbation_scale * (u * prescribed) @ _adjoint(u),
                                          bn + perturbation_scale * u @ _adjoint(u))
    values, keep, residual, norms = _physical_roots(
        an, bn, roots, left, right, residual_tolerance, metric_tolerance)
    if u is not None and u.shape[1]:
        keep &= ((vec_norms(_adjoint(u) @ right, axis=0) <= metric_tolerance)
                 & (vec_norms(_adjoint(u) @ left, axis=0) <= metric_tolerance))
    indices = np.flatnonzero(keep)
    indices = indices[np.argsort(values[indices])]
    if states is not None:
        _subset(states, len(indices))
        indices = indices[:states]
    c = right[:, indices] * (scale[:, None] / np.sqrt(norms[indices])[None, :])
    e = values[indices]
    info = dict(normal_rank=normal_rank, returned_roots=len(e), rank=normal_rank,
                candidate_residuals=residual, accepted=keep, method=method,
                residual_norms=eigenpair_residuals(a, b, e, c))
    if len(e):
        info['metric_error'] = float(np.max(np.abs(_adjoint(c) @ b @ c - np.eye(len(e)))))
    return _result(e, c, info, return_info)


def rank_projection_eigh(a, b, normal_rank, states=None, seed=None,
                         equilibrate=True, residual_tolerance=1e-8,
                         metric_tolerance=1e-10, return_info=False):
    """Hermitian random rank projection, with full-pencil left/right residual tests.

    Requires the pencil's normal rank as input (Hochstenbach/Mehl/Plestenjak,
    2024). Returns finite real roots with positive original-metric norm. An
    approximate rank for a nearly singular pencil does not have the exact-rank
    theorem's guarantees. No automatic energy-dependent rank inference is used.
    """
    return _rank_eigh(a, b, normal_rank, "projection", states, seed, equilibrate,
                      residual_tolerance, metric_tolerance, None, None, return_info)


def rank_completion_eigh(a, b, normal_rank, states=None, seed=None,
                         equilibrate=True, residual_tolerance=1e-8,
                         metric_tolerance=1e-10, perturbation_scale=1.,
                         prescribed_values=None, return_info=False):
    """Hermitian rank completion and filtering of prescribed/random eigenvalues.

    Uses complex random U and U* right/left-vector tests in addition to residuals.
    `prescribed_values` belong to an artificial perturbation, not a potential
    zero or an energy window for accepting physical roots. Same rank limitation
    and positive-metric output convention as rank_projection_eigh.
    """
    return _rank_eigh(a, b, normal_rank, "completion", states, seed, equilibrate,
                      residual_tolerance, metric_tolerance, perturbation_scale,
                      prescribed_values, return_info)

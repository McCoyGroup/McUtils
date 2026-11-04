"""Stable symmetric/Hermitian generalized eigenproblem tools.

All eigensolvers return (values, column vectors); return_info=True appends a
diagnostic dictionary. Geometric Cholesky and absolute iterative tolerances
are independent of matrix dimension and Hamiltonian energy origin. FH retains
its original relative spectral perturbation model. Singular-pencil random
methods require an explicit normal rank; they do not infer it from A's zero.
"""
import numpy as np
from scipy.linalg import cholesky, eigh, eig, qr, lapack, solve_triangular

from .VectorOps import vec_norms

__all__ = [
    "eigenpair_residuals",
    "ritz_eigh",
    "cholesky_orthogonalize",
    "shifted_preconditioner",
    "pivoted_cholesky",
    "cholesky_eigh",
    "robust_lobpcg",
    "SingularPencilError",
    "fix_heiberger",
    "rank_projection_eigh",
    "rank_completion_eigh",
    "generalized_eigh",
]


# --------------------------------------------------------------------------------------------- #
#  shared metric and Ritz operations
# --------------------------------------------------------------------------------------------- #

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


# --------------------------------------------------------------------------------------------- #
#  overlap selection by Cholesky factorization
# --------------------------------------------------------------------------------------------- #

def pivoted_cholesky(matrix, tolerance=1e-10, max_rank=None, method="greedy",
                     block_size=32, seed=None, return_info=False):
    """Factor a PSD matrix as F F*, stopping at max residual diagonal <= tolerance.

    Random pivots use residual-diagonal probabilities. Accelerated random pivots
    use block proposals and rejection sampling (Epperly, Tropp, Webber, 2024).
    The accelerated method checks tolerance after each accepted block. `matrix`
    is unscaled: normalize its diagonal first for a per-function error criterion.
    Returns (factor, pivots), optionally followed by diagnostics.
    """
    matrix = np.asarray(matrix)
    a = _hermitian(np.asarray(matrix, dtype=np.result_type(matrix.dtype, float)))
    n = len(a)
    if a.ndim != 2 or a.shape != (n, n) or not np.isfinite(a).all():
        raise ValueError("finite square matrix required")
    limit = n if max_rank is None else min(n, int(max_rank))
    if tolerance < 0 or limit < 0 or block_size < 1:
        raise ValueError("nonnegative tolerance/rank and positive block size required")
    diagonal = a.diagonal().real.copy()
    if np.min(diagonal, initial=0) < -tolerance:
        raise np.linalg.LinAlgError("negative metric diagonal")
    if method == "greedy":
        routine = lapack.get_lapack_funcs("pstrf", (a,))
        packed, pivots, rank, status = routine(a, tol=tolerance, lower=True)
        if status < 0:
            raise ValueError("invalid pivoted Cholesky argument")
        rank = min(rank, limit)
        pivots = pivots - 1  # LAPACK uses one-based permutations.
        factor = np.empty((n, rank), dtype=a.dtype)
        factor[pivots] = np.tril(packed[:, :rank])
        selected = pivots[:rank]
        diagonal -= vec_norms(factor, axis=1)**2
        proposed = rank
    elif method in {"random", "accelerated"}:
        random = np.random.default_rng(seed)
        factor = np.empty((n, limit), dtype=a.dtype)
        selected, proposed = [], 0
        diagonal = np.maximum(diagonal, 0)
        while len(selected) < limit and np.max(diagonal, initial=0) > tolerance:
            rank = len(selected)
            width = 1 if method == "random" else min(block_size, limit - rank)
            proposals = random.choice(n, size=width, p=diagonal / diagonal.sum())
            proposed += width
            residual = a[np.ix_(proposals, proposals)].copy()
            if rank:
                old = factor[proposals, :rank]
                residual -= old @ _adjoint(old)
            local = np.zeros((width, width), dtype=a.dtype)
            accepted = []
            for j in range(width):
                if proposals[j] in proposals[accepted]:
                    continue
                k = len(accepted)
                value = float(residual[j, j].real - vec_norms(local[j, :k])**2)
                # Repeated proposals have zero conditional variance.
                if value <= 0 or (method == "accelerated" and
                                 random.random() * diagonal[proposals[j]] >= value):
                    continue
                column = residual[:, j] - local[:, :k] @ local[j, :k].conj()
                local[:, k] = column / np.sqrt(value)
                accepted.append(j)
            if not accepted:
                continue
            pivots = proposals[accepted]
            columns = a[:, pivots].copy()
            if rank:
                columns -= factor[:, :rank] @ _adjoint(factor[pivots, :rank])
            added = _adjoint(solve_triangular(local[accepted, :len(accepted)],
                                             _adjoint(columns), lower=True))
            factor[:, rank:rank + len(accepted)] = added
            selected.extend(pivots.tolist())
            diagonal -= vec_norms(added, axis=1)**2
            if np.min(diagonal, initial=0) < -tolerance:
                raise np.linalg.LinAlgError("matrix is not positive semidefinite at this tolerance")
            diagonal = np.maximum(diagonal, 0)
            diagonal[selected] = 0
        factor = factor[:, :len(selected)]
        selected = np.array(selected, dtype=int)
    else:
        raise ValueError(f"unknown Cholesky method {method!r}")
    if np.min(diagonal, initial=0) < -tolerance:
        raise np.linalg.LinAlgError("matrix is not positive semidefinite at this tolerance")
    residual = float(np.max(diagonal, initial=0))
    info = dict(rank=len(selected), pivots=selected, residual_diagonal=diagonal,
                maximum_residual=residual, tolerance=tolerance,
                converged=residual <= tolerance, proposed_pivots=proposed, method=method)
    return _result(factor, selected, info, return_info)


def cholesky_eigh(a, b, states=None, tolerance=1e-10, method="greedy",
                  equilibrate=True, return_info=False, **options):
    """Select normalized functions and solve the original reduced pencil."""
    a, b = _pencil(a, b)
    an, bn, scale = _equilibrate(a, b, equilibrate)
    _, pivots, info = pivoted_cholesky(bn, tolerance=tolerance, method=method,
                                      return_info=True, **options)
    if not len(pivots):
        return _result(np.empty(0), np.empty((len(b), 0)), info, return_info)
    selected = np.ix_(pivots, pivots)
    h, l = _whiten(an[selected], bn[selected])
    e, u = eigh(h, subset_by_index=_subset(states, len(h)))
    c = np.zeros((len(b), len(e)), dtype=u.dtype)
    c[pivots] = scale[pivots, None] * solve_triangular(_adjoint(l), u, lower=False)
    return _result(e, c, info, return_info)


# --------------------------------------------------------------------------------------------- #
#  robust LOBPCG
# --------------------------------------------------------------------------------------------- #

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


# --------------------------------------------------------------------------------------------- #
#  Fix-Heiberger and singular-pencil reductions
# --------------------------------------------------------------------------------------------- #

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


# --------------------------------------------------------------------------------------------- #
#  solver dispatch
# --------------------------------------------------------------------------------------------- #

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

"""Overlap selection by greedy, random, or accelerated random Cholesky."""
import numpy as np
from scipy.linalg import lapack, solve_triangular, eigh
from ..VectorOps import vec_norms
from .Common import _adjoint, _hermitian, _pencil, _equilibrate, _result, _whiten, _subset

__all__ = ["pivoted_cholesky", "cholesky_eigh"]


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

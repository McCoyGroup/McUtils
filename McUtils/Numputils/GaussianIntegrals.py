"""Gaussian polynomial averages grouped by Taylor order about a supplied center."""
import functools
import numpy as np
from .Misc import is_int
from ..Misc import njit

__all__ = ['gaussian_polynomial_integral']


@functools.lru_cache(maxsize=32)
def _gaussian_polynomial_layout(powers):
    # Build the required moments first; every recurrence dependency has lower degree.
    ndim = len(powers[0]) if powers else 0
    zero = (0,) * ndim
    needed = set(powers) | {zero}
    pending = list(powers)
    while pending:
        power = pending.pop()
        if not any(power):
            continue
        axis = next(i for i, p in enumerate(power) if p)
        previous = list(power); previous[axis] -= 1
        dependencies = [tuple(previous)]
        for other, count in enumerate(previous):
            if count:
                reduced = previous.copy(); reduced[other] -= 1
                dependencies.append(tuple(reduced))
        for dependency in dependencies:
            if dependency not in needed:
                needed.add(dependency); pending.append(dependency)
    ordered = sorted(needed, key=lambda p: (sum(p), p))
    lookup = {p: i for i, p in enumerate(ordered)}
    first = np.zeros(len(ordered), dtype=np.intp)
    parent = np.zeros(len(ordered), dtype=np.intp)
    second = np.full((len(ordered), ndim), -1, dtype=np.intp)
    for index, power in enumerate(ordered[1:], 1):
        axis = next(i for i, p in enumerate(power) if p)
        first[index] = axis
        previous = list(power); previous[axis] -= 1
        parent[index] = lookup[tuple(previous)]
        for other, count in enumerate(previous):
            if count:
                reduced = previous.copy(); reduced[other] -= 1
                second[index, other] = lookup[tuple(reduced)]
    return (np.asarray(ordered, dtype=np.intp), first, parent, second,
            np.asarray([lookup[p] for p in powers], dtype=np.intp))


@njit(cache=True)
def _gaussian_polynomial_integral(coefficients, centers, shifts, covariances,
                                  powers, first, parent, second, requested, degree):
    output = np.zeros((len(centers), degree + 1), dtype=coefficients.dtype)
    step = 1 if np.any(shifts) else 2
    for point in range(len(centers)):
        moments = np.zeros((len(powers), degree + 1), dtype=coefficients.dtype)
        moments[0, 0] = 1
        # Coefficients of t**order in E[(center + t*shift + t*Z)**powers], Z ~ N(0, C).
        for index in range(1, len(powers)):
            axis, previous = first[index], parent[index]
            for order in range(0, min(degree, np.sum(powers[index])) + 1, step):
                value = centers[point, axis] * moments[previous, order]
                if order:
                    value += shifts[point, axis] * moments[previous, order - 1]
                if order >= 2:
                    for other in range(centers.shape[1]):
                        reduced = second[index, other]
                        if reduced >= 0:
                            value += (covariances[point, axis, other] * powers[previous, other]
                                      * moments[reduced, order - 2])
                moments[index, order] = value
        for term, index in enumerate(requested):
            for order in range(degree + 1):
                output[point, order] += coefficients[point, term] * moments[index, order]
    return output


def gaussian_polynomial_integral(powers, coefficients, means, covariances,
                                expansion_degree=None, expansion_center=None,
                                return_expansion=False):
    """Average a polynomial over normalized, possibly correlated Gaussians.

    ``powers`` has shape (terms, dimension); ordinary monomial coefficients
    have shape (..., terms), means (..., dimension), and covariances
    (..., dimension, dimension). Their leading axes broadcast. Extra value
    axes can be broadcast explicitly into means and covariances.

    Contributions are grouped by Taylor degree about ``expansion_center``
    (the Gaussian mean by default). Truncation does not truncate the input
    polynomial's degree. A displaced center also allows complex means from
    plane-wave factors, including odd Taylor orders. With center == mean,
    only degree 2*k contributes and k counts covariance pairings.

    Return the sum, or contributions of shape (..., expansion_degree + 1).
    The complete integral is exact when no degree is supplied. No overlap or
    Gaussian normalization factor is included. Zero polynomial terms and
    repeated or non-downward-closed exponent lists are supported.
    """
    powers = np.asarray(powers)
    if (powers.ndim != 2 or not np.issubdtype(powers.dtype, np.integer)
            or np.any(powers < 0) or powers.shape[1] == 0):
        raise ValueError('powers must be a nonnegative integer (terms, dimension) array')
    coefficients, means, covariances = map(np.asarray, (coefficients, means, covariances))
    ndim = powers.shape[1]
    if coefficients.ndim == 0 or coefficients.shape[-1] != len(powers):
        raise ValueError('the final coefficient axis must match the polynomial terms')
    if means.ndim == 0 or means.shape[-1] != ndim or covariances.shape[-2:] != (ndim, ndim):
        raise ValueError('mean and covariance dimensions must match powers')
    degree = int(np.max(np.sum(powers, axis=1), initial=0))
    if expansion_degree is not None:
        if not is_int(expansion_degree) or expansion_degree < 0:
            raise ValueError('expansion_degree must be a nonnegative integer')
        degree = int(expansion_degree)
    center = means if expansion_center is None else np.asarray(expansion_center)
    if center.ndim == 0 or center.shape[-1] != ndim:
        raise ValueError('expansion_center must have the coordinate dimension last')
    batch = np.broadcast_shapes(coefficients.shape[:-1], means.shape[:-1],
                                covariances.shape[:-2], center.shape[:-1])
    dtype = np.result_type(coefficients, means, covariances, center, float)
    coefficients = np.broadcast_to(coefficients.astype(dtype, copy=False), batch + (len(powers),))
    means = np.broadcast_to(means.astype(dtype, copy=False), batch + (ndim,))
    center = np.broadcast_to(center.astype(dtype, copy=False), batch + (ndim,))
    covariances = np.broadcast_to(covariances.astype(dtype, copy=False), batch + (ndim, ndim))
    if len(powers) == 0:
        values = np.zeros(batch + (degree + 1,), dtype=dtype)
    else:
        layout = _gaussian_polynomial_layout(tuple(map(tuple, powers)))
        values = _gaussian_polynomial_integral(
            coefficients.reshape(-1, len(powers)), center.reshape(-1, ndim),
            (means - center).reshape(-1, ndim), covariances.reshape(-1, ndim, ndim),
            *layout, degree).reshape(batch + (degree + 1,))
    return values if return_expansion else values.sum(axis=-1)

"""
A module of useful math for handling coordinate transformations and things
"""
from __future__ import annotations
import enum
import itertools
import math

import numpy as np
from . import Misc as util
from .Options import Options

__all__ = [
    "vec_dots",
    "vec_handle_zero_norms",
    "vec_apply_zero_threshold",
    "vec_normalize",
    "vec_rescale",
    "vec_norms",
    "vec_tensordot",
    "vec_tensordiag",
    "vec_block_diag",
    "diag_indices",
    "block_array",
    "vec_tdot",
    "distance_matrix",
    "unembedded_pts_rmsd",
    "points_from_distance_matrix",
    "identity_tensors",
    "block_broadcast_indices",
    "broadcast_constant",
    "semisparse_tensordot",
    "frac_powh",
    "vec_crosses",
    "vec_angles",
    "vec_sins",
    "vec_cos",
    "vec_outer",
    "pts_norms",
    "pts_angles",
    "pts_normals",
    "vec_dihedrals",
    "pts_dihedrals",
    "pts_book_angles",
    "mat_vec_muls",
    "one_pad_vecs",
    "affine_multiply",
    "cartesian_from_rad",
    "polar_to_cartesian",
    "apply_by_coordinates",
    "apply_by_structures",
    "find_basis",
    "projection_matrix",
    "orthogonal_projection_matrix",
    "project_onto",
    "project_out",
    "fractional_power",
    "unitarize_transformation",
    "maximum_similarity_transformation",
    "polar_decomposition",
    "matrix_transform_from_eigs",
    "symmetric_matrix_exp",
    "imaginary_symmetric_matrix_exp",
    "symmetric_matrix_log",
    "imaginary_symmetric_matrix_log",
    "sylvester_solve",
    "symmetrize_array",
    "integer_exponent"
]

##
# TODO: The design of a lot of this stuff needs a bit of work
#       Like should it work with things that aren't just stacks of vectors?
#       Or should it all be specifically for vector-vector operations?
#       Lots of it doesn't even make sense in a non-vector context...
#       But then there's also like "vec_tensordot" which is explicitly non-vector in scope...
#       Not sure what exactly I want with this. Lots of stuff TBD.

################################################
#
#       vec_dots
#
def vec_dots(vecs1, vecs2, axis=-1):
    """
    Computes the pair-wise dot product of two lists of vecs using np.matmul

    :param vecs1:
    :type vecs1:
    :param vecs2:
    :type vecs2:
    """

    vecs1 = np.expand_dims(vecs1, axis-1)
    vecs2 = np.expand_dims(vecs2, axis)
    res = np.matmul(vecs1, vecs2)
    res_shape = res.shape

    for _ in range(2):
        if res_shape[axis] == 1:
            res = res.reshape(np.delete(res_shape, axis))
            res_shape = res.shape

    return res

################################################
#
#       vec_norms
#
def vec_norms(vecs, axis=-1):
    """

    :param vecs:
    :type vecs: np.ndarray
    :param axis:
    :type axis: int
    :return:
    :rtype:
    """
    # if axis != -1:
    #     raise NotImplementedError("Norm along not-the-last axis not there yet...")
    return np.linalg.norm(vecs, axis=axis)

def points_from_distance_matrix(dist_mat, test_idx=None, target_dim=None, use_triu=False, zero_cutoff=1e-8):
    """
    **LLM Docstring**

    Reconstruct a set of point coordinates that reproduce a given pairwise
    distance matrix (classical multidimensional scaling).

    The distance matrix is squared and double-centered (or centered on `test_idx`
    when supplied) to form the Gram matrix, which is diagonalized; the positive
    eigenvalues and their eigenvectors give the embedded coordinates. Distances may
    be passed as a dense matrix or as the flattened upper triangle (`use_triu`), and
    the output can be zero-padded up to `target_dim`.

    :param dist_mat: pairwise distances (dense matrix or flattened upper triangle)
    :type dist_mat: np.ndarray
    :param test_idx: reference point to center on (double-centering if omitted)
    :type test_idx: int | None
    :param target_dim: dimension to zero-pad the coordinates up to
    :type target_dim: int | None
    :param use_triu: whether `dist_mat` is a flattened upper triangle
    :type use_triu: bool
    :param zero_cutoff: eigenvalue cutoff for counting significant dimensions
    :type zero_cutoff: float
    :return: the reconstructed point coordinates
    :rtype: np.ndarray
    """
    dist_mat = np.asanyarray(dist_mat)
    if use_triu:
        #TODO: make this into a func
        n = int(1 + np.sqrt(1 + 8 * dist_mat.shape[-1])) // 2
        dm = np.zeros(dist_mat.shape[:-1] + (n, n), dtype=dist_mat.dtype)
        row, col = np.triu_indices(n, k=1)
        dm[..., row, col] = dist_mat
        dm[..., col, row] = dist_mat
        dist_mat = dm
    d2 = dist_mat ** 2
    if test_idx is not None:
        dd = (d2[..., test_idx, :, np.newaxis] + d2[..., test_idx, np.newaxis, :] - d2[..., :, :])/2
    else:
        n = dist_mat.shape[-1]
        base_shape = d2.shape[:-2]
        c = identity_tensors(base_shape, n) - 1/n * np.ones(base_shape + (n, n))
        dd = -1/2 * (c @ d2 @ c)
    s, u = np.linalg.eigh(dd)
    ndim = np.max(np.sum(s > zero_cutoff, axis=-1))
    vecs = u[..., :, -ndim:] * np.sqrt(s[..., np.newaxis, -ndim:])
    if target_dim is not None and ndim < target_dim:
        vecs = np.concatenate([
            vecs,
            np.zeros(vecs.shape[:-1] + (target_dim - vecs.shape[-1],), dtype=vecs.dtype)
            ], axis=-1)

    return vecs

def distance_matrix(pts, axis=-1, axis2=None, return_triu=False, return_indices=False, return_diffs=False):
    """
    **LLM Docstring**

    Compute the matrix of pairwise distances between a set of points.

    Distances are formed from the upper-triangular pairs and scattered into a
    symmetric matrix (or returned as the compact upper triangle when `return_triu`).
    The pair indices and/or the raw difference vectors can optionally be returned
    alongside the distances.

    :param pts: the points, with the coordinate axis given by `axis`
    :type pts: np.ndarray
    :param axis: axis holding each point's Cartesian components
    :type axis: int
    :param axis2: axis enumerating the points (defaults to `axis - 1`)
    :type axis2: int | None
    :param return_triu: return the compact upper triangle instead of a full matrix
    :type return_triu: bool
    :param return_indices: also return the `(rows, cols)` pair indices
    :type return_indices: bool
    :param return_diffs: also return the difference vectors
    :type return_diffs: bool
    :return: the distances (plus indices/diffs if requested)
    :rtype: np.ndarray | tuple
    """
    pts = np.asanyarray(pts)
    if axis2 is None:
        axis2 = axis-1

    n = pts.shape[axis2]
    rows, cols = np.triu_indices(n, k=1)
    vecs_r = np.take(pts, rows, axis=axis2)
    vecs_c = np.take(pts, cols, axis=axis2)

    diffs = vecs_r - vecs_c
    dists = vec_norms(diffs, axis=axis)
    if return_triu:
        if return_indices:
            res = dists, (rows, cols)
        else:
            res = (dists,)
    else:
        dist_mats = np.zeros(tuple(np.delete(pts.shape, [axis, axis2])) + (n, n), dtype=dists.dtype)
        dist_mats[..., rows, cols] = dists
        dist_mats[..., cols, rows] = dists
        #TODO: handle transposition
        res = (dist_mats,)
    if return_diffs:
        res = res + (diffs,)

    if len(res) == 1:
        res = res[0]
    return res

def unembedded_pts_rmsd(coords, ref, return_diffs=False, averaged=False, total=False):
    """
    **LLM Docstring**

    Compute the RMSD between a set of coordinates and a reference *without* first
    aligning (embedding) them.

    The straight coordinate difference norm is taken; when `total` is set the norm
    is divided by `sqrt(n_atoms)` (or `sqrt(n_atoms * 3)` unless `averaged`) to give
    a per-atom value. The raw difference vectors can optionally be returned.

    :param coords: the coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param ref: the reference coordinates
    :type ref: np.ndarray
    :param return_diffs: also return the difference vectors
    :type return_diffs: bool
    :param averaged: normalize by `sqrt(n_atoms)` rather than `sqrt(3 * n_atoms)`
    :type averaged: bool
    :param total: whether to apply the per-atom normalization
    :type total: bool
    :return: the RMSD (plus diffs if requested)
    :rtype: np.ndarray | tuple
    """
    coords = np.asanyarray(coords)
    ref = np.asanyarray(ref)

    base_shape = coords.shape[:-2]

    ncoords = np.prod(ref.shape[-2:], dtype=int)

    base_ref = ref.shape[-2:]
    ref = ref.reshape((-1, ncoords))
    coords = coords.reshape((-1, ncoords))

    diffs = ref - coords
    base_rmsd = np.linalg.norm(diffs, axis=-1).reshape(base_shape)
    if total:
        if averaged:
            base_rmsd = base_rmsd / np.sqrt(base_ref[-2])
        else:
            base_rmsd = base_rmsd / np.sqrt(np.prod(base_ref))

    if return_diffs:
        return base_rmsd, diffs.reshape(base_shape + base_ref)
    else:
        return base_rmsd

################################################
#
#       vec_normalize
#
def vec_apply_zero_threshold(vecs, zero_thresh=None, return_zeros=False):
    """
    Applies a threshold to cast nearly-zero vectors to proper zero

    :param vecs:
    :type vecs:
    :param zero_thresh:
    :type zero_thresh:
    :return:
    :rtype:
    """
    norms = vec_norms(vecs)
    vecs, zeros = vec_handle_zero_norms(vecs, norms, zero_thresh=zero_thresh)
    norms = norms[..., np.newaxis]
    norms[zeros] = Options.zero_placeholder

    if return_zeros:
        return vecs, norms, zeros
    else:
        return vecs, norms

def vec_handle_zero_norms(vecs, norms, axis=-1, zero_thresh=None):
    """
    Tries to handle zero-threshold application to vectors

    :param vecs:
    :type vecs:
    :param norms:
    :type norms:
    :param zero_thesh:
    :type zero_thesh:
    :return:
    :rtype:
    """
    norms = np.expand_dims(norms, axis)
    zero_thresh = Options.norm_zero_threshold if zero_thresh is None else zero_thresh
    zeros = np.abs(norms) < zero_thresh
    vecs = vecs * (1 - zeros.astype(int))
    return vecs, zeros

def vec_normalize(vecs, norms=None, axis=-1, zero_thresh=None, return_norms=False):
    """

    :param vecs:
    :type vecs: np.ndarray
    :param axis:
    :type axis: int
    :return:
    :rtype:
    """
    if norms is None:
        norms = vec_norms(vecs, axis=axis)
    vecs, zeros = vec_handle_zero_norms(vecs, norms, axis=axis, zero_thresh=zero_thresh)
    e_norms = np.expand_dims(norms, axis)
    e_norms[zeros] = Options.zero_placeholder # since we already zeroed out the vector

    if return_norms:
        return vecs/e_norms, norms
    else:
        return vecs/e_norms

def vec_rescale(vecs, target_range=None, cur_range=None, midpoint=None, axis=-1, clip=False):
    """
    **LLM Docstring**

    Linearly rescale values from their current range onto a target range.

    The current range is inferred from the data (optionally symmetrized about
    `midpoint`) unless supplied explicitly. Values are mapped to `[0, 1]` and then
    onto `target_range` (a scalar upper bound or a `(min, max)` pair), with optional
    clipping to the target interval.

    :param vecs: the values to rescale
    :type vecs: np.ndarray
    :param target_range: destination range (scalar max, or `(min, max)`)
    :type target_range: float | tuple | None
    :param cur_range: explicit source range `(min, max)` (inferred if omitted)
    :type cur_range: tuple | None
    :param midpoint: value to symmetrize the inferred source range about
    :type midpoint: float | None
    :param axis: axis along which to infer the range
    :type axis: int
    :param clip: whether to clip the result to the target range
    :type clip: bool
    :return: the rescaled values
    :rtype: np.ndarray
    """
    vecs = np.asanyarray(vecs)
    if cur_range is None:
        cur_mins = np.expand_dims(np.min(vecs, axis=axis), axis)
        cur_max = np.expand_dims(np.max(vecs, axis=axis), axis)
        if midpoint is not None:
            min_diff = midpoint - cur_mins
            max_diff = cur_max - midpoint
            abs_diff = np.max([np.abs(min_diff), max_diff], axis=0)
            cur_mins = midpoint - abs_diff
            cur_range = 2 * abs_diff
        else:
            cur_range = cur_max - cur_mins
    else:
        cur_mins = cur_range[0]
        cur_range = cur_range[1] - cur_range[0]
    rescaled = (vecs - cur_mins) / cur_range
    if target_range is not None:
        if util.is_numeric(target_range):
            rescaled = rescaled * target_range
        else:
            t_min, t_max = target_range
            if not util.is_numeric(t_min):
                t_min = np.expand_dims(np.asanyarray(t_min), axis)
            if not util.is_numeric(t_max):
                t_max = np.expand_dims(np.asanyarray(t_max), axis)
            rescaled = rescaled*(t_max - t_min) + t_min
        if clip:
            rescaled = np.clip(rescaled, *target_range)
    elif clip:
        rescaled = np.clip(rescaled, 0, 1)
    return rescaled

################################################
#
#       vec_crosses
#

def vec_crosses(vecs1, vecs2, normalize=False, zero_thresh=None, axis=-1):
    """
    **LLM Docstring**

    Compute the cross products of two stacks of vectors, optionally normalizing the
    results.

    When `normalize` is set the cross products are divided by their norms, with
    near-zero norms (below `zero_thresh`, defaulting to `Options.norm_zero_threshold`)
    handled safely so the corresponding results are zeroed rather than producing
    NaNs.

    :param vecs1: first stack of vectors
    :type vecs1: np.ndarray
    :param vecs2: second stack of vectors
    :type vecs2: np.ndarray
    :param normalize: whether to normalize the cross products
    :type normalize: bool
    :param zero_thresh: norm below which a result is treated as zero
    :type zero_thresh: float | None
    :param axis: axis holding the vector components
    :type axis: int
    :return: the (optionally normalized) cross products
    :rtype: np.ndarray
    """
    crosses = np.cross(vecs1, vecs2, axis=axis)
    if normalize:
        norms = vec_norms(crosses, axis=axis)
        zero_thresh = Options.norm_zero_threshold if zero_thresh is None else zero_thresh
        smol = util.is_numeric(norms)
        if smol:
            bad_norms = norms < zero_thresh
            if bad_norms:
                norms = np.array(1.)
        else:
            bad_norms = np.where(norms <= zero_thresh)
            norms[bad_norms] = 1.

        crosses = crosses/norms[..., np.newaxis]

        if smol:
            if bad_norms:
                crosses *= 0.
        else:
            crosses[bad_norms] *= 0.

    return crosses

################################################
#
#       vec_cos
#
def vec_cos(vectors1, vectors2, zero_thresh=None, axis=-1):
    """Gets the cos of the angle between two vectors

    :param vectors1:
    :type vectors1: np.ndarray
    :param vectors2:
    :type vectors2: np.ndarray
    """
    dots   = vec_dots(vectors1, vectors2, axis=axis)
    norms1 = vec_norms(vectors1, axis=axis)
    norms2 = vec_norms(vectors2, axis=axis)

    norm_prod = norms1 * norms2
    if isinstance(norm_prod, np.ndarray):
        zero_thresh = Options.norm_zero_threshold if zero_thresh is None else zero_thresh
        bad_norm_prods = np.where(np.abs(norm_prod) <= zero_thresh)
        norm_prod[bad_norm_prods] = 1.

    coses = dots/(norms1*norms2)

    if isinstance(norm_prod, np.ndarray):
        coses[bad_norm_prods] = 0.

    return coses

################################################
#
#       vec_sins
#
def vec_sins(vectors1, vectors2, zero_thresh=None, axis=-1):
    """Gets the sin of the angle between two vectors

    :param vectors1:
    :type vectors1: np.ndarray
    :param vectors2:
    :type vectors2: np.ndarray
    """
    crosses= vec_crosses(vectors1, vectors2, axis=axis)
    norms1 = vec_norms(vectors1, axis=axis)
    norms2 = vec_norms(vectors2, axis=axis)

    norm_prod = norms1 * norms2
    if isinstance(norm_prod, np.ndarray):
        zero_thresh = Options.norm_zero_threshold if zero_thresh is None else zero_thresh
        bad_norm_prods = np.where(np.abs(norm_prod) <= zero_thresh)
        norm_prod[bad_norm_prods] = 1.

    sines = vec_norms(crosses)/norm_prod

    if isinstance(norm_prod, np.ndarray):
        sines[bad_norm_prods] = 0.

    return sines


################################################
#
#       vec_angles
#
def vec_angles(vectors1, vectors2, norms=None, up_vectors=None, zero_thresh=None, axis=-1,
               return_norms=False,
               return_crosses=True,
               return_cross_norms=False,
               check_zeros=True
               ):
    """
    Gets the angles and normals between two vectors

    :param vectors1:
    :type vectors1: np.ndarray
    :param vectors2:
    :type vectors2: np.ndarray
    :param up_vectors: orientation vectors to obtain signed angles
    :type up_vectors: None | np.ndarray
    :return: angles and normals between two vectors
    :rtype: (np.ndarray, np.ndarray)
    """
    vectors1 = np.asanyarray(vectors1)
    vectors2 = np.asanyarray(vectors2)
    if vectors1.shape[axis] == 2:
        vectors1 = vec_normalize(vectors1, axis=axis)
        vectors2 = vec_normalize(vectors2, axis=axis)
        x1 = np.take(vectors1, 0, axis=axis)
        y1 = np.take(vectors1, 1, axis=axis)
        x2 = np.take(vectors2, 0, axis=axis)
        y2 = np.take(vectors2, 1, axis=axis)
        sin = x1 * y2 - x2 * y1
        dots = vec_dots(vectors1, vectors2, axis=axis)
        return np.arctan2(sin, dots)
    else:
        dots = vec_dots(vectors1, vectors2, axis=axis)
        crosses = vec_crosses(vectors1, vectors2, axis=axis)
        if norms is not None:
            norms1, norms2 = norms
        else:
            norms1 = vec_norms(vectors1, axis=axis)
            norms2 = vec_norms(vectors2, axis=axis)
            norms = (norms1, norms2)

        norm_prod = norms1*norms2
        if check_zeros:
            zero_thresh = Options.norm_zero_threshold if zero_thresh is None else zero_thresh
            smol = util.is_numeric(norm_prod)
            if smol:
                bad_norms = norm_prod < zero_thresh
                if bad_norms:
                    norm_prod = np.array(1.)
            else:
                bad_norm_prods = np.where(np.abs(norm_prod) <= zero_thresh)
                norm_prod[bad_norm_prods] = 1.

        cos_comps = dots/norm_prod
        cross_norms = vec_norms(crosses, axis=axis)
        sin_comps = cross_norms/norm_prod

        angles = np.arctan2(sin_comps, cos_comps)

        if check_zeros:
            if smol:
                if bad_norms:
                    angles = np.array(0.)
            else:
                angles[bad_norm_prods] = 0.

        # return signed angles
        if up_vectors is not None:
            if up_vectors.ndim < crosses.ndim:
                up_vectors = np.broadcast_to(up_vectors, crosses.shape[:-len(up_vectors.shape)] + up_vectors.shape)
            orientations = np.sign(vec_dots(up_vectors, crosses))
            angles = orientations * angles

        if return_crosses or return_norms or return_cross_norms:
            ret = (angles,)
            if return_crosses:
                ret = ret + (crosses,)
            if return_norms:
                ret = ret + (norms,)
            if return_cross_norms:
                ret = ret + (cross_norms,)
        else:
            ret = angles

    return ret

################################################
#
#       vec_outer
#
def _vec_outer(a, b, axes=None):
    """
    Provides the outer product of a and b in a vectorized way.
    Currently not entirely convinced I'm doing it right :|

    :param a:
    :type a:
    :param b:
    :type b:
    :param axis:
    :type axis:
    :return:
    :rtype:
    """
    # we'll treat this like tensor_dot:
    #   first we turn this into a plain matrix
    #   then we do the outer on the matrix
    #   then we cast back to the shape we want
    if axes is None:
        if a.ndim > 1:
            axes = [-1, -1]
        else:
            axes = [0, 0]

    # we figure out how we'd conver
    a_ax = axes[0]
    if isinstance(a_ax, (int, np.integer)):
        a_ax = [a_ax]
    a_ax = [ax + a.ndim if ax<0 else ax for ax in a_ax]
    a_leftover = [x for x in range(a.ndim) if x not in a_ax]
    a_transp = a_leftover + a_ax
    a_shape = a.shape
    a_old_shape = [a_shape[x] for x in a_leftover]
    a_subshape = [a_shape[x] for x in a_ax]
    a_contract = a_old_shape + [np.prod(a_subshape)]

    b_ax = axes[1]
    if isinstance(b_ax, (int, np.integer)):
        b_ax = [b_ax]
    b_ax = [ax + b.ndim if ax<0 else ax for ax in b_ax]
    b_leftover = [x for x in range(b.ndim) if x not in b_ax]
    b_transp = b_leftover + b_ax
    b_shape = b.shape
    b_old_shape = [b_shape[x] for x in b_leftover]
    b_subshape = [b_shape[x] for x in b_ax]
    b_contract = b_old_shape + [np.prod(b_subshape)]

    a_new = a.transpose(a_transp).reshape(a_contract)
    b_new = b.transpose(b_transp).reshape(b_contract)

    if b_new.ndim < a_new.ndim:
        ...
    elif a_new.ndim < b_new.ndim:
        ...

    outer = a_new[..., :, np.newaxis] * b_new[..., np.newaxis, :]

    # now we put the shapes right again and revert the transposition
    # base assumption is that a_old_shape == b_old_shape
    # if not we'll get an error anyway
    final_shape = a_old_shape + a_subshape + b_subshape

    res = outer.reshape(final_shape)
    final_transp = np.argsort(a_leftover + a_ax + b_ax)

    return res.transpose(final_transp)

def bump_axes(a_ax, b_ax):
    """
    **LLM Docstring**

    Shift a set of `b` axis indices so they do not collide with the `a` axis
    indices, producing a block layout with the `a` axes first.

    Each `b` index is incremented until it clashes with neither an `a` index nor an
    already-assigned `b` index.

    :param a_ax: the first (fixed) set of axis indices
    :type a_ax: Iterable[int]
    :param b_ax: the axis indices to shift out of collision
    :type b_ax: Iterable[int]
    :return: the shifted `b` axis indices
    :rtype: list[int]
    """
    new_b = []
    for _ in b_ax:  # pad b to get block form (a first, then b)
        while _ in a_ax or _ in new_b:
            _ = _ + 1
        new_b.append(_)
    return new_b
def riffle_axes(a_ax, b_ax):
    """
    **LLM Docstring**

    Interleave two axis-index lists into a collision-free ordering.

    Walks the two lists in parallel; when a `b` index collides with an `a` index it
    is bumped and any downstream duplicates in either list are pushed along to keep
    both orderings strictly increasing.

    :param a_ax: the first set of axis indices
    :type a_ax: Iterable[int]
    :param b_ax: the second set of axis indices
    :type b_ax: Iterable[int]
    :return: the reconciled `(a_axes, b_axes)`
    :rtype: tuple[list[int], list[int]]
    """
    new_b = []
    new_a = []
    a_ax = list(a_ax)
    b_ax = list(b_ax)
    nmax = max(len(b_ax), len(a_ax))
    for n in range(nmax):
        if n < len(b_ax):
            bx = b_ax[n]
            if bx in a_ax:  # hit a collision, need to bump bx, then force a_ax to check for collisions next
                bx = bx + 1
                b_ax[n] = bx
                for m in range(n + 1, len(b_ax)):
                    if b_ax[m] == b_ax[m - 1]:
                        b_ax[m] += 1
                try:
                    bx_ax_pos = a_ax.index(bx)
                except:
                    pass
                else:
                    a_ax[bx_ax_pos] += 1
                    for m in range(bx_ax_pos + 1, len(a_ax)):
                        if a_ax[m] == a_ax[m - 1]:
                            a_ax[m] += 1
            new_b.append(bx)
        if n < len(a_ax):
            new_a.append(a_ax[n])
    return new_a, new_b
def vec_outer(a, b, axes=None, order=2):
    """
    Provides the outer product of a and b in a vectorized way.
    We have to prioritize what goes where, and `order` determines
    if the axes of `a` come first or `b` come first

    :param a:
    :type a:
    :param b:
    :type b:
    :param axis:
    :type axis:
    :return:
    :rtype:
    """
    if axes is None:
        if a.ndim > 1:
            axes = [-1, -1]
        else:
            axes = [0, 0]

    a_ax, b_ax = axes
    if isinstance(a_ax, (int, np.integer)): a_ax = [a_ax]
    if isinstance(b_ax, (int, np.integer)): b_ax = [b_ax]
    a_ax = [a.ndim + x if x < 0 else x for x in a_ax]
    b_ax = [b.ndim + x if x < 0 else x for x in b_ax]

    a_ax = list(np.sort(a_ax))
    b_ax = list(np.sort(b_ax))
    # we resolve axis conflicts, where two axes are mapping to the same spot
    if order == 0: # pad b to get block form (a first, then b)
        b_ax = bump_axes(a_ax, b_ax)
    elif order == 1: # pad a to get block form (b first, then a)
        a_ax = bump_axes(b_ax, a_ax)
    elif order == 2: # pad to get interleaving (a first, then b)
        a_ax, b_ax = riffle_axes(a_ax, b_ax)
    elif order == 3: # pad to get interleaving (a first, then b)
        a_ax, b_ax = riffle_axes(b_ax, a_ax)

    # we expand A and B appropriately now
    a = np.expand_dims(a, b_ax)
    b = np.expand_dims(b, a_ax)

    # and just multipy and let numpy broadcasting do the rest
    return a * b

################################################
#
#       vec_outer
#
def diag_indices(block_shape, n, k=2):
    """
    **LLM Docstring**

    Build the fancy-index tuple that addresses the `k`-fold diagonal of a tensor of
    shape `block_shape + (n,) * k`.

    The leading `block_shape` axes are indexed elementwise while the trailing `k`
    axes share a single `arange(n)` index, so assigning through the result writes
    values along the generalized diagonal.

    :param block_shape: shape of the leading (batch) axes
    :type block_shape: tuple[int, ...]
    :param n: size of each diagonal axis
    :type n: int
    :param k: number of diagonal axes
    :type k: int
    :return: the diagonal index tuple
    :rtype: tuple
    """
    ranges = [np.arange(s, dtype=int) for s in block_shape]
    indexing_shape = []
    m = len(block_shape)
    for i,r in enumerate(ranges):
        r = np.expand_dims(r, list(range(i)))
        r = np.expand_dims(r, [-x for x in range(1, m-i+1)])
        indexing_shape.append(r)
    di = np.expand_dims(np.arange(n, dtype=int), list(range(len(block_shape))))
    return tuple(indexing_shape) + (di,) * k
def vec_tensordiag(obj, axis=-1, extra_dims=1):
    """
    **LLM Docstring**

    Embed an array onto the diagonal of a higher-rank tensor.

    `extra_dims` new axes (each the size of the first post-`axis` dimension) are
    prepended to the trailing block and the input is written along that diagonal via
    `diag_indices`, leaving zeros off-diagonal.

    :param obj: the array to place on the diagonal
    :type obj: np.ndarray
    :param axis: boundary between batch axes and the block to diagonalize
    :type axis: int
    :param extra_dims: number of extra diagonal axes to add
    :type extra_dims: int
    :return: the diagonal-embedded tensor
    :rtype: np.ndarray
    """
    obj = np.asanyarray(obj)
    base_shape = obj.shape[:axis]
    shp = obj.shape[axis:]
    extra_shp = (shp[0],) * extra_dims
    tensor = np.zeros(base_shape + extra_shp + shp, dtype=obj.dtype)
    inds = diag_indices(base_shape, shp[0], k=(extra_dims + 1))
    tensor[inds] = obj
    return tensor
def block_array(blocks, ndim=2, padding=0):
    """
    **LLM Docstring**

    Collapse a nested block array into a single dense array by concatenating the
    outer block axes.

    The leading block axes (those beyond `ndim + padding` trailing axes) are folded
    in one at a time via `np.concatenate`.

    :param blocks: the block array to collapse
    :type blocks: np.ndarray
    :param ndim: number of trailing axes belonging to each block
    :type ndim: int
    :param padding: extra trailing axes to leave untouched
    :type padding: int
    :return: the collapsed dense array
    :rtype: np.ndarray
    """
    blocks = np.asanyarray(blocks)
    for k in range(blocks.ndim-ndim-padding):
        blocks = np.concatenate(blocks, axis=-(k+1))
    return blocks
def vec_block_diag(mats, kroneckerize=True):
    """
    **LLM Docstring**

    Build block-diagonal matrices from a stack of matrices.

    Each stacked matrix is placed on the diagonal of a larger `(stack, stack)`
    block array (via `diag_indices`); when `kroneckerize` is set the block structure
    is flattened into a single dense `(stack * rows, stack * cols)` matrix.

    :param mats: stack of matrices, shape `(..., stack, rows, cols)`
    :type mats: np.ndarray
    :param kroneckerize: whether to flatten the block structure into a dense matrix
    :type kroneckerize: bool
    :return: the block-diagonal matrices
    :rtype: np.ndarray
    """
    mats = np.asanyarray(mats)
    base_shape = mats.shape[:-3]
    stack_shape = mats.shape[-3]
    arr_shape = mats.shape[-2:]
    arr = np.zeros(base_shape + (stack_shape, stack_shape) + arr_shape)
    inds = diag_indices(base_shape, stack_shape, k=2)
    arr[inds] = mats
    if kroneckerize:
        arr = np.moveaxis(arr, -2, -3).reshape(base_shape + (stack_shape*arr_shape[-1], stack_shape*arr_shape[-2]))
    return arr


def identity_tensors(base_shape, ndim):
    """
    **LLM Docstring**

    Return a stack of identity matrices broadcast over a leading batch shape.

    :param base_shape: the leading (batch) shape to broadcast over
    :type base_shape: int | tuple[int, ...]
    :param ndim: the dimension of each identity matrix
    :type ndim: int
    :return: the broadcast identity tensor, shape `base_shape + (ndim, ndim)`
    :rtype: np.ndarray
    """
    eye = np.eye(ndim)
    if util.is_int(base_shape):
        base_shape = [base_shape]
    base_shape = tuple(base_shape)
    return np.broadcast_to(
        np.expand_dims(eye, list(range(len(base_shape)))),
        base_shape + (ndim, ndim)
    )

def block_broadcast_indices(base_pos, block_inds, block_size=None):
    """
    **LLM Docstring**

    Expand a set of base positions into flattened indices spanning a contiguous
    block of size `block_size` around each position.

    Typically used to turn atom indices into the flattened Cartesian indices
    `3 * atom + component`. `block_inds` may be an integer (a full `0..block_inds`
    range) or an explicit set of offsets (in which case `block_size` is required).

    :param base_pos: the base positions (e.g. atom indices)
    :type base_pos: np.ndarray
    :param block_inds: block offsets, or an int giving the block width
    :type block_inds: int | np.ndarray
    :param block_size: stride between base positions (required if offsets given)
    :type block_size: int | None
    :return: the flattened block indices
    :rtype: np.ndarray
    """
    if util.is_int(block_inds):
        if block_size is None:
            block_size = block_inds
        block_inds = np.arange(block_inds)
    else:
        if block_size is None:
            raise ValueError("block size required")
        block_inds = np.asanyarray(block_inds)
    base_pos = np.asanyarray(base_pos)
    return (
        base_pos[..., :, np.newaxis] * block_size
        + block_inds[..., np.newaxis, :]
    ).flatten()

def broadcast_constant(base_array, target_shape, pad_base=False):
    """
    **LLM Docstring**

    Broadcast a scalar or array up to a target shape.

    A scalar is filled into `target_shape`; an array is expanded with leading axes
    so it broadcasts against `target_shape` (with the array's own shape appended
    when `pad_base` is set).

    :param base_array: the value to broadcast
    :type base_array: float | np.ndarray
    :param target_shape: the desired leading shape
    :type target_shape: tuple[int, ...]
    :param pad_base: append the base array's shape to the target shape
    :type pad_base: bool
    :return: the broadcast array
    :rtype: np.ndarray
    """
    if util.is_numeric(base_array):
        return np.full(target_shape, base_array)
    else:
        if pad_base: target_shape = tuple(target_shape) + base_array.shape
        base_array = np.asanyarray(base_array)
        base_array = np.expand_dims(base_array, list(range(len(target_shape) - base_array.ndim)))
        return np.broadcast_to(base_array, target_shape)

#################################################################################
#
#   vec_tensordot
#
def vec_tensordot(tensa, tensb, axes=2, shared=None):
    """Defines a version of tensordot that uses matmul to operate over stacks of things
    Basically had to duplicate the code for regular tensordot but then change the final call

    :param tensa:
    :type tensa:
    :param tensb:
    :type tensb:
    :param axes:
    :type axes: [list[int]|int, list[int]|int] | int
    :param shared: the axes that should be treated as shared (for now just an int)
    :type shared: int | None
    :return:
    :rtype:
    """

    if isinstance(axes, (int, np.integer)):
        axes = (list(range(-axes, 0)), list(range(0, axes)))
    axes_a, axes_b = axes
    try:
        na = len(axes_a)
        axes_a = list(axes_a)
    except TypeError:
        axes_a = [axes_a]
        na = 1
    try:
        nb = len(axes_b)
        axes_b = list(axes_b)
    except TypeError:
        axes_b = [axes_b]
        nb = 1

    a, b = np.asarray(tensa), np.asarray(tensb)

    axes_a = [ax if ax >= 0 else a.ndim + ax for ax in axes_a]
    axes_b = [ax if ax >= 0 else b.ndim + ax for ax in axes_b]
    a_shape = tensa.shape
    b_shape = tensb.shape

    if shared is None:
        shared = 0
        for shared, s in enumerate(zip(a_shape, b_shape)):
            if s[0] != s[1]:
                break
            shared = shared + 1
    # else:

    # the minimum number of possible shared axes
    # is constrained by the contraction of axes
    shared = min([shared, min(axes_a), min(axes_b)])

    if shared == 0: #easier to just delegate here than handle more special cases
        return np.tensordot(a, b, axes=axes)

    as_ = a_shape
    nda = a.ndim
    bs = b.shape
    ndb = b.ndim

    equal = True
    if na != nb:
        equal = False
        raise ValueError("{}: shape-mismatch ({}) and ({}) in number of axes to contract over".format(
            "vec_tensordot",
            na,
            nb
        ))
    else:
        for k in range(na):
            if as_[axes_a[k]] != bs[axes_b[k]]:
                equal = False
                raise ValueError("{}: shape-mismatch ({}) and ({}) in contraction over axes ({}) and ({})".format(
                    "vec_tensordot",
                    axes_a[k],
                    axes_b[k],
                    na,
                    nb
                    ))
            if axes_a[k] < 0:
                axes_a[k] += nda
            if axes_b[k] < 0:
                axes_b[k] += ndb

    # Move the axes to sum over to the end of "a"
    # and to the front of "b"
    # preserve things so that the "shared" stuff remains at the fron of both of these...
    notin_a = [k for k in range(shared, nda) if k not in axes_a]
    newaxes_a = list(range(shared)) + notin_a + axes_a
    N2_a = 1
    for axis in axes_a:
        N2_a *= as_[axis]
    newshape_a = as_[:shared] + (int(np.prod([as_[ax] for ax in notin_a if ax >= shared])), N2_a)
    olda = [as_[axis] for axis in notin_a if axis >= shared]

    notin_b = [k for k in range(shared, ndb) if k not in axes_b]
    newaxes_b = list(range(shared)) + axes_b + notin_b
    N2_b = 1
    for axis in axes_b:
        N2_b *= bs[axis]
    newshape_b = as_[:shared] + (N2_b, int(np.prod([bs[ax] for ax in notin_b if ax >= shared])))
    oldb = [bs[axis] for axis in notin_b if axis >= shared]

    at = a.transpose(newaxes_a).reshape(newshape_a)
    bt = b.transpose(newaxes_b).reshape(newshape_b)
    res = np.matmul(at, bt)
    final_shape = list(a_shape[:shared]) + olda + oldb
    # raise Exception(res.shape, final_shape)
    return res.reshape(final_shape)
def vec_tdot(tensa, tensb, axes=((-1,), (1,))):
    """
    Tensor dot but just along the final axes by default. Totally a convenience function.

    :param tensa:
    :type tensa:
    :param tensb:
    :type tensb:
    :param axes:
    :type axes:
    :return:
    :rtype:
    """

    return vec_tensordot(tensa, tensb, axes=axes)

def semisparse_tensordot(sparse_data, a, /, axes, shared=None):
    """
    **LLM Docstring**

    Contract a sparse tensor (given as `(positions, values, shape)`) with a dense
    array, analogous to `np.tensordot` but exploiting the sparsity.

    The requested `axes` of each operand are aligned (with an optional number of
    `shared` leading batch axes), the sparse positions are flattened into a
    contracted/free index pair, and the contraction is performed either as a single
    `vec_tensordot` (full contraction) or an explicit accumulation over the nonzero
    entries.

    :param sparse_data: the sparse tensor as `(positions, values, shape)`
    :type sparse_data: tuple
    :param a: the dense array to contract against
    :type a: np.ndarray
    :param axes: `(sparse_axes, dense_axes)` to contract
    :type axes: tuple
    :param shared: number of shared leading batch axes
    :type shared: int | None
    :return: the contracted result
    :rtype: np.ndarray
    """
    pos, vals, shape = sparse_data
    a = np.asanyarray(a)
    lv_axes = axes[0]
    a_axes = axes[1]
    if util.is_numeric(lv_axes):
        lv_axes = [lv_axes]
    if util.is_numeric(a_axes):
        a_axes = [a_axes]


    if shared is None:
        shared = 0
    nax = len(lv_axes)
    for ax in reversed(a_axes):
        a = np.moveaxis(a, ax, shared)

    idx = np.setdiff1d(np.arange(len(shape)), lv_axes)

    target_shape = a.shape[:shared] + tuple(shape[i] for i in idx) + a.shape[nax + shared:]

    pos = [pos[i] for i in idx] + [pos[i] for i in lv_axes]
    shape = [shape[i] for i in idx] + [shape[i] for i in lv_axes]
    flat_shape = (np.prod([shape[i] for i in idx], dtype=int), np.prod([shape[i] for i in lv_axes], dtype=int))
    flat_pos = np.array(np.unravel_index(np.ravel_multi_index(pos, shape), flat_shape)).T

    a = np.reshape(a, a.shape[:shared] + (np.prod([a.shape[i+shared] for i in range(nax)], dtype=int), -1))

    # now we can do a form of sparse dot product

    ndim = len(shape) - shared
    if nax == ndim:
        idx = (slice(None),)*shared + (flat_pos,)
        new = vec_tensordot(
            vals,
            a[idx],
            axes=[0, shared]
        )
    else:
        new_shape = a.shape[:shared] + (flat_shape[0],) + a.shape[shared+1:]
        new = np.zeros(new_shape)
        pad_pos = (slice(None),)*shared
        for (i,k),v in zip(flat_pos, vals):
            i = pad_pos + (i,)
            k = pad_pos + (k,)
            new[i] += v * a[k]

    return np.reshape(new, target_shape)


def frac_powh(A, k, eigsys=None, pow=None, nonzero_cutoff=None):
    """
    **LLM Docstring**

    Raise a symmetric/Hermitian matrix to a fractional power via its eigen
    decomposition.

    The matrix is diagonalized with `np.linalg.eigh` (reusing a supplied `eigsys`
    if given), each eigenvalue is raised to the power `k` with `pow`, and the matrix
    is reassembled. A `nonzero_cutoff` treats near-zero eigenvalues as `1` during
    the power and zeros them afterward so they vanish on contraction; non-square
    inputs are padded to square first.

    :param A: the symmetric matrix
    :type A: np.ndarray
    :param k: the exponent
    :type k: float
    :param eigsys: precomputed `(eigenvalues, eigenvectors)` (optional)
    :type eigsys: tuple | None
    :param pow: elementwise power function (defaults to `np.power`)
    :type pow: Callable | None
    :param nonzero_cutoff: eigenvalue magnitude below which values are treated as zero
    :type nonzero_cutoff: float | None
    :return: the fractional matrix power
    :rtype: np.ndarray
    """
    A = np.asanyarray(A)
    if eigsys is None:
        if A.shape[-1] != A.shape[-2] and nonzero_cutoff is not None:
            A = np.pad(A,
                       [
                           [0, max(A.shape[-1] - A.shape[-2], 0)],
                           [0, max(A.shape[-2] - A.shape[-1], 0)]
                       ])
        eigsys = np.linalg.eigh(A)
    eigvals, Q = eigsys
    if pow is None:
        pow = np.power

    if nonzero_cutoff is not None:
        bad_pos = np.abs(eigvals) < nonzero_cutoff
        eigvals[bad_pos] = 1 # always well behaved
        pow_vals = pow(eigvals, k)
        pow_vals[bad_pos] = 0 # vanishes upon contraction
    else:
        pow_vals = pow(eigvals, k)
    # TODO: speed up with semisparse dot products
    if pow_vals.ndim == 1:
        return Q @ np.diag(pow_vals) @ Q.T
    else:
        shared = pow_vals.ndim - 1
        v = vec_tensordiag(pow_vals, extra_dims=shared)
        return vec_tensordot(vec_tensordot(Q, v, axes=[-1, -2], shared=shared), Q, axes=[-1, -2], shared=shared)
################################################
#
#       pts_norms
#
def pts_norms(pts1, pts2, **opts):
    """Provides the distance between the points

    :param pts1:
    :type pts1: np.ndarray
    :param pts2:
    :type pts2: np.ndarray
    :return:
    :rtype: np.ndarray
    """
    return vec_norms(pts2-pts1, **opts)

################################################
#
#       pts_angles
#
def pts_angles(pts1, pts2, pts3, **opts):
    """Provides the vector normal to the plane of the three points

    :param pts1:
    :type pts1: np.ndarray
    :param pts2:
    :type pts2: np.ndarray
    :param pts3:
    :type pts3: np.ndarray
    :return:
    :rtype: np.ndarray
    """
    return vec_angles(pts1-pts2, pts3-pts2, **opts)

################################################
#
#       pts_normals
#
def pts_normals(pts1, pts2, pts3, normalize=True, **opts):
    """Provides the vector normal to the plane of the three points

    :param pts1:
    :type pts1: np.ndarray
    :param pts2:
    :type pts2: np.ndarray
    :param pts3:
    :type pts3: np.ndarray
    :param normalize:
    :type normalize:
    :return:
    :rtype: np.ndarray
    """
    # should I normalize these...?
    return vec_crosses(pts2-pts1, pts3-pts1, normalize=normalize, **opts)

################################################
#
#       vec_dihedrals
#
def vec_dihedrals(b1, b2, b3,
                  crosses=None,
                  norms=None,
                  return_crosses=False
                  ):
    """
    Provides the dihedral angle between pts4 and the plane of the other three vectors

    :param pts1:
    :type pts1: np.ndarray
    :param pts2:
    :type pts2: np.ndarray
    :param pts3:
    :type pts3: np.ndarray
    :return:
    :rtype:
    """

    # # should I normalize these...?
    # normals = pts_normals(pts2, pts3, pts4, normalize=False)
    # off_plane_vecs = pts1 - pts4
    # return vec_angles(normals, off_plane_vecs)[0]

    # compute signed angle between the normals to the b1xb2 plane and b2xb3 plane
    # b1 = pts2-pts1 # 4->1
    # b2 = pts3-pts2 # 1->2
    # b3 = pts4-pts3 # 2->3

    if crosses is not None:
        crosses, cross_norms = crosses
        n1, n2 = crosses
        n1 = vec_normalize(n1, cross_norms[0])
        n2 = vec_normalize(n2, cross_norms[1])
    else:
        n1 = vec_crosses(b1, b2)#, normalize=True)
        n2 = vec_crosses(b2, b3)#, normalize=True)
        norm1 = vec_norms(n1)
        norm2 = vec_norms(n2)
        n1 = vec_normalize(n1, norm1)
        n2 = vec_normalize(n2, norm2)
        crosses = [(n1, n2), (norm1, norm2)]

    if norms is not None:
        nb1, nb2, nb3 = norms
        u2 = vec_normalize(b2, nb2)
    else:
        u2 = vec_normalize(b2)

    m1 = vec_crosses(n1, u2)
    d1 = vec_dots(n1, n2)
    d2 = vec_dots(m1, n2)

    # arctan(d2/d1) + sign stuff from relative signs of d2 and d1
    ret = -np.arctan2(d2, d1)
    if return_crosses:
        ret = (ret, crosses)
    return ret

################################################
#
#       pts_dihedrals
#
def pts_dihedrals(pts1, pts2, pts3, pts4,
                  crosses=None,
                  norms=None,
                  return_crosses=False, **opts
                  ):
    """
    Provides the dihedral angle between pts4 and the plane of the other three vectors

    :param pts1:
    :type pts1: np.ndarray
    :param pts2:
    :type pts2: np.ndarray
    :param pts3:
    :type pts3: np.ndarray
    :return:
    :rtype:
    """

    # b1 = pts2-pts1 # 4->1
    # b2 = pts3-pts2 # 1->2
    # b3 = pts4-pts3 # 2->3

    # # should I normalize these...?
    # normals = pts_normals(pts2, pts3, pts4, normalize=False)
    # off_plane_vecs = pts1 - pts4
    # return vec_angles(normals, off_plane_vecs)[0]

    # compute signed angle between the normals to the b1xb2 plane and b2xb3 plane
    b1 = pts2-pts1 # 4->1
    b2 = pts3-pts2 # 1->2
    b3 = pts4-pts3 # 2->3

    return vec_dihedrals(
        b1, b2, b3,
        crosses=crosses,
        norms=norms,
        return_crosses=return_crosses,
        **opts
    )

def pts_book_angles(pts1, pts2, pts3, pts4,
        crosses=None,
        norms=None,
        return_crosses=False,
        **opts
):
    """
    **LLM Docstring**

    Compute *book* angles from four sets of points.

    Builds the three defining edge vectors from the point sets and defers to
    `vec_dihedrals`, so the result is the signed angle between the two half-planes
    hinged on the shared edge.

    :param pts1: first point set
    :type pts1: np.ndarray
    :param pts2: second point set (shared hinge)
    :type pts2: np.ndarray
    :param pts3: third point set
    :type pts3: np.ndarray
    :param pts4: fourth point set
    :type pts4: np.ndarray
    :param crosses: precomputed cross products (optional)
    :type crosses: np.ndarray | None
    :param norms: precomputed norms (optional)
    :type norms: np.ndarray | None
    :param return_crosses: also return the cross products
    :type return_crosses: bool
    :param opts: extra options forwarded to `vec_dihedrals`
    :return: the book angles (plus crosses if requested)
    :rtype: np.ndarray | tuple
    """
    # compute signed angle between the normals to the b1xb2 plane and b2xb3 plane
    b2 = pts1 - pts2  # 1->2
    b1 = pts2 - pts3  # 1->2
    b3 = pts4 - pts2  # 2->3

    return vec_dihedrals(
        b1, b2, b3,
        crosses=crosses,
        norms=norms,
        return_crosses=return_crosses,
        **opts
    )

################################################
#
#       mat_vec_muls
def mat_vec_muls(mats, vecs):
    """Pairwise multiplies mats and vecs

    :param mats:
    :type mats:
    :param vecs:
    :type vecs:
    :return:
    :rtype:
    """

    vecs_2 = np.matmul(mats, vecs[..., np.newaxis])
    return np.reshape(vecs_2, vecs.shape)

################################################
#
#       one_pad_vecs
def one_pad_vecs(vecs):
    """
    **LLM Docstring**

    Append a trailing column of ones to a stack of vectors (the homogeneous-
    coordinate padding used for affine transforms).

    :param vecs: the vectors to pad
    :type vecs: np.ndarray
    :return: the vectors with a `1` appended along the last axis
    :rtype: np.ndarray
    """
    ones = np.ones(vecs.shape[:-1] + (1,))
    vecs = np.concatenate([vecs, ones], axis=-1)
    return vecs

################################################
#
#       affine_multiply
def affine_multiply(mats, vecs):
    """
    Multiplies affine mats and vecs

    :param mats:
    :type mats:
    :param vecs:
    :type vecs:
    :return:
    :rtype:
    """

    vec_shape = vecs.shape
    if vec_shape[-1] != 4:
        vecs = one_pad_vecs(vecs)
    res = mat_vec_muls(mats, vecs)
    if vec_shape[-1] != 4:
        res = res[..., :3]
    return res

###
#
#       cartesian_from_rad_transforms
default_angle_sign = 1
def cartesian_from_rad_transforms(centers, vecs1, vecs2, angles, dihedrals, return_comps=False, angle_sign=None):
    """Builds a single set of affine transformation matrices to apply to the vecs1 to get a set of points

    :param centers: central coordinates
    :type centers: np.ndarray
    :param vecs1: vectors coming off of the centers
    :type vecs1: np.ndarray
    :param vecs2: vectors coming off of the centers
    :type vecs2: np.ndarray
    :param angles: angle values
    :type angles: np.ndarray
    :param dihedrals: dihedral values
    :type dihedrals: np.ndarray | None
    :return:
    :rtype:
    """
    from .TransformationMatrices import rotation_matrix, affine_matrix
    if angle_sign is None:
        angle_sign = default_angle_sign

    crosses = vec_crosses(vecs1, vecs2)
    rot_mats_1 = rotation_matrix(crosses, angle_sign*angles)
    if dihedrals is not None:
        rot_mats_2 = rotation_matrix(vecs1, -dihedrals) # add negative sign to match Gaussian sign convention
        rot_mat = np.matmul(rot_mats_2, rot_mats_1)
    else:
        rot_mat = rot_mats_1
        rot_mats_2 = None
    transfs = affine_matrix(rot_mat, centers)

    if return_comps:
        comps = (crosses, rot_mats_2, rot_mats_1)
    else:
        comps = None
    return transfs, comps

##############################################################################
#
#       cartesian_from_rad
#
def cartesian_from_rad(xa, xb, xc, r, a, d, psi=False, return_comps=False):
    """
    Constructs a Cartesian coordinate from a bond length, angle, and dihedral
    and three points defining an embedding
    :param xa: first coordinate defining the embedding
    :type xa: np.ndarray
    :param xb: third coordinate defining the embedding
    :type xb: np.ndarray
    :param xc: third coordinate defining the embedding
    :type xc: np.ndarray
    :param r:
    :type r:
    :param a:
    :type a:
    :param d:
    :type d:
    :param ref_axis:
    :type ref_axis:
    :param return_comps:
    :type return_comps:
    :return:
    :rtype:
    """

    v = xb - xa
    center = xa
    if a is None:
        vecs1 = vec_normalize(v)
        # no angle so all we have is a bond length to work with
        # means we don't even really want to build an affine transformation
        newstuff = xa + r[..., np.newaxis] * vecs1
        comps = (v, None, None, None, None)
    else:
        # print(">>>", psi)
        u = xc - xb
        if isinstance(psi, np.ndarray):
            # a = -a
            # vecs1 = vec_normalize(v)
            # v[psi] = -v[psi]
            # center = center.copy()
            # center[psi] = xb[psi]
            d = np.pi - d
            # d[psi] = np.pi-d
        # elif psi:
        #     center = xb
        #     v = xa - xb
        #     u = xa - xc
        vecs1 = vec_normalize(v)
        vecs2 = vec_normalize(u)
        transfs, comps = cartesian_from_rad_transforms(center, vecs1, vecs2, a, d,
                                                       return_comps=return_comps)
        newstuff = affine_multiply(transfs, r * vecs1)
        if return_comps:
            comps = (v, u) + comps
        else:
            comps = None
    return newstuff, comps

##############################################################################
#
#       polar_to_cartesian
#
def polar_to_cartesian_transforms(centers, vecs1, vecs2, azimuths, polars):
    """Builds a single set of affine transformation matrices to apply to the vecs1 to get a set of points

    :param centers: central coordinates
    :type centers: np.ndarray
    :param vecs1: vectors coming off of the centers
    :type vecs1: np.ndarray
    :param vecs2: vectors coming off of the centers
    :type vecs2: np.ndarray
    :param angles: angle values
    :type angles: np.ndarray
    :param dihedrals: dihedral values
    :type dihedrals: np.ndarray | None
    :return:
    :rtype:
    """
    from .TransformationMatrices import rotation_matrix, affine_matrix

    rot_mats_1 = rotation_matrix(vecs2, -azimuths)
    if polars is not None:
        vecs1 = np.broadcast_to(vecs1, rot_mats_1.shape[:-1])
        vecs2 = np.broadcast_to(vecs2, rot_mats_1.shape[:-1])
        new_ax = mat_vec_muls(rot_mats_1, vecs1)
        rot_mats_2 = rotation_matrix(vec_crosses(vecs2, new_ax), np.pi/2-polars)
        rot_mat = np.matmul(rot_mats_2, rot_mats_1)
    else:
        rot_mat = rot_mats_1
    transfs = affine_matrix(rot_mat, centers)
    return transfs

def polar_to_cartesian(center, v, u, r, a, d):
    """
    Constructs a Cartesian coordinate from a bond length, angle, and dihedral
    and three points defining an embedding
    :param xa: first coordinate defining the embedding
    :type xa: np.ndarray
    :param xb: third coordinate defining the embedding
    :type xb: np.ndarray
    :param xc: third coordinate defining the embedding
    :type xc: np.ndarray
    :param r:
    :type r:
    :param a:
    :type a:
    :param d:
    :type d:
    :param ref_axis:
    :type ref_axis:
    :param return_comps:
    :type return_comps:
    :return:
    :rtype:
    """

    if a is None:
        vecs1 = vec_normalize(v)
        # no angle so all we have is a bond length to work with
        # means we don't even really want to build an affine transformation
        newstuff = center + r[..., np.newaxis] * vecs1
    else:
        vecs1 = vec_normalize(v)
        vecs2 = vec_normalize(u)
        transfs = polar_to_cartesian_transforms(center, vecs1, vecs2, a, d)
        newstuff = affine_multiply(transfs, r[..., np.newaxis] * vecs1)
    return newstuff


##############################################################################
#
#       apply_pointwise
#
def apply_by_coordinates(tf, points, reroll=None, ndim=1, **kwargs):
    """
    **LLM Docstring**

    Apply a transformation function that expects its inputs split into separate
    coordinate arguments.

    The trailing `ndim` coordinate axes are rolled to the front so they can be
    unpacked as positional arguments to `tf`; the result is rolled back (when it
    matches the input layout, or when `reroll` is forced). If `tf` returns extra
    values alongside the transformed points, those are passed through.

    :param tf: the transformation function (called as `tf(*coords, **kwargs)`)
    :type tf: Callable
    :param points: the points to transform
    :type points: np.ndarray
    :param reroll: force rolling the coordinate axes back (auto-detected if `None`)
    :type reroll: bool | None
    :param ndim: number of trailing coordinate axes to split off
    :type ndim: int
    :param kwargs: extra keyword arguments forwarded to `tf`
    :return: the transformed points (plus any extra returns from `tf`)
    :rtype: np.ndarray | tuple
    """
    points = np.asanyarray(points)
    for i in range(ndim):
        points = np.moveaxis(points, -1, 0)

    vals = tf(*points, **kwargs)
    #TODO: this is a bit of a hack, let's clean it up
    if not isinstance(vals, np.ndarray) and isinstance(vals[0], np.ndarray):
        vals, rest = vals[0], vals[1:]
        if len(rest) == 1:
            rest = rest[0]
    else:
        rest = None

    vals = np.asanyarray(vals)
    if reroll or (reroll is None and vals.shape == points.shape):
        for i in range(ndim):
            vals = np.moveaxis(vals, 0, -1)
    if rest is not None:
        return vals, rest
    else:
        return vals

def apply_by_structures(tf, points, ndim=1, **kwargs):
    """
    **LLM Docstring**

    Apply a transformation function to each structure in a batch individually.

    The leading batch axes are flattened, `tf` is called once per structure, and the
    results are restacked. If `tf` returns extra values alongside its primary array,
    those are collected and returned separately.

    :param tf: the per-structure transformation function
    :type tf: Callable
    :param points: the batched points/structures
    :type points: np.ndarray
    :param ndim: number of trailing axes belonging to a single structure
    :type ndim: int
    :param kwargs: extra keyword arguments forwarded to `tf`
    :return: the stacked results (plus any extra returns from `tf`)
    :rtype: np.ndarray | tuple
    """
    points = np.asanyarray(points)
    base_shape = points.shape[:-ndim]
    points = points.reshape((-1,) + points.shape[-ndim:])

    vals = [
        tf(pt, **kwargs)
        for pt in points
    ]


    if not (util.is_numeric(vals[0]) or util.is_numeric_array_like(vals[0])):
        vals, rest = np.asanyarray([v[0] for v in vals]), [v[1:] for v in vals]
    else:
        vals = np.asanyarray(vals)
        rest = None

    if rest is not None:
        return vals, rest
    else:
        return vals


# ##############################################################################
# #
# #       kron_sum
# #
# def kron_sum(A, B, shared=None)
#     if shared is None:
#         n = A.shape[0]
#         m = B.shape[0]
#     else:
#         raise NotImplementedError("vectorized kron sum not implemented yet...just use vec_outer tricks")
#         n = A.shape[shared]
#         m = B.shape[shared]:
#     A_ = vec_outer(A, np.eye())
#     A_ = np.kron(A, np.eye(m))
#     B_ = np.kron(np.eye(n), B)
#     if shared is not None:
#         B_ = np.moveaxis
#
#     np.moveaxis(np.kron(np.eye(), A), ) +


##############################################################################
#
#       project_out
#

def find_basis(mat, nonzero_cutoff=1e-8, method='svd'):
    """
    **LLM Docstring**

    Find an orthonormal basis for the column space (range) of a matrix.

    Supports several methods: `'qr'` returns the `Q` factor, `'svd'` returns the
    left singular vectors with singular values above `nonzero_cutoff`, and
    `'right-svd'` / `'right-unitary'` build right-projected bases. Batched inputs are
    handled per matrix; when the retained rank varies across the batch a list of
    per-matrix bases is returned rather than a single stacked array.

    :param mat: the matrix (or stack of matrices)
    :type mat: np.ndarray
    :param nonzero_cutoff: singular-value cutoff for retained directions
    :type nonzero_cutoff: float
    :param method: `'svd'`, `'qr'`, `'right-svd'`, or `'right-unitary'`
    :type method: str
    :return: the basis (or a list of bases for ragged batches)
    :rtype: np.ndarray | list[np.ndarray]
    """
    if method == 'qr':
        basis, _ = np.linalg.qr(mat)
        return basis
    elif method == 'svd':
        u, s, v = np.linalg.svd(mat)
        mask = s > nonzero_cutoff
        if u.ndim == 2:
            good_s = np.where(mask)
            return u[:, good_s[0]]
        else:
            base_shape = u.shape[:-2]
            u = u.reshape((-1,) + u.shape[-2:])
            mask = mask.reshape((-1, mask.shape[-1]))
            good_sums = np.sum(mask, axis=1)
            num_good = np.unique(good_sums)
            if len(num_good) == 1:
                # num_good = num_good[0]
                # mask_inds = np.where(mask)
                # take_spec = mask_inds[:-1] + (slice(None),) + mask_inds[-1:]
                # print(take_spec)
                # u = u[take_spec].reshape(u.shape[:-1] + (num_good,))
                # return u.reshape(base_shape + u.shape[-2:])
                blocks = []
                for uu, m in zip(u, mask):
                    w = np.where(m)
                    blocks.append(uu[:, w[0]])
                blocks = np.array(blocks)
                return blocks.reshape(base_shape + blocks.shape[1:])
            else:
                blocks = []
                for uu,m in zip(u, mask):
                    w = np.where(m)
                    blocks.append(uu[:, w[0]])
                #TODO: handle base shape
                return blocks
    elif method == 'right-svd':
        u, s, v = np.linalg.svd(mat)
        mask = s > nonzero_cutoff
        if u.ndim == 2:
            good_s = np.where(mask)
            return mat @ v.T[:, good_s[0]]
        else:
            base_shape = u.shape[:-2]
            v = v.reshape((-1,) + v.shape[-2:])
            mask = mask.reshape((-1, mask.shape[-1]))
            mat = mat.reshape((-1,) + mat.shape[-2:])
            good_sums = np.sum(mask, axis=1)
            num_good = np.unique(good_sums)
            if len(num_good) == 1:
                blocks = []
                for vv, m, a in zip(v, mask, mat):
                    w = np.where(m)
                    blocks.append(a @ vv.T[:, w[0]])
                blocks = np.array(blocks)
                return blocks.reshape(base_shape + blocks.shape[1:])
            else:
                blocks = []
                for vv, m, a in zip(v, mask, mat):
                    w = np.where(m)
                    blocks.append(a @ vv.T[:, w[0]])
                # TODO: handle base shape
                return blocks
    elif method == 'right-unitary':
        u, s, v = np.linalg.svd(mat)
        mask = s > nonzero_cutoff
        if u.ndim == 2:
            good_s = np.where(mask)
            return mat @ (np.diag(1/s) @ v).T[:, good_s[0]]
        else:
            base_shape = u.shape[:-2]
            v = v.reshape((-1,) + v.shape[-2:])
            mask = mask.reshape((-1, mask.shape[-1]))
            s = s.reshape((-1, s.shape[-1]))
            mat = mat.reshape((-1,) + mat.shape[-2:])
            good_sums = np.sum(mask, axis=1)
            num_good = np.unique(good_sums)
            if len(num_good) == 1:
                blocks = []
                for vv, m, a, ss in zip(v, mask, mat, s):
                    w = np.where(m)
                    blocks.append(a @ (np.diag(1/ss) @ vv).T[:, w[0]])
                blocks = np.array(blocks)
                return blocks.reshape(base_shape + blocks.shape[1:])
            else:
                blocks = []
                for vv, m, a, ss in zip(v, mask, mat, s):
                    w = np.where(m)
                    blocks.append(a @ (np.diag(1/ss) @ vv).T[:, w[0]])
                # TODO: handle base shape
                return blocks
    else:
        raise ValueError(f"method `{method}`")

def projection_matrix(basis, inverse=None, orthonormal=False, allow_pinv=False):
    """
    **LLM Docstring**

    Build the projection matrix onto the span of a basis.

    The projector is `basis @ inverse`; the inverse defaults to the transpose when
    the basis is orthonormal (or after an internal QR), or to the pseudoinverse when
    `allow_pinv` is set.

    :param basis: the basis vectors (columns)
    :type basis: np.ndarray
    :param inverse: explicit left inverse of the basis (optional)
    :type inverse: np.ndarray | None
    :param orthonormal: whether the basis is already orthonormal
    :type orthonormal: bool
    :param allow_pinv: use the pseudoinverse instead of QR/transpose
    :type allow_pinv: bool
    :return: the projection matrix
    :rtype: np.ndarray
    """
    basis = np.asanyarray(basis)
    if basis.ndim == 1:
        basis = basis[np.newaxis]
    if inverse is None:
        if allow_pinv:
            inverse = np.linalg.pinv(basis)
        else:
            if not orthonormal:
                basis, _ = np.linalg.qr(basis)
            inverse = np.moveaxis(basis, -2, -1)

    return basis @ inverse

def orthogonal_projection_matrix(basis, inverse=None, orthonormal=False, allow_pinv=False):
    """
    **LLM Docstring**

    Build the complementary projector that removes the span of a basis (`I - P`).

    :param basis: the basis vectors (columns)
    :type basis: np.ndarray
    :param inverse: explicit left inverse of the basis (optional)
    :type inverse: np.ndarray | None
    :param orthonormal: whether the basis is already orthonormal
    :type orthonormal: bool
    :param allow_pinv: use the pseudoinverse instead of QR/transpose
    :type allow_pinv: bool
    :return: the orthogonal (complementary) projection matrix
    :rtype: np.ndarray
    """
    proj = projection_matrix(basis, inverse=inverse, orthonormal=orthonormal, allow_pinv=allow_pinv)
    identities = identity_tensors(proj.shape[:-2], proj.shape[-1])
    return identities - proj

def _proj(projection_type, vecs, basis, ndim=None, orthonormal=False, inverse=None, allow_pinv=False):
    """
    **LLM Docstring**

    Shared implementation for projecting vectors onto or out of a basis.

    Validates the vector/basis dimensions, builds the requested projector via
    `projection_type`, and applies it to the (possibly multi-axis) vectors,
    inferring the number of vector axes from the basis batch shape when `ndim` is
    omitted.

    :param projection_type: projector builder (`projection_matrix` or its orthogonal form)
    :type projection_type: Callable
    :param vecs: the vectors to project
    :type vecs: np.ndarray
    :param basis: the basis to project against
    :type basis: np.ndarray
    :param ndim: number of vector axes (inferred if omitted)
    :type ndim: int | None
    :param orthonormal: whether the basis is orthonormal
    :type orthonormal: bool
    :param inverse: explicit basis inverse (optional)
    :type inverse: np.ndarray | None
    :param allow_pinv: use the pseudoinverse
    :type allow_pinv: bool
    :return: the projected vectors
    :rtype: np.ndarray
    """
    vecs = np.asanyarray(vecs)
    basis = np.asanyarray(basis)
    if vecs.shape[-1] != basis.shape[-2]:
        raise ValueError(f"mismatch between vector dim {vecs.shape[-1]} and basis dim {basis.shape[-2]} ({basis.shape[-1]} basis vectors)")
    if ndim is None:
        base_shape = basis.shape[:-2]
        if len(base_shape) == 0:
            ndim = 1
        else:
            ndim = vecs.ndim - len(base_shape)
    base_shape = vecs.shape[:-ndim]

    proj = projection_type(basis, orthonormal=orthonormal, inverse=inverse, allow_pinv=allow_pinv)
    if ndim == 1:
        vecs = (vecs[..., np.newaxis, :] @ proj).reshape(vecs.shape)
    else:
        for _ in range(ndim):
            vecs = np.moveaxis(vecs @ proj, -1, len(base_shape))

    return vecs

def project_onto(vecs, basis, ndim=None, orthonormal=False, inverse=None, allow_pinv=False):
    """
    **LLM Docstring**

    Project vectors onto the span of a basis.

    :param vecs: the vectors to project
    :type vecs: np.ndarray
    :param basis: the basis to project onto
    :type basis: np.ndarray
    :param ndim: number of vector axes (inferred if omitted)
    :type ndim: int | None
    :param orthonormal: whether the basis is orthonormal
    :type orthonormal: bool
    :param inverse: explicit basis inverse (optional)
    :type inverse: np.ndarray | None
    :param allow_pinv: use the pseudoinverse
    :type allow_pinv: bool
    :return: the projected vectors
    :rtype: np.ndarray
    """
    return _proj(projection_matrix, vecs, basis, ndim=ndim,
                 orthonormal=orthonormal, inverse=inverse, allow_pinv=allow_pinv)

def project_out(vecs, basis, ndim=None, orthonormal=False, inverse=None, allow_pinv=False):
    """
    **LLM Docstring**

    Project the span of a basis *out* of a set of vectors (keep the orthogonal
    complement).

    :param vecs: the vectors to project
    :type vecs: np.ndarray
    :param basis: the basis to remove
    :type basis: np.ndarray
    :param ndim: number of vector axes (inferred if omitted)
    :type ndim: int | None
    :param orthonormal: whether the basis is orthonormal
    :type orthonormal: bool
    :param inverse: explicit basis inverse (optional)
    :type inverse: np.ndarray | None
    :param allow_pinv: use the pseudoinverse
    :type allow_pinv: bool
    :return: the vectors with the basis removed
    :rtype: np.ndarray
    """
    return _proj(orthogonal_projection_matrix, vecs, basis, ndim=ndim,
                 orthonormal=orthonormal, inverse=inverse, allow_pinv=allow_pinv)

def fractional_power(A, pow, zero_cutoff=1e-8):
    """
    **LLM Docstring**

    Raise a symmetric matrix to an arbitrary (fractional) power, discarding
    near-zero eigenvalues.

    The matrix is diagonalized with `np.linalg.eigh`; eigenvalues with magnitude
    above `zero_cutoff` are kept and raised to `pow`, and the matrix is reassembled
    from the retained eigenpairs. Batched inputs are handled per matrix, returning a
    list when the retained rank varies across the batch.

    :param A: the symmetric matrix (or stack)
    :type A: np.ndarray
    :param pow: the exponent
    :type pow: float
    :param zero_cutoff: eigenvalue magnitude below which directions are dropped
    :type zero_cutoff: float
    :return: the fractional matrix power (or a list for ragged batches)
    :rtype: np.ndarray | list[np.ndarray]
    """
    # only applies to symmetric A
    # if symmetric:
    vals, vecs = np.linalg.eigh(A)
    if vals.ndim == 1:
        cutoffs = np.abs(vals) > zero_cutoff
        take_pos = np.where(cutoffs)[0]
        s = vals[..., take_pos]
        u = vecs[..., take_pos]
        v = np.moveaxis(u, -1, -2)
        return u @ vec_tensordiag(np.power(s, pow)) @ v
    else:
        base_shape = vals.shape[:-1]
        vals = vals.reshape((-1,) + vals.shape[-1:])
        vecs = vecs.reshape((-1,) + vecs.shape[-2:])
        cutoffs = np.abs(vals) > zero_cutoff
        cutoff_tests = np.sum(cutoffs, axis=-1)
        num_block_types = np.unique(cutoff_tests)
        blocks = len(num_block_types) > 1
        if blocks:
            take_pos = [np.where(c)[0] for c in cutoffs]
            return [
                vv[:, tp].T @ np.diag(np.power(va[tp], pow)) @ vv[:, tp]
                for vv,va,tp in zip(vecs, vals, take_pos)
            ]
        else:
            bt = num_block_types[0]
            if bt == A.shape[-1]:
                u = vecs
                v = np.moveaxis(vecs, -2, -1)
                s = vals
            else:
                take_idx = np.ravel_multi_index(np.where(cutoffs), vals.shape)
                s = vals.reshape(-1)[take_idx,].reshape((-1, bt))
                v = np.moveaxis(vecs, -2, -1).reshape((-1, vecs.shape[-1]))[
                    take_idx
                ].reshape((vecs.shape[0], bt, vecs.shape[-1]))
                u = np.moveaxis(v, -2, -1)

            flat_pow = u @ vec_tensordiag(np.power(s, pow)) @ v
            return flat_pow.reshape(base_shape + flat_pow.shape[-2:])

def unitarize_transformation(tf):
    """
    **LLM Docstring**

    Return the nearest unitary (orthogonal) matrix to a transformation, via its
    SVD (`U V` with the singular values dropped).

    :param tf: the transformation matrix
    :type tf: np.ndarray
    :return: the closest unitary transformation
    :rtype: np.ndarray
    """
    u, s, v = np.linalg.svd(tf)
    shared_dim = min((u.shape[-1], v.shape[-2]))
    return u[..., :, :shared_dim] @ v[..., :shared_dim, :]

def polar_decomposition(tf, order='scale-first'):
    """
    **LLM Docstring**

    Compute the polar decomposition of a transformation into a symmetric
    positive part `P` and a unitary part `Q`, using the SVD.

    With `order='scale-first'` the factorization is `tf = P Q` (scale then rotate);
    otherwise it is returned in rotate-then-scale order.

    :param tf: the transformation matrix
    :type tf: np.ndarray
    :param order: `'scale-first'` for `(P, Q)`, else `(Q, P)`
    :type order: str
    :return: the two polar factors
    :rtype: tuple[np.ndarray, np.ndarray]
    """
    u, s, v = np.linalg.svd(tf)
    shared_dim = min((u.shape[-1], v.shape[-2]))
    Q = u[..., :, :shared_dim] @ v[..., :shared_dim, :]
    if order == 'scale-first':
        P = u @ vec_tensordiag(s) @ np.moveaxis(u, -1, -2)
        return P, Q
    else:
        Q = Q.T
        P = np.moveaxis(v, -1, -2) @ vec_tensordiag(s) @ v
        return Q, P

def maximum_similarity_transformation(basis, target, apply_transformation=True):
    """
    **LLM Docstring**

    Find the unitary transformation that best maps a basis onto a target (in the
    least-squares sense) and optionally apply it.

    A least-squares fit is unitarized with `unitarize_transformation`; the resulting
    rotation is returned, or applied to `basis` when `apply_transformation` is set.

    :param basis: the source basis
    :type basis: np.ndarray
    :param target: the target the basis should align with
    :type target: np.ndarray
    :param apply_transformation: return `basis @ tf` instead of `tf`
    :type apply_transformation: bool
    :return: the aligned basis or the alignment transformation
    :rtype: np.ndarray
    """
    lstsq_tf = np.linalg.lstsq(basis, target, rcond=None)[0]
    tf = unitarize_transformation(lstsq_tf)
    if apply_transformation:
        return basis @ tf
    else:
        return tf

def matrix_transform_from_eigs(evals, evecs, tf):
    """
    **LLM Docstring**

    Apply a scalar function to the eigenvalues of a matrix and reassemble it in the
    original eigenbasis (`Vᵀ diag(f(evals)) V`).

    :param evals: the eigenvalues
    :type evals: np.ndarray
    :param evecs: the eigenvectors
    :type evecs: np.ndarray
    :param tf: scalar function applied to the eigenvalues
    :type tf: Callable
    :return: the transformed matrix
    :rtype: np.ndarray
    """
    return np.moveaxis(evecs, -1, -2) @ vec_tensordiag(tf(evals), extra_dims=evals.ndim-1) @ evecs

def symmetric_matrix_exp(mats):
    """
    **LLM Docstring**

    Matrix exponential of a symmetric matrix, computed by exponentiating its
    eigenvalues.

    :param mats: the symmetric matrix (or stack)
    :type mats: np.ndarray
    :return: the matrix exponential
    :rtype: np.ndarray
    """
    evals, evecs = np.linalg.eigh(mats)
    return matrix_transform_from_eigs(evals, evecs, np.exp)

def imaginary_symmetric_matrix_exp(mats):
    """
    **LLM Docstring**

    Real and imaginary parts of `exp(i A)` for a symmetric matrix `A`, obtained by
    applying `cos` and `sin` to its eigenvalues.

    :param mats: the symmetric matrix (or stack)
    :type mats: np.ndarray
    :return: `[real_part, imaginary_part]`
    :rtype: list[np.ndarray]
    """
    evals, evecs = np.linalg.eigh(mats)
    return [
        matrix_transform_from_eigs(evals, evecs, np.cos),
        matrix_transform_from_eigs(evals, evecs, np.sin)
    ]

def symmetric_matrix_log(mats):
    """
    **LLM Docstring**

    Matrix logarithm of a symmetric matrix, computed by taking the log of its
    eigenvalues.

    :param mats: the symmetric matrix (or stack)
    :type mats: np.ndarray
    :return: the matrix logarithm
    :rtype: np.ndarray
    """
    evals, evecs = np.linalg.eigh(mats)
    return matrix_transform_from_eigs(evals, evecs, np.log)

def imaginary_symmetric_matrix_log(mats_real, mats_imag):
    """
    **LLM Docstring**

    Recover the symmetric generator `A` from the real and imaginary parts of
    `exp(i A)`.

    The real part is diagonalized to obtain `arccos` of its eigenvalues, the
    imaginary part is rotated into the same basis to supply `arcsin`, and the
    generator is rebuilt in that eigenbasis.

    :param mats_real: real part of `exp(i A)`
    :type mats_real: np.ndarray
    :param mats_imag: imaginary part of `exp(i A)`
    :type mats_imag: np.ndarray
    :return: the symmetric generator
    :rtype: np.ndarray
    """
    evals_real, evecs = np.linalg.eigh(mats_real)
    evals_imag = np.diagonal(
        evecs @ mats_imag @ np.moveaxis(evecs, -1, -2),
        axis1=-1,
        axis2=-2
    )
    return matrix_transform_from_eigs(
        np.arccos(evals_real) + np.arcsin(evals_imag), evecs, lambda x: x
    )

def sylvester_solve(A, B, C):
    """
    **LLM Docstring**

    Solve the Sylvester equation `A X + X B = C` for `X`.

    The equation is vectorized into the Kronecker-form linear system `(Bᵀ ⊗ I + I ⊗
    A) vec(X) = vec(C)` and solved with `np.linalg.solve`.

    :param A: the left coefficient matrix
    :type A: np.ndarray
    :param B: the right coefficient matrix
    :type B: np.ndarray
    :param C: the right-hand side
    :type C: np.ndarray
    :return: the solution `X`
    :rtype: np.ndarray
    """
    A = np.asanyarray(A)
    B = np.asanyarray(B)
    C = np.asanyarray(C)
    n = A.shape[1]
    m = B.shape[0]
    S = np.kron(B.T, np.eye(n)) + np.kron(np.eye(m), A)
    val = np.linalg.solve(S, C.flatten()) # in case it can be cleverer than I can
    return val.reshape(m,n)

def symmetrize_array(a,
                     axes=None,
                     symmetrization_mode='total',
                     axes_block_ordering=None,
                     mixed_block_symmetrize=False,
                     restricted_diagonal=False,
                     out=None
                     ):
    """
    **LLM Docstring**

    Symmetrize an array over one or more groups of axes.

    The default `'total'` mode averages the array over all permutations within each
    axis group. Other modes select rather than average a canonical ordering
    (`'low'`, `'high'`, `'average'`) and broadcast it across the permuted positions;
    `restricted_diagonal`, `axes_block_ordering`, and `mixed_block_symmetrize`
    control which index tuples and permutations participate.

    :param a: the array to symmetrize
    :type a: np.ndarray
    :param axes: axis or list of axis groups to symmetrize over (defaults to all)
    :type axes: Iterable | None
    :param symmetrization_mode: `'total'`, `'low'`, `'high'`, `'average'`, or `'unhandled'`
    :type symmetrization_mode: str
    :param axes_block_ordering: explicit block ordering for the selected value
    :type axes_block_ordering: Iterable | None
    :param mixed_block_symmetrize: permute across all axes rather than within blocks
    :type mixed_block_symmetrize: bool
    :param restricted_diagonal: restrict to diagonal index tuples
    :type restricted_diagonal: bool
    :param out: optional output array to write into
    :type out: np.ndarray | None
    :return: the symmetrized array
    :rtype: np.ndarray
    """
    from . import Misc as misc

    if axes is None:
        axes = np.arange(a.ndim)
    if misc.is_numeric(axes[0]):
        axes = [axes]

    axes_groups = axes
    del axes # easier debugging

    symmetrization_mode = symmetrization_mode.lower()

    if (
            not restricted_diagonal
            and axes_block_ordering is None
            and symmetrization_mode == 'total'
    ):
        if mixed_block_symmetrize:
            axes_groups = np.concatenate(axes_groups)
        b = a
        for i,axes in enumerate(axes_groups):
            a = b / math.factorial(len(axes))
            missing = np.setdiff1d(np.arange(a.ndim), axes)
            inv = np.argsort(np.concatenate([axes, missing]), axis=0)
            perm_iter = itertools.permutations(axes)
            b = a
            next(perm_iter) # first step
            if len(missing) == 0:
                for p in itertools.permutations(axes):
                    b += a.transpose(p)
            else:
                for p in itertools.permutations(axes):
                    p = np.concatenate([p, missing])[inv]
                    b += a.transpose(p)
        if out is not None:
            out[:] = b
            b = out
    else:
        flat_axes = np.concatenate(axes_groups)
        rem_axes = np.setdiff1d(np.arange(a.ndim), flat_axes)
        ordering = np.argsort(np.concatenate([flat_axes, rem_axes]))
        nmodes = a.shape[0]

        if restricted_diagonal:
            if mixed_block_symmetrize:
                pos_spec = [
                    sum(
                        [(i,)*len(axes) for i,axes in zip(term, axes_groups)],
                        ()
                    )
                    for term in itertools.combinations_with_replacement(
                        range(nmodes),
                        len(axes_groups)
                    )
                ]
            else:
                pos_spec = [
                    sum(
                        [(i,) * len(axes) for i, axes in zip(p, axes_groups)],
                        ()
                    )
                    for term in itertools.combinations_with_replacement(
                        range(nmodes),
                        len(axes_groups)
                    )
                    for p in np.unique(list(itertools.permutations(term)), axis=0)
                ]
        else:
            pos_spec = list(
                itertools.combinations_with_replacement(
                    range(nmodes),
                    len(flat_axes)
                )
            )

        if mixed_block_symmetrize:
            perms = itertools.permutations(np.arange(len(flat_axes)), len(flat_axes))
        else:
            cumlens = np.cumsum([0] + [len(a) for a in axes_groups])
            perms = (
                sum(t, ())
                for t in itertools.product(*[
                    itertools.permutations(range(l, l + len(x)), len(x))
                    for x, l in zip(axes_groups, cumlens)
                ])
            )

        if out is None:
            b = a.copy()
        else:
            b = out

        pos_arr = tuple(np.array(list(pos_spec)).T)
        padding = (slice(None),) * len(rem_axes)
        if symmetrization_mode == 'unhandled':
            for perm in perms:
                new_pos = tuple(pos_arr[flat_axes[p]] for p in perm) + padding
                new_pos = tuple(new_pos[i] for i in ordering)
                b[new_pos] = a[new_pos]
        else:
            if axes_block_ordering is not None:
                new_pos = tuple(
                    pos_arr[p] for p in
                    np.concatenate([axes_groups[f] for f in axes_block_ordering])
                ) + padding
                new_pos = tuple(new_pos[i] for i in ordering)
                val = a[new_pos]
            else:
                if symmetrization_mode == 'low':
                    new_pos = tuple(pos_arr[f] for f in reversed(flat_axes)) + padding
                    new_pos = tuple(new_pos[i] for i in ordering)
                    val = a[new_pos]
                elif symmetrization_mode == 'high':
                    new_pos = tuple(pos_arr[f] for f in flat_axes) + padding
                    new_pos = tuple(new_pos[i] for i in ordering)
                    val = a[new_pos]
                elif symmetrization_mode == 'average':
                    new_pos_1 = tuple(pos_arr[f] for f in reversed(flat_axes)) + padding
                    new_pos_1 = tuple(new_pos_1[i] for i in ordering)
                    new_pos_2 = tuple(pos_arr[f] for f in flat_axes) + padding
                    new_pos_2 = tuple(new_pos_2[i] for i in ordering)
                    val = (a[new_pos_1] + a[new_pos_2]) / 2
                else:
                    raise ValueError(
                        f"don't know what to do with `symmetrization_mode` '{symmetrization_mode}' "
                    )

            for perm in perms:
                new_pos = tuple(pos_arr[flat_axes[p]] for p in perm) + padding
                new_pos = tuple(new_pos[i] for i in ordering)
                b[new_pos] = val

    return b

def integer_exponent(ints, k, max_its=None):
    """
    **LLM Docstring**

    For each integer, factor out the largest power of `k` that divides it.

    Repeatedly divides the entries still divisible by `k`, counting the divisions,
    until no entry is divisible or `max_its` is reached.

    :param ints: the integers to factor
    :type ints: np.ndarray
    :param k: the base to factor out
    :type k: int
    :param max_its: cap on the number of division passes (inferred if omitted)
    :type max_its: int | None
    :return: `(residuals, exponents)` — the co-factors and the powers of `k` removed
    :rtype: tuple[np.ndarray, np.ndarray]
    """
    ints = np.asanyarray(ints, dtype=int)
    base_shape = ints.shape
    ints = ints.reshape(-1)
    sel = np.arange(ints.shape[0])
    counts = np.zeros(ints.shape[0], dtype=int)
    if max_its is None:
        if k == 2:
            test_its = np.log2(ints)
        elif k == 10:
            test_its = np.log10(ints)
        else:
            test_its = np.log(ints) / np.log(k)
        max_its = int(np.ceil(np.max(test_its)))
    for i in range(max_its):
        mask = np.where(ints[sel,] % k == 0)
        if len(mask) == 0 or len(mask[0]) == 0:
            break

        sel = sel[mask[0],]
        counts[sel,] += 1
        ints[sel,] //= k
    return ints.reshape(base_shape), counts.reshape(base_shape)
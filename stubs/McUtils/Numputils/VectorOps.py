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
__all__ = ['vec_dots', 'vec_handle_zero_norms', 'vec_apply_zero_threshold', 'vec_normalize', 'vec_rescale', 'vec_norms', 'vec_tensordot', 'vec_tensordiag', 'vec_block_diag', 'diag_indices', 'block_array', 'vec_tdot', 'distance_matrix', 'unembedded_pts_rmsd', 'points_from_distance_matrix', 'identity_tensors', 'block_broadcast_indices', 'broadcast_constant', 'semisparse_tensordot', 'frac_powh', 'vec_crosses', 'vec_angles', 'vec_sins', 'vec_cos', 'vec_outer', 'pts_norms', 'pts_angles', 'pts_normals', 'vec_dihedrals', 'pts_dihedrals', 'pts_book_angles', 'mat_vec_muls', 'one_pad_vecs', 'affine_multiply', 'cartesian_from_rad', 'polar_to_cartesian', 'apply_by_coordinates', 'apply_by_structures', 'find_basis', 'projection_matrix', 'orthogonal_projection_matrix', 'project_onto', 'project_out', 'fractional_power', 'unitarize_transformation', 'maximum_similarity_transformation', 'polar_decomposition', 'matrix_transform_from_eigs', 'symmetric_matrix_exp', 'imaginary_symmetric_matrix_exp', 'symmetric_matrix_log', 'imaginary_symmetric_matrix_log', 'sylvester_solve', 'symmetrize_array', 'integer_exponent']

def vec_dots(vecs1, vecs2, axis=-1):
    """
    Computes the pair-wise dot product of two lists of vecs using np.matmul

    :param vecs1:
    :type vecs1:
    :param vecs2:
    :type vecs2:
    """
    ...

def vec_norms(vecs, axis=-1):
    """

    :param vecs:
    :type vecs: np.ndarray
    :param axis:
    :type axis: int
    :return:
    :rtype:
    """
    ...

def points_from_distance_matrix(dist_mat, test_idx=None, target_dim=None, use_triu=False, zero_cutoff=1e-08):
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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

def vec_normalize(vecs, norms=None, axis=-1, zero_thresh=None, return_norms=False):
    """

    :param vecs:
    :type vecs: np.ndarray
    :param axis:
    :type axis: int
    :return:
    :rtype:
    """
    ...

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
    ...

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
    ...

def vec_cos(vectors1, vectors2, zero_thresh=None, axis=-1):
    """Gets the cos of the angle between two vectors

    :param vectors1:
    :type vectors1: np.ndarray
    :param vectors2:
    :type vectors2: np.ndarray
    """
    ...

def vec_sins(vectors1, vectors2, zero_thresh=None, axis=-1):
    """Gets the sin of the angle between two vectors

    :param vectors1:
    :type vectors1: np.ndarray
    :param vectors2:
    :type vectors2: np.ndarray
    """
    ...

def vec_angles(vectors1, vectors2, norms=None, up_vectors=None, zero_thresh=None, axis=-1, return_norms=False, return_crosses=True, return_cross_norms=False, check_zeros=True):
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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

def pts_norms(pts1, pts2, **opts):
    """Provides the distance between the points

    :param pts1:
    :type pts1: np.ndarray
    :param pts2:
    :type pts2: np.ndarray
    :return:
    :rtype: np.ndarray
    """
    ...

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
    ...

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
    ...

def vec_dihedrals(b1, b2, b3, crosses=None, norms=None, return_crosses=False):
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
    ...

def pts_dihedrals(pts1, pts2, pts3, pts4, crosses=None, norms=None, return_crosses=False, **opts):
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
    ...

def pts_book_angles(pts1, pts2, pts3, pts4, crosses=None, norms=None, return_crosses=False, **opts):
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
    ...

def mat_vec_muls(mats, vecs):
    """Pairwise multiplies mats and vecs

    :param mats:
    :type mats:
    :param vecs:
    :type vecs:
    :return:
    :rtype:
    """
    ...

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
    ...

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
    ...
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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

def find_basis(mat, nonzero_cutoff=1e-08, method='svd'):
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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

def fractional_power(A, pow, zero_cutoff=1e-08):
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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

def symmetrize_array(a, axes=None, symmetrization_mode='total', axes_block_ordering=None, mixed_block_symmetrize=False, restricted_diagonal=False, out=None):
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
    ...

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
    ...
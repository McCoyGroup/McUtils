from __future__ import annotations
'\nProvides analytic derivatives for some common base terms with the hope that we can reuse them elsewhere\n'
import itertools
import math
import numpy as np
from .VectorOps import *
from . import CoordinateFrames as frames
from . import TensorDerivatives as td
from . import Misc as misc
from . import SetOps as setops
from . import PermutationOps as pops
from . import Geometry as geom
from . import TransformationMatrices as transforms
from .Options import Options
__all__ = ['rot_deriv', 'rot_deriv2', 'cartesian_from_rad_derivatives', 'dist_basis', 'angle_basis', 'internal_basis', 'prep_disp_expansion', 'prep_unit_vector_expansion_from_cache', 'dist_deriv', 'angle_deriv', 'normal_deriv', 'dihed_deriv', 'book_deriv', 'oop_deriv', 'wag_deriv', 'transrot_deriv', 'com_dist_deriv', 'orientation_deriv', 'rotation_expansion_from_axis_angle', 'dist_expansion', 'dihed_expansion', 'angle_expansion', 'rock_deriv', 'rock_vec', 'dist_vec', 'angle_vec', 'dihed_vec', 'book_vec', 'oop_vec', 'wag_vec', 'oop_expansion', 'wag_expansion', 'transrot_vecs', 'transrot_expansion', 'orientation_vecs', 'orientation_expansion', 'internal_conversion_function', 'combine_coordinate_deriv_expansions', 'internal_coordinate_tensors', 'inverse_internal_coordinate_tensors', 'inverse_coordinate_solve', 'combine_coordinate_inverse_expansions', 'metric_tensor', 'delocalized_internal_coordinate_transformation', 'relocalize_coordinate_transformation', 'transform_cartesian_derivatives']

def _prod_deriv(op, a, b, da, db):
    """
    Simple product derivative to make apply the product rule and its analogs
    a bit cleaner. Assumes a derivative that doesn't change dimension.
    Should be generalized at some point to handle arbitrary outer products and shit of that sort.
    :param op:
    :type op:
    :param a:
    :type a:
    :param b:
    :type b:
    :param da:
    :type da:
    :param db:
    :type db:
    :return:
    :rtype:
    """
    ...

def _prod_deriv_2(op, a, b, da1, da2, db1, db2, da12, db12):
    """
    2nd derivative of op(a, b) assuming it operates under a product-rule type ish
    """
    ...

def normalized_vec_deriv(v, dv):
    """
    Derivative of a normalized vector w/r/t some unspecified coordinate
    """
    ...

def normalized_vec_deriv2(v, dv1, dv2, d2v):
    """
    Second derivative of a normalized vector w/r/t some unspecified coordinates
    """
    ...

def rot_deriv(angle, axis, dAngle, dAxis):
    """
    Gives a rotational derivative w/r/t some unspecified coordinate
    (you have to supply the chain rule terms)
    Assumes that axis is a unit vector.

    :param angle: angle for rotation
    :type angle: float
    :param axis: axis for rotation
    :type axis: np.ndarray
    :param dAngle: chain rule angle deriv.
    :type dAngle: float
    :param dAxis: chain rule axis deriv.
    :type dAxis: np.ndarray
    :return: derivatives of the rotation matrices with respect to both the angle and the axis
    :rtype: np.ndarray
    """
    ...

def rot_deriv2(angle, axis, dAngle1, dAxis1, dAngle2, dAxis2, d2Angle, d2Axis):
    """
    Gives a rotation matrix second derivative w/r/t some unspecified coordinate
    (you have to supply the chain rule terms)

    :param angle: angle for rotation
    :type angle: float
    :param axis: axis for rotation
    :type axis: np.ndarray
    :param dAngle: chain rule angle deriv.
    :type dAngle: float
    :param dAxis: chain rule axis deriv.
    :type dAxis: np.ndarray
    :return: derivatives of the rotation matrices with respect to both the angle and the axis
    :rtype: np.ndarray
    """
    ...

def _rad_d1(i, z, m, r, a, d, v, u, n, R1, R2, Q, rv, dxa, dxb, dxc):
    """
    **LLM Docstring**

    First derivative of a Cartesian atom position that was generated from a
    `(r, angle, dihedral)` (Z-matrix style) internal-coordinate spec, taken with
    respect to a *single* perturbed internal coordinate.

    The perturbed coordinate is identified by the atom index `z` and the component
    `m` (`0` = bond length, `1` = angle, `2` = dihedral); the corresponding
    `dr`/`dq`/`df` seeds are `1` only when `z == i` and `m` matches. The routine
    threads those seeds through the normalized embedding axes (`v`, `u`, `n`), the
    rotation matrices (`R1`, `R2`, combined `Q`) and the radial vector `r * v` using
    the product rule.

    :param i: index of the atom whose position is being differentiated
    :type i: int
    :param z: atom index of the internal coordinate being perturbed
    :type z: int
    :param m: which internal component is perturbed (`0`=bond, `1`=angle, `2`=dihedral)
    :type m: int
    :param r: bond length
    :type r: np.ndarray
    :param a: bend angle (or `None` if only a bond is defined)
    :type a: np.ndarray | None
    :param d: dihedral angle (or `None` if not defined)
    :type d: np.ndarray | None
    :param v: unnormalized primary embedding vector
    :type v: np.ndarray
    :param u: unnormalized secondary embedding vector
    :type u: np.ndarray
    :param n: unnormalized normal vector (`v x u`)
    :type n: np.ndarray
    :param R1: rotation matrix about `n` by the angle
    :type R1: np.ndarray
    :param R2: rotation matrix about `v` by the dihedral
    :type R2: np.ndarray
    :param Q: combined rotation matrix
    :type Q: np.ndarray
    :param rv: radial vector `r * v`
    :type rv: np.ndarray
    :param dxa: derivative of the base-atom Cartesian
    :type dxa: np.ndarray
    :param dxb: derivative of the second reference Cartesian
    :type dxb: np.ndarray
    :param dxc: derivative of the third reference Cartesian
    :type dxc: np.ndarray
    :return: the position derivative plus the tuple of intermediate derivatives
        (reused when building the second derivative)
    :rtype: tuple[np.ndarray, tuple]
    """
    ...

def _rad_d2(i, z1, m1, z2, m2, r, a, d, v, u, n, R1, R2, Q, rv, dr1, dq1, df1, dv1, du1, dn1, dR11, dR21, dQ1, drv1, dr2, dq2, df2, dv2, du2, dn2, dR12, dR22, dQ2, drv2, d2xa, d2xb, d2xc):
    """
    **LLM Docstring**

    Second (mixed) derivative of the Cartesian position generated from a
    `(r, angle, dihedral)` internal-coordinate spec.

    Consumes the first-derivative intermediates produced by `_rad_d1` along the two
    perturbation directions (subscripts `1` and `2`) and combines them with the
    second-order product rule. All internal-coordinate second derivatives vanish, so
    the atom-index/component arguments (`z1`, `m1`, `z2`, `m2`) are accepted only for
    signature symmetry and are not used.

    :param i: index of the atom whose position is being differentiated
    :type i: int
    :param z1: atom index of the first perturbed coordinate (unused)
    :type z1: int
    :param m1: component of the first perturbed coordinate (unused)
    :type m1: int
    :param z2: atom index of the second perturbed coordinate (unused)
    :type z2: int
    :param m2: component of the second perturbed coordinate (unused)
    :type m2: int
    :param r: bond length
    :type r: np.ndarray
    :param a: bend angle (or `None`)
    :type a: np.ndarray | None
    :param d: dihedral angle (or `None`)
    :type d: np.ndarray | None
    :param v: unnormalized primary embedding vector
    :type v: np.ndarray
    :param u: unnormalized secondary embedding vector
    :type u: np.ndarray
    :param n: unnormalized normal vector
    :type n: np.ndarray
    :param R1: rotation matrix about `n`
    :type R1: np.ndarray
    :param R2: rotation matrix about `v`
    :type R2: np.ndarray
    :param Q: combined rotation matrix
    :type Q: np.ndarray
    :param rv: radial vector `r * v`
    :type rv: np.ndarray
    :return: the second derivative plus the tuple of intermediate second derivatives
    :rtype: tuple[np.ndarray, tuple]
    """
    ...

class _dumb_comps_wrapper:
    """
    Exists solely to prevent numpy from unpacking
    """

    def __init__(self, comp):
        """
        **LLM Docstring**

        Wrap a single component object so that `numpy` will not try to unpack or
        broadcast it when it is stored inside an array or passed around alongside
        numeric data.

        :param comp: the object to shield from `numpy` unpacking
        :type comp: Any
        """
        ...

def cartesian_from_rad_derivatives(xa, xb, xc, r, a, d, i, ia, ib, ic, derivs, order=2, return_comps=False):
    """
    Returns derivatives of the generated Cartesian coordinates with respect
    to the internals
    """
    ...

def vec_norm_derivs(a, order=1, zero_thresh=None):
    """
    Derivative of the norm of `a` with respect to its components

    :param a: vector
    :type a: np.ndarray
    :param order: number of derivatives to return
    :type order: int
    :param zero_thresh:
    :type zero_thresh:
    :return: derivative tensors
    :rtype: list
    """
    ...

def vec_sin_cos_derivs(a, b, order=1, up_vectors=None, check_derivatives=False, zero_thresh=None):
    """
    Derivative of `sin(a, b)` and `cos(a, b)` with respect to both vector components

    :param a: vector
    :type a: np.ndarray
    :param a: other vector
    :type a: np.ndarray
    :param order: number of derivatives to return
    :type order: int
    :param zero_thresh: threshold for when a norm should be called 0. for numerical reasons
    :type zero_thresh: None | float
    :return: derivative tensors
    :rtype: list
    """
    ...

def coord_deriv_mat(nats, coords, axes=None, base_shape=None):
    """
    **LLM Docstring**

    Build the `(3N, 3N)` selection matrix that has `1`s on the diagonal for the
    requested Cartesian components of the requested atoms and `0`s elsewhere.

    This is effectively the Jacobian of a set of "raw Cartesian" coordinates with
    respect to the full Cartesian vector: it picks out the `axes` components of the
    atoms listed in `coords`. When `base_shape` is given the matrix is broadcast to
    carry those extra leading (structure/batch) dimensions.

    :param nats: total number of atoms
    :type nats: int
    :param coords: atom index or indices to select
    :type coords: int | Iterable[int]
    :param axes: Cartesian components to select (defaults to `[0, 1, 2]`)
    :type axes: Iterable[int] | None
    :param base_shape: optional leading shape to broadcast the matrix over
    :type base_shape: tuple[int, ...] | None
    :return: the `(..., 3N, 3N)` selection matrix
    :rtype: np.ndarray
    """
    ...

def jacobian_mat_inds(ind_lists, axes=None):
    """
    **LLM Docstring**

    Construct the fancy-index tuples used to scatter per-atom displacement values
    into a stacked `(structure, atom, axis, axis)` Jacobian array.

    For each atom-index list, an index tuple `(struct_inds, row_inds, col_inds,
    col_inds)` is produced that places one entry per requested Cartesian `axes`
    component along the diagonal of the trailing axis block.

    :param ind_lists: one list of atom indices per value to be scattered
    :type ind_lists: Iterable[int | Iterable[int]]
    :param axes: Cartesian components to fill (defaults to `[0, 1, 2]`)
    :type axes: Iterable[int] | None
    :return: one index tuple per entry in `ind_lists`
    :rtype: list[tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]
    """
    ...

def jacobian_proj_inds(ind_lists, axes=None):
    """
    **LLM Docstring**

    Like `jacobian_mat_inds`, but for a *projected* (reduced-atom-block) Jacobian.

    Each element of `ind_lists` is an `(atom_indices, block_index)` pair; the block
    index offsets the trailing column so that values land in the correct
    `3 * block` sub-block of the projected coordinate axis.

    :param ind_lists: `(atom_indices, block_index)` pairs
    :type ind_lists: Iterable[tuple]
    :param axes: Cartesian components to fill (defaults to `[0, 1, 2]`)
    :type axes: Iterable[int] | None
    :return: one index tuple per entry in `ind_lists`
    :rtype: list[tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]
    """
    ...

def fill_disp_jacob_atom(mat, ind_val_pairs, base_shape=None, axes=None):
    """
    **LLM Docstring**

    Scatter a set of `(atom_indices, value)` pairs into a displacement Jacobian,
    broadcasting the matrix over any new leading dimensions implied by the index
    shapes as needed.

    Each pair writes `value` into the diagonal Cartesian block of the listed atoms
    (via `jacobian_mat_inds`). The result is reshaped back to
    `base_shape + index_shape + (..., 3)` and squeezed when scalar indices were
    supplied.

    :param mat: the Jacobian to fill (modified/broadcast as needed)
    :type mat: np.ndarray
    :param ind_val_pairs: `(atom_indices, value)` pairs to scatter
    :type ind_val_pairs: Iterable[tuple]
    :param base_shape: leading shape of the matrix (inferred if omitted)
    :type base_shape: tuple[int, ...] | None
    :param axes: Cartesian components to fill (defaults to `[0, 1, 2]`)
    :type axes: Iterable[int] | None
    :return: the filled Jacobian
    :rtype: np.ndarray
    """
    ...

def fill_proj_jacob_atom(mat, ind_val_pairs, base_shape=None, axes=None):
    """
    **LLM Docstring**

    Scatter `(atom_indices, block_index, value)` triples into a *projected*
    Jacobian, broadcasting over any new leading dimensions implied by the index
    shapes.

    Behaves like `fill_disp_jacob_atom` but uses `jacobian_proj_inds` so that each
    value is placed in the `block_index` sub-block of the projected coordinate axis.

    :param mat: the projection Jacobian to fill
    :type mat: np.ndarray
    :param ind_val_pairs: `(atom_indices, block_index, value)` triples
    :type ind_val_pairs: Iterable[tuple]
    :param base_shape: leading shape of the matrix (inferred if omitted)
    :type base_shape: tuple[int, ...] | None
    :param axes: Cartesian components to fill (defaults to `[0, 1, 2]`)
    :type axes: Iterable[int] | None
    :return: the filled projection Jacobian
    :rtype: np.ndarray
    """
    ...
fast_proj = True

def disp_deriv_mat(coords, i, j, at_list, axes=None):
    """
    **LLM Docstring**

    Build the derivative (Jacobian) of the displacement vector between atoms `i`
    and `j` with respect to the Cartesian coordinates.

    When the module-level `fast_proj` flag is off, the full `(N, 3, 3)` Jacobian is
    returned directly. When it is on, the work is restricted to the atoms in
    `at_list`: a small `(len(at_list), 3, 3)` displacement Jacobian is built for the
    `i`/`j` pair together with a projection matrix mapping that reduced block back
    onto the full coordinate set.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param i: index of the first atom
    :type i: int
    :param j: index of the second atom
    :type j: int
    :param at_list: atoms retained in the reduced (projected) block
    :type at_list: Iterable[int]
    :param axes: Cartesian components to fill (defaults to `[0, 1, 2]`)
    :type axes: Iterable[int] | None
    :return: `(projection, displacement_jacobian)`; the projection is `None` when
        `fast_proj` is off
    :rtype: tuple[np.ndarray | None, np.ndarray]
    """
    ...

def prep_disp_expansion(coords, i, j, at_list, fixed_atoms=None, expand=True):
    """
    **LLM Docstring**

    Prepare the derivative expansion of the displacement vector `coords[j] -
    coords[i]`.

    Returns the vector itself and, when `expand` is truthy, its first-order
    Jacobian (flattened over the atom/axis dimensions), optionally zeroing out the
    rows belonging to any `fixed_atoms`. When `expand` is falsey only the raw vector
    is returned.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param i: index of the tail atom
    :type i: int
    :param j: index of the head atom
    :type j: int
    :param at_list: atoms retained in the reduced (projected) block
    :type at_list: Iterable[int]
    :param fixed_atoms: atoms whose Jacobian rows should be zeroed
    :type fixed_atoms: Iterable[int] | None
    :param expand: whether to also compute the Jacobian
    :type expand: bool
    :return: `(projection, [vector, jacobian])` when expanding, else `[vector]`
    :rtype: tuple | list
    """
    ...

def prep_expanded_mats_from_cache(expansion, i, j, at_list, root_dim=1, core_dim=0):
    """
    **LLM Docstring**

    Re-embed a cached derivative expansion that was computed on the minimal atom
    pair `(i, j)` into the larger `at_list` coordinate block.

    The cached tensors only carry entries for the two atoms; this routine places
    those entries at the correct positions (`3 * a` and `3 * b`) inside zero-padded
    tensors sized for the full `at_list`. `root_dim` counts leading derivative axes
    already accounted for, and `core_dim` counts trailing (non-derivative) core
    axes that should be preserved.

    :param expansion: cached expansion tensors (value + derivatives)
    :type expansion: list[np.ndarray]
    :param i: first cached atom index
    :type i: int
    :param j: second cached atom index
    :type j: int
    :param at_list: atoms of the target block
    :type at_list: Iterable[int]
    :param root_dim: number of leading derivative axes already present
    :type root_dim: int
    :param core_dim: number of trailing core axes to preserve
    :type core_dim: int
    :return: the re-embedded expansion tensors
    :rtype: list[np.ndarray]
    """
    ...

def prep_unit_vector_expansion_from_cache(cache, coords, i, j, at_list, *, order, expand, fixed_atoms):
    """
    **LLM Docstring**

    Prepare the derivative expansion of the *normalized* displacement vector
    (unit bond vector) between atoms `i` and `j`, reusing a cache where possible.

    When no cache is available (or `fixed_atoms`/non-expanded requests make caching
    unsafe) the norm/unit-vector expansion is computed directly from
    `prep_disp_expansion`. Otherwise the expensive `(i, j)` unit-vector expansion is
    computed once on the minimal atom pair, cached keyed by `((i, j), expand,
    fixed_atoms)`, and re-embedded into the `at_list` block with
    `prep_expanded_mats_from_cache`.

    :param cache: expansion cache (may be `None`)
    :type cache: dict | None
    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param i: index of the tail atom
    :type i: int
    :param j: index of the head atom
    :type j: int
    :param at_list: atoms retained in the reduced block
    :type at_list: Iterable[int]
    :param order: maximum derivative order
    :type order: int
    :param expand: whether to compute derivatives (vs. just the value)
    :type expand: bool
    :param fixed_atoms: atoms whose contributions should be zeroed
    :type fixed_atoms: Iterable[int] | None
    :return: `(projection, (norm_expansion, unit_vector_expansion))`
    :rtype: tuple
    """
    ...

def vec_angle_derivs(a, b, order=1, up_vectors=None, zero_thresh=None, return_comps=False):
    """
    Returns the derivatives of the angle between `a` and `b` with respect to their components

    :param a: vector
    :type a: np.ndarray
    :param b: vector
    :type b: np.ndarray
    :param order: order of derivatives to go up to
    :type order: int
    :param zero_thresh: threshold for what is zero in a vector norm
    :type zero_thresh: float | None
    :return: derivative tensors
    :rtype: list
    """
    ...

def dist_deriv(coords, i, j, /, order=1, method='expansion', fixed_atoms=None, cache=None, expanded_vectors=None, reproject=True, zero_thresh=None):
    """
    Gives the derivative of the distance between i and j with respect to coords i and coords j

    :param coords:
    :type coords: np.ndarray
    :param i: index of one of the atoms
    :type i: int | Iterable[int]
    :param j: index of the other atom
    :type j: int | Iterable[int]
    :return: derivatives of the distance with respect to atoms i, j, and k
    :rtype: list
    """
    ...

def angle_deriv(coords, i, j, k, *, order=1, method='expansion', cache=None, up_vector=None, l=None, angle_ordering='jik', fixed_atoms=None, expanded_vectors=None, reproject=True, zero_thresh=None):
    """
    Gives the derivative of the angle between i, j, and k with respect to the Cartesians

    :param coords:
    :type coords: np.ndarray
    :param i: index of the central atom
    :type i: int | Iterable[int]
    :param j: index of one of the outside atoms
    :type j: int | Iterable[int]
    :param k: index of the other outside atom
    :type k: int | Iterable[int]
    :return: derivatives of the angle with respect to atoms i, j, and k
    :rtype: np.ndarray
    """
    ...

def normal_deriv(coords, i, j, k, *, order=1, method='expansion', cache=None, up_vector=None, l=None, angle_ordering='jik', fixed_atoms=None, expanded_vectors=None, reproject=True, normalize=True):
    """
    Gives the derivative of the angle between i, j, and k with respect to the Cartesians

    :param coords:
    :type coords: np.ndarray
    :param i: index of the central atom
    :type i: int | Iterable[int]
    :param j: index of one of the outside atoms
    :type j: int | Iterable[int]
    :param k: index of the other outside atom
    :type k: int | Iterable[int]
    :return: derivatives of the angle with respect to atoms i, j, and k
    :rtype: np.ndarray
    """
    ...

def rock_deriv(coords, i, j, k, /, order=1, method='expansion', angle_ordering='ijk', cache=None, reproject=True, zero_thresh=None, fixed_atoms=None, expanded_vectors=None):
    """
    Gives the derivative of the rocking motion (symmetric bend basically)

    :param coords:
    :type coords: np.ndarray
    :param i: index of the central atom
    :type i: int | Iterable[int]
    :param j: index of one of the outside atoms
    :type j: int | Iterable[int]
    :param k: index of the other outside atom
    :type k: int | Iterable[int]
    :return: derivatives of the angle with respect to atoms i, j, and k
    :rtype: np.ndarray
    """
    ...

def dihed_deriv(coords, i, j, k, l, /, order=1, zero_thresh=None, method='expansion', fixed_atoms=None, cache=None, reproject=True, expanded_vectors=None):
    """
    Gives the derivative of the dihedral between i, j, k, and l with respect to the Cartesians
    Currently gives what are sometimes called the `psi` angles.
    Can also support more traditional `phi` angles by using a different angle ordering

    :param coords:
    :type coords: np.ndarray
    :param i:
    :type i: int | Iterable[int]
    :param j:
    :type j: int | Iterable[int]
    :param k:
    :type k: int | Iterable[int]
    :param l:
    :type l: int | Iterable[int]
    :return: derivatives of the dihedral with respect to atoms i, j, k, and l
    :rtype: np.ndarray
    """
    ...

def book_deriv(coords, i, j, k, l, /, order=1, zero_thresh=None, method='expansion', fixed_atoms=None, cache=None, reproject=True, expanded_vectors=None):
    """
    **LLM Docstring**

    Analytic derivative expansion of a *book* angle (the angle between the two
    half-planes sharing the `i`-`j` edge, defined by atoms `i`, `j`, `k`, `l`) with
    respect to the Cartesian coordinates.

    Only `method='expansion'` is implemented. It builds the displacement/unit-vector
    expansions for the three defining vectors, feeds them to
    `TensorDerivatives.vec_dihed_deriv`, and (when `reproject`) maps the derivatives
    back through the projection returned by the displacement setup.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param i: first edge atom
    :type i: int
    :param j: second edge atom
    :type j: int
    :param k: atom defining the first half-plane
    :type k: int
    :param l: atom defining the second half-plane
    :type l: int
    :param order: maximum derivative order
    :type order: int
    :param zero_thresh: threshold below which values are treated as zero
    :type zero_thresh: float | None
    :param method: derivative method (`'expansion'` only)
    :type method: str
    :param fixed_atoms: atoms whose contributions should be zeroed
    :type fixed_atoms: Iterable[int] | None
    :param cache: expansion cache
    :type cache: dict | None
    :param reproject: whether to reproject the derivatives onto the full coordinates
    :type reproject: bool
    :param expanded_vectors: which of the defining vectors to expand (defaults to all)
    :type expanded_vectors: Iterable[int] | None
    :return: the derivative expansion `[value, d1, d2, ...]`
    :rtype: list
    """
    ...

def wag_deriv(coords, i, j, k, l=None, *, order=1, method='expansion', cache=None, reproject=True, fixed_atoms=None, expanded_vectors=None):
    """
    **LLM Docstring**

    Analytic derivative expansion of a *wag* coordinate for the `i`-`j`-`k` group
    (with `j` treated as fixed) with respect to the Cartesian coordinates.

    Only `method='expansion'` is implemented. The central atom `j` is added to
    `fixed_atoms`, the defining displacement/unit-vector expansions are assembled,
    and `TensorDerivatives.vec_dihed_deriv` produces the derivatives, which are
    reprojected onto the full coordinate set when `reproject` is set.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param i: first outer atom
    :type i: int
    :param j: central atom (held fixed)
    :type j: int
    :param k: second outer atom
    :type k: int
    :param l: optional reference atom (defaults to `i`)
    :type l: int | None
    :param order: maximum derivative order
    :type order: int
    :param method: derivative method (`'expansion'` only)
    :type method: str
    :param cache: expansion cache
    :type cache: dict | None
    :param reproject: whether to reproject the derivatives
    :type reproject: bool
    :param fixed_atoms: additional atoms to hold fixed
    :type fixed_atoms: Iterable[int] | None
    :param expanded_vectors: which defining vectors to expand
    :type expanded_vectors: Iterable[int] | None
    :return: the derivative expansion `[value, d1, d2, ...]`
    :rtype: list
    """
    ...

def plane_angle_deriv(coords, i, j, k, l, m, n, /, order=1, method='expansion', fixed_atoms=None, cache=None, reproject=True, expanded_vectors=None):
    """
    **LLM Docstring**

    Analytic derivative expansion of the angle between the plane defined by atoms
    `i`, `j`, `k` and the plane defined by atoms `l`, `m`, `n`, with respect to the
    Cartesian coordinates.

    Only `method='expansion'` is implemented. Four displacement-vector expansions
    are built (two per plane) and passed to
    `TensorDerivatives.vec_plane_angle_deriv`; the result is reprojected onto the
    full coordinate set when `reproject` is set.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param i: first atom of plane 1
    :type i: int
    :param j: second atom of plane 1
    :type j: int
    :param k: third atom of plane 1
    :type k: int
    :param l: first atom of plane 2
    :type l: int
    :param m: second atom of plane 2
    :type m: int
    :param n: third atom of plane 2
    :type n: int
    :param order: maximum derivative order
    :type order: int
    :param method: derivative method (`'expansion'` only)
    :type method: str
    :param fixed_atoms: atoms whose contributions should be zeroed
    :type fixed_atoms: Iterable[int] | None
    :param cache: expansion cache
    :type cache: dict | None
    :param reproject: whether to reproject the derivatives
    :type reproject: bool
    :param expanded_vectors: which defining vectors to expand (defaults to all)
    :type expanded_vectors: Iterable[int] | None
    :return: the derivative expansion `[value, d1, d2, ...]`
    :rtype: list
    """
    ...

def oop_deriv(coords, i, j, k, l=None, *, order=1, method='expansion', fixed_atoms=None, cache=None, reproject=True, expanded_vectors=None):
    """
    **LLM Docstring**

    Analytic derivative expansion of an *out-of-plane* coordinate for the
    `i`-`j`-`k` group (with `j` treated as fixed) with respect to the Cartesian
    coordinates.

    Only `method='expansion'` is implemented. The out-of-plane value is formed as
    the difference of two dihedral-style derivatives (one holding the `k` vector
    frozen, one holding the `i` vector frozen), then reprojected onto the full
    coordinate set when `reproject` is set.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param i: first outer atom
    :type i: int
    :param j: central atom (held fixed)
    :type j: int
    :param k: second outer atom
    :type k: int
    :param l: optional reference atom (defaults to `i`)
    :type l: int | None
    :param order: maximum derivative order
    :type order: int
    :param method: derivative method (`'expansion'` only)
    :type method: str
    :param fixed_atoms: additional atoms to hold fixed
    :type fixed_atoms: Iterable[int] | None
    :param cache: expansion cache
    :type cache: dict | None
    :param reproject: whether to reproject the derivatives
    :type reproject: bool
    :param expanded_vectors: which defining vectors to expand
    :type expanded_vectors: Iterable[int] | None
    :return: the derivative expansion `[value, d1, d2, ...]`
    :rtype: list
    """
    ...

def transrot_deriv(coords, *pos, order=1, masses=None, return_rot=True, return_frame=False, cache=None, reproject=True, axes=None, fixed_atoms=None):
    """
    **LLM Docstring**

    Derivative expansion of the translation (center of mass) and, optionally,
    rotation degrees of freedom of a (sub)set of atoms with respect to the
    Cartesian coordinates.

    The center of mass and the translation/rotation eigenvectors are obtained from
    `CoordinateFrames.translation_rotation_eigenvectors`. When atom positions `pos`
    are supplied only those atoms contribute; their eigenvectors are scattered back
    into the full `3N` coordinate space and rows for `fixed_atoms` are zeroed.
    Higher-order terms are exact zeros for these (linear) coordinates.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param pos: atom indices defining the fragment (empty = all atoms)
    :type pos: int
    :param order: maximum derivative order
    :type order: int
    :param masses: per-atom masses (defaults to unit masses)
    :type masses: np.ndarray | None
    :param return_rot: whether to include the rotational modes
    :type return_rot: bool
    :param return_frame: whether to also return the principal-axis frame
    :type return_frame: bool
    :param cache: expansion cache (unused here, kept for interface parity)
    :type cache: dict | None
    :param reproject: kept for interface parity
    :type reproject: bool
    :param axes: optional fixed principal axes to use
    :type axes: np.ndarray | None
    :param fixed_atoms: atoms whose contributions should be zeroed
    :type fixed_atoms: Iterable[int] | None
    :return: the expansion, or `(expansion, principal_axes)` if `return_frame`
    :rtype: list | tuple
    """
    ...

def com_dist_deriv(coords, frame_pos_1, frame_pos_2, *, order=1, masses=None, cache=None, reproject=True, fixed_atoms=None):
    """
    **LLM Docstring**

    Derivative expansion of the distance between the centers of mass of two atom
    fragments with respect to the Cartesian coordinates.

    The center-of-mass expansions of the two fragments (from `transrot_deriv` with
    rotation disabled) are subtracted and the norm of the resulting vector is
    expanded via `TensorDerivatives.vec_norm_unit_deriv`.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param frame_pos_1: atom indices of the first fragment
    :type frame_pos_1: Iterable[int]
    :param frame_pos_2: atom indices of the second fragment
    :type frame_pos_2: Iterable[int]
    :param order: maximum derivative order
    :type order: int
    :param masses: per-atom masses
    :type masses: np.ndarray | None
    :param cache: expansion cache (interface parity)
    :type cache: dict | None
    :param reproject: interface parity
    :type reproject: bool
    :param fixed_atoms: atoms whose contributions should be zeroed
    :type fixed_atoms: Iterable[int] | None
    :return: the norm derivative expansion `[value, d1, d2, ...]`
    :rtype: list
    """
    ...

def moment_of_inertia_expansion_deriv(coords, *pos, order=1, masses=None, cache=None, reproject=True, fixed_atoms=None):
    """
    **LLM Docstring**

    Derivative expansion of the moments of inertia (eigenvalues) and principal
    axes (eigenvectors) of a (sub)set of atoms with respect to the Cartesian
    coordinates.

    The expansion is obtained from `CoordinateFrames.moments_of_inertia_expansion`;
    when only a subset `pos` of atoms is used, the value/vector derivative tensors
    are scattered back into the full `3N` coordinate space, and rows for
    `fixed_atoms` are zeroed.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param pos: atom indices defining the fragment (empty = all atoms)
    :type pos: int
    :param order: maximum derivative order
    :type order: int
    :param masses: per-atom masses
    :type masses: np.ndarray | None
    :param cache: expansion cache (interface parity)
    :type cache: dict | None
    :param reproject: interface parity
    :type reproject: bool
    :param fixed_atoms: atoms whose contributions should be zeroed
    :type fixed_atoms: Iterable[int] | None
    :return: `(eigenvalue_expansion, eigenvector_expansion)`
    :rtype: tuple[list, list]
    """
    ...

def _frame_data(coords, *pos, masses=None):
    """
    **LLM Docstring**

    Return the moments of inertia and center of mass for a (sub)set of atoms.

    Thin wrapper around `CoordinateFrames.moments_of_inertia` that optionally
    restricts to the atoms in `pos` (slicing the masses to match) before requesting
    the center of mass alongside the inertia data.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param pos: atom indices defining the fragment (empty = all atoms)
    :type pos: int
    :param masses: per-atom masses
    :type masses: np.ndarray | None
    :return: the moments of inertia together with the center of mass
    :rtype: tuple
    """
    ...

def _rot_deriv_vecs(axes, coords, com=None):
    """
    **LLM Docstring**

    Compute the infinitesimal-rotation displacement vectors for a set of frames.

    For each frame the rotation generators are formed by contracting the axis
    system with the Levi-Civita tensor, and those generators act on the
    (center-of-mass-shifted) coordinates to give, for every Cartesian degree of
    freedom, its response to an infinitesimal rotation about each principal axis.

    :param axes: stacked `(..., 3, 3)` principal-axis frames
    :type axes: np.ndarray
    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param com: centers of mass to shift by (optional)
    :type com: np.ndarray | None
    :return: rotation displacement vectors, shape `(..., 3N, 3)`
    :rtype: np.ndarray
    """
    ...

def _orientation_axis_system(coords, frame_pos_1, frame_pos_2, masses):
    """
    **LLM Docstring**

    Build the shared axis system used to define the relative *orientation*
    coordinate between two atom fragments.

    Each fragment contributes a center of mass and a principal-axis frame; the
    inter-fragment vector (`com2 - com1`) and the cross product of the two `z`
    axes define a viewing frame via `TransformationMatrices.view_matrix`.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param frame_pos_1: atom indices of the first fragment
    :type frame_pos_1: Iterable[int]
    :param frame_pos_2: atom indices of the second fragment
    :type frame_pos_2: Iterable[int]
    :param masses: per-atom masses
    :type masses: np.ndarray
    :return: `((com1, axes1), (com2, axes2), view_matrix)`
    :rtype: tuple
    """
    ...

def orientation_deriv(coords, frame_pos_1, frame_pos_2, *, order=1, masses=None, fixed_atoms=None, cache=None, reproject=True, return_frame=False, return_rot=True):
    """
    **LLM Docstring**

    Derivative expansion of the relative orientation coordinate between two atom
    fragments with respect to the Cartesian coordinates.

    Both fragments are expanded with `transrot_deriv` in the shared axis system from
    `_orientation_axis_system`, then combined with mass-weighted coefficients
    `p1 = m1 / sqrt(m1^2 + m2^2)` and `p2 = m2 / sqrt(m1^2 + m2^2)`. (The commented
    block preserves an earlier angle-based formulation.)

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param frame_pos_1: atom indices of the first fragment
    :type frame_pos_1: Iterable[int]
    :param frame_pos_2: atom indices of the second fragment
    :type frame_pos_2: Iterable[int]
    :param order: maximum derivative order
    :type order: int
    :param masses: per-atom masses (defaults to unit masses)
    :type masses: np.ndarray | None
    :param fixed_atoms: atoms whose contributions should be zeroed
    :type fixed_atoms: Iterable[int] | None
    :param cache: expansion cache (interface parity)
    :type cache: dict | None
    :param reproject: interface parity
    :type reproject: bool
    :param return_frame: whether to also return the per-fragment frames
    :type return_frame: bool
    :param return_rot: whether to include rotational modes
    :type return_rot: bool
    :return: the expansion, or `(expansion, frames)` if `return_frame`
    :rtype: list | tuple
    """
    ...

def _pop_bond_vecs(bond_tf, i, j, coords):
    """
    **LLM Docstring**

    Scatter a bond-vector transformation into the full flattened Cartesian
    coordinate layout for atoms `i` and `j`.

    Delegates to `_fill_derivs` (expansion method) with a zero value term and the
    supplied bond transformation, returning the first-order (flattened) tensor.

    :param bond_tf: the bond-vector transformation to place
    :type bond_tf: np.ndarray
    :param i: first atom index
    :type i: int
    :param j: second atom index
    :type j: int
    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :return: the scattered, flattened bond-vector tensor
    :rtype: np.ndarray
    """
    ...

def _fill_derivs(coords, idx, derivs, method='old'):
    """
    **LLM Docstring**

    Scatter compact per-atom derivative tensors (indexed only by the atoms in
    `idx`) into full tensors indexed over all atoms, then flatten the atom/axis
    dimensions.

    Two layouts are supported: the legacy `'old'` method iterates the index
    product explicitly, while any other method uses vectorized fancy indexing into
    the flattened `3N` layout. The zeroth-order value term is passed through
    unchanged.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param idx: the atom indices the compact tensors are defined over
    :type idx: Iterable[int | None]
    :param derivs: the compact expansion `[value, d1, d2, ...]`
    :type derivs: list[np.ndarray]
    :param method: `'old'` for the explicit path, else the vectorized path
    :type method: str
    :return: the scattered, flattened expansion
    :rtype: list[np.ndarray]
    """
    ...

def dist_vec(coords, i, j, order=None, method='expansion', cache=None, reproject=True, fixed_atoms=None):
    """
    Returns the full vectors that define the linearized version of a bond displacement

    :param coords:
    :param i:
    :param j:
    :return:
    """
    ...

def angle_vec(coords, i, j, k, order=None, up_vector=None, l=None, method='expansion', angle_ordering='ijk', cache=None, reproject=True, fixed_atoms=None):
    """
    Returns the full vectors that define the linearized version of an angle displacement

    :param coords:
    :param i:
    :param j:
    :return:
    """
    ...

def rock_vec(coords, i, j, k, order=None, method='expansion', cache=None, reproject=True, angle_ordering='ijk', fixed_atoms=None):
    """
    Returns the full vectors that define the linearized version of an angle displacement

    :param coords:
    :param i:
    :param j:
    :return:
    """
    ...

def dihed_vec(coords, i, j, k, l, order=None, method='expansion', cache=None, reproject=True, fixed_atoms=None):
    """
    Returns the full vectors that define the linearized version of a dihedral displacement

    :param coords:
    :param i:
    :param j:
    :return:
    """
    ...

def book_vec(coords, i, j, k, l, order=None, method='expansion', cache=None, reproject=True, fixed_atoms=None):
    """
    Returns the full vectors that define the linearized version of a dihedral displacement

    :param coords:
    :param i:
    :param j:
    :return:
    """
    ...

def oop_vec(coords, i, j, k, l=None, order=None, method='expansion', cache=None, reproject=True, fixed_atoms=None):
    """
    Returns the full vectors that define the linearized version of an oop displacement

    :param coords:
    :param i:
    :param j:
    :return:
    """
    ...

def wag_vec(coords, i, j, k, l=None, order=None, method='expansion', cache=None, reproject=True, fixed_atoms=None):
    """
    Returns the full vectors that define the linearized version of an oop displacement

    :param coords:
    :param i:
    :param j:
    :return:
    """
    ...

def plane_angle_vec(coords, i, j, k, l, m, n, order=None, method='expansion', cache=None, reproject=True, fixed_atoms=None):
    """
    **LLM Docstring**

    Convenience wrapper returning the plane-angle derivative(s) as bare vectors.

    Calls `plane_angle_deriv` and, when `order is None`, returns just the
    first-derivative term; otherwise returns the full expansion. When `reproject`
    is off the derivatives are scattered onto the full coordinate set via
    `_fill_derivs`.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param i: first atom of plane 1
    :type i: int
    :param j: second atom of plane 1
    :type j: int
    :param k: third atom of plane 1
    :type k: int
    :param l: first atom of plane 2
    :type l: int
    :param m: second atom of plane 2
    :type m: int
    :param n: third atom of plane 2
    :type n: int
    :param order: derivative order (`None` returns only the first derivative)
    :type order: int | None
    :param method: derivative method (`'expansion'` only)
    :type method: str
    :param cache: expansion cache
    :type cache: dict | None
    :param reproject: whether to reproject the derivatives
    :type reproject: bool
    :param fixed_atoms: atoms whose contributions should be zeroed
    :type fixed_atoms: Iterable[int] | None
    :return: the plane-angle derivative vector(s)
    :rtype: np.ndarray | list
    """
    ...

def transrot_vecs(coords, *pos, order=None, masses=None, return_rot=True, cache=None, reproject=True, fixed_atoms=None):
    """
    **LLM Docstring**

    Convenience wrapper returning the translation/rotation derivative(s) as bare
    vectors.

    Calls `transrot_deriv`; when `order is None` returns only the first-derivative
    term, otherwise the full expansion.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param pos: atom indices defining the fragment (empty = all atoms)
    :type pos: int
    :param order: derivative order (`None` returns only the first derivative)
    :type order: int | None
    :param masses: per-atom masses
    :type masses: np.ndarray | None
    :param return_rot: whether to include rotational modes
    :type return_rot: bool
    :param cache: expansion cache (interface parity)
    :type cache: dict | None
    :param reproject: interface parity
    :type reproject: bool
    :param fixed_atoms: atoms whose contributions should be zeroed
    :type fixed_atoms: Iterable[int] | None
    :return: the translation/rotation derivative vector(s)
    :rtype: np.ndarray | list
    """
    ...

def orientation_vecs(coords, frame_pos_1, frame_pos_2, *, order=None, masses=None, cache=None, reproject=True, fixed_atoms=None, return_rot=True):
    """
    **LLM Docstring**

    Convenience wrapper returning the orientation-coordinate derivative(s) as bare
    vectors.

    Calls `orientation_deriv`; when `order is None` returns only the
    first-derivative term, otherwise the full expansion.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param frame_pos_1: atom indices of the first fragment
    :type frame_pos_1: Iterable[int]
    :param frame_pos_2: atom indices of the second fragment
    :type frame_pos_2: Iterable[int]
    :param order: derivative order (`None` returns only the first derivative)
    :type order: int | None
    :param masses: per-atom masses
    :type masses: np.ndarray | None
    :param cache: expansion cache (interface parity)
    :type cache: dict | None
    :param reproject: interface parity
    :type reproject: bool
    :param fixed_atoms: atoms whose contributions should be zeroed
    :type fixed_atoms: Iterable[int] | None
    :param return_rot: whether to include rotational modes
    :type return_rot: bool
    :return: the orientation derivative vector(s)
    :rtype: np.ndarray | list
    """
    ...

def internal_conversion_specs(specs, angle_ordering='ijk', coord_type_dispatch=None, **opts):
    """
    **LLM Docstring**

    Normalize a list of coordinate specifications into `(function, indices,
    options)` triples ready for evaluation.

    Each spec may be a dict (whose key names the coordinate type), an object
    exposing `get_expansion` (for integration with the `Internals` machinery), or a
    bare index tuple whose length implies the type (`2` -> distance, `3` -> bend,
    `4` -> dihedral). Bend/rock specs inherit the default `angle_ordering` unless
    overridden.

    :param specs: the coordinate specifications to normalize
    :type specs: Iterable
    :param angle_ordering: default angle-index ordering for bend/rock coordinates
    :type angle_ordering: str
    :param coord_type_dispatch: mapping from type name to derivative function
        (defaults to `coord_type_map`)
    :type coord_type_dispatch: dict | None
    :param opts: extra options merged into every spec's option dict
    :return: list of `(function, indices, options)` triples
    :rtype: list[tuple]
    """
    ...

def combine_coordinate_deriv_expansions(expansions, order=None, base_dim=0, base_transformation=None, reference_internals=None):
    """
    **LLM Docstring**

    Concatenate the per-coordinate derivative expansions into a single stacked
    expansion for the full internal-coordinate set.

    Each coordinate's tensors are expanded along a new trailing coordinate axis and
    concatenated. When an `order` is given the value term and derivative terms are
    handled separately: reference internals are subtracted, and an optional
    `base_transformation` is applied (via `TensorDerivatives.tensor_reexpand`) to
    re-express the coordinates and their derivatives in a new basis.

    :param expansions: per-coordinate expansions to combine
    :type expansions: list
    :param order: maximum derivative order (`None` = values only)
    :type order: int | None
    :param base_dim: number of leading (structure/batch) dimensions
    :type base_dim: int
    :param base_transformation: optional transformation into a new coordinate basis
    :type base_transformation: list[np.ndarray] | None
    :param reference_internals: reference values subtracted from the internals
    :type reference_internals: np.ndarray | None
    :return: the combined expansion `[internals, d1, d2, ...]`
    :rtype: list
    """
    ...

def internal_conversion_function(specs, base_transformation=None, reference_internals=None, use_cache=True, reproject=False, **opts):
    """
    **LLM Docstring**

    Build a reusable Cartesian-to-internal conversion function from a set of
    coordinate specifications.

    The specs are normalized once with `internal_conversion_specs`; the returned
    `convert` closure evaluates every coordinate's derivative expansion for a given
    Cartesian geometry and stitches them together with
    `combine_coordinate_deriv_expansions`, optionally applying a base
    transformation and reference internals.

    :param specs: the coordinate specifications
    :type specs: Iterable
    :param base_transformation: optional transformation into a new coordinate basis
    :type base_transformation: list[np.ndarray] | None
    :param reference_internals: reference internal values to subtract
    :type reference_internals: np.ndarray | None
    :param use_cache: whether to share an expansion cache across coordinates
    :type use_cache: bool
    :param reproject: whether individual coordinate derivatives are reprojected
    :type reproject: bool
    :param opts: options forwarded to `internal_conversion_specs`
    :return: a `convert(coords, order=None)` function
    :rtype: Callable
    """
    ...

def internal_coordinate_tensors(coords, specs, order=None, return_inverse=False, masses=None, fixed_atoms=None, fixed_cartesians=None, fixed_coords=None, remove_inverse_translation_rotation=True, **opts):
    """
    **LLM Docstring**

    Compute the internal coordinates for a geometry together with their forward
    (and optionally inverse) derivative tensors.

    The forward expansion comes from `internal_conversion_function`; its derivative
    terms are cleaned with `prep_internal_derivatives` (zeroing fixed
    atoms/Cartesians/coordinates). When `return_inverse` is set the inverse
    transformation is also produced via `inverse_internal_coordinate_tensors`.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param specs: the coordinate specifications
    :type specs: Iterable
    :param order: maximum derivative order (`None` = values only)
    :type order: int | None
    :param return_inverse: whether to also return the inverse tensors
    :type return_inverse: bool
    :param masses: per-atom masses (used for the inverse)
    :type masses: np.ndarray | None
    :param fixed_atoms: atoms to hold fixed
    :type fixed_atoms: Iterable[int] | None
    :param fixed_cartesians: `(atom, component)` Cartesians to hold fixed
    :type fixed_cartesians: Iterable | None
    :param fixed_coords: internal coordinates to hold fixed
    :type fixed_coords: Iterable[int] | None
    :param remove_inverse_translation_rotation: strip translation/rotation from the
        inverse
    :type remove_inverse_translation_rotation: bool
    :param opts: options forwarded to the conversion function
    :return: the forward tensors, or `(forward, inverse)` if `return_inverse`
    :rtype: list | tuple
    """
    ...

def prep_internal_derivatives(expansion, fixed_atoms=None, fixed_coords=None, fixed_cartesians=None):
    """
    **LLM Docstring**

    Zero out the requested constraints in a *forward* (internals-by-Cartesians)
    derivative expansion.

    Fixed atoms and fixed Cartesian components are zeroed along every Cartesian
    (input) axis of each derivative tensor, while fixed internal coordinates are
    zeroed along the output axis. The expansion is copied before the first
    modification so the input is left untouched.

    :param expansion: the forward derivative expansion
    :type expansion: list[np.ndarray]
    :param fixed_atoms: atoms to hold fixed
    :type fixed_atoms: Iterable[int] | None
    :param fixed_coords: internal coordinates to hold fixed
    :type fixed_coords: Iterable[int] | None
    :param fixed_cartesians: `(atom, component)` Cartesians to hold fixed
    :type fixed_cartesians: Iterable | None
    :return: the constrained expansion
    :rtype: list[np.ndarray]
    """
    ...

def prep_inverse_derivatives(expansion, fixed_atoms=None, fixed_coords=None, fixed_cartesians=None):
    """
    **LLM Docstring**

    Zero out the requested constraints in an *inverse* (Cartesians-by-internals)
    derivative expansion.

    The Cartesian axis is now the output, so fixed atoms/Cartesians are zeroed along
    the trailing (Cartesian) axis while fixed internal coordinates are zeroed along
    the input axes. The expansion is copied before the first modification.

    :param expansion: the inverse derivative expansion
    :type expansion: list[np.ndarray]
    :param fixed_atoms: atoms to hold fixed
    :type fixed_atoms: Iterable[int] | None
    :param fixed_coords: internal coordinates to hold fixed
    :type fixed_coords: Iterable[int] | None
    :param fixed_cartesians: `(atom, component)` Cartesians to hold fixed
    :type fixed_cartesians: Iterable | None
    :return: the constrained expansion
    :rtype: list[np.ndarray]
    """
    ...
_transrot_projection_method = 'addition'
_pre_mass_weight = True

def inverse_internal_coordinate_tensors(expansion, coords=None, masses=None, order=None, mass_weighted=True, remove_translation_rotation=True, fixed_atoms=None, fixed_coords=None, fixed_cartesians=None):
    """
    **LLM Docstring**

    Invert a forward internals-by-Cartesians derivative expansion to obtain the
    Cartesians-by-internals expansion, optionally removing translation/rotation and
    mass-weighting.

    Depending on the module flags `_transrot_projection_method` and
    `_pre_mass_weight`, the translation/rotation subspace is either projected out
    or augmented onto the transformation before the (pseudo)inverse is taken with
    `TensorDerivatives.inverse_transformation`; mass weighting is applied and undone
    around the inversion. Constraints are re-applied with `prep_inverse_derivatives`.

    :param expansion: the forward derivative expansion
    :type expansion: list[np.ndarray]
    :param coords: Cartesian coordinates (needed to remove translation/rotation)
    :type coords: np.ndarray | None
    :param masses: per-atom masses
    :type masses: np.ndarray | None
    :param order: maximum derivative order (defaults to `len(expansion)`)
    :type order: int | None
    :param mass_weighted: whether to mass-weight the plain inverse
    :type mass_weighted: bool
    :param remove_translation_rotation: whether to strip translation/rotation
    :type remove_translation_rotation: bool
    :param fixed_atoms: atoms to hold fixed
    :type fixed_atoms: Iterable[int] | None
    :param fixed_coords: internal coordinates to hold fixed
    :type fixed_coords: Iterable[int] | None
    :param fixed_cartesians: `(atom, component)` Cartesians to hold fixed
    :type fixed_cartesians: Iterable | None
    :return: the inverse derivative expansion
    :rtype: list[np.ndarray]
    """
    ...

def rotation_expansion_from_axis_angle(coords, axis, order=1, *, angle=0.0, axis_order=0):
    """
    **LLM Docstring**

    Build the derivative expansion of coordinates rotated about a given axis, taken
    with respect to either the rotation angle or the axis itself.

    The rotation-generator derivatives come from `Geometry.axis_rot_gen_deriv`. With
    `axis_order = 0` the expansion is taken in the angle; otherwise it is taken in
    the axis components. A batched axis whose leading shape matches the coordinates
    is handled by looping over the batch (a slow path); mismatched broadcasting is
    not supported.

    :param coords: coordinates to rotate, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param axis: rotation axis (normalized internally)
    :type axis: np.ndarray
    :param order: maximum derivative order
    :type order: int
    :param angle: rotation angle
    :type angle: float
    :param axis_order: `0` to differentiate w.r.t. the angle, else w.r.t. the axis
    :type axis_order: int
    :return: the rotated-coordinate expansion `[value, d1, d2, ...]`
    :rtype: list[np.ndarray]
    """
    ...

def _handle_expansion_atom_exclusions(coords, left_expansion, right_expansion, left_atoms, right_atoms):
    """
    **LLM Docstring**

    Merge a "left" and a "right" coordinate expansion into a single expansion with
    the correct per-atom ownership.

    Atoms belonging to the left group take the left expansion's values/derivatives,
    atoms belonging to neither group keep their unrotated Cartesian value and get
    zero derivatives, and remaining atoms keep the right expansion. The right
    expansion is modified in place and returned.

    :param coords: Cartesian coordinates, shape `(N, 3)`
    :type coords: np.ndarray
    :param left_expansion: expansion for the left atom group
    :type left_expansion: list[np.ndarray]
    :param right_expansion: expansion for the right atom group (modified in place)
    :type right_expansion: list[np.ndarray]
    :param left_atoms: atoms owned by the left group
    :type left_atoms: Iterable[int]
    :param right_atoms: atoms owned by the right group
    :type right_atoms: Iterable[int]
    :return: the merged expansion
    :rtype: list[np.ndarray]
    """
    ...

def dist_expansion(coords, i, j, order=1, left_atoms=None, right_atoms=None, *, include_core=True, amount=0):
    """
    **LLM Docstring**

    Build the finite-displacement expansion of the coordinates associated with
    stretching the `i`-`j` bond.

    Atoms on the `i` side are displaced by `-vec` and atoms on the `j` side by
    `+vec` (half the normalized bond vector), with a first-order term equal to that
    unit direction and higher-order terms zero. Group membership (and unaffected
    atoms) is resolved by `_handle_expansion_atom_exclusions`.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param i: tail atom of the bond
    :type i: int
    :param j: head atom of the bond
    :type j: int
    :param order: maximum expansion order
    :type order: int
    :param left_atoms: atoms moving with `i` (defaults to `[i]`)
    :type left_atoms: Iterable[int] | None
    :param right_atoms: atoms moving with `j` (defaults to `[j]`)
    :type right_atoms: Iterable[int] | None
    :param include_core: whether to prepend the core atom to the group lists
    :type include_core: bool
    :param amount: displacement magnitude applied to the value term
    :type amount: float
    :return: the displacement expansion `[coords, d1, ...]`
    :rtype: list[np.ndarray]
    """
    ...

def angle_expansion(coords, i, j, k, order=1, left_atoms=None, right_atoms=None, *, include_core=True, angle=0, axis_order=0):
    """
    **LLM Docstring**

    Build the finite-rotation expansion of the coordinates associated with opening
    the `i`-`j`-`k` bend.

    The two arms are rotated by equal and opposite half-angles about the axis normal
    to the `i`-`j`-`k` plane (using `rotation_expansion_from_axis_angle`), shifted so
    `j` sits at the origin and back again. Group ownership is resolved by
    `_handle_expansion_atom_exclusions`, and derivative terms are halved to account
    for the split rotation.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param i: first outer atom
    :type i: int
    :param j: vertex atom
    :type j: int
    :param k: second outer atom
    :type k: int
    :param order: maximum expansion order
    :type order: int
    :param left_atoms: atoms moving with `i` (defaults to `[i]`)
    :type left_atoms: Iterable[int] | None
    :param right_atoms: atoms moving with `k` (defaults to `[k]`)
    :type right_atoms: Iterable[int] | None
    :param include_core: whether to prepend the core atom to the group lists
    :type include_core: bool
    :param angle: total displacement angle
    :type angle: float
    :param axis_order: differentiation order w.r.t. the axis (see
        `rotation_expansion_from_axis_angle`)
    :type axis_order: int
    :return: the rotation expansion `[coords, d1, ...]`
    :rtype: list[np.ndarray]
    """
    ...

def dihed_expansion(coords, i, j, k, l, order=1, left_atoms=None, right_atoms=None, *, include_core=True, angle=0, axis_order=0):
    """
    **LLM Docstring**

    Build the finite-rotation expansion of the coordinates associated with twisting
    the `i`-`j`-`k`-`l` dihedral.

    The two halves are rotated by equal and opposite half-angles about the `j`-`k`
    bond axis (shifted so `k` is at the origin), with group ownership resolved by
    `_handle_expansion_atom_exclusions` and derivative terms halved.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param i: first terminal atom
    :type i: int
    :param j: first central atom
    :type j: int
    :param k: second central atom
    :type k: int
    :param l: second terminal atom
    :type l: int
    :param order: maximum expansion order
    :type order: int
    :param left_atoms: atoms moving with `i` (defaults to `[i]`)
    :type left_atoms: Iterable[int] | None
    :param right_atoms: atoms moving with `l` (defaults to `[l]`)
    :type right_atoms: Iterable[int] | None
    :param include_core: whether to prepend the core atom to the group lists
    :type include_core: bool
    :param angle: total twist angle
    :type angle: float
    :param axis_order: differentiation order w.r.t. the axis
    :type axis_order: int
    :return: the rotation expansion `[coords, d1, ...]`
    :rtype: list[np.ndarray]
    """
    ...

def oop_expansion(coords, i, j, k, order=1, left_atoms=None, right_atoms=None, *, include_core=True, angle=0, axis_order=0):
    """
    **LLM Docstring**

    Build the finite-rotation expansion of the coordinates associated with an
    out-of-plane bend of the `i`-`j`-`k` group.

    The two halves are rotated by opposite half-angles about the averaged
    `i`/`k` direction (relative to the vertex `j`), with group ownership resolved by
    `_handle_expansion_atom_exclusions` and derivative terms halved.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param i: first outer atom
    :type i: int
    :param j: vertex atom
    :type j: int
    :param k: second outer atom
    :type k: int
    :param order: maximum expansion order
    :type order: int
    :param left_atoms: atoms moving with `i` (defaults to `[i]`)
    :type left_atoms: Iterable[int] | None
    :param right_atoms: atoms moving with `k` (defaults to `[k]`)
    :type right_atoms: Iterable[int] | None
    :param include_core: whether to prepend the core atom to the group lists
    :type include_core: bool
    :param angle: total displacement angle
    :type angle: float
    :param axis_order: differentiation order w.r.t. the axis
    :type axis_order: int
    :return: the rotation expansion `[coords, d1, ...]`
    :rtype: list[np.ndarray]
    """
    ...

def wag_expansion(coords, i, j, k, order=1, left_atoms=None, right_atoms=None, *, include_core=True, angle=0, axis_order=0):
    """
    **LLM Docstring**

    Build the finite-rotation expansion of the coordinates associated with a wag of
    the `i`-`j`-`k` group.

    Both halves are rotated by the same half-angle about the averaged `i`/`k`
    direction (relative to the vertex `j`); group ownership is resolved by
    `_handle_expansion_atom_exclusions` and derivative terms are halved.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param i: first outer atom
    :type i: int
    :param j: vertex atom
    :type j: int
    :param k: second outer atom
    :type k: int
    :param order: maximum expansion order
    :type order: int
    :param left_atoms: atoms moving with `i` (defaults to `[i]`)
    :type left_atoms: Iterable[int] | None
    :param right_atoms: atoms moving with `k` (defaults to `[k]`)
    :type right_atoms: Iterable[int] | None
    :param include_core: whether to prepend the core atom to the group lists
    :type include_core: bool
    :param angle: total displacement angle
    :type angle: float
    :param axis_order: differentiation order w.r.t. the axis
    :type axis_order: int
    :return: the rotation expansion `[coords, d1, ...]`
    :rtype: list[np.ndarray]
    """
    ...

def transrot_expansion(coords, *pos, order=1, shift=None, rotation=None, masses=None, axes=None, extra_atoms=None, return_rot=True, return_frame=False):
    """
    **LLM Docstring**

    Build the finite-displacement expansion of the coordinates associated with
    translating and/or rotating an atom fragment as a rigid body.

    The fragment (`pos` plus any `extra_atoms`) is optionally shifted along, and
    rotated about, its principal axes, then the mass-weighted translation/rotation
    eigenvectors from `CoordinateFrames.translation_rotation_eigenvectors` are
    scattered into the full `3N` coordinate space to form the first-order term.
    Higher-order terms are zero.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param pos: atom indices defining the fragment (empty = all atoms)
    :type pos: int
    :param order: maximum expansion order
    :type order: int
    :param shift: translation applied in the principal-axis frame
    :type shift: np.ndarray | None
    :param rotation: per-axis rotation angles
    :type rotation: np.ndarray | None
    :param masses: per-atom masses (defaults to unit masses)
    :type masses: np.ndarray | None
    :param axes: optional fixed principal axes
    :type axes: np.ndarray | None
    :param extra_atoms: additional atoms carried with the fragment
    :type extra_atoms: Iterable[int] | None
    :param return_rot: whether to include rotational modes
    :type return_rot: bool
    :param return_frame: whether to also return the frame
    :type return_frame: bool
    :return: the expansion, or `(expansion, frame)` if `return_frame`
    :rtype: list | tuple
    """
    ...

def orientation_expansion(coords, frame_pos_1, frame_pos_2, *, order=1, masses=None, fixed_atoms=None, cache=None, reproject=True, return_frame=False, left_extra_atoms=None, right_extra_atoms=None, shift=None, rotation=None, return_rot=True):
    """
    **LLM Docstring**

    Build the finite-displacement expansion of the relative orientation coordinate
    between two atom fragments.

    Each fragment is expanded with `transrot_expansion` in the shared axis system
    from `_orientation_axis_system`, with the applied `shift`/`rotation` split
    between the fragments by the mass-weighted coefficients `p1` and `p2`. The two
    expansions are combined through `_handle_expansion_atom_exclusions`. (The long
    commented block preserves an earlier explicit-construction approach.)

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param frame_pos_1: atom indices of the first fragment
    :type frame_pos_1: Iterable[int]
    :param frame_pos_2: atom indices of the second fragment
    :type frame_pos_2: Iterable[int]
    :param order: maximum expansion order
    :type order: int
    :param masses: per-atom masses (defaults to unit masses)
    :type masses: np.ndarray | None
    :param fixed_atoms: atoms to hold fixed
    :type fixed_atoms: Iterable[int] | None
    :param cache: expansion cache (interface parity)
    :type cache: dict | None
    :param reproject: interface parity
    :type reproject: bool
    :param return_frame: whether to also return the frame
    :type return_frame: bool
    :param left_extra_atoms: extra atoms carried with the first fragment
    :type left_extra_atoms: Iterable[int] | None
    :param right_extra_atoms: extra atoms carried with the second fragment
    :type right_extra_atoms: Iterable[int] | None
    :param shift: relative translation to apply
    :type shift: np.ndarray | None
    :param rotation: relative rotation to apply
    :type rotation: np.ndarray | None
    :param return_rot: whether to include rotational modes
    :type return_rot: bool
    :return: the orientation expansion
    :rtype: list[np.ndarray]
    """
    ...

def combine_coordinate_inverse_expansions(expansions, order=None, base_dim=None, base_transformation=None):
    """
    **LLM Docstring**

    Concatenate the per-coordinate *inverse* (Cartesians-by-internals) expansions
    into one stacked inverse expansion.

    Each sub-expansion's tensors are expanded along new leading internal-coordinate
    axes and concatenated with `TensorDerivatives.concatenate_expansions`. An
    optional `base_transformation` re-expresses the result via
    `TensorDerivatives.tensor_reexpand`. When `order is None` only the first-order
    block is returned; otherwise the coordinate values are prepended.

    :param expansions: per-coordinate inverse expansions
    :type expansions: list
    :param order: maximum derivative order (`None` = first order only)
    :type order: int | None
    :param base_dim: number of leading dimensions (inferred if omitted)
    :type base_dim: int | None
    :param base_transformation: optional transformation to apply
    :type base_transformation: list[np.ndarray] | None
    :return: the combined inverse expansion
    :rtype: list
    """
    ...

class _inverse_coordinate_conversion_caller:

    def __init__(self, conversion, target_internals, remove_translation_rotation=True, masses=None, order=1, gradient_function=None, gradient_scaling=None, fixed_atoms=None, fixed_coords=None):
        """
        **LLM Docstring**

        Store the configuration used to drive the iterative Cartesian-from-internal
        solve.

        Holds the forward conversion function, the target internal values, mass and
        constraint information, the optional external gradient function/scaling, and the
        derivative order. `last_call` caches the most recent forward expansion so the
        value and Jacobian evaluations can share work.

        :param conversion: forward Cartesian-to-internal conversion function
        :type conversion: Callable
        :param target_internals: internal values being solved for
        :type target_internals: np.ndarray
        :param remove_translation_rotation: whether to strip translation/rotation
        :type remove_translation_rotation: bool
        :param masses: per-atom masses
        :type masses: np.ndarray | None
        :param order: derivative order used in the Jacobian
        :type order: int
        :param gradient_function: optional external gradient (e.g. a potential)
        :type gradient_function: Callable | None
        :param gradient_scaling: scaling applied to the external gradient
        :type gradient_scaling: float | None
        :param fixed_atoms: atoms to hold fixed
        :type fixed_atoms: Iterable[int] | None
        :param fixed_coords: internal coordinates to hold fixed
        :type fixed_coords: Iterable[int] | None
        """
        ...

    def func(self, coords, mask):
        """
        **LLM Docstring**

        Objective function for the solve: the (summed) residual between the current
        internals and the targets.

        Reshapes the flattened coordinate vector back to `(..., N, 3)`, evaluates the
        zeroth-order internals, subtracts the (masked) targets, and sums over the
        coordinate axis.

        :param coords: flattened Cartesian coordinates for the batch
        :type coords: np.ndarray
        :param mask: mask selecting the active batch entries / targets
        :type mask: np.ndarray
        :return: the summed internal-coordinate residual per structure
        :rtype: np.ndarray
        """
        ...

    def jacobian(self, coords, mask):
        """
        **LLM Docstring**

        Newton-style update direction for the solve: the internal-coordinate residual
        mapped back into Cartesian space through the inverse transformation.

        Evaluates the forward expansion, applies the fixed-atom/coordinate constraints,
        builds the inverse expansion (removing translation/rotation or mass-weighting as
        configured), then contracts each inverse-derivative order against the residual
        with the appropriate `1 / n!` factor. An optional external gradient term is
        subtracted when a `gradient_function` was supplied.

        :param coords: flattened Cartesian coordinates for the batch
        :type coords: np.ndarray
        :param mask: mask selecting the active batch entries / targets
        :type mask: np.ndarray
        :return: the Cartesian update direction
        :rtype: np.ndarray
        """
        ...
DEFAULT_SOLVER_ORDER = 1

def inverse_coordinate_solve(specs, target_internals, initial_cartesians, masses=None, remove_translation_rotation=True, order=None, solver_order=None, tol=0.001, max_iterations=15, max_displacement=0.5, gradient_function=None, gradient_scaling=0.1, method='gradient-descent', optimizer_parameters=None, line_search=False, damping_parameter=None, damping_exponent=None, restart_interval=None, raise_on_failure=False, return_internals=True, return_expansions=True, base_transformation=None, reference_internals=None, fixed_atoms=None, fixed_coords=None, angle_ordering='ijk'):
    """
    **LLM Docstring**

    Solve for the Cartesian geometry that reproduces a target set of internal
    coordinates, starting from an initial guess.

    Wraps the forward conversion (`specs` may be a spec list or a ready-made
    conversion function) in an `_inverse_coordinate_conversion_caller` and drives it
    with the iterative minimizer from the `Optimization` module (gradient-descent by
    default, quasi-Newton optionally). Handles batching, optional
    translation/rotation removal, an external gradient bias, and returns the solved
    coordinates together with convergence errors and, optionally, the internal
    values and/or inverse expansions.

    :param specs: coordinate specifications or a conversion function
    :type specs: Iterable | Callable
    :param target_internals: target internal-coordinate values
    :type target_internals: np.ndarray
    :param initial_cartesians: initial Cartesian guess
    :type initial_cartesians: np.ndarray
    :param masses: per-atom masses
    :type masses: np.ndarray | None
    :param remove_translation_rotation: whether to strip translation/rotation
    :type remove_translation_rotation: bool
    :param order: expansion order for the returned inverse tensors
    :type order: int | None
    :param solver_order: expansion order used inside the solver
    :type solver_order: int | None
    :param tol: convergence tolerance
    :type tol: float
    :param max_iterations: maximum solver iterations
    :type max_iterations: int
    :param max_displacement: cap on the per-step Cartesian displacement
    :type max_displacement: float
    :param gradient_function: optional external gradient function
    :type gradient_function: Callable | None
    :param gradient_scaling: scaling for the external gradient
    :type gradient_scaling: float
    :param method: optimizer method (`'gradient-descent'` or `'quasi-newton'`)
    :type method: str
    :param optimizer_parameters: extra optimizer options
    :type optimizer_parameters: dict | None
    :param line_search: whether to use a line search
    :type line_search: bool
    :param damping_parameter: optional step damping parameter
    :type damping_parameter: float | None
    :param damping_exponent: optional step damping exponent
    :type damping_exponent: float | None
    :param restart_interval: optional optimizer restart interval
    :type restart_interval: int | None
    :param raise_on_failure: raise if convergence is not reached
    :type raise_on_failure: bool
    :param return_internals: whether to also return the solved internals
    :type return_internals: bool
    :param return_expansions: whether to also return the inverse expansions
    :type return_expansions: bool
    :param base_transformation: optional coordinate-basis transformation
    :type base_transformation: list[np.ndarray] | None
    :param reference_internals: reference internals for the transformation
    :type reference_internals: np.ndarray | None
    :param fixed_atoms: atoms to hold fixed
    :type fixed_atoms: Iterable[int] | None
    :param fixed_coords: internal coordinates to hold fixed
    :type fixed_coords: Iterable[int] | None
    :param angle_ordering: default angle-index ordering
    :type angle_ordering: str
    :return: the solved transformation and errors (with internals when requested)
    :rtype: tuple
    """
    ...

def coordinate_projection_data(basis_mat, fixed_mat, inds, nonzero_cutoff=1e-08, masses=None, coords=None, project_transrot=False):
    """
    **LLM Docstring**

    Build the basis / complementary-basis / selection data used to project a set of
    local internal coordinates onto the full coordinate space.

    Optionally projects out (or augments) the translation/rotation subspace for the
    selected atoms via `CoordinateFrames.translation_rotation_projector`. A
    `find_basis` call orthonormalizes the supplied basis (or fixed) matrix, an
    atom-selection matrix `mat` is assembled for the requested indices, and the
    complementary basis is obtained by subtracting the relevant projection matrix.

    :param basis_mat: the basis matrix to keep (or `None`)
    :type basis_mat: np.ndarray | None
    :param fixed_mat: the fixed/constraint matrix (used when `basis_mat` is `None`)
    :type fixed_mat: np.ndarray | None
    :param inds: atom indices spanned by the coordinate
    :type inds: Iterable[int]
    :param nonzero_cutoff: singular-value cutoff for `find_basis`
    :type nonzero_cutoff: float
    :param masses: per-atom masses (for translation/rotation projection)
    :type masses: np.ndarray | None
    :param coords: Cartesian coordinates (for translation/rotation projection)
    :type coords: np.ndarray | None
    :param project_transrot: whether to project out translation/rotation
    :type project_transrot: bool
    :return: `(basis, complementary_basis, selection_matrix)`
    :rtype: tuple[np.ndarray, np.ndarray, np.ndarray]
    """
    ...

def dist_basis_mat(coords, i, j):
    """
    **LLM Docstring**

    Build the (unnormalized) coordinate basis matrix for a distance coordinate
    between atoms `i` and `j`.

    Places `+1` on the diagonal Cartesian block of atom `i` and `-1` on that of
    atom `j`, then flattens the atom/axis dimensions.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param i: first atom index
    :type i: int
    :param j: second atom index
    :type j: int
    :return: the flattened distance basis matrix
    :rtype: np.ndarray
    """
    ...

def dist_basis(coords, i, j, **opts):
    """
    **LLM Docstring**

    Return the projection data for a distance coordinate between atoms `i` and `j`.

    Builds the distance basis with `dist_basis_mat` and passes it through
    `coordinate_projection_data`.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param i: first atom index
    :type i: int
    :param j: second atom index
    :type j: int
    :param opts: options forwarded to `coordinate_projection_data`
    :return: `(basis, complementary_basis, selection_matrix)`
    :rtype: tuple
    """
    ...

def fixed_angle_basis(coords, i, j, k):
    """
    **LLM Docstring**

    Build the fixed coordinate basis matrix for a bend coordinate on atoms `i`,
    `j`, `k`.

    Combines pure translations of the three atoms with the two arm vectors
    (`i - j` and `k - j`) distributed across the atoms, giving a seven-column basis
    that spans the rigid motions to be projected out when isolating the bend.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param i: first outer atom
    :type i: int
    :param j: vertex atom
    :type j: int
    :param k: second outer atom
    :type k: int
    :return: the flattened fixed-angle basis matrix (7 columns)
    :rtype: np.ndarray
    """
    ...

def angle_basis(coords, i, j, k, angle_ordering='ijk', **opts):
    """
    **LLM Docstring**

    Return the projection data for a bend coordinate on atoms `i`, `j`, `k`.

    Honors the `angle_ordering` convention (swapping `i`/`j` for `'jik'`), builds
    the fixed basis with `fixed_angle_basis`, and passes it through
    `coordinate_projection_data`.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param i: first atom (interpretation depends on `angle_ordering`)
    :type i: int
    :param j: second atom
    :type j: int
    :param k: third atom
    :type k: int
    :param angle_ordering: angle-index ordering (`'ijk'` or `'jik'`)
    :type angle_ordering: str
    :param opts: options forwarded to `coordinate_projection_data`
    :return: `(basis, complementary_basis, selection_matrix)`
    :rtype: tuple
    """
    ...

def fixed_dihed_basis(coords, i, j, k, l):
    """
    **LLM Docstring**

    Build the fixed coordinate basis matrix for a dihedral coordinate on atoms
    `i`, `j`, `k`, `l`.

    Combines pure translations of the four atoms with vectors spanning the two
    defining planes (`i - j`, `j - k`, `l - k`), giving a nine-column basis of rigid
    motions to project out when isolating the torsion.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param i: first terminal atom
    :type i: int
    :param j: first central atom
    :type j: int
    :param k: second central atom
    :type k: int
    :param l: second terminal atom
    :type l: int
    :return: the flattened fixed-dihedral basis matrix (9 columns)
    :rtype: np.ndarray
    """
    ...

def dihed_basis(coords, i, j, k, l, **opts):
    """
    **LLM Docstring**

    Return the projection data for a dihedral coordinate on atoms `i`, `j`, `k`,
    `l`.

    Builds the fixed basis with `fixed_dihed_basis` and passes it through
    `coordinate_projection_data`.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param i: first terminal atom
    :type i: int
    :param j: first central atom
    :type j: int
    :param k: second central atom
    :type k: int
    :param l: second terminal atom
    :type l: int
    :param opts: options forwarded to `coordinate_projection_data`
    :return: `(basis, complementary_basis, selection_matrix)`
    :rtype: tuple
    """
    ...
basis_coord_type_map = {'dist': dist_basis, 'bend': angle_basis, 'dihed': dihed_basis}

def internal_basis_specs(specs, angle_ordering='ijk', **opts):
    """
    **LLM Docstring**

    Normalize coordinate specifications for *basis* construction.

    Thin wrapper over `internal_conversion_specs` that dispatches through
    `basis_coord_type_map` (the basis-building functions) instead of the
    derivative functions.

    :param specs: the coordinate specifications
    :type specs: Iterable
    :param angle_ordering: default angle-index ordering
    :type angle_ordering: str
    :param opts: extra options merged into every spec
    :return: list of `(basis_function, indices, options)` triples
    :rtype: list[tuple]
    """
    ...

def internal_basis(coords, specs, **opts):
    """
    **LLM Docstring**

    Build the internal-coordinate bases for a geometry from a set of coordinate
    specifications.

    Normalizes the specs with `internal_basis_specs`, then evaluates each basis
    function to collect its basis, orthogonal complement, and sub-projection.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param specs: the coordinate specifications
    :type specs: Iterable
    :param opts: options forwarded to `internal_basis_specs`
    :return: `(bases, orthogonal_complements, sub_projections)`
    :rtype: tuple[list, list, list]
    """
    ...

def metric_tensor(internals_by_cartesians, masses=None):
    """
    **LLM Docstring**

    Compute the internal-coordinate metric (Wilson G-style) tensor from an
    internals-by-Cartesians transformation.

    Optionally mass-weights the transformation with `M^{-1/2}` before forming
    `Jᵀ J`. A bare 2D array is accepted and treated as the first (linear) term of an
    expansion.

    :param internals_by_cartesians: the transformation (or its expansion)
    :type internals_by_cartesians: np.ndarray | list[np.ndarray]
    :param masses: per-atom masses for mass-weighting
    :type masses: np.ndarray | None
    :return: the metric tensor
    :rtype: np.ndarray
    """
    ...

def delocalized_internal_coordinate_transformation(internals_by_cartesians, untransformed_coordinates=None, masses=None, relocalize=False):
    """
    **LLM Docstring**

    Construct a set of delocalized (non-redundant) internal coordinates from a
    redundant internals-by-Cartesians transformation.

    Optionally mass-weights the transformation and separates out any
    `untransformed_coordinates` (projecting their contribution out of the remaining
    coordinates so the space dimension is preserved). Diagonalizing the internal
    `G` matrix and keeping the nonzero-eigenvalue eigenvectors yields the
    delocalized transformation, which is optionally relocalized to align with the
    untransformed coordinates.

    :param internals_by_cartesians: the redundant transformation (or its expansion)
    :type internals_by_cartesians: np.ndarray | list[np.ndarray]
    :param untransformed_coordinates: coordinates to keep out of the delocalization
    :type untransformed_coordinates: Iterable[int] | None
    :param masses: per-atom masses for mass-weighting
    :type masses: np.ndarray | None
    :param relocalize: whether to relocalize onto the untransformed coordinates
    :type relocalize: bool
    :return: the delocalized coordinate transformation
    :rtype: np.ndarray | list[np.ndarray]
    """
    ...

def relocalize_coordinate_transformation(redund_tf, untransformed_coordinates=None):
    """
    **LLM Docstring**

    Rotate a redundant/delocalized coordinate transformation so that it aligns as
    closely as possible with a chosen set of localized target coordinates.

    A target matrix is built (an identity block, or unit columns on the requested
    `untransformed_coordinates`), the least-squares alignment is solved, and its
    SVD gives the orthogonal rotation `R = U V` applied to the transformation.

    :param redund_tf: the transformation to relocalize
    :type redund_tf: np.ndarray
    :param untransformed_coordinates: coordinates to align to (identity if omitted)
    :type untransformed_coordinates: Iterable[int] | None
    :return: the relocalized transformation
    :rtype: np.ndarray
    """
    ...

def transform_cartesian_derivatives(derivs, tfs, axes=None):
    """
    **LLM Docstring**

    Apply a Cartesian coordinate transformation to a set of Cartesian derivative
    tensors, one derivative axis at a time.

    For each `n`-th order tensor the routine reshapes each Cartesian axis into
    `(atom, 3)`, contracts the `3`-component sub-axis against the transformation
    `tfs` (using a shared/broadcast contraction when the transformation is itself
    batched), and restores the original shape. Numeric (scalar) entries are skipped.

    :param derivs: the Cartesian derivative tensors
    :type derivs: list[np.ndarray]
    :param tfs: the per-atom transformation matrices
    :type tfs: np.ndarray
    :param axes: `(derivative_axis, transform_axis)`; defaults to `[-1, -2]`
    :type axes: list[int] | int | None
    :return: the transformed derivative tensors
    :rtype: list[np.ndarray]
    """
    ...
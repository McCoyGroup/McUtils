from __future__ import annotations

"""
Provides analytic derivatives for some common base terms with the hope that we can reuse them elsewhere
"""

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

__all__ = [
    'rot_deriv',
    'rot_deriv2',
    'cartesian_from_rad_derivatives',
    'dist_basis',
    'angle_basis',
    # 'dihed_bases',
    'internal_basis',
    'prep_disp_expansion',
    'prep_unit_vector_expansion_from_cache',
    'dist_deriv',
    'angle_deriv',
    'normal_deriv',
    'dihed_deriv',
    'book_deriv',
    'oop_deriv',
    'wag_deriv',
    'transrot_deriv',
    'com_dist_deriv',
    # "com_pos_diff_deriv",
    'orientation_deriv',
    "rotation_expansion_from_axis_angle",
    "dist_expansion",
    "dihed_expansion",
    "angle_expansion",
    # 'vec_norm_derivs',
    # 'vec_sin_cos_derivs',
    # 'vec_angle_derivs',
    'rock_deriv',
    'rock_vec',
    'dist_vec',
    'angle_vec',
    'dihed_vec',
    'book_vec',
    'oop_vec',
    'wag_vec',
    'oop_expansion',
    'wag_expansion',
    'transrot_vecs',
    'transrot_expansion',
    # "com_pos_diff_deriv",
    'orientation_vecs',
    'orientation_expansion',
    "internal_conversion_function",
    "combine_coordinate_deriv_expansions",
    "internal_coordinate_tensors",
    "inverse_internal_coordinate_tensors",
    "inverse_coordinate_solve",
    "combine_coordinate_inverse_expansions",
    "metric_tensor",
    "delocalized_internal_coordinate_transformation",
    "relocalize_coordinate_transformation",
    "transform_cartesian_derivatives"
]

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
    return op(a, db) + op(da, b)
def _prod_deriv_2(op, a, b, da1, da2, db1, db2, da12, db12):
    """
    2nd derivative of op(a, b) assuming it operates under a product-rule type ish
    """
    return op(da12, b) + op(da1, db2) + op(da2, db1) + op(a, db12)

def normalized_vec_deriv(v, dv):
    """
    Derivative of a normalized vector w/r/t some unspecified coordinate
    """
    norms = vec_norms(v)[..., np.newaxis]
    vh = v / norms
    i3 = np.broadcast_to(np.eye(3), dv.shape[:-1] + (3, 3))
    vXv = vec_outer(vh, vh)
    wat = np.matmul(i3 - vXv, dv[..., np.newaxis])[..., 0] # gotta add a 1 for matmul
    return wat / norms

def normalized_vec_deriv2(v, dv1, dv2, d2v):
    """
    Second derivative of a normalized vector w/r/t some unspecified coordinates
    """
    # derivative of inverse norm
    norms = vec_norms(v)[..., np.newaxis]
    vds2 = vec_dots(dv2, v)[..., np.newaxis]
    dnorminv = -1/(norms**3) * vds2
    vh = v / norms
    i3 = np.broadcast_to(np.eye(3), dv1.shape[:-1] + (3, 3))
    vXv = vec_outer(vh, vh)
    dvh2 = normalized_vec_deriv(v, dv2)
    dvXv2 = _prod_deriv(vec_outer, vh, vh, dvh2, dvh2)
    right = np.matmul(i3 - vXv, dv1[..., np.newaxis])[..., 0]  # gotta add a 1 for matmul
    dright = _prod_deriv(np.matmul, i3 - vXv, dv1[..., np.newaxis], -dvXv2, d2v[..., np.newaxis])[..., 0]
    der = _prod_deriv(np.multiply, 1/norms, right, dnorminv, dright)
    return der

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

    # Will still need work to be appropriately vectorized (can't remember if I did this or not?)
    vdOdv = vec_outer(dAxis, axis) + vec_outer(axis, dAxis)
    c = np.cos(angle)[..., np.newaxis]
    s = np.sin(angle)[..., np.newaxis]
    i3 = np.broadcast_to(np.eye(3), axis.shape[:-1] + (3, 3))
    e3 = np.broadcast_to(pops.levi_cevita3, axis.shape[:-1] + (3, 3, 3))
    # e3 = pops.levi_cevita3
    # i3 = np.eye(3)
    ct = vdOdv*(1-c[..., np.newaxis])
    st = (i3-vec_outer(axis, axis))*s[..., np.newaxis]*dAngle
    wat = (dAxis*s + axis*c*dAngle)
    et = vec_tensordot(e3, wat, axes=[-1, 1]) # currently explicitly takes a stack of vectors...
    return ct - st - et

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

    from operator import mul

    # lots of duplication since we've got the same axis twice
    vXv = vec_outer(axis, axis)
    dvXv1 = _prod_deriv(vec_outer, axis, axis, dAxis1, dAxis1)
    dvXv2 = _prod_deriv(vec_outer, axis, axis, dAxis2, dAxis2)
    d2vXv = _prod_deriv_2(vec_outer, axis, axis, dAxis1, dAxis2, dAxis1, dAxis2, d2Axis, d2Axis)

    i3 = np.broadcast_to(np.eye(3), axis.shape[:-1] + (3, 3))
    e3 = np.broadcast_to(pops.levi_cevita3, axis.shape[:-1] + (3, 3, 3))

    c = np.cos(angle)
    s = np.sin(angle)

    dc1 = -s * dAngle1
    dc2 = -s * dAngle2
    d2c = -s * d2Angle - c * dAngle1 * dAngle2

    cos_term = _prod_deriv_2(mul,
                             i3 - vXv,
                             c[..., np.newaxis, np.newaxis],
                             dvXv1, dvXv2,
                             dc1[..., np.newaxis, np.newaxis], dc2[..., np.newaxis, np.newaxis],
                             d2vXv, d2c[..., np.newaxis, np.newaxis]
                             )

    ds1 = c * dAngle1
    ds2 = c * dAngle2
    d2s = c * d2Angle - s * dAngle1 * dAngle2
    fack = _prod_deriv_2(mul, axis, s[..., np.newaxis], dAxis1, dAxis2, ds1[..., np.newaxis], ds2[..., np.newaxis], d2Axis, d2s[..., np.newaxis])
    sin_term = vec_tensordot(e3, fack, axes=[-1, 1])

    return d2vXv + cos_term - sin_term

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

    # derivatives of coordinates
    dr = 1 if (z == i and m == 0) else 0
    dq = 1 if (z == i and m == 1) else 0
    df = 1 if (z == i and m == 2) else 0

    dv_ = dxb - dxa
    dv = normalized_vec_deriv(v, dv_)
    v = vec_normalize(v)
    if a is None:
        # no derivative about any of the rotation shit
        drv = _prod_deriv(np.multiply, r[..., np.newaxis], v, dr, dv)
        du_ = dn_ = dR1 = dR2 = dQ = None
        der = dxa + drv
    else:
        # derivatives of axis system vectors
        du_ = dxc - dxb
        du = normalized_vec_deriv(u, du_)
        u = vec_normalize(u)
        dn_ = _prod_deriv(vec_crosses, v, u, dv, du)
        # we actually need the derivatives of the unit vectors for our rotation axes
        dn = normalized_vec_deriv(n, dn_)
        n = vec_normalize(n)
        # raise Exception(n.shape, dn.shape, dn_.shape)

        # derivatives of rotation matrices
        dR1 = rot_deriv(a, n, dq, dn)
        if d is not None:
            dR2 = rot_deriv(d, v, df, dv)
            # derivative of total rotation matrix
            dQ = _prod_deriv(np.matmul, R2, R1, dR2, dR1)
        else:
            dR2 = None
            dQ = dR1

        # derivative of vector along the main axis
        drv = _prod_deriv(np.multiply, r, v, dr, dv)
        der = dxa + _prod_deriv(np.matmul, Q, rv[..., np.newaxis], dQ, drv[..., np.newaxis])[..., 0]

    return der, (dr, dq, df, dv_, du_, dn_, dR1, dR2, dQ, drv)

def _rad_d2(i, z1, m1, z2, m2, # don't actually use these because all the coordinate 2nd derivatives are 0 :yay:
            r, a, d, v, u, n, R1, R2, Q, rv,
            dr1, dq1, df1, dv1, du1, dn1, dR11, dR21, dQ1, drv1,
            dr2, dq2, df2, dv2, du2, dn2, dR12, dR22, dQ2, drv2,
            d2xa, d2xb, d2xc):
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

    # second derivatives of embedding axes
    # fuck this is annoying...need to get the _unnormalized_ shit too to get the norm deriv as I have it...
    d2v = normalized_vec_deriv2(v, dv1, dv2, d2xb - d2xa)
    dv1 = normalized_vec_deriv(v, dv1)
    dv2 = normalized_vec_deriv(v, dv2)
    v = vec_normalize(v)
    if r.shape[-1] == 1: # shape hack for now... to flatten r I guess...
        r = r[..., 0]
    if a is None:
        d2rv = _prod_deriv_2(np.multiply, r[..., np.newaxis], v, dr1, dr2, dv1, dv2, 0, d2v)
        der = d2xa + d2rv
        d2u = d2n = d2R1 = d2R2 = d2Q = None
    else:
        d2u = normalized_vec_deriv2(u, du1, du2, d2xc - d2xb)
        du1 = normalized_vec_deriv(u, du1)
        du2 = normalized_vec_deriv(u, du2)
        u = vec_normalize(u)
        d2n_ = _prod_deriv_2(vec_crosses, v, u, dv1, dv2, du1, du2, d2v, d2u)
        d2n = normalized_vec_deriv2(v, dn1, dn2, d2n_)
        dn1 = normalized_vec_deriv(u, dn1)
        dn2 = normalized_vec_deriv(u, dn2)
        n = vec_normalize(n)

        # second derivatives of rotation matrices
        d2R1 = rot_deriv2(a, n, dq1, dn1, dq2, dn2, 0, d2n)
        if d is None:
            d2R2 = None
            d2Q = d2R1
        else:
            d2R2 = rot_deriv2(d, v, df1, dv1, df2, dv2, 0, d2v)
            d2Q = _prod_deriv_2(np.matmul, R2, R1, dR21, dR22, dR11, dR12, d2R1, d2R2)

        # second derivatives of r*v
        d2rv = _prod_deriv_2(np.multiply, r[..., np.newaxis], v, dr1, dr2, dv1, dv2, 0, d2v)

        # new derivative
        der = d2xa + _prod_deriv_2(np.matmul, Q, rv[..., np.newaxis], dQ1, dQ2, drv1[..., np.newaxis], drv2[..., np.newaxis], d2Q, d2rv[..., np.newaxis])[..., 0]

    # if der.shape == (7, 7, 3):
    #     raise ValueError(r.shape, d2v.shape, d2rv.shape)#, d2u.shape, d2n.shape, d2R1.shape, d2R2.shape, d2Q.shape, d2rv.shape)
    return der, (d2v, d2u, d2n, d2R1, d2R2, d2Q, d2rv)

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
        self.comp = comp
def cartesian_from_rad_derivatives(
        xa, xb, xc,
        r, a, d,
        i,
        ia, ib, ic,
        derivs,
        order=2,
        return_comps=False
):
    """
    Returns derivatives of the generated Cartesian coordinates with respect
    to the internals
    """

    if order > 2:
        raise NotImplementedError("bond-angle-dihedral to Cartesian derivatives only implemented up to order 2")

    coord, comps = cartesian_from_rad(xa, xb, xc, r, a, d, return_comps=True)
    v, u, n, R2, R1 = comps
    if R2 is not None:
        Q = np.matmul(R2, R1)
    elif R1 is not None:
        Q = R1
    else:
        Q = None
    if r.ndim < v.ndim:
        rv = r[..., np.newaxis] * vec_normalize(v)
    else:
        rv = r * vec_normalize(v)

    #TODO: I think I'm re-calculating terms I did for a previous value of i?
    #       ...except I'm not because _rad_d1 has some Kronecker delta terms...
    #       still, it could all be made way more efficient I bet by reusing stuff
    new_derivs = []
    new_derivs.append(coord)
    new_comps = []
    new_comps.append(comps)
    inds = np.arange(len(ia))
    if order > 0:
        if derivs[1].ndim != 5:
            raise ValueError("as implemented, derivative blocks have to look like (nconfigs, nzlines, 3, natoms, 3)")
        config_shape = derivs[1].shape[:-4]
        d1 = np.zeros(config_shape + (i+1, 3, 3)) # the next block in the derivative tensor
        d1_comps = np.full((i+1, 3), None) # the components used to build the derivatives
        for z in range(i + 1):  # Lower-triangle is 0 so we do nothing with it
            for m in range(3):
                # we'll need to do some special casing for z < 2
                # also we gotta pull o
                dxa = derivs[1][inds, z, m, ia, :]
                dxb = derivs[1][inds, z, m, ib, :]
                dxc = derivs[1][inds, z, m, ic, :]

                # raise Exception(dxa.shape, derivs[1].shape)
                der, comps1 = _rad_d1(i, z, m, r, a, d, v, u, n, R1, R2, Q, rv, dxa, dxb, dxc)
                d1_comps[z, m] = _dumb_comps_wrapper(comps1)

                d1[inds, z, m, :] = der
        new_derivs.append(d1)
        new_comps.append(d1_comps)
        if order > 1:
            d2 = np.zeros(config_shape + (i+1, 3, i+1, 3, 3)) # the next block in the 2nd derivative tensor
            d2_comps = np.full((i+1, 3, i+1, 3), None) # the components used to build the derivatives
            for z1 in range(i + 1):
                for m1 in range(3):
                    for z2 in range(i + 1):
                        for m2 in range(3):
                                d2xa = derivs[2][inds, z1, m1, z2, m2, ia, :]
                                d2xb = derivs[2][inds, z1, m1, z2, m2, ib, :]
                                d2xc = derivs[2][inds, z1, m1, z2, m2, ic, :]
                                dr1, dq1, df1, dv1, du1, dn1, dR11, dR21, dQ1, drv1 = d1_comps[z1, m1].comp
                                dr2, dq2, df2, dv2, du2, dn2, dR12, dR22, dQ2, drv2 = d1_comps[z2, m2].comp

                                # now we feed this in
                                der, comps2 = _rad_d2(i, z1, m1, z2, m2,
                                                      r, a, d, v, u, n, R1, R2, Q, rv,
                                                      dr1, dq1, df1, dv1, du1, dn1, dR11, dR21, dQ1, drv1,
                                                      dr2, dq2, df2, dv2, du2, dn2, dR12, dR22, dQ2, drv2,
                                                      d2xa, d2xb, d2xc
                                                      )
                                d2[inds, z1, m1, z2, m2, :] = der
                                d2_comps[z1, m1, z2, m2] = _dumb_comps_wrapper(comps2)
            new_derivs.append(d2)
            new_comps.append(d2_comps)

    if return_comps:
        return new_derivs, new_comps
    else:
        return new_derivs

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

    if order > 2:
        raise NotImplementedError("derivatives currently only up to order {}".format(2))

    derivs = []

    na = vec_norms(a)
    derivs.append(np.copy(na)) # we return the value itself for Taylor-series reasons

    # print(a.shape)
    a, zeros = vec_handle_zero_norms(a, na, zero_thresh=zero_thresh)
    na = na[..., np.newaxis]
    na[zeros] = Options.zero_placeholder

    if order >= 1:
        d1 = a / na
        # print(a.shape, na.shape)

        derivs.append(d1)

    if order >= 2:
        n = a.shape[-1]
        extra_shape = a.ndim - 1
        if extra_shape > 0:
            i3 = np.broadcast_to(np.eye(n), (1,)*extra_shape + (n, n))
        else:
            i3 = np.eye(n)
        v = vec_outer(d1, d1)
        # na shold have most of the extra_shape needed
        d2 = (i3 - v) / na[..., np.newaxis]
        derivs.append(d2)

    return derivs

def vec_sin_cos_derivs(a, b, order=1,
                       up_vectors=None,
                       check_derivatives=False, zero_thresh=None):
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

    if order > 2:
        raise NotImplementedError("derivatives currently only up to order {}".format(2))

    extra_dims = a.ndim - 1

    sin_derivs = []
    cos_derivs = []

    a, n_a = vec_apply_zero_threshold(a, zero_thresh=zero_thresh)
    b, n_b = vec_apply_zero_threshold(b, zero_thresh=zero_thresh)

    n = vec_crosses(a, b)
    n, n_n, bad_ns = vec_apply_zero_threshold(n, zero_thresh=zero_thresh, return_zeros=True)

    adb = vec_dots(a, b)[..., np.newaxis]

    zero_thresh = Options.norm_zero_threshold if zero_thresh is None else zero_thresh

    s = n_n / (n_a * n_b)
    # s[n_n <= zero_thresh] = 0.
    c = adb / (n_a * n_b)
    # c[adb <= zero_thresh] = 0.

    sin_derivs.append(s)
    cos_derivs.append(c)

    if order > 0:
        if bad_ns.any():  # ill-defined sin components need an "up" vector and then point perpendicular to this
            if up_vectors is None:
                if n.ndim > 1:
                    up_vectors = np.broadcast_to(
                        np.array([0, 0, 1])[np.newaxis],
                        a.shape[:-1] + (3,)
                    )
                else:
                    up_vectors = np.array([0, 0, 1])
            if n.ndim == 1:
                n = vec_normalize(up_vectors)
                n_n = 1
            else:
                n[bad_ns] = vec_normalize(up_vectors[bad_ns])
                n_n[bad_ns] = 1

        bxn_ = vec_crosses(b, n)
        bxn, n_bxn = vec_apply_zero_threshold(bxn_, zero_thresh=zero_thresh)

        nxa_ = vec_crosses(n, a)
        nxa, n_nxa = vec_apply_zero_threshold(nxa_, zero_thresh=zero_thresh)

        if order <= 1:
            _, na_da = vec_norm_derivs(a, order=1)
            _, nb_db = vec_norm_derivs(b, order=1)
        else:
            _, na_da, na_daa = vec_norm_derivs(a, order=2)
            _, nb_db, nb_dbb = vec_norm_derivs(b, order=2)
            _, nn_dn, nn_dnn = vec_norm_derivs(n, order=2)

        if order >= 1:
            s_da = (bxn / (n_b * n_n) - s * na_da) / n_a
            s_db = (nxa / (n_n * n_a) - s * nb_db) / n_b

            # now we build our derivs, but we also need to transpose so that the OG shape comes first
            d1 = np.array([s_da, s_db])
            d1_reshape = tuple(range(1, extra_dims+1)) + (0, extra_dims+1)
            meh = d1.transpose(d1_reshape)

            sin_derivs.append(meh)

            # print(
            #     nb_db.shape,
            #     na_da.shape,
            #     c.shape,
            #     n_a.shape
            # )

            c_da = (nb_db - c * na_da) / n_a
            c_db = (na_da - c * nb_db) / n_b

            d1 = np.array([c_da, c_db])
            meh = d1.transpose(d1_reshape)

            cos_derivs.append(meh)

        if order >= 2:

            extra_dims = a.ndim - 1
            extra_shape = a.shape[:-1]
            if check_derivatives:
                if extra_dims > 0:
                    bad_norms = n_n.flatten() <= zero_thresh
                    if bad_norms.any():
                        raise ValueError("2nd derivative of sin not well defined when {} and {} are nearly colinear".format(
                            a[bad_norms],
                            b[bad_norms]
                        ))
                else:
                    if n_n <= zero_thresh:
                        raise ValueError("2nd derivative of sin not well defined when {} and {} are nearly colinear".format(
                            a, b
                        ))

            if extra_dims > 0:
                e3 = np.broadcast_to(pops.levi_cevita3,  extra_shape + (3, 3, 3))
                # td = np.tensordot
                outer = vec_outer
                vec_td = lambda a, b, **kw: vec_tensordot(a, b, shared=extra_dims, **kw)
            else:
                e3 = pops.levi_cevita3
                # td = np.tensordot
                vec_td = lambda a, b, **kw: vec_tensordot(a, b, shared=0, **kw)
                outer = np.outer
                a = a.squeeze()
                b = b.squeeze()
                nb_db = nb_db.squeeze(); na_da = na_da.squeeze(); nn_dn = nn_dn.squeeze()
                na_daa = na_daa.squeeze(); nb_dbb = nb_dbb.squeeze(); nn_dnn = nn_dnn.squeeze()

            # print(na_da, s_da, s, na_daa, bxdna)

            # compute terms we'll need for various cross-products
            e3b = vec_td(e3, b, axes=[-1, -1])
            e3a = vec_td(e3, a, axes=[-1, -1])
            # e3n = vec_td(e3, n, axes=[-1, -1])

            e3nbdb = vec_td(e3, nb_db, axes=[-1, -1])
            e3nada = vec_td(e3, na_da, axes=[-1, -1])
            e3nndn = vec_td(e3, nn_dn, axes=[-1, -1])

            n_da = -vec_td(e3b,  nn_dnn, axes=[-1, -2])
            bxdna = vec_td(n_da, e3nbdb, axes=[-1, -2])

            s_daa = - (
                outer(na_da, s_da) + outer(s_da, na_da)
                + s[..., np.newaxis] * na_daa
                - bxdna
            ) / n_a[..., np.newaxis]

            ndaXnada = -vec_td(n_da, e3nada, axes=[-1, -2])
            nndnXnadaa = vec_td(na_daa, e3nndn, axes=[-1, -2])

            s_dab = (
                         ndaXnada + nndnXnadaa - outer(s_da, nb_db)
            ) / n_b[..., np.newaxis]

            n_db = vec_td(e3a, nn_dnn, axes=[-1, -2])

            nbdbXnda = vec_td(n_db, e3nbdb, axes=[-1, -2])
            nbdbbXnndn = -vec_td(nb_dbb, e3nndn, axes=[-1, -2])

            s_dba = (
                    nbdbXnda + nbdbbXnndn - outer(s_db, na_da)
            ) / n_a[..., np.newaxis]

            dnbxa = - vec_td(n_db, e3nada, axes=[-1, -2])

            s_dbb = - (
                outer(nb_db, s_db) + outer(s_db, nb_db) + s[..., np.newaxis] * nb_dbb - dnbxa
            ) / n_b[..., np.newaxis]

            s2 = np.array([
                [s_daa, s_dab],
                [s_dba, s_dbb]
            ])

            d2_reshape = tuple(range(2, extra_dims+2)) + (0, 1, extra_dims+2, extra_dims+3)
            s2 = s2.transpose(d2_reshape)

            sin_derivs.append(s2)

            # na_daa = np.zeros_like(na_daa)

            c_daa = - (
                outer(na_da, c_da) + outer(c_da, na_da)
                + c[..., np.newaxis] * na_daa
            ) / n_a[..., np.newaxis]
            c_dab = (na_daa - outer(c_da, nb_db)) / n_b[..., np.newaxis]
            c_dba = (nb_dbb - outer(c_db, na_da)) / n_a[..., np.newaxis]
            c_dbb = - (
                outer(nb_db, c_db) + outer(c_db, nb_db)
                + c[..., np.newaxis] * nb_dbb
            ) / n_b[..., np.newaxis]

            c2 = np.array([
                [c_daa, c_dab],
                [c_dba, c_dbb]
            ])

            c2 = c2.transpose(d2_reshape)

            cos_derivs.append(c2)

    return sin_derivs, cos_derivs

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
    if axes is None:
        axes = [0, 1, 2]
    if misc.is_numeric(coords):
        coords = [coords]
    z = np.zeros((nats, 3, nats, 3))
    row_inds = np.repeat(coords, len(axes), axis=0)
    col_inds = np.repeat(axes, len(coords), axis=0).flatten()
    z[row_inds, col_inds, row_inds, col_inds] = 1
    z = z.reshape(nats*3, nats*3)
    if base_shape is not None:
        sh = z.shape
        expax = list(range(len(base_shape)))
        z = np.broadcast_to(np.expand_dims(z, expax), base_shape + sh)
    return z

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
    if axes is None:
        axes = [0, 1, 2]

    smol = misc.is_numeric(ind_lists[0])
    ind_lists = [
        np.asanyarray([i] if smol else i).reshape(-1)
        for i in ind_lists
    ]

    nstruct = ind_lists[0].shape[0]
    struct_inds = np.repeat(np.arange(nstruct), len(axes), axis=0)

    inds = []
    for i in ind_lists:
        row_inds = np.repeat(i, len(axes), axis=0)
        col_inds = np.repeat(axes, len(i), axis=0).flatten()
        inds.append((struct_inds, row_inds, col_inds, col_inds))

    return inds

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
    if axes is None:
        axes = [0, 1, 2]
    axes = np.asanyarray(axes)

    smol = misc.is_numeric(ind_lists[0][0])
    ind_lists = [
        [
            np.asanyarray([i] if smol else i).reshape(-1),
            np.asanyarray([a] if smol else a).reshape(-1)
        ]
        for i,a in ind_lists
    ]

    nstruct = ind_lists[0][0].shape[0]
    struct_inds = np.repeat(np.arange(nstruct), len(axes), axis=0)

    inds = []
    for i,a in ind_lists:
        ax = axes + len(axes) * a
        row_inds = np.repeat(i, len(axes), axis=0)
        col_inds = np.repeat(axes, len(i), axis=0).flatten()
        scol_inds = ax
        inds.append((struct_inds, row_inds, col_inds, scol_inds))

    return inds

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
    ind_lists = [i for i,v in ind_val_pairs]
    vals = [v for i,v in ind_val_pairs]
    smol = misc.is_numeric(ind_lists[0])
    ind_lists = [
        np.asanyarray([i] if smol else i)
        for i in ind_lists
    ]

    i_shape = ind_lists[0].shape
    nnew = len(i_shape)
    if base_shape is None:
        base_shape = mat.shape[:-3]
    target_shape = base_shape + i_shape + mat.shape[-3:]
    if target_shape != mat.shape:
        nog = len(base_shape)
        mat = np.broadcast_to(
            np.expand_dims(mat, np.arange(nog, nog+nnew).tolist()),
            target_shape
        ).copy()
    else:
        base_shape = mat.shape[:-(3+nnew)]
        # target_shape = base_shape + i_shape + mat.shape[-3:]

    mat = np.reshape(mat, base_shape + (np.prod(i_shape, dtype=int),) + mat.shape[-3:])
    for idx_tup,val in zip(jacobian_mat_inds(ind_lists, axes=axes), vals):
        idx_tup = (...,) + idx_tup
        mat[idx_tup] = val
    mat = mat.reshape(target_shape)

    if smol:
        mat = mat.reshape(base_shape + mat.shape[-3:])
    return mat

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
    ind_lists = [[i,a] for i,a,v in ind_val_pairs]
    vals = [v for i,a,v in ind_val_pairs]
    smol = misc.is_numeric(ind_lists[0][0])
    ind_lists = [
        [
            np.asanyarray([i] if smol else i),
            np.asanyarray([a] if smol else a),
        ]
        for i,a in ind_lists
    ]

    i_shape = ind_lists[0][0].shape
    nnew = len(i_shape)
    if base_shape is None:
        base_shape = mat.shape[:-3]
    target_shape = base_shape + i_shape + mat.shape[-3:]
    if target_shape != mat.shape:
        nog = len(base_shape)
        mat = np.broadcast_to(
            np.expand_dims(mat, np.arange(nog, nog+nnew).tolist()),
            target_shape
        ).copy()
    else:
        base_shape = mat.shape[:-(3+nnew)]
        # target_shape = base_shape + i_shape + mat.shape[-3:]

    mat = np.reshape(mat, base_shape + (np.prod(i_shape, dtype=int),) + mat.shape[-3:])
    for idx_tup,val in zip(jacobian_proj_inds(ind_lists, axes=axes), vals):
        idx_tup = (...,) + idx_tup
        mat[idx_tup] = val
    mat = mat.reshape(target_shape)

    if smol:
        mat = mat.reshape(base_shape + mat.shape[-3:])
    return mat

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
    if not fast_proj:
        mats = np.zeros(coords.shape + (3,))
        return None, fill_disp_jacob_atom(
            mats,
            [[i, 1], [j, -1]],
            axes=axes,
            base_shape=coords.shape[:-2]
        )
    else:
        proj = np.zeros(coords.shape + (3 * len(at_list),))
        mats = np.zeros(coords[..., at_list, :].shape + (3,))
        _, (a, b), ord = np.intersect1d(at_list, [i, j], return_indices=True)
        inv = np.argsort(ord)
        a, b = np.array([a, b])[inv,]
        mats = fill_disp_jacob_atom(
            mats,
            [[a, 1], [b, -1]],
            axes=axes,
            base_shape=coords.shape[:-2]
        )
        proj = fill_proj_jacob_atom(
            proj,
            [[x, n, 1] for n,x in enumerate(at_list)],
            axes=axes,
            base_shape=coords.shape[:-2]
        )
        proj = proj.reshape(proj.shape[:-3] + (-1, proj.shape[-1]))
        return proj, mats

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
    a = coords[..., j, :] - coords[..., i, :]

    if expand:
        proj, A_d = disp_deriv_mat(coords, j, i, at_list)
        if fixed_atoms is not None:
            if fast_proj:
                _, fixed_atoms, _ = np.intersect1d(at_list, fixed_atoms, return_indices=True)
            if len(fixed_atoms) > 0:
                A_d = fill_disp_jacob_atom(A_d, [[x, 0] for x in fixed_atoms], base_shape=coords.shape[:-2])

        return proj, [a, misc.flatten_inds(A_d, [-3, -2])]
    else:
        return [a]

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
    _, (a, b), ord = np.intersect1d(at_list, [i, j], return_indices=True)
    inv = np.argsort(ord)
    a, b = np.array([a, b])[inv,]
    # a, b = np.sort([a,b])
    # print(at_list, (i, j), a, b)
    natl = len(at_list) * 3
    subpos = (np.array([a, b])[:, np.newaxis] * 3 + np.arange(3)[np.newaxis, :]).flatten()
    new = []
    if core_dim > 0:
        core_shape = expansion[0].shape[-core_dim:]
    else:
        core_shape = ()
    pad_dim = expansion[0].ndim - (root_dim + core_dim)
    base_shape = expansion[0].shape[:pad_dim]
    for n,e in enumerate(expansion):
        n = n + root_dim
        if n > 0:
            block = np.ix_(*[subpos]*n)
            idx = (...,) + block + (slice(None),)*core_dim
            new_sub = np.zeros(base_shape + (natl,) * n + core_shape)
            new_sub[idx] = e
        else:
            new_sub = e
        new.append(new_sub)
    return new

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

    if cache is None or fixed_atoms is not None or not expand:
        proj, A_expansion = prep_disp_expansion(coords, i, j, at_list,
                                                fixed_atoms=fixed_atoms,
                                                expand=expand)
        A_norms, A_expansion = td.vec_norm_unit_deriv(A_expansion, order)
    else:
        proj, A_base = prep_disp_expansion(coords, i, j, at_list,
                                                fixed_atoms=None,
                                                expand=True)

        # if i > j:
        #     j, i = i, j
        #     sign = -1
        # else:
        #     sign = 1
        sign = 1

        key = ((i, j), expand, fixed_atoms)
        A_norms = []
        if key in cache:
            (A_raw, A_norms, A_expansion) = cache[key]
        if len(A_norms) < (order + 1):
            _, A_raw = prep_disp_expansion(coords, i, j, [i, j],
                                                    fixed_atoms=None,
                                                    expand=True)
            A_norms, A_expansion = td.vec_norm_unit_deriv(A_raw, order)
            cache[key] = (A_raw, A_norms, A_expansion)

        A_norms = A_norms[:order+1]
        A_expansion = A_expansion[:order+1]

        # print(sign, i, j, at_list)
        # print(sign*A_norms[1])
        A_norms = prep_expanded_mats_from_cache(
            [A_norms[0]] + [(sign ** (n + 1)) * a for n, a in enumerate(A_norms[1:])],
            i, j, at_list,
            root_dim=0,
            core_dim=0
        )
        # print(A_norms[1])
        # print("-"*50)
        A_expansion = prep_expanded_mats_from_cache(
            [(sign ** (n + 1)) * a for n, a in enumerate(A_expansion)], i, j, at_list,
            root_dim=0,
            core_dim=1
        )
        # A_raw = prep_expanded_mats_from_cache(A_raw, i, j, at_list,
        #                                       root_dim=0,
        #                                       core_dim=1
        #                                       )
        # if np.max(np.abs(A_raw[1] - A_base[1])) > 1e-12:
        #     print(A_raw[1])
        #     print(A_base[1])
        #     raise ValueError(sign, i, j, at_list)
        # A_norms2, A_expansion2 = td.vec_norm_unit_deriv(A_base, len(A_base))
        # if np.max(np.abs(A_norms[1] - A_norms2[1])) > 1e-12:
        #     print(A_norms[1])
        #     print(A_norms2[1])
        #     raise ValueError(sign, i, j, at_list)
        # if np.max(np.abs(A_norms[2] - A_norms2[2])) > 1e-12:
        #     print(A_norms[2])
        #     print(A_norms2[2])
        #     raise ValueError(sign, i, j, at_list)
        # if np.max(np.abs(A_expansion[1] - A_expansion2[1])) > 1e-12:
        #     print(A_expansion[1])
        #     print(A_expansion2[1])
        #     raise ValueError(sign, i, j, at_list)
        # if np.max(np.abs(A_expansion[2] - A_expansion2[2])) > 1e-12:
        #     print(A_expansion[2])
        #     print(A_expansion2[2])
        #     raise ValueError(sign, i, j, at_list)
        # # (A_norms, A_expansion) = (A_norms2, A_expansion2)
    return proj, (A_norms, A_expansion)

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

    if order > 2:
        raise NotImplementedError("derivatives currently only up to order {}".format(2))

    derivs = []

    sin_derivs, cos_derivs = vec_sin_cos_derivs(a, b,
                                                up_vectors=up_vectors,
                                                order=order, zero_thresh=zero_thresh)
    # cos_expansion = [0] + [block_array(c, i+1) for i,c in enumerate(cos_derivs[1:])]
    # sin_expansion = [0] + [block_array(c, i+1) for i,c in enumerate(sin_derivs[1:])]
    # print(
    #     (cos_expansion[1][:, np.newaxis, np.newaxis] * sin_expansion[2][np.newaxis, :, :])[2][:3, :3]
    # )
    # print(
    #     (sin_expansion[1][:, np.newaxis, np.newaxis] * cos_expansion[2][np.newaxis, :, :])[2][:3, :3]
    # )

    s = sin_derivs[0]
    c = cos_derivs[0]

    q = np.arctan2(s, c)
    # # force wrapping if near to pi
    # if isinstance(q, np.ndarray):
    #     sel = np.abs(q) > np.pi - 1e-10
    #     q[sel] = np.abs(q[sel])
    # elif np.abs(q) > np.pi - 1e-10:
    #     q = np.abs(q)

    if up_vectors is not None:
        n = vec_crosses(a, b)
        if up_vectors.ndim < n.ndim:
            up_vectors = np.broadcast_to(up_vectors, n.shape[:-len(up_vectors.shape)] + up_vectors.shape)

        # zero_thresh = Options.norm_zero_threshold if zero_thresh is None else zero_thresh
        up = vec_dots(up_vectors, n)
        # up[np.abs(up) < zero_thresh] = 0.
        sign = np.sign(up)
    else:
        sign = np.ones(a.shape[:-1])

    if isinstance(sign, np.ndarray):
        sign[sign == 0] = 1.
    elif sign == 0:
        sign = np.array(1)

    derivs.append(sign*q)

    if order >= 1:
        # d = sin_derivs[1]
        # s_da = d[..., 0, :]; s_db = d[..., 1, :]
        # d = cos_derivs[1]
        # c_da = d[..., 0, :]; c_db = d[..., 1, :]
        #
        # q_da = c * s_da - s * c_da
        # q_db = c * s_db - s * c_db

        # we can do some serious simplification here
        # if we use some of the analytic work I've done
        # to write these in terms of the vector tangent
        # to the rotation

        a, na = vec_apply_zero_threshold(a, zero_thresh=zero_thresh)
        b, nb = vec_apply_zero_threshold(b, zero_thresh=zero_thresh)

        ha = a / na
        hb = b / nb

        ca = hb - (vec_dots(ha, hb)[..., np.newaxis]) * ha
        cb = ha - (vec_dots(hb, ha)[..., np.newaxis]) * hb

        ca, nca = vec_apply_zero_threshold(ca, zero_thresh=zero_thresh)
        cb, ncb = vec_apply_zero_threshold(cb, zero_thresh=zero_thresh)

        ca = ca / nca
        cb = cb / ncb

        q_da = -ca/na
        q_db = -cb/nb

        extra_dims = a.ndim - 1
        extra_shape = a.shape[:-1]

        d1 = (
            sign[np.newaxis, ..., np.newaxis] *
            np.array([q_da, q_db])
        )
        d1_reshape = tuple(range(1, extra_dims + 1)) + (0, extra_dims + 1)
        derivs.append(d1.transpose(d1_reshape))

    if order >= 2:

        d = sin_derivs[1]
        s_da = d[..., 0, :]; s_db = d[..., 1, :]
        d = cos_derivs[1]
        c_da = d[..., 0, :]; c_db = d[..., 1, :]

        d = sin_derivs
        s_daa = d[2][..., 0, 0, :, :]; s_dab = d[2][..., 0, 1, :, :]
        s_dba = d[2][..., 1, 0, :, :]; s_dbb = d[2][..., 1, 1, :, :]

        d = cos_derivs
        c_daa = d[2][..., 0, 0, :, :]; c_dab = d[2][..., 0, 1, :, :]
        c_dba = d[2][..., 1, 0, :, :]; c_dbb = d[2][..., 1, 1, :, :]

        c = c[..., np.newaxis]
        s = s[..., np.newaxis]
        q_daa = vec_outer(c_da, s_da) + c * s_daa - vec_outer(s_da, c_da) - s * c_daa
        q_dba = vec_outer(c_da, s_db) + c * s_dba - vec_outer(s_da, c_db) - s * c_dba
        q_dab = vec_outer(c_db, s_da) + c * s_dab - vec_outer(s_db, c_da) - s * c_dab
        q_dbb = vec_outer(c_db, s_db) + c * s_dbb - vec_outer(s_db, c_db) - s * c_dbb

        d2 = (
                sign[np.newaxis, np.newaxis, ..., np.newaxis, np.newaxis] *
                np.array([
                    [q_daa, q_dab],
                    [q_dba, q_dbb]
                ])
        )

        d2_reshape = tuple(range(2, extra_dims+2)) + (0, 1, extra_dims+2, extra_dims+3)

        derivs.append(
            d2.transpose(d2_reshape)
        )

    if return_comps:
        return derivs, (sin_derivs, cos_derivs)
    else:
        return derivs

def dist_deriv(coords, i, j, /, order=1, method='expansion', fixed_atoms=None,
               cache=None,
               expanded_vectors=None,
               reproject=True,
               zero_thresh=None):
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

    if method == 'expansion':
        proj, (base_deriv, _) = prep_unit_vector_expansion_from_cache(
            cache,
            coords, j, i, [i, j],
            order=order,
            fixed_atoms=fixed_atoms, expand=True
        )
        # proj, A_expansion = prep_disp_expansion(coords, j, i, [i, j], fixed_atoms=fixed_atoms, expand=True)
        # base_deriv = td.vec_norm_unit_deriv(A_expansion, order=order)[0]
        if proj is None: return base_deriv
        if reproject:
            base_deriv = [base_deriv[0]] + td.tensor_reexpand([proj], base_deriv[1:])
        return base_deriv
    else:

        if order > 2:
            raise NotImplementedError("derivatives currently only up to order {}".format(2))

        a = coords[..., j, :] - coords[..., i, :]
        d = vec_norm_derivs(a, order=order, zero_thresh=zero_thresh)

        derivs = []

        derivs.append(d[0])

        if order >= 1:
            da = d[1]
            derivs.append(np.array([-da, da]))

        if order >= 2:
            daa = d[2]
            # ii ij
            # ji jj
            derivs.append(np.array([
                [ daa, -daa],
                [-daa,  daa]
            ]))

        return derivs

def angle_deriv(coords, i, j, k, *, order=1, method='expansion',
                cache=None,
                up_vector=None,
                l=None,
                angle_ordering='jik',
                fixed_atoms=None,
                expanded_vectors=None,
                reproject=True,
                zero_thresh=None):
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

    if method == 'expansion':
        if expanded_vectors is None:
            expanded_vectors = [0, 1]
        if angle_ordering == 'ijk':
            proj, (A_norms, A_expansion) = prep_unit_vector_expansion_from_cache(
                cache,
                coords, i, j, [j, i, k],
                order=order, fixed_atoms=fixed_atoms, expand=0 in expanded_vectors
            )
            _, (B_norms, B_expansion) = prep_unit_vector_expansion_from_cache(
                cache,
                coords, k, j, [j, i, k],
                order=order, fixed_atoms=fixed_atoms, expand=1 in expanded_vectors
            )
        else:
            proj, (A_norms, A_expansion) = prep_unit_vector_expansion_from_cache(
                cache,
                coords, j, i, [i, j, k],
                order=order, fixed_atoms=fixed_atoms, expand=0 in expanded_vectors
            )
            _, (B_norms, B_expansion) = prep_unit_vector_expansion_from_cache(
                cache,
                coords, k, i, [i, j, k],
                order=order, fixed_atoms=fixed_atoms, expand=1 in expanded_vectors
            )

        if up_vector is None and l is not None:
            up_vector = vec_crosses(A_expansion[0], B_expansion[0])
            up_vector, up_norms = vec_normalize(up_vector, return_norms=True)
            bad_ups = up_norms <= Options.norm_zero_threshold
            up_vector[bad_ups] = vec_crosses(
                A_expansion[0][bad_ups], (coords[..., l, :] - coords[..., j, :]),
                normalize=True
            )

        # A_expansion = [A_expansion[0], np.concatenate([np.eye(3), np.zeros((3, 3))], axis=0)]
        # B_expansion = [B_expansion[0], np.concatenate([np.zeros((3, 3)), np.eye(3)], axis=0)]
        base_deriv = td.vec_angle_deriv(A_expansion, B_expansion,
                                        order=order, unitized=True,
                                        up_vector=up_vector)
        if proj is None: return base_deriv
        if reproject:
            base_deriv = [base_deriv[0]] + td.tensor_reexpand([proj], base_deriv[1:])
        return base_deriv
    else:
        if angle_ordering == 'ijk':
            # derivs = angle_deriv(coords, j, i, k, order=order, angle_ordering='jik',
            #                      method=method,
            #                      fixed_atoms=fixed_atoms,
            #                      expanded_vectors=expanded_vectors,
            #                      zero_thresh=zero_thresh
            #                      )
            # change signs if necessary
            raise NotImplementedError('too annoying')


        if order > 2:
            raise NotImplementedError("derivatives currently only up to order {}".format(2))

        a = coords[..., j, :] - coords[..., i, :]
        b = coords[..., k, :] - coords[..., i, :]
        d = vec_angle_derivs(a, b, order=order, zero_thresh=zero_thresh)

        derivs = []

        base_shape = coords.shape[:-2]
        derivs.append(d[0].reshape(base_shape))

        if order >= 1:
            da = d[1][..., 0, :]; db = d[1][..., 1, :]
            derivs.append(np.array([-(da + db), da, db]))

        if order >= 2:
            daa = d[2][..., 0, 0, :, :]; dab = d[2][..., 0, 1, :, :]
            dba = d[2][..., 1, 0, :, :]; dbb = d[2][..., 1, 1, :, :]
            # ii ij ik
            # ji jj jk
            # ki kj kk
            derivs.append(np.array([
                [daa + dba + dab + dbb, -(daa + dab), -(dba + dbb)],
                [         -(daa + dba),          daa,   dba       ],
                [         -(dab + dbb),          dab,   dbb       ]
            ]))

        return derivs

def normal_deriv(coords, i, j, k, *, order=1, method='expansion',
                 cache=None,
                 up_vector=None,
                 l=None,
                 angle_ordering='jik',
                 fixed_atoms=None,
                 expanded_vectors=None,
                 reproject=True,
                 normalize=True):
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

    if method == 'expansion':
        if expanded_vectors is None:
            expanded_vectors = [0, 1]
        if angle_ordering == 'ijk':
            proj, (A_norms, A_expansion) = prep_unit_vector_expansion_from_cache(
                cache,
                coords, i, j, [j, i, k],
                order=order, fixed_atoms=fixed_atoms, expand=0 in expanded_vectors
            )
            _, (B_norms, B_expansion) = prep_unit_vector_expansion_from_cache(
                cache,
                coords, k, j, [j, i, k],
                order=order, fixed_atoms=fixed_atoms, expand=1 in expanded_vectors
            )
        else:
            proj, (A_norms, A_expansion) = prep_unit_vector_expansion_from_cache(
                cache,
                coords, j, i, [i, j, k],
                order=order, fixed_atoms=fixed_atoms, expand=0 in expanded_vectors
            )
            _, (B_norms, B_expansion) = prep_unit_vector_expansion_from_cache(
                cache,
                coords, k, i, [i, j, k],
                order=order, fixed_atoms=fixed_atoms, expand=1 in expanded_vectors
            )

        if up_vector is None and l is not None:
            up_vector = vec_crosses(A_expansion[0], B_expansion[0])
            up_vector, up_norms = vec_normalize(up_vector, return_norms=True)
            bad_ups = up_norms <= Options.norm_zero_threshold
            up_vector[bad_ups] = vec_crosses(
                A_expansion[0][bad_ups], (coords[..., l, :] - coords[..., j, :]),
                normalize=True
            )

        # A_expansion = [A_expansion[0], np.concatenate([np.eye(3), np.zeros((3, 3))], axis=0)]
        # B_expansion = [B_expansion[0], np.concatenate([np.zeros((3, 3)), np.eye(3)], axis=0)]
        base_deriv = td.vec_normal_deriv(A_expansion, B_expansion, order=order, unitized=True, normalize=normalize)
        if proj is None: return base_deriv
        if reproject:
            base_deriv = [base_deriv[0]] + td.tensor_reexpand([proj], base_deriv[1:])
        return base_deriv
    else:
        raise NotImplementedError('too annoying')

def rock_deriv(coords, i, j, k, /, order=1, method='expansion', angle_ordering='ijk',
               cache=None,
               reproject=True,
               zero_thresh=None, fixed_atoms=None, expanded_vectors=None):
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


    if method == 'expansion':
        if expanded_vectors is None:
            expanded_vectors = [0, 1]

        if angle_ordering == 'ijk':
            proj, (A_norms, A_expansion) = prep_unit_vector_expansion_from_cache(
                cache,
                coords, i, j, [j, i, k],
                order=order, fixed_atoms=fixed_atoms, expand=0 in expanded_vectors
            )
            _, (B_norms, B_expansion) = prep_unit_vector_expansion_from_cache(
                cache,
                coords, k, j, [j, i, k],
                order=order, fixed_atoms=fixed_atoms, expand=1 in expanded_vectors
            )
        else:
            proj, (A_norms, A_expansion) = prep_unit_vector_expansion_from_cache(
                cache,
                coords, j, i, [i, j, k],
                order=order, fixed_atoms=fixed_atoms, expand=0 in expanded_vectors
            )
            _, (B_norms, B_expansion) = prep_unit_vector_expansion_from_cache(
                cache,
                coords, k, i, [i, j, k],
                order=order, fixed_atoms=fixed_atoms, expand=1 in expanded_vectors
            )

        A_deriv = td.vec_angle_deriv(A_expansion, B_expansion[:1], order=order, unitized=True)
        B_deriv = td.vec_angle_deriv(A_expansion[:1], B_expansion, order=order, unitized=True)
        base_deriv = [A_deriv[0]] + [ad - bd for ad,bd in zip(A_deriv[1:], B_deriv[1:])]
        if proj is None: return base_deriv
        if reproject:
            base_deriv = [base_deriv[0]] + td.tensor_reexpand([proj], base_deriv[1:])
        return base_deriv

    else:

        if angle_ordering == 'ijk':
            raise NotImplementedError("too annoying")

        if order > 2:
            raise NotImplementedError("derivatives currently only up to order {}".format(2))
        a = coords[..., j, :] - coords[..., i, :]
        b = coords[..., k, :] - coords[..., i, :]

        d = vec_angle_derivs(a, b, order=order, zero_thresh=zero_thresh)

        derivs = []

        derivs.append(d[0])

        if order >= 1:
            da = d[1][..., 0, :]; db = d[1][..., 1, :]
            derivs.append(np.array([-(da - db), da, -db]))

        if order >= 2:
            daa = d[2][..., 0, 0, :, :]; dab = d[2][..., 0, 1, :, :]
            dba = d[2][..., 1, 0, :, :]; dbb = d[2][..., 1, 1, :, :]
            # ii ij ik
            # ji jj jk
            # ki kj kk
            derivs.append(np.array([
                [daa + dba + dab + dbb, -(daa + dab), -(dba + dbb)],
                [         -(daa + dba),          daa,   dba       ],
                [         -(dab + dbb),          dab,   dbb       ]
            ]))

        return derivs

def dihed_deriv(coords, i, j, k, l, /, order=1, zero_thresh=None, method='expansion',
                fixed_atoms=None,
                cache=None,
                reproject=True,
                expanded_vectors=None):
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

    if method == 'expansion':
        if expanded_vectors is None:
            expanded_vectors = [0, 1, 2]
        proj, A_expansion = prep_disp_expansion(coords, j, i, [i, j, k, l], fixed_atoms=fixed_atoms, expand=0 in expanded_vectors)
        _, (B_norms, B_expansion) = prep_unit_vector_expansion_from_cache(
            cache,
            coords, j, k, [i, j, k, l], #TODO: patch explicit expansion flip, this convention necessary for opts
            order=order, fixed_atoms=fixed_atoms, expand=1 in expanded_vectors
        )
        _, C_expansion = prep_disp_expansion(coords, l, k, [i, j, k, l], fixed_atoms=fixed_atoms, expand=2 in expanded_vectors)
        base_deriv = td.vec_dihed_deriv(A_expansion, B_expansion, C_expansion,
                                        B_norms=B_norms,
                                        order=order)
        if proj is None: return base_deriv
        if reproject:
            base_deriv = [base_deriv[0]] + td.tensor_reexpand([proj], base_deriv[1:])
        return base_deriv

    else:
        if fixed_atoms is not None:
            raise NotImplementedError("direct derivatives with specified fixed atoms not implemented")
        if order > 2:
            raise NotImplementedError("derivatives currently only up to order {}".format(2))

        a = coords[..., j, :] - coords[..., i, :]
        b = coords[..., k, :] - coords[..., j, :]
        c = coords[..., l, :] - coords[..., k, :]

        n1 = vec_crosses(a, b)
        n2 = vec_crosses(b, c)

        # coll = vec_crosses(n1, n2)
        # coll_norms = vec_norms(coll)
        # bad = coll_norms < 1.e-17
        # if bad.any():
        #     raise Exception([
        #         bad,
        #         i, j, k, l,
        #         a[bad], b[bad], c[bad]])

        # zero_thresh = Options.norm_zero_threshold if zero_thresh is None else zero_thresh

        cnb = vec_crosses(n1, n2)

        cnb, n_cnb, bad_friends = vec_apply_zero_threshold(cnb, zero_thresh=zero_thresh, return_zeros=True)
        bad_friends = bad_friends.reshape(cnb.shape[:-1])
        orient = vec_dots(b, cnb)
        # orient[np.abs(orient) < 1.0] = 0.
        sign = np.sign(orient)

        d, (sin_derivs, cos_derivs) = vec_angle_derivs(n1, n2, order=order,
                                                       up_vectors=vec_normalize(b),
                                                       zero_thresh=zero_thresh, return_comps=True)

        derivs = []

        base_shape = coords.shape[:-2]
        derivs.append(d[0].reshape(base_shape))

        if order >= 1:
            dn1 = d[1][..., 0, :]; dn2 = d[1][..., 1, :]
            if dn1.ndim == 1:
                if bad_friends:
                    dn1 = sin_derivs[1][0]
                    dn2 = sin_derivs[1][1]
                    sign = np.array(1)
            else:
                dn1[bad_friends] = sin_derivs[1][bad_friends, 0, :] # TODO: clean up shapes I guess...
                dn2[bad_friends] = sin_derivs[1][bad_friends, 1, :]
                sign[bad_friends] = 1

            di = vec_crosses(b, dn1)
            dj = vec_crosses(c, dn2) - vec_crosses(a+b, dn1)
            dk = vec_crosses(a, dn1) - vec_crosses(b+c, dn2)
            dl = vec_crosses(b, dn2)

            deriv_tensors = sign[np.newaxis, ..., np.newaxis]*np.array([di, dj, dk, dl])

            # if we have problem points we deal with them via averaging
            # over tiny displacements since the dihedral derivative is
            # continuous
            # if np.any(bad_friends):
            #     raise NotImplementedError("planar dihedral angles remain an issue for me...")
            #     if coords.ndim > 2:
            #         raise NotImplementedError("woof")
            #     else:
            #         bad_friends = bad_friends.flatten()
            #         bad_i = i[bad_friends]
            #         bad_j = j[bad_friends]
            #         bad_k = k[bad_friends]
            #         bad_l = l[bad_friends]
            #         bad_coords = np.copy(coords)
            #         if isinstance(i, (int, np.integer)):
            #             raise NotImplementedError("woof")
            #         else:
            #             # for now we do this with finite difference...
            #             for which,(bi,bj,bk,bl) in enumerate(zip(bad_i, bad_j, bad_k, bad_l)):
            #                 for nat,at in enumerate([bi, bj, bk, bl]):
            #                     for x in range(3):
            #                         bad_coords[at, x] += zero_point_step_size
            #                         d01, = dihed_deriv(bad_coords, bi, bj, bk, bl, order=0, zero_thresh=-1.0)
            #                         bad_coords[at, x] -= 2*zero_point_step_size
            #                         d02, = dihed_deriv(bad_coords, bi, bj, bk, bl, order=0, zero_thresh=-1.0)
            #                         bad_coords[at, x] += zero_point_step_size
            #                         deriv_tensors[nat, which, x] = (d01[0] + d02[0])/(2*zero_point_step_size)
            #                         # print(
            #                         #     "D1", d1[nat, x]
            #                         #
            #                         # )
            #                         # print(
            #                         #     "D2", d2[nat, x]
            #                         #
            #                         # )
            #                         # print("avg", (d1[nat, x] + d2[nat, x])/2)
            #                         # print("FD", (d01[0], d02[0]))#/(2*zero_point_step_size))
            #                         # raise Exception(
            #                         #  "wat",
            #                         #     di,
            #                         # d01.shape
            #                         # )

            derivs.append(deriv_tensors)


        if order >= 2:

            d11 = d[2][..., 0, 0, :, :]; d12 = d[2][..., 0, 1, :, :]
            d21 = d[2][..., 1, 0, :, :]; d22 = d[2][..., 1, 1, :, :]

            # explicit write out of chain-rule transformations to isolate different Kron-delta terms
            extra_dims = a.ndim - 1
            extra_shape = a.shape[:-1]
            dot = lambda x, y, axes=(-1, -2) : vec_tensordot(x, y, axes=axes, shared=extra_dims)
            if extra_dims > 0:
                e3 = np.broadcast_to(pops.levi_cevita3,  extra_shape + pops.levi_cevita3.shape)
            else:
                e3 = pops.levi_cevita3

            Ca = dot(e3, a, axes=[-1, -1])
            Cb = dot(e3, b, axes=[-1, -1])
            Cc = dot(e3, c, axes=[-1, -1])
            Cab = Ca+Cb
            Cbc = Cb+Cc

            CaCa, CaCb, CaCc, CaCab, CaCbc = [dot(Ca, x) for x in (Ca, Cb, Cc, Cab, Cbc)]
            CbCa, CbCb, CbCc, CbCab, CbCbc = [dot(Cb, x) for x in (Ca, Cb, Cc, Cab, Cbc)]
            CcCa, CcCb, CcCc, CcCab, CcCbc = [dot(Cc, x) for x in (Ca, Cb, Cc, Cab, Cbc)]
            CabCa, CabCb, CabCc, CabCab, CabCbc = [dot(Cab, x) for x in (Ca, Cb, Cc, Cab, Cbc)]
            CbcCa, CbcCb, CbcCc, CbcCab, CbcCbc = [dot(Cbc, x) for x in (Ca, Cb, Cc, Cab, Cbc)]

            dii = dot(CbCb, d11)
            dij = dot(CcCb, d12) - dot(CabCb, d11)
            dik = dot(CaCb, d11) - dot(CbcCb, d12)
            dil = dot(CbCb, d12)

            dji = dot(CbCc, d21) - dot(CbCab, d11)
            djj = dot(CabCab, d11) - dot(CabCc, d21) - dot(CcCab, d12) + dot(CcCc, d22)
            djk = dot(CbcCab, d12) - dot(CbcCc, d22) - dot(CaCab, d11) + dot(CaCc, d21)
            djl = dot(CbCc, d22) - dot(CbCab, d12)

            dki = dot(CbCa, d11) - dot(CbCbc, d21)
            dkj = dot(CabCbc, d21) - dot(CcCbc, d22) - dot(CabCa, d11) + dot(CcCa, d12)
            dkk = dot(CaCa, d11) - dot(CaCbc, d21) - dot(CbcCa, d12) + dot(CbcCbc, d22)
            dkl = dot(CbCa, d12) - dot(CbCbc, d22)

            dli = dot(CbCb, d21)
            dlj = dot(CcCb, d22) - dot(CabCb, d21)
            dlk = dot(CaCb, d21) - dot(CbcCb, d22)
            dll = dot(CbCb, d22)

            derivs.append(
                -sign[np.newaxis, np.newaxis, ..., np.newaxis, np.newaxis] *
                np.array([
                    [dii, dij, dik, dil],
                    [dji, djj, djk, djl],
                    [dki, dkj, dkk, dkl],
                    [dli, dlj, dlk, dll]
                ])
            )

    return derivs

def book_deriv(coords, i, j, k, l, /, order=1, zero_thresh=None, method='expansion',
               fixed_atoms=None,
               cache=None,
               reproject=True,
               expanded_vectors=None):
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
    if method == 'expansion':
        if expanded_vectors is None:
            expanded_vectors = [0, 1, 2]

        proj, A_expansion = prep_disp_expansion(coords, j, i, [i, j, k, l], fixed_atoms=fixed_atoms, expand=0 in expanded_vectors)
        _, (B_norms, B_expansion) = prep_unit_vector_expansion_from_cache(
            cache,
            coords, k, j, [i, j, k, l],
            order=order, fixed_atoms=fixed_atoms, expand=1 in expanded_vectors
        )
        _, C_expansion = prep_disp_expansion(coords,  l, j, [i, j, k, l], fixed_atoms=fixed_atoms, expand=2 in expanded_vectors)

        base_deriv = td.vec_dihed_deriv(A_expansion, B_expansion, C_expansion, order=order)
        if proj is None: return base_deriv
        if reproject:
            base_deriv = [base_deriv[0]] + td.tensor_reexpand([proj], base_deriv[1:])
        return base_deriv
    else:
        raise NotImplementedError("too annoying")

def wag_deriv(coords, i, j, k, l=None, *, order=1, method='expansion',
              cache=None,
              reproject=True,
               fixed_atoms=None,
               expanded_vectors=None):
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
    if method == 'expansion':
        if fixed_atoms is None: fixed_atoms = []
        fixed_atoms = list(fixed_atoms) + [j]
        if expanded_vectors is None:
            expanded_vectors = [0, 1]
        # proj, A_expansion = prep_disp_expansion(coords, j, i, [i, j, k], fixed_atoms=fixed_atoms, expand=0 in expanded_vectors)
        # _, B_expansion = prep_disp_expansion(coords, k, j, [i, j, k], fixed_atoms=fixed_atoms, expand=1 in expanded_vectors)
        # _, C_expansion = prep_disp_expansion(coords, i, k, [i, j, k], fixed_atoms=fixed_atoms, expand=2 in expanded_vectors)

        # base_deriv = td.vec_dihed_deriv(A_expansion, B_expansion, C_expansion, order=order)
        # if proj is None: return base_deriv
        # return [base_deriv[0]] + td.tensor_reexpand([proj], base_deriv[1:])

        proj, A_expansion = prep_disp_expansion(coords, j, i, [i, j, k], fixed_atoms=fixed_atoms,
                                                expand=0 in expanded_vectors)
        _, (B_norms, B_expansion) = prep_unit_vector_expansion_from_cache(
            cache,
            coords, k, j, [i, j, k],
            order=order, fixed_atoms=fixed_atoms, expand=1 in expanded_vectors
        )
        if l is None:
            l = i
        C_expansion = prep_disp_expansion(coords, l, k, [i, j, k], fixed_atoms=fixed_atoms, expand=2 in expanded_vectors)
        if len(C_expansion) > 1:
            _, C_expansion = C_expansion
        base_deriv = td.vec_dihed_deriv(A_expansion, B_expansion, C_expansion,
                                        B_norms=B_norms,
                                        order=order)
        if proj is None: return base_deriv
        if reproject:
            base_deriv = [base_deriv[0]] + td.tensor_reexpand([proj], base_deriv[1:])
        return base_deriv
    else:
        raise NotImplementedError("too annoying")

def plane_angle_deriv(coords, i, j, k, l, m, n, /, order=1,
                      method='expansion',
                      fixed_atoms=None,
                      cache=None,
                      reproject=True,
                      expanded_vectors=None,

                      ):
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
    if method == 'expansion':
        if expanded_vectors is None:
            expanded_vectors = [0, 1, 2, 3]
        atom_list = [i, j, k, l, m, n]
        proj, A_expansion = prep_disp_expansion(coords, j, i, atom_list, fixed_atoms=fixed_atoms, expand=0 in expanded_vectors)
        _, B_expansion = prep_disp_expansion(coords, k, j, atom_list, fixed_atoms=fixed_atoms, expand=1 in expanded_vectors)
        _, C_expansion = prep_disp_expansion(coords, m, l, atom_list, fixed_atoms=fixed_atoms, expand=2 in expanded_vectors)
        _, D_expansion = prep_disp_expansion(coords, n, m, atom_list, fixed_atoms=fixed_atoms, expand=3 in expanded_vectors)

        base_deriv = td.vec_plane_angle_deriv(A_expansion, B_expansion, C_expansion, D_expansion, order=order)
        if proj is None: return base_deriv
        if reproject:
            base_deriv = [base_deriv[0]] + td.tensor_reexpand([proj], base_deriv[1:])
        return base_deriv
    else:
        raise NotImplementedError("too annoying")

def oop_deriv(coords, i, j, k, l=None, *, order=1, method='expansion',
              fixed_atoms=None,
              cache=None,
              reproject=True,
              expanded_vectors=None):
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
    if method == 'expansion':
        if fixed_atoms is None: fixed_atoms = []
        fixed_atoms = list(fixed_atoms) + [j]
        if expanded_vectors is None:
            expanded_vectors = [0, 1]
        at_list = [x for x in [i, j, k] if x is not None]
        proj, A_expansion = prep_disp_expansion(coords, j, i, at_list, fixed_atoms=fixed_atoms, expand=0 in expanded_vectors)
        _, (B_norms, B_expansion) = prep_unit_vector_expansion_from_cache(
            cache,
            coords, k, j, at_list,
            order=order, fixed_atoms=fixed_atoms, expand=1 in expanded_vectors
        )
        if l is None:
            l = i
        C_expansion = prep_disp_expansion(coords, l, k, at_list, fixed_atoms=fixed_atoms, expand=2 in expanded_vectors)
        if len(C_expansion) > 1:
            _, C_expansion = C_expansion

        # _, D_expansion = prep_disp_expansion(coords, n, m, [i, j, k, l, m, n], fixed_atoms=fixed_atoms, expand=2 in expanded_vectors)

        i_deriv = td.vec_dihed_deriv(A_expansion, B_expansion[:1], C_expansion, order=order)
        k_deriv = td.vec_dihed_deriv(A_expansion[:1], B_expansion, C_expansion, order=order)
        base_deriv = [i_deriv[0]] + [ad - bd for ad, bd in zip(i_deriv[1:], k_deriv[1:])]
        if proj is None: return base_deriv
        if reproject:
            base_deriv = [base_deriv[0]] + td.tensor_reexpand([proj], base_deriv[1:])
        return base_deriv
    else:
        raise NotImplementedError("too annoying")

def transrot_deriv(coords, *pos, order=1, masses=None, return_rot=True, return_frame=False,
                   cache=None,
                   reproject=True,
                   axes=None,
                   fixed_atoms=None):
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
    coords = np.asanyarray(coords)
    if len(pos) > 0:
        if masses is not None:
            masses = np.asanyarray(masses)[pos,]
        subcoords = coords[..., pos, :]
    else:
        subcoords = coords
    (com, eigs), principle_axes = frames.translation_rotation_eigenvectors(
        subcoords,
        masses,
        mass_weighted=False,
        return_com=True,
        return_rot=return_rot,
        return_principle_axes=True,
        axes=axes
    )

    nc = com.shape[-1]
    expansion = [com]
    if order > 0:
        n = coords.shape[-2] * 3
        if len(pos) > 0:
            subpos = (np.asanyarray(pos)[:, np.newaxis] * 3 + np.arange(3)[np.newaxis, :]).flatten()
            _ = np.zeros(coords.shape[:-2] + (n, nc))
            _[..., subpos, :] = eigs
            eigs = _
        if fixed_atoms is not None:
            fixed_pos = (np.asanyarray(fixed_atoms)[:, np.newaxis] * 3 + np.arange(3)[np.newaxis, :]).flatten()
            eigs[..., fixed_pos, :] = 0
        expansion.append(eigs)

        for o in range(1, order):
            # is this right? I guess probably given the form of the rotation generator...
            expansion.append(
                np.zeros(coords.shape[:-2] + (n,) * (o+1) + (nc,))
            )

    if return_frame:
        return expansion, principle_axes
    else:
        return expansion

def com_dist_deriv(coords, frame_pos_1, frame_pos_2, *, order=1, masses=None,
                   cache=None,
                   reproject=True,
                   fixed_atoms=None):
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
    #TODO: could also include the com vec if that was useful...
    coords = np.asanyarray(coords)
    com_deriv1 = transrot_deriv(coords, *frame_pos_1, masses=masses, order=order,
                             return_rot=False,
                             fixed_atoms=fixed_atoms)
    com_deriv2 = transrot_deriv(coords, *frame_pos_2, masses=masses, order=order,
                             return_rot=False,
                             fixed_atoms=fixed_atoms)

    #TODO: restrict the number of displaced positions for efficiency
    disp_exp = [cd1 - cd2 for cd1, cd2 in zip(com_deriv1, com_deriv2)]

    norm_deriv, _ = td.vec_norm_unit_deriv(disp_exp, order=order)
    return norm_deriv

def moment_of_inertia_expansion_deriv(coords, *pos, order=1, masses=None,
                                      cache=None,
                                      reproject=True,
                                      fixed_atoms=None):
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
    coords = np.asanyarray(coords)
    if len(pos) > 0:
        if masses is not None:
            masses = np.asanyarray(masses)[pos,]
        subcoords = coords[..., pos, :]
    else:
        subcoords = coords
    vals, vecs = frames.moments_of_inertia_expansion(subcoords, order=order, masses=masses, mass_weighted=False)
    if len(pos) > 0 and order > 0:
        val_expansion = [vals[0]]
        vec_expansion = [vecs[0]]

        n = coords.shape[-2] * 3
        subpos = (np.asanyarray(pos)[:, np.newaxis] * 3 + np.arange(3)[np.newaxis, :]).flatten()
        for i,(val_set, vec_set) in enumerate(zip(vals[1:], vecs[1:])):
            new_vals = np.zeros(val_set.shape[:-(i+2)] + (n,)*(i+1) + val_set.shape[-1:])
            idx = (...,) + np.ix_(*[subpos]*(i+1)) + (slice(None),)
            new_vals[idx] = val_set
            val_expansion.append(new_vals)

            new_vecs = np.zeros(vec_set.shape[:-(i+3)] + (n,)*(i+1) + vec_set.shape[-2:])
            idx = (...,) + np.ix_(*[subpos]*(i+1)) + (slice(None), slice(None),)
            new_vecs[idx] = vec_set
            vec_expansion.append(new_vecs)

        vals = val_expansion
        vecs = vec_expansion

    if fixed_atoms is not None:
        subpos = (np.asanyarray(fixed_atoms)[:, np.newaxis] * 3 + np.arange(3)[np.newaxis, :]).flatten()
        for i, (val_set, vec_set) in enumerate(zip(vals[1:], vecs[:1])):
            idx = (...,) + np.ix_(*[subpos] * (i + 1)) + (slice(None),)
            val_set[idx] = 0

            idx = (...,) + np.ix_(*[subpos] * (i + 1)) + (slice(None),)
            vec_set[idx] = 0

    return vals, vecs

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
    coords = np.asanyarray(coords)
    if len(pos) > 0:
        if masses is not None:
            masses = np.asanyarray(masses)[pos,]
        subcoords = coords[..., pos, :]
    else:
        subcoords = coords
    return frames.moments_of_inertia(subcoords, masses=masses, return_com=True)

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
    base_shape = axes.shape[:-2]
    axes = axes.reshape(-1, 3, 3)
    cos_rot1 = pops.levi_cevita_dot(3, axes, axes=[0, -1], shared=1)  # kx3bx3cx3j
    com = com.reshape(-1, 3)
    coords = coords.reshape((-1,) + coords.shape[-2:])
    if com is not None:
        shift_coords = coords - com[:, np.newaxis, :]
    else:
        shift_coords = coords
    rot_vecs1 = -vec_tensordot(
        shift_coords, cos_rot1,
        shared=1,
        axes=[-1, 1]
    )
    return rot_vecs1.reshape(base_shape + (coords.shape[-2]*coords.shape[-1], 3))

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
    c1 = coords[..., frame_pos_1, :]
    m1 = masses[frame_pos_1,]
    c2 = coords[..., frame_pos_2, :]
    m2 = masses[frame_pos_2,]
    com1 = frames.center_of_mass(c1, m1)
    _, axes1 = frames.moments_of_inertia(c1, m1)
    com2 = frames.center_of_mass(c2, m2)
    _, axes2 = frames.moments_of_inertia(c2, m2)

    ax1 = com2 - com1
    z1 = axes1[..., 2, :]
    z2 = axes2[..., 2, :]
    ax2 = vec_crosses(z1, z2)
    return (com1, axes1), (com2, axes2), transforms.view_matrix(ax2, view_vector=ax1)

def orientation_deriv(coords, frame_pos_1, frame_pos_2, *, order=1, masses=None,
                      fixed_atoms=None,
                      cache=None,
                      reproject=True,
                      return_frame=False,
                      return_rot=True
                      ):
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
    coords = np.asanyarray(coords)
    if masses is None:
        masses = np.ones(coords.shape[-2])
    masses = np.asanyarray(masses, dtype=float)
    _, _, axes = _orientation_axis_system(coords, frame_pos_1, frame_pos_2, masses)

    disps1, axes1 = transrot_deriv(coords, *frame_pos_1,
                                   order=order,
                                   masses=masses,
                                   fixed_atoms=fixed_atoms,
                                   return_frame=True,
                                   return_rot=return_rot,
                                   axes=axes
                                   )
    disps2, axes2 = transrot_deriv(coords, *frame_pos_2,
                                   order=order,
                                   masses=masses,
                                   fixed_atoms=fixed_atoms,
                                   return_frame=True,
                                   return_rot=return_rot,
                                   axes=axes
                                   )

    m1 = np.sum(masses[frame_pos_1,])
    m2 = np.sum(masses[frame_pos_2,])

    norm = np.sqrt(m1**2+m2**2)
    p1 = m1 / norm
    p2 = m2 / norm

    # p1 = 1/np.sqrt(2)
    # p2 = 1/np.sqrt(2)

    # p1 = np.sqrt(2)
    # p2 = np.sqrt(2)

    total_expansion = [
        (cd1*p1 - cd2*p2)
        for cd1, cd2 in zip(disps1, disps2)
    ]

    # if return_rot:
    #     angle_expansion = []
    #
    #     rot1 = axes1
    #     # rot1 = identity_tensors(coords.shape[:-2], 3)
    #     rot_vecs1 = _rot_deriv_vecs(rot1, coords[..., frame_pos_1, :], disps1[0][..., :3])
    #     full_vecs1 = np.zeros(rot_vecs1.shape[:-2] + (3*coords.shape[-2], 3), dtype=rot_vecs1.dtype)
    #     idx1 = block_broadcast_indices(frame_pos_1, 3)
    #     full_vecs1[..., idx1, :] = rot_vecs1
    #
    #     rot2 = axes2
    #     # rot2 = identity_tensors(coords.shape[:-2], 3)
    #     rot_vecs2 = _rot_deriv_vecs(rot2, coords[..., frame_pos_2, :], disps2[0][..., :3])
    #     full_vecs2 = np.zeros(rot_vecs2.shape[:-2] + (3 * coords.shape[-2], 3), dtype=rot_vecs1.dtype)
    #     idx2 = block_broadcast_indices(frame_pos_2, 3)
    #     full_vecs2[..., idx2, :] = rot_vecs2
    #
    #     for i in range(3):
    #         vecs1 = [axes1[..., i]]
    #         # for d in [full_vecs1]:#disps1[1:]:
    #         #     base_vec = d[..., i]
    #         #     new_tensor = np.zeros(base_vec.shape + (3,))
    #         #     new_tensor[..., ::3, 0] = base_vec[..., ::3]
    #         #     new_tensor[..., 1::3, 1] = base_vec[..., 1::3]
    #         #     new_tensor[..., 2::3, 2] = base_vec[..., 2::3]
    #         #     vecs1.append(new_tensor)
    #         #
    #         vecs2 = [axes2[..., i]]
    #         # for d in [full_vecs2]:#disps2[1:]:
    #         #     base_vec = d[..., i]
    #         #     new_tensor = np.zeros(base_vec.shape + (3,))
    #         #     new_tensor[..., ::3, 0] = base_vec[..., ::3]
    #         #     new_tensor[..., 1::3, 1] = base_vec[..., 1::3]
    #         #     new_tensor[..., 2::3, 2] = base_vec[..., 2::3]
    #         #     vecs2.append(new_tensor)
    #
    #         # subexpansion = td.vec_angle_deriv(
    #         #     vecs1,
    #         #     vecs2,
    #         #     up_vector=axes1[..., (i + 2) % 3],
    #         #     order=order
    #         # )
    #
    #         full_vec = full_vecs1[..., :, i] + full_vecs2[..., :, i]
    #         subexpansion = [
    #             vec_angles(vecs1[0], vecs2[0], return_crosses=False),
    #             full_vec
    #         ]
    #         angle_expansion.append(subexpansion)
    #
    #     total_expansion = [
    #         np.concatenate([xyz, a[..., np.newaxis], b[..., np.newaxis], c[..., np.newaxis]], axis=-1)
    #         for a,b,c,xyz in zip(*angle_expansion, xyz_expansion)
    #     ]
    # else:
    #     total_expansion = xyz_expansion


    if return_frame:
        return total_expansion, ((disps1[0], axes1), (disps2[0], axes2))
    else:
        return total_expansion

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
    # bond_vectors = np.zeros(coords.shape)
    # bond_vectors[..., i, :] = bond_tf[0]
    # bond_vectors[..., j, :] = bond_tf[1]
    #
    # return bond_vectors.reshape(
    #     coords.shape[:-2] + (coords.shape[-2] * coords.shape[-1],)
    # )
    return _fill_derivs(coords, (i, j), [0, bond_tf], method='expansion')[1]
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
    vals = []
    # nx = np.prod(coords.shape, dtype=int)
    nats = coords.shape[-2]
    nidx = len(idx)
    if method != 'old':
        subpos = (np.array(idx)[:, np.newaxis] * 3 + np.arange(3)[np.newaxis, :]).flatten()
    else:
        subpos = None
    base_shape = coords.shape[:-2]
    for n, d in enumerate(derivs):
        if n == 0:
            vals.append(d)
            continue
        if method == 'old':
            tensor = np.zeros((nats, 3) * n)
            for pos in itertools.product(*[range(nidx) for _ in range(n)]):
                actual = ()
                for r in pos:
                    actual += (slice(None) if idx[r] is None else idx[r], slice(None))
                tensor[actual] = d[pos]
        else:
            tensor = np.zeros(base_shape + (nats*3,) * n)
            block = np.ix_(*[subpos] * n)
            idx = (...,) + block #+ (slice(None),)*core_dim
            tensor[idx] = d
        vals.append(tensor.reshape(base_shape + (nats * 3,) * n))
    return vals
def dist_vec(coords, i, j, order=None, method='expansion', cache=None, reproject=True, fixed_atoms=None):
    """
    Returns the full vectors that define the linearized version of a bond displacement

    :param coords:
    :param i:
    :param j:
    :return:
    """

    derivs = dist_deriv(coords, i, j, method=method, order=(1 if order is None else order),
                        cache=cache,
                        reproject=reproject,
                        fixed_atoms=fixed_atoms)
    if reproject and method == 'expansion':
        return derivs[1] if order is None else derivs
    else:
        if order is None:
            return _pop_bond_vecs(derivs[1], i, j, coords)
        else:
            return _fill_derivs(coords, (i,j), derivs, method=method)

def angle_vec(coords, i, j, k, order=None, up_vector=None, l=None,
              method='expansion', angle_ordering='ijk',
              cache=None, reproject=True, fixed_atoms=None):
    """
    Returns the full vectors that define the linearized version of an angle displacement

    :param coords:
    :param i:
    :param j:
    :return:
    """
    coords = np.asanyarray(coords)

    if method != "expansion" and angle_ordering == 'ijk':
        i, j, k = j, i, k
        angle_ordering = 'jik'
    derivs = angle_deriv(coords, i, j, k, order=(1 if order is None else order), method=method,
                         cache=cache, l=l,
                         reproject=reproject,
                         up_vector=up_vector,
                         angle_ordering=angle_ordering,
                         fixed_atoms=fixed_atoms)
    if reproject and method == 'expansion':
        return derivs[1] if order is None else derivs
    else:
        if angle_ordering == 'ijk':
            full = _fill_derivs(coords, (j, i, k), derivs, method=method)
        else:
            full = _fill_derivs(coords, (i, j, k), derivs, method=method)
        if order is None:
            return full[1]
        else:
            return full

def rock_vec(coords, i, j, k, order=None, method='expansion',
             cache=None, reproject=True,
             angle_ordering='ijk',
             fixed_atoms=None):
    """
    Returns the full vectors that define the linearized version of an angle displacement

    :param coords:
    :param i:
    :param j:
    :return:
    """

    derivs = rock_deriv(coords, i, j, k, order=(1 if order is None else order),
                        cache=cache, reproject=reproject,
                        fixed_atoms=fixed_atoms, method=method)
    if reproject and method == 'expansion':
        return derivs[1] if order is None else derivs
    else:
        if angle_ordering == 'ijk':
            full = _fill_derivs(coords, (j, i, k), derivs, method=method)
        else:
            full = _fill_derivs(coords, (i, j, k), derivs, method=method)
        if order is None:
            return full[1]
        else:
            return full

def dihed_vec(coords, i, j, k, l, order=None, method='expansion', cache=None, reproject=True, fixed_atoms=None):
    """
    Returns the full vectors that define the linearized version of a dihedral displacement

    :param coords:
    :param i:
    :param j:
    :return:
    """
    derivs = dihed_deriv(coords, i, j, k, l, method=method, order=(1 if order is None else order),
                         cache=cache,
                         reproject=reproject,
                         fixed_atoms=fixed_atoms)
    if reproject and method == 'expansion':
        return derivs[1] if order is None else derivs
    else:
        full = _fill_derivs(coords, (i, j, k, l), derivs, method=method)
        if order is None:
            return full[1]
        else:
            return full

def book_vec(coords, i, j, k, l, order=None, method='expansion', cache=None, reproject=True, fixed_atoms=None):
    """
    Returns the full vectors that define the linearized version of a dihedral displacement

    :param coords:
    :param i:
    :param j:
    :return:
    """

    if method == 'expansion':
        derivs = book_deriv(coords, i, j, k, l,
                            method=method, order=(1 if order is None else order),
                            cache=cache,
                            reproject=reproject,
                            fixed_atoms=fixed_atoms)
        if reproject:
            return derivs[1] if order is None else derivs
        else:
            full = _fill_derivs(coords, (i, j, k, l), derivs, method=method)
            if order is None:
                return full[1]
            else:
                return full
    else:
        derivs = dihed_deriv(coords, j, k, i, l, order=(1 if order is None else order), method=method,
                             fixed_atoms=fixed_atoms)
        full = _fill_derivs(coords, (i, j, k, l), derivs)
        if order is None:
            return full[1]
        else:
            return full

def oop_vec(coords, i, j, k, l=None, order=None, method='expansion', cache=None, reproject=True, fixed_atoms=None):
    """
    Returns the full vectors that define the linearized version of an oop displacement

    :param coords:
    :param i:
    :param j:
    :return:
    """

    if method == 'expansion':
        derivs = oop_deriv(coords, i, j, k, l=l, order=(1 if order is None else order),
                           cache=cache,
                           reproject=reproject,
                           method=method, fixed_atoms=fixed_atoms)
        if reproject:
            return derivs[1] if order is None else derivs
        else:
            full = _fill_derivs(coords, (i, j, k), derivs, method=method)
            if order is None:
                return full[1]
            else:
                return full
    else:
        dihed_tf = dihed_deriv(coords, i, k, j, i, order=(1 if order is None else order), method=method,
                               fixed_atoms=fixed_atoms,
                               expanded_vectors=[0]
                               )
        full = _fill_derivs(coords, (i, j, k, None), dihed_tf)
        if order is None:
            return full[1]
        else:
            return full
        # if order is not None and order > 1:
        #     raise NotImplementedError("OOP deriv reshaping not done yet")
        # else:
        #     dihed_tf = dihed_tf[1]
        # dihed_vectors = np.zeros(coords.shape)
        # dihed_vectors[..., i, :] = dihed_tf[0]
        # dihed_vectors[..., j, :] = dihed_tf[1]
        # dihed_vectors[..., k, :] = dihed_tf[2]
        #
        # return dihed_vectors.reshape(
        #     coords.shape[:-2] + (coords.shape[-2] * coords.shape[-1],)
        # )

def wag_vec(coords, i, j, k, l=None, order=None, method='expansion', cache=None, reproject=True, fixed_atoms=None):
    """
    Returns the full vectors that define the linearized version of an oop displacement

    :param coords:
    :param i:
    :param j:
    :return:
    """

    if method == 'expansion':
        derivs = wag_deriv(coords, i, j, k, l=l, order=(1 if order is None else order),
                           cache=cache, reproject=reproject,
                           method=method, fixed_atoms=fixed_atoms)
        if reproject:
            return derivs[1] if order is None else derivs
        else:
            full = _fill_derivs(coords, (i, j, k), derivs, method=method)
            if order is None:
                return full[1]
            else:
                return full
    else:
        raise NotImplementedError("too annoying")

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
    if method == 'expansion':
        derivs = plane_angle_deriv(coords, i, j, k, l, m, n, order=(1 if order is None else order),
                           cache=cache, reproject=reproject,
                           method=method, fixed_atoms=fixed_atoms)
        if reproject:
            return derivs[1] if order is None else derivs
        else:
            full = _fill_derivs(coords, (i, j, k, l, m, n), derivs, method=method)
            if order is None:
                return full[1]
            else:
                return full
    else:
        raise NotImplementedError("too annoying")

def transrot_vecs(coords, *pos, order=None, masses=None, return_rot=True,
                  cache=None, reproject=True, fixed_atoms=None):
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
    derivs = transrot_deriv(coords, *pos,
                            order=(1 if order is None else order),
                            masses=masses,
                            return_rot=return_rot,
                            return_frame=False, fixed_atoms=fixed_atoms)
    return derivs[1] if order is None else derivs

def orientation_vecs(coords, frame_pos_1, frame_pos_2, *, order=None, masses=None,
                     cache=None, reproject=True, fixed_atoms=None,
                     return_rot=True):
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
    derivs = orientation_deriv(coords, frame_pos_1, frame_pos_2,
                               order=(1 if order is None else order),
                               masses=masses, return_frame=False,
                               fixed_atoms=fixed_atoms,
                               return_rot=return_rot)
    return derivs[1] if order is None else derivs

coord_type_map = {
    'dist':dist_vec,
    'bend':angle_vec,
    'rock':rock_vec,
    'dihed':dihed_vec,
    'book':book_vec,
    'oop':oop_vec,
    'wag':wag_vec,
    'transrot':transrot_vecs,
    'orientation':orientation_vecs,
    'plane_angle':plane_angle_vec
}
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
    if coord_type_dispatch is None:
        coord_type_dispatch = coord_type_map
    targets = []
    for idx in specs:
        if isinstance(idx, dict):
            for k in coord_type_dispatch.keys():
                if k in idx:
                    coord_type = k
                    subopts = idx.copy()
                    idx = idx[k]
                    del subopts[k]
                    break
            else:
                raise ValueError("can't parse coordinate spec {}".format(idx))
        elif hasattr(idx, 'get_expansion'): # forward integrate with Internals stuff
            coord_type = idx.get_expansion
            subopts = {}
        else:
            nidx = len(idx)
            if nidx == 2:
                coord_type = 'dist'
            elif nidx == 3:
                coord_type = 'bend'
            elif nidx == 4:
                coord_type = 'dihed'
            else:
                raise ValueError("can't parse coordinate spec {}".format(idx))
            subopts = {}

        if coord_type in {'bend', 'rock'}: # very common to change
            subopts['angle_ordering'] = subopts.get('angle_ordering', angle_ordering)
        targets.append(
            (coord_type_dispatch[coord_type], idx, dict(opts, **subopts))
                if isinstance(coord_type, str) else
            (coord_type, (), dict(opts, **subopts))
        )

    return targets

def combine_coordinate_deriv_expansions(expansions,
                                        order=None,
                                        base_dim=0,
                                        base_transformation=None,
                                        reference_internals=None):
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
    if order is None:
        targets = [
            np.expand_dims(t, -1)
                if t.ndim - 1 == base_dim else
            t
            for t in expansions
        ]
        base = np.concatenate(targets, axis=-1)
        if base_transformation is not None:
            base = td.tensor_reexpand(base, base_transformation)  # del_XR * del_RQ
    else:
        targets = [
            [
                np.expand_dims(t, -1)
                    if t.ndim - i == base_dim else
                t
                for i, t in enumerate(subt)
            ]
            for subt in expansions
        ]
        base = [
            np.concatenate(t, axis=-1)
            for t in zip(*targets)
        ]
        internals, expansion = base[0], base[1:]
        if reference_internals is not None:
            if reference_internals.ndim == 1 and internals.ndim > 1:
                reference_internals = np.expand_dims(reference_internals, list(range(internals.ndim - 1)))
            internals = internals - reference_internals
        if base_transformation is not None:
            if base_transformation[0].ndim == 2 and len(expansion) > 0 and expansion[0].ndim > 2:
                base_transformation = [
                    np.broadcast_to(
                        np.expand_dims(b, list(range(expansion[0].ndim - 2))),
                        expansion[0].shape[:-2] + b.shape
                    ) for b in base_transformation
                ]
            internals = (internals[..., np.newaxis, :] @ base_transformation[0]).reshape(
                internals.shape[:-1] + base_transformation[0].shape[-1:]
            )
            expansion = (
                td.tensor_reexpand(expansion, base_transformation, order=len(expansion))
                    if len(expansion) > 0 else
                expansion
            )
        base = [internals] + expansion

    return base

def internal_conversion_function(specs,
                                 base_transformation=None,
                                 reference_internals=None,
                                 use_cache=True,
                                 reproject=False,
                                 **opts):
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
    base_specs = internal_conversion_specs(specs, **opts)
    def convert(coords, order=None,
                use_cache=use_cache,
                reference_internals=reference_internals,
                base_transformation=base_transformation):
        """
        **LLM Docstring**

        Evaluate the configured internal coordinates (and their derivative expansion)
        for a Cartesian geometry.

        Runs every normalized coordinate spec, collecting each expansion, then combines
        them with `combine_coordinate_deriv_expansions` using the enclosing
        transformation/reference settings. An expansion cache is shared across
        coordinates when `use_cache` is set.

        :param coords: Cartesian coordinates, shape `(..., N, 3)`
        :type coords: np.ndarray
        :param order: maximum derivative order (`None` = values only)
        :type order: int | None
        :param use_cache: whether to share an expansion cache
        :type use_cache: bool
        :param reference_internals: reference internal values to subtract
        :type reference_internals: np.ndarray | None
        :param base_transformation: optional transformation into a new coordinate basis
        :type base_transformation: list[np.ndarray] | None
        :return: the combined expansion `[internals, d1, d2, ...]`
        :rtype: list
        """
        targets = []
        #
        if use_cache:
            cache = {}
        else:
            cache = None
        for f, idx, subopts in base_specs:
            res = f(coords, *idx, **dict(subopts, reproject=reproject, cache=cache, order=order))
            targets.append(res)

        base_dim = coords.ndim - 2
        return combine_coordinate_deriv_expansions(
            targets,
            order=order,
            base_dim=base_dim,
            base_transformation=base_transformation,
            reference_internals=reference_internals
        )
    return convert

def internal_coordinate_tensors(coords, specs, order=None, return_inverse=False, masses=None,
                                fixed_atoms=None,
                                fixed_cartesians=None,
                                fixed_coords=None,
                                remove_inverse_translation_rotation=True,
                                **opts):
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
    coords = np.asanyarray(coords)
    base_tensors = internal_conversion_function(specs, **opts)(
        coords,
        order=order
    )
    if order is None:
        bt = [base_tensors]
    else:
        bt = base_tensors[1:]
    bt = prep_internal_derivatives(bt,
                                   fixed_atoms=fixed_atoms,
                                   fixed_cartesians=fixed_cartesians,
                                   fixed_coords=fixed_coords
                                   )
    if order is None:
        base_tensors = bt[0]
    else:
        base_tensors = base_tensors[:1] + bt
    if return_inverse:
        if order is None:
            bt = [base_tensors]
        else:
            bt = base_tensors[1:]
        return base_tensors, inverse_internal_coordinate_tensors(bt, coords, masses=masses, order=order,
                                                                 fixed_atoms=fixed_atoms,
                                                                 fixed_coords=fixed_coords,
                                                                 fixed_cartesians=fixed_cartesians,
                                                                 remove_translation_rotation=remove_inverse_translation_rotation
                                                                 )
    else:
        return base_tensors

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
    copied = False
    if fixed_atoms is not None:
        atom_pos = np.reshape(
            (np.array(fixed_atoms) * 3)[:, np.newaxis]
            + np.arange(3)[np.newaxis],
            -1
        )
        expansion = [e.copy() for e in expansion]
        copied = True
        for n, e in enumerate(expansion):
            idx = (...,) + np.ix_(*[atom_pos] * (n + 1)) + (slice(None),)
            e[idx] = 0
    if fixed_cartesians is not None:
        if not copied:
            expansion = [e.copy() for e in expansion]
            copied = True
        fc = np.array(fixed_cartesians)
        fc = 3*fc[:, 0] + fc[:, 1]
        for n, e in enumerate(expansion):
            idx = (...,) + np.ix_(*[fc] * (n + 1)) + (slice(None),)
            e[idx] = 0
    if fixed_coords is not None:
        if not copied:
            expansion = [e.copy() for e in expansion]
            copied = True
        for n, e in enumerate(expansion):
            e[..., fixed_coords] = 0

    return expansion

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
    copied = False
    if fixed_atoms is not None:
        atom_pos = np.reshape(
            (np.array(fixed_atoms) * 3)[:, np.newaxis]
            + np.arange(3)[np.newaxis],
            -1
        )
        expansion = [e.copy() for e in expansion]
        copied = True
        for n, e in enumerate(expansion):
            e[..., atom_pos] = 0
    if fixed_cartesians is not None:
        if not copied:
            expansion = [e.copy() for e in expansion]
            copied = True
        fc = np.array(fixed_cartesians)
        fc = 3*fc[:, 0] + fc[:, 1]
        for n, e in enumerate(expansion):
            e[..., fc] = 0
    if fixed_coords is not None:
        if not copied:
            expansion = [e.copy() for e in expansion]
            copied = True
        for n, e in enumerate(expansion):
            idx = (...,) + np.ix_(*[fixed_coords] * (n + 1)) + (slice(None),)
            e[idx] = 0

    return expansion

_transrot_projection_method = 'addition'
_pre_mass_weight = True
def inverse_internal_coordinate_tensors(expansion,
                                        coords=None, masses=None, order=None,
                                        mass_weighted=True,
                                        remove_translation_rotation=True,
                                        fixed_atoms=None,
                                        fixed_coords=None,
                                        fixed_cartesians=None,
                                        ):
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
    from .CoordinateFrames import translation_rotation_invariant_transformation, translation_rotation_eigenvectors

    if order is None:
        order = len(expansion)

    expansion = prep_internal_derivatives(
        expansion,
        fixed_atoms=fixed_atoms,
        fixed_coords=fixed_coords,
        fixed_cartesians=fixed_cartesians
    )

    if coords is not None and remove_translation_rotation:
        # expansion = remove_translation_rotations(expansion, coords[opt_inds], masses)
        if _pre_mass_weight and masses is not None:
            base_shape = coords.shape[:-2]
            g12 = np.diag(np.repeat(1 / np.sqrt(masses), 3))
            if len(base_shape) > 0:
                g12 = np.repeat(
                    g12[np.newaxis],
                    np.prod(base_shape),
                    axis=0
                ).reshape(base_shape + g12.shape)
            expansion = td.tensor_reexpand([g12], expansion, len(expansion))
        if _transrot_projection_method == 'projector':
            #TODO: is this the correct definition? Do we want to project out before or after the inverse?
            L_base, L_inv = translation_rotation_invariant_transformation(coords, masses,
                                                                          mass_weighted=True,
                                                                          strip_embedding=True)
            new_tf = td.tensor_reexpand([L_inv], expansion, order)
            inverse_tf = td.inverse_transformation(new_tf, order, allow_pseudoinverse=True)
            inverse_expansion = [
                vec_tensordot(j, np.moveaxis(L_inv, -1, -2), axes=[-1, -1], shared=L_base.ndim - 2)
                    if not misc.is_numeric(j) else
                j
                for j in inverse_tf
            ]
        else:
            _, tr = translation_rotation_eigenvectors(coords, masses, mass_weighted=_pre_mass_weight)
            tr_expansion = [tr]
            n = tr.shape[-1]
            for e in expansion[1:]:
                base_shape = e.shape[:-1]
                final_shape = base_shape + (n,)
                tr_expansion.append(np.zeros(final_shape))
            total_exp = [np.concatenate([t, e], axis=-1) for t,e in zip(tr_expansion, expansion)]
            inverse_tf = td.inverse_transformation(total_exp, order, allow_pseudoinverse=True)
            inverse_expansion = []
            for i,t in enumerate(inverse_tf):
                idx = (...,) + (slice(n, None),)*(i+1) + (slice(None),)
                inverse_expansion.append(t[idx])
        if _pre_mass_weight  and masses is not None:
            inverse_expansion = td.tensor_reexpand(inverse_expansion, [g12], order)
    elif mass_weighted and masses is not None:
        sqrt_mass = np.expand_dims(
            np.repeat(
                np.diag(np.repeat(1 / np.sqrt(masses), 3)),
                coords.shape[0],
                axis=0
            ),
            list(range(expansion[0].ndim - 2))
        )
        expansion = td.tensor_reexpand([sqrt_mass], expansion, len(expansion))
        inverse_expansion = td.inverse_transformation(expansion, order=order, allow_pseudoinverse=True)
        inverse_expansion = td.tensor_reexpand(inverse_expansion, [sqrt_mass], order)
    else:
        inverse_expansion = td.inverse_transformation(expansion, order=order, allow_pseudoinverse=True)

    inverse_expansion = prep_inverse_derivatives(inverse_expansion,
                                                 fixed_atoms=fixed_atoms,
                                                 fixed_coords=fixed_coords,
                                                 fixed_cartesians=fixed_cartesians)

    return inverse_expansion

def rotation_expansion_from_axis_angle(coords, axis, order=1, *, angle=0., axis_order=0):
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
    axis = vec_normalize(axis)
    if axis.ndim > 1:
        ## TODO: get this off the slow path
        ax_shape = axis.shape[:-1]
        coords = np.asanyarray(coords)
        coord_shape = coords.shape[:-2]
        if ax_shape == coord_shape:
            blocks = [
                rotation_expansion_from_axis_angle(c, a, order=order, angle=angle, axis_order=axis_order)
                for c,a in zip(
                    coords.reshape((-1,) + coords.shape[-2:]),
                    axis.reshape((-1,) + axis.shape[-1:])
                )
            ]
            #TODO: handle mixed axis orders
            return [
                np.concatenate([
                    exp[i][np.newaxis, ...]
                    for exp in blocks
                ], axis=0)
                for i in range(order+1)
            ]
        else:
            raise NotImplementedError("multi-axis broadcasting is tedious")

    R_expansion = geom.axis_rot_gen_deriv(angle, axis, angle_order=order, axis_order=axis_order)
    if axis_order == 0:
        return [
            (coords[..., np.newaxis, :] @ np.moveaxis(R, -1, -2)).reshape(
                coords.shape
                    if i == 0 else
                (coords.shape[:-2] + (coords.shape[-2] * coords.shape[-1],))
            )
            for i,R in enumerate(R_expansion)
        ]
    else:
        extra = coords.ndim - 2
        base_expansion = [
            np.moveaxis(np.tensordot(coords, R, axes=[-1, -1]), extra, -2)
            for R in R_expansion
        ]
        return [
            np.reshape(
                e,
                e.shape[:-2] + (e.shape[-2] * e.shape[-1],)
            ) if i > 0 else e
            for i,e in enumerate(base_expansion)
        ]

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
    rem_atoms = np.setdiff1d(np.arange(len(coords)), np.concatenate([left_atoms, right_atoms]))
    left_pos = block_broadcast_indices(left_atoms, 3)
    # right_pos = block_broadcast_indices(right_atoms, 3)
    rem_pos = block_broadcast_indices(rem_atoms, 3)
    if len(left_pos) > 0:
        right_expansion[0][..., left_atoms, :] = left_expansion[0][..., left_atoms, :]
    if len(rem_atoms) > 0:
        right_expansion[0][..., rem_atoms, :] = coords[..., rem_atoms, :]
    for e,l in zip(right_expansion[1:], left_expansion[1:]):
        if len(left_pos) > 0:
            e[..., left_pos] = l[..., left_pos]
        if len(rem_pos) > 0:
            e[..., rem_pos] = 0
    return right_expansion

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
    coords = np.asanyarray(coords)
    vec = vec_normalize(coords[..., j, :] - coords[..., i, :]) / 2
    base_shape = coords.shape[:-2]
    targ_shape = base_shape + (coords.shape[-2] * coords.shape[-1],)
    right_expansion = [coords + (amount/2)*vec[..., np.newaxis, :]]
    for o in range(order):
        term = np.zeros(coords.shape)
        if o == 0:
            term[..., :] = vec
        right_expansion.append(term.reshape(targ_shape))
    left_expansion = [coords - (amount/2)*vec[..., np.newaxis, :]]
    for o in range(order):
        term = np.zeros(coords.shape)
        if o == 0:
            term[..., :] = -vec
        left_expansion.append(term.reshape(targ_shape))

    if left_atoms is None:
        left_atoms = [i]
    elif include_core and i not in left_atoms:
        left_atoms = [i] + list(left_atoms)
    if right_atoms is None:
        right_atoms = [j]
    elif include_core and j not in right_atoms:
        right_atoms = [j] + list(right_atoms)
    _handle_expansion_atom_exclusions(coords, left_expansion, right_expansion, left_atoms, right_atoms)
    return right_expansion

def angle_expansion(coords, i, j, k, order=1, left_atoms=None, right_atoms=None, *,
                    include_core=True,
                    angle=0, axis_order=0):
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
    coords = np.asanyarray(coords)
    shift_coords = coords - coords[..., (j,), :]
    axis = vec_crosses(coords[..., i, :] - coords[..., j, :],
                       coords[..., k, :] - coords[..., j, :],
                       normalize=True)
    right_expansion = rotation_expansion_from_axis_angle(shift_coords, axis, order=order, angle=angle/2, axis_order=axis_order)
    left_expansion = rotation_expansion_from_axis_angle(shift_coords, -axis, order=order, angle=angle/2, axis_order=axis_order)
    #TODO: fix this
    left_expansion[0] += coords[..., (j,), :] # shift back from origin
    right_expansion[0] += coords[..., (j,), :] # shift back from origin
    if left_atoms is None:
        left_atoms = [i]
    elif include_core and i not in left_atoms:
        left_atoms = [i] + list(left_atoms)
    if right_atoms is None:
        right_atoms = [k]
    elif include_core and k not in right_atoms:
        right_atoms = [k] + list(right_atoms)
    _handle_expansion_atom_exclusions(coords, left_expansion, right_expansion, left_atoms, right_atoms)
    right_expansion = right_expansion[:1] + [e/2 for e in right_expansion[1:]]
    return right_expansion

def dihed_expansion(coords, i, j, k, l, order=1, left_atoms=None, right_atoms=None, *,
                    include_core=True,
                    angle=0, axis_order=0):
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
    coords = np.asanyarray(coords)
    shift_coords = coords - coords[..., (k,), :]
    axis = shift_coords[..., j, :]
    right_expansion = rotation_expansion_from_axis_angle(shift_coords, -axis, order=order, angle=angle/2, axis_order=axis_order)
    left_expansion = rotation_expansion_from_axis_angle(shift_coords, axis, order=order, angle=angle/2, axis_order=axis_order)
    # left might not always be the negation...I think
    left_expansion[0] += coords[..., (k,), :] # shift back from origin
    right_expansion[0] += coords[..., (k,), :] # shift back from origin

    if left_atoms is None:
        left_atoms = [i]
    elif include_core and i not in left_atoms:
        left_atoms = [i] + list(left_atoms)
    if right_atoms is None:
        right_atoms = [l]
    elif include_core and l not in right_atoms:
        right_atoms = [l] + list(right_atoms)
    _handle_expansion_atom_exclusions(coords, left_expansion, right_expansion, left_atoms, right_atoms)
    right_expansion = right_expansion[:1] + [e/2 for e in right_expansion[1:]]
    return right_expansion

def oop_expansion(coords, i, j, k, order=1, left_atoms=None, right_atoms=None, *,
                  include_core=True,
                  angle=0, axis_order=0):
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
    coords = np.asanyarray(coords)
    shift_coords = coords - coords[..., (j,), :]
    axis = (shift_coords[..., i, :] + shift_coords[..., k, :]) / 2
    right_expansion = rotation_expansion_from_axis_angle(shift_coords, -axis, order=order, angle=angle/2, axis_order=axis_order)
    left_expansion = rotation_expansion_from_axis_angle(shift_coords, axis, order=order, angle=angle/2, axis_order=axis_order)
    # left might not always be the negation...I think
    left_expansion[0] += coords[..., (j,), :] # shift back from origin
    right_expansion[0] += coords[..., (j,), :] # shift back from origin

    if left_atoms is None:
        left_atoms = [i]
    elif include_core and i not in left_atoms:
        left_atoms = [i] + list(left_atoms)
    if right_atoms is None:
        right_atoms = [k]
    elif include_core and k not in right_atoms:
        right_atoms = [k] + list(right_atoms)
    _handle_expansion_atom_exclusions(coords, left_expansion, right_expansion, left_atoms, right_atoms)
    right_expansion = right_expansion[:1] + [e/2 for e in right_expansion[1:]]
    return right_expansion

def wag_expansion(coords, i, j, k, order=1, left_atoms=None, right_atoms=None, *,
                  include_core=True,
                  angle=0, axis_order=0):
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
    coords = np.asanyarray(coords)
    shift_coords = coords - coords[..., (j,), :]
    axis = (shift_coords[..., i, :] + shift_coords[..., k, :]) / 2
    right_expansion = rotation_expansion_from_axis_angle(shift_coords, axis, order=order, angle=angle/2, axis_order=axis_order)
    left_expansion = rotation_expansion_from_axis_angle(shift_coords, axis, order=order, angle=angle/2, axis_order=axis_order)
    # left might not always be the negation...I think
    left_expansion[0] += coords[..., (j,), :] # shift back from origin
    right_expansion[0] += coords[..., (j,), :] # shift back from origin

    if left_atoms is None:
        left_atoms = [i]
    elif include_core and i not in left_atoms:
        left_atoms = [i] + list(left_atoms)
    if right_atoms is None:
        right_atoms = [k]
    elif include_core and k not in right_atoms:
        right_atoms = [k] + list(right_atoms)
    _handle_expansion_atom_exclusions(coords, left_expansion, right_expansion, left_atoms, right_atoms)
    right_expansion = right_expansion[:1] + [e/2 for e in right_expansion[1:]]
    return right_expansion

def transrot_expansion(coords, *pos, order=1,
                       shift=None,
                       rotation=None,
                       masses=None,
                       axes=None,
                       extra_atoms=None,
                       return_rot=True,
                       return_frame=False
                       ):
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
    coords = np.asanyarray(coords)
    if len(pos) == 0:
        pos = np.arange(coords.shape[-2])
    if masses is None:
        masses = np.ones(coords.shape[-2])
    full_masses = np.asanyarray(masses)
    full_coords = coords.copy()
    if extra_atoms is None:
        extra_atoms = []
    transformation_unit = tuple(pos) + tuple(extra_atoms)
    ref = coords[..., pos, :]
    ref_masses = masses[pos,]
    coords = coords[..., transformation_unit, :]
    masses = masses[transformation_unit,]
    if axes is None:
        _, principle_axes = frames.moments_of_inertia(ref, ref_masses)
    else:
        principle_axes = axes
    if shift is not None:
        shift = np.asanyarray(shift) @ principle_axes
        coords = coords[..., :, :] + shift[..., np.newaxis, :]
    if rotation is not None:
        com = frames.center_of_mass(ref, ref_masses)
        rot = (
            transforms.rotation_matrix(principle_axes[0], rotation[0])
            @ transforms.rotation_matrix(principle_axes[1], rotation[1])
            @ transforms.rotation_matrix(principle_axes[2], rotation[2])
        )
        coords = (coords - com[..., np.newaxis, :]) @ rot + (com[..., np.newaxis, :])

    (freqs, eigs), values, frame = frames.translation_rotation_eigenvectors(
        coords,
        ref=ref,
        masses=masses,
        axes=axes,
        ref_masses=ref_masses,
        return_rot=return_rot,
        mass_weighted=True,
        return_principle_axes=True,
        return_values=True,
        return_com=True
    )

    full_coords[..., transformation_unit, :] = coords
    expansion = [full_coords]
    if order > 0:
        base_shape = eigs.shape[:-2]
        full_eigs = np.zeros(base_shape + (3*len(full_masses),) + eigs.shape[-1:], dtype=eigs.dtype)
        idx = block_broadcast_indices(transformation_unit, 3)
        full_eigs[..., idx, :] = eigs
        eigs = full_eigs

        W = np.diag(np.repeat(1/np.sqrt(full_masses), 3))
        eigs = np.tensordot(eigs, W, axes=[-2, 0])
        # eigs = np.moveaxis(eigs, -2, -1)
        expansion.append(eigs)

        for n in range(2, order+1):
            exp = np.zeros(base_shape + (eigs.shape[-1:] * n) + (3 * len(full_masses),), dtype=eigs.dtype)
            expansion.append(exp)


    if return_frame:
        return expansion, frame
    else:
        return expansion

def orientation_expansion(coords, frame_pos_1, frame_pos_2, *, order=1, masses=None,
                          fixed_atoms=None,
                          cache=None,
                          reproject=True,
                          return_frame=False,
                          left_extra_atoms=None,
                          right_extra_atoms=None,
                          shift=None,
                          rotation=None,
                          return_rot=True
                          ):
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
    #TODO: could also include the com vec if that was useful...
    coords = np.asanyarray(coords)
    if masses is None:
        masses = np.ones(coords.shape[-2])

    (com_1, axes_1), (com_2, axes_2), axes = _orientation_axis_system(coords, frame_pos_1, frame_pos_2, masses)

    if left_extra_atoms is None:
        left_extra_atoms = []
    if right_extra_atoms is None:
        right_extra_atoms = []

    translation_unit_1 = list(frame_pos_1) + list(left_extra_atoms)
    translation_unit_2 = list(frame_pos_2) + list(right_extra_atoms)

    m1 = np.sum(masses[frame_pos_1,])
    m2 = np.sum(masses[frame_pos_2,])

    norm = np.sqrt(m1**2+m2**2)
    p1 = m1 / norm
    p2 = m2 / norm

    # p1 = p2 = 1/np.sqrt(2)

    left_expansion = transrot_expansion(coords, *frame_pos_1,
                                order=order,
                                masses=masses,
                                extra_atoms=left_extra_atoms,
                                return_rot=return_rot,
                                axes=axes,
                                shift=(np.asanyarray(shift) * (p1**2) if shift is not None else shift),
                                rotation=(np.asanyarray(rotation) * (p1**2) if rotation is not None else rotation)
                                )
    right_expansion = transrot_expansion(coords, *frame_pos_2,
                                order=order,
                                masses=masses,
                                extra_atoms=right_extra_atoms,
                                return_rot=return_rot,
                                axes=axes,
                                shift=(-np.asanyarray(shift) * (p2**2) if shift is not None else shift),
                                rotation=(-np.asanyarray(rotation) * (p2**2) if rotation is not None else rotation)
                                )

    left_expansion = [left_expansion[0]] + [e*p1 for e in left_expansion[1:]]
    right_expansion = [right_expansion[0]] + [-e*p2 for e in right_expansion[1:]]
    _handle_expansion_atom_exclusions(coords, left_expansion, right_expansion, translation_unit_1, translation_unit_2)
    expansion = right_expansion
    # if shift is not None:
    #     shift = np.asanyarray(shift)
    #     if shift.ndim == 1:
    #         shift = np.expand_dims(shift[np.newaxis, :], list(range(coords.ndim - shift.ndim-1)))
    #     com_diff_signs = np.sign(com_1 - com_2)
    #     delta = com_diff_signs * shift / 2
    #     coords[..., translation_unit_1, :] += delta
    #     coords[..., translation_unit_2, :] -= delta
    #
    # if return_rot:
    #     if rotation is not None:
    #         rotation = np.asanyarray(rotation)
    #         if rotation.ndim > 1:
    #             rotation = np.moveaxis(rotation, -1, 0)
    #         rot1 = (
    #             transforms.rotation_matrix(axes[..., 0, :], rotation[0]/2)
    #             @ transforms.rotation_matrix(axes[..., 1, :], rotation[1]/2)
    #             @ transforms.rotation_matrix(axes[..., 2, :], rotation[2]/2)
    #         )
    #         sub1 = coords[..., translation_unit_1, :]
    #         coords[..., translation_unit_1, :] = (sub1 - com_1[..., np.newaxis, :]) @ rot1 + (com_1[..., np.newaxis, :])
    #
    #         rot2 = (
    #             transforms.rotation_matrix(axes[..., 0, :], -rotation[0]/2)
    #             @ transforms.rotation_matrix(axes[..., 1, :], -rotation[1]/2)
    #             @ transforms.rotation_matrix(axes[..., 2, :], -rotation[2]/2)
    #         )
    #         sub2 = coords[..., translation_unit_2, :]
    #         coords[..., translation_unit_2, :] = (sub2 - com_2[..., np.newaxis, :]) @ rot2 + (com_2[..., np.newaxis, :])
    #
    # expansion = [coords]
    # if order > 0:
    #     base_shape = coords.shape[:-2]
    #     nats = coords.shape[-2]
    #     com_disp = np.zeros(base_shape + (3, nats * 3))
    #     m1 = masses[translation_unit_1,] / np.sqrt(2 * np.sum(masses[frame_pos_1,]))
    #     M = np.kron(m1, np.eye(3))  # translation eigenvectors
    #     pos = block_broadcast_indices(translation_unit_1, 3)
    #     com_disp[..., :, pos] = M
    #
    #     m2 = masses[translation_unit_2,] / np.sqrt(2 * np.sum(masses[frame_pos_2,]))
    #     M = np.kron(m2, np.eye(3))  # translation eigenvectors
    #     pos = block_broadcast_indices(translation_unit_2, 3)
    #     com_disp[..., :, pos] = -M
    #
    #     com_expansion = [com_disp]
    #     for i in range(2, order+1):
    #         com_expansion.append(np.zeros(base_shape + (3,)*i + (nats * 3,)))
    #
    #     if return_rot:
    #         if rotation is None:
    #             rotation = [0, 0, 0]
    #         rotation = np.asanyarray(rotation)
    #
    #         sub1 = coords[..., translation_unit_1, :] - (com_1[..., np.newaxis, :])
    #         rot_disp_11 = rotation_expansion_from_axis_angle(
    #             sub1,
    #             rotation_axis_1,
    #             order=order,
    #             angle=rotation[0]/2
    #         )
    #         rot_disp_12 = rotation_expansion_from_axis_angle(
    #             sub1,
    #             rotation_axis_2,
    #             order=order,
    #             angle=rotation[1]/2
    #         )
    #         rot_disp_13 = rotation_expansion_from_axis_angle(
    #             sub1,
    #             rotation_axis_3,
    #             order=order,
    #             angle=rotation[2]/2
    #         )
    #
    #         sub2 = coords[..., translation_unit_2, :] - (com_2[..., np.newaxis, :])
    #         rot_disp_21 = rotation_expansion_from_axis_angle(
    #             sub2,
    #             -rotation_axis_1,
    #             order=order,
    #             angle=rotation[0] / 2
    #         )
    #         rot_disp_22 = rotation_expansion_from_axis_angle(
    #             sub2,
    #             -rotation_axis_2,
    #             order=order,
    #             angle=rotation[1] / 2
    #         )
    #         rot_disp_23 = rotation_expansion_from_axis_angle(
    #             sub2,
    #             -rotation_axis_3,
    #             order=order,
    #             angle=rotation[2] / 2
    #         )
    #
    #         rot_exp = []
    #         pos1 = block_broadcast_indices(translation_unit_1, 3)
    #         pos2 = block_broadcast_indices(translation_unit_2, 3)
    #         for i in range(1, order+1):
    #             exp_term = np.zeros(base_shape + (3,)*i + (nats * 3,))
    #             for n,(a,b) in enumerate(zip(
    #                     [rot_disp_11, rot_disp_12, rot_disp_13],
    #                     [rot_disp_21, rot_disp_22, rot_disp_23]
    #             )):
    #                 sel = (...,) + (n,) * i # diagonal for now
    #                 sel_1 = sel + (pos1,)
    #                 exp_term[sel_1] = a[i]
    #                 sel_2 = sel + (pos2,)
    #                 exp_term[sel_2] = b[i]
    #             rot_exp.append(exp_term)
    #
    #         full_exp = []
    #         for i in range(1, order+1):
    #             exp_term = np.zeros(base_shape + (6,)*i + (nats * 3,))
    #             sel_1 = (...,) + (slice(3),) * i + (slice(None),)
    #             exp_term[sel_1] = com_expansion[i-1]
    #             sel_2 = (...,) + (slice(3,6),) * i + (slice(None),)
    #             exp_term[sel_2] = rot_exp[i-1]
    #             full_exp.append(exp_term)
    #     else:
    #         full_exp = com_expansion
    #
    #     expansion = expansion + full_exp
    return expansion

def combine_coordinate_inverse_expansions(expansions,
                                          order=None,
                                          base_dim=None,
                                          base_transformation=None):
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
    coords = [e[0] for e in expansions]
    if base_dim is None:
        base_dim = coords[0].ndim - 2
    expansions = [e[1:] for e in expansions]
    # if order is None:
    #     targets = [
    #         np.expand_dims(t, -1)
    #             if t.ndim - 1 == base_dim else
    #         t
    #         for t in expansions
    #     ]
    #     base = np.concatenate(targets, axis=-1)
    #     if base_transformation is not None:
    #         base = td.tensor_reexpand(base, base_transformation)  # del_XR * del_RQ
    # else:
    targets = [
        [
            np.expand_dims(t, list(range(base_dim, base_dim+i+1)))
                if t.ndim - 1 == base_dim else
            t
            for i, t in enumerate(subt)
        ]
        for subt in expansions
    ]
    base = td.concatenate_expansions(targets, concatenate_values=False)
    if base_transformation is not None:
        base = td.tensor_reexpand(base_transformation, base, axes=[-1, -2])

    if order is None:
        base = base[0]
    else:
        base = [coords] + base

    return base

class _inverse_coordinate_conversion_caller:
    def __init__(self, conversion, target_internals,
                 remove_translation_rotation=True,
                 masses=None,
                 order=1,
                 gradient_function=None,
                 gradient_scaling=None,
                 fixed_atoms=None,
                 fixed_coords=None
                 ):
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
        self.conversion = conversion
        self.target_internals = target_internals
        self.masses = masses
        self.remove_translation_rotation = remove_translation_rotation
        self.gradient_function = gradient_function
        self.gradient_scaling = gradient_scaling
        self.last_call = None
        self.caller_order = order
        self.fixed_atoms = fixed_atoms
        self.fixed_coords = fixed_coords

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
        coords = coords.reshape(coords.shape[0], -1, 3)
        internals = self.conversion(coords, order=0)[0]
        delta = internals - self.target_internals[mask]
        return np.sum(delta, axis=1)

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
        ord = self.caller_order
        coords = coords.reshape(coords.shape[0], -1, 3)
        expansion = self.last_call = self.conversion(coords, order=ord)
        internals, expansion = expansion[0], expansion[1:] # dr/dx
        delta = internals - self.target_internals[mask]
        fixed_coords = self.fixed_coords

        if self.fixed_atoms is not None:
            atom_pos = np.reshape(
                (np.array(self.fixed_atoms) * 3)[:, np.newaxis]
                + np.arange(3)[np.newaxis],
                -1
            )
            for n,e in enumerate(expansion):
                idx = (...,) + np.ix_(*[atom_pos] * (n + 1)) + (slice(None),)
                e[idx] = 0
        if fixed_coords is not None:
            for n,e in enumerate(expansion):
                e[..., fixed_coords] = 0

        if self.remove_translation_rotation: # dx/dr
            inverse_expansion = inverse_internal_coordinate_tensors(expansion, coords, self.masses, ord)
        else:
            sqrt_mass = np.expand_dims(
                np.repeat(
                    np.diag(np.repeat(1 / np.sqrt(self.masses), 3)),
                    coords.shape[0],
                    axis=0
                ),
                list(range(expansion[0].ndim - 2))
            )
            expansion = td.tensor_reexpand([sqrt_mass], expansion, len(expansion))
            inverse_expansion = td.inverse_transformation(expansion, order=ord, allow_pseudoinverse=True)
            inverse_expansion = td.tensor_reexpand(inverse_expansion, [sqrt_mass], ord)

        if self.fixed_atoms is not None:
            atom_pos = np.reshape(
                    (np.array(self.fixed_atoms) * 3)[:, np.newaxis]
                    + np.arange(3)[np.newaxis],
                -1
            )
            for n,e in enumerate(inverse_expansion):
                e[..., atom_pos] = 0
        if fixed_coords is not None:
            delta[..., fixed_coords] = 0
            for n,e in enumerate(inverse_expansion):
                idx = (...,) + np.ix_(*[fixed_coords]*(n+1)) + (slice(None),)
                e[idx] = 0

        nr_change = 0
        for n, e in enumerate(inverse_expansion):
            for ax in range(n + 1):
                e = vec_tensordot(e, delta, axes=[1, -1], shared=1)
            nr_change += (1 / math.factorial(n + 1)) * e

        if self.gradient_function is not None:
            if self.fixed_atoms is not None:
                subcrd = np.delete(coords, self.fixed_atoms, axis=-2).reshape(coords.shape[0], -1)
                subgrad = self.gradient_function(subcrd, mask)
                contrib = np.zeros((coords.shape[0], coords.shape[1]*coords.shape[2]), dtype=subgrad.dtype)
                atom_pos = np.reshape(
                    (np.array(self.fixed_atoms) * 3)[:, np.newaxis]
                    + np.arange(3)[np.newaxis],
                    -1
                )
                rem_pos = np.delete(np.arange(contrib.shape[1]), atom_pos)
                contrib[..., rem_pos] = subgrad
            else:
                contrib = self.gradient_function(coords.reshape(coords.shape[0], -1), mask)
            extra_gradient = -self.gradient_scaling * contrib
            nr_change = nr_change + extra_gradient

        return nr_change

DEFAULT_SOLVER_ORDER = 1
def inverse_coordinate_solve(specs, target_internals, initial_cartesians,
                             masses=None,
                             remove_translation_rotation=True,
                             order=None,
                             solver_order=None,
                             tol=1e-3, max_iterations=15,
                             max_displacement=.5,
                             gradient_function=None,
                             gradient_scaling=.1,
                             # method='quasi-newton',
                             method='gradient-descent',
                             optimizer_parameters=None,
                             line_search=False,
                             damping_parameter=None,
                             damping_exponent=None,
                             restart_interval=None,
                             raise_on_failure=False,
                             return_internals=True,
                             return_expansions=True,
                             base_transformation=None,
                             reference_internals=None,
                             fixed_atoms=None,
                             fixed_coords=None,
                             angle_ordering='ijk'):
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
    from . import Optimization as opt

    if method == 'quasi-newton':
        if optimizer_parameters is None: optimizer_parameters = {}
        optimizer_parameters['initial_beta'] = optimizer_parameters.get('initial_beta', 70)

    if order is None:
        order = DEFAULT_SOLVER_ORDER
    if solver_order is None:
        solver_order = order
    if not misc.is_numeric(solver_order):
        solver_order = max(solver_order)

    if callable(specs):
        conversion = specs
    else:
        conversion = internal_conversion_function(specs,
                                                  angle_ordering=angle_ordering,
                                                  base_transformation=base_transformation,
                                                  reference_internals=reference_internals
                                                  )
    target_internals = np.asanyarray(target_internals)
    initial_cartesians = np.asanyarray(initial_cartesians)

    base_shape = target_internals.shape[:-1]
    smol = len(base_shape) == 0
    if smol:
        target_internals = target_internals[np.newaxis]
        initial_cartesians = initial_cartesians[np.newaxis]
        base_shape = (1,)
    if initial_cartesians.ndim == 2:
        coords = np.expand_dims(initial_cartesians, list(range(len(base_shape))))
        coords = np.broadcast_to(coords, base_shape + coords.shape[-2:]).copy()
    else:
        coords = initial_cartesians.copy()
    coords = coords.reshape((-1,) + coords.shape[-2:])
    init_coords = coords
    target_internals = target_internals.reshape((-1,) + target_internals.shape[-1:])

    caller = _inverse_coordinate_conversion_caller(
        conversion,
        target_internals,
        remove_translation_rotation=remove_translation_rotation,
        masses=masses,
        gradient_function=gradient_function,
        gradient_scaling=gradient_scaling,
        fixed_atoms=fixed_atoms,
        fixed_coords=fixed_coords
    )

    coords, converged, (errors, its) = opt.iterative_step_minimize(
        coords.reshape(coords.shape[:1] + (-1,)),
        opt.get_step_finder(
            caller.func,
            method=method,
            jacobian=caller.jacobian,
            damping_parameter=damping_parameter,
            damping_exponent=damping_exponent,
            restart_interval=restart_interval,
            line_search=line_search,
            **({} if optimizer_parameters is None else optimizer_parameters)
        ),
        tol=tol,
        max_displacement=max_displacement,
        max_iterations=max_iterations,
        prevent_oscillations=True
        # termination_function=caller.terminate
    )

    coords = coords.reshape(coords.shape[:1] + (-1, 3))
    opt_internals = conversion(
        coords,
        order=0 if not return_expansions else order
    )
    if not converged:
        init_internals = conversion(
            init_coords,
            order=0 if not return_expansions else order
        )[0]
        if raise_on_failure:
            raise ValueError(
                f"failed to find coordinates after {max_iterations} iterations"
                f"\ntarget:{target_internals}\ninitial:{init_internals}"
                f"\nresidual:{target_internals - opt_internals[0]}"
                f"\n1-norm error: {errors}"
                f"\n1-norm error: {errors}"
                f"\nmax deviation error: {np.max(abs(target_internals - opt_internals[0]))}"
            )
        # else:
        #     print(
        #         f"failed to find coordinates after {max_iterations} iterations"
        #         f"\ntarget:{target_internals}\ninitial:{init_internals}"
        #         f"\nresidual:{target_internals - opt_internals[0]}"
        #         f"\n1-norm error: {errors}"
        #         f"\nmax deviation error: {np.max(abs(target_internals - opt_internals[0]))}"
        #     )
    if return_expansions:
        expansion = opt_internals[1:]
        if remove_translation_rotation:
            opt_expansions = inverse_internal_coordinate_tensors(expansion, coords, masses, order)
        else:
            opt_expansions = td.inverse_transformation(expansion, order=order, allow_pseudoinverse=True)
    else:
        opt_expansions = None

    coords = coords.reshape(base_shape + coords.shape[-2:])
    errors = errors.reshape(base_shape)
    if opt_expansions is not None:
        opt_expansions = [
            o.reshape(base_shape + o.shape[1:]) if isinstance(o, np.ndarray) else o
            for o in opt_expansions
        ]
    opt_internals = [o.reshape(base_shape + o.shape[1:]) for o in opt_internals]
    if smol:
        coords = coords[0]
        errors = errors[0]
        opt_internals = [o[0] for o in opt_internals]
        if opt_expansions is not None:
            opt_expansions = [
                o[0] if isinstance(o, np.ndarray) else o
                for o in opt_expansions
            ]


    if return_expansions:
        tf = [coords] + opt_expansions
    else:
        tf = coords
    if return_internals:
        return (tf, errors), opt_internals
    else:
        return tf, errors

def coordinate_projection_data(basis_mat, fixed_mat, inds, nonzero_cutoff=1e-8,
                               masses=None, coords=None,
                               project_transrot=False):
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
    from .CoordinateFrames import translation_rotation_projector

    if project_transrot and coords is not None:
        sub_projector, sub_tr_modes = translation_rotation_projector(
            coords[..., inds, :],
            masses=(
                [masses[i] for i in inds]
                    if masses is not None else
                masses
            ),
            mass_weighted=False,
            return_modes=True
        )
        cs = coords.shape[-1]
        ncoord = coords.shape[-2]*coords.shape[-1]
        projector = np.zeros(coords.shape[:-2] + (ncoord, ncoord))
        full_idx = sum(( tuple(i*3+j for j in range(cs)) for i in inds ), ())
        proj_sel = (...,) + np.ix_(full_idx, full_idx)
        projector[proj_sel] = sub_projector
        tr_modes = np.zeros(coords.shape[:-2] + (ncoord, sub_tr_modes.shape[-1]))
        tr_modes[..., full_idx, :] = sub_tr_modes
    else:
        projector, tr_modes = None, None
    if basis_mat is not None:
        if projector is not None:
            #TODO: handle broadcasting
            basis_mat = projector @ basis_mat
        nats = basis_mat.shape[-2] // 3
        basis_mat = find_basis(basis_mat, nonzero_cutoff=nonzero_cutoff)
        mat = np.zeros(basis_mat.shape[:-2] + (nats, 3, nats, 3))
    else:
        if projector is not None:
            #     #TODO: handle broadcasting
            #     fixed_mat = projector @ fixed_mat
            fixed_mat = np.concatenate([tr_modes, fixed_mat], axis=-1)
        nats = fixed_mat.shape[-2] // 3
        fixed_mat = find_basis(fixed_mat, nonzero_cutoff=nonzero_cutoff)
        mat = np.zeros(fixed_mat.shape[:-2] + (nats, 3, nats, 3))
    for x in range(3):
        for i in inds:
            mat[..., i, x, i, x] = 1
    mat = np.reshape(mat, mat.shape[:-4] + (nats*3, nats*3))

    if basis_mat is not None:
        return basis_mat, find_basis(mat - projection_matrix(basis_mat, orthonormal=True)), mat
    else:
        return find_basis(mat - projection_matrix(fixed_mat, orthonormal=True)), fixed_mat, mat

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
    coords = np.asanyarray(coords)
    mat = np.zeros(coords.shape + (3,))
    for x in range(3):
        mat[..., i, x, x] = 1
        mat[..., j, x, x] = -1

    mat = mat.reshape(mat.shape[:-3] + (-1, 3))
    return mat

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
    basis_mat = dist_basis_mat(coords, i, j)
    return coordinate_projection_data(basis_mat, None, (i,j),
                                      coords=coords,
                                      **opts
                                      )

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
    coords = np.asanyarray(coords)
    mat = np.zeros(coords.shape + (7,))
    for x in range(3):
        mat[..., i, x, x] = 1
        mat[..., j, x, x] = 1
        mat[..., k, x, x] = 1
    v1 = coords[..., i, :] - coords[..., j, :]
    mat[..., i, :, 3] = v1
    mat[..., j, :, 4] = -v1
    mat[..., k, :, 4] = -v1
    v2 = coords[..., k, :] - coords[..., j, :]
    mat[..., k, :, 5] = v2
    mat[..., j, :, 6] = -v2
    mat[..., i, :, 6] = -v2

    mat = mat.reshape(mat.shape[:-3] + (-1, 7))
    return mat

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
    if angle_ordering == 'jik':
        i,j,k = j,i,k
    fixed_mat = fixed_angle_basis(coords, i, j, k)
    return coordinate_projection_data(None, fixed_mat, (i,j,k),
                                      coords=coords,
                                      **opts
                                      )

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
    coords = np.asanyarray(coords)
    mat = np.zeros(coords.shape + (9,))
    for x in range(3):
        mat[..., i, x, x] = 1
        mat[..., j, x, x] = 1
        mat[..., k, x, x] = 1
        mat[..., l, x, x] = 1
    # basis for plane 1
    v1 = coords[..., i, :] - coords[..., j, :]
    v2 = coords[..., j, :] - coords[..., k, :]
    mat[..., i, :, 3] = v1
    mat[..., i, :, 4] = v2
    mat[..., j, :, 5] = v2
    # basis for plane 2
    v3 = coords[..., l, :] - coords[..., k, :]
    mat[..., l, :, 6] = v2
    mat[..., l, :, 7] = v3
    mat[..., k, :, 8] = v2

    mat = mat.reshape(mat.shape[:-3] + (-1, 9))
    return mat

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
    fixed_mat = fixed_dihed_basis(coords, i, j, k, l)
    return coordinate_projection_data(None, fixed_mat, (i,j,k,l),
                                      coords=coords,
                                      **opts
                                      )

basis_coord_type_map = {
    'dist':dist_basis,
    'bend':angle_basis,
    'dihed':dihed_basis,
}
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
    return internal_conversion_specs(
        specs,
        angle_ordering=angle_ordering,
        coord_type_dispatch=basis_coord_type_map,
        **opts
    )
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
    base_specs = internal_basis_specs(specs, **opts)
    bases = []
    ortos = []
    subprojs = []
    for f, idx, subopts in base_specs:
        basis, orthog, subproj = f(coords, *idx, **subopts)
        bases.append(basis)
        ortos.append(orthog)
        subprojs.append(subproj)
    return bases, ortos, subprojs


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
    if misc.is_numeric_array_like(internals_by_cartesians):
        internals_by_cartesians = np.asanyarray(internals_by_cartesians)
        if internals_by_cartesians.ndim == 2:
            internals_by_cartesians = [internals_by_cartesians]
    transformation = np.asanyarray(internals_by_cartesians[0])
    if masses is not None:
        g12_base = np.diag(np.repeat(1/np.sqrt(masses), 3))
        transformation = np.moveaxis(
            np.tensordot(transformation, g12_base, axes=[-2, 0]),
            -1, -2
        )
    return np.moveaxis(transformation, -1, -2) @ transformation

def delocalized_internal_coordinate_transformation(
        internals_by_cartesians,
        untransformed_coordinates=None,
        masses=None,
        relocalize=False
):
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
    if misc.is_numeric_array_like(internals_by_cartesians):
        internals_by_cartesians = [internals_by_cartesians]
    conv = np.asanyarray(internals_by_cartesians[0])
    if masses is not None:
        g12_base = np.diag(np.repeat(1/np.sqrt(masses), 3))
        conv = np.moveaxis(
            np.tensordot(conv, g12_base, axes=[-2, 0]),
            -1, -2
        )

    if untransformed_coordinates is not None:
        transformed_coords = np.setdiff1d(np.arange(conv.shape[-1]), untransformed_coordinates)
        ut_conv = conv[..., untransformed_coordinates]
        conv = conv[..., transformed_coords]

        # project out contributions along untransformed coordinates to ensure
        # dimension of space remains unchanged
        ut_conv_norm = vec_normalize(np.moveaxis(ut_conv, -1, -2))
        proj = np.moveaxis(ut_conv_norm, -1, -2) @ ut_conv_norm
        proj = identity_tensors(proj.shape[:-2], proj.shape[-1]) - proj

        conv = np.concatenate([ut_conv, proj @ conv], axis=-1)

    G_internal = np.moveaxis(conv, -1, -2) @ conv
    redund_vals, redund_tf = np.linalg.eigh(G_internal)
    redund_pos = np.where(np.abs(redund_vals) > 1e-10)
    if redund_vals.ndim > 1:
        redund_tf = setops.take_where_groups(redund_tf, redund_pos)
    else:
        redund_tf = redund_tf[:, redund_pos[0]]
    if isinstance(redund_tf, np.ndarray):
        redund_tf = np.flip(redund_tf, axis=-1)
    else:
        redund_tf = [
            np.flip(tf, axis=-1)
            for tf in redund_tf
        ]

    if relocalize:
        if untransformed_coordinates is not None:
            perm = np.concatenate([untransformed_coordinates,
                                   np.delete(np.arange(redund_tf.shape[-2]), untransformed_coordinates)
                                   ])
            perm = np.argsort(perm)
            if isinstance(redund_tf, np.ndarray):
                redund_tf = redund_tf[..., perm, :]
            else:
                redund_tf = [
                    redund_tf[..., perm, :]
                    for tf in redund_tf
                ]


    return redund_tf

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
    n = redund_tf.shape[-1]
    if untransformed_coordinates is None:
        ndim = redund_tf.ndim - 2
        eye = identity_tensors(redund_tf.shape[:-2], n)
        target = np.pad(eye, ([[0, 0]] * ndim) + [[0, redund_tf.shape[-2] - n], [0, 0]])
    else:
        untransformed_coordinates = np.asanyarray(untransformed_coordinates)
        coords = np.concatenate([
            untransformed_coordinates,
            np.delete(np.arange(redund_tf.shape[-2]), untransformed_coordinates)
        ])[:n]
        target = np.moveaxis(np.zeros(redund_tf.shape), -1, -2)
        idx = setops.vector_ix(target.shape[:-1], coords[:, np.newaxis])
        target[idx] = 1
        target = np.moveaxis(target, -1, -2)
    loc = np.linalg.lstsq(redund_tf, target, rcond=None)
    U, s, V = np.linalg.svd(loc[0])
    R = U @ V
    return redund_tf @ R

def transform_cartesian_derivatives(
        derivs,
        tfs,
        axes=None
):
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
    if axes is None:
        axes = -1
    if misc.is_numeric(axes):
        axes = [-1, -2]
    derivs = [
        np.asanyarray(d) if not misc.is_numeric(d) else d
        for d in derivs
    ]

    tfs = np.asanyarray(tfs)
    d_ax, t_ax = axes
    if d_ax < 0:
        d_ax = derivs[0].ndim + d_ax
    if tfs.ndim > 2:
        shared = d_ax
    else:
        shared = None

    new_derivs = []
    for i,d in enumerate(derivs):
        if not misc.is_numeric(d):
            for j in range(i+1):
                d_shape = d.shape
                d = d.reshape(
                    d.shape[:d_ax+j] + (d.shape[d_ax+j]//3, 3) + d.shape[d_ax+j+1:]
                )
                if shared is not None:
                    d = vec_tensordot(d, tfs, axes=[d_ax+j+1, tfs], shared=shared)
                else:
                    d = np.tensordot(d, tfs, axes=[d_ax + j + 1, tfs])
                d = np.moveaxis(d, -1, d_ax + j + 1).reshape(d_shape)
            new_derivs.append(d)

    return new_derivs

__all__ = [
    "center_of_mass",
    "inertia_tensors",
    "moments_of_inertia",
    "inertial_frame_derivatives",
    "translation_rotation_eigenvectors",
    "translation_rotation_projector",
    "remove_translation_rotations",
    "translation_rotation_invariant_transformation",
    "eckart_embedding",
    "rmsd_minimizing_transformation"
]

import itertools

import numpy as np
from . import VectorOps as vec_ops
from . import TensorDerivatives as td_ops
from . import SetOps as set_ops
from . import Misc as misc
from . import TransformationMatrices as tf_mats

def center_of_mass(coords, masses=None):
    """Gets the center of mass for the coordinates

    :param coords:
    :type coords: CoordinateSet
    :param masses:
    :type masses:
    :return:
    :rtype:
    """

    if masses is None:
        masses = np.ones(coords.shape[-2])

    masses = masses.copy()
    masses[masses < 0] = 0

    return np.tensordot(masses / np.sum(masses), coords, axes=[0, -2])

def inertia_tensors(coords, masses=None):
    """
    Computes the moment of intertia tensors for the walkers with coordinates coords (assumes all have the same masses)

    :param coords:
    :type coords: CoordinateSet
    :param masses:
    :type masses: np.ndarray
    :return:
    :rtype:
    """

    if masses is None:
        masses = np.ones(coords.shape[-2])

    com = center_of_mass(coords, masses)
    coords = coords - com[..., np.newaxis, :]

    real_spots = masses > 0 # allow for dropping out dummy atoms
    coords = coords[..., real_spots, :]
    masses = masses[real_spots]

    d = np.zeros(coords.shape[:-1] + (3, 3), dtype=float)
    diag = vec_ops.vec_dots(coords, coords)
    d[..., (0, 1, 2), (0, 1, 2)] = diag[..., np.newaxis]
    # o = np.array([[np.outer(a, a) for a in r] for r in coords])
    o = vec_ops.vec_outer(coords, coords, axes=[-1, -1])
    tens = np.tensordot(masses, d - o, axes=[0, -3])

    return tens

def inertial_frame_derivatives(coords, masses=None, sel=None):
    if masses is None:
        masses = np.ones(coords.shape[-2])

    masses = np.asanyarray(masses)
    coords = np.asanyarray(coords)
    real_pos = masses > 0
    if sel is not None:
        real_pos = np.intersect1d(sel, real_pos)

    smol = coords.ndim == 2
    if smol:
        coords = coords[np.newaxis]
    base_shape = coords.shape[:-2]
    coords = coords.reshape((-1,) + coords.shape[-2:])
    if masses.ndim == 1:
        masses = masses[np.newaxis]
    else:
        masses = np.reshape(masses, (-1, masses.shape[-1]))

    masses = masses[..., real_pos]
    coords = coords[..., real_pos, :]

    masses = np.sqrt(masses)
    carts = masses[..., :, np.newaxis] * coords  # mass-weighted Cartesian coordinates

    ### compute basic inertia tensor derivatives
    # first derivs are computed as a full (nAt, 3, I_rows (3), I_cols (3)) tensor
    # and then reshaped to (nAt * 3, I_rows, I_cols)
    eyeXeye = np.eye(9).reshape(3, 3, 3, 3).transpose((2, 0, 1, 3))
    I0Y_1 = np.tensordot(carts, eyeXeye, axes=[2, 0])

    nAt = carts.shape[1]
    nY = nAt * 3
    I0Y_21 = (
            np.reshape(np.eye(3), (9,))[np.newaxis, :, np.newaxis]
            * carts[:, :, np.newaxis, :]
    )  # a flavor of outer product
    I0Y_21 = I0Y_21.reshape((-1, nAt, 3, 3, 3))
    I0Y_2 = (I0Y_21 + I0Y_21.transpose((0, 1, 2, 4, 3)))
    I0Y = 2 * I0Y_1 - I0Y_2
    I0Y = I0Y.reshape(base_shape + (nY, 3, 3))

    # second derivatives are 100% independent of coorinates
    # only the diagonal blocks are non-zero, so we compute that block
    # and then tile appropriately
    keyXey = np.eye(9).reshape(3, 3, 3, 3)
    I0YY_nn = 2 * eyeXeye - (keyXey + keyXey.transpose((0, 1, 3, 2)))
    I0YY = np.zeros((nAt, 3, nAt, 3, 3, 3))
    for n in range(nAt):
        I0YY[n, :, n, :, :, :] = I0YY_nn
    I0YY = I0YY.reshape((nY, nY, 3, 3))
    I0YY = np.broadcast_to(I0YY[np.newaxis, :, :, :, :], (carts.shape[0],) + I0YY.shape)
    I0YY = np.reshape(I0YY, base_shape + (nY, nY, 3, 3))

    if smol:
        I0Y = I0Y[0]
        I0YY = I0YY[0]

    return [I0Y, I0YY]

def moments_of_inertia(coords, masses=None):
    """
    Computes the moment of inertia tensor for the walkers with coordinates coords (assumes all have the same masses)

    :param coords:
    :type coords: CoordinateSet
    :param masses:
    :type masses: np.ndarray
    :return:
    :rtype:
    """

    if coords.ndim == 1:
        raise ValueError("can't get moment of inertia for single point (?)")
    elif coords.ndim == 2:
        multiconfig = False
        coords = coords[np.newaxis]
        extra_shape = None
    else:
        multiconfig = True
        extra_shape = coords.shape[:-2]
        coords = coords.reshape((np.prod(extra_shape),) + coords.shape[-2:])


    if masses is None:
        masses = np.ones(coords.shape[-2])

    massy_doop = inertia_tensors(coords, masses)
    moms, axes = np.linalg.eigh(massy_doop)
    # a = axes[..., :, 0]
    # c = axes[..., :, 2]
    # b = nput.vec_crosses(a, c)  # force right-handedness to avoid inversions
    # axes[..., :, 1] = b
    a = axes[..., :, 0]
    b = axes[..., :, 1]
    c = vec_ops.vec_crosses(b, a)  # force right-handedness to avoid inversions
    axes[..., :, 2] = c
    dets = np.linalg.det(axes) # ensure we have true rotation matrices to avoid inversions
    axes[..., :, 2] /= dets[..., np.newaxis]

    if multiconfig:
        moms = moms.reshape(extra_shape + (3,))
        axes = axes.reshape(extra_shape + (3, 3))
    else:
        moms = moms[0]
        axes = axes[0]
    return moms, axes

def translation_rotation_eigenvectors(coords, masses=None, mass_weighted=True):
    """
    Returns the eigenvectors corresponding to translations and rotations
    in the system

    :param coords:
    :type coords:
    :param masses:
    :type masses:
    :return:
    :rtype:
    """


    if masses is None:
        masses = np.ones(coords.shape[-2])

    n = len(masses)
    # explicitly put masses in m_e from AMU
    # masses = UnitsData.convert("AtomicMassUnits", "AtomicUnitOfMass") * masses
    mT = np.sqrt(np.sum(masses))
    mvec = np.sqrt(masses)

    # no_derivs = order is None
    # if no_derivs:
    #     order = 0

    smol = coords.ndim == 2
    if smol:
        coords = coords[np.newaxis]
    # base_shape = None
    # if coords.ndim > 3:
    base_shape = coords.shape[:-2]
    coords = coords.reshape((-1,) + coords.shape[-2:])

    M = np.kron(mvec / mT, np.eye(3)).T  # translation eigenvectors
    mom_rot, ax_rot = moments_of_inertia(coords, masses)
    # if order > 0:
    #     base_tensor = StructuralProperties.get_prop_inertia_tensors(coords, masses)
    #     mom_expansion = StructuralProperties.get_prop_inertial_frame_derivatives(coords, masses)
    #     inertia_expansion = [base_tensor] + mom_expansion
    #     sqrt_expansion = nput.matsqrt_deriv(inertia_expansion, order)
    #     inv_rot_expansion = nput.matinv_deriv(sqrt_expansion, order=order)
    #     inv_rot_2 = inv_rot_expansion[0]
    # else:
    inv_mom_2 = vec_ops.vec_tensordiag(1 / np.sqrt(mom_rot))
    inv_rot_2 = vec_ops.vec_tensordot(
        ax_rot,
        vec_ops.vec_tensordot(
            ax_rot,
            inv_mom_2,
            shared=1,
            axes=[-1, -1]
        ),
        shared=1,
        axes=[-1, -1]
    )
    # inv_rot_expansion = [inv_rot_2]
    com = center_of_mass(coords, masses)
    com = np.expand_dims(com, 1) # ???
    shift_crds = mvec[np.newaxis, :, np.newaxis] * (coords - com[: np.newaxis, :])
    # if order > 0:
    #     # could be more efficient but oh well...
    #     e = np.broadcast_to(nput.levi_cevita3[np.newaxis], (shift_crds.shape[0], 3, 3, 3))
    #     n = shift_crds.shape[-2]
    #     shift_crd_deriv = np.broadcast_to(
    #         np.eye(3*n).reshape(3*n, n, 3)[np.newaxis],
    #         (shift_crds.shape[0], 3*n, n, 3)
    #     )
    #     shift_crd_expansion = [shift_crds]
    #     R_expansion = nput.tensorops_deriv(
    #         shift_crd_expansion,
    #             [-1, -1],
    #         [e],
    #             [-1, -2],
    #         inv_rot_expansion,
    #         order=order,
    #         shared=1
    #     )
    #     with np.printoptions(linewidth=1e8):
    #         print()
    #         # print(R_expansion[0][0])
    #         print(R_expansion[1][0].reshape(3*n, 3*n, 3)[:, :, 0])
    #         print(
    #             np.moveaxis(
    #                 np.tensordot(
    #                     np.tensordot(shift_crds[0], e[0], axes=[-1, 1]),
    #                     inv_rot_expansion[1][0],
    #                     axes=[1, -1]
    #                 ),
    #                 -2,
    #                 0
    #             ).reshape(15, 15, 3)[:, :, 0]
    #         )
    #     raise Exception(...)
    #     R_expansion = [
    #         r.reshape(r.shape[:-3] + (r.shape[-3]*r.shape[-2], r.shape[-1]))
    #         for r in R_expansion
    #     ]
    #     R = R_expansion[0]
    #     raise Exception(R_expansion[1][0] - np.moveaxis(R_expansion[1][0], 1, 0))
    #
    # else:
    cos_rot = td_ops.levi_cevita_dot(3, inv_rot_2, axes=[0, -1], shared=1) # kx3bx3cx3j
    R = vec_ops.vec_tensordot(
        shift_crds, cos_rot,
        shared=1,
        axes=[-1, 1]
    ).reshape((coords.shape[0], 3 * n, 3))  # rotations
    # raise Exception(R)

    freqs = np.concatenate([
        np.broadcast_to([[1e-14, 1e-14, 1e-14]], mom_rot.shape),
        (1 / (2 * mom_rot))
        # this isn't right, I'm totally aware, but I think the frequency is supposed to be zero anyway and this
        # will be tiny
    ], axis=-1)
    M = np.broadcast_to(M[np.newaxis], R.shape)
    eigs = np.concatenate([M, R], axis=2)

    if not mass_weighted:
        W = np.diag(np.repeat(1/np.sqrt(masses), 3))
        eigs = np.moveaxis(np.tensordot(eigs, W, axes=[-2, 0]), -1, -2)

    if smol:
        eigs = eigs[0]
        freqs = freqs[0]
    else:
        eigs = eigs.reshape(base_shape + eigs.shape[1:])
        freqs = freqs.reshape(base_shape + freqs.shape[1:])

    return freqs, eigs

def translation_rotation_projector(coords, masses=None, mass_weighted=False, return_modes=False):
    if masses is None:
        masses = np.ones(coords.shape[-2])
    _, tr_modes = translation_rotation_eigenvectors(coords, masses, mass_weighted=mass_weighted)
    shared = tr_modes.ndim - 2
    eye = vec_ops.identity_tensors(tr_modes.shape[:-2], tr_modes.shape[-2])
    projector = eye - vec_ops.vec_tensordot(tr_modes, tr_modes, axes=[-1, -1], shared=shared)

    if return_modes:
        return projector, tr_modes
    else:
        return projector


def remove_translation_rotations(expansion, coords, masses=None, mass_weighted=False):
    projector = translation_rotation_projector(coords, masses=masses, mass_weighted=mass_weighted)
    shared = projector.ndim - 2

    proj_expansion = []
    for n,d in enumerate(expansion):
        for ax in range(n+1):
            d = vec_ops.vec_tensordot(projector, d, axes=[-1, shared+ax], shared=shared)
        proj_expansion.append(d)

    return proj_expansion

def translation_rotation_invariant_transformation(
        coords, masses=None,
        mass_weighted=True,
        strip_embedding=True
):

    if masses is None:
        masses = np.ones(coords.shape[-2])

    A, L_tr = translation_rotation_projector(coords, masses, mass_weighted=True, return_modes=True)
    base_shape = A.shape[:-2]
    A = A.reshape((-1,) + A.shape[-2:])
    L_tr = L_tr.reshape((-1,) + L_tr.shape[-2:])
    evals, tf = np.linalg.eigh(A)
    # zero_pos = np.where(np.abs(evals) < 1e-4) # the rest should be 1
    # raise Exception(
    #     evals.shape,
    #     zero_pos,
    #     # set_ops.vector_ix(tf.shape, zero_pos)
    # )

    # zero_pos = zero_pos[:-1] + (slice(None),) + zero_pos[-1:]
    # raise Exception(zero_pos, tf.shape, tf[zero_pos].shape, L_tr.shape)
    # tf[zero_pos] = np.moveaxis(L_tr)
    tf[:, :, :6] = L_tr
    if strip_embedding:
        # nzpos = np.where(np.abs(evals) > 1e-4) # the rest should be 1
        # nzpos = nzpos[:-1] + (slice(None),) + nzpos[-1:]
        tf = tf[:, :, 6:]
    else:
        tf[:, :, :6] = L_tr

    inv = np.moveaxis(tf, -1, -2)
    if not mass_weighted:
        W = np.diag(np.repeat(np.sqrt(masses), 3))
        tf = np.moveaxis(
            np.tensordot(W, tf, axes=[0, 1]),
            1, 0
        )

        W = np.diag(np.repeat(1/np.sqrt(masses), 3))
        inv = np.tensordot(inv, W, axes=[2, 0])

    tf = tf.reshape(base_shape + tf.shape[-2:])
    inv = inv.reshape(base_shape + inv.shape[-2:])

    return tf, inv

def principle_axis_embedded_coords(coords, masses=None):
    """
    Returns coordinate embedded in the principle axis frame

    :param coords:
    :type coords:
    :param masses:
    :type masses:
    :return:
    :rtype:
    """
    com = center_of_mass(coords, masses)
    # crds_ = coords
    coords = coords - com[..., np.newaxis, :]
    moms, pax_axes = moments_of_inertia(coords, masses)
    # pax_axes = np.swapaxes(pax_axes, -2, -1)
    coords = np.matmul(coords, pax_axes)

    return coords, com, pax_axes


planar_ref_tolerance=1e-6
def _eckart_embedding(ref, coords,
                     masses=None,
                     sel=None,
                     in_paf=False,
                     planar_ref_tolerance=None,
                     proper_rotation=False
                     ):
    """
    Generates the Eckart rotation that will align ref and coords, assuming initially that `ref` and `coords` are
    in the principle axis frame

    :param masses:
    :type masses:
    :param ref:
    :type ref:
    :param coords:
    :type coords: np.ndarray
    :return:
    :rtype:
    """
    if masses is None:
        masses = np.ones(coords.shape[-2])

    if coords.ndim == 2:
        coords = np.broadcast_to(coords, (1,) + coords.shape)

    if planar_ref_tolerance is None:
        planar_ref_tolerance = planar_ref_tolerance

    if not in_paf:
        coords, com, pax_axes = principle_axis_embedded_coords(coords, masses)
        ref, ref_com, ref_axes = principle_axis_embedded_coords(ref, masses)
        # raise ValueError(ref)
    else:
        com = pax_axes = None
        ref_com = ref_axes = None

    og_coords = coords
    if sel is not None:
        coords = coords[..., sel, :]
        masses = masses[sel]
        ref = ref[..., sel, :]

    real_pos = masses > 0
    # print(real_pos)
    # og_coords = coords
    coords = coords[..., real_pos, :]
    masses = masses[real_pos,]
    og_ref = ref
    ref = ref[..., real_pos, :]

    if ref.ndim == 2:
        ref = ref[np.newaxis]
    if ref.shape[0] > 1 and ref.shape[0] < coords.shape[0]:  # TODO: make less hacky
        # need to make them broadcast together and we assume
        # we have an extra stack of coords
        n_sys = coords.shape[0]
        ref = np.reshape(
            np.broadcast_to(
                ref[np.newaxis],
                (n_sys // ref.shape[0],) + ref.shape
            ),
            (n_sys,) + ref.shape[1:]
        )
        ref_axes = np.reshape(
            np.broadcast_to(
                ref_axes[np.newaxis],
                (n_sys // ref_axes.shape[0],) + ref_axes.shape
            ),
            (n_sys,) + ref_axes.shape[1:]
        )
        ref_com = np.reshape(
            np.broadcast_to(
                ref_com[np.newaxis],
                (n_sys // ref_com.shape[0],) + ref_com.shape
            ),
            (n_sys,) + ref_com.shape[1:]
        )

    # needs to be updated for the multiple reference case?
    # TODO: make sure that we broadcast this correctly to check if all or
    #       none of the reference structures are planar
    planar_ref = np.allclose(ref[0][:, 2], 0., atol=planar_ref_tolerance)

    if not planar_ref:
        # generate pair-wise product matrix
        A = np.tensordot(
            masses / np.sum(masses),
            ref[:, :, :, np.newaxis] * coords[:, :, np.newaxis, :],
            axes=[0, 1]
        )
        # take SVD of this
        U, S, V = np.linalg.svd(A)
        rot = np.matmul(U, V)
    else:
        # generate pair-wise product matrix but only in 2D
        F = ref[:, :, :2, np.newaxis] * coords[:, :, np.newaxis, :2]
        A = np.tensordot(masses / np.sum(masses), F, axes=[0, 1])
        U, S, V = np.linalg.svd(A)
        rot = np.broadcast_to(np.eye(3, dtype=float), (len(coords), 3, 3)).copy()
        rot[..., :2, :2] = np.matmul(U, V)

    if proper_rotation:
        a = rot[..., :, 0]
        b = rot[..., :, 1]
        c = vec_ops.vec_crosses(a, b, normalize=True)  # force right-handedness because we can
        rot[..., :, 2] = c  # ensure we have true rotation matrices
        dets = np.linalg.det(rot)
        rot[..., :, 2] /= dets[..., np.newaxis]  # ensure we have true rotation matrices

    # dets = np.linalg.det(rot)
    # raise ValueError(dets)

    return rot, (og_ref, ref_com, ref_axes), (og_coords, com, pax_axes)

def eckart_embedding(ref, coords,
                     masses=None,
                     sel=None,
                     in_paf=False,
                     planar_ref_tolerance=None,
                     proper_rotation=False,
                     permutable_groups=None):
    if permutable_groups is None:
        return _eckart_embedding(
            ref, coords,
            masses=masses,
            sel=sel,
            in_paf=in_paf,
            planar_ref_tolerance=planar_ref_tolerance,
            proper_rotation=proper_rotation
        )
    else:
        if misc.is_numeric(permutable_groups[0]):
            permutable_groups = permutable_groups[0]

        if masses is None:
            masses = np.ones(coords.shape[-2])
        masses = np.asanyarray(masses)

        # permutes solely based on the first element in coords
        perm = np.arange(coords.shape[-2])
        for g in permutable_groups:
            rotation_angles = []
            r = ref[..., g, :]
            m = masses[g,]
            for p in itertools.permutations(g):
                c = coords[..., g, :]
                rot = _eckart_embedding(r, c, masses=m, in_paf=False)
                angle,axis = tf_mats.extract_rotation_angle_axis(rot)

rmsd_minimizing_transformation = eckart_embedding
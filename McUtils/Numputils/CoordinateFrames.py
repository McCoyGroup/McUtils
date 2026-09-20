__all__ = [
    "center_of_mass",
    "inertia_tensors",
    "moments_of_inertia",
    "moments_of_inertia_expansion",
    "inertial_frame_derivatives",
    "frame_displacement_projector",
    "translation_rotation_eigenvectors",
    "translation_rotation_projector",
    "remove_translation_rotations",
    "translation_rotation_invariant_transformation",
    "eckart_embedding",
    "rmsd_minimizing_transformation",
    "eckart_permutation",
    "eckart_rmsd",
    "incremental_eckart_rmsd"
]

import itertools, collections

import numpy as np, scipy.optimize as opt
from . import VectorOps as vec_ops
from . import PermutationOps as perm_ops
from . import TensorDerivatives as td
# from . import SetOps as set_ops
# from . import Misc as misc
# from . import TransformationMatrices as tf_mats

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
    masses = np.asanyarray(masses)

    masses = masses.copy()
    masses[masses < 0] = 0

    return np.tensordot(masses / np.sum(masses), coords, axes=[0, -2])

def inertia_tensors(coords, masses=None, mass_weighted=False, return_com=False):
    """
    Computes the moment of intertia tensors for the walkers with coordinates coords (assumes all have the same masses)

    :param coords:
    :type coords: CoordinateSet
    :param masses:
    :type masses: np.ndarray
    :return:
    :rtype:
    """
    if mass_weighted:
        raise ValueError("mass-weighted inertia tensor not supported yet")

    if masses is None:
        masses = np.ones(coords.shape[-2])
    masses = np.asanyarray(masses)

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

    if return_com:
        return tens, com
    else:
        return tens

def inertial_frame_derivatives(coords, masses=None, sel=None, mass_weighted=True):
    """
    **LLM Docstring**

    Compute the first and second derivatives of the moment-of-inertia tensor with
    respect to the (mass-weighted) Cartesian coordinates.

    Working in center-of-mass, mass-weighted coordinates, the first derivatives are
    assembled from the standard inertia-tensor identities and reshaped to `(3N, 3,
    3)`; the second derivatives are coordinate-independent and nonzero only on the
    diagonal atom blocks, so one block is built and tiled to `(3N, 3N, 3, 3)`. When
    `mass_weighted` is off the derivatives are un-weighted by `M^{1/2}`.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param masses: per-atom masses (defaults to unit masses)
    :type masses: np.ndarray | None
    :param sel: optional subset of atoms to include
    :type sel: Iterable[int] | None
    :param mass_weighted: whether to return mass-weighted derivatives
    :type mass_weighted: bool
    :return: `[first_derivatives, second_derivatives]` of the inertia tensor
    :rtype: list[np.ndarray]
    """
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

    com = center_of_mass(coords, masses[0])
    masses = np.sqrt(masses)
    carts = masses[..., :, np.newaxis] * (coords - com[..., np.newaxis, :])  # mass-weighted Cartesian coordinates

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

    if not mass_weighted:
        g12 = np.diag(np.repeat(masses, 3))
        I0Y = np.moveaxis(np.tensordot(I0Y, g12, axes=[-3, -1]), -1, -3)
        I0YY = np.moveaxis(np.moveaxis(
            np.tensordot(np.tensordot(I0YY, g12, axes=[-4, -1]), g12, axes=[-4, -1]),
            -1, -4
        ), -1, -4)

    if smol:
        I0Y = I0Y[0]
        I0YY = I0YY[0]

    return [I0Y, I0YY]

def moments_of_inertia(coords, masses=None, force_rotation=True, return_com=False):
    """
    Computes the moment of inertia tensor for the walkers with coordinates coords (assumes all have the same masses)

    :param coords:
    :type coords: CoordinateSet
    :param masses:
    :type masses: np.ndarray
    :return:
    :rtype:
    """

    coords = np.asanyarray(coords)
    if coords.shape[-1] != 3:
        if coords.shape[-1] % 3 != 0: raise ValueError('coordinates are not valid for Cartesians')
        coords = coords.reshape(coords.shape[:-1] + (coords.shape[-1]//3, 3))

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

    massy_doop, com = inertia_tensors(coords, masses, return_com=True)
    moms, axes = np.linalg.eigh(massy_doop)
    # a = axes[..., :, 0]
    # c = axes[..., :, 2]
    # b = nput.vec_crosses(a, c)  # force right-handedness to avoid inversions
    # axes[..., :, 1] = b
    if force_rotation:
        a = axes[..., :, 0]
        b = axes[..., :, 1]
        c = vec_ops.vec_crosses(b, a)  # force right-handedness to avoid inversions
        axes[..., :, 2] = c
        dets = np.linalg.det(axes) # ensure we have true rotation matrices to avoid inversions
        axes[..., :, 2] /= dets[..., np.newaxis]

    if multiconfig:
        moms = moms.reshape(extra_shape + (3,))
        axes = axes.reshape(extra_shape + (3, 3))
        com = com.reshape(extra_shape + (3,))
    else:
        moms = moms[0]
        axes = axes[0]
        com = com[0]

    if return_com:
        return (moms, axes), com
    else:
        return moms, axes

def moments_of_inertia_expansion(coords, masses=None, order=1, force_rotation=True, mass_weighted=True):
    """
    **LLM Docstring**

    Compute the derivative expansion of the moments of inertia (eigenvalues) and
    principal axes (eigenvectors) with respect to the Cartesian coordinates.

    The inertia tensor and its derivatives (from `inertial_frame_derivatives`) form
    an expansion that is fed, together with the base eigenvalues/eigenvectors, to
    `TensorDerivatives.mateigh_deriv`; the eigenvalue derivatives are read off the
    diagonal of the resulting tensors.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param masses: per-atom masses
    :type masses: np.ndarray | None
    :param order: maximum derivative order
    :type order: int
    :param force_rotation: force a proper-rotation (right-handed) axis convention
    :type force_rotation: bool
    :param mass_weighted: whether the expansion is mass-weighted
    :type mass_weighted: bool
    :return: `(eigenvalue_expansion, eigenvector_expansion)`
    :rtype: tuple[list, list]
    """
    inertia_base = inertia_tensors(coords, masses=masses, mass_weighted=mass_weighted)
    inertia_higher = inertial_frame_derivatives(coords, masses=masses, mass_weighted=mass_weighted)
    inertia_expansion = [inertia_base] + inertia_higher
    vals, vecs = moments_of_inertia(coords, masses, force_rotation=force_rotation)
    base_expansion = [
        [vec_ops.vec_tensordiag(vals)],
        [vecs]
    ]
    val_exp, vec_exp = td.mateigh_deriv(inertia_expansion, order, base_expansion=base_expansion)
    r, c = np.diag_indices(3)
    return [v[..., r, c] for v in val_exp], vec_exp

def translation_rotation_eigenvectors(coords,
                                      masses=None,
                                      mass_weighted=True,
                                      ref=None,
                                      ref_masses=None,
                                      axes=None,
                                      align_with_frame=True,
                                      return_values=False,
                                      return_com=False,
                                      return_rot=True,
                                      return_principle_axes=False
                                      ):
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
    coords = np.asanyarray(coords)


    if masses is None:
        masses = np.ones(coords.shape[-2])
    masses = np.asanyarray(masses)

    if ref is None:
        ref = coords
    if ref_masses is None:
        ref_masses = masses

    n = len(masses)
    # explicitly put masses in m_e from AMU
    # masses = UnitsData.convert("AtomicMassUnits", "AtomicUnitOfMass") * masses
    mT = np.sqrt(np.sum(ref_masses))
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

    values = []

    M = np.kron(mvec / mT, np.eye(3)).T  # translation eigenvectors
    principle_axes = None
    if axes is not None:
        axes = np.broadcast_to(
            np.asanyarray(axes).reshape(-1, 3, 3),
            (coords.shape[0], 3, 3)
        )
        M = np.broadcast_to(M.reshape((-1,) + M.shape), (coords.shape[0],) + M.shape)
        M = vec_ops.vec_tensordot(
            M,
            axes,
            axes=[-1, -1],
            shared=1
        )
    elif align_with_frame:
        ref = np.broadcast_to(ref.reshape((-1,) + ref.shape[-2:]), coords.shape[:1] + ref.shape[-2:])
        mom_rot, ax_rot = moments_of_inertia(ref, ref_masses)
        principle_axes = ax_rot
        M = np.broadcast_to(M.reshape((-1,) + M.shape), (coords.shape[0],) + M.shape)
        M = vec_ops.vec_tensordot(
            M,
            principle_axes,
            axes=[-1, -1],
            shared=1
        )

    if return_rot:
        if principle_axes is None:
            ref = np.broadcast_to(ref.reshape((-1,) + ref.shape[-2:]), coords.shape[:1] + ref.shape[-2:])
            mom_rot, ax_rot = moments_of_inertia(ref, ref_masses)
            principle_axes = ax_rot
        # if order > 0:
        #     base_tensor = StructuralProperties.get_prop_inertia_tensors(coords, masses)
        #     mom_expansion = StructuralProperties.get_prop_inertial_frame_derivatives(coords, masses)
        #     inertia_expansion = [base_tensor] + mom_expansion
        #     sqrt_expansion = nput.matsqrt_deriv(inertia_expansion, order)
        #     inv_rot_expansion = nput.matinv_deriv(sqrt_expansion, order=order)
        #     inv_rot_2 = inv_rot_expansion[0]
        # else:
        good_ax = np.abs(mom_rot) > 1e-8
        nonlinear = good_ax.flatten().all()
        if nonlinear:
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
        else:
            all_linear = len(good_ax)==0 or np.sum(np.abs(np.diff(good_ax, axis=0))) == 0
            if all_linear:
                good_ax = good_ax[0]
                inv_mom_2 = vec_ops.vec_tensordiag(1 / np.sqrt(mom_rot[:, good_ax,]))
                inv_rot_2 = vec_ops.vec_tensordot(
                    ax_rot[:, :, good_ax],
                    vec_ops.vec_tensordot(
                        ax_rot[:, :, good_ax],
                        inv_mom_2,
                        shared=1,
                        axes=[-1, -1]
                    ),
                    shared=1,
                    axes=[-1, -1]
                )
            else:
                inv_rot_2 = []
                for sel,moms,rot in zip(good_ax, mom_rot, ax_rot):
                    inv_mom_2 = vec_ops.vec_tensordiag(1 / np.sqrt(moms[sel,]))
                    subinv = rot[:, sel] @ inv_mom_2 @ rot[:, sel].T
                    rem = np.array([0, 1, 2])[np.logical_not(sel)]
                    subinv[:, rem] = rot.T[:, rem]
                    inv_rot_2.append(subinv)
                inv_rot_2 = np.array(inv_rot_2)

        com = center_of_mass(ref, ref_masses)
        # com = np.expand_dims(com, 1) # ???
        shift_crds = mvec[np.newaxis, :, np.newaxis] * (coords - com[:, np.newaxis, :])
        if return_values:
            values.append(np.sum(shift_crds/mT, axis=-2))
        cos_rot = perm_ops.levi_cevita_dot(3, inv_rot_2, axes=[0, -1], shared=1) # kx3bx3cx3j
        R = -vec_ops.vec_tensordot(
            shift_crds, cos_rot,
            shared=1,
            axes=[-1, 1]
        ).reshape((coords.shape[0], 3 * n, 3))  # rotations

        if return_values:
            # mT = np.sqrt(np.sum(masses))
            mvec_ref = np.sqrt(ref_masses)
            shift_ref = mvec_ref[np.newaxis, :, np.newaxis] * (ref - com[:, np.newaxis, :])
            shift_ref = shift_ref.reshape(shift_ref.shape[0], -1)
            values.append(
                -vec_ops.vec_tensordot(
                    R[:, :shift_ref.shape[-1], :],
                    shift_ref,
                    shared=1,
                    axes=[-2, -1]
                )
            )

        if axes is not None:
            axes = np.broadcast_to(
                np.asanyarray(axes).reshape(-1, 3, 3),
                (coords.shape[0], 3, 3)
            )
            R = vec_ops.vec_tensordot(R, np.moveaxis(axes, -2, -1), shared=1, axes=[-1, -1])
        elif align_with_frame:
            R = vec_ops.vec_tensordot(R, np.moveaxis(principle_axes, -2, -1), shared=1, axes=[-1, -1])

        if nonlinear:
            if return_com:
                t_freq = com
            else:
                t_freq = np.broadcast_to([[1e-14, 1e-14, 1e-14]], mom_rot.shape)
            freqs = np.concatenate([
                t_freq,
                (1 / (2 * mom_rot))
                # this isn't right, I'm totally aware, but I think the frequency is supposed to be zero anyway and this
                # will be tiny
            ], axis=-1)
            if M.ndim < R.ndim:
                M = np.broadcast_to(M[np.newaxis], R.shape)
            eigs = np.concatenate([M, R], axis=2)
        elif all_linear:
            mom_rot = mom_rot[:, good_ax]
            if return_com:
                t_freq = com
            else:
                t_freq = np.broadcast_to([[1e-14, 1e-14, 1e-14]], R.shape[:1] + (3,))
            freqs = np.concatenate([
                t_freq,
                (1 / (2 * mom_rot))
                # this isn't right, I'm totally aware, but I think the frequency is supposed to be zero anyway and this
                # will be tiny
            ], axis=-1)
            R = R[:, :, good_ax]
            if M.ndim < R.ndim:
                M = np.broadcast_to(M[np.newaxis], R.shape[:1] + M.shape)
            eigs = np.concatenate([M, R], axis=2)
        else:
            freqs = []
            eigs = []
            if return_com:
                t_freq = com
            else:
                t_freq = [1e-14, 1e-14, 1e-14]
            for sel, moms, rot in zip(good_ax, mom_rot, R):
                f = np.concatenate([t_freq, 1/(2*mom_rot[sel,])])
                r = rot[:, sel]
                freqs.append(f)
                eigs.append(np.concatenate([M, r], axis=1))
    else:
        if M.ndim == 2:
            eigs = np.broadcast_to(M[np.newaxis], coords.shape[:-2] + M.shape)
        else:
            eigs = M
        if return_com:
            com = freqs = center_of_mass(ref, ref_masses)
            if return_values:
                shift_crds = mvec[np.newaxis, :, np.newaxis] * (coords - com[:, np.newaxis, :])
                values.append(np.sum(shift_crds / mT, axis=-2))
        else:
            freqs = np.full(M.shape[:-2] + (3,), 1e-14)
            if return_values:
                com  = center_of_mass(ref, ref_masses)
                shift_crds = mvec[np.newaxis, :, np.newaxis] * (coords - com[:, np.newaxis, :])
                values.append(np.sum(shift_crds / mT, axis=-2))

    if not mass_weighted:
        W = np.diag(np.repeat(np.sqrt(masses), 3))
        eigs = np.moveaxis(np.tensordot(eigs, W, axes=[-2, 0]), -1, -2)

    if return_values:
        values = np.concatenate(values, axis=-1)
    if smol:
        eigs = eigs[0]
        freqs = freqs[0]
        principle_axes = principle_axes[0]
        if return_values:
            values = values[0]
    else:
        eigs = eigs.reshape(base_shape + eigs.shape[1:])
        freqs = freqs.reshape(base_shape + freqs.shape[1:])
        principle_axes = principle_axes.reshape(base_shape + principle_axes.shape[1:])
        if return_values:
            values = values.reshape(base_shape + values.shape[1:])

    res = (freqs, eigs)
    if return_values or return_principle_axes:
        res = (res,)
    if return_values:
        res = res + (values,)
    if return_principle_axes:
        res = res + (principle_axes,)
    return res

def frame_displacement_projector(tr_modes, masses,
                                 mass_weighted=False,
                                 orthonormal=True,
                                 pre_weighted=False,
                                 direction='forward'):
    """
    **LLM Docstring**

    Build the projector that removes a set of frame (translation/rotation) modes
    from a displacement space.

    Depending on `mass_weighted` and `pre_weighted`, the appropriate left inverse of
    the mode matrix is formed (applying or assuming the `M^{±1/2}` weighting), then
    the complementary projector `I - L Lᵀ` is assembled — orthonormally via
    `orthogonal_projection_matrix` when `orthonormal` is set, otherwise by an
    explicit contraction.

    :param tr_modes: the translation/rotation mode vectors
    :type tr_modes: np.ndarray
    :param masses: per-atom masses
    :type masses: np.ndarray
    :param mass_weighted: whether the output space should be mass-weighted
    :type mass_weighted: bool
    :param orthonormal: whether the modes are orthonormal
    :type orthonormal: bool
    :param pre_weighted: whether the modes already carry the mass weighting
    :type pre_weighted: bool
    :return: the frame-removing projector
    :rtype: np.ndarray
    """
    if not mass_weighted:
        if pre_weighted:
            g12 = np.diag(np.repeat(np.sqrt(masses), 3)) # sqrt factor already applied
            gi12 = np.diag(np.repeat(np.sqrt(1/masses), 3)) # sqrt factor already applied
            if direction != 'forward':
                g12, gi12 = gi12, g12
            inv = np.tensordot(tr_modes, g12, axes=[-2, -1])
            tr_modes = np.moveaxis(np.tensordot(tr_modes, gi12, axes=[-2, -1]), -1, -2)
        else:
            inv = np.moveaxis(tr_modes, -2, -1)
    else:
        if pre_weighted:
            inv = np.moveaxis(tr_modes, -2, -1)
        else:
            g12 = np.diag(np.repeat(np.sqrt(masses), 3)) # sqrt factor already applied
            gi12 = np.diag(np.repeat(np.sqrt(1/masses), 3)) # sqrt factor already applied
            if direction != 'forward':
                g12, gi12 = gi12, g12
            inv = np.tensordot(tr_modes, gi12, axes=[-2, -1])
            tr_modes = np.moveaxis(np.tensordot(tr_modes, g12, axes=[-2, -1]), -1, -2)
    if orthonormal:
        projector = vec_ops.orthogonal_projection_matrix(tr_modes, inverse=inv, orthonormal=True)
    else:
        shared = tr_modes.ndim - 2
        eye = vec_ops.identity_tensors(tr_modes.shape[:-2], tr_modes.shape[-2])
        projector = eye - vec_ops.vec_tensordot(tr_modes, inv, axes=[-1, -2], shared=shared)
    return projector

def translation_rotation_projector(coords, masses=None, mass_weighted=False, return_modes=False,
                                   orthonormal=False, direction='forward'
                                   ):
    """
    **LLM Docstring**

    Build the projector that removes overall translation and rotation from a
    Cartesian displacement space.

    The translation/rotation eigenvectors are obtained from
    `translation_rotation_eigenvectors` and passed to
    `frame_displacement_projector`. The mode vectors themselves can optionally be
    returned alongside the projector.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param masses: per-atom masses (defaults to unit masses)
    :type masses: np.ndarray | None
    :param mass_weighted: whether the output space should be mass-weighted
    :type mass_weighted: bool
    :param return_modes: also return the translation/rotation modes
    :type return_modes: bool
    :param orthonormal: whether to build an orthonormal projector
    :type orthonormal: bool
    :return: the projector (and the modes if `return_modes`)
    :rtype: np.ndarray | tuple
    """
    if masses is None:
        masses = np.ones(coords.shape[-2])
    _, tr_modes = translation_rotation_eigenvectors(coords, masses, mass_weighted=True)

    projector = frame_displacement_projector(
        tr_modes, masses,
        mass_weighted=mass_weighted,
        orthonormal=orthonormal,
        pre_weighted=True,
        direction=direction
    )

    if return_modes:
        return projector, tr_modes
    else:
        return projector


def remove_translation_rotations(expansion, coords, masses=None, mass_weighted=False):
    """
    **LLM Docstring**

    Apply the translation/rotation projector to every tensor in a derivative
    expansion, removing the overall translation/rotation content from each
    Cartesian axis.

    :param expansion: the derivative expansion `[value, d1, d2, ...]`
    :type expansion: list[np.ndarray]
    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param masses: per-atom masses
    :type masses: np.ndarray | None
    :param mass_weighted: whether the working space is mass-weighted
    :type mass_weighted: bool
    :return: the projected expansion
    :rtype: list[np.ndarray]
    """
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
    """
    **LLM Docstring**

    Construct the transformation (and its inverse) into the space of internal,
    translation/rotation-invariant coordinates.

    The translation/rotation projector is diagonalized; the near-zero eigenvectors
    are replaced by the exact translation/rotation modes, and the remaining
    eigenvectors span the invariant subspace (optionally stripped of the embedding
    directions). The transformation and inverse are un-mass-weighted with `M^{±1/2}`
    when `mass_weighted` is off.

    :param coords: Cartesian coordinates, shape `(..., N, 3)`
    :type coords: np.ndarray
    :param masses: per-atom masses (defaults to unit masses)
    :type masses: np.ndarray | None
    :param mass_weighted: whether to keep the transformation mass-weighted
    :type mass_weighted: bool
    :param strip_embedding: drop the translation/rotation columns from the result
    :type strip_embedding: bool
    :return: `(transformation, inverse)`
    :rtype: tuple[np.ndarray, np.ndarray]
    """

    if masses is None:
        masses = np.ones(coords.shape[-2])

    A, L_tr = translation_rotation_projector(coords, masses, mass_weighted=True, return_modes=True)
    base_shape = A.shape[:-2]
    A = A.reshape((-1,) + A.shape[-2:])
    L_tr = L_tr.reshape((-1,) + L_tr.shape[-2:])
    evals, tf = np.linalg.eigh(A)
    zero_pos = np.abs(evals) < 1e-4# the rest should be 1
    zero_counts = np.sum(zero_pos, axis=1)
    ucounts = np.min(zero_counts)

    tf[:, :, :ucounts] = L_tr
    if strip_embedding:
        # nzpos = np.where(np.abs(evals) > 1e-4) # the rest should be 1
        # nzpos = nzpos[:-1] + (slice(None),) + nzpos[-1:]
        tf = tf[:, :, ucounts:]
    else:
        tf[:, :, :ucounts] = L_tr

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

EmbeddingData = collections.namedtuple("PrincipleAxisData", ['coords', 'com', 'axes'])
EckartData = collections.namedtuple('EckartData', ['rotations', 'coordinates', 'reference_data', 'coord_data'])
def principle_axis_embedded_coords(coords, masses=None, sel=None):
    """
    Returns coordinate embedded in the principle axis frame

    :param coords:
    :type coords:
    :param masses:
    :type masses:
    :return:
    :rtype:
    """

    og_coords = coords
    if sel is not None:
        coords = coords[..., sel, :]
        masses = masses[sel,]

    real_pos = np.where(masses > 0)[0]
    # print(real_pos)
    # og_coords = coords
    coords = coords[..., real_pos, :]
    masses = masses[real_pos,]

    com = center_of_mass(coords, masses)
    # crds_ = coords
    coords = coords - com[..., np.newaxis, :]
    moms, pax_axes = moments_of_inertia(coords, masses)
    # pax_axes = np.swapaxes(pax_axes, -2, -1)
    coords = np.matmul(og_coords - com[..., np.newaxis, :], pax_axes)
    # coords = np.matmul(coords, pax_axes)

    return EmbeddingData(coords, com, pax_axes)

def _prep_eckart_data(ref, coords, masses, in_paf=False, sel=None):
    """
    **LLM Docstring**

    Prepare a reference and a set of coordinates for an Eckart embedding.

    Unless the inputs are already in the principal-axis frame (`in_paf`), both the
    coordinates and the reference are moved into their principal-axis embeddings.
    Atoms are optionally restricted to `sel`, dummy atoms (non-positive mass) are
    dropped, and the reference is broadcast to match a stacked set of coordinates.

    :param ref: the reference geometry
    :type ref: np.ndarray
    :param coords: the coordinates to embed
    :type coords: np.ndarray
    :param masses: per-atom masses (defaults to unit masses)
    :type masses: np.ndarray | None
    :param in_paf: whether the inputs are already in the principal-axis frame
    :type in_paf: bool
    :param sel: optional subset of atoms to use
    :type sel: Iterable[int] | None
    :return: `((ref, ref_com, ref_axes), (coords, com, axes), masses,
        (original_ref, original_coords))`
    :rtype: tuple
    """

    if masses is None:
        masses = np.ones(coords.shape[-2])
    masses = np.asanyarray(masses)

    if coords.ndim == 2:
        coords = np.broadcast_to(coords, (1,) + coords.shape)

    if not in_paf:
        coords, com, pax_axes = principle_axis_embedded_coords(coords, masses, sel=sel)
        ref, ref_com, ref_axes = principle_axis_embedded_coords(ref, masses, sel=sel)
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

    return (ref, ref_com, ref_axes), (coords, com, pax_axes), masses, (og_ref, og_coords)

def _eckart_embedding(ref, coords,
                      masses=None,
                      sel=None,
                      in_paf=False,
                      planar_ref_tolerance=1e-6,
                      proper_rotation=False,
                      permutable_groups=None,
                      reset_com=True,
                      transform_coordinates=True
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

    coords = np.asanyarray(coords)
    og_og_coords = coords
    ref = np.asanyarray(ref)
    og_og_ref = ref

    (ref, ref_com, ref_axes), (coords, com, pax_axes), masses, (og_ref, og_coords) = _prep_eckart_data(
        ref, coords, masses,
        sel=sel, in_paf=in_paf
    )

    # needs to be updated for the multiple reference case?
    # TODO: make sure that we broadcast this correctly to check if all or
    #       none of the reference structures are planar
    if planar_ref_tolerance is None or planar_ref_tolerance < 0:
        planar_ref = False
    else:
        planar_ref = np.allclose(ref[0][:, 2], 0., atol=planar_ref_tolerance)

    if permutable_groups is not None:
        if sel is not None:
            reindexing = {a:i for i,a in enumerate(sel)}
            permutable_groups = [
                [reindexing[a] for a in g if a in reindexing]
                for g in permutable_groups
            ]
            permutable_groups = [g for g in permutable_groups if len(g) > 1]
        # `permutable_groups` can be fully emptied by the `len(g) > 1` filter above
        # (e.g. when `_eckart_embedding` is invoked, as `eckart_permutation` does
        # internally, on a single-atom `sel`/group) -- `np.concatenate` can't take an
        # empty sequence, and in that case every remaining atom is unassigned anyway.
        if len(permutable_groups) > 0:
            rem_atoms = np.delete(np.arange(len(masses)), np.concatenate(permutable_groups))
        else:
            rem_atoms = np.arange(len(masses))
        permutable_groups = list(permutable_groups) + rem_atoms[:, np.newaxis].tolist()
    if not planar_ref:
        # generate pair-wise product matrix
        if permutable_groups is None:
            A = np.tensordot(
                masses / np.sum(masses),
                ref[..., :, :, np.newaxis] * coords[..., :, np.newaxis, :],
                axes=[0, -3]
            )
        else:
            mw_scaling = np.expand_dims(np.sqrt(masses) / np.sum(masses), [0, 2])
            mw_ref = ref * mw_scaling
            mw_coords = coords * mw_scaling
            A = sum(
                np.sum(
                    mw_ref[..., g, :, np.newaxis] * mw_coords[..., g, np.newaxis, :],
                    axis=-3
                ) for g in permutable_groups
            )
        # take SVD of this
        U, S, V = np.linalg.svd(A)
        rot = np.matmul(U, V)
        if proper_rotation:
            dets = np.linalg.det(rot)
            inversions = np.where(dets < 0)
            V[inversions, :, 2] *= -1
            rot = np.matmul(U, V)

    else:
        # generate pair-wise product matrix but only in 2D
        if permutable_groups is None:
            F = ref[:, :, :2, np.newaxis] * coords[:, :, np.newaxis, :2]
            A = np.tensordot(masses / np.sum(masses), F, axes=[0, 1])
        else:
            mw_scaling = np.expand_dims(np.sqrt(masses) / np.sum(masses), [0, 2])
            mw_ref = ref * mw_scaling
            mw_coords = coords * mw_scaling
            A = sum(
                np.sum(
                    mw_ref[:, g, :2, np.newaxis] * mw_coords[:, g, np.newaxis, :2],
                    axis=1
                ) for g in permutable_groups
            )

        U, S, V = np.linalg.svd(A)
        base_rot = np.matmul(U, V)
        if proper_rotation:
            dets = np.linalg.det(base_rot)
            inversions = np.where(dets < 0)
            V[inversions, :, 1] *= -1
            base_rot = np.matmul(U, V)

        rot = np.broadcast_to(np.eye(3, dtype=float), (len(coords), 3, 3)).copy()
        rot[..., :2, :2] = base_rot

    if transform_coordinates:
        # crd is in _its_ principle axis frame, so now we transform it using ek_rot
        ek_rot = np.swapaxes(rot, -2, -1)
        coords = og_coords @ ek_rot
        # now we rotate this back to the reference frame
        coords = coords @ np.swapaxes(ref_axes if ref_axes.ndim > 2 else ref_axes[np.newaxis], -2, -1)
        # and then shift so the COM doesn't change
        if reset_com:
            if (
                    ref_com.ndim == coords.ndim - 1
                    and ref_com.shape[:-1] == coords.shape[:-2]
            ):
                pad_ref = np.expand_dims(ref_com, -2)
            elif ref_com.ndim == 1:
                pad_ref = np.expand_dims(ref_com, list(range(coords.ndim - 1)))
            else:
                pad_ref = ref_com
            coords = coords + pad_ref
    else:
        coords = None

    base_coord_shape = og_og_coords.shape[:-2]
    coords = coords.reshape(base_coord_shape + coords.shape[-2:])
    og_coords = og_coords.reshape(base_coord_shape + og_coords.shape[-2:])
    com = com.reshape(base_coord_shape + com.shape[-1:])
    pax_axes = pax_axes.reshape(base_coord_shape + pax_axes.shape[-2:])
    rot = rot.reshape(base_coord_shape + rot.shape[-2:])
    base_ref_shape = og_og_ref.shape[:-2]
    og_ref = og_ref.reshape(base_ref_shape + og_ref.shape[-2:])
    ref_com = ref_com.reshape(base_ref_shape + ref_com.shape[-1:])
    ref_axes = ref_axes.reshape(base_ref_shape + ref_axes.shape[-2:])
    return EckartData(
        rot,
        coords,
        EmbeddingData(og_ref, ref_com, ref_axes),
        EmbeddingData(og_coords, com, pax_axes)
    )

def eckart_embedding(ref, coords,
                     masses=None,
                     sel=None,
                     in_paf=False,
                     planar_ref_tolerance=1e-6,
                     proper_rotation=False,
                     permutable_groups=None,
                     reset_com=True,
                     transform_coordinates=True) -> EckartData:
    """
    **LLM Docstring**

    Compute the Eckart embedding that rotates a set of coordinates into maximal
    alignment with a reference geometry.

    Thin public wrapper over the internal `_eckart_embedding`, forwarding all
    options (atom selection, principal-axis handling, planarity tolerance,
    proper-rotation constraint, permutable groups, center-of-mass reset, and whether
    to actually transform the coordinates).

    :param ref: the reference geometry
    :type ref: np.ndarray
    :param coords: the coordinates to embed
    :type coords: np.ndarray
    :param masses: per-atom masses (defaults to unit masses)
    :type masses: np.ndarray | None
    :param sel: optional subset of atoms used to define the embedding
    :type sel: Iterable[int] | None
    :param in_paf: whether the inputs are already in the principal-axis frame
    :type in_paf: bool
    :param planar_ref_tolerance: tolerance for detecting a planar reference
    :type planar_ref_tolerance: float
    :param proper_rotation: restrict the embedding to proper rotations
    :type proper_rotation: bool
    :param permutable_groups: groups of atoms allowed to permute
    :type permutable_groups: Iterable | None
    :param reset_com: re-center on the center of mass after embedding
    :type reset_com: bool
    :param transform_coordinates: apply the rotation to the coordinates
    :type transform_coordinates: bool
    :return: the Eckart embedding data
    :rtype: EckartData
    """
    # if permutable_groups is None:
    return _eckart_embedding(
        ref, coords,
        masses=masses,
        sel=sel,
        in_paf=in_paf,
        planar_ref_tolerance=planar_ref_tolerance,
        proper_rotation=proper_rotation,
        permutable_groups=permutable_groups,
        reset_com=reset_com,
        transform_coordinates=transform_coordinates
    )
rmsd_minimizing_transformation = eckart_embedding

def _validate_permutation_candidates(candidates, n_atoms):
    """
    **LLM Docstring**

    Sanity-check a stack of permutation candidates: integer, in range, and each row
    an actual bijection of `range(n_atoms)`. This exists because a silently-wrong
    candidate (e.g. from a mis-composed atom map) doesn't error downstream -- it just
    quietly returns a bad alignment, which is much worse than failing loudly here.

    :param candidates: candidate permutations, shape `(n_candidates, n_atoms)`
    :type candidates: np.ndarray
    :param n_atoms: the expected number of atoms
    :type n_atoms: int
    :return: the validated candidates, as an int array
    :rtype: np.ndarray
    """
    candidates = np.asanyarray(candidates)
    if candidates.ndim == 1:
        candidates = candidates[np.newaxis]
    if candidates.ndim != 2:
        raise ValueError(
            f"permutation_candidates should be 2D (n_candidates, n_atoms), got shape {candidates.shape}"
        )
    if candidates.shape[-1] != n_atoms:
        raise ValueError(
            f"permutation_candidates has {candidates.shape[-1]} columns but coords has {n_atoms} atoms; "
            "candidates must be full-length permutations over every atom (sel only restricts what is "
            "used to score the match, not what can be permuted)"
        )
    if not np.issubdtype(candidates.dtype, np.integer):
        candidates = candidates.astype(int)
    if not np.all(np.sort(candidates, axis=-1) == np.arange(n_atoms)):
        bad = np.where(np.any(np.sort(candidates, axis=-1) != np.arange(n_atoms), axis=-1))[0]
        raise ValueError(
            f"permutation_candidates rows {bad.tolist()[:5]}{'...' if len(bad) > 5 else ''} "
            f"are not valid permutations of range({n_atoms})"
        )
    return candidates

def _eckart_permutation_from_candidates(
        ref, coords, candidates,
        masses=None,
        sel=None,
        in_paf=False,
        planar_ref_tolerance=1e-6,
        proper_rotation=False,
        candidate_chunk_size=512,
        return_rmsd=False,
        validate_candidates=True
):
    """
    **LLM Docstring**

    Find the best-matching permutation for each structure by exhaustive search over
    an explicit set of candidate permutations, rather than the independent per-group
    Hungarian matching `eckart_permutation` otherwise uses.

    This is the "graph-automorphism-restricted brute force" strategy: every
    candidate is assumed to already be a structurally valid relabeling (e.g. one
    element of a molecular graph's automorphism group, so bonds/elements/chirality
    are guaranteed to line up); this function's only job is to figure out which of
    those valid relabelings actually minimizes the Eckart RMSD to `ref`, since that's
    not something graph automorphism search itself can tell you. Unlike the
    per-group Hungarian matching, this can't accidentally produce a mapping that
    isn't a real automorphism, at the cost of the caller having to supply (or
    generate, e.g. via RDKit) the candidate set up front.

    Every candidate is scored with a single (batched) call into `eckart_rmsd` per
    chunk, so this is cheap for anything up to several thousand candidates; the
    chunking just bounds peak memory; it does not change the result.

    :param ref: the reference geometry, `(n_atoms, 3)`
    :type ref: np.ndarray
    :param coords: the coordinates to permute, `(n_atoms, 3)` or `(n_structures, n_atoms, 3)`
    :type coords: np.ndarray
    :param candidates: candidate permutations, `(n_candidates, n_atoms)`; every atom must
        appear (atoms outside `sel` should simply map to themselves)
    :type candidates: np.ndarray
    :param masses: per-atom masses (defaults to unit masses)
    :type masses: np.ndarray | None
    :param sel: optional subset of atoms used to define/score the embedding (does not
        restrict which atoms `candidates` may permute)
    :type sel: Iterable[int] | None
    :param in_paf: whether the inputs are already in the principal-axis frame
    :type in_paf: bool
    :param planar_ref_tolerance: tolerance for detecting a planar reference
    :type planar_ref_tolerance: float
    :param proper_rotation: restrict embeddings to proper rotations
    :type proper_rotation: bool
    :param candidate_chunk_size: number of candidates scored per batched `eckart_rmsd` call
    :type candidate_chunk_size: int
    :param return_rmsd: also return the winning RMSD for each structure
    :type return_rmsd: bool
    :param validate_candidates: check that every candidate is a genuine permutation
    :type validate_candidates: bool
    :return: the optimal per-structure permutation(s) (and, if requested, the matching
        RMSD(s)); see `eckart_permutation` for the exact index convention (it's the
        same "new atom ordering" convention `candidates` themselves must already use)
    :rtype: np.ndarray | tuple
    """
    ref = np.asanyarray(ref)
    coords = np.asanyarray(coords)
    n_atoms = coords.shape[-2]

    if validate_candidates:
        candidates = _validate_permutation_candidates(candidates, n_atoms)
    else:
        candidates = np.asanyarray(candidates)
        if candidates.ndim == 1:
            candidates = candidates[np.newaxis]
    n_cand = candidates.shape[0]
    if n_cand == 0:
        raise ValueError("permutation_candidates must contain at least one candidate (e.g. the identity)")

    smol = coords.ndim == 2
    if smol:
        coords = coords[np.newaxis]
    n_structs = coords.shape[0]

    best_perm = np.broadcast_to(candidates[0], (n_structs, n_atoms)).copy()
    best_rmsd = np.full(n_structs, np.inf)

    for start in range(0, n_cand, candidate_chunk_size):
        chunk = candidates[start:start + candidate_chunk_size]
        c = chunk.shape[0]
        # coords: (n_structs, n_atoms, 3), chunk: (c, n_atoms) -> (n_structs, c, n_atoms, 3)
        permuted = coords[:, chunk, :]
        rmsd = eckart_rmsd(
            permuted.reshape(n_structs * c, n_atoms, 3),
            ref,
            masses=masses,
            embedding_sel=sel,
            comparison_sel=sel,
            in_paf=in_paf,
            planar_ref_tolerance=planar_ref_tolerance,
            proper_rotation=proper_rotation
        ).reshape(n_structs, c)

        chunk_best = np.argmin(rmsd, axis=1)
        chunk_best_rmsd = rmsd[np.arange(n_structs), chunk_best]
        improved = chunk_best_rmsd < best_rmsd
        best_rmsd = np.where(improved, chunk_best_rmsd, best_rmsd)
        best_perm[improved] = chunk[chunk_best[improved]]

    if smol:
        best_perm = best_perm[0]
        best_rmsd = best_rmsd[0]

    if return_rmsd:
        return best_perm, best_rmsd
    return best_perm

def eckart_permutation(
        ref, coords,
        masses=None,
        sel=None,
        in_paf=False,
        prealign=False,
        planar_ref_tolerance=1e-6,
        proper_rotation=False,
        permutable_groups=None,
        permutation_candidates=None,
        candidate_chunk_size=512,
        return_rmsd=False,
        validate_candidates=True
):
    """
    **LLM Docstring**

    Find, for each structure, the atom permutation that best matches a reference
    under the Eckart embedding.

    Two independent strategies are available. By default (`permutation_candidates`
    left as `None`), this works group by group over `permutable_groups`: for each
    group it Eckart-embeds, builds the mass-weighted distance matrix between
    embedded coordinates and reference atoms, and solves the assignment problem
    (`scipy.optimize.linear_sum_assignment`) to get the optimal relabeling. This is
    fast, but only exact when every group is "freely" permutable on its own (e.g. the
    three hydrogens of an isolated, freely-rotating methyl) -- when the atoms judged
    equivalent actually span more than one branch of the molecule (e.g. two whole
    equivalent methyl groups), independently reassigning each atom within the
    combined group is not guaranteed to land on a permutation that respects the
    molecular graph (it can e.g. mix hydrogens from two different methyls).

    If `permutation_candidates` is given instead (an explicit `(n_candidates,
    n_atoms)` set of full-molecule permutations -- typically the automorphism group
    of the reference's molecular graph, composed with an atom map to `coords`'
    labeling, e.g. from `McUtils.ExternalPrograms.RDMolecule.get_automorphisms`/
    `match_atoms`), this instead exhaustively scores every candidate with
    `eckart_rmsd` and returns whichever is best. This is exact -- every candidate is
    assumed to already be graph-consistent, so the only question is which one best
    matches the actual geometry -- at the cost of needing that candidate set up
    front. See `_eckart_permutation_from_candidates` for the implementation.

    :param ref: the reference geometry
    :type ref: np.ndarray
    :param coords: the coordinates to permute
    :type coords: np.ndarray
    :param masses: per-atom masses (defaults to unit masses)
    :type masses: np.ndarray | None
    :param sel: optional subset of atoms to consider
    :type sel: Iterable[int] | None
    :param in_paf: whether the inputs are already in the principal-axis frame
    :type in_paf: bool
    :param prealign: Eckart-align the coordinates before matching (ignored when
        `permutation_candidates` is given -- every candidate is independently
        re-embedded, so any starting orientation scores identically)
    :type prealign: bool
    :param planar_ref_tolerance: tolerance for detecting a planar reference
    :type planar_ref_tolerance: float
    :param proper_rotation: restrict embeddings to proper rotations
    :type proper_rotation: bool
    :param permutable_groups: groups of atoms allowed to permute (defaults to all);
        ignored when `permutation_candidates` is given
    :type permutable_groups: Iterable | None
    :param permutation_candidates: an explicit set of full-molecule candidate
        permutations to search exhaustively instead of the per-group Hungarian
        matching (see above)
    :type permutation_candidates: np.ndarray | None
    :param candidate_chunk_size: batch size used when scoring `permutation_candidates`
    :type candidate_chunk_size: int
    :param return_rmsd: also return the winning RMSD(s); only supported together
        with `permutation_candidates`
    :type return_rmsd: bool
    :param validate_candidates: check that every entry of `permutation_candidates`
        is a genuine permutation before using it
    :type validate_candidates: bool
    :return: the optimal per-structure atom permutations (and, if `return_rmsd` and
        `permutation_candidates` were both given, the matching RMSD(s)). Each
        permutation is a "new atom ordering": `perm[j]` is the index, in the
        *original* `coords` numbering, of the atom that belongs at position `j` to
        match `ref`'s atom `j` -- so `coords[perm]` is the reordered structure, and
        this is the same convention `Psience.Molecools.Molecule.permute_atoms` and
        RDKit's `RenumberAtoms` use (apply it directly, no inversion needed).
    :rtype: np.ndarray | tuple
    """
    if permutation_candidates is not None:
        return _eckart_permutation_from_candidates(
            ref, coords, permutation_candidates,
            masses=masses,
            sel=sel,
            in_paf=in_paf,
            planar_ref_tolerance=planar_ref_tolerance,
            proper_rotation=proper_rotation,
            candidate_chunk_size=candidate_chunk_size,
            return_rmsd=return_rmsd,
            validate_candidates=validate_candidates
        )
    elif return_rmsd:
        raise NotImplementedError(
            "return_rmsd is currently only supported together with permutation_candidates"
        )

    ref = np.asanyarray(ref)
    og_og_ref = ref
    coords = np.asanyarray(coords)
    og_og_coords = coords
    if prealign:
        embedding_data = eckart_embedding(ref, coords,
                                          masses=masses,
                                          sel=sel,
                                          in_paf=in_paf,
                                          planar_ref_tolerance=planar_ref_tolerance,
                                          proper_rotation=proper_rotation,
                                          permutable_groups=permutable_groups)
        # ref = embedding_data.reference_data.coords
        coords = embedding_data.coordinates

    (ref, ref_com, ref_axes), (coords, com, pax_axes), masses, (og_ref, og_coords) = _prep_eckart_data(
        ref, coords, masses,
        sel=sel, in_paf=True
    )

    mw_scaling = np.expand_dims(np.sqrt(masses) / np.sum(masses), [0, 2])
    mw_ref = ref * mw_scaling
    # mw_coords = coords * mw_scaling

    if permutable_groups is not None:
        if sel is not None:
            reindexing = {a: i for i, a in enumerate(sel)}
            permutable_groups = [
                [reindexing[a] for a in g if a in reindexing]
                for g in permutable_groups
            ]
            permutable_groups = [g for g in permutable_groups if len(g) > 1]
        # `permutable_groups` can be fully emptied by the `len(g) > 1` filter above
        # (e.g. when `_eckart_embedding` is invoked, as `eckart_permutation` does
        # internally, on a single-atom `sel`/group) -- `np.concatenate` can't take an
        # empty sequence, and in that case every remaining atom is unassigned anyway.
        if len(permutable_groups) > 0:
            rem_atoms = np.delete(np.arange(len(masses)), np.concatenate(permutable_groups))
        else:
            rem_atoms = np.arange(len(masses))
        permutable_groups = list(permutable_groups) + rem_atoms[:, np.newaxis].tolist()
    else:
        permutable_groups = [np.arange(mw_ref.shape[-2])]

    base_perm = np.repeat(np.arange(og_ref.shape[-2])[np.newaxis], ref.shape[0], axis=0)
    if sel is not None:
        perm = base_perm[:, sel]
    else:
        perm = base_perm
    base_shape = ref.shape[:-2]
    for p in permutable_groups:
        sub_data = eckart_embedding(ref, coords,
                                    masses=masses,
                                    sel=p,
                                    in_paf=in_paf,
                                    planar_ref_tolerance=planar_ref_tolerance,
                                    proper_rotation=proper_rotation,
                                    permutable_groups=[p])
        mw_coords = sub_data.coordinates * mw_scaling

        p = np.asanyarray(p)
        n = len(p)
        dists = np.zeros(base_shape + (n, n))
        rows, cols = np.triu_indices(n, k=0)
        dist_triu = np.linalg.norm(
            mw_coords[..., rows, :] - mw_ref[..., p[cols], :],
            axis=-1
        )
        dists[..., rows, cols] = dist_triu
        dists[..., cols, rows] = dist_triu

        for k,cost in enumerate(dists):
            _, sub_perm = opt.linear_sum_assignment(cost)
            perm[k][p] = p[sub_perm]
    if sel is not None:
        base_perm[:, sel] = perm

    targ_shape = og_og_coords.shape[:-2]
    return base_perm.reshape(targ_shape + (-1,))


def eckart_displacement_coords(coords, ref, masses=None, **embedding_parameters):
    """
    **LLM Docstring**

    Express Eckart-embedded coordinates in the reference's translation/rotation-
    invariant (internal) coordinate frame.

    The reference's invariant transformation (from
    `translation_rotation_invariant_transformation`) is applied to the Eckart-embedded
    coordinates.

    :param coords: the coordinates to embed and project
    :type coords: np.ndarray
    :param ref: the reference geometry
    :type ref: np.ndarray
    :param masses: per-atom masses
    :type masses: np.ndarray | None
    :param embedding_parameters: extra options forwarded to `eckart_embedding`
    :return: the displacement coordinates in the reference internal frame
    :rtype: np.ndarray
    """
    ref_embedding, _ = translation_rotation_invariant_transformation(ref,
                                                                  masses=masses,
                                                                  mass_weighted=False
                                                                  )
    base_embedding = eckart_embedding(ref, coords, masses=masses, **embedding_parameters)
    return np.reshape(
        ref_embedding @ base_embedding.coordinates[..., np.newaxis],
        base_embedding.coordinates.shape
    )

def eckart_rmsd(coords, ref,
                masses=None,
                embed=True,
                comparison_sel=None,
                embedding_sel=None,
                mass_weighted=False,
                return_diffs=False,
                averaged=False,
                total=False,
                **embedding_parameters):
    """
    **LLM Docstring**

    Compute the RMSD between a set of coordinates and a reference after Eckart
    embedding.

    The coordinates are optionally Eckart-embedded onto the reference (using
    `embedding_sel`), optionally mass-weighted, and optionally restricted to
    `comparison_sel` before the (unaligned) RMSD is taken with
    `unembedded_pts_rmsd`.

    :param coords: the coordinates to compare
    :type coords: np.ndarray
    :param ref: the reference geometry
    :type ref: np.ndarray
    :param masses: per-atom masses
    :type masses: np.ndarray | None
    :param embed: whether to Eckart-embed before comparing
    :type embed: bool
    :param comparison_sel: atoms included in the RMSD
    :type comparison_sel: Iterable[int] | None
    :param embedding_sel: atoms used to define the embedding
    :type embedding_sel: Iterable[int] | None
    :param mass_weighted: mass-weight the coordinates before comparison
    :type mass_weighted: bool
    :param return_diffs: also return the difference vectors
    :type return_diffs: bool
    :param averaged: per-atom rather than per-coordinate normalization
    :type averaged: bool
    :param total: apply the per-atom normalization
    :type total: bool
    :param embedding_parameters: extra options forwarded to `eckart_embedding`
    :return: the Eckart RMSD (plus diffs if requested)
    :rtype: np.ndarray | tuple
    """
    if embed:
        if embedding_sel is None:
            embedding_sel = comparison_sel
        ref = np.asanyarray(ref)
        eckart_data:EckartData = eckart_embedding(
            ref, coords,
            masses=masses,
            sel=embedding_sel,
            **embedding_parameters
        )
        coords = eckart_data.coordinates

    if masses is not None and mass_weighted:
        masses = np.sqrt(np.asanyarray(masses) / np.sum(masses))
        coords = coords * vec_ops.broadcast_constant(masses[:, np.newaxis], coords.shape[:-2], pad_base=True)
        ref = ref * vec_ops.broadcast_constant(masses[:, np.newaxis], ref.shape[:-2], pad_base=True)

    if comparison_sel is not None:
        coords = coords[..., comparison_sel, :]
        ref = ref[..., comparison_sel, :]

    return vec_ops.unembedded_pts_rmsd(coords, ref,
                                       return_diffs=return_diffs,
                                       total=total,
                                       averaged=averaged)

def incremental_eckart_rmsd(coords,
                            refs=None,
                            masses=None,
                            mass_weighted=False,
                            **embedding_parameters):
    """
    **LLM Docstring**

    Compute the cumulative Eckart RMSD along a sequence of geometries.

    Consecutive structures are compared pairwise with `eckart_rmsd` (or against the
    supplied `refs`), and the resulting step RMSDs are cumulatively summed to give a
    running path length; a leading zero is prepended so the output aligns with the
    input sequence.

    :param coords: the sequence of geometries
    :type coords: np.ndarray
    :param refs: explicit references per step (defaults to the previous frame)
    :type refs: np.ndarray | None
    :param masses: per-atom masses
    :type masses: np.ndarray | None
    :param mass_weighted: mass-weight the coordinates before comparison
    :type mass_weighted: bool
    :param embedding_parameters: extra options forwarded to `eckart_rmsd`
    :return: the cumulative Eckart RMSD along the sequence
    :rtype: np.ndarray
    """
    coords = np.asanyarray(coords)
    if refs is None:
        coords, refs = coords[..., :-1, :, :], coords[..., 1:, :, :]

    base_rmsd = eckart_rmsd(coords, refs, masses=masses, mass_weighted=mass_weighted, **embedding_parameters)
    z = np.zeros(base_rmsd.shape[:-1] + (1,))
    return np.cumsum(
        np.concatenate([z, base_rmsd], axis=-1),
        axis=-1
    )
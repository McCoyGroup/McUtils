import itertools

import numpy as np
import collections

from .. import Numputils as nput

__all__ = [
    "RedundantCoordinateGenerator"
]


class RedundantCoordinateGenerator:

    def __init__(self,
                 coordinate_specs, angle_ordering='ijk',
                 untransformed_coordinates=None, masses=None,
                 relocalize=False,
                 **opts):
        """
        **LLM Docstring**

        Store the coordinate specification and options used to construct nonredundant combinations of redundant internals.

        `angle_ordering` is inserted into the option dictionary passed to internal-coordinate tensor generation. Optional fixed coordinates, masses, and relocalization behavior become defaults for later calls to `compute_redundant_expansions`.

        :param coordinate_specs: Internal-coordinate definitions consumed by `internal_coordinate_tensors`.
        :type coordinate_specs: collections.abc.Sequence
        :param angle_ordering: Angular derivative/index convention forwarded as an option.
        :type angle_ordering: str
        :param untransformed_coordinates: Coordinate positions that should remain explicit rather than mixed into the redundant transformation.
        :type untransformed_coordinates: collections.abc.Sequence[int] | None
        :param masses: Atom or Cartesian-component masses used for mass weighting.
        :type masses: np.ndarray | None
        :param relocalize: Whether to rotate the nonredundant basis toward selected original coordinates.
        :type relocalize: bool
        :param opts: Additional options forwarded to internal-coordinate tensor generation.
        :type opts: dict
        :return: None.
        :rtype: None
        """
        self.specs = coordinate_specs
        self.untransformed_coordinates = untransformed_coordinates
        self.relocalize = relocalize
        self.masses = masses
        self.opts = dict(
            opts,
            angle_ordering=angle_ordering
        )

    @classmethod
    def _pad_redund_tf(cls, redund_tf, n):
        """
        **LLM Docstring**

        Embed a redundant-coordinate transformation beneath an `n`-dimensional identity block.

        The result leaves the first `n` coordinates unchanged and applies `redund_tf` to the remaining coordinates. Leading batch dimensions are preserved by constructing batched identity tensors and padding both blocks before concatenating them along the output-coordinate axis.

        :param redund_tf: Transformation with shape `(..., n_redundant, n_nonredundant)`.
        :type redund_tf: np.ndarray
        :param n: Number of leading coordinates to pass through unchanged.
        :type n: int
        :return: Block transformation with `n` identity columns prepended and `n` zero rows above `redund_tf`.
        :rtype: np.ndarray
        """
        ndim = redund_tf.ndim - 2
        eye = nput.identity_tensors(redund_tf.shape[:-2], n)
        return np.concatenate(
            [
                np.pad(eye, ([[0, 0]] * ndim) + [[0, redund_tf.shape[-2]], [0, 0]]),
                np.pad(redund_tf, ([[0, 0]] * ndim) + [[n, 0], [0, 0]])
            ],
            axis=-1
        )

    @classmethod
    def _relocalize_tf(cls, redund_tf, untransformed_coordinates=None):
        """
        **LLM Docstring**

        Rotate a nonredundant basis toward selected original redundant coordinates without changing its spanned subspace.

        A target matrix is built from the first `n` original coordinate axes, or from axes listed in `untransformed_coordinates` followed by remaining axes. A least-squares map from `redund_tf` to that target is projected to the nearest orthogonal matrix via SVD (`U @ V`), and the original transformation is right-multiplied by that rotation.

        :param redund_tf: Basis matrix with redundant coordinates on the penultimate axis and nonredundant coordinates on the last axis.
        :type redund_tf: np.ndarray
        :param untransformed_coordinates: Original coordinate indices that should be favored first in the localized basis.
        :type untransformed_coordinates: collections.abc.Sequence[int] | None
        :return: Orthogonally rotated transformation spanning the same column space.
        :rtype: np.ndarray
        """
        n = redund_tf.shape[-1]
        if untransformed_coordinates is None:
            # target = np.pad(np.eye(n), [[0, 173 - 108], [0, 0]])
            ndim = redund_tf.ndim - 2
            eye = nput.identity_tensors(redund_tf.shape[:-2], n)
            target = np.pad(eye, ([[0, 0]] * ndim) + [[0, redund_tf.shape[-2] - n], [0, 0]])
        else:
            untransformed_coordinates = np.asanyarray(untransformed_coordinates)
            coords = np.concatenate([
                untransformed_coordinates,
                np.delete(np.arange(redund_tf.shape[-2]), untransformed_coordinates)
                ])[:n]
            target = np.moveaxis(np.zeros(redund_tf.shape), -1, -2)
            idx = nput.vector_ix(target.shape[:-1], coords[:, np.newaxis])
            target[idx] = 1
            target = np.moveaxis(target, -1, -2)
        loc = np.linalg.lstsq(redund_tf, target, rcond=None)
        U, s, V = np.linalg.svd(loc[0])
        R = U @ V
        return redund_tf @ R


    @classmethod
    def base_redundant_transformation(cls, expansion,
                                      untransformed_coordinates=None,
                                      masses=None,
                                      relocalize=False
                                      ):
        """
        **LLM Docstring**

        Extract an orthonormal basis for the non-null internal-coordinate subspace from a Cartesian-to-internal derivative expansion.

        The first expansion tensor is optionally mass weighted by `1/sqrt(mass)`; atom masses are repeated over Cartesian components when necessary. When fixed coordinates are requested, their derivative columns are placed first and projected out of the remaining columns so they stay explicit without reducing rank. The internal metric `G = B.T @ B` is diagonalized, eigenvectors with eigenvalues above `1e-10` are retained, and their order is reversed. Optional relocalization rotates this basis toward original coordinate axes.

        :param expansion: Derivative expansion whose first element is the Cartesian-to-internal Jacobian `B`.
        :type expansion: collections.abc.Sequence[np.ndarray]
        :param untransformed_coordinates: Internal-coordinate column indices that should remain explicit in the basis.
        :type untransformed_coordinates: collections.abc.Sequence[int] | None
        :param masses: Atom masses or Cartesian-component masses for mass weighting.
        :type masses: np.ndarray | None
        :param relocalize: Whether to rotate the retained eigenvector basis toward original coordinate axes.
        :type relocalize: bool
        :return: Transformation matrix or per-batch list mapping redundant internals to the retained non-null basis.
        :rtype: np.ndarray | list[np.ndarray]
        """
        conv = np.asanyarray(expansion[0])
        if masses is not None:
            masses = np.asanyarray(masses)
            if len(masses) == conv.shape[-2] // 3:
                masses = np.repeat(masses, 3)
            masses = np.diag(1 / np.sqrt(masses))
            if conv.ndim > 2:
                masses = np.broadcast_to(
                    np.expand_dims(masses, list(range(conv.ndim - 2))),
                    conv.shape[:-2] + masses.shape
                )
            conv = masses @ conv

        if untransformed_coordinates is not None:
            transformed_coords = np.setdiff1d(np.arange(conv.shape[-1]), untransformed_coordinates)
            ut_conv = conv[..., untransformed_coordinates]
            conv = conv[..., transformed_coords]

            # project out contributions along untransformed coordinates to ensure
            # dimension of space remains unchanged
            ut_conv_norm = nput.vec_normalize(np.moveaxis(ut_conv, -1, -2))
            proj = np.moveaxis(ut_conv_norm, -1, -2) @ ut_conv_norm
            proj = nput.identity_tensors(proj.shape[:-2], proj.shape[-1]) - proj

            conv = np.concatenate([ut_conv, proj @ conv], axis=-1)

        G_internal = np.moveaxis(conv, -1, -2) @ conv
        redund_vals, redund_tf = np.linalg.eigh(G_internal)
        redund_pos = np.where(np.abs(redund_vals) > 1e-10)
        if redund_vals.ndim > 1:
            redund_tf = nput.take_where_groups(redund_tf, redund_pos)
        else:
            redund_tf = redund_tf[:, redund_pos[0]]
        if isinstance(redund_tf, np.ndarray):
            redund_tf = np.flip(redund_tf, axis=-1)
        else:
            redund_tf = [
                np.flip(tf, axis=-1)
                for tf in redund_tf
            ]

        # if transformed_coords is not None:
        #     n = len(untransformed_coordinates)
        #     if isinstance(redund_tf, np.ndarray):
        #         redund_tf = cls._pad_redund_tf(redund_tf, n)
        #     else:
        #         redund_tf = [
        #             cls._pad_redund_tf(tf, n)
        #             for tf in redund_tf
        #         ]

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
            # provide some facility for rearranging coords?
            if isinstance(redund_tf, np.ndarray):
                redund_tf = cls._relocalize_tf(redund_tf, untransformed_coordinates=untransformed_coordinates)
            else:
                redund_tf = [
                    cls._relocalize_tf(tf, untransformed_coordinates=untransformed_coordinates)
                    for tf in redund_tf
                ]



        return redund_tf


    @classmethod
    def get_redundant_transformation(cls, base_expansions, untransformed_coordinates=None, masses=None,
                                     relocalize=False):
        """
        **LLM Docstring**

        Construct the nonredundant transformation and re-expand derivative tensors into that basis.

        The input may be a single 2-D Jacobian, a derivative expansion sequence, or `(forward_expansions, inverse_expansions)`. After `base_redundant_transformation` determines the basis, `tensor_reexpand` applies it to every derivative order. If inverse expansions are supplied, they are transformed with the transposed basis and returned alongside the forward expansions. Batched transformations represented as a list are processed independently.

        :param base_expansions: Forward derivative tensors, optionally paired with inverse derivative tensors.
        :type base_expansions: np.ndarray | collections.abc.Sequence | tuple
        :param untransformed_coordinates: Coordinate indices preserved explicitly in the transformation.
        :type untransformed_coordinates: collections.abc.Sequence[int] | None
        :param masses: Masses used to weight the base Jacobian.
        :type masses: np.ndarray | None
        :param relocalize: Whether to rotate the basis toward original coordinate axes.
        :type relocalize: bool
        :return: `(transformation, transformed_expansions)`, where transformed expansions may itself be `(forward, inverse)`.
        :rtype: tuple
        """
        if isinstance(base_expansions, np.ndarray) and base_expansions.ndim == 2:
            base_expansions = [base_expansions]
            base_inv = None
        elif (
                len(base_expansions) == 2
                and not nput.is_numeric_array_like(base_expansions[0], ndim=2)
        ):
            base_expansions, base_inv = base_expansions
        else:
            base_inv = None
        redund_tf = cls.base_redundant_transformation(base_expansions,
                                                      untransformed_coordinates=untransformed_coordinates,
                                                      masses=masses,
                                                      relocalize=relocalize
                                                      )

        # dQ/dR, which we can transform with dR/dX to get dQ/dX
        if isinstance(redund_tf, np.ndarray):
            redund_expansions = nput.tensor_reexpand(base_expansions, [redund_tf], order=len(base_expansions))
            if base_inv is not None:
                redund_inv = nput.tensor_reexpand([redund_tf.T], base_inv, order=len(base_inv))
                redund_expansions = (redund_expansions, redund_inv)
        else:
            redund_expansions = [
                nput.tensor_reexpand(base_expansions, [tf], order=len(base_expansions))
                for tf in redund_tf
            ]
            if base_inv is not None:
                redund_inv = [
                    nput.tensor_reexpand([tf.T], base_inv, order=len(base_inv))
                    for tf in redund_tf
                ]
                redund_expansions = (redund_expansions, redund_inv)

        return redund_tf, redund_expansions

    def compute_redundant_expansions(self,
                                     coords,
                                     order=None,
                                     untransformed_coordinates=None,
                                     expansions=None,
                                     relocalize=None):
        """
        **LLM Docstring**

        Evaluate Cartesian derivatives of the configured redundant coordinates and transform them to a nonredundant basis.

        Unless derivative tensors are supplied directly, `internal_coordinate_tensors` is evaluated for `coords` and `self.specs`; its coordinate values are discarded and derivative orders are retained. The requested order defaults to one. Instance defaults for fixed coordinates, masses, relocalization, angle ordering, and other options are then passed to `get_redundant_transformation`.

        :param coords: Cartesian coordinates at which internal-coordinate derivatives are evaluated.
        :type coords: np.ndarray
        :param order: Highest derivative order. Defaults to one when omitted.
        :type order: int | None
        :param untransformed_coordinates: Override for coordinate positions kept explicit.
        :type untransformed_coordinates: collections.abc.Sequence[int] | None
        :param expansions: Precomputed derivative expansion, bypassing `internal_coordinate_tensors`.
        :type expansions: collections.abc.Sequence[np.ndarray] | None
        :param relocalize: Override for whether the basis is localized toward original coordinates.
        :type relocalize: bool | None
        :return: Nonredundant transformation and transformed derivative expansions.
        :rtype: tuple
        """
        coords = np.asanyarray(coords)
        if order is None:
            opts = dict(dict(order=1), **self.opts)
        else:
            opts = dict(self.opts, order=order)
        if untransformed_coordinates is None:
            untransformed_coordinates = self.untransformed_coordinates
        if relocalize is None:
            relocalize = self.relocalize
        if expansions is None:
            base_expansions = nput.internal_coordinate_tensors(coords, self.specs, **opts)[1:]
        else:
            base_expansions = expansions
        return self.get_redundant_transformation(base_expansions,
                                                 untransformed_coordinates=untransformed_coordinates,
                                                 masses=self.masses,
                                                 relocalize=relocalize
                                                 )

    @classmethod
    def _prune_coords_svd(cls, b_mat, svd_cutoff=5e-2, sort=True, fixed_vecs=None):
        """
        **LLM Docstring**

        Select coordinate columns that are strongly represented in the row space of a B matrix.

        After optional projection away from fixed columns, an SVD is computed. For each coordinate column, the largest squared component among non-null right singular vectors is used as a localization score. Columns above `svd_cutoff` are retained and optionally sorted by decreasing score; fixed columns are prepended unchanged.

        :param b_mat: B matrix with Cartesian directions on rows and internal coordinates on columns.
        :type b_mat: np.ndarray
        :param svd_cutoff: Minimum maximum squared right-singular-vector component required for retention.
        :type svd_cutoff: float
        :param sort: Whether to order retained nonfixed coordinates by decreasing localization score.
        :type sort: bool
        :param fixed_vecs: Coordinate columns that must be retained and projected out before scoring the rest.
        :type fixed_vecs: collections.abc.Sequence[int] | None
        :return: Selected coordinate-column indices.
        :rtype: np.ndarray
        """
        # turns out, equivalent to finding maximimum loc in eigenvectors of G
        if fixed_vecs is not None:
            transformed_coords = np.delete(np.arange(b_mat.shape[-1]), fixed_vecs)
            ut_conv = b_mat[..., fixed_vecs]
            conv = b_mat[..., transformed_coords]

            # project out contributions along untransformed coordinates to ensure
            # dimension of space remains unchanged
            ut_conv = nput.vec_normalize(ut_conv)
            proj = ut_conv @ np.moveaxis(ut_conv, -1, -2)
            proj = nput.identity_tensors(proj.shape[:-2], proj.shape[-1]) - proj

            b_mat = proj @ conv

        _, s, Q = np.linalg.svd(b_mat)
        pos = np.where(s > 1e-8)
        loc_val = np.max(Q[pos]**2, axis=0)
        coords = np.where(loc_val > svd_cutoff)[0]
        if sort:
            coords = coords[np.argsort(-loc_val[coords,],)]
        if fixed_vecs is not None:
            coords = transformed_coords[coords,]
            coords = np.concatenate([fixed_vecs, coords])
        return coords

    @classmethod
    def _prune_coords_loc(cls, b_mat, loc_cutoff=.33, sort=True, fixed_vecs=None):
        """
        **LLM Docstring**

        Select coordinate columns from the diagonal of the projector onto the B-matrix row space.

        The non-null eigenvectors of `B.T @ B` define the row-space basis. Solving `Q X ~= I` and taking `diag(Q X)` gives a per-coordinate localization/leverage score; columns above `loc_cutoff` are retained and optionally sorted. Fixed columns are prepended, after which localization is recomputed on the reduced matrix to remove newly incompatible nonfixed columns.

        :param b_mat: B matrix with candidate coordinates as columns.
        :type b_mat: np.ndarray
        :param loc_cutoff: Minimum projector-diagonal localization score.
        :type loc_cutoff: float
        :param sort: Whether to sort selected nonfixed columns by decreasing score.
        :type sort: bool
        :param fixed_vecs: Coordinate columns that must appear first in the result.
        :type fixed_vecs: collections.abc.Sequence[int] | None
        :return: Selected coordinate-column indices.
        :rtype: np.ndarray
        """
        # if fixed_vecs is not None:
        #     transformed_coords = np.delete(np.arange(b_mat.shape[-1]), fixed_vecs)
        #     ut_conv = b_mat[..., fixed_vecs]
        #     b_mat = b_mat[..., transformed_coords]
        #
        #     # # project out contributions along untransformed coordinates to ensure
        #     # # dimension of space remains unchanged
        #     # ut_conv = nput.vec_normalize(ut_conv)
        #     # proj = ut_conv @ np.moveaxis(ut_conv, -1, -2)
        #     # proj = nput.identity_tensors(proj.shape[:-2], proj.shape[-1]) - proj
        #     #
        #     # b_mat = proj @ conv

        s, Q = np.linalg.eigh(b_mat.T @ b_mat)
        pos = np.where(s > 1e-8)[0]
        Q = Q[:, pos]
        loc_mat = np.linalg.lstsq(Q, np.eye(Q.shape[-2]), rcond=None)
        loc_val = np.diag(Q @ loc_mat[0])
        coords = np.where(loc_val > loc_cutoff)[0]
        if fixed_vecs is not None:
            coords = np.setdiff1d(coords, fixed_vecs)
        if sort:
            coords = coords[np.argsort(-loc_val[coords,], )]
        if fixed_vecs is not None:
            coords = np.concatenate([fixed_vecs, coords])

            # have to run this back again in case these added coords break the localization
            # a third run back isn't work it since that will just repeat what's found here
            b_mat = b_mat[:, coords]
            s, Q = np.linalg.eigh(b_mat.T @ b_mat)
            pos = np.where(s > 1e-8)[0]
            Q = Q[:, pos]
            loc_mat = np.linalg.lstsq(Q, np.eye(Q.shape[-2]), rcond=None)
            loc_val = np.diag(Q @ loc_mat[0])
            subcoords = np.setdiff1d(np.where(loc_val > loc_cutoff)[0], np.arange(len(fixed_vecs)))
            if sort:
                subcoords = subcoords[np.argsort(-loc_val[subcoords,], )]
            coords = np.concatenate([coords[:len(fixed_vecs)], coords[subcoords]])

        return coords

    @classmethod
    def _prune_coords_gs(cls, b_mat, fixed_vecs=None, core_scaling=1e3, max_condition_number=1e8):
        """
        **LLM Docstring**

        Greedily add coordinate columns while controlling the condition number of the selected Gram matrix.

        When no fixed core is supplied, columns with norm greater than `0.9` across nonzero right singular vectors are chosen as the initial core. Remaining columns are tested in index order. A column is retained in the overall selection when the augmented Gram matrix condition number is below `max_condition_number`; it remains in the evolving core only when that condition number does not exceed the scaled base-core condition.

        :param b_mat: B matrix with candidate coordinates as columns.
        :type b_mat: np.ndarray
        :param fixed_vecs: Initial mandatory coordinate columns, or `None` to infer them from the SVD.
        :type fixed_vecs: collections.abc.Sequence[int] | None
        :param core_scaling: Factor multiplying the initial core condition number before comparing later additions.
        :type core_scaling: float
        :param max_condition_number: Absolute condition-number limit for retaining a tested column.
        :type max_condition_number: float
        :return: Indices marked for retention.
        :rtype: np.ndarray
        """
        if fixed_vecs is None:
            _, s, Q = np.linalg.svd(b_mat)
            pos = np.where(s > 0)
            fixed_vecs = np.where(np.linalg.norm(Q[pos], axis=0) > .9)[0]
        fixed_vecs = np.array(fixed_vecs)
        core_mask = np.full(b_mat.shape[1], False)
        core_mask[fixed_vecs] = True
        all_mask = core_mask.copy()
        rem_pos = np.setdiff1d(np.arange(b_mat.shape[1]), fixed_vecs)
        base_evals = np.linalg.eigvalsh(b_mat[:, core_mask].T @ b_mat[:, core_mask])
        base_cond = base_evals[-1] / base_evals[0] * core_scaling
        for r in rem_pos:
            core_mask[r] = True
            evals = np.linalg.eigvalsh(b_mat[:, core_mask].T @ b_mat[:, core_mask])
            new_cond = abs(evals[-1] / evals[0])
            if new_cond < max_condition_number:
                all_mask[r] = True
                if new_cond > base_cond:
                    core_mask[r] = False
            else:
                core_mask[r] = False

        return np.where(all_mask)[0]

    @classmethod
    def prune_coordinate_specs(cls, expansion,
                               masses=None,
                               untransformed_coordinates=None,
                               pruning_mode='loc',
                               **opts
                               ):
        """
        **LLM Docstring**

        Mass-weight a coordinate Jacobian and dispatch one of the supported column-selection algorithms.

        The first expansion tensor is interpreted as a Cartesian-to-internal Jacobian. Atom masses are repeated three times when their count matches one third of the Cartesian row count, then the Jacobian is left-multiplied by `diag(1/sqrt(mass))`. `pruning_mode` selects SVD localization, projector localization, or greedy condition-number pruning.

        :param expansion: Derivative expansion whose first element is the coordinate Jacobian.
        :type expansion: collections.abc.Sequence[np.ndarray]
        :param masses: Atom or Cartesian-component masses. The implementation requires this argument despite its default of `None`.
        :type masses: np.ndarray
        :param untransformed_coordinates: Coordinate columns that must be retained.
        :type untransformed_coordinates: collections.abc.Sequence[int] | None
        :param pruning_mode: One of `"svd"`, `"loc"`, or `"gs"`.
        :type pruning_mode: str
        :param opts: Additional options passed to the selected pruning helper.
        :type opts: dict
        :return: Selected coordinate-column indices.
        :rtype: np.ndarray
        :raises ValueError: If `pruning_mode` is not recognized.
        """
        conv = np.asanyarray(expansion[0])
        masses = np.asanyarray(masses)
        if len(masses) == conv.shape[-2] // 3:
            masses = np.repeat(masses, 3)
        masses = np.diag(1 / np.sqrt(masses))
        b_mat = masses @ conv

        if pruning_mode == 'svd':
            return cls._prune_coords_svd(b_mat, fixed_vecs=untransformed_coordinates, **opts)
        elif pruning_mode == 'loc':
            return cls._prune_coords_loc(b_mat, fixed_vecs=untransformed_coordinates, **opts)
        elif pruning_mode == 'gs':
            return cls._prune_coords_gs(b_mat, fixed_vecs=untransformed_coordinates, **opts)
        else:
            raise ValueError(f"don't understand pruning mode {pruning_mode}")

class MultiOriginCoordinates:

    def __init__(self, origins, zmats):
        """
        **LLM Docstring**

        Placeholder constructor for multi-origin coordinate support.

        The body contains only `...`; `origins` and `zmats` are not stored or otherwise processed, so instances receive no initialization beyond normal object creation.

        :param origins: Intended origin definitions; currently unused.
        :type origins: object
        :param zmats: Intended Z-matrix definitions; currently unused.
        :type zmats: object
        :return: None.
        :rtype: None
        """
        ...


"""
An object-level interface to the spherical multipole kernels in `McUtils.Numputils.Multipoles`
"""

import numpy as np

from .. import Numputils as nput

__all__ = [
    "MultipoleExpansion"
]


class MultipoleExpansion:
    """
    A (possibly batched) spherical multipole (outer) or local (inner) expansion about one
    or more centers.

    Coefficients are stored in the packed complex layout of `Numputils.Multipoles`
    (`l(l+1)/2 + m`, `m >= 0`), with shape `batch_shape + (P,)`; `center` has shape
    `batch_shape + (3,)`. A batch can hold independent expansions (e.g. one per structure)
    or the sites of a distributed expansion (e.g. one per atom), which `evaluate(..., sum_axis=...)`
    and `sum` reduce over.

    Multipole expansions may carry a Gaussian `smearing` width per site, in which case they
    represent the GTO-smeared densities used by MACE-POLAR/`graph_longrange` and evaluate to the
    exact smeared potential. Smeared expansions can be rotated and moved rigidly, but not
    re-expanded about another center.
    """

    kinds = ('multipole', 'local')

    def __init__(self, coefficients, center=None, kind='multipole', smearing=None):
        """
        :param coefficients: packed complex coefficients, `(..., P)`
        :type coefficients: np.ndarray
        :param center: expansion center(s), `(..., 3)` (origin if `None`)
        :type center: np.ndarray | None
        :param kind: `'multipole'` or `'local'`
        :type kind: str
        :param smearing: Gaussian width(s) for smeared multipole sites, broadcast against the batch shape
        :type smearing: float | np.ndarray | None
        """
        coefficients = np.asanyarray(coefficients)
        if not np.iscomplexobj(coefficients):
            coefficients = coefficients.astype(complex)
        kind = kind.lower()
        if kind not in self.kinds:
            raise ValueError(f"unknown expansion kind '{kind}', expected one of {self.kinds}")
        if smearing is not None and kind != 'multipole':
            raise ValueError("only multipole expansions can be smeared")
        self._order = nput.multipole_expansion_order(coefficients)
        batch_shape = coefficients.shape[:-1]
        if center is None:
            center = np.zeros(3)
        center = np.asanyarray(center, dtype=float)
        batch_shape = np.broadcast_shapes(batch_shape, center.shape[:-1])
        if smearing is not None:
            smearing = np.asanyarray(smearing, dtype=float)
            batch_shape = np.broadcast_shapes(batch_shape, smearing.shape)
            smearing = np.broadcast_to(smearing, batch_shape)
        self.coefficients = np.broadcast_to(coefficients, batch_shape + coefficients.shape[-1:])
        self.center = np.broadcast_to(center, batch_shape + (3,))
        self.kind = kind
        self.smearing = smearing

    # region construction

    @classmethod
    def from_charges(cls, positions, charges, order, center=None, kind='multipole'):
        """
        Builds the expansion of a set of point charges.

        :param positions: charge positions, `(..., N, 3)`
        :type positions: np.ndarray
        :param charges: charges, `(..., N)` (`None` for unit charges)
        :type charges: np.ndarray | None
        :param order: expansion order
        :type order: int
        :param center: expansion center(s), `(..., 3)`
        :type center: np.ndarray | None
        :param kind: `'multipole'` (valid outside the charges) or `'local'` (valid inside them)
        :type kind: str
        :return: the expansion
        :rtype: MultipoleExpansion
        """
        if kind == 'multipole':
            coeffs = nput.multipole_moments(positions, charges, order, center=center)
        elif kind == 'local':
            coeffs = nput.local_multipole_expansion(positions, charges, order, center=center)
        else:
            raise ValueError(f"unknown expansion kind '{kind}'")
        return cls(coeffs, center=center, kind=kind)

    @classmethod
    def from_real(cls, coefficients, center=None, smearing=None):
        """
        Builds a multipole expansion from real Racah-normalized moments ordered `m = -l..l`
        per `l` (the `e3nn`/MACE-POLAR `density_coefficients` convention).

        :param coefficients: real moments, `(..., (L+1)^2)`
        :type coefficients: np.ndarray
        :param center: expansion center(s), `(..., 3)`
        :type center: np.ndarray | None
        :param smearing: Gaussian width(s) for smeared sites
        :type smearing: float | np.ndarray | None
        :return: the expansion
        :rtype: MultipoleExpansion
        """
        return cls(nput.real_spherical_to_multipoles(coefficients), center=center, smearing=smearing)

    @classmethod
    def from_cartesian(cls, tensors, center=None, convention='raw', smearing=None):
        """
        Builds a multipole expansion from Cartesian moments `[M0, M1, M2, ...]`.

        :param tensors: Cartesian moments by order
        :type tensors: list[np.ndarray]
        :param center: expansion center(s), `(..., 3)`
        :type center: np.ndarray | None
        :param convention: `'raw'`, `'traceless'`, or `'buckingham'`
        :type convention: str
        :param smearing: Gaussian width(s) for smeared sites
        :type smearing: float | np.ndarray | None
        :return: the expansion
        :rtype: MultipoleExpansion
        """
        return cls(
            nput.cartesian_to_spherical_multipoles(tensors, convention=convention),
            center=center,
            smearing=smearing
        )

    def to_real(self):
        """
        :return: real Racah-normalized moments ordered `m = -l..l` per `l`
        :rtype: np.ndarray
        """
        self._require_kind('multipole', 'to_real')
        return nput.multipoles_to_real_spherical(self.coefficients)

    def to_cartesian(self, convention='traceless'):
        """
        :param convention: `'traceless'` or `'buckingham'`
        :type convention: str
        :return: traceless Cartesian moments `[M0, M1, M2, ...]`
        :rtype: list[np.ndarray]
        """
        self._require_kind('multipole', 'to_cartesian')
        return nput.spherical_to_cartesian_multipoles(self.coefficients, convention=convention)

    def modify(self, coefficients=None, center=None, kind=None, smearing=None, drop_smearing=False):
        """
        Returns a copy with the given fields replaced.

        :return: the new expansion
        :rtype: MultipoleExpansion
        """
        return type(self)(
            self.coefficients if coefficients is None else coefficients,
            center=self.center if center is None else center,
            kind=self.kind if kind is None else kind,
            smearing=None if drop_smearing else (self.smearing if smearing is None else smearing)
        )

    # endregion

    # region properties

    @property
    def order(self):
        return self._order

    @property
    def shape(self):
        """the batch shape"""
        return self.coefficients.shape[:-1]

    @property
    def ndim(self):
        return len(self.shape)

    @property
    def is_smeared(self):
        return self.smearing is not None

    @property
    def charge(self):
        """the monopole term(s)"""
        self._require_kind('multipole', 'charge')
        return self.coefficients[..., 0].real

    @property
    def dipole(self):
        """the Cartesian dipole moment(s) about the center(s)"""
        self._require_kind('multipole', 'dipole')
        if self.order < 1:
            return np.zeros(self.shape + (3,))
        return self.to_real()[..., [3, 1, 2]]

    def __getitem__(self, item):
        if not isinstance(item, tuple):
            item = (item,)
        return type(self)(
            self.coefficients[item + (slice(None),)],
            center=self.center[item + (slice(None),)],
            kind=self.kind,
            smearing=None if self.smearing is None else self.smearing[item]
        )

    def __len__(self):
        return self.shape[0]

    def __repr__(self):
        return "{}(kind={!r}, order={}, shape={}{})".format(
            type(self).__name__, self.kind, self.order, self.shape,
            ", smeared" if self.is_smeared else ""
        )

    def _require_kind(self, kind, op):
        if self.kind != kind:
            raise ValueError(f"`{op}` requires a {kind} expansion (this is a {self.kind} expansion)")

    def _require_unsmeared(self, op):
        if self.is_smeared:
            raise ValueError(f"`{op}` would re-expand a smeared expansion; use `drop_smearing` explicitly if a point approximation is intended")

    # endregion

    # region transformations

    def shift(self, new_center):
        """
        Re-expands the same sources about a new center (M2M for multipole expansions, L2L for
        local expansions). Exact for the truncated expansion.

        :param new_center: new center(s), `(..., 3)`
        :type new_center: np.ndarray
        :return: the re-centered expansion
        :rtype: MultipoleExpansion
        """
        self._require_unsmeared('shift')
        new_center = np.asanyarray(new_center, dtype=float)
        disp = new_center - self.center
        if self.kind == 'multipole':
            coeffs = nput.translate_multipoles(self.coefficients, disp)
        else:
            coeffs = nput.translate_local_multipoles(self.coefficients, disp)
        return self.modify(coefficients=coeffs, center=np.broadcast_to(new_center, coeffs.shape[:-1] + (3,)))

    def translate(self, displacement):
        """
        Rigidly moves the sources (and the center) by `displacement`.

        :param displacement: `(..., 3)`
        :type displacement: np.ndarray
        :return: the moved expansion
        :rtype: MultipoleExpansion
        """
        return self.modify(center=self.center + np.asanyarray(displacement, dtype=float))

    def rotate(self, rotation, origin=None):
        """
        Rigidly rotates the sources by `rotation` about `origin` (default: each expansion's own
        center), `x -> Q (x - o) + o`. Improper rotations are allowed.

        :param rotation: orthogonal matrix/matrices, `(..., 3, 3)`
        :type rotation: np.ndarray
        :param origin: rotation origin, `(..., 3)`
        :type origin: np.ndarray | None
        :return: the rotated expansion
        :rtype: MultipoleExpansion
        """
        Q = np.asanyarray(rotation, dtype=float)
        if self.kind == 'multipole':
            coeffs = nput.rotate_multipoles(self.coefficients, Q)
        else:
            coeffs = nput.rotate_local_multipoles(self.coefficients, Q)
        if origin is None:
            center = np.broadcast_to(self.center, coeffs.shape[:-1] + (3,))
        else:
            origin = np.asanyarray(origin, dtype=float)
            center = origin + np.einsum('...ij,...j->...i', Q, self.center - origin)
        return self.modify(coefficients=coeffs, center=center)

    def to_local(self, center, order=None):
        """
        Converts a multipole expansion into a local expansion about `center` (M2L), valid where
        the evaluation region is well separated from the sources.

        :param center: local expansion center(s), `(..., 3)`
        :type center: np.ndarray
        :param order: local expansion order (defaults to this expansion's order)
        :type order: int | None
        :return: the local expansion
        :rtype: MultipoleExpansion
        """
        self._require_kind('multipole', 'to_local')
        self._require_unsmeared('to_local')
        center = np.asanyarray(center, dtype=float)
        coeffs = nput.multipoles_to_local_multipoles(self.coefficients, center - self.center, local_order=order)
        return type(self)(coeffs, center=center, kind='local')

    def truncate(self, order):
        """
        :param order: new (lower) order
        :type order: int
        :return: the expansion truncated at `order`
        :rtype: MultipoleExpansion
        """
        if order > self.order:
            raise ValueError(f"can't truncate an order {self.order} expansion to order {order}")
        return self.modify(coefficients=self.coefficients[..., :(order + 1) * (order + 2) // 2])

    def pad(self, order):
        """
        :param order: new (higher) order
        :type order: int
        :return: the expansion zero-padded to `order` (e.g. before shifting site expansions,
            whose higher moments about a new center are nonzero)
        :rtype: MultipoleExpansion
        """
        if order < self.order:
            raise ValueError(f"can't pad an order {self.order} expansion to order {order}")
        return self.modify(coefficients=self._pad(self.coefficients, order))

    def sum(self, axis=-1, center=None, order=None):
        """
        Collapses a batch axis (e.g. per-atom sites) into one expansion per remaining batch
        element by shifting every term to a common center and adding.

        :param axis: batch axis to reduce
        :type axis: int
        :param center: common center, `(..., 3)` for the reduced batch (default: mean of the centers)
        :type center: np.ndarray | None
        :param order: order of the summed expansion (default: this expansion's order); site moments
            generate higher moments about the common center, so this should usually be raised
        :type order: int | None
        :return: the summed expansion
        :rtype: MultipoleExpansion
        """
        self._require_unsmeared('sum')
        axis = axis % self.ndim
        if center is None:
            center = np.mean(self.center, axis=axis)
        center = np.asanyarray(center, dtype=float)
        base = self if order is None or order == self.order else (
            self.pad(order) if order > self.order else self.truncate(order)
        )
        shifted = base.shift(np.expand_dims(center, axis))
        return type(self)(np.sum(shifted.coefficients, axis=axis), center=center, kind=self.kind)

    def _binary_compat(self, other):
        if not isinstance(other, MultipoleExpansion):
            return NotImplemented
        if other.kind != self.kind:
            raise ValueError("can't combine multipole and local expansions")
        return other

    def __add__(self, other):
        other = self._binary_compat(other)
        if other is NotImplemented:
            return other
        if self.is_smeared or other.is_smeared:
            raise ValueError("smeared expansions can't be combined into a single expansion")
        if not np.allclose(other.center, self.center):
            other = other.shift(self.center)
        L = max(self.order, other.order)
        a = self._pad(self.coefficients, L)
        b = self._pad(other.coefficients, L)
        return type(self)(a + b, center=np.broadcast_to(self.center, np.broadcast_shapes(a.shape, b.shape)[:-1] + (3,)), kind=self.kind)

    @staticmethod
    def _pad(coeffs, L):
        P = (L + 1) * (L + 2) // 2
        if coeffs.shape[-1] == P:
            return coeffs
        out = np.zeros(coeffs.shape[:-1] + (P,), dtype=coeffs.dtype)
        out[..., :coeffs.shape[-1]] = coeffs
        return out

    def __neg__(self):
        return self.modify(coefficients=-self.coefficients)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, scalar):
        scalar = np.asanyarray(scalar)
        if np.iscomplexobj(scalar):
            raise ValueError("expansions can only be scaled by real numbers")
        return self.modify(coefficients=self.coefficients * scalar[..., np.newaxis])

    __rmul__ = __mul__

    # endregion

    # region evaluation

    def evaluate(self, points, deriv_order=0, sum_axis=None):
        """
        Evaluates the potential and optionally its Cartesian derivatives.

        :param points: evaluation points, `(N, 3)` (broadcast against every expansion) or
            `(..., N, 3)` matching the batch shape (with `sum_axis` removed, if given)
        :type points: np.ndarray
        :param deriv_order: number of Cartesian derivatives to return
        :type deriv_order: int
        :param sum_axis: a batch axis to sum the result over (e.g. the site axis of a distributed expansion)
        :type sum_axis: int | None
        :return: `V` with shape `(..., N)` if `deriv_order == 0`, else `[V, dV, d2V, ...]`
        :rtype: np.ndarray | list[np.ndarray]
        """
        points = np.asanyarray(points, dtype=float)
        if sum_axis is not None:
            sum_axis = sum_axis % self.ndim
            if points.ndim > 2:
                if points.ndim - 2 != self.ndim - 1:
                    raise ValueError(
                        f"points batch shape {points.shape[:-2]} doesn't match expansion batch shape {self.shape} "
                        f"with axis {sum_axis} summed"
                    )
                points = np.expand_dims(points, sum_axis)
        if self.kind == 'multipole':
            res = nput.multipole_potential(
                self.coefficients, points, center=self.center,
                deriv_order=deriv_order, smearing=self.smearing
            )
        else:
            res = nput.local_multipole_potential(self.coefficients, points, center=self.center, deriv_order=deriv_order)
        if sum_axis is not None:
            res = np.sum(res, axis=sum_axis) if deriv_order == 0 else [np.sum(r, axis=sum_axis) for r in res]
        return res

    def density(self, points, sum_axis=None):
        """
        Evaluates the smeared density these (multipole) moments describe, which requires
        `smearing`; point multipoles have no finite density.

        :param points: evaluation points, as for `evaluate`
        :type points: np.ndarray
        :param sum_axis: a batch axis to sum the result over (e.g. the site axis)
        :type sum_axis: int | None
        :return: the density, `(..., N)`
        :rtype: np.ndarray
        """
        self._require_kind('multipole', 'density')
        if not self.is_smeared:
            raise ValueError("point multipoles have no finite density; construct the expansion with `smearing`")
        points = np.asanyarray(points, dtype=float)
        if sum_axis is not None:
            sum_axis = sum_axis % self.ndim
            if points.ndim > 2:
                points = np.expand_dims(points, sum_axis)
        res = nput.smeared_multipole_density(self.coefficients, points, center=self.center, smearing=self.smearing)
        if sum_axis is not None:
            res = np.sum(res, axis=sum_axis)
        return res

    def __call__(self, points, deriv_order=0, sum_axis=None):
        return self.evaluate(points, deriv_order=deriv_order, sum_axis=sum_axis)

    def potential(self, points, sum_axis=None):
        """the potential at `points`"""
        return self.evaluate(points, sum_axis=sum_axis)

    def field(self, points, sum_axis=None):
        """the field `-grad V` at `points`, `(..., N, 3)`"""
        return -self.evaluate(points, deriv_order=1, sum_axis=sum_axis)[1]

    def field_gradient(self, points, sum_axis=None):
        """the field gradient `-grad grad V` at `points`, `(..., N, 3, 3)`"""
        return -self.evaluate(points, deriv_order=2, sum_axis=sum_axis)[2]

    def interaction_energy(self, other):
        """
        The interaction energy between the sources of two well-separated multipole expansions,
        `E = sum_lm F_lm conj(M^other_lm)` with `F` the local expansion of `self` about
        `other.center`.

        :param other: the other multipole expansion
        :type other: MultipoleExpansion
        :return: the energy, broadcast over the batch shapes
        :rtype: np.ndarray
        """
        self._require_kind('multipole', 'interaction_energy')
        other._require_kind('multipole', 'interaction_energy')
        local = self.to_local(other.center, order=other.order)
        L = other.order
        m = np.concatenate([np.arange(l + 1) for l in range(L + 1)])
        w = np.where(m == 0, 1., 2.)
        return np.sum(w * local.coefficients * np.conj(other.coefficients), axis=-1).real

    # endregion

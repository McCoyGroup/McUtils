
import numpy as np
from scipy.special import ndtr, ndtri

__all__ = [
    "ConformerEncoder"
]

class ConformerEncoder:
    compressed_bond_range = (0.5, 2.5)
    compressed_angle_range = (0, np.pi - 1e-6)
    compressed_dihedral_range = (0, 2 * np.pi)

    # Distributions are expressed over normalized coordinates [0, 1].
    # angle_distribution = {
    #     "means": (2 / 3,),
    #     "stds": (0.5,),
    # }
    angle_distribution = {}

    # dihedral_distribution = {
    #     "means": (0.0, 0.5, 1.0),
    #     "stds": (0.5, 0.5, 0.5),
    # }
    dihedral_distribution = {}

    distribution_grid_size = 1001
    _inverse_distribution_cache = {}

    @staticmethod
    def _distribution_parameters(distribution):
        """
        Normalize a distribution specification.

        Returns
        -------
        None
            For a uniform distribution.
        tuple[np.ndarray, np.ndarray, np.ndarray]
            Means, standard deviations, and normalized weights for a
            Gaussian mixture.
        """
        if distribution is None or not distribution:
            return None

        means = distribution.get("means")
        weights = distribution.get("weights")

        # No means and no weights indicates a uniform distribution.
        if means is None and weights is None:
            return None

        if means is None:
            raise ValueError(
                "distribution weights were provided without component means"
            )

        means = np.atleast_1d(
            np.asarray(means, dtype=float)
        )

        if means.ndim != 1 or means.size == 0:
            raise ValueError(
                "distribution means must be a nonempty 1D sequence"
            )

        stds = distribution.get("stds")
        if stds is None:
            raise ValueError(
                "distribution stds are required when means are provided"
            )

        stds = np.asarray(stds, dtype=float)

        # Permit a scalar standard deviation for all components.
        if stds.ndim == 0:
            stds = np.full(means.shape, stds.item())
        elif stds.shape != means.shape:
            raise ValueError(
                "distribution stds must be scalar or match means"
            )

        if np.any(stds <= 0):
            raise ValueError(
                "distribution standard deviations must be positive"
            )

        # Omitted weights mean equal component weights.
        if weights is None:
            weights = np.full(means.shape, 1 / means.size)
        else:
            weights = np.asarray(weights, dtype=float)

            if weights.ndim == 0 and means.size == 1:
                weights = weights.reshape(1)

            if weights.shape != means.shape:
                raise ValueError(
                    "distribution weights must match means"
                )

            if np.any(weights < 0) or not np.any(weights > 0):
                raise ValueError(
                    "distribution weights must be nonnegative with "
                    "at least one positive value"
                )

            weights = weights / weights.sum()

        return means, stds, weights

    @classmethod
    def _distribution_cdf(cls, x, distribution=None):
        """
        Evaluate a distribution CDF truncated and normalized to [0, 1].

        A missing or empty distribution specification represents a uniform
        distribution, for which the CDF is the identity.
        """
        x = np.asarray(x, dtype=float)
        parameters = cls._distribution_parameters(distribution)

        if parameters is None:
            return np.clip(x, 0.0, 1.0)

        means, stds, weights = parameters

        lower_cdf = ndtr(-means / stds)
        upper_cdf = ndtr((1 - means) / stds)

        normalization = weights @ (upper_cdf - lower_cdf)

        if normalization <= 0:
            raise ValueError(
                "distribution has no numerically resolvable mass in [0, 1]"
            )

        component_cdfs = ndtr(
            (x[..., np.newaxis] - means) / stds
        )

        result = (
                         (component_cdfs - lower_cdf) @ weights
                 ) / normalization

        return np.clip(result, 0.0, 1.0)

    @classmethod
    def _inverse_distribution_grid(cls, distribution):
        """
        Build and cache an inverse-CDF interpolation grid for a Gaussian
        mixture containing two or more components.
        """
        parameters = cls._distribution_parameters(distribution)

        if parameters is None:
            return (
                np.array([0.0, 1.0]),
                np.array([0.0, 1.0]),
            )

        means, stds, weights = parameters

        if means.size == 1:
            raise ValueError(
                "A single Gaussian uses the direct inverse-CDF path"
            )

        key = (
            tuple(means),
            tuple(stds),
            tuple(weights),
            cls.distribution_grid_size,
        )

        try:
            return cls._inverse_distribution_cache[key]
        except KeyError:
            pass

        positions = np.linspace(
            0.0,
            1.0,
            cls.distribution_grid_size,
        )

        probabilities = cls._distribution_cdf(
            positions,
            distribution,
        )

        probabilities[0] = 0.0
        probabilities[-1] = 1.0

        # Exclude saturated endpoints before removing duplicate CDF values.
        interior = (
                (probabilities > 0.0)
                & (probabilities < 1.0)
        )

        interior_probabilities = probabilities[interior]
        interior_positions = positions[interior]

        if interior_probabilities.size:
            keep = np.concatenate((
                [True],
                np.diff(interior_probabilities) > 0,
            ))

            interior_probabilities = interior_probabilities[keep]
            interior_positions = interior_positions[keep]

        probabilities = np.concatenate((
            [0.0],
            interior_probabilities,
            [1.0],
        ))

        positions = np.concatenate((
            [0.0],
            interior_positions,
            [1.0],
        ))

        result = probabilities, positions
        cls._inverse_distribution_cache[key] = result

        return result

    @classmethod
    def _distribution_ppf(cls, probability, distribution=None):
        """
        Evaluate an inverse CDF on [0, 1].

        Uniform distributions use the identity, single Gaussians use the
        analytic truncated-normal inverse, and mixtures use the cached
        dense interpolation.
        """
        probability = np.asarray(probability, dtype=float)

        if np.any((probability < 0) | (probability > 1)):
            raise ValueError("probabilities must lie in [0, 1]")

        parameters = cls._distribution_parameters(distribution)

        # Uniform distribution: Q(p) = p.
        if parameters is None:
            result = probability.copy()

        else:
            means, stds, weights = parameters

            if means.size == 1:
                # Exact inverse CDF for a Gaussian truncated to [0, 1].
                mean = means[0]
                std = stds[0]

                lower_cdf = ndtr(-mean / std)
                upper_cdf = ndtr((1 - mean) / std)

                untruncated_probability = (
                        lower_cdf
                        + probability * (upper_cdf - lower_cdf)
                )

                result = (
                        mean
                        + std * ndtri(untruncated_probability)
                )

                result = np.clip(result, 0.0, 1.0)

            else:
                probabilities, positions = (
                    cls._inverse_distribution_grid(distribution)
                )

                result = np.interp(
                    probability,
                    probabilities,
                    positions,
                )

        # Ensure exact bounds in every branch.
        result = np.where(probability == 0, 0.0, result)
        result = np.where(probability == 1, 1.0, result)

        return result.item() if result.ndim == 0 else result

    @staticmethod
    def _encoding_types(byte_size):
        if byte_size == 16:
            return np.uint16, np.float16
        if byte_size == 32:
            return np.uint32, np.float32
        if byte_size == 64:
            return np.uint64, np.float64

        raise ValueError(
            f"can't pack into byte size {byte_size}"
        )

    @staticmethod
    def _encoding_limits(byte_size, pack_angles=False):
        full_max = 2**byte_size - 1
        step_max = 2**(byte_size - 1) - 1

        if pack_angles:
            pack_max = 2**(byte_size // 2) - 1
        else:
            pack_max = full_max

        return step_max, pack_max, full_max

    @classmethod
    def bond_encoder(
        cls,
        bonds,
        byte_size,
        primary_bond_range=None,
    ):
        """
        Encode a standalone bond-length stream.
        """
        base_type, float_type = cls._encoding_types(byte_size)
        step_max, _, _ = cls._encoding_limits(byte_size)

        if primary_bond_range is None:
            primary_bond_range = cls.compressed_bond_range

        bonds = np.asanyarray(bonds)
        encoded = np.zeros(bonds.shape, dtype=base_type)

        lower, upper = primary_bond_range
        compressed = (bonds >= lower) & (bonds < upper)

        total_range = upper - lower
        encoded[compressed] = np.round(
            step_max
            * (bonds[compressed] - lower)
            / total_range
        ).astype(base_type)

        # Values outside the primary range are retained in the
        # corresponding floating-point representation.
        raw_values = bonds[~compressed].astype(float_type)
        encoded[~compressed] = (
            raw_values.view(base_type) + step_max
        )

        return encoded

    @classmethod
    def bond_decoder(
        cls,
        encoded_bonds,
        byte_size,
        primary_bond_range=None,
    ):
        """
        Decode a standalone encoded bond-length stream.
        """
        base_type, float_type = cls._encoding_types(byte_size)
        step_max, _, _ = cls._encoding_limits(byte_size)

        if primary_bond_range is None:
            primary_bond_range = cls.compressed_bond_range

        encoded_bonds = np.asarray(
            encoded_bonds,
            dtype=base_type,
        )

        compressed = encoded_bonds < step_max
        bonds = np.zeros(encoded_bonds.shape, dtype=float)

        lower, upper = primary_bond_range
        total_range = upper - lower

        bonds[compressed] = (
            total_range
            * encoded_bonds[compressed]
            / step_max
        ) + lower

        raw_values = (
            encoded_bonds[~compressed] - step_max
        ).astype(base_type)

        bonds[~compressed] = raw_values.view(float_type)

        return bonds

    @classmethod
    def angle_encoder(
        cls,
        angles,
        byte_size,
        angle_range=None,
        pack_angles=False,
    ):
        """
        Encode a standalone angle stream.

        The first angle always uses the full integer width. Remaining
        angles use either the full width or half width depending on
        `pack_angles`.
        """
        base_type, _ = cls._encoding_types(byte_size)
        _, pack_max, full_max = cls._encoding_limits(
            byte_size,
            pack_angles,
        )

        if angle_range is None:
            angle_range = cls.compressed_angle_range

        angles = np.asanyarray(angles)

        normalized = (
            (angles - angle_range[0])
            / (angle_range[1] - angle_range[0])
        )

        quantiles = cls._distribution_cdf(
            normalized,
            cls.angle_distribution,
        )

        encoded = np.empty(angles.shape, dtype=base_type)

        if encoded.size:
            encoded[0] = np.round(
                full_max * quantiles[0]
            ).astype(base_type)

            encoded[1:] = np.round(
                pack_max * quantiles[1:]
            ).astype(base_type)

        return encoded

    @classmethod
    def angle_decoder(
        cls,
        encoded_angles,
        byte_size,
        angle_range=None,
        pack_angles=False,
    ):
        """
        Decode a standalone angle stream.
        """
        base_type, _ = cls._encoding_types(byte_size)
        _, pack_max, full_max = cls._encoding_limits(
            byte_size,
            pack_angles,
        )

        if angle_range is None:
            angle_range = cls.compressed_angle_range

        encoded_angles = np.asarray(
            encoded_angles,
            dtype=base_type,
        )

        quantiles = np.empty(
            encoded_angles.shape,
            dtype=float,
        )

        if quantiles.size:
            quantiles[0] = encoded_angles[0] / full_max
            quantiles[1:] = encoded_angles[1:] / pack_max

        normalized = cls._distribution_ppf(
            quantiles,
            cls.angle_distribution,
        )

        return (
            angle_range[0]
            + (angle_range[1] - angle_range[0])
            * normalized
        )

    @classmethod
    def dihedral_encoder(
        cls,
        dihedrals,
        byte_size,
        dihedral_range=None,
        pack_angles=False,
    ):
        """
        Encode a standalone dihedral stream.
        """
        base_type, _ = cls._encoding_types(byte_size)
        _, pack_max, _ = cls._encoding_limits(
            byte_size,
            pack_angles,
        )

        if dihedral_range is None:
            dihedral_range = cls.compressed_dihedral_range

        dihedrals = np.asanyarray(dihedrals).copy()

        # Convert negative dihedrals into the default [0, 2π) range.
        dihedrals[dihedrals < 0] += 2 * np.pi

        normalized = (
            (dihedrals - dihedral_range[0])
            / (dihedral_range[1] - dihedral_range[0])
        )

        quantiles = cls._distribution_cdf(
            normalized,
            cls.dihedral_distribution,
        )

        return np.round(
            pack_max * quantiles
        ).astype(base_type)

    @classmethod
    def dihedral_decoder(
        cls,
        encoded_dihedrals,
        byte_size,
        dihedral_range=None,
        pack_angles=False,
    ):
        """
        Decode a standalone dihedral stream.
        """
        base_type, _ = cls._encoding_types(byte_size)
        _, pack_max, _ = cls._encoding_limits(
            byte_size,
            pack_angles,
        )

        if dihedral_range is None:
            dihedral_range = cls.compressed_dihedral_range

        encoded_dihedrals = np.asarray(
            encoded_dihedrals,
            dtype=base_type,
        )

        quantiles = encoded_dihedrals / pack_max

        normalized = cls._distribution_ppf(
            quantiles,
            cls.dihedral_distribution,
        )

        dihedrals = (
            dihedral_range[0]
            + (dihedral_range[1] - dihedral_range[0])
            * normalized
        )

        # Restore the original [-π, π] convention.
        dihedrals[dihedrals > np.pi] -= 2 * np.pi

        return dihedrals

    @staticmethod
    def _split_coordinate_streams(flat_z):
        """
        Split a flattened Z-matrix into bond, angle, and dihedral streams.
        """
        flat_z = np.asanyarray(flat_z)

        bonds = np.concatenate((
            flat_z[:2],
            flat_z[3::3],
        ))

        angles = np.concatenate((
            flat_z[[2]],
            flat_z[4::3],
        ))

        dihedrals = flat_z[5::3]

        return bonds, angles, dihedrals

    @staticmethod
    def _merge_coordinate_streams(
        bonds,
        angles,
        dihedrals,
    ):
        """
        Reconstruct a flattened Z-matrix from separate coordinate streams.
        """
        flat_z = np.empty(
            3 * (len(bonds) - 1),
            dtype=float,
        )

        flat_z[:2] = bonds[:2]
        flat_z[2] = angles[0]
        flat_z[3::3] = bonds[2:]
        flat_z[4::3] = angles[1:]
        flat_z[5::3] = dihedrals

        return flat_z

    @classmethod
    def encode(
            cls,
            flat_z,
            byte_size,
            primary_bond_range=None,
            angle_range=None,
            dihedral_range=None,
            pack_angles=False,
    ):
        """
        Encode a flattened Z-matrix coordinate stream.
        """
        base_type, _ = cls._encoding_types(byte_size)

        bonds, angles, dihedrals = (
            cls._split_coordinate_streams(flat_z)
        )

        encoded_bonds = cls.bond_encoder(
            bonds,
            byte_size,
            primary_bond_range=primary_bond_range,
        )

        encoded_angles = cls.angle_encoder(
            angles,
            byte_size,
            angle_range=angle_range,
            pack_angles=pack_angles,
        )

        encoded_dihedrals = cls.dihedral_encoder(
            dihedrals,
            byte_size,
            dihedral_range=dihedral_range,
            pack_angles=pack_angles,
        )

        if pack_angles:
            encoded = np.zeros(
                len(bonds) + len(angles),
                dtype=base_type,
            )

            encoded[:2] = encoded_bonds[:2]
            encoded[2] = encoded_angles[0]
            encoded[3::2] = encoded_bonds[2:]

            half_width = byte_size // 2

            encoded[4::2] = (
                                    encoded_angles[1:] << half_width
                            ) | encoded_dihedrals

        else:
            encoded = np.zeros(
                len(flat_z),
                dtype=base_type,
            )

            encoded[:2] = encoded_bonds[:2]
            encoded[2] = encoded_angles[0]
            encoded[3::3] = encoded_bonds[2:]
            encoded[4::3] = encoded_angles[1:]
            encoded[5::3] = encoded_dihedrals

        return encoded

    @classmethod
    def _split_encoded_streams(
            cls,
            uint_stream,
            byte_size,
            pack_angles=False,
    ):
        """
        Split the encoded buffer into bond, angle, and dihedral streams.
        """
        if pack_angles:
            half_width = byte_size // 2
            half_mask = 2 ** half_width - 1

            bonds = np.concatenate((
                uint_stream[:2],
                uint_stream[3::2],
            ))

            packed_angles = uint_stream[4::2]

            angles = np.concatenate((
                uint_stream[[2]],
                packed_angles >> half_width,
            ))

            dihedrals = packed_angles & half_mask

        else:
            bonds = np.concatenate((
                uint_stream[:2],
                uint_stream[3::3],
            ))

            angles = np.concatenate((
                uint_stream[[2]],
                uint_stream[4::3],
            ))

            dihedrals = uint_stream[5::3]

        return bonds, angles, dihedrals

    @classmethod
    def decode(
        cls,
        buffer,
        byte_size,
        primary_bond_range=None,
        angle_range=None,
        dihedral_range=None,
        pack_angles=False,
    ):
        """
        Decode a packed flattened Z-matrix coordinate stream.
        """
        base_type, _ = cls._encoding_types(byte_size)
        uint_stream = np.frombuffer(buffer, dtype=base_type)

        encoded_bonds, encoded_angles, encoded_dihedrals = (
            cls._split_encoded_streams(
                uint_stream,
                byte_size,
                pack_angles=pack_angles,
            )
        )

        bonds = cls.bond_decoder(
            encoded_bonds,
            byte_size,
            primary_bond_range=primary_bond_range,
        )

        angles = cls.angle_decoder(
            encoded_angles,
            byte_size,
            angle_range=angle_range,
            pack_angles=pack_angles,
        )

        dihedrals = cls.dihedral_decoder(
            encoded_dihedrals,
            byte_size,
            dihedral_range=dihedral_range,
            pack_angles=pack_angles,
        )

        return cls._merge_coordinate_streams(
            bonds,
            angles,
            dihedrals,
        )
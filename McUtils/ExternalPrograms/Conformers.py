
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

    @classmethod
    def encode(cls, flat_z, byte_size,
               primary_bond_range=None,
               angle_range=None,
               dihedral_range=None,
               pack_angles=False):
        """
        Compress distances such that if they are between 1 and 2 angstroms, we get
        an extra digit of precision
        :param flat_z:
        :param dtype:
        :return:
        """
        if byte_size == 16:
            base_type = np.uint16
            float_type = np.float16
            if pack_angles:
                pack_type = np.uint8
            else:
                pack_type = np.uint16
        elif byte_size == 32:
            base_type = np.uint32
            float_type = np.float32
            if pack_angles:
                pack_type = np.uint16
            else:
                pack_type = np.uint32
        elif byte_size == 64:
            base_type = np.uint64
            float_type = np.float64
            if pack_angles:
                pack_type = np.uint32
            else:
                pack_type = np.uint64
        else:
            raise ValueError(f"can't pack into byte size {byte_size}")

        if primary_bond_range is None:
            primary_bond_range = cls.compressed_bond_range
        if angle_range is None:
            angle_range = cls.compressed_angle_range
        if dihedral_range is None:
            dihedral_range = cls.compressed_dihedral_range

        flat_z = np.asanyarray(flat_z)
        dists = np.concatenate([flat_z[:2], flat_z[3::3]])
        compressed = (dists >= primary_bond_range[0]) & (dists < primary_bond_range[1])
        comp_vals = dists[compressed]

        step_max = 2 ** (byte_size - 1) - 1
        total_bond_range = primary_bond_range[1] - primary_bond_range[0]
        comp_vals = np.round(step_max * (comp_vals - primary_bond_range[0]) / total_bond_range).astype(base_type)
        packaged_dists = np.zeros(len(dists), dtype=base_type)
        packaged_dists[compressed] = comp_vals
        # takes advantage of the fact that we are never negative to use that
        # bit for this encoding
        dx = dists[~compressed].astype(float_type)
        packaged_dists[~compressed] = dx.view(base_type) + step_max

        full_max = 2 ** byte_size - 1
        if pack_angles:
            pack_max = 2 ** (byte_size // 2) - 1
        else:
            pack_max = full_max
        angles = np.concatenate([
            flat_z[[2]],
            flat_z[4::3],
        ])

        normalized_angles = (
                (angles - angle_range[0])
                / (angle_range[1] - angle_range[0])
        )
        # normalized_angles = np.clip(normalized_angles, 0.0, 1.0)

        # Map physical positions into uniform CDF quantiles.
        angle_quantiles = cls._distribution_cdf(
            normalized_angles,
            cls.angle_distribution,
        )

        first_angle = np.round(
            full_max * angle_quantiles[0]
        ).astype(base_type)

        scaled_angles = np.round(
            pack_max * angle_quantiles[1:]
        ).astype(base_type)

        dihedrals = flat_z[5::3].copy()

        # Preserve the existing conversion of negative dihedrals into [0, 2π).
        dihedrals[dihedrals < 0] += 2 * np.pi

        normalized_dihedrals = (
                (dihedrals - dihedral_range[0])
                / (dihedral_range[1] - dihedral_range[0])
        )
        # normalized_dihedrals = np.clip(normalized_dihedrals, 0.0, 1.0)

        dihedral_quantiles = cls._distribution_cdf(
            normalized_dihedrals,
            cls.dihedral_distribution,
        )

        scaled_dihedrals = np.round(
            pack_max * dihedral_quantiles
        ).astype(base_type)

        if pack_angles:
            full_pack = np.zeros(len(dists) + len(angles), dtype=base_type)
        else:
            full_pack = np.zeros(len(flat_z), dtype=base_type)

        full_pack[:2] = packaged_dists[:2]
        full_pack[2] = first_angle

        packaged_angles = np.zeros(len(angles), dtype=base_type)
        if pack_angles:
            full_pack[3::2] = packaged_dists[2:]
            packaged_angles[1:] = (scaled_angles << (byte_size // 2) | scaled_dihedrals)
            full_pack[4::2] = packaged_angles[1:]
        else:
            full_pack[3::3] = packaged_dists[2:]
            full_pack[4::3] = scaled_angles
            full_pack[5::3] = scaled_dihedrals

        return full_pack

    @classmethod
    def decode(cls, buffer, byte_size,
               primary_bond_range=None,
               angle_range=None,
               dihedral_range=None, pack_angles=False):
        """
        Compress distances such that if they are between 1 and 2 angstroms, we get
        an extra digit of precision
        :param flat_z:
        :param dtype:
        :return:
        """
        if byte_size == 16:
            base_type = np.uint16
            float_type = np.float16
            if pack_angles:
                pack_type = np.uint8
            else:
                pack_type = np.uint16
        elif byte_size == 32:
            base_type = np.uint32
            float_type = np.float32
            if pack_angles:
                pack_type = np.uint16
            else:
                pack_type = np.uint32
        elif byte_size == 64:
            base_type = np.uint64
            float_type = np.float64
            if pack_angles:
                pack_type = np.uint32
            else:
                pack_type = np.uint64
        else:
            raise ValueError(f"can't pack into byte size {byte_size}")

        uint_stream = np.frombuffer(buffer, base_type)
        if pack_angles:
            dists = np.concatenate([uint_stream[:2], uint_stream[3::2]])
        else:
            dists = np.concatenate([uint_stream[:2], uint_stream[3::3]])

        if primary_bond_range is None:
            primary_bond_range = cls.compressed_bond_range
        if angle_range is None:
            angle_range = cls.compressed_angle_range
        if dihedral_range is None:
            dihedral_range = cls.compressed_dihedral_range

        step_max = 2 ** (byte_size - 1) - 1
        compressed = dists < step_max
        decompressed_dists = np.zeros(len(dists), dtype=float)

        total_bond_range = primary_bond_range[1] - primary_bond_range[0]
        decompressed_dists[compressed] = (total_bond_range *  dists[compressed] / step_max) + primary_bond_range[0]
        decompressed_dists[~compressed] = (dists[~compressed] - step_max).view(float_type)

        full_max = 2 ** byte_size - 1
        if pack_angles:
            pack_max = 2 ** (byte_size // 2) - 1
        else:
            pack_max = full_max

        if pack_angles:
            full_pack = np.zeros(3*(len(dists) - 1) , dtype=float)
            packed_angles = np.concatenate([uint_stream[[2],], uint_stream[4::2]])
            angles = np.concatenate([packed_angles[[0],], packed_angles[1:] >> (byte_size // 2)])
            dihedrals = packed_angles[1:] & (2**(byte_size // 2) - 1)
        else:
            full_pack = np.zeros(len(uint_stream) , dtype=float)
            angles = np.concatenate([uint_stream[[2],], uint_stream[4::3]])
            dihedrals = uint_stream[5::3]

        angle_quantiles = np.concatenate([
            angles[:1] / full_max,
            angles[1:] / pack_max,
        ])

        normalized_angles = cls._distribution_ppf(
            angle_quantiles,
            cls.angle_distribution,
        )

        full_angles = (
                angle_range[0]
                + (angle_range[1] - angle_range[0]) * normalized_angles
        )

        dihedral_quantiles = dihedrals / pack_max

        normalized_dihedrals = cls._distribution_ppf(
            dihedral_quantiles,
            cls.dihedral_distribution,
        )

        full_dihedrals = (
                dihedral_range[0]
                + (
                        dihedral_range[1] - dihedral_range[0]
                ) * normalized_dihedrals
        )
        full_dihedrals[full_dihedrals > np.pi] -= 2 * np.pi

        full_pack[:2] = decompressed_dists[:2]
        full_pack[2] = full_angles[0]
        full_pack[3::3] = decompressed_dists[2:]
        full_pack[4::3] = full_angles[1:]
        full_pack[5::3] = full_dihedrals

        return full_pack
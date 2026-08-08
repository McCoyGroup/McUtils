
import numpy as np

__all__ = [
    "ConformerEncoder",
]


class DistributionDataEncoder:
    def __init__(self, data_range, byte_size=None, distribution=None, assume_in_range=False):
        self.data_range = data_range
        self.distribution = distribution
        self._cdf_bounds = None
        self._quantiles = None
        self.assume_in_range = assume_in_range
        self.byte_size = byte_size
        self.base_type, self.float_type = self._encoding_types(byte_size)
        self.encoding_limits = self._encoding_limits(byte_size, pack_angles=True)

    @classmethod
    def _truncated_cdf_bounds(cls, distribution, data_range):
        lower, upper = data_range
        if distribution is None:
            return lower, upper, (upper - lower)
        cdf_lower = float(distribution.cdf(np.asarray([lower]))[0])
        cdf_upper = float(distribution.cdf(np.asarray([upper]))[0])
        return cdf_lower, cdf_upper, (cdf_upper - cdf_lower)

    @classmethod
    def _truncated_quantiles(cls, values, distribution, cdf_bounds):
        cdf_lower, _, cdf_span = cdf_bounds
        raw = values if distribution is None else distribution.cdf(values)
        return (raw - cdf_lower) / cdf_span

    @classmethod
    def _untruncate_quantiles(cls, quantiles, distribution, cdf_bounds):
        cdf_lower, _, cdf_span = cdf_bounds
        rescaled = cdf_lower + quantiles * cdf_span
        return rescaled if distribution is None else distribution.ppf(rescaled)

    @property
    def cdf_bounds(self):
        if self._cdf_bounds is None:
            self._cdf_bounds = self._truncated_cdf_bounds(self.distribution, self.data_range)
        return self._cdf_bounds

    def quantiles(self, values):
        return self._truncated_quantiles(values, self.distribution, self.cdf_bounds)

    def data_values(self, quantiles):
        return self._untruncate_quantiles(quantiles, self.distribution, self.cdf_bounds)

    @staticmethod
    def _encoding_types(byte_size):
        if byte_size == 16:
            return np.uint16, np.float16
        if byte_size == 32:
            return np.uint32, np.float32
        if byte_size == 64:
            return np.uint64, np.float64
        raise ValueError(f"can't pack into byte size {byte_size}")

    @staticmethod
    def _encoding_limits(byte_size, pack_angles=False):
        full_max = 2**byte_size - 1
        step_max = 2**(byte_size - 1) - 1
        if pack_angles:
            pack_max = 2**(byte_size // 2) - 1
        else:
            pack_max = full_max
        return step_max, pack_max, full_max

    def encode(self, data, packing_offset=-1):
        base_type, float_type = self.base_type, self.float_type
        step_max, pack_max, full_max = self.encoding_limits

        data = np.asanyarray(data)

        if self.assume_in_range:
            quantiles = self.quantiles(data)
            if packing_offset < 0:
                quant_max = full_max
            elif packing_offset == 0:
                quant_max = pack_max
            else:
                position = np.arange(data.shape[0])
                quant_max = np.where(position < packing_offset, full_max, pack_max)
            return np.round(quant_max * quantiles).astype(base_type)
        else:
            lower, upper = self.data_range
            encoded = np.zeros(data.shape, dtype=base_type)
            in_range = (data >= lower) & (data < upper)

            quantiles = self.quantiles(data[in_range])
            encoded[in_range] = np.round(step_max * quantiles).astype(base_type)

            raw_values = data[~in_range].astype(float_type)
            encoded[~in_range] = raw_values.view(base_type) + step_max

            return encoded

    def decode(self, encoded_data, packing_offset=-1):
        base_type, float_type = self.base_type, self.float_type
        step_max, pack_max, full_max = self.encoding_limits

        encoded_data = np.asarray(encoded_data, dtype=base_type)

        if self.assume_in_range:
            if packing_offset < 0:
                quant_max = full_max
            elif packing_offset == 0:
                quant_max = pack_max
            else:
                position = np.arange(encoded_data.shape[0])
                quant_max = np.where(position < packing_offset, full_max, pack_max)
            quantiles = encoded_data / quant_max
            return self.data_values(quantiles)
        else:
            in_range = encoded_data < step_max
            data = np.zeros(encoded_data.shape, dtype=float)

            quantiles = encoded_data[in_range] / step_max
            data[in_range] = self.data_values(quantiles)

            raw_values = (encoded_data[~in_range] - step_max).astype(base_type)
            data[~in_range] = raw_values.view(float_type)

            return data


class DataStreamPacker:
    @staticmethod
    def _pack_streams(values_list, pack_offsets, dtype):
        packed = np.zeros(values_list[0].shape, dtype=dtype)
        for values, offset in zip(values_list, pack_offsets):
            packed |= (values.astype(dtype) << np.array(offset, dtype=dtype))
        return packed

    @staticmethod
    def _unpack_streams(packed, pack_offsets, total_bits):
        pack_offsets = np.asarray(pack_offsets)
        order = np.argsort(pack_offsets)
        sorted_offsets = pack_offsets[order]
        boundaries = np.append(sorted_offsets, total_bits)
        widths = np.diff(boundaries)

        unpacked_sorted = []
        for offset, width in zip(sorted_offsets, widths):
            mask = (1 << int(width)) - 1
            unpacked_sorted.append((packed >> int(offset)) & mask)

        unpacked = [None] * len(pack_offsets)
        for sorted_idx, orig_idx in enumerate(order):
            unpacked[orig_idx] = unpacked_sorted[sorted_idx]
        return unpacked

    @staticmethod
    def _merge_streams(streams, interleaving_offsets, period, header_lengths=None):
        n = len(streams)
        if header_lengths is None:
            header_lengths = [0] * n

        header_parts = [s[:h] for s, h in zip(streams, header_lengths)]
        header = (
            np.concatenate(header_parts) if any(header_lengths)
            else np.empty(0, dtype=streams[0].dtype)
        )
        remainders = [s[h:] for s, h in zip(streams, header_lengths)]

        total_length = len(header) + sum(len(r) for r in remainders)
        flat = np.empty(total_length, dtype=streams[0].dtype)
        flat[: len(header)] = header

        for remainder, offset in zip(remainders, interleaving_offsets):
            flat[offset::period] = remainder

        return flat

    @staticmethod
    def _split_streams(flat, interleaving_offsets, period, header_lengths=None):
        n = len(interleaving_offsets)
        if header_lengths is None:
            header_lengths = [0] * n

        header = flat[: sum(header_lengths)]

        streams = []
        cursor = 0
        for i in range(n):
            h = header_lengths[i]
            header_part = header[cursor: cursor + h]
            cursor += h
            interleaved_part = flat[interleaving_offsets[i]::period]
            streams.append(np.concatenate([header_part, interleaved_part]))
        return streams


class CoordinateStreamPacker(DataStreamPacker):
    def __init__(self, byte_size=None, bond_header_length=2, angle_header_length=1):
        """
        byte_size : int, optional
            Bit width of the encoded uint streams this packer will see.
            If omitted (None), it's inferred on each call from the given
            stream's own dtype (`array.dtype.itemsize * 8`) instead --
            no need to know it up front. If given, it's still checked
            against that same inference wherever a stream is available,
            so a mismatch (e.g. handing a uint16 stream to a packer
            configured for 32 bits) raises immediately instead of
            silently producing wrong bit-shifts.
        """
        self.byte_size = byte_size
        self.header_lengths = [bond_header_length, angle_header_length, 0]
        offset = bond_header_length + angle_header_length
        self.interleaving_offsets = [offset, offset + 1, offset + 2]

    def _resolve_byte_size(self, array):
        """Infer bit width from `array`'s dtype, guarding it against
        `self.byte_size` when that was explicitly set."""
        inferred = array.dtype.itemsize * 8
        if self.byte_size is None:
            return inferred
        if self.byte_size != inferred:
            raise ValueError(
                f"byte_size mismatch: packer configured for "
                f"{self.byte_size} bits, but the given stream's dtype "
                f"({array.dtype}) implies {inferred} bits."
            )
        return self.byte_size

    def interleave_coordinate_streams(self, bonds, angles, dihedrals):
        return self._merge_streams(
            streams=[bonds, angles, dihedrals],
            interleaving_offsets=self.interleaving_offsets,
            period=3,
            header_lengths=self.header_lengths,
        )

    def split_interleaved_streams(self, flat_z):
        flat_z = np.asanyarray(flat_z)
        bonds, angles, dihedrals = self._split_streams(
            flat_z,
            interleaving_offsets=self.interleaving_offsets,
            period=3,
            header_lengths=self.header_lengths,
        )
        return bonds, angles, dihedrals

    def unpack_coordinate_streams(self, uint_stream, pack_angles=False):
        if pack_angles:
            byte_size = self._resolve_byte_size(uint_stream)
            half_width = byte_size // 2

            bonds, angle_or_packed = self._split_streams(
                uint_stream,
                interleaving_offsets=self.interleaving_offsets[:2],
                period=2,
                header_lengths=self.header_lengths[:2],
            )

            header_angle = angle_or_packed[:1]
            packed_angles = angle_or_packed[1:]

            angle_high, dihedral_low = self._unpack_streams(
                packed_angles,
                pack_offsets=[half_width, 0],
                total_bits=byte_size,
            )

            angles = np.concatenate([header_angle, angle_high])
            dihedrals = dihedral_low
        else:
            bonds, angles, dihedrals = self.split_interleaved_streams(uint_stream)

        return bonds, angles, dihedrals

    def _merge_encoded_streams(self, bonds, angles, dihedrals, pack_angles=False):
        if pack_angles:
            byte_size = self._resolve_byte_size(bonds)
            half_width = byte_size // 2

            header_angle = angles[: self.header_lengths[1]]
            angle_remainder = angles[self.header_lengths[1]:]
            dihedral_remainder = dihedrals

            packed_angles = self._pack_streams(
                [angle_remainder, dihedral_remainder],
                pack_offsets=[half_width, 0],
                dtype=bonds.dtype,
            )

            angle_or_packed = np.concatenate((header_angle, packed_angles))

            return self._merge_streams(
                streams=[bonds, angle_or_packed],
                interleaving_offsets=self.interleaving_offsets[:2],
                period=2,
                header_lengths=self.header_lengths[:2],
            )
        else:
            return self.interleave_coordinate_streams(bonds, angles, dihedrals)


class ConformerEncoder:
    compressed_bond_range = (0.5, 2.5)
    compressed_angle_range = (0, np.pi - 1e-6)
    compressed_dihedral_range = (0, 2 * np.pi)

    def __init__(
        self,
        byte_size=None,
        bond_encoder=None,
        angle_encoder=None,
        dihedral_encoder=None,
        stream_packer=None,
        primary_bond_range=None,
        angle_range=None,
        dihedral_range=None,
    ):
        """
        Parameters
        ----------
        byte_size : int, optional
            Bit width (16/32/64) used to build whichever of the default
            encoders below aren't overridden, and to interpret buffers
            in `decode`. If omitted (None), it's resolved from the first
            supplied `bond_encoder` / `angle_encoder` / `dihedral_encoder`
            / `stream_packer` that exposes its own `.byte_size`. If none
            of those are supplied either, there's nothing to build the
            defaults from, so construction raises immediately rather
            than failing later with a confusing error. `decode` can
            still work even with `byte_size=None` here, by inferring bit
            width directly from a typed buffer at call time -- see
            `decode`.
        ... (see previous docstring for the rest of the parameters)
        """
        if byte_size is None:
            for candidate in (bond_encoder, angle_encoder, dihedral_encoder, stream_packer):
                inferred = getattr(candidate, "byte_size", None)
                if inferred is not None:
                    byte_size = inferred
                    break

        need_defaults = any(
            e is None for e in (bond_encoder, angle_encoder, dihedral_encoder, stream_packer)
        )
        if byte_size is None and need_defaults:
            raise ValueError(
                "byte_size was not given and could not be inferred from "
                "any supplied bond_encoder/angle_encoder/dihedral_encoder/"
                "stream_packer, but at least one of those wasn't supplied "
                "and would need byte_size to build a default. Pass "
                "byte_size explicitly, or supply all four pre-built."
            )

        self.byte_size = byte_size
        if byte_size is not None:
            self.base_type, self.float_type = DistributionDataEncoder._encoding_types(byte_size)
        else:
            # All four were supplied (need_defaults is False), so nothing
            # here needs byte_size directly; base_type stays unresolved
            # until decode() sees an actual typed buffer to infer it from.
            self.base_type, self.float_type = None, None

        self.primary_bond_range = primary_bond_range or self.compressed_bond_range
        self.angle_range = angle_range or self.compressed_angle_range
        self.dihedral_range = dihedral_range or self.compressed_dihedral_range

        self.bond_encoder = bond_encoder or DistributionDataEncoder(
            data_range=self.primary_bond_range,
            byte_size=byte_size,
            distribution=None,
            assume_in_range=False,
        )
        self.angle_encoder = angle_encoder or DistributionDataEncoder(
            data_range=self.angle_range,
            byte_size=byte_size,
            distribution=None,
            assume_in_range=True,
        )
        self.dihedral_encoder = dihedral_encoder or DistributionDataEncoder(
            data_range=self.dihedral_range,
            byte_size=byte_size,
            distribution=None,
            assume_in_range=True,
        )

        self.stream_packer = stream_packer or CoordinateStreamPacker(byte_size=byte_size)

    def encode(self, flat_z, pack_angles=False):
        """
        Encode a flattened Z-matrix coordinate stream.
        """
        bonds, angles, dihedrals = self.stream_packer.split_interleaved_streams(flat_z)

        # Dihedral wraparound: [-pi, pi] -> [0, 2*pi), a presentation
        # convention DistributionDataEncoder itself knows nothing about.
        dihedrals = np.asanyarray(dihedrals).copy()
        dihedrals[dihedrals < 0] += 2 * np.pi

        encoded_bonds = self.bond_encoder.encode(bonds)

        angle_header = self.stream_packer.header_lengths[1]
        encoded_angles = self.angle_encoder.encode(
            angles,
            packing_offset=(angle_header if pack_angles else -1),
        )

        # Dihedral has no full-width header element (unlike angle) --
        # matches the old dihedral_encoder, which always used pack_max
        # uniformly for every element.
        encoded_dihedrals = self.dihedral_encoder.encode(
            dihedrals,
            packing_offset=(0 if pack_angles else -1),
        )

        return self.stream_packer._merge_encoded_streams(
            encoded_bonds,
            encoded_angles,
            encoded_dihedrals,
            pack_angles=pack_angles,
        )

    def _resolve_decode_base_type(self, buffer):
        """
        Determine the dtype to interpret `buffer` as. If `buffer` is
        already a typed numpy array, its dtype's bit width is inferred
        directly; if `self.byte_size` was also set, that inference is
        checked against it (a cheap guard against e.g. accidentally
        decoding a 16-bit stream with a 32-bit-configured encoder) rather
        than silently trusting whichever one happens to be used. If
        `self.byte_size` is None, the inferred dtype is used directly --
        this is what lets `ConformerEncoder(byte_size=None, ...)` still
        decode, as long as `buffer` carries its own dtype.
        """
        if isinstance(buffer, np.ndarray):
            inferred_byte_size = buffer.dtype.itemsize * 8
            if self.byte_size is not None and inferred_byte_size != self.byte_size:
                raise ValueError(
                    f"byte_size mismatch: this ConformerEncoder is "
                    f"configured for {self.byte_size} bits, but the given "
                    f"buffer's dtype ({buffer.dtype}) implies "
                    f"{inferred_byte_size} bits."
                )
            return buffer.dtype.type

        if self.byte_size is None:
            raise ValueError(
                "byte_size was not set at construction and could not be "
                "inferred (`buffer` is raw bytes, not a typed numpy "
                "array). Pass byte_size explicitly at construction, or "
                "pass `buffer` as a numpy array with a concrete dtype."
            )
        return self.base_type

    def decode(self, buffer, pack_angles=False):
        """
        Decode a packed flattened Z-matrix coordinate stream.
        """
        base_type = self._resolve_decode_base_type(buffer)
        uint_stream = (
            buffer.astype(base_type, copy=False)
            if isinstance(buffer, np.ndarray)
            else np.frombuffer(buffer, dtype=base_type)
        )

        encoded_bonds, encoded_angles, encoded_dihedrals = (
            self.stream_packer.unpack_coordinate_streams(
                uint_stream,
                pack_angles=pack_angles,
            )
        )

        bonds = self.bond_encoder.decode(encoded_bonds)

        angle_header = self.stream_packer.header_lengths[1]
        angles = self.angle_encoder.decode(
            encoded_angles,
            packing_offset=(angle_header if pack_angles else -1),
        )

        dihedrals = self.dihedral_encoder.decode(
            encoded_dihedrals,
            packing_offset=(0 if pack_angles else -1),
        )

        # Restore the [-pi, pi] convention.
        dihedrals = np.where(dihedrals > np.pi, dihedrals - 2 * np.pi, dihedrals)

        return self.stream_packer.interleave_coordinate_streams(bonds, angles, dihedrals)
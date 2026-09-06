
import numpy as np
import scipy
import itertools
from typing import NamedTuple, Optional

from .. import Devutils as dev
from .. import Iterators as itut
from .. import Numputils as nput
from ..Zachary import MixtureDistribution

__all__ = [
    "ConformerEncoder",
    "BondPatcher",
    "prune_conformers_by_rmsd",
    "generate_conformer_ensemble"
]

_SOURCE_FLOAT_DTYPES = {32: np.float32, 64: np.float64}
_SOURCE_UINT_DTYPES  = {32: np.uint32,  64: np.uint64}
def max_exp_field_of(exp_bits):
    return (1 << exp_bits) - 1

IEEE754_PARAMS = {
    2:  dict(exp_bits=5,  mant_bits=10),   # half
    4:  dict(exp_bits=8,  mant_bits=23),   # single
    8:  dict(exp_bits=11, mant_bits=52),   # double
}
def make_ufloat_codec(total_bits, exp_bits, reserved_bits=0, source_bits=None):
    """
    Build pack/unpack functions for a custom unsigned-float format:
    - exp_bits bits of exponent (IEEE-style bias)
    - (total_bits - exp_bits - reserved_bits) bits of mantissa (implicit leading 1)
    - no sign bit (values must be >= 0)
    - reserved_bits: top bits of the container left as 0 / free for external
      use (e.g. a type tag). Taken out of the mantissa, not the exponent.

    source_bits: precision to do the intermediate math in (32 or 64).
    Auto-picked to be the smallest that can hold the requested mantissa
    if not given.
    """
    mant_bits = total_bits - exp_bits - reserved_bits
    if mant_bits < 1:
        raise ValueError("Not enough bits left for a mantissa after "
                          "exponent and reserved bits")

    if source_bits is None:
        source_bits = 32 if mant_bits <= 23 else 64
    if mant_bits > {32: 23, 64: 52}[source_bits]:
        raise ValueError(f"mant_bits={mant_bits} exceeds float{source_bits}'s "
                          f"{ {32: 23, 64: 52}[source_bits] }-bit mantissa")

    src_float = _SOURCE_FLOAT_DTYPES[source_bits]
    src_uint = _SOURCE_UINT_DTYPES[source_bits]
    src_exp_bits = {32: 8, 64: 11}[source_bits]
    src_mant_bits = {32: 23, 64: 52}[source_bits]
    src_bias = (1 << (src_exp_bits - 1)) - 1

    bias = (1 << (exp_bits - 1)) - 1
    max_exp_field = (1 << exp_bits) - 1
    shift = src_mant_bits - mant_bits
    usable_bits = total_bits - reserved_bits   # exponent + mantissa span
    usable_mask = (1 << usable_bits) - 1       # masks off any caller-set tag bits

    # container is sized by the *nominal* total_bits, so reserved bits
    # still physically live in the same word (e.g. uint16 for total_bits=16)
    for container in (np.uint8, np.uint16, np.uint32, np.uint64):
        if total_bits <= np.dtype(container).itemsize * 8:
            break
    else:
        raise ValueError("total_bits too large")

    def to_ufloat(x):
        x = np.asarray(x, dtype=src_float)
        if np.any(x < 0):
            raise ValueError("ufloat requires non-negative values")

        bits = x.view(src_uint)
        exp_src = ((bits >> src_mant_bits) & ((1 << src_exp_bits) - 1)).astype(np.int64)
        mant_src = (bits & ((1 << src_mant_bits) - 1)).astype(np.int64)

        exp_new = exp_src - src_bias + bias

        if shift > 0:
            mant_new = (mant_src + (1 << (shift - 1))) >> shift
            carry = mant_new >> mant_bits
            exp_new += carry
            mant_new &= (1 << mant_bits) - 1
        else:
            mant_new = mant_src << (-shift)

        exp_new = np.where(exp_new >= max_exp_field, max_exp_field, exp_new)
        exp_new = np.where(exp_new <= 0, 0, exp_new)
        mant_new = np.where(exp_new == 0, 0, mant_new)

        # top reserved_bits are 0 by construction: max possible value here
        # is (2^exp_bits - 1) << mant_bits | (2^mant_bits - 1) == 2^usable_bits - 1
        out = (exp_new.astype(container) << mant_bits) | mant_new.astype(container)
        return out.astype(container)

    def from_ufloat(bits):
        bits = np.asarray(bits, dtype=container) & container(usable_mask)  # strip any tag
        exp_field = (bits >> mant_bits) & max_exp_field
        mant_field = bits & ((1 << mant_bits) - 1)

        exp_src = exp_field.astype(np.int64) - bias + src_bias
        mant_src = mant_field.astype(np.int64) << shift

        out_bits = (exp_src.astype(src_uint) << src_mant_bits) | mant_src.astype(src_uint)
        return out_bits.view(src_float)

    sig_bits = mant_bits + 1
    info = {
        "total_bits": total_bits,
        "exp_bits": exp_bits,
        "mant_bits": mant_bits,
        "reserved_bits": reserved_bits,
        "usable_bits": usable_bits,
        "tag_shift": usable_bits,        # caller: tagged = packed | (tag << tag_shift)
        "bias": bias,
        "container_dtype": container,
        "source_dtype": src_float,
        "sig_decimal_digits": sig_bits * np.log10(2),
        "machine_eps": 2.0 ** -sig_bits,
    }
    return to_ufloat, from_ufloat, info


def ieee_ufloat_codec(byte_size, reserved_bits=0):
    if byte_size not in IEEE754_PARAMS:
        raise ValueError(f"No IEEE 754 standard format for {byte_size} bytes; "
                          f"supported: {sorted(IEEE754_PARAMS)}")
    params = IEEE754_PARAMS[byte_size]
    total_bits = byte_size * 8
    target_mant_bits = total_bits - params["exp_bits"] - reserved_bits

    if target_mant_bits <= 23:
        source_bits = 32
    elif target_mant_bits <= 52:
        source_bits = 64
    else:
        raise ValueError(f"needs {target_mant_bits} mantissa bits; no safe source")

    return make_ufloat_codec(total_bits=total_bits,
                              exp_bits=params["exp_bits"],
                              reserved_bits=reserved_bits,
                              source_bits=source_bits)

codec_cache = {}
def ufloat_converters(bit_size, reserved_bits=0, cache=None):
    if cache is None: cache = codec_cache
    if (bit_size, reserved_bits) not in codec_cache:
        codec_cache[(bit_size, reserved_bits)] = ieee_ufloat_codec(bit_size // 8, reserved_bits=reserved_bits)
    return codec_cache[(bit_size, reserved_bits)]

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
        self._initialized = False

    def initialize(self):
        if not self._initialized:
            self._initialized = True
            self._initialize_distribution_ppf()

    def _initialize_distribution_ppf(self):
        # Periodic distributions need their unwrapped-CDF/PPF grid built
        # at higher resolution than the library default: the "cut point"
        # chosen for unwrapping a circle onto a line can sit right next
        # to a real density mode (the same physical peak then contributes
        # steep CDF rise on *both* sides of the cut), and a coarse grid
        # resolves that badly right at the seam. Pre-warming here with a
        # finer grid once, at construction, avoids paying for that
        # resolution repeatedly on every encode/decode call.
        if getattr(self.distribution, "periodic", False):
            self.distribution.ppf(np.array([0.5]), grid_size=20_000)

    @classmethod
    def _truncated_cdf_bounds(cls, distribution, data_range):
        """
        (cdf_lower, cdf_upper, cdf_span) for rescaling `distribution`'s
        CDF so that the portion of its mass inside `data_range` maps onto
        the *full* [0, 1] quantile range -- i.e. the truncated/conditional
        CDF, not the raw one. `distribution=None` means "uniform on
        data_range," matching the old bond_encoder's plain linear scaling
        exactly (cdf_lower=lower, cdf_upper=upper, so the formula below
        reduces to (x - lower) / (upper - lower)).

        Periodic distributions (e.g. angle/dihedral mixtures) are
        expected to have `data_range` span exactly one full period, in
        which case *all* of the distribution's mass is inside range by
        definition -- no truncation is needed, so bounds are fixed at
        (0, 1, 1) rather than evaluated via `.cdf()`, which is itself
        periodic and would give cdf_lower == cdf_upper (a divide-by-zero)
        for a range spanning a full period.
        """
        lower, upper = data_range
        if distribution is None:
            return lower, upper, (upper - lower)
        if getattr(distribution, "periodic", False):
            return 0.0, 1.0, 1.0
        cdf_lower = float(distribution.cdf(np.asarray([lower]))[0])
        cdf_upper = float(distribution.cdf(np.asarray([upper]))[0])
        return cdf_lower, cdf_upper, (cdf_upper - cdf_lower)

    @classmethod
    def _truncated_quantiles(cls, values, distribution, cdf_bounds):
        """Map raw values -> quantiles in [0, 1] via distribution's CDF,
        truncated to the range implied by `cdf_bounds`. Periodic
        distributions use `unwrapped_cdf` instead of `cdf` -- see
        `_truncated_cdf_bounds` for why the ordinary `cdf` doesn't work
        here for a full-period range."""
        if distribution is not None and getattr(distribution, "periodic", False):
            return distribution.unwrapped_cdf(values)
        cdf_lower, _, cdf_span = cdf_bounds
        raw = values if distribution is None else distribution.cdf(values)
        return (raw - cdf_lower) / cdf_span

    @classmethod
    def _untruncate_quantiles(cls, quantiles, distribution, cdf_bounds):
        """Inverse of `_truncated_quantiles`: quantiles in [0, 1] -> raw
        values, via distribution's PPF, un-truncated from the range
        implied by `cdf_bounds`. For periodic distributions cdf_span=1
        and cdf_lower=0 (see `_truncated_cdf_bounds`), so this reduces to
        a plain `distribution.ppf(quantiles)` call, the exact inverse of
        `unwrapped_cdf`."""
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
        """
        Inverse of `quantiles`: q in [0, 1] -> x in `self.data_range`.

        Clipped to `self.data_range` before returning. This isn't just
        defensive rounding: q in [0, 1] mapping into [lower, upper] is
        the entire definition of truncation, so any excursion outside it
        is never a meaningful answer -- it's a grid-resolution artifact.
        This bites hardest right at q=0/q=1 (or generally whenever
        `distribution.cdf(lower)` isn't genuinely ~0, e.g. a hand-built
        MixtureDistribution with a component whose tail leaks past a
        physical boundary): ppf's grid is spaced uniformly in q, so an
        extreme, rare corner of q-space gets almost no resolution,  and
        interpolating through it can land far outside the valid range
        entirely (see conversation: a component 3.5 std from the
        boundary leaking ~1.9e-5 probability mass past it produced a
        result 27 degrees outside a (0, 180) degree angle range).
        """
        raw = self._untruncate_quantiles(quantiles, self.distribution, self.cdf_bounds)
        if not getattr(self.distribution, "periodic", False):
            lower, upper = self.data_range
            raw = np.clip(raw, lower, upper)
        return raw

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
        self.initialize()

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

    def decode(self, buffer, pack_angles=False, return_streams=False):
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

        return self.decode_from_data(encoded_bonds, encoded_angles, encoded_dihedrals,
                                     pack_angles=pack_angles, return_streams=return_streams)

    def decode_from_data(self, encoded_bonds, encoded_angles, encoded_dihedrals,
                         pack_angles=False, return_streams=False):
        if not return_streams:
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
        else:
            bonds = encoded_bonds
            angles = encoded_angles
            dihedrals = encoded_dihedrals

        return self.stream_packer.interleave_coordinate_streams(bonds, angles, dihedrals)

    @classmethod
    def from_distributions(
        cls,
        byte_size,
        angle_distribution=None,
        dihedral_distribution=None,
        primary_bond_range=None,
        angle_range=None,
        dihedral_range=None,
        bond_encoder=None,
        stream_packer=None,
    ):
        """
        Build a ConformerEncoder whose angle and/or dihedral encoders use
        distributions loaded from saved PPF-grid files -- i.e. `.npz`
        files written by `MixtureDistribution.save_ppf_grid` (after
        fitting a `FittedMixtureDistribution` via `fit_mixture`) -- rather
        than the plain uniform-on-range default.

        Parameters
        ----------
        angle_ppf_path, dihedral_ppf_path : str or os.PathLike, optional
            Paths to `.npz` PPF-grid files. Loaded via
            `MixtureDistribution.load_ppf_grid`, which reconstructs the
            distribution's kernels/params/weights plus its precomputed
            PPF lookup -- no re-fitting needed at load time. If either
            is omitted, that encoder falls back to the usual
            uniform-distribution default (`distribution=None`), exactly
            like the plain constructor.
        bond_encoder : object, optional
            Bonds aren't periodic and don't currently have a saved-file
            path here -- pass a pre-built encoder directly if you want a
            non-uniform bond distribution; otherwise the usual uniform
            default is used.
        (all other parameters as in `__init__`)

        Returns
        -------
        ConformerEncoder
        """
        if isinstance(angle_distribution, str):
            angle_distribution =  MixtureDistribution.load_ppf_grid(angle_distribution)
        if isinstance(dihedral_distribution, str):
            dihedral_distribution =  MixtureDistribution.load_ppf_grid(dihedral_distribution)

        resolved_angle_range = angle_range or cls.compressed_angle_range
        resolved_dihedral_range = dihedral_range or cls.compressed_dihedral_range

        angle_encoder = DistributionDataEncoder(
            data_range=resolved_angle_range,
            byte_size=byte_size,
            distribution=angle_distribution,
            assume_in_range=True,
        )
        dihedral_encoder = DistributionDataEncoder(
            data_range=resolved_dihedral_range,
            byte_size=byte_size,
            distribution=dihedral_distribution,
            assume_in_range=True,
        )

        return cls(
            byte_size=byte_size,
            bond_encoder=bond_encoder,
            angle_encoder=angle_encoder,
            dihedral_encoder=dihedral_encoder,
            stream_packer=stream_packer,
            primary_bond_range=primary_bond_range,
            angle_range=angle_range,
            dihedral_range=dihedral_range,
        )

class BondPatcher:
    # Tunable thresholds for what counts as a "simple" patch vs. a
    # wholesale rearrangement that shouldn't be heuristically patched.
    DEFAULT_MAX_BOND_CHANGES = 4       # absolute cap on # of bonds that differ
    DEFAULT_MAX_BOND_FRACTION = 0.15   # cap as a fraction of total bonds

    @classmethod
    def _get_tagged_bond_types(cls, mol):
        a = mol.atoms
        b = mol.bonds
        return itut.counts(tuple(sorted((a[i], a[j]))) for i, j, _ in b)

    @classmethod
    def _bond_type_differences(cls, mol1, mol2):
        c1 = cls._get_tagged_bond_types(mol1)
        c2 = cls._get_tagged_bond_types(mol2)
        # union of keys, not just c1 — otherwise bond types that appear
        # only in mol2 (e.g. from a rearrangement) are invisible here.
        keys = c1.keys() | c2.keys()
        diffs = {
            k: (c1.get(k, 0) - c2.get(k, 0))
            for k in keys
        }
        return {k: v for k, v in diffs.items() if v != 0}

    @classmethod
    def _is_large_scale_rearrangement(
        cls, mol1, mol2, diffs,
        max_bond_changes=DEFAULT_MAX_BOND_CHANGES,
        max_bond_fraction=DEFAULT_MAX_BOND_FRACTION,
    ):
        """
        Heuristic gate: decide whether the bond-type differences between
        mol1 and mol2 are small/local enough to fix with nearest-atom
        bond patching, or whether they indicate a broad rearrangement
        that patching shouldn't try to touch.
        """
        if not diffs:
            return False

        n_changed = sum(abs(v) for v in diffs.values())
        total_bonds = max(len(mol1.bonds), len(mol2.bonds), 1)

        if n_changed > max_bond_changes:
            return True
        if (n_changed / total_bonds) > max_bond_fraction:
            return True
        return False

    @classmethod
    def _find_bond_fixes_from_diffs(cls, mol2, diffs, allow_bond_formation=False):
        coords2 = mol2.coords
        atom_map = itut.index_groups(mol2.atoms)
        bonds = [b[:2] for b in mol2.bonds]
        new_bonds = []
        dm = nput.distance_matrix(coords2)
        for ti, tj in bonds:
            dm[ti, tj] = dm[tj, ti] = 1000000
        np.fill_diagonal(dm, 1000000)
        for (t1, t2), deficit in diffs.items():
            if deficit < 0:
                if allow_bond_formation:
                    continue
                else:
                    raise ValueError("need to handle bond formation")
            for _ in range(deficit):
                new_pair = cls._find_replacement_candidates(atom_map, dm, t1, t2)
                new_bonds.append(new_pair)
                ii, jj = new_pair
                dm[ii, jj] = 1000000
                dm[jj, ii] = 1000000
        return new_bonds

    @classmethod
    def _find_bond_fixes(cls, mol1, mol2, allow_bond_formation=False):
        # kept for backwards compatibility with any external callers
        diffs = cls._bond_type_differences(mol1, mol2)
        return cls._find_bond_fixes_from_diffs(mol2, diffs, allow_bond_formation=allow_bond_formation)

    @classmethod
    def _find_replacement_candidates(cls, atom_map, dm, t1, t2):
        i = atom_map[t1]
        j = atom_map[t2]
        sub_dm = dm[np.ix_(i, j)]
        min_pos = np.argmin(sub_dm)
        ri, rj = np.unravel_index(min_pos, sub_dm.shape)
        return i[ri], j[rj]

    @classmethod
    def patch_bonds(
            cls, mol1, mol2,
            allow_bond_formation=False,
            max_bond_changes=DEFAULT_MAX_BOND_CHANGES,
            max_bond_fraction=DEFAULT_MAX_BOND_FRACTION,
            raise_on_large_rearrangement=False,
            patch_hydrogens=False,
    ):
        ref_check = mol2.to_smiles(remove_hydrogens=True)
        patch_check = mol1.to_smiles(remove_hydrogens=True)

        if ref_check == patch_check:
            return mol2, True, (ref_check, patch_check)

        diffs = cls._bond_type_differences(mol1, mol2)
        if not patch_hydrogens:
            for k in list(diffs.keys()):
                if "H" in k: diffs.pop(k)

        if cls._is_large_scale_rearrangement(
            mol1, mol2, diffs,
            max_bond_changes=max_bond_changes,
            max_bond_fraction=max_bond_fraction,
        ):
            if raise_on_large_rearrangement:
                raise ValueError(
                    f"bond differences too extensive to patch safely "
                    f"({sum(abs(v) for v in diffs.values())} bond changes); "
                    f"looks like a large-scale rearrangement, not a local error"
                )
            # Don't even attempt the nearest-atom patch heuristic here —
            # it's only reliable for a handful of local bond errors.
            return mol2, False, (ref_check, patch_check)

        new_bonds = cls._find_bond_fixes_from_diffs(
            mol2, diffs, allow_bond_formation=allow_bond_formation
        )
        if len(new_bonds) > 0:
            mol_new = mol2.add_bonds(
                new_bonds,
                sanitize=False,
                adjust_charges=True,
                reguess_bonds=False,
            )
        else:
            mol_new = mol2

        patch_check = mol_new.to_smiles(remove_hydrogens=True, compute_stereo=True)
        return mol_new, ref_check == patch_check, (ref_check, patch_check)


def _pairwise_eckart_rmsd(coords: np.ndarray, masses: np.ndarray) -> np.ndarray:
    """
    The full `MxM` pairwise, mass-weighted RMSD matrix for a stack of `M`
    conformers, via `McUtils.Numputils.eckart_rmsd`: each pair is optimally
    (Eckart) aligned as part of the comparison, so no separate up-front
    embedding step is needed.
    """
    n = len(coords)
    if n <= 1:
        return np.zeros((n, n))
    r, c = np.triu_indices(n, k=1)
    pair_rmsd = nput.eckart_rmsd(coords[r], coords[c], masses=masses, mass_weighted=True)
    rmsds = np.zeros((n, n))
    rmsds[r, c] = pair_rmsd
    rmsds[c, r] = pair_rmsd
    return rmsds


def _rmsd_cluster_representatives(rmsd_matrix: np.ndarray, indices: np.ndarray, rmsd_cutoff: float) -> list:
    """
    Cluster `indices` by thresholding `rmsd_matrix` at `rmsd_cutoff`
    (connected components of the "within cutoff" graph), then pick one
    representative per cluster -- the member with the smallest average
    RMSD to the rest of its cluster. Clusters whose internal spread is
    more than twice the cutoff are recursively re-clustered at half the
    cutoff, so a single loose "chain" of near-duplicates doesn't collapse
    into one representative.
    """
    r, c = np.triu_indices(len(indices), k=1)
    equiv = rmsd_matrix[r, c] < rmsd_cutoff
    graph = np.zeros((len(indices), len(indices)), dtype=bool)
    np.fill_diagonal(graph, True)
    graph[r[equiv], c[equiv]] = True
    graph[c[equiv], r[equiv]] = True
    _, labels = scipy.sparse.csgraph.connected_components(graph, directed=False, return_labels=True)
    _, groups = nput.group_by(np.arange(len(labels)), labels)[0]

    representatives = []
    for g in groups:
        if len(g) == 1:
            representatives.append(g[0])
            continue
        rmsd_block = rmsd_matrix[np.ix_(g, g)]
        rr, cc = np.array(list(itertools.combinations(range(len(g)), 2))).T
        if np.max(rmsd_block[rr, cc]) > 2 * rmsd_cutoff:
            representatives.extend(_rmsd_cluster_representatives(rmsd_block, g, rmsd_cutoff / 2))
        else:
            rep = g[np.argmin(np.average(rmsd_block, axis=0))]
            representatives.append(rep)
    return [indices[r] for r in representatives]


def prune_conformers_by_rmsd(coords, masses=None, rmsd_cutoff: float = .025) -> np.ndarray[int]:
    """
    Deduplicate a list of `Psience.Molecools.Molecule` conformers (same
    connectivity, different geometries) by mass-weighted, Eckart-aligned
    RMSD. No pre-alignment/embedding step is required -- the optimal
    alignment is computed per compared pair by `McUtils.Numputils.eckart_rmsd`.

    :param structs: conformers of a single molecule
    :param rmsd_cutoff: the (per-atom, mass-weighted) RMSD below which two
        conformers are considered duplicates
    :return: one representative `Molecule` per RMSD cluster, in their
        original relative order
    """
    coords = np.asanyarray(coords)
    masses = np.asanyarray(masses)
    rmsds = _pairwise_eckart_rmsd(coords, masses=masses)
    keep = np.sort(_rmsd_cluster_representatives(rmsds, np.arange(len(coords)), rmsd_cutoff))
    return keep


class ConformerRecord(NamedTuple):
    """A single optimized conformer, with enough information to reconstruct or re-optimize it."""
    smiles: str
    atoms: tuple
    coords: np.ndarray
    bonds: list
    energy: Optional[float]
    energy_evaluator: object = None
    optimization_settings: Optional[dict] = None


def _make_conformer_record(struct, energy, smiles, energy_evaluator, optimizer_settings) -> ConformerRecord:
    return ConformerRecord(
        smiles=smiles,
        atoms=struct.atoms,
        coords=struct.coords,
        bonds=[[int(i), int(j), float(t)] for i, j, t in struct.bonds],
        energy=float(energy) if energy is not None else None,
        energy_evaluator=energy_evaluator,
        optimization_settings=optimizer_settings,
    )


default_conformer_generator_options = dict(
    maxAttempts=1000, pruneRmsThresh=0.1, useExpTorsionAnglePrefs=True,
    useBasicKnowledge=True, enforceChirality=True, numThreads=0
)

def _prune_mols(structs, rmsd_cutoff):
    struct_ids = prune_conformers_by_rmsd([c.coords for c in structs], masses=structs[0].masses,
                                          rmsd_cutoff=rmsd_cutoff)
    structs = [structs[i] for i in struct_ids]
    return structs

def generate_conformer_ensemble(
        molecule_generator,
        smiles: str,
        *,
        energy_evaluator=None,
        optimizer=None,
        target_num_structs: int = 10,
        num_pregen: int = None,
        conf_gen_options: Optional[dict] = None,
        evaluate_energy: bool = True,
        preoptimize: bool = True,
        optimizer_settings: Optional[dict] = None,
        rmsd_cutoff: Optional[float] = .025,
        preopt_iterations: int = 50,
        spin: int = 1,
        verbose: bool = False,
        **molecule_options
) -> list:
    """
    The core, single-SMILES "generate -> dedupe -> optimize" routine.

    Given one SMILES string, this:

      1. embeds up to `conf_gen_options['numConfs']` (or `target_num_structs`, if
         energies aren't being evaluated) 3D conformers with RDKit's
         ETKDG-family embedder (via `Psience.Molecools.Molecule`),
      2. deduplicates them by mass-weighted, Eckart-aligned RMSD
         (`prune_conformers_by_rmsd`, `rmsd_cutoff`),
      3. optionally pre-optimizes every surviving conformer and re-dedupes,
      4. evaluates each conformer's energy and picks the lowest-`target_num_structs`
         (re-optimizing -- and re-scoring -- that final set if it wasn't
         already fully optimized in step 3), and
      5. returns them as `ConformerRecord`s, most-favorable first.

    This function is side-effect free: it never writes to disk, and it
    never raises on chemically invalid or unembeddable SMILES -- it returns
    an empty list instead, so batch drivers can skip bad entries without
    special-casing them.

    :param smiles: a single SMILES string
    :param target_num_structs: number of final conformers to keep
    :param conf_gen_options: passed through to the ETKDG embedder; merged
        over `default_conformer_generator_options` (user options win)
    :param energy_evaluator: the `Psience` energy evaluator (name, spec
        dict, or a raw ASE-style calculator object)
    :param evaluate_energy: whether to compute energies at all
    :param preoptimize: optimize every surviving conformer up front (rather
        than only the final selected set)
    :param optimizer_settings: passed to `Molecule.optimize`
    :param rmsd_cutoff: RMSD below which two conformers are considered
        duplicates (`None` disables deduplication)
    :param preopt_iterations: max iterations for the (cheaper)
        pre-optimization pass
    :param spin: passed through to `Molecule.from_string`
    :param verbose: print basic progress information
    :return: the selected conformers as `ConformerRecord`s (empty if the
        SMILES couldn't be parsed, embedded, or optimized)
    """
    opts = dict(default_conformer_generator_options)
    if conf_gen_options:
        opts.update(conf_gen_options)

    if energy_evaluator is None:
        evaluate_energy = False
    elif isinstance(energy_evaluator, str) or dev.is_dict_like(energy_evaluator):
        molecule_options['energy_evaluator'] = energy_evaluator
        def energy_evaluator(mol, **etc):
            return mol.calculate_energy(**etc)
        if optimizer is None:
            def optimizer(mol, **etc):
                return mol.optimize(**etc)

    if num_pregen is None:
        num_pregen = opts.pop('numConfs', 2 * target_num_structs)
    # if not evaluate_energy:
    #     num_pregen = target_num_structs

    if optimizer_settings is None:
        optimizer_settings = {}

    if verbose:
        print(f"Generating up to {num_pregen} conformers for {smiles}")

    structs = molecule_generator(
        smiles, 'smi',
        num_confs=num_pregen,
        conf_gen_options=opts,
        spin=spin,
        **molecule_options
    )

    if not structs:
        return []

    if rmsd_cutoff is not None:
        structs = _prune_mols(structs, rmsd_cutoff=rmsd_cutoff)
    if not structs:
        return []

    if optimizer is not None and preoptimize:
        preopt_settings = dict(optimizer_settings, max_iterations=preopt_iterations)
        structs = [optimizer(struct, **preopt_settings) for struct in structs]
        if rmsd_cutoff is not None:
            structs = _prune_mols(structs, rmsd_cutoff=rmsd_cutoff)
        if not structs:
            return []

    if evaluate_energy:
        energies = np.array([energy_evaluator(struct) for struct in structs])
    else:
        energies = None#np.zeros(len(structs))

    if evaluate_energy:
        if len(structs) > target_num_structs:
            top = np.argpartition(energies, target_num_structs - 1)[:target_num_structs]
            ord = np.argsort(energies[top])
            top = top[ord]
            energies = energies[ord,]
        else:
            top = np.argsort(energies)
            energies = energies[top,]
    else:
        top = np.arange(min(len(structs), target_num_structs))

    records = []
    for i in top:
        struct = structs[i]
        if optimizer is not None and not preoptimize and evaluate_energy:
            # only a cheap single-point scoring pass was done above (to
            # pick which conformers are worth the expense); now fully
            # optimize -- and re-score, so the reported energy matches the
            # returned structure -- just the selected subset
            struct = optimizer(struct, **optimizer_settings)
            energy = energy_evaluator(struct)
            energies[i] = energy
        records.append(struct)

    return records, energies
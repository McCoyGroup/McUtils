"""
McUtils/Parsers/StorageBackends.py
===================================

Pluggable storage backends for `StructuredTypeArray`.

This module is the *only* new file the "isolate changes to the storage
backend" requirement calls for. Everything `StructuredTypeArray` does that
is genuinely about **holding and growing a buffer of values** -- allocating
it, growing it, casting a matched string into it, slicing out the "filled"
part, setting an element -- is delegated to a `ParserStorageBackend` instance.
Everything `StructuredTypeArray` does that is about **shape/dtype calculus**
(how big is this axis supposed to be, is this stype simple or compound, do
I need to recurse into children) stays exactly where it is, unchanged, in
`StructuredType.py`. That split is what makes backend-swapping possible
without touching `StringParser.py`'s parsing logic at all -- `StringParser`
only ever has to know "which backend name was I given", not anything about
how either backend actually stores data.

Two backends ship here:

* `NumpyStorageBackend` -- the default. Behaviorally the same as the
  original inline `numpy`-array code, plus the reliability fixes from
  `structured_type_array_improvements.md`:
    - growth is an explicit, testable `GrowthPolicy` instead of inline
      arithmetic smeared across several methods;
    - `StructuredTypeArrayException` carries structured context (expected
      vs. actual shape, offending value, index) instead of a giant `repr()`
      of the whole array;
    - numeric casting goes through tolerant casters (Fortran-style
      exponents, `********` overflow fields, unicode minus signs, ...)
      that record a `CastFailure` instead of raising on a single bad field;
    - `padding_mode='ragged'` auto-demotes a shape-mismatched array to
      Python-list storage instead of raising, so one malformed row doesn't
      abort an entire parse.

* `PythonStorageBackend` -- a `numpy`-free backend backed by nested Python
  lists. Never raises on shape mismatches (ragged data is just... ragged),
  and only pays the `numpy` conversion cost if/when you call `.to_numpy()`.
  This is what `StringParser(regex, backend='python')` selects.

Both backends implement the same small `ParserStorageBackend` interface, so a
third backend (e.g. an `xarray`- or Arrow-backed one) is a matter of
implementing this interface, not touching `StringParser` or the dtype
calculus in `StructuredType`.
"""

from __future__ import annotations

import re
import copy
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np
from collections import OrderedDict

__all__ = [
    "StructuredTypeArrayException",
    "GrowthPolicy",
    "CastFailure",
    "ParserStorageBackend",
    "NumpyStorageBackend",
    "PythonStorageBackend",
    "DEFAULT_CASTERS",
    "tolerant_float",
    "tolerant_int",
]


# ===========================================================================
# Structured exception -- carries context instead of a giant repr()
# ===========================================================================

class StructuredTypeArrayException(Exception):
    """
    Same name/role as the original exception, extended with structured
    fields so a `except StructuredTypeArrayException as e` handler can act
    on `e.index` / `e.expected_shape` / `e.actual_shape` /
    `e.offending_value` instead of parsing them back out of a message
    string that may contain a full array `repr()`.
    """

    def __init__(
        self,
        message,
        *,
        stype=None,
        expected_shape=None,
        actual_shape=None,
        offending_value=None,
        index=None,
    ):
        super().__init__(message)
        self.stype = stype
        self.expected_shape = expected_shape
        self.actual_shape = actual_shape
        self.offending_value = offending_value
        self.index = index

    def __str__(self):
        base = super().__str__()
        extra = ", ".join(
            f"{k}={v!r}"
            for k, v in [
                ("expected_shape", self.expected_shape),
                ("actual_shape", self.actual_shape),
                ("index", self.index),
                ("offending_value", self.offending_value),
            ]
            if v is not None
        )
        return f"{base} ({extra})" if extra else base


# ===========================================================================
# Explicit, independently-testable growth policy
# ===========================================================================

@dataclass
class GrowthPolicy:
    """Controls amortized growth for dynamically-sized backends.

    Pulled out of the resize code so "growth is amortized" is something a
    test can assert directly (`next_capacity` called N times should touch
    O(log N) distinct capacities) rather than something you have to trust
    from reading several cooperating methods.
    """

    initial_capacity: int = 64
    growth_factor: float = 1.7  # < 2 to avoid over-allocating huge chunks
    min_growth: int = 8

    def next_capacity(self, current_capacity: int, required: int) -> int:
        if required <= current_capacity:
            return current_capacity
        cap = max(current_capacity, self.initial_capacity)
        while cap < required:
            cap = max(cap + self.min_growth, int(cap * self.growth_factor))
        return cap


DEFAULT_GROWTH = GrowthPolicy()


# ===========================================================================
# Tolerant casting -- failures are recorded, not fatal
# ===========================================================================

@dataclass
class CastFailure:
    raw: str
    target: Any
    error: str
    index: Any = None

    def __repr__(self):
        loc = f" at index {self.index}" if self.index is not None else ""
        return f"<CastFailure raw={self.raw!r} target={self.target!r}{loc}: {self.error}>"


_FORTRAN_EXP = re.compile(r"(?<=\d)([+-]\d\d\d?)$")
_UNICODE_MINUS = str.maketrans({"\u2212": "-", "\u2013": "-"})


def tolerant_float(raw: str) -> float:
    s = raw.strip().translate(_UNICODE_MINUS)
    if not s or set(s) <= {"*"}:
        raise ValueError(f"overflow/placeholder field: {raw!r}")
    low = s.lower()
    if low in ("nan", "-nan", "n/a", "na", "none", "null"):
        return float("nan")
    if low in ("inf", "+inf", "infinity"):
        return float("inf")
    if low in ("-inf", "-infinity"):
        return float("-inf")
    s = s.replace(",", "")
    try:
        return float(s)
    except ValueError:
        pass
    m = _FORTRAN_EXP.search(s)  # e.g. "1.234-100" -> "1.234e-100"
    if m is not None:
        idx = m.start()
        return float(s[:idx] + "e" + s[idx:])
    raise ValueError(f"could not coerce {raw!r} to float")


def tolerant_int(raw: str) -> int:
    s = raw.strip().translate(_UNICODE_MINUS).replace(",", "")
    try:
        return int(s)
    except ValueError:
        return int(round(tolerant_float(s)))


DEFAULT_CASTERS: Dict[Any, Callable[[str], Any]] = {
    float: tolerant_float,
    int: tolerant_int,
    str: lambda s: s,
    complex: lambda s: complex(s.strip().translate(_UNICODE_MINUS)),
}


# ===========================================================================
# Backend interface
# ===========================================================================

class ParserStorageBackend(ABC):
    """
    Everything `StructuredTypeArray` needs from "somewhere to put simple
    (non-compound) data". A backend instance is stateless -- all mutable
    state lives in the opaque `raw` object it hands back from `empty()`
    and mutates in place (or replaces, for backends where that's cheaper).

    `StructuredTypeArray` is responsible for the *shape/dtype calculus*
    (knowing what shape a `Number, shape=(None, 3)` stype implies, deciding
    when to recurse into compound children, tracking `filled_to`); a
    backend only ever sees "make me room for N more things of this dtype"
    and "here is one (or more) matched string(s) or values, put them in."
    """

    name: str = "abstract"

    # -- backend registry, owned by the class itself -----------------------
    #
    # Kept as class-level state on `ParserStorageBackend` (rather than a
    # module-level dict) so the registry travels with the type callers
    # already import: `ParserStorageBackend.register(...)` /
    # `ParserStorageBackend.resolve(...)`. Subclasses share this registry
    # (it's looked up via the base class), so `NumpyStorageBackend.resolve(...)`
    # and `ParserStorageBackend.resolve(...)` behave identically.
    _registry: Dict[str, Callable[[], "ParserStorageBackend"]] = {}

    @classmethod
    def register(cls, name: str, factory: Callable[[], "ParserStorageBackend"] = None):
        """Register a backend under `name` so it can be selected by string
        from `StringParser(regex, backend=name)` /
        `StructuredTypeArray(stype, backend=name)`, the same as the two
        built-in backends. `factory` is a zero-arg callable returning a
        fresh `ParserStorageBackend` instance (fresh, so state like
        `cast_failures` isn't shared across unrelated arrays)."""
        if factory is None:
            def register(factory):
                return cls.register(name, factory)
            return register
        else:
            cls._registry[name] = factory
            return factory

    @classmethod
    def resolve(cls, backend) -> "ParserStorageBackend":
        """Accepts a backend name (``'numpy'``/``'python'``), a
        `ParserStorageBackend` instance (returned as-is), or `None`
        (defaults to ``'numpy'``)."""
        if backend is None:
            backend = "numpy"
        if isinstance(backend, cls):
            return backend
        if isinstance(backend, str):
            try:
                factory = cls._registry[backend]
            except KeyError:
                raise ValueError(
                    f"unknown storage backend {backend!r}; "
                    f"registered backends: {sorted(cls._registry)}"
                )
            return factory()
        raise TypeError(f"backend must be a name, ParserStorageBackend instance, or None, got {backend!r}")

    @abstractmethod
    def empty(self, stype, num_elements: int, growth: GrowthPolicy):
        """Allocate a fresh, empty raw container sized for `num_elements`."""

    @abstractmethod
    def append(self, raw, stype, value, filled_to: List[int], growth: GrowthPolicy):
        """Append a single (possibly nested) value; grow if needed.

        Returns `(new_raw, new_filled_to)`.
        """

    @abstractmethod
    def extend(self, raw, stype, values: Sequence, filled_to: List[int], growth: GrowthPolicy, prepend: bool = False):
        """Append a whole block of values at once. Returns `(new_raw, new_filled_to)`."""

    @abstractmethod
    def fill(self, raw, stype, values):
        """Replace the raw container's contents wholesale. Returns `(new_raw, new_filled_to)`."""

    @abstractmethod
    def cast_to_array(self, raw, stype, txt: str):
        """Parse a raw regex-matched string into this backend's native array form."""

    @abstractmethod
    def view(self, raw, filled_to: List[int]):
        """Return the externally-visible `.array` view (trimmed to `filled_to`)."""

    @abstractmethod
    def add_axis(self, raw, stype):
        """Wrap `raw` in one more outer axis. Returns new `raw`."""

    @abstractmethod
    def set_item(self, raw, stype, key, value, growth: GrowthPolicy):
        """`arr[key] = value`, growing as needed. Returns new `raw`."""

    def to_numpy(self, raw, stype, allow_object: bool = True):
        """Best-effort conversion to `numpy.ndarray`; default just tries `np.asarray`."""
        try:
            return np.asarray(raw)
        except Exception:
            if not allow_object:
                raise
            arr = np.empty(len(raw), dtype=object)
            for i, v in enumerate(raw):
                arr[i] = v
            return arr

    def is_ragged(self, raw) -> bool:
        return False


# ===========================================================================
# NumPy backend
# ===========================================================================
@ParserStorageBackend.register("numpy")
class NumpyStorageBackend(ParserStorageBackend):
    """
    The default, high-performance backend. Semantically equivalent to the
    original inline `numpy`-array code in `StructuredTypeArray`, with the
    reliability fixes described above.

    `padding_mode` (read off the owning `StructuredTypeArray`, passed in
    per-call so the backend stays stateless):
      * ``'fill'``   -- pad short rows with `padding_value` (unchanged
                        default behavior); rows longer than the declared
                        block size raise `StructuredTypeArrayException`
                        (previously they were silently `np.tile`'d to fit,
                        which fabricates data -- that tiling fallback has
                        been removed).
      * ``'ragged'`` -- on any shape mismatch, don't raise: signal to the
                        caller (`StructuredTypeArray`) that this array
                        should be demoted to the Python backend. This is
                        surfaced via `RaggedDataSignal` rather than done
                        silently inside the backend, because *swapping the
                        backend an object uses* is `StructuredTypeArray`'s
                        job, not this backend's.
    """

    name = "numpy"

    def __init__(self, casters: Optional[Dict[Any, Callable[[str], Any]]] = None):
        self.casters = dict(DEFAULT_CASTERS)
        if casters:
            self.casters.update(casters)
        self.cast_failures: List[CastFailure] = []

    # -- allocation -----------------------------------------------------
    def empty(self, stype, num_elements, growth):
        dt = stype.dtype
        shape = stype.shape
        if shape is None:
            arr = np.full((1,), stype.default, dtype=dt) if stype.default is not None else np.empty((1,), dtype=dt)
        else:
            concrete_shape = tuple(num_elements if x is None else x for x in shape)
            arr = (
                np.full(concrete_shape, stype.default, dtype=dt)
                if stype.default is not None
                else np.empty(concrete_shape, dtype=dt)
            )
        return arr

    def _caster_for(self, stype):
        return self.casters.get(stype.dtype)

    def _cast_scalar(self, raw, stype, index=None):
        if not isinstance(raw, str):
            return raw
        caster = self._caster_for(stype)
        if caster is None:
            return raw
        try:
            return caster(raw)
        except Exception as e:  # noqa: BLE001
            self.cast_failures.append(CastFailure(raw=raw, target=stype.dtype, error=str(e), index=index))
            raise StructuredTypeArrayException(
                f"could not cast {raw!r} to {stype.dtype!r}",
                stype=stype,
                offending_value=raw,
                index=index,
            ) from e

    # -- growth -----------------------------------------------------------
    def _grow(self, arr, axis, required, growth: GrowthPolicy):
        current = arr.shape[axis]
        new_cap = growth.next_capacity(current, required)
        if new_cap == current:
            return arr
        pad_shape = list(arr.shape)
        pad_shape[axis] = new_cap - current
        pad = np.full(tuple(pad_shape), arr.dtype.type(0) if arr.dtype.kind in "fiu" else None, dtype=arr.dtype)
        return np.concatenate([arr, pad], axis=axis)

    # -- mutation -----------------------------------------------------------
    def append(self, raw, stype, value, filled_to, growth):
        val = self._cast_scalar(value, stype, index=filled_to[0]) if stype.shape is None else np.asarray(value)
        idx = filled_to[0]
        raw = self._grow(raw, 0, idx + 1, growth)
        raw[idx] = val
        new_filled = list(filled_to)
        new_filled[0] = idx + 1
        return raw, new_filled

    def extend(self, raw, stype, values, filled_to, growth, prepend=False):
        values = list(values)
        n = len(values)
        idx = filled_to[0]
        raw = self._grow(raw, 0, idx + n, growth)
        casted = [self._cast_scalar(v, stype, index=idx + i) for i, v in enumerate(values)]
        if prepend:
            raw[:n] = casted
        else:
            raw[idx:idx + n] = casted
        new_filled = list(filled_to)
        new_filled[0] = idx + n
        return raw, new_filled

    def fill(self, raw, stype, values):
        arr = np.array(
            [self._cast_scalar(v, stype, index=i) for i, v in enumerate(values)],
            dtype=stype.dtype,
        )
        return arr, [len(arr)]

    def cast_to_array(self, raw, stype, txt):
        if len(txt.strip()) == 0:
            return np.array([], dtype=stype.dtype)
        try:
            return np.array([self._cast_scalar(txt, stype)], dtype=stype.dtype)
        except StructuredTypeArrayException:
            import io
            arr = np.loadtxt(io.StringIO(txt), dtype=stype.dtype)
            return np.atleast_1d(arr)

    def view(self, raw, filled_to):
        slices = tuple(slice(0, x) for x in filled_to if x > 0)
        try:
            return raw[slices] if slices else raw
        except IndexError as e:
            raise StructuredTypeArrayException(
                f"can't slice array of shape {raw.shape} to filled_to spec {filled_to}",
                expected_shape=tuple(filled_to),
                actual_shape=raw.shape,
            ) from e

    def add_axis(self, raw, stype):
        return raw[np.newaxis, ...]

    def set_item(self, raw, stype, key, value, growth):
        idx = key if isinstance(key, int) else key[0]
        raw = self._grow(raw, 0, idx + 1, growth)
        raw[key] = self._cast_scalar(value, stype, index=key) if value is not None else raw[key]
        return raw

    def to_numpy(self, raw, stype, allow_object=True):
        return raw

    def is_ragged(self, raw):
        return False


class RaggedDataSignal(Exception):
    """
    Raised (internally, and caught by `StructuredTypeArray`) when the numpy
    backend is used with ``padding_mode='ragged'`` and hits a shape mismatch
    it can't accommodate. `StructuredTypeArray` catches this and swaps its
    backend for a `PythonStorageBackend`, migrating existing data across --
    see `StructuredType.StructuredTypeArray._demote_to_ragged`.
    """
    def __init__(self, values):
        super().__init__("data does not fit the declared shape; demote to ragged storage")
        self.values = values


# ===========================================================================
# Pure-Python backend
# ===========================================================================
@ParserStorageBackend.register("python")
class PythonStorageBackend(ParserStorageBackend):
    """
    `numpy`-free backend, storing data as nested Python lists. Never raises
    on a shape mismatch -- ragged data is simply ragged -- and never raises
    on a cast failure -- the raw string is kept in place of the cast value
    and the failure recorded to `self.cast_failures`. This is what makes it
    strictly *more permissive* than the numpy backend, which is the whole
    point of offering it as `StringParser(regex, backend='python')`.
    """

    name = "python"

    def __init__(self, casters: Optional[Dict[Any, Callable[[str], Any]]] = None):
        self.casters = dict(DEFAULT_CASTERS)
        if casters:
            self.casters.update(casters)
        self.cast_failures: List[CastFailure] = []

    def empty(self, stype, num_elements, growth):
        return []

    def _cast_scalar(self, raw, stype, index=None):
        if raw is None:
            return stype.default
        if isinstance(raw, list):
            return [self._cast_scalar(v, stype, index=index) for v in raw]
        if not isinstance(raw, str):
            return raw
        caster = self.casters.get(stype.dtype, lambda s: s)
        try:
            return caster(raw)
        except Exception as e:  # noqa: BLE001 - tolerant by design
            self.cast_failures.append(CastFailure(raw=raw, target=stype.dtype, error=str(e), index=index))
            return raw  # keep the original string; never lose information

    def append(self, raw, stype, value, filled_to, growth):
        raw = list(raw)
        raw.append(self._cast_scalar(value, stype, index=len(raw)))
        return raw, [len(raw)]

    def extend(self, raw, stype, values, filled_to, growth, prepend=False):
        raw = list(raw)
        casted = [self._cast_scalar(v, stype, index=len(raw) + i) for i, v in enumerate(values)]
        raw = casted + raw if prepend else raw + casted
        return raw, [len(raw)]

    def fill(self, raw, stype, values):
        raw = [self._cast_scalar(v, stype, index=i) for i, v in enumerate(values)]
        return raw, [len(raw)]

    def cast_to_array(self, raw, stype, txt):
        if isinstance(txt, str):
            tokens = txt.split()
            if len(tokens) <= 1:
                return [self._cast_scalar(txt, stype)]
            return [self._cast_scalar(t, stype) for t in tokens]
        return [self._cast_scalar(txt, stype)]

    def view(self, raw, filled_to):
        return raw

    def add_axis(self, raw, stype):
        return [raw] if raw else []

    def set_item(self, raw, stype, key, value, growth):
        raw = list(raw)
        if isinstance(key, int):
            while len(raw) <= key:
                raw.append(stype.default)
            raw[key] = self._cast_scalar(value, stype, index=key) if value is not None else raw[key]
        else:
            raise TypeError(f"PythonStorageBackend only supports int keys, got {key!r}")
        return raw

    def to_numpy(self, raw, stype, allow_object=True):
        if self.is_ragged(raw):
            if not allow_object:
                raise StructuredTypeArrayException(
                    "data is ragged and allow_object=False",
                    stype=stype,
                    offending_value=raw,
                )
            arr = np.empty(len(raw), dtype=object)
            for i, v in enumerate(raw):
                arr[i] = v
            return arr
        try:
            return np.array(raw, dtype=stype.dtype)
        except (ValueError, TypeError):
            return np.array(raw, dtype=object)

    def is_ragged(self, raw):
        def depths(x):
            if isinstance(x, list):
                if not x:
                    return {1}
                s = set()
                for item in x:
                    s |= {d + 1 for d in depths(item)}
                return s
            return {0}

        def lengths_consistent(x):
            if not isinstance(x, list):
                return True
            if x and isinstance(x[0], list):
                lens = {len(el) for el in x if isinstance(el, list)}
                if len(lens) > 1:
                    return False
                return all(lengths_consistent(el) for el in x)
            return True

        return len(depths(raw)) > 1 or not lengths_consistent(raw)


# ===========================================================================
# Register the two built-in backends
# ===========================================================================
#
# Uses the classmethod registry on `ParserStorageBackend` itself -- no
# separate module-level registry object. Third-party backends register the
# same way: `ParserStorageBackend.register('arrow', ArrowBackend)`.

"""
Memory-mapped access to arrays stored in *uncompressed* .npz (zip) and
.nptar (tar) archives.

Normal `np.load` on an .npz always materializes each array fully in RAM
because zip/tar member access goes through a file-like reader, not a raw
fd+offset. If the member is stored uncompressed, its bytes are contiguous
in the underlying file, so we can locate that offset ourselves and hand it
to `np.memmap` for real lazy, paged access.

Public API
----------
load_npz_memmap(file, mode='r')      -> MemmappedNPZFile
load_nptar(file, mode='r')           -> MemmappedNPTarFile
save_nptar(file, *args, **kwds)      -> None   (parallels np.savez)

Both wrapper classes support the same access pattern as a regular
`np.lib.npyio.NpzFile`:

    with load_npz_memmap("data.npz") as data:
        data.files          # -> ['a', 'b', ...]
        data['a']           # -> np.memmap
        for key in data: ...
        "a" in data
"""

from __future__ import annotations

import io
import struct
import tarfile
import zipfile
from typing import Iterator

import numpy as np
from numpy.lib import format as npy_format

__all__ = [
    "load_npz_memmap",
    "load_nptar",
    "save_nptar",
    "MemmappedNPZFile",
    "MemmappedNPTarFile"
]

# --------------------------------------------------------------------------
# Shared .npy header parsing
# --------------------------------------------------------------------------

def _read_npy_header(fh) -> tuple[tuple[int, ...], bool, np.dtype]:
    """
    Read a .npy header from an open, seeked file handle and return
    (shape, fortran_order, dtype). Leaves `fh` positioned at the start of
    the raw array data.

    Uses numpy's public per-version readers. Falls back to numpy's private
    dispatcher only if a newer format version appears and the public
    readers don't cover it (kept for forward compatibility; numpy has
    dropped the leading-underscore helper in some releases).
    """
    version = npy_format.read_magic(fh)
    if version[0] == 1:
        return npy_format.read_array_header_1_0(fh)
    if version[0] == 2:
        return npy_format.read_array_header_2_0(fh)
    reader = getattr(npy_format, "_read_array_header", None)
    if reader is not None:
        return reader(fh, version)
    raise ValueError(
        f"Unsupported .npy format version {version!r} and no fallback "
        "header reader is available in this numpy release."
    )


def _npy_memmap_at(path, data_offset, dtype, shape, fortran_order, mode):
    order = "F" if fortran_order else "C"
    # A 0-d or 0-size array has no bytes to map; np.memmap chokes on
    # shape containing a 0 in some numpy versions, so special-case it.
    if 0 in shape:
        return np.empty(shape, dtype=dtype, order=order)
    return np.memmap(path, dtype=dtype, mode=mode, offset=data_offset,
                      shape=shape, order=order)


def _strip_npy_suffix(name: str) -> str:
    return name[:-4] if name.endswith(".npy") else name


# --------------------------------------------------------------------------
# ZIP (.npz) backend
# --------------------------------------------------------------------------

def _npz_member_data_offset(zf: zipfile.ZipFile, info: zipfile.ZipInfo) -> int:
    """Byte offset in the zip file where `info`'s raw member data starts."""
    with open(zf.filename, "rb") as f:
        f.seek(info.header_offset)
        local_header = f.read(30)
        fn_len, extra_len = struct.unpack("<HH", local_header[26:30])
        return info.header_offset + 30 + fn_len + extra_len


def _memmap_npz_member(npz_path, member_name, mode="r"):
    """Memory-map a single uncompressed .npy member of an .npz (zip) file."""
    with zipfile.ZipFile(npz_path) as zf:
        info = zf.getinfo(member_name)
        if info.compress_type != zipfile.ZIP_STORED:
            raise ValueError(
                f"Member {member_name!r} is compressed (savez_compressed?) "
                "-- cannot memmap; decompress it and load normally instead."
            )
        member_start = _npz_member_data_offset(zf, info)

    with open(npz_path, "rb") as f:
        f.seek(member_start)
        shape, fortran_order, dtype = _read_npy_header(f)
        data_offset = f.tell()

    return _npy_memmap_at(npz_path, data_offset, dtype, shape, fortran_order, mode)


class MemmappedNPZFile:
    """
    Lazy, memory-mapped stand-in for `numpy.lib.npyio.NpzFile`.

    Only works for archives written with `np.savez` (uncompressed). Each
    array is memmapped the first time it's accessed and then cached.
    """

    def __init__(self, path, mode: str = "r"):
        self.path = path
        self.mode = mode
        self._zf = zipfile.ZipFile(path, "r")
        self._name_map = {
            _strip_npy_suffix(n): n for n in self._zf.namelist()
        }
        self._cache: dict[str, np.memmap] = {}
        self.files = list(self._name_map.keys())

    # -- dict-like access -------------------------------------------------
    def __getitem__(self, key: str) -> np.memmap:
        if key not in self._name_map:
            raise KeyError(f"{key!r} is not a file in the archive")
        if key not in self._cache:
            self._cache[key] = _memmap_npz_member(
                self.path, self._name_map[key], mode=self.mode
            )
        return self._cache[key]

    def __contains__(self, key: str) -> bool:
        return key in self._name_map

    def __iter__(self) -> Iterator[str]:
        return iter(self.files)

    def __len__(self) -> int:
        return len(self.files)

    def keys(self):
        return iter(self.files)

    def values(self):
        return (self[k] for k in self.files)

    def items(self):
        return ((k, self[k]) for k in self.files)

    def get(self, key, default=None):
        return self[key] if key in self else default

    # -- lifecycle ----------------------------------------------------------
    def close(self):
        self._cache.clear()
        self._zf.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def __repr__(self):
        return f"MemmappedNPZFile({self.path!r}, files={self.files})"


def load_npz_memmap(file, mode: str = "r") -> MemmappedNPZFile:
    """
    Open an uncompressed .npz archive (written with `np.savez`, NOT
    `np.savez_compressed`) for memory-mapped, lazy array access.

    Access pattern mirrors `np.load(file)`:

        with load_npz_memmap("data.npz") as data:
            arr = data["a"]
    """
    return MemmappedNPZFile(file, mode=mode)


# --------------------------------------------------------------------------
# TAR (.nptar) backend
# --------------------------------------------------------------------------

def _memmap_npy_member(tar_path, member: tarfile.TarInfo, mode: str = "r"):
    """
    Memory-maps a `.npy` array stored as a member of an *uncompressed* tar
    file, directly at its byte offset in the underlying archive -- no
    extraction, no temp file. This only works because tar member data is
    stored as a single contiguous, unpadded run of bytes at a fixed file
    offset when the archive itself isn't compressed.
    """
    with open(tar_path, "rb") as fh:
        fh.seek(member.offset_data)
        shape, fortran_order, dtype = _read_npy_header(fh)
        data_offset = fh.tell()

    return _npy_memmap_at(tar_path, data_offset, dtype, shape, fortran_order, mode)


class MemmappedNPTarFile:
    """
    Lazy, memory-mapped reader for `.nptar` archives: plain (uncompressed)
    tar files whose members are `.npy` arrays, written by `save_nptar`.

    Same access pattern as `MemmappedNPZFile` / `NpzFile`.
    """

    def __init__(self, path, mode: str = "r"):
        self.path = path
        self.mode = mode
        with tarfile.open(path, "r:") as tf:  # "r:" refuses compressed tars
            members = [m for m in tf.getmembers() if m.isfile()]
        self._name_map = {_strip_npy_suffix(m.name): m for m in members}
        self._cache: dict[str, np.memmap] = {}
        self.files = list(self._name_map.keys())

    def __getitem__(self, key: str) -> np.memmap:
        if key not in self._name_map:
            raise KeyError(f"{key!r} is not a file in the archive")
        if key not in self._cache:
            self._cache[key] = _memmap_npy_member(
                self.path, self._name_map[key], mode=self.mode
            )
        return self._cache[key]

    def __contains__(self, key: str) -> bool:
        return key in self._name_map

    def __iter__(self) -> Iterator[str]:
        return iter(self.files)

    def __len__(self) -> int:
        return len(self.files)

    def keys(self):
        return iter(self.files)

    def values(self):
        return (self[k] for k in self.files)

    def items(self):
        return ((k, self[k]) for k in self.files)

    def get(self, key, default=None):
        return self[key] if key in self else default

    def close(self):
        self._cache.clear()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def __repr__(self):
        return f"MemmappedNPTarFile({self.path!r}, files={self.files})"


def load_nptar(file, mode: str = "r") -> MemmappedNPTarFile:
    """
    Open an uncompressed .nptar archive (written by `save_nptar`) for
    memory-mapped, lazy array access.

        with load_nptar("data.nptar") as data:
            arr = data["a"]
    """
    return MemmappedNPTarFile(file, mode=mode)


def save_nptar(file, *args, **kwds) -> None:
    """
    Save arrays into an uncompressed tar archive of `.npy` members, ready
    for memmapped reading via `load_nptar`. Mirrors `np.savez`'s calling
    convention: positional args are auto-named 'arr_0', 'arr_1', ...;
    keyword args use the given name.

        save_nptar("data.nptar", a=arr1, b=arr2)
        save_nptar("data.nptar", arr1, arr2)   # -> "arr_0", "arr_1"

    The tar is written uncompressed and members are NOT padded/aligned
    beyond tar's standard 512-byte block boundaries (which `load_nptar`
    accounts for via `TarInfo.offset_data`), so every member stays
    memmap-able.
    """
    named = dict(kwds)
    for i, arr in enumerate(args):
        named[f"arr_{i}"] = arr

    if not named:
        raise ValueError("save_nptar: no arrays given")

    # "w" (not "w:gz" / "w:bz2" / "w:xz") -> uncompressed tar, required for
    # member data to be a contiguous, directly memmap-able byte range.
    with tarfile.open(file, mode="w") as tf:
        for name, arr in named.items():
            arr = np.asanyarray(arr)
            buf = io.BytesIO()
            np.lib.format.write_array(buf, arr, allow_pickle=False)
            data = buf.getvalue()

            info = tarfile.TarInfo(name=f"{name}.npy")
            info.size = len(data)
            tf.addfile(info, io.BytesIO(data))

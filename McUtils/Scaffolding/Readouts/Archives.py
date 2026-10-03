"""
Readouts for array archives and checkpoints: `NumpyTreeArchive`, `Checkpointer`s (NumPy/JSON/
HDF5/dict), plain ``.npz`` files, memory-mapped ``.npz``/``.nptar`` files and shared-memory
arrays. Contents are enumerated lazily (array headers, memmaps, per-record access) and only
small arrays are previewed; selected entries can be shown in full with ``show=[...]``.
"""

import json
import os
import zipfile

import numpy as np

from ...Jupyter.Readouts import (
    ReadoutAdapter, readout_section, ReadoutSectionUnavailable, ReadoutFields, ReadoutTable, ReadoutArray,
    ReadoutText, FieldSet, Field, Column, TabularData, ArrayData,
)

__all__ = [
    "ArchiveReadout",
    "npz_index",
]

_SEP = "::>|<::"


def npz_index(path):
    """``[(key, shape, dtype, nbytes)]`` read from the member headers only (no array data loaded)."""
    out = []
    with zipfile.ZipFile(path) as z:
        for info in z.infolist():
            if not info.filename.endswith(".npy"):
                continue
            with z.open(info) as f:
                version = np.lib.format.read_magic(f)
                if version == (1, 0):
                    shape, fortran, dtype = np.lib.format.read_array_header_1_0(f)
                else:
                    shape, fortran, dtype = np.lib.format.read_array_header_2_0(f)
            out.append((info.filename[:-4], tuple(shape), dtype, int(np.prod(shape, dtype=np.int64)) * dtype.itemsize))
    return out


def _preview(arr, max_items=8):
    a = np.asarray(arr)
    if a.dtype == object:
        return str(a.tolist())[:60]
    if a.ndim == 0:
        return str(a.item())[:60]
    if a.size <= max_items:
        if np.issubdtype(a.dtype, np.number):
            return "[" + ", ".join(f"{v:.6g}" for v in a.reshape(-1)) + "]"
        return str(a.reshape(-1).tolist())[:60]
    return ""


class ArchiveReadout(ReadoutAdapter):
    """
    **LLM Docstring**

    Readout for an archive-like object or path. ``max_entries`` bounds how many entries are
    indexed; entries listed in ``show`` are loaded and displayed in full.
    """
    readout_id = "archive"

    def __init__(self, archive, max_entries=500):
        super().__init__(archive)
        self.max_entries = max_entries
        self._index = None

    # ---- normalization ------------------------------------------------------------------- #
    def kind(self):
        a = self.obj
        name = type(a).__name__
        if isinstance(a, (str, os.PathLike)):
            ext = str(a).rsplit(".", 1)[-1].lower()
            return {"npz": "npz", "json": "json", "nptar": "nptar", "hdf5": "hdf5", "h5": "hdf5"}.get(ext, "file")
        if name == "NumpyTreeArchive":
            return "tree"
        if name.endswith("Checkpointer"):
            return "checkpointer"
        if name in ("MemmappedNPZFile", "MemmappedNPTarFile"):
            return "memmap"
        if name.startswith("SharedMemory") and hasattr(a, "shape"):
            return "shared"
        if isinstance(a, dict):
            return "dict"
        return "object"

    def path(self):
        a = self.obj
        if isinstance(a, (str, os.PathLike)):
            return str(a)
        for k in ("checkpoint_file", "file", "path", "filename"):
            v = getattr(a, k, None)
            if isinstance(v, (str, os.PathLike)):
                return str(v)
        return None

    def index(self):
        """``[(path, shape, dtype, nbytes, loader)]`` for up to ``max_entries`` entries."""
        if self._index is not None:
            return self._index
        k = self.kind()
        a = self.obj
        out = []
        p = self.path()
        if k in ("npz",) or (k == "checkpointer" and p and p.endswith(".npz")):
            for key, shape, dtype, nb in npz_index(p):
                out.append((key.replace(_SEP, "/"), shape, dtype, nb,
                            (lambda key=key: np.load(p, allow_pickle=False)[key])))
        elif k in ("json",) or (k == "checkpointer" and p and p.endswith(".json")):
            with open(p) as f:
                data = json.load(f)
            out = self._walk(data)
        elif k == "hdf5" or (k == "checkpointer" and p and p.rsplit(".", 1)[-1] in ("hdf5", "h5")):
            import h5py
            f = h5py.File(p, "r")
            f.visititems(lambda name, obj: out.append((name, obj.shape, obj.dtype, obj.size * obj.dtype.itemsize,
                                                       (lambda name=name: f[name][()])))
                         if hasattr(obj, "shape") else None)
        elif k == "checkpointer":
            with a:
                keys = list(a.keys())
                data = {key: a[key] for key in keys[:self.max_entries]}
            out = self._walk(data)
        elif k == "tree":
            keys = [key for key in a.keys()]
            leaves = [key for key in keys if not any(other.startswith(key + "/") for other in keys)]
            for key in leaves[:self.max_entries]:
                v = a[key]
                out.extend(self._walk({key: v}))
        elif k == "memmap":
            for key in list(a.keys())[:self.max_entries]:
                v = a[key]
                out.append((key, v.shape, v.dtype, v.nbytes, (lambda v=v: np.asarray(v))))
        elif k == "shared":
            out.append(("array", a.shape, a.dtype, a.nbytes, (lambda: np.asarray(a))))
        elif k == "dict":
            out = self._walk(a)
        else:
            raise TypeError(f"don't know how to index {type(a).__name__}")
        self._index = out[:self.max_entries]
        self._truncated = len(out) > self.max_entries
        return self._index

    def _walk(self, data, prefix=""):
        out = []
        if isinstance(data, dict):
            for k, v in data.items():
                out.extend(self._walk(v, f"{prefix}{k}/"))
            return out
        arr = np.asarray(data) if not isinstance(data, np.ndarray) else data
        out.append((prefix.rstrip("/"), arr.shape, arr.dtype, arr.nbytes, (lambda arr=arr: arr)))
        return out

    def get_readout_title(self):
        p = self.path()
        return f"Archive: {os.path.basename(p)}" if p else f"{type(self.obj).__name__}"

    # ---- sections ------------------------------------------------------------------------ #
    @readout_section("summary", title="Archive")
    def readout_summary(self, ctx):
        """Kind, location, entry count and total size."""
        idx = self.index()
        f = [Field("kind", type(self.obj).__name__ if not isinstance(self.obj, (str, os.PathLike)) else f".{self.kind()} file",
                   label="Kind")]
        p = self.path()
        if p:
            f.append(Field("file", os.path.abspath(p), label="File", quantity="path"))
            if os.path.isfile(p):
                f.append(Field("file_size", os.path.getsize(p), label="File size (bytes)", quantity="int"))
        f += [Field("entries", len(idx), label="Entries" + (" (truncated)" if getattr(self, "_truncated", False) else ""),
                    quantity="int"),
              Field("data_size", int(sum(e[3] for e in idx)), label="Array data (bytes)", quantity="int")]
        if self.kind() == "shared":
            f.append(Field("shm_name", getattr(getattr(self.obj, "buf", None), "name", ""), label="Shared memory name"))
        return ReadoutFields(FieldSet(f, name="summary"))

    @readout_section("contents", title="Contents")
    def readout_contents(self, ctx, max_rows=60, preview_items=8):
        """Path, shape, dtype and size of each entry, with previews of tiny arrays."""
        idx = self.index()
        if not idx:
            raise ReadoutSectionUnavailable("empty")
        rows = idx[:max_rows]
        previews = []
        for e in rows:
            if int(np.prod(e[1], dtype=np.int64)) <= preview_items:
                try:
                    previews.append(_preview(e[4](), preview_items))
                except Exception:
                    previews.append("")
            else:
                previews.append("")
        cols = [Column("path", np.array([e[0] for e in rows]), label="Path"),
                Column("shape", np.array(["×".join(map(str, e[1])) or "scalar" for e in rows]), label="Shape"),
                Column("dtype", np.array([str(e[2]) for e in rows]), label="dtype"),
                Column("nbytes", np.array([e[3] for e in rows]), label="Bytes"),
                Column("preview", np.array(previews), label="Value")]
        nodes = [ReadoutTable(TabularData(cols, name="entries"))]
        if len(idx) > max_rows:
            nodes.append(ReadoutText(f"{len(idx) - max_rows} more entries not listed", role="note"))
        return nodes

    @readout_section("selected", title="Selected entries", default=False)
    def readout_selected(self, ctx, show=()):
        """Entries named in ``show`` (paths from the contents table), loaded and shown in full."""
        idx = {e[0]: e for e in self.index()}
        nodes = []
        for p in show:
            if p not in idx:
                nodes.append(ReadoutText(f"{p}: not found", role="note"))
                continue
            arr = np.asarray(idx[p][4]())
            nodes.append(ReadoutArray(ArrayData(p.replace("/", "_"), arr, label=p), display=True, title=p))
        if not nodes:
            raise ReadoutSectionUnavailable("nothing selected (pass show=[...])")
        return nodes

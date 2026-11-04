"""File and record storage: indexed tar, line suppliers and storage lifecycle.

Serializers.py owns object/tree encodings. Numputils.Serialization owns the
lightweight array archives and NumPy-member mapper reused here.
"""

from __future__ import annotations

import collections
import contextlib
from collections.abc import Mapping
import io
import json
import operator
import os
import posixpath
import re
import shutil
import sqlite3
import tarfile
import tempfile
import threading
import uuid
import numpy as np
from .. import Devutils as dev
from ..Numputils.Serialization import _memmap_npy_member, _load_npy_member_bytes

__all__ = [
    "ArchiveMapping", "FileStoreLock", "IndexedTarStore",
    "LineIndexedSupplier", "SerializedObjectSupplier", "JSONLSupplier", "NPZLSupplier"
]


def _close_owned_directory(archive):
    owned = getattr(archive, "_owned_directory", None)
    if owned is not None:
        owned.cleanup()
        archive._owned_directory = None


class ArchiveMapping(Mapping):
    """Keyed, lazy access with consistent mapping and lifecycle operations.

    Concrete archives retain their own value model: tree records, ndarrays,
    integer-indexed line records, or file bytes. Persistence is implemented by each concrete archive.
    """

    @property
    def files(self):
        return list(self.keys())

    @classmethod
    def load(cls, file, **reader_options):
        return cls(file, **reader_options)

    def unpack(self):
        """Materialize the keyed values; structured archives can refine this."""
        return dict(self.items())

    def close(self):
        _close_owned_directory(self)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def to_readout(self, **options):
        from .Readouts import ArchiveReadout
        return ArchiveReadout(self).to_readout(**options)


class _FileWrapper:
    """Give a tar member the small file interface expected by StreamInterface."""

    def __init__(self, stream, mode="rb", encoding="utf-8"):
        self.stream = stream
        self.mode = mode
        self.encoding = encoding

    def read(self, n=None):
        return self.stream.read() if n is None else self.stream.read(n)

    def readline(self, n=None):
        return self.stream.readline() if n is None else self.stream.readline(n)

    def seek(self, n, *args):
        return self.stream.seek(n, *args)

    def tell(self):
        return self.stream.tell()

    def peek(self, n=1):
        return self.stream.peek(n) if hasattr(self.stream, "peek") else b""

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class LineIndexedSupplier:
    """Stream and randomly access objects serialized one per line.

    ``deserialization_function`` receives one raw line (normally ``bytes``)
    and returns the corresponding object.  A line-index is an ndarray of
    byte offsets.  A jump database is an uncompressed tar containing the
    source lines, that ndarray, metadata, and optional index-aligned arrays.

    Subclasses configure the default name of the source member with
    ``STORED_FILE_NAME``.  ``stored_file_name=`` on
    :meth:`build_jump_database` overrides it for one database; the selected
    name is recorded in the database metadata and honored when it is loaded.
    """

    STORED_FILE_NAME = "lines.dat"
    INDEX_FILE_NAME = "line_indices.npy"
    META_FILE_NAME = "meta.json"

    _EOF = object()

    def __init__(
        self,
        data_file,
        line_indices=None,
        name=None,
        size=int(1e3),
        managed_streams=None,
        deserialization_function=None,
        metadata_arrays=None,
        stored_file_name=None,
    ):
        self.name = name
        self.data = dev.StreamInterface(data_file, mode="rb")
        self.line_indices = line_indices
        self._size = size
        self._call_depth = 0
        self._stream = None
        self._cur = None
        self._max_offset = None
        self._offsets = None
        self._flexible_offsets = None
        self._assignable_offsets = None
        self._encoding = self.data.get_encoding()
        self._binary = self.data.is_binary()
        self._deserialization_function = deserialization_function
        self.deserialization_function = deserialization_function
        self.managed_streams = managed_streams
        self._exit_codes = (None, None, None)
        self.metadata_arrays = metadata_arrays
        self.stored_file_name = stored_file_name or self.STORED_FILE_NAME

    def _default_deserialization_function(self, line):
        if isinstance(line, bytes):
            line = line.decode(self._encoding)
        return line.rstrip("\r\n")

    @classmethod
    def from_jump_database(
        cls,
        database_file,
        name=None,
        deserialization_function=None,
        metadata_arrays=None,
        create=False,
        **extra,
    ):
        """Open a packaged or expanded jump database.

        When ``create=True``, ``database_file`` is treated as an expanded
        database directory. The directory and any missing empty database
        files are created before opening it. Existing database files are
        never truncated or replaced.
        """
        if create:
            cls._create_database_directory(database_file, name=name)
        data_file, line_indices, meta, streams, archive_arrays = cls._load_database_archive(
            database_file
        )
        if meta is not None and name is None:
            name = meta.get("name")
        stored_file_name = (
            meta.get("stored_file_name", cls.STORED_FILE_NAME)
            if meta is not None
            else cls.STORED_FILE_NAME
        )

        if metadata_arrays is None:
            metadata_arrays = archive_arrays
        elif archive_arrays:
            merged = dict(archive_arrays)
            merged.update(metadata_arrays)
            metadata_arrays = merged

        return cls(
            data_file,
            line_indices=line_indices,
            name=name,
            managed_streams=streams,
            deserialization_function=deserialization_function,
            metadata_arrays=metadata_arrays,
            stored_file_name=stored_file_name,
            **extra,
        )

    @classmethod
    def _create_database_directory(cls, directory, name=None):
        if not isinstance(directory, (str, os.PathLike)):
            raise TypeError("a created jump database must be a filesystem directory")
        directory = os.fspath(directory)
        if os.path.exists(directory) and not os.path.isdir(directory):
            if tarfile.is_tarfile(directory):
                return directory
            raise NotADirectoryError(
                f"cannot create a jump database directory at {directory!r}: "
                "a non-directory entry already exists"
            )
        os.makedirs(directory, exist_ok=True)

        meta_path = os.path.join(directory, cls.META_FILE_NAME)
        if os.path.isfile(meta_path):
            with open(meta_path, "r", encoding="utf-8") as stream:
                meta = json.load(stream)
        else:
            meta = None
        stored_file_name = (
            meta.get("stored_file_name", cls.STORED_FILE_NAME)
            if meta is not None
            else cls.STORED_FILE_NAME
        )
        data_path = os.path.join(directory, stored_file_name)
        index_path = os.path.join(directory, cls.INDEX_FILE_NAME)

        data_exists = os.path.isfile(data_path)
        index_exists = os.path.isfile(index_path)
        if not data_exists and index_exists:
            line_indices = np.load(index_path, mmap_mode="r")
            if len(line_indices) > 0:
                raise ValueError(
                    f"cannot create missing data file {data_path!r}: "
                    f"{index_path!r} contains {len(line_indices)} record offsets"
                )
        if data_exists and not index_exists and os.path.getsize(data_path) > 0:
            raise ValueError(
                f"cannot create an empty index for non-empty data file {data_path!r}"
            )

        if not data_exists:
            with open(data_path, "xb"):
                pass
        if not index_exists:
            np.save(index_path, np.empty(0, dtype=np.uint16))
        if meta is None:
            with open(meta_path, "x", encoding="utf-8") as stream:
                json.dump(
                    {"name": name, "stored_file_name": stored_file_name},
                    stream,
                )

        return directory

    @classmethod
    def _read_archive_meta(cls, tar, names):
        if cls.META_FILE_NAME not in names:
            return None
        stream = tar.extractfile(cls.META_FILE_NAME)
        try:
            return json.loads(stream.read().decode("utf-8"))
        finally:
            stream.close()

    @classmethod
    def _load_database_archive(cls, path):
        if not isinstance(path, (str, os.PathLike)):
            return path, None, None, None, None
        if not os.path.exists(path):
            return path, None, None, None, None
        if os.path.isdir(path):
            return cls._load_database_directory(path)
        if not tarfile.is_tarfile(path):
            return path, None, None, None, None

        tar_path = os.fspath(path)
        tar = tarfile.open(tar_path, mode="r:").__enter__()
        names = set(tar.getnames())
        meta = cls._read_archive_meta(tar, names)
        stored_file_name = (
            meta.get("stored_file_name", cls.STORED_FILE_NAME)
            if meta is not None
            else cls.STORED_FILE_NAME
        )
        if stored_file_name not in names or cls.INDEX_FILE_NAME not in names:
            tar.__exit__(None, None, None)
            return path, None, None, None, None

        data_file = _FileWrapper(tar.extractfile(stored_file_name))
        line_indices = _memmap_npy_member(
            tar_path, tar.getmember(cls.INDEX_FILE_NAME)
        )
        metadata_arrays = cls._load_metadata_arrays(tar, meta)
        return data_file, line_indices, meta, [tar], metadata_arrays

    @classmethod
    def _load_metadata_arrays(cls, tar, meta):
        members = meta.get("metadata_arrays") if meta is not None else None
        if not members:
            return None
        return {
            key: _load_npy_member_bytes(tar, tar.getmember(member_name))
            for key, member_name in members.items()
        }

    @classmethod
    def _load_database_directory(cls, directory):
        directory = os.fspath(directory)
        meta_path = os.path.join(directory, cls.META_FILE_NAME)
        meta = None
        if os.path.isfile(meta_path):
            with open(meta_path, "r", encoding="utf-8") as stream:
                meta = json.load(stream)
        stored_file_name = (
            meta.get("stored_file_name", cls.STORED_FILE_NAME)
            if meta is not None
            else cls.STORED_FILE_NAME
        )
        data_path = os.path.join(directory, stored_file_name)
        index_path = os.path.join(directory, cls.INDEX_FILE_NAME)
        if not (os.path.isfile(data_path) and os.path.isfile(index_path)):
            return directory, None, None, None, None

        line_indices = np.load(index_path, mmap_mode="r")
        members = meta.get("metadata_arrays") if meta is not None else None
        metadata_arrays = None
        if members:
            metadata_arrays = {
                key: np.load(os.path.join(directory, member_name), allow_pickle=True)
                for key, member_name in members.items()
            }
        return data_path, line_indices, meta, None, metadata_arrays

    def to_mp_state(self):
        return (
            self.data._input,
            self.name,
            self._deserialization_function,
            self.stored_file_name,
        )

    @classmethod
    def from_mp_state(cls, state, line_indices=None, **extra):
        data_file, name, deserialization_function, stored_file_name = state
        return cls(
            data_file,
            line_indices=line_indices,
            name=name,
            deserialization_function=deserialization_function,
            stored_file_name=stored_file_name,
            **extra,
        )

    def __enter__(self):
        self._call_depth += 1
        if self._call_depth == 1:
            if self.deserialization_function is None:
                self.deserialization_function = self._default_deserialization_function
            self._stream = self.data.__enter__()
            self._cur = 0
            if self.line_indices is None:
                self._max_offset = 0
                self.line_indices = np.zeros(self._size, dtype="uint64")
                self._flexible_offsets = True
            if isinstance(self.line_indices, np.ndarray) and not isinstance(
                self.line_indices, np.memmap
            ):
                self._offsets = self.line_indices
                if self._flexible_offsets is None:
                    self._flexible_offsets = False
                self._assignable_offsets = self._flexible_offsets
            else:
                self._offsets = (
                    self.line_indices
                    if isinstance(self.line_indices, np.memmap)
                    else np.load(self.line_indices, mmap_mode="r")
                )
                self._flexible_offsets = False
                self._assignable_offsets = False
            if self._max_offset is None:
                self._max_offset = len(self._offsets)
        self._exit_codes = (None, None, None)
        return self, self._stream

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._call_depth -= 1
        if self._call_depth == 0:
            self.deserialization_function = self._deserialization_function
            self._cur = None
            self._stream.__exit__(exc_type, exc_val, exc_tb)
            self._stream = None
            if self._flexible_offsets:
                self.line_indices = self._offsets
            self._offsets = None
            self._exit_codes = (exc_type, exc_val, exc_tb)

    def __del__(self):
        if hasattr(self, "managed_streams"):
            self.close()

    def close(self):
        """Release packaged streams and any owned temporary database."""
        if self._call_depth:
            return
        if self.managed_streams is not None:
            for stream in self.managed_streams:
                stream.__exit__(*self._exit_codes)
            self.managed_streams = None
        _close_owned_directory(self)

    @classmethod
    def load(cls, file, **reader_options):
        return cls.from_jump_database(file, **reader_options)

    def save(self, file, **writer_options):
        return self.write_jump_database(file, **writer_options)

    @property
    def files(self):
        return list(self.keys())

    def keys(self):
        return range(len(self))

    def values(self):
        return self.consume_iter(start_at=0)

    def items(self):
        return enumerate(self.values())

    def to_readout(self, **options):
        from .Readouts import ArchiveReadout
        return ArchiveReadout(self).to_readout(**options)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return [self[i] for i in range(*index.indices(len(self)))]
        index = operator.index(index)
        size = len(self)
        if index < 0:
            index += size
        if not 0 <= index < size:
            raise IndexError(index)
        return self.find_object(index)

    def get(self, index, default=None):
        try:
            return self[index]
        except (IndexError, TypeError):
            return default

    def unpack(self):
        return list(self.values())

    def __len__(self):
        with self:
            if self._flexible_offsets:
                self.create_line_index(return_index=False)
            return self._max_offset

    @classmethod
    def _consume_next(cls, db, deserialization_function):
        line = db.readline()
        if len(line) == 0:
            return cls._EOF
        return deserialization_function(line)

    def _metadata_at(self, n):
        return {key: array[n] for key, array in self.metadata_arrays.items()}

    def _metadata_slice(self, start, stop):
        return {
            key: array[start:stop] for key, array in self.metadata_arrays.items()
        }

    def find_object(self, n, block_size=None, include_metadata=None):
        if include_metadata is None:
            include_metadata = self.metadata_arrays is not None
        elif include_metadata and self.metadata_arrays is None:
            raise ValueError(
                f"{type(self).__name__} has no `metadata_arrays`; "
                "pass `metadata_arrays=...` to use `include_metadata`"
            )
        with self as (_, db):
            if n >= self._max_offset:
                self.create_line_index(n, return_index=False)
            db.seek(self._offsets[n])
            if block_size is None:
                self._cur = n
                obj = self._consume_next(db, self.deserialization_function)
                if obj is self._EOF:
                    obj = b""
                return (obj, self._metadata_at(n)) if include_metadata else obj

            self._cur = n + block_size
            objects = []
            for offset in range(block_size):
                if self._assignable_offsets:
                    self._expand_offset_if_needed(n + offset)
                    self._offsets[n + offset] = db.tell()
                obj = self._consume_next(db, self.deserialization_function)
                if obj is self._EOF:
                    obj = b""
                objects.append(obj)
            if include_metadata:
                return objects, self._metadata_slice(n, n + block_size)
            return objects

    def consume_iter(self, start_at=None, upto=None, include_metadata=None):
        if include_metadata is None:
            include_metadata = self.metadata_arrays is not None
        elif include_metadata and self.metadata_arrays is None:
            raise ValueError(
                f"{type(self).__name__} has no `metadata_arrays`; "
                "pass `metadata_arrays=...` to use `include_metadata`"
            )
        with self as (_, db):
            if start_at is None:
                start_at = self._cur
            else:
                self.create_line_index(upto=start_at, return_index=False)
            ninds = start_at
            if not self._assignable_offsets and ninds >= self._max_offset:
                return
            try:
                db.seek(self._offsets[ninds])
                if upto is not None and ninds >= upto:
                    return
                obj = self._consume_next(db, self.deserialization_function)
                while obj is not self._EOF and (upto is None or ninds < upto):
                    row = ninds
                    ninds += 1
                    if self._assignable_offsets:
                        self._expand_offset_if_needed(ninds)
                        self._offsets[ninds] = db.tell()
                    yield (obj, self._metadata_at(row)) if include_metadata else obj
                    obj = self._consume_next(db, self.deserialization_function)
            finally:
                self._cur = ninds
                self._max_offset = max(self._max_offset, ninds)

    def __next__(self):
        if self._stream is None:
            raise ValueError(
                f"{type(self).__name__} must be opened via `with` before iteration"
            )
        with self as (_, db):
            if not self._assignable_offsets and self._cur >= self._max_offset:
                raise StopIteration
            db.seek(self._offsets[self._cur])
            obj = self._consume_next(db, self.deserialization_function)
            if obj is self._EOF:
                raise StopIteration
            self._cur += 1
            return obj

    def __iter__(self):
        return self.consume_iter()

    def _expand_offset_if_needed(self, n):
        if n < len(self._offsets):
            return
        if not self._flexible_offsets:
            raise ValueError(
                f"{self._max_offset} `line_indices` were passed, but the database extends beyond that"
            )
        new_offsets = np.zeros(max(1, 2 * len(self._offsets)), dtype="uint64")
        new_offsets[: len(self._offsets)] = self._offsets
        self._offsets = new_offsets

    def create_line_index(self, upto=None, return_index=True):
        with self as (_, db):
            if not self._assignable_offsets:
                return self._offsets[: self._max_offset] if return_index else None
            ninds = self._max_offset
            db.seek(self._offsets[ninds])
            try:
                line_length = len(db.readline())
                while line_length > 0 and (upto is None or ninds < upto):
                    ninds += 1
                    self._expand_offset_if_needed(ninds)
                    self._offsets[ninds] = self._offsets[ninds - 1] + line_length
                    if not self._binary and db.peek(1) == "\r":
                        self._offsets[ninds] += 1
                    line_length = len(db.readline())
            finally:
                self._max_offset = ninds
            return self._offsets[: self._max_offset] if return_index else None

    @classmethod
    def save_line_index(cls, file, line_index):
        max_offset = np.max(line_index, initial=0)
        for dtype in (np.uint16, np.uint32, np.uint64):
            if max_offset < np.iinfo(dtype).max:
                line_index = line_index.astype(dtype)
                break
        return np.save(file, line_index)

    def write_jump_database(self, target, **options):
        with self as (_, stream):
            self.create_line_index(return_index=False)
            indices = self._offsets[:self._max_offset]
            if isinstance(self.data._input, (str, os.PathLike)):
                return self.build_jump_database(self, target, line_indices=indices, **options)
            # Packaged records already have a jump table; copy their byte stream
            # without deserializing/re-serializing records or losing metadata.
            with tempfile.TemporaryDirectory(prefix="mcutils-repack-") as temporary:
                data = os.path.join(temporary, "records")
                position = stream.tell()
                try:
                    stream.seek(0)
                    with open(data, "wb") as output:
                        shutil.copyfileobj(stream, output)
                finally:
                    stream.seek(position)
                parameters = dict(name=self.name, metadata_arrays=self.metadata_arrays,
                                  stored_file_name=self.stored_file_name)
                parameters.update(options)
                return self.build_jump_database(data, target, line_indices=indices, **parameters)

    @staticmethod
    def _metadata_member_name(key, disambiguator=None):
        slug = re.sub(r"[^A-Za-z0-9_.-]+", "_", str(key)).strip("_") or "field"
        name = f"metadata_{slug}"
        if disambiguator is not None:
            name = f"{name}_{disambiguator}"
        return f"{name}.npy"

    @classmethod
    def build_jump_database(
        cls,
        supplier_or_data_file,
        out_file,
        line_indices=None,
        name=None,
        metadata_arrays=None,
        stored_file_name=None,
        overwrite=False,
        extra_metadata=None,
    ):
        if not overwrite and os.path.exists(out_file):
            raise FileExistsError(
                f"{out_file} already exists; pass overwrite=True to replace it"
            )

        if isinstance(supplier_or_data_file, LineIndexedSupplier):
            supplier = supplier_or_data_file
            data_path = supplier.data._input
            if not isinstance(data_path, (str, os.PathLike)):
                raise ValueError("can only package a supplier backed by a real file path")
            if line_indices is None:
                line_indices = supplier.line_indices
            if name is None:
                name = supplier.name
            if metadata_arrays is None:
                metadata_arrays = supplier.metadata_arrays
            if stored_file_name is None:
                stored_file_name = supplier.stored_file_name
        else:
            data_path = supplier_or_data_file
        if stored_file_name is None:
            stored_file_name = cls.STORED_FILE_NAME

        if line_indices is None:
            scanner = cls(data_path)
            with scanner:
                line_indices = scanner.create_line_index(return_index=True)
        if isinstance(line_indices, (str, os.PathLike)):
            with open(line_indices, "rb") as stream:
                index_bytes = stream.read()
        else:
            buffer = io.BytesIO()
            cls.save_line_index(buffer, np.asarray(line_indices))
            index_bytes = buffer.getvalue()

        meta = {"name": name, "stored_file_name": stored_file_name}
        if extra_metadata:
            meta.update(extra_metadata)
            meta["stored_file_name"] = stored_file_name

        metadata_payloads = {}
        if metadata_arrays:
            member_names = {}
            used_names = set()
            for i, (key, array) in enumerate(metadata_arrays.items()):
                member_name = cls._metadata_member_name(key)
                if member_name in used_names:
                    member_name = cls._metadata_member_name(key, disambiguator=i)
                used_names.add(member_name)
                buffer = io.BytesIO()
                np.save(buffer, np.asarray(array))
                metadata_payloads[member_name] = buffer.getvalue()
                member_names[key] = member_name
            meta["metadata_arrays"] = member_names

        meta_bytes = json.dumps(meta).encode("utf-8")
        with tarfile.open(out_file, mode="w") as tar:
            tar.add(data_path, arcname=stored_file_name)
            for member_name, payload in (
                [(cls.INDEX_FILE_NAME, index_bytes)]
                + list(metadata_payloads.items())
                + [(cls.META_FILE_NAME, meta_bytes)]
            ):
                info = tarfile.TarInfo(name=member_name)
                info.size = len(payload)
                tar.addfile(info, io.BytesIO(payload))
        return out_file

class SerializedObjectSupplier(LineIndexedSupplier):
    """Shared writing and packaging support for concrete object formats."""

    @classmethod
    def serialize_object(cls, obj):
        raise NotImplementedError

    @classmethod
    def from_tree(cls, records, file=None, **reader_options):
        """Create a packaged archive from an iterable of records."""
        owned = tempfile.TemporaryDirectory(prefix="mcutils-records-") if file is None else None
        target = os.path.join(owned.name, "records.tar") if owned is not None else file
        try:
            cls.create_jump_database(records, target)
            archive = cls.load(target, **reader_options)
            archive._owned_directory = owned
            return archive
        except BaseException:
            if owned is not None:
                owned.cleanup()
            raise

    @classmethod
    def write_object(cls, stream, obj):
        payload = cls.serialize_object(obj)
        stream.write(payload)
        stream.write(b"\n")

    @classmethod
    def write_objects(cls, objects, data_file, line_indices_file=None, overwrite=False):
        """Serialize objects and return a supplier with a complete jump index."""
        data_file = os.fspath(data_file)
        if line_indices_file is None:
            line_indices_file = data_file + ".line_indices.npy"
        if not overwrite and os.path.exists(data_file):
            raise FileExistsError(
                f"{data_file} already exists; pass overwrite=True to replace it"
            )
        line_indices_file = os.fspath(line_indices_file)
        if not overwrite and os.path.exists(line_indices_file):
            raise FileExistsError(
                f"{line_indices_file} already exists; pass overwrite=True to replace it"
            )

        offsets = []
        with open(data_file, "wb") as stream:
            for obj in objects:
                offsets.append(stream.tell())
                cls.write_object(stream, obj)
        offsets = np.asarray(offsets, dtype=np.uint64)
        if len(offsets) == 0:
            # LineIndexedSupplier.save_line_index chooses a dtype from the
            # final offset, which an empty database does not have.
            np.save(line_indices_file, offsets.astype(np.uint16))
        else:
            cls.save_line_index(line_indices_file, offsets)
        return cls(data_file, line_indices=line_indices_file)

    def append(self, obj):
        """Append one object and its byte offset to the sidecar jump index."""
        return self.extend((obj,))

    def extend(self, objects):
        """Append an iterable of objects and atomically update the jump index.

        Only suppliers backed by ordinary files are mutable. Packaged jump
        databases are intentionally read-only because changing a tar member
        would require rebuilding the archive. If serialization or index
        persistence fails, the data file is truncated to its original size.
        """
        if self._call_depth != 0:
            raise RuntimeError("cannot extend a supplier while it is open")
        if self.metadata_arrays is not None:
            raise ValueError(
                "cannot extend a supplier with index-aligned metadata_arrays"
            )

        data_file = self.data._input
        if not isinstance(data_file, (str, os.PathLike)):
            raise ValueError("packaged jump databases are read-only")
        data_file = os.fspath(data_file)
        if not os.path.isfile(data_file):
            raise FileNotFoundError(data_file)

        current_offsets, index_file = self._append_index_state(data_file)
        original_size = os.path.getsize(data_file)
        appended_offsets = []
        try:
            with open(data_file, "r+b") as stream:
                stream.seek(0, os.SEEK_END)
                for obj in objects:
                    appended_offsets.append(stream.tell())
                    self.write_object(stream, obj)
                stream.flush()

            if len(appended_offsets) == 0:
                return self

            new_offsets = np.concatenate(
                [current_offsets, np.asarray(appended_offsets, dtype=np.uint64)]
            )
            self._replace_line_index(index_file, new_offsets)
        except BaseException:
            with open(data_file, "r+b") as stream:
                stream.truncate(original_size)
            raise

        # Reopen the new index lazily on the next supplier operation.
        self.line_indices = index_file
        self._offsets = None
        self._max_offset = None
        self._flexible_offsets = None
        self._assignable_offsets = None
        return self

    def _append_index_state(self, data_file):
        line_indices = self.line_indices
        if isinstance(line_indices, (str, os.PathLike)):
            index_file = os.fspath(line_indices)
            current_offsets = np.asarray(np.load(index_file, mmap_mode="r")).copy()
        elif isinstance(line_indices, np.memmap):
            index_file = os.fspath(line_indices.filename)
            current_offsets = np.asarray(line_indices).copy()
        elif isinstance(line_indices, np.ndarray):
            count = self._max_offset
            current_offsets = np.asarray(
                line_indices if count is None else line_indices[:count]
            ).copy()
            index_file = data_file + ".line_indices.npy"
        else:
            # A supplier without a fixed index may only have scanned part of
            # its input. Complete the scan before adding new offsets.
            with self:
                current_offsets = np.asarray(self.create_line_index()).copy()
            index_file = data_file + ".line_indices.npy"
        return current_offsets, index_file

    @classmethod
    def _replace_line_index(cls, index_file, line_indices):
        index_dir = os.path.dirname(os.path.abspath(index_file))
        temp_name = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="wb", dir=index_dir, prefix=".line_indices-", delete=False
            ) as temp:
                temp_name = temp.name
                cls.save_line_index(temp, line_indices)
                temp.flush()
            os.replace(temp_name, index_file)
            temp_name = None
        finally:
            if temp_name is not None and os.path.exists(temp_name):
                os.unlink(temp_name)

    @classmethod
    def create_jump_database(
        cls,
        objects,
        out_file,
        name=None,
        metadata_arrays=None,
        stored_file_name=None,
        overwrite=False,
    ):
        """Serialize an iterable directly into a packaged jump database."""
        stored_file_name = stored_file_name or cls.STORED_FILE_NAME
        suffix = os.path.splitext(stored_file_name)[1]
        with tempfile.TemporaryDirectory() as temp_dir:
            data_file = os.path.join(temp_dir, "records" + suffix)
            supplier = cls.write_objects(objects, data_file)
            return cls.build_jump_database(
                supplier,
                out_file,
                line_indices=supplier.line_indices,
                name=name,
                metadata_arrays=metadata_arrays,
                stored_file_name=stored_file_name,
                overwrite=overwrite,
            )

class JSONLSupplier(SerializedObjectSupplier):
    """Serialize JSON-compatible objects one compact JSON value per line."""

    STORED_FILE_NAME = "records.jsonl"

    def __init__(self, *args, json_load_options=None, **kwargs):
        self.json_load_options = {} if json_load_options is None else json_load_options
        super().__init__(*args, **kwargs)

    @classmethod
    def serialize_object(cls, obj):
        return json.dumps(
            obj,
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8")

    def _default_deserialization_function(self, line):
        return json.loads(line, **self.json_load_options)

class NPZLSupplier(SerializedObjectSupplier):
    """Serialize mappings/arrays as binary, length-framed NPZ records.

    Each record has the form ``<decimal byte length>\n<raw npz bytes>\n``.
    The explicit byte length is required because an NPZ file is a ZIP stream
    and may contain arbitrary newline bytes internally. Jump indices point to
    the start of each decimal length header.
    """

    STORED_FILE_NAME = "records.npzl"

    def __init__(self, *args, allow_pickle=False, **kwargs):
        self.allow_pickle = allow_pickle
        super().__init__(*args, **kwargs)

    @classmethod
    def serialize_object(cls, obj):
        buffer = io.BytesIO()
        if hasattr(obj, "items"):
            np.savez(buffer, **obj)
        elif isinstance(obj, (tuple, list)):
            np.savez(buffer, *obj)
        else:
            np.savez(buffer, obj)
        return buffer.getvalue()

    @classmethod
    def write_object(cls, stream, obj):
        payload = cls.serialize_object(obj)
        stream.write(str(len(payload)).encode("ascii"))
        stream.write(b"\n")
        stream.write(payload)
        stream.write(b"\n")

    def _default_deserialization_function(self, payload):
        with np.load(io.BytesIO(payload), allow_pickle=self.allow_pickle) as archive:
            return {key: archive[key] for key in archive.files}

    @classmethod
    def _consume_next(cls, db, deserialization_function):
        length_line = db.readline()
        if len(length_line) == 0:
            return cls._EOF
        try:
            payload_length = int(length_line)
        except ValueError as exc:
            raise ValueError(f"invalid NPZL record length {length_line!r}") from exc
        payload = db.read(payload_length)
        if len(payload) != payload_length:
            raise EOFError(
                f"truncated NPZL record: expected {payload_length} bytes, "
                f"found {len(payload)}"
            )
        if db.read(1) != b"\n":
            raise ValueError("NPZL record is not followed by a newline separator")
        return deserialization_function(payload)

    def create_line_index(self, upto=None, return_index=True):
        with self as (_, db):
            if not self._assignable_offsets:
                return self._offsets[: self._max_offset] if return_index else None
            ninds = self._max_offset
            db.seek(self._offsets[ninds])
            try:
                length_line = db.readline()
                while len(length_line) > 0 and (upto is None or ninds < upto):
                    try:
                        payload_length = int(length_line)
                    except ValueError as exc:
                        raise ValueError(
                            f"invalid NPZL record length {length_line!r}"
                        ) from exc
                    payload_start = db.tell()
                    db.seek(payload_length, os.SEEK_CUR)
                    if db.tell() - payload_start != payload_length:
                        raise EOFError("truncated NPZL record")
                    if db.read(1) != b"\n":
                        raise ValueError(
                            "NPZL record is not followed by a newline separator"
                        )
                    ninds += 1
                    self._expand_offset_if_needed(ninds)
                    self._offsets[ninds] = db.tell()
                    length_line = db.readline()
            finally:
                self._max_offset = ninds
            return self._offsets[: self._max_offset] if return_index else None


class FileStoreLock:
    """Reentrant thread/process lock on a stable sidecar file (POSIX)."""

    _registry = {}
    _guard = threading.Lock()

    def __init__(self, path):
        self.path = os.path.realpath(os.fspath(path))

    @contextlib.contextmanager
    def __call__(self):
        import fcntl

        key = (os.getpid(), self.path)
        with self._guard:
            mutex, local = self._registry.setdefault(key, (threading.RLock(), threading.local()))
        with mutex:
            depth = getattr(local, "depth", 0)
            if depth == 0:
                os.makedirs(os.path.dirname(self.path), exist_ok=True)
                local.stream = open(self.path, "a+b")
                try:
                    fcntl.flock(local.stream.fileno(), fcntl.LOCK_EX)
                except BaseException:
                    local.stream.close()
                    raise
            local.depth = depth + 1
            try:
                yield
            finally:
                local.depth -= 1
                if local.depth == 0:
                    try:
                        fcntl.flock(local.stream.fileno(), fcntl.LOCK_UN)
                    finally:
                        local.stream.close()


class _MemberReader(io.RawIOBase):
    """A bounded view that keeps its tar inode alive across archive replacement."""

    def __init__(self, path, offset, size):
        super().__init__()
        self.stream = open(path, "rb")
        self.offset, self.size, self.position = offset, size, 0

    def readable(self):
        return True

    def seekable(self):
        return True

    def tell(self):
        self._checkClosed()
        return self.position

    def seek(self, offset, whence=os.SEEK_SET):
        self._checkClosed()
        position = offset if whence == os.SEEK_SET else (
            self.position + offset if whence == os.SEEK_CUR else
            self.size + offset if whence == os.SEEK_END else None)
        if position is None or position < 0:
            raise ValueError("invalid seek")
        self.position = position
        return position

    def readinto(self, buffer):
        self._checkClosed()
        length = min(len(buffer), max(0, self.size - self.position))
        self.stream.seek(self.offset + self.position)
        data = self.stream.read(length)
        buffer[:len(data)] = data
        self.position += len(data)
        return len(data)

    def close(self):
        if not self.closed:
            self.stream.close()
        super().close()


class IndexedTarStore(ArchiveMapping):
    """Append file trees and seek directly to individual live members.

    ``path`` is an uncompressed tar; ``path + '.index.sqlite3'`` is its jump
    table and ``path + '.lock'`` serializes readers/writers during publication.
    Reads of a missing store do not create any files. Overwriting a prefix
    supersedes its old members; :meth:`compact` reclaims their physical bytes.
    A missing or stale index is rebuilt from tar headers, never from payloads.
    """

    def __init__(self, path, index_path=None):
        self.path = os.path.abspath(os.fspath(path))
        self.index_path = os.fspath(index_path) if index_path is not None else self.path + ".index.sqlite3"
        self.lock = FileStoreLock(self.path + ".lock")

    @classmethod
    def from_tree(cls, tree, file=None, **options):
        """Create a byte-file archive from a nested mapping, like NumpyTreeArchive.

        Leaves are bytes-like file contents and mappings are directories. When
        no file is supplied the archive owns temporary storage until close().
        """
        if not isinstance(tree, Mapping):
            raise TypeError("a tar tree must be a mapping")
        owned = tempfile.TemporaryDirectory(prefix="mcutils-tar-") if file is None else None
        target = os.path.join(owned.name, "archive.tar") if owned is not None else file
        files = {}

        def visit(mapping, prefix=""):
            for key, value in mapping.items():
                name = cls.normalize_name(prefix + "/" + key if prefix else key)
                if name in files:
                    raise ValueError("duplicate tree path: " + name)
                if isinstance(value, Mapping):
                    files[name] = None
                    visit(value, name)
                elif isinstance(value, (bytes, bytearray, memoryview)):
                    files[name] = bytes(value)
                else:
                    raise TypeError("tar tree leaves must be bytes-like: " + name)
        try:
            visit(tree)
            for name in list(files):
                pieces = name.split("/")
                for end in range(1, len(pieces)):
                    parent = "/".join(pieces[:end])
                    if parent in files and files[parent] is not None:
                        raise ValueError("file is also used as a directory: " + parent)
                    files.setdefault(parent, None)
            archive = cls(target, **options)
            trees = []
            for prefix in sorted({name.split("/", 1)[0] for name in files}):
                value = files[prefix]
                if value is not None:
                    # A top-level file has no containing record directory.
                    trees.append((prefix, None, {"": value}))
                else:
                    trees.append((prefix, None, {name[len(prefix) + 1:]: data for name, data in files.items()
                                                if name.startswith(prefix + "/")}))
            if trees:
                archive.write_trees(trees)
            else:
                with archive.lock():
                    with tarfile.open(archive.path, "w"):
                        pass
                    with archive._index():
                        pass
            archive._owned_directory = owned
            return archive
        except BaseException:
            if owned is not None:
                owned.cleanup()
            raise

    def __getitem__(self, path):
        try:
            return self.read(path)
        except IsADirectoryError:
            return self.unpack(prefix=path)
        except FileNotFoundError:
            if self.names(path):
                return self.unpack(prefix=path)
            raise KeyError(path) from None

    def __iter__(self):
        return iter(self.names())

    def __len__(self):
        if not os.path.exists(self.path):
            return 0
        with self.lock(), self._index() as db:
            return db.execute("SELECT count(*) FROM members").fetchone()[0]

    def __contains__(self, path):
        return bool(self.names(path))

    def member_info(self, path):
        """Return a member's TarInfo without opening its payload."""
        path = self.normalize_name(path)
        if not os.path.exists(self.path):
            raise KeyError(path)
        with self.lock(), self._index() as db:
            row = db.execute("SELECT header, offset FROM members WHERE name=?", (path,)).fetchone()
            if row is None:
                raise KeyError(path)
            info = self._info(row[0])
            info.offset_data = row[1]
            return info

    def memmap(self, path, mode="r"):
        """Map a stored .npy array using the same implementation as array/line archives.

        Views are read-only or copy-on-write. Persistent modifications use the
        archive's write methods so the payload and jump table stay consistent.
        """
        if mode not in ("r", "c"):
            raise ValueError("indexed tar mappings support modes 'r' and 'c'")
        if not os.path.exists(self.path):
            raise KeyError(path)
        with self.lock():
            info = self.member_info(path)
            if not info.isfile():
                raise ValueError("only regular .npy members can be memory-mapped")
            return _memmap_npy_member(self.path, info, mode=mode)

    def unpack(self, prefix=None):
        """Materialize nested dictionaries of file bytes, optionally below a directory."""
        if not os.path.exists(self.path):
            if prefix is not None:
                raise KeyError(prefix)
            return {}
        with self.lock():
            return self._unpack(prefix)

    def _unpack(self, prefix):
        names = self.names(prefix)
        if prefix is not None:
            prefix = self.normalize_name(prefix)
            if not names:
                raise KeyError(prefix)
        tree = {}
        for name in names:
            if name == prefix:
                continue
            relative = name if prefix is None else name[len(prefix) + 1:]
            pieces = relative.split("/")
            node = tree
            for key in pieces[:-1]:
                node = node.setdefault(key, {})
            info = self.member_info(name)
            if info.isdir():
                node.setdefault(pieces[-1], {})
            else:
                node[pieces[-1]] = self.read(name)
        return tree

    @staticmethod
    def normalize_name(name):
        name = os.fspath(name).replace(os.sep, "/")
        if name.startswith("/") or "\x00" in name or ".." in name.split("/"):
            raise ValueError("archive member must be a relative path without '..'")
        name = posixpath.normpath(name)
        if name in ("", "."):
            raise ValueError("empty archive member name")
        return name

    def _fingerprint(self):
        if not os.path.exists(self.path):
            return None
        stat = os.stat(self.path)
        return [stat.st_dev, stat.st_ino, stat.st_size, stat.st_mtime_ns]

    @staticmethod
    def _state(db, key, default=None):
        row = db.execute("SELECT value FROM state WHERE key=?", (key,)).fetchone()
        return default if row is None else json.loads(row[0])

    @staticmethod
    def _set_state(db, **items):
        db.executemany("INSERT OR REPLACE INTO state VALUES (?, ?)",
                       [(key, json.dumps(value)) for key, value in items.items()])

    @staticmethod
    def _header(member):
        data = member.get_info()
        data["type"] = data["type"].decode("ascii")
        data["pax_headers"] = member.pax_headers
        return json.dumps(data)

    @staticmethod
    def _info(header):
        data = json.loads(header)
        data["type"] = data["type"].encode("ascii")
        member = tarfile.TarInfo(data.pop("name"))
        for key, value in data.items():
            setattr(member, key, value)
        return member

    @classmethod
    def _row(cls, member, offset):
        return (member.name.rstrip("/"), offset, member.size, cls._header(member))

    @contextlib.contextmanager
    def _index(self):
        os.makedirs(os.path.dirname(os.path.abspath(self.index_path)), exist_ok=True)
        db = sqlite3.connect(self.index_path, timeout=60)
        try:
            db.execute("CREATE TABLE IF NOT EXISTS members (name TEXT PRIMARY KEY, offset INTEGER, size INTEGER, header TEXT)")
            db.execute("CREATE TABLE IF NOT EXISTS state (key TEXT PRIMARY KEY, value TEXT)")
            pending = self._state(db, "pending_end")
            if pending is not None:
                if os.path.exists(self.path):
                    self._rollback_append(pending)
                self._rebuild(db)
            elif self._state(db, "fingerprint") != self._fingerprint():
                self._rebuild(db)
            yield db
        finally:
            db.close()

    def _rebuild(self, db):
        end = 0
        with db:
            db.execute("DELETE FROM members")
            if os.path.exists(self.path):
                with tarfile.open(self.path, "r:") as archive:
                    for member in archive:
                        name = self.normalize_name(member.name)
                        if member.pax_headers.get("mcutils.replace_tree") == "1":
                            db.execute("DELETE FROM members WHERE name=? OR (name>=? AND name<?)",
                                       (name, name + "/", name + "0"))
                        if member.pax_headers.get("mcutils.deleted_tree") != "1":
                            db.execute("INSERT OR REPLACE INTO members VALUES (?, ?, ?, ?)",
                                       self._row(member, member.offset_data))
                        end = member.offset_data + ((member.size + 511) // 512) * 512
                        archive.members.clear()
            self._set_state(db, fingerprint=self._fingerprint(), end=end, pending_end=None)

    def _rollback_append(self, end):
        with open(self.path, "r+b") as stream:
            stream.seek(end)
            stream.write(b"\0" * 1024)
            stream.truncate()
            stream.flush()
            os.fsync(stream.fileno())

    @staticmethod
    def _prefix_rows(db, prefix):
        return db.execute(
            "SELECT name, offset, size, header FROM members WHERE name=? OR (name>=? AND name<?) ORDER BY offset",
            (prefix, prefix + "/", prefix + "0")).fetchall()

    @staticmethod
    def _add(archive, member, stream, rows):
        archive.addfile(member, stream)
        offset = archive.offset - ((member.size + 511) // 512) * 512
        rows.append(IndexedTarStore._row(member, offset))

    @classmethod
    def _write_tree(cls, archive, prefix, directory, extra_files, rows, deleted=False):
        # A hard link in one logical record must not point into another record:
        # that target could later be superseded independently.
        archive.inodes.clear()
        if "" in extra_files:
            if directory is not None or len(extra_files) != 1:
                raise ValueError("a root file cannot also contain a directory tree")
            payload = extra_files[""]
            member = tarfile.TarInfo(prefix)
            member.size = len(payload)
            member.pax_headers = {"mcutils.replace_tree": "1"}
            cls._add(archive, member, io.BytesIO(payload), rows)
            return
        extra_files = {cls.normalize_name(key): value for key, value in extra_files.items()}
        root = tarfile.TarInfo(prefix)
        root.type = tarfile.DIRTYPE
        root.pax_headers = {"mcutils.replace_tree": "1"}
        if deleted:
            root.pax_headers["mcutils.deleted_tree"] = "1"
        cls._add(archive, root, None, rows)
        if deleted:
            rows.pop()
            return
        if directory is not None:
            if os.path.islink(directory) or not os.path.isdir(directory):
                raise NotADirectoryError(directory)
            for current, dirs, files in os.walk(directory, followlinks=False):
                for filename in sorted(dirs + files):
                    path = os.path.join(current, filename)
                    relative = os.path.relpath(path, directory).replace(os.sep, "/")
                    if relative in extra_files:
                        continue
                    member = archive.gettarinfo(path, arcname=prefix + "/" + relative)
                    if not (member.isfile() or member.isdir() or member.issym() or member.islnk()):
                        raise ValueError("cannot archive special file: " + path)
                    with open(path, "rb") if member.isfile() else contextlib.nullcontext() as source:
                        cls._add(archive, member, source, rows)
        for relative, payload in extra_files.items():
            member = tarfile.TarInfo(prefix + "/" + relative)
            if payload is None:
                member.type = tarfile.DIRTYPE
                cls._add(archive, member, None, rows)
            else:
                member.size = len(payload)
                cls._add(archive, member, io.BytesIO(payload), rows)

    @classmethod
    def export_trees(cls, trees, out_file, compression=None, **options):
        """Write a standalone tar, optionally compressed, using the same tree format."""
        mode = "w" if compression is None else "w:" + compression
        with open(out_file, "wb") as stream:
            with tarfile.open(fileobj=stream, mode=mode, dereference=False, **options) as archive:
                for prefix, directory, files in trees:
                    cls._write_tree(archive, cls.normalize_name(prefix), directory, files or {}, [])
            stream.flush()
            os.fsync(stream.fileno())

    def write_trees(self, trees, *, deleted=False):
        """Atomically publish ``(prefix, directory_or_None, extra_files)`` trees.

        ``extra_files`` maps relative names to bytes and replaces matching source
        files. Symlinks are stored as links, never followed while archiving.
        Source directories are left untouched; callers remove them after success.
        """
        trees = [(self.normalize_name(prefix), directory, {} if files is None else files)
                 for prefix, directory, files in trees]
        if not trees:
            return
        prefixes = [prefix for prefix, _, _ in trees]
        if len(set(prefixes)) != len(prefixes):
            raise ValueError("duplicate tree prefixes")
        ordered = sorted(prefixes)
        if any(right.startswith(left + "/") for left, right in zip(ordered, ordered[1:])):
            raise ValueError("overlapping tree prefixes")
        with self.lock(), self._index() as db:
            end = self._state(db, "end", 0)
            with db:
                self._set_state(db, pending_end=end)
            rows = []
            try:
                with open(self.path, "r+b" if os.path.exists(self.path) else "w+b") as stream:
                    stream.seek(end)
                    with tarfile.open(fileobj=stream, mode="w", dereference=False) as archive:
                        for prefix, directory, extra_files in trees:
                            self._write_tree(archive, prefix, directory, extra_files, rows, deleted=deleted)
                        next_end = archive.offset
                    stream.truncate()
                    stream.flush()
                    os.fsync(stream.fileno())
                with db:
                    for prefix in prefixes:
                        db.execute("DELETE FROM members WHERE name=? OR (name>=? AND name<?)",
                                   (prefix, prefix + "/", prefix + "0"))
                    db.executemany("INSERT OR REPLACE INTO members VALUES (?, ?, ?, ?)", rows)
                    self._set_state(db, end=next_end, pending_end=None, fingerprint=self._fingerprint())
            except BaseException:
                if os.path.exists(self.path):
                    self._rollback_append(end)
                self._rebuild(db)
                raise

    def open(self, name):
        """Open one member in binary mode without scanning the tar or loading it."""
        name = self.normalize_name(name)
        if not os.path.exists(self.path):
            raise FileNotFoundError(name)
        with self.lock(), self._index() as db:
            for _ in range(40):
                row = db.execute("SELECT offset, size, header FROM members WHERE name=?", (name,)).fetchone()
                if row is None:
                    raise FileNotFoundError(name)
                offset, size, header = row
                info = self._info(header)
                if info.isfile():
                    return io.BufferedReader(_MemberReader(self.path, offset, size))
                if info.isdir():
                    raise IsADirectoryError(name)
                name = self.normalize_name(posixpath.normpath(
                    posixpath.join(posixpath.dirname(name), info.linkname)
                    if info.issym() else info.linkname))
            raise OSError("too many archive symlinks")

    def read(self, name):
        with self.open(name) as stream:
            return stream.read()

    def discard(self, prefix):
        """Forget a tree; compact later to reclaim superseded physical bytes."""
        if self.names(prefix):
            self.write_trees([(prefix, None, {})], deleted=True)

    def names(self, prefix=None):
        if not os.path.exists(self.path):
            return []
        with self.lock(), self._index() as db:
            if prefix is None:
                return [row[0] for row in db.execute("SELECT name FROM members ORDER BY name")]
            return [row[0] for row in self._prefix_rows(db, self.normalize_name(prefix))]

    def compact(self):
        """Rewrite live members only, publishing with an atomic file replacement."""
        if not os.path.exists(self.path):
            return
        with self.lock(), self._index() as db:
            rows = db.execute("SELECT name, offset, size, header FROM members ORDER BY offset").fetchall()
            fd, temporary = tempfile.mkstemp(prefix=".tar-compact-", dir=os.path.dirname(self.path))
            try:
                with os.fdopen(fd, "wb") as stream:
                    with tarfile.open(fileobj=stream, mode="w") as archive:
                        for _, offset, size, header in rows:
                            info = self._info(header)
                            with _MemberReader(self.path, offset, size) if info.isfile() else contextlib.nullcontext() as source:
                                archive.addfile(info, source)
                    stream.flush()
                    os.fsync(stream.fileno())
                os.replace(temporary, self.path)
                self._rebuild(db)
            finally:
                if os.path.exists(temporary):
                    os.unlink(temporary)

    def _write_snapshot(self, db, stream):
        rows = db.execute("SELECT offset, size, header FROM members ORDER BY offset").fetchall()
        with tarfile.open(fileobj=stream, mode="w") as archive:
            for offset, size, header in rows:
                info = self._info(header)
                with _MemberReader(self.path, offset, size) if info.isfile() else contextlib.nullcontext() as source:
                    archive.addfile(info, source)

    def save(self, file, index_path=None):
        """Save the current live view; saving to this store also compacts it."""
        if hasattr(file, "write"):
            with self.lock(), self._index() as db:
                self._write_snapshot(db, file)
            return file
        target = type(self)(file, index_path=index_path)
        if target.path == self.path:
            self.compact()
            return file
        with contextlib.ExitStack() as stack:
            for lock in sorted((self.lock, target.lock), key=lambda item: item.path):
                stack.enter_context(lock())
            db = stack.enter_context(self._index())
            target_db = stack.enter_context(target._index())
            fd, temporary = tempfile.mkstemp(prefix=".tar-save-", dir=os.path.dirname(target.path))
            try:
                with os.fdopen(fd, "wb") as stream:
                    self._write_snapshot(db, stream)
                    stream.flush()
                    os.fsync(stream.fileno())
                os.replace(temporary, target.path)
                target._rebuild(target_db)
            finally:
                if os.path.exists(temporary):
                    os.unlink(temporary)
        return file

"""
A directory-per-entry, content-addressed store on top of the atomic file helpers.

Layout (``shard=2``, the default)::

    root/<key[:2]>/<key>/<meta_name>    metadata (JSON); its presence marks the entry as complete
    root/<key[:2]>/<key>/<files>        payload files (``/`` allowed for subdirectories)
    root/aliases/<name>.json            optional ``name -> key`` indirections

With ``shard=0`` entries sit directly at ``root/<key>``. Entries are published by renaming a fully built
temporary directory, so an interrupted write never leaves a half-written entry. This is the one
implementation behind the readout store, the compiled-expression store and `ObjectStore`.
"""
from __future__ import annotations

import contextlib
import datetime
import errno
import json
import os
import re
import shutil
import time
import uuid

from .FileHelpers import atomic_write, atomic_write_json, FileStoreLock

__all__ = [
    "EntryStore",
    "StagedEntry",
]


class StagedEntry:
    """The handle `EntryStore.stage` yields: fill `path`, optionally set `meta`, and it is published on exit."""

    def __init__(self, store, key, path, meta):
        self.store = store
        self.key = key
        self.path = path
        self.meta = meta

    def file(self, *name):
        """Path of a (not yet written) file inside the staged entry."""
        return os.path.join(self.path, *name)


class EntryStore:
    """
    Content-addressed directory entries with atomic publication, aliases, `prune` and LRU `gc`.

    Subclasses configure ``meta_name``, ``key_pattern``, ``shard``, ``format_version`` and ``lock_name``
    (``None`` disables the cross-process lock, which committed stores don't want as an extra file).
    """

    meta_name = "meta.json"
    key_pattern = r"[0-9a-f]{64}"
    shard = 2
    format_version = 1
    lock_name = None
    aliases_name = "aliases"
    alias_field = "key"
    stage_prefix = ".stage-"

    def __init__(self, root):
        self.root = os.fspath(root)

    # ---- keys and paths ---- #
    def check_key(self, key):
        if not isinstance(key, str) or not re.fullmatch(self.key_pattern, key):
            raise ValueError("not a valid store key: {!r}".format(key))
        return key

    @staticmethod
    def _check_filename(name):
        parts = name.replace("\\", "/").split("/")
        if name == "" or os.path.isabs(name) or ".." in parts or "" in parts:
            raise ValueError("invalid entry file name: {!r}".format(name))
        return name

    def entry_path(self, key, *parts):
        self.check_key(key)
        if self.shard:
            return os.path.join(self.root, key[:self.shard], key, *parts)
        return os.path.join(self.root, key, *parts)

    def has(self, key):
        return os.path.isfile(self.entry_path(key, self.meta_name))

    def has_file(self, key, name):
        return os.path.isfile(self.entry_path(key, self._check_filename(name)))

    def read_meta(self, key):
        path = self.entry_path(key, self.meta_name)
        if not os.path.isfile(path):
            return None
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def read_file(self, key, name, binary=False):
        self._check_filename(name)
        path = self.entry_path(key, *name.split("/"))
        with open(path, "rb" if binary else "r", **({} if binary else {"encoding": "utf-8"})) as f:
            return f.read()

    def keys(self):
        """All keys present in the store (entries with a metadata file)."""
        found = []
        if not os.path.isdir(self.root):
            return found
        def scan(directory, prefix=None):
            for key in sorted(os.listdir(directory)):
                if key.startswith(".") or (prefix is not None and not key.startswith(prefix)):
                    continue
                if re.fullmatch(self.key_pattern, key) and os.path.isfile(os.path.join(directory, key, self.meta_name)):
                    found.append(key)
        if self.shard:
            for shard in sorted(os.listdir(self.root)):
                sp = os.path.join(self.root, shard)
                if len(shard) == self.shard and os.path.isdir(sp):
                    scan(sp, shard)
        else:
            scan(self.root)
        return found

    # ---- locking ---- #
    def lock(self):
        """A reentrant cross-process lock on the store (a no-op context if ``lock_name`` is ``None``)."""
        if self.lock_name is None:
            return contextlib.nullcontext()
        return FileStoreLock(os.path.join(self.root, self.lock_name))()

    @contextlib.contextmanager
    def transaction(self):
        """Holds the store lock for a block of related reads and writes."""
        with self.lock():
            yield self

    # ---- writing ---- #
    def _stamp(self, key, meta):
        return dict(meta, key=key, store_version=self.format_version,
                    written=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))

    def write(self, key, meta, files=None):
        """
        Writes (replacing) the entry for ``key``.

        :param meta: JSON-able metadata; ``key``, ``written`` and ``store_version`` are added
        :param files: mapping of relative file name (``/`` allowed for subdirectories) to ``str``/``bytes``
        :return: the entry directory
        """
        self.check_key(key)
        final = self.entry_path(key)
        os.makedirs(self.root, exist_ok=True)
        with self.lock():
            from .FileHelpers import atomic_dir
            with atomic_dir(final) as tmp:
                for name, data in (files or {}).items():
                    self._check_filename(name)
                    if name == self.meta_name:
                        raise ValueError("`{}` is reserved".format(self.meta_name))
                    path = os.path.join(tmp, *name.split("/"))
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    atomic_write(path, data, fsync=False, keep_mode=False)
                atomic_write_json(os.path.join(tmp, self.meta_name), self._stamp(key, meta), sort_keys=True, fsync=False)
        return final

    @contextlib.contextmanager
    def stage(self, key, meta=None, replace=False):
        """
        Builds an entry in a temporary directory and publishes it when the block ends without an error.

        If ``meta`` is given it is stamped and written as the metadata file at the end (the yielded
        `StagedEntry.meta` can still be changed in the block); otherwise the block writes the metadata file
        itself. With ``replace=False`` an entry that already exists (typically written by a concurrent
        process) is kept and the staged copy is dropped.
        """
        self.check_key(key)
        final = self.entry_path(key)
        os.makedirs(self.root, exist_ok=True)
        tmp = os.path.join(self.root, "{}{}-{}".format(self.stage_prefix, key[:12], uuid.uuid4().hex))
        os.makedirs(tmp)
        staged = StagedEntry(self, key, tmp, None if meta is None else dict(meta))
        try:
            yield staged
            if staged.meta is not None:
                atomic_write_json(os.path.join(tmp, self.meta_name), self._stamp(key, staged.meta),
                                  sort_keys=True, fsync=False)
            elif not os.path.isfile(os.path.join(tmp, self.meta_name)):
                raise ValueError("a staged entry needs a `{}` file".format(self.meta_name))
            with self.lock():
                if os.path.isdir(final):
                    if self.has(key) and not replace:
                        return
                    shutil.rmtree(final)
                os.makedirs(os.path.dirname(final), exist_ok=True)
                try:
                    os.rename(tmp, final)
                except OSError as error:
                    if error.errno not in {errno.EEXIST, errno.ENOTEMPTY} or not self.has(key):
                        raise
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # ---- aliases ---- #
    def _alias_path(self, name):
        if not re.fullmatch(r"[0-9A-Za-z._-]+", name or "") or name.startswith("."):
            raise ValueError("invalid alias name: {!r}".format(name))
        return os.path.join(self.root, self.aliases_name, name + ".json")

    def set_alias(self, name, key):
        self.check_key(key)
        path = self._alias_path(name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        atomic_write_json(path, {self.alias_field: key}, sort_keys=True, fsync=False)

    def resolve_alias(self, name):
        """The key an alias points at, or ``None`` (also if the target entry is gone)."""
        path = self._alias_path(name)
        if not os.path.isfile(path):
            return None
        with open(path, encoding="utf-8") as f:
            key = json.load(f)[self.alias_field]
        self.check_key(key)
        return key if self.has(key) else None

    # ---- housekeeping ---- #
    def entry_size(self, key):
        """Total bytes of the files in an entry."""
        total = 0
        for base, _, names in os.walk(self.entry_path(key)):
            for name in names:
                total += os.path.getsize(os.path.join(base, name))
        return total

    def touch(self, key):
        """Marks an entry as just used (for `gc`'s least-recently-used order)."""
        try:
            os.utime(self.entry_path(key, self.meta_name), None)
        except OSError:
            pass

    def last_used(self, key):
        return os.stat(self.entry_path(key, self.meta_name)).st_mtime

    def _remove(self, key):
        shutil.rmtree(self.entry_path(key))
        if self.shard:
            shard = os.path.dirname(self.entry_path(key))
            if not os.listdir(shard):
                os.rmdir(shard)

    def prune(self, keep_keys, dry_run=False):
        """
        Removes entries whose key is not in ``keep_keys`` (and empty shard directories).

        :return: the keys that were (or, with ``dry_run``, would be) removed
        """
        keep = set(keep_keys)
        with self.lock():
            doomed = [k for k in self.keys() if k not in keep]
            if not dry_run:
                for k in doomed:
                    self._remove(k)
        return doomed

    def gc(self, max_bytes=None, max_age=None, protect=(), dry_run=False):
        """
        Removes entries older than ``max_age`` seconds (by last use) and then the least recently used ones
        until the store is at most ``max_bytes``. Keys in ``protect`` are never removed.

        :return: the removed keys, oldest first
        """
        protect = set(protect)
        with self.lock():
            now = time.time()
            entries = sorted(((self.last_used(k), k, self.entry_size(k)) for k in self.keys()))
            doomed = []
            if max_age is not None:
                doomed = [k for used, k, size in entries if now - used > max_age and k not in protect]
            kept = [(used, k, size) for used, k, size in entries if k not in doomed]
            if max_bytes is not None:
                total = sum(size for _, _, size in kept)
                for used, k, size in kept:
                    if total <= max_bytes:
                        break
                    if k not in protect:
                        doomed.append(k)
                        total -= size
            doomed = [k for _, k, _ in entries if k in set(doomed)]
            if not dry_run:
                for k in doomed:
                    self._remove(k)
        return doomed

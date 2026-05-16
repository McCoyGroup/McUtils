from __future__ import annotations
from typing import *

import io
import os
import pathlib
import json
import shutil
import hashlib
import tempfile
import base64

from . import Options as opts_handler

__all__ = [
    "is_filepath_like",
    "safe_open",
    "write_file",
    "read_file",
    "read_json",
    "write_json",
    "split_path",
    "drop_directory_prefix",
    "filename",
    "bytestream_hash",
    "string_hash",
    "file_hash",
    "files_hash",
    "directory_hash",
    "compress_dir",
    "compressed_dir_bytes",
    "decompress_dir",
    "unpack_gzip_bytes",
    "FileBackedIO",
    "StreamInterface",
]

bad_file_chars = {" ", "\t", "\n"}
def is_filepath_like(file, bad_chars=None):
    if bad_chars is None:
        bad_chars = bad_file_chars
    return isinstance(file, pathlib.Path) or (
        isinstance(file, str)
        and all(b not in file for b in bad_chars)
    )

class safe_open:
    def __init__(self, file, **opts):
        self.file = file
        self._stream = None
        self.opts = opts
    def __enter__(self):
        if hasattr(self.file, 'seek'):
            return self.file
        else:
            self._stream = open(self.file, **self.opts)
            return self._stream.__enter__()
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._stream is not None:
            return self._stream.__exit__(exc_type, exc_val, exc_tb)

class open_opts:
    mode: 'str'
    buffering: 'int'
    encoding: 'str | None'
    errors: 'str | None'
    newline: 'str | None'
    closefd: 'bool'
    opener: '(str, int)'

def write_file(file, data, mode='w+', **opts):
    with safe_open(file, mode=mode, **opts) as fs:
        fs.write(data)
    return file

def read_file(file, **opts):
    with safe_open(file, **opts) as fs:
        return fs.read()

def read_json(file, **opts):
    opts, js_opts = opts_handler.OptionsSet(opts).split(open_opts)
    with safe_open(file, **opts) as fs:
        return json.load(fs, **js_opts)

def write_json(file, data, mode="w+", **opts):
    opts, js_opts = opts_handler.OptionsSet(opts).split(open_opts)
    with safe_open(file, mode=mode, **opts) as fs:
        return json.dump(data, fs)

def split_path(path, nsteps=-1):
    if len(path) == 0:
        return []

    if isinstance(path, pathlib.Path):
        splitter = lambda p:(p.parent,p.name)
    else:
        splitter = lambda p:(("","") if p == os.path.sep else os.path.split(p))
    if nsteps < 0:
        subpath = []
        root = path
        while len(root) > 0:
            root, end = splitter(root)
            subpath.append(end)
        return subpath[::-1]
    else:
        subpath = []
        root = path
        for i in range(nsteps):
            root, end = splitter(root)
            subpath.append(end)
            if len(root) == 0:
                break
        return [root] + subpath[::-1]

def drop_directory_prefix(prefix, path):
    split1 = split_path(prefix)
    split2 = split_path(path)
    i = -1
    for i,(s1,s2) in enumerate(zip(split1, split2)):
        if s1 != s2:
            break

    if i+1 < len(split2):
        subsplit = split2[i+1:]
        if subsplit[0] == "":
            subsplit[0] = os.path.sep
        subpath = os.path.join(*subsplit)
    else:
        subpath = ""

    if isinstance(path, pathlib.Path):
        subpath = pathlib.Path(subpath)
    return subpath

def filename(path, check_dir=True):
    split = os.path.splitext(os.path.basename(path))
    if check_dir and len(split[1]) == 0:
        return None
    else:
        return split[0]

HASH_TYPE = hashlib.md5
def _update_fs_hash(fs, sha, buff):
    mv = memoryview(buff)
    while n := fs.readinto(mv):
        sha.update(mv[:n])

def _digest_hash(sha, base, bits=None, id_generator=None):
    digest = sha.digest()
    if bits is not None:
        digest = digest[:bits]
    if (
            id_generator is None
            or id_generator is str
            or (isinstance(id_generator, str) and id_generator == 'str')
    ):
        if base == 85:
            hash = base64.b85encode(digest).decode()
        elif base == 64:
            hash = base64.b64encode(digest).decode()
        else:# base == 16:
            hash = base64.b16encode(digest).decode()
        hash = hash.replace("/", '-')
    elif (
            id_generator is int
            or (isinstance(id_generator, str) and id_generator == 'int')
    ):
        hash = int.from_bytes(digest, byteorder='little')
    else:
        hash = id_generator(digest)
    # else:
    #     hash = sha.hexdigest()
    return hash

def string_hash(string, base=None, bits=None, id_generator=None):
    with io.BytesIO(string.encode('utf-8')) as buf:
        return bytestream_hash(buf, base, bits=bits, id_generator=id_generator)

HASH_ENCODING_BASE = 64
def bytestream_hash(filestream, base=None, bits=None, id_generator=None):
    """
    https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
    """
    h = HASH_TYPE()
    b = bytearray(128 * 1024)
    _update_fs_hash(filestream, h, b)
    if base is None:
        base = HASH_ENCODING_BASE
    return _digest_hash(h, base, bits=bits, id_generator=id_generator)

def file_hash(filename, base=None, bits=None, id_generator=None):
    with open(filename, 'rb', buffering=0) as fs:
        return bytestream_hash(fs, base=base, bits=bits, id_generator=id_generator)

def files_hash(files, base=None, bits=None, id_generator=None):
    h = HASH_TYPE()
    b = bytearray(128 * 1024)
    for filename in files:
        with open(filename, 'rb', buffering=0) as fs:
            _update_fs_hash(fs, h, b)
    if base is None:
        base = HASH_ENCODING_BASE
    return _digest_hash(h, base, bits=bits, id_generator=id_generator)
def directory_hash(directory, files=None, base=None, bits=None, id_generator=None):
    if files is None:
        files = os.listdir(directory)
    files = [
        os.path.join(directory, fn)
        for fn in files
    ]
    return files_hash(files, base=base, bits=bits, id_generator=id_generator)

def compress_dir(config_dir, cache_dir=None, name=None, files=None):
    if files is None:
        files = os.listdir(config_dir)
    if name is None:
        name = os.path.basename(config_dir)
    if cache_dir is None:
        cache_dir = os.path.dirname(config_dir)
    curdir = os.getcwd()
    try:
        os.chdir(cache_dir)
        with tempfile.TemporaryDirectory() as td:
            os.makedirs(os.path.join(td, name))
            for f in files:
                shutil.copy(
                    os.path.join(config_dir, f),
                    os.path.join(td, name, f)
                )
            return shutil.make_archive(
                name,
                format='gztar',
                root_dir=td,
                base_dir=name
            )
    finally:
        os.chdir(curdir)

def compressed_dir_bytes(config_dir, name=None, files=None):
    with tempfile.TemporaryDirectory() as td:
        gzip = compress_dir(config_dir, cache_dir=td, name=name, files=files)
        return read_file(gzip)

def decompress_dir(target_dir, config_gzip):
    shutil.unpack_archive(config_gzip, target_dir)

def unpack_gzip_bytes(build_dir, gzip:bytes):
    with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as tf:
        tf.write(gzip)
    try:
        shutil.unpack_archive(tf.name, build_dir, format="gztar")
    finally:
        if os.path.exists(tf.name):
            os.remove(tf.name)


class FileBackedIO:
    def __init__(self, buffer:str|bytes|Callable[[], str|bytes], mode='w+', file=None, delete=True, **tempfile_opts):
        self.mode = mode
        self.opts = tempfile_opts
        self.buf = buffer
        self._file = file
        self._stream = None
        self.delete = delete

    def resolve_buffer(self):
        b = self.buf
        if not isinstance(b, (str, bytes)):
            b: str | bytes = b()
        return b
    @property
    def name(self):
        if self._file is not None:
            if isinstance(self._file, str):
                return self._file
            else:
                return self._file.name
        else:
            return None
    @property
    def file(self):
        if self._file is None:
            if 'b' in self.mode:
                submode = 'w+b'
            else:
                submode = 'w+'
            with tempfile.NamedTemporaryFile(mode=submode, delete=False, **self.opts) as base:
                if 'w' not in self.mode:
                    base.write(self.resolve_buffer())
            self._file = base.name
        return self._file

    def write(self, file=None, mode=None):
        if mode is None:
            mode = self.mode
        if 'w' not in mode and 'a' not in mode:
            mode = mode.replace('r', 'w')
        if file is None: file = self.file
        with open(file, mode) as stream:
            stream.write(self.resolve_buffer())
        return file

    def __enter__(self):
        if self._stream is None:
            self._stream = open(self.file, self.mode).__enter__()
            if 'w' in self.mode:
                self._stream.write(self.resolve_buffer())
                self._stream.seek(0)
        return self._stream
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stream.__exit__(exc_type, exc_val, exc_tb)
        if self.delete:
            os.remove(self._file)

class StreamInterface:
    def __init__(self, stream, file_backed=False, **file_opts):
        self._input = stream
        self._io_wrapper = None
        self._stream = None
        self.file_backed = file_backed
        self.file_opts = file_opts
        self._was_open = None

    def is_binary(self):
        if isinstance(self._input, (str, bytes)):
            return "b" in self.file_opts.get('mode', '')
        else:
            return "b" in self._input.mode

    def get_encoding(self):
        if isinstance(self._input, (str, bytes)):
            return self.file_opts.get('encoding', 'utf-8')
        else:
            return self._input.encoding

    @classmethod
    def is_path_like(cls, input):
        return (len(input) > 0 and all(k not in input for k in ["\n", ",", "(", ")"]))

    def __enter__(self):
        if isinstance(self._input, str) and (os.path.exists(self._input) or self.is_path_like(self._input)):
            self._was_open = False
            self._io_wrapper = open(self._input, **self.file_opts)
            self._stream = self._io_wrapper.__enter__()
        elif isinstance(self._input, (str, bytes)):
            self._was_open = False
            if self.file_backed:
                self._io_wrapper = FileBackedIO(self._input, **self.file_opts)
            elif isinstance(self._input, str):
                self._io_wrapper = io.StringIO(self._input)
            else:
                self._io_wrapper = io.BytesIO(self._input)
            self._stream = self._io_wrapper.__enter__()
        else:
            self._was_open = True
            self._stream = self._input
        return self._stream

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._was_open is False:
            if self._io_wrapper is not None:
                try:
                    self._io_wrapper.__exit__(exc_type, exc_val, exc_tb)
                finally:
                    self._io_wrapper = None
            else:
                self._stream.__exit__(exc_type, exc_val, exc_tb)
            self._stream = None
            self._was_open = None
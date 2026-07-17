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
    """
    **LLM Docstring**

    Test whether a value looks like a file path (a `Path`, or a string free of
    whitespace/other bad characters).

    :param file: the value to test
    :param bad_chars: characters that disqualify a string (defaults to whitespace)
    :type bad_chars: set | None
    :return: whether it looks path-like
    :rtype: bool
    """
    if bad_chars is None:
        bad_chars = bad_file_chars
    return isinstance(file, pathlib.Path) or (
        isinstance(file, str)
        and all(b not in file for b in bad_chars)
    )

class safe_open:
    def __init__(self, file, **opts):
        """
        **LLM Docstring**

        Context manager that opens a file path, or passes through an already-open
        stream.

        :param file: the file path or open stream
        :param opts: options forwarded to `open`
        """
        self.file = file
        self._stream = None
        self.opts = opts
    def __enter__(self):
        """
        **LLM Docstring**

        Return the stream: the passed-in object if it's already stream-like, else a
        freshly opened file.

        :return: the open stream
        """
        if hasattr(self.file, 'seek'):
            return self.file
        else:
            self._stream = open(self.file, **self.opts)
            return self._stream.__enter__()
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Close the stream if this manager opened it.

        :param exc_type: the exception type, if any
        :param exc_val: the exception value, if any
        :param exc_tb: the traceback, if any
        """
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
    """
    **LLM Docstring**

    Write data to a file (path or stream).

    :param file: the file path or stream
    :param data: the data to write
    :param mode: the open mode
    :type mode: str
    :param opts: options forwarded to `open`
    :return: the file
    """
    with safe_open(file, mode=mode, **opts) as fs:
        fs.write(data)
    return file

def read_file(file, **opts):
    """
    **LLM Docstring**

    Read the full contents of a file (path or stream).

    :param file: the file path or stream
    :param opts: options forwarded to `open`
    :return: the file contents
    """
    with safe_open(file, **opts) as fs:
        return fs.read()

def read_json(file, loader=None, **opts):
    """
    **LLM Docstring**

    Read and parse JSON from a file, separating `open` options from loader options.

    :param file: the file path or stream
    :param loader: the JSON loader (defaults to `json.load`)
    :type loader: Callable | None
    :param opts: mixed `open` and loader options
    :return: the parsed JSON
    """
    opts, js_opts = opts_handler.OptionsSet(opts).split(open_opts)
    with safe_open(file, **opts) as fs:
        if loader is None:
            loader = json.load
        return loader(fs, **js_opts)

def read_orjson(file, loader=None, mode='rb', **opts):
    """
    **LLM Docstring**

    Read and parse JSON from a file using `orjson`.

    :param file: the file path or stream
    :param loader: an explicit loader
    :type loader: Callable | None
    :param mode: the open mode
    :type mode: str
    :param opts: options forwarded to `read_json`
    :return: the parsed JSON
    """
    import orjson
    if loader is None:
        loader = lambda fs: orjson.loads(fs.read())
    return read_json(file, loader=loader, mode=mode, **opts)

def write_json(file, data, writer=None, mode="w+", encoder=None, **opts):
    """
    **LLM Docstring**

    Serialize data to a file as JSON, separating `open` options from dumper options
    and supporting a custom encoder class or default function.

    :param file: the file path or stream
    :param data: the data to serialize
    :param writer: the JSON writer (defaults to `json.dump`)
    :type writer: Callable | None
    :param mode: the open mode
    :type mode: str
    :param encoder: a JSON encoder class or default-serializer function
    :param opts: mixed `open` and dumper options
    :return: the writer's result
    """
    opts, js_opts = opts_handler.OptionsSet(opts).split(open_opts)
    if encoder is not None:
        if isinstance(encoder, type):
            js_opts['cls'] = encoder
        else:
            js_opts['default'] = encoder
    with safe_open(file, mode=mode, **opts) as fs:
        if writer is None:
            writer = json.dump
        return writer(data, fs, **js_opts)

def write_orjson(file, data, writer=None, mode='w+b', **opts):
    """
    **LLM Docstring**

    Serialize data to a file as JSON using `orjson`.

    :param file: the file path or stream
    :param data: the data to serialize
    :param writer: an explicit writer
    :type writer: Callable | None
    :param mode: the open mode
    :type mode: str
    :param opts: options forwarded to `write_json`
    :return: the writer's result
    """
    import orjson
    if writer is None:
        writer = lambda data, fs: fs.write(orjson.dumps(data))
    return write_json(file, data, writer=writer, mode=mode, **opts)

def split_path(path, nsteps=-1):
    """
    **LLM Docstring**

    Split a path into its components, either fully (`nsteps < 0`) or only the last
    `nsteps` (returning the remaining root as the first element).

    :param path: the path (string or `Path`)
    :param nsteps: the number of trailing components to split off (all if negative)
    :type nsteps: int
    :return: the path components
    :rtype: list
    """
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
    """
    **LLM Docstring**

    Return `path` with the leading portion it shares with `prefix` removed.

    :param prefix: the prefix path
    :param path: the path to trim
    :return: the path relative to the shared prefix
    """
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
    """
    **LLM Docstring**

    Return the base filename (without extension), optionally requiring that the path
    actually has an extension.

    :param path: the path
    :param check_dir: return `None` when there's no extension (treating it as a directory)
    :type check_dir: bool
    :return: the filename stem, or `None`
    :rtype: str | None
    """
    split = os.path.splitext(os.path.basename(path))
    if check_dir and len(split[1]) == 0:
        return None
    else:
        return split[0]

HASH_TYPE = hashlib.md5
def _update_fs_hash(fs, sha, buff):
    """
    **LLM Docstring**

    Feed a file stream into a hash object in chunks via a reusable buffer.

    :param fs: the readable byte stream
    :param sha: the hash object (updated in place)
    :param buff: the reusable byte buffer
    """
    mv = memoryview(buff)
    while n := fs.readinto(mv):
        sha.update(mv[:n])

def _digest_hash(sha, base, bits=None, id_generator=None):
    """
    **LLM Docstring**

    Turn a hash object's digest into an encoded id: a base-16/64/85 string, an
    integer, or the output of a custom generator, optionally truncated.

    :param sha: the hash object
    :param base: the string-encoding base (16/64/85)
    :type base: int
    :param bits: truncate the digest to this many bytes
    :type bits: int | None
    :param id_generator: `str`/`int`/`'str'`/`'int'` or a custom digest transformer
    :return: the encoded hash
    """
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
    """
    **LLM Docstring**

    Hash a string (via its UTF-8 bytes).

    :param string: the string to hash
    :type string: str
    :param base: the string-encoding base
    :type base: int | None
    :param bits: truncate the digest to this many bytes
    :type bits: int | None
    :param id_generator: the id encoding (see `_digest_hash`)
    :return: the hash
    """
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
    """
    **LLM Docstring**

    Hash the contents of a file.

    :param filename: the file path
    :type filename: str
    :param base: the string-encoding base
    :type base: int | None
    :param bits: truncate the digest to this many bytes
    :type bits: int | None
    :param id_generator: the id encoding
    :return: the hash
    """
    with open(filename, 'rb', buffering=0) as fs:
        return bytestream_hash(fs, base=base, bits=bits, id_generator=id_generator)

def files_hash(files, base=None, bits=None, id_generator=None):
    """
    **LLM Docstring**

    Hash the concatenated contents of several files into a single digest.

    :param files: the file paths
    :type files: Iterable[str]
    :param base: the string-encoding base
    :type base: int | None
    :param bits: truncate the digest to this many bytes
    :type bits: int | None
    :param id_generator: the id encoding
    :return: the combined hash
    """
    h = HASH_TYPE()
    b = bytearray(128 * 1024)
    for filename in files:
        with open(filename, 'rb', buffering=0) as fs:
            _update_fs_hash(fs, h, b)
    if base is None:
        base = HASH_ENCODING_BASE
    return _digest_hash(h, base, bits=bits, id_generator=id_generator)
def directory_hash(directory, files=None, base=None, bits=None, id_generator=None):
    """
    **LLM Docstring**

    Hash the contents of a directory's files.

    :param directory: the directory path
    :type directory: str
    :param files: the file names to include (defaults to all)
    :type files: Iterable[str] | None
    :param base: the string-encoding base
    :type base: int | None
    :param bits: truncate the digest to this many bytes
    :type bits: int | None
    :param id_generator: the id encoding
    :return: the directory hash
    """
    if files is None:
        files = os.listdir(directory)
    files = [
        os.path.join(directory, fn)
        for fn in files
    ]
    return files_hash(files, base=base, bits=bits, id_generator=id_generator)

def compress_dir(config_dir, cache_dir=None, name=None, files=None):
    """
    **LLM Docstring**

    Create a gzipped tar archive of (some of) a directory's files.

    :param config_dir: the directory to archive
    :type config_dir: str
    :param cache_dir: where to write the archive (defaults to the parent directory)
    :type cache_dir: str | None
    :param name: the archive base name (defaults to the directory name)
    :type name: str | None
    :param files: the file names to include (defaults to all)
    :type files: Iterable[str] | None
    :return: the archive path
    :rtype: str
    """
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
    """
    **LLM Docstring**

    Return the raw bytes of a gzipped tar archive of a directory.

    :param config_dir: the directory to archive
    :type config_dir: str
    :param name: the archive base name
    :type name: str | None
    :param files: the file names to include
    :type files: Iterable[str] | None
    :return: the archive bytes
    :rtype: bytes
    """
    with tempfile.TemporaryDirectory() as td:
        gzip = compress_dir(config_dir, cache_dir=td, name=name, files=files)
        return read_file(gzip)

def decompress_dir(target_dir, config_gzip):
    """
    **LLM Docstring**

    Unpack an archive into a target directory.

    :param target_dir: the destination directory
    :type target_dir: str
    :param config_gzip: the archive path
    :type config_gzip: str
    """
    shutil.unpack_archive(config_gzip, target_dir)

def unpack_gzip_bytes(build_dir, gzip:bytes):
    """
    **LLM Docstring**

    Unpack a gzipped tar archive supplied as raw bytes into a directory (via a
    temporary file).

    :param build_dir: the destination directory
    :type build_dir: str
    :param gzip: the archive bytes
    :type gzip: bytes
    """
    with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as tf:
        tf.write(gzip)
    try:
        shutil.unpack_archive(tf.name, build_dir, format="gztar")
    finally:
        if os.path.exists(tf.name):
            os.remove(tf.name)


class FileBackedIO:
    def __init__(self, buffer:str|bytes|Callable[[], str|bytes], mode='w+', file=None, delete=True, **tempfile_opts):
        """
        **LLM Docstring**

        A stream-like wrapper backing an in-memory (or lazily generated) buffer with a
        temporary file.

        :param buffer: the buffer content, or a callable producing it
        :type buffer: str | bytes | Callable
        :param mode: the open mode
        :type mode: str
        :param file: an explicit backing file
        :param delete: delete the backing file on exit
        :type delete: bool
        :param tempfile_opts: options for the temporary file
        """
        self.mode = mode
        self.opts = tempfile_opts
        self.buf = buffer
        self._file = file
        self._stream = None
        self.delete = delete

    def resolve_buffer(self):
        """
        **LLM Docstring**

        Return the buffer contents, calling the generator if the buffer is a callable.

        :return: the buffer contents
        :rtype: str | bytes
        """
        b = self.buf
        if not isinstance(b, (str, bytes)):
            b: str | bytes = b()
        return b
    @property
    def name(self):
        """
        **LLM Docstring**

        The backing file's path (or `None` if not yet created).

        :return: the file path
        :rtype: str | None
        """
        if self._file is not None:
            if isinstance(self._file, str):
                return self._file
            else:
                return self._file.name
        else:
            return None
    @property
    def file(self):
        """
        **LLM Docstring**

        The backing file path, creating (and seeding) a temporary file on first access.

        :return: the file path
        :rtype: str
        """
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
        """
        **LLM Docstring**

        Write the buffer contents out to a file.

        :param file: the destination file (defaults to the backing file)
        :param mode: the open mode (coerced to a writing mode)
        :type mode: str | None
        :return: the file written
        """
        if mode is None:
            mode = self.mode
        if 'w' not in mode and 'a' not in mode:
            mode = mode.replace('r', 'w')
        if file is None: file = self.file
        with open(file, mode) as stream:
            stream.write(self.resolve_buffer())
        return file

    def __enter__(self):
        """
        **LLM Docstring**

        Open the backing file as a stream, seeding it from the buffer in write modes.

        :return: the open stream
        """
        if self._stream is None:
            self._stream = open(self.file, self.mode).__enter__()
            if 'w' in self.mode:
                self._stream.write(self.resolve_buffer())
                self._stream.seek(0)
        return self._stream
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Close the stream and (optionally) delete the backing file.

        :param exc_type: the exception type, if any
        :param exc_val: the exception value, if any
        :param exc_tb: the traceback, if any
        """
        self._stream.__exit__(exc_type, exc_val, exc_tb)
        if self.delete:
            os.remove(self._file)

class StreamInterface:
    def __init__(self, stream, file_backed=False, **file_opts):
        """
        **LLM Docstring**

        Uniform context manager over a stream: accepts an open stream, a file path, or
        raw string/bytes content.

        :param stream: the stream, file path, or raw content
        :param file_backed: back raw content with a temporary file rather than an in-memory buffer
        :type file_backed: bool
        :param file_opts: options for opening/creating the stream
        """
        self._input = stream
        self._io_wrapper = None
        self._stream = None
        self.file_backed = file_backed
        self.file_opts = file_opts
        self._was_open = None

    def is_binary(self):
        """
        **LLM Docstring**

        Whether the stream is (or would be opened in) binary mode.

        :return: whether the stream is binary
        :rtype: bool
        """
        if isinstance(self._input, (str, bytes)):
            return "b" in self.file_opts.get('mode', '')
        else:
            return "b" in self._input.mode

    def get_encoding(self):
        """
        **LLM Docstring**

        The stream's text encoding.

        :return: the encoding
        :rtype: str
        """
        if isinstance(self._input, (str, bytes)):
            return self.file_opts.get('encoding', 'utf-8')
        else:
            return self._input.encoding

    @classmethod
    def is_path_like(cls, input):
        """
        **LLM Docstring**

        Heuristic test for whether a string is a path rather than inline content (no
        newlines, commas, or parentheses).

        :param input: the string to test
        :type input: str
        :return: whether it looks like a path
        :rtype: bool
        """
        return (len(input) > 0 and all(k not in input for k in ["\n", ",", "(", ")"]))

    def __enter__(self):
        """
        **LLM Docstring**

        Resolve the input into an open stream: open a file path, wrap raw content in a
        buffer/file-backed stream, or pass through an already-open stream.

        :return: the open stream
        """
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
        """
        **LLM Docstring**

        Close any stream/buffer this interface opened, leaving already-open inputs alone.

        :param exc_type: the exception type, if any
        :param exc_val: the exception value, if any
        :param exc_tb: the traceback, if any
        """
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
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
__all__ = ['is_filepath_like', 'safe_open', 'write_file', 'read_file', 'read_json', 'write_json', 'split_path', 'drop_directory_prefix', 'filename', 'bytestream_hash', 'string_hash', 'file_hash', 'files_hash', 'directory_hash', 'compress_dir', 'compressed_dir_bytes', 'decompress_dir', 'unpack_gzip_bytes', 'FileBackedIO', 'StreamInterface']
bad_file_chars = {' ', '\t', '\n'}

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
    ...

class safe_open:

    def __init__(self, file, **opts):
        """
        **LLM Docstring**

        Context manager that opens a file path, or passes through an already-open
        stream.

        :param file: the file path or open stream
        :param opts: options forwarded to `open`
        """
        ...

    def __enter__(self):
        """
        **LLM Docstring**

        Return the stream: the passed-in object if it's already stream-like, else a
        freshly opened file.

        :return: the open stream
        """
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Close the stream if this manager opened it.

        :param exc_type: the exception type, if any
        :param exc_val: the exception value, if any
        :param exc_tb: the traceback, if any
        """
        ...

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
    ...

def read_file(file, **opts):
    """
    **LLM Docstring**

    Read the full contents of a file (path or stream).

    :param file: the file path or stream
    :param opts: options forwarded to `open`
    :return: the file contents
    """
    ...

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
    ...

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
    ...

def write_json(file, data, writer=None, mode='w+', encoder=None, **opts):
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
    ...

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
    ...

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
    ...

def drop_directory_prefix(prefix, path):
    """
    **LLM Docstring**

    Return `path` with the leading portion it shares with `prefix` removed.

    :param prefix: the prefix path
    :param path: the path to trim
    :return: the path relative to the shared prefix
    """
    ...

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
    ...
HASH_TYPE = hashlib.md5

def _update_fs_hash(fs, sha, buff):
    """
    **LLM Docstring**

    Feed a file stream into a hash object in chunks via a reusable buffer.

    :param fs: the readable byte stream
    :param sha: the hash object (updated in place)
    :param buff: the reusable byte buffer
    """
    ...

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
    ...

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
    ...
HASH_ENCODING_BASE = 64

def bytestream_hash(filestream, base=None, bits=None, id_generator=None):
    """
    https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
    """
    ...

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
    ...

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
    ...

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
    ...

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
    ...

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
    ...

def decompress_dir(target_dir, config_gzip):
    """
    **LLM Docstring**

    Unpack an archive into a target directory.

    :param target_dir: the destination directory
    :type target_dir: str
    :param config_gzip: the archive path
    :type config_gzip: str
    """
    ...

def unpack_gzip_bytes(build_dir, gzip: bytes):
    """
    **LLM Docstring**

    Unpack a gzipped tar archive supplied as raw bytes into a directory (via a
    temporary file).

    :param build_dir: the destination directory
    :type build_dir: str
    :param gzip: the archive bytes
    :type gzip: bytes
    """
    ...

class FileBackedIO:

    def __init__(self, buffer: str | bytes | Callable[[], str | bytes], mode='w+', file=None, delete=True, **tempfile_opts):
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
        ...

    def resolve_buffer(self):
        """
        **LLM Docstring**

        Return the buffer contents, calling the generator if the buffer is a callable.

        :return: the buffer contents
        :rtype: str | bytes
        """
        ...

    @property
    def name(self):
        """
        **LLM Docstring**

        The backing file's path (or `None` if not yet created).

        :return: the file path
        :rtype: str | None
        """
        ...

    @property
    def file(self):
        """
        **LLM Docstring**

        The backing file path, creating (and seeding) a temporary file on first access.

        :return: the file path
        :rtype: str
        """
        ...

    def write(self, file=None, mode=None):
        """
        **LLM Docstring**

        Write the buffer contents out to a file.

        :param file: the destination file (defaults to the backing file)
        :param mode: the open mode (coerced to a writing mode)
        :type mode: str | None
        :return: the file written
        """
        ...

    def __enter__(self):
        """
        **LLM Docstring**

        Open the backing file as a stream, seeding it from the buffer in write modes.

        :return: the open stream
        """
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Close the stream and (optionally) delete the backing file.

        :param exc_type: the exception type, if any
        :param exc_val: the exception value, if any
        :param exc_tb: the traceback, if any
        """
        ...

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
        ...

    def is_binary(self):
        """
        **LLM Docstring**

        Whether the stream is (or would be opened in) binary mode.

        :return: whether the stream is binary
        :rtype: bool
        """
        ...

    def get_encoding(self):
        """
        **LLM Docstring**

        The stream's text encoding.

        :return: the encoding
        :rtype: str
        """
        ...

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
        ...

    def __enter__(self):
        """
        **LLM Docstring**

        Resolve the input into an open stream: open a file path, wrap raw content in a
        buffer/file-backed stream, or pass through an already-open stream.

        :return: the open stream
        """
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Close any stream/buffer this interface opened, leaving already-open inputs alone.

        :param exc_type: the exception type, if any
        :param exc_val: the exception value, if any
        :param exc_tb: the traceback, if any
        """
        ...
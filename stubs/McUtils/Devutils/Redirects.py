import sys, os
import tempfile as tf, io
import contextlib
__all__ = ['StreamRedirect', 'OutputRedirect', 'DefaultDirectory', 'temporary_sys_path_insert']

@contextlib.contextmanager
def temporary_sys_path_insert(path):
    ...

class StreamRedirect:

    def __init__(self, logger, base_stream=None, line_join=True, strip_empty=True):
        """
        **LLM Docstring**

        Wrap a logging callback as a writable stream, so writes are forwarded to the
        logger.

        :param logger: the callback invoked with written data
        :type logger: Callable
        :param base_stream: an underlying stream to delegate reads/seeks/flush to
        :param line_join: joiner for `writelines` (`True` uses `''`), or `None` to pass lines through
        :param strip_empty: drop whitespace-only writes
        :type strip_empty: bool
        """
        ...

    def write(self, data):
        """
        **LLM Docstring**

        Forward written data to the logger, skipping whitespace-only data when
        `strip_empty` is set.

        :param data: the data to write
        """
        ...

    def writelines(self, lines):
        """
        **LLM Docstring**

        Forward multiple lines to the logger, joining them with the configured joiner
        (encoding it for bytes lines) or passing them through when no joiner is set.

        :param lines: the lines to write
        :type lines: Sequence
        """
        ...

    def flush(self):
        """
        **LLM Docstring**

        Flush the underlying base stream, if any.
        """
        ...

    def seek(self, offset: int, whence: int=0):
        """
        **LLM Docstring**

        Seek on the underlying base stream, if any.

        :param offset: the seek offset
        :type offset: int
        :param whence: the seek origin
        :type whence: int
        :return: the new position, or `None`
        """
        ...

    def seekable(self):
        """
        **LLM Docstring**

        Whether the underlying base stream is seekable.

        :return: whether seeking is supported
        :rtype: bool
        """
        ...

    def read(self, size):
        """
        **LLM Docstring**

        Read from the underlying base stream, if any.

        :param size: the number of bytes/characters to read
        :return: the data read, or `None`
        """
        ...

    def readline(self, limit: int=-1):
        """
        **LLM Docstring**

        Read a line from the underlying base stream, if any.

        :param limit: the maximum number of bytes/characters
        :type limit: int
        :return: the line read, or `None`
        """
        ...

    def readlines(self, hint: int=-1):
        """
        **LLM Docstring**

        Read all lines from the underlying base stream, if any.

        :param hint: an approximate byte-count hint
        :type hint: int
        :return: the lines read, or `None`
        """
        ...

class OutputRedirect:

    def __init__(self, redirect=True, stdout=None, stderr=None, capture_output=False, capture_errors=None, file_handles=False):
        """
        **LLM Docstring**

        Context manager that redirects `stdout`/`stderr`, optionally capturing them to
        in-memory buffers, files, or discarding them.

        :param redirect: whether to actually redirect
        :type redirect: bool
        :param stdout: an explicit stdout target (stream or file path)
        :param stderr: an explicit stderr target (stream or file path)
        :param capture_output: capture stdout to a buffer/temp file
        :type capture_output: bool
        :param capture_errors: capture stderr (defaults to `capture_output`)
        :type capture_errors: bool | None
        :param file_handles: use file handles rather than in-memory buffers when capturing
        :type file_handles: bool
        """
        ...

    @classmethod
    def get_handle(cls, handles=None, file_handles=False):
        """
        **LLM Docstring**

        Resolve a capture target: return the supplied handle, a fresh in-memory buffer,
        or `None` (for a file handle to be created later).

        :param handles: an explicit handle
        :param file_handles: prefer a file handle (returns `None`) over a buffer
        :type file_handles: bool
        :return: the capture handle, or `None`
        """
        ...

    @classmethod
    def get_temp_stream(cls):
        """
        **LLM Docstring**

        Open and enter a writable named temporary file to capture output into.

        :return: the temporary file stream
        """
        ...

    def __enter__(self):
        """
        **LLM Docstring**

        Redirect `sys.stdout`/`sys.stderr` to the configured targets (buffers, temp
        files, given streams/paths, or the null device), saving the originals.
        """
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Restore the original `sys.stdout`/`sys.stderr` and close any streams opened on
        entry.

        :param exc_type: the exception type, if any
        :param exc_val: the exception value, if any
        :param exc_tb: the traceback, if any
        """
        ...

class DefaultDirectory:

    def __init__(self, output_dir=None, chdir=True, **tempdir_opts):
        """
        **LLM Docstring**

        Context manager providing a working directory (a given one, or a fresh temporary
        one), optionally `chdir`-ing into it.

        :param output_dir: the directory to use (a temp dir is created if omitted)
        :type output_dir: str | None
        :param chdir: change into the directory on enter
        :type chdir: bool
        :param tempdir_opts: options for the temporary-directory creation
        """
        ...

    def get_temp_dir(self):
        """
        **LLM Docstring**

        Create a `TemporaryDirectory` using the stored options.

        :return: the temporary directory
        """
        ...

    @property
    def dirname(self):
        """
        **LLM Docstring**

        The path of the managed directory (or `None` before entering).

        :return: the directory path
        :rtype: str | None
        """
        ...

    def __enter__(self):
        """
        **LLM Docstring**

        Establish the directory (creating a temp dir if needed) and optionally `chdir`
        into it, returning its path.

        :return: the directory path
        :rtype: str
        """
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Restore the previous working directory and clean up the temporary directory if
        one was created.

        :param exc_type: the exception type, if any
        :param exc_val: the exception value, if any
        :param exc_tb: the traceback, if any
        """
        ...
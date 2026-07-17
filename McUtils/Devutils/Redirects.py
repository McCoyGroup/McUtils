import sys, os
import tempfile as tf, io

__all__ = [
    "StreamRedirect",
    "OutputRedirect",
    "DefaultDirectory"
]

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
        self._redirect = logger
        if line_join is True:
            line_join = ""
        self._line_join = line_join
        self.strip_empty = strip_empty
        self.base_stream = base_stream
    def write(self, data):
        """
        **LLM Docstring**

        Forward written data to the logger, skipping whitespace-only data when
        `strip_empty` is set.

        :param data: the data to write
        """
        if self.strip_empty and len(data.strip()) == 0:
            ...
        else:
            self._redirect(data)
    def writelines(self, lines):
        """
        **LLM Docstring**

        Forward multiple lines to the logger, joining them with the configured joiner
        (encoding it for bytes lines) or passing them through when no joiner is set.

        :param lines: the lines to write
        :type lines: Sequence
        """
        if self._line_join is not None:
            lj = self._line_join
            if not isinstance(lines[0], str) and isinstance(lj, str):
                lj = lj.encode()
            self.write(lj.join(lines))
        else:
            if self.strip_empty and len(lines) == 0:
                ...
            else:
                self._redirect(lines)
    def flush(self):
        """
        **LLM Docstring**

        Flush the underlying base stream, if any.
        """
        if self.base_stream is not None:
            self.base_stream.flush()
    def seek(self, offset: int, whence: int = 0):
        """
        **LLM Docstring**

        Seek on the underlying base stream, if any.

        :param offset: the seek offset
        :type offset: int
        :param whence: the seek origin
        :type whence: int
        :return: the new position, or `None`
        """
        if self.base_stream is not None:
            return self.base_stream.seek(offset, whence)
        else:
            return None
    def seekable(self):
        """
        **LLM Docstring**

        Whether the underlying base stream is seekable.

        :return: whether seeking is supported
        :rtype: bool
        """
        if self.base_stream is not None:
            return self.base_stream.seekable()
        else:
            return False
    def read(self, size):
        """
        **LLM Docstring**

        Read from the underlying base stream, if any.

        :param size: the number of bytes/characters to read
        :return: the data read, or `None`
        """
        if self.base_stream is not None:
            return self.base_stream.read(size)
        else:
            return None
    def readline(self, limit:int=-1):
        """
        **LLM Docstring**

        Read a line from the underlying base stream, if any.

        :param limit: the maximum number of bytes/characters
        :type limit: int
        :return: the line read, or `None`
        """
        if self.base_stream is not None:
            return self.base_stream.readline(limit)
        else:
            return None
    def readlines(self, hint: int=-1):
        """
        **LLM Docstring**

        Read all lines from the underlying base stream, if any.

        :param hint: an approximate byte-count hint
        :type hint: int
        :return: the lines read, or `None`
        """
        if self.base_stream is not None:
            return self.base_stream.readlines(hint)
        else:
            return None

class OutputRedirect:
    def __init__(self,
                 redirect=True,
                 stdout=None, stderr=None,
                 capture_output=False,
                 capture_errors=None,
                 file_handles=False
                 ):
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
        self.redirect = redirect
        if capture_errors is None:
            capture_errors = capture_output
        self.capture_output = capture_output
        self.capture_errors = capture_errors
        if capture_output:
            stdout = self.get_handle(stdout, file_handles)
        if capture_errors:
            stderr = self.get_handle(stderr, file_handles)
        self._tmp = [None, None]
        self._stdout = None
        self._stderr = None
        self._devnull = None
        self._out_stream = stdout
        self._err_stream = stderr

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
        if handles is not None:
            return handles
        if not file_handles:
            return io.StringIO()
        else:
            return None

    @classmethod
    def get_temp_stream(cls):
        """
        **LLM Docstring**

        Open and enter a writable named temporary file to capture output into.

        :return: the temporary file stream
        """
        return tf.NamedTemporaryFile(mode='w+').__enter__()

    def __enter__(self):
        """
        **LLM Docstring**

        Redirect `sys.stdout`/`sys.stderr` to the configured targets (buffers, temp
        files, given streams/paths, or the null device), saving the originals.
        """
        if self.redirect:
            self._stdout = sys.stdout
            self._stderr = sys.stderr
            if (
                    not self.capture_output
                    and self._out_stream is None
            ) or (
                    not self.capture_errors
                    and self._err_stream is None
            ):
                self._devnull = open(os.devnull, 'w+').__enter__()

            if self._out_stream is None:
                if self.capture_output:
                    self._tmp[0] = self.get_temp_stream()
                    sys.stdout = self._tmp[0]
                else:
                    sys.stdout = self._devnull
            else:
                if isinstance(self._out_stream, str):
                    self._tmp[0] = open(self._out_stream, 'a').__enter__()
                    sys.stdout = self._tmp[0]
                else:
                    sys.stdout = self._out_stream

            if self._err_stream is None:
                if self.capture_errors:
                    self._tmp[1] = self.get_temp_stream()
                    sys.stderr = self._tmp[1]
                else:
                    sys.stderr = self._devnull
            else:
                if isinstance(self._err_stream, str):
                    self._tmp[1] = open(self._err_stream, 'a').__enter__()
                    sys.stderr = self._tmp[1]
                else:
                    sys.stderr = self._err_stream
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Restore the original `sys.stdout`/`sys.stderr` and close any streams opened on
        entry.

        :param exc_type: the exception type, if any
        :param exc_val: the exception value, if any
        :param exc_tb: the traceback, if any
        """
        if self.redirect:
            sys.stdout = self._stdout
            sys.stderr = self._stderr
            if self._devnull is not None:
                self._devnull.__exit__(exc_type, exc_val, exc_tb)
                self._devnull = None
            self._stdout = None
            self._stderr = None

            if self._tmp[0] is not None:
                self._tmp[0].__exit__(exc_type, exc_val, exc_tb)
                self._tmp[0] = None
            if self._tmp[1] is not None:
                self._tmp[1].__exit__(exc_type, exc_val, exc_tb)
                self._tmp[1] = None

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
        self.chdir = chdir
        self._outdir = output_dir
        self._curdir = None
        self._tmp = None
        self._opts = tempdir_opts

    def get_temp_dir(self):
        """
        **LLM Docstring**

        Create a `TemporaryDirectory` using the stored options.

        :return: the temporary directory
        """
        return tf.TemporaryDirectory(**self._opts)

    @property
    def dirname(self):
        """
        **LLM Docstring**

        The path of the managed directory (or `None` before entering).

        :return: the directory path
        :rtype: str | None
        """
        if self._tmp is None:
            return None
        if isinstance(self._tmp, str):
            return self._tmp
        else:
            return self._tmp.name

    def __enter__(self):
        """
        **LLM Docstring**

        Establish the directory (creating a temp dir if needed) and optionally `chdir`
        into it, returning its path.

        :return: the directory path
        :rtype: str
        """
        if self._outdir is None:
            self._tmp = self.get_temp_dir()
            self._tmp.__enter__()
        else:
            self._tmp = self._outdir
        if self.chdir:
            self._curdir = os.getcwd()
            os.makedirs(self.dirname, exist_ok=True)
            os.chdir(self.dirname)
        return self.dirname

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Restore the previous working directory and clean up the temporary directory if
        one was created.

        :param exc_type: the exception type, if any
        :param exc_val: the exception value, if any
        :param exc_tb: the traceback, if any
        """
        if self.chdir:
            os.chdir(self._curdir)
        if self._outdir is None:
            self._tmp.__exit__(exc_type, exc_val, exc_tb)
        self._tmp = None
from __future__ import annotations

import enum
from mmap import mmap
import abc, io
import sys
import textwrap

__all__ = [
    "FileStreamReader",
    "FileStreamCheckPoint",
    "FileStreamerTag",
    "FileStreamReaderException",
    "StringStreamReader",
    "FileLineByLineReader",
    "StringLineByLineReader"
]

########################################################################################################################
#
#                                           FileStreamReader
#
class FileStreamCheckPoint:
    """
    A checkpoint for a file that can be returned to when parsing
    """
    def __init__(self, parent, revert = True):
        """
        **LLM Docstring**

        Record the reader's current byte/character offset and configure whether leaving the context restores that position.

        :param parent: the parent reader or regex node
        :type parent: object

        :param revert: whether to restore the captured position on context exit
        :type revert: object
        """
        self.parent = parent
        self.chk = parent.tell()
        self._revert = revert
    def disable(self):
        """
        **LLM Docstring**

        Disable automatic restoration when the checkpoint context exits.

        :return: None.
        :rtype: None
        """
        self._revert = False
    def enable(self):
        """
        **LLM Docstring**

        Enable automatic restoration when the checkpoint context exits.

        :return: None.
        :rtype: None
        """
        self._revert = True
    def revert(self):
        """
        **LLM Docstring**

        Seek the parent reader back to the offset captured when this checkpoint was created.

        :return: None.
        :rtype: None
        """
        self.parent.seek(self.chk)
    def __enter__(self, ):
        """
        **LLM Docstring**

        Return this checkpoint for use in a `with` statement.

        :return: The opened stream, reader, parser, or checkpoint object.
        :rtype: object
        """
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Restore the captured stream position when reversion is enabled; exceptions are not suppressed.

        :param exc_type: the exception class raised in the context, if any
        :type exc_type: object

        :param exc_val: the exception instance raised in the context, if any
        :type exc_val: object

        :param exc_tb: the traceback raised in the context, if any
        :type exc_tb: object
        """
        if self._revert:
            self.revert()

class FileStreamReaderException(IOError):
    pass

class SearchStream(metaclass=abc.ABCMeta):
    """
    Represents a stream from which we can pull block of data.
    Just provides a core interface with which we can work
    """

    @abc.abstractmethod
    def read(self, n=-1):
        """
        **LLM Docstring**

        Define the interface for reading up to `n` units from the current stream position.

        :param n: the requested count or fixed repetition count
        :type n: object

        :return: The text read from the requested region of the stream.
        :rtype: object
        """
        raise NotImplementedError("SearchStream is a base class")
    def rread(self, n=-1):
        """
        **LLM Docstring**

        Read the `n` units immediately preceding the current position, leaving the stream positioned at the beginning of the returned block.

        :param n: the requested count or fixed repetition count
        :type n: object

        :return: The text read from the requested region of the stream.
        :rtype: object
        """
        cur = self.tell()
        if n > 0:
            if n > cur:
                targ = 0
                block = cur
            else:
                targ = cur - n
                block = n
        else:
            targ = 0
            block = cur
        self.seek(targ)
        res = self.read(block)
        self.seek(targ)
        return res
    @abc.abstractmethod
    def readline(self):
        """
        **LLM Docstring**

        Define the interface for reading one line from the stream.

        :return: The text read from the requested region of the stream.
        :rtype: object
        """
        raise NotImplementedError("SearchStream is a base class")
    @abc.abstractmethod
    def seek(self, *args, **kwargs):
        """
        **LLM Docstring**

        Define the interface for repositioning the stream.

        :param args: positional arguments forwarded to the wrapped callable
        :type args: tuple

        :param kwargs: keyword arguments forwarded to the wrapped callable
        :type kwargs: dict

        :return: define the interface for repositioning the stream.
        :rtype: object
        """
        raise NotImplementedError("SearchStream is a base class")
    @abc.abstractmethod
    def tell(self):
        """
        **LLM Docstring**

        Define the interface for reporting the current stream offset.

        :return: The current stream offset.
        :rtype: int
        """
        raise NotImplementedError("SearchStream is a base class")
    @abc.abstractmethod
    def find(self, tag, start=None, end=None):
        """
        **LLM Docstring**

        Define the interface for locating the first occurrence of a tag within optional bounds.

        :param tag: the delimiter or search token
        :type tag: object

        :param start: the inclusive lower search bound or starting stream position
        :type start: object

        :param end: the exclusive upper search bound or ending stream position
        :type end: object

        :return: The matching stream offset, or `-1` when the tag is absent.
        :rtype: int
        """
        raise NotImplementedError("SearchStream is a base class")
    @abc.abstractmethod
    def rfind(self, tag, start=None, end=None):
        """
        **LLM Docstring**

        Define the interface for locating the last occurrence of a tag within optional bounds.

        :param tag: the delimiter or search token
        :type tag: object

        :param start: the inclusive lower search bound or starting stream position
        :type start: object

        :param end: the exclusive upper search bound or ending stream position
        :type end: object

        :return: The matching stream offset, or `-1` when the tag is absent.
        :rtype: int
        """
        raise NotImplementedError("SearchStream is a base class")
    @abc.abstractmethod
    def tag_size(self, tag):
        """
        **LLM Docstring**

        Define the interface for measuring a tag in the stream's native units.

        :param tag: the delimiter or search token
        :type tag: object

        :return: The tag length in the stream's native position units.
        :rtype: int
        """
        raise NotImplementedError("SearchStream is a base class")

    @abc.abstractmethod
    def __iter__(self):
        """
        **LLM Docstring**

        Define iteration over stream records or lines.

        :return: An iterator yielding the records described above.
        :rtype: object
        """
        ...
    def __enter__(self):
        """
        **LLM Docstring**

        Return the stream object without opening additional resources in the abstract implementation.

        :return: The opened stream, reader, parser, or checkpoint object.
        :rtype: object
        """
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Perform no cleanup in the abstract implementation.

        :param exc_type: the exception class raised in the context, if any
        :type exc_type: object

        :param exc_val: the exception instance raised in the context, if any
        :type exc_val: object

        :param exc_tb: the traceback raised in the context, if any
        :type exc_tb: object
        """
        pass

class ByteSearchStream(SearchStream):
    """
    A stream that is implemented for searching in byte strings
    """
    def __init__(self, data, encoding="utf-8", **kw):
        """
        :param data:
        :type data: bytearray
        :param encoding:
        :type encoding:
        :param kw:
        :type kw:
        """
        self._data = data
        self._encoding = encoding
        self._kw = kw
        self._stream = None
        self._wasopen = None
    def __enter__(self):
        """
        **LLM Docstring**

        Open an in-memory `BytesIO` view over the stored byte sequence.

        :return: The opened stream, reader, parser, or checkpoint object.
        :rtype: object
        """
        self._stream = io.BytesIO(self._data)
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Close the in-memory byte stream.

        :param exc_type: the exception class raised in the context, if any
        :type exc_type: object

        :param exc_val: the exception instance raised in the context, if any
        :type exc_val: object

        :param exc_tb: the traceback raised in the context, if any
        :type exc_tb: object
        """
        self._stream.close()
    def __repr__(self):
        """
        **LLM Docstring**

        Return a shortened representation of the stored bytes or active `BytesIO` object.

        :return: The regex source or textual representation constructed by the operation.
        :rtype: str
        """
        cls = type(self)
        stream = textwrap.shorten(repr(
            self._data
                if self._stream is None else
            self._stream
        ), 100)
        return f"{cls.__name__}({stream})"
    def __iter__(self):
        """
        **LLM Docstring**

        Iterate over lines from the active `BytesIO` stream.

        :return: An iterator yielding the records described above.
        :rtype: object
        """
        return iter(self._stream)
    def read(self, n=-1):
        """
        **LLM Docstring**

        Read bytes from the active buffer and decode them with the configured encoding.

        :param n: the requested count or fixed repetition count
        :type n: object

        :return: The text read from the requested region of the stream.
        :rtype: object
        """
        return self._stream.read(n).decode(self._encoding)
    def readline(self):
        """
        **LLM Docstring**

        Read one byte line and decode it with the configured encoding.

        :return: The text read from the requested region of the stream.
        :rtype: object
        """
        return self._stream.readline().decode(self._encoding)
    def seek(self, *args, **kwargs):
        """
        **LLM Docstring**

        Move the active byte-buffer cursor using `BytesIO.seek` semantics.

        :param args: positional arguments forwarded to the wrapped callable
        :type args: tuple

        :param kwargs: keyword arguments forwarded to the wrapped callable
        :type kwargs: dict

        :return: move the active byte-buffer cursor using `BytesIO.seek` semantics.
        :rtype: object
        """
        return self._stream.seek(*args, **kwargs)
    def tell(self):
        """
        **LLM Docstring**

        Return the active byte-buffer cursor offset.

        :return: The current stream offset.
        :rtype: int
        """
        return self._stream.tell()
    def encode_tag(self, tag):
        """
        **LLM Docstring**

        Convert a text tag to bytes using the configured encoding, leaving byte tags unchanged.

        :param tag: the delimiter or search token
        :type tag: object

        :return: convert a text tag to bytes using the configured encoding, leaving byte tags unchanged.
        :rtype: object
        """
        if not isinstance(tag, bytes):
            tag = tag.encode(self._encoding)
        return tag
    def find(self, tag, start=None, end=None):
        """
        **LLM Docstring**

        Search the stored bytes forward for a tag, defaulting to the current cursor as the lower bound.

        :param tag: the delimiter or search token
        :type tag: object

        :param start: the inclusive lower search bound or starting stream position
        :type start: object

        :param end: the exclusive upper search bound or ending stream position
        :type end: object

        :return: The matching stream offset, or `-1` when the tag is absent.
        :rtype: int
        """
        enc_tag = self.encode_tag(tag)
        if start is None:
            start = self.tell()
        if end is None:
            end = -1
        arg_vec = [enc_tag, start, end]
        return self._data.find(*arg_vec)
    def rfind(self, tag, start=None, end=None):
        """
        **LLM Docstring**

        Search the stored bytes backward for a tag, defaulting to the current cursor as the upper bound.

        :param tag: the delimiter or search token
        :type tag: object

        :param start: the inclusive lower search bound or starting stream position
        :type start: object

        :param end: the exclusive upper search bound or ending stream position
        :type end: object

        :return: The matching stream offset, or `-1` when the tag is absent.
        :rtype: int
        """
        enc_tag = self.encode_tag(tag)
        if start is None:
            start = 0
        if end is None:
            end = self.tell()
        arg_vec = [enc_tag, start, end]
        return self._data.rfind(*arg_vec)
    def tag_size(self, tag):
        """
        **LLM Docstring**

        Return the encoded byte length of a search tag.

        :param tag: the delimiter or search token
        :type tag: object

        :return: The tag length in the stream's native position units.
        :rtype: int
        """
        enc_tag = self.encode_tag(tag)
        return len(enc_tag)

class FileSearchStream(SearchStream):
    """
    A stream that is implemented for searching in mmap-ed files
    """
    default_binary = True
    def __init__(self, file, mode="r", binary=None, encoding="utf-8",
                 check_decoding=False,
                 decoding_mode="strict",
                 **kw):
        """
        **LLM Docstring**

        Configure a file-backed searchable stream, normalizing the mode to read/write binary or text-compatible form for memory mapping.

        :param file: a filesystem path or open file object
        :type file: object

        :param mode: the file open mode or parser multiplicity mode
        :type mode: object

        :param binary: whether stream values should remain bytes
        :type binary: object

        :param encoding: the text encoding used to convert between bytes and strings
        :type encoding: object

        :param check_decoding: whether decoding errors should be converted to contextual `ValueError`s
        :type check_decoding: object

        :param decoding_mode: the error policy passed to `bytes.decode`
        :type decoding_mode: object

        :param kw: extra keyword arguments forwarded to the underlying stream constructor
        :type kw: object
        """
        self._file = file
        if binary is None:
            binary = self.default_binary
        if binary:
            mode = mode.strip("+b") + "+b"
        else:
            mode = mode.strip('+') + '+'
        self._mode = mode
        self._encoding = encoding
        self.check_decoding = check_decoding,
        self.decoding_mode = decoding_mode
        self._kw = kw
        self._stream = None
        self._wasopen = None
    def __repr__(self):
        """
        **LLM Docstring**

        Show the file object/path and normalized open mode.

        :return: The regex source or textual representation constructed by the operation.
        :rtype: str
        """
        cls = type(self)
        return f"{cls.__name__}({self._file}, {self._mode!r})"
    def __enter__(self):
        """
        **LLM Docstring**

        Open the file when given a path and memory-map its complete contents.

        :return: The opened stream, reader, parser, or checkpoint object.
        :rtype: object
        """
        if isinstance(self._file, str):
            self._wasopen = False
            self._fstream = open(self._file, mode=self._mode, **self._kw)
        else:
            self._wasopen = True
            self._fstream = self._file
        handle = self._fstream.fileno()
        self._stream = mmap(handle, 0)
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Close the memory map and close the underlying file only when this object opened it.

        :param exc_type: the exception class raised in the context, if any
        :type exc_type: object

        :param exc_val: the exception instance raised in the context, if any
        :type exc_val: object

        :param exc_tb: the traceback raised in the context, if any
        :type exc_tb: object
        """
        self._stream.close()
        if not self._wasopen:
            self._fstream.close()
    def __iter__(self):
        """
        **LLM Docstring**

        Yield successive raw lines from the memory map until its cursor stops advancing.

        :return: An iterator yielding the records described above.
        :rtype: object
        """
        new_pos = self._stream.tell()
        not_exhausted = True
        while not_exhausted:
            line = self._stream.readline()
            old_pos = new_pos
            new_pos = self._stream.tell()
            not_exhausted = new_pos > old_pos
            if not_exhausted:
                yield line
    def handle_chunk(self, chunk):
        """
        **LLM Docstring**

        Decode byte chunks with the configured encoding and error mode, optionally converting decode failures to `ValueError`.

        :param chunk: a raw chunk read from the memory map
        :type chunk: object

        :return: decode byte chunks with the configured encoding and error mode, optionally converting decode failures to `ValueError`.
        :rtype: object
        """
        if isinstance(chunk, bytes):
            if self.check_decoding:
                try:
                    chunk = chunk.decode(self._encoding, self.decoding_mode)
                except UnicodeDecodeError:
                    raise ValueError(f"error decoding: {chunk}")
            else:
                chunk = chunk.decode(self._encoding, self.decoding_mode)
        return chunk
    def read(self, n=-1):
        """
        **LLM Docstring**

        Read from the memory map and decode the returned chunk.

        :param n: the requested count or fixed repetition count
        :type n: object

        :return: The text read from the requested region of the stream.
        :rtype: object
        """
        return self.handle_chunk(self._stream.read(n))
    def readline(self):
        """
        **LLM Docstring**

        Read one line from the memory map and decode it.

        :return: The text read from the requested region of the stream.
        :rtype: object
        """
        return self.handle_chunk(self._stream.readline())
    def seek(self, *args, **kwargs):
        """
        **LLM Docstring**

        Move the memory-map cursor.

        :param args: positional arguments forwarded to the wrapped callable
        :type args: tuple

        :param kwargs: keyword arguments forwarded to the wrapped callable
        :type kwargs: dict

        :return: move the memory-map cursor.
        :rtype: object
        """
        return self._stream.seek(*args, **kwargs)
    def tell(self):
        """
        **LLM Docstring**

        Return the memory-map cursor offset.

        :return: The current stream offset.
        :rtype: int
        """
        return self._stream.tell()
    def find(self, tag, start=None, end=None):
        """
        **LLM Docstring**

        Find the next encoded tag in the memory map, starting at the current cursor unless bounds are supplied.

        :param tag: the delimiter or search token
        :type tag: object

        :param start: the inclusive lower search bound or starting stream position
        :type start: object

        :param end: the exclusive upper search bound or ending stream position
        :type end: object

        :return: The matching stream offset, or `-1` when the tag is absent.
        :rtype: int
        """
        enc_tag = tag.encode(self._encoding)
        if start is None:
            start = self.tell()
        if end is None:
            end = -1
        arg_vec = [enc_tag, start, end]
        return self._stream.find(*arg_vec)
    def rfind(self, tag, start=None, end=None):
        """
        **LLM Docstring**

        Find the previous encoded tag in the memory map, ending at the current cursor unless bounds are supplied.

        :param tag: the delimiter or search token
        :type tag: object

        :param start: the inclusive lower search bound or starting stream position
        :type start: object

        :param end: the exclusive upper search bound or ending stream position
        :type end: object

        :return: The matching stream offset, or `-1` when the tag is absent.
        :rtype: int
        """
        enc_tag = tag.encode(self._encoding)
        if start is None:
            start = 0
        if end is None:
            end = self.tell()
        arg_vec = [enc_tag, start, end]

        return self._stream.rfind(*arg_vec)
    def tag_size(self, tag):
        """
        **LLM Docstring**

        Return the byte length of a tag encoded with this stream's encoding.

        :param tag: the delimiter or search token
        :type tag: object

        :return: The tag length in the stream's native position units.
        :rtype: int
        """
        enc_tag = tag.encode(self._encoding)
        return len(enc_tag)

class StringSearchStream(SearchStream):
    """
    A stream that is implemented for searching in strings.
    Current implementation creates a `StringIO` buffer to support `read`/`tell`/etc.
    This is very memory inefficient, but we're not winning performance awards for
    any of this anyway
    """
    def __init__(self, string):
        """
        :param string:
        :type string: str
        """
        self._data = string
        self._stream = None

    def __enter__(self):
        """
        **LLM Docstring**

        Open a `StringIO` cursor over the stored string.

        :return: The opened stream, reader, parser, or checkpoint object.
        :rtype: object
        """
        self._stream = io.StringIO(self._data)
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Close the active `StringIO` object.

        :param exc_type: the exception class raised in the context, if any
        :type exc_type: object

        :param exc_val: the exception instance raised in the context, if any
        :type exc_val: object

        :param exc_tb: the traceback raised in the context, if any
        :type exc_tb: object
        """
        self._stream.close()
    def __iter__(self):
        """
        **LLM Docstring**

        Iterate over lines from the active `StringIO` object.

        :return: An iterator yielding the records described above.
        :rtype: object
        """
        return iter(self._stream)

    def read(self, n=-1):
        """
        **LLM Docstring**

        Read characters from the active string cursor.

        :param n: the requested count or fixed repetition count
        :type n: object

        :return: The text read from the requested region of the stream.
        :rtype: object
        """
        return self._stream.read(n)
    def readline(self):
        """
        **LLM Docstring**

        Read one line from the active string cursor.

        :return: The text read from the requested region of the stream.
        :rtype: object
        """
        return self._stream.readline()
    def seek(self, *args, **kwargs):
        """
        **LLM Docstring**

        Move the string cursor.

        :param args: positional arguments forwarded to the wrapped callable
        :type args: tuple

        :param kwargs: keyword arguments forwarded to the wrapped callable
        :type kwargs: dict

        :return: move the string cursor.
        :rtype: object
        """
        return self._stream.seek(*args, **kwargs)
    def tell(self):
        """
        **LLM Docstring**

        Return the current character offset.

        :return: The current stream offset.
        :rtype: int
        """
        return self._stream.tell()
    def find(self, tag, start=None, end=None):
        """
        **LLM Docstring**

        Find the next tag in the original string, beginning at the current cursor by default.

        :param tag: the delimiter or search token
        :type tag: object

        :param start: the inclusive lower search bound or starting stream position
        :type start: object

        :param end: the exclusive upper search bound or ending stream position
        :type end: object

        :return: The matching stream offset, or `-1` when the tag is absent.
        :rtype: int
        """
        if start is None:
            start = self.tell()
        if end is None:
            end = len(self._data) + 1
        arg_vec = [tag, start, end]

        return self._data.find(*arg_vec)
    def rfind(self, tag, start=None, end=None):
        """
        **LLM Docstring**

        Find the previous tag in the original string, ending at the current cursor by default.

        :param tag: the delimiter or search token
        :type tag: object

        :param start: the inclusive lower search bound or starting stream position
        :type start: object

        :param end: the exclusive upper search bound or ending stream position
        :type end: object

        :return: The matching stream offset, or `-1` when the tag is absent.
        :rtype: int
        """
        if start is None:
            start = 0
        if end is None:
            end = self.tell()
        arg_vec = [tag, start, end]
        return self._data.rfind(*arg_vec)
    def tag_size(self, tag):
        """
        **LLM Docstring**

        Return the number of characters in a tag.

        :param tag: the delimiter or search token
        :type tag: object

        :return: The tag length in the stream's native position units.
        :rtype: int
        """
        return len(tag)

class SearchStreamReader:
    """
    Represents a reader which implements finding chunks of data in a stream
    """

    def __init__(self, stream):
        """
        :param stream:
        :type stream: SearchStream
        """
        self.stream = stream
        self._exhausted_tag_pos = {} # an optimization for tag alternative searching
        self._next_tag_pos = [{}, {}] # an optimization for tag alternative searching
    def __enter__(self):
        """
        **LLM Docstring**

        Open the wrapped search stream and return this reader.

        :return: The opened stream, reader, parser, or checkpoint object.
        :rtype: object
        """
        self.stream.__enter__()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Forward context-manager cleanup to the wrapped stream.

        :param exc_type: the exception class raised in the context, if any
        :type exc_type: object

        :param exc_val: the exception instance raised in the context, if any
        :type exc_val: object

        :param exc_tb: the traceback raised in the context, if any
        :type exc_tb: object
        """
        self.stream.__exit__(exc_type, exc_val, exc_tb)
    def __repr__(self):
        """
        **LLM Docstring**

        Represent the reader together with its wrapped search stream.

        :return: The regex source or textual representation constructed by the operation.
        :rtype: str
        """
        cls = type(self)
        return f"{cls.__name__}({self.stream})"

    class StreamSearchDirection(enum.Enum):
        Forward = "forward"
        Reverse = "reverse"
        ForwardReverse = "forward-reverse"
        ReverseForward = "reverse-forward"

    @classmethod
    def _is_forward(self, direction):
        """
        **LLM Docstring**

        Return whether a direction value is exactly the forward-search enum member.

        :param direction: the direction in which delimiters are searched
        :type direction: object

        :return: `True` when the condition described above holds; otherwise `False`.
        :rtype: bool
        """
        #TODO: optimize this away
        return self.StreamSearchDirection(direction) is self.StreamSearchDirection.Forward
    @classmethod
    def _is_reverse(self, direction):
        """
        **LLM Docstring**

        Return whether a direction value is exactly the reverse-search enum member.

        :param direction: the direction in which delimiters are searched
        :type direction: object

        :return: `True` when the condition described above holds; otherwise `False`.
        :rtype: bool
        """
        #TODO: optimize this away
        return self.StreamSearchDirection(direction) is self.StreamSearchDirection.Reverse

    def _find_tag(self, tag,
                  skip_tag=True,
                  seek=True,
                  direction='forward'
                  ):
        """
        Finds a tag in a file

        :param header: a tag specifying a header to look for + optional follow-up processing/offsets
        :type header: FileStreamerTag
        :return: position of tag
        :rtype: int
        """
        direction = self.StreamSearchDirection(direction)
        forward = self._is_forward(direction)
        with FileStreamCheckPoint(self, revert=False) as chk:
            if forward:
                pos = self.stream.find(tag)
            else:
                pos = self.stream.rfind(tag)

            if pos >= 0:
                if skip_tag:
                    tag_size = self.stream.tag_size(tag)
                else:
                    tag_size = 0
                pos += tag_size
                if seek:
                    self.stream.seek(pos)
            elif pos < 0:
                chk.revert()
        return pos

    def find_tag(self,
                 tag,
                 skip_tag=None,
                 seek=None,
                 allow_terminal=False,
                 validator=None,
                 return_body=False,
                 direction='forward'
                 ):
        """
        Finds a tag in a file

        :param header: a tag specifying a header to look for + optional follow-up processing/offsets
        :type header: FileStreamerTag
        :return: position of tag
        :rtype: int
        """
        if isinstance(tag, str):
            tags = FileStreamerTag(tag)
        elif isinstance(tag, dict):
            tag = tag.copy()
            t = tag['tag']
            del tag['tag']
            tags = FileStreamerTag(t, **tag)
        else:
            tags = tag

        pos = -1
        if skip_tag is None:
            skip_tag = tags.skip_tag
        if seek is None:
            seek = tags.seek
        res = None

        tag_positions = {}
        cur = self.tell()
        tag = None
        direction = self.StreamSearchDirection(direction)
        forward = self._is_forward(direction)
        reverse = not forward
        for t in tags.tags:
            # if (
            #         t not in self._exhausted_tag_pos
            #         or cur < self._exhausted_tag_pos[t]
            # ):
            #     self.seek(cur)
            #     pos = self._find_tag(t, skip_tag=skip_tag, seek=seek)
            #     if pos < 0:
            #         self._exhausted_tag_pos[t] = cur
            #     else:
            #         tag_positions[pos] = t

            if forward:
                (cur_test, p_test) = self._next_tag_pos[0].get(t, (cur + 1, -1))
                if (
                        (p_test < 0 or p_test >= cur_test)
                        and cur_test <= cur and p_test > cur
                ):
                    if p_test > 0:
                        tag_positions[p_test] = t
                    continue
            else:
                (cur_test, p_test) = self._next_tag_pos[1].get(t, (cur-1, -1))
                if (
                        (p_test < 0 or p_test <= cur_test)
                        and cur_test >= cur and p_test < cur
                ):
                    if p_test >= 0:
                        tag_positions[p_test] = t
                    continue

            self.seek(cur)
            pos = self._find_tag(t, skip_tag=skip_tag, seek=seek, direction=direction)
            if forward:
                self._next_tag_pos[0][t] = (cur, pos)
            else:
                self._next_tag_pos[1][t] = (cur, pos)
            if pos > 0:
                tag_positions[pos] = t

        tag_keys = sorted(tag_positions.keys())
        if reverse:
            tag_keys = reversed(tag_keys)
        for pos in tag_keys:
            og_pos = pos
            tag = tag_positions[pos]
            if skip_tag and (return_body or validator is not None):
                ts = self.stream.tag_size(tag)
            else:
                ts = 0

            follow_ups = tags.skips
            if follow_ups is not None:
                prev_tag = tag
                for tag in follow_ups:
                    prev_size = self.stream.tag_size(prev_tag)
                    if forward:
                        self.stream.seek(pos+prev_size)
                    else:
                        self.stream.seek(pos-prev_size)
                    p = self._find_tag(tag, seek=False, direction=direction)
                    if p > -1:
                        pos = p
                    elif allow_terminal:
                        pos = p
                        break
                    prev_tag = tag

                # if not seek:
                #     self.seek(pre_follows)
                if validator is not None:
                    block_size = abs(pos - og_pos + ts)
                    if forward:
                        self.stream.seek(og_pos - ts)
                        res = self.stream.read(block_size)
                    else:
                        self.stream.seek(pos + ts)
                        res = self.stream.rread(block_size)
                    test = validator(res)
                    if test == self.TagSentinels.NextMatch:
                        return self.find_tag(tags,
                                             skip_tag=skip_tag,
                                             seek=seek,
                                             allow_terminal=allow_terminal,
                                             validator=validator,
                                             return_body=return_body
                                             )
                    while test == self.TagSentinels.Continue or not test:
                        if forward:
                            self.stream.seek(pos + 1)
                        else:
                            self.stream.seek(pos - 1)
                        p = self.find_tag(tag, direction=direction)
                        pos = p
                        if p == -1:
                            break
                        else:
                            block_size = abs(pos - og_pos + ts)
                            if forward:
                                self.stream.seek(og_pos - ts)
                                res = self.stream.read(block_size)
                            else:
                                self.stream.seek(pos + ts)
                                res = self.stream.rread(block_size)
                            test = validator(res)
                            if test == self.TagSentinels.NextMatch:
                                return self.find_tag(tags,
                                                     skip_tag=skip_tag,
                                                     seek=seek,
                                                     allow_terminal=allow_terminal,
                                                     validator=validator,
                                                     return_body=return_body,
                                                     direction=direction
                                                     )
                    if pos < 0:
                        res = None
                        continue
                else:
                    block_size = abs(pos - og_pos + ts)
                    if forward:
                        self.stream.seek(og_pos - ts)
                        res = self.stream.read(block_size)
                    else:
                        self.stream.seek(pos + ts)
                        res = self.stream.rread(block_size)

            else:
                block_size = abs(pos - og_pos + ts)
                if forward:
                    self.stream.seek(og_pos - ts)
                    res = self.stream.read(block_size)
                else:
                    self.stream.seek(pos + ts)
                    res = self.stream.rread(block_size)

            offset = tags.offset
            if offset is not None:
                # why are we using self._stream.tell here...?
                # I won't touch it for now but I feel like it should be pos
                if forward:
                    pos = self.stream.tell() + offset
                else:
                    pos = self.stream.tell() - offset

            if return_body and res is None:
                if forward:
                    self.stream.seek(og_pos - ts)
                    res = self.stream.read(pos - og_pos + ts)
                else:
                    self.stream.seek(pos)
                    res = self.stream.rread(abs(pos - og_pos - ts))
            if not skip_tag:
                if forward:
                    self.stream.seek(og_pos)
                else:
                    self.stream.seek(pos + ts)
                pos = og_pos
            break # first match in alternatives

        if seek is False:
            self.seek(cur)

        if return_body:
            return res, pos
        else:
            return pos

    class TagSentinels(enum.Enum):
        EOF = 'end_of_file'
        Continue = "continue"
        NextMatch = "next_match"
    def _parse_end_block(self,
                         start, tag_end, allow_terminal,
                         expand_until_valid, validator,
                         direction="forward"
                         ):
        """
        **LLM Docstring**

        Starting from a known boundary, locate an end tag, read the intervening block in the requested direction, and optionally extend across later end tags until validation succeeds.

        :param start: the inclusive lower search bound or starting stream position
        :type start: object

        :param tag_end: the delimiter that terminates the block
        :type tag_end: object

        :param allow_terminal: whether end-of-stream may terminate an otherwise unterminated block
        :type allow_terminal: object

        :param expand_until_valid: whether to continue through later end delimiters until validation succeeds
        :type expand_until_valid: object

        :param validator: a callable that decides whether an extracted block is complete and valid
        :type validator: object

        :param direction: the direction in which delimiters are searched
        :type direction: object

        :return: The extracted block, optionally paired with delimiter text or source endpoints according to the flags.
        :rtype: object
        """
        with FileStreamCheckPoint(self):
            end = self.find_tag(tag_end, allow_terminal=allow_terminal, seek=False, direction=direction)
        reverse = self._is_reverse(direction)
        forward = not reverse
        if reverse:
            start, end = end, start
        if (start < 0 or end < 0):
            if allow_terminal:
                block = self.stream.read()
                if validator is not None and not validator(block):
                    block = None
            else:
                block = self.TagSentinels.EOF
        else:
            if forward:
                block = self.stream.read(end - start)
            else:
                block = self.stream.rread(end - start)


            if expand_until_valid:
                with FileStreamCheckPoint(self) as chk:
                    if not validator(block):
                        if forward:
                            block = block + self.stream.read(1)
                        else:
                            block = self.stream.rread(1) + block
                    while not validator(block):
                        if forward:
                            self.stream.seek(end + 1)
                            extra = self.find_tag(tag_end, allow_terminal=allow_terminal, seek=False, direction=direction)
                            if extra > 0:
                                block = block + self.stream.read(extra - end)
                                end = extra
                            else:
                                if allow_terminal:
                                    self.stream.seek(start)
                                    block = self.stream.read()
                                    if not validator(block):
                                        block = None
                                    end = -1
                                else:
                                    block = None
                                break
                        else:
                            self.stream.seek(max(start - 1, 0))
                            extra = self.find_tag(tag_end, allow_terminal=allow_terminal, seek=False, direction=direction)
                            if extra > 0:
                                block = self.stream.rread(start - extra) + block
                                start = extra
                            else:
                                if allow_terminal:
                                    self.stream.seek(end)
                                    block = self.stream.rread()
                                    if not validator(block):
                                        block = None
                                    start = -1
                                else:
                                    block = None
                                break
                    if block is not None:
                        chk.disable()
        return (start, end), block

    @classmethod
    def _get_search_directions(cls, direction):
        """
        **LLM Docstring**

        Translate a combined search mode into separate directions for locating the start and end delimiters.

        :param direction: the direction in which delimiters are searched
        :type direction: object

        :return: A `(start_direction, end_direction)` pair.
        :rtype: object
        """
        direction = cls.StreamSearchDirection(direction)
        if direction is cls.StreamSearchDirection.Forward:
            start_direction = end_direction = cls.StreamSearchDirection.Forward
        elif direction is cls.StreamSearchDirection.Reverse:
            start_direction = end_direction = cls.StreamSearchDirection.Reverse
        elif direction is cls.StreamSearchDirection.ForwardReverse:
            start_direction, end_direction = cls.StreamSearchDirection.Forward, cls.StreamSearchDirection.Reverse
        else:
            start_direction, end_direction = cls.StreamSearchDirection.Reverse, cls.StreamSearchDirection.Forward
        return start_direction, end_direction
    def get_tagged_block(self, tag_start, tag_end,
                         validator=None, tag_validator=None,
                         allow_terminal=False,
                         expand_until_valid=None,
                         return_tag=False,
                         return_end_points=False,
                         direction='forward',
                         block_size=500):
        """
        Pulls the string between tag_start and tag_end

        :param tag_start:
        :type tag_start: FileStreamerTag or None
        :param tag_end:
        :type tag_end: FileStreamerTag
        :return:
        :rtype:
        """

        block = None
        tag_body = None
        end_points = None

        start_direction, end_direction = self._get_search_directions(direction)
        _eps = end_points
        if expand_until_valid is None:
            expand_until_valid = validator is not None
        while block is None:
            if tag_start is not None:
                tag_str, start = self.find_tag(tag_start,
                                               allow_terminal=False,
                                               return_body=True,
                                               validator=tag_validator,
                                               direction=start_direction)

                if start >= 0:
                    end_points, block = self._parse_end_block(start, tag_end, allow_terminal, expand_until_valid,
                                                              validator, end_direction)
                    if end_points is not None and _eps is not None and end_points == _eps:
                        raise ValueError(f"stuck in a loop while searching for {tag_end} starting from {start} in dir {end_direction}")
                    _eps = end_points
                    if block is not None:
                        tag_body = tag_str
                else:
                    block = self.TagSentinels.EOF
                    end_points = (start,-1)
            else:
                start = self.tell()
                end_points, block = self._parse_end_block(start, tag_end, allow_terminal, expand_until_valid,
                                                          validator, end_direction)

            if (
                    not expand_until_valid # quick check, we already validated up above
                    and block is not None
                    and block is not self.TagSentinels.EOF
                    and (validator is not None and not validator(block))
            ):
                # invalid block found, skip ahead
                # protected by EOF check
                if self._is_forward(start_direction):
                    self.seek(end_points[-1]+1)
                else:
                    self.seek(end_points[0]-1)
                end_points = None

        if block is self.TagSentinels.EOF:
            block = None

        if return_tag or return_end_points:
            aux = ()
            if return_tag:
                aux = aux + (tag_body,)
            if return_end_points:
                aux = aux + (end_points,)
            return aux, block
        else:
            return block

    def _parse_block(self, tag_start, tag_end, validator, tag_validator,
                     allow_terminal, expand_until_valid, preserve_tag, return_end_points, direction):
        """
        **LLM Docstring**

        Extract one tagged block, optionally restore the start tag text, and normalize optional endpoint metadata.

        :param tag_start: the delimiter that begins the block, or `None` to begin at the current cursor
        :type tag_start: object

        :param tag_end: the delimiter that terminates the block
        :type tag_end: object

        :param validator: a callable that decides whether an extracted block is complete and valid
        :type validator: object

        :param tag_validator: a callable that accepts or redirects candidate start tags
        :type tag_validator: object

        :param allow_terminal: whether end-of-stream may terminate an otherwise unterminated block
        :type allow_terminal: object

        :param expand_until_valid: whether to continue through later end delimiters until validation succeeds
        :type expand_until_valid: object

        :param preserve_tag: whether to prepend a skipped start tag back onto the returned block
        :type preserve_tag: object

        :param return_end_points: whether to return source offsets with the parsed block
        :type return_end_points: object

        :param direction: the direction in which delimiters are searched
        :type direction: object

        :return: The extracted block, optionally paired with delimiter text or source endpoints according to the flags.
        :rtype: object
        """
        ret_tag = preserve_tag
        if ret_tag and isinstance(tag_start, FileStreamerTag):
            ret_tag = tag_start.skip_tag
        block = self.get_tagged_block(tag_start, tag_end,
                                      validator=validator,
                                      tag_validator=tag_validator,
                                      return_tag=ret_tag,
                                      return_end_points=return_end_points,
                                      allow_terminal=allow_terminal,
                                      expand_until_valid=expand_until_valid,
                                      direction=direction
                                      )

        end_points = None
        if ret_tag:
            start_direction, end_direction = self._get_search_directions(direction)
            if return_end_points:
                (tag_body, end_points), block = block
            else:
                (tag_body,), block = block
            if self._is_forward(end_direction) and block is not None and tag_body is not None:
                block = tag_body + block
                if end_points is not None:
                    start, end = end_points
                    if self._is_forward(start_direction):
                        start = start - len(tag_body)
                    end_points = (start, end)
        elif return_end_points:
            (end_points,), block = block

        if end_points is not None:
            return end_points, block
        else:
            return block
    def parse_key_block(self,
                        tag_start=None,
                        tag_end=None,
                        mode="Single",
                        validator=None,
                        tag_validator=None,
                        expand_until_valid=False,
                        preserve_tag=False,
                        return_end_points=False,
                        parser=None,
                        parse_mode="List",
                        num=None,
                        pass_context=False,
                        allow_terminal=False,
                        direction="forward",
                        **ignore
                        ):
        """Parses a block by starting at tag_start and looking for tag_end and parsing what's in between them

        :param key: registered key pattern to pull from a file
        :type key: str
        :return:
        :rtype:
        """
        # if tag_start is None:
        #     raise FileStreamReaderException("{}.{}: needs a '{}' argument".format(
        #         type(self).__name__,
        #         "parse_key_block",
        #         "tag_start"
        #     ))
        if tag_end is None:
            raise FileStreamReaderException("{}.{}: needs a '{}' argument".format(
                type(self).__name__,
                "parse_key_block",
                "tag_end"
            ))
        if mode == "List":
            with FileStreamCheckPoint(self):
                # we do this in a checkpointed fashion only for list-type tokens
                # for all other tokens we introduce an ordering to apply when checking
                # does it need to be done like this... probably not?
                # I suppose we could be a significantly more efficient by returning a
                # generator statement in these multi-block cases
                # and then introducing a sorting order across these multi-blocks
                # that tells us which to check first, second, etc.
                # but this is probably good enough
                if isinstance(num, int):
                    blocks = [None]*num
                    if parser is None:
                        parser = lambda a, reader=None:a

                    i = 0 # protective
                    for i in range(num):
                        block = self._parse_block(tag_start, tag_end, validator, tag_validator,
                                                  allow_terminal, expand_until_valid, preserve_tag, return_end_points,
                                                  direction)
                        if block is None:
                            break
                        if parse_mode != "List":
                            if pass_context:
                                block = parser(block, reader=self)
                            else:
                                block = parser(block)
                        blocks[i] = block

                    if parse_mode == "List":
                        blocks = parser(blocks[:i+1])
                else:
                    blocks = []
                    block = self._parse_block(tag_start, tag_end, validator, tag_validator,
                                              allow_terminal, expand_until_valid, preserve_tag, return_end_points,
                                              direction)
                    if parser is None:
                        parser = lambda a, reader=None:a
                    while block is not None:
                        if parse_mode != "List":
                            if pass_context:
                                block = parser(block, reader=self)
                            else:
                                block = parser(block)

                        blocks.append(block)
                        block = self._parse_block(tag_start, tag_end, validator, tag_validator,
                                                  allow_terminal, expand_until_valid, preserve_tag, return_end_points,
                                                  direction)

                    if parse_mode == "List":
                        if pass_context:
                            blocks = parser(blocks, reader=self)
                        else:
                            blocks = parser(blocks)
                return blocks
        else:
            block = self._parse_block(tag_start, tag_end, validator, tag_validator,
                                      allow_terminal, expand_until_valid, preserve_tag, return_end_points,
                                      direction)
            if parser is not None:
                block = parser(block)
            return block

    def read(self, n=1):
        """
        **LLM Docstring**

        Read from the wrapped stream.

        :param n: the requested count or fixed repetition count
        :type n: object

        :return: The text read from the requested region of the stream.
        :rtype: object
        """
        return self.stream.read(n)
    def readline(self):
        """
        **LLM Docstring**

        Read one line from the wrapped stream.

        :return: The text read from the requested region of the stream.
        :rtype: object
        """
        return self.stream.readline()
    def seek(self, *args, **kwargs):
        """
        **LLM Docstring**

        Reposition the wrapped stream.

        :param args: positional arguments forwarded to the wrapped callable
        :type args: tuple

        :param kwargs: keyword arguments forwarded to the wrapped callable
        :type kwargs: dict

        :return: reposition the wrapped stream.
        :rtype: object
        """
        return self.stream.seek(*args, **kwargs)
    def tell(self):
        """
        **LLM Docstring**

        Return the wrapped stream's current offset.

        :return: The current stream offset.
        :rtype: int
        """
        return self.stream.tell()
    def find(self, tag):
        """
        **LLM Docstring**

        Find a tag in the wrapped stream using its native search operation.

        :param tag: the delimiter or search token
        :type tag: object

        :return: The matching stream offset, or `-1` when the tag is absent.
        :rtype: int
        """
        return self.stream.find(tag)
    def rfind(self, tag, search_window=None):
        """
        **LLM Docstring**

        Find a preceding tag, using the stream's reverse search when available or a bounded read-and-search fallback.

        :param tag: the delimiter or search token
        :type tag: object

        :param search_window: the maximum number of preceding characters to inspect in the fallback reverse search
        :type search_window: object

        :return: The matching stream offset, or `-1` when the tag is absent.
        :rtype: int
        """
        if hasattr(self.stream, 'rfind'):
            return self.stream.rfind(tag)
        else:
            cur = self.stream.tell()
            if search_window is None:
                start = 0
            else:
                start = cur - search_window
            self.seek(start)
            body = self.read(cur)
            pos = body.rfind(tag)
            if pos > 0:
                pos = start + pos
            return pos
    def skip_tag(self, tag):
        """
        **LLM Docstring**

        Call the wrapped stream's `skip_tag` operation; the supplied stream implementations do not define this method.

        :param tag: the delimiter or search token
        :type tag: object

        :return: call the wrapped stream's `skip_tag` operation; the supplied stream implementations do not define this method.
        :rtype: object
        """
        return self.stream.skip_tag(tag)
    def rskip_tag(self, tag):
        """
        **LLM Docstring**

        Call the wrapped stream's `rskip_tag` operation; the supplied stream implementations do not define this method.

        :param tag: the delimiter or search token
        :type tag: object

        :return: call the wrapped stream's `rskip_tag` operation; the supplied stream implementations do not define this method.
        :rtype: object
        """
        return self.stream.rskip_tag(tag)

class FileStreamReader(SearchStreamReader):
    """
    Represents a file from which we'll stream blocks of data by finding tags and parsing what's between them
    """
    def __init__(self, file, mode="r", encoding="utf-8", **kw):
        """
        **LLM Docstring**

        Wrap a path or file object in `FileSearchStream` and initialize tagged-block parsing over it.

        :param file: a filesystem path or open file object
        :type file: object

        :param mode: the file open mode or parser multiplicity mode
        :type mode: object

        :param encoding: the text encoding used to convert between bytes and strings
        :type encoding: object

        :param kw: extra keyword arguments forwarded to the underlying stream constructor
        :type kw: object
        """
        stream = FileSearchStream(file, mode=mode, encoding=encoding, **kw)
        super().__init__(stream)
class StringStreamReader(SearchStreamReader):
    """
    Represents a string from which we'll stream blocks of data by finding tags and parsing what's between them
    """
    def __init__(self, string):
        """
        **LLM Docstring**

        Wrap a string in `StringSearchStream` and initialize tagged-block parsing over it.

        :param string: the source string or byte sequence wrapped by the reader
        :type string: object
        """
        stream = StringSearchStream(string)
        super().__init__(stream)
class ByteStreamReader(SearchStreamReader):
    """
    Represents a string from which we'll stream blocks of data by finding tags and parsing what's between them
    """
    def __init__(self, string, encoding="utf-8", **kw):
        """
        **LLM Docstring**

        Wrap bytes in `ByteSearchStream` and initialize tagged-block parsing over it.

        :param string: the source string or byte sequence wrapped by the reader
        :type string: object

        :param encoding: the text encoding used to convert between bytes and strings
        :type encoding: object

        :param kw: extra keyword arguments forwarded to the underlying stream constructor
        :type kw: object
        """
        stream = ByteSearchStream(string, encoding=encoding, **kw)
        super().__init__(stream)

class FileStreamerTag:
    def __init__(self,
                 tag_alternatives=None,
                 follow_ups=None,
                 offset=None,
                 direction="forward",
                 skip_tag=True,
                 seek=True
                 ):
        """
        **LLM Docstring**

        Normalize one or more alternative delimiters plus optional follow-up delimiters, offset, direction, skip, and seek behavior into a tag specification.

        :param tag_alternatives: one delimiter or a collection of alternative delimiters
        :type tag_alternatives: object

        :param follow_ups: additional delimiters that must be located in sequence after the first tag
        :type follow_ups: object

        :param offset: an additional cursor displacement applied after a match
        :type offset: object

        :param direction: the direction in which delimiters are searched
        :type direction: object

        :param skip_tag: whether the returned position should lie after the matched delimiter
        :type skip_tag: object

        :param seek: whether finding a delimiter should move the stream cursor
        :type seek: object
        """
        if tag_alternatives is None:
            raise FileStreamReaderException("{} needs to be supplied with some set of tag_alternatives to look for".format(
                type(self).__name__
            ))
        self.tags = (tag_alternatives,) if isinstance(tag_alternatives, str) else tag_alternatives
        self.skips = (follow_ups,) if isinstance(follow_ups, (str, FileStreamerTag)) else follow_ups
        self.offset = offset
        self.direction = direction
        self.skip_tag = skip_tag
        self.seek = seek

    def __repr__(self):
        """
        **LLM Docstring**

        Show the configured tag alternatives and the skip/seek flags.

        :return: The regex source or textual representation constructed by the operation.
        :rtype: str
        """
        cls = type(self)
        return f"{cls.__name__}({self.tags=}, {self.skip_tag=}, {self.seek=})"

class LineByLineParser(metaclass=abc.ABCMeta):
    def __init__(self, stream, binary=True, encoding='utf-8', max_nesting_depth=-1, ignore_comments=False):
        """
        :param stream:
        :type stream: SearchStream
        """
        self.stream = stream
        self.binary = binary
        self.encoding = encoding
        self.max_nesting_depth = max_nesting_depth
        self.ignore_comments = ignore_comments

    def __enter__(self):
        """
        **LLM Docstring**

        Open the underlying stream and return this parser.

        :return: The opened stream, reader, parser, or checkpoint object.
        :rtype: object
        """
        self.stream.__enter__()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Close the underlying stream through its context-manager interface.

        :param exc_type: the exception class raised in the context, if any
        :type exc_type: object

        :param exc_val: the exception instance raised in the context, if any
        :type exc_val: object

        :param exc_tb: the traceback raised in the context, if any
        :type exc_tb: object
        """
        self.stream.__exit__(exc_type, exc_val, exc_tb)
    @abc.abstractmethod
    def check_tag(self, line, depth:int=0, active_tag=None, label:str=None, history:list[str]=None):
        """
        **LLM Docstring**

        Classify a line as a block boundary, value, comment, skip, or other parser tag; subclasses must implement the classification.

        :param line: the current stream line
        :type line: object

        :param depth: the current recursive block depth
        :type depth: int

        :param active_tag: the tag currently defining the block
        :type active_tag: object

        :param label: the current block label
        :type label: str

        :param history: lines or values accumulated for the current block
        :type history: list[str]

        :return: classify a line as a block boundary, value, comment, skip, or other parser tag; subclasses must implement the classification.
        :rtype: object
        """
        ...
    def handle_block_line(self, label, line, depth=0, history:list[str]=None):
        """
        **LLM Docstring**

        Return a line unchanged before it is added to the current block; subclasses may transform it.

        :param label: the current block label
        :type label: object

        :param line: the current stream line
        :type line: object

        :param depth: the current recursive block depth
        :type depth: object

        :param history: lines or values accumulated for the current block
        :type history: list[str]

        :return: return a line unchanged before it is added to the current block; subclasses may transform it.
        :rtype: object
        """
        return line
    def handle_block(self, label, block, depth=0):
        """
        **LLM Docstring**

        Return an accumulated block unchanged; subclasses may convert it to another representation.

        :param label: the current block label
        :type label: object

        :param block: the candidate TeX or BibTeX source block
        :type block: object

        :param depth: the current recursive block depth
        :type depth: object

        :return: return an accumulated block unchanged; subclasses may convert it to another representation.
        :rtype: object
        """
        return block
    class LineReaderTags(enum.Enum):
        RESETTING_BLOCK_END = 'implict_end'
        BLOCK_END = 'end'
        BLOCK_START = 'block'
        COMMENT = "comment"
        SKIP = "skip"
        VALUE = "value"
        CONSUME_REST = 'consume'
    def read_stream_line(self, binary=None):
        """
        **LLM Docstring**

        Read the next iterated line and decode it when text mode is requested.

        :param binary: whether stream values should remain bytes
        :type binary: object

        :return: read the next iterated line and decode it when text mode is requested.
        :rtype: object
        """
        if binary is None:
            binary = self.binary
        data = next(iter(self.stream))
        if not binary and hasattr(data, 'decode'):
            data = data.decode(self.encoding)
        return data
    def stream_iter(self, binary=None):
        """
        **LLM Docstring**

        Yield every line from the underlying stream, decoding byte lines exactly once when operating in text mode.

        :param binary: whether stream values should remain bytes
        :type binary: object

        :return: An iterator yielding the records described above.
        :rtype: object
        """
        if binary is None:
            binary = self.binary
        line_iter = iter(self.stream)
        try:
            data = next(line_iter)
        except StopIteration:
            yield None
        test = not binary and hasattr(data, 'decode')
        if test:
            data = data.decode(self.encoding)
        yield data
        if test:
            for data in line_iter:
                data = data.decode(self.encoding)
                yield data
        else:
            for line in line_iter:
                yield line

    def find_next_block(self, binary=None, ignore_comments=None, max_nesting_depth=None,
                        aggregate_values=True, depth=0):
        """
        **LLM Docstring**

        Consume lines until a logical block ends, recursively parse nested blocks, optionally discard comments, and return either the transformed block or a one-key mapping when the block has a label.

        :param binary: whether stream values should remain bytes
        :type binary: object

        :param ignore_comments: whether comment-tagged lines are discarded
        :type ignore_comments: object

        :param max_nesting_depth: the maximum recursive block depth, with a negative value meaning unlimited
        :type max_nesting_depth: object

        :param aggregate_values: whether value-tagged lines are accumulated in the current block
        :type aggregate_values: object

        :param depth: the current recursive block depth
        :type depth: object

        :return: consume lines until a logical block ends, recursively parse nested blocks, optionally discard comments, and return either the transformed block or a one-key mapping when the block has a label.
        :rtype: object
        """
        if ignore_comments is None:
            ignore_comments = self.ignore_comments
        if max_nesting_depth is None:
            max_nesting_depth = self.max_nesting_depth

        stream_pos = self.stream.tell()
        block_data = []
        empty = True
        active_tag = None
        label = None
        try:
            sitter = self.stream_iter(binary=binary)
            for i,line in enumerate(sitter):
                if line is None: break
                empty = False
                next_tag = self.check_tag(line, depth, active_tag=active_tag, label=label, history=block_data)
                tag_label = tag_body = None
                if not isinstance(next_tag, self.LineReaderTags) and next_tag is not None:
                    if isinstance(next_tag, (str, bytes)):
                        tag_label = next_tag
                        next_tag = None
                    elif len(next_tag) == 2:
                        next_tag, tag_body = next_tag
                    else:
                        next_tag, tag_label, tag_body = next_tag
                if next_tag == self.LineReaderTags.SKIP:
                    stream_pos = self.stream.tell()
                    continue
                if ignore_comments and next_tag == self.LineReaderTags.COMMENT:
                    stream_pos = self.stream.tell()
                    continue
                if next_tag is self.LineReaderTags.VALUE:
                    if not aggregate_values:
                        next_tag = self.LineReaderTags.BLOCK_START
                    else:
                        if tag_label is not None:
                            val = self.handle_block_line(tag_label, line, depth)
                        elif tag_body is None:
                            raise ValueError("got {} tag but no associated `(key,value)` pair")
                        else:
                            val = self.handle_block_line(label, line, depth)
                        block_data.append(val)
                        stream_pos = self.stream.tell()
                        continue

                if next_tag is self.LineReaderTags.BLOCK_END:
                    if tag_body is not None: block_data.append(tag_body)
                    stream_pos = None
                    break
                elif next_tag is self.LineReaderTags.BLOCK_START:
                    if active_tag is None:
                        label = tag_label
                        if tag_body is not None: block_data.append(tag_body)
                    else:
                        if max_nesting_depth < 0 or depth < max_nesting_depth:
                            self.stream.seek(stream_pos)
                            sub_block = self.find_next_block(binary=binary, ignore_comments=ignore_comments,
                                                             max_nesting_depth=max_nesting_depth, depth=depth+1)
                            block_data.append(sub_block)
                        else:
                            break
                elif next_tag is self.LineReaderTags.RESETTING_BLOCK_END:
                    break
                elif next_tag is self.LineReaderTags.CONSUME_REST:
                    if active_tag is None:
                        label = tag_label
                        if tag_body is not None: block_data.append(tag_body)
                    block_data.extend(list(sitter))
                    stream_pos = None
                    break
                elif active_tag is not None and next_tag is not None and next_tag != active_tag:
                    if depth == 0 or (max_nesting_depth > 0 and depth >= max_nesting_depth):
                        break
                    else:
                        self.stream.seek(stream_pos)
                        sub_block = self.find_next_block(binary=binary, ignore_comments=ignore_comments,
                                                         max_nesting_depth=max_nesting_depth, depth=depth + 1)
                        block_data.append(sub_block)
                else:
                    if tag_body is not None: block_data.append(tag_body)
                    if next_tag is not None and active_tag is None:
                        active_tag = next_tag
                        stream_pos = None
                        break
                    block_data.append(self.handle_block_line(label, line, depth))
                stream_pos = self.stream.tell()
                if active_tag is None and next_tag is not None:
                    active_tag = next_tag
        except StopIteration:
            pass
        finally:
            if stream_pos is not None:
                self.stream.seek(stream_pos)

        if empty:
            return None
        else:
            if label is None:
                return self.handle_block(None, block_data)
            else:
                return {label:self.handle_block(label, block_data)}

    MAX_BLOCKS = sys.maxsize # a debug tool
    def __iter__(self):
        """
        **LLM Docstring**

        Repeatedly call `find_next_block` until exhaustion or `MAX_BLOCKS` is reached.

        :return: An iterator yielding the records described above.
        :rtype: object
        """
        block = self.find_next_block()
        for i in range(self.MAX_BLOCKS):
            if block is None: break
            yield block
            block = self.find_next_block()

class FileLineByLineReader(LineByLineParser):
    """
    Represents a file from which we'll stream blocks of data by finding tags and parsing what's between them
    """
    def __init__(self, file,
                 mode="r", binary=False, encoding="utf-8",
                 ignore_comments=False, max_nesting_depth=-1, **kw):
        """
        **LLM Docstring**

        Create a line-oriented parser over a file-backed search stream with configured binary, encoding, comment, and nesting behavior.

        :param file: a filesystem path or open file object
        :type file: object

        :param mode: the file open mode or parser multiplicity mode
        :type mode: object

        :param binary: whether stream values should remain bytes
        :type binary: object

        :param encoding: the text encoding used to convert between bytes and strings
        :type encoding: object

        :param ignore_comments: whether comment-tagged lines are discarded
        :type ignore_comments: object

        :param max_nesting_depth: the maximum recursive block depth, with a negative value meaning unlimited
        :type max_nesting_depth: object

        :param kw: extra keyword arguments forwarded to the underlying stream constructor
        :type kw: object
        """
        stream = FileSearchStream(file, binary=binary, mode=mode, encoding=encoding, **kw)
        super().__init__(stream,
                         binary='b' in stream._mode, encoding=encoding,
                         ignore_comments=ignore_comments, max_nesting_depth=max_nesting_depth
                         )
class StringLineByLineReader(LineByLineParser):
    """
    Represents a string from which we'll stream blocks of data by finding tags and parsing what's between them
    """
    def __init__(self, string, ignore_comments=False, max_nesting_depth=-1):
        """
        **LLM Docstring**

        Create a text-mode line parser over an in-memory string.

        :param string: the source string or byte sequence wrapped by the reader
        :type string: object

        :param ignore_comments: whether comment-tagged lines are discarded
        :type ignore_comments: object

        :param max_nesting_depth: the maximum recursive block depth, with a negative value meaning unlimited
        :type max_nesting_depth: object
        """
        stream = StringSearchStream(string)
        super().__init__(stream, binary=False, ignore_comments=ignore_comments, max_nesting_depth=max_nesting_depth)
class ByteLineByLineReader(LineByLineParser):
    """
    Represents a string from which we'll stream blocks of data by finding tags and parsing what's between them
    """
    def __init__(self, string, encoding="utf-8", ignore_comments=False, max_nesting_depth=-1, **kw):
        """
        **LLM Docstring**

        Create a binary line parser over an in-memory byte sequence.

        :param string: the source string or byte sequence wrapped by the reader
        :type string: object

        :param encoding: the text encoding used to convert between bytes and strings
        :type encoding: object

        :param ignore_comments: whether comment-tagged lines are discarded
        :type ignore_comments: object

        :param max_nesting_depth: the maximum recursive block depth, with a negative value meaning unlimited
        :type max_nesting_depth: object

        :param kw: extra keyword arguments forwarded to the underlying stream constructor
        :type kw: object
        """
        stream = ByteSearchStream(string, encoding=encoding, **kw)
        super().__init__(stream, binary=True, encoding=encoding,
                         ignore_comments=ignore_comments,
                         max_nesting_depth=max_nesting_depth)

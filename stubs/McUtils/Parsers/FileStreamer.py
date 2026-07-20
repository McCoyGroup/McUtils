from __future__ import annotations
import enum
from mmap import mmap
import abc, io
import sys
import textwrap
__all__ = ['FileStreamReader', 'FileStreamCheckPoint', 'FileStreamerTag', 'FileStreamReaderException', 'StringStreamReader', 'FileLineByLineReader', 'StringLineByLineReader']

class FileStreamCheckPoint:
    """
    A checkpoint for a file that can be returned to when parsing
    """

    def __init__(self, parent, revert=True):
        """
        **LLM Docstring**

        Record the reader's current byte/character offset and configure whether leaving the context restores that position.

        :param parent: the parent reader or regex node
        :type parent: object

        :param revert: whether to restore the captured position on context exit
        :type revert: object
        """
        ...

    def disable(self):
        """
        **LLM Docstring**

        Disable automatic restoration when the checkpoint context exits.

        :return: None.
        :rtype: None
        """
        ...

    def enable(self):
        """
        **LLM Docstring**

        Enable automatic restoration when the checkpoint context exits.

        :return: None.
        :rtype: None
        """
        ...

    def revert(self):
        """
        **LLM Docstring**

        Seek the parent reader back to the offset captured when this checkpoint was created.

        :return: None.
        :rtype: None
        """
        ...

    def __enter__(self):
        """
        **LLM Docstring**

        Return this checkpoint for use in a `with` statement.

        :return: The opened stream, reader, parser, or checkpoint object.
        :rtype: object
        """
        ...

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
        ...

class FileStreamReaderException(IOError):
    ...

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
        ...

    def rread(self, n=-1):
        """
        **LLM Docstring**

        Read the `n` units immediately preceding the current position, leaving the stream positioned at the beginning of the returned block.

        :param n: the requested count or fixed repetition count
        :type n: object

        :return: The text read from the requested region of the stream.
        :rtype: object
        """
        ...

    @abc.abstractmethod
    def readline(self):
        """
        **LLM Docstring**

        Define the interface for reading one line from the stream.

        :return: The text read from the requested region of the stream.
        :rtype: object
        """
        ...

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
        ...

    @abc.abstractmethod
    def tell(self):
        """
        **LLM Docstring**

        Define the interface for reporting the current stream offset.

        :return: The current stream offset.
        :rtype: int
        """
        ...

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
        ...

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
        ...

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
        ...

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
        ...

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
        ...

class ByteSearchStream(SearchStream):
    """
    A stream that is implemented for searching in byte strings
    """

    def __init__(self, data, encoding='utf-8', **kw):
        """
        :param data:
        :type data: bytearray
        :param encoding:
        :type encoding:
        :param kw:
        :type kw:
        """
        ...

    def __enter__(self):
        """
        **LLM Docstring**

        Open an in-memory `BytesIO` view over the stored byte sequence.

        :return: The opened stream, reader, parser, or checkpoint object.
        :rtype: object
        """
        ...

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
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a shortened representation of the stored bytes or active `BytesIO` object.

        :return: The regex source or textual representation constructed by the operation.
        :rtype: str
        """
        ...

    def __iter__(self):
        """
        **LLM Docstring**

        Iterate over lines from the active `BytesIO` stream.

        :return: An iterator yielding the records described above.
        :rtype: object
        """
        ...

    def read(self, n=-1):
        """
        **LLM Docstring**

        Read bytes from the active buffer and decode them with the configured encoding.

        :param n: the requested count or fixed repetition count
        :type n: object

        :return: The text read from the requested region of the stream.
        :rtype: object
        """
        ...

    def readline(self):
        """
        **LLM Docstring**

        Read one byte line and decode it with the configured encoding.

        :return: The text read from the requested region of the stream.
        :rtype: object
        """
        ...

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
        ...

    def tell(self):
        """
        **LLM Docstring**

        Return the active byte-buffer cursor offset.

        :return: The current stream offset.
        :rtype: int
        """
        ...

    def encode_tag(self, tag):
        """
        **LLM Docstring**

        Convert a text tag to bytes using the configured encoding, leaving byte tags unchanged.

        :param tag: the delimiter or search token
        :type tag: object

        :return: convert a text tag to bytes using the configured encoding, leaving byte tags unchanged.
        :rtype: object
        """
        ...

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
        ...

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
        ...

    def tag_size(self, tag):
        """
        **LLM Docstring**

        Return the encoded byte length of a search tag.

        :param tag: the delimiter or search token
        :type tag: object

        :return: The tag length in the stream's native position units.
        :rtype: int
        """
        ...

class FileSearchStream(SearchStream):
    """
    A stream that is implemented for searching in mmap-ed files
    """
    default_binary = True

    def __init__(self, file, mode='r', binary=None, encoding='utf-8', check_decoding=False, decoding_mode='strict', **kw):
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
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Show the file object/path and normalized open mode.

        :return: The regex source or textual representation constructed by the operation.
        :rtype: str
        """
        ...

    def __enter__(self):
        """
        **LLM Docstring**

        Open the file when given a path and memory-map its complete contents.

        :return: The opened stream, reader, parser, or checkpoint object.
        :rtype: object
        """
        ...

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
        ...

    def __iter__(self):
        """
        **LLM Docstring**

        Yield successive raw lines from the memory map until its cursor stops advancing.

        :return: An iterator yielding the records described above.
        :rtype: object
        """
        ...

    def handle_chunk(self, chunk):
        """
        **LLM Docstring**

        Decode byte chunks with the configured encoding and error mode, optionally converting decode failures to `ValueError`.

        :param chunk: a raw chunk read from the memory map
        :type chunk: object

        :return: decode byte chunks with the configured encoding and error mode, optionally converting decode failures to `ValueError`.
        :rtype: object
        """
        ...

    def read(self, n=-1):
        """
        **LLM Docstring**

        Read from the memory map and decode the returned chunk.

        :param n: the requested count or fixed repetition count
        :type n: object

        :return: The text read from the requested region of the stream.
        :rtype: object
        """
        ...

    def readline(self):
        """
        **LLM Docstring**

        Read one line from the memory map and decode it.

        :return: The text read from the requested region of the stream.
        :rtype: object
        """
        ...

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
        ...

    def tell(self):
        """
        **LLM Docstring**

        Return the memory-map cursor offset.

        :return: The current stream offset.
        :rtype: int
        """
        ...

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
        ...

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
        ...

    def tag_size(self, tag):
        """
        **LLM Docstring**

        Return the byte length of a tag encoded with this stream's encoding.

        :param tag: the delimiter or search token
        :type tag: object

        :return: The tag length in the stream's native position units.
        :rtype: int
        """
        ...

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
        ...

    def __enter__(self):
        """
        **LLM Docstring**

        Open a `StringIO` cursor over the stored string.

        :return: The opened stream, reader, parser, or checkpoint object.
        :rtype: object
        """
        ...

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
        ...

    def __iter__(self):
        """
        **LLM Docstring**

        Iterate over lines from the active `StringIO` object.

        :return: An iterator yielding the records described above.
        :rtype: object
        """
        ...

    def read(self, n=-1):
        """
        **LLM Docstring**

        Read characters from the active string cursor.

        :param n: the requested count or fixed repetition count
        :type n: object

        :return: The text read from the requested region of the stream.
        :rtype: object
        """
        ...

    def readline(self):
        """
        **LLM Docstring**

        Read one line from the active string cursor.

        :return: The text read from the requested region of the stream.
        :rtype: object
        """
        ...

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
        ...

    def tell(self):
        """
        **LLM Docstring**

        Return the current character offset.

        :return: The current stream offset.
        :rtype: int
        """
        ...

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
        ...

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
        ...

    def tag_size(self, tag):
        """
        **LLM Docstring**

        Return the number of characters in a tag.

        :param tag: the delimiter or search token
        :type tag: object

        :return: The tag length in the stream's native position units.
        :rtype: int
        """
        ...

class SearchStreamReader:
    """
    Represents a reader which implements finding chunks of data in a stream
    """

    def __init__(self, stream):
        """
        :param stream:
        :type stream: SearchStream
        """
        ...

    def __enter__(self):
        """
        **LLM Docstring**

        Open the wrapped search stream and return this reader.

        :return: The opened stream, reader, parser, or checkpoint object.
        :rtype: object
        """
        ...

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
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Represent the reader together with its wrapped search stream.

        :return: The regex source or textual representation constructed by the operation.
        :rtype: str
        """
        ...

    class StreamSearchDirection(enum.Enum):
        Forward = 'forward'
        Reverse = 'reverse'
        ForwardReverse = 'forward-reverse'
        ReverseForward = 'reverse-forward'

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
        ...

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
        ...

    def _find_tag(self, tag, skip_tag=True, seek=True, direction='forward'):
        """
        Finds a tag in a file

        :param header: a tag specifying a header to look for + optional follow-up processing/offsets
        :type header: FileStreamerTag
        :return: position of tag
        :rtype: int
        """
        ...

    def find_tag(self, tag, skip_tag=None, seek=None, allow_terminal=False, validator=None, return_body=False, direction='forward'):
        """
        Finds a tag in a file

        :param header: a tag specifying a header to look for + optional follow-up processing/offsets
        :type header: FileStreamerTag
        :return: position of tag
        :rtype: int
        """
        ...

    class TagSentinels(enum.Enum):
        EOF = 'end_of_file'
        Continue = 'continue'
        NextMatch = 'next_match'

    def _parse_end_block(self, start, tag_end, allow_terminal, expand_until_valid, validator, direction='forward'):
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
        ...

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
        ...

    def get_tagged_block(self, tag_start, tag_end, validator=None, tag_validator=None, allow_terminal=False, expand_until_valid=None, return_tag=False, return_end_points=False, direction='forward', block_size=500):
        """
        Pulls the string between tag_start and tag_end

        :param tag_start:
        :type tag_start: FileStreamerTag or None
        :param tag_end:
        :type tag_end: FileStreamerTag
        :return:
        :rtype:
        """
        ...

    def _parse_block(self, tag_start, tag_end, validator, tag_validator, allow_terminal, expand_until_valid, preserve_tag, return_end_points, direction):
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
        ...

    def parse_key_block(self, tag_start=None, tag_end=None, mode='Single', validator=None, tag_validator=None, expand_until_valid=False, preserve_tag=False, return_end_points=False, parser=None, parse_mode='List', num=None, pass_context=False, allow_terminal=False, direction='forward', **ignore):
        """Parses a block by starting at tag_start and looking for tag_end and parsing what's in between them

        :param key: registered key pattern to pull from a file
        :type key: str
        :return:
        :rtype:
        """
        ...

    def read(self, n=1):
        """
        **LLM Docstring**

        Read from the wrapped stream.

        :param n: the requested count or fixed repetition count
        :type n: object

        :return: The text read from the requested region of the stream.
        :rtype: object
        """
        ...

    def readline(self):
        """
        **LLM Docstring**

        Read one line from the wrapped stream.

        :return: The text read from the requested region of the stream.
        :rtype: object
        """
        ...

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
        ...

    def tell(self):
        """
        **LLM Docstring**

        Return the wrapped stream's current offset.

        :return: The current stream offset.
        :rtype: int
        """
        ...

    def find(self, tag):
        """
        **LLM Docstring**

        Find a tag in the wrapped stream using its native search operation.

        :param tag: the delimiter or search token
        :type tag: object

        :return: The matching stream offset, or `-1` when the tag is absent.
        :rtype: int
        """
        ...

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
        ...

    def skip_tag(self, tag):
        """
        **LLM Docstring**

        Call the wrapped stream's `skip_tag` operation; the supplied stream implementations do not define this method.

        :param tag: the delimiter or search token
        :type tag: object

        :return: call the wrapped stream's `skip_tag` operation; the supplied stream implementations do not define this method.
        :rtype: object
        """
        ...

    def rskip_tag(self, tag):
        """
        **LLM Docstring**

        Call the wrapped stream's `rskip_tag` operation; the supplied stream implementations do not define this method.

        :param tag: the delimiter or search token
        :type tag: object

        :return: call the wrapped stream's `rskip_tag` operation; the supplied stream implementations do not define this method.
        :rtype: object
        """
        ...

class FileStreamReader(SearchStreamReader):
    """
    Represents a file from which we'll stream blocks of data by finding tags and parsing what's between them
    """

    def __init__(self, file, mode='r', encoding='utf-8', **kw):
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
        ...

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
        ...

class ByteStreamReader(SearchStreamReader):
    """
    Represents a string from which we'll stream blocks of data by finding tags and parsing what's between them
    """

    def __init__(self, string, encoding='utf-8', **kw):
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
        ...

class FileStreamerTag:

    def __init__(self, tag_alternatives=None, follow_ups=None, offset=None, direction='forward', skip_tag=True, seek=True):
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
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Show the configured tag alternatives and the skip/seek flags.

        :return: The regex source or textual representation constructed by the operation.
        :rtype: str
        """
        ...

class LineByLineParser(metaclass=abc.ABCMeta):

    def __init__(self, stream, binary=True, encoding='utf-8', max_nesting_depth=-1, ignore_comments=False):
        """
        :param stream:
        :type stream: SearchStream
        """
        ...

    def __enter__(self):
        """
        **LLM Docstring**

        Open the underlying stream and return this parser.

        :return: The opened stream, reader, parser, or checkpoint object.
        :rtype: object
        """
        ...

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
        ...

    @abc.abstractmethod
    def check_tag(self, line, depth: int=0, active_tag=None, label: str=None, history: list[str]=None):
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

    def handle_block_line(self, label, line, depth=0, history: list[str]=None):
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
        ...

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
        ...

    class LineReaderTags(enum.Enum):
        """Real access pattern: LineReaderTags.<MemberName> (this is an enum with 7 members, e.g. LineReaderTags.RESETTING_BLOCK_END == 'implict_end'). Collapsed into a dict below purely for compactness -- do not index it as a dict in real code:"""
        _MEMBERS = {'RESETTING_BLOCK_END': 'implict_end', 'BLOCK_END': 'end', 'BLOCK_START': 'block', 'COMMENT': 'comment', 'SKIP': 'skip', 'VALUE': 'value', 'CONSUME_REST': 'consume'}

    def read_stream_line(self, binary=None):
        """
        **LLM Docstring**

        Read the next iterated line and decode it when text mode is requested.

        :param binary: whether stream values should remain bytes
        :type binary: object

        :return: read the next iterated line and decode it when text mode is requested.
        :rtype: object
        """
        ...

    def stream_iter(self, binary=None):
        """
        **LLM Docstring**

        Yield every line from the underlying stream, decoding byte lines exactly once when operating in text mode.

        :param binary: whether stream values should remain bytes
        :type binary: object

        :return: An iterator yielding the records described above.
        :rtype: object
        """
        ...

    def find_next_block(self, binary=None, ignore_comments=None, max_nesting_depth=None, aggregate_values=True, depth=0):
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
        ...
    MAX_BLOCKS = sys.maxsize

    def __iter__(self):
        """
        **LLM Docstring**

        Repeatedly call `find_next_block` until exhaustion or `MAX_BLOCKS` is reached.

        :return: An iterator yielding the records described above.
        :rtype: object
        """
        ...

class FileLineByLineReader(LineByLineParser):
    """
    Represents a file from which we'll stream blocks of data by finding tags and parsing what's between them
    """

    def __init__(self, file, mode='r', binary=False, encoding='utf-8', ignore_comments=False, max_nesting_depth=-1, **kw):
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
        ...

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
        ...

class ByteLineByLineReader(LineByLineParser):
    """
    Represents a string from which we'll stream blocks of data by finding tags and parsing what's between them
    """

    def __init__(self, string, encoding='utf-8', ignore_comments=False, max_nesting_depth=-1, **kw):
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
        ...
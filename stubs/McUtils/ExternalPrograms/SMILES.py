import functools
import multiprocessing
from .. import Devutils as dev
from .RDKit import RDMolecule
import numpy as np
import hashlib
__all__ = ['SMILESSupplier', 'consume_smiles_supplier', 'match_smiles_supplier', 'smarts_matcher']

class SMILESSupplier:

    def __init__(self, smiles_file, line_indices=None, name=None, size=int(1000.0), split_idx=0, split_char=None, line_parser=None):
        """
        **LLM Docstring**

        Set up a streaming reader over a (potentially very large) SMILES file, using a
        line-offset index for random access.

        :param smiles_file: the SMILES file (path or stream)
        :type smiles_file: str
        :param line_indices: precomputed byte offsets, or a `.npy` path to load them from
        :type line_indices: np.ndarray | str | None
        :param name: an optional name for the supplier
        :type name: str | None
        :param size: the initial offset-index size
        :type size: int
        :param split_idx: which whitespace/`split_char`-delimited field holds the SMILES
        :type split_idx: int
        :param split_char: the field separator (defaults to whitespace)
        :type split_char: str | bytes | None
        :param line_parser: a custom line-to-SMILES parser
        :type line_parser: Callable | None
        """
        ...

    @classmethod
    def from_name(cls, name):
        """
        **LLM Docstring**

        Build a supplier for one of the known SMILES databases (e.g. `zinc20`,
        `emols`, `pubchem`).

        :param name: the database name
        :type name: str
        :return: the supplier
        :rtype: SMILESSupplier
        """
        ...

    def to_mp_state(self):
        """
        **LLM Docstring**

        Serialize the minimal state needed to rebuild this supplier in a worker process.

        :return: the picklable state tuple
        :rtype: tuple
        """
        ...

    @classmethod
    def from_mp_state(cls, state, line_indices=None, **extra):
        """
        **LLM Docstring**

        Rebuild a supplier from the state produced by `to_mp_state`, optionally with a
        fresh offset index.

        :param state: the state tuple from `to_mp_state`
        :type state: tuple
        :param line_indices: precomputed byte offsets for this worker's block
        :type line_indices: np.ndarray | None
        :param extra: extra constructor overrides
        :return: the supplier
        :rtype: SMILESSupplier
        """
        ...

    def __enter__(self):
        """
        **LLM Docstring**

        Open the underlying stream (reentrantly), initializing the offset index and
        default parser on the outermost entry.

        :return: the opened stream
        :rtype: object
        """
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Close the underlying stream on the outermost exit, restoring the offset index and
        parser.

        :param exc_type: the exception type, if any
        :param exc_val: the exception value, if any
        :param exc_tb: the traceback, if any
        """
        ...

    def __len__(self):
        """
        **LLM Docstring**

        The number of entries in the file, building the full line index if it isn't
        already known.

        :return: the entry count
        :rtype: int
        """
        ...

    @classmethod
    def _split_smi(cls, line: bytes, encoding='utf-8', split_idx=0, split_char=None, maxsplit=-1):
        """
        **LLM Docstring**

        Extract the SMILES field from a raw (bytes) line by splitting and decoding.

        :param line: the raw line
        :type line: bytes
        :param encoding: the text encoding
        :type encoding: str
        :param split_idx: which field holds the SMILES
        :type split_idx: int
        :param split_char: the field separator (whitespace if omitted)
        :type split_char: bytes | None
        :param maxsplit: the maximum number of splits
        :type maxsplit: int
        :return: the SMILES string
        :rtype: str
        """
        ...

    def _default_parser(self, line):
        """
        **LLM Docstring**

        The default line parser: extract the configured SMILES field from a line.

        :param line: the raw line
        :type line: bytes
        :return: the SMILES string
        :rtype: str
        """
        ...

    @classmethod
    def _consume_next(self, db, parser):
        """
        **LLM Docstring**

        Read and parse the next line from the stream, returning the raw (empty) line at
        end of file.

        :param db: the open stream
        :param parser: the line parser
        :type parser: Callable
        :return: the parsed SMILES, or the empty line at EOF
        :rtype: str | bytes
        """
        ...

    def find_smi(self, n, block_size=None):
        """
        **LLM Docstring**

        Seek to and read the `n`-th entry (extending the line index if needed),
        optionally reading a block of `block_size` consecutive entries.

        :param n: the entry index
        :type n: int
        :param block_size: number of consecutive entries to read
        :type block_size: int | None
        :return: the SMILES entry, or a list of entries
        :rtype: str | list[str]
        """
        ...

    def consume_iter(self, start_at=None, upto=None):
        """
        **LLM Docstring**

        Iterate over the SMILES entries from `start_at` up to `upto` (or the end),
        recording byte offsets as it goes when the index is assignable.

        :param start_at: the starting entry index (defaults to the current position)
        :type start_at: int | None
        :param upto: the exclusive stopping index (or the end if omitted)
        :type upto: int | None
        :return: a generator of SMILES strings
        :rtype: Iterator[str]
        """
        ...

    def __next__(self):
        """
        **LLM Docstring**

        Read the entry at the current cursor position (the supplier must be open).

        :return: the SMILES entry
        :rtype: str
        :raises ValueError: if the supplier hasn't been opened via `with`
        """
        ...

    def __iter__(self):
        """
        **LLM Docstring**

        Iterate over all entries from the current position.

        :return: a generator of SMILES strings
        :rtype: Iterator[str]
        """
        ...

    def _expand_offset_if_needed(self, n):
        """
        **LLM Docstring**

        Grow the offset-index array (doubling it) when entry `n` would exceed its
        current length; errors if the index is fixed-size.

        :param n: the entry index that must fit
        :type n: int
        :raises ValueError: if the offsets are not flexible/growable
        """
        ...

    def create_line_index(self, upto=None, return_index=True):
        """
        **LLM Docstring**

        Scan the file to build (or extend) the byte-offset index, up to `upto` entries or
        the end of the file.

        :param upto: the entry index to build up to (or the whole file if omitted)
        :type upto: int | None
        :param return_index: return the offsets rather than just building them
        :type return_index: bool
        :return: the offset index, or `None`
        :rtype: np.ndarray | None
        """
        ...

    @classmethod
    def save_line_index(cls, file, line_index):
        """
        **LLM Docstring**

        Save a byte-offset index to a `.npy` file, down-casting it to the smallest
        unsigned integer dtype that fits.

        :param file: the output file
        :type file: str
        :param line_index: the offset index
        :type line_index: np.ndarray
        :return: the result of `np.save`
        """
        ...

def _consume_supplier_mp(state, consumer, line_offset, block_size):
    """
    **LLM Docstring**

    Worker entry point: rebuild a supplier from its multiprocessing state, consume a
    block of entries, and return the consumer's per-entry results.

    :param state: the supplier state from `to_mp_state`
    :type state: tuple
    :param consumer: the per-SMILES callable
    :type consumer: Callable
    :param line_offset: the byte offset of this block's first entry
    :type line_offset: int
    :param block_size: the number of entries in this block
    :type block_size: int
    :return: the non-`None` consumer results
    :rtype: list
    """
    ...

def consume_smiles_supplier(supplier: SMILESSupplier, consumer, pool=None, start_at=None, upto=None, initializer=None):
    """
    **LLM Docstring**

    Apply a consumer function to the SMILES entries of a supplier, optionally in
    parallel across a multiprocessing pool (splitting the entries into per-worker
    blocks).

    :param supplier: the SMILES supplier
    :type supplier: SMILESSupplier
    :param consumer: the per-SMILES callable (its non-`None` results are collected)
    :type consumer: Callable
    :param pool: a pool, process count, `True` for a default pool, or `None` for serial
    :type pool: object | int | bool | None
    :param start_at: the starting entry index
    :type start_at: int | None
    :param upto: the exclusive stopping index
    :type upto: int | None
    :param initializer: a worker initializer
    :type initializer: Callable | None
    :return: the collected results
    :rtype: list
    """
    ...

def _match_rdkit(matcher, smi, error_value=None, sanitize=False, **parser_options):
    """
    **LLM Docstring**

    Return the SMILES string if its molecule contains the SMARTS substructure match,
    else the error value; sanitizes and retries on a substructure-match runtime
    error.

    :param matcher: the compiled SMARTS query mol
    :param smi: the SMILES string
    :type smi: str
    :param error_value: the value returned when parsing fails
    :param sanitize: sanitize the parsed molecule
    :type sanitize: bool
    :param parser_options: extra SMILES-parsing options
    :return: the SMILES on a match, else the error value
    :rtype: str | None
    """
    ...

def _disable_rdkit_log(blockage=[]):
    """
    **LLM Docstring**

    Suppress RDKit's C++ logging for the current (worker) process, keeping the
    block-logs object alive in a module-level list.

    :param blockage: a persistent list holding the active block-logs objects
    :type blockage: list
    """
    ...

def smarts_matcher(pattern, error_value=None, sanitize=True, **parser_options):
    """
    **LLM Docstring**

    Build a matcher callable that tests whether a SMILES string contains a given
    SMARTS substructure.

    :param pattern: the SMARTS pattern
    :type pattern: str
    :param error_value: the value returned when parsing fails
    :param sanitize: sanitize the query and candidates
    :type sanitize: bool
    :param parser_options: extra SMILES-parsing options
    :return: the matcher callable
    :rtype: Callable
    """
    ...

def match_smiles_supplier(supplier: SMILESSupplier, matcher, pool=None, start_at=None, upto=None, quiet=True, out_file=None, initializer=None):
    """
    **LLM Docstring**

    Match every SMILES entry in a supplier against a SMARTS pattern (or matcher),
    optionally in parallel and with RDKit logging suppressed, and optionally write
    the matches to a file.

    :param supplier: the SMILES supplier
    :type supplier: SMILESSupplier
    :param matcher: a matcher callable, or a SMARTS pattern string
    :type matcher: Callable | str
    :param pool: a pool/process count for parallel matching
    :type pool: object | int | bool | None
    :param start_at: the starting entry index
    :type start_at: int | None
    :param upto: the exclusive stopping index
    :type upto: int | None
    :param quiet: suppress RDKit logging
    :type quiet: bool
    :param out_file: an output file path, or `True` to auto-name one
    :type out_file: str | bool | None
    :param initializer: a worker initializer
    :type initializer: Callable | None
    :return: the matching SMILES strings
    :rtype: list[str]
    """
    ...
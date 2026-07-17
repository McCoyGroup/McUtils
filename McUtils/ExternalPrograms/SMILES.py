import functools
import multiprocessing

from .. import Devutils as dev
from .RDKit import RDMolecule
import numpy as np
import hashlib

__all__ = [
    "SMILESSupplier",
    "consume_smiles_supplier",
    "match_smiles_supplier",
    "smarts_matcher"
]

class SMILESSupplier:
    def __init__(self, smiles_file, line_indices=None, name=None,
                 size=int(1e3),
                 split_idx=0,
                 split_char=None,
                 line_parser=None):
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
        self.name = name
        self.smi = dev.StreamInterface(smiles_file, mode='rb')
        self.line_indices = line_indices
        self._size = size
        self._call_depth = 0
        self._stream = None
        self._cur = None
        self._max_offset = None
        self._offsets:np.ndarray[(None,), int] = None
        self._flexible_offsets = None
        self._assignable_offsets = None
        self._encoding = self.smi.get_encoding()
        self._binary = self.smi.is_binary()
        if isinstance(split_char, str) and self._binary:
            split_char = split_char.encode(self._encoding)
        self.split_char = split_char
        self.split_idx = split_idx
        self._line_parser = line_parser
        self.line_parser = line_parser

    known_suppliers = {
        "zinc20": {
            'smiles_file': 'ZINC20.smi',
            'line_indices': 'ZINC20_idx.npy',
            'split_idx': 0
        },
        "emols": {
            'smiles_file': 'emolecule_sc_2026_01_01.smi',
            'line_indices': 'molecule_sc_2026_01_01_idx.npy',
            'split_idx': 0
        },
        "pubchem":{
            'smiles_file':'pubchem_cid_smi_2026_01.smi',
            'line_indices':'pubchem_cid_smi_2026_01_idx.npy',
            'split_idx':1
        }
    }
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
        return cls(**cls.known_suppliers[name], name=name)

    def to_mp_state(self):
        """
        **LLM Docstring**

        Serialize the minimal state needed to rebuild this supplier in a worker process.

        :return: the picklable state tuple
        :rtype: tuple
        """
        return (
            self.smi._input,
            self.name,
            self.split_idx,
            self.split_char,
            self._line_parser
        )
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
        smi, name, split_idx, split_char, line_parser = state
        kwargs = {}
        kwargs['line_indices'] = line_indices
        kwargs['name'] = name
        kwargs['split_idx'] = split_idx
        kwargs['split_char'] = split_char
        kwargs['line_parser'] = line_parser
        kwargs.update(extra)

        return cls(
            smi,
            **kwargs
        )

    def __enter__(self):
        """
        **LLM Docstring**

        Open the underlying stream (reentrantly), initializing the offset index and
        default parser on the outermost entry.

        :return: the opened stream
        :rtype: object
        """
        self._call_depth += 1
        if self._call_depth == 1:
            if self.line_parser is None:
                self.line_parser = self._default_parser
            self._stream = self.smi.__enter__()
            self._cur = 0
            if self.line_indices is None:
                #TODO: add an array offset style index to this
                #      in case the SMI file is too big for even uint64
                self._max_offset = 0
                self.line_indices = np.zeros(self._size, dtype='uint64')
            if isinstance(self.line_indices, np.ndarray):
                self._offsets = self.line_indices
                self._flexible_offsets = True
                self._assignable_offsets = True
            else:
                self._offsets = np.load(self.line_indices, mmap_mode='r')
                self._flexible_offsets = False
                self._assignable_offsets = False
            if self._max_offset is None:
                self._max_offset = len(self._offsets) - 1
        return self._stream
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Close the underlying stream on the outermost exit, restoring the offset index and
        parser.

        :param exc_type: the exception type, if any
        :param exc_val: the exception value, if any
        :param exc_tb: the traceback, if any
        """
        self._call_depth -= 1
        if self._call_depth == 0:
            self.line_parser = self._line_parser
            self._cur = None
            self._stream.__exit__(exc_type, exc_val, exc_tb)
            self._stream = None
            if self._flexible_offsets:
                self.line_indices = self._offsets
            self._offsets = None

    def __len__(self):
        """
        **LLM Docstring**

        The number of entries in the file, building the full line index if it isn't
        already known.

        :return: the entry count
        :rtype: int
        """
        with self:
            if self._flexible_offsets:
                self.create_line_index(return_index=False)
                return self._max_offset
            else:
                return self._max_offset
    @classmethod
    def _split_smi(cls, line:bytes, encoding='utf-8', split_idx=0, split_char=None, maxsplit=-1):
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
        if split_char is None:
            return line.split(maxsplit=maxsplit)[split_idx].strip().decode(encoding)
        else:
            return line.split(sep=split_char, maxsplit=maxsplit)[split_idx].strip().decode(encoding)
    def _default_parser(self, line):
        """
        **LLM Docstring**

        The default line parser: extract the configured SMILES field from a line.

        :param line: the raw line
        :type line: bytes
        :return: the SMILES string
        :rtype: str
        """
        return self._split_smi(line, split_idx=self.split_idx, split_char=self.split_char, encoding=self._encoding)

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
        line = db.readline()
        if len(line) == 0:
            return line
        else:
            return parser(line)
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
        with self as db:
            #TODO: add ability to stream line indices to avoid reading them into memory
            if n >= self._max_offset:
                self.create_line_index(n, return_index=False)
            db.seek(self._offsets[n])
            if block_size is None:
                self._cur = n
                return self._consume_next(db, self.line_parser)
            else:
                self._cur = n + block_size
                if n + block_size >= self._max_offset:
                    blocks = []
                    for m in range(block_size):
                        if self._assignable_offsets:
                            self._expand_offset_if_needed(n+m)
                            self._offsets[n+m] = db.tell()
                        blocks.append(self._consume_next(db, self.line_parser))
                    return blocks
                else:
                    return [
                        self._consume_next(db, self.line_parser)
                        for _ in range(block_size)
                    ]
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
        with self as db:
            if start_at is None:
                start_at = self._cur
            else:
                self.create_line_index(upto=start_at, return_index=False)
            ninds = start_at
            try:
                db.seek(self._offsets[ninds])
                if upto is None:
                    smi = self._consume_next(db, self.line_parser)
                    while len(smi) > 0:
                        ninds += 1
                        if self._assignable_offsets:
                            self._expand_offset_if_needed(ninds)
                            self._offsets[ninds] = db.tell()
                        yield smi
                        smi = self._consume_next(db, self.line_parser)
                else:
                    if ninds >= upto: return
                    smi = self._consume_next(db, self.line_parser)
                    while ninds < upto and len(smi) > 0:
                        ninds += 1
                        if self._assignable_offsets:
                            self._expand_offset_if_needed(ninds)
                            self._offsets[ninds] = db.tell()
                        yield smi
                        smi = self._consume_next(db, self.line_parser)
            finally:
                self._cur = ninds
                self._max_offset = max(self._max_offset, ninds)

    def __next__(self):
        """
        **LLM Docstring**

        Read the entry at the current cursor position (the supplier must be open).

        :return: the SMILES entry
        :rtype: str
        :raises ValueError: if the supplier hasn't been opened via `with`
        """
        if self._stream is None:
            cls = type(self)
            raise ValueError(f"{cls.__name__} must be opened via `with` before it can be iterated over")
        with self as db:
            db.seek(self._offsets[self._cur])
            return self._consume_next(db, self.line_parser)

    def __iter__(self):
        """
        **LLM Docstring**

        Iterate over all entries from the current position.

        :return: a generator of SMILES strings
        :rtype: Iterator[str]
        """
        return self.consume_iter()

    def _expand_offset_if_needed(self, n):
        """
        **LLM Docstring**

        Grow the offset-index array (doubling it) when entry `n` would exceed its
        current length; errors if the index is fixed-size.

        :param n: the entry index that must fit
        :type n: int
        :raises ValueError: if the offsets are not flexible/growable
        """
        if n >= len(self._offsets):
            if not self._flexible_offsets:
                raise ValueError(f"{self._max_offset} `line_indices` were passed, but db extends beyond that")
            else:
                new_offsets = np.zeros(2 * len(self._offsets), dtype='uint64')
                new_offsets[:len(self._offsets)] = self._offsets
                self._offsets = new_offsets
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
        with self as db:
            if not self._assignable_offsets:
                if return_index:
                    return self._offsets[:self._max_offset]
                else:
                    return None
            ninds = self._max_offset
            db.seek(self._offsets[ninds])
            try:
                if upto is None:
                    l = len(db.readline())
                    while l > 0:
                        ninds += 1
                        self._expand_offset_if_needed(ninds)
                        self._offsets[ninds] = self._offsets[ninds-1] + l
                        if not self._binary:
                            if db.peek(1) == "\r": self._offsets[ninds] += 1
                        l = len(db.readline())
                else:
                    if ninds < upto:
                        l = len(db.readline())
                        while ninds < upto and l > 0:
                            ninds += 1
                            self._expand_offset_if_needed(ninds)
                            self._offsets[ninds] = self._offsets[ninds-1] + l
                            if not self._binary:
                                if db.peek(1) == "\r": self._offsets[ninds] += 1
                            # self._offsets[ninds] = db.tell()
                            l = len(db.readline())
            finally:
                self._max_offset = ninds
            if return_index:
                return self._offsets[:self._max_offset]
            else:
                return None
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
        max_offset = line_index[-1]
        for dtype in [np.uint16, np.uint32, np.uint64]:
            if max_offset < np.iinfo(dtype).max:
                line_index = line_index.astype(dtype)
                break
        return np.save(file, line_index)

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
    offsets = np.full(block_size, line_offset)
    supplier = SMILESSupplier.from_mp_state(state, line_indices=offsets)
    res = []
    with supplier:
        for smi in supplier.consume_iter(start_at=0, upto=block_size):
            subres = consumer(smi)
            if subres is not None: res.append(subres)
    return res

def consume_smiles_supplier(supplier:SMILESSupplier, consumer, pool=None, start_at=None, upto=None, initializer=None):
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
    if pool is True:
        pool = multiprocessing.Pool(initializer=initializer)
    elif dev.is_int(pool):
        pool = multiprocessing.Pool(pool, initializer=initializer)

    if pool is None:
        res = []
        with supplier:
            for smi in supplier.consume_iter(start_at=start_at, upto=upto):
                subres = consumer(smi)
                if subres is not None: res.append(subres)

        return res
    else:
        with supplier:
            max_size = len(supplier) if upto is None else upto
            offsets = supplier._offsets # TODO: gross
            nproc = pool._processes
            block_size = max_size // nproc
            num_blocks = int(np.ceil(max_size / block_size))
            block_starts_sizes = [
                (offsets[block_size*i], min([block_size, max_size - (block_size*i+1) + 1]))
                for i in range(num_blocks)
            ]
            #TODO: don't access the `_input` argument directly...
            state = supplier.to_mp_state()
            args = [(state, consumer) + bs for bs in block_starts_sizes]
        res = pool.starmap(_consume_supplier_mp, args)

        return sum(res, [])

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
    from .RDKit import RDKitInterface
    AllChem = RDKitInterface.submodule("Chem.AllChem")

    mol = RDMolecule.parse_smiles(smi, sanitize=sanitize, **parser_options)
    if mol is None: return error_value
    if not sanitize:
        try:
            if mol.GetSubstructMatch(matcher): return smi
        except RuntimeError:
            AllChem.SanitizeMol(mol)
            if mol.GetSubstructMatch(matcher): return smi
    else:
        if mol.GetSubstructMatch(matcher): return smi


def _disable_rdkit_log(blockage=[]):
    """
    **LLM Docstring**

    Suppress RDKit's C++ logging for the current (worker) process, keeping the
    block-logs object alive in a module-level list.

    :param blockage: a persistent list holding the active block-logs objects
    :type blockage: list
    """
    from rdkit.rdBase import BlockLogs
    bl = BlockLogs()
    blockage.append([bl,  bl.__enter__()])

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
    from .RDKit import RDKitInterface
    AllChem = RDKitInterface.submodule("Chem.AllChem")
    smarts_candidate = AllChem.MolFromSmarts(pattern)
    if sanitize:
        smarts_candidate.UpdatePropertyCache()
        AllChem.SanitizeMol(smarts_candidate)
        AllChem.GetSSSR(smarts_candidate)
    matcher = functools.partial(_match_rdkit, smarts_candidate,
                                error_value=error_value,
                                sanitize=sanitize,
                                **parser_options)
    return matcher


def match_smiles_supplier(supplier:SMILESSupplier, matcher, pool=None,
                          start_at=None, upto=None, quiet=True,
                          out_file=None,
                          initializer=None):
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
    from rdkit.rdBase import BlockLogs
    smarts_tag = str(matcher)
    if isinstance(matcher, str):
        from .RDKit import RDKitInterface
        AllChem = RDKitInterface.submodule("Chem.AllChem")
        smarts_candidate = AllChem.MolFromSmarts(matcher)
        matcher = functools.partial(_match_rdkit, smarts_candidate)
        if quiet and initializer is None:
            initializer = _disable_rdkit_log

    if out_file is True:
        out_file_bits = [
            "match",
            "{name}" if supplier.name is not None else None,
            "s{start}" if start_at is not None else None,
            "t{to}" if upto is not None else None,
            "{smarts_key}.smi"
        ]
        out_file = "_".join(b for b in out_file_bits if b is not None)

    hash_obj = hashlib.md5(smarts_tag.encode('utf-8'))
    smarts_key = hash_obj.hexdigest()
    if isinstance(out_file, str):
        out_file = out_file.format(
            name=supplier.name,
            start=start_at,
            to=upto,
            smarts_key=smarts_key,
            smarts_tag=smarts_tag)

    if quiet:
        with BlockLogs():
            matches = consume_smiles_supplier(supplier, matcher, pool=pool, start_at=start_at, upto=upto, initializer=initializer)
    else:
        matches = consume_smiles_supplier(supplier, matcher, pool=pool, start_at=start_at, upto=upto, initializer=initializer)

    if out_file is not None:
        with dev.StreamInterface(out_file, mode='w+') as match_output:
            match_output.write(f"SMARTS: {smarts_tag} ({smarts_key})\n")
            for match in matches:
                match_output.write(match + "\n")

    return matches
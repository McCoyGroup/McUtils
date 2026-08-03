from __future__ import annotations

import functools
import multiprocessing

from .. import Devutils as dev
from .. import Numputils as nput
from .RDKit import RDMolecule
import numpy as np
import hashlib
import itertools
import json

import re
from typing import (
    Any,
    Callable,
    ClassVar,
    Collection,
    Iterator,
    NamedTuple,
)

__all__ = [
    "SMILESSupplier",
    "consume_smiles_supplier",
    "match_smiles_supplier",
    "smarts_matcher",
    "join_smiles_fragments",
    "set_smiles_chiralities",
    "set_smiles_stereochemistry",
    "set_smiles_bond_order",
    "renumber_smiles_atom_map",
    "get_canonical_smiles_renumbering",
    "smiles_binding_sites",
    "set_smiles_binding_sites",
    "remove_smiles_binding_sites",
    "substitute_smiles_atoms",
    "parse_smiles_and_atom_map",
    "build_templated_smiles",
    "SMILESTokenizer"
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
        self._offsets:'np.ndarray[(None,), int]' = None
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
    AllChem = RDMolecule.allchem_api()

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
    AllChem = RDMolecule.allchem_api()
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
        AllChem = RDMolecule.allchem_api()
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



def _get_atom_idx(mol, map_num):
    for atom in mol.GetAtoms():
        if atom.GetAtomMapNum() == map_num:
            return atom.GetIdx()
    raise ValueError(f"Atom map number {map_num} not found in molecule.")
def _check_ring_aromatic(new_mol, ring_indices):
    return all(
        new_mol.GetAtomWithIdx(i).GetIsAromatic() for i in ring_indices
    )
def _break_ring_aromaticities(new_mol, idx2):
    ring_info = new_mol.GetRingInfo()
    all_atom_rings = ring_info.AtomRings()
    aromatic_rings = {
        r:_check_ring_aromatic(new_mol, r) if idx2 not in r else False
        for r in all_atom_rings
    }
    for ring in all_atom_rings:
        if idx2 in ring:
            other_atoms = [idx for idx in ring if idx != idx2]
        else:
            continue
        for idx in other_atoms:
            if (
                    new_mol.GetAtomWithIdx(idx).GetIsAromatic()
                and not any(is_aromatic for ring,is_aromatic in aromatic_rings.items() if idx in ring)
            ):
                _break_aromaticity(new_mol, new_mol, idx, idx, break_rings=False)
def _push_inc_bond(new_mol, idx:int, visted:set):
    # TODO: check that valencies are bad first
    a1 = new_mol.GetAtomWithIdx(idx)
    visted.add(idx)
    for b in a1.GetBonds():
        t = b.GetBondTypeAsDouble()
        if t < 2:
            targs = [b.GetBeginAtomIdx(), b.GetEndAtomIdx()]
            if (
                    any(t not in visted for t in targs)
                    and not any(new_mol.GetAtomWithIdx(t).GetSymbol() == "H" for t in targs)
            ):
                new_type = get_rdkit_bond_type(t + 1)
                b.SetBondType(new_type)
                for x2 in targs:
                    if x2 not in visted:
                        _push_dec_bond(new_mol, x2, visted)
                break
def _push_dec_bond(new_mol, idx:int, visted:set):
    #TODO: check that valencies are bad first
    a1 = new_mol.GetAtomWithIdx(idx)
    visted.add(idx)
    for b in a1.GetBonds():
        t = b.GetBondTypeAsDouble()
        if t > 1:
            targs = [b.GetBeginAtomIdx(), b.GetEndAtomIdx()]
            if (
                    any(t not in visted for t in targs)
                    and not any(new_mol.GetAtomWithIdx(t).GetSymbol() == "H" for t in targs)
            ):
                new_type = get_rdkit_bond_type(t - 1)
                b.SetBondType(new_type)
                for x2 in targs:
                    if x2 not in visted:
                        _push_inc_bond(new_mol, x2, visted)
                break

def _break_aromaticity(ref_mol, new_mol, idx1, idx2,
                       original_aromaticity_map,
                       push_bonds=True, break_rings=True, check_valences=False):
    Chem = RDMolecule.allchem_api()
    a1 = ref_mol.GetAtomWithIdx(idx1)
    is_aromatic = a1.GetIsAromatic()
    fixed = False
    if break_rings and is_aromatic:
        a1 = new_mol.GetAtomWithIdx(idx2)
        a1.SetIsAromatic(False)
        for b in a1.GetBonds():
            if b.GetBondType() == Chem.BondType.AROMATIC:
                b.SetBondType(Chem.BondType.SINGLE)
                fixed = True
        if fixed and break_rings:
            _break_ring_aromaticities(new_mol, idx2)
    if not fixed and push_bonds:
        visited = {idx2}
        _push_dec_bond(new_mol, idx2, visited)
        if check_valences:
            for x in visited:
                a = new_mol.GetAtomWithIdx(x)
                if a.HasValenceViolation():
                    if original_aromaticity_map[x]:
                        a.SetIsAromatic(True)
                        for b in a.GetBonds():
                            b.SetBondType(Chem.BondType.Aromatic)
                    else:
                        while a.HasValenceViolation():
                            for b in a.GetBonds():
                                t = b.GetBondTypeAsDouble()
                                if t > 1:
                                    new_type = get_rdkit_bond_type(t - 1)
                                    b.SetBondType(new_type)
                            else:
                                break


    return is_aromatic
def _pop_hydrogen(ref_mol, new_mol, idx1, idx2):
    a1 = ref_mol.GetAtomWithIdx(idx1)
    implicit_hs = a1.GetNumImplicitHs()
    explicit_hs = a1.GetNumExplicitHs()
    if implicit_hs > 0:
        return False
    elif explicit_hs > 0:
        a1 = new_mol.GetAtomWithIdx(idx2)
        explicit_hs = a1.GetNumExplicitHs()
        a1.SetNumExplicitHs(explicit_hs - 1)
        return False
    else:
        # Find one explicit neighbor on the new mol
        a1 = new_mol.GetAtomWithIdx(idx2)
        for neighbor in a1.GetNeighbors():
            if neighbor.GetAtomicNum() == 1:
                h_idx = neighbor.GetIdx()
                new_mol.RemoveAtom(h_idx)
                return True
        return False
def _add_hydrogen(new_mol, idx1, allow_explicit=True):
    Chem = RDMolecule.allchem_api()
    a1 = new_mol.GetAtomWithIdx(idx1)
    implicit_hs = not a1.GetNoImplicit()
    explicit_hs = a1.GetNumExplicitHs()
    if implicit_hs:
        return False
    elif explicit_hs >= 0 and allow_explicit:
        explicit_hs = a1.GetNumExplicitHs()
        a1.SetNumExplicitHs(explicit_hs + 1)
        return False
    else:
        # Find one explicit neighbor on the new mol
        a = Chem.Atom("H")
        idx2 = new_mol.AddAtom(a)
        new_mol.AddBond(idx2, idx1, Chem.BondType.SINGLE)
        return True
def parse_smiles_and_atom_map(smiles1, cache,
                              add_implicit_hydrogens=False,
                              reorder_from_atom_map=True):
    if cache is None: cache = {}
    key = (smiles1, add_implicit_hydrogens, reorder_from_atom_map)
    if key not in cache:
        mol = RDMolecule.parse_smiles(smiles1, remove_hydrogens=True,
                                      add_implicit_hydrogens=add_implicit_hydrogens,
                                      reorder_from_atom_map=reorder_from_atom_map)
        if mol is not None:
            map = {a.GetAtomMapNum(): a.GetIdx() for a in mol.GetAtoms()}
            map.pop(0, None)
        else:
            map = None
        cache[key] = {'mol': mol, 'map': map}
    return cache[key]
def get_rdkit_bond_type(t, as_number=False):
    Chem = RDMolecule.allchem_api()
    if nput.is_numeric(t):
        if as_number: return t
        if t == 1:
            t = Chem.BondType.SINGLE
        elif t == 2:
            t = Chem.BondType.DOUBLE
        elif t == 3:
            t = Chem.BondType.TRIPLE
        elif 1 < t and t < 2:
            t = Chem.BondType.AROMATIC
        elif 2 < t and t < 3:
            t = Chem.BondType.TWOANDAHALF
        elif 3 < t and t < 4:
            t = Chem.BondType.THREEANDAHALF
        else:
            raise ValueError(f"Bond type {t} is not supported.")
    elif not as_number:
        bond_type_map = {
            Chem.BondType.SINGLE: 1.0,
            Chem.BondType.DOUBLE: 2.0,
            Chem.BondType.TRIPLE: 3.0,
            Chem.BondType.AROMATIC: 1.5,
            Chem.BondType.TWOANDAHALF: 2.5,
            Chem.BondType.THREEANDAHALF: 3.5,
            Chem.BondType.UNSPECIFIED: 0.0
        }
        return bond_type_map[t]
    return t
def remove_smiles_binding_sites(smi,
                             sites=None,
                             cache=None,
                             add_implicit_hydrogens='full'):
    Chem = RDMolecule.allchem_api()
    mol_data = parse_smiles_and_atom_map(smi, cache=cache, add_implicit_hydrogens=add_implicit_hydrogens)

    mol = Chem.Mol(mol_data['mol'])
    map = mol_data['map']
    if sites is None:
        sites = [x-1 for x in map.keys()]
    for idx in sites:
        idx = map.get(idx+1)
        if idx is not None:
            mol.GetAtomWithIdx(idx).SetAtomMapNum(0)

    if add_implicit_hydrogens:
        mol = Chem.RemoveHs(mol)

    return Chem.MolToSmiles(mol)
def _is_valence_site(a):
    if (
            a.GetNumImplicitHs() > 0
            or a.GetNumExplicitHs() > 0
    ):
        return True
    for b in a.GetNeighbors():
        if b.GetSymbol() == 'H':
            return True
    else:
        for b in a.GetBonds():
            t = b.GetBondTypeAsDouble()
            if t > 1:
                return True
    return False
def _get_mol_valence_sites(mol):
    sites = []
    for i,a in enumerate(mol.GetAtoms()):
        if _is_valence_site(a):  sites.append(i)
    return sites
def smiles_binding_sites(smi,
                         cache=None,
                        valence_site_fallback=True,
                         add_implicit_hydrogens='full'):
    # Chem = RDMolecule.allchem_api()
    mol_data = parse_smiles_and_atom_map(smi, cache=cache, add_implicit_hydrogens=add_implicit_hydrogens)
    map = mol_data['map']
    if len(map) == 0:
        return _get_mol_valence_sites(mol_data['mol'])
    else:
        return [k-1 for k in map.keys()]
def set_smiles_binding_sites(smi,
                             site_map,
                             cache=None,
                             add_implicit_hydrogens='full'):
    Chem = RDMolecule.allchem_api()
    mol_data = parse_smiles_and_atom_map(smi, cache=cache, add_implicit_hydrogens=add_implicit_hydrogens)
    if not dev.is_dict_like(site_map):
        site_map = {n:i for i,n in enumerate(site_map)}
    site_map = {k:v for k,v in mol_data['map'].items()} | site_map

    mol = Chem.Mol(mol_data['mol'])
    for k,v in site_map.items():
        mol.GetAtomWithIdx(k).SetAtomMapNum(v+1)

    if add_implicit_hydrogens:
        mol = Chem.RemoveHs(mol)

    return Chem.MolToSmiles(mol)
def substitute_smiles_atoms(smi,
                            site_atom_map,
                            cache=None,
                            resanitize=True,
                            preserve_valence_defect=True,
                            add_implicit_hydrogens='full',
                            return_mol=False):
    Chem = RDMolecule.allchem_api()
    pt = Chem.GetPeriodicTable()
    mol_data = parse_smiles_and_atom_map(smi, cache=cache, add_implicit_hydrogens=add_implicit_hydrogens)

    mol = Chem.RWMol(mol_data['mol'])
    map = mol_data['map']
    for site, atom_type in site_atom_map.items():
        if isinstance(atom_type, str):
            atom_type = {'element':atom_type}
        idx = map[site + 1]
        atom = mol.GetAtomWithIdx(idx)
        if preserve_valence_defect:
            cur_valence = atom.GetTotalValence()
            defect = pt.GetDefaultValence(atom.GetSymbol()) - cur_valence
        else:
            defect = None
        new_atom = Chem.Atom(atom_type['element'])
        if 'charge' in atom_type:
            new_atom.SetFormalCharge(atom_type['charge'])
        new_atom.SetAtomMapNum(atom.GetAtomMapNum())
        mol.ReplaceAtom(idx, new_atom)
        if defect is not None:
            mol.UpdatePropertyCache(strict=False)
            new_atom = mol.GetAtomWithIdx(idx)
            cur_valence = new_atom.GetTotalValence()
            defect2 = pt.GetDefaultValence(new_atom.GetSymbol()) - cur_valence
            defect_diff = defect2 - defect
            if defect_diff != 0:
                implicit_hs = not new_atom.GetNoImplicit()
                if implicit_hs and 'charge' not in atom_type:
                    new_atom.SetFormalCharge(new_atom.GetFormalCharge() - defect_diff)
                elif defect_diff < 0:
                    for i in range(int(np.ceil(-defect_diff))):
                        _pop_hydrogen(mol, mol, idx, idx)
                else:
                    for i in range(int(np.ceil(defect_diff))):
                        _add_hydrogen(mol, idx)

    mol = mol.GetMol()

    if resanitize:
        Chem.SanitizeMol(mol)
    if add_implicit_hydrogens:
        mol = Chem.RemoveHs(mol, sanitize=resanitize)

    if return_mol:
        return mol
    else:
        return Chem.MolToSmiles(mol)
def join_smiles_fragments(scaffold: str, functional_group: str,
                          new_bonds=((0, 0),),
                          cache=None,
                          resanitize=True,
                          add_implicit_hydrogens='full',
                          fallback_to_ordering=False,
                          decrement_hydrogens=True,
                          prekekulize=True,
                          push_bonds=False,
                          return_fragment_indices=False,
                          return_bond_indices=False,
                          return_mol=False) -> str | tuple['str', tuple[list[int], list[int]]]:
    Chem = RDMolecule.allchem_api()
    if cache is None:
        cache = {}
    mol_data1 = parse_smiles_and_atom_map(scaffold, cache, add_implicit_hydrogens=add_implicit_hydrogens)
    mol_data2 = parse_smiles_and_atom_map(functional_group, cache, add_implicit_hydrogens=add_implicit_hydrogens)
    mol1 = mol_data1['mol']
    mol2 = mol_data2['mol']

    if mol1 is None:
        raise ValueError(f"bad SMILES {scaffold}")
    if mol1 is None:
        raise ValueError(f"bad SMILES {functional_group}")

    map1 = mol_data1['map']
    map2 = mol_data2['map']
    offset = mol1.GetNumAtoms()

    map2 = {m+offset: i+offset for m,i in map2.items()}

    # Combine both molecules into one (no bond yet)
    if return_fragment_indices:
        mol1 = Chem.Mol(mol1)
        for b in mol1.GetAtoms():
            b.SetIntProp("mol_idx", 0)
        mol2 = Chem.Mol(mol2)
        for b in mol2.GetAtoms():
            b.SetIntProp("mol_idx", 1)

    combined = Chem.CombineMols(mol1, mol2)
    editable = Chem.RWMol(combined)

    if isinstance(push_bonds, str):
        break_scaffold_aromaticity = dev.str_is(push_bonds, 'scaffold')
        break_fg_aromaticity = dev.str_is(push_bonds, 'functional')
    else:
        break_scaffold_aromaticity = break_fg_aromaticity = push_bonds

    if prekekulize:
        try:
            Chem.Kekulize(editable, clearAromaticFlags=True)
        except Chem.rdchem.KekulizeException:
            ...

    original_aromaticity_map = [a.GetIsAromatic() for a in combined.GetAtoms()]
    dearomitized_atoms = []
    bond_indices = []
    for b in new_bonds:
        if len(b) == 2:
            m1, m2 = b
            t = 1
        else:
            m1, m2, t = b
        if fallback_to_ordering:
            if m1+1 not in map1:
                map1 = map1.copy()
                map1[m1 + 1] = m1
            if m2+offset+1 not in map2:
                map2 = map2.copy()
                map2[m2+offset+1] = m2+offset
        idx1 = map1[m1 + 1]
        idx2 = map2[m2 + offset + 1]

        if nput.is_numeric(t):
            if t == 1:
                t = Chem.BondType.SINGLE
            elif t == 2:
                t = Chem.BondType.DOUBLE
            elif t == 3:
                t = Chem.BondType.TRIPLE
            elif 1 < t and t < 2:
                t = Chem.BondType.AROMATIC
            else:
                raise ValueError(f"Bond type {t} is not supported.")

        editable.AddBond(idx1, idx2, t)
        if decrement_hydrogens:
            dearomitized_mods = [False, False]
            i2 = idx2 - offset
            for _ in range(int(np.ceil(get_rdkit_bond_type(t, as_number=True)))):
                editable.UpdatePropertyCache(strict=False)
                if break_scaffold_aromaticity:
                    dearomitized = _break_aromaticity(mol1, editable, idx1, idx1, original_aromaticity_map)
                else:
                    dearomitized = False
                if not dearomitized:
                    modified = _pop_hydrogen(mol1, editable, idx1, idx1)
                else:
                    modified = False
                    if not dearomitized_mods[0]:
                        dearomitized_mods[0] = True
                        dearomitized_atoms.append(editable.GetAtomWithIdx(idx1))
                if modified:
                    idx2 = idx2 - 1
                    map2 = {m:i-1 for m,i in map2.items()}
                if break_fg_aromaticity:
                    dearomitized = _break_aromaticity(mol2, editable, i2, idx2, original_aromaticity_map)
                else:
                    dearomitized = False
                if not dearomitized:
                    _pop_hydrogen(mol2, editable, i2, idx2)
                else:
                    if not dearomitized_mods[1]:
                        dearomitized_mods[1] = True
                        dearomitized_atoms.append(editable.GetAtomWithIdx(idx2))
        bond_indices.append([idx1, idx2]) # can be modified
    dearomitized_atoms = [a.GetIdx() for a in dearomitized_atoms]
    joined = editable.GetMol()

    if resanitize:
        Chem.SanitizeMol(joined)

    for idx in dearomitized_atoms:
        joined.GetAtomWithIdx(idx).SetProp("dearomitized", "true")

    for m,i in map1.items():
        joined.GetAtomWithIdx(i).SetAtomMapNum(m)
    for m,i in map2.items():
        joined.GetAtomWithIdx(i).SetAtomMapNum(m - offset + len(map1))

    if add_implicit_hydrogens:
        for i,a in enumerate(joined.GetAtoms()):
            a.SetIntProp('preremoval_idx', i)
        joined = Chem.RemoveHs(joined, sanitize=resanitize)

    for atom in joined.GetAtoms():
        if atom.GetPropsAsDict().get('dearomitized'):
            atom.SetIsAromatic(False)

    if return_fragment_indices:
        f1 = []
        f2 = []
        for a in joined.GetAtoms():
            if a.GetIntProp('mol_idx') == 0:
                f1.append(a.GetIdx())
            else:
                f2.append(a.GetIdx())
    if return_mol:
        if return_fragment_indices:
            res = (joined, (f1, f2))
        else:
            res = (joined,)
        if return_bond_indices:
            res += (new_bonds,)
    else:
        smi = Chem.MolToSmiles(joined)
        res = (smi,)
        if return_fragment_indices or return_bond_indices:
            idx = json.loads(joined.GetProp("_smilesAtomOutputOrder"))
        if return_fragment_indices:
            j1, j2 = [], []
            for n,i in enumerate(idx):
                if i in f1:
                    j1.append(n)
                else:
                    j2.append(n)
            res += ((j1, j2),)
        if return_bond_indices:
            idx_map = {i:a.GetIntProp('preremoval_idx') for i,a in enumerate(joined.GetAtoms())}
            map = {idx_map[i]:n for n,i in enumerate(idx)}
            new_bonds = [
                (map[b[0]], map[b[1]])
                for b in bond_indices
            ]
            res += (new_bonds,)
    if len(res) == 1:
        res = res[0]
    return res

def get_canonical_smiles_renumbering(smiles,
                                     cache=None,
                                     reorder_from_atom_map=False,
                                     add_implicit_hydrogens=False):
    Chem = RDMolecule.allchem_api()
    if cache is None:
        cache = {}
    mol_data = parse_smiles_and_atom_map(smiles, cache,
                                         add_implicit_hydrogens=add_implicit_hydrogens,
                                         reorder_from_atom_map=reorder_from_atom_map)
    mol = mol_data['mol']
    if add_implicit_hydrogens:
        mol = Chem.RemoveHs(mol)

    smi = Chem.MolToSmiles(mol)
    idx = json.loads(mol.GetProp("_smilesAtomOutputOrder"))
    return smi, idx

def renumber_smiles_atom_map(smiles,
                             remapping,
                             cache=None,
                             shift=True,
                             add_implicit_hydrogens=False):
    Chem = RDMolecule.allchem_api()
    if cache is None:
        cache = {}
    mol_data = parse_smiles_and_atom_map(smiles, cache, add_implicit_hydrogens=add_implicit_hydrogens)
    mol = mol_data['mol']
    map = mol_data['map']

    mol = Chem.Mol(mol)
    map = map.copy()
    for i,j in remapping.items():
        i = i + 1
        j = j + 1
        cur_i = map[i]
        cur_j = map.get(j)
        del map[i]
        map[j] = cur_i
        if cur_j is not None:
            if shift:
                k = j+1
                while k in map:
                    tmp = map[k]
                    map[k] = cur_j
                    cur_j = tmp
                    k = k + 1
                else:
                    map[k] = cur_j
            else:
                map[i] = cur_j
    for i,a in map.items():
        mol.GetAtomWithIdx(a).SetAtomMapNum(i)
    if add_implicit_hydrogens:
        mol = Chem.RemoveHs(mol)

    return Chem.MolToSmiles(mol)

def set_smiles_bond_order(smiles, start, end, order,
                          cache=None,
                          adjust_hydrogens=True,
                          add_implicit_hydrogens=False,
                          resanitize=False,
                          return_mol=False):
    Chem = RDMolecule.allchem_api()
    if cache is None:
        cache = {}
    mol_data = parse_smiles_and_atom_map(smiles, cache=cache, add_implicit_hydrogens=add_implicit_hydrogens)
    start = mol_data['map'][start + 1]
    end = mol_data['map'][end + 1]
    editable = Chem.RWMol(mol_data['mol'])
    b = editable.GetBondBetweenAtoms(start, end)
    ext_type = b.GetBondTypeAsDouble()
    order = get_rdkit_bond_type(order)
    order_num = get_rdkit_bond_type(order, as_number=True)
    if ext_type != order_num:
        b.SetBondType(order)
        if adjust_hydrogens:
            if ext_type > order_num:
                for i in range(int(np.ceil(ext_type - order_num))):
                    _add_hydrogen(editable, start)
                    _add_hydrogen(editable, end)
            else:
                for i in range(int(np.ceil(ext_type - order_num))):
                    _pop_hydrogen(mol_data['mol'], editable, start, start)
                    _pop_hydrogen(mol_data['mol'], editable, end, end)
    mol = editable.GetMol()
    if add_implicit_hydrogens is not None:
        mol = Chem.RemoveHs(mol)
    if return_mol:
        return mol
    else:
        return Chem.MolToSmiles(mol)

def set_smiles_chiralities(base_smiles, site_chirality_map, cache=None,
                           add_implicit_hydrogens='full',
                           return_mol=False):
    Chem = RDMolecule.allchem_api()
    mol_data = parse_smiles_and_atom_map(base_smiles, cache=cache, add_implicit_hydrogens=add_implicit_hydrogens)
    mol = Chem.Mol(mol_data['mol'])

    atom_map_pos = mol_data['map']
    for map_num, winding in site_chirality_map.items():
        atom_idx = atom_map_pos[map_num+1]
        winding_map = {
            "CW": Chem.ChiralType.CHI_TETRAHEDRAL_CW,
            "CCW": Chem.ChiralType.CHI_TETRAHEDRAL_CCW,
        }
        if winding.upper() not in winding_map:
            raise ValueError("winding must be 'CW' or 'CCW'")
        atom = mol.GetAtomWithIdx(atom_idx)


        atom.SetChiralTag(winding_map[winding.upper()])

    Chem.AssignStereochemistry(mol, cleanIt=True, force=True)
    if add_implicit_hydrogens is not None:
        mol = Chem.RemoveHs(mol)
    if return_mol:
        return mol
    else:
        return Chem.MolToSmiles(mol)

def _get_stereoreference_index(atom, other_index):
    valid_neighbors = []
    for neighbor in atom.GetNeighbors():
        n_idx = neighbor.GetIdx()
        if n_idx == other_index: continue

        if neighbor.HasProp('_CIPRank'):
            rank = neighbor.GetIntProp('_CIPRank')
        else:
            rank = -1  # Fallback for implicit or unranked atoms (like Hydrogens)

        valid_neighbors.append((rank, n_idx))
    valid_neighbors.sort(reverse=True, key=lambda x: x[0])
    return valid_neighbors[0][1] if valid_neighbors else None
def set_smiles_stereochemistry(base_smiles,
                               site_pair_stereo_map,
                               cache=None,
                               add_implicit_hydrogens='full',
                               return_mol=False):
    Chem = RDMolecule.allchem_api()
    mol_data = parse_smiles_and_atom_map(base_smiles, cache=cache, add_implicit_hydrogens=add_implicit_hydrogens)
    mol = Chem.Mol(mol_data['mol'])

    atom_map_pos = mol_data['map']
    stereo_map = {
        'trans':Chem.BondStereo.STEREOE,
        'e':Chem.BondStereo.STEREOE,
        'cis':Chem.BondStereo.STEREOZ,
        'z':Chem.BondStereo.STEREOZ,
        'any':Chem.BondStereo.STEREOANY
    }

    for bond, stereo_atag in site_pair_stereo_map.items():
        if len(bond) == 4:
            i, j, k, l = [atom_map_pos[a+1] if a is not None else None for a in bond]
        else:
            j, k = [atom_map_pos[a+1] for a in bond]
            i, l = None, None
        if i is None:
            i = _get_stereoreference_index(mol.GetAtomWithIdx(j), k)
        if l is None:
            l = _get_stereoreference_index(mol.GetAtomWithIdx(k), j)
        if i is None or l is None:
            if add_implicit_hydrogens is not None:
                mol = Chem.RemoveHs(mol)
            smi = Chem.MolToSmiles(mol)
            raise ValueError(f"bad stereorefs ({i}, {l}) for bond ({j}, {k}) in {smi} ")
        stereo = stereo_map[stereo_atag.lower()]
        # TODO: ensure this is robust, might need to iterate on this
        bond = mol.GetBondBetweenAtoms(j, k)
        bond.SetStereo(stereo)
        bond.SetStereoAtoms(i, l)
        if stereo == Chem.BondStereo.STEREOE:
            mol.GetBondBetweenAtoms(i, j).SetBondDir(Chem.BondDir.ENDDOWNRIGHT)
            mol.GetBondBetweenAtoms(k, l).SetBondDir(Chem.BondDir.ENDDOWNRIGHT)
        elif stereo == Chem.BondStereo.STEREOZ:
            mol.GetBondBetweenAtoms(i, j).SetBondDir(Chem.BondDir.ENDUPRIGHT)
            mol.GetBondBetweenAtoms(k, l).SetBondDir(Chem.BondDir.ENDDOWNRIGHT)
        elif stereo == Chem.BondStereo.STEREOANY:
            mol.GetBondBetweenAtoms(i, j).SetBondDir(Chem.BondDir.EITHERDOUBLE)
            mol.GetBondBetweenAtoms(k, l).SetBondDir(Chem.BondDir.EITHERDOUBLE)
    Chem.AssignStereochemistry(mol, cleanIt=True, force=True)
    if add_implicit_hydrogens is not None:
        mol = Chem.RemoveHs(mol)
    if return_mol:
        return mol
    else:
        return Chem.MolToSmiles(mol)

def build_templated_smiles(
        scaffold,
        *replacements,
        active_sites=None,
        chiralities=None,
        stereos=None,
        bond_orders=None,
        atom_replacements=None,
        cache=None,
        add_implicit_hydrogens='full',
        remove_sites=False,
        return_fragment_indices=False,
        return_new_bonds=False,
):
    if cache is None: cache = {}
    if active_sites is not None:
        scaffold = set_smiles_binding_sites(scaffold,
                                            active_sites,
                                            cache=cache,
                                            add_implicit_hydrogens=add_implicit_hydrogens)
    fragments = None
    rfi = (
            return_fragment_indices
            or return_new_bonds
    )
    bond_indices = []
    new_bonds = []
    for i,replacement in enumerate(replacements):
        if isinstance(replacement, str):
            replacement = {
                "functional_group": replacement
            }
        if 'new_bonds' not in replacement:
            replacement = replacement.copy()
            bo = replacement.pop('bond_order', 1)
            replacement['new_bonds'] = [[i, 0, bo]]
        scaffold = join_smiles_fragments(scaffold,
                                         cache=cache,
                                         add_implicit_hydrogens=add_implicit_hydrogens,
                                         return_fragment_indices=rfi,
                                         return_bond_indices=return_new_bonds,
                                         **replacement)
        if return_new_bonds:
            bond_indices = scaffold[2]
            scaffold = scaffold[:2]
        if rfi:
            scaffold, (f1, f2) = scaffold
            if fragments is not None:
                new_bonds = [
                    [(f1[b[0]], f1[b[1]]) + b[2:]  for b in nb_list]
                    for nb_list in new_bonds
                ]
                fragments = tuple(
                    [f1[i] for i in f]
                    for f in fragments
                ) + (f2,)
            else:
                fragments = (f1, f2)
        if return_new_bonds:
            new_bonds.append([
                (x[0], x[1], b[2] if len(b) > 2 else 1)
                for x, b in zip(bond_indices, replacement['new_bonds'])
            ])

    # _ = []
    # if return_new_bonds:
    #     for i, (bi, bb) in enumerate(zip(bond_indices, new_bonds)):
    #         f = sum(fragments[:i + 2], [])
    #         _.append([
    #             (f[x[0]], f[x[1]], b[2] if len(b) > 2 else 1)
    #             for x, b in zip(bi, bb)
    #         ])
    # new_bonds = _
    if atom_replacements is not None:
        scaffold = substitute_smiles_atoms(scaffold, atom_replacements,
                                           cache=cache,
                                           add_implicit_hydrogens=add_implicit_hydrogens)
    if bond_orders is not None:
        for start,end,t in bond_orders:
            scaffold = set_smiles_bond_order(scaffold, start, end, t,
                                               cache=cache,
                                               add_implicit_hydrogens=add_implicit_hydrogens)
    if chiralities is not None:
        scaffold = set_smiles_chiralities(scaffold,
                                          chiralities,
                                          cache=cache,
                                          add_implicit_hydrogens=add_implicit_hydrogens)
    if stereos is not None:
        scaffold = set_smiles_stereochemistry(scaffold,
                                              stereos,
                                              cache=cache,
                                              add_implicit_hydrogens=add_implicit_hydrogens)
    if remove_sites:
        if remove_sites is True: remove_sites = None
        scaffold = remove_smiles_binding_sites(scaffold, remove_sites,
                                               cache=cache,
                                               add_implicit_hydrogens=add_implicit_hydrogens)
    res = (scaffold,)
    if return_fragment_indices:
        res += (fragments,)
    if return_new_bonds:
        res += (new_bonds,)
    if len(res) == 1:
        res = res[0]
    return res


Metadata = dict[str, Any]


class SMILESAtom(NamedTuple):
    index: int
    symbol: str
    previous: int | None
    bond_order: float | None
    bond_stereochemistry: str | None
    stereochemistry: str | None
    metadata: Metadata

class AnnotatedAtom(NamedTuple):
    atom: SMILESAtom
    annotation: str
    annotation_start: int
    annotation_end: int

class SMILESTokenizer:
    """
    Atom-only SMILES tokenizer.

    Regular expressions are compiled lazily and cached at the class
    level. Each instance controls which bracket metadata fields are
    retained.
    """

    SUPPORTED_METADATA: ClassVar[frozenset[str]] = frozenset({
        "isotope",
        "hydrogens",
        "charge",
        "atom_map",
    })

    BOND_ORDERS: ClassVar[dict[str, float]] = {
        "-": 1.0,
        "=": 2.0,
        "#": 3.0,
        "$": 4.0,
        ":": 1.5,
        "/": 1.0,
        "\\": 1.0,
    }

    BOND_STEREOCHEMISTRY: ClassVar[frozenset[str]] = frozenset({
        "/",
        "\\",
    })

    UNBRACKETED_ATOMS: ClassVar[frozenset[str]] = frozenset({
        "B", "C", "N", "O", "P", "S", "F", "I",
        "Cl", "Br",
        "b", "c", "n", "o", "p", "s",
        "*",
    })

    AROMATIC_ATOMS: ClassVar[frozenset[str]] = frozenset({
        "b", "c", "n", "o", "p", "s", "se", "as",
    })

    _REGEX_SOURCES: ClassVar[dict[str, str]] = {
        "bracket_atom": (
            r"^(?P<isotope>\d+)?"
            r"(?P<symbol>[A-Z][a-z]?|[bcnops]|se|as|\*)"
            r"(?P<body>.*)$"
        ),
        "chirality": (
            r"@(?:@|TH\d*|AL\d*|SP\d*|TB\d*|OH\d*)?"
        ),
        "hydrogens": r"H(?P<count>\d*)",
        "charge": r"(?P<charge>[+-]\d+|\++|-+)",
        "atom_map": r":(?P<map>\d+)",
    }

    _REGEX_CACHE: ClassVar[dict[str, re.Pattern[str]]] = {}

    def __init__(
        self,
        *,
        metadata_fields: Collection[str] | None = None,
    ) -> None:
        if metadata_fields is None:
            metadata_fields = self.SUPPORTED_METADATA

        self.metadata_fields = frozenset(metadata_fields)
        unknown = self.metadata_fields - self.SUPPORTED_METADATA

        if unknown:
            raise ValueError(
                f"Unsupported metadata fields: {sorted(unknown)}"
            )

    @classmethod
    def _regex(cls, name: str) -> re.Pattern[str]:
        """
        Compile a named regular expression on first use.
        """
        try:
            return cls._REGEX_CACHE[name]
        except KeyError:
            try:
                source = cls._REGEX_SOURCES[name]
            except KeyError:
                raise KeyError(f"Unknown regular expression {name!r}") from None

            pattern = re.compile(source)
            cls._REGEX_CACHE[name] = pattern
            return pattern

    @staticmethod
    def _parse_charge(text: str) -> int:
        sign = 1 if text[0] == "+" else -1
        suffix = text[1:]

        if suffix.isdigit():
            return sign * int(suffix)

        return sign * len(text)

    def _parse_bracket_atom(
        self,
        token: str,
    ) -> tuple[str, str | None, Metadata]:
        match = self._regex("bracket_atom").fullmatch(token[1:-1])

        if match is None:
            raise ValueError(f"Invalid bracket atom: {token!r}")

        symbol = match.group("symbol")
        body = match.group("body")
        metadata: Metadata = {}

        chirality_match = self._regex("chirality").search(body)
        stereochemistry = (
            chirality_match.group()
            if chirality_match is not None
            else None
        )

        if "isotope" in self.metadata_fields:
            isotope = match.group("isotope")
            metadata["isotope"] = int(isotope) if isotope else None

        if "hydrogens" in self.metadata_fields:
            hydrogen_match = self._regex("hydrogens").search(body)

            if hydrogen_match is None:
                metadata["hydrogens"] = 0
            else:
                count = hydrogen_match.group("count")
                metadata["hydrogens"] = int(count) if count else 1

        if "charge" in self.metadata_fields:
            charge_match = self._regex("charge").search(body)
            metadata["charge"] = (
                self._parse_charge(charge_match.group("charge"))
                if charge_match is not None
                else 0
            )

        if "atom_map" in self.metadata_fields:
            map_match = self._regex("atom_map").search(body)
            metadata["atom_map"] = (
                int(map_match.group("map"))
                if map_match is not None
                else None
            )

        return symbol, stereochemistry, metadata

    def _default_bond_order(
        self,
        previous_symbol: str,
        symbol: str,
    ) -> float:
        if (
            previous_symbol in self.AROMATIC_ATOMS
            and symbol in self.AROMATIC_ATOMS
        ):
            return 1.5

        return 1.0

    @staticmethod
    def _read_ring_label(
        smiles: str,
        position: int,
    ) -> tuple[str, int]:
        """
        Consume ``1``, ``%12``, or ``%(123)`` ring syntax.
        """
        if smiles[position].isdigit():
            return smiles[position], position + 1

        if position + 1 >= len(smiles):
            raise ValueError(
                f"Incomplete ring label at position {position}"
            )

        if smiles[position + 1] == "(":
            end = smiles.find(")", position + 2)

            if end < 0:
                raise ValueError(
                    f"Unclosed ring label at position {position}"
                )

            label = smiles[position + 2:end]
            if not label.isdigit():
                raise ValueError(
                    f"Invalid ring label {smiles[position:end + 1]!r}"
                )

            return label, end + 1

        label = smiles[position + 1:position + 3]

        if len(label) != 2 or not label.isdigit():
            raise ValueError(
                f"Invalid ring label at position {position}"
            )

        return label, position + 3

    def tokenize(self, smiles: str) -> Iterator[SMILESAtom]:
        """
        Generate atom tokens in SMILES traversal order.

        Non-atom tokens are consumed but not yielded. ``previous`` is
        the index of the atom from which the generated atom branches.
        """
        atoms: list[SMILESAtom] = []
        branches: list[int] = []
        current: int | None = None
        pending_bond: str | None = None
        position = 0

        def add_atom(
            symbol: str,
            stereochemistry: str | None = None,
            metadata: Metadata | None = None,
        ) -> None:
            nonlocal current, pending_bond

            bond_stereochemistry = (
                pending_bond
                if pending_bond in self.BOND_STEREOCHEMISTRY
                else None
            )

            if current is None:
                bond_order = None
            elif pending_bond is not None:
                bond_order = self.BOND_ORDERS[pending_bond]
            else:
                bond_order = self._default_bond_order(
                    atoms[current].symbol,
                    symbol,
                )

            atoms.append(
                SMILESAtom(
                    index=len(atoms),
                    symbol=symbol,
                    previous=current,
                    bond_order=bond_order,
                    bond_stereochemistry=bond_stereochemistry,
                    stereochemistry=stereochemistry,
                    metadata=metadata or {},
                )
            )

            current = len(atoms) - 1
            pending_bond = None

        while position < len(smiles):
            character = smiles[position]

            if character.isspace():
                position += 1
                continue

            if character == "[":
                end = smiles.find("]", position + 1)

                if end < 0:
                    raise ValueError(
                        f"Unclosed bracket atom at position {position}"
                    )

                symbol, stereochemistry, metadata = (
                    self._parse_bracket_atom(
                        smiles[position:end + 1]
                    )
                )
                add_atom(symbol, stereochemistry, metadata)
                position = end + 1
                continue

            pair = smiles[position:position + 2]

            if pair in {"Cl", "Br"}:
                add_atom(pair)
                position += 2
                continue

            if character in self.UNBRACKETED_ATOMS:
                add_atom(character)
                position += 1
                continue

            if character in self.BOND_ORDERS:
                if pending_bond is not None:
                    raise ValueError(
                        f"Consecutive bond symbols at position {position}"
                    )

                pending_bond = character
                position += 1
                continue

            if character == "(":
                if current is None:
                    raise ValueError(
                        f"Branch before an atom at position {position}"
                    )

                branches.append(current)
                position += 1
                continue

            if character == ")":
                if not branches:
                    raise ValueError(
                        f"Unmatched ')' at position {position}"
                    )

                if pending_bond is not None:
                    raise ValueError(
                        f"Branch ends after a bond at position {position}"
                    )

                current = branches.pop()
                position += 1
                continue

            if character == ".":
                if pending_bond is not None:
                    raise ValueError(
                        f"Bond immediately before '.' at position {position}"
                    )

                current = None
                position += 1
                continue

            if character.isdigit() or character == "%":
                _, position = self._read_ring_label(smiles, position)
                pending_bond = None
                continue

            raise ValueError(
                f"Unrecognized SMILES character {character!r} "
                f"at position {position}"
            )

        if branches:
            raise ValueError(
                f"{len(branches)} unclosed branch expression(s)"
            )

        if pending_bond is not None:
            raise ValueError(
                f"SMILES ends after bond symbol {pending_bond!r}"
            )

        yield from atoms

    def annotate(
        self,
        smiles: str,
        annotation: str,
        k: int,
        *,
        require_all_annotations: bool = True,
    ) -> Iterator[AnnotatedAtom]:
        """
        Add annotation slices and offsets to the base atom stream.
        """
        if k <= 0 or k % 2:
            raise ValueError(
                f"k must be a positive even integer; received {k}"
            )

        offset = 0

        for atom in self.tokenize(smiles):
            width = k // 2 if atom.index == 0 else k
            end = offset + width

            if end > len(annotation):
                raise ValueError(
                    f"Annotation ended before atom {atom.index}: "
                    f"needed [{offset}:{end}], but its length is "
                    f"{len(annotation)}"
                )

            yield AnnotatedAtom(
                atom=atom,
                annotation=annotation[offset:end],
                annotation_start=offset,
                annotation_end=end,
            )

            offset = end

        if require_all_annotations and offset != len(annotation):
            raise ValueError(
                f"{len(annotation) - offset} unused annotation "
                f"characters remain at offset {offset}"
            )
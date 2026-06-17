from __future__ import annotations

import io

import numpy as np
from collections import namedtuple
from pathlib import Path
from typing import Union
import re

from ...Parsers import FileLineByLineReader, RegexPattern, Number, Integer, Whitespace, StartOfString, Optional

__all__ = [
    "CubeFileData",
    "CubeFileParser"
]


CubeFileAtomData = namedtuple(
    "CubeFileAtomData",
    [
        "numbers",
        "positions",
        "charges",
        "mo_indices"
    ]
)
CubeFileGridData = namedtuple(
    "CubeFileGridData",
    [
        "origin",
        "axes",
        "steps"
    ]
)
CubeFileData = namedtuple(
    "CubeFileData",
    [
        "header",
        "atoms",
        "grid",
        "values"
    ]
)

class CubeFileParser(FileLineByLineReader):
    def __init__(self, file, **kw):
        super().__init__(file, max_nesting_depth=0, **kw)
        self._flags = []
        self._total_atoms = -1

    _grid_tag_pat = RegexPattern([StartOfString, Optional(Whitespace),
                                  Integer, Whitespace, Number, Whitespace, Number, Whitespace, Number])
    @classmethod
    def _is_grid_tag(cls, line):
        return cls._grid_tag_pat.match(line)
    def check_tag(self, line:str, depth:int=0, active_tag=None, label:str=None, history:list[str]=None):
        if len(line.strip()) == 0:
            return self.LineReaderTags.SKIP
        if label == 'header' and self._is_grid_tag(line):
            return self.LineReaderTags.RESETTING_BLOCK_END, None, None
        elif label == 'grid' and len(history) == 4:
            return self.LineReaderTags.RESETTING_BLOCK_END, None, None
        elif label == 'atoms' and len(history) == self._total_atoms:
            return self.LineReaderTags.RESETTING_BLOCK_END, None, None
        elif label is None:
            if 'header' not in self._flags:
                self._flags.append('header')
                return self.LineReaderTags.BLOCK_START, 'header', line
            elif 'grid' not in self._flags:
                self._flags.append('grid')
                self._total_atoms = int(line.strip().split()[0])
                if self._total_atoms < 0:
                    self._total_atoms = abs(self._total_atoms) + 1
                return self.LineReaderTags.BLOCK_START, 'grid', line
            elif 'atoms' not in self._flags:
                self._flags.append('atoms')
                return self.LineReaderTags.BLOCK_START, 'atoms', line
            else:
                return self.LineReaderTags.CONSUME_REST, 'values', line

    @classmethod
    def _parse_atoms(cls, atom_lines, has_mo_fields=False):
        if has_mo_fields:
            mo_stuff = atom_lines[-1].split()
            atom_lines = atom_lines[:-1]
            n_mos = int(mo_stuff[0])
            mo_indices = [int(mo_stuff[i + 1]) for i in range(n_mos)]
        else:
            mo_indices = None
        numbers = []
        positions = np.zeros((len(atom_lines), 3))
        charges = np.zeros(len(atom_lines))
        for i,al in enumerate(atom_lines):
            bits = al.split()
            numbers.append(int(bits[0]) if bits[0].isdigit() else bits[0])
            if len(bits) > 3:
                charges[i] = float(bits[1])
                positions[i] = [float(x) for x in bits[2:]]
            else:
                positions[i] = [float(x) for x in bits[1:]]
        return CubeFileAtomData(numbers, positions, charges, mo_indices)

    @classmethod
    def _parse_grid(cls, grid_lines):
        origin = np.array(grid_lines[0].split()[1:]).astype(float)
        axes = np.zeros((3, 3))
        steps = np.zeros(3, dtype=int)
        for i,line in enumerate(grid_lines[1:]):
            bits = line.split()
            steps[i] = int(bits[0])
            axes[i] = [float(x) for x in bits[1:]]
        return CubeFileGridData(origin, axes, steps)
    def handle_block(self, label:'str|None', block_data, join=True, depth=0):
        if label == 'atoms':
            return self._parse_atoms(block_data)
        elif label == 'grid':
            return self._parse_grid(block_data)
        elif label == 'header':
            return "".join(block_data)
        elif label == 'values':
            ugh = io.StringIO("".join(block_data).replace("\n", " "))
            return np.loadtxt(ugh).reshape(-1)
        else:
            return block_data

    def parse(self):
        bits = list(iter(self))
        res = bits[0]
        for b in bits[1:]:
            res = res | b
        return CubeFileData(**res)

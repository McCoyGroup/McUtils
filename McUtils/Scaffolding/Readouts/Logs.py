"""
Readout for McUtils block-structured logs (written by `Logger`, read with `LogParser`): block
structure, per-block contents, and numeric values that recur across blocks (``key: value`` lines
and ``took 1.23s`` timings) as series. Only the first ``max_blocks`` blocks are shown in full.
"""

import os
import re

import numpy as np

from ...Jupyter.Readouts import (
    ReadoutAdapter, readout_section, ReadoutSectionUnavailable, ReadoutSection, ReadoutFields, ReadoutTable,
    ReadoutCode, ReadoutText, FieldSet, Field, Column, TabularData, line_chart,
)

__all__ = [
    "LogReadout",
]

_KEY_VALUE = re.compile(r"^\s*([A-Za-z][\w \-/().]*?)\s*[:=]\s*([-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?)\s*([A-Za-z/%]*)\s*$")
_TOOK = re.compile(r"\btook\s+([-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?)\s*(s|sec|seconds|ms)?\b", re.I)


class _Block:
    def __init__(self, tag, lines, children):
        self.tag, self.lines, self.children = tag, lines, children

    def text(self, depth=0):
        pad = "  " * depth
        out = [pad + l.strip() for l in self.lines]
        for c in self.children:
            out.append(pad + f"▸ {c.tag}")
            out.extend(c.text(depth + 1).splitlines())
        return "\n".join(out)

    def all_lines(self):
        yield from self.lines
        for c in self.children:
            yield from c.all_lines()


def _convert(parser_block):
    lines, kids = [], []
    for l in parser_block.lines:
        if isinstance(l, str):
            lines.append(l)
        else:
            kids.append(_convert(l))
    return _Block(parser_block.tag, lines, kids)


class LogReadout(ReadoutAdapter):
    """
    **LLM Docstring**

    Readout for a McUtils log file (a path, a `LogParser`, or a `Logger` writing to a file).
    """
    readout_id = "log"

    def __init__(self, source):
        path = source
        if hasattr(source, "log_file"):
            path = source.log_file
        elif hasattr(source, "file") and not isinstance(source, str):
            path = getattr(source, "file")
        if not isinstance(path, (str, os.PathLike)):
            stream = getattr(source, "stream", None)
            path = getattr(stream, "_file", path)
        if not isinstance(path, (str, os.PathLike)) or not os.path.isfile(path):
            raise ValueError(f"log readouts need a log file on disk (got {source!r})")
        super().__init__(str(path))
        self._blocks = None

    @property
    def path(self):
        return self.obj

    def blocks(self):
        if self._blocks is None:
            from ..Logging import LogParser
            with LogParser(self.path) as p:
                self._blocks = [_convert(b) for b in p.get_blocks()]
        return self._blocks

    def get_readout_title(self):
        return f"Log: {os.path.basename(self.path)}"

    @readout_section("summary", title="Log")
    def readout_summary(self, ctx):
        """File, size and block statistics."""
        bl = self.blocks()
        tags = {}
        for b in bl:
            base = re.sub(r"\s*\d+$", "", b.tag)
            tags[base] = tags.get(base, 0) + 1
        nlines = sum(1 for b in bl for _ in b.all_lines())
        f = [Field("file", os.path.abspath(self.path), label="File", quantity="path"),
             Field("size", os.path.getsize(self.path), label="Size (bytes)", quantity="int"),
             Field("blocks", len(bl), label="Top-level blocks", quantity="int"),
             Field("lines", nlines, label="Logged lines", quantity="int"),
             Field("tags", ", ".join(f"{k} ×{v}" for k, v in tags.items()), label="Block tags")]
        return ReadoutFields(FieldSet(f, name="summary"))

    @readout_section("blocks", title="Blocks")
    def readout_blocks(self, ctx, max_rows=40):
        """One row per top-level block."""
        bl = self.blocks()
        if not bl:
            raise ReadoutSectionUnavailable("no blocks")
        rows = bl[:max_rows]
        cols = [Column("index", np.arange(1, len(rows) + 1), label="#", quantity="index"),
                Column("tag", np.array([b.tag for b in rows]), label="Tag"),
                Column("lines", np.array([len(list(b.all_lines())) for b in rows]), label="Lines"),
                Column("sub_blocks", np.array([len(b.children) for b in rows]), label="Sub-blocks"),
                Column("first_line", np.array([(b.lines[0].strip() if b.lines else "")[:70] for b in rows]),
                       label="First line")]
        nodes = [ReadoutTable(TabularData(cols, name="blocks"))]
        if len(bl) > max_rows:
            nodes.append(ReadoutText(f"{len(bl) - max_rows} more blocks not listed", role="note"))
        return nodes

    def series(self, min_blocks=3):
        """``{key: (block indices, values, unit)}`` for numeric values recurring across blocks."""
        found = {}
        for i, b in enumerate(self.blocks()):
            for l in b.all_lines():
                m = _KEY_VALUE.match(l)
                if m:
                    found.setdefault(m.group(1).strip(), {})[i] = (float(m.group(2)), m.group(3))
                for t in _TOOK.finditer(l):
                    v = float(t.group(1)) * (1e-3 if (t.group(2) or "").lower() == "ms" else 1)
                    found.setdefault("took (s)", {})[i] = (v, "s")
        out = {}
        for k, d in found.items():
            if len(d) >= min_blocks:
                idx = np.array(sorted(d))
                out[k] = (idx, np.array([d[i][0] for i in idx]), d[idx[0]][1])
        return out

    def _has_series(self):
        return bool(self.series()), "no recurring numeric values"

    @readout_section("values", title="Recurring values", available="_has_series")
    def readout_values(self, ctx, max_series=6):
        """Numeric ``key: value`` lines (and ``took …s`` timings) that recur across blocks."""
        nodes = []
        for k, (idx, vals, unit) in list(self.series().items())[:max_series]:
            slug = re.sub(r"\W+", "_", k).strip("_").lower()
            nodes.append(line_chart(idx + 1, vals, "Block", k + (f" ({unit})" if unit and unit != "s" else ""),
                                    names=[slug], markers=len(idx) < 60, x_name="block", id=slug,
                                    caption=f"{k} in {len(idx)} blocks"))
        return nodes

    @readout_section("contents", title="Block contents")
    def readout_contents(self, ctx, max_blocks=8, max_lines=40):
        """The first ``max_blocks`` blocks (nested blocks indented)."""
        bl = self.blocks()[:max_blocks]
        if not bl:
            raise ReadoutSectionUnavailable("no blocks")
        nodes = [ReadoutCode(b.text(), title=b.tag, id=f"block_{i + 1}", max_lines=max_lines) for i, b in enumerate(bl)]
        if len(self.blocks()) > max_blocks:
            nodes.append(ReadoutText(f"{len(self.blocks()) - max_blocks} more blocks not shown", role="note"))
        return nodes

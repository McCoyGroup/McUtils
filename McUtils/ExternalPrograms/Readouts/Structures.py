"""
Readout for XYZ records (single structures and multi-frame trajectories, as returned by
`McUtils.Parsers.XYZParser`): frame summary, the first (or selected) structure, numeric comment
lines (energies) as a series, and an animation over the frames.
"""

import os

import numpy as np

from ...Jupyter.Readouts import (
    ReadoutAdapter, readout_section, ReadoutSectionUnavailable, ReadoutFields, ReadoutTable, ReadoutArray,
    FieldSet, Field, ArrayData, Column, TabularData, structure_scene, trajectory_scene, atoms_table, line_chart,
)

__all__ = [
    "XYZReadout",
]


def _number(comment):
    try:
        return float(str(comment).split()[0])
    except (ValueError, IndexError):
        return None


class XYZReadout(ReadoutAdapter):
    """
    **LLM Docstring**

    Readout for XYZ frames ``[(comment, atoms, coords), ...]``. Coordinates are assumed to be in
    ``units`` (Å by default, the XYZ convention). If every comment line starts with a number it is
    treated as an energy (``comment_quantity='energy'``, ``comment_unit='Hartrees'`` by default).
    """
    readout_id = "xyz"

    def __init__(self, frames, source=None, units="Angstroms", comment_quantity="energy", comment_unit="Hartrees"):
        if isinstance(frames, tuple) and len(frames) == 3 and isinstance(frames[0], str):
            frames = [frames]
        super().__init__(list(frames))
        self.source = source
        self.units = units
        self.comment_quantity = comment_quantity
        self.comment_unit = comment_unit

    @classmethod
    def from_file(cls, file, max_blocks=None, **opts):
        from ...Parsers import XYZParser
        with XYZParser(file) as p:
            frames = p.parse(max_blocks=max_blocks)
        return cls(frames, source=file, **opts)

    @property
    def frames(self):
        return self.obj

    def comment_values(self):
        vals = [_number(c) for c, _, _ in self.frames]
        return None if any(v is None for v in vals) else np.asarray(vals)

    def get_readout_title(self):
        c, atoms, _ = self.frames[0]
        counts = {}
        for a in atoms:
            counts[a] = counts.get(a, 0) + 1
        formula = "".join(f"{k}{v if v > 1 else ''}" for k, v in counts.items())
        return formula + (f" — {len(self.frames)} frames" if len(self.frames) > 1 else "")

    def get_readout_subtitle(self):
        return os.path.basename(self.source) if self.source else None

    @readout_section("summary", title="Record")
    def readout_summary(self, ctx):
        """Frame count, atom count and comments."""
        c, atoms, _ = self.frames[0]
        f = []
        if self.source:
            f.append(ctx.field("file", os.path.abspath(self.source), label="File", quantity="path"))
        f += [Field("frames", len(self.frames), label="Frames", quantity="int"),
              Field("atoms", len(atoms), label="Atoms", quantity="int")]
        vals = self.comment_values()
        if vals is None:
            f.append(Field("comment", str(c).strip()[:300], label="Comment (frame 1)"))
        else:
            f.append(ctx.field("first_value", float(vals[0]), quantity=self.comment_quantity, unit=self.comment_unit,
                               label="Comment value (frame 1)"))
        return ReadoutFields(FieldSet(f, name="summary"))

    @readout_section("structure", title="Structure")
    def readout_structure(self, ctx, frame=0):
        """One frame (the first by default): 3D view and coordinates."""
        c, atoms, xyz = self.frames[frame]
        return [structure_scene(atoms, xyz, units=self.units, caption=f"frame {frame + 1}", id="view"),
                atoms_table(ctx, atoms, xyz, units=self.units, name="coordinates")]

    def _has_series(self):
        return len(self.frames) > 1 and self.comment_values() is not None, "comments are not numeric"

    @readout_section("series", title="Comment values", available="_has_series")
    def readout_series(self, ctx):
        """Numeric comment lines per frame (e.g. energies)."""
        vals = self.comment_values()
        rel, unit = ctx.convert(vals - np.nanmin(vals), self.comment_quantity, self.comment_unit)
        return line_chart(np.arange(1, len(vals) + 1), rel, "Frame", "Value − min", y_unit=unit, markers=True,
                          x_name="frame", id="plot", caption=f"{len(vals)} frames")

    def _has_frames(self):
        return len(self.frames) > 1, "single frame"

    @readout_section("trajectory", title="Frames", available="_has_frames")
    def readout_trajectory(self, ctx, max_frames=60):
        """An animation over the frames (subsampled to ``max_frames``); all coordinates are exported."""
        atoms = self.frames[0][1]
        same = all(list(a) == list(atoms) for _, a, _ in self.frames)
        if not same:
            raise ReadoutSectionUnavailable("frames have different atoms")
        coords = np.array([x for _, _, x in self.frames])
        cd, unit = ctx.convert(coords, "length", self.units)
        return [trajectory_scene(atoms, coords, units=self.units, max_frames=max_frames,
                                 caption=f"{len(coords)} frames", id="animation"),
                ReadoutArray(ArrayData("coordinates", cd, axes=("frame", "atom", "xyz"), unit=unit,
                                       quantity="length"), display=False)]

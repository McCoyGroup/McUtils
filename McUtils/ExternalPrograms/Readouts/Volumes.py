"""
Readout for volumetric (cube) data: grid summary, atoms, value statistics, isosurfaces over the
structure and three central slices. The full volume, grid origin/axes and atom positions are
exported; display only ever shows bounded views of it.
"""

import os

import numpy as np

from ...Jupyter.Readouts import (
    ReadoutAdapter, readout_section, ReadoutSectionUnavailable, ReadoutFields, ReadoutArray, ReadoutGallery,
    ReadoutPlot, FieldSet, Field, ArrayData, Column, TabularData, structure_scene, atoms_table,
)

__all__ = [
    "CubeReadout",
]


def _symbols(numbers):
    from ...Data import AtomData
    return [AtomData[int(z), "Symbol"] for z in numbers]


class CubeReadout(ReadoutAdapter):
    """
    **LLM Docstring**

    Readout for `CubeFileData` (from `CubeFileParser`) or a `CubePropEvaluator`. Cube files use
    Bohr; the grid ``axes`` are the voxel step vectors. Isovalues default to ±(fraction × max |value|).
    """
    readout_id = "cube"

    def __init__(self, data, source=None):
        super().__init__(data)
        self.source = source

    @classmethod
    def from_file(cls, file):
        from ..Parsers import CubeFileParser
        with CubeFileParser(file) as p:
            return cls(p.parse(), source=file)

    # ---- normalized views of either input ------------------------------------------------ #
    @property
    def grid(self):
        d = self.obj
        if hasattr(d, "grid"):
            return np.asarray(d.grid.origin, float), np.asarray(d.grid.axes, float), np.asarray(d.grid.steps, int)
        return np.asarray(d.origin, float), np.asarray(d.axes, float), np.asarray(d.steps, int)

    @property
    def values(self):
        d = self.obj
        origin, axes, steps = self.grid
        v = d.values if hasattr(d, "values") else d.values
        return np.asarray(v, dtype=float).reshape(tuple(steps))

    def atoms(self):
        d = self.obj
        a = getattr(d, "atoms", None)
        if a is None and getattr(d, "base_data", None) is not None:
            a = getattr(d.base_data, "atoms", None)
        if a is None:
            return None
        return _symbols(a.numbers), np.asarray(a.positions, dtype=float)

    def header(self):
        d = self.obj
        h = getattr(d, "header", None)
        if h is None and getattr(d, "base_data", None) is not None:
            h = d.base_data.header
        return h

    def get_readout_title(self):
        h = self.header()
        if h:
            lines = [l.strip() for l in str(h).splitlines() if l.strip()]
            for l in lines:
                if l.lower().startswith("property"):
                    return l.split(".")[0]
            return lines[0] if lines else "Cube volume"
        return "Cube volume"

    def get_readout_subtitle(self):
        return os.path.basename(self.source) if self.source else None

    def isovalues(self, isovalue=None, fraction=.25):
        v = self.values
        if isovalue is None:
            m = np.max(np.abs(v))
            iso = fraction * m
            return [iso, -iso] if v.min() < -1e-12 and v.max() > 1e-12 else [iso if v.max() > 0 else -iso]
        return list(np.atleast_1d(isovalue))

    # ---- sections ---------------------------------------------------------------------- #
    @readout_section("grid", title="Grid")
    def readout_grid(self, ctx):
        """Grid geometry and value statistics; the full volume is exported."""
        origin, axes, steps = self.grid
        v = self.values
        dv = abs(np.linalg.det(axes))
        lengths = np.linalg.norm(axes, axis=1) * (steps - 1)
        f = []
        if self.source:
            f.append(ctx.field("file", os.path.abspath(self.source), label="File", quantity="path"))
        h = self.header()
        if h:
            f.append(ctx.field("header", " / ".join(l.strip() for l in str(h).splitlines() if l.strip()), label="Header"))
        f += [ctx.field("points", " × ".join(str(int(s)) for s in steps), label="Grid points"),
              ctx.field("voxels", int(np.prod(steps)), label="Voxels", quantity="int"),
              ctx.field("spacing", " × ".join(f"{s:.4g}" for s in ctx.convert(np.linalg.norm(axes, axis=1), "length",
                                                                               "BohrRadius")[0]),
                        label=f"Spacing ({ctx.units.target_unit('length', 'BohrRadius')})"),
              ctx.field("extent", " × ".join(f"{s:.4g}" for s in ctx.convert(lengths, "length", "BohrRadius")[0]),
                        label=f"Extent ({ctx.units.target_unit('length', 'BohrRadius')})"),
              ctx.field("min", float(v.min()), label="Min value"),
              ctx.field("max", float(v.max()), label="Max value"),
              ctx.field("integral", float(v.sum() * dv), label="∑ value × dV (a₀³)"),
              ctx.field("integral_sq", float((v ** 2).sum() * dv), label="∑ value² × dV (a₀³)")]
        o, ou = ctx.convert(origin, "length", "BohrRadius")
        f.append(Field("origin", ", ".join(f"{x:.4f}" for x in o), label=f"Origin ({ou})"))
        return [ReadoutFields(FieldSet(f, name="grid")),
                ReadoutArray(ArrayData("values", v, axes=("i", "j", "k"), label="Values"), display=False),
                ReadoutArray(ArrayData("axes", axes, unit="BohrRadius", label="Voxel axes"), display=False),
                ReadoutArray(ArrayData("origin", origin, unit="BohrRadius", label="Origin"), display=False)]

    def _has_atoms(self):
        return self.atoms() is not None, "no atoms in the cube"

    @readout_section("atoms", title="Atoms", available="_has_atoms")
    def readout_atoms(self, ctx):
        """Atoms stored in the cube header (Bohr)."""
        atoms, pos = self.atoms()
        return atoms_table(ctx, atoms, pos, units="BohrRadius", name="atoms")

    @readout_section("isosurface", title="Isosurfaces")
    def readout_isosurface(self, ctx, isovalue=None, fraction=.25, colors=("#2F6DB5", "#C0392B"), opacity=.55):
        """Isosurfaces (positive and negative lobes) drawn over the molecule."""
        from ..CubeProp import CubePropEvaluator
        origin, axes, steps = self.grid
        ev = self.obj if isinstance(self.obj, CubePropEvaluator) else CubePropEvaluator(origin, axes, steps, self.values)
        surfaces = []
        for i, iso in enumerate(self.isovalues(isovalue, fraction)):
            try:
                surf = ev.get_isosurface(iso)
            except Exception:
                continue
            surfaces.append((iso, surf, colors[0] if iso >= 0 else colors[1]))
        if not surfaces:
            raise ReadoutSectionUnavailable("no isosurface at the requested values")

        def make_extra(surf, color):
            return lambda fig: surf.plot(figure=fig, color=color, transparency=1 - opacity)

        extras = [make_extra(s, c) for _, s, c in surfaces]
        at = self.atoms()
        atoms, pos = at if at is not None else ([], np.zeros((0, 3)))
        caption = "isovalues " + ", ".join(f"{iso:+.4g}" for iso, _, _ in surfaces)
        return structure_scene(atoms, pos, units="BohrRadius", extras=extras, caption=caption, id="view")

    @readout_section("slices", title="Slices")
    def readout_slices(self, ctx, cmap="RdBu_r"):
        """Central slices through the volume along each grid axis."""
        v = self.values
        origin, axes, steps = self.grid
        lim = float(np.max(np.abs(v))) or 1.0
        plots = []
        names = "ijk"
        for ax in range(3):
            idx = steps[ax] // 2
            sl = np.take(v, idx, axis=ax)
            others = [a for a in range(3) if a != ax]

            def build(sl=sl, others=others, ax=ax):
                from matplotlib.figure import Figure
                from matplotlib.backends.backend_agg import FigureCanvasAgg
                fig = Figure(figsize=(3.2, 2.8), dpi=100)
                FigureCanvasAgg(fig)
                a = fig.add_subplot(111)
                ext = [0, np.linalg.norm(axes[others[1]]) * (sl.shape[1] - 1),
                       0, np.linalg.norm(axes[others[0]]) * (sl.shape[0] - 1)]
                im = a.imshow(sl, origin="lower", cmap=cmap, vmin=-lim, vmax=lim, extent=ext, aspect="equal")
                a.set_xlabel(f"{names[others[1]]} (a₀)")
                a.set_ylabel(f"{names[others[0]]} (a₀)")
                fig.colorbar(im, ax=a, fraction=.046, pad=.04)
                fig.tight_layout()
                return fig

            plots.append(ReadoutPlot(build, caption=f"{names[ax]} = {idx} (central plane)", id=f"slice_{names[ax]}",
                                     data=ArrayData(f"slice_{names[ax]}", sl, axes=tuple(names[o] for o in others))))
        return ReadoutGallery(*plots, id="planes", per_slide=3, shared_view=False)

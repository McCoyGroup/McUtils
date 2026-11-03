"""
Builders used by readout adapters.

*Structures.* Structure helpers shared by readout adapters that only have atoms + coordinates (parsed logs,
XYZ/CIF records, conformers, toolkit wrappers): bond guessing, ball-and-stick scenes built from
`McUtils.Plots` primitives (mesh3D for PowerPoint/posters, X3D for HTML, one camera for both),
trajectory animations, and coordinate tables in the readout's display units.

*Charts.* Small chart builders used by readout adapters. Each returns a `ReadoutPlot` that draws with
`McUtils.Plots` (matplotlib backend) and carries the plotted values as `data`, so exports keep
the numbers rather than the picture.
"""

import math
import re

import numpy as np

from .Data import Column, TabularData, ArrayData
from .Nodes import ReadoutScene, ReadoutTable
from .Views import ReadoutPlot

__all__ = [
    "element_symbol",
    "guess_bonds",
    "structure_figure",
    "structure_scene",
    "trajectory_scene",
    "atoms_table",
    "cell_matrix",
    "to_angstroms",
    "line_chart",
    "stick_chart",
    "bar_chart",
    "matrix_chart",
]

# --------------------------------------------------------------------------------------------- #
#  structures
# --------------------------------------------------------------------------------------------- #
_SYM = re.compile(r"([A-Z][a-z]?)")


def element_symbol(label):
    """'Sr0' -> 'Sr', 'O2-' -> 'O', 'C12' -> 'C', 8 -> 'O'."""
    if isinstance(label, (int, np.integer)):
        from ..Data import AtomData
        return AtomData[int(label), "Symbol"]
    m = _SYM.match(str(label).strip())
    if m is None:
        return str(label)
    sym = m.group(1)
    from ..Data import AtomData
    try:
        AtomData[sym]
        return sym
    except Exception:
        return sym[0]


def _atom_data(sym):
    from ..Data import AtomData
    try:
        return AtomData[sym]
    except Exception:
        return AtomData["C"]


def to_angstroms(coords, units):
    coords = np.asarray(coords, dtype=float)
    if units in (None, "Angstroms", "Angstrom", "angstrom"):
        return coords
    from ..Data import UnitsData
    return coords * UnitsData.convert(units, "Angstroms")


def guess_bonds(atoms, coords, tolerance=1.15, units="Angstroms", max_atoms=2000):
    """Bonds ``[[i, j, 1.0], ...]`` between atoms closer than ``tolerance`` × (sum of covalent radii)."""
    syms = [element_symbol(a) for a in atoms]
    xyz = to_angstroms(coords, units)
    if len(xyz) > max_atoms:
        return []
    radii = np.array([_atom_data(s)["CovalentRadius"] for s in syms])
    d = np.linalg.norm(xyz[:, None] - xyz[None], axis=-1)
    cut = tolerance * (radii[:, None] + radii[None])
    i, j = np.where(np.triu((d < cut) & (d > 0.1), 1))
    return [[int(a), int(b), 1.0] for a, b in zip(i, j)]


def cell_matrix(a, b, c, alpha, beta, gamma):
    """Lattice vectors (rows, Å) from cell lengths (Å) and angles (degrees); a along x, b in the xy-plane."""
    al, be, ga = (math.radians(x) for x in (alpha, beta, gamma))
    ax = np.array([a, 0, 0])
    bx = np.array([b * math.cos(ga), b * math.sin(ga), 0])
    cx = c * math.cos(be)
    cy = c * (math.cos(al) - math.cos(be) * math.cos(ga)) / math.sin(ga)
    cz = math.sqrt(max(c ** 2 - cx ** 2 - cy ** 2, 0))
    return np.array([ax, bx, [cx, cy, cz]])


def structure_figure(atoms, coords, bonds=None, backend="mesh3D", units="Angstroms", radius_scale=.25,
                     bond_radius=.1, cell=None, cell_color="#5A6270", background="white", extras=(),
                     view_settings=None, sphere_points=32, highlight=None, mesh_resolution=None):
    """
    A ball-and-stick `Graphics3D` (``backend='mesh3D'`` or ``'x3d'``) in Å. ``cell`` (3×3 lattice
    rows, Å) adds unit-cell edges; ``extras`` are callables ``f(figure)`` that add more primitives
    (e.g. an isosurface). ``mesh_resolution`` sets the mesh3D tessellation (points around each
    sphere/cylinder; the backend default when ``None``).
    """
    from .. import Plots as plt
    xyz = to_angstroms(coords, units)
    syms = [element_symbol(a) for a in atoms]
    opts = dict(backend=backend, background=background)
    if view_settings is not None:
        opts["view_settings"] = view_settings
    fig = plt.Graphics3D(**opts)
    if bonds is None:
        bonds = guess_bonds(syms, xyz)
    datas = [_atom_data(s) for s in syms]
    cyl_opts, sph_opts = {}, {}
    if mesh_resolution is not None and "mesh3d" in str(backend).lower():
        cyl_opts = {"n_phi": int(mesh_resolution)}
        sph_opts = {"n_phi": int(mesh_resolution), "n_theta": max(4, int(mesh_resolution) // 2)}
    radii = []
    for d in datas:
        r = d["IconRadius"]
        radii.append((r if r >= .8 else d["VanDerWaalsRadius"]) * radius_scale)
    for (i, j, *_rest) in bonds:
        i, j = int(i), int(j)
        mid = (xyz[i] + xyz[j]) / 2
        if np.linalg.norm(xyz[i] - xyz[j]) < 1e-6:
            continue
        plt.Cylinder(xyz[i], mid, bond_radius, color=datas[i]["IconColor"], **cyl_opts).plot(fig)
        plt.Cylinder(mid, xyz[j], bond_radius, color=datas[j]["IconColor"], **cyl_opts).plot(fig)
    for k, (p, d, r) in enumerate(zip(xyz, datas, radii)):
        color = d["IconColor"] if highlight is None or k not in highlight else highlight[k]
        plt.Sphere(p, r, color=color, sphere_points=sphere_points, **sph_opts).plot(fig)
    if cell is not None:
        cell = np.asarray(cell, dtype=float)
        corners = np.array([i * cell[0] + j * cell[1] + k * cell[2]
                            for i in (0, 1) for j in (0, 1) for k in (0, 1)])
        for a in range(8):
            for b in range(a + 1, 8):
                if bin(a ^ b).count("1") == 1:
                    plt.Cylinder(corners[a], corners[b], bond_radius / 3, color=cell_color).plot(fig)
    for e in extras:
        e(fig)
    return fig


def structure_scene(atoms, coords, units="Angstroms", bonds=None, caption=None, id="structure", cell=None,
                    extras=(), **figure_opts):
    """A `ReadoutScene` for a structure: mesh3D model for PowerPoint/posters, X3D (same camera) for HTML."""
    atoms = list(atoms)
    coords = to_angstroms(coords, units)
    if bonds is None and cell is None:
        bonds = guess_bonds(atoms, coords)
    elif bonds is None:
        bonds = []
    model = lambda: structure_figure(atoms, coords, bonds, backend="mesh3D", cell=cell, extras=extras,
                                     **figure_opts)

    def html(view=None):
        vs = view.x3d_viewpoint() if view is not None else None
        return structure_figure(atoms, coords, bonds, backend="x3d", cell=cell, extras=extras,
                                view_settings=vs, **figure_opts).figure.to_x3d()

    return ReadoutScene(model=model, html=html, caption=caption, id=id, animated=False)


def trajectory_scene(atoms, frames, units="Angstroms", bonds=None, duration=None, caption=None, id="trajectory",
                     max_frames=60, frame_budget=1500, mesh_resolution=None, **figure_opts):
    """
    An animated `ReadoutScene` over coordinate frames ``(nframes, natoms, 3)``, subsampled to at
    most ``max_frames`` and to about ``frame_budget / (atoms + bonds)`` frames (animations store
    every vertex of every frame, so large molecules get fewer frames and, by default, coarser meshes). Bonds are
    guessed from the first frame unless given.
    """
    atoms = list(atoms)
    frames = to_angstroms(frames, units)
    if bonds is None:
        bonds = guess_bonds(atoms, frames[0])
    max_frames = min(max_frames, max(12, int(frame_budget / max(1, len(atoms) + len(bonds)))))
    if len(frames) > max_frames:
        frames = frames[np.linspace(0, len(frames) - 1, max_frames).round().astype(int)]
    if mesh_resolution is None:
        mesh_resolution = 20 if len(atoms) + len(bonds) <= 24 else 12
    figure_opts["mesh_resolution"] = mesh_resolution
    if duration is None:
        duration = max(2.0, len(frames) / 6)

    def model():
        figs = [structure_figure(atoms, f, bonds, backend="mesh3D", **figure_opts) for f in frames]
        meshes = [list(f.figure.iter_meshes()) for f in figs]
        return figs[0].figure.animate_frames(meshes, animation_duration=duration)

    return ReadoutScene(model=model, caption=caption, id=id, animated=True)


def atoms_table(ctx, atoms, coords, units="Angstroms", name="atoms", **extra_columns):
    """``#``, atom and x/y/z (converted to the readout's length unit), plus any extra columns."""
    coords = np.asarray(coords, dtype=float)
    cols = [Column("index", np.arange(1, len(atoms) + 1), label="#", quantity="index"),
            Column("atom", np.array([str(a) for a in atoms]), label="Atom")]
    for k, v in extra_columns.items():
        if isinstance(v, Column):
            cols.append(v)
        else:
            cols.append(Column(k, np.asarray(v), label=k.replace("_", " ")))
    for ax, k in enumerate("xyz"):
        cols.append(ctx.column(k, coords[:, ax], quantity="length", unit=units, label=k))
    return ReadoutTable(TabularData(cols, name=name))


# --------------------------------------------------------------------------------------------- #
#  charts
# --------------------------------------------------------------------------------------------- #
_SIZE = (460, 300)
_COLOR = "#1F4E79"


def _label(label, unit, theme_labels=None):
    if not unit:
        return label
    from .Styles import ReadoutTheme
    return f"{label} ({ReadoutTheme.default_tokens['unit_labels'].get(unit, unit)})"


def _columns(x, ys, x_name, x_label, x_unit, y_names, y_label, y_unit, x_quantity=None, y_quantity=None):
    cols = [Column(x_name, np.asarray(x), label=x_label, unit=x_unit, quantity=x_quantity)]
    for n, y in zip(y_names, ys):
        cols.append(Column(n, np.asarray(y), label=n if len(ys) > 1 else y_label, unit=y_unit, quantity=y_quantity))
    return TabularData(cols, name="series")


def line_chart(x, y, x_label="x", y_label="y", x_unit=None, y_unit=None, caption=None, names=None, markers=False,
               x_name="x", y_quantity=None, x_quantity=None, image_size=_SIZE, id=None, title=None, **plot_opts):
    """One or more series (``y`` may be a list of arrays) against ``x``."""
    ys = [np.asarray(y)] if np.asarray(y).ndim == 1 and not isinstance(y, (list, tuple)) else [np.asarray(v) for v in y]
    names = list(names) if names is not None else (["y"] if len(ys) == 1 else [f"y{i}" for i in range(len(ys))])
    data = _columns(x, ys, x_name, x_label, x_unit, names, y_label, y_unit, x_quantity, y_quantity)

    def build():
        from .. import Plots as plt
        palette = [_COLOR, "#C55A11", "#2E7D32", "#6A1B9A", "#00838F"]
        fig = None
        for i, v in enumerate(ys):
            opts = dict(color=palette[i % len(palette)], image_size=list(image_size),
                        axes_labels=[_label(x_label, x_unit), _label(y_label, y_unit)], **plot_opts)
            if len(ys) > 1:
                opts["label"] = str(names[i])
                if i == len(ys) - 1:
                    opts["plot_legend"] = True
            if fig is not None:
                opts["figure"] = fig
            if markers:
                fig = plt.Plot(x, v, marker="o", markersize=3, **opts)
            else:
                fig = plt.Plot(x, v, **opts)
        return fig

    return ReadoutPlot(build, caption=caption, data=data, id=id, title=title)


def stick_chart(x, y, x_label="x", y_label="y", x_unit=None, y_unit=None, caption=None, image_size=_SIZE, id=None,
                title=None, x_name="x", y_name="y", x_quantity=None, y_quantity=None):
    """A stick spectrum (e.g. frequencies vs. intensities)."""
    data = _columns(x, [y], x_name, x_label, x_unit, [y_name], y_label, y_unit, x_quantity, y_quantity)

    def build():
        from .. import Plots as plt
        return plt.StickPlot(np.asarray(x), np.asarray(y), color=_COLOR, image_size=list(image_size),
                             axes_labels=[_label(x_label, x_unit), _label(y_label, y_unit)])

    return ReadoutPlot(build, caption=caption, data=data, id=id, title=title)


def bar_chart(labels, values, y_label="value", y_unit=None, caption=None, image_size=_SIZE, horizontal=True, id=None,
              title=None, value_name="value"):
    """Labelled bars (horizontal by default, for long labels such as function names)."""
    labels = [str(l) for l in labels]
    values = np.asarray(values, dtype=float)
    data = TabularData([Column("label", np.array(labels), label="Label"),
                        Column(value_name, values, label=y_label, unit=y_unit)], name="series")

    def build():
        import matplotlib
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_agg import FigureCanvasAgg
        h = max(2.2, .28 * len(labels) + .8) if horizontal else image_size[1] / 100
        fig = Figure(figsize=(image_size[0] / 100 * 1.3, h), dpi=100)
        FigureCanvasAgg(fig)
        ax = fig.add_subplot(111)
        short = [l if len(l) <= 48 else "…" + l[-47:] for l in labels]
        if horizontal:
            ax.barh(range(len(values))[::-1], values, color=_COLOR)
            ax.set_yticks(range(len(values))[::-1], short, fontsize=8)
            ax.set_xlabel(_label(y_label, y_unit))
        else:
            ax.bar(range(len(values)), values, color=_COLOR)
            ax.set_xticks(range(len(values)), short, rotation=45, ha="right", fontsize=8)
            ax.set_ylabel(_label(y_label, y_unit))
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        fig.tight_layout()
        return fig

    return ReadoutPlot(build, caption=caption, data=data, id=id, title=title)


def matrix_chart(matrix, caption=None, label="value", unit=None, image_size=(360, 320), id=None, title=None,
                 cmap="RdBu_r", symmetric=True, name="matrix"):
    """A heatmap of a matrix; the full matrix is exported as `ArrayData`."""
    m = np.asarray(matrix, dtype=float)
    data = ArrayData(name, m, axes=("row", "column"), label=label, unit=unit)

    def build():
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_agg import FigureCanvasAgg
        fig = Figure(figsize=(image_size[0] / 100, image_size[1] / 100), dpi=100)
        FigureCanvasAgg(fig)
        ax = fig.add_subplot(111)
        lim = np.nanmax(np.abs(m)) if symmetric and m.size else None
        im = ax.imshow(m, cmap=cmap, vmin=-lim if lim else None, vmax=lim)
        fig.colorbar(im, ax=ax, fraction=.046, pad=.04).set_label(_label(label, unit))
        ax.set_xlabel("column")
        ax.set_ylabel("row")
        fig.tight_layout()
        return fig

    return ReadoutPlot(build, caption=caption, data=data, id=id, title=title)

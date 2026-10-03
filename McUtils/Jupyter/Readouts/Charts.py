"""
Small chart builders used by readout adapters. Each returns a `ReadoutPlot` that draws with
`McUtils.Plots` (matplotlib backend) and carries the plotted values as `data`, so exports keep
the numbers rather than the picture.
"""

import numpy as np

from .Data import Column, TabularData, ArrayData
from .Views import ReadoutPlot

__all__ = [
    "line_chart",
    "stick_chart",
    "bar_chart",
    "matrix_chart",
]

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
        from ... import Plots as plt
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
        from ... import Plots as plt
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

"""
Readouts for displayable objects: McUtils `Graphics`/`GraphicsGrid` (matplotlib, x3d and mesh3D
backends), `X3D` scenes, `Mesh3DAnimation`s and PowerPoint primitives. A view readout is the view
itself (rendered for HTML and PowerPoint by the readout renderers) plus an optional description of
the figure (backend, size, ranges, labels). Any of these can also be dropped straight into another
readout with `ReadoutSection.compose(...)`.
"""

import numpy as np

from ...Jupyter.Readouts import (
    ReadoutAdapter, readout_section, ReadoutSectionUnavailable, ReadoutFields, FieldSet, Field,
    as_readout_node,
)

__all__ = [
    "ViewReadout",
]


def _safe(f):
    try:
        return f()
    except Exception:
        return None


class ViewReadout(ReadoutAdapter):
    """
    **LLM Docstring**

    Readout for one displayable object. ``caption`` labels the view; ``details=True`` (or
    ``include=['view', 'details']``) adds the figure description.
    """
    readout_id = "view"

    def __init__(self, view, caption=None, title=None):
        super().__init__(view)
        self.caption = caption
        self.title = title

    def get_readout_title(self):
        if self.title is not None:
            return self.title
        label = _safe(lambda: self.obj.plot_label)
        return str(label) if label else type(self.obj).__name__

    @readout_section("view", title="View")
    def readout_view(self, ctx):
        """The view (plot, scene, animation, primitive)."""
        return as_readout_node(self.obj, caption=self.caption, dispatch=False, id="view")

    @readout_section("details", title="Details", default=False)
    def readout_details(self, ctx):
        """Type, backend, image size, ranges and labels (whatever the object reports)."""
        o = self.obj
        f = [Field("type", f"{type(o).__module__.rsplit('.', 1)[-1]}.{type(o).__name__}", label="Type")]
        for name, label, get in [
            ("backend", "Backend", lambda: o.backend if isinstance(o.backend, str) else type(o.backend).__name__),
            ("image_size", "Image size", lambda: "×".join(str(int(v)) for v in np.ravel(o.image_size))),
            ("plot_range", "Plot range", lambda: str(np.round(np.asarray(o.plot_range, dtype=float), 4).tolist())),
            ("axes_labels", "Axes labels", lambda: ", ".join(str(a) for a in o.axes_labels if a is not None)),
            ("children", "Child graphics", lambda: len(o.children)),
            ("frames", "Frames", lambda: len(o.frames)),
            ("shape", "Grid", lambda: "×".join(map(str, o.shape))),
        ]:
            v = _safe(get)
            if v not in (None, "", "None"):
                f.append(Field(name, v, label=label))
        return ReadoutFields(FieldSet(f, name="details"))

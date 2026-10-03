"""
The readout tree: a backend-neutral description of a set of results.

Nodes hold payloads (`Data` objects, lazy scene factories, text) plus semantic hints
(`role`, `style`). Renderers in `Renderers/` turn the same tree into HTML, PowerPoint,
plain text or exported data. Like the X3D/PresentationML primitives, any node may provide a
per-backend hook (``to_html``, ``to_presml``, ``to_text``) that overrides the renderer's
default handler.
"""

import os
import re

from .Data import Field, FieldSet, TabularData, ArrayData

__all__ = [
    "ReadoutNode",
    "ReadoutSection",
    "ReadoutText",
    "ReadoutFields",
    "ReadoutTable",
    "ReadoutArray",
    "ReadoutImage",
    "ReadoutScene",
    "ReadoutGallery",
    "Readout",
]


def _slug(text):
    text = re.sub(r"[^0-9a-zA-Z]+", "_", str(text)).strip("_").lower()
    return text or "node"


class ReadoutNode:
    kind = "node"
    _counter = 0

    def __init__(self, *children, id=None, title=None, role=None, style=None, meta=None, description=None):
        if len(children) == 1 and isinstance(children[0], (list, tuple)):
            children = children[0]
        self.children = [c for c in children if c is not None]
        if id is None:
            if title is not None:
                id = _slug(title)
            else:
                type(self)._counter += 1
                id = f"{self.kind}_{type(self)._counter}"
        self.id = id
        self.title = title
        self.role = role
        self.style = dict(style or {})
        self.meta = dict(meta or {})
        self.description = description

    def get_children(self):
        return self.children

    def walk(self, path=()):
        """Yield ``(path, node)`` pairs depth-first; paths are tuples of node ids."""
        path = path + (self.id,)
        yield path, self
        for c in self.get_children():
            yield from c.walk(path)

    def find(self, path):
        if isinstance(path, str):
            path = [p for p in path.split("/") if p]
        node = self
        for p in path:
            for c in node.get_children():
                if c.id == p:
                    node = c
                    break
            else:
                raise KeyError(f"no child {p!r} under {node.id!r} (have {[c.id for c in node.get_children()]})")
        return node

    def __getitem__(self, path):
        return self.find(path)

    def __repr__(self):
        return f"{type(self).__name__}(id={self.id!r}, title={self.title!r}, children={len(self.children)})"


class ReadoutSection(ReadoutNode):
    kind = "section"


class ReadoutText(ReadoutNode):
    kind = "text"

    def __init__(self, text, **opts):
        super().__init__(**opts)
        self.text = text


class ReadoutFields(ReadoutNode):
    kind = "fields"

    def __init__(self, fields, **opts):
        if not isinstance(fields, FieldSet):
            fields = FieldSet(fields)
        opts.setdefault("title", fields.title)
        if opts.get("id") is None and fields.name is not None:
            opts["id"] = fields.name
        super().__init__(**opts)
        self.data = fields


class ReadoutTable(ReadoutNode):
    kind = "table"

    def __init__(self, data, **opts):
        if not isinstance(data, TabularData):
            data = TabularData(data)
        opts.setdefault("title", data.title)
        if opts.get("id") is None and data.name is not None:
            opts["id"] = data.name
        super().__init__(**opts)
        self.data = data


class ReadoutArray(ReadoutNode):
    """Array data that is exported but (by default) not displayed."""
    kind = "array"

    def __init__(self, data, display=False, **opts):
        if not isinstance(data, ArrayData):
            raise TypeError("ReadoutArray needs an ArrayData")
        opts.setdefault("id", data.name)
        super().__init__(**opts)
        self.data = data
        self.display = display


class ReadoutImage(ReadoutNode):
    """A static image (PNG/SVG bytes, a file path, or a factory returning either)."""
    kind = "image"

    def __init__(self, image, content_type=None, caption=None, **opts):
        super().__init__(**opts)
        self._image = image
        self.content_type = content_type
        self.caption = caption

    def get_image(self):
        img = self._image() if callable(self._image) else self._image
        if isinstance(img, (str, os.PathLike)):
            with open(img, "rb") as f:
                data = f.read()
            ctype = self.content_type or ("image/svg+xml" if str(img).endswith(".svg") else "image/png")
            return data, ctype
        return img, self.content_type or "image/png"


class ReadoutScene(ReadoutNode):
    """
    A 3D scene, possibly animated.

    :param model: a mesh source (a `Mesh3DAnimation`, a mesh3D `Graphics3D`/`Mesh3DFigure`)
        or a zero-argument factory returning one. Used for PowerPoint (`.glb`), posters and,
        unless `html` is given, for the HTML/X3D view.
    :param html: optional X3D object (or factory, optionally taking ``view=``) to use for HTML
        instead of the mesh source
    :param caption: a string or `Field` (formatted with the theme at render time)
    :param view: an explicit `SceneView`; galleries with `shared_view=True` fill this in
    """
    kind = "scene"

    def __init__(self, model=None, html=None, caption=None, view=None, animated=None, **opts):
        super().__init__(**opts)
        self._model = model
        self._html = html
        self.caption = caption
        self.view = view
        self._animated = animated
        self._source = None

    def get_source(self):
        if self._source is None:
            if self._model is None:
                return None
            from .Scenes import MeshSceneSource
            model = self._model
            if callable(model) and not any(hasattr(model, a) for a in ("frames", "figure", "iter_meshes")):
                model = model()
            self._source = MeshSceneSource(model)
        return self._source

    def get_html(self, view=None):
        """The X3D object for HTML; a factory may take a ``view`` (a `SceneView`) argument."""
        if self._html is None:
            return None
        if callable(self._html) and not hasattr(self._html, "to_x3d"):
            import inspect
            try:
                takes_view = "view" in inspect.signature(self._html).parameters
            except (TypeError, ValueError):
                takes_view = False
            self._html = self._html(view=view) if takes_view else self._html()
        return self._html

    @property
    def animated(self):
        if self._animated is not None:
            return self._animated
        src = self.get_source()
        return src is not None and src.animated

    def format_caption(self, theme=None):
        cap = self.caption
        if cap is None:
            return None
        if isinstance(cap, Field):
            return cap.label + ": " + cap.format(theme) if cap.label else cap.format(theme)
        return str(cap)


class ReadoutGallery(ReadoutNode):
    """
    A set of items (usually scenes) shown together: a grid in HTML, tiled ``per_slide`` at a
    time in PowerPoint. ``shared_view=True`` fits a single camera to every item so all items
    are drawn at the same scale.
    """
    kind = "gallery"

    def __init__(self, *items, shared_view=True, per_slide=None, columns=None, **opts):
        super().__init__(*items, **opts)
        self.shared_view = shared_view
        self.per_slide = per_slide
        self.columns = columns


class Readout(ReadoutSection):
    """
    The root of a readout. Display it in Jupyter, or export it with `to_html`, `to_pptx`,
    `to_npz`, `to_pandas`, `to_json` and `to_text`; all exports read the same values in the
    same (display) units.
    """
    kind = "readout"

    def __init__(self, *children, title=None, subtitle=None, units=None, id=None, **opts):
        super().__init__(*children, title=title, id=id or "readout", **opts)
        self.subtitle = subtitle
        self.units = units

    # ---- text --------------------------------------------------------------------------- #
    def to_text(self, style=None):
        from .Renderers.Text import TextReadoutRenderer
        return TextReadoutRenderer(style).render_readout(self)

    def __str__(self):
        return self.to_text()

    # ---- HTML / Jupyter ----------------------------------------------------------------- #
    def to_html_element(self, mode="static", style=None, **opts):
        from .Renderers.HTML import HTMLReadoutRenderer
        return HTMLReadoutRenderer(style, mode=mode, **opts).render_readout(self)

    def to_html(self, file=None, style=None, x3dom_path=None, **opts):
        """Standalone HTML document (string), optionally written to ``file``."""
        from .Renderers.HTML import HTMLReadoutRenderer
        html = HTMLReadoutRenderer(style, mode="static", x3dom_path=x3dom_path, **opts).render_document(self)
        if file is not None:
            with open(file, "w", encoding="utf-8") as f:
                f.write(html)
            return file
        return html

    def to_widget(self, style=None, **opts):
        return self.to_html_element(mode="widget", style=style, **opts)

    def _repr_html_(self):
        return self.to_widget().tostring()

    def get_mime_bundle(self):
        return self.to_widget().get_mime_bundle()

    def _ipython_display_(self):
        return self.to_widget()._ipython_display_()

    # ---- PowerPoint --------------------------------------------------------------------- #
    def to_powerpoint(self, style=None, rasterizer=None, rasterizer_options=None, **opts):
        """Build (but don't write) a mutable `PowerPointPresentation`."""
        from .Renderers.PowerPoint import PowerPointReadoutRenderer
        return PowerPointReadoutRenderer(style, rasterizer=rasterizer,
                                         rasterizer_options=rasterizer_options, **opts).render_readout(self)

    def to_pptx(self, file=None, style=None, rasterizer=None, rasterizer_options=None, validate=True, **opts):
        pres = self.to_powerpoint(style=style, rasterizer=rasterizer, rasterizer_options=rasterizer_options, **opts)
        if file is None:
            return pres.to_bytes(validate=validate)
        pres.write(file, validate=validate)
        return file

    # ---- data --------------------------------------------------------------------------- #
    def to_data(self):
        """``(values, meta)``: nested dicts of arrays/scalars and per-path unit metadata."""
        from .Renderers.Data import DataReadoutRenderer
        return DataReadoutRenderer().render_readout(self)

    def to_flat_data(self, sep="/"):
        from .Renderers.Data import DataReadoutRenderer
        return DataReadoutRenderer().flatten(self, sep=sep)

    def to_npz(self, file):
        from .Renderers.Data import DataReadoutRenderer
        return DataReadoutRenderer().write_npz(self, file)

    def to_pandas(self):
        from .Renderers.Data import DataReadoutRenderer
        return DataReadoutRenderer().to_pandas(self)

    def to_json(self, file=None, indent=2):
        from .Renderers.Data import DataReadoutRenderer
        return DataReadoutRenderer().write_json(self, file, indent=indent)

    def export_assets(self, directory, skinned=True):
        """Write every scene's `.glb` into ``directory``; returns ``{path: file}``."""
        from .Renderers.Data import DataReadoutRenderer
        return DataReadoutRenderer().export_assets(self, directory, skinned=skinned)

    def save(self, file, **opts):
        ext = str(file).rsplit(".", 1)[-1].lower()
        dispatch = {"html": self.to_html, "htm": self.to_html, "pptx": self.to_pptx,
                    "npz": self.to_npz, "json": self.to_json}
        if ext == "txt":
            with open(file, "w", encoding="utf-8") as f:
                f.write(self.to_text(**opts))
            return file
        if ext not in dispatch:
            raise ValueError(f"don't know how to save a readout as .{ext}")
        return dispatch[ext](file, **opts)

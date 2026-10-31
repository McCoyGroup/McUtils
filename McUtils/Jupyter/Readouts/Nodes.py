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
    "ReadoutGrid",
    "ReadoutFlex",
    "ReadoutPanel",
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

    def to_widget(self, style=None, **opts):
        from .Renderers.HTML import HTMLReadoutRenderer
        return HTMLReadoutRenderer(style, mode='widget', **opts).render_fragment(self)

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

    def __init__(self, *children, **opts):
        from .Views import as_readout_node
        if len(children) == 1 and isinstance(children[0], (list, tuple)):
            children = children[0]
        super().__init__(*[as_readout_node(child) for child in children if child is not None], **opts)

    @classmethod
    def compose(cls, *items, **opts):
        """
        Build a section (or a `Readout`) from arbitrary objects: plots, scenes, X3D objects, TeX,
        JHTML elements, PowerPoint primitives, tables, other readouts, ... (see `as_readout_node`).
        """
        from .Views import as_readout_node
        return cls(*[as_readout_node(i) for i in items if i is not None], **opts)


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

    def __init__(self, image, content_type=None, caption=None, fallback=None, **opts):
        super().__init__(**opts)
        self._image = image
        self.content_type = content_type
        self.caption = caption
        self.fallback = fallback  # PNG bytes used where the image format isn't supported (SVG in PowerPoint)

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


def _app_ui_theme(ui_theme):
    from ..Apps.Themes import AppTheme
    return AppTheme(ui_theme).name if ui_theme is not None else AppTheme.selected()


class ReadoutGrid(ReadoutSection):
    """A semantic grid, using Apps' CSS Grid sizing and placement conventions.

    ``rows`` is a list of rows; a cell may be any readout/widget object, None,
    or an existing ``Grid.Item`` carrying explicit placement and spans.
    """
    kind = 'grid'

    def __init__(self, rows, column_width='1fr', row_height='auto', row_spacing=None,
                 col_spacing=None, alignment=None, justification=None, ui_theme=None,
                 style=None, collapse_below=None, html_attrs=None, **opts):
        from .Views import as_readout_node
        from ..Apps import Grid
        cells = []
        nrows = ncols = 0
        for i, row in enumerate(rows, 1):
            for j, value in enumerate(row, 1):
                if value is None:
                    continue
                if isinstance(value, Grid.Item):
                    placement = dict(row=i if value.row is None else value.row,
                                     col=j if value.col is None else value.col,
                                     row_span=value.row_span, col_span=value.col_span,
                                     alignment=value.alignment, justification=value.justification)
                    attrs = dict(value.attrs)
                    value = value.item
                else:
                    placement = dict(row=i, col=j)
                    attrs = {}
                for key in ('row','col','row_span','col_span'):
                    count = placement.get(key)
                    if count is not None and (isinstance(count,bool) or int(count) != count or count < 1):
                        raise ValueError('Grid positions and spans must be positive integers')
                nrows = max(nrows, placement['row']+(placement.get('row_span') or 1)-1)
                ncols = max(ncols, placement['col']+(placement.get('col_span') or 1)-1)
                cells.append((as_readout_node(value), placement, attrs))
        super().__init__(*[cell[0] for cell in cells], style=style, **opts)
        self.cells = cells
        self.grid_options = dict(rows=nrows,cols=ncols,row_height=row_height,col_width=column_width,
                                 row_gap=row_spacing,col_gap=col_spacing,
                                 alignment=alignment,justification=justification)
        self.ui_theme = _app_ui_theme(ui_theme)
        self.collapse_below = collapse_below
        self.html_attrs = dict(html_attrs or {})

    @classmethod
    def from_layout(cls, layout, **opts):
        from ..Apps import AppTheme
        opts.setdefault('ui_theme',layout.ui_theme or AppTheme.selected())
        opts.setdefault('style',layout._style)
        opts.setdefault('html_attrs',layout.attrs)
        opts.setdefault('collapse_below',getattr(layout,'collapse_below',None))
        # Explicit GridItems carry their original positions; a single storage
        # row does not change their layout or semantic reading order.
        return cls([layout.elements], column_width=layout.col_width,row_height=layout.row_height,
                   row_spacing=layout.row_gaps,col_spacing=layout.col_gaps,
                   alignment=layout.alignment,justification=layout.justification,**opts)


class ReadoutFlex(ReadoutSection):
    """A semantic flex layout retaining Apps item order/grow/shrink/basis."""
    kind = 'flex'

    def __init__(self, *items, direction='row', wrap=None, gap=None, alignment=None,
                 justification=None, content_alignment=None, ui_theme=None, html_attrs=None, **opts):
        from ..Apps import Flex
        from .Views import as_readout_node
        cells=[]
        for item in items:
            if isinstance(item,Flex.Item):
                placement={key:getattr(item,key) for key in ('order','grow','shrink','basis','alignment')}
                attrs=dict(item.attrs);item=item.item
            else:placement={};attrs={}
            if item is not None:cells.append((as_readout_node(item),placement,attrs))
        super().__init__(*[cell[0] for cell in cells],**opts)
        if isinstance(wrap,bool):wrap='wrap' if wrap else 'nowrap'
        self.flex_options=dict(direction=direction,wrap=wrap,alignment=alignment,
                               justification=justification,content_alignment=content_alignment)
        self.ui_theme=_app_ui_theme(ui_theme);self.gap=gap;self.cells=cells
        self.html_attrs = dict(html_attrs or {})

    @classmethod
    def from_layout(cls, layout, **opts):
        from ..Apps import AppTheme
        opts.setdefault('ui_theme',layout.ui_theme or AppTheme.selected())
        opts.setdefault('style',layout._style)
        opts.setdefault('html_attrs',layout.attrs)
        return cls(*layout.elements,direction=layout.direction,wrap=layout.wrap,
                   gap=layout._style.get('gap'),alignment=layout.alignment,
                   justification=layout.justification,content_alignment=layout.content_alignment,**opts)


class ReadoutPanel(ReadoutSection):
    """A panel with independent header/body/footer flow, retaining node data."""
    kind = 'panel'

    def __init__(self, *body, header=None, footer=None, ui_theme=None, html_attrs=None, **opts):
        from .Views import as_readout_node
        def part(value, name):
            if value is None:return None
            if isinstance(value,(list,tuple)):return ReadoutSection.compose(*value,id=name)
            return as_readout_node(value)
        self.header,self.footer = part(header,'header'),part(footer,'footer')
        self.body = [as_readout_node(item) for item in body if item is not None]
        super().__init__(self.header,*self.body,self.footer,**opts)
        self.ui_theme = _app_ui_theme(ui_theme)
        self.html_attrs = dict(html_attrs or {})


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

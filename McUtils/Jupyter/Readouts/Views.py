"""
View leaves: existing McUtils display objects (plots, equations, HTML components, PowerPoint
primitives, source text) embedded in a readout.

Each view keeps the object that produced it and, optionally, the semantic data behind it
(``data=``), which is what the data exports use; the rendered picture is never the source of
the numbers. `as_readout_node` turns arbitrary displayable objects into the right leaf, so
adapters (and users) can compose readouts from things they already have.
"""

import io
import re
import uuid

import numpy as np

from .Data import Field, FieldSet, TabularData, ArrayData, Column
from .Nodes import (ReadoutNode, ReadoutSection, ReadoutText, ReadoutFields, ReadoutTable, ReadoutArray,
                    ReadoutImage, ReadoutScene, ReadoutGallery, Readout)

__all__ = [
    "ReadoutPlot",
    "ReadoutEquation",
    "ReadoutCode",
    "ReadoutHTML",
    "ReadoutPresML",
    "as_readout_node",
]


def _png_size(data):
    """(width, height) of PNG bytes, read from the IHDR chunk."""
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")


def _strip_svg_prolog(svg):
    if isinstance(svg, bytes):
        svg = svg.decode("utf-8")
    i = svg.find("<svg")
    return svg[i:] if i >= 0 else svg


def _resolve(obj):
    if callable(obj) and not any(hasattr(obj, a) for a in ("savefig", "figure", "format_tex", "tostring",
                                                           "to_presml", "to_jhtml")):
        return obj()
    return obj


class ReadoutPlot(ReadoutNode):
    """
    A 2D (or matplotlib 3D) figure: a McUtils `Graphics`/`GraphicsGrid`, a matplotlib `Figure`, or a
    zero-argument factory returning one. HTML embeds it as inline SVG (or PNG), PowerPoint as a
    picture. ``data`` (a `TabularData`, `ArrayData`, `FieldSet` or dict of arrays) is what gets
    exported; the figure itself is never mined for values.
    """
    kind = "plot"

    def __init__(self, graphics, caption=None, data=None, dpi=150, **opts):
        super().__init__(**opts)
        self._graphics = graphics
        self.caption = caption
        if isinstance(data, dict):
            data = TabularData(data) if len({len(np.atleast_1d(v)) for v in data.values()}) == 1 \
                else FieldSet(data)
        self.data = data
        self.dpi = dpi
        self._cache = {}

    def get_graphics(self):
        self._graphics = _resolve(self._graphics)
        return self._graphics

    def _render(self, fmt):
        if fmt in self._cache:
            return self._cache[fmt]
        g = self.get_graphics()
        buf = io.BytesIO()
        if hasattr(g, "savefig") and hasattr(g, "figure") and not hasattr(g, "canvas"):
            if fmt == "svg":
                import matplotlib
                with matplotlib.rc_context({"svg.hashsalt": uuid.uuid4().hex}):  # unique ids per inline svg
                    g.savefig(buf, format="svg", bbox_inches="tight")
            else:
                g.savefig(buf, format=fmt, bbox_inches="tight", dpi=self.dpi)
        elif hasattr(g, "savefig"):  # a matplotlib Figure
            import matplotlib
            with matplotlib.rc_context({"svg.hashsalt": uuid.uuid4().hex}):
                g.savefig(buf, format=fmt, dpi=self.dpi, bbox_inches="tight")
        else:
            raise TypeError(f"don't know how to render {type(g).__name__} as {fmt}")
        self._cache[fmt] = buf.getvalue()
        return self._cache[fmt]

    def to_png(self):
        return self._render("png")

    def to_svg(self):
        return _strip_svg_prolog(self._render("svg"))

    def aspect(self):
        size = _png_size(self.to_png())
        return size[0] / size[1] if size else 4 / 3


class ReadoutEquation(ReadoutNode):
    """
    An equation: a LaTeX string or a McUtils `TeX` object. Rendered offline with matplotlib
    mathtext (SVG in HTML, PNG in PowerPoint); the LaTeX source travels with it.
    """
    kind = "equation"

    def __init__(self, tex, label=None, fontsize=16, **opts):
        super().__init__(**opts)
        self.tex = tex
        self.label = label
        self.fontsize = fontsize
        self._cache = {}

    def latex(self):
        tex = self.tex.format_tex() if hasattr(self.tex, "format_tex") else str(self.tex)
        tex = re.sub(r"\\(begin|end)\{(equation|align)\*?\}", "", tex)
        tex = re.sub(r"\\label\{[^}]*\}", "", tex).strip()
        if tex.startswith("$$") and tex.endswith("$$"):
            tex = tex[2:-2]
        elif tex.startswith("$") and tex.endswith("$"):
            tex = tex[1:-1]
        return tex.strip()

    def _render(self, fmt, dpi=200, color="black"):
        key = (fmt, dpi, color)
        if key not in self._cache:
            from matplotlib.figure import Figure
            from matplotlib.backends.backend_agg import FigureCanvasAgg
            import matplotlib
            fig = Figure(figsize=(0.01, 0.01))
            FigureCanvasAgg(fig)
            fig.text(0, 0, "$" + self.latex() + "$", fontsize=self.fontsize, color=color)
            buf = io.BytesIO()
            with matplotlib.rc_context({"svg.hashsalt": uuid.uuid4().hex, "svg.fonttype": "path"}):
                fig.savefig(buf, format=fmt, dpi=dpi, transparent=True, bbox_inches="tight", pad_inches=0.04)
            self._cache[key] = buf.getvalue()
        return self._cache[key]

    def to_svg(self, color="black"):
        return _strip_svg_prolog(self._render("svg", color=color))

    def to_png(self, dpi=200, color="black"):
        return self._render("png", dpi=dpi, color=color)


class ReadoutCode(ReadoutNode):
    """Preformatted source (job inputs, logs, profiler output); long text is truncated for display."""
    kind = "code"

    def __init__(self, text, language=None, max_lines=None, **opts):
        super().__init__(**opts)
        self.text = str(text)
        self.language = language
        self.max_lines = max_lines

    def display_text(self, max_lines=None):
        max_lines = max_lines or self.max_lines
        lines = self.text.splitlines()
        if max_lines is not None and len(lines) > max_lines:
            return "\n".join(lines[:max_lines] + [f"… ({len(lines) - max_lines} more lines)"])
        return self.text


class ReadoutHTML(ReadoutNode):
    """
    An HTML view: a JHTML element, an Apps component (``to_jhtml``), anything with ``tostring`` or
    a raw HTML string. ``head`` lists extra `<head>` elements it needs (scripts/stylesheets) in
    standalone pages. In PowerPoint the ``fallback`` node is used instead; without one, static
    elements contribute their visible text and scripted ones a short note.
    """
    kind = "html"

    def __init__(self, element, fallback=None, head=(), **opts):
        super().__init__(**opts)
        self.element = element
        self.fallback = fallback
        self.head = tuple(head)

    def get_element(self):
        el = _resolve(self.element)
        if hasattr(el, "to_jhtml") and not hasattr(el, "tostring"):
            el = el.to_jhtml()
        return el

    def text_content(self, max_chars=2000):
        """Visible text of a static element (``None`` if it carries scripts or can't be serialized)."""
        import html as _html
        import re as _re
        try:
            el = self.get_element()
            src = el if isinstance(el, str) else el.tostring()
        except Exception:
            return None
        if _re.search(r"<(script|canvas|iframe|x3d)\b", src, _re.I):
            return None
        src = _re.sub(r"<(style)\b.*?</\1>", " ", src, flags=_re.I | _re.S)
        src = _re.sub(r"</(p|div|h[1-6]|li|tr|br)\s*>|<br\s*/?>", "\n", src, flags=_re.I)
        text = _html.unescape(_re.sub(r"<[^>]+>", " ", src))
        lines = [" ".join(l.split()) for l in text.splitlines()]
        text = "\n".join(l for l in lines if l).strip()
        return text[:max_chars] or None


class ReadoutPresML(ReadoutNode):
    """
    A PowerPoint primitive (`PresentationMLText/Image/Shape/Table/Model3D` or raw OpenXML) placed
    into the readout's layout box. HTML shows ``fallback`` (or, for images/text/tables, an
    equivalent derived from the primitive).
    """
    kind = "presml"

    def __init__(self, primitive, fallback=None, size=None, **opts):
        super().__init__(**opts)
        self.primitive = primitive
        self.fallback = fallback
        self.size = size

    def get_fallback(self):
        if self.fallback is not None:
            return self.fallback
        p = self.primitive
        name = type(p).__name__
        if name == "PresentationMLText":
            return ReadoutText(p.text)
        if name == "PresentationMLTable" and p.rows:
            rows = [[c.get("text") if isinstance(c, dict) else c for c in r] for r in p.rows]
            head, body = rows[0], rows[1:]
            cols = [Column(f"c{j}", np.array([str(r[j]) if j < len(r) else "" for r in body]),
                           label=str(head[j])) for j in range(len(head))]
            return ReadoutTable(TabularData(cols))
        if name == "PresentationMLImage" and getattr(p, "image", None) is not None:
            return ReadoutImage(p.image.data, content_type=p.image.content_type)
        if name == "PresentationMLModel3D" and getattr(p, "fallback", None) is not None:
            return ReadoutImage(p.fallback.data, content_type=p.fallback.content_type)
        return ReadoutText(f"[{name}: PowerPoint only]", role="note")


def _is_graphics(obj):
    return hasattr(obj, "savefig") and hasattr(obj, "figure") and hasattr(obj, "backend") \
        if not isinstance(obj, type) else False


def as_readout_node(obj, caption=None, dispatch=True, **opts):
    """
    Turn a displayable or data object into a readout node:

    * readout nodes pass through; a `Readout` becomes a section; objects with ``to_readout``
      contribute their readout as a section
    * McUtils `Graphics`: matplotlib/SVG backends -> `ReadoutPlot`; ``x3d`` -> `ReadoutScene`
      (HTML); ``mesh3D`` -> `ReadoutScene` (HTML + PowerPoint)
    * `X3D` objects -> `ReadoutScene`; `Mesh3DAnimation` -> animated `ReadoutScene`
    * TeX expressions/equations -> `ReadoutEquation`; other TeX writers -> LaTeX `ReadoutCode`
    * JHTML elements / Apps components -> `ReadoutHTML`; PowerPoint primitives -> `ReadoutPresML`
    * `TabularData`/`FieldSet`/`ArrayData`, pandas DataFrames, dicts, arrays, PNG bytes, strings

    ``dispatch=False`` skips the object's own ``to_readout`` (used by adapters that implement it).
    """
    if isinstance(obj, Readout):
        children = obj.children
        if len(children) == 1 and isinstance(children[0], ReadoutSection):  # e.g. a one-section view readout
            children = children[0].children
        return ReadoutSection(*children, id=opts.get("id", obj.id), title=opts.get("title", obj.title))
    if isinstance(obj, ReadoutNode):
        return obj
    if isinstance(obj, (TabularData,)):
        return ReadoutTable(obj, **opts)
    if isinstance(obj, FieldSet):
        return ReadoutFields(obj, **opts)
    if isinstance(obj, ArrayData):
        return ReadoutArray(obj, display=True, **opts)
    cls_name = type(obj).__name__
    module = type(obj).__module__ or ""
    if cls_name == "Mesh3DAnimation":
        return ReadoutScene(model=obj, caption=caption, animated=True, **opts)
    if _is_graphics(obj):
        backend = str(getattr(obj, "backend", "")).lower()
        figure = obj.figure
        fig_name = type(figure).__name__
        if fig_name.startswith("Mesh3D") or "mesh3d" in backend:
            return ReadoutScene(model=obj, caption=caption, **opts)
        if fig_name.startswith("X3D") or "x3d" in backend:
            return ReadoutScene(html=figure.to_x3d(), caption=caption, **opts)
        return ReadoutPlot(obj, caption=caption, **opts)
    if cls_name == "X3D" and hasattr(obj, "to_widget"):
        return ReadoutScene(html=obj, caption=caption, **opts)
    if dispatch and hasattr(obj, "to_readout") and not isinstance(obj, type):
        return as_readout_node(obj.to_readout(), **opts)
    if hasattr(obj, "format_tex"):
        kind = cls_name
        if kind in ("TeXTable", "Table", "TeXArray", "Array", "TeXBlock"):
            return ReadoutCode(obj.format_tex(), language="latex", **opts)
        return ReadoutEquation(obj, **opts)
    if "PowerPoint" in module and hasattr(obj, "to_presml"):
        return ReadoutPresML(obj, **opts)
    if module.endswith("OpenXML.Elements") or cls_name == "Element" and hasattr(obj, "to_presml"):
        return ReadoutPresML(obj, **opts)
    if hasattr(obj, "to_jhtml") or (hasattr(obj, "tostring") and "JHTML" in module) or \
            (hasattr(obj, "tostring") and "Jupyter" in module):
        return ReadoutHTML(obj, **opts)
    if type(obj).__name__ == "Figure" and hasattr(obj, "savefig"):
        return ReadoutPlot(obj, caption=caption, **opts)
    if hasattr(obj, "to_dict") and hasattr(obj, "columns") and hasattr(obj, "dtypes"):  # pandas
        cols = [Column(str(c), obj[c].to_numpy()) for c in obj.columns]
        return ReadoutTable(TabularData(cols), **opts)
    if isinstance(obj, (bytes, bytearray)):
        return ReadoutImage(bytes(obj), caption=caption, **opts)
    if isinstance(obj, str):
        return ReadoutText(obj, **opts)
    if isinstance(obj, np.ndarray):
        return ReadoutArray(ArrayData(opts.pop("id", "array"), obj), display=True, **opts)
    from .Registry import record_nodes
    return ReadoutSection(*record_nodes(obj), **opts)

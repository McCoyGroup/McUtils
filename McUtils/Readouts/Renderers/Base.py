"""Shared renderer machinery (node dispatch, the render-time context) and the plain-text renderer."""

import textwrap

from ..Styles import ReadoutTheme
from ..Nodes import (ReadoutNode, ReadoutSection, ReadoutText, ReadoutFields, ReadoutTable,
                     ReadoutArray, ReadoutImage, ReadoutScene, ReadoutGallery, Readout)
from ..Views import ReadoutPlot, ReadoutEquation, ReadoutCode, ReadoutHTML, ReadoutPresML

__all__ = [
    "is_visible",
    "is_trivial",
    "array_preview",
    "hidden_stub",
    "ReadoutRenderer",
    "RenderContext",
    "handles",
    "TextReadoutRenderer",
]


def handles(*node_types):
    """Mark a renderer method as the handler for the given node classes."""
    def decorate(func):
        func._handles = node_types
        return func
    return decorate


def is_visible(node):
    """Whether a node has anything to display (export-only arrays don't)."""
    if isinstance(node, ReadoutArray):
        return node.display
    if isinstance(node, ReadoutSection) or node.kind == "gallery":
        return any(is_visible(c) for c in node.get_children())
    return True


def hidden_stub(node, theme=None, limit=3, force=False):
    """
    One line for a section that shows nothing because everything in it is an export-only array, or ``None`` (the node
    shows something, or holds no such array). A renderer writes it in place of the section's content so that a block a
    format can't show is never silently left out: it names each array with its shape and range and says the values
    are in the data export.

    Plain readouts keep export-only arrays out of sight (that is what they are for), so the stub is written only when the
    theme has the token ``stub_hidden`` (a report sets it) or ``force`` is true.
    """
    if not force and not (theme is not None and theme.get("stub_hidden")):
        return None
    if is_visible(node):
        return None
    arrays = [n for _, n in node.walk() if isinstance(n, ReadoutArray) and not n.display]
    if not arrays:
        return None
    parts = [f"{a.title or a.data.label or a.id}: {array_preview(a.data, theme)[1]}" for a in arrays[:limit]]
    more = f" and {len(arrays) - limit} more" if len(arrays) > limit else ""
    return "Not displayed (data only): " + "; ".join(parts) + more + ". The values are in the data export."


_CONTAINER_KINDS = ("section", "readout", "gallery", "grid", "flex", "panel")


def is_trivial(node, theme=None):
    """
    Whether a node is not worth showing on its own: it says (almost) nothing a plain ``repr`` wouldn't.

    With ``theme`` (``stub_hidden`` set, as a report does) an export-only array is not trivial: a renderer writes a stub
    line for it (see `hidden_stub`).

    A leaf is trivial if it is empty text, a hidden (export-only) array, or marked ``meta["trivial"] = True`` by
    whatever made it (a bare number or string wrapped in a one-field record is marked so; a record that merely has
    one field is not). Everything else (tables, arrays, images, scenes, plots, equations, code, html, ...) is not. A container (section, readout, gallery, layout) is trivial unless at least one of its
    children is not, so wrapping trivial content in more containers never makes it interesting.
    """
    kind = getattr(node, "kind", None)
    if kind not in _CONTAINER_KINDS and "trivial" in node.meta:
        return bool(node.meta["trivial"])
    if kind in _CONTAINER_KINDS:
        return all(is_trivial(c, theme) for c in node.get_children())
    if kind == "text":
        return not str(node.text).strip()
    if kind == "fields":
        return bool(node.meta.get("trivial", False))
    if kind == "array":
        return not node.display and not (theme is not None and theme.get("stub_hidden"))   # a stub is something to show
    return False


def array_preview(data, theme=None, max_rows=12, max_cols=10):
    """``(TabularData | None, summary text)`` for showing an `ArrayData`."""
    import numpy as np
    from ..Data import Column, TabularData
    a = np.asarray(data.array)
    unit = theme.get_unit_label(data.unit) if (theme is not None and data.unit) else data.unit
    summary = f"shape {a.shape}, {a.dtype}" + (f", {unit}" if unit else "")
    if a.size and np.issubdtype(a.dtype, np.number) and not np.iscomplexobj(a):
        summary += f"; min {np.nanmin(a):.6g}, max {np.nanmax(a):.6g}"
    if a.ndim == 1 and a.size <= max_rows * max_cols:
        if a.size > max_rows:
            return None, summary + f": [{', '.join(f'{v:.6g}' if np.issubdtype(a.dtype, np.number) else str(v) for v in a[:max_rows])}, …]"
        cols = [Column("index", np.arange(len(a)), label="i", quantity="index"),
                Column("value", a, label=data.label, unit=data.unit, quantity=data.quantity, fmt=data.fmt)]
        return TabularData(cols), summary
    if a.ndim == 2 and a.shape[1] <= max_cols:
        rows = a[:max_rows]
        cols = [Column("row", np.arange(len(rows)), label="i", quantity="index")]
        cols += [Column(f"c{j}", rows[:, j], label=str(j), unit=data.unit, quantity=data.quantity, fmt=data.fmt)
                 for j in range(a.shape[1])]
        if len(a) > max_rows:
            summary += f" (first {max_rows} of {len(a)} rows)"
        return TabularData(cols), summary
    return None, summary


class RenderContext:
    """Render-time state: the node path, nesting depth and a cache shared across the tree."""

    def __init__(self, path=(), depth=0, cache=None, **extra):
        self.path = tuple(path)
        self.depth = depth
        self.cache = {} if cache is None else cache
        self.extra = extra

    def child(self, node, depth_increment=1, **extra):
        return type(self)(self.path + (node.id,), self.depth + depth_increment, self.cache,
                          **dict(self.extra, **extra))

    @property
    def path_string(self):
        return "/".join(self.path)


class ReadoutRenderer:
    hook_name = None
    handlers = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        handlers = {}
        for base in reversed(cls.__mro__[1:]):
            handlers.update(getattr(base, "handlers", {}) or {})
        for attr, val in cls.__dict__.items():
            for node_type in getattr(val, "_handles", ()):
                handlers[node_type] = attr
        cls.handlers = handlers

    @classmethod
    def register(cls, node_type, func):
        """Register ``func(renderer, node, ctx)`` as the handler for ``node_type``."""
        name = "_registered_" + node_type.__name__
        setattr(cls, name, func)
        cls.handlers[node_type] = name

    def __init__(self, style=None):
        self.theme = ReadoutTheme.resolve(style)

    def render(self, node, ctx):
        if self.hook_name is not None:
            hook = getattr(node, self.hook_name, None)
            if hook is not None and callable(hook):
                return hook(self, ctx)
        for klass in type(node).__mro__:
            if klass in self.handlers:
                return getattr(self, self.handlers[klass])(node, ctx)
        raise TypeError(f"{type(self).__name__} has no handler for {type(node).__name__}")

    def render_children(self, node, ctx, depth_increment=1):
        return [self.render(c, ctx.child(c, depth_increment)) for c in node.get_children()]


# --------------------------------------------------------------------------------------------- #
#  plain text (``repr``, logs, quick checks)
# --------------------------------------------------------------------------------------------- #
class TextReadoutRenderer(ReadoutRenderer):
    hook_name = "readout_text"
    width = 100

    def render_readout(self, readout):
        return "\n".join(self.render(readout, RenderContext())).rstrip() + "\n"

    @handles(Readout)
    def render_root(self, node, ctx):
        lines = [node.title or "Readout", "=" * len(node.title or "Readout")]
        if node.subtitle:
            lines.append(node.subtitle)
        lines.append("")
        for c in node.get_children():
            lines.extend(self.render(c, ctx.child(c)))
        return lines

    @handles(ReadoutSection)
    def render_section(self, node, ctx):
        title = node.title or node.id
        rule = "-" if ctx.depth <= 1 else "·"
        lines = [title, rule * len(title)]
        for c in node.get_children():
            lines.extend(self.render(c, ctx.child(c)))
        lines.append("")
        return lines

    @handles(ReadoutText)
    def render_text(self, node, ctx):
        return textwrap.wrap(str(node.text), self.width) + [""]

    @handles(ReadoutFields)
    def render_fields(self, node, ctx):
        fields = list(node.data)
        if not fields:
            return []
        w = max(len(f.label) for f in fields)
        lines = [node.title + ":"] if node.title else []
        lines += [f"{f.label.ljust(w)}  {f.format(self.theme)}" for f in fields]
        return lines + [""]

    @handles(ReadoutTable)
    def render_table(self, node, ctx):
        lines = [node.title + ":"] if node.title else []
        return lines + node.data.to_text(self.theme).split("\n") + [""]

    @handles(ReadoutArray)
    def render_array(self, node, ctx):
        a = node.data
        unit = f" ({self.theme.get_unit_label(a.unit)})" if a.unit else ""
        return [f"{a.label}{unit}: array of shape {a.array.shape}", ""]

    @handles(ReadoutImage)
    def render_image(self, node, ctx):
        return [f"[image{': ' + node.caption if node.caption else ''}]", ""]

    @handles(ReadoutScene)
    def render_scene(self, node, ctx):
        kind = "animated 3D scene" if node._animated else "3D scene"  # never builds the model
        cap = node.format_caption(self.theme)
        return [f"[{kind}{': ' + cap if cap else ''}]"]

    @handles(ReadoutGallery)
    def render_gallery(self, node, ctx):
        lines = [node.title + ":"] if node.title else []
        for c in node.get_children():
            lines.extend("  " + l for l in self.render(c, ctx.child(c)))
        return lines + [""]

    @handles(ReadoutPlot)
    def render_plot(self, node, ctx):
        """A plot as text: its caption and, when it carries its data, what is plotted (so a peek at it is not blank)."""
        from ..Data import TabularData
        d = getattr(node, "data", None)
        what = ""
        if isinstance(d, TabularData) and d.nrows:
            names = ", ".join(str(getattr(c, "label", None) or c.name) for c in d.columns[:6])
            what = f" ({d.nrows} points of {names})"
        return [f"[plot{what}{': ' + node.caption if node.caption else ''}]", ""]

    @handles(ReadoutEquation)
    def render_equation(self, node, ctx):
        return ["  " + node.latex(), ""]

    @handles(ReadoutCode)
    def render_code(self, node, ctx):
        lines = [node.title + ":"] if node.title else []
        return lines + ["    " + l for l in node.display_text(40).splitlines()] + [""]

    @handles(ReadoutHTML)
    def render_html(self, node, ctx):
        if node.fallback is not None:
            return self.render(node.fallback, ctx)
        text = node.text_content()
        return (text.splitlines() if text else ["[HTML view]"]) + [""]

    @handles(ReadoutPresML)
    def render_presml(self, node, ctx):
        return self.render(node.get_fallback(), ctx)

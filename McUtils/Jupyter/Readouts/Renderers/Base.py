"""Shared renderer machinery: node dispatch and the render-time context."""

from ..Styles import ReadoutTheme
from ..Nodes import ReadoutArray

__all__ = [
    "is_visible",
    "array_preview",
    "ReadoutRenderer",
    "RenderContext",
    "handles",
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
    if node.kind in ("section", "gallery", "readout"):
        return any(is_visible(c) for c in node.get_children())
    return True


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

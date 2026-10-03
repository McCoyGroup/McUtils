"""Plain-text rendering (``repr``, logs, quick checks)."""

import textwrap

from ..Nodes import (ReadoutNode, ReadoutSection, ReadoutText, ReadoutFields, ReadoutTable,
                     ReadoutArray, ReadoutImage, ReadoutScene, ReadoutGallery, Readout)
from .Base import ReadoutRenderer, RenderContext, handles

__all__ = ["TextReadoutRenderer"]


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

"""
PowerPoint rendering: flows a readout onto 16:9 slides.

Each top-level section starts a slide with a title band; blocks are laid out top to bottom and
overflow onto continuation slides ("(cont.)"). Tables and field lists are split by rows with the
header repeated. Galleries are tiled ``per_slide`` items per slide. Scenes become native 3D
models (`.glb`, skinned when animated, since PowerPoint only plays skeletal animation) with a
PNG poster from a configurable `ReadoutRasterizer`; one `SceneView` drives both the model
camera and the poster, so they match.

Text heights are estimated (there are no font metrics here), so the layout errs on the side of
generous row heights; PowerPoint grows table rows to fit wrapped text.
"""

import io
import json
import math
import struct

from ..Nodes import (ReadoutNode, ReadoutSection, ReadoutText, ReadoutFields, ReadoutTable,
                     ReadoutArray, ReadoutImage, ReadoutScene, ReadoutGallery, Readout)
from ..Scenes import ReadoutRasterizer, PosterRequest
from .Base import ReadoutRenderer, RenderContext, handles, is_visible
from .HTML import resolve_scene_view, resolve_gallery_views
from ..Views import ReadoutPlot, ReadoutEquation, ReadoutCode, ReadoutHTML, ReadoutPresML, _png_size

__all__ = ["PowerPointReadoutRenderer"]


def _grid(n):
    return {1: (1, 1), 2: (1, 2), 3: (1, 3), 4: (2, 2), 5: (2, 3), 6: (2, 3)}.get(
        n, (math.ceil(n / math.ceil(math.sqrt(n))), math.ceil(math.sqrt(n))))


def _glb_json(data):
    magic, version, size = struct.unpack_from("<4sII", data)
    if magic != b"glTF" or version != 2 or size != len(data):
        raise ValueError("not a binary glTF 2.0 file")
    length, kind = struct.unpack_from("<II", data, 12)
    if kind != 0x4E4F534A:
        raise ValueError("binary glTF without a JSON chunk")
    return json.loads(data[20:20 + length])


class _Flow:
    """A cursor over the current slide's content box."""

    def __init__(self, renderer, presentation):
        self.r = renderer
        self.pres = presentation
        t = renderer.theme
        self.W, self.H = t.get("slide.size")
        self.top, self.right, self.bottom_margin, self.left = t.get("slide.margin")
        self.title_height = t.get("slide.title_height")
        self.gap = t.get("slide.gap")
        self.slide = None
        self.title = None
        self.slide_titles = []
        self.y = None

    @property
    def x0(self):
        return self.left

    @property
    def width(self):
        return self.W - self.left - self.right

    @property
    def content_top(self):
        return self.top + self.title_height + self.gap

    @property
    def bottom(self):
        return self.H - self.bottom_margin

    @property
    def remaining(self):
        return self.bottom - self.y

    @property
    def content_height(self):
        return self.bottom - self.content_top

    def new_slide(self, title, continued=False):
        self.finish()
        self.slide = self.pres.add_slide()
        self.title = title
        self.slide_titles = [title + (" (cont.)" if continued else "")] if title else []
        self.y = self.content_top
        self.fresh = True
        return self.slide

    def finish(self):
        """Draw the current slide's title band (deferred so packed sections can join it)."""
        if self.slide is not None and self.slide_titles:
            self.r.draw_slide_title(self.slide, "  ·  ".join(self.slide_titles))
        self.slide_titles = []

    def ensure(self, height):
        """Make sure ``height`` fits; start a continuation slide if it doesn't."""
        if self.slide is None or (self.remaining < height and self.y > self.content_top + 1e-6):
            self.new_slide(self.title, continued=self.slide is not None)

    def advance(self, height):
        self.y += height + self.gap
        self.fresh = False

    def page(self, title):
        """Start a page for full-slide content, reusing the current slide if nothing is on it yet."""
        if self.slide is not None and getattr(self, "fresh", False):
            self.slide_titles = [title] if title else []
            self.title = title
            return self.slide
        return self.new_slide(title)


class PowerPointReadoutRenderer(ReadoutRenderer):
    hook_name = "readout_presml"

    def __init__(self, style=None, rasterizer=None, rasterizer_options=None, skinned=True,
                 validate_assets=True, title_slide=None, gallery_per_slide=None):
        super().__init__(style)
        self.rasterizer = ReadoutRasterizer.resolve(rasterizer, rasterizer_options)
        self.skinned = skinned
        self.validate_assets = validate_assets
        self.title_slide = self.theme.get("slide.title_slide") if title_slide is None else title_slide
        self.gallery_per_slide = gallery_per_slide
        self.posters = {}
        self.assets = {}

    # ---- primitives ------------------------------------------------------------------- #
    def font(self, size_key, color="text", bold=False, size=None, family=None):
        t = self.theme
        return {"size": size if size is not None else t.get("sizes." + size_key),
                "color": t.color(color), "family": family or t.get("font.pptx_family"), "bold": bold}

    def text_height(self, text, size, width, line_height=None):
        line_height = line_height or self.theme.get("slide.line_height")
        chars = max(int(width / (0.52 * size)), 8)
        lines = sum(max(1, math.ceil(len(par) / chars)) for par in str(text).split("\n"))
        return lines * size * line_height + 4

    def draw_text(self, slide, text, x, y, w, h, size_key="body", color="text", bold=False, align="left",
                  valign="top", size=None, name=None, family=None, fill=None):
        appearance = {"font": self.font(size_key, color, bold, size, family)}
        if fill is not None:
            appearance["fill"] = fill
        return slide.draw_text(
            text, layout={"position": (x, y), "size": (w, h), "alignment": align, "vertical_alignment": valign},
            appearance=appearance, name=name)

    def draw_slide_title(self, slide, title):
        t = self.theme
        W = t.get("slide.size")[0]
        top, right, _, left = t.get("slide.margin")
        h = t.get("slide.title_height")
        self.draw_text(slide, title, left, top, W - left - right, h - 6, "section", "primary", bold=True,
                       valign="bottom", name="Title")
        slide.draw_shape("rect", layout={"position": (left, top + h - 2), "size": (W - left - right, 1.5)},
                         appearance={"fill": t.color("rule")}, name="Title rule")

    def render_readout(self, readout):
        from ....Plots.PowerPoint import PowerPointPresentation
        W, H = self.theme.get("slide.size")
        pres = PowerPointPresentation(size=(W, H), units=self.theme.get("slide.units"))
        flow = _Flow(self, pres)
        ctx = RenderContext(flow=flow)
        self.render(readout, ctx)
        flow.finish()
        return pres

    # ---- size estimates (for packing short sections onto one slide) ----------------------- #
    def estimate_height(self, node, width):
        """Estimated height of ``node`` in the flow, or ``None`` if it should start its own slide."""
        t = self.theme
        rh, gap = t.get("slide.row_height"), t.get("slide.gap")
        title_h = t.get("sizes.caption") * 1.6
        if not is_visible(node):
            return 0
        if isinstance(node, ReadoutText):
            return self.text_height(node.text, t.get("sizes.body"), width) + gap
        if isinstance(node, ReadoutFields):
            size = t.get("sizes.table")
            value_w = width - max(110, width * t.get("slide.field_label_fraction"))
            chars = max(int((value_w - 12) / (0.55 * size)), 8)
            h = sum(rh + (max(1, math.ceil(len(f.format(t)) / chars)) - 1) * size * 1.25 for f in node.data)
            return h + gap + (title_h if node.title else 0)
        if isinstance(node, ReadoutTable):
            if node.data.nrows > t.get("slide.max_table_rows"):
                return None
            return (node.data.nrows + 1) * rh + gap + (title_h if node.title else 0)
        if isinstance(node, (ReadoutPlot, ReadoutEquation, ReadoutCode)):
            return self.block_size(node, width)[1] + gap
        if isinstance(node, ReadoutArray):
            from .Base import array_preview
            table, _ = array_preview(node.data, t)
            return rh * (1.5 + (table.nrows + 1 if table is not None else 0)) + gap
        if isinstance(node, (ReadoutScene, ReadoutGallery, ReadoutImage, ReadoutHTML, ReadoutPresML)):
            return None
        if isinstance(node, ReadoutSection):
            total = t.get("sizes.subsection") * 1.6
            for c in node.get_children():
                h = self.estimate_height(c, width)
                if h is None:
                    return None
                total += h
            return total
        return None

    def draw_inline_heading(self, flow, title):
        t = self.theme
        size = t.get("sizes.section") * .8
        h = size * 1.5
        flow.y += flow.gap / 2
        self.draw_text(flow.slide, title, flow.x0, flow.y, flow.width, h, "section", "primary", bold=True,
                       size=size, valign="bottom", name="Heading")
        flow.slide.draw_shape("rect", layout={"position": (flow.x0, flow.y + h + 1), "size": (flow.width, .75)},
                              appearance={"fill": t.color("rule")}, name="Heading rule")
        flow.advance(h)

    # ---- structure ---------------------------------------------------------------------- #
    def _children(self, node, ctx):
        for c in node.get_children():
            self.render(c, ctx.child(c))

    @handles(Readout)
    def render_root(self, node, ctx):
        flow = ctx.extra["flow"]
        if self.title_slide:
            t = self.theme
            slide = flow.new_slide(None)
            W, H = t.get("slide.size")
            left = t.get("slide.margin")[3]
            w = W - 2 * left
            slide.draw_shape("rect", layout={"position": (0, 0), "size": (W, 8)},
                             appearance={"fill": t.color("primary")}, name="Accent bar")
            self.draw_text(slide, node.title or "Readout", left, H * .30, w, 60, "title", "primary", bold=True,
                           valign="bottom", name="Title")
            y = H * .30 + 66
            if node.subtitle:
                self.draw_text(slide, node.subtitle, left, y, w, 32, "subtitle", "muted", name="Subtitle")
                y += 38
            if node.units is not None:
                labels = [f"{q}: {t.get_unit_label(u)}" for q, u in node.units.units.items() if u is not None]
                if labels:
                    self.draw_text(slide, "Units — " + ", ".join(labels), left, H - 70, w, 24, "caption", "muted",
                                   name="Units")
            flow.slide = None
            flow.slide_titles = []
        self._children(node, ctx)

    @handles(ReadoutSection)
    def render_section(self, node, ctx):
        flow = ctx.extra["flow"]
        if not is_visible(node):
            return
        if ctx.depth <= 1:
            title = node.title or node.id
            est = self.estimate_height(node, flow.width) if self.theme.get("slide.pack_sections") else None
            head = self.theme.get("sizes.section") * 1.2 + flow.gap
            if (est is not None and flow.slide is not None and flow.y > flow.content_top + 1e-6
                    and est + head <= flow.remaining):
                self.draw_inline_heading(flow, title)
                flow.slide_titles.append(title)
                flow.title = title
            else:
                flow.new_slide(title)
        else:
            size = self.theme.get("sizes.subsection")
            h = size * 1.6
            nxt = node.get_children()[0] if node.get_children() else None
            if isinstance(nxt, ReadoutGallery):
                flow.title = node.title or flow.title
            else:
                flow.ensure(h + 3 * self.theme.get("slide.row_height"))
                self.draw_text(flow.slide, node.title or node.id, flow.x0, flow.y, flow.width, h, "subsection",
                               "primary", bold=True, name="Subheading")
                flow.advance(h - flow.gap / 2)
        self._children(node, ctx)

    # ---- blocks ------------------------------------------------------------------------- #
    @handles(ReadoutText)
    def render_text(self, node, ctx):
        flow = ctx.extra["flow"]
        size = self.theme.get("sizes.body")
        h = self.text_height(node.text, size, flow.width)
        flow.ensure(h)
        color = {"note": "muted", "error": "accent"}.get(node.role, "text")
        self.draw_text(flow.slide, str(node.text), flow.x0, flow.y, flow.width, h, "body", color)
        flow.advance(h)

    def _block_title(self, node, flow):
        if not node.title:
            return
        size = self.theme.get("sizes.caption")
        h = size * 1.6
        flow.ensure(h + 2 * self.theme.get("slide.row_height"))
        self.draw_text(flow.slide, node.title.upper(), flow.x0, flow.y, flow.width, h, "caption", "muted", bold=True)
        flow.y += h

    def _table_style(self):
        t = self.theme
        return dict(
            font=self.font("table"), header_font=self.font("table", "header_text", bold=True),
            header_fill=t.color("header_fill"), stripe_fill=t.color("stripe"),
            rule={"color": t.color("rule"), "width": .75},
            padding=t.get("slide.cell_padding"), row_height=t.get("slide.row_height"),
        )

    def _draw_rows(self, flow, rows, header, widths, row_heights, aligns, name, extra=None):
        """Place rows (with an optional repeated header) across as many slides as needed."""
        rh = self.theme.get("slide.row_height")
        min_rows = self.theme.get("slide.min_table_rows")
        max_rows = self.theme.get("slide.max_table_rows")
        i = 0
        while i < len(rows):
            head_h = rh if header is not None else 0
            need = head_h + sum(row_heights[i:i + min(min_rows, len(rows) - i)])
            flow.ensure(need)
            avail = flow.remaining - head_h
            n, used = 0, 0
            while i + n < len(rows) and n < max_rows and used + row_heights[i + n] <= avail + 1e-6:
                used += row_heights[i + n]
                n += 1
            n = max(n, 1)
            chunk = rows[i:i + n]
            used = sum(row_heights[i:i + n])
            table_rows = ([header] if header is not None else []) + chunk
            style = dict(self._table_style(), **(extra or {}))
            flow.slide.draw_table(
                table_rows, layout={"position": (flow.x0, flow.y), "size": (sum(widths), head_h + used)},
                column_widths=widths, header_rows=1 if header is not None else 0, alignments=aligns,
                name=name, **style)
            flow.advance(head_h + used)
            i += n

    @handles(ReadoutTable)
    def render_table(self, node, ctx):
        flow = ctx.extra["flow"]
        data = node.data
        size = self.theme.get("sizes.table")
        pad = sum(self.theme.get("slide.cell_padding")[1::2])
        headers = data.headers(self.theme)
        rows = data.format_rows(self.theme)
        widths = [max(48, 0.58 * size * max([len(h)] + [len(r[j]) for r in rows]) + pad + 4)
                  for j, h in enumerate(headers)]
        total = sum(widths)
        if total > flow.width:
            widths = [w * flow.width / total for w in widths]
        aligns = [c.align for c in data.columns]
        self._block_title(node, flow)
        rh = self.theme.get("slide.row_height")
        self._draw_rows(flow, rows, headers, widths, [rh] * len(rows), aligns, name=node.title or node.id)

    @handles(ReadoutFields)
    def render_fields(self, node, ctx):
        flow = ctx.extra["flow"]
        t = self.theme
        size = t.get("sizes.table")
        rh = t.get("slide.row_height")
        label_w = max(110, flow.width * t.get("slide.field_label_fraction"))
        value_w = flow.width - label_w
        label_font = self.font("table", "field_label")
        rows, heights = [], []
        for f in node.data:
            text = f.format(t)
            chars = max(int((value_w - 12) / (0.55 * size)), 8)
            lines = max(1, math.ceil(len(text) / chars))
            rows.append([{"text": f.label, "font": label_font}, {"text": text}])
            heights.append(rh + (lines - 1) * size * 1.25)
        self._block_title(node, flow)
        self._draw_rows(flow, rows, None, [label_w, value_w], heights, ["left", "left"],
                        name=node.title or node.id, extra={"stripe_fill": None})

    @handles(ReadoutArray)
    def render_array(self, node, ctx):
        if not node.display:
            return
        from .Base import array_preview
        table, summary = array_preview(node.data, self.theme)
        label = node.title or node.data.label
        self.render_text(ReadoutText(f"{label}: {summary}", role="note"), ctx)
        if table is not None:
            self.render_table(ReadoutTable(table), ctx)

    # ---- view leaves -------------------------------------------------------------------- #
    def block_size(self, node, width, max_height=None):
        """Natural (w, h) of a view leaf in the flow, scaled to fit ``width``/``max_height``."""
        t = self.theme
        if isinstance(node, ReadoutPlot):
            pw, ph = t.get("slide.plot_size")
            w = min(width, pw)
            h = w / node.aspect()
            if node.caption:
                h += t.get("sizes.caption") * 1.6
        elif isinstance(node, ReadoutEquation):
            px = _png_size(node.to_png())
            w, h = px[0] * 72 / 200, px[1] * 72 / 200
            if w > width:
                w, h = width, h * width / w
        elif isinstance(node, ReadoutCode):
            size = t.get("sizes.caption")
            n = min(len(node.text.splitlines()) or 1, t.get("slide.code_lines"))
            w, h = width, n * size * 1.22 + 12
        else:
            w, h = width, t.get("slide.row_height") * 2
        if max_height is not None and h > max_height:
            w, h = w * max_height / h, max_height
        return w, h

    def _image_asset(self, data, content_type):
        from ....Plots.PowerPoint import PresentationMLAsset
        ext = {"image/png": "png", "image/svg+xml": "svg", "image/jpeg": "jpg", "image/gif": "gif"}.get(content_type, "png")
        return PresentationMLAsset(data if isinstance(data, bytes) else data.encode(), content_type, ext)

    def _fit_image(self, slide, png, x, y, w, h, name=None):
        size = _png_size(png)
        aspect = size[0] / size[1] if size else w / h
        iw, ih = self._fit(w, h, aspect)
        slide.draw_image(self._image_asset(png, "image/png"),
                         layout={"position": (x + (w - iw) / 2, y + (h - ih) / 2), "size": (iw, ih)}, name=name)
        return iw, ih

    def draw_in_box(self, slide, node, x, y, w, h, ctx, view=None):
        """Draw any leaf into a fixed box (gallery cells, user layouts)."""
        t = self.theme
        if isinstance(node, ReadoutScene):
            if node.get_source() is None:
                self.draw_text(slide, "Interactive 3D view (see the HTML readout)", x, y + h / 2 - 12, w, 24,
                               "caption", "muted", align="center")
                return
            if view is None:
                view = resolve_scene_view(node, w / h, t, ctx.cache)
            self.draw_scene(slide, node, x, y, w, h, view, ctx.path_string)
        elif isinstance(node, ReadoutPlot):
            cap_h = t.get("sizes.caption") * 1.6 if node.caption else 0
            iw, ih = self._fit_image(slide, node.to_png(), x, y, w, h - cap_h, name=node.title or node.id)
            if node.caption:
                self.draw_text(slide, node.caption, x, y + (h - cap_h + ih) / 2, w, cap_h, "caption", "muted",
                               align="center")
        elif isinstance(node, ReadoutEquation):
            png = node.to_png(color="#" + t.color("text").lstrip("#"))
            ew, eh = self.block_size(node, w, h)
            self._fit_image(slide, png, x, y, ew if ew < w else w, eh, name="Equation")
        elif isinstance(node, ReadoutImage):
            data, ctype = node.get_image()
            if ctype == "image/png":
                self._fit_image(slide, data, x, y, w, h)
            elif node.fallback is not None:
                size = _png_size(node.fallback)
                iw, ih = self._fit(w, h, size[0] / size[1] if size else w / h)
                slide.draw_image(self._image_asset(data, ctype),
                                 fallback=self._image_asset(node.fallback, "image/png"),
                                 layout={"position": (x + (w - iw) / 2, y + (h - ih) / 2), "size": (iw, ih)})
            else:
                slide.draw_image(self._image_asset(data, ctype), layout={"position": (x, y), "size": (w, h)})
            if node.caption:
                self.draw_text(slide, node.caption, x, y + h, w, 18, "caption", "muted", align="center")
        elif isinstance(node, ReadoutCode):
            size = t.get("sizes.caption")
            n = max(1, int((h - 12) / (size * 1.22)))
            self.draw_text(slide, node.display_text(n - 1 if len(node.text.splitlines()) > n else None),
                           x, y, w, h, "caption", family=t.get("font.pptx_mono"), fill=t.color("stripe"),
                           name=node.title or "Code")
        elif isinstance(node, ReadoutPresML):
            from ....Plots.PowerPoint import PresentationMLElementLayout
            p = node.primitive
            if not hasattr(p, "layout"):
                from ....Plots.PowerPoint import PresentationMLPrimitive
                p = PresentationMLPrimitive(p)
            pw, ph = node.size or (w, h)
            p.layout = PresentationMLElementLayout.from_options(p.layout, bounds=(x, y, min(pw, w), min(ph, h)),
                                                                units=t.get("slide.units"))
            slide.draw_primitive(p)
        elif isinstance(node, ReadoutHTML):
            if node.fallback is not None:
                self.draw_in_box(slide, node.fallback, x, y, w, h, ctx)
            else:
                self.draw_text(slide, node.title or "HTML view (see the HTML readout)", x, y + h / 2 - 12, w, 24,
                               "caption", "muted", align="center")
        elif isinstance(node, ReadoutText):
            self.draw_text(slide, str(node.text), x, y, w, h, "body")
        elif isinstance(node, (ReadoutTable, ReadoutFields)):
            rh = t.get("slide.row_height")
            if isinstance(node, ReadoutTable):
                data = node.data
                headers, rows = data.headers(t), data.format_rows(t)
                aligns = [c.align for c in data.columns]
            else:
                headers, rows, aligns = None, [[f.label, f.format(t)] for f in node.data], ["left", "left"]
            n = max(1, int(h / rh) - (1 if headers else 0))
            rows = rows[:n]
            ncol = len(rows[0]) if rows else len(headers or [])
            slide.draw_table(([headers] if headers else []) + rows,
                             layout={"position": (x, y), "size": (w, rh * (len(rows) + (1 if headers else 0)))},
                             column_widths=[w / ncol] * ncol, header_rows=1 if headers else 0, alignments=aligns,
                             **self._table_style())
        else:
            self.draw_text(slide, f"[{type(node).__name__}]", x, y, w, 24, "caption", "muted")

    def _flow_block(self, node, ctx):
        flow = ctx.extra["flow"]
        self._block_title(node, flow)
        w, h = self.block_size(node, flow.width, flow.content_height)
        flow.ensure(h)
        if h > flow.remaining:
            w, h = self.block_size(node, flow.width, flow.remaining)
        x = flow.x0 + (flow.width - w) / 2 if not isinstance(node, (ReadoutCode, ReadoutEquation)) else flow.x0
        self.draw_in_box(flow.slide, node, x, flow.y, w, h, ctx)
        flow.advance(h)

    @handles(ReadoutPlot, ReadoutEquation)
    def render_view(self, node, ctx):
        self._flow_block(node, ctx)

    @handles(ReadoutCode)
    def render_code(self, node, ctx):
        flow = ctx.extra["flow"]
        t = self.theme
        size = t.get("sizes.caption")
        line_h = size * 1.22
        lines = node.display_text().splitlines() or [""]
        self._block_title(node, flow)
        i = 0
        while i < len(lines):
            flow.ensure(min(len(lines) - i, 4) * line_h + 12)
            n = max(1, min(int((flow.remaining - 12) / line_h), t.get("slide.code_lines"), len(lines) - i))
            h = n * line_h + 12
            self.draw_text(flow.slide, "\n".join(lines[i:i + n]), flow.x0, flow.y, flow.width, h, "caption",
                           family=t.get("font.pptx_mono"), fill=t.color("stripe"), name=node.title or "Code")
            flow.advance(h)
            i += n

    @handles(ReadoutHTML)
    def render_html(self, node, ctx):
        if node.fallback is not None:
            return self.render(node.fallback, ctx)
        text = node.text_content()
        if text:
            return self.render_text(ReadoutText(text), ctx)
        self.render_text(ReadoutText(f"{node.title or 'Interactive HTML view'}: see the HTML readout", role="note"), ctx)

    @handles(ReadoutPresML)
    def render_presml(self, node, ctx):
        flow = ctx.extra["flow"]
        lay = getattr(node.primitive, "layout", None)
        opts = lay.get_options() if hasattr(lay, "get_options") else {}
        w = node.size[0] if node.size else (opts.get("width") or flow.width)
        if node.size:
            h = node.size[1]
        elif opts.get("height"):
            h = opts["height"]
        elif hasattr(node.primitive, "text"):
            fs = getattr(getattr(node.primitive, "appearance", None), "opts", {}).get("font")
            size = getattr(fs, "opts", {}).get("size", 18) if fs is not None else 18
            h = self.text_height(node.primitive.text, size, w)
        else:
            h = self.theme.get("slide.plot_size")[1]
        w, h = min(w, flow.width), min(h, flow.content_height)
        flow.ensure(h)
        self.draw_in_box(flow.slide, node, flow.x0 + (flow.width - w) / 2, flow.y, w, h, ctx)
        flow.advance(h)

    @handles(ReadoutImage)
    def render_image(self, node, ctx):
        flow = ctx.extra["flow"]
        data, ctype = node.get_image()
        png = data if ctype == "image/png" else node.fallback
        size = _png_size(png) if png is not None else None
        pw, ph = self.theme.get("slide.plot_size")
        if size:
            w = min(flow.width, pw, size[0] * .75)
            h = w * size[1] / size[0]
        else:
            w, h = min(flow.width, pw), ph
        cap = self.theme.get("sizes.caption") * 1.6 if node.caption else 0
        flow.ensure(h + cap)
        if h + cap > flow.remaining:
            h = flow.remaining - cap
        self.draw_in_box(flow.slide, ReadoutImage(data, content_type=ctype, fallback=node.fallback),
                         flow.x0 + (flow.width - w) / 2, flow.y, w, h, ctx)
        if node.caption:
            self.draw_text(flow.slide, node.caption, flow.x0, flow.y + h, flow.width, cap, "caption", "muted",
                           align="center")
        flow.advance(h + cap)

    # ---- scenes ------------------------------------------------------------------------- #
    def _lighting(self):
        from ....Plots.PowerPoint import PresentationML
        lights = []
        for l in self.theme.get("scene.lighting"):
            l = dict(l)
            kind = l.pop("type")
            lights.append(PresentationML.AmbientLight(**l) if kind == "ambient" else PresentationML.PointLight(**l))
        return PresentationML.Appearance(lighting=tuple(lights))

    def _validate_glb(self, data, animated, path):
        gltf = _glb_json(data)
        if animated:
            if not gltf.get("animations"):
                raise ValueError(f"{path}: animated scene exported without animations")
            if self.skinned:
                if not gltf.get("skins"):
                    raise ValueError(f"{path}: PowerPoint only plays skinned animation, but no skin was exported")
                joints = set(gltf["skins"][0]["joints"])
                bad = [c for c in gltf["animations"][0]["channels"] if c["target"]["node"] not in joints]
                if bad:
                    raise ValueError(f"{path}: {len(bad)} animation channels don't target skin joints")
        return gltf

    def get_poster(self, node, view, w, h, path):
        t = self.theme
        scale = t.get("scene.poster_scale")
        key = (id(node), id(view), round(w), round(h))
        if key not in self.posters:
            req = PosterRequest(node.get_source(), view, int(round(w * scale)), int(round(h * scale)),
                                background=t.get("scene.background"), scene_id=node.id, path=path)
            self.posters[key] = self.rasterizer.rasterize(req)
        return self.posters[key]

    def draw_scene(self, slide, node, x, y, w, h, view, path):
        from ....Plots.PowerPoint import PresentationML, PresentationMLAsset
        src = node.get_source()
        if src is None:
            raise ValueError(f"{path}: scene has no mesh model to export")
        glb = src.to_glb(skinned=self.skinned)
        if self.validate_assets:
            self._validate_glb(glb, src.animated, path)
        self.assets[path] = glb
        poster = self.get_poster(node, view, w, h, path)
        layout = PresentationML.Layout(
            position=(x, y), size=(w, h),
            view=PresentationML.Model3DView(
                camera=PresentationML.Camera(position=tuple(view.camera_offset.tolist()),
                                             up=tuple(view.up.tolist()), field_of_view=view.fov),
                transform=PresentationML.ModelTransform(center=tuple(view.center.tolist()),
                                                        metres_per_unit=self.theme.get("scene.metres_per_unit")),
            ))
        animation = PresentationML.Animation(duration=src.duration, loop=True) if src.animated else None
        slide.draw_glb(PresentationMLAsset(glb, "model/gltf.binary", "glb"),
                       fallback=PresentationMLAsset(poster, "image/png", "png"),
                       layout=layout, appearance=self._lighting(), animation=animation,
                       name=(node.title or node.format_caption(self.theme) or node.id))

    def _fit(self, box_w, box_h, aspect):
        w = min(box_w, box_h * aspect)
        return w, w / aspect

    @handles(ReadoutScene)
    def render_scene(self, node, ctx):
        flow = ctx.extra["flow"]
        if node.get_source() is None:
            return self.render_text(ReadoutText(
                f"{node.format_caption(self.theme) or 'Interactive 3D view'}: see the HTML readout", role="note"), ctx)
        sw, sh = self.theme.get("slide.scene_size")
        cap_h = self.theme.get("slide.scene_caption_height") if node.caption else 0
        if flow.slide is None or flow.remaining < .6 * sh + cap_h:
            flow.ensure(flow.content_height)
        w, h = self._fit(flow.width, min(sh, flow.remaining - cap_h), sw / sh)
        x = flow.x0 + (flow.width - w) / 2
        view = resolve_scene_view(node, w / h, self.theme, ctx.cache)
        self.draw_scene(flow.slide, node, x, flow.y, w, h, view, ctx.path_string)
        if node.caption:
            self.draw_text(flow.slide, node.format_caption(self.theme), flow.x0, flow.y + h + 4, flow.width,
                           cap_h - 4, "scene_caption", align="center", name="Caption")
        flow.advance(h + cap_h)

    @handles(ReadoutGallery)
    def render_gallery(self, node, ctx):
        flow = ctx.extra["flow"]
        t = self.theme
        items = list(node.get_children())
        if not items:
            return
        k = self.gallery_per_slide or node.per_slide or t.get("slide.gallery_per_slide")
        rows, cols = _grid(min(k, len(items))) if node.columns is None else (math.ceil(k / node.columns), node.columns)
        k = min(k, rows * cols)
        sw, sh = t.get("slide.scene_size")
        aspect = sw / sh
        cap_h = t.get("slide.scene_caption_height")
        gap = flow.gap
        cell_w = (flow.width - (cols - 1) * gap) / cols
        cell_h = (flow.content_height - (rows - 1) * gap) / rows
        w, h = self._fit(cell_w, min(sh, cell_h - cap_h), aspect)
        views = resolve_gallery_views(node, w / h, t, ctx.cache)
        title = flow.title if node.title is None else node.title
        npages = math.ceil(len(items) / k)
        for p in range(npages):
            page = items[p * k:(p + 1) * k]
            flow.page(title + (f"  ({p + 1}/{npages})" if npages > 1 else ""))
            flow.title = title
            flow.fresh = False
            for j, item in enumerate(page):
                r, c = divmod(j, cols)
                cx = flow.x0 + c * (cell_w + gap)
                cy = flow.content_top + r * (cell_h + gap)
                x = cx + (cell_w - w) / 2
                y = cy + max(0, (cell_h - cap_h - h) / 2)
                ictx = ctx.child(item)
                if isinstance(item, ReadoutScene):
                    self.draw_scene(flow.slide, item, x, y, w, h, views.get(id(item)), ictx.path_string)
                    cap = item.format_caption(t)
                    if cap:
                        self.draw_text(flow.slide, cap, cx, y + h + 4, cell_w, cap_h - 4, "scene_caption",
                                       align="center", name="Caption")
                else:
                    self.draw_in_box(flow.slide, item, cx, cy, cell_w, cell_h, ictx)
            flow.y = flow.bottom

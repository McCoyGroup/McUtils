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
    def font(self, size_key, color="text", bold=False, size=None):
        t = self.theme
        return {"size": size if size is not None else t.get("sizes." + size_key),
                "color": t.color(color), "family": t.get("font.pptx_family"), "bold": bold}

    def text_height(self, text, size, width, line_height=None):
        line_height = line_height or self.theme.get("slide.line_height")
        chars = max(int(width / (0.52 * size)), 8)
        lines = sum(max(1, math.ceil(len(par) / chars)) for par in str(text).split("\n"))
        return lines * size * line_height + 4

    def draw_text(self, slide, text, x, y, w, h, size_key="body", color="text", bold=False, align="left",
                  valign="top", size=None, name=None):
        return slide.draw_text(
            text, layout={"position": (x, y), "size": (w, h), "alignment": align, "vertical_alignment": valign},
            appearance={"font": self.font(size_key, color, bold, size)}, name=name)

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
        if isinstance(node, (ReadoutScene, ReadoutGallery, ReadoutImage)):
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
        a = node.data
        self.render_text(ReadoutText(f"{a.label}: array of shape {a.array.shape}", role="note"), ctx)

    @handles(ReadoutImage)
    def render_image(self, node, ctx):
        flow = ctx.extra["flow"]
        data, ctype = node.get_image()
        from ....Plots.PowerPoint import PresentationMLAsset
        w = flow.width * .6
        h = min(flow.content_height * .8, w * .75)
        flow.ensure(h)
        ext = "svg" if "svg" in ctype else "png"
        flow.slide.draw_image(PresentationMLAsset(data if isinstance(data, bytes) else data.encode(), ctype, ext),
                              layout={"position": (flow.x0 + (flow.width - w) / 2, flow.y), "size": (w, h)})
        flow.advance(h)

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
            flow.new_slide(title + (f"  ({p + 1}/{npages})" if npages > 1 else ""))
            flow.title = title
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
                    # non-scene items get their own flow on the slide
                    self.render(item, ictx)
            flow.y = flow.bottom

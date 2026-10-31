"""
HTML rendering for Jupyter and standalone pages.

* ``mode='static'``: plain elements, with the X3DOM runtime loaded once in the document head
  (`render_document`); good for files and for sharing.
* ``mode='widget'``: each scene uses `X3D.to_widget()` (dynamic runtime loading), which is what
  displays reliably in Jupyter outputs.

Theme tokens become CSS custom properties scoped to ``.mcr-root``.
"""

import base64
import html as _html
import os

from ..Nodes import (ReadoutNode, ReadoutSection, ReadoutText, ReadoutFields, ReadoutTable,
                     ReadoutArray, ReadoutImage, ReadoutScene, ReadoutGallery, Readout,
                     ReadoutGrid, ReadoutFlex, ReadoutPanel)
from ..Views import ReadoutPlot, ReadoutEquation, ReadoutCode, ReadoutHTML, ReadoutPresML, ReadoutWidget
from ..Scenes import SceneView
from .Base import ReadoutRenderer, RenderContext, handles, is_visible

__all__ = ["HTMLReadoutRenderer", "resolve_scene_view", "resolve_gallery_views"]


def resolve_scene_view(scene, aspect, theme, cache=None):
    if scene.view is not None:
        return scene.view
    key = ("view", id(scene), round(aspect, 4))
    if cache is not None and key in cache:
        return cache[key]
    src = scene.get_source()
    if src is None:
        # HTML-only X3D scenes retain their authored camera; there is no mesh to fit.
        return None
    view = SceneView.fit(src.vertices(), aspect=aspect, fov=theme.get("scene.fov"),
                         padding=theme.get("scene.padding"))
    if cache is not None:
        cache[key] = view
    return view


def resolve_gallery_views(gallery, aspect, theme, cache=None):
    """One view per item; a single shared fit when ``gallery.shared_view``."""
    scenes = [c for c in gallery.get_children() if isinstance(c, ReadoutScene)]
    if not gallery.shared_view:
        return {id(s): resolve_scene_view(s, aspect, theme, cache) for s in scenes}
    key = ("gallery_view", id(gallery), round(aspect, 4))
    if cache is not None and key in cache:
        return cache[key]
    import numpy as np
    explicit = {id(s): s.view for s in scenes if s.view is not None}
    rest = [s for s in scenes if s.view is None and s.get_source() is not None]
    views = dict(explicit)
    if rest:
        verts = np.concatenate([s.get_source().vertices() for s in rest])
        shared = SceneView.fit(verts, aspect=aspect, fov=theme.get("scene.fov"), padding=theme.get("scene.padding"))
        views.update({id(s): shared for s in rest})
    if cache is not None:
        cache[key] = views
    return views


_CSS = """
.mcr-root{{--mcr-text:{text};--mcr-muted:{muted};--mcr-primary:{primary};--mcr-accent:{accent};
 --mcr-rule:{rule};--mcr-header-fill:{header_fill};--mcr-header-text:{header_text};--mcr-stripe:{stripe};
 --mcr-bg:{background};--mcr-label:{field_label};
 font-family:{family};font-size:{body}px;line-height:1.45;color:var(--mcr-text);background:var(--mcr-bg);
 max-width:{max_width}px;margin:0 auto;padding:18px 22px;box-sizing:border-box;border-radius:8px}}
.mcr-root *{{box-sizing:border-box}}
.mcr-header{{margin-bottom:10px}}
.mcr-title{{font-size:{title}px;font-weight:650;margin:0;color:var(--mcr-primary);line-height:1.2}}
.mcr-subtitle{{color:var(--mcr-muted);margin-top:4px;font-size:{subtitle}px}}
.mcr-meta{{color:var(--mcr-muted);font-size:{caption}px;margin-top:4px}}
.mcr-section{{border-top:1px solid var(--mcr-rule);padding:6px 0 10px}}
.mcr-section>summary{{cursor:pointer;list-style:none;display:flex;align-items:baseline;gap:.45em;padding:4px 0}}
.mcr-section>summary::-webkit-details-marker{{display:none}}
.mcr-section>summary::before{{content:'\\25B8';color:var(--mcr-muted);font-size:.9em;width:.8em}}
.mcr-section[open]>summary::before{{content:'\\25BE'}}
.mcr-h{{margin:0;font-weight:620;color:var(--mcr-primary)}}
.mcr-h1{{font-size:{section}px}} .mcr-h2{{font-size:{subsection}px}} .mcr-h3{{font-size:{body}px}}
.mcr-body{{padding-left:1.25em}}
.mcr-subsection{{margin-top:6px}}
.mcr-block-title{{font-weight:600;color:var(--mcr-muted);margin:8px 0 4px;font-size:{caption}px;
 text-transform:uppercase;letter-spacing:.04em}}
.mcr-fields{{display:grid;grid-template-columns:max-content minmax(0,1fr);gap:3px 20px;margin:4px 0 8px}}
.mcr-fields dt{{color:var(--mcr-label)}}
.mcr-fields dd{{margin:0;font-variant-numeric:tabular-nums;overflow-wrap:anywhere}}
.mcr-mono{{font-family:{mono};font-size:.92em}}
.mcr-table-wrap{{max-height:{table_max_height}px;overflow:auto;border:1px solid var(--mcr-rule);
 border-radius:6px;display:inline-block;max-width:100%;margin:4px 0 8px}}
table.mcr-table{{border-collapse:collapse;font-size:{table}px;font-variant-numeric:tabular-nums}}
table.mcr-table th{{position:sticky;top:0;background:var(--mcr-header-fill);color:var(--mcr-header-text);
 font-weight:600;padding:5px 12px;white-space:nowrap}}
table.mcr-table td{{padding:3px 12px;border-top:1px solid var(--mcr-rule);white-space:nowrap}}
table.mcr-table tbody tr:nth-child(even){{background:var(--mcr-stripe)}}
.mcr-r{{text-align:right}} .mcr-l{{text-align:left}} .mcr-c{{text-align:center}}
.mcr-gallery{{display:flex;flex-wrap:wrap;gap:12px;margin:6px 0}}
figure.mcr-scene{{margin:6px 0;display:inline-block;border:1px solid var(--mcr-rule);border-radius:6px;
 overflow:hidden;background:{scene_bg};vertical-align:top}}
figure.mcr-scene x3d{{display:block;border:none}}
figure.mcr-scene figcaption{{text-align:center;padding:4px 8px 6px;font-size:{scene_caption}px;
 border-top:1px solid var(--mcr-rule);background:var(--mcr-bg)}}
.mcr-text{{margin:4px 0 8px}}
.mcr-note{{color:var(--mcr-muted);font-style:italic}}
.mcr-error{{color:#B42318}}
.mcr-image{{max-width:100%}}
figure.mcr-plot{{margin:6px 0;display:inline-block;max-width:100%;vertical-align:top}}
figure.mcr-plot svg,figure.mcr-plot img{{max-width:100%;height:auto;display:block}}
figure.mcr-plot figcaption{{text-align:center;color:var(--mcr-muted);font-size:{caption}px;padding-top:2px}}
.mcr-eq{{margin:8px 0;overflow-x:auto}} .mcr-eq svg{{max-width:100%;height:auto}}
pre.mcr-code{{background:var(--mcr-stripe);border:1px solid var(--mcr-rule);border-radius:6px;padding:8px 10px;
 font-family:{mono};font-size:{caption}px;line-height:1.35;max-height:{table_max_height}px;overflow:auto;margin:4px 0 8px;
 white-space:pre}}
.mcr-cell{{display:inline-block;vertical-align:top;max-width:100%}}
.mcr-html{{margin:4px 0 8px}}
"""


class HTMLReadoutRenderer(ReadoutRenderer):
    hook_name = "readout_html"

    def __init__(self, style=None, mode="static", x3dom_path=None, collapsible=None, scene_size=None,
                 gallery_scene_size=None):
        super().__init__(style)
        if mode not in ("static", "widget"):
            raise ValueError("mode must be 'static' or 'widget'")
        self.mode = mode
        self.x3dom_path = x3dom_path
        self.collapsible = self.theme.get("html.collapsible") if collapsible is None else collapsible
        self.scene_size = scene_size or self.theme.get("html.scene_size")
        self.gallery_scene_size = gallery_scene_size or self.theme.get("html.gallery_scene_size")
        from ... import JHTML
        class WidgetElements:
            def __getattr__(self, name):
                return getattr(JHTML, name) if hasattr(JHTML, name) else getattr(JHTML.HTML, name)
        self.H = WidgetElements() if mode == "widget" else JHTML.HTML

    # ---- documents ------------------------------------------------------------------- #
    def css(self):
        t = self.theme
        scale = t.get("html.font_scale")
        px = {k: round(v * scale * 1.0) for k, v in t.get("sizes").items()}
        return _CSS.format(
            **{k: t.css_color(k) for k in t.get("colors")},
            family=t.get("font.family"), mono=t.get("font.mono"),
            max_width=t.get("html.max_width"), table_max_height=t.get("html.table_max_height"),
            scene_bg=t.get("scene.background"),
            **px,
        )

    def render_readout(self, readout):
        self._has_scenes = False
        self._head = []
        return self.render(readout, RenderContext())

    def render_fragment(self, node):
        self._has_scenes = False
        self._head = []
        body = self.render(node, RenderContext())
        items = body if isinstance(body,list) else [body]
        return self.H.Div(self.H.Style(self.css()), *items, cls='mcr-root')

    def runtime_elements(self):
        H = self.H
        from ....Plots.X3DInterface import X3D
        path = self.x3dom_path
        local = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                             "resources", "x3dom-full.js")
        if path is None:
            return [H.Link(rel="stylesheet", href=X3D.X3DOM_CSS), H.Script(src=X3D.X3DOM_JS)]
        if path == "local":
            return [H.Script(src="file://" + local)]
        if path == "inline":
            with open(local, encoding="utf-8") as f:
                return [H.Script(f.read().replace("</script", "<\\/script"))]
        return [H.Script(src=path)]

    def render_document(self, readout):
        H = self.H
        body = self.render_readout(readout)
        viewport=H.Meta(name='viewport')
        # `content` is also a CSS property in JHTML; set the actual Meta attribute.
        viewport.attrs=dict(viewport.attrs,content='width=device-width, initial-scale=1')
        head = [H.Meta(charset="utf-8"), viewport,
                H.Title(readout.title or "Readout"),
                H.Style("html,body{margin:0;background:#F6F8FA} body{padding:16px 0}")]
        if self._has_scenes and self.mode == "static":
            head.extend(self.runtime_elements())
        seen = set()
        for el in self._head:
            key = el if isinstance(el, str) else el.tostring()
            if key not in seen:
                seen.add(key)
                head.append(H.RawHTML(el) if isinstance(el, str) else el)
        return "<!DOCTYPE html>\n" + H.Html(H.Head(*head), H.Body(body), lang="en").tostring()

    # ---- nodes ------------------------------------------------------------------------- #
    def _children(self, node, ctx):
        out = []
        for c in node.get_children():
            res = self.render(c, ctx.child(c))
            if res is None:
                continue
            out.extend(res if isinstance(res, list) else [res])
        return out

    @handles(Readout)
    def render_root(self, node, ctx):
        H = self.H
        header = [H.Div(node.title or "Readout", cls="mcr-title")]
        if node.subtitle:
            header.append(H.Div(node.subtitle, cls="mcr-subtitle"))
        if node.units is not None:
            labels = [f"{q}: {self.theme.get_unit_label(u)}" for q, u in node.units.units.items() if u is not None]
            if labels:
                header.append(H.Div("Units — " + ", ".join(labels), cls="mcr-meta"))
        return H.Div(H.Style(self.css()), H.Div(*header, cls="mcr-header"), *self._children(node, ctx),
                     cls="mcr-root", id="mcr-" + node.id)

    @handles(ReadoutSection)
    def render_section(self, node, ctx):
        H = self.H
        if not is_visible(node):
            return None
        level = min(max(ctx.depth, 1), 3)
        heading = H.Span(node.title or node.id, cls=f"mcr-h mcr-h{level}")
        body = H.Div(*self._children(node, ctx), cls="mcr-body")
        cls = "mcr-section" if level == 1 else "mcr-section mcr-subsection"
        if self.collapsible:
            return H.Details(H.Summary(heading), body, cls=cls, open=True, id=f"mcr-{ctx.path_string.replace('/', '-')}")
        return H.Div(H.Div(heading), body, cls=cls)

    @handles(ReadoutText)
    def render_text(self, node, ctx):
        cls = "mcr-text" + {"note": " mcr-note", "error": " mcr-error"}.get(node.role, "")
        return self.H.P(str(node.text), cls=cls)

    def _block_title(self, node):
        return [self.H.Div(node.title, cls="mcr-block-title")] if node.title else []

    @handles(ReadoutFields)
    def render_fields(self, node, ctx):
        H = self.H
        items = []
        for f in node.data:
            mono = f.quantity in ("identifier", "path")
            items.append(H.Dt(f.label, title=f.description) if f.description else H.Dt(f.label))
            items.append(H.Dd(f.format(self.theme), cls="mcr-mono" if mono else None))
        return self._block_title(node) + [H.Dl(*items, cls="mcr-fields")]

    @handles(ReadoutTable)
    def render_table(self, node, ctx):
        H = self.H
        data = node.data
        aligns = ["mcr-r" if c.align == "right" else "mcr-l" for c in data.columns]
        head = H.Thead(H.Tr(*[H.Th(h, cls=a) for h, a in zip(data.headers(self.theme), aligns)]))
        rows = [H.Tr(*[H.Td(v, cls=a) for v, a in zip(r, aligns)]) for r in data.format_rows(self.theme)]
        table = H.Table(head, H.Tbody(*rows), cls="mcr-table")
        return self._block_title(node) + [H.Div(table, cls="mcr-table-wrap")]

    @handles(ReadoutArray)
    def render_array(self, node, ctx):
        if not node.display:
            return None
        from .Base import array_preview
        table, summary = array_preview(node.data, self.theme)
        out = self._block_title(node) + [self.H.P(summary, cls="mcr-text mcr-note")]
        if table is not None:
            out.append(self.render_table(ReadoutTable(table), ctx)[-1])
        return out

    @handles(ReadoutImage)
    def render_image(self, node, ctx):
        H = self.H
        data, ctype = node.get_image()
        if isinstance(data, str):
            data = data.encode()
        src = f"data:{ctype};base64," + base64.b64encode(data).decode()
        kids = [H.Img(src=src, cls="mcr-image")]
        if node.caption:
            kids.append(H.Figcaption(node.caption))
        return H.Figure(*kids, cls="mcr-scene")

    def _scene_element(self, node, ctx, size, view=None):
        H = self.H
        w, h = size
        src = node.get_source()
        if view is None and src is not None:
            view = resolve_scene_view(node, w / h, self.theme, ctx.cache)
        x3d = node.get_html(view)
        if x3d is None:
            x3d = src.to_x3d(view=view, width=w, height=h, background=self.theme.get("scene.background"))
        else:
            x3d.opts["width"] = w
            x3d.opts["height"] = h
        self._has_scenes = True
        if self.mode == "widget":
            elem = x3d.to_widget()
        elif getattr(x3d, 'components', ()) or x3d.has_playback():
            # Keep component controls and their lifecycle in standalone reports.
            # render_document supplies the shared X3DOM runtime in the head.
            elem = x3d.to_widget(dynamic_loading=False, include_resources=False)
        else:
            elem = x3d.to_x3d()
        kids = [elem]
        cap = node.format_caption(self.theme)
        if cap:
            kids.append(H.Figcaption(cap))
        return H.Figure(*kids, cls="mcr-scene", style=f"width:{w + 2}px")

    @handles(ReadoutScene)
    def render_scene(self, node, ctx):
        return self._scene_element(node, ctx, self.scene_size)

    @handles(ReadoutPlot)
    def render_plot(self, node, ctx):
        H = self.H
        try:
            body = H.RawHTML(node.to_svg())
        except Exception:
            body = H.Img(src="data:image/png;base64," + base64.b64encode(node.to_png()).decode())
        kids = [body]
        if node.caption:
            kids.append(H.Figcaption(node.caption))
        return self._block_title(node) + [H.Figure(*kids, cls="mcr-plot")]

    @handles(ReadoutEquation)
    def render_equation(self, node, ctx):
        H = self.H
        color = "#" + self.theme.color("text").lstrip("#")
        return H.Div(H.RawHTML(node.to_svg(color=color)), cls="mcr-eq", title=node.latex(),
                     data_latex=node.latex())

    @handles(ReadoutCode)
    def render_code(self, node, ctx):
        return self._block_title(node) + [self.H.Pre(node.display_text(), cls="mcr-code")]

    @handles(ReadoutHTML)
    def render_html(self, node, ctx):
        self._head.extend(node.head)
        from ...Apps.Interfaces import Component
        if isinstance(node,ReadoutWidget) and isinstance(node.element,Component):
            from ...Apps import AppTheme
            app_theme = AppTheme(node.element.ui_theme or AppTheme.current().name)
            key = ('app-theme',app_theme.name)
            if self.mode == 'static' and key not in ctx.cache:
                ctx.cache[key]=True
                self._head.extend(app_theme.resources())
        el = node.get_element(mode=self.mode)
        if isinstance(node, ReadoutWidget) and self.mode == 'static':
            from ...JHTML import JHTML, ActiveHTMLWrapper
            if not isinstance(el,(str,JHTML.HTML.XMLElement)) and not hasattr(el,'tostring'):
                if node.fallback is not None:
                    return self.render(node.fallback,ctx)
                return self.H.P((node.title or 'Interactive widget')+' requires a live Python kernel.',
                                cls='mcr-note',data_requires_kernel='true')
        if isinstance(el,str):
            el = self.H.RawHTML(el)
        return self._block_title(node)+[self.H.Div(el,cls='mcr-html')]

    def _app_theme(self, node, ctx):
        from ...Apps import AppTheme
        theme = AppTheme(node.ui_theme) if node.ui_theme is not None else ctx.extra.get('app_theme',AppTheme.current())
        key = ('app-theme',theme.name)
        if key not in ctx.cache:
            ctx.cache[key] = True
            if self.mode == 'static':
                self._head.extend(theme.resources())
        return theme

    def _layout_child(self, child, ctx, theme):
        from ...Apps import AppTheme
        with AppTheme.rendering(theme):
            result = self.render(child,ctx.child(child,app_theme=theme))
        return result if isinstance(result,list) else [result] if result is not None else []

    def _layout_root(self, body, theme):
        if self.mode == 'widget':
            return theme.decorate(body)
        return theme.component('root',body,mode=self.mode,cls=['mcui-root','mcui-'+theme.name])

    @handles(ReadoutGrid)
    def render_grid(self, node, ctx):
        from ...Apps import Grid
        theme = self._app_theme(node,ctx)
        cells = []
        for child, placement, attrs in node.cells:
            attrs = theme.attrs(attrs)
            style = dict(attrs.pop('style',{}),**Grid.Item.get_grid_styles(**placement))
            style.setdefault('min-width',0)
            cells.append(self.H.Div(*self._layout_child(child,ctx,theme),style=style,**attrs))
        style = dict(node.style,**Grid.get_grid_styles(**node.grid_options))
        attrs=theme.attrs(node.html_attrs)
        attrs.setdefault('id','mcr-grid-'+node.id)
        body = theme.component('grid',*cells,mode=self.mode,style=style,**attrs)
        if node.collapse_below is not None:
            body = self.H.Div(self.H.Style(Grid.responsive_css(attrs['id'],node.collapse_below)),body)
        return self._layout_root(body,theme)

    @handles(ReadoutFlex)
    def render_flex(self, node, ctx):
        from ...Apps import Flex
        theme = self._app_theme(node,ctx)
        style = dict(node.style,**Flex.get_flex_styles(**node.flex_options))
        style.setdefault('min-width',0)
        if node.gap is not None:style['gap']=node.gap
        cells=[]
        for child,placement,attrs in node.cells:
            attrs=theme.attrs(attrs)
            item_style=dict(attrs.pop('style',{}),**Flex.Item.get_flex_styles(**placement))
            item_style.setdefault('min-width',0)
            cells.append(self.H.Div(*self._layout_child(child,ctx,theme),style=item_style,**attrs))
        return self._layout_root(theme.component('flex',*cells,mode=self.mode,style=style,**theme.attrs(node.html_attrs)),theme)

    @handles(ReadoutPanel)
    def render_panel(self, node, ctx):
        theme = self._app_theme(node,ctx)
        prefix = 'mcui-' if theme.name == 'native' else ''
        def content(child):
            if type(child) is ReadoutSection and child.title is None:
                return [item for nested in child.children for item in self._layout_child(nested,ctx.child(child),theme)]
            return self._layout_child(child,ctx,theme)
        parts=[]
        if node.header is not None:parts.append(theme.component('panel-header',*content(node.header),mode=self.mode,cls=prefix+'card-header'))
        if node.title:parts.append(theme.component('panel-header',node.title,mode=self.mode,cls=prefix+'card-header'))
        parts.append(theme.component('panel-body',*[item for child in node.body for item in content(child)],mode=self.mode,cls=prefix+'card-body'))
        if node.footer is not None:parts.append(theme.component('panel-footer',*content(node.footer),mode=self.mode,cls=prefix+'card-footer'))
        attrs = theme.attrs(node.html_attrs)
        from ...JHTML import JHTML
        attrs['cls'] = JHTML.manage_class(attrs.get('cls')) + [prefix+'card']
        return self._layout_root(theme.component('panel',*parts,mode=self.mode,style=node.style,**attrs),theme)

    @handles(ReadoutPresML)
    def render_presml(self, node, ctx):
        fb = node.get_fallback()
        return self.render(fb, ctx)

    @handles(ReadoutGallery)
    def render_gallery(self, node, ctx):
        H = self.H
        w, h = self.gallery_scene_size
        views = resolve_gallery_views(node, w / h, self.theme, ctx.cache)
        items = []
        for c in node.get_children():
            if isinstance(c, ReadoutScene):
                items.append(self._scene_element(c, ctx.child(c), (w, h), views.get(id(c))))
            else:
                res = self.render(c, ctx.child(c))
                if res is not None:
                    res = res if isinstance(res, list) else [res]
                    items.append(H.Div(*res, cls="mcr-cell", style=f"width:{w + 2}px"))
        style = None
        if node.columns is not None:
            import operator
            columns = operator.index(node.columns)
            if columns < 1:
                raise ValueError("ReadoutGallery.columns must be a positive integer")
            style = {"display": "grid", "grid-template-columns": f"repeat({columns}, max-content)"}
        return self._block_title(node) + [H.Div(*items, cls="mcr-gallery", style=style)]

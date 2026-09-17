import uuid

from .JHTML import HTML

__all__ = [
    "JSMol"
]

__reload_hooks__ = [".JHTML"]

class JSMol:
    class Applet(HTML.Div):
        version = "16.3.7.9"
        jsmol_source = f"https://cdn.jsdelivr.net/gh/b3m2a1/jsmol-cdn@{version}/jsmol/JSmol.min.js"
        jmol2_source = f"https://cdn.jsdelivr.net/gh/b3m2a1/jsmol-cdn@{version}/jsmol/js/Jmol2.js"
        patch_script = f"""
        if (typeof Jmol._patched === 'undefined') {{
            Jmol._patched = true;
            Jmol._serverUrl = Jmol.Info["serverURL"];
            Jmol._appletNameMap = {{}};
            jmolInitialize('https://cdn.jsdelivr.net/gh/b3m2a1/jsmol-cdn@{version}/jsmol/');
        }};
        """
        unsynced_properties = ['width', 'height']
        # can_by_dynamic = False

        @classmethod
        def get_ready_flag_script(cls):
            """
            Build the JavaScript that wires up `rasterize`'s readiness
            signal, for injection into the same closure that calls
            `jmolApplet(...)` (i.e. right after `cls.patch_script`, before
            the applet itself gets created).

            JSmol/Jmol.js has no *documented* way to poll "has the applet
            rendered yet" the way X3DOM exposes `.runtime.isReady` -- the
            legacy `jmolSetCallback("AppletReadyCallback", ...)` name from
            the Jmol wiki does not actually fire for this HTML5-mode
            applet (verified against the real `JSmol.min.js`/`Jmol2.js`
            sources for the pinned `version` above: `jmolSetCallback`
            just does `Jmol.Info[callbackName] = funcName`, and the
            HTML5 applet only ever reads back `Info.readyFunction`
            (exact key, camelCase) -- `"AppletReadyCallback"` is never
            looked up at all in this build). `readyFunction` *is* read
            back, and is called with the applet object as its only
            argument once, right after the applet's own initial script
            (the `load ...` command plus anything from `load_script`,
            e.g. `animate`/`vibrate`) has been handed to the engine --
            matching the Jmol/JSmol docs' own description of when a
            "ready" callback should fire ("when the JSmol object has
            been created and is ready to receive commands").

            This sets a single page-level flag rather than trying to key
            it by applet id (contrast `X3DInterface.X3D.get_ready_check_expression`,
            which is per-scene): `rasterize()` always builds a fresh,
            single-applet page, so there is never more than one applet
            to disambiguate, and a global flag is far less fragile than
            reconstructing JSmol's internal `"jmolApplet" + targetSuffix`
            naming convention (used elsewhere in this file only for the
            *export*/*record* buttons, which read a DOM id, not this
            flag) just to filter on it.

            :return: the script fragment
            :rtype: str
            """
            return """
       window.__mcutils_jsmol_ready = false;
       jmolSetCallback('readyFunction', function(applet) {
           window.__mcutils_jsmol_ready = true;
       });
            """

        @classmethod
        def get_ready_check_expression(cls):
            """
            Build the JavaScript predicate `rasterize` polls (via
            Playwright's `wait_for_function`) to find out whether this
            applet's initial script has actually been handed to the
            JSmol engine, instead of sleeping a fixed amount of time and
            hoping it was enough. See `get_ready_flag_script` for what
            sets the flag this reads and why.

            Caveat worth knowing: this fires once JSmol's engine has
            *accepted* the applet's script, which is normally
            near-instantaneous after `readyFunction` is registered --
            but the very first time a page loads JSmol, the engine's own
            core class files still need to be fetched (lazily, on
            demand) before anything actually paints. On a slow
            connection (or a from-scratch page with nothing cached) the
            first real frame can land a little after this flag flips,
            the same way a browser can report "DOM ready" slightly
            before a slow image finishes painting. If you see an empty
            canvas in practice, pairing a larger `timeout` with a short
            fixed grace period (e.g. wrapping `rasterize`'s call and
            sleeping ~1-2s afterward before re-screenshotting) is a
            reasonable belt-and-suspenders fix; this wasn't needed in
            any case actually exercised here, so it isn't built in.

            :return: the ready-check predicate, as the body of a
                Playwright `wait_for_function` expression
            :rtype: str
            """
            return """
() => window.__mcutils_jsmol_ready === true
            """

        @classmethod
        def load_applet_script(cls, id, loader,
                               include_script_interface=False,
                               interface_target="",
                               recording_options=None,
                               target=None):
            if target is None:
                target = id
            if recording_options is None:
                recording_options = {}

            injection = "''"
            if include_script_interface:
                from ..Plots.X3DInterface import X3D

                input_tag = id + "-script-input"

                elems = []
                console = HTML.Textarea(id=input_tag, width='100%')
                elems.append(console)
                button = HTML.Button("Run Script", id=id + "-button-input",
                                onclick=f"""
                (function() {{
                    const script = document.getElementById('{input_tag}').value;
                    const app = Jmol._appletNameMap['{id}'];
                    app._script(script);
                    document.getElementById('{input_tag}').value = '';
                }})()
                """
                                )

                new_id = 'jmolApplet_' + id.split("-")[-2]
                elems.append(button)
                elems.append(
                    HTML.Div([
                        HTML.Button("Save Figure", onclick=X3D.get_export_script(new_id + '_appletdiv')),
                        HTML.Button("Record Animation", onclick=X3D.get_record_screen_script(new_id+ '_appletdiv', **recording_options)),
                        HTML.Input(value="2", id=id + '-duration-input',
                                   oninput=X3D.set_animation_duration_script(id))
                    ], style='display:flex')
                )

                strings = "\n\n".join([e.tostring() for e in elems])

                injection = f"`<div style='display:block'>\n{strings}\n</div>`"
            load_script = f"""
(function() {{
   $.getScript('{cls.jmol2_source}').then(
   () => {{
       {cls.patch_script}
       {cls.get_ready_flag_script()}
       let loaded = false;
        if (!loaded) {{
            if (typeof Jmol._appletNameMap === "undefined") {{
                Jmol._appletNameMap = {{}}
            }};
            loaded = true;
            let applet = {loader};
            applet.serverURL = Jmol.Info.serverURL;
            let wrapper = document.getElementById('{id}');
            wrapper.innerHTML = applet._code;
            Jmol._appletNameMap['{id}'] = applet;
            wrapper.ondelete = function() {{ delete Jmol._appletNameMap['{id}'] }};
            if ('{interface_target}'.length > 0) {{
                document.getElementById('{interface_target}').innerHTML = {injection};
            }}
        }}
    }})
}})();
"""
            base_script = HTML.Script(src=cls.jsmol_source,
                               onload=load_script
                               )
            return base_script

        def __init__(self, *model_etc, width=500, height=500,
                     animate=False, vibrate=False,
                     load_script=None,
                     suffix=None,
                     id=None,
                     dynamic_loading=None,
                     include_script_interface=False,
                     recording_options=None,
                     create_applet_loader=None,
                     style=None,
                     autobond=False,
                     **attrs):
            if suffix is None:
                suffix = str(uuid.uuid4())[:6].replace("-", "")
            self.suffix = suffix
            if id is None:
                id =  "jsmol-applet-" + self.suffix
            self.id = id
            if recording_options is None:
                recording_options = {}
            self.recording_options = recording_options
            if len(model_etc) > 0:
                if isinstance(model_etc[0], str):
                    model_file = model_etc[0]
                    rest = model_etc[1:]
                    if create_applet_loader is None:
                        create_applet_loader = True
                else:
                    model_file = None
                    if create_applet_loader is None:
                        create_applet_loader = False
                    rest = model_etc
            else:
                model_file = None
                if create_applet_loader is None:
                    create_applet_loader = False
                rest = model_etc
            if len(rest) == 1 and isinstance(rest[0], (list, tuple)):
                rest = rest[0]

            if load_script is None:
                load_script = []
            if isinstance(load_script, str):
                load_script = [load_script]
            load_script = list(load_script)

            if animate:
                load_script.extend(["anim mode palindrome", "anim on"])
            elif vibrate:
                load_script.append("vibration on")

            if dynamic_loading is None:
                from ..Jupyter.JHTML import JupyterAPIs
                dynamic_loading = JupyterAPIs().in_jupyter_environment()
            self.dynamic_loading = dynamic_loading

            self.load_script = load_script
            self.width, self.height = width, height
            self.model_file = model_file
            self.autobond = autobond
            if create_applet_loader:
                elems = self.create_applet(model_file, include_script_interface=include_script_interface) + list(rest)
            else:
                elems = rest
            if include_script_interface:
                height = height + 200
            if style is not None:
                if 'width' not in style:
                    style['width'] =  f'{width}px'
                if 'height' not in style:
                    style['height'] =  f'{height}px'
            else:
                attrs['width'] =  f'{width}px'
                attrs['height'] = f'{height}px'
            super().__init__(*elems, id=self.id, style=style, **attrs)

        @property
        def applet_target(self):
            return f"_{self.suffix}"
        def prep_load_script(self):
            return '; '.join(self.load_script)
        def create_applet(self, model_file, include_script_interface=False):
            targ = self.applet_target
            width, height = self.width, self.height
            load_script = self.prep_load_script()
            if model_file is None:
                load_command = f"'load {model_file};'"
            elif (
                    model_file.startswith("https://")
                    or model_file.startswith("file://")
                    or model_file.startswith("http://")
            ):
                load_command = f"'load {model_file};'"
            else:
                load_command = f"""`load DATA "inline"\n {model_file}\n END "inline";`"""
            if not self.autobond:
                load_command = "'set autobond OFF;' +" + load_command
            loader = f"""jmolApplet([{width}, {height}], {load_command} + '{load_script}', '{targ}')"""

            kill_id = "tmp-" + str(uuid.uuid4())[:10]
            if include_script_interface:
                replacement_target = self.id+'-applet'
                interface_target = self.id+'-interface'
            else:
                replacement_target = self.id
                interface_target = ""
            load_script = self.load_applet_script(replacement_target,
                                                  loader,
                                                  target=targ,
                                                  interface_target=interface_target,
                                                  recording_options=self.recording_options,
                                                  include_script_interface=include_script_interface)

            if self.dynamic_loading:
                load_script = load_script.tostring().replace("`", r"\`")
                loader = HTML.Image(
                        src='data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7',
                        id=kill_id,
                        onload=f"""
                            (function() {{
                                let killElem = document.getElementById("{kill_id}");
                                if (killElem !== null) {{
                                    killElem.remove();
                                    const frag = document.createRange().createContextualFragment(`{load_script}`);
                                    document.head.appendChild(frag);
                                }}
                            }})()"""
                    )
            else:
                loader = load_script

            if include_script_interface:
                loader = [
                    HTML.Div(loader, width='100%', height=f'{self.height}px', id=replacement_target),
                    HTML.Div(height='200px', width='100%', padding='2rem', id=interface_target)
                ]
            else:
                loader = [loader]

            return loader

        def show(self):
            return self.display()

        jquery_source = "https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.min.js"

        def to_html(self, *base_elems, header_elems=None, **header_info):
            """
            Wrap the applet in a full standalone HTML document (head +
            body), the way `X3DInterface.X3D.to_html` does for X3D
            scenes. This applet's own markup already embeds its
            `<script>` tag(s) (added in `create_applet`, either directly
            or via the `dynamic_loading` image-onload trick); the one
            thing a bare `self.write(...)` wouldn't give this page is
            jQuery, which `load_applet_script`'s loader unconditionally
            needs (`$.getScript(...)`) but which this codebase otherwise
            just assumes is already on the page (true inside a Jupyter
            notebook, not true of a blank page opened directly) -- so
            this always includes it, ahead of the applet itself, unless
            `header_elems` already supplies one.

            :param base_elems: extra body elements
            :param header_elems: extra head elements; if none of them
                looks like a jQuery `<script>` tag already, one is
                prepended for you
            :type header_elems: list | None
            :param header_info: extra head attributes
            :return: the HTML document
            """
            header_elems = list(header_elems) if header_elems is not None else []
            if not any(
                    getattr(e, 'tag', None) == 'script'
                    and 'jquery' in str(e.attrs.get('src', '')).lower()
                    for e in header_elems
            ):
                header_elems = [HTML.Script(src=self.jquery_source)] + header_elems
            return HTML.Html(
                HTML.Head(
                    *header_elems,
                    **header_info
                ),
                HTML.Body(*base_elems, self),
                id=self.id
            )

        def dump(self, file, write_html=True, **opts):
            """
            Write the applet to a file, as a full standalone HTML page or
            as its own bare markup (mirroring `X3DInterface.X3D.dump`).

            :param file: the destination file
            :param write_html: write a full HTML document (vs. just this
                applet's own markup, which on its own is missing jQuery
                and so won't load standalone -- only useful for embedding
                into a page that already has it)
            :type write_html: bool
            :param opts: extra write options
            :return: the write result
            """
            html = self.to_html() if write_html else self
            return html.write(file, **opts)

        def rasterize(self, file=None, image_format='png', width=None, height=None,
                      device_scale_factor=1,
                      background=None, transparent=None,
                      timeout=15000, executable_path=None, channel=None,
                      browser_args=None, keep_html=False,
                      ready_timeout_action='warn'):
            """
            Render this applet to a raster image, the same way
            `X3DInterface.X3D.rasterize` does for X3D scenes: build the
            standalone page this applet needs (jQuery plus a margin
            reset and optional background) and hand the actual
            headless-browser work off to that page's own
            `HTML.XMLElement.rasterize`, passing this applet's own
            "has my script actually been handed to JSmol yet" check
            (`get_ready_check_expression`) as its `ready_function`, and
            the `<canvas>` JSmol renders onto (not the wrapper div, or
            the whole page/viewport) as what to screenshot.

            :param file: destination; a path, a writable/bytes-like
                buffer (e.g. `io.BytesIO()`), or `None` to get a new
                `io.BytesIO` back
            :param image_format: `"png"` or `"jpg"`/`"jpeg"`
            :type image_format: str
            :param width: viewport width; defaults to this applet's own
                configured `width`
            :param height: viewport height; defaults to this applet's
                own configured `height`
            :param device_scale_factor: forwarded to Playwright's
                `new_page` (a page rendered at `device_scale_factor=2`
                and screenshotted gives a 2x-resolution image at the
                same CSS size -- the same trick `X3DFigure.savefig` uses
                for its `dpi` option)
            :param background: an HTML background color for the page
                before the applet loads (mostly invisible once JSmol's
                own canvas covers it)
            :param transparent: if truthy, take the screenshot with
                `omit_background=True`
            :param timeout: milliseconds to wait for the ready signal
                before giving up and capturing whatever is currently
                rendered
            :type timeout: int
            :param executable_path: forwarded to `resolve_chromium_launch_kwargs`
            :param channel: forwarded to `resolve_chromium_launch_kwargs`
            :param browser_args: extra Chromium command-line flags;
                defaults to `DEFAULT_RASTERIZE_ARGS`
            :param keep_html: if truthy, don't delete the intermediate
                HTML file/directory (useful for debugging what got
                rendered)
            :type keep_html: bool
            :param ready_timeout_action: `"warn"` (default), `"raise"`,
                or `"ignore"` -- what to do if the ready signal doesn't
                fire within `timeout`
            :type ready_timeout_action: str
            :return: `file` if given (the path or buffer passed in),
                otherwise a new `io.BytesIO` holding the image
            """
            def _px(v):
                if isinstance(v, str):
                    v = float(v.rstrip('px').strip())
                return int(round(v))

            if width is None:
                width = self.width
            if height is None:
                height = self.height
            width = _px(width)
            height = _px(height)

            header_elems = [HTML.Style("html, body { margin:0; padding:0; }")]
            if background is not None:
                header_elems.append(HTML.Style(f"html, body {{ background:{background}; }}"))

            html = self.to_html(header_elems=header_elems)

            return html.rasterize(
                file,
                width=width, height=height, device_scale_factor=device_scale_factor,
                ready_function=self.get_ready_check_expression(),
                screenshot_selector=f"#{self.id} canvas",
                image_format=image_format, transparent=transparent, timeout=timeout,
                executable_path=executable_path, channel=channel, browser_args=browser_args,
                keep_html=keep_html, ready_timeout_action=ready_timeout_action,
            )

        raster_formats = {'png', 'jpg', 'jpeg'}
        def savefig(self, file, format=None,
                    dpi=144, facecolor=None, transparent=None,
                    rasterize_options=None,
                    **opts):
            """
            Save the applet to a file, mirroring
            `Backends.X3DFigure.savefig`'s dispatch: vector/markup
            formats (the default, or an explicit `format="html"`) are
            written directly via `dump`; raster formats (`png`,
            `jpg`/`jpeg`, inferred from `file`'s extension when `format`
            is left as `None`) instead render the applet in a headless
            browser and screenshot it (see `rasterize`).

            `dpi` is converted to a `device_scale_factor` the same way
            `X3DFigure.savefig` does, so `savefig(..., dpi=288)` renders
            at 2x pixel density without changing the applet's own
            configured (CSS) size.

            :param format: `"png"`/`"jpg"`/`"jpeg"` to rasterize, or a
                markup format (`"html"`) to hand off to `dump`; inferred
                from `file`'s extension when omitted
            :param dpi: only used when rasterizing; converted to
                `rasterize`'s `device_scale_factor` as `dpi / 72`
            :param facecolor: background color to use when rasterizing,
                forwarded to `rasterize` as `background`
            :param transparent: if rasterizing, try to omit the
                page/browser background so the export can come out with
                an alpha channel
            :param rasterize_options: extra keyword options forwarded to
                `rasterize` (`timeout`, `executable_path`, `channel`,
                `browser_args`, `keep_html`, `ready_timeout_action`, ...)
            :param opts: extra options forwarded to `dump` when not
                rasterizing (e.g. `write_html=False`)
            """
            import os

            fmt = format
            if fmt is None and isinstance(file, str):
                fmt = os.path.splitext(file)[1].lstrip('.')
            if fmt is not None and fmt.lower() in self.raster_formats:
                return self.rasterize(
                    file,
                    image_format=fmt.lower(),
                    background=facecolor,
                    transparent=transparent,
                    device_scale_factor=(dpi / 72 if dpi is not None else 1),
                    **(rasterize_options if rasterize_options is not None else {})
                )
            else:
                return self.dump(file, **opts)
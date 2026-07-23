from __future__ import annotations

import abc
import collections
import uuid
import numpy as np
import os
import json

from .. import Devutils as dev
from ..Jupyter import JHTML, X3DHTML
from .. import Numputils as nput

__all__ = [
    "X3D",
    "X3DPrimitive",
    "X3DGeometryObject",
    "X3DGeometryGroup",
    "X3DGroup",
    "X3DScene",
    "X3DBackground",
    "X3DMaterial",
    "X3DLine",
    "X3DSphere",
    "X3DCone",
    "X3DBox",
    "X3DCylinder",
    "X3DCappedCylinder",
    "X3DArrow",
    "X3DTorus",
    "X3DRectangle2D",
    "X3DDisk2D",
    "X3DCircle2D",
    "X3DPolyline2D",
    "X3DTriangleSet",
    "X3DIndexedTriangleSet",
    "X3DIndexedLineSet",
    "X3DSwitch",
    "X3DListAnimator",
    "X3DInterpolatingAnimator"
]

#TODO: cache these resources or put them on a path that is accessible by Jupyter
#      might be pretty simple depending on what resource paths Jupyter naturally exposes

class X3DObject(metaclass=abc.ABCMeta):
    id: str
    @abc.abstractmethod
    def to_x3d(self) -> X3DHTML.X3DElement:
        """
        **LLM Docstring**

        Abstract: render this object to its X3D DOM element.

        :return: the X3D element
        """
        ...

    def get_interpolated_attributes(self):
        """
        **LLM Docstring**

        Return the object's attributes used when building animation frames (its X3D element's attrs).

        :return: the attribute dict
        :rtype: dict
        """
        return self.to_x3d().attrs
    def get_children(self):
        """
        **LLM Docstring**

        Return the object's child objects (none by default).

        :return: the children
        :rtype: list
        """
        return []

    @classmethod
    def get_new_id(cls):
        """
        **LLM Docstring**

        Generate a fresh unique id for a new object.

        :return: the id
        :rtype: str
        """
        return str(uuid.uuid4())[:6]

    def resolve_prop_attr(self, prop_name):
        """
        **LLM Docstring**

        Map a property name to the X3D attribute name it animates (identity by default).

        :param prop_name: the property name
        :return: the attribute name
        """
        return prop_name
    def prep_animation_values(self, prop_name, values):
        """
        **LLM Docstring**

        Normalize a property's per-frame animation values (e.g. defaulting `transparency` gaps to 0).

        :param prop_name: the property name
        :param values: the per-frame values
        :return: the normalized values
        """
        if prop_name == 'transparency':
            values = [v if v is not None else 0 for v in values]
        return values
    def get_prop_node_id(self, prop_name):
        """
        **LLM Docstring**

        Return the id of the DOM node that carries a given animated property (this object by default).

        :param prop_name: the property name
        :return: the node id
        :rtype: str
        """
        return self.id

class X3D(X3DObject):
    defaults = dict(
        width=500,
        height=500
    )
    @classmethod
    def get_new_id(cls):
        """
        **LLM Docstring**

        Generate a fresh `x3d-`-prefixed id.

        :return: the id
        :rtype: str
        """
        return "x3d-" + str(uuid.uuid4())[:6]
    def __init__(self, *children, id=None, dynamic_loading=True,
                 x3dom_path=None,
                 x3dom_css_path=None,
                 include_mathjax=False,
                 recording_options=None,
                 include_export_button=False,
                 include_record_button=False,
                 include_view_settings_button=False,
                 preload_scripts=None,
                 onload_scripts=None,
                 **opts):
        """
        **LLM Docstring**

        Set up the top-level X3D scene container: its children, size, resource paths, and
        the optional export/record/view-settings UI and MathJax/loader scripting.

        :param children: the scene's child objects
        :param id: the DOM id (auto-generated if omitted)
        :param dynamic_loading: load the X3DOM runtime dynamically
        :type dynamic_loading: bool
        :param x3dom_path: an override path/URL for the X3DOM JS
        :param x3dom_css_path: an override path/URL for the X3DOM CSS
        :param include_mathjax: include MathJax for text rendering
        :type include_mathjax: bool
        :param recording_options: options for the screen recorder
        :type recording_options: dict | None
        :param include_export_button: include the image-export button
        :type include_export_button: bool
        :param include_record_button: include the screen-record button
        :type include_record_button: bool
        :param include_view_settings_button: include the view-settings button
        :type include_view_settings_button: bool
        :param preload_scripts: scripts to run before the scene loads
        :param onload_scripts: scripts to run once the scene loads
        :param opts: extra scene options (e.g. width/height)
        """
        if len(children) == 1 and isinstance(children[0], (tuple, list)):
            children = children[0]
        self.children = children
        self.opts = opts
        if id is None:
            id = self.get_new_id()
        self.id = id
        self.dynamic_loading = dynamic_loading
        if recording_options is None:
            recording_options = {}
        self.recording_options = recording_options
        self.include_export_button =include_export_button
        self.include_record_button = include_record_button
        self.include_view_settings_button =include_view_settings_button
        if x3dom_path is not None:
            if dev.str_is(x3dom_path, 'local') and not os.path.isfile('local'):
                # get the relative path
                x3dom_path = 'file://' + os.path.join(
                    os.path.dirname(os.path.dirname(__file__)),
                    'Jupyter', 'resources', 'x3dom-full.js'
                )
            self.X3DOM_JS = x3dom_path
        if x3dom_css_path is not None:
            self.X3DOM_CSS = x3dom_css_path
        self.include_mathjax = include_mathjax
        self.preload_scripts = preload_scripts
        self.onload_scripts = onload_scripts
        self._widg = None

    X3DOM_JS = 'https://www.x3dom.org/download/1.8.3/x3dom-full.js'
    X3DOM_CSS = 'https://www.x3dom.org/download/x3dom.css'
    MATHJAX_CDN = 'https://cdn.jsdelivr.net/npm/mathjax@4/tex-svg.js'

    @classmethod
    def get_export_script(self, id):
        """
        **LLM Docstring**

        Build the JavaScript that exports the scene canvas to a PNG and triggers a download.

        :param id: the scene DOM id
        :type id: str
        :return: the export script
        :rtype: str
        """
        return f"""
(function(){{
  let link = document.createElement('a');
  let base_name = '{id}';
  link.download = base_name + '.png';
  link.href = document.getElementById('{id}').getElementsByTagName('canvas')[0].toDataURL()
  link.click();
}})()
       """

    @classmethod
    def get_view_settings_script(self, id):
        """
        **LLM Docstring**

        Build the JavaScript that reads the current view matrix and writes it into the view-matrix output field.

        :param id: the scene DOM id
        :type id: str
        :return: the script
        :rtype: str
        """
        return f"""
    (function(){{
        let fig = document.getElementById('{id}');
        let x3d = fig.getElementsByTagName("x3d")[0];
        let vmObj = x3d.runtime.viewMatrix();
        let vmA = [
            [vmObj["_00"], vmObj["_01"], vmObj["_02"], vmObj["_03"]],
            [vmObj["_10"], vmObj["_11"], vmObj["_12"], vmObj["_13"]],
            [vmObj["_20"], vmObj["_21"], vmObj["_22"], vmObj["_23"]],
            [vmObj["_30"], vmObj["_31"], vmObj["_32"], vmObj["_33"]]
        ];
        let out = document.getElementById('{id}-view-matrix');
        out.value = JSON.stringify(vmA, 1);
    }})()
           """

    @classmethod
    def parse_view_matrix(cls, vs):
        """
        **LLM Docstring**

        Convert a serialized X3DOM view matrix into `{position, orientation}` viewpoint
        options (inverting the matrix and extracting the rotation angle/axis).

        :param vs: the view matrix (JSON string or array)
        :return: the viewpoint options
        :rtype: dict
        """
        import json
        if isinstance(vs, str):
            vs = json.loads(vs)
        vm = np.linalg.inv(vs)
        ang, ax = nput.extract_rotation_angle_axis(vm[:3, :3])
        v_pos = vm[:3, -1].tolist()
        v_ort = np.array(list(ax) + [ang]).tolist()
        opts = {"position": v_pos, "orientation": v_ort}
        return opts

    @classmethod
    def get_record_screen_script(self, id, polling_rate=30, recording_duration=2, video_format='video/webm'):
        """
        **LLM Docstring**

        Build the JavaScript that records the scene canvas to a video and triggers a download.

        :param id: the scene DOM id
        :type id: str
        :param polling_rate: the capture frame rate
        :type polling_rate: int
        :param recording_duration: the recording length in seconds
        :type recording_duration: float
        :param video_format: the recording MIME type
        :type video_format: str
        :return: the recording script
        :rtype: str
        """
        return f"""
    (function(){{
        let canvas = document.getElementById('{id}').getElementsByTagName('canvas')[0];
        
        let pollingRate = (typeof canvas.pollingRate === 'undefined') ? {polling_rate} : canvas.pollingRate;
        let videoFormat = (typeof canvas.videoFormat === 'undefined') ? "{video_format}" : canvas.videoFormat;
        let videoExtension = canvas.videoExtension;
        if (typeof canvas.videoExtension === 'undefined') {{
            videoExtension = ''
        }}
        let x3DRecordingStream = canvas.captureStream(pollingRate);
        let mediaRecorder = new MediaRecorder(x3DRecordingStream, {{mimeType: videoFormat}});
        
        mediaRecorder.frames = [];
        mediaRecorder.ondataavailable = function(e) {{
          mediaRecorder.frames.push(e.data);
        }};
        
        mediaRecorder.onstop = function(e) {{
          link = document.createElement('a');
          const base_name = '{id}';
          const blob = mediaRecorder.frames[0];
          link.download = base_name + videoExtension;
          console.log(blob);
          const blobURL = window.URL.createObjectURL(blob);
          link.href = blobURL;
          console.log(blobURL);
          mediaRecorder.frames = [];
          link.click();
        }};
        
        let duration = (typeof canvas.recordingDuration === 'undefined') ? {recording_duration} : canvas.recordingDuration;
        setTimeout(() => {{mediaRecorder.stop()}}, duration * 1000);
        mediaRecorder.start()
    }})()
           """
    @classmethod
    def set_animation_duration_script(self, id):
        """
        **LLM Docstring**

        Build the JavaScript that reads the duration input and stores it on the canvas.

        :param id: the scene DOM id
        :type id: str
        :return: the script
        :rtype: str
        """
        return f"""
    (function(){{
        let canvas = document.getElementById('{id}').getElementsByTagName('canvas')[0];
        let input = document.getElementById('{id}-duration-input');
        
        canvas.recordingDuration = input.value;
    }})()
           """

    @classmethod
    def _create_loader_fragment(cls, i, s):
        """
        **LLM Docstring**

        Build a JavaScript fragment that dynamically injects a preload/onload script or
        library (handling variable capture/restore around the load).

        :param i: the fragment index
        :type i: int
        :param s: the loader spec (a `{lib: callback}` dict, a raw string, or an element)
        :return: the loader fragment
        :rtype: str
        """
        if isinstance(s, dict):
            lib, callback = list(s.items())[0]
            if not isinstance(lib, str):
                var, lib = lib
                if isinstance(var, str):
                    return f'''
try {{
    window._vcontext{i} = {var};
    delete {var};
}} catch (e) {{}}
const frag{i} = document.createElement('script');
frag{i}.src='{lib}';
frag{i}.onload=function() {{window._vcontext{i}; {callback}; var {var} = window._vcontext{i};}};
document.head.append(frag{i});
'''
                else:
                    var, target = var
                    return f'''
try {{
    window._vcontext{i} = {var};
    delete {var};
}} catch (e) {{}}
const frag{i} = document.createElement('script');
frag{i}.src='{lib}';
frag{i}.onload=function() {{let {target} = {var}; {callback}; {var} = window._vcontext{i};}};
document.head.append(frag{i});
'''
            else:
                return f'''
const frag{i} = document.createElement('script');
frag{i}.src='{lib}';
frag{i}.onload=function() {{{callback}}};
document.head.append(frag{i});
'''
        elif isinstance(s, str):
            return f'''(function() {{ {s} }})()'''
        else:
            return f'''const frag{i} = document.createRange().createContextualFragment(`{s.tostring()}`); document.head.appendChild(frag{i});'''

    def to_widget(self,
                  dynamic_loading=None,
                  include_export_button=None,
                  include_record_button=None,
                  include_view_settings_button=None
                  ):
        """
        **LLM Docstring**

        Render the scene to an interactive X3DOM widget (cached), wiring up the loader
        scripts and any export/record/view-settings UI.

        :param dynamic_loading: load the runtime dynamically
        :type dynamic_loading: bool | None
        :param include_export_button: include the export button
        :type include_export_button: bool | None
        :param include_record_button: include the record button
        :type include_record_button: bool | None
        :param include_view_settings_button: include the view-settings button
        :type include_view_settings_button: bool | None
        :return: the widget
        """
        if self._widg is not None:
            return self._widg
        id = self.id
        x3d_embed = self.to_x3d()#.tostring()


        if dynamic_loading is None:
            dynamic_loading = self.dynamic_loading
        if include_export_button is None:
            include_export_button = self.include_export_button
        if include_record_button is None:
            include_record_button = self.include_record_button
        if include_view_settings_button is None:
            include_view_settings_button = self.include_view_settings_button

        if not dynamic_loading:
            elems = [
                JHTML.Link(rel='stylesheet', href=self.X3DOM_CSS),
                JHTML.Script(src=self.X3DOM_JS)
            ]
            if self.include_mathjax:
                elems.append(JHTML.Script(src=self.MATHJAX_CDN))
            if self.preload_scripts is not None:
                elems.extend(
                    JHTML.Script(s) if isinstance(s, str) else s for s in self.preload_scripts
                )
            base_fig = JHTML.Div(
                *elems,
                x3d_embed,
                id=id,
                width=x3d_embed['width'],
                height=x3d_embed['height'],
                can_be_dynamic=False
            )
        else:
            JHTML.Link(rel='stylesheet', href=self.X3DOM_CSS),
            load_scripts = [
                JHTML.Script(src=self.X3DOM_JS)
            ]
            if self.include_mathjax:
                load_scripts.append(JHTML.Script(src=self.MATHJAX_CDN))
            if self.preload_scripts is not None:
                load_scripts.extend(
                    JHTML.Script(s) if isinstance(s, str) else s for s in self.preload_scripts
                )
            loader_frags = "\n".join([
                f'''
                const frag{i} = document.createRange().createContextualFragment(`{load_script.tostring()}`);
                document.head.appendChild(frag{i});'''
                for i,load_script in enumerate(load_scripts)
            ])
            kill_id = "tmp-"+str(uuid.uuid4())[:10]
            base_fig = JHTML.Figure(
                # JHTML.Link(rel='stylesheet', href=self.X3DOM_CSS),
                x3d_embed,
                JHTML.Image(
                    src='data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7',
                    id=kill_id,
                    onload=f"""
                    (function() {{
                        let killElem = document.getElementById('{kill_id}');
                        if (killElem !== null) {{
                            killElem.remove();
                            {loader_frags}
                        }}
                    }})()"""
                    ),
                id=id,
                width=x3d_embed['width'],
                height=x3d_embed['height'],
                can_be_dynamic=False
            )

        elems = [base_fig]
        if include_export_button:
            elems.append(JHTML.Button("Save Figure", onclick=self.get_export_script(self.id)))
        if include_record_button:
            elems.extend([
                JHTML.Button("Record Animation", onclick=self.get_record_screen_script(self.id, **self.recording_options)),
                JHTML.Input(value=str(self.recording_options.get('recording_duration', 2)),
                            id=self.id+'-duration-input', width="50px", oninput=self.set_animation_duration_script(self.id))
            ])
        if include_view_settings_button:
            elems.append(
                JHTML.Div(
                    [
                        JHTML.Button("Show View Matrix", onclick=self.get_view_settings_script(self.id)),
                        JHTML.Textarea(id=self.id + '-view-matrix')
                    ],
                    display="block"
                )
            )

        if self.onload_scripts is not None and len(self.onload_scripts) > 0:
            loader_frags = "\n".join([
                self._create_loader_fragment(i, load_script)
                for i, load_script in enumerate(self.onload_scripts)
            ])
            kill_id = "tmp-loader-"+str(uuid.uuid4())[:10]
            elems.append(
                JHTML.Image(
                    src='data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7',
                    id=kill_id,
                    onload=f"""
                                (function() {{
                                    let killElem = document.getElementById('{kill_id}');
                                    if (killElem !== null) {{
                                        killElem.remove();
                                        {loader_frags}
                                    }}
                                }})()"""
                )
            )

        if len(elems) > 1:
            self._widg = JHTML.Div(
                *elems
            )
        else:
            self._widg = elems[0]

        return self._widg

    def to_html(self, *base_elems, header_elems=None,
                dynamic_loading=False,
                include_export_button=None,
                include_record_button=None,
                **header_info):
        """
        **LLM Docstring**

        Wrap the scene widget in a full HTML document (with the X3DOM CSS/JS in the head).

        :param base_elems: extra body elements
        :param header_elems: extra head elements
        :type header_elems: list | None
        :param dynamic_loading: load the runtime dynamically
        :type dynamic_loading: bool
        :param include_export_button: include the export button
        :type include_export_button: bool | None
        :param include_record_button: include the record button
        :type include_record_button: bool | None
        :param header_info: extra head attributes
        :return: the HTML document
        """
        id = self.id
        x3d_embed = self.to_widget(
            dynamic_loading=dynamic_loading,
            include_export_button=include_export_button,
            include_record_button=include_record_button
        )  # .tostring()

        return JHTML.Html(
            JHTML.Head(
                *(header_elems if header_elems is not None else []),
                JHTML.Link(rel='stylesheet', href=self.X3DOM_CSS),
                JHTML.Script(src=self.X3DOM_JS),
                **header_info
            ),
            JHTML.Body(
                *base_elems,
                x3d_embed
            ),
            id=id
        )

    def _ipython_display_(self):
        """
        **LLM Docstring**

        Display the scene widget in IPython.
        """
        return self.to_widget()._ipython_display_()
    def get_mime_bundle(self):
        """
        **LLM Docstring**

        Return the scene widget's MIME bundle for rich display.

        :return: the MIME bundle
        :rtype: dict
        """
        return self.to_widget().get_mime_bundle()
    def to_x3d(self):
        """
        **LLM Docstring**

        Render the scene to its `<x3d>` DOM element, formatting the size and rendering each child.

        :return: the X3D element
        """
        base_opts = dict(self.defaults, **self.opts)
        for k in ['width', 'height']:
            if k in base_opts:
                v = base_opts[k]
                if nput.is_numeric(v):
                    base_opts[k] = f'{v:.0f}px'
        return X3DHTML.X3D(
            JHTML.HTML.Head(),
            *[a.to_x3d() if hasattr(a, 'to_x3d') else a for a in self.children],
            **base_opts
        )
    def display(self):
        """
        **LLM Docstring**

        Display the scene widget.
        """
        return self.to_widget().display()

    def show(self):
        """
        **LLM Docstring**

        Display the scene, enabling dynamic loading when in a Jupyter environment.
        """
        from ..Jupyter.JHTML import JupyterAPIs
        dynamic_loading = JupyterAPIs().in_jupyter_environment()
        self.to_widget(dynamic_loading=dynamic_loading).display()

    def dump(self, file, write_html=True, **opts):
        """
        **LLM Docstring**

        Write the scene to a file, as full HTML or as bare X3D.

        :param file: the destination file
        :param write_html: write full HTML (vs bare X3D)
        :type write_html: bool
        :param opts: extra write options
        :return: the write result
        """
        if write_html:
            html = self.to_html()
        else:
            html = self.to_x3d()
        return html.write(file, **opts)

    def get_children(self):
        """
        **LLM Docstring**

        Return the scene's child objects.

        :return: the children
        :rtype: list
        """
        return self.children

class X3DOptionsSet(X3DObject):
    __props__ = {}

    @classmethod
    def parse_color(cls, color):
        """
        **LLM Docstring**

        Parse a color specification into `(color, transparency)`, resolving named colors /
        hex codes into normalized `[0, 1]` components and splitting off an alpha channel.

        :param color: the color specification
        :return: `(color_components, transparency_or_None)`
        :rtype: tuple
        """
        if isinstance(color, (list, tuple, np.ndarray)) and all(isinstance(c, str) for c in color):
            color = " ".join(color)
        if isinstance(color, str):
            if color == 'transparent':
                color = '#' + 'F'*8
            try:
                _ = [float(s) for s in color.split()]
            except ValueError:
                from .Colors import ColorPalette

                bits = []
                for c in color.split():
                    if c.startswith('#'):
                        c = ColorPalette.parse_rgb_code(c)
                    else:
                        c = np.array(ColorPalette.parse_color_string(c))
                    bit_bits = np.array(c) / 255
                    bits.extend(bit_bits)

            else:
                bits = _
        else:
            bits = color
        if len(bits) > 3:
            color = bits[:-1]
            transparency = bits[-1]
        else:
            color = bits
            transparency = None

        return color, transparency

    @classmethod
    def get_new_id(cls):
        """
        **LLM Docstring**

        Generate a fresh `x3d-opts-`-prefixed id.

        :return: the id
        :rtype: str
        """
        return "x3d-opts-" + str(uuid.uuid4())[:6]
    def __init__(self, id=None, **attrs):
        """
        **LLM Docstring**

        Hold a set of X3D node attributes under an id.

        :param id: the node id (auto-generated if omitted)
        :param attrs: the node attributes
        """
        if id is None:
            id = self.get_new_id()
        self.id = id
        self.attrs = attrs

    conversion_map = {}
    @classmethod
    def prop_keys(cls):
        """
        **LLM Docstring**

        Return the set of valid property keys (declared props plus conversion-map aliases).

        :return: the valid keys
        :rtype: set
        """
        return (cls.__props__ | cls.conversion_map.keys())
    def prep_attrs(self, attrs:dict):
        """
        **LLM Docstring**

        Canonicalize the node attributes (applying the conversion-map aliases and attaching the id), validating against the declared props.

        :param attrs: the attributes
        :type attrs: dict
        :return: the canonicalized attributes
        :rtype: dict
        :raises ValueError: for invalid attribute keys
        """
        attrs = {
            self.conversion_map.get(k, k):v
            for k,v in attrs.items()
        }
        excess_keys = attrs.keys() - self.__props__
        if len(excess_keys) > 0:
            cls = type(self).__name__
            raise ValueError(f"keys {excess_keys} are invalid keys for {cls}")
        attrs['id'] = self.id
        return attrs

    @classmethod
    def resolve_prop_attr(self, prop_name):
        """
        **LLM Docstring**

        Map a property name to its X3D attribute name via the conversion map.

        :param prop_name: the property name
        :return: the attribute name
        """
        return self.conversion_map.get(prop_name, prop_name)

    def get_prop_node_id(self, prop_name):
        """
        **LLM Docstring**

        Return the node id carrying a given property (this node).

        :param prop_name: the property name
        :return: the node id
        :rtype: str
        """
        return self.id

class X3DMaterial(X3DOptionsSet):
    __props__ = {
        "diffuseColor",
        "ambientIntensity",
        "emissiveColor",
        "specularColor",
        "shininess",
        "transparency",
        # "metadata"
    }
    conversion_map = {
        "brightness": "ambientIntensity",
        "glow": "emissiveColor",
        "color": "diffuseColor",
        "specularity": "specularColor"
    }
    def prep_attrs(self, attrs:dict):
        """
        **LLM Docstring**

        Canonicalize the material attributes (resolving the color into components/transparency) before rendering.

        :param attrs: the attributes
        :type attrs: dict
        :return: the canonicalized attributes
        :rtype: dict
        """
        if attrs.get('color') is not None:
            new_attrs = attrs.copy()
            color, transparency = self.parse_color(attrs['color'])
            new_attrs['color'] = color
            if transparency is not None:
                new_attrs['transparency'] = transparency
        else:
            new_attrs = attrs
        return super().prep_attrs(new_attrs)
    def to_x3d(self):
        """
        **LLM Docstring**

        Render the material to its X3D DOM element.

        :return: the X3D element
        """
        return X3DHTML.Material(**self.prep_attrs(self.attrs))

class X3DTexture(X3DOptionsSet):
    __props__ = {
        "url",
        "image",
        "crossOrigin",
        "hideChildren",
        "metadata",
        "repeatS",
        "repeatT",
        "scale",
        "textureProperties",
        "texture_type"
    }
    conversion_map = {
    }
    # def prep_attrs(self, attrs: dict):
    #     if 'color' in attrs:
    #         new_attrs = attrs.copy()
    #         color, transparency = self.parse_color(attrs['color'])
    #         new_attrs['color'] = color
    #         if transparency is not None:
    #             new_attrs['transparency'] = transparency
    #     else:
    #         new_attrs = attrs
    #     return super().prep_attrs(new_attrs)
    texture_type_mapping = {
        "pixel":X3DHTML.PixelTexture,
        "image":X3DHTML.ImageTexture,
        "movie":X3DHTML.MovieTexture
    }
    movie_types = ['.mp4', '.webm']
    @classmethod
    def infer_texture_type(self, ats):
        """
        **LLM Docstring**

        Infer the texture type (pixel/image/movie) from the supplied attributes.

        :param ats: the texture attributes
        :type ats: dict
        :return: the texture type name
        :rtype: str
        """
        if "image" in ats:
            return "pixel"
        elif "loop" in ats or any(ats['url'].endswith(mt) for mt in self.movie_types):
            return "movie"
        else:
            return "image"
    def to_x3d(self):
        """
        **LLM Docstring**

        Render the texture to its X3D DOM element, dispatching on the (inferred) texture type.

        :return: the X3D element
        """
        ats = self.prep_attrs(self.attrs)
        texture_type = ats.pop('texture_type', None)
        if texture_type is None:
            texture_type = self.infer_texture_type(ats)
        if isinstance(texture_type, str):
            texture_type = self.texture_type_mapping[texture_type]
        texture_type:X3DHTML.Texture|X3DHTML.MovieTexture|X3DHTML.PixelTexture|X3DHTML.ImageTexture
        return texture_type(**ats)

class X3DAppearance(X3DOptionsSet):
    __props__ = {
        "alphaClipThreshold",
        "blendMode",
        "colorMaskMode"
        "depthMode"
        "lineProperties"
        "material"
        "metadata"
        "pointProperties"
        "shaders",
        "sortKey",
        "sortType",
        "texture",
        "textureTransform"
    }
    @classmethod
    def get_new_id(cls):
        """
        **LLM Docstring**

        Generate a fresh appearance id.

        :return: the id
        :rtype: str
        """
        return "x3d-appearance-" + str(uuid.uuid4())[:6]
    def prep_attrs(self, attrs:dict):
        """
        **LLM Docstring**

        Canonicalize the appearance attributes, splitting the material/texture/line/point sub-properties out into their own nodes.

        :param attrs: the attributes
        :type attrs: dict
        :return: the canonicalized attributes
        :rtype: dict
        """
        material_keys = attrs.keys() & X3DMaterial.prop_keys()
        line_keys = attrs.keys() & X3DLineProperties.prop_keys()
        point_keys = attrs.keys() & X3DPointProperties.prop_keys()

        rem_keys = attrs.keys() - (
            X3DMaterial.prop_keys()
            | X3DLineProperties.prop_keys()
            | X3DPointProperties.prop_keys()
        )
        base_attrs = {k:attrs[k] for k in rem_keys}

        if len(material_keys) > 0:
            base_attrs['material'] = {k:attrs[k] for k in material_keys}

        if len(line_keys) > 0:
            base_attrs['lineProperties'] = {k:attrs[k] for k in line_keys}

        if len(point_keys) > 0:
            base_attrs['pointProperties'] = {k:attrs[k] for k in point_keys}

        return base_attrs
    def to_x3d(self):
        """
        **LLM Docstring**

        Render the appearance to its X3D DOM element (with its material/texture/line/point child nodes).

        :return: the X3D element
        """
        base_attrs = self.prep_attrs(self.attrs)

        comps = []
        line_props = base_attrs.pop('lineProperties', None)
        if line_props is not None:
            if isinstance(line_props, dict):
                line_props = X3DLineProperties(id=self.id+'-lineprops', **line_props)
            if isinstance(line_props, X3DLineProperties):
                line_props = line_props.to_x3d()
            comps.append(line_props)

        point_props = base_attrs.pop('pointProperties', None)
        if point_props is not None:
            if isinstance(point_props, dict):
                point_props = X3DPointProperties(id=self.id+'-pointprops', **point_props)
            if isinstance(point_props, X3DPointProperties):
                point_props = point_props.to_x3d()
            comps.append(point_props)

        texture_props = base_attrs.pop('texture', None)
        if texture_props is not None:
            if isinstance(texture_props, str):
                texture_props = {'url':texture_props}
            if isinstance(texture_props, dict):
                texture_props = X3DTexture(id=self.id+'-texture', **texture_props)
            if isinstance(texture_props, X3DTexture):
                texture_props = texture_props.to_x3d()
            comps.append(texture_props)

        material_props = base_attrs.pop('material', None)
        if material_props is not None:
            if isinstance(material_props, dict):
                material_props = X3DMaterial(id=self.id+'-material', **material_props)
            if isinstance(material_props, X3DMaterial):
                material_props = material_props.to_x3d()
            comps.append(material_props)

        return X3DHTML.Appearance(*comps, **base_attrs)

    @classmethod
    def resolve_prop_attr(self, prop_name):
        """
        **LLM Docstring**

        Map a property name to the appearance sub-node attribute it animates.

        :param prop_name: the property name
        :return: the attribute name
        """
        if prop_name in X3DAppearance.prop_keys():
            return self.conversion_map.get(prop_name, prop_name)
        elif prop_name in X3DLineProperties.prop_keys():
            return X3DLineProperties.conversion_map.get(prop_name, prop_name)
        elif prop_name in X3DLineProperties.prop_keys():
            return X3DLineProperties.conversion_map.get(prop_name, prop_name)
        elif prop_name in X3DMaterial.prop_keys():
            return X3DMaterial.conversion_map.get(prop_name, prop_name)
        else:
            raise ValueError(f"property {prop_name} not known")

    def get_prop_node_id(self, prop_name):
        """
        **LLM Docstring**

        Return the id of the appearance sub-node (material/texture/...) carrying a property.

        :param prop_name: the property name
        :return: the node id
        :rtype: str
        """
        if prop_name in X3DAppearance.prop_keys():
            return self.id
        elif prop_name in X3DLineProperties.prop_keys():
            return self.id+'-lineprops'
        elif prop_name in X3DLineProperties.prop_keys():
            return self.id+'-pointprops'
        elif prop_name in X3DMaterial.prop_keys():
            return self.id+'-material'
        else:
            raise ValueError(f"property {prop_name} not known")

class X3DLineProperties(X3DOptionsSet):
    __props__ = {
        "applied",
        "linetype",
        "linewidth",
        "linewidthScaleFactor"
    }
    conversion_map = {
        "line_style":"linetype",
        "line_thickness":"linewidth"
    }
    def prep_attrs(self, attrs:dict):
        """
        **LLM Docstring**

        Canonicalize the line-properties attributes (resolving the color into components/transparency) before rendering.

        :param attrs: the attributes
        :type attrs: dict
        :return: the canonicalized attributes
        :rtype: dict
        """
        attrs = super().prep_attrs(attrs)
        attrs['linewidthScaleFactor'] = attrs.get('linewidthScaleFactor', '1')
        attrs['containerField'] = attrs.get('containerField', 'lineProperties')
        return attrs
    def to_x3d(self):
        """
        **LLM Docstring**

        Render the line properties to its X3D DOM element.

        :return: the X3D element
        """
        return X3DHTML.LineProperties(**self.prep_attrs(self.attrs))

class X3DPointProperties(X3DOptionsSet):
    __props__ = {
        "attenuation",
        "pointSizeMaxValue",
        "pointSizeMinValue",
        "pointSizeScaleFactor"
    }
    conversion_map = {
        "point_size":"pointSizeScaleFactor"
    }
    def prep_attrs(self, attrs:dict):
        """
        **LLM Docstring**

        Canonicalize the point-properties attributes (resolving the color into components/transparency) before rendering.

        :param attrs: the attributes
        :type attrs: dict
        :return: the canonicalized attributes
        :rtype: dict
        """
        attrs = super().prep_attrs(attrs)
        attrs['containerField'] = attrs.get('containerField', 'pointProperties')
        attrs['pointSizeMaxValue'] = str(
            max([
                float(attrs.get('pointSizeMaxValue', '0')),
                float(attrs.get('pointSizeMinValue', '0')),
                float(attrs.get('pointSizeScaleFactor', '0')),
            ])
        )
        return attrs
    def to_x3d(self):
        """
        **LLM Docstring**

        Render the point properties to its X3D DOM element.

        :return: the X3D element
        """
        return X3DHTML.PointProperties(**self.prep_attrs(self.attrs))

class X3DPrimitive(X3DObject):
    wrapper_class = None
    tag_class = None
    @classmethod
    def get_new_id(cls):
        """
        **LLM Docstring**

        Generate a fresh `x3d-obj-`-prefixed id.

        :return: the id
        :rtype: str
        """
        return "x3d-obj-" + str(uuid.uuid4())[:6]
    def __init__(self, *children, id=None, **opts):
        """
        **LLM Docstring**

        Set up a primitive holding its child objects and options (under an id).

        :param children: the child objects
        :param id: the primitive id (auto-generated if omitted)
        :param opts: the primitive options
        """
        if len(children) == 1 and isinstance(children[0], (tuple, list)):
            children = children[0]
        self.children = children
        if id is None:
            id = self.get_new_id()
        opts['id'] = id
        self.opts = opts
    @property
    def id(self):
        """
        **LLM Docstring**

        The primitive's id.

        :return: the id
        :rtype: str
        """
        return self.opts['id']
    @id.setter
    def id(self, new_id):
        """
        **LLM Docstring**

        The primitive's id.

        :return: the id
        :rtype: str
        """
        self.opts['id'] = new_id
    def split_opts(self, opts:dict):
        """
        **LLM Docstring**

        Split options into the non-appearance options and the material/appearance/line/point options.

        :param opts: the options
        :type opts: dict
        :return: `(object_opts, appearance_opts)`
        :rtype: tuple
        """
        material_keys = opts.keys() & (
            X3DMaterial.prop_keys()
            | X3DAppearance.prop_keys()
            | X3DLineProperties.prop_keys()
            | X3DPointProperties.prop_keys()
        )
        rem_keys = opts.keys() - material_keys
        return {k:opts[k] for k in rem_keys}, {k:opts[k] for k in material_keys}
    def get_appearance(self, appearance_options):
        """
        **LLM Docstring**

        Build the appearance node from the appearance options (or `None` if there are none).

        :param appearance_options: the appearance options
        :type appearance_options: dict
        :return: the appearance element (or `None`)
        """
        if len(appearance_options) > 0:
            return X3DAppearance(id=self.id+"-appearance", **appearance_options).to_x3d()
        else:
            return None
    def to_x3d(self):
        """
        **LLM Docstring**

        Render the primitive to its X3D DOM element, wrapping its children and appearance under the tag/wrapper classes.

        :return: the X3D element
        """
        obj_opts, appearance_opts = self.split_opts(self.opts)
        kids = [k.to_x3d() if hasattr(k, 'to_x3d') else k for k in self.children]
        appearance = self.get_appearance(appearance_opts)
        if self.tag_class is None:
            if appearance is not None:
                kids = [appearance] + kids
            return self.wrapper_class(
                kids,
                **obj_opts
            )
        else:
            core = self.tag_class(kids, **obj_opts)
            appearance = self.get_appearance(appearance_opts)
            if appearance is not None:
                return self.wrapper_class(appearance, core)
            else:
                return core

    @classmethod
    def resolve_prop_attr(self, prop_name):
        """
        **LLM Docstring**

        Map a property name to its attribute, routing appearance properties through the appearance node.

        :param prop_name: the property name
        :return: the attribute name
        """
        if prop_name in (
                X3DMaterial.prop_keys()
                | X3DAppearance.prop_keys()
                | X3DLineProperties.prop_keys()
                | X3DPointProperties.prop_keys()
        ):
            return X3DAppearance.resolve_prop_attr(prop_name)
        #TODO: handle mapping of transform props
        else:
            return prop_name

    def get_prop_node_id(self, prop_name):
        """
        **LLM Docstring**

        Return the node id carrying a property, routing appearance properties to the appearance node.

        :param prop_name: the property name
        :return: the node id
        :rtype: str
        """
        if prop_name in (
            X3DMaterial.prop_keys()
            | X3DAppearance.prop_keys()
            | X3DLineProperties.prop_keys()
            | X3DPointProperties.prop_keys()
        ):
            return X3DAppearance(id=self.id + "-appearance").get_prop_node_id(prop_name)
        else:
            return self.id

    def get_children(self):
        """
        **LLM Docstring**

        Return the primitive's child objects.

        :return: the children
        :rtype: list
        """
        return self.children

class X3DScene(X3DPrimitive):
    wrapper_class = X3DHTML.Scene
    default_viewpoint = {'viewAll':True}
    children: list
    def __init__(self, *children:X3DPrimitive, background=None, viewpoint=None, **opts):
        """
        **LLM Docstring**

        Set up a scene primitive with an optional background and viewpoint.

        :param children: the scene's child primitives
        :param background: the background specification
        :param viewpoint: the viewpoint specification
        :param opts: extra scene options
        """
        if viewpoint is None:
            viewpoint = self.default_viewpoint
        elif viewpoint is False:
            viewpoint = {}
        super().__init__(*children, **opts)
        if background is not None:
            self.children = [X3DBackground(color=background)] + list(self.children)
        if len(viewpoint) > 0:
            viewpoint = self.get_view_settings(**viewpoint)
            self.children = [X3DHTML.Viewpoint(**viewpoint)] + list(self.children)

    default_up_vector = (0, 1, 0)
    default_right_vector = (1, 0, 0)
    default_view_vector = (0, 0, 1)
    default_view_distance = 10
    @classmethod
    def get_view_settings(cls,
                          up_vector=None, view_vector=None, right_vector=None,
                          view_distance=None,
                          view_center=None,
                          view_matrix=None,
                          view_position=None,
                          return_settings=False,
                          **etc):
        """
        **LLM Docstring**

        Build viewpoint settings (position/orientation/etc.) from a flexible view
        specification.

        :param args: positional view arguments
        :param kwargs: view options
        :return: the viewpoint settings
        :rtype: dict
        """
        # CO = coords0[1] - coords0[0]
        # OH = coords0[5] - coords0[1]
        if view_matrix is None:
            if view_vector is None:
                if (
                    up_vector is not None and right_vector is not None
                ):
                    view_vector = nput.vec_crosses(up_vector, right_vector, normalize=True)
                elif right_vector is not None:
                    view_vector = nput.vec_crosses(cls.default_up_vector, right_vector, normalize=True)
                elif up_vector is not None:
                    view_vector = nput.vec_crosses(up_vector, cls.default_right_vector, normalize=True)

            if view_vector is not None:
                m = nput.rotation_matrix(
                    view_vector,
                    cls.default_view_vector
                )
            else:
                m = np.eye(3)

            if up_vector is None and right_vector is not None:
                if view_vector is None:
                    view_vector = cls.default_view_vector
                up_vector = nput.vec_normalize(
                    nput.vec_crosses(right_vector, view_vector)
                )
            elif up_vector is not None and view_vector is not None:
                up_vector = nput.vec_crosses(
                    view_vector,
                    nput.vec_crosses(view_vector, up_vector),
                    normalize=True
                )
            if up_vector is not None:
                m = m @ nput.rotation_matrix(
                    m.T @ up_vector,
                    cls.default_up_vector
                )
            view_matrix = m

        ang, cross = nput.extract_rotation_angle_axis(view_matrix)
        if view_vector is None:
            view_vector = view_matrix[:, -1]
        if view_position is None:
            if view_distance is None:
                view_distance = cls.default_view_distance
            view_position = view_distance * nput.vec_normalize(np.asanyarray(view_vector))
            if view_center is not None:
                if isinstance(view_center, dict):
                    view_center = view_center['untransformed']
                else:
                    view_center = view_matrix @ np.asanyarray(view_center)
                view_position = view_distance * nput.vec_normalize(
                    view_position + view_center
                )
        else:
            if isinstance(view_position, dict):
                view_position = view_position['untransformed']
            else:
                view_position = view_matrix @ np.asanyarray(view_position)
        if return_settings:
            return dict(
                {
                    'view_angle': ang,
                    'rotation_axis': cross,
                    'view': view_vector,
                    'dist': view_distance,
                    'center': view_center
                },
                **etc
            )
        else:
            return dict(
                {
                    'orientation': list(cross) + [ang],
                    'position': view_position
                },
                **etc
            )

class X3DBackground(X3DOptionsSet):
    wrapper_class = X3DHTML.Background
    __props__ = {
        'skyColor',
        'skyAngle'
    }
    conversion_map = {
        "color": "skyColor"
    }
    def prep_attrs(self, attrs: dict):
        """
        **LLM Docstring**

        Canonicalize the background attributes (resolving the color into components/transparency) before rendering.

        :param attrs: the attributes
        :type attrs: dict
        :return: the canonicalized attributes
        :rtype: dict
        """
        attrs = super().prep_attrs(attrs)
        color = attrs.get('skyColor', None)
        if color is not None:
            color, transparency = self.parse_color(color)
            attrs['skyColor'] = color
            if transparency is not None:
                attrs['transparency'] = transparency
        return attrs

    def to_x3d(self):
        """
        **LLM Docstring**

        Render the background to its X3D DOM element.

        :return: the X3D element
        """
        return X3DHTML.Background(**self.prep_attrs(self.attrs))

class X3DCoordinate(X3DPrimitive):
    wrapper_class = X3DHTML.Coordinate
    def __init__(self, points, id=None, **etc):
        """
        **LLM Docstring**

        Hold a set of coordinate points as an X3D coordinate node.

        :param points: the coordinate points
        :param id: the node id
        :param etc: extra options
        """
        super().__init__(point=self.prep_points(points), id=id, **etc)
    @classmethod
    def prep_points(cls, points):
        """
        **LLM Docstring**

        Normalize coordinate points into the X3D point format.

        :param points: the points
        :return: the prepared points
        """
        return " ".join(np.asanyarray(np.round(points, 4)).flatten().astype(str))

class X3DColor(X3DPrimitive):
    wrapper_class = X3DHTML.Color
    def __init__(self, colors, id=None, **etc):
        """
        **LLM Docstring**

        Hold a set of per-vertex colors as an X3D color node.

        :param colors: the colors
        :param id: the node id
        :param etc: extra options
        """
        super().__init__(color_list=colors, id=id, **etc)
    def split_opts(self, opts:dict):
        """
        **LLM Docstring**

        Split options for the color node (colors aren't material properties).

        :param opts: the options
        :type opts: dict
        :return: `(object_opts, appearance_opts)`
        :rtype: tuple
        """
        base_opts, appearance_opts = super().split_opts(opts)
        base_opts['color'] = self.prep_color(base_opts.pop('color_list'))
        return base_opts, appearance_opts
    @classmethod
    def prep_color(cls, points):
        """
        **LLM Docstring**

        Normalize color values into the X3D color format.

        :param points: the colors
        :return: the prepared colors
        """
        if isinstance(points, str):
            points = X3DOptionsSet.parse_color(points)[0]
        elif isinstance(points[0], str):
            points = [X3DOptionsSet.parse_color(p)[0] for p in points]
        return " ".join(np.asanyarray(np.round(points, 4)).flatten().astype(str))

class X3DGroup(X3DPrimitive):
    wrapper_class = X3DHTML.Group

class X3DSwitch(X3DPrimitive):
    wrapper_class = X3DHTML.Switch

class X3DGeometryObject(X3DPrimitive):
    wrapper_class = X3DHTML.Shape
    def __init__(self, *args, id=None, **opts):
        """
        **LLM Docstring**

        Set up a geometry object, splitting the material options out and preparing the geometry options.

        :param args: the geometry-defining arguments
        :param id: the object id
        :param opts: the geometry and material options
        """
        geom_opts, self.material_opts = self.split_opts(opts)
        self.geometry_opts = self.prep_geometry_opts(*args, **geom_opts)
        super().__init__(id=id)
    def get_interpolated_attributes(self):
        """
        **LLM Docstring**

        Return the geometry plus material attributes used for animation.

        :return: the attributes
        :rtype: dict
        """
        return dict(self.geometry_opts, **self.material_opts)
    @abc.abstractmethod
    def prep_geometry_opts(self, *args, **opts) -> dict:
        """
        **LLM Docstring**

        Abstract: build the geometry options for this shape from its defining arguments.

        :param args: the shape arguments
        :param opts: extra options
        :return: the geometry options
        :rtype: dict
        """
        ...
    def create_tag_object(self, **core_opts):
        """
        **LLM Docstring**

        Build the core geometry tag element from the core options.

        :param core_opts: the core geometry options
        :return: the geometry element
        """
        return self.tag_class(**core_opts)
    def create_object(self,
                      translation=None,
                      rotation=None,
                      scale=None,
                      normal=None,
                      up_vector=None,
                      bbox_center=None,
                      **core_opts):
        """
        **LLM Docstring**

        Build the geometry element together with its transform (translation/rotation/
        scale), computing the rotation needed to align the shape's up-vector with a
        supplied normal.

        :param translation: the translation
        :param rotation: the base rotation (axis-angle)
        :param scale: the scale
        :param normal: a normal to orient the shape toward
        :param up_vector: the shape's reference up-vector
        :param bbox_center: the bounding-box center
        :param core_opts: the core geometry options
        :return: `(geometry_element, transform_dict_or_None)`
        :rtype: tuple
        """
        core_opts['id'] = core_opts.get('id', self.id)
        base_obj = self.create_tag_object(**core_opts)
        tf = {}
        if normal is not None:
            if up_vector is None:
                up_vector = [0, 0, 1]
            angs, crosses, cn = nput.vec_angles(up_vector, normal, return_crosses=True, return_norms=False, return_cross_norms=True)
            if cn < 1e-6:
                orth = [1, 0, 0]
                if abs(np.dot(up_vector, orth)) < 1e-6:
                    orth = [0, 1, 0]
                crosses = nput.vec_crosses(orth, up_vector, normalize=True)
                if np.dot(normal, up_vector) > 0:
                    angs = 0
                else:
                    angs = np.pi
            if rotation is not None:
                if isinstance(rotation, str):
                    rotation = np.array(rotation.split()).astype(float)
                full_rot = (
                    nput.rotation_matrix(crosses, angs)
                        @ nput.rotation_matrix(rotation[:3], rotation[3])
                )
                angs, crosses = nput.extract_rotation_angle_axis(full_rot)
            rotation = np.concatenate([crosses, [angs]])
        for k,v in [["translation",translation], ["rotation",rotation], ["scale", scale], ['bboxcenter', bbox_center]]:
            if v is not None:
                tf[k] = np.round(v, 4) if not isinstance(v, str) else v
        if len(tf) == 0:
            tf = None
        # base_obj = X3DHTML.Transform(base_obj, translation=translation, rotation=rotation, scale=scale)
        return base_obj, tf
    def get_rotation(self, axis, up_vector=None):
        """
        **LLM Docstring**

        Compute the axis-angle rotation that aligns an up-vector with a target axis (and the axis norm).

        :param axis: the target axis
        :param up_vector: the reference up-vector
        :return: `(axis_angle_rotation, axis_norm)`
        :rtype: tuple
        """
        if up_vector is None:
            up_vector = [0, 1, 0]
        angs, crosses, norms = nput.vec_angles(up_vector, axis, return_crosses=True, return_norms=True)
        if nput.is_numeric(angs):
            return np.concatenate([crosses, [angs]]), norms[1]
        else:
            return np.concatenate([crosses, angs[..., np.newaxis]], axis=-1), norms[1]

    transform_props = ("translation", "rotation", "scale", "bboxcenter")
    def get_prop_node_id(self, prop_name):
        """
        **LLM Docstring**

        Return the node id carrying a property, routing transform properties to the transform node.

        :param prop_name: the property name
        :return: the node id
        :rtype: str
        """
        if prop_name in self.transform_props:
            return self.id + "-transform"
        else:
            return self.id
    def to_x3d(self):
        """
        **LLM Docstring**

        Render the geometry to its X3D DOM element, wrapping it in its appearance and transform.

        :return: the X3D element
        """
        # obj_opts, material_opts = self.split_opts(self.opts)
        # kids = [k.to_x3d() for k in self.children]
        core, tf = self.create_object(**self.geometry_opts)
        appearance = self.get_appearance(self.material_opts)
        if appearance is not None:
            core = self.wrapper_class(appearance, core)
        if tf is not None:
            core = X3DHTML.Transform(core, id=core.id+"-transform", **tf)
        return core

class X3DGeometryGroup(X3DGeometryObject):
    @abc.abstractmethod
    def prep_geometry_opts(self, *args, **opts) -> list[dict]:
        """
        **LLM Docstring**

        Abstract: build a list of per-instance geometry option dicts for this (possibly batched) shape.

        :param args: the shape arguments
        :param opts: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        ...
    def get_interpolated_attributes(self):
        """
        **LLM Docstring**

        Return the first instance's geometry plus material attributes used for animation.

        :return: the attributes
        :rtype: dict
        """
        return dict(self.geometry_opts[0], **self.material_opts)
    def prep_vecs(self, vecs, nstruct=None):
        """
        **LLM Docstring**

        Broadcast a vector (or `None`) across `nstruct` instances.

        :param vecs: the vector(s) (or `None`)
        :param nstruct: the number of instances
        :type nstruct: int | None
        :return: the per-instance vectors
        :rtype: np.ndarray | list
        """
        if vecs is None:
            return [None] * nstruct
        else:
            vecs = np.asanyarray(vecs)
            if vecs.ndim == 1:
                vecs = vecs[np.newaxis]
            if nstruct is not None:
                vecs = np.broadcast_to(vecs, (nstruct, vecs.shape[-1]))
        return vecs
    def prep_mats(self, mats, nstruct=None):
        """
        **LLM Docstring**

        Broadcast a matrix (or `None`) across `nstruct` instances.

        :param mats: the matrix/matrices (or `None`)
        :param nstruct: the number of instances
        :type nstruct: int | None
        :return: the per-instance matrices
        :rtype: np.ndarray | list
        """
        if mats is None:
            return [None] * nstruct
        else:
            mats = np.asanyarray(mats)
            if mats.ndim == 2:
                mats = mats[np.newaxis]
            if nstruct is not None:
                mats = np.broadcast_to(mats, (nstruct,) + mats.shape[-2:])
            return mats
    def prep_const(self, const, nstruct):
        """
        **LLM Docstring**

        Broadcast a scalar constant (or `None`) across `nstruct` instances.

        :param const: the constant (or `None`)
        :param nstruct: the number of instances
        :type nstruct: int
        :return: the per-instance constants
        :rtype: np.ndarray | list
        """
        if const is None:
            return [None] * nstruct
        else:
            const = np.asanyarray(const)
            if const.ndim == 0:
                const = const[np.newaxis]
            const = np.broadcast_to(const, (nstruct,))
            return const
    def to_x3d(self):
        """
        **LLM Docstring**

        Render every instance to its X3D element (wrapped in appearance/transform), grouping them under a single group node.

        :return: the X3D element
        """
        kids = [self.create_object(**g) for g in self.geometry_opts]
        appearance = self.get_appearance(self.material_opts)
        objs = []
        for i,(o,tf) in enumerate(kids):
            if hasattr(o, 'id'):
                id = o.id
            else:
                try:
                    id = o['id']
                except KeyError:
                    id = None
            if appearance is not None:
                o = self.wrapper_class(appearance, o)
            if tf is not None:
                o = X3DHTML.Transform(o, id=id+"-transform", **tf)
            objs.append(o)
        if len(objs) == 1:
            return objs[0]
        else:
            return X3DHTML.Group(objs)

class X3DSphere(X3DGeometryGroup):
    tag_class = X3DHTML.Sphere

    def prep_geometry_opts(self, centers, radius=1, **opts):
        """
        **LLM Docstring**

        Build the per-instance geometry options for spheres at the given centers.

        :param centers: the sphere centers
        :param radius: the sphere radius/radii
        :param opts: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        centers = self.prep_vecs(centers)
        rads = self.prep_const(radius, centers.shape[0])
        return [{"translation":c, "radius":r, **opts} for c,r in zip(centers, rads)]

class X3DBox(X3DGeometryGroup):
    tag_class = X3DHTML.Box

    def prep_geometry_opts(self, starts, ends, normal=None, rotation=None, **opts):
        """
        **LLM Docstring**

        Build the per-instance geometry options for boxes spanning the given corner pairs.

        :param starts: the min corners
        :param ends: the max corners
        :param normal: a normal to orient the boxes toward
        :param rotation: a base rotation
        :param opts: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        starts = self.prep_vecs(starts)
        ends = self.prep_vecs(ends)
        if normal is None:
            normal = [0, 1, 0]
        normal = self.prep_vecs(normal, len(starts))
        axes = self.prep_vecs([0, 1, 0], len(starts))
        rots, norms = self.get_rotation(axes, normal)

        rmats = nput.rotation_matrix(rots[:, :3], rots[:, 3])
        sizes = ((ends - starts) @ rmats).reshape(starts.shape)

        if rotation is not None:
            rots = self.prep_vecs(rotation, len(starts))

        return [
            {"translation": s, "rotation": a,
             "size": " ".join(np.round(size, 4).astype(str)) if not isinstance(size, str) else size,
             **opts}
            for s,a,size in zip((starts + ends) / 2, rots, sizes)
        ]

class X3DCylinder(X3DGeometryGroup):
    tag_class = X3DHTML.Cylinder

    def prep_geometry_opts(self, starts, ends, radius=1, **opts):
        """
        **LLM Docstring**

        Build the per-instance geometry options for cylinders between the given endpoints.

        :param starts: the start points
        :param ends: the end points
        :param radius: the cylinder radius/radii
        :param opts: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        starts = self.prep_vecs(starts)
        ends = self.prep_vecs(ends)
        radius = self.prep_const(radius, starts.shape[0])

        axes = ends - starts
        rots, norms = self.get_rotation(axes)

        return [
            {"translation":s, "rotation":a, "height":n, "radius":r, **opts}
            for s,a,n,r in zip((starts + ends) / 2, rots, norms, radius)
        ]

class X3DCone(X3DGeometryGroup):
    tag_class = X3DHTML.Cone

    def prep_geometry_opts(self, starts, ends, radius=1, top_radius=None, **opts):
        """
        **LLM Docstring**

        Build the per-instance geometry options for cones (or truncated cones) between the given endpoints.

        :param starts: the base points
        :param ends: the apex points
        :param radius: the base radius/radii
        :param top_radius: the top radius (for truncated cones)
        :param opts: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        starts = self.prep_vecs(starts)
        ends = self.prep_vecs(ends)
        radius = self.prep_const(radius, starts.shape[0])
        top_radius = self.prep_const(top_radius, starts.shape[0])

        axes = ends - starts
        rots, norms = self.get_rotation(axes)

        return [
            {"translation":s, "rotation":a, "height":n, "bottomRadius":r, "topRadius":t, **opts}
            for s,a,n,r,t in zip((starts + ends) / 2, rots, norms, radius, top_radius)
        ]

class X3DArrow(X3DGroup):

    arrowhead_class = X3DCone
    cylinder_class = X3DCylinder

    def __init__(self,
                 starts, ends,
                 radius=1,
                 top_radius=None,
                 arrowhead_radius=2,
                 arrowhead_radius_mode='scaled',
                 arrowhead_offset=.3,
                 arrowhead_offset_mode='scaled',
                 cylinder_class=None,
                 arrowhead_class=None,
                 **opts):
        """
        **LLM Docstring**

        Build an arrow (a cylinder shaft plus a cone head) between two endpoints.

        :param args: the arrow-defining arguments (endpoints, etc.)
        :param opts: styling and geometry options
        """
        if arrowhead_class is None:
            arrowhead_class = self.arrowhead_class
        if cylinder_class is None:
            cylinder_class = self.cylinder_class

        ends = np.asanyarray(ends)
        starts = np.asanyarray(starts)
        arrow_vectors = ends - starts
        norms = nput.vec_norms(arrow_vectors)
        if arrowhead_offset_mode == 'scaled':
            arrowhead_offset = arrowhead_offset * norms
        disp_vectors = arrowhead_offset * nput.vec_normalize(arrow_vectors, norms=norms)
        arrow_starts = ends - disp_vectors
        if arrowhead_radius_mode == 'scaled':
            arrowhead_radius = arrowhead_radius * radius
        arrowheads = arrowhead_class(arrow_starts, ends,
                                     radius=arrowhead_radius,
                                     top_radius=top_radius,
                                     **opts)
        cylinders = cylinder_class(starts, arrow_starts, radius=radius, **opts)

        super().__init__(
            arrowheads, cylinders
        )

class X3DCappedCylinder(X3DGroup):

    cap_class = X3DSphere
    cylinder_class = X3DCylinder

    def __init__(self,
                 starts, ends,
                 radius=1,
                 cylinder_class=None,
                 cap_class=None,
                 cap_offset=0,
                 use_caps=(True, True),
                 **opts):
        """
        **LLM Docstring**

        Build a capped cylinder (a cylinder plus end-cap spheres/disks) between two
        endpoints.

        :param args: the cylinder-defining arguments
        :param opts: styling and geometry options
        """
        if cap_class is None:
            cap_class = self.cap_class
        if cylinder_class is None:
            cylinder_class = self.cylinder_class

        if cap_offset != 0:
            raise NotImplementedError("cap offseting not supported yet")

        if use_caps is True: use_caps = [True, True]
        elif use_caps is False: use_caps = [False, False]

        cap_list = []
        if use_caps[0]:
            cap_list.append(cap_class(starts, radius=radius, **opts))
        if use_caps[1]:
            cap_list.append(cap_class(ends, radius=radius, **opts))
        cylinders = cylinder_class(starts, ends, radius=radius, **opts)

        super().__init__(
            *cap_list, cylinders
        )

class X3DText(X3DGeometryGroup):
    tag_class = X3DHTML.Text

    def __init__(self, *args, billboard=True, solid=None, billboard_opts=None, **opts):
        """
        **LLM Docstring**

        Build a text geometry, optionally billboarded to face the camera.

        :param args: the text-defining arguments
        :param billboard: face the camera
        :type billboard: bool
        :param solid: render single-sided
        :param billboard_opts: options for the billboard
        :type billboard_opts: dict | None
        :param opts: extra options
        """
        if solid is None:
            solid = bool(billboard)
        if billboard:
            if billboard_opts is None:
                billboard_opts = {'axisOfRotation':'0 0 0'}
            self.wrapper_class = lambda *x,**y:X3DHTML.Billboard(X3DHTML.Shape(*x, **y), **billboard_opts)
        super().__init__(*args, solid=solid, **opts)
    def create_tag_object(self, font_style=None, **core_opts):
        """
        **LLM Docstring**

        Build the text geometry tag with its font style.

        :param font_style: the font styling
        :type font_style: dict | None
        :param core_opts: the core geometry options
        :return: the text element
        """
        body = []
        if font_style is not None:
            body.append(font_style)
        return self.tag_class(body, **core_opts)
    def prep_geometry_opts(self, centers, text, font_style=None, rotation=None, normal=None, **opts):
        """
        **LLM Docstring**

        Build the per-instance geometry options for text labels at the given centers.

        :param centers: the label positions
        :param text: the label text
        :param font_style: the font styling
        :param rotation: a base rotation
        :param normal: a normal to orient the text toward
        :param opts: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        centers = self.prep_vecs(centers)
        rotation = self.prep_vecs(rotation, len(centers))
        normal = self.prep_vecs(normal, len(centers))
        text = self.prep_const(text, len(centers))
        if font_style is None:
            font_style = {}
        subfonts =  {o.partition("_")[-1]: v for o, v in opts.items() if o.startswith('font_')}
        for f in subfonts:
            del opts['font_' + f]
        font_style = subfonts | font_style
        if len(font_style) == 0:
            font_style = None
        font_style = [
            X3DHTML.FontStyle(**fs)
                if fs is not None else
            None
            for fs in self.prep_const(font_style, len(centers))
        ]
        return [
            {"translation": c, 'string': t, 'length': len(t), 'font_style':fs, 'rotation':r, 'normal':n, **opts}
            for c, t, fs, r, n in zip(centers, text, font_style, rotation, normal)
        ]

class X3DTorus(X3DGeometryGroup):
    tag_class = X3DHTML.Torus

    def prep_geometry_opts(self, centers, radius=1, inner_radius=None,
                           normal=None, rotation=None, scale=None,
                           angle=None,
                           **opts):
        """
        **LLM Docstring**

        Build the per-instance geometry options for tori at the given centers.

        :param centers: the torus centers
        :param radius: the outer radius/radii
        :param inner_radius: the inner (tube) radius
        :param opts: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        if angle is not None and angle < 0:
            if rotation is None:
                rotation = [0, 0, 1, 0]
            if isinstance(rotation, str):
                rotation = np.array(rotation.split()).astype(float)
            rotation = list(rotation[:3]) + [rotation[3] + angle]
            angle = abs(angle)
        centers = self.prep_vecs(centers)
        normal = self.prep_vecs(normal, centers.shape[0])
        rotation = self.prep_vecs(rotation, centers.shape[0])
        scale = self.prep_vecs(scale, centers.shape[0])
        radius = self.prep_const(radius, centers.shape[0])
        inner_radius = self.prep_const(inner_radius, centers.shape[0])
        angle = self.prep_const(angle, centers.shape[0])

        return [
            {
                "translation": s, "normal": n, "outerRadius": r,
                "innerRadius": i, 'rotation': rot, 'scale': sc,
                'angle': ang,
                **opts}
            for s, n, rot, sc, r, i, ang in zip(
                centers, normal,
                rotation, scale,
                radius, inner_radius, angle
            )
        ]

class X3DCoordinatesWrapper(X3DGeometryGroup):
    tag_class: X3DHTML.X3DElement
    def create_tag_object(self, *, point, color=None, **etc):
        """
        **LLM Docstring**

        Build the geometry tag wrapping a coordinate (and optional color) node.

        :param point: the coordinate points
        :param color: the per-vertex colors
        :param etc: extra options
        :return: the geometry element
        """
        body = [X3DCoordinate(point, id=self.id+"-coord").to_x3d()]
        if color is not None:
            body.append(X3DColor(color, id=self.id+'-color').to_x3d())
        return self.tag_class(body, **etc)
    def prep_geometry_opts(self, point, **etc):
        """
        **LLM Docstring**

        Build the per-instance geometry options for a coordinate-backed geometry.

        :param point: the coordinate points
        :param etc: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        return [
            dict({"translation":"0,0,0", "point":point}, **etc)
        ]

class X3DVertexCoordinatesWrapper(X3DCoordinatesWrapper):
    tag_class: X3DHTML.X3DElement
    def prep_geometry_opts(self, point, vertex_colors=None, **etc):
        """
        **LLM Docstring**

        Build the per-instance geometry options for a vertex-coordinate geometry with optional per-vertex colors.

        :param point: the vertex points
        :param vertex_colors: the per-vertex colors
        :param etc: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        base_dict = super().prep_geometry_opts(point, **etc)
        if vertex_colors is not None:
            if isinstance(vertex_colors[0], str) or nput.is_numeric(vertex_colors[0][0]):
                for bd in base_dict:
                    bd['colorPerVertex'] = bd.get('colorPerVertex', True)
                    bd['color'] = vertex_colors
            else:
                for bd, cc in zip(base_dict, vertex_colors):
                    bd['colorPerVertex'] = bd.get('colorPerVertex', True)
                    bd['color'] = cc
        return base_dict

class X3DIndexedCoordinatesWrapper(X3DCoordinatesWrapper):
    def prep_geometry_opts(self, point, indices, vertex_colors=None, **etc):
        """
        **LLM Docstring**

        Build the per-instance geometry options for an indexed-coordinate geometry.

        :param point: the coordinate points
        :param indices: the connectivity indices
        :param vertex_colors: the per-vertex colors
        :param etc: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        base_dict = dict(
                {
                    'index': " ".join(np.asanyarray(indices).flatten().astype(int).astype(str))
                },
                **super().prep_geometry_opts(point, **etc)[0]
            )
        if vertex_colors is not None:
            base_dict['colorPerVertex'] = True
            base_dict['color'] = vertex_colors
        return [base_dict]

class X3DGeometry2DGroup(X3DGeometryGroup):
    def __init__(self, *args, billboard=False, billboard_opts=None, **opts):
        """
        **LLM Docstring**

        Set up a 2D geometry group, optionally billboarded to face the camera.

        :param args: the geometry-defining arguments
        :param billboard: face the camera
        :type billboard: bool
        :param billboard_opts: billboard options
        :type billboard_opts: dict | None
        :param opts: extra options
        """
        if billboard:
            if billboard_opts is None:
                billboard_opts = {'axisOfRotation':'0 0 0'}
            self.wrapper_class = lambda *x,**y:X3DHTML.Billboard(X3DHTML.Shape(*x, **y), **billboard_opts)
        super().__init__(*args, **opts)
    @classmethod
    def prep_2d_coords(cls, coords):
        """
        **LLM Docstring**

        Normalize coordinates into the 2D geometry point format.

        :param coords: the coordinates
        :return: the prepared 2D coordinates
        """
        coords = np.asanyarray(coords)
        coords = coords.reshape(-1, coords.shape[-1])
        if coords.shape[-1] == 2:
            coords = np.pad(coords, [[0, 0], [0, 1]])
        return coords
    def prep_geometry_opts(self, center, **etc):
        """
        **LLM Docstring**

        Build the per-instance geometry options for a 2D geometry at the given center.

        :param center: the geometry center
        :param etc: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        center = self.prep_2d_coords(center)
        return [
            {
                "translation":c,
                 **etc
            }
            for c in center
        ]

class X3DRectangle2D(X3DGeometry2DGroup):
    tag_class = X3DHTML.Rectangle2D
    def prep_geometry_opts(self, left_endpoints, right_endpoints, normal=None, rotation=None, **etc):
        """
        **LLM Docstring**

        Build the per-instance geometry options for 2D rectangles spanning the given endpoint pairs.

        :param left_endpoints: the min corners
        :param right_endpoints: the max corners
        :param normal: a normal to orient toward
        :param rotation: a base rotation
        :param etc: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        left_endpoints = self.prep_2d_coords(left_endpoints)
        right_endpoints = self.prep_2d_coords(right_endpoints)
        center = (left_endpoints + right_endpoints ) / 2
        base_opts = super().prep_geometry_opts(center, **etc)

        if normal is None and rotation is not None:
            normal = np.array([0, 0, 1])
            rotation = np.asanyarray(rotation)
            if np.asanyarray(rotation).ndim > 1:
                normal = np.repeat(normal[np.newaxis], len(rotation), axis=0)
        if normal is not None:
            embedding_axes = nput.rotation_matrix(normal, [0, 0, 1])
            if rotation is not None:
                rotation = np.asanyarray(rotation)
                embedding_axes = embedding_axes @ nput.rotation_matrix(rotation[..., :3], rotation[..., 3])
            right_endpoints = (right_endpoints - center) @ embedding_axes
            left_endpoints = (left_endpoints - center) @ embedding_axes
        normal = self.prep_vecs(normal, right_endpoints.shape[0])
        rotation = self.prep_vecs(rotation, right_endpoints.shape[0])
        size_x = np.abs(right_endpoints[..., 0] - left_endpoints[..., 0])
        size_y = np.abs(right_endpoints[..., 1] - left_endpoints[..., 1])
        return [
            dict(b, size=[x, y], normal=n, rotation=r)
            for b,x,y,n,r in zip(base_opts, size_x, size_y, normal, rotation)
        ]
class X3DCircle2D(X3DGeometry2DGroup):
    tag_class = X3DHTML.Circle2D
    def prep_geometry_opts(self, centers, radius=1,
                           normal=None, rotation=None, scale=None,
                           angle=None,
                           **opts):
        """
        **LLM Docstring**

        Build the per-instance geometry options for 2D circles at the given centers.

        :param centers: the circle centers
        :param radius: the radius/radii
        :param etc: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        centers = self.prep_vecs(centers)
        normal = self.prep_vecs(normal, centers.shape[0])
        if angle is not None and angle < 0:
            if rotation is None:
                rotation = [0, 0, 1, 0]
            if isinstance(rotation, str):
                rotation = np.array(rotation.split()).astype(float)
            rotation = list(rotation[:3]) + [rotation[3] + angle]
            angle = abs(angle)
        rotation = self.prep_vecs(rotation, centers.shape[0])
        scale = self.prep_vecs(scale, centers.shape[0])
        radius = self.prep_const(radius, centers.shape[0])
        angle = self.prep_const(angle, centers.shape[0])

        return [
            {
                "translation": s, "normal": n, "radius": r,
                'rotation': rot, 'scale': sc,
                'angle': ang,
                **opts}
            for s, n, rot, sc, r, ang in zip(
                centers, normal,
                rotation, scale,
                radius, angle
            )
        ]

class X3DDisk2D(X3DGeometry2DGroup):
    tag_class = X3DHTML.Disk2D

    def prep_geometry_opts(self, centers, radius=1, inner_radius=None,
                           normal=None, rotation=None, scale=None,
                           angle=None,
                           **opts):
        """
        **LLM Docstring**

        Build the per-instance geometry options for 2D disks (or annuli) at the given centers.

        :param centers: the disk centers
        :param radius: the outer radius/radii
        :param inner_radius: the inner radius (for annuli)
        :param etc: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        centers = self.prep_vecs(centers)
        normal = self.prep_vecs(normal, centers.shape[0])
        if angle is not None and angle < 0:
            if rotation is None:
                rotation = [0, 0, 1, 0]
            if isinstance(rotation, str):
                rotation = np.array(rotation.split()).astype(float)
            rotation = list(rotation[:3]) + [rotation[3] + angle]
            angle = abs(angle)
        rotation = self.prep_vecs(rotation, centers.shape[0])
        scale = self.prep_vecs(scale, centers.shape[0])
        radius = self.prep_const(radius, centers.shape[0])
        inner_radius = self.prep_const(inner_radius, centers.shape[0])
        angle = self.prep_const(angle, centers.shape[0])

        return [
            {
                "translation": s, "normal": n, "outerRadius": r,
                "innerRadius": i, 'rotation': rot, 'scale': sc,
                'angle': ang,
                **opts}
            for s, n, rot, sc, r, i, ang in zip(
                centers, normal,
                rotation, scale,
                radius, inner_radius, angle
            )
        ]
class X3DPolyline2D(X3DGeometry2DGroup):
    tag_class = X3DHTML.Polyline2D

class X3DPointSet(X3DVertexCoordinatesWrapper):
    tag_class = X3DHTML.PointSet
class X3DLine(X3DCoordinatesWrapper):
    tag_class = X3DHTML.LineSet
class X3DTriangleSet(X3DCoordinatesWrapper):
    tag_class = X3DHTML.TriangleSet
class X3DIndexedTriangleSet(X3DIndexedCoordinatesWrapper):
    tag_class = X3DHTML.IndexedTriangleSet
class X3DIndexedLineSet(X3DIndexedCoordinatesWrapper):
    tag_class = X3DHTML.IndexedLineSet
    def prep_geometry_opts(self, point, indices, **etc):
        """
        **LLM Docstring**

        Build the per-instance geometry options for an indexed line set.

        :param point: the coordinate points
        :param indices: the line connectivity indices
        :param etc: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        opts = super().prep_geometry_opts(point, indices, **etc)
        opts[0]['coordIndex'] = opts[0].pop('index')
        return opts
class X3DIndexedQuadSet(X3DIndexedCoordinatesWrapper):
    tag_class = X3DHTML.IndexedQuadSet
class X3DIndexedFaceSet(X3DIndexedCoordinatesWrapper):
    tag_class = X3DHTML.IndexedFaceSet

class X3DGenericAnimator(X3DGroup):
    def __init__(self, *animation_data, id=None, animation_duration=2, running=True, slider=False,
                 **opts):
        """
        **LLM Docstring**

        Build an animator group: the animated objects, a time clock/sequencer, the
        per-property interpolators/sequencers, and an optional frame slider.

        :param animation_data: the animation data (interpreted by the subclass)
        :param id: the animator id (auto-generated if omitted)
        :param animation_duration: the loop duration in seconds
        :type animation_duration: float
        :param running: start the animation running
        :type running: bool
        :param slider: include a frame slider
        :type slider: bool
        :param opts: extra options
        """
        self.uuid = str(uuid.uuid4())
        if id is None:
            id = f"animation-{self.uuid}"

        animated_objects, attributes, nframes = self.get_animation_objects(animation_data, id)
        elements = []
        if slider:
            elements.append(
                JHTML.Input(type="range", value="0", min="0", max=f"{nframes}", step="1", cls="slider",
                            oninput=f"""document.getElementById('{id}').setAttribute('whichChoice', this.value)""")
            )
        elements.extend(animated_objects)
        # if running:
        elements.extend(
            self.build_animator_group(attributes,
                                      nframes=nframes,
                                      animation_duration=animation_duration,
                                      running=running,
                                      uuid=self.uuid
                                      )
        )

        super().__init__(elements, id=id, **opts)

    @classmethod
    @abc.abstractmethod
    def get_animation_objects(cls, animation_data, id) -> tuple[list[X3DObject], dict, int]:
        """
        **LLM Docstring**

        Abstract: build the `(objects, per-property attribute sets, frame count)` for the animation.

        :param animation_data: the animation data
        :param id: the animator id
        :return: `(objects, attribute_sets, nframes)`
        :rtype: tuple
        """
        ...

    @classmethod
    def build_animator_group(cls, attribute_sets, nframes, *, uuid, running=True, animation_duration=2):
        """
        **LLM Docstring**

        Build the animation driver nodes: a time sensor, an integer sequencer keyed to the
        frames, the routing between them, and the per-property animation controls.

        :param attribute_sets: the per-object property attribute sets
        :param nframes: the number of frames
        :type nframes: int
        :param uuid: the animation uuid
        :param running: start running
        :type running: bool
        :param animation_duration: the loop duration in seconds
        :type animation_duration: float
        :return: the driver nodes
        :rtype: list
        """
        key_frames = np.linspace(0, 1, nframes+1)[:-1]
        base = [
            X3DHTML.TimeSensor(id=f'animation-clock-{uuid}', cycleInterval=animation_duration, loop=True,
                               enabled=running),
            X3DHTML.IntegerSequencer(id=f'animation-indexer-{uuid}',
                                     key=key_frames,
                                     keyValue=np.arange(nframes)),
            X3DHTML.Route(
                fromField='fraction_changed', fromNode=f'animation-clock-{uuid}',
                toField='set_fraction', toNode=f'animation-indexer-{uuid}'
            )
        ]
        controls = sum((
            cls.create_animation_control(name, uuid=uuid, **opts)
            for attributes in attribute_sets
            for name,opts in attributes.items()),
            []
        )
        controls = [c for c in controls if c is not None]
        return base + controls

    @classmethod
    def resolve_control_type(cls, name, values):
        """
        **LLM Docstring**

        Decide whether a property animates by discrete indexing or by interpolation (from its value sequence).

        :param name: the property name
        :param values: the per-frame values
        :return: `'indexed'` or `'interpolated'`
        :rtype: str
        """
        if np.all(values == np.arange(1, len(values)+1)):
            return 'indexed'
        else:
            return 'interpolated'

    interpolator_map = {
        ('color', 'glow'): X3DHTML.ColorInterpolator,
        ('position', 'translation'): X3DHTML.PositionInterpolator,
        ('point', 'coordinate'): X3DHTML.CoordinateInterpolator,
        ('rotation',): X3DHTML.OrientationInterpolator
    }
    @classmethod
    def resolve_interpolator_type(cls, name, values):
        """
        **LLM Docstring**

        Determine the X3D interpolator class (and frame count) for a property from its
        name and the shape/type of its values.

        :param name: the property name
        :type name: str
        :param values: the per-frame values
        :return: `(interpolator_class, nframes)`
        :rtype: tuple
        :raises ValueError: if the interpolator can't be determined
        """
        nl = name.lower()
        for k,t in cls.interpolator_map.items():
            if any(kl in nl for kl in k):
                interp_type = t
                if issubclass(interp_type, X3DHTML.PositionInterpolator):
                    values = np.asanyarray(values)
                    if values.ndim == 1:
                        nframes = len(values) // 3
                    else:
                        nframes = len(values)
                elif issubclass(interp_type, X3DHTML.OrientationInterpolator):
                    values = np.asanyarray(values)
                    if values.ndim == 1:
                        nframes = len(values) // 4
                    else:
                        nframes = len(values)
                # elif issubclass(interp_type, X3DHTML.CoordinateInterpolator):
                #    ## Ill-defined if flattened
                else:
                    nframes = len(values)
                break
        else:
            values = np.asanyarray(values)
            nframes = len(values)
            if np.issubdtype(values.dtype, np.dtype(str)):
                interp_type = X3DHTML.ColorInterpolator
            elif values.ndim == 1:
                interp_type = X3DHTML.ScalarInterpolator
            elif values.ndim == 2 and values.shape[-1] == 3:
                interp_type = X3DHTML.PositionInterpolator
            elif values.ndim == 3 and values.shape[-1] == 3:
                interp_type = X3DHTML.CoordinateInterpolator
            elif values.ndim == 2 and values.shape[-1] == 4:
                interp_type = X3DHTML.OrientationInterpolator
            else:
                raise ValueError(f"interpolator can't be determined for property {name} with shape {values.shape}")

        return interp_type, nframes

    @classmethod
    def _raf_get_color_array_interpolator(cls,
                                          *,
                                          key,
                                          keyValue,
                                          id,
                                          clockId,
                                          targetId):
        """
        **LLM Docstring**

        Build a `requestAnimationFrame`-driven JavaScript interpolator for animating a
        per-vertex color array (which X3DOM can't interpolate natively).

        :param args: the interpolator-defining arguments
        :param kwargs: interpolator options
        :return: the interpolator nodes/scripts
        """
        key = np.asanyarray(key).tolist()
        keyValue = np.asanyarray(keyValue).tolist()

        key_js = json.dumps(key)
        keyValue_js = json.dumps(keyValue)

        return X3DHTML.Script(f'''
  let keys = {key_js};
  let keyValues = {keyValue_js};
  let numPoints = keyValues[0].length;

  function interpolateColors(f) {{
    let i = 0;
    while (i < keys.length - 2 && f >= keys[i + 1]) {{
      i++;
    }}
    let k0 = keys[i], k1 = keys[i + 1];
    let t = (k1 > k0) ? (f - k0) / (k1 - k0) : 0.0;
    t = Math.max(0.0, Math.min(1.0, t));

    let parts = [];
    for (let p = 0; p < numPoints; p++) {{
      let c0 = keyValues[i][p];
      let c1 = keyValues[i + 1][p];
      parts.push(
        (c0[0] + t * (c1[0] - c0[0])).toFixed(4) + " " +
        (c0[1] + t * (c1[1] - c0[1])).toFixed(4) + " " +
        (c0[2] + t * (c1[2] - c0[2])).toFixed(4)
      );
    }}
    return parts.join(" ");
  }}

  document.addEventListener("DOMContentLoaded", function () {{
    const ts = document.getElementById("{clockId}");
    const colorNode = document.getElementById("{targetId}");
    // cycleInterval read directly off the clock (attribute is a string)
    function getCycleInterval() {{
      const raw = ts.getAttribute("cycleInterval");
      const v = parseFloat(raw);
      return v > 0 ? v : 1.0; // guard against 0/NaN -> avoids divide-by-zero
    }}

    let lastColorString = null;
    let lastElapsed = null;

    function getElapsed() {{
        const node = ts._x3domNode;
        // _vf holds the field values; elapsedTime is maintained there while running
        if (node && node._vf && typeof node._vf.elapsedTime === "number") {{
            return node._vf.elapsedTime;
        }}
        return null;
    }}

    function tick() {{
      // ts.elapsedTime is exposed on the X3DOM node once the runtime is live.
      // Before that it's undefined, so fall back to 0.
      const elapsed = getElapsed()??0;
      if (lastElapsed == elapsed) {{ requestAnimationFrame(tick); return }};
      const cycle = getCycleInterval();

      // fraction in [0,1), looping — matches loop="True"
      const f = (elapsed % cycle) / cycle;

      const colorString = interpolateColors(f);

      // skip the setAttribute when nothing changed (cheap dedupe)
      if (colorString !== lastColorString) {{
        colorNode.setAttribute("color", colorString);
        lastColorString = colorString;
      }}

      requestAnimationFrame(tick);
    }}
    requestAnimationFrame(tick);
  }});
    ''', id=id)

    @classmethod
    def get_color_array_interpolator(cls,
                                     *,
                                     key,
                                     keyValue,
                                     id,
                                     clockId,
                                     targetId):
        """
        **LLM Docstring**

        Build the color-array interpolator for animating per-vertex colors across frames.

        :param args: the interpolator-defining arguments
        :param kwargs: interpolator options
        :return: the interpolator nodes
        """
        color_driver_id = id
        driver = X3DHTML.CoordinateInterpolator(key=key, keyValue=keyValue,
                                                id=color_driver_id,
                                                clockId=clockId,
                                                targetId=id+'-update')
        script = JHTML.Script(f"""(function() {{
const driver = document.getElementById("{id}");
const colorNode = document.getElementById("{targetId}");

function getInterpValue() {{
  const node = driver._x3domNode;
  if (node && node._vf && node._vf.value_changed) return node._vf.value_changed;
  return null;
}}

let lastStr = null;
function tick() {{
  requestAnimationFrame(tick);          // always re-arm
  const v = getInterpValue();
  if (!v || v.length === 0) return;

  // v is an array of x3dom SFVec3f objects (have .x/.y/.z) or arrays
  let str;
  if (typeof v[0] === "object" && "x" in v[0]) {{
    str = v.map(c => `${{c.x}} ${{c.y}} ${{c.z}}`).join(" ");
  }} else if (Array.isArray(v[0])) {{
    str = v.map(c => `${{c[0]}} ${{c[1]}} ${{c[2]}}`).join(" ");
  }} else {{
    str = v.join(" ");
  }}
  if (str === lastStr) return;
  colorNode.setAttribute("color", str);
  lastStr = str;
}}

requestAnimationFrame(tick)
// document.addEventListener("DOMContentLoaded", () => requestAnimationFrame(tick));
        }})()""", id=id+"-update")
        return [
            driver,
            script
        ]





    @classmethod
    def prep_interpolator(cls, interpolator_type, name, values, nframes, id, clock_id):
        """
        **LLM Docstring**

        Build the interpolator node (and its routing) for one animated property, keyed to
        the frames and wired to the target node.

        :param interpolator_type: the interpolator class
        :param name: the property name
        :param values: the per-frame values
        :param nframes: the number of frames
        :type nframes: int
        :param id: the target node id
        :param clock_id: the animation clock id
        :return: the interpolator nodes
        :rtype: list
        """
        target_id = id
        convert_values = True
        if interpolator_type == X3DHTML.ColorInterpolator:
            if isinstance(values[0], str) or values[0] is None:
                target_id = id + "-appearance-material"
                values = [
                    X3DOptionsSet.parse_color('black' if c is None else c)[0]
                    for c in values
                ]
            else:
                target_id = id + "-color"
                name = None
                interpolator_type = cls.get_color_array_interpolator
                values = [
                    [X3DOptionsSet.parse_color('black' if c is None else c)[0] for c in vl]
                    for vl in values
                ]
                convert_values = True
        elif interpolator_type == X3DHTML.CoordinateInterpolator:
            target_id = id + "-coord"
        if convert_values and nput.is_numeric_array_like(values):
            values = " ".join(np.round(values, 4).flatten().astype(str))
        key_frames = np.linspace(0, 1, nframes)

        interp_obj = (
            interpolator_type(key=key_frames, keyValue=values,
                              id=id + "-interpolator-" + cls.get_new_id(),
                              clockId=f'animation-clock-{clock_id}',
                              targetId=target_id)
                if not hasattr(interpolator_type, 'id') else
            interpolator_type
        )
        return interp_obj, name, target_id

    @classmethod
    def create_animation_control(cls, name, *, id, uuid, type=None, values=None, interpolator_type=None):
        """
        **LLM Docstring**

        Build the animation control (a sequencer or interpolator, plus routing) for one
        property, choosing indexed vs interpolated animation.

        :param name: the property name
        :param id: the target node id
        :param uuid: the animation uuid
        :param type: the control type (inferred if omitted)
        :param values: the per-frame values
        :param interpolator_type: an explicit interpolator class
        :return: the control nodes
        :rtype: list
        """
        if values is None:
            if type is None:
                raise ValueError("`values` or `type` must be passed")
            return [
                X3DHTML.Route(
                    fromField='value_changed' if type == 'indexed' else 'fraction_changed',
                    fromNode=f'animation-indexer-{uuid}' if type == 'indexed' else f'animation-clock-{uuid}',
                    toField=name, toNode=id
                )
            ]
        else:
            if all(v is None for v in values): return [None]
            # if type is None:
            #     type = self.resolve_control_type(name, values)
            interpolator_type, nframes = cls.resolve_interpolator_type(name, values)
            interp_obj, name, target_id = cls.prep_interpolator(interpolator_type, name, values, nframes, id, uuid)
            if not isinstance(interp_obj, list):
                interp_obj = [interp_obj]
            if hasattr(interp_obj[0], 'id'):
                interp_id = interp_obj[0].id
            else:
                interp_id = interp_obj[0]['id']
            if not isinstance(interp_obj, list):
                interp_obj = [interp_obj]
            objs = interp_obj + [
                    X3DHTML.Route(
                        fromField='fraction_changed',
                        fromNode=f'animation-clock-{uuid}',
                        toField='set_fraction', toNode=interp_id
                    )]
            if name is not None:
                objs.append(X3DHTML.Route(
                    fromField='value_changed',
                    fromNode=interp_id,
                    toField='set_'+name, toNode=target_id
                ))
            return objs

class X3DListAnimator(X3DGenericAnimator):
    @classmethod
    def get_animation_objects(self, frames, id):
        """
        **LLM Docstring**

        Build a frame-switching animation: wrap the frames in an X3D `Switch` and animate
        its `whichChoice` by discrete index.

        :param frames: the per-frame objects
        :param id: the animator id
        :return: `(objects, attribute_sets, nframes)`
        :rtype: tuple
        """
        anim_frames = X3DSwitch(
                *frames,
                id=id+"-switch",
                whichChoice="0"
            )
        nframes = len(anim_frames.children)
        attributes = [
            {
                'whichChoice':{'type':'indexed', 'id':id+"-switch"}
            }
        ]
        return [anim_frames], attributes, nframes

class X3DInterpolatingAnimator(X3DGenericAnimator):
    @classmethod
    def get_animation_objects(cls, object_attr_sets:dict[X3DObject, dict], id):
        """
        **LLM Docstring**

        Build an interpolating animation from a mapping of objects to their per-property
        frame values, validating a consistent frame count and resolving each property's
        target node.

        :param object_attr_sets: the `{object: {property: per_frame_values}}` mapping
        :type object_attr_sets: dict
        :param id: the animator id
        :return: `(objects, attribute_sets, nframes)`
        :rtype: tuple
        :raises ValueError: if the properties have mismatched frame counts
        """
        if isinstance(object_attr_sets, tuple) and len(object_attr_sets) == 1:
            object_attr_sets = object_attr_sets[0]
        objects = []
        att_set = []
        nframes = None
        for i,(obj,attrs) in enumerate(object_attr_sets.items()):
            objects.append(obj)
            at_list = {}
            for a,v in attrs.items():
                if nframes is None:
                    nframes = len(v)
                else:
                    nf = len(v)
                    if nframes != nf:
                        raise ValueError(f"attribute {a} has different number of frames {nf} than other attributes {nframes}")
                prop = obj.resolve_prop_attr(a)
                node = obj.get_prop_node_id(a)
                at_list[prop] = {
                    'id':node,
                    'values':obj.prep_animation_values(a, v)
                }
            att_set.append(at_list)

        return objects, att_set, nframes

    @classmethod
    def frame_diffs(cls, ref:X3DObject|X3DHTML.X3DElement, test:X3DObject|X3DHTML.X3DElement, *rest:X3DObject|X3DHTML.X3DElement):
        """
        **LLM Docstring**

        Walk several X3D object trees in parallel and find which nodes/attributes differ
        across frames, separating the static nodes from the per-node attribute changes.

        :param ref: the reference (first-frame) tree
        :param test: the second-frame tree
        :param rest: the remaining frames' trees
        :return: `(static_nodes, {node: per_frame_attribute_values})`
        :rtype: tuple
        :raises ValueError: if the trees have mismatched structure
        """
        statics = []
        changes = {}
        queue = collections.deque([(ref, test) + rest])
        # avoid bugs
        del ref
        del test
        while queue:
            trees = queue.pop()
            left = trees[0]
            rights = trees[1:]
            if isinstance(left, X3DObject):
                left_kids = left.get_children()
                right_kids = [right.get_children() for right in rights]
            else:
                left_kids = left.elems
                right_kids = [right.elems for right in rights]

            l = len(left_kids)
            for right,rk in zip(rights, right_kids):
                if l != len(rk):
                    raise ValueError(f"tree nodes have different numbers of children {l} vs {len(rk)} for  {left} and {right}")

            if l > 0:
                all_kids = [left_kids] + right_kids
                queue.extend(zip(*all_kids))

            if isinstance(left, X3DObject):
                left_attrs = left.get_interpolated_attributes()
                right_attrs = [right.get_interpolated_attributes() for right in rights]
            else:
                left_attrs = left.attrs
                right_attrs = [right.attrs for right in rights]

            attr_diffs = {}
            all_keys = {
                k
                for a in [left_attrs] + right_attrs
                for k in a.keys()
            } - {'id'}
            for k in all_keys:
                v = left_attrs.get(k)
                vals = [v]
                diffed = False
                for a in right_attrs:
                    v2 = a.get(k)
                    vals.append(v2)
                    if not diffed:
                        diffed = (
                                v is None and v2 is not None
                                or v2 is None and v is None
                        )
                        if not diffed:
                            if nput.is_numeric_array_like(v):
                                if not nput.is_numeric_array_like(v2):
                                    diffed = True
                                else:
                                    diffed = not np.allclose(v, v2)
                            elif nput.is_numeric_array_like(2):
                                diffed = True
                            else:
                                diffed = v2 != v
                if diffed:
                    attr_diffs[k] = vals
            if len(attr_diffs) > 0:
                changes[left] = attr_diffs
            elif l == 0:
                statics.append(left)
        return statics, changes

    @classmethod
    def from_frames(cls, frames:list[X3DObject|X3DHTML.X3DElement], **opts):
        """
        **LLM Docstring**

        Build an interpolating animation from a list of frame trees by diffing them:
        static content is kept as-is and only the changing attributes are animated.

        :param frames: the per-frame object trees
        :type frames: list
        :param opts: options for the animator
        :return: the animation (or the single frame if nothing changes)
        """
        static_objects, interpolated_objects = cls.frame_diffs(*frames)
        if len(interpolated_objects) == 0:
            return frames[0]
        else:
            anim = X3DInterpolatingAnimator(interpolated_objects, **opts)
            if len(static_objects) > 0:
                anim = X3DGroup(static_objects + [anim])
            return anim


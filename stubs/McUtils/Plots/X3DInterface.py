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
__all__ = ['X3D', 'X3DPrimitive', 'X3DGeometryObject', 'X3DGeometryGroup', 'X3DGroup', 'X3DScene', 'X3DBackground', 'X3DMaterial', 'X3DLine', 'X3DSphere', 'X3DCone', 'X3DBox', 'X3DCylinder', 'X3DCappedCylinder', 'X3DArrow', 'X3DTorus', 'X3DRectangle2D', 'X3DDisk2D', 'X3DCircle2D', 'X3DPolyline2D', 'X3DTriangleSet', 'X3DIndexedTriangleSet', 'X3DIndexedLineSet', 'X3DSwitch', 'X3DListAnimator', 'X3DInterpolatingAnimator']

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
        ...

    def get_children(self):
        """
        **LLM Docstring**

        Return the object's child objects (none by default).

        :return: the children
        :rtype: list
        """
        ...

    @classmethod
    def get_new_id(cls):
        """
        **LLM Docstring**

        Generate a fresh unique id for a new object.

        :return: the id
        :rtype: str
        """
        ...

    def resolve_prop_attr(self, prop_name):
        """
        **LLM Docstring**

        Map a property name to the X3D attribute name it animates (identity by default).

        :param prop_name: the property name
        :return: the attribute name
        """
        ...

    def prep_animation_values(self, prop_name, values):
        """
        **LLM Docstring**

        Normalize a property's per-frame animation values (e.g. defaulting `transparency` gaps to 0).

        :param prop_name: the property name
        :param values: the per-frame values
        :return: the normalized values
        """
        ...

    def get_prop_node_id(self, prop_name):
        """
        **LLM Docstring**

        Return the id of the DOM node that carries a given animated property (this object by default).

        :param prop_name: the property name
        :return: the node id
        :rtype: str
        """
        ...

class X3D(X3DObject):
    defaults = dict(width=500, height=500)

    @classmethod
    def get_new_id(cls):
        """
        **LLM Docstring**

        Generate a fresh `x3d-`-prefixed id.

        :return: the id
        :rtype: str
        """
        ...

    def __init__(self, *children, id=None, dynamic_loading=True, x3dom_path=None, x3dom_css_path=None, include_mathjax=False, recording_options=None, include_export_button=False, include_record_button=False, include_view_settings_button=False, preload_scripts=None, onload_scripts=None, **opts):
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
        ...
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
        ...

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
        ...

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
        ...

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
        ...

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
        ...

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
        ...

    def to_widget(self, dynamic_loading=None, include_export_button=None, include_record_button=None, include_view_settings_button=None):
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
        ...

    def to_html(self, *base_elems, header_elems=None, dynamic_loading=False, include_export_button=None, include_record_button=None, **header_info):
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
        ...

    def _ipython_display_(self):
        """
        **LLM Docstring**

        Display the scene widget in IPython.
        """
        ...

    def get_mime_bundle(self):
        """
        **LLM Docstring**

        Return the scene widget's MIME bundle for rich display.

        :return: the MIME bundle
        :rtype: dict
        """
        ...

    def to_x3d(self):
        """
        **LLM Docstring**

        Render the scene to its `<x3d>` DOM element, formatting the size and rendering each child.

        :return: the X3D element
        """
        ...

    def display(self):
        """
        **LLM Docstring**

        Display the scene widget.
        """
        ...

    def show(self):
        """
        **LLM Docstring**

        Display the scene, enabling dynamic loading when in a Jupyter environment.
        """
        ...

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
        ...

    def get_children(self):
        """
        **LLM Docstring**

        Return the scene's child objects.

        :return: the children
        :rtype: list
        """
        ...

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
        ...

    @classmethod
    def get_new_id(cls):
        """
        **LLM Docstring**

        Generate a fresh `x3d-opts-`-prefixed id.

        :return: the id
        :rtype: str
        """
        ...

    def __init__(self, id=None, **attrs):
        """
        **LLM Docstring**

        Hold a set of X3D node attributes under an id.

        :param id: the node id (auto-generated if omitted)
        :param attrs: the node attributes
        """
        ...
    conversion_map = {}

    @classmethod
    def prop_keys(cls):
        """
        **LLM Docstring**

        Return the set of valid property keys (declared props plus conversion-map aliases).

        :return: the valid keys
        :rtype: set
        """
        ...

    def prep_attrs(self, attrs: dict):
        """
        **LLM Docstring**

        Canonicalize the node attributes (applying the conversion-map aliases and attaching the id), validating against the declared props.

        :param attrs: the attributes
        :type attrs: dict
        :return: the canonicalized attributes
        :rtype: dict
        :raises ValueError: for invalid attribute keys
        """
        ...

    @classmethod
    def resolve_prop_attr(self, prop_name):
        """
        **LLM Docstring**

        Map a property name to its X3D attribute name via the conversion map.

        :param prop_name: the property name
        :return: the attribute name
        """
        ...

    def get_prop_node_id(self, prop_name):
        """
        **LLM Docstring**

        Return the node id carrying a given property (this node).

        :param prop_name: the property name
        :return: the node id
        :rtype: str
        """
        ...

class X3DMaterial(X3DOptionsSet):
    __props__ = {'diffuseColor', 'ambientIntensity', 'emissiveColor', 'specularColor', 'shininess', 'transparency'}
    conversion_map = {'brightness': 'ambientIntensity', 'glow': 'emissiveColor', 'color': 'diffuseColor', 'specularity': 'specularColor'}

    def prep_attrs(self, attrs: dict):
        """
        **LLM Docstring**

        Canonicalize the material attributes (resolving the color into components/transparency) before rendering.

        :param attrs: the attributes
        :type attrs: dict
        :return: the canonicalized attributes
        :rtype: dict
        """
        ...

    def to_x3d(self):
        """
        **LLM Docstring**

        Render the material to its X3D DOM element.

        :return: the X3D element
        """
        ...

class X3DTexture(X3DOptionsSet):
    __props__ = {'url', 'image', 'crossOrigin', 'hideChildren', 'metadata', 'repeatS', 'repeatT', 'scale', 'textureProperties', 'texture_type'}
    conversion_map = {}
    texture_type_mapping = {'pixel': X3DHTML.PixelTexture, 'image': X3DHTML.ImageTexture, 'movie': X3DHTML.MovieTexture}
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
        ...

    def to_x3d(self):
        """
        **LLM Docstring**

        Render the texture to its X3D DOM element, dispatching on the (inferred) texture type.

        :return: the X3D element
        """
        ...

class X3DAppearance(X3DOptionsSet):
    __props__ = {'alphaClipThreshold', 'blendMode', 'colorMaskModedepthModelinePropertiesmaterialmetadatapointPropertiesshaders', 'sortKey', 'sortType', 'texture', 'textureTransform'}

    @classmethod
    def get_new_id(cls):
        """
        **LLM Docstring**

        Generate a fresh appearance id.

        :return: the id
        :rtype: str
        """
        ...

    def prep_attrs(self, attrs: dict):
        """
        **LLM Docstring**

        Canonicalize the appearance attributes, splitting the material/texture/line/point sub-properties out into their own nodes.

        :param attrs: the attributes
        :type attrs: dict
        :return: the canonicalized attributes
        :rtype: dict
        """
        ...

    def to_x3d(self):
        """
        **LLM Docstring**

        Render the appearance to its X3D DOM element (with its material/texture/line/point child nodes).

        :return: the X3D element
        """
        ...

    @classmethod
    def resolve_prop_attr(self, prop_name):
        """
        **LLM Docstring**

        Map a property name to the appearance sub-node attribute it animates.

        :param prop_name: the property name
        :return: the attribute name
        """
        ...

    def get_prop_node_id(self, prop_name):
        """
        **LLM Docstring**

        Return the id of the appearance sub-node (material/texture/...) carrying a property.

        :param prop_name: the property name
        :return: the node id
        :rtype: str
        """
        ...

class X3DLineProperties(X3DOptionsSet):
    __props__ = {'applied', 'linetype', 'linewidth', 'linewidthScaleFactor'}
    conversion_map = {'line_style': 'linetype', 'line_thickness': 'linewidth'}

    def prep_attrs(self, attrs: dict):
        """
        **LLM Docstring**

        Canonicalize the line-properties attributes (resolving the color into components/transparency) before rendering.

        :param attrs: the attributes
        :type attrs: dict
        :return: the canonicalized attributes
        :rtype: dict
        """
        ...

    def to_x3d(self):
        """
        **LLM Docstring**

        Render the line properties to its X3D DOM element.

        :return: the X3D element
        """
        ...

class X3DPointProperties(X3DOptionsSet):
    __props__ = {'attenuation', 'pointSizeMaxValue', 'pointSizeMinValue', 'pointSizeScaleFactor'}
    conversion_map = {'point_size': 'pointSizeScaleFactor'}

    def prep_attrs(self, attrs: dict):
        """
        **LLM Docstring**

        Canonicalize the point-properties attributes (resolving the color into components/transparency) before rendering.

        :param attrs: the attributes
        :type attrs: dict
        :return: the canonicalized attributes
        :rtype: dict
        """
        ...

    def to_x3d(self):
        """
        **LLM Docstring**

        Render the point properties to its X3D DOM element.

        :return: the X3D element
        """
        ...

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
        ...

    def __init__(self, *children, id=None, **opts):
        """
        **LLM Docstring**

        Set up a primitive holding its child objects and options (under an id).

        :param children: the child objects
        :param id: the primitive id (auto-generated if omitted)
        :param opts: the primitive options
        """
        ...

    @property
    def id(self):
        """
        **LLM Docstring**

        The primitive's id.

        :return: the id
        :rtype: str
        """
        ...

    @id.setter
    def id(self, new_id):
        """
        **LLM Docstring**

        The primitive's id.

        :return: the id
        :rtype: str
        """
        ...

    def split_opts(self, opts: dict):
        """
        **LLM Docstring**

        Split options into the non-appearance options and the material/appearance/line/point options.

        :param opts: the options
        :type opts: dict
        :return: `(object_opts, appearance_opts)`
        :rtype: tuple
        """
        ...

    def get_appearance(self, appearance_options):
        """
        **LLM Docstring**

        Build the appearance node from the appearance options (or `None` if there are none).

        :param appearance_options: the appearance options
        :type appearance_options: dict
        :return: the appearance element (or `None`)
        """
        ...

    def to_x3d(self):
        """
        **LLM Docstring**

        Render the primitive to its X3D DOM element, wrapping its children and appearance under the tag/wrapper classes.

        :return: the X3D element
        """
        ...

    @classmethod
    def resolve_prop_attr(self, prop_name):
        """
        **LLM Docstring**

        Map a property name to its attribute, routing appearance properties through the appearance node.

        :param prop_name: the property name
        :return: the attribute name
        """
        ...

    def get_prop_node_id(self, prop_name):
        """
        **LLM Docstring**

        Return the node id carrying a property, routing appearance properties to the appearance node.

        :param prop_name: the property name
        :return: the node id
        :rtype: str
        """
        ...

    def get_children(self):
        """
        **LLM Docstring**

        Return the primitive's child objects.

        :return: the children
        :rtype: list
        """
        ...

class X3DScene(X3DPrimitive):
    wrapper_class = X3DHTML.Scene
    default_viewpoint = {'viewAll': True}
    children: list

    def __init__(self, *children: X3DPrimitive, background=None, viewpoint=None, **opts):
        """
        **LLM Docstring**

        Set up a scene primitive with an optional background and viewpoint.

        :param children: the scene's child primitives
        :param background: the background specification
        :param viewpoint: the viewpoint specification
        :param opts: extra scene options
        """
        ...
    default_up_vector = (0, 1, 0)
    default_right_vector = (1, 0, 0)
    default_view_vector = (0, 0, 1)
    default_view_distance = 10

    @classmethod
    def get_view_settings(cls, up_vector=None, view_vector=None, right_vector=None, view_distance=None, view_center=None, view_matrix=None, view_position=None, **etc):
        """
        **LLM Docstring**

        Build viewpoint settings (position/orientation/etc.) from a flexible view
        specification.

        :param args: positional view arguments
        :param kwargs: view options
        :return: the viewpoint settings
        :rtype: dict
        """
        ...

class X3DBackground(X3DOptionsSet):
    wrapper_class = X3DHTML.Background
    __props__ = {'skyColor', 'skyAngle'}
    conversion_map = {'color': 'skyColor'}

    def prep_attrs(self, attrs: dict):
        """
        **LLM Docstring**

        Canonicalize the background attributes (resolving the color into components/transparency) before rendering.

        :param attrs: the attributes
        :type attrs: dict
        :return: the canonicalized attributes
        :rtype: dict
        """
        ...

    def to_x3d(self):
        """
        **LLM Docstring**

        Render the background to its X3D DOM element.

        :return: the X3D element
        """
        ...

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
        ...

    @classmethod
    def prep_points(cls, points):
        """
        **LLM Docstring**

        Normalize coordinate points into the X3D point format.

        :param points: the points
        :return: the prepared points
        """
        ...

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
        ...

    def split_opts(self, opts: dict):
        """
        **LLM Docstring**

        Split options for the color node (colors aren't material properties).

        :param opts: the options
        :type opts: dict
        :return: `(object_opts, appearance_opts)`
        :rtype: tuple
        """
        ...

    @classmethod
    def prep_color(cls, points):
        """
        **LLM Docstring**

        Normalize color values into the X3D color format.

        :param points: the colors
        :return: the prepared colors
        """
        ...

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
        ...

    def get_interpolated_attributes(self):
        """
        **LLM Docstring**

        Return the geometry plus material attributes used for animation.

        :return: the attributes
        :rtype: dict
        """
        ...

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
        ...

    def create_object(self, translation=None, rotation=None, scale=None, normal=None, up_vector=None, bbox_center=None, **core_opts):
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
        ...

    def get_rotation(self, axis, up_vector=None):
        """
        **LLM Docstring**

        Compute the axis-angle rotation that aligns an up-vector with a target axis (and the axis norm).

        :param axis: the target axis
        :param up_vector: the reference up-vector
        :return: `(axis_angle_rotation, axis_norm)`
        :rtype: tuple
        """
        ...
    transform_props = ('translation', 'rotation', 'scale', 'bboxcenter')

    def get_prop_node_id(self, prop_name):
        """
        **LLM Docstring**

        Return the node id carrying a property, routing transform properties to the transform node.

        :param prop_name: the property name
        :return: the node id
        :rtype: str
        """
        ...

    def to_x3d(self):
        """
        **LLM Docstring**

        Render the geometry to its X3D DOM element, wrapping it in its appearance and transform.

        :return: the X3D element
        """
        ...

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
        ...

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
        ...

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
        ...

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
        ...

    def to_x3d(self):
        """
        **LLM Docstring**

        Render every instance to its X3D element (wrapped in appearance/transform), grouping them under a single group node.

        :return: the X3D element
        """
        ...

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
        ...

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
        ...

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
        ...

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
        ...

class X3DArrow(X3DGroup):
    arrowhead_class = X3DCone
    cylinder_class = X3DCylinder

    def __init__(self, starts, ends, radius=1, top_radius=None, arrowhead_radius=2, arrowhead_radius_mode='scaled', arrowhead_offset=0.3, arrowhead_offset_mode='scaled', cylinder_class=None, arrowhead_class=None, **opts):
        """
        **LLM Docstring**

        Build an arrow (a cylinder shaft plus a cone head) between two endpoints.

        :param args: the arrow-defining arguments (endpoints, etc.)
        :param opts: styling and geometry options
        """
        ...

class X3DCappedCylinder(X3DGroup):
    cap_class = X3DSphere
    cylinder_class = X3DCylinder

    def __init__(self, starts, ends, radius=1, cylinder_class=None, cap_class=None, cap_offset=0, use_caps=(True, True), **opts):
        """
        **LLM Docstring**

        Build a capped cylinder (a cylinder plus end-cap spheres/disks) between two
        endpoints.

        :param args: the cylinder-defining arguments
        :param opts: styling and geometry options
        """
        ...

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
        ...

    def create_tag_object(self, font_style=None, **core_opts):
        """
        **LLM Docstring**

        Build the text geometry tag with its font style.

        :param font_style: the font styling
        :type font_style: dict | None
        :param core_opts: the core geometry options
        :return: the text element
        """
        ...

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
        ...

class X3DTorus(X3DGeometryGroup):
    tag_class = X3DHTML.Torus

    def prep_geometry_opts(self, centers, radius=1, inner_radius=None, normal=None, rotation=None, scale=None, angle=None, **opts):
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
        ...

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
        ...

    def prep_geometry_opts(self, point, **etc):
        """
        **LLM Docstring**

        Build the per-instance geometry options for a coordinate-backed geometry.

        :param point: the coordinate points
        :param etc: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        ...

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
        ...

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
        ...

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
        ...

    @classmethod
    def prep_2d_coords(cls, coords):
        """
        **LLM Docstring**

        Normalize coordinates into the 2D geometry point format.

        :param coords: the coordinates
        :return: the prepared 2D coordinates
        """
        ...

    def prep_geometry_opts(self, center, **etc):
        """
        **LLM Docstring**

        Build the per-instance geometry options for a 2D geometry at the given center.

        :param center: the geometry center
        :param etc: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        ...

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
        ...

class X3DCircle2D(X3DGeometry2DGroup):
    tag_class = X3DHTML.Circle2D

    def prep_geometry_opts(self, centers, radius=1, normal=None, rotation=None, scale=None, angle=None, **opts):
        """
        **LLM Docstring**

        Build the per-instance geometry options for 2D circles at the given centers.

        :param centers: the circle centers
        :param radius: the radius/radii
        :param etc: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        ...

class X3DDisk2D(X3DGeometry2DGroup):
    tag_class = X3DHTML.Disk2D

    def prep_geometry_opts(self, centers, radius=1, inner_radius=None, normal=None, rotation=None, scale=None, angle=None, **opts):
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
        ...

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
        ...

class X3DIndexedQuadSet(X3DIndexedCoordinatesWrapper):
    tag_class = X3DHTML.IndexedQuadSet

class X3DIndexedFaceSet(X3DIndexedCoordinatesWrapper):
    tag_class = X3DHTML.IndexedFaceSet

class X3DGenericAnimator(X3DGroup):

    def __init__(self, *animation_data, id=None, animation_duration=2, running=True, slider=False, **opts):
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
        ...

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
        ...

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
        ...

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
        ...

    @classmethod
    def _raf_get_color_array_interpolator(cls, *, key, keyValue, id, clockId, targetId):
        """
        **LLM Docstring**

        Build a `requestAnimationFrame`-driven JavaScript interpolator for animating a
        per-vertex color array (which X3DOM can't interpolate natively).

        :param args: the interpolator-defining arguments
        :param kwargs: interpolator options
        :return: the interpolator nodes/scripts
        """
        ...

    @classmethod
    def get_color_array_interpolator(cls, *, key, keyValue, id, clockId, targetId):
        """
        **LLM Docstring**

        Build the color-array interpolator for animating per-vertex colors across frames.

        :param args: the interpolator-defining arguments
        :param kwargs: interpolator options
        :return: the interpolator nodes
        """
        ...

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
        ...

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
        ...

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
        ...

class X3DInterpolatingAnimator(X3DGenericAnimator):

    @classmethod
    def get_animation_objects(cls, object_attr_sets: dict[X3DObject, dict], id):
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
        ...

    @classmethod
    def frame_diffs(cls, ref: X3DObject | X3DHTML.X3DElement, test: X3DObject | X3DHTML.X3DElement, *rest: X3DObject | X3DHTML.X3DElement):
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
        ...

    @classmethod
    def from_frames(cls, frames: list[X3DObject | X3DHTML.X3DElement], **opts):
        """
        **LLM Docstring**

        Build an interpolating animation from a list of frame trees by diffing them:
        static content is kept as-is and only the changing attributes are animated.

        :param frames: the per-frame object trees
        :type frames: list
        :param opts: options for the animator
        :return: the animation (or the single frame if nothing changes)
        """
        ...
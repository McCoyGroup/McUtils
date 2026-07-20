import numpy as np
from ..JHTML import JHTML, HTML, HTMLWidgets
from ..Apps import WrapperComponent
import uuid
__all__ = ['D3']
__reload_hook__ = ['..JHTML', '..Apps']

class D3API:
    _api_versions = {}

    @classmethod
    def load(cls, version='v5'):
        ...

def short_uuid(len=6):
    ...

class D3:
    """
    Provides a namespace for encapsultating various D3 object types
    """

    class Frame(WrapperComponent):
        """
        Provides a frame in which to run D3 commands + access to the D3 handles
        """
        wrappers = dict(wrapper=JHTML.Div)
        theme = dict(wrapper={'cls': []}, item={'cls': []})

        def __init__(self, *elems, version='v5', id=None, javascript_handles=None, dynamic=None, **attrs):
            ...

        def canonicalize_element(self, e):
            ...

        def call(self, commands, id=None, debug=False, **call_kwargs):
            ...

        def props(self, props, id=None):
            ...

        def select(self, id):
            ...

        def attr(self, execute=True, id=None, **attrs):
            ...

        def set_id(self, id, parent_id=None):
            ...

        def append(self, shape, id=None, parent_id=None, debug=False, **attrs):
            ...

        def insert(self, before_id, shape, id=None, parent_id=None, debug=False, **attrs):
            ...

        def remove(self, id=None):
            ...

        def transition(self, id=None):
            ...

        class CallChain:

            def __init__(self, frame, commands, id=None):
                ...

            def __getattr__(self, command):
                ...

            class call:

                def __init__(self, parent, command):
                    ...

                def __call__(self, *args):
                    ...

            def execute(self):
                ...

        class Selection:

            def __init__(self, frame, handle):
                ...

            def call(self, commands):
                ...

            def props(self, properties):
                ...

            def transition(self):
                ...
    _cls_map = None

    @classmethod
    def get_class_map(cls):
        ...

    class D3Element(HTML.XMLElement):
        """
        Provides a hook into the XMLElement API to provide a model
        that can talk with `d3` through a `D3.Frame`
        """

        def __init__(self, tag, *elems, frame: 'D3.Frame'=None, id=None, on_update=None, style=None, activator=None, **attrs):
            ...

        def __repr__(self):
            ...

        @property
        def frame(self):
            ...

        @frame.setter
        def frame(self, frame):
            ...

        def set_frame(self, frame, parent_id=None):
            ...

        @property
        def id(self):
            ...

        def set_id(self, parent_id, overwrite=False):
            ...

        def initialize(self, parent_id=None):
            ...

        def initialize_children(self):
            ...

        def to_d3(self):
            ...

        def __setitem__(self, item, value):
            ...

        def insert(self, where, child):
            ...

        def set_elems(self, elems):
            ...

        @staticmethod
        def _on_update(element: 'D3.D3Element', key, value, old_value, caller, subkey=None):
            ...

        def reset_attributes(self, new_attrs, old_attrs):
            ...

        def set_attribute(self, attr, new_value, old_value):
            ...

        def insert_child(self, where, new_value: 'D3.D3Element'):
            ...

        def replace_child(self, where, old, new: 'D3.D3Element'):
            ...

        def reset_children(self, new_children: 'Iterable[D3.D3Element]', old_children: 'Iterable[D3.D3Element]'):
            ...

        def _wrap_d3(self, e) -> 'D3.D3Element':
            ...

    class TagElement(D3Element):
        tag = None

        def __init__(self, *elems, frame=None, **attrs):
            ...

        def __call__(self, *elems, **kwargs):
            ...

    class A(TagElement):
        tag = 'a'
    Link = A

    class Animate(TagElement):
        tag = 'animate'

    class AnimateMotion(TagElement):
        tag = 'animateMotion'

    class AnimateTransform(TagElement):
        tag = 'animateTransform'

    class Circle(TagElement):
        tag = 'circle'

    class ClipPath(TagElement):
        tag = 'clipPath'

    class Defs(TagElement):
        tag = 'defs'
    Definitions = Defs

    class Desc(TagElement):
        tag = 'desc'
    Description = Desc

    class Ellipse(TagElement):
        tag = 'ellipse'

    class FeBlend(TagElement):
        tag = 'feBlend'
    FilterBlend = FeBlend

    class FeColorMatrix(TagElement):
        tag = 'feColorMatrix'
    FilterColorMatrix = FeColorMatrix

    class FeComponentTransfer(TagElement):
        tag = 'feComponentTransfer'
    FilterComponentTransfer = FeComponentTransfer

    class FeComposite(TagElement):
        tag = 'feComposite'
    FilterComposite = FeComposite

    class FeConvolveMatrix(TagElement):
        tag = 'feConvolveMatrix'
    FilterConvolveMatrix = FeConvolveMatrix

    class FeDiffuseLighting(TagElement):
        tag = 'feDiffuseLighting'
    FilterDiffuseLighting = FeDiffuseLighting

    class FeDisplacementMap(TagElement):
        tag = 'feDisplacementMap'
    FilterDisplacementMap = FeDisplacementMap

    class FeDistantLight(TagElement):
        tag = 'feDistantLight'
    FilterDistantLight = FeDistantLight

    class FeDropShadow(TagElement):
        tag = 'feDropShadow'
    FilterDropShadow = FeDropShadow

    class FeFlood(TagElement):
        tag = 'feFlood'
    FilterFlood = FeFlood

    class FeFuncA(TagElement):
        tag = 'feFuncA'
    FilterAlphaChannelFunction = FeFuncA

    class FeFuncB(TagElement):
        tag = 'feFuncB'
    FilterBlueChannelFunction = FeFuncB

    class FeFuncG(TagElement):
        tag = 'feFuncG'
    FilterGreenChannelFunction = FeFuncG

    class FeFuncR(TagElement):
        tag = 'feFuncR'
    FilterRedChannelFunction = FeFuncR

    class FeGaussianBlur(TagElement):
        tag = 'feGaussianBlur'
    FilterGaussianBlur = FeGaussianBlur

    class FeImage(TagElement):
        tag = 'feImage'
    FilterImage = FeImage

    class FeMerge(TagElement):
        tag = 'feMerge'
    FilterMerge = FeMerge

    class FeMergeNode(TagElement):
        tag = 'feMergeNode'
    FilterMergeNode = FeMergeNode

    class FeMorphology(TagElement):
        tag = 'feMorphology'
    FilterMorphology = FeMorphology

    class FeOffset(TagElement):
        tag = 'feOffset'
    FilterOffset = FeOffset

    class FePointLight(TagElement):
        tag = 'fePointLight'
    FilterPointLight = FePointLight

    class FeSpecularLighting(TagElement):
        tag = 'feSpecularLighting'
    FilterSpecularLighting = FeSpecularLighting

    class FeSpotLight(TagElement):
        tag = 'feSpotLight'
    FilterSpotLight = FeSpotLight

    class FeTile(TagElement):
        tag = 'feTile'
    FilterTile = FeTile

    class FeTurbulence(TagElement):
        tag = 'feTurbulence'
    FilterTurbulence = FeTurbulence

    class Filter(TagElement):
        tag = 'filter'

    class ForeignObject(TagElement):
        tag = 'foreignObject'

    class G(TagElement):
        tag = 'g'
    Group = G

    class Hatch(TagElement):
        tag = 'hatch'

    class HatchPath(TagElement):
        tag = 'hatchpath'

    class Image(TagElement):
        tag = 'image'

    class Line(TagElement):
        tag = 'line'

    class LinearGradient(TagElement):
        tag = 'linearGradient'

    class Marker(TagElement):
        tag = 'marker'

    class Mask(TagElement):
        tag = 'mask'

    class Metadata(TagElement):
        tag = 'metadata'

    class MPath(TagElement):
        tag = 'mpath'
    MotionPath = MPath

    class Path(TagElement):
        tag = 'path'

    class Pattern(TagElement):
        tag = 'pattern'

    class Polygon(TagElement):
        tag = 'polygon'

    class Polyline(TagElement):
        tag = 'polyline'

    class RadialGradient(TagElement):
        tag = 'radialGradient'

    class Rect(TagElement):
        tag = 'rect'

    class Script(TagElement):
        tag = 'script'

    class Set(TagElement):
        tag = 'set'

    class SolidColor(TagElement):
        tag = 'solidcolor'

    class Stop(TagElement):
        tag = 'stop'

    class Style(TagElement):
        tag = 'style'

    class SVG(TagElement):
        tag = 'svg'

    class Switch(TagElement):
        tag = 'switch'

    class Symbol(TagElement):
        tag = 'symbol'

    class Text(TagElement):
        tag = 'text'

    class TextPath(TagElement):
        tag = 'textPath'

    class Title(TagElement):
        tag = 'title'

    class Tspan(TagElement):
        tag = 'tspan'
    TextSpan = Tspan

    class Use(TagElement):
        tag = 'use'

    class View(TagElement):
        tag = 'view'

    class Plots:
        """
        Helper namespace for wrapping matplotlib plots
        """

        @classmethod
        def use_as_backend(cls):
            ...

        @classmethod
        def get_plot_object(cls, figure):
            ...

        @classmethod
        def render_mpl(cls, figure, mpl_objs):
            ...

        @classmethod
        def get_mpl_plot_bounds(cls, figure):
            ...

        @classmethod
        def to_plot_coords(cls, figure, data_points):
            ...
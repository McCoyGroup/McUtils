"""
Provides Graphics base classes that can be extended upon
"""
import os, weakref, numpy as np, functools
from .Properties import GraphicsPropertyManager, GraphicsPropertyManager3D
from .Styling import Styled, ThemeManager, PlotLegend
from .Backends import GraphicsBackend, GraphicsFigure, GraphicsAxes, DPI_SCALING
from .. import Devutils as dev
__all__ = ['GraphicsBase', 'Graphics', 'Graphics3D', 'GraphicsGrid']
__reload_hook__ = ['.Properties', '.Styling', '.Backends']

class GraphicsException(Exception):
    ...
from abc import *

class FigureTreeManager:
    _figure_mapping = weakref.WeakValueDictionary()
    _figure_children = weakref.WeakKeyDictionary()

    @classmethod
    def resolve_figure_graphics(cls, fig):
        """
        **LLM Docstring**

        Return the `Graphics` object registered as the owner of a backend figure.

        :param fig: the backend figure
        :return: the owning graphics object (or `None`)
        :rtype: GraphicsBase | None
        """
        ...

    @classmethod
    def add_figure_graphics(cls, fig, graphics):
        """
        **LLM Docstring**

        Register a `Graphics` object as the owner of a backend figure (the first one
        registered becomes the parent).

        :param fig: the backend figure
        :param graphics: the graphics object to register
        :type graphics: GraphicsBase
        """
        ...

    @classmethod
    def remove_figure_mapping(cls, fig):
        """
        **LLM Docstring**

        Drop the registration for a backend figure and its child graphics.

        :param fig: the backend figure
        """
        ...

    @classmethod
    def get_child_graphics(cls, fig):
        """
        **LLM Docstring**

        Return the child `Graphics` objects registered against a backend figure.

        :param fig: the backend figure
        :return: the child graphics
        """
        ...
    _axes_mapping = weakref.WeakValueDictionary()
    _axes_children = weakref.WeakKeyDictionary()

    @classmethod
    def resolve_axes_graphics(cls, axes):
        """
        **LLM Docstring**

        Return the `Graphics` object registered as the owner of a backend axes (for
        insets).

        :param axes: the backend axes
        :return: the owning graphics object (or `None`)
        :rtype: GraphicsBase | None
        """
        ...

    @classmethod
    def add_axes_graphics(cls, axes, graphics):
        """
        **LLM Docstring**

        Register a `Graphics` object as the owner of a backend axes (for insets).

        :param axes: the backend axes
        :param graphics: the graphics object to register
        :type graphics: GraphicsBase
        """
        ...

    @classmethod
    def remove_axes_mapping(cls, axes):
        """
        **LLM Docstring**

        Drop the registration for a backend axes and its child graphics.

        :param axes: the backend axes
        """
        ...

    @classmethod
    def get_axes_child_graphics(cls, axes):
        """
        **LLM Docstring**

        Return the child `Graphics` objects registered against a backend axes.

        :param axes: the backend axes
        :return: the child graphics
        """
        ...

class GraphicsBase(metaclass=ABCMeta):
    """
    The base class for all things Graphics
    Defines the common parts of the interface
    """

    @staticmethod
    def _split_props_list(props, filter_set):
        """
        **LLM Docstring**

        Split an options dict into the entries whose keys are in a filter set and the
        entries that aren't.

        :param props: the options
        :type props: dict
        :param filter_set: the keys to include in the first result
        :return: `(included, excluded)`
        :rtype: tuple
        """
        ...

    def get_raw_attr(self, key):
        """
        **LLM Docstring**

        Read the stored (underscore-prefixed) value for an option, checking the object
        itself and then its property manager.

        :param key: the option name
        :type key: str
        :return: the stored value
        :raises AttributeError: if neither the object nor the property manager has it
        """
        ...

    def _get_def_opt(self, key, val, theme, parent=None):
        """
        **LLM Docstring**

        Resolve an option's value, falling back (when `val` is `None`) to the stored
        value, the parent's value, the class default style, and finally the theme.

        :param key: the option name
        :type key: str
        :param val: an explicit value (returned as-is if not `None`)
        :param theme: the theme dict to fall back to
        :param parent: a parent graphics object to inherit from
        :type parent: GraphicsBase | None
        :return: the resolved value
        """
        ...

    def _update_copy_opt(self, key, val):
        """
        **LLM Docstring**

        Record an option change in the stored init-options (used so copies reproduce the
        change), unless still inside `__init__` or the value is unchanged.

        :param key: the option name
        :type key: str
        :param val: the new value
        """
        ...

    def __init__(self, *args, name=None, figure=None, tighten=False, axes=None, subplot_kw=None, parent=None, image_size=None, padding=None, aspect_ratio=None, interactive=None, reshowable=None, backend='matplotlib', backend_options=None, theme=None, prop_manager=GraphicsPropertyManager, theme_manager=ThemeManager, managed=None, strict=True, **opts):
        """
        :param args:
        :type args:
        :param figure:
        :type figure: GraphicsFigure | None
        :param axes:
        :type axes: GraphicsAxes | None
        :param subplot_kw:
        :type subplot_kw: dict | None
        :param parent:
        :type parent: GraphicsBase | None
        :param opts:
        :type opts:
        """
        ...

    def initialize_figure_and_axes(self, figure, axes, *args, **kw) -> 'tuple[GraphicsFigure, GraphicsAxes]':
        """Initializes the subplots for the Graphics object

        :param figure:
        :type figure:
        :param axes:
        :type axes:
        :param args:
        :type args:
        :param kw:
        :type kw:
        :return: figure, axes
        :rtype: GraphicsFigure, GraphicsAxes
        """
        ...

    @property
    def parent(self):
        """
        **LLM Docstring**

        The owning graphics object for this figure/axes (self if this is the parent).

        :return: the parent graphics
        :rtype: GraphicsBase
        """
        ...

    @property
    def figure_parent(self):
        """
        **LLM Docstring**

        The graphics object that owns this object's backend figure.

        :return: the figure's owner
        :rtype: GraphicsBase
        """
        ...

    @property
    def inset(self):
        """
        **LLM Docstring**

        Whether this graphics object is an inset (its axes differ from the figure
        parent's axes and it isn't managed).

        :return: whether it's an inset
        :rtype: bool
        """
        ...

    @property
    def children(self):
        """
        **LLM Docstring**

        The child graphics registered against this object's figure/axes (or `None` if
        this isn't the parent).

        :return: the child graphics
        """
        ...

    @property
    def event_handlers(self):
        """
        **LLM Docstring**

        The bound event-handler data, if any.

        :return: the event handlers
        """
        ...

    @property
    def animated(self):
        """
        **LLM Docstring**

        The animation specification for this figure.

        :return: the animation spec
        """
        ...

    def bind_events(self, *handlers, **events):
        """
        **LLM Docstring**

        Bind interactive event handlers to the figure.

        :param handlers: a handlers dict (or handler pairs)
        :param events: additional event-name/handler keyword pairs
        """
        ...

    def create_animation(self, *args, **opts):
        """
        **LLM Docstring**

        Create (and start) an animator for the figure from the given frame
        specification.

        :param args: the animation frames/spec
        :param opts: options for the animator
        """
        ...

    def animate_frames(self, frames, **opts):
        """
        **LLM Docstring**

        Prepare the figure and animate the supplied frames via the backend.

        :param frames: the animation frames
        :param opts: animation options
        :return: the animation
        """
        ...
    known_keys = layout_keys

    def _check_opts(self, opts):
        """
        **LLM Docstring**

        Raise if any of the supplied option keys aren't recognized (in `known_keys`).

        :param opts: the options to check
        :type opts: dict
        :raises ValueError: for unknown option keys
        """
        ...

    def set_options(self, event_handlers=None, animated=None, prolog=None, epilog=None, strict=True, **opts):
        """Sets options for the plot
        :param event_handlers:
        :param animated:
        :param opts:
        :type opts:
        :return:
        :rtype:
        """
        ...

    @property
    def prolog(self):
        """
        **LLM Docstring**

        The prolog graphics primitives drawn before the main content. Setting it records
        the change for copying.

        :return: the prolog primitives
        """
        ...

    @prolog.setter
    def prolog(self, p):
        """
        **LLM Docstring**

        The prolog graphics primitives drawn before the main content. Setting it records
        the change for copying.

        :return: the prolog primitives
        """
        ...

    @property
    def epilog(self):
        """
        **LLM Docstring**

        The epilog graphics primitives drawn after the main content. Setting it records
        the change for copying.

        :return: the epilog primitives
        """
        ...

    @epilog.setter
    def epilog(self, e):
        """
        **LLM Docstring**

        The epilog graphics primitives drawn after the main content. Setting it records
        the change for copying.

        :return: the epilog primitives
        """
        ...

    @property
    def opts(self):
        """
        **LLM Docstring**

        The current values of the tracked `opt_keys` options, as a dict.

        :return: the options dict
        :rtype: dict
        """
        ...

    def copy(self, **kwargs):
        """Creates a copy of the object with new axes and a new figure

        :return:
        :rtype:
        """
        ...

    def _get_init_opts(self, parent_opts, unmerged_keys=None):
        """
        **LLM Docstring**

        Return the stored init-options, dropping layout keys that are being supplied by
        the parent (so they aren't doubly applied on copy).

        :param parent_opts: the options being inherited from the parent
        :type parent_opts: dict
        :param unmerged_keys: the keys to drop when present in `parent_opts`
        :return: the init options
        :rtype: dict
        """
        ...

    def change_figure(self, new, *init_args, figs=None, **init_kwargs):
        """Creates a copy of the object with new axes and a new figure

        :return:
        :rtype:
        """
        ...

    def _get_init_args(self, *init_args):
        """
        **LLM Docstring**

        Return the positional construction arguments to reuse when copying (identity by
        default).

        :param init_args: the supplied positional args
        :return: the positional args
        :rtype: tuple
        """
        ...

    def _change_figure(self, new, *init_args, parent_opts=None, **init_kwargs):
        """Creates a copy of the object with new axes and a new figure

        :return:
        :rtype:
        """
        ...

    def _prep_show(self, parent=False):
        """
        **LLM Docstring**

        Prepare this object for display: re-apply options, draw the prolog/epilog, tighten
        the layout if requested, and prep the figure and axes.

        :param parent: whether this is the parent of the figure
        :type parent: bool
        :return: self
        :rtype: GraphicsBase
        """
        ...

    def prep_show(self):
        """
        **LLM Docstring**

        Prepare the whole figure tree (parent and children) for display.

        :return: self
        :rtype: GraphicsBase
        """
        ...

    def show(self, reshow=None):
        """
        **LLM Docstring**

        Display the figure, preparing it first and (temporarily) enabling interactivity
        as needed; makes a copy if the figure was already shown and isn't reshowable.

        :param reshow: force a reshow of an already-shown figure
        :type reshow: bool | None
        :return: the backend's show result
        """
        ...

    def close(self, force=False):
        """
        **LLM Docstring**

        Close the figure (or remove the inset axes), cleaning up the figure registration
        when this object owns it.

        :param force: close even if this object isn't the registered owner
        :type force: bool
        """
        ...

    def __del__(self):
        """
        **LLM Docstring**

        Close the figure on garbage collection (ignoring teardown errors).
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation showing the type, name/id, and backing figure.

        :return: the representation
        :rtype: str
        """
        ...

    def clear(self):
        """
        **LLM Docstring**

        Clear the drawn content from the axes.
        """
        ...
    _display_locks = set()

    def _ipython_display_(self):
        """
        **LLM Docstring**

        Display the figure in IPython (guarded against re-entrant display calls).
        """
        ...

    def _repr_html_(self):
        """
        **LLM Docstring**

        Return the figure's HTML representation for IPython.

        :return: the HTML
        :rtype: str
        """
        ...

    def get_mime_bundle(self):
        """
        **LLM Docstring**

        Return the figure's MIME bundle (HTML or PNG) for rich display.

        :return: the MIME bundle
        :rtype: dict
        """
        ...

    def savefig(self, where, expanduser=True, format=None, **kw):
        """
        Saves the image to file
        :param where:
        :type where:
        :param format:
        :type format:
        :param kw:
        :type kw:
        :return: file it was saved to (I think...?)
        :rtype: str
        """
        ...

    def to_png(self):
        """
        Used by Jupyter and friends to make a version of the image that they can display, hence the extra 'tight_layout' call
        :return:
        :rtype:
        """
        ...

    def to_widget(self):
        """
        **LLM Docstring**

        Prepare the figure and return it as an interactive backend widget.

        :return: the widget
        """
        ...

    def _repr_png_(self):
        """
        **LLM Docstring**

        Return the figure's PNG bytes for IPython.

        :return: the PNG data
        :rtype: bytes
        """
        ...

    def create_colorbar_axis(self, figure=None, size=(20, 200), tick_padding=40, origin=None, orientation='vertical', alignment=None):
        """
        **LLM Docstring**

        Create an inset axis positioned to hold a colorbar, expanding the figure padding
        (and compensating the panel spacings) so the colorbar fits.

        :param figure: the figure to add the axis to (defaults to this one)
        :param size: the colorbar `(width, height)` (fractional if < 1)
        :param tick_padding: extra space for the colorbar ticks
        :param origin: the colorbar origin (auto-placed if omitted)
        :param orientation: `'vertical'` or `'horizontal'`
        :type orientation: str
        :param alignment: the origin alignment within the colorbar box
        :return: the colorbar axis
        :rtype: GraphicsAxes
        """
        ...
    _default_colorbar_size = (20, 200)

    def add_colorbar(self, graphics=None, norm=None, cmap=None, size=None, orientation='vertical', origin=None, tick_padding=40, colorbar_axes=None, cax=None, **kw):
        """
        **LLM Docstring**

        Add a colorbar to the figure, creating (and tracking) a dedicated colorbar axis
        if one isn't supplied.

        :param graphics: the mappable/graphics the colorbar describes
        :param norm: the color normalization
        :param cmap: the colormap
        :param size: the colorbar size (auto by orientation if omitted)
        :param orientation: `'vertical'` or `'horizontal'`
        :type orientation: str
        :param origin: the colorbar origin
        :param tick_padding: space for the ticks
        :param colorbar_axes: an explicit colorbar axis
        :param cax: an alias for the colorbar graphics
        :param kw: extra options for the backend colorbar
        :return: the colorbar
        """
        ...
    inset_options = dict()
    axes_keys = set()
    _axes_padding_offset = [1, 0]

    def create_inset(self, bbox, coordinates='scaled', graphics_class=None, **opts):
        """
        **LLM Docstring**

        Create an inset graphics object within this figure, converting the bbox from the
        requested coordinate system into figure-scaled coordinates.

        :param bbox: the inset bounding box
        :param coordinates: `'scaled'` (within the frame) or `'absolute'`
        :type coordinates: str
        :param graphics_class: the class of the inset (defaults to this type)
        :param opts: options for the inset graphics
        :return: the inset graphics object
        :rtype: GraphicsBase
        """
        ...

class Graphics(GraphicsBase):
    figure_keys = {'scale', 'aspect_ratioimage_size', 'padding', 'spacings', 'background', 'colorbar'}
    layout_keys = axes_keys | figure_keys | GraphicsBase.layout_keys
    known_keys = layout_keys

    def set_options(self, axes_labels=None, plot_label=None, style_list=None, plot_range=None, plot_legend=None, legend_style=None, frame=None, frame_style=None, ticks=None, scale=None, padding=None, spacings=None, ticks_style=None, ticks_label_style=None, image_size=None, axes_bbox=None, aspect_ratio=None, background=None, colorbar=None, prolog=None, epilog=None, **parent_opts):
        """
        **LLM Docstring**

        Set the plot's styling and layout options (labels, legend, frame, ticks, range,
        scale, padding, spacings, background, colorbar, etc.), resolving defaults and
        applying each non-`None` value.

        :param axes_labels: the axis labels
        :param plot_label: the plot title
        :param style_list: the per-series style cycle
        :param plot_range: the plotted data range
        :param plot_legend: the legend (or legend spec)
        :param legend_style: legend styling
        :param frame: which frame edges to draw
        :param frame_style: frame styling
        :param ticks: the tick specification
        :param scale: the axis scaling
        :param padding: the figure padding
        :param spacings: the panel spacings
        :param ticks_style: tick styling
        :param ticks_label_style: tick-label styling
        :param image_size: the image size
        :param axes_bbox: the axes bounding box
        :param aspect_ratio: the aspect ratio
        :param background: the background color
        :param colorbar: the colorbar spec
        :param prolog: prolog primitives
        :param epilog: epilog primitives
        :param parent_opts: options forwarded to the base class
        """
        ...
    padding_line_height = 50

    def get_plot_label_padding(self, plot_label):
        """
        **LLM Docstring**

        Return the extra padding needed to fit a plot label (top padding when a label is
        present).

        :param plot_label: the plot label (or `None`)
        :return: the `((left, right), (bottom, top))` padding contribution
        :rtype: list
        """
        ...

    def get_axes_label_padding(self, axes_labels):
        """
        **LLM Docstring**

        Return the extra padding needed to fit the axis labels (left/bottom padding for
        the y/x labels).

        :param axes_labels: the axis labels (or `None`)
        :return: the `((left, right), (bottom, top))` padding contribution
        :rtype: list
        """
        ...

    def resolve_default_padding(self, padding, modifications=None):
        """
        **LLM Docstring**

        Resolve the final padding by filling unset sides from the default style and
        adding the supplied label-padding modifications.

        :param padding: the requested padding (or `None`)
        :param modifications: per-side padding contributions to add
        :type modifications: list | None
        :return: the resolved `((left, right), (bottom, top))` padding
        :rtype: tuple
        """
        ...

    @property
    def artists(self):
        """
        **LLM Docstring**

        The plot's artist objects (empty for the base `Graphics`).

        :return: the artists
        :rtype: list
        """
        ...

    @property
    def plot_label(self):
        """
        **LLM Docstring**

        The plot title/label. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the plot label value
        """
        ...

    @plot_label.setter
    def plot_label(self, value):
        """
        **LLM Docstring**

        The plot title/label. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the plot label value
        """
        ...

    @property
    def style_list(self):
        """
        **LLM Docstring**

        The per-series style cycle (shared with the parent). Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the style list value
        """
        ...

    @style_list.setter
    def style_list(self, value):
        """
        **LLM Docstring**

        The per-series style cycle (shared with the parent). Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the style list value
        """
        ...

    @property
    def plot_legend(self):
        """
        **LLM Docstring**

        The plot legend (or legend spec). Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the plot legend value
        """
        ...

    @plot_legend.setter
    def plot_legend(self, value):
        """
        **LLM Docstring**

        The plot legend (or legend spec). Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the plot legend value
        """
        ...

    @property
    def legend_style(self):
        """
        **LLM Docstring**

        The legend styling options. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the legend style value
        """
        ...

    @legend_style.setter
    def legend_style(self, value):
        """
        **LLM Docstring**

        The legend styling options. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the legend style value
        """
        ...

    @property
    def axes_labels(self):
        """
        **LLM Docstring**

        The per-axis labels. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the axes labels value
        """
        ...

    @axes_labels.setter
    def axes_labels(self, value):
        """
        **LLM Docstring**

        The per-axis labels. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the axes labels value
        """
        ...

    @property
    def frame(self):
        """
        **LLM Docstring**

        Which frame (spine) edges are drawn. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the frame value
        """
        ...

    @frame.setter
    def frame(self, value):
        """
        **LLM Docstring**

        Which frame (spine) edges are drawn. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the frame value
        """
        ...

    @property
    def frame_style(self):
        """
        **LLM Docstring**

        The frame styling options. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the frame style value
        """
        ...

    @frame_style.setter
    def frame_style(self, value):
        """
        **LLM Docstring**

        The frame styling options. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the frame style value
        """
        ...

    @property
    def plot_range(self):
        """
        **LLM Docstring**

        The plotted data range per axis. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the plot range value
        """
        ...

    @plot_range.setter
    def plot_range(self, value):
        """
        **LLM Docstring**

        The plotted data range per axis. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the plot range value
        """
        ...

    @property
    def ticks(self):
        """
        **LLM Docstring**

        The tick locations/specification. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the ticks value
        """
        ...

    @ticks.setter
    def ticks(self, value):
        """
        **LLM Docstring**

        The tick locations/specification. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the ticks value
        """
        ...

    @property
    def ticks_style(self):
        """
        **LLM Docstring**

        The tick styling options. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the ticks style value
        """
        ...

    @ticks_style.setter
    def ticks_style(self, value):
        """
        **LLM Docstring**

        The tick styling options. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the ticks style value
        """
        ...

    @property
    def ticks_label_style(self):
        """
        **LLM Docstring**

        The tick-label styling options. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the tick-label style value
        """
        ...

    @ticks_label_style.setter
    def ticks_label_style(self, value):
        """
        **LLM Docstring**

        The tick-label styling options. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the tick-label style value
        """
        ...

    @property
    def scale(self):
        """
        **LLM Docstring**

        The axis scaling (e.g. linear/log). Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the scale value
        """
        ...

    @scale.setter
    def scale(self, value):
        """
        **LLM Docstring**

        The axis scaling (e.g. linear/log). Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the scale value
        """
        ...

    @property
    def axes_bbox(self):
        """
        **LLM Docstring**

        The axes bounding box within the figure. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the axes bbox value
        """
        ...

    @axes_bbox.setter
    def axes_bbox(self, value):
        """
        **LLM Docstring**

        The axes bounding box within the figure. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the axes bbox value
        """
        ...

    @property
    def aspect_ratio(self):
        """
        **LLM Docstring**

        The axes aspect ratio. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the aspect ratio value
        """
        ...

    @aspect_ratio.setter
    def aspect_ratio(self, value):
        """
        **LLM Docstring**

        The axes aspect ratio. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the aspect ratio value
        """
        ...

    @property
    def image_size(self):
        """
        **LLM Docstring**

        The figure image size in pixels. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the image size value
        """
        ...

    @image_size.setter
    def image_size(self, value):
        """
        **LLM Docstring**

        The figure image size in pixels. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the image size value
        """
        ...

    @property
    def figure_label(self):
        """
        **LLM Docstring**

        The overall figure label. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the figure label value
        """
        ...

    @figure_label.setter
    def figure_label(self, value):
        """
        **LLM Docstring**

        The overall figure label. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the figure label value
        """
        ...

    @property
    def padding(self):
        """
        **LLM Docstring**

        The figure padding on each side. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the padding value
        """
        ...

    @padding.setter
    def padding(self, value):
        """
        **LLM Docstring**

        The figure padding on each side. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the padding value
        """
        ...

    @property
    def padding_left(self):
        """
        **LLM Docstring**

        The left figure padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the left padding value
        """
        ...

    @padding_left.setter
    def padding_left(self, value):
        """
        **LLM Docstring**

        The left figure padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the left padding value
        """
        ...

    @property
    def padding_right(self):
        """
        **LLM Docstring**

        The right figure padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the right padding value
        """
        ...

    @padding_right.setter
    def padding_right(self, value):
        """
        **LLM Docstring**

        The right figure padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the right padding value
        """
        ...

    @property
    def padding_top(self):
        """
        **LLM Docstring**

        The top figure padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the top padding value
        """
        ...

    @padding_top.setter
    def padding_top(self, value):
        """
        **LLM Docstring**

        The top figure padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the top padding value
        """
        ...

    @property
    def padding_bottom(self):
        """
        **LLM Docstring**

        The bottom figure padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the bottom padding value
        """
        ...

    @padding_bottom.setter
    def padding_bottom(self, value):
        """
        **LLM Docstring**

        The bottom figure padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the bottom padding value
        """
        ...

    @property
    def spacings(self):
        """
        **LLM Docstring**

        The inter-panel spacings. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the spacings value
        """
        ...

    @spacings.setter
    def spacings(self, value):
        """
        **LLM Docstring**

        The inter-panel spacings. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the spacings value
        """
        ...

    @property
    def background(self):
        """
        **LLM Docstring**

        The figure background color. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the background value
        """
        ...

    @background.setter
    def background(self, value):
        """
        **LLM Docstring**

        The figure background color. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the background value
        """
        ...

    @property
    def colorbar(self):
        """
        **LLM Docstring**

        The colorbar specification. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the colorbar value
        """
        ...

    @colorbar.setter
    def colorbar(self, value):
        """
        **LLM Docstring**

        The colorbar specification. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the colorbar value
        """
        ...

    def _prep_show(self, parent=False):
        """
        **LLM Docstring**

        Prepare the plot for display, additionally drawing the legend and re-applying the
        ticks when this is the parent figure.

        :param parent: whether this is the parent of the figure
        :type parent: bool
        """
        ...

    def get_padding_offsets(self):
        """
        **LLM Docstring**

        Compute the padding, expressed in plot-data coordinates, on each side of the
        axes (from the pixel padding and the plot range).

        :return: the `((left, right), (bottom, top))` data-coordinate offsets
        :rtype: list
        """
        ...

    def get_bbox(self):
        """
        **LLM Docstring**

        Return the effective bounding box (in plot-data coordinates) of the total space
        the figure occupies, including padding.

        :return: the `[(min_x, min_y), (max_x, max_y)]` bbox
        :rtype: list
        """
        ...

    def create_inset(self, bbox, coordinates='absolute', graphics_class=None, **opts):
        """
        **LLM Docstring**

        Create an inset within this plot, converting an absolute-data-coordinate bbox
        into frame-scaled coordinates first.

        :param bbox: the inset bounding box
        :param coordinates: `'absolute'` (data coordinates) or `'scaled'`
        :type coordinates: str
        :param graphics_class: the inset class (defaults to `Graphics`)
        :param opts: options for the inset
        :return: the inset graphics object
        :rtype: Graphics
        """
        ...

class Graphics3D(Graphics):
    default_style = Graphics.default_style | dict(frame=((True, False), (True, False), (True, False)))
    opt_keys = GraphicsBase.opt_keys | {'view_settings', 'box_ratios', 'projection_type', 'autoscale', 'aspect_ratio'}
    known_keys = Graphics.opt_keys | {'animate'}

    def __init__(self, *args, figure=None, axes=None, subplot_kw=None, event_handlers=None, animate=None, axes_labels=None, plot_label=None, style_list=None, plot_range=None, plot_legend=None, ticks=None, scale=None, ticks_style=None, image_size=None, background=None, view_settings=None, box_ratios=None, projection_type=None, aspect_ratio=None, autoscale=None, backend='matplotlib3D', **kwargs):
        """
        **LLM Docstring**

        Set up a 3D plot, forwarding the 2D styling options to `Graphics` and adding the
        3D-specific ones (view settings, box ratios, projection, autoscale) with a 3D
        backend and property manager.

        :param args: positional plot arguments
        :param figure: an existing figure to draw into
        :param axes: existing axes to draw into
        :param subplot_kw: subplot construction options
        :type subplot_kw: dict | None
        :param event_handlers: interactive event handlers
        :param animate: an animation specification
        :param axes_labels: the axis labels
        :param plot_label: the plot title
        :param style_list: the style cycle
        :param plot_range: the data range
        :param plot_legend: the legend
        :param ticks: the tick specification
        :param scale: the axis scaling
        :param ticks_style: tick styling
        :param image_size: the image size
        :param background: the background color
        :param view_settings: the 3D camera/view settings
        :param box_ratios: the 3D box aspect ratios
        :param projection_type: the projection (e.g. perspective/ortho)
        :param aspect_ratio: the aspect ratio
        :param autoscale: the autoscale setting
        :param backend: the plotting backend
        :type backend: str
        :param kwargs: extra options
        """
        ...

    def set_options(self, view_settings=None, box_ratios=None, projection_type=None, aspect_ratio=None, autoscale=None, **parent_opts):
        """
        **LLM Docstring**

        Set the 3D-specific options (view settings, box ratios, projection, autoscale,
        aspect ratio) on top of the base options.

        :param view_settings: the 3D view settings
        :param box_ratios: the 3D box aspect ratios
        :param projection_type: the projection type
        :param aspect_ratio: the aspect ratio
        :param autoscale: the autoscale setting
        :param parent_opts: options forwarded to `Graphics.set_options`
        """
        ...

    @property
    def box_ratios(self):
        """
        **LLM Docstring**

        The 3D box aspect ratios. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the box ratios value
        """
        ...

    @box_ratios.setter
    def box_ratios(self, value):
        """
        **LLM Docstring**

        The 3D box aspect ratios. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the box ratios value
        """
        ...

    @property
    def autoscale(self):
        """
        **LLM Docstring**

        Whether the 3D axes autoscale. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the autoscale value
        """
        ...

    @autoscale.setter
    def autoscale(self, value):
        """
        **LLM Docstring**

        Whether the 3D axes autoscale. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the autoscale value
        """
        ...

    @property
    def projection_type(self):
        """
        **LLM Docstring**

        The 3D projection type. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the projection type value
        """
        ...

    @projection_type.setter
    def projection_type(self, value):
        """
        **LLM Docstring**

        The 3D projection type. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the projection type value
        """
        ...

    @property
    def view_settings(self):
        """
        **LLM Docstring**

        The 3D camera/view settings. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the view settings value
        """
        ...

    @view_settings.setter
    def view_settings(self, value):
        """
        **LLM Docstring**

        The 3D camera/view settings. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the view settings value
        """
        ...

    def _prep_show(self, parent=False):
        """
        **LLM Docstring**

        Prepare the 3D plot for display, resolving `'auto'` box ratios to a concrete
        aspect ratio.

        :param parent: whether this is the parent of the figure
        :type parent: bool
        """
        ...

class GraphicsGrid(GraphicsBase):
    """
    A class for easily building sophisticated multi-panel figures.
    Robustification work still needs to be done, but the core interface is there.
    Supports themes & direct, easy access to the panels, among other things.
    Builds off of `GraphicsBase`.
    """
    default_style = dict(theme='mccoy', spacings=(50, 0), padding=((50, 10), (50, 10)))
    layout_keys = GraphicsBase.layout_keys | {'nrows', 'ncols'}
    known_keys = GraphicsBase.known_keys | {'graphics_class'}

    def __init__(self, *args, nrows=None, ncols=None, graphics_class=Graphics, figure=None, axes=None, subplot_kw=None, subimage_size=(310, 310), subimage_aspect_ratio='auto', padding=None, spacings=None, **opts):
        """
        **LLM Docstring**

        Build a multi-panel figure grid, inferring the shape from any supplied graphics,
        sizing the figure from the sub-image size/padding/spacings, and populating the
        panels.

        :param args: an optional nested list of graphics to place in the grid
        :param nrows: the number of rows
        :type nrows: int | None
        :param ncols: the number of columns
        :type ncols: int | None
        :param graphics_class: the class used for each panel
        :param figure: an existing figure to draw into
        :param axes: existing axes to draw into
        :param subplot_kw: subplot construction options
        :type subplot_kw: dict | None
        :param subimage_size: the per-panel image size
        :param subimage_aspect_ratio: the per-panel aspect ratio
        :param padding: the grid padding
        :param spacings: the inter-panel spacings
        :param opts: extra options
        """
        ...

    class GraphicsStack:

        def __init__(self, parent, graphics):
            """
            **LLM Docstring**

            Wrap the grid's panel graphics as an object array for indexed access and
            broadcast calls.

            :param parent: the owning grid
            :type parent: GraphicsBase
            :param graphics: the panel graphics
            """
            ...

        def __getitem__(self, item):
            """
            **LLM Docstring**

            Index into the panel stack.

            :param item: the index
            :return: the panel(s)
            """
            ...

        def __setitem__(self, item, value):
            """
            **LLM Docstring**

            Assign into the panel stack.

            :param item: the index
            :param value: the panel(s)
            """
            ...

        def _call_iter(self, attr):
            """
            **LLM Docstring**

            Return a callable that invokes a `Graphics` method on every panel, yielding each
            result.

            :param attr: the method name
            :type attr: str
            :return: the broadcasting callable
            :rtype: Callable
            """
            ...

        def _axes_call_iter(self, attr):
            """
            **LLM Docstring**

            Return a callable that invokes a backend-axes method on every panel's axes,
            yielding each result.

            :param attr: the method name
            :type attr: str
            :return: the broadcasting callable
            :rtype: Callable
            """
            ...

        def get_bboxes(self):
            """
            **LLM Docstring**

            Return each panel's bounding box.

            :return: the per-panel bounding boxes
            :rtype: list
            """
            ...

        def get_bbox(self):
            """
            **LLM Docstring**

            Return the bounding box enclosing all panels.

            :return: the combined bounding box
            :rtype: list
            """
            ...

        def get_padding(self):
            """
            **LLM Docstring**

            Compute the grid's outer padding from the panels' paddings.

            :return: the `((left, right), (bottom, top))` padding
            :rtype: list
            """
            ...

        def set_facecolor(self, fg):
            """
            **LLM Docstring**

            No-op face-color setter (panels manage their own backgrounds).

            :param fg: the (ignored) face color
            """
            ...

        def __iter__(self):
            """
            **LLM Docstring**

            Iterate over the panels (flattened).

            :return: the panel iterator
            """
            ...

    def initialize_figure_and_axes(self, figure, axes, *, nrows=None, ncols=None, graphics_class=None, fig_kw=None, subplot_kw=None, padding=None, spacings=None, subimage_size=None, subimage_aspect_ratio=None, **kw):
        """Initializes the subplots for the Graphics object

        :param figure:
        :type figure:
        :param axes:
        :type axes:
        :param args:
        :type args:
        :param kw:
        :type kw:
        :return: figure, axes
        :rtype: GraphicsBackend.Figure, GraphicsBackend.Figure.Axes
        """
        ...

    def set_options(self, padding=None, spacings=None, background=None, colorbar=None, figure_label=None, **parent_opts):
        """
        **LLM Docstring**

        Set the grid-level options (figure label, padding, spacings, background,
        colorbar) on top of the base options, recomputing the image size.

        :param padding: the grid padding
        :param spacings: the inter-panel spacings
        :param background: the background color
        :param colorbar: the colorbar spec
        :param figure_label: the overall figure label
        :param parent_opts: options forwarded to the base class
        """
        ...

    def __iter__(self):
        """
        **LLM Docstring**

        Iterate over the grid's panels.

        :return: the panel iterator
        """
        ...

    def __getitem__(self, item):
        """
        **LLM Docstring**

        Get a panel by `(row, col)` (or a flat index).

        :param item: the index
        :return: the panel
        :rtype: GraphicsBase
        """
        ...

    def __setitem__(self, item, val):
        """
        **LLM Docstring**

        Place a graphics object into a panel by `(row, col)` (or flat index), re-hosting
        it onto the grid's figure.

        :param item: the index
        :param val: the graphics object (or raw value)
        """
        ...

    def set_image(self, pos, val, **opts):
        """
        **LLM Docstring**

        Place a graphics object into the panel at `pos`, re-hosting it onto the grid's
        figure with the given options.

        :param pos: the panel position
        :param val: the graphics object
        :type val: GraphicsBase
        :param opts: options forwarded to the re-hosting
        :return: the placed panel
        :rtype: GraphicsBase
        """
        ...

    def calc_image_size(self):
        """
        **LLM Docstring**

        Compute the grid's overall image size from the panels' sizes, the inter-panel
        spacings, and the padding.

        :return: the `(width, height)` image size
        :rtype: tuple
        """
        ...

    @property
    def image_size(self):
        """
        **LLM Docstring**

        The grid's overall image size (recomputed from the panels on access).

        :return: the `(width, height)` image size
        :rtype: tuple
        """
        ...

    @image_size.setter
    def image_size(self, value):
        """
        **LLM Docstring**

        The grid's overall image size (recomputed from the panels on access).

        :return: the `(width, height)` image size
        :rtype: tuple
        """
        ...

    @property
    def figure_label(self):
        """
        **LLM Docstring**

        The overall figure label. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the figure label value
        """
        ...

    @figure_label.setter
    def figure_label(self, value):
        """
        **LLM Docstring**

        The overall figure label. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the figure label value
        """
        ...

    @property
    def padding(self):
        """
        **LLM Docstring**

        The grid's outer padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the padding value
        """
        ...

    @padding.setter
    def padding(self, value):
        """
        **LLM Docstring**

        The grid's outer padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the padding value
        """
        ...

    @property
    def padding_left(self):
        """
        **LLM Docstring**

        The grid's left padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the left padding value
        """
        ...

    @padding_left.setter
    def padding_left(self, value):
        """
        **LLM Docstring**

        The grid's left padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the left padding value
        """
        ...

    @property
    def padding_right(self):
        """
        **LLM Docstring**

        The grid's right padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the right padding value
        """
        ...

    @padding_right.setter
    def padding_right(self, value):
        """
        **LLM Docstring**

        The grid's right padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the right padding value
        """
        ...

    @property
    def padding_top(self):
        """
        **LLM Docstring**

        The grid's top padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the top padding value
        """
        ...

    @padding_top.setter
    def padding_top(self, value):
        """
        **LLM Docstring**

        The grid's top padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the top padding value
        """
        ...

    @property
    def padding_bottom(self):
        """
        **LLM Docstring**

        The grid's bottom padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the bottom padding value
        """
        ...

    @padding_bottom.setter
    def padding_bottom(self, value):
        """
        **LLM Docstring**

        The grid's bottom padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the bottom padding value
        """
        ...

    @property
    def spacings(self):
        """
        **LLM Docstring**

        The inter-panel spacings. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the spacings value
        """
        ...

    @spacings.setter
    def spacings(self, value):
        """
        **LLM Docstring**

        The inter-panel spacings. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the spacings value
        """
        ...

    @property
    def background(self):
        """
        **LLM Docstring**

        The grid background color. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the background value
        """
        ...

    @background.setter
    def background(self, value):
        """
        **LLM Docstring**

        The grid background color. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the background value
        """
        ...

    @property
    def colorbar(self):
        """
        **LLM Docstring**

        The grid colorbar specification. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the colorbar value
        """
        ...

    @colorbar.setter
    def colorbar(self, value):
        """
        **LLM Docstring**

        The grid colorbar specification. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the colorbar value
        """
        ...

    def _prep_show(self, parent=False):
        """
        **LLM Docstring**

        Prepare the grid for display: recompute the image size and re-apply the
        spacings/padding, tightening the layout if requested.

        :param parent: whether this is the parent of the figure
        :type parent: bool
        """
        ...
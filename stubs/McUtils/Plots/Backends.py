"""
For now, just a super simple Enum of supported backends
Maybe in the future we'll add better support so that the backends themselves can all support a common subset
of features, but I think we'll 90% of the time just want to use MPL or VTK so who knows...
If that happens, lots of the 'if backend == MPL' stuff will change to use a Backend object
"""
from __future__ import annotations
__all__ = ['GraphicsBackend']
import enum, abc, contextlib, numpy as np
import re
import uuid
import functools
import io
import base64
from .. import Numputils as nput
from .. import Devutils as dev
from . import VTKInterface as vtk
from ..ExternalPrograms import VPythonInterface as vpython
from . import X3DInterface as x3d
from . import SVG as svg
from .SceneJSON import SceneJSON as sceneJSON
from .Colors import ColorPalette
DPI_SCALING = 72

class AxisManager:

    def __init__(self, tick_getter, tick_setter, tick_locator, minor_tick_locator, tick_formatter, minor_tick_formatter):
        """
        **LLM Docstring**

        Hold the getter/setter/locator/formatter callables that back a single axis's tick
        management.

        :param tick_getter: returns the current tick locations
        :param tick_setter: sets the tick locations
        :param tick_locator: sets the major-tick locator
        :param minor_tick_locator: sets the minor-tick locator
        :param tick_formatter: sets the major-tick formatter
        :param minor_tick_formatter: sets the minor-tick formatter
        """
        ...

class XAxisManager(AxisManager):

    def get_xticks(self):
        """
        **LLM Docstring**

        Return the x-axis tick locations.

        :return: the result
        """
        ...

    def set_xticks(self, ticks, **kwargs):
        """
        **LLM Docstring**

        Set the x-axis tick locations.

        :param ticks: the tick locations
        :param kwargs: extra keyword options
        """
        ...

class YAxisManager(AxisManager):

    def get_yticks(self):
        """
        **LLM Docstring**

        Return the y-axis tick locations.

        :return: the result
        """
        ...

    def set_yticks(self, ticks, **kwargs):
        """
        **LLM Docstring**

        Set the y-axis tick locations.

        :param ticks: the tick locations
        :param kwargs: extra keyword options
        """
        ...

class ZAxisManager(AxisManager):

    def get_zticks(self):
        """
        **LLM Docstring**

        Return the z-axis tick locations.

        :return: the result
        """
        ...

    def set_zticks(self, ticks, **kwargs):
        """
        **LLM Docstring**

        Set the z-axis tick locations.

        :param ticks: the tick locations
        :param kwargs: extra keyword options
        """
        ...

class GraphicsAxes(metaclass=abc.ABCMeta):
    """
    A wrapper to provide a canonical form for matplotlib.axes.Axes
    so that other backends can plug in cleanly
    """

    def __init__(self):
        """
        **LLM Docstring**

        Set up the axes wrapper, building its per-axis tick managers.
        """
        ...

    def get_xaxis_manager(self):
        """
        **LLM Docstring**

        Build the x-axis tick manager for this axes.

        :return: the result
        """
        ...

    def get_yaxis_manager(self):
        """
        **LLM Docstring**

        Build the y-axis tick manager for this axes.

        :return: the result
        """
        ...

    class TicksManager:

        class Locator:
            ...

        class FixedLocator(Locator):

            def __init__(self, locs, **opts):
                """
                **LLM Docstring**

                Hold a fixed set of tick locations.

                :param locs: the tick locations
                :param opts: extra locator options
                """
                ...

    @classmethod
    def canonicalize_opts(cls, opts):
        """
        **LLM Docstring**

        Normalize construction options into the backend's canonical form.

        :param opts: the options to canonicalize
        """
        ...

    @abc.abstractmethod
    def remove(self, *, backend):
        """
        **LLM Docstring**

        Tear down (remove) this axes from its figure.

        """
        ...

    @abc.abstractmethod
    def clear(self, *, backend):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure.

        """
        ...

    def prep_show(self):
        """
        **LLM Docstring**

        Prepare the axes/figure for display.

        """
        ...

    @abc.abstractmethod
    def get_plotter(self, method):
        """
        **LLM Docstring**

        Resolve a plotting-method name to the backend callable that draws it.

        :param method: the plot-method name
        :return: the result
        """
        ...

    @abc.abstractmethod
    def get_plot_label(self):
        """
        **LLM Docstring**

        Return the plot title/label.

        :return: the result
        """
        ...

    @abc.abstractmethod
    def set_plot_label(self, val, **style):
        """
        **LLM Docstring**

        Set the plot title/label.

        :param val: the label text
        :param style: label styling options
        """
        ...

    @abc.abstractmethod
    def get_style_list(self):
        """
        **LLM Docstring**

        Return the per-series style cycle.

        :return: the result
        """
        ...

    @abc.abstractmethod
    def set_style_list(self, props):
        """
        **LLM Docstring**

        Set the per-series style cycle.

        :param props: the style cycle
        """
        ...

    @abc.abstractmethod
    def get_frame_visible(self):
        """
        **LLM Docstring**

        Return which frame (spine) edges are drawn.

        :return: the result
        """
        ...

    @abc.abstractmethod
    def set_frame_visible(self, frame_spec):
        """
        **LLM Docstring**

        Set which frame (spine) edges are drawn.

        :param frame_spec: the per-edge visibility spec
        """
        ...

    @abc.abstractmethod
    def get_frame_style(self):
        """
        **LLM Docstring**

        Return the frame (spine) styling.

        :return: the result
        """
        ...

    @abc.abstractmethod
    def set_frame_style(self, frame_spec):
        """
        **LLM Docstring**

        Set the frame (spine) styling.

        :param frame_spec: the frame styling
        """
        ...

    def get_grid_visible(self):
        ...

    def set_grid_visible(self, grid_spec):
        ...

    def get_grid_style(self):
        ...

    def set_grid_style(self, grid_spec):
        ...

    @abc.abstractmethod
    def get_xlabel(self):
        """
        **LLM Docstring**

        Return the x-axis label.

        :return: the result
        """
        ...

    @abc.abstractmethod
    def set_xlabel(self, val, **style):
        """
        **LLM Docstring**

        Set the x-axis label.

        :param val: the label text
        :param style: label styling options
        """
        ...

    @abc.abstractmethod
    def get_ylabel(self):
        """
        **LLM Docstring**

        Return the y-axis label.

        :return: the result
        """
        ...

    @abc.abstractmethod
    def set_ylabel(self, val, **style):
        """
        **LLM Docstring**

        Set the y-axis label.

        :param val: the label text
        :param style: label styling options
        """
        ...

    @abc.abstractmethod
    def get_xlim(self):
        """
        **LLM Docstring**

        Return the x-axis limits.

        :return: the result
        """
        ...

    @abc.abstractmethod
    def set_xlim(self, val, **opts):
        """
        **LLM Docstring**

        Set the x-axis limits.

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        ...

    @abc.abstractmethod
    def get_ylim(self):
        """
        **LLM Docstring**

        Return the y-axis limits.

        :return: the result
        """
        ...

    @abc.abstractmethod
    def set_ylim(self, val, **opts):
        """
        **LLM Docstring**

        Set the y-axis limits.

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        ...

    @abc.abstractmethod
    def get_xticks(self):
        """
        **LLM Docstring**

        Return the x-axis tick locations.

        :return: the result
        """
        ...

    @abc.abstractmethod
    def set_xticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the x-axis tick locations.

        :param val: the tick locations
        :param opts: extra options
        """
        ...

    @abc.abstractmethod
    def get_yticks(self):
        """
        **LLM Docstring**

        Return the y-axis tick locations.

        :return: the result
        """
        ...

    @abc.abstractmethod
    def set_yticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the y-axis tick locations.

        :param val: the tick locations
        :param opts: extra options
        """
        ...

    @abc.abstractmethod
    def get_xtick_style(self):
        """
        **LLM Docstring**

        Return the x-axis tick styling.

        :return: the result
        """
        ...

    @abc.abstractmethod
    def set_xtick_style(self, **opts):
        """
        **LLM Docstring**

        Set the x-axis tick styling.

        :param opts: extra options
        """
        ...

    @abc.abstractmethod
    def get_ytick_style(self):
        """
        **LLM Docstring**

        Return the y-axis tick styling.

        :return: the result
        """
        ...

    @abc.abstractmethod
    def set_ytick_style(self, **opts):
        """
        **LLM Docstring**

        Set the y-axis tick styling.

        :param opts: extra options
        """
        ...

    @abc.abstractmethod
    def set_aspect_ratio(self, ar):
        """
        **LLM Docstring**

        Set the axes aspect ratio.

        :param ar: the aspect ratio
        """
        ...

    @abc.abstractmethod
    def get_bbox(self):
        """
        **LLM Docstring**

        Return the axes bounding box.

        :return: the result
        """
        ...

    @abc.abstractmethod
    def set_bbox(self, bbox):
        """
        **LLM Docstring**

        Set the axes bounding box.

        :param bbox: the bounding box
        """
        ...

    @abc.abstractmethod
    def get_facecolor(self):
        """
        **LLM Docstring**

        Return the background/face color.

        :return: the result
        """
        ...

    @abc.abstractmethod
    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color.

        :param fg: the face color
        """
        ...

    @abc.abstractmethod
    def get_padding(self):
        """
        **LLM Docstring**

        Return the axes padding.

        :return: the result
        """
        ...

    def legend(self, **opts):
        """
        **LLM Docstring**

        Draw the axes legend.

        :param opts: legend options
        :return: the result
        """
        ...

    def get_graphics_properties(self, obj, property=None):
        """
        **LLM Docstring**

        Get backend properties of a drawn graphics object.

        :param obj: the graphics object
        :param property: a specific property to fetch
        :return: the result
        """
        ...

    def set_graphics_properties(self, obj, **props):
        """
        **LLM Docstring**

        Set backend properties on a drawn graphics object.

        :param obj: the graphics object
        :param props: the properties to set
        """
        ...

    @abc.abstractmethod
    def draw_line(self, points, **styles):
        """
        **LLM Docstring**

        Draw a line/polyline through the given points.

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    def draw_point(self, points, **styles):
        """
        **LLM Docstring**

        Draw a point (as a small disk) at the given position(s).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    @abc.abstractmethod
    def draw_disk(self, points, **styles):
        """
        **LLM Docstring**

        Draw a filled disk at the given position(s).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    @abc.abstractmethod
    def draw_rect(self, points, **styles):
        """
        **LLM Docstring**

        Draw a rectangle from the given points.

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    def draw_triangle(self, points, **styles):
        """
        **LLM Docstring**

        Draw a triangle from the given points.

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    @abc.abstractmethod
    def draw_poly(self, points, **styles):
        """
        **LLM Docstring**

        Draw a filled polygon from the given points.

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    @abc.abstractmethod
    def draw_arrow(self, points, **styles):
        """
        **LLM Docstring**

        Draw an arrow from the given points.

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    @abc.abstractmethod
    def draw_text(self, points, vals, **styles):
        """
        **LLM Docstring**

        Draw text at the given position(s).

        :param points: the points to draw
        :param vals: the text string(s)
        :param styles: the styling options
        """
        ...

    @abc.abstractmethod
    def draw_path(self, commands, **styles):
        """
        **LLM Docstring**

        Draw a path from a sequence of drawing commands.

        :param commands: the path drawing commands
        :param styles: the styling options
        """
        ...

class GraphicsAxes3D(GraphicsAxes):

    def __init__(self):
        """
        **LLM Docstring**

        Set up the 3D axes wrapper, adding the z-axis tick manager.
        """
        ...

    @abc.abstractmethod
    def get_zlim(self):
        """
        **LLM Docstring**

        Return the z-axis limits.

        :return: the result
        """
        ...

    @abc.abstractmethod
    def set_zlim(self, val, **opts):
        """
        **LLM Docstring**

        Set the z-axis limits.

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        ...

    @abc.abstractmethod
    def get_zticks(self):
        """
        **LLM Docstring**

        Return the z-axis tick locations.

        :return: the result
        """
        ...

    @abc.abstractmethod
    def set_zticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the z-axis tick locations.

        :param val: the tick locations
        :param opts: extra options
        """
        ...

    @abc.abstractmethod
    def get_ztick_style(self):
        """
        **LLM Docstring**

        Return the z-axis tick styling.

        :return: the result
        """
        ...

    @abc.abstractmethod
    def set_ztick_style(self, **opts):
        """
        **LLM Docstring**

        Set the z-axis tick styling.

        :param opts: extra options
        """
        ...

    def set_projection_type(self, proj_type, **kwargs):
        """
        **LLM Docstring**

        Set the 3D projection type.

        :param proj_type: the projection type
        :param kwargs: extra keyword options
        """
        ...

    def get_projection_type(self):
        """
        **LLM Docstring**

        Return the 3D projection type.

        :return: the result
        """
        ...

    def get_autoscale(self):
        """
        **LLM Docstring**

        Return the autoscale setting.

        :return: the result
        """
        ...

    def set_autoscale(self, autoscale):
        """
        **LLM Docstring**

        Set the autoscale setting.

        :param autoscale: the autoscale setting
        """
        ...

    @abc.abstractmethod
    def get_view_settings(self):
        """
        **LLM Docstring**

        Return the 3D camera/view settings.

        :return: the result
        """
        ...

    @abc.abstractmethod
    def set_view_settings(self, **ops):
        """
        **LLM Docstring**

        Set the 3D camera/view settings.

        :param ops: the view settings
        """
        ...

    @abc.abstractmethod
    def draw_sphere(self, points, rads, **styles):
        """
        **LLM Docstring**

        Draw a sphere (or spheres) at the given center(s) with the given radii.

        :param points: the sphere center(s)
        :param rads: the sphere radii
        :param styles: the styling options
        """
        ...

    @abc.abstractmethod
    def draw_cylinder(self, start, end, rad, circle_points=48, **opts):
        """
        **LLM Docstring**

        Draw a cylinder between two endpoints.

        :param start: the start point
        :param end: the end point
        :param rad: the cylinder radius
        :param circle_points: the number of points around the circular cross-section
        :param opts: extra options
        """
        ...

    @abc.abstractmethod
    def draw_box(self, start, end, **opts):
        """
        **LLM Docstring**

        Draw an axis-aligned box between two corners.

        :param start: the min corner
        :param end: the max corner
        :param opts: extra options
        """
        ...

class GraphicsFigure(metaclass=abc.ABCMeta):
    """
    A wrapper to provide a canonical form for matplotlib.figure.Figure
    so that other backends can plug in cleanly
    """
    Axes = None

    def __init__(self, axes=None):
        """
        **LLM Docstring**

        Set up the figure wrapper.

        :param axes: the initial axes
        """
        ...

    @classmethod
    def construct(self, **kw) -> 'GraphicsFigure':
        """
        **LLM Docstring**

        Construct a figure of this backend type.

        :param kw: construction options
        :return: the result
        """
        ...

    @classmethod
    def canonicalize_opts(cls, opts):
        """
        **LLM Docstring**

        Normalize construction options into the backend's canonical form.

        :param opts: the options to canonicalize
        """
        ...

    @abc.abstractmethod
    def create_axes(self, rows, cols, spans, **kw) -> 'GraphicsAxes':
        """
        **LLM Docstring**

        Create a new axes within the figure at the given grid position.

        :param rows: the number of grid rows
        :param cols: the number of grid columns
        :param spans: the panel span/index
        :param kw: extra keyword options
        :return: the result
        """
        ...

    @abc.abstractmethod
    def create_inset(self, bbox, **kw) -> 'GraphicsAxes':
        """
        **LLM Docstring**

        Create an inset axes at the given bounding box.

        :param bbox: the inset bounding box
        :param kw: extra keyword options
        :return: the result
        """
        ...

    def create_colorbar(self, graphics, axes, norm=None, cmap=None, **kw):
        """
        **LLM Docstring**

        Create a colorbar for a mappable on the given axes.

        :param graphics: the mappable/graphics
        :param axes: the colorbar axes
        :param norm: the color normalization
        :param cmap: the colormap
        :param kw: extra keyword options
        :return: the result
        """
        ...

    def add_axes(self, ax) -> 'GraphicsAxes':
        """
        **LLM Docstring**

        Add an existing axes object to the figure.

        :param ax: the axes to add
        """
        ...

    @abc.abstractmethod
    def clear(self, *, backend):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure.

        """
        ...

    @abc.abstractmethod
    def close(self, *, backend):
        """
        **LLM Docstring**

        Close the figure.

        """
        ...

    def get_bboxes(self):
        """
        **LLM Docstring**

        Return the bounding boxes of the figure's axes.

        :return: the result
        """
        ...

    def prep_show(self):
        """
        **LLM Docstring**

        Prepare the axes/figure for display.

        """
        ...

    @abc.abstractmethod
    def get_size_inches(self):
        """
        **LLM Docstring**

        Return the figure size in inches.

        :return: the result
        """
        ...

    @abc.abstractmethod
    def set_size_inches(self, w, h):
        """
        **LLM Docstring**

        Set the figure size in inches.

        :param w: the width in inches
        :param h: the height in inches
        """
        ...

    @abc.abstractmethod
    def set_extents(self, extents):
        """
        **LLM Docstring**

        Set the figure's coordinate extents.

        :param extents: the extents
        """
        ...

    @abc.abstractmethod
    def get_facecolor(self):
        """
        **LLM Docstring**

        Return the background/face color.

        :return: the result
        """
        ...

    @abc.abstractmethod
    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color.

        :param fg: the face color
        """
        ...

    @abc.abstractmethod
    def savefig(self, file, **opts):
        """
        **LLM Docstring**

        Save the figure to a file.

        :param file: the destination file/path
        :param opts: extra options
        """
        ...

    @abc.abstractmethod
    def animate_frames(self, frames, **animation_opts):
        """
        **LLM Docstring**

        Animate a sequence of frames.

        :param frames: the animation frames
        :param animation_opts: animation options
        """
        ...

    def to_html(self):
        """
        **LLM Docstring**

        Render the figure to HTML.

        :return: the result
        """
        ...

    def to_widget(self, **opts):
        """
        **LLM Docstring**

        Render the figure as an interactive widget.

        :param opts: extra options
        :return: the result
        """
        ...

    def _repr_html_(self):
        """
        **LLM Docstring**

        Return the figure's HTML representation for IPython (delegates to `to_html`).

        :return: the HTML
        :rtype: str
        """
        ...

    def get_mime_bundle(self):
        """
        **LLM Docstring**

        Return the figure's MIME bundle for rich display.

        :return: the result
        """
        ...

    def tight_layout(self):
        """
        **LLM Docstring**

        Tighten the figure layout to remove excess whitespace.

        """
        ...

class GraphicsBackend(metaclass=abc.ABCMeta):
    Figure = GraphicsFigure
    figure_defaults = {}

    def create_figure(self, *args, **kwargs):
        ...

    @abc.abstractmethod
    def create_raw_figure(self, *args, **kwargs) -> 'tuple[GraphicsFigure, tuple[GraphicsAxes]]':
        """
        **LLM Docstring**

        Create a new figure (and its initial axes) for this backend.

        :param args: positional arguments
        :param kwargs: extra keyword options
        :return: the result
        """
        ...
    axes_defaults = {}

    def create_axes(self, figure: 'GraphicsFigure', *args, **kwargs):
        """
        **LLM Docstring**

        Create a new axes within the figure at the given grid position.

        :param figure: the `figure`
        :param args: positional arguments
        :param kwargs: extra keyword options
        :return: the result
        """
        ...
    inset_defaults = {}

    def create_inset(self, figure, *args, **kw) -> 'GraphicsAxes':
        """
        **LLM Docstring**

        Create an inset axes at the given bounding box.

        :param figure: the `figure`
        :param args: positional arguments
        :param kw: extra keyword options
        :return: the result
        """
        ...

    def close_figure(self, figure: 'GraphicsFigure'):
        """
        **LLM Docstring**

        Close a figure via the backend.

        :param figure: the figure to close
        """
        ...

    def remove_axes(self, axes: 'GraphicsAxes'):
        """
        **LLM Docstring**

        Remove an axes via the backend.

        :param axes: the axes to remove
        """
        ...

    def clear_figure(self, figure: 'GraphicsFigure'):
        """
        **LLM Docstring**

        Clear a figure via the backend.

        :param figure: the figure to clear
        """
        ...

    def clear_axes(self, axes: 'GraphicsAxes'):
        """
        **LLM Docstring**

        Clear an axes via the backend.

        :param axes: the axes to clear
        """
        ...

    @abc.abstractmethod
    def get_interactive_status(self) -> 'bool':
        """
        **LLM Docstring**

        Return whether interactive mode is on.

        :return: the result
        """
        ...

    @abc.abstractmethod
    def disable_interactivity(self):
        """
        **LLM Docstring**

        Disable interactive mode.

        """
        ...

    @abc.abstractmethod
    def enable_interactivity(self):
        """
        **LLM Docstring**

        Enable interactive mode.

        """
        ...

    @abc.abstractmethod
    def show_figure(self, figure, reshow=None):
        """
        **LLM Docstring**

        Display a figure via the backend.

        :param figure: the figure to show
        :param reshow: force a reshow of an already-shown figure
        """
        ...

    def to_widget(self, figure: GraphicsFigure):
        """
        **LLM Docstring**

        Render the figure as an interactive widget.

        :param figure: the `figure`
        :return: the result
        """
        ...

    @abc.abstractmethod
    def get_available_themes(self):
        """
        **LLM Docstring**

        Return the themes available for this backend.

        :return: the result
        """
        ...

    class ThemeContextManager(metaclass=abc.ABCMeta):

        def __init__(self, theme_parents, theme_spec, backend):
            """
            **LLM Docstring**

            Canonicalize and store the theme specification for the context.

            :param theme_parents: the parent themes
            :param theme_spec: the theme specification
            """
            ...

        @classmethod
        @abc.abstractmethod
        def canonicalize_theme_opts(self, theme_parents, theme_spec):
            """
            **LLM Docstring**

            Normalize theme options into the backend's canonical form.

            :param theme_parents: the parent themes
            :param theme_spec: the theme specification
            """
            ...

        def __enter__(self):
            ...

        @abc.abstractmethod
        def begin_context(self):
            """
            **LLM Docstring**

            Enter the context, applying the theme.

            """
            ...

        @abc.abstractmethod
        def end_context(self, exc_type, exc_val, exc_tb):
            """
            **LLM Docstring**

            Exit the context, restoring the previous theme.

            :param exc_type: the exception type, if any
            :param exc_val: the exception value, if any
            :param exc_tb: the traceback, if any
            """
            ...

        def __exit__(self, exc_type, exc_val, exc_tb):
            ...

    def theme_context(self, theme_parents, spec):
        """
        **LLM Docstring**

        Return a context manager that applies a theme for this backend.

        :param theme_parents: the parent themes
        :param spec: the theme specification
        """
        ...

    class DefaultBackends(enum.Enum):
        """Real access pattern: DefaultBackends.<MemberName> (this is an enum with 11 members, e.g. DefaultBackends.MPL == 'matplotlib'). Collapsed into a dict below purely for compactness -- do not index it as a dict in real code:"""
        _MEMBERS = {'MPL': 'matplotlib', 'MPL3D': 'matplotlib3D', 'VTK': 'vtk', 'VPython': 'vpython', 'VPython2D': 'vpython2D', 'X3D': 'x3d', 'SVG': 'svg', 'SVG3D': 'svg3D', 'SceneJSON': 'json', 'Plotly': 'plotly', 'Plotly3D': 'plotly3D'}
    registered_backends = {}

    @classmethod
    def get_default_backends(cls):
        """
        **LLM Docstring**

        Return the mapping of default backend names to their backend classes.

        :return: the default-backends mapping
        :rtype: dict
        """
        ...

    @classmethod
    def lookup(cls, backend, opts=None) -> 'GraphicsBackend':
        """
        **LLM Docstring**

        Resolve a backend (name or instance) to an instantiated backend object,
        consulting the registered and default backends.

        :param backend: the backend name or instance
        :param opts: options passed to the backend constructor
        :type opts: dict | None
        :return: the backend instance
        :rtype: GraphicsBackend
        """
        ...

class MPLManager:
    """Real access pattern: MPLManager.<AttrName> (9 class attributes, e.g. MPLManager._plt == None). Collapsed into a dict below purely for compactness -- do not index it as a dict in real code:"""
    _MEMBERS = {'_plt': None, '_patch': None, '_path': None, '_coll': None, '_mpl': None, '_colors': None, '_jlab': None, '_widg': None, '_anim': None}

    @classmethod
    def plt_api(cls):
        """
        **LLM Docstring**

        Lazily import and cache `matplotlib.pyplot`, returning the module.

        :return: the `matplotlib.pyplot` module
        """
        ...

    @classmethod
    def mpl_api(cls):
        """
        **LLM Docstring**

        Lazily import and cache the top-level `matplotlib` module, returning it.

        :return: the `matplotlib` module
        """
        ...

    @classmethod
    def color_api(cls):
        """
        **LLM Docstring**

        Lazily import and cache `matplotlib.colors`, returning the module.

        :return: the `matplotlib.colors` module
        """
        ...

    @classmethod
    def patch_api(cls):
        """
        **LLM Docstring**

        Lazily import and cache `matplotlib.patches`, returning the module.

        :return: the `matplotlib.patches` module
        """
        ...

    @classmethod
    def path_api(cls):
        """
        **LLM Docstring**

        Lazily import and cache `matplotlib.path`, returning the module.

        :return: the `matplotlib.path` module
        """
        ...

    @classmethod
    def collections_api(cls):
        """
        **LLM Docstring**

        Lazily import and cache `matplotlib.collections`, returning the module.

        :return: the `matplotlib.collections` module
        """
        ...

    @classmethod
    def widgets_api(cls):
        """
        **LLM Docstring**

        Lazily import and cache `matplotlib.widgets`, returning the module.

        :return: the `matplotlib.widgets` module
        """
        ...

    @classmethod
    def animations_api(cls):
        """
        **LLM Docstring**

        Lazily import and cache `matplotlib.animation`, returning the module.

        :return: the `matplotlib.animation` module
        """
        ...

    @classmethod
    def draw_if_interactive(self, *args, **kwargs):
        """
        **LLM Docstring**

        No-op override of matplotlib's interactive-draw hook (used to suppress automatic
        drawing).

        :param args: ignored
        :param kwargs: ignored
        """
        ...

    @classmethod
    def magic_backend(self, backend):
        """
        **LLM Docstring**

        Set the matplotlib backend via the IPython `%matplotlib` magic when running in a
        notebook.

        :param backend: the backend name
        :type backend: str
        """
        ...
    _draw_called = False
    _to_draw = []
    settings_stack = []

    @contextlib.contextmanager
    @classmethod
    def figure_settings(cls, figure):
        """
        **LLM Docstring**

        Context helper that captures and adjusts matplotlib's global backend/interactivity
        state for a figure, pushing the previous state onto a stack for later restoration.

        :param figure: the figure being configured
        :return: the settings context
        """
        ...

    @classmethod
    def mpl_disconnect(cls, graphics):
        """
        **LLM Docstring**

        Detach a figure from matplotlib's global figure manager (`Gcf`) when using an
        inline backend, so it isn't auto-displayed.

        :param graphics: the figure's graphics object
        """
        ...

    @classmethod
    def mpl_connect(cls, graphics):
        """
        **LLM Docstring**

        Register a figure with matplotlib's global figure manager (`Gcf`) under an inline
        backend, wiring up its activation handler.

        :param graphics: the figure's graphics object
        """
        ...

    @classmethod
    def jupyter_show(cls, close=None, block=None):
        """Show all figures as SVG/PNG payloads sent to the IPython clients.
        Parameters
        ----------
        close : bool, optional
            If true, a ``plt.close('all')`` call is automatically issued after
            sending all the figures. If this is set, the figures will entirely
            removed from the internal list of figures.
        block : Not used.
            The `block` parameter is a Matplotlib experimental parameter.
            We accept it in the function signature for compatibility with other
            backends.
        """
        ...

class MPLAxes(GraphicsAxes):

    def __init__(self, mpl_axes_object, **opts):
        """
        **LLM Docstring**

        Wrap a matplotlib `Axes` object, exposing it through the canonical `GraphicsAxes`
        interface.

        :param mpl_axes_object: the backing matplotlib axes
        :param opts: canonicalized axes options
        """
        ...

    class TicksManager:

        def __init__(self):
            """
            **LLM Docstring**

            Import and cache matplotlib's tick locator/formatter classes for building tick
            specifications.
            """
            ...

        @property
        def Locator(self):
            """
            **LLM Docstring**

            Return matplotlib's `Locator` locator base class.

            :return: the `Locator` class
            """
            ...

        @property
        def FixedLocator(self):
            """
            **LLM Docstring**

            Return matplotlib's `FixedLocator` locator class.

            :return: the `FixedLocator` class
            """
            ...

        @property
        def AutoLocator(self):
            """
            **LLM Docstring**

            Return matplotlib's `AutoLocator` locator class.

            :return: the `AutoLocator` class
            """
            ...

        @property
        def AutoMinorLocator(self):
            """
            **LLM Docstring**

            Return matplotlib's `AutoMinorLocator` locator class.

            :return: the `AutoMinorLocator` class
            """
            ...

        @property
        def MultipleLocator(self):
            """
            **LLM Docstring**

            Return matplotlib's `MultipleLocator` locator class.

            :return: the `MultipleLocator` class
            """
            ...

        @property
        def StrMethodFormatter(self):
            """
            **LLM Docstring**

            Return matplotlib's `StrMethodFormatter` formatter class.

            :return: the `StrMethodFormatter` class
            """
            ...

        @property
        def NullFormatter(self):
            """
            **LLM Docstring**

            Return matplotlib's `NullFormatter` formatter class.

            :return: the `NullFormatter` class
            """
            ...

        @property
        def FixedFormatter(self):
            """
            **LLM Docstring**

            Return matplotlib's `FixedFormatter` formatter class.

            :return: the `FixedFormatter` class
            """
            ...

        @property
        def ScalarFormatter(self):
            """
            **LLM Docstring**

            Return matplotlib's `ScalarFormatter` formatter class.

            :return: the `ScalarFormatter` class
            """
            ...

    def clear(self, *, backend=None):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (matplotlib backend).

        """
        ...

    def remove(self, *, backend):
        """
        **LLM Docstring**

        Tear down (remove) this axes from its figure (matplotlib backend).

        """
        ...

    def get_plotter(self, method):
        """
        **LLM Docstring**

        Resolve a plotting-method name to the backend callable that draws it (matplotlib backend).

        :param method: the plot-method name
        :return: the result
        """
        ...

    def get_plot_label(self):
        """
        **LLM Docstring**

        Return the plot title/label (matplotlib backend).

        :return: the result
        """
        ...

    def set_plot_label(self, val, **style):
        """
        **LLM Docstring**

        Set the plot title/label (matplotlib backend).

        :param val: the label text
        :param style: label styling options
        """
        ...

    def get_style_list(self):
        """
        **LLM Docstring**

        Return the per-series style cycle (matplotlib backend).

        :return: the result
        """
        ...

    def set_style_list(self, props):
        """
        **LLM Docstring**

        Set the per-series style cycle (matplotlib backend).

        :param props: the style cycle
        """
        ...

    def get_frame_visible(self):
        """
        **LLM Docstring**

        Return which frame (spine) edges are drawn (matplotlib backend).

        :return: the result
        """
        ...

    def set_frame_visible(self, frame_spec):
        """
        **LLM Docstring**

        Set which frame (spine) edges are drawn (matplotlib backend).

        :param frame_spec: the per-edge visibility spec
        """
        ...

    def get_frame_style(self):
        """
        **LLM Docstring**

        Return the frame (spine) styling (matplotlib backend).

        :return: the result
        """
        ...

    def set_frame_style(self, frame_spec):
        """
        **LLM Docstring**

        Set the frame (spine) styling (matplotlib backend).

        :param frame_spec: the frame styling
        """
        ...

    def get_grid_visible(self):
        ...

    def set_grid_visible(self, grid_spec):
        ...

    def get_grid_style(self):
        ...

    def set_grid_style(self, grid_spec):
        ...

    def get_xlabel(self):
        """
        **LLM Docstring**

        Return the x-axis label (matplotlib backend).

        :return: the result
        """
        ...

    def set_xlabel(self, val, **style):
        """
        **LLM Docstring**

        Set the x-axis label (matplotlib backend).

        :param val: the label text
        :param style: label styling options
        """
        ...

    def get_ylabel(self):
        """
        **LLM Docstring**

        Return the y-axis label (matplotlib backend).

        :return: the result
        """
        ...

    def set_ylabel(self, val, **style):
        """
        **LLM Docstring**

        Set the y-axis label (matplotlib backend).

        :param val: the label text
        :param style: label styling options
        """
        ...

    def get_xlim(self):
        """
        **LLM Docstring**

        Return the x-axis limits (matplotlib backend).

        :return: the result
        """
        ...

    def set_xlim(self, val, **opts):
        """
        **LLM Docstring**

        Set the x-axis limits (matplotlib backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        ...

    def get_ylim(self):
        """
        **LLM Docstring**

        Return the y-axis limits (matplotlib backend).

        :return: the result
        """
        ...

    def set_ylim(self, val, **opts):
        """
        **LLM Docstring**

        Set the y-axis limits (matplotlib backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        ...

    def get_xticks(self):
        """
        **LLM Docstring**

        Return the x-axis tick locations (matplotlib backend).

        :return: the result
        """
        ...

    def set_xticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the x-axis tick locations (matplotlib backend).

        :param val: the tick locations
        :param opts: extra options
        """
        ...

    def get_yticks(self):
        """
        **LLM Docstring**

        Return the y-axis tick locations (matplotlib backend).

        :return: the result
        """
        ...

    def set_yticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the y-axis tick locations (matplotlib backend).

        :param val: the tick locations
        :param opts: extra options
        """
        ...

    def get_xtick_style(self):
        """
        **LLM Docstring**

        Return the x-axis tick styling (matplotlib backend).

        :return: the result
        """
        ...

    def set_xtick_style(self, **opts):
        """
        **LLM Docstring**

        Set the x-axis tick styling (matplotlib backend).

        :param opts: extra options
        """
        ...

    def get_ytick_style(self):
        """
        **LLM Docstring**

        Return the y-axis tick styling (matplotlib backend).

        :return: the result
        """
        ...

    def set_ytick_style(self, **opts):
        """
        **LLM Docstring**

        Set the y-axis tick styling (matplotlib backend).

        :param opts: extra options
        """
        ...

    def set_aspect_ratio(self, ar):
        """
        **LLM Docstring**

        Set the axes aspect ratio (matplotlib backend).

        :param ar: the aspect ratio
        """
        ...

    def get_bbox(self):
        """
        **LLM Docstring**

        Return the axes bounding box (matplotlib backend).

        :return: the result
        """
        ...

    def set_bbox(self, bbox):
        """
        **LLM Docstring**

        Set the axes bounding box (matplotlib backend).

        :param bbox: the bounding box
        """
        ...

    def get_facecolor(self):
        """
        **LLM Docstring**

        Return the background/face color (matplotlib backend).

        :return: the result
        """
        ...

    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color (matplotlib backend).

        :param fg: the face color
        """
        ...

    def get_padding(self):
        """
        **LLM Docstring**

        Return the axes padding (matplotlib backend).

        :return: the result
        """
        ...

    def legend(self, **opts):
        """
        **LLM Docstring**

        Draw the axes legend (matplotlib backend).

        :param opts: legend options
        :return: the result
        """
        ...

    def get_graphics_properties(self, obj, property=None):
        """
        **LLM Docstring**

        Get backend properties of a drawn graphics object (matplotlib backend).

        :param obj: the graphics object
        :param property: a specific property to fetch
        :return: the result
        """
        ...

    def set_graphics_properties(self, obj, **props):
        """
        **LLM Docstring**

        Set backend properties on a drawn graphics object (matplotlib backend).

        :param obj: the graphics object
        :param props: the properties to set
        """
        ...

    def draw_line(self, points, **styles):
        """
        **LLM Docstring**

        Draw a line/polyline through the given points (matplotlib backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    def draw_disk(self, points, radius=None, s=None, **styles):
        """
        **LLM Docstring**

        Draw a filled disk at the given position(s) (matplotlib backend).

        :param points: the points to draw
        :param radius: the `radius`
        :param s: the `s`
        :param styles: the styling options
        """
        ...

    def draw_rect(self, points, **styles):
        """
        **LLM Docstring**

        Draw a rectangle from the given points (matplotlib backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    def draw_poly(self, points, **styles):
        """
        **LLM Docstring**

        Draw a filled polygon from the given points (matplotlib backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    def draw_arrow(self, points, **styles):
        """
        **LLM Docstring**

        Draw an arrow from the given points (matplotlib backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    def draw_text(self, points, vals, **styles):
        """
        **LLM Docstring**

        Draw text at the given position(s) (matplotlib backend).

        :param points: the points to draw
        :param vals: the text string(s)
        :param styles: the styling options
        """
        ...

    @classmethod
    def svg_to_mpl_path(cls, path, target_bbox=None, base_height=None, y_flip: bool=False):
        """
        **LLM Docstring**

        Convert an SVG-style path (a sequence of `(command, args)` drawing operations)
        into a matplotlib `Path`, expanding arc commands into point samples and mapping
        move/line/curve/close verbs to matplotlib path codes.

        :param path: the SVG path commands
        :param target_bbox: a bounding box to fit the path into
        :param base_height: the reference height (for y-flipping)
        :param y_flip: flip the y-axis (SVG's y grows downward)
        :type y_flip: bool
        :return: the matplotlib path
        :rtype: matplotlib.path.Path
        """
        ...

    def _adjust_limits(self, xmin: float, xmax: float, ymin: float, ymax: float, pad: float=0.05) -> None:
        """
        **LLM Docstring**

        Expand the axes limits to include a new `(xmin, xmax, ymin, ymax)` region (with
        fractional padding), freezing autoscale afterward.

        :param xmin: the region's x lower bound
        :param xmax: the region's x upper bound
        :param ymin: the region's y lower bound
        :param ymax: the region's y upper bound
        :param pad: the fractional padding to add
        :type pad: float
        """
        ...

    def draw_path(self, commands, **styles):
        """
        **LLM Docstring**

        Draw a path from a sequence of drawing commands (matplotlib backend).

        :param commands: the path drawing commands
        :param styles: the styling options
        """
        ...

class MPLAxes3D(MPLAxes):

    def __init__(self, mpl_axes_object, **opts):
        """
        **LLM Docstring**

        Wrap a matplotlib 3D `Axes`, exposing the z-axis and installing the custom draw
        monkeypatch used to control 3D z-ordering.

        :param mpl_axes_object: the backing matplotlib 3D axes
        :param opts: canonicalized axes options
        """
        ...

    def set_projection_type(self, proj_type, **kwargs):
        """
        **LLM Docstring**

        Set the 3D projection type (matplotlib backend).

        :param proj_type: the projection type
        :param kwargs: extra keyword options
        """
        ...

    def get_projection_type(self):
        """
        **LLM Docstring**

        Return the 3D projection type (matplotlib backend).

        :return: the result
        """
        ...

    def get_autoscale(self):
        """
        **LLM Docstring**

        Return the autoscale setting (matplotlib backend).

        :return: the result
        """
        ...

    def set_autoscale(self, autoscale):
        """
        **LLM Docstring**

        Set the autoscale setting (matplotlib backend).

        :param autoscale: the autoscale setting
        """
        ...

    @classmethod
    def _get_dist(cls, artist):
        """
        **LLM Docstring**

        Compute an artist's camera-space depth (for manual z-ordering), using its
        `do_3d_projection` or projecting its 3D vertices, plus any per-artist depth
        offset.

        :param artist: the matplotlib artist
        :return: the depth value
        :rtype: float
        """
        ...

    @classmethod
    def _artist_predraw(cls, obj, dist):
        """
        **LLM Docstring**

        Call an artist's `predraw` hook (if any) with its computed depth, before drawing.

        :param obj: the artist
        :param dist: the artist's depth
        """
        ...
    zdir_map = {'x': [1, 0, 0], 'y': [0, 1, 0], 'z': [0, 0, 1]}

    @classmethod
    def _transform_zdir(cls, zdir):
        """
        **LLM Docstring**

        Build the rotation matrix that maps the z-axis onto a given direction vector
        (used to orient 2D patches in 3D).

        :param zdir: the target direction (name or vector)
        :return: the `3x3` rotation matrix
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def _set_patch_3d_properties(cls, self, verts, zs, zdir='z', axlim_clip=None):
        """
        **LLM Docstring**

        Give a 2D patch 3D vertex data by lifting its vertices into a plane oriented along
        `zdir` at height `zs` (a reimplementation of matplotlib's internal helper).

        :param self: the patch being modified
        :param verts: the patch's 2D vertices
        :param zs: the per-vertex z heights
        :param zdir: the plane normal direction
        :param axlim_clip: whether to clip to the axis limits
        """
        ...

    @classmethod
    def _set_pathpatch_3d_properties(cls, self, path, zs, zdir='z', axlim_clip=None):
        """
        **LLM Docstring**

        Give a 2D path-patch 3D vertex data (as `_set_patch_3d_properties`), also carrying
        over the path codes.

        :param self: the path-patch being modified
        :param path: the patch's 2D path
        :param zs: the per-vertex z heights
        :param zdir: the plane normal direction
        :param axlim_clip: whether to clip to the axis limits
        """
        ...

    @classmethod
    def _pathpatch_translate(cls, pathpatch, delta):
        """
        **LLM Docstring**

        Translate a 3D-lifted patch by a delta in its 3D segment coordinates.

        :param pathpatch: the patch
        :param delta: the translation
        """
        ...

    @classmethod
    def _patch_do_3d_projection(cls, self, mode=None):
        """
        **LLM Docstring**

        Project a 3D-lifted patch into 2D for drawing and return its depth key for
        z-ordering (a reimplementation of matplotlib's internal projection).

        :param self: the patch
        :param mode: the depth-reduction mode (defaults to the patch's `distance_mode`)
        :return: the depth key
        :rtype: float
        """
        ...

    @classmethod
    def _pathpatch_do_3d_projection(cls, self, mode=None):
        """
        **LLM Docstring**

        Project a 3D-lifted path-patch into 2D for drawing (carrying the path codes) and
        return its depth key.

        :param self: the path-patch
        :param mode: the depth-reduction mode
        :return: the depth key
        :rtype: float
        """
        ...

    @classmethod
    def _line_do_3d_projection(cls, self, mode=None):
        """
        **LLM Docstring**

        Project a 3D line into 2D and return its depth key for z-ordering.

        :param self: the line artist
        :param mode: the depth-reduction mode
        :return: the depth key
        :rtype: float
        """
        ...

    def _monkeypatch_patch(self, patch, pos, zdir='z', zorder_mode=None):
        """
        **LLM Docstring**

        Attach the custom 3D-projection machinery to a 2D patch, lifting it into 3D at a
        position and assigning its z-order distance mode.

        :param patch: the matplotlib patch
        :param pos: the 3D position to place it at
        :param zdir: the plane normal direction
        :param zorder_mode: the depth-reduction mode for z-ordering
        """
        ...

    def _monkeypatch_draw(self, obj):
        """
        **LLM Docstring**

        Replace a 3D axes' `draw` method with one that manually depth-sorts the child
        artists (and rescales the box aspect by camera distance) before drawing, giving
        correct z-ordering.

        :param obj: the matplotlib 3D axes
        """
        ...

    def set_frame_visible(self, frame_spec):
        """
        **LLM Docstring**

        Set which frame (spine) edges are drawn (matplotlib backend).

        :param frame_spec: the per-edge visibility spec
        """
        ...

    def get_zlabel(self):
        """
        **LLM Docstring**

        Return the z-axis label (matplotlib backend).

        :return: the result
        """
        ...

    def set_zlabel(self, val, **style):
        """
        **LLM Docstring**

        Set the z-axis label (matplotlib backend).

        :param val: the label text
        :param style: label styling options
        """
        ...

    def get_zlim(self):
        """
        **LLM Docstring**

        Return the z-axis limits (matplotlib backend).

        :return: the result
        """
        ...

    def set_zlim(self, val, **opts):
        """
        **LLM Docstring**

        Set the z-axis limits (matplotlib backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        ...

    def get_zticks(self):
        """
        **LLM Docstring**

        Return the z-axis tick locations (matplotlib backend).

        :return: the result
        """
        ...

    def set_zticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the z-axis tick locations (matplotlib backend).

        :param val: the tick locations
        :param opts: extra options
        """
        ...

    def get_ztick_style(self):
        """
        **LLM Docstring**

        Return the z-axis tick styling (matplotlib backend).

        :return: the result
        """
        ...

    def set_ztick_style(self, **opts):
        """
        **LLM Docstring**

        Set the z-axis tick styling (matplotlib backend).

        :param opts: extra options
        """
        ...

    def get_box_aspect(self):
        """
        **LLM Docstring**

        Return the 3D box aspect ratios (matplotlib backend).

        :return: the result
        """
        ...

    def set_box_aspect(self, br, **kwargs):
        """
        **LLM Docstring**

        Set the 3D box aspect ratios (matplotlib backend).

        :param br: the box aspect ratios
        :param kwargs: extra keyword options
        """
        ...

    def get_view_settings(self):
        """
        **LLM Docstring**

        Return the 3D camera/view settings (matplotlib backend).

        :return: the result
        """
        ...

    def set_view_settings(self, elev=None, azim=None, roll=None, vertical_axis=None, dist=None, up_vector=None, right_vector=None, view_vector=None, view_distance=None, view_matrix=None, **values):
        """
        **LLM Docstring**

        Set the 3D camera/view settings (matplotlib backend).

        :param elev: the `elev`
        :param azim: the `azim`
        :param roll: the `roll`
        :param vertical_axis: the `vertical_axis`
        :param dist: the `dist`
        :param up_vector: the `up_vector`
        :param right_vector: the `right_vector`
        :param view_vector: the `view_vector`
        :param view_distance: the `view_distance`
        :param view_matrix: the `view_matrix`
        :param values: keyword options
        """
        ...

    def prep_show(self):
        """
        **LLM Docstring**

        Prepare the axes/figure for display (matplotlib backend).

        """
        ...

    @classmethod
    def _get_axis_scaling(cls, sphere_path):
        """
        **LLM Docstring**

        Compute the size-rescaling factor for a 3D artist from how much the axis limits
        have changed since it was first drawn (so on-screen sizes stay consistent).

        :param sphere_path: the artist (carrying the reference limits)
        :return: the size-rescaling factor
        :rtype: float
        """
        ...

    @classmethod
    def _flat_sphere_predraw(cls, sphere_path, dist, *, depth_shading_range, depth_shading_targets, depth_shrink_range, depth_shrink_targets, radius=None):
        """
        **LLM Docstring**

        Predraw hook for a flat (scatter-drawn) sphere: apply depth-based shading and/or
        shrinking and rescale its marker size for the current view.

        :param sphere_path: the sphere artist
        :param dist: the sphere's depth
        :param depth_shading_range: the depth range mapped to shading
        :param depth_shading_targets: the shading amounts at the range ends
        :param depth_shrink_range: the depth range mapped to shrinking
        :param depth_shrink_targets: the shrink amounts at the range ends
        :param radius: the sphere radius
        """
        ...

    @classmethod
    def _get_sphere_proj(cls, artist, *, radius):
        """
        **LLM Docstring**

        Return the depth offset used to bias a sphere's z-order (a heuristic accounting
        for projection distortion).

        :param artist: the sphere artist
        :param radius: the sphere radius
        :return: the depth offset
        :rtype: float
        """
        ...

    def draw_sphere(self, center, radius, sphere_points=48, rendering='standard', s=None, box_scalings=None, edgecolors=None, edge_color=None, lw=None, edge_width=0.01, glow=None, color='white', plotter='scatter', depth_shading_range=(-1, 1), depth_shading_targets=(-0.5, 0.5), depth_shrink_range=None, depth_shrink_targets=None, **opts):
        """
        **LLM Docstring**

        Draw a sphere (or spheres) at the given center(s) with the given radii (matplotlib backend).

        :param center: the `center`
        :param radius: the `radius`
        :param sphere_points: the `sphere_points`
        :param rendering: the `rendering`
        :param s: the `s`
        :param box_scalings: the `box_scalings`
        :param edgecolors: the `edgecolors`
        :param edge_color: the `edge_color`
        :param lw: the `lw`
        :param edge_width: the `edge_width`
        :param glow: the `glow`
        :param color: the `color`
        :param plotter: the `plotter`
        :param depth_shading_range: the `depth_shading_range`
        :param depth_shading_targets: the `depth_shading_targets`
        :param depth_shrink_range: the `depth_shrink_range`
        :param depth_shrink_targets: the `depth_shrink_targets`
        :param opts: extra options
        """
        ...

    @classmethod
    def _get_line_outline_proj(cls, artist, radius=None):
        """
        **LLM Docstring**

        Return the depth offset for a line's outline, accounting for the line's screen
        extent and (optionally) its radius.

        :param artist: the line artist
        :param radius: the line radius
        :return: the depth offset
        :rtype: float
        """
        ...

    @classmethod
    def _get_line_proj(cls, artist, radius=None):
        """
        **LLM Docstring**

        Return the depth offset for a line (biasing its z-order by radius when it faces
        the camera).

        :param artist: the line artist
        :param radius: the line radius
        :return: the depth offset
        :rtype: float
        """
        ...
    _off_stroke = None

    @classmethod
    def _load_stroke(cls):
        """
        **LLM Docstring**

        Lazily build and cache an `OffsetStroke` path-effect class (a `Stroke` that
        offsets the outline), returning it.

        :return: the `OffsetStroke` class
        :rtype: type
        """
        ...

    @classmethod
    def _flat_cylinder_predraw(cls, line3d, dist, *, depth_shading_range, depth_shading_targets, edge_color=None, edge_width=None, pixel_scaling=1):
        """
        **LLM Docstring**

        Predraw hook for a flat (line-drawn) cylinder: apply depth-based shading, rescale
        its linewidth for the current view, and optionally add an outline stroke.

        :param line3d: the cylinder line artist
        :param dist: the cylinder's depth
        :param depth_shading_range: the depth range mapped to shading
        :param depth_shading_targets: the shading amounts at the range ends
        :param edge_color: the outline color
        :param edge_width: the outline width
        :param pixel_scaling: the pixel-to-data scaling
        """
        ...

    def draw_cylinder(self, start, end, rad, circle_points=48, rendering=None, box_scalings=None, edge_color=None, color='black', glow=None, segments=1, segment_overdraw=0.05, edge_width=0.01, lw=None, depth_shading_range=(-1, 1), depth_shading_targets=(-0.5, 0.5), color_cycle=False, capstyle='butt', plotter='plot', **opts):
        """
        **LLM Docstring**

        Draw a cylinder between two endpoints (matplotlib backend).

        :param start: the start point
        :param end: the end point
        :param rad: the cylinder radius
        :param circle_points: the number of points around the circular cross-section
        :param rendering: the `rendering`
        :param box_scalings: the `box_scalings`
        :param edge_color: the `edge_color`
        :param color: the `color`
        :param glow: the `glow`
        :param segments: the `segments`
        :param segment_overdraw: the `segment_overdraw`
        :param edge_width: the `edge_width`
        :param lw: the `lw`
        :param depth_shading_range: the `depth_shading_range`
        :param depth_shading_targets: the `depth_shading_targets`
        :param color_cycle: the `color_cycle`
        :param capstyle: the `capstyle`
        :param plotter: the `plotter`
        :param opts: extra options
        """
        ...
    default_up_vector = (0, 0, 1)
    default_right_vector = (0, 1, 0)
    default_view_vector = (1, 0, 0)

    @classmethod
    def _arc_proj_max(cls, zs):
        """
        **LLM Docstring**

        Depth-reduction mode that biases an arc's z-order toward its far edge
        (`2*min - max`).

        :param zs: the arc's projected depths
        :return: the depth key
        :rtype: float
        """
        ...

    def draw_disk(self, centers, radius=None, angle=None, normal=None, uv_axes=None, zdir=None, theta1=None, theta2=None, rendering='flat', box_scalings=None, line_color=None, line_thickness=None, color=None, glow=None, lw=None, **styles):
        """
        **LLM Docstring**

        Draw a filled disk at the given position(s) (matplotlib backend).

        :param centers: the `centers`
        :param radius: the `radius`
        :param angle: the `angle`
        :param normal: the `normal`
        :param uv_axes: the `uv_axes`
        :param zdir: the `zdir`
        :param theta1: the `theta1`
        :param theta2: the `theta2`
        :param rendering: the `rendering`
        :param box_scalings: the `box_scalings`
        :param line_color: the `line_color`
        :param line_thickness: the `line_thickness`
        :param color: the `color`
        :param glow: the `glow`
        :param lw: the `lw`
        :param styles: the styling options
        """
        ...

    def draw_line(self, points, rendering='flat', box_scalings=None, line_thickness=None, lw=None, s=None, edgecolors=None, **styles):
        """
        **LLM Docstring**

        Draw a line/polyline through the given points (matplotlib backend).

        :param points: the points to draw
        :param rendering: the `rendering`
        :param box_scalings: the `box_scalings`
        :param line_thickness: the `line_thickness`
        :param lw: the `lw`
        :param s: the `s`
        :param edgecolors: the `edgecolors`
        :param styles: the styling options
        """
        ...
    _Arrow3D = None

    @classmethod
    def _load_arrow_drawer(cls):
        """
        **LLM Docstring**

        Lazily build and cache an `Arrow3D` class (a `FancyArrowPatch` that projects a 3D
        vector into 2D each draw), returning it.

        :return: the `Arrow3D` class
        :rtype: type
        """
        ...

    def draw_arrow(self, points, radius=None, rendering=None, segments=8, box_scalings=None, lw=None, **styles):
        """
        **LLM Docstring**

        Draw an arrow from the given points (matplotlib backend).

        :param points: the points to draw
        :param radius: the `radius`
        :param rendering: the `rendering`
        :param segments: the `segments`
        :param box_scalings: the `box_scalings`
        :param lw: the `lw`
        :param styles: the styling options
        """
        ...

    def draw_text(self, points, vals, billboard=True, normal=None, rendering='flat', box_scalings=None, zdir=None, **styles):
        """
        **LLM Docstring**

        Draw text at the given position(s) (matplotlib backend).

        :param points: the points to draw
        :param vals: the text string(s)
        :param billboard: the `billboard`
        :param normal: the `normal`
        :param rendering: the `rendering`
        :param box_scalings: the `box_scalings`
        :param zdir: the `zdir`
        :param styles: the styling options
        """
        ...

    def draw_box(self, start, end, **opts):
        """
        **LLM Docstring**

        Draw an axis-aligned box between two corners (matplotlib backend).

        :param start: the min corner
        :param end: the max corner
        :param opts: extra options
        """
        ...

class MPLFigure(GraphicsFigure):
    Axes = MPLAxes
    default_display_format = 'png'
    _refs = set()

    def __init__(self, mpl_figure_object, display_format=None, **opts):
        """
        **LLM Docstring**

        Wrap a matplotlib `Figure`, tracking it to avoid double-wrapping and setting the
        default display format.

        :param mpl_figure_object: the backing matplotlib figure
        :param display_format: the default display format
        :param opts: canonicalized figure options
        :raises ValueError: if the figure is already wrapped
        """
        ...

    def __hash__(self):
        """
        **LLM Docstring**

        Hash by the backing figure (so weak references behave correctly).

        :return: the hash
        :rtype: int
        """
        ...

    def create_axes(self, rows, cols, spans, **kw):
        """
        **LLM Docstring**

        Create a new axes within the figure at the given grid position (matplotlib backend).

        :param rows: the number of grid rows
        :param cols: the number of grid columns
        :param spans: the panel span/index
        :param kw: extra keyword options
        :return: the result
        """
        ...

    def create_inset(self, bbox, **kw) -> 'GraphicsAxes':
        """
        **LLM Docstring**

        Create an inset axes at the given bounding box (matplotlib backend).

        :param bbox: the inset bounding box
        :param kw: extra keyword options
        :return: the result
        """
        ...

    def clear(self, *, backend):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (matplotlib backend).

        """
        ...

    def close(self, *, backend):
        """
        **LLM Docstring**

        Close the figure (matplotlib backend).

        """
        ...
    _cb_opts = ('orientation', 'extendfrac', 'extendrect', 'drawedges', 'boundaries', 'spacing')

    def create_colorbar(self, graphics, axes, norm=None, cmap=None, **kw):
        """
        **LLM Docstring**

        Create a colorbar for a mappable on the given axes (matplotlib backend).

        :param graphics: the mappable/graphics
        :param axes: the colorbar axes
        :param norm: the color normalization
        :param cmap: the colormap
        :param kw: extra keyword options
        :return: the result
        """
        ...

    def get_figure_label(self):
        """
        **LLM Docstring**

        Return the overall figure label (matplotlib backend).

        :return: the result
        """
        ...

    def set_figure_label(self, val, **style):
        """
        **LLM Docstring**

        Set the overall figure label (matplotlib backend).

        :param val: the label text
        :param style: label styling options
        """
        ...

    def get_size_inches(self):
        """
        **LLM Docstring**

        Return the figure size in inches (matplotlib backend).

        :return: the result
        """
        ...

    def set_size_inches(self, w, h):
        """
        **LLM Docstring**

        Set the figure size in inches (matplotlib backend).

        :param w: the width in inches
        :param h: the height in inches
        """
        ...

    def set_extents(self, extents):
        """
        **LLM Docstring**

        Set the figure's coordinate extents (matplotlib backend).

        :param extents: the extents
        """
        ...

    def set_figure_spacings(self, spacing):
        """
        **LLM Docstring**

        Set the inter-panel spacings (matplotlib backend).

        :param spacing: the spacings
        """
        ...

    def get_facecolor(self):
        """
        **LLM Docstring**

        Return the background/face color (matplotlib backend).

        :return: the result
        """
        ...

    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color (matplotlib backend).

        :param fg: the face color
        """
        ...

    def savefig(self, file, facecolor=None, **opts):
        """
        **LLM Docstring**

        Save the figure to a file (matplotlib backend).

        :param file: the destination file/path
        :param facecolor: the `facecolor`
        :param opts: extra options
        """
        ...

    def animate_frames(self, frames, export_html=True, **animation_opts):
        """
        **LLM Docstring**

        Animate a sequence of frames (matplotlib backend).

        :param frames: the animation frames
        :param export_html: the `export_html`
        :param animation_opts: animation options
        """
        ...

    def to_html(self, format=None):
        """
        **LLM Docstring**

        Render the figure to HTML (matplotlib backend).

        :param format: the `format`
        :return: the result
        """
        ...

    def to_data_url(self):
        """
        **LLM Docstring**

        Render the figure to a base64-encoded PNG `data:` URL.

        :return: the data URL
        :rtype: str
        """
        ...

    def to_svg(self):
        """
        **LLM Docstring**

        Render the figure to an SVG string.

        :return: the SVG markup
        :rtype: str
        """
        ...

    def to_widget(self, format=None, autoclose=True):
        """
        **LLM Docstring**

        Render the figure as an interactive widget (matplotlib backend).

        :param format: the `format`
        :param autoclose: the `autoclose`
        :return: the result
        """
        ...

    def get_mime_bundle(self):
        """
        **LLM Docstring**

        Return the figure's MIME bundle for rich display (matplotlib backend).

        :return: the result
        """
        ...

    def tight_layout(self):
        """
        **LLM Docstring**

        Tighten the figure layout to remove excess whitespace (matplotlib backend).

        """
        ...

class MPLBackend(GraphicsBackend):
    Figure = MPLFigure

    @property
    def plt(self):
        """
        **LLM Docstring**

        The matplotlib `pyplot` module.

        :return: the `pyplot` module
        """
        ...

    @property
    def mpl(self):
        """
        **LLM Docstring**

        The top-level `matplotlib` module.

        :return: the `matplotlib` module
        """
        ...

    def create_raw_figure(self, *args, **kwargs):
        """
        **LLM Docstring**

        Create a new figure (and its initial axes) for this backend (matplotlib backend).

        :param args: positional arguments
        :param kwargs: extra keyword options
        :return: the result
        """
        ...

    def show_all(self):
        """
        **LLM Docstring**

        Show all open matplotlib figures.
        """
        ...

    class ThemeContextManager(GraphicsBackend.ThemeContextManager):

        def __init__(self, theme_parents, theme_spec, backend):
            """
            **LLM Docstring**

            Set up the matplotlib theme context (an `rc_context`-style style override).

            :param args: positional theme arguments
            :param kwargs: theme options
            """
            ...

        @classmethod
        def canonicalize_theme_opts(self, theme_parents, theme_opts) -> 'tuple[list[str], dict]':
            """
            **LLM Docstring**

            Normalize theme options into the backend's canonical form (matplotlib backend).

            :param theme_parents: the parent themes
            :param theme_opts: the `theme_opts`
            """
            ...

        def begin_context(self):
            """
            **LLM Docstring**

            Enter the context, applying the theme.

            """
            ...

        def end_context(self, exc_type, exc_val, exc_tb):
            """
            **LLM Docstring**

            Exit the context, restoring the previous theme.

            :param exc_type: the exception type, if any
            :param exc_val: the exception value, if any
            :param exc_tb: the traceback, if any
            """
            ...

    def show_figure(self, graphics: MPLFigure, autoclose=True, reshow=None):
        """
        **LLM Docstring**

        Display a figure via the backend (matplotlib backend).

        :param graphics: the `graphics`
        :param autoclose: the `autoclose`
        :param reshow: force a reshow of an already-shown figure
        """
        ...

    def to_widget(self, figure: GraphicsFigure, autoclose=True):
        """
        **LLM Docstring**

        Render the figure as an interactive widget (matplotlib backend).

        :param figure: the `figure`
        :param autoclose: the `autoclose`
        :return: the result
        """
        ...

    def get_interactive_status(self) -> 'bool':
        """
        **LLM Docstring**

        Return whether interactive mode is on (matplotlib backend).

        :return: the result
        """
        ...

    def disable_interactivity(self):
        """
        **LLM Docstring**

        Disable interactive mode (matplotlib backend).

        """
        ...

    def enable_interactivity(self):
        """
        **LLM Docstring**

        Enable interactive mode (matplotlib backend).

        """
        ...

    def get_available_themes(self):
        """
        **LLM Docstring**

        Return the themes available for this backend (matplotlib backend).

        :return: the result
        """
        ...

class MPLFigure3D(MPLFigure):
    Axes = MPLAxes3D
    default_display_format = 'svg'

    def create_axes(self, rows, cols, spans, projection='3d', **kw):
        """
        **LLM Docstring**

        Create a new axes within the figure at the given grid position (matplotlib backend).

        :param rows: the number of grid rows
        :param cols: the number of grid columns
        :param spans: the panel span/index
        :param projection: the `projection`
        :param kw: extra keyword options
        :return: the result
        """
        ...

class MPLBackend3D(MPLBackend):
    Figure = MPLFigure3D

    def create_raw_figure(self, *args, subplot_kw=None, **kwargs):
        """
        **LLM Docstring**

        Create a new figure (and its initial axes) for this backend (matplotlib backend).

        :param args: positional arguments
        :param kwargs: extra keyword options
        :return: the result
        """
        ...

class PlotlyAxes(GraphicsAxes):
    base_axis_theme = {}
    base_theme = {}

    def __init__(self, elements=None, xaxis=None, yaxis=None, annotations=None, **opts):
        """
        **LLM Docstring**

        Set up a Plotly axes wrapper holding the trace elements, annotations, and
        per-axis theme options.

        :param elements: the initial trace elements
        :type elements: list | None
        :param xaxis: the x-axis theme options
        :param yaxis: the y-axis theme options
        :param annotations: the initial annotations
        :type annotations: list | None
        :param opts: extra (canonicalized) axes options
        """
        ...

    def clear(self, *, backend=None):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (Plotly backend).

        """
        ...

    def remove(self, *, backend):
        """
        **LLM Docstring**

        Tear down (remove) this axes from its figure (Plotly backend).

        """
        ...

    def prep_elems(self):
        """
        **LLM Docstring**

        Return the axes' trace elements for figure assembly.

        :return: the trace elements
        :rtype: list
        """
        ...

    def prep_annotations(self):
        """
        **LLM Docstring**

        Return the axes' annotations for figure assembly.

        :return: the annotations
        :rtype: list
        """
        ...
    axes_props = ['xaxis', 'xaxis2', 'yaxis', 'yaxis2']

    def prep_opts(self):
        """
        **LLM Docstring**

        Return the axes' layout options, dropping `None`-valued per-axis sub-options.

        :return: the layout options
        :rtype: dict
        """
        ...

    def get_plot_label(self):
        """
        **LLM Docstring**

        Return the plot title/label (Plotly backend).

        :return: the result
        """
        ...

    def set_plot_label(self, val, **style):
        """
        **LLM Docstring**

        Set the plot title/label (Plotly backend).

        :param val: the label text
        :param style: label styling options
        """
        ...

    def get_style_list(self):
        """
        **LLM Docstring**

        Return the per-series style cycle (Plotly backend).

        :return: the result
        """
        ...

    def set_style_list(self, props):
        """
        **LLM Docstring**

        Set the per-series style cycle (Plotly backend).

        :param props: the style cycle
        """
        ...

    def get_frame_visible(self):
        """
        **LLM Docstring**

        Return which frame (spine) edges are drawn (Plotly backend).

        :return: the result
        """
        ...

    def set_frame_visible(self, frame_spec):
        """
        **LLM Docstring**

        Set which frame (spine) edges are drawn (Plotly backend).

        :param frame_spec: the per-edge visibility spec
        """
        ...

    def get_frame_style(self):
        """
        **LLM Docstring**

        Return the frame (spine) styling (Plotly backend).

        :return: the result
        """
        ...

    def set_frame_style(self, frame_spec):
        """
        **LLM Docstring**

        Set the frame (spine) styling (Plotly backend).

        :param frame_spec: the frame styling
        """
        ...

    def get_xlabel(self):
        """
        **LLM Docstring**

        Return the x-axis label (Plotly backend).

        :return: the result
        """
        ...

    def set_xlabel(self, val, **style):
        """
        **LLM Docstring**

        Set the x-axis label (Plotly backend).

        :param val: the label text
        :param style: label styling options
        """
        ...

    def get_ylabel(self):
        """
        **LLM Docstring**

        Return the y-axis label (Plotly backend).

        :return: the result
        """
        ...

    def set_ylabel(self, val, **style):
        """
        **LLM Docstring**

        Set the y-axis label (Plotly backend).

        :param val: the label text
        :param style: label styling options
        """
        ...

    def get_plot_range(self):
        """
        **LLM Docstring**

        Return the plotted data range (Plotly backend).

        :return: the result
        """
        ...

    def get_xlim(self):
        """
        **LLM Docstring**

        Return the x-axis limits (Plotly backend).

        :return: the result
        """
        ...

    def set_xlim(self, val, **opts):
        """
        **LLM Docstring**

        Set the x-axis limits (Plotly backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        ...

    def get_ylim(self):
        """
        **LLM Docstring**

        Return the y-axis limits (Plotly backend).

        :return: the result
        """
        ...

    def set_ylim(self, val, **opts):
        """
        **LLM Docstring**

        Set the y-axis limits (Plotly backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        ...

    def get_xticks(self):
        """
        **LLM Docstring**

        Return the x-axis tick locations (Plotly backend).

        :return: the result
        """
        ...

    def set_xticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the x-axis tick locations (Plotly backend).

        :param val: the tick locations
        :param opts: extra options
        """
        ...

    def get_yticks(self):
        """
        **LLM Docstring**

        Return the y-axis tick locations (Plotly backend).

        :return: the result
        """
        ...

    def set_yticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the y-axis tick locations (Plotly backend).

        :param val: the tick locations
        :param opts: extra options
        """
        ...

    def get_xtick_style(self):
        """
        **LLM Docstring**

        Return the x-axis tick styling (Plotly backend).

        :return: the result
        """
        ...

    def set_xtick_style(self, **opts):
        """
        **LLM Docstring**

        Set the x-axis tick styling (Plotly backend).

        :param opts: extra options
        """
        ...

    def get_ytick_style(self):
        """
        **LLM Docstring**

        Return the y-axis tick styling (Plotly backend).

        :return: the result
        """
        ...

    def set_ytick_style(self, **opts):
        """
        **LLM Docstring**

        Set the y-axis tick styling (Plotly backend).

        :param opts: extra options
        """
        ...

    def get_aspect_ratio(self):
        """
        **LLM Docstring**

        Return the axes aspect ratio (Plotly backend).

        :return: the result
        """
        ...

    def set_aspect_ratio(self, ar):
        """
        **LLM Docstring**

        Set the axes aspect ratio (Plotly backend).

        :param ar: the aspect ratio
        """
        ...

    def get_bbox(self):
        """
        **LLM Docstring**

        Return the axes bounding box (Plotly backend).

        :return: the result
        """
        ...

    def set_bbox(self, bbox):
        """
        **LLM Docstring**

        Set the axes bounding box (Plotly backend).

        :param bbox: the bounding box
        """
        ...
    style_mapping = {'c': 'color', 'linewidth': 'width', 'linestyle': 'dash', 'label': 'name'}
    line_options = ['color', 'width', 'dash']

    def _prep_line_opts(self, line, opts):
        """
        **LLM Docstring**

        Split styling options into the Plotly `line` sub-dict and the remaining options,
        applying the style-name remapping.

        :param line: an explicit `line` dict (built from the options if omitted)
        :type line: dict | None
        :param opts: the styling options
        :type opts: dict
        :return: `(line, opts)`
        :rtype: tuple
        """
        ...

    def plot(self, x, y, line=None, type='scatter', mode='lines', **opts):
        """
        **LLM Docstring**

        Add a line trace to the axes (a Plotly `scatter` trace in `lines` mode).

        :param x: the x data
        :param y: the y data
        :param line: the line styling
        :type line: dict | None
        :param type: the Plotly trace type
        :type type: str
        :param mode: the trace mode
        :type mode: str
        :param opts: extra trace options
        :return: the trace dict
        :rtype: dict
        """
        ...

    def scatter(self, x, y, line=None, type='scatter', mode='markers', **opts):
        """
        **LLM Docstring**

        Add a marker (scatter) trace to the axes.

        :param x: the x data
        :param y: the y data
        :param line: the line styling
        :type line: dict | None
        :param type: the Plotly trace type
        :type type: str
        :param mode: the trace mode
        :type mode: str
        :param opts: extra trace options
        :return: the trace dict
        :rtype: dict
        """
        ...

    def text(self, text, x, y, line=None, type='scatter', mode='text', textposition='middle center', color=None, textfont=None, **opts):
        """
        **LLM Docstring**

        Add a text trace to the axes, assembling the text-font options.

        :param text: the text string(s)
        :param x: the x position(s)
        :param y: the y position(s)
        :param line: the line styling
        :type line: dict | None
        :param type: the Plotly trace type
        :type type: str
        :param mode: the trace mode
        :type mode: str
        :param textposition: the text placement
        :type textposition: str
        :param color: the text color
        :param textfont: explicit text-font options
        :type textfont: dict | None
        :param opts: extra trace options
        :return: the trace dict
        :rtype: dict
        """
        ...

    def get_plotter(self, method, **opts):
        """
        **LLM Docstring**

        Resolve a plotting-method name to the backend callable that draws it (Plotly backend).

        :param method: the plot-method name
        :param opts: extra options
        :return: the result
        """
        ...

    def get_facecolor(self):
        """
        **LLM Docstring**

        Return the background/face color (Plotly backend).

        :return: the result
        """
        ...

    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color (Plotly backend).

        :param fg: the face color
        """
        ...

    def get_padding(self):
        """
        **LLM Docstring**

        Return the axes padding (Plotly backend).

        :return: the result
        """
        ...

    def legend(self, show=True, **opts):
        """
        **LLM Docstring**

        Draw the axes legend (Plotly backend).

        :param show: the `show`
        :param opts: legend options
        :return: the result
        """
        ...

    def get_graphics_properties(self, obj, property=None):
        """
        **LLM Docstring**

        Get backend properties of a drawn graphics object (Plotly backend).

        :param obj: the graphics object
        :param property: a specific property to fetch
        :return: the result
        """
        ...

    def set_graphics_properties(self, obj: dict, **props):
        """
        **LLM Docstring**

        Set backend properties on a drawn graphics object (Plotly backend).

        :param obj: the graphics object
        :param props: the properties to set
        """
        ...

    def draw_poly(self, points, **styles):
        """
        **LLM Docstring**

        Draw a filled polygon from the given points (Plotly backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    def draw_line(self, points, **styles):
        """
        **LLM Docstring**

        Draw a line/polyline through the given points (Plotly backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    def draw_path(self, commands, **styles):
        """
        **LLM Docstring**

        Draw a path from a sequence of drawing commands (Plotly backend).

        :param commands: the path drawing commands
        :param styles: the styling options
        """
        ...

    def draw_disk(self, points, radius=None, s=None, **styles):
        """
        **LLM Docstring**

        Draw a filled disk at the given position(s) (Plotly backend).

        :param points: the points to draw
        :param radius: the `radius`
        :param s: the `s`
        :param styles: the styling options
        """
        ...

    def draw_rect(self, points, **styles):
        """
        **LLM Docstring**

        Draw a rectangle from the given points (Plotly backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    def annotation(self, points, **opts):
        """
        **LLM Docstring**

        Add an annotation (optionally an arrow annotation) to the axes.

        :param points: the annotation position (or `((ax, ay), (x, y))` for an arrow)
        :param opts: extra annotation options
        :return: the annotation dict
        :rtype: dict
        """
        ...

    def draw_arrow(self, points, color=None, width=None, size=None, head=None, **styles):
        """
        **LLM Docstring**

        Draw an arrow from the given points (Plotly backend).

        :param points: the points to draw
        :param color: the `color`
        :param width: the `width`
        :param size: the `size`
        :param head: the `head`
        :param styles: the styling options
        """
        ...

    def draw_text(self, points, vals, **styles):
        """
        **LLM Docstring**

        Draw text at the given position(s) (Plotly backend).

        :param points: the points to draw
        :param vals: the text string(s)
        :param styles: the styling options
        """
        ...

class PlotlyFigure(GraphicsFigure):
    Axes = PlotlyAxes
    default_export_format = 'svg'

    def __init__(self, axes=None, layout=None, export_format=None, width=500, height=500, figsize=None, id=None, include_save_buttons=False, **opts):
        """
        **LLM Docstring**

        Set up a Plotly figure wrapper (holding axes, layout, size, and export/save
        settings).

        :param axes: the initial axes
        :type axes: list | None
        :param layout: the base layout options
        :type layout: dict | None
        :param export_format: the default image export format
        :param width: the figure width in pixels
        :type width: int
        :param height: the figure height in pixels
        :type height: int
        :param figsize: the figure size in inches (overrides width/height)
        :param id: the figure's DOM id (auto-generated if omitted)
        :param include_save_buttons: include the save/export buttons in the HTML
        :type include_save_buttons: bool
        :param opts: extra (canonicalized) options
        """
        ...

    def __setitem__(self, key, value):
        """
        **LLM Docstring**

        Set a figure option by key.

        :param key: the option name
        :param value: the option value
        """
        ...

    def __getitem__(self, item):
        """
        **LLM Docstring**

        Get a figure option by key.

        :param item: the option name
        :return: the option value
        """
        ...

    def clear(self, *, backend):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (Plotly backend).

        """
        ...

    def close(self, *, backend):
        """
        **LLM Docstring**

        Close the figure (Plotly backend).

        """
        ...

    def create_inset(self, bbox, **kw) -> 'GraphicsAxes':
        """
        **LLM Docstring**

        Create an inset axes at the given bounding box (Plotly backend).

        :param bbox: the inset bounding box
        :param kw: extra keyword options
        :return: the result
        """
        ...

    def create_axes(self, **kw) -> 'GraphicsAxes':
        """
        **LLM Docstring**

        Create a new axes within the figure at the given grid position (Plotly backend).

        :param kw: extra keyword options
        :return: the result
        """
        ...

    @classmethod
    def construct(cls, **kw) -> 'GraphicsFigure':
        """
        **LLM Docstring**

        Construct a figure of this backend type (Plotly backend).

        :param kw: construction options
        :return: the result
        """
        ...

    def get_size_inches(self):
        """
        **LLM Docstring**

        Return the figure size in inches (Plotly backend).

        :return: the result
        """
        ...

    def set_size_inches(self, w, h):
        """
        **LLM Docstring**

        Set the figure size in inches (Plotly backend).

        :param w: the width in inches
        :param h: the height in inches
        """
        ...

    def set_extents(self, extents):
        """
        **LLM Docstring**

        Set the figure's coordinate extents (Plotly backend).

        :param extents: the extents
        """
        ...

    def get_facecolor(self):
        """
        **LLM Docstring**

        Return the background/face color (Plotly backend).

        :return: the result
        """
        ...

    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color (Plotly backend).

        :param fg: the face color
        """
        ...

    def savefig(self, file, facecolor=None, **opts):
        """
        **LLM Docstring**

        Save the figure to a file (Plotly backend).

        :param file: the destination file/path
        :param facecolor: the `facecolor`
        :param opts: extra options
        """
        ...

    @classmethod
    def _prep_layout_props(cls, layout):
        """
        **LLM Docstring**

        Normalize the layout properties (currently a pass-through).

        :param layout: the layout options
        :type layout: dict
        :return: the layout options
        :rtype: dict
        """
        ...

    def prep_dict(self):
        """
        **LLM Docstring**

        Assemble the full Plotly figure dict from the axes' traces, annotations, and
        layout, applying the size and aspect-ratio margins.

        :return: the `{data, annotations, layout}` figure dict
        :rtype: dict
        """
        ...

    def to_plotly(self):
        """
        **LLM Docstring**

        Build a `plotly.graph_objects.Figure` from the assembled figure dict.

        :return: the Plotly figure
        """
        ...
    split_plot_fragment = True
    embed_mathjax = True
    preload_plotly = True
    mathjax_cdn = 'https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.min.js'
    plotly_cdn = 'https://cdn.plot.ly/plotly-3.4.0.min.js'

    def get_core_body(self, html):
        """
        **LLM Docstring**

        Extract the contents of the `<body>` from a Plotly HTML export.

        :param html: the exported HTML
        :type html: str
        :return: the body contents
        :rtype: str
        """
        ...

    def set_plotly_script_id(self, html, id):
        """
        **LLM Docstring**

        Insert the figure's id into the last `<script>` tag of a Plotly HTML export.

        :param html: the exported HTML
        :type html: str
        :param id: the id to insert
        :type id: str
        :return: the modified HTML
        :rtype: str
        """
        ...

    def configure_mathjax(self, html, id):
        """
        **LLM Docstring**

        Inject a MathJax configuration/loader script into a Plotly HTML export.

        :param html: the exported HTML
        :type html: str
        :param id: the figure's script id
        :type id: str
        :return: the modified HTML
        :rtype: str
        """
        ...

    def postprocess_plotly_html(self, html):
        """
        **LLM Docstring**

        Post-process a Plotly HTML export: tag the script, optionally strip to the core
        body, and preload the Plotly library from a CDN.

        :param html: the exported HTML
        :type html: str
        :return: the post-processed HTML
        :rtype: str
        """
        ...

    def to_html(self):
        """
        **LLM Docstring**

        Render the figure to HTML (Plotly backend).

        :return: the result
        """
        ...

    def to_svg(self):
        """
        **LLM Docstring**

        Render the figure to an SVG string.

        :return: the SVG markup
        :rtype: str
        """
        ...

    @classmethod
    def get_export_script(self, id, format='svg'):
        """
        **LLM Docstring**

        Build the JavaScript that exports the figure canvas to an image and triggers a
        download.

        :param id: the figure's DOM id
        :type id: str
        :param format: the export image format
        :type format: str
        :return: the export script
        :rtype: str
        """
        ...

    @classmethod
    def set_export_format_script(self, id):
        """
        **LLM Docstring**

        Build the JavaScript that reads the export-format selector and stores it on the
        canvas.

        :param id: the figure's DOM id
        :type id: str
        :return: the script
        :rtype: str
        """
        ...

    @classmethod
    def get_record_screen_script(self, id, polling_rate=30, recording_duration=2, video_format='video/webm'):
        """
        **LLM Docstring**

        Build the JavaScript that records the figure canvas to a video and triggers a
        download.

        :param id: the figure's DOM id
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

        :param id: the figure's DOM id
        :type id: str
        :return: the script
        :rtype: str
        """
        ...

    def to_widget(self, format=None, autoclose=True):
        """
        **LLM Docstring**

        Render the figure as an interactive widget (Plotly backend).

        :param format: the `format`
        :param autoclose: the `autoclose`
        :return: the result
        """
        ...

    def animate_frames(self, frames, **animation_opts):
        """
        **LLM Docstring**

        Animate a sequence of frames (Plotly backend).

        :param frames: the animation frames
        :param animation_opts: animation options
        """
        ...

class PlotlyBackend(GraphicsBackend):
    Figure = PlotlyFigure

    def create_raw_figure(self, *args, **kwargs):
        ...

    def create_figure(self, *args, template=None, **kwargs):
        """
        **LLM Docstring**

        Create a new figure (and its initial axes) for this backend (Plotly backend).

        :param args: positional arguments
        :param kwargs: extra keyword options
        :return: the result
        """
        ...

    @classmethod
    def prep_color(cls, v):
        """
        **LLM Docstring**

        Parse a color string and re-encode it as a Plotly-compatible RGB(A) code.

        :param v: the color string
        :return: the encoded color
        :rtype: str
        """
        ...
    property_mapping = {'labelsize': 'fontsize'}
    axes_props = {'xtick': 'xaxis', 'ytick': 'yaxis'}
    unthemed_props = {'aspect_ratio'}

    @classmethod
    def remap_property(cls, name, value, context=None):
        """
        **LLM Docstring**

        Recursively translate a canonical style property (and value) into Plotly
        template/layout properties, splitting out any properties Plotly can't theme.

        :param name: the property name
        :type name: str
        :param value: the property value
        :param context: the enclosing context (e.g. `'axis'`)
        :type context: str | None
        :return: `(template_props, unhandled_props)`
        :rtype: tuple
        """
        ...

    class ThemeContextManager(GraphicsBackend.ThemeContextManager):
        theme_stack = []
        base_theme = dict(plot_bgcolor='white', showlegend=False)

        @classmethod
        def canonicalize_theme_opts(self, theme_parents, theme_opts) -> 'tuple[list[str], dict]':
            """
            **LLM Docstring**

            Normalize theme options into the backend's canonical form (Plotly backend).

            :param theme_parents: the parent themes
            :param theme_opts: the `theme_opts`
            """
            ...

        def get_axes_theme(self):
            """
            **LLM Docstring**

            Return the axes theme (Plotly backend).

            :return: the result
            """
            ...

        def prep_spec(self):
            """
            **LLM Docstring**

            Assemble the Plotly layout template (and leftover properties) from the theme
            spec by remapping each object type's options.

            :return: `(layout, other_props)`
            :rtype: tuple
            """
            ...

        @classmethod
        def current_theme(cls):
            """
            **LLM Docstring**

            Return the current theme (Plotly backend).

            """
            ...

        def begin_context(self):
            """
            **LLM Docstring**

            Enter the context, applying the theme.

            """
            ...

        def end_context(self, exc_type, exc_val, exc_tb):
            """
            **LLM Docstring**

            Exit the context, restoring the previous theme.

            :param exc_type: the exception type, if any
            :param exc_val: the exception value, if any
            :param exc_tb: the traceback, if any
            """
            ...

    def show_figure(self, graphics: PlotlyFigure, reshow=None):
        """
        **LLM Docstring**

        Display a figure via the backend (Plotly backend).

        :param graphics: the `graphics`
        :param reshow: force a reshow of an already-shown figure
        """
        ...

    def get_interactive_status(self) -> 'bool':
        """
        **LLM Docstring**

        Return whether interactive mode is on (Plotly backend).

        :return: the result
        """
        ...

    def disable_interactivity(self):
        """
        **LLM Docstring**

        Disable interactive mode (Plotly backend).

        """
        ...

    def enable_interactivity(self):
        """
        **LLM Docstring**

        Enable interactive mode (Plotly backend).

        """
        ...

    def get_available_themes(self):
        """
        **LLM Docstring**

        Return the themes available for this backend (Plotly backend).

        :return: the result
        """
        ...

class PlotlyAxes3D(PlotlyAxes):
    axes_props = ['xaxis', 'yaxis', 'zaxis', 'xaxis2', 'yaxis2', 'zaxis2']

    def __init__(self, elements=None, *, zaxis=None, **opts):
        """
        **LLM Docstring**

        Set up a Plotly 3D axes wrapper holding trace elements and per-axis (x/y/z) theme
        options.

        :param elements: the initial trace elements
        :type elements: list | None
        :param zaxis: the z-axis theme options
        :param opts: extra (canonicalized) axes options
        """
        ...

    def get_zaxis_manager(self):
        """
        **LLM Docstring**

        Build the z-axis tick manager for this axes (Plotly backend).

        :return: the result
        """
        ...

    def set_projection_type(self, proj_type, **kwargs):
        """
        **LLM Docstring**

        Set the 3D projection type (Plotly backend).

        :param proj_type: the projection type
        :param kwargs: extra keyword options
        """
        ...

    def get_projection_type(self):
        """
        **LLM Docstring**

        Return the 3D projection type (Plotly backend).

        :return: the result
        """
        ...

    def get_autoscale(self):
        """
        **LLM Docstring**

        Return the autoscale setting (Plotly backend).

        :return: the result
        """
        ...

    def set_autoscale(self, autoscale):
        """
        **LLM Docstring**

        Set the autoscale setting (Plotly backend).

        :param autoscale: the autoscale setting
        """
        ...

    def get_box_aspect(self):
        """
        **LLM Docstring**

        Return the 3D box aspect ratios (Plotly backend).

        :return: the result
        """
        ...

    def set_box_aspect(self, br, **kwargs):
        """
        **LLM Docstring**

        Set the 3D box aspect ratios (Plotly backend).

        :param br: the box aspect ratios
        :param kwargs: extra keyword options
        """
        ...

    def get_frame_visible(self):
        """
        **LLM Docstring**

        Return which frame (spine) edges are drawn (Plotly backend).

        :return: the result
        """
        ...

    def set_frame_visible(self, frame_spec):
        """
        **LLM Docstring**

        Set which frame (spine) edges are drawn (Plotly backend).

        :param frame_spec: the per-edge visibility spec
        """
        ...

    def get_frame_style(self):
        """
        **LLM Docstring**

        Return the frame (spine) styling (Plotly backend).

        :return: the result
        """
        ...

    def set_frame_style(self, frame_spec):
        """
        **LLM Docstring**

        Set the frame (spine) styling (Plotly backend).

        :param frame_spec: the frame styling
        """
        ...

    def get_plot_range(self):
        """
        **LLM Docstring**

        Return the plotted data range (Plotly backend).

        :return: the result
        """
        ...

    def get_zlabel(self):
        """
        **LLM Docstring**

        Return the z-axis label (Plotly backend).

        :return: the result
        """
        ...

    def set_zlabel(self, val, **style):
        """
        **LLM Docstring**

        Set the z-axis label (Plotly backend).

        :param val: the label text
        :param style: label styling options
        """
        ...

    def get_zlim(self):
        """
        **LLM Docstring**

        Return the z-axis limits (Plotly backend).

        :return: the result
        """
        ...

    def set_zlim(self, val, **opts):
        """
        **LLM Docstring**

        Set the z-axis limits (Plotly backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        ...

    def get_zticks(self):
        """
        **LLM Docstring**

        Return the z-axis tick locations (Plotly backend).

        :return: the result
        """
        ...

    def set_zticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the z-axis tick locations (Plotly backend).

        :param val: the tick locations
        :param opts: extra options
        """
        ...

    def get_ztick_style(self):
        """
        **LLM Docstring**

        Return the z-axis tick styling (Plotly backend).

        :return: the result
        """
        ...

    def set_ztick_style(self, **opts):
        """
        **LLM Docstring**

        Set the z-axis tick styling (Plotly backend).

        :param opts: extra options
        """
        ...

    def get_view_settings(self):
        """
        **LLM Docstring**

        Return the 3D camera/view settings (Plotly backend).

        :return: the result
        """
        ...
    default_up_vector = (0, 0, 1)
    default_right_vector = (0, 1, 0)
    default_view_vector = (1, 0, 0)

    def set_view_settings(self, up=None, eye=None, center=None, vertical_axis=None, up_vector=None, right_vector=None, view_vector=None, view_distance=None, view_matrix=None, view_center=None):
        """
        **LLM Docstring**

        Set the 3D camera/view settings (Plotly backend).

        :param up: the `up`
        :param eye: the `eye`
        :param center: the `center`
        :param vertical_axis: the `vertical_axis`
        :param up_vector: the `up_vector`
        :param right_vector: the `right_vector`
        :param view_vector: the `view_vector`
        :param view_distance: the `view_distance`
        :param view_matrix: the `view_matrix`
        :param view_center: the `view_center`
        """
        ...

    def plot(self, x, y, z, line=None, type='scatter3d', **opts):
        """
        **LLM Docstring**

        Add a 3D line trace to the axes (a Plotly `scatter3d` trace).

        :param args: the trace data
        :param opts: trace options
        :return: the trace dict
        :rtype: dict
        """
        ...

    def scatter(self, x, y, z, line=None, type='scatter3d', marker=None, edge_color=None, size=None, line_width=None, **opts):
        """
        **LLM Docstring**

        Add a 3D marker (scatter) trace to the axes.

        :param args: the trace data
        :param opts: trace options
        :return: the trace dict
        :rtype: dict
        """
        ...

    def text(self, text, x, y, z, line=None, type='scatter3d', **opts):
        """
        **LLM Docstring**

        Add a 3D text trace to the axes.

        :param args: the trace data
        :param opts: trace options
        :return: the trace dict
        :rtype: dict
        """
        ...

    def mesh(self, verts, indices=None, type='mesh3d', **opts):
        """
        **LLM Docstring**

        Add a 3D mesh (`mesh3d`) trace to the axes from vertices and triangle indices.

        :param verts: the mesh vertices
        :param indices: the triangle vertex indices
        :param type: the trace type
        :param opts: trace options
        :return: the trace dict
        :rtype: dict
        """
        ...

    def draw_poly(self, points, flatshading=True, **styles):
        """
        **LLM Docstring**

        Draw a filled polygon from the given points (Plotly backend).

        :param points: the points to draw
        :param flatshading: the `flatshading`
        :param styles: the styling options
        """
        ...

    def draw_sphere(self, center, radius, sphere_points=48, rendering='flat', s=None, box_scalings=None, edgecolors=None, edge_color=None, lw=None, edge_width=0.01, glow=None, color='white', default_view_distance='auto', **opts):
        """
        **LLM Docstring**

        Draw a sphere (or spheres) at the given center(s) with the given radii (Plotly backend).

        :param center: the `center`
        :param radius: the `radius`
        :param sphere_points: the `sphere_points`
        :param rendering: the `rendering`
        :param s: the `s`
        :param box_scalings: the `box_scalings`
        :param edgecolors: the `edgecolors`
        :param edge_color: the `edge_color`
        :param lw: the `lw`
        :param edge_width: the `edge_width`
        :param glow: the `glow`
        :param color: the `color`
        :param default_view_distance: the `default_view_distance`
        :param opts: extra options
        """
        ...

    def draw_cylinder(self, start, end, rad, circle_points=48, rendering='flat', box_scalings=None, edge_color=None, color='black', glow=None, segments=1, segment_overdraw=0, edge_width=0.01, lw=None, color_cycle=False, layer='above', default_view_distance='auto', **opts):
        """
        **LLM Docstring**

        Draw a cylinder between two endpoints (Plotly backend).

        :param start: the start point
        :param end: the end point
        :param rad: the cylinder radius
        :param circle_points: the number of points around the circular cross-section
        :param rendering: the `rendering`
        :param box_scalings: the `box_scalings`
        :param edge_color: the `edge_color`
        :param color: the `color`
        :param glow: the `glow`
        :param segments: the `segments`
        :param segment_overdraw: the `segment_overdraw`
        :param edge_width: the `edge_width`
        :param lw: the `lw`
        :param color_cycle: the `color_cycle`
        :param layer: the `layer`
        :param default_view_distance: the `default_view_distance`
        :param opts: extra options
        """
        ...

    @classmethod
    def _get_arc_points(self, center, zdir, radius, theta1, theta2, angular_density=None):
        """
        **LLM Docstring**

        Sample points along a circular arc (used to build 3D arc/cylinder geometry).

        :param center: the arc center
        :param zdir: the arc-plane normal
        :param radius: the arc radius
        :param theta1: the start angle
        :param theta2: the end angle
        :param angular_density: the angular sampling density
        :return: the arc points
        :rtype: np.ndarray
        """
        ...

    def draw_disk(self, centers, radius=None, angle=None, normal=None, uv_axes=None, zdir=None, theta1=None, theta2=None, rendering='flat', box_scalings=None, line_color=None, line_thickness=None, color=None, glow=None, lw=None, **styles):
        """
        **LLM Docstring**

        Draw a filled disk at the given position(s) (Plotly backend).

        :param centers: the `centers`
        :param radius: the `radius`
        :param angle: the `angle`
        :param normal: the `normal`
        :param uv_axes: the `uv_axes`
        :param zdir: the `zdir`
        :param theta1: the `theta1`
        :param theta2: the `theta2`
        :param rendering: the `rendering`
        :param box_scalings: the `box_scalings`
        :param line_color: the `line_color`
        :param line_thickness: the `line_thickness`
        :param color: the `color`
        :param glow: the `glow`
        :param lw: the `lw`
        :param styles: the styling options
        """
        ...

    def draw_text(self, points, vals, billboard=True, normal=None, rendering='flat', box_scalings=None, zdir=None, **styles):
        """
        **LLM Docstring**

        Draw text at the given position(s) (Plotly backend).

        :param points: the points to draw
        :param vals: the text string(s)
        :param billboard: the `billboard`
        :param normal: the `normal`
        :param rendering: the `rendering`
        :param box_scalings: the `box_scalings`
        :param zdir: the `zdir`
        :param styles: the styling options
        """
        ...

    def draw_rect(self, points, rotation=None, normal=None, **styles):
        """
        **LLM Docstring**

        Draw a rectangle from the given points (Plotly backend).

        :param points: the points to draw
        :param rotation: the `rotation`
        :param normal: the `normal`
        :param styles: the styling options
        """
        ...

    def draw_line(self, points, line_thickness=None, width=None, s=None, edgecolors=None, box_scalings=None, **styles):
        """
        **LLM Docstring**

        Draw a line/polyline through the given points (Plotly backend).

        :param points: the points to draw
        :param line_thickness: the `line_thickness`
        :param width: the `width`
        :param s: the `s`
        :param edgecolors: the `edgecolors`
        :param box_scalings: the `box_scalings`
        :param styles: the styling options
        """
        ...

    def draw_mesh(self, points, i=None, j=None, k=None, type='mesh3d', **styles):
        """
        **LLM Docstring**

        Draw a 3D mesh from vertices and per-triangle vertex indices.

        :param points: the mesh vertices
        :param i: the first triangle-vertex indices
        :param j: the second triangle-vertex indices
        :param k: the third triangle-vertex indices
        :param type: the trace type
        :param styles: the styling options
        :return: the trace dict
        :rtype: dict
        """
        ...

    def draw_arrow(self, points, radius, width=None, arrowhead=None, arrowhead_scaling=1.2, arrowhead_points=None, normal=None, rendering='flat', box_scalings=None, **styles):
        """
        **LLM Docstring**

        Draw an arrow from the given points (Plotly backend).

        :param points: the points to draw
        :param radius: the `radius`
        :param width: the `width`
        :param arrowhead: the `arrowhead`
        :param arrowhead_scaling: the `arrowhead_scaling`
        :param arrowhead_points: the `arrowhead_points`
        :param normal: the `normal`
        :param rendering: the `rendering`
        :param box_scalings: the `box_scalings`
        :param styles: the styling options
        """
        ...

class PlotlyFigure3D(PlotlyFigure):
    Axes = PlotlyAxes3D
    omitted_tick_properties = {'minor', 'minor_ticks'}
    scene_props = ['xaxis', 'yaxis', 'zaxis', 'xaxis2', 'yaxis2', 'zaxis2', 'aspectmode', 'aspectratio']

    @classmethod
    def _prep_layout_props(cls, layout):
        """
        **LLM Docstring**

        Normalize the 3D layout properties, folding the per-axis options into a Plotly
        `scene`.

        :param layout: the layout options
        :type layout: dict
        :return: the layout options
        :rtype: dict
        """
        ...

class PlotlyBackend3D(PlotlyBackend):
    Figure = PlotlyFigure3D
    axes_props = {'xtick': 'xaxis', 'ytick': 'yaxis', 'ztick': 'zaxis'}

    class ThemeContextManager(PlotlyBackend.ThemeContextManager):

        def get_axes_theme(self):
            """
            **LLM Docstring**

            Return the axes theme (Plotly backend).

            :return: the result
            """
            ...

class GraphicsRegionAxes(GraphicsAxes):

    def __init__(self, figure_region):
        """
        **LLM Docstring**

        Wrap a figure region as an axes, mapping data coordinates into that region.

        :param figure_region: the target region (per-axis `(min, max)` extents)
        """
        ...

    @staticmethod
    def renormalize(pos, og_reg, final_reg=None):
        """
        **LLM Docstring**

        Rescale a position from an original range into `[0, 1]` (and optionally on into a
        final range).

        :param pos: the position(s)
        :param og_reg: the original `(min, max)` range
        :param final_reg: the target `(min, max)` range (unit range if omitted)
        :return: the rescaled position(s)
        :rtype: np.ndarray
        """
        ...

    def normalize_positions(self, pos):
        """
        **LLM Docstring**

        Map data-coordinate positions into the axes' figure region (per axis).

        :param pos: the positions, shape `(..., ndim)`
        :type pos: np.ndarray
        :return: the region-normalized positions
        :rtype: np.ndarray
        """
        ...

class SVGAxes(GraphicsAxes):

    def __init__(self, base_fig=None, label_text=None, frame=None, prop_cycle=None):
        """
        **LLM Docstring**

        Set up an SVG axes wrapping an `SVGFigure`, with a frame, label, and style cycle.

        :param base_fig: the backing SVG figure (created if omitted)
        :param label_text: the axes label
        :param frame: the frame specification
        :param prop_cycle: the per-series style cycle
        """
        ...

    def remove(self, *, backend):
        """
        **LLM Docstring**

        Tear down (remove) this axes from its figure (SVG backend).

        """
        ...

    def clear(self, *, backend):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (SVG backend).

        """
        ...

    def prep_show(self):
        """
        **LLM Docstring**

        Prepare the axes/figure for display (SVG backend).

        """
        ...

    def get_plotter(self, method):
        """
        **LLM Docstring**

        Resolve a plotting-method name to the backend callable that draws it (SVG backend).

        :param method: the plot-method name
        :return: the result
        """
        ...

    def get_plot_label(self):
        """
        **LLM Docstring**

        Return the plot title/label (SVG backend).

        :return: the result
        """
        ...

    def set_plot_label(self, val, **style):
        """
        **LLM Docstring**

        Set the plot title/label (SVG backend).

        :param val: the label text
        :param style: label styling options
        """
        ...

    def get_style_list(self):
        """
        **LLM Docstring**

        Return the per-series style cycle (SVG backend).

        :return: the result
        """
        ...

    def set_style_list(self, props):
        """
        **LLM Docstring**

        Set the per-series style cycle (SVG backend).

        :param props: the style cycle
        """
        ...

    def get_frame_visible(self):
        """
        **LLM Docstring**

        Return which frame (spine) edges are drawn (SVG backend).

        :return: the result
        """
        ...

    def set_frame_visible(self, frame_spec):
        """
        **LLM Docstring**

        Set which frame (spine) edges are drawn (SVG backend).

        :param frame_spec: the per-edge visibility spec
        """
        ...

    def get_frame_style(self):
        """
        **LLM Docstring**

        Return the frame (spine) styling (SVG backend).

        :return: the result
        """
        ...

    def set_frame_style(self, frame_spec):
        """
        **LLM Docstring**

        Set the frame (spine) styling (SVG backend).

        :param frame_spec: the frame styling
        """
        ...

    def get_xlabel(self):
        """
        **LLM Docstring**

        Return the x-axis label (SVG backend).

        :return: the result
        """
        ...

    def set_xlabel(self, val, **style):
        """
        **LLM Docstring**

        Set the x-axis label (SVG backend).

        :param val: the label text
        :param style: label styling options
        """
        ...

    def get_ylabel(self):
        """
        **LLM Docstring**

        Return the y-axis label (SVG backend).

        :return: the result
        """
        ...

    def set_ylabel(self, val, **style):
        """
        **LLM Docstring**

        Set the y-axis label (SVG backend).

        :param val: the label text
        :param style: label styling options
        """
        ...
    num_axes = 2

    def get_limit(self, axis):
        """
        **LLM Docstring**

        Return the axis limits from the SVG figure's view box (computing it if needed).

        :param axis: the axis index
        :type axis: int
        :return: the `(min, max)` limits
        :rtype: tuple
        """
        ...

    def set_limit(self, axis, lims):
        """
        **LLM Docstring**

        Set one axis's limits in the SVG figure's view box.

        :param axis: the axis index
        :type axis: int
        :param lims: the `(min, max)` limits
        """
        ...

    def get_xlim(self):
        """
        **LLM Docstring**

        Return the x-axis limits (SVG backend).

        :return: the result
        """
        ...

    def set_xlim(self, val, **opts):
        """
        **LLM Docstring**

        Set the x-axis limits (SVG backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        ...

    def get_ylim(self):
        """
        **LLM Docstring**

        Return the y-axis limits (SVG backend).

        :return: the result
        """
        ...

    def set_ylim(self, val, **opts):
        """
        **LLM Docstring**

        Set the y-axis limits (SVG backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        ...

    def get_xticks(self):
        """
        **LLM Docstring**

        Return the x-axis tick locations (SVG backend).

        :return: the result
        """
        ...

    def set_xticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the x-axis tick locations (SVG backend).

        :param val: the tick locations
        :param opts: extra options
        """
        ...

    def get_yticks(self):
        """
        **LLM Docstring**

        Return the y-axis tick locations (SVG backend).

        :return: the result
        """
        ...

    def set_yticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the y-axis tick locations (SVG backend).

        :param val: the tick locations
        :param opts: extra options
        """
        ...

    def get_xtick_style(self):
        """
        **LLM Docstring**

        Return the x-axis tick styling (SVG backend).

        :return: the result
        """
        ...

    def set_xtick_style(self, **opts):
        """
        **LLM Docstring**

        Set the x-axis tick styling (SVG backend).

        :param opts: extra options
        """
        ...

    def get_ytick_style(self):
        """
        **LLM Docstring**

        Return the y-axis tick styling (SVG backend).

        :return: the result
        """
        ...

    def set_ytick_style(self, **opts):
        """
        **LLM Docstring**

        Set the y-axis tick styling (SVG backend).

        :param opts: extra options
        """
        ...

    def set_aspect_ratio(self, ar):
        """
        **LLM Docstring**

        Set the axes aspect ratio (SVG backend).

        :param ar: the aspect ratio
        """
        ...

    def get_bbox(self):
        """
        **LLM Docstring**

        Return the axes bounding box (SVG backend).

        :return: the result
        """
        ...

    def set_bbox(self, bbox):
        """
        **LLM Docstring**

        Set the axes bounding box (SVG backend).

        :param bbox: the bounding box
        """
        ...

    def get_facecolor(self):
        """
        **LLM Docstring**

        Return the background/face color (SVG backend).

        :return: the result
        """
        ...

    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color (SVG backend).

        :param fg: the face color
        """
        ...

    def get_padding(self):
        """
        **LLM Docstring**

        Return the axes padding (SVG backend).

        :return: the result
        """
        ...

    def set_padding(self, padding):
        """
        **LLM Docstring**

        Set the axes padding (SVG backend).

        :param padding: the padding
        """
        ...

    def legend(self, **opts):
        """
        **LLM Docstring**

        Draw the axes legend (SVG backend).

        :param opts: legend options
        :return: the result
        """
        ...

    def get_graphics_properties(self, obj, property=None):
        """
        **LLM Docstring**

        Get backend properties of a drawn graphics object (SVG backend).

        :param obj: the graphics object
        :param property: a specific property to fetch
        :return: the result
        """
        ...

    def set_graphics_properties(self, obj, **props):
        """
        **LLM Docstring**

        Set backend properties on a drawn graphics object (SVG backend).

        :param obj: the graphics object
        :param props: the properties to set
        """
        ...
    style_mapping = {'edgecolor': 'stroke', 'lw': 'stroke-width', 'color': 'fill', 'line_color': 'stroke', 'line_width': 'stroke-width'}

    def prep_styles(self, styles):
        """
        **LLM Docstring**

        Normalize SVG styling: resolve a `glow` option into a color and remap style names.

        :param styles: the styling options
        :type styles: dict
        :return: the prepared styles
        :rtype: dict
        """
        ...

    def draw_line(self, points, stroke=None, line_color=None, color=None, **styles):
        """
        **LLM Docstring**

        Draw a line/polyline through the given points (SVG backend).

        :param points: the points to draw
        :param stroke: the `stroke`
        :param line_color: the `line_color`
        :param color: the `color`
        :param styles: the styling options
        """
        ...

    def draw_point(self, points, **styles):
        """
        **LLM Docstring**

        Draw a point (as a small disk) at the given position(s) (SVG backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    def draw_disk(self, points, *, radius, **styles):
        """
        **LLM Docstring**

        Draw a filled disk at the given position(s) (SVG backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    def draw_rect(self, points, **styles):
        """
        **LLM Docstring**

        Draw a rectangle from the given points (SVG backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    def draw_triangle(self, points, **styles):
        """
        **LLM Docstring**

        Draw a triangle from the given points (SVG backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    def draw_poly(self, points, **styles):
        """
        **LLM Docstring**

        Draw a filled polygon from the given points (SVG backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    def draw_arrow(self, points, arrowhead=None, marker=None, **styles):
        """
        **LLM Docstring**

        Draw an arrow from the given points (SVG backend).

        :param points: the points to draw
        :param arrowhead: the `arrowhead`
        :param marker: the `marker`
        :param styles: the styling options
        """
        ...

    @classmethod
    def filter_font_options(cls, styles):
        """
        **LLM Docstring**

        Split styling options into font options (remapped to their SVG names) and the
        remaining options.

        :param styles: the styling options
        :type styles: dict
        :return: `(font_options, remaining_options)`
        :rtype: tuple
        """
        ...

    @classmethod
    def _text_to_path(cls, origin, text, invert=False, size=None, plot_range=None, anchor=None, font_size_scaling=13, **font_opts):
        """
        **LLM Docstring**

        Convert a text string into an SVG path via matplotlib's `TextPath`, applying
        optional y-inversion, size scaling (fitting into a plot range), and anchoring.

        :param origin: the text origin
        :param text: the text string
        :type text: str
        :param invert: flip the path vertically
        :type invert: bool
        :param size: the font size (or a target render size)
        :param plot_range: a range to scale the text into
        :param anchor: the text anchor alignment
        :param font_size_scaling: the reference font size for scaling
        :param font_opts: font properties
        :return: the text path (and its bounds/placement)
        """
        ...

    def draw_text(self, points, vals, use_path=False, invert=False, anchor=None, plot_range=None, font_size_scaling=13, **styles):
        """
        **LLM Docstring**

        Draw text at the given position(s) (SVG backend).

        :param points: the points to draw
        :param vals: the text string(s)
        :param use_path: the `use_path`
        :param invert: the `invert`
        :param anchor: the `anchor`
        :param plot_range: the `plot_range`
        :param font_size_scaling: the `font_size_scaling`
        :param styles: the styling options
        """
        ...

    def draw_path(self, commands, use_polyline=False, **styles):
        """
        **LLM Docstring**

        Draw a path from a sequence of drawing commands (SVG backend).

        :param commands: the path drawing commands
        :param use_polyline: the `use_polyline`
        :param styles: the styling options
        """
        ...

class SVGFigure(GraphicsFigure):
    Axes = SVGAxes
    default_styles = {'vector-effect': 'non-scaling-stroke'}

    def __init__(self, axes=None, layout=None, figsize=None, flip_y=True, **kwargs):
        """
        **LLM Docstring**

        Set up an SVG figure holding its axes, layout, and default styling.

        :param axes: the initial axes
        :type axes: list | None
        :param layout: the layout specification
        :param figsize: the figure size in inches
        :param flip_y: flip the y-axis (SVG's y grows downward)
        :type flip_y: bool
        :param kwargs: extra default styling options
        """
        ...

    def create_axes(self, rows, cols, spans, **kw):
        """
        **LLM Docstring**

        Create a new axes within the figure at the given grid position (SVG backend).

        :param rows: the number of grid rows
        :param cols: the number of grid columns
        :param spans: the panel span/index
        :param kw: extra keyword options
        :return: the result
        """
        ...

    def create_inset(self, bbox, **kw) -> 'GraphicsAxes':
        """
        **LLM Docstring**

        Create an inset axes at the given bounding box (SVG backend).

        :param bbox: the inset bounding box
        :param kw: extra keyword options
        :return: the result
        """
        ...

    def create_colorbar(self, graphics, axes, norm=None, cmap=None, **kw):
        """
        **LLM Docstring**

        Create a colorbar for a mappable on the given axes (SVG backend).

        :param graphics: the mappable/graphics
        :param axes: the colorbar axes
        :param norm: the color normalization
        :param cmap: the colormap
        :param kw: extra keyword options
        :return: the result
        """
        ...

    def add_axes(self, ax) -> 'GraphicsAxes':
        """
        **LLM Docstring**

        Add an existing axes object to the figure (SVG backend).

        :param ax: the axes to add
        """
        ...

    def clear(self, *, backend):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (SVG backend).

        """
        ...

    def close(self, *, backend):
        """
        **LLM Docstring**

        Close the figure (SVG backend).

        """
        ...

    def get_size_inches(self):
        """
        **LLM Docstring**

        Return the figure size in inches (SVG backend).

        :return: the result
        """
        ...

    def set_size_inches(self, w, h):
        """
        **LLM Docstring**

        Set the figure size in inches (SVG backend).

        :param w: the width in inches
        :param h: the height in inches
        """
        ...

    def set_extents(self, extents):
        """
        **LLM Docstring**

        Set the figure's coordinate extents (SVG backend).

        :param extents: the extents
        """
        ...

    def get_facecolor(self):
        """
        **LLM Docstring**

        Return the background/face color (SVG backend).

        :return: the result
        """
        ...

    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color (SVG backend).

        :param fg: the face color
        """
        ...

    def savefig(self, file, **opts):
        """
        **LLM Docstring**

        Save the figure to a file (SVG backend).

        :param file: the destination file/path
        :param opts: extra options
        """
        ...

    def animate_frames(self, frames, **animation_opts):
        """
        **LLM Docstring**

        Animate a sequence of frames (SVG backend).

        :param frames: the animation frames
        :param animation_opts: animation options
        """
        ...

    def to_html(self):
        """
        **LLM Docstring**

        Render the figure to HTML (SVG backend).

        :return: the result
        """
        ...

    def prep_args(self, opts):
        """
        **LLM Docstring**

        Merge the figure's default styling with per-call options.

        :param opts: the per-call options
        :type opts: dict
        :return: the merged options
        :rtype: dict
        """
        ...

    def to_svg_figure(self, **opts):
        """
        **LLM Docstring**

        Assemble the figure's axes into a single HTML `Div` of SVGs (applying the y-flip
        transform).

        :param opts: extra styling options
        :return: the assembled figure element
        """
        ...

    def to_svg(self):
        """
        **LLM Docstring**

        Render the whole figure to a combined SVG string.

        :return: the SVG markup
        :rtype: str
        """
        ...

    def to_widget(self, **opts):
        """
        **LLM Docstring**

        Render the figure as an interactive widget (SVG backend).

        :param opts: extra options
        :return: the result
        """
        ...

    def _repr_html_(self):
        """
        **LLM Docstring**

        Return the figure's SVG as its IPython HTML representation.

        :return: the SVG/HTML
        :rtype: str
        """
        ...

    def get_mime_bundle(self):
        """
        **LLM Docstring**

        Return the figure's MIME bundle for rich display (SVG backend).

        :return: the result
        """
        ...

class SVGBackend(GraphicsBackend):
    Figure = SVGFigure

    def create_raw_figure(self, *args, **kwargs):
        """
        **LLM Docstring**

        Create a new figure (and its initial axes) for this backend (SVG backend).

        :param args: positional arguments
        :param kwargs: extra keyword options
        :return: the result
        """
        ...

    class ThemeContextManager(GraphicsBackend.ThemeContextManager):
        theme_stack = []

        @classmethod
        def canonicalize_theme_opts(self, theme_parents, theme_spec):
            """
            **LLM Docstring**

            Normalize theme options into the backend's canonical form (SVG backend).

            :param theme_parents: the parent themes
            :param theme_spec: the theme specification
            """
            ...

        def begin_context(self):
            """
            **LLM Docstring**

            Enter the context, applying the theme.

            """
            ...

        def end_context(self, exc_type, exc_val, exc_tb):
            """
            **LLM Docstring**

            Exit the context, restoring the previous theme.

            :param exc_type: the exception type, if any
            :param exc_val: the exception value, if any
            :param exc_tb: the traceback, if any
            """
            ...

    def show_figure(self, graphics: SVGFigure, reshow=None):
        """
        **LLM Docstring**

        Display a figure via the backend (SVG backend).

        :param graphics: the `graphics`
        :param reshow: force a reshow of an already-shown figure
        """
        ...

    def get_interactive_status(self) -> 'bool':
        """
        **LLM Docstring**

        Return whether interactive mode is on (SVG backend).

        :return: the result
        """
        ...

    def disable_interactivity(self):
        """
        **LLM Docstring**

        Disable interactive mode (SVG backend).

        """
        ...

    def enable_interactivity(self):
        """
        **LLM Docstring**

        Enable interactive mode (SVG backend).

        """
        ...

    def get_available_themes(self):
        """
        **LLM Docstring**

        Return the themes available for this backend (SVG backend).

        :return: the result
        """
        ...

class SVGAxes3D(SVGAxes):
    figure: svg.SVGFigure3D

    def __init__(self, base_fig=None, **opts):
        """
        **LLM Docstring**

        Set up an SVG 3D axes wrapping an `SVGFigure3D`, adding the z-axis manager.

        :param base_fig: the backing SVG 3D figure (created if omitted)
        :param opts: extra axes options
        """
        ...

    def get_zaxis_manager(self):
        """
        **LLM Docstring**

        Build the z-axis tick manager for this axes (SVG backend).

        :return: the result
        """
        ...
    num_axes = 3

    def get_zlim(self):
        """
        **LLM Docstring**

        Return the z-axis limits (SVG backend).

        :return: the result
        """
        ...

    def set_zlim(self, val, **opts):
        """
        **LLM Docstring**

        Set the z-axis limits (SVG backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        ...

    def get_zticks(self):
        """
        **LLM Docstring**

        Return the z-axis tick locations (SVG backend).

        :return: the result
        """
        ...

    def set_zticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the z-axis tick locations (SVG backend).

        :param val: the tick locations
        :param opts: extra options
        """
        ...

    def get_ztick_style(self):
        """
        **LLM Docstring**

        Return the z-axis tick styling (SVG backend).

        :return: the result
        """
        ...

    def set_ztick_style(self, **opts):
        """
        **LLM Docstring**

        Set the z-axis tick styling (SVG backend).

        :param opts: extra options
        """
        ...

    def set_projection_type(self, proj_type, **kwargs):
        """
        **LLM Docstring**

        Set the 3D projection type (SVG backend).

        :param proj_type: the projection type
        :param kwargs: extra keyword options
        """
        ...

    def get_projection_type(self):
        """
        **LLM Docstring**

        Return the 3D projection type (SVG backend).

        :return: the result
        """
        ...

    def get_autoscale(self):
        """
        **LLM Docstring**

        Return the autoscale setting (SVG backend).

        :return: the result
        """
        ...

    def set_autoscale(self, autoscale):
        """
        **LLM Docstring**

        Set the autoscale setting (SVG backend).

        :param autoscale: the autoscale setting
        """
        ...

    def get_view_settings(self):
        """
        **LLM Docstring**

        Return the 3D camera/view settings (SVG backend).

        :return: the result
        """
        ...

    def set_view_settings(self, **ops):
        """
        **LLM Docstring**

        Set the 3D camera/view settings (SVG backend).

        :param ops: the view settings
        """
        ...

    def embedding_matrix(self, rotation, normal):
        """
        **LLM Docstring**

        Build the view/embedding matrix that projects 3D points onto the SVG plane from a
        rotation and a plane normal.

        :param rotation: the in-plane rotation (or `None`)
        :param normal: the plane normal (defaults to the z-axis)
        :return: the embedding matrix
        :rtype: np.ndarray
        """
        ...

    def draw_line(self, points, **styles):
        """
        **LLM Docstring**

        Draw a line/polyline through the given points (SVG backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    def draw_disk(self, points, *, radius, angle=None, normal=None, uv_axes=None, offset_angle=None, span_angle=None, **styles):
        """
        **LLM Docstring**

        Draw a filled disk at the given position(s) (SVG backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    def draw_rect(self, points, rotation=None, normal=None, **styles):
        """
        **LLM Docstring**

        Draw a rectangle from the given points (SVG backend).

        :param points: the points to draw
        :param rotation: the `rotation`
        :param normal: the `normal`
        :param styles: the styling options
        """
        ...

    def draw_sphere(self, points, rads, **styles):
        """
        **LLM Docstring**

        Draw a sphere (or spheres) at the given center(s) with the given radii (SVG backend).

        :param points: the sphere center(s)
        :param rads: the sphere radii
        :param styles: the styling options
        """
        ...

    def draw_cylinder(self, start, end, rad, **styles):
        """
        **LLM Docstring**

        Draw a cylinder between two endpoints (SVG backend).

        :param start: the start point
        :param end: the end point
        :param rad: the cylinder radius
        :param styles: the styling options
        """
        ...

    def draw_box(self, start, end, **styles):
        """
        **LLM Docstring**

        Draw an axis-aligned box between two corners (SVG backend).

        :param start: the min corner
        :param end: the max corner
        :param styles: the styling options
        """
        ...

    def draw_text(self, points, vals, projected=False, use_path=False, flip_y=True, **styles):
        """
        **LLM Docstring**

        Draw text at the given position(s) (SVG backend).

        :param points: the points to draw
        :param vals: the text string(s)
        :param projected: the `projected`
        :param use_path: the `use_path`
        :param flip_y: the `flip_y`
        :param styles: the styling options
        """
        ...

class SVGFigure3D(SVGFigure):
    Axes = SVGAxes3D

class SVGBackend3D(SVGBackend):
    Figure = SVGFigure3D

class VTKAxes(GraphicsRegionAxes):

    def __init__(self, figure_region, figure: vtk.VTKWindow):
        """
        **LLM Docstring**

        Set up a VTK axes over a figure region.

        :param args: positional arguments forwarded to the base region axes
        :param opts: axes options
        """
        ...

    @classmethod
    def canonicalize_opts(cls, opts):
        """
        **LLM Docstring**

        Normalize construction options into the backend's canonical form (VTK backend).

        :param opts: the options to canonicalize
        """
        ...

    def remove(self, *, backend):
        """
        **LLM Docstring**

        Tear down (remove) this axes from its figure (VTK backend).

        """
        ...

    def clear(self, *, backend):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (VTK backend).

        """
        ...

    def get_plotter(self, method):
        """
        **LLM Docstring**

        Resolve a plotting-method name to the backend callable that draws it (VTK backend).

        :param method: the plot-method name
        :return: the result
        """
        ...

    def get_plot_label(self):
        """
        **LLM Docstring**

        Return the plot title/label (VTK backend).

        :return: the result
        """
        ...

    def set_plot_label(self, val, **style):
        """
        **LLM Docstring**

        Set the plot title/label (VTK backend).

        :param val: the label text
        :param style: label styling options
        """
        ...

    def get_style_list(self):
        """
        **LLM Docstring**

        Return the per-series style cycle (VTK backend).

        :return: the result
        """
        ...

    def set_style_list(self, props):
        """
        **LLM Docstring**

        Set the per-series style cycle (VTK backend).

        :param props: the style cycle
        """
        ...

    def get_frame_visible(self):
        """
        **LLM Docstring**

        Return which frame (spine) edges are drawn (VTK backend).

        :return: the result
        """
        ...

    def set_frame_visible(self, frame_spec):
        """
        **LLM Docstring**

        Set which frame (spine) edges are drawn (VTK backend).

        :param frame_spec: the per-edge visibility spec
        """
        ...

    def get_frame_style(self):
        """
        **LLM Docstring**

        Return the frame (spine) styling (VTK backend).

        :return: the result
        """
        ...

    def set_frame_style(self, frame_spec):
        """
        **LLM Docstring**

        Set the frame (spine) styling (VTK backend).

        :param frame_spec: the frame styling
        """
        ...

    def get_xlabel(self):
        """
        **LLM Docstring**

        Return the x-axis label (VTK backend).

        :return: the result
        """
        ...

    def set_xlabel(self, val, **style):
        """
        **LLM Docstring**

        Set the x-axis label (VTK backend).

        :param val: the label text
        :param style: label styling options
        """
        ...

    def get_ylabel(self):
        """
        **LLM Docstring**

        Return the y-axis label (VTK backend).

        :return: the result
        """
        ...

    def set_ylabel(self, val, **style):
        """
        **LLM Docstring**

        Set the y-axis label (VTK backend).

        :param val: the label text
        :param style: label styling options
        """
        ...

    def get_xlim(self):
        """
        **LLM Docstring**

        Return the x-axis limits (VTK backend).

        :return: the result
        """
        ...

    def set_xlim(self, val, **opts):
        """
        **LLM Docstring**

        Set the x-axis limits (VTK backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        ...

    def get_ylim(self):
        """
        **LLM Docstring**

        Return the y-axis limits (VTK backend).

        :return: the result
        """
        ...

    def set_ylim(self, val, **opts):
        """
        **LLM Docstring**

        Set the y-axis limits (VTK backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        ...

    def get_zlim(self):
        """
        **LLM Docstring**

        Return the z-axis limits (VTK backend).

        :return: the result
        """
        ...

    def set_zlim(self, val, **opts):
        """
        **LLM Docstring**

        Set the z-axis limits (VTK backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        ...

    def get_xticks(self):
        """
        **LLM Docstring**

        Return the x-axis tick locations (VTK backend).

        :return: the result
        """
        ...

    def set_xticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the x-axis tick locations (VTK backend).

        :param val: the tick locations
        :param opts: extra options
        """
        ...

    def get_yticks(self):
        """
        **LLM Docstring**

        Return the y-axis tick locations (VTK backend).

        :return: the result
        """
        ...

    def set_yticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the y-axis tick locations (VTK backend).

        :param val: the tick locations
        :param opts: extra options
        """
        ...

    def get_xtick_style(self):
        """
        **LLM Docstring**

        Return the x-axis tick styling (VTK backend).

        :return: the result
        """
        ...

    def set_xtick_style(self, **opts):
        """
        **LLM Docstring**

        Set the x-axis tick styling (VTK backend).

        :param opts: extra options
        """
        ...

    def get_ytick_style(self):
        """
        **LLM Docstring**

        Return the y-axis tick styling (VTK backend).

        :return: the result
        """
        ...

    def set_ytick_style(self, **opts):
        """
        **LLM Docstring**

        Set the y-axis tick styling (VTK backend).

        :param opts: extra options
        """
        ...

    def set_aspect_ratio(self, ar):
        """
        **LLM Docstring**

        Set the axes aspect ratio (VTK backend).

        :param ar: the aspect ratio
        """
        ...

    def get_bbox(self):
        """
        **LLM Docstring**

        Return the axes bounding box (VTK backend).

        :return: the result
        """
        ...

    def set_bbox(self, bbox):
        """
        **LLM Docstring**

        Set the axes bounding box (VTK backend).

        :param bbox: the bounding box
        """
        ...

    def get_facecolor(self):
        """
        **LLM Docstring**

        Return the background/face color (VTK backend).

        :return: the result
        """
        ...

    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color (VTK backend).

        :param fg: the face color
        """
        ...

    def get_padding(self):
        """
        **LLM Docstring**

        Return the axes padding (VTK backend).

        :return: the result
        """
        ...

    @abc.abstractmethod
    def draw_line(self, points, **styles):
        """
        **LLM Docstring**

        Draw a line/polyline through the given points (VTK backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    @abc.abstractmethod
    def draw_disk(self, points, **styles):
        """
        **LLM Docstring**

        Draw a filled disk at the given position(s) (VTK backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    @abc.abstractmethod
    def draw_rect(self, points, **styles):
        """
        **LLM Docstring**

        Draw a rectangle from the given points (VTK backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    @abc.abstractmethod
    def draw_poly(self, points, **styles):
        """
        **LLM Docstring**

        Draw a filled polygon from the given points (VTK backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    @abc.abstractmethod
    def draw_arrow(self, points, **styles):
        """
        **LLM Docstring**

        Draw an arrow from the given points (VTK backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    @abc.abstractmethod
    def draw_text(self, points, vals, **styles):
        """
        **LLM Docstring**

        Draw text at the given position(s) (VTK backend).

        :param points: the points to draw
        :param vals: the text string(s)
        :param styles: the styling options
        """
        ...

    @abc.abstractmethod
    def draw_sphere(self, points, rads, **styles):
        """
        **LLM Docstring**

        Draw a sphere (or spheres) at the given center(s) with the given radii (VTK backend).

        :param points: the sphere center(s)
        :param rads: the sphere radii
        :param styles: the styling options
        """
        ...

    @abc.abstractmethod
    def animate_frames(self, frames, **animation_opts):
        """
        **LLM Docstring**

        Animate a sequence of frames (VTK backend).

        :param frames: the animation frames
        :param animation_opts: animation options
        """
        ...

class VTKFigure(GraphicsFigure):
    Axes = VTKAxes

    def __init__(self, vtk_window: vtk.VTKWindow, **opts):
        """
        **LLM Docstring**

        Set up a VTK figure.

        :param args: positional figure arguments
        :param opts: figure options
        """
        ...

    def create_axes(self, rows, cols, spans, **kw) -> 'GraphicsAxes':
        """
        **LLM Docstring**

        Create a new axes within the figure at the given grid position (VTK backend).

        :param rows: the number of grid rows
        :param cols: the number of grid columns
        :param spans: the panel span/index
        :param kw: extra keyword options
        :return: the result
        """
        ...

    @abc.abstractmethod
    def create_inset(self, bbox, **kw) -> 'GraphicsAxes':
        """
        **LLM Docstring**

        Create an inset axes at the given bounding box (VTK backend).

        :param bbox: the inset bounding box
        :param kw: extra keyword options
        :return: the result
        """
        ...

    @abc.abstractmethod
    def clear(self, *, backend):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (VTK backend).

        """
        ...

    @abc.abstractmethod
    def close(self, *, backend):
        """
        **LLM Docstring**

        Close the figure (VTK backend).

        """
        ...

    def get_bboxes(self):
        """
        **LLM Docstring**

        Return the bounding boxes of the figure's axes (VTK backend).

        :return: the result
        """
        ...

    @abc.abstractmethod
    def get_size_inches(self):
        """
        **LLM Docstring**

        Return the figure size in inches (VTK backend).

        :return: the result
        """
        ...

    @abc.abstractmethod
    def set_size_inches(self, w, h):
        """
        **LLM Docstring**

        Set the figure size in inches (VTK backend).

        :param w: the width in inches
        :param h: the height in inches
        """
        ...

    @abc.abstractmethod
    def savefig(self, file, **opts):
        """
        **LLM Docstring**

        Save the figure to a file (VTK backend).

        :param file: the destination file/path
        :param opts: extra options
        """
        ...

class VTKBackend(GraphicsBackend):
    ...

class VPythonWrapper:
    _vec = None

    @classmethod
    def vpythonify(cls, arg):
        """
        **LLM Docstring**

        Coerce a value into a VPython object, wrapping list/array vectors as VPython
        `vector`s.

        :param arg: the value to coerce
        :return: the VPython-compatible value
        """
        ...

    @classmethod
    def vpython_color(cls, color):
        """
        **LLM Docstring**

        Coerce a color (name or RGB) into a VPython color vector.

        :param color: the color
        :return: the VPython color vector
        """
        ...

class VPythonCanvasWrapper(VPythonWrapper):

    def __init__(self, canvas):
        """
        **LLM Docstring**

        Wrap a VPython canvas for drawing 3D primitives.

        :param canvas: the VPython canvas
        """
        ...

    def remove(self, *, backend=None):
        """
        **LLM Docstring**

        Tear down (remove) this axes from its figure (VPython backend).

        """
        ...

    def clear(self, *, backend=None):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (VPython backend).

        """
        ...

    @property
    def width(self):
        """
        **LLM Docstring**

        Return the width (VPython backend).

        :param width: the `width`
        """
        ...

    @width.setter
    def width(self, width):
        """
        **LLM Docstring**

        Return the width (VPython backend).

        :param width: the `width`
        """
        ...

    @property
    def height(self):
        """
        **LLM Docstring**

        Return the height (VPython backend).

        :param height: the `height`
        """
        ...

    @height.setter
    def height(self, height):
        """
        **LLM Docstring**

        Return the height (VPython backend).

        :param height: the `height`
        """
        ...

    @property
    def title(self):
        """
        **LLM Docstring**

        Return the title (VPython backend).

        :param title: the `title`
        """
        ...

    @title.setter
    def title(self, title):
        """
        **LLM Docstring**

        Return the title (VPython backend).

        :param title: the `title`
        """
        ...

    @property
    def axis(self):
        """
        **LLM Docstring**

        Return the axis object/handle (VPython backend).

        :param axis: the `axis`
        """
        ...

    @axis.setter
    def axis(self, axis):
        """
        **LLM Docstring**

        Return the axis object/handle (VPython backend).

        :param axis: the `axis`
        """
        ...

    @property
    def up(self):
        """
        **LLM Docstring**

        Return the camera up-vector (VPython backend).

        :param up: the `up`
        """
        ...

    @up.setter
    def up(self, up):
        """
        **LLM Docstring**

        Return the camera up-vector (VPython backend).

        :param up: the `up`
        """
        ...

    @property
    def background(self):
        """
        **LLM Docstring**

        Return the background color (VPython backend).

        :param background: the `background`
        """
        ...

    @background.setter
    def background(self, background):
        """
        **LLM Docstring**

        Return the background color (VPython backend).

        :param background: the `background`
        """
        ...

    def primitive(self, name, *args, color=None, **opts):
        """
        **LLM Docstring**

        Create a VPython primitive on the canvas by name, coercing the arguments and
        color into VPython objects.

        :param name: the VPython primitive name
        :type name: str
        :param args: the positional primitive arguments
        :param color: the primitive color
        :param opts: extra primitive options
        :return: the created VPython object
        """
        ...

    def box(self, left_corner, right_corner, **styles):
        """
        **LLM Docstring**

        Draw a box between two corners.

        :param left_corner: the min corner
        :param right_corner: the max corner
        :param styles: the styling options
        :return: the VPython box
        """
        ...

    def curve(self, points, **styles):
        """
        **LLM Docstring**

        Draw a curve through the given points.

        :param points: the curve points
        :param styles: the styling options
        :return: the VPython curve
        """
        ...

    def cylinder(self, start, end, rad, **styles):
        """
        **LLM Docstring**

        Draw a cylinder between two endpoints (deriving the axis and length from them).

        :param start: the start point
        :param end: the end point
        :param rad: the cylinder radius
        :param styles: the styling options
        :return: the VPython cylinder
        """
        ...

    def arrow(self, points, **styles):
        """
        **LLM Docstring**

        Draw an arrow at/through the given points.

        :param points: the arrow points
        :param styles: the styling options
        :return: the VPython arrow
        """
        ...

    def label(self, pos, text, **styles):
        """
        **LLM Docstring**

        Draw a text label at a position.

        :param pos: the label position
        :param text: the label text
        :param styles: the styling options
        :return: the VPython label
        """
        ...

    def sphere(self, points, rads, **styles):
        """
        **LLM Docstring**

        Draw a sphere at the given center(s) with the given radii.

        :param points: the sphere center(s)
        :param rads: the sphere radii
        :param styles: the styling options
        :return: the VPython sphere
        """
        ...

class VPythonGraphWrapper(VPythonWrapper):

    def __init__(self, graph):
        """
        **LLM Docstring**

        Wrap a VPython graph for 2D plotting, tracking the created plot objects.

        :param graph: the VPython graph
        """
        ...

    @property
    def title(self):
        """
        **LLM Docstring**

        Return the title (VPython backend).

        :param title: the `title`
        """
        ...

    @title.setter
    def title(self, title):
        """
        **LLM Docstring**

        Return the title (VPython backend).

        :param title: the `title`
        """
        ...

    @property
    def xtitle(self):
        """
        **LLM Docstring**

        Return the x-axis title (VPython backend).

        :param xtitle: the `xtitle`
        """
        ...

    @xtitle.setter
    def xtitle(self, xtitle):
        """
        **LLM Docstring**

        Return the x-axis title (VPython backend).

        :param xtitle: the `xtitle`
        """
        ...

    @property
    def ytitle(self):
        """
        **LLM Docstring**

        Return the y-axis title (VPython backend).

        :param ytitle: the `ytitle`
        """
        ...

    @ytitle.setter
    def ytitle(self, ytitle):
        """
        **LLM Docstring**

        Return the y-axis title (VPython backend).

        :param ytitle: the `ytitle`
        """
        ...

    @property
    def background(self):
        """
        **LLM Docstring**

        Return the background color (VPython backend).

        :param background: the `background`
        """
        ...

    @background.setter
    def background(self, background):
        """
        **LLM Docstring**

        Return the background color (VPython backend).

        :param background: the `background`
        """
        ...

    @property
    def foreground(self):
        """
        **LLM Docstring**

        Return the foreground color (VPython backend).

        :param foreground: the `foreground`
        """
        ...

    @foreground.setter
    def foreground(self, foreground):
        """
        **LLM Docstring**

        Return the foreground color (VPython backend).

        :param foreground: the `foreground`
        """
        ...

    @property
    def xmin(self):
        """
        **LLM Docstring**

        Return the x lower bound (VPython backend).

        :param xmin: the `xmin`
        """
        ...

    @xmin.setter
    def xmin(self, xmin):
        """
        **LLM Docstring**

        Return the x lower bound (VPython backend).

        :param xmin: the `xmin`
        """
        ...

    @property
    def xmax(self):
        """
        **LLM Docstring**

        Return the x upper bound (VPython backend).

        :param xmax: the `xmax`
        """
        ...

    @xmax.setter
    def xmax(self, xmax):
        """
        **LLM Docstring**

        Return the x upper bound (VPython backend).

        :param xmax: the `xmax`
        """
        ...

    @property
    def ymin(self):
        """
        **LLM Docstring**

        Return the y lower bound (VPython backend).

        :param ymin: the `ymin`
        """
        ...

    @ymin.setter
    def ymin(self, ymin):
        """
        **LLM Docstring**

        Return the y lower bound (VPython backend).

        :param ymin: the `ymin`
        """
        ...

    @property
    def ymax(self):
        """
        **LLM Docstring**

        Return the y upper bound (VPython backend).

        :param ymax: the `ymax`
        """
        ...

    @ymax.setter
    def ymax(self, ymax):
        """
        **LLM Docstring**

        Return the y upper bound (VPython backend).

        :param ymax: the `ymax`
        """
        ...

    @property
    def width(self):
        """
        **LLM Docstring**

        Return the width (VPython backend).

        :param width: the `width`
        """
        ...

    @width.setter
    def width(self, width):
        """
        **LLM Docstring**

        Return the width (VPython backend).

        :param width: the `width`
        """
        ...

    @property
    def height(self):
        """
        **LLM Docstring**

        Return the height (VPython backend).

        :param height: the `height`
        """
        ...

    @height.setter
    def height(self, height):
        """
        **LLM Docstring**

        Return the height (VPython backend).

        :param height: the `height`
        """
        ...

    def remove(self, *, backend=None):
        """
        **LLM Docstring**

        Tear down (remove) this axes from its figure (VPython backend).

        """
        ...

    def clear(self, *, backend=None):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (VPython backend).

        """
        ...

    def plot(self, x, y, color=None, marker_color=None, dot_color=None, **styles):
        """
        **LLM Docstring**

        Add a line series to the graph (via VPython `gcurve`).

        :param x: the x data
        :param y: the y data
        :param color: the series color
        :param marker_color: the marker color
        :param dot_color: the dot color
        :param styles: extra styling options
        :return: the VPython plot object
        """
        ...

    def scatter(self, x, y, color=None, marker_color=None, dot_color=None, **styles):
        """
        **LLM Docstring**

        Add a scatter series to the graph (via VPython `gdots`).

        :param x: the x data
        :param y: the y data
        :param color: the series color
        :param marker_color: the marker color
        :param dot_color: the dot color
        :param styles: extra styling options
        :return: the VPython plot object
        """
        ...

    def vbars(self, x, y, color=None, marker_color=None, dot_color=None, **styles):
        """
        **LLM Docstring**

        Add a vertical-bar series to the graph (via VPython `gvbars`).

        :param x: the x data
        :param y: the y data
        :param color: the series color
        :param marker_color: the marker color
        :param dot_color: the dot color
        :param styles: extra styling options
        :return: the VPython plot object
        """
        ...

    def hbars(self, x, y, color=None, marker_color=None, dot_color=None, **styles):
        """
        **LLM Docstring**

        Add a horizontal-bar series to the graph (via VPython `ghbars`).

        :param x: the x data
        :param y: the y data
        :param color: the series color
        :param marker_color: the marker color
        :param dot_color: the dot color
        :param styles: extra styling options
        :return: the VPython plot object
        """
        ...

class VPythonAxes(GraphicsAxes):

    def __init__(self, graph: VPythonGraphWrapper):
        """
        **LLM Docstring**

        Set up a VPython 2D axes over a graph wrapper.

        :param graph: the VPython graph wrapper
        :type graph: VPythonGraphWrapper
        """
        ...

    def remove(self, *, backend):
        """
        **LLM Docstring**

        Tear down (remove) this axes from its figure (VPython backend).

        """
        ...

    def clear(self, *, backend):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (VPython backend).

        """
        ...

    def get_plotter(self, method):
        """
        **LLM Docstring**

        Resolve a plotting-method name to the backend callable that draws it (VPython backend).

        :param method: the plot-method name
        :return: the result
        """
        ...

    def get_plot_label(self):
        """
        **LLM Docstring**

        Return the plot title/label (VPython backend).

        :return: the result
        """
        ...

    def set_plot_label(self, val, **style):
        """
        **LLM Docstring**

        Set the plot title/label (VPython backend).

        :param val: the label text
        :param style: label styling options
        """
        ...

    def get_style_list(self):
        """
        **LLM Docstring**

        Return the per-series style cycle (VPython backend).

        :return: the result
        """
        ...

    def set_style_list(self, props):
        """
        **LLM Docstring**

        Set the per-series style cycle (VPython backend).

        :param props: the style cycle
        """
        ...

    def get_frame_visible(self):
        """
        **LLM Docstring**

        Return which frame (spine) edges are drawn (VPython backend).

        :return: the result
        """
        ...

    def set_frame_visible(self, frame_spec):
        """
        **LLM Docstring**

        Set which frame (spine) edges are drawn (VPython backend).

        :param frame_spec: the per-edge visibility spec
        """
        ...

    def get_frame_style(self):
        """
        **LLM Docstring**

        Return the frame (spine) styling (VPython backend).

        :return: the result
        """
        ...

    def set_frame_style(self, frame_spec):
        """
        **LLM Docstring**

        Set the frame (spine) styling (VPython backend).

        :param frame_spec: the frame styling
        """
        ...

    def get_xlabel(self):
        """
        **LLM Docstring**

        Return the x-axis label (VPython backend).

        :return: the result
        """
        ...

    def set_xlabel(self, val, **style):
        """
        **LLM Docstring**

        Set the x-axis label (VPython backend).

        :param val: the label text
        :param style: label styling options
        """
        ...

    def get_ylabel(self):
        """
        **LLM Docstring**

        Return the y-axis label (VPython backend).

        :return: the result
        """
        ...

    def set_ylabel(self, val, **style):
        """
        **LLM Docstring**

        Set the y-axis label (VPython backend).

        :param val: the label text
        :param style: label styling options
        """
        ...

    def get_xlim(self):
        """
        **LLM Docstring**

        Return the x-axis limits (VPython backend).

        :return: the result
        """
        ...

    def set_xlim(self, val, **opts):
        """
        **LLM Docstring**

        Set the x-axis limits (VPython backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        ...

    def get_ylim(self):
        """
        **LLM Docstring**

        Return the y-axis limits (VPython backend).

        :return: the result
        """
        ...

    def set_ylim(self, val, **opts):
        """
        **LLM Docstring**

        Set the y-axis limits (VPython backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        ...

    def get_xticks(self):
        """
        **LLM Docstring**

        Return the x-axis tick locations (VPython backend).

        :return: the result
        """
        ...

    def set_xticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the x-axis tick locations (VPython backend).

        :param val: the tick locations
        :param opts: extra options
        """
        ...

    def get_yticks(self):
        """
        **LLM Docstring**

        Return the y-axis tick locations (VPython backend).

        :return: the result
        """
        ...

    def set_yticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the y-axis tick locations (VPython backend).

        :param val: the tick locations
        :param opts: extra options
        """
        ...

    def get_xtick_style(self):
        """
        **LLM Docstring**

        Return the x-axis tick styling (VPython backend).

        :return: the result
        """
        ...

    def set_xtick_style(self, **opts):
        """
        **LLM Docstring**

        Set the x-axis tick styling (VPython backend).

        :param opts: extra options
        """
        ...

    def get_ytick_style(self):
        """
        **LLM Docstring**

        Return the y-axis tick styling (VPython backend).

        :return: the result
        """
        ...

    def set_ytick_style(self, **opts):
        """
        **LLM Docstring**

        Set the y-axis tick styling (VPython backend).

        :param opts: extra options
        """
        ...

    def set_aspect_ratio(self, ar):
        """
        **LLM Docstring**

        Set the axes aspect ratio (VPython backend).

        :param ar: the aspect ratio
        """
        ...

    def get_bbox(self):
        """
        **LLM Docstring**

        Return the axes bounding box (VPython backend).

        :return: the result
        """
        ...

    def set_bbox(self, bbox):
        """
        **LLM Docstring**

        Set the axes bounding box (VPython backend).

        :param bbox: the bounding box
        """
        ...

    def get_facecolor(self):
        """
        **LLM Docstring**

        Return the background/face color (VPython backend).

        :return: the result
        """
        ...

    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color (VPython backend).

        :param fg: the face color
        """
        ...

    def get_padding(self):
        """
        **LLM Docstring**

        Return the axes padding (VPython backend).

        :return: the result
        """
        ...

    def draw_line(self, points, **styles):
        """
        **LLM Docstring**

        Draw a line/polyline through the given points (VPython backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    def draw_disk(self, points, color=None, edge_color=None, radius=1, edgecolors=None, s=None, **styles):
        """
        **LLM Docstring**

        Draw a filled disk at the given position(s) (VPython backend).

        :param points: the points to draw
        :param color: the `color`
        :param edge_color: the `edge_color`
        :param radius: the `radius`
        :param edgecolors: the `edgecolors`
        :param s: the `s`
        :param styles: the styling options
        """
        ...

    def draw_rect(self, points, **styles):
        """
        **LLM Docstring**

        Draw a rectangle from the given points (VPython backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    def draw_poly(self, points, **styles):
        """
        **LLM Docstring**

        Draw a filled polygon from the given points (VPython backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    def draw_arrow(self, points, color=None, **styles):
        """
        **LLM Docstring**

        Draw an arrow from the given points (VPython backend).

        :param points: the points to draw
        :param color: the `color`
        :param styles: the styling options
        """
        ...

    def draw_text(self, points, vals, color=None, **styles):
        """
        **LLM Docstring**

        Draw text at the given position(s) (VPython backend).

        :param points: the points to draw
        :param vals: the text string(s)
        :param color: the `color`
        :param styles: the styling options
        """
        ...

    def draw_sphere(self, points, rads, color=None, **styles):
        """
        **LLM Docstring**

        Draw a sphere (or spheres) at the given center(s) with the given radii (VPython backend).

        :param points: the sphere center(s)
        :param rads: the sphere radii
        :param color: the `color`
        :param styles: the styling options
        """
        ...

    def animate_frames(self, frames, **animation_opts):
        """
        **LLM Docstring**

        Animate a sequence of frames (VPython backend).

        :param frames: the animation frames
        :param animation_opts: animation options
        """
        ...

class VPythonFigure(GraphicsFigure):
    Axes = VPythonAxes
    _refs = set()

    def __init__(self, vpython_graph: VPythonGraphWrapper, **opts):
        """
        **LLM Docstring**

        Wrap a VPython graph as a figure (tracked to avoid double-wrapping).

        :param vpython_graph: the VPython graph wrapper
        :type vpython_graph: VPythonGraphWrapper
        :param opts: canonicalized figure options
        :raises ValueError: if the graph is already wrapped
        """
        ...

    @classmethod
    def construct(cls, **kw) -> 'VPythonFigure':
        """
        **LLM Docstring**

        Construct a figure of this backend type (VPython backend).

        :param kw: construction options
        :return: the result
        """
        ...

    def create_axes(self, rows=1, cols=1, spans=1, **kw) -> 'GraphicsAxes':
        """
        **LLM Docstring**

        Create a new axes within the figure at the given grid position (VPython backend).

        :param rows: the number of grid rows
        :param cols: the number of grid columns
        :param spans: the panel span/index
        :param kw: extra keyword options
        :return: the result
        """
        ...

    def create_inset(self, bbox, **kw) -> 'GraphicsAxes':
        """
        **LLM Docstring**

        Create an inset axes at the given bounding box (VPython backend).

        :param bbox: the inset bounding box
        :param kw: extra keyword options
        :return: the result
        """
        ...

    def clear(self, *, backend):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (VPython backend).

        """
        ...

    def close(self, *, backend):
        """
        **LLM Docstring**

        Close the figure (VPython backend).

        """
        ...

    def get_size_inches(self):
        """
        **LLM Docstring**

        Return the figure size in inches (VPython backend).

        :return: the result
        """
        ...

    def set_size_inches(self, w, h):
        """
        **LLM Docstring**

        Set the figure size in inches (VPython backend).

        :param w: the width in inches
        :param h: the height in inches
        """
        ...

    def get_facecolor(self):
        """
        **LLM Docstring**

        Return the background/face color (VPython backend).

        :return: the result
        """
        ...

    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color (VPython backend).

        :param fg: the face color
        """
        ...

    def savefig(self, file, **opts):
        """
        **LLM Docstring**

        Save the figure to a file (VPython backend).

        :param file: the destination file/path
        :param opts: extra options
        """
        ...

class VPythonBackend(GraphicsBackend):
    Figure = VPythonFigure

    def create_raw_figure(self, *args, **kwargs):
        """
        **LLM Docstring**

        Create a new figure (and its initial axes) for this backend (VPython backend).

        :param args: positional arguments
        :param kwargs: extra keyword options
        :return: the result
        """
        ...

    class ThemeContextManager(GraphicsBackend.ThemeContextManager):
        theme_stack = []

        @classmethod
        def canonicalize_theme_opts(self, theme_parents, theme_spec):
            """
            **LLM Docstring**

            Normalize theme options into the backend's canonical form (VPython backend).

            :param theme_parents: the parent themes
            :param theme_spec: the theme specification
            """
            ...

        def begin_context(self):
            """
            **LLM Docstring**

            Enter the context, applying the theme.

            """
            ...

        def end_context(self, exc_type, exc_val, exc_tb):
            """
            **LLM Docstring**

            Exit the context, restoring the previous theme.

            :param exc_type: the exception type, if any
            :param exc_val: the exception value, if any
            :param exc_tb: the traceback, if any
            """
            ...

    def show_figure(self, graphics, reshow=None):
        """
        **LLM Docstring**

        Display a figure via the backend (VPython backend).

        :param graphics: the `graphics`
        :param reshow: force a reshow of an already-shown figure
        """
        ...

    def get_interactive_status(self) -> 'bool':
        """
        **LLM Docstring**

        Return whether interactive mode is on (VPython backend).

        :return: the result
        """
        ...

    def disable_interactivity(self):
        """
        **LLM Docstring**

        Disable interactive mode (VPython backend).

        """
        ...

    def enable_interactivity(self):
        """
        **LLM Docstring**

        Enable interactive mode (VPython backend).

        """
        ...

    def get_available_themes(self):
        """
        **LLM Docstring**

        Return the themes available for this backend (VPython backend).

        :return: the result
        """
        ...

class VPythonAxes3D(GraphicsAxes3D):

    def __init__(self, canvas: VPythonCanvasWrapper):
        """
        **LLM Docstring**

        Set up a VPython 3D axes over a canvas wrapper.

        :param canvas: the VPython canvas wrapper
        :type canvas: VPythonCanvasWrapper
        """
        ...

    def remove(self, *, backend):
        """
        **LLM Docstring**

        Tear down (remove) this axes from its figure (VPython backend).

        """
        ...

    def clear(self, *, backend):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (VPython backend).

        """
        ...

    def get_plotter(self, method):
        """
        **LLM Docstring**

        Resolve a plotting-method name to the backend callable that draws it (VPython backend).

        :param method: the plot-method name
        :return: the result
        """
        ...

    def get_plot_label(self):
        """
        **LLM Docstring**

        Return the plot title/label (VPython backend).

        :return: the result
        """
        ...

    def set_plot_label(self, val, **style):
        """
        **LLM Docstring**

        Set the plot title/label (VPython backend).

        :param val: the label text
        :param style: label styling options
        """
        ...

    def get_style_list(self):
        """
        **LLM Docstring**

        Return the per-series style cycle (VPython backend).

        :return: the result
        """
        ...

    def set_style_list(self, props):
        """
        **LLM Docstring**

        Set the per-series style cycle (VPython backend).

        :param props: the style cycle
        """
        ...

    def get_frame_visible(self):
        """
        **LLM Docstring**

        Return which frame (spine) edges are drawn (VPython backend).

        :return: the result
        """
        ...

    def set_frame_visible(self, frame_spec):
        """
        **LLM Docstring**

        Set which frame (spine) edges are drawn (VPython backend).

        :param frame_spec: the per-edge visibility spec
        """
        ...

    def get_frame_style(self):
        """
        **LLM Docstring**

        Return the frame (spine) styling (VPython backend).

        :return: the result
        """
        ...

    def set_frame_style(self, frame_spec):
        """
        **LLM Docstring**

        Set the frame (spine) styling (VPython backend).

        :param frame_spec: the frame styling
        """
        ...

    def get_xlabel(self):
        """
        **LLM Docstring**

        Return the x-axis label (VPython backend).

        :return: the result
        """
        ...

    def set_xlabel(self, val, **style):
        """
        **LLM Docstring**

        Set the x-axis label (VPython backend).

        :param val: the label text
        :param style: label styling options
        """
        ...

    def get_ylabel(self):
        """
        **LLM Docstring**

        Return the y-axis label (VPython backend).

        :return: the result
        """
        ...

    def set_ylabel(self, val, **style):
        """
        **LLM Docstring**

        Set the y-axis label (VPython backend).

        :param val: the label text
        :param style: label styling options
        """
        ...

    def get_xlim(self):
        """
        **LLM Docstring**

        Return the x-axis limits (VPython backend).

        :return: the result
        """
        ...

    def set_xlim(self, val, **opts):
        """
        **LLM Docstring**

        Set the x-axis limits (VPython backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        ...

    def get_ylim(self):
        """
        **LLM Docstring**

        Return the y-axis limits (VPython backend).

        :return: the result
        """
        ...

    def set_ylim(self, val, **opts):
        """
        **LLM Docstring**

        Set the y-axis limits (VPython backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        ...

    def get_zlim(self):
        """
        **LLM Docstring**

        Return the z-axis limits (VPython backend).

        :return: the result
        """
        ...

    def set_zlim(self, val, **opts):
        """
        **LLM Docstring**

        Set the z-axis limits (VPython backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        ...

    def get_xticks(self):
        """
        **LLM Docstring**

        Return the x-axis tick locations (VPython backend).

        :return: the result
        """
        ...

    def set_xticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the x-axis tick locations (VPython backend).

        :param val: the tick locations
        :param opts: extra options
        """
        ...

    def get_yticks(self):
        """
        **LLM Docstring**

        Return the y-axis tick locations (VPython backend).

        :return: the result
        """
        ...

    def set_yticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the y-axis tick locations (VPython backend).

        :param val: the tick locations
        :param opts: extra options
        """
        ...

    def get_zticks(self):
        """
        **LLM Docstring**

        Return the z-axis tick locations (VPython backend).

        :return: the result
        """
        ...

    def set_zticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the z-axis tick locations (VPython backend).

        :param val: the tick locations
        :param opts: extra options
        """
        ...

    def get_xtick_style(self):
        """
        **LLM Docstring**

        Return the x-axis tick styling (VPython backend).

        :return: the result
        """
        ...

    def set_xtick_style(self, **opts):
        """
        **LLM Docstring**

        Set the x-axis tick styling (VPython backend).

        :param opts: extra options
        """
        ...

    def get_ytick_style(self):
        """
        **LLM Docstring**

        Return the y-axis tick styling (VPython backend).

        :return: the result
        """
        ...

    def set_ytick_style(self, **opts):
        """
        **LLM Docstring**

        Set the y-axis tick styling (VPython backend).

        :param opts: extra options
        """
        ...

    def get_ztick_style(self):
        """
        **LLM Docstring**

        Return the z-axis tick styling (VPython backend).

        :return: the result
        """
        ...

    def set_ztick_style(self, **opts):
        """
        **LLM Docstring**

        Set the z-axis tick styling (VPython backend).

        :param opts: extra options
        """
        ...

    def set_aspect_ratio(self, ar):
        """
        **LLM Docstring**

        Set the axes aspect ratio (VPython backend).

        :param ar: the aspect ratio
        """
        ...

    def get_bbox(self):
        """
        **LLM Docstring**

        Return the axes bounding box (VPython backend).

        :return: the result
        """
        ...

    def set_bbox(self, bbox):
        """
        **LLM Docstring**

        Set the axes bounding box (VPython backend).

        :param bbox: the bounding box
        """
        ...

    def get_facecolor(self):
        """
        **LLM Docstring**

        Return the background/face color (VPython backend).

        :return: the result
        """
        ...

    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color (VPython backend).

        :param fg: the face color
        """
        ...

    def get_padding(self):
        """
        **LLM Docstring**

        Return the axes padding (VPython backend).

        :return: the result
        """
        ...

    def draw_line(self, points, **styles):
        """
        **LLM Docstring**

        Draw a line/polyline through the given points (VPython backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    def draw_disk(self, points, **styles):
        """
        **LLM Docstring**

        Draw a filled disk at the given position(s) (VPython backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    def draw_rect(self, points, **styles):
        """
        **LLM Docstring**

        Draw a rectangle from the given points (VPython backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    def draw_poly(self, points, **styles):
        """
        **LLM Docstring**

        Draw a filled polygon from the given points (VPython backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    def draw_arrow(self, points, **styles):
        """
        **LLM Docstring**

        Draw an arrow from the given points (VPython backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    def draw_text(self, points, vals, **styles):
        """
        **LLM Docstring**

        Draw text at the given position(s) (VPython backend).

        :param points: the points to draw
        :param vals: the text string(s)
        :param styles: the styling options
        """
        ...

    def draw_sphere(self, points, rads, **styles):
        """
        **LLM Docstring**

        Draw a sphere (or spheres) at the given center(s) with the given radii (VPython backend).

        :param points: the sphere center(s)
        :param rads: the sphere radii
        :param styles: the styling options
        """
        ...

    def draw_cylinder(self, start, end, rad, **styles):
        """
        **LLM Docstring**

        Draw a cylinder between two endpoints (VPython backend).

        :param start: the start point
        :param end: the end point
        :param rad: the cylinder radius
        :param styles: the styling options
        """
        ...

    def draw_primitive(self, name, *args, **kwargs):
        """
        **LLM Docstring**

        Draw a named VPython primitive on the axes' canvas.

        :param name: the primitive name
        :type name: str
        :param args: the positional primitive arguments
        :param kwargs: extra primitive options
        :return: the created VPython object
        """
        ...

class VPythonFigure3D(GraphicsFigure):
    Axes = VPythonAxes3D
    _refs = set()

    def __init__(self, vpython_canvas: VPythonCanvasWrapper, **opts):
        """
        **LLM Docstring**

        Wrap a VPython canvas as a 3D figure (tracked to avoid double-wrapping).

        :param vpython_canvas: the VPython canvas (or its wrapper)
        :param opts: canonicalized figure options
        :raises ValueError: if the canvas is already wrapped
        """
        ...

    @classmethod
    def construct(cls, **kw) -> 'GraphicsFigure':
        """
        **LLM Docstring**

        Construct a figure of this backend type (VPython backend).

        :param kw: construction options
        :return: the result
        """
        ...

    def create_axes(self, rows=1, cols=1, spans=1, **kw) -> 'GraphicsAxes':
        """
        **LLM Docstring**

        Create a new axes within the figure at the given grid position (VPython backend).

        :param rows: the number of grid rows
        :param cols: the number of grid columns
        :param spans: the panel span/index
        :param kw: extra keyword options
        :return: the result
        """
        ...

    def create_inset(self, bbox, **kw) -> 'GraphicsAxes':
        """
        **LLM Docstring**

        Create an inset axes at the given bounding box (VPython backend).

        :param bbox: the inset bounding box
        :param kw: extra keyword options
        :return: the result
        """
        ...

    def clear(self, *, backend):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (VPython backend).

        """
        ...

    def close(self, *, backend):
        """
        **LLM Docstring**

        Close the figure (VPython backend).

        """
        ...

    def get_size_inches(self):
        """
        **LLM Docstring**

        Return the figure size in inches (VPython backend).

        :return: the result
        """
        ...

    def set_size_inches(self, w, h):
        """
        **LLM Docstring**

        Set the figure size in inches (VPython backend).

        :param w: the width in inches
        :param h: the height in inches
        """
        ...

    def set_extents(self, extents):
        """
        **LLM Docstring**

        Set the figure's coordinate extents (VPython backend).

        :param extents: the extents
        """
        ...

    def get_facecolor(self):
        """
        **LLM Docstring**

        Return the background/face color (VPython backend).

        :return: the result
        """
        ...

    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color (VPython backend).

        :param fg: the face color
        """
        ...

    def savefig(self, file, **opts):
        """
        **LLM Docstring**

        Save the figure to a file (VPython backend).

        :param file: the destination file/path
        :param opts: extra options
        """
        ...

class VPythonBackend3D(GraphicsBackend):
    Figure = VPythonFigure3D

    def create_raw_figure(self, *args, **kwargs):
        """
        **LLM Docstring**

        Create a new figure (and its initial axes) for this backend (VPython backend).

        :param args: positional arguments
        :param kwargs: extra keyword options
        :return: the result
        """
        ...

    class ThemeContextManager(VPythonBackend.ThemeContextManager):
        ...

    def show_figure(self, graphics, reshow=None):
        """
        **LLM Docstring**

        Display a figure via the backend (VPython backend).

        :param graphics: the `graphics`
        :param reshow: force a reshow of an already-shown figure
        """
        ...

    def get_interactive_status(self) -> 'bool':
        """
        **LLM Docstring**

        Return whether interactive mode is on (VPython backend).

        :return: the result
        """
        ...

    def disable_interactivity(self):
        """
        **LLM Docstring**

        Disable interactive mode (VPython backend).

        """
        ...

    def enable_interactivity(self):
        """
        **LLM Docstring**

        Enable interactive mode (VPython backend).

        """
        ...

    def get_available_themes(self):
        """
        **LLM Docstring**

        Return the themes available for this backend (VPython backend).

        :return: the result
        """
        ...

class X3DAxes(GraphicsAxes3D):

    def __init__(self, *children, title=None, background=None, include_mathjax=None, **opts):
        """
        **LLM Docstring**

        Set up an X3D axes holding its child primitives, title, background, and MathJax
        settings.

        :param children: the child X3D primitives
        :param title: the axes title
        :param background: the background color
        :param include_mathjax: include MathJax for text rendering
        :type include_mathjax: bool | None
        :param opts: extra axes options
        """
        ...

    @classmethod
    def canonicalize_opts(cls, opts):
        """
        **LLM Docstring**

        Normalize construction options into the backend's canonical form (X3D backend).

        :param opts: the options to canonicalize
        """
        ...

    def remove(self, *, backend):
        """
        **LLM Docstring**

        Tear down (remove) this axes from its figure (X3D backend).

        """
        ...

    def clear(self, *, backend):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (X3D backend).

        """
        ...

    def get_plotter(self, method):
        """
        **LLM Docstring**

        Resolve a plotting-method name to the backend callable that draws it (X3D backend).

        :param method: the plot-method name
        :return: the result
        """
        ...

    def get_plot_label(self):
        """
        **LLM Docstring**

        Return the plot title/label (X3D backend).

        :return: the result
        """
        ...

    def set_plot_label(self, val, **style):
        """
        **LLM Docstring**

        Set the plot title/label (X3D backend).

        :param val: the label text
        :param style: label styling options
        """
        ...

    def get_style_list(self):
        """
        **LLM Docstring**

        Return the per-series style cycle (X3D backend).

        :return: the result
        """
        ...

    def set_style_list(self, props):
        """
        **LLM Docstring**

        Set the per-series style cycle (X3D backend).

        :param props: the style cycle
        """
        ...

    def get_frame_visible(self):
        """
        **LLM Docstring**

        Return which frame (spine) edges are drawn (X3D backend).

        :return: the result
        """
        ...

    def set_frame_visible(self, frame_spec):
        """
        **LLM Docstring**

        Set which frame (spine) edges are drawn (X3D backend).

        :param frame_spec: the per-edge visibility spec
        """
        ...

    def get_frame_style(self):
        """
        **LLM Docstring**

        Return the frame (spine) styling (X3D backend).

        :return: the result
        """
        ...

    def set_frame_style(self, frame_spec):
        """
        **LLM Docstring**

        Set the frame (spine) styling (X3D backend).

        :param frame_spec: the frame styling
        """
        ...

    def get_xlabel(self):
        """
        **LLM Docstring**

        Return the x-axis label (X3D backend).

        :return: the result
        """
        ...

    def set_xlabel(self, val, **style):
        """
        **LLM Docstring**

        Set the x-axis label (X3D backend).

        :param val: the label text
        :param style: label styling options
        """
        ...

    def get_ylabel(self):
        """
        **LLM Docstring**

        Return the y-axis label (X3D backend).

        :return: the result
        """
        ...

    def set_ylabel(self, val, **style):
        """
        **LLM Docstring**

        Set the y-axis label (X3D backend).

        :param val: the label text
        :param style: label styling options
        """
        ...

    def get_xlim(self):
        """
        **LLM Docstring**

        Return the x-axis limits (X3D backend).

        :return: the result
        """
        ...

    def set_xlim(self, val, **opts):
        """
        **LLM Docstring**

        Set the x-axis limits (X3D backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        ...

    def get_ylim(self):
        """
        **LLM Docstring**

        Return the y-axis limits (X3D backend).

        :return: the result
        """
        ...

    def set_ylim(self, val, **opts):
        """
        **LLM Docstring**

        Set the y-axis limits (X3D backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        ...

    def get_zlim(self):
        """
        **LLM Docstring**

        Return the z-axis limits (X3D backend).

        :return: the result
        """
        ...

    def set_zlim(self, val, **opts):
        """
        **LLM Docstring**

        Set the z-axis limits (X3D backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        ...

    def get_xticks(self):
        """
        **LLM Docstring**

        Return the x-axis tick locations (X3D backend).

        :return: the result
        """
        ...

    def set_xticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the x-axis tick locations (X3D backend).

        :param val: the tick locations
        :param opts: extra options
        """
        ...

    def get_yticks(self):
        """
        **LLM Docstring**

        Return the y-axis tick locations (X3D backend).

        :return: the result
        """
        ...

    def set_yticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the y-axis tick locations (X3D backend).

        :param val: the tick locations
        :param opts: extra options
        """
        ...

    def get_zticks(self):
        """
        **LLM Docstring**

        Return the z-axis tick locations (X3D backend).

        :return: the result
        """
        ...

    def set_zticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the z-axis tick locations (X3D backend).

        :param val: the tick locations
        :param opts: extra options
        """
        ...

    def get_xtick_style(self):
        """
        **LLM Docstring**

        Return the x-axis tick styling (X3D backend).

        :return: the result
        """
        ...

    def set_xtick_style(self, **opts):
        """
        **LLM Docstring**

        Set the x-axis tick styling (X3D backend).

        :param opts: extra options
        """
        ...

    def get_ytick_style(self):
        """
        **LLM Docstring**

        Return the y-axis tick styling (X3D backend).

        :return: the result
        """
        ...

    def set_ytick_style(self, **opts):
        """
        **LLM Docstring**

        Set the y-axis tick styling (X3D backend).

        :param opts: extra options
        """
        ...

    def get_ztick_style(self):
        """
        **LLM Docstring**

        Return the z-axis tick styling (X3D backend).

        :return: the result
        """
        ...

    def set_ztick_style(self, **opts):
        """
        **LLM Docstring**

        Set the z-axis tick styling (X3D backend).

        :param opts: extra options
        """
        ...

    def set_aspect_ratio(self, ar):
        """
        **LLM Docstring**

        Set the axes aspect ratio (X3D backend).

        :param ar: the aspect ratio
        """
        ...

    def get_bbox(self):
        """
        **LLM Docstring**

        Return the axes bounding box (X3D backend).

        :return: the result
        """
        ...

    def set_bbox(self, bbox):
        """
        **LLM Docstring**

        Set the axes bounding box (X3D backend).

        :param bbox: the bounding box
        """
        ...

    def get_facecolor(self):
        """
        **LLM Docstring**

        Return the background/face color (X3D backend).

        :return: the result
        """
        ...

    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color (X3D backend).

        :param fg: the face color
        """
        ...

    def get_padding(self):
        """
        **LLM Docstring**

        Return the axes padding (X3D backend).

        :return: the result
        """
        ...

    def get_view_settings(self):
        """
        **LLM Docstring**

        Return the 3D camera/view settings (X3D backend).

        :return: the result
        """
        ...

    def set_view_settings(self, **values):
        """
        **LLM Docstring**

        Set the 3D camera/view settings (X3D backend).

        :param values: keyword options
        """
        ...

    @classmethod
    def _apply_dashing(cls, dashing, starts, ends, scaled=None):
        """
        **LLM Docstring**

        Split line segments into dashed sub-segments according to a dashing spec
        (segment/space widths, optionally scaled by segment length).

        :param dashing: the dashing spec (`True`, `[seg, space]`, or a dict)
        :param starts: the segment start points
        :param ends: the segment end points
        :param scaled: interpret the widths as fractions of the segment length
        :type scaled: bool | None
        :return: the `(new_starts, new_ends)` of the dash sub-segments
        :rtype: tuple
        """
        ...

    def draw_line(self, points, indices=None, s=None, riffle=True, line_thickness=None, edgecolors=None, color=None, glow=None, line_style=None, dashing=None, connected=True, **styles):
        """
        **LLM Docstring**

        Draw a line/polyline through the given points (X3D backend).

        :param points: the points to draw
        :param indices: the `indices`
        :param s: the `s`
        :param riffle: the `riffle`
        :param line_thickness: the `line_thickness`
        :param edgecolors: the `edgecolors`
        :param color: the `color`
        :param glow: the `glow`
        :param line_style: the `line_style`
        :param dashing: the `dashing`
        :param connected: the `connected`
        :param styles: the styling options
        """
        ...

    def draw_path(self, commands, **styles):
        """
        **LLM Docstring**

        Draw a path from a sequence of drawing commands (X3D backend).

        :param commands: the path drawing commands
        :param styles: the styling options
        """
        ...

    def draw_disk(self, points, radius=None, color=None, line_color=None, edgecolors=None, s=None, normal=None, line_thickness=None, innerRadius=None, outerRadius=None, uv_axes=None, uv_sign=None, angle=None, rotation=None, solid=None, **styles):
        """
        **LLM Docstring**

        Draw a filled disk at the given position(s) (X3D backend).

        :param points: the points to draw
        :param radius: the `radius`
        :param color: the `color`
        :param line_color: the `line_color`
        :param edgecolors: the `edgecolors`
        :param s: the `s`
        :param normal: the `normal`
        :param line_thickness: the `line_thickness`
        :param innerRadius: the `innerRadius`
        :param outerRadius: the `outerRadius`
        :param uv_axes: the `uv_axes`
        :param uv_sign: the `uv_sign`
        :param angle: the `angle`
        :param rotation: the `rotation`
        :param solid: the `solid`
        :param styles: the styling options
        """
        ...

    def draw_arrow(self, points, **styles):
        """
        **LLM Docstring**

        Draw an arrow from the given points (X3D backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...
    mathjax_cdn = 'https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.min.js'
    default_texture_font = {'font_family': 'sans-serif', 'font_size': '6px', 'dominant_baseline': 'central'}
    font_style_remapping = {'color': 'fill'}

    def texture_svg(self, text, id, font_style=None, resolution=72):
        """
        **LLM Docstring**

        Build an SVG texture (as markup) rendering a text string, for use as an X3D
        texture.

        :param text: the text
        :type text: str
        :param id: the DOM id
        :type id: str
        :param font_style: font styling overrides
        :type font_style: dict | None
        :param resolution: the per-character pixel resolution
        :type resolution: int
        :return: the SVG markup
        :rtype: str
        """
        ...

    def mathjax_load_script(self, text, id, resolution_upscaling=10, font_style=None):
        """
        **LLM Docstring**

        Build the JavaScript that renders a LaTeX string with MathJax and installs the
        resulting SVG as an X3D texture (resizing the target to fit).

        :param text: the LaTeX text
        :type text: str
        :param id: the DOM id
        :type id: str
        :param resolution_upscaling: the texture resolution multiplier
        :type resolution_upscaling: int
        :param font_style: font styling overrides
        :type font_style: dict | None
        :return: the loader script
        :rtype: str
        """
        ...

    @classmethod
    def _is_math(cls, text):
        """
        **LLM Docstring**

        Test whether a text string is a `$...$`-delimited math expression.

        :param text: the text
        :type text: str
        :return: whether it's a math expression
        :rtype: bool
        """
        ...

    @classmethod
    def _prep_font_size(cls, text, font_style, opts, line_height=10, char_width=None, char_width_scaling=1 / 30):
        """
        **LLM Docstring**

        Extract and normalize the font styling (folding in `font_*` options and scaling
        the font size into X3D units).

        :param text: the text being sized
        :param font_style: explicit font styling
        :type font_style: dict | None
        :param opts: the styling options (consumed `font_*` keys removed)
        :type opts: dict
        :param line_height: the line height
        :param char_width: the per-character width
        :param char_width_scaling: the character-width scaling factor
        :return: `(font_style, opts)`
        :rtype: tuple
        """
        ...

    def draw_text(self, points, vals, endpoint=None, allow_mathjax=True, line_height=10, char_width=None, char_width_scaling=1 / 30, font_style=None, **styles):
        """
        **LLM Docstring**

        Draw text at the given position(s) (X3D backend).

        :param points: the points to draw
        :param vals: the text string(s)
        :param endpoint: the `endpoint`
        :param allow_mathjax: the `allow_mathjax`
        :param line_height: the `line_height`
        :param char_width: the `char_width`
        :param char_width_scaling: the `char_width_scaling`
        :param font_style: the `font_style`
        :param styles: the styling options
        """
        ...

    @classmethod
    def prep_uv(cls, uv_axes, normal=None, uv_sign=None, rotation=None, angle=None):
        """
        **LLM Docstring**

        Compute the embedding rotation and angle that place a 2D primitive in 3D given
        its `(u, v)` in-plane axes and an optional plane normal/rotation.

        :param uv_axes: the in-plane `(u, v)` axes
        :param normal: the plane normal (derived from `u`, `v` if omitted)
        :param uv_sign: the orientation sign (inferred if omitted)
        :param rotation: an explicit rotation
        :param angle: an explicit sweep angle
        :return: the embedding rotation/angle data
        """
        ...

    def draw_rect(self, points, color=None, line_color=None, edgecolors=None, normal=None, line_thickness=None, innerRadius=None, outerRadius=None, uv_axes=None, uv_sign=None, angle=None, rotation=None, solid=None, cap_style='round', **styles):
        """
        **LLM Docstring**

        Draw a rectangle from the given points (X3D backend).

        :param points: the points to draw
        :param color: the `color`
        :param line_color: the `line_color`
        :param edgecolors: the `edgecolors`
        :param normal: the `normal`
        :param line_thickness: the `line_thickness`
        :param innerRadius: the `innerRadius`
        :param outerRadius: the `outerRadius`
        :param uv_axes: the `uv_axes`
        :param uv_sign: the `uv_sign`
        :param angle: the `angle`
        :param rotation: the `rotation`
        :param solid: the `solid`
        :param cap_style: the `cap_style`
        :param styles: the styling options
        """
        ...

    def draw_point(self, points, color=None, glow=None, **styles):
        """
        **LLM Docstring**

        Draw a point (as a small disk) at the given position(s) (X3D backend).

        :param points: the points to draw
        :param color: the `color`
        :param glow: the `glow`
        :param styles: the styling options
        """
        ...

    def draw_triangle(self, points, indices=None, **styles):
        """
        **LLM Docstring**

        Draw a triangle from the given points (X3D backend).

        :param points: the points to draw
        :param indices: the `indices`
        :param styles: the styling options
        """
        ...

    def draw_poly(self, points, **styles):
        """
        **LLM Docstring**

        Draw a filled polygon from the given points (X3D backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    def draw_sphere(self, centers, rads, **styles):
        """
        **LLM Docstring**

        Draw a sphere (or spheres) at the given center(s) with the given radii (X3D backend).

        :param centers: the `centers`
        :param rads: the sphere radii
        :param styles: the styling options
        """
        ...

    def draw_cylinder(self, starts, ends, rads, capped=False, **styles):
        """
        **LLM Docstring**

        Draw a cylinder between two endpoints (X3D backend).

        :param starts: the `starts`
        :param ends: the `ends`
        :param rads: the `rads`
        :param capped: the `capped`
        :param styles: the styling options
        """
        ...

    def draw_box(self, start, end, **opts):
        """
        **LLM Docstring**

        Draw an axis-aligned box between two corners (X3D backend).

        :param start: the min corner
        :param end: the max corner
        :param opts: extra options
        """
        ...

    def prep_opts(self):
        """
        **LLM Docstring**

        Assemble the axes' options for X3D scene construction (folding in the background
        and title).

        :return: the options dict
        :rtype: dict
        """
        ...

    def to_x3d(self):
        """
        **LLM Docstring**

        Build the X3D scene from the axes' child primitives and options.

        :return: the X3D scene
        """
        ...

class X3DFigure(GraphicsFigure):
    Axes = X3DAxes

    def __init__(self, width=640, height=500, background='white', figsize=None, profile='Immersive', version='3.3', dynamic_loading=None, include_export_button=None, include_record_button=None, include_view_settings_button=None, recording_options=None, id=None, **opts):
        """
        **LLM Docstring**

        Set up an X3D figure holding its size, profile/version, background, and the
        export/record/view-settings UI options.

        :param width: the figure width in pixels
        :type width: int
        :param height: the figure height in pixels
        :type height: int
        :param background: the background color
        :param figsize: the figure size in inches (overrides width/height)
        :param profile: the X3D profile
        :type profile: str
        :param version: the X3D version
        :type version: str
        :param dynamic_loading: enable dynamic scene loading
        :param include_export_button: include the image-export button
        :param include_record_button: include the screen-record button
        :param include_view_settings_button: include the view-settings button
        :param recording_options: options for the recording UI
        :param id: the DOM id (auto-generated if omitted)
        :param opts: extra options
        """
        ...

    def __setitem__(self, key, value):
        """
        **LLM Docstring**

        Set a figure option by key.

        :param key: the option name
        :param value: the option value
        """
        ...

    def __getitem__(self, item):
        """
        **LLM Docstring**

        Get a figure option by key.

        :param item: the option name
        :return: the option value
        """
        ...

    def clear(self, *, backend):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (X3D backend).

        """
        ...

    def close(self, *, backend):
        """
        **LLM Docstring**

        Close the figure (X3D backend).

        """
        ...

    def create_inset(self, bbox, **kw) -> 'GraphicsAxes':
        """
        **LLM Docstring**

        Create an inset axes at the given bounding box (X3D backend).

        :param bbox: the inset bounding box
        :param kw: extra keyword options
        :return: the result
        """
        ...

    def create_axes(self, rows=1, cols=1, spans=1, **kw) -> 'GraphicsAxes':
        """
        **LLM Docstring**

        Create a new axes within the figure at the given grid position (X3D backend).

        :param rows: the number of grid rows
        :param cols: the number of grid columns
        :param spans: the panel span/index
        :param kw: extra keyword options
        :return: the result
        """
        ...

    @classmethod
    def construct(cls, **kw) -> 'GraphicsFigure':
        """
        **LLM Docstring**

        Construct a figure of this backend type (X3D backend).

        :param kw: construction options
        :return: the result
        """
        ...

    def get_size_inches(self):
        """
        **LLM Docstring**

        Return the figure size in inches (X3D backend).

        :return: the result
        """
        ...

    def set_size_inches(self, w, h):
        """
        **LLM Docstring**

        Set the figure size in inches (X3D backend).

        :param w: the width in inches
        :param h: the height in inches
        """
        ...

    def set_extents(self, extents):
        """
        **LLM Docstring**

        Set the figure's coordinate extents (X3D backend).

        :param extents: the extents
        """
        ...

    def get_facecolor(self):
        """
        **LLM Docstring**

        Return the background/face color (X3D backend).

        :return: the result
        """
        ...

    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color (X3D backend).

        :param fg: the face color
        """
        ...

    def savefig(self, file, format=None, **opts):
        """
        **LLM Docstring**

        Save the figure to a file (X3D backend).

        :param file: the destination file/path
        :param format: the `format`
        :param opts: extra options
        """
        ...

    def prep_opts(self):
        """
        **LLM Docstring**

        Assemble the figure's options for X3D construction (size, profile/version,
        background, UI buttons, etc.).

        :return: the options dict
        :rtype: dict
        """
        ...

    def to_x3d(self, **opts):
        """
        **LLM Docstring**

        Build the full X3D element from the figure's axes, resolving MathJax and onload
        scripts.

        :param opts: extra construction options
        :return: the X3D element
        """
        ...

    def to_widget(self, **opts):
        """
        **LLM Docstring**

        Render the figure as an interactive widget (X3D backend).

        :param opts: extra options
        :return: the result
        """
        ...

    def to_html(self):
        """
        **LLM Docstring**

        Render the figure to HTML (X3D backend).

        :return: the result
        """
        ...

    def animate_frames(self, frames: list['X3DAxes'], mode=None, **animation_opts):
        """
        **LLM Docstring**

        Animate a sequence of frames (X3D backend).

        :param frames: the animation frames
        :param mode: the `mode`
        :param animation_opts: animation options
        """
        ...

class X3DBackend(GraphicsBackend):
    Figure = X3DFigure

    def create_raw_figure(self, *args, **kwargs):
        """
        **LLM Docstring**

        Create a new figure (and its initial axes) for this backend (X3D backend).

        :param args: positional arguments
        :param kwargs: extra keyword options
        :return: the result
        """
        ...

    class ThemeContextManager(GraphicsBackend.ThemeContextManager):
        theme_stack = []

        @classmethod
        def canonicalize_theme_opts(self, theme_parents, theme_spec):
            """
            **LLM Docstring**

            Normalize theme options into the backend's canonical form (X3D backend).

            :param theme_parents: the parent themes
            :param theme_spec: the theme specification
            """
            ...

        def begin_context(self):
            """
            **LLM Docstring**

            Enter the context, applying the theme.

            """
            ...

        def end_context(self, exc_type, exc_val, exc_tb):
            """
            **LLM Docstring**

            Exit the context, restoring the previous theme.

            :param exc_type: the exception type, if any
            :param exc_val: the exception value, if any
            :param exc_tb: the traceback, if any
            """
            ...

    def show_figure(self, graphics: X3DFigure, reshow=None):
        """
        **LLM Docstring**

        Display a figure via the backend (X3D backend).

        :param graphics: the `graphics`
        :param reshow: force a reshow of an already-shown figure
        """
        ...

    def get_interactive_status(self) -> 'bool':
        """
        **LLM Docstring**

        Return whether interactive mode is on (X3D backend).

        :return: the result
        """
        ...

    def disable_interactivity(self):
        """
        **LLM Docstring**

        Disable interactive mode (X3D backend).

        """
        ...

    def enable_interactivity(self):
        """
        **LLM Docstring**

        Enable interactive mode (X3D backend).

        """
        ...

    def get_available_themes(self):
        """
        **LLM Docstring**

        Return the themes available for this backend (X3D backend).

        :return: the result
        """
        ...

class SceneJSONAxes(GraphicsAxes3D):

    def __init__(self, *children, title=None, background=None, **opts):
        """
        **LLM Docstring**

        Set up a SceneJSON axes holding its child primitives, title, and background.

        :param children: the child scene primitives
        :param title: the axes title
        :param background: the background color
        :param opts: extra axes options
        """
        ...

    @classmethod
    def canonicalize_opts(cls, opts):
        """
        **LLM Docstring**

        Normalize construction options into the backend's canonical form (SceneJSON backend).

        :param opts: the options to canonicalize
        """
        ...

    def remove(self, *, backend):
        """
        **LLM Docstring**

        Tear down (remove) this axes from its figure (SceneJSON backend).

        """
        ...

    def clear(self, *, backend):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (SceneJSON backend).

        """
        ...

    def get_plotter(self, method):
        """
        **LLM Docstring**

        Resolve a plotting-method name to the backend callable that draws it (SceneJSON backend).

        :param method: the plot-method name
        :return: the result
        """
        ...

    def get_plot_label(self):
        """
        **LLM Docstring**

        Return the plot title/label (SceneJSON backend).

        :return: the result
        """
        ...

    def set_plot_label(self, val, **style):
        """
        **LLM Docstring**

        Set the plot title/label (SceneJSON backend).

        :param val: the label text
        :param style: label styling options
        """
        ...

    def get_style_list(self):
        """
        **LLM Docstring**

        Return the per-series style cycle (SceneJSON backend).

        :return: the result
        """
        ...

    def set_style_list(self, props):
        """
        **LLM Docstring**

        Set the per-series style cycle (SceneJSON backend).

        :param props: the style cycle
        """
        ...

    def get_frame_visible(self):
        """
        **LLM Docstring**

        Return which frame (spine) edges are drawn (SceneJSON backend).

        :return: the result
        """
        ...

    def set_frame_visible(self, frame_spec):
        """
        **LLM Docstring**

        Set which frame (spine) edges are drawn (SceneJSON backend).

        :param frame_spec: the per-edge visibility spec
        """
        ...

    def get_frame_style(self):
        """
        **LLM Docstring**

        Return the frame (spine) styling (SceneJSON backend).

        :return: the result
        """
        ...

    def set_frame_style(self, frame_spec):
        """
        **LLM Docstring**

        Set the frame (spine) styling (SceneJSON backend).

        :param frame_spec: the frame styling
        """
        ...

    def get_xlabel(self):
        """
        **LLM Docstring**

        Return the x-axis label (SceneJSON backend).

        :return: the result
        """
        ...

    def set_xlabel(self, val, **style):
        """
        **LLM Docstring**

        Set the x-axis label (SceneJSON backend).

        :param val: the label text
        :param style: label styling options
        """
        ...

    def get_ylabel(self):
        """
        **LLM Docstring**

        Return the y-axis label (SceneJSON backend).

        :return: the result
        """
        ...

    def set_ylabel(self, val, **style):
        """
        **LLM Docstring**

        Set the y-axis label (SceneJSON backend).

        :param val: the label text
        :param style: label styling options
        """
        ...

    def get_xlim(self):
        """
        **LLM Docstring**

        Return the x-axis limits (SceneJSON backend).

        :return: the result
        """
        ...

    def set_xlim(self, val, **opts):
        """
        **LLM Docstring**

        Set the x-axis limits (SceneJSON backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        ...

    def get_ylim(self):
        """
        **LLM Docstring**

        Return the y-axis limits (SceneJSON backend).

        :return: the result
        """
        ...

    def set_ylim(self, val, **opts):
        """
        **LLM Docstring**

        Set the y-axis limits (SceneJSON backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        ...

    def get_zlim(self):
        """
        **LLM Docstring**

        Return the z-axis limits (SceneJSON backend).

        :return: the result
        """
        ...

    def set_zlim(self, val, **opts):
        """
        **LLM Docstring**

        Set the z-axis limits (SceneJSON backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        ...

    def get_xticks(self):
        """
        **LLM Docstring**

        Return the x-axis tick locations (SceneJSON backend).

        :return: the result
        """
        ...

    def set_xticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the x-axis tick locations (SceneJSON backend).

        :param val: the tick locations
        :param opts: extra options
        """
        ...

    def get_yticks(self):
        """
        **LLM Docstring**

        Return the y-axis tick locations (SceneJSON backend).

        :return: the result
        """
        ...

    def set_yticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the y-axis tick locations (SceneJSON backend).

        :param val: the tick locations
        :param opts: extra options
        """
        ...

    def get_zticks(self):
        """
        **LLM Docstring**

        Return the z-axis tick locations (SceneJSON backend).

        :return: the result
        """
        ...

    def set_zticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the z-axis tick locations (SceneJSON backend).

        :param val: the tick locations
        :param opts: extra options
        """
        ...

    def get_xtick_style(self):
        """
        **LLM Docstring**

        Return the x-axis tick styling (SceneJSON backend).

        :return: the result
        """
        ...

    def set_xtick_style(self, **opts):
        """
        **LLM Docstring**

        Set the x-axis tick styling (SceneJSON backend).

        :param opts: extra options
        """
        ...

    def get_ytick_style(self):
        """
        **LLM Docstring**

        Return the y-axis tick styling (SceneJSON backend).

        :return: the result
        """
        ...

    def set_ytick_style(self, **opts):
        """
        **LLM Docstring**

        Set the y-axis tick styling (SceneJSON backend).

        :param opts: extra options
        """
        ...

    def get_ztick_style(self):
        """
        **LLM Docstring**

        Return the z-axis tick styling (SceneJSON backend).

        :return: the result
        """
        ...

    def set_ztick_style(self, **opts):
        """
        **LLM Docstring**

        Set the z-axis tick styling (SceneJSON backend).

        :param opts: extra options
        """
        ...

    def set_aspect_ratio(self, ar):
        """
        **LLM Docstring**

        Set the axes aspect ratio (SceneJSON backend).

        :param ar: the aspect ratio
        """
        ...

    def get_bbox(self):
        """
        **LLM Docstring**

        Return the axes bounding box (SceneJSON backend).

        :return: the result
        """
        ...

    def set_bbox(self, bbox):
        """
        **LLM Docstring**

        Set the axes bounding box (SceneJSON backend).

        :param bbox: the bounding box
        """
        ...

    def get_facecolor(self):
        """
        **LLM Docstring**

        Return the background/face color (SceneJSON backend).

        :return: the result
        """
        ...

    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color (SceneJSON backend).

        :param fg: the face color
        """
        ...

    def get_padding(self):
        """
        **LLM Docstring**

        Return the axes padding (SceneJSON backend).

        :return: the result
        """
        ...

    def get_view_settings(self):
        """
        **LLM Docstring**

        Return the 3D camera/view settings (SceneJSON backend).

        :return: the result
        """
        ...

    def set_view_settings(self, **values):
        """
        **LLM Docstring**

        Set the 3D camera/view settings (SceneJSON backend).

        :param values: keyword options
        """
        ...

    def draw_line(self, points, **styles):
        """
        **LLM Docstring**

        Draw a line/polyline through the given points (SceneJSON backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    def draw_disk(self, points, rads=1, **styles):
        """
        **LLM Docstring**

        Draw a filled disk at the given position(s) (SceneJSON backend).

        :param points: the points to draw
        :param rads: the `rads`
        :param styles: the styling options
        """
        ...

    def draw_arrow(self, points, radius=0.1, **styles):
        """
        **LLM Docstring**

        Draw an arrow from the given points (SceneJSON backend).

        :param points: the points to draw
        :param radius: the `radius`
        :param styles: the styling options
        """
        ...

    def draw_text(self, points, vals, **styles):
        """
        **LLM Docstring**

        Draw text at the given position(s) (SceneJSON backend).

        :param points: the points to draw
        :param vals: the text string(s)
        :param styles: the styling options
        """
        ...

    def draw_rect(self, points, **styles):
        """
        **LLM Docstring**

        Draw a rectangle from the given points (SceneJSON backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    def draw_poly(self, points, **styles):
        """
        **LLM Docstring**

        Draw a filled polygon from the given points (SceneJSON backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        ...

    def draw_sphere(self, centers, rads, **styles):
        """
        **LLM Docstring**

        Draw a sphere (or spheres) at the given center(s) with the given radii (SceneJSON backend).

        :param centers: the `centers`
        :param rads: the sphere radii
        :param styles: the styling options
        """
        ...

    def draw_cylinder(self, starts, ends, rads, **styles):
        """
        **LLM Docstring**

        Draw a cylinder between two endpoints (SceneJSON backend).

        :param starts: the `starts`
        :param ends: the `ends`
        :param rads: the `rads`
        :param styles: the styling options
        """
        ...

    def to_json(self):
        """
        **LLM Docstring**

        Serialize the axes (its children and options) to the scene-JSON representation.

        :return: the scene-JSON object
        :rtype: dict
        """
        ...

class SceneJSONFigure(GraphicsFigure):
    Axes = SceneJSONAxes

    def __init__(self, width=640, height=500, background='white', figsize=None, profile='Immersive', version='3.3', id=None, **opts):
        """
        **LLM Docstring**

        Set up a SceneJSON figure holding its axes and options.

        :param args: positional figure arguments
        :param opts: figure options
        """
        ...

    def __setitem__(self, key, value):
        """
        **LLM Docstring**

        Set a figure option by key.

        :param key: the option name
        :param value: the option value
        """
        ...

    def __getitem__(self, item):
        """
        **LLM Docstring**

        Get a figure option by key.

        :param item: the option name
        :return: the option value
        """
        ...

    def clear(self, *, backend):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (SceneJSON backend).

        """
        ...

    def close(self, *, backend):
        """
        **LLM Docstring**

        Close the figure (SceneJSON backend).

        """
        ...

    def create_inset(self, bbox, **kw) -> 'GraphicsAxes':
        """
        **LLM Docstring**

        Create an inset axes at the given bounding box (SceneJSON backend).

        :param bbox: the inset bounding box
        :param kw: extra keyword options
        :return: the result
        """
        ...

    def create_axes(self, rows=1, cols=1, spans=1, **kw) -> 'GraphicsAxes':
        """
        **LLM Docstring**

        Create a new axes within the figure at the given grid position (SceneJSON backend).

        :param rows: the number of grid rows
        :param cols: the number of grid columns
        :param spans: the panel span/index
        :param kw: extra keyword options
        :return: the result
        """
        ...

    @classmethod
    def construct(cls, **kw) -> 'GraphicsFigure':
        """
        **LLM Docstring**

        Construct a figure of this backend type (SceneJSON backend).

        :param kw: construction options
        :return: the result
        """
        ...

    def get_size_inches(self):
        """
        **LLM Docstring**

        Return the figure size in inches (SceneJSON backend).

        :return: the result
        """
        ...

    def set_size_inches(self, w, h):
        """
        **LLM Docstring**

        Set the figure size in inches (SceneJSON backend).

        :param w: the width in inches
        :param h: the height in inches
        """
        ...

    def set_extents(self, extents):
        """
        **LLM Docstring**

        Set the figure's coordinate extents (SceneJSON backend).

        :param extents: the extents
        """
        ...

    def get_facecolor(self):
        """
        **LLM Docstring**

        Return the background/face color (SceneJSON backend).

        :return: the result
        """
        ...

    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color (SceneJSON backend).

        :param fg: the face color
        """
        ...

    def savefig(self, file, format=None, **opts):
        """
        **LLM Docstring**

        Save the figure to a file (SceneJSON backend).

        :param file: the destination file/path
        :param format: the `format`
        :param opts: extra options
        """
        ...

    def to_json(self, **opts):
        """
        **LLM Docstring**

        Serialize the whole figure (its axes and options) to the scene-JSON
        representation.

        :return: the scene-JSON object
        :rtype: dict
        """
        ...

    def animate_frames(self, frames: list['SceneJSONAxes'], **animation_opts):
        """
        **LLM Docstring**

        Animate a sequence of frames (SceneJSON backend).

        :param frames: the animation frames
        :param animation_opts: animation options
        """
        ...

class SceneJSONBackend(GraphicsBackend):
    Figure = SceneJSONFigure

    def create_raw_figure(self, *args, **kwargs):
        """
        **LLM Docstring**

        Create a new figure (and its initial axes) for this backend (SceneJSON backend).

        :param args: positional arguments
        :param kwargs: extra keyword options
        :return: the result
        """
        ...

    class ThemeContextManager(GraphicsBackend.ThemeContextManager):
        theme_stack = []

        @classmethod
        def canonicalize_theme_opts(self, theme_parents, theme_spec):
            """
            **LLM Docstring**

            Normalize theme options into the backend's canonical form (SceneJSON backend).

            :param theme_parents: the parent themes
            :param theme_spec: the theme specification
            """
            ...

        def begin_context(self):
            """
            **LLM Docstring**

            Enter the context, applying the theme.

            """
            ...

        def end_context(self, exc_type, exc_val, exc_tb):
            """
            **LLM Docstring**

            Exit the context, restoring the previous theme.

            :param exc_type: the exception type, if any
            :param exc_val: the exception value, if any
            :param exc_tb: the traceback, if any
            """
            ...

    def show_figure(self, graphics: SceneJSONFigure, reshow=None):
        """
        **LLM Docstring**

        Display a figure via the backend (SceneJSON backend).

        :param graphics: the `graphics`
        :param reshow: force a reshow of an already-shown figure
        """
        ...

    def get_interactive_status(self) -> 'bool':
        """
        **LLM Docstring**

        Return whether interactive mode is on (SceneJSON backend).

        :return: the result
        """
        ...

    def disable_interactivity(self):
        """
        **LLM Docstring**

        Disable interactive mode (SceneJSON backend).

        """
        ...

    def enable_interactivity(self):
        """
        **LLM Docstring**

        Enable interactive mode (SceneJSON backend).

        """
        ...

    def get_available_themes(self):
        """
        **LLM Docstring**

        Return the themes available for this backend (SceneJSON backend).

        :return: the result
        """
        ...
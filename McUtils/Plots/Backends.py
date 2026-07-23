"""
For now, just a super simple Enum of supported backends
Maybe in the future we'll add better support so that the backends themselves can all support a common subset
of features, but I think we'll 90% of the time just want to use MPL or VTK so who knows...
If that happens, lots of the 'if backend == MPL' stuff will change to use a Backend object
"""

from __future__ import annotations

__all__ = [
    "GraphicsBackend"
]

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
    def __init__(self,
                 tick_getter,
                 tick_setter,
                 tick_locator,
                 minor_tick_locator,
                 tick_formatter,
                 minor_tick_formatter
                 ):
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
        self.get_ticks = tick_getter
        self.set_ticks = tick_setter
        self.set_major_locator = tick_locator
        self.set_minor_locator = minor_tick_locator
        self.set_major_formatter = tick_formatter
        self.set_minor_formatter = minor_tick_formatter


class XAxisManager(AxisManager):
    def get_xticks(self):
        """
        **LLM Docstring**

        Return the x-axis tick locations.

        :return: the result
        """
        return self.get_ticks()
    def set_xticks(self, ticks, **kwargs):
        """
        **LLM Docstring**

        Set the x-axis tick locations.

        :param ticks: the tick locations
        :param kwargs: extra keyword options
        """
        return self.set_ticks(ticks, **kwargs)

class YAxisManager(AxisManager):
    def get_yticks(self):
        """
        **LLM Docstring**

        Return the y-axis tick locations.

        :return: the result
        """
        return self.get_ticks()
    def set_yticks(self, ticks, **kwargs):
        """
        **LLM Docstring**

        Set the y-axis tick locations.

        :param ticks: the tick locations
        :param kwargs: extra keyword options
        """
        return self.set_ticks(ticks, **kwargs)

class ZAxisManager(AxisManager):
    def get_zticks(self):
        """
        **LLM Docstring**

        Return the z-axis tick locations.

        :return: the result
        """
        return self.get_ticks()
    def set_zticks(self, ticks, **kwargs):
        """
        **LLM Docstring**

        Set the z-axis tick locations.

        :param ticks: the tick locations
        :param kwargs: extra keyword options
        """
        return self.set_ticks(ticks, **kwargs)

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
        self.xaxis = self.get_xaxis_manager()
        self.yaxis = self.get_yaxis_manager()

    def get_xaxis_manager(self):
        """
        **LLM Docstring**

        Build the x-axis tick manager for this axes.

        :return: the result
        """
        return XAxisManager(
            self.get_xticks,
            self.set_xticks,
            None,
            None,
            None,
            None
        )
    def get_yaxis_manager(self):
        """
        **LLM Docstring**

        Build the y-axis tick manager for this axes.

        :return: the result
        """
        return YAxisManager(
            self.get_yticks,
            self.set_yticks,
            None,
            None,
            None,
            None
        )

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
                self.locs = locs
                self.opts = opts

    @classmethod
    def canonicalize_opts(cls, opts):
        """
        **LLM Docstring**

        Normalize construction options into the backend's canonical form.

        :param opts: the options to canonicalize
        """
        return opts
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
        raise NotImplementedError(...)
    def set_grid_visible(self, grid_spec):
        raise NotImplementedError(...)
    def get_grid_style(self):
        raise NotImplementedError(...)
    def set_grid_style(self, grid_spec):
        raise NotImplementedError(...)

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
        raise NotImplementedError("legend")

    def get_graphics_properties(self, obj, property=None):
        """
        **LLM Docstring**

        Get backend properties of a drawn graphics object.

        :param obj: the graphics object
        :param property: a specific property to fetch
        :return: the result
        """
        raise NotImplementedError("get_graphics_properties")
    def set_graphics_properties(self, obj, **props):
        """
        **LLM Docstring**

        Set backend properties on a drawn graphics object.

        :param obj: the graphics object
        :param props: the properties to set
        """
        raise NotImplementedError("set_graphics_properties")

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
        return self.draw_disk(points, **styles)
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
        return self.draw_poly(points, **styles)
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
        super().__init__()
        self.zaxis = ZAxisManager(
            self.get_zticks,
            self.set_zticks,
            None,
            None,
            None,
            None
        )

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
        self.shown = False
        self.axes = axes
    @classmethod
    def construct(self, **kw) -> 'GraphicsFigure':
        """
        **LLM Docstring**

        Construct a figure of this backend type.

        :param kw: construction options
        :return: the result
        """
        raise NotImplementedError("needs an overload")
    @classmethod
    def canonicalize_opts(cls, opts):
        """
        **LLM Docstring**

        Normalize construction options into the backend's canonical form.

        :param opts: the options to canonicalize
        """
        return opts
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
        raise NotImplementedError("create_colorbar")
    def add_axes(self, ax) -> 'GraphicsAxes':
        """
        **LLM Docstring**

        Add an existing axes object to the figure.

        :param ax: the axes to add
        """
        if self.axes is None: self.axes = []
        if not isinstance(ax, self.Axes): ax = self.Axes(ax)
        self.axes.append(ax)
        return ax
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
        return [
            a.get_bbox() for a in self.axes
        ]
    def prep_show(self):
        """
        **LLM Docstring**

        Prepare the axes/figure for display.

        """
        if self.axes is not None:
            for a in self.axes:
                a.prep_show()

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
        raise NotImplementedError("needs an overload")
    def to_widget(self, **opts):
        """
        **LLM Docstring**

        Render the figure as an interactive widget.

        :param opts: extra options
        :return: the result
        """
        raise NotImplementedError("needs an overload")
    def _repr_html_(self):
        """
        **LLM Docstring**

        Return the figure's HTML representation for IPython (delegates to `to_html`).

        :return: the HTML
        :rtype: str
        """
        return self.to_html()
    def get_mime_bundle(self):
        """
        **LLM Docstring**

        Return the figure's MIME bundle for rich display.

        :return: the result
        """
        try:
            html = self.to_html()
        except NotImplementedError:
            buf = io.BytesIO()
            self.savefig(buf, format='png')
            data = {
                'image/png':buf.getvalue()
            }
        else:
            data = {
                'text/html': html
            }
        return data
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
        kwargs = self.figure_defaults | kwargs
        return self.create_raw_figure(*args, **kwargs)
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
    def create_axes(self, figure:'GraphicsFigure', *args, **kwargs):
        """
        **LLM Docstring**

        Create a new axes within the figure at the given grid position.

        :param figure: the `figure`
        :param args: positional arguments
        :param kwargs: extra keyword options
        :return: the result
        """
        kwargs = self.axes_defaults | kwargs
        return figure.create_axes(*args, **kwargs, backend=self)
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
        kw = self.inset_defaults | kw
        return figure.create_inset(*args, **kw)
    def close_figure(self, figure:'GraphicsFigure'):
        """
        **LLM Docstring**

        Close a figure via the backend.

        :param figure: the figure to close
        """
        return figure.close(backend=self)
    def remove_axes(self, axes:'GraphicsAxes'):
        """
        **LLM Docstring**

        Remove an axes via the backend.

        :param axes: the axes to remove
        """
        return axes.remove(backend=self)
    def clear_figure(self, figure:'GraphicsFigure'):
        """
        **LLM Docstring**

        Clear a figure via the backend.

        :param figure: the figure to clear
        """
        return figure.clear(backend=self)
    def clear_axes(self, axes:'GraphicsAxes'):
        """
        **LLM Docstring**

        Clear an axes via the backend.

        :param axes: the axes to clear
        """
        return axes.clear(backend=self)
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
    def to_widget(self, figure:GraphicsFigure):
        """
        **LLM Docstring**

        Render the figure as an interactive widget.

        :param figure: the `figure`
        :return: the result
        """
        return figure.to_widget()

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
            self.backend = backend
            self.spec, self.opts = self.canonicalize_theme_opts(theme_parents, theme_spec)
            self.backend_theme_stack = []

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
            self.backend_theme_stack.append((
                self.backend.figure_defaults,
                self.backend.axes_defaults,
                self.backend.inset_defaults
            ))
            spec = self.opts.copy()
            axes_defaults = spec.pop('axes', {})
            inset_defaults = spec.pop('inset', {})
            self.backend.figure_defaults = self.backend.figure_defaults | spec
            self.backend.axes_defaults = self.backend.axes_defaults | axes_defaults
            self.backend.inset_defaults = self.backend.inset_defaults | inset_defaults
            return self.begin_context()
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
            figure_defaults, axes_defaults, inset_defaults = self.backend_theme_stack.pop()
            self.backend.figure_defaults = figure_defaults
            self.backend.axes_defaults = axes_defaults
            self.backend.inset_defaults = inset_defaults
            return self.end_context(exc_type, exc_val, exc_tb)
    def theme_context(self, theme_parents, spec):
        """
        **LLM Docstring**

        Return a context manager that applies a theme for this backend.

        :param theme_parents: the parent themes
        :param spec: the theme specification
        """
        return self.ThemeContextManager(theme_parents, spec, self)

    class DefaultBackends(enum.Enum):
        MPL = 'matplotlib'
        MPL3D = 'matplotlib3D'
        VTK = 'vtk'
        VPython = 'vpython'
        VPython2D = 'vpython2D'
        X3D = 'x3d'
        SVG = 'svg'
        SVG3D = 'svg3D'
        SceneJSON = 'json'
        Plotly = 'plotly'
        Plotly3D = 'plotly3D'

    registered_backends = {}
    @classmethod
    def get_default_backends(cls):
        """
        **LLM Docstring**

        Return the mapping of default backend names to their backend classes.

        :return: the default-backends mapping
        :rtype: dict
        """
        return {
            cls.DefaultBackends.MPL.value: MPLBackend,
            cls.DefaultBackends.MPL3D.value: MPLBackend3D,
            cls.DefaultBackends.Plotly.value: PlotlyBackend,
            cls.DefaultBackends.Plotly3D.value: PlotlyBackend3D,
            cls.DefaultBackends.VTK.value: VTKBackend,
            cls.DefaultBackends.VPython2D.value: VPythonBackend,
            cls.DefaultBackends.VPython.value: VPythonBackend3D,
            cls.DefaultBackends.X3D.value: X3DBackend,
            cls.DefaultBackends.SVG.value: SVGBackend,
            cls.DefaultBackends.SVG3D.value: SVGBackend3D,
            cls.DefaultBackends.SceneJSON.value: SceneJSONBackend,
        }
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
        if opts is None: opts = {}
        if not isinstance(backend, GraphicsBackend):
            name = backend
            backend = cls.registered_backends.get(name, None)
            if backend is None:
                backend_key = cls.DefaultBackends(name).value
                backend = cls.get_default_backends().get(backend_key)
        return backend(**opts)

class MPLManager:
    _plt = None
    _patch = None
    _path = None
    _coll = None
    _mpl = None
    _colors = None
    _jlab = None
    _widg = None
    _anim = None

    @classmethod
    def plt_api(cls):
        """
        **LLM Docstring**

        Lazily import and cache `matplotlib.pyplot`, returning the module.

        :return: the `matplotlib.pyplot` module
        """
        if cls._plt is None:
            import matplotlib.pyplot as plt
            cls._plt = plt
        return cls._plt
    @classmethod
    def mpl_api(cls):
        """
        **LLM Docstring**

        Lazily import and cache the top-level `matplotlib` module, returning it.

        :return: the `matplotlib` module
        """
        if cls._mpl is None:
            import matplotlib as mpl
            cls._mpl = mpl
        return cls._mpl
    @classmethod
    def color_api(cls):
        """
        **LLM Docstring**

        Lazily import and cache `matplotlib.colors`, returning the module.

        :return: the `matplotlib.colors` module
        """
        if cls._colors is None:
            import matplotlib.colors as colors
            cls._colors = colors
        return cls._colors

    @classmethod
    def patch_api(cls):
        """
        **LLM Docstring**

        Lazily import and cache `matplotlib.patches`, returning the module.

        :return: the `matplotlib.patches` module
        """
        if cls._patch is None:
            import matplotlib.patches as patch
            cls._patch = patch
        return cls._patch
    @classmethod
    def path_api(cls):
        """
        **LLM Docstring**

        Lazily import and cache `matplotlib.path`, returning the module.

        :return: the `matplotlib.path` module
        """
        if cls._path is None:
            import matplotlib.path as patch
            cls._path = patch
        return cls._path
    @classmethod
    def collections_api(cls):
        """
        **LLM Docstring**

        Lazily import and cache `matplotlib.collections`, returning the module.

        :return: the `matplotlib.collections` module
        """
        if cls._coll is None:
            import matplotlib.collections as coll
            cls._coll = coll
        return cls._coll
    @classmethod
    def widgets_api(cls):
        """
        **LLM Docstring**

        Lazily import and cache `matplotlib.widgets`, returning the module.

        :return: the `matplotlib.widgets` module
        """
        if cls._widg is None:
            import matplotlib.widgets as widg
            cls._widg = widg
        return cls._widg
    @classmethod
    def animations_api(cls):
        """
        **LLM Docstring**

        Lazily import and cache `matplotlib.animation`, returning the module.

        :return: the `matplotlib.animation` module
        """
        if cls._anim is None:
            import matplotlib.animation as anim
            cls._anim = anim
        return cls._anim
    @classmethod
    def draw_if_interactive(self, *args, **kwargs):
        """
        **LLM Docstring**

        No-op override of matplotlib's interactive-draw hook (used to suppress automatic
        drawing).

        :param args: ignored
        :param kwargs: ignored
        """
        pass
    @classmethod
    def magic_backend(self, backend):
        """
        **LLM Docstring**

        Set the matplotlib backend via the IPython `%matplotlib` magic when running in a
        notebook.

        :param backend: the backend name
        :type backend: str
        """
        try:
            from IPython.core.getipython import get_ipython
        except ImportError:
            pass
        else:
            shell = get_ipython()
            ip_name = type(shell).__name__
            in_nb = ip_name == 'ZMQInteractiveShell'
            if in_nb:
                try:
                    from IPython.core.magics import PylabMagics
                except ImportError:
                    pass
                else:
                    set_jupyter_backend = PylabMagics(shell).matplotlib
                    set_jupyter_backend(backend)

    # This flag will be reset by draw_if_interactive when called
    _draw_called = False
    # list of figures to draw when flush_figures is called
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
        old_backend = None
        was_interactive = None
        drawer = None
        draw_all = None
        old_magic_backend = None
        old_show = None

        mpl = cls.mpl_api()
        plt = cls.plt_api()

        if figure.mpl_backend is not None:
            old_backend = mpl.get_backend()
        was_interactive = plt.isinteractive()

        cls.settings_stack.append((
            old_backend,
            was_interactive,
            drawer,
            draw_all,
            old_magic_backend,
            old_show
        ))
        try:
            if not figure.managed:
                # import matplotlib.pyplot as plt
                # plt.ioff
                # if 'inline' in self.mpl.get_backend():
                #     backend = self.plt._backend_mod
                #     self.plt.show = ...
                #     self._old_show = backend.show
                #     backend.show = self.jupyter_show
                if not figure.interactive:
                    plt.ioff()
                    # manager.canvas.mpl_disconnect(manager._cidgcf)
                    # self._drawer = self.plt.draw_if_interactive
                    # self._draw_all = self.plt.draw_all
                    # self.plt.draw_if_interactive = self.draw_if_interactive
                    # self.plt.draw_all = self.draw_if_interactive
                    # if self.fig.mpl_backend is None:
                    #     self._old_magic_backend = self.mpl.get_backend()
                    #     self.magic_backend('Agg')
                else:
                    plt.ion()
                    # if self.fig.mpl_backend is None:
                    #     self._old_magic_backend = self.mpl.get_backend()
                    #     if 'inline' not in self._old_magic_backend:
                    #         self.magic_backend('inline')

            yield None
        finally:
            (
                old_backend,
                was_interactive,
                drawer,
                draw_all,
                old_magic_backend,
                old_show
            ) = cls.settings_stack.pop()

            if old_backend is not None:
                mpl.use(old_backend)
            if drawer is not None:
                plt.draw_if_interactive = drawer
            if draw_all is not None:
                plt.draw_all = draw_all
            if old_show is not None:
                plt._backend_mod.show = old_show

            if old_magic_backend is not None:
                if 'inline' in old_magic_backend:
                    cls.magic_backend('inline')
                else:
                    mpl.use(old_magic_backend)
            if was_interactive and not plt.isinteractive():
                plt.ion()

    @classmethod
    def mpl_disconnect(cls, graphics):
        """
        **LLM Docstring**

        Detach a figure from matplotlib's global figure manager (`Gcf`) when using an
        inline backend, so it isn't auto-displayed.

        :param graphics: the figure's graphics object
        """
        # this is a hack that might need to be updated in the future
        if 'inline' in cls.mpl_api().get_backend():
            try:
                from matplotlib._pylab_helpers import Gcf
                canvas = graphics.figure.canvas
                num = canvas.manager.num
                if all(hasattr(num, attr) for attr in ["num", "_cidgcf", "destroy"]):
                    manager = num
                    if Gcf.figs.get(manager.num) is manager:
                        Gcf.figs.pop(manager.num)
                    else:
                        return
                else:
                    try:
                        manager = Gcf.figs.pop(num)
                    except KeyError:
                        return
                # manager.canvas.mpl_disconnect(manager._cidgcf)
                # self.fig.figure.canvas.mpl_disconnect(
                #     self.fig.figure.canvas.manager._cidgcf
                # )
            except:
                pass

    @classmethod
    def mpl_connect(cls, graphics):
        """
        **LLM Docstring**

        Register a figure with matplotlib's global figure manager (`Gcf`) under an inline
        backend, wiring up its activation handler.

        :param graphics: the figure's graphics object
        """
        if 'inline' in cls.mpl_api().get_backend():
            # try:
            from matplotlib._pylab_helpers import Gcf
            canvas = graphics.figure.canvas
            manager = canvas.manager
            num = canvas.manager.num
            Gcf.figs[num] = manager
            manager._cidgcf = canvas.mpl_connect(
                "button_press_event", lambda event: Gcf.set_active(manager)
            )
            # manager.canvas.mpl_disconnect(manager._cidgcf)
            # self.fig.figure.canvas.mpl_disconnect(
            #     self.fig.figure.canvas.manager._cidgcf
            # )
            # except:
            #     pass

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

        from matplotlib._pylab_helpers import Gcf
        from IPython.core.display import display
        plt = cls.plt_api()
        mpl_inline = plt._backend_mod

        if close is None:
            close = mpl_inline.InlineBackend.instance().close_figures
        try:
            for figure_manager in [Gcf.get_active()]:
                display(
                    figure_manager.canvas.figure,
                    metadata=mpl_inline._fetch_figure_metadata(figure_manager.canvas.figure)
                )
        finally:
            cls._to_draw = []
            # only call close('all') if any to close
            # close triggers gc.collect, which can be slow
            if close and Gcf.get_all_fig_managers():
                plt.close('all')

class MPLAxes(GraphicsAxes):
    def __init__(self, mpl_axes_object, **opts):
        """
        **LLM Docstring**

        Wrap a matplotlib `Axes` object, exposing it through the canonical `GraphicsAxes`
        interface.

        :param mpl_axes_object: the backing matplotlib axes
        :param opts: canonicalized axes options
        """
        self.obj = mpl_axes_object
        self.opts = self.canonicalize_opts(opts)
        super().__init__()
        self.xaxis = self.obj.xaxis
        self.yaxis = self.obj.yaxis

    class TicksManager:
        def __init__(self):
            """
            **LLM Docstring**

            Import and cache matplotlib's tick locator/formatter classes for building tick
            specifications.
            """
            import matplotlib.ticker as ticks
            self._Locator = ticks.Locator
            self._FixedLocator = ticks.FixedLocator
            self._AutoLocator = ticks.AutoLocator
            self._AutoMinorLocator = ticks.AutoMinorLocator
            self._MultipleLocator = ticks.MultipleLocator
            self._StrMethodFormatter = ticks.StrMethodFormatter
            self._NullFormatter = ticks.NullFormatter
            self._FixedFormatter = ticks.FixedFormatter
            self._ScalarFormatter = ticks.ScalarFormatter
        @property
        def Locator(self):
            """
            **LLM Docstring**

            Return matplotlib's `Locator` locator base class.

            :return: the `Locator` class
            """
            return self._Locator
        @property
        def FixedLocator(self):
            """
            **LLM Docstring**

            Return matplotlib's `FixedLocator` locator class.

            :return: the `FixedLocator` class
            """
            return self._FixedLocator
        @property
        def AutoLocator(self):
            """
            **LLM Docstring**

            Return matplotlib's `AutoLocator` locator class.

            :return: the `AutoLocator` class
            """
            return self._AutoLocator
        @property
        def AutoMinorLocator(self):
            """
            **LLM Docstring**

            Return matplotlib's `AutoMinorLocator` locator class.

            :return: the `AutoMinorLocator` class
            """
            return self._AutoMinorLocator
        @property
        def MultipleLocator(self):
            """
            **LLM Docstring**

            Return matplotlib's `MultipleLocator` locator class.

            :return: the `MultipleLocator` class
            """
            return self._MultipleLocator
        @property
        def StrMethodFormatter(self):
            """
            **LLM Docstring**

            Return matplotlib's `StrMethodFormatter` formatter class.

            :return: the `StrMethodFormatter` class
            """
            return self._StrMethodFormatter
        @property
        def NullFormatter(self):
            """
            **LLM Docstring**

            Return matplotlib's `NullFormatter` formatter class.

            :return: the `NullFormatter` class
            """
            return self._NullFormatter
        @property
        def FixedFormatter(self):
            """
            **LLM Docstring**

            Return matplotlib's `FixedFormatter` formatter class.

            :return: the `FixedFormatter` class
            """
            return self._FixedFormatter
        @property
        def ScalarFormatter(self):
            """
            **LLM Docstring**

            Return matplotlib's `ScalarFormatter` formatter class.

            :return: the `ScalarFormatter` class
            """
            return self._ScalarFormatter

    def clear(self, *, backend=None):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (matplotlib backend).

        """
        ax = self.obj
        all_things = ax.artists + ax.patches
        for a in all_things:
            a.remove()
    def remove(self, *, backend):
        """
        **LLM Docstring**

        Tear down (remove) this axes from its figure (matplotlib backend).

        """
        self.obj.remove()

    def get_plotter(self, method):
        """
        **LLM Docstring**

        Resolve a plotting-method name to the backend callable that draws it (matplotlib backend).

        :param method: the plot-method name
        :return: the result
        """
        plot_method = getattr(self.obj, method)
        def plot(*data, **styles):
            """
            **LLM Docstring**

            Call the resolved matplotlib plot method with the given data and styles.

            :param data: the plot data
            :param styles: the styling options
            :return: the matplotlib graphics object
            """
            return plot_method(*data, **styles)
        return plot


    def get_plot_label(self):
        """
        **LLM Docstring**

        Return the plot title/label (matplotlib backend).

        :return: the result
        """
        return self.obj.set_title()
    def set_plot_label(self, val, **style):
        """
        **LLM Docstring**

        Set the plot title/label (matplotlib backend).

        :param val: the label text
        :param style: label styling options
        """
        self.obj.set_title(val, **style)

    def get_style_list(self):
        """
        **LLM Docstring**

        Return the per-series style cycle (matplotlib backend).

        :return: the result
        """
        raise NotImplementedError("style list cyclers not supported")
    def set_style_list(self, props):
        """
        **LLM Docstring**

        Set the per-series style cycle (matplotlib backend).

        :param props: the style cycle
        """
        self.obj.set_prop_cycle(**props)

    def get_frame_visible(self):
        """
        **LLM Docstring**

        Return which frame (spine) edges are drawn (matplotlib backend).

        :return: the result
        """
        return (
            (
                self.obj.spines['left'].get_visible(),
                self.obj.spines['right'].get_visible()
            ),
            (
                self.obj.spines['bottom'].get_visible(),
                self.obj.spines['top'].get_visible()
            ),
        )
    def set_frame_visible(self, frame_spec):
        """
        **LLM Docstring**

        Set which frame (spine) edges are drawn (matplotlib backend).

        :param frame_spec: the per-edge visibility spec
        """
        if frame_spec is True or frame_spec is False:
            self.obj.set_frame_on(frame_spec)
        else:
            lr, bt = frame_spec
            if lr is None:
                l = r = None
            elif lr is True or lr is False:
                l = r = lr
            else:
                l,r = lr
            if bt is True or bt is False:
                b = t = bt
            else:
                b,t = bt
            for k,v in [
                ['left', l],
                ['right', r],
                ['bottom', b],
                ['top', t]
            ]:
                if v is not None: self.obj.spines[k].set_visible(v)

    def get_frame_style(self):
        """
        **LLM Docstring**

        Return the frame (spine) styling (matplotlib backend).

        :return: the result
        """
        return (
            (
                self.obj.spines['left'].get(),
                self.obj.spines['right'].get()
            ),
            (
                self.obj.spines['bottom'].get(),
                self.obj.spines['top'].get()
            ),
        )
    def set_frame_style(self, frame_spec):
        """
        **LLM Docstring**

        Set the frame (spine) styling (matplotlib backend).

        :param frame_spec: the frame styling
        """
        if isinstance(frame_spec, dict):
            l, r, b, t = frame_spec
        else:
            lr, bt = frame_spec
            if lr is None:
                l = r = None
            elif lr is True or lr is False:
                l = r = lr
            else:
                l,r = lr
            if bt is True or bt is False:
                b = t = bt
            else:
                b,t = bt
        for k,v in [
            ['left', l],
            ['right', r],
            ['bottom', b],
            ['top', t]
        ]:
            if v is not None: self.obj.spines[k].set(**v)

    def get_grid_visible(self):
        x, y = (
            self.xaxis.get_tick_params()["gridOn"],
            self.yaxis.get_tick_params()["gridOn"]
        )
        if x and y:
            return True
        elif (not x) and (not y):
            return False
        else:
            return (x, y)
    def set_grid_visible(self, grid_spec):
        if grid_spec is True:
            self.obj.grid(True)
        elif grid_spec is False:
            self.obj.grid(False)
        else:
            x, y = grid_spec
            if x:
                self.obj.grid(True, axis='x')
            if y:
                self.obj.grid(True, axis='y')
    def get_grid_style(self):
        import matplotlib.pyplot as plt
        styles = {}
        for k,v in plt.rcParams.items():
            if k.startswith('grid.'):
                styles[k[5:]] = v
        return styles
    def set_grid_style(self, grid_spec):
        if dev.is_dict_like(grid_spec):
            self.obj.grid(True, **grid_spec)
        else:
            x, y = grid_spec
            if dev.is_dict_like(x):
                self.obj.grid(axis='x', **x)
            if y:
                self.obj.grid(axis='y', **y)

    def get_xlabel(self):
        """
        **LLM Docstring**

        Return the x-axis label (matplotlib backend).

        :return: the result
        """
        return self.obj.get_xlabel()
    def set_xlabel(self, val, **style):
        """
        **LLM Docstring**

        Set the x-axis label (matplotlib backend).

        :param val: the label text
        :param style: label styling options
        """
        self.obj.set_xlabel(val, **style)
    def get_ylabel(self):
        """
        **LLM Docstring**

        Return the y-axis label (matplotlib backend).

        :return: the result
        """
        return self.obj.get_ylabel()
    def set_ylabel(self, val, **style):
        """
        **LLM Docstring**

        Set the y-axis label (matplotlib backend).

        :param val: the label text
        :param style: label styling options
        """
        self.obj.set_ylabel(val, **style)

    def get_xlim(self):
        """
        **LLM Docstring**

        Return the x-axis limits (matplotlib backend).

        :return: the result
        """
        return self.obj.get_xlim()
    def set_xlim(self, val, **opts):
        """
        **LLM Docstring**

        Set the x-axis limits (matplotlib backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        self.obj.set_xlim(val, **opts)
    def get_ylim(self):
        """
        **LLM Docstring**

        Return the y-axis limits (matplotlib backend).

        :return: the result
        """
        return self.obj.get_ylim()
    def set_ylim(self, val, **opts):
        """
        **LLM Docstring**

        Set the y-axis limits (matplotlib backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        self.obj.set_ylim(val, **opts)

    def get_xticks(self):
        """
        **LLM Docstring**

        Return the x-axis tick locations (matplotlib backend).

        :return: the result
        """
        return self.obj.get_xticks()
    def set_xticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the x-axis tick locations (matplotlib backend).

        :param val: the tick locations
        :param opts: extra options
        """
        self.obj.set_xticks(val, **opts)

    def get_yticks(self):
        """
        **LLM Docstring**

        Return the y-axis tick locations (matplotlib backend).

        :return: the result
        """
        return self.obj.get_yticks()
    def set_yticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the y-axis tick locations (matplotlib backend).

        :param val: the tick locations
        :param opts: extra options
        """
        self.obj.set_yticks(val, **opts)

    def get_xtick_style(self):
        """
        **LLM Docstring**

        Return the x-axis tick styling (matplotlib backend).

        :return: the result
        """
        return self.obj.tick_params(axis='x')
    def set_xtick_style(self, **opts):
        """
        **LLM Docstring**

        Set the x-axis tick styling (matplotlib backend).

        :param opts: extra options
        """
        return self.obj.tick_params(axis='x', **opts)
    def get_ytick_style(self):
        """
        **LLM Docstring**

        Return the y-axis tick styling (matplotlib backend).

        :return: the result
        """
        return self.obj.tick_params(axis='y')
    def set_ytick_style(self, **opts):
        """
        **LLM Docstring**

        Set the y-axis tick styling (matplotlib backend).

        :param opts: extra options
        """
        return self.obj.tick_params(axis='y', **opts)

    def set_aspect_ratio(self, ar):
        """
        **LLM Docstring**

        Set the axes aspect ratio (matplotlib backend).

        :param ar: the aspect ratio
        """
        if nput.is_numeric(ar):
            a, b = self.get_xlim(), self.get_ylim()
            if a is not None and b is not None:
                cur_ar = abs(b[1] - b[0]) / abs(a[1] - a[0])
                ar = ar / cur_ar
        self.obj.set_aspect(ar)

    def get_bbox(self):
        """
        **LLM Docstring**

        Return the axes bounding box (matplotlib backend).

        :return: the result
        """
        bbox = self.obj.get_position()
        if hasattr(bbox, 'get_points'):
            bbox = bbox.get_points()
        bbox = [
            [b*DPI_SCALING for b in bb]
            for bb in bbox
        ]

        return bbox
    def set_bbox(self, bbox):
        """
        **LLM Docstring**

        Set the axes bounding box (matplotlib backend).

        :param bbox: the bounding box
        """
        if hasattr(bbox, 'get_points'):
            bbox = bbox.get_points()
        else:
            bbox = [
                [b / DPI_SCALING for b in bb]
                for bb in bbox
            ]
        ((lx, by), (rx, ty)) = bbox
        self.obj.set_position([lx, by, rx-lx, ty-by])

    def get_facecolor(self):
        """
        **LLM Docstring**

        Return the background/face color (matplotlib backend).

        :return: the result
        """
        return self.obj.get_facecolor()
    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color (matplotlib backend).

        :param fg: the face color
        """
        if isinstance(fg, str) and fg == 'transparent':
            fg = 'none'
        return self.obj.set_facecolor(fg)

    def get_padding(self):
        """
        **LLM Docstring**

        Return the axes padding (matplotlib backend).

        :return: the result
        """
        padding = [
            ['left', 'right'],
            ['bottom', 'top']
        ]
        xlab_padding = None
        ylab_padding = None
        for i, l in enumerate(padding):
            for j, key in enumerate(l):
                spine = self.obj.spines[key]
                viz = spine.get_visible()
                if viz:
                    ((l, b), (r, t)) = bbox = spine.get_window_extent().get_points()
                    if i == 0:
                        base_pad = r - l
                        if xlab_padding is None:
                            xlabs = self.obj.get_xticklabels()
                            if len(xlabs) > 0:
                                min_x = 1e10
                                max_x = -1e10
                                for lab in xlabs:
                                    ((l, b), (r, t)) = lab.get_window_extent().get_points()
                                    min_x = min(l, min_x)
                                    max_x = max(r, max_x)
                                xlab_padding = max_x - min_x
                            else:
                                xlab_padding = 0
                        padding[i][j] = base_pad + xlab_padding
                    else:
                        base_pad = t - b
                        if ylab_padding is None:
                            ylabs = self.obj.get_yticklabels()
                            if len(ylabs) > 0:
                                min_y = 1e10
                                max_y = -1e10
                                for lab in ylabs:
                                    ((l, b), (r, t)) = lab.get_window_extent().get_points()
                                    min_y = min(b, min_y)
                                    max_y = max(t, max_y)
                                ylab_padding = max_y - min_y
                            else:
                                ylab_padding = 0
                        padding[i][j] = base_pad + ylab_padding
                else:
                    padding[i][j] = 0
        return padding

    def legend(self, **opts):
        """
        **LLM Docstring**

        Draw the axes legend (matplotlib backend).

        :param opts: legend options
        :return: the result
        """
        return self.get_plotter('legend')(**opts)

    def get_graphics_properties(self, obj, property=None):
        """
        **LLM Docstring**

        Get backend properties of a drawn graphics object (matplotlib backend).

        :param obj: the graphics object
        :param property: a specific property to fetch
        :return: the result
        """
        from matplotlib.artist import getp

        return getp(obj, property=property)
    def set_graphics_properties(self, obj, **props):
        """
        **LLM Docstring**

        Set backend properties on a drawn graphics object (matplotlib backend).

        :param obj: the graphics object
        :param props: the properties to set
        """
        from matplotlib.artist import setp

        return setp(obj, **props)

    def draw_line(self, points, **styles):
        """
        **LLM Docstring**

        Draw a line/polyline through the given points (matplotlib backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        points = np.asanyarray(points)
        if points.ndim == 2:
            points = points[np.newaxis]
        return self.get_plotter('plot')(
            points[:, 0],
            points[:, 1],
            **styles
        )

    def draw_disk(self, points, radius=None, s=None, **styles):
        """
        **LLM Docstring**

        Draw a filled disk at the given position(s) (matplotlib backend).

        :param points: the points to draw
        :param radius: the `radius`
        :param s: the `s`
        :param styles: the styling options
        """
        points = np.asanyarray(points)
        if points.ndim == 1:
            points = points[np.newaxis]
        if radius is not None and s is None:
            s = radius * 100
        return self.get_plotter('scatter')(
            points[:, 0],
            points[:, 1],
            **styles
        )

    def draw_rect(self, points, **styles):
        """
        **LLM Docstring**

        Draw a rectangle from the given points (matplotlib backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        patches = MPLManager.patch_api()
        coll = MPLManager.collections_api()
        points = np.asanyarray(points)
        if points.ndim == 2:
            points = points[np.newaxis]

        anchors = points[:, 0]
        widths = points[:, 1, 0] - points[:, 0, 0]
        heights = points[:, 1, 1] - points[:, 0, 1]

        rects = coll.PatchCollection([
            patches.Rectangle(a, w, h, **styles)
            for a,w,h in zip(anchors, widths, heights)
        ])

        self.obj.add_patch(rects)

    def draw_poly(self, points, **styles):
        """
        **LLM Docstring**

        Draw a filled polygon from the given points (matplotlib backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        patches = MPLManager.patch_api()
        coll = MPLManager.collections_api()
        points = np.asanyarray(points)
        if points.ndim == 2:
            points = points[np.newaxis]

        polys = coll.PatchCollection([
            patches.Polygon(pt, **styles) for pt in points
        ])

        self.obj.add_patch(polys)

    def draw_arrow(self, points, **styles):
        """
        **LLM Docstring**

        Draw an arrow from the given points (matplotlib backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        points = np.asanyarray(points)
        if points.ndim == 2:
            points = points[np.newaxis]
        return self.get_plotter('arrow')(
            *points[0],
            *(points[1] - points[0]),
            **styles
        )

    def draw_text(self, points, vals, **styles):
        """
        **LLM Docstring**

        Draw text at the given position(s) (matplotlib backend).

        :param points: the points to draw
        :param vals: the text string(s)
        :param styles: the styling options
        """
        points = np.asanyarray(points)
        if points.ndim == 1:
            points = points[np.newaxis]
        if isinstance(vals, str):
            vals = [vals]

        text_plotter = self.get_plotter('text')
        styles = {
            o.partition("_")[-1] if o.startswith('font_') else o:v
            for o,v in styles.items()
        }
        text = [
             text_plotter(*pt, txt, **styles)
             for pt, txt in zip(points, vals)
        ]

        return text

    @classmethod
    def svg_to_mpl_path(cls,
                        path,
                        target_bbox=None,
                        base_height=None,
                        y_flip: bool = False):
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
        from matplotlib.path import Path
        _CMD_MAP = {
            "M": Path.MOVETO,
            "L": Path.LINETO,
            "Q": Path.CURVE3,  # quadratic Bézier
            "C": Path.CURVE4,  # cubic Bézier
            "Z": Path.CLOSEPOLY
        }

        point_lists = []
        codes = []
        start = np.zeros(2)
        cur = np.zeros(2)
        for command, args in path:
            command:str
            accumulate = False
            if command in "Aa":
                rel = command.islower()
                if rel:
                    command = "l"
                else:
                    command = "L"
                rx, ry, phi_deg, large, sweep, x2, y2 = args
                args = nput.arc_points_from_endpoints(
                    [0, 0] if rel else cur,
                    end=[x2, y2] if rel else cur + np.array([x2, y2]),
                    radius=[rx, ry],
                    rotation=np.deg2rad(phi_deg),
                    use_major_rotation=large,
                    clockwise=sweep
                )
            elif command == 'l':
                accumulate = True
            code = _CMD_MAP[command.upper()]
            rel = command.islower()
            args = np.asanyarray(args).reshape(-1, 2)
            if accumulate:
                args = np.cumsum(args, axis=0)
            if code == Path.CLOSEPOLY:
                cur = start
                args = [[-1, -1]]
            else:
                if rel:
                    args = args + cur[np.newaxis]
                if code == Path.MOVETO:
                    cur = args[0]
                else:
                    cur = args[-1]
                print(cur)
                point_lists.append(args)
            codes.extend([code] * len(args))

        verts = np.concatenate(point_lists, dtype=float, axis=0)
        # TODO: use proper SVG extrema code
        bbox_init = (
            (np.min(verts[:, 0]), np.max(verts[:, 0])),
            (np.min(verts[:, 1]), np.max(verts[:, 1]))
        )
        dims_init = (
            bbox_init[0][1] - bbox_init[0][0],
            bbox_init[1][1] - bbox_init[1][0],
        )
        if y_flip:
            h = dims_init[1] if base_height is None else base_height
            verts = verts.copy()
            verts[:, 1] = h - verts[:, 1]

        if target_bbox is None:
            target_bbox = bbox_init
        dims_target = (
            target_bbox[0][1] - target_bbox[0][0],
            target_bbox[1][1] - target_bbox[1][0],
        )
        scaling = max(np.array(dims_target) / np.array(dims_init))

        verts = (
                (verts - np.array([[bbox_init[0][0], bbox_init[1][0]]])) * scaling
                + np.array([[target_bbox[0][0], target_bbox[1][0]]])
        )

        return Path(verts, codes)

    def _adjust_limits(self,
                       xmin: float, xmax: float,
                       ymin: float, ymax: float,
                       pad: float = 0.05,
                       ) -> None:
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
        ax = self.obj
        cur_xl = ax.get_xlim()
        cur_yl = ax.get_ylim()
        autoscaling = ax.get_autoscale_on()

        if autoscaling:
            # No data yet — start from the path's own bounds
            new_xmin, new_xmax = xmin, xmax
            new_ymin, new_ymax = ymin, ymax
        else:
            new_xmin = min(cur_xl[0], xmin)
            new_xmax = max(cur_xl[1], xmax)
            new_ymin = min(cur_yl[0], ymin)
            new_ymax = max(cur_yl[1], ymax)

        # Apply symmetric fractional padding
        xspan = new_xmax - new_xmin or 1.0  # guard against zero-width
        yspan = new_ymax - new_ymin or 1.0
        ax.set_xlim(new_xmin - pad * xspan, new_xmax + pad * xspan)
        ax.set_ylim(new_ymin - pad * yspan, new_ymax + pad * yspan)
        ax.set_autoscale_on(False)  # freeze after first path is added
    def draw_path(self, commands, **styles):
        """
        **LLM Docstring**

        Draw a path from a sequence of drawing commands (matplotlib backend).

        :param commands: the path drawing commands
        :param styles: the styling options
        """
        patches = MPLManager.patch_api()
        path = self.svg_to_mpl_path(commands)
        path = patches.PathPatch(path, **styles)
        bbox = path.get_extents()
        self._adjust_limits(
            bbox.x0, bbox.x1,
            bbox.y0, bbox.y1
        )
        self.obj.add_patch(path)
        return path

class MPLAxes3D(MPLAxes):
    def __init__(self, mpl_axes_object, **opts):
        """
        **LLM Docstring**

        Wrap a matplotlib 3D `Axes`, exposing the z-axis and installing the custom draw
        monkeypatch used to control 3D z-ordering.

        :param mpl_axes_object: the backing matplotlib 3D axes
        :param opts: canonicalized axes options
        """
        super().__init__(mpl_axes_object, **opts)
        self.zaxis = self.obj.zaxis
        self.computed_zorder = self.obj.computed_zorder
        self._monkeypatch_draw(self.obj)
        self._dist = None
        self._view_scaling = 1

    def set_projection_type(self, proj_type, **kwargs):
        """
        **LLM Docstring**

        Set the 3D projection type (matplotlib backend).

        :param proj_type: the projection type
        :param kwargs: extra keyword options
        """
        if proj_type is not None:
            return self.obj.set_proj_type(proj_type, **kwargs)
    def get_projection_type(self):
        """
        **LLM Docstring**

        Return the 3D projection type (matplotlib backend).

        :return: the result
        """
        return self.obj.get_proj_type()

    def get_autoscale(self):
        """
        **LLM Docstring**

        Return the autoscale setting (matplotlib backend).

        :return: the result
        """
        return self.obj.autoscale()
    def set_autoscale(self, autoscale):
        """
        **LLM Docstring**

        Set the autoscale setting (matplotlib backend).

        :param autoscale: the autoscale setting
        """
        return self.obj.autoscale(autoscale)

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
        from mpl_toolkits.mplot3d import proj3d
        try:
            dist = artist.do_3d_projection()
        except AttributeError:
            if hasattr(artist, '_verts3d'):
                # if artist.axes.M is not None:
                xs, ys, zs, vis = proj3d._proj_transform_clip(*artist._verts3d, artist.axes.M,
                                                              artist.axes._focal_length)
                dist = np.min(zs)
                # else:
                #     dist = np.min(artist._verts3d[-1])
            else:
                dist = 1000000
        if hasattr(artist, 'zdist_offset'):
            offset = artist.zdist_offset
            if callable(offset):
                offset = offset(artist)
            dist += offset
        return dist

    @classmethod
    def _artist_predraw(cls, obj, dist):
        """
        **LLM Docstring**

        Call an artist's `predraw` hook (if any) with its computed depth, before drawing.

        :param obj: the artist
        :param dist: the artist's depth
        """
        if hasattr(obj, 'predraw'):
            obj.predraw(dist)

    zdir_map = {
        'x':[1, 0, 0],
        'y':[0, 1, 0],
        'z':[0, 0, 1],
    }
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
        #https://stackoverflow.com/a/76151563/5720002
        zn = nput.vec_normalize(cls.zdir_map[zdir] if isinstance(zdir, str) else zdir)

        cos_angle = zn[2]
        sin_angle = np.linalg.norm(zn[:2])
        if sin_angle == 0:
            return np.sign(cos_angle) * np.eye(3)

        d = np.array((zn[1], -zn[0], 0))
        d /= sin_angle
        ddt = np.outer(d, d)
        skew = np.array([[0, 0, -d[1]], [0, 0, d[0]], [d[1], -d[0], 0]], dtype=np.float64)
        return ddt + cos_angle * (np.eye(3) - ddt) + sin_angle * skew

    @classmethod
    def _set_patch_3d_properties(cls, self, verts, zs, zdir="z", axlim_clip=None):
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
        zs = np.broadcast_to(zs, len(verts))
        self._axlim_clip = axlim_clip
        self._segment3d = np.asarray(
            [
                np.dot(cls._transform_zdir(zdir), (x, y, 0)) + (0, 0, z)
                for ((x, y), z) in zip(verts, zs)
            ]
        )

    @classmethod
    def _set_pathpatch_3d_properties(cls, self, path, zs, zdir="z", axlim_clip=None):
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
        cls._set_patch_3d_properties(self, path.vertices, zs, zdir=zdir, axlim_clip=axlim_clip)
        self._code3d = path.codes

    @classmethod
    def _pathpatch_translate(cls, pathpatch, delta):
        """
        **LLM Docstring**

        Translate a 3D-lifted patch by a delta in its 3D segment coordinates.

        :param pathpatch: the patch
        :param delta: the translation
        """
        pathpatch._segment3d += np.asarray(delta)

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
        import mpl_toolkits.mplot3d.art3d as art3d
        from mpl_toolkits.mplot3d import proj3d
        mpath = MPLManager().path_api()

        s = self._segment3d
        if self._axlim_clip:
            xs, ys, zs = art3d._viewlim_mask(*zip(*s), self.axes)
        else:
            xs, ys, zs = zip(*s)
        vxs, vys, vzs, vis = proj3d._proj_transform_clip(xs, ys, zs,
                                                         self.axes.M,
                                                         self.axes._focal_length)
        self._path2d = mpath.Path(np.ma.column_stack([vxs, vys]))

        if mode is None:
            mode = self.distance_mode

        return mode(vzs)

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
        import mpl_toolkits.mplot3d.art3d as art3d
        from mpl_toolkits.mplot3d import proj3d
        mpath = MPLManager().path_api()

        s = self._segment3d
        if self._axlim_clip:
            xs, ys, zs = art3d._viewlim_mask(*zip(*s), self.axes)
        else:
            xs, ys, zs = zip(*s)
        vxs, vys, vzs, vis = proj3d._proj_transform_clip(xs, ys, zs,
                                                         self.axes.M,
                                                         self.axes._focal_length)
        self._path2d = mpath.Path(np.ma.column_stack([vxs, vys]), self._code3d)

        if mode is None:
            mode = self.distance_mode

        return mode(vzs)

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
        # import mpl_toolkits.mplot3d.art3d as art3d
        from mpl_toolkits.mplot3d import proj3d
        try:
            verts = self._og_verts
        except AttributeError:
            verts = self._og_verts = self._verts3d
        vxs, vys, vzs, vis = proj3d._proj_transform_clip(*verts,
                                                         self.axes.M,
                                                         self.axes._focal_length)
        # self._verts3d = (vxs, vys, vzs)

        if mode is None:
            mode = self.distance_mode

        return mode(vzs)

    def _monkeypatch_patch(self, patch, pos, zdir="z", zorder_mode=None):
        """
        **LLM Docstring**

        Attach the custom 3D-projection machinery to a 2D patch, lifting it into 3D at a
        position and assigning its z-order distance mode.

        :param patch: the matplotlib patch
        :param pos: the 3D position to place it at
        :param zdir: the plane normal direction
        :param zorder_mode: the depth-reduction mode for z-ordering
        """
        import mpl_toolkits.mplot3d.art3d as art3d
        import matplotlib.patches as patches
        if isinstance(patch, patches.PathPatch):
            patch.set_3d_properties = functools.partial(self._set_pathpatch_3d_properties, patch)
            patch.translate = functools.partial(self._pathpatch_translate, patch)
            art3d.pathpatch_2d_to_3d(patch, z=0, zdir=zdir)
            patch.do_3d_projection =  functools.partial(self._patch_do_3d_projection, patch)
        else:
            patch.set_3d_properties = functools.partial(self._set_patch_3d_properties, patch)
            patch.translate = functools.partial(self._pathpatch_translate, patch)
            art3d.patch_2d_to_3d(patch, z=0, zdir=zdir)
            patch.do_3d_projection =  functools.partial(self._pathpatch_do_3d_projection, patch)
        patch.translate(pos)

        if zorder_mode is None:
            zorder_mode = np.min
        patch.distance_mode = zorder_mode

    def _monkeypatch_draw(self, obj):
        """
        **LLM Docstring**

        Replace a 3D axes' `draw` method with one that manually depth-sorts the child
        artists (and rescales the box aspect by camera distance) before drawing, giving
        correct z-ordering.

        :param obj: the matplotlib 3D axes
        """
        cur_draw = obj.draw
        obj.computed_zorder = False

        @functools.wraps(obj.draw)
        def draw(renderer):
            """
            **LLM Docstring**

            The replacement draw routine: depth-sort the visible artists, run their predraw
            hooks, then draw.

            :param renderer: the matplotlib renderer
            """
            from mpl_toolkits.mplot3d import proj3d
            if self._dist is not None:
                obj.set_box_aspect(obj.get_box_aspect(), zoom=(1.8294640721620434 * 25/24) / (self._dist / 10)) # magic number from MPL)
            if self.computed_zorder:
                obj.M = obj.get_proj()
                obj.invM = np.linalg.inv(obj.M)
                zorder_offset = max(axis.get_zorder()
                                    for axis in obj._axis_map.values()) + 1
                artists = [
                    artist for artist in self.obj._children
                    if artist.get_visible() and artist.zorder > 0
                ]
                mean_point = proj3d.proj_transform([0], [0], [0], obj.M)
                dists = [
                    self._get_dist(artist) - mean_point[-1][0]
                    for artist in artists
                ]
                for artist, dist in sorted(zip(artists, dists),
                                     key=lambda ad: ad[1],
                                     reverse=True):
                    artist.zorder = zorder_offset + 1
                    self._artist_predraw(artist, dist)
                    zorder_offset += 1

                # print(self.get_xlim(), self.get_ylim(), self.get_zlim())
                # print(self.get_box_aspect())

            cur_draw(renderer)

        obj.draw = draw

    def set_frame_visible(self, frame_spec):
        """
        **LLM Docstring**

        Set which frame (spine) edges are drawn (matplotlib backend).

        :param frame_spec: the per-edge visibility spec
        """
        if frame_spec is True:
            self.obj.set_axis_on()
        elif frame_spec is False:
            self.obj.set_axis_off()

    def get_zlabel(self):
        """
        **LLM Docstring**

        Return the z-axis label (matplotlib backend).

        :return: the result
        """
        return self.obj.get_zlabel()
    def set_zlabel(self, val, **style):
        """
        **LLM Docstring**

        Set the z-axis label (matplotlib backend).

        :param val: the label text
        :param style: label styling options
        """
        self.obj.set_zlabel(val, **style)


    def get_zlim(self):
        """
        **LLM Docstring**

        Return the z-axis limits (matplotlib backend).

        :return: the result
        """
        return self.obj.get_zlim()
    def set_zlim(self, val, **opts):
        """
        **LLM Docstring**

        Set the z-axis limits (matplotlib backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        self.obj.set_zlim(val, **opts)

    def get_zticks(self):
        """
        **LLM Docstring**

        Return the z-axis tick locations (matplotlib backend).

        :return: the result
        """
        return self.obj.get_zticks()
    def set_zticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the z-axis tick locations (matplotlib backend).

        :param val: the tick locations
        :param opts: extra options
        """
        self.obj.set_zticks(val, **opts)

    def get_ztick_style(self):
        """
        **LLM Docstring**

        Return the z-axis tick styling (matplotlib backend).

        :return: the result
        """
        return self.obj.tick_params(axis='z')
    def set_ztick_style(self, **opts):
        """
        **LLM Docstring**

        Set the z-axis tick styling (matplotlib backend).

        :param opts: extra options
        """
        return self.obj.tick_params(axis='z', **opts)

    def get_box_aspect(self):
        """
        **LLM Docstring**

        Return the 3D box aspect ratios (matplotlib backend).

        :return: the result
        """
        return self.obj.get_box_aspect()
    def set_box_aspect(self, br, **kwargs):
        """
        **LLM Docstring**

        Set the 3D box aspect ratios (matplotlib backend).

        :param br: the box aspect ratios
        :param kwargs: extra keyword options
        """
        return self.obj.set_box_aspect(br, **kwargs)

    def get_view_settings(self):
        """
        **LLM Docstring**

        Return the 3D camera/view settings (matplotlib backend).

        :return: the result
        """
        return {'elev': self.obj.elev, 'azim':self.obj.azim,
                'roll':self.obj.roll, 'vertical_axis':self.obj.vertical_axis,
                'dist':self.obj.dist}
    def set_view_settings(self,
                          elev=None, azim=None, roll=None, vertical_axis=None, dist=None,
                          up_vector=None, right_vector=None, view_vector=None, view_distance=None,
                          view_matrix=None,
                          **values):
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
        if view_matrix is None and (
                view_vector is not None
                or right_vector is not None
                or up_vector is not None
        ):
            if view_vector is None:
                if (
                        up_vector is not None and right_vector is not None
                ):
                    view_vector = nput.vec_crosses(up_vector, right_vector, normalize=True)
                elif right_vector is not None:
                    view_vector = nput.vec_crosses(self.default_up_vector, right_vector, normalize=True)
                elif up_vector is not None:
                    view_vector = nput.vec_crosses(up_vector, self.default_right_vector, normalize=True)

            if view_vector is not None:
                m = nput.rotation_matrix(
                    view_vector,
                    self.default_view_vector
                )
            else:
                m = np.eye(3)

            if up_vector is None and right_vector is not None:
                if view_vector is None:
                    view_vector = self.default_view_vector
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
                    self.default_up_vector
                )
            view_matrix = m

        if view_matrix is not None:
            if vertical_axis is None:
                target_vertical = [0, 1, 0]
                target_view = [0, 0, 1]
            else:
                target_vertical = [
                    [1, 0, 0]
                        if vertical_axis == 'x' else
                    [0, 1, 0]
                        if vertical_axis == 'y' else
                    [0, 0, 1]
                ]
                target_view = [
                    [0, 0, 1]
                        if vertical_axis == 'x' else
                    [0, 1, 0]
                        if vertical_axis == 'y' else
                    [1, 0, 0]
                ]

            # v1 = R(azim, z) . x
            # n = z x v1
            # v = R(elev, n) . v1
            view_vector, right_vector, up_vector = view_matrix.T
            elev = np.arctan2(view_vector[-1], np.linalg.norm(view_vector[:2]))
            azim = np.arctan2(view_vector[1], view_vector[0])
            roll = nput.vec_angles(target_vertical, up_vector,
                                   up_vectors=view_vector,
                                   return_crosses=False)

            elev = np.rad2deg(elev)
            azim = np.rad2deg(azim)
            roll = np.rad2deg(roll)

            if view_distance is not None:
                v_box = np.array([self.get_xlim(), self.get_ylim(), self.get_zlim()]).T @ view_matrix
                default_view_distance =  np.max(np.abs(v_box[1][:2] - v_box[0][:2]))
                scaling = view_distance / default_view_distance
                dist = 10 * scaling
            elif dist is not None:
                scaling = dist / 10
            else:
                scaling = 1
        elif view_distance is not None:
            v_box = np.array([self.get_xlim(), self.get_ylim(), self.get_zlim()]).T
            default_view_distance =  np.max(np.abs(v_box[1][:2] - v_box[0][:2]))
            scaling = view_distance / default_view_distance
            dist = 10 * scaling
        elif dist is not None:
            scaling = dist / 10
        else:
            scaling = 1
            # roll = np.rad2deg(nput.vec_angles([1, 0, 0], view_vector, return_crosses=False))
            # elev = nput.vec_angles([1, 0, 0], view_vector, return_crosses=False)

        values = values | {
            k:v for k,v in
            dict(elev=elev, azim=azim, roll=roll, vertical_axis=vertical_axis).items()
            if v is not None
        }
        self.obj.view_init(**values)
        self._view_scaling = 1 / scaling
        if dist is not None:
            self._dist = dist
            self.obj.dist = dist
            # self.obj.set_box_aspect(None, zoom=(1.8294640721620434 * 25/24) / (dist / 10)) # magic number from MPL

    def prep_show(self):
        """
        **LLM Docstring**

        Prepare the axes/figure for display (matplotlib backend).

        """
        if self._dist is not None:
            self.obj.dist = self._dist

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
        try:
            cur_aspect = sphere_path.axes._og_lims
        except AttributeError:
            cur_aspect = sphere_path.axes._og_lims = (
                sphere_path.axes.get_xlim3d(),
                sphere_path.axes.get_ylim3d(),
                sphere_path.axes.get_zlim3d()
            )
        size_rescaling = np.max([
                (B-b) / (A-a)
                for (a,A), (b,B) in zip(
                (
                    sphere_path.axes.get_xlim3d(),
                    sphere_path.axes.get_ylim3d(),
                    sphere_path.axes.get_zlim3d()
                ), cur_aspect
            )
        ])
        return size_rescaling

    @classmethod
    def _flat_sphere_predraw(cls, sphere_path, dist, *,
                             depth_shading_range, depth_shading_targets,
                             depth_shrink_range, depth_shrink_targets,
                             radius=None
                             ):
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
        if depth_shading_range is not None and depth_shading_targets is not None:
            perc = nput.vec_rescale(dist, depth_shading_targets, cur_range=depth_shading_range, clip=True)
            try:
                cur_fc = sphere_path._og_facecolors
            except AttributeError:
                cur_fc = sphere_path._og_facecolors = np.asanyarray(sphere_path.get_facecolors())
            new_fc = ColorPalette.color_lighten(cur_fc[:, :3].T * 255, -perc, shift=True, modification_space='lab') / 255
            sphere_path.set_facecolors(np.concatenate([new_fc.T, cur_fc[:, (3,)]], axis=1))
        else:
            perc = None

        if depth_shrink_range is not None or depth_shrink_targets is not None:
            if depth_shrink_range is None:
                depth_shrink_range = depth_shading_range
            elif depth_shrink_targets is None:
                depth_shrink_targets = depth_shading_targets
            if depth_shrink_range is not None and depth_shrink_targets is not None:
                perc = nput.vec_rescale(dist, depth_shrink_targets, cur_range=depth_shrink_range, clip=True)
            else:
                perc = None

        try:
            cur_size = sphere_path._og_sizes
        except AttributeError:
            cur_size = sphere_path._og_sizes = np.asanyarray(sphere_path.get_sizes())
        sphere_path.set_sizes((cls._get_axis_scaling(sphere_path)**2) * cur_size)

        if perc is not None:
            cur_size = np.asanyarray(sphere_path.get_sizes())
            new_size = ((1 - perc)**2) * cur_size
            sphere_path.set_sizes(new_size)

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
        # from mpl_toolkits.mplot3d import proj3d
        # xyzs_list = proj3d.proj_transform([0], [0], [radius], artist.axes.M)
        # base_shift = np.linalg.norm([xyzs_list[0], xyzs_list[1], xyzs_list[2]])
        return -radius / 10 #1.5 * (radius / base_shift) # account for distortion due to projection
    def draw_sphere(self, center, radius, sphere_points=48, rendering='standard',
                    s=None,
                    box_scalings=None,
                    edgecolors=None,
                    edge_color=None,
                    lw=None,
                    edge_width=.01,
                    glow=None,
                    color='white',
                    plotter='scatter',
                    depth_shading_range=(-1, 1),
                    depth_shading_targets=(-.5, .5),
                    depth_shrink_range=None,
                    depth_shrink_targets=None,
                    **opts):
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
        if dev.str_is(rendering, 'flat'):

            if glow is not None:
                if color is None:
                    color = glow
                else:
                    color = ColorPalette.prep_color(palette=[glow, color], blending=.5)

            center = np.asanyarray(center)
            if center.ndim == 1:
                center = center[np.newaxis]
            if edgecolors is None:
                if edge_color is not None:
                    edgecolors = edge_color
                else:
                    edgecolors = [[0.] * 3 + [.3]]
            if isinstance(edgecolors, str) or nput.is_numeric(edgecolors[0]):
                edgecolors = [edgecolors] * len(center)
            if isinstance(color, str) or nput.is_numeric(color[0]):
                color = [color] * len(center)
            if box_scalings is None:
                box_scalings = [1, 1, 1]
            if box_scalings is not None:
                box_scalings = np.array(box_scalings) * self._view_scaling
            if s is None:
                s = (radius * max(box_scalings) * 72)**2 * np.pi
            if lw is None:
                lw = (edge_width * max(box_scalings) * 72)

            if nput.is_numeric(s):
                s = [s] * len(center)
            areas = s
            if plotter == 'plot':
                surface = self.get_plotter('plot')
                spheres = []
                s = np.sqrt(s)
                for x,s,c,ec,w in zip(center, s, color, edgecolors, lw):
                    spheres.append(
                        surface([x[0], x[0]], [x[1], x[1]], [x[2], x[2]],
                                   markersize=s,
                                   marker='o',
                                   linestyle='',
                                   markerfacecolor=c,
                                   markeredgecolor=ec,
                                   markerlw=w,
                                   **opts)
                    )
                dists = (np.sqrt(areas) / (max(box_scalings) * 72)) / 10
                for s, r in zip(spheres, dists):
                    # s.zdist_offset = functools.partial(self._get_sphere_proj, radius=r)
                    s.predraw = functools.partial(self._flat_sphere_predraw, s,
                                                  radius=r * 10,
                                                  depth_shading_range=depth_shading_range,
                                                  depth_shading_targets=depth_shading_targets,
                                                  depth_shrink_range=depth_shrink_range,
                                                  depth_shrink_targets=depth_shrink_targets)
            else:
                spheres = self.get_plotter('scatter')(
                    center[:, 0], center[:, 1], center[:, 2],
                    edgecolors=edgecolors,
                    color=color,
                    s=s,
                    lw=lw,
                    **opts
                )
                dists = (np.sqrt(areas) / (max(box_scalings) * 72)) / 10
                # spheres.zdist_offset = functools.partial(self._get_sphere_proj, radius=np.max(dists))
                spheres.predraw = functools.partial(self._flat_sphere_predraw,
                                                    spheres,
                                                    radius=dists * 10,
                                                    depth_shading_range=depth_shading_range,
                                                    depth_shading_targets=depth_shading_targets,
                                                    depth_shrink_range=depth_shrink_range,
                                                    depth_shrink_targets=depth_shrink_targets)
            return spheres
        else:
            surface = self.get_plotter('plot_surface')

            u = np.linspace(0, 2 * np.pi, sphere_points)
            v = np.linspace(0, np.pi, sphere_points)
            x = radius * np.outer(np.cos(u), np.sin(v))
            y = radius * np.outer(np.sin(u), np.sin(v))
            z = radius * np.outer(np.ones(np.size(u)), np.cos(v))

            return surface(x + center[0], y + center[1], z + center[2], color=color, **opts)

    # @classmethod
    # def _load_patch_line(cls):
    #     mpl_toolkits.mplot3d.art3d
    #     fr
    #     class PatchLine()
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
        from mpl_toolkits.mplot3d import proj3d
        x,y,z = artist._verts3d
        xyzs_list = proj3d.proj_transform(x,y,z, artist.axes.M)
        base_shift = 1.5 * (np.max(xyzs_list[-1]) - np.min(xyzs_list[-1]))
        if radius is not None:
            ortho = radius*nput.vec_crosses(
                [x[-1] - x[0], y[-1] - y[0], z[-1] - z[0]], [0, 0, 1],
                normalize=True
            )
            x,y,z = proj3d.proj_transform([ortho[0]], [ortho[1]], [ortho[2]], artist.axes.M)
            base_shift += np.linalg.norm([x[0], y[0], z[0]]) / 5
        return base_shift
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
        from mpl_toolkits.mplot3d import proj3d
        xyzs_list = proj3d.proj_transform(*artist._verts3d, artist.axes.M)
        # base_shift = 1.5 * (np.max(xyzs_list[-1]) - np.min(xyzs_list[-1]))
        base_shift = 0
        if radius is not None:
            if xyzs_list[-1][0] > xyzs_list[-1][-1]:
                base_shift += radius
        return base_shift

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
        if cls._off_stroke is None:
            import matplotlib.patheffects as pe
            class OffsetStroke(pe.Stroke):
                def __init__(self, offset=(0, 0), pixel_scaling=1, stroke_offset=.025, **kwargs):
                    """
                    **LLM Docstring**

                    Set up an offset outline stroke path-effect.

                    :param offset: the base offset
                    :param pixel_scaling: the pixel-to-data scaling
                    :param stroke_offset: the outline offset amount
                    :param kwargs: options forwarded to `Stroke`
                    """
                    self._scaling = pixel_scaling
                    super().__init__(offset, **kwargs)
                    self._stroke_offset = stroke_offset

                def draw_path(self, renderer, gc, tpath, affine, rgbFace):
                    """
                    **LLM Docstring**

                    Draw the stroked path with the configured offset.

                    :param renderer: the renderer
                    :param gc: the graphics context
                    :param tpath: the path
                    :param affine: the affine transform
                    :param rgbFace: the fill color
                    """
                    # lw = self._gc.get('linewidth')
                    # if lw is not None:
                    verts = tpath.vertices
                    # n = lw * self._scaling / 2
                    # dx, m = nput.vec_normalize(verts[-1] - verts[0], return_norms=True)
                    # n = m / 4
                    # if m < n:
                    #     tpath = None
                    # else:
                    dx = (verts[-1] - verts[0])
                    new_verts = np.array([
                        verts[0] + self._stroke_offset * dx,
                        verts[-1] - self._stroke_offset * dx
                    ])
                    # raise Exception(new_verts, verts, dx, n)
                    tpath = type(tpath)(new_verts, tpath.codes)
                    # if tpath is not None:
                    super().draw_path(renderer, gc, tpath, affine, rgbFace)
            cls._off_stroke = OffsetStroke
        return cls._off_stroke
    @classmethod
    def _flat_cylinder_predraw(cls, line3d, dist, *,
                               depth_shading_range, depth_shading_targets,
                               edge_color=None, edge_width=None, pixel_scaling=1
                               ):
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

        import matplotlib.patheffects as pe

        if depth_shading_range is not None and depth_shading_targets is not None:
            perc = nput.vec_rescale(dist, depth_shading_targets, cur_range=depth_shading_range, clip=True)
            try:
                cur_fc = line3d._og_facecolors
            except AttributeError:
                c = line3d.get_color()
                if isinstance(c, str): c = np.array(ColorPalette.parse_color_string(c)) / 255
                if len(c) == 3: c = np.concatenate([c, [1]])
                cur_fc = line3d._og_facecolors = np.asanyarray(c)
            new_fc = ColorPalette.color_lighten(cur_fc[:3] * 255, -perc, shift=True, modification_space='lab') / 255
            line3d.set_color(np.concatenate([new_fc, cur_fc[(3,),]], axis=0))
        else:
            perc = None

        # print(dir(line3d))
        try:
            cur_size = line3d._og_sizes
        except AttributeError:
            cur_size = line3d._og_sizes = np.asanyarray(line3d.get_linewidth())
        sclaing = cls._get_axis_scaling(line3d)
        lw = sclaing * cur_size
        line3d.set_linewidth(lw)
        if edge_color is not None and edge_width is not None:
            # offset_vector = line3d.get_data()
            # x = nput.vec_normalize(offset_vector[-1] - offset_vector[0])
            # y = np.array([-x[1], x[0]])
            OffStroke = cls._load_stroke()
            line3d.set_path_effects(
                [
                    OffStroke(linewidth=lw+edge_width,
                              foreground=edge_color,
                              capstyle='butt'),
                    pe.Normal()
                ]
            )
    def draw_cylinder(self, start, end, rad, circle_points=48, rendering=None,
                      box_scalings=None,
                      edge_color=None,
                      color='black',
                      glow=None,
                      segments=1,
                      segment_overdraw=.05,
                      edge_width=.01,
                      lw=None,
                      depth_shading_range=(-1, 1),
                      depth_shading_targets=(-.5, .5),
                      color_cycle=False,
                      capstyle='butt',
                      plotter='plot',
                      **opts):
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
        import matplotlib.patheffects as pe

        if glow is not None:
            if color is None:
                color = glow
            else:
                color = ColorPalette.prep_color(palette=[glow, color], blending=.5)
        if dev.str_is(rendering, 'flat'):
            # from mpl_toolkits.mplot3d.art3d import Line3DCollection
            start = np.asanyarray(start)
            if start.ndim == 1:
                start = start[np.newaxis]
            end = np.asanyarray(end)
            if end.ndim == 1:
                end = end[np.newaxis]
            plot = self.get_plotter('plot')
            if box_scalings is None:
                box_scalings = [1, 1, 1]
            if box_scalings is not None:
                box_scalings = np.array(box_scalings) * self._view_scaling
            if lw is None:
                rad = np.asanyarray(rad)
                if rad.ndim == 0:
                    rad = np.array([rad])
                lw = rad * 72 * max(box_scalings)
            if edge_color is None:
                edge_color = [None] * len(start)
            elif isinstance(edge_color, str) or nput.is_numeric(edge_color[0]):
                edge_color = [edge_color] * len(start)
            if isinstance(color, str) or nput.is_numeric(color[0]):
                color = [color] * len(start)

            coll = []
            # lines = []
            # colors = []
            # linewidths = []
            # if plotter == 'plot':
            #
            # for s, e, w, ec, c in zip(start, end, lw, edge_color, color):
            #     if ec is not None:
            #         ww = w + (edge_width * 72 * max(box_scalings))
            #         cw = ww / (72 * max(box_scalings))
            #         v, n = nput.vec_normalize(e - s, return_norms=True)
            #         d = np.linspace(cw, n-cw, segments+1)
            #         # print(c, v, n)
            #         x_points, y_points, z_points = (s[np.newaxis] + v[np.newaxis] * d[:, np.newaxis]).T
            #         # x_points = [s[0], e[0]]
            #         # y_points = [s[1], e[1]]
            #         # z_points = [s[2], e[2]]
            #         # lines.append(
            #         #     np.vstack([x_points, y_points, z_points]).T
            #         # )
            #         # colors.append(ec)
            #         # linewidths.append(w + (.05 * 72 * max(box_scalings)))
            #         coll.append(
            #             plot(
            #                 x_points,
            #                 y_points,
            #                 zs=z_points,
            #                 color=ec,
            #                 lw=ww,
            #                 # zorder=-1,
            #                 **opts
            #             )
            #         )
            #         for l in coll[-1]:
            #             l.zdist_offset = functools.partial(self._get_line_outline_proj, radius=cw)
            #             l.do_3d_projection = functools.partial(self._line_do_3d_projection, l)
            #             l.distance_mode = np.max
            #         # for i, (x1, y1, z1, x2, y2, z2) in enumerate(zip(
            #         #         x_points[:-1], y_points[:-1], z_points[:-1],
            #         #         x_points[1:], y_points[1:], z_points[1:],
            #         # )):
            #         #     coll.append(
            #         #         plot(
            #         #             [x1, x2],
            #         #             [y1, y2],
            #         #             zs=[z1, z2],
            #         #             lw=w + (edge_width * 72 * max(box_scalings)),
            #         #             color=ec,  # cycle[i%5],
            #         #             **opts
            #         #         )
            #         #     )

            if color_cycle is True:
                color_cycle = ["red", "blue", "green", "orange", "purple"]
            ew = edge_width * (72 * max(box_scalings))
            for s, e, w, ec, c in zip(start, end, lw, edge_color, color):
                # cw = w / (72 * max(box_scalings))
                v, n = nput.vec_normalize(e - s, return_norms=True)
                # s = s - cw * v
                # e = e + cw * v
                d = np.linspace(0, n, segments+1)
                x_points, y_points, z_points = (s[np.newaxis] + v[np.newaxis] * d[:, np.newaxis]).T
                if segment_overdraw > 0:
                    d = d + (n * segment_overdraw)
                    # d[-1] = n
                    x2_points, y2_points, z2_points = (s[np.newaxis] + v[np.newaxis] * d[1:, np.newaxis]).T
                else:
                    x2_points, y2_points, z2_points = x_points[1:], y_points[1:], z_points[1:]
                for i,(x1,y1,z1,x2,y2,z2) in enumerate(zip(
                    x_points[:-1],y_points[:-1],z_points[:-1],
                    x2_points, y2_points, z2_points
                )):
                    if color_cycle:
                        c = color_cycle[i%len(color_cycle)]
                    coll.append(
                        plot(
                            [x1, x2],
                            [y1, y2],
                            zs=[z1, z2],
                            lw=w,
                            color=c,
                            solid_capstyle=capstyle,
                            path_effects=(
                                [pe.Stroke(linewidth=w+ew, foreground=ec, capstyle='butt'), pe.Normal()]
                                    if ec is not None and ew > 0 else
                                None
                            ),
                            **opts
                        )
                    )
                    for l in coll[-1]:
                        # l.zdist_offset = functools.partial(self._get_line_proj, radius=cw)
                        l.do_3d_projection = functools.partial(self._line_do_3d_projection, l)
                        l.distance_mode = np.min
                        l.predraw = functools.partial(self._flat_cylinder_predraw, l,
                                                      depth_shading_range=depth_shading_range,
                                                      depth_shading_targets=depth_shading_targets,
                                                      edge_color=ec,
                                                      edge_width=ew,
                                                      pixel_scaling=1/(72 * np.max(box_scalings)))
                # coll.append(
                #     plot(
                #         x_points,
                #         y_points,
                #         zs=z_points,
                #         lw=w,
                #         color=c,
                #         **opts
                #     )
                # )


            # elif plotter == 'rect':
            #     import matplotlib.patches as patches
            #     import mpl_toolkits.mplot3d.art3d as art3d
            #     # Create a 2D Rectangle patch object
            #     lw = lw / (72 * max(box_scalings))
            #     z_positions = None
            #     for s, e, w, c in zip(start, end, lw, color):
            #         x_points = np.linspace(s[0], e[0], segments)
            #         y_points = np.linspace(s[1], e[1], segments)
            #         z_points = np.linspace(s[2], e[2], segments)
            #         # for (x1,y1,z1,x2,y2,z2) in zip(
            #         #     x_points[:-1],y_points[:-1],z_points[:-1],
            #         #     x_points[1:],y_points[1:],z_points[1:],
            #         # ):
            #         #     lines.append(
            #         #         [[x1, y1, z1], [x2, y2, z2]]
            #         #     )
            #         #     colors.append(c)
            #         #     linewidths.append(w)
            #         # cycle = ['red', 'green', 'blue', 'orange', 'pink']
            #         for i,(x1,y1,z1,x2,y2,z2) in enumerate(zip(
            #             x_points[:-1],y_points[:-1],z_points[:-1],
            #             x_points[1:],y_points[1:],z_points[1:],
            #         )):
            #             x0 = min([x1,x2])
            #             x0 = min([x1,x2])
            #
            #             w = x2-x1
            #             h = y2-y1
            #             coll.append(
            #                 patches.Rectangle(xy_center, width, height, color=color, alpha=alpha)
            #                 plot(
            #                     [x1, x2],
            #                     [y1, y2],
            #                     zs=[z1, z2],
            #                     lw=w,
            #                     color=c,#cycle[i%5],
            #                     edgecolor=ec,
            #                     **opts
            #                 )
            #             )
            #     rect = patches.Rectangle(xy_center, width, height, color=color, alpha=alpha)
            #
            #     for z_pos,rect in zip(z_positions, coll):
            #         # Convert the 2D patch to a 3D patch and add it to the axes
            #         self.obj.add_patch(rect)
            #         art3d.pathpatch_2d_to_3d(rect, z_pos=z_pos, zdir='z')
            # else:
            #     coll = Line3DCollection(lines, colors=colors, linewidths=linewidths, **opts)
            #
            #     min_x = np.min(start[:, 0])
            #     max_x = np.max(start[:, 0])
            #     xl_m, xl_M = self.get_xlim()
            #     if xl_m > min_x:
            #         xl_m = min_x
            #     if xl_M < max_x:
            #         xl_M = max_x
            #     self.set_xlim([xl_m, xl_M])
            #     min_y = np.min(start[:, 1])
            #     max_y = np.max(start[:, 1])
            #     yl_m, yl_M = self.get_ylim()
            #     if xl_m > min_y:
            #         yl_m = min_y
            #     if yl_M < max_y:
            #         yl_M = max_y
            #     self.set_ylim([yl_m, yl_M])
            #     min_z = np.min(start[:, 2])
            #     max_z = np.max(start[:, 2])
            #     zl_m, zl_M = self.get_zlim()
            #     if zl_m > min_z:
            #         zl_m = min_z
            #     if zl_M < max_z:
            #         zl_M = max_z
            #     self.set_zlim([zl_m, zl_M])
            #     self.obj.add_collection(coll)
            return coll
        else:
            surface = self.get_plotter('plot_surface')

            u = np.linspace(0, 2 * np.pi, circle_points)
            v = np.linspace(0, np.pi, circle_points)

            # pulled from SO: https://stackoverflow.com/a/32383775/5720002

            # vector in direction of axis
            v = end - start
            # find magnitude of vector
            mag = np.linalg.norm(v)
            # unit vector in direction of axis
            v = v / mag
            # make some vector not in the same direction as v
            not_v = np.array([1, 0, 0])
            if (v == not_v).all():
                not_v = np.array([0, 1, 0])
            # make vector perpendicular to v
            n1 = np.cross(v, not_v)
            # normalize n1
            n1 /= np.linalg.norm(n1)
            # make unit vector perpendicular to v and n1
            n2 = np.cross(v, n1)
            # surface ranges over t from 0 to length of axis and 0 to 2*pi
            t = np.linspace(0, mag, circle_points)
            theta = np.linspace(0, 2 * np.pi, circle_points)
            # use meshgrid to make 2d arrays
            t, theta = np.meshgrid(t, theta)
            # generate coordinates for surface
            X, Y, Z = [start[i] + v[i] * t + rad * np.sin(theta) * n1[i] + rad * np.cos(theta) * n2[i] for i
                       in [0, 1, 2]]

            return surface(X, Y, Z, color=color, **opts)

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
        return 2*np.min(zs) - np.max(zs)
    def draw_disk(self, centers, radius=None, angle=None, normal=None, uv_axes=None, zdir=None,
                  theta1=None, theta2=None,
                  rendering='flat', box_scalings=None,
                  line_color=None, line_thickness=None,
                  color=None,
                  glow=None,
                  lw=None,
                  **styles):
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
        patches = MPLManager.patch_api()
        paths = MPLManager.path_api()
        # coll = MPLManager.collections_api()
        centers = np.asanyarray(centers)
        if centers.ndim == 1:
            centers = centers[np.newaxis]

        if rendering != 'flat':
            raise NotImplementedError(f'arc rendering {rendering}')

        if glow is not None:
            if color is None:
                color = glow
            else:
                color = ColorPalette.prep_color(palette=[glow, color], blending=.5)

        if uv_axes is not None:
            u, v = uv_axes
            base_ang, base_norm = nput.vec_angles(u, v, return_crosses=True)
            base_norm = nput.vec_normalize(base_norm)
            if normal is None:
                normal = base_norm
            angs, crosses, cns = nput.vec_angles([0, 0, 1], normal, return_crosses=True, return_cross_norms=True)
            if cns < 1e-6:
                embedding_axes = np.eye(3)
            else:
                embedding_axes = nput.rotation_matrix(crosses, angs)
            emb_u, emb_v = np.array([u, v]) @ embedding_axes
            emb_z = np.cross(emb_u, emb_v)
            emb_angle = np.arctan2(emb_u[1], emb_u[0])
            if emb_z[2] < 0:
                emb_angle = -emb_angle
            if angle is None:
                angle = base_ang
            # if np.dot(ax2, local_z) < 0:
            #     emb_angle = (emb_angle - angle)
            #     if emb_angle < 0:
            #         emb_angle = 2*np.pi + emb_angle
            if theta1 is None:
                theta1 = np.rad2deg(emb_angle)
            if theta2 is None:
                theta2 = np.rad2deg(emb_angle + angle)
        if zdir is None:
            zdir = normal

        if theta1 is None or nput.is_numeric(theta1):
            theta1 = [theta1] * len(centers)
        if theta2 is None or nput.is_numeric(theta2):
            theta2 = [theta2] * len(centers)
        if radius is None or nput.is_numeric(radius):
            radius = [radius] * len(centers)
        if isinstance(zdir, str) or zdir is None or nput.is_numeric(zdir[0]):
            zdir = [zdir] * len(centers)
        if isinstance(line_color, str) or line_color is None:
            line_color = [line_color] * len(centers)
        if box_scalings is None:
            box_scalings = [1, 1, 1]
        if box_scalings is not None:
            box_scalings = np.array(box_scalings) * self._view_scaling
        if lw is None:
            if line_thickness is None or nput.is_numeric(line_thickness):
                line_thickness = [line_thickness] * len(centers)
            lw = np.asanyarray(line_thickness) * 72 * max(box_scalings)
        if lw is None or nput.is_numeric(lw):
            lw = [lw] * len(centers)
        if isinstance(color, str) or color is None:
            color = [color] * len(centers)

        arcs = []

        for c,r,t1,t2,zd,col,lc,w in zip(centers, radius, theta1, theta2, zdir,
                                       color, line_color,lw):
            if col is None:
                # a = patches.Arc((0, 0), 2 * r, 2 * r,
                #                 theta1=t1, theta2=t2)
                # from matplotlib.path import Path as paths
                n = int(72 / 360 * (t2 - t1))
                p = paths.Path.arc(theta1=t1, theta2=t2, n=n)
                a = patches.PathPatch(
                    p,
                    # paths.Path(p.vertices, p.codes),
                    lw=w,
                    facecolor='none',
                    edgecolor=lc,
                    **styles
                )
                # raise Exception(a.codes)
            else:
                a = patches.Wedge((0, 0), r,
                                  theta1=t1, theta2=t2,
                                  color=col, edgecolor=lc, lw=w,
                                  # facecolor='none',
                                  **styles)
            arcs.append(a)
            self._monkeypatch_patch(a, c, zdir=zd, zorder_mode=self._arc_proj_max)
            self.obj.add_patch(a)

        return arcs

    def draw_line(self, points,
                  rendering='flat', box_scalings=None,
                  line_thickness=None,
                  lw=None,
                  s=None,
                  edgecolors=None,
                  **styles):
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
        points = np.asanyarray(points)
        if points.ndim > 2:
            points = points.reshape(-1, 3)
        if box_scalings is None:
            box_scalings = [1, 1, 1]
        if box_scalings is not None:
            box_scalings = np.array(box_scalings) * self._view_scaling
        if lw is None and line_thickness is not None:
            rad = np.asanyarray(line_thickness)
            if rad.ndim == 0:
                rad = np.array([rad])
            lw = rad * 72 * max(box_scalings)
        return self.get_plotter('plot')(
            points[:, 0],
            points[:, 1],
            zs=points[:, 2],
            lw=lw,
            **styles
        )

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
        if cls._Arrow3D is None:
            from mpl_toolkits.mplot3d.proj3d import proj_transform
            from matplotlib.patches import FancyArrowPatch
            class Arrow3D(FancyArrowPatch):

                def __init__(self, x, y, z, dx, dy, dz, *args, **kwargs):
                    """
                    **LLM Docstring**

                    Set up a 3D arrow from a base point and a displacement vector.

                    :param x: the base x
                    :param y: the base y
                    :param z: the base z
                    :param dx: the x displacement
                    :param dy: the y displacement
                    :param dz: the z displacement
                    :param args: extra `FancyArrowPatch` args
                    :param kwargs: extra `FancyArrowPatch` options
                    """
                    super().__init__((0, 0), (0, 0), *args, **kwargs)
                    self._xyz = (x, y, z)
                    self._dxdydz = (dx, dy, dz)

                def draw(self, renderer):
                    """
                    **LLM Docstring**

                    Project the arrow's 3D endpoints into 2D and draw it.

                    :param renderer: the matplotlib renderer
                    """
                    x1, y1, z1 = self._xyz
                    dx, dy, dz = self._dxdydz
                    x2, y2, z2 = (x1 + dx, y1 + dy, z1 + dz)

                    xs, ys, zs = proj_transform((x1, x2), (y1, y2), (z1, z2), self.axes.M)
                    fuzz = np.random.rand(2, 2) * 1e-8
                    xs = xs[:2] + fuzz[0]
                    ys = ys[:2] + fuzz[1]
                    self.set_positions((xs[0], ys[0]), (xs[1], ys[1]+1e-8))
                    super().draw(renderer)

                distance_mode = staticmethod(np.min)
                def do_3d_projection(self, renderer=None, mode=None):
                    """
                    **LLM Docstring**

                    Project the arrow's 3D endpoints into 2D and return its depth key for z-ordering.

                    :param renderer: the renderer
                    :param mode: the depth-reduction mode
                    :return: the depth key
                    :rtype: float
                    """
                    x1, y1, z1 = self._xyz
                    dx, dy, dz = self._dxdydz
                    x2, y2, z2 = (x1 + dx, y1 + dy, z1 + dz)

                    xs, ys, zs = proj_transform((x1, x2), (y1, y2), (z1, z2), self.axes.M)
                    self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))

                    if mode is None:
                        mode = self.distance_mode
                    return mode(zs)
            cls._Arrow3D = Arrow3D
        return cls._Arrow3D

    def draw_arrow(self, points, radius=None, rendering=None, segments=8, box_scalings=None,
                   lw=None,
                   **styles):
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
        if dev.str_is(rendering, 'flat'):
            points = np.asanyarray(points)
            if points.ndim == 1:
                points = points[np.newaxis]
            Arrow3D = self._load_arrow_drawer()
            points = np.asanyarray(points)
            if points.ndim == 2:
                points = points[np.newaxis]
            diffs = points[:, 1, :] - points[:, 0, :]
            if box_scalings is None:
                box_scalings = [1, 1, 1]
            if box_scalings is not None:
                box_scalings = np.array(box_scalings) * self._view_scaling
            if lw is None:
                radius = np.asanyarray(radius)
                if radius.ndim == 0:
                    radius = np.array([radius])
                if box_scalings is None:
                    box_scalings = [1, 1, 1]
                lw = radius * 72 * max(box_scalings)
            # if head_width is None:
            #     head_width = lw*1.5
            # if head_length is None:
            #     head_length = head_width
            arrows = [
                Arrow3D(x, y, z, dx, dy, dz, mutation_scale=w, **styles)
                for (x,y,z),(dx,dy,dz),w in zip(points[:, 0, :], diffs, lw)
            ]
            for a in arrows:
                self.obj.add_artist(a)
            return arrows
        else:
            raise NotImplementedError("too annoying")

    def draw_text(self, points, vals, billboard=True, normal=None, rendering='flat',
                  box_scalings=None, zdir=None,
                  **styles):
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
        if billboard:
            normal = None
        if zdir is None:
            zdir = normal
            if isinstance(zdir, np.ndarray): zdir = tuple(float(z) for z in zdir)
        return super().draw_text(points, vals, zdir=zdir, **styles)

    def draw_box(self, start, end, **opts):
        """
        **LLM Docstring**

        Draw an axis-aligned box between two corners (matplotlib backend).

        :param start: the min corner
        :param end: the max corner
        :param opts: extra options
        """
        raise NotImplementedError(...)
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
        if mpl_figure_object in self._refs: raise ValueError(...)
        self._refs.add(mpl_figure_object)
        self.obj = mpl_figure_object
        if display_format is None:
            display_format = self.default_display_format
        self.display_format = display_format
        super().__init__(**self.canonicalize_opts(opts))
    def __hash__(self): # we need weakref to behave right
        """
        **LLM Docstring**

        Hash by the backing figure (so weak references behave correctly).

        :return: the hash
        :rtype: int
        """
        return hash(self.obj)
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
        return self.add_axes(
            self.obj.add_subplot((rows, cols, spans), **kw)
        )
    def create_inset(self, bbox, **kw) -> 'GraphicsAxes':
        """
        **LLM Docstring**

        Create an inset axes at the given bounding box (matplotlib backend).

        :param bbox: the inset bounding box
        :param kw: extra keyword options
        :return: the result
        """
        ((x, y), (X, Y)) = bbox
        return self.add_axes(
            self.obj.add_axes([x, y, X-x, Y-y], **kw)
        )
    def clear(self, *, backend):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (matplotlib backend).

        """
        raise NotImplementedError(...)
    def close(self, *, backend):
        """
        **LLM Docstring**

        Close the figure (matplotlib backend).

        """
        return backend.plt.close(self.obj)

    _cb_opts = ("orientation", "extendfrac", "extendrect", "drawedges", "boundaries", "spacing")
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
        if graphics is None:
            import matplotlib.cm as cm
            graphics = cm.ScalarMappable(norm=norm, cmap=cmap)
        cb_opts, fig_opts = dev.OptionsSet(kw).split(None, self._cb_opts)
        self.obj.colorbar(graphics, cax=axes.obj, **cb_opts)
        if len(fig_opts) > 0:
            from .Graphics import Graphics
            Graphics(
                # parent=self,
                figure=self,
                axes=axes
            ).set_options(**fig_opts)
        return axes
    def get_figure_label(self):
        """
        **LLM Docstring**

        Return the overall figure label (matplotlib backend).

        :return: the result
        """
        return self.obj.suptitle()
    def set_figure_label(self, val, **style):
        """
        **LLM Docstring**

        Set the overall figure label (matplotlib backend).

        :param val: the label text
        :param style: label styling options
        """
        self.obj.suptitle(val, **style)

    def get_size_inches(self):
        """
        **LLM Docstring**

        Return the figure size in inches (matplotlib backend).

        :return: the result
        """
        return self.obj.get_size_inches()
    def set_size_inches(self, w, h):
        """
        **LLM Docstring**

        Set the figure size in inches (matplotlib backend).

        :param w: the width in inches
        :param h: the height in inches
        """
        self.obj.set_size_inches(w, h)

    def set_extents(self, extents):
        """
        **LLM Docstring**

        Set the figure's coordinate extents (matplotlib backend).

        :param extents: the extents
        """
        if isinstance(extents, (list, tuple)):
            lr, bt = extents
            if isinstance(lr, (list, tuple)):
                l,r = lr
            else:
                l = r = lr
            if isinstance(bt, (list, tuple)):
                b,t = bt
            else:
                b = t = bt
        else:
            l = r = b = t = extents
        self.obj.subplots_adjust(
            left=l,
            right=r,
            bottom=b,
            top=t
        )  # , hspace=0, wspace=0)

    def set_figure_spacings(self, spacing):
        """
        **LLM Docstring**

        Set the inter-panel spacings (matplotlib backend).

        :param spacing: the spacings
        """
        if isinstance(spacing, (list, tuple)):
            w,h = spacing
        else:
            w = h = spacing
        self.obj.subplots_adjust(wspace=w, hspace=h)

    def get_facecolor(self):
        """
        **LLM Docstring**

        Return the background/face color (matplotlib backend).

        :return: the result
        """
        return self.obj.get_facecolor()
    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color (matplotlib backend).

        :param fg: the face color
        """
        if isinstance(fg, str) and fg == 'transparent':
            fg = 'none'
        return self.obj.set_facecolor(fg)

    def savefig(self, file, facecolor=None, **opts):
        """
        **LLM Docstring**

        Save the figure to a file (matplotlib backend).

        :param file: the destination file/path
        :param facecolor: the `facecolor`
        :param opts: extra options
        """
        if dev.str_is(facecolor, 'transparent'):
            facecolor = 'none'
        return self.obj.savefig(file, facecolor=facecolor, **opts)

    def animate_frames(self, frames, export_html=True, **animation_opts):
        """
        **LLM Docstring**

        Animate a sequence of frames (matplotlib backend).

        :param frames: the animation frames
        :param export_html: the `export_html`
        :param animation_opts: animation options
        """
        fig = self.obj
        frames = [
            [f] if hasattr(f, 'axes') else f
            for f in frames
        ]
        frames = [
            [
                f.graphics if hasattr(f, 'graphics') else f
                for f in frame_list
            ]
            for frame_list in frames
        ]
        animation = MPLManager.animations_api().ArtistAnimation(
            fig,
            frames,
            **animation_opts
        )
        if export_html:
            from ..Jupyter import JHTML
            display = JHTML.APIs.get_display_api()
            animation = display.HTML(animation.to_jshtml())
        return animation
    def to_html(self, format=None):
        """
        **LLM Docstring**

        Render the figure to HTML (matplotlib backend).

        :param format: the `format`
        :return: the result
        """
        if format is None:
            format = self.display_format
        if format == 'svg':
            html = self.to_svg()
        else:
            html = self.obj._repr_html_()
        return html
    def to_data_url(self):
        """
        **LLM Docstring**

        Render the figure to a base64-encoded PNG `data:` URL.

        :return: the data URL
        :rtype: str
        """
        buf = io.BytesIO()
        self.obj.savefig(buf, format='png')
        buf.seek(0)
        b64_img = base64.b64encode(buf.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{b64_img}"
    def to_svg(self):
        """
        **LLM Docstring**

        Render the figure to an SVG string.

        :return: the SVG markup
        :rtype: str
        """
        buf = io.StringIO()
        self.obj.savefig(buf, format='svg')
        buf.seek(0)
        return buf.read()
    def to_widget(self, format=None, autoclose=True):
        """
        **LLM Docstring**

        Render the figure as an interactive widget (matplotlib backend).

        :param format: the `format`
        :param autoclose: the `autoclose`
        :return: the result
        """
        from .. import Jupyter as interactive
        if format is None:
            format = self.display_format
        if format == 'svg':
            widg = interactive.JHTML.HTML.RawHTML(self.to_svg())
        elif format == 'html':
            widg = interactive.JHTML.HTML.RawHTML(self.to_html(format='html'))
        else:
            widg = interactive.JHTML.Image(src=self.to_data_url())
        return widg
    def get_mime_bundle(self):
        """
        **LLM Docstring**

        Return the figure's MIME bundle for rich display (matplotlib backend).

        :return: the result
        """
        if self.display_format == 'svg':
            return {
                'image/svg+xml':self.to_svg()
            }
        else:
            return super().get_mime_bundle()
    def tight_layout(self):
        """
        **LLM Docstring**

        Tighten the figure layout to remove excess whitespace (matplotlib backend).

        """
        self.obj.tight_layout()

class MPLBackend(GraphicsBackend):
    Figure = MPLFigure
    default_mpl_backend = None
    @property
    def plt(self):
        """
        **LLM Docstring**

        The matplotlib `pyplot` module.

        :return: the `pyplot` module
        """
        return MPLManager.plt_api()
    @property
    def mpl(self):
        """
        **LLM Docstring**

        The top-level `matplotlib` module.

        :return: the `matplotlib` module
        """
        return MPLManager.mpl_api()
    @contextlib.contextmanager
    def manage_backend(self, target=None):
        matplotlib = MPLManager.mpl_api()
        if target is None:
            target = self.default_mpl_backend
        if target is None:
            from ..Jupyter.JHTML import JupyterAPIs
            dynamic_loading = JupyterAPIs().in_jupyter_environment()
            if dynamic_loading:
                target = 'agg'
        if target is not None:
            old_backend = matplotlib.get_backend()
            try:
                matplotlib.use(target)
                yield
            finally:
                matplotlib.use(old_backend)
        else:
            yield
    def create_raw_figure(self, *args, **kwargs):
        """
        **LLM Docstring**

        Create a new figure (and its initial axes) for this backend (matplotlib backend).

        :param args: positional arguments
        :param kwargs: extra keyword options
        :return: the result
        """
        Axes = self.Figure.Axes
        with self.manage_backend():
            figure, axes = MPLManager.plt_api().subplots(*args, **kwargs)
        if isinstance(axes, (np.ndarray, list, tuple)):
            if isinstance(axes[0], (np.ndarray, list, tuple)):
                axes = tuple(tuple(Axes(b) for b in a) for a in axes)
            else:
                axes = tuple(Axes(a) for a in axes)
        else:
            axes = Axes(axes)
        return self.Figure(figure), axes
    def show_all(self):
        """
        **LLM Docstring**

        Show all open matplotlib figures.
        """
        self.plt.show()

    class ThemeContextManager(GraphicsBackend.ThemeContextManager):
        def __init__(self, theme_parents, theme_spec, backend):
            """
            **LLM Docstring**

            Set up the matplotlib theme context (an `rc_context`-style style override).

            :param args: positional theme arguments
            :param kwargs: theme options
            """
            super().__init__(theme_parents, theme_spec, backend)
            self.context = MPLManager.plt_api().style.context(self.spec)

        @classmethod
        def canonicalize_theme_opts(self, theme_parents, theme_opts) -> 'tuple[list[str], dict]':
            """
            **LLM Docstring**

            Normalize theme options into the backend's canonical form (matplotlib backend).

            :param theme_parents: the parent themes
            :param theme_opts: the `theme_opts`
            """
            from cycler import cycler
            from .Graphics import Graphics

            rem_opts = {}
            theme_dict = {}
            for k,v in theme_opts.items():
                if k in (
                        Graphics.opt_keys
                        | Graphics.axes_keys
                        | Graphics.figure_keys
                ):
                    continue
                if isinstance(v, dict):
                    for sk,sv in v.items():
                        if isinstance(sv, dict):
                            sv = cycler(**sv)
                        theme_dict[k+'.'+sk] = sv
                # else:
                #     rem_opts[k] = v
                # else:
                #     theme_dict[k] = v
            return theme_parents + [theme_dict], rem_opts

        def begin_context(self):
            """
            **LLM Docstring**

            Enter the context, applying the theme.

            """
            return self.context.__enter__()
        def end_context(self, exc_type, exc_val, exc_tb):
            """
            **LLM Docstring**

            Exit the context, restoring the previous theme.

            :param exc_type: the exception type, if any
            :param exc_val: the exception value, if any
            :param exc_tb: the traceback, if any
            """
            return self.context.__exit__(exc_type, exc_val, exc_tb)

    def show_figure(self, graphics:MPLFigure, autoclose=True, reshow=None):
        """
        **LLM Docstring**

        Display a figure via the backend (matplotlib backend).

        :param graphics: the `graphics`
        :param autoclose: the `autoclose`
        :param reshow: force a reshow of an already-shown figure
        """
        from ..Jupyter.JHTML import JupyterAPIs
        dynamic_loading = JupyterAPIs().in_jupyter_environment()
        if not dynamic_loading:
            self.plt.show()
        elif not graphics.shown:
            graphics.shown = True
            html = graphics.to_widget()
            if autoclose:
                self.close_figure(graphics)
            return html.display()
    def to_widget(self, figure:GraphicsFigure, autoclose=True):
        """
        **LLM Docstring**

        Render the figure as an interactive widget (matplotlib backend).

        :param figure: the `figure`
        :param autoclose: the `autoclose`
        :return: the result
        """
        widg = super().to_widget(figure)
        if autoclose:
            self.close_figure(figure)
        return widg

    def get_interactive_status(self) -> 'bool':
        """
        **LLM Docstring**

        Return whether interactive mode is on (matplotlib backend).

        :return: the result
        """
        return self.plt.isinteractive()
    def disable_interactivity(self):
        """
        **LLM Docstring**

        Disable interactive mode (matplotlib backend).

        """
        return self.plt.ioff()
    def enable_interactivity(self):
        """
        **LLM Docstring**

        Enable interactive mode (matplotlib backend).

        """
        return self.plt.ion()
    def get_available_themes(self):
        """
        **LLM Docstring**

        Return the themes available for this backend (matplotlib backend).

        :return: the result
        """
        import matplotlib.style as sty
        theme_names = sty.available
        return theme_names

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
        return super().create_axes(rows, cols, spans, projection=projection, **kw)
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
        from mpl_toolkits.mplot3d import Axes3D
        subplot_kw = dict({"projection": '3d'}, **({} if subplot_kw is None else subplot_kw))
        return super().create_figure(*args, subplot_kw=subplot_kw, **kwargs)

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
        if elements is None:
            elements = []
        self.elements = elements
        if annotations is None:
            annotations = []
        self.annotations = annotations
        if xaxis is None:
            xaxis = self.base_axis_theme
        if yaxis is None:
            yaxis = self.base_axis_theme
        self.opts = self.canonicalize_opts(self.base_theme|opts|dict(yaxis=yaxis, xaxis=xaxis))
        super().__init__()

    def clear(self, *, backend=None):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (Plotly backend).

        """
        self.elements = []
    def remove(self, *, backend):
        """
        **LLM Docstring**

        Tear down (remove) this axes from its figure (Plotly backend).

        """
        self.elements = []

    def prep_elems(self):
        """
        **LLM Docstring**

        Return the axes' trace elements for figure assembly.

        :return: the trace elements
        :rtype: list
        """
        return self.elements
    def prep_annotations(self):
        """
        **LLM Docstring**

        Return the axes' annotations for figure assembly.

        :return: the annotations
        :rtype: list
        """
        return self.annotations
    axes_props = ['xaxis', 'xaxis2', 'yaxis', 'yaxis2']
    def prep_opts(self):
        """
        **LLM Docstring**

        Return the axes' layout options, dropping `None`-valued per-axis sub-options.

        :return: the layout options
        :rtype: dict
        """
        opts = self.opts.copy()
        for lab in self.axes_props:
            if lab in opts:
                opts[lab] = {k:v for k,v in opts[lab].items() if v is not None}
        return opts
    def get_plot_label(self):
        """
        **LLM Docstring**

        Return the plot title/label (Plotly backend).

        :return: the result
        """
        return self.opts.get('title')
    def set_plot_label(self, val, **style):
        """
        **LLM Docstring**

        Set the plot title/label (Plotly backend).

        :param val: the label text
        :param style: label styling options
        """
        self.opts['title'] = (val, style)

    def get_style_list(self):
        """
        **LLM Docstring**

        Return the per-series style cycle (Plotly backend).

        :return: the result
        """
        raise NotImplementedError("style list cyclers not supported")
    def set_style_list(self, props):
        """
        **LLM Docstring**

        Set the per-series style cycle (Plotly backend).

        :param props: the style cycle
        """
        self._prop_cycle = props

    def get_frame_visible(self):
        """
        **LLM Docstring**

        Return which frame (spine) edges are drawn (Plotly backend).

        :return: the result
        """
        return (
            (
                self.opts.get('yaxis', {}).get('showline', True)
                and self.opts.get('yaxis', {}).get('side', 'left') == 'left',
                self.opts.get('yaxis', {}).get('showline', True)
                and (self.opts.get('yaxis', {}).get('mirror', False)
                     or self.opts.get('yaxis', {}).get('side', 'left') == 'right'),
            ),
            (
                self.opts.get('xaxis', {}).get('showline', True)
                and self.opts.get('xaxis', {}).get('side', 'bottom') == 'bottom',
                self.opts.get('xaxis', {}).get('showline', True)
                and (self.opts.get('xaxis', {}).get('mirror', False)
                     or self.opts.get('xaxis', {}).get('side', 'bottom') == 'top'),
            )
        )
    def set_frame_visible(self, frame_spec):
        """
        **LLM Docstring**

        Set which frame (spine) edges are drawn (Plotly backend).

        :param frame_spec: the per-edge visibility spec
        """
        if frame_spec is True or frame_spec is False:
            frame_spec = (frame_spec, frame_spec)
        lr, bt = frame_spec
        if lr in {True, False}:
            l, r = lr, lr
        else:
            l, r = lr
        if bt in {True, False}:
            b, t = bt, bt
        else:
            b, t = bt
        if l:
            if r:
                self.opts['yaxis'] = self.opts.get('yaxis', {}) | {'showline': True, 'linecolor': 'black',
                                                                   'mirror': True}
            else:
                self.opts['yaxis'] = self.opts.get('yaxis', {}) | {'showline': True, 'linecolor': 'black'}
        elif r:
            self.opts['yaxis'] = self.opts.get('yaxis', {}) | {'showline': True, 'linecolor': 'black', 'side': 'right'}
        if b:
            if t:
                self.opts['xaxis'] = self.opts.get('xaxis', {}) | {'showline': True, 'linecolor': 'black',
                                                                   'mirror': True}
            else:
                self.opts['xaxis'] = self.opts.get('xaxis', {}) | {'showline': True, 'linecolor': 'black'}
        elif t:
            self.opts['xaxis'] = self.opts.get('xaxis', {}) | {'showline': True, 'linecolor': 'black', 'side': 'top'}

    def get_frame_style(self):
        """
        **LLM Docstring**

        Return the frame (spine) styling (Plotly backend).

        :return: the result
        """
        raise NotImplementedError(...)
    def set_frame_style(self, frame_spec):
        """
        **LLM Docstring**

        Set the frame (spine) styling (Plotly backend).

        :param frame_spec: the frame styling
        """
        (l, r), (b, t) = frame_spec
        if l:
            self.opts['xaxis'] = self.opts.get('xaxis', {}) | l
        if r:
            self.opts['yaxis2'] = self.opts.get('yaxis2', {}) | r
        if b:
            self.opts['yaxis'] = self.opts.get('yaxis', {}) | b
        if t:
            self.opts['xaxis2'] = self.opts.get('xaxis2', {}) | t

    def get_xlabel(self):
        """
        **LLM Docstring**

        Return the x-axis label (Plotly backend).

        :return: the result
        """
        return self.opts.get('xaxis', {}).get('title_text')
    def set_xlabel(self, val, **style):
        """
        **LLM Docstring**

        Set the x-axis label (Plotly backend).

        :param val: the label text
        :param style: label styling options
        """
        self.opts['xaxis'] = self.opts.get('xaxis', {}) | dict(
            title_text=val,
            **style
        )
    def get_ylabel(self):
        """
        **LLM Docstring**

        Return the y-axis label (Plotly backend).

        :return: the result
        """
        return self.opts.get('yaxis', {}).get('title_text')
    def set_ylabel(self, val, **style):
        """
        **LLM Docstring**

        Set the y-axis label (Plotly backend).

        :param val: the label text
        :param style: label styling options
        """
        self.opts['yaxis'] = self.opts.get('yaxis', {}) | dict(
            title_text=val,
            **style
        )

    def get_plot_range(self):
        """
        **LLM Docstring**

        Return the plotted data range (Plotly backend).

        :return: the result
        """
        min_x = None
        max_x = None
        min_y = None
        max_y = None
        for e in self.elements:
            if 'x' in e:
                if min_x is None:
                    min_x = np.min(e['x'])
                else:
                    min_x = min([min_x, np.min(e['x'])])
                if max_x is None:
                    max_x = np.max(e['x'])
                else:
                    max_x = max([max_x, np.max(e['x'])])
            if 'y' in e:
                if min_y is None:
                    min_y = np.min(e['y'])
                else:
                    min_y = min([min_x, np.min(e['y'])])
                if max_y is None:
                    max_y = np.max(e['y'])
                else:
                    max_y = max([max_y, np.max(e['y'])])
        xrange = [min_x, max_x]
        if xrange == [None, None]:
            xrange = None
        yrange = [min_y, max_y]
        if yrange == [None, None]:
            yrange = None
        return xrange, yrange

    def get_xlim(self):
        """
        **LLM Docstring**

        Return the x-axis limits (Plotly backend).

        :return: the result
        """
        xrange = self.opts.get('xaxis', {}).get('range')
        if xrange is None:
            xrange = self.get_plot_range()[0]
        return xrange
    def set_xlim(self, val, **opts):
        """
        **LLM Docstring**

        Set the x-axis limits (Plotly backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        self.opts['xaxis'] = self.opts.get('xaxis', {}) | dict(
            range=val,
            **opts
        )
    def get_ylim(self):
        """
        **LLM Docstring**

        Return the y-axis limits (Plotly backend).

        :return: the result
        """
        yrange = self.opts.get('yaxis', {}).get('range')
        if yrange is None:
            yrange = self.get_plot_range()[1]
        return yrange
    def set_ylim(self, val, **opts):
        """
        **LLM Docstring**

        Set the y-axis limits (Plotly backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        self.opts['yaxis'] = self.opts.get('yaxis', {}) | dict(
            range=val,
            **opts
        )

    def get_xticks(self):
        """
        **LLM Docstring**

        Return the x-axis tick locations (Plotly backend).

        :return: the result
        """
        return self.opts.get('xaxis', {}).get('tickvals')
    def set_xticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the x-axis tick locations (Plotly backend).

        :param val: the tick locations
        :param opts: extra options
        """
        if isinstance(val, self.TicksManager.FixedLocator):
            val = val.locs
        self.opts['xaxis'] = self.opts.get('xaxis', {}) | dict(
            tickvals=val,
            tickmode='array',
            **opts
        )
    def get_yticks(self):
        """
        **LLM Docstring**

        Return the y-axis tick locations (Plotly backend).

        :return: the result
        """
        return self.opts.get('yaxis', {}).get('tickvals')
    def set_yticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the y-axis tick locations (Plotly backend).

        :param val: the tick locations
        :param opts: extra options
        """
        if isinstance(val, self.TicksManager.FixedLocator):
            val = val.locs
        self.opts['yaxis'] = self.opts.get('yaxis', {}) | dict(
            tickvals=val,
            tickmode='array',
            **opts
        )

    def get_xtick_style(self):
        """
        **LLM Docstring**

        Return the x-axis tick styling (Plotly backend).

        :return: the result
        """
        return {
            k:v
            for k,v in self.opts.get('xaxis', {}).items()
            if k.startswith('tick') or k.startswith('minor')
        }
    def set_xtick_style(self, **opts):
        """
        **LLM Docstring**

        Set the x-axis tick styling (Plotly backend).

        :param opts: extra options
        """
        self.opts['xaxis'] = self.opts.get('xaxis', {}) | opts
    def get_ytick_style(self):
        """
        **LLM Docstring**

        Return the y-axis tick styling (Plotly backend).

        :return: the result
        """
        return {
            k:v
            for k,v in self.opts.get('yaxis', {}).items()
            if k.startswith('tick') or k.startswith('minor')
        }
    def set_ytick_style(self, **opts):
        """
        **LLM Docstring**

        Set the y-axis tick styling (Plotly backend).

        :param opts: extra options
        """
        self.opts['yaxis'] = self.opts.get('yaxis', {}) | opts

    def get_aspect_ratio(self):
        """
        **LLM Docstring**

        Return the axes aspect ratio (Plotly backend).

        :return: the result
        """
        return self.opts.get('aspect_ratio')
        # y = self.opts.get('yaxis', {})
        # if y.get('scaleanchor', '') == 'x':
        #     return y.get('scaleratio')
        # else:
        #     return None
    def set_aspect_ratio(self, ar):
        """
        **LLM Docstring**

        Set the axes aspect ratio (Plotly backend).

        :param ar: the aspect ratio
        """
        self.opts['aspect_ratio'] = ar
        # if not dev.str_is(ar, 'auto'):
        #     # self.opts['xaxis'] = self.opts.get('xaxis', {}) | {'scaleratio': 1}
        #     self.opts['yaxis'] = self.opts.get('yaxis', {}) | {
        #         'scaleanchor': 'x',
        #         'scaleratio': ar,
        #         'constrain': "domain"
        #     }


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

    style_mapping = {
        'c':'color',
        'linewidth':'width',
        'linestyle':'dash',
        'label':'name'
    }
    line_options = [
        'color',
        'width',
        'dash'
    ]
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
        for k,a in self.style_mapping.items():
            if k in opts:
                opts[a] = opts.pop(k)
        if line is None:
            line = {}
            for k in self.line_options:
                if k in opts:
                    line[k] = opts.pop(k)
        return line, opts
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
        # import plotly.graph_objects as go
        opts['mode'] = mode
        line, opts = self._prep_line_opts(line, opts)
        plot_dict = dict(type=type, x=x, y=y, line=line, **opts)
        self.elements.append(plot_dict)
        return plot_dict
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
        # import plotly.graph_objects as go
        opts['mode'] = mode
        line, opts = self._prep_line_opts(line, opts)
        plot_dict = dict(type=type, x=x, y=y, line=line, **opts)
        self.elements.append(plot_dict)
        return plot_dict
    def text(self, text, x, y, line=None, type='scatter', mode='text', textposition="middle center", color=None, textfont=None, **opts):
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
        # import plotly.graph_objects as go
        opts['mode'] = mode
        line, opts = self._prep_line_opts(line, opts)
        if textfont is None:
            textfont = {o.partition("_")[-1]:v for o,v in opts.items() if o.startswith('font_')}
            for f in textfont:
                del opts['font_'+f]
        if textfont is not None:
            textfont['color'] = color
        if len(textfont) > 0:
            opts['textfont'] = textfont
        plot_dict = dict(type=type, text=text, x=x, y=y, line=line, textposition=textposition, **opts)
        self.elements.append(plot_dict)
        return plot_dict

    def get_plotter(self, method, **opts):
        """
        **LLM Docstring**

        Resolve a plotting-method name to the backend callable that draws it (Plotly backend).

        :param method: the plot-method name
        :param opts: extra options
        :return: the result
        """
        if method == 'plot':
            return self.plot
        elif method == 'scatter':
            return self.scatter
        else:
            raise ValueError(f"don't know method {method}")

    def get_facecolor(self):
        """
        **LLM Docstring**

        Return the background/face color (Plotly backend).

        :return: the result
        """
        return self.opts.get('plot_bgcolor')
    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color (Plotly backend).

        :param fg: the face color
        """
        if dev.str_is(fg, 'transparent'):
            fg = None
        self.opts['plot_bgcolor'] = fg

    def get_padding(self):
        """
        **LLM Docstring**

        Return the axes padding (Plotly backend).

        :return: the result
        """
        return None

    def legend(self, show=True, **opts):
        """
        **LLM Docstring**

        Draw the axes legend (Plotly backend).

        :param show: the `show`
        :param opts: legend options
        :return: the result
        """
        self.opts['showlegend'] = show

    def get_graphics_properties(self, obj, property=None):
        """
        **LLM Docstring**

        Get backend properties of a drawn graphics object (Plotly backend).

        :param obj: the graphics object
        :param property: a specific property to fetch
        :return: the result
        """
        if property is not None:
            return obj.get(property)
        else:
            return obj
    def set_graphics_properties(self, obj:dict, **props):
        """
        **LLM Docstring**

        Set backend properties on a drawn graphics object (Plotly backend).

        :param obj: the graphics object
        :param props: the properties to set
        """
        obj.update(props)

    def draw_poly(self, points, **styles):
        """
        **LLM Docstring**

        Draw a filled polygon from the given points (Plotly backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        raise NotImplementedError(...)

    def draw_line(self, points, **styles):
        """
        **LLM Docstring**

        Draw a line/polyline through the given points (Plotly backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        return self.plot(*np.asanyarray(points).T, **styles)
    def draw_path(self, commands, **styles):
        """
        **LLM Docstring**

        Draw a path from a sequence of drawing commands (Plotly backend).

        :param commands: the path drawing commands
        :param styles: the styling options
        """
        points = nput.parametric_path_points(commands)
        return self.draw_line(points, **styles)
    def draw_disk(self, points, radius=None, s=None, **styles):
        """
        **LLM Docstring**

        Draw a filled disk at the given position(s) (Plotly backend).

        :param points: the points to draw
        :param radius: the `radius`
        :param s: the `s`
        :param styles: the styling options
        """
        raise NotImplementedError(...)
    def draw_rect(self, points, **styles):
        """
        **LLM Docstring**

        Draw a rectangle from the given points (Plotly backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        raise NotImplementedError(...)

    def annotation(self, points, **opts):
        """
        **LLM Docstring**

        Add an annotation (optionally an arrow annotation) to the axes.

        :param points: the annotation position (or `((ax, ay), (x, y))` for an arrow)
        :param opts: extra annotation options
        :return: the annotation dict
        :rtype: dict
        """
        if nput.is_numeric(points[0]):
            x, y = points
            ax, ay = None, None
            showarrow = False
        else:
            (ax, ay), (x, y) = points
            showarrow = True
        annotation_dict = {
            'x':x,
            'y':y,
            'ax':ax,
            'ay':ay,
            'showarrow':showarrow,
            **opts
        }
        annotation_dict = {
            k:v for k,v in annotation_dict.items()
            if v is not None
        }
        self.annotations.append(annotation_dict)
        return annotation_dict
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
        styles = dict(
            arrowcolor=color,
            arrowwidth=width,
            arrowsize=size,
            arrowhead=head,
        ) | styles
        return self.annotation(points, **styles)

    def draw_text(self, points, vals, **styles):
        """
        **LLM Docstring**

        Draw text at the given position(s) (Plotly backend).

        :param points: the points to draw
        :param vals: the text string(s)
        :param styles: the styling options
        """
        points = np.asanyarray(points)
        if points.ndim == 1:
            points = points[np.newaxis]
            vals = [vals]
        return self.text(vals, *points.T, **styles)

class PlotlyFigure(GraphicsFigure):
    Axes = PlotlyAxes
    default_export_format = 'svg'
    def __init__(self, axes=None, layout=None, export_format=None,
                 width=500,
                 height=500,
                 figsize=None,
                 id=None,
                 include_save_buttons=False,
                 **opts):
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
        if id is None:
            id = 'plotly-' + str(uuid.uuid4())[:6]
        if axes is None:
            axes = []
        if layout is None:
            layout = {}
        self.layout = layout
        if export_format is None:
            export_format = self.default_export_format
        self.export_format = export_format
        self.id = id
        self.opts = self.canonicalize_opts(opts)
        self.width = width
        self.height = height
        if figsize is not None:
            self.set_size_inches(*figsize)
        self.shown = False
        self.include_save_buttons = include_save_buttons
        super().__init__(axes=axes)
    def __setitem__(self, key, value):
        """
        **LLM Docstring**

        Set a figure option by key.

        :param key: the option name
        :param value: the option value
        """
        self.opts[key] = value
    def __getitem__(self, item):
        """
        **LLM Docstring**

        Get a figure option by key.

        :param item: the option name
        :return: the option value
        """
        return self.opts[item]
    def clear(self, *, backend):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (Plotly backend).

        """
        self.axes = []
    def close(self, *, backend):
        """
        **LLM Docstring**

        Close the figure (Plotly backend).

        """
        self.clear(backend=backend)
    def create_inset(self, bbox, **kw) -> 'GraphicsAxes':
        """
        **LLM Docstring**

        Create an inset axes at the given bounding box (Plotly backend).

        :param bbox: the inset bounding box
        :param kw: extra keyword options
        :return: the result
        """
        raise NotImplementedError(...)
    def create_axes(self, **kw) -> 'GraphicsAxes':
        """
        **LLM Docstring**

        Create a new axes within the figure at the given grid position (Plotly backend).

        :param kw: extra keyword options
        :return: the result
        """
        ax = self.Axes(**kw)
        return self.add_axes(ax)
    @classmethod
    def construct(cls, **kw) -> 'GraphicsFigure':
        """
        **LLM Docstring**

        Construct a figure of this backend type (Plotly backend).

        :param kw: construction options
        :return: the result
        """
        return cls(**kw)
    def get_size_inches(self):
        """
        **LLM Docstring**

        Return the figure size in inches (Plotly backend).

        :return: the result
        """
        return [self.width/DPI_SCALING, self.height/DPI_SCALING]
    def set_size_inches(self, w, h):
        """
        **LLM Docstring**

        Set the figure size in inches (Plotly backend).

        :param w: the width in inches
        :param h: the height in inches
        """
        self.width, self.height = w*DPI_SCALING, h*DPI_SCALING
    def set_extents(self, extents):
        """
        **LLM Docstring**

        Set the figure's coordinate extents (Plotly backend).

        :param extents: the extents
        """
        (l, r), (b, t) = extents
        self.layout['margin'] = self.layout.get('margin', {}) | dict(
            l=self.width*l,
            r=(1-r)*self.width,
            t=(1-t)*self.height,
            b=b*self.height
        )
    def get_facecolor(self):
        """
        **LLM Docstring**

        Return the background/face color (Plotly backend).

        :return: the result
        """
        return self.layout.get('paper_bgcolor')
    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color (Plotly backend).

        :param fg: the face color
        """
        if dev.str_is(fg, 'transparent'):
            fg = None
        self.layout['paper_bgcolor'] = fg

    def savefig(self, file, facecolor=None, **opts):
        """
        **LLM Docstring**

        Save the figure to a file (Plotly backend).

        :param file: the destination file/path
        :param facecolor: the `facecolor`
        :param opts: extra options
        """
        return self.to_plotly().savefig(file, facecolor=facecolor, **opts)

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
        # template = layout.pop('template', None)
        # if template is not None:
        #     if 'layout' in template:
        #         template['layout'] = cls._prep_layout_props(template['layout'])
        #
        # scene = layout.pop('scene', {})
        # for lab in cls.Axes.axes_props:
        #     if lab in layout:
        #         scene[lab] = {k:v for k,v in layout.pop(lab).items() if v is not None}
        # if len(scene) > 0:
        #     layout['scene'] = scene
        #
        # print(scene)

        return layout
    def prep_dict(self):
        """
        **LLM Docstring**

        Assemble the full Plotly figure dict from the axes' traces, annotations, and
        layout, applying the size and aspect-ratio margins.

        :return: the `{data, annotations, layout}` figure dict
        :rtype: dict
        """
        elems = []
        annotations = []
        axes_layout = self.opts
        for ax in self.axes:
            elems.extend(ax.prep_elems())
            annotations.extend(ax.prep_annotations())
            axes_layout = axes_layout | ax.prep_opts()
        layout = axes_layout | self.layout
        layout['width'] = self.width
        layout['height'] = self.height
        aspect_ratio = layout.pop('aspect_ratio', None)
        if aspect_ratio is not None:
            if nput.is_numeric(aspect_ratio):
                margin = layout.get('margin', {})
                cur_w = self.width - (margin.get('l', 0) + margin.get('r', 0))
                cur_h = self.height - (margin.get('b', 0) + margin.get('t', 0))
                h = cur_w * aspect_ratio
                dh = cur_h - h
                if dh > 0:
                    margin['b'] = margin.get('b', 0) + dh/2
                    margin['t'] = margin.get('t', 0) + dh/2
                else:
                    w = cur_h / aspect_ratio
                    dw = cur_w - w
                    margin['l'] = margin.get('l', 0) + dw/2
                    margin['r'] = margin.get('r', 0) + dw/2
                layout['margin'] = margin
        layout = self._prep_layout_props(layout)
        fig_dict = {
            'data':elems,
            'annotations':annotations,
            'layout':layout
        }
        # import pprint
        # pprint.pprint(fig_dict)
        # raise Exception(...)
        return fig_dict
    def to_plotly(self):
        """
        **LLM Docstring**

        Build a `plotly.graph_objects.Figure` from the assembled figure dict.

        :return: the Plotly figure
        """
        import plotly.graph_objects as go
        return go.Figure(self.prep_dict())

    split_plot_fragment = True
    embed_mathjax = True
    preload_plotly = True
    mathjax_cdn = "https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.min.js"
    plotly_cdn = "https://cdn.plot.ly/plotly-3.4.0.min.js"
    def get_core_body(self, html):
        """
        **LLM Docstring**

        Extract the contents of the `<body>` from a Plotly HTML export.

        :param html: the exported HTML
        :type html: str
        :return: the body contents
        :rtype: str
        """
        return html.split("<body>")[1].rsplit("</body>")[0].strip()
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
        return f'<script id="{id}"'.join(html.rsplit("""<script""", 1))
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
        plotly_tag = f"""<script type="text/javascript" id="{id}">"""
        mathjax_load_script = """
        if (window.MathJax && window.MathJax.Hub && window.MathJax.Hub.Config) {
            window.MathJax.Hub.Config({SVG: {font: "STIX-Web"}});
        }
        window.PlotlyConfig = {MathJaxConfig: "local"};
        """
        mathjax_config = f"""
        <script src="{self.mathjax_cdn}" onload='(function(){{
        {mathjax_load_script}
        }})()'>
        </script>"""
        header, tag, footer = html.partition(plotly_tag)
        footer = footer.replace("</script>", f"</script>\n{mathjax_config}", 1)
        return header + tag + footer
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
        id = 'plotly-plot-' + str(uuid.uuid4())[:6]
        html = self.set_plotly_script_id(html, id)
        if self.split_plot_fragment:
            html = self.get_core_body(html)
        # if self.embed_mathjax:
        #     html = self.configure_mathjax(html, id)
        if self.preload_plotly:
            tag =  f"""<script id="{id}" type="text/javascript">"""
            if tag in html:
                new_tag = f"""<script src="{self.plotly_cdn}" charset="utf-8" id="{id}" onload='(function(){{"""
                html = html.replace(
                    tag,
                    new_tag,
                    1
                )
            else:
                tag = f"""<script id="{id}">"""
                if tag in html:
                    new_tag = f"""<script src="{self.plotly_cdn}" charset="utf-8" id="{id}" onload='(function(){{"""
                    html = html.replace(
                        tag,
                        new_tag,
                        1
                    )
                else:
                    preamble, div_id, core = html.partition(f'id="{id}"')
                    tag = ">"
                    new_tag = f""" src="{self.plotly_cdn}" charset="utf-8" onload='(function(){{"""
                    core = core.replace(
                        tag,
                        new_tag,
                        1
                    )
                    html = preamble + div_id + core
            # replace from end, should replace with version that starts from the plotly tag
            header, tag, footer = html.partition(new_tag)
            footer = footer.replace("</script>",  "})()'></script>", 1)
            html = header + tag + footer
        return html
    def to_html(self):
        """
        **LLM Docstring**

        Render the figure to HTML (Plotly backend).

        :return: the result
        """
        # print(fig)
        buf = io.StringIO()
        self.to_plotly().write_html(buf, div_id=self.id,
                                    include_plotlyjs=False,
                                    include_mathjax='cdn' if self.embed_mathjax else False)
        buf.seek(0)
        html = buf.read()
        return self.postprocess_plotly_html(html)
    def to_svg(self):
        """
        **LLM Docstring**

        Render the figure to an SVG string.

        :return: the SVG markup
        :rtype: str
        """
        buf = io.StringIO()
        self.to_plotly().savefig(buf, format='svg')
        buf.seek(0)
        return buf.read()

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
        return f"""
    (function(){{
      let base_name = '{id}';
      let canvas = document.getElementById('{id}');
      let format = canvas.exportFormat??'{format}'
      Plotly.toImage(canvas, {{format: format}})
        .then(function(url) {{
            let link = document.createElement('a');
            link.download = base_name + '.' + format;
            link.href = url;
            link.click();
        }})
    }})()
           """
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
        return f"""
        (function(){{
            let canvas = document.getElementById('{id}');
            let input = document.getElementById('{id}-export-format');

            canvas.exportFormat = input.value;
        }})()
               """
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

        :param id: the figure's DOM id
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
    def to_widget(self, format=None, autoclose=True):
        """
        **LLM Docstring**

        Render the figure as an interactive widget (Plotly backend).

        :param format: the `format`
        :param autoclose: the `autoclose`
        :return: the result
        """
        from .. import Jupyter as interactive
        widg = interactive.JHTML.HTML.RawHTML(self.to_html())
        if self.include_save_buttons:
            widg = interactive.JHTML.Div([
                widg,
                interactive.JHTML.Button("Save Image",
                             onclick=self.get_export_script(self.id, format=self.export_format)),
                interactive.JHTML.Input(value=str(self.export_format),
                            id=self.id + '-export-format', width="50px",
                            oninput=self.set_export_format_script(self.id))
            ])
        return widg
    def animate_frames(self, frames, **animation_opts):
        """
        **LLM Docstring**

        Animate a sequence of frames (Plotly backend).

        :param frames: the animation frames
        :param animation_opts: animation options
        """
        raise NotImplementedError(...)
class PlotlyBackend(GraphicsBackend):
    Figure = PlotlyFigure
    def create_raw_figure(self, *args, **kwargs):
        fig = self.Figure(*args, **kwargs)
        ax = fig.create_axes()
        return fig, ax
    def create_figure(self, *args, template=None, **kwargs):
        """
        **LLM Docstring**

        Create a new figure (and its initial axes) for this backend (Plotly backend).

        :param args: positional arguments
        :param kwargs: extra keyword options
        :return: the result
        """
        if template is None:
            template, others = self.ThemeContextManager.current_theme()
            kwargs = others | kwargs
        return self.create_raw_figure(*args, template=dict(layout=template), **kwargs)

    @classmethod
    def prep_color(cls, v):
        """
        **LLM Docstring**

        Parse a color string and re-encode it as a Plotly-compatible RGB(A) code.

        :param v: the color string
        :return: the encoded color
        :rtype: str
        """
        v, padding = ColorPalette.parse_color_string(v, return_padding=True)
        return ColorPalette.rgb_code(v, padding)

    property_mapping = {
        'labelsize':'fontsize'
    }
    axes_props = {'xtick':'xaxis', 'ytick':'yaxis'}
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
        handler = cls.property_mapping.get(name, name)
        if not isinstance(handler, str):
            return handler(value)
        name = handler
        if name in cls.unthemed_props:
            return {}, {name:value}
        elif name == 'axes':
            vals = {}
            others = {}
            for k,v in value.items():
                remapped, unhandled = cls.remap_property(k, v)
                vals = vals | remapped
                others = others | unhandled
            return vals, others
        elif name in cls.axes_props:
            subname = cls.axes_props[name]
            vals = {}
            others = {}
            for k,v in value.items():
                remapped, unhandled = cls.remap_property(k, v, context='axis')
                vals = vals | remapped
                others = others | unhandled
            return {subname:vals}, others
        elif name == 'prop_cycle':
            vals = {}
            others = {}
            if 'color' in value:
                vals['colorway'] = tuple(cls.prep_color(v) for v in value['color'])
            return vals, others
        elif name in {'patch'}:
            return {}, {}
        elif name == 'padding':
            if nput.is_numeric(value):
                value = [value, value]
            lr, bt = value
            if nput.is_numeric(lr):
                lr = [lr, lr]
            if nput.is_numeric(bt):
                bt = [bt, bt]
            l, r = lr
            b, t = bt
            return {
                'margin': {
                    'l':l,
                    'r':r,
                    'b':b,
                    't':t
                }
            }, {}
        elif name == 'figsize':
            w, h = value
            return {
                'width':DPI_SCALING * w,
                'height':DPI_SCALING * h
            }, {}
        elif name.startswith('font'):
            key = name.split('font', 1)[-1]
            if context == 'axis':
                ax = 'tickfont'
            else:
                ax = 'font'
            return {ax:{key:value}}, {}
        elif name in {
            'frame'
        }:
            return {}, {}
        else:
            return {name:value}, {}

    class ThemeContextManager(GraphicsBackend.ThemeContextManager):
        theme_stack = []
        base_axis_theme = dict(linecolor='black',
                               showline=True,
                               showgrid=False,
                               zeroline=False,
                               ticks="outside",
                               ticklen=5,  # length in px
                               tickwidth=1,  # width in px
                               tickcolor='black',
                               minor_ticks="outside",
                               minor=dict(ticklen=2))
        base_theme = dict(plot_bgcolor='white',
                          showlegend=False)
        @classmethod
        def canonicalize_theme_opts(self, theme_parents, theme_opts) -> 'tuple[list[str], dict]':
            """
            **LLM Docstring**

            Normalize theme options into the backend's canonical form (Plotly backend).

            :param theme_parents: the parent themes
            :param theme_opts: the `theme_opts`
            """
            # theme_dict = {}
            # for k, v in theme_opts.items():
            #     if isinstance(v, dict):
            #         for sk, sv in v.items():
            #             if isinstance(sv, dict):
            #                 sv = cycler(**sv)
            #             theme_dict[k + '.' + sk] = sv
            #     # else:
            #     #     theme_dict[k] = v
            return theme_parents + [theme_opts], theme_opts
        def get_axes_theme(self):
            """
            **LLM Docstring**

            Return the axes theme (Plotly backend).

            :return: the result
            """
            return {
                'xaxis':self.base_axis_theme,
                'yaxis':self.base_axis_theme
            }
        def prep_spec(self):
            """
            **LLM Docstring**

            Assemble the Plotly layout template (and leftover properties) from the theme
            spec by remapping each object type's options.

            :return: `(layout, other_props)`
            :rtype: tuple
            """
            from .Graphics import Graphics
            layout = self.base_theme | self.get_axes_theme()
            others = {

            }
            for subspec in self.spec:
                for obj_type,opts in subspec.items():
                    template_props, other_props = PlotlyBackend.remap_property(obj_type, opts)
                    layout = dev.merge_dicts(layout, template_props)
                    others = dev.merge_dicts(others, other_props)
            return layout, others

        @classmethod
        def current_theme(cls):
            """
            **LLM Docstring**

            Return the current theme (Plotly backend).

            """
            if len(cls.theme_stack) == 0:
                return 'plotly'
            else:
                return cls.theme_stack[-1]

        def begin_context(self):
            """
            **LLM Docstring**

            Enter the context, applying the theme.

            """
            self.theme_stack.append(self.prep_spec())

        def end_context(self, exc_type, exc_val, exc_tb):
            """
            **LLM Docstring**

            Exit the context, restoring the previous theme.

            :param exc_type: the exception type, if any
            :param exc_val: the exception value, if any
            :param exc_tb: the traceback, if any
            """
            self.theme_stack.pop()

    def show_figure(self, graphics:PlotlyFigure, reshow=None):
        """
        **LLM Docstring**

        Display a figure via the backend (Plotly backend).

        :param graphics: the `graphics`
        :param reshow: force a reshow of an already-shown figure
        """
        if not graphics.shown:
            widg = graphics.to_widget()
            graphics.shown = True
            return widg.display()

    def get_interactive_status(self) -> 'bool':
        """
        **LLM Docstring**

        Return whether interactive mode is on (Plotly backend).

        :return: the result
        """
        return True
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
        return []


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
        if zaxis is None:
            zaxis = self.base_axis_theme
        super().__init__(
            elements=elements,
            zaxis=zaxis,
            **opts
        )
        self.zaxis = self.get_zaxis_manager()

    def get_zaxis_manager(self):
        """
        **LLM Docstring**

        Build the z-axis tick manager for this axes (Plotly backend).

        :return: the result
        """
        return ZAxisManager(
            self.get_zticks,
            self.set_zticks,
            None,
            None,
            None,
            None
        )

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
        return self.opts.get('aspectratio')
    def set_box_aspect(self, br, **kwargs):
        """
        **LLM Docstring**

        Set the 3D box aspect ratios (Plotly backend).

        :param br: the box aspect ratios
        :param kwargs: extra keyword options
        """
        if isinstance(br, str):
            self.opts['aspectmode'] = br
        else:
            self.opts['aspectmode'] = 'manual'
            self.opts['aspectratio'] = dict(zip(['x','y','z'], br), **kwargs)

    def get_frame_visible(self):
        """
        **LLM Docstring**

        Return which frame (spine) edges are drawn (Plotly backend).

        :return: the result
        """
        return (
            (
                self.opts.get('yaxis', {}).get('showline', True)
                and self.opts.get('yaxis', {}).get('side', 'left') == 'left',
                self.opts.get('yaxis', {}).get('showline', True)
                and (self.opts.get('yaxis', {}).get('mirror', False)
                     or self.opts.get('yaxis', {}).get('side', 'left') == 'right'),
            ),
            (
                self.opts.get('xaxis', {}).get('showline', True)
                and self.opts.get('xaxis', {}).get('side', 'bottom') == 'bottom',
                self.opts.get('xaxis', {}).get('showline', True)
                and (self.opts.get('xaxis', {}).get('mirror', False)
                     or self.opts.get('xaxis', {}).get('side', 'bottom') == 'top'),
            ),
            (
                self.opts.get('zaxis', {}).get('showline', True)
                and self.opts.get('zaxis', {}).get('side', 'left') in {'left', 'bottom'},
                self.opts.get('zaxis', {}).get('showline', True)
                and (self.opts.get('zaxis', {}).get('mirror', False)
                     or self.opts.get('zaxis', {}).get('side', 'left') in {'left', 'bottom'}),
            )
        )
    def set_frame_visible(self, frame_spec):
        """
        **LLM Docstring**

        Set which frame (spine) edges are drawn (Plotly backend).

        :param frame_spec: the per-edge visibility spec
        """
        if frame_spec is True or frame_spec is False:
            frame_spec = (frame_spec, frame_spec, frame_spec)
        lr, bt, xy = frame_spec
        if lr in {True, False}:
            l,r = lr,lr
        else:
            l,r = lr
        if bt in {True, False}:
            b,t = bt,bt
        else:
            b,t = bt
        if xy in {True, False}:
            x,y = xy,xy
        else:
            x,y = xy
        if l:
            if r:
                self.opts['yaxis'] = self.opts.get('yaxis', {}) | {'showline': True, 'linecolor':'black', 'mirror':True}
            else:
                self.opts['yaxis'] = self.opts.get('yaxis', {}) | {'showline': True, 'linecolor':'black'}
        elif r:
            self.opts['yaxis'] = self.opts.get('yaxis', {}) | {'showline': True, 'linecolor':'black', 'side':'right'}
        elif l is not None:
            self.opts['yaxis'] = self.opts.get('yaxis', {}) | {'showline': False, 'tickvals':[], 'title_text':""}
        if b:
            if t:
                self.opts['xaxis'] = self.opts.get('xaxis', {}) | {'showline': True, 'linecolor':'black', 'mirror':True}
            else:
                self.opts['xaxis'] = self.opts.get('xaxis', {}) | {'showline': True, 'linecolor':'black'}
        elif t:
            self.opts['xaxis'] = self.opts.get('xaxis', {}) | {'showline': True, 'linecolor':'black', 'side':'top'}
        elif b is not None:
            self.opts['xaxis'] = self.opts.get('xaxis', {}) | {'showline': False, 'tickvals':[], 'title_text':""}
        if x:
            if y:
                self.opts['zaxis'] = self.opts.get('zaxis', {}) | {'showline': True, 'linecolor':'black', 'mirror':True}
            else:
                self.opts['zaxis'] = self.opts.get('zaxis', {}) | {'showline': True, 'linecolor':'black'}
        elif y:
            self.opts['zaxis'] = self.opts.get('zaxis', {}) | {'showline': True, 'linecolor':'black', 'side':'left'}
        elif x is not None:
            self.opts['zaxis'] = self.opts.get('zaxis', {}) | {'showline': False, 'tickvals':[], 'title_text':""}

    def get_frame_style(self):
        """
        **LLM Docstring**

        Return the frame (spine) styling (Plotly backend).

        :return: the result
        """
        raise NotImplementedError(...)
    def set_frame_style(self, frame_spec):
        """
        **LLM Docstring**

        Set the frame (spine) styling (Plotly backend).

        :param frame_spec: the frame styling
        """
        (l, r), (b, t), (x, y) = frame_spec
        if l:
            self.opts['yaxis'] = self.opts.get('yaxis', {}) | l
        if r:
            self.opts['yaxis2'] = self.opts.get('yaxis2', {}) | r
        if b:
            self.opts['xaxis'] = self.opts.get('xaxis', {}) | b
        if t:
            self.opts['xaxis2'] = self.opts.get('xaxis2', {}) | t
        if x:
            self.opts['zaxis'] = self.opts.get('zaxis', {}) | x
        if y:
            self.opts['zaxis2'] = self.opts.get('zaxis2', {}) | y

    def get_plot_range(self):
        """
        **LLM Docstring**

        Return the plotted data range (Plotly backend).

        :return: the result
        """
        xrange, yrange = super().get_plot_range()
        min_z = None
        max_z = None
        for e in self.elements:
            if 'z' in e:
                if min_z is None:
                    min_z = np.min(e['z'])
                else:
                    min_z = min([min_z, np.min(e['z'])])
                if max_z is None:
                    max_z = np.max(e['z'])
                else:
                    max_z = max([max_z, np.max(e['z'])])
        zrange = [min_z, max_z]
        if zrange == [None, None]:
            zrange = None
        return xrange, yrange, zrange

    def get_zlabel(self):
        """
        **LLM Docstring**

        Return the z-axis label (Plotly backend).

        :return: the result
        """
        return self.opts.get('zaxis', {}).get('title_text')
    def set_zlabel(self, val, **style):
        """
        **LLM Docstring**

        Set the z-axis label (Plotly backend).

        :param val: the label text
        :param style: label styling options
        """
        self.opts['zaxis'] = self.opts.get('zaxis', {}) | dict(
            title_text=val,
            **style
        )

    def get_zlim(self):
        """
        **LLM Docstring**

        Return the z-axis limits (Plotly backend).

        :return: the result
        """
        zrange = self.opts.get('zaxis', {}).get('range')
        if zrange is None:
            zrange = self.get_plot_range()[2]
        return zrange
    def set_zlim(self, val, **opts):
        """
        **LLM Docstring**

        Set the z-axis limits (Plotly backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        self.opts['zaxis'] = self.opts.get('zaxis', {}) | dict(
            range=val,
            **opts
        )
    def get_zticks(self):
        """
        **LLM Docstring**

        Return the z-axis tick locations (Plotly backend).

        :return: the result
        """
        return self.opts.get('zaxis', {}).get('tickvals')
    def set_zticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the z-axis tick locations (Plotly backend).

        :param val: the tick locations
        :param opts: extra options
        """
        if isinstance(val, self.TicksManager.FixedLocator):
            val = val.locs
        self.opts['zaxis'] = self.opts.get('zaxis', {}) | dict(
            tickvals=val,
            tickmode='array',
            **opts
        )
    def get_ztick_style(self):
        """
        **LLM Docstring**

        Return the z-axis tick styling (Plotly backend).

        :return: the result
        """
        return {
            k:v
            for k,v in self.opts.get('zaxis', {}).items()
            if k.startswith('tick') or k.startswith('minor')
        }
    def set_ztick_style(self, **opts):
        """
        **LLM Docstring**

        Set the z-axis tick styling (Plotly backend).

        :param opts: extra options
        """
        self.opts['zaxis'] = self.opts.get('zaxis', {}) | opts

    def get_view_settings(self):
        """
        **LLM Docstring**

        Return the 3D camera/view settings (Plotly backend).

        :return: the result
        """
        return self.opts.get('scene_camera', {})

    default_up_vector = (0, 0, 1)
    default_right_vector = (0, 1, 0)
    default_view_vector = (1, 0, 0)
    def set_view_settings(self,
                          up=None, eye=None, center=None,
                          vertical_axis=None,
                          up_vector=None, right_vector=None, view_vector=None, view_distance=None,
                          view_matrix=None, view_center=None):
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

        if view_matrix is None and  (
                view_vector is not None
                or right_vector is not None
                or up_vector is not None
        ):
            if view_vector is None:
                if (
                        up_vector is not None and right_vector is not None
                ):
                    view_vector = nput.vec_crosses(up_vector, right_vector, normalize=True)
                elif right_vector is not None:
                    view_vector = nput.vec_crosses(self.default_up_vector, right_vector, normalize=True)
                elif up_vector is not None:
                    view_vector = nput.vec_crosses(up_vector, self.default_right_vector, normalize=True)

            if view_vector is not None:
                m = nput.rotation_matrix(
                    view_vector,
                    self.default_view_vector
                )
            else:
                m = np.eye(3)

            if up_vector is None and right_vector is not None:
                if view_vector is None:
                    view_vector = self.default_view_vector
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
                    self.default_up_vector
                )
            view_matrix = m

        camera = {}
        if up is not None:
            camera['up'] = up
        if eye is not None:
            camera['eye'] = eye
        if center is not None:
            camera['center'] = center
        if view_matrix is not None:
            # roll, cross = nput.extract_rotation_angle_axis(view_matrix)
            view_vector, up_vector, right_vector = view_matrix.T
            if view_distance is None:
                view_distance = np.sqrt(25 / 16 * 3)
            if view_center is not None:
                camera['center'] = dict(zip('xyz', view_center)) if center is None else center
            view_axis = view_vector * view_distance
            camera = camera | {
                'up':dict(zip('xyz', up_vector)) if up is None else up,
                'eye': dict(zip('xyz', view_axis + camera.get('center', np.zeros(3)))) if eye is None else eye
            }
        elif view_distance is not None:
            if view_center is not None:
                camera['center'] = dict(zip('xyz', view_center)) if center is None else center
            view_axis = np.array([view_distance, view_distance, view_distance])
            camera = camera | {
                'eye': dict(zip('xyz', view_axis + camera.get('center', np.zeros(3)))) if eye is None else eye
            }

        if view_center is not None:
            camera['center'] = dict(zip('xyz', view_center)) if center is None else center

        if len(camera) > 0:
            self.opts['scene_camera'] = camera

    def plot(self, x, y, z, line=None,  type='scatter3d', **opts):
        """
        **LLM Docstring**

        Add a 3D line trace to the axes (a Plotly `scatter3d` trace).

        :param args: the trace data
        :param opts: trace options
        :return: the trace dict
        :rtype: dict
        """
        return super().plot(x, y, z=z, type=type, line=line, **opts)
    def scatter(self, x, y, z, line=None, type='scatter3d',
                marker=None,
                edge_color=None,
                size=None,
                line_width=None,
                **opts):
        """
        **LLM Docstring**

        Add a 3D marker (scatter) trace to the axes.

        :param args: the trace data
        :param opts: trace options
        :return: the trace dict
        :rtype: dict
        """
        marker_line_props = {k:v for k,v in dict(width=line_width, color=edge_color).items() if v is not None}
        if len(marker_line_props) > 0:
            if marker is None: marker = {}
            marker['line'] = marker_line_props | marker.pop('line', {})
        if size is not None:
            if marker is None: marker = {}
            marker['size'] = marker.get('size', size)
        return super().scatter(x, y, z=z, type=type, line=line, marker=marker, **opts)
    def text(self, text, x, y, z, line=None,  type='scatter3d', **opts):
        """
        **LLM Docstring**

        Add a 3D text trace to the axes.

        :param args: the trace data
        :param opts: trace options
        :return: the trace dict
        :rtype: dict
        """
        return super().text(text, x, y, z=z, type=type, line=line, **opts)

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
        verts = np.asanyarray(verts)
        if indices is not None:
            indices = np.asanyarray(indices)
            plot_dict = dict(type=type,
                             x=verts[:, 0], y=verts[:, 1], z=verts[:, 2],
                             i=indices[:, 0], j=indices[:, 1], k=indices[:, 2], **opts)
        else:
            plot_dict = dict(type=type,
                             x=verts[:, 0], y=verts[:, 1], z=verts[:, 2], **opts)
        self.elements.append(plot_dict)
        return plot_dict
    def draw_poly(self, points, flatshading=True, **styles):
        """
        **LLM Docstring**

        Draw a filled polygon from the given points (Plotly backend).

        :param points: the points to draw
        :param flatshading: the `flatshading`
        :param styles: the styling options
        """
        indices = nput.triangulate_polygon(points)
        return self.mesh(points, indices, flatshading=flatshading, **styles)
    def draw_sphere(self, center, radius,
                    sphere_points=48,
                    rendering='flat',
                    s=None,
                    box_scalings=None,
                    edgecolors=None,
                    edge_color=None,
                    lw=None,
                    edge_width=.01,
                    glow=None,
                    color='white',
                    default_view_distance='auto',
                    **opts):
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
        if dev.str_is(rendering, 'flat'):
            if glow is not None:
                if color is None:
                    color = glow
                else:
                    color = ColorPalette.prep_color(palette=[glow, color], blending=.5)

            eye = self.get_view_settings().get('eye')
            if eye is not None and default_view_distance is not None:
                view_distance = np.linalg.norm([eye[x] for x in ['x', 'y', 'z']])
                if dev.str_is(default_view_distance, 'auto'):
                    default_view_distance = np.sqrt(25 / 16 * 3)
                view_distance_scaling = default_view_distance / view_distance
            else:
                view_distance_scaling = 1


            center = np.asanyarray(center)
            if center.ndim == 1:
                center = center[np.newaxis]
            if edgecolors is None:
                if edge_color is not None:
                    edgecolors = edge_color
                else:
                    edgecolors = [[0.] * 3 + [.3]]
            if isinstance(edgecolors, str) or nput.is_numeric(edgecolors[0]):
                edgecolors = [edgecolors] * len(center)
            if isinstance(color, str) or nput.is_numeric(color[0]):
                color = [color] * len(center)
            if s is None:
                if box_scalings is None:
                    box_scalings = [1, 1, 1]
                s = (radius * max(box_scalings) * 72)**2
            if lw is None:
                if box_scalings is None:
                    box_scalings = [1, 1, 1]
                lw = (edge_width * max(box_scalings) * 72)

            if nput.is_numeric(s):
                s = [s] * len(center)

            # if box_scalings is None:
            #     box_scalings = [1, 1, 1]
            sizes = view_distance_scaling * np.sqrt(s) / 2 #/ (72 * max(box_scalings))
            line_width = view_distance_scaling * lw / 2 #/ (72 * max(box_scalings))
            spheres = []
            if lw is not None:
                spheres += [
                    self.get_plotter('scatter')(
                        [cent[0]], [cent[1]], [cent[2]],
                        color=ec,
                        size=sz + line_width,
                        **opts
                    )
                    for (cent, ec, sz, c) in zip(
                    center, edgecolors, sizes, color
                )
                ]
            spheres += [
                self.get_plotter('scatter')(
                    [cent[0]], [cent[1]], [cent[2]],
                    color=c,
                    size=sz,
                    **opts
                )
                for (cent, ec, sz, c) in zip(
                    center, edgecolors, sizes, color
                )
            ]
            # dists = (np.sqrt(areas) / (max(box_scalings) * 72)) / 10
            # spheres.zdist_offset = functools.partial(self._get_sphere_proj, radius=np.max(dists))
            # spheres.predraw = functools.partial(self._flat_sphere_predraw,
            #                                     spheres,
            #                                     radius=dists * 10,
            #                                     depth_shading_range=depth_shading_range,
            #                                     depth_shading_targets=depth_shading_targets,
            #                                     depth_shrink_range=depth_shrink_range,
            #                                     depth_shrink_targets=depth_shrink_targets)
            return spheres
        else:
            surface = self.get_plotter('mesh3d')

            u = np.linspace(0, 2 * np.pi, sphere_points)
            v = np.linspace(0, np.pi, sphere_points)
            x = radius * np.outer(np.cos(u), np.sin(v))
            y = radius * np.outer(np.sin(u), np.sin(v))
            z = radius * np.outer(np.ones(np.size(u)), np.cos(v))

            return surface(x + center[0], y + center[1], z + center[2], color=color, **opts)
    def draw_cylinder(self, start, end, rad, circle_points=48,
                      rendering='flat',
                      box_scalings=None,
                      edge_color=None,
                      color='black',
                      glow=None,
                      segments=1,
                      segment_overdraw=0,
                      edge_width=.01,
                      lw=None,
                      color_cycle=False,
                      layer='above',
                      # capstyle='butt',
                      default_view_distance='auto',
                      **opts):
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
        if glow is not None:
            if color is None:
                color = glow
            else:
                color = ColorPalette.prep_color(palette=[glow, color], blending=.5)
        if dev.str_is(rendering, 'flat'):
            eye = self.get_view_settings().get('eye')
            if eye is not None and default_view_distance is not None:
                view_distance = np.linalg.norm([eye[x] for x in ['x', 'y', 'z']])
                if dev.str_is(default_view_distance, 'auto'):
                    default_view_distance = np.sqrt(25 / 16 * 3)
                view_distance_scaling = default_view_distance / view_distance
            else:
                view_distance_scaling = 1

            start = np.asanyarray(start)
            if start.ndim == 1:
                start = start[np.newaxis]
            end = np.asanyarray(end)
            if end.ndim == 1:
                end = end[np.newaxis]
            plot = self.get_plotter('plot')
            if lw is None:
                rad = np.asanyarray(rad)
                if rad.ndim == 0:
                    rad = np.array([rad])
                if box_scalings is None:
                    box_scalings = [1, 1, 1]
                lw = rad * 72 * max(box_scalings)
            if edge_color is None:
                edge_color = [None] * len(start)
            elif isinstance(edge_color, str) or nput.is_numeric(edge_color[0]):
                edge_color = [edge_color] * len(start)
            if isinstance(color, str) or nput.is_numeric(color[0]):
                color = [color] * len(start)

            coll = []
            if color_cycle is True:
                color_cycle = ["red", "blue", "green", "orange", "purple"]
            ew = edge_width * (72 * max(box_scalings))
            lw = lw * view_distance_scaling
            ew = ew * view_distance_scaling
            for s, e, w, ec, c in zip(start, end, lw, edge_color, color):
                cw = w / (72 * max(box_scalings))
                v, n = nput.vec_normalize(e - s, return_norms=True)
                # s = s - cw * v
                # e = e + cw * v
                d = np.linspace(0, n, segments+1)
                x_points, y_points, z_points = (s[np.newaxis] + v[np.newaxis] * d[:, np.newaxis]).T
                if segment_overdraw > 0:
                    d = d + (n * segment_overdraw)
                    # d[-1] = n
                    x2_points, y2_points, z2_points = (s[np.newaxis] + v[np.newaxis] * d[1:, np.newaxis]).T
                else:
                    x2_points, y2_points, z2_points = x_points[1:], y_points[1:], z_points[1:]
                for i,(x1,y1,z1,x2,y2,z2) in enumerate(zip(
                    x_points[:-1],y_points[:-1],z_points[:-1],
                    x2_points, y2_points, z2_points
                )):
                    if color_cycle:
                        c = color_cycle[i%len(color_cycle)]
                    coll.append(
                        plot(
                            [x1, x2],
                            [y1, y2],
                            [z1, z2],
                            width=w+ew,
                            color=ec,
                            **opts
                        )
                    )
            for s, e, w, ec, c in zip(start, end, lw, edge_color, color):
                cw = w / (72 * max(box_scalings))
                v, n = nput.vec_normalize(e - s, return_norms=True)
                # s = s - cw * v
                # e = e + cw * v
                d = np.linspace(0, n, segments+1)
                x_points, y_points, z_points = (s[np.newaxis] + v[np.newaxis] * d[:, np.newaxis]).T
                if segment_overdraw > 0:
                    d = d + (n * segment_overdraw)
                    # d[-1] = n
                    x2_points, y2_points, z2_points = (s[np.newaxis] + v[np.newaxis] * d[1:, np.newaxis]).T
                else:
                    x2_points, y2_points, z2_points = x_points[1:], y_points[1:], z_points[1:]
                for i,(x1,y1,z1,x2,y2,z2) in enumerate(zip(
                    x_points[:-1],y_points[:-1],z_points[:-1],
                    x2_points, y2_points, z2_points
                )):
                    if color_cycle:
                        c = color_cycle[i%len(color_cycle)]
                    coll.append(
                        plot(
                            [x1, x2],
                            [y1, y2],
                            [z1, z2],
                            width=w,
                            color=c,
                            # solid_capstyle=capstyle,
                            # path_effects=(
                            #     [pe.Stroke(linewidth=w+ew, foreground=ec, capstyle='butt'), pe.Normal()]
                            #         if ec is not None and ew > 0 else
                            #     None
                            # ),
                            **opts
                        )
                    )
            return coll
        else:
            surface = self.get_plotter('mesh3d')

            u = np.linspace(0, 2 * np.pi, circle_points)
            v = np.linspace(0, np.pi, circle_points)

            # pulled from SO: https://stackoverflow.com/a/32383775/5720002

            # vector in direction of axis
            v = end - start
            # find magnitude of vector
            mag = np.linalg.norm(v)
            # unit vector in direction of axis
            v = v / mag
            # make some vector not in the same direction as v
            not_v = np.array([1, 0, 0])
            if (v == not_v).all():
                not_v = np.array([0, 1, 0])
            # make vector perpendicular to v
            n1 = np.cross(v, not_v)
            # normalize n1
            n1 /= np.linalg.norm(n1)
            # make unit vector perpendicular to v and n1
            n2 = np.cross(v, n1)
            # surface ranges over t from 0 to length of axis and 0 to 2*pi
            t = np.linspace(0, mag, circle_points)
            theta = np.linspace(0, 2 * np.pi, circle_points)
            # use meshgrid to make 2d arrays
            t, theta = np.meshgrid(t, theta)
            # generate coordinates for surface
            X, Y, Z = [start[i] + v[i] * t + rad * np.sin(theta) * n1[i] + rad * np.cos(theta) * n2[i] for i
                       in [0, 1, 2]]

            return surface(X, Y, Z, color=color, **opts)
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
        # in angles b.c. copied from mpl
        start_angle_rad = np.deg2rad(theta1)
        end_angle_rad = np.deg2rad(theta2)
        if angular_density is None:
            angular_density = 72/(2*np.pi)
        npoints = angular_density * (end_angle_rad - start_angle_rad)
        angles = np.linspace(start_angle_rad, end_angle_rad, int(np.ceil(npoints)))
        points = np.array([radius * np.cos(angles), radius * np.sin(angles), np.zeros(len(angles))]).T
        points = center[np.newaxis] + np.reshape(
            points[:, np.newaxis, :] @ nput.rotation_matrix([0, 0, 1], zdir)[np.newaxis],
            (-1, 3)
        )
        return points

    def draw_disk(self, centers, radius=None, angle=None,
                  normal=None, uv_axes=None, zdir=None,
                  theta1=None, theta2=None,
                  rendering='flat', box_scalings=None,
                  line_color=None, line_thickness=None,
                  color=None,
                  glow=None,
                  lw=None,
                  **styles):
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
        # patches = MPLManager.patch_api()
        # paths = MPLManager.path_api()
        # coll = MPLManager.collections_api()
        centers = np.asanyarray(centers)
        if centers.ndim == 1:
            centers = centers[np.newaxis]

        if rendering != 'flat':
            raise NotImplementedError(f'arc rendering {rendering}')

        if glow is not None:
            if color is None:
                color = glow
            else:
                color = ColorPalette.prep_color(palette=[glow, color], blending=.5)

        if uv_axes is not None:
            u, v = uv_axes
            base_ang, base_norm = nput.vec_angles(u, v, return_crosses=True)
            base_norm = nput.vec_normalize(base_norm)
            if normal is None:
                normal = base_norm
            angs, crosses, cns = nput.vec_angles([0, 0, 1], normal, return_crosses=True, return_cross_norms=True)
            if cns < 1e-6:
                embedding_axes = np.eye(3)
            else:
                embedding_axes = nput.rotation_matrix(crosses, angs)
            emb_u, emb_v = np.array([u, v]) @ embedding_axes
            emb_z = np.cross(emb_u, emb_v)
            emb_angle = np.arctan2(emb_u[1], emb_u[0])
            if emb_z[2] < 0:
                emb_angle = -emb_angle
            if theta1 is None:
                theta1 = np.rad2deg(emb_angle)
            if theta2 is None:
                theta2 = np.rad2deg(emb_angle + angle)
        if zdir is None:
            zdir = normal

        if theta1 is None or nput.is_numeric(theta1):
            theta1 = [theta1] * len(centers)
        if theta2 is None or nput.is_numeric(theta2):
            theta2 = [theta2] * len(centers)
        if radius is None or nput.is_numeric(radius):
            radius = [radius] * len(centers)
        if isinstance(zdir, str) or zdir is None or nput.is_numeric(zdir[0]):
            zdir = [zdir] * len(centers)
        if isinstance(line_color, str) or line_color is None:
            line_color = [line_color] * len(centers)
        if lw is None:
            if box_scalings is None:
                box_scalings = [1, 1, 1]
            if line_thickness is None or nput.is_numeric(line_thickness):
                line_thickness = [line_thickness] * len(centers)
            lw = np.asanyarray(line_thickness) * 72 * max(box_scalings)
        if lw is None or nput.is_numeric(lw):
            lw = [lw] * len(centers)
        if isinstance(color, str) or color is None:
            color = [color] * len(centers)

        arcs = []

        for c,r,t1,t2,zd,col,lc,w in zip(centers, radius, theta1, theta2, zdir,
                                       color, line_color,lw):
            if col is None:
                pts = self._get_arc_points(c, zd, r, t1, t2).T
                a = self.plot(*pts, color=lc, width=w)
            else:
                raise NotImplementedError(...)
            arcs.append(a)

        return arcs

    def draw_text(self, points, vals, billboard=True, normal=None, rendering='flat',
                  box_scalings=None, zdir=None,
                  **styles):
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
        points = np.asanyarray(points)
        if points.ndim == 1:
            points = points[np.newaxis]
            vals = [vals]
        return self.text(vals, *points.T, **styles)

    def draw_rect(self, points, rotation=None, normal=None, **styles):
        """
        **LLM Docstring**

        Draw a rectangle from the given points (Plotly backend).

        :param points: the points to draw
        :param rotation: the `rotation`
        :param normal: the `normal`
        :param styles: the styling options
        """
        points = np.asanyarray(points)
        if normal is None:
            ax = points[1] - points[0]
            normal = nput.vec_normalize(nput.project_out([0, 0, 1], ax[:, np.newaxis]))
        rot = nput.rotation_normal_view_matrix(rotation, normal)
        eps = points @ rot
        (x1, y1, z1), (x2, y2, z2) = eps
        w = x2 - x1
        h = y2 - y1
        mesh_points = np.array(
            [
                [0, 0, 0],
                [0, h, 0],
                [w, h, 0],
                [w, 0, 0]
            ]
        ) @ rot.T + points[0][np.newaxis]
        return self.draw_poly(mesh_points, **styles)

    def draw_line(self, points,
                  line_thickness=None,
                  width=None,
                  s=None,
                  edgecolors=None,
                  box_scalings=None, **styles):
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
        if width is None:
            if line_thickness is not None:
                if box_scalings is None:
                    box_scalings = [1, 1, 1]
                # if radius is None or nput.is_numeric(radius):
                #     radius = [radius] * len(centers)
                width = np.asanyarray(line_thickness) * 72 * max(box_scalings)
        return super().draw_line(points, width=width, **styles)

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
        x,y,z = points.T
        opts = dict(
            x=x,
            y=y,
            z=z,
            i=i,
            j=j,
            k=k,
            type=type
        ) | styles
        mesh_params = {k:v for k,v in opts.items() if v is not None}
        self.elements.append(mesh_params)
        return mesh_params
    def draw_arrow(self, points, radius, width=None, arrowhead=None,
                   arrowhead_scaling=1.2, arrowhead_points=None, normal=None,
                   rendering='flat',
                   box_scalings=None,
                   **styles):
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
        points = np.asanyarray(points)
        if width is None:
            if box_scalings is None:
                box_scalings = [1, 1, 1]
            # if radius is None or nput.is_numeric(radius):
            #     radius = [radius] * len(centers)
            width = np.asanyarray(radius) * 72 * max(box_scalings)
        if arrowhead is None:
            arrowhead = np.asanyarray(radius) * arrowhead_scaling * max(box_scalings)
        line_params = self.draw_line(points, width=width, **styles)
        if arrowhead_points is None:
            ax = nput.vec_normalize(points[-1] - points[-2])
            if normal is None:
                normal = [0, 0, 1]
            if np.dot(normal, ax) == 1:
                normal = [1, 0, 0]
            right = nput.vec_crosses(ax, normal, normalize=True)
            tf = np.array([
                ax,
                right,
                normal
            ])
            arrowhead_points = arrowhead * np.array([
                [0, -1/2, 0],
                [0,  1/2, 0],
                [np.sqrt(3)/2, 0, 0]
            ]) @ tf
        arrow_points = points[-1][np.newaxis] + arrowhead_points
        mesh_params = self.draw_mesh(arrow_points, i=[0], j=[1], k=[2], **styles)
        return [line_params, mesh_params]
    # fig = go.Figure(data=[go.Scatter3d(
    #     x=[1, 2, 3],
    #     y=[2, 1, 3],
    #     z=[3, 2, 1],
    #     mode='markers+text',
    #     text=['Label A', 'Label B', 'Label C'],
    #     textposition='top center',
    #     marker=dict(size=8)
    # )])
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
        template = layout.pop('template', None)
        if template is not None:
            if 'layout' in template:
                template['layout'] = cls._prep_layout_props(template['layout'])
            layout['template'] = template

        scene = layout.pop('scene', {})
        for lab in cls.scene_props:
            if lab in layout:
                base_prop = layout.pop(lab)
                if isinstance(base_prop, dict):
                    scene[lab] = {
                        k: v for k, v in base_prop.items()
                        if v is not None and k not in cls.omitted_tick_properties
                    }
                else:
                    scene[lab] = base_prop
        if len(scene) > 0:
            layout['scene'] = scene

        return layout
class PlotlyBackend3D(PlotlyBackend):
    Figure = PlotlyFigure3D

    axes_props = {'xtick':'xaxis', 'ytick':'yaxis', 'ztick':'zaxis'}
    class ThemeContextManager(PlotlyBackend.ThemeContextManager):
        def get_axes_theme(self):
            """
            **LLM Docstring**

            Return the axes theme (Plotly backend).

            :return: the result
            """
            return {
                'xaxis': self.base_axis_theme,
                'yaxis': self.base_axis_theme,
                'zaxis': self.base_axis_theme,
            }

class GraphicsRegionAxes(GraphicsAxes):
    def __init__(self, figure_region):
        """
        **LLM Docstring**

        Wrap a figure region as an axes, mapping data coordinates into that region.

        :param figure_region: the target region (per-axis `(min, max)` extents)
        """
        self.region = figure_region

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
        o_min, o_max = og_reg
        pos = (pos - o_min) / (o_max - o_min)
        if final_reg is not None:
            F_min, F_max = final_reg
            pos = pos * (F_max - F_min) + F_min
        return pos

    def normalize_positions(self, pos):
        """
        **LLM Docstring**

        Map data-coordinate positions into the axes' figure region (per axis).

        :param pos: the positions, shape `(..., ndim)`
        :type pos: np.ndarray
        :return: the region-normalized positions
        :rtype: np.ndarray
        """
        ndim = pos.shape[-1]

        x = self.renormalize(pos[..., 0], self.get_xlim(), self.region[0])
        y = self.renormalize(pos[..., 1], self.get_ylim(), self.region[1])
        if ndim == 2:
            z = self.renormalize(pos[..., 2], self.get_zlim(), self.region[2])
            crds = [x, y, z]
        else:
            crds = [x, y]
        return np.moveaxis(np.array(crds), 0, -1)

class SVGAxes(GraphicsAxes):
    def __init__(self,
                 base_fig=None,
                 label_text=None,
                 frame=None,
                 prop_cycle=None
                 ):
        """
        **LLM Docstring**

        Set up an SVG axes wrapping an `SVGFigure`, with a frame, label, and style cycle.

        :param base_fig: the backing SVG figure (created if omitted)
        :param label_text: the axes label
        :param frame: the frame specification
        :param prop_cycle: the per-series style cycle
        """
        if base_fig is None:
            base_fig = svg.SVGFigure()
        self.figure = base_fig
        self.frame = frame
        self.label_text = label_text
        self.prop_cyle = prop_cycle
        super().__init__()

    def remove(self, *, backend):
        """
        **LLM Docstring**

        Tear down (remove) this axes from its figure (SVG backend).

        """
        raise NotImplementedError(f"remove doesn't make sense for SVG")
    def clear(self, *, backend):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (SVG backend).

        """
        self.figure = svg.SVGFigure()

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
        return self.label_text
    def set_plot_label(self, val, **style):
        """
        **LLM Docstring**

        Set the plot title/label (SVG backend).

        :param val: the label text
        :param style: label styling options
        """
        self.label_text = (val, style)

    def get_style_list(self):
        """
        **LLM Docstring**

        Return the per-series style cycle (SVG backend).

        :return: the result
        """
        return self.prop_cyle
    def set_style_list(self, props):
        """
        **LLM Docstring**

        Set the per-series style cycle (SVG backend).

        :param props: the style cycle
        """
        self.prop_cyle = props

    def get_frame_visible(self):
        """
        **LLM Docstring**

        Return which frame (spine) edges are drawn (SVG backend).

        :return: the result
        """
        return False if self.frame else self.frame
    def set_frame_visible(self, frame_spec):
        """
        **LLM Docstring**

        Set which frame (spine) edges are drawn (SVG backend).

        :param frame_spec: the per-edge visibility spec
        """
        self.frame = frame_spec

    def get_frame_style(self):
        """
        **LLM Docstring**

        Return the frame (spine) styling (SVG backend).

        :return: the result
        """
        return self.frame_style
    def set_frame_style(self, frame_spec):
        """
        **LLM Docstring**

        Set the frame (spine) styling (SVG backend).

        :param frame_spec: the frame styling
        """
        self.frame_style = frame_spec

    def get_xlabel(self):
        """
        **LLM Docstring**

        Return the x-axis label (SVG backend).

        :return: the result
        """
        return self.x_label
    def set_xlabel(self, val, **style):
        """
        **LLM Docstring**

        Set the x-axis label (SVG backend).

        :param val: the label text
        :param style: label styling options
        """
        self.x_label = (val, style)

    def get_ylabel(self):
        """
        **LLM Docstring**

        Return the y-axis label (SVG backend).

        :return: the result
        """
        return self.y_label
    def set_ylabel(self, val, **style):
        """
        **LLM Docstring**

        Set the y-axis label (SVG backend).

        :param val: the label text
        :param style: label styling options
        """
        self.y_label = (val, style)

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
        vb = self.figure.view_box
        if vb is None:
            vb = self.figure.compute_viewbox()
        if vb is None:
            vb = [(None, None)] * self.num_axes
        return vb[axis]
    def set_limit(self, axis, lims):
        """
        **LLM Docstring**

        Set one axis's limits in the SVG figure's view box.

        :param axis: the axis index
        :type axis: int
        :param lims: the `(min, max)` limits
        """
        vb = self.figure.view_box
        just_axis = vb is None
        if just_axis:
            vb = self.figure.compute_viewbox()
        if just_axis:
            vb = [(None, None),] * self.num_axes
        else:
            vb = list(vb)
        vb[axis] = lims
        self.figure.view_box = tuple(tuple(v) for v in vb)
    def get_xlim(self):
        """
        **LLM Docstring**

        Return the x-axis limits (SVG backend).

        :return: the result
        """
        return self.get_limit(0)
    def set_xlim(self, val, **opts):
        """
        **LLM Docstring**

        Set the x-axis limits (SVG backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        self.set_limit(0, val)

    def get_ylim(self):
        """
        **LLM Docstring**

        Return the y-axis limits (SVG backend).

        :return: the result
        """
        return self.get_limit(1)
    def set_ylim(self, val, **opts):
        """
        **LLM Docstring**

        Set the y-axis limits (SVG backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        self.set_limit(1, val)

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
        raise NotImplementedError("ticks not implemented for SVG")
    def set_xtick_style(self, **opts):
        """
        **LLM Docstring**

        Set the x-axis tick styling (SVG backend).

        :param opts: extra options
        """
        raise NotImplementedError("ticks not implemented for SVG")
    def get_ytick_style(self):
        """
        **LLM Docstring**

        Return the y-axis tick styling (SVG backend).

        :return: the result
        """
        raise NotImplementedError("ticks not implemented for SVG")
    def set_ytick_style(self, **opts):
        """
        **LLM Docstring**

        Set the y-axis tick styling (SVG backend).

        :param opts: extra options
        """
        raise NotImplementedError("ticks not implemented for SVG")

    def set_aspect_ratio(self, ar):
        """
        **LLM Docstring**

        Set the axes aspect ratio (SVG backend).

        :param ar: the aspect ratio
        """
        if ar is None or dev.str_is(ar, 'auto'):
            self.figure.kwargs.pop('aspect_ratio', None)
        else:
            self.figure.kwargs['aspect_ratio'] = ar
    def get_bbox(self):
        """
        **LLM Docstring**

        Return the axes bounding box (SVG backend).

        :return: the result
        """
        vb = self.figure.view_box
        if vb is None:
            vb = self.figure.compute_viewbox()
        return vb
    def set_bbox(self, bbox):
        """
        **LLM Docstring**

        Set the axes bounding box (SVG backend).

        :param bbox: the bounding box
        """
        self.figure.view_box = bbox
    def get_facecolor(self):
        """
        **LLM Docstring**

        Return the background/face color (SVG backend).

        :return: the result
        """
        return self.figure.kwargs.get('background')
    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color (SVG backend).

        :param fg: the face color
        """
        self.figure.kwargs['background'] = fg
    def get_padding(self):
        """
        **LLM Docstring**

        Return the axes padding (SVG backend).

        :return: the result
        """
        return self.figure.kwargs.get('margin')
    def set_padding(self, padding):
        """
        **LLM Docstring**

        Set the axes padding (SVG backend).

        :param padding: the padding
        """
        self.figure.kwargs['margin'] = padding

    def legend(self, **opts):
        """
        **LLM Docstring**

        Draw the axes legend (SVG backend).

        :param opts: legend options
        :return: the result
        """
        raise NotImplementedError("legend")

    def get_graphics_properties(self, obj, property=None):
        """
        **LLM Docstring**

        Get backend properties of a drawn graphics object (SVG backend).

        :param obj: the graphics object
        :param property: a specific property to fetch
        :return: the result
        """
        if property is None:
            return obj.styles | obj.attrs
        else:
            return obj.attrs.get(property, obj.styles.get(property))
    def set_graphics_properties(self, obj, **props):
        """
        **LLM Docstring**

        Set backend properties on a drawn graphics object (SVG backend).

        :param obj: the graphics object
        :param props: the properties to set
        """
        obj.styles.update(props)

    style_mapping = {
        'edgecolor':'stroke',
        'lw':'stroke-width',
        'color':'fill',
        'line_color':'stroke',
        'line_width':'stroke-width'
    }
    def prep_styles(self, styles):
        """
        **LLM Docstring**

        Normalize SVG styling: resolve a `glow` option into a color and remap style names.

        :param styles: the styling options
        :type styles: dict
        :return: the prepared styles
        :rtype: dict
        """
        glow = styles.pop('glow', None)
        if glow is not None:
            color = styles.pop('color')
            if color is None:
                color = glow
            else:
                color = ColorPalette.prep_color(palette=[glow, color], blending=.5)
            styles['color'] = color
        return {
            self.style_mapping.get(k, k):v
            for k,v in styles.items()
        }
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
        if line_color is None:
            line_color = color
            color = None
        styles = self.prep_styles(styles | {'line_color':line_color, 'color':color})
        if stroke is not None:
            styles['stroke'] = stroke
        points = np.asanyarray(points)
        if len(points) > 2:
            return self.figure.add_polyline(points=points, **styles)
        else:
            (x1, y1), (x2, y2) = points
            return self.figure.add_line(x1=x1, y1=y1, x2=x2, y2=y2, **styles)
    def draw_point(self, points, **styles):
        """
        **LLM Docstring**

        Draw a point (as a small disk) at the given position(s) (SVG backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        styles = self.prep_styles(styles)
        return self.draw_disk(points, **styles)
    def draw_disk(self, points, *, radius, **styles):
        """
        **LLM Docstring**

        Draw a filled disk at the given position(s) (SVG backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        styles = self.prep_styles(styles)
        x, y = np.asanyarray(points)
        return self.figure.add_circle(cx=x, cy=y, r=radius, **styles)
    def draw_rect(self, points, **styles):
        """
        **LLM Docstring**

        Draw a rectangle from the given points (SVG backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        styles = self.prep_styles(styles)
        (x1, y1), (x2, y2) = np.asanyarray(points)
        return self.figure.add_rect(x=x1, y=y1, width=x2-x1, height=y2-y1, **styles)
    def draw_triangle(self, points, **styles):
        """
        **LLM Docstring**

        Draw a triangle from the given points (SVG backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        raise NotImplementedError(...)
    def draw_poly(self, points, **styles):
        """
        **LLM Docstring**

        Draw a filled polygon from the given points (SVG backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        styles = self.prep_styles(styles)
        return self.figure.add_polygon(points=np.asanyarray(points), **styles)
    default_arrowhead = dict(
        body=svg.SVG.Path(d="M 0 0 L 10 5 L 0 10 z"),
        viewBox="0 0 10 10",
        refX="5",
        refY="5",
        markerWidth="6",
        markerHeight="6",
        orient="auto-start-reverse"
    )
    def draw_arrow(self, points, arrowhead=None, marker=None, **styles):
        """
        **LLM Docstring**

        Draw an arrow from the given points (SVG backend).

        :param points: the points to draw
        :param arrowhead: the `arrowhead`
        :param marker: the `marker`
        :param styles: the styling options
        """
        styles = self.prep_styles(styles)
        if marker is None:
            if arrowhead is None:
                arrowhead = self.default_arrowhead
            self.figure.add_def(
                "arrowhead",
                tag="marker",
                **arrowhead
            )
            marker = 'url(#arrowhead)'
        self.draw_line(points, marker=marker, **styles)

    mpl_font_map = dict(
        font_family='family',
        font_style='style',
        font_variant='variant',
        font_weight='weight',
        font_stretch='stretch',
        font_size='size',
        font_fname='fname',  # if set, it's a hardcoded filename to use
        font_math_fontfamily='math_fontfamily'
    )
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
        font_opts = {}
        rem_opts = {}
        for k,v in styles.items():
            k2 = cls.mpl_font_map.get(k)
            if k2 is None:
                rem_opts[k] = v
            else:
                font_opts[k2] = v
        return font_opts, rem_opts
    @classmethod
    def _text_to_path(cls, origin, text, invert=False, size=None, plot_range=None,
                      anchor=None,
                      font_size_scaling=13, **font_opts):
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
        from matplotlib.textpath import TextPath
        from matplotlib.font_manager import FontProperties
        from matplotlib.transforms import Affine2D
        if nput.is_numeric(size):
            scaling = size / font_size_scaling
            size = None
        else:
            scaling = None
        fp = FontProperties(size=size, **font_opts)
        path = TextPath((0, 0), text, prop=fp)
        if invert:
            tf = (
                Affine2D()
                    # .translate(tx=-origin[0], ty=-origin[1])
                    .scale(sx=1, sy=-1)
                    # .translate(tx=origin[0], ty=origin[1])
                  )
            path = tf.transform_path(path)
            origin = (origin[0], -origin[1])

        if scaling is not None:
            tf = Affine2D()
            if plot_range is not None:
                min_x = np.min(path.vertices[:, 0])
                max_x = np.max(path.vertices[:, 0])
                min_y = np.min(path.vertices[:, 1])
                max_y = np.max(path.vertices[:, 1])
                scaling = scaling / np.max([(max_y - min_y), (max_x - min_x)])
                tf = (
                    tf
                    # .translate(tx=-origin[0], ty=-origin[1])
                    .scale(sx=scaling, sy=scaling)
                    # .translate(tx=origin[0], ty=origin[1])
                )
            else:
                tf.scale(sx=scaling, sy=scaling)
            path = tf.transform_path(path)
        if anchor is not None:
            min_x = np.min(path.vertices[:, 0])
            max_x = np.max(path.vertices[:, 0])
            min_y = np.min(path.vertices[:, 1])
            max_y = np.max(path.vertices[:, 1])
            offset = (max_x - min_x) * anchor[0], (max_y - min_y)* anchor[1]
            origin = origin[0] + offset[0], origin[1] + offset[1]
        path = Affine2D().translate(tx=origin[0], ty=origin[1]).transform_path(path)

        return path
    def draw_text(self, points, vals,
                  use_path=False,
                  invert=False,
                  anchor=None,
                  plot_range=None, font_size_scaling=13, **styles):
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
        styles = self.prep_styles(styles)
        if use_path:
            font_opts, styles = self.filter_font_options(styles)
            mpl_path = self._text_to_path(points, vals,
                                          plot_range=plot_range,
                                          font_size_scaling=font_size_scaling,
                                          invert=invert,
                                          anchor=anchor,
                                          **font_opts)
            commands = svg.SVGPath.from_mpl(mpl_path)
            return self.figure.add_path(d=commands, **styles)
        else:
            x, y = points
            return self.figure.add_text(x=x, y=y, text=vals, **styles)
    def draw_path(self, commands, use_polyline=False, **styles):
        """
        **LLM Docstring**

        Draw a path from a sequence of drawing commands (SVG backend).

        :param commands: the path drawing commands
        :param use_polyline: the `use_polyline`
        :param styles: the styling options
        """
        styles = self.prep_styles(styles)
        if use_polyline:
            points = nput.parametric_path_points(commands)
            # shifts = np.concatenate([[points[0]], np.diff(points, axis=0)], axis=0)
            return self.draw_line(points, **styles)
        else:
            return self.figure.add_path(d=commands, **styles)

class SVGFigure(GraphicsFigure):
    Axes = SVGAxes
    default_styles= {
        "vector-effect":'non-scaling-stroke'
    }
    def __init__(self, axes=None, layout=None, figsize=None,
                 flip_y=True,
                 **kwargs):
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
        super().__init__(axes=axes)
        self.layout = layout
        self.kwargs = self.default_styles | kwargs
        self.flip_y = flip_y
        if figsize is not None:
            self.set_size_inches(*figsize)
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
        if rows == 1 and cols == 1:
            self.axes = [self.Axes(**kw)]
            axes = self.axes[0]
        else:
            raise NotImplementedError("grid layout not implemented")
        return axes

    def create_inset(self, bbox, **kw) -> 'GraphicsAxes':
        """
        **LLM Docstring**

        Create an inset axes at the given bounding box (SVG backend).

        :param bbox: the inset bounding box
        :param kw: extra keyword options
        :return: the result
        """
        raise NotImplementedError("create_inset")

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
        raise NotImplementedError("create_colorbar")

    def add_axes(self, ax) -> 'GraphicsAxes':
        """
        **LLM Docstring**

        Add an existing axes object to the figure (SVG backend).

        :param ax: the axes to add
        """
        if self.axes is None: self.axes = []
        if not isinstance(ax, self.Axes): ax = self.Axes(ax)
        self.axes.append(ax)
        return ax

    def clear(self, *, backend):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (SVG backend).

        """
        self.axes = []

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
        width = self.kwargs.get('width')
        height = self.kwargs.get('height')
        if isinstance(width, str) and width.endswith("px"):
            width = float(width.split("px")[0].strip())
        if nput.is_numeric(width):
            width = width / DPI_SCALING
        else:
            width = 0
        if isinstance(height, str) and height.endswith("px"):
            height = float(height.split("px")[0].strip())
        if nput.is_numeric(height):
            height = height / DPI_SCALING
        else:
            height = 0
        return width, height

    def set_size_inches(self, w, h):
        """
        **LLM Docstring**

        Set the figure size in inches (SVG backend).

        :param w: the width in inches
        :param h: the height in inches
        """
        if nput.is_numeric(w): w = w * DPI_SCALING
        self.kwargs['width'] = f"{w:.0f}px"
        if nput.is_numeric(h): h = h * DPI_SCALING
        self.kwargs['height'] = f"{h:.0f}px"

    def set_extents(self, extents):
        """
        **LLM Docstring**

        Set the figure's coordinate extents (SVG backend).

        :param extents: the extents
        """
        (l, r), (b, t) = extents
        ml = l * 100
        mr = (1 - r) * 100
        mt = (1 - t) * 100
        mb = (b) * 100
        self.kwargs['pad'] = f"{mt:.0f}% {mr:.0f}% {mb:.0f}% {ml:.0f}%"

    def get_facecolor(self):
        """
        **LLM Docstring**

        Return the background/face color (SVG backend).

        :return: the result
        """
        return self.kwargs.get('background')
    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color (SVG backend).

        :param fg: the face color
        """
        self.kwargs['background'] = fg

    def savefig(self, file, **opts):
        """
        **LLM Docstring**

        Save the figure to a file (SVG backend).

        :param file: the destination file/path
        :param opts: extra options
        """
        return self.to_widget().write(file, **opts)

    def animate_frames(self, frames, **animation_opts):
        """
        **LLM Docstring**

        Animate a sequence of frames (SVG backend).

        :param frames: the animation frames
        :param animation_opts: animation options
        """
        raise NotImplementedError("animate_frames")

    def to_html(self):
        """
        **LLM Docstring**

        Render the figure to HTML (SVG backend).

        :return: the result
        """
        return self.to_widget().tostring()

    def prep_args(self, opts):
        """
        **LLM Docstring**

        Merge the figure's default styling with per-call options.

        :param opts: the per-call options
        :type opts: dict
        :return: the merged options
        :rtype: dict
        """
        kwargs = self.kwargs | opts
        ...
    def to_svg_figure(self, **opts):
        """
        **LLM Docstring**

        Assemble the figure's axes into a single HTML `Div` of SVGs (applying the y-flip
        transform).

        :param opts: extra styling options
        :return: the assembled figure element
        """
        from ..Jupyter import JHTML
        sub_svgs = [
            s.figure.to_svg()
            for s in self.axes
        ]
        #TODO: handle layout
        fig = JHTML.Div(sub_svgs, **(self.kwargs | opts))
        if self.flip_y:
            fig.style['transform'] = (fig.style.get('transform', '') + ' scaleY(-1)').strip()
        return fig
    def to_svg(self):
        """
        **LLM Docstring**

        Render the whole figure to a combined SVG string.

        :return: the SVG markup
        :rtype: str
        """
        sub_svgs = [
            s.figure.to_svg()
            for s in self.axes
        ]
        buf = io.StringIO()
        for s in sub_svgs:
            s.write(buf)
        buf.seek(0)
        return buf.read()
    def to_widget(self, **opts):
        """
        **LLM Docstring**

        Render the figure as an interactive widget (SVG backend).

        :param opts: extra options
        :return: the result
        """
        return self.to_svg_figure(**opts)

    def _repr_html_(self):
        """
        **LLM Docstring**

        Return the figure's SVG as its IPython HTML representation.

        :return: the SVG/HTML
        :rtype: str
        """
        return self.to_html()

    def get_mime_bundle(self):
        """
        **LLM Docstring**

        Return the figure's MIME bundle for rich display (SVG backend).

        :return: the result
        """
        html = self.to_html()
        return {
            'image/svg':  html
        }

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
        figure = self.Figure(*args, **kwargs)
        axes = figure.create_axes(1, 1, 1)
        return figure, axes

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
            return [], {}

        def begin_context(self):
            """
            **LLM Docstring**

            Enter the context, applying the theme.

            """
            return self

        def end_context(self, exc_type, exc_val, exc_tb):
            """
            **LLM Docstring**

            Exit the context, restoring the previous theme.

            :param exc_type: the exception type, if any
            :param exc_val: the exception value, if any
            :param exc_tb: the traceback, if any
            """
            ...

    def show_figure(self, graphics:SVGFigure, reshow=None):
        """
        **LLM Docstring**

        Display a figure via the backend (SVG backend).

        :param graphics: the `graphics`
        :param reshow: force a reshow of an already-shown figure
        """
        if not graphics.shown:
            graphics.shown = True
            graphics.to_svg_figure().display()

    def get_interactive_status(self) -> 'bool':
        """
        **LLM Docstring**

        Return whether interactive mode is on (SVG backend).

        :return: the result
        """
        return False
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
        return []

class SVGAxes3D(SVGAxes):
    figure: svg.SVGFigure3D
    def __init__(self,
                 base_fig=None,
                 **opts
                 ):
        """
        **LLM Docstring**

        Set up an SVG 3D axes wrapping an `SVGFigure3D`, adding the z-axis manager.

        :param base_fig: the backing SVG 3D figure (created if omitted)
        :param opts: extra axes options
        """
        if base_fig is None:
            base_fig = svg.SVGFigure3D()
        super().__init__(base_fig=base_fig, **opts)
        self.zaxis = self.get_zaxis_manager()

    def get_zaxis_manager(self):
        """
        **LLM Docstring**

        Build the z-axis tick manager for this axes (SVG backend).

        :return: the result
        """
        return ZAxisManager(
            self.get_zticks,
            self.set_zticks,
            None,
            None,
            None,
            None
        )

    num_axes = 3
    def get_zlim(self):
        """
        **LLM Docstring**

        Return the z-axis limits (SVG backend).

        :return: the result
        """
        return self.get_limit(2)
    def set_zlim(self, val, **opts):
        """
        **LLM Docstring**

        Set the z-axis limits (SVG backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        self.set_limit(2, val)

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
        raise NotImplementedError("ticks not implemented for SVG")
    def set_ztick_style(self, **opts):
        """
        **LLM Docstring**

        Set the z-axis tick styling (SVG backend).

        :param opts: extra options
        """
        raise NotImplementedError("ticks not implemented for SVG")

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
        return self.figure.get_projection_kwargs()
    def set_view_settings(self, **ops):
        """
        **LLM Docstring**

        Set the 3D camera/view settings (SVG backend).

        :param ops: the view settings
        """
        return self.figure.set_projection_kwargs(**ops)


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
        if normal is None:
            normal = np.array([0, 0, 1])
        if rotation is not None:
            up_vector = nput.rotation_matrix(normal, rotation)[:, 0]
        else:
            up_vector = nput.vec_crosses([1, 0, 0], normal)
        return nput.view_matrix(
            up_vector,
            view_vector=normal,
            output_order=['x', 'y', 'z']
        )
    def draw_line(self, points, **styles):
        """
        **LLM Docstring**

        Draw a line/polyline through the given points (SVG backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        styles = self.prep_styles(styles)
        points = np.asanyarray(points)
        if len(points) > 2:
            return self.figure.add_polyline(points=points, **styles)
        else:
            (x1, y1, z1), (x2, y2, z2) = points
            return self.figure.add_line(x1=x1, y1=y1, z1=z1, x2=x2, y2=y2, z2=z2, **styles)
    def draw_disk(self, points, *, radius,
                  angle=None,
                  normal=None, uv_axes=None,
                  offset_angle=None, span_angle=None,
                  **styles):
        """
        **LLM Docstring**

        Draw a filled disk at the given position(s) (SVG backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        styles = self.prep_styles(styles)
        if uv_axes is not None:
            u, v = uv_axes
            base_ang, base_norm = nput.vec_angles(u, v, return_crosses=True)
            base_norm = nput.vec_normalize(base_norm)
            if normal is None:
                normal = base_norm
            angs, crosses, cns = nput.vec_angles([0, 0, 1], normal, return_crosses=True, return_cross_norms=True)
            if cns < 1e-6:
                embedding_axes = np.eye(3)
            else:
                embedding_axes = nput.rotation_matrix(crosses, angs)
            emb_u, emb_v = np.array([u, v]) @ embedding_axes
            det = emb_u[0] * emb_v[1] - emb_u[1] * emb_v[0]
            emb_z = np.cross(emb_u, emb_v)
            if det < 0:
                emb_angle = np.arctan2(emb_v[1], emb_v[0])
                if emb_z[2] > 0:
                    emb_angle = -emb_angle
            else:
                emb_angle = np.arctan2(emb_u[1], emb_u[0])
                if emb_z[2] < 0:
                    emb_angle = -emb_angle
            if offset_angle is None:
                offset_angle = emb_angle
            if span_angle is None:
                span_angle = angle
        x, y, z = np.asanyarray(points)
        return self.figure.add_circle(x=x, y=y, z=z, r=radius,
                                      normal=normal,
                                      offset_angle=offset_angle,
                                      span_angle=span_angle,
                                      **styles)
    def draw_rect(self, points, rotation=None, normal=None, **styles):
        """
        **LLM Docstring**

        Draw a rectangle from the given points (SVG backend).

        :param points: the points to draw
        :param rotation: the `rotation`
        :param normal: the `normal`
        :param styles: the styling options
        """
        points = np.asanyarray(points)
        if normal is None:
            ax = points[1] - points[0]
            normal = nput.vec_normalize(nput.project_out([0, 0, 1], ax[:, np.newaxis]))
        eps = points @ self.embedding_matrix(rotation, normal)
        (x1, y1, z1), (x2, y2, z2) = eps
        x, y, z = points[0]
        return self.figure.add_rect(x=x, y=y, z=z, width=x2-x1, height=y2-y1, rotation=rotation, normal=normal, **styles)
    def draw_sphere(self, points, rads, **styles):
        """
        **LLM Docstring**

        Draw a sphere (or spheres) at the given center(s) with the given radii (SVG backend).

        :param points: the sphere center(s)
        :param rads: the sphere radii
        :param styles: the styling options
        """
        styles = self.prep_styles(styles)
        return self.figure.add_sphere(center=points, radius=rads, **styles)
    def draw_cylinder(self, start, end, rad, **styles):
        """
        **LLM Docstring**

        Draw a cylinder between two endpoints (SVG backend).

        :param start: the start point
        :param end: the end point
        :param rad: the cylinder radius
        :param styles: the styling options
        """
        styles = self.prep_styles(styles)
        return self.figure.add_cylinder(start=start, end=end, radius=rad, **styles)
    def draw_box(self, start, end, **styles):
        """
        **LLM Docstring**

        Draw an axis-aligned box between two corners (SVG backend).

        :param start: the min corner
        :param end: the max corner
        :param styles: the styling options
        """
        styles = self.prep_styles(styles)
        return self.figure.add_box(start, end, **styles)
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
        styles = self.prep_styles(styles)
        if projected or use_path:
            font_opts, styles = self.filter_font_options(styles)
            mpl_path = self._text_to_path(points, vals, **font_opts)
            commands = svg.SVGPath.from_mpl(mpl_path)
            return self.figure.add_path(commands=commands, **styles)
        else:
            x, y, z = points
            if flip_y:
                styles['transform'] = (styles.get('transform', ' ') + 'scale(1 -1)')
                styles['transform-box'] = 'fill-box' # TODO: make this compose well with other transforms...
            return self.figure.add_text(x=x, y=y, z=z, text=vals, **styles)

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
        self.obj = figure
        self.objs = []
        self._plot_label = None
        super().__init__(figure_region)

    @classmethod
    def canonicalize_opts(cls, opts):
        """
        **LLM Docstring**

        Normalize construction options into the backend's canonical form (VTK backend).

        :param opts: the options to canonicalize
        """
        return opts

    def remove(self, *, backend):
        """
        **LLM Docstring**

        Tear down (remove) this axes from its figure (VTK backend).

        """
        self.obj.close()

    def clear(self, *, backend):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (VTK backend).

        """
        for o in self.objs:
            self.obj.remove_object(o)

    def get_plotter(self, method):
        """
        **LLM Docstring**

        Resolve a plotting-method name to the backend callable that draws it (VTK backend).

        :param method: the plot-method name
        :return: the result
        """
        raise NotImplementedError(f"plotter for {method} not implemented")

    def get_plot_label(self):
        """
        **LLM Docstring**

        Return the plot title/label (VTK backend).

        :return: the result
        """
        return self.obj.get_title()
        # return self._plot_label

    def set_plot_label(self, val, **style):
        """
        **LLM Docstring**

        Set the plot title/label (VTK backend).

        :param val: the label text
        :param style: label styling options
        """
        return self.obj.set_title(val)
        # x_min, x_max = self.region[0]
        # y_min, y_max = self.region[1]
        # pos = self.renormalize(np.array([(x_max+x_min)/2, (y_max+y_min)/2, 0]))
        # self.obj.draw_text(val, )

    def get_style_list(self):
        """
        **LLM Docstring**

        Return the per-series style cycle (VTK backend).

        :return: the result
        """
        raise NotImplementedError("style list cyclers not supported")
    def set_style_list(self, props):
        """
        **LLM Docstring**

        Set the per-series style cycle (VTK backend).

        :param props: the style cycle
        """
        raise NotImplementedError("style list cyclers not supported")

    def get_frame_visible(self):
        """
        **LLM Docstring**

        Return which frame (spine) edges are drawn (VTK backend).

        :return: the result
        """
        raise NotImplementedError("get_frame_visible")

    def set_frame_visible(self, frame_spec):
        """
        **LLM Docstring**

        Set which frame (spine) edges are drawn (VTK backend).

        :param frame_spec: the per-edge visibility spec
        """
        raise NotImplementedError("set_frame_visible")

    def get_frame_style(self):
        """
        **LLM Docstring**

        Return the frame (spine) styling (VTK backend).

        :return: the result
        """
        raise NotImplementedError("get_frame_style")

    def set_frame_style(self, frame_spec):
        """
        **LLM Docstring**

        Set the frame (spine) styling (VTK backend).

        :param frame_spec: the frame styling
        """
        raise NotImplementedError("set_frame_style")

    def get_xlabel(self):
        """
        **LLM Docstring**

        Return the x-axis label (VTK backend).

        :return: the result
        """
        raise NotImplementedError("get_xlabel")

    def set_xlabel(self, val, **style):
        """
        **LLM Docstring**

        Set the x-axis label (VTK backend).

        :param val: the label text
        :param style: label styling options
        """
        raise NotImplementedError("set_xlabel")

    def get_ylabel(self):
        """
        **LLM Docstring**

        Return the y-axis label (VTK backend).

        :return: the result
        """
        raise NotImplementedError("get_xlabel")

    def set_ylabel(self, val, **style):
        """
        **LLM Docstring**

        Set the y-axis label (VTK backend).

        :param val: the label text
        :param style: label styling options
        """
        raise NotImplementedError("set_ylabel")

    def get_xlim(self):
        """
        **LLM Docstring**

        Return the x-axis limits (VTK backend).

        :return: the result
        """
        return self.obj.get_xlim()
    def set_xlim(self, val, **opts):
        """
        **LLM Docstring**

        Set the x-axis limits (VTK backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        return self.obj.set_xlim(val)

    def get_ylim(self):
        """
        **LLM Docstring**

        Return the y-axis limits (VTK backend).

        :return: the result
        """
        return self.obj.get_ylim()
    def set_ylim(self, val, **opts):
        """
        **LLM Docstring**

        Set the y-axis limits (VTK backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        return self.obj.set_ylim(val)

    def get_zlim(self):
        """
        **LLM Docstring**

        Return the z-axis limits (VTK backend).

        :return: the result
        """
        return self.obj.get_zlim()
    def set_zlim(self, val, **opts):
        """
        **LLM Docstring**

        Set the z-axis limits (VTK backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        return self.obj.set_zlim(val)

    def get_xticks(self):
        """
        **LLM Docstring**

        Return the x-axis tick locations (VTK backend).

        :return: the result
        """
        raise NotImplementedError("get_xticks")
    def set_xticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the x-axis tick locations (VTK backend).

        :param val: the tick locations
        :param opts: extra options
        """
        raise NotImplementedError("set_xticks")

    def get_yticks(self):
        """
        **LLM Docstring**

        Return the y-axis tick locations (VTK backend).

        :return: the result
        """
        raise NotImplementedError("get_yticks")
    def set_yticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the y-axis tick locations (VTK backend).

        :param val: the tick locations
        :param opts: extra options
        """
        raise NotImplementedError("set_yticks")

    def get_xtick_style(self):
        """
        **LLM Docstring**

        Return the x-axis tick styling (VTK backend).

        :return: the result
        """
        raise NotImplementedError("get_xtick_style")
    def set_xtick_style(self, **opts):
        """
        **LLM Docstring**

        Set the x-axis tick styling (VTK backend).

        :param opts: extra options
        """
        raise NotImplementedError("set_xtick_style")

    def get_ytick_style(self):
        """
        **LLM Docstring**

        Return the y-axis tick styling (VTK backend).

        :return: the result
        """
        raise NotImplementedError("get_ytick_style")
    def set_ytick_style(self, **opts):
        """
        **LLM Docstring**

        Set the y-axis tick styling (VTK backend).

        :param opts: extra options
        """
        raise NotImplementedError("set_ytick_style")

    def set_aspect_ratio(self, ar):
        """
        **LLM Docstring**

        Set the axes aspect ratio (VTK backend).

        :param ar: the aspect ratio
        """
        raise NotImplementedError("set_aspect_ratio")

    def get_bbox(self):
        """
        **LLM Docstring**

        Return the axes bounding box (VTK backend).

        :return: the result
        """
        raise NotImplementedError("get_bbox")
        return [self.obj.get_xlim(), self.obj.get_ylim(), self.obj.get_zlim()]
    def set_bbox(self, bbox):
        """
        **LLM Docstring**

        Set the axes bounding box (VTK backend).

        :param bbox: the bounding box
        """
        raise NotImplementedError("set_bbox")

    def get_facecolor(self):
        """
        **LLM Docstring**

        Return the background/face color (VTK backend).

        :return: the result
        """
        return self.obj.get_facecolor()
    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color (VTK backend).

        :param fg: the face color
        """
        return self.obj.set_facecolor(fg)

    def get_padding(self):
        """
        **LLM Docstring**

        Return the axes padding (VTK backend).

        :return: the result
        """
        raise NotImplementedError("get_padding")

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
        self.obj = vtk_window
        super().__init__(**self.canonicalize_opts(opts))

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
        return self.add_axes(
            self.obj.add_subplot((rows, cols, spans), **kw)
        )

    @abc.abstractmethod
    def create_inset(self, bbox, **kw) -> 'GraphicsAxes':
        """
        **LLM Docstring**

        Create an inset axes at the given bounding box (VTK backend).

        :param bbox: the inset bounding box
        :param kw: extra keyword options
        :return: the result
        """
        raise NotImplementedError(...)

    @abc.abstractmethod
    def clear(self, *, backend):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (VTK backend).

        """
        self.obj.clear()
        # for obj in ...:


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
        return [
            a.get_bbox() for a in self.axes
        ]

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
        if cls._vec is None:
            cls._vec = vpython.method('vector')
        if isinstance(arg, (list, tuple, np.ndarray)):
            arg = cls._vec(*arg)
        return arg
    @classmethod
    def vpython_color(cls, color):
        """
        **LLM Docstring**

        Coerce a color (name or RGB) into a VPython color vector.

        :param color: the color
        :return: the VPython color vector
        """
        if isinstance(color, str):
            color = MPLManager.color_api().to_rgb(color)
        return cls.vpythonify(color)

class VPythonCanvasWrapper(VPythonWrapper):

    def __init__(self, canvas):
        """
        **LLM Docstring**

        Wrap a VPython canvas for drawing 3D primitives.

        :param canvas: the VPython canvas
        """
        self.canvas = canvas

    def remove(self, *, backend=None):
        """
        **LLM Docstring**

        Tear down (remove) this axes from its figure (VPython backend).

        """
        self.canvas.delete()
    def clear(self, *, backend=None):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (VPython backend).

        """
        for obj in self.canvas.objects:
            obj.visible = False

    @property
    def width(self):
        """
        **LLM Docstring**

        Return the width (VPython backend).

        :param width: the `width`
        """
        return self.canvas.width
    @width.setter
    def width(self, width):
        """
        **LLM Docstring**

        Return the width (VPython backend).

        :param width: the `width`
        """
        self.canvas.width = width

    @property
    def height(self):
        """
        **LLM Docstring**

        Return the height (VPython backend).

        :param height: the `height`
        """
        return self.canvas.height
    @height.setter
    def height(self, height):
        """
        **LLM Docstring**

        Return the height (VPython backend).

        :param height: the `height`
        """
        self.canvas.height = height

    @property
    def title(self):
        """
        **LLM Docstring**

        Return the title (VPython backend).

        :param title: the `title`
        """
        return self.canvas.title
    @title.setter
    def title(self, title):
        """
        **LLM Docstring**

        Return the title (VPython backend).

        :param title: the `title`
        """
        self.canvas.title = title

    @property
    def axis(self):
        """
        **LLM Docstring**

        Return the axis object/handle (VPython backend).

        :param axis: the `axis`
        """
        return self.canvas.axis
    @axis.setter
    def axis(self, axis):
        """
        **LLM Docstring**

        Return the axis object/handle (VPython backend).

        :param axis: the `axis`
        """
        self.canvas.axis = axis

    @property
    def up(self):
        """
        **LLM Docstring**

        Return the camera up-vector (VPython backend).

        :param up: the `up`
        """
        return self.canvas.up
    @up.setter
    def up(self, up):
        """
        **LLM Docstring**

        Return the camera up-vector (VPython backend).

        :param up: the `up`
        """
        self.canvas.up = up

    @property
    def background(self):
        """
        **LLM Docstring**

        Return the background color (VPython backend).

        :param background: the `background`
        """
        return self.canvas.background
    @background.setter
    def background(self, background):
        """
        **LLM Docstring**

        Return the background color (VPython backend).

        :param background: the `background`
        """
        self.canvas.background = self.vpython_color(background)

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
        args = [
            self.vpythonify(arg) for arg in args
        ]
        opts = {
            k:self.vpythonify(arg) for k,arg in opts.items()
        }
        opts['color'] = self.vpython_color(color)
        opts = {
            k:o for k,o in opts.items()
            if o is not None
        }
        return vpython.method(name)(*args, canvas=self.canvas, **opts)

    def box(self, left_corner, right_corner, **styles):
        """
        **LLM Docstring**

        Draw a box between two corners.

        :param left_corner: the min corner
        :param right_corner: the max corner
        :param styles: the styling options
        :return: the VPython box
        """
        return self.primitive('box',
                              pos=left_corner,
                              length=right_corner[0] - left_corner[0],
                              height=right_corner[1] - left_corner[1],
                              width=right_corner[2] - left_corner[2], **styles)

    def curve(self, points, **styles):
        """
        **LLM Docstring**

        Draw a curve through the given points.

        :param points: the curve points
        :param styles: the styling options
        :return: the VPython curve
        """
        return self.primitive('curve', points, **styles)

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
        start = np.asanyarray(start)
        end = np.asanyarray(end)
        v = end - start
        n = np.linalg.norm(v)
        v = v / n

        return self.primitive('cylinder',
                              start,
                              rad=rad,
                              axis=v,
                              length=n,
                              **styles)

    def arrow(self, points, **styles):
        """
        **LLM Docstring**

        Draw an arrow at/through the given points.

        :param points: the arrow points
        :param styles: the styling options
        :return: the VPython arrow
        """
        return self.primitive('arrow', points, **styles)

    def label(self, pos, text, **styles):
        """
        **LLM Docstring**

        Draw a text label at a position.

        :param pos: the label position
        :param text: the label text
        :param styles: the styling options
        :return: the VPython label
        """
        return self.primitive('label', pos, text **styles)

    def sphere(self, points, rads, **styles):
        """
        **LLM Docstring**

        Draw a sphere at the given center(s) with the given radii.

        :param points: the sphere center(s)
        :param rads: the sphere radii
        :param styles: the styling options
        :return: the VPython sphere
        """
        return self.primitive('sphere', pos=points, rad=rads, **styles)

class VPythonGraphWrapper(VPythonWrapper):

    def __init__(self, graph):
        """
        **LLM Docstring**

        Wrap a VPython graph for 2D plotting, tracking the created plot objects.

        :param graph: the VPython graph
        """
        self.graph = graph
        self.objs = []

    @property
    def title(self):
        """
        **LLM Docstring**

        Return the title (VPython backend).

        :param title: the `title`
        """
        return self.graph.title
    @title.setter
    def title(self, title):
        """
        **LLM Docstring**

        Return the title (VPython backend).

        :param title: the `title`
        """
        self.graph.title = title

    @property
    def xtitle(self):
        """
        **LLM Docstring**

        Return the x-axis title (VPython backend).

        :param xtitle: the `xtitle`
        """
        return self.graph.xtitle
    @xtitle.setter
    def xtitle(self, xtitle):
        """
        **LLM Docstring**

        Return the x-axis title (VPython backend).

        :param xtitle: the `xtitle`
        """
        self.graph.xtitle = xtitle

    @property
    def ytitle(self):
        """
        **LLM Docstring**

        Return the y-axis title (VPython backend).

        :param ytitle: the `ytitle`
        """
        return self.graph.ytitle
    @ytitle.setter
    def ytitle(self, ytitle):
        """
        **LLM Docstring**

        Return the y-axis title (VPython backend).

        :param ytitle: the `ytitle`
        """
        self.graph.ytitle = ytitle

    @property
    def background(self):
        """
        **LLM Docstring**

        Return the background color (VPython backend).

        :param background: the `background`
        """
        return self.graph.background
    @background.setter
    def background(self, background):
        """
        **LLM Docstring**

        Return the background color (VPython backend).

        :param background: the `background`
        """
        self.graph.background = self.vpython_color(background)

    @property
    def foreground(self):
        """
        **LLM Docstring**

        Return the foreground color (VPython backend).

        :param foreground: the `foreground`
        """
        return self.graph.foreground
    @foreground.setter
    def foreground(self, foreground):
        """
        **LLM Docstring**

        Return the foreground color (VPython backend).

        :param foreground: the `foreground`
        """
        self.graph.foreground = self.vpython_color(foreground)

    @property
    def xmin(self):
        """
        **LLM Docstring**

        Return the x lower bound (VPython backend).

        :param xmin: the `xmin`
        """
        return self.graph.xmin
    @xmin.setter
    def xmin(self, xmin):
        """
        **LLM Docstring**

        Return the x lower bound (VPython backend).

        :param xmin: the `xmin`
        """
        self.graph.xmin = xmin

    @property
    def xmax(self):
        """
        **LLM Docstring**

        Return the x upper bound (VPython backend).

        :param xmax: the `xmax`
        """
        return self.graph.xmax
    @xmax.setter
    def xmax(self, xmax):
        """
        **LLM Docstring**

        Return the x upper bound (VPython backend).

        :param xmax: the `xmax`
        """
        self.graph.xmax = xmax

    @property
    def ymin(self):
        """
        **LLM Docstring**

        Return the y lower bound (VPython backend).

        :param ymin: the `ymin`
        """
        return self.graph.ymin
    @ymin.setter
    def ymin(self, ymin):
        """
        **LLM Docstring**

        Return the y lower bound (VPython backend).

        :param ymin: the `ymin`
        """
        self.graph.ymin = ymin

    @property
    def ymax(self):
        """
        **LLM Docstring**

        Return the y upper bound (VPython backend).

        :param ymax: the `ymax`
        """
        return self.graph.ymax
    @ymax.setter
    def ymax(self, ymax):
        """
        **LLM Docstring**

        Return the y upper bound (VPython backend).

        :param ymax: the `ymax`
        """
        self.graph.ymax = ymax

    @property
    def width(self):
        """
        **LLM Docstring**

        Return the width (VPython backend).

        :param width: the `width`
        """
        return self.graph.width
    @width.setter
    def width(self, width):
        """
        **LLM Docstring**

        Return the width (VPython backend).

        :param width: the `width`
        """
        self.graph.width = width

    @property
    def height(self):
        """
        **LLM Docstring**

        Return the height (VPython backend).

        :param height: the `height`
        """
        return self.graph.height
    @height.setter
    def height(self, height):
        """
        **LLM Docstring**

        Return the height (VPython backend).

        :param height: the `height`
        """
        self.graph.height = height

    def remove(self, *, backend=None):
        """
        **LLM Docstring**

        Tear down (remove) this axes from its figure (VPython backend).

        """
        self.graph.delete()
    def clear(self, *, backend=None):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (VPython backend).

        """
        for obj in self.graph.objects:
            obj.visible = False

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
        curve = vpython.gcurve(
            color=self.vpython_color(color),
            marker_color=self.vpython_color(marker_color),
            dot_color=self.vpython_color(dot_color),
            graph=self.graph,
            **styles
        )
        curve.plot(np.array([x, y]).T)
        self.objs.append(curve)
        return curve

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
        curve = vpython.gdots(
            color=self.vpython_color(color),
            marker_color=self.vpython_color(marker_color),
            dot_color=self.vpython_color(dot_color),
            graph=self.graph,
            **styles
        )
        curve.plot(np.array([x, y]).T)
        self.objs.append(curve)
        return curve

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
        curve = vpython.gvbars(
            color=self.vpython_color(color),
            marker_color=self.vpython_color(marker_color),
            dot_color=self.vpython_color(dot_color),
            graph=self.graph,
            **styles
        )
        curve.plot(np.array([x, y]).T)
        self.objs.append(curve)
        return curve

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
        curve = vpython.ghbars(
            color=self.vpython_color(color),
            marker_color=self.vpython_color(marker_color),
            dot_color=self.vpython_color(dot_color),
            graph=self.graph,
            **styles
        )
        curve.plot(np.array([x, y]).T)
        self.objs.append(curve)
        return curve

class VPythonAxes(GraphicsAxes):
    def __init__(self, graph:VPythonGraphWrapper):
        """
        **LLM Docstring**

        Set up a VPython 2D axes over a graph wrapper.

        :param graph: the VPython graph wrapper
        :type graph: VPythonGraphWrapper
        """
        super().__init__()
        self.graph = graph

    def remove(self, *, backend):
        """
        **LLM Docstring**

        Tear down (remove) this axes from its figure (VPython backend).

        """
        self.graph.remove(backend=backend)
    def clear(self, *, backend):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (VPython backend).

        """
        self.graph.clear(backend=backend)

    def get_plotter(self, method):
        """
        **LLM Docstring**

        Resolve a plotting-method name to the backend callable that draws it (VPython backend).

        :param method: the plot-method name
        :return: the result
        """
        raise NotImplementedError(...)

    def get_plot_label(self):
        """
        **LLM Docstring**

        Return the plot title/label (VPython backend).

        :return: the result
        """
        return self.graph.title
    def set_plot_label(self, val, **style):
        """
        **LLM Docstring**

        Set the plot title/label (VPython backend).

        :param val: the label text
        :param style: label styling options
        """
        self.graph.title = val

    def get_style_list(self):
        """
        **LLM Docstring**

        Return the per-series style cycle (VPython backend).

        :return: the result
        """
        raise NotImplementedError("style list cyclers not supported")
    def set_style_list(self, props):
        """
        **LLM Docstring**

        Set the per-series style cycle (VPython backend).

        :param props: the style cycle
        """
        raise NotImplementedError("style list cyclers not supported")

    def get_frame_visible(self):
        """
        **LLM Docstring**

        Return which frame (spine) edges are drawn (VPython backend).

        :return: the result
        """
        raise NotImplementedError(...)
    def set_frame_visible(self, frame_spec):
        """
        **LLM Docstring**

        Set which frame (spine) edges are drawn (VPython backend).

        :param frame_spec: the per-edge visibility spec
        """
        raise NotImplementedError(...)

    def get_frame_style(self):
        """
        **LLM Docstring**

        Return the frame (spine) styling (VPython backend).

        :return: the result
        """
        raise NotImplementedError(...)
    def set_frame_style(self, frame_spec):
        """
        **LLM Docstring**

        Set the frame (spine) styling (VPython backend).

        :param frame_spec: the frame styling
        """
        raise NotImplementedError(...)

    def get_xlabel(self):
        """
        **LLM Docstring**

        Return the x-axis label (VPython backend).

        :return: the result
        """
        return self.graph.xtitle
    def set_xlabel(self, val, **style):
        """
        **LLM Docstring**

        Set the x-axis label (VPython backend).

        :param val: the label text
        :param style: label styling options
        """
        self.graph.xtitle = val

    def get_ylabel(self):
        """
        **LLM Docstring**

        Return the y-axis label (VPython backend).

        :return: the result
        """
        return self.graph.ytitle
    def set_ylabel(self, val, **style):
        """
        **LLM Docstring**

        Set the y-axis label (VPython backend).

        :param val: the label text
        :param style: label styling options
        """
        self.graph.ytitle = val

    def get_xlim(self):
        """
        **LLM Docstring**

        Return the x-axis limits (VPython backend).

        :return: the result
        """
        return [self.graph.xmin, self.graph.xmax]
    def set_xlim(self, val, **opts):
        """
        **LLM Docstring**

        Set the x-axis limits (VPython backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        self.graph.xmin, self.graph.xmax = val

    def get_ylim(self):
        """
        **LLM Docstring**

        Return the y-axis limits (VPython backend).

        :return: the result
        """
        return [self.graph.ymin, self.graph.ymax]
    def set_ylim(self, val, **opts):
        """
        **LLM Docstring**

        Set the y-axis limits (VPython backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        self.graph.ymin, self.graph.ymax = val

    def get_xticks(self):
        """
        **LLM Docstring**

        Return the x-axis tick locations (VPython backend).

        :return: the result
        """
        raise NotImplementedError(...)
    def set_xticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the x-axis tick locations (VPython backend).

        :param val: the tick locations
        :param opts: extra options
        """
        raise NotImplementedError(...)

    def get_yticks(self):
        """
        **LLM Docstring**

        Return the y-axis tick locations (VPython backend).

        :return: the result
        """
        raise NotImplementedError(...)
    def set_yticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the y-axis tick locations (VPython backend).

        :param val: the tick locations
        :param opts: extra options
        """
        raise NotImplementedError(...)

    def get_xtick_style(self):
        """
        **LLM Docstring**

        Return the x-axis tick styling (VPython backend).

        :return: the result
        """
        raise NotImplementedError(...)
    def set_xtick_style(self, **opts):
        """
        **LLM Docstring**

        Set the x-axis tick styling (VPython backend).

        :param opts: extra options
        """
        raise NotImplementedError(...)

    def get_ytick_style(self):
        """
        **LLM Docstring**

        Return the y-axis tick styling (VPython backend).

        :return: the result
        """
        raise NotImplementedError(...)
    def set_ytick_style(self, **opts):
        """
        **LLM Docstring**

        Set the y-axis tick styling (VPython backend).

        :param opts: extra options
        """
        raise NotImplementedError(...)

    def set_aspect_ratio(self, ar):
        """
        **LLM Docstring**

        Set the axes aspect ratio (VPython backend).

        :param ar: the aspect ratio
        """
        raise NotImplementedError(...)

    def get_bbox(self):
        """
        **LLM Docstring**

        Return the axes bounding box (VPython backend).

        :return: the result
        """
        raise NotImplementedError(...)
    def set_bbox(self, bbox):
        """
        **LLM Docstring**

        Set the axes bounding box (VPython backend).

        :param bbox: the bounding box
        """
        raise NotImplementedError(...)

    def get_facecolor(self):
        """
        **LLM Docstring**

        Return the background/face color (VPython backend).

        :return: the result
        """
        return self.graph.background
    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color (VPython backend).

        :param fg: the face color
        """
        self.graph.background = fg

    def get_padding(self):
        """
        **LLM Docstring**

        Return the axes padding (VPython backend).

        :return: the result
        """
        raise NotImplementedError(...)

    def draw_line(self, points, **styles):
        """
        **LLM Docstring**

        Draw a line/polyline through the given points (VPython backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        return self.graph.plot(*np.asanyarray(points).T, **styles)

    def draw_disk(self, points, color=None, edge_color=None, radius=1,
                  edgecolors=None,
                  s=None, **styles):
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
        if edgecolors is None:
            if edge_color is not None:
                edgecolors = edge_color
            else:
                edgecolors=[[0.] * 3 + [.3]]
        if s is None:
            s = (10 * radius) ** 2
        return self.graph.scatter(*np.asanyarray(points).T, s=s, edgecolors=edgecolors, **styles)

    def draw_rect(self, points, **styles):
        """
        **LLM Docstring**

        Draw a rectangle from the given points (VPython backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        raise NotImplementedError("too annoying")

    def draw_poly(self, points, **styles):
        """
        **LLM Docstring**

        Draw a filled polygon from the given points (VPython backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        raise NotImplementedError("too annoying")

    def draw_arrow(self, points, color=None, **styles):
        """
        **LLM Docstring**

        Draw an arrow from the given points (VPython backend).

        :param points: the points to draw
        :param color: the `color`
        :param styles: the styling options
        """
        raise NotImplementedError("too annoying")

    def draw_text(self, points, vals, color=None, **styles):
        """
        **LLM Docstring**

        Draw text at the given position(s) (VPython backend).

        :param points: the points to draw
        :param vals: the text string(s)
        :param color: the `color`
        :param styles: the styling options
        """
        raise NotImplementedError("too annoying")
        # pts = np.asanyarray(points)
        # if pts.ndim == 1:
        #     return vpython.label(pts, vals, color=self.vpython_color(color), canvas=self.canvas, **styles)
        # else:
        #     return [
        #         vpython.label(pt, t, color=self.vpython_color(color), canvas=self.canvas, **styles)
        #         for pt, t in zip(pts, vals)
        #     ]

    def draw_sphere(self, points, rads, color=None, **styles):
        """
        **LLM Docstring**

        Draw a sphere (or spheres) at the given center(s) with the given radii (VPython backend).

        :param points: the sphere center(s)
        :param rads: the sphere radii
        :param color: the `color`
        :param styles: the styling options
        """
        raise NotImplementedError("too annoying")
        # return vpython.sphere(points, rads, color=self.vpython_color(color), canvas=self.canvas, **styles)

    def animate_frames(self, frames, **animation_opts):
        """
        **LLM Docstring**

        Animate a sequence of frames (VPython backend).

        :param frames: the animation frames
        :param animation_opts: animation options
        """
        raise NotImplementedError("not sure how to animate vpython")

class VPythonFigure(GraphicsFigure):
    Axes = VPythonAxes

    _refs = set()
    def __init__(self, vpython_graph:VPythonGraphWrapper, **opts):
        """
        **LLM Docstring**

        Wrap a VPython graph as a figure (tracked to avoid double-wrapping).

        :param vpython_graph: the VPython graph wrapper
        :type vpython_graph: VPythonGraphWrapper
        :param opts: canonicalized figure options
        :raises ValueError: if the graph is already wrapped
        """
        if vpython_graph in self._refs: raise ValueError(...)
        self._refs.add(vpython_graph)
        self.graph = vpython_graph
        super().__init__(**self.canonicalize_opts(opts))
    @classmethod
    def construct(cls, **kw) -> 'VPythonFigure':
        """
        **LLM Docstring**

        Construct a figure of this backend type (VPython backend).

        :param kw: construction options
        :return: the result
        """
        return cls(vpython.graph(**kw))
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
        if (rows, cols, spans) != (1, 1, 1):
            raise NotImplementedError("can't create subcanvases")
        return self.add_axes(self.graph)
    def create_inset(self, bbox, **kw) -> 'GraphicsAxes':
        """
        **LLM Docstring**

        Create an inset axes at the given bounding box (VPython backend).

        :param bbox: the inset bounding box
        :param kw: extra keyword options
        :return: the result
        """
        raise NotImplementedError(...)
    def clear(self, *, backend):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (VPython backend).

        """
        self.graph.clear()
    def close(self, *, backend):
        """
        **LLM Docstring**

        Close the figure (VPython backend).

        """
        self.graph.remove()

    def get_size_inches(self):
        """
        **LLM Docstring**

        Return the figure size in inches (VPython backend).

        :return: the result
        """
        return [self.graph.width//72, self.graph.height//72]
    def set_size_inches(self, w, h):
        """
        **LLM Docstring**

        Set the figure size in inches (VPython backend).

        :param w: the width in inches
        :param h: the height in inches
        """
        self.graph.width, self.graph.height = w*72, h*72

    def get_facecolor(self):
        """
        **LLM Docstring**

        Return the background/face color (VPython backend).

        :return: the result
        """
        return self.graph.background
    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color (VPython backend).

        :param fg: the face color
        """
        self.graph.background = fg

    def savefig(self, file, **opts):
        """
        **LLM Docstring**

        Save the figure to a file (VPython backend).

        :param file: the destination file/path
        :param opts: extra options
        """
        raise NotImplementedError("too annoying")

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
        figure = self.Figure.construct(**kwargs)
        axes = self.Figure.create_axes()
        return figure, axes

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
            return [], {}
        def begin_context(self):
            """
            **LLM Docstring**

            Enter the context, applying the theme.

            """
            return self
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
        return True
    def disable_interactivity(self):
        """
        **LLM Docstring**

        Disable interactive mode (VPython backend).

        """
        raise NotImplementedError("not possible")
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
        return []

class VPythonAxes3D(GraphicsAxes3D):
    def __init__(self, canvas:VPythonCanvasWrapper):
        """
        **LLM Docstring**

        Set up a VPython 3D axes over a canvas wrapper.

        :param canvas: the VPython canvas wrapper
        :type canvas: VPythonCanvasWrapper
        """
        super().__init__()
        self.canvas = canvas

    def remove(self, *, backend):
        """
        **LLM Docstring**

        Tear down (remove) this axes from its figure (VPython backend).

        """
        self.canvas.remove(backend=backend)
    def clear(self, *, backend):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (VPython backend).

        """
        self.canvas.clear(backend=backend)

    def get_plotter(self, method):
        """
        **LLM Docstring**

        Resolve a plotting-method name to the backend callable that draws it (VPython backend).

        :param method: the plot-method name
        :return: the result
        """
        raise NotImplementedError(...)

    def get_plot_label(self):
        """
        **LLM Docstring**

        Return the plot title/label (VPython backend).

        :return: the result
        """
        return self.canvas.title
    def set_plot_label(self, val, **style):
        """
        **LLM Docstring**

        Set the plot title/label (VPython backend).

        :param val: the label text
        :param style: label styling options
        """
        self.canvas.title = val

    def get_style_list(self):
        """
        **LLM Docstring**

        Return the per-series style cycle (VPython backend).

        :return: the result
        """
        raise NotImplementedError("style list cyclers not supported")
    def set_style_list(self, props):
        """
        **LLM Docstring**

        Set the per-series style cycle (VPython backend).

        :param props: the style cycle
        """
        raise NotImplementedError("style list cyclers not supported")

    def get_frame_visible(self):
        """
        **LLM Docstring**

        Return which frame (spine) edges are drawn (VPython backend).

        :return: the result
        """
        raise NotImplementedError(...)
    def set_frame_visible(self, frame_spec):
        """
        **LLM Docstring**

        Set which frame (spine) edges are drawn (VPython backend).

        :param frame_spec: the per-edge visibility spec
        """
        ...
        # raise NotImplementedError(...)

    def get_frame_style(self):
        """
        **LLM Docstring**

        Return the frame (spine) styling (VPython backend).

        :return: the result
        """
        raise NotImplementedError(...)
    def set_frame_style(self, frame_spec):
        """
        **LLM Docstring**

        Set the frame (spine) styling (VPython backend).

        :param frame_spec: the frame styling
        """
        ...
        # raise NotImplementedError(...)

    def get_xlabel(self):
        """
        **LLM Docstring**

        Return the x-axis label (VPython backend).

        :return: the result
        """
        raise NotImplementedError(...)
    def set_xlabel(self, val, **style):
        """
        **LLM Docstring**

        Set the x-axis label (VPython backend).

        :param val: the label text
        :param style: label styling options
        """
        ...
        # raise NotImplementedError(...)

    def get_ylabel(self):
        """
        **LLM Docstring**

        Return the y-axis label (VPython backend).

        :return: the result
        """
        raise NotImplementedError(...)
    def set_ylabel(self, val, **style):
        """
        **LLM Docstring**

        Set the y-axis label (VPython backend).

        :param val: the label text
        :param style: label styling options
        """
        ...
        # raise NotImplementedError(...)

    def get_xlim(self):
        """
        **LLM Docstring**

        Return the x-axis limits (VPython backend).

        :return: the result
        """
        raise NotImplementedError(...)
    def set_xlim(self, val, **opts):
        """
        **LLM Docstring**

        Set the x-axis limits (VPython backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        ...
        # raise NotImplementedError(...)

    def get_ylim(self):
        """
        **LLM Docstring**

        Return the y-axis limits (VPython backend).

        :return: the result
        """
        raise NotImplementedError(...)
    def set_ylim(self, val, **opts):
        """
        **LLM Docstring**

        Set the y-axis limits (VPython backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        ...
        # raise NotImplementedError(...)

    def get_zlim(self):
        """
        **LLM Docstring**

        Return the z-axis limits (VPython backend).

        :return: the result
        """
        raise NotImplementedError(...)
    def set_zlim(self, val, **opts):
        """
        **LLM Docstring**

        Set the z-axis limits (VPython backend).

        :param val: the `(min, max)` limits
        :param opts: extra options
        """
        ...
        # raise NotImplementedError(...)

    def get_xticks(self):
        """
        **LLM Docstring**

        Return the x-axis tick locations (VPython backend).

        :return: the result
        """
        return []
    def set_xticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the x-axis tick locations (VPython backend).

        :param val: the tick locations
        :param opts: extra options
        """
        ...
        # raise NotImplementedError(...)

    def get_yticks(self):
        """
        **LLM Docstring**

        Return the y-axis tick locations (VPython backend).

        :return: the result
        """
        return []
    def set_yticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the y-axis tick locations (VPython backend).

        :param val: the tick locations
        :param opts: extra options
        """
        ...
        # raise NotImplementedError(...)

    def get_zticks(self):
        """
        **LLM Docstring**

        Return the z-axis tick locations (VPython backend).

        :return: the result
        """
        return []
    def set_zticks(self, val, **opts):
        """
        **LLM Docstring**

        Set the z-axis tick locations (VPython backend).

        :param val: the tick locations
        :param opts: extra options
        """
        ...
        # raise NotImplementedError(...)

    def get_xtick_style(self):
        """
        **LLM Docstring**

        Return the x-axis tick styling (VPython backend).

        :return: the result
        """
        return {}
    def set_xtick_style(self, **opts):
        """
        **LLM Docstring**

        Set the x-axis tick styling (VPython backend).

        :param opts: extra options
        """
        ...
        # raise NotImplementedError(...)

    def get_ytick_style(self):
        """
        **LLM Docstring**

        Return the y-axis tick styling (VPython backend).

        :return: the result
        """
        return {}
    def set_ytick_style(self, **opts):
        """
        **LLM Docstring**

        Set the y-axis tick styling (VPython backend).

        :param opts: extra options
        """
        ...
        # raise NotImplementedError(...)

    def get_ztick_style(self):
        """
        **LLM Docstring**

        Return the z-axis tick styling (VPython backend).

        :return: the result
        """
        return {}
    def set_ztick_style(self, **opts):
        """
        **LLM Docstring**

        Set the z-axis tick styling (VPython backend).

        :param opts: extra options
        """
        ...
        # raise NotImplementedError(...)

    def set_aspect_ratio(self, ar):
        """
        **LLM Docstring**

        Set the axes aspect ratio (VPython backend).

        :param ar: the aspect ratio
        """
        ...
        # raise NotImplementedError(...)

    def get_bbox(self):
        """
        **LLM Docstring**

        Return the axes bounding box (VPython backend).

        :return: the result
        """
        raise NotImplementedError(...)
    def set_bbox(self, bbox):
        """
        **LLM Docstring**

        Set the axes bounding box (VPython backend).

        :param bbox: the bounding box
        """
        raise NotImplementedError(...)

    def get_facecolor(self):
        """
        **LLM Docstring**

        Return the background/face color (VPython backend).

        :return: the result
        """
        return self.canvas.background
    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color (VPython backend).

        :param fg: the face color
        """
        self.canvas.background = fg

    def get_padding(self):
        """
        **LLM Docstring**

        Return the axes padding (VPython backend).

        :return: the result
        """
        raise NotImplementedError(...)

    def draw_line(self, points, **styles):
        """
        **LLM Docstring**

        Draw a line/polyline through the given points (VPython backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        return self.canvas.curve(points, **styles)

    def draw_disk(self, points, **styles):
        """
        **LLM Docstring**

        Draw a filled disk at the given position(s) (VPython backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        raise NotImplementedError("2D")

    def draw_rect(self, points, **styles):
        """
        **LLM Docstring**

        Draw a rectangle from the given points (VPython backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        raise NotImplementedError("2D")

    def draw_poly(self, points, **styles):
        """
        **LLM Docstring**

        Draw a filled polygon from the given points (VPython backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        raise NotImplementedError("2D")

    def draw_arrow(self, points, **styles):
        """
        **LLM Docstring**

        Draw an arrow from the given points (VPython backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        return self.canvas.arrow(points, **styles)

    def draw_text(self, points, vals, **styles):
        """
        **LLM Docstring**

        Draw text at the given position(s) (VPython backend).

        :param points: the points to draw
        :param vals: the text string(s)
        :param styles: the styling options
        """
        pts = np.asanyarray(points)
        if pts.ndim == 1:
            return self.canvas.label(pts, vals, **styles)
        else:
            return [
                self.canvas.label(pt, t, **styles)
                for pt, t in zip(pts, vals)
            ]

    def draw_sphere(self, points, rads, **styles):
        """
        **LLM Docstring**

        Draw a sphere (or spheres) at the given center(s) with the given radii (VPython backend).

        :param points: the sphere center(s)
        :param rads: the sphere radii
        :param styles: the styling options
        """
        return self.canvas.sphere(points, rads, **styles)

    def draw_cylinder(self, start, end, rad, **styles):
        """
        **LLM Docstring**

        Draw a cylinder between two endpoints (VPython backend).

        :param start: the start point
        :param end: the end point
        :param rad: the cylinder radius
        :param styles: the styling options
        """
        return self.canvas.cylinder(start, end, rad, **styles)

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
        return self.canvas.primitive(name, *args, **kwargs)

class VPythonFigure3D(GraphicsFigure):
    Axes = VPythonAxes3D

    _refs = set()
    def __init__(self, vpython_canvas:VPythonCanvasWrapper, **opts):
        """
        **LLM Docstring**

        Wrap a VPython canvas as a 3D figure (tracked to avoid double-wrapping).

        :param vpython_canvas: the VPython canvas (or its wrapper)
        :param opts: canonicalized figure options
        :raises ValueError: if the canvas is already wrapped
        """
        if isinstance(vpython_canvas, VPythonCanvasWrapper):
            vpython_canvas = vpython_canvas.canvas
        if vpython_canvas in self._refs: raise ValueError(...)
        self._refs.add(vpython_canvas)
        self.canvas = VPythonCanvasWrapper(vpython_canvas)
        super().__init__(**self.canonicalize_opts(opts))
    @classmethod
    def construct(cls, **kw) -> 'GraphicsFigure':
        """
        **LLM Docstring**

        Construct a figure of this backend type (VPython backend).

        :param kw: construction options
        :return: the result
        """
        return cls(vpython.method('canvas')(**kw))
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
        if (rows, cols, spans) != (1, 1, 1):
            raise NotImplementedError("can't create subcanvases")
        return self.add_axes(self.canvas)
    def create_inset(self, bbox, **kw) -> 'GraphicsAxes':
        """
        **LLM Docstring**

        Create an inset axes at the given bounding box (VPython backend).

        :param bbox: the inset bounding box
        :param kw: extra keyword options
        :return: the result
        """
        raise NotImplementedError(...)
    def clear(self, *, backend):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (VPython backend).

        """
        self.canvas.clear()
    def close(self, *, backend):
        """
        **LLM Docstring**

        Close the figure (VPython backend).

        """
        self.canvas.remove()
    def get_size_inches(self):
        """
        **LLM Docstring**

        Return the figure size in inches (VPython backend).

        :return: the result
        """
        return [self.canvas.width//72, self.canvas.height//72]
    def set_size_inches(self, w, h):
        """
        **LLM Docstring**

        Set the figure size in inches (VPython backend).

        :param w: the width in inches
        :param h: the height in inches
        """
        self.canvas.width, self.canvas.height = w*72, h*72
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
        return self.canvas.background
    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color (VPython backend).

        :param fg: the face color
        """
        self.canvas.background = fg
    def savefig(self, file, **opts):
        """
        **LLM Docstring**

        Save the figure to a file (VPython backend).

        :param file: the destination file/path
        :param opts: extra options
        """
        raise NotImplementedError("too annoying")

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
        figure = self.Figure.construct(**kwargs)
        axes = figure.create_axes()
        return figure, axes

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
        return True
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
        return []

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
        super().__init__()
        self.children = list(children)
        self.title = title
        self.background = background
        self.opts = opts
        self.include_mathjax = include_mathjax
        self.onloads = []

    @classmethod
    def canonicalize_opts(cls, opts):
        """
        **LLM Docstring**

        Normalize construction options into the backend's canonical form (X3D backend).

        :param opts: the options to canonicalize
        """
        return opts

    def remove(self, *, backend):
        """
        **LLM Docstring**

        Tear down (remove) this axes from its figure (X3D backend).

        """
        self.children = []
        self.title = ""
        self.background = "white"

    def clear(self, *, backend):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (X3D backend).

        """
        self.children = []
        self.title = ""
        self.background = "white"

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
        return self.title
    def set_plot_label(self, val, **style):
        """
        **LLM Docstring**

        Set the plot title/label (X3D backend).

        :param val: the label text
        :param style: label styling options
        """
        self.title = val

    def get_style_list(self):
        """
        **LLM Docstring**

        Return the per-series style cycle (X3D backend).

        :return: the result
        """
        raise NotImplementedError("style list cyclers not supported")
    def set_style_list(self, props):
        """
        **LLM Docstring**

        Set the per-series style cycle (X3D backend).

        :param props: the style cycle
        """
        raise NotImplementedError("style list cyclers not supported")

    def get_frame_visible(self):
        """
        **LLM Docstring**

        Return which frame (spine) edges are drawn (X3D backend).

        :return: the result
        """
        raise NotImplementedError(...)
    def set_frame_visible(self, frame_spec):
        """
        **LLM Docstring**

        Set which frame (spine) edges are drawn (X3D backend).

        :param frame_spec: the per-edge visibility spec
        """
        ...
        # raise NotImplementedError(...)

    def get_frame_style(self):
        """
        **LLM Docstring**

        Return the frame (spine) styling (X3D backend).

        :return: the result
        """
        raise NotImplementedError(...)
    def set_frame_style(self, frame_spec):
        """
        **LLM Docstring**

        Set the frame (spine) styling (X3D backend).

        :param frame_spec: the frame styling
        """
        ...
        # raise NotImplementedError(...)

    def get_xlabel(self):
        """
        **LLM Docstring**

        Return the x-axis label (X3D backend).

        :return: the result
        """
        raise NotImplementedError(...)
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
        raise NotImplementedError(...)
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
        raise NotImplementedError(...)
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
        raise NotImplementedError(...)
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
        raise NotImplementedError(...)
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
        return []
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
        return []
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
        return []
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
        return {}
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
        return {}
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
        return {}
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
        raise NotImplementedError(...)
    def set_bbox(self, bbox):
        """
        **LLM Docstring**

        Set the axes bounding box (X3D backend).

        :param bbox: the bounding box
        """
        raise NotImplementedError(...)

    def get_facecolor(self):
        """
        **LLM Docstring**

        Return the background/face color (X3D backend).

        :return: the result
        """
        return self.background
    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color (X3D backend).

        :param fg: the face color
        """
        self.background = fg

    def get_padding(self):
        """
        **LLM Docstring**

        Return the axes padding (X3D backend).

        :return: the result
        """
        raise NotImplementedError(...)

    def get_view_settings(self):
        """
        **LLM Docstring**

        Return the 3D camera/view settings (X3D backend).

        :return: the result
        """
        return self.opts.get('viewpoint', {})
    def set_view_settings(self, **values):
        """
        **LLM Docstring**

        Set the 3D camera/view settings (X3D backend).

        :param values: keyword options
        """
        new_opts = {
            k:v for k,v in dict(self.opts.get('viewpoint', {}), **values).items()
            if v is not None
        }
        if len(new_opts) == 0 and 'viewpoint' in self.opts:
            del self.opts['viewpoint']
        else:
            self.opts['viewpoint'] = new_opts

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
        if dashing is True:
            return cls._apply_dashing([.2, .1], starts, ends, scaled=True)
        elif isinstance(dashing, dict):
            return cls._apply_dashing(dashing['dashing'], starts, ends, scaled=dashing.get('scaled', False))
        else:
            seg_w, space_w = dashing
            new_starts = []
            new_ends = []
            for s,e in zip(starts, ends):
                l,n = nput.vec_normalize(e-s, return_norms=True)
                if scaled:
                    dx = n * seg_w
                    ds = n * space_w
                else:
                    dx, ds = seg_w, space_w
                w = dx+ds
                if w <= 0: raise ValueError(f'invalid dashing spec, {dashing} (scaled={scaled})')
                nseg = int(n // w)
                for i in range(nseg):
                    new_starts.append(s + l*(i*w))
                    new_ends.append(s + l*(i*w+dx))

            return np.array(new_starts), np.array(new_ends)

    def draw_line(self, points, indices=None, s=None, riffle=True, line_thickness=None,
                  edgecolors=None, color=None, glow=None,
                  line_style=None,
                  dashing=None,
                  connected=True,
                  **styles):
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
        if color is None: color = edgecolors
        if color is None: color = 'black'
        # if line_thickness is None and s is not None:
        #     if not nput.is_numeric(s): s = s[0]
        #     line_thickness = s / 1000
        points = np.asanyarray(points)
        if riffle:
            if indices is not None:
                indices = np.asanyarray(indices)
                if indices.ndim > 1 and indices.shape[-1] > 2:
                    riff_start = np.arange(indices.shape[-1])
                    riff_end = np.roll(riff_start, -1)
                    indices = np.concatenate([
                        indices[..., riff_start, np.newaxis],
                        indices[..., riff_end, np.newaxis]
                    ], axis=-1).reshape(-1, 2)
                    indices = np.concatenate([indices, np.full((indices.shape[0], 1), -1)], axis=-1)
            elif points.ndim > 2 and points.shape[-2] > 2:
                riff_start = np.arange(points.shape[-2])
                riff_end = np.roll(riff_start, 1)
                points = np.concatenate([
                    points[..., riff_start, np.newaxis, :],
                    points[..., riff_end, np.newaxis, :]
                ], axis=-2).reshape((-1, 2, 3))

        if dashing is None and dev.str_is(line_style, 'dashed'):
            dashing = True

        if dashing is not None:
            if indices is not None:
                raise NotImplementedError("dashing + indices")
            else:
                if riffle:
                    starts, ends  = self._apply_dashing(dashing, points[:-1], points[1:])
                else:
                    starts, ends  = self._apply_dashing(dashing, points[::2], points[1::2])
                points = np.zeros((starts.shape[0]*2,) + starts.shape[1:], dtype=starts.dtype)
                points[::2] = starts
                points[1::2] = ends
            riffle = False

        if line_thickness is not None:
            if indices is not None:
                raise NotImplementedError("line thickness + indices")
            else:
                # line_set = x3d.X3DGroup([
                #     x3d.X3DCylinder(p1, p2, line_thickness=line_thickness, color=glow, **styles)
                #     for p1, p2 in zip(points[:-1], points[1:])
                # ])
                if glow is None:
                    glow = color
                    color = 'black'
                if riffle:
                    starts, ends = points[:-1], points[1:]
                else:
                    starts, ends = points[::2], points[1::2]
                line_set = x3d.X3DCylinder(starts, ends, radius=line_thickness,
                                           glow=glow,
                                           color=color,
                                           **styles)
        else:
            if glow is None:
                glow = color
            if indices is not None:
                line_set = x3d.X3DIndexedLineSet(points, indices, line_thickness=line_thickness, glow=glow, **styles)
            else:
                line_set = x3d.X3DLine(points, line_thickness=line_thickness, glow=glow, **styles)
        self.children.append(line_set)

        return line_set
    def draw_path(self, commands, **styles):
        """
        **LLM Docstring**

        Draw a path from a sequence of drawing commands (X3D backend).

        :param commands: the path drawing commands
        :param styles: the styling options
        """
        points = nput.parametric_path_points(commands)
        return self.draw_line(points, **styles)

    def draw_disk(self,
                  points,
                  radius=None,
                  color=None,
                  line_color=None,
                  edgecolors=None,
                  s=None,
                  normal=None,
                  line_thickness=None,
                  innerRadius=None,
                  outerRadius=None,
                  uv_axes=None,
                  uv_sign=None,
                  angle=None,
                  rotation=None,
                  solid=None,
                  **styles):
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
        if radius is None and s is not None:
            radius = s / 100
        if line_color is None:
            line_color = edgecolors

        if uv_axes is not None:
            u, v = uv_axes
            base_ang, base_norm = nput.vec_angles(u, v, return_crosses=True)
            base_norm = nput.vec_normalize(base_norm)
            if normal is None:
                normal = base_norm
            angs, crosses, cns = nput.vec_angles([0, 0, 1], normal, return_crosses=True, return_cross_norms=True)
            if cns < 1e-6:
                if np.dot([0, 0, 1], normal) > 0:
                    embedding_axes = np.eye(3)
                else:
                    embedding_axes = -np.eye(3)
            else:
                embedding_axes = nput.rotation_matrix(crosses, angs)
            emb_u, emb_v = np.array([u, v]) @ embedding_axes
            det = emb_u[0] * emb_v[1] - emb_u[1] * emb_v[0]
            emb_z = np.cross(emb_u, emb_v)
            if det > 0:
                emb_angle = np.arctan2(emb_v[1], emb_v[0])
                if emb_z[2] < 0:
                    emb_angle = -emb_angle
            else:
                emb_angle = np.arctan2(emb_u[1], emb_u[0])
                if emb_z[2] > 0:
                    emb_angle = -emb_angle
            if rotation is None:
                rotation = [0, 0, 1, emb_angle]
            if angle is None:
                angle = base_ang

        objects = []
        if line_color is not None:
            if line_thickness is None:
                disk_set = x3d.X3DCircle2D(points,
                                           normal=normal,
                                           radius=radius,
                                           rotation=rotation,
                                           solid=False if solid is None else solid,
                                           angle=angle,
                                           **(styles | dict(glow=line_color))
                                           )
            else:
                if color is None:
                    if innerRadius is None:
                        innerRadius = line_thickness
                    if outerRadius is None:
                        outerRadius = radius
                disk_set = x3d.X3DTorus(points,
                                        normal=normal,
                                        inner_radius=innerRadius if color is None else line_thickness,
                                        radius=outerRadius if color is None else radius,
                                        solid=solid,
                                        rotation=rotation,
                                        angle=angle,
                                        **(styles | dict(color='black', glow=line_color))
                                        )
            objects.append(disk_set)

        if color is None and line_color is None:
            color = 'black'
        if color is not None:
            if outerRadius is None:
                outerRadius = radius
            disk_set = x3d.X3DDisk2D(points,
                                     normal=normal,
                                     inner_radius=innerRadius,
                                     radius=outerRadius,
                                     color=color,
                                     rotation=rotation,
                                     solid=False if solid is None else solid,
                                     angle=angle,
                                     **styles
                                     )
            objects.append(disk_set)

        self.children.extend(objects)
        return objects

    def draw_arrow(self, points, **styles):
        """
        **LLM Docstring**

        Draw an arrow from the given points (X3D backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        points = np.asanyarray(points)
        arrows = x3d.X3DArrow(points[..., 0, :], points[..., 1, :], **styles)
        self.children.append(arrows)
        return arrows

    mathjax_cdn = 'https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.min.js'
    default_texture_font = {
        'font_family':'sans-serif',
        'font_size':'6px',
        # 'fill':'black',
        'dominant_baseline':'central'
    }
    font_style_remapping = {
        'color':'fill'
    }
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
        from ..Jupyter.JHTML import CSS
        if font_style is None:
            font_style = {}
        fs = self.default_texture_font | font_style
        fs = {self.font_style_remapping.get(k, k):v for k,v in fs.items()}
        fs = CSS(f"text", **fs).tostring()
        lines = text.splitlines()
        w = resolution * max(len(t) for t in lines)
        vh = 20 + 10 * len(lines)
        return re.sub(r"\s+", " ", f"""
<svg version="1.1" viewBox="0 0 100 {vh}" width="{w}" height="auto" id='{id}-svg' xmlns="http://www.w3.org/2000/svg">
  <style>{fs}</style>
  <text 
    x="0" y="10" 
    textLength="90" 
    lengthAdjust="spacingAndGlyphs">""") + text + "</text></svg>"
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
        from ..Jupyter.JHTML import CSS
        if font_style is None:
            font_style = {}
        fs = self.default_texture_font | font_style
        # fs = {self.font_style_remapping.get(k, k):v for k,v in fs.items()}
        fs = CSS(**fs).tostring()
        return re.sub(r"\s+", " ", f"""(function() {{
    let textureNode = document.getElementById('{id}-appearance-texture');
    if (textureNode??null !== null) {{
      MathJax_3.tex2svgPromise('""") + "\\\\text{" + text.replace("\\", "") + re.sub(r"\s+", " ", """}', {display: true}).then((textWrapper) => {
          MathJax_3.tex2svgPromise('""") + text + re.sub(r"\s+", " ", f"""', {{display: true}})
            .then((svgWrapper) => {{
                let textNode = textWrapper.getElementsByTagName('svg')[0];
                let svgNode = svgWrapper.getElementsByTagName('svg')[0];
                let serializer = new XMLSerializer();
                let w = parseFloat(svgNode.getAttribute('width')) * {resolution_upscaling};
                let h = parseFloat(svgNode.getAttribute('height')) * {resolution_upscaling};
                svgNode.setAttribute('width', w.toString() + 'ex');
                svgNode.setAttribute('height', h.toString() + 'ex');
                let w0 = parseFloat(textNode.getAttribute('width')) * {resolution_upscaling};
                let h0 = parseFloat(textNode.getAttribute('height')) * {resolution_upscaling};
                textNode.setAttribute('width', w0.toString() + 'ex');
                textNode.setAttribute('height', h0.toString() + 'ex');
                svgNode.style.cssText = '{fs}';
                let svgString = serializer.serializeToString(svgNode);
                textureNode.setAttribute('url', 'data:image/svg+xml,' + encodeURIComponent(svgString)); 
                
                let rectNode = document.getElementById('{id}');
                let curSize = rectNode.getAttribute('size').trim().split().map(parseFloat);
                let aspect = h / w;
                let scaling = w / w0;
                let scalingH = (w * aspect) / h0;
                if (scalingH < scaling) {{
                    scaling = scalingH;
                }}
                rectNode.setAttribute('size', (scaling * curSize[0]).toString() + " " + (scaling * curSize[0] * aspect).toString());
            }})
            .catch((err) => console.error(err));
        }});
    }}
}})()""")
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
        text = text.strip()
        num_dollar = text.count("$")
        return num_dollar == 2 and text[0] == "$" and text[-1] == "$"
    @classmethod
    def _prep_font_size(cls, text, font_style, opts,
                        line_height=10, char_width=None, char_width_scaling=1 / 30):
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
        if font_style is None:
            font_style = {}
        subfonts =  {o.partition("_")[-1]: v for o, v in opts.items() if o.startswith('font_')}
        for f in subfonts:
            del opts['font_' + f]
        font_style = subfonts | font_style
        font_size = font_style.get('size', 12)

        # lines = text.splitlines()
        # if char_width is None:
        #     font_size = font_style.get('font_size', 6)
        #     char_width = font_size * char_width_scaling
        # w = char_width * max(len(t) for t in lines)
        # vh = char_width * line_height * len(lines)
        font_size = font_size / 48
        font_style['size'] = font_size

        return font_style, opts
    def draw_text(self, points, vals, endpoint=None, allow_mathjax=True,
                  line_height=10, char_width=None, char_width_scaling=1/30, font_style=None, **styles):
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
        if allow_mathjax and self._is_math(vals):
            vals = vals.strip("$")
            id = 'x3d-obj-' + str(uuid.uuid4())[:6]
            if not isinstance(vals, str):
                raise NotImplementedError("need to dispatch")
            if font_style is None:
                font_style = styles
            if endpoint is None:
                points = np.asanyarray(points)
                if len(points) == 2:
                    points, endpoint = points
                else:
                    lines = vals.splitlines()
                    if char_width is None:
                        font_size = font_style.get('font_size', 6)
                        char_width = font_size * char_width_scaling
                    w = char_width * max(len(t) for t in lines)
                    vh = char_width * line_height * len(lines)
                    points = np.asanyarray(points)
                    endpoint = points + [w/2, vh/2, 0]
                    points = points - [w/2, vh/2, 0]
            # loader_id = 'tex-loader-' + str(uuid.uuid4())[:6]
            # loader = JHTML.HTML.Image(
            #     id=loader_id,
            #     src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7",
            #     onload=self.mathjax_load_script(vals.replace("\\", "\\\\"), id, font_style=font_style)
            # )
            self.onloads.append(
                {
                    (("MathJax", "MathJax_3"), self.mathjax_cdn):
                    self.mathjax_load_script(vals.replace("\\", "\\\\"), id, font_style=font_style)
                }
            )
            text = [
                x3d.X3DRectangle2D(points, endpoint,
                                      id=id,
                                      texture={'url':'data:image/svg+xml,'+self.texture_svg(vals, id, font_style)},
                                      **styles),
                # loader
            ]
            # self.include_mathjax = True
        else:
            font_style, styles = self._prep_font_size(vals, font_style, styles,
                                                      line_height=line_height, char_width=char_width,
                                                      char_width_scaling=char_width_scaling)

            text = [x3d.X3DText(points, text=vals, font_style=font_style, **styles)]
        self.children.extend(text)
        return text

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
        u, v = uv_axes
        base_ang, base_norm = nput.vec_angles(u, v, return_crosses=True)
        base_norm = nput.vec_normalize(base_norm)
        if normal is None:
            normal = base_norm
        angs, crosses = nput.vec_angles([0, 0, 1], normal, return_crosses=True, return_norms=False)
        embedding_axes = nput.rotation_matrix(crosses, angs).T
        local_x, local_y, local_z = embedding_axes
        emb_angle, ax2 = nput.vec_angles(local_x, v)
        if uv_sign is None:
            # print(np.dot(local_x, v))
            # print(np.dot(local_y, v))
            # print(np.dot(local_x, u))
            # print(np.dot(local_y, u))
            uv_sign = np.sign(np.dot(local_y, v))
        emb_angle = uv_sign * emb_angle
        if rotation is None:
            rotation = [0, 0, 1, emb_angle]
        if angle is None:
            angle = base_ang

        return normal, rotation, angle, embedding_axes

    def draw_rect(self, # TODO: this feels like circle just got duped?
                  points,
                  color=None,
                  line_color=None,
                  edgecolors=None,
                  normal=None,
                  line_thickness=None,
                  innerRadius=None,
                  outerRadius=None,
                  uv_axes=None,
                  uv_sign=None,
                  angle=None,
                  rotation=None,
                  solid=None,
                  cap_style='round',
                  **styles):
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

        if line_color is None:
            line_color = edgecolors

        if uv_axes is not None:
            normal, rotation, angle, embedding_axes = self.prep_uv(
                uv_axes, normal=normal, uv_sign=uv_sign, rotation=rotation, angle=angle
            )
        elif normal is not None:
            embedding_axes = nput.rotation_matrix(normal, [0, 0, 1])
            if rotation is not None:
                rotation = np.asanyarray(rotation)
                embedding_axes = embedding_axes @ nput.rotation_matrix(rotation[..., :3], rotation[..., 3])
        else:
            embedding_axes = None

        objects = []
        if line_color is not None:
            line_points = np.asanyarray(points)
            if embedding_axes is not None:
                center = (line_points[..., (0,), :] + line_points[..., (1,), :]) / 2
                line_points = line_points - center
                line_points = line_points @ embedding_axes
            left = line_points[..., 0, :]
            right = line_points[..., 1, :]
            second = np.concatenate([left[..., (0,)], right[..., (1,)], left[..., (2,)]], axis=-1)
            fourth = np.concatenate([right[..., (0,)], left[..., (1,)], right[..., (2,)]], axis=-1)
            if line_thickness is None:
                line_points = np.moveaxis(np.array([left, second, second, right, right, fourth, fourth, left]), 0, -2)
                if embedding_axes is not None:
                    line_points = line_points @ embedding_axes.T + center
                line_set = x3d.X3DLine(line_points,
                                           glow=line_color,
                                           **styles
                                           )
            else:
                starts = np.moveaxis(np.array([left, second, right, fourth]), 0, -2)
                ends = np.moveaxis(np.array([second, right, fourth, left]), 0, -2)
                if embedding_axes is not None:
                    starts = starts @ embedding_axes.T + center
                    ends = ends @ embedding_axes.T + center
                if cap_style == 'butt':
                    line_set = x3d.X3DCylinder(starts, ends,
                                               radius=line_thickness,
                                               color=line_color,
                                               solid=solid,
                                               **styles
                                               )
                else:
                    line_set = x3d.X3DCappedCylinder(starts, ends,
                                                     radius=line_thickness,
                                                     color=line_color,
                                                     solid=solid,
                                                     **styles
                                                     )
            objects.append(line_set)

        if color is None and line_color is None:
            color = 'black'
        if color is not None:
            points = np.asanyarray(points)
            rect_set = x3d.X3DRectangle2D(points[..., 0, :], points[..., 1, :],
                                     normal=normal,
                                     color=color,
                                     rotation=rotation,
                                     solid=False if solid is None else solid,
                                     **styles
                                     )
            objects.append(rect_set)

        self.children.extend(objects)

        return objects
    def draw_point(self, points, color=None, glow=None, **styles):
        """
        **LLM Docstring**

        Draw a point (as a small disk) at the given position(s) (X3D backend).

        :param points: the points to draw
        :param color: the `color`
        :param glow: the `glow`
        :param styles: the styling options
        """
        points = np.asanyarray(points)
        if glow is None: glow = color
        rects = x3d.X3DPointSet(points, glow=glow, **styles)
        self.children.append(rects)

        return rects
    def draw_triangle(self, points, indices=None, **styles):
        """
        **LLM Docstring**

        Draw a triangle from the given points (X3D backend).

        :param points: the points to draw
        :param indices: the `indices`
        :param styles: the styling options
        """
        if indices is None:
            points = np.asanyarray(points)
            rects = x3d.X3DTriangleSet(points, **styles)
        else:
            points = np.asanyarray(points)
            indices = np.asanyarray(indices)
            rects = x3d.X3DIndexedTriangleSet(points, indices, **styles)
        self.children.append(rects)

        return rects
    def draw_poly(self, points, **styles):
        """
        **LLM Docstring**

        Draw a filled polygon from the given points (X3D backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        raise NotImplementedError("2D")

    def draw_sphere(self, centers, rads, **styles):
        """
        **LLM Docstring**

        Draw a sphere (or spheres) at the given center(s) with the given radii (X3D backend).

        :param centers: the `centers`
        :param rads: the sphere radii
        :param styles: the styling options
        """
        spheres = x3d.X3DSphere(centers, radius=rads, **styles)
        self.children.append(spheres)

        return spheres

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
        if capped:
            cyls = x3d.X3DCappedCylinder(starts, ends, radius=rads, **styles)
        else:
            cyls = x3d.X3DCylinder(starts, ends, radius=rads, **styles)
        self.children.append(cyls)

        return cyls
    def draw_box(self, start, end, **opts):
        """
        **LLM Docstring**

        Draw an axis-aligned box between two corners (X3D backend).

        :param start: the min corner
        :param end: the max corner
        :param opts: extra options
        """
        box = x3d.X3DBox(start, end, **opts)
        self.children.append(box)
        return box
    def prep_opts(self):
        """
        **LLM Docstring**

        Assemble the axes' options for X3D scene construction (folding in the background
        and title).

        :return: the options dict
        :rtype: dict
        """
        return dict(
            self.opts,
            background=self.background,
            title=self.title
        )
    def to_x3d(self):
        """
        **LLM Docstring**

        Build the X3D scene from the axes' child primitives and options.

        :return: the X3D scene
        """
        return x3d.X3DScene(
            self.children,
            **self.prep_opts()
        )

class X3DFigure(GraphicsFigure):
    Axes = X3DAxes

    def __init__(self, width=640, height=500,
                 background='white', figsize=None, profile='Immersive', version='3.3',
                 dynamic_loading=None,
                 include_export_button=None,
                 include_record_button=None,
                 include_view_settings_button=None,
                 recording_options=None,
                 id=None,
                 **opts):
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
        if id is None:
            id = f"x3d-{uuid.uuid4()}"
        self.id = id
        self.profile = profile
        self.version = version
        self.opts = dict(opts)
        self.width = width
        self.height = height
        if figsize is not None:
            self.set_size_inches(*figsize)
        self.background = background
        self.shown = False
        self.recording_options = recording_options
        self.dynamic_loading = dynamic_loading
        self.include_export_button = include_export_button
        self.include_record_button = include_record_button
        self.include_view_settings_button = include_view_settings_button
        super().__init__()

    def __setitem__(self, key, value):
        """
        **LLM Docstring**

        Set a figure option by key.

        :param key: the option name
        :param value: the option value
        """
        self.opts[key] = value
    def __getitem__(self, item):
        """
        **LLM Docstring**

        Get a figure option by key.

        :param item: the option name
        :return: the option value
        """
        return self.opts[item]

    def clear(self, *, backend):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (X3D backend).

        """
        self.axes = []

    def close(self, *, backend):
        """
        **LLM Docstring**

        Close the figure (X3D backend).

        """
        self.clear(backend=backend)

    def create_inset(self, bbox, **kw) -> 'GraphicsAxes':
        """
        **LLM Docstring**

        Create an inset axes at the given bounding box (X3D backend).

        :param bbox: the inset bounding box
        :param kw: extra keyword options
        :return: the result
        """
        raise NotImplementedError("not possible")

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
        if (rows, cols, spans) != (1, 1, 1):
            raise NotImplementedError("can't create subcanvases")
        return self.add_axes(self.Axes(**kw))

    @classmethod
    def construct(cls, **kw) -> 'GraphicsFigure':
        """
        **LLM Docstring**

        Construct a figure of this backend type (X3D backend).

        :param kw: construction options
        :return: the result
        """
        return cls(**kw)

    def get_size_inches(self):
        """
        **LLM Docstring**

        Return the figure size in inches (X3D backend).

        :return: the result
        """
        return [self.width/DPI_SCALING, self.height/DPI_SCALING]
    def set_size_inches(self, w, h):
        """
        **LLM Docstring**

        Set the figure size in inches (X3D backend).

        :param w: the width in inches
        :param h: the height in inches
        """
        self.width, self.height = w*DPI_SCALING, h*DPI_SCALING
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
        return self.background
    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color (X3D backend).

        :param fg: the face color
        """
        self.background = fg
    def savefig(self, file, format=None, **opts):
        """
        **LLM Docstring**

        Save the figure to a file (X3D backend).

        :param file: the destination file/path
        :param format: the `format`
        :param opts: extra options
        """
        return self.to_x3d(**opts).dump(file)
    def prep_opts(self):
        """
        **LLM Docstring**

        Assemble the figure's options for X3D construction (size, profile/version,
        background, UI buttons, etc.).

        :return: the options dict
        :rtype: dict
        """
        return dict(
            self.opts,
            profile=self.profile,
            version=self.version,
            width=self.width,
            height=self.height,
            id=self.id,
            background=self.background,
            recording_options=self.recording_options,
            dynamic_loading=self.dynamic_loading,
            include_export_button=self.include_export_button,
            include_record_button=self.include_record_button,
            include_view_settings_button=self.include_view_settings_button
        )
    def to_x3d(self, **opts):
        """
        **LLM Docstring**

        Build the full X3D element from the figure's axes, resolving MathJax and onload
        scripts.

        :param opts: extra construction options
        :return: the X3D element
        """
        opts = dict(self.prep_opts(), **opts)
        if 'include_mathjax' not in opts:
            opts['include_mathjax'] = ([
                a.include_mathjax
                for a in self.axes
                if a.include_mathjax is not None
            ] + [False])[0]
        if 'onload_scripts' not in opts:
            opts['onload_scripts'] = sum((a.onloads for a in self.axes), [])
        return x3d.X3D(
            *[a.to_x3d() for a in self.axes],
            **opts
        )
    def to_widget(self, **opts):
        """
        **LLM Docstring**

        Render the figure as an interactive widget (X3D backend).

        :param opts: extra options
        :return: the result
        """
        return self.to_x3d(**opts).to_widget()
    def to_html(self):
        """
        **LLM Docstring**

        Render the figure to HTML (X3D backend).

        :return: the result
        """
        return self.to_widget().tostring()

    def animate_frames(self, frames: list['X3DAxes'], mode=None, **animation_opts):
        """
        **LLM Docstring**

        Animate a sequence of frames (X3D backend).

        :param frames: the animation frames
        :param mode: the `mode`
        :param animation_opts: animation options
        """
        frame_data = [
                    x3d.X3DGroup(f.children if hasattr(f, 'children') else f)
                    for f in frames
                ]
        if mode is None:
            try:
                animation = x3d.X3DInterpolatingAnimator.from_frames(
                    frame_data,
                    **animation_opts
                )
            except ValueError:
                animation = x3d.X3DListAnimator(
                    frame_data,
                    **animation_opts
                )
        elif mode == 'interpolated':
            animation = x3d.X3DInterpolatingAnimator.from_frames(
                frame_data,
                **animation_opts
            )
        elif mode == 'list':
            animation = x3d.X3DListAnimator(
                frame_data,
                **animation_opts
            )
        else:
            raise ValueError(f"bad mode {mode}")

        animator = X3DAxes(
            animation,
            **self.axes[0].prep_opts()
        )
        return x3d.X3D(animator.to_x3d(), **self.prep_opts())

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
        figure = self.Figure.construct(**kwargs)
        axes = figure.create_axes()
        return figure, axes

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
            return [], {}

        def begin_context(self):
            """
            **LLM Docstring**

            Enter the context, applying the theme.

            """
            return self

        def end_context(self, exc_type, exc_val, exc_tb):
            """
            **LLM Docstring**

            Exit the context, restoring the previous theme.

            :param exc_type: the exception type, if any
            :param exc_val: the exception value, if any
            :param exc_tb: the traceback, if any
            """
            ...

    def show_figure(self, graphics:X3DFigure, reshow=None):
        """
        **LLM Docstring**

        Display a figure via the backend (X3D backend).

        :param graphics: the `graphics`
        :param reshow: force a reshow of an already-shown figure
        """
        if not graphics.shown:
            from ..Jupyter.JHTML import JupyterAPIs
            dynamic_loading = JupyterAPIs().in_jupyter_environment()
            graphics.shown = True
            graphics.to_x3d().to_widget(dynamic_loading=dynamic_loading).display()

            # from ..Jupyter.JHTML.WidgetTools import JupyterAPIs
            #
            # display = JupyterAPIs.get_display_api()
            # html = graphics.to_x3d().to_widget().tostring()
            # return display.display(display.HTML(html))

    def get_interactive_status(self) -> 'bool':
        """
        **LLM Docstring**

        Return whether interactive mode is on (X3D backend).

        :return: the result
        """
        return True
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
        return []

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
        super().__init__()
        self.children = list(children)
        self.title = title
        self.background = background
        self.opts = opts
        self.mode = None
        for c in children:
            mode = c.attrs.get('mode')
            if mode is not None:
                self.mode = mode
                break

    @classmethod
    def canonicalize_opts(cls, opts):
        """
        **LLM Docstring**

        Normalize construction options into the backend's canonical form (SceneJSON backend).

        :param opts: the options to canonicalize
        """
        return opts

    def remove(self, *, backend):
        """
        **LLM Docstring**

        Tear down (remove) this axes from its figure (SceneJSON backend).

        """
        self.children = []
        self.title = ""
        self.background = "white"

    def clear(self, *, backend):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (SceneJSON backend).

        """
        self.children = []
        self.title = ""
        self.background = "white"

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
        return self.title
    def set_plot_label(self, val, **style):
        """
        **LLM Docstring**

        Set the plot title/label (SceneJSON backend).

        :param val: the label text
        :param style: label styling options
        """
        self.title = val

    def get_style_list(self):
        """
        **LLM Docstring**

        Return the per-series style cycle (SceneJSON backend).

        :return: the result
        """
        raise NotImplementedError("style list cyclers not supported")
    def set_style_list(self, props):
        """
        **LLM Docstring**

        Set the per-series style cycle (SceneJSON backend).

        :param props: the style cycle
        """
        raise NotImplementedError("style list cyclers not supported")

    def get_frame_visible(self):
        """
        **LLM Docstring**

        Return which frame (spine) edges are drawn (SceneJSON backend).

        :return: the result
        """
        raise NotImplementedError(...)
    def set_frame_visible(self, frame_spec):
        """
        **LLM Docstring**

        Set which frame (spine) edges are drawn (SceneJSON backend).

        :param frame_spec: the per-edge visibility spec
        """
        ...
        # raise NotImplementedError(...)

    def get_frame_style(self):
        """
        **LLM Docstring**

        Return the frame (spine) styling (SceneJSON backend).

        :return: the result
        """
        raise NotImplementedError(...)
    def set_frame_style(self, frame_spec):
        """
        **LLM Docstring**

        Set the frame (spine) styling (SceneJSON backend).

        :param frame_spec: the frame styling
        """
        ...
        # raise NotImplementedError(...)

    def get_xlabel(self):
        """
        **LLM Docstring**

        Return the x-axis label (SceneJSON backend).

        :return: the result
        """
        raise NotImplementedError(...)
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
        raise NotImplementedError(...)
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
        raise NotImplementedError(...)
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
        raise NotImplementedError(...)
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
        raise NotImplementedError(...)
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
        return []
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
        return []
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
        return []
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
        return {}
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
        return {}
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
        return {}
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
        raise NotImplementedError(...)
    def set_bbox(self, bbox):
        """
        **LLM Docstring**

        Set the axes bounding box (SceneJSON backend).

        :param bbox: the bounding box
        """
        raise NotImplementedError(...)

    def get_facecolor(self):
        """
        **LLM Docstring**

        Return the background/face color (SceneJSON backend).

        :return: the result
        """
        return self.background
    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color (SceneJSON backend).

        :param fg: the face color
        """
        self.background = fg

    def get_padding(self):
        """
        **LLM Docstring**

        Return the axes padding (SceneJSON backend).

        :return: the result
        """
        raise NotImplementedError(...)

    def get_view_settings(self):
        """
        **LLM Docstring**

        Return the 3D camera/view settings (SceneJSON backend).

        :return: the result
        """
        return self.opts.get('viewpoint', {})
    def set_view_settings(self, **values):
        """
        **LLM Docstring**

        Set the 3D camera/view settings (SceneJSON backend).

        :param values: keyword options
        """
        new_opts = {
            k:v for k,v in dict(self.opts.get('viewpoint', {}), **values).items()
            if v is not None
        }
        if len(new_opts) == 0 and 'viewpoint' in self.opts:
            del self.opts['viewpoint']
        else:
            self.opts['viewpoint'] = new_opts

    def draw_line(self, points, **styles):
        """
        **LLM Docstring**

        Draw a line/polyline through the given points (SceneJSON backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        points = np.asanyarray(points)
        if points.shape[-1] == 3:
            self.mode = '3d'
        else:
            self.mode = '2d'
        line_set = sceneJSON.Line(points=points.tolist(), mode=self.mode, **styles)
        self.children.append(line_set)

        return line_set

    def draw_disk(self, points, rads=1, **styles):
        """
        **LLM Docstring**

        Draw a filled disk at the given position(s) (SceneJSON backend).

        :param points: the points to draw
        :param rads: the `rads`
        :param styles: the styling options
        """
        points = np.asanyarray(points)
        if points.shape[-1] == 3:
            self.mode = '3d'
        else:
            self.mode = '2d'
        rads = np.asanyarray(rads).tolist()
        disk_set = sceneJSON.Disk(center=points.tolist(), radius=rads, mode=self.mode, **styles)
        self.children.append(disk_set)

        return disk_set

    def draw_arrow(self, points, radius=.1, **styles):
        """
        **LLM Docstring**

        Draw an arrow from the given points (SceneJSON backend).

        :param points: the points to draw
        :param radius: the `radius`
        :param styles: the styling options
        """
        points = np.asanyarray(points)
        if points.shape[-1] == 3:
            self.mode = '3d'
        else:
            self.mode = '2d'
        arrows = sceneJSON.Arrow(points=points.tolist(), radius=radius, mode=self.mode, **styles)
        self.children.append(arrows)
        return arrows

    def draw_text(self, points, vals, **styles):
        """
        **LLM Docstring**

        Draw text at the given position(s) (SceneJSON backend).

        :param points: the points to draw
        :param vals: the text string(s)
        :param styles: the styling options
        """
        points = np.asanyarray(points)
        if points.shape[-1] == 3:
            self.mode = '3d'
        else:
            self.mode = '2d'
        text = sceneJSON.Text(centers=points.tolist(), text=vals, mode=self.mode, **styles)
        self.children.append(text)
        return text

    def draw_rect(self, points, **styles):
        """
        **LLM Docstring**

        Draw a rectangle from the given points (SceneJSON backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        points = np.asanyarray(points)
        if points.shape[-1] == 3:
            self.mode = '3d'
        else:
            self.mode = '2d'
        rects = sceneJSON.Rectangle(points=points.tolist(), mode=self.mode, **styles)
        self.children.append(rects)

        return rects

    def draw_poly(self, points, **styles):
        """
        **LLM Docstring**

        Draw a filled polygon from the given points (SceneJSON backend).

        :param points: the points to draw
        :param styles: the styling options
        """
        points = np.asanyarray(points)
        if points.shape[-1] == 3:
            self.mode = '3d'
        else:
            self.mode = '2d'
        rects = sceneJSON.Polygon(points=points.tolist(), mode=self.mode, **styles)
        self.children.append(rects)

        return rects

    def draw_sphere(self, centers, rads, **styles):
        """
        **LLM Docstring**

        Draw a sphere (or spheres) at the given center(s) with the given radii (SceneJSON backend).

        :param centers: the `centers`
        :param rads: the sphere radii
        :param styles: the styling options
        """
        centers = np.asanyarray(centers)
        if centers.shape[-1] == 3:
            self.mode = '3d'
        else:
            self.mode = '2d'
        spheres = sceneJSON.Sphere(center=centers.tolist(), radius=rads, mode=self.mode, **styles)
        self.children.append(spheres)

        return spheres

    def draw_cylinder(self, starts, ends, rads, **styles):
        """
        **LLM Docstring**

        Draw a cylinder between two endpoints (SceneJSON backend).

        :param starts: the `starts`
        :param ends: the `ends`
        :param rads: the `rads`
        :param styles: the styling options
        """
        starts = np.asanyarray(starts)
        if starts.shape[-1] == 3:
            self.mode = '3d'
        else:
            self.mode = '2d'
        ends = np.asanyarray(ends).tolist()
        rads = np.asanyarray(rads).tolist()
        cyls = sceneJSON.Cylinder(start=starts.tolist(), end=ends, radius=rads, mode=self.mode, **styles)
        self.children.append(cyls)

        return cyls

    def to_json(self):
        """
        **LLM Docstring**

        Serialize the axes (its children and options) to the scene-JSON representation.

        :return: the scene-JSON object
        :rtype: dict
        """
        opts = dict(
            self.opts,
            background=self.background,
            title=self.title
        )
        return sceneJSON.Scene(
            self.children,
            **opts
        )

class SceneJSONFigure(GraphicsFigure):
    Axes = SceneJSONAxes

    def __init__(self, width=640, height=500,
                 background='white', figsize=None, profile='Immersive', version='3.3',
                 id=None,
                 **opts):
        """
        **LLM Docstring**

        Set up a SceneJSON figure holding its axes and options.

        :param args: positional figure arguments
        :param opts: figure options
        """
        if id is None:
            id = f"scene-{uuid.uuid4()}"
        self.id = id
        self.profile = profile
        self.version = version
        self.opts = dict(opts)
        self.width = width
        self.height = height
        if figsize is not None:
            self.set_size_inches(*figsize)
        self.background = background
        self.shown = False
        super().__init__()

    def __setitem__(self, key, value):
        """
        **LLM Docstring**

        Set a figure option by key.

        :param key: the option name
        :param value: the option value
        """
        self.opts[key] = value
    def __getitem__(self, item):
        """
        **LLM Docstring**

        Get a figure option by key.

        :param item: the option name
        :return: the option value
        """
        return self.opts[item]

    def clear(self, *, backend):
        """
        **LLM Docstring**

        Clear the drawn content from this axes/figure (SceneJSON backend).

        """
        self.axes = []

    def close(self, *, backend):
        """
        **LLM Docstring**

        Close the figure (SceneJSON backend).

        """
        self.clear(backend=backend)

    def create_inset(self, bbox, **kw) -> 'GraphicsAxes':
        """
        **LLM Docstring**

        Create an inset axes at the given bounding box (SceneJSON backend).

        :param bbox: the inset bounding box
        :param kw: extra keyword options
        :return: the result
        """
        raise NotImplementedError("not possible")

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
        if (rows, cols, spans) != (1, 1, 1):
            raise NotImplementedError("can't create subcanvases")
        return self.add_axes(self.Axes(**kw))

    @classmethod
    def construct(cls, **kw) -> 'GraphicsFigure':
        """
        **LLM Docstring**

        Construct a figure of this backend type (SceneJSON backend).

        :param kw: construction options
        :return: the result
        """
        return cls(**kw)

    def get_size_inches(self):
        """
        **LLM Docstring**

        Return the figure size in inches (SceneJSON backend).

        :return: the result
        """
        return [self.width/DPI_SCALING, self.height/DPI_SCALING]
    def set_size_inches(self, w, h):
        """
        **LLM Docstring**

        Set the figure size in inches (SceneJSON backend).

        :param w: the width in inches
        :param h: the height in inches
        """
        self.width, self.height = w*DPI_SCALING, h*DPI_SCALING
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
        return self.background
    def set_facecolor(self, fg):
        """
        **LLM Docstring**

        Set the background/face color (SceneJSON backend).

        :param fg: the face color
        """
        self.background = fg
    def savefig(self, file, format=None, **opts):
        """
        **LLM Docstring**

        Save the figure to a file (SceneJSON backend).

        :param file: the destination file/path
        :param format: the `format`
        :param opts: extra options
        """
        return self.to_json(**opts).dump(file)
    def to_json(self, **opts):
        """
        **LLM Docstring**

        Serialize the whole figure (its axes and options) to the scene-JSON
        representation.

        :return: the scene-JSON object
        :rtype: dict
        """
        opts = dict(
            self.opts,
            profile=self.profile,
            version=self.version,
            width=self.width,
            height=self.height,
            id=self.id,
            **opts
        )
        mode = '2d'
        for a in self.axes:
            if a.mode == '3d': mode = '3d'
        if mode == '3d':
            wrapper = sceneJSON.Graphics3D
        else:
            wrapper = sceneJSON.Graphics

        return wrapper(
            *[a.to_json() for a in self.axes],
            **opts
        )

    def animate_frames(self, frames: list['SceneJSONAxes'], **animation_opts):
        """
        **LLM Docstring**

        Animate a sequence of frames (SceneJSON backend).

        :param frames: the animation frames
        :param animation_opts: animation options
        """
        frames = [
            SceneJSONAxes(*f) if not isinstance(f, SceneJSONAxes) else f
            for f in frames
        ]
        wrapper = sceneJSON.Graphics if frames[0].mode == '2d' else sceneJSON.Graphics3D
        return sceneJSON.Animation(
            [wrapper(f.to_json()) for f in frames],
            **animation_opts
        )
        # animator = X3DAxes(
        #     x3d.X3DListAnimator(
        #         [
        #             x3d.X3DGroup(f.children if hasattr(f, 'children') else f)
        #             for f in frames
        #         ],
        #         **animation_opts
        #     ),
        #     **self.axes[0].opts
        # )
        # opts = dict(
        #     self.opts,
        #     profile=self.profile,
        #     version=self.version,
        #     width=self.width,
        #     height=self.height
        # )
        # return x3d.X3D(animator.to_x3d(), **opts).to_widget()

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
        figure = self.Figure.construct(**kwargs)
        axes = figure.create_axes()
        return figure, axes

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
            return [], {}

        def begin_context(self):
            """
            **LLM Docstring**

            Enter the context, applying the theme.

            """
            return self

        def end_context(self, exc_type, exc_val, exc_tb):
            """
            **LLM Docstring**

            Exit the context, restoring the previous theme.

            :param exc_type: the exception type, if any
            :param exc_val: the exception value, if any
            :param exc_tb: the traceback, if any
            """
            ...

    def show_figure(self, graphics:SceneJSONFigure, reshow=None):
        """
        **LLM Docstring**

        Display a figure via the backend (SceneJSON backend).

        :param graphics: the `graphics`
        :param reshow: force a reshow of an already-shown figure
        """
        if not graphics.shown:
            graphics.shown = True

            from ..Jupyter import JHTML
            #
            # display = JupyterAPIs.get_display_api()
            return JHTML.Pre(graphics.to_json().tostring(indent=2)).display()
            # return html.display()

    def get_interactive_status(self) -> 'bool':
        """
        **LLM Docstring**

        Return whether interactive mode is on (SceneJSON backend).

        :return: the result
        """
        return True
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
        return []
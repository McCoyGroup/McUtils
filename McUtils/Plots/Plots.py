"""
Provides various types of plots and plotting utilities
"""
import collections
from typing import Callable

from .Graphics import Graphics, Graphics3D, GraphicsGrid
from .Backends import GraphicsAxes, GraphicsFigure
from .. import Devutils as dev
from .. import Numputils as nput
from . import Colors as colops
import numpy as np
import itertools
# import matplotlib.figure
# import matplotlib.axes

__all__ = [
    "Plot", "DataPlot", "ArrayPlot", "TensorPlot",
    "Plot2D", "ListPlot2D",
    "Plot3D", "ListPlot3D",
    "CompositePlot",
    "resolve_plotter",
    "plot_generic",
    "plot_multi"
]

######################################################################################################
#
#                                    'adaptive' function sampling
#
#
# region function application
def _apply_f(f, grid):
    """
    **LLM Docstring**

    Evaluate a function on a grid, falling back to `np.vectorize` if a direct call
    fails.

    :param f: the function to evaluate
    :type f: Callable
    :param grid: the input grid
    :type grid: np.ndarray
    :return: the function values
    :rtype: np.ndarray
    """
    try:
        vals = f(grid)
    except:
        vals = np.vectorize(f)(grid)

    return vals

def _semi_adaptive_sample_func(f, xmin, xmax, npts=150, max_refines=10, der_cut=10**5):
    """
    **LLM Docstring**

    Sample a 1-D function over `[xmin, xmax]`, refining the grid (doubling the point
    count) until the finite-difference derivative stays below a cutoff or the refine
    limit is hit.

    :param f: the function to sample
    :type f: Callable
    :param xmin: the lower bound
    :param xmax: the upper bound
    :param npts: the initial number of points
    :type npts: int
    :param max_refines: the maximum number of refinements
    :type max_refines: int
    :param der_cut: the derivative-magnitude cutoff
    :return: `(grid, values, npts, refines)`
    :rtype: tuple
    """

    refines = 0
    der_good = False

    try:
        from ..Zachary import finite_difference
    except ImportError:
        pass
    else:
        while refines < max_refines and not der_good:
            grid = np.linspace(xmin, xmax, npts)
            vals = _apply_f(f, grid)
            ders = finite_difference(grid, vals, 1, 5)
            der_good = not np.any(abs(ders) > der_cut)
            npts *= 2
            refines += 1

    if refines == 0:  # edge case
        grid = np.linspace(xmin, xmax, npts)
        vals = _apply_f(f, grid)

    return grid, vals, npts, refines

def _semi_adaptive_sample_func2(f, xmin, xmax, ymin, ymax, npts=15, max_refines=10, der_cut=10**5):
    """
    **LLM Docstring**

    Sample a 2-D function over a rectangle, refining the mesh until the
    finite-difference derivative stays below a cutoff or the refine limit is hit.

    :param f: the function to sample
    :type f: Callable
    :param xmin: the x lower bound
    :param xmax: the x upper bound
    :param ymin: the y lower bound
    :param ymax: the y upper bound
    :param npts: the initial per-axis point count
    :type npts: int
    :param max_refines: the maximum number of refinements
    :type max_refines: int
    :param der_cut: the derivative-magnitude cutoff
    :return: `(grid, values, npts, refines)`
    :rtype: tuple
    """
    from ..Zachary import finite_difference

    refines = 0
    der_good = False
    try:
        from ..Zachary import finite_difference
    except ImportError:
        pass
    else:
        while refines < max_refines and not der_good:
            grid = np.array(np.meshgrid(np.linspace(xmin, xmax, npts), np.linspace(ymin, ymax, npts))).T
            vals = _apply_f(f, grid)
            ders = finite_difference(grid, vals, (1, 1), (5, 5))
            der_good = not np.any(abs(ders) > der_cut)
            npts *= 2
            refines += 1

    if refines == 0:  # edge case
        grid = np.linspace(xmin, xmax, npts)
        vals = _apply_f(f, grid)

    return grid, vals, npts, refines
# endregion


######################################################################################################
#
#                                    Plot data methods
#
#
# region plot data prep
def _interp2DData(gpts, **opts):
    """
    **LLM Docstring**

    Interpolate scattered `(x, y, z)` points onto a regular 2-D mesh via
    `scipy.interpolate.griddata`.

    :param gpts: the `(n, 3)` scattered points
    :type gpts: np.ndarray
    :param opts: options forwarded to `griddata`
    :return: `(xmesh, ymesh, values)`
    :rtype: tuple
    """
    from scipy.interpolate import griddata

    x = np.sort(gpts[:, 0])
    y = np.sort(gpts[:, 1])

    xmin = np.min(x); xmax = np.max(x)

    xdiffs = np.abs(np.diff(x)); xh = np.min(xdiffs[np.nonzero(xdiffs)])
    ymin = np.min(y); ymax = np.max(y)
    ydiffs = np.abs(np.diff(y)); yh = np.min(xdiffs[np.nonzero(ydiffs)])

    num_x = (xmin - xmax) / xh
    if 5 > num_x or num_x < 10000:  # don't want to get too wild
        num_x = 100  # okay but let's get a little wild
    num_y = (ymin - ymax) / yh
    if 5 > num_y or num_y < 10000:  # don't want to get too wild
        num_y = 100  # okay but let's get a little wild

    # import sys
    # print(num_x, num_y, file = sys.stderr)

    xmesh = np.linspace(xmin, xmax, num_x); ymesh = np.linspace(ymin, ymax, num_y)
    xmesh, ymesh = np.meshgrid(xmesh, ymesh)
    mesh = np.array((xmesh, ymesh)).T
    vals = griddata(gpts[:, (0, 1)], gpts[:, 2], mesh, **opts)

    return xmesh, ymesh, vals.T

def _get_2D_plotdata(func, xrange):
    """
    **LLM Docstring**

    Resolve 2-D plot inputs into `(xrange, values)`, handling sympy expressions,
    explicit `(x, y)` arrays, sampled ranges, and adaptive sampling of a callable.

    :param func: a callable, sympy expression, or the x data
    :param xrange: the x range/values (or the y data)
    :return: `(xrange, values)`
    :rtype: tuple
    """
    if hasattr(func, 'subs'):
        from sympy import lambdify
        sym, xrange = xrange
        xrange = np.arange(*xrange)
        fvalues = lambdify([sym], func)(xrange)
    elif not callable(func):
        fvalues = xrange
        xrange = func
    else:
        if len(xrange) == 3 and abs(xrange[2]) < abs(xrange[1] - xrange[0]):
            xrange = np.arange(*xrange)
            fvalues = _apply_f(func, xrange)
        elif len(xrange) > 2:
            fvalues = _apply_f(func, xrange)
        else:
            res = _semi_adaptive_sample_func(func, *xrange)
            xrange = res[0]
            fvalues = res[1]
    return xrange, fvalues

def _get_3D_plotdata(func, xrange, yrange):
    """
    **LLM Docstring**

    Resolve 3-D plot inputs into `(xrange, yrange, values)`, handling explicit
    arrays, meshed ranges, and adaptive sampling of a callable.

    :param func: a callable or the x data
    :param xrange: the x range/values
    :param yrange: the y range/values
    :return: `(xrange, yrange, values)`
    :rtype: tuple
    """
    if not callable(func):
        fvalues = yrange
        yrange = xrange
        xrange = func
    else:
        if len(xrange) == 3 and abs(xrange[2]) < abs(xrange[1] - xrange[0]):
            xrange = np.arange(*xrange)
            yrange = np.arange(*yrange)
            xrange, yrange = mesh = np.meshgrid(xrange, yrange)
            fvalues = _apply_f(func, mesh)
        elif len(xrange) > 2 and len(yrange) > 2:
            xrange, yrange = mesh = np.meshgrid(xrange, yrange)
            fvalues = _apply_f(func, mesh)
        else:
            res = _semi_adaptive_sample_func2(func, *xrange, *yrange)
            xrange, yrange = res[0].T
            fvalues = res[1]

    return xrange, yrange, fvalues
# endregion

######################################################################################################
#
#                                    Unified PlotBase class
#
#
# Never implemented this

######################################################################################################
#
#                                    2D Plots on 2D Axes
#
#
class Plot(Graphics):
    """
    The base plotting class to interface into matplotlib or (someday 3D) VTK.
    In the future hopefully we'll be able to make a general-purpose `PlottingBackend` class that doesn't need to be `matplotlib` .
    Builds off of the `Graphics` class to make a unified and convenient interface to generating plots.
    Some sophisticated legwork unfortunately has to be done vis-a-vis tracking constructed lines and other plotting artefacts,
    since `matplotlib` is designed to infuriate.
    """

    line_params = {
        "linewidth", "linestyle", "color", "marker", "markersize",
        "markeredgewidth", "markeredgecolor", "markerfacecolor", "markerfacecoloralt",
        "fillstyle", "antialiased", "dash_capstyle", "solid_capstyle",
        "dash_joinstyle", "solid_joinstyle", "pickradius", "drawstyle", "markevery",
        'gid', "zorder", 'label'
    }
    patch_parms = {
        "agg_filter", "alpha", "animated", "antialiased", "capstyle",
        "clip_box", "clip_on", "clip_path", "color", "edgecolor", "facecolor",
        "figure", "fill", "gid", "hatch", "in_layout", "joinstyle",
         "label", "linestyle", "linewidth", "path_effects",
        "picker", "rasterized", "sketch_params", "snap",
        "transform", "url", "visible", "zorder"
    }

    opt_keys = Graphics.opt_keys | {"plot_style", "display_format", 'prep_colors', 'color_value_scaling'}

    default_plot_style = {}
    default_colormap = 'viridis'
    style_mapping = {"format":"fmt"}
    known_styles = {"fmt"} | line_params
    method = "plot"
    def __init__(self,
                 *params,
                 method=None,
                 figure=None, axes=None, subplot_kw=None,
                 plot_style=None, theme=None,
                 display_format=None,
                 **opts
                 ):
        """
        :param params: _empty_ or _x_, _y_ arrays or _function_, _xrange_
        :type params:
        :param plot_style: the plot styling options to be fed into the plot method
        :type plot_style: dict | None
        :param method: the method name as a string or functional form of the method to plot
        :type method: str | function
        :param figure: the Graphics object on which to plot (None means make a new one)
        :type figure: Graphics | None
        :param axes: the axes on which to plot (used in constructing a Graphics, None means make a new one)
        :type axes: None
        :param subplot_kw: the keywords to pass on when initializing the plot
        :type subplot_kw: dict | None
        :param colorbar: whether to use a colorbar or what options to pass to the colorbar
        :type colorbar: None | bool | dict
        :param opts: options to be fed in when initializing the Graphics
        :type opts:
        """

        self.graphics = None

        # we're gonna set things up so that we can have delayed evaluation of the plotting.
        # i.e. a Plot can be initialized but then do all its plotting later
        if plot_style is None:
            plot_style = {}
        for k,v in self.style_mapping.items():
            if k in opts:
                opts[v] = opts[k]
                del opts[k]
        for k in self.known_styles:
            if k in opts:
                plot_style[k] = opts[k]
                del opts[k]
        for k in self.default_plot_style:
            if k not in plot_style:
                plot_style[k] = self.default_plot_style[k]
        self._plot_style = plot_style
        self.plot_opts = opts
        self._initialized = False
        self._data = None
        self.display_format = display_format

        super().__init__(figure=figure, axes=axes, theme=theme, subplot_kw=subplot_kw, **opts)
        self._init_opts['plot_style'] = plot_style
        if method is None:
           method = self.method
        if isinstance(method, str):
            method = self.axes.get_plotter(method)
        self._method = method

        if len(params) > 0:
            self.plot(*params)

    known_keys = Graphics.known_keys | {
        'method',
        'plot_style',
        'display_format',
        'insert_default_styles'
    }
    @classmethod
    def filter_options(cls, opts, allowed=None):
        """
        **LLM Docstring**

        Return the subset of options recognized by this plot type (its known styles and
        keys, or an explicit allowed set).

        :param opts: the options to filter
        :type opts: dict
        :param allowed: an explicit allowed-key set
        :type allowed: set | None
        :return: the filtered options
        :rtype: dict
        """
        new = {}
        if allowed is None:
            allowed = cls.known_styles | cls.known_keys
        for k in opts.keys() & allowed:
                new[k] = opts[k]
        return new
    def _check_opts(self, opts):
        """
        **LLM Docstring**

        Raise if any option keys aren't among this plot's known styles or keys.

        :param opts: the options to check
        :type opts: dict
        :raises ValueError: for unknown option keys
        """
        diff = opts.keys() - (self.known_styles | self.known_keys)
        if len(diff) > 0:
            raise ValueError("unknown options for {}: {}".format(
                type(self).__name__, list(diff)
            ))

    def _initialize(self):
        """
        **LLM Docstring**

        Mark the plot initialized and apply its (non-style) figure options.
        """
        self._initialized = True
        self.set_options(**self.plot_opts)

    def _get_plot_data(self, func, xrange):
        """
        **LLM Docstring**

        Resolve the plot's positional arguments into the `(xrange, values)` the plot
        method expects.

        :param func: a callable or the x data
        :param xrange: the x range/values
        :return: the resolved plot data
        :rtype: tuple
        """
        xrange, fvalues = _get_2D_plotdata(func, xrange)
        return xrange, fvalues

    def _plot_data(self, *data, **plot_style):
        """
        **LLM Docstring**

        Call the backend plot method on the resolved plot data.

        :param data: the positional plot arguments
        :param plot_style: the styling options
        :return: the backend graphics object
        """
        return self._method(*self._get_plot_data(*data), **plot_style)

    def prep_styles(self, c=None, edgecolors=None, facecolors=None, cmap=None, prep_colors=False, color_value_rescaling=True, **styles):
        """
        **LLM Docstring**

        Normalize color-related styling: when a colormap is supplied and color values are
        numeric, rescale them and map them through the colormap (into `c`, `facecolors`,
        or `edgecolors`), returning the cleaned style dict.

        :param c: the point colors/values
        :param edgecolors: the edge colors/values
        :param facecolors: the face colors/values
        :param cmap: the colormap (name, dict spec, or callable)
        :param prep_colors: actually map numeric values through the colormap
        :type prep_colors: bool
        :param color_value_rescaling: rescale numeric color values before mapping
        :type color_value_rescaling: bool
        :param styles: the remaining styling options
        :return: the prepared style dict
        :rtype: dict
        """
        if (
                prep_colors
                and cmap is not None
                and (
                    (c is not None and nput.is_numeric(c[0]))
                    or (edgecolors is not None and nput.is_numeric(facecolors[0]))
                    or (facecolors is not None and nput.is_numeric(edgecolors[0]))
                )
        ):
            if not callable(cmap) and not isinstance(cmap, dict):
                cmap = {'palette': cmap}
            if isinstance(cmap, dict):
                if c is not None and nput.is_numeric(c[0]):
                    if color_value_rescaling:
                        c = nput.vec_rescale(c)
                    c = colops.prep_color(blending=c, **cmap)
                if facecolors is not None and nput.is_numeric(facecolors[0]):
                    if color_value_rescaling:
                        facecolors = nput.vec_rescale(facecolors)
                    facecolors = colops.prep_color(blending=facecolors, **cmap)
                if edgecolors is not None and nput.is_numeric(edgecolors[0]):
                    if color_value_rescaling:
                        edgecolors = nput.vec_rescale(edgecolors)
                    edgecolors = colops.prep_color(blending=edgecolors, **cmap)
            else:
                cmap: Callable
                if c is not None and nput.is_numeric(c[0]):
                    if color_value_rescaling:
                        c = nput.vec_rescale(c)
                    c = cmap(c)
                if facecolors is not None and nput.is_numeric(facecolors[0]):
                    if color_value_rescaling:
                        facecolors = nput.vec_rescale(facecolors)
                    facecolors = cmap(facecolors)
                if edgecolors is not None and nput.is_numeric(edgecolors[0]):
                    if color_value_rescaling:
                        edgecolors = nput.vec_rescale(edgecolors)
                    edgecolors = cmap(edgecolors)

            cmap = None
            # TODO: attach colorbars
            # sm = cm.ScalarMappable(cmap='viridis', norm=norm)
            # sm.set_array([])

        new_opts = {
            k:v for k,v in
            {'c':c, 'facecolors':facecolors, 'edgecolors':edgecolors, 'cmap':cmap}.items()
            if v is not None
        } | styles
        return new_opts
    def plot(self, *params, insert_default_styles=True, **plot_style):
        """
        Plots a set of data & stores the result
        :return: the graphics that matplotlib made
        :rtype:
        """
        if insert_default_styles:
            plot_style = dict(self.plot_style, **plot_style)
        self._data = (params, plot_style)
        plot_style = self.prep_styles(**plot_style)
        self.graphics = self._plot_data(*params, **plot_style)
        if not self._initialized:
            self._initialize()
            if self.display_format is not None:
                self.figure.figure.default_display_format = self.display_format
        return self.graphics
    @property
    def artists(self):
        """
        **LLM Docstring**

        The backend artist objects produced by the plot (as a list).

        :return: the artists
        :rtype: list | None
        """
        if self.graphics is None or isinstance(self.graphics, list):
            return self.graphics
        else:
            return [self.graphics]

    # def copy(self):
    #     return self.change_figure(None)
    def _change_figure(self, new, *init_args, **init_kwargs):
        """Creates a copy of the object with new axes and a new figure

        :return:
        :rtype:
        """
        # print(init_kwargs)
        # print(self._data[0], init_args)
        # print(init_kwargs, self._init_opts)
        return super()._change_figure(new, *self._data[0], *init_args, **init_kwargs)

    def clear(self):
        """
        Removes the plotted data
        """
        for g in self.graphics:
            self.axes.remove(g)
        self.graphics=None
    def restyle(self, **plot_style):
        """
        Replots the data with updated plot styling
        :param plot_style:
        :type plot_style:
        """
        self.clear()
        self.plot(*self.data, **plot_style)

    @property
    def data(self):
        """
        The data that we plotted
        """
        if self._data is None:
            raise ValueError("{} hasn't been plotted in the first place...")
        return self._data[0]
    @property
    def plot_style(self):
        """
        The styling options applied to the plot
        """
        if self._data is None:
            style = self._plot_style
        else:
            style = self._data[1]
        return style

    def add_colorbar(self, graphics=None, norm=None,  **kw):
        """
        Adds a colorbar to the plot
        """
        if self._initialized:
            if graphics is None and norm is None:
                graphics = self.graphics
            return super().add_colorbar(graphics=graphics, **kw)

    def set_graphics_properties(self, *which, **kw):
        """
        **LLM Docstring**

        Set backend properties on the plot's artists (all of them, or the selected
        indices).

        :param which: the artist indices to modify (all if empty)
        :param kw: the properties to set
        """
        if isinstance(self.graphics, tuple):
            for n,g in enumerate(self.graphics):
                if len(which) == 0 or n in which:
                    self.axes.set_graphics_properties(g, **kw)
        else:
            self.axes.set_graphics_properties(self.graphics, **kw)


    @classmethod
    def merge(cls, main, other, *rest, **kwargs):
        """
        **LLM Docstring**

        Combine this plot with others into a `CompositePlot`.

        :param main: the first plot
        :param other: the second plot
        :param rest: additional plots
        :param kwargs: options for the composite
        :return: the composite plot
        :rtype: CompositePlot
        """
        return CompositePlot(main, other, *rest, **kwargs)

    plot_classes = {}
    @classmethod
    def resolve_method(cls, mpl_name):
        """
        **LLM Docstring**

        Look up the registered plot class for a backend method name.

        :param mpl_name: the method/class name
        :type mpl_name: str
        :return: the plot class
        :rtype: type
        """
        return cls.plot_classes[mpl_name]
    # @classmethod
    # def merge_plots(cls, *plots, **styles):
    #     ...
    @classmethod
    def register(cls, plot_class):
        """
        **LLM Docstring**

        Register a plot class in the class registry, keyed by its backend method name (or
        class name if the method is already registered). Usable as a decorator.

        :param plot_class: the plot class to register
        :type plot_class: type
        :return: the registered class
        :rtype: type
        """
        if plot_class.method in cls.plot_classes:
            cls.plot_classes[plot_class.__name__] = plot_class
        else:
            cls.plot_classes[plot_class.method] = plot_class
        return plot_class
Plot.register(Plot)

class CompositePlot:
    def __init__(self, main, other, *rest, **kwargs):
        """
        **LLM Docstring**

        Hold several plots to be merged onto a shared figure.

        :param main: the first plot
        :param other: the second plot
        :param rest: additional plots
        :param kwargs: options applied when merging
        """
        self.kwargs = kwargs
        self.plots = [main, other, *rest]
    def merge(self, **kwargs):
        """
        **LLM Docstring**

        Merge the held plots onto a shared new figure (re-hosting each onto the first's
        figure).

        :param kwargs: options for the shared figure
        :return: the merged base plot
        :rtype: Graphics
        """
        base = self.plots[0].change_figure(None, **kwargs)
        for p in self.plots[1:]:
            p.change_figure(base)
        return base
    def show(self, interactive=True):
        """
        **LLM Docstring**

        Merge the plots and display the result.

        :param interactive: show interactively
        :type interactive: bool
        """
        self._ref = self.merge(interactive=interactive, **self.kwargs)
        # self._ref.pyplot.mpl_connect()
        self._ref.show()
    def _ipython_display_(self):
        """
        **LLM Docstring**

        Display the composite plot in IPython.
        """
        self.show()

@Plot.register
class FilledPlot(Plot):
    """
    Inherits from `Plot`.
    Plots a bunch of x values against a bunch of y values using the `scatter` method.
    """
    known_styles = { "where", "interpolate", "step", "data" } | Plot.patch_parms
    method = "fill_between"

@Plot.register
class ScatterPlot(Plot):
    """
    Inherits from `Plot`.
    Plots a bunch of x values against a bunch of y values using the `scatter` method.
    """
    known_styles = { "s", "c", "marker", "cmap", "norm", "vmin", "vmax",
                     "linewidths", "edgecolors", 'facecolors', "plotnonfinite", "data"} | (
            Plot.patch_parms - {'linewidth', 'edgecolor', 'facecolor'}
    ) | {'filled'}
    style_mapping = {"color":"c", "marker_size":"s"}
    method = "scatter"

    def prep_styles(self, cmap=None, c=None, facecolors=None, edgecolors=None, filled=None, prep_colors=False, **etc):
        """
        **LLM Docstring**

        Resolve scatter-specific color handling (filled vs open markers, moving colors
        between `c`/`facecolors`/`edgecolors`) before delegating to the base style prep.

        :param cmap: the colormap
        :param c: the point colors/values
        :param facecolors: the face colors
        :param edgecolors: the edge colors
        :param filled: draw filled (vs open) markers
        :type filled: bool | None
        :param prep_colors: map numeric values through the colormap
        :type prep_colors: bool
        :param etc: the remaining styling options
        :return: the prepared style dict
        :rtype: dict
        """
        if filled:
            if c is None and facecolors is None:
                c = edgecolors
                edgecolors = None
        elif filled is not None:
            if cmap is None:
                cmap = self.default_colormap
            if c is not None:
                facecolors = 'none'
                edgecolors = c
                prep_colors = True
                c = None
        else:
            if c is not None:
                if facecolors is not None:
                    if edgecolors is None:
                        edgecolors = c
                        prep_colors = True
                    c = None
                elif edgecolors is not None:
                    facecolors = c
                    prep_colors = True
                    c = None

        return super().prep_styles(prep_colors=prep_colors, cmap=cmap, c=c, facecolors=facecolors, edgecolors=edgecolors, **etc)

class ListScatterPlot(ScatterPlot):
    """
    Inherits from `Plot`.
    Plots a bunch of (x, y) points using the `scatter` method.
    """
    def __init__(self, griddata, **opts):
        """
        **LLM Docstring**

        Build a scatter plot from an `(n, 2)` array of `(x, y)` points.

        :param griddata: the points
        :type griddata: np.ndarray
        :param opts: plot options
        """
        super().__init__(griddata[:, 0], griddata[:, 1], **opts)

@Plot.register
class ErrorBarPlot(Plot):
    """
    Inherits from `Plot`.
    Plots error bars using the `errorbar` method.
    """
    known_styles = {"yerr", "xerr", "fmt", "ecolor", "elinewidth", "capsize", "barsabove",
    "lolims", "uplims", "xlolims", "xuplims", "errorevery", "capthick", "data"} | Plot.known_styles
    method = "errorbar"
class ListErrorBarPlot(ErrorBarPlot):
    """A Plot that pulls the errorbar data from a list"""
    def __init__(self, griddata, **opts):
        """
        **LLM Docstring**

        Build an error-bar plot from an `(n, 2)` array of `(x, y)` points.

        :param griddata: the points
        :type griddata: np.ndarray
        :param opts: plot options
        """
        super().__init__(griddata[:, 0], griddata[:, 1], **opts)

@Plot.register
class StickPlot(Plot):
    """A Plot object that plots sticks"""

    default_plot_style = {'basefmt': " ", 'markerfmt': " "}
    known_styles = {
                       "linefmt", "markerfmt", "basefmt", "bottom", "label", "orientation", "data", 'color',
                       'line_style'
                   } | Plot.known_styles
    method = "stem"
    def plot(self, *params, insert_default_styles=True, **plot_style):
        """
        Plots a set of data | stores the result
        :return: the graphics that matplotlib made
        :rtype:
        """
        if insert_default_styles:
            plot_style = dict(self.plot_style, **plot_style)
        # plot_style = dict(self.plot_style, **plot_style)
        if 'linewidth' in plot_style:
            lw = plot_style['linewidth']
            del plot_style['linewidth']
        else:
            lw = None
        lc = None
        if 'color' in plot_style:
            if 'linefmt' in plot_style:
                raise ValueError("modifying linefmt not currently supported")
            lc = plot_style['color']
            del plot_style['color']
        linefmt = ''
        ls = plot_style.pop('line_style', None)
        if ls is not None:
            if ls == 'dashed':
                if 'linefmt' in plot_style:
                    raise ValueError("modifying passed linefmt not currently supported")
                linefmt+="--"
            elif ls == 'dotted':
                if 'linefmt' in plot_style:
                    raise ValueError("modifying passed linefmt not currently supported")
                linefmt+="-."
            plot_style['linefmt'] = linefmt
        super().plot(*params, insert_default_styles=False, **plot_style)
        if lw is not None:
            self.set_graphics_properties(1, linewidth=lw)
        if lc is not None:
            self.set_graphics_properties(1, color=lc)
        return self.graphics
class ListStickPlot(StickPlot):
    """A Plot object that plots sticks from a list"""
    def __init__(self, griddata, **opts):
        """
        **LLM Docstring**

        Build a stick (stem) plot from an `(n, 2)` array of `(x, y)` points.

        :param griddata: the points
        :type griddata: np.ndarray
        :param opts: plot options
        """
        super().__init__(griddata[:, 0], griddata[:, 1], **opts)

@Plot.register
class DatePlot(Plot):
    method = 'plot_date'
    known_styles = {'fmt', 'tz', 'xdate', 'ydate', 'data'} | Plot.known_styles
@Plot.register
class StepPlot(Plot):
    method = 'step'
    known_styles = {'where', 'data'} | Plot.known_styles
@Plot.register
class LogLogPlot(Plot):
    method = 'loglog'
    # known_styles = {}
@Plot.register
class SemiLogXPlot(Plot):
    method = 'semilogx'
    # known_styles = {}
@Plot.register
class SemilogYPlot(Plot):
    method = 'semilogy'
    # known_styles = {}
@Plot.register
class HorizontalFilledPlot(Plot):
    method = 'fill_betweenx'
    known_styles = {'where', 'step', 'interpolate', 'data'} | Plot.patch_parms
@Plot.register
class BarPlot(Plot):
    method = 'bar'
    known_styles = {'height', 'width', 'bottom', 'align', 'data'} | Plot.patch_parms
@Plot.register
class HorizontalBarPlot(Plot):
    method = 'barh'
    known_styles = {'width', 'height', 'left', 'align'} | Plot.patch_parms
# @Plot.register
# class BarLabelPlot(Plot):
#     method = 'bar_label'
#     known_styles = {'container', 'labels', 'fmt', 'label_type', 'padding'}  | Plot.patch_parms
@Plot.register
class EventPlot(Plot):
    method = 'eventplot'
    known_styles = {'positions', 'orientation', 'lineoffsets', 'linelengths', 'linewidths', 'colors', 'linestyles', 'data'} | Plot.line_params
@Plot.register
class PiePlot(Plot):
    method = 'pie'
    known_styles = {'explode', 'labels', 'colors', 'autopct', 'pctdistance',
                    'shadow', 'labeldistance', 'startangle', 'radius', 'counterclock',
                    'wedgeprops', 'textprops', 'center', 'frame', 'rotatelabels', 'normalize',
                    'data'} | Plot.patch_parms
@Plot.register
class StackPlot(Plot):
    method = 'stackplot'
    known_styles = {'labels', 'colors', 'baseline', 'data'} | Plot.patch_parms
@Plot.register
class BrokenHorizontalBarPlot(Plot):
    method = 'broken_barh'
    known_styles = {'xranges', 'yrange', 'data'} | Plot.patch_parms
@Plot.register
class VerticalLinePlot(Plot):
    """
    Plots a bunch of vertical lines
    """
    known_styles = {'ymin', 'ymax', 'colors', 'linestyles', 'label', 'data'} | Plot.line_params
    method = 'vlines'
    def _get_plot_data(self, x, y=1.0):
        """
        **LLM Docstring**

        Resolve the data for vertical lines at x positions `x` spanning `y` (expanding a
        scalar `y` to `[0, y]`).

        :param x: the x positions
        :param y: the line extent (scalar or `[ymin, ymax]`)
        :return: `(x, y)`
        :rtype: tuple
        """
        if isinstance(y, (int, float)):
            y = [0, y]
        return (x, y)
    def _plot_data(self, *data, **plot_style):
        """
        **LLM Docstring**

        Draw the vertical lines via the backend `vlines` method.

        :param data: the resolved `(x, y)` data
        :param plot_style: the styling options
        :return: the backend graphics object
        """
        x, y = data
        return self._method(x, *y, **plot_style)
@Plot.register
class HorizontalLinePlot(Plot):
    """
    Plots a bunch of vertical lines
    """
    known_styles = {'xmin', 'xmax', 'colors', 'linestyles', 'label', 'data'} | Plot.line_params
    method = 'hlines'
    def _get_plot_data(self, y, x=None):
        """
        **LLM Docstring**

        Resolve the data for horizontal lines at y positions `y` spanning `x` (swapping
        args and expanding a scalar extent to `[0, x]`).

        :param y: the y positions
        :param x: the line extent (scalar or `[xmin, xmax]`)
        :return: `(x, y)`
        :rtype: tuple
        """
        if x is not None:
            x, y = y, x
        else:
            x = 1.0
        if isinstance(x, (int, float)):
            x = [0, x]
        return (x, y)
    def _plot_data(self, *data, **plot_style):
        """
        **LLM Docstring**

        Draw the horizontal lines via the backend `hlines` method.

        :param data: the resolved `(x, y)` data
        :param plot_style: the styling options
        :return: the backend graphics object
        """
        x, y = data
        return self._method(y, *x, **plot_style)
#     known_styles = {'xmin', 'xmax', 'colors', 'linestyles', 'label', 'data'}
@Plot.register
class PolygonPlot(Plot):
    method = 'fill'
    known_styles = {'data'} | Plot.patch_parms

@Plot.register
class AxisHorizontalLinePlot(Plot):
    method = 'axhline'
    known_styles = {'xmin', 'xmax'} | Plot.line_params
@Plot.register
class AxisHorizontalSpanPlot(Plot):
    method = 'axhspan'
    known_styles = {'ymin', 'ymax', 'xmin', 'xmax'} | Plot.patch_parms
@Plot.register
class AxisVerticalLinePlot(Plot):
    method = 'axvline'
    known_styles = {'ymin', 'ymax'} | Plot.line_params
@Plot.register
class AxisVeticalSpanPlot(Plot):
    method = 'axvspan'
    known_styles = {'xmin', 'xmax', 'ymin', 'ymax'} | Plot.patch_parms
@Plot.register
class AxisLinePlot(Plot):
    method = 'axline'
    known_styles = {'xy1', 'xy2', 'slope'} | Plot.line_params

@Plot.register
class StairsPlot(Plot):
    method = 'stairs'
    known_styles = {'values', 'edges', 'orientation', 'baseline', 'fill', 'data'} | Plot.patch_parms

# class ClabelPlot(Plot):
#     method = 'clabel'
#     known_styles = {'CS', 'levels'}


# class AnnotatePlot(Plot):
#     method = 'annotate'
#     known_styles = {'text', 'xy'}
# class TextPlot(Plot):
#     method = 'text'
#     known_styles = {'s', 'fontdict'}
# class TablePlot(Plot):
#     method = 'table'
#     known_styles = {'cellText', 'cellColours', 'cellLoc', 'colWidths', 'rowLabels', 'rowColours', 'rowLoc', 'colLabels', 'colColours', 'colLoc',
#                     'loc', 'bbox', 'edges'}
# class ArrowPlot(Plot):
#     method = 'arrow'
#     known_styles = {'dx', 'dy'}
# class InsetAxesPlot(Plot):
#     method = 'inset_axes'
#     known_styles = {'bounds', 'transform', 'zorder'}
# class IndicateInsetPlot(Plot):
#     method = 'indicate_inset'
#     known_styles = {'bounds', 'inset_ax', 'transform', 'facecolor', 'edgecolor', 'alpha', 'zorder'}
# class IndicateInsetZoomPlot(Plot):
#     method = 'indicate_inset_zoom'
#     known_styles = {'inset_ax'}
# class SecondaryXaxisPlot(Plot):
#     method = 'secondary_xaxis'
#     known_styles = {'location', 'functions'}
# class SecondaryYaxisPlot(Plot):
#     method = 'secondary_yaxis'
#     known_styles = {'location', 'functions'}
# class BarbsPlot(Plot):
#     method = 'barbs'
#     known_styles = {'data'}


######################################################################################################
#
#                                    Pure Data Plots on 2D Axes
#
#
class DataPlot(Plot):
    """
    Makes a 2D plot of arbitrary data using a plot method that handles that data type
    """
    image_params = {'cmap', 'norm', 'aspect', 'interpolation', 'alpha', 'vmin', 'vmax', 'origin',
                    'extent', 'interpolation_stage', 'filternorm', 'filterrad', 'resample', 'url', 'data'}
    def __init__(self,
                 *params,
                 plot_style=None, method=None,
                 figure=None, axes=None, subplot_kw=None,
                 colorbar=None,
                 **opts
                 ):
        """
        :param params: _empty_ or _data_
        :type params:
        :param plot_style: the plot styling options to be fed into the plot method
        :type plot_style: dict | None
        :param method: the method name as a string
        :type method: str
        :param figure: the Graphics object on which to plot (None means make a new one)
        :type figure: Graphics | None
        :param axes: the axes on which to plot (used in constructing a Graphics, None means make a new one)
        :type axes: None
        :param subplot_kw: the keywords to pass on when initializing the plot
        :type subplot_kw: dict | None
        :param colorbar: whether to use a colorbar or what options to pass to the colorbar
        :type colorbar: None | bool | dict
        :param opts: options to be fed in when initializing the Graphics
        :type opts:
        """
        super().__init__(*params,
                         plot_style=plot_style, method=method,
                         colorbar=colorbar, figure=figure,
                         axes=axes, subplot_kw=subplot_kw,
                         **opts
                         )
    def _get_plot_data(self, data):
        """
        **LLM Docstring**

        Pass the data array straight through to the plot method.

        :param data: the data to plot
        :return: the data as a one-tuple
        :rtype: tuple
        """
        return data,

@Plot.register
class HistogramPlot(DataPlot):
    """
    Makes a Histogram of data
    """
    method = 'hist'
    known_styles = {'bins', 'range', 'density', 'weights', 'cumulative',
                    'bottom', 'histtype', 'align', 'orientation', 'rwidth', 'log', 'color',
                    'label', 'stacked', 'data'}

@Plot.register
class HistogramPlot2D(DataPlot):
    """
    Makes a 2D histogram of data
    """
    method = 'hist2d'
    known_styles = {'bins', 'range', 'density', 'weights', 'cmin', 'cmax', 'data'}

@Plot.register
class SpectrogramPlot(DataPlot):
    method = 'specgram'
    known_styles = {'NFFT', 'Fs', 'Fc', 'detrend', 'window', 'noverlap',
                    'cmap', 'xextent', 'pad_to', 'sides', 'scale_by_freq', 'mode', 'scale', 'vmin',
                    'vmax', 'data'} | DataPlot.image_params
@Plot.register
class AutocorrelationPlot(DataPlot):
    method = 'acorr'
    known_styles = {'detrend', 'normed', 'usevlines', 'maxlags', 'linestyle', 'marker', 'data'} | Plot.known_styles
@Plot.register
class AngleSpectrumPlot(DataPlot):
    method = 'angle_spectrum'
    known_styles = {'Fs', 'Fc', 'window', 'pad_to', 'sides', 'data'}  | Plot.patch_parms
@Plot.register
class CoherencePlot(DataPlot):
    method = 'cohere'
    known_styles = {'NFFT', 'Fs', 'Fc', 'noverlap', 'pad_to', 'sides', 'scale_by_freq', 'data'} | Plot.known_styles
@Plot.register
class CrossSpectralDensityPlot(DataPlot):
    method = 'csd'
    known_styles = {'NFFT', 'Fs', 'Fc', 'detrend', 'window', 'noverlap', 'pad_to', 'sides', 'scale_by_freq', 'return_line', 'data'}  | Plot.known_styles
@Plot.register
class MagnitudeSpectrumPlot(DataPlot):
    method = 'magnitude_spectrum'
    known_styles = {'Fs', 'Fc', 'window', 'pad_to', 'sides', 'scale', 'data'} | Plot.known_styles
@Plot.register
class PhaseSpectrumPlot(DataPlot):
    method = 'phase_spectrum'
    known_styles = {'Fs', 'Fc', 'window', 'pad_to', 'sides', 'data'} | Plot.known_styles
@Plot.register
class PowerSpectralDensityPlot(DataPlot):
    method = 'psd'
    known_styles = {'NFFT', 'Fs', 'Fc', 'detrend', 'window', 'noverlap', 'pad_to', 'sides', 'scale_by_freq', 'return_line', 'data'} | Plot.known_styles
@Plot.register
class CrossCorrelationPlot(DataPlot):
    method = 'xcorr'
    known_styles = {'normed', 'usevlines', 'maxlags', 'data', 'linestyle', 'marker'} | Plot.known_styles
@Plot.register
class BoxPlot(DataPlot):
    method = 'boxplot'
    known_styles = {'notch', 'sym', 'vert', 'whis', 'positions', 'widths',
                    'patch_artist', 'bootstrap', 'usermedians', 'conf_intervals', 'meanline',
                    'showmeans', 'showcaps', 'showbox', 'showfliers', 'boxprops', 'labels',
                    'flierprops', 'medianprops', 'meanprops', 'capprops', 'whiskerprops',
                    'manage_ticks', 'autorange', 'zorder', 'data'}
@Plot.register
class ViolinPlot(DataPlot):
    method = 'violinplot'
    known_styles = {'dataset', 'positions', 'vert', 'widths', 'showmeans',
                    'showextrema', 'showmedians', 'quantiles', 'points', 'bw_method', 'data'}
# class ViolinPlot(Plot):
#     method = 'violin'
#     known_styles = {'vpstats', 'positions', 'vert', 'widths', 'showmeans',
#                     'showextrema', 'showmedians'}
@Plot.register
class BoxAndWhiskerPlot(DataPlot):
    method = 'bxp'
    known_styles = {'bxpstats', 'positions', 'widths', 'vert', 'patch_artist',
                    'shownotches', 'showmeans', 'showcaps', 'showbox', 'showfliers', 'boxprops',
                    'whiskerprops', 'flierprops', 'medianprops', 'capprops', 'meanprops',
                    'meanline', 'manage_ticks', 'zorder'}
@Plot.register
class HexagonalHistogramPlot(DataPlot):
    method = 'hexbin'
    known_styles = {'C', 'gridsize', 'bins', 'xscale', 'yscale', 'extent', 'cmap', 'norm', 'vmin',
                    'vmax', 'alpha', 'linewidths', 'edgecolors', 'mincnt', 'marginals', 'data', 'reduce_C_function'} | Plot.patch_parms

class VectorFieldPlot(Plot):
    """
    Makes a plot of some 2D vector field with center points and arrows
    """
    def _get_plot_data(self, x, y, u, v):
        """
        **LLM Docstring**

        Pass the `(x, y, u, v)` vector-field data through to the plot method.

        :param x: the x positions
        :param y: the y positions
        :param u: the x components
        :param v: the y components
        :return: `(x, y, u, v)`
        :rtype: tuple
        """
        return (x, y, u, v)

@Plot.register
class QuiverPlot(VectorFieldPlot):
    method = 'quiver'
    known_styles = {"units", "angles", "scale", "scale_units", "width", "headwidth", "headlength",
                    "headaxislength", "minshaft", "minlength", "pivot", "color", "data"} | Plot.patch_parms
@Plot.register
class StreamPlot(VectorFieldPlot):
    method = 'streamplot'
    known_styles = {'density', 'linewidth', 'color', 'cmap', 'norm',
                    'arrowsize', 'arrowstyle', 'minlength', 'transform', 'zorder', 'start_points',
                    'maxlength', 'integration_direction', 'data'}

@Plot.register
class ArrayPlot(DataPlot):
    """
    Plots an array as an image
    """

    method = 'imshow'
    known_styles = DataPlot.image_params
    def __init__(self, *params,
                 plot_style=None, colorbar=None,
                 figure=None, axes=None, subplot_kw=None,
                 **opts
                 ):
        """
        **LLM Docstring**

        Build an image plot of a 2-D array (via `imshow`).

        :param params: empty, or the array to plot
        :param plot_style: styling options
        :type plot_style: dict | None
        :param colorbar: whether/how to add a colorbar
        :param figure: an existing figure to draw into
        :param axes: existing axes to draw into
        :param subplot_kw: subplot construction options
        :type subplot_kw: dict | None
        :param opts: options forwarded to `Graphics`
        """
        super().__init__(*params,
                         plot_style=plot_style,
                         colorbar=colorbar, figure=figure,
                         axes=axes, subplot_kw=subplot_kw,
                         **opts
                         )
    def _get_plot_data(self, data):
        """
        **LLM Docstring**

        Pass the array through to the plot method, densifying a sparse array first.

        :param data: the array (or sparse array)
        :return: the array as a one-tuple
        :rtype: tuple
        """
        if hasattr(data, 'toarray'):
            data = data.toarray()
        return data,
@Plot.register
class MatrixPlot(ArrayPlot):
    method = 'matshow'
@Plot.register
class SparsityPlot(ArrayPlot):
    method = 'spy'
    known_styles = {'precision', 'marker', 'markersize', 'aspect', 'origin'} | ArrayPlot.known_styles

class TensorPlot(GraphicsGrid):
    """
    Plots slices of a tensor as a grid
    """
    def __init__(self, tensor,
                 nrows=None, ncols=None,
                 plot_style=None, colorbar=None,
                 figure=None, axes=None, subplot_kw=None,
                 method='imshow', plot_class=None,
                 **opts
                 ):
        """
        **LLM Docstring**

        Plot the 2-D slices of a higher-rank tensor as a grid of array plots, inferring
        the grid shape from the tensor's leading dimensions.

        :param tensor: the tensor to plot
        :type tensor: np.ndarray
        :param nrows: the number of rows (inferred if omitted)
        :type nrows: int | None
        :param ncols: the number of columns (inferred if omitted)
        :type ncols: int | None
        :param plot_style: styling options for each slice
        :type plot_style: dict | None
        :param colorbar: whether/how to add colorbars
        :param figure: an existing figure to draw into
        :param axes: existing axes to draw into
        :param subplot_kw: subplot construction options
        :type subplot_kw: dict | None
        :param method: the backend method for each slice
        :type method: str
        :param plot_class: a custom per-slice plot class/factory
        :param opts: options forwarded to each slice plot
        """
        from operator import mul
        from functools import reduce
        tensor_shape = tensor.shape
        total_dim = reduce(mul, tensor_shape[:-2], 1)
        if nrows is None or ncols is None:
            if len(tensor_shape) == 3:
                nrows = 1
                ncols = tensor_shape[0]
            elif len(tensor_shape) == 4:  # best case
                nrows, ncols = tensor_shape[:2]
            else:
                if nrows is not None:
                    ncols = total_dim // nrows
                elif ncols is not None:
                    nrows = total_dim // ncols
                else:
                    ncols = 5
                    nrows = total_dim // ncols
        super().__init__(nrows=nrows, ncols=ncols,
                         figure=figure,
                         axes=axes,
                         subplot_kw=subplot_kw
                         )

        tensor = tensor.reshape((total_dim,) + tensor_shape[-2:])
        if plot_class is None:
            plot_class = lambda data,colorbar=colorbar,**opts:ArrayPlot(data, colorbar=colorbar,**opts)
        for i in range(nrows):
            for j in range(ncols):
                graphics = self.axes[i][j]
                self.axes[i][j] = plot_class(
                    tensor[nrows * i + j],
                    figure=graphics,
                    plot_style=plot_style,
                    method=method,
                    **opts
                )

######################################################################################################
#
#                                    3D Plots on 2D Axes
#
#

class Plot2D(Plot):
    """
    A base class for plots of 3D data but plotted on 2D axes
    """
    known_styles = {"corner_mask", "colors", "alpha", "cmap", "norm", "vmin", "vmax", "origin",
                    "extent", "locator", "extend", "xunits, yunits", "antialiased", "nchunk",
                    "linewidths", "linestyles", "hatches", "data"}
    method='contour'
    def __init__(self, *params,
                 plot_style=None,
                 colorbar=None,
                 figure=None,
                 axes=None,
                 subplot_kw=None,
                 **opts
                 ):
        """
        :param params: either _empty_ or _x_, _y_, _z_ arrays or _function_, _xrange_, _yrange_
        :type params:
        :param plot_style: the plot styling options to be fed into the plot method
        :type plot_style: dict | None
        :param method: the method name as a string
        :type method: str
        :param figure: the Graphics object on which to plot (None means make a new one)
        :type figure: Graphics | None
        :param axes: the axes on which to plot (used in constructing a Graphics, None means make a new one)
        :type axes: None
        :param subplot_kw: the keywords to pass on when initializing the plot
        :type subplot_kw: dict | None
        :param colorbar: whether to use a colorbar or what options to pass to the colorbar
        :type colorbar: None | bool | dict
        :param opts: options to be fed in when initializing the Graphics
        :type opts:
        """
        super().__init__(*params,
                         plot_style=plot_style,
                         colorbar=colorbar, figure=figure,
                         axes=axes, subplot_kw=subplot_kw,
                         **opts
                         )
    def _get_plot_data(self, func, xrange, yrange):
        """
        **LLM Docstring**

        Resolve the `(func, xrange, yrange)` inputs into gridded `(x, y, z)` data for a
        2-D-axes plot of 3-D data.

        :param func: a callable or the x data
        :param xrange: the x range/values
        :param yrange: the y range/values
        :return: `(x, y, z)`
        :rtype: tuple
        """
        return _get_3D_plotdata(func, xrange, yrange)
@Plot.register
class ContourPlot(Plot2D):
    method = 'contourf'
    known_styles = {"triangles", "mask", "levels", "colors",
                    "alpha", "cmap", "norm", "vmin", "vmax", "origin", "extent", "locator", "extend",
                    "xunits, yunits", "antialiased"}
@Plot.register
class ContourLinePlot(ContourPlot):
    method = 'contour'
    known_styles = ContourPlot.known_styles | {"linewidths", "linestyles", "negative_linestyles"}
@Plot.register
class DensityPlot(Plot2D):
    method = 'pcolormesh'
    known_styles = {'alpha', 'norm', 'cmap', 'vmin', 'vmax', 'shading', 'antialiased', 'data'} | Plot.patch_parms
@Plot.register
class HeatmapPlot(Plot2D):
    method = 'pcolor'
    known_styles = {'shading', 'alpha', 'norm', 'cmap', 'vmin', 'vmax', 'data'} | ArrayPlot.known_styles
@Plot.register
class TriPlot(Plot2D):
    """A Plot object that plots a triangulation bars"""
    method = 'triplot'
    known_styles = {"triangles", "mask"} | Plot.known_styles
class ListTriPlot(Plot2D):
    """A Plot that pulls the triangulation data from a list"""
    def __init__(self, griddata, **opts):
        """
        **LLM Docstring**

        Build a triangulation plot from an `(n, 2)` array of points.

        :param griddata: the points
        :type griddata: np.ndarray
        :param opts: plot options
        """
        super().__init__(griddata[:, 0], griddata[:, 1], **opts)
@Plot.register
class TriDensityPlot(Plot2D):
    method = 'tripcolor'
    known_styles = {'alpha', 'norm', 'cmap', 'vmin', 'vmax', 'shading', 'facecolors'}
@Plot.register
class TriContourLinesPlot(Plot2D):
    method = 'tricontour'
    known_styles = {"triangles", "mask", "levels", "colors",
                    "alpha", "cmap", "norm", "vmin", "vmax", "origin", "extent", "locator", "extend",
                    "xunits, yunits", "antialiased", "linewidths", "linestyles"}
@Plot.register
class TriContourPlot(Plot2D):
    method = 'tricontourf'
    known_styles = {"triangles", "mask", "levels", "colors",
                    "alpha", "cmap", "norm", "vmin", "vmax", "origin", "extent", "locator", "extend",
                    "xunits, yunits", "antialiased", "hatches"}

class ListPlot2D(Plot2D):
    """
    Convenience class that handles the interpolation first
    """
    def __init__(self,
                 *params,
                 plot_style=None,
                 method='contour',
                 colorbar=None,
                 figure=None,
                 axes=None,
                 subplot_kw=None,
                 interpolate=True,
                 **opts
                 ):
        """
        :param params: either _empty_ or and array of (_x_, _y_, _z_) points
        :type params:
        :param plot_style: the plot styling options to be fed into the plot method
        :type plot_style: dict | None
        :param method: the method name as a string
        :type method: str
        :param figure: the Graphics object on which to plot (None means make a new one)
        :type figure: Graphics | None
        :param axes: the axes on which to plot (used in constructing a Graphics, None means make a new one)
        :type axes: None
        :param subplot_kw: the keywords to pass on when initializing the plot
        :type subplot_kw: dict | None
        :param colorbar: whether to use a colorbar or what options to pass to the colorbar
        :type colorbar: None | bool | dict
        :param interpolate: whether to interpolate the data or not
        :type interpolate: bool
        :param opts: options to be fed in when initializing the Graphics
        :type opts:
        """
        self.interpolate = interpolate
        super().__init__(*params,
                         plot_style=plot_style, method=method,
                         colorbar=colorbar, figure=figure,
                         axes=axes, subplot_kw=subplot_kw,
                         **opts
                         )

    def _get_plot_data(self, *griddata, interpolate=None):
        """
        **LLM Docstring**

        Resolve scattered `(x, y, z)` points into gridded data, interpolating onto a mesh
        when the data is given as a single point array.

        :param griddata: the `(x, y, z)` arrays or a single point array
        :param interpolate: interpolate a point array onto a mesh (defaults to the instance setting)
        :type interpolate: bool | None
        :return: `(x, y, z)`
        :rtype: tuple
        """
        if interpolate is None:
            interpolate = self.interpolate
        if len(griddata) == 3:
            x, y, z = griddata
        elif interpolate:
            x, y, z = _interp2DData(griddata[0])
        else:
            x = griddata[0][:, 0]
            y = griddata[0][:, 1]
            z = griddata[0][:, 2]

        return (x, y, z)

@Plot.register
class ListContourPlot(ContourPlot):
    _get_plot_data = ListPlot2D._get_plot_data
    def __init__(self,*params, interpolate=True, **opts):
        """
        **LLM Docstring**

        Build a contour plot from scattered points, interpolating them onto a mesh.

        :param params: the scattered point data
        :param interpolate: interpolate onto a mesh
        :type interpolate: bool
        :param opts: plot options
        """
        self.interpolate = interpolate
        super().__init__(*params, **opts)
@Plot.register
class ListDensityPlot(DensityPlot):
    _get_plot_data = ListPlot2D._get_plot_data
    def __init__(self,*params, interpolate=True, **opts):
        """
        **LLM Docstring**

        Build a density plot from scattered points, interpolating them onto a mesh.

        :param params: the scattered point data
        :param interpolate: interpolate onto a mesh
        :type interpolate: bool
        :param opts: plot options
        """
        self.interpolate = interpolate
        super().__init__(*params, **opts)
@Plot.register
class ListTriContourPlot(TriContourPlot):
    _get_plot_data = ListPlot2D._get_plot_data
    def __init__(self,*params, interpolate=True, **opts):
        """
        **LLM Docstring**

        Build a triangulated contour plot from scattered points.

        :param params: the scattered point data
        :param interpolate: interpolate onto a mesh
        :type interpolate: bool
        :param opts: plot options
        """
        self.interpolate = interpolate
        super().__init__(*params, **opts)
@Plot.register
class ListTriDensityPlot(TriDensityPlot):
    _get_plot_data = ListPlot2D._get_plot_data
    def __init__(self,*params, interpolate=True, **opts):
        """
        **LLM Docstring**

        Build a triangulated density plot from scattered points.

        :param params: the scattered point data
        :param interpolate: interpolate onto a mesh
        :type interpolate: bool
        :param opts: plot options
        """
        self.interpolate = interpolate
        super().__init__(*params, **opts)


######################################################################################################
#
#                                    3D Plots on 3D Axes
#
#
class Plot3D(Graphics3D):  # basically a mimic of the Plot class but inheriting from Graphics3D
    """A base class for 3D plots"""

    default_plot_style = {}
    style_mapping = {"format": "fmt"}
    known_styles = {"fmt"} | Plot.line_params
    method = 'plot_surface'
    def __init__(self, *params,
                 plot_style=None,
                 method=None, colorbar=None,
                 figure=None, axes=None, subplot_kw=None,
                 **opts
                 ):
        """
        :param params: either _empty_ or _x_, _y_, _z_ arrays or _function_, _xrange_, _yrange_
        :type params:
        :param plot_style: the plot styling options to be fed into the plot method
        :type plot_style: dict | None
        :param method: the method name as a string
        :type method: str
        :param figure: the Graphics object on which to plot (None means make a new one)
        :type figure: Graphics | None
        :param axes: the axes on which to plot (used in constructing a Graphics, None means make a new one)
        :type axes: None
        :param subplot_kw: the keywords to pass on when initializing the plot
        :type subplot_kw: dict | None
        :param colorbar: whether to use a colorbar or what options to pass to the colorbar
        :type colorbar: None | bool | dict
        :param opts: options to be fed in when initializing the Graphics
        :type opts:
        """

        super().__init__(figure=figure, axes=axes, subplot_kw=subplot_kw)
        if method is None:
           method = self.method
        if isinstance(method, str):
            method = getattr(self.axes, method)
        self._method = method

        # we're gonna set things up so that we can have delayed evaluation of the plotting.
        # i.e. a Plot3D can be initialized but then do all its plotting later
        if plot_style is None:
            plot_style = {}
        for k,v in self.style_mapping.items():
            if k in opts:
                opts[v] = opts[k]
                del opts[k]
        for k in self.known_styles:
            if k in opts:
                plot_style[k] = opts[k]
        for k in self.default_plot_style:
            if k not in plot_style:
                plot_style[k] = self.default_plot_style[k]
        self._plot_style = plot_style
        self.plot_style = plot_style
        self.plot_opts = opts
        self._colorbar = colorbar
        self._initialized = False

        if len(params) > 0:
            self.plot(*params)

    def _initialize(self):
        """
        **LLM Docstring**

        Mark the 3-D plot initialized, apply its figure options, and add a colorbar if
        one was requested.
        """
        self._initialized = True
        self.set_options(**self.plot_opts)
        if self.colorbar:
            self.add_colorbar()
        elif isinstance(self.colorbar, dict):
            self.add_colorbar(**self.colorbar)

    def _get_plot_data(self, func, xrange, yrange):
        """
        **LLM Docstring**

        Resolve the `(func, xrange, yrange)` inputs into gridded `(x, y, z)` data for a
        3-D-axes plot.

        :param func: a callable or the x data
        :param xrange: the x range/values
        :param yrange: the y range/values
        :return: `(x, y, z)`
        :rtype: tuple
        """
        return _get_3D_plotdata(func, xrange, yrange)

    def _plot_data(self, *data, **plot_style):
        """
        **LLM Docstring**

        Call the backend 3-D plot method on the resolved plot data.

        :param data: the positional plot arguments
        :param plot_style: the styling options
        :return: the backend graphics object
        """
        return self._method(*self._get_plot_data(*data), **plot_style)

    def plot(self, *params, **plot_style):
        """
        **LLM Docstring**

        Plot the data on the 3-D axes and store the result, initializing the figure on
        the first call.

        :param params: the plot arguments
        :param plot_style: the styling options (merged with the defaults)
        :return: the backend graphics object
        """
        plot_style = dict(self.plot_style, **plot_style)
        self.graphics = self._plot_data(*params, **plot_style)
        if not self._initialized:
            self._initialize()
        return self.graphics
    def add_colorbar(self, **kw):
        """
        **LLM Docstring**

        Add a colorbar to the 3-D plot (deferring until the figure is initialized).

        :param kw: options for the colorbar
        :return: the colorbar (once initialized)
        """
        if self._initialized:
            fig:GraphicsFigure = self.figure
            ax:GraphicsAxes = self.axes
            return fig.create_colorbar(self.graphics, **kw)
        else:
            self._colorbar = kw
    plot_classes = {}
    @classmethod
    def resolve_method(cls, mpl_name):
        """
        **LLM Docstring**

        Look up the registered 3-D plot class for a backend method name.

        :param mpl_name: the method/class name
        :type mpl_name: str
        :return: the plot class
        :rtype: type
        """
        return cls.plot_classes[mpl_name]
    # @classmethod
    # def merge_plots(cls, *plots, **styles):
    #     ...
    @classmethod
    def register(cls, plot_class):
        """
        **LLM Docstring**

        Register a 3-D plot class in the registry, keyed by its backend method name (or
        class name if already registered). Usable as a decorator.

        :param plot_class: the plot class to register
        :type plot_class: type
        :return: the registered class
        :rtype: type
        """
        if plot_class.method in cls.plot_classes:
            cls.plot_classes[plot_class.__name__] = plot_class
        else:
            cls.plot_classes[plot_class.method] = plot_class
        return plot_class

@Plot3D.register
class ScatterPlot3D(Plot3D):
    """
    Creates a ScatterPlot of 3D data
    """
    method = 'scatter'

@Plot3D.register
class WireframePlot3D(Plot3D):
    """
    Creates a Wireframe mesh plot of 3D data
    """
    method = 'plot_wireframe'

@Plot3D.register
class ContourPlot3D(Plot3D):
    """
    Creates a 3D ContourPlot of 3D data
    """
    method = 'contourf'

class ListPlot3D(Plot3D):
    """
    Convenience 3D plotting class that handles the interpolation first
    """
    method = 'contour'
    def __init__(self,
                 *params,
                 plot_style=None,
                 method=None,
                 colorbar=None,
                 figure=None,
                 axes=None,
                 subplot_kw=None,
                 interpolate=True,
                 **opts
                 ):
        """
        :param params: either _empty_ or and array of (_x_, _y_, _z_) points
        :type params:
        :param plot_style: the plot styling options to be fed into the plot method
        :type plot_style: dict | None
        :param method: the method name as a string
        :type method: str
        :param figure: the Graphics object on which to plot (None means make a new one)
        :type figure: Graphics | None
        :param axes: the axes on which to plot (used in constructing a Graphics, None means make a new one)
        :type axes: None
        :param subplot_kw: the keywords to pass on when initializing the plot
        :type subplot_kw: dict | None
        :param colorbar: whether to use a colorbar or what options to pass to the colorbar
        :type colorbar: None | bool | dict
        :param interpolate: whether to interpolate the data or not
        :type interpolate: bool
        :param opts: options to be fed in when initializing the Graphics
        :type opts:
        """
        self.interpolate = interpolate
        super().__init__(*params,
                         plot_style=plot_style, method=method,
                         colorbar=colorbar, figure=figure,
                         axes=axes, subplot_kw=subplot_kw,
                         **opts
                         )

    def _get_plot_data(self, *griddata, interpolate=None):
        """
        **LLM Docstring**

        Resolve scattered `(x, y, z)` points into 3-D plot data, interpolating onto a
        mesh when the data is a single point array.

        :param griddata: the `(x, y, z)` arrays or a single point array
        :param interpolate: interpolate a point array onto a mesh (defaults to the instance setting)
        :type interpolate: bool | None
        :return: `(x, y, z)`
        :rtype: tuple
        """
        if interpolate is None:
            interpolate = self.interpolate
        if len(griddata) == 3:
            x, y, z = griddata
        elif interpolate:
            x, y, z = _interp2DData(griddata[0])
        else:
            x = griddata[0][:, 0]
            y = griddata[0][:, 1]
            z = griddata[0][:, 2]

        return (x, y, z)

@Plot3D.register
class ListTriPlot3D(ListPlot3D):
    """
    Creates a triangulated surface plot in 3D
    """
    method = 'plot_trisurf'
    default_plot_style = {}

def resolve_plotter(tag):
    """
    **LLM Docstring**

    Resolve a plot-type tag to its plot class, searching the 2-D and 3-D registries
    by key (case-insensitively) and then by backend method name.

    :param tag: the plot-type name (or an already-resolved class)
    :type tag: str | type
    :return: the plot class (or `None`)
    :rtype: type | None
    """
    if isinstance(tag, str):
        plotter = Plot.plot_classes.get(tag,Plot3D.plot_classes.get(tag))
        if plotter is None:
            plotter = Plot.plot_classes.get(tag.lower(), Plot3D.plot_classes.get(tag.lower()))
        if plotter is None:
            for v in itertools.chain(Plot.plot_classes.values(), Plot3D.plot_classes.values()):
                if v.method == tag:
                    plotter = v
                    break
        return plotter
    else:
        return tag
def plot_generic(*, x, type='plot', y=None, z=None, func=None, **kwargs):
    """
    **LLM Docstring**

    Build a plot of the resolved type from `x`/`y`/`z`/`func` inputs, assembling the
    positional arguments appropriately for function plots, `(x, y)` data, and
    `(x, y, z)` data.

    :param x: the x data
    :param type: the plot-type tag
    :type type: str
    :param y: the y data
    :param z: the z data
    :param func: a function to plot
    :type func: Callable | None
    :param kwargs: options forwarded to the plot class
    :return: the plot
    :raises ValueError: for an unknown type or missing required inputs
    """
    plotter = resolve_plotter(type)
    if plotter is None:
        raise ValueError(f"unknown plot type {plotter}")
    if func is not None:
        if y is not None:
            args = [func, x, y]
        else:
            args = [func, x]
    elif z is not None:
        if y is None:
            raise ValueError("need `x` and `y` values when supplied `z`")
        args = [x, y, z]
    else:
        if y is None:
            raise ValueError("need `x` and `y` values when no `func` supplied")
        args = [x, y]
    return plotter(*args, **kwargs)
plot_spec_schema = {'type':str, 'args':list, 'opts':dict}
def plot_multi(
        *plot_specs: dict,
        figure=None,
        plot_type_styles=None,
        default_type='plot',
        x=None,
        y=None,
        z=None,
        func=None,
        common_settings=None,
        **global_settings
):
    """
    **LLM Docstring**

    Build several plots onto a shared figure from a sequence of plot specs, layering
    common settings, per-type styles, and global settings, and expanding any
    list-valued `func` into multiple curves.

    :param plot_specs: the per-plot specification dicts
    :param figure: an existing figure to draw onto
    :param plot_type_styles: per-plot-type default styles
    :type plot_type_styles: dict | None
    :param default_type: the default plot type
    :type default_type: str
    :param x: shared x data
    :param y: shared y data
    :param z: shared z data
    :param func: shared function(s) to plot
    :param common_settings: settings shared across all plots
    :type common_settings: dict | None
    :param global_settings: settings applied only to the first (figure-creating) plot
    :return: the shared figure
    :rtype: Graphics
    """
    if plot_type_styles is None:
        plot_type_styles = {}
    if common_settings is None:
        common_settings = {}
    for key, val in [
        ['x', x],
        ['y', y],
        ['z', z],
        ['func', func]
    ]:
        if not dev.is_default(val):
            common_settings[key] = val
    for i,f in enumerate(plot_specs):
        f = collections.ChainMap(
            f,
            plot_type_styles.get(f.get('type', default_type), {}),
            common_settings
        )
        f['type'] = f.get('type', default_type)
        f['figure'] = f.get('figure', figure)
        func = f.get('func')
        if not dev.is_list_like(func):
            if i == 0:
                figure = plot_generic(**collections.ChainMap(f, global_settings))
            else:
                _ = plot_generic(**f)  # TDB if I prefer to update the object each iteration or not
        else:
            for j, c in enumerate(func):
                if i == 0 and j == 0:
                    figure = plot_generic(**collections.ChainMap(dict(func=c), f, global_settings))
                    if f['figure'] is None:
                        f['figure'] = figure
                else:
                    _ = plot_generic(**collections.ChainMap(dict(func=c), f))
    return figure

# add classes to __all__
for c in Plot.plot_classes.values():
    if c.__name__ not in __all__:
        __all__.append(c.__name__)
for c in Plot3D.plot_classes.values():
    if c.__name__ not in __all__:
        __all__.append(c.__name__)
del c
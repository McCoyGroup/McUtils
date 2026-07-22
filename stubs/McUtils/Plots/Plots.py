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
__all__ = ['Plot', 'DataPlot', 'ArrayPlot', 'TensorPlot', 'Plot2D', 'ListPlot2D', 'Plot3D', 'ListPlot3D', 'CompositePlot', 'resolve_plotter', 'plot_generic', 'plot_multi', 'FilledPlot', 'ScatterPlot', 'ListScatterPlot', 'ErrorBarPlot', 'ListErrorBarPlot', 'StickPlot', 'DatePlot', 'StepPlot', 'LogLogPlot', 'SemiLogXPlot', 'SemilogYPlot', 'HorizontalFilledPlot', 'BarPlot', 'HorizontalBarPlot', 'EventPlot', 'PiePlot', 'StackPlot', 'BrokenHorizontalBarPlot', 'VerticalLinePlot', 'HorizontalLinePlot', 'PolygonPlot', 'AxisHorizontalLinePlot', 'AxisHorizontalSpanPlot', 'AxisVerticalLinePlot', 'AxisVeticalSpanPlot', 'AxisLinePlot', 'StairsPlot', 'HistogramPlot', 'HistogramPlot2D', 'SpectrogramPlot', 'AutocorrelationPlot', 'AngleSpectrumPlot', 'CoherencePlot', 'CrossSpectralDensityPlot', 'MagnitudeSpectrumPlot', 'PhaseSpectrumPlot', 'PowerSpectralDensityPlot', 'CrossCorrelationPlot', 'BoxPlot', 'ViolinPlot', 'BoxAndWhiskerPlot', 'HexagonalHistogramPlot', 'QuiverPlot', 'StreamPlot', 'MatrixPlot', 'SparsityPlot', 'ContourPlot', 'ContourLinePlot', 'DensityPlot', 'HeatmapPlot', 'TriPlot', 'TriDensityPlot', 'TriContourLinesPlot', 'TriContourPlot', 'ListContourPlot', 'ListDensityPlot', 'ListTriContourPlot', 'ListTriDensityPlot', 'ScatterPlot3D', 'WireframePlot3D', 'ContourPlot3D', 'ListTriPlot3D']

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
    ...

def _semi_adaptive_sample_func(f, xmin, xmax, npts=150, max_refines=10, der_cut=10 ** 5):
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
    ...

def _semi_adaptive_sample_func2(f, xmin, xmax, ymin, ymax, npts=15, max_refines=10, der_cut=10 ** 5):
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
    ...

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
    ...

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
    ...

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
    ...

class Plot(Graphics):
    """
    The base plotting class to interface into matplotlib or (someday 3D) VTK.
    In the future hopefully we'll be able to make a general-purpose `PlottingBackend` class that doesn't need to be `matplotlib` .
    Builds off of the `Graphics` class to make a unified and convenient interface to generating plots.
    Some sophisticated legwork unfortunately has to be done vis-a-vis tracking constructed lines and other plotting artefacts,
    since `matplotlib` is designed to infuriate.
    """
    opt_keys = Graphics.opt_keys | {'plot_style', 'display_format', 'prep_colors', 'color_value_scaling'}
    default_plot_style = {}
    default_colormap = 'viridis'
    style_mapping = {'format': 'fmt'}
    known_styles = {'fmt'} | line_params
    method = 'plot'

    def __init__(self, *params, method=None, figure=None, axes=None, subplot_kw=None, plot_style=None, theme=None, display_format=None, **opts):
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
        ...
    known_keys = Graphics.known_keys | {'method', 'plot_style', 'display_format', 'insert_default_styles'}

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
        ...

    def _check_opts(self, opts):
        """
        **LLM Docstring**

        Raise if any option keys aren't among this plot's known styles or keys.

        :param opts: the options to check
        :type opts: dict
        :raises ValueError: for unknown option keys
        """
        ...

    def _initialize(self):
        """
        **LLM Docstring**

        Mark the plot initialized and apply its (non-style) figure options.
        """
        ...

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
        ...

    def _plot_data(self, *data, **plot_style):
        """
        **LLM Docstring**

        Call the backend plot method on the resolved plot data.

        :param data: the positional plot arguments
        :param plot_style: the styling options
        :return: the backend graphics object
        """
        ...

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
        ...

    def plot(self, *params, insert_default_styles=True, **plot_style):
        """
        Plots a set of data & stores the result
        :return: the graphics that matplotlib made
        :rtype:
        """
        ...

    @property
    def artists(self):
        """
        **LLM Docstring**

        The backend artist objects produced by the plot (as a list).

        :return: the artists
        :rtype: list | None
        """
        ...

    def _change_figure(self, new, *init_args, **init_kwargs):
        """Creates a copy of the object with new axes and a new figure

        :return:
        :rtype:
        """
        ...

    def clear(self):
        """
        Removes the plotted data
        """
        ...

    def restyle(self, **plot_style):
        """
        Replots the data with updated plot styling
        :param plot_style:
        :type plot_style:
        """
        ...

    @property
    def data(self):
        """
        The data that we plotted
        """
        ...

    @property
    def plot_style(self):
        """
        The styling options applied to the plot
        """
        ...

    def add_colorbar(self, graphics=None, norm=None, **kw):
        """
        Adds a colorbar to the plot
        """
        ...

    def set_graphics_properties(self, *which, **kw):
        """
        **LLM Docstring**

        Set backend properties on the plot's artists (all of them, or the selected
        indices).

        :param which: the artist indices to modify (all if empty)
        :param kw: the properties to set
        """
        ...

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
        ...
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
        ...

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
        ...

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
        ...

    def merge(self, **kwargs):
        """
        **LLM Docstring**

        Merge the held plots onto a shared new figure (re-hosting each onto the first's
        figure).

        :param kwargs: options for the shared figure
        :return: the merged base plot
        :rtype: Graphics
        """
        ...

    def show(self, interactive=True):
        """
        **LLM Docstring**

        Merge the plots and display the result.

        :param interactive: show interactively
        :type interactive: bool
        """
        ...

    def _ipython_display_(self):
        """
        **LLM Docstring**

        Display the composite plot in IPython.
        """
        ...

@Plot.register
class FilledPlot(Plot):
    """
    Inherits from `Plot`.
    Plots a bunch of x values against a bunch of y values using the `scatter` method.
    """
    known_styles = {'where', 'interpolate', 'step', 'data'} | Plot.patch_parms
    method = 'fill_between'

@Plot.register
class ScatterPlot(Plot):
    """
    Inherits from `Plot`.
    Plots a bunch of x values against a bunch of y values using the `scatter` method.
    """
    style_mapping = {'color': 'c', 'marker_size': 's'}
    method = 'scatter'

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
        ...

@Plot.register
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
        ...

@Plot.register
class ErrorBarPlot(Plot):
    """
    Inherits from `Plot`.
    Plots error bars using the `errorbar` method.
    """
    method = 'errorbar'

@Plot.register
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
        ...

@Plot.register
class StickPlot(Plot):
    """A Plot object that plots sticks"""
    default_plot_style = {'basefmt': ' ', 'markerfmt': ' '}
    method = 'stem'

    def plot(self, *params, insert_default_styles=True, **plot_style):
        """
        Plots a set of data | stores the result
        :return: the graphics that matplotlib made
        :rtype:
        """
        ...

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
        ...

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

@Plot.register
class SemiLogXPlot(Plot):
    method = 'semilogx'

@Plot.register
class SemilogYPlot(Plot):
    method = 'semilogy'

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

@Plot.register
class EventPlot(Plot):
    method = 'eventplot'

@Plot.register
class PiePlot(Plot):
    method = 'pie'

    def _get_plot_data(self, data):
        ...

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
        ...

    def _plot_data(self, *data, **plot_style):
        """
        **LLM Docstring**

        Draw the vertical lines via the backend `vlines` method.

        :param data: the resolved `(x, y)` data
        :param plot_style: the styling options
        :return: the backend graphics object
        """
        ...

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
        ...

    def _plot_data(self, *data, **plot_style):
        """
        **LLM Docstring**

        Draw the horizontal lines via the backend `hlines` method.

        :param data: the resolved `(x, y)` data
        :param plot_style: the styling options
        :return: the backend graphics object
        """
        ...

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

class DataPlot(Plot):
    """
    Makes a 2D plot of arbitrary data using a plot method that handles that data type
    """

    def __init__(self, *params, plot_style=None, method=None, figure=None, axes=None, subplot_kw=None, colorbar=None, **opts):
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
        ...

    def _get_plot_data(self, data):
        """
        **LLM Docstring**

        Pass the data array straight through to the plot method.

        :param data: the data to plot
        :return: the data as a one-tuple
        :rtype: tuple
        """
        ...

@Plot.register
class HistogramPlot(DataPlot):
    """
    Makes a Histogram of data
    """
    method = 'hist'

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

@Plot.register
class AutocorrelationPlot(DataPlot):
    method = 'acorr'
    known_styles = {'detrend', 'normed', 'usevlines', 'maxlags', 'linestyle', 'marker', 'data'} | Plot.known_styles

@Plot.register
class AngleSpectrumPlot(DataPlot):
    method = 'angle_spectrum'
    known_styles = {'Fs', 'Fc', 'window', 'pad_to', 'sides', 'data'} | Plot.patch_parms

@Plot.register
class CoherencePlot(DataPlot):
    method = 'cohere'
    known_styles = {'NFFT', 'Fs', 'Fc', 'noverlap', 'pad_to', 'sides', 'scale_by_freq', 'data'} | Plot.known_styles

@Plot.register
class CrossSpectralDensityPlot(DataPlot):
    method = 'csd'

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

@Plot.register
class CrossCorrelationPlot(DataPlot):
    method = 'xcorr'
    known_styles = {'normed', 'usevlines', 'maxlags', 'data', 'linestyle', 'marker'} | Plot.known_styles

@Plot.register
class BoxPlot(DataPlot):
    method = 'boxplot'

@Plot.register
class ViolinPlot(DataPlot):
    method = 'violinplot'

@Plot.register
class BoxAndWhiskerPlot(DataPlot):
    method = 'bxp'

@Plot.register
class HexagonalHistogramPlot(DataPlot):
    method = 'hexbin'

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
        ...

@Plot.register
class QuiverPlot(VectorFieldPlot):
    method = 'quiver'

@Plot.register
class StreamPlot(VectorFieldPlot):
    method = 'streamplot'

@Plot.register
class ArrayPlot(DataPlot):
    """
    Plots an array as an image
    """
    method = 'imshow'
    known_styles = DataPlot.image_params

    def __init__(self, *params, plot_style=None, colorbar=None, figure=None, axes=None, subplot_kw=None, **opts):
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
        ...

    def _get_plot_data(self, data):
        """
        **LLM Docstring**

        Pass the array through to the plot method, densifying a sparse array first.

        :param data: the array (or sparse array)
        :return: the array as a one-tuple
        :rtype: tuple
        """
        ...

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

    def __init__(self, tensor, nrows=None, ncols=None, plot_style=None, colorbar=None, figure=None, axes=None, subplot_kw=None, method='imshow', plot_class=None, **opts):
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
        ...

class Plot2D(Plot):
    """
    A base class for plots of 3D data but plotted on 2D axes
    """
    method = 'contour'

    def __init__(self, *params, plot_style=None, colorbar=None, figure=None, axes=None, subplot_kw=None, **opts):
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
        ...

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
        ...

@Plot.register
class ContourPlot(Plot2D):
    method = 'contourf'

@Plot.register
class ContourLinePlot(ContourPlot):
    method = 'contour'
    known_styles = ContourPlot.known_styles | {'linewidths', 'linestyles', 'negative_linestyles'}

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
    known_styles = {'triangles', 'mask'} | Plot.known_styles

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
        ...

@Plot.register
class TriDensityPlot(Plot2D):
    method = 'tripcolor'
    known_styles = {'alpha', 'norm', 'cmap', 'vmin', 'vmax', 'shading', 'facecolors'}

@Plot.register
class TriContourLinesPlot(Plot2D):
    method = 'tricontour'

@Plot.register
class TriContourPlot(Plot2D):
    method = 'tricontourf'

class ListPlot2D(Plot2D):
    """
    Convenience class that handles the interpolation first
    """

    def __init__(self, *params, plot_style=None, method='contour', colorbar=None, figure=None, axes=None, subplot_kw=None, interpolate=True, **opts):
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
        ...

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
        ...

@Plot.register
class ListContourPlot(ContourPlot):
    _get_plot_data = ListPlot2D._get_plot_data

    def __init__(self, *params, interpolate=True, **opts):
        """
        **LLM Docstring**

        Build a contour plot from scattered points, interpolating them onto a mesh.

        :param params: the scattered point data
        :param interpolate: interpolate onto a mesh
        :type interpolate: bool
        :param opts: plot options
        """
        ...

@Plot.register
class ListDensityPlot(DensityPlot):
    _get_plot_data = ListPlot2D._get_plot_data

    def __init__(self, *params, interpolate=True, **opts):
        """
        **LLM Docstring**

        Build a density plot from scattered points, interpolating them onto a mesh.

        :param params: the scattered point data
        :param interpolate: interpolate onto a mesh
        :type interpolate: bool
        :param opts: plot options
        """
        ...

@Plot.register
class ListTriContourPlot(TriContourPlot):
    _get_plot_data = ListPlot2D._get_plot_data

    def __init__(self, *params, interpolate=True, **opts):
        """
        **LLM Docstring**

        Build a triangulated contour plot from scattered points.

        :param params: the scattered point data
        :param interpolate: interpolate onto a mesh
        :type interpolate: bool
        :param opts: plot options
        """
        ...

@Plot.register
class ListTriDensityPlot(TriDensityPlot):
    _get_plot_data = ListPlot2D._get_plot_data

    def __init__(self, *params, interpolate=True, **opts):
        """
        **LLM Docstring**

        Build a triangulated density plot from scattered points.

        :param params: the scattered point data
        :param interpolate: interpolate onto a mesh
        :type interpolate: bool
        :param opts: plot options
        """
        ...

class Plot3D(Graphics3D):
    """A base class for 3D plots"""
    default_plot_style = {}
    style_mapping = {'format': 'fmt'}
    known_styles = {'fmt'} | Plot.line_params
    method = 'plot_surface'

    def __init__(self, *params, plot_style=None, method=None, colorbar=None, figure=None, axes=None, subplot_kw=None, **opts):
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
        ...

    def _initialize(self):
        """
        **LLM Docstring**

        Mark the 3-D plot initialized, apply its figure options, and add a colorbar if
        one was requested.
        """
        ...

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
        ...

    def _plot_data(self, *data, **plot_style):
        """
        **LLM Docstring**

        Call the backend 3-D plot method on the resolved plot data.

        :param data: the positional plot arguments
        :param plot_style: the styling options
        :return: the backend graphics object
        """
        ...

    def plot(self, *params, **plot_style):
        """
        **LLM Docstring**

        Plot the data on the 3-D axes and store the result, initializing the figure on
        the first call.

        :param params: the plot arguments
        :param plot_style: the styling options (merged with the defaults)
        :return: the backend graphics object
        """
        ...

    def add_colorbar(self, **kw):
        """
        **LLM Docstring**

        Add a colorbar to the 3-D plot (deferring until the figure is initialized).

        :param kw: options for the colorbar
        :return: the colorbar (once initialized)
        """
        ...
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
        ...

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
        ...

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

    def __init__(self, *params, plot_style=None, method=None, colorbar=None, figure=None, axes=None, subplot_kw=None, interpolate=True, **opts):
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
        ...

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
        ...

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
    ...

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
    ...
plot_spec_schema = {'type': str, 'args': list, 'opts': dict}

def plot_multi(*plot_specs: dict, figure=None, plot_type_styles=None, default_type='plot', x=None, y=None, z=None, func=None, common_settings=None, **global_settings):
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
    ...
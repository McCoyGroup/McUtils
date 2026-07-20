"""
Handles all the nastiness of Matplotlib properties so that we can use a more classically python plotting method
"""
from .. import Devutils as dev
from .Backends import DPI_SCALING
from .Styling import Styled, PlotLegend
__all__ = ['GraphicsPropertyManager', 'GraphicsPropertyManager3D']
__reload_hook__ = ['.Styling']

class GraphicsPropertyManager:
    """
    Manages properties for Graphics objects so that concrete GraphicsBase instances don't need to duplicate code, but
    at the same time things that build off of GraphicsBase don't need to implement all of these properties
    """

    def __init__(self, graphics, figure, axes, managed=False):
        """
        **LLM Docstring**

        Set up the property manager that backs a `Graphics` object's styling/layout
        properties, holding references to the graphics, figure, and axes and initializing
        the cached property values.

        :param graphics: the owning graphics object
        :type graphics: GraphicsBase
        :param figure: the backend figure
        :param axes: the backend axes
        :param managed: whether an external manager owns the layout (e.g. a grid panel)
        :type managed: bool
        """
        ...

    @property
    def figure_label(self):
        """
        **LLM Docstring**

        The overall figure label. The getter returns the cached value (reading it from the backend axes when
        unset); the setter caches it and pushes it to the backend axes (unwrapping any
        `Styled` value).

        :return: the figure label
        """
        ...

    @figure_label.setter
    def figure_label(self, label):
        """
        **LLM Docstring**

        The overall figure label. The getter returns the cached value (reading it from the backend axes when
        unset); the setter caches it and pushes it to the backend axes (unwrapping any
        `Styled` value).

        :return: the figure label
        """
        ...

    @property
    def plot_label(self):
        """
        **LLM Docstring**

        The plot title/label. The getter returns the cached value (reading it from the backend axes when
        unset); the setter caches it and pushes it to the backend axes (unwrapping any
        `Styled` value).

        :return: the plot label
        """
        ...

    @plot_label.setter
    def plot_label(self, label):
        """
        **LLM Docstring**

        The plot title/label. The getter returns the cached value (reading it from the backend axes when
        unset); the setter caches it and pushes it to the backend axes (unwrapping any
        `Styled` value).

        :return: the plot label
        """
        ...

    @property
    def style_list(self):
        """
        **LLM Docstring**

        The per-series style cycle. The getter returns the cached styles; the setter
        merges in new styles and pushes them to the backend axes when anything changed.

        :return: the style cycle
        """
        ...

    @style_list.setter
    def style_list(self, props):
        """
        **LLM Docstring**

        The per-series style cycle. The getter returns the cached styles; the setter
        merges in new styles and pushes them to the backend axes when anything changed.

        :return: the style cycle
        """
        ...

    @property
    def plot_legend(self):
        """
        **LLM Docstring**

        The plot legend. The setter coerces legend-like values into a `PlotLegend`
        (accepting `True` to keep an inferred legend).

        :return: the legend
        :raises NotImplementedError: for the unsupported inferred-legend path
        """
        ...

    @plot_legend.setter
    def plot_legend(self, legend):
        """
        **LLM Docstring**

        The plot legend. The setter coerces legend-like values into a `PlotLegend`
        (accepting `True` to keep an inferred legend).

        :return: the legend
        :raises NotImplementedError: for the unsupported inferred-legend path
        """
        ...

    @property
    def legend_style(self):
        """
        **LLM Docstring**

        The legend styling options. The getter returns the cached value (reading it from the backend axes when
        unset); the setter caches it and pushes it to the backend axes (unwrapping any
        `Styled` value).

        :return: the legend style
        """
        ...

    @legend_style.setter
    def legend_style(self, style):
        """
        **LLM Docstring**

        The legend styling options. The getter returns the cached value (reading it from the backend axes when
        unset); the setter caches it and pushes it to the backend axes (unwrapping any
        `Styled` value).

        :return: the legend style
        """
        ...

    @property
    def axes_labels(self):
        """
        **LLM Docstring**

        The `(x, y)` axis labels. The setter fills the missing side from the cached
        labels and pushes each to the backend axes (unwrapping `Styled` values).

        :return: the axis labels
        """
        ...

    @axes_labels.setter
    def axes_labels(self, labels):
        """
        **LLM Docstring**

        The `(x, y)` axis labels. The setter fills the missing side from the cached
        labels and pushes each to the backend axes (unwrapping `Styled` values).

        :return: the axis labels
        """
        ...

    @property
    def plot_range(self):
        """
        **LLM Docstring**

        The plotted `(x, y)` data range. The getter reads (and sorts) the backend limits
        when unset; the setter caches the range and pushes each axis's limits (unwrapping
        `Styled` values).

        :return: the plot range
        """
        ...

    @plot_range.setter
    def plot_range(self, ranges):
        """
        **LLM Docstring**

        The plotted `(x, y)` data range. The getter reads (and sorts) the backend limits
        when unset; the setter caches the range and pushes each axis's limits (unwrapping
        `Styled` values).

        :return: the plot range
        """
        ...

    @property
    def absolute_plot_range(self):
        """
        **LLM Docstring**

        The plot range with any unset axis filled in from the backend limits.

        :return: the absolute plot range
        """
        ...

    @property
    def ticks(self):
        """
        **LLM Docstring**

        The tick specification. The getter returns the cached value; the setter applies
        the x/y tick specs via the tick-setting helpers.

        :return: the tick specification
        """
        ...

    def _set_ticks(self, x, *, set_ticks, set_locator, set_minor_locator, set_formatter, set_minor_formatter, **opts):
        """
        **LLM Docstring**

        Apply a tick specification to one axis, dispatching on the spec type (a
        `Styled` value, a locator, `'auto'`, a fixed list, a `(locations, labels)` or
        `(locator, minor)` pair, or a spacing number) to the appropriate locator and
        formatter, and handling minor ticks and labels.

        :param x: the tick specification
        :param set_ticks: the backend tick-setter
        :param set_locator: the backend major-locator setter
        :param set_minor_locator: the backend minor-locator setter
        :param set_formatter: the backend major-formatter setter
        :param set_minor_formatter: the backend minor-formatter setter
        :param opts: extra tick options (`minor`, `labels`, `minor_labels`, ...)
        """
        ...

    def _set_xticks(self, x, **opts):
        """
        **LLM Docstring**

        Apply a tick specification to the x-axis (via `_set_ticks` with the x-axis
        setters).

        :param x: the tick specification
        :param opts: extra tick options
        """
        ...

    def _set_yticks(self, y, **opts):
        """
        **LLM Docstring**

        Apply a tick specification to the y-axis (via `_set_ticks` with the y-axis
        setters).

        :param y: the tick specification
        :param opts: extra tick options
        """
        ...

    @ticks.setter
    def ticks(self, ticks):
        """
        **LLM Docstring**

        The tick specification. The getter returns the cached value; the setter applies
        the x/y tick specs via the tick-setting helpers.

        :return: the tick specification
        """
        ...

    @property
    def ticks_style(self):
        """
        **LLM Docstring**

        The tick styling. The getter returns the cached value; the setter applies the
        x/y tick styles to the backend axes.

        :return: the tick styling
        """
        ...

    @ticks_style.setter
    def ticks_style(self, ticks_style):
        """
        **LLM Docstring**

        The tick styling. The getter returns the cached value; the setter applies the
        x/y tick styles to the backend axes.

        :return: the tick styling
        """
        ...

    @property
    def frame_style(self):
        """
        **LLM Docstring**

        The frame (spine) styling. The getter returns the cached value; the setter
        applies it to the backend axes.

        :return: the frame styling
        """
        ...

    @frame_style.setter
    def frame_style(self, f_style):
        """
        **LLM Docstring**

        The frame (spine) styling. The getter returns the cached value; the setter
        applies it to the backend axes.

        :return: the frame styling
        """
        ...
    ticks_label_base_styles = {'size', 'color', 'top', 'left', 'right', 'bottom'}
    ticks_label_style_remapping = {'fontsize': 'size', 'fontcolor': 'color'}

    @classmethod
    def clean_tick_label_styles(cls, k):
        """
        **LLM Docstring**

        Normalize a tick-label style key: strip/add the `label` prefix as appropriate and
        apply the style-name remapping.

        :param k: the style key
        :type k: str
        :return: the normalized key
        :rtype: str
        """
        ...

    @property
    def ticks_label_style(self):
        """
        **LLM Docstring**

        The tick-label styling. The getter returns the cached value; the setter applies
        the cleaned label styles to the backend axes.

        :return: the tick-label styling
        """
        ...

    @ticks_label_style.setter
    def ticks_label_style(self, ticks_style):
        """
        **LLM Docstring**

        The tick-label styling. The getter returns the cached value; the setter applies
        the cleaned label styles to the backend axes.

        :return: the tick-label styling
        """
        ...

    @property
    def aspect_ratio(self):
        """
        **LLM Docstring**

        The axes aspect ratio. The getter returns the cached value; the setter pushes it
        to the backend axes (accepting a `(value, opts)` pair).

        :return: the aspect ratio
        """
        ...

    @aspect_ratio.setter
    def aspect_ratio(self, ar):
        """
        **LLM Docstring**

        The axes aspect ratio. The getter returns the cached value; the setter pushes it
        to the backend axes (accepting a `(value, opts)` pair).

        :return: the aspect ratio
        """
        ...

    def _compute_inset_imagesize(self):
        """
        **LLM Docstring**

        Compute the effective image size: for a managed/inset axes, the axes bbox plus
        padding; otherwise the figure size scaled from inches to pixels.

        :return: the `(width, height)` image size
        :rtype: tuple
        """
        ...

    @property
    def image_size(self):
        """
        **LLM Docstring**

        The figure image size in pixels. The getter resolves `'auto'` to the computed
        inset size; the setter caches the size (filling a missing dimension from the
        aspect ratio) and resizes the backend figure (in inches) unless managed/inset.

        :return: the image size
        """
        ...

    @image_size.setter
    def image_size(self, wh):
        """
        **LLM Docstring**

        The figure image size in pixels. The getter resolves `'auto'` to the computed
        inset size; the setter caches the size (filling a missing dimension from the
        aspect ratio) and resizes the backend figure (in inches) unless managed/inset.

        :return: the image size
        """
        ...

    @property
    def axes_bbox(self):
        """
        **LLM Docstring**

        The axes bounding box. The getter reads it from the backend axes; the setter
        pushes a new bbox.

        :return: the axes bbox
        """
        ...

    @axes_bbox.setter
    def axes_bbox(self, bbox):
        """
        **LLM Docstring**

        The axes bounding box. The getter reads it from the backend axes; the setter
        pushes a new bbox.

        :return: the axes bbox
        """
        ...

    @property
    def background(self):
        """
        **LLM Docstring**

        The background/face color. The getter returns the cached value; the setter
        applies it to the backend axes (and figure).

        :return: the background color
        """
        ...

    @background.setter
    def background(self, bg):
        """
        **LLM Docstring**

        The background/face color. The getter returns the cached value; the setter
        applies it to the backend axes (and figure).

        :return: the background color
        """
        ...

    @property
    def frame(self):
        """
        **LLM Docstring**

        Which frame (spine) edges are drawn. The getter returns the cached value; the
        setter applies the visibility spec to the backend axes.

        :return: the frame visibility
        """
        ...

    @frame.setter
    def frame(self, fr):
        """
        **LLM Docstring**

        Which frame (spine) edges are drawn. The getter returns the cached value; the
        setter applies the visibility spec to the backend axes.

        :return: the frame visibility
        """
        ...

    @property
    def scale(self):
        """
        **LLM Docstring**

        The per-axis scaling (e.g. linear/log). The getter returns the cached value; the
        setter applies the x/y scales to the backend axes.

        :return: the axis scaling
        """
        ...

    @scale.setter
    def scale(self, scales):
        """
        **LLM Docstring**

        The per-axis scaling (e.g. linear/log). The getter returns the cached value; the
        setter applies the x/y scales to the backend axes.

        :return: the axis scaling
        """
        ...

    @property
    def padding(self):
        """
        **LLM Docstring**

        The figure padding on each side. The getter returns the cached value; the setter
        caches it and pushes it to the backend.

        :return: the padding
        """
        ...

    @padding.setter
    def padding(self, padding):
        """
        **LLM Docstring**

        The figure padding on each side. The getter returns the cached value; the setter
        caches it and pushes it to the backend.

        :return: the padding
        """
        ...

    @property
    def padding_left(self):
        """
        **LLM Docstring**

        The left figure padding. The getter returns the cached value; the setter updates
        just the left component of the padding.

        :return: the left padding
        """
        ...

    @padding_left.setter
    def padding_left(self, p):
        """
        **LLM Docstring**

        The left figure padding. The getter returns the cached value; the setter updates
        just the left component of the padding.

        :return: the left padding
        """
        ...

    @property
    def padding_right(self):
        """
        **LLM Docstring**

        The right figure padding. The getter returns the cached value; the setter updates
        just the right component of the padding.

        :return: the right padding
        """
        ...

    @padding_right.setter
    def padding_right(self, p):
        """
        **LLM Docstring**

        The right figure padding. The getter returns the cached value; the setter updates
        just the right component of the padding.

        :return: the right padding
        """
        ...

    @property
    def padding_top(self):
        """
        **LLM Docstring**

        The top figure padding. The getter returns the cached value; the setter updates
        just the top component of the padding.

        :return: the top padding
        """
        ...

    @padding_top.setter
    def padding_top(self, p):
        """
        **LLM Docstring**

        The top figure padding. The getter returns the cached value; the setter updates
        just the top component of the padding.

        :return: the top padding
        """
        ...

    @property
    def padding_bottom(self):
        """
        **LLM Docstring**

        The bottom figure padding. The getter returns the cached value; the setter updates
        just the bottom component of the padding.

        :return: the bottom padding
        """
        ...

    @padding_bottom.setter
    def padding_bottom(self, p):
        """
        **LLM Docstring**

        The bottom figure padding. The getter returns the cached value; the setter updates
        just the bottom component of the padding.

        :return: the bottom padding
        """
        ...

    @property
    def spacings(self):
        """
        **LLM Docstring**

        The inter-panel spacings. The getter returns `[0, 0]` for a managed/inset axes,
        else the cached value; the setter converts fractional spacings to absolute sizes
        (from the panel bboxes) and pushes them to the figure.

        :return: the spacings
        """
        ...

    @spacings.setter
    def spacings(self, spacings):
        """
        **LLM Docstring**

        The inter-panel spacings. The getter returns `[0, 0]` for a managed/inset axes,
        else the cached value; the setter converts fractional spacings to absolute sizes
        (from the panel bboxes) and pushes them to the figure.

        :return: the spacings
        """
        ...

    @property
    def colorbar(self):
        """
        **LLM Docstring**

        The colorbar specification. The getter returns the cached value; the setter
        records it and adds a colorbar to the graphics (from `True` or an options dict).

        :return: the colorbar spec
        """
        ...

    @colorbar.setter
    def colorbar(self, c):
        """
        **LLM Docstring**

        The colorbar specification. The getter returns the cached value; the setter
        records it and adds a colorbar to the graphics (from `True` or an options dict).

        :return: the colorbar spec
        """
        ...

class GraphicsPropertyManager3D(GraphicsPropertyManager):

    def __init__(self, graphics, figure, axes, managed=False):
        """
        **LLM Docstring**

        Set up the 3D property manager, adding the cached view-settings and box-ratios
        values.

        :param graphics: the owning graphics object
        :type graphics: GraphicsBase
        :param figure: the backend figure
        :param axes: the backend 3D axes
        :param managed: whether an external manager owns the layout
        :type managed: bool
        """
        ...

    @property
    def axes_labels(self):
        """
        **LLM Docstring**

        The `(x, y, z)` axis labels. The setter fills missing sides from the cached
        labels and pushes each to the backend 3D axes (unwrapping `Styled` values).

        :return: the axis labels
        """
        ...

    @axes_labels.setter
    def axes_labels(self, labels):
        """
        **LLM Docstring**

        The `(x, y, z)` axis labels. The setter fills missing sides from the cached
        labels and pushes each to the backend 3D axes (unwrapping `Styled` values).

        :return: the axis labels
        """
        ...

    @property
    def box_ratios(self):
        """
        **LLM Docstring**

        The 3D box aspect ratios. The getter reads them from the backend when unset; the
        setter resolves `'auto'` from the plot range and pushes the ratios to the backend
        axes.

        :return: the box aspect ratios
        """
        ...

    @box_ratios.setter
    def box_ratios(self, br):
        """
        **LLM Docstring**

        The 3D box aspect ratios. The getter reads them from the backend when unset; the
        setter resolves `'auto'` from the plot range and pushes the ratios to the backend
        axes.

        :return: the box aspect ratios
        """
        ...

    @property
    def projection_type(self):
        """
        **LLM Docstring**

        The 3D projection type, read from / written to the backend axes.

        :return: the projection type
        """
        ...

    @projection_type.setter
    def projection_type(self, ptype):
        """
        **LLM Docstring**

        The 3D projection type, read from / written to the backend axes.

        :return: the projection type
        """
        ...

    @property
    def autoscale(self):
        """
        **LLM Docstring**

        The 3D autoscale setting, read from / written to the backend axes.

        :return: the autoscale setting
        """
        ...

    @autoscale.setter
    def autoscale(self, autoscale):
        """
        **LLM Docstring**

        The 3D autoscale setting, read from / written to the backend axes.

        :return: the autoscale setting
        """
        ...

    @property
    def plot_range(self):
        """
        **LLM Docstring**

        The plotted `(x, y, z)` data range. The getter reads the backend limits when
        unset; the setter fills missing axes from the cache and pushes each axis's limits
        (unwrapping `Styled` values).

        :return: the plot range
        :raises ValueError: for a malformed range specification
        """
        ...

    @plot_range.setter
    def plot_range(self, ranges):
        """
        **LLM Docstring**

        The plotted `(x, y, z)` data range. The getter reads the backend limits when
        unset; the setter fills missing axes from the cache and pushes each axis's limits
        (unwrapping `Styled` values).

        :return: the plot range
        :raises ValueError: for a malformed range specification
        """
        ...

    @property
    def absolute_plot_range(self):
        """
        **LLM Docstring**

        The 3D plot range with any unset axis filled in from the backend limits.

        :return: the absolute plot range
        """
        ...

    def _set_zticks(self, z, **opts):
        """
        **LLM Docstring**

        Apply a tick specification to the z-axis (via `_set_ticks` with the z-axis
        setters).

        :param z: the tick specification
        :param opts: extra tick options
        """
        ...

    @property
    def frame(self):
        """
        **LLM Docstring**

        Which 3D frame edges are drawn. The getter returns the cached value; the setter
        applies the visibility spec to the backend 3D axes.

        :return: the frame visibility
        """
        ...

    @frame.setter
    def frame(self, fr):
        """
        **LLM Docstring**

        Which 3D frame edges are drawn. The getter returns the cached value; the setter
        applies the visibility spec to the backend 3D axes.

        :return: the frame visibility
        """
        ...

    @property
    def frame_style(self):
        """
        **LLM Docstring**

        The 3D frame styling. The getter returns the cached value; the setter applies it
        to the backend 3D axes.

        :return: the frame styling
        """
        ...

    @frame_style.setter
    def frame_style(self, f_style):
        """
        **LLM Docstring**

        The 3D frame styling. The getter returns the cached value; the setter applies it
        to the backend 3D axes.

        :return: the frame styling
        """
        ...

    @property
    def ticks(self):
        """
        **LLM Docstring**

        The 3D tick specification. The getter returns the cached value; the setter applies
        the x/y/z tick specs.

        :return: the tick specification
        """
        ...

    @ticks.setter
    def ticks(self, ticks):
        """
        **LLM Docstring**

        The 3D tick specification. The getter returns the cached value; the setter applies
        the x/y/z tick specs.

        :return: the tick specification
        """
        ...

    @property
    def ticks_style(self):
        """
        **LLM Docstring**

        The 3D tick styling. The getter returns the cached value; the setter applies the
        x/y/z tick styles to the backend axes.

        :return: the tick styling
        """
        ...

    @ticks_style.setter
    def ticks_style(self, ticks_style):
        """
        **LLM Docstring**

        The 3D tick styling. The getter returns the cached value; the setter applies the
        x/y/z tick styles to the backend axes.

        :return: the tick styling
        """
        ...

    @property
    def view_settings(self):
        """
        **LLM Docstring**

        The 3D camera/view settings, read from / written to the backend axes.

        :return: the view settings
        """
        ...

    @view_settings.setter
    def view_settings(self, value):
        """
        **LLM Docstring**

        The 3D camera/view settings, read from / written to the backend axes.

        :return: the view settings
        """
        ...
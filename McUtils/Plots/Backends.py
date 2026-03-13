"""
For now, just a super simple Enum of supported backends
Maybe in the future we'll add better support so that the backends themselves can all support a common subset
of features, but I think we'll 90% of the time just want to use MPL or VTK so who knows...
If that happens, lots of the 'if backend == MPL' stuff will change to use a Backend object
"""

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
        self.get_ticks = tick_getter
        self.set_ticks = tick_setter
        self.set_major_locator = tick_locator
        self.set_minor_locator = minor_tick_locator
        self.set_major_formatter = tick_formatter
        self.set_minor_formatter = minor_tick_formatter


class XAxisManager(AxisManager):
    def get_xticks(self):
        return self.get_ticks()
    def set_xticks(self, ticks, **kwargs):
        return self.set_ticks(ticks, **kwargs)

class YAxisManager(AxisManager):
    def get_yticks(self):
        return self.get_ticks()
    def set_yticks(self, ticks, **kwargs):
        return self.set_ticks(ticks, **kwargs)

class ZAxisManager(AxisManager):
    def get_zticks(self):
        return self.get_ticks()
    def set_zticks(self, ticks, **kwargs):
        return self.set_ticks(ticks, **kwargs)

class GraphicsAxes(metaclass=abc.ABCMeta):
    """
    A wrapper to provide a canonical form for matplotlib.axes.Axes
    so that other backends can plug in cleanly
    """
    def __init__(self):
        self.xaxis = self.get_xaxis_manager()
        self.yaxis = self.get_yaxis_manager()

    def get_xaxis_manager(self):
        return XAxisManager(
            self.get_xticks,
            self.set_xticks,
            None,
            None,
            None,
            None
        )
    def get_yaxis_manager(self):
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
                self.locs = locs
                self.opts = opts

    @classmethod
    def canonicalize_opts(cls, opts):
        return opts
    @abc.abstractmethod
    def remove(self, *, backend):
        ...
    @abc.abstractmethod
    def clear(self, *, backend):
        ...
    def prep_show(self):
        ...

    @abc.abstractmethod
    def get_plotter(self, method):
        ...

    @abc.abstractmethod
    def get_plot_label(self):
        ...
    @abc.abstractmethod
    def set_plot_label(self, val, **style):
        ...

    @abc.abstractmethod
    def get_style_list(self):
        ...
    @abc.abstractmethod
    def set_style_list(self, props):
        ...

    @abc.abstractmethod
    def get_frame_visible(self):
        ...
    @abc.abstractmethod
    def set_frame_visible(self, frame_spec):
        ...
    @abc.abstractmethod
    def get_frame_style(self):
        ...
    @abc.abstractmethod
    def set_frame_style(self, frame_spec):
        ...
    @abc.abstractmethod
    def get_xlabel(self):
        ...
    @abc.abstractmethod
    def set_xlabel(self, val, **style):
        ...
    @abc.abstractmethod
    def get_ylabel(self):
        ...
    @abc.abstractmethod
    def set_ylabel(self, val, **style):
        ...
    @abc.abstractmethod
    def get_xlim(self):
        ...
    @abc.abstractmethod
    def set_xlim(self, val, **opts):
        ...
    @abc.abstractmethod
    def get_ylim(self):
        ...
    @abc.abstractmethod
    def set_ylim(self, val, **opts):
        ...
    @abc.abstractmethod
    def get_xticks(self):
        ...
    @abc.abstractmethod
    def set_xticks(self, val, **opts):
        ...
    @abc.abstractmethod
    def get_yticks(self):
        ...
    @abc.abstractmethod
    def set_yticks(self, val, **opts):
        ...
    @abc.abstractmethod
    def get_xtick_style(self):
        ...
    @abc.abstractmethod
    def set_xtick_style(self, **opts):
        ...
    @abc.abstractmethod
    def get_ytick_style(self):
        ...
    @abc.abstractmethod
    def set_ytick_style(self, **opts):
        ...
    @abc.abstractmethod
    def set_aspect_ratio(self, ar):
        ...
    @abc.abstractmethod
    def get_bbox(self):
        ...
    @abc.abstractmethod
    def set_bbox(self, bbox):
        ...
    @abc.abstractmethod
    def get_facecolor(self):
        ...
    @abc.abstractmethod
    def set_facecolor(self, fg):
        ...
    @abc.abstractmethod
    def get_padding(self):
        ...

    def legend(self, **opts):
        raise NotImplementedError("legend")

    def get_graphics_properties(self, obj, property=None):
        raise NotImplementedError("get_graphics_properties")
    def set_graphics_properties(self, obj, **props):
        raise NotImplementedError("set_graphics_properties")

    @abc.abstractmethod
    def draw_line(self, points, **styles):
        ...
    def draw_point(self, points, **styles):
        return self.draw_disk(points, **styles)
    @abc.abstractmethod
    def draw_disk(self, points, **styles):
        ...
    @abc.abstractmethod
    def draw_rect(self, points, **styles):
        ...
    def draw_triangle(self, points, **styles):
        return self.draw_poly(points, **styles)
    @abc.abstractmethod
    def draw_poly(self, points, **styles):
        ...
    @abc.abstractmethod
    def draw_arrow(self, points, **styles):
        ...
    @abc.abstractmethod
    def draw_text(self, points, vals, **styles):
        ...

class GraphicsAxes3D(GraphicsAxes):
    def __init__(self):
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
        ...
    @abc.abstractmethod
    def set_zlim(self, val, **opts):
        ...
    @abc.abstractmethod
    def get_zticks(self):
        ...
    @abc.abstractmethod
    def set_zticks(self, val, **opts):
        ...
    @abc.abstractmethod
    def get_ztick_style(self):
        ...
    @abc.abstractmethod
    def set_ztick_style(self, **opts):
        ...

    def set_projection_type(self, proj_type, **kwargs):
        ...
    def get_projection_type(self):
        ...

    def get_autoscale(self):
        ...
    def set_autoscale(self, autoscale):
        ...

    @abc.abstractmethod
    def get_view_settings(self):
        ...
    @abc.abstractmethod
    def set_view_settings(self, **ops):
        ...

    @abc.abstractmethod
    def draw_sphere(self, points, rads, **styles):
        ...

    @abc.abstractmethod
    def draw_cylinder(self, start, end, rad, circle_points=48, **opts):
        ...

    @abc.abstractmethod
    def draw_box(self, start, end, **opts):
        ...

class GraphicsFigure(metaclass=abc.ABCMeta):
    """
    A wrapper to provide a canonical form for matplotlib.figure.Figure
    so that other backends can plug in cleanly
    """
    Axes = None
    def __init__(self, axes=None):
        self.axes = axes
    @classmethod
    def construct(self, **kw) -> 'GraphicsFigure':
        raise NotImplementedError("needs an overload")
    @classmethod
    def canonicalize_opts(cls, opts):
        return opts
    @abc.abstractmethod
    def create_axes(self, rows, cols, spans, **kw) -> 'GraphicsAxes':
        ...
    @abc.abstractmethod
    def create_inset(self, bbox, **kw) -> 'GraphicsAxes':
        ...
    def create_colorbar(self, graphics, axes, norm=None, cmap=None, **kw):
        raise NotImplementedError("create_colorbar")
    def add_axes(self, ax) -> 'GraphicsAxes':
        if self.axes is None: self.axes = []
        if not isinstance(ax, self.Axes): ax = self.Axes(ax)
        self.axes.append(ax)
        return ax
    @abc.abstractmethod
    def clear(self, *, backend):
        ...
    @abc.abstractmethod
    def close(self, *, backend):
        ...

    def get_bboxes(self):
        return [
            a.get_bbox() for a in self.axes
        ]
    def prep_show(self):
        if self.axes is not None:
            for a in self.axes:
                a.prep_show()

    @abc.abstractmethod
    def get_size_inches(self):
        ...
    @abc.abstractmethod
    def set_size_inches(self, w, h):
        ...
    @abc.abstractmethod
    def set_extents(self, extents):
        ...

    @abc.abstractmethod
    def get_facecolor(self):
        ...
    @abc.abstractmethod
    def set_facecolor(self, fg):
        ...

    @abc.abstractmethod
    def savefig(self, file, **opts):
        ...

    @abc.abstractmethod
    def animate_frames(self, frames, **animation_opts):
        ...

    def to_html(self):
        raise NotImplementedError("needs an overload")
    def to_widget(self, **opts):
        raise NotImplementedError("needs an overload")
    def _repr_html_(self):
        return self.to_html()
    def get_mime_bundle(self):
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
        ...


class GraphicsBackend(metaclass=abc.ABCMeta):
    Figure = GraphicsFigure
    @abc.abstractmethod
    def create_figure(self, *args, **kwargs) -> 'tuple[GraphicsFigure, tuple[GraphicsAxes]]':
        ...
    def create_axes(self, figure:'GraphicsFigure', *args, **kwargs):
        return figure.create_axes(*args, **kwargs, backend=self)
    def create_inset(self, figure, *args, **kw) -> 'GraphicsAxes':
        return figure.create_inset(*args, **kw)
    def close_figure(self, figure:'GraphicsFigure'):
        return figure.close(backend=self)
    def remove_axes(self, axes:'GraphicsAxes'):
        return axes.remove(backend=self)
    def clear_figure(self, figure:'GraphicsFigure'):
        return figure.clear(backend=self)
    def clear_axes(self, axes:'GraphicsAxes'):
        return axes.clear(backend=self)
    @abc.abstractmethod
    def get_interactive_status(self) -> 'bool':
        ...
    @abc.abstractmethod
    def disable_interactivity(self):
        ...
    @abc.abstractmethod
    def enable_interactivity(self):
        ...
    @abc.abstractmethod
    def show_figure(self, figure, reshow=None):
        ...
    def to_widget(self, figure:GraphicsFigure):
        return figure.to_widget()

    @abc.abstractmethod
    def get_available_themes(self):
        ...
    class ThemeContextManager(metaclass=abc.ABCMeta):
        def __init__(self, theme_parents, theme_spec):
            self.spec = self.canonicalize_theme_opts(theme_parents, theme_spec)

        @classmethod
        @abc.abstractmethod
        def canonicalize_theme_opts(self, theme_parents, theme_spec):
            ...
        @abc.abstractmethod
        def __enter__(self):
            ...
        @abc.abstractmethod
        def __exit__(self, exc_type, exc_val, exc_tb):
            ...
    def theme_context(self, theme_parents, spec):
        return self.ThemeContextManager(theme_parents, spec)

    class DefaultBackends(enum.Enum):
        MPL = 'matplotlib'
        MPL3D = 'matplotlib3D'
        VTK = 'vtk'
        VPython = 'vpython'
        VPython2D = 'vpython2D'
        X3D = 'x3d'
        SceneJSON = 'json'
        Plotly = 'plotly'

    registered_backends = {}
    @classmethod
    def get_default_backends(cls):
        return {
            cls.DefaultBackends.MPL.value: MPLBackend,
            cls.DefaultBackends.MPL3D.value: MPLBackend3D,
            cls.DefaultBackends.Plotly.value: PlotlyBackend,
            cls.DefaultBackends.VTK.value: VTKBackend,
            cls.DefaultBackends.VPython2D.value: VPythonBackend,
            cls.DefaultBackends.VPython.value: VPythonBackend3D,
            cls.DefaultBackends.X3D.value: X3DBackend,
            cls.DefaultBackends.SceneJSON.value: SceneJSONBackend,
        }
    @classmethod
    def lookup(cls, backend, opts=None) -> 'GraphicsBackend':
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
        if cls._plt is None:
            import matplotlib.pyplot as plt
            cls._plt = plt
        return cls._plt
    @classmethod
    def mpl_api(cls):
        if cls._mpl is None:
            import matplotlib as mpl
            cls._mpl = mpl
        return cls._mpl
    @classmethod
    def color_api(cls):
        if cls._colors is None:
            import matplotlib.colors as colors
            cls._colors = colors
        return cls._colors

    @classmethod
    def patch_api(cls):
        if cls._patch is None:
            import matplotlib.patches as patch
            cls._patch = patch
        return cls._patch
    @classmethod
    def path_api(cls):
        if cls._path is None:
            import matplotlib.path as patch
            cls._path = patch
        return cls._path
    @classmethod
    def collections_api(cls):
        if cls._coll is None:
            import matplotlib.collections as coll
            cls._coll = coll
        return cls._coll
    @classmethod
    def widgets_api(cls):
        if cls._widg is None:
            import matplotlib.widgets as widg
            cls._widg = widg
        return cls._widg
    @classmethod
    def animations_api(cls):
        if cls._anim is None:
            import matplotlib.animation as anim
            cls._anim = anim
        return cls._anim
    @classmethod
    def draw_if_interactive(self, *args, **kwargs):
        pass
    @classmethod
    def magic_backend(self, backend):
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
        self.obj = mpl_axes_object
        self.opts = self.canonicalize_opts(opts)
        super().__init__()
        self.xaxis = self.obj.xaxis
        self.yaxis = self.obj.yaxis

    class TicksManager:
        def __init__(self):
            import matplotlib.ticker as ticks
            self._Locator = ticks.Locator
            self._FixedLocator = ticks.FixedLocator
        @property
        def Locator(self):
            return self._Locator
        @property
        def FixedLocator(self):
            return self._FixedLocator

    def clear(self, *, backend=None):
        ax = self.obj
        all_things = ax.artists + ax.patches
        for a in all_things:
            a.remove()
    def remove(self, *, backend):
        self.obj.remove()

    def get_plotter(self, method):
        plot_method = getattr(self.obj, method)
        def plot(*data, **styles):
            return plot_method(*data, **styles)
        return plot


    def get_plot_label(self):
        return self.obj.set_title()
    def set_plot_label(self, val, **style):
        self.obj.set_title(val, **style)

    def get_style_list(self):
        raise NotImplementedError("style list cyclers not supported")
    def set_style_list(self, props):
        self.obj.set_prop_cycle(**props)

    def get_frame_visible(self):
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
        if frame_spec is True:
            self.obj.set_frame_on(frame_spec)
        elif frame_spec is False:
            self.obj.set_frame_off(frame_spec)
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

    def get_xlabel(self):
        return self.obj.get_xlabel()
    def set_xlabel(self, val, **style):
        self.obj.set_xlabel(val, **style)
    def get_ylabel(self):
        return self.obj.get_ylabel()
    def set_ylabel(self, val, **style):
        self.obj.set_ylabel(val, **style)

    def get_xlim(self):
        return self.obj.get_xlim()
    def set_xlim(self, val, **opts):
        self.obj.set_xlim(val, **opts)
    def get_ylim(self):
        return self.obj.get_ylim()
    def set_ylim(self, val, **opts):
        self.obj.set_ylim(val, **opts)

    def get_xticks(self):
        return self.obj.get_xticks()
    def set_xticks(self, val, **opts):
        self.obj.set_xticks(val, **opts)

    def get_yticks(self):
        return self.obj.get_yticks()
    def set_yticks(self, val, **opts):
        self.obj.set_yticks(val, **opts)

    def get_xtick_style(self):
        return self.obj.tick_params(axis='x')
    def set_xtick_style(self, **opts):
        return self.obj.tick_params(axis='x', **opts)
    def get_ytick_style(self):
        return self.obj.tick_params(axis='y')
    def set_ytick_style(self, **opts):
        return self.obj.tick_params(axis='y', **opts)

    def set_aspect_ratio(self, ar):
        if nput.is_numeric(ar):
            a, b = self.get_xlim(), self.get_ylim()
            if a is not None and b is not None:
                cur_ar = abs(b[1] - b[0]) / abs(a[1] - a[0])
                ar = ar / cur_ar
        self.obj.set_aspect(ar)

    def get_bbox(self):
        bbox = self.obj.get_position()
        if hasattr(bbox, 'get_points'):
            bbox = bbox.get_points()
        bbox = [
            [b*DPI_SCALING for b in bb]
            for bb in bbox
        ]

        return bbox
    def set_bbox(self, bbox):
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
        return self.obj.get_facecolor()
    def set_facecolor(self, fg):
        if isinstance(fg, str) and fg == 'transparent':
            fg = 'none'
        return self.obj.set_facecolor(fg)

    def get_padding(self):
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
        return self.get_plotter('legend')(**opts)

    def get_graphics_properties(self, obj, property=None):
        from matplotlib.artist import getp

        return getp(obj, property=property)
    def set_graphics_properties(self, obj, **props):
        from matplotlib.artist import setp

        return setp(obj, **props)

    def draw_line(self, points, **styles):
        points = np.asanyarray(points)
        if points.ndim == 2:
            points = points[np.newaxis]
        return self.get_plotter('plot')(
            points[:, 0],
            points[:, 1],
            **styles
        )

    def draw_disk(self, points, radius=None, s=None, **styles):
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
        points = np.asanyarray(points)
        if points.ndim == 2:
            points = points[np.newaxis]
        return self.get_plotter('arrow')(
            *points[0],
            *(points[1] - points[0]),
            **styles
        )

    def draw_text(self, points, vals, **styles):
        points = np.asanyarray(points)
        if points.ndim == 1:
            points = points[np.newaxis]
        if isinstance(vals, str):
            vals = [vals]

        text_plotter = self.get_plotter('text')
        text = [
             text_plotter(*pt, txt, **styles)
             for pt, txt in zip(points, vals)
        ]

        return text

class MPLAxes3D(MPLAxes):
    def __init__(self, mpl_axes_object, **opts):
        super().__init__(mpl_axes_object, **opts)
        self.zaxis = self.obj.zaxis
        self.computed_zorder = self.obj.computed_zorder
        self._monkeypatch_draw(self.obj)
        self._dist = None

    def set_projection_type(self, proj_type, **kwargs):
        if proj_type is not None:
            return self.obj.set_proj_type(proj_type, **kwargs)
    def get_projection_type(self):
        return self.obj.get_proj_type()

    def get_autoscale(self):
        return self.obj.autoscale()
    def set_autoscale(self, autoscale):
        return self.obj.autoscale(autoscale)

    @classmethod
    def _get_dist(cls, artist):
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
        if hasattr(obj, 'predraw'):
            obj.predraw(dist)

    zdir_map = {
        'x':[1, 0, 0],
        'y':[0, 1, 0],
        'z':[0, 0, 1],
    }
    @classmethod
    def _transform_zdir(cls, zdir):
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
        cls._set_patch_3d_properties(self, path.vertices, zs, zdir=zdir, axlim_clip=axlim_clip)
        self._code3d = path.codes

    @classmethod
    def _pathpatch_translate(cls, pathpatch, delta):
        pathpatch._segment3d += np.asarray(delta)

    @classmethod
    def _patch_do_3d_projection(cls, self, mode=None):
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
        cur_draw = obj.draw
        obj.computed_zorder = False

        @functools.wraps(obj.draw)
        def draw(renderer):
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
        if frame_spec is True:
            self.obj.set_axis_on()
        elif frame_spec is False:
            self.obj.set_axis_off()

    def get_zlim(self):
        return self.obj.get_zlim()
    def set_zlim(self, val, **opts):
        self.obj.set_zlim(val, **opts)

    def get_zticks(self):
        return self.obj.get_zticks()
    def set_zticks(self, val, **opts):
        self.obj.set_zticks(val, **opts)

    def get_ztick_style(self):
        return self.obj.tick_params(axis='z')
    def set_ztick_style(self, **opts):
        return self.obj.tick_params(axis='z', **opts)

    def get_box_aspect(self):
        return self.obj.get_box_aspect()
    def set_box_aspect(self, br, **kwargs):
        return self.obj.set_box_aspect(br, **kwargs)

    def get_view_settings(self):
        return {'elev': self.obj.elev, 'azim':self.obj.azim,
                'roll':self.obj.roll, 'vertical_axis':self.obj.vertical_axis,
                'dist':self.obj.dist}
    def set_view_settings(self,
                          elev=None, azim=None, roll=None, vertical_axis=None, dist=None,
                          up_vector=None, right_vector=None, view_vector=None, view_distance=None,
                          view_matrix=None,
                          **values):
        if view_distance is not None:
            dist = view_distance
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
                    view_vector = nput.vec_crosses([0, 0, 1], right_vector, normalize=True)
                elif up_vector is not None:
                    view_vector = nput.vec_crosses(up_vector, [0, 1, 0], normalize=True)

            if view_vector is not None:
                m = nput.rotation_matrix(
                    view_vector,
                    [1, 0, 0]
                )
            else:
                m = np.eye(3)

            if up_vector is None and right_vector is not None:
                if view_vector is None:
                    view_vector = [1, 0, 0]
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
                    [1, 0, 0]
                )
            view_matrix = m

        if view_matrix is not None:
            if vertical_axis is None:
                target_vertical = [0, 0, 1]
                target_view = [1, 0, 0]
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
            # roll, cross = nput.extract_rotation_angle_axis(view_matrix)
            view_vector, right_vector, up_vector = view_matrix.T
            elev = np.rad2deg(nput.vec_angles(target_vertical, up_vector, return_crosses=False))
            azim = np.rad2deg(nput.vec_angles(right_vector, target_view,
                                              up_vectors=np.asanyarray(target_vertical),
                                              return_crosses=False))
            # roll = np.rad2deg(nput.vec_angles([1, 0, 0], view_vector, return_crosses=False))
            # elev = nput.vec_angles([1, 0, 0], view_vector, return_crosses=False)

        # if isinstance(value, dict):
        #     if 'elev' not in value:
        #         value['elev'] = self.obj.elev
        #     if 'azim' not in value:
        #         value['azim'] = self.obj.azim
        #     if 'roll' not in value:
        #         value['roll'] = self.obj.arollzim
        #     if 'vertical_axis' not in value:
        #         value['vertical_axis'] = self.obj.vertical_axis
        # else:
        #     value = dict(zip(['elev', 'azim', 'roll', 'vertical_axis'], value))
        values = values | {
            k:v for k,v in
            dict(elev=elev, azim=azim, roll=roll, vertical_axis=vertical_axis).items()
            if v is not None
        }
        self.obj.view_init(**values)
        if dist is not None:
            self._dist = dist
            self.obj.dist = dist
            # self.obj.set_box_aspect(None, zoom=(1.8294640721620434 * 25/24) / (dist / 10)) # magic number from MPL

    def prep_show(self):
        if self._dist is not None:
            self.obj.dist = self._dist

    @classmethod
    def _get_axis_scaling(cls, sphere_path):
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
                    s.zdist_offset = functools.partial(self._get_sphere_proj, radius=r)
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
                spheres.zdist_offset = functools.partial(self._get_sphere_proj, radius=np.max(dists))
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
        if cls._off_stroke is None:
            import matplotlib.patheffects as pe
            class OffsetStroke(pe.Stroke):
                def __init__(self, offset=(0, 0), pixel_scaling=1, stroke_offset=.025, **kwargs):
                    self._scaling = pixel_scaling
                    super().__init__(offset, **kwargs)
                    self._stroke_offset = stroke_offset

                def draw_path(self, renderer, gc, tpath, affine, rgbFace):
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
                        l.zdist_offset = functools.partial(self._get_line_proj, radius=cw)
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

    @classmethod
    def _arc_proj_max(cls, zs):
        return 2*np.min(zs) - np.max(zs)
    def draw_disk(self, centers, radius=None, angle=None, normal=None, uv_axes=None, zdir=None,
                  theta1=None, theta2=None,
                  rendering='flat', box_scalings=None,
                  line_color=None, line_thickness=None,
                  color=None,
                  glow=None,
                  lw=None,
                  **styles):
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
            angs, crosses = nput.vec_angles([0, 0, 1], normal, return_crosses=True, return_norms=False)
            embedding_axes = nput.rotation_matrix(crosses, angs)
            # local_x, local_y, local_z = embedding_axes
            emb_u, emb_v = np.array([u, v]) @ embedding_axes
            # emb_angle, ax2 = nput.vec_angles(local_x, emb_u)
            emb_u = nput.vec_normalize(emb_u)
            # emb_v = nput.vec_normalize(emb_v)
            # det = emb_u[0] * emb_v[1] - emb_u[1] * emb_v[0]
            emb_angle = np.arccos(emb_u[0])
            # raise Exception(angs, det)
            if normal[2] > 0:
                emb_angle = 2*np.pi - emb_angle
            # emb_angle = np.arccos(emb_v[0])
            #     emb_angle, ax2 = nput.vec_angles(local_x, u)
            # else:
            #     emb_angle, ax2 = nput.vec_angles(local_x, v)
            # emb_angle = uv_sign * emb_angle
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
                a = patches.Arc((0, 0), 2 * r, 2 * r,
                                theta1=t1, theta2=t2)
                p = a.get_path()
                # codes = list(p.codes)
                # codes[-1] = p.STOP
                a = patches.PathPatch(
                    paths.Path(p.vertices, p.codes),
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
            self._monkeypatch_patch(a, c, zdir=zd, zorder_mode=self._arc_proj_max)
            self.obj.add_patch(a)

        return arcs

    _Arrow3D = None
    @classmethod
    def _load_arrow_drawer(cls):
        if cls._Arrow3D is None:
            from mpl_toolkits.mplot3d.proj3d import proj_transform
            from matplotlib.patches import FancyArrowPatch
            class Arrow3D(FancyArrowPatch):

                def __init__(self, x, y, z, dx, dy, dz, *args, **kwargs):
                    super().__init__((0, 0), (0, 0), *args, **kwargs)
                    self._xyz = (x, y, z)
                    self._dxdydz = (dx, dy, dz)

                def draw(self, renderer):
                    x1, y1, z1 = self._xyz
                    dx, dy, dz = self._dxdydz
                    x2, y2, z2 = (x1 + dx, y1 + dy, z1 + dz)

                    xs, ys, zs = proj_transform((x1, x2), (y1, y2), (z1, z2), self.axes.M)
                    self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
                    super().draw(renderer)

                distance_mode = staticmethod(np.min)
                def do_3d_projection(self, renderer=None, mode=None):
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
        if dev.str_is(rendering, 'flat'):
            points = np.asanyarray(points)
            if points.ndim == 1:
                points = points[np.newaxis]
            Arrow3D = self._load_arrow_drawer()
            points = np.asanyarray(points)
            if points.ndim == 2:
                points = points[np.newaxis]
            diffs = points[:, 1, :] - points[:, 0, :]
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
        if billboard:
            normal = None
        if zdir is None:
            zdir = normal
            if isinstance(zdir, np.ndarray): zdir = tuple(float(z) for z in zdir)
        return super().draw_text(points, vals, zdir=zdir, **styles)

    def draw_box(self, start, end, **opts):
        raise NotImplementedError(...)
class MPLFigure(GraphicsFigure):
    Axes = MPLAxes
    default_display_format = 'png'
    _refs = set()
    def __init__(self, mpl_figure_object, display_format=None, **opts):
        if mpl_figure_object in self._refs: raise ValueError(...)
        self._refs.add(mpl_figure_object)
        self.obj = mpl_figure_object
        if display_format is None:
            display_format = self.default_display_format
        self.display_format = display_format
        super().__init__(**self.canonicalize_opts(opts))
    def __hash__(self): # we need weakref to behave right
        return hash(self.obj)
    def create_axes(self, rows, cols, spans, **kw):
        return self.add_axes(
            self.obj.add_subplot((rows, cols, spans), **kw)
        )
    def create_inset(self, bbox, **kw) -> 'GraphicsAxes':
        ((x, y), (X, Y)) = bbox
        return self.add_axes(
            self.obj.add_axes([x, y, X-x, Y-y], **kw)
        )
    def clear(self, *, backend):
        raise NotImplementedError(...)
    def close(self, *, backend):
        return backend.plt.close(self.obj)

    _cb_opts = ("orientation", "extendfrac", "extendrect", "drawedges", "boundaries", "spacing")
    def create_colorbar(self, graphics, axes, norm=None, cmap=None, **kw):
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
        return self.obj.suptitle()
    def set_figure_label(self, val, **style):
        self.obj.suptitle(val, **style)

    def get_size_inches(self):
        return self.obj.get_size_inches()
    def set_size_inches(self, w, h):
        self.obj.set_size_inches(w, h)

    def set_extents(self, extents):
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
        if isinstance(spacing, (list, tuple)):
            w,h = spacing
        else:
            w = h = spacing
        self.obj.subplots_adjust(wspace=w, hspace=h)

    def get_facecolor(self):
        return self.obj.get_facecolor()
    def set_facecolor(self, fg):
        if isinstance(fg, str) and fg == 'transparent':
            fg = 'none'
        return self.obj.set_facecolor(fg)

    def savefig(self, file, facecolor=None, **opts):
        if dev.str_is(facecolor, 'transparent'):
            facecolor = 'none'
        return self.obj.savefig(file, facecolor=facecolor, **opts)

    def animate_frames(self, frames, export_html=True, **animation_opts):
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
        if format is None:
            format = self.display_format
        if format == 'svg':
            html = self.to_svg()
        else:
            html = self.obj._repr_html_()
        return html
    def to_data_url(self):
        buf = io.BytesIO()
        self.obj.savefig(buf, format='png')
        buf.seek(0)
        b64_img = base64.b64encode(buf.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{b64_img}"
    def to_svg(self):
        buf = io.StringIO()
        self.obj.savefig(buf, format='svg')
        buf.seek(0)
        return buf.read()
    def to_widget(self, format=None, autoclose=True):
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
        if self.display_format == 'svg':
            return {
                'image/svg+xml':self.to_svg()
            }
        else:
            return super().get_mime_bundle()
    def tight_layout(self):
        self.obj.tight_layout()

class MPLBackend(GraphicsBackend):
    Figure = MPLFigure
    @property
    def plt(self):
        return MPLManager.plt_api()
    @property
    def mpl(self):
        return MPLManager.mpl_api()
    def create_figure(self, *args, **kwargs):
        Axes = self.Figure.Axes
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
        self.plt.show()

    class ThemeContextManager(GraphicsBackend.ThemeContextManager):
        def __init__(self, theme_parents, theme_spec):
            super().__init__(theme_parents, theme_spec)
            self.context = MPLManager.plt_api().style.context(self.spec)

        @classmethod
        def canonicalize_theme_opts(self, theme_parents, theme_opts) -> 'tuple[list[str], dict]':
            from cycler import cycler

            theme_dict = {}
            for k,v in theme_opts.items():
                if isinstance(v, dict):
                    for sk,sv in v.items():
                        if isinstance(sv, dict):
                            sv = cycler(**sv)
                        theme_dict[k+'.'+sk] = sv
                # else:
                #     theme_dict[k] = v
            return theme_parents + [theme_dict]

        def __enter__(self):
            return self.context.__enter__()
        def __exit__(self, exc_type, exc_val, exc_tb):
            return self.context.__exit__(exc_type, exc_val, exc_tb)

    def show_figure(self, graphics:MPLFigure, autoclose=True, reshow=None):
        from ..Jupyter.JHTML import JupyterAPIs
        dynamic_loading = JupyterAPIs().in_jupyter_environment()
        if not dynamic_loading:
            self.plt.show()
        else:
            display = JupyterAPIs().display_api
            graphics.shown = True
            html = graphics.to_widget()
            if autoclose:
                self.close_figure(graphics)
            display.clear_output(wait=True)
            return html.display()
            # return display.display(display.HTML(html))
        # self.plt.show()
        # return graphics.show_mpl(self, reshow=reshow)
    def to_widget(self, figure:GraphicsFigure, autoclose=True):
        widg = super().to_widget(figure)
        if autoclose:
            self.close_figure(figure)
        return widg

    def get_interactive_status(self) -> 'bool':
        return self.plt.isinteractive()
    def disable_interactivity(self):
        return self.plt.ioff()
    def enable_interactivity(self):
        return self.plt.ion()
    def get_available_themes(self):
        import matplotlib.style as sty
        theme_names = sty.available
        return theme_names

class MPLFigure3D(MPLFigure):
    Axes = MPLAxes3D
    default_display_format = 'svg'
    def create_axes(self, rows, cols, spans, projection='3d', **kw):
        return super().create_axes(rows, cols, spans, projection=projection, **kw)
class MPLBackend3D(MPLBackend):
    Figure = MPLFigure3D
    def create_figure(self, *args, subplot_kw=None, **kwargs):
        from mpl_toolkits.mplot3d import Axes3D
        subplot_kw = dict({"projection": '3d'}, **({} if subplot_kw is None else subplot_kw))
        return super().create_figure(*args, subplot_kw=subplot_kw, **kwargs)

class PlotlyAxes(GraphicsAxes):
    base_axis_theme = {}
    base_theme = {}
    def __init__(self, elements=None, xaxis=None, yaxis=None, **opts):
        if elements is None:
            elements = []
        self.elements = elements
        if xaxis is None:
            xaxis = self.base_axis_theme
        if yaxis is None:
            yaxis = self.base_axis_theme
        self.opts = self.canonicalize_opts(self.base_theme|opts|dict(yaxis=yaxis, xaxis=xaxis))
        super().__init__()

    def clear(self, *, backend=None):
        self.elements = []
    def remove(self, *, backend):
        self.elements = []

    def prep_elems(self):
        return self.elements
    def prep_opts(self):
        opts = self.opts
        for lab in ['xaxis', 'yaxis']:
            if lab in opts:
                opts[lab] = {k:v for k,v in opts[lab].items() if v is not None}
        return opts
    def get_plot_label(self):
        return self.opts.get('title')
    def set_plot_label(self, val, **style):
        self.opts['title'] = (val, style)

    def get_style_list(self):
        raise NotImplementedError("style list cyclers not supported")
    def set_style_list(self, props):
        self._prop_cycle = props

    def get_frame_visible(self):
        return (
            (
                self.opts.get('yaxis', {}).get('showline', True),
                self.opts.get('yaxis2', {}).get('showline', False)
            ),
            (
                self.opts.get('xaxis', {}).get('showline', True),
                self.opts.get('xaxis2', {}).get('showline', False)
            )
        )
    def set_frame_visible(self, frame_spec):
        if frame_spec is True or frame_spec is False:
            frame_spec = (frame_spec, frame_spec)
        lr, bt = frame_spec
        if lr in {True, False}:
            l,r = lr,lr
        else:
            l,r = lr
        if bt in {True, False}:
            b,t = bt,bt
        else:
            b,t = bt
        if l:
            if r:
                self.opts['yaxis'] = self.opts.get('yaxis', {}) | {'showline': True, 'linecolor':'black', 'mirror':True}
            else:
                self.opts['yaxis'] = self.opts.get('yaxis', {}) | {'showline': True, 'linecolor':'black'}
        elif r:
            self.opts['yaxis'] = self.opts.get('yaxis', {}) | {'showline': True, 'linecolor':'black', 'side':'right'}
        if b:
            if t:
                self.opts['xaxis'] = self.opts.get('xaxis', {}) | {'showline': True, 'linecolor':'black', 'mirror':True}
            else:
                self.opts['xaxis'] = self.opts.get('xaxis', {}) | {'showline': True, 'linecolor':'black'}
        elif t:
            self.opts['xaxis'] = self.opts.get('xaxis', {}) | {'showline': True, 'linecolor':'black', 'side':'top'}

    def get_frame_style(self):
        raise NotImplementedError(...)
    def set_frame_style(self, frame_spec):
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
        return self.opts.get('xaxis', {}).get('title_text')
    def set_xlabel(self, val, **style):
        self.opts['xaxis'] = self.opts.get('xaxis', {}) | dict(
            title_text=val,
            **style
        )
    def get_ylabel(self):
        return self.opts.get('yaxis', {}).get('title_text')
    def set_ylabel(self, val, **style):
        self.opts['yaxis'] = self.opts.get('yaxis', {}) | dict(
            title_text=val,
            **style
        )

    def get_plot_range(self):
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
        xrange = self.opts.get('xaxis', {}).get('range')
        if xrange is None:
            xrange, _ = self.get_plot_range()
        return xrange
    def set_xlim(self, val, **opts):
        self.opts['xaxis'] = self.opts.get('xaxis', {}) | dict(
            range=val,
            **opts
        )
    def get_ylim(self):
        yrange = self.opts.get('yaxis', {}).get('range')
        if yrange is None:
            _, yrange = self.get_plot_range()
        return yrange
    def set_ylim(self, val, **opts):
        self.opts['yaxis'] = self.opts.get('yaxis', {}) | dict(
            range=val,
            **opts
        )

    def get_xticks(self):
        return self.opts.get('xaxis', {}).get('tickvals')
    def set_xticks(self, val, **opts):
        if isinstance(val, self.TicksManager.FixedLocator):
            val = val.locs
        self.opts['xaxis'] = self.opts.get('xaxis', {}) | dict(
            tickvals=val,
            tickmode='array',
            **opts
        )
    def get_yticks(self):
        return self.opts.get('yaxis', {}).get('tickvals')
    def set_yticks(self, val, **opts):
        if isinstance(val, self.TicksManager.FixedLocator):
            val = val.locs
        self.opts['yaxis'] = self.opts.get('yaxis', {}) | dict(
            tickvals=val,
            tickmode='array',
            **opts
        )

    def get_xtick_style(self):
        return {
            k:v
            for k,v in self.opts.get('xaxis', {}).items()
            if k.startswith('tick') or k.startswith('minor')
        }
    def set_xtick_style(self, **opts):
        self.opts['xaxis'] = self.opts.get('xaxis', {}) | opts
    def get_ytick_style(self):
        return {
            k:v
            for k,v in self.opts.get('yaxis', {}).items()
            if k.startswith('tick') or k.startswith('minor')
        }
    def set_ytick_style(self, **opts):
        self.opts['yaxis'] = self.opts.get('yaxis', {}) | opts

    def get_aspect_ratio(self):
        return self.opts.get('aspect_ratio')
        # y = self.opts.get('yaxis', {})
        # if y.get('scaleanchor', '') == 'x':
        #     return y.get('scaleratio')
        # else:
        #     return None
    def set_aspect_ratio(self, ar):
        self.opts['aspect_ratio'] = ar
        # if not dev.str_is(ar, 'auto'):
        #     # self.opts['xaxis'] = self.opts.get('xaxis', {}) | {'scaleratio': 1}
        #     self.opts['yaxis'] = self.opts.get('yaxis', {}) | {
        #         'scaleanchor': 'x',
        #         'scaleratio': ar,
        #         'constrain': "domain"
        #     }


    def get_bbox(self):
        ...
    def set_bbox(self, bbox):
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
        for k,a in self.style_mapping.items():
            if k in opts:
                opts[a] = opts.pop(k)
        if line is None:
            line = {}
            for k in self.line_options:
                if k in opts:
                    line[k] = opts.pop(k)
        return line, opts
    def plot(self, x, y, line=None, mode='lines', **opts):
        # import plotly.graph_objects as go
        opts['mode'] = mode
        line, opts = self._prep_line_opts(line, opts)
        plot_dict = dict(type='scatter', x=x, y=y, line=line, **opts)
        self.elements.append(plot_dict)
        return plot_dict
    def scatter(self, x, y, line=None, mode='markers', **opts):
        # import plotly.graph_objects as go
        opts['mode'] = mode
        line, opts = self._prep_line_opts(line, opts)
        plot_dict = dict(type='scatter', x=x, y=y, line=line, **opts)
        self.elements.append(plot_dict)
        return plot_dict

    def get_plotter(self, method, **opts):
        if method == 'plot':
            return self.plot
        elif method == 'scatter':
            return self.scatter
        else:
            raise ValueError(f"don't know method {method}")

    def get_facecolor(self):
        return self.opts.get('plot_bgcolor')
    def set_facecolor(self, fg):
        self.opts['plot_bgcolor'] = fg

    def get_padding(self):
        return None

    def legend(self, show=True, **opts):
        self.opts['showlegend'] = show

    def get_graphics_properties(self, obj, property=None):
        raise NotImplementedError(...)
    def set_graphics_properties(self, obj, **props):
        raise NotImplementedError(...)
    def draw_line(self, points, **styles):
        raise NotImplementedError(...)
    def draw_disk(self, points, radius=None, s=None, **styles):
        raise NotImplementedError(...)
    def draw_rect(self, points, **styles):
        raise NotImplementedError(...)
    def draw_poly(self, points, **styles):
        raise NotImplementedError(...)
    def draw_arrow(self, points, **styles):
        raise NotImplementedError(...)
    def draw_text(self, points, vals, **styles):
        raise NotImplementedError(...)

class PlotlyFigure(GraphicsFigure):
    Axes = PlotlyAxes
    default_display_format = 'png'
    def __init__(self, axes=None, layout=None, display_format=None,
                 width=500,
                 height=500,
                 figsize=None,
                 **opts):
        if axes is None:
            axes = []
        if layout is None:
            layout = {}
        self.layout = layout
        if display_format is None:
            display_format = self.default_display_format
        self.display_format = display_format
        self.opts = self.canonicalize_opts(opts)
        self.width = width
        self.height = height
        if figsize is not None:
            self.set_size_inches(*figsize)
        self.shown = False
        super().__init__(axes=axes)
    def __setitem__(self, key, value):
        self.opts[key] = value
    def __getitem__(self, item):
        return self.opts[item]
    def clear(self, *, backend):
        self.axes = []
    def close(self, *, backend):
        self.clear(backend=backend)
    def create_inset(self, bbox, **kw) -> 'GraphicsAxes':
        raise NotImplementedError(...)
    def create_axes(self, **kw) -> 'GraphicsAxes':
        ax = self.Axes(**kw)
        return self.add_axes(ax)
    @classmethod
    def construct(cls, **kw) -> 'GraphicsFigure':
        return cls(**kw)
    def get_size_inches(self):
        return [self.width/DPI_SCALING, self.height/DPI_SCALING]
    def set_size_inches(self, w, h):
        self.width, self.height = w*DPI_SCALING, h*DPI_SCALING
    def set_extents(self, extents):
        (l, r), (b, t) = extents
        self.layout['margin'] = self.layout.get('margin', {}) | dict(
            l=self.width*l,
            r=(1-r)*self.width,
            t=(1-t)*self.height,
            b=b*self.height
        )
    def get_facecolor(self):
        return self.layout.get('paper_bgcolor')
    def set_facecolor(self, fg):
        self.layout['paper_bgcolor'] = fg

    def savefig(self, file, facecolor=None, **opts):
        return self.to_plotly().savefig(file, facecolor=facecolor, **opts)

    def prep_dict(self):
        elems = []
        axes_layout = self.opts
        for ax in self.axes:
            elems.extend(ax.prep_elems())
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
        fig_dict = {
            'data':elems,
            'layout':layout
        }
        # import pprint
        # pprint.pprint(fig_dict)
        # raise Exception(...)
        return fig_dict
    def to_plotly(self):
        import plotly.graph_objects as go
        return go.Figure(self.prep_dict())

    split_plot_fragment = True
    embed_mathjax = True
    preload_plotly = True
    mathjax_cdn = "https://cdn.jsdelivr.net/npm/mathjax@4/tex-svg.js"
    plotly_cdn = "https://cdn.plot.ly/plotly-3.4.0.min.js"
    def get_core_body(self, html):
        return html.split("<body>")[1].rsplit("</body>")[0].strip()
    def set_plotly_script_id(self, html, id):
        return f"""<script type="text/javascript" id="{id}">""".join(html.rsplit("""<script type="text/javascript">""", 1))
    def configure_mathjax(self, html, id):
        plotly_tag = f"""<script type="text/javascript" id="{id}">"""
        mathjax_load_script = """
        if (window.MathJax && window.MathJax.Hub && window.MathJax.Hub.Config) {
            // window.MathJax.Hub.Config({SVG: {font: "STIX-Web"}});
            window.PlotlyConfig = {MathJaxConfig: 'local'};
        }
        """
        mathjax_config = f"""<script src="{self.mathjax_cdn}" onload='function(){{
        {mathjax_load_script}
        }}()'>
        </script>"""
        return html.replace(
            plotly_tag,
            f"""{mathjax_config}\n{plotly_tag}"""
        )
    def postprocess_plotly_html(self, html):
        id = 'plotly-plot-' + str(uuid.uuid4())[:6]
        html = self.set_plotly_script_id(html, id)
        if self.split_plot_fragment:
            html = self.get_core_body(html)
        if self.embed_mathjax:
            html = self.configure_mathjax(html, id)
        if self.preload_plotly:
            # tag_pos = html.index(f"""<script type="text/javascript" id="{id}">""")
            html = html.replace(
                f"""<script type="text/javascript" id="{id}">""",
                f"""<script src="{self.plotly_cdn}" charset="utf-8" id="{id}" onload='(function(){{""",
                1
            )
            # replace from end, should replace with version that starts from the plotly tag
            html = "})()'></script>".join(html.rsplit("</script>", 1))
        return html
    def to_html(self):
        # print(fig)
        buf = io.StringIO()
        self.to_plotly().write_html(buf, include_plotlyjs=False)
        buf.seek(0)
        html = buf.read()
        return self.postprocess_plotly_html(html)
    def to_svg(self):
        buf = io.StringIO()
        self.to_plotly().savefig(buf, format='svg')
        buf.seek(0)
        return buf.read()
    def to_widget(self, format=None, autoclose=True):
        from .. import Jupyter as interactive
        widg = interactive.JHTML.HTML.RawHTML(self.to_html())
        return widg
    def animate_frames(self, frames, **animation_opts):
        raise NotImplementedError(...)
class PlotlyBackend(GraphicsBackend):
    Figure = PlotlyFigure
    def create_figure(self, *args, template=None, **kwargs):
        if template is None:
            template, others = self.ThemeContextManager.current_theme()
            kwargs = others | kwargs
        fig = self.Figure(*args, template=dict(layout=template), **kwargs)
        ax = fig.create_axes()
        return fig, ax

    @classmethod
    def prep_color(cls, v):
        v, padding = ColorPalette.parse_color_string(v, return_padding=True)
        return ColorPalette.rgb_code(v, padding)

    property_mapping = {
        'labelsize':'fontsize'
    }
    axes_props = {'xtick':'xaxis', 'ytick':'yaxis'}
    unthemed_props = {'aspect_ratio'}
    @classmethod
    def remap_property(cls, name, value, context=None):
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
            return {
                'margin': {
                    'l':value,
                    'r':value,
                    'b':value,
                    't':value
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
            # theme_dict = {}
            # for k, v in theme_opts.items():
            #     if isinstance(v, dict):
            #         for sk, sv in v.items():
            #             if isinstance(sv, dict):
            #                 sv = cycler(**sv)
            #             theme_dict[k + '.' + sk] = sv
            #     # else:
            #     #     theme_dict[k] = v
            return theme_parents + [theme_opts]
        def prep_spec(self):
            layout = self.base_theme | {
                'xaxis':self.base_axis_theme,
                'yaxis':self.base_axis_theme
            }
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
            if len(cls.theme_stack) == 0:
                return 'plotly'
            else:
                return cls.theme_stack[-1]

        def __enter__(self):
            self.theme_stack.append(self.prep_spec())

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.theme_stack.pop()

    def show_figure(self, graphics:PlotlyFigure, reshow=None):
        if not graphics.shown:
            widg = graphics.to_widget()
            graphics.shown = True
            return widg.display()

    def get_interactive_status(self) -> 'bool':
        return True
    def disable_interactivity(self):
        ...
    def enable_interactivity(self):
        ...
    def get_available_themes(self):
        return []

class GraphicsRegionAxes(GraphicsAxes):
    def __init__(self, figure_region):
        self.region = figure_region

    @staticmethod
    def renormalize(pos, og_reg, final_reg=None):
        o_min, o_max = og_reg
        pos = (pos - o_min) / (o_max - o_min)
        if final_reg is not None:
            F_min, F_max = final_reg
            pos = pos * (F_max - F_min) + F_min
        return pos

    def normalize_positions(self, pos):
        ndim = pos.shape[-1]

        x = self.renormalize(pos[..., 0], self.get_xlim(), self.region[0])
        y = self.renormalize(pos[..., 1], self.get_ylim(), self.region[1])
        if ndim == 2:
            z = self.renormalize(pos[..., 2], self.get_zlim(), self.region[2])
            crds = [x, y, z]
        else:
            crds = [x, y]
        return np.moveaxis(np.array(crds), 0, -1)

class VTKAxes(GraphicsRegionAxes):

    def __init__(self, figure_region, figure: vtk.VTKWindow):
        self.obj = figure
        self.objs = []
        self._plot_label = None
        super().__init__(figure_region)

    @classmethod
    def canonicalize_opts(cls, opts):
        return opts

    def remove(self, *, backend):
        self.obj.close()

    def clear(self, *, backend):
        for o in self.objs:
            self.obj.remove_object(o)

    def get_plotter(self, method):
        raise NotImplementedError(f"plotter for {method} not implemented")

    def get_plot_label(self):
        return self.obj.get_title()
        # return self._plot_label

    def set_plot_label(self, val, **style):
        return self.obj.set_title(val)
        # x_min, x_max = self.region[0]
        # y_min, y_max = self.region[1]
        # pos = self.renormalize(np.array([(x_max+x_min)/2, (y_max+y_min)/2, 0]))
        # self.obj.draw_text(val, )

    def get_style_list(self):
        raise NotImplementedError("style list cyclers not supported")
    def set_style_list(self, props):
        raise NotImplementedError("style list cyclers not supported")

    def get_frame_visible(self):
        raise NotImplementedError("get_frame_visible")

    def set_frame_visible(self, frame_spec):
        raise NotImplementedError("set_frame_visible")

    def get_frame_style(self):
        raise NotImplementedError("get_frame_style")

    def set_frame_style(self, frame_spec):
        raise NotImplementedError("set_frame_style")

    def get_xlabel(self):
        raise NotImplementedError("get_xlabel")

    def set_xlabel(self, val, **style):
        raise NotImplementedError("set_xlabel")

    def get_ylabel(self):
        raise NotImplementedError("get_xlabel")

    def set_ylabel(self, val, **style):
        raise NotImplementedError("set_ylabel")

    def get_xlim(self):
        return self.obj.get_xlim()
    def set_xlim(self, val, **opts):
        return self.obj.set_xlim(val)

    def get_ylim(self):
        return self.obj.get_ylim()
    def set_ylim(self, val, **opts):
        return self.obj.set_ylim(val)

    def get_zlim(self):
        return self.obj.get_zlim()
    def set_zlim(self, val, **opts):
        return self.obj.set_zlim(val)

    def get_xticks(self):
        raise NotImplementedError("get_xticks")
    def set_xticks(self, val, **opts):
        raise NotImplementedError("set_xticks")

    def get_yticks(self):
        raise NotImplementedError("get_yticks")
    def set_yticks(self, val, **opts):
        raise NotImplementedError("set_yticks")

    def get_xtick_style(self):
        raise NotImplementedError("get_xtick_style")
    def set_xtick_style(self, **opts):
        raise NotImplementedError("set_xtick_style")

    def get_ytick_style(self):
        raise NotImplementedError("get_ytick_style")
    def set_ytick_style(self, **opts):
        raise NotImplementedError("set_ytick_style")

    def set_aspect_ratio(self, ar):
        raise NotImplementedError("set_aspect_ratio")

    def get_bbox(self):
        raise NotImplementedError("get_bbox")
        return [self.obj.get_xlim(), self.obj.get_ylim(), self.obj.get_zlim()]
    def set_bbox(self, bbox):
        raise NotImplementedError("set_bbox")

    def get_facecolor(self):
        return self.obj.get_facecolor()
    def set_facecolor(self, fg):
        return self.obj.set_facecolor(fg)

    def get_padding(self):
        raise NotImplementedError("get_padding")

    @abc.abstractmethod
    def draw_line(self, points, **styles):
        ...

    @abc.abstractmethod
    def draw_disk(self, points, **styles):
        ...

    @abc.abstractmethod
    def draw_rect(self, points, **styles):
        ...

    @abc.abstractmethod
    def draw_poly(self, points, **styles):
        ...

    @abc.abstractmethod
    def draw_arrow(self, points, **styles):
        ...

    @abc.abstractmethod
    def draw_text(self, points, vals, **styles):
        ...

    @abc.abstractmethod
    def draw_sphere(self, points, rads, **styles):
        ...

    @abc.abstractmethod
    def animate_frames(self, frames, **animation_opts):
        ...

class VTKFigure(GraphicsFigure):
    Axes = VTKAxes

    def __init__(self, vtk_window: vtk.VTKWindow, **opts):
        self.obj = vtk_window
        super().__init__(**self.canonicalize_opts(opts))

    def create_axes(self, rows, cols, spans, **kw) -> 'GraphicsAxes':
        return self.add_axes(
            self.obj.add_subplot((rows, cols, spans), **kw)
        )

    @abc.abstractmethod
    def create_inset(self, bbox, **kw) -> 'GraphicsAxes':
        raise NotImplementedError(...)

    @abc.abstractmethod
    def clear(self, *, backend):
        self.obj.clear()
        # for obj in ...:


    @abc.abstractmethod
    def close(self, *, backend):
        ...

    def get_bboxes(self):
        return [
            a.get_bbox() for a in self.axes
        ]

    @abc.abstractmethod
    def get_size_inches(self):
        ...

    @abc.abstractmethod
    def set_size_inches(self, w, h):
        ...

    @abc.abstractmethod
    def savefig(self, file, **opts):
        ...

class VTKBackend(GraphicsBackend):
    ...

class VPythonWrapper:
    _vec = None
    @classmethod
    def vpythonify(cls, arg):
        if cls._vec is None:
            cls._vec = vpython.method('vector')
        if isinstance(arg, (list, tuple, np.ndarray)):
            arg = cls._vec(*arg)
        return arg
    @classmethod
    def vpython_color(cls, color):
        if isinstance(color, str):
            color = MPLManager.color_api().to_rgb(color)
        return cls.vpythonify(color)

class VPythonCanvasWrapper(VPythonWrapper):

    def __init__(self, canvas):
        self.canvas = canvas

    def remove(self, *, backend=None):
        self.canvas.delete()
    def clear(self, *, backend=None):
        for obj in self.canvas.objects:
            obj.visible = False

    @property
    def width(self):
        return self.canvas.width
    @width.setter
    def width(self, width):
        self.canvas.width = width

    @property
    def height(self):
        return self.canvas.height
    @height.setter
    def height(self, height):
        self.canvas.height = height

    @property
    def title(self):
        return self.canvas.title
    @title.setter
    def title(self, title):
        self.canvas.title = title

    @property
    def axis(self):
        return self.canvas.axis
    @axis.setter
    def axis(self, axis):
        self.canvas.axis = axis

    @property
    def up(self):
        return self.canvas.up
    @up.setter
    def up(self, up):
        self.canvas.up = up

    @property
    def background(self):
        return self.canvas.background
    @background.setter
    def background(self, background):
        self.canvas.background = self.vpython_color(background)

    def primitive(self, name, *args, color=None, **opts):
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
        return self.primitive('box',
                              pos=left_corner,
                              length=right_corner[0] - left_corner[0],
                              height=right_corner[1] - left_corner[1],
                              width=right_corner[2] - left_corner[2], **styles)

    def curve(self, points, **styles):
        return self.primitive('curve', points, **styles)

    def cylinder(self, start, end, rad, **styles):
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
        return self.primitive('arrow', points, **styles)

    def label(self, pos, text, **styles):
        return self.primitive('label', pos, text **styles)

    def sphere(self, points, rads, **styles):
        return self.primitive('sphere', pos=points, rad=rads, **styles)

class VPythonGraphWrapper(VPythonWrapper):

    def __init__(self, graph):
        self.graph = graph
        self.objs = []

    @property
    def title(self):
        return self.graph.title
    @title.setter
    def title(self, title):
        self.graph.title = title

    @property
    def xtitle(self):
        return self.graph.xtitle
    @xtitle.setter
    def xtitle(self, xtitle):
        self.graph.xtitle = xtitle

    @property
    def ytitle(self):
        return self.graph.ytitle
    @ytitle.setter
    def ytitle(self, ytitle):
        self.graph.ytitle = ytitle

    @property
    def background(self):
        return self.graph.background
    @background.setter
    def background(self, background):
        self.graph.background = self.vpython_color(background)

    @property
    def foreground(self):
        return self.graph.foreground
    @foreground.setter
    def foreground(self, foreground):
        self.graph.foreground = self.vpython_color(foreground)

    @property
    def xmin(self):
        return self.graph.xmin
    @xmin.setter
    def xmin(self, xmin):
        self.graph.xmin = xmin

    @property
    def xmax(self):
        return self.graph.xmax
    @xmax.setter
    def xmax(self, xmax):
        self.graph.xmax = xmax

    @property
    def ymin(self):
        return self.graph.ymin
    @ymin.setter
    def ymin(self, ymin):
        self.graph.ymin = ymin

    @property
    def ymax(self):
        return self.graph.ymax
    @ymax.setter
    def ymax(self, ymax):
        self.graph.ymax = ymax

    @property
    def width(self):
        return self.graph.width
    @width.setter
    def width(self, width):
        self.graph.width = width

    @property
    def height(self):
        return self.graph.height
    @height.setter
    def height(self, height):
        self.graph.height = height

    def remove(self, *, backend=None):
        self.graph.delete()
    def clear(self, *, backend=None):
        for obj in self.graph.objects:
            obj.visible = False

    def plot(self, x, y, color=None, marker_color=None, dot_color=None, **styles):
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
        super().__init__()
        self.graph = graph

    def remove(self, *, backend):
        self.graph.remove(backend=backend)
    def clear(self, *, backend):
        self.graph.clear(backend=backend)

    def get_plotter(self, method):
        raise NotImplementedError(...)

    def get_plot_label(self):
        return self.graph.title
    def set_plot_label(self, val, **style):
        self.graph.title = val

    def get_style_list(self):
        raise NotImplementedError("style list cyclers not supported")
    def set_style_list(self, props):
        raise NotImplementedError("style list cyclers not supported")

    def get_frame_visible(self):
        raise NotImplementedError(...)
    def set_frame_visible(self, frame_spec):
        raise NotImplementedError(...)

    def get_frame_style(self):
        raise NotImplementedError(...)
    def set_frame_style(self, frame_spec):
        raise NotImplementedError(...)

    def get_xlabel(self):
        return self.graph.xtitle
    def set_xlabel(self, val, **style):
        self.graph.xtitle = val

    def get_ylabel(self):
        return self.graph.ytitle
    def set_ylabel(self, val, **style):
        self.graph.ytitle = val

    def get_xlim(self):
        return [self.graph.xmin, self.graph.xmax]
    def set_xlim(self, val, **opts):
        self.graph.xmin, self.graph.xmax = val

    def get_ylim(self):
        return [self.graph.ymin, self.graph.ymax]
    def set_ylim(self, val, **opts):
        self.graph.ymin, self.graph.ymax = val

    def get_xticks(self):
        raise NotImplementedError(...)
    def set_xticks(self, val, **opts):
        raise NotImplementedError(...)

    def get_yticks(self):
        raise NotImplementedError(...)
    def set_yticks(self, val, **opts):
        raise NotImplementedError(...)

    def get_xtick_style(self):
        raise NotImplementedError(...)
    def set_xtick_style(self, **opts):
        raise NotImplementedError(...)

    def get_ytick_style(self):
        raise NotImplementedError(...)
    def set_ytick_style(self, **opts):
        raise NotImplementedError(...)

    def set_aspect_ratio(self, ar):
        raise NotImplementedError(...)

    def get_bbox(self):
        raise NotImplementedError(...)
    def set_bbox(self, bbox):
        raise NotImplementedError(...)

    def get_facecolor(self):
        return self.graph.background
    def set_facecolor(self, fg):
        self.graph.background = fg

    def get_padding(self):
        raise NotImplementedError(...)

    def draw_line(self, points, **styles):
        return self.graph.plot(*np.asanyarray(points).T, **styles)

    def draw_disk(self, points, color=None, edge_color=None, radius=1,
                  edgecolors=None,
                  s=None, **styles):
        if edgecolors is None:
            if edge_color is not None:
                edgecolors = edge_color
            else:
                edgecolors=[[0.] * 3 + [.3]]
        if s is None:
            s = (10 * radius) ** 2
        return self.graph.scatter(*np.asanyarray(points).T, s=s, edgecolors=edgecolors, **styles)

    def draw_rect(self, points, **styles):
        raise NotImplementedError("too annoying")

    def draw_poly(self, points, **styles):
        raise NotImplementedError("too annoying")

    def draw_arrow(self, points, color=None, **styles):
        raise NotImplementedError("too annoying")

    def draw_text(self, points, vals, color=None, **styles):
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
        raise NotImplementedError("too annoying")
        # return vpython.sphere(points, rads, color=self.vpython_color(color), canvas=self.canvas, **styles)

    def animate_frames(self, frames, **animation_opts):
        raise NotImplementedError("not sure how to animate vpython")

class VPythonFigure(GraphicsFigure):
    Axes = VPythonAxes

    _refs = set()
    def __init__(self, vpython_graph:VPythonGraphWrapper, **opts):
        if vpython_graph in self._refs: raise ValueError(...)
        self._refs.add(vpython_graph)
        self.graph = vpython_graph
        super().__init__(**self.canonicalize_opts(opts))
    @classmethod
    def construct(cls, **kw) -> 'VPythonFigure':
        return cls(vpython.graph(**kw))
    def create_axes(self, rows=1, cols=1, spans=1, **kw) -> 'GraphicsAxes':
        if (rows, cols, spans) != (1, 1, 1):
            raise NotImplementedError("can't create subcanvases")
        return self.add_axes(self.graph)
    def create_inset(self, bbox, **kw) -> 'GraphicsAxes':
        raise NotImplementedError(...)
    def clear(self, *, backend):
        self.graph.clear()
    def close(self, *, backend):
        self.graph.remove()

    def get_size_inches(self):
        return [self.graph.width//72, self.graph.height//72]
    def set_size_inches(self, w, h):
        self.graph.width, self.graph.height = w*72, h*72

    def get_facecolor(self):
        return self.graph.background
    def set_facecolor(self, fg):
        self.graph.background = fg

    def savefig(self, file, **opts):
        raise NotImplementedError("too annoying")

class VPythonBackend(GraphicsBackend):
    Figure = VPythonFigure
    def create_figure(self, *args, **kwargs):
        figure = self.Figure.construct(**kwargs)
        axes = self.Figure.create_axes()
        return figure, axes

    class ThemeContextManager(GraphicsBackend.ThemeContextManager):
        theme_stack = []

        @classmethod
        def canonicalize_theme_opts(self, theme_parents, theme_spec):
            return []
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            ...

    def show_figure(self, graphics, reshow=None):
        ...

    def get_interactive_status(self) -> 'bool':
        return True
    def disable_interactivity(self):
        raise NotImplementedError("not possible")
    def enable_interactivity(self):
        ...
    def get_available_themes(self):
        return []

class VPythonAxes3D(GraphicsAxes3D):
    def __init__(self, canvas:VPythonCanvasWrapper):
        super().__init__()
        self.canvas = canvas

    def remove(self, *, backend):
        self.canvas.remove(backend=backend)
    def clear(self, *, backend):
        self.canvas.clear(backend=backend)

    def get_plotter(self, method):
        raise NotImplementedError(...)

    def get_plot_label(self):
        return self.canvas.title
    def set_plot_label(self, val, **style):
        self.canvas.title = val

    def get_style_list(self):
        raise NotImplementedError("style list cyclers not supported")
    def set_style_list(self, props):
        raise NotImplementedError("style list cyclers not supported")

    def get_frame_visible(self):
        raise NotImplementedError(...)
    def set_frame_visible(self, frame_spec):
        ...
        # raise NotImplementedError(...)

    def get_frame_style(self):
        raise NotImplementedError(...)
    def set_frame_style(self, frame_spec):
        ...
        # raise NotImplementedError(...)

    def get_xlabel(self):
        raise NotImplementedError(...)
    def set_xlabel(self, val, **style):
        ...
        # raise NotImplementedError(...)

    def get_ylabel(self):
        raise NotImplementedError(...)
    def set_ylabel(self, val, **style):
        ...
        # raise NotImplementedError(...)

    def get_xlim(self):
        raise NotImplementedError(...)
    def set_xlim(self, val, **opts):
        ...
        # raise NotImplementedError(...)

    def get_ylim(self):
        raise NotImplementedError(...)
    def set_ylim(self, val, **opts):
        ...
        # raise NotImplementedError(...)

    def get_zlim(self):
        raise NotImplementedError(...)
    def set_zlim(self, val, **opts):
        ...
        # raise NotImplementedError(...)

    def get_xticks(self):
        return []
    def set_xticks(self, val, **opts):
        ...
        # raise NotImplementedError(...)

    def get_yticks(self):
        return []
    def set_yticks(self, val, **opts):
        ...
        # raise NotImplementedError(...)

    def get_zticks(self):
        return []
    def set_zticks(self, val, **opts):
        ...
        # raise NotImplementedError(...)

    def get_xtick_style(self):
        return {}
    def set_xtick_style(self, **opts):
        ...
        # raise NotImplementedError(...)

    def get_ytick_style(self):
        return {}
    def set_ytick_style(self, **opts):
        ...
        # raise NotImplementedError(...)

    def get_ztick_style(self):
        return {}
    def set_ztick_style(self, **opts):
        ...
        # raise NotImplementedError(...)

    def set_aspect_ratio(self, ar):
        ...
        # raise NotImplementedError(...)

    def get_bbox(self):
        raise NotImplementedError(...)
    def set_bbox(self, bbox):
        raise NotImplementedError(...)

    def get_facecolor(self):
        return self.canvas.background
    def set_facecolor(self, fg):
        self.canvas.background = fg

    def get_padding(self):
        raise NotImplementedError(...)

    def draw_line(self, points, **styles):
        return self.canvas.curve(points, **styles)

    def draw_disk(self, points, **styles):
        raise NotImplementedError("2D")

    def draw_rect(self, points, **styles):
        raise NotImplementedError("2D")

    def draw_poly(self, points, **styles):
        raise NotImplementedError("2D")

    def draw_arrow(self, points, **styles):
        return self.canvas.arrow(points, **styles)

    def draw_text(self, points, vals, **styles):
        pts = np.asanyarray(points)
        if pts.ndim == 1:
            return self.canvas.label(pts, vals, **styles)
        else:
            return [
                self.canvas.label(pt, t, **styles)
                for pt, t in zip(pts, vals)
            ]

    def draw_sphere(self, points, rads, **styles):
        return self.canvas.sphere(points, rads, **styles)

    def draw_cylinder(self, start, end, rad, **styles):
        return self.canvas.cylinder(start, end, rad, **styles)

    def draw_primitive(self, name, *args, **kwargs):
        return self.canvas.primitive(name, *args, **kwargs)

class VPythonFigure3D(GraphicsFigure):
    Axes = VPythonAxes3D

    _refs = set()
    def __init__(self, vpython_canvas:VPythonCanvasWrapper, **opts):
        if isinstance(vpython_canvas, VPythonCanvasWrapper):
            vpython_canvas = vpython_canvas.canvas
        if vpython_canvas in self._refs: raise ValueError(...)
        self._refs.add(vpython_canvas)
        self.canvas = VPythonCanvasWrapper(vpython_canvas)
        super().__init__(**self.canonicalize_opts(opts))
    @classmethod
    def construct(cls, **kw) -> 'GraphicsFigure':
        return cls(vpython.method('canvas')(**kw))
    def create_axes(self, rows=1, cols=1, spans=1, **kw) -> 'GraphicsAxes':
        if (rows, cols, spans) != (1, 1, 1):
            raise NotImplementedError("can't create subcanvases")
        return self.add_axes(self.canvas)
    def create_inset(self, bbox, **kw) -> 'GraphicsAxes':
        raise NotImplementedError(...)
    def clear(self, *, backend):
        self.canvas.clear()
    def close(self, *, backend):
        self.canvas.remove()
    def get_size_inches(self):
        return [self.canvas.width//72, self.canvas.height//72]
    def set_size_inches(self, w, h):
        self.canvas.width, self.canvas.height = w*72, h*72
    def set_extents(self, extents):
        ...
    def get_facecolor(self):
        return self.canvas.background
    def set_facecolor(self, fg):
        self.canvas.background = fg
    def savefig(self, file, **opts):
        raise NotImplementedError("too annoying")

class VPythonBackend3D(GraphicsBackend):
    Figure = VPythonFigure3D
    def create_figure(self, *args, **kwargs):
        figure = self.Figure.construct(**kwargs)
        axes = figure.create_axes()
        return figure, axes

    class ThemeContextManager(VPythonBackend.ThemeContextManager):
        ...

    def show_figure(self, graphics, reshow=None):
        ...

    def get_interactive_status(self) -> 'bool':
        return True
    def disable_interactivity(self):
        ...
    def enable_interactivity(self):
        ...
    def get_available_themes(self):
        return []

class X3DAxes(GraphicsAxes3D):
    def __init__(self, *children, title=None, background=None, include_mathjax=None, **opts):
        super().__init__()
        self.children = list(children)
        self.title = title
        self.background = background
        self.opts = opts
        self.include_mathjax = include_mathjax
        self.onloads = []

    @classmethod
    def canonicalize_opts(cls, opts):
        return opts

    def remove(self, *, backend):
        self.children = []
        self.title = ""
        self.background = "white"

    def clear(self, *, backend):
        self.children = []
        self.title = ""
        self.background = "white"

    def get_plotter(self, method):
        ...

    def get_plot_label(self):
        return self.title
    def set_plot_label(self, val, **style):
        self.title = val

    def get_style_list(self):
        raise NotImplementedError("style list cyclers not supported")
    def set_style_list(self, props):
        raise NotImplementedError("style list cyclers not supported")

    def get_frame_visible(self):
        raise NotImplementedError(...)
    def set_frame_visible(self, frame_spec):
        ...
        # raise NotImplementedError(...)

    def get_frame_style(self):
        raise NotImplementedError(...)
    def set_frame_style(self, frame_spec):
        ...
        # raise NotImplementedError(...)

    def get_xlabel(self):
        raise NotImplementedError(...)
    def set_xlabel(self, val, **style):
        ...

    def get_ylabel(self):
        raise NotImplementedError(...)
    def set_ylabel(self, val, **style):
        ...

    def get_xlim(self):
        raise NotImplementedError(...)
    def set_xlim(self, val, **opts):
        ...

    def get_ylim(self):
        raise NotImplementedError(...)
    def set_ylim(self, val, **opts):
        ...

    def get_zlim(self):
        raise NotImplementedError(...)
    def set_zlim(self, val, **opts):
        ...

    def get_xticks(self):
        return []
    def set_xticks(self, val, **opts):
        ...

    def get_yticks(self):
        return []
    def set_yticks(self, val, **opts):
        ...

    def get_zticks(self):
        return []
    def set_zticks(self, val, **opts):
        ...

    def get_xtick_style(self):
        return {}
    def set_xtick_style(self, **opts):
        ...

    def get_ytick_style(self):
        return {}
    def set_ytick_style(self, **opts):
        ...

    def get_ztick_style(self):
        return {}
    def set_ztick_style(self, **opts):
        ...

    def set_aspect_ratio(self, ar):
        ...

    def get_bbox(self):
        raise NotImplementedError(...)
    def set_bbox(self, bbox):
        raise NotImplementedError(...)

    def get_facecolor(self):
        return self.background
    def set_facecolor(self, fg):
        self.background = fg

    def get_padding(self):
        raise NotImplementedError(...)

    def get_view_settings(self):
        return self.opts.get('viewpoint', {})
    def set_view_settings(self, **values):
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
                                        **(styles | dict(color=line_color))
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
        from ..Jupyter.JHTML import CSS
        if font_style is None:
            font_style = {}
        fs = self.default_texture_font | font_style
        fs = {self.font_style_remapping.get(k, k):v for k,v in fs.items()}
        fs = CSS(f"text", **fs).tostring()
        lines = text.splitlines()
        w = resolution * max(len(t) for t in lines)
        vh = 20 + 10 * len(lines)
        return re.sub("\s+", " ", f"""
<svg version="1.1" viewBox="0 0 100 {vh}" width="{w}" height="auto" id='{id}-svg' xmlns="http://www.w3.org/2000/svg">
  <style>{fs}</style>
  <text 
    x="0" y="10" 
    textLength="90" 
    lengthAdjust="spacingAndGlyphs">""") + text + "</text></svg>"
    def mathjax_load_script(self, text, id, resolution_upscaling=10, font_style=None):
        from ..Jupyter.JHTML import CSS
        if font_style is None:
            font_style = {}
        fs = self.default_texture_font | font_style
        # fs = {self.font_style_remapping.get(k, k):v for k,v in fs.items()}
        fs = CSS(**fs).tostring()
        return re.sub("\s+", " ", f"""(function() {{
    let textureNode = document.getElementById('{id}-appearance-texture');
    if (textureNode??null !== null) {{
      MathJax_3.tex2svgPromise('""") + "\\\\text{" + text.replace("\\", "") + re.sub("\s+", " ", """}', {display: true}).then((textWrapper) => {
          MathJax_3.tex2svgPromise('""") + text + re.sub("\s+", " ", f"""', {{display: true}})
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
        text = text.strip()
        num_dollar = text.count("$")
        return num_dollar == 2 and text[0] == "$" and text[-1] == "$"
    def draw_text(self, points, vals, endpoint=None, allow_mathjax=True, line_height=10, char_width=None, char_width_scaling=1/30, font_style=None, **styles):
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
            text = [x3d.X3DText(points, text=vals, font_style=font_style, **styles)]
        self.children.extend(text)
        return text

    @classmethod
    def prep_uv(cls, uv_axes, normal=None, uv_sign=None, rotation=None, angle=None):
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

    def draw_rect(self,
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
        points = np.asanyarray(points)
        if glow is None: glow = color
        rects = x3d.X3DPointSet(points, glow=glow, **styles)
        self.children.append(rects)

        return rects
    def draw_triangle(self, points, indices=None, **styles):
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
        raise NotImplementedError("2D")

    def draw_sphere(self, centers, rads, **styles):
        spheres = x3d.X3DSphere(centers, radius=rads, **styles)
        self.children.append(spheres)

        return spheres

    def draw_cylinder(self, starts, ends, rads, capped=False, **styles):
        if capped:
            cyls = x3d.X3DCappedCylinder(starts, ends, radius=rads, **styles)
        else:
            cyls = x3d.X3DCylinder(starts, ends, radius=rads, **styles)
        self.children.append(cyls)

        return cyls
    def draw_box(self, start, end, **opts):
        box = x3d.X3DBox(start, end, **opts)
        self.children.append(box)
        return box
    def prep_opts(self):
        return dict(
            self.opts,
            background=self.background,
            title=self.title
        )
    def to_x3d(self):
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
        self.opts[key] = value
    def __getitem__(self, item):
        return self.opts[item]

    def clear(self, *, backend):
        self.axes = []

    def close(self, *, backend):
        self.clear(backend=backend)

    def create_inset(self, bbox, **kw) -> 'GraphicsAxes':
        raise NotImplementedError("not possible")

    def create_axes(self, rows=1, cols=1, spans=1, **kw) -> 'GraphicsAxes':
        if (rows, cols, spans) != (1, 1, 1):
            raise NotImplementedError("can't create subcanvases")
        return self.add_axes(self.Axes(**kw))

    @classmethod
    def construct(cls, **kw) -> 'GraphicsFigure':
        return cls(**kw)

    def get_size_inches(self):
        return [self.width/DPI_SCALING, self.height/DPI_SCALING]
    def set_size_inches(self, w, h):
        self.width, self.height = w*DPI_SCALING, h*DPI_SCALING
    def set_extents(self, extents):
        ...
    def get_facecolor(self):
        return self.background
    def set_facecolor(self, fg):
        self.background = fg
    def savefig(self, file, format=None, **opts):
        return self.to_x3d(**opts).dump(file)
    def prep_opts(self):
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
        return self.to_x3d(**opts).to_widget()
    def to_html(self):
        return self.to_widget().tostring()

    def animate_frames(self, frames: list['X3DAxes'], mode=None, **animation_opts):
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
    def create_figure(self, *args, **kwargs):
        figure = self.Figure.construct(**kwargs)
        axes = figure.create_axes()
        return figure, axes

    class ThemeContextManager(GraphicsBackend.ThemeContextManager):
        theme_stack = []

        @classmethod
        def canonicalize_theme_opts(self, theme_parents, theme_spec):
            return []

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            ...

    def show_figure(self, graphics:X3DFigure, reshow=None):
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
        return True
    def disable_interactivity(self):
        ...
    def enable_interactivity(self):
        ...
    def get_available_themes(self):
        return []

class SceneJSONAxes(GraphicsAxes3D):
    def __init__(self, *children, title=None, background=None, **opts):
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
        return opts

    def remove(self, *, backend):
        self.children = []
        self.title = ""
        self.background = "white"

    def clear(self, *, backend):
        self.children = []
        self.title = ""
        self.background = "white"

    def get_plotter(self, method):
        ...

    def get_plot_label(self):
        return self.title
    def set_plot_label(self, val, **style):
        self.title = val

    def get_style_list(self):
        raise NotImplementedError("style list cyclers not supported")
    def set_style_list(self, props):
        raise NotImplementedError("style list cyclers not supported")

    def get_frame_visible(self):
        raise NotImplementedError(...)
    def set_frame_visible(self, frame_spec):
        ...
        # raise NotImplementedError(...)

    def get_frame_style(self):
        raise NotImplementedError(...)
    def set_frame_style(self, frame_spec):
        ...
        # raise NotImplementedError(...)

    def get_xlabel(self):
        raise NotImplementedError(...)
    def set_xlabel(self, val, **style):
        ...

    def get_ylabel(self):
        raise NotImplementedError(...)
    def set_ylabel(self, val, **style):
        ...

    def get_xlim(self):
        raise NotImplementedError(...)
    def set_xlim(self, val, **opts):
        ...

    def get_ylim(self):
        raise NotImplementedError(...)
    def set_ylim(self, val, **opts):
        ...

    def get_zlim(self):
        raise NotImplementedError(...)
    def set_zlim(self, val, **opts):
        ...

    def get_xticks(self):
        return []
    def set_xticks(self, val, **opts):
        ...

    def get_yticks(self):
        return []
    def set_yticks(self, val, **opts):
        ...

    def get_zticks(self):
        return []
    def set_zticks(self, val, **opts):
        ...

    def get_xtick_style(self):
        return {}
    def set_xtick_style(self, **opts):
        ...

    def get_ytick_style(self):
        return {}
    def set_ytick_style(self, **opts):
        ...

    def get_ztick_style(self):
        return {}
    def set_ztick_style(self, **opts):
        ...

    def set_aspect_ratio(self, ar):
        ...

    def get_bbox(self):
        raise NotImplementedError(...)
    def set_bbox(self, bbox):
        raise NotImplementedError(...)

    def get_facecolor(self):
        return self.background
    def set_facecolor(self, fg):
        self.background = fg

    def get_padding(self):
        raise NotImplementedError(...)

    def get_view_settings(self):
        return self.opts.get('viewpoint', {})
    def set_view_settings(self, **values):
        new_opts = {
            k:v for k,v in dict(self.opts.get('viewpoint', {}), **values).items()
            if v is not None
        }
        if len(new_opts) == 0 and 'viewpoint' in self.opts:
            del self.opts['viewpoint']
        else:
            self.opts['viewpoint'] = new_opts

    def draw_line(self, points, **styles):
        points = np.asanyarray(points)
        if points.shape[-1] == 3:
            self.mode = '3d'
        else:
            self.mode = '2d'
        line_set = sceneJSON.Line(points=points.tolist(), mode=self.mode, **styles)
        self.children.append(line_set)

        return line_set

    def draw_disk(self, points, rads=1, **styles):
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
        points = np.asanyarray(points)
        if points.shape[-1] == 3:
            self.mode = '3d'
        else:
            self.mode = '2d'
        arrows = sceneJSON.Arrow(points=points.tolist(), radius=radius, mode=self.mode, **styles)
        self.children.append(arrows)
        return arrows

    def draw_text(self, points, vals, **styles):
        points = np.asanyarray(points)
        if points.shape[-1] == 3:
            self.mode = '3d'
        else:
            self.mode = '2d'
        text = sceneJSON.Text(centers=points.tolist(), text=vals, mode=self.mode, **styles)
        self.children.append(text)
        return text

    def draw_rect(self, points, **styles):
        points = np.asanyarray(points)
        if points.shape[-1] == 3:
            self.mode = '3d'
        else:
            self.mode = '2d'
        rects = sceneJSON.Rectangle(points=points.tolist(), mode=self.mode, **styles)
        self.children.append(rects)

        return rects

    def draw_poly(self, points, **styles):
        points = np.asanyarray(points)
        if points.shape[-1] == 3:
            self.mode = '3d'
        else:
            self.mode = '2d'
        rects = sceneJSON.Polygon(points=points.tolist(), mode=self.mode, **styles)
        self.children.append(rects)

        return rects

    def draw_sphere(self, centers, rads, **styles):
        centers = np.asanyarray(centers)
        if centers.shape[-1] == 3:
            self.mode = '3d'
        else:
            self.mode = '2d'
        spheres = sceneJSON.Sphere(center=centers.tolist(), radius=rads, mode=self.mode, **styles)
        self.children.append(spheres)

        return spheres

    def draw_cylinder(self, starts, ends, rads, **styles):
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
        self.opts[key] = value
    def __getitem__(self, item):
        return self.opts[item]

    def clear(self, *, backend):
        self.axes = []

    def close(self, *, backend):
        self.clear(backend=backend)

    def create_inset(self, bbox, **kw) -> 'GraphicsAxes':
        raise NotImplementedError("not possible")

    def create_axes(self, rows=1, cols=1, spans=1, **kw) -> 'GraphicsAxes':
        if (rows, cols, spans) != (1, 1, 1):
            raise NotImplementedError("can't create subcanvases")
        return self.add_axes(self.Axes(**kw))

    @classmethod
    def construct(cls, **kw) -> 'GraphicsFigure':
        return cls(**kw)

    def get_size_inches(self):
        return [self.width/DPI_SCALING, self.height/DPI_SCALING]
    def set_size_inches(self, w, h):
        self.width, self.height = w*DPI_SCALING, h*DPI_SCALING
    def set_extents(self, extents):
        ...
    def get_facecolor(self):
        return self.background
    def set_facecolor(self, fg):
        self.background = fg
    def savefig(self, file, format=None, **opts):
        return self.to_json(**opts).dump(file)
    def to_json(self, **opts):
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
    def create_figure(self, *args, **kwargs):
        figure = self.Figure.construct(**kwargs)
        axes = figure.create_axes()
        return figure, axes

    class ThemeContextManager(GraphicsBackend.ThemeContextManager):
        theme_stack = []

        @classmethod
        def canonicalize_theme_opts(self, theme_parents, theme_spec):
            return []

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            ...

    def show_figure(self, graphics:SceneJSONFigure, reshow=None):
        if not graphics.shown:
            graphics.shown = True

            from ..Jupyter import JHTML
            #
            # display = JupyterAPIs.get_display_api()
            return JHTML.Pre(graphics.to_json().tostring(indent=2)).display()
            # return html.display()

    def get_interactive_status(self) -> 'bool':
        return True
    def disable_interactivity(self):
        ...
    def enable_interactivity(self):
        ...
    def get_available_themes(self):
        return []
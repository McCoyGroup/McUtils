"""
Provides Graphics base classes that can be extended upon
"""

import os, weakref, numpy as np, functools

from .Properties import GraphicsPropertyManager, GraphicsPropertyManager3D
from .Styling import Styled, ThemeManager, PlotLegend
from .Backends import GraphicsBackend, GraphicsFigure, GraphicsAxes, DPI_SCALING

from .. import Devutils as dev

__all__ = ["GraphicsBase", "Graphics", "Graphics3D", "GraphicsGrid"]
__reload_hook__ = ['.Properties', ".Styling", ".Backends"]


class GraphicsException(Exception):
    pass

########################################################################################################################
#
#                                               GraphicsBase
#
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
        if fig in cls._figure_mapping:
            return cls._figure_mapping[fig]
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
        if fig in cls._figure_mapping:
            parent = cls._figure_mapping[fig]
            # cls._figure_children[parent].add(graphics)
            cls._figure_children[parent].append(graphics)
        else:
            cls._figure_mapping[fig] = graphics
            cls._figure_children[graphics] = []
    @classmethod
    def remove_figure_mapping(cls, fig):
        """
        **LLM Docstring**

        Drop the registration for a backend figure and its child graphics.

        :param fig: the backend figure
        """
        if fig in cls._figure_mapping:
            parent = cls._figure_mapping[fig]
            del cls._figure_mapping[fig]
            del cls._figure_children[parent]
    @classmethod
    def get_child_graphics(cls, fig):
        """
        **LLM Docstring**

        Return the child `Graphics` objects registered against a backend figure.

        :param fig: the backend figure
        :return: the child graphics
        """
        if fig in cls._figure_mapping:
            parent = cls._figure_mapping[fig]
            return cls._figure_children[parent]

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
        if hasattr(axes, 'figure'):  # ignore GraphicsGrids
            if axes in cls._axes_mapping:
                return cls._axes_mapping[axes]
    @classmethod
    def add_axes_graphics(cls, axes, graphics):
        """
        **LLM Docstring**

        Register a `Graphics` object as the owner of a backend axes (for insets).

        :param axes: the backend axes
        :param graphics: the graphics object to register
        :type graphics: GraphicsBase
        """
        if hasattr(axes, 'figure'):
            if axes in cls._axes_mapping:
                parent = cls._axes_mapping[axes]
                cls._axes_children[parent].append(graphics)
            else:
                cls._axes_mapping[axes] = graphics
                cls._axes_children[graphics] = []
    @classmethod
    def remove_axes_mapping(cls, axes):
        """
        **LLM Docstring**

        Drop the registration for a backend axes and its child graphics.

        :param axes: the backend axes
        """
        if hasattr(axes, 'figure'):
            if axes in cls._axes_mapping:
                parent = cls._axes_mapping[axes]
                del cls._axes_mapping[axes]
                del cls._axes_children[parent]
    @classmethod
    def get_axes_child_graphics(cls, axes):
        """
        **LLM Docstring**

        Return the child `Graphics` objects registered against a backend axes.

        :param axes: the backend axes
        :return: the child graphics
        """
        if hasattr(axes, 'figure'):
            if axes in cls._axes_mapping:
                parent = cls._axes_mapping[axes]
                return cls._axes_children[parent]


class GraphicsBase(metaclass=ABCMeta):
    """
    The base class for all things Graphics
    Defines the common parts of the interface
    """


    opt_keys = {
        'background',
        # 'axes_labels',
        # 'plot_label',
        # 'plot_range',
        # 'plot_legend',
        # 'legend_style',
        # 'ticks',
        # 'ticks_style',
        # 'ticks_label_style',
        # 'axes_bbox',
        # 'scale',
        'padding',
        'spacings',
        # 'aspect_ratio',
        'image_size',
        'event_handlers',
        'animated',
        'epilog'
        'prolog',
        'subplot_kw',
        'theme',
        'annotations'
    }

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
        excl = {k: props[k] for k in props.keys() - filter_set}
        incl = {k: props[k] for k in props.keys() & filter_set}
        return incl, excl

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
        exc = None
        try:
            v = object.__getattribute__(self, '_' + key)  # we overloaded getattr
        except AttributeError as e:
            try:
                v = object.__getattribute__(self._prop_manager, '_' + key)  # we overloaded getattr
            except AttributeError as e:
                exc = e
            else:
                exc = None
        if exc is not None:
            raise exc # from None
        return v

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
        if val is None:
            try:
                v = object.__getattribute__(self, '_'+key) # we overloaded getattr
            except AttributeError as e:
                try:
                    v = object.__getattribute__(self._prop_manager, '_' + key)  # we overloaded getattr
                except AttributeError:
                    if parent is not None:
                        try:
                            v = parent.get_raw_attr(key)
                        except AttributeError:
                            v = None
                    else:
                        v = None
            if v is None and key in self.default_style:
                v = self.default_style[key]
            if v is None and theme is not None and key in theme:
                v = theme[key]
            return v
        else:
            return val

    def _update_copy_opt(self, key, val):
        """
        **LLM Docstring**

        Record an option change in the stored init-options (used so copies reproduce the
        change), unless still inside `__init__` or the value is unchanged.

        :param key: the option name
        :type key: str
        :param val: the new value
        """
        if not self._in_init:
            has_val = False
            if key not in self._init_opts or self._init_opts[key] is None:
                has_val = True
                old = self._get_def_opt(key, None, self.theme)
            elif key in self._init_opts:
                has_val = True
                old = self._init_opts[key]
            else:
                old = None
            if has_val:
                changed = val != old
                if isinstance(changed, np.ndarray):
                    changed = changed.any()
                if changed:
                    self._init_opts[key] = val

    layout_keys = {
        'name',
        'figure',
        'tighten',
        'axes',
        'subplot_kw',
        'parent',
        'image_size',
        'figsize',
        'padding',
        'aspect_ratio',
        'interactive',
        'reshowable',
        'theme',
        'prop_manager',
        'theme_manager',
        'managed',
        # 'inset',
        'event_handlers',
        'animated',
        'prolog',
        'epilog',
        'annotations',
        'backend',
        'backend_options'
    }
    def __init__(self,
                 *args,
                 name=None,
                 figure=None,
                 tighten=False,
                 axes=None,
                 subplot_kw=None,
                 parent=None,
                 image_size=None,
                 padding=None,
                 aspect_ratio=None,
                 interactive=None,
                 reshowable=None,
                 backend='matplotlib',
                 backend_options=None,
                 theme=None,
                 prop_manager=GraphicsPropertyManager,
                 theme_manager=ThemeManager,
                 managed=None,
                 # inset=False,
                 strict=True,
                 # annotations=None,
                 **opts
                 ):
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

        self.name = name

        self._init_opts = dict(opts, # for copying
                               tighten=tighten,
                               axes=axes,
                               subplot_kw=subplot_kw,
                               image_size=image_size,
                               padding=padding,
                               aspect_ratio=aspect_ratio,
                               interactive=interactive,
                               reshowable=reshowable,
                               backend=backend,
                               backend_options=backend_options,
                               theme=theme,
                               prop_manager=prop_manager,
                               theme_manager=theme_manager,
                               managed=managed
                               )
        self._in_init = True

        if subplot_kw is None:
            subplot_kw = {}

        self.interactive = interactive
        self.backend = GraphicsBackend.lookup(backend, backend_options)
        if isinstance(figure, GraphicsBase): parent = figure
        inherit_layout = parent is not None and (axes is None or parent.axes is axes) # check inset
        if inherit_layout: prop_manager = parent._prop_manager

        theme = self._get_def_opt('theme', theme, {})
        self.theme=theme
        self.theme_manager=theme_manager
        # if theme is not None:
        #     theme_dict = theme_manager.resolve_theme(theme)[1]
        # else:
        #     theme_dict = {}

        if managed is None:
            if figure is not None and isinstance(figure, GraphicsBase):
                managed = figure.managed
            else:
                managed = False
        self.managed = managed
        self._inset = None

        with self.theme_manager.from_spec(self.theme, backend=self.backend) as manager:
            theme = manager.current_theme[1]
            interactive = self._get_def_opt('interactive', interactive, theme)
            self.interactive = interactive

            reshowable = self._get_def_opt('reshowable', reshowable, theme)
            self.reshowable = reshowable

            theme_parent = parent if inherit_layout else None
            aspect_ratio = self._get_def_opt('aspect_ratio', aspect_ratio,  theme, theme_parent)
            image_size = self._get_def_opt('image_size', image_size, theme, theme_parent)
            padding = self._get_def_opt('padding', padding, theme, theme_parent)
            if figure is None and image_size is not None and 'figsize' not in subplot_kw:
                try:
                    w, h = image_size
                except TypeError:
                    w = image_size
                    asp = aspect_ratio
                    if asp is None or isinstance(asp, str):
                        asp = 4.8/6.4
                    h = w * asp
                if padding is not None:
                    if dev.is_number(padding):
                        padding = [padding, padding]
                    pw, ph = padding
                    try:
                        pwx, pwy = pw
                    except (TypeError, ValueError):
                        pwx = pwy = pw
                    try:
                        phx, phy = ph
                    except (TypeError, ValueError):
                        phx = phy = ph
                    w += pwx + pwy
                    h += phx + phy
                    image_size = (w, h)
                subplot_kw['figsize'] = (w/DPI_SCALING, h/DPI_SCALING)
        del theme

        self.subplot_kw = subplot_kw
        with self.theme_manager.from_spec(self.theme, backend=self.backend):
            fig, ax = self.initialize_figure_and_axes(figure, axes, *args, **subplot_kw)
        self.figure: GraphicsFigure = fig
        self.axes: GraphicsAxes = ax
        self.figure._called_show = False # for avoiding excess show calls with a custom backend
        if self.inset:
            FigureTreeManager.add_axes_graphics(self.axes, self)
        else:
            FigureTreeManager.add_figure_graphics(self.figure, self)

        if not self.interactive: # TODO: should this really be done here...?
            self.backend.disable_interactivity()

        if isinstance(prop_manager, type):
            prop_manager = prop_manager(self, self.figure, self.axes, managed=managed)
        self._prop_manager = prop_manager
        self._colorbar_axis = None
        with self.theme_manager.from_spec(self.theme, backend=self.backend) as manager:
            self.set_options(padding=padding, aspect_ratio=aspect_ratio, image_size=image_size, strict=strict,
                             theme=manager.current_theme[1],
                             **opts)

        self.event_handler = None
        self._shown = False
        self.animator = None
        self.tighten = tighten

        self._in_init = False

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

        if figure is None:
            figure, axes = self.backend.create_figure(*args, **kw)
        elif isinstance(figure, GraphicsBase) or all(hasattr(figure, h) for h in ['layout_keys']):
            if axes is None:
                axes = figure.axes # type: GraphicsAxes
            figure = figure.figure # type: GraphicsFigure

        self.figure = figure
        self.axes = axes # we set these temporarily to make inset work right
        if self.inset:
            FigureTreeManager.add_axes_graphics(self.axes, self)
        else:
            FigureTreeManager.add_figure_graphics(self.figure, self)

        if axes is None:
            raise NotImplementedError("dealing with just getting a figure object not implemented...")
            # if isinstance(figure, GraphicsBase):
            #
            # if not hasattr(figure, 'create_axes'):
            #     figure = figure.figure
            # if not hasattr(figure, 'axes'):
            #     axes = figure.create_axes(1, 1, 1) # type: GraphicsAxes
            # else:
            #     axes = figure.axes

        return figure, axes

    @property
    def parent(self):
        """
        **LLM Docstring**

        The owning graphics object for this figure/axes (self if this is the parent).

        :return: the parent graphics
        :rtype: GraphicsBase
        """
        if self.inset:
            return FigureTreeManager.resolve_axes_graphics(self.axes)
        else:
            return FigureTreeManager.resolve_figure_graphics(self.figure)
    @property
    def figure_parent(self):
        """
        **LLM Docstring**

        The graphics object that owns this object's backend figure.

        :return: the figure's owner
        :rtype: GraphicsBase
        """
        return FigureTreeManager.resolve_figure_graphics(self.figure)
    @property
    def inset(self):
        """
        **LLM Docstring**

        Whether this graphics object is an inset (its axes differ from the figure
        parent's axes and it isn't managed).

        :return: whether it's an inset
        :rtype: bool
        """
        fp = self.figure_parent
        return not self.managed and fp is not None and (self.axes is not fp.axes)
    @property
    def children(self):
        """
        **LLM Docstring**

        The child graphics registered against this object's figure/axes (or `None` if
        this isn't the parent).

        :return: the child graphics
        """
        if self.parent is self:
            if self.inset:
                return FigureTreeManager.get_axes_child_graphics(self.axes)
            else:
                return FigureTreeManager.get_child_graphics(self.figure)
        else:
            return None

    @property
    def event_handlers(self):
        """
        **LLM Docstring**

        The bound event-handler data, if any.

        :return: the event handlers
        """
        from .Interactive import EventHandler
        h = self.event_handler  # type: EventHandler
        if h is not None:
            h = h.data
        return h

    @property
    def animated(self):
        """
        **LLM Docstring**

        The animation specification for this figure.

        :return: the animation spec
        """
        return self._animated

    def bind_events(self, *handlers, **events):
        """
        **LLM Docstring**

        Bind interactive event handlers to the figure.

        :param handlers: a handlers dict (or handler pairs)
        :param events: additional event-name/handler keyword pairs
        """
        from .Interactive import EventHandler

        if len(handlers) > 0 and isinstance(handlers[0], dict):
            handlers = handlers[0]
        elif len(handlers) == 0 or (len(handlers) > 0 and handlers[0] is not None):
            handlers = dict(handlers)
        if isinstance(handlers, dict):
            handlers = dict(handlers, **events)
            if self.event_handler is None:
                self.event_handler = EventHandler(self, **handlers)
            else:
                self.event_handler.bind(**handlers)

    def create_animation(self, *args, **opts):
        """
        **LLM Docstring**

        Create (and start) an animator for the figure from the given frame
        specification.

        :param args: the animation frames/spec
        :param opts: options for the animator
        """
        from .Interactive import Animator

        if len(args) > 0 and args[0] is not None:
            if self.animator is not None:
                self.animator.stop()
            self.animator = Animator(self, *args, **opts)

    def animate_frames(self, frames, **opts):
        """
        **LLM Docstring**

        Prepare the figure and animate the supplied frames via the backend.

        :param frames: the animation frames
        :param opts: animation options
        :return: the animation
        """
        self.prep_show()
        return self.figure.animate_frames(frames, **opts)

    known_keys = layout_keys
    def _check_opts(self, opts):
        """
        **LLM Docstring**

        Raise if any of the supplied option keys aren't recognized (in `known_keys`).

        :param opts: the options to check
        :type opts: dict
        :raises ValueError: for unknown option keys
        """
        diff = opts.keys() - self.known_keys
        if len(diff) > 0:
            raise ValueError("unknown options for {}: {}".format(
                type(self).__name__, list(diff)
            ))
    def set_options(self,
                    event_handlers=None,
                    animated=None,
                    prolog=None,
                    epilog=None,
                    strict=True,
                    theme=None,
                    **opts
                    ):
        """Sets options for the plot
        :param event_handlers:
        :param animated:
        :param opts:
        :type opts:
        :return:
        :rtype:
        """
        if strict:
            self._check_opts(opts)

        self.bind_events(event_handlers)
        self._animated = animated
        self.create_animation(animated)

        if prolog is not None or not hasattr(self, '_prolog'):
            self._prolog = prolog
            if self._prolog is not None:
                self.prolog = prolog

        if epilog is not None or not hasattr(self, '_epilog'):
            self._epilog = epilog
            if self._epilog is not None:
                self.epilog = epilog

    @property
    def prolog(self):
        """
        **LLM Docstring**

        The prolog graphics primitives drawn before the main content. Setting it records
        the change for copying.

        :return: the prolog primitives
        """
        return self._prolog
    @prolog.setter
    def prolog(self, p):
        """
        **LLM Docstring**

        The prolog graphics primitives drawn before the main content. Setting it records
        the change for copying.

        :return: the prolog primitives
        """
        self._update_copy_opt('prolog', p)
        # might want to clear the elements in the prolog?
        self._prolog = p

    @property
    def epilog(self):
        """
        **LLM Docstring**

        The epilog graphics primitives drawn after the main content. Setting it records
        the change for copying.

        :return: the epilog primitives
        """
        return self._epilog
    @epilog.setter
    def epilog(self, e):
        """
        **LLM Docstring**

        The epilog graphics primitives drawn after the main content. Setting it records
        the change for copying.

        :return: the epilog primitives
        """
        self._update_copy_opt('epilog', e)
        # might want to clear the elements in the epilog?
        self._epilog = e

    @property
    def opts(self):
        """
        **LLM Docstring**

        The current values of the tracked `opt_keys` options, as a dict.

        :return: the options dict
        :rtype: dict
        """
        opt_dict = {}
        for k in self.opt_keys:
            if (
                    k in self.__dict__
                    or hasattr(self._prop_manager, k)
            ):
                opt_dict[k] = getattr(self, k)
            elif (
                    "_"+k in self.__dict__
                    or hasattr(self, "_"+k)
            ):
                opt_dict[k] = getattr(self, "_" + k)
        return opt_dict

    def copy(self, **kwargs):
        """Creates a copy of the object with new axes and a new figure

        :return:
        :rtype:
        """
        return self.change_figure(None, **kwargs)
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
        if unmerged_keys is None:
            unmerged_keys = self.layout_keys
        base = self._init_opts.copy()
        problems = unmerged_keys & base.keys()
        for k in problems & parent_opts.keys():
            del base[k]
        return base
    def change_figure(self, new, *init_args, figs=None, **init_kwargs):
        """Creates a copy of the object with new axes and a new figure

        :return:
        :rtype:
        """
        parent = self.figure_parent
        figs = {} if figs is None else figs
        if parent is self:
            if new is not None and new.figure is self.figure:
                figs[self] = self
                for c in self.children:
                    figs[c] = c
            else:
                # opts = self.get_init_opts(**init_kwargs)
                if self not in figs:
                    figs[self] = self._change_figure(new, *init_args, parent_opts={}, **init_kwargs)
                base = figs[self]
                parent_opts = dict(self._get_init_opts({}), **init_kwargs)
                for c in self.children:
                    if c not in figs:
                        figs[c] = c._change_figure(base, parent_opts=parent_opts)
        else:
            parent.change_figure(new, *init_args, figs=figs, **init_kwargs)
        return figs[self]
    def _get_init_args(self, *init_args):
        """
        **LLM Docstring**

        Return the positional construction arguments to reuse when copying (identity by
        default).

        :param init_args: the supplied positional args
        :return: the positional args
        :rtype: tuple
        """
        return init_args
    def _change_figure(self, new, *init_args, parent_opts=None, **init_kwargs):
        """Creates a copy of the object with new axes and a new figure

        :return:
        :rtype:
        """
        return type(self)(
            *self._get_init_args(*init_args),
            **dict(
                self._get_init_opts(parent_opts),
                figure=new,
                **init_kwargs
            )
        )

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
        with self.theme_manager.from_spec(self.theme, backend=self.backend) as manager:
            theme = manager.current_theme[1]
            self.set_options(
                **(self.opts | dict(theme=theme))
            )  # matplotlib is dumb so it makes sense to just reset these again...
        if self.prolog is not None:
            self._prolog_graphics = [p.plot(self.axes, graphics=self) for p in self.prolog] # not sure this is doing what it should...
        if self.epilog is not None:
            self._epilog_graphics = [e.plot(self.axes, graphics=self) for e in self.epilog]
        if self.tighten:
            self.figure.tight_layout()
        self.figure.prep_show()
        self.axes.prep_show()
        self._shown = True
        return self

    def prep_show(self):
        """
        **LLM Docstring**

        Prepare the whole figure tree (parent and children) for display.

        :return: self
        :rtype: GraphicsBase
        """
        if self.figure_parent is self:
            self._prep_show(parent=True)
            for c in self.children:
                if hasattr(c, '_prep_show'):
                    c._prep_show(parent=False)
                else:
                    c.prep_show()
        else:
            self.figure_parent.prep_show()
        return self
    def show(self, reshow=None):
        """
        **LLM Docstring**

        Display the figure, preparing it first and (temporarily) enabling interactivity
        as needed; makes a copy if the figure was already shown and isn't reshowable.

        :param reshow: force a reshow of an already-shown figure
        :type reshow: bool | None
        :return: the backend's show result
        """
        if reshow or not self._shown:
            self.prep_show()
            if not self.managed:
                ni = not self.interactive
                try:
                    if ni:
                        self.backend.enable_interactivity()
                    self.backend.show_figure(self.figure, reshow=reshow)
                finally:
                    self.interactive = not ni
                    if ni:
                        self.backend.disable_interactivity()
        else:
            if self.reshowable:
                return self.show(reshow=True)
            else:
                # self._shown = False
                return self.copy().show()
                # raise GraphicsException("{}.show can only be called once per object".format(type(self).__name__))

        return self.backend.show_figure(self.figure, reshow=reshow)

    def close(self, force=False):
        """
        **LLM Docstring**

        Close the figure (or remove the inset axes), cleaning up the figure registration
        when this object owns it.

        :param force: close even if this object isn't the registered owner
        :type force: bool
        """
        if (
                force
                or self.figure not in FigureTreeManager._figure_mapping
                or FigureTreeManager.resolve_figure_graphics(self.figure) is self
                or FigureTreeManager.resolve_axes_graphics(self.axes) is self
        ): # parent manages cleanup
            if self.inset:
                # print("removing inset axes: {}".format(self))
                self.backend.remove_axes(self.axes)
            else:
                # print("closing: {}".format(self))
                self.backend.close_figure(self.figure)
                FigureTreeManager.remove_figure_mapping(self.figure)
        # else:
        #     print("close failed: {}".format(self))

    def __del__(self):
        """
        **LLM Docstring**

        Close the figure on garbage collection (ignoring teardown errors).
        """
        try:
            self.close()
        except AttributeError:
            pass

    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation showing the type, name/id, and backing figure.

        :return: the representation
        :rtype: str
        """
        return "{}({}, figure={}<{}>)".format(
            type(self).__name__,
            id(self) if self.name is None else self.name,
            self.figure,
            id(self.figure)
        )

    def clear(self):
        """
        **LLM Docstring**

        Clear the drawn content from the axes.
        """
        self.backend.clear_axes(self.axes)
        # FigureTreeManager.remove_figure_mapping(self.figure)

    _display_locks = set()
    def _ipython_display_(self):
        """
        **LLM Docstring**

        Display the figure in IPython (guarded against re-entrant display calls).
        """
        if self not in self._display_locks:  # don't want to call this over and over...
            self._display_locks.add(self)
            try:
                self.show()
            finally:
                self._display_locks.remove(self)
    def _repr_html_(self):
        """
        **LLM Docstring**

        Return the figure's HTML representation for IPython.

        :return: the HTML
        :rtype: str
        """
        # hacky, but hopefully enough to make it work?
        return self.figure._repr_html_()
    def get_mime_bundle(self):
        """
        **LLM Docstring**

        Return the figure's MIME bundle (HTML or PNG) for rich display.

        :return: the MIME bundle
        :rtype: dict
        """
        return self.figure.get_mime_bundle()

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
        if 'facecolor' not in kw:
            kw['facecolor'] = self.background
        if format is None:
            format = os.path.splitext(where)[1].split('.')[-1]
        self.prep_show()
        if isinstance(where, str) and expanduser:
            where = os.path.expanduser(where)
        return self.figure.savefig(where, format=format, **kw)
    def to_png(self):
        """
        Used by Jupyter and friends to make a version of the image that they can display, hence the extra 'tight_layout' call
        :return:
        :rtype:
        """
        import io
        buf = io.BytesIO()
        self.prep_show()
        self.figure.tight_layout()
        fig = self.figure
        fig.savefig(buf,
                    format='png',
                    facecolor=self.background #-_- stupid MPL
                    )
        buf.seek(0)
        return buf

    def to_widget(self):
        """
        **LLM Docstring**

        Prepare the figure and return it as an interactive backend widget.

        :return: the widget
        """
        self.prep_show()
        self.figure.tight_layout()
        return self.backend.to_widget(self.figure)

    def _repr_png_(self):
        """
        **LLM Docstring**

        Return the figure's PNG bytes for IPython.

        :return: the PNG data
        :rtype: bytes
        """
        return self.to_png().read()

    def create_colorbar_axis(self,
                             figure=None,
                             size=(20, 200),
                             tick_padding=40,
                             origin=None,
                             orientation='vertical',
                             alignment=None
                             ):
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
        fig = self.figure if figure is None else figure
        # if self._colorbar_axis is None:
        # TODO: I'd like to have better control over how much space this colorbar takes in the future
        #   it might be a mistake to make this not percentage based...
        W, H = self.image_size
        if size[0] < 1:
            size = (W * size[0], H * size[1])
        size = (size[0] + tick_padding, size[1])
        if origin is None:
            if orientation == 'vertical':
                origin = (W, H / 2)
            else:
                origin = (W / 2, 0)
        if alignment is None:
            if orientation == 'vertical':
                alignment = (0, .5)
            else:
                alignment = (.5, 0)
        if isinstance(tick_padding, (int, float, np.integer, np.floating)):
            if orientation == 'vertical':
                tick_padding = (tick_padding, 0)
            else:
                tick_padding = (0, tick_padding)
        cur_padding = self.padding
        x_overrun = origin[0] + size[0] - (W + cur_padding[0][0])
        if x_overrun > 5:
            self.padding_right = x_overrun
            new_padding = self.padding
            wpad_old = cur_padding[0][0] + cur_padding[0][1]
            wpad_new = new_padding[0][0] + new_padding[0][1]
            wdiff = wpad_new - wpad_old
        else:
            x_overrun = 0
            wdiff = 0


        y_overrun = origin[1] + size[1] - (H + cur_padding[1][1])
        if y_overrun > 5:
            self.padding_top = y_overrun
            new_padding = self.padding
            wpad_old = cur_padding[1][0] + cur_padding[1][1]
            wpad_new = new_padding[1][0] + new_padding[1][1]
            hdiff = wpad_new - wpad_old
        else:
            y_overrun = 0
            hdiff = 0

        # we need to now shrink the spacing by enough to compensate for this
        # it would be best to mess with the figure sizes themselves, but this is the easier
        # solution for the moment...
        sp = self.spacings
        if sp is not None:
            ws, hs = sp
            nspaces = self.shape[1] - 1
            ws = ws - (wdiff / nspaces)
            ws = max(ws, 0)
            nspaces = self.shape[0] - 1
            hs = hs - (hdiff / nspaces)
            hs = max(hs, 0)
            self.spacings = (ws, hs)
        cbw = (size[0]) / (W + x_overrun)
        tw = tick_padding[0] / (W + x_overrun)
        cbh = (size[1]) / (H + y_overrun)
        th = tick_padding[1] / (H + y_overrun)
        xpos = (origin[0] - alignment[0]*size[0]) / (W + x_overrun)
        ypos = (origin[1] - alignment[1]*size[1]) / (H + x_overrun)  # new_padding[1][0]/H

        bbox = [[xpos, ypos], [xpos + cbw, ypos + cbh]]
        theme = self.theme
        if self.theme is not None:
            with self.theme_manager.from_spec(theme, backend=self.backend):
                axis = fig.create_inset(bbox)
        else:
            axis = fig.create_inset(bbox)
        return axis
    _default_colorbar_size = (20, 200)
    def add_colorbar(self,
                     graphics=None,
                     norm=None,
                     cmap=None,
                     size=None,
                     orientation='vertical',
                     origin=None,
                     tick_padding=40,
                     colorbar_axes=None,
                     cax=None,
                     **kw
                     ):
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
        fig = self.figure  # type: GraphicsBackend.Figure
        ax = self.axes  # type: GraphicsBackend.Figure.Axes

        if size is None:
            if orientation == 'vertical':
                size = self._default_colorbar_size
            else:
                size = (self._default_colorbar_size[1], self._default_colorbar_size[0])

        if cax is not None:
            graphics = cax
        if colorbar_axes is None:
            if self._colorbar_axis is None:
                colorbar_axes = self.create_colorbar_axis(
                    size=size,
                    tick_padding=tick_padding,
                    origin=origin,
                    orientation=orientation
                )
        if self._colorbar_axis is None:
            self._colorbar_axis = colorbar_axes
        if colorbar_axes is not self._colorbar_axis:
            self._colorbar_axis.remove()
            self._colorbar_axis = colorbar_axes

        return fig.create_colorbar(graphics, colorbar_axes,
                                   norm=norm,
                                   cmap=cmap,
                                   orientation=orientation,
                                   **kw)

    axes_params = {"adjustable", "agg_filter", "alpha", "anchor", "animated", "aspect",
                   "autoscale_on", "autoscalex_on", "autoscaley_on", "axes_locator", "axisbelow",
                   "box_aspect", "clip_box", "clip_on", "clip_path", "facecolor",
                   "frame_on", "gid", "in_layout", "label", "navigate",
                   "navigate_mode", "path_effects", "picker", "position",
                   "prop_cycle", "rasterization_zorder", "rasterized", "sketch_params",
                   "snap", "title", "transform", "url", "visible", "xbound",
                   "xlabel", "xlim", "xmargin", "xscale", "xticklabels", "xticks",
                   "ybound", "ylabel", "ylim", "ymargin", "yscale", "yticklabels",
                   "yticks", "zorder"} # not sure what to do with these yet...
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
        if hasattr(bbox, 'get_points'):
            bbox = bbox.get_points()
        ((lx, by), (rx, ty)) = bbox

        if coordinates == 'absolute':
            raise NotImplementedError("can't construct inset axes with absolute coordinates")
        elif coordinates == 'scaled': # scaled to live within the frame
            ((alx, aby), (arx, aty)) = self.axes.bbox.get_points()
            alx = alx + self._axes_padding_offset[0]
            arx = arx + self._axes_padding_offset[0]
            aby = aby + self._axes_padding_offset[1]
            aty = aty + self._axes_padding_offset[1]
            w, h = self.figure_parent.image_size
            # we scale the coordinates to live within the axes screenbox
            sl = alx / w
            sr = arx / w
            sw = (sr - sl)
            sb = aby / h
            st = aty / h
            sh = (st - sb)
            lx = lx * sw + sl
            rx = rx * sw + sl
            by = by * sh + sb
            ty = ty * sh + sb

        if graphics_class is None:
            graphics_class = type(self)
        opts = dict(self.inset_options, **opts)
        # raise Exception(opts, self.axes_keys)
        # ax_par, fig_par = self._split_props_list(opts, self.axes_keys)

        with self.theme_manager.from_spec(self.theme, backend=self.backend):
            ax = self.figure.add_axes([lx, by, rx-lx, ty-by])
        return graphics_class(figure=self, axes=ax, **opts)

########################################################################################################################
#
#                                               Graphics
#
class Graphics(GraphicsBase):

    default_style = dict(
        theme='mccoy',
        image_size=(370, 345),
        interactive=False,
        reshowable=False,
    )

    axes_keys = {
        'plot_label',
        'style_list',
        'plot_legend',
        'legend_style'
        'axes_labels',
        'frame',
        'frame_style',
        'grid',
        'grid_style',
        'plot_range',
        'ticks',
        'ticks_style',
        'ticks_label_style',
        'axes_bbox'
    }
    figure_keys = {
        'scale',
        'aspect_ratio'
        'image_size',
        'padding',
        'spacings',
        'background',
        'colorbar'
    }
    layout_keys = axes_keys | figure_keys | GraphicsBase.layout_keys
    known_keys = layout_keys
    def set_options(self,
                    axes_labels=None,
                    plot_label=None,
                    style_list=None,
                    plot_range=None,
                    plot_legend=None,
                    legend_style=None,
                    frame=None,
                    frame_style=None,
                    grid=None,
                    grid_style=None,
                    ticks=None,
                    scale=None,
                    padding=None,
                    spacings=None,
                    ticks_style=None,
                    ticks_label_style=None,
                    image_size=None,
                    axes_bbox=None,
                    aspect_ratio=None,
                    background=None,
                    colorbar=None,
                    prolog=None,
                    epilog=None,
                    theme=None,
                    **parent_opts
                    ):
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

        super().set_options(prolog=prolog, epilog=epilog, theme=theme, **parent_opts)

        if theme is None:
            theme = {}

        if self is self.parent:
            plot_label_padding = self.get_plot_label_padding(plot_label)
            axes_label_padding = self.get_axes_label_padding(axes_labels)
            padding = self.resolve_default_padding(padding, [plot_label_padding, axes_label_padding],
                                                   theme=theme)
        opts = (
            ('plot_label', plot_label),
            ('style_list', style_list),
            ('plot_legend', plot_legend),
            ('legend_style', legend_style),
            ('axes_labels', axes_labels),
            ('frame', frame),
            ('frame_style', frame_style),
            ('grid', grid),
            ('grid_style', grid_style),
            ('plot_range', plot_range),
            ('ticks', ticks),
            ('ticks_style', ticks_style),
            ('ticks_label_style', ticks_label_style),
            ('scale', scale),
            ('aspect_ratio', aspect_ratio),
            ('image_size', image_size),
            ('axes_bbox', axes_bbox),
            ('padding', padding),
            ('spacings', spacings),
            ('background', background),
            ('colorbar', colorbar)
        )
        for oname, oval in opts:
            oval = self._get_def_opt(oname, oval, theme)
            if oval is not None:
                setattr(self, oname, oval)

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
        p = self.padding_line_height
        if plot_label is None:
            return [[None, None], [None, None]]
        else:
            return [[None, None], [None, p]]
    def get_axes_label_padding(self, axes_labels):
        """
        **LLM Docstring**

        Return the extra padding needed to fit the axis labels (left/bottom padding for
        the y/x labels).

        :param axes_labels: the axis labels (or `None`)
        :return: the `((left, right), (bottom, top))` padding contribution
        :rtype: list
        """
        p = self.padding_line_height
        if axes_labels is None:
            return [[None, None], [None, None]]
        else:
            x,y = axes_labels[:2]
            return [
                [None, None] if y is None or len(y) == 0 else [p, None],
                [None, None] if x is None or len(x) == 0 else [p, None]
            ]

    def resolve_default_padding(self, padding, modifications=None, theme=None):
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
        base_padding = self._get_def_opt('padding', None, theme)
        if padding is None:
            padding = base_padding
            if modifications is not None:
                if padding is None:
                    padding = 0
                if dev.is_number(padding):
                    padding = [[padding, padding], [padding, padding]]
                lr, bt = padding
                if lr is None or dev.is_number(lr):
                    lr = [lr, lr]
                if bt is None or dev.is_number(bt):
                    bt = [bt, bt]
                l, r = lr
                b, t = bt
                for mods in modifications:
                    ((l_m,r_m), (b_m, t_m)) = mods
                    l = l + (l_m if l_m is not None else 0)
                    r = r + (r_m if r_m is not None else 0)
                    b = b + (b_m if b_m is not None else 0)
                    t = t + (t_m if t_m is not None else 0)
                padding = ((l,r), (b, t))
        else:
            if dev.is_number(padding):
                padding = [[padding, padding], [padding, padding]]
            lr, bt = padding
            if lr is None or dev.is_number(lr):
                lr = [lr, lr]
            if bt is None or dev.is_number(bt):
                bt = [bt, bt]
            l,r = lr
            b,t = bt

            ((l_b,r_b), (b_b, t_b)) = base_padding
            l_none = l is None
            if l_none: l = l_b
            r_none = r is None
            if r_none: r = r_b
            b_none = b is None
            if b_none: b = b_b
            t_none = t is None
            if t_none: t = t_b
            if modifications is not None:
                for mods in modifications:
                    ((l_m,r_m), (b_m, t_m)) = mods
                    if l_none:
                        l = l + (l_m if l_m is not None else 0)
                    if r_none:
                        r = r_b + (r_m if r_m is not None else 0)
                    if b_none:
                        b = b_b + (b_m if b_m is not None else 0)
                    if t_none:
                        t = t_b + (t_m if r_m is not None else 0)
            padding = ((l,r), (b, t))

        return padding



    @property
    def artists(self):
        """
        **LLM Docstring**

        The plot's artist objects (empty for the base `Graphics`).

        :return: the artists
        :rtype: list
        """
        return []

    # attaching custom property setters
    @property
    def plot_label(self):
        """
        **LLM Docstring**

        The plot title/label. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the plot label value
        """
        return self._prop_manager.plot_label
    @plot_label.setter
    def plot_label(self, value):
        """
        **LLM Docstring**

        The plot title/label. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the plot label value
        """
        self._update_copy_opt('plot_label', value)
        self._prop_manager.plot_label = value


    @property
    def style_list(self):
        """
        **LLM Docstring**

        The per-series style cycle (shared with the parent). Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the style list value
        """
        return self.parent._prop_manager.style_list
    @style_list.setter
    def style_list(self, value):
        """
        **LLM Docstring**

        The per-series style cycle (shared with the parent). Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the style list value
        """
        self._update_copy_opt('style_list', value)
        self.parent._prop_manager.style_list = value

    @property
    def plot_legend(self):
        """
        **LLM Docstring**

        The plot legend (or legend spec). Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the plot legend value
        """
        return self._prop_manager.plot_legend
    @plot_legend.setter
    def plot_legend(self, value):
        """
        **LLM Docstring**

        The plot legend (or legend spec). Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the plot legend value
        """
        self._update_copy_opt('plot_legend', value)
        self._prop_manager.plot_legend = value

    @property
    def legend_style(self):
        """
        **LLM Docstring**

        The legend styling options. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the legend style value
        """
        return self._prop_manager.legend_style
    @legend_style.setter
    def legend_style(self, value):
        """
        **LLM Docstring**

        The legend styling options. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the legend style value
        """
        self._update_copy_opt('legend_style', value)
        self._prop_manager.legend_style = value

    @property
    def axes_labels(self):
        """
        **LLM Docstring**

        The per-axis labels. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the axes labels value
        """
        return self._prop_manager.axes_labels
    @axes_labels.setter
    def axes_labels(self, value):
        """
        **LLM Docstring**

        The per-axis labels. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the axes labels value
        """
        self._update_copy_opt('axes_labels', value)
        self._prop_manager.axes_labels = value

    @property
    def frame(self):
        """
        **LLM Docstring**

        Which frame (spine) edges are drawn. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the frame value
        """
        return self._prop_manager.frame
    @frame.setter
    def frame(self, value):
        """
        **LLM Docstring**

        Which frame (spine) edges are drawn. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the frame value
        """
        self._update_copy_opt('frame', value)
        self._prop_manager.frame = value

    @property
    def frame_style(self):
        """
        **LLM Docstring**

        The frame styling options. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the frame style value
        """
        return self._prop_manager.frame_style
    @frame_style.setter
    def frame_style(self, value):
        """
        **LLM Docstring**

        The frame styling options. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the frame style value
        """
        self._update_copy_opt('frame_style', value)
        self._prop_manager.frame_style = value

    @property
    def grid(self):
        """
        **LLM Docstring**

        Which frame (spine) edges are drawn. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the frame value
        """
        return self._prop_manager.grid
    @grid.setter
    def grid(self, value):
        """
        **LLM Docstring**

        Which frame (spine) edges are drawn. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the frame value
        """
        self._update_copy_opt('grid', value)
        self._prop_manager.grid = value

    @property
    def grid_style(self):
        """
        **LLM Docstring**

        The frame styling options. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the frame style value
        """
        return self._prop_manager.grid_style
    @grid_style.setter
    def grid_style(self, value):
        """
        **LLM Docstring**

        The frame styling options. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the frame style value
        """
        self._update_copy_opt('grid_style', value)
        self._prop_manager.grid_style = value

    @property
    def plot_range(self):
        """
        **LLM Docstring**

        The plotted data range per axis. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the plot range value
        """
        return self._prop_manager.plot_range
    @plot_range.setter
    def plot_range(self, value):
        """
        **LLM Docstring**

        The plotted data range per axis. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the plot range value
        """
        self._update_copy_opt('plot_range', value)
        self._prop_manager.plot_range = value

    @property
    def ticks(self):
        """
        **LLM Docstring**

        The tick locations/specification. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the ticks value
        """
        return self._prop_manager.ticks
    @ticks.setter
    def ticks(self, value):
        """
        **LLM Docstring**

        The tick locations/specification. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the ticks value
        """
        self._update_copy_opt('ticks', value)
        self._prop_manager.ticks = value

    @property
    def ticks_style(self):
        """
        **LLM Docstring**

        The tick styling options. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the ticks style value
        """
        return self._prop_manager.ticks_style
    @ticks_style.setter
    def ticks_style(self, value):
        """
        **LLM Docstring**

        The tick styling options. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the ticks style value
        """
        self._update_copy_opt('ticks_style', value)
        self._prop_manager.ticks_style = value

    @property
    def ticks_label_style(self):
        """
        **LLM Docstring**

        The tick-label styling options. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the tick-label style value
        """
        return self._prop_manager.ticks_label_style
    @ticks_label_style.setter
    def ticks_label_style(self, value):
        """
        **LLM Docstring**

        The tick-label styling options. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the tick-label style value
        """
        self._update_copy_opt('ticks_label_style', value)
        self._prop_manager.ticks_label_style = value

    @property
    def scale(self):
        """
        **LLM Docstring**

        The axis scaling (e.g. linear/log). Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the scale value
        """
        return self._prop_manager.scale
    @scale.setter
    def scale(self, value):
        """
        **LLM Docstring**

        The axis scaling (e.g. linear/log). Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the scale value
        """
        self._update_copy_opt('scale', value)
        self._prop_manager.scale = value

    @property
    def axes_bbox(self):
        """
        **LLM Docstring**

        The axes bounding box within the figure. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the axes bbox value
        """
        return self._prop_manager.axes_bbox
    @axes_bbox.setter
    def axes_bbox(self, value):
        """
        **LLM Docstring**

        The axes bounding box within the figure. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the axes bbox value
        """
        self._update_copy_opt('axes_bbox', value)
        self._prop_manager.axes_bbox = value

    @property
    def aspect_ratio(self):
        """
        **LLM Docstring**

        The axes aspect ratio. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the aspect ratio value
        """
        return self._prop_manager.aspect_ratio
    @aspect_ratio.setter
    def aspect_ratio(self, value):
        """
        **LLM Docstring**

        The axes aspect ratio. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the aspect ratio value
        """
        self._update_copy_opt('aspect_ratio', value)
        self._prop_manager.aspect_ratio = value

    @property
    def image_size(self):
        """
        **LLM Docstring**

        The figure image size in pixels. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the image size value
        """
        return self._prop_manager.image_size
    @image_size.setter
    def image_size(self, value):
        """
        **LLM Docstring**

        The figure image size in pixels. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the image size value
        """
        self._update_copy_opt('image_size', value)
        self._prop_manager.image_size = value

    @property
    def figure_label(self):
        """
        **LLM Docstring**

        The overall figure label. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the figure label value
        """
        return self._prop_manager.figure_label
    @figure_label.setter
    def figure_label(self, value):
        """
        **LLM Docstring**

        The overall figure label. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the figure label value
        """
        self._update_copy_opt('figure_label', value)
        self._prop_manager.figure_label = value

    @property
    def padding(self):
        """
        **LLM Docstring**

        The figure padding on each side. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the padding value
        """
        return self._prop_manager.padding
    @padding.setter
    def padding(self, value):
        """
        **LLM Docstring**

        The figure padding on each side. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the padding value
        """
        self._update_copy_opt('padding', value)
        self._prop_manager.padding = value
    @property
    def padding_left(self):
        """
        **LLM Docstring**

        The left figure padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the left padding value
        """
        return self._prop_manager.padding_left
    @padding_left.setter
    def padding_left(self, value):
        """
        **LLM Docstring**

        The left figure padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the left padding value
        """
        self._update_copy_opt('padding_left', value)
        self._prop_manager.padding_left = value
    @property
    def padding_right(self):
        """
        **LLM Docstring**

        The right figure padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the right padding value
        """
        return self._prop_manager.padding_right
    @padding_right.setter
    def padding_right(self, value):
        """
        **LLM Docstring**

        The right figure padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the right padding value
        """
        self._update_copy_opt('padding_right', value)
        self._prop_manager.padding_right = value
    @property
    def padding_top(self):
        """
        **LLM Docstring**

        The top figure padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the top padding value
        """
        return self._prop_manager.padding_top
    @padding_top.setter
    def padding_top(self, value):
        """
        **LLM Docstring**

        The top figure padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the top padding value
        """
        self._update_copy_opt('padding_top', value)
        self._prop_manager.padding_top = value
    @property
    def padding_bottom(self):
        """
        **LLM Docstring**

        The bottom figure padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the bottom padding value
        """
        return self._prop_manager.padding_bottom
    @padding_bottom.setter
    def padding_bottom(self, value):
        """
        **LLM Docstring**

        The bottom figure padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the bottom padding value
        """
        self._update_copy_opt('padding_bottom', value)
        self._prop_manager.padding_bottom = value

    @property
    def spacings(self):
        """
        **LLM Docstring**

        The inter-panel spacings. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the spacings value
        """
        return self._prop_manager.spacings
    @spacings.setter
    def spacings(self, value):
        """
        **LLM Docstring**

        The inter-panel spacings. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the spacings value
        """
        self._update_copy_opt('spacings', value)
        self._prop_manager.spacings = value

    @property
    def background(self):
        """
        **LLM Docstring**

        The figure background color. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the background value
        """
        return self._prop_manager.background
    @background.setter
    def background(self, value):
        """
        **LLM Docstring**

        The figure background color. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the background value
        """
        self._update_copy_opt('background', value)
        self._prop_manager.background = value

    @property
    def colorbar(self):
        """
        **LLM Docstring**

        The colorbar specification. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the colorbar value
        """
        return self._prop_manager.colorbar
    @colorbar.setter
    def colorbar(self, value):
        """
        **LLM Docstring**

        The colorbar specification. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the colorbar value
        """
        self._update_copy_opt('colorbar', value)
        self._prop_manager.colorbar = value

    def _prep_show(self, parent=False):
        """
        **LLM Docstring**

        Prepare the plot for display, additionally drawing the legend and re-applying the
        ticks when this is the parent figure.

        :param parent: whether this is the parent of the figure
        :type parent: bool
        """
        super()._prep_show(parent=parent)
        if parent:
            if self.plot_legend or any(hasattr(c, 'plot_legend') and c.plot_legend for c in self.children):
                pls = self.plot_legend
                ls = self.legend_style if self.legend_style is not None else {}
                PlotLegend.check_styles(ls)
                if isinstance(pls, PlotLegend):
                    self.axes.legend(handles=pls, **pls.opts, **ls)
                else:
                    self.axes.legend(**ls)
            if 'ticks' in self._init_opts:
                self.ticks = self._init_opts['ticks']

    def get_padding_offsets(self):
        """
        **LLM Docstring**

        Compute the padding, expressed in plot-data coordinates, on each side of the
        axes (from the pixel padding and the plot range).

        :return: the `((left, right), (bottom, top))` data-coordinate offsets
        :rtype: list
        """
        ((l, r), (b, t)) = self.plot_range
        # w, h = self.image_size
        ((pl, pr), (pb, pt)) = self.padding
        ((alx, aby), (arx, aty)) = self.axes.get_bbox()
        w = arx - alx
        h = aty - aby
        pix_rat_x = (r - l) / w  # pixel to image coordiantes
        pix_rat_y = (t - b) / h
        ofl = pix_rat_x * (pl + self._axes_padding_offset[0])
        ofr = pix_rat_x * pr
        ofb = pix_rat_y * (pb + self._axes_padding_offset[1])
        oft = pix_rat_y * pt
        return [(ofl, ofr), (ofb, oft)]
    def get_bbox(self):
        """
        **LLM Docstring**

        Return the effective bounding box (in plot-data coordinates) of the total space
        the figure occupies, including padding.

        :return: the `[(min_x, min_y), (max_x, max_y)]` bbox
        :rtype: list
        """
        # gives _effective_ image coordinates for the total space taken up by the figure
        plr = self.plot_range
        (ofl, ofr), (ofb, oft) = self.get_padding_offsets()
        bbox = [
            (plr[0][0] - ofl, plr[1][0] - ofb),
            (plr[0][1] + ofr, plr[1][1] + oft)
        ]
        return bbox
    inset_options = dict(
        image_size='auto',
        background='#FFFFFF00',
        frame_style={'linewidth':0},#, 'color':'#FFFFFF00'},
        aspect_ratio='auto',
        ticks=[[], []],
        ticks_style={'width':0},
        ticks_label_style=[{'fontsize':0}, {'fontsize':0}]
    )
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
        if coordinates == 'absolute':
            ((lx, rx), (by, ty)) = self.plot_range
            w = rx - lx
            h = ty - by
            ((blx, bby), (brx, bty)) = bbox
            slx = ((blx - lx)) / w
            srx = ((brx - lx)) / w
            sby = ((bby - by)) / h
            sty = ((bty - by)) / h
            bbox = [(slx, sby), (srx, sty)]

            # ((ofl, ofr), (ofb, oft)) = self.get_padding_offsets()
            # w = (rx - lx + ofr + ofl)
            # h = (ty - by + oft + ofb)
            # # get coordinates relative to plot frame
            # ((blx, bby), (brx, bty)) = bbox
            # slx = (ofl+(blx-lx))/w
            # srx = (ofl+(brx-lx))/w
            # sby = (ofb+(bby-by))/h
            # sty = (ofb+(bty-by))/h
            # bbox = [(slx, sby), (srx, sty)]
            # # now shift to position of axis in total image
            coordinates = 'scaled'
        if graphics_class is None:
            graphics_class = Graphics
        return super().create_inset(bbox, coordinates=coordinates, graphics_class=graphics_class, **opts)

########################################################################################################################
#
#                                               Graphics3D
#
class Graphics3D(Graphics):

    default_style = Graphics.default_style | dict(frame=((True, False), (True, False), (True, False)))
    opt_keys = GraphicsBase.opt_keys | {'view_settings', 'box_ratios', 'projection_type', 'autoscale', 'aspect_ratio'}
    known_keys = Graphics.opt_keys | {'animate'}

    # layout_keys = axes_keys | figure_keys | GraphicsBase.layout_keys
    # known_keys = layout_keys

    def __init__(self, *args,
                 figure=None,
                 axes=None,
                 subplot_kw=None,
                 event_handlers=None,
                 animate=None,
                 axes_labels=None,
                 plot_label=None,
                 style_list=None,
                 plot_range=None,
                 plot_legend=None,
                 ticks=None,
                 scale=None,
                 ticks_style=None,
                 image_size=None,
                 background=None,
                 view_settings=None,
                 box_ratios=None,
                 projection_type=None,
                 aspect_ratio=None,
                 autoscale=None,
                 backend='matplotlib3D',
                 **kwargs
                 ):
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

        self._backend = backend
        super().__init__(
            *args,
            figure=figure,
            axes=axes,
            subplot_kw=subplot_kw,
            axes_labels=axes_labels,
            plot_label=plot_label,
            style_list=style_list,
            plot_range=plot_range,
            plot_legend=plot_legend,
            ticks=ticks,
            scale=scale,
            ticks_style=ticks_style,
            image_size=image_size,
            event_handlers=event_handlers,
            animate=animate,
            view_settings=view_settings,
            backend=backend,
            background=background,
            box_ratios=box_ratios,
            prop_manager=GraphicsPropertyManager3D,
            projection_type=projection_type,
            aspect_ratio=aspect_ratio,
            autoscale=autoscale,
            **kwargs
        )

    def set_options(self,
                    view_settings=None,
                    box_ratios=None,
                    projection_type=None,
                    aspect_ratio=None,
                    autoscale=None,
                    **parent_opts
                    ):
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

        super().set_options(**parent_opts)

        opts = (
            ('view_settings', view_settings),
            ('box_ratios', box_ratios),
            ('projection_type', projection_type),
            ('autoscale', autoscale),
            ('aspect_ratio', aspect_ratio)
        )
        for oname, oval in opts:
            oval = self._get_def_opt(oname, oval, {})
            if oval is not None:
                setattr(self, oname, oval)

    @property
    def box_ratios(self):
        """
        **LLM Docstring**

        The 3D box aspect ratios. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the box ratios value
        """
        return self._prop_manager.box_ratios
    @box_ratios.setter
    def box_ratios(self, value):
        """
        **LLM Docstring**

        The 3D box aspect ratios. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the box ratios value
        """
        self._prop_manager.box_ratios = value

    @property
    def autoscale(self):
        """
        **LLM Docstring**

        Whether the 3D axes autoscale. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the autoscale value
        """
        return self._prop_manager.autoscale
    @autoscale.setter
    def autoscale(self, value):
        """
        **LLM Docstring**

        Whether the 3D axes autoscale. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the autoscale value
        """
        self._prop_manager.autoscale = value

    @property
    def projection_type(self):
        """
        **LLM Docstring**

        The 3D projection type. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the projection type value
        """
        return self._prop_manager.projection_type
    @projection_type.setter
    def projection_type(self, value):
        """
        **LLM Docstring**

        The 3D projection type. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the projection type value
        """
        self._prop_manager.projection_type = value

    @property
    def view_settings(self):
        """
        **LLM Docstring**

        The 3D camera/view settings. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the view settings value
        """
        return self._prop_manager.view_settings
    @view_settings.setter
    def view_settings(self, value):
        """
        **LLM Docstring**

        The 3D camera/view settings. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the view settings value
        """
        self._prop_manager.view_settings = value

    def _prep_show(self, parent=False):
        """
        **LLM Docstring**

        Prepare the 3D plot for display, resolving `'auto'` box ratios to a concrete
        aspect ratio.

        :param parent: whether this is the parent of the figure
        :type parent: bool
        """
        super()._prep_show(parent=parent)
        br = self._prop_manager._box_ratios
        if dev.str_is(br, 'auto'):
            self.box_ratios = 'auto' # a bit of a hack, sets the actual aspect ratio

########################################################################################################################
#
#                                               GraphicsGrid
#
class GraphicsGrid(GraphicsBase):
    """
    A class for easily building sophisticated multi-panel figures.
    Robustification work still needs to be done, but the core interface is there.
    Supports themes & direct, easy access to the panels, among other things.
    Builds off of `GraphicsBase`.
    """
    default_style = dict(
        theme='mccoy',
        spacings=(50, 0)
    )
    layout_keys = GraphicsBase.layout_keys | {'nrows', 'ncols'}
    known_keys = GraphicsBase.known_keys | {'graphics_class'}
    def __init__(self,
                 *args,
                 nrows=None, ncols=None,
                 graphics_class=Graphics,
                 figure=None,
                 axes=None,
                 subplot_kw=None,
                 subimage_size=(310, 310),
                 subimage_aspect_ratio='auto',
                 padding=None,
                 spacings=None,
                 **opts
                 ):
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

        if len(args) > 0:
            if len(args) > 1:
                raise ValueError("wat")
            args = args[0]
            if isinstance(args[0], GraphicsBase):
                nr = 1
                nc = len(args)
            else:
                nr = len(args)
                nc = max(len(a) for a in args)

            if nrows is None:
                nrows = nr
            if ncols is None:
                ncols = nc
        if nrows is None:
            nrows = 2
        if ncols is None:
            ncols = 2
        self.shape = (nrows, ncols)

        if subplot_kw is None:
            subplot_kw={}
        else:
            subplot_kw={'subplot_kw':subplot_kw}
        subplot_kw.update(dict(
            nrows=nrows, ncols=ncols,
            graphics_class=graphics_class,
            subimage_size=subimage_size,
            subimage_aspect_ratio=subimage_aspect_ratio,
            padding=padding,
            spacings=spacings
        ))
        super().__init__(
            figure=figure, axes=axes,
            graphics_class=graphics_class,
            subplot_kw=subplot_kw,
            padding=padding,
            spacings=spacings,
            **opts
        )
        self._colorbar_axis = None # necessary hack for only GraphicsGrid

        if len(args) > 0:
            if isinstance(args[0], GraphicsBase):
                for i, g in enumerate(args):
                    self[0, i] = g
            else:
                for i, r in enumerate(args):
                    for j, g in enumerate(r):
                        self[i, j] = g

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
            self.parent = parent #type: GraphicsBase
            self.stack = np.empty_like(graphics, dtype=object)
            self.stack[:] = graphics
        def __getitem__(self, item):
            """
            **LLM Docstring**

            Index into the panel stack.

            :param item: the index
            :return: the panel(s)
            """
            return self.stack[item]
        def __setitem__(self, item, value):
            """
            **LLM Docstring**

            Assign into the panel stack.

            :param item: the index
            :param value: the panel(s)
            """
            self.stack[item] = value
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
            @functools.wraps(getattr(Graphics, attr))
            def call(*args, **kwargs):
                """
                **LLM Docstring**

                Invoke the captured method on each panel, yielding the results.

                :param args: positional arguments for the method
                :param kwargs: keyword arguments for the method
                :return: a generator of per-panel results
                """
                for ax in self.stack.flat:
                    yield getattr(ax, attr)(*args, **kwargs)
            return call
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
            ax = next(self.stack.flat).axes
            @functools.wraps(getattr(ax, attr))
            def call(*args, **kwargs):
                """
                **LLM Docstring**

                Invoke the captured axes method on each panel's axes, yielding the results.

                :param args: positional arguments for the method
                :param kwargs: keyword arguments for the method
                :return: a generator of per-panel results
                """
                for ax in self.stack.flat:
                    yield getattr(ax.axes, attr)(*args, **kwargs)
            return call
        def get_bboxes(self):
            """
            **LLM Docstring**

            Return each panel's bounding box.

            :return: the per-panel bounding boxes
            :rtype: list
            """
            return [
                    a.get_bbox() for a in self.stack.flat
                ]
        def get_bbox(self):
            """
            **LLM Docstring**

            Return the bounding box enclosing all panels.

            :return: the combined bounding box
            :rtype: list
            """
            bboxes = [
                a.get_bbox() for a in self.stack.flat
            ]

            bbox = [list(x) for x in bboxes[0]]
            for ((bl, br), (tl, tr)) in bboxes[1:]:
                bbox[0][0] = min(bbox[0][0], bl)
                bbox[0][1] = min(bbox[0][1], br)
                bbox[1][0] = max(bbox[1][0], tl)
                bbox[1][1] = max(bbox[1][1], tr)

            return bbox
        def get_padding(self):
            """
            **LLM Docstring**

            Compute the grid's outer padding from the panels' paddings.

            :return: the `((left, right), (bottom, top))` padding
            :rtype: list
            """
            paddings = [
                [a.padding for a in ax]
                for ax in self.stack
            ]
            padding = [[0, 0], [0, 0]]
            for i,pad_list in enumerate(paddings):
                if i == 0:
                    padding[1][1] = max(p[1][1] for p in pad_list)
                elif i == len(paddings) - 1:
                    padding[1][0] = max(p[1][0] for p in pad_list)
                padding[0][0] = max([padding[0][0], pad_list[0][0][0]])
                padding[0][1] = max([padding[0][1], pad_list[-1][0][1]])

            return padding

        def set_facecolor(self, fg):
            """
            **LLM Docstring**

            No-op face-color setter (panels manage their own backgrounds).

            :param fg: the (ignored) face color
            """
            pass

        def prep_show(self):
            """
            **LLM Docstring**

            No-op satisfying `GraphicsBase._prep_show`'s `self.axes.prep_show()` call
            for a `GraphicsGrid`.

            A grid's panels are each independent `Graphics` objects registered as
            children of the shared figure (see `GraphicsBase.children`), so
            `GraphicsBase.prep_show` already iterates `self.children` and calls
            `_prep_show` on every panel directly -- and *that* call reaches each
            panel's own single-axes wrapper and invokes `prep_show` there. This
            `GraphicsStack` (the grid's stand-in for a single `axes`) therefore has
            nothing further to prepare; it exists only so the grid's own
            `_prep_show`, which treats `self.axes` like any other axes wrapper,
            has something to call instead of raising `AttributeError`.

            :return: `None`
            """
            pass

        def __iter__(self):
            """
            **LLM Docstring**

            Iterate over the panels (flattened).

            :return: the panel iterator
            """
            return self.stack.flat
            # else:
            #     raise AttributeError("{} has no attribute {}".format(Graphics.__name__, attr))

    def initialize_figure_and_axes(self,
                      figure, axes, *,
                      nrows=None, ncols=None, graphics_class=None,
                      fig_kw=None, subplot_kw=None,
                      padding=None, spacings=None,
                      subimage_size=None, subimage_aspect_ratio=None,
                      **kw
                      ):
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

        if 'image_size' not in kw:
            kw['image_size'] = subimage_size
        else:
            subimage_size = kw['image_size']
        if figure is None:
            padding = self._get_def_opt('padding', padding, {})
            # subimage_aspect_ratio = self._get_def_opt('aspect_ratio', subimage_aspect_ratio, {})
            spacings = self._get_def_opt('spacings', spacings, {})
            if subplot_kw is None:
                subplot_kw = {}
            if fig_kw is None:
                fig_kw = {}
            if 'figsize' not in fig_kw:
                try:
                    dw, dh = subimage_size
                except (ValueError, TypeError):
                    dw = dh = subimage_size
                w = ncols * dw
                h = nrows * dh
                if padding is not None:
                    if dev.is_number(padding): padding = [padding, padding]
                    pw, ph = padding
                    try:
                        pwx, pwy = pw
                    except (TypeError, ValueError):
                        pwx = pwy = pw
                    try:
                        phx, phy = ph
                    except (TypeError, ValueError):
                        phx = phy = ph

                    w += pwx + pwy
                    h += phx + phy
                if spacings is not None:
                    sw, sh = spacings
                    w += (ncols-1) * sw
                    h += (nrows-1) * sh
                fig_kw['figsize'] = (w/DPI_SCALING, h/DPI_SCALING)

            figure, axes = super().initialize_figure_and_axes(
                figure, axes, nrows=nrows, ncols=ncols, subplot_kw=subplot_kw,
                **fig_kw
            )


            if not isinstance(axes, (np.ndarray, list, tuple)):
                axes = [[axes]]
            elif not isinstance(axes[0], (np.ndarray, list, tuple)):
                if ncols == 1:
                    axes = [[ax] for ax in axes]
                else:
                    axes = [axes]

            axes = [[a for a in ax] for ax in axes]
            for i in range(nrows):
                for j in range(ncols):
                    axes[i][j] = graphics_class(figure=figure, axes=axes[i][j], managed=True, **kw)
            axes = self.GraphicsStack(self, axes)
        elif isinstance(figure, GraphicsGrid):
            axes = figure.axes
            figure = figure.figure

        if axes is None:
            axes = self.GraphicsStack(self, [
                graphics_class(
                    figure.create_axes(nrows, ncols, i),
                    managed=True,
                    **kw
                ) for i in range(nrows * ncols)
            ])

        return figure, axes

    def set_options(self,
                    padding=None,
                    spacings=None,
                    background=None,
                    colorbar=None,
                    figure_label=None,
                    **parent_opts
                    ):
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

        super().set_options(**parent_opts)

        self.image_size = None
        opts = (
            ('figure_label', figure_label),
            ('padding', padding),
            ('spacings', spacings),
            ('background', background),
            ('colorbar', colorbar)
        )
        for oname, oval in opts:
            oval = self._get_def_opt(oname, oval, {})
            if oval is not None:
                setattr(self, oname, oval)

    def __iter__(self):
        """
        **LLM Docstring**

        Iterate over the grid's panels.

        :return: the panel iterator
        """
        return iter(self.axes)
    def __getitem__(self, item):
        """
        **LLM Docstring**

        Get a panel by `(row, col)` (or a flat index).

        :param item: the index
        :return: the panel
        :rtype: GraphicsBase
        """
        try:
            i, j = item
        except ValueError:
            return self.axes[item]
        else:
            return self.axes[i][j]
    def __setitem__(self, item, val):
        """
        **LLM Docstring**

        Place a graphics object into a panel by `(row, col)` (or flat index), re-hosting
        it onto the grid's figure.

        :param item: the index
        :param val: the graphics object (or raw value)
        """
        try:
            i, j = item
        except ValueError:
            if isinstance(val, GraphicsBase):
                self.axes[item] = val.change_figure(self.axes[item], image_size=val.image_size)
            else:
                self.axes[item] = val
        else:
            if isinstance(val, GraphicsBase):
                self.axes[i][j] = val.change_figure(self.axes[i][j], image_size=val.image_size)
            else:
                self.axes[i][j] = val
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
        pos = tuple(pos) if not isinstance(pos, int) else pos
        self.axes[pos] = val.change_figure(self.axes[pos], image_size=val.image_size, **opts)
        return self.axes[pos]

    # set size
    def calc_image_size(self):
        """
        **LLM Docstring**

        Compute the grid's overall image size from the panels' sizes, the inter-panel
        spacings, and the padding.

        :return: the `(width, height)` image size
        :rtype: tuple
        """
        w=0; h=0
        for l in self.axes.stack:
            mh = 0; mw = 0
            for f in l:
                wh = f.image_size
                if wh is not None:
                    mw += wh[0]
                    if wh[1] > mh:
                        mh = wh[1]
            h += mh
            if w < mw:
                w = mw

        spacings = self.spacings
        if spacings is not None:
            sw, sh = spacings
            w += (self.shape[1] - 1) * sw
            h += (self.shape[0] - 1) * sh

        pad = self.padding
        if pad is not None:
            pw, ph = pad
            w += pw[0] + pw[1]
            h += ph[0] + ph[1]
        return w, h

    @property
    def image_size(self):
        """
        **LLM Docstring**

        The grid's overall image size (recomputed from the panels on access).

        :return: the `(width, height)` image size
        :rtype: tuple
        """
        s = self.calc_image_size()
        self._prop_manager.image_size = s
        return s
    @image_size.setter
    def image_size(self, value):
        """
        **LLM Docstring**

        The grid's overall image size (recomputed from the panels on access).

        :return: the `(width, height)` image size
        :rtype: tuple
        """
        s = self.calc_image_size()
        self._prop_manager.image_size = s

    @property
    def figure_label(self):
        """
        **LLM Docstring**

        The overall figure label. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the figure label value
        """
        return self._prop_manager.figure_label
    @figure_label.setter
    def figure_label(self, value):
        """
        **LLM Docstring**

        The overall figure label. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the figure label value
        """
        self._prop_manager.figure_label = value
    @property
    def padding(self):
        """
        **LLM Docstring**

        The grid's outer padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the padding value
        """
        return self._prop_manager.padding
    @padding.setter
    def padding(self, value):
        """
        **LLM Docstring**

        The grid's outer padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the padding value
        """
        self._prop_manager.padding = value
    @property
    def padding_left(self):
        """
        **LLM Docstring**

        The grid's left padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the left padding value
        """
        return self._prop_manager.padding_left
    @padding_left.setter
    def padding_left(self, value):
        """
        **LLM Docstring**

        The grid's left padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the left padding value
        """
        self._prop_manager.padding_left = value
    @property
    def padding_right(self):
        """
        **LLM Docstring**

        The grid's right padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the right padding value
        """
        return self._prop_manager.padding_right
    @padding_right.setter
    def padding_right(self, value):
        """
        **LLM Docstring**

        The grid's right padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the right padding value
        """
        self._prop_manager.padding_right = value
    @property
    def padding_top(self):
        """
        **LLM Docstring**

        The grid's top padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the top padding value
        """
        return self._prop_manager.padding_top
    @padding_top.setter
    def padding_top(self, value):
        """
        **LLM Docstring**

        The grid's top padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the top padding value
        """
        self._prop_manager.padding_top = value
    @property
    def padding_bottom(self):
        """
        **LLM Docstring**

        The grid's bottom padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the bottom padding value
        """
        return self._prop_manager.padding_bottom
    @padding_bottom.setter
    def padding_bottom(self, value):
        """
        **LLM Docstring**

        The grid's bottom padding. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the bottom padding value
        """
        self._prop_manager.padding_bottom = value

    @property
    def spacings(self):
        """
        **LLM Docstring**

        The inter-panel spacings. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the spacings value
        """
        return self._prop_manager.spacings
    @spacings.setter
    def spacings(self, value):
        """
        **LLM Docstring**

        The inter-panel spacings. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the spacings value
        """
        self._prop_manager.spacings = value

    @property
    def background(self):
        """
        **LLM Docstring**

        The grid background color. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the background value
        """
        return self._prop_manager.background
    @background.setter
    def background(self, value):
        """
        **LLM Docstring**

        The grid background color. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the background value
        """
        self._prop_manager.background = value

    @property
    def colorbar(self):
        """
        **LLM Docstring**

        The grid colorbar specification. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the colorbar value
        """
        return self._prop_manager.colorbar
    @colorbar.setter
    def colorbar(self, value):
        """
        **LLM Docstring**

        The grid colorbar specification. Getter/setter delegate to the property manager (the setter also records
        the change for copying).

        :return: the colorbar value
        """
        self._prop_manager.colorbar = value

    # def _prep_show(self):
    #     self.image_size = None
    #     if self.spacings is not None:
    #         self.spacings = self.spacings
    #     if self.padding is not None:
    #         self.padding = self.padding
    #     if self.tighten:
    #         self.figure.tight_layout()
        # super().prep_show()

    def _prep_show(self, parent=False):
        """
        **LLM Docstring**

        Prepare the grid for display: recompute the image size and re-apply the
        spacings/padding, tightening the layout if requested.

        :param parent: whether this is the parent of the figure
        :type parent: bool
        """
        super()._prep_show(parent=parent)
        self.image_size = None
        if self.spacings is not None:
            self.spacings = self.spacings
        if self.padding is not None:
            self.padding = self.padding
        if self.tighten:
            self.figure.tight_layout()
    # def prep_show(self):
    #     if self.figure_parent is self:
    #         self._prep_show(parent=True)
    #         for c in self.children:
    #             if hasattr(c, '_prep_show'):
    #                 c._prep_show(parent=False)
    #             else:
    #                 c.prep_show()
    #     else:
    #         self.figure_parent.prep_show()
    #     return self

    # def show(self, **kwargs):
    #     super().show(**kwargs)


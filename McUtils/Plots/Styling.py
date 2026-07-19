"""
Defines a helper class Styled to make it easier to style plots and stuff and a ThemeManager to handle all that shiz
"""
import contextlib
from collections import deque
from .Backends import GraphicsBackend
from .Colors import ColorPalette

__all__ = [
    "Styled",
    "ThemeManager",
    "PlotLegend"
]


class Styled:
    """
    Simple styling class
    """
    def __init__(self, *str, **opts):
        """
        **LLM Docstring**

        Hold a value together with a dict of styling options.

        :param str: the value(s) (optionally a `(value, opts_dict)` pair)
        :param opts: styling options
        """
        if len(str) == 2 and isinstance(str[1], dict):
            opts = dict(str[1], **opts)
            str = [str[0]]
        self.val = str
        self.opts = opts
    @classmethod
    def could_be(cls, data):
        """
        **LLM Docstring**

        Test whether a piece of data is a `(value, opts_dict)` pair that could be a
        `Styled`.

        :param data: the data to test
        :return: whether it looks like a styled value
        :rtype: bool
        """
        return isinstance(data, tuple) and len(data) == 2 and isinstance(data[1], dict)
    @classmethod
    def construct(cls, data):
        """
        **LLM Docstring**

        Build a `Styled` from a `(value, opts_dict)` pair.

        :param data: the `(value, opts_dict)` pair
        :return: the styled value
        :rtype: Styled
        """
        return cls(data[0], **data[1])
    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation showing the value and options.

        :return: the representation
        :rtype: str
        """
        cls = type(self)
        return f"{cls.__name__}({self.val}, {self.opts})"

class PlotLegend(list):
    known_styles = {"handles", "labels", "loc", "bbox_to_anchor", "ncol", "prop", "fontsize",
                    "labelcolor", "numpoints", "scatterpoints", "scatteryoffsets", "markerscale",
                    "markerfirst", "frameon", "fancybox", "shadow", "framealpha", "facecolor",
                    "edgecolor", "mode", "bbox_transform", "title", "title_fontproperties",
                    "title_fontsize", "borderpad", "labelspacing", "handlelength", "handleheight",
                    "handletextpad", "borderaxespad", "columnspacing", "handler_map",
                    "draggable"}
    default_styles={'frameon':False}
    def __init__(self, components, **styles):
        """
        **LLM Docstring**

        Build a legend (a list of handle components plus styling options), validating the
        styles and filling in defaults.

        :param components: the legend handle components (or another `PlotLegend`)
        :param styles: legend styling options
        :raises ValueError: for unknown style keys
        """
        if isinstance(components, type(self)):
            self.__init__(list(self), **self.opts)
        else:
            super().__init__(components)
            self.check_styles(styles)
            for d in self.default_styles - styles.keys():
                styles[d] = self.default_styles[d]
            self.opts = styles
    @classmethod
    def check_styles(cls, styles):
        """
        **LLM Docstring**

        Raise if any style keys aren't among the known legend styles.

        :param styles: the styles to check
        :type styles: dict
        :raises ValueError: for unknown style keys
        """
        unkown = styles.keys() - cls.known_styles
        if len(unkown) > 0:
            raise ValueError("styles {} not known for {}".format(unkown, cls.__name__))
    @classmethod
    def could_be_legend(cls, bits):
        """
        **LLM Docstring**

        Test whether a value could be legend components (an iterable that isn't a bare
        scalar/string).

        :param bits: the value to test
        :return: whether it could be a legend
        :rtype: bool
        """
        if isinstance(bits, (str, int, float)):
            return False
        try:
            iter(bits)
        except TypeError:
            return False
        return True
    @classmethod
    def construct(cls, bits):
        """
        **LLM Docstring**

        Build a `PlotLegend` from components (accepting an existing legend, a
        `(components, opts)` pair, or a bare component list), canonicalizing dict-specified
        handles.

        :param bits: the components (or `(components, opts)` pair)
        :return: the legend
        :rtype: PlotLegend
        """
        if isinstance(bits, cls):
            return bits
        elif len(bits) == 2 and hasattr(bits[1], 'items') and not hasattr(bits[0], 'items'):
            bits, opts = bits
        else:
            opts = {}
        bits = [b if not hasattr(b, 'items') else cls.canonicalize_bit(**b) for b in bits]
        return cls(bits, **opts)
    @classmethod
    def construct_line_marker(cls, lw=4, **opts):
        """
        **LLM Docstring**

        Build a line legend handle (a matplotlib `Line2D`).

        :param lw: the line width
        :type lw: float
        :param opts: extra line options
        :return: the legend handle
        """
        from matplotlib.lines import Line2D
        return Line2D([0], [0], lw=lw, **opts)
    @classmethod
    def construct_dot_marker(cls, **opts):
        """
        **LLM Docstring**

        Build a dot/patch legend handle (a matplotlib `Patch`).

        :param opts: patch options
        :return: the legend handle
        """
        from matplotlib.patches import Patch
        return Patch(**opts)
    @classmethod
    def load_constructors(cls):
        """
        **LLM Docstring**

        Return the mapping of marker names to their legend-handle constructors.

        :return: the constructor mapping
        :rtype: dict
        """
        return {
        'line':cls.construct_line_marker,
        'dot':cls.construct_dot_marker
    }
    marker_synonyms={'-':'line', '.':'dot'}
    @classmethod
    def canonicalize_bit(cls, marker='-', **opts):
        """
        **LLM Docstring**

        Build a single legend handle from a marker spec (resolving marker synonyms and
        dispatching to the appropriate constructor).

        :param marker: the marker name/synonym (or a constructor callable)
        :param opts: handle options
        :return: the legend handle
        """
        if isinstance(marker, str) and marker in cls.marker_synonyms:
            marker = cls.marker_synonyms[marker]
        if isinstance(marker, str):
            return cls.load_constructors()[marker](**opts)
        else:
            return marker(**opts)
    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation showing the components and options.

        :return: the representation
        :rtype: str
        """
        return "{}({}, {})".format(
            type(self).__name__,
            super().__repr__(),
            self.opts
        )

class cycler:
    # transparent mimic of mpl cycler
    def __init__(self, **style_cycles):
        """
        **LLM Docstring**

        A minimal transparent mimic of matplotlib's `cycler`, cycling through several
        named style-value lists in lockstep.

        :param style_cycles: the named lists of style values to cycle through
        """
        self.opts = style_cycles
        self.keys = list(style_cycles.keys())
        self.lens = [len(style_cycles[k]) for k in self.keys]
        self.inds = [0]*len(style_cycles)
    def __next__(self):
        """
        **LLM Docstring**

        Return the next combination of style values, advancing each cycle (wrapping at its
        length).

        :return: the current `{style: value}` mapping
        :rtype: dict
        """
        vals = {
            k:self.opts[k][i]
            for k,i in zip(self.keys, self.inds)
        }
        self.inds = [(i+1)%l for i,l in zip(self.inds, self.lens)]
        return vals

class ThemeManager:
    """
    Simple manager class for plugging into themes in a semi-background agnostic way
    """
    extra_themes = {
        'mccoy': (
            ([],),
            {
                'axes': {
                    'prop_cycle':{'color': ['#001C7F', '#017517', '#8C0900', '#7600A1', '#B8860B', '#006374']},
                    'labelsize':13
                },
                'patch': {'facecolor': '#001C7F'},
                'xtick': {'labelsize': 13},
                'ytick': {'labelsize': 13},
                'padding': 50,
                'aspect_ratio': 'auto'
            }
        )

    }
    _resolved_theme_cache = {

    }
    def __init__(self, *theme_names, backend=None, graphics_styles=None, **extra_styles):
        """
        **LLM Docstring**

        Set up a theme manager that applies named themes (and extra styles) via a graphics
        backend's theme context.

        :param theme_names: the base theme names
        :param backend: the graphics backend (defaults to matplotlib)
        :param graphics_styles: extra graphics-level styles
        :type graphics_styles: dict | None
        :param extra_styles: extra theme properties
        """
        self.main_theme_names = theme_names
        self.extra_styles = extra_styles
        self.graphics_styles = graphics_styles
        if backend is None: backend = GraphicsBackend.lookup('matplotlib')
        self.backend = backend
        self.context_manager = None
    @classmethod
    def from_spec(cls, theme, backend=None):
        """
        **LLM Docstring**

        Build a `ThemeManager` (or a `NoThemeManager` for `None`) from a flexible theme
        specification (a name, a properties dict, or a `(names, properties)` pair).

        :param theme: the theme specification
        :param backend: the graphics backend
        :return: the theme manager
        :rtype: ThemeManager | NoThemeManager
        """
        if theme is None:
            return NoThemeManager()
        if isinstance(theme, str):
            theme = [theme]
        elif isinstance(theme, dict):
            theme = [(), theme]
        if len(theme) > 0:
            try:
                theme_names, theme_properties = theme
            except ValueError:
                theme_names = theme[0]
                theme_properties = {}
            if isinstance(theme_names, dict):
                theme_properties = theme_names
                theme_names = []
            elif isinstance(theme_names, str):
                theme_names = [theme_names]
        else:
            theme_names = []
            theme_properties = {}
        return cls(*theme_names, backend=backend, **theme_properties)
    def _test_rcparam(self, k):
        """
        **LLM Docstring**

        Test whether a key is a dotted matplotlib rcParam name.

        :param k: the key
        :type k: str
        :return: whether it's an rcParam key
        :rtype: bool
        """
        return '.' in k
    @classmethod
    def canonicalize_theme_props(cls, props):
        """
        **LLM Docstring**

        Recursively normalize theme properties, expanding a `palette` entry into a color
        `prop_cycle`.

        :param props: the theme properties
        :return: the canonicalized properties
        """
        if isinstance(props, dict):
            new_props = {}
            for k,v in props.items():
                if isinstance(v, dict):
                    new_props[k] = cls.canonicalize_theme_props(v)
                elif k == 'palette':
                    colors = ColorPalette(v).color_strings
                    new_props['prop_cyle'] = dict(
                        new_props.get('prop_cycle'),
                        color=colors
                    )
        else:
            return props

    def __enter__(self):
        """
        **LLM Docstring**

        Enter the theme context: resolve, validate, and canonicalize the theme, then
        apply it via the backend's theme context.

        :return: the entered theme context
        """
        theme = self.resolve_theme(None, *self.main_theme_names, **self.extra_styles)
        name_list = self.validate_theme(*theme)
        theme_props = self.canonicalize_theme_props(theme)
        # name_list = list(theme[0])
        # opts = {k:v for k,v in theme[1].items() if self._test_rcparam(k)}

        self.context_manager = self.backend.theme_context(name_list, theme[1])
        return self.context_manager.__enter__()
        # don't currently support any other backends...
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Exit the theme context, restoring the previous theme.

        :param exc_type: the exception type, if any
        :param exc_val: the exception value, if any
        :param exc_tb: the traceback, if any
        """
        if self.context_manager is not None:
            self.context_manager.__exit__(exc_type, exc_val, exc_tb)
            self.context_manager = None
    @property
    def theme(self):
        """
        **LLM Docstring**

        The resolved theme (names and styles) for this manager.

        :return: the `[theme_names, styles]` theme
        :rtype: list
        """
        return self.resolve_theme(None, *self.main_theme_names, **self.extra_styles)
    @classmethod
    def add_theme(self, theme_name, *base_theme, **extra_styles):
        """
        Adds a theme to the extra themes dict. At some future date we'll
        want to make it so that this does a level of validation, too.
        :param theme_name:
        :type theme_name:
        :param base_theme:
        :type base_theme:
        :param extra_styles:
        :type extra_styles:
        :return:
        :rtype:
        """
        self.extra_themes[theme_name] = (base_theme, extra_styles)
    @classmethod
    def resolve_theme(self, theme_name, *base_themes, **extra_styles):
        """
        Resolves a theme so that it only uses strings for built-in styles
        :return:
        :rtype:
        """
        if theme_name is not None:
            if theme_name in self._resolved_theme_cache:
                themes, styles = self._resolved_theme_cache[theme_name]
            elif theme_name in self.extra_themes:
                # recursively resolve the theme
                bases, extras = self.extra_themes[theme_name]
                if isinstance(bases, str):
                    bases = [bases]
                theme_stack = deque()
                style_stack = deque()
                for theme_list in bases:
                    if isinstance(theme_list, str):
                        theme_list = [theme_list]
                    remainder_themes = []
                    for theme in theme_list:
                        if theme in self.extra_themes:
                            t, s = self.resolve_theme(theme_name)
                            theme_stack.appendleft(t)
                            style_stack.append(s)
                        else:
                            remainder_themes.append(theme)
                    if len(remainder_themes) > 0:
                        theme_stack.appendleft([remainder_themes])
                themes = tuple(x for y in theme_stack for x in y)
                styles = {}
                for s in style_stack:
                    styles.update(s)
                styles.update(extras)
                self._resolved_theme_cache[theme_name] = [themes, styles]
            else:
                themes = (theme_name,)
                styles = {}
        else:
            themes = ()
            styles = {}

        for name_list in base_themes:
            if isinstance(name_list, str):
                name_list = [name_list]
            remainder_themes = []
            for b in name_list:
                if b in self.extra_themes:
                    t, s = self.resolve_theme(b)
                    themes = tuple(t) + themes
                    styles.update(s)
                else:
                    remainder_themes.append(b)
            if len(remainder_themes) > 0:
                themes = (remainder_themes,) + themes

        styles.update(extra_styles)

        return [themes, styles]
    def validate_theme(self, theme_names, theme_styless):
        """
        **LLM Docstring**

        Validate the theme names against the backend's supported themes, resolving each
        name (or the first supported alternative in a group).

        :param theme_names: the theme names (or alternative groups)
        :param theme_styless: the theme styles (unused here)
        :return: the resolved theme names
        :rtype: list
        :raises ValueError: if a theme name isn't supported
        """
        valid_names = set(self.backend_themes)
        resolved_names = []
        for k in theme_names:
            if isinstance(k, str):
                if k not in valid_names:
                    raise ValueError("{}.{}: theme '{}' isn't in supported set ({})".format(
                        type(self).__name__,
                        'validate_theme',
                        k,
                        valid_names
                    ))
                else:
                    resolved_names.append(k)
            else:
                for altname in k:
                    if altname in valid_names:
                        resolved_names.append(altname)
                        break
                else:
                    raise ValueError("{}.{}: no theme in '{}' isn't in supported set ({})".format(
                        type(self).__name__,
                        'validate_theme',
                        k,
                        valid_names
                    ))
        return resolved_names

    @property
    def backend_themes(self):
        """
        **LLM Docstring**

        The theme names supported by the backend.

        :return: the supported theme names
        :rtype: tuple
        """
        theme_names = self.backend.get_available_themes()
        return tuple(theme_names)
    @property
    def theme_names(self):
        """
        **LLM Docstring**

        All available theme names (backend themes plus the registered extra themes).

        :return: the theme names
        :rtype: tuple
        """
        return self.backend_themes + tuple(self.extra_themes.keys())

class NoThemeManager:
    """
    Does nothing but makes code consistent
    """
    def __enter__(self):
        """
        **LLM Docstring**

        No-op context entry (a do-nothing theme manager).
        """
        pass
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        No-op context exit.

        :param exc_type: the exception type, if any
        :param exc_val: the exception value, if any
        :param exc_tb: the traceback, if any
        """
        pass

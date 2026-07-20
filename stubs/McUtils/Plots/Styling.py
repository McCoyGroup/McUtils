"""
Defines a helper class Styled to make it easier to style plots and stuff and a ThemeManager to handle all that shiz
"""
import contextlib
from collections import deque
from .Backends import GraphicsBackend
from .Colors import ColorPalette
__all__ = ['Styled', 'ThemeManager', 'PlotLegend']

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
        ...

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
        ...

    @classmethod
    def construct(cls, data):
        """
        **LLM Docstring**

        Build a `Styled` from a `(value, opts_dict)` pair.

        :param data: the `(value, opts_dict)` pair
        :return: the styled value
        :rtype: Styled
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation showing the value and options.

        :return: the representation
        :rtype: str
        """
        ...

class PlotLegend(list):
    default_styles = {'frameon': False}

    def __init__(self, components, **styles):
        """
        **LLM Docstring**

        Build a legend (a list of handle components plus styling options), validating the
        styles and filling in defaults.

        :param components: the legend handle components (or another `PlotLegend`)
        :param styles: legend styling options
        :raises ValueError: for unknown style keys
        """
        ...

    @classmethod
    def check_styles(cls, styles):
        """
        **LLM Docstring**

        Raise if any style keys aren't among the known legend styles.

        :param styles: the styles to check
        :type styles: dict
        :raises ValueError: for unknown style keys
        """
        ...

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
        ...

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
        ...

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
        ...

    @classmethod
    def construct_dot_marker(cls, **opts):
        """
        **LLM Docstring**

        Build a dot/patch legend handle (a matplotlib `Patch`).

        :param opts: patch options
        :return: the legend handle
        """
        ...

    @classmethod
    def load_constructors(cls):
        """
        **LLM Docstring**

        Return the mapping of marker names to their legend-handle constructors.

        :return: the constructor mapping
        :rtype: dict
        """
        ...
    marker_synonyms = {'-': 'line', '.': 'dot'}

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
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation showing the components and options.

        :return: the representation
        :rtype: str
        """
        ...

class cycler:

    def __init__(self, **style_cycles):
        """
        **LLM Docstring**

        A minimal transparent mimic of matplotlib's `cycler`, cycling through several
        named style-value lists in lockstep.

        :param style_cycles: the named lists of style values to cycle through
        """
        ...

    def __next__(self):
        """
        **LLM Docstring**

        Return the next combination of style values, advancing each cycle (wrapping at its
        length).

        :return: the current `{style: value}` mapping
        :rtype: dict
        """
        ...

class ThemeManager:
    """
    Simple manager class for plugging into themes in a semi-background agnostic way
    """
    _resolved_theme_cache = {}

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
        ...

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
        ...

    def _test_rcparam(self, k):
        """
        **LLM Docstring**

        Test whether a key is a dotted matplotlib rcParam name.

        :param k: the key
        :type k: str
        :return: whether it's an rcParam key
        :rtype: bool
        """
        ...

    @classmethod
    def canonicalize_theme_props(cls, props):
        """
        **LLM Docstring**

        Recursively normalize theme properties, expanding a `palette` entry into a color
        `prop_cycle`.

        :param props: the theme properties
        :return: the canonicalized properties
        """
        ...

    def __enter__(self):
        """
        **LLM Docstring**

        Enter the theme context: resolve, validate, and canonicalize the theme, then
        apply it via the backend's theme context.

        :return: the entered theme context
        """
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Exit the theme context, restoring the previous theme.

        :param exc_type: the exception type, if any
        :param exc_val: the exception value, if any
        :param exc_tb: the traceback, if any
        """
        ...

    @property
    def theme(self):
        """
        **LLM Docstring**

        The resolved theme (names and styles) for this manager.

        :return: the `[theme_names, styles]` theme
        :rtype: list
        """
        ...

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
        ...

    @classmethod
    def resolve_theme(self, theme_name, *base_themes, **extra_styles):
        """
        Resolves a theme so that it only uses strings for built-in styles
        :return:
        :rtype:
        """
        ...

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
        ...

    @property
    def backend_themes(self):
        """
        **LLM Docstring**

        The theme names supported by the backend.

        :return: the supported theme names
        :rtype: tuple
        """
        ...

    @property
    def theme_names(self):
        """
        **LLM Docstring**

        All available theme names (backend themes plus the registered extra themes).

        :return: the theme names
        :rtype: tuple
        """
        ...

class NoThemeManager:
    """
    Does nothing but makes code consistent
    """

    def __enter__(self):
        """
        **LLM Docstring**

        No-op context entry (a do-nothing theme manager).
        """
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        No-op context exit.

        :param exc_type: the exception type, if any
        :param exc_val: the exception value, if any
        :param exc_tb: the traceback, if any
        """
        ...
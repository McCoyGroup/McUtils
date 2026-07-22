__all__ = ['App', 'SettingsPane', 'Manipulator']
import types, typing
import numpy as np
from ..JHTML import JHTML, DefaultOutputWidget
from .Interfaces import *
from .Controls import Control, FunctionDisplay
from .Variables import WidgetControl, InterfaceVars, DefaultVars
__reload_hook__ = ['..JHTML', '.Interfaces', '.Controls', '.Variables']

class Manipulator(Card):
    theme = Card.merge_themes(Card.theme, {'controls': {}, 'output': {}})

    def __init__(self, func, *controls, debounce=None, autoclear=True, namespace=None, layout_function=None, control_layout_function=None, **etc):
        """
        **LLM Docstring**

        Build an interactive `Card` that re-runs a function over a set of controls
        (ipywidgets-`interact`-style), laying out the output above the controls.

        :param func: the function driven by the controls
        :type func: Callable
        :param controls: the control specs (values, ranges, or existing controls)
        :param debounce: the debounce interval for updates
        :param autoclear: clear the output before each update
        :type autoclear: bool
        :param namespace: the variable namespace (a fresh one if omitted)
        :param etc: extra `Card` options
        """
        ...

    @classmethod
    def default_layout(cls, self):
        ...

    @classmethod
    def default_control_layout(cls, self):
        ...

    @classmethod
    def canonicalize_control(cls, settings, namespace=None):
        """
        **LLM Docstring**

        Normalize a control spec into a `Control`: pass existing controls through, else
        build one from a `(var, settings)` pair (inferring a `range`/`value` settings dict
        and the control type).

        :param settings: the control spec
        :param namespace: the variable namespace
        :return: the control
        :rtype: Control
        """
        ...

    def initialize(self):
        """
        **LLM Docstring**

        Run the function once (with no event) to populate the output.
        """
        ...

class App(Component):
    """
    Provides a framework for making Jupyter Apps with the
    elements built out in the Interfaces package
    """
    _app_stack = []

    @classmethod
    def merge_themes(cls, theme_1, theme_2):
        """
        **LLM Docstring**

        Recursively merge two theme dicts (the second overriding/extending the first).

        :param theme_1: the base theme
        :type theme_1: dict
        :param theme_2: the overriding theme
        :type theme_2: dict
        :return: the merged theme
        :rtype: dict
        """
        ...

    def __init__(self, body=None, header=None, footer=None, sidebar=None, toolbar=None, theme='primary', layout='grid', cls='app border', output=None, capture_output=None, namespace=None, vars=None, **attrs):
        """
        **LLM Docstring**

        Build a Jupyter app framework from optional header/footer/sidebar/toolbar/body
        sections, a theme, and a layout, tracking the app stack and its output/variable
        context.

        :param body: the body content
        :param header: the header content
        :param footer: the footer content
        :param sidebar: the sidebar content
        :param toolbar: the toolbar content
        :param theme: the theme name or overrides
        :param layout: the layout style (e.g. `'grid'`)
        :type layout: str
        :param cls: the root CSS classes
        :param output: the output area (created if omitted)
        :param capture_output: show a captured-output panel (defaults to top-level only)
        :type capture_output: bool | None
        :param vars: the variable set (resolved from the default if omitted)
        :param attrs: extra layout attributes
        """
        ...

    def __enter__(self):
        """
        **LLM Docstring**

        Enter the app context: activate its variable set and default output widget and
        push it onto the app stack (reentrant via a depth counter).

        :return: the app
        :rtype: App
        """
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Exit the app context, restoring the variable set/output widget and popping the app
        stack when fully unwound.

        :param exc_type: the exception type, if any
        :param exc_val: the exception value, if any
        :param exc_tb: the traceback, if any
        """
        ...

    @property
    def body(self):
        """
        **LLM Docstring**

        The app's body component, constructed lazily (within the app context) from the
        supplied body spec on first access. The setter resets the cached component.

        :return: the body component
        """
        ...

    @body.setter
    def body(self, b):
        """
        **LLM Docstring**

        The app's body component, constructed lazily (within the app context) from the
        supplied body spec on first access. The setter resets the cached component.

        :return: the body component
        """
        ...

    @property
    def header(self):
        """
        **LLM Docstring**

        The app's header component, constructed lazily (within the app context) from the
        supplied header spec on first access. The setter resets the cached component.

        :return: the header component
        """
        ...

    @header.setter
    def header(self, h):
        """
        **LLM Docstring**

        The app's header component, constructed lazily (within the app context) from the
        supplied header spec on first access. The setter resets the cached component.

        :return: the header component
        """
        ...

    @property
    def sidebar(self):
        """
        **LLM Docstring**

        The app's sidebar component, constructed lazily (within the app context) from the
        supplied sidebar spec on first access. The setter resets the cached component.

        :return: the sidebar component
        """
        ...

    @sidebar.setter
    def sidebar(self, s):
        """
        **LLM Docstring**

        The app's sidebar component, constructed lazily (within the app context) from the
        supplied sidebar spec on first access. The setter resets the cached component.

        :return: the sidebar component
        """
        ...

    @property
    def toolbar(self):
        """
        **LLM Docstring**

        The app's toolbar component, constructed lazily (within the app context) from the
        supplied toolbar spec on first access. The setter resets the cached component.

        :return: the toolbar component
        """
        ...

    @toolbar.setter
    def toolbar(self, t):
        """
        **LLM Docstring**

        The app's toolbar component, constructed lazily (within the app context) from the
        supplied toolbar spec on first access. The setter resets the cached component.

        :return: the toolbar component
        """
        ...

    @property
    def footer(self):
        """
        **LLM Docstring**

        The app's footer component, constructed lazily (within the app context) from the
        supplied footer spec on first access. The setter resets the cached component.

        :return: the footer component
        """
        ...

    @footer.setter
    def footer(self, f):
        """
        **LLM Docstring**

        The app's footer component, constructed lazily (within the app context) from the
        supplied footer spec on first access. The setter resets the cached component.

        :return: the footer component
        """
        ...

    @classmethod
    def prep_head_item(cls, item):
        """
        **LLM Docstring**

        Coerce a `(label, callback)` head item into a `Button`.

        :param item: the head item
        :return: the prepared item
        """
        ...

    @classmethod
    def construct_navbar_item(cls, item):
        """
        **LLM Docstring**

        Coerce a navbar item spec into a component: a `(label, sub-items)` pair becomes a
        `Dropdown`, a `(label, callback)` pair becomes a `Button`.

        :param item: the navbar item spec
        :return: the navbar item
        """
        ...

    def construct_header(self, header, **opts):
        """
        **LLM Docstring**

        Build the header `Navbar` from its spec (a list, a `(spec, opts)` pair, or an
        `items` dict), theming it.

        :param header: the header spec
        :param opts: extra navbar options
        :return: the header component
        """
        ...

    def construct_footer(self, footer, **opts):
        """
        **LLM Docstring**

        Build the footer `Navbar` from its spec, theming it.

        :param footer: the footer spec
        :param opts: extra navbar options
        :return: the footer component
        """
        ...

    def construct_sidebar_item(self, item):
        """
        **LLM Docstring**

        Coerce a sidebar item spec into an `Opener` (nesting sub-`Sidebar`s for grouped
        items).

        :param item: the sidebar item spec
        :return: the sidebar item
        """
        ...

    def construct_sidebar(self, sidebar, **opts):
        """
        **LLM Docstring**

        Build the `Sidebar` from its spec (a list, a `(spec, opts)` pair, or an `items`
        dict), theming it.

        :param sidebar: the sidebar spec
        :param opts: extra sidebar options
        :return: the sidebar component
        """
        ...

    def construct_toolbar_item(self, item):
        """
        **LLM Docstring**

        Coerce a toolbar item spec (a control settings dict) into a `Control`.

        :param item: the toolbar item spec
        :return: the toolbar item
        """
        ...

    def construct_toolbar(self, toolbar, **opts):
        """
        **LLM Docstring**

        Build the toolbar from its spec, as a `Grid` (for a list of rows) or a `Div`,
        theming it.

        :param toolbar: the toolbar spec
        :param opts: extra toolbar options
        :return: the toolbar component
        """
        ...

    def wrap_body(self, fn, **styles):
        """
        **LLM Docstring**

        Wrap a function as a `FunctionDisplay` bound to the app's variables.

        :param fn: the function
        :type fn: Callable
        :param styles: extra display styles
        :return: the function display
        :rtype: FunctionDisplay
        """
        ...

    def construct_body_item(self, item):
        """
        **LLM Docstring**

        Coerce a body item into a component: wrap functions as `FunctionDisplay`s and
        `(content, styles)` pairs as displays/spans, passing existing components through.

        :param item: the body item spec
        :return: the body item
        """
        ...

    def construct_body(self, body):
        """
        **LLM Docstring**

        Build the body from its spec: a dict becomes `Tabs`, a list becomes a list of
        bodies, else a single body item.

        :param body: the body spec
        :return: the body component(s)
        """
        ...

    def construct_layout(self):
        """
        **LLM Docstring**

        Assemble the app's `Grid` layout from its header/sidebar/toolbar/body/output/footer
        sections, computing the row/column spans and sizes.

        :return: the layout grid
        :rtype: Grid
        :raises NotImplementedError: for an unsupported layout style
        """
        ...

    def to_jhtml(self):
        """
        **LLM Docstring**

        Render the app to its JHTML element (via the constructed layout).

        :return: the JHTML element
        """
        ...

class SettingsPane(App):
    themes = {'primary': App.merge_themes(App.themes['primary'], {'toolbar': dict(cls=['form-check'])})}

    def __init__(self, settings, cls=None, **opts):
        """
        **LLM Docstring**

        An `App` specialized to display a set of controls as a form toolbar.

        :param settings: the control settings (used as the toolbar)
        :param cls: the root CSS classes
        :param opts: extra `App` options
        """
        ...
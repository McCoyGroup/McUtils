
__all__ = [
    "App",
    "SettingsPane",
    "Manipulator",
]

import types, typing

import numpy as np

from ..JHTML import JHTML, DefaultOutputWidget#, HTML, ActiveHTMLWrapper
from .Interfaces import *
from .Controls import Control, FunctionDisplay
from .Variables import WidgetControl, InterfaceVars, DefaultVars

# NonPrimitiveInterfaceType = typing.Union[
#     HTMLableType,
#     WidgetableType,
#     Component,
#     typing.Tuple[
#         typing.Union[
#             HTMLableType,
#             WidgetableType,
#             Component
#         ],
#         typing.Mapping
#     ]
# ]


__reload_hook__ = ['..JHTML', '.Interfaces', '.Controls', '.Variables']

# class FunctionDisplay:
#     def __init__(self, func, vars):
#         self.func = func
#         self.vars = vars
#         self.output = JupyterAPIs.get_widgets_api().Output()
#         self.update = self.update # a weird kluge to prevent a weakref issue...
#     def display(self):
#         self.output.clear_output()
#         with self.output:
#             res = self.func(**{x.name: x.value for x in self.vars})
#             if res is not None:
#                 JupyterAPIs.get_display_api().display(res)
#     def update(self, *ignored_settings):
#         return self.display()
#     def to_widget(self):
#         for v in self.vars:
#             v.callbacks.add(self.update)
#         return self.output
class Manipulator(Card):

    theme = Card.merge_themes(
        Card.theme,
        {
            'controls': {},
            'output': {}
        }
    )
    def __init__(self, func, *controls, debounce=None, autoclear=True, namespace=None,
                 layout_function=None,
                 control_layout_function=None,
                 **etc):
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
        super().__init__(**etc)
        if namespace is None:
            namespace = InterfaceVars.unique_namespace()
        self.controls = [self.canonicalize_control(c, namespace=namespace) for c in controls]
        vars = [c.var for c in self.controls]
        self.output = FunctionDisplay(func, vars, debounce=debounce, autoclear=autoclear,
                                      namespace=namespace,
                                      **self.theme.get('output', {}))
        if control_layout_function is None:
            control_layout_function = self.default_control_layout
        self.control_panel = control_layout_function(self)
        if layout_function is None:
            layout_function = self.default_layout
        self.component_args['body'] = layout_function(self)
    @classmethod
    def default_layout(cls, self):
        return (Flex(
            [
                self.output,
                self.control_panel
            ],
            direction='column'
        ),)
    @classmethod
    def default_control_layout(cls, self):
        return Flex(self.controls, direction='column', **self.theme.get('controls', {}))
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
        if isinstance(settings, (WidgetControl, Control)):
            return settings
        else:
            var, settings = settings
            if not isinstance(settings, dict):
                if isinstance(settings, (list, tuple)) and isinstance(settings[0], (int, float, np.integer, np.floating)):
                    settings = {'range':settings}
                else:
                    settings = {'value':settings}
            if namespace is not None:
                settings['namespace'] = settings.get('namespace', namespace)
            # try:
            control = Control.construct(var, **settings)
            # except:
            #     control = WidgetControl(var, **settings)

            return control
    def initialize(self):
        """
        **LLM Docstring**

        Run the function once (with no event) to populate the output.
        """
        self.output.update(None)

class App(Component):
    """
    Provides a framework for making Jupyter Apps with the
    elements built out in the Interfaces package
    """
    _app_stack=[]
    themes = {
        'primary':{
            'header':{
                'wrapper': {'cls': ['navbar-dark', 'bg-secondary', 'border-bottom']}
            },
            'toolbar':{'cls':['form-check', 'bg-light', 'border-bottom']},
            'sidebar':{
                'classes':['bg-light', 'border-end', 'h-100'],
                'styles':{},
                'opener':{
                    'header':{
                        'cls':['pt-0', 'bg-light'],
                        'border_top':'1px solid rgb(240, 240, 240)'
                    },
                    'body': {
                        'cls':['ps-0', 'pe-0']
                    }
                },
                'body':{
                    'wrapper':{'cls':['bg-light', 'border-end', 'h-100']}
                }
            },
            'footer':{
                 'wrapper': {'cls': ['navbar-light', 'bg-light', 'border-top']}
            }
        }
    }
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
        new = theme_1.copy()
        for k in theme_2:
            if k in new and isinstance(new[k], dict):
                new[k] = cls.merge_themes(new[k], theme_2[k])
            else:
                new[k] = theme_2[k]
        return new


    def __init__(self,
                 body=None,
                 header=None,
                 footer=None,
                 sidebar=None,
                 toolbar=None,
                 theme='primary',
                 layout='grid',
                 cls='app border',
                 output=None,
                 capture_output=None,
                 namespace=None,
                 vars=None,
                 **attrs
                 ):
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
        self._parent = None if len(self._app_stack) == 0 else self._app_stack[-1]
        super().__init__()
        self.vars = DefaultVars.resolve() if vars is None else vars
        self.output = JHTML.OutputArea(autoclear=True) if output is None else output
        self.capture_output = self._parent is None if capture_output is None else capture_output
        self.theme = self.themes[theme] if isinstance(theme, str) else self.merge_themes(self.themes['primary'], theme)
        self._body = [None, body]
        self._header = [None, header]
        self._footer = [None, footer]
        self._sidebar = [None, sidebar]
        self._toolbar = [None, toolbar]
        self.layout = layout
        self.cls = cls
        self.attrs = attrs
        self._out = None
        self._vv = None
        self._stack_depth = 0
    def __enter__(self):
        """
        **LLM Docstring**

        Enter the app context: activate its variable set and default output widget and
        push it onto the app stack (reentrant via a depth counter).

        :return: the app
        :rtype: App
        """
        if self._stack_depth == 0:
            self._vv = DefaultVars(self.vars)
            self._vv.__enter__()
            self._out = DefaultOutputWidget(self.output)
            self._out.__enter__()
            self._app_stack.append(self)
        self._stack_depth += 1
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Exit the app context, restoring the variable set/output widget and popping the app
        stack when fully unwound.

        :param exc_type: the exception type, if any
        :param exc_val: the exception value, if any
        :param exc_tb: the traceback, if any
        """
        self._stack_depth -= max(0, self._stack_depth - 1)
        if self._stack_depth == 0:
            self._vv.__exit__(exc_type, exc_val, exc_tb)
            self._vv = None
            self._out.__exit__(exc_type, exc_val, exc_tb)
            self._out = None
            self._app_stack.remove(self)
    @property
    def body(self):
        """
        **LLM Docstring**

        The app's body component, constructed lazily (within the app context) from the
        supplied body spec on first access. The setter resets the cached component.

        :return: the body component
        """
        if self._body[1] is not None:
            if self._body[0] is None:
                with self:
                    self._body[0] = self.construct_body(self._body[1])
        return self._body[0]
    @body.setter
    def body(self, b):
        """
        **LLM Docstring**

        The app's body component, constructed lazily (within the app context) from the
        supplied body spec on first access. The setter resets the cached component.

        :return: the body component
        """
        self._body = [None, b]
    @property
    def header(self):
        """
        **LLM Docstring**

        The app's header component, constructed lazily (within the app context) from the
        supplied header spec on first access. The setter resets the cached component.

        :return: the header component
        """
        if self._header[1] is not None:
            if self._header[0] is None:
                with self:
                    self._header[0] = self.construct_header(self._header[1])
        return self._header[0]
    @header.setter
    def header(self, h):
        """
        **LLM Docstring**

        The app's header component, constructed lazily (within the app context) from the
        supplied header spec on first access. The setter resets the cached component.

        :return: the header component
        """
        self._header = [None, h]
    @property
    def sidebar(self):
        """
        **LLM Docstring**

        The app's sidebar component, constructed lazily (within the app context) from the
        supplied sidebar spec on first access. The setter resets the cached component.

        :return: the sidebar component
        """
        if self._sidebar[1] is not None:
            if self._sidebar[0] is None:
                with self:
                    self._sidebar[0] = self.construct_sidebar(self._sidebar[1])
        return self._sidebar[0]
    @sidebar.setter
    def sidebar(self, s):
        """
        **LLM Docstring**

        The app's sidebar component, constructed lazily (within the app context) from the
        supplied sidebar spec on first access. The setter resets the cached component.

        :return: the sidebar component
        """
        self._sidebar = [None, s]
    @property
    def toolbar(self):
        """
        **LLM Docstring**

        The app's toolbar component, constructed lazily (within the app context) from the
        supplied toolbar spec on first access. The setter resets the cached component.

        :return: the toolbar component
        """
        if self._toolbar[1] is not None:
            if self._toolbar[0] is None:
                with self:
                    self._toolbar[0] = self.construct_toolbar(self._toolbar[1])
        return self._toolbar[0]
    @toolbar.setter
    def toolbar(self, t):
        """
        **LLM Docstring**

        The app's toolbar component, constructed lazily (within the app context) from the
        supplied toolbar spec on first access. The setter resets the cached component.

        :return: the toolbar component
        """
        self._toolbar = [None, t]
    @property
    def footer(self):
        """
        **LLM Docstring**

        The app's footer component, constructed lazily (within the app context) from the
        supplied footer spec on first access. The setter resets the cached component.

        :return: the footer component
        """
        if self._footer[1] is not None:
            if self._footer[0] is None:
                with self:
                    self._footer[0] = self.construct_footer(self._footer[1])
        return self._footer[0]
    @footer.setter
    def footer(self, f):
        """
        **LLM Docstring**

        The app's footer component, constructed lazily (within the app context) from the
        supplied footer spec on first access. The setter resets the cached component.

        :return: the footer component
        """
        self._footer = [None, f]
    @classmethod
    def prep_head_item(cls, item):
        """
        **LLM Docstring**

        Coerce a `(label, callback)` head item into a `Button`.

        :param item: the head item
        :return: the prepared item
        """
        if (
                isinstance(item, (tuple, list))
                and len(item) == 2
                and isinstance(item[1], (types.FunctionType, types.MethodType))
        ):
            item = Button(*item)
        return item
    @classmethod
    def construct_navbar_item(cls, item):
        """
        **LLM Docstring**

        Coerce a navbar item spec into a component: a `(label, sub-items)` pair becomes a
        `Dropdown`, a `(label, callback)` pair becomes a `Button`.

        :param item: the navbar item spec
        :return: the navbar item
        """
        if isinstance(item, dict) and len(item) == 1 and 'body' not in item:
            for item in item.items():
                item = tuple(item)
        if isinstance(item, (tuple, list)) and len(item) == 2:
            k,v = item
            if isinstance(v, (tuple, list, dict)):
                v = tuple(cls.prep_head_item(i) for i in v)
                item = {'raw':Dropdown(k, v)}
            elif isinstance(v, (types.FunctionType, types.MethodType)):
                item = Button(k, v)
        return item
    def construct_header(self, header, **opts):
        """
        **LLM Docstring**

        Build the header `Navbar` from its spec (a list, a `(spec, opts)` pair, or an
        `items` dict), theming it.

        :param header: the header spec
        :param opts: extra navbar options
        :return: the header component
        """
        if isinstance(header, tuple) and len(header) == 2 and isinstance(header[1], dict):
            opts = dict(header[1], **opts)
            header = header[0]
        elif isinstance(header, dict):
            header = header.copy()
            sb = header['items']
            del header['items']
            opts = dict(header, **opts)
            header = sb
        elif not (isinstance(header, (list, tuple, Component)) or hasattr(header, 'to_widget') or hasattr(header, 'to_tree')):
            header = [header]
        if isinstance(header, (list, tuple)):
            header = Navbar(
                [self.construct_navbar_item(h) for h in header],
                **dict({'theme':self.theme['header']}, **opts)
            )
        # elif isinstance(header, str):
        #     header = ...
        # elif isinstance(header, (HTML.XMLElement, ActiveHTMLWrapper)):
        #     ...
        return header
    def construct_footer(self, footer, **opts):
        """
        **LLM Docstring**

        Build the footer `Navbar` from its spec, theming it.

        :param footer: the footer spec
        :param opts: extra navbar options
        :return: the footer component
        """
        if isinstance(footer, tuple) and len(footer) == 2 and isinstance(footer[1], dict):
            opts = dict(footer[1], **opts)
            footer = footer[0]
        elif isinstance(footer, dict):
            footer = footer.copy()
            sb = footer['items']
            del footer['items']
            opts = dict(footer, **opts)
            footer = sb
        elif not (isinstance(footer, (list, tuple, Component)) or hasattr(footer, 'to_widget') or hasattr(footer, 'to_tree')):
            footer = [footer]
        if isinstance(footer, (list, tuple)):
            footer = Navbar(
                footer,
                **dict({'theme':self.theme['footer']}, **opts)
            )
        return footer
    def construct_sidebar_item(self, item):
        """
        **LLM Docstring**

        Coerce a sidebar item spec into an `Opener` (nesting sub-`Sidebar`s for grouped
        items).

        :param item: the sidebar item spec
        :return: the sidebar item
        """
        if isinstance(item, tuple):
            if isinstance(item[0], tuple) and len(item[0]) == 2:
                items = []
                for k,v in item:
                    if isinstance(v, tuple):
                        v = Sidebar([self.construct_sidebar_item(h) for h in v])
                    items.append((k, v))
                item = dict(body=Opener(items, theme=self.theme['sidebar']['opener']['header']), theme=self.theme['sidebar']['opener']['body'])
            else:
                k,v = item
                if isinstance(v, tuple):
                    v = Sidebar([self.construct_sidebar_item(h) for h in v])
                item = dict(body=Opener(((k, v),), theme=self.theme['sidebar']['opener']['header']), theme=self.theme['sidebar']['opener']['body'])
        return item
    def construct_sidebar(self, sidebar, **opts):
        """
        **LLM Docstring**

        Build the `Sidebar` from its spec (a list, a `(spec, opts)` pair, or an `items`
        dict), theming it.

        :param sidebar: the sidebar spec
        :param opts: extra sidebar options
        :return: the sidebar component
        """
        if isinstance(sidebar, tuple) and len(sidebar) == 2 and isinstance(sidebar[1], dict):
            opts = dict(sidebar[1], **opts)
            sidebar = sidebar[0]
        elif isinstance(sidebar, dict):
            sidebar = sidebar.copy()
            sb = sidebar['items']
            del sidebar['items']
            opts = dict(sidebar, **opts)
            sidebar = sb
        elif not (isinstance(sidebar, (list, tuple, Component)) or hasattr(sidebar, 'to_widget') or hasattr(sidebar, 'to_tree')):
            sidebar = [sidebar]
        if isinstance(sidebar, (list, tuple)):
            sidebar = Sidebar(
                [self.construct_sidebar_item(h) for h in sidebar],
                **dict({'theme':self.theme['sidebar']['body']}, **opts)
            )
        return sidebar

    def construct_toolbar_item(self, item):
        """
        **LLM Docstring**

        Coerce a toolbar item spec (a control settings dict) into a `Control`.

        :param item: the toolbar item spec
        :return: the toolbar item
        """
        if isinstance(item, dict):
            item = item.copy()
            var = item['var']
            del item['var']
            item = Control.construct(var, **item)
        return item
    def construct_toolbar(self, toolbar, **opts):
        """
        **LLM Docstring**

        Build the toolbar from its spec, as a `Grid` (for a list of rows) or a `Div`,
        theming it.

        :param toolbar: the toolbar spec
        :param opts: extra toolbar options
        :return: the toolbar component
        """
        if not (isinstance(toolbar, (list, tuple, Component)) or hasattr(toolbar, 'to_widget') or hasattr(toolbar, 'to_tree')):
            toolbar = [toolbar]
        if isinstance(toolbar, (list, tuple)):
            if isinstance(toolbar[0], (list, tuple)):
                toolbar = Grid(
                    [[self.construct_toolbar_item(h) for h in row] for row in toolbar],
                    **dict(self.theme['toolbar'], **opts)
                )
            else:
                toolbar = JHTML.Div(
                    [self.construct_toolbar_item(h) for h in toolbar],
                    **dict(self.theme['toolbar'], **opts)
                )
        return toolbar

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
        # @functools.wraps(fn)
        # def wrapper(event=None, pane=None, **vars):
        #     return fn(event=event, pane=pane, **vars)
        return FunctionDisplay(fn, self.vars, **styles)
    def construct_body_item(self, item):
        """
        **LLM Docstring**

        Coerce a body item into a component: wrap functions as `FunctionDisplay`s and
        `(content, styles)` pairs as displays/spans, passing existing components through.

        :param item: the body item spec
        :return: the body item
        """
        if isinstance(item, (types.MethodType, types.FunctionType, types.LambdaType)):
            item = self.wrap_body(item)
        elif not isinstance(item, (str, Component, JHTML.Styled)) and not (hasattr(item, 'to_string') or hasattr(item, 'to_jhtml')):
            try:
                item, styles = item
            except (ValueError, TypeError):
                pass
            else:
                if isinstance(item, (types.MethodType, types.FunctionType, types.LambdaType)):
                    item = self.wrap_body(item, **styles)
                else:
                    item = JHTML.Span(item, **styles)
        return item
    def construct_body(self, body):
        """
        **LLM Docstring**

        Build the body from its spec: a dict becomes `Tabs`, a list becomes a list of
        bodies, else a single body item.

        :param body: the body spec
        :return: the body component(s)
        """
        if isinstance(body, dict):
            body = Tabs({k:self.construct_body_item(b) for k,b in body.items()})
        elif isinstance(body, (list, tuple)):
            body = [self.construct_body(b) for b in body]
        else:
            body = self.construct_body_item(body)
        return body

    def construct_layout(self):
        """
        **LLM Docstring**

        Assemble the app's `Grid` layout from its header/sidebar/toolbar/body/output/footer
        sections, computing the row/column spans and sizes.

        :return: the layout grid
        :rtype: Grid
        :raises NotImplementedError: for an unsupported layout style
        """
        with self:
            if self.layout == 'grid':
                elements = []
                nrows = 0
                ncols = 0

                # if self.header is not None:
                #     nrows += 1
                if self.sidebar is not None:
                    ncols += 1
                if self.toolbar is not None:
                    nrows += 1
                    ncols += 1
                if self.capture_output:
                    nrows += 1
                if self.body is not None:
                    nrows += 1 if not isinstance(self.body, list) else len(self.body)
                    ncols = min(ncols+1, 2)
                # if self.footer is not None:
                #     nrows += 1

                column_width = []
                row_height = []
                if self.header is not None:
                    header = []
                    header.append(Grid.Item(self.header, col_span=ncols))
                    elements.append(header)
                    row_height.append('auto')

                body = []
                if self.sidebar is not None:
                    body.append(Grid.Item(self.sidebar, row_span=nrows))
                    column_width.append('auto')
                if self.toolbar is not None:
                    body.append(self.toolbar)
                    elements.append(body)
                    if self.sidebar is not None:
                        body = [None]
                    else:
                        body = []
                    row_height.append('auto')
                if isinstance(self.body, (list, tuple)):
                    for i,b in enumerate(self.body):
                        body.append(b)
                        if i == 0:
                            row_height.append('1fr')
                            column_width.append('1fr')
                        else:
                            row_height.append('auto')
                        elements.append(body)
                        if self.sidebar is not None:
                            body = [None]
                        else:
                            body = []
                else:
                    body.append(self.body)
                    row_height.append('1fr')
                    column_width.append('1fr')
                    elements.append(body)

                if self.capture_output:
                    output_list = []
                    if self.sidebar is not None:
                        output_list.append(None)
                    output_list.append(Grid.Item(self.output))
                    elements.append(output_list)
                    row_height.append('auto')

                if self.footer is not None:
                    footer = []
                    footer.append(Grid.Item(self.footer, col_span=ncols))
                    elements.append(footer)
                    row_height.append('auto')

                layout = Grid(
                    elements,
                    column_width=column_width,
                    row_height=row_height,
                    cls=self.cls,
                    **self.attrs
                )
            else:
                raise NotImplementedError("ugh")
        return layout

    def to_jhtml(self):
        """
        **LLM Docstring**

        Render the app to its JHTML element (via the constructed layout).

        :return: the JHTML element
        """
        return self.construct_layout().to_jhtml()
class SettingsPane(App):
    themes = {
        'primary': App.merge_themes(
            App.themes['primary'],
            {'toolbar': dict(cls=['form-check'])}
        )
    }
    def __init__(self, settings, cls=None, **opts):
        """
        **LLM Docstring**

        An `App` specialized to display a set of controls as a form toolbar.

        :param settings: the control settings (used as the toolbar)
        :param cls: the root CSS classes
        :param opts: extra `App` options
        """
        super().__init__(
            toolbar=settings,
            cls=cls,
            **opts
        )
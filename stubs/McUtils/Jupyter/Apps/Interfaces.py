import abc, weakref, uuid, traceback as tb
import sys
import threading
from .types import *
from ...Misc import mixedmethod
from ..JHTML import JHTML, DefaultOutputWidget
from ..JHTML.WidgetTools import JupyterAPIs, frozendict

class JHTMLConversionError(Exception):
    """
    Represents an error in converting to JHTML
    """

    def __init__(self, widgets, cause, tb, message='failed to convert to JHTML:\n{}'):
        """
        **LLM Docstring**

        Wrap the failure to convert a component chain to JHTML, capturing the widget
        chain and the underlying cause/traceback.

        :param widgets: the chain of widgets involved
        :param cause: the underlying exception
        :param tb: the underlying traceback
        :param message: the message template
        :type message: str
        """
        ...

    def format_message(self, limit=10):
        """
        **LLM Docstring**

        Format the error message: the widget chain plus the (length-limited) underlying
        traceback.

        :param limit: the traceback depth limit
        :type limit: int
        :return: the formatted message
        :rtype: str
        """
        ...
__all__ = ['WidgetInterface', 'GenericDisplay', 'DelayedResult', 'Component', 'WrapperComponent', 'Container', 'MenuComponent', 'ListGroup', 'Button', 'LinkButton', 'Spinner', 'Progress', 'ButtonGroup', 'Navbar', 'Carousel', 'Pagination', 'Sidebar', 'Dropdown', 'DropdownList', 'Tabs', 'TabPane', 'TabList', 'Accordion', 'AccordionHeader', 'AccordionBody', 'Opener', 'OpenerHeader', 'OpenerBody', 'CardOpener', 'Modal', 'ModalHeader', 'ModalBody', 'ModalFooter', 'Offcanvas', 'OffcanvasHeader', 'OffcanvasBody', 'Toast', 'ToastBody', 'ToastHeader', 'ToastContainer', 'Spacer', 'Breadcrumb', 'Card', 'CardHeader', 'CardBody', 'CardFooter', 'ModifierComponent', 'Tooltip', 'Popover', 'Layout', 'Grid', 'Table', 'Flex']
__reload_hook__ = ['..JHTML', '..WidgetTools']

class WidgetInterface(metaclass=abc.ABCMeta):
    """
    Provides the absolute minimum necessary for hooking
    an interface that creates an `ipywidget` into the
    Jupyter display runtime
    """

    @abc.abstractmethod
    def to_widget(self):
        """
        **LLM Docstring**

        Abstract: render this interface to an `ipywidget`.

        :return: the widget
        """
        ...

    def initialize(self):
        """
        **LLM Docstring**

        Hook run after display; overridable for post-display setup (no-op by default).
        """
        ...

    def _ipython_display_(self):
        """
        **LLM Docstring**

        Display the interface's widget in IPython, then run `initialize`.
        """
        ...

    @classmethod
    def _get_boostrap_links(cls):
        """
        **LLM Docstring**

        Return the Bootstrap CSS/JS `<link>`/`<script>` elements for static HTML.

        :return: the link/script elements
        :rtype: list
        """
        ...

    def to_static_html(self, include_bootstrap=True, create_body=True):
        """
        **LLM Docstring**

        Render the interface to static HTML, optionally embedding the Bootstrap links and
        wrapping it in a full document.

        :param include_bootstrap: embed the Bootstrap links
        :type include_bootstrap: bool
        :param create_body: wrap in a full `<html><body>` document
        :type create_body: bool
        :return: the static HTML element
        :raises ValueError: if the widget can't reduce to static HTML
        """
        ...
    _display_locks = set()

    def display(self):
        """
        **LLM Docstring**

        Display the interface (guarded against re-entrant display calls).
        """
        ...

    def get_mime_bundle(self):
        """
        **LLM Docstring**

        Return the widget's MIME bundle for rich display.

        :return: the MIME bundle
        :rtype: dict
        """
        ...

    @mixedmethod
    def _ipython_pinfo_(self):
        """
        **LLM Docstring**

        Provide IPython's rich `?` documentation for the interface (via `jdoc`).

        :return: the documentation
        """
        ...

class Component(WidgetInterface):
    """
    Provides an abstract base class for an interface element
    to allow for the easy construction of interesting interfaces
    """

    def __init__(self, dynamic=True, debug_pane=None, **attrs):
        """
        **LLM Docstring**

        Base interface component holding its attributes, parent links, and widget cache.

        :param dynamic: build a dynamic (reactive) widget
        :type dynamic: bool
        :param debug_pane: the output pane for construction errors
        :param attrs: the component attributes
        """
        ...

    @property
    def attrs(self):
        """
        **LLM Docstring**

        The component's attributes (as an immutable mapping). The setter replaces the
        attribute dict.

        :return: the attributes
        :rtype: frozendict
        """
        ...

    @attrs.setter
    def attrs(self, value):
        """
        **LLM Docstring**

        The component's attributes (as an immutable mapping). The setter replaces the
        attribute dict.

        :return: the attributes
        :rtype: frozendict
        """
        ...

    def get_attr(self, key):
        """
        **LLM Docstring**

        Get an attribute by key.

        :param key: the attribute name
        :return: the value
        """
        ...

    def get_child(self, key):
        """
        **LLM Docstring**

        Get a child by key (unsupported on the base component).

        :param key: the child index
        :raises NotImplementedError: on components without children
        """
        ...

    def __getitem__(self, item):
        """
        **LLM Docstring**

        Get an attribute (string key) or a child (other key).

        :param item: the key
        :return: the attribute value or child
        """
        ...

    def set_attr(self, key, value):
        """
        **LLM Docstring**

        Set an attribute in the component's attribute dict.

        :param key: the attribute name
        :param value: the value
        """
        ...

    def update_widget_attr(self, key, value):
        """
        **LLM Docstring**

        Push an attribute change into the live widget cache.

        :param key: the attribute name
        :param value: the value
        """
        ...

    def set_child(self, which, new):
        """
        **LLM Docstring**

        Set a child (unsupported on the base component).

        :param which: the child index
        :param new: the new child
        :raises NotImplementedError: on components without children
        """
        ...

    def update_widget_child(self, key, value):
        """
        **LLM Docstring**

        Push a child change into the live widget cache.

        :param key: the child index
        :param value: the new child
        """
        ...

    def __setitem__(self, key, value):
        """
        **LLM Docstring**

        Set an attribute (string key) or child (other key), syncing the widget cache.

        :param key: the key
        :param value: the value
        """
        ...

    def del_attr(self, key):
        """
        **LLM Docstring**

        Delete an attribute from the attribute dict.

        :param key: the attribute name
        """
        ...

    def del_widget_attr(self, key):
        """
        **LLM Docstring**

        Delete an attribute from the live widget cache.

        :param key: the attribute name
        """
        ...

    def del_child(self, which):
        """
        **LLM Docstring**

        Delete a child (unsupported on the base component).

        :param which: the child index
        :raises NotImplementedError: on components without children
        """
        ...

    def del_widget_child(self, key):
        """
        **LLM Docstring**

        Delete a child from the live widget cache.

        :param key: the child index
        """
        ...

    def __delitem__(self, key):
        """
        **LLM Docstring**

        Delete an attribute (string key) or child (other key), syncing the widget cache.

        :param key: the key
        """
        ...

    def insert(self, where, new):
        """
        **LLM Docstring**

        Insert a new child at a position, syncing the widget cache.

        :param where: the insertion index
        :param new: the child to insert
        """
        ...

    def append(self, child):
        """
        **LLM Docstring**

        Append a child to the end.

        :param child: the child to append
        """
        ...

    def insert_child(self, where, child):
        """
        **LLM Docstring**

        Insert a child (unsupported on the base component).

        :param where: the index
        :param child: the child
        :raises NotImplementedError: on components without children
        """
        ...

    def insert_widget_child(self, where, child):
        """
        **LLM Docstring**

        Insert a child into the live widget cache.

        :param where: the index
        :param child: the child
        """
        ...

    def add_class(self, *cls):
        """
        **LLM Docstring**

        Add CSS class(es) to the component (and the live widget).

        :param cls: the class name(s)
        """
        ...

    def add_component_class(self, *cls):
        """
        **LLM Docstring**

        Add CSS class(es) to the component's stored attributes.

        :param cls: the class name(s)
        """
        ...

    def add_widget_class(self, *cls):
        """
        **LLM Docstring**

        Add CSS class(es) to the live widget.

        :param cls: the class name(s)
        """
        ...

    def remove_class(self, *cls):
        """
        **LLM Docstring**

        Remove CSS class(es) from the component (and the live widget).

        :param cls: the class name(s)
        """
        ...

    def remove_component_class(self, *cls):
        """
        **LLM Docstring**

        Remove CSS class(es) from the component's stored attributes.

        :param cls: the class name(s)
        """
        ...

    def remove_widget_class(self, *cls):
        """
        **LLM Docstring**

        Remove CSS class(es) from the live widget.

        :param cls: the class name(s)
        """
        ...

    @abc.abstractmethod
    def to_jhtml(self, parent=None):
        """
        **LLM Docstring**

        Abstract: render the component to its JHTML element.

        :param parent: the parent component
        :return: the JHTML element
        """
        ...

    def to_widget(self, parent=None):
        """
        **LLM Docstring**

        Render the component to a widget (cached), registering the parent and wrapping any
        conversion failure as a `JHTMLConversionError`.

        :param parent: the parent component
        :return: the widget
        :raises JHTMLConversionError: if conversion fails
        """
        ...

    def mutate(self, fn):
        """
        **LLM Docstring**

        Apply a mutation function to the component and invalidate its cached widget.

        :param fn: the mutation callback
        :type fn: Callable
        """
        ...

    def invalidate_cache(self):
        """
        **LLM Docstring**

        Invalidate the cached widget (and propagate the invalidation to parents).
        """
        ...

class WrapperComponent(Component):
    """
    Extends the base component interface to allow for the
    construction of interesting compound interfaces (using `JHTML.Compound`).
    Takes a `dict` of `wrappers` naming the successive levels of the interface
    along with a `theme` that provides style declarations for each level.

    Used primarily to create `Bootstrap`-based interfaces.
    """
    wrappers = dict(wrapper=JHTML.Div)
    theme = dict(wrapper={'cls': []})

    def __init__(self, items: ElementType, wrappers=None, theme=None, extend_base_theme=True, **attrs):
        """
        **LLM Docstring**

        A component that renders its items inside one or more themed wrapper elements
        (the basis for Bootstrap interfaces).

        :param items: the wrapped items
        :param wrappers: the named wrapper element classes
        :type wrappers: dict | None
        :param theme: the per-wrapper style theme
        :type theme: dict | None
        :param extend_base_theme: merge with the class's base theme
        :type extend_base_theme: bool
        :param attrs: extra attributes (merged into the outer wrapper's theme)
        """
        ...

    def handle_variants(self, theme):
        """
        **LLM Docstring**

        Expand a theme's `variant`/`base-cls` shorthand into the concrete
        `base-cls-variant` CSS class.

        :param theme: the theme
        :type theme: dict
        :return: the expanded theme
        :rtype: dict
        """
        ...

    def manage_theme(self, theme, extend_base_theme=True):
        """
        **LLM Docstring**

        Resolve the effective theme, optionally merging it over the class's base theme.

        :param theme: the supplied theme (the class theme if `None`)
        :param extend_base_theme: merge with the base theme
        :type extend_base_theme: bool
        :return: the resolved theme
        :rtype: dict
        """
        ...

    @classmethod
    def merge_themes(cls, theme: 'None|dict', attrs: dict, merge_keys=('cls',)):
        """
        Needs to handle cases where a `theme` is provided
        which includes things like `cls` declarations and then the
        `attrs` may also include `cls` declarations and the `attrs`
        declarations get appended to the theme
        """
        ...

    @classmethod
    def _check_is_widget_class(cls, el):
        """
        **LLM Docstring**

        Test whether an object is an ipywidgets `Widget`.

        :param el: the object
        :return: whether it's a widget
        :rtype: bool
        """
        ...

    @classmethod
    def manage_items(cls, items, attrs):
        """
        **LLM Docstring**

        Normalize the items spec into a `(items_list, attrs)` pair, pulling out any
        attribute dict (from a dict body or a `(items, opts)` pair) and wrapping a scalar
        item in a list.

        :param items: the items spec
        :param attrs: the base attributes
        :type attrs: dict
        :return: `(items_list, attrs)`
        :rtype: tuple
        """
        ...

    def get_child(self, key):
        """
        **LLM Docstring**

        Get a wrapped item by index.

        :param key: the item index
        :return: the item
        """
        ...

    def set_child(self, which, new):
        """
        **LLM Docstring**

        Set a wrapped item by index.

        :param which: the item index
        :param new: the new item
        """
        ...

    def insert_child(self, where, child):
        """
        **LLM Docstring**

        Insert a wrapped item at a position (appending if `where` is `None`).

        :param where: the index
        :param child: the item
        """
        ...

    def wrap_items(self, items):
        """
        **LLM Docstring**

        Render the items inside the wrapper element(s), applying the themed attributes.

        :param items: the items to wrap
        :return: the wrapper element
        """
        ...

    def to_jhtml(self, parent=None):
        """
        **LLM Docstring**

        Render the component by wrapping its items.

        :param parent: the parent component
        :return: the JHTML element
        """
        ...

class Container(WrapperComponent):
    """
    Extends the base `WrapperComponent` to include a final
    `items` spec for cases where there is a base wrapper and a set of items,
    e.g. a list group which has the `list-group` outer class and a set of `list-items` inside.
    """
    wrappers = dict(wrapper=JHTML.Div, item=JHTML.Span)
    theme = dict(wrapper={'cls': []}, item={'cls': []})

    def __init__(self, items: ElementType, wrappers: dict=None, **attrs) -> None:
        """
        **LLM Docstring**

        A `WrapperComponent` with an outer wrapper plus a per-item element (e.g. a list
        group with a `list-group` wrapper and `list-item` children).

        :param items: the item bodies
        :param wrappers: the wrapper-plus-item element classes
        :type wrappers: dict | None
        :param attrs: extra attributes
        """
        ...

    @property
    def items(self):
        """
        **LLM Docstring**

        The wrapped items, each built via `create_item`. Assigning is disallowed once
        initialized.

        :return: the built items
        :rtype: list
        """
        ...

    @items.setter
    def items(self, items):
        """
        **LLM Docstring**

        The wrapped items, each built via `create_item`. Assigning is disallowed once
        initialized.

        :return: the built items
        :rtype: list
        """
        ...

    def _create_dict_item(self, body=None, **extra):
        """
        **LLM Docstring**

        Build an item element from a dict body (merging its extra options into the item
        theme).

        :param body: the item body
        :param extra: extra per-item options
        :return: the item element
        """
        ...

    def _create_base_item(self, body):
        """
        **LLM Docstring**

        Build an item element from a bare body using the base item theme.

        :param body: the item body
        :return: the item element
        """
        ...

    def create_item(self, i, **kw):
        """
        **LLM Docstring**

        Build an item element from a spec: pass a `raw` element through, expand a dict
        body, or wrap a bare body.

        :param i: the item spec
        :param kw: extra per-item options
        :return: the item element
        """
        ...

    def update_widget_child(self, key, value):
        """
        **LLM Docstring**

        Rebuild an item and push it into the live widget cache.

        :param key: the item index
        :param value: the new item spec
        """
        ...

    def insert_widget_child(self, where, child):
        """
        **LLM Docstring**

        Build an item and insert it into the live widget cache.

        :param where: the index
        :param child: the item spec
        """
        ...

class ComponentContainer(WrapperComponent):
    components = {}

    def __init__(self, component_args: dict=None, component_kwargs: dict=None, components=None, **attrs):
        """
        **LLM Docstring**

        A `WrapperComponent` whose children are named sub-components built from
        per-component args/kwargs.

        :param component_args: per-component positional args
        :type component_args: dict | None
        :param component_kwargs: per-component keyword args
        :type component_kwargs: dict | None
        :param components: the name-to-class component map
        :type components: dict | None
        :param attrs: extra attributes
        """
        ...

    def create_components(self):
        """
        **LLM Docstring**

        Instantiate the named sub-components from their args/kwargs and per-component
        theme (skipping ones explicitly set to `None`).

        :return: the built sub-components
        :rtype: dict
        """
        ...

    def handle_variants(self, theme):
        """
        **LLM Docstring**

        Pass the theme through unchanged (variants are handled per sub-component).

        :param theme: the theme
        :return: the theme
        """
        ...

    def wrap_items(self, items):
        """
        **LLM Docstring**

        Build the sub-components and wrap them in the outer element.

        :param items: ignored (components are built internally)
        :return: the wrapper element
        """
        ...

class ModifierComponent(Component):
    modifiers = None

    def __init__(self, base=None, **modifiers):
        """
        **LLM Docstring**

        A component that modifies an existing base element's attributes rather than
        wrapping new content.

        :param base: the base element to modify
        :param modifiers: the attribute modifiers to apply
        """
        ...

    def __call__(self, base):
        """
        **LLM Docstring**

        Bind a base element to the modifier (callable form), erroring if one is already
        bound.

        :param base: the base element
        :return: self
        :rtype: ModifierComponent
        :raises ValueError: if a base is already bound
        """
        ...
    blacklist = {'dynamic'}

    def to_jhtml(self):
        """
        **LLM Docstring**

        Render the base element with the modifier attributes applied.

        :return: the JHTML element
        """
        ...

class Button(WrapperComponent):
    wrappers = dict(button=JHTML.Bootstrap.Button)
    theme = dict(button={'cls': ['btn'], 'variant': 'primary'})

    def __init__(self, body, action=None, event_handlers=None, **kwargs):
        """
        **LLM Docstring**

        A Bootstrap button with an optional click action/handlers.

        :param body: the button label/content
        :param action: the click action (callable)
        :param event_handlers: extra event handlers
        :param kwargs: extra attributes
        """
        ...

    @property
    def action(self):
        """
        **LLM Docstring**

        The button's click action. Setting it updates the click handler.

        :return: the action
        """
        ...

    @action.setter
    def action(self, a):
        """
        **LLM Docstring**

        The button's click action. Setting it updates the click handler.

        :return: the action
        """
        ...

    def _eval(self, *args):
        """
        **LLM Docstring**

        Invoke the button's action (the click handler).

        :param args: the event arguments
        :return: the action's result
        """
        ...

class LinkButton(Button):
    wrappers = dict(button=JHTML.Anchor)
    theme = dict(button={'cls': []})

class Spinner(WrapperComponent):
    wrappers = {'spinner': JHTML.Div}
    theme = {'spinner': {'cls': [], 'base-cls': 'spinner', 'variant': 'border'}}

    def __init__(self, body=None, role='status', **attrs):
        """
        :param variant:
        :type variant:
        :param attrs:
        :type attrs:
        """
        ...

class Progress(WrapperComponent):
    wrappers = {'wrapper': JHTML.Div, 'bar': None}
    theme = {'wrapper': {'cls': ['progress']}, 'bar': {'cls': ['progress-bar']}}

    def __init__(self, value=0, label=None, wrappers=None, **attrs):
        """
        **LLM Docstring**

        A Bootstrap progress bar.

        :param value: the initial percentage
        :param label: the bar label
        :param wrappers: the wrapper element classes
        :param attrs: extra attributes
        """
        ...

    @property
    def container(self):
        """
        **LLM Docstring**

        The progress bar's outer container element.

        :return: the container
        """
        ...

    @property
    def bar(self):
        """
        **LLM Docstring**

        The progress bar's inner (filled) element.

        :return: the bar
        """
        ...

    def update_widget_attr(self, attr, val):
        """
        **LLM Docstring**

        Push an attribute change into the bar's live widget.

        :param attr: the attribute name
        :param val: the value
        """
        ...

class MenuComponent(Container):

    def __init__(self, items: ElementType, **attrs):
        """
        **LLM Docstring**

        A `Container` of menu-style items.

        :param items: the menu items
        :param attrs: extra attributes
        """
        ...

    def create_item(self, item, **kw):
        """
        **LLM Docstring**

        Build a menu item element from its spec.

        :param item: the item spec
        :param kw: extra options
        :return: the item element
        """
        ...

class ListGroup(MenuComponent):
    ...

class ButtonGroup(MenuComponent):
    wrappers = {'wrapper': JHTML.Div, 'item': Button}
    theme = {'wrapper': {'cls': ['btn-group']}}

class DropdownList(MenuComponent):
    wrappers = {'wrapper': JHTML.Ul, 'item': {'list-item': JHTML.Li, 'link': JHTML.Anchor}}
    theme = {'wrapper': {'cls': ['dropdown-menu']}, 'item': {'list-item': {}, 'link': {'cls': ['dropdown-item']}}}

    def create_item(self, item, **kw):
        """
        **LLM Docstring**

        Build a dropdown-list item element (a dropdown menu entry).

        :param item: the item spec
        :param kw: extra options
        :return: the item element
        """
        ...

class Dropdown(ComponentContainer):
    components = {'toggle': Button, 'list': DropdownList}
    theme = {'wrapper': {'cls': ['dropdown']}, 'toggle': {'button': {'cls': ['dropdown-toggle'], 'data-bs-toggle': 'dropdown'}}}

    def __init__(self, header: ElementType, actions: ElementType, **attrs):
        """
        **LLM Docstring**

        A Bootstrap dropdown with a header/toggle and a list of actions.

        :param header: the toggle content
        :param actions: the dropdown actions
        :param attrs: extra attributes
        """
        ...

    def prep_actions(self, actions):
        """
        **LLM Docstring**

        Normalize the dropdown actions into item specs.

        :param actions: the actions
        :return: the prepared action items
        """
        ...

class Navbar(MenuComponent):
    wrappers = {'wrapper': JHTML.Nav, 'container': JHTML.Div, 'nav': JHTML.Div, 'item': JHTML.Anchor}

class Sidebar(MenuComponent):
    wrappers = {'wrapper': JHTML.Nav, 'item': {'list-item': JHTML.Li, 'link': JHTML.Anchor}}

class Pagination(MenuComponent):
    wrappers = {'wrapper': JHTML.Nav, 'container': JHTML.Ul, 'item': {'page-item': JHTML.Li, 'link': JHTML.Anchor}}

def short_uuid(len=6):
    """
    **LLM Docstring**

    Generate a short random id string.

    :return: the id
    :rtype: str
    """
    ...

class Carousel(MenuComponent):
    wrappers = {'wrapper': JHTML.Div, 'inner': JHTML.Div, 'item': JHTML.Div}

    def __init__(self, items, include_controls=True, data_bs_ride='carousel', include_indicators=False, overlap_controls=False, interval=None, **attrs):
        """
        **LLM Docstring**

        A Bootstrap carousel.

        :param items: the carousel slides
        :param include_controls: include the prev/next controls
        :type include_controls: bool
        :param data_bs_ride: the Bootstrap auto-ride mode
        :param attrs: extra attributes
        """
        ...

    def create_item(self, item, cls=None, data_bs_interval=None, **kw):
        """
        **LLM Docstring**

        Build a carousel slide element.

        :param item: the slide spec
        :param cls: extra CSS classes
        :param data_bs_interval: the slide interval
        :param kw: extra options
        :return: the slide element
        """
        ...

    def _control_button(self, dir, body=None, cls='carousel-control-{dir}', **kwargs):
        """
        **LLM Docstring**

        Build a carousel control (prev/next) button.

        :param dir: the direction
        :param body: the button content
        :param cls: the CSS class template
        :param kwargs: extra options
        :return: the control button
        """
        ...

    def next_button(self, body=None, **kwargs):
        """
        **LLM Docstring**

        Build the carousel's next-slide button.

        :param body: the button content
        :param kwargs: extra options
        :return: the button
        """
        ...

    def prev_button(self, body=None, **kwargs):
        """
        **LLM Docstring**

        Build the carousel's previous-slide button.

        :param body: the button content
        :param kwargs: extra options
        :return: the button
        """
        ...

    def indicators(self, **kwargs):
        """
        **LLM Docstring**

        Build the carousel's slide-indicator elements.

        :param kwargs: extra options
        :return: the indicators
        """
        ...

    def wrap_items(self, items):
        """
        **LLM Docstring**

        Wrap the slides (and controls/indicators) into the carousel element.

        :param items: the slides
        :return: the carousel element
        """
        ...

class TabList(MenuComponent):
    wrappers = {'wrapper': JHTML.Ul, 'item': {'list-item': JHTML.Li, 'tab-button': JHTML.Button}}

    def __init__(self, *args, base_name=None, role='tablist', **kwargs):
        """
        **LLM Docstring**

        The tab-buttons list of a tabbed interface.

        :param args: the tab specs
        :param base_name: the shared id prefix
        :param role: the ARIA role
        :type role: str
        :param kwargs: extra attributes
        """
        ...

    def create_item(self, item, cls=None, **kw):
        """
        **LLM Docstring**

        Build a tab-button element.

        :param item: the tab spec
        :param cls: extra CSS classes
        :param kw: extra options
        :return: the tab button
        """
        ...

class TabPane(MenuComponent):
    wrappers = {'wrapper': JHTML.Div, 'item': JHTML.Div}
    theme = {'wrapper': {'cls': ['tab-content']}, 'item': {'cls': ['tab-pane']}}

    def __init__(self, *args, base_name=None, **kwargs):
        """
        **LLM Docstring**

        The tab-content panes of a tabbed interface.

        :param args: the pane specs
        :param base_name: the shared id prefix
        :param kwargs: extra attributes
        """
        ...

    def create_item(self, item, cls=None, **kw):
        """
        **LLM Docstring**

        Build a tab-content pane element.

        :param item: the pane spec
        :param cls: extra CSS classes
        :param kw: extra options
        :return: the pane
        """
        ...

class Tabs(ComponentContainer):
    components = {'list': TabList, 'pane': TabPane}
    theme = {'pane': {}, 'list': {}}

    def __init__(self, tabs, base_name=None, **attrs):
        """
        **LLM Docstring**

        A tabbed interface (a tab list plus its content panes).

        :param tabs: the `{label: content}` tabs
        :param base_name: the shared id prefix
        :param attrs: extra attributes
        """
        ...

class AccordionHeader(Container):
    wrapper_classes = ['accordion-header']
    item = JHTML.Button
    item_classes = ['accordion-button']

    def __init__(self, key, base_name=None, **kw):
        """
        **LLM Docstring**

        An accordion item's header (toggle).

        :param key: the item's id
        :param base_name: the accordion id prefix
        :param kw: extra attributes
        """
        ...

    def create_item(self, i, **kw):
        """
        **LLM Docstring**

        Build the accordion header element.

        :param i: the header content
        :param kw: extra options
        :return: the header element
        """
        ...

class AccordionBody(Container):
    wrapper_classes = ['accordion-collapse', 'collapse']
    item = JHTML.Div
    item_classes = ['accordion-body']

    def __init__(self, key, parent_name=None, base_name=None, **kw):
        """
        **LLM Docstring**

        An accordion item's collapsible body.

        :param key: the item's id
        :param parent_name: the accordion id
        :param base_name: the item id prefix
        :param kw: extra attributes
        """
        ...

class Accordion(MenuComponent):
    wrapper_classes = ['accordion']
    item = JHTML.Div
    item_classes = ['accordion-item']
    header_classes = ['h2']

    def __init__(self, items, base_name=None, header_classes=None, **attrs):
        """
        **LLM Docstring**

        A Bootstrap accordion of collapsible items.

        :param items: the `{label: content}` items
        :param base_name: the accordion id prefix
        :param header_classes: extra header CSS classes
        :param attrs: extra attributes
        """
        ...

    def create_item(self, item, cls=None, **kw):
        """
        **LLM Docstring**

        Build an accordion item (header plus collapsible body).

        :param item: the item spec
        :param cls: extra CSS classes
        :param kw: extra options
        :return: the item element
        """
        ...

class OpenerHeader(Container):
    wrappers = {'wrapper': JHTML.Div, 'item': Button}
    theme = {'wrapper': {'cls': ['collapse-header']}, 'item': {'cls': ['accordion-button']}}

    def __init__(self, key, base_name=None, **kw):
        """
        **LLM Docstring**

        An opener's clickable header (toggle).

        :param key: the opener id
        :param base_name: the id prefix
        :param kw: extra attributes
        """
        ...

    def create_item(self, i, **kw):
        """
        **LLM Docstring**

        Build the opener header element.

        :param i: the header content
        :param kw: extra options
        :return: the header element
        """
        ...

class OpenerBody(Container):
    wrappers = {'wrapper': JHTML.Div, 'item': JHTML.Div}
    theme = {'wrapper': {'cls': ['collapse']}, 'item': {'cls': ['collapse-body']}}

    def __init__(self, key, base_name=None, **kw):
        """
        **LLM Docstring**

        An opener's collapsible body.

        :param key: the opener id
        :param base_name: the id prefix
        :param kw: extra attributes
        """
        ...

class Opener(MenuComponent):
    wrappers = {'wrapper': JHTML.Div, 'item': JHTML.Div}
    theme = {'wrapper': {'cls': ['opener']}, 'item': {'cls': ['opener-item']}, 'header': {}, 'body': {}}

    def __init__(self, items, base_name=None, open=False, **attrs):
        """
        **LLM Docstring**

        A collapsible opener (a simpler, single-level accordion-style disclosure).

        :param items: the `{label: content}` items
        :param base_name: the id prefix
        :param open: start expanded
        :type open: bool
        :param attrs: extra attributes
        """
        ...

    def create_item(self, item, open=None, **kw):
        """
        **LLM Docstring**

        Build an opener item (header plus collapsible body).

        :param item: the item spec
        :param open: start expanded
        :param kw: extra options
        :return: the item element
        """
        ...

class CardOpener(Opener):
    ...

class Breadcrumb(MenuComponent):
    wrappers = {'wrapper': JHTML.Nav, 'list': JHTML.Ol, 'item': JHTML.Li}
    theme = {'wrapper': {'cls': []}, 'list': {'cls': ['breadcrumb']}, 'item': {'cls': ['breadcrumb-item']}}

class CardBody(WrapperComponent):
    wrappers = {'wrapper': JHTML.Bootstrap.CardBody}

class CardHeader(WrapperComponent):
    wrappers = {'wrapper': JHTML.Bootstrap.CardHeader}

class CardFooter(WrapperComponent):
    wrappers = {'wrapper': JHTML.Bootstrap.CardFooter}

class Card(ComponentContainer):
    wrappers = {'wrapper': JHTML.Bootstrap.Card}
    components = {'header': CardHeader, 'body': CardBody, 'footer': CardFooter}

    def __init__(self, *args, header=None, body=None, footer=None, **attrs):
        """
        **LLM Docstring**

        A Bootstrap card (header/body/footer sub-components).

        :param args: the card content
        :param attrs: extra attributes and per-section options
        """
        ...

class Modal(Container):
    wrapper_classes = ['modal', 'fade']
    subwrappers = [JHTML.Div, JHTML.Div]
    subwrapper_classes = [['modal-dialog', 'modal-dialog-centered'], ['modal-content']]

    def __init__(self, header=None, body=None, footer=None, id=None, tabindex=-1, **attrs):
        """
        **LLM Docstring**

        A Bootstrap modal dialog (header/body/footer).

        :param args: the modal content
        :param attrs: extra attributes and per-section options
        """
        ...
    trigger_class = JHTML.Bootstrap.Button

    def get_trigger(self, *items, trigger_class=None, data_bs_toggle='modal', data_bs_target=None, **attrs):
        """
        **LLM Docstring**

        Build a trigger element that opens the modal.

        :param items: the trigger content
        :param trigger_class: the trigger's CSS class
        :param data_bs_toggle: the Bootstrap toggle type
        :param data_bs_target: the modal target id
        :param attrs: extra attributes
        :return: the trigger element
        """
        ...

    @classmethod
    def close_button(self):
        """
        **LLM Docstring**

        Build a modal close button.

        :return: the close button
        """
        ...

class ModalHeader(WrapperComponent):
    wrappers = {'wrapper': JHTML.Div}
    theme = {'wrapper': {'cls': ['modal-header']}}

    def __init__(self, items, **attrs):
        """
        **LLM Docstring**

        A modal's header section.

        :param items: the header content
        :param attrs: extra attributes
        """
        ...

class ModalFooter(WrapperComponent):
    wrappers = {'wrapper': JHTML.Div}
    theme = {'wrapper': {'cls': ['modal-footer']}}

class ModalBody(WrapperComponent):
    wrappers = {'wrapper': JHTML.Div}
    theme = {'wrapper': {'cls': ['modal-body']}}

class Offcanvas(Container):
    wrapper_classes = ['offcanvas', 'ps-4', 'pt-5', 'pb-5']

    def __init__(self, header=None, body=None, id=None, tabindex=-1, cls=None, placement='start', **attrs):
        """
        **LLM Docstring**

        A Bootstrap offcanvas panel (header/body).

        :param args: the panel content
        :param attrs: extra attributes and per-section options
        """
        ...
    trigger_class = JHTML.Bootstrap.Button

    def get_trigger(self, *items, trigger_class=None, data_bs_toggle='offcanvas', data_bs_target=None, **attrs):
        """
        **LLM Docstring**

        Build a trigger element that opens the offcanvas panel.

        :param items: the trigger content
        :param trigger_class: the trigger's CSS class
        :param data_bs_toggle: the Bootstrap toggle type
        :param data_bs_target: the panel target id
        :param attrs: extra attributes
        :return: the trigger element
        """
        ...

    @classmethod
    def close_button(self):
        """
        **LLM Docstring**

        Build an offcanvas close button.

        :return: the close button
        """
        ...

class OffcanvasHeader(WrapperComponent):
    wrappers = {'wrapper': JHTML.Div}
    theme = {'wrapper': {'cls': ['offcanvas-header', 'm-2', 'border-bottom']}}

    def __init__(self, items, **attrs):
        """
        **LLM Docstring**

        An offcanvas panel's header section.

        :param items: the header content
        :param attrs: extra attributes
        """
        ...

class OffcanvasBody(WrapperComponent):
    wrappers = {'wrapper': JHTML.Div}
    theme = {'wrapper': {'cls': ['offcanvas-body']}}

class Spacer(WrapperComponent):
    wrappers = {'wrapper': JHTML.Span}
    theme = {'wrapper': {'cls': ['me-auto']}}

    def __init__(self, items=None, **kwargs):
        """
        **LLM Docstring**

        A spacing element.

        :param items: optional content
        :param kwargs: extra attributes
        """
        ...

class ToastBody(WrapperComponent):
    wrappers = {'wrapper': JHTML.Div}
    theme = {'wrapper': {'cls': ['toast-body']}}

    def __init__(self, items, include_controls=False, cls=None, **attrs):
        """
        **LLM Docstring**

        A toast's body section.

        :param items: the body content
        :param include_controls: include the close control
        :type include_controls: bool
        :param cls: extra CSS classes
        :param attrs: extra attributes
        """
        ...

class ToastHeader(WrapperComponent):
    wrappers = {'wrapper': JHTML.Div}
    theme = {'wrapper': {'cls': ['toast-header']}}

    def __init__(self, items, include_controls=True, **attrs):
        """
        **LLM Docstring**

        A toast's header section.

        :param items: the header content
        :param include_controls: include the close control
        :type include_controls: bool
        :param attrs: extra attributes
        """
        ...

class Toast(WrapperComponent):
    wrappers = {'wrapper': JHTML.Div}
    theme = {'wrapper': {'cls': ['toast']}}

    def __init__(self, header=None, body=None, role='alert', hidden=True, cls=None, id=None, javascript_handles=None, onevents=None, **attrs):
        """
        **LLM Docstring**

        A Bootstrap toast notification (header/body).

        :param args: the toast content
        :param attrs: extra attributes and per-section options
        """
        ...
    trigger_class = JHTML.Bootstrap.Button

    def get_trigger(self, *items, trigger_class=None, data_bs_toggle='toast', data_bs_target=None, **attrs):
        """
        **LLM Docstring**

        Build a trigger element that shows the toast.

        :param items: the trigger content
        :param trigger_class: the trigger's CSS class
        :param data_bs_toggle: the Bootstrap toggle type
        :param data_bs_target: the toast target id
        :param attrs: extra attributes
        :return: the trigger element
        """
        ...

    @classmethod
    def close_button(self):
        """
        **LLM Docstring**

        Build a toast close button.

        :return: the close button
        """
        ...

    def show(self):
        """
        **LLM Docstring**

        Show the toast.
        """
        ...

    def hide(self):
        """
        **LLM Docstring**

        Hide the toast.
        """
        ...

class ToastContainer(WrapperComponent):
    wrappers = {'wrapper': JHTML.Div}
    theme = {'wrapper': {'cls': ['toast-container']}}

    def __init__(self, items=None, **kwargs):
        """
        **LLM Docstring**

        A positioned container that holds toast notifications.

        :param items: the initial toasts
        :param kwargs: extra attributes
        """
        ...

    def create_toast(self, header=None, body=None, hidden=False, **kwargs):
        """
        **LLM Docstring**

        Create and add a toast to the container.

        :param header: the toast header
        :param body: the toast body
        :param hidden: start hidden
        :type hidden: bool
        :param kwargs: extra toast options
        :return: the toast
        """
        ...

class Tooltip(ModifierComponent):

    def __init__(self, base=None, title='tooltip', data_bs_html=None, **kwargs):
        """
        **LLM Docstring**

        A modifier that attaches a Bootstrap tooltip to a base element.

        :param base: the base element
        :param title: the tooltip text
        :param data_bs_html: allow HTML in the tooltip
        :param kwargs: extra attributes
        """
        ...

class Popover(ModifierComponent):

    def __init__(self, base=None, body='', data_bs_trigger='hover focus', data_bs_html=None, title=None, **kwargs):
        """
        **LLM Docstring**

        A modifier that attaches a Bootstrap popover to a base element.

        :param base: the base element
        :param body: the popover body
        :param data_bs_trigger: the trigger events
        :type data_bs_trigger: str
        :param data_bs_html: allow HTML in the popover
        :param title: the popover title
        :param kwargs: extra attributes
        """
        ...

class LayoutItem(Component):
    wrapper = JHTML.Div
    properties = []

    def __init__(self, item, **attrs):
        """
        **LLM Docstring**

        A single positioned item within a layout.

        :param item: the item content
        :param attrs: extra attributes
        """
        ...

    @abc.abstractmethod
    def get_layout_styles(self, **kwargs):
        """
        **LLM Docstring**

        Abstract: return the CSS styles positioning this item.

        :param kwargs: layout parameters
        :return: the styles
        :rtype: dict
        """
        ...

    def to_jhtml(self):
        """
        **LLM Docstring**

        Render the item in its wrapper with the layout styles applied.

        :return: the JHTML element
        """
        ...

class Layout(Component):
    wrapper = JHTML.Div
    Item = LayoutItem

    def __init__(self, elements, wrapper=None, item_attrs=None, style=None, **attrs):
        """
        **LLM Docstring**

        A container that arranges its elements via CSS layout styles.

        :param elements: the elements to arrange
        :param wrapper: the wrapper element class
        :param item_attrs: default per-item attributes
        :type item_attrs: dict | None
        :param style: extra container styles
        :param attrs: extra attributes
        """
        ...

    def wrap_item(self, e, attrs):
        """
        **LLM Docstring**

        Wrap an element as a layout `Item`.

        :param e: the element
        :param attrs: the item attributes
        :return: the layout item
        """
        ...

    def setup_layout(self, elements, item_attrs):
        """
        **LLM Docstring**

        Prepare the layout: wrap each element as an item, returning `(layout_settings, items)`.

        :param elements: the elements
        :param item_attrs: the per-item attributes
        :return: `(settings, items)`
        :rtype: tuple
        """
        ...

    @abc.abstractmethod
    def get_layout_styles(self, **kwargs):
        """
        **LLM Docstring**

        Abstract: return the CSS styles for the container.

        :param kwargs: layout parameters
        :return: the styles
        :rtype: dict
        """
        ...

    @property
    def styles(self):
        """
        **LLM Docstring**

        The container's combined explicit and computed layout styles.

        :return: the styles
        :rtype: dict
        """
        ...

    def to_jhtml(self):
        """
        **LLM Docstring**

        Render the layout container with its items and styles.

        :return: the JHTML element
        """
        ...

class GridItem(LayoutItem):

    def __init__(self, item, row=None, col=None, row_span=None, col_span=None, alignment=None, justification=None, **attrs):
        """
        **LLM Docstring**

        A grid-positioned item.

        :param item: the item content
        :param row: the starting row
        :param col: the starting column
        :param row_span: the row span
        :param col_span: the column span
        :param alignment: the self-alignment
        :param justification: the self-justification
        :param attrs: extra attributes
        """
        ...

    @classmethod
    def get_grid_styles(cls, row=None, row_span=None, col=None, col_span=None, alignment=None, justification=None):
        """
        **LLM Docstring**

        Compute the CSS grid-placement styles from a row/column position and span.

        :param row: the starting row
        :param row_span: the row span
        :param col: the starting column
        :param col_span: the column span
        :param alignment: the self-alignment
        :param justification: the self-justification
        :return: the styles
        :rtype: dict
        """
        ...

    def get_layout_styles(self):
        """
        **LLM Docstring**

        Return this item's grid-placement styles.

        :return: the styles
        :rtype: dict
        """
        ...

class Grid(Layout):
    Item = GridItem

    def __init__(self, elements, rows=None, cols=None, alignment=None, justification=None, row_spacing=None, col_spacing=None, item_attrs=None, row_height='auto', column_width='1fr', **attrs):
        """
        **LLM Docstring**

        A CSS-grid layout of elements (given as a list of rows).

        :param elements: the grid rows of elements
        :param rows: the number of rows (inferred if omitted)
        :param cols: the number of columns (inferred if omitted)
        :param alignment: the item alignment
        :param justification: the item justification
        :param row_spacing: the row gap
        :param col_spacing: the column gap
        :param item_attrs: default per-item attributes
        :param row_height: the row track sizing
        :param column_width: the column track sizing
        :param attrs: extra attributes
        """
        ...

    def setup_layout(self, grid, attrs):
        """
        **LLM Docstring**

        Wrap each non-empty grid cell as a positioned item and infer the row/column counts.

        :param grid: the grid of elements
        :param attrs: the per-item attributes
        :return: `(settings, items)`
        :rtype: tuple
        """
        ...

    def wrap_item(self, e, attrs):
        """
        **LLM Docstring**

        Wrap a grid element as a positioned `GridItem`, filling in its row/column.

        :param e: the element
        :param attrs: the item attributes (row/col)
        :return: the grid item
        """
        ...

    @classmethod
    def get_grid_styles(cls, rows=None, cols=None, alignment=None, justification=None, row_gap=None, col_gap=None, row_height='1fr', col_width='1fr'):
        """
        **LLM Docstring**

        Compute the CSS grid-container styles (template rows/columns, gaps, alignment).

        :param rows: the number of rows
        :param cols: the number of columns
        :param alignment: the item alignment
        :param justification: the item justification
        :param row_gap: the row gap
        :param col_gap: the column gap
        :param row_height: the row track sizing
        :param col_width: the column track sizing
        :return: the styles
        :rtype: dict
        """
        ...

    def get_layout_styles(self):
        """
        **LLM Docstring**

        Return the grid container's styles.

        :return: the styles
        :rtype: dict
        """
        ...

class TableItem(GridItem):

    def __init__(self, item, row=None, col=None, row_span=None, col_span=None, alignment=None, justification=None, header=False, **attrs):
        """
        **LLM Docstring**

        A table cell (a grid item rendered as a `<td>`/`<th>`).

        :param item: the cell content
        :param row: the row
        :param col: the column
        :param row_span: the row span
        :param col_span: the column span
        :param alignment: the self-alignment
        :param justification: the self-justification
        :param header: render as a header cell
        :type header: bool
        :param attrs: extra attributes
        """
        ...

    def wrapper(self, item, **kwargs):
        """
        **LLM Docstring**

        Return the cell element (a heading cell if `header`, else a data cell).

        :param item: the cell content
        :param kwargs: extra attributes
        :return: the cell element
        """
        ...

class Table(Grid):
    Item = TableItem

    def __init__(self, elements, rows=None, cols=None, alignment=None, justification=None, row_spacing=None, col_spacing=None, item_attrs=None, row_height='1fr', column_width='1fr', table_headings=None, striped=True, **attrs):
        """
        **LLM Docstring**

        A table rendered as a CSS grid (`display: contents` rows), optionally with headings
        and striping.

        :param elements: the table rows of cells
        :param rows: the number of rows
        :param cols: the number of columns
        :param alignment: the cell alignment
        :param justification: the cell justification
        :param row_spacing: the row gap
        :param col_spacing: the column gap
        :param item_attrs: default per-cell attributes
        :param row_height: the row track sizing
        :param column_width: the column track sizing
        :param table_headings: the header row cells
        :param striped: use striped rows
        :type striped: bool
        :param attrs: extra attributes
        """
        ...

    def wrapper(self, *elems, cls=None, **attrs):
        """
        **LLM Docstring**

        Wrap the rows in a `<table>` (with header/body sections and striping).

        :param elems: the table rows
        :param cls: extra CSS classes
        :param attrs: extra attributes
        :return: the table element
        """
        ...

    def setup_layout(self, grid, attrs):
        """
        **LLM Docstring**

        Build the table rows (including an optional heading row) and infer the row/column counts.

        :param grid: the grid of cells
        :param attrs: the per-cell attributes
        :return: `(settings, rows)`
        :rtype: tuple
        """
        ...

class FlexItem(LayoutItem):

    def __init__(self, item, order=None, grow=None, shrink=None, basis=None, alignment=None, **attrs):
        """
        **LLM Docstring**

        A flexbox item.

        :param item: the item content
        :param order: the flex order
        :param grow: the flex-grow factor
        :param shrink: the flex-shrink factor
        :param basis: the flex basis
        :param alignment: the self-alignment
        :param attrs: extra attributes
        """
        ...

    @classmethod
    def get_flex_styles(cls, order=None, grow=None, shrink=None, basis=None, alignment=None):
        """
        **LLM Docstring**

        Compute the CSS flex-item styles from the order/grow/shrink/basis/alignment.

        :param order: the flex order
        :param grow: the flex-grow factor
        :param shrink: the flex-shrink factor
        :param basis: the flex basis
        :param alignment: the self-alignment
        :return: the styles
        :rtype: dict
        """
        ...

    def get_layout_styles(self):
        """
        **LLM Docstring**

        Return this item's flex styles.

        :return: the styles
        :rtype: dict
        """
        ...

class Flex(Layout):
    Item = FlexItem

    def __init__(self, elements, direction=None, wrap=None, alignment=None, justification=None, content_alignment=None, **attrs):
        """
        **LLM Docstring**

        A flexbox layout of elements.

        :param elements: the elements to arrange
        :param direction: the flex direction
        :param wrap: the flex-wrap mode
        :param alignment: the cross-axis item alignment
        :param justification: the main-axis justification
        :param content_alignment: the multi-line content alignment
        :param attrs: extra attributes
        """
        ...

    @classmethod
    def get_flex_styles(cls, direction=None, wrap=None, alignment=None, justification=None, content_alignment=None):
        """
        **LLM Docstring**

        Compute the CSS flex-container styles from the direction/wrap/alignment.

        :param direction: the flex direction
        :param wrap: the flex-wrap mode
        :param alignment: the item alignment
        :param justification: the justification
        :param content_alignment: the content alignment
        :return: the styles
        :rtype: dict
        """
        ...

    def get_layout_styles(self):
        """
        **LLM Docstring**

        Return the flex container's styles.

        :return: the styles
        :rtype: dict
        """
        ...

class GenericDisplay(WidgetInterface):

    def __init__(self, obj):
        """
        **LLM Docstring**

        Wrap an arbitrary object for display as a widget.

        :param obj: the object to display
        """
        ...

    def to_widget(self):
        """
        **LLM Docstring**

        Render the object to a widget (using its own `to_widget` or an output area).

        :return: the widget
        """
        ...

class ResultTypes:
    NoResult = 'NoResult'

class DelayedResult(WidgetInterface):
    NoResult = ResultTypes.NoResult

    def __init__(self, func, *args, output=None, callback=None, parent=None, **kwargs):
        """
        **LLM Docstring**

        Run a function on a background thread and display its result when ready.

        :param func: the function to run
        :type func: Callable
        :param args: positional arguments for the function
        :param output: the output area (created if omitted)
        :param callback: a `(result, error, runner)` completion callback
        :param parent: the parent interface
        :param kwargs: keyword arguments for the function
        """
        ...

    def get_output_area(self, output=None):
        """
        **LLM Docstring**

        Return the output area (creating one if none is given).

        :param output: an explicit output area
        :return: the output area
        """
        ...

    def __enter__(self):
        """
        **LLM Docstring**

        Enter the output area's context.

        :return: self
        :rtype: DelayedResult
        """
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Exit the output area's context.

        :param exc_type: the exception type, if any
        :param exc_val: the exception value, if any
        :param exc_tb: the traceback, if any
        """
        ...

    def _run(self):
        """
        **LLM Docstring**

        Run the function, capturing the result or error, displaying the result in the
        output area, and firing the completion callback.
        """
        ...

    def start_process(self):
        """
        **LLM Docstring**

        Start the background thread running the function (once).

        :return: the thread
        """
        ...

    def to_widget(self):
        """
        **LLM Docstring**

        Start the background process and return the output area widget.

        :return: the output area
        """
        ...
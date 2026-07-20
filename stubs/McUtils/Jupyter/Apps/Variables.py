import uuid
import numpy as np, weakref
from ..JHTML import JHTML, DefaultOutputWidget, JupyterAPIs
__all__ = ['Var', 'DefaultVars', 'InterfaceVars', 'VariableSynchronizer', 'VariableNamespace', 'WidgetControl']
__reload_hook__ = ['..JHTML']

class SettingChecker:
    int_types = (int, np.integer)
    numerics_types = (int, np.integer, float, np.floating)
    control_type = None

    @classmethod
    def check(self, **props):
        """
        **LLM Docstring**

        Base predicate: test whether a set of control settings matches this checker's
        control type (always `False` on the base class).

        :param props: the candidate control settings
        :return: whether the settings match
        :rtype: bool
        """
        ...
    checkers = []

class CheckboxChecker(SettingChecker):
    control_type = 'Checkbox'

    @classmethod
    def check(self, value=None, **rest):
        """
        **LLM Docstring**

        Test whether the settings describe a `Checkbox` control (the value is a bool).

        :param value: the control's value
        :param rest: the other control settings
        :return: whether a `Checkbox` fits
        :rtype: bool
        """
        ...

class DropdownChecker(SettingChecker):
    control_type = 'Dropdown'

    @classmethod
    def check(self, options=None, **rest):
        """
        **LLM Docstring**

        Test whether the settings describe a `Dropdown` control (`options` are given).

        :param options: the dropdown options
        :param rest: the other control settings
        :return: whether a `Dropdown` fits
        :rtype: bool
        """
        ...

class TextChecker(SettingChecker):
    control_type = 'Text'

    @classmethod
    def check(self, value=None, **rest):
        """
        **LLM Docstring**

        Test whether the settings describe a `Text` control (the value is a string).

        :param value: the control's value
        :param rest: the other control settings
        :return: whether a `Text` fits
        :rtype: bool
        """
        ...

class IntSliderChecker(SettingChecker):
    control_type = 'IntSlider'

    @classmethod
    def check(self, value=None, min=None, max=None, **rest):
        """
        **LLM Docstring**

        Test whether the settings describe an `IntSlider` (integer value with integer
        min/max).

        :param value: the value
        :param min: the minimum
        :param max: the maximum
        :param rest: the other settings
        :return: whether an `IntSlider` fits
        :rtype: bool
        """
        ...

class FloatSliderChecker(SettingChecker):
    control_type = 'FloatSlider'

    @classmethod
    def check(self, value=None, min=None, max=None, **rest):
        """
        **LLM Docstring**

        Test whether the settings describe a `FloatSlider` (numeric value with numeric
        min/max).

        :param value: the value
        :param min: the minimum
        :param max: the maximum
        :param rest: the other settings
        :return: whether a `FloatSlider` fits
        :rtype: bool
        """
        ...

class IntRangeChecker(SettingChecker):
    control_type = 'IntRangeSlider'

    @classmethod
    def check(self, value=None, min=None, max=None, **rest):
        """
        **LLM Docstring**

        Test whether the settings describe an `IntRangeSlider` (a length-2 integer value
        with integer min/max).

        :param value: the `(low, high)` value
        :param min: the minimum
        :param max: the maximum
        :param rest: the other settings
        :return: whether an `IntRangeSlider` fits
        :rtype: bool
        """
        ...

class FloatRangeChecker(SettingChecker):
    control_type = 'FloatRangeSlider'

    @classmethod
    def check(self, value=None, min=None, max=None, **rest):
        """
        **LLM Docstring**

        Test whether the settings describe a `FloatRangeSlider` (a length-2 numeric value
        with numeric min/max).

        :param value: the `(low, high)` value
        :param min: the minimum
        :param max: the maximum
        :param rest: the other settings
        :return: whether a `FloatRangeSlider` fits
        :rtype: bool
        """
        ...

class InterfaceVars:
    _cache_stack = []

    def __init__(self, *vars, callbacks=None, namespace=None):
        """
        **LLM Docstring**

        Hold a set of interface variables (coercing each into a `Var`) plus the callbacks
        fired when the set changes.

        :param vars: the variables (names or synchronizers)
        :param callbacks: callbacks fired when a variable is added
        :param namespace: the variable namespace
        """
        ...

    @classmethod
    def unique_namespace(cls, tag='vars'):
        """
        **LLM Docstring**

        Generate a unique namespace name.

        :param tag: the name prefix
        :type tag: str
        :return: the namespace name
        :rtype: str
        """
        ...

    @classmethod
    def active_vars(cls):
        """
        **LLM Docstring**

        Return the innermost active variable set (from the context stack), or `None`.

        :return: the active variable set
        :rtype: InterfaceVars | None
        """
        ...

    @property
    def dict(self):
        """
        **LLM Docstring**

        The variables as a `{name: value}` mapping.

        :return: the variable values
        :rtype: dict
        """
        ...

    @property
    def items(self):
        """
        **LLM Docstring**

        The variables as a list of `(name, value)` pairs.

        :return: the variable items
        :rtype: list
        """
        ...

    def __iter__(self):
        """
        **LLM Docstring**

        Iterate over the variables.

        :return: the variable iterator
        """
        ...

    def add(self, var):
        """
        **LLM Docstring**

        Add a variable to the set (if new), firing the change callbacks.

        :param var: the variable to add
        """
        ...

    def __enter__(self):
        """
        **LLM Docstring**

        Push this set onto the active-vars stack so newly created variables register
        here.

        :return: the variable list
        :rtype: list
        """
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Pop this set off the active-vars stack.

        :param exc_type: the exception type, if any
        :param exc_val: the exception value, if any
        :param exc_tb: the traceback, if any
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation listing the variable names.

        :return: the representation
        :rtype: str
        """
        ...

class DefaultVars:
    _var_stack = []

    def __init__(self, vars: InterfaceVars=None):
        """
        **LLM Docstring**

        Context manager holding a default `InterfaceVars` set to activate.

        :param vars: the variable set (a fresh one if omitted)
        :type vars: InterfaceVars | None
        """
        ...

    def __enter__(self):
        """
        **LLM Docstring**

        Push this default onto the stack and activate its variable set.

        :return: the variable set
        :rtype: InterfaceVars
        """
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Pop this default off the stack and deactivate its variable set.

        :param exc_type: the exception type, if any
        :param exc_val: the exception value, if any
        :param exc_tb: the traceback, if any
        """
        ...

    @classmethod
    def resolve(cls):
        """
        **LLM Docstring**

        Return the current default variable set (a fresh one if none is active).

        :return: the variable set
        :rtype: InterfaceVars
        """
        ...

class VariableNamespace:
    _namespace_cache = weakref.WeakValueDictionary()

    def __init__(self, name=None, dedupe=True):
        """
        **LLM Docstring**

        A named namespace of variables, optionally deduplicated so the same name reuses a
        shared variable cache.

        :param name: the namespace name (a uuid if omitted)
        :param dedupe: share the variable cache with an existing namespace of the same name
        :type dedupe: bool
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation showing the name and cached variables.

        :return: the representation
        :rtype: str
        """
        ...

    @classmethod
    def create(cls, name):
        """
        **LLM Docstring**

        Resolve a namespace name (or namespace) to a cached `VariableNamespace`, creating
        and caching it if needed.

        :param name: the namespace name or object
        :return: the namespace
        :rtype: VariableNamespace
        """
        ...

    def __contains__(self, item):
        """
        **LLM Docstring**

        Test whether a variable name is in the namespace.

        :param item: the variable name
        :return: whether it's present
        :rtype: bool
        """
        ...

    def __getitem__(self, item):
        """
        **LLM Docstring**

        Get a variable from the namespace by name.

        :param item: the variable name
        :return: the variable
        """
        ...

    def __setitem__(self, key, value):
        """
        **LLM Docstring**

        Store a variable in the namespace under a name.

        :param key: the variable name
        :param value: the variable
        """
        ...

    def __enter__(self):
        """
        **LLM Docstring**

        Activate this namespace as the current one, saving the previous.
        """
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Restore the previously active namespace.

        :param exc_type: the exception type, if any
        :param exc_val: the exception value, if any
        :param exc_tb: the traceback, if any
        """
        ...

class VariableSynchronizer:
    current_namespace = VariableNamespace.create('globals')

    def __init__(self, name, namespace=None, value=None, callbacks=(), output_pane=None, autounlink=True):
        """
        **LLM Docstring**

        A reactive variable that synchronizes its value across linked widgets and fires
        callbacks on change.

        :param name: the variable name
        :param namespace: the owning namespace
        :param value: the initial value
        :param callbacks: change callbacks
        :param output_pane: the output pane for error display
        :param autounlink: unlink other widgets when a new one links
        :type autounlink: bool
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation showing the name and value.

        :return: the representation
        :rtype: str
        """
        ...

    @classmethod
    def create_var(cls, var, namespace=None):
        """
        **LLM Docstring**

        Resolve a name (or synchronizer) to a `VariableSynchronizer` in the namespace,
        creating and caching it if needed, and registering it with the active variable
        set.

        :param var: the variable name or synchronizer
        :param namespace: the namespace (defaults to the current one)
        :return: the variable
        :rtype: VariableSynchronizer
        """
        ...

    @property
    def name(self):
        """
        **LLM Docstring**

        The variable's name.

        :return: the name
        """
        ...

    @property
    def value(self):
        """
        **LLM Docstring**

        The variable's current value. Setting it propagates to linked widgets and fires
        the change callbacks.

        :return: the value
        """
        ...

    @value.setter
    def value(self, v):
        """
        **LLM Docstring**

        The variable's current value. Setting it propagates to linked widgets and fires
        the change callbacks.

        :return: the value
        """
        ...

    def set_value(self, v, caller=None):
        """
        **LLM Docstring**

        Set the value (if changed), firing the change callbacks and propagating to every
        linked widget except the caller.

        :param v: the new value
        :param caller: the widget that triggered the change (not re-notified)
        """
        ...

    def link(self, widget):
        """
        **LLM Docstring**

        Link a widget to the variable: seed the variable from the widget's value, observe
        the widget for changes, and (if `autounlink`) unlink other widgets.

        :param widget: the widget to link
        """
        ...

    def unlink(self, widget):
        """
        **LLM Docstring**

        Unlink a widget from the variable, removing its change observers.

        :param widget: the widget to unlink
        """
        ...

def Var(name, namespace=None):
    """
    **LLM Docstring**

    Resolve a name (or synchronizer) to a `VariableSynchronizer`, optionally within a
    named namespace.

    :param name: the variable name or synchronizer
    :param namespace: the namespace name/object (the current one if omitted)
    :return: the variable
    :rtype: VariableSynchronizer
    """
    ...

class WidgetControl:

    def __init__(self, var, control_type=None, widget=None, **settings):
        """
        **LLM Docstring**

        Bind a variable to a control widget, inferring the widget type from the settings
        when one isn't given.

        :param var: the variable (name or synchronizer)
        :param control_type: the widget type (inferred from the settings if omitted)
        :param widget: an explicit widget (built if omitted)
        :param settings: the widget settings
        """
        ...

    @classmethod
    def _build_widget(cls, control_type, settings):
        """
        **LLM Docstring**

        Build the control widget: use the given type, or infer it by running the settings
        through the registered `SettingChecker`s (falling back to an output area).

        :param control_type: the widget type (or `None` to infer)
        :param settings: the widget settings
        :type settings: dict
        :return: the widget
        """
        ...

    def to_widget(self):
        """
        **LLM Docstring**

        Link the variable to the widget and return the widget.

        :return: the widget
        """
        ...
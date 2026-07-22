import uuid

import numpy as np, weakref
from ..JHTML import JHTML, DefaultOutputWidget, JupyterAPIs

__all__ = [
    "Var",
    "DefaultVars",
    "InterfaceVars",
    "VariableSynchronizer",
    "VariableNamespace",
    "WidgetControl"
]

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
        return False
    checkers = []
class CheckboxChecker(SettingChecker):
    control_type = "Checkbox"
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
        return isinstance(value, bool)
SettingChecker.checkers.append(CheckboxChecker)
class DropdownChecker(SettingChecker):
    control_type = "Dropdown"
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
        return options is not None
SettingChecker.checkers.append(DropdownChecker)
class TextChecker(SettingChecker):
    control_type = "Text"
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
        return isinstance(value, str)
SettingChecker.checkers.append(TextChecker)
class IntSliderChecker(SettingChecker):
    control_type = "IntSlider"
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
        return isinstance(value, self.int_types) and isinstance(min, self.int_types) and isinstance(max, self.int_types)
SettingChecker.checkers.append(IntSliderChecker)
class FloatSliderChecker(SettingChecker):
    control_type = "FloatSlider"
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
        return (
                isinstance(value, self.numerics_types)
                and isinstance(min, self.numerics_types)
                and isinstance(max, self.numerics_types)
        )
SettingChecker.checkers.append(FloatSliderChecker)
class IntRangeChecker(SettingChecker):
    control_type = "IntRangeSlider"
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
        return (
                len(value) == 2
                and isinstance(value[0], self.int_types)
                and isinstance(value[1], self.int_types)
                and isinstance(min, self.int_types) and isinstance(max, self.int_types)
        )
SettingChecker.checkers.append(IntRangeChecker)
class FloatRangeChecker(SettingChecker):
    control_type = "FloatRangeSlider"
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
        return (
                len(value) == 2
                and isinstance(value[0], self.numerics_types)
                and isinstance(value[1], self.numerics_types)
                and isinstance(min, self.numerics_types) and isinstance(max, self.numerics_types)
        )
SettingChecker.checkers.append(FloatRangeChecker)

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
        vars = [Var(x, namespace=namespace) if isinstance(x, str) else x for x in vars]
        self._var_set = set(vars)
        self.var_list = vars
        self.callbacks = set(callbacks) if callbacks is not None else set()
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
        return tag+"-"+str(uuid.uuid4())[:6]
    @classmethod
    def active_vars(cls):
        """
        **LLM Docstring**

        Return the innermost active variable set (from the context stack), or `None`.

        :return: the active variable set
        :rtype: InterfaceVars | None
        """
        if len(cls._cache_stack) > 0:
            return cls._cache_stack[-1]
        else:
            return None
    @property
    def dict(self):
        """
        **LLM Docstring**

        The variables as a `{name: value}` mapping.

        :return: the variable values
        :rtype: dict
        """
        return {v.name:v.value for v in self.var_list}
    @property
    def items(self):
        """
        **LLM Docstring**

        The variables as a list of `(name, value)` pairs.

        :return: the variable items
        :rtype: list
        """
        return [(v.name, v.value) for v in self.var_list]
    def __iter__(self):
        """
        **LLM Docstring**

        Iterate over the variables.

        :return: the variable iterator
        """
        return iter(self.var_list)
    def add(self, var):
        """
        **LLM Docstring**

        Add a variable to the set (if new), firing the change callbacks.

        :param var: the variable to add
        """
        if var not in self._var_set:
            self.var_list.append(var)
            self._var_set.add(var)
            for c in self.callbacks:
                c(self)
    def __enter__(self):
        """
        **LLM Docstring**

        Push this set onto the active-vars stack so newly created variables register
        here.

        :return: the variable list
        :rtype: list
        """
        self._cache_stack.append(self)
        return self.var_list
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Pop this set off the active-vars stack.

        :param exc_type: the exception type, if any
        :param exc_val: the exception value, if any
        :param exc_tb: the traceback, if any
        """
        self._cache_stack.pop()
    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation listing the variable names.

        :return: the representation
        :rtype: str
        """
        return "{}({})".format(type(self).__name__, ", ".join(s.name for s in self._var_set))
class DefaultVars:
    _var_stack = []
    def __init__(self, vars:InterfaceVars=None):
        """
        **LLM Docstring**

        Context manager holding a default `InterfaceVars` set to activate.

        :param vars: the variable set (a fresh one if omitted)
        :type vars: InterfaceVars | None
        """
        self.vars = InterfaceVars() if vars is None else vars
    def __enter__(self):
        """
        **LLM Docstring**

        Push this default onto the stack and activate its variable set.

        :return: the variable set
        :rtype: InterfaceVars
        """
        self._var_stack.append(self)
        self.vars.__enter__()
        return self.vars
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Pop this default off the stack and deactivate its variable set.

        :param exc_type: the exception type, if any
        :param exc_val: the exception value, if any
        :param exc_tb: the traceback, if any
        """
        self._var_stack.pop()
        self.vars.__exit__(exc_type, exc_val, exc_tb)
    @classmethod
    def resolve(cls):
        """
        **LLM Docstring**

        Return the current default variable set (a fresh one if none is active).

        :return: the variable set
        :rtype: InterfaceVars
        """
        return InterfaceVars() if len(cls._var_stack) == 0 else cls._var_stack[-1].vars
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
        if name is None:
            name = uuid.uuid4()
        self.name = name
        self._old_space = None
        if dedupe:
            if name in self._namespace_cache:
                self._var_cache = self._namespace_cache[name]._var_cache
            else:
                self._var_cache = weakref.WeakValueDictionary()
                self._namespace_cache[name] = self
        else:
            self._var_cache = weakref.WeakValueDictionary()
    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation showing the name and cached variables.

        :return: the representation
        :rtype: str
        """
        return "{}({}, {})".format(
            type(self).__name__,
            self.name,
            list(self._var_cache.values())
        )
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
        if isinstance(name, VariableNamespace):
            return name
        else:
            if name not in cls._namespace_cache:
                this = VariableNamespace(name)
                cls._namespace_cache[name] = this # hold a reference...
            return cls._namespace_cache[name]
    def __contains__(self, item):
        """
        **LLM Docstring**

        Test whether a variable name is in the namespace.

        :param item: the variable name
        :return: whether it's present
        :rtype: bool
        """
        return self._var_cache.__contains__(item)
    def __getitem__(self, item):
        """
        **LLM Docstring**

        Get a variable from the namespace by name.

        :param item: the variable name
        :return: the variable
        """
        return self._var_cache[item]
    def __setitem__(self, key, value):
        """
        **LLM Docstring**

        Store a variable in the namespace under a name.

        :param key: the variable name
        :param value: the variable
        """
        self._var_cache[key] = value
    def __enter__(self):
        """
        **LLM Docstring**

        Activate this namespace as the current one, saving the previous.
        """
        self._old_space = VariableSynchronizer.current_namespace
        VariableSynchronizer.current_namespace = self
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Restore the previously active namespace.

        :param exc_type: the exception type, if any
        :param exc_val: the exception value, if any
        :param exc_tb: the traceback, if any
        """
        VariableSynchronizer.current_namespace = self._old_space
        self._old_space = None
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
        self._name = name
        self.namespace = namespace
        self.autounlink = autounlink
        self._value = value
        self.callbacks = weakref.WeakSet(callbacks)
        self.output_pane = DefaultOutputWidget.get_default() if output_pane is None else output_pane
        self._watchers = weakref.WeakKeyDictionary()
    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation showing the name and value.

        :return: the representation
        :rtype: str
        """
        return "{}({}, {!r})".format(
            type(self).__name__,
            self._name,
            self._value
        )
    @classmethod
    def create_var(cls, var, namespace=None, **opts):
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
        if namespace is None:
            namespace = cls.current_namespace
        var_cache = InterfaceVars.active_vars()
        if isinstance(var, VariableSynchronizer):
            if var_cache is not None:
                var_cache.add(var)
            return var
        else:
            if var not in namespace:
                this_var = VariableSynchronizer(var, namespace=namespace, **opts)
                namespace[var] = this_var
            if var_cache is not None:
                var_cache.add(namespace[var])
            return namespace[var]
    @property
    def name(self):
        """
        **LLM Docstring**

        The variable's name.

        :return: the name
        """
        return self._name
    @property
    def value(self):
        """
        **LLM Docstring**

        The variable's current value. Setting it propagates to linked widgets and fires
        the change callbacks.

        :return: the value
        """
        return self._value
    @value.setter
    def value(self, v):
        """
        **LLM Docstring**

        The variable's current value. Setting it propagates to linked widgets and fires
        the change callbacks.

        :return: the value
        """
        self.set_value(v)
    def set_value(self, v, caller=None):
        """
        **LLM Docstring**

        Set the value (if changed), firing the change callbacks and propagating to every
        linked widget except the caller.

        :param v: the new value
        :param caller: the widget that triggered the change (not re-notified)
        """
        with self.output_pane:
            old = self._value
            try:
                check = old != v
            except TypeError:
                check = old is not v
            if check:
                self._value = v
                for c in self.callbacks:
                    c({'var': self, 'old': old, 'new': self._value})
                for w in self._watchers:
                    if w is not caller:
                        w.value = self._value
    def link(self, widget):
        """
        **LLM Docstring**

        Link a widget to the variable: seed the variable from the widget's value, observe
        the widget for changes, and (if `autounlink`) unlink other widgets.

        :param widget: the widget to link
        """
        if self.autounlink:
            for w in list(self._watchers.keys()):
                if w is not widget:
                    self.unlink(w)
        if hasattr(widget, 'value'):
            self.set_value(widget.value, caller=widget)
            handler = lambda d: self.set_value(widget.value, caller=widget)
        else:
            handler = None
        if widget not in self._watchers:
            self._watchers[widget] = []
            if handler is not None:
                widget.observe(handler, names=['value'])
            if len(self._watchers[widget]) == 0:
                self._watchers[widget].append(handler)
    def unlink(self, widget):
        """
        **LLM Docstring**

        Unlink a widget from the variable, removing its change observers.

        :param widget: the widget to unlink
        """
        for handler in self._watchers.get(widget, []):
            try:
                widget.unobserve(handler, names=['value'])
            except ValueError:
                ...
        self._watchers.pop(widget, None)
def Var(name, namespace=None, **opts):
    """
    **LLM Docstring**

    Resolve a name (or synchronizer) to a `VariableSynchronizer`, optionally within a
    named namespace.

    :param name: the variable name or synchronizer
    :param namespace: the namespace name/object (the current one if omitted)
    :return: the variable
    :rtype: VariableSynchronizer
    """
    if namespace is not None:
        with VariableNamespace.create(namespace) as ns:
            return VariableSynchronizer.create_var(name, namespace=ns, **opts)
    else:
        return VariableSynchronizer.create_var(name, **opts)
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
        self.var = VariableSynchronizer.create_var(var)
        self.settings = settings
        if widget is None:
            widget = self._build_widget(control_type, settings)
        self.widget = widget
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
        if control_type is None:
            for checker in SettingChecker.checkers:
                if checker.check(**settings):
                    control_type = getattr(JupyterAPIs.get_widgets_api(), checker.control_type)
                    break
            else:
                control_type = JHTML.OutputArea
        return control_type(**settings)

    def to_widget(self):
        """
        **LLM Docstring**

        Link the variable to the widget and return the widget.

        :return: the widget
        """
        self.var.link(self.widget)
        return self.widget
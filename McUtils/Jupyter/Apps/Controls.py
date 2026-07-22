
import abc, uuid, numpy as np
import asyncio, traceback, sys
import time

from ..JHTML import JHTML

from .Interfaces import Component, ListGroup, Dropdown, Progress
from .Variables import Var, InterfaceVars

__all__ = [
    "Control",
    "InputField",
    "StringField",
    "Slider",
    "Checkbox",
    "RadioButton",
    "Switch",
    "TextArea",
    "Selector",
    "VariableDisplay",
    "FunctionDisplay",
    # "DropdownMenu",
    "MenuSelect",
    "DropdownSelect",
    "ProgressBar"
]

__reload_hook__ = ['.Interfaces', '.Variables']

#region JHTML Controls
class Control(Component):
    layout_orientation = 'row'
    def __init__(self, var, namespace=None):
        """
        **LLM Docstring**

        Base control component bound to a reactive variable.

        :param var: the variable (name or synchronizer) the control drives
        :param namespace: the variable namespace
        """
        self.var = Var(var, namespace=namespace) if isinstance(var, str) else var
        self._widget_cache = None
        super().__init__()
    def to_widget(self, parent=None):
        """
        **LLM Docstring**

        Render the control to a widget, linking it to its variable and syncing the initial
        value on first construction.

        :param parent: the parent component
        :return: the widget
        """
        needs_link = self._widget_cache is None
        widg = super().to_widget(parent=parent)
        if needs_link:
            val = self.var.value
            self.var.link(self)
            self.var.value = val
            self.set_value()
        return widg
    @abc.abstractmethod
    def set_value(self):
        """
        **LLM Docstring**

        Abstract: push the variable's value into the underlying widget.
        """
        ...
    @abc.abstractmethod
    def get_value(self):
        """
        **LLM Docstring**

        Abstract: read the control's current value.

        :return: the value
        """
        ...
    @property
    def value(self):
        """
        **LLM Docstring**

        The control's current value. The getter reads the widget; the setter updates the
        bound variable (as the caller) and syncs the widget.

        :return: the value
        """
        return self.get_value()
    @value.setter
    def value(self, v):
        """
        **LLM Docstring**

        The control's current value. The getter reads the widget; the setter updates the
        bound variable (as the caller) and syncs the widget.

        :return: the value
        """
        self.var.set_value(v, caller=self)
        self.set_value()
    def observe(self, fn, names=None):
        """
        **LLM Docstring**

        Observe changes on the underlying widget.

        :param fn: the change handler
        :param names: the trait name(s) to observe
        :return: the observation handle
        :raises ValueError: if the control isn't initialized
        """
        if self._widget_cache is None:
            raise ValueError("not initialized")
        return self._widget_cache.to_widget().observe(fn, names=names)
    def unobserve(self, fn, names=None):
        """
        **LLM Docstring**

        Remove a change observer from the underlying widget.

        :param fn: the handler to remove
        :param names: the trait name(s)
        """
        return self._widget_cache.to_widget().unobserve(fn, names=names)

    control_types = {}
    @classmethod
    def construct(cls, var, control_type=None, field_type=None, value=None, **attrs):
        """
        **LLM Docstring**

        Construct a control of the appropriate type (inferred from the field type/value
        if not given), from the control-type registry.

        :param var: the bound variable
        :param control_type: the control type name/class (inferred if omitted)
        :param field_type: the value's field type
        :param value: the initial value
        :param attrs: extra control attributes
        :return: the control
        :rtype: Control
        """
        if control_type is None:
            control_type = cls.infer_control(field_type=field_type, value=value, **attrs)
        if isinstance(control_type, str):
            control_type = cls.control_types[control_type]
        if value is not None:
            value = str(value)
        return control_type(var, value=value, **attrs)
    @classmethod
    def infer_control(cls, field_type=None, value=None, **ignored):
        """
        **LLM Docstring**

        Infer the control type from a field type or value (string→`StringField`,
        bool→`Checkbox`, number→`Slider`, a `range`→`Slider`).

        :param field_type: the field type
        :param value: the value (used to infer the field type)
        :param ignored: other attributes (checked for `range`)
        :return: the control class
        :rtype: type
        :raises NotImplementedError: if the type can't be inferred
        """
        if field_type is None and value is not None:
            field_type = type(value)
        if field_type is not None:
            if issubclass(field_type, str):
                return cls.control_types['StringField']
            elif issubclass(field_type, (bool,)):
                return cls.control_types['Checkbox']
            elif issubclass(field_type, (int, np.integer, float, np.floating)):
                return cls.control_types['Slider']
            else:
                raise NotImplementedError("can't infer control type for 'field_type' {}".format(field_type))
        elif 'range' in ignored:
            return cls.control_types['Slider']
        else:
            raise NotImplementedError("can't infer control type without 'field_type'")

class ValueWidget(Control):
    def __init__(self, var, value=None, namespace=None):
        """
        **LLM Docstring**

        A control backed directly by a widget's `value` trait, seeding the variable with
        an initial (or empty) value.

        :param var: the bound variable
        :param value: the initial value
        :param namespace: the variable namespace
        """
        super().__init__(var, namespace=namespace)
        if value is not None:
            self.var.value = value
        if self.var.value is None:
            self.var.value = ""
    def get_value(self):
        """
        **LLM Docstring**

        Read the value from the underlying widget (or the variable before construction),
        treating `None` as an empty string.

        :return: the value
        """
        if self._widget_cache is not None:
            val = self._widget_cache.value
            return "" if val is None else val
        else:
            return self.var.value
    def set_value(self):
        """
        **LLM Docstring**

        Push the variable's value into the underlying widget.
        """
        if self._widget_cache is not None:
            self._widget_cache.value = self.var.value
    def update(self, e):
        """
        **LLM Docstring**

        Sync the variable from the widget's current value (a change handler).

        :param e: the change event
        """
        if self._widget_cache is not None:
            self.var.value = self._widget_cache.value
class InputField(ValueWidget):
    base_cls = ['form-control']
    def __init__(self, var, value=None, tag='input', track_value=True, continuous_update=False, base_cls=None, cls=None, namespace=None, **attrs):
        """
        **LLM Docstring**

        An `<input>`-style control.

        :param var: the bound variable
        :param value: the initial value
        :param tag: the HTML tag
        :type tag: str
        :param track_value: track the widget's value trait
        :type track_value: bool
        :param continuous_update: update on every keystroke
        :type continuous_update: bool
        :param base_cls: the base CSS classes
        :param cls: extra CSS classes
        :param namespace: the variable namespace
        :param attrs: extra HTML attributes
        """
        super().__init__(var, value=value, namespace=namespace)
        if base_cls is not None:
            self.base_cls = base_cls
        attrs['cls'] = self.base_cls + JHTML.manage_class(cls)
        attrs['tag'] = tag
        attrs['track_value'] = track_value
        attrs['continuous_update'] = continuous_update
        self.attrs = attrs
    def to_jhtml(self):
        """
        **LLM Docstring**

        Render the input field to its JHTML element.

        :return: the JHTML element
        """
        # value = self.var.value
        # if value is not None and not isinstance(value, str):
        #     value = str(value)
        # self._attrs['value'] = value
        field = JHTML.Input(**self.attrs)
        return field
class StringField(InputField):
    # base_cls = ['form-text']
    def __init__(self, var, type='text', **attrs):
        """
        **LLM Docstring**

        A text input field.

        :param var: the bound variable
        :param type: the input type
        :type type: str
        :param attrs: extra attributes
        """
        super().__init__(var, type=type, **attrs)
Control.control_types['StringField'] = StringField
class Slider(InputField):
    base_cls = ['form-range']
    def __init__(self, var, type='range', value=None, range=None, **attrs):
        """
        **LLM Docstring**

        A range-slider control, deriving min/max/step from a `range` spec when given.

        :param var: the bound variable
        :param type: the input type
        :type type: str
        :param value: the initial value
        :param range: a `(min, max[, step])` range spec
        :param attrs: extra attributes
        """
        if range is not None:
            if value is None:
                value = range[0]
            min = attrs.get('min', None)
            if min is None:
                min = range[0]
            max = attrs.get('max', None)
            if max is None:
                max = range[1]
            step = attrs.get('step', None)
            if step is None:
                step = (max-min) / 25 if len(range) == 2 else range[2]
            attrs.update(
                min=min,
                max=max,
                step=step
            )
        if value is not None and not isinstance(value, str):
            value = str(value)
        super().__init__(var, type=type, value=value, **attrs)
    def get_value(self):
        """
        **LLM Docstring**

        Read the slider value, coercing it to an int or float when possible.

        :return: the numeric value
        """
        if self._widget_cache is not None:
            val = self._widget_cache.value
            try:
                val = int(val)
            except (ValueError, TypeError):
                try:
                    val = float(val)
                except (ValueError, TypeError):
                    ...
            return val
    def set_value(self):
        """
        **LLM Docstring**

        Push the variable's value into the slider (as a string).
        """
        if self._widget_cache is not None:
            v = self.var.value
            if not isinstance(v, str):
                v = str(v)
            self._widget_cache.value = v
Control.control_types['Slider'] = Slider
class Checkbox(InputField):
    base_cls = ['form-check-input']
    def __init__(self, var, type='checkbox', **attrs):
        """
        **LLM Docstring**

        A checkbox control.

        :param var: the bound variable
        :param type: the input type
        :type type: str
        :param attrs: extra attributes
        """
        super().__init__(var, type=type, **attrs)
    def get_value(self):
        """
        **LLM Docstring**

        Read the checkbox as a bool (from its `'true'`/`'false'` string).

        :return: the checked state
        :rtype: bool
        """
        if self._widget_cache is not None:
            val = self._widget_cache.value
            return isinstance(val, str) and val == "true"
    def set_value(self):
        """
        **LLM Docstring**

        Set the checkbox's `'true'`/`'false'` string from the variable's truthiness.
        """
        if self._widget_cache is not None:
            if self.var.value:
                self._widget_cache.value = 'true'
            else:
                self._widget_cache.value = 'false'
Control.control_types['Checkbox'] = Checkbox
class RadioButton(Checkbox):
    base_cls = ['form-check-input']
    def __init__(self, var, type='radio', **attrs):
        """
        **LLM Docstring**

        A radio-button control.

        :param var: the bound variable
        :param type: the input type
        :type type: str
        :param attrs: extra attributes
        """
        super().__init__(var, type=type, **attrs)
Control.control_types['RadioButton'] = RadioButton
class Switch(Checkbox):
    base_cls = ['form-check-input']
    def __init__(self, var, type='checkbox', role='switch', **attrs):
        """
        **LLM Docstring**

        A toggle-switch control (a checkbox with a `switch` role).

        :param var: the bound variable
        :param type: the input type
        :type type: str
        :param role: the ARIA role
        :type role: str
        :param attrs: extra attributes
        """
        super().__init__(var, type=type, role=role, **attrs)
    def get_value(self):
        """
        **LLM Docstring**

        Read the switch as a bool (from its inner checkbox).

        :return: the toggled state
        :rtype: bool
        """
        if self._widget_cache is not None:
            val = self._widget_cache.get_child(0).value
            return isinstance(val, str) and val == "true"
    def set_value(self):
        """
        **LLM Docstring**

        Set the switch's inner checkbox from the variable's truthiness.
        """
        if self._widget_cache is not None:
            if self.var.value:
                self._widget_cache.get_child(0).value = 'true'
            else:
                self._widget_cache.get_child(0).value = 'false'
    def to_jhtml(self):
        """
        **LLM Docstring**

        Render the switch (wrapping the checkbox in a `form-switch` div).

        :return: the JHTML element
        """
        return JHTML.Div(super().to_jhtml(), cls=['form-switch'])
Control.control_types['Switch'] = Switch
class TextArea(InputField):
    base_cls = ['form-control']
    def __init__(self, var, tag='textarea', **attrs):
        """
        **LLM Docstring**

        A multi-line text-area control.

        :param var: the bound variable
        :param tag: the HTML tag
        :type tag: str
        :param attrs: extra attributes
        """
        super().__init__(var, tag=tag, **attrs)
    def to_jhtml(self):
        """
        **LLM Docstring**

        Render the text area to its JHTML element.

        :return: the JHTML element
        """
        field = JHTML.Textarea(**self.attrs)
        return field
Control.control_types['TextArea'] = TextArea
class ChangeTracker(ValueWidget):
    base = None
    base_cls = []
    def __init__(self, var, base=None, value=None, track_value=True, continuous_update=False, base_cls=None, cls=None, **attrs):
        """
        **LLM Docstring**

        A value control that tracks changes on a configurable base widget class.

        :param var: the bound variable
        :param base: the base widget class (or its JHTML name)
        :param value: the initial value
        :param track_value: track the value trait
        :type track_value: bool
        :param continuous_update: update continuously
        :type continuous_update: bool
        :param base_cls: the base CSS classes
        :param cls: extra CSS classes
        :param attrs: extra attributes
        """
        super().__init__(var, value=value)
        base = self.base if base is None else base
        self.base = getattr(JHTML, base) if isinstance(base, str) else base
        if base_cls is not None:
            self.base_cls = base_cls
        attrs['cls'] = self.base_cls + JHTML.manage_class(cls)
        attrs['track_value'] = track_value
        attrs['continuous_update'] = continuous_update
        self.attrs = attrs
class Selector(ChangeTracker):
    base=JHTML.Select
    base_cls = ['form-select']
    def __init__(self, var, options=None, value=None, multiple=False, **attrs):
        """
        **LLM Docstring**

        A `<select>` dropdown control, single- or multi-select.

        :param var: the bound variable
        :param options: the selectable options
        :param value: the initial value (defaults to the first option)
        :param multiple: allow multiple selections
        :type multiple: bool
        :param attrs: extra attributes
        """
        self._options = self.canonicalize_options(options)
        if not multiple and value is None and len(self._options) > 0:
            value = self._options[0][1]
        if multiple:
            attrs['multiple']=True
        super().__init__(var, value=value, **attrs)
    @property
    def multiple(self):
        """
        **LLM Docstring**

        Whether the selector allows multiple selections.

        :return: the multi-select flag
        :rtype: bool
        """
        if self._widget_cache is not None:
            try:
                mult = self._widget_cache['multiple']
            except KeyError:
                mult = False
            return mult is True or mult == 'true'
        else:
            return 'multiple' in self.attrs and self.attrs['multiple']
    def get_value(self):
        """
        **LLM Docstring**

        Read the selection, splitting the multi-select value into a list.

        :return: the selected value(s)
        """
        if self._widget_cache is not None:
            val = super().get_value()
            if self.multiple:
                if val is None or val == "":
                    val = []
                else:
                    val = val.split("&&")
            elif val == "":
                val = None
            return val
    def set_value(self):
        """
        **LLM Docstring**

        Push the variable's selection into the widget (joining a multi-select list).
        """
        if self._widget_cache is not None:
            if self.multiple:
                v = self.var.value
                if not isinstance(v, str):
                    v = "&&".join(v)
                self._widget_cache.value = v
            else:
                super().set_value()
    @classmethod
    def canonicalize_options(cls, options):
        """
        **LLM Docstring**

        Normalize the options into `(label, value)` pairs.

        :param options: the options (strings or `(label, value)` pairs)
        :return: the canonicalized options
        :rtype: tuple
        """
        ops = []
        for k in options:
            if isinstance(k, str):
                v = k
            else:
                try:
                    k, v = k
                except ValueError:
                    v = k
            ops.append((k,v))
        return tuple(ops)
    def _build_options_list(self):
        """
        **LLM Docstring**

        Build the `<option>` elements, marking the currently-selected value(s).

        :return: the option elements
        :rtype: list
        """
        if self.multiple:
            vals = self.var.value
            if vals is None:
                vals = []
            elif isinstance(vals, str):
                vals = vals.split("&&")
            opts = [JHTML.Option(k, value=v, selected="true") if v in vals else JHTML.Option(k, value=v) for k,v in self._options]
        else:
            val = self.var.value
            opts = [JHTML.Option(k, value=v, selected=(val is not None and v == val)) for k,v in self._options]
        return opts
    def to_jhtml(self):
        """
        **LLM Docstring**

        Render the select element with its options.

        :return: the JHTML element
        """
        field = self.base(*self._build_options_list(), **self.attrs)
        return field
Control.control_types['Selector'] = Selector
class VariableDisplay(Control):
    def __init__(self, var, value=None, pane=None, autoclear=True, namespace=None, **attrs):
        """
        **LLM Docstring**

        A control that displays a variable's value in an output pane.

        :param var: the bound variable
        :param value: the initial value
        :param pane: the output pane (created if omitted)
        :param autoclear: clear the pane before each update
        :type autoclear: bool
        :param namespace: the variable namespace
        :param attrs: extra pane attributes
        """
        super().__init__(var, namespace=namespace)
        if pane is None:
            pane = JHTML.OutputArea(autoclear=autoclear, **attrs)
        self.out = pane
        if value is not None:
            self.var.value = value
    def get_value(self):
        """
        **LLM Docstring**

        Return the variable's value.

        :return: the value
        """
        return self.var.value
    def set_value(self):
        """
        **LLM Docstring**

        Render the variable's value into the output pane (clearing it when empty).
        """
        val = self.var.value
        if val is None or isinstance(val, str) and val == "":
            self.out.clear()
        else:
            self.out.set_output(val)
    def update(self, e):
        """
        **LLM Docstring**

        Re-render the display (a change handler).

        :param e: the change event
        """
        self.set_value()
    def to_jhtml(self):
        """
        **LLM Docstring**

        Render the display, populating the output pane.

        :return: the output pane
        """
        with self.out:
            self.set_value()
        return self.out
class FunctionDisplay(Component):
    def __init__(self, fn, vars, pane=None, autoclear=True, debounce=None, delay_time=.1, namespace=None, **attrs):
        """
        **LLM Docstring**

        A component that re-runs a function (over a set of variables) and displays its
        result whenever an input changes, with optional debouncing.

        :param fn: the function to run
        :type fn: Callable
        :param vars: the input variables
        :param pane: the output pane (created if omitted)
        :param autoclear: clear the pane before each update
        :type autoclear: bool
        :param debounce: the debounce interval (seconds)
        :param delay_time: the minimum time between calls
        :type delay_time: float
        :param namespace: the variable namespace
        :param attrs: extra pane attributes
        """
        super().__init__()
        if pane is None:
            pane = JHTML.OutputArea(autoclear=autoclear, **attrs)
        self.out = pane
        self.fn = fn
        self.debounce = debounce
        self._delayed_executor = None
        # self._executions = []
        self.vars = (
            InterfaceVars(*vars, namespace=namespace)
                if not isinstance(vars, InterfaceVars) else
            vars
        )
        self._prev_call = None
        self.delay_time = delay_time
    def link_vars(self, *var):
        """
        **LLM Docstring**

        Link the display's update handler to every input variable (and to future
        variable additions).
        """
        self.update = self.update  # weakref patch
        for v in self.vars:
            v.callbacks.add(self.update)
            v.link(self)
        self.vars.callbacks.add(self.link_vars)
    def to_widget(self, parent=None):
        """
        **LLM Docstring**

        Render to a widget, linking the input variables on first construction (with a
        temporarily relaxed debounce).

        :param parent: the parent component
        :return: the widget
        """
        needs_link = self._widget_cache is None
        dt = self.delay_time
        db = self.debounce
        try:
            self.delay_time = 1000
            self.debounce = 10
            widg = super().to_widget(parent=parent)
            if needs_link:
                self.link_vars()
        finally:
            self.delay_time = dt
            self.debounce = db
        return widg
    def observe(self, fn, names=None):
        """
        **LLM Docstring**

        Observe changes on the underlying widget.

        :param fn: the change handler
        :param names: the trait name(s)
        :return: the observation handle
        :raises ValueError: if not initialized
        """
        if self._widget_cache is None:
            raise ValueError("not initialized")
        return self._widget_cache.to_widget().observe(fn, names=names)
    def unobserve(self, fn, names=None):
        """
        **LLM Docstring**

        Remove a change observer.

        :param fn: the handler
        :param names: the trait name(s)
        """
        return self._widget_cache.to_widget().unobserve(fn, names=names)

    # directly from the jupyter docs
    async def _delayed_update(self, event):
        """
        **LLM Docstring**

        Await the debounce interval, then run the update (the async debounced path).

        :param event: the change event
        :return: the update result
        """
        await asyncio.sleep(self.debounce)
        return self._update(event)
    def update(self, event):
        """
        **LLM Docstring**

        Handle an input change: run the update immediately or schedule a debounced
        execution, honoring the minimum delay between calls and reporting errors to the
        pane.

        :param event: the change event
        """
        if self._prev_call is None or (time.time() - self._prev_call) > self.delay_time:
            self._prev_call = time.time()
            try:
                if self.debounce is not None:
                    if self._delayed_executor is not None:
                        self._delayed_executor.cancel()
                    self._delayed_executor = asyncio.ensure_future(self._delayed_update(event))
                else:
                    self._update(event)
            except:
                with self.out:
                    _, _, tb = sys.exc_info()
                    traceback.print_tb(tb)

    def _update(self, e):
        """
        **LLM Docstring**

        Run the display function over the current variable values and render its result.

        :param e: the change event
        """
        res = self.fn(event=e, pane=self, **self.vars.dict)
        self._last_res = res
        if res is not None:
            self.out.set_output(res)
            self._delayed_executor = None

    def to_jhtml(self):
        """
        **LLM Docstring**

        Render the display, running the function once to populate the pane.

        :return: the output pane
        """
        with self.out:
            self._update(None)
        return self.out

class ProgressBar(Control):
    def __init__(self, var, bar=None, **attrs):
        """
        **LLM Docstring**

        A control that drives a progress bar from a variable.

        :param var: the bound variable (the percentage)
        :param bar: the progress bar component (created if omitted)
        :param attrs: extra bar attributes
        """
        super().__init__(var)
        if bar is None:
            bar = Progress(self.value, **attrs)
        self.bar = bar
    def get_value(self):
        """
        **LLM Docstring**

        Return the variable's value, coercing empty/None to 0 and strings to ints.

        :return: the progress percentage
        """
        val = self.var.value
        if val is None or val == "":
            self.var.value = 0
        elif isinstance(val, str):
            self.var.val = int(val)
        return self.var.value
    def set_value(self):
        """
        **LLM Docstring**

        Set the bar's width from the current percentage.
        """
        self.bar.bar['width'] = str(self.value) + "%"
    def update(self, e):
        """
        **LLM Docstring**

        Re-render the bar (a change handler).

        :param e: the change event
        """
        self.set_value()
    def to_jhtml(self):
        """
        **LLM Docstring**

        Render the progress bar widget.

        :return: the widget
        """
        self.set_value()
        return self.bar.to_widget()

class MenuSelect(ValueWidget):
    menu_type = ListGroup
    def __init__(self, var, options, menu_type=None, **attrs):
        """
        **LLM Docstring**

        A control that selects a value by activating an item in a menu component (e.g. a
        list group).

        :param var: the bound variable
        :param options: the menu options
        :param menu_type: the menu component class
        :param attrs: extra menu attributes
        """
        super().__init__(var)
        self._value_map, self.ops = self.canonicalize_options(options)
        if menu_type is not None:
            self.menu_type = menu_type
        self._obj = self.menu_type(self.ops, **attrs) #type: MenuComponent
        self._active_item = None
    def get_value(self):
        """
        **LLM Docstring**

        Return the value mapped to the currently active item.

        :return: the value
        """
        if self._active_item is not None:
            return self._value_map[self._active_item]
    def set_value(self):
        """
        **LLM Docstring**

        Activate the menu item matching the variable's value.
        """
        self.set_active(self.var.value)
    def update(self, e):
        """
        **LLM Docstring**

        Activate the item matching the current value (a change handler).

        :param e: the change event
        """
        self.set_active(self.value)
    def set_active(self, v):
        """
        **LLM Docstring**

        Activate the menu item whose mapped value equals `v`.

        :param v: the value to select
        """
        for k, test in self._value_map.items():
            if test == v:
                break
        else:
            k = None
        if k is not None:
            self.set_active_key(k)
    def set_active_key(self, k):
        """
        **LLM Docstring**

        Activate the menu item with the given key, deactivating the previously active one.

        :param k: the item key
        """
        if len(self._obj._item_map) > 0:
            if (
                    self._active_item is not None
                    and k != self._active_item
            ):
                cur = self._obj._item_map[self._active_item]
                if cur is not None:
                    cur.remove_class('active')
            self._active_item = k
            new = self._obj._item_map[k]
            if new is not None:
                new.add_class('active')
    def onclick(self, e, i, v):
        """
        **LLM Docstring**

        Handle a menu-item click: set the variable and activate the item.

        :param e: the click event
        :param i: the item id
        :param v: the item's value
        """
        self.var.set_value(v, caller=self)
        # with self.logger_pane:
        self.set_active(v)

    def canonicalize_options(self, options):
        """
        **LLM Docstring**

        Normalize the menu options into item dicts (with ids and click handlers) and a
        `{id: value}` value map.

        :param options: the options
        :return: `(value_map, item_dicts)`
        :rtype: tuple
        """
        ops = []
        val_dict = {}
        for k in options:
            if not isinstance(k, dict):
                if isinstance(k, str):
                    v = k
                else:
                    try:
                        k, v = k
                    except (TypeError, ValueError):
                        v = k
                k = {
                    'body':k,
                    'value':v
                }
            if 'id' not in k:
                uid = str(uuid.uuid4()).replace("-", "")
                k['id'] = uid
            val_dict[k['id']] = k['value']
            k['event_handlers'] = {'click':lambda *e,i=k['id'],v=k['value']:self.onclick(e, i, v)}
            ops.append(k)
        return val_dict, tuple(ops)
    def to_jhtml(self):
        """
        **LLM Docstring**

        Render the menu widget and activate the initial item.

        :return: the widget
        """
        widg = self._obj.to_jhtml()
        init_key = next(iter(self._value_map.keys()))
        self.set_active(init_key)
        return widg

class DropdownSelect(ValueWidget):
    menu_type = Dropdown
    def __init__(self, var, options, name=None, menu_type=None, **attrs):
        """
        **LLM Docstring**

        A control that selects a value from a dropdown menu.

        :param var: the bound variable
        :param options: the dropdown options
        :param name: the dropdown label (defaults to the variable name)
        :param menu_type: the dropdown component class
        :param attrs: extra attributes
        """
        super().__init__(var)
        if menu_type is not None:
            self.menu_type = menu_type
        self.selector = MenuSelect(var, options, menu_type=self.menu_type.List)
        if name is None:
            name = self.var.name
        self.name = name
        self.attrs = attrs

    def get_value(self):
        """
        **LLM Docstring**

        Return the selected value (from the inner menu selector).

        :return: the value
        """
        return self.selector.get_value()
    def set_value(self):
        """
        **LLM Docstring**

        Sync the inner menu selector to the variable's value.
        """
        self.selector.set_value()
    def update(self, e):
        """
        **LLM Docstring**

        Update the inner menu selector (a change handler).

        :param e: the change event
        """
        self.selector.update(e)
    def to_jhtml(self):
        """
        **LLM Docstring**

        Render the dropdown with its menu selector.

        :return: the JHTML element
        """
        return self.menu_type(
            self.name,
            self.selector.to_widget(),
            **self.attrs
        ).to_jhtml()

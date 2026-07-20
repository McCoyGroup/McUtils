import abc, uuid, numpy as np
import asyncio, traceback, sys
import time
from ..JHTML import JHTML
from .Interfaces import Component, ListGroup, Dropdown, Progress
from .Variables import Var, InterfaceVars
__all__ = ['Control', 'InputField', 'StringField', 'Slider', 'Checkbox', 'RadioButton', 'Switch', 'TextArea', 'Selector', 'VariableDisplay', 'FunctionDisplay', 'MenuSelect', 'DropdownSelect', 'ProgressBar']
__reload_hook__ = ['.Interfaces', '.Variables']

class Control(Component):
    layout_orientation = 'row'

    def __init__(self, var, namespace=None):
        """
        **LLM Docstring**

        Base control component bound to a reactive variable.

        :param var: the variable (name or synchronizer) the control drives
        :param namespace: the variable namespace
        """
        ...

    def to_widget(self, parent=None):
        """
        **LLM Docstring**

        Render the control to a widget, linking it to its variable and syncing the initial
        value on first construction.

        :param parent: the parent component
        :return: the widget
        """
        ...

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
        ...

    @value.setter
    def value(self, v):
        """
        **LLM Docstring**

        The control's current value. The getter reads the widget; the setter updates the
        bound variable (as the caller) and syncs the widget.

        :return: the value
        """
        ...

    def observe(self, fn, names=None):
        """
        **LLM Docstring**

        Observe changes on the underlying widget.

        :param fn: the change handler
        :param names: the trait name(s) to observe
        :return: the observation handle
        :raises ValueError: if the control isn't initialized
        """
        ...

    def unobserve(self, fn, names=None):
        """
        **LLM Docstring**

        Remove a change observer from the underlying widget.

        :param fn: the handler to remove
        :param names: the trait name(s)
        """
        ...
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
        ...

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
        ...

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
        ...

    def get_value(self):
        """
        **LLM Docstring**

        Read the value from the underlying widget (or the variable before construction),
        treating `None` as an empty string.

        :return: the value
        """
        ...

    def set_value(self):
        """
        **LLM Docstring**

        Push the variable's value into the underlying widget.
        """
        ...

    def update(self, e):
        """
        **LLM Docstring**

        Sync the variable from the widget's current value (a change handler).

        :param e: the change event
        """
        ...

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
        ...

    def to_jhtml(self):
        """
        **LLM Docstring**

        Render the input field to its JHTML element.

        :return: the JHTML element
        """
        ...

class StringField(InputField):

    def __init__(self, var, type='text', **attrs):
        """
        **LLM Docstring**

        A text input field.

        :param var: the bound variable
        :param type: the input type
        :type type: str
        :param attrs: extra attributes
        """
        ...
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
        ...

    def get_value(self):
        """
        **LLM Docstring**

        Read the slider value, coercing it to an int or float when possible.

        :return: the numeric value
        """
        ...

    def set_value(self):
        """
        **LLM Docstring**

        Push the variable's value into the slider (as a string).
        """
        ...
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
        ...

    def get_value(self):
        """
        **LLM Docstring**

        Read the checkbox as a bool (from its `'true'`/`'false'` string).

        :return: the checked state
        :rtype: bool
        """
        ...

    def set_value(self):
        """
        **LLM Docstring**

        Set the checkbox's `'true'`/`'false'` string from the variable's truthiness.
        """
        ...
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
        ...
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
        ...

    def get_value(self):
        """
        **LLM Docstring**

        Read the switch as a bool (from its inner checkbox).

        :return: the toggled state
        :rtype: bool
        """
        ...

    def set_value(self):
        """
        **LLM Docstring**

        Set the switch's inner checkbox from the variable's truthiness.
        """
        ...

    def to_jhtml(self):
        """
        **LLM Docstring**

        Render the switch (wrapping the checkbox in a `form-switch` div).

        :return: the JHTML element
        """
        ...
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
        ...

    def to_jhtml(self):
        """
        **LLM Docstring**

        Render the text area to its JHTML element.

        :return: the JHTML element
        """
        ...
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
        ...

class Selector(ChangeTracker):
    base = JHTML.Select
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
        ...

    @property
    def multiple(self):
        """
        **LLM Docstring**

        Whether the selector allows multiple selections.

        :return: the multi-select flag
        :rtype: bool
        """
        ...

    def get_value(self):
        """
        **LLM Docstring**

        Read the selection, splitting the multi-select value into a list.

        :return: the selected value(s)
        """
        ...

    def set_value(self):
        """
        **LLM Docstring**

        Push the variable's selection into the widget (joining a multi-select list).
        """
        ...

    @classmethod
    def canonicalize_options(cls, options):
        """
        **LLM Docstring**

        Normalize the options into `(label, value)` pairs.

        :param options: the options (strings or `(label, value)` pairs)
        :return: the canonicalized options
        :rtype: tuple
        """
        ...

    def _build_options_list(self):
        """
        **LLM Docstring**

        Build the `<option>` elements, marking the currently-selected value(s).

        :return: the option elements
        :rtype: list
        """
        ...

    def to_jhtml(self):
        """
        **LLM Docstring**

        Render the select element with its options.

        :return: the JHTML element
        """
        ...
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
        ...

    def get_value(self):
        """
        **LLM Docstring**

        Return the variable's value.

        :return: the value
        """
        ...

    def set_value(self):
        """
        **LLM Docstring**

        Render the variable's value into the output pane (clearing it when empty).
        """
        ...

    def update(self, e):
        """
        **LLM Docstring**

        Re-render the display (a change handler).

        :param e: the change event
        """
        ...

    def to_jhtml(self):
        """
        **LLM Docstring**

        Render the display, populating the output pane.

        :return: the output pane
        """
        ...

class FunctionDisplay(Component):

    def __init__(self, fn, vars, pane=None, autoclear=True, debounce=None, delay_time=0.1, namespace=None, **attrs):
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
        ...

    def link_vars(self, *var):
        """
        **LLM Docstring**

        Link the display's update handler to every input variable (and to future
        variable additions).
        """
        ...

    def to_widget(self, parent=None):
        """
        **LLM Docstring**

        Render to a widget, linking the input variables on first construction (with a
        temporarily relaxed debounce).

        :param parent: the parent component
        :return: the widget
        """
        ...

    def observe(self, fn, names=None):
        """
        **LLM Docstring**

        Observe changes on the underlying widget.

        :param fn: the change handler
        :param names: the trait name(s)
        :return: the observation handle
        :raises ValueError: if not initialized
        """
        ...

    def unobserve(self, fn, names=None):
        """
        **LLM Docstring**

        Remove a change observer.

        :param fn: the handler
        :param names: the trait name(s)
        """
        ...

    async def _delayed_update(self, event):
        """
        **LLM Docstring**

        Await the debounce interval, then run the update (the async debounced path).

        :param event: the change event
        :return: the update result
        """
        ...

    def update(self, event):
        """
        **LLM Docstring**

        Handle an input change: run the update immediately or schedule a debounced
        execution, honoring the minimum delay between calls and reporting errors to the
        pane.

        :param event: the change event
        """
        ...

    def _update(self, e):
        """
        **LLM Docstring**

        Run the display function over the current variable values and render its result.

        :param e: the change event
        """
        ...

    def to_jhtml(self):
        """
        **LLM Docstring**

        Render the display, running the function once to populate the pane.

        :return: the output pane
        """
        ...

class ProgressBar(Control):

    def __init__(self, var, bar=None, **attrs):
        """
        **LLM Docstring**

        A control that drives a progress bar from a variable.

        :param var: the bound variable (the percentage)
        :param bar: the progress bar component (created if omitted)
        :param attrs: extra bar attributes
        """
        ...

    def get_value(self):
        """
        **LLM Docstring**

        Return the variable's value, coercing empty/None to 0 and strings to ints.

        :return: the progress percentage
        """
        ...

    def set_value(self):
        """
        **LLM Docstring**

        Set the bar's width from the current percentage.
        """
        ...

    def update(self, e):
        """
        **LLM Docstring**

        Re-render the bar (a change handler).

        :param e: the change event
        """
        ...

    def to_jhtml(self):
        """
        **LLM Docstring**

        Render the progress bar widget.

        :return: the widget
        """
        ...

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
        ...

    def get_value(self):
        """
        **LLM Docstring**

        Return the value mapped to the currently active item.

        :return: the value
        """
        ...

    def set_value(self):
        """
        **LLM Docstring**

        Activate the menu item matching the variable's value.
        """
        ...

    def update(self, e):
        """
        **LLM Docstring**

        Activate the item matching the current value (a change handler).

        :param e: the change event
        """
        ...

    def set_active(self, v):
        """
        **LLM Docstring**

        Activate the menu item whose mapped value equals `v`.

        :param v: the value to select
        """
        ...

    def set_active_key(self, k):
        """
        **LLM Docstring**

        Activate the menu item with the given key, deactivating the previously active one.

        :param k: the item key
        """
        ...

    def onclick(self, e, i, v):
        """
        **LLM Docstring**

        Handle a menu-item click: set the variable and activate the item.

        :param e: the click event
        :param i: the item id
        :param v: the item's value
        """
        ...

    def canonicalize_options(self, options):
        """
        **LLM Docstring**

        Normalize the menu options into item dicts (with ids and click handlers) and a
        `{id: value}` value map.

        :param options: the options
        :return: `(value_map, item_dicts)`
        :rtype: tuple
        """
        ...

    def to_jhtml(self):
        """
        **LLM Docstring**

        Render the menu widget and activate the initial item.

        :return: the widget
        """
        ...

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
        ...

    def get_value(self):
        """
        **LLM Docstring**

        Return the selected value (from the inner menu selector).

        :return: the value
        """
        ...

    def set_value(self):
        """
        **LLM Docstring**

        Sync the inner menu selector to the variable's value.
        """
        ...

    def update(self, e):
        """
        **LLM Docstring**

        Update the inner menu selector (a change handler).

        :param e: the change event
        """
        ...

    def to_jhtml(self):
        """
        **LLM Docstring**

        Render the dropdown with its menu selector.

        :return: the JHTML element
        """
        ...
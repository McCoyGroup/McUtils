"""
Smoke/regression tests for `McUtils.Jupyter.Apps` itself, drafted from the
`McUtils/stubs/McUtils/Jupyter/Apps` docstrings (`Variables.py`, `Controls.py`,
`Interfaces.py`, `Apps.py`).

`McUtils.Jupyter.Apps` is a reactive-widget framework meant to run inside a
live Jupyter kernel; outside one, the most meaningful thing to verify
headlessly is that (a) the reactive `Var`/`VariableSynchronizer` machinery
works in plain Python, and (b) every component actually *constructs* and
renders to a real `ipywidget` (via `.to_widget()`) without raising, since
that's the code path a live notebook actually exercises. `ipywidgets` is a
pure-Python package with no system dependency, so it's installed here (via
pip) to make that possible; `Peeves.TestUtils` is not used, matching the rest
of this batch.
"""

import unittest

from McUtils.Jupyter import (
    Var,
    VariableSynchronizer,
    VariableDisplay,
    FunctionDisplay,
    Slider,
    Checkbox,
    StringField,
    Selector,
    Manipulator,
    App,
    Card,
    CardHeader,
    CardBody,
    Table,
)


class JupyterAppsFrameworkTests(unittest.TestCase):
    """Exercises the reactive `Var` machinery and confirms every core component builds a real widget."""

    # region Variables: Var / VariableSynchronizer

    def test_VarCreatesAndReusesSynchronizer(self):
        """`Var(name)` returns a `VariableSynchronizer`, and calling it again with the same name returns the *same* one."""
        v1 = Var('framework_test_var_a')
        v2 = Var('framework_test_var_a')
        self.assertIsInstance(v1, VariableSynchronizer)
        self.assertIs(v1, v2)

    def test_VarDifferentNamesAreDistinct(self):
        """Two different variable names resolve to two distinct synchronizers."""
        v1 = Var('framework_test_var_b')
        v2 = Var('framework_test_var_c')
        self.assertIsNot(v1, v2)

    def test_VariableValueSetAndGet(self):
        """Setting `.value` on a `Var` stores and returns exactly that value."""
        v = Var('framework_test_var_d')
        v.value = 42
        self.assertEqual(v.value, 42)
        v.value = 'hello'
        self.assertEqual(v.value, 'hello')

    def test_VariableChangeCallbackFires(self):
        """A callback registered via the `callbacks` constructor argument fires when the value changes."""
        seen = []

        def on_change(e):
            seen.append(e['new'])

        # VariableSynchronizer.callbacks is a weakref.WeakSet, so the callback
        # must be kept alive by a strong reference (like on_change here) for
        # the duration of the test -- a bare inline lambda would be garbage
        # collected immediately and silently never fire.
        v = VariableSynchronizer('framework_test_var_e', value=0, callbacks=[on_change])
        v.value = 1
        v.value = 2
        self.assertEqual(seen, [1, 2])

    def test_VariableNoCallbackFireOnSameValue(self):
        """Setting a variable to its current value again does not re-fire change callbacks."""
        seen = []

        def on_change(e):
            seen.append(e['new'])

        v = VariableSynchronizer('framework_test_var_f', value=0, callbacks=[on_change])
        v.value = 5
        v.value = 5  # unchanged -- should not fire again
        self.assertEqual(seen, [5])

    # endregion

    # region Controls: construction -> real ipywidget

    def test_SliderBuildsRealWidget(self):
        """`Slider` builds a real `ipywidget`-backed input element."""
        w = Slider(Var('framework_slider'), value=5, range=(0, 10, 1)).to_widget()
        self.assertTrue(hasattr(w, 'widget') or hasattr(w, 'value') or w is not None)

    def test_CheckboxBuildsRealWidget(self):
        """`Checkbox` builds a real `ipywidget`-backed input element."""
        w = Checkbox(Var('framework_checkbox')).to_widget()
        self.assertIsNotNone(w)

    def test_StringFieldBuildsRealWidget(self):
        """`StringField` builds a real `ipywidget`-backed input element."""
        w = StringField(Var('framework_string')).to_widget()
        self.assertIsNotNone(w)

    def test_VariableDisplayBuildsRealWidget(self):
        """`VariableDisplay` builds a real output-area widget."""
        w = VariableDisplay(Var('framework_display')).to_widget()
        self.assertIsNotNone(w)

    def test_FunctionDisplayReactsToVariableChange(self):
        """`FunctionDisplay` re-runs its function and reflects the new value once its bound variable changes."""
        calls = []

        def render(**kwargs):
            calls.append(kwargs.get('framework_fd_x'))
            return str(kwargs.get('framework_fd_x'))

        x = Var('framework_fd_x')
        x.value = 1
        fd = FunctionDisplay(render, [x])
        fd.to_widget()
        self.assertIn(1, calls)

        x.value = 2
        self.assertIn(2, calls)

    # endregion

    # region Manipulator / App: full component construction

    def test_ManipulatorBuildsRealWidget(self):
        """`Manipulator` (an ipywidgets-`interact`-style Card) constructs and renders to a real widget."""
        def render(n=1, **_ignored):
            return Card(CardBody(f"n={n}"))

        m = Manipulator(render, ('n', dict(value=1, min=0, max=10)))
        w = m.to_widget()
        self.assertIsNotNone(w)

    def test_AppBuildsRealWidget(self):
        """A minimal `App` (header + body) constructs and renders to a real widget."""
        app = App(
            header=Card(CardHeader("Framework Smoke Test")),
            body=Card(CardBody("hello")),
        )
        w = app.to_widget()
        self.assertIsNotNone(w)

    def test_TableBuildsRealWidgetWithHeadings(self):
        """`Table` with an explicit list of column headings (not a bare `True`/`False`) constructs and renders."""
        t = Table([['a', '1'], ['b', '2']], table_headings=['Key', 'Value'])
        w = t.to_widget()
        self.assertIsNotNone(w)

    # endregion

    # region Selector: real bug found while building the dashboard

    def test_SelectorBuildsRealWidget(self):
        """`Selector`'s live-widget path (`.to_widget()`, what an actual Jupyter kernel uses) works fine."""
        w = Selector(Var('framework_selector'), options=['a', 'b', 'c'], value='a').to_widget()
        self.assertIsNotNone(w)

    def test_SelectorStaticHtmlExportRegression(self):
        """
        `Selector.to_jhtml()` marks each `<option>` with a literal Python
        `selected=True`/`selected=False` attribute (see `_build_options_list`)
        rather than a proper HTML boolean-attribute encoding. That's harmless
        for the live-widget path above, but the static-HTML export path
        (`element.to_html().tostring()` -- used by, e.g., `display_in_browser`
        or dumping a notebook to standalone HTML) crashes: the underlying
        `xml.etree.ElementTree` HTML serializer raises `TypeError: cannot
        serialize True (type bool)` the moment it hits a `True`-valued
        attribute. This reproduces that crash directly and confirms it's
        specific to the static-export path.
        """
        sel = Selector(Var('framework_selector_export'), options=['a', 'b', 'c'], value='a')
        elem = sel.to_jhtml()
        html_tree = elem.to_html()

        # confirm the root cause: a literal Python bool sitting in the attribute dict
        option_attrs = [child.attrs for child in html_tree.elems]
        self.assertTrue(any(attrs.get('selected') is True for attrs in option_attrs))

        with self.assertRaises(TypeError):
            html_tree.tostring()

    # endregion


if __name__ == '__main__':
    unittest.main(verbosity=2)

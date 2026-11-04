"""The jdoc Run control is built from JHTML elements, and the ActiveHTMLWidget extension check."""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import types
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))


def have_widgets():
    try:
        import ipywidgets, markdown  # noqa: F401
    except ImportError:
        return False
    return True


BLOCKS = (
    '<!-- readout(id="c-1") -->\n```python\nimport numpy as np\nnp.arange(3)\n```\n\n'
    '<!-- readout(id="c-2") -->\n```python\n1/0\n```\n\n'
    '<!-- readout(id="c-3") -->\n```python\n"<b>not markup</b>"\n```\n\n'
)


def parts(control):
    """The wrappers behind the button and output area of a control."""
    from McUtils.Jupyter.JHTML.HTMLWidgets import ActiveHTMLWrapper
    return [ActiveHTMLWrapper._subwrappers[k] for k in control.elem.children]


@unittest.skipUnless(have_widgets(), "ipywidgets/markdown not installed")
class RunControlTests(unittest.TestCase):
    def setUp(self):
        from McUtils.Docs.ExampleLive import LiveExamplePage
        self.page = LiveExamplePage(BLOCKS, owner="controls.demo")
        self.displayed()      # keep the runtime script out of the test output

    def click(self, button):
        button._event_handlers["click"]({"type": "click"})

    def test_the_control_is_made_of_jhtml_elements(self):
        from McUtils.Jupyter import JHTML
        from McUtils.Jupyter.JHTML.HTMLWidgets import ActiveHTMLWrapper
        control = self.page.control("c-1")
        self.assertIsInstance(control, ActiveHTMLWrapper)
        button, out = parts(control)
        self.assertIsInstance(button, JHTML.HTMLWidgets.Button)
        self.assertEqual(button.elem.tagName, "button")
        self.assertIn("click", button.elem.eventPropertiesDict)
        self.assertEqual(out.elem.tagName, "div")
        self.assertNotIsInstance(out, JHTML.HTMLWidgets.OutputArea)   # no ipywidgets Output underneath

    def test_clicking_runs_the_block_and_writes_into_the_output_element(self):
        button, out = parts(self.page.control("c-1"))
        self.assertEqual(out.elem.innerHTML, "")
        self.click(button)
        self.assertIn("mcr-root", out.elem.innerHTML)
        self.assertIn("shape (3,)", out.elem.innerHTML)
        self.assertEqual(len(out.elem.children), 0)

    def test_a_failure_is_shown_escaped_and_does_not_raise(self):
        button, out = parts(self.page.control("c-2"))
        self.click(button)
        html = out.elem.innerHTML
        self.assertTrue(html.startswith("<pre>"))
        self.assertIn("ZeroDivisionError", html)
        self.assertNotIn("<example", html)          # the file name is escaped, not parsed as a tag
        self.assertNotIn("ExampleLive.py", html)    # nothing of the machinery in the traceback

    def test_the_button_goes_after_a_successful_run_but_stays_after_a_failure(self):
        ok_button, _ = parts(self.page.control("c-1"))
        self.click(ok_button)
        self.assertEqual(ok_button.elem.styleDict.get("display"), "none")
        bad_button, _ = parts(self.page.control("c-2"))
        self.click(bad_button)
        self.assertNotEqual(bad_button.elem.styleDict.get("display"), "none")

    def test_text_values_are_escaped_not_injected(self):
        button, out = parts(self.page.control("c-3"))
        self.click(button)
        self.assertNotIn("<b>not markup</b>", out.elem.innerHTML)

    def test_a_block_with_stored_output_shows_it_and_has_no_run_button(self):
        from McUtils.Docs.Examples import ExampleRunner, ReadoutStore
        with tempfile.TemporaryDirectory() as tmp:
            store = ReadoutStore(os.path.join(tmp, "readouts"))
            ExampleRunner(store, timeout=20).run_text(BLOCKS.split("<!-- readout(id=\"c-2\")")[0], owner="controls.demo")
            from McUtils.Docs.ExampleLive import LiveExamplePage
            page = LiveExamplePage(BLOCKS, owner="controls.demo", store=store)
            stored = parts(page.control("c-1"))
            self.assertEqual(len(stored), 1)                            # just the output
            self.assertIn("mcr-root", stored[0].elem.innerHTML)
            self.assertNotIn("c-1", page._ran)
            self.assertEqual(len(parts(page.control("c-2"))), 2)         # nothing stored for c-2: button and output
            button, bare = parts(page.control("c-1", show_stored=False))
            self.assertEqual(bare.elem.innerHTML, "")                    # stored output ignored: runnable
            self.click(button)
            self.assertIn("mcr-root", bare.elem.innerHTML)

    def test_a_block_from_another_parse_of_the_same_text_runs(self):
        """`split_examples` parses separately from the page; the engine hands those blocks to `control`."""
        from McUtils.Docs.ExampleLive import split_examples
        pieces = [p for kind, p in split_examples(BLOCKS, "controls.demo") if kind != "text"]
        self.assertIsNot(pieces[0], self.page.blocks[0])
        button, out = parts(self.page.control(pieces[0]))
        self.click(button)
        self.assertIn("shape (3,)", out.elem.innerHTML)
        self.assertNotIn("not in list", out.elem.innerHTML)

    def test_the_run_button_takes_the_apps_theme(self):
        button, out = parts(self.page.control("c-1"))
        classes = button.elem.classList
        self.assertIn("mcui-button", classes)               # native theme styling, not the browser default
        self.assertIn("mcr-run", classes)

    def test_place_accepts_markup_elements_and_widgets(self):
        from McUtils.Docs.ExampleLive import LiveExamplePage, Fragment
        from McUtils.Jupyter import JHTML
        out = JHTML.Div(dynamic=True)
        LiveExamplePage.place(out, Fragment("<i>ready</i>"))
        self.assertEqual(out.elem.innerHTML, "<i>ready</i>")
        LiveExamplePage.place(out, "<script>x</script>")
        self.assertNotIn("<script>", out.elem.innerHTML)
        LiveExamplePage.place(out, JHTML.Span("plain"))
        self.assertIn("<span>plain</span>", out.elem.innerHTML)
        LiveExamplePage.place(out, JHTML.Button("live", event_handlers={"click": lambda *a: None}))
        self.assertEqual(len(out.elem.children), 1)
        self.assertEqual(out.elem.innerHTML, "")
        LiveExamplePage.place(out, "text again")
        self.assertEqual(len(out.elem.children), 0)
        with self.assertRaises(TypeError):
            LiveExamplePage.place(out, 5)

    def displayed(self):
        """Patches the display API; returns the list of things shown through it."""
        from McUtils.Jupyter.JHTML.WidgetTools import JupyterAPIs
        shown = []
        fake = types.SimpleNamespace(display=lambda *a, **k: shown.extend(a), HTML=lambda s: ("html", s))
        patcher = mock.patch.object(JupyterAPIs, "get_display_api", classmethod(lambda cls: fake))
        patcher.start()
        self.addCleanup(patcher.stop)
        return shown

    def test_scene_output_is_written_like_any_other_fragment(self):
        from McUtils.Docs.ExampleLive import LiveExamplePage
        from McUtils.Jupyter import JHTML
        from McUtils.Readouts.Renderers.HTML import FragmentResult
        out = JHTML.Div(dynamic=True)
        scene = FragmentResult("<div class=\"mcr-root\"><X3D></X3D></div>", {"x3dom"}, {"x3dom": {"script": "s.js"}})
        LiveExamplePage.place(out, scene)
        self.assertIn("<X3D>", out.elem.innerHTML)
        self.assertEqual(len(out.elem.children), 0)
        self.assertEqual(out.elem.jsHandlers, {})              # no JavaScript handlers involved

    def test_the_x3dom_watcher_is_shown_once_per_page_where_jdoc_is_called(self):
        shown = self.displayed()
        self.page.control("c-1")
        self.page.control("c-2")
        self.assertEqual(len(shown), 1)
        kind, markup = shown[0]
        self.assertEqual(kind, "html")
        self.assertTrue(markup.startswith("<script>"))
        self.assertIn("x3dom", markup)
        self.assertNotIn("__RUNTIME__", markup)
        from McUtils.Plots.X3DInterface import X3D
        self.assertIn(X3D.X3DOM_JS, markup)                    # the default runtime location
        self.assertIn(X3D.X3DOM_CSS, markup)

    def test_a_runner_with_a_published_x3dom_url_is_respected(self):
        from McUtils.Docs.ExampleLive import LiveExamplePage
        from McUtils.Docs.Examples import ExampleRunner
        shown = self.displayed()
        page = LiveExamplePage(BLOCKS, owner="controls.demo", runner=ExampleRunner(None, x3dom_path="https://x.org/x3dom.js"))
        page.show_runtime()
        self.assertIn("https://x.org/x3dom.js", shown[0][1])
        shown.clear()
        page = LiveExamplePage(BLOCKS, owner="controls.demo", runner=ExampleRunner(None, x3dom_path="local"))
        page.show_runtime()                                     # 'local' can't be used in a notebook: falls back
        self.assertEqual(len(shown), 1)

    @unittest.skipUnless(shutil.which("node"), "node not installed")
    def test_the_watcher_is_valid_javascript(self):
        from McUtils.Docs.ExampleEmbed import X3DOM_WATCHER_JS
        script = X3DOM_WATCHER_JS.replace("__RUNTIME__", json.dumps({"script": "s.js", "stylesheet": "c.css"}))
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "watcher.js")
            with open(path, "w") as f:
                f.write(script)
            done = subprocess.run(["node", "--check", path], capture_output=True, text=True)
            self.assertEqual(done.returncode, 0, done.stderr)

    def test_example_live_never_imports_ipywidgets_or_ipython_display(self):
        import McUtils.Docs.ExampleLive as module
        with open(module.__file__) as f:
            source = f.read()
        self.assertIsNone(re.search(r"^\s*(from|import)\s+ipywidgets", source, re.M))
        self.assertNotIn("IPython.display", source)
        self.assertNotIn("set_output", source)

    def test_the_engine_composes_the_controls_into_the_doc_tree(self):
        from McUtils.Docs.DocWalker import InteractiveTemplateEngine
        out = InteractiveTemplateEngine().format_examples(BLOCKS)
        self.assertTrue(hasattr(out, "get_mime_bundle"))


class TrivialReadoutTests(unittest.TestCase):
    """A readout that says next to nothing (a bare number) is suppressed unless asked for."""

    @staticmethod
    def example(src, **options):
        from McUtils.Docs.Examples import ExampleParser
        opts = "".join(', {}={!r}'.format(k, v) for k, v in options.items())
        text = '<!-- readout(id="t-1"{}) -->\n```python\n{}\n```\n'.format(opts, src)
        return ExampleParser.parse(text).blocks[0]

    def test_node_triviality(self):
        import numpy as np
        from McUtils.Readouts.Nodes import Readout, ReadoutSection, ReadoutFields, ReadoutText, ReadoutTable
        from McUtils.Readouts.Renderers.Base import is_trivial
        from McUtils.Readouts.Interface import RecordReadout
        one = ReadoutFields([], meta={"trivial": True})
        self.assertTrue(is_trivial(one))
        self.assertTrue(is_trivial(ReadoutText("  ")))
        self.assertFalse(is_trivial(ReadoutText("something to read")))
        # a container is only non-trivial if something inside it is
        nested = Readout(ReadoutSection(ReadoutSection(one, id="b"), id="a"), title="x")
        self.assertTrue(is_trivial(nested))
        self.assertFalse(is_trivial(Readout(ReadoutSection(ReadoutSection(one, ReadoutText("hello"), id="b"), id="a"))))
        self.assertTrue(is_trivial(Readout()))
        self.assertTrue(is_trivial(RecordReadout(np.int64(1)).to_readout()))
        self.assertFalse(is_trivial(RecordReadout({"a": 1, "b": 2}).to_readout()))
        self.assertFalse(is_trivial(RecordReadout({"a": 1}).to_readout()))   # one named field is still a record
        self.assertFalse(is_trivial(ReadoutFields([])))

    def test_view_suppresses_by_default(self):
        import numpy as np
        from McUtils.Docs.Examples import ExampleView
        block = self.example("np.int64(1)")
        self.assertIsNone(ExampleView(block, np.int64(1)).node())
        self.assertIsNone(ExampleView(block, np.int64(1)).to_fragment())
        self.assertIsNotNone(ExampleView(block, np.int64(1), show_trivial=True).node())
        self.assertIsNotNone(ExampleView(self.example("np.int64(1)", show_trivial=True), np.int64(1)).node())
        self.assertIsNotNone(ExampleView(block, {"a": 1, "b": 2}).node())

    def test_live_page_reports_empty(self):
        from McUtils.Docs.ExampleLive import LiveExamplePage
        text = '<!-- readout(id="t-1") -->\n```python\nimport numpy as np\nnp.int64(1)\n```\n'
        page = LiveExamplePage(text, imports=False)
        self.assertEqual(page.try_run(page.blocks[0]).status, "empty")
        page = LiveExamplePage(text.replace('id="t-1"', 'id="t-1", show_trivial=True'), imports=False)
        self.assertEqual(page.try_run(page.blocks[0]).status, "ok")


@unittest.skipUnless(have_widgets(), "ipywidgets/markdown not installed")
class MemberIndexTests(unittest.TestCase):
    """A module's members are links; a member's page is built when its link is clicked."""

    def setUp(self):
        from McUtils.Docs.DocWalker import InteractiveTemplateEngine
        from McUtils.Jupyter import JHTML
        self.JHTML = JHTML
        self.engine = InteractiveTemplateEngine()
        self.built = []
        outer = self

        def make(name):
            outer.built.append(name)
            return JHTML.Div("page of " + name)

        class Tree(dict):
            def get(self, k, default=None):
                return {"output": make(k)} if k in ("m.eager",) else default
        self.owner = types.SimpleNamespace(tree=Tree(), obj=types.SimpleNamespace(lazy=len))

    def walk(self, wrapper, out=None):
        from McUtils.Jupyter.JHTML.HTMLWidgets import ActiveHTMLWrapper
        out = [] if out is None else out
        elem = getattr(wrapper, "elem", wrapper)
        for k in getattr(elem, "children", []):
            child = ActiveHTMLWrapper._subwrappers.get(k)
            if child is not None:
                out.append(child)
                self.walk(child, out)
        return out

    def parts(self, index):
        """The header buttons and the (lazy) content slots of the member sections, in order."""
        found = self.walk(index)
        buttons = [w for w in found if w.elem.tagName == "button" and "click" in w._event_handlers]
        slots = [w for w in found if "mcui-doc-member" in (w.elem.classList or [])]
        return buttons, slots

    def click(self, button):
        button._event_handlers["click"]({"type": "click"})

    def test_the_members_are_collapsible_sections_and_nothing_is_built_up_front(self):
        index = self.engine.member_index({"m.eager": None, "m.lazy": None}, self.owner, "m")
        buttons, slots = self.parts(index)
        self.assertEqual(len(buttons), 2)
        self.assertEqual(len(slots), 2)
        self.assertEqual(self.built, [])
        self.assertEqual([s.elem.innerHTML for s in slots], ["", ""])

    def test_opening_a_section_fills_it_once(self):
        index = self.engine.member_index({"m.eager": None}, self.owner, "m")
        buttons, slots = self.parts(index)
        self.click(buttons[0])
        self.assertIn("page of m.eager", slots[0].elem.innerHTML)
        self.click(buttons[0])                                      # closing and reopening is free
        self.click(buttons[0])
        self.assertEqual(self.built, ["m.eager"])

    def test_a_member_without_a_prepared_page_is_documented_on_demand(self):
        index = self.engine.member_index({"m.lazy": None}, self.owner, "m")
        buttons, slots = self.parts(index)
        with mock.patch.object(sys.modules["McUtils.Docs.DocWalker"], "jdoc", return_value=self.JHTML.Div("documented lazily")) as jd:
            self.click(buttons[0])
            self.click(buttons[0])
        jd.assert_called_once()
        self.assertIs(jd.call_args.args[0], len)
        self.assertIn("documented lazily", slots[0].elem.innerHTML)


@unittest.skipUnless(have_widgets(), "ipywidgets/markdown not installed")
class HighlightedCodeTests(unittest.TestCase):
    def setUp(self):
        from McUtils.Jupyter.JHTML.CodeHighlighting import CodeHighlighter
        self.H = CodeHighlighter
        self.addCleanup(setattr, CodeHighlighter, "_shown", CodeHighlighter._shown)
        CodeHighlighter._shown = False

    def shown(self):
        from McUtils.Jupyter.JHTML.WidgetTools import JupyterAPIs
        shown = []
        fake = types.SimpleNamespace(display=lambda *a, **k: shown.extend(a), HTML=lambda text: text)
        patcher = mock.patch.object(JupyterAPIs, "get_display_api", classmethod(lambda cls: fake))
        patcher.start()
        self.addCleanup(patcher.stop)
        return shown

    def static(self, component):
        from McUtils.Jupyter.Apps.Themes import _mode
        token = _mode.set("static")
        try:
            return component.to_jhtml().tostring()
        finally:
            _mode.reset(token)

    def test_the_element_is_escaped_code_with_a_language_class(self):
        from McUtils.Jupyter import HighlightedCode
        html = self.static(HighlightedCode("x = [1 < 2]", language="python", load=False))
        self.assertIn('<code class="language-python">x = [1 &lt; 2]</code>', html)
        self.assertTrue(html.startswith("<pre"))
        self.assertNotIn("language-", self.static(HighlightedCode("plain", language=None, load=False)))

    def test_it_displays_as_a_widget(self):
        from McUtils.Jupyter import HighlightedCode
        self.assertTrue(hasattr(HighlightedCode("1", load=False).to_widget(), "children"))

    def test_the_loader_is_shown_once_and_names_the_cdn(self):
        from McUtils.Jupyter import HighlightedCode
        shown = self.shown()
        HighlightedCode("a")
        HighlightedCode("b")
        self.assertEqual(len(shown), 1)
        self.assertIn("<script>", shown[0])
        self.assertIn(self.H.script_url(), shown[0])
        self.assertIn(self.H.style_url(), shown[0])
        self.assertTrue(self.H.script_url().startswith("https://cdnjs.cloudflare.com/"))
        self.assertTrue(self.H.ensure_loaded(force=True))
        self.assertEqual(len(shown), 2)

    def test_the_loader_only_touches_unmarked_code_blocks(self):
        js = self.H.loader_js()
        self.assertIn("pre > code[class*=\"language-\"]:not([data-mcu-hl])", js)
        self.assertIn("children.length===0", js)            # code that is already marked up is left alone

    def test_static_pages_get_head_elements(self):
        from McUtils.Docs.HTMLDocs import static_doc
        text = "".join(e.tostring() for e in self.H.head_elements())
        self.assertIn(self.H.style_url(), text)
        self.assertIn(self.H.script_url(), text)

    def test_signatures_are_shown_as_highlighted_code(self):
        from McUtils.Docs.DocWalker import InteractiveTemplateEngine as E
        self.assertEqual(E.signature_source("f", "(x, y)"), "def f(x, y):")
        self.assertEqual(E.signature_source("f", "(cls)", "@classmethod\n"), "@classmethod\ndef f(cls):")


class VerbosityTests(unittest.TestCase):
    """`jdoc` is silent by default; `verbose` follows the `Devutils.LogLevel` scheme."""

    def run_doc(self, **kw):
        import contextlib, io
        from McUtils.Docs.DocWalker import DocWalker
        import McUtils.Combinatorics as mod
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            DocWalker(out=None, description="", **kw).write([mod], max_depth=1)
        return out.getvalue()

    def test_levels_resolve_like_the_logger(self):
        from McUtils.Docs.DocWalker import doc_logger
        from McUtils.Devutils.Loggers import LogLevel, Logger
        self.assertEqual(doc_logger(False).verbosity, LogLevel.Quiet)
        self.assertEqual(doc_logger(None).verbosity, LogLevel.Quiet)
        self.assertEqual(doc_logger(True).verbosity, LogLevel.Normal)
        self.assertEqual(doc_logger("Debug").verbosity, LogLevel.Debug)
        self.assertEqual(doc_logger("moredebug").verbosity, LogLevel.MoreDebug)
        self.assertEqual(doc_logger(LogLevel.All).verbosity, LogLevel.All)
        self.assertEqual(doc_logger(50).verbosity, 50)
        mine = Logger(log_level=LogLevel.Debug)
        self.assertIs(doc_logger(mine), mine)

    def test_each_level_prints_what_it_should(self):
        quiet = self.run_doc(verbose=False)
        normal = self.run_doc(verbose=True)
        debug = self.run_doc(verbose="Debug")
        self.assertEqual(quiet, "")
        self.assertIn("documenting module McUtils.Combinatorics", normal)
        self.assertNotIn("members:", normal)
        self.assertIn("members:", debug)
        self.assertIn("{", debug)                       # braces in a member table are written as they are

    @unittest.skipUnless(have_widgets(), "ipywidgets/markdown not installed")
    def test_jdoc_prints_nothing_by_default(self):
        import contextlib, io
        from McUtils.Docs import jdoc
        from McUtils.Docs.DocWalker import InteractiveTemplateEngine
        import McUtils.Combinatorics as mod
        for kw in ({}, {"verbose": False}):
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                jdoc(mod, engine=InteractiveTemplateEngine(), **kw)
            self.assertEqual(out.getvalue(), "", kw)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            jdoc(mod, engine=InteractiveTemplateEngine(), verbose=True)
        self.assertIn("documenting module", out.getvalue())


class ExtensionCheckTests(unittest.TestCase):
    def setUp(self):
        from McUtils.Jupyter.JHTML.HTMLWidgets import HTMLWidgets
        self.W = HTMLWidgets
        self.addCleanup(setattr, HTMLWidgets, "_extension_checked", HTMLWidgets._extension_checked)
        HTMLWidgets._extension_checked = False
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        patcher = mock.patch.object(
            self.W, "server_environment",
            classmethod(lambda cls, refresh=False: {"python": sys.executable, "how": "test", "prefix": None,
                                                    "labextension": None, "nbextension": None}))
        patcher.start()
        self.addCleanup(patcher.stop)
        patcher = mock.patch("jupyter_core.paths.jupyter_path", lambda *a: [])   # ignore what is installed on this machine
        try:
            patcher.start()
        except ImportError:
            pass
        else:
            self.addCleanup(patcher.stop)

    def shown(self):
        """Patches the display API and returns the list of things displayed."""
        from McUtils.Jupyter.JHTML.WidgetTools import JupyterAPIs
        shown = []
        fake = types.SimpleNamespace(display=lambda *a, **k: shown.extend(a))
        patcher = mock.patch.object(JupyterAPIs, "get_display_api", classmethod(lambda cls: fake))
        patcher.start()
        self.addCleanup(patcher.stop)
        return shown

    def install_at(self, kind):
        target = os.path.join(self._tmp.name, "share", "jupyter", kind + "s", self.W.extension_name)
        shutil.copytree(self.W.extension_source(kind), target)    # a current copy, as JHTML.load installs

    @unittest.skipUnless(have_widgets(), "ipywidgets/markdown not installed")
    def test_a_missing_extension_shows_the_install_notice_once(self):
        shown = self.shown()
        with mock.patch.object(sys, "exec_prefix", self._tmp.name):
            self.assertFalse(self.W.extension_installed())
            self.assertIs(self.W.check_extension(), False)
            self.assertIsNone(self.W.check_extension())      # only the first display is checked
        self.assertEqual(len(shown), 1)
        text = shown[0].tostring()
        self.assertIn("not installed", text)
        self.assertIn("JHTML.load()", text)
        self.assertIn("<pre><code>", text)                   # a code block to copy
        self.assertIn("Reload the page", text)
        self.assertIn(self._tmp.name, text)                  # says which environment it looked in

    @unittest.skipUnless(have_widgets(), "ipywidgets/markdown not installed")
    def test_an_installed_extension_shows_nothing(self):
        shown = self.shown()
        self.install_at("labextension")
        with mock.patch.object(sys, "exec_prefix", self._tmp.name):
            self.assertTrue(self.W.extension_installed())
            self.assertIs(self.W.check_extension(), True)
        self.assertEqual(shown, [])

    def test_either_kind_of_installation_counts(self):
        self.install_at("nbextension")
        with mock.patch.object(sys, "exec_prefix", self._tmp.name):
            found = self.W.extension_locations()
        self.assertEqual(found["labextension"], [])
        self.assertEqual(len(found["nbextension"]), 1)

    @unittest.skipUnless(have_widgets(), "ipywidgets/markdown not installed")
    def test_force_checks_again(self):
        shown = self.shown()
        with mock.patch.object(sys, "exec_prefix", self._tmp.name):
            self.W.check_extension()
            self.W.check_extension(force=True)
        self.assertEqual(len(shown), 2)

    @unittest.skipUnless(have_widgets(), "ipywidgets/markdown not installed")
    def test_displaying_a_widget_runs_the_check(self):
        from McUtils.Jupyter import JHTML
        self.shown()
        with mock.patch.object(sys, "exec_prefix", self._tmp.name), \
                mock.patch.object(self.W, "check_extension", wraps=self.W.check_extension) as check:
            JHTML.Div(JHTML.Button("x", event_handlers={"click": lambda *a: None})).display()
        check.assert_called()

    @unittest.skipUnless(have_widgets(), "ipywidgets/markdown not installed")
    def test_jhtml_exposes_the_check(self):
        from McUtils.Jupyter import JHTML
        self.assertEqual(JHTML.check_extension.__func__, self.W.check_extension.__func__)
        self.assertEqual(JHTML.extension_installed.__func__, self.W.extension_installed.__func__)


@unittest.skipUnless(have_widgets(), "ipywidgets/markdown not installed")
class StaticFrameTests(unittest.TestCase):
    def setUp(self):
        import McUtils.Docs.HTMLDocs as hd
        self.hd = hd
        for kind, names in (("css", hd._FINX_CSS_FILES), ("js", hd._FINX_JS_FILES)):
            for name in names:
                hd._FINX_ASSET_CACHE.setdefault((kind, name), "")
        self.mod = types.ModuleType("controls_static")
        exec('def shown(x):\n    """\n    Shows.\n\n    :param x: input\n    :type x: int\n    """\n    return x\n',
             self.mod.__dict__)
        self.mod.shown.__module__ = "controls_static"
        sys.modules["controls_static"] = self.mod
        self.addCleanup(sys.modules.pop, "controls_static", None)

    def test_the_page_is_a_jhtml_element(self):
        page = self.hd.static_doc(self.mod.shown)
        self.assertEqual(page.tag.lower(), "html")
        self.assertTrue(hasattr(page, "_ipython_display_"))

    def test_static_doc_passes_walker_arguments_like_jdoc(self):
        seen = {}
        real = self.hd.DocWalker
        class Spy(real):
            def __init__(self, *a, **kw):
                seen.update(kw)
                super().__init__(*a, **kw)
        with mock.patch.object(self.hd, "DocWalker", Spy):
            self.hd.static_doc(self.mod.shown, examples_directory=tempfile.gettempdir())
        self.assertEqual(seen.get("examples_directory"), tempfile.gettempdir())

    def test_frame_returns_a_self_displaying_iframe(self):
        frame = self.hd.static_doc(self.mod.shown, frame={"height": "300px"})
        self.assertEqual(frame.tag.lower(), "iframe")
        text = frame.tostring()
        self.assertIn("srcdoc=", text)
        self.assertIn("height:300px", text)
        import html
        value = re.search(r'srcdoc="(.*?)" style=', text, re.S).group(1)
        document = html.unescape(value)                       # what the browser makes of the attribute
        self.assertTrue(document.startswith("<!DOCTYPE html>"))
        self.assertIn('<html lang="en">', document)
        self.assertNotIn('"', value)                          # quotes can't end the attribute early
        self.assertTrue(hasattr(frame, "_ipython_display_"))


if __name__ == "__main__":
    unittest.main()

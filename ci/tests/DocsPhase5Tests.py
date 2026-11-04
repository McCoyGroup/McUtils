"""Phase 5: method examples on class pages, the layout fix, interactive (`jdoc`) examples, and `static_doc`."""

import contextlib
import importlib.util
import io
import os
import re
import sys
import tempfile
import textwrap
import types
import unittest

from McUtils.Docs import DocBuilder
from McUtils.Docs.Examples import ExampleParser, ExampleRunner, ReadoutStore
from McUtils.Docs.ExampleEmbed import ExampleEmbedder
from McUtils.Docs.ExampleLive import LiveExamplePage, split_examples

HERE = os.path.dirname(os.path.abspath(__file__))


def _load_sibling(name):
    spec = importlib.util.spec_from_file_location(name + "_for_phase5", os.path.join(HERE, name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_embed_tests = _load_sibling("DocsReadoutEmbedTests")
PipelineTestBase = _embed_tests.PipelineTestBase
load_build_readouts = _embed_tests.load_build_readouts


def block(id, code, **options):
    opts = ", ".join(["id={!r}".format(id)] + ["{}={!r}".format(k, v) for k, v in options.items()])
    return "<!-- readout({}) -->\n```python\n{}\n```\n\n".format(opts, textwrap.dedent(code).strip("\n"))


def have_widgets():
    try:
        import ipywidgets, markdown  # noqa: F401
    except ImportError:
        return False
    return True


class MethodExamplesTests(PipelineTestBase):
    def built(self):
        store_dir = os.path.join(self.new_dir(), "readouts")
        module = load_build_readouts()
        module.load_doc_config = lambda: self.config(self.new_dir())
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(module.main(["--store", store_dir, "--timeout", "30"]), 0)
        target = self.new_dir()
        self.build(self.config(target, readouts=store_dir))
        return target, store_dir

    def test_method_examples_appear_on_the_class_page(self):
        target, store_dir = self.built()
        box = self.page(target, "Box.md")
        self.assertIn('data-readout="box-volume"', box)
        self.assertIn("**Examples**", box)
        self.assertNotIn("readout(", box)
        key = ExampleParser.parse(
            '<!-- readout(id="box-volume", display="output") -->\n```python\nprint("volume is 8")\n```\n').blocks[0].key
        self.assertIn(key, box)

    def test_the_method_examples_follow_the_method_signature(self):
        target, _ = self.built()
        box = self.page(target, "Box.md")
        start = box.index("docs-object-method")
        self.assertLess(start, box.index('data-readout="box-volume"'))
        self.assertLess(box.index("volume(self)"), box.index('data-readout="box-volume"'))

    def test_only_methods_with_examples_get_the_heading(self):
        # every page's footer has an "Examples" column; the method heading is the one extra occurrence
        target, _ = self.built()
        self.assertEqual(self.page(target, "Box.md").count("**Examples**"), 2)
        self.assertEqual(self.page(target, "energy.md").count("**Examples**"), 1)

    def test_without_a_store_the_marker_text_is_left_as_written(self):
        target = self.new_dir()
        self.build(self.config(target))
        self.assertIn('readout(id="box-volume"', self.page(target, "Box.md"))


class ExampleWorkingDirectoryTests(PipelineTestBase):
    def run_main(self, *extra):
        module = load_build_readouts()
        module.load_doc_config = lambda: self.config(self.new_dir())
        seen = []
        import McUtils.Docs as docs
        original = docs.SubprocessExampleRunner

        class Spy(original):
            def __init__(self, *a, **kw):
                seen.append(kw.get("cwd"))
                super().__init__(*a, **kw)

        docs.SubprocessExampleRunner = Spy
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                module.main(["--store", os.path.join(self.new_dir(), "readouts"), "--timeout", "30", *extra])
        finally:
            docs.SubprocessExampleRunner = original
        return module, seen

    def test_examples_run_in_a_scratch_directory_by_default(self):
        module, seen = self.run_main()
        self.assertEqual(len(seen), 1)
        self.assertNotEqual(os.path.abspath(seen[0]), os.path.abspath(module.root))
        self.assertFalse(os.path.exists(seen[0]))   # and it is cleaned up afterwards

    def test_cwd_repo_and_cwd_path(self):
        module, seen = self.run_main("--cwd", "repo")
        self.assertEqual(seen, [module.root])
        here = self.new_dir()
        _, seen = self.run_main("--cwd", here)
        self.assertEqual(seen, [here])

    def test_a_relative_store_path_survives_the_changed_directory(self):
        module = load_build_readouts()
        module.load_doc_config = lambda: self.config(self.new_dir())
        base = self.new_dir()
        old = os.getcwd()
        os.chdir(base)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                module.main(["--store", "rel-readouts", "--timeout", "30"])
        finally:
            os.chdir(old)
        self.assertTrue(os.path.isfile(os.path.join(base, "rel-readouts", "manifest.json")))


class SplitExamplesTests(unittest.TestCase):
    def test_no_markers_means_none(self):
        self.assertIsNone(split_examples("Just **text**\n\n```python\nx = 1\n```\n"))
        self.assertIsNone(split_examples(None))

    def test_a_marker_inside_another_fence_is_not_a_marker(self):
        text = "```md\n<!-- readout(id='a') -->\n```python\n1\n```\n```\n"
        self.assertIsNone(split_examples(text))

    def test_malformed_markers_fall_back_to_plain_markdown(self):
        self.assertIsNone(split_examples("<!-- readout(nonsense=1) -->\n```python\n1\n```\n"))

    def test_pieces_alternate_text_and_blocks_and_rebuild_the_text(self):
        text = "Intro\n\n" + block("a", "1 + 1") + "Between\n\n" + block("b", "2 + 2")
        pieces = split_examples(text, owner="demo")
        self.assertEqual([k for k, _ in pieces], ["text", "code", "text", "code"])
        self.assertEqual([p.id for k, p in pieces if k == "code"], ["a", "b"])
        self.assertEqual(pieces[1][1].fence, "```python\n1 + 1\n```\n")
        self.assertNotIn("readout", pieces[1][1].fence)


class LiveExamplePageTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.store_dir = os.path.join(self._tmp.name, "readouts")

    def page(self, text, **kw):
        return LiveExamplePage(text, owner="demo", **kw)

    def test_blocks_share_a_namespace_in_order(self):
        page = self.page(block("a", "x = 21", display="none") + block("b", "x * 2"))
        result = page.try_run("b")
        self.assertEqual(result.status, "ok")
        self.assertEqual(result.view.value, 42)

    def test_running_a_later_block_first_runs_the_earlier_ones_once(self):
        text = (block("a", "log = []\nlog.append('a')", display="none")
                + block("b", "log.append('b')", display="none") + block("c", "log"))
        page = self.page(text)
        self.assertEqual(page.run("c").value, ["a", "b"])
        self.assertEqual(page.run("c").value, ["a", "b"])   # re-running c re-runs only c
        page.run("b")
        self.assertEqual(page.run("c").value, ["a", "b", "b"])

    def test_isolated_blocks_start_fresh(self):
        text = block("a", "x = 1", display="none") + block("b", "x = 2\nx", isolated=True) + block("c", "x", isolated=True)
        page = self.page(text)
        self.assertEqual(page.try_run("b").status, "ok")
        result = page.try_run("c")
        self.assertEqual(result.status, "error")
        self.assertIn("NameError", result.error)

    def test_errors_are_reported_not_raised_and_hide_our_frames(self):
        page = self.page(block("boom", "1/0"))
        result = page.try_run("boom")
        self.assertEqual(result.status, "error")
        self.assertIn("ZeroDivisionError", result.error)
        self.assertIn("1/0", result.error)
        self.assertNotIn("Examples.py", result.error)
        self.assertNotIn("ExampleLive.py", result.error)
        with self.assertRaises(ZeroDivisionError):
            page.run("boom")

    def test_a_failed_earlier_block_stops_the_later_one(self):
        page = self.page(block("a", "1/0", display="none") + block("b", "2"))
        self.assertEqual(page.try_run("b").status, "error")

    def test_display_none_and_missing_values(self):
        page = self.page(block("quiet", "y = 1", display="none") + block("noval", "z = 2"))
        self.assertEqual(page.try_run("quiet").status, "empty")
        result = page.try_run("noval")
        self.assertEqual(result.status, "error")
        self.assertIn("produced no value", result.error)

    def test_private_namespaces_leave_the_callers_alone_but_a_given_dict_is_used(self):
        mine = {"base": 10}
        page = self.page(block("a", "out = base + 1\nout"), namespace=mine)
        self.assertEqual(page.run("a").value, 11)
        self.assertEqual(mine["out"], 11)
        other = self.page(block("a", "'out' in globals()"))
        self.assertIs(other.run("a").value, False)

    def test_user_namespace_needs_ipython(self):
        page = self.page(block("a", "1"), namespace="user")
        try:
            import IPython  # noqa: F401
        except ImportError:
            self.skipTest("IPython not installed")
        if IPython.get_ipython() is not None:
            self.skipTest("running inside IPython")
        with self.assertRaises(RuntimeError):
            page.run("a")

    def test_reset_starts_the_page_again(self):
        page = self.page(block("a", "n = globals().get('n', 0) + 1", display="none") + block("b", "n"))
        self.assertEqual(page.run("b").value, 1)
        page.reset()
        self.assertEqual(page.run("b").value, 1)

    def test_block_lookup(self):
        page = self.page(block("a", "1") + block("b", "2"))
        self.assertEqual(page.block(1).id, "b")
        self.assertEqual(page.block("a").id, "a")
        with self.assertRaises(KeyError):
            page.block("nope")

    def test_a_seeded_example_matches_the_stored_output(self):
        text = block("r", "import random\nimport numpy as np\n{'r': random.random(), 'n': float(np.random.rand())}")
        store = ReadoutStore(self.store_dir)
        (stored,) = ExampleRunner(store, timeout=20).run_text(text, owner="demo")
        page = self.page(text, store=store)
        live = page.run("r").node().to_text()
        self.assertEqual(live, store.read_file(stored.block.key, "readout.txt"))

    def test_stored_fragment(self):
        store = ReadoutStore(self.store_dir)
        text = block("ok", "{'k': 1}") + block("bad", "1/0")
        ExampleRunner(store, timeout=20).run_text(text, owner="demo")
        page = self.page(text, store=self.store_dir)
        self.assertIn("mcr-root", page.stored_fragment("ok"))
        self.assertIsNone(page.stored_fragment("bad"))
        self.assertIsNone(self.page(text).stored_fragment("ok"))

    def test_show_result_gives_text_for_errors_and_a_fragment_for_output(self):
        page = self.page(block("a", "{'k': 1}") + block("b", "1/0", isolated=True))
        shown = []
        page.show_result(page.try_run("b"), lambda *d: shown.append(d))
        self.assertIn("failed", shown[-1][0])
        self.assertIn("ZeroDivisionError", shown[-1][0])
        if not have_widgets():
            self.skipTest("ipywidgets/markdown not installed")
        page.show_result(page.try_run("a"), lambda *d: shown.append(d))
        from McUtils.Readouts.Renderers.HTML import FragmentResult
        self.assertIsInstance(shown[-1][0], FragmentResult)


@unittest.skipUnless(have_widgets(), "ipywidgets/markdown not installed")
class JdocExamplesTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.mod = types.ModuleType("phase5_demo")
        exec(textwrap.dedent('''
            def shown(x):
                """
                Shows a thing.

                :param x: input
                :type x: int
                :examples:
                Some prose.

                <!-- readout(id="first") -->
                ```python
                {"x": 1}
                ```

                <!-- readout(id="second") -->
                ```python
                {"x": 2}
                ```
                """
                return x

            def plain(x):
                """
                Plain.

                :examples:
                ```python
                plain(1)
                ```
                """
                return x
            '''), self.mod.__dict__)
        self.mod.shown.__module__ = "phase5_demo"
        self.mod.plain.__module__ = "phase5_demo"
        sys.modules["phase5_demo"] = self.mod
        self.addCleanup(sys.modules.pop, "phase5_demo", None)

    def engine(self, **kw):
        from McUtils.Docs.DocWalker import InteractiveTemplateEngine
        return InteractiveTemplateEngine(**kw)

    def writer(self, obj, name):
        from McUtils.Docs.DocWalker import DocWalker, FunctionWriter
        return DocWalker(description="").get_handler(obj, cls=FunctionWriter, name=name)

    def test_marker_free_examples_are_still_a_markdown_view(self):
        from McUtils.Jupyter import JHTML
        text = "Prose\n\n```python\nplain(1)\n```\n"
        out = self.engine().format_examples(text)
        self.assertEqual(out.tostring(), JHTML.Markdown(text).tostring())
        self.assertEqual(self.engine().format_examples("raw", markdown=False), "raw")
        self.assertIsNone(self.engine().format_examples(None))

    def test_marked_examples_become_prose_code_and_controls(self):
        engine = self.engine()
        text = ExampleParser.parse(  # round trip through the parser to get the same text jdoc sees
            "Some prose.\n\n" + block("first", '{"x": 1}') + block("second", '{"x": 2}')).__str__()
        out = engine.format_examples(text, self.writer(self.mod.shown, "shown"))
        self.assertEqual(len(engine._example_pages), 1)
        (page,) = engine._example_pages.values()
        self.assertEqual([b.id for b in page.blocks], ["first", "second"])
        self.assertTrue(hasattr(out, "get_mime_bundle") or hasattr(out, "tostring"))

    def test_the_same_text_reuses_one_page_and_so_one_namespace(self):
        engine = self.engine()
        text = block("a", "x = 5", display="none") + block("b", "x")
        engine.format_examples(text)
        engine.format_examples(text)
        self.assertEqual(len(engine._example_pages), 1)
        (page,) = engine._example_pages.values()
        self.assertEqual(page.run("b").value, 5)

    def test_live_examples_can_be_turned_off(self):
        from McUtils.Jupyter import JHTML
        engine = self.engine(live_examples=False)
        text = block("a", "1")
        out = engine.format_examples(text)
        self.assertEqual(out.tostring(), JHTML.Markdown(text).tostring())
        self.assertEqual(engine._example_pages, {})

    def test_engine_settings_reach_the_pages(self):
        ns = {"seed": 3}
        engine = self.engine(readouts=self._tmp.name, example_namespace=ns)
        engine.format_examples(block("a", "seed"))
        (page,) = engine._example_pages.values()
        self.assertIs(page.namespace, ns)
        self.assertEqual(page.store.root, self._tmp.name)

    def test_jdoc_builds_the_view_and_registers_the_pages(self):
        from McUtils.Docs import jdoc
        from McUtils.Docs.DocWalker import InteractiveTemplateEngine
        engine = InteractiveTemplateEngine()
        view = jdoc(self.mod.shown, engine=engine)
        self.assertIsNotNone(view)
        self.assertEqual(len(engine._example_pages), 1)

    def test_jdoc_builds_an_engine_for_the_new_options(self):
        from McUtils.Docs import jdoc
        dw = importlib.import_module("McUtils.Docs.DocWalker")   # `McUtils.Docs.DocWalker` the attribute is the class
        seen = []
        original = dw.DocWalker.__init__

        def spy(self, *a, **kw):
            seen.append(kw.get("engine"))
            return original(self, *a, **kw)

        dw.DocWalker.__init__ = spy
        try:
            jdoc(self.mod.plain, readouts=self._tmp.name, example_namespace={})
            jdoc(self.mod.plain)
        finally:
            dw.DocWalker.__init__ = original
        self.assertIsInstance(seen[0], dw.InteractiveTemplateEngine)
        self.assertEqual(seen[0].readouts, self._tmp.name)
        self.assertIsNone(seen[1])


FINX_STUB_CSS = ".stub{}"


@unittest.skipUnless(have_widgets(), "ipywidgets/markdown not installed")
class StaticDocTests(unittest.TestCase):
    def setUp(self):
        import McUtils.Docs.HTMLDocs as hd
        self.hd = hd
        for kind, names in (("css", hd._FINX_CSS_FILES), ("js", hd._FINX_JS_FILES)):
            for name in names:
                hd._FINX_ASSET_CACHE.setdefault((kind, name), "")   # no network in tests
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.store = ReadoutStore(os.path.join(self._tmp.name, "readouts"))
        self.mod = types.ModuleType("phase5_static")
        exec(textwrap.dedent('''
            def shown(x):
                """
                Shows a thing.

                :param x: input
                :type x: int
                :examples:
                Prose before.

                <!-- readout(id="s1") -->
                ```python
                {"alpha": 1, "beta": [1, 2, 3]}
                ```

                Prose after.
                """
                return x
            '''), self.mod.__dict__)
        self.mod.shown.__module__ = "phase5_static"
        sys.modules["phase5_static"] = self.mod
        self.addCleanup(sys.modules.pop, "phase5_static", None)
        text = block("s1", '{"alpha": 1, "beta": [1, 2, 3]}')
        ExampleRunner(self.store, timeout=20).run_text(text, owner="phase5_static.shown")

    def doc(self, **kw):
        return self.hd.static_doc(self.mod.shown, return_string=True, **kw)

    def test_stored_output_is_written_into_the_page(self):
        out = self.doc(readouts=self.store)
        self.assertIn("mcr-inline", out)
        self.assertIn("mcr-root", out)
        self.assertIn("alpha", out)
        self.assertNotIn("readout(", out)
        self.assertNotIn("data-src", out)
        self.assertNotIn("IntersectionObserver", out)   # no loader: the page is self-contained
        self.assertIn("Prose before.", out)
        self.assertIn("Prose after.", out)

    def test_without_a_store_the_page_is_as_before(self):
        out = self.doc()
        self.assertNotIn("mcr-inline", out)
        self.assertNotIn("mcr-root", out)

    def test_a_missing_entry_leaves_a_note_and_strict_raises(self):
        empty = ReadoutStore(os.path.join(self._tmp.name, "empty"))
        self.assertIn("Readout not generated yet", self.doc(readouts=empty))
        from McUtils.Docs.ExampleEmbed import ExampleEmbedError
        with self.assertRaises(ExampleEmbedError):
            self.doc(readouts=empty, strict_readouts=True)


class InlineEmbedderTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.store = ReadoutStore(os.path.join(self._tmp.name, "readouts"))

    def test_inline_mode_inlines_the_fragment_and_emits_no_loader(self):
        text = block("a", "{'k': 1}")
        ExampleRunner(self.store, timeout=20).run_text(text, owner="demo")
        embedder = ExampleEmbedder(self.store, inline=True, warn=None)
        out = embedder(text, owner="demo")
        self.assertIn("mcr-inline", out)
        self.assertIn(self.store.read_file(ExampleParser.parse(text).blocks[0].key, "fragment.html"), out)
        self.assertNotIn("<script>", out)
        self.assertEqual(embedder.assets, {})
        self.assertEqual(len(embedder.embedded), 1)

    def test_stylesheet_entries_get_the_shared_css_inlined_once(self):
        text = block("a", "{'k': 1}") + block("b", "{'k': 2}")
        ExampleRunner(self.store, timeout=20, css="stylesheet").run_text(text, owner="demo")
        out = ExampleEmbedder(self.store, inline=True, warn=None)(text, owner="demo")
        self.assertEqual(out.count("<style>"), 1)
        self.assertEqual(out.count("mcr-inline"), 2)

    def test_scene_entries_record_the_x3dom_runtime(self):
        text = block("a", "{'k': 1}")
        ExampleRunner(self.store, timeout=20).run_text(text, owner="demo")
        key = ExampleParser.parse(text).blocks[0].key
        meta = self.store.read_meta(key)
        meta["fragment"] = dict(meta["fragment"], needs=["x3dom"],
                                runtime={"x3dom": {"script": "https://x/x3dom.js", "stylesheet": "https://x/x3dom.css"}})
        self.store.write(key, meta, {"fragment.html": self.store.read_file(key, "fragment.html")})
        embedder = ExampleEmbedder(self.store, inline=True, warn=None)
        embedder(text, owner="demo")
        self.assertEqual(embedder.assets["x3dom"], {"script": "https://x/x3dom.js", "stylesheet": "https://x/x3dom.css"})

    def test_block_fence_property(self):
        (b,) = ExampleParser.parse(block("a", "1 + 1")).blocks
        self.assertEqual(b.fence, "```python\n1 + 1\n```\n")


if __name__ == "__main__":
    unittest.main()

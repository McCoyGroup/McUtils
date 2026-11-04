"""Examples start with the public names of the module they document, so a page needn't import them."""

import contextlib
import importlib.util
import io
import os
import sys
import tempfile
import textwrap
import unittest

from McUtils.Docs.Examples import ExampleCache, ExampleParser, ExampleRunner, ReadoutStore, implicit_namespace
from McUtils.Docs.ExampleLive import LiveExamplePage
from McUtils.Docs.ExampleProcess import SubprocessExampleRunner

CI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def block(id, code, **options):
    opts = ", ".join(["id={!r}".format(id)] + ["{}={!r}".format(k, v) for k, v in options.items()])
    return "<!-- readout({}) -->\n```python\n{}\n```\n\n".format(opts, textwrap.dedent(code).strip("\n"))


class ImplicitBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        pkg = os.path.join(cls._tmp.name, "implpkg")
        os.makedirs(pkg)
        with open(os.path.join(pkg, "__init__.py"), "w") as f:
            f.write("TOP = 'top'\n")
        with open(os.path.join(pkg, "sub.py"), "w") as f:
            f.write(textwrap.dedent('''
                __all__ = ["Widget", "make"]
                _hidden = 1
                other = "not exported"
                class Widget:
                    size = 3
                def make(n):
                    return [Widget.size] * n
                '''))
        with open(os.path.join(pkg, "plain.py"), "w") as f:
            f.write("visible = 1\n_private = 2\n")
        sys.path.insert(0, cls._tmp.name)
        cls.addClassCleanup(cls._cleanup)

    @classmethod
    def _cleanup(cls):
        if cls._tmp.name in sys.path:
            sys.path.remove(cls._tmp.name)
        for name in [n for n in sys.modules if n == "implpkg" or n.startswith("implpkg.")]:
            sys.modules.pop(name)
        cls._tmp.cleanup()

    def setUp(self):
        self._store_tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._store_tmp.cleanup)
        self.store = ReadoutStore(os.path.join(self._store_tmp.name, "readouts"))


class ImplicitNamespaceTests(ImplicitBase):
    def test_all_is_honoured_and_the_top_level_package_comes_along(self):
        ns = implicit_namespace("implpkg.sub")
        self.assertEqual(sorted(k for k in ns if k != "implpkg"), ["Widget", "make"])
        self.assertEqual(ns["implpkg"].TOP, "top")

    def test_without_all_the_public_names_are_used(self):
        ns = implicit_namespace("implpkg.plain")
        self.assertIn("visible", ns)
        self.assertNotIn("_private", ns)

    def test_the_longest_importable_prefix_of_an_object_name_is_used(self):
        ns = implicit_namespace("implpkg.sub.Widget.size")
        self.assertIn("make", ns)
        self.assertIn("implpkg", ns)

    def test_nothing_importable_or_no_owner_gives_nothing(self):
        self.assertEqual(implicit_namespace(None), {})
        self.assertEqual(implicit_namespace(""), {})
        self.assertEqual(implicit_namespace("definitely_not_a_module.thing"), {})

    def test_the_result_is_a_copy(self):
        implicit_namespace("implpkg.sub")["Widget"] = None
        self.assertIsNotNone(implicit_namespace("implpkg.sub")["Widget"])


class RunnerImportsTests(ImplicitBase):
    def test_examples_can_use_the_modules_names_without_importing_them(self):
        (r,) = ExampleRunner(self.store, timeout=20).run_text(block("a", "make(2)"), owner="implpkg.sub")
        self.assertEqual(r.status, "ok")
        self.assertIn("shape (2,)", self.store.read_file(r.block.key, "readout.txt"))

    def test_without_the_option_they_cannot(self):
        (r,) = ExampleRunner(self.store, timeout=20, imports=False).run_text(block("a", "make(2)"), owner="implpkg.sub")
        self.assertEqual(r.status, "error")
        self.assertEqual(r.meta["error"]["type"], "NameError")

    def test_an_explicit_import_in_the_example_wins(self):
        text = block("a", "from implpkg.plain import visible as make\nmake", show_trivial=True)
        (r,) = ExampleRunner(self.store, timeout=20).run_text(text, owner="implpkg.sub")
        self.assertEqual(r.status, "ok")
        self.assertIn("1", self.store.read_file(r.block.key, "readout.txt"))

    def test_the_runners_own_namespace_wins_over_the_implicit_one(self):
        text = block("a", "Widget", show_trivial=True)
        (r,) = ExampleRunner(self.store, timeout=20, namespace={"Widget": "mine"}).run_text(text, owner="implpkg.sub")
        self.assertIn("mine", self.store.read_file(r.block.key, "readout.txt"))

    def test_every_chain_gets_the_names_again(self):
        text = block("a", "del make", display="none") + block("b", "make(1)", isolated=True)
        results = ExampleRunner(self.store, timeout=20).run_text(text, owner="implpkg.sub")
        self.assertEqual({r.block.id: r.status for r in results}, {"a": "ok", "b": "ok"})

    def test_a_page_without_an_owner_is_unchanged(self):
        (r,) = ExampleRunner(self.store, timeout=20).run_text(block("a", "make(1)"))
        self.assertEqual(r.status, "error")

    def test_the_worker_process_does_the_same(self):
        runner = SubprocessExampleRunner(self.store, timeout=30)
        (r,) = runner.run_text(block("a", "make(2)"), owner="implpkg.sub")
        self.assertEqual(r.status, "ok")
        other = ReadoutStore(os.path.join(self._store_tmp.name, "off"))
        (r,) = SubprocessExampleRunner(other, timeout=30, imports=False).run_text(block("a", "make(2)"), owner="implpkg.sub")
        self.assertEqual(r.status, "error")
        self.assertEqual(r.meta["error"]["type"], "NameError")

    def test_live_pages_get_them_too(self):
        page = LiveExamplePage(block("a", "make(2)"), owner="implpkg.sub")
        self.assertEqual(page.run("a").value, [3, 3])
        self.assertEqual(LiveExamplePage(block("a", "make(2)"), owner="implpkg.sub", imports=False).try_run("a").status, "error")


class RetryErrorsTests(ImplicitBase):
    def test_refresh_errors_retries_only_failed_blocks(self):
        text = block("bad", "make(1)", isolated=True) + block("good", "{'k': 1}", isolated=True)
        ExampleRunner(self.store, timeout=20, imports=False).run_text(text, owner="implpkg.sub")
        cache = ExampleCache(self.store)
        blocks = ExampleParser.parse(text, owner="implpkg.sub").blocks
        self.assertEqual([(b.id, why) for b, why in cache.plan(blocks, "errors")], [("bad", "retry")])
        self.assertEqual(cache.plan(blocks, False), [])
        results = ExampleRunner(self.store, timeout=20).run_text(text, owner="implpkg.sub", refresh="errors")
        self.assertEqual({r.block.id: r.status for r in results}, {"bad": "ok"})
        self.assertEqual(cache.plan(blocks, "errors"), [])

    def test_a_chain_behind_a_retried_failure_runs_again(self):
        text = block("a", "x = make(1)", display="none") + block("b", "x")
        ExampleRunner(self.store, timeout=20, imports=False).run_text(text, owner="implpkg.sub")
        results = ExampleRunner(self.store, timeout=20).run_text(text, owner="implpkg.sub", refresh="errors")
        self.assertEqual({r.block.id: r.status for r in results}, {"a": "ok", "b": "ok"})


def load_tool(name):
    spec = importlib.util.spec_from_file_location(name + "_imports_test", os.path.join(CI, name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ToolOptionTests(unittest.TestCase):
    def test_build_readouts_flags(self):
        module = load_tool("build_readouts")
        args = module.parse_args(["--refresh", "errors"], "x")
        self.assertEqual(args.refresh_plan, "errors")
        self.assertFalse(args.no_implicit_imports)
        self.assertTrue(module.parse_args(["--no-implicit-imports"], "x").no_implicit_imports)
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            module.parse_args(["--refresh", "errors", "--refresh", "stale"], "x")
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            module.parse_args(["--refresh", "errors", "--refresh", "water-*"], "x")

    def test_mark_examples_names_the_owner_like_the_docs_walk(self):
        module = load_tool("mark_examples")
        self.assertEqual(module.page_owner(os.path.join("McUtils", "Zachary.md")), "McUtils.Zachary")
        self.assertEqual(module.page_owner("McUtils.md"), "McUtils")


if __name__ == "__main__":
    unittest.main()

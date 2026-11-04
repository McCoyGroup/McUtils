"""Embedding stored example output into documentation pages, the `DocWalker` hook, and `ci/build_readouts.py`."""

import contextlib
import importlib.util
import io
import json
import os
import re
import sys
import tempfile
import textwrap
import unittest

from McUtils.Docs import DocBuilder, ExamplesParser
from McUtils.Docs.Examples import ExampleParser, ExampleRunner, ReadoutStore
from McUtils.Docs.ExampleEmbed import (
    ExampleCollector, ExampleEmbedder, ExampleEmbedError, EXAMPLE_LOADER_JS, EXAMPLE_DEBUG_JS, publish_readouts
)

CI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def block(id, code, **options):
    opts = ", ".join(["id={!r}".format(id)] + ["{}={!r}".format(k, v) for k, v in options.items()])
    return "<!-- readout({}) -->\n```python\n{}\n```\n\n".format(opts, textwrap.dedent(code).strip("\n"))


class EmbedderTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.store = ReadoutStore(os.path.join(self._tmp.name, "readouts"))
        self.warnings = []

    def embedder(self, **kw):
        kw.setdefault("warn", self.warnings.append)
        return ExampleEmbedder(self.store, **kw)

    def generate(self, text, owner="demo.fn"):
        ExampleRunner(self.store, timeout=20).run_text(text, owner=owner)

    def test_text_without_markers_is_returned_untouched(self):
        text = "Some **markdown**\n\n```python\nx = 1\n```\n\nand a <!-- plain comment -->\n"
        self.assertEqual(self.embedder()(text, owner="demo.fn"), text)
        self.assertEqual(self.warnings, [])

    def test_marker_removed_fence_kept_placeholder_added(self):
        text = "Before\n\n" + block("water", "{'e': -76.0}") + "After\n"
        self.generate(text)
        out = self.embedder()(text, owner="demo.fn")
        self.assertNotIn("readout(", out)
        self.assertNotIn("<!--", out)
        self.assertIn("```python\n{'e': -76.0}\n```", out)
        self.assertTrue(out.startswith("Before\n\n```python"))
        self.assertTrue(out.rstrip().endswith("After"))
        key = ExampleParser.parse(text, owner="demo.fn").blocks[0].key
        self.assertIn('class="mcr-example"', out)
        self.assertIn('data-readout="water"', out)
        self.assertIn('data-key="{}"'.format(key), out)
        self.assertIn("{{ '/readouts/%s/%s/fragment.html' | relative_url }}" % (key[:2], key), out)
        self.assertIn(">Open readout</a>", out)   # the no-JS fallback
        self.assertEqual(self.warnings, [])

    def test_the_loader_is_added_once_per_page_and_is_liquid_safe(self):
        text = block("a", "{'k': 1}") + block("b", "{'k': 2}")
        self.generate(text)
        out = self.embedder()(text, owner="demo.fn")
        self.assertEqual(out.count("<script>"), 1)
        self.assertEqual(out.count("data-src="), 2)
        for token in ("{{", "{%"):   # Liquid's openers; a stray closing brace pair is plain text to it
            self.assertNotIn(token, EXAMPLE_LOADER_JS)
        self.assertTrue(out.index("<script>") > out.index('data-readout="a"'))
        self.assertNotIn("\n\n", EXAMPLE_LOADER_JS)   # blank lines would end a raw HTML block in Markdown
        self.assertEqual(self.embedder(loader=False)(text, owner="demo.fn").count("<script>"), 0)

    def test_the_debug_badge_script_is_opt_in(self):
        text = block("a", "{'k': 1}") + block("b", "{'k': 2}")
        self.generate(text)
        self.assertNotIn("mcrDebug", self.embedder()(text, owner="demo.fn"))
        out = self.embedder(debug=True)(text, owner="demo.fn")
        self.assertEqual(out.count("<script>"), 2)           # the loader and, once per page, the badge
        self.assertEqual(out.count("window.mcrDebug=true"), 1)
        for token in ("{{", "{%"):
            self.assertNotIn(token, EXAMPLE_DEBUG_JS)
        self.assertNotIn("\n\n", EXAMPLE_DEBUG_JS)

    def test_url_template_and_eager_loading(self):
        text = block("a", "{'k': 1}")
        self.generate(text)
        out = self.embedder(url_template="/site/readouts/{key2}/{key}/fragment.html", lazy=False)(text, owner="demo.fn")
        self.assertIn('data-src="/site/readouts/', out)
        self.assertIn('data-lazy="false"', out)
        self.assertNotIn("{{", out.split("<script>")[0])

    def test_missing_failed_and_silent_blocks(self):
        generated = block("ok", "{'k': 1}") + block("bad", "1/0") + block("quiet", "x = 1", display="none")
        text = generated + block("never_run", "{'k': 3}", isolated=True)
        ExampleRunner(self.store, timeout=20).run_text(generated, owner="demo.fn")
        emb = self.embedder()
        out = emb(text, owner="demo.fn")
        self.assertIn("mcr-error", out)
        self.assertIn("ZeroDivisionError", out)
        self.assertIn("mcr-missing", out)
        self.assertEqual(out.count('class="mcr-example'), 3)   # ok, bad, never_run; not the silent one
        self.assertNotIn('data-readout="quiet"', out)          # display="none": code shown, nothing embedded
        self.assertIn("x = 1", out)
        kinds = sorted(k for _, _, k, _ in emb.problems)
        self.assertEqual(kinds, ["failed", "missing"])
        self.assertEqual(len(self.warnings), 2)

    def test_strict_collects_every_problem_then_raises_in_finish(self):
        text = block("a", "{'k': 1}") + block("b", "{'k': 2}")
        emb = self.embedder(strict=True)
        emb(text, owner="demo.fn")             # does not raise while embedding
        with self.assertRaises(ExampleEmbedError) as cm:
            emb.finish()
        self.assertIn("a", str(cm.exception))
        self.assertIn("b", str(cm.exception))
        self.assertEqual(len(self.embedder().finish()), 0)

    def test_scene_requirements_become_data_attributes(self):
        text = block("a", "{'k': 1}")
        self.generate(text)
        key = ExampleParser.parse(text, owner="demo.fn").blocks[0].key
        meta = self.store.read_meta(key)
        meta["fragment"] = dict(meta["fragment"], needs=["x3dom"],
                                runtime={"x3dom": {"script": "https://x/x3dom.js", "stylesheet": "https://x/x3dom.css"}})
        self.store.write(key, meta, {"fragment.html": self.store.read_file(key, "fragment.html")})
        out = self.embedder()(text, owner="demo.fn")
        self.assertIn('data-needs="x3dom"', out)
        self.assertIn('data-x3dom-script="https://x/x3dom.js"', out)
        self.assertIn('data-x3dom-css="https://x/x3dom.css"', out)

    def test_stylesheet_entries_ask_for_the_shared_css(self):
        text = block("a", "{'k': 1}", css="stylesheet")
        self.generate(text)
        out = self.embedder()(text, owner="demo.fn")
        self.assertIn('data-css-href="{{ \'/readouts/mcr.css\' | relative_url }}"', out)

    def test_markers_inside_other_fences_stay_as_they_are(self):
        text = "````markdown\n" + block("shown", "1") + "````\n"
        self.assertEqual(self.embedder()(text, owner="demo.fn"), text)

    def test_malformed_markers_fail_loudly_with_the_owner(self):
        with self.assertRaises(ValueError) as cm:
            self.embedder()("<!-- readout(id=1+1) -->\n```python\nx\n```\n", owner="demo.fn")
        self.assertIn("demo.fn", str(cm.exception))

    def test_publish_copies_the_store_next_to_the_pages(self):
        text = block("a", "{'k': 1}", css="stylesheet")
        self.generate(text)
        site = os.path.join(self._tmp.name, "site")
        dest = publish_readouts(self.store, site)
        key = ExampleParser.parse(text, owner="demo.fn").blocks[0].key
        self.assertTrue(os.path.isfile(os.path.join(dest, key[:2], key, "fragment.html")))
        self.assertTrue(os.path.isfile(os.path.join(dest, "mcr.css")))
        self.assertEqual(publish_readouts(ReadoutStore(dest), site), dest)   # already in place: nothing to do


class CollectorTests(unittest.TestCase):
    def test_collects_pages_with_markers_only_and_leaves_text_alone(self):
        col = ExampleCollector()
        a = block("a", "1") + "tail\n"
        self.assertEqual(col(a, owner="m.a"), a)
        self.assertEqual(col("no examples here\n", owner="m.b"), "no examples here\n")
        self.assertEqual(list(col.pages), ["m.a"])
        (owner, parsed), = col.parsed_pages()
        self.assertEqual((owner, [b.id for b in parsed.blocks]), ("m.a", ["a"]))

    def test_ids_must_be_unique_across_pages(self):
        col = ExampleCollector()
        col(block("same", "1"), owner="m.a")
        with self.assertRaises(ValueError) as cm:
            col(block("same", "2"), owner="m.b")
        self.assertIn("same", str(cm.exception))
        col(block("same", "1"), owner="m.a")   # the same page seen twice is fine


# --------------------------------------------------------------------------------------------- #
# the DocWalker hook and the whole pipeline, on a small throwaway package
# --------------------------------------------------------------------------------------------- #

DEMO_PACKAGE = '''
"""Demo package."""
__all__ = ["energy", "Box"]
__examples__ = """
Inline examples for the module.

<!-- readout(id="mod-inline") -->
```python
{"module": "demopkg", "n": 3}
```
"""

def energy(x):
    """
    Computes a thing.

    :param x: a number
    :type x: float
    :return: the thing
    :rtype: float
    :examples:
    Plain prose first.

    <!-- readout(id="energy-1") -->
    ```python
    import numpy as np
    x = np.linspace(0, 1, 4)
    {"x": x, "total": float(x.sum())}
    ```

    <!-- readout(id="energy-2") -->
    ```python
    {"again": float(x.mean())}
    ```
    """
    return x

class Box:
    """A box."""
    def volume(self):
        """
        Volume.

        :examples:
        <!-- readout(id="box-volume", display="output") -->
        ```python
        print("volume is 8")
        ```
        """
        return 8
'''

FILE_EXAMPLES = block("from-file", "{'never': 'shown'}")


def load_build_readouts():
    spec = importlib.util.spec_from_file_location("build_readouts_under_test", os.path.join(CI, "build_readouts.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PipelineTestBase(unittest.TestCase):
    package_name = "demopkg"

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.tmp = cls._tmp.name
        pkg = os.path.join(cls.tmp, cls.package_name)
        os.makedirs(pkg)
        with open(os.path.join(pkg, "__init__.py"), "w") as f:
            f.write(DEMO_PACKAGE)
        os.makedirs(os.path.join(cls.tmp, "examples", cls.package_name))
        with open(os.path.join(cls.tmp, "examples", cls.package_name, "energy.md"), "w") as f:
            f.write(FILE_EXAMPLES)   # shadowed by the docstring's :examples: field
        sys.path.insert(0, cls.tmp)
        sys.path.insert(0, CI)
        cls.addClassCleanup(cls._cleanup)
        import build_docs
        cls.base_config = dict(build_docs.doc_config)

    @classmethod
    def _cleanup(cls):
        for p in (cls.tmp, CI):
            if p in sys.path:
                sys.path.remove(p)
        sys.modules.pop(cls.package_name, None)
        sys.modules.pop("build_docs", None)
        cls._tmp.cleanup()

    def config(self, target, **kw):
        cfg = dict(self.base_config)
        cfg.update(
            packages=[{"id": self.package_name, "tests_root": os.path.join(self.tmp, "tests")}],
            root=self.tmp, target=target, readme="demo", examples_directory=os.path.join(self.tmp, "examples"),
            config=dict(self.base_config["config"], path=self.package_name)
        )
        cfg.update(kw)
        return cfg

    def build(self, cfg, builder=DocBuilder):
        ExamplesParser.IGNORE_UNHANDLED_STATEMENTS = True
        with contextlib.redirect_stdout(io.StringIO()):
            return builder(**cfg).build()

    def page(self, target, name):
        for dirpath, _, files in os.walk(target):
            if name in files:
                with open(os.path.join(dirpath, name)) as f:
                    return f.read()
        raise AssertionError("no page " + name)

    def new_dir(self):
        d = tempfile.TemporaryDirectory(dir=self.tmp)
        self.addCleanup(d.cleanup)
        return d.name


class DocWalkerHookTests(PipelineTestBase):
    def collect(self):
        col = ExampleCollector()

        class Collecting(DocBuilder):
            def load_embedder(self):
                self.embedder = None
                return col

        self.build(self.config(self.new_dir()), Collecting)
        return col

    def test_the_hook_sees_docstring_inline_and_method_examples(self):
        col = self.collect()
        self.assertEqual(sorted(col.pages), ["demopkg", "demopkg.Box.volume", "demopkg.energy"])
        self.assertEqual(sorted(col.ids), ["box-volume", "energy-1", "energy-2", "mod-inline"])

    def test_a_docstring_examples_field_wins_over_an_examples_file(self):
        col = self.collect()
        self.assertNotIn("from-file", col.ids)
        self.assertIn("energy-1", col.pages["demopkg.energy"])
        self.assertNotIn("from-file", col.pages["demopkg.energy"])

    def test_indentation_of_docstring_examples_survives_to_the_hook(self):
        text = self.collect().pages["demopkg.energy"]
        self.assertIn("```python\nimport numpy as np\nx = np.linspace(0, 1, 4)", text)

    def test_without_a_processor_pages_are_unchanged(self):
        target = self.new_dir()
        self.build(self.config(target))
        self.assertIn("readout(id=\"energy-1\")", self.page(target, "energy.md"))


class PipelineTests(PipelineTestBase):
    def generate(self, store_dir):
        module = load_build_readouts()
        module.load_doc_config = lambda: self.config(self.new_dir())
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = module.main(["--store", store_dir, "--timeout", "30"])
        return code, out.getvalue(), module

    def test_generate_then_embed_end_to_end(self):
        store_dir = os.path.join(self.new_dir(), "readouts")
        code, output, _ = self.generate(store_dir)
        self.assertEqual(code, 0, output)
        self.assertIn("4 marked example(s) on 3 page(s)", output)
        store = ReadoutStore(store_dir)
        manifest = store.load_manifest()["entries"]
        self.assertEqual(sorted(manifest), ["box-volume", "energy-1", "energy-2", "mod-inline"])
        self.assertTrue(all(e["status"] == "ok" for e in manifest.values()))

        target = self.new_dir()
        self.build(self.config(target, readouts=store_dir))
        energy = self.page(target, "energy.md")
        self.assertNotIn("readout(", energy)
        self.assertIn("```python\nimport numpy as np\nx = np.linspace(0, 1, 4)", energy)   # fence kept, indentation intact
        self.assertEqual(energy.count('class="mcr-example"'), 2)
        self.assertEqual(energy.count("<script>"), 1)
        self.assertNotIn("from-file", energy)
        # method examples are generated and embedded like any other, but the stock `method.md` template has no
        # `{examples}` slot, so they don't appear on the class page (see DESIGN.md, open issues)
        self.assertNotIn("readout(", self.page(target, "Box.md"))
        self.assertIn('data-readout="mod-inline"', self.page(target, "demopkg.md"))
        # the store is published next to the pages, ready for the loader to fetch
        key = manifest["energy-1"]["key"]
        self.assertTrue(os.path.isfile(os.path.join(target, "readouts", key[:2], key, "fragment.html")))

    def test_second_run_runs_nothing_and_refresh_reruns_only_what_matches(self):
        store_dir = os.path.join(self.new_dir(), "readouts")
        self.generate(store_dir)
        code, output, module = self.generate(store_dir)
        self.assertNotIn("running", output)
        module.load_doc_config = lambda: self.config(self.new_dir())
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            module.main(["--store", store_dir, "--refresh", "energy-*", "--timeout", "30"])
        text = out.getvalue()
        self.assertIn("energy-1 (refresh)", text)
        self.assertIn("energy-2 (refresh)", text)
        self.assertNotIn("mod-inline", text)
        self.assertNotIn("box-volume", text)

    def test_status_and_strict(self):
        store_dir = os.path.join(self.new_dir(), "readouts")
        module = load_build_readouts()
        module.load_doc_config = lambda: self.config(self.new_dir())
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = module.main(["--store", store_dir, "--status", "--strict"])
        self.assertEqual(code, 1)
        self.assertIn("4 missing", out.getvalue())
        self.assertFalse(os.path.exists(store_dir))   # --status runs and writes nothing
        self.generate(store_dir)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = module.main(["--store", store_dir, "--status", "--strict"])
        self.assertEqual(code, 0)
        self.assertIn("4 ok", out.getvalue())

    def test_prune_removes_entries_nothing_refers_to(self):
        store_dir = os.path.join(self.new_dir(), "readouts")
        self.generate(store_dir)
        store = ReadoutStore(store_dir)
        orphan = ExampleRunner(store, timeout=20).run_text(block("gone", "{'x': 1}"), owner="old.page")[0].block.key
        module = load_build_readouts()
        module.load_doc_config = lambda: self.config(self.new_dir())
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            module.main(["--store", store_dir, "--status", "--prune", "--dry-run"])
        self.assertIn("would remove 1 stored entry", out.getvalue())
        self.assertTrue(store.has(orphan))
        with contextlib.redirect_stdout(io.StringIO()):
            module.main(["--store", store_dir, "--status", "--prune"])
        self.assertFalse(store.has(orphan))
        self.assertNotIn("gone", store.load_manifest()["entries"])
        self.assertEqual(len(store.keys()), 4)

    def test_prune_cannot_be_combined_with_only(self):
        module = load_build_readouts()
        module.load_doc_config = lambda: self.config(self.new_dir())
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            module.main(["--prune", "--only", "demopkg.*"])

    def test_build_docs_script_has_the_readout_options(self):
        import subprocess
        out = subprocess.run([sys.executable, os.path.join(CI, "build_docs.py"), "--help"], capture_output=True,
                             text=True, cwd=CI, timeout=120)
        self.assertEqual(out.returncode, 0, out.stderr)
        for flag in ("--target", "--readouts", "--no-readouts", "--strict-readouts", "--readout-debug"):
            self.assertIn(flag, out.stdout)

    def test_build_docs_can_write_somewhere_other_than_the_repo(self):
        import subprocess
        target = self.new_dir()
        docs = os.path.join(CI, "docs")
        before = os.path.getmtime(docs) if os.path.isdir(docs) else None
        out = subprocess.run([sys.executable, os.path.join(CI, "build_docs.py"), "--target", target, "--no-readouts"],
                             capture_output=True, text=True, cwd=CI, timeout=600)
        self.assertEqual(out.returncode, 0, out.stderr[-2000:])
        self.assertTrue(os.path.isfile(os.path.join(target, "_config.yml")))
        self.assertTrue(os.path.isfile(os.path.join(target, "McUtils.md")))
        if before is not None:
            self.assertEqual(os.path.getmtime(docs), before)   # nothing was added to ci/docs

    def test_debug_option_reaches_the_pages(self):
        store_dir = os.path.join(self.new_dir(), "readouts")
        self.generate(store_dir)
        target = self.new_dir()
        self.build(self.config(target, readouts={"store": store_dir, "debug": True}))
        self.assertEqual(self.page(target, "energy.md").count("window.mcrDebug=true"), 1)

    def test_strict_docs_build_fails_when_outputs_are_missing(self):
        store_dir = os.path.join(self.new_dir(), "readouts")
        with self.assertRaises(ExampleEmbedError):
            self.build(self.config(self.new_dir(), readouts={"store": store_dir, "strict": True, "warn": None}))

    def test_a_failing_example_is_reported_and_still_published(self):
        store_dir = os.path.join(self.new_dir(), "readouts")
        self.generate(store_dir)
        store = ReadoutStore(store_dir)
        key = store.load_manifest()["entries"]["energy-2"]["key"]
        meta = store.read_meta(key)
        meta.update(status="error", error={"type": "ValueError", "message": "nope", "traceback": "..."})
        store.write(key, meta)
        target = self.new_dir()
        self.build(self.config(target, readouts={"store": store_dir, "warn": None}))
        self.assertIn("mcr-error", self.page(target, "energy.md"))


if __name__ == "__main__":
    unittest.main()

"""Running documentation examples: execution, value -> readout, store entries, caching and failures."""

import os
import tempfile
import unittest

import numpy as np

from McUtils.Docs.Examples import (
    ExampleParser, ExampleRunner, ExampleView, ReadoutStore, ExampleError, value_to_readout
)
from McUtils.Readouts import Readout, ReadoutText


def doc(*blocks):
    out = "Intro\n\n"
    for marker, src in blocks:
        out += "<!-- readout{} -->\n```python\n{}\n```\n\n".format(marker, src)
    return out


class RunnerCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.store = ReadoutStore(os.path.join(self._tmp.name, "readouts"))
        self.calls = []

    def runner(self, **kw):
        kw.setdefault("namespace", {"calls": self.calls})
        return ExampleRunner(self.store, revisions={"McUtils": "test"}, **kw)

    def meta(self, text, i=0, owner="o"):
        return self.store.read_meta(ExampleParser.parse(text, owner=owner).blocks[i].key)


class RunnerBasicsTests(RunnerCase):
    def test_runs_a_block_and_writes_the_entry(self):
        text = doc(('(id="a")', 'data = {"energy": -76.02, "freqs": [1.0, 2.0]}\nprint("hello")\ndata'))
        (r,) = self.runner().run_text(text, owner="o")
        self.assertTrue(r.ok)
        self.assertEqual(r.reason, "missing")
        key = r.block.key
        self.assertEqual(sorted(os.listdir(self.store.entry_path(key))),
                         ["fragment.html", "meta.json", "readout.json", "readout.txt"])
        meta = self.store.read_meta(key)
        self.assertEqual(meta["status"], "ok")
        self.assertEqual(meta["id"], "a")
        self.assertEqual(meta["revisions"], {"McUtils": "test"})
        self.assertEqual(meta["stdout"], "hello\n")
        self.assertEqual(meta["display"], "readout")
        self.assertEqual(meta["fragment"]["needs"], [])
        self.assertIn("energy", self.store.read_file(key, "fragment.html"))
        self.assertIn("-76.02", self.store.read_file(key, "readout.txt"))
        self.assertEqual(self.store.load_manifest()["entries"]["a"]["status"], "ok")

    def test_second_run_does_nothing(self):
        text = doc(('(id="a")', "calls.append('a')\n{'x': 1}"))
        runner = self.runner()
        self.assertEqual(len(runner.run_text(text, owner="o")), 1)
        self.assertEqual(runner.run_text(text, owner="o"), [])
        self.assertEqual(self.calls, ["a"])

    def test_refresh_modes(self):
        text = doc(('(id="a")', "calls.append('a')\n{'x': 1}"), ('(id="b")', "calls.append('b')\n{'y': 1}"))
        runner = self.runner()
        runner.run_text(text, owner="o")
        self.calls.clear()
        self.assertEqual([r.block.id for r in runner.run_text(text, owner="o", refresh="b")], ["b"])
        # b is reproduced, so its chain (a, then b) is replayed
        self.assertEqual(self.calls, ["a", "b"])
        self.calls.clear()
        self.assertEqual([r.block.id for r in runner.run_text(text, owner="o", refresh=True)], ["a", "b"])
        self.assertEqual(self.calls, ["a", "b"])

    def test_replaying_a_chain_does_not_rewrite_cached_predecessors(self):
        text = doc(('(id="a")', "calls.append('a')\nx = 1\n{'x': x}"), ('(id="b")', "calls.append('b')\n{'y': x + 1}"))
        runner = self.runner()
        runner.run_text(text, owner="o")
        blocks = ExampleParser.parse(text, owner="o").blocks
        path_a = self.store.entry_path(blocks[0].key, "meta.json")
        before = os.stat(path_a).st_mtime_ns
        import shutil
        shutil.rmtree(self.store.entry_path(blocks[1].key))
        self.calls.clear()
        results = runner.run_text(text, owner="o")
        self.assertEqual([r.block.id for r in results], ["b"])
        self.assertEqual(self.calls, ["a", "b"])  # a replayed to rebuild the namespace...
        self.assertEqual(os.stat(path_a).st_mtime_ns, before)  # ...but its entry is untouched

    def test_editing_an_early_block_regenerates_later_ones(self):
        v1 = doc(('(id="a")', "x = 1\n{'x': x}"), ('(id="b")', "{'y': x + 1}"))
        v2 = doc(('(id="a")', "x = 2\n{'x': x}"), ('(id="b")', "{'y': x + 1}"))
        runner = self.runner()
        runner.run_text(v1, owner="o")
        self.assertEqual([r.block.id for r in runner.run_text(v2, owner="o")], ["a", "b"])
        self.assertIn("3", self.store.read_file(ExampleParser.parse(v2, owner="o").blocks[1].key, "readout.txt"))


class NamespaceTests(RunnerCase):
    def test_blocks_share_a_namespace_until_an_isolated_block(self):
        text = doc(
            ('(id="a")', "x = 41\n{'x': x}"),
            ('(id="b")', "{'x': x + 1}"),
            ('(id="c", isolated=True)', "{'seen': 'x' in globals()}"),
        )
        results = self.runner().run_text(text, owner="o")
        self.assertEqual([r.status for r in results], ["ok", "ok", "ok"])
        self.assertIn("42", self.store.read_file(results[1].block.key, "readout.txt"))
        self.assertIn("False", self.store.read_file(results[2].block.key, "readout.txt"))

    def test_isolated_block_cannot_see_earlier_names(self):
        text = doc(('(id="a")', "x = 1\n{'x': x}"), ('(id="b", isolated=True)', "{'x': x}"))
        results = self.runner().run_text(text, owner="o")
        self.assertEqual([r.status for r in results], ["ok", "error"])
        self.assertEqual(results[1].meta["error"]["type"], "NameError")

    def test_seeding_is_reproducible_per_key(self):
        text = doc(('(id="a", display="output")', "import numpy as np, random\nprint(np.random.rand(), random.random())"))
        outputs = []
        for name in ("one", "two"):
            store = ReadoutStore(os.path.join(self._tmp.name, name))
            (r,) = ExampleRunner(store).run_text(text, owner="o")
            outputs.append(r.meta["stdout"])
        self.assertEqual(outputs[0], outputs[1])
        other = doc(('(id="a", display="output")', "import numpy as np, random\nprint(np.random.rand(), random.random())  # edited"))
        (r,) = ExampleRunner(ReadoutStore(os.path.join(self._tmp.name, "three"))).run_text(other, owner="o")
        self.assertNotEqual(outputs[0], r.meta["stdout"])


class ValueToReadoutTests(RunnerCase):
    def test_value_kinds(self):
        class WithReadout:
            def to_readout(self, **kw):
                return Readout(ReadoutText("custom"), title="Custom")

        class WithHTML:
            def _repr_html_(self):
                return "<b>bold</b>"

        ro = Readout(ReadoutText("mine"), title="Mine")
        self.assertIs(value_to_readout(ro), ro)
        self.assertEqual(value_to_readout(WithReadout()).title, "Custom")
        html = value_to_readout(WithHTML()).to_html_fragment().html
        self.assertIn("<b>bold</b>", html)
        record = value_to_readout({"a": 1, "arr": np.arange(3.)})
        self.assertIn("arr", record.to_text())

    def test_marker_options_reach_to_readout(self):
        seen = {}

        class Capture:
            def to_readout(self, **kw):
                seen.update(kw)
                return Readout(ReadoutText("x"))

        value_to_readout(Capture(), {"include": ["overview"], "exclude": ["a"], "units": "default", "style": "talk"})
        self.assertEqual(seen, {"include": ["overview"], "exclude": ["a"], "units": "default"})  # style is a render option


class DisplayModeTests(RunnerCase):
    def run_one(self, marker, src):
        (r,) = self.runner().run_text(doc((marker, src)), owner="o")
        return r

    def test_output(self):
        r = self.run_one('(id="a", display="output")', "print('line one')\nprint('line two')")
        self.assertTrue(r.ok)
        self.assertIn("line two", self.store.read_file(r.block.key, "fragment.html"))

    def test_output_with_nothing_printed_is_a_note(self):
        r = self.run_one('(id="a", display="output")', "x = 1")
        self.assertTrue(r.ok)
        self.assertIn("printed nothing", self.store.read_file(r.block.key, "fragment.html"))

    def test_both_shows_the_readout_and_the_output(self):
        r = self.run_one('(id="a", display="both")', "print('side effect')\n{'energy': 1.5}")
        html = self.store.read_file(r.block.key, "fragment.html")
        self.assertIn("energy", html)
        self.assertIn("side effect", html)
        self.assertIn("Output", html)

    def test_none_runs_but_stores_no_display_files(self):
        r = self.run_one('(id="a", display="none")', "calls.append('ran')")
        self.assertTrue(r.ok)
        self.assertEqual(self.calls, ["ran"])
        self.assertEqual(os.listdir(self.store.entry_path(r.block.key)), ["meta.json"])

    def test_readout_without_a_value_is_an_error_with_advice(self):
        r = self.run_one('(id="a")', "x = 1")
        self.assertEqual(r.status, "error")
        self.assertIn("produced no value", r.meta["error"]["message"])

    def test_trailing_semicolon_suppresses_the_value(self):
        r = self.run_one('(id="a", display="output")', "print('shown')\n{'zzsuppressed': 1};")
        self.assertTrue(r.ok)
        html = self.store.read_file(r.block.key, "fragment.html")
        self.assertIn("shown", html)
        self.assertNotIn("zzsuppressed", html)  # (not "hidden": the inline CSS contains `overflow:hidden`)

    def test_view_for_interactive_use_includes_the_code(self):
        (block,) = ExampleParser.parse(doc(('(id="a")', "x = {'energy': 1.5}\nx")), owner="o").blocks
        view = ExampleView(block, {"energy": 1.5}, "")
        html = view.to_element("static").tostring()
        self.assertIn('class="mcr-code"', html)  # the source is shown first
        self.assertIn("energy", html)
        self.assertLess(html.index('class="mcr-code"'), html.index("1.5000") if "1.5000" in html else len(html))

    def test_display_none_has_no_view(self):
        (block,) = ExampleParser.parse(doc(('(id="a", display="none")', "x = 1")), owner="o").blocks
        view = ExampleView(block)
        self.assertEqual(view.display, "none")
        self.assertIsNone(view.node())
        self.assertIsNone(view.to_fragment())
        self.assertIsNone(view.to_element("static"))


class FailureTests(RunnerCase):
    def test_errors_are_cached_with_a_user_code_traceback(self):
        text = doc(('(id="a")', "calls.append('a')\nvalue = 1 / 0\nvalue"))
        runner = self.runner()
        (r,) = runner.run_text(text, owner="o")
        self.assertEqual(r.status, "error")
        error = self.meta(text)["error"]
        self.assertEqual(error["type"], "ZeroDivisionError")
        self.assertIn('File "<example a>", line 2', error["traceback"])
        self.assertIn("value = 1 / 0", error["traceback"])
        self.assertNotIn("Examples.py", error["traceback"])
        self.assertEqual(self.store.load_manifest()["entries"]["a"]["status"], "error")
        # cached: not re-run without a refresh
        self.assertEqual(runner.run_text(text, owner="o"), [])
        self.assertEqual(self.calls, ["a"])
        self.assertEqual([r.status for r in runner.run_text(text, owner="o", refresh="a")], ["error"])

    def test_later_blocks_in_a_failed_chain_are_blocked_and_not_stored(self):
        text = doc(('(id="a")', "1 / 0"), ('(id="b")', "{'ok': 1}"))
        runner = self.runner()
        results = runner.run_text(text, owner="o")
        self.assertEqual([(r.block.id, r.status) for r in results], [("a", "error"), ("b", "blocked")])
        self.assertEqual(results[1].blocked_by, "a")
        self.assertIsNone(self.meta(text, 1))
        # blocked blocks are retried on the next run (and are blocked again while `a` stays broken)
        again = runner.run_text(text, owner="o")
        self.assertEqual([(r.block.id, r.status) for r in again], [("b", "blocked")])

    def test_syntax_errors_and_exit_are_recorded_not_raised(self):
        for src, kind in (("def broken(:\n    pass", "SyntaxError"), ("raise SystemExit(3)", "SystemExit")):
            with self.subTest(kind):
                text = doc(('(id="a")', src))
                (r,) = self.runner().run_text(text, owner=kind)
                self.assertEqual(r.status, "error")
                self.assertEqual(r.meta["error"]["type"], kind)

    @unittest.skipUnless(hasattr(__import__("signal"), "setitimer"), "needs SIGALRM")
    def test_timeout(self):
        text = doc(('(id="a", timeout=0.2)', "while True:\n    pass"))
        (r,) = self.runner().run_text(text, owner="o")
        self.assertEqual(r.status, "error")
        self.assertEqual(r.meta["error"]["type"], "ExampleTimeout")

    def test_failure_in_rendering_is_an_error_not_a_crash(self):
        def broken(value, options):
            raise RuntimeError("cannot display")

        text = doc(('(id="a")', "{'x': 1}"))
        (r,) = self.runner(to_readout=broken).run_text(text, owner="o")
        self.assertEqual(r.status, "error")
        self.assertIn("cannot display", r.meta["error"]["message"])

    def test_stdout_is_captured_not_printed(self):
        import contextlib, io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.runner().run_text(doc(('(id="a", display="output")', "print('inside')")), owner="o")
        self.assertEqual(buf.getvalue(), "")


class StylesheetModeTests(RunnerCase):
    def test_stylesheet_mode_writes_one_shared_stylesheet(self):
        text = doc(('(id="a")', "{'x': 1}"), ('(id="b")', "{'y': 2}"))
        results = self.runner(css="stylesheet").run_text(text, owner="o")
        self.assertEqual([r.status for r in results], ["ok", "ok"])
        html = self.store.read_file(results[0].block.key, "fragment.html")
        self.assertNotIn("<style", html)
        with open(os.path.join(self.store.root, "mcr.css"), encoding="utf-8") as f:
            css = f.read()
        self.assertIn(".mcr-root", css)
        self.assertEqual(results[0].meta["css_md5"], self.store.stylesheet_md5())
        self.assertEqual(results[0].meta["fragment"]["css"], "stylesheet")

    def test_marker_css_overrides_runner_default(self):
        text = doc(('(id="a", css="stylesheet")', "{'x': 1}"))
        (r,) = self.runner(css="inline").run_text(text, owner="o")
        self.assertNotIn("<style", self.store.read_file(r.block.key, "fragment.html"))

    def test_conflicting_styles_cannot_share_one_stylesheet(self):
        text = doc(('(id="a")', "{'x': 1}"),
                   ('(id="b", style={"html": {"font_scale": 0.5}})', "{'y': 2}"))
        results = self.runner(css="stylesheet").run_text(text, owner="o")
        self.assertEqual([r.status for r in results], ["ok", "error"])
        self.assertIn("shared mcr.css", results[1].meta["error"]["message"])


if __name__ == "__main__":
    unittest.main()

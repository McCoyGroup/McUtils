"""Tests for documentation examples that produce readouts (parsing, chained keys, store, cache policy)."""

import json
import os
import tempfile
import unittest

from McUtils.Docs.Examples import (
    ExampleMarkerError, ExampleParser, ReadoutStore, ExampleCache, compute_key
)


def page(*blocks, head="Intro text\n\n", tail="\nOutro\n"):
    return head + "\n".join(blocks) + tail


def block(src, marker='<!-- readout(id="{id}") -->', id=None, fence="```python"):
    m = "" if marker is None else marker.replace("{id}", str(id)) + "\n"
    return m + fence + "\n" + src + "\n```\n"


class ParserTests(unittest.TestCase):
    def test_basic_block_and_round_trip(self):
        text = page(block("x = 1\nx", id="demo"))
        parsed = ExampleParser.parse(text, owner="pkg.fn")
        self.assertEqual(str(parsed), text)
        (b,) = parsed.blocks
        self.assertEqual(b.id, "demo")
        self.assertEqual(b.source, "x = 1\nx\n")
        self.assertEqual(b.owner, "pkg.fn")
        self.assertEqual(b.line, 3)
        self.assertEqual(len(b.key), 32)

    def test_default_ids(self):
        text = page(block("a", marker="<!-- readout -->"), block("b", marker="<!-- readout() -->"))
        ids = [b.id for b in ExampleParser.parse(text, owner="pkg.fn").blocks]
        self.assertEqual(ids, ["pkg.fn#1", "pkg.fn#2"])
        ids = [b.id for b in ExampleParser.parse(text).blocks]
        self.assertEqual(ids, ["example#1", "example#2"])

    def test_unmarked_fences_are_plain_text(self):
        text = page(block("print(1)", marker=None))
        parsed = ExampleParser.parse(text)
        self.assertEqual(parsed.blocks, [])
        self.assertEqual(str(parsed), text)

    def test_marker_inside_another_fence_is_inert(self):
        text = "Docs about markers:\n\n````\n<!-- readout(id=\"x\") -->\n```python\nx\n```\n````\n"
        parsed = ExampleParser.parse(text)
        self.assertEqual(parsed.blocks, [])
        self.assertEqual(str(parsed), text)

    def test_options(self):
        marker = '<!-- readout(id="a", include=["overview", "normal_modes"], exclude="cartesians", ' \
                 'units={"length": "Angstroms"}, display="both", css="stylesheet", isolated=True, timeout=30) -->'
        (b,) = ExampleParser.parse(page(block("x", marker=marker))).blocks
        self.assertEqual(b.options["include"], ["overview", "normal_modes"])
        self.assertEqual(b.options["units"], {"length": "Angstroms"})
        self.assertTrue(b.isolated)
        self.assertEqual(b.options["timeout"], 30)

    def test_positional_id(self):
        (b,) = ExampleParser.parse(page(block("x", marker='<!-- readout("short") -->'))).blocks
        self.assertEqual(b.id, "short")

    def test_multiline_marker(self):
        marker = '<!-- readout(\n    id="m",\n    include=["overview"],\n) -->'
        text = page(block("x", marker=marker))
        parsed = ExampleParser.parse(text)
        (b,) = parsed.blocks
        self.assertEqual(b.id, "m")
        self.assertEqual(str(parsed), text)

    def test_blank_line_between_marker_and_fence(self):
        text = '<!-- readout(id="a") -->\n\n```python\nx\n```\n'
        (b,) = ExampleParser.parse(text).blocks
        self.assertEqual(b.source, "x\n")

    def test_indented_fence_is_dedented(self):
        text = '<!-- readout(id="a") -->\n   ```python\n   if x:\n       y\n   ```\n'
        (b,) = ExampleParser.parse(text).blocks
        self.assertEqual(b.source, "if x:\n    y\n")

    def test_tilde_and_longer_fences(self):
        text = '<!-- readout(id="a") -->\n~~~python\nx = "```"\n~~~\n'
        (b,) = ExampleParser.parse(text).blocks
        self.assertEqual(b.source, 'x = "```"\n')
        text = '<!-- readout(id="b") -->\n````py\nx\n```\ny\n````\n'
        (b,) = ExampleParser.parse(text).blocks
        self.assertEqual(b.source, "x\n```\ny\n")

    def test_render_replaces_blocks(self):
        text = page(block("a", id="one"), block("b", id="two"))
        out = ExampleParser.parse(text).render(lambda b: "[[{}]]\n".format(b.id))
        self.assertIn("[[one]]", out)
        self.assertIn("[[two]]", out)
        self.assertNotIn("readout", out)
        self.assertTrue(out.startswith("Intro text"))
        self.assertTrue(out.rstrip().endswith("Outro"))

    def test_line_offset(self):
        text = page(block("x", id="a"))
        (b,) = ExampleParser.parse(text, first_line=100).blocks
        self.assertEqual(b.line, 102)

    def test_errors(self):
        cases = {
            "unknown option": '<!-- readout(bogus=1) -->\n```python\nx\n```\n',
            "non-literal": '<!-- readout(include=foo()) -->\n```python\nx\n```\n',
            "bad display": '<!-- readout(display="loud") -->\n```python\nx\n```\n',
            "bad id": '<!-- readout(id="has space") -->\n```python\nx\n```\n',
            "bad timeout": '<!-- readout(timeout=-1) -->\n```python\nx\n```\n',
            "twice": '<!-- readout(id="a", id="b") -->\n```python\nx\n```\n',
            "two positional": '<!-- readout("a", "b") -->\n```python\nx\n```\n',
            "star": '<!-- readout(**{}) -->\n```python\nx\n```\n',
            "syntax": '<!-- readout(id=) -->\n```python\nx\n```\n',
            "not a call": '<!-- readout id=x -->\n```python\nx\n```\n',
            "no fence": '<!-- readout(id="a") -->\nJust text\n',
            "not python": '<!-- readout(id="a") -->\n```bash\nls\n```\n',
            "no language": '<!-- readout(id="a") -->\n```\nls\n```\n',
            "unterminated fence": '<!-- readout(id="a") -->\n```python\nx\n',
            "unterminated marker": '<!-- readout(id="a"\n```python\nx\n```\n',
            "duplicate": '<!-- readout(id="a") -->\n```python\nx\n```\n<!-- readout(id="a") -->\n```python\ny\n```\n',
        }
        for name, text in cases.items():
            with self.subTest(name):
                with self.assertRaises(ExampleMarkerError):
                    ExampleParser.parse(text, owner="pkg.fn")

    def test_error_mentions_location(self):
        try:
            ExampleParser.parse("a\nb\n<!-- readout(bogus=1) -->\n```python\nx\n```\n", owner="pkg.fn", first_line=10)
        except ExampleMarkerError as e:
            self.assertIn("pkg.fn", str(e))
            self.assertIn("line 12", str(e))
        else:
            self.fail("expected an error")


class KeyTests(unittest.TestCase):
    def keys(self, text):
        return [b.key for b in ExampleParser.parse(text).blocks]

    def test_stable_and_deterministic(self):
        text = page(block("x = 1", id="a"))
        self.assertEqual(self.keys(text), self.keys(text))

    def test_source_changes_key(self):
        self.assertNotEqual(self.keys(page(block("x = 1", id="a"))), self.keys(page(block("x = 2", id="a"))))

    def test_id_timeout_and_marker_formatting_do_not_change_key(self):
        a = self.keys(page(block("x", marker='<!-- readout(id="a") -->')))
        b = self.keys(page(block("x", marker='<!--   readout( id = "zzz",  timeout=99 )   -->')))
        self.assertEqual(a, b)

    def test_output_affecting_options_change_key(self):
        base = self.keys(page(block("x", marker="<!-- readout -->")))
        for opt in ('include=["overview"]', 'exclude=["a"]', 'units="default"', 'style="talk"',
                    'display="output"', 'css="stylesheet"'):
            with self.subTest(opt):
                other = self.keys(page(block("x", marker="<!-- readout({}) -->".format(opt))))
                self.assertNotEqual(base, other)

    def test_option_order_does_not_matter(self):
        a = self.keys(page(block("x", marker='<!-- readout(include=["a"], style="t") -->')))
        b = self.keys(page(block("x", marker='<!-- readout(style="t", include=["a"]) -->')))
        self.assertEqual(a, b)

    def test_line_endings_and_trailing_newlines_normalized(self):
        unix = '<!-- readout(id="a") -->\n```python\nx = 1\ny\n```\n'
        dos = unix.replace("\n", "\r\n")
        self.assertEqual(self.keys(unix), self.keys(dos))

    def test_whitespace_in_source_matters(self):
        a = self.keys(page(block("if x:\n    y", id="a")))
        b = self.keys(page(block("if x:\n  y", id="a")))
        self.assertNotEqual(a, b)

    def test_chaining(self):
        def doc(first, second="b", third="c"):
            return page(block(first, id="one"), block(second, id="two"), block(third, id="three"))

        base = self.keys(doc("a"))
        edited_first = self.keys(doc("A"))
        self.assertNotEqual(base[0], edited_first[0])
        self.assertNotEqual(base[1], edited_first[1])
        self.assertNotEqual(base[2], edited_first[2])
        edited_last = self.keys(doc("a", third="C"))
        self.assertEqual(base[:2], edited_last[:2])
        self.assertNotEqual(base[2], edited_last[2])

    def test_chained_key_depends_on_previous_key(self):
        parsed = ExampleParser.parse(page(block("a", id="one"), block("b", id="two")))
        b1, b2 = parsed.blocks
        self.assertEqual(b1.prev_key, "")
        self.assertEqual(b2.prev_key, b1.key)
        self.assertEqual(b2.key, compute_key("b", {"id": "two"}, b1.key))

    def test_isolated_breaks_chain(self):
        def doc(first, third="c"):
            return page(
                block(first, id="one"),
                block("b", marker='<!-- readout(id="two", isolated=True) -->'),
                block(third, id="three")
            )

        base = self.keys(doc("a"))
        edited = self.keys(doc("A"))
        self.assertNotEqual(base[0], edited[0])
        self.assertEqual(base[1:], edited[1:])
        self.assertEqual(ExampleParser.parse(doc("a")).blocks[1].prev_key, "")

    def test_same_example_on_two_pages_shares_a_key(self):
        a = ExampleParser.parse(page(block("x", id="a")), owner="one").blocks[0].key
        b = ExampleParser.parse(page(block("x", id="b")), owner="two").blocks[0].key
        self.assertEqual(a, b)

    def test_chain_helper(self):
        parsed = ExampleParser.parse(page(
            block("a", id="one"),
            block("b", id="two"),
            block("c", marker='<!-- readout(id="three", isolated=True) -->'),
            block("d", id="four"),
        ))
        one, two, three, four = parsed.blocks
        self.assertEqual([b.id for b in parsed.chain(one)], ["one"])
        self.assertEqual([b.id for b in parsed.chain(two)], ["one", "two"])
        self.assertEqual([b.id for b in parsed.chain(three)], ["three"])
        self.assertEqual([b.id for b in parsed.chain(four)], ["three", "four"])


class DocstringTests(unittest.TestCase):
    def test_marker_survives_the_docstring_field_parser(self):
        from McUtils.Docs.DocWalker import FunctionWriter

        def f(x):
            """
            Does a thing.

            :param x: a value
            :type x: int
            :examples:
            Show it

            <!-- readout(id="f-demo", include=["overview"], isolated=True) -->
            ```python
            y = f(1)
            y
            ```

            ```python
            print("plain")
            ```
            :related: .g
            """

        _, _, fields = FunctionWriter(f).parse_doc(f.__doc__)
        parsed = ExampleParser.parse(fields["examples"], owner="f")
        (b,) = parsed.blocks
        self.assertEqual(b.id, "f-demo")
        self.assertEqual(b.source, "y = f(1)\ny\n")
        self.assertTrue(b.isolated)
        self.assertEqual(b.options["include"], ["overview"])
        self.assertIn('print("plain")', str(parsed))


class StoreTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = os.path.join(self._tmp.name, "readouts")
        self.store = ReadoutStore(self.root)
        self.key = "ab" + "0" * 30

    def test_round_trip(self):
        self.assertFalse(self.store.has(self.key))
        self.assertIsNone(self.store.read_meta(self.key))
        path = self.store.write(
            self.key,
            {"status": "ok", "options": {"include": ["overview"]}},
            {"fragment.html": "<div>é</div>", "readout.json": "{}", "assets/a.glb": b"\x00\x01"}
        )
        self.assertEqual(path, os.path.join(self.root, "ab", self.key))
        self.assertTrue(self.store.has(self.key))
        meta = self.store.read_meta(self.key)
        self.assertEqual(meta["status"], "ok")
        self.assertEqual(meta["key"], self.key)
        self.assertIn("written", meta)
        self.assertEqual(self.store.read_file(self.key, "fragment.html"), "<div>é</div>")
        self.assertEqual(self.store.read_file(self.key, "assets/a.glb", binary=True), b"\x00\x01")
        self.assertEqual(self.store.keys(), [self.key])
        self.assertEqual([n for n in os.listdir(self.root) if n.startswith(".tmp")], [])

    def test_rewrite_replaces_old_files(self):
        self.store.write(self.key, {"status": "ok"}, {"old.txt": "old"})
        self.store.write(self.key, {"status": "ok"}, {"new.txt": "new"})
        self.assertFalse(os.path.exists(self.store.entry_path(self.key, "old.txt")))
        self.assertEqual(self.store.read_file(self.key, "new.txt"), "new")

    def test_rejects_bad_names_and_keys(self):
        for name in ("../x", "/abs", "a//b", "", "meta.json"):
            with self.subTest(name):
                with self.assertRaises(ValueError):
                    self.store.write(self.key, {}, {name: "x"})
        self.assertEqual(self.store.keys(), [])  # nothing half-written
        for key in ("short", "../" + "a" * 29, "Z" * 32):
            with self.subTest(key):
                with self.assertRaises(ValueError):
                    self.store.entry_path(key)

    def test_prune(self):
        k2 = "cd" + "1" * 30
        k3 = "ab" + "2" * 30
        for k in (self.key, k2, k3):
            self.store.write(k, {"status": "ok"})
        self.assertEqual(self.store.prune([self.key], dry_run=True), sorted([k2, k3]))
        self.assertEqual(len(self.store.keys()), 3)
        self.store.prune([self.key])
        self.assertEqual(self.store.keys(), [self.key])
        self.assertFalse(os.path.exists(os.path.join(self.root, "cd")))

    def test_manifest_is_stable(self):
        self.assertEqual(self.store.load_manifest()["entries"], {})
        entries = {"b": {"key": self.key, "status": "ok"}, "a": {"key": self.key, "status": "missing"}}
        self.assertTrue(self.store.update_manifest(entries))
        self.assertFalse(self.store.update_manifest(entries))  # unchanged: file not rewritten
        with open(os.path.join(self.root, "manifest.json")) as f:
            raw = f.read()
        self.assertEqual(list(json.loads(raw)["entries"]), ["a", "b"])
        self.assertTrue(raw.endswith("\n"))
        self.assertTrue(self.store.update_manifest({}, drop=["a"]))
        self.assertEqual(list(self.store.load_manifest()["entries"]), ["b"])


class CacheTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.store = ReadoutStore(os.path.join(self._tmp.name, "readouts"))
        self.parsed = ExampleParser.parse(
            page(block("a", id="water-1"), block("b", id="water-2"), block("c", id="benzene-1")), owner="o"
        )
        self.blocks = self.parsed.blocks

    def cache(self, **kw):
        return ExampleCache(self.store, **kw)

    def test_status_and_default_plan(self):
        cache = self.cache()
        self.assertEqual([cache.status(b) for b in self.blocks], ["missing"] * 3)
        self.store.write(self.blocks[0].key, {"status": "ok"})
        self.store.write(self.blocks[1].key, {"status": "error", "error": "Traceback"})
        self.assertEqual([cache.status(b) for b in self.blocks], ["ok", "error", "missing"])
        # hits and cached errors are not re-run by default
        self.assertEqual([(b.id, r) for b, r in cache.plan(self.blocks)], [("benzene-1", "missing")])
        self.assertEqual(dict(cache.report(self.blocks)),
                         {"ok": ["water-1"], "stale": [], "error": ["water-2"], "missing": ["benzene-1"]})

    def test_refresh_modes(self):
        cache = self.cache()
        for b in self.blocks:
            self.store.write(b.key, {"status": "ok"})
        self.assertEqual(cache.plan(self.blocks), [])
        self.assertEqual([b.id for b, _ in cache.plan(self.blocks, refresh=True)], ["water-1", "water-2", "benzene-1"])
        self.assertEqual([b.id for b, _ in cache.plan(self.blocks, refresh="all")], ["water-1", "water-2", "benzene-1"])
        self.assertEqual([b.id for b, _ in cache.plan(self.blocks, refresh="water-*")], ["water-1", "water-2"])
        self.assertEqual([b.id for b, _ in cache.plan(self.blocks, refresh=["benzene-*", "water-1"])],
                         ["water-1", "benzene-1"])
        self.assertEqual(cache.plan(self.blocks, refresh="stale"), [])

    def test_staleness_from_revisions(self):
        for b in self.blocks:
            self.store.write(b.key, {"status": "ok", "revisions": {"McUtils": "old"}})
        fresh = self.cache(revisions={"McUtils": "old"})
        stale = self.cache(revisions={"McUtils": "new"})
        self.assertEqual(fresh.status(self.blocks[0]), "ok")
        self.assertEqual(stale.status(self.blocks[0]), "stale")
        self.assertEqual(stale.plan(self.blocks), [])  # no refresh by default, even if stale
        self.assertEqual([(b.id, r) for b, r in stale.plan(self.blocks, refresh="stale")],
                         [(b.id, "stale") for b in self.blocks])
        self.assertEqual(self.cache().status(self.blocks[0]), "ok")  # staleness checks off without revisions

    def test_editing_an_early_block_invalidates_later_entries(self):
        cache = self.cache()
        for b in self.blocks:
            self.store.write(b.key, {"status": "ok"})
        edited = ExampleParser.parse(
            page(block("A", id="water-1"), block("b", id="water-2"), block("c", id="benzene-1")), owner="o"
        ).blocks
        self.assertEqual([b.id for b, _ in cache.plan(edited)], ["water-1", "water-2", "benzene-1"])

    def test_sync_manifest(self):
        cache = self.cache()
        self.store.write(self.blocks[0].key, {"status": "ok"})
        self.assertTrue(cache.sync_manifest(self.blocks))
        entries = self.store.load_manifest()["entries"]
        self.assertEqual(entries["water-1"]["status"], "ok")
        self.assertEqual(entries["water-2"]["status"], "missing")
        self.assertEqual(entries["water-1"]["key"], self.blocks[0].key)
        self.assertEqual(entries["water-1"]["owner"], "o")
        self.assertFalse(cache.sync_manifest(self.blocks))


if __name__ == "__main__":
    unittest.main()

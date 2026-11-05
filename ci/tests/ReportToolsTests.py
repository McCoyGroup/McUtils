"""Tool mode: `report_toolset` (the report operations as tools) and the stdio MCP server around it."""
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

from McUtils.JobDrivers import MCPServer
from McUtils.Readouts.Reports import (ReportDocument, ReportRenderer, ReportTemplate, register_report_template,
                                      report_toolset, template_menu, find_report_template, SourceCatalog)

from ReportFixtures import ToyResult, toy_catalog

HERE = os.path.dirname(os.path.abspath(__file__))


class TemplatedToy(ToyResult):
    pass


@register_report_template(TemplatedToy)
class ToyTemplate(ReportTemplate):
    name = "toy-tools"
    sections = [("Overview", ["summary"]), ("Vibrations", ["frequencies", "missing"])]
    optional = ["picture", "frequencies.nothing"]

    def caption_for(self, handle, section, source):
        return {"summary": "Energy and size.", "frequencies": "Harmonic frequencies."}.get(section)


class LockedToy(ToyResult):
    pass


@register_report_template(LockedToy)
class LockedToyTemplate(ReportTemplate):
    name = "toy-locked"
    sections = [("Overview", ["summary"]), ("Vibrations", ["frequencies"])]
    optional = ["picture"]
    locked = ["summary"]
    locked_headings = ["Vibrations"]

    def caption_for(self, handle, section, source):
        return {"summary": "Energy and size.", "frequencies": "Harmonic frequencies."}.get(section)


def make(policy="grounded", renderer=False, out_dir=None, calls=None, config=None, lock=None, **sources):
    catalog = toy_catalog(**(sources or {"water": lock or TemplatedToy("water")}))
    doc = ReportDocument("Tools", catalog)
    tools = report_toolset(doc, catalog, renderer=ReportRenderer(catalog) if renderer else None, policy=policy,
                           out_dir=out_dir, on_change=None if calls is None else (lambda d: calls.append(len(d.blocks))),
                           **(config or {}))
    return doc, catalog, tools


def ok(result):
    assert result.ok, result.error
    return result.value


class ReadingTests(unittest.TestCase):
    def test_tool_names(self):
        _, _, tools = make()
        self.assertEqual(tools.names(), ["list_sources", "describe_source", "peek", "outline", "compile", "diff", "apply_template",
                                         "add_heading", "add_readout", "add_text", "set_caption", "edit_text", "move",
                                         "remove"])
        self.assertIn("render", make(renderer=True, out_dir="/tmp/x")[2].names())
        with self.assertRaises(ValueError):
            report_toolset(ReportDocument("x"), toy_catalog(), renderer=ReportRenderer(toy_catalog()))

    def test_list_and_describe(self):
        _, _, tools = make()
        rows = ok(tools.call("list_sources"))
        self.assertEqual([(r["handle"], r["template"]) for r in rows], [("water", "toy-tools")])
        d = ok(tools.call("describe_source", {"handle": "water"}))
        t = d["template"]
        self.assertEqual(t["name"], "toy-tools")
        self.assertEqual([h["heading"] for h in t["outline"]], ["Overview", "Vibrations"])
        names = {r["name"]: r for h in t["outline"] for r in h["sections"]}
        self.assertTrue(names["frequencies"]["available"])
        self.assertFalse(names["missing"]["available"])
        self.assertTrue(names["frequencies"]["description"])
        opt = {r["name"]: r for r in t["optional"]}
        self.assertEqual(opt["picture"]["description"], "A picture of the system (no numbers).")
        self.assertEqual(opt["frequencies.nothing"]["part"], "nothing")
        self.assertTrue(all("description" in r for r in d["sections"]))

    def test_generic_template_has_no_outline(self):
        _, catalog, tools = make(plain=ToyResult("plain"))
        self.assertEqual(template_menu(catalog.get("plain"))["outline"], [])
        r = tools.call("apply_template", {"handle": "plain"})
        self.assertFalse(r.ok)
        self.assertEqual(r.error["code"], "no_template")

    def test_peek_is_capped_by_the_schema(self):
        _, _, tools = make()
        self.assertIn("1648.23", ok(tools.call("peek", {"handle": "water", "section": "frequencies"})))
        r = tools.call("peek", {"handle": "water", "section": "frequencies", "max_chars": 99999})
        self.assertEqual(r.error["code"], "bad_arguments")


class TemplateTests(unittest.TestCase):
    def test_apply_template_builds_the_outline(self):
        doc, _, tools = make()
        v = ok(tools.call("apply_template", {"handle": "water"}))
        self.assertEqual(v["skipped_unavailable"], ["missing"])
        kinds = [(b.kind, getattr(b, "text", None) or b.include) for b in doc.blocks]
        self.assertEqual(kinds, [("heading", "Overview"), ("readout", ["summary"]), ("heading", "Vibrations"),
                                 ("readout", ["frequencies"])])
        caps = [(b.caption, b.caption_status) for b in doc.blocks if b.kind == "readout"]
        self.assertEqual(caps, [("Energy and size.", "template"), ("Harmonic frequencies.", "template")])
        self.assertEqual(doc.validate(), [])

    def test_optional_sections_are_added_under_their_own_heading(self):
        doc, _, tools = make()
        ok(tools.call("apply_template", {"handle": "water", "optional": ["picture"]}))
        self.assertEqual([b.text for b in doc.blocks if b.kind == "heading"], ["Overview", "Vibrations", "Additional detail"])
        self.assertEqual(doc.blocks[-1].include, ["picture"])

    def test_only_the_templates_optional_sections_are_accepted(self):
        doc, _, tools = make()
        r = tools.call("apply_template", {"handle": "water", "optional": ["summary"]})
        self.assertEqual(r.error["code"], "unknown_section")
        self.assertEqual(r.error["choices"], ["picture", "frequencies.nothing"])
        self.assertEqual(doc.blocks, [])

    def test_apply_after_a_block(self):
        doc, _, tools = make()
        ok(tools.call("add_heading", {"text": "Intro"}))
        ok(tools.call("add_heading", {"text": "Last"}))
        ok(tools.call("apply_template", {"handle": "water", "after": "h1"}))
        self.assertEqual([getattr(b, "text", None) for b in doc.blocks if b.kind == "heading"],
                         ["Intro", "Overview", "Vibrations", "Last"])


class ReceiptTests(unittest.TestCase):
    def test_mutating_tools_return_a_receipt_not_the_outline(self):
        doc, _, tools = make()
        v = ok(tools.call("add_heading", {"text": "A"}))
        self.assertEqual(v, {"ok": True, "block_id": "h1", "n_blocks": 1, "revision": 1})
        v = ok(tools.call("apply_template", {"handle": "water"}))
        self.assertEqual(sorted(v), ["added", "locked", "n_blocks", "ok", "revision", "skipped_unavailable"])
        self.assertEqual((v["n_blocks"], v["revision"]), (5, 2))
        for name, args in (("move", {"block_id": "h2", "after": "start"}), ("remove", {"block_id": "h2"}),
                           ("edit_text", {"block_id": "h1", "text": "B"})):
            self.assertNotIn("outline", ok(tools.call(name, args)), name)

    def test_the_revision_only_moves_when_something_changed(self):
        doc, _, tools = make()
        ok(tools.call("add_heading", {"text": "A"}))
        self.assertEqual(ok(tools.call("edit_text", {"block_id": "h1", "text": "A"}))["revision"], 1)
        self.assertEqual(ok(tools.call("edit_text", {"block_id": "h1", "text": "B"}))["revision"], 2)
        self.assertFalse(tools.call("remove", {"block_id": "zz"}).ok)
        self.assertEqual(ok(tools.call("outline"))[0]["text"], "B")
        self.assertEqual(ok(tools.call("compile"))["revision"], 2)

    def test_a_failed_mutation_leaves_the_document_and_ids_alone(self):
        doc, _, tools = make()
        ok(tools.call("add_heading", {"text": "A"}))
        before = doc.to_markdown()
        r = tools.call("add_readout", {"handle": "water", "include": ["frequencies"], "caption": "At 12345.6."})
        self.assertEqual(r.error["code"], "ungrounded")
        self.assertEqual(doc.to_markdown(), before)
        self.assertEqual(ok(tools.call("add_readout", {"handle": "water", "include": ["frequencies"]}))["block_id"], "r1")


class CompileAndDiffTests(unittest.TestCase):
    def setUp(self):
        self.doc, _, self.tools = make()
        ok(self.tools.call("apply_template", {"handle": "water"}))

    def test_compile_reads_back_checks_and_sets_a_checkpoint(self):
        c = ok(self.tools.call("compile"))
        self.assertEqual((c["revision"], c["n_blocks"], c["problems"]), (1, 4, []))
        self.assertEqual([b["id"] for b in c["blocks"]], ["h1", "r1", "h2", "r2"])
        self.assertEqual(c["text_status"], {"template": 2})
        self.assertEqual(c["changes_since_last_compile"], 4)       # since the report was opened
        self.assertEqual(c["grounding"], {"policy": "grounded", "rel_tol": 1e-3, "small_int_max": 10, "year_range": [1900, 2100]})
        ok(self.tools.call("add_text", {"text": "Value 1648.23.", "cites": ["r2"]}))
        c = ok(self.tools.call("compile"))
        self.assertEqual((c["changes_since_last_compile"], c["text_status"]), (1, {"template": 2, "grounded": 1}))
        self.assertEqual(ok(self.tools.call("compile"))["changes_since_last_compile"], 0)

    def test_compile_full_text_does_not_clip(self):
        long = "word " * 40 + "end 1648.23"
        ok(self.tools.call("add_text", {"text": long, "cites": ["r2"]}))
        clipped = [b for b in ok(self.tools.call("compile"))["blocks"] if b["kind"] == "prose"][0]
        full = [b for b in ok(self.tools.call("compile", {"full_text": True}))["blocks"] if b["kind"] == "prose"][0]
        self.assertLess(len(clipped["text"]), len(long))
        self.assertEqual(full["text"], long.strip())

    def test_compile_reports_problems(self):
        self.doc.sources["water"]["digest"] = "stale"
        c = ok(self.tools.call("compile"))
        self.assertEqual(c["problems"][0]["problem"], "digest_mismatch")

    def test_diff_since_the_last_change(self):
        ok(self.tools.call("compile"))
        ok(self.tools.call("add_text", {"text": "Value 1648.23.", "cites": ["r2"], "after": "r2"}))
        d = ok(self.tools.call("diff"))
        self.assertEqual((d["since"], d["from_revision"], d["revision"], d["n_changes"]), ("last_change", 1, 2, 1))
        self.assertEqual(d["changes"][0], {"op": "added", "id": "p1", "after": "r2",
                                           "block": {"kind": "prose", "role": "body", "text": "Value 1648.23."}})
        ok(self.tools.call("set_caption", {"block_id": "r2", "text": "Top mode 3943.88."}))
        d = ok(self.tools.call("diff"))
        self.assertEqual(d["changes"], [{"op": "changed", "id": "r2", "fields": {
            "caption": {"from": "Harmonic frequencies.", "to": "Top mode 3943.88."},
            "caption_status": {"from": "template", "to": "grounded"}}}])

    def test_a_failed_request_does_not_change_the_diff(self):
        ok(self.tools.call("add_heading", {"text": "X"}))
        self.assertFalse(self.tools.call("remove", {"block_id": "zz"}).ok)
        d = ok(self.tools.call("diff"))
        self.assertEqual([c["id"] for c in d["changes"]], ["h3"])

    def test_diff_since_the_last_compile_combines_requests(self):
        ok(self.tools.call("compile"))
        ok(self.tools.call("add_heading", {"text": "Extra"}))
        ok(self.tools.call("move", {"block_id": "h2", "after": "start"}))
        ok(self.tools.call("remove", {"block_id": "r1"}))
        ok(self.tools.call("edit_text", {"block_id": "h1", "text": "Renamed"}))
        d = ok(self.tools.call("diff", {"since": "compile"}))
        ops = {(c["op"], c["id"]) for c in d["changes"] if c["op"] != "moved"}
        self.assertEqual(ops, {("added", "h3"), ("removed", "r1"), ("changed", "h1")})
        moved = [c for c in d["changes"] if c["op"] == "moved"]       # h1/h2 swapped: either one is "the" move
        self.assertEqual(len(moved), 1)
        self.assertIn(moved[0]["id"], ("h1", "h2"))
        self.assertEqual([c for c in d["changes"] if c["op"] == "removed"][0]["block"]["include"], ["summary"])
        last = ok(self.tools.call("diff"))
        self.assertEqual([c["id"] for c in last["changes"]], ["h1"])
        ok(self.tools.call("compile"))
        self.assertEqual(ok(self.tools.call("diff", {"since": "compile"}))["n_changes"], 0)

    def test_apply_template_is_one_change_set(self):
        d = ok(self.tools.call("diff"))
        self.assertEqual([c["op"] for c in d["changes"]], ["added"] * 4)
        self.assertEqual(d["from_revision"], 0)

    def test_moving_one_block_is_one_move(self):
        ok(self.tools.call("compile"))
        ok(self.tools.call("move", {"block_id": "r2", "after": "start"}))
        d = ok(self.tools.call("diff", {"since": "compile"}))
        self.assertEqual([(c["op"], c["id"]) for c in d["changes"]], [("moved", "r2")])

    def test_bad_since(self):
        self.assertEqual(self.tools.call("diff", {"since": "yesterday"}).error["code"], "bad_arguments")


class ToleranceTests(unittest.TestCase):
    TEXT = "The bend is at 1648.3."          # evidence 1648.23: off by 0.07, relative 4e-5

    def test_the_default_accepts_a_close_value(self):
        doc, _, tools = make()
        ok(tools.call("apply_template", {"handle": "water"}))
        ok(tools.call("add_text", {"text": self.TEXT, "cites": ["r2"]}))

    def test_a_tighter_tolerance_rejects_it(self):
        doc, _, tools = make(config={"rel_tol": 1e-6})
        ok(tools.call("apply_template", {"handle": "water"}))
        self.assertEqual(tools.call("add_text", {"text": self.TEXT, "cites": ["r2"]}).error["code"], "ungrounded")
        ok(tools.call("add_text", {"text": "The bend is at 1648.23.", "cites": ["r2"]}))
        self.assertEqual(ok(tools.call("compile"))["grounding"]["rel_tol"], 1e-6)

    def test_small_int_max(self):
        doc, _, tools = make(config={"small_int_max": 0})
        ok(tools.call("apply_template", {"handle": "water"}))
        self.assertEqual(tools.call("add_text", {"text": "There are 3 modes.", "cites": ["r2"]}).error["code"], "ungrounded")
        doc, _, tools = make()
        ok(tools.call("add_text", {"text": "There are 3 modes."}))

    def test_four_digit_numbers_in_the_year_range_are_exempt_unless_asked(self):
        # evidence has 1648.23 / 3832.71 / 3943.88: "2000" is not in the data but looks like a year
        doc, _, tools = make()
        ok(tools.call("apply_template", {"handle": "water"}))
        ok(tools.call("add_text", {"text": "Roughly 2000 wavenumbers.", "cites": ["r2"]}))
        self.assertEqual(ok(tools.call("compile"))["grounding"]["year_range"], [1900, 2100])
        doc, _, tools = make(config={"year_range": None})
        ok(tools.call("apply_template", {"handle": "water"}))
        self.assertEqual(tools.call("add_text", {"text": "Roughly 2000 wavenumbers.", "cites": ["r2"]}).error["code"], "ungrounded")
        self.assertIsNone(ok(tools.call("compile"))["grounding"]["year_range"])
        doc, _, tools = make(config={"year_range": (1990, 2010)})
        ok(tools.call("apply_template", {"handle": "water"}))
        self.assertEqual(tools.call("add_text", {"text": "About 1950 wavenumbers.", "cites": ["r2"]}).error["code"], "ungrounded")
        ok(tools.call("add_text", {"text": "About 2000 wavenumbers.", "cites": ["r2"]}))

    def test_bad_settings_are_refused(self):
        for cfg in ({"rel_tol": 0}, {"rel_tol": 1.5}, {"rel_tol": "x"}, {"small_int_max": -1}, {"small_int_max": 2.5},
                    {"year_range": (2000, 1900)}, {"year_range": (1900,)}):
            with self.assertRaises(ValueError, msg=cfg):
                make(config=cfg)


class LockTests(unittest.TestCase):
    def setUp(self):
        self.doc, self.catalog, self.tools = make(lock=LockedToy("water"))
        self.v = ok(self.tools.call("apply_template", {"handle": "water", "optional": ["picture"]}))
        # h1 Overview, r1 summary (locked), h2 Vibrations (locked), r2 frequencies (locked), h3 Additional, r3 picture

    def assertLocked(self, name, args, block_id):
        before, rev = self.doc.to_markdown(), ok(self.tools.call("compile"))["revision"]
        r = self.tools.call(name, args)
        self.assertFalse(r.ok, name)
        self.assertEqual((r.error["code"], r.error["block_id"]), ("locked", block_id), name)
        self.assertEqual(self.doc.to_markdown(), before, name)
        self.assertEqual(ok(self.tools.call("compile"))["revision"], rev, name)

    def test_the_template_decides_what_is_locked(self):
        self.assertEqual(self.v["locked"], ["r1", "h2", "r2"])
        self.assertEqual(self.doc.meta["locked"], ["r1", "h2", "r2"])
        t = ok(self.tools.call("describe_source", {"handle": "water"}))["template"]
        self.assertEqual(t["locked"], ["summary", "everything under 'Vibrations'"])

    def test_locked_blocks_refuse_every_change(self):
        self.assertLocked("set_caption", {"block_id": "r1", "text": "Mine."}, "r1")
        self.assertLocked("edit_text", {"block_id": "h2", "text": "Renamed"}, "h2")
        self.assertLocked("move", {"block_id": "r2", "after": "start"}, "r2")
        self.assertLocked("remove", {"block_id": "r1"}, "r1")
        self.assertLocked("remove", {"block_id": "h2"}, "h2")

    def test_everything_else_still_works(self):
        ok(self.tools.call("set_caption", {"block_id": "r3", "text": "A picture."}))
        ok(self.tools.call("edit_text", {"block_id": "h1", "text": "Overview!"}))
        ok(self.tools.call("move", {"block_id": "r3", "after": "r1"}))     # an unlocked block may sit after a locked one
        ok(self.tools.call("add_text", {"text": "Value 1648.23.", "cites": ["r2"], "after": "r2"}))
        ok(self.tools.call("add_heading", {"text": "More", "after": "r1"}))
        ok(self.tools.call("remove", {"block_id": "r3"}))
        self.assertEqual(self.doc.get("r2").caption, "Harmonic frequencies.")

    def test_the_model_cannot_unlock_and_the_flags_are_visible(self):
        self.assertNotIn("unlock", make()[2].names())
        c = ok(self.tools.call("compile"))
        self.assertEqual(c["locked"], ["r1", "h2", "r2"])
        self.assertEqual([b["id"] for b in c["blocks"] if b.get("locked")], ["r1", "h2", "r2"])
        self.assertEqual([b["id"] for b in ok(self.tools.call("outline")) if b.get("locked")], ["r1", "h2", "r2"])
        c = ok(self.tools.call("compile", {"full_text": True}))
        self.assertTrue([b for b in c["blocks"] if b["id"] == "r1"][0]["locked"])

    def test_locks_survive_a_save_and_reload(self):
        text = self.doc.to_markdown()
        again = ReportDocument.from_markdown(text, self.catalog)
        self.assertEqual(again.meta["locked"], ["r1", "h2", "r2"])
        self.assertEqual(again.to_markdown(), text)
        tools = report_toolset(again, self.catalog)
        r = tools.call("remove", {"block_id": "r2"})
        self.assertEqual(r.error["code"], "locked")

    def test_a_locked_block_can_be_cited_and_commented_on(self):
        ok(self.tools.call("add_text", {"text": "Energy -76.02665.", "cites": ["r1"], "after": "r1"}))

    def test_owner_helpers(self):
        doc, _, tools = make()
        ok(tools.call("apply_template", {"handle": "water"}))
        self.assertEqual(doc.lock(["h1", "r1"]), ["h1", "r1"])
        self.assertEqual(doc.lock(["r1", "r2"]), ["h1", "r1", "r2"])
        self.assertEqual(tools.call("remove", {"block_id": "h1"}).error["code"], "locked")
        self.assertEqual(doc.unlock(["h1"]), ["r1", "r2"])
        ok(tools.call("remove", {"block_id": "h1"}))
        self.assertEqual(doc.unlock(), [])
        self.assertNotIn("locked", doc.meta)
        with self.assertRaises(Exception):
            doc.lock(["nope"])

    def test_unlocked_templates_lock_nothing(self):
        doc, _, tools = make()
        v = ok(tools.call("apply_template", {"handle": "water"}))
        self.assertEqual(v["locked"], [])
        self.assertNotIn("locked", doc.meta)
        self.assertEqual(ok(tools.call("compile"))["locked"], [])

    def test_a_section_name_covers_its_parts(self):
        t = ReportTemplate()
        t.locked = ["normal_modes"]
        self.assertTrue(t.locks("X", "normal_modes.frequencies"))
        self.assertTrue(t.locks("X", "normal_modes"))
        self.assertFalse(t.locks("X", "normal_modes_extra"))


class WritingTests(unittest.TestCase):
    def setUp(self):
        self.doc, self.catalog, self.tools = make()
        ok(self.tools.call("apply_template", {"handle": "water"}))
        self.freq = [b.id for b in self.doc.blocks if b.kind == "readout"][1]

    def test_grounded_text_is_accepted(self):
        v = ok(self.tools.call("add_text", {"text": "The bend is at 1648.23 and there are 3 modes.",
                                            "cites": [self.freq]}))
        self.assertEqual(self.doc.get(v["block_id"]).status, "grounded")

    def test_an_ungrounded_number_is_rejected_and_nothing_is_written(self):
        n = len(self.doc.blocks)
        r = self.tools.call("add_text", {"text": "The bend is at 1700.5.", "cites": [self.freq]})
        self.assertFalse(r.ok)
        self.assertEqual(r.error["code"], "ungrounded")
        self.assertEqual(r.error["unmatched"], ["1700.5"])
        self.assertEqual(len(self.doc.blocks), n)

    def test_text_without_cites_cannot_state_numbers(self):
        r = self.tools.call("add_text", {"text": "The energy is -76.02665."})
        self.assertEqual(r.error["code"], "ungrounded")
        self.assertIn("cites", r.error["detail"])
        ok(self.tools.call("add_text", {"text": "A plain statement with no numbers."}))

    def test_captions_are_checked_against_their_block(self):
        self.assertFalse(self.tools.call("set_caption", {"block_id": self.freq, "text": "Peak at 9999.9."}).ok)
        ok(self.tools.call("set_caption", {"block_id": self.freq, "text": "The top mode is 3943.88."}))
        blk = self.doc.get(self.freq)
        self.assertEqual((blk.caption, blk.caption_status), ("The top mode is 3943.88.", "grounded"))

    def test_a_refused_caption_on_add_readout_leaves_no_block(self):
        n = len(self.doc.blocks)
        r = self.tools.call("add_readout", {"handle": "water", "include": ["frequencies"], "caption": "At 12345.6."})
        self.assertEqual(r.error["code"], "ungrounded")
        self.assertEqual(len(self.doc.blocks), n)
        v = ok(self.tools.call("add_readout", {"handle": "water", "include": ["frequencies"],
                                               "caption": "Frequencies near 3832.71."}))
        self.assertEqual(self.doc.get(v["block_id"]).caption, "Frequencies near 3832.71.")

    def test_edit_text_is_rechecked_against_the_cites(self):
        v = ok(self.tools.call("add_text", {"text": "Value 1648.23.", "cites": [self.freq]}))
        self.assertFalse(self.tools.call("edit_text", {"block_id": v["block_id"], "text": "Value 2222.22."}).ok)
        self.assertEqual(self.doc.get(v["block_id"]).text, "Value 1648.23.")
        ok(self.tools.call("edit_text", {"block_id": v["block_id"], "text": "Value 3943.88."}))
        ok(self.tools.call("edit_text", {"block_id": "h1", "text": "Renamed"}))

    def test_move_remove_and_unknown_blocks(self):
        ok(self.tools.call("move", {"block_id": "h2", "after": "start"}))
        self.assertEqual(self.doc.blocks[0].id, "h2")
        ok(self.tools.call("remove", {"block_id": "h2"}))
        r = self.tools.call("remove", {"block_id": "nope"})
        self.assertEqual((r.ok, r.error["code"]), (False, "unknown_block"))
        r = self.tools.call("add_text", {"text": "x", "cites": ["nope"]})
        self.assertEqual(r.error["code"], "unknown_block")
        r = self.tools.call("add_readout", {"handle": "water", "include": ["nonsense"]})
        self.assertEqual(r.error["code"], "unknown_section")
        self.assertIn("frequencies", r.error["choices"])

    def test_bad_arguments(self):
        self.assertEqual(self.tools.call("add_heading", {"text": "x", "level": 5}).error["code"], "bad_arguments")
        self.assertEqual(self.tools.call("add_heading", {}).error["code"], "bad_arguments")
        self.assertEqual(self.tools.call("nope").error["code"], "unknown_tool")


class PolicyTests(unittest.TestCase):
    def test_unchecked_accepts_any_number_and_marks_it(self):
        doc, _, tools = make(policy="unchecked")
        v = ok(tools.call("add_text", {"text": "Roughly 12345.6 wavenumbers."}))
        self.assertEqual(doc.get(v["block_id"]).status, "unchecked")

    def test_structure_only_turns_text_off_but_not_structure(self):
        doc, _, tools = make(policy="structure_only")
        ok(tools.call("apply_template", {"handle": "water"}))
        for name, args in (("add_text", {"text": "hello"}), ("set_caption", {"block_id": "r1", "text": "hi"}),
                           ("add_readout", {"handle": "water", "include": ["summary"], "caption": "hi"})):
            r = tools.call(name, args)
            self.assertEqual((r.ok, r.error["code"]), (False, "writing_disabled"), name)
        ok(tools.call("edit_text", {"block_id": "h1", "text": "Renamed"}))


class ChangeHookTests(unittest.TestCase):
    def test_on_change_runs_after_each_successful_mutation_only(self):
        calls = []
        _, _, tools = make(calls=calls)
        tools.call("list_sources"); tools.call("outline")
        self.assertEqual(calls, [])
        ok(tools.call("add_heading", {"text": "A"}))
        tools.call("remove", {"block_id": "nope"})
        ok(tools.call("add_heading", {"text": "B"}))
        self.assertEqual(calls, [1, 2])


class RenderToolTests(unittest.TestCase):
    def test_render_writes_the_report(self):
        with tempfile.TemporaryDirectory() as d:
            doc, _, tools = make(renderer=True, out_dir=d)
            ok(tools.call("apply_template", {"handle": "water"}))
            v = ok(tools.call("render", {"formats": ["md", "html"]}))
            self.assertTrue(v["ok"], v)
            self.assertTrue(os.path.exists(v["paths"]["html"]))
            self.assertNotIn("pptx", v["paths"])


class ProtocolTests(unittest.TestCase):
    def setUp(self):
        _, _, tools = make()
        self.server = MCPServer(tools, instructions="use the tools")

    def rpc(self, method, params=None, id=1):
        line = json.dumps({"jsonrpc": "2.0", "id": id, "method": method, **({} if params is None else {"params": params})})
        return json.loads(self.server.handle_line(line))

    def test_initialize_echoes_the_protocol_version(self):
        r = self.rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {}})
        self.assertEqual(r["result"]["protocolVersion"], "2025-06-18")
        self.assertEqual(r["result"]["capabilities"], {"tools": {}})
        self.assertEqual(r["result"]["instructions"], "use the tools")
        self.assertIn("name", r["result"]["serverInfo"])

    def test_notifications_get_no_reply(self):
        self.assertIsNone(self.server.handle_line(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"})))
        self.assertIsNone(self.server.handle_line("   "))

    def test_ping_list_and_call(self):
        self.assertEqual(self.rpc("ping")["result"], {})
        names = [t["name"] for t in self.rpc("tools/list")["result"]["tools"]]
        self.assertIn("apply_template", names)
        schema = self.rpc("tools/list")["result"]["tools"][0]
        self.assertEqual(set(schema), {"name", "description", "inputSchema"})
        r = self.rpc("tools/call", {"name": "list_sources", "arguments": {}})["result"]
        self.assertFalse(r["isError"])
        self.assertEqual(json.loads(r["content"][0]["text"])[0]["handle"], "water")

    def test_tool_errors_are_results_not_protocol_errors(self):
        r = self.rpc("tools/call", {"name": "remove", "arguments": {"block_id": "zz"}})["result"]
        self.assertTrue(r["isError"])
        self.assertEqual(json.loads(r["content"][0]["text"])["error"]["code"], "unknown_block")
        r = self.rpc("tools/call", {"name": "nope"})["result"]
        self.assertTrue(r["isError"])

    def test_protocol_errors(self):
        self.assertEqual(self.rpc("resources/list")["error"]["code"], -32601)
        self.assertEqual(self.rpc("tools/call", {"arguments": {}})["error"]["code"], -32602)
        self.assertEqual(json.loads(self.server.handle_line("{not json"))["error"]["code"], -32700)
        self.assertEqual(json.loads(self.server.handle_line("[1]"))["error"]["code"], -32600)

    def test_call_log_records_each_tool_call(self):
        recs = []
        _, _, tools = make()
        server = MCPServer(tools, call_log=recs.append)
        for name, args in (("list_sources", {}), ("remove", {"block_id": "zz"}), ("nope", {})):
            server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                                           "params": {"name": name, "arguments": args}}))
        server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}))
        self.assertEqual([(r["tool"], r["ok"], r["error_code"]) for r in recs],
                         [("list_sources", True, None), ("remove", False, "unknown_block"), ("nope", False, "unknown_tool")])
        self.assertEqual(recs[1]["arguments"], {"block_id": "zz"})

    def test_call_log_file_and_a_broken_log_does_not_break_calls(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "calls.jsonl")
            _, _, tools = make()
            server = MCPServer(tools, call_log=path)
            line = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "list_sources"}})
            server.handle_line(line)
            server.handle_line(line)
            rows = [json.loads(l) for l in open(path)]
            self.assertEqual([r["tool"] for r in rows], ["list_sources"] * 2)
        bad = MCPServer(tools, call_log=os.path.join("/nonexistent-dir", "x.jsonl"), log=open(os.devnull, "w"))
        self.assertFalse(json.loads(bad.handle_line(line))["result"]["isError"])

    def test_replies_are_single_lines(self):
        line = self.server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                                                   "params": {"name": "describe_source", "arguments": {"handle": "water"}}}))
        self.assertNotIn("\n", line)


SOURCES = '''
from ReportFixtures import ToyResult, toy_catalog
import ReportTools_templates  # registers the toy template


def build_catalog():
    return toy_catalog(water=ReportTools_templates.TemplatedToy("water"))
'''


class SubprocessServerTests(unittest.TestCase):
    """The real thing: ``python -m McUtils.Readouts.Reports`` driven with JSON-RPC lines on stdin."""

    def run_server(self, tmp, lines, extra=()):
        with open(os.path.join(tmp, "ReportTools_templates.py"), "w") as f:
            f.write("from ReportToolsTests import TemplatedToy, ToyTemplate\n")
        with open(os.path.join(tmp, "toy_sources.py"), "w") as f:
            f.write(SOURCES)
        env = dict(os.environ)
        env["PYTHONPATH"] = os.pathsep.join([tmp, HERE] + [p for p in sys.path if p and os.path.isdir(p)][:0]
                                            + ([env["PYTHONPATH"]] if env.get("PYTHONPATH") else []))
        md = os.path.join(tmp, "report.md")
        p = subprocess.run([sys.executable, "-m", "McUtils.Readouts.Reports", md, "--sources",
                            os.path.join(tmp, "toy_sources.py"), "--title", "Served", *extra],
                           input="\n".join(json.dumps(l) for l in lines) + "\n", capture_output=True, text=True,
                           env=env, timeout=100)
        replies = [json.loads(l) for l in p.stdout.splitlines() if l.strip()]
        return md, replies, p

    def call(self, id, name, **args):
        return {"jsonrpc": "2.0", "id": id, "method": "tools/call", "params": {"name": name, "arguments": args}}

    def test_session(self):
        with tempfile.TemporaryDirectory() as tmp:
            lines = [{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-03-26"}},
                     {"jsonrpc": "2.0", "method": "notifications/initialized"},
                     {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
                     self.call(3, "apply_template", handle="water"),
                     self.call(4, "remove", block_id="zzz"),
                     self.call(5, "add_text", text="The bend is 1648.23.", cites=["r2"]),
                     self.call(6, "compile")]
            md, replies, p = self.run_server(tmp, lines, extra=("--rel-tol", "1e-5", "--small-int-max", "3", "--check-years"))
            self.assertEqual(p.returncode, 0, p.stderr)
            by_id = {r["id"]: r for r in replies}
            self.assertEqual(sorted(by_id), [1, 2, 3, 4, 5, 6])
            self.assertEqual(by_id[1]["result"]["protocolVersion"], "2025-03-26")
            self.assertIn("render", [t["name"] for t in by_id[2]["result"]["tools"]])
            self.assertFalse(by_id[3]["result"]["isError"])
            self.assertTrue(by_id[4]["result"]["isError"])
            self.assertEqual(json.loads(by_id[4]["result"]["content"][0]["text"])["error"]["code"], "unknown_block")
            self.assertFalse(by_id[5]["result"]["isError"], by_id[5])
            comp = json.loads(by_id[6]["result"]["content"][0]["text"])
            self.assertEqual(comp["grounding"], {"policy": "grounded", "rel_tol": 1e-5, "small_int_max": 3,
                                                 "year_range": None})
            self.assertEqual(comp["revision"], 2)
            self.assertNotIn("outline", json.loads(by_id[3]["result"]["content"][0]["text"]))
            text = open(md).read()
            self.assertIn("The bend is 1648.23.", text)
            self.assertIn("Harmonic frequencies.", text)
            again = ReportDocument.from_markdown(text, toy_catalog(water=TemplatedToy("water")))
            self.assertEqual(again.to_markdown(), text)
            self.assertIn("serving", p.stderr)

    def test_the_file_is_saved_after_each_mutation_and_reloaded(self):
        with tempfile.TemporaryDirectory() as tmp:
            md, _, _ = self.run_server(tmp, [self.call(1, "add_heading", text="First")])
            self.assertIn("## First", open(md).read())
            md, replies, _ = self.run_server(tmp, [self.call(1, "outline"), self.call(2, "add_heading", text="Second")])
            rows = json.loads(replies[0]["result"]["content"][0]["text"])
            self.assertEqual([r["text"] for r in rows], ["First"])
            text = open(md).read()
            self.assertLess(text.index("First"), text.index("Second"))

    def test_lock_and_unlock_from_the_command_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.run_server(tmp, [self.call(1, "apply_template", handle="water")])
            md, replies, p = self.run_server(tmp, [self.call(1, "remove", block_id="r1"),
                                                   self.call(2, "remove", block_id="h1")],
                                             extra=("--lock", "r1", "--unlock", "h1"))
            by_id = {r["id"]: json.loads(r["result"]["content"][0]["text"]) for r in replies}
            self.assertEqual(by_id[1]["error"]["code"], "locked")
            self.assertTrue(by_id[2]["ok"])
            self.assertEqual(json.loads(re.search(r"<!-- report-meta (.*?) -->", open(md).read()).group(1))["meta"]["locked"],
                             ["r1"])

    def test_stdout_is_protocol_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            _, replies, p = self.run_server(tmp, [{"jsonrpc": "2.0", "id": 1, "method": "ping"}])
            self.assertEqual(p.stdout.strip(), json.dumps({"jsonrpc": "2.0", "id": 1, "result": {}}))


if __name__ == "__main__":
    unittest.main()

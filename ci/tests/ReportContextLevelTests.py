"""context_level: what a model is shown (tools, descriptions, instructions, receipts) at levels 1, 2 and 3."""
import unittest

from McUtils.JobDrivers import MCPServer
from McUtils.Readouts.Reports import (ReportDocument, report_toolset, ReportTemplate, register_report_template,
                                      report_instructions, context_level, LEVEL_TOOLS, REPORT_INSTRUCTIONS)
from ReportFixtures import toy_catalog, ToyResult


class LevelToy(ToyResult):
    pass


@register_report_template(LevelToy)
class LevelToyTemplate(ReportTemplate):
    name = "toy-levels"
    sections = [("Structure", ["summary"]), ("Vibrations", ["frequencies"])]
    optional = ["picture"]


def ok(result):
    assert result.ok, result.error
    return result.value


def make(level, n_sources=1, **kw):
    sources = {f"s{i}": LevelToy(f"s{i}") for i in range(n_sources)}
    cat = toy_catalog(**sources)
    doc = ReportDocument("Levels", cat)
    return doc, report_toolset(doc, cat, context_level=level, **kw)


class LevelTests(unittest.TestCase):
    def test_level_names(self):
        self.assertEqual([context_level(x) for x in (1, 2, 3, "compact", "standard", "full", "2")], [1, 2, 3, 1, 2, 3, 2])
        for bad in (0, 4, "big", True, None):
            with self.assertRaises(ValueError):
                context_level(bad)

    def test_tools_per_level(self):
        names = {lvl: make(lvl)[1].names() for lvl in (1, 2, 3)}
        self.assertEqual(set(names[1]), set(LEVEL_TOOLS[1]) - {"render"})
        for gone in ("list_sources", "describe_source", "outline", "checkpoint", "move", "apply_edits"):
            self.assertNotIn(gone, names[1])
        for lvl in (1, 2, 3):
            self.assertNotIn("apply_edits", names[lvl], "apply_edits is never part of a level")
        self.assertLess(len(names[1]), len(names[2]))
        self.assertEqual(set(names[3]), set(names[2]))

    def test_compact_adds_the_catalog_tools_back_when_the_catalog_is_big(self):
        _, tools = make(1, n_sources=3, inline_max=2)
        self.assertIn("list_sources", tools.names())
        self.assertIn("call list_sources", tools.instructions)

    def test_include_and_exclude(self):
        _, tools = make(1, include_tools=["outline"], exclude_tools=["move_source"])
        self.assertIn("outline", tools.names())
        self.assertNotIn("move_source", tools.names())
        with self.assertRaises(ValueError):
            make(2, include_tools=["bogus"])

    def test_compact_descriptions_are_short_and_schemas_bare(self):
        _, t1 = make(1)
        _, t2 = make(2)
        d1 = {t["name"]: t for t in t1.tools()}
        d2 = {t["name"]: t for t in t2.tools()}
        for name in d1:
            self.assertLessEqual(len(d1[name]["description"]), len(d2[name]["description"]), name)
            for prop in d1[name]["inputSchema"].get("properties", {}).values():
                self.assertNotIn("description", prop, name)
        self.assertIn("description", d2["add_text"]["inputSchema"]["properties"]["cites"])
        size = lambda ts: sum(len(str(t)) for t in ts.tools()) + len(ts.instructions)
        self.assertLess(size(t1), 0.6 * size(t2), "level 1 sends much less text per request")

    def test_instructions(self):
        _, t1 = make(1)
        _, t2 = make(2)
        _, t3 = make(3)
        self.assertIn("- s0: Source s0; Structure [summary]; Vibrations [frequencies]; optional: picture", t1.instructions)
        self.assertLess(len(t1.instructions), len(t2.instructions))
        for t in (t1, t2, t3):
            self.assertNotIn("apply_edits", t.instructions)
        self.assertIn("Why the rules", t3.instructions)
        self.assertNotIn("Why the rules", t2.instructions)
        self.assertIn("listed below", t2.instructions)
        self.assertIn("Start with list_sources", report_instructions(None, 2))
        self.assertEqual(report_instructions(None, 2), REPORT_INSTRUCTIONS)
        for lvl, tools in ((1, t1), (2, t2), (3, t3)):
            for name in tools.names():
                if name not in ("compile", "list_sources", "describe_source", "add_heading", "add_readout",
                                "set_caption", "edit_text", "render") or lvl > 1:
                    self.assertIn(name, tools.instructions, (lvl, name))

    def test_every_level_strongly_encourages_placeholders(self):
        for lvl in (1, 2, 3):
            _, tools = make(lvl)
            text = " ".join(tools.instructions.split())
            lead = "WRITE VALUES FROM THE DATA AS PLACEHOLDERS" if lvl == 1 else "WRITE VALUES AS PLACEHOLDERS"
            self.assertIn(lead, text, lvl)
            self.assertIn("{r3.frequency[2]}", text, lvl)
            self.assertIn("unit", text.split(lead, 1)[1][:600], lvl)
            self.assertIn("never mistyped" if lvl == 1 else "you never copy a digit", text, lvl)
            self.assertIn("{=300 K}", text, lvl)               # a number from outside the data has its own marker
            self.assertNotIn("ungrounded", text, lvl)           # the number check is only described when it is on
            desc = {t["name"]: t["description"] for t in tools.tools()}
            for name in ("add_text", "set_caption"):
                self.assertIn("placeholder", desc[name], (lvl, name))
            if lvl > 1:
                self.assertIn("WRITE VALUES FROM THE DATA AS PLACEHOLDERS", desc["add_text"])

    def test_derived_values_are_mentioned_only_when_on(self):
        for lvl in (1, 2, 3):
            _, off = make(lvl)
            _, on = make(lvl, allow_derived=True)
            self.assertNotIn("mean(", off.instructions, lvl)
            self.assertIn("mean(", on.instructions, lvl)
            self.assertNotIn("mean(", {t["name"]: t["description"] for t in off.tools()}["add_text"], lvl)
        self.assertIn("mean(", {t["name"]: t["description"] for t in make(2, allow_derived=True)[1].tools()}["add_text"])

    def test_apply_edits_is_off_by_default_at_every_level_and_on_with_the_flag(self):
        for lvl in (1, 2, 3):
            _, tools = make(lvl, apply_edits=True)
            self.assertIn("apply_edits", tools.names(), lvl)
            self.assertIn("apply_edits", tools.instructions, lvl)
            self.assertNotIn("apply_edits", make(lvl)[1].names(), lvl)
        for kw in ({"include_tools": ["apply_edits"]}, {"exclude_tools": ["apply_edits"]}):
            with self.assertRaises(ValueError):
                make(2, **kw)
        self.assertEqual(set(make(2, apply_edits=True)[1].names()) - set(make(2)[1].names()), {"apply_edits"})
        _, tools = make(2, apply_edits=True)
        self.assertTrue(ok(tools.call("compile"))["grounding"]["apply_edits"])
        self.assertFalse(ok(make(2)[1].call("compile"))["grounding"]["apply_edits"])

    def test_compact_receipts_carry_the_order(self):
        doc, tools = make(1)
        v = ok(tools.call("apply_template", {"handle": "s0"}))
        self.assertEqual(v["order"], "h1 Structure: r1 | h2 Vibrations: r2")
        v = ok(tools.call("add_text", {"text": "Lowest {r2.frequency[1]} cm-1.", "under": "h2"}))
        self.assertEqual(v["order"], "h1 Structure: r1 | h2 Vibrations: r2 p1")
        doc2, tools2 = make(2)
        self.assertNotIn("order", ok(tools2.call("apply_template", {"handle": "s0"})))

    def test_compact_peek_and_compile(self):
        doc, tools = make(1)
        text = ok(tools.call("peek", {"handle": "s0", "section": "frequencies", "expand": True}))
        self.assertFalse(text.startswith("Toy s0"), text[:40])
        _, tools2 = make(2)
        self.assertTrue(ok(tools2.call("peek", {"handle": "s0", "section": "frequencies", "expand": True})).startswith("Toy s0"))
        ok(tools.call("apply_template", {"handle": "s0"}))
        self.assertIn("answer the user now", ok(tools.call("compile"))["next"])
        self.assertNotIn("next", ok(tools2.call("compile")))

    def test_errors_say_whether_to_retry(self):
        for lvl in (1, 2, 3):
            doc, tools = make(lvl, policy="grounded")
            ok(tools.call("apply_template", {"handle": "s0"}))
            self.assertEqual(tools.call("apply_template", {"handle": "nope"}).error["retry"], "no")
            self.assertEqual(tools.call("add_text", {"text": "At 1700.5.", "cites": ["r2"]}).error["retry"], "once")
            self.assertEqual(tools.call("remove", {"block_id": "zz"}).error["retry"], "after_fix")

    def test_the_server_sends_the_levels_instructions(self):
        _, tools = make(1)
        server = MCPServer(tools, instructions=tools.instructions)
        r = server.handle({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}})
        self.assertEqual(r["result"]["instructions"], tools.instructions)


class ApplyEditsTests(unittest.TestCase):
    def setUp(self):
        self.doc, self.tools = make(2, apply_edits=True, policy="grounded")
        ok(self.tools.call("apply_template", {"handle": "s0"}))      # h1 r1 | h2 r2, revision 1

    def test_several_steps_one_revision(self):
        v = ok(self.tools.call("apply_edits", {"edits": [
            {"tool": "add_text", "args": {"text": "Energy {r1.energy}.", "under": "h1"}},
            {"tool": "add_text", "args": {"text": "Lowest {r2.frequency[1]} cm-1.", "under": "h2"}},
            {"tool": "add_heading", "args": {"text": "Notes"}},
            {"tool": "add_text", "args": {"text": "See above.", "after": "$3", "cites": ["r2"]}},
        ]}))
        self.assertEqual(v["revision"], 2)
        self.assertEqual([s["block_id"] for s in v["steps"]], ["p1", "p2", "h3", "p3"])
        self.assertEqual(v["order"], "h1 Structure: r1 p1 | h2 Vibrations: r2 p2 | h3 Notes: p3")
        self.assertEqual(v["steps"][0]["filled"][0]["expr"], "r1.energy")

    def test_a_failing_step_changes_nothing(self):
        before = [b.id for b in self.doc.blocks]
        r = self.tools.call("apply_edits", {"edits": [
            {"tool": "add_text", "args": {"text": "Lowest {r2.frequency[1]}.", "under": "h2"}},
            {"tool": "add_text", "args": {"text": "Made up 1700.5.", "cites": ["r2"]}},
        ]})
        self.assertEqual((r.error["code"], r.error["step"], r.error["retry"]), ("ungrounded", 2, "once"))
        self.assertIn("step 2 (add_text)", r.error["detail"])
        self.assertEqual([b.id for b in self.doc.blocks], before)
        self.assertEqual(ok(self.tools.call("compile"))["revision"], 1)

    def test_bad_steps(self):
        r = self.tools.call("apply_edits", {"edits": [{"tool": "add_text", "args": {"txt": "x"}}]})
        self.assertEqual(r.error["code"], "invalid_arguments")
        r = self.tools.call("apply_edits", {"edits": [{"tool": "render"}]})
        self.assertEqual(r.error["code"], "invalid_arguments")
        r = self.tools.call("apply_edits", {"edits": [{"tool": "add_heading", "args": {"text": "A", "after": "$2"}}]})
        self.assertEqual(r.error["code"], "bad_argument")

    def test_locks_hold_inside_a_batch(self):
        self.doc.lock(["r1"])
        r = self.tools.call("apply_edits", {"edits": [{"tool": "remove", "args": {"block_id": "r1"}}]})
        self.assertEqual(r.error["code"], "locked")


if __name__ == "__main__":
    unittest.main()

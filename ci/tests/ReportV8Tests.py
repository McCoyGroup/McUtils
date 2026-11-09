"""
V8: row selectors ({r5.y[max]}, {r5.x[max:y]}), section names that are headings or titles, an idempotent
`apply_template`, advice on a repeated selection, hints that name only the tools the level offers, and computed values on
by default.
"""
import re
import subprocess
import sys
import unittest

from McUtils.Readouts.Reports import (ReportDocument, report_toolset, report_instructions, fill_text, unfill, refill,
                                      ReportTemplate, register_report_template)
from McUtils.Readouts.Reports.Tools import _ALL
from ReportFillTests import make, ok
from ReportFixtures import toy_catalog, ToyResult


class Multi(ToyResult):
    pass


@register_report_template(Multi)
class MultiTemplate(ReportTemplate):
    name = "toy-multi"
    sections = [("Everything", ["summary", "frequencies"])]


def multi(**kw):
    cat = toy_catalog(water=Multi("water"))
    doc = ReportDocument("Multi", cat)
    return doc, cat, report_toolset(doc, cat, **kw)


def text(tools, t, **kw):
    return ok(tools.call("add_text", {"text": t, **kw}))


class SelectorTests(unittest.TestCase):
    def setUp(self):
        self.doc, self.cat, self.tools = make()      # r2.frequency = 1648.23, 3832.71, 3943.88

    def filled(self, t):
        v = text(self.tools, t)
        return self.doc.get(v["block_id"]).text, v

    def test_each_selector_picks_a_row_and_is_not_a_computed_value(self):
        for sel, want in (("max", "3943.88"), ("min", "1648.23"), ("first", "1648.23"), ("last", "3943.88")):
            t, v = self.filled("At {r2.frequency[%s]}." % sel)
            self.assertIn(want, t, sel)
            self.assertFalse(v["filled"][0]["derived"])

    def test_selectors_work_with_derived_values_off(self):
        doc, cat, tools = make(allow_derived=False)
        self.assertIn("3943.88", doc.get(text(tools, "At {r2.frequency[max]}.")["block_id"]).text)

    def test_another_column_can_be_read_at_the_extreme_row(self):
        t, _ = self.filled("{r2.mode[max:frequency]} and {r2.mode[min:frequency]}.")
        self.assertEqual(t, "%s and %s." % (self.mode(3), self.mode(1)))

    def mode(self, row):
        return self.doc.get(text(self.tools, "{r2.mode[%d]}" % row)["block_id"]).text

    def test_the_written_form_keeps_the_selector_and_refill_recomputes_it(self):
        v = text(self.tools, "At {r2.frequency[max]}, {=300 K}.")
        p = self.doc.get(v["block_id"])
        self.assertEqual(self.doc.written_text(p.id), "At {r2.frequency[max]}, {=300 K}.")
        self.assertEqual([f["expr"] for f in p.fills], ["r2.frequency[max]", "=300 K"])

    def test_misuse_is_refused_with_a_reason(self):
        for bad, frag in (("{r2.mode[max]}", "numeric"), ("{r2.frequency[first:mode]}", "takes no column"),
                          ("{r2.frequency[3:mode]}", "[min] or [max]"), ("{r2.frequency[max:nope]}", "not a column")):
            r = self.tools.call("add_text", {"text": bad})
            self.assertEqual(r.error["code"], "bad_reference", bad)
            self.assertIn(frag, r.error["detail"], bad)

    def test_the_row_error_mentions_the_selectors(self):
        r = self.tools.call("add_text", {"text": "{r2.frequency[0]}"})
        self.assertIn("rows start at 1", r.error["detail"])
        self.assertIn("[max]", r.error["detail"])

    def test_first_and_last_work_on_text_columns(self):
        t, _ = self.filled("{r2.mode[first]} {r2.mode[last]}")
        self.assertEqual(t, "%s %s" % (self.mode(1), self.mode(3)))

    def test_ties_give_the_first_row(self):
        from McUtils.Readouts.Reports.Grounding import EvidenceItem, EvidenceSet
        items = EvidenceSet([EvidenceItem(v, None, None, "y", "r9", i + 1, "data", False, "t/y") for i, v in enumerate((2.0, 5.0, 5.0))])
        out, fills = fill_text("{r9.y[max]}", items)
        self.assertEqual(out, "5")
        self.assertEqual(fills[0].inputs[0].row, 2)


class SectionNameTests(unittest.TestCase):
    def test_peek_takes_a_heading_title_or_other_case(self):
        doc, cat, tools = make()
        base = ok(tools.call("peek", {"handle": "water", "section": "frequencies"}))
        for name in ("Vibrations", "FREQUENCIES", "Frequencies"):
            out = ok(tools.call("peek", {"handle": "water", "section": name}))
            self.assertTrue(out.startswith("(Showing section 'frequencies'"), (name, out[:80]))
            self.assertTrue(out.endswith(base), name)
        self.assertEqual(ok(tools.call("peek", {"handle": "water", "section": "frequencies"})), base)

    def test_an_unknown_name_still_lists_the_sections(self):
        doc, cat, tools = make()
        r = tools.call("peek", {"handle": "water", "section": "Spectrum"})
        self.assertEqual(r.error["code"], "unknown_section")
        self.assertIn("frequencies", r.error["choices"])

    def test_add_readout_resolves_names_and_says_so(self):
        doc, cat, tools = make()
        v = ok(tools.call("add_readout", {"handle": "water", "include": ["Vibrations"]}))
        self.assertEqual(v["matched"], {"Vibrations": "frequencies"})
        self.assertEqual(doc.get(v["block_id"]).include, ["frequencies"])

    def test_a_heading_over_several_sections_stands_for_all_of_them(self):
        doc, cat, tools = multi()
        v = ok(tools.call("add_readout", {"handle": "water", "include": ["Everything"]}))
        self.assertEqual(v["matched"], {"Everything": ["summary", "frequencies"]})
        r = tools.call("peek", {"handle": "water", "section": "Everything"})
        self.assertEqual(r.error["code"], "unknown_section")
        self.assertEqual(r.error["choices"], ["summary", "frequencies"])

    def test_exact_names_are_untouched(self):
        doc, cat, tools = make()
        v = ok(tools.call("add_readout", {"handle": "water", "include": ["summary"]}))
        self.assertNotIn("matched", v)


class TemplateTests(unittest.TestCase):
    def test_a_second_apply_adds_nothing_and_leaves_the_baseline_alone(self):
        doc, cat, tools = make()
        ok(tools.call("add_heading", {"text": "Mine"}))
        before = ([b.id for b in doc.blocks], ok(tools.call("compile"))["revision"])
        v = ok(tools.call("apply_template", {"handle": "water"}))
        self.assertTrue(v["already_applied"])
        self.assertEqual(v["added"], [])
        self.assertEqual(v["blocks"], {"summary": "r1", "frequencies": "r2"})
        self.assertIn("r2", v["placeholders"])
        self.assertEqual(([b.id for b in doc.blocks], v["revision"]), before)
        self.assertEqual(ok(tools.call("diff", {"since": "template"}))["n_changes"], 1)       # only 'Mine'

    def test_a_partly_built_template_is_not_repeated(self):
        doc, cat, tools = make()
        ok(tools.call("remove", {"block_id": "r2"}))
        v = ok(tools.call("apply_template", {"handle": "water"}))
        self.assertTrue(v["partly_applied"])
        self.assertEqual(v["missing"], ["frequencies"])
        self.assertEqual([b.id for b in doc.blocks], ["h1", "r1", "h2"])

    def test_again_builds_a_second_copy_and_notes_the_repeat(self):
        doc, cat, tools = make()
        v = ok(tools.call("apply_template", {"handle": "water", "again": True}))
        self.assertEqual(len(v["added"]), 4)
        self.assertTrue(any("same sections" in n for n in v["notes"]))

    def test_another_source_is_not_blocked(self):
        cat = toy_catalog(water=ToyResult("water"))
        doc, cat2, tools = make()
        self.assertEqual(len(doc.blocks), 4)


class DuplicateTests(unittest.TestCase):
    def test_adding_a_selection_that_is_already_shown_is_noted_not_refused(self):
        doc, cat, tools = make()
        v = ok(tools.call("add_readout", {"handle": "water", "include": ["summary"]}))
        self.assertEqual(v["block_id"], "r3")
        self.assertIn("r1, r3", v["notes"][0])

    def test_a_different_selection_has_no_note(self):
        doc, cat, tools = multi()
        ok(tools.call("add_readout", {"handle": "water", "include": ["summary"]}))
        v = ok(tools.call("add_readout", {"handle": "water", "include": ["frequencies"]}))
        self.assertNotIn("notes", v)

    def test_the_default_selection_counts_as_its_sections(self):
        doc, cat, tools = multi()
        ok(tools.call("add_readout", {"handle": "water"}))
        names = ok(tools.call("add_readout", {"handle": "water"}))
        self.assertIn("notes", names)

    def test_compile_lists_the_repeats(self):
        doc, cat, tools = make()
        self.assertEqual([w for w in ok(tools.call("compile"))["warnings"] if w["code"] == "duplicate_selection"], [])
        ok(tools.call("add_readout", {"handle": "water", "include": ["frequencies"]}))
        warn = [w for w in ok(tools.call("compile"))["warnings"] if w["code"] == "duplicate_selection"]
        self.assertEqual(warn[0]["blocks"], ["r2", "r3"])


class HintTests(unittest.TestCase):
    def test_a_hint_names_only_tools_the_level_offers(self):
        for lvl in (1, 2, 3):
            doc, cat, tools = make(context_level=lvl)
            have = set(tools.names())
            for code, hint in tools.hints.items():
                for name in _ALL:
                    if name not in have and name != "render":
                        # "outline" is also an ordinary noun ("no fixed outline"): only a call to the tool counts
                        pattern = r"(?i)\b(call|from|use|with) outline\b|outline or compile" if name == "outline" else r"\b%s\b" % name
                        self.assertIsNone(re.search(pattern, hint), (lvl, code, name))

    def test_the_compact_unknown_section_hint_points_at_the_choices(self):
        doc, cat, tools = make(context_level=1)
        r = tools.call("add_readout", {"handle": "water", "include": ["Spectrum"]})
        self.assertIn("choices", r.error["hint"])
        self.assertNotIn("describe_source", r.error["hint"])

    def test_the_standard_hint_is_unchanged(self):
        doc, cat, tools = make()
        r = tools.call("add_readout", {"handle": "water", "include": ["Spectrum"]})
        self.assertIn("describe_source", r.error["hint"])


class DerivedDefaultTests(unittest.TestCase):
    def test_computed_values_are_on_by_default_and_described_briefly(self):
        doc, cat, tools = make()
        self.assertIn("mean(", tools.instructions)
        self.assertIn("do not add comparisons or statistics the user did not ask for", " ".join(tools.instructions.split()))
        self.assertTrue(ok(tools.call("compile"))["grounding"]["derived"])

    def test_the_instructions_mention_the_selectors(self):
        for lvl in (1, 2, 3):
            self.assertIn("[max]", report_instructions(None, lvl))

    def test_the_cli_can_turn_them_off(self):
        out = subprocess.run([sys.executable, "-m", "McUtils.Readouts.Reports", "--help"], capture_output=True, text=True).stdout
        self.assertIn("--no-derived", out)
        self.assertIn("--derived", out)


if __name__ == "__main__":
    unittest.main()

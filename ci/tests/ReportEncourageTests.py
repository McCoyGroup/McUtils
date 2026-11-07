"""
Encouraging placeholders by design (V7): the number check is off by default; the tools list each block's placeholders
(receipts, `values`, `peek`), readout data is shown as placeholders unless expanded, a paragraph reads back as it was
written, typed numbers get notes (never refusals), given values are marked ``{=300 K}``, ``autolink`` rewrites exact
matches, ``basis`` says what a paragraph is about, and `compile` reports the coverage.
"""
import json
import unittest

from McUtils.Readouts.Reports import (ReportDocument, report_toolset, report_instructions, ReportOperationError,
                                      fill_text, find_markers, unfill, fill_spans, refill, EvidenceSet, EvidenceItem,
                                      autolink, advise, coverage, column_summary)
from ReportFillTests import make, ok, FillToy
from ReportFixtures import toy_catalog


def bare():
    """A document with no blocks yet (so a section is not in the report)."""
    cat = toy_catalog(water=FillToy("water"))
    doc = ReportDocument("Bare", cat)
    return doc, cat, report_toolset(doc, cat)


class DefaultsTests(unittest.TestCase):
    def test_the_number_check_is_off_by_default(self):
        doc, cat, tools = make()
        self.assertEqual(ok(tools.call("compile"))["grounding"]["policy"], "unchecked")
        v = ok(tools.call("add_text", {"text": "The bend is near 1650.5 cm-1 at 300 K."}))     # not in the data, no cites
        self.assertEqual(doc.get(v["block_id"]).status, "unchecked")
        self.assertEqual(doc.get(v["block_id"]).cites, [])

    def test_the_grounded_policy_is_opt_in_and_unchanged(self):
        doc, cat, tools = make(policy="grounded")
        self.assertEqual(tools.call("add_text", {"text": "At 300 K."}).error["code"], "needs_citation")
        self.assertEqual(tools.call("add_text", {"text": "At 1650.5 cm-1.", "cites": ["r2"]}).error["code"], "ungrounded")

    def test_status_says_whether_the_server_wrote_every_number(self):
        doc, cat, tools = make()
        a = ok(tools.call("add_text", {"text": "Lowest {r2.frequency[1]}."}))["block_id"]
        b = ok(tools.call("add_text", {"text": "There are 3 modes."}))["block_id"]
        c = ok(tools.call("add_text", {"text": "Lowest {r2.frequency[1]}, about 3832.71 cm-1."}))["block_id"]
        d = ok(tools.call("add_text", {"text": "Run at {=300 K}."}))["block_id"]
        self.assertEqual([doc.get(x).status for x in (a, b, c, d)], ["checked", "no_numbers", "unchecked", "no_numbers"])

    def test_the_cli_defaults(self):
        import subprocess, sys
        out = subprocess.run([sys.executable, "-m", "McUtils.Readouts.Reports", "--help"], capture_output=True, text=True).stdout
        self.assertIn("--autolink", out)
        self.assertIn("--no-advice", out)
        self.assertIn("unchecked (default)", " ".join(out.split()))


class LiteralTests(unittest.TestCase):
    def setUp(self):
        self.doc, self.cat, self.tools = make()

    def test_a_marker_writes_the_value_as_given_and_records_it(self):
        v = ok(self.tools.call("add_text", {"text": "Run at {=300 K}: {r2.frequency[1]}."}))
        p = self.doc.get(v["block_id"])
        self.assertEqual(p.text, "Run at 300 K: 1648.23 cm⁻¹.")
        self.assertEqual([f["expr"] for f in p.fills], ["=300 K", "r2.frequency[1]"])
        self.assertTrue(any(f.get("literal") for f in v["filled"]))
        self.assertEqual(self.doc.written_text(p.id), "Run at {=300 K}: {r2.frequency[1]}.")

    def test_the_literals_field_is_the_same_thing(self):
        v = ok(self.tools.call("add_text", {"text": "The run used 300 K and 6-31G.", "literals": ["300 K"]}))
        p = self.doc.get(v["block_id"])
        self.assertEqual(p.text, "The run used 300 K and 6-31G.")
        self.assertEqual(self.doc.written_text(p.id), "The run used {=300 K} and 6-31G.")
        self.assertNotIn("notes", v)

    def test_a_literal_that_is_not_in_the_text_is_an_error(self):
        r = self.tools.call("add_text", {"text": "Nothing here.", "literals": ["300 K"]})
        self.assertEqual(r.error["code"], "bad_argument")
        r = self.tools.call("add_text", {"text": "At 300 K.", "literals": ["{=300 K}"]})
        self.assertEqual(r.error["code"], "bad_argument")

    def test_a_literal_is_skipped_by_the_number_check_and_survives_a_round_trip(self):
        doc, cat, tools = make(policy="grounded")
        v = ok(tools.call("add_text", {"text": "At {=300 K}, the bend is {r2.frequency[1]}."}))
        self.assertEqual(doc.get(v["block_id"]).status, "checked")
        again = ReportDocument.from_markdown(doc.to_markdown(), cat)
        self.assertEqual(again.written_text(v["block_id"]), "At {=300 K}, the bend is {r2.frequency[1]}.")
        self.assertTrue(again.check_prose(v["block_id"]).ok)

    def test_markers_and_unfill(self):
        items = self.doc.evidence(["r2"])
        text, fills = fill_text("A {=2 eV} B {r2.frequency[2]:.0f}.", items)
        self.assertEqual(text, "A 2 eV B 3833 cm⁻¹.")
        self.assertEqual([k for _, _, k in find_markers("{=1} {r2.mode[1]} {plain}")], ["literal", "ref"])
        recs = [f.record() for f in fills]
        self.assertEqual(unfill(text, recs), "A {=2 eV} B {r2.frequency[2]:.0f}.")
        self.assertEqual(len(fill_spans(text, recs)), 2)
        spans, problems = refill(text, recs, items)
        self.assertEqual((len(spans), problems), (2, []))


class ReadBackTests(unittest.TestCase):
    def test_compile_shows_a_paragraph_as_it_was_written(self):
        doc, cat, tools = make()
        ok(tools.call("add_text", {"text": "The stretches are {r2.frequency[2]} and {r2.frequency[3]}."}))
        row = {b["id"]: b for b in ok(tools.call("compile", {"full_text": True}))["blocks"]}["p1"]
        self.assertEqual(row["text"], "The stretches are {r2.frequency[2]} and {r2.frequency[3]}.")
        self.assertEqual(row["fills"][0]["text"], "3832.71 cm⁻¹")
        row = {b["id"]: b for b in ok(tools.call("compile", {"full_text": True, "expand": True}))["blocks"]}["p1"]
        self.assertEqual(row["text"], "The stretches are 3832.71 cm⁻¹ and 3943.88 cm⁻¹.")

    def test_the_stored_text_has_the_values(self):
        doc, cat, tools = make()
        ok(tools.call("add_text", {"text": "Lowest {r2.frequency[1]}."}))
        self.assertEqual(doc.get("p1").text, "Lowest 1648.23 cm⁻¹.")
        self.assertIn("1648.23 cm⁻¹", doc.to_markdown())

    def test_a_paragraph_without_fills_reads_back_unchanged(self):
        doc, cat, tools = make()
        ok(tools.call("add_text", {"text": "Plain words."}))
        self.assertEqual(doc.written_text("p1"), "Plain words.")
        with self.assertRaises(ReportOperationError):
            doc.written_text("r2")


class PlaceholderViewTests(unittest.TestCase):
    def test_peek_shows_placeholders_not_data_by_default(self):
        doc, cat, tools = make()
        text = ok(tools.call("peek", {"handle": "water", "section": "frequencies"}))
        self.assertIn("{r2.frequency[ROW]} (rows 1-3): {r2.frequency[1]} = 1648.23 cm⁻¹", text)
        self.assertIn("{r2.mode[ROW]} (rows 1-3, text): {r2.mode[1]} = 'bend'", text)
        self.assertIn("In the report as r2", text)
        self.assertNotIn("3832.71", text)                    # only an example per column, not the data
        self.assertNotIn("sym stretch", text)

    def test_expand_gives_the_text_with_the_values(self):
        doc, cat, tools = make()
        text = ok(tools.call("peek", {"handle": "water", "section": "frequencies", "expand": True}))
        self.assertIn("3832.71", text)
        self.assertIn("sym stretch", text)
        self.assertIn("Placeholders in the report (r2)", text)

    def test_a_section_that_is_not_in_the_report_uses_BLOCK(self):
        doc, cat, tools = bare()
        text = ok(tools.call("peek", {"handle": "water", "section": "frequencies"}))
        self.assertIn("{BLOCK.frequency[ROW]}", text)
        self.assertNotIn("{r0.", text)
        self.assertIn("Not in the report yet", text)
        r = ok(tools.call("add_readout", {"handle": "water", "include": ["frequencies"]}))
        self.assertIn("{r1.frequency[ROW]} (rows 1-3): {r1.frequency[1]} = 1648.23 cm⁻¹", r["placeholders"][1])

    def test_peek_keeps_its_errors(self):
        doc, cat, tools = make()
        self.assertEqual(tools.call("peek", {"handle": "water", "section": "nope"}).error["code"], "unknown_section")

    def test_the_unit_style_applies(self):
        doc, cat, tools = make()
        doc.unit_style = "ascii"
        self.assertIn("1648.23 cm-1", ok(tools.call("peek", {"handle": "water", "section": "frequencies"})))

    def test_receipts_list_the_placeholders(self):
        doc, cat, tools = bare()
        v = ok(tools.call("apply_template", {"handle": "water"}))
        self.assertEqual(sorted(v["placeholders"]), ["r1", "r2"])
        self.assertIn("{r1.energy} = -76.0267 Eₕ", v["placeholders"]["r1"])


class ValuesToolTests(unittest.TestCase):
    def setUp(self):
        self.doc, self.cat, self.tools = make()

    def test_a_block_lists_its_columns(self):
        v = ok(self.tools.call("values", {"block_id": "r2"}))
        self.assertEqual(v["placeholders"][1], "{r2.frequency[ROW]} (rows 1-3): {r2.frequency[1]} = 1648.23 cm⁻¹")

    def test_a_column_lists_every_row(self):
        v = ok(self.tools.call("values", {"block_id": "r2", "column": "frequency"}))
        self.assertEqual([(r["row"], r["use"], r["value"]) for r in v["rows"]],
                         [(1, "{r2.frequency[1]}", "1648.23 cm⁻¹"), (2, "{r2.frequency[2]}", "3832.71 cm⁻¹"),
                          (3, "{r2.frequency[3]}", "3943.88 cm⁻¹")])
        v = ok(self.tools.call("values", {"block_id": "r2", "column": "mode"}))
        self.assertEqual(v["rows"][0]["value"], "bend")

    def test_errors(self):
        self.assertEqual(self.tools.call("values", {"block_id": "r2", "column": "nope"}).error["code"], "bad_reference")
        self.assertEqual(self.tools.call("values", {"block_id": "h1"}).error["code"], "bad_argument")
        self.assertEqual(self.tools.call("values", {"block_id": "zz"}).error["code"], "unknown_block")

    def test_level_one_leaves_it_out_but_include_tools_adds_it(self):
        cat = toy_catalog(water=FillToy("water"))
        self.assertNotIn("values", report_toolset(ReportDocument("x", cat), cat, context_level=1).names())
        self.assertIn("values", report_toolset(ReportDocument("x", cat), cat, context_level=1, include_tools=["values"]).names())


class NotesTests(unittest.TestCase):
    def setUp(self):
        self.doc, self.cat, self.tools = make()

    def test_a_value_of_the_data_gets_its_placeholder(self):
        v = ok(self.tools.call("add_text", {"text": "The stretch is at 3832.71 cm-1."}))
        self.assertEqual(len(v["notes"]), 1)
        self.assertIn("write {r2.frequency[2]}", v["notes"][0])

    def test_a_number_that_is_not_in_the_data_is_offered_the_marker(self):
        v = ok(self.tools.call("add_text", {"text": "Computed at 300 K."}))
        self.assertIn("{=300 K}", v["notes"][0])

    def test_nothing_is_noted_for_placeholders_literals_small_integers_or_years(self):
        v = ok(self.tools.call("add_text", {"text": "In 2019 the 3 modes were {r2.frequency[1]} at {=300 K}."}))
        self.assertNotIn("notes", v)

    def test_notes_never_refuse_and_can_be_switched_off(self):
        doc, cat, tools = make(advice=False)
        v = ok(tools.call("add_text", {"text": "The stretch is at 3832.71 cm-1 and 99.9 K."}))
        self.assertNotIn("notes", v)

    def test_notes_are_capped(self):
        v = ok(self.tools.call("add_text", {"text": " ".join(f"{i}.5 eV" for i in range(20, 30))}))
        self.assertEqual(len(v["notes"]), 7)
        self.assertIn("4 more typed numbers", v["notes"][-1])

    def test_without_cites_the_reports_readouts_are_compared(self):
        v = ok(self.tools.call("add_text", {"text": "Energy -76.0267 Eₕ."}))
        self.assertIn("{r1.energy}", v["notes"][0])

    def test_edit_text_has_notes_too(self):
        ok(self.tools.call("add_text", {"text": "Plain."}))
        v = ok(self.tools.call("edit_text", {"block_id": "p1", "text": "Now 1648.23 cm-1."}))
        self.assertIn("{r2.frequency[1]}", v["notes"][0])


class AutolinkTests(unittest.TestCase):
    def test_off_by_default_on_by_flag_or_per_call(self):
        doc, cat, tools = make()
        ok(tools.call("add_text", {"text": "Bend 1648.23 cm-1."}))
        self.assertEqual(doc.get("p1").text, "Bend 1648.23 cm-1.")
        v = ok(tools.call("add_text", {"text": "Bend 1648.23 cm-1.", "autolink": True}))
        self.assertEqual(doc.get(v["block_id"]).text, "Bend 1648.23 cm⁻¹.")
        self.assertEqual(v["autolinked"], [{"typed": "1648.23 cm-1", "use": "{r2.frequency[1]}"}])
        self.assertEqual(doc.written_text(v["block_id"]), "Bend {r2.frequency[1]}.")
        self.assertEqual(doc.get(v["block_id"]).cites, ["r2"])
        doc, cat, tools = make(autolink=True)
        v = ok(tools.call("add_text", {"text": "Bend 1648.23 cm-1."}))
        self.assertIn("autolinked", v)
        v = ok(tools.call("add_text", {"text": "Bend 1648.23 cm-1.", "autolink": False}))
        self.assertNotIn("autolinked", v)

    def test_it_is_conservative(self):
        doc, cat, tools = make(autolink=True)
        for text in ("About 3830 cm-1.", "Ratio 2.5.", "Count 12.", "Shift -3832.71 cm-1.", "Bend 1648.23 eV.", "About 50%."):
            v = ok(tools.call("add_text", {"text": text}))
            self.assertNotIn("autolinked", v, text)
            self.assertEqual(doc.get(v["block_id"]).text, text)

    def test_a_value_the_data_has_twice_is_left_alone(self):
        items = EvidenceSet([EvidenceItem(1.5, "angstrom", "length", "A", "r1", 1, "data", key="a/x", unit_name="Angstroms"),
                             EvidenceItem(1.5, "angstrom", "length", "B", "r1", 1, "data", key="a/y", unit_name="Angstroms")])
        self.assertEqual(autolink("Bond 1.5 Å.", items), ("Bond 1.5 Å.", []))

    def test_a_typed_unit_with_a_unitless_value_is_left_alone(self):
        items = EvidenceSet([EvidenceItem(0.75, None, None, "X", "r1", None, "data", key="a/x")])
        self.assertEqual(autolink("Weight 0.75 eV.", items)[1], [])


class BasisTests(unittest.TestCase):
    def test_basis_is_stored_validated_and_round_trips(self):
        doc, cat, tools = make()
        self.assertEqual(tools.call("add_text", {"text": "x", "basis": "guess"}).error["code"], "invalid_arguments")
        v = ok(tools.call("add_text", {"text": "Background.", "basis": "background"}))
        self.assertEqual(doc.get(v["block_id"]).basis, "background")
        self.assertEqual(doc.outline()[-1]["basis"], "background")
        again = ReportDocument.from_markdown(doc.to_markdown(), cat)
        self.assertEqual(again.get(v["block_id"]).basis, "background")
        ok(tools.call("edit_text", {"block_id": v["block_id"], "text": "Still background."}))
        self.assertEqual(doc.get(v["block_id"]).basis, "background")           # kept
        ok(tools.call("edit_text", {"block_id": v["block_id"], "text": "Now data.", "basis": "data"}))
        self.assertEqual(doc.get(v["block_id"]).basis, "data")

    def test_documents_without_a_basis_write_no_marker_field(self):
        doc, cat, tools = make()
        ok(tools.call("add_text", {"text": "Plain."}))
        self.assertNotIn("basis", doc.to_markdown())

    def test_grounded_needs_cites_unless_the_text_is_not_about_the_data(self):
        doc, cat, tools = make(policy="grounded")
        self.assertEqual(tools.call("add_text", {"text": "Words."}).error["code"], "needs_citation")
        self.assertEqual(tools.call("add_text", {"text": "Words.", "basis": "data"}).error["code"], "needs_citation")
        ok(tools.call("add_text", {"text": "General words.", "basis": "background"}))
        ok(tools.call("add_text", {"text": "At {=300 K}, as the user said.", "basis": "user_input"}))
        r = tools.call("add_text", {"text": "At 300 K.", "basis": "background"})       # a typed number has no data to match
        self.assertEqual(r.error["code"], "ungrounded")
        self.assertIn("{=300 K}", r.error["hint"])


class CoverageTests(unittest.TestCase):
    def test_counts_placeholders_literals_and_typed_numbers(self):
        doc, cat, tools = make()
        ok(tools.call("add_text", {"text": "Lowest {r2.frequency[1]}, highest {r2.frequency[3]}, at {=300 K}."}))
        ok(tools.call("add_text", {"text": "The stretch is 3832.71 cm-1 and the run was 2.5 hours."}))
        cov = ok(tools.call("compile"))["coverage"]
        self.assertEqual({k: cov[k] for k in ("paragraphs", "placeholders", "literals", "typed", "typed_in_data")},
                         {"paragraphs": 2, "placeholders": 2, "literals": 1, "typed": 2, "typed_in_data": 1})
        self.assertEqual((cov["numbers"], cov["paragraphs_with_typed"]), (5, ["p2"]))
        self.assertEqual(doc.number_coverage(match=False).get("typed_in_data"), None)

    def test_basis_counts(self):
        doc, cat, tools = make()
        ok(tools.call("add_text", {"text": "A.", "basis": "background"}))
        ok(tools.call("add_text", {"text": "B.", "basis": "background"}))
        self.assertEqual(coverage(doc)["basis"], {"background": 2})

    def test_an_empty_report(self):
        doc, cat, tools = bare()
        self.assertEqual(ok(tools.call("compile"))["coverage"]["numbers"], 0)


class InstructionTests(unittest.TestCase):
    def test_the_number_check_is_described_only_under_the_grounded_policy(self):
        cat = toy_catalog(water=FillToy("water"))
        for lvl in (1, 2, 3):
            off = report_toolset(ReportDocument("x", cat), cat, context_level=lvl).instructions
            on = report_toolset(ReportDocument("x", cat), cat, context_level=lvl, policy="grounded").instructions
            self.assertNotIn("This report is checked", off)
            self.assertIn("This report is checked", on)
            self.assertIn("ungrounded", on)

    def test_autolink_and_values_tool_mentions(self):
        cat = toy_catalog(water=FillToy("water"))
        t = report_toolset(ReportDocument("x", cat), cat, autolink=True).instructions
        self.assertIn("rewritten into", t)
        self.assertNotIn("rewritten into", report_toolset(ReportDocument("x", cat), cat).instructions)
        self.assertIn("values(block_id)", report_toolset(ReportDocument("x", cat), cat).instructions)
        self.assertNotIn("values(block_id", report_toolset(ReportDocument("x", cat), cat, exclude_tools=["values"]).instructions)
        self.assertEqual(report_instructions(None, 2), report_instructions(None, 2, values_tool=True))

    def test_the_schema_carries_an_example_and_the_new_fields(self):
        cat = toy_catalog(water=FillToy("water"))
        schema = {t["name"]: t for t in report_toolset(ReportDocument("x", cat), cat).tools()}["add_text"]["inputSchema"]
        props = schema["properties"]
        self.assertIn("{r3.frequency[1]}", props["text"]["examples"][0])
        self.assertIn("{=300 K}", props["text"]["examples"][0])
        self.assertEqual(props["basis"]["enum"], ["data", "background", "user_input"])
        self.assertIn("literals", props)
        self.assertIn("autolink", props)


if __name__ == "__main__":
    unittest.main()

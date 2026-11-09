"""
Server-filled values in report text: {r2.frequency[2]} written with its unit label, text columns, derived values
(opt-in), stored fills, and the ungrounded refusal that shows the matching placeholder.
"""
import unittest

from McUtils.Readouts.Reports import (ReportDocument, report_toolset, fill_text, find_references, unit_shorthand,
                                      ReportOperationError, ReportTemplate, register_report_template)
from ReportFixtures import toy_catalog, ToyResult


class FillToy(ToyResult):
    pass


@register_report_template(FillToy)
class FillToyTemplate(ReportTemplate):
    name = "toy-fill"
    sections = [("Overview", ["summary"]), ("Vibrations", ["frequencies"])]


def ok(result):
    assert result.ok, result.error
    return result.value


def make(**kw):
    cat = toy_catalog(water=FillToy("water"))
    doc = ReportDocument("Fill", cat)
    tools = report_toolset(doc, cat, **kw)
    ok(tools.call("apply_template", {"handle": "water"}))     # h1 r1 | h2 r2 (frequencies: 1648.23, 3832.71, 3943.88)
    assert [b.id for b in doc.blocks] == ["h1", "r1", "h2", "r2"], doc.outline()
    return doc, cat, tools


class UnitShorthandTests(unittest.TestCase):
    def test_labels_follow_the_units_data_names(self):
        self.assertEqual(unit_shorthand("Wavenumbers"), "cm⁻¹")
        self.assertEqual(unit_shorthand("Hartrees"), "Eₕ")
        self.assertEqual(unit_shorthand("Angstroms"), "Å")

    def test_other_spellings_of_the_same_unit(self):
        self.assertEqual(unit_shorthand("cm^-1"), "cm⁻¹")
        self.assertEqual(unit_shorthand("Hartree"), "Eₕ")
        self.assertEqual(unit_shorthand("percent"), "%")

    def test_unknown_units_are_written_as_named(self):
        self.assertEqual(unit_shorthand("furlongs"), "furlongs")
        self.assertIsNone(unit_shorthand(None))


class FillTextTests(unittest.TestCase):
    def setUp(self):
        self.doc, self.cat, self.tools = make()
        self.items = self.doc.evidence(["r1", "r2"])

    def test_references_are_found_only_with_a_block(self):
        self.assertEqual(len(find_references("a {r2.frequency[1]} b {not a ref} c")), 1)
        text, fills = fill_text("plain {braces} stay", self.items)
        self.assertEqual((text, fills), ("plain {braces} stay", []))

    def test_a_value_is_written_with_its_unit_label(self):
        text, fills = fill_text("at {r2.frequency[1]}.", self.items)
        self.assertEqual(text, "at 1648.23 cm⁻¹.")
        f = fills[0]
        self.assertEqual((f.number, f.unit, f.text, f.derived), ("1648.23", "cm⁻¹", "1648.23 cm⁻¹", False))
        self.assertEqual(text[f.span[0]:f.span[1]], "1648.23 cm⁻¹")

    def test_energy_unit_label(self):
        text, _ = fill_text("E = {r1.energy}", self.items)
        self.assertTrue(text.endswith(" Eₕ"), text)

    def test_a_typed_unit_is_swallowed_and_replaced(self):
        for typed in ("cm-1", "cm^-1", "cm⁻¹", "wavenumbers"):
            with self.subTest(typed=typed):
                text, fills = fill_text("at {r2.frequency[1]} " + typed + " here", self.items)
                self.assertEqual(text, "at 1648.23 cm⁻¹ here")
                self.assertEqual(text.count("cm"), 1)
        self.assertEqual(fill_text("at {r2.frequency[1]}cm-1 here", self.items)[0], "at 1648.23 cm⁻¹ here")

    def test_a_mismatched_unit_is_an_error(self):
        for bad in ("{r2.frequency[1]} eV", "{r2.frequency[1]} kcal/mol", "{r2.frequency[1]}%", "{r1.energy} cm-1"):
            with self.subTest(bad=bad):
                with self.assertRaises(ReportOperationError) as cm:
                    fill_text(bad, self.items)
                self.assertEqual(cm.exception.code, "unit_mismatch")

    def test_a_unit_after_a_value_that_has_none_is_an_error(self):
        with self.assertRaises(ReportOperationError) as cm:
            fill_text("{r1.n_modes} cm-1", self.items)
        self.assertEqual(cm.exception.code, "unit_mismatch")
        self.assertEqual(fill_text("{r1.n_modes} modes", self.items)[0], "3 modes")

    def test_a_format_spec_changes_the_number_only(self):
        text, _ = fill_text("{r2.frequency[1]:.0f}", self.items)
        self.assertEqual(text, "1648 cm⁻¹")

    def test_errors(self):
        for bad, code in (("{r2.freq[1]}", "bad_reference"), ("{r2.frequency[9]}", "bad_reference"),
                          ("{r2.frequency}", "bad_reference"), ("{__import__('os')}", None),
                          ("{r2.frequency[1] ** 2}", "bad_reference"), ("{r9.frequency[1]}", "bad_reference")):
            with self.subTest(bad=bad):
                if code is None:
                    self.assertEqual(fill_text(bad, self.items)[1], [])      # no block reference: left alone
                    continue
                with self.assertRaises(ReportOperationError) as cm:
                    fill_text(bad, self.items)
                self.assertEqual(cm.exception.code, code)

    def test_unknown_column_lists_the_choices(self):
        with self.assertRaises(ReportOperationError) as cm:
            fill_text("{r2.freq[1]}", self.items)
        self.assertIn("frequency", cm.exception.info["choices"])
        self.assertIn("mode", cm.exception.info["choices"])


class TextColumnFillTests(unittest.TestCase):
    """Fills also work on string columns: the ToyResult ``mode`` labels."""

    def setUp(self):
        self.doc, self.cat, self.tools = make()
        self.items = self.doc.evidence(["r2"])

    def test_a_label_is_written_as_it_is(self):
        text, fills = fill_text("The {r2.mode[2]} mode is at {r2.frequency[2]}.", self.items)
        self.assertEqual(text, "The sym stretch mode is at 3832.71 cm⁻¹.")
        self.assertEqual([f.kind for f in fills], ["text", "single"])
        self.assertEqual(fills[0].text, "sym stretch")
        self.assertIsNone(fills[0].unit)

    def test_a_unit_typed_after_a_label_is_left_alone(self):
        self.assertEqual(fill_text("{r2.mode[1]} K", self.items)[0], "bend K")

    def test_text_values_are_filled_alone(self):
        for bad in ("{r2.mode[1] + r2.mode[2]}", "{r2.mode}", "{r2.mode[1]:.2f}", "{r2.mode[1] + 1}"):
            with self.subTest(bad=bad):
                with self.assertRaises(ReportOperationError) as cm:
                    fill_text(bad, self.items, allow_derived=True)
                self.assertEqual(cm.exception.code, "bad_reference")

    def test_a_text_fill_is_stored_and_rechecked(self):
        tools = self.tools
        v = ok(tools.call("add_text", {"text": "The {r2.mode[1]} mode is lowest, at {r2.frequency[1]}."}))
        p = self.doc.get(v["block_id"])
        self.assertEqual(p.text, "The bend mode is lowest, at 1648.23 cm⁻¹.")
        self.assertEqual(p.fills[0], {"expr": "r2.mode[1]", "text": "bend"})
        self.assertEqual(p.status, "checked")
        doc2 = ReportDocument.from_markdown(self.doc.to_markdown(), self.cat)
        self.assertTrue(doc2.check_prose(v["block_id"]).ok)

    def test_only_text_fills_leave_nothing_checked(self):
        v = ok(self.tools.call("add_text", {"text": "The first mode is the {r2.mode[1]} mode."}))
        self.assertEqual(self.doc.get(v["block_id"]).status, "no_numbers")


class DerivedValueTests(unittest.TestCase):
    """Computed values are off by default and opt in with allow_derived."""

    def setUp(self):
        self.doc, self.cat, self.tools = make()
        self.items = self.doc.evidence(["r1", "r2"])

    def test_off_by_default(self):
        fill_text("{r2.frequency[1]}", self.items)
        with self.assertRaises(ReportOperationError) as cm:
            fill_text("{mean(r2.frequency[1], r2.frequency[2])}", self.items)
        self.assertEqual(cm.exception.code, "derived_disabled")

    def test_opt_in_values_carry_the_inputs_unit(self):
        text, fills = fill_text("{mean(r2.frequency[2], r2.frequency[3])}, {diff(r2.frequency[3], r2.frequency[2])}, "
                                "{max(r2.frequency)}, {r2.frequency[3] - r2.frequency[2]:.1f}", self.items,
                                allow_derived=True)
        self.assertEqual(text, "3888.30 cm⁻¹, 111.17 cm⁻¹, 3943.88 cm⁻¹, 111.2 cm⁻¹")
        self.assertTrue(all(f.derived for f in fills))

    def test_a_ratio_has_no_unit_and_its_typed_text_is_the_writers(self):
        text, _ = fill_text("{ratio(r2.frequency[3], r2.frequency[2])}", self.items, allow_derived=True)
        self.assertEqual(text, "1.029")

    def test_mixed_units_are_refused(self):
        with self.assertRaises(ReportOperationError) as cm:
            fill_text("{r1.energy + r2.frequency[1]}", self.items, allow_derived=True)
        self.assertEqual(cm.exception.code, "unit_mismatch")

    def test_there_is_no_suggestion_machinery(self):
        import McUtils.Readouts.Reports as R
        import McUtils.Readouts.Reports.Fill as F
        self.assertFalse(hasattr(R, "suggest_derivations") or hasattr(F, "suggest_derivations"))

    def test_the_tools_accept_derived_values_by_default_and_refuse_them_when_off(self):
        doc, cat, tools = make()
        self.assertEqual(ok(tools.call("add_text", {"text": "Mean {mean(r2.frequency[2], r2.frequency[3])}."}))["filled"][0]["derived"], True)
        doc, cat, self.tools = make(allow_derived=False)
        r = self.tools.call("add_text", {"text": "Mean {mean(r2.frequency)}."})
        self.assertEqual(r.error["code"], "derived_disabled")
        self.assertEqual(r.error["retry"], "no")

    def test_the_tools_accept_them_with_the_flag(self):
        doc, cat, tools = make(allow_derived=True)
        v = ok(tools.call("add_text", {"text": "The stretches average {mean(r2.frequency[2], r2.frequency[3])}."}))
        p = doc.get(v["block_id"])
        self.assertEqual(p.text, "The stretches average 3888.30 cm⁻¹.")
        self.assertEqual(p.fills, [{"expr": "mean(r2.frequency[2], r2.frequency[3])", "text": "3888.30 cm⁻¹", "style": "unicode"}])
        self.assertTrue(v["filled"][0]["derived"])
        self.assertTrue(doc.check_prose(v["block_id"]).ok)

    def test_captions_never_take_derived_values(self):
        doc, cat, tools = make(allow_derived=True)
        self.assertEqual(tools.call("set_caption", {"block_id": "r2", "text": "{mean(r2.frequency)}"}).error["code"],
                         "derived_disabled")


class FillToolTests(unittest.TestCase):
    def test_add_text_fills_cites_and_records(self):
        doc, cat, tools = make()
        v = ok(tools.call("add_text", {"text": "The lowest mode is at {r2.frequency[1]}."}))
        p = doc.get(v["block_id"])
        self.assertEqual(p.text, "The lowest mode is at 1648.23 cm⁻¹.")
        self.assertEqual(p.cites, ["r2"], "the referenced block is cited automatically")
        self.assertEqual(p.status, "checked")
        self.assertEqual(v["filled"][0]["value"], "1648.23 cm⁻¹")
        self.assertFalse(v["filled"][0]["derived"])
        self.assertEqual(p.fills, [{"expr": "r2.frequency[1]", "text": "1648.23 cm⁻¹", "style": "unicode"}])

    def test_a_typed_unit_after_a_placeholder_is_corrected_not_doubled(self):
        doc, cat, tools = make()
        v = ok(tools.call("add_text", {"text": "At {r2.frequency[1]} cm-1."}))
        self.assertEqual(doc.get(v["block_id"]).text, "At 1648.23 cm⁻¹.")

    def test_a_wrong_unit_after_a_placeholder_is_refused(self):
        doc, cat, tools = make()
        r = tools.call("add_text", {"text": "At {r2.frequency[1]} eV."})
        self.assertEqual((r.ok, r.error["code"], r.error["retry"]), (False, "unit_mismatch", "after_fix"))
        self.assertEqual(len(doc.blocks), 4, "nothing was written")

    def test_fills_survive_a_reload_and_are_rechecked(self):
        doc, cat, tools = make()
        ok(tools.call("add_text", {"text": "Lowest {r2.frequency[1]}, highest {r2.frequency[3]}."}))
        doc2 = ReportDocument.from_markdown(doc.to_markdown(), cat)
        self.assertEqual(doc2.get("p1").fills, doc.get("p1").fills)
        self.assertTrue(doc2.check_prose("p1").ok)
        doc2.get("p1").fills[0]["text"] = "3000.00 cm⁻¹"
        self.assertFalse(doc2.check_prose("p1").ok, "a recorded value that no longer follows is reported")

    def test_captions_take_only_their_own_values(self):
        doc, cat, tools = make()
        ok(tools.call("set_caption", {"block_id": "r2", "text": "Lowest mode at {r2.frequency[1]}."}))
        self.assertEqual(doc.get("r2").caption, "Lowest mode at 1648.23 cm⁻¹.")
        self.assertEqual(tools.call("set_caption", {"block_id": "r2", "text": "{r1.energy}"}).error["code"],
                         "bad_reference")

    def test_edit_text_refills(self):
        doc, cat, tools = make()
        ok(tools.call("add_text", {"text": "Lowest {r2.frequency[1]}."}))
        ok(tools.call("edit_text", {"block_id": "p1", "text": "Highest {r2.frequency[3]}."}))
        self.assertEqual(doc.get("p1").text, "Highest 3943.88 cm⁻¹.")
        self.assertEqual(doc.get("p1").fills[0]["expr"], "r2.frequency[3]")


class LiteralNumberTests(unittest.TestCase):
    """Under the grounded policy typed numbers are checked, unit-aware, and the refusal shows the placeholder."""

    def setUp(self):
        self.doc, self.cat, self.tools = make(policy="grounded")

    def test_a_correct_literal_is_accepted_and_the_receipt_shows_the_placeholder(self):
        v = ok(self.tools.call("add_text", {"text": "The bend is at 1648.23 cm-1.", "cites": ["r2"]}))
        self.assertEqual(v["numbers"][0]["use"], "{r2.frequency[1]}")
        self.assertIn("r2 frequency row 1", v["numbers"][0]["matched"])

    def test_an_unknown_number_is_refused_with_the_closest_placeholder(self):
        r = self.tools.call("add_text", {"text": "The bend is at 1650.5 cm-1.", "cites": ["r2"]})
        self.assertEqual(r.error["code"], "ungrounded")
        self.assertEqual(r.error["unmatched"], ["1650.5"])
        self.assertTrue(r.error["placeholders"]["1650.5"][0].startswith("{r2.frequency[1]}"))
        self.assertIn("{r2.frequency[1]}", r.error["detail"])
        self.assertTrue(any(v.startswith("{r2.frequency[1]} = 1648.23") for v in r.error["values"]))
        self.assertNotIn("try", r.error)
        self.assertEqual(r.error["retry"], "once")

    def test_a_right_number_in_the_wrong_unit_names_the_placeholder_that_matches(self):
        r = self.tools.call("add_text", {"text": "The bend is at 1648.23 eV.", "cites": ["r2"]})
        self.assertEqual(r.error["code"], "ungrounded")
        self.assertTrue(r.error["placeholders"]["1648.23"][0].startswith("{r2.frequency[1]}"))
        self.assertIn("matching placeholder", r.error["detail"])

    def test_the_hint_points_at_placeholders(self):
        doc, cat, self.tools = make(policy="grounded", allow_derived=False)
        r = self.tools.call("add_text", {"text": "At 1650.5 cm-1.", "cites": ["r2"]})
        self.assertIn("placeholder", r.error["hint"])
        self.assertNotIn("mean", r.error["hint"])

    def test_the_hint_mentions_expressions_only_when_derived_is_on(self):
        doc, cat, tools = make(allow_derived=True, policy="grounded")
        r = tools.call("add_text", {"text": "At 1650.5 cm-1.", "cites": ["r2"]})
        self.assertIn("mean(", r.error["hint"])


if __name__ == "__main__":
    unittest.main()

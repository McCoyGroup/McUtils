
import os as _test_os
import unittest as _test_unittest
_RUN_EXTRAS = _test_os.environ.get("MCUTILS_TEST_EXTRAS") == "1"

import json
import os
import re
import tempfile
import unittest

from McUtils.JobDrivers import ScriptedClient, DecisionRunner, Ledger, Budget
from McUtils.Readouts.Reports import (ReportHarness, ReportLimits, ReportDocument, ReportRenderer, ReportTemplate,
                                      register_report_template, find_report_template, WritingPolicy, UNCHECKED_NOTE)
from McUtils.Readouts.Reports import Templates
from ReportFixtures import ToyResult, toy_catalog


def stage_of(schema):
    props = schema.get("properties", {})
    for name in ("sections", "caption", "paragraphs", "summary"):
        if name in props:
            return {"sections": "outline", "caption": "caption", "paragraphs": "section_text",
                    "summary": "summary"}[name]
    return "select_content"


class Script:
    """A scripted model that answers by stage. ``over[stage]`` is a list of answers consumed in order for that stage
    (after it runs out, the default answer is used) or a callable ``(messages, schema, n) -> answer``."""

    def __init__(self, pick=2, **over):
        self.pick, self.over, self.count, self.client = pick, over, {}, None

    def default(self, stage, messages, schema):
        if stage == "select_content":
            return {h: p["items"]["enum"][:self.pick] for h, p in schema["properties"].items()}
        if stage == "outline":
            ev = messages[1]["content"]
            groups = {}
            for m in re.finditer(r"^(i\d+): (\w+)\.", ev, re.M):
                groups.setdefault(m.group(2), []).append(m.group(1))
            return {"sections": [{"heading": h.title(), "items": ids} for h, ids in groups.items()]}
        if stage == "caption":
            return {"caption": "A caption for this block."}
        if stage == "section_text":
            return {"paragraphs": ["An introduction to this section."]}
        return {"summary": "A short summary of the report."}

    def __call__(self, messages, schema):
        stage = stage_of(schema)
        n = self.count[stage] = self.count.get(stage, 0) + 1
        ov = self.over.get(stage)
        if callable(ov):
            return ov(messages, schema, n)
        if ov is not None and n <= len(ov):
            return ov[n - 1]
        return self.default(stage, messages, schema)

    def stages(self):
        return dict(self.count)


def harness(script=None, catalog=None, policy="grounded", limits=None, template=None, ledger=None, budget=None,
            large=None):
    script = script or Script()
    client = ScriptedClient(script)
    clients = {"small": client}
    if large is not None:
        clients["large"] = large
    runner = DecisionRunner(clients, budget=budget, ledger=ledger, policy=policy)
    h = ReportHarness(catalog or toy_catalog(), runner, policy=policy, limits=limits, template=template)
    return h, client, script


def three_sources():
    return toy_catalog(a=ToyResult("a"), b=ToyResult("b", freqs=(1500.5, 3700.25, 3800.0)),
                       c=ToyResult("c", energy=-1.5))


class FixedTemplate(ReportTemplate):
    name = "toy-fixed"
    sections = [("Overview", ["summary"]), ("Vibrations", ["frequencies"])]

    def caption_for(self, handle, section, source):
        return {"summary": "Energy and size.", "frequencies": "Harmonic frequencies."}.get(section)


class ComposeCallCountTests(unittest.TestCase):
    def test_grounded_call_count(self):
        h, client, script = harness()
        res = h.compose("Toy report")
        doc = res.doc
        blocks = [b for b in doc.blocks if b.kind == "readout"]
        sections = [b for b in doc.blocks if b.kind == "heading"]
        self.assertEqual((len(blocks), len(sections)), (2, 1))
        self.assertEqual(res.calls, 2 + len(blocks) + len(sections) + 1)
        self.assertEqual(len(client.calls), res.calls)
        self.assertEqual(script.stages(), {"select_content": 1, "outline": 1, "caption": 2, "section_text": 1,
                                           "summary": 1})
        self.assertEqual(len(res.records), 6)
        self.assertEqual({r.outcome for r in res.records}, {"applied"})

    def test_grounded_call_count_three_sources(self):
        h, client, _ = harness(catalog=three_sources())
        res = h.compose("Three sources")
        n_blocks = sum(b.kind == "readout" for b in res.doc.blocks)
        n_sections = sum(b.kind == "heading" for b in res.doc.blocks)
        self.assertEqual((n_blocks, n_sections), (6, 3))
        self.assertEqual(res.calls, 2 + 6 + 3 + 1)
        self.assertEqual(sorted({b.handle for b in res.doc.blocks if b.kind == "readout"}), ["a", "b", "c"])

    def test_structure_only_is_two_calls(self):
        h, client, script = harness(policy="structure_only")
        res = h.compose("Structure only")
        self.assertEqual(res.calls, 2)
        self.assertEqual(script.stages(), {"select_content": 1, "outline": 1})
        self.assertEqual([b.kind for b in res.doc.blocks], ["heading", "readout", "readout"])
        self.assertTrue(all(b.caption is None for b in res.doc.blocks if b.kind == "readout"))
        self.assertEqual(res.doc.meta["writing_policy"], "structure_only")

    def test_fixed_single_source_template_structure_only_is_zero_calls(self):
        h, client, _ = harness(policy="structure_only", template=FixedTemplate())
        res = h.compose("Fixed")
        self.assertEqual(res.calls, 0)
        self.assertEqual(len(client.calls), 0)
        self.assertEqual(len(res.records), 0)
        doc = res.doc
        self.assertEqual([(b.kind, getattr(b, "text", None) or b.include) for b in doc.blocks],
                         [("heading", "Overview"), ("readout", ["summary"]), ("heading", "Vibrations"),
                          ("readout", ["frequencies"])])
        caps = {b.id: (b.caption, b.caption_status) for b in doc.blocks if b.kind == "readout"}
        self.assertEqual(sorted(caps.values()), [("Energy and size.", "template"), ("Harmonic frequencies.", "template")])
        self.assertEqual(doc.meta["template"], "toy-fixed")

    def test_fixed_template_can_name_a_part_of_a_section(self):
        from McUtils.Readouts import (ReadoutAdapter, readout_section, register_readout, ReadoutSection, ReadoutText)

        class Sub(ReadoutAdapter):
            @readout_section(description="First part.")
            def readout_first(self, ctx):
                return ReadoutText("first part")

            @readout_section(description="Second part.")
            def readout_second(self, ctx):
                return ReadoutText("second part")

        class Nested:
            pass

        @register_readout(Nested)
        class NestedReadout(ReadoutAdapter):
            readout_id = "nested-toy"

            @readout_section("parts", description="Two parts.")
            def readout_parts(self, ctx, include=None, exclude=None, **opts):
                return ReadoutSection(*Sub(self.obj).get_readout_sections(include=include, exclude=exclude,
                                                                           ctx=ctx, **opts))

        class Dotted(ReportTemplate):
            name = "nested-dotted"
            sections = [("Parts", ["parts.second"])]

            def caption_for(self, handle, section, source):
                return "A part."

        from McUtils.Readouts.Reports import SourceCatalog
        cat = SourceCatalog()
        cat.add("n", Nested(), title="Nested")
        h, client, _ = harness(catalog=cat, policy="structure_only", template=Dotted())
        res = h.compose("Dotted")
        self.assertEqual(res.calls, 0)
        blocks = [b for b in res.doc.blocks if b.kind == "readout"]
        self.assertEqual([b.include for b in blocks], [["parts.second"]])
        self.assertEqual(blocks[0].caption, "A part.")
        self.assertIn("second part", res.doc.to_markdown() + cat.peek("n", "parts.second", max_chars=500))

    def test_fixed_template_with_grounded_policy_writes_text_only(self):
        h, client, script = harness(template=FixedTemplate())
        res = h.compose("Fixed grounded")
        self.assertEqual(script.stages(), {"caption": 2, "section_text": 2, "summary": 1})
        self.assertEqual(res.calls, 2 + 2 + 1)

    def test_template_flags_switch_stages_off(self):
        class NoProse(FixedTemplate):
            captions = True
            section_text = False
            summary = False
        h, _, script = harness(template=NoProse())
        h.compose("No prose")
        self.assertEqual(script.stages(), {"caption": 2})

    def test_no_prose_at_all_costs_zero_calls(self):
        class Silent(FixedTemplate):
            captions = section_text = summary = False
        h, client, _ = harness(template=Silent())
        res = h.compose("Silent")
        self.assertEqual((res.calls, len(client.calls)), (0, 0))
        self.assertEqual(sum(b.kind == "readout" for b in res.doc.blocks), 2)

    def test_unchecked_policy(self):
        h, _, script = harness(policy="unchecked")
        res = h.compose("Unchecked")
        doc = res.doc
        self.assertEqual(script.stages(), {"select_content": 1, "outline": 1, "caption": 2, "section_text": 1,
                                           "summary": 1})
        self.assertEqual(doc.blocks[0].kind, "callout")
        self.assertEqual(doc.blocks[0].text, UNCHECKED_NOTE)
        self.assertEqual(doc.blocks[1].role, "summary")
        self.assertTrue(all(b.caption_status == "unchecked" for b in doc.blocks if b.kind == "readout"))
        self.assertTrue(all(b.status == "unchecked" for b in doc.blocks if b.kind == "prose"))

    def test_grounded_statuses_and_layout(self):
        h, _, _ = harness()
        doc = h.compose("Grounded").doc
        kinds = [b.kind for b in doc.blocks]
        self.assertEqual(kinds, ["prose", "heading", "prose", "readout", "readout"])
        self.assertEqual((doc.blocks[0].role, doc.blocks[0].status), ("summary", "checked"))
        section_text = doc.blocks[2]
        self.assertEqual(section_text.cites, ["r1", "r2"])
        self.assertTrue(all(b.caption_status == "checked" for b in doc.blocks if b.kind == "readout"))
        self.assertEqual(doc.meta["prompt_version"], ReportHarness.PROMPT_VERSION)
        self.assertEqual(doc.validate(), [])


class StageFailureTests(unittest.TestCase):
    def test_grounding_failure_in_caption_then_revision_passes(self):
        bad = {"caption": "The bend is near 1650 cm-1."}
        good = {"caption": "The bend is at 1648.2 cm-1."}
        h, client, script = harness(Script(select_content=[{"water": ["frequencies"]}], caption=[bad, good]))
        res = h.compose("Revision")
        caps = [b.caption for b in res.doc.blocks if b.kind == "readout"]
        self.assertEqual(caps, ["The bend is at 1648.2 cm-1."])
        cap_calls = [c for c in client.calls if stage_of(c[1]) == "caption"]
        self.assertEqual(len(cap_calls), 2)          # bad, then good
        revised = cap_calls[1][0]
        self.assertEqual([m["role"] for m in revised], ["system", "user", "assistant", "user"])
        self.assertIn("'1650'", revised[-1]["content"])
        self.assertIn("does not appear in the evidence", revised[-1]["content"])
        cap_records = [r for r in res.records if r.decision == "caption"]
        self.assertEqual([r.outcome for r in cap_records], ["applied"])
        self.assertEqual(len(cap_records[0].attempts), 2)
        self.assertTrue(cap_records[0].attempts[0]["errors"])
        self.assertEqual(cap_records[0].attempts[1]["errors"], [])

    def test_grounding_failure_twice_drops_the_caption(self):
        bad = {"caption": "The bend is near 1650 cm-1."}
        h, client, _ = harness(Script(select_content=[{"water": ["frequencies", "summary"]}] , caption=[bad, bad]))
        res = h.compose("Dropped")
        cap_records = [r for r in res.records if r.decision == "caption"]
        by_block = {r.stage: r for r in cap_records}
        self.assertEqual(len(cap_records), 2)
        dropped = [r for r in cap_records if r.outcome == "defaulted"]
        self.assertEqual(len(dropped), 1)
        self.assertEqual(dropped[0].source, "default")
        self.assertIn("1650", dropped[0].reason)
        blocks = [b for b in res.doc.blocks if b.kind == "readout"]
        self.assertEqual(sorted(b.caption is None for b in blocks), [False, True])
        self.assertEqual(dropped[0].stage, f"caption:{[b.id for b in blocks if b.caption is None][0]}")
        self.assertEqual(res.doc.validate(), [])

    def test_unchecked_policy_accepts_ungrounded_numbers(self):
        h, _, _ = harness(Script(caption=[{"caption": "The bend is near 1650 cm-1."}]), policy="unchecked")
        doc = h.compose("Unchecked").doc
        self.assertEqual([b.caption for b in doc.blocks if b.kind == "readout"][0], "The bend is near 1650 cm-1.")

    def test_section_text_and_summary_are_grounded(self):
        ungrounded = {"paragraphs": ["The stretches are near 4000 cm-1."]}
        h, client, _ = harness(Script(section_text=[ungrounded, ungrounded],
                                      summary=[{"summary": "Energy is -99.9 Eh."}, {"summary": "Energy is −76.02665 Eh."}]))
        res = h.compose("Grounded prose")
        self.assertEqual([b.kind for b in res.doc.blocks], ["prose", "heading", "readout", "readout"])
        self.assertEqual(res.doc.blocks[0].text, "Energy is −76.02665 Eh.")
        outcomes = {r.decision: r.outcome for r in res.records if r.decision in ("section_text", "summary")}
        self.assertEqual(outcomes, {"section_text": "defaulted", "summary": "applied"})

    def test_summary_word_limit(self):
        h, client, _ = harness(Script(summary=[{"summary": " ".join(["w"] * 15)}]),
                               limits=ReportLimits(summary_words=10))
        res = h.compose("Wordy")
        rec = [r for r in res.records if r.decision == "summary"][0]
        self.assertEqual(len(rec.attempts), 2)
        self.assertIn("15 words", rec.attempts[0]["errors"][0])
        self.assertEqual(res.doc.blocks[0].text, "A short summary of the report.")

    def test_summary_sees_only_checked_text(self):
        h, client, _ = harness(Script(caption=[{"caption": "The bend is near 1650 cm-1."}] * 2))
        res = h.compose("Checked text only")
        summary_ev = [r for r in res.records if r.decision == "summary"][0].evidence_text
        self.assertNotIn("1650", summary_ev)
        self.assertIn("A caption for this block.", summary_ev)

    def test_text_the_document_would_refuse_is_revised(self):
        h, client, _ = harness(Script(section_text=[{"paragraphs": ["A line\n# not a heading"]}]))
        res = h.compose("Refused text")
        rec = [r for r in res.records if r.decision == "section_text"][0]
        self.assertIn("starting with '#'", rec.attempts[0]["errors"][0])
        self.assertEqual(rec.outcome, "applied")

    def test_escalation_to_large_tier(self):
        large = ScriptedClient(lambda messages, schema: {"caption": "From the large model."}, name="large-model")
        bad = {"caption": "The bend is near 1650 cm-1."}
        h, client, _ = harness(Script(caption=[bad, bad]), large=large)
        res = h.compose("Escalate")
        rec = [r for r in res.records if r.decision == "caption"][0]
        self.assertEqual((rec.outcome, rec.escalated_to, rec.model), ("escalated", "large", "large-model"))
        self.assertEqual(len(large.calls), 1)
        self.assertEqual([b.caption for b in res.doc.blocks if b.kind == "readout"][0], "From the large model.")

    def test_invalid_select_answers_fall_back_to_defaults(self):
        h, _, script = harness(Script(select_content=[{"water": []}, {"water": ["nope"]}]))
        res = h.compose("Default selection")
        rec = res.records[0]
        self.assertEqual((rec.decision, rec.outcome), ("select_content", "defaulted"))
        included = [b.include for b in res.doc.blocks if b.kind == "readout"]
        self.assertEqual(included, [["summary"], ["frequencies"]])      # the source's default=True sections

    def test_select_respects_max_blocks(self):
        first = {"a": ["summary", "frequencies"], "b": ["summary"], "c": []}          # 3 in total, one handle each <= 2
        second = {"a": ["summary"], "b": ["frequencies"], "c": []}
        h, _, _ = harness(Script(select_content=[first, second]), catalog=three_sources(),
                          limits=ReportLimits(max_blocks=2))
        res = h.compose("Too many")
        rec = res.records[0]
        self.assertEqual(rec.outcome, "applied")
        self.assertIn("3 sections chosen; at most 2", rec.attempts[0]["errors"][0])
        self.assertEqual(sum(b.kind == "readout" for b in res.doc.blocks), 2)

    def test_select_needs_at_least_one_section(self):
        h, _, _ = harness(Script(select_content=[{"a": [], "b": [], "c": []}]), catalog=three_sources())
        rec = h.compose("None chosen").records[0]
        self.assertIn("at least one section", rec.attempts[0]["errors"][0])
        self.assertEqual(rec.outcome, "applied")

    def test_outline_errors_are_listed(self):
        def outline(messages, schema, n):
            if n == 1:
                return {"sections": [{"heading": "A", "items": ["i1"]}, {"heading": "a", "items": ["i1"]}]}
            return {"sections": [{"heading": "Structure", "items": ["i1"]}, {"heading": "Vibrations", "items": ["i2"]}]}
        h, client, _ = harness(Script(outline=outline))
        res = h.compose("Outline")
        rec = [r for r in res.records if r.decision == "outline"][0]
        errors = " ".join(rec.attempts[0]["errors"])
        self.assertIn("used twice", errors)
        self.assertIn("item i2 is not used", errors)
        self.assertIn("item i1 is used 2 times", errors)
        self.assertEqual([b.text for b in res.doc.blocks if b.kind == "heading"], ["Structure", "Vibrations"])

    def test_default_outline_is_one_section_per_source(self):
        h, _, _ = harness(Script(outline=[{"sections": []}, {"sections": []}]), catalog=three_sources())
        res = h.compose("Default outline")
        self.assertEqual([b.text for b in res.doc.blocks if b.kind == "heading"],
                         ["Source a", "Source b", "Source c"])

    def test_budget_exhaustion_degrades_to_a_structure_only_report(self):
        h, client, _ = harness(budget=Budget(max_calls=2))
        res = h.compose("Over budget")
        self.assertEqual(len(client.calls), 2)
        outcomes = [r.outcome for r in res.records]
        self.assertEqual(outcomes[:2], ["applied", "applied"])
        self.assertTrue(all(o == "defaulted" for o in outcomes[2:]))
        self.assertEqual([b.kind for b in res.doc.blocks], ["heading", "readout", "readout"])
        self.assertEqual(res.doc.validate(), [])


class EvidenceCapTests(unittest.TestCase):
    CAPS = ReportLimits().evidence_tokens

    def check_caps(self, res, caps=None):
        caps = caps or self.CAPS
        seen = set()
        for r in res.records:
            tokens = len(r.evidence_text) // 4
            self.assertLessEqual(tokens, caps[r.decision], (r.decision, r.stage, tokens))
            seen.add(r.decision)
        return seen

    def test_toy_and_three_source_catalogs(self):
        for cat in (toy_catalog(), three_sources()):
            with self.subTest(sources=len(cat)):
                h, _, _ = harness(catalog=cat)
                seen = self.check_caps(h.compose("Caps"))
                self.assertEqual(seen, {"select_content", "outline", "caption", "section_text", "summary"})

    def test_tight_caps_are_still_respected(self):
        caps = {"select_content": 30, "outline": 20, "caption": 40, "section_text": 60, "summary": 40}
        h, _, _ = harness(catalog=three_sources(), limits=ReportLimits(evidence_tokens=caps))
        self.check_caps(h.compose("Tight"), caps)

    def test_figure_caption_evidence_says_no_numbers(self):
        pick = lambda messages, schema, n: {"water": ["picture"]}
        h, _, _ = harness(Script(select_content=pick))
        res = h.compose("Figure")
        ev = [r.evidence_text for r in res.records if r.decision == "caption"][0]
        self.assertIn("Block: water.picture (figure)", ev)
        self.assertIn("This block is a figure without numeric text; describe what it shows, do not state numbers.", ev)

    def test_select_evidence_lists_available_sections_only(self):
        h, _, _ = harness()
        res = h.compose("Menu")
        ev = res.records[0].evidence_text
        self.assertIn("water (ToyResult): Source water", ev)
        self.assertIn("- frequencies [table]: Vibrational frequencies in cm-1.", ev)
        self.assertNotIn("missing", ev)


class ReplayAndRenderTests(unittest.TestCase):
    def test_cache_makes_a_second_compose_free_and_identical(self):
        h, client, _ = harness()
        first = h.compose("Cached")
        n = len(client.calls)
        second = h.compose("Cached")
        self.assertEqual(len(client.calls), n)
        self.assertEqual(second.calls, 0)
        self.assertEqual({r.source for r in second.records}, {"cache"})
        self.assertEqual(first.doc.to_markdown(), second.doc.to_markdown())

    def test_ledger_file_has_one_line_per_decision(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "ledger.jsonl")
            h, _, _ = harness(ledger=Ledger(path))
            res = h.compose("Ledger")
            rows = [json.loads(l) for l in open(path).read().strip().split("\n")]
            self.assertEqual(len(rows), len(res.records))
            self.assertEqual({r["policy"] for r in rows}, {"grounded"})
            self.assertTrue(all(r["evidence_text"] and r["prompt_version"] == "report-v1" for r in rows))
            self.assertTrue(any(r["stage"].startswith("caption:r") for r in rows))
            self.assertEqual(res.doc.meta["ledger"], path)

    def test_composed_document_round_trips_through_markdown(self):
        h, _, _ = harness(catalog=three_sources())
        res = h.compose("Round trip")
        md = res.doc.to_markdown()
        again = ReportDocument.from_markdown(md, h.catalog)
        self.assertEqual(again.to_markdown(), md)
        self.assertEqual(again.validate(), [])
        self.assertEqual(again.meta["writing_policy"], "grounded")

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_composed_document_renders(self):
        h, _, _ = harness()
        res = h.compose("Render me")
        with tempfile.TemporaryDirectory() as d:
            out = ReportRenderer(h.catalog, timeout=120).render(res.doc, os.path.join(d, "r"), formats=("html",))
            self.assertTrue(out.ok, out.problems)
            html = open(out.paths["html"], encoding="utf-8").read()
        self.assertIn("A short summary of the report.", html)
        self.assertIn("A caption for this block.", html)
        self.assertIn("1648.2", html)

    def test_policy_enum_and_bad_policy(self):
        h, _, _ = harness(policy=WritingPolicy.STRUCTURE_ONLY)
        self.assertEqual(h.compose("Enum").calls, 2)
        with self.assertRaises(ValueError):
            ReportHarness(toy_catalog(), DecisionRunner({}), policy="bogus")


class TemplateRegistryTests(unittest.TestCase):
    def test_generic_by_default(self):
        t = find_report_template(toy_catalog().get("water"))
        self.assertEqual((type(t), t.name, t.is_fixed), (ReportTemplate, "generic", False))

    def test_registered_template_by_class_and_applies_to(self):
        class T(FixedTemplate):
            def applies_to(self, source):
                return source.obj.name != "skip"
        saved = dict(Templates._TEMPLATES)
        try:
            register_report_template(ToyResult, T)
            self.assertIsInstance(find_report_template(toy_catalog().get("water")), T)
            self.assertEqual(find_report_template(toy_catalog(x=ToyResult("skip")).get("x")).name, "generic")
        finally:
            Templates._TEMPLATES.clear()
            Templates._TEMPLATES.update(saved)

    def test_decorator_form_and_string_target(self):
        saved = dict(Templates._TEMPLATES)
        try:
            @register_report_template(ToyResult)
            class D(FixedTemplate):
                name = "decorated"
            self.assertEqual(find_report_template(toy_catalog().get("water")).name, "decorated")
            register_report_template(f"{ToyResult.__module__}.{ToyResult.__qualname__}", FixedTemplate)
            self.assertEqual(find_report_template(toy_catalog().get("water")).name, "toy-fixed")
        finally:
            Templates._TEMPLATES.clear()
            Templates._TEMPLATES.update(saved)

    def test_interface_attribute(self):
        src = toy_catalog().get("water")
        iface_cls = type(src.interface())
        iface_cls.report_template = FixedTemplate
        try:
            self.assertEqual(find_report_template(src).name, "toy-fixed")
        finally:
            del iface_cls.report_template
        self.assertIsNone(__import__("McUtils.Readouts", fromlist=["ReadoutInterface"]).ReadoutInterface.report_template)

    def test_registered_template_drives_compose(self):
        saved = dict(Templates._TEMPLATES)
        try:
            register_report_template(ToyResult, FixedTemplate)
            h, client, _ = harness(policy="structure_only")
            self.assertEqual(h.compose("By registry").calls, 0)
        finally:
            Templates._TEMPLATES.clear()
            Templates._TEMPLATES.update(saved)


if __name__ == "__main__":
    unittest.main()

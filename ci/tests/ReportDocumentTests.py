"""The report document model: operations and their errors, the Markdown round trip, and the source catalog."""

import json
import unittest

from McUtils.Readouts.Reports import (ReportDocument, ReportOperationError, SourceCatalog, ReportSourceError,
                                      Heading, ReadoutBlock, Prose, RawMarkdown, source_digest,
                                      resolve_readout_interface)
from McUtils.Readouts import Readout

from ReportFixtures import ToyResult, toy_catalog


class CatalogTests(unittest.TestCase):
    def test_handles_and_errors(self):
        cat = toy_catalog(water=ToyResult("water"))
        self.assertEqual(cat.handles(), ["water"])
        self.assertIn("water", cat)
        self.assertEqual(len(cat), 1)
        with self.assertRaises(ReportSourceError):
            cat.add("water", ToyResult())          # duplicate
        for bad in ("Water", "1water", "has space", "", "x" * 41):
            with self.assertRaises(ReportSourceError, msg=bad):
                cat.add(bad, ToyResult())
        with self.assertRaises(ReportSourceError):
            cat.get("nope")

    def test_describe_lists_sections_with_kinds(self):
        d = toy_catalog().describe("water")
        rows = {r["name"]: r for r in d["sections"]}
        self.assertEqual(list(rows), ["summary", "frequencies", "picture", "missing"])
        self.assertEqual(rows["summary"]["kind"], "fields")
        self.assertEqual(rows["frequencies"]["kind"], "table")
        self.assertEqual(rows["picture"]["kind"], "figure")
        self.assertEqual(rows["missing"]["kind"], "unknown")
        self.assertFalse(rows["missing"]["available"])
        self.assertIn("reason", rows["missing"])
        self.assertEqual(rows["summary"]["description"], "Energy and size of the system.")
        self.assertTrue(rows["summary"]["default"])
        self.assertFalse(rows["picture"]["default"])
        self.assertTrue(d["type"].endswith("ToyResult"))

    def test_peek_is_truncated_at_a_line(self):
        cat = toy_catalog()
        full = cat.peek("water", "frequencies", max_chars=5000)
        self.assertIn("1648.23", full)
        self.assertNotIn("truncated", full)
        short = cat.peek("water", "frequencies", max_chars=80)
        self.assertTrue(short.endswith("[... truncated]"))
        body = short[:-len("\n[... truncated]")]
        self.assertTrue(full.startswith(body))
        self.assertIn(body, full.split("\n")[0] + "\n" + "\n".join(full.split("\n")[1:]))

    def test_load_checks_the_digest(self):
        cat = toy_catalog()
        src = cat.get("water")
        self.assertIs(cat.load("water"), src.obj)
        self.assertIs(cat.load("water", digest=src.digest), src.obj)
        with self.assertRaises(ReportSourceError) as cm:
            cat.load("water", digest="0" * 16)
        self.assertIn(src.digest, str(cm.exception))
        self.assertIn("0" * 16, str(cm.exception))
        self.assertIs(cat.namespace()["report_source"]("water"), src.obj)

    def test_digest_is_stable_and_tracks_the_data(self):
        self.assertEqual(source_digest(ToyResult()), source_digest(ToyResult()))
        self.assertNotEqual(source_digest(ToyResult()), source_digest(ToyResult(energy=-75.0)))
        self.assertEqual(len(source_digest(ToyResult())), 16)

        class Custom:
            def __report_digest__(self):
                return "abcdef0123456789ffff"
        self.assertEqual(source_digest(Custom()), "abcdef0123456789")

    def test_record_sources_have_one_pseudo_section(self):
        cat = SourceCatalog()
        cat.add("rec", {"energy": -76.0, "n": 3})
        rows = cat.get("rec").sections()
        self.assertEqual([r["name"] for r in rows], ["record"])
        self.assertEqual(rows[0]["kind"] if "kind" in rows[0] else cat.get("rec").section_kind("record"), "fields")
        self.assertIsInstance(cat.get("rec").readout(include=["record"]), Readout)
        self.assertIn("energy", cat.peek("rec", "record"))
        doc = ReportDocument("Records", cat)
        doc.add_readout("rec")
        doc.add_readout("rec", include=["record"])
        self.assertEqual([b.include for b in doc.blocks], [None, None])   # the marker must not carry a bogus include
        with self.assertRaises(ReportOperationError) as cm:
            doc.add_readout("rec", include=["contents"])
        self.assertEqual(cm.exception.code, "unknown_section")

    def test_reason_is_only_reported_for_unavailable_sections(self):
        from ReportFixtures import ReasonQuirkResult
        cat = SourceCatalog()
        cat.add("q", ReasonQuirkResult())
        rows = {r["name"]: r for r in cat.describe("q")["sections"]}
        self.assertTrue(rows["noted"]["available"])
        self.assertNotIn("reason", rows["noted"])
        self.assertFalse(rows["missing"]["available"])
        self.assertIn("reason", rows["missing"])

    def test_interface_resolution_order(self):
        class WithGetter:
            def get_readout_interface(self):
                return "getter"
        self.assertEqual(resolve_readout_interface(WithGetter()), "getter")
        iface = resolve_readout_interface(ToyResult())
        self.assertTrue(hasattr(iface, "list_readout_sections"))


def code_of(call):
    try:
        call()
    except ReportOperationError as e:
        return e.code
    raise AssertionError("no ReportOperationError")


class OperationTests(unittest.TestCase):
    def setUp(self):
        self.cat = toy_catalog()
        self.doc = ReportDocument("Water", self.cat)

    def test_every_operation(self):
        d = self.doc
        h = d.add_heading("Structure")
        self.assertEqual((h.ok, h.block_id), (True, "h1"))
        r = d.add_readout("water", include=["summary"], caption="The energy.")
        self.assertEqual(r.block_id, "r1")
        p = d.add_text("The energy is -76.0267.", cites=["r1"], status="grounded")
        self.assertEqual(p.block_id, "p1")
        c = d.add_callout("Check the basis set.", kind="flag")
        self.assertEqual(c.block_id, "c1")
        d.set_caption("r1", "A better caption.", status="template")
        self.assertEqual((d.get("r1").caption, d.get("r1").caption_status), ("A better caption.", "template"))
        d.edit_text("p1", "Revised text.", status="manual")
        self.assertEqual((d.get("p1").text, d.get("p1").status), ("Revised text.", "manual"))
        d.edit_text("h1", "Geometry")
        self.assertEqual(d.get("h1").text, "Geometry")
        d.move("c1", "start")
        self.assertEqual([b.id for b in d.blocks], ["c1", "h1", "r1", "p1"])
        rec = d.remove("p1")
        self.assertEqual([b.id for b in d.blocks], ["c1", "h1", "r1"])
        self.assertEqual([row["id"] for row in rec.outline], ["c1", "h1", "r1"])
        self.assertEqual(rec.to_dict()["block_id"], "p1")

    def test_placement(self):
        d = self.doc
        d.add_heading("A")
        d.add_heading("B")
        d.add_heading("Zero", after="start")
        d.add_heading("Mid", after="h1")
        self.assertEqual([b.text for b in d.blocks], ["Zero", "A", "Mid", "B"])
        d.move("h2", "start")
        self.assertEqual([b.text for b in d.blocks], ["B", "Zero", "A", "Mid"])

    def test_error_codes(self):
        d = self.doc
        d.add_heading("Structure")
        d.add_readout("water", include=["summary"])
        self.assertEqual(code_of(lambda: d.add_readout("nope")), "unknown_source")
        self.assertEqual(code_of(lambda: d.add_readout("water", include=["nonesuch"])), "unknown_section")
        self.assertEqual(code_of(lambda: d.add_readout("water", exclude=["nonesuch"])), "unknown_section")
        self.assertEqual(code_of(lambda: d.add_readout("water", include=["missing"])), "unavailable_section")
        self.assertEqual(code_of(lambda: d.add_readout("water", include=[])), "bad_argument")
        self.assertEqual(code_of(lambda: d.add_readout("water", include="summary")), "bad_argument")
        self.assertEqual(code_of(lambda: d.remove("zz9")), "unknown_block")
        self.assertEqual(code_of(lambda: d.set_caption("zz9", "x")), "unknown_block")
        self.assertEqual(code_of(lambda: d.set_caption("h1", "x")), "bad_argument")
        self.assertEqual(code_of(lambda: d.edit_text("r1", "x")), "bad_argument")
        self.assertEqual(code_of(lambda: d.add_heading("x", after="zz9")), "bad_position")
        self.assertEqual(code_of(lambda: d.move("h1", "zz9")), "bad_position")
        self.assertEqual(code_of(lambda: d.move("h1", "h1")), "bad_position")
        self.assertEqual(code_of(lambda: d.add_text("x", cites=["h1"])), "unknown_block")   # not a readout block
        self.assertEqual(code_of(lambda: d.add_heading("x", level=4)), "bad_argument")
        self.assertEqual(code_of(lambda: d.add_text("x", status="bogus")), "bad_argument")
        self.assertEqual(code_of(lambda: d.add_callout("x", kind="loud")), "bad_argument")
        # failed operations changed nothing and burned no ids
        self.assertEqual([b.id for b in d.blocks], ["h1", "r1"])
        self.assertEqual(d.add_heading("Next").block_id, "h2")
        e = ReportOperationError("bad_argument", "detail", extra=1)
        self.assertEqual(e.to_dict(), {"code": "bad_argument", "detail": "detail", "extra": 1})

    def test_error_details_name_the_choices(self):
        with self.assertRaises(ReportOperationError) as cm:
            self.doc.add_readout("water", include=["nonesuch"])
        self.assertIn("frequencies", cm.exception.detail)
        self.assertIn("summary", cm.exception.info["choices"])
        with self.assertRaises(ReportOperationError) as cm:
            self.doc.add_readout("zzz")
        self.assertEqual(cm.exception.info["choices"], ["water"])

    def test_text_limits(self):
        d = self.doc
        self.assertEqual(code_of(lambda: d.add_heading("x" * 81)), "bad_argument")
        d.add_heading("x" * 80)
        self.assertEqual(code_of(lambda: d.add_heading("two\nlines")), "bad_argument")
        self.assertEqual(code_of(lambda: d.add_heading("  ")), "bad_argument")
        d.add_readout("water", include=["summary"], caption="c" * 300)
        self.assertEqual(code_of(lambda: d.set_caption("r1", "c" * 301)), "bad_argument")
        self.assertEqual(code_of(lambda: d.set_caption("r1", "two\nlines")), "bad_argument")
        self.assertEqual(code_of(lambda: d.add_text("hidden <!-- comment -->")), "bad_argument")
        self.assertEqual(code_of(lambda: d.add_text("")), "bad_argument")
        self.assertEqual(code_of(lambda: ReportDocument("two\nlines")), "bad_argument")

    def test_ids_are_never_reused(self):
        d = self.doc
        d.add_heading("A")
        d.add_heading("B")
        d.remove("h2")
        self.assertEqual(d.add_heading("C").block_id, "h3")
        d.remove("h3")
        d.remove("h1")
        self.assertEqual(d.add_heading("D").block_id, "h4")
        self.assertEqual(d.add_text("t").block_id, "p1")

    def test_remove_drops_citations(self):
        d = self.doc
        d.add_readout("water", include=["summary"])
        d.add_readout("water", include=["frequencies"])
        d.add_text("Both.", cites=["r1", "r2"])
        d.remove("r1")
        self.assertEqual(d.get("p1").cites, ["r2"])
        self.assertEqual(d.validate(), [])

    def test_outline_contents(self):
        d = self.doc
        d.add_heading("Structure", level=3)
        d.add_readout("water", include=["summary"], caption="The energy.")
        d.add_text("x " * 100, role="summary")
        d.add_callout("A flag.", kind="flag")
        rows = {r["id"]: r for r in d.outline()}
        self.assertEqual(rows["h1"], {"id": "h1", "kind": "heading", "level": 3, "text": "Structure"})
        self.assertEqual(rows["r1"]["handle"], "water")
        self.assertEqual(rows["r1"]["include"], ["summary"])
        self.assertEqual(rows["r1"]["caption"], "The energy.")
        self.assertEqual(rows["p1"]["role"], "summary")
        self.assertLessEqual(len(rows["p1"]["text"]), 80)
        self.assertEqual(rows["c1"]["callout"], "flag")

    def test_sections_group_under_level_two_headings(self):
        d = self.doc
        d.add_text("Intro.", role="summary")
        d.add_heading("One")
        d.add_heading("Sub", level=3)
        d.add_readout("water", include=["summary"])
        d.add_heading("Two")
        d.add_text("Last.")
        groups = d.sections()
        self.assertEqual([(g[0].text if g[0] else None, [b.id for b in g[1]]) for g in groups],
                         [(None, ["p1"]), ("One", ["h2", "r1"]), ("Two", ["p2"])])

    def test_validate(self):
        d = self.doc
        d.add_readout("water", include=["summary"])
        self.assertEqual(d.validate(), [])
        d.blocks.append(ReadoutBlock("r9", "gone"))
        d.blocks.append(Prose("p9", "x", cites=["h77"]))
        d.blocks.append(Heading("r1", "dup id"))
        codes = sorted(e.code for e in d.validate())
        self.assertEqual(codes, ["invalid_document", "unknown_block", "unknown_source"])


class MarkdownTests(unittest.TestCase):
    def build(self):
        cat = toy_catalog(water=ToyResult("water"), hod=ToyResult("hod", energy=-76.5))
        d = ReportDocument("Water & friends", cat, meta={"note": "a --> b", "policy": "grounded", "n": [1, 2]})
        d.add_text("Summary of -76.0267 Hartree.", cites=[], role="summary", status="grounded")
        d.add_heading("Structure")
        d.add_readout("water", include=["summary"], caption="Energy *of* water_1 \\ done.")
        d.add_readout("hod", include=["frequencies"], units={"frequency": "cm^-1"}, style="dark")
        d.add_text("Body text.\n\nSecond paragraph.", cites=["r1", "r2"], status="unchecked")
        d.add_heading("Details", level=3)
        d.add_readout("water", exclude=["frequencies"], header=True)
        d.add_callout("Heads up --> careful.", kind="flag")
        d.add_callout("Just a note.")
        d.blocks.append(RawMarkdown(d._mint(RawMarkdown), "Hand written *markdown*.\n\n- item one\n- item two"))
        return d, cat

    def test_round_trip_is_exact(self):
        d, cat = self.build()
        md = d.to_markdown()
        again = ReportDocument.from_markdown(md, cat)
        self.assertEqual(again.to_markdown(), md)
        self.assertEqual([b.id for b in again.blocks], [b.id for b in d.blocks])
        self.assertEqual(again.meta, d.meta)
        self.assertEqual(again.title, "Water & friends")
        self.assertEqual(again.get("r1").caption, "Energy *of* water_1 \\ done.")
        self.assertEqual(again.get("r2").units, {"frequency": "cm^-1"})
        self.assertEqual(again.get("p2").cites, ["r1", "r2"])
        self.assertEqual(again.get("c1").callout_kind, "flag")
        self.assertEqual(again.validate(), [])
        # id counters resume above the highest id found
        self.assertEqual(again.add_heading("New").block_id, "h3")

    def test_format_shape(self):
        d, cat = self.build()
        md = d.to_markdown()
        lines = md.split("\n")
        self.assertTrue(lines[0].startswith("<!-- report-meta {"))
        self.assertEqual(lines[2], "# Water & friends")
        self.assertIn('<!-- block(p1, role="summary", status="checked") -->', md)
        self.assertIn('<!-- readout(id="r1", include=["summary"], header=False, show_code=False, isolated=True) -->', md)
        self.assertIn('header=True, show_code=False, isolated=True) -->', md)      # r3 asked for its title block
        self.assertIn('report_source("water", digest="%s")' % cat.get("water").digest, md)
        self.assertIn('<!-- caption(r1, status="manual") -->\n*Energy \\*of\\* water\\_1 \\\\ done.*', md)
        self.assertIn("> **Flag:** Heads up --> careful.", md)
        self.assertIn('<!-- block(p2, role="body", status="unchecked", cites=["r1","r2"]) -->', md)
        self.assertTrue(md.endswith("\n") and not md.endswith("\n\n"))

    def test_meta_comment_cannot_terminate_early(self):
        d, cat = self.build()
        first = d.to_markdown().split("\n")[0]
        self.assertEqual(first.count("-->"), 1)               # only the closing one
        self.assertTrue(first.endswith(" -->"))
        blob = first[len("<!-- report-meta "):-len(" -->")]
        self.assertNotIn(">", blob)
        self.assertNotIn("--", blob)
        self.assertEqual(json.loads(blob)["meta"]["note"], "a --> b")
        self.assertEqual(json.loads(blob)["format"], "mcr-report-v1")

    def test_marker_options_are_the_docs_whitelist(self):
        from McUtils.Docs.Examples import ExampleParser
        d, cat = self.build()
        blocks = ExampleParser.parse(d.to_markdown(), owner="t").blocks
        self.assertEqual([b.id for b in blocks], ["r1", "r2", "r3"])
        self.assertTrue(all(b.isolated for b in blocks))
        self.assertEqual(blocks[1].options["units"], {"frequency": "cm^-1"})
        self.assertEqual(blocks[1].options["style"], "dark")
        self.assertEqual(blocks[2].options["exclude"], ["frequencies"])
        self.assertEqual(len({b.key for b in blocks}), 3)
        self.assertEqual([b.options["header"] for b in blocks], [False, False, True])
        self.assertTrue(all(b.options["show_code"] is False for b in blocks))

    def test_hand_edited_text(self):
        d, cat = self.build()
        md = d.to_markdown()
        edited = md.replace("<!-- block(p2,", "An extra paragraph added by hand.\n\n## A Hand Heading\n\n```python\n## not a heading\n```\n\n<!-- block(p2,")
        edited += "\n<!-- readout(id=\"hand\", include=[\"x\"]) -->\n```python\nsomething_else()\n```\n"
        doc = ReportDocument.from_markdown(edited, cat)
        kinds = [(b.kind, b.id) for b in doc.blocks]
        raw_texts = [b.text for b in doc.blocks if isinstance(b, RawMarkdown)]
        self.assertTrue(any(t.startswith("An extra paragraph") for t in raw_texts))
        self.assertTrue(any("## not a heading" in t for t in raw_texts))              # fenced text isn't a heading
        self.assertIn("A Hand Heading", [b.text for b in doc.blocks if isinstance(b, Heading)])
        self.assertTrue(any("something_else()" in t and "readout(" in t for t in raw_texts))   # hand-written marked fence
        # the hand edits survive a second round trip, and nothing was lost
        again = ReportDocument.from_markdown(doc.to_markdown(), cat)
        self.assertEqual(again.to_markdown(), doc.to_markdown())
        self.assertEqual([b.kind for b in again.blocks], [b.kind for b in doc.blocks])
        self.assertEqual(len({b.id for b in doc.blocks}), len(doc.blocks))

    def test_moved_heading(self):
        d, cat = self.build()
        md = d.to_markdown()
        doc = ReportDocument.from_markdown(md.replace("<!-- block(h1, level=2) -->\n## Structure", "## Renamed"), cat)
        self.assertEqual([b.text for b in doc.blocks if isinstance(b, Heading) and b.level == 2], ["Renamed"])
        self.assertEqual(doc.title, "Water & friends")

    def test_digest_mismatch_is_reported_by_validate_not_by_parsing(self):
        d, cat = self.build()
        md = d.to_markdown()
        cat2 = toy_catalog(water=ToyResult("water", energy=-1.0), hod=ToyResult("hod", energy=-76.5))
        doc = ReportDocument.from_markdown(md, cat2)           # parsing doesn't complain
        problems = doc.validate()
        self.assertTrue(problems)
        self.assertTrue(all(p.info.get("problem") == "digest_mismatch" for p in problems))
        self.assertEqual({p.info["handle"] for p in problems}, {"water"})
        self.assertEqual(doc.to_markdown(), md)                # the report still says what it was written against
        self.assertEqual(doc.refresh_sources(), ["water"])
        self.assertEqual(doc.validate(), [])
        self.assertIn(cat2.get("water").digest, doc.to_markdown())
        self.assertNotEqual(doc.to_markdown(), md)

    def test_to_readout_tree(self):
        d, cat = self.build()
        ro = d.to_readout()
        self.assertIsInstance(ro, Readout)
        text = ro.to_text()
        self.assertTrue(text.startswith("Water & friends\n==="))
        self.assertLess(text.index("Summary of -76.0267"), text.index("Structure"))   # the summary comes first
        self.assertIn("Energy *of* water_1", text)                                    # captions
        self.assertIn("1648.23", text)
        self.assertIn("Heads up --> careful.", text)
        d.blocks.append(RawMarkdown("x9", '<!-- readout(id="z") -->\n```python\n1\n```'))
        self.assertIn("[hand-written readout: see the HTML report]", d.to_readout().to_text())
        no_catalog = ReportDocument.from_markdown(d.to_markdown())
        with self.assertRaises(ReportSourceError):
            no_catalog.to_readout()

    def test_block_titles_are_off_by_default_and_configurable(self):
        cat = toy_catalog()
        d = ReportDocument("T", cat)
        self.assertFalse(d.block_headers)
        d.add_readout("water", include=["summary"])
        d.add_readout("water", include=["summary"], header=True)
        self.assertEqual([b.header for b in d.blocks], [False, True])
        on = ReportDocument("T", cat, block_headers=True)
        on.add_readout("water", include=["summary"])
        on.add_readout("water", include=["summary"], header=False)
        self.assertEqual([b.header for b in on.blocks], [True, False])
        self.assertEqual(code_of(lambda: d.add_readout("water", header="yes")), "bad_argument")
        # all of it survives the Markdown, including the document default for blocks added later
        again = ReportDocument.from_markdown(on.to_markdown(), cat)
        self.assertTrue(again.block_headers)
        self.assertEqual([b.header for b in again.blocks], [True, False])
        self.assertEqual(again.to_markdown(), on.to_markdown())
        self.assertTrue(again.add_readout("water", include=["summary"]) and again.blocks[-1].header)

    def test_header_controls_the_title_in_the_tree(self):
        cat = toy_catalog()
        d = ReportDocument("T", cat)
        d.add_heading("Section")
        d.add_readout("water", include=["summary"])
        d.add_readout("water", include=["frequencies"], header=True)
        text = d.to_readout().to_text()
        self.assertEqual(text.count("Toy water"), 1)             # only the block that asked for its title block
        self.assertIn("-76.0267 Hartree", text)
        self.assertIn("1648.23", text)

    def test_generated_text_cannot_look_like_a_heading(self):
        d, cat = self.build()
        self.assertEqual(code_of(lambda: d.add_text("fine\n## not fine")), "bad_argument")
        self.assertEqual(code_of(lambda: d.edit_text("p1", "# nope")), "bad_argument")

    def test_heading_text_cannot_carry_its_own_hashes(self):
        d, cat = self.build()
        n = len(d.blocks)
        self.assertEqual(code_of(lambda: d.add_heading("## Results")), "bad_argument")
        self.assertEqual(code_of(lambda: d.edit_text("h1", "# Results")), "bad_argument")
        self.assertEqual(len(d.blocks), n)
        d.add_heading("Results # one")                      # a '#' that isn't first is just text


if __name__ == "__main__":
    unittest.main()

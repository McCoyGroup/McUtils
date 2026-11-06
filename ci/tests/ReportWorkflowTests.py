"""The report document's own Python API for working on a report (no model, no tools): templates, locks, history, checks."""
import unittest

from McUtils.Readouts.Reports import ReportDocument, ReportOperationError, DocumentSnapshot, diff_snapshots

from ReportFixtures import toy_catalog
from ReportToolsTests import TemplatedToy, LockedToy


def catalog(cls=TemplatedToy, **kw):
    return toy_catalog(water=cls("water", **kw))


class FromTemplateTests(unittest.TestCase):
    def test_from_template_builds_the_outline(self):
        doc = ReportDocument.from_template("Water", catalog(), "water")
        self.assertEqual([(b.kind, getattr(b, "text", None) or b.include) for b in doc.blocks],
                         [("heading", "Overview"), ("readout", ["summary"]), ("heading", "Vibrations"),
                          ("readout", ["frequencies"])])
        self.assertEqual(doc.text_status(), {"template": 2})
        self.assertEqual(doc.validate(), [])
        self.assertEqual(ReportDocument.from_markdown(doc.to_markdown(), doc.catalog).to_markdown(), doc.to_markdown())

    def test_apply_template_result_and_options(self):
        doc = ReportDocument("Water", catalog())
        r = doc.apply_template("water", optional=["picture"])
        self.assertEqual(r, {"added": ["h1", "r1", "h2", "r2", "h3", "r3"], "locked": [], "skipped_unavailable": ["missing"]})
        with self.assertRaises(ReportOperationError) as e:
            doc.apply_template("water", optional=["summary"])
        self.assertEqual(e.exception.code, "unknown_section")

    def test_a_source_without_a_template_outline(self):
        from ReportFixtures import ToyResult
        doc = ReportDocument("x", toy_catalog(plain=ToyResult("plain")))
        with self.assertRaises(ReportOperationError) as e:
            doc.apply_template("plain")
        self.assertEqual(e.exception.code, "no_template")

    def test_no_catalog(self):
        with self.assertRaises(ReportOperationError):
            ReportDocument("x").apply_template("water")

    def test_a_failed_apply_leaves_the_document_alone(self):
        doc = ReportDocument("Water", catalog())
        doc.add_heading("Mine")
        before = doc.to_markdown()
        with self.assertRaises(ReportOperationError):
            doc.apply_template("water", after="nope")
        self.assertEqual(doc.to_markdown(), before)


class LockTests(unittest.TestCase):
    def setUp(self):
        self.doc = ReportDocument.from_template("Water", catalog(LockedToy), "water")

    def test_the_template_locks_and_the_document_can_still_edit_them(self):
        self.assertEqual(self.doc.locked, ["r1", "h2", "r2"])
        self.assertTrue(self.doc.is_locked("r1"))
        self.assertFalse(self.doc.is_locked("h1"))
        # the document's own operations don't refuse: a person can always edit
        self.doc.set_caption("r1", "My caption.")
        self.doc.edit_text("h2", "Renamed")
        self.doc.remove("r2")
        self.assertEqual(self.doc.locked, ["r1", "h2"])           # ids no longer in the document are not reported

    def test_check_unlocked(self):
        with self.assertRaises(ReportOperationError) as e:
            self.doc.check_unlocked("r1")
        self.assertEqual((e.exception.code, e.exception.info["block_id"]), ("locked", "r1"))
        self.doc.check_unlocked("h1")

    def test_lock_unlock_and_lock_off(self):
        doc = ReportDocument.from_template("Water", catalog(), "water")
        self.assertEqual(doc.lock(["h1"]), ["h1"])
        self.assertEqual(doc.unlock(["h1"]), [])
        doc = ReportDocument("Water", catalog())
        self.assertEqual(doc.apply_template("water", lock=False)["locked"], [])
        doc2 = ReportDocument("Water", catalog(LockedToy))
        self.assertEqual(doc2.apply_template("water", lock=False)["locked"], [])
        self.assertEqual(doc2.locked, [])
        with self.assertRaises(ReportOperationError):
            doc.lock(["nope"])

    def test_locks_are_saved_with_the_report(self):
        again = ReportDocument.from_markdown(self.doc.to_markdown(), self.doc.catalog)
        self.assertEqual(again.locked, ["r1", "h2", "r2"])


class HistoryTests(unittest.TestCase):
    def setUp(self):
        self.doc = ReportDocument.from_template("Water", catalog(), "water")

    def test_snapshot_diff_and_restore(self):
        snap = self.doc.snapshot()
        self.assertIsInstance(snap, DocumentSnapshot)
        self.assertEqual(self.doc.diff(snap), [])
        self.doc.add_text("Hello.", cites=["r2"])
        self.doc.set_caption("r1", "New.")
        self.doc.remove("h1")
        ops = {(c["op"], c["id"]) for c in self.doc.diff(snap)}
        self.assertEqual(ops, {("added", "p1"), ("changed", "r1"), ("removed", "h1")})
        changed = [c for c in self.doc.diff(snap) if c["op"] == "changed"][0]
        self.assertEqual(changed["fields"]["caption"], {"from": "Energy and size.", "to": "New."})
        self.doc.restore(snap)
        self.assertEqual(self.doc.diff(snap), [])
        self.assertEqual([b.id for b in self.doc.blocks], ["h1", "r1", "h2", "r2"])

    def test_the_snapshot_is_independent_of_later_edits(self):
        snap = self.doc.snapshot()
        self.doc.edit_text("h1", "Changed")
        self.assertEqual(snap.blocks[0].text, "Overview")

    def test_diff_between_two_snapshots(self):
        a = self.doc.snapshot()
        self.doc.move("r2", "start")
        b = self.doc.snapshot()
        self.assertEqual([(c["op"], c["id"], c["after"]) for c in a.diff(b)], [("moved", "r2", "start")])
        self.assertEqual(diff_snapshots(b, a)[0]["op"], "moved")

    def test_a_transaction_rolls_back_on_error_including_ids_and_locks(self):
        doc = ReportDocument.from_template("Water", catalog(LockedToy), "water")
        before = doc.to_markdown()
        with self.assertRaises(RuntimeError):
            with doc.transaction():
                doc.add_heading("Temp")
                doc.unlock()
                raise RuntimeError("boom")
        self.assertEqual(doc.to_markdown(), before)
        self.assertEqual(doc.locked, ["r1", "h2", "r2"])
        self.assertEqual(doc.add_heading("Next").block_id, "h3")      # the id minted inside the transaction is free again

    def test_a_transaction_keeps_the_changes_when_nothing_fails(self):
        with self.doc.transaction():
            self.doc.add_heading("Kept")
        self.assertEqual(self.doc.blocks[-1].text, "Kept")


class TextChecksTests(unittest.TestCase):
    def setUp(self):
        self.doc = ReportDocument.from_template("Water", catalog(), "water")

    def test_text_status_counts_captions_and_paragraphs(self):
        self.doc.add_text("a", status="manual")
        self.doc.add_text("b", status="grounded")
        self.doc.add_callout("not counted")
        self.assertEqual(self.doc.text_status(), {"template": 2, "manual": 1, "checked": 1})

    def test_check_text_against_cited_blocks(self):
        res = self.doc.check_text("The bend is at 1648.23 and the stretches at 3832.71.", ["r2"])
        self.assertTrue(res.ok)
        res = self.doc.check_text("The bend is at 1700.5.", ["r2"])
        self.assertEqual([t.text for t in res.unmatched], ["1700.5"])
        self.assertFalse(self.doc.check_text("The energy is -76.02665.", []).ok)

    def test_check_text_tolerances_are_arguments(self):
        text = "The bend is at 1648.3."
        self.assertTrue(self.doc.check_text(text, ["r2"]).ok)
        self.assertFalse(self.doc.check_text(text, ["r2"], rel_tol=1e-6).ok)
        self.assertFalse(self.doc.check_text("There are 3 modes.", ["r2"], small_int_max=0).ok)

    def test_check_text_year_range(self):
        self.assertTrue(self.doc.check_text("Roughly 2000 wavenumbers.", ["r2"]).ok)
        self.assertFalse(self.doc.check_text("Roughly 2000 wavenumbers.", ["r2"], year_range=None).ok)
        self.assertFalse(self.doc.check_text("Roughly 2000 wavenumbers.", ["r2"], year_range=(1990, 1999)).ok)

    def test_check_text_needs_readout_blocks(self):
        with self.assertRaises(ReportOperationError):
            self.doc.check_text("x", ["h1"])
        with self.assertRaises(ReportOperationError):
            self.doc.check_text("x", ["nope"])


if __name__ == "__main__":
    unittest.main()


def sectioned():
    """h1 [r1, p1] / h2 [r2, h3(level 3) [p2]] / h4 [p3]"""
    doc = ReportDocument("S", toy_catalog(water=TemplatedToy("water")))
    doc.add_heading("One")                                     # h1
    doc.add_readout("water", include=["summary"])               # r1
    doc.add_text("a")                                           # p1
    doc.add_heading("Two")                                      # h2
    doc.add_readout("water", include=["frequencies"])           # r2
    doc.add_heading("Sub", level=3)                             # h3
    doc.add_text("b")                                           # p2
    doc.add_heading("Three")                                    # h4
    doc.add_text("c")                                           # p3
    return doc


class SectionTests(unittest.TestCase):
    def ids(self, doc):
        return [b.id for b in doc.blocks]

    def test_section_end_and_ids(self):
        doc = sectioned()
        self.assertEqual(doc.section_end("h1"), "p1")
        self.assertEqual(doc.section_end("h2"), "p2")        # the level-3 subsection belongs to the level-2 section
        self.assertEqual(doc.section_ids("h3"), ["h3", "p2"])
        self.assertEqual(doc.section_end("h4"), "p3")
        doc.add_heading("Empty")
        self.assertEqual(doc.section_end("h5"), "h5")
        with self.assertRaises(ReportOperationError) as e:
            doc.section_end("r1")
        self.assertEqual(e.exception.code, "bad_argument")
        self.assertEqual(self.raises(lambda: doc.section_end("zz")), "unknown_block")

    def raises(self, f):
        with self.assertRaises(ReportOperationError) as e:
            f()
        return e.exception.code

    def test_move_section_takes_the_contents_along(self):
        doc = sectioned()
        doc.move_section("h2", "start")
        self.assertEqual(self.ids(doc), ["h2", "r2", "h3", "p2", "h1", "r1", "p1", "h4", "p3"])
        doc.move_section("h2", "p3")
        self.assertEqual(self.ids(doc), ["h1", "r1", "p1", "h4", "p3", "h2", "r2", "h3", "p2"])

    def test_move_section_after_a_heading_goes_after_its_whole_section(self):
        doc = sectioned()
        doc.move_section("h1", "h2")
        self.assertEqual(self.ids(doc), ["h2", "r2", "h3", "p2", "h1", "r1", "p1", "h4", "p3"])

    def test_move_section_into_itself_is_refused_and_changes_nothing(self):
        doc = sectioned()
        before = self.ids(doc)
        self.assertEqual(self.raises(lambda: doc.move_section("h2", "p2")), "bad_position")
        self.assertEqual(self.raises(lambda: doc.move_section("h2", "h3")), "bad_position")
        self.assertEqual(self.raises(lambda: doc.move_section("h2", "nope")), "bad_position")
        self.assertEqual(self.raises(lambda: doc.move_section("r1", "start")), "bad_argument")
        self.assertEqual(self.ids(doc), before)

    def test_under_adds_at_the_end_of_a_section(self):
        doc = sectioned()
        doc.add_text("new", under="h1")
        doc.add_readout("water", include=["summary"], under="h2")
        doc.add_heading("Later", under="h4")
        self.assertEqual(self.ids(doc), ["h1", "r1", "p1", "p4", "h2", "r2", "h3", "p2", "r3", "h4", "p3", "h5"])
        self.assertEqual(self.raises(lambda: doc.add_text("x", after="h1", under="h1")), "bad_argument")
        self.assertEqual(self.raises(lambda: doc.add_text("x", under="r1")), "bad_argument")

    def test_legacy_grounded_status_reads_as_checked(self):
        doc = sectioned()
        doc.add_text("g", status="grounded")
        self.assertEqual(doc.blocks[-1].status, "checked")
        md = doc.to_markdown().replace('status="checked"', 'status="grounded"')
        again = ReportDocument.from_markdown(md, doc.catalog)
        self.assertEqual(again.blocks[-1].status, "checked")
        doc.set_caption("r1", "c", status="grounded")
        self.assertEqual(doc.get("r1").caption_status, "checked")
        self.assertEqual(self.raises(lambda: doc.add_text("x", status="bogus")), "bad_argument")


class SourceErrorTests(unittest.TestCase):
    def test_source_errors_are_structured(self):
        from McUtils.Readouts.Reports import ReportSourceError
        cat = toy_catalog(water=TemplatedToy("water"))
        with self.assertRaises(ReportSourceError) as e:
            cat.get("nope")
        self.assertEqual((e.exception.code, e.exception.info["choices"]), ("unknown_source", ["water"]))
        with self.assertRaises(ReportSourceError) as e:
            cat.peek("water", "nope")
        self.assertEqual(e.exception.code, "unknown_section")
        self.assertIn("frequencies", e.exception.info["choices"])
        self.assertEqual(e.exception.to_dict()["section"], "nope")
        with self.assertRaises(ValueError):                  # still a ValueError
            cat.get("nope")

    def test_dotted_parts_are_validated(self):
        from ReportFixtures import NestedToy
        doc = ReportDocument("N", toy_catalog(n=NestedToy()))
        doc.add_readout("n", include=["parts.second"])
        with self.assertRaises(ReportOperationError) as e:
            doc.add_readout("n", include=["parts.bogus"])
        self.assertEqual(e.exception.code, "unknown_section")
        self.assertIn("bogus", e.exception.detail)
        self.assertEqual(len(doc.blocks), 1)
        self.assertIn("second part", doc.catalog.peek("n", "parts.second"))
        from McUtils.Readouts.Reports import ReportSourceError
        with self.assertRaises(ReportSourceError):
            doc.catalog.peek("n", "parts.bogus")

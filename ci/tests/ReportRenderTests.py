"""Rendering reports: HTML through the docs pipeline (with caching), PowerPoint, and the Markdown copy."""

import io
import os
import re
import tempfile
import unittest
import zipfile

from McUtils.Readouts.Reports import ReportDocument, ReportRenderer, ReportRenderError

from ReportFixtures import ToyResult, toy_catalog


def build(cat):
    doc = ReportDocument("Toy Report", cat)
    doc.add_text("A summary mentioning -76.0267 Hartree.", role="summary")
    doc.add_heading("Structure")
    doc.add_readout("water", include=["summary"], caption="The energy of water.")
    doc.add_heading("Vibrations")
    doc.add_readout("hod", include=["frequencies"], caption="Three vibrational modes.")
    doc.add_callout("Frequencies are harmonic.", kind="note")
    return doc


def slide_texts(path):
    with zipfile.ZipFile(path) as z:
        names = sorted((n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)),
                       key=lambda n: int(re.findall(r"\d+", n.rsplit("/", 1)[1])[0]))
        return [re.findall(r"<a:t>([^<]*)</a:t>", z.read(n).decode("utf-8")) for n in names]


def outside_code(html):
    return re.sub(r"<code[^>]*>.*?</code>", "", html, flags=re.S)


class RenderTestBase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.out = os.path.join(self._tmp.name, "out")
        self.cat = toy_catalog(water=ToyResult("water"), hod=ToyResult("hod", energy=-76.5, freqs=(1400.5, 2700.25, 2800.75)))
        self.doc = build(self.cat)


class HTMLRenderTests(RenderTestBase):
    def test_html_is_self_contained_with_inline_fragments(self):
        res = ReportRenderer(self.cat).render(self.doc, self.out, formats=("html",))
        self.assertTrue(res.ok, res.problems)
        self.assertEqual(res.statuses, {"r1": "ok", "r2": "ok"})
        with open(res.paths["html"], encoding="utf-8") as f:
            html = f.read()
        self.assertTrue(html.startswith("<!DOCTYPE html>"))
        self.assertIn("<title>Toy Report</title>", html)
        self.assertEqual(html.count('class="mcr-root"'), 2)          # one fragment per readout block
        self.assertIn("-76.0267", html)                              # water's energy
        self.assertIn("1400.5", html)                                # hod's frequencies
        self.assertIn("The energy of water.", html)                  # the caption
        self.assertIn("Frequencies are harmonic.", html)
        self.assertIn("<h2>Structure</h2>", html)
        self.assertNotIn("data-src=", html)                          # nothing is fetched at view time
        self.assertNotIn("<!-- readout(", html)
        self.assertNotIn("report_source(", html)                     # the code is not shown at all
        self.assertNotIn("<pre><code", html.split("<body")[1])
        self.assertNotIn('class="mcr-header"', html.split("<body")[1])   # nor the readouts' own title blocks
        self.assertNotIn("report-meta", html)

    def test_the_store_defaults_beside_the_output(self):
        ReportRenderer(self.cat).render(self.doc, self.out, formats=("html",))
        self.assertTrue(os.path.isfile(os.path.join(self.out, "readouts", "manifest.json")))
        other = os.path.join(self._tmp.name, "elsewhere")
        ReportRenderer(self.cat, store=other).render(self.doc, self.out, formats=("html",))
        self.assertTrue(os.path.isdir(other))

    def test_an_unchanged_document_executes_nothing(self):
        r = ReportRenderer(self.cat)
        first = r.render(self.doc, self.out, formats=("html",))
        self.assertEqual(sorted(first.executed), ["r1", "r2"])
        second = r.render(self.doc, self.out, formats=("html",))
        self.assertEqual(second.executed, [])
        self.assertTrue(second.ok)
        # captions and prose don't invalidate anything either
        self.doc.set_caption("r1", "A new caption.")
        self.doc.add_text("More prose.")
        third = r.render(self.doc, self.out, formats=("html",))
        self.assertEqual(third.executed, [])
        with open(third.paths["html"], encoding="utf-8") as f:
            self.assertIn("A new caption.", f.read())
        self.assertEqual(r.render(self.doc, self.out, formats=("html",), refresh=True).executed.__len__(), 2)

    def test_a_changed_source_reruns_exactly_its_blocks(self):
        r = ReportRenderer(self.cat)
        r.render(self.doc, self.out, formats=("html",))
        cat2 = toy_catalog(water=ToyResult("water", energy=-70.5), hod=ToyResult("hod", energy=-76.5,
                                                                                    freqs=(1400.5, 2700.25, 2800.75)))
        doc2 = ReportDocument.from_markdown(self.doc.to_markdown(), cat2)
        self.assertEqual(doc2.refresh_sources(), ["water"])
        res = ReportRenderer(cat2).render(doc2, self.out, formats=("html",))
        self.assertEqual(res.executed, ["r1"])
        with open(res.paths["html"], encoding="utf-8") as f:
            html = f.read()
        self.assertIn("-70.5", html)
        self.assertEqual(html.count("-76.0267"), 1)        # only the hand-written summary still says so

    def test_a_stale_digest_is_an_error_not_silently_wrong(self):
        cat2 = toy_catalog(water=ToyResult("water", energy=-70.5), hod=ToyResult("hod", energy=-76.5,
                                                                                    freqs=(1400.5, 2700.25, 2800.75)))
        stale = ReportDocument.from_markdown(self.doc.to_markdown(), cat2)       # not refreshed
        with self.assertRaises(ReportRenderError) as cm:
            ReportRenderer(cat2).render(stale, self.out, formats=("html",))
        self.assertEqual(cm.exception.result.statuses["r1"], "error")
        self.assertEqual(cm.exception.result.statuses["r2"], "ok")
        self.assertIn("has changed", str(cm.exception))
        self.assertFalse(os.path.exists(os.path.join(self.out, "report.html")))
        lenient = ReportRenderer(cat2, strict=False).render(stale, self.out, formats=("html",))
        self.assertFalse(lenient.ok)
        self.assertEqual(lenient.statuses, {"r1": "error", "r2": "ok"})
        with open(lenient.paths["html"], encoding="utf-8") as f:
            html = f.read()
        self.assertIn("mcr-error", html)
        self.assertIn("1400.5", html)                      # the good block is still there

    def test_a_missing_source_is_an_error(self):
        doc = ReportDocument.from_markdown(self.doc.to_markdown(), toy_catalog(water=ToyResult("water")))
        with self.assertRaises(ReportRenderError):
            ReportRenderer(toy_catalog(water=ToyResult("water"))).render(doc, self.out, formats=("html",))


class BlockTitleTests(RenderTestBase):
    def test_html_title_block_is_opt_in(self):
        self.doc.add_readout("water", include=["summary"], header=True)
        res = ReportRenderer(self.cat).render(self.doc, self.out, formats=("html",))
        with open(res.paths["html"], encoding="utf-8") as f:
            body = f.read().split("<body")[1]
        self.assertEqual(body.count('<div class="mcr-title">Toy water</div>'), 1)    # r3 only

    def test_pptx_title_is_opt_in(self):
        flat = lambda path: [t for s in slide_texts(path) for t in s]
        res = ReportRenderer(self.cat).render(self.doc, self.out, formats=("pptx",))
        self.assertNotIn("Toy water", flat(res.paths["pptx"]))
        self.doc.add_readout("water", include=["summary"], header=True)
        res = ReportRenderer(self.cat).render(self.doc, self.out, formats=("pptx",))
        self.assertEqual(flat(res.paths["pptx"]).count("Toy water"), 1)


class PowerPointRenderTests(RenderTestBase):
    def test_pptx_holds_headings_values_and_captions(self):
        res = ReportRenderer(self.cat).render(self.doc, self.out, formats=("pptx",))
        self.assertTrue(res.ok, res.problems)
        with zipfile.ZipFile(res.paths["pptx"]) as z:
            self.assertIsNone(z.testzip())
            self.assertTrue(any(n.startswith("ppt/slides/slide") for n in z.namelist()))
        slides = slide_texts(res.paths["pptx"])
        flat = [t for s in slides for t in s]
        self.assertGreaterEqual(len(slides), 3)
        self.assertEqual(slides[0], ["Toy Report"])
        for expected in ("Structure", "Vibrations", "The energy of water.", "Three vibrational modes.",
                         "A summary mentioning -76.0267 Hartree.", "Frequencies are harmonic."):
            self.assertIn(expected, flat)
        joined = " ".join(flat)
        self.assertIn("-76.0267", joined)
        self.assertIn("2700.25", joined)

    def test_all_formats_together(self):
        res = ReportRenderer(self.cat).render(self.doc, self.out)
        self.assertEqual(sorted(res.paths), ["html", "md", "pptx"])
        self.assertTrue(all(os.path.isfile(p) for p in res.paths.values()))
        with open(res.paths["md"], encoding="utf-8") as f:
            self.assertEqual(f.read(), self.doc.to_markdown())

    def test_text_export_of_the_tree(self):
        text = self.doc.to_readout().to_text()
        self.assertIn("Toy Report\n==========", text)
        self.assertIn("1400.5", text)
        self.assertIn("The energy of water.", text)


if __name__ == "__main__":
    unittest.main()

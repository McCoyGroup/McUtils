"""Moving a whole source's sections (move_source) and the warning when one source's sections are split up."""
import unittest

from McUtils.Readouts.Reports import ReportDocument, report_toolset, ReportTemplate, register_report_template
from ReportFixtures import toy_catalog, ToyResult


class GroupToy(ToyResult):
    pass


@register_report_template(GroupToy)
class GroupToyTemplate(ReportTemplate):
    name = "toy-groups"
    sections = [("Structure", ["summary"]), ("Vibrations", ["frequencies"])]


def ok(result):
    assert result.ok, result.error
    return result.value


def make():
    cat = toy_catalog(hoh=GroupToy("hoh"), hod=GroupToy("hod"))
    doc = ReportDocument("Groups", cat)
    tools = report_toolset(doc, cat)
    ok(tools.call("apply_template", {"handle": "hoh"}))     # h1 r1 h2 r2
    ok(tools.call("apply_template", {"handle": "hod"}))     # h3 r3 h4 r4
    return doc, tools


def order(doc):
    return [b.id for b in doc.blocks]


class SourceGroupTests(unittest.TestCase):
    def test_source_sections(self):
        doc, _ = make()
        self.assertEqual(doc.source_sections("hoh"), ["h1", "h2"])
        self.assertEqual(doc.source_sections("hod"), ["h3", "h4"])
        self.assertEqual(doc.grouping_warnings(), [])

    def test_swap_with_one_call(self):
        doc, tools = make()
        v = ok(tools.call("move_source", {"handle": "hod", "after": "start"}))
        self.assertEqual(order(doc), ["h3", "r3", "h4", "r4", "h1", "r1", "h2", "r2"])
        self.assertNotIn("warnings", v)

    def test_after_a_heading_means_after_its_section(self):
        doc, tools = make()
        ok(tools.call("move_source", {"handle": "hoh", "after": "h3"}))
        self.assertEqual(order(doc), ["h3", "r3", "h1", "r1", "h2", "r2", "h4", "r4"])
        self.assertEqual(doc.grouping_warnings()[0]["handle"], "hod")

    def test_moving_one_section_warns_about_the_split(self):
        # the Granite T13 failure: only HOD Structure moved to the front
        doc, tools = make()
        v = ok(tools.call("move_section", {"heading_id": "h3", "after": "start"}))
        self.assertEqual([w["handle"] for w in v["warnings"]], ["hod"])
        self.assertIn("move_source", v["warnings"][0]["detail"])
        self.assertEqual(ok(tools.call("compile"))["warnings"][0]["sections"], ["h3", "h4"])
        ok(tools.call("move_source", {"handle": "hod", "after": "start"}))
        self.assertEqual(order(doc)[:4], ["h3", "r3", "h4", "r4"])
        self.assertEqual(ok(tools.call("compile"))["warnings"], [])

    def test_errors(self):
        doc, tools = make()
        self.assertEqual(tools.call("move_source", {"handle": "hot", "after": "start"}).error["code"], "bad_argument")
        self.assertEqual(tools.call("move_source", {"handle": "hod", "after": "r3"}).error["code"], "bad_position")
        self.assertEqual(order(doc), ["h1", "r1", "h2", "r2", "h3", "r3", "h4", "r4"])

    def test_mixed_sections_are_left_alone(self):
        doc, tools = make()
        ok(tools.call("add_heading", {"text": "Comparison"}))
        ok(tools.call("add_readout", {"handle": "hoh", "include": ["frequencies"]}))
        ok(tools.call("add_readout", {"handle": "hod", "include": ["frequencies"]}))
        ok(tools.call("move_source", {"handle": "hod", "after": "start"}))
        self.assertEqual(order(doc)[-3:], ["h5", "r5", "r6"])


if __name__ == "__main__":
    unittest.main()

"""
Unit labels in `UnitsData` (unicode / ASCII / LaTeX), the theme's use of them, and filled report values in each style. Nothing here touches the network.
"""
import json
import os
import tempfile
import unittest

from McUtils.Data import UnitsData
from McUtils.Readouts.Reports import ReportDocument, report_toolset, fill_text, unit_shorthand, ReportOperationError
from McUtils.Readouts.Reports.Fill import _join, example_value
from McUtils.Readouts.Reports.Instructions import report_instructions
from McUtils.Readouts.Styles import ReadoutTheme
from ReportFixtures import toy_catalog
from ReportFillTests import make as make_toy


class Restore(unittest.TestCase):
    def setUp(self):
        self._snap = ({k: dict(v) for k, v in UnitsData._label_table().items()}, UnitsData.label_style)
        self.addCleanup(self._restore)

    def _restore(self):
        UnitsData._unit_labels = {k: dict(v) for k, v in self._snap[0].items()}
        UnitsData.set_label_style(self._snap[1])


class UnitsDataLabelTests(Restore):
    def test_three_styles(self):
        self.assertEqual(UnitsData.unit_label("Wavenumbers"), "cm⁻¹")
        self.assertEqual(UnitsData.unit_label("Wavenumbers", "ascii"), "cm-1")
        self.assertEqual(UnitsData.unit_label("Wavenumbers", "latex"), r"\mathrm{cm^{-1}}")
        self.assertEqual(UnitsData.unit_label("Hartrees", "latex"), r"E_{\mathrm{h}}")
        self.assertEqual(UnitsData.unit_label("Angstroms", "ascii"), "Ang")

    def test_default_style_can_be_switched(self):
        v = UnitsData.label_version
        UnitsData.set_label_style("ascii")
        self.assertEqual(UnitsData.unit_label("Degrees"), "deg")
        self.assertGreater(UnitsData.label_version, v)
        with self.assertRaises(ValueError):
            UnitsData.set_label_style("html")
        with self.assertRaises(ValueError):
            UnitsData.unit_label("Degrees", "html")

    def test_unknown_unit_gives_its_name_and_missing_style_is_derived(self):
        self.assertEqual(UnitsData.unit_label("Furlongs"), "Furlongs")
        UnitsData.update_unit_labels({"Furlongs": {"unicode": "fur⁻¹"}})
        self.assertEqual(UnitsData.unit_label("Furlongs", "ascii"), "fur-1")
        self.assertEqual(UnitsData.unit_label("Furlongs", "latex"), r"\mathrm{fur^{-1}}")

    def test_update_overwrite_flag_and_styles(self):
        UnitsData.update_unit_labels({"Hartrees": {"unicode": "Ha", "ascii": "Ha"}}, overwrite=False)
        self.assertEqual(UnitsData.unit_label("Hartrees"), "Eₕ")
        UnitsData.update_unit_labels({"Hartrees": {"unicode": "Ha", "ascii": "HA"}}, styles=["unicode"])
        self.assertEqual((UnitsData.unit_label("Hartrees"), UnitsData.unit_label("Hartrees", "ascii")), ("Ha", "Eh"))

    def test_listed_labels_are_complete_and_ascii_is_ascii(self):
        table = UnitsData.unit_labels("unicode")
        self.assertGreater(len(table), 40)
        for name in table:
            for style in UnitsData.label_styles:
                self.assertTrue(UnitsData.unit_label(name, style), (name, style))
            self.assertTrue(UnitsData.unit_label(name, "ascii").isascii(), name)

    def test_composed_labels(self):
        cases = {      # name: (unicode, ascii, latex)
            "KilocaloriesPerMole": ("kcal/mol", "kcal/mol", r"\mathrm{kcal\,mol^{-1}}"),
            "Kilocalories/Mole": ("kcal/mol", "kcal/mol", r"\mathrm{kcal\,mol^{-1}}"),
            "KilojoulesPerMole": ("kJ/mol", "kJ/mol", r"\mathrm{kJ\,mol^{-1}}"),
            "KilometersPerMole": ("km/mol", "km/mol", r"\mathrm{km\,mol^{-1}}"),
            "InverseCentimeters": ("cm⁻¹", "cm-1", r"\mathrm{cm^{-1}}"),
            "InverseAngstromsSquared": ("Å⁻²", "Ang-2", r"\mathrm{\AA^{-2}}"),
            "GigaElectronVolts": ("GeV", "GeV", r"\mathrm{GeV}"),
            "MilliHartrees": ("mEₕ", "mEh", r"\mathrm{m}E_{\mathrm{h}}"),
            "Meters/Seconds": ("m/s", "m/s", r"\mathrm{m\,s^{-1}}"),
            "MetersSquared": ("m²", "m2", r"\mathrm{m^{2}}"),
            "Micrometers": ("µm", "um", r"\mu\mathrm{m}"),
            "MegaHerz": ("MHz", "MHz", r"\mathrm{MHz}"),
            "HartreesPerBohrRadius": ("Eₕ/a₀", "Eh/a0", r"E_{\mathrm{h}}\,a_{0}^{-1}"),
            "JoulesPerMole": ("J/mol", "J/mol", r"\mathrm{J\,mol^{-1}}"),
        }
        for name, want in cases.items():
            self.assertEqual(tuple(UnitsData.unit_label(name, s) for s in UnitsData.label_styles), want, name)

    def test_aliases_and_unresolved_names(self):
        self.assertEqual(UnitsData.unit_label("AtomicUnitOfEnergy"), UnitsData.unit_label("Hartrees"))
        for name in ("Furlongs", "FooPerMole", "KilocaloriesPerFurlong"):
            self.assertEqual(UnitsData.unit_label(name, "latex"), name)

    def test_every_real_target_unit_of_the_conversion_data_has_a_label(self):
        UnitsData.load()
        targets = {k[1] if isinstance(k[1], str) else k[1][0] for k, v in UnitsData._data.items()
                   if isinstance(k, tuple) and "Conversion" in v}
        known_gaps = {"HDebye", "HTeslas", "ProtonMassDifference", "ProtonMassDifferenceEnergyEquivalent"}
        missing = {u for u in targets if UnitsData.unit_label(u, "unicode") == u and u not in UnitsData._label_table()}
        self.assertEqual(missing - known_gaps, set())

    def test_conversion_rules(self):
        self.assertEqual(UnitsData.ascii_label("cm⁻¹"), "cm-1")
        self.assertEqual(UnitsData.ascii_label("Eₕ"), "Eh")
        self.assertEqual(UnitsData.latex_label("mₑ"), r"m_{\mathrm{e}}")
        self.assertEqual(UnitsData.latex_label("°"), r"^{\circ}")

    def test_load_from_json(self):
        with tempfile.TemporaryDirectory(dir="/tmp") as d:
            path = os.path.join(d, "labels.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"Debyes": {"unicode": "Debye", "note": "ignored"}}, f)
            UnitsData.load_unit_labels(path)
        self.assertEqual(UnitsData.unit_label("Debyes"), "Debye")


class ThemeTests(Restore):
    def test_theme_defaults_to_unitsdata(self):
        theme = ReadoutTheme()
        self.assertEqual(theme.get_unit_label("Wavenumbers"), "cm⁻¹")
        self.assertEqual(theme.get_unit_label("Wavenumbers", "ascii"), "cm-1")
        UnitsData.set_label_style("ascii")
        self.assertEqual(theme.get_unit_label("Hartrees"), "Eh")

    def test_theme_override_wins(self):
        theme = ReadoutTheme(unit_labels={"Hartrees": "Ha", "Degrees": {"ascii": "d"}}, unit_style="ascii")
        self.assertEqual(theme.get_unit_label("Hartrees"), "Ha")
        self.assertEqual(theme.get_unit_label("Degrees"), "d")
        self.assertEqual(theme.get_unit_label("Wavenumbers"), "cm-1")


class ReportStyleTests(Restore):
    def make(self, style=None):
        doc, cat, tools = make_toy(unit_style=style)       # h1 r1 | h2 r2 (frequencies 1648.23, 3832.71, 3943.88)
        return doc, tools

    def test_shorthand_in_each_style(self):
        self.assertEqual(unit_shorthand("cm^-1", "ascii"), "cm-1")
        self.assertEqual(unit_shorthand("Hartree", "latex"), r"E_{\mathrm{h}}")
        self.assertEqual(unit_shorthand("percent", "latex"), r"\%")

    def test_join(self):
        self.assertEqual(_join("1.0", "cm⁻¹", "unicode"), "1.0 cm⁻¹")
        self.assertEqual(_join("90.0", "°", "unicode"), "90.0°")
        self.assertEqual(_join("1.0", r"\mathrm{cm^{-1}}", "latex"), r"$1.0\,\mathrm{cm^{-1}}$")
        self.assertEqual(_join("90.0", r"^{\circ}", "latex"), r"$90.0^{\circ}$")
        self.assertEqual(_join("12.5", r"\%", "latex"), r"$12.5\%$")

    def test_fill_per_style(self):
        doc, tools = self.make("ascii")
        r = tools.call("add_text", {"text": "Lowest: {r2.frequency[1]}."})
        self.assertTrue(r.ok, r.error)
        self.assertEqual(doc.get(r.value["block_id"]).text, "Lowest: 1648.23 cm-1.")
        self.assertEqual(doc.unit_style, "ascii")
        doc, tools = self.make("latex")
        r = tools.call("add_text", {"text": "Lowest: {r2.frequency[1]}."})
        self.assertEqual(doc.get(r.value["block_id"]).text, r"Lowest: $1648.23\,\mathrm{cm^{-1}}$.")

    def test_typed_unit_is_swallowed_in_any_style(self):
        doc, tools = self.make("ascii")
        r = tools.call("add_text", {"text": "Lowest: {r2.frequency[1]} cm⁻¹."})
        self.assertEqual(doc.get(r.value["block_id"]).text, "Lowest: 1648.23 cm-1.")
        r = tools.call("add_text", {"text": "Lowest: {r2.frequency[1]} eV."})
        self.assertFalse(r.ok)
        self.assertEqual(r.error["code"], "unit_mismatch")

    def test_style_is_stored_and_recheck_passes(self):
        doc, tools = self.make("latex")
        r = tools.call("add_text", {"text": "Lowest: {r2.frequency[1]}."})
        bid = r.value["block_id"]
        doc2 = ReportDocument.from_markdown(doc.to_markdown(), doc.catalog)
        self.assertEqual(doc2.unit_style, "latex")
        self.assertTrue(doc2.check_prose(bid).ok)

    def test_bad_style_is_refused(self):
        cat = toy_catalog()
        with self.assertRaises(ValueError):
            report_toolset(ReportDocument("x", cat), cat, unit_style="html")

    def test_default_follows_unitsdata(self):
        UnitsData.set_label_style("ascii")
        doc, tools = self.make()
        r = tools.call("add_text", {"text": "Lowest: {r2.frequency[1]}."})
        self.assertEqual(doc.get(r.value["block_id"]).text, "Lowest: 1648.23 cm-1.")

    def test_instruction_examples_follow_the_style(self):
        for level in (1, 2, 3):
            self.assertIn("3803.3 cm-1", report_instructions(None, level, unit_style="ascii"))
            self.assertNotIn("cm⁻¹", report_instructions(None, level, unit_style="ascii"))
            self.assertIn(r"$3803.3\,\mathrm{cm^{-1}}$", report_instructions(None, level, unit_style="latex"))
            self.assertIn("3803.3 cm⁻¹", report_instructions(None, level))
        self.assertEqual(example_value("latex"), r"$3803.3\,\mathrm{cm^{-1}}$")

    def test_tool_description_follows_the_style(self):
        doc, tools = self.make("ascii")
        self.assertIn("3803.3 cm-1", tools._tools["add_text"].description)


class GuidelinesPackagingTests(unittest.TestCase):
    ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    def test_guidelines_live_in_readouts_resources(self):
        path = os.path.join(self.ROOT, "McUtils", "Readouts", "resources", "READOUT_GUIDELINES.md")
        self.assertTrue(os.path.isfile(path), path)
        with open(path, encoding="utf-8") as f:
            self.assertIn("UnitsData", f.read())

    def test_manifest_includes_them(self):
        with open(os.path.join(self.ROOT, "MANIFEST.in"), encoding="utf-8") as f:
            self.assertIn("recursive-include McUtils/Readouts/resources", f.read())


if __name__ == "__main__":
    unittest.main()

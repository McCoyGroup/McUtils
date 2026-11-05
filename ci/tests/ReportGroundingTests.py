import unittest

import numpy as np

from McUtils.Readouts.Reports.Grounding import (extract_numbers, evidence_numbers, check_grounding, WritingPolicy,
                                                NumberToken)
from ReportFixtures import toy_catalog


def values(text):
    return [t.value for t in extract_numbers(text)]


class ExtractNumbersTests(unittest.TestCase):
    def test_plain_decimal_and_decimals_count(self):
        toks = extract_numbers("The bend is at 1648.2 cm-1.")
        self.assertEqual([(t.text, t.value, t.decimals) for t in toks], [("1648.2", 1648.2, 1)])

    def test_integers(self):
        toks = extract_numbers("There are 3 modes and 1648 is one.")
        self.assertEqual([(t.value, t.decimals) for t in toks], [(3.0, 0), (1648.0, 0)])

    def test_unicode_minus_and_hyphen_sign(self):
        self.assertEqual(values("energy of −76.02665 Eh"), [-76.02665])
        self.assertEqual(values("a shift of -12.3"), [-12.3])
        self.assertEqual(values("(-12.3)"), [-12.3])

    def test_scientific_notation(self):
        self.assertAlmostEqual(values("rate 1.2e-3 s")[0], 1.2e-3)
        self.assertAlmostEqual(values("rate 1.5E+4")[0], 1.5e4)
        t = extract_numbers("2.5e-3")[0]
        self.assertEqual(t.decimals, 4)      # 0.0025

    def test_times_ten_forms(self):
        self.assertAlmostEqual(values("1.5×10^3 units")[0], 1500.0)
        self.assertAlmostEqual(values("2.5 x 10^-3 units")[0], 2.5e-3)
        self.assertAlmostEqual(values("2×10⁻³ units")[0], 2e-3)
        self.assertEqual(len(extract_numbers("2.5 x 10^-3")), 1)       # the exponent is not a second number

    def test_percentages(self):
        t = extract_numbers("a 12.5% change")[0]
        self.assertTrue(t.percent)
        self.assertEqual(t.value, 12.5)
        self.assertEqual(t.text, "12.5%")

    def test_thousands_separator(self):
        self.assertEqual(values("about 1,234.5 steps"), [1234.5])

    def test_formulas_and_units_excluded(self):
        for text in ("H2O", "the C2v point group", "frequency in cm-1", "block r1 and r12", "CH3OH and D2O", "v_2",
                     "O-H2", "NH3"):
            with self.subTest(text=text):
                self.assertEqual(values(text), [], text)

    def test_number_beside_a_formula_is_kept(self):
        self.assertEqual(values("H2O has 3 atoms"), [3.0])
        self.assertEqual(values("CO2 at 2349.1"), [2349.1])

    def test_inline_code_excluded(self):
        self.assertEqual(values("use `add_readout(r3, 42.5)` for 7.5"), [7.5])

    def test_ranges_give_both_ends(self):
        for text in ("1600–1650", "1600-1650", "1600 – 1650", "1600−1650"):
            with self.subTest(text=text):
                self.assertEqual(values(text), [1600.0, 1650.0])
        self.assertEqual(values("between 5% and 10%"), [5.0, 10.0])
        self.assertEqual(values("5%-10%"), [5.0, 10.0])

    def test_spans_point_at_the_text(self):
        text = "x 1648.2 y"
        t = extract_numbers(text)[0]
        self.assertEqual(text[t.span[0]:t.span[1]], "1648.2")

    def test_version_like_strings_dont_split(self):
        self.assertEqual(len(extract_numbers("version 1.2.3")), 1)


class CheckGroundingTests(unittest.TestCase):
    EV = evidence_numbers(["Frequency 1648.23, 3832.71, 3943.88. Energy -76.02665. Shift -12.34. Fraction 0.125"])

    def ok(self, text, **kw):
        return check_grounding(text, self.EV, **kw)

    def test_rounding_matches(self):
        self.assertTrue(self.ok("The bend is at 1648.2 cm-1.").ok)
        self.assertTrue(self.ok("The bend is at 1648 cm-1.").ok)
        self.assertTrue(self.ok("about 1648.23").ok)

    def test_too_coarse_fails(self):
        r = self.ok("The bend is near 1650 cm-1.")
        self.assertFalse(r.ok)
        self.assertEqual([t.text for t in r.unmatched], ["1650"])

    def test_wrong_digit_fails(self):
        # with the default relative tolerance (1e-3) 1648.3 and 1649.2 are "close enough" to 1648.23: see STATUS.md
        self.assertFalse(self.ok("The bend is at 1648.3 cm-1.", rel_tol=0).ok)
        self.assertFalse(self.ok("The bend is at 1649.2.", rel_tol=0).ok)
        self.assertFalse(self.ok("The bend is at 1651.2.").ok)

    def test_negative_matches_with_either_sign(self):
        self.assertTrue(self.ok("an energy of −76.02665 Eh").ok)
        self.assertTrue(self.ok("a shift of 12.3").ok)          # the evidence has -12.34
        self.assertTrue(self.ok("a shift of -12.3").ok)

    def test_percent(self):
        self.assertTrue(self.ok("a fraction of 12.5%").ok)      # 0.125 as a percentage
        self.assertTrue(self.ok("a fraction of 0.125").ok)
        self.assertTrue(self.ok("a fraction of 13%").ok, "12.5% rounds to 13%")
        self.assertFalse(self.ok("a fraction of 20%").ok)

    def test_scientific_notation(self):
        ev = evidence_numbers(["rate 0.0012"])
        self.assertTrue(check_grounding("rate of 1.2e-3", ev).ok)
        self.assertTrue(check_grounding("rate of 1.2×10^-3", ev).ok)
        self.assertFalse(check_grounding("rate of 1.3e-3", ev).ok)

    def test_scientific_notation_in_evidence_text(self):
        ev = evidence_numbers(["rate 1.2e-3"])
        self.assertTrue(check_grounding("rate of 0.0012", ev).ok)

    def test_exempt_small_ints_and_years(self):
        self.assertTrue(self.ok("There are 3 modes, two of them stretches.").ok)
        self.assertTrue(self.ok("measured in 2019").ok)
        r = self.ok("There are 11 modes.")
        self.assertFalse(r.ok)
        self.assertEqual(self.ok("There are 11 modes.", small_int_max=20).ok, True)
        self.assertFalse(self.ok("a value of 2500").ok, "four digits outside the year range")
        self.assertFalse(self.ok("3.5 modes").ok, "a decimal is not a count")
        self.assertFalse(self.ok("3% of them").ok, "a percentage is not a count")

    def test_formulas_units_do_not_count(self):
        r = self.ok("H2O in C2v has stretches near 3832.7 cm-1.")
        self.assertTrue(r.ok, r)
        self.assertEqual(r.checked, 1)

    def test_ranges(self):
        self.assertTrue(self.ok("stretches span 3832–3944").ok)
        self.assertFalse(self.ok("stretches span 3832–4000").ok)

    def test_relative_tolerance(self):
        ev = np.array([123456.0])
        self.assertTrue(check_grounding("about 123500", ev).ok)               # within 1e-3 of 123456
        self.assertFalse(check_grounding("about 123500", ev, rel_tol=1e-6).ok)

    def test_empty_evidence_and_no_numbers(self):
        self.assertTrue(check_grounding("No numbers here at all.", np.zeros(0)).ok)
        self.assertFalse(check_grounding("A value of 12.5.", np.zeros(0)).ok)
        self.assertEqual(check_grounding("No numbers here.", self.EV).checked, 0)

    def test_errors_text_names_the_number(self):
        r = self.ok("The bend is near 1650 cm-1 and 2222.2.")
        errs = r.errors()
        self.assertEqual(len(errs), 2)
        self.assertIn("'1650'", errs[0])
        self.assertIn("do not compute", errs[0])

    def test_derived_quantities_are_not_matched(self):
        # 3832.71 - 3943.88 = -111.17, but differences are not in the evidence
        self.assertFalse(self.ok("the stretches differ by 111.2").ok)


class EvidenceNumbersTests(unittest.TestCase):
    def test_from_texts(self):
        arr = evidence_numbers(["a 1.5 b", "c −2"])
        self.assertEqual(sorted(arr.tolist()), [-2.0, 1.5])
        self.assertEqual(evidence_numbers("just 4.5").tolist(), [4.5])
        self.assertEqual(evidence_numbers().size, 0)

    def test_formula_digits_not_evidence(self):
        self.assertEqual(evidence_numbers(["H2O and C2v"]).size, 0)

    def test_from_readout_flat_data(self):
        cat = toy_catalog()
        ro = cat.get("water").readout(include=["summary", "frequencies"])
        ev = evidence_numbers(readouts=[ro])
        for expected in (-76.02665, 1648.23, 3832.71, 3943.88, 3):
            self.assertTrue(np.any(np.isclose(ev, expected)), expected)
        # a value only in the flat data (not in any text) is groundable
        self.assertTrue(check_grounding("frequencies 1648.23 and 3943.88", ev).ok)
        self.assertFalse(check_grounding("frequency 2000.5", ev).ok)

    def test_array_values_in_flat_data_and_cap(self):
        cat = toy_catalog()
        ro = cat.get("water").readout(include=["frequencies"])
        self.assertEqual(evidence_numbers(readouts=[ro], cap=2).size, 2)
        self.assertEqual(evidence_numbers(["1.5 2.5 3.5"], cap=2).size, 2)


class WritingPolicyTests(unittest.TestCase):
    def test_values_and_coerce(self):
        self.assertEqual({p.value for p in WritingPolicy}, {"grounded", "structure_only", "unchecked"})
        self.assertIs(WritingPolicy.coerce("grounded"), WritingPolicy.GROUNDED)
        self.assertIs(WritingPolicy.coerce(WritingPolicy.UNCHECKED), WritingPolicy.UNCHECKED)
        with self.assertRaises(ValueError):
            WritingPolicy.coerce("bogus")


if __name__ == "__main__":
    unittest.main()

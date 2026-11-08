
import os as _test_os
import unittest as _test_unittest
_RUN_EXTRAS = _test_os.environ.get("MCUTILS_TEST_EXTRAS") == "1"

import unittest
from xml.etree import ElementTree

from McUtils.Jupyter import JHTML


class JHTMLParseVoidTests(unittest.TestCase):
    def test_own_output_with_void_elements_parses(self):
        src = JHTML.Div(JHTML.Input(type="range", min="0"), JHTML.Br(), JHTML.Image(src="a.png"),
                        JHTML.Hr(), JHTML.P("text")).tostring()
        self.assertIn('<input type="range" min="0">', src)         # HTML serialization: no end tag
        for strict in (True, False):
            with self.subTest(strict=strict):
                el = JHTML.parse(src, strict=strict)
                self.assertEqual(type(el).__name__, "Div")
                self.assertEqual([c.tag for c in el.elems], ["input", "br", "img", "hr", "p"])
                self.assertEqual(el.elems[0].attrs["min"], "0")
                self.assertEqual(el.elems[2].attrs["src"], "a.png")

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_markdown_with_raw_void_elements_is_not_a_fallback_span(self):
        el = JHTML.Markdown('<div class="x"><label>Speed <input type="number" value="1"></label></div>')
        self.assertEqual(type(el).__name__, "Div")
        self.assertIn('<input type="number" value="1">', el.tostring())

    def test_attribute_values_containing_angle_brackets(self):
        el = JHTML.parse('<div><input type="text" value="a > b" title=\'x>y\'><span>s</span></div>')
        inp = el.elems[0]
        self.assertEqual((inp.attrs["value"], inp.attrs["title"]), ("a > b", "x>y"))
        self.assertEqual(el.elems[1].tag, "span")

    def test_already_closed_void_elements_are_untouched(self):
        el = JHTML.parse('<div><br/><input type="x"/></div>')
        self.assertEqual([c.tag for c in el.elems], ["br", "input"])

    def test_real_playback_controls_round_trip(self):
        from McUtils.Plots.X3DInterface import X3D
        src = X3D.get_playback_controls().tostring()
        el = JHTML.parse(src, strict=True)
        roles = [e.attrs.get("data-role") for e in el.find_all("input")] if hasattr(el, "find_all") else None
        self.assertIn('data-role="playback-position"', el.tostring())
        self.assertIn('data-role="playback-loop"', el.tostring())

    def test_invalid_markup_still_fails(self):
        with self.assertRaises(ElementTree.ParseError):
            JHTML.parse("<div><b></div>", strict=True)
        with self.assertRaises(ElementTree.ParseError):
            JHTML.parse("<div><input type='x'><b></div>", strict=True)
        self.assertEqual(type(JHTML.parse("<div><b></div>", strict=False)).__name__, "Span")


if __name__ == "__main__":
    unittest.main()

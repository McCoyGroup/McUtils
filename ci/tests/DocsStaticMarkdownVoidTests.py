
import os as _test_os
import unittest as _test_unittest
_RUN_EXTRAS = _test_os.environ.get("MCUTILS_TEST_EXTRAS") == "1"

import unittest

from McUtils.Docs import static_markdown


class DocsStaticMarkdownRawHTMLTests(unittest.TestCase):
    def body(self, text):
        return static_markdown(text, title="T").split("<body", 1)[1]

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_void_elements_render_as_markup(self):
        body = self.body('# Title\n\n<div class="c"><label>Speed <input type="number" value="1"></label><br>'
                         '<img src="a.png"></div>\n\nSome *text*.\n')
        self.assertIn("<h1>Title</h1>", body)
        self.assertIn('<input type="number" value="1">', body)
        self.assertIn("<em>text</em>", body)
        self.assertNotIn("&lt;", body)

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_script_text_is_not_escaped(self):
        body = self.body("# T\n\n<div><script>if (a < b && c > d) go();</script></div>\n")
        self.assertIn("if (a < b && c > d) go();", body)
        self.assertNotIn("&lt;", body)
        self.assertNotIn("&gt;", body)

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_not_well_formed_html_is_not_written_out_as_text(self):
        body = self.body("# T\n\n<div><b>unclosed</div>\n")
        self.assertIn("<h1>T</h1>", body)
        self.assertNotIn("&lt;", body)

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_html_comments_are_dropped(self):
        body = self.body("<!-- meta {\"a\": 1} -->\n\n# T\n\ntext <!-- inline --> more\n")
        self.assertNotIn("<!--", body)
        self.assertNotIn("meta", body)
        self.assertIn("<h1>T</h1>", body)

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_fenced_code_still_works(self):
        body = self.body("```python\nx = 1 < 2\n```\n")
        self.assertIn("language-python", body)
        self.assertIn("x = 1 &lt; 2", body)        # code is escaped, as it should be


if __name__ == "__main__":
    unittest.main()

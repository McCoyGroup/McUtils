import re
import unittest

from McUtils.Jupyter import JHTML


class JHTMLParseX3DTests(unittest.TestCase):
    MARKUP = ('<div><p>text</p><X3D><Scene>'
              '<Viewpoint orientation="0 1 0 1" position="2 0 1" fieldOfView="0.7"></Viewpoint>'
              '<Cylinder radius="1" height="1" bottom="true" top="false"></Cylinder>'
              '</Scene></X3D></div>')

    def _tag(self, s, name):
        return re.search(r"<%s[^>]*>" % name, s).group(0)

    def test_x3d_attributes_stay_attributes(self):
        for parse in (JHTML.parse, JHTML.Markdown):
            with self.subTest(parse=parse.__name__):
                s = parse(self.MARKUP).tostring()
                vp = self._tag(s, "Viewpoint")
                self.assertIn('position="2 0 1"', vp)
                self.assertNotIn("style=", vp)
                cyl = self._tag(s, "Cylinder")
                for attr in ('height="1"', 'bottom="true"', 'top="false"'):
                    self.assertIn(attr, cyl)
                self.assertNotIn("style=", cyl)

    def test_html_still_uses_styles(self):
        s = JHTML.parse('<div position="absolute" color="red">x</div>').tostring()
        self.assertIn("style=", s)

"""Shared XML fixes and compatibility with the existing HTML/SVG/X3D adapters."""
import io
import unittest
import xml.etree.ElementTree as ET

import numpy as np

from McUtils.Jupyter.JHTML import ContentXML, HTML, SVG
from McUtils.Jupyter.X3D import X3DHTML


def signature(xml):
    def walk(node):
        return node.tag, sorted(node.attrib.items()), node.text, [(walk(c), c.tail) for c in node]
    return walk(ET.fromstring(xml))


class ContentXMLTests(unittest.TestCase):
    def test_xml_attribute_names_and_literal_style(self):
        node = ContentXML.Element('node', snake_case='A', CamelCase='B', class_='C',
                                  xmlns__q='urn:q', q__value='D', width=4, color='red',
                                  style='literal XML style')
        self.assertEqual(node.attrs, {'snake_case': 'A', 'CamelCase': 'B', 'class': 'C',
                                     'xmlns:q': 'urn:q', 'q:value': 'D', 'width': 4,
                                     'color': 'red', 'style': 'literal XML style'})
        node['snake_case'] = 'changed'
        node['q__value'] = 'qualified'
        self.assertEqual(node['snake_case'], 'changed')
        self.assertEqual(node['q:value'], 'qualified')
        del node['snake_case']
        self.assertNotIn('snake_case', node.attrs)
        tree = ET.fromstring(node.to_bytes())
        self.assertEqual(tree.attrib['{urn:q}value'], 'qualified')
        self.assertEqual(tree.attrib['style'], 'literal XML style')

    def test_xml_values_and_adjacent_text(self):
        node = ContentXML.Element('node', 'a', 'b', ContentXML.Element('child'),
                                  'c', 'd', None, count=np.int64(3), pair=(1, 2),
                                  enabled=True, omitted=None)
        tree = node.to_etree()
        self.assertEqual(tree.text, 'ab')
        self.assertEqual(tree[0].tail, 'cd')
        self.assertEqual(tree.attrib, {'count': '3', 'pair': '1 2', 'enabled': 'true'})
        self.assertEqual(ContentXML.Element('text', ' a ', 'b ').to_etree().text, ' a b ')

    def test_shared_serializer_options(self):
        node = ContentXML.Element('root', ContentXML.Element('empty'), 'μ & λ')
        for prettify in (False, True):
            with self.subTest(prettify=prettify):
                text = node.tostring(prettify=prettify, encoding='unicode')
                data = node.tostring(prettify=prettify, encoding='utf-8', xml_declaration=True)
                self.assertIsInstance(text, str)
                self.assertIsInstance(data, bytes)
                self.assertTrue(data.startswith(b'<?xml'))
                self.assertEqual(signature(data), signature(text))
                self.assertIn('μ', text)
        self.assertEqual(node.tostring(prettify=False, method='text', encoding='unicode'), 'μ & λ')
        self.assertIn('<empty />', node.tostring(prettify=False, method='xml', encoding='unicode'))
        self.assertIn('<empty></empty>', node.tostring(prettify=False, method='html', encoding='unicode'))

    def test_parent_parse_preserves_namespaces_and_whitespace(self):
        source = (b'<x:root xmlns:x="urn:a" xmlns="urn:default" xmlns:q="urn:unused" Requires="q" '
                  b'snake_case="A" class_="B" q__literal="C">\n a <child> x </child> b '
                  b'<x:child xmlns:x="urn:b"/> c <x:child/>\n</x:root>')
        for value in (source, source.decode(), io.BytesIO(source)):
            node = ContentXML.parse(value)
            self.assertEqual(signature(node.to_bytes(prettify=False)), signature(source))
            self.assertEqual(node.attrs['xmlns:q'], 'urn:unused')
            self.assertEqual(node['class_'], 'B')
            self.assertEqual(node['q__literal'], 'C')
        self.assertEqual(ContentXML.parse('<node>\nvalue\n</node>', strip=True).to_etree().text, 'value')
        reserved = '<node tag="data" style="literal" on_update="data" activator="data"/>'
        self.assertEqual(signature(ContentXML.parse(reserved).to_bytes(prettify=False)), signature(reserved))

    def test_namespace_scope_is_recomputed_when_reusing_a_child(self):
        child = ContentXML.Element('x:child')
        a = ContentXML.Element('x:root', child, xmlns__x='urn:a')
        b = ContentXML.Element('x:root', child, xmlns__x='urn:b')
        self.assertEqual(ET.fromstring(a.to_bytes())[0].tag, '{urn:a}child')
        self.assertEqual(ET.fromstring(b.to_bytes())[0].tag, '{urn:b}child')
        self.assertEqual(ET.fromstring(a.to_bytes())[0].tag, '{urn:a}child')
        self.assertEqual(len(a.to_etree()), 1)

    def test_registered_types_use_parent_conversion(self):
        class TypedXML(ContentXML):
            class Entry(ContentXML.TagElement):
                tag = 'x:entry'

            @classmethod
            def get_class_map(cls):
                return {'{urn:test}entry': cls.Entry}

        source = '<x:entry xmlns:x="urn:test">a<x:entry/>b</x:entry>'
        node = TypedXML.parse(source)
        self.assertIsInstance(node, TypedXML.Entry)
        self.assertIsInstance(node.elems[1], TypedXML.Entry)
        self.assertEqual(signature(node.to_bytes(prettify=False)), signature(source))

    def test_html_styles_text_and_raw_html_still_work(self):
        node = HTML.Div(HTML.Br(), cls=['sample'], font_size=14, data_kind='demo')
        self.assertEqual(node.attrs['class'], ['sample'])
        self.assertEqual(node.attrs['style']['font-size'], 14)
        self.assertEqual(node.attrs['data-kind'], 'demo')
        self.assertIn('<br>', node.tostring(encoding='unicode', riffle=None))
        self.assertEqual(HTML.Div('a', 'b').to_tree()[0].text, 'a\nb')
        mixed = HTML.Div('A', HTML.B('B'), 'C')
        self.assertEqual(mixed.tostring(encoding='unicode', riffle=None), '<div>A<b>B</b>C</div>')
        raw = HTML.Div(HTML.RawHTML('<em>literal</em>'))
        self.assertEqual(raw.tostring(encoding='utf-8', riffle=None), b'<div><em>literal</em></div>')
        visited = []
        def converter(node, strip=True):
            visited.append(node.tag)
            return HTML.convert(node, strip=strip, converter=converter)
        parsed = HTML.parse('<div><span>text</span></div>', converter=converter)
        self.assertEqual(parsed.tag, 'div')
        self.assertEqual(visited, ['div', 'span'])

    def test_svg_and_x3d_serialization(self):
        svg = SVG.Svg(SVG.Rect(x=0, y=0, width=10, height=20))
        rect = ET.fromstring(svg.tostring(method='xml', prettify=True)).find('{*}rect')
        self.assertEqual(rect.attrib['width'], '10')
        scene = X3DHTML.Transform(X3DHTML.Shape(X3DHTML.Sphere(radius=1)), translation=(1, 2, 3))
        tree = ET.fromstring(scene.tostring(method='xml', prettify=True))
        self.assertEqual(tree.attrib['translation'], '1 2 3')
        self.assertEqual(tree.find('Shape/Sphere').attrib['radius'], '1')


if __name__ == '__main__':
    unittest.main()

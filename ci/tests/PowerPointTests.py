"""OPC, declarative XML reconstruction and PowerPoint export regressions."""
import io
import os
import runpy
import unittest
import xml.etree.ElementTree as ET
import zipfile
from unittest import mock

from McUtils.Jupyter.OpenXML import OpenXML, OpenXMLPackage, OpenXMLPart
from McUtils.Plots.PowerPoint import (
    PresentationML, PresentationMLSlide, PresentationMLPrimitive,
    PresentationMLText, PresentationMLImage, PresentationMLModel3D,
    PresentationMLAsset, PowerPointPresentation
)
from McUtils.Plots.PowerPoint import (
    PresentationMLElementLayout, PresentationMLAppearance, PresentationMLLine,
    PresentationMLAnimation, PresentationMLCamera, PresentationMLModel3DView,
    PresentationMLModelTransform, PresentationMLShape,
)

TEST_DATA = os.path.join(os.path.dirname(__file__), 'TestData')
REFERENCE = os.environ.get('MCUTILS_POWERPOINT_REFERENCE', os.path.join(TEST_DATA, 'example.pptx'))


def xml_signature(data):
    def walk(element):
        return (element.tag, tuple(sorted(element.attrib.items())), element.text,
                tuple((walk(c), c.tail) for c in element))
    return walk(ET.fromstring(data))


class OpenXMLTests(unittest.TestCase):
    def test_manifest_uses_default_namespace_without_mutating_objects(self):
        package = OpenXMLPackage([OpenXMLPart('data.xml', 'application/xml', OpenXML.a.t('data'))])
        source = package.content_types.to_bytes()
        with zipfile.ZipFile(io.BytesIO(package.to_bytes())) as archive:
            manifest = archive.read('[Content_Types].xml')
        self.assertIn(b'<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"', manifest)
        self.assertNotIn(b'<opc:', manifest)
        self.assertEqual(package.content_types.to_bytes(), source)
        self.assertEqual(ET.fromstring(manifest).tag,
                         '{http://schemas.openxmlformats.org/package/2006/content-types}Types')

    def test_catalog_and_contentxml(self):
        from McUtils.Jupyter.JHTML import ContentXML
        self.assertTrue(issubclass(OpenXML.p.sld, ContentXML.Element))
        self.assertIs(OpenXML.Element.to_tree, ContentXML.Element.to_tree)
        self.assertIs(OpenXML.Element.to_etree, ContentXML.Element.to_etree)
        self.assertIs(OpenXML.Element.tostring, ContentXML.Element.tostring)
        self.assertIs(OpenXML.parse.__func__, ContentXML.parse.__func__)
        self.assertIs(OpenXML.p.sld, OpenXML.Presentation.Slide)
        self.assertIs(OpenXML.w.document, OpenXML.Wordprocessing.Document)
        self.assertIs(OpenXML.x.worksheet, OpenXML.Spreadsheet.Worksheet)
        self.assertLess(len(OpenXML.get_class_map()), 1000)
        from McUtils.Jupyter.OpenXML.Vocabulary import Presentation
        self.assertIs(OpenXML.Presentation.Slide, Presentation.Slide)
        self.assertEqual(OpenXML.p.sld().local_tag, 'sld')
        with self.assertRaises(AttributeError):
            OpenXML.p.thisIsNotAnElement
        custom = OpenXML.register_namespace('test', 'urn:test', [])
        element = OpenXML.register_element('test', 'bespoke', name='Bespoke')
        self.assertIs(custom.Bespoke, element)
        self.assertEqual(ET.fromstring(element(value=3).to_bytes()).tag, '{urn:test}bespoke')

    def test_namespaces_attributes_and_mixed_text(self):
        element = OpenXML.mc.AlternateContent(
            OpenXML.mc.Choice(OpenXML.p.sp(), Requires='am3d'),
            OpenXML.mc.Fallback(OpenXML.p.pic()), mc__Ignorable='asvg')
        data = element.to_bytes()
        self.assertIn(b'xmlns:am3d=', data)
        self.assertIn(b'xmlns:asvg=', data)
        ET.fromstring(data)
        mixed = OpenXML.parse('<x:node xmlns:x="urn:custom" CamelCase="A" snake_case="B"> a <x:child/> b </x:node>')
        self.assertEqual(xml_signature(mixed.to_bytes()), xml_signature(
            b'<x:node xmlns:x="urn:custom" CamelCase="A" snake_case="B"> a <x:child/> b </x:node>'))
        self.assertEqual(mixed.attrs['snake_case'], 'B')
        self.assertEqual(OpenXML.a.t(' a ', 'b ').to_etree().text, ' a b ')
        self.assertIn('saveSubsetFonts="0"', OpenXML.p.presentation(saveSubsetFonts=False).tostring())

    def test_rebound_namespace_scope(self):
        source = b'<x:node xmlns:x="urn:a"><x:node xmlns:x="urn:b"/><x:node/></x:node>'
        self.assertEqual(xml_signature(OpenXML.parse(source).to_bytes()), xml_signature(source))

    def test_declarative_source(self):
        source = b'<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld/></p:sld>'
        element = OpenXML.parse(source)
        rebuilt = eval(element.to_source(), {'OpenXML': OpenXML})
        self.assertEqual(xml_signature(rebuilt.to_bytes()), xml_signature(source))
        clone = element.clone()
        clone.append(OpenXML.p.extLst())
        self.assertNotEqual(len(clone.elems), len(element.elems))

    def test_package_relationships_and_manifest(self):
        package = OpenXMLPackage()
        package.add_part('main.xml', 'application/custom+xml', OpenXML.a.t('x'))
        package.add_part('assets/one.bin', 'application/octet-stream', b'123')
        rid = package.add_relationship('main.xml', 'assets/one.bin', 'urn:asset')
        self.assertEqual(rid, 'rId1')
        self.assertEqual(package.add_relationship('main.xml', 'assets/one.bin', 'urn:asset'), rid)
        self.assertEqual(package.add_relationship('main.xml', 'https://example.com', 'urn:link', external=True), 'rId2')
        restored = OpenXMLPackage.from_file(package.to_bytes())
        restored.validate()
        self.assertEqual(restored['assets/one.bin'].to_bytes(), b'123')
        self.assertEqual(restored.content_type('main.xml'), 'application/custom+xml')
        with self.assertRaises(ValueError):
            restored.add_relationship('main.xml', 'assets/one.bin', 'urn:another', id='rId1')
        restored.remove_part('assets/one.bin')
        with self.assertRaisesRegex(ValueError, 'missing relationship target'):
            restored.validate()

    def test_dangling_explicit_relationship(self):
        package = OpenXMLPackage()
        package.add_part('main.xml', 'application/xml', OpenXML.a.blip(r__embed='rId99'))
        with self.assertRaisesRegex(ValueError, 'missing relationship'):
            package.validate()


@unittest.skipUnless(os.path.isfile(REFERENCE), 'example.pptx reference fixture is required')
class PowerPointTests(unittest.TestCase):
    def assert_package_matches_reference(self, data):
        with zipfile.ZipFile(REFERENCE) as expected, zipfile.ZipFile(io.BytesIO(data)) as actual:
            self.assertEqual(set(expected.namelist()), set(actual.namelist()))
            for name in expected.namelist():
                with self.subTest(part=name):
                    if name.endswith(('.xml', '.rels')):
                        self.assertEqual(xml_signature(expected.read(name)), xml_signature(actual.read(name)))
                    else:
                        self.assertEqual(expected.read(name), actual.read(name))

    def test_full_reference_round_trip(self):
        presentation = PresentationML.from_file(REFERENCE)
        self.assertEqual(len(presentation), 3)
        self.assertTrue(all(s.presentation is presentation for s in presentation.slides))
        self.assertFalse(hasattr(presentation, 'add_slide'))
        self.assertIsInstance(presentation[1][2], PresentationMLModel3D)
        self.assertIsInstance(presentation[2][1], PresentationMLImage)
        self.assertEqual(presentation.size, (12192000, 6858000))
        self.assert_package_matches_reference(presentation.to_bytes())

    def test_explicit_declarative_reference_without_reading_xml(self):
        build = runpy.run_path(os.path.join(TEST_DATA, 'PowerPointExample.py'))['build_example']
        original = zipfile.ZipFile.read
        def binary_only(archive, name, *args, **kwargs):
            if str(name).endswith(('.xml', '.rels')):
                raise AssertionError('declarative example must not read XML from the archive')
            return original(archive, name, *args, **kwargs)
        with mock.patch.object(zipfile.ZipFile, 'read', binary_only):
            presentation = build(REFERENCE)
            data = presentation.to_bytes()
        self.assert_package_matches_reference(data)

    def test_mutable_reference_round_trip(self):
        presentation = PowerPointPresentation.from_file(REFERENCE)
        self.assertIs(presentation[0].presentation, presentation)
        self.assert_package_matches_reference(presentation.to_bytes())

    def test_fresh_assets_and_slide_local_relationships(self):
        reference = PresentationML.from_file(REFERENCE)
        png = reference.scaffold['ppt/media/image4.png']
        svg = reference.scaffold['ppt/media/image3.svg']
        png_asset = PresentationMLAsset(png.to_bytes(), png.content_type, 'png')
        svg_asset = PresentationMLAsset(svg.to_bytes(), svg.content_type, 'svg')
        builder = PowerPointPresentation(size=(12, 8), units='in')
        a, b = builder.add_slide(), builder.add_slide()
        a.draw_text('  A & B  \nsecond', (1, 1, 3, 1), font_size=24)
        a.draw_image(png_asset, (1, 2, 4, 2))
        b.draw_image(svg_asset, (1, 2, 4, 2), fallback=png_asset)
        package = builder.to_package().validate()
        pres = ET.fromstring(package['ppt/presentation.xml'].to_bytes())
        size = pres.find('{%s}sldSz' % OpenXML.namespace_uris['p'])
        self.assertEqual(size.attrib, {'cx': str(12 * 914400), 'cy': str(8 * 914400)})
        slide_a = package['ppt/slides/slide1.xml'].data
        self.assertEqual(slide_a.find('off').attrs['x'], 0)  # shape-tree group transform
        offsets = [e for e in slide_a.walk() if e.local_tag == 'off']
        self.assertTrue(any(e.attrs['x'] == 914400 for e in offsets))
        self.assertIn('  A &amp; B  ', slide_a.tostring())
        slide_b = package['ppt/slides/slide2.xml'].data
        self.assertIsNotNone(slide_b.find('svgBlip'))
        media = [p for p in package.parts if p.startswith('ppt/media/')]
        self.assertEqual(len(media), 2)  # the PNG is shared by both slides
        self.assertEqual(len(package.relationships('ppt/slides/slide1.xml')), 2)
        self.assertEqual(len(package.relationships('ppt/slides/slide2.xml')), 3)
        self.assertEqual(builder.to_bytes(), builder.to_bytes())

    def test_native_models_from_view_and_appearance_objects(self):
        reference = PresentationML.from_file(REFERENCE)
        builder = PowerPointPresentation()
        slide = builder.add_slide()
        for i, primitive in enumerate(reference[1].children[2:]):
            model_xml = primitive.element.find('model3d')
            rels = {r.id: r for r in reference.scaffold.relationships(reference[1].part_name)}
            model_part = reference.scaffold[reference.scaffold.resolve_target(
                reference[1].part_name, rels[model_xml.attrs['r:embed']].target)]
            raster = model_xml.find('raster').find('blip')
            image_part = reference.scaffold[reference.scaffold.resolve_target(
                reference[1].part_name, rels[raster.attrs['r:embed']].target)]
            lighting = [e for e in model_xml.elems if isinstance(e, OpenXML.Element)
                        and e.local_tag in {'ambientLight', 'ptLight'}]
            slide.draw_glb(PresentationMLAsset(model_part.to_bytes(), model_part.content_type, 'glb'),
                           (30 + i * 400, 50, 360, 260),
                           fallback=PresentationMLAsset(image_part.to_bytes(), image_part.content_type, 'png'),
                           layout={'view': PresentationMLModel3DView.from_presml(model_xml)},
                           appearance={'lighting': lighting},
                           animation=PresentationMLAnimation.from_presml(model_xml))
        package = builder.to_package().validate()
        root = package['ppt/slides/slide1.xml'].data
        self.assertEqual(len([e for e in root.walk() if e.local_tag == 'model3d']), 2)
        self.assertEqual(len([e for e in root.walk() if e.local_tag == 'Fallback']), 2)
        self.assertEqual(len([e for e in root.walk() if e.local_tag == 'embedAnim']), 1)
        self.assertEqual(len(package.relationships('ppt/slides/slide1.xml')), 5)
        self.assertIn(b'xmlns:am3d=', root.to_bytes())

    def test_snapshot_isolation_and_repeat_export(self):
        builder = PowerPointPresentation()
        slide = builder.add_slide()
        drawn = slide.draw_text('before', (0, 0, 100, 20))
        snapshot = builder.to_presentationml()
        before = snapshot.to_bytes()
        drawn.text = 'after'
        slide.draw_shape('triangle', (10, 40, 100, 60))
        self.assertEqual(snapshot.to_bytes(), before)
        self.assertEqual(len(snapshot[0]), 1)
        self.assertEqual(len(builder[0]), 2)
        self.assertNotEqual(builder.to_bytes(), before)
        self.assertEqual(builder.to_bytes(), builder.to_bytes())

    def test_append_to_imported_slide_and_new_slide(self):
        builder = PowerPointPresentation.from_file(REFERENCE)
        builder[1].draw_text('new', (10, 10, 40, 20))
        builder.add_slide().draw_text('fourth', (20, 20, 80, 30))
        package = builder.to_package().validate()
        self.assertIn('ppt/slides/slide4.xml', package.parts)
        ids = [int(e.attrs['id']) for e in package['ppt/slides/slide2.xml'].data.walk() if e.local_tag == 'cNvPr']
        self.assertIn(3, ids)  # fill the reference slide's unused ID
        rebuilt = PresentationML.from_package(package)
        self.assertEqual(len(rebuilt), 4)

    def test_requested_ids_and_generic_xml_primitives(self):
        root = OpenXML.p.sp(OpenXML.p.nvSpPr(OpenXML.p.cNvPr(id=10, name='raw'),
                                           OpenXML.p.cNvSpPr(), OpenXML.p.nvPr()), OpenXML.p.spPr())
        slide = PresentationMLSlide(PresentationMLText('auto', (0, 0, 40, 20)),
                                    PresentationMLText('explicit', (0, 30, 40, 20), id=2),
                                    PresentationMLPrimitive(root))
        presentation = PresentationML(slide)
        ids = [int(e.attrs['id']) for e in presentation.to_package()['ppt/slides/slide1.xml'].data.walk()
               if e.local_tag == 'cNvPr']
        self.assertEqual(ids, [1, 3, 2, 10])
        self.assertIs(presentation[0].presentation, presentation)
        self.assertIsNone(slide.presentation)  # attaching did not mutate the supplied slide

    def test_invalid_dimensions_and_incomplete_model_view(self):
        with self.assertRaises(ValueError):
            PowerPointPresentation(size=(0, 5)).to_package()
        with self.assertRaises(ValueError):
            PresentationMLText('bad', (0, 0, -1, 20))
        with self.assertRaises(ValueError):
            PresentationMLText('bad', (float('nan'), 0, 1, 20))
        builder = PowerPointPresentation()
        builder.add_slide().draw_text('bad', (0, 0, 40, 20), id=2.5)
        with self.assertRaisesRegex(ValueError, 'integers'):
            builder.to_package()
        with self.assertRaisesRegex(ValueError, 'camera and trans'):
            PresentationMLModel3DView.from_presml(OpenXML.Model3D.Model3D())

    def model_assets(self):
        reference = PresentationML.from_file(REFERENCE)
        model, raster = (reference.scaffold[name] for name in
                         ('ppt/media/model3d1.glb', 'ppt/media/image1.png'))
        return (PresentationMLAsset(model.to_bytes(), model.content_type, 'glb'),
                PresentationMLAsset(raster.to_bytes(), raster.content_type, 'png'))

    def test_layout_owns_geometry_text_flow_and_crop(self):
        layout = PresentationMLElementLayout(position=(1, 2), size=(3, 4), units='in', rotation=30,
                                             flip_horizontal=True, padding=(.1, .2), alignment='center',
                                             vertical_alignment='bottom', crop={'left': .1, 'bottom': .2})
        element = layout.to_presml()
        self.assertEqual(element.find('off').attrs, {'x': 914400, 'y': 1828800})
        self.assertEqual(element.find('ext').attrs, {'cx': 2743200, 'cy': 3657600})
        self.assertEqual(element.attrs, {'rot': 1800000, 'flipH': True})
        self.assertEqual(layout.to_crop(), {'l': 10000, 'b': 20000})
        body = layout.to_body_properties()
        self.assertEqual(body.attrs['lIns'], 182880)
        self.assertEqual(body.attrs['tIns'], 91440)
        self.assertEqual(body.attrs['anchor'], 'b')
        self.assertEqual(layout.to_paragraph_properties().attrs['algn'], 'ctr')

    def test_line_appearance_replaces_handwritten_xml(self):
        expected = OpenXML.a.ln(OpenXML.a.solidFill(OpenXML.a.srgbClr(val='4472C4')), w=12700, cap='flat')
        expected.append(OpenXML.a.prstDash(val='solid'))
        self.assertEqual(xml_signature(PresentationMLLine(color='4472C4', width=1).to_presml().to_bytes()),
                         xml_signature(expected.to_bytes()))
        shape = PresentationMLShape('triangle', layout={'position': (700, 100), 'size': (60, 60)},
                                    appearance={'fill': None, 'line': {'color': '4472C4', 'width': 1}})
        builder = PowerPointPresentation(PresentationMLSlide(shape))
        root = builder.to_package()['ppt/slides/slide1.xml'].data
        self.assertIsNotNone(root.find('spPr').find('noFill'))
        self.assertEqual(root.find('ln').attrs['w'], 12700)
        self.assertEqual(root.find('srgbClr').attrs['val'], '4472C4')

    def test_primitive_options_are_split_and_explicit_layout_units_win(self):
        builder = PowerPointPresentation(units='in')
        text = builder.add_slide().draw_text('frequency', layout={'position': (10, 20), 'size': (200, 40), 'units': 'pt'},
                                            font_size=32, color='202020', align='ctr')
        self.assertIsInstance(text.prepare_layout(), PresentationMLElementLayout)
        self.assertIsInstance(text.prepare_appearance(), PresentationMLAppearance)
        self.assertNotIn('font_size', text.get_layout_options())
        self.assertNotIn('position', text.get_appearance_options())
        self.assertEqual(text.bounds, (127000, 254000, 2540000, 508000))
        root = builder.to_package()['ppt/slides/slide1.xml'].data
        shape = root.find('sp')
        self.assertIsNotNone(shape.find('spPr').find('noFill'))
        self.assertIsNone(shape.find('spPr').find('solidFill'))
        self.assertEqual(shape.find('rPr').attrs['sz'], 3200)
        self.assertEqual(shape.find('pPr').attrs['algn'], 'ctr')

    def test_wrappers_are_copied_at_construction_and_snapshot(self):
        layout = PresentationMLElementLayout(position=(10, 20), size=(200, 40))
        appearance = PresentationMLAppearance(font={'size': 24, 'color': '202020'})
        builder = PowerPointPresentation()
        drawn = builder.add_slide().draw_text('before', layout=layout, appearance=appearance)
        before = builder.to_bytes()
        layout.opts['position'] = (90, 90)
        appearance.font.opts['size'] = 50
        self.assertEqual(builder.to_bytes(), before)
        snapshot = builder.to_presentationml()
        drawn.layout.opts['position'] = (50, 50)
        self.assertEqual(snapshot.to_bytes(), before)
        self.assertNotEqual(builder.to_bytes(), before)

    def test_model_view_and_lights_need_no_openxml_constructors(self):
        model, png = self.model_assets()
        builder = PowerPointPresentation()
        builder.add_slide().draw_glb(model, fallback=png,
            layout={'position': (40, 80), 'size': (420, 320), 'view': {
                'camera': {'position': (3, 0, 0), 'up': (0, 0, 1)},
                'transform': {'center': (1, 2, 3), 'metres_per_unit': .03}}},
            appearance={'lighting': [{'type': 'ambient', 'color': (.5, .5, .5), 'illuminance': .5},
                                     {'type': 'point', 'position': (1, 2, 3), 'intensity': 10}]})
        root = builder.to_package()['ppt/slides/slide1.xml'].data
        self.assertEqual(root.find('camera').find('pos').attrs['x'], 3240000)
        self.assertEqual(root.find('preTrans').attrs, {'dx': -1080000, 'dy': -2160000, 'dz': -3240000})
        self.assertEqual(root.find('objViewport').attrs['viewportSz'], 4064000)
        self.assertIsNotNone(root.find('ambientLight'))
        self.assertIsNotNone(root.find('ptLight'))

    def test_animated_model_generates_reference_timing_with_allocated_shape_id(self):
        model, png = self.model_assets()
        builder = PowerPointPresentation()
        slide = builder.add_slide()
        slide.draw_text('earlier', position=(10, 10), width=200, height=30)
        slide.draw_glb(model, fallback=png, layout={'position': (40, 80), 'size': (420, 320)},
                       animation=PresentationMLAnimation(duration=2, loop=True))
        root = builder.to_package()['ppt/slides/slide1.xml'].data
        expected = PresentationML.from_file(REFERENCE)[1].structure.find('timing').clone()
        expected.find('spTgt').attrs = {'spid': '3'}
        self.assertEqual(xml_signature(root.find('timing').to_bytes()), xml_signature(expected.to_bytes()))
        self.assertEqual(root.find('animPr').attrs, {'length': 2000, 'count': 'indefinite'})
        self.assertEqual(builder.to_bytes(), builder.to_bytes())

    def test_multiple_animations_have_unique_time_nodes_and_shape_targets(self):
        model, png = self.model_assets()
        builder = PowerPointPresentation()
        slide = builder.add_slide()
        slide.draw_glb(model, fallback=png, position=(10, 10), width=200, height=200,
                       animation={'duration': 2}, id=7)
        slide.draw_glb(model, fallback=png, position=(250, 10), width=200, height=200,
                       animation={'duration': 3, 'loop': False})
        root = builder.to_package()['ppt/slides/slide1.xml'].data
        timing = root.find('timing')
        ids = [int(n.attrs['id']) for n in timing.walk() if n.local_tag == 'cTn']
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual([n.attrs['spid'] for n in timing.walk() if n.local_tag == 'spTgt'], [7, 2])
        self.assertEqual([n.attrs['dur'] for n in timing.walk() if n.local_tag == 'cTn' and n.attrs.get('dur') != 'indefinite'
                          and 'dur' in n.attrs], [2000, 3000])

    def test_new_animation_extends_imported_timing_without_id_collisions(self):
        model, png = self.model_assets()
        builder = PowerPointPresentation.from_file(REFERENCE)
        builder[1].draw_glb(model, fallback=png, position=(10, 10), width=200, height=200, animation={})
        timing = builder.to_package()['ppt/slides/slide2.xml'].data.find('timing')
        ids = [int(n.attrs['id']) for n in timing.walk() if n.local_tag == 'cTn']
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual([int(n.attrs['spid']) for n in timing.walk() if n.local_tag == 'spTgt'], [5, 3])

    def test_generic_editable_xml_accepts_layout_and_appearance(self):
        editable = OpenXML.Presentation.Shape(OpenXML.Presentation.ShapeProperties(
            OpenXML.Drawing.PresetGeometry(OpenXML.Drawing.AdjustValueList(), prst='triangle')))
        primitive = PresentationMLPrimitive(editable, position=(1, 2), width=30, height=40,
                                            appearance={'fill': 'ABCDEF'})
        root = primitive.to_presml()
        self.assertEqual(root.find('off').attrs, {'x': 12700, 'y': 25400})
        self.assertEqual(root.find('srgbClr').attrs['val'], 'ABCDEF')
        self.assertIsNone(editable.find('xfrm'))

    def test_appearance_color_opacity_and_invalid_wrapper_inputs(self):
        appearance = PresentationMLAppearance(fill='blue', opacity=.5, line={'color': (1, 0, 0), 'width': 2})
        fill, line = appearance.to_presml()
        self.assertEqual(fill.find('srgbClr').attrs['val'], '0000FF')
        self.assertEqual(fill.find('alpha').attrs['val'], 50000)
        self.assertEqual(line.find('srgbClr').attrs['val'], 'FF0000')
        with self.assertRaises(ValueError):
            PresentationMLLine(width=0)
        with self.assertRaises(ValueError):
            PresentationMLAppearance(font={'size': -1})
        with self.assertRaises(ValueError):
            PresentationMLElementLayout(position=(1, 2), size=(3, 4), alignment='sideways')
        with self.assertRaises(TypeError):
            PresentationMLShape('triangle', position=(1, 2), width=3, height=4, line_width_typo=1)


if __name__ == '__main__':
    unittest.main()

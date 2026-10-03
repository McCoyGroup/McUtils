"""The example deck expressed as declarative constructors.

Only opaque binary assets are read from example.pptx; no XML is read from it.
All XML parts, including geometry, 3D view/animation and SVG extensions, are
constructed here as McUtils.Jupyter.OpenXML types.
"""

import zipfile

from McUtils.Jupyter.OpenXML import OpenXML, OpenXMLPart, OpenXMLPackage, OpenXMLRelationship
from McUtils.Plots.PowerPoint import (PresentationML, PresentationMLSlide, PresentationMLPrimitive,
    PresentationMLText, PresentationMLShape, PresentationMLImage, PresentationMLModel3D)


def build_example(reference):
    with zipfile.ZipFile(reference) as archive:
        assets = [
            OpenXMLPart('docProps/thumbnail.jpeg', 'image/jpeg', archive.read('docProps/thumbnail.jpeg')),
            OpenXMLPart('ppt/media/image4.png', 'image/png', archive.read('ppt/media/image4.png')),
            OpenXMLPart('ppt/media/image3.svg', 'image/svg+xml', archive.read('ppt/media/image3.svg')),
            OpenXMLPart('ppt/media/image2.png', 'image/png', archive.read('ppt/media/image2.png')),
            OpenXMLPart('ppt/media/image1.png', 'image/png', archive.read('ppt/media/image1.png')),
            OpenXMLPart('ppt/media/model3d2.glb', 'model/gltf.binary', archive.read('ppt/media/model3d2.glb')),
            OpenXMLPart('ppt/media/model3d1.glb', 'model/gltf.binary', archive.read('ppt/media/model3d1.glb')),
        ]
    scaffold = OpenXMLPackage([
        *assets,
        OpenXMLPart('_rels/.rels', 'application/vnd.openxmlformats-package.relationships+xml',
            OpenXML.Relationships.Relationships(
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId3', 'Type': 'http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties', 'Target': 'docProps/core.xml'}
                ),
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId2', 'Type': 'http://schemas.openxmlformats.org/package/2006/relationships/metadata/thumbnail', 'Target': 'docProps/thumbnail.jpeg'}
                ),
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId1', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument', 'Target': 'ppt/presentation.xml'}
                ),
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId4', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties', 'Target': 'docProps/app.xml'}
                ),
                **{'xmlns': 'http://schemas.openxmlformats.org/package/2006/relationships'}
            )),
        OpenXMLPart('ppt/slides/_rels/slide3.xml.rels', 'application/vnd.openxmlformats-package.relationships+xml',
            OpenXML.Relationships.Relationships(
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId3', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image', 'Target': '../media/image4.png'}
                ),
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId2', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image', 'Target': '../media/image3.svg'}
                ),
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId1', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout', 'Target': '../slideLayouts/slideLayout2.xml'}
                ),
                **{'xmlns': 'http://schemas.openxmlformats.org/package/2006/relationships'}
            )),
        OpenXMLPart('ppt/slides/_rels/slide2.xml.rels', 'application/vnd.openxmlformats-package.relationships+xml',
            OpenXML.Relationships.Relationships(
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId3', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image', 'Target': '../media/image1.png'}
                ),
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId2', 'Type': 'http://schemas.microsoft.com/office/2017/06/relationships/model3d', 'Target': '../media/model3d1.glb'}
                ),
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId1', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout', 'Target': '../slideLayouts/slideLayout2.xml'}
                ),
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId5', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image', 'Target': '../media/image2.png'}
                ),
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId4', 'Type': 'http://schemas.microsoft.com/office/2017/06/relationships/model3d', 'Target': '../media/model3d2.glb'}
                ),
                **{'xmlns': 'http://schemas.openxmlformats.org/package/2006/relationships'}
            )),
        OpenXMLPart('ppt/slides/_rels/slide1.xml.rels', 'application/vnd.openxmlformats-package.relationships+xml',
            OpenXML.Relationships.Relationships(
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId1', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout', 'Target': '../slideLayouts/slideLayout1.xml'}
                ),
                **{'xmlns': 'http://schemas.openxmlformats.org/package/2006/relationships'}
            )),
        OpenXMLPart('ppt/_rels/presentation.xml.rels', 'application/vnd.openxmlformats-package.relationships+xml',
            OpenXML.Relationships.Relationships(
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId8', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/tableStyles', 'Target': 'tableStyles.xml'}
                ),
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId3', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide', 'Target': 'slides/slide2.xml'}
                ),
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId7', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme', 'Target': 'theme/theme1.xml'}
                ),
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId2', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide', 'Target': 'slides/slide1.xml'}
                ),
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId1', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster', 'Target': 'slideMasters/slideMaster1.xml'}
                ),
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId6', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/viewProps', 'Target': 'viewProps.xml'}
                ),
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId5', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/presProps', 'Target': 'presProps.xml'}
                ),
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId4', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide', 'Target': 'slides/slide3.xml'}
                ),
                **{'xmlns': 'http://schemas.openxmlformats.org/package/2006/relationships'}
            )),
        OpenXMLPart('ppt/slideLayouts/slideLayout2.xml', 'application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml',
            OpenXML.Presentation.SlideLayout(
                OpenXML.Presentation.CommonSlideData(
                    OpenXML.Presentation.ShapeTree(
                        OpenXML.Presentation.NonVisualGroupShapeProperties(
                            OpenXML.Presentation.NonVisualDrawingProperties(**{'id': '1', 'name': ''}),
                            OpenXML.Presentation.NonVisualGroupShapeDrawingProperties(),
                            OpenXML.Presentation.ApplicationNonVisualDrawingProperties()
                        ),
                        OpenXML.Presentation.GroupShapeProperties(
                            OpenXML.Drawing.Transform2D(
                                OpenXML.Drawing.Offset(**{'x': '0', 'y': '0'}),
                                OpenXML.Drawing.Extents(**{'cx': '0', 'cy': '0'}),
                                OpenXML.Drawing.ChildOffset(**{'x': '0', 'y': '0'}),
                                OpenXML.Drawing.ChildExtents(**{'cx': '0', 'cy': '0'})
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{BF7B05E2-7CA3-C862-7F7B-A83F0634D575}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '2', 'name': 'Title 1'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(**{'type': 'title'})
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Click to edit Master title style')
                                    )
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{D88EDF50-BFDB-4B0A-C450-9A61E4BD2B27}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '3', 'name': 'Content Placeholder 2'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(**{'idx': '1'})
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '0'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Click to edit Master text styles')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '1'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Second level')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '2'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Third level')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '3'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Fourth level')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '4'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Fifth level')
                                    )
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{70928638-1F00-A537-768C-81115C1108D9}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '4', 'name': 'Date Placeholder 3'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'dt', 'sz': 'half', 'idx': '10'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Field(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US', 'smtClean': '0'}),
                                        OpenXML.Drawing.Text('10/3/26'),
                                        **{'id': '{D68DF6A3-B8D2-1244-AA57-60AE5089C008}', 'type': 'datetimeFigureOut'}
                                    ),
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{0BF0570E-3B15-B404-574E-65C2D5C2F195}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '5', 'name': 'Footer Placeholder 4'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'ftr', 'sz': 'quarter', 'idx': '11'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{4438AAF4-E1B3-7869-84A0-EFDC9E6B17FB}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '6', 'name': 'Slide Number Placeholder 5'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'sldNum', 'sz': 'quarter', 'idx': '12'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Field(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US', 'smtClean': '0'}),
                                        OpenXML.Drawing.Text('‹#›'),
                                        **{'id': '{190F7A14-BFAA-8642-8063-7C43CC189FC6}', 'type': 'slidenum'}
                                    ),
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        )
                    ),
                    OpenXML.Presentation.ExtensionListWithModification(
                        OpenXML.Presentation.Extension(
                            OpenXML.Presentation2010.CreationId(
                                **{'val': '1717761096', 'xmlns:p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main'}
                            ),
                            **{'uri': '{BB962C8B-B14F-4D97-AF65-F5344CB8AC3E}'}
                        )
                    ),
                    **{'name': 'Title and Content'}
                ),
                OpenXML.Presentation.ColorMapOverride(OpenXML.Drawing.MasterColorMapping()),
                **{'type': 'obj', 'preserve': '1', 'xmlns:a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'xmlns:r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships', 'xmlns:p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
            )),
        OpenXMLPart('ppt/slideLayouts/slideLayout3.xml', 'application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml',
            OpenXML.Presentation.SlideLayout(
                OpenXML.Presentation.CommonSlideData(
                    OpenXML.Presentation.ShapeTree(
                        OpenXML.Presentation.NonVisualGroupShapeProperties(
                            OpenXML.Presentation.NonVisualDrawingProperties(**{'id': '1', 'name': ''}),
                            OpenXML.Presentation.NonVisualGroupShapeDrawingProperties(),
                            OpenXML.Presentation.ApplicationNonVisualDrawingProperties()
                        ),
                        OpenXML.Presentation.GroupShapeProperties(
                            OpenXML.Drawing.Transform2D(
                                OpenXML.Drawing.Offset(**{'x': '0', 'y': '0'}),
                                OpenXML.Drawing.Extents(**{'cx': '0', 'cy': '0'}),
                                OpenXML.Drawing.ChildOffset(**{'x': '0', 'y': '0'}),
                                OpenXML.Drawing.ChildExtents(**{'cx': '0', 'cy': '0'})
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{D9DF7CA6-3E04-0174-F723-0282092399F5}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '2', 'name': 'Title 1'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(**{'type': 'title'})
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(
                                OpenXML.Drawing.Transform2D(
                                    OpenXML.Drawing.Offset(**{'x': '831850', 'y': '1709738'}),
                                    OpenXML.Drawing.Extents(**{'cx': '10515600', 'cy': '2852737'})
                                )
                            ),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(**{'anchor': 'b'}),
                                OpenXML.Drawing.ListStyle(
                                    OpenXML.Drawing.Level1ParagraphProperties(
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '6000'})
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Click to edit Master title style')
                                    )
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{0257830E-E896-64DD-8307-0D33AA47CBBF}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '3', 'name': 'Text Placeholder 2'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(**{'type': 'body', 'idx': '1'})
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(
                                OpenXML.Drawing.Transform2D(
                                    OpenXML.Drawing.Offset(**{'x': '831850', 'y': '4589463'}),
                                    OpenXML.Drawing.Extents(**{'cx': '10515600', 'cy': '1500187'})
                                )
                            ),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(
                                    OpenXML.Drawing.Level1ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(
                                            OpenXML.Drawing.SolidFill(
                                                OpenXML.Drawing.SchemeColor(
                                                    OpenXML.Drawing.Tint(**{'val': '82000'}),
                                                    **{'val': 'tx1'}
                                                )
                                            ),
                                            **{'sz': '2400'}
                                        ),
                                        **{'marL': '0', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level2ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(
                                            OpenXML.Drawing.SolidFill(
                                                OpenXML.Drawing.SchemeColor(
                                                    OpenXML.Drawing.Tint(**{'val': '82000'}),
                                                    **{'val': 'tx1'}
                                                )
                                            ),
                                            **{'sz': '2000'}
                                        ),
                                        **{'marL': '457200', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level3ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(
                                            OpenXML.Drawing.SolidFill(
                                                OpenXML.Drawing.SchemeColor(
                                                    OpenXML.Drawing.Tint(**{'val': '82000'}),
                                                    **{'val': 'tx1'}
                                                )
                                            ),
                                            **{'sz': '1800'}
                                        ),
                                        **{'marL': '914400', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level4ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(
                                            OpenXML.Drawing.SolidFill(
                                                OpenXML.Drawing.SchemeColor(
                                                    OpenXML.Drawing.Tint(**{'val': '82000'}),
                                                    **{'val': 'tx1'}
                                                )
                                            ),
                                            **{'sz': '1600'}
                                        ),
                                        **{'marL': '1371600', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level5ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(
                                            OpenXML.Drawing.SolidFill(
                                                OpenXML.Drawing.SchemeColor(
                                                    OpenXML.Drawing.Tint(**{'val': '82000'}),
                                                    **{'val': 'tx1'}
                                                )
                                            ),
                                            **{'sz': '1600'}
                                        ),
                                        **{'marL': '1828800', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level6ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(
                                            OpenXML.Drawing.SolidFill(
                                                OpenXML.Drawing.SchemeColor(
                                                    OpenXML.Drawing.Tint(**{'val': '82000'}),
                                                    **{'val': 'tx1'}
                                                )
                                            ),
                                            **{'sz': '1600'}
                                        ),
                                        **{'marL': '2286000', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level7ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(
                                            OpenXML.Drawing.SolidFill(
                                                OpenXML.Drawing.SchemeColor(
                                                    OpenXML.Drawing.Tint(**{'val': '82000'}),
                                                    **{'val': 'tx1'}
                                                )
                                            ),
                                            **{'sz': '1600'}
                                        ),
                                        **{'marL': '2743200', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level8ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(
                                            OpenXML.Drawing.SolidFill(
                                                OpenXML.Drawing.SchemeColor(
                                                    OpenXML.Drawing.Tint(**{'val': '82000'}),
                                                    **{'val': 'tx1'}
                                                )
                                            ),
                                            **{'sz': '1600'}
                                        ),
                                        **{'marL': '3200400', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level9ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(
                                            OpenXML.Drawing.SolidFill(
                                                OpenXML.Drawing.SchemeColor(
                                                    OpenXML.Drawing.Tint(**{'val': '82000'}),
                                                    **{'val': 'tx1'}
                                                )
                                            ),
                                            **{'sz': '1600'}
                                        ),
                                        **{'marL': '3657600', 'indent': '0'}
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '0'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Click to edit Master text styles')
                                    )
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{C138B554-C8AE-1D4B-4FEB-5F63E4561A41}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '4', 'name': 'Date Placeholder 3'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'dt', 'sz': 'half', 'idx': '10'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Field(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US', 'smtClean': '0'}),
                                        OpenXML.Drawing.Text('10/3/26'),
                                        **{'id': '{D68DF6A3-B8D2-1244-AA57-60AE5089C008}', 'type': 'datetimeFigureOut'}
                                    ),
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{A2852742-03FA-3478-AD2B-B1EB920EF3DE}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '5', 'name': 'Footer Placeholder 4'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'ftr', 'sz': 'quarter', 'idx': '11'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{68D4D3DD-BF20-6D8B-B0F5-5A99EC5F4381}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '6', 'name': 'Slide Number Placeholder 5'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'sldNum', 'sz': 'quarter', 'idx': '12'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Field(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US', 'smtClean': '0'}),
                                        OpenXML.Drawing.Text('‹#›'),
                                        **{'id': '{190F7A14-BFAA-8642-8063-7C43CC189FC6}', 'type': 'slidenum'}
                                    ),
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        )
                    ),
                    OpenXML.Presentation.ExtensionListWithModification(
                        OpenXML.Presentation.Extension(
                            OpenXML.Presentation2010.CreationId(
                                **{'val': '2434233494', 'xmlns:p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main'}
                            ),
                            **{'uri': '{BB962C8B-B14F-4D97-AF65-F5344CB8AC3E}'}
                        )
                    ),
                    **{'name': 'Section Header'}
                ),
                OpenXML.Presentation.ColorMapOverride(OpenXML.Drawing.MasterColorMapping()),
                **{'type': 'secHead', 'preserve': '1', 'xmlns:a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'xmlns:r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships', 'xmlns:p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
            )),
        OpenXMLPart('ppt/slideLayouts/slideLayout4.xml', 'application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml',
            OpenXML.Presentation.SlideLayout(
                OpenXML.Presentation.CommonSlideData(
                    OpenXML.Presentation.ShapeTree(
                        OpenXML.Presentation.NonVisualGroupShapeProperties(
                            OpenXML.Presentation.NonVisualDrawingProperties(**{'id': '1', 'name': ''}),
                            OpenXML.Presentation.NonVisualGroupShapeDrawingProperties(),
                            OpenXML.Presentation.ApplicationNonVisualDrawingProperties()
                        ),
                        OpenXML.Presentation.GroupShapeProperties(
                            OpenXML.Drawing.Transform2D(
                                OpenXML.Drawing.Offset(**{'x': '0', 'y': '0'}),
                                OpenXML.Drawing.Extents(**{'cx': '0', 'cy': '0'}),
                                OpenXML.Drawing.ChildOffset(**{'x': '0', 'y': '0'}),
                                OpenXML.Drawing.ChildExtents(**{'cx': '0', 'cy': '0'})
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{5967BCC8-EB46-BD07-2D00-0A8E39DAF0B8}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '2', 'name': 'Title 1'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(**{'type': 'title'})
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Click to edit Master title style')
                                    )
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{DAAA34F6-7FA8-9AD4-472E-E410840E86D4}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '3', 'name': 'Content Placeholder 2'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(**{'sz': 'half', 'idx': '1'})
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(
                                OpenXML.Drawing.Transform2D(
                                    OpenXML.Drawing.Offset(**{'x': '838200', 'y': '1825625'}),
                                    OpenXML.Drawing.Extents(**{'cx': '5181600', 'cy': '4351338'})
                                )
                            ),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '0'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Click to edit Master text styles')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '1'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Second level')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '2'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Third level')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '3'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Fourth level')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '4'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Fifth level')
                                    )
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{2B1A9B9A-0DD5-5539-637F-46CC53A83F69}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '4', 'name': 'Content Placeholder 3'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(**{'sz': 'half', 'idx': '2'})
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(
                                OpenXML.Drawing.Transform2D(
                                    OpenXML.Drawing.Offset(**{'x': '6172200', 'y': '1825625'}),
                                    OpenXML.Drawing.Extents(**{'cx': '5181600', 'cy': '4351338'})
                                )
                            ),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '0'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Click to edit Master text styles')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '1'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Second level')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '2'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Third level')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '3'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Fourth level')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '4'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Fifth level')
                                    )
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{AA7A23F8-A9BA-EC7B-2B10-3899667BC539}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '5', 'name': 'Date Placeholder 4'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'dt', 'sz': 'half', 'idx': '10'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Field(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US', 'smtClean': '0'}),
                                        OpenXML.Drawing.Text('10/3/26'),
                                        **{'id': '{D68DF6A3-B8D2-1244-AA57-60AE5089C008}', 'type': 'datetimeFigureOut'}
                                    ),
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{D6E715EC-FD74-7112-5DD5-784C8DAD7B99}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '6', 'name': 'Footer Placeholder 5'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'ftr', 'sz': 'quarter', 'idx': '11'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{A20E96CD-3ABC-B8C1-0540-84CC48B9EE9D}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '7', 'name': 'Slide Number Placeholder 6'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'sldNum', 'sz': 'quarter', 'idx': '12'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Field(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US', 'smtClean': '0'}),
                                        OpenXML.Drawing.Text('‹#›'),
                                        **{'id': '{190F7A14-BFAA-8642-8063-7C43CC189FC6}', 'type': 'slidenum'}
                                    ),
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        )
                    ),
                    OpenXML.Presentation.ExtensionListWithModification(
                        OpenXML.Presentation.Extension(
                            OpenXML.Presentation2010.CreationId(
                                **{'val': '1275724577', 'xmlns:p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main'}
                            ),
                            **{'uri': '{BB962C8B-B14F-4D97-AF65-F5344CB8AC3E}'}
                        )
                    ),
                    **{'name': 'Two Content'}
                ),
                OpenXML.Presentation.ColorMapOverride(OpenXML.Drawing.MasterColorMapping()),
                **{'type': 'twoObj', 'preserve': '1', 'xmlns:a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'xmlns:r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships', 'xmlns:p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
            )),
        OpenXMLPart('ppt/slideLayouts/slideLayout5.xml', 'application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml',
            OpenXML.Presentation.SlideLayout(
                OpenXML.Presentation.CommonSlideData(
                    OpenXML.Presentation.ShapeTree(
                        OpenXML.Presentation.NonVisualGroupShapeProperties(
                            OpenXML.Presentation.NonVisualDrawingProperties(**{'id': '1', 'name': ''}),
                            OpenXML.Presentation.NonVisualGroupShapeDrawingProperties(),
                            OpenXML.Presentation.ApplicationNonVisualDrawingProperties()
                        ),
                        OpenXML.Presentation.GroupShapeProperties(
                            OpenXML.Drawing.Transform2D(
                                OpenXML.Drawing.Offset(**{'x': '0', 'y': '0'}),
                                OpenXML.Drawing.Extents(**{'cx': '0', 'cy': '0'}),
                                OpenXML.Drawing.ChildOffset(**{'x': '0', 'y': '0'}),
                                OpenXML.Drawing.ChildExtents(**{'cx': '0', 'cy': '0'})
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{0BAF97B6-5FD8-500E-ED49-42A4D282F49D}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '2', 'name': 'Title 1'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(**{'type': 'title'})
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(
                                OpenXML.Drawing.Transform2D(
                                    OpenXML.Drawing.Offset(**{'x': '839788', 'y': '365125'}),
                                    OpenXML.Drawing.Extents(**{'cx': '10515600', 'cy': '1325563'})
                                )
                            ),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Click to edit Master title style')
                                    )
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{61950829-E584-32A7-99D5-F22FF9AA192A}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '3', 'name': 'Text Placeholder 2'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(**{'type': 'body', 'idx': '1'})
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(
                                OpenXML.Drawing.Transform2D(
                                    OpenXML.Drawing.Offset(**{'x': '839788', 'y': '1681163'}),
                                    OpenXML.Drawing.Extents(**{'cx': '5157787', 'cy': '823912'})
                                )
                            ),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(**{'anchor': 'b'}),
                                OpenXML.Drawing.ListStyle(
                                    OpenXML.Drawing.Level1ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '2400', 'b': '1'}),
                                        **{'marL': '0', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level2ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '2000', 'b': '1'}),
                                        **{'marL': '457200', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level3ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1800', 'b': '1'}),
                                        **{'marL': '914400', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level4ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1600', 'b': '1'}),
                                        **{'marL': '1371600', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level5ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1600', 'b': '1'}),
                                        **{'marL': '1828800', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level6ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1600', 'b': '1'}),
                                        **{'marL': '2286000', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level7ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1600', 'b': '1'}),
                                        **{'marL': '2743200', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level8ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1600', 'b': '1'}),
                                        **{'marL': '3200400', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level9ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1600', 'b': '1'}),
                                        **{'marL': '3657600', 'indent': '0'}
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '0'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Click to edit Master text styles')
                                    )
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{B7E9EA74-563C-9BCE-EF24-4AF43B403501}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '4', 'name': 'Content Placeholder 3'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(**{'sz': 'half', 'idx': '2'})
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(
                                OpenXML.Drawing.Transform2D(
                                    OpenXML.Drawing.Offset(**{'x': '839788', 'y': '2505075'}),
                                    OpenXML.Drawing.Extents(**{'cx': '5157787', 'cy': '3684588'})
                                )
                            ),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '0'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Click to edit Master text styles')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '1'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Second level')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '2'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Third level')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '3'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Fourth level')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '4'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Fifth level')
                                    )
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{E56C6F57-BE71-2C73-246B-8ADDA40F07EA}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '5', 'name': 'Text Placeholder 4'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'body', 'sz': 'quarter', 'idx': '3'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(
                                OpenXML.Drawing.Transform2D(
                                    OpenXML.Drawing.Offset(**{'x': '6172200', 'y': '1681163'}),
                                    OpenXML.Drawing.Extents(**{'cx': '5183188', 'cy': '823912'})
                                )
                            ),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(**{'anchor': 'b'}),
                                OpenXML.Drawing.ListStyle(
                                    OpenXML.Drawing.Level1ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '2400', 'b': '1'}),
                                        **{'marL': '0', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level2ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '2000', 'b': '1'}),
                                        **{'marL': '457200', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level3ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1800', 'b': '1'}),
                                        **{'marL': '914400', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level4ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1600', 'b': '1'}),
                                        **{'marL': '1371600', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level5ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1600', 'b': '1'}),
                                        **{'marL': '1828800', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level6ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1600', 'b': '1'}),
                                        **{'marL': '2286000', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level7ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1600', 'b': '1'}),
                                        **{'marL': '2743200', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level8ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1600', 'b': '1'}),
                                        **{'marL': '3200400', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level9ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1600', 'b': '1'}),
                                        **{'marL': '3657600', 'indent': '0'}
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '0'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Click to edit Master text styles')
                                    )
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{3598BC2C-B204-1AC1-1585-F100A3D6D4EC}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '6', 'name': 'Content Placeholder 5'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(**{'sz': 'quarter', 'idx': '4'})
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(
                                OpenXML.Drawing.Transform2D(
                                    OpenXML.Drawing.Offset(**{'x': '6172200', 'y': '2505075'}),
                                    OpenXML.Drawing.Extents(**{'cx': '5183188', 'cy': '3684588'})
                                )
                            ),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '0'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Click to edit Master text styles')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '1'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Second level')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '2'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Third level')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '3'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Fourth level')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '4'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Fifth level')
                                    )
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{5CF0AE8E-D1E5-F5F1-E750-B8E30195B077}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '7', 'name': 'Date Placeholder 6'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'dt', 'sz': 'half', 'idx': '10'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Field(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US', 'smtClean': '0'}),
                                        OpenXML.Drawing.Text('10/3/26'),
                                        **{'id': '{D68DF6A3-B8D2-1244-AA57-60AE5089C008}', 'type': 'datetimeFigureOut'}
                                    ),
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{630E2E00-0D12-5F15-5AF0-C61DFF7A6C83}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '8', 'name': 'Footer Placeholder 7'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'ftr', 'sz': 'quarter', 'idx': '11'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{AB79D8AA-932A-DF27-72BF-636A2ED55DB6}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '9', 'name': 'Slide Number Placeholder 8'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'sldNum', 'sz': 'quarter', 'idx': '12'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Field(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US', 'smtClean': '0'}),
                                        OpenXML.Drawing.Text('‹#›'),
                                        **{'id': '{190F7A14-BFAA-8642-8063-7C43CC189FC6}', 'type': 'slidenum'}
                                    ),
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        )
                    ),
                    OpenXML.Presentation.ExtensionListWithModification(
                        OpenXML.Presentation.Extension(
                            OpenXML.Presentation2010.CreationId(
                                **{'val': '1802548630', 'xmlns:p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main'}
                            ),
                            **{'uri': '{BB962C8B-B14F-4D97-AF65-F5344CB8AC3E}'}
                        )
                    ),
                    **{'name': 'Comparison'}
                ),
                OpenXML.Presentation.ColorMapOverride(OpenXML.Drawing.MasterColorMapping()),
                **{'type': 'twoTxTwoObj', 'preserve': '1', 'xmlns:a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'xmlns:r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships', 'xmlns:p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
            )),
        OpenXMLPart('ppt/slideLayouts/slideLayout6.xml', 'application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml',
            OpenXML.Presentation.SlideLayout(
                OpenXML.Presentation.CommonSlideData(
                    OpenXML.Presentation.ShapeTree(
                        OpenXML.Presentation.NonVisualGroupShapeProperties(
                            OpenXML.Presentation.NonVisualDrawingProperties(**{'id': '1', 'name': ''}),
                            OpenXML.Presentation.NonVisualGroupShapeDrawingProperties(),
                            OpenXML.Presentation.ApplicationNonVisualDrawingProperties()
                        ),
                        OpenXML.Presentation.GroupShapeProperties(
                            OpenXML.Drawing.Transform2D(
                                OpenXML.Drawing.Offset(**{'x': '0', 'y': '0'}),
                                OpenXML.Drawing.Extents(**{'cx': '0', 'cy': '0'}),
                                OpenXML.Drawing.ChildOffset(**{'x': '0', 'y': '0'}),
                                OpenXML.Drawing.ChildExtents(**{'cx': '0', 'cy': '0'})
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{28EAD0F0-CD91-E904-8E8D-4A95EC028BDB}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '2', 'name': 'Title 1'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(**{'type': 'title'})
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Click to edit Master title style')
                                    )
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{EDC1AC7D-9CEB-7D07-23E0-74CC6D4C0C91}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '3', 'name': 'Date Placeholder 2'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'dt', 'sz': 'half', 'idx': '10'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Field(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US', 'smtClean': '0'}),
                                        OpenXML.Drawing.Text('10/3/26'),
                                        **{'id': '{D68DF6A3-B8D2-1244-AA57-60AE5089C008}', 'type': 'datetimeFigureOut'}
                                    ),
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{E50B71DB-EBB0-9E63-3D5B-D2A88F0D5527}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '4', 'name': 'Footer Placeholder 3'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'ftr', 'sz': 'quarter', 'idx': '11'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{9061C451-495F-0E17-E8CC-F337D34FA827}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '5', 'name': 'Slide Number Placeholder 4'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'sldNum', 'sz': 'quarter', 'idx': '12'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Field(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US', 'smtClean': '0'}),
                                        OpenXML.Drawing.Text('‹#›'),
                                        **{'id': '{190F7A14-BFAA-8642-8063-7C43CC189FC6}', 'type': 'slidenum'}
                                    ),
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        )
                    ),
                    OpenXML.Presentation.ExtensionListWithModification(
                        OpenXML.Presentation.Extension(
                            OpenXML.Presentation2010.CreationId(
                                **{'val': '3085961687', 'xmlns:p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main'}
                            ),
                            **{'uri': '{BB962C8B-B14F-4D97-AF65-F5344CB8AC3E}'}
                        )
                    ),
                    **{'name': 'Title Only'}
                ),
                OpenXML.Presentation.ColorMapOverride(OpenXML.Drawing.MasterColorMapping()),
                **{'type': 'titleOnly', 'preserve': '1', 'xmlns:a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'xmlns:r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships', 'xmlns:p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
            )),
        OpenXMLPart('ppt/slideLayouts/slideLayout7.xml', 'application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml',
            OpenXML.Presentation.SlideLayout(
                OpenXML.Presentation.CommonSlideData(
                    OpenXML.Presentation.ShapeTree(
                        OpenXML.Presentation.NonVisualGroupShapeProperties(
                            OpenXML.Presentation.NonVisualDrawingProperties(**{'id': '1', 'name': ''}),
                            OpenXML.Presentation.NonVisualGroupShapeDrawingProperties(),
                            OpenXML.Presentation.ApplicationNonVisualDrawingProperties()
                        ),
                        OpenXML.Presentation.GroupShapeProperties(
                            OpenXML.Drawing.Transform2D(
                                OpenXML.Drawing.Offset(**{'x': '0', 'y': '0'}),
                                OpenXML.Drawing.Extents(**{'cx': '0', 'cy': '0'}),
                                OpenXML.Drawing.ChildOffset(**{'x': '0', 'y': '0'}),
                                OpenXML.Drawing.ChildExtents(**{'cx': '0', 'cy': '0'})
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{4666A4D5-5E28-389F-1F60-FB162C36FBC8}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '2', 'name': 'Date Placeholder 1'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'dt', 'sz': 'half', 'idx': '10'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Field(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US', 'smtClean': '0'}),
                                        OpenXML.Drawing.Text('10/3/26'),
                                        **{'id': '{D68DF6A3-B8D2-1244-AA57-60AE5089C008}', 'type': 'datetimeFigureOut'}
                                    ),
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{F4E99428-D663-CE42-C7BD-170610A61195}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '3', 'name': 'Footer Placeholder 2'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'ftr', 'sz': 'quarter', 'idx': '11'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{9DA28F5C-BFE3-2373-4899-7508D152DC94}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '4', 'name': 'Slide Number Placeholder 3'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'sldNum', 'sz': 'quarter', 'idx': '12'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Field(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US', 'smtClean': '0'}),
                                        OpenXML.Drawing.Text('‹#›'),
                                        **{'id': '{190F7A14-BFAA-8642-8063-7C43CC189FC6}', 'type': 'slidenum'}
                                    ),
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        )
                    ),
                    OpenXML.Presentation.ExtensionListWithModification(
                        OpenXML.Presentation.Extension(
                            OpenXML.Presentation2010.CreationId(
                                **{'val': '2889861316', 'xmlns:p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main'}
                            ),
                            **{'uri': '{BB962C8B-B14F-4D97-AF65-F5344CB8AC3E}'}
                        )
                    ),
                    **{'name': 'Blank'}
                ),
                OpenXML.Presentation.ColorMapOverride(OpenXML.Drawing.MasterColorMapping()),
                **{'type': 'blank', 'preserve': '1', 'xmlns:a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'xmlns:r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships', 'xmlns:p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
            )),
        OpenXMLPart('ppt/slideLayouts/slideLayout8.xml', 'application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml',
            OpenXML.Presentation.SlideLayout(
                OpenXML.Presentation.CommonSlideData(
                    OpenXML.Presentation.ShapeTree(
                        OpenXML.Presentation.NonVisualGroupShapeProperties(
                            OpenXML.Presentation.NonVisualDrawingProperties(**{'id': '1', 'name': ''}),
                            OpenXML.Presentation.NonVisualGroupShapeDrawingProperties(),
                            OpenXML.Presentation.ApplicationNonVisualDrawingProperties()
                        ),
                        OpenXML.Presentation.GroupShapeProperties(
                            OpenXML.Drawing.Transform2D(
                                OpenXML.Drawing.Offset(**{'x': '0', 'y': '0'}),
                                OpenXML.Drawing.Extents(**{'cx': '0', 'cy': '0'}),
                                OpenXML.Drawing.ChildOffset(**{'x': '0', 'y': '0'}),
                                OpenXML.Drawing.ChildExtents(**{'cx': '0', 'cy': '0'})
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{5FB57B52-B822-CBDC-B0DD-DCD34B9E6EC7}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '2', 'name': 'Title 1'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(**{'type': 'title'})
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(
                                OpenXML.Drawing.Transform2D(
                                    OpenXML.Drawing.Offset(**{'x': '839788', 'y': '457200'}),
                                    OpenXML.Drawing.Extents(**{'cx': '3932237', 'cy': '1600200'})
                                )
                            ),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(**{'anchor': 'b'}),
                                OpenXML.Drawing.ListStyle(
                                    OpenXML.Drawing.Level1ParagraphProperties(
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '3200'})
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Click to edit Master title style')
                                    )
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{F57B45FE-E907-3902-F943-E4855F8914C8}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '3', 'name': 'Content Placeholder 2'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(**{'idx': '1'})
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(
                                OpenXML.Drawing.Transform2D(
                                    OpenXML.Drawing.Offset(**{'x': '5183188', 'y': '987425'}),
                                    OpenXML.Drawing.Extents(**{'cx': '6172200', 'cy': '4873625'})
                                )
                            ),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(
                                    OpenXML.Drawing.Level1ParagraphProperties(
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '3200'})
                                    ),
                                    OpenXML.Drawing.Level2ParagraphProperties(
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '2800'})
                                    ),
                                    OpenXML.Drawing.Level3ParagraphProperties(
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '2400'})
                                    ),
                                    OpenXML.Drawing.Level4ParagraphProperties(
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '2000'})
                                    ),
                                    OpenXML.Drawing.Level5ParagraphProperties(
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '2000'})
                                    ),
                                    OpenXML.Drawing.Level6ParagraphProperties(
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '2000'})
                                    ),
                                    OpenXML.Drawing.Level7ParagraphProperties(
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '2000'})
                                    ),
                                    OpenXML.Drawing.Level8ParagraphProperties(
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '2000'})
                                    ),
                                    OpenXML.Drawing.Level9ParagraphProperties(
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '2000'})
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '0'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Click to edit Master text styles')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '1'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Second level')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '2'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Third level')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '3'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Fourth level')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '4'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Fifth level')
                                    )
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{9CDB780D-8850-A1D9-AE97-9901138BDF75}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '4', 'name': 'Text Placeholder 3'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'body', 'sz': 'half', 'idx': '2'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(
                                OpenXML.Drawing.Transform2D(
                                    OpenXML.Drawing.Offset(**{'x': '839788', 'y': '2057400'}),
                                    OpenXML.Drawing.Extents(**{'cx': '3932237', 'cy': '3811588'})
                                )
                            ),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(
                                    OpenXML.Drawing.Level1ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1600'}),
                                        **{'marL': '0', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level2ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1400'}),
                                        **{'marL': '457200', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level3ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1200'}),
                                        **{'marL': '914400', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level4ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1000'}),
                                        **{'marL': '1371600', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level5ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1000'}),
                                        **{'marL': '1828800', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level6ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1000'}),
                                        **{'marL': '2286000', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level7ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1000'}),
                                        **{'marL': '2743200', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level8ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1000'}),
                                        **{'marL': '3200400', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level9ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1000'}),
                                        **{'marL': '3657600', 'indent': '0'}
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '0'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Click to edit Master text styles')
                                    )
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{6E1F9578-8F0A-FC10-4760-0EAEA697F6D9}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '5', 'name': 'Date Placeholder 4'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'dt', 'sz': 'half', 'idx': '10'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Field(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US', 'smtClean': '0'}),
                                        OpenXML.Drawing.Text('10/3/26'),
                                        **{'id': '{D68DF6A3-B8D2-1244-AA57-60AE5089C008}', 'type': 'datetimeFigureOut'}
                                    ),
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{8FC6934C-2CD2-49CD-9B2A-7D9981524203}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '6', 'name': 'Footer Placeholder 5'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'ftr', 'sz': 'quarter', 'idx': '11'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{FDF6ED84-EDF9-83D9-A5ED-94E61249DA26}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '7', 'name': 'Slide Number Placeholder 6'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'sldNum', 'sz': 'quarter', 'idx': '12'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Field(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US', 'smtClean': '0'}),
                                        OpenXML.Drawing.Text('‹#›'),
                                        **{'id': '{190F7A14-BFAA-8642-8063-7C43CC189FC6}', 'type': 'slidenum'}
                                    ),
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        )
                    ),
                    OpenXML.Presentation.ExtensionListWithModification(
                        OpenXML.Presentation.Extension(
                            OpenXML.Presentation2010.CreationId(
                                **{'val': '1713868369', 'xmlns:p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main'}
                            ),
                            **{'uri': '{BB962C8B-B14F-4D97-AF65-F5344CB8AC3E}'}
                        )
                    ),
                    **{'name': 'Content with Caption'}
                ),
                OpenXML.Presentation.ColorMapOverride(OpenXML.Drawing.MasterColorMapping()),
                **{'type': 'objTx', 'preserve': '1', 'xmlns:a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'xmlns:r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships', 'xmlns:p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
            )),
        OpenXMLPart('ppt/slideLayouts/slideLayout9.xml', 'application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml',
            OpenXML.Presentation.SlideLayout(
                OpenXML.Presentation.CommonSlideData(
                    OpenXML.Presentation.ShapeTree(
                        OpenXML.Presentation.NonVisualGroupShapeProperties(
                            OpenXML.Presentation.NonVisualDrawingProperties(**{'id': '1', 'name': ''}),
                            OpenXML.Presentation.NonVisualGroupShapeDrawingProperties(),
                            OpenXML.Presentation.ApplicationNonVisualDrawingProperties()
                        ),
                        OpenXML.Presentation.GroupShapeProperties(
                            OpenXML.Drawing.Transform2D(
                                OpenXML.Drawing.Offset(**{'x': '0', 'y': '0'}),
                                OpenXML.Drawing.Extents(**{'cx': '0', 'cy': '0'}),
                                OpenXML.Drawing.ChildOffset(**{'x': '0', 'y': '0'}),
                                OpenXML.Drawing.ChildExtents(**{'cx': '0', 'cy': '0'})
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{E1F131D9-14A4-58CD-7FBA-200952911F9C}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '2', 'name': 'Title 1'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(**{'type': 'title'})
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(
                                OpenXML.Drawing.Transform2D(
                                    OpenXML.Drawing.Offset(**{'x': '839788', 'y': '457200'}),
                                    OpenXML.Drawing.Extents(**{'cx': '3932237', 'cy': '1600200'})
                                )
                            ),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(**{'anchor': 'b'}),
                                OpenXML.Drawing.ListStyle(
                                    OpenXML.Drawing.Level1ParagraphProperties(
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '3200'})
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Click to edit Master title style')
                                    )
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{688A4F8C-E18C-3BA3-0D58-5B0AE6094346}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '3', 'name': 'Picture Placeholder 2'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(**{'type': 'pic', 'idx': '1'})
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(
                                OpenXML.Drawing.Transform2D(
                                    OpenXML.Drawing.Offset(**{'x': '5183188', 'y': '987425'}),
                                    OpenXML.Drawing.Extents(**{'cx': '6172200', 'cy': '4873625'})
                                )
                            ),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(
                                    OpenXML.Drawing.Level1ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '3200'}),
                                        **{'marL': '0', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level2ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '2800'}),
                                        **{'marL': '457200', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level3ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '2400'}),
                                        **{'marL': '914400', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level4ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '2000'}),
                                        **{'marL': '1371600', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level5ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '2000'}),
                                        **{'marL': '1828800', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level6ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '2000'}),
                                        **{'marL': '2286000', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level7ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '2000'}),
                                        **{'marL': '2743200', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level8ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '2000'}),
                                        **{'marL': '3200400', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level9ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '2000'}),
                                        **{'marL': '3657600', 'indent': '0'}
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{C398707B-55AD-00DD-CCD3-CBF50AA38987}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '4', 'name': 'Text Placeholder 3'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'body', 'sz': 'half', 'idx': '2'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(
                                OpenXML.Drawing.Transform2D(
                                    OpenXML.Drawing.Offset(**{'x': '839788', 'y': '2057400'}),
                                    OpenXML.Drawing.Extents(**{'cx': '3932237', 'cy': '3811588'})
                                )
                            ),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(
                                    OpenXML.Drawing.Level1ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1600'}),
                                        **{'marL': '0', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level2ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1400'}),
                                        **{'marL': '457200', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level3ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1200'}),
                                        **{'marL': '914400', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level4ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1000'}),
                                        **{'marL': '1371600', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level5ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1000'}),
                                        **{'marL': '1828800', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level6ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1000'}),
                                        **{'marL': '2286000', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level7ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1000'}),
                                        **{'marL': '2743200', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level8ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1000'}),
                                        **{'marL': '3200400', 'indent': '0'}
                                    ),
                                    OpenXML.Drawing.Level9ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1000'}),
                                        **{'marL': '3657600', 'indent': '0'}
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '0'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Click to edit Master text styles')
                                    )
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{8800B589-EE07-CE3B-194E-B4907F287C7F}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '5', 'name': 'Date Placeholder 4'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'dt', 'sz': 'half', 'idx': '10'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Field(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US', 'smtClean': '0'}),
                                        OpenXML.Drawing.Text('10/3/26'),
                                        **{'id': '{D68DF6A3-B8D2-1244-AA57-60AE5089C008}', 'type': 'datetimeFigureOut'}
                                    ),
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{B87A2357-028E-0E41-4087-2C266B6681F5}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '6', 'name': 'Footer Placeholder 5'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'ftr', 'sz': 'quarter', 'idx': '11'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{75203096-0B5B-B038-22F7-9EA8144D91EB}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '7', 'name': 'Slide Number Placeholder 6'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'sldNum', 'sz': 'quarter', 'idx': '12'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Field(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US', 'smtClean': '0'}),
                                        OpenXML.Drawing.Text('‹#›'),
                                        **{'id': '{190F7A14-BFAA-8642-8063-7C43CC189FC6}', 'type': 'slidenum'}
                                    ),
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        )
                    ),
                    OpenXML.Presentation.ExtensionListWithModification(
                        OpenXML.Presentation.Extension(
                            OpenXML.Presentation2010.CreationId(
                                **{'val': '2339305606', 'xmlns:p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main'}
                            ),
                            **{'uri': '{BB962C8B-B14F-4D97-AF65-F5344CB8AC3E}'}
                        )
                    ),
                    **{'name': 'Picture with Caption'}
                ),
                OpenXML.Presentation.ColorMapOverride(OpenXML.Drawing.MasterColorMapping()),
                **{'type': 'picTx', 'preserve': '1', 'xmlns:a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'xmlns:r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships', 'xmlns:p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
            )),
        OpenXMLPart('ppt/slideLayouts/slideLayout10.xml', 'application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml',
            OpenXML.Presentation.SlideLayout(
                OpenXML.Presentation.CommonSlideData(
                    OpenXML.Presentation.ShapeTree(
                        OpenXML.Presentation.NonVisualGroupShapeProperties(
                            OpenXML.Presentation.NonVisualDrawingProperties(**{'id': '1', 'name': ''}),
                            OpenXML.Presentation.NonVisualGroupShapeDrawingProperties(),
                            OpenXML.Presentation.ApplicationNonVisualDrawingProperties()
                        ),
                        OpenXML.Presentation.GroupShapeProperties(
                            OpenXML.Drawing.Transform2D(
                                OpenXML.Drawing.Offset(**{'x': '0', 'y': '0'}),
                                OpenXML.Drawing.Extents(**{'cx': '0', 'cy': '0'}),
                                OpenXML.Drawing.ChildOffset(**{'x': '0', 'y': '0'}),
                                OpenXML.Drawing.ChildExtents(**{'cx': '0', 'cy': '0'})
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{C3FFF955-E052-B408-46DD-BD86AFB32ED9}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '2', 'name': 'Title 1'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(**{'type': 'title'})
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Click to edit Master title style')
                                    )
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{C2317F87-2572-8BAF-A09F-A5C8B33EB1C4}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '3', 'name': 'Vertical Text Placeholder 2'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'body', 'orient': 'vert', 'idx': '1'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(**{'vert': 'eaVert'}),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '0'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Click to edit Master text styles')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '1'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Second level')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '2'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Third level')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '3'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Fourth level')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '4'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Fifth level')
                                    )
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{6368AB55-136A-E4C4-958B-C3226465F279}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '4', 'name': 'Date Placeholder 3'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'dt', 'sz': 'half', 'idx': '10'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Field(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US', 'smtClean': '0'}),
                                        OpenXML.Drawing.Text('10/3/26'),
                                        **{'id': '{D68DF6A3-B8D2-1244-AA57-60AE5089C008}', 'type': 'datetimeFigureOut'}
                                    ),
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{30544F3E-FEAB-DF72-43CE-CD0E0906F141}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '5', 'name': 'Footer Placeholder 4'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'ftr', 'sz': 'quarter', 'idx': '11'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{101ADE1D-6011-0956-641D-CCFEFF45E136}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '6', 'name': 'Slide Number Placeholder 5'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'sldNum', 'sz': 'quarter', 'idx': '12'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Field(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US', 'smtClean': '0'}),
                                        OpenXML.Drawing.Text('‹#›'),
                                        **{'id': '{190F7A14-BFAA-8642-8063-7C43CC189FC6}', 'type': 'slidenum'}
                                    ),
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        )
                    ),
                    OpenXML.Presentation.ExtensionListWithModification(
                        OpenXML.Presentation.Extension(
                            OpenXML.Presentation2010.CreationId(
                                **{'val': '2064164496', 'xmlns:p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main'}
                            ),
                            **{'uri': '{BB962C8B-B14F-4D97-AF65-F5344CB8AC3E}'}
                        )
                    ),
                    **{'name': 'Title and Vertical Text'}
                ),
                OpenXML.Presentation.ColorMapOverride(OpenXML.Drawing.MasterColorMapping()),
                **{'type': 'vertTx', 'preserve': '1', 'xmlns:a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'xmlns:r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships', 'xmlns:p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
            )),
        OpenXMLPart('ppt/slideLayouts/slideLayout11.xml', 'application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml',
            OpenXML.Presentation.SlideLayout(
                OpenXML.Presentation.CommonSlideData(
                    OpenXML.Presentation.ShapeTree(
                        OpenXML.Presentation.NonVisualGroupShapeProperties(
                            OpenXML.Presentation.NonVisualDrawingProperties(**{'id': '1', 'name': ''}),
                            OpenXML.Presentation.NonVisualGroupShapeDrawingProperties(),
                            OpenXML.Presentation.ApplicationNonVisualDrawingProperties()
                        ),
                        OpenXML.Presentation.GroupShapeProperties(
                            OpenXML.Drawing.Transform2D(
                                OpenXML.Drawing.Offset(**{'x': '0', 'y': '0'}),
                                OpenXML.Drawing.Extents(**{'cx': '0', 'cy': '0'}),
                                OpenXML.Drawing.ChildOffset(**{'x': '0', 'y': '0'}),
                                OpenXML.Drawing.ChildExtents(**{'cx': '0', 'cy': '0'})
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{77F49985-1AAB-6EDD-C679-8E038622DC18}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '2', 'name': 'Vertical Title 1'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'title', 'orient': 'vert'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(
                                OpenXML.Drawing.Transform2D(
                                    OpenXML.Drawing.Offset(**{'x': '8724900', 'y': '365125'}),
                                    OpenXML.Drawing.Extents(**{'cx': '2628900', 'cy': '5811838'})
                                )
                            ),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(**{'vert': 'eaVert'}),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Click to edit Master title style')
                                    )
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{A6FDBA70-F1F5-FF77-2F9A-8EC5E8D5042C}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '3', 'name': 'Vertical Text Placeholder 2'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'body', 'orient': 'vert', 'idx': '1'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(
                                OpenXML.Drawing.Transform2D(
                                    OpenXML.Drawing.Offset(**{'x': '838200', 'y': '365125'}),
                                    OpenXML.Drawing.Extents(**{'cx': '7734300', 'cy': '5811838'})
                                )
                            ),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(**{'vert': 'eaVert'}),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '0'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Click to edit Master text styles')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '1'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Second level')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '2'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Third level')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '3'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Fourth level')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '4'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Fifth level')
                                    )
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{ABA4307A-30EC-CF50-2F2B-81E3CC5B5AB7}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '4', 'name': 'Date Placeholder 3'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'dt', 'sz': 'half', 'idx': '10'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Field(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US', 'smtClean': '0'}),
                                        OpenXML.Drawing.Text('10/3/26'),
                                        **{'id': '{D68DF6A3-B8D2-1244-AA57-60AE5089C008}', 'type': 'datetimeFigureOut'}
                                    ),
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{C38AEF30-C80E-656A-DC2E-5AD60E56D531}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '5', 'name': 'Footer Placeholder 4'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'ftr', 'sz': 'quarter', 'idx': '11'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{A2DCD0C9-42F6-7971-D263-AC5C85370CDB}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '6', 'name': 'Slide Number Placeholder 5'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'sldNum', 'sz': 'quarter', 'idx': '12'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Field(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US', 'smtClean': '0'}),
                                        OpenXML.Drawing.Text('‹#›'),
                                        **{'id': '{190F7A14-BFAA-8642-8063-7C43CC189FC6}', 'type': 'slidenum'}
                                    ),
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        )
                    ),
                    OpenXML.Presentation.ExtensionListWithModification(
                        OpenXML.Presentation.Extension(
                            OpenXML.Presentation2010.CreationId(
                                **{'val': '472634817', 'xmlns:p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main'}
                            ),
                            **{'uri': '{BB962C8B-B14F-4D97-AF65-F5344CB8AC3E}'}
                        )
                    ),
                    **{'name': 'Vertical Title and Text'}
                ),
                OpenXML.Presentation.ColorMapOverride(OpenXML.Drawing.MasterColorMapping()),
                **{'type': 'vertTitleAndTx', 'preserve': '1', 'xmlns:a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'xmlns:r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships', 'xmlns:p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
            )),
        OpenXMLPart('ppt/slideLayouts/_rels/slideLayout11.xml.rels', 'application/vnd.openxmlformats-package.relationships+xml',
            OpenXML.Relationships.Relationships(
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId1', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster', 'Target': '../slideMasters/slideMaster1.xml'}
                ),
                **{'xmlns': 'http://schemas.openxmlformats.org/package/2006/relationships'}
            )),
        OpenXMLPart('ppt/slideLayouts/_rels/slideLayout10.xml.rels', 'application/vnd.openxmlformats-package.relationships+xml',
            OpenXML.Relationships.Relationships(
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId1', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster', 'Target': '../slideMasters/slideMaster1.xml'}
                ),
                **{'xmlns': 'http://schemas.openxmlformats.org/package/2006/relationships'}
            )),
        OpenXMLPart('ppt/slideLayouts/_rels/slideLayout9.xml.rels', 'application/vnd.openxmlformats-package.relationships+xml',
            OpenXML.Relationships.Relationships(
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId1', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster', 'Target': '../slideMasters/slideMaster1.xml'}
                ),
                **{'xmlns': 'http://schemas.openxmlformats.org/package/2006/relationships'}
            )),
        OpenXMLPart('ppt/slideLayouts/_rels/slideLayout8.xml.rels', 'application/vnd.openxmlformats-package.relationships+xml',
            OpenXML.Relationships.Relationships(
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId1', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster', 'Target': '../slideMasters/slideMaster1.xml'}
                ),
                **{'xmlns': 'http://schemas.openxmlformats.org/package/2006/relationships'}
            )),
        OpenXMLPart('ppt/slideLayouts/_rels/slideLayout7.xml.rels', 'application/vnd.openxmlformats-package.relationships+xml',
            OpenXML.Relationships.Relationships(
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId1', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster', 'Target': '../slideMasters/slideMaster1.xml'}
                ),
                **{'xmlns': 'http://schemas.openxmlformats.org/package/2006/relationships'}
            )),
        OpenXMLPart('ppt/slideLayouts/_rels/slideLayout6.xml.rels', 'application/vnd.openxmlformats-package.relationships+xml',
            OpenXML.Relationships.Relationships(
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId1', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster', 'Target': '../slideMasters/slideMaster1.xml'}
                ),
                **{'xmlns': 'http://schemas.openxmlformats.org/package/2006/relationships'}
            )),
        OpenXMLPart('ppt/slideLayouts/_rels/slideLayout5.xml.rels', 'application/vnd.openxmlformats-package.relationships+xml',
            OpenXML.Relationships.Relationships(
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId1', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster', 'Target': '../slideMasters/slideMaster1.xml'}
                ),
                **{'xmlns': 'http://schemas.openxmlformats.org/package/2006/relationships'}
            )),
        OpenXMLPart('ppt/slideLayouts/_rels/slideLayout4.xml.rels', 'application/vnd.openxmlformats-package.relationships+xml',
            OpenXML.Relationships.Relationships(
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId1', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster', 'Target': '../slideMasters/slideMaster1.xml'}
                ),
                **{'xmlns': 'http://schemas.openxmlformats.org/package/2006/relationships'}
            )),
        OpenXMLPart('ppt/slideLayouts/_rels/slideLayout3.xml.rels', 'application/vnd.openxmlformats-package.relationships+xml',
            OpenXML.Relationships.Relationships(
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId1', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster', 'Target': '../slideMasters/slideMaster1.xml'}
                ),
                **{'xmlns': 'http://schemas.openxmlformats.org/package/2006/relationships'}
            )),
        OpenXMLPart('ppt/slideLayouts/_rels/slideLayout2.xml.rels', 'application/vnd.openxmlformats-package.relationships+xml',
            OpenXML.Relationships.Relationships(
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId1', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster', 'Target': '../slideMasters/slideMaster1.xml'}
                ),
                **{'xmlns': 'http://schemas.openxmlformats.org/package/2006/relationships'}
            )),
        OpenXMLPart('ppt/slideLayouts/_rels/slideLayout1.xml.rels', 'application/vnd.openxmlformats-package.relationships+xml',
            OpenXML.Relationships.Relationships(
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId1', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster', 'Target': '../slideMasters/slideMaster1.xml'}
                ),
                **{'xmlns': 'http://schemas.openxmlformats.org/package/2006/relationships'}
            )),
        OpenXMLPart('ppt/slideMasters/_rels/slideMaster1.xml.rels', 'application/vnd.openxmlformats-package.relationships+xml',
            OpenXML.Relationships.Relationships(
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId8', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout', 'Target': '../slideLayouts/slideLayout8.xml'}
                ),
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId3', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout', 'Target': '../slideLayouts/slideLayout3.xml'}
                ),
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId7', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout', 'Target': '../slideLayouts/slideLayout7.xml'}
                ),
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId12', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme', 'Target': '../theme/theme1.xml'}
                ),
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId2', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout', 'Target': '../slideLayouts/slideLayout2.xml'}
                ),
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId1', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout', 'Target': '../slideLayouts/slideLayout1.xml'}
                ),
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId6', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout', 'Target': '../slideLayouts/slideLayout6.xml'}
                ),
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId11', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout', 'Target': '../slideLayouts/slideLayout11.xml'}
                ),
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId5', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout', 'Target': '../slideLayouts/slideLayout5.xml'}
                ),
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId10', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout', 'Target': '../slideLayouts/slideLayout10.xml'}
                ),
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId4', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout', 'Target': '../slideLayouts/slideLayout4.xml'}
                ),
                OpenXML.Relationships.Relationship(
                    **{'Id': 'rId9', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout', 'Target': '../slideLayouts/slideLayout9.xml'}
                ),
                **{'xmlns': 'http://schemas.openxmlformats.org/package/2006/relationships'}
            )),
        OpenXMLPart('ppt/slideMasters/slideMaster1.xml', 'application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml',
            OpenXML.Presentation.SlideMaster(
                OpenXML.Presentation.CommonSlideData(
                    OpenXML.Presentation.Background(
                        OpenXML.Presentation.BackgroundStyleReference(
                            OpenXML.Drawing.SchemeColor(**{'val': 'bg1'}),
                            **{'idx': '1001'}
                        )
                    ),
                    OpenXML.Presentation.ShapeTree(
                        OpenXML.Presentation.NonVisualGroupShapeProperties(
                            OpenXML.Presentation.NonVisualDrawingProperties(**{'id': '1', 'name': ''}),
                            OpenXML.Presentation.NonVisualGroupShapeDrawingProperties(),
                            OpenXML.Presentation.ApplicationNonVisualDrawingProperties()
                        ),
                        OpenXML.Presentation.GroupShapeProperties(
                            OpenXML.Drawing.Transform2D(
                                OpenXML.Drawing.Offset(**{'x': '0', 'y': '0'}),
                                OpenXML.Drawing.Extents(**{'cx': '0', 'cy': '0'}),
                                OpenXML.Drawing.ChildOffset(**{'x': '0', 'y': '0'}),
                                OpenXML.Drawing.ChildExtents(**{'cx': '0', 'cy': '0'})
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{F91E97F6-5303-3627-E058-6EBC52F745C9}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '2', 'name': 'Title Placeholder 1'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(**{'type': 'title'})
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(
                                OpenXML.Drawing.Transform2D(
                                    OpenXML.Drawing.Offset(**{'x': '838200', 'y': '365125'}),
                                    OpenXML.Drawing.Extents(**{'cx': '10515600', 'cy': '1325563'})
                                ),
                                OpenXML.Drawing.PresetGeometry(
                                    OpenXML.Drawing.AdjustValueList(),
                                    **{'prst': 'rect'}
                                )
                            ),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(
                                    OpenXML.Drawing.NormalAutoFit(),
                                    **{'vert': 'horz', 'lIns': '91440', 'tIns': '45720', 'rIns': '91440', 'bIns': '45720', 'rtlCol': '0', 'anchor': 'ctr'}
                                ),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Click to edit Master title style')
                                    )
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{965336F1-2641-EDB0-9428-60299912C12C}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '3', 'name': 'Text Placeholder 2'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(**{'type': 'body', 'idx': '1'})
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(
                                OpenXML.Drawing.Transform2D(
                                    OpenXML.Drawing.Offset(**{'x': '838200', 'y': '1825625'}),
                                    OpenXML.Drawing.Extents(**{'cx': '10515600', 'cy': '4351338'})
                                ),
                                OpenXML.Drawing.PresetGeometry(
                                    OpenXML.Drawing.AdjustValueList(),
                                    **{'prst': 'rect'}
                                )
                            ),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(
                                    OpenXML.Drawing.NormalAutoFit(),
                                    **{'vert': 'horz', 'lIns': '91440', 'tIns': '45720', 'rIns': '91440', 'bIns': '45720', 'rtlCol': '0'}
                                ),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '0'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Click to edit Master text styles')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '1'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Second level')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '2'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Third level')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '3'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Fourth level')
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.ParagraphProperties(**{'lvl': '4'}),
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Fifth level')
                                    )
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{364C5B88-7E09-C72A-F23B-850759054F9E}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '4', 'name': 'Date Placeholder 3'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'dt', 'sz': 'half', 'idx': '2'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(
                                OpenXML.Drawing.Transform2D(
                                    OpenXML.Drawing.Offset(**{'x': '838200', 'y': '6356350'}),
                                    OpenXML.Drawing.Extents(**{'cx': '2743200', 'cy': '365125'})
                                ),
                                OpenXML.Drawing.PresetGeometry(
                                    OpenXML.Drawing.AdjustValueList(),
                                    **{'prst': 'rect'}
                                )
                            ),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(
                                    **{'vert': 'horz', 'lIns': '91440', 'tIns': '45720', 'rIns': '91440', 'bIns': '45720', 'rtlCol': '0', 'anchor': 'ctr'}
                                ),
                                OpenXML.Drawing.ListStyle(
                                    OpenXML.Drawing.Level1ParagraphProperties(
                                        OpenXML.Drawing.DefaultRunProperties(
                                            OpenXML.Drawing.SolidFill(
                                                OpenXML.Drawing.SchemeColor(
                                                    OpenXML.Drawing.Tint(**{'val': '82000'}),
                                                    **{'val': 'tx1'}
                                                )
                                            ),
                                            **{'sz': '1200'}
                                        ),
                                        **{'algn': 'l'}
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Field(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US', 'smtClean': '0'}),
                                        OpenXML.Drawing.Text('10/3/26'),
                                        **{'id': '{D68DF6A3-B8D2-1244-AA57-60AE5089C008}', 'type': 'datetimeFigureOut'}
                                    ),
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{C519FB53-85D1-43AF-117E-1FC8D5F3713A}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '5', 'name': 'Footer Placeholder 4'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'ftr', 'sz': 'quarter', 'idx': '3'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(
                                OpenXML.Drawing.Transform2D(
                                    OpenXML.Drawing.Offset(**{'x': '4038600', 'y': '6356350'}),
                                    OpenXML.Drawing.Extents(**{'cx': '4114800', 'cy': '365125'})
                                ),
                                OpenXML.Drawing.PresetGeometry(
                                    OpenXML.Drawing.AdjustValueList(),
                                    **{'prst': 'rect'}
                                )
                            ),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(
                                    **{'vert': 'horz', 'lIns': '91440', 'tIns': '45720', 'rIns': '91440', 'bIns': '45720', 'rtlCol': '0', 'anchor': 'ctr'}
                                ),
                                OpenXML.Drawing.ListStyle(
                                    OpenXML.Drawing.Level1ParagraphProperties(
                                        OpenXML.Drawing.DefaultRunProperties(
                                            OpenXML.Drawing.SolidFill(
                                                OpenXML.Drawing.SchemeColor(
                                                    OpenXML.Drawing.Tint(**{'val': '82000'}),
                                                    **{'val': 'tx1'}
                                                )
                                            ),
                                            **{'sz': '1200'}
                                        ),
                                        **{'algn': 'ctr'}
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{3C5FC232-37CE-F347-49BE-BF090244F179}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '6', 'name': 'Slide Number Placeholder 5'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'sldNum', 'sz': 'quarter', 'idx': '4'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(
                                OpenXML.Drawing.Transform2D(
                                    OpenXML.Drawing.Offset(**{'x': '8610600', 'y': '6356350'}),
                                    OpenXML.Drawing.Extents(**{'cx': '2743200', 'cy': '365125'})
                                ),
                                OpenXML.Drawing.PresetGeometry(
                                    OpenXML.Drawing.AdjustValueList(),
                                    **{'prst': 'rect'}
                                )
                            ),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(
                                    **{'vert': 'horz', 'lIns': '91440', 'tIns': '45720', 'rIns': '91440', 'bIns': '45720', 'rtlCol': '0', 'anchor': 'ctr'}
                                ),
                                OpenXML.Drawing.ListStyle(
                                    OpenXML.Drawing.Level1ParagraphProperties(
                                        OpenXML.Drawing.DefaultRunProperties(
                                            OpenXML.Drawing.SolidFill(
                                                OpenXML.Drawing.SchemeColor(
                                                    OpenXML.Drawing.Tint(**{'val': '82000'}),
                                                    **{'val': 'tx1'}
                                                )
                                            ),
                                            **{'sz': '1200'}
                                        ),
                                        **{'algn': 'r'}
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Field(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US', 'smtClean': '0'}),
                                        OpenXML.Drawing.Text('‹#›'),
                                        **{'id': '{190F7A14-BFAA-8642-8063-7C43CC189FC6}', 'type': 'slidenum'}
                                    ),
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        )
                    ),
                    OpenXML.Presentation.ExtensionListWithModification(
                        OpenXML.Presentation.Extension(
                            OpenXML.Presentation2010.CreationId(
                                **{'val': '3091200045', 'xmlns:p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main'}
                            ),
                            **{'uri': '{BB962C8B-B14F-4D97-AF65-F5344CB8AC3E}'}
                        )
                    )
                ),
                OpenXML.Presentation.ColorMap(
                    **{'bg1': 'lt1', 'tx1': 'dk1', 'bg2': 'lt2', 'tx2': 'dk2', 'accent1': 'accent1', 'accent2': 'accent2', 'accent3': 'accent3', 'accent4': 'accent4', 'accent5': 'accent5', 'accent6': 'accent6', 'hlink': 'hlink', 'folHlink': 'folHlink'}
                ),
                OpenXML.Presentation.SlideLayoutIdList(
                    OpenXML.Presentation.SlideLayoutId(**{'id': '2147483649', 'r:id': 'rId1'}),
                    OpenXML.Presentation.SlideLayoutId(**{'id': '2147483650', 'r:id': 'rId2'}),
                    OpenXML.Presentation.SlideLayoutId(**{'id': '2147483651', 'r:id': 'rId3'}),
                    OpenXML.Presentation.SlideLayoutId(**{'id': '2147483652', 'r:id': 'rId4'}),
                    OpenXML.Presentation.SlideLayoutId(**{'id': '2147483653', 'r:id': 'rId5'}),
                    OpenXML.Presentation.SlideLayoutId(**{'id': '2147483654', 'r:id': 'rId6'}),
                    OpenXML.Presentation.SlideLayoutId(**{'id': '2147483655', 'r:id': 'rId7'}),
                    OpenXML.Presentation.SlideLayoutId(**{'id': '2147483656', 'r:id': 'rId8'}),
                    OpenXML.Presentation.SlideLayoutId(**{'id': '2147483657', 'r:id': 'rId9'}),
                    OpenXML.Presentation.SlideLayoutId(**{'id': '2147483658', 'r:id': 'rId10'}),
                    OpenXML.Presentation.SlideLayoutId(**{'id': '2147483659', 'r:id': 'rId11'})
                ),
                OpenXML.Presentation.TextStyles(
                    OpenXML.Presentation.TitleStyle(
                        OpenXML.Drawing.Level1ParagraphProperties(
                            OpenXML.Drawing.LineSpacing(OpenXML.Drawing.SpacingPercent(**{'val': '90000'})),
                            OpenXML.Drawing.SpaceBefore(OpenXML.Drawing.SpacingPercent(**{'val': '0'})),
                            OpenXML.Drawing.NoBullet(),
                            OpenXML.Drawing.DefaultRunProperties(
                                OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'tx1'})),
                                OpenXML.Drawing.LatinFont(**{'typeface': '+mj-lt'}),
                                OpenXML.Drawing.EastAsianFont(**{'typeface': '+mj-ea'}),
                                OpenXML.Drawing.ComplexScriptFont(**{'typeface': '+mj-cs'}),
                                **{'sz': '4400', 'kern': '1200'}
                            ),
                            **{'algn': 'l', 'defTabSz': '914400', 'rtl': '0', 'eaLnBrk': '1', 'latinLnBrk': '0', 'hangingPunct': '1'}
                        )
                    ),
                    OpenXML.Presentation.BodyStyle(
                        OpenXML.Drawing.Level1ParagraphProperties(
                            OpenXML.Drawing.LineSpacing(OpenXML.Drawing.SpacingPercent(**{'val': '90000'})),
                            OpenXML.Drawing.SpaceBefore(OpenXML.Drawing.SpacingPoints(**{'val': '1000'})),
                            OpenXML.Drawing.BulletFont(
                                **{'typeface': 'Arial', 'panose': '020B0604020202020204', 'pitchFamily': '34', 'charset': '0'}
                            ),
                            OpenXML.Drawing.CharacterBullet(**{'char': '•'}),
                            OpenXML.Drawing.DefaultRunProperties(
                                OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'tx1'})),
                                OpenXML.Drawing.LatinFont(**{'typeface': '+mn-lt'}),
                                OpenXML.Drawing.EastAsianFont(**{'typeface': '+mn-ea'}),
                                OpenXML.Drawing.ComplexScriptFont(**{'typeface': '+mn-cs'}),
                                **{'sz': '2800', 'kern': '1200'}
                            ),
                            **{'marL': '228600', 'indent': '-228600', 'algn': 'l', 'defTabSz': '914400', 'rtl': '0', 'eaLnBrk': '1', 'latinLnBrk': '0', 'hangingPunct': '1'}
                        ),
                        OpenXML.Drawing.Level2ParagraphProperties(
                            OpenXML.Drawing.LineSpacing(OpenXML.Drawing.SpacingPercent(**{'val': '90000'})),
                            OpenXML.Drawing.SpaceBefore(OpenXML.Drawing.SpacingPoints(**{'val': '500'})),
                            OpenXML.Drawing.BulletFont(
                                **{'typeface': 'Arial', 'panose': '020B0604020202020204', 'pitchFamily': '34', 'charset': '0'}
                            ),
                            OpenXML.Drawing.CharacterBullet(**{'char': '•'}),
                            OpenXML.Drawing.DefaultRunProperties(
                                OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'tx1'})),
                                OpenXML.Drawing.LatinFont(**{'typeface': '+mn-lt'}),
                                OpenXML.Drawing.EastAsianFont(**{'typeface': '+mn-ea'}),
                                OpenXML.Drawing.ComplexScriptFont(**{'typeface': '+mn-cs'}),
                                **{'sz': '2400', 'kern': '1200'}
                            ),
                            **{'marL': '685800', 'indent': '-228600', 'algn': 'l', 'defTabSz': '914400', 'rtl': '0', 'eaLnBrk': '1', 'latinLnBrk': '0', 'hangingPunct': '1'}
                        ),
                        OpenXML.Drawing.Level3ParagraphProperties(
                            OpenXML.Drawing.LineSpacing(OpenXML.Drawing.SpacingPercent(**{'val': '90000'})),
                            OpenXML.Drawing.SpaceBefore(OpenXML.Drawing.SpacingPoints(**{'val': '500'})),
                            OpenXML.Drawing.BulletFont(
                                **{'typeface': 'Arial', 'panose': '020B0604020202020204', 'pitchFamily': '34', 'charset': '0'}
                            ),
                            OpenXML.Drawing.CharacterBullet(**{'char': '•'}),
                            OpenXML.Drawing.DefaultRunProperties(
                                OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'tx1'})),
                                OpenXML.Drawing.LatinFont(**{'typeface': '+mn-lt'}),
                                OpenXML.Drawing.EastAsianFont(**{'typeface': '+mn-ea'}),
                                OpenXML.Drawing.ComplexScriptFont(**{'typeface': '+mn-cs'}),
                                **{'sz': '2000', 'kern': '1200'}
                            ),
                            **{'marL': '1143000', 'indent': '-228600', 'algn': 'l', 'defTabSz': '914400', 'rtl': '0', 'eaLnBrk': '1', 'latinLnBrk': '0', 'hangingPunct': '1'}
                        ),
                        OpenXML.Drawing.Level4ParagraphProperties(
                            OpenXML.Drawing.LineSpacing(OpenXML.Drawing.SpacingPercent(**{'val': '90000'})),
                            OpenXML.Drawing.SpaceBefore(OpenXML.Drawing.SpacingPoints(**{'val': '500'})),
                            OpenXML.Drawing.BulletFont(
                                **{'typeface': 'Arial', 'panose': '020B0604020202020204', 'pitchFamily': '34', 'charset': '0'}
                            ),
                            OpenXML.Drawing.CharacterBullet(**{'char': '•'}),
                            OpenXML.Drawing.DefaultRunProperties(
                                OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'tx1'})),
                                OpenXML.Drawing.LatinFont(**{'typeface': '+mn-lt'}),
                                OpenXML.Drawing.EastAsianFont(**{'typeface': '+mn-ea'}),
                                OpenXML.Drawing.ComplexScriptFont(**{'typeface': '+mn-cs'}),
                                **{'sz': '1800', 'kern': '1200'}
                            ),
                            **{'marL': '1600200', 'indent': '-228600', 'algn': 'l', 'defTabSz': '914400', 'rtl': '0', 'eaLnBrk': '1', 'latinLnBrk': '0', 'hangingPunct': '1'}
                        ),
                        OpenXML.Drawing.Level5ParagraphProperties(
                            OpenXML.Drawing.LineSpacing(OpenXML.Drawing.SpacingPercent(**{'val': '90000'})),
                            OpenXML.Drawing.SpaceBefore(OpenXML.Drawing.SpacingPoints(**{'val': '500'})),
                            OpenXML.Drawing.BulletFont(
                                **{'typeface': 'Arial', 'panose': '020B0604020202020204', 'pitchFamily': '34', 'charset': '0'}
                            ),
                            OpenXML.Drawing.CharacterBullet(**{'char': '•'}),
                            OpenXML.Drawing.DefaultRunProperties(
                                OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'tx1'})),
                                OpenXML.Drawing.LatinFont(**{'typeface': '+mn-lt'}),
                                OpenXML.Drawing.EastAsianFont(**{'typeface': '+mn-ea'}),
                                OpenXML.Drawing.ComplexScriptFont(**{'typeface': '+mn-cs'}),
                                **{'sz': '1800', 'kern': '1200'}
                            ),
                            **{'marL': '2057400', 'indent': '-228600', 'algn': 'l', 'defTabSz': '914400', 'rtl': '0', 'eaLnBrk': '1', 'latinLnBrk': '0', 'hangingPunct': '1'}
                        ),
                        OpenXML.Drawing.Level6ParagraphProperties(
                            OpenXML.Drawing.LineSpacing(OpenXML.Drawing.SpacingPercent(**{'val': '90000'})),
                            OpenXML.Drawing.SpaceBefore(OpenXML.Drawing.SpacingPoints(**{'val': '500'})),
                            OpenXML.Drawing.BulletFont(
                                **{'typeface': 'Arial', 'panose': '020B0604020202020204', 'pitchFamily': '34', 'charset': '0'}
                            ),
                            OpenXML.Drawing.CharacterBullet(**{'char': '•'}),
                            OpenXML.Drawing.DefaultRunProperties(
                                OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'tx1'})),
                                OpenXML.Drawing.LatinFont(**{'typeface': '+mn-lt'}),
                                OpenXML.Drawing.EastAsianFont(**{'typeface': '+mn-ea'}),
                                OpenXML.Drawing.ComplexScriptFont(**{'typeface': '+mn-cs'}),
                                **{'sz': '1800', 'kern': '1200'}
                            ),
                            **{'marL': '2514600', 'indent': '-228600', 'algn': 'l', 'defTabSz': '914400', 'rtl': '0', 'eaLnBrk': '1', 'latinLnBrk': '0', 'hangingPunct': '1'}
                        ),
                        OpenXML.Drawing.Level7ParagraphProperties(
                            OpenXML.Drawing.LineSpacing(OpenXML.Drawing.SpacingPercent(**{'val': '90000'})),
                            OpenXML.Drawing.SpaceBefore(OpenXML.Drawing.SpacingPoints(**{'val': '500'})),
                            OpenXML.Drawing.BulletFont(
                                **{'typeface': 'Arial', 'panose': '020B0604020202020204', 'pitchFamily': '34', 'charset': '0'}
                            ),
                            OpenXML.Drawing.CharacterBullet(**{'char': '•'}),
                            OpenXML.Drawing.DefaultRunProperties(
                                OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'tx1'})),
                                OpenXML.Drawing.LatinFont(**{'typeface': '+mn-lt'}),
                                OpenXML.Drawing.EastAsianFont(**{'typeface': '+mn-ea'}),
                                OpenXML.Drawing.ComplexScriptFont(**{'typeface': '+mn-cs'}),
                                **{'sz': '1800', 'kern': '1200'}
                            ),
                            **{'marL': '2971800', 'indent': '-228600', 'algn': 'l', 'defTabSz': '914400', 'rtl': '0', 'eaLnBrk': '1', 'latinLnBrk': '0', 'hangingPunct': '1'}
                        ),
                        OpenXML.Drawing.Level8ParagraphProperties(
                            OpenXML.Drawing.LineSpacing(OpenXML.Drawing.SpacingPercent(**{'val': '90000'})),
                            OpenXML.Drawing.SpaceBefore(OpenXML.Drawing.SpacingPoints(**{'val': '500'})),
                            OpenXML.Drawing.BulletFont(
                                **{'typeface': 'Arial', 'panose': '020B0604020202020204', 'pitchFamily': '34', 'charset': '0'}
                            ),
                            OpenXML.Drawing.CharacterBullet(**{'char': '•'}),
                            OpenXML.Drawing.DefaultRunProperties(
                                OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'tx1'})),
                                OpenXML.Drawing.LatinFont(**{'typeface': '+mn-lt'}),
                                OpenXML.Drawing.EastAsianFont(**{'typeface': '+mn-ea'}),
                                OpenXML.Drawing.ComplexScriptFont(**{'typeface': '+mn-cs'}),
                                **{'sz': '1800', 'kern': '1200'}
                            ),
                            **{'marL': '3429000', 'indent': '-228600', 'algn': 'l', 'defTabSz': '914400', 'rtl': '0', 'eaLnBrk': '1', 'latinLnBrk': '0', 'hangingPunct': '1'}
                        ),
                        OpenXML.Drawing.Level9ParagraphProperties(
                            OpenXML.Drawing.LineSpacing(OpenXML.Drawing.SpacingPercent(**{'val': '90000'})),
                            OpenXML.Drawing.SpaceBefore(OpenXML.Drawing.SpacingPoints(**{'val': '500'})),
                            OpenXML.Drawing.BulletFont(
                                **{'typeface': 'Arial', 'panose': '020B0604020202020204', 'pitchFamily': '34', 'charset': '0'}
                            ),
                            OpenXML.Drawing.CharacterBullet(**{'char': '•'}),
                            OpenXML.Drawing.DefaultRunProperties(
                                OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'tx1'})),
                                OpenXML.Drawing.LatinFont(**{'typeface': '+mn-lt'}),
                                OpenXML.Drawing.EastAsianFont(**{'typeface': '+mn-ea'}),
                                OpenXML.Drawing.ComplexScriptFont(**{'typeface': '+mn-cs'}),
                                **{'sz': '1800', 'kern': '1200'}
                            ),
                            **{'marL': '3886200', 'indent': '-228600', 'algn': 'l', 'defTabSz': '914400', 'rtl': '0', 'eaLnBrk': '1', 'latinLnBrk': '0', 'hangingPunct': '1'}
                        )
                    ),
                    OpenXML.Presentation.OtherStyle(
                        OpenXML.Drawing.DefaultParagraphProperties(
                            OpenXML.Drawing.DefaultRunProperties(**{'lang': 'en-US'})
                        ),
                        OpenXML.Drawing.Level1ParagraphProperties(
                            OpenXML.Drawing.DefaultRunProperties(
                                OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'tx1'})),
                                OpenXML.Drawing.LatinFont(**{'typeface': '+mn-lt'}),
                                OpenXML.Drawing.EastAsianFont(**{'typeface': '+mn-ea'}),
                                OpenXML.Drawing.ComplexScriptFont(**{'typeface': '+mn-cs'}),
                                **{'sz': '1800', 'kern': '1200'}
                            ),
                            **{'marL': '0', 'algn': 'l', 'defTabSz': '914400', 'rtl': '0', 'eaLnBrk': '1', 'latinLnBrk': '0', 'hangingPunct': '1'}
                        ),
                        OpenXML.Drawing.Level2ParagraphProperties(
                            OpenXML.Drawing.DefaultRunProperties(
                                OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'tx1'})),
                                OpenXML.Drawing.LatinFont(**{'typeface': '+mn-lt'}),
                                OpenXML.Drawing.EastAsianFont(**{'typeface': '+mn-ea'}),
                                OpenXML.Drawing.ComplexScriptFont(**{'typeface': '+mn-cs'}),
                                **{'sz': '1800', 'kern': '1200'}
                            ),
                            **{'marL': '457200', 'algn': 'l', 'defTabSz': '914400', 'rtl': '0', 'eaLnBrk': '1', 'latinLnBrk': '0', 'hangingPunct': '1'}
                        ),
                        OpenXML.Drawing.Level3ParagraphProperties(
                            OpenXML.Drawing.DefaultRunProperties(
                                OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'tx1'})),
                                OpenXML.Drawing.LatinFont(**{'typeface': '+mn-lt'}),
                                OpenXML.Drawing.EastAsianFont(**{'typeface': '+mn-ea'}),
                                OpenXML.Drawing.ComplexScriptFont(**{'typeface': '+mn-cs'}),
                                **{'sz': '1800', 'kern': '1200'}
                            ),
                            **{'marL': '914400', 'algn': 'l', 'defTabSz': '914400', 'rtl': '0', 'eaLnBrk': '1', 'latinLnBrk': '0', 'hangingPunct': '1'}
                        ),
                        OpenXML.Drawing.Level4ParagraphProperties(
                            OpenXML.Drawing.DefaultRunProperties(
                                OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'tx1'})),
                                OpenXML.Drawing.LatinFont(**{'typeface': '+mn-lt'}),
                                OpenXML.Drawing.EastAsianFont(**{'typeface': '+mn-ea'}),
                                OpenXML.Drawing.ComplexScriptFont(**{'typeface': '+mn-cs'}),
                                **{'sz': '1800', 'kern': '1200'}
                            ),
                            **{'marL': '1371600', 'algn': 'l', 'defTabSz': '914400', 'rtl': '0', 'eaLnBrk': '1', 'latinLnBrk': '0', 'hangingPunct': '1'}
                        ),
                        OpenXML.Drawing.Level5ParagraphProperties(
                            OpenXML.Drawing.DefaultRunProperties(
                                OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'tx1'})),
                                OpenXML.Drawing.LatinFont(**{'typeface': '+mn-lt'}),
                                OpenXML.Drawing.EastAsianFont(**{'typeface': '+mn-ea'}),
                                OpenXML.Drawing.ComplexScriptFont(**{'typeface': '+mn-cs'}),
                                **{'sz': '1800', 'kern': '1200'}
                            ),
                            **{'marL': '1828800', 'algn': 'l', 'defTabSz': '914400', 'rtl': '0', 'eaLnBrk': '1', 'latinLnBrk': '0', 'hangingPunct': '1'}
                        ),
                        OpenXML.Drawing.Level6ParagraphProperties(
                            OpenXML.Drawing.DefaultRunProperties(
                                OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'tx1'})),
                                OpenXML.Drawing.LatinFont(**{'typeface': '+mn-lt'}),
                                OpenXML.Drawing.EastAsianFont(**{'typeface': '+mn-ea'}),
                                OpenXML.Drawing.ComplexScriptFont(**{'typeface': '+mn-cs'}),
                                **{'sz': '1800', 'kern': '1200'}
                            ),
                            **{'marL': '2286000', 'algn': 'l', 'defTabSz': '914400', 'rtl': '0', 'eaLnBrk': '1', 'latinLnBrk': '0', 'hangingPunct': '1'}
                        ),
                        OpenXML.Drawing.Level7ParagraphProperties(
                            OpenXML.Drawing.DefaultRunProperties(
                                OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'tx1'})),
                                OpenXML.Drawing.LatinFont(**{'typeface': '+mn-lt'}),
                                OpenXML.Drawing.EastAsianFont(**{'typeface': '+mn-ea'}),
                                OpenXML.Drawing.ComplexScriptFont(**{'typeface': '+mn-cs'}),
                                **{'sz': '1800', 'kern': '1200'}
                            ),
                            **{'marL': '2743200', 'algn': 'l', 'defTabSz': '914400', 'rtl': '0', 'eaLnBrk': '1', 'latinLnBrk': '0', 'hangingPunct': '1'}
                        ),
                        OpenXML.Drawing.Level8ParagraphProperties(
                            OpenXML.Drawing.DefaultRunProperties(
                                OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'tx1'})),
                                OpenXML.Drawing.LatinFont(**{'typeface': '+mn-lt'}),
                                OpenXML.Drawing.EastAsianFont(**{'typeface': '+mn-ea'}),
                                OpenXML.Drawing.ComplexScriptFont(**{'typeface': '+mn-cs'}),
                                **{'sz': '1800', 'kern': '1200'}
                            ),
                            **{'marL': '3200400', 'algn': 'l', 'defTabSz': '914400', 'rtl': '0', 'eaLnBrk': '1', 'latinLnBrk': '0', 'hangingPunct': '1'}
                        ),
                        OpenXML.Drawing.Level9ParagraphProperties(
                            OpenXML.Drawing.DefaultRunProperties(
                                OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'tx1'})),
                                OpenXML.Drawing.LatinFont(**{'typeface': '+mn-lt'}),
                                OpenXML.Drawing.EastAsianFont(**{'typeface': '+mn-ea'}),
                                OpenXML.Drawing.ComplexScriptFont(**{'typeface': '+mn-cs'}),
                                **{'sz': '1800', 'kern': '1200'}
                            ),
                            **{'marL': '3657600', 'algn': 'l', 'defTabSz': '914400', 'rtl': '0', 'eaLnBrk': '1', 'latinLnBrk': '0', 'hangingPunct': '1'}
                        )
                    )
                ),
                **{'xmlns:a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'xmlns:r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships', 'xmlns:p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
            )),
        OpenXMLPart('ppt/slideLayouts/slideLayout1.xml', 'application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml',
            OpenXML.Presentation.SlideLayout(
                OpenXML.Presentation.CommonSlideData(
                    OpenXML.Presentation.ShapeTree(
                        OpenXML.Presentation.NonVisualGroupShapeProperties(
                            OpenXML.Presentation.NonVisualDrawingProperties(**{'id': '1', 'name': ''}),
                            OpenXML.Presentation.NonVisualGroupShapeDrawingProperties(),
                            OpenXML.Presentation.ApplicationNonVisualDrawingProperties()
                        ),
                        OpenXML.Presentation.GroupShapeProperties(
                            OpenXML.Drawing.Transform2D(
                                OpenXML.Drawing.Offset(**{'x': '0', 'y': '0'}),
                                OpenXML.Drawing.Extents(**{'cx': '0', 'cy': '0'}),
                                OpenXML.Drawing.ChildOffset(**{'x': '0', 'y': '0'}),
                                OpenXML.Drawing.ChildExtents(**{'cx': '0', 'cy': '0'})
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{A57A5C87-7E82-44D3-1BB6-DD266B17978E}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '2', 'name': 'Title 1'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(**{'type': 'ctrTitle'})
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(
                                OpenXML.Drawing.Transform2D(
                                    OpenXML.Drawing.Offset(**{'x': '1524000', 'y': '1122363'}),
                                    OpenXML.Drawing.Extents(**{'cx': '9144000', 'cy': '2387600'})
                                )
                            ),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(**{'anchor': 'b'}),
                                OpenXML.Drawing.ListStyle(
                                    OpenXML.Drawing.Level1ParagraphProperties(
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '6000'}),
                                        **{'algn': 'ctr'}
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Click to edit Master title style')
                                    )
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{722D3024-AA3A-8302-3B5B-E4E7A28C6BDB}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '3', 'name': 'Subtitle 2'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(**{'type': 'subTitle', 'idx': '1'})
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(
                                OpenXML.Drawing.Transform2D(
                                    OpenXML.Drawing.Offset(**{'x': '1524000', 'y': '3602038'}),
                                    OpenXML.Drawing.Extents(**{'cx': '9144000', 'cy': '1655762'})
                                )
                            ),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(
                                    OpenXML.Drawing.Level1ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '2400'}),
                                        **{'marL': '0', 'indent': '0', 'algn': 'ctr'}
                                    ),
                                    OpenXML.Drawing.Level2ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '2000'}),
                                        **{'marL': '457200', 'indent': '0', 'algn': 'ctr'}
                                    ),
                                    OpenXML.Drawing.Level3ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1800'}),
                                        **{'marL': '914400', 'indent': '0', 'algn': 'ctr'}
                                    ),
                                    OpenXML.Drawing.Level4ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1600'}),
                                        **{'marL': '1371600', 'indent': '0', 'algn': 'ctr'}
                                    ),
                                    OpenXML.Drawing.Level5ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1600'}),
                                        **{'marL': '1828800', 'indent': '0', 'algn': 'ctr'}
                                    ),
                                    OpenXML.Drawing.Level6ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1600'}),
                                        **{'marL': '2286000', 'indent': '0', 'algn': 'ctr'}
                                    ),
                                    OpenXML.Drawing.Level7ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1600'}),
                                        **{'marL': '2743200', 'indent': '0', 'algn': 'ctr'}
                                    ),
                                    OpenXML.Drawing.Level8ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1600'}),
                                        **{'marL': '3200400', 'indent': '0', 'algn': 'ctr'}
                                    ),
                                    OpenXML.Drawing.Level9ParagraphProperties(
                                        OpenXML.Drawing.NoBullet(),
                                        OpenXML.Drawing.DefaultRunProperties(**{'sz': '1600'}),
                                        **{'marL': '3657600', 'indent': '0', 'algn': 'ctr'}
                                    )
                                ),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Run(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US'}),
                                        OpenXML.Drawing.Text('Click to edit Master subtitle style')
                                    )
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{B5319B43-D048-BC3A-9CD7-D5CE72BDC803}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '4', 'name': 'Date Placeholder 3'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'dt', 'sz': 'half', 'idx': '10'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Field(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US', 'smtClean': '0'}),
                                        OpenXML.Drawing.Text('10/3/26'),
                                        **{'id': '{D68DF6A3-B8D2-1244-AA57-60AE5089C008}', 'type': 'datetimeFigureOut'}
                                    ),
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{A6D8F7FB-6F1D-479C-71FB-F88679CB6FFE}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '5', 'name': 'Footer Placeholder 4'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'ftr', 'sz': 'quarter', 'idx': '11'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        ),
                        OpenXML.Presentation.Shape(
                            OpenXML.Presentation.NonVisualShapeProperties(
                                OpenXML.Presentation.NonVisualDrawingProperties(
                                    OpenXML.Drawing.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Drawing2014.CreationId(
                                                **{'id': '{4517593F-8BE6-4ED0-578A-3474C6DD6121}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                            ),
                                            **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                        )
                                    ),
                                    **{'id': '6', 'name': 'Slide Number Placeholder 5'}
                                ),
                                OpenXML.Presentation.NonVisualShapeDrawingProperties(
                                    OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                                ),
                                OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                    OpenXML.Presentation.PlaceholderShape(
                                        **{'type': 'sldNum', 'sz': 'quarter', 'idx': '12'}
                                    )
                                )
                            ),
                            OpenXML.Presentation.ShapeProperties(),
                            OpenXML.Presentation.TextBody(
                                OpenXML.Drawing.BodyProperties(),
                                OpenXML.Drawing.ListStyle(),
                                OpenXML.Drawing.Paragraph(
                                    OpenXML.Drawing.Field(
                                        OpenXML.Drawing.RunProperties(**{'lang': 'en-US', 'smtClean': '0'}),
                                        OpenXML.Drawing.Text('‹#›'),
                                        **{'id': '{190F7A14-BFAA-8642-8063-7C43CC189FC6}', 'type': 'slidenum'}
                                    ),
                                    OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                                )
                            )
                        )
                    ),
                    OpenXML.Presentation.ExtensionListWithModification(
                        OpenXML.Presentation.Extension(
                            OpenXML.Presentation2010.CreationId(
                                **{'val': '710181942', 'xmlns:p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main'}
                            ),
                            **{'uri': '{BB962C8B-B14F-4D97-AF65-F5344CB8AC3E}'}
                        )
                    ),
                    **{'name': 'Title Slide'}
                ),
                OpenXML.Presentation.ColorMapOverride(OpenXML.Drawing.MasterColorMapping()),
                **{'type': 'title', 'preserve': '1', 'xmlns:a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'xmlns:r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships', 'xmlns:p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
            )),
        OpenXMLPart('ppt/theme/theme1.xml', 'application/vnd.openxmlformats-officedocument.theme+xml',
            OpenXML.Drawing.Theme(
                OpenXML.Drawing.ThemeElements(
                    OpenXML.Drawing.ColorScheme(
                        OpenXML.Drawing.Dark1Color(
                            OpenXML.Drawing.SystemColor(**{'val': 'windowText', 'lastClr': '000000'})
                        ),
                        OpenXML.Drawing.Light1Color(
                            OpenXML.Drawing.SystemColor(**{'val': 'window', 'lastClr': 'FFFFFF'})
                        ),
                        OpenXML.Drawing.Dark2Color(OpenXML.Drawing.RgbColorModelHex(**{'val': '0E2841'})),
                        OpenXML.Drawing.Light2Color(OpenXML.Drawing.RgbColorModelHex(**{'val': 'E8E8E8'})),
                        OpenXML.Drawing.Accent1Color(OpenXML.Drawing.RgbColorModelHex(**{'val': '156082'})),
                        OpenXML.Drawing.Accent2Color(OpenXML.Drawing.RgbColorModelHex(**{'val': 'E97132'})),
                        OpenXML.Drawing.Accent3Color(OpenXML.Drawing.RgbColorModelHex(**{'val': '196B24'})),
                        OpenXML.Drawing.Accent4Color(OpenXML.Drawing.RgbColorModelHex(**{'val': '0F9ED5'})),
                        OpenXML.Drawing.Accent5Color(OpenXML.Drawing.RgbColorModelHex(**{'val': 'A02B93'})),
                        OpenXML.Drawing.Accent6Color(OpenXML.Drawing.RgbColorModelHex(**{'val': '4EA72E'})),
                        OpenXML.Drawing.Hyperlink(OpenXML.Drawing.RgbColorModelHex(**{'val': '467886'})),
                        OpenXML.Drawing.FollowedHyperlinkColor(
                            OpenXML.Drawing.RgbColorModelHex(**{'val': '96607D'})
                        ),
                        **{'name': 'Office'}
                    ),
                    OpenXML.Drawing.FontScheme(
                        OpenXML.Drawing.MajorFont(
                            OpenXML.Drawing.LatinFont(
                                **{'typeface': 'Aptos Display', 'panose': '02110004020202020204'}
                            ),
                            OpenXML.Drawing.EastAsianFont(**{'typeface': ''}),
                            OpenXML.Drawing.ComplexScriptFont(**{'typeface': ''}),
                            OpenXML.Drawing.Fonts(**{'script': 'Jpan', 'typeface': '游ゴシック Light'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Hang', 'typeface': '맑은 고딕'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Hans', 'typeface': '等线 Light'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Hant', 'typeface': '新細明體'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Arab', 'typeface': 'Times New Roman'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Hebr', 'typeface': 'Times New Roman'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Thai', 'typeface': 'Angsana New'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Ethi', 'typeface': 'Nyala'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Beng', 'typeface': 'Vrinda'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Gujr', 'typeface': 'Shruti'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Khmr', 'typeface': 'MoolBoran'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Knda', 'typeface': 'Tunga'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Guru', 'typeface': 'Raavi'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Cans', 'typeface': 'Euphemia'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Cher', 'typeface': 'Plantagenet Cherokee'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Yiii', 'typeface': 'Microsoft Yi Baiti'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Tibt', 'typeface': 'Microsoft Himalaya'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Thaa', 'typeface': 'MV Boli'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Deva', 'typeface': 'Mangal'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Telu', 'typeface': 'Gautami'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Taml', 'typeface': 'Latha'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Syrc', 'typeface': 'Estrangelo Edessa'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Orya', 'typeface': 'Kalinga'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Mlym', 'typeface': 'Kartika'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Laoo', 'typeface': 'DokChampa'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Sinh', 'typeface': 'Iskoola Pota'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Mong', 'typeface': 'Mongolian Baiti'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Viet', 'typeface': 'Times New Roman'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Uigh', 'typeface': 'Microsoft Uighur'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Geor', 'typeface': 'Sylfaen'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Armn', 'typeface': 'Arial'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Bugi', 'typeface': 'Leelawadee UI'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Bopo', 'typeface': 'Microsoft JhengHei'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Java', 'typeface': 'Javanese Text'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Lisu', 'typeface': 'Segoe UI'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Mymr', 'typeface': 'Myanmar Text'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Nkoo', 'typeface': 'Ebrima'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Olck', 'typeface': 'Nirmala UI'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Osma', 'typeface': 'Ebrima'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Phag', 'typeface': 'Phagspa'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Syrn', 'typeface': 'Estrangelo Edessa'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Syrj', 'typeface': 'Estrangelo Edessa'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Syre', 'typeface': 'Estrangelo Edessa'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Sora', 'typeface': 'Nirmala UI'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Tale', 'typeface': 'Microsoft Tai Le'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Talu', 'typeface': 'Microsoft New Tai Lue'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Tfng', 'typeface': 'Ebrima'})
                        ),
                        OpenXML.Drawing.MinorFont(
                            OpenXML.Drawing.LatinFont(
                                **{'typeface': 'Aptos', 'panose': '02110004020202020204'}
                            ),
                            OpenXML.Drawing.EastAsianFont(**{'typeface': ''}),
                            OpenXML.Drawing.ComplexScriptFont(**{'typeface': ''}),
                            OpenXML.Drawing.Fonts(**{'script': 'Jpan', 'typeface': '游ゴシック'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Hang', 'typeface': '맑은 고딕'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Hans', 'typeface': '等线'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Hant', 'typeface': '新細明體'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Arab', 'typeface': 'Arial'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Hebr', 'typeface': 'Arial'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Thai', 'typeface': 'Cordia New'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Ethi', 'typeface': 'Nyala'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Beng', 'typeface': 'Vrinda'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Gujr', 'typeface': 'Shruti'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Khmr', 'typeface': 'DaunPenh'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Knda', 'typeface': 'Tunga'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Guru', 'typeface': 'Raavi'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Cans', 'typeface': 'Euphemia'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Cher', 'typeface': 'Plantagenet Cherokee'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Yiii', 'typeface': 'Microsoft Yi Baiti'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Tibt', 'typeface': 'Microsoft Himalaya'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Thaa', 'typeface': 'MV Boli'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Deva', 'typeface': 'Mangal'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Telu', 'typeface': 'Gautami'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Taml', 'typeface': 'Latha'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Syrc', 'typeface': 'Estrangelo Edessa'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Orya', 'typeface': 'Kalinga'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Mlym', 'typeface': 'Kartika'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Laoo', 'typeface': 'DokChampa'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Sinh', 'typeface': 'Iskoola Pota'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Mong', 'typeface': 'Mongolian Baiti'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Viet', 'typeface': 'Arial'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Uigh', 'typeface': 'Microsoft Uighur'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Geor', 'typeface': 'Sylfaen'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Armn', 'typeface': 'Arial'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Bugi', 'typeface': 'Leelawadee UI'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Bopo', 'typeface': 'Microsoft JhengHei'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Java', 'typeface': 'Javanese Text'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Lisu', 'typeface': 'Segoe UI'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Mymr', 'typeface': 'Myanmar Text'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Nkoo', 'typeface': 'Ebrima'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Olck', 'typeface': 'Nirmala UI'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Osma', 'typeface': 'Ebrima'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Phag', 'typeface': 'Phagspa'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Syrn', 'typeface': 'Estrangelo Edessa'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Syrj', 'typeface': 'Estrangelo Edessa'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Syre', 'typeface': 'Estrangelo Edessa'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Sora', 'typeface': 'Nirmala UI'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Tale', 'typeface': 'Microsoft Tai Le'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Talu', 'typeface': 'Microsoft New Tai Lue'}),
                            OpenXML.Drawing.Fonts(**{'script': 'Tfng', 'typeface': 'Ebrima'})
                        ),
                        **{'name': 'Office'}
                    ),
                    OpenXML.Drawing.FormatScheme(
                        OpenXML.Drawing.FillStyleList(
                            OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'phClr'})),
                            OpenXML.Drawing.GradientFill(
                                OpenXML.Drawing.GradientStopList(
                                    OpenXML.Drawing.GradientStop(
                                        OpenXML.Drawing.SchemeColor(
                                            OpenXML.Drawing.LuminanceModulation(**{'val': '110000'}),
                                            OpenXML.Drawing.SaturationModulation(**{'val': '105000'}),
                                            OpenXML.Drawing.Tint(**{'val': '67000'}),
                                            **{'val': 'phClr'}
                                        ),
                                        **{'pos': '0'}
                                    ),
                                    OpenXML.Drawing.GradientStop(
                                        OpenXML.Drawing.SchemeColor(
                                            OpenXML.Drawing.LuminanceModulation(**{'val': '105000'}),
                                            OpenXML.Drawing.SaturationModulation(**{'val': '103000'}),
                                            OpenXML.Drawing.Tint(**{'val': '73000'}),
                                            **{'val': 'phClr'}
                                        ),
                                        **{'pos': '50000'}
                                    ),
                                    OpenXML.Drawing.GradientStop(
                                        OpenXML.Drawing.SchemeColor(
                                            OpenXML.Drawing.LuminanceModulation(**{'val': '105000'}),
                                            OpenXML.Drawing.SaturationModulation(**{'val': '109000'}),
                                            OpenXML.Drawing.Tint(**{'val': '81000'}),
                                            **{'val': 'phClr'}
                                        ),
                                        **{'pos': '100000'}
                                    )
                                ),
                                OpenXML.Drawing.LinearGradientFill(**{'ang': '5400000', 'scaled': '0'}),
                                **{'rotWithShape': '1'}
                            ),
                            OpenXML.Drawing.GradientFill(
                                OpenXML.Drawing.GradientStopList(
                                    OpenXML.Drawing.GradientStop(
                                        OpenXML.Drawing.SchemeColor(
                                            OpenXML.Drawing.SaturationModulation(**{'val': '103000'}),
                                            OpenXML.Drawing.LuminanceModulation(**{'val': '102000'}),
                                            OpenXML.Drawing.Tint(**{'val': '94000'}),
                                            **{'val': 'phClr'}
                                        ),
                                        **{'pos': '0'}
                                    ),
                                    OpenXML.Drawing.GradientStop(
                                        OpenXML.Drawing.SchemeColor(
                                            OpenXML.Drawing.SaturationModulation(**{'val': '110000'}),
                                            OpenXML.Drawing.LuminanceModulation(**{'val': '100000'}),
                                            OpenXML.Drawing.Shade(**{'val': '100000'}),
                                            **{'val': 'phClr'}
                                        ),
                                        **{'pos': '50000'}
                                    ),
                                    OpenXML.Drawing.GradientStop(
                                        OpenXML.Drawing.SchemeColor(
                                            OpenXML.Drawing.LuminanceModulation(**{'val': '99000'}),
                                            OpenXML.Drawing.SaturationModulation(**{'val': '120000'}),
                                            OpenXML.Drawing.Shade(**{'val': '78000'}),
                                            **{'val': 'phClr'}
                                        ),
                                        **{'pos': '100000'}
                                    )
                                ),
                                OpenXML.Drawing.LinearGradientFill(**{'ang': '5400000', 'scaled': '0'}),
                                **{'rotWithShape': '1'}
                            )
                        ),
                        OpenXML.Drawing.LineStyleList(
                            OpenXML.Drawing.Outline(
                                OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'phClr'})),
                                OpenXML.Drawing.PresetDash(**{'val': 'solid'}),
                                OpenXML.Drawing.Miter(**{'lim': '800000'}),
                                **{'w': '12700', 'cap': 'flat', 'cmpd': 'sng', 'algn': 'ctr'}
                            ),
                            OpenXML.Drawing.Outline(
                                OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'phClr'})),
                                OpenXML.Drawing.PresetDash(**{'val': 'solid'}),
                                OpenXML.Drawing.Miter(**{'lim': '800000'}),
                                **{'w': '19050', 'cap': 'flat', 'cmpd': 'sng', 'algn': 'ctr'}
                            ),
                            OpenXML.Drawing.Outline(
                                OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'phClr'})),
                                OpenXML.Drawing.PresetDash(**{'val': 'solid'}),
                                OpenXML.Drawing.Miter(**{'lim': '800000'}),
                                **{'w': '25400', 'cap': 'flat', 'cmpd': 'sng', 'algn': 'ctr'}
                            )
                        ),
                        OpenXML.Drawing.EffectStyleList(
                            OpenXML.Drawing.EffectStyle(OpenXML.Drawing.EffectList()),
                            OpenXML.Drawing.EffectStyle(OpenXML.Drawing.EffectList()),
                            OpenXML.Drawing.EffectStyle(
                                OpenXML.Drawing.EffectList(
                                    OpenXML.Drawing.OuterShadow(
                                        OpenXML.Drawing.RgbColorModelHex(
                                            OpenXML.Drawing.Alpha(**{'val': '63000'}),
                                            **{'val': '000000'}
                                        ),
                                        **{'blurRad': '57150', 'dist': '19050', 'dir': '5400000', 'algn': 'ctr', 'rotWithShape': '0'}
                                    )
                                )
                            )
                        ),
                        OpenXML.Drawing.BackgroundFillStyleList(
                            OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'phClr'})),
                            OpenXML.Drawing.SolidFill(
                                OpenXML.Drawing.SchemeColor(
                                    OpenXML.Drawing.Tint(**{'val': '95000'}),
                                    OpenXML.Drawing.SaturationModulation(**{'val': '170000'}),
                                    **{'val': 'phClr'}
                                )
                            ),
                            OpenXML.Drawing.GradientFill(
                                OpenXML.Drawing.GradientStopList(
                                    OpenXML.Drawing.GradientStop(
                                        OpenXML.Drawing.SchemeColor(
                                            OpenXML.Drawing.Tint(**{'val': '93000'}),
                                            OpenXML.Drawing.SaturationModulation(**{'val': '150000'}),
                                            OpenXML.Drawing.Shade(**{'val': '98000'}),
                                            OpenXML.Drawing.LuminanceModulation(**{'val': '102000'}),
                                            **{'val': 'phClr'}
                                        ),
                                        **{'pos': '0'}
                                    ),
                                    OpenXML.Drawing.GradientStop(
                                        OpenXML.Drawing.SchemeColor(
                                            OpenXML.Drawing.Tint(**{'val': '98000'}),
                                            OpenXML.Drawing.SaturationModulation(**{'val': '130000'}),
                                            OpenXML.Drawing.Shade(**{'val': '90000'}),
                                            OpenXML.Drawing.LuminanceModulation(**{'val': '103000'}),
                                            **{'val': 'phClr'}
                                        ),
                                        **{'pos': '50000'}
                                    ),
                                    OpenXML.Drawing.GradientStop(
                                        OpenXML.Drawing.SchemeColor(
                                            OpenXML.Drawing.Shade(**{'val': '63000'}),
                                            OpenXML.Drawing.SaturationModulation(**{'val': '120000'}),
                                            **{'val': 'phClr'}
                                        ),
                                        **{'pos': '100000'}
                                    )
                                ),
                                OpenXML.Drawing.LinearGradientFill(**{'ang': '5400000', 'scaled': '0'}),
                                **{'rotWithShape': '1'}
                            )
                        ),
                        **{'name': 'Office'}
                    )
                ),
                OpenXML.Drawing.ObjectDefaults(
                    OpenXML.Drawing.LineDefault(
                        OpenXML.Drawing.ShapeProperties(),
                        OpenXML.Drawing.BodyProperties(),
                        OpenXML.Drawing.ListStyle(),
                        OpenXML.Drawing.ShapeStyle(
                            OpenXML.Drawing.LineReference(
                                OpenXML.Drawing.SchemeColor(**{'val': 'accent1'}),
                                **{'idx': '2'}
                            ),
                            OpenXML.Drawing.FillReference(
                                OpenXML.Drawing.SchemeColor(**{'val': 'accent1'}),
                                **{'idx': '0'}
                            ),
                            OpenXML.Drawing.EffectReference(
                                OpenXML.Drawing.SchemeColor(**{'val': 'accent1'}),
                                **{'idx': '1'}
                            ),
                            OpenXML.Drawing.FontReference(
                                OpenXML.Drawing.SchemeColor(**{'val': 'tx1'}),
                                **{'idx': 'minor'}
                            )
                        )
                    )
                ),
                OpenXML.Drawing.ExtraColorSchemeList(),
                OpenXML.Drawing.ExtensionList(
                    OpenXML.Drawing.Extension(
                        OpenXML.THM15.ThemeFamily(
                            **{'name': 'Office Theme', 'id': '{2E142A2C-CD16-42D6-873A-C26D2A0506FA}', 'vid': '{1BDDFF52-6CD6-40A5-AB3C-68EB2F1E4D0A}', 'xmlns:thm15': 'http://schemas.microsoft.com/office/thememl/2012/main'}
                        ),
                        **{'uri': '{05A4C25C-085E-4340-85A3-A5531E510DB2}'}
                    )
                ),
                **{'name': 'Office Theme', 'xmlns:a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
            )),
        OpenXMLPart('ppt/viewProps.xml', 'application/vnd.openxmlformats-officedocument.presentationml.viewProps+xml',
            OpenXML.Presentation.ViewProperties(
                OpenXML.Presentation.NormalViewProperties(
                    OpenXML.Presentation.RestoredLeft(**{'sz': '15621'}),
                    OpenXML.Presentation.RestoredTop(**{'sz': '94658'})
                ),
                OpenXML.Presentation.SlideViewProperties(
                    OpenXML.Presentation.CommonSlideViewProperties(
                        OpenXML.Presentation.CommonViewProperties(
                            OpenXML.Presentation.ScaleFactor(
                                OpenXML.Drawing.ScaleX(**{'n': '120', 'd': '100'}),
                                OpenXML.Drawing.ScaleY(**{'n': '120', 'd': '100'})
                            ),
                            OpenXML.Presentation.Origin(**{'x': '800', 'y': '184'}),
                            **{'varScale': '1'}
                        ),
                        OpenXML.Presentation.GuideList(),
                        **{'snapToGrid': '0'}
                    )
                ),
                OpenXML.Presentation.NotesTextViewProperties(
                    OpenXML.Presentation.CommonViewProperties(
                        OpenXML.Presentation.ScaleFactor(
                            OpenXML.Drawing.ScaleX(**{'n': '1', 'd': '1'}),
                            OpenXML.Drawing.ScaleY(**{'n': '1', 'd': '1'})
                        ),
                        OpenXML.Presentation.Origin(**{'x': '0', 'y': '0'})
                    )
                ),
                OpenXML.Presentation.GridSpacing(**{'cx': '76200', 'cy': '76200'}),
                **{'xmlns:a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'xmlns:r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships', 'xmlns:p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
            )),
        OpenXMLPart('ppt/tableStyles.xml', 'application/vnd.openxmlformats-officedocument.presentationml.tableStyles+xml',
            OpenXML.Drawing.TableStyleList(
                **{'def': '{5C22544A-7EE6-4342-B048-85BDC9FD1C3A}', 'xmlns:a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
            )),
        OpenXMLPart('ppt/presProps.xml', 'application/vnd.openxmlformats-officedocument.presentationml.presProps+xml',
            OpenXML.Presentation.PresentationProperties(
                OpenXML.Presentation.ExtensionListWithModification(
                    OpenXML.Presentation.Extension(
                        OpenXML.Presentation2010.DiscardImageEditData(
                            **{'val': '0', 'xmlns:p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main'}
                        ),
                        **{'uri': '{E76CE94A-603C-4142-B9EB-6D1370010A27}'}
                    ),
                    OpenXML.Presentation.Extension(
                        OpenXML.Presentation2010.DefaultImageDpi(
                            **{'val': '32767', 'xmlns:p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main'}
                        ),
                        **{'uri': '{D31A062A-798A-4329-ABDD-BBA856620510}'}
                    ),
                    OpenXML.Presentation.Extension(
                        OpenXML.Presentation2013.ChartTrackingReferenceBased(
                            **{'val': '1', 'xmlns:p15': 'http://schemas.microsoft.com/office/powerpoint/2012/main'}
                        ),
                        **{'uri': '{FD5EFAAD-0ECE-453E-9831-46B23BE46B34}'}
                    )
                ),
                **{'xmlns:a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'xmlns:r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships', 'xmlns:p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
            )),
        OpenXMLPart('docProps/app.xml', 'application/vnd.openxmlformats-officedocument.extended-properties+xml',
            OpenXML.ExtendedProperties.Properties(
                OpenXML.ExtendedProperties.TotalTime('3'),
                OpenXML.ExtendedProperties.Words('5'),
                OpenXML.ExtendedProperties.Application('Microsoft Macintosh PowerPoint'),
                OpenXML.ExtendedProperties.PresentationFormat('Widescreen'),
                OpenXML.ExtendedProperties.Paragraphs('5'),
                OpenXML.ExtendedProperties.Slides('3'),
                OpenXML.ExtendedProperties.Notes('0'),
                OpenXML.ExtendedProperties.HiddenSlides('0'),
                OpenXML.ExtendedProperties.MultimediaClips('0'),
                OpenXML.ExtendedProperties.ScaleCrop('false'),
                OpenXML.ExtendedProperties.HeadingPairs(
                    OpenXML.VT.VTVector(
                        OpenXML.VT.Variant(OpenXML.VT.VTLPSTR('Fonts Used')),
                        OpenXML.VT.Variant(OpenXML.VT.VTInt32('3')),
                        OpenXML.VT.Variant(OpenXML.VT.VTLPSTR('Theme')),
                        OpenXML.VT.Variant(OpenXML.VT.VTInt32('1')),
                        OpenXML.VT.Variant(OpenXML.VT.VTLPSTR('Slide Titles')),
                        OpenXML.VT.Variant(OpenXML.VT.VTInt32('3')),
                        **{'size': '6', 'baseType': 'variant'}
                    )
                ),
                OpenXML.ExtendedProperties.TitlesOfParts(
                    OpenXML.VT.VTVector(
                        OpenXML.VT.VTLPSTR('Aptos'),
                        OpenXML.VT.VTLPSTR('Aptos Display'),
                        OpenXML.VT.VTLPSTR('Arial'),
                        OpenXML.VT.VTLPSTR('Office Theme'),
                        OpenXML.VT.VTLPSTR('Title'),
                        OpenXML.VT.VTLPSTR('qqqq'),
                        OpenXML.VT.VTLPSTR('PowerPoint Presentation'),
                        **{'size': '7', 'baseType': 'lpstr'}
                    )
                ),
                OpenXML.ExtendedProperties.Company(),
                OpenXML.ExtendedProperties.LinksUpToDate('false'),
                OpenXML.ExtendedProperties.SharedDocument('false'),
                OpenXML.ExtendedProperties.HyperlinksChanged('false'),
                OpenXML.ExtendedProperties.ApplicationVersion('16.0000'),
                **{'xmlns': 'http://schemas.openxmlformats.org/officeDocument/2006/extended-properties', 'xmlns:vt': 'http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes'}
            )),
        OpenXMLPart('docProps/core.xml', 'application/vnd.openxmlformats-package.core-properties+xml',
            OpenXML.CoreProperties.CoreProperties(
                OpenXML.DublinCore.Title(),
                OpenXML.DublinCore.Creator('Boyer, Mark Austin'),
                OpenXML.CoreProperties.LastModifiedBy('Boyer, Mark Austin'),
                OpenXML.CoreProperties.Revision('4'),
                OpenXML.DublinCoreTerms.Created('2026-10-03T11:51:36Z', **{'xsi:type': 'dcterms:W3CDTF'}),
                OpenXML.DublinCoreTerms.Modified('2026-10-03T11:54:40Z', **{'xsi:type': 'dcterms:W3CDTF'}),
                **{'xmlns:cp': 'http://schemas.openxmlformats.org/package/2006/metadata/core-properties', 'xmlns:dc': 'http://purl.org/dc/elements/1.1/', 'xmlns:dcterms': 'http://purl.org/dc/terms/', 'xmlns:dcmitype': 'http://purl.org/dc/dcmitype/', 'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
            )),
    ], content_types=OpenXML.ContentTypes.Types(
        OpenXML.ContentTypes.Default(**{'Extension': 'glb', 'ContentType': 'model/gltf.binary'}),
        OpenXML.ContentTypes.Default(**{'Extension': 'jpeg', 'ContentType': 'image/jpeg'}),
        OpenXML.ContentTypes.Default(**{'Extension': 'png', 'ContentType': 'image/png'}),
        OpenXML.ContentTypes.Default(
            **{'Extension': 'rels', 'ContentType': 'application/vnd.openxmlformats-package.relationships+xml'}
        ),
        OpenXML.ContentTypes.Default(**{'Extension': 'svg', 'ContentType': 'image/svg+xml'}),
        OpenXML.ContentTypes.Default(**{'Extension': 'xml', 'ContentType': 'application/xml'}),
        OpenXML.ContentTypes.Override(
            **{'PartName': '/ppt/presentation.xml', 'ContentType': 'application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml'}
        ),
        OpenXML.ContentTypes.Override(
            **{'PartName': '/ppt/slideMasters/slideMaster1.xml', 'ContentType': 'application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml'}
        ),
        OpenXML.ContentTypes.Override(
            **{'PartName': '/ppt/slides/slide1.xml', 'ContentType': 'application/vnd.openxmlformats-officedocument.presentationml.slide+xml'}
        ),
        OpenXML.ContentTypes.Override(
            **{'PartName': '/ppt/slides/slide2.xml', 'ContentType': 'application/vnd.openxmlformats-officedocument.presentationml.slide+xml'}
        ),
        OpenXML.ContentTypes.Override(
            **{'PartName': '/ppt/slides/slide3.xml', 'ContentType': 'application/vnd.openxmlformats-officedocument.presentationml.slide+xml'}
        ),
        OpenXML.ContentTypes.Override(
            **{'PartName': '/ppt/presProps.xml', 'ContentType': 'application/vnd.openxmlformats-officedocument.presentationml.presProps+xml'}
        ),
        OpenXML.ContentTypes.Override(
            **{'PartName': '/ppt/viewProps.xml', 'ContentType': 'application/vnd.openxmlformats-officedocument.presentationml.viewProps+xml'}
        ),
        OpenXML.ContentTypes.Override(
            **{'PartName': '/ppt/theme/theme1.xml', 'ContentType': 'application/vnd.openxmlformats-officedocument.theme+xml'}
        ),
        OpenXML.ContentTypes.Override(
            **{'PartName': '/ppt/tableStyles.xml', 'ContentType': 'application/vnd.openxmlformats-officedocument.presentationml.tableStyles+xml'}
        ),
        OpenXML.ContentTypes.Override(
            **{'PartName': '/ppt/slideLayouts/slideLayout1.xml', 'ContentType': 'application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml'}
        ),
        OpenXML.ContentTypes.Override(
            **{'PartName': '/ppt/slideLayouts/slideLayout2.xml', 'ContentType': 'application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml'}
        ),
        OpenXML.ContentTypes.Override(
            **{'PartName': '/ppt/slideLayouts/slideLayout3.xml', 'ContentType': 'application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml'}
        ),
        OpenXML.ContentTypes.Override(
            **{'PartName': '/ppt/slideLayouts/slideLayout4.xml', 'ContentType': 'application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml'}
        ),
        OpenXML.ContentTypes.Override(
            **{'PartName': '/ppt/slideLayouts/slideLayout5.xml', 'ContentType': 'application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml'}
        ),
        OpenXML.ContentTypes.Override(
            **{'PartName': '/ppt/slideLayouts/slideLayout6.xml', 'ContentType': 'application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml'}
        ),
        OpenXML.ContentTypes.Override(
            **{'PartName': '/ppt/slideLayouts/slideLayout7.xml', 'ContentType': 'application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml'}
        ),
        OpenXML.ContentTypes.Override(
            **{'PartName': '/ppt/slideLayouts/slideLayout8.xml', 'ContentType': 'application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml'}
        ),
        OpenXML.ContentTypes.Override(
            **{'PartName': '/ppt/slideLayouts/slideLayout9.xml', 'ContentType': 'application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml'}
        ),
        OpenXML.ContentTypes.Override(
            **{'PartName': '/ppt/slideLayouts/slideLayout10.xml', 'ContentType': 'application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml'}
        ),
        OpenXML.ContentTypes.Override(
            **{'PartName': '/ppt/slideLayouts/slideLayout11.xml', 'ContentType': 'application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml'}
        ),
        OpenXML.ContentTypes.Override(
            **{'PartName': '/docProps/core.xml', 'ContentType': 'application/vnd.openxmlformats-package.core-properties+xml'}
        ),
        OpenXML.ContentTypes.Override(
            **{'PartName': '/docProps/app.xml', 'ContentType': 'application/vnd.openxmlformats-officedocument.extended-properties+xml'}
        ),
        **{'xmlns': 'http://schemas.openxmlformats.org/package/2006/content-types'}
    ))
    return PresentationML(
        PresentationMLSlide(
            PresentationMLText(element=OpenXML.Presentation.Shape(
                OpenXML.Presentation.NonVisualShapeProperties(
                    OpenXML.Presentation.NonVisualDrawingProperties(
                        OpenXML.Drawing.ExtensionList(
                            OpenXML.Drawing.Extension(
                                OpenXML.Drawing2014.CreationId(
                                    **{'id': '{4CB4A506-CF6E-4936-04FD-93611A585E80}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                ),
                                **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                            )
                        ),
                        **{'id': '2', 'name': 'Title 1'}
                    ),
                    OpenXML.Presentation.NonVisualShapeDrawingProperties(
                        OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                    ),
                    OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                        OpenXML.Presentation.PlaceholderShape(**{'type': 'ctrTitle'})
                    )
                ),
                OpenXML.Presentation.ShapeProperties(),
                OpenXML.Presentation.TextBody(
                    OpenXML.Drawing.BodyProperties(),
                    OpenXML.Drawing.ListStyle(),
                    OpenXML.Drawing.Paragraph(
                        OpenXML.Drawing.Run(
                            OpenXML.Drawing.RunProperties(**{'lang': 'en-US', 'dirty': '0'}),
                            OpenXML.Drawing.Text('Title')
                        )
                    )
                )
            )),
            PresentationMLText(element=OpenXML.Presentation.Shape(
                OpenXML.Presentation.NonVisualShapeProperties(
                    OpenXML.Presentation.NonVisualDrawingProperties(
                        OpenXML.Drawing.ExtensionList(
                            OpenXML.Drawing.Extension(
                                OpenXML.Drawing2014.CreationId(
                                    **{'id': '{9CD70484-899A-4576-FE44-F5B90B6AF3BA}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                ),
                                **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                            )
                        ),
                        **{'id': '3', 'name': 'Subtitle 2'}
                    ),
                    OpenXML.Presentation.NonVisualShapeDrawingProperties(
                        OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                    ),
                    OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                        OpenXML.Presentation.PlaceholderShape(**{'type': 'subTitle', 'idx': '1'})
                    )
                ),
                OpenXML.Presentation.ShapeProperties(),
                OpenXML.Presentation.TextBody(
                    OpenXML.Drawing.BodyProperties(),
                    OpenXML.Drawing.ListStyle(),
                    OpenXML.Drawing.Paragraph(
                        OpenXML.Drawing.Run(
                            OpenXML.Drawing.RunProperties(**{'lang': 'en-US', 'dirty': '0'}),
                            OpenXML.Drawing.Text('Example')
                        )
                    )
                )
            )),
            PresentationMLShape(element=OpenXML.Presentation.Shape(
                OpenXML.Presentation.NonVisualShapeProperties(
                    OpenXML.Presentation.NonVisualDrawingProperties(
                        OpenXML.Drawing.ExtensionList(
                            OpenXML.Drawing.Extension(
                                OpenXML.Drawing2014.CreationId(
                                    **{'id': '{503135BF-3AD1-E54B-8813-F0B55F87A947}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                ),
                                **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                            )
                        ),
                        **{'id': '4', 'name': 'Rectangle 3'}
                    ),
                    OpenXML.Presentation.NonVisualShapeDrawingProperties(),
                    OpenXML.Presentation.ApplicationNonVisualDrawingProperties()
                ),
                OpenXML.Presentation.ShapeProperties(
                    OpenXML.Drawing.Transform2D(
                        OpenXML.Drawing.Offset(**{'x': '457200', 'y': '435935'}),
                        OpenXML.Drawing.Extents(**{'cx': '1066800', 'cy': '1020725'})
                    ),
                    OpenXML.Drawing.PresetGeometry(OpenXML.Drawing.AdjustValueList(), **{'prst': 'rect'})
                ),
                OpenXML.Presentation.ShapeStyle(
                    OpenXML.Drawing.LineReference(
                        OpenXML.Drawing.SchemeColor(
                            OpenXML.Drawing.Shade(**{'val': '15000'}),
                            **{'val': 'accent1'}
                        ),
                        **{'idx': '2'}
                    ),
                    OpenXML.Drawing.FillReference(
                        OpenXML.Drawing.SchemeColor(**{'val': 'accent1'}),
                        **{'idx': '1'}
                    ),
                    OpenXML.Drawing.EffectReference(
                        OpenXML.Drawing.SchemeColor(**{'val': 'accent1'}),
                        **{'idx': '0'}
                    ),
                    OpenXML.Drawing.FontReference(
                        OpenXML.Drawing.SchemeColor(**{'val': 'lt1'}),
                        **{'idx': 'minor'}
                    )
                ),
                OpenXML.Presentation.TextBody(
                    OpenXML.Drawing.BodyProperties(**{'rtlCol': '0', 'anchor': 'ctr'}),
                    OpenXML.Drawing.ListStyle(),
                    OpenXML.Drawing.Paragraph(
                        OpenXML.Drawing.ParagraphProperties(**{'algn': 'ctr'}),
                        OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                    )
                )
            )),
            PresentationMLShape(element=OpenXML.Presentation.Shape(
                OpenXML.Presentation.NonVisualShapeProperties(
                    OpenXML.Presentation.NonVisualDrawingProperties(
                        OpenXML.Drawing.ExtensionList(
                            OpenXML.Drawing.Extension(
                                OpenXML.Drawing2014.CreationId(
                                    **{'id': '{91B1F89B-0F80-554E-4D2E-2C12402E5F04}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                ),
                                **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                            )
                        ),
                        **{'id': '5', 'name': 'Freeform 4'}
                    ),
                    OpenXML.Presentation.NonVisualShapeDrawingProperties(),
                    OpenXML.Presentation.ApplicationNonVisualDrawingProperties()
                ),
                OpenXML.Presentation.ShapeProperties(
                    OpenXML.Drawing.Transform2D(
                        OpenXML.Drawing.Offset(**{'x': '372140', 'y': '2658140'}),
                        OpenXML.Drawing.Extents(**{'cx': '2232837', 'cy': '1552353'})
                    ),
                    OpenXML.Drawing.CustomGeometry(
                        OpenXML.Drawing.AdjustValueList(),
                        OpenXML.Drawing.ShapeGuideList(
                            OpenXML.Drawing.ShapeGuide(**{'name': 'csX0', 'fmla': '*/ 0 w 2232837'}),
                            OpenXML.Drawing.ShapeGuide(**{'name': 'csY0', 'fmla': '*/ 1190846 h 1552353'}),
                            OpenXML.Drawing.ShapeGuide(**{'name': 'csX1', 'fmla': '*/ 552893 w 2232837'}),
                            OpenXML.Drawing.ShapeGuide(**{'name': 'csY1', 'fmla': '*/ 0 h 1552353'}),
                            OpenXML.Drawing.ShapeGuide(**{'name': 'csX2', 'fmla': '*/ 2232837 w 2232837'}),
                            OpenXML.Drawing.ShapeGuide(**{'name': 'csY2', 'fmla': '*/ 276446 h 1552353'}),
                            OpenXML.Drawing.ShapeGuide(**{'name': 'csX3', 'fmla': '*/ 1977655 w 2232837'}),
                            OpenXML.Drawing.ShapeGuide(**{'name': 'csY3', 'fmla': '*/ 1233376 h 1552353'}),
                            OpenXML.Drawing.ShapeGuide(**{'name': 'csX4', 'fmla': '*/ 967562 w 2232837'}),
                            OpenXML.Drawing.ShapeGuide(**{'name': 'csY4', 'fmla': '*/ 1552353 h 1552353'}),
                            OpenXML.Drawing.ShapeGuide(**{'name': 'csX5', 'fmla': '*/ 925032 w 2232837'}),
                            OpenXML.Drawing.ShapeGuide(**{'name': 'csY5', 'fmla': '*/ 754911 h 1552353'}),
                            OpenXML.Drawing.ShapeGuide(**{'name': 'csX6', 'fmla': '*/ 520995 w 2232837'}),
                            OpenXML.Drawing.ShapeGuide(**{'name': 'csY6', 'fmla': '*/ 1190846 h 1552353'}),
                            OpenXML.Drawing.ShapeGuide(**{'name': 'csX7', 'fmla': '*/ 0 w 2232837'}),
                            OpenXML.Drawing.ShapeGuide(**{'name': 'csY7', 'fmla': '*/ 1190846 h 1552353'})
                        ),
                        OpenXML.Drawing.AdjustHandleList(),
                        OpenXML.Drawing.ConnectionSiteList(
                            OpenXML.Drawing.ConnectionSite(
                                OpenXML.Drawing.Position(**{'x': 'csX0', 'y': 'csY0'}),
                                **{'ang': '0'}
                            ),
                            OpenXML.Drawing.ConnectionSite(
                                OpenXML.Drawing.Position(**{'x': 'csX1', 'y': 'csY1'}),
                                **{'ang': '0'}
                            ),
                            OpenXML.Drawing.ConnectionSite(
                                OpenXML.Drawing.Position(**{'x': 'csX2', 'y': 'csY2'}),
                                **{'ang': '0'}
                            ),
                            OpenXML.Drawing.ConnectionSite(
                                OpenXML.Drawing.Position(**{'x': 'csX3', 'y': 'csY3'}),
                                **{'ang': '0'}
                            ),
                            OpenXML.Drawing.ConnectionSite(
                                OpenXML.Drawing.Position(**{'x': 'csX4', 'y': 'csY4'}),
                                **{'ang': '0'}
                            ),
                            OpenXML.Drawing.ConnectionSite(
                                OpenXML.Drawing.Position(**{'x': 'csX5', 'y': 'csY5'}),
                                **{'ang': '0'}
                            ),
                            OpenXML.Drawing.ConnectionSite(
                                OpenXML.Drawing.Position(**{'x': 'csX6', 'y': 'csY6'}),
                                **{'ang': '0'}
                            ),
                            OpenXML.Drawing.ConnectionSite(
                                OpenXML.Drawing.Position(**{'x': 'csX7', 'y': 'csY7'}),
                                **{'ang': '0'}
                            )
                        ),
                        OpenXML.Drawing.Rectangle(**{'l': 'l', 't': 't', 'r': 'r', 'b': 'b'}),
                        OpenXML.Drawing.PathList(
                            OpenXML.Drawing.PathGradientFill(
                                OpenXML.Drawing.MoveTo(OpenXML.Drawing.Point(**{'x': '0', 'y': '1190846'})),
                                OpenXML.Drawing.LineTo(OpenXML.Drawing.Point(**{'x': '552893', 'y': '0'})),
                                OpenXML.Drawing.LineTo(
                                    OpenXML.Drawing.Point(**{'x': '2232837', 'y': '276446'})
                                ),
                                OpenXML.Drawing.LineTo(
                                    OpenXML.Drawing.Point(**{'x': '1977655', 'y': '1233376'})
                                ),
                                OpenXML.Drawing.LineTo(
                                    OpenXML.Drawing.Point(**{'x': '967562', 'y': '1552353'})
                                ),
                                OpenXML.Drawing.LineTo(OpenXML.Drawing.Point(**{'x': '925032', 'y': '754911'})),
                                OpenXML.Drawing.LineTo(
                                    OpenXML.Drawing.Point(**{'x': '520995', 'y': '1190846'})
                                ),
                                OpenXML.Drawing.LineTo(OpenXML.Drawing.Point(**{'x': '0', 'y': '1190846'})),
                                OpenXML.Drawing.CloseShapePath(),
                                **{'w': '2232837', 'h': '1552353'}
                            )
                        )
                    ),
                    OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'accent5'}))
                ),
                OpenXML.Presentation.ShapeStyle(
                    OpenXML.Drawing.LineReference(
                        OpenXML.Drawing.SchemeColor(
                            OpenXML.Drawing.Shade(**{'val': '15000'}),
                            **{'val': 'accent1'}
                        ),
                        **{'idx': '2'}
                    ),
                    OpenXML.Drawing.FillReference(
                        OpenXML.Drawing.SchemeColor(**{'val': 'accent1'}),
                        **{'idx': '1'}
                    ),
                    OpenXML.Drawing.EffectReference(
                        OpenXML.Drawing.SchemeColor(**{'val': 'accent1'}),
                        **{'idx': '0'}
                    ),
                    OpenXML.Drawing.FontReference(
                        OpenXML.Drawing.SchemeColor(**{'val': 'lt1'}),
                        **{'idx': 'minor'}
                    )
                ),
                OpenXML.Presentation.TextBody(
                    OpenXML.Drawing.BodyProperties(**{'rtlCol': '0', 'anchor': 'ctr'}),
                    OpenXML.Drawing.ListStyle(),
                    OpenXML.Drawing.Paragraph(
                        OpenXML.Drawing.ParagraphProperties(**{'algn': 'ctr'}),
                        OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                    )
                )
            )),
            structure=OpenXML.Presentation.Slide(
                OpenXML.Presentation.CommonSlideData(
                    OpenXML.Presentation.ShapeTree(
                        OpenXML.Presentation.NonVisualGroupShapeProperties(
                            OpenXML.Presentation.NonVisualDrawingProperties(**{'id': '1', 'name': ''}),
                            OpenXML.Presentation.NonVisualGroupShapeDrawingProperties(),
                            OpenXML.Presentation.ApplicationNonVisualDrawingProperties()
                        ),
                        OpenXML.Presentation.GroupShapeProperties(
                            OpenXML.Drawing.Transform2D(
                                OpenXML.Drawing.Offset(**{'x': '0', 'y': '0'}),
                                OpenXML.Drawing.Extents(**{'cx': '0', 'cy': '0'}),
                                OpenXML.Drawing.ChildOffset(**{'x': '0', 'y': '0'}),
                                OpenXML.Drawing.ChildExtents(**{'cx': '0', 'cy': '0'})
                            )
                        )
                    ),
                    OpenXML.Presentation.ExtensionListWithModification(
                        OpenXML.Presentation.Extension(
                            OpenXML.Presentation2010.CreationId(
                                **{'val': '2022917286', 'xmlns:p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main'}
                            ),
                            **{'uri': '{BB962C8B-B14F-4D97-AF65-F5344CB8AC3E}'}
                        )
                    )
                ),
                OpenXML.Presentation.ColorMapOverride(OpenXML.Drawing.MasterColorMapping()),
                **{'xmlns:a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'xmlns:r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships', 'xmlns:p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
            ),
            part_name='ppt/slides/slide1.xml', layout='ppt/slideLayouts/slideLayout1.xml', id=256, relationship_id='rId2',
            relationships=(
                OpenXMLRelationship('rId1', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout', '../slideLayouts/slideLayout1.xml', None),
            ),
        ),
        PresentationMLSlide(
            PresentationMLText(element=OpenXML.Presentation.Shape(
                OpenXML.Presentation.NonVisualShapeProperties(
                    OpenXML.Presentation.NonVisualDrawingProperties(
                        OpenXML.Drawing.ExtensionList(
                            OpenXML.Drawing.Extension(
                                OpenXML.Drawing2014.CreationId(
                                    **{'id': '{9031307B-46F5-943B-F2F4-E6847C35A6BB}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                ),
                                **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                            )
                        ),
                        **{'id': '2', 'name': 'Title 1'}
                    ),
                    OpenXML.Presentation.NonVisualShapeDrawingProperties(
                        OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                    ),
                    OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                        OpenXML.Presentation.PlaceholderShape(**{'type': 'title'})
                    )
                ),
                OpenXML.Presentation.ShapeProperties(),
                OpenXML.Presentation.TextBody(
                    OpenXML.Drawing.BodyProperties(),
                    OpenXML.Drawing.ListStyle(),
                    OpenXML.Drawing.Paragraph(
                        OpenXML.Drawing.Run(
                            OpenXML.Drawing.RunProperties(**{'lang': 'en-US', 'dirty': '0', 'err': '1'}),
                            OpenXML.Drawing.Text('qqqq')
                        ),
                        OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US', 'dirty': '0'})
                    )
                )
            )),
            PresentationMLText(element=OpenXML.Presentation.Shape(
                OpenXML.Presentation.NonVisualShapeProperties(
                    OpenXML.Presentation.NonVisualDrawingProperties(
                        OpenXML.Drawing.ExtensionList(
                            OpenXML.Drawing.Extension(
                                OpenXML.Drawing2014.CreationId(
                                    **{'id': '{6269FDF0-2985-0BB2-F683-892C37C43589}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                ),
                                **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                            )
                        ),
                        **{'id': '4', 'name': 'TextBox 3'}
                    ),
                    OpenXML.Presentation.NonVisualShapeDrawingProperties(**{'txBox': '1'}),
                    OpenXML.Presentation.ApplicationNonVisualDrawingProperties()
                ),
                OpenXML.Presentation.ShapeProperties(
                    OpenXML.Drawing.Transform2D(
                        OpenXML.Drawing.Offset(**{'x': '8750595', 'y': '255181'}),
                        OpenXML.Drawing.Extents(**{'cx': '723014', 'cy': '923330'})
                    ),
                    OpenXML.Drawing.PresetGeometry(OpenXML.Drawing.AdjustValueList(), **{'prst': 'rect'}),
                    OpenXML.Drawing.NoFill()
                ),
                OpenXML.Presentation.TextBody(
                    OpenXML.Drawing.BodyProperties(
                        OpenXML.Drawing.ShapeAutoFit(),
                        **{'wrap': 'square', 'rtlCol': '0'}
                    ),
                    OpenXML.Drawing.ListStyle(),
                    OpenXML.Drawing.Paragraph(
                        OpenXML.Drawing.Run(
                            OpenXML.Drawing.RunProperties(**{'lang': 'en-US', 'dirty': '0', 'err': '1'}),
                            OpenXML.Drawing.Text('bbbbbbbbbb')
                        ),
                        OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US', 'dirty': '0'})
                    )
                )
            )),
            PresentationMLModel3D(element=OpenXML.Compatibility.AlternateContent(
                OpenXML.Compatibility.Choice(
                    OpenXML.Presentation.GraphicFrame(
                        OpenXML.Presentation.NonVisualGraphicFrameProperties(
                            OpenXML.Presentation.NonVisualDrawingProperties(
                                OpenXML.Drawing.ExtensionList(
                                    OpenXML.Drawing.Extension(
                                        OpenXML.Drawing2014.CreationId(
                                            **{'id': '{8F013EEC-3375-23BB-9D4F-AF8EC023B116}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                        ),
                                        **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                    )
                                ),
                                **{'id': '5', 'name': '3D Model 4'}
                            ),
                            OpenXML.Presentation.NonVisualGraphicFrameDrawingProperties(
                                OpenXML.Drawing.GraphicFrameLocks(**{'noChangeAspect': '1'})
                            ),
                            OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                OpenXML.Presentation.ExtensionListWithModification(
                                    OpenXML.Presentation.Extension(
                                        OpenXML.Presentation2010.ModificationId(
                                            **{'val': '1106248948', 'xmlns:p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main'}
                                        ),
                                        **{'uri': '{D42A27DB-BD31-4B8C-83A1-F6EECF244321}'}
                                    )
                                )
                            )
                        ),
                        OpenXML.Presentation.Transform(
                            OpenXML.Drawing.Offset(**{'x': '1482381', 'y': '2568790'}),
                            OpenXML.Drawing.Extents(**{'cx': '4421321', 'cy': '2980474'})
                        ),
                        OpenXML.Drawing.Graphic(
                            OpenXML.Drawing.GraphicData(
                                OpenXML.Model3D.Model3D(
                                    OpenXML.Model3D.ShapeProperties(
                                        OpenXML.Drawing.Transform2D(
                                            OpenXML.Drawing.Offset(**{'x': '0', 'y': '0'}),
                                            OpenXML.Drawing.Extents(**{'cx': '4421321', 'cy': '2980474'})
                                        ),
                                        OpenXML.Drawing.PresetGeometry(
                                            OpenXML.Drawing.AdjustValueList(),
                                            **{'prst': 'rect'}
                                        )
                                    ),
                                    OpenXML.Model3D.Camera(
                                        OpenXML.Model3D.Position(**{'x': '0', 'y': '0', 'z': '58145205'}),
                                        OpenXML.Model3D.Up(**{'dx': '0', 'dy': '36000000', 'dz': '0'}),
                                        OpenXML.Model3D.LookAt(**{'x': '0', 'y': '0', 'z': '0'}),
                                        OpenXML.Model3D.Perspective(**{'fov': '2700000'})
                                    ),
                                    OpenXML.Model3D.Transform(
                                        OpenXML.Model3D.MeterPerModelUnit(**{'n': '101530', 'd': '1000000'}),
                                        OpenXML.Model3D.PreTranslate(
                                            **{'dx': '-2630557', 'dy': '339751', 'dz': '1084686'}
                                        ),
                                        OpenXML.Model3D.Scale(
                                            OpenXML.Model3D.ScaleX(**{'n': '1000000', 'd': '1000000'}),
                                            OpenXML.Model3D.ScaleY(**{'n': '1000000', 'd': '1000000'}),
                                            OpenXML.Model3D.ScaleZ(**{'n': '1000000', 'd': '1000000'})
                                        ),
                                        OpenXML.Model3D.Rotate3D(),
                                        OpenXML.Model3D.PostTranslate(**{'dx': '0', 'dy': '0', 'dz': '0'})
                                    ),
                                    OpenXML.Model3D.Model3DRaster(
                                        OpenXML.Model3D.Blip(**{'r:embed': 'rId3'}),
                                        **{'rName': 'Office3DRenderer', 'rVer': '16.0.8326'}
                                    ),
                                    OpenXML.Model3D.ExtensionList(
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Model3DAnimation.EmbeddedAnimation(
                                                OpenXML.Model3DAnimation.AnimationProperties(
                                                    **{'length': '2000', 'count': 'indefinite'}
                                                ),
                                                **{'animId': '0', 'xmlns:a3danim': 'http://schemas.microsoft.com/office/drawing/2018/animation/model3d'}
                                            ),
                                            **{'uri': '{9A65AA19-BECB-4387-8358-8AD5134E1D82}'}
                                        ),
                                        OpenXML.Drawing.Extension(
                                            OpenXML.Model3DAnimation.PosterFrame(
                                                **{'animId': '0', 'xmlns:a3danim': 'http://schemas.microsoft.com/office/drawing/2018/animation/model3d'}
                                            ),
                                            **{'uri': '{E9DE012E-A134-456F-84FE-255F9AAD75C6}'}
                                        )
                                    ),
                                    OpenXML.Model3D.ObjectViewport(**{'viewportSz': '5418667'}),
                                    OpenXML.Model3D.AmbientLight(
                                        OpenXML.Model3D.Color(
                                            OpenXML.Drawing.RgbColorModelPercentage(
                                                **{'r': '50000', 'g': '50000', 'b': '50000'}
                                            )
                                        ),
                                        OpenXML.Model3D.IlluminancePositiveRatio(
                                            **{'n': '500000', 'd': '1000000'}
                                        )
                                    ),
                                    OpenXML.Model3D.PointLight(
                                        OpenXML.Model3D.Color(
                                            OpenXML.Drawing.RgbColorModelPercentage(
                                                **{'r': '100000', 'g': '75000', 'b': '50000'}
                                            )
                                        ),
                                        OpenXML.Model3D.IntensityPositiveRatio(
                                            **{'n': '9765625', 'd': '1000000'}
                                        ),
                                        OpenXML.Model3D.Position(
                                            **{'x': '21959998', 'y': '70920001', 'z': '16344003'}
                                        ),
                                        **{'rad': '0'}
                                    ),
                                    OpenXML.Model3D.PointLight(
                                        OpenXML.Model3D.Color(
                                            OpenXML.Drawing.RgbColorModelPercentage(
                                                **{'r': '40000', 'g': '60000', 'b': '95000'}
                                            )
                                        ),
                                        OpenXML.Model3D.IntensityPositiveRatio(
                                            **{'n': '12250000', 'd': '1000000'}
                                        ),
                                        OpenXML.Model3D.Position(
                                            **{'x': '-37964106', 'y': '51130435', 'z': '57631972'}
                                        ),
                                        **{'rad': '0'}
                                    ),
                                    OpenXML.Model3D.PointLight(
                                        OpenXML.Model3D.Color(
                                            OpenXML.Drawing.RgbColorModelPercentage(
                                                **{'r': '86837', 'g': '72700', 'b': '100000'}
                                            )
                                        ),
                                        OpenXML.Model3D.IntensityPositiveRatio(
                                            **{'n': '3125000', 'd': '1000000'}
                                        ),
                                        OpenXML.Model3D.Position(
                                            **{'x': '-37739122', 'y': '58056624', 'z': '-34769649'}
                                        ),
                                        **{'rad': '0'}
                                    ),
                                    **{'r:embed': 'rId2'}
                                ),
                                **{'uri': 'http://schemas.microsoft.com/office/drawing/2017/model3d'}
                            )
                        )
                    ),
                    **{'Requires': 'am3d', 'xmlns:am3d': 'http://schemas.microsoft.com/office/drawing/2017/model3d'}
                ),
                OpenXML.Compatibility.Fallback(
                    OpenXML.Presentation.Picture(
                        OpenXML.Presentation.NonVisualPictureProperties(
                            OpenXML.Presentation.NonVisualDrawingProperties(
                                OpenXML.Drawing.ExtensionList(
                                    OpenXML.Drawing.Extension(
                                        OpenXML.Drawing2014.CreationId(
                                            **{'id': '{8F013EEC-3375-23BB-9D4F-AF8EC023B116}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                        ),
                                        **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                    )
                                ),
                                **{'id': '5', 'name': '3D Model 4'}
                            ),
                            OpenXML.Presentation.NonVisualPictureDrawingProperties(
                                OpenXML.Drawing.PictureLocks(
                                    **{'noGrp': '1', 'noRot': '1', 'noChangeAspect': '1', 'noMove': '1', 'noResize': '1', 'noEditPoints': '1', 'noAdjustHandles': '1', 'noChangeArrowheads': '1', 'noChangeShapeType': '1', 'noCrop': '1'}
                                )
                            ),
                            OpenXML.Presentation.ApplicationNonVisualDrawingProperties()
                        ),
                        OpenXML.Presentation.BlipFill(
                            OpenXML.Drawing.Blip(**{'r:embed': 'rId3'}),
                            OpenXML.Drawing.Stretch(OpenXML.Drawing.FillRectangle())
                        ),
                        OpenXML.Presentation.ShapeProperties(
                            OpenXML.Drawing.Transform2D(
                                OpenXML.Drawing.Offset(**{'x': '1482381', 'y': '2568790'}),
                                OpenXML.Drawing.Extents(**{'cx': '4421321', 'cy': '2980474'})
                            ),
                            OpenXML.Drawing.PresetGeometry(OpenXML.Drawing.AdjustValueList(), **{'prst': 'rect'})
                        )
                    )
                ),
                **{'xmlns:mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006'}
            )),
            PresentationMLModel3D(element=OpenXML.Compatibility.AlternateContent(
                OpenXML.Compatibility.Choice(
                    OpenXML.Presentation.GraphicFrame(
                        OpenXML.Presentation.NonVisualGraphicFrameProperties(
                            OpenXML.Presentation.NonVisualDrawingProperties(
                                OpenXML.Drawing.ExtensionList(
                                    OpenXML.Drawing.Extension(
                                        OpenXML.Drawing2014.CreationId(
                                            **{'id': '{D8BED147-1C89-DED1-DB5F-DAFAC3D0D7E2}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                        ),
                                        **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                    )
                                ),
                                **{'id': '6', 'name': '3D Model 5'}
                            ),
                            OpenXML.Presentation.NonVisualGraphicFrameDrawingProperties(
                                OpenXML.Drawing.GraphicFrameLocks(**{'noChangeAspect': '1'})
                            ),
                            OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                                OpenXML.Presentation.ExtensionListWithModification(
                                    OpenXML.Presentation.Extension(
                                        OpenXML.Presentation2010.ModificationId(
                                            **{'val': '3482784002', 'xmlns:p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main'}
                                        ),
                                        **{'uri': '{D42A27DB-BD31-4B8C-83A1-F6EECF244321}'}
                                    )
                                )
                            )
                        ),
                        OpenXML.Presentation.Transform(
                            OpenXML.Drawing.Offset(**{'x': '7403013', 'y': '2568790'}),
                            OpenXML.Drawing.Extents(**{'cx': '4403461', 'cy': '2975060'})
                        ),
                        OpenXML.Drawing.Graphic(
                            OpenXML.Drawing.GraphicData(
                                OpenXML.Model3D.Model3D(
                                    OpenXML.Model3D.ShapeProperties(
                                        OpenXML.Drawing.Transform2D(
                                            OpenXML.Drawing.Offset(**{'x': '0', 'y': '0'}),
                                            OpenXML.Drawing.Extents(**{'cx': '4403461', 'cy': '2975060'})
                                        ),
                                        OpenXML.Drawing.PresetGeometry(
                                            OpenXML.Drawing.AdjustValueList(),
                                            **{'prst': 'rect'}
                                        )
                                    ),
                                    OpenXML.Model3D.Camera(
                                        OpenXML.Model3D.Position(**{'x': '0', 'y': '0', 'z': '63745533'}),
                                        OpenXML.Model3D.Up(**{'dx': '0', 'dy': '36000000', 'dz': '0'}),
                                        OpenXML.Model3D.LookAt(**{'x': '0', 'y': '0', 'z': '0'}),
                                        OpenXML.Model3D.Perspective(**{'fov': '2700000'})
                                    ),
                                    OpenXML.Model3D.Transform(
                                        OpenXML.Model3D.MeterPerModelUnit(**{'n': '120471', 'd': '1000000'}),
                                        OpenXML.Model3D.PreTranslate(
                                            **{'dx': '27616', 'dy': '-616635', 'dz': '1945449'}
                                        ),
                                        OpenXML.Model3D.Scale(
                                            OpenXML.Model3D.ScaleX(**{'n': '1000000', 'd': '1000000'}),
                                            OpenXML.Model3D.ScaleY(**{'n': '1000000', 'd': '1000000'}),
                                            OpenXML.Model3D.ScaleZ(**{'n': '1000000', 'd': '1000000'})
                                        ),
                                        OpenXML.Model3D.Rotate3D(),
                                        OpenXML.Model3D.PostTranslate(**{'dx': '0', 'dy': '0', 'dz': '0'})
                                    ),
                                    OpenXML.Model3D.Model3DRaster(
                                        OpenXML.Model3D.Blip(**{'r:embed': 'rId5'}),
                                        **{'rName': 'Office3DRenderer', 'rVer': '16.0.8326'}
                                    ),
                                    OpenXML.Model3D.ObjectViewport(**{'viewportSz': '5418665'}),
                                    OpenXML.Model3D.AmbientLight(
                                        OpenXML.Model3D.Color(
                                            OpenXML.Drawing.RgbColorModelPercentage(
                                                **{'r': '50000', 'g': '50000', 'b': '50000'}
                                            )
                                        ),
                                        OpenXML.Model3D.IlluminancePositiveRatio(
                                            **{'n': '500000', 'd': '1000000'}
                                        )
                                    ),
                                    OpenXML.Model3D.PointLight(
                                        OpenXML.Model3D.Color(
                                            OpenXML.Drawing.RgbColorModelPercentage(
                                                **{'r': '100000', 'g': '75000', 'b': '50000'}
                                            )
                                        ),
                                        OpenXML.Model3D.IntensityPositiveRatio(
                                            **{'n': '9765625', 'd': '1000000'}
                                        ),
                                        OpenXML.Model3D.Position(
                                            **{'x': '21959998', 'y': '70920001', 'z': '16344003'}
                                        ),
                                        **{'rad': '0'}
                                    ),
                                    OpenXML.Model3D.PointLight(
                                        OpenXML.Model3D.Color(
                                            OpenXML.Drawing.RgbColorModelPercentage(
                                                **{'r': '40000', 'g': '60000', 'b': '95000'}
                                            )
                                        ),
                                        OpenXML.Model3D.IntensityPositiveRatio(
                                            **{'n': '12250000', 'd': '1000000'}
                                        ),
                                        OpenXML.Model3D.Position(
                                            **{'x': '-37964106', 'y': '51130435', 'z': '57631972'}
                                        ),
                                        **{'rad': '0'}
                                    ),
                                    OpenXML.Model3D.PointLight(
                                        OpenXML.Model3D.Color(
                                            OpenXML.Drawing.RgbColorModelPercentage(
                                                **{'r': '86837', 'g': '72700', 'b': '100000'}
                                            )
                                        ),
                                        OpenXML.Model3D.IntensityPositiveRatio(
                                            **{'n': '3125000', 'd': '1000000'}
                                        ),
                                        OpenXML.Model3D.Position(
                                            **{'x': '-37739122', 'y': '58056624', 'z': '-34769649'}
                                        ),
                                        **{'rad': '0'}
                                    ),
                                    **{'r:embed': 'rId4'}
                                ),
                                **{'uri': 'http://schemas.microsoft.com/office/drawing/2017/model3d'}
                            )
                        )
                    ),
                    **{'Requires': 'am3d', 'xmlns:am3d': 'http://schemas.microsoft.com/office/drawing/2017/model3d'}
                ),
                OpenXML.Compatibility.Fallback(
                    OpenXML.Presentation.Picture(
                        OpenXML.Presentation.NonVisualPictureProperties(
                            OpenXML.Presentation.NonVisualDrawingProperties(
                                OpenXML.Drawing.ExtensionList(
                                    OpenXML.Drawing.Extension(
                                        OpenXML.Drawing2014.CreationId(
                                            **{'id': '{D8BED147-1C89-DED1-DB5F-DAFAC3D0D7E2}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                        ),
                                        **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                                    )
                                ),
                                **{'id': '6', 'name': '3D Model 5'}
                            ),
                            OpenXML.Presentation.NonVisualPictureDrawingProperties(
                                OpenXML.Drawing.PictureLocks(
                                    **{'noGrp': '1', 'noRot': '1', 'noChangeAspect': '1', 'noMove': '1', 'noResize': '1', 'noEditPoints': '1', 'noAdjustHandles': '1', 'noChangeArrowheads': '1', 'noChangeShapeType': '1', 'noCrop': '1'}
                                )
                            ),
                            OpenXML.Presentation.ApplicationNonVisualDrawingProperties()
                        ),
                        OpenXML.Presentation.BlipFill(
                            OpenXML.Drawing.Blip(**{'r:embed': 'rId5'}),
                            OpenXML.Drawing.Stretch(OpenXML.Drawing.FillRectangle())
                        ),
                        OpenXML.Presentation.ShapeProperties(
                            OpenXML.Drawing.Transform2D(
                                OpenXML.Drawing.Offset(**{'x': '7403013', 'y': '2568790'}),
                                OpenXML.Drawing.Extents(**{'cx': '4403461', 'cy': '2975060'})
                            ),
                            OpenXML.Drawing.PresetGeometry(OpenXML.Drawing.AdjustValueList(), **{'prst': 'rect'})
                        )
                    )
                ),
                **{'xmlns:mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006'}
            )),
            structure=OpenXML.Presentation.Slide(
                OpenXML.Presentation.CommonSlideData(
                    OpenXML.Presentation.ShapeTree(
                        OpenXML.Presentation.NonVisualGroupShapeProperties(
                            OpenXML.Presentation.NonVisualDrawingProperties(**{'id': '1', 'name': ''}),
                            OpenXML.Presentation.NonVisualGroupShapeDrawingProperties(),
                            OpenXML.Presentation.ApplicationNonVisualDrawingProperties()
                        ),
                        OpenXML.Presentation.GroupShapeProperties(
                            OpenXML.Drawing.Transform2D(
                                OpenXML.Drawing.Offset(**{'x': '0', 'y': '0'}),
                                OpenXML.Drawing.Extents(**{'cx': '0', 'cy': '0'}),
                                OpenXML.Drawing.ChildOffset(**{'x': '0', 'y': '0'}),
                                OpenXML.Drawing.ChildExtents(**{'cx': '0', 'cy': '0'})
                            )
                        )
                    ),
                    OpenXML.Presentation.ExtensionListWithModification(
                        OpenXML.Presentation.Extension(
                            OpenXML.Presentation2010.CreationId(
                                **{'val': '4199645439', 'xmlns:p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main'}
                            ),
                            **{'uri': '{BB962C8B-B14F-4D97-AF65-F5344CB8AC3E}'}
                        )
                    )
                ),
                OpenXML.Presentation.ColorMapOverride(OpenXML.Drawing.MasterColorMapping()),
                OpenXML.Presentation.Timing(
                    OpenXML.Presentation.TimeNodeList(
                        OpenXML.Presentation.ParallelTimeNode(
                            OpenXML.Presentation.CommonTimeNode(
                                OpenXML.Presentation.ChildTimeNodeList(
                                    OpenXML.Presentation.SequenceTimeNode(
                                        OpenXML.Presentation.CommonTimeNode(
                                            OpenXML.Presentation.ChildTimeNodeList(
                                                OpenXML.Presentation.ParallelTimeNode(
                                                    OpenXML.Presentation.CommonTimeNode(
                                                        OpenXML.Presentation.StartConditionList(
                                                            OpenXML.Presentation.Condition(
                                                                **{'delay': 'indefinite'}
                                                            ),
                                                            OpenXML.Presentation.Condition(
                                                                OpenXML.Presentation.TimeNode(**{'val': '2'}),
                                                                **{'evt': 'onBegin', 'delay': '0'}
                                                            )
                                                        ),
                                                        OpenXML.Presentation.ChildTimeNodeList(
                                                            OpenXML.Presentation.ParallelTimeNode(
                                                                OpenXML.Presentation.CommonTimeNode(
                                                                    OpenXML.Presentation.StartConditionList(
                                                                        OpenXML.Presentation.Condition(
                                                                            **{'delay': '0'}
                                                                        )
                                                                    ),
                                                                    OpenXML.Presentation.ChildTimeNodeList(
                                                                        OpenXML.Presentation.ParallelTimeNode(
                                                                            OpenXML.Presentation.CommonTimeNode(
                                                                                OpenXML.Presentation.StartConditionList(
                                                                                    OpenXML.Presentation.Condition(
                                                                                        **{'delay': '0'}
                                                                                    )
                                                                                ),
                                                                                OpenXML.Presentation.ChildTimeNodeList(
                                                                                    OpenXML.Presentation.Animate(
                                                                                        OpenXML.Presentation.CommonBehavior(
                                                                                            OpenXML.Presentation.CommonTimeNode(
                                                                                                **{'id': '6', 'dur': '2000', 'fill': 'hold'}
                                                                                            ),
                                                                                            OpenXML.Presentation.TargetElement(
                                                                                                OpenXML.Presentation.ShapeTarget(
                                                                                                    **{'spid': '5'}
                                                                                                )
                                                                                            ),
                                                                                            OpenXML.Presentation.AttributeNameList(
                                                                                                OpenXML.Presentation.AttributeName(
                                                                                                    'embedded1'
                                                                                                )
                                                                                            )
                                                                                        ),
                                                                                        OpenXML.Presentation.TimeAnimateValueList(
                                                                                            OpenXML.Presentation.TimeAnimateValue(
                                                                                                OpenXML.Presentation.VariantValue(
                                                                                                    OpenXML.Presentation.FloatVariantValue(
                                                                                                        **{'val': '0'}
                                                                                                    )
                                                                                                ),
                                                                                                **{'tm': '0'}
                                                                                            ),
                                                                                            OpenXML.Presentation.TimeAnimateValue(
                                                                                                OpenXML.Presentation.VariantValue(
                                                                                                    OpenXML.Presentation.FloatVariantValue(
                                                                                                        **{'val': '1'}
                                                                                                    )
                                                                                                ),
                                                                                                **{'tm': '100000'}
                                                                                            )
                                                                                        ),
                                                                                        **{'calcmode': 'lin', 'valueType': 'num'}
                                                                                    )
                                                                                ),
                                                                                **{'id': '5', 'presetID': '100', 'presetClass': 'emph', 'presetSubtype': '1', 'repeatCount': 'indefinite', 'fill': 'hold', 'nodeType': 'withEffect'}
                                                                            )
                                                                        )
                                                                    ),
                                                                    **{'id': '4', 'fill': 'hold'}
                                                                )
                                                            )
                                                        ),
                                                        **{'id': '3', 'fill': 'hold'}
                                                    )
                                                )
                                            ),
                                            **{'id': '2', 'dur': 'indefinite', 'nodeType': 'mainSeq'}
                                        ),
                                        OpenXML.Presentation.PreviousConditionList(
                                            OpenXML.Presentation.Condition(
                                                OpenXML.Presentation.TargetElement(
                                                    OpenXML.Presentation.SlideTarget()
                                                ),
                                                **{'evt': 'onPrev', 'delay': '0'}
                                            )
                                        ),
                                        OpenXML.Presentation.NextConditionList(
                                            OpenXML.Presentation.Condition(
                                                OpenXML.Presentation.TargetElement(
                                                    OpenXML.Presentation.SlideTarget()
                                                ),
                                                **{'evt': 'onNext', 'delay': '0'}
                                            )
                                        ),
                                        **{'concurrent': '1', 'nextAc': 'seek'}
                                    )
                                ),
                                **{'id': '1', 'dur': 'indefinite', 'restart': 'never', 'nodeType': 'tmRoot'}
                            )
                        )
                    )
                ),
                **{'xmlns:a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'xmlns:r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships', 'xmlns:p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
            ),
            part_name='ppt/slides/slide2.xml', layout='ppt/slideLayouts/slideLayout2.xml', id=257, relationship_id='rId3',
            relationships=(
                OpenXMLRelationship('rId3', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image', '../media/image1.png', None),
                OpenXMLRelationship('rId2', 'http://schemas.microsoft.com/office/2017/06/relationships/model3d', '../media/model3d1.glb', None),
                OpenXMLRelationship('rId1', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout', '../slideLayouts/slideLayout2.xml', None),
                OpenXMLRelationship('rId5', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image', '../media/image2.png', None),
                OpenXMLRelationship('rId4', 'http://schemas.microsoft.com/office/2017/06/relationships/model3d', '../media/model3d2.glb', None),
            ),
        ),
        PresentationMLSlide(
            PresentationMLText(element=OpenXML.Presentation.Shape(
                OpenXML.Presentation.NonVisualShapeProperties(
                    OpenXML.Presentation.NonVisualDrawingProperties(
                        OpenXML.Drawing.ExtensionList(
                            OpenXML.Drawing.Extension(
                                OpenXML.Drawing2014.CreationId(
                                    **{'id': '{FFE916E4-9F24-5FD1-80C8-5F4EC2C41D95}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                ),
                                **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                            )
                        ),
                        **{'id': '2', 'name': 'Title 1'}
                    ),
                    OpenXML.Presentation.NonVisualShapeDrawingProperties(
                        OpenXML.Drawing.ShapeLocks(**{'noGrp': '1'})
                    ),
                    OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                        OpenXML.Presentation.PlaceholderShape(**{'type': 'title'})
                    )
                ),
                OpenXML.Presentation.ShapeProperties(),
                OpenXML.Presentation.TextBody(
                    OpenXML.Drawing.BodyProperties(),
                    OpenXML.Drawing.ListStyle(),
                    OpenXML.Drawing.Paragraph(OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'}))
                )
            )),
            PresentationMLImage(element=OpenXML.Presentation.Picture(
                OpenXML.Presentation.NonVisualPictureProperties(
                    OpenXML.Presentation.NonVisualDrawingProperties(
                        OpenXML.Drawing.ExtensionList(
                            OpenXML.Drawing.Extension(
                                OpenXML.Drawing2014.CreationId(
                                    **{'id': '{5F4A2643-146B-CFE6-E3FA-52080B42CB6F}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                ),
                                **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                            )
                        ),
                        **{'id': '5', 'name': 'Content Placeholder 4'}
                    ),
                    OpenXML.Presentation.NonVisualPictureDrawingProperties(
                        OpenXML.Drawing.PictureLocks(**{'noGrp': '1', 'noChangeAspect': '1'})
                    ),
                    OpenXML.Presentation.ApplicationNonVisualDrawingProperties(
                        OpenXML.Presentation.PlaceholderShape(**{'idx': '1'})
                    )
                ),
                OpenXML.Presentation.BlipFill(
                    OpenXML.Drawing.Blip(
                        OpenXML.Drawing.ExtensionList(
                            OpenXML.Drawing.Extension(
                                OpenXML.SVG.SVGBlip(
                                    **{'r:embed': 'rId2', 'xmlns:asvg': 'http://schemas.microsoft.com/office/drawing/2016/SVG/main'}
                                ),
                                **{'uri': '{96DAC541-7B7A-43D3-8B79-37D633B846F1}'}
                            )
                        )
                    ),
                    OpenXML.Drawing.Stretch(OpenXML.Drawing.FillRectangle())
                ),
                OpenXML.Presentation.ShapeProperties(
                    OpenXML.Drawing.Transform2D(
                        OpenXML.Drawing.Offset(**{'x': '5594350', 'y': '3944144'}),
                        OpenXML.Drawing.Extents(**{'cx': '1003300', 'cy': '114300'})
                    ),
                    OpenXML.Drawing.PresetGeometry(OpenXML.Drawing.AdjustValueList(), **{'prst': 'rect'})
                )
            )),
            PresentationMLImage(element=OpenXML.Presentation.Picture(
                OpenXML.Presentation.NonVisualPictureProperties(
                    OpenXML.Presentation.NonVisualDrawingProperties(
                        OpenXML.Drawing.ExtensionList(
                            OpenXML.Drawing.Extension(
                                OpenXML.Drawing2014.CreationId(
                                    **{'id': '{5B5FF695-BABC-4607-9421-B494ECEC8D31}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                ),
                                **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                            )
                        ),
                        **{'id': '6', 'name': 'Picture 5'}
                    ),
                    OpenXML.Presentation.NonVisualPictureDrawingProperties(
                        OpenXML.Drawing.PictureLocks(**{'noChangeAspect': '1'})
                    ),
                    OpenXML.Presentation.ApplicationNonVisualDrawingProperties()
                ),
                OpenXML.Presentation.BlipFill(
                    OpenXML.Drawing.Blip(**{'r:embed': 'rId3'}),
                    OpenXML.Drawing.SourceRectangle(**{'t': '3920'}),
                    OpenXML.Drawing.Stretch(OpenXML.Drawing.FillRectangle())
                ),
                OpenXML.Presentation.ShapeProperties(
                    OpenXML.Drawing.Transform2D(
                        OpenXML.Drawing.Offset(**{'x': '578779', 'y': '5101398'}),
                        OpenXML.Drawing.Extents(**{'cx': '3864900', 'cy': '1323628'})
                    ),
                    OpenXML.Drawing.PresetGeometry(OpenXML.Drawing.AdjustValueList(), **{'prst': 'rect'})
                )
            )),
            PresentationMLShape(element=OpenXML.Presentation.Shape(
                OpenXML.Presentation.NonVisualShapeProperties(
                    OpenXML.Presentation.NonVisualDrawingProperties(
                        OpenXML.Drawing.ExtensionList(
                            OpenXML.Drawing.Extension(
                                OpenXML.Drawing2014.CreationId(
                                    **{'id': '{CAC475A0-B819-F668-087F-0C6DBAA3243B}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                ),
                                **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                            )
                        ),
                        **{'id': '7', 'name': 'Triangle 6'}
                    ),
                    OpenXML.Presentation.NonVisualShapeDrawingProperties(),
                    OpenXML.Presentation.ApplicationNonVisualDrawingProperties()
                ),
                OpenXML.Presentation.ShapeProperties(
                    OpenXML.Drawing.Transform2D(
                        OpenXML.Drawing.Offset(**{'x': '3225114', 'y': '4856205'}),
                        OpenXML.Drawing.Extents(**{'cx': '1964724', 'cy': '1532238'})
                    ),
                    OpenXML.Drawing.PresetGeometry(OpenXML.Drawing.AdjustValueList(), **{'prst': 'triangle'}),
                    OpenXML.Drawing.NoFill(),
                    OpenXML.Drawing.Outline(
                        OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'accent3'})),
                        OpenXML.Drawing.PresetDash(**{'val': 'lgDashDot'}),
                        **{'w': '76200'}
                    )
                ),
                OpenXML.Presentation.ShapeStyle(
                    OpenXML.Drawing.LineReference(
                        OpenXML.Drawing.SchemeColor(
                            OpenXML.Drawing.Shade(**{'val': '15000'}),
                            **{'val': 'accent1'}
                        ),
                        **{'idx': '2'}
                    ),
                    OpenXML.Drawing.FillReference(
                        OpenXML.Drawing.SchemeColor(**{'val': 'accent1'}),
                        **{'idx': '1'}
                    ),
                    OpenXML.Drawing.EffectReference(
                        OpenXML.Drawing.SchemeColor(**{'val': 'accent1'}),
                        **{'idx': '0'}
                    ),
                    OpenXML.Drawing.FontReference(
                        OpenXML.Drawing.SchemeColor(**{'val': 'lt1'}),
                        **{'idx': 'minor'}
                    )
                ),
                OpenXML.Presentation.TextBody(
                    OpenXML.Drawing.BodyProperties(**{'rtlCol': '0', 'anchor': 'ctr'}),
                    OpenXML.Drawing.ListStyle(),
                    OpenXML.Drawing.Paragraph(
                        OpenXML.Drawing.ParagraphProperties(**{'algn': 'ctr'}),
                        OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                    )
                )
            )),
            PresentationMLShape(element=OpenXML.Presentation.Shape(
                OpenXML.Presentation.NonVisualShapeProperties(
                    OpenXML.Presentation.NonVisualDrawingProperties(
                        OpenXML.Drawing.ExtensionList(
                            OpenXML.Drawing.Extension(
                                OpenXML.Drawing2014.CreationId(
                                    **{'id': '{48E921B7-DFAA-A15F-1FD7-F761DB666DE3}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                ),
                                **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                            )
                        ),
                        **{'id': '8', 'name': 'Right Brace 7'}
                    ),
                    OpenXML.Presentation.NonVisualShapeDrawingProperties(),
                    OpenXML.Presentation.ApplicationNonVisualDrawingProperties()
                ),
                OpenXML.Presentation.ShapeProperties(
                    OpenXML.Drawing.Transform2D(
                        OpenXML.Drawing.Offset(**{'x': '8155172', 'y': '2796363'}),
                        OpenXML.Drawing.Extents(**{'cx': '350875', 'cy': '2059842'})
                    ),
                    OpenXML.Drawing.PresetGeometry(OpenXML.Drawing.AdjustValueList(), **{'prst': 'rightBrace'})
                ),
                OpenXML.Presentation.ShapeStyle(
                    OpenXML.Drawing.LineReference(
                        OpenXML.Drawing.SchemeColor(**{'val': 'accent1'}),
                        **{'idx': '2'}
                    ),
                    OpenXML.Drawing.FillReference(
                        OpenXML.Drawing.SchemeColor(**{'val': 'accent1'}),
                        **{'idx': '0'}
                    ),
                    OpenXML.Drawing.EffectReference(
                        OpenXML.Drawing.SchemeColor(**{'val': 'accent1'}),
                        **{'idx': '1'}
                    ),
                    OpenXML.Drawing.FontReference(
                        OpenXML.Drawing.SchemeColor(**{'val': 'tx1'}),
                        **{'idx': 'minor'}
                    )
                ),
                OpenXML.Presentation.TextBody(
                    OpenXML.Drawing.BodyProperties(**{'rtlCol': '0', 'anchor': 'ctr'}),
                    OpenXML.Drawing.ListStyle(),
                    OpenXML.Drawing.Paragraph(
                        OpenXML.Drawing.ParagraphProperties(**{'algn': 'ctr'}),
                        OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US'})
                    )
                )
            )),
            PresentationMLText(element=OpenXML.Presentation.Shape(
                OpenXML.Presentation.NonVisualShapeProperties(
                    OpenXML.Presentation.NonVisualDrawingProperties(
                        OpenXML.Drawing.ExtensionList(
                            OpenXML.Drawing.Extension(
                                OpenXML.Drawing2014.CreationId(
                                    **{'id': '{7866B1D7-9C21-9EFC-1B4A-2EDB64A1F50F}', 'xmlns:a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}
                                ),
                                **{'uri': '{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}'}
                            )
                        ),
                        **{'id': '9', 'name': 'TextBox 8'}
                    ),
                    OpenXML.Presentation.NonVisualShapeDrawingProperties(**{'txBox': '1'}),
                    OpenXML.Presentation.ApplicationNonVisualDrawingProperties()
                ),
                OpenXML.Presentation.ShapeProperties(
                    OpenXML.Drawing.Transform2D(
                        OpenXML.Drawing.Offset(**{'x': '8506047', 'y': '3631962'}),
                        OpenXML.Drawing.Extents(**{'cx': '566117', 'cy': '369332'})
                    ),
                    OpenXML.Drawing.PresetGeometry(OpenXML.Drawing.AdjustValueList(), **{'prst': 'rect'}),
                    OpenXML.Drawing.NoFill()
                ),
                OpenXML.Presentation.TextBody(
                    OpenXML.Drawing.BodyProperties(
                        OpenXML.Drawing.ShapeAutoFit(),
                        **{'wrap': 'none', 'rtlCol': '0'}
                    ),
                    OpenXML.Drawing.ListStyle(),
                    OpenXML.Drawing.Paragraph(
                        OpenXML.Drawing.Run(
                            OpenXML.Drawing.RunProperties(**{'lang': 'en-US', 'dirty': '0', 'err': '1'}),
                            OpenXML.Drawing.Text('Asd')
                        ),
                        OpenXML.Drawing.EndParagraphRunProperties(**{'lang': 'en-US', 'dirty': '0'})
                    )
                )
            )),
            structure=OpenXML.Presentation.Slide(
                OpenXML.Presentation.CommonSlideData(
                    OpenXML.Presentation.ShapeTree(
                        OpenXML.Presentation.NonVisualGroupShapeProperties(
                            OpenXML.Presentation.NonVisualDrawingProperties(**{'id': '1', 'name': ''}),
                            OpenXML.Presentation.NonVisualGroupShapeDrawingProperties(),
                            OpenXML.Presentation.ApplicationNonVisualDrawingProperties()
                        ),
                        OpenXML.Presentation.GroupShapeProperties(
                            OpenXML.Drawing.Transform2D(
                                OpenXML.Drawing.Offset(**{'x': '0', 'y': '0'}),
                                OpenXML.Drawing.Extents(**{'cx': '0', 'cy': '0'}),
                                OpenXML.Drawing.ChildOffset(**{'x': '0', 'y': '0'}),
                                OpenXML.Drawing.ChildExtents(**{'cx': '0', 'cy': '0'})
                            )
                        )
                    ),
                    OpenXML.Presentation.ExtensionListWithModification(
                        OpenXML.Presentation.Extension(
                            OpenXML.Presentation2010.CreationId(
                                **{'val': '4051434219', 'xmlns:p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main'}
                            ),
                            **{'uri': '{BB962C8B-B14F-4D97-AF65-F5344CB8AC3E}'}
                        )
                    )
                ),
                OpenXML.Presentation.ColorMapOverride(OpenXML.Drawing.MasterColorMapping()),
                **{'xmlns:a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'xmlns:r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships', 'xmlns:p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
            ),
            part_name='ppt/slides/slide3.xml', layout='ppt/slideLayouts/slideLayout2.xml', id=258, relationship_id='rId4',
            relationships=(
                OpenXMLRelationship('rId3', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image', '../media/image4.png', None),
                OpenXMLRelationship('rId2', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image', '../media/image3.svg', None),
                OpenXMLRelationship('rId1', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout', '../slideLayouts/slideLayout2.xml', None),
            ),
        ),
        scaffold=scaffold,
        structure=OpenXML.Presentation.Presentation(
            OpenXML.Presentation.SlideMasterIdList(
                OpenXML.Presentation.SlideMasterId(**{'id': '2147483648', 'r:id': 'rId1'})
            ),
            OpenXML.Presentation.SlideIdList(
                OpenXML.Presentation.SlideId(**{'id': '256', 'r:id': 'rId2'}),
                OpenXML.Presentation.SlideId(**{'id': '257', 'r:id': 'rId3'}),
                OpenXML.Presentation.SlideId(**{'id': '258', 'r:id': 'rId4'})
            ),
            OpenXML.Presentation.SlideSize(**{'cx': '12192000', 'cy': '6858000'}),
            OpenXML.Presentation.NotesSize(**{'cx': '6858000', 'cy': '9144000'}),
            OpenXML.Presentation.DefaultTextStyle(
                OpenXML.Drawing.DefaultParagraphProperties(
                    OpenXML.Drawing.DefaultRunProperties(**{'lang': 'en-US'})
                ),
                OpenXML.Drawing.Level1ParagraphProperties(
                    OpenXML.Drawing.DefaultRunProperties(
                        OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'tx1'})),
                        OpenXML.Drawing.LatinFont(**{'typeface': '+mn-lt'}),
                        OpenXML.Drawing.EastAsianFont(**{'typeface': '+mn-ea'}),
                        OpenXML.Drawing.ComplexScriptFont(**{'typeface': '+mn-cs'}),
                        **{'sz': '1800', 'kern': '1200'}
                    ),
                    **{'marL': '0', 'algn': 'l', 'defTabSz': '914400', 'rtl': '0', 'eaLnBrk': '1', 'latinLnBrk': '0', 'hangingPunct': '1'}
                ),
                OpenXML.Drawing.Level2ParagraphProperties(
                    OpenXML.Drawing.DefaultRunProperties(
                        OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'tx1'})),
                        OpenXML.Drawing.LatinFont(**{'typeface': '+mn-lt'}),
                        OpenXML.Drawing.EastAsianFont(**{'typeface': '+mn-ea'}),
                        OpenXML.Drawing.ComplexScriptFont(**{'typeface': '+mn-cs'}),
                        **{'sz': '1800', 'kern': '1200'}
                    ),
                    **{'marL': '457200', 'algn': 'l', 'defTabSz': '914400', 'rtl': '0', 'eaLnBrk': '1', 'latinLnBrk': '0', 'hangingPunct': '1'}
                ),
                OpenXML.Drawing.Level3ParagraphProperties(
                    OpenXML.Drawing.DefaultRunProperties(
                        OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'tx1'})),
                        OpenXML.Drawing.LatinFont(**{'typeface': '+mn-lt'}),
                        OpenXML.Drawing.EastAsianFont(**{'typeface': '+mn-ea'}),
                        OpenXML.Drawing.ComplexScriptFont(**{'typeface': '+mn-cs'}),
                        **{'sz': '1800', 'kern': '1200'}
                    ),
                    **{'marL': '914400', 'algn': 'l', 'defTabSz': '914400', 'rtl': '0', 'eaLnBrk': '1', 'latinLnBrk': '0', 'hangingPunct': '1'}
                ),
                OpenXML.Drawing.Level4ParagraphProperties(
                    OpenXML.Drawing.DefaultRunProperties(
                        OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'tx1'})),
                        OpenXML.Drawing.LatinFont(**{'typeface': '+mn-lt'}),
                        OpenXML.Drawing.EastAsianFont(**{'typeface': '+mn-ea'}),
                        OpenXML.Drawing.ComplexScriptFont(**{'typeface': '+mn-cs'}),
                        **{'sz': '1800', 'kern': '1200'}
                    ),
                    **{'marL': '1371600', 'algn': 'l', 'defTabSz': '914400', 'rtl': '0', 'eaLnBrk': '1', 'latinLnBrk': '0', 'hangingPunct': '1'}
                ),
                OpenXML.Drawing.Level5ParagraphProperties(
                    OpenXML.Drawing.DefaultRunProperties(
                        OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'tx1'})),
                        OpenXML.Drawing.LatinFont(**{'typeface': '+mn-lt'}),
                        OpenXML.Drawing.EastAsianFont(**{'typeface': '+mn-ea'}),
                        OpenXML.Drawing.ComplexScriptFont(**{'typeface': '+mn-cs'}),
                        **{'sz': '1800', 'kern': '1200'}
                    ),
                    **{'marL': '1828800', 'algn': 'l', 'defTabSz': '914400', 'rtl': '0', 'eaLnBrk': '1', 'latinLnBrk': '0', 'hangingPunct': '1'}
                ),
                OpenXML.Drawing.Level6ParagraphProperties(
                    OpenXML.Drawing.DefaultRunProperties(
                        OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'tx1'})),
                        OpenXML.Drawing.LatinFont(**{'typeface': '+mn-lt'}),
                        OpenXML.Drawing.EastAsianFont(**{'typeface': '+mn-ea'}),
                        OpenXML.Drawing.ComplexScriptFont(**{'typeface': '+mn-cs'}),
                        **{'sz': '1800', 'kern': '1200'}
                    ),
                    **{'marL': '2286000', 'algn': 'l', 'defTabSz': '914400', 'rtl': '0', 'eaLnBrk': '1', 'latinLnBrk': '0', 'hangingPunct': '1'}
                ),
                OpenXML.Drawing.Level7ParagraphProperties(
                    OpenXML.Drawing.DefaultRunProperties(
                        OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'tx1'})),
                        OpenXML.Drawing.LatinFont(**{'typeface': '+mn-lt'}),
                        OpenXML.Drawing.EastAsianFont(**{'typeface': '+mn-ea'}),
                        OpenXML.Drawing.ComplexScriptFont(**{'typeface': '+mn-cs'}),
                        **{'sz': '1800', 'kern': '1200'}
                    ),
                    **{'marL': '2743200', 'algn': 'l', 'defTabSz': '914400', 'rtl': '0', 'eaLnBrk': '1', 'latinLnBrk': '0', 'hangingPunct': '1'}
                ),
                OpenXML.Drawing.Level8ParagraphProperties(
                    OpenXML.Drawing.DefaultRunProperties(
                        OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'tx1'})),
                        OpenXML.Drawing.LatinFont(**{'typeface': '+mn-lt'}),
                        OpenXML.Drawing.EastAsianFont(**{'typeface': '+mn-ea'}),
                        OpenXML.Drawing.ComplexScriptFont(**{'typeface': '+mn-cs'}),
                        **{'sz': '1800', 'kern': '1200'}
                    ),
                    **{'marL': '3200400', 'algn': 'l', 'defTabSz': '914400', 'rtl': '0', 'eaLnBrk': '1', 'latinLnBrk': '0', 'hangingPunct': '1'}
                ),
                OpenXML.Drawing.Level9ParagraphProperties(
                    OpenXML.Drawing.DefaultRunProperties(
                        OpenXML.Drawing.SolidFill(OpenXML.Drawing.SchemeColor(**{'val': 'tx1'})),
                        OpenXML.Drawing.LatinFont(**{'typeface': '+mn-lt'}),
                        OpenXML.Drawing.EastAsianFont(**{'typeface': '+mn-ea'}),
                        OpenXML.Drawing.ComplexScriptFont(**{'typeface': '+mn-cs'}),
                        **{'sz': '1800', 'kern': '1200'}
                    ),
                    **{'marL': '3657600', 'algn': 'l', 'defTabSz': '914400', 'rtl': '0', 'eaLnBrk': '1', 'latinLnBrk': '0', 'hangingPunct': '1'}
                )
            ),
            **{'saveSubsetFonts': '1', 'autoCompressPictures': '0', 'xmlns:a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'xmlns:r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships', 'xmlns:p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
        ),
        size=(12192000, 6858000), units="emu",
        part_name='ppt/presentation.xml', default_layout='ppt/slideLayouts/slideLayout7.xml'
    )

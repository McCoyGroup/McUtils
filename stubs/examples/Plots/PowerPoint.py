"""PowerPoint construction, independent of an installed PowerPoint application."""
from McUtils.Plots import (
    PresentationML, PresentationMLSlide, PresentationMLText,
    PresentationMLImage, PresentationMLShape, PowerPointPresentation
)


def declarative_example(png_file, svg_file):
    return PresentationML(
        PresentationMLSlide(
            PresentationMLText('Scientific results',
                               layout={'position': (36, 24), 'size': (500, 40)},
                               appearance={'font': {'size': 28}}),
            PresentationMLImage(png_file, layout={'position': (36, 90), 'size': (300, 240)}),
            PresentationMLImage(svg_file, layout={'position': (380, 90), 'size': (300, 240)}),
            PresentationMLShape('triangle',
                                layout={'position': (700, 100), 'size': (60, 60)},
                                appearance={'fill': None, 'line': {'color': '4472C4', 'width': 1}})
        ),
        size=(12, 6.75), units='in'
    )


def mutable_example(png_file, svg_file):
    presentation = PowerPointPresentation(size=(12, 6.75), units='in')
    slide = presentation.add_slide()
    slide.draw_text('Scientific results', layout={'position': (0.5, 0.3), 'size': (7, 0.6)},
                    appearance={'font': {'size': 28}})
    slide.draw_image(png_file, layout={'position': (0.5, 1.2), 'size': (4, 3)})
    slide.draw_image(svg_file, layout={'position': (5, 1.2), 'size': (4, 3)})
    # presentation[0] is the same mutable slide; snapshots contain static tuples.
    return presentation


def model_example(glb_file, png_fallback):
    """Camera and playback are wrapper data; the slide scaffold is automatic."""
    presentation = PowerPointPresentation()
    presentation.add_slide().draw_glb(
        glb_file, fallback=png_fallback,
        layout=PresentationML.Layout(position=(40, 80), size=(420, 320),
                                     view=PresentationML.Model3DView(
                                         camera=PresentationML.Camera(position=(0, 0, 3)))),
        animation=PresentationML.Animation(duration=2, loop=True),
    )
    return presentation

# Each returned object supports .write(path), .to_package() and .to_presml().
# PresentationML deliberately has no add_slide method.

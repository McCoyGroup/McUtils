import json
__all__ = ['SceneJSON']

class SceneJSON:
    """
    JSON interchange format to use with Mathematica
    """

    class Primitive:

        def __init__(self, tag, *children, **attrs):
            ...

        def to_json(self):
            ...

        def tostring(self, **opts):
            ...

        def dump(self, file, **opts):
            ...

    class TagElement(Primitive):
        tag = None

        def __init__(self, *children, **attrs):
            ...

    class Graphics3D(TagElement):
        tag = 'graphics3d'

    class Graphics(TagElement):
        tag = 'graphics'

    class Animation(TagElement):
        tag = 'animation'

    class Scene(TagElement):
        tag = 'scene'

    class Circle(TagElement):
        tag = 'circle'

    class Line(TagElement):
        tag = 'line'

    class Rectangle(TagElement):
        tag = 'rectangle'

    class Polygon(TagElement):
        tag = 'polygon'

    class Disk(TagElement):
        tag = 'disk'

    class Cone(TagElement):
        tag = 'cone'

    class Sphere(TagElement):
        tag = 'sphere'

    class Cuboid(TagElement):
        tag = 'cuboid'

    class Cylinder(TagElement):
        tag = 'cylinder'

    class Text(TagElement):
        tag = 'text'
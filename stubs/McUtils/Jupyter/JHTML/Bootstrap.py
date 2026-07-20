from .HTML import HTML, CSS
from .BootstrapEnums import *
__all__ = ['Bootstrap']
__reload_hook__ = ['.HTML']

class BootstrapBase(HTML):

    @classmethod
    def _add_cls(kls, base_cls, cls):
        ...

    @classmethod
    def _manage_cls(kls, obj, cls, variant):
        ...

    class DivComponent(HTML.Div):
        cls = None
        base_style = None

        def __init__(self, *elems, variant=None, cls=None, **attrs):
            ...

    class SpanComponent(HTML.Span):
        cls = None
        base_style = None

        def __init__(self, *elems, variant=None, cls=None, **attrs):
            ...

    class ListComponent(HTML.List):
        cls = None
        base_style = None

        def __init__(self, *elems, variant=None, cls=None, **attrs):
            ...

    class ListItemComponent(HTML.ListItem):
        cls = None
        base_style = None

        def __init__(self, *elems, variant=None, cls=None, **attrs):
            ...

    class ItalicComponent(HTML.Italic):
        cls = None
        base_style = None

        def __init__(self, *elems, variant=None, cls=None, **attrs):
            ...

    class TableComponent(HTML.Table):
        cls = None

        def __init__(self, *elems, variant=None, cls=None, **attrs):
            ...

    class ButtonComponent(HTML.Button):
        cls = None

        def __init__(self, *elems, variant=None, cls=None, **attrs):
            ...

    class AnchorComponent(HTML.Anchor):
        cls = None

        def __init__(self, *elems, variant=None, cls=None, **attrs):
            ...

    class BoostrapIcon(ItalicComponent):
        cls = 'bi'

        def __init__(self, icon_name, cls=None, **attrs):
            ...

    class FontAwesomeIcon(SpanComponent):
        cls = 'fa'

        def __init__(self, icon_name, **attrs):
            ...

    class GlyphIcon(SpanComponent):
        cls = 'glyphicon'

        def __init__(self, icon_name, **attrs):
            ...

    class Col(HTML.Div):
        cls = 'col'
        base_size = None
        base_width = None

        def __init__(self, *elems, width=None, size=None, cls=None, **attrs):
            ...

        def __repr__(self):
            ...

    class Row(DivComponent):
        cls = 'row'

        def __init__(self, *cols, item_attributes=None, **attrs):
            ...

    class Container(DivComponent):
        cls = 'container'

    @staticmethod
    def Grid(rows, row_attributes=None, item_attributes=None, auto_size=False, **attrs):
        ...

    class Alert(DivComponent):
        cls = 'alert'

    class Breadcrumb(ListComponent):
        cls = ['breadcrumb']

    class BreadcrumbItem(ListItemComponent):
        cls = ['breadcrumb-item']

    class ListGroup(ListComponent):
        cls = 'list-group'

    class ListGroupItem(ListItemComponent):
        cls = 'list-group-item'

    class ButtonGroup(DivComponent):
        cls = 'btn-group'

    class Button(ButtonComponent):
        cls = 'btn'
        base_style = 'primary'

    class CloseButton(ButtonComponent):
        cls = 'btn-close'

    class LinkButton(AnchorComponent):
        cls = 'btn'
        base_style = 'default'

    class Table(TableComponent):
        cls = 'table'
        base_style = 'hover'

    class Label(SpanComponent):
        cls = 'label'
        base_style = 'default'

    class Badge(SpanComponent):
        cls = 'badge'
    Class = SemanticClass
    Variant = SemanticVariant

class Bootstrap3(BootstrapBase):
    Icon = BootstrapBase.GlyphIcon

    class Jumbotron(BootstrapBase.DivComponent):
        cls = 'jumbotron'

    class PanelBody(BootstrapBase.DivComponent):
        cls = 'panel-body'

    class PanelHeader(BootstrapBase.DivComponent):
        cls = 'panel-heading'

    class Panel(BootstrapBase.DivComponent):
        cls = 'panel'
        base_style = 'default'

        def __init__(self, *elems, header=None, **attrs):
            ...

class Bootstrap4(BootstrapBase):
    Icon = BootstrapBase.FontAwesomeIcon

    class Jumbotron(BootstrapBase.DivComponent):
        cls = 'jumbotron'

    class Pill(BootstrapBase.SpanComponent):
        cls = ['badge', 'badge-pill']

    class Collapse(BootstrapBase.DivComponent):
        cls = 'collapse'

    class CardBody(BootstrapBase.DivComponent):
        cls = 'card-body'

    class CardHeader(BootstrapBase.DivComponent):
        cls = 'card-header'

    class CardFooter(BootstrapBase.DivComponent):
        cls = 'card-footer'

    class CardImage(BootstrapBase.DivComponent):
        cls = 'card-img-top'

    class Card(BootstrapBase.DivComponent):
        cls = 'card'
        base_style = None

        def __init__(self, *elems, header=None, **attrs):
            ...

class Bootstrap5(BootstrapBase):
    Icon = BootstrapBase.BoostrapIcon

    class Pill(BootstrapBase.SpanComponent):
        cls = ['badge', 'rounded-pill']

    class Accordion(BootstrapBase.DivComponent):
        cls = 'accordion'

    class AccordionItem(BootstrapBase.DivComponent):
        cls = 'accordion-item'

    class AccordionCollapse(BootstrapBase.DivComponent):
        cls = 'accordion-collapse'

    class AccordionBody(BootstrapBase.DivComponent):
        cls = 'accordion-body'

    class Carousel(BootstrapBase.DivComponent):
        cls = 'carousel'

    class CarouselInner(BootstrapBase.DivComponent):
        cls = 'carousel-inner'

    class CarouselItem(BootstrapBase.DivComponent):
        cls = 'carousel-item'

    class Collapse(BootstrapBase.DivComponent):
        cls = 'collapse'

    class CardBody(BootstrapBase.DivComponent):
        cls = 'card-body'

    class CardHeader(BootstrapBase.DivComponent):
        cls = 'card-header'

    class CardFooter(BootstrapBase.DivComponent):
        cls = 'card-footer'

    class CardImage(BootstrapBase.DivComponent):
        cls = 'card-img-top'

    class Card(BootstrapBase.DivComponent):
        cls = 'card'
        base_style = None

        def __init__(self, *elems, header=None, **attrs):
            ...
Bootstrap = Bootstrap5
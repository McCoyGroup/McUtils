from __future__ import annotations
from .HTML import HTML, CSS, SVG, ContentXML, HTMLManager
from .Bootstrap import Bootstrap
from .HTMLWidgets import ActiveHTMLWrapper, HTMLWidgets
from .BootstrapWidgets import BootstrapWidgets
from .WidgetTools import JupyterAPIs, DefaultOutputWidget
import functools
__all__ = ['JHTML']
__reload_hook__ = ['.HTML', '.HTMLWidgets', '.Bootstrap', '.BootstrapWidgets', '.WidgetTools']

class JHTML:
    HTML = HTML
    SVGContext = SVG
    HTMLManager = HTMLManager
    CSS = CSS
    XML = ContentXML
    HTMLWidgets = HTMLWidgets
    APIs = JupyterAPIs
    DefaultOutputWidget = DefaultOutputWidget
    '\n    Provides dispatchers to either pure HTML components or Widget components based on whether interactivity\n    is required or not\n    '
    manage_class = HTMLManager.manage_class
    manage_style = HTMLManager.manage_styles
    extract_styles = HTMLManager.extract_styles
    manage_attrs = HTMLManager.manage_attrs

    @classmethod
    def load(cls, exec_prefix=None, overwrite=False):
        ...

    @classmethod
    def Markdown(cls, text):
        ...

    def __init__(self, context=None, include_bootstrap=False, expose_classes=False, output_pane=True, callbacks=None, widgets=None):
        ...

    def _get_frame_vars(self):
        ...

    def insert_vars(self):
        ...

    def wrap_callbacks(self, c):
        ...
    _callback_stack = []
    _widget_stack = []

    def __enter__(self):
        """
        To make writing HTML interactively a bit nicer

        :return:
        :rtype:
        """
        ...

    @property
    def out(self):
        ...

    def prune_vars(self):
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...
    callbacks = {}

    @classmethod
    def parse_handlers(cls, handler_string):
        ...
    widgets = {}

    @classmethod
    def parse_widget(cls, uuid):
        ...

    @classmethod
    def convert(cls, etree, strip=True, converter=None, **extra_attrs):
        ...

    @classmethod
    def parse(cls, src, event_handlers=None, dynamic=None, track_value=None, strict=True, fallback=None, **attrs):
        ...

    @classmethod
    def _check_widg_static(cls, elems, Widget):
        ...

    @classmethod
    def _check_widg(cls, elems):
        ...

    @classmethod
    def _resolve_source(jhtml, plain, widget, *elems, event_handlers=None, dynamic=None, track_value=None, trackInput=None, _debugPrint=None, javascript_handles=None, oninitialize=None, **attrs):
        ...

    @classmethod
    def _dispatch(jhtml, plain, widget, *elements, event_handlers=None, dynamic=None, **styles):
        ...

    def dispatcher(fn):
        ...

    @classmethod
    @dispatcher
    def Abbr(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Address(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Anchor(jhtml, *elements, **styles):
        ...
    A = Anchor

    @classmethod
    @dispatcher
    def Area(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Article(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Aside(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Audio(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def B(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Base(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Bdi(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Bdo(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Blockquote(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Body(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Bold(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Br(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Button(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Canvas(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Caption(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Cite(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Code(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Col(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Colgroup(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Data(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Datalist(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Dd(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Del(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Details(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Dfn(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Dialog(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Div(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Dl(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Dt(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Em(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Embed(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Fieldset(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Figcaption(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Figure(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Footer(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Form(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Head(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Header(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Heading(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Hr(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Html(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Iframe(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Image(jhtml, *elements, **styles):
        ...

    @classmethod
    def image_from_string(cls, image_string: bytes | str, format='image/png', **styles):
        ...

    @classmethod
    @dispatcher
    def Img(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Input(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Ins(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Italic(jhtml, *elements, **styles):
        ...
    I = Italic

    @classmethod
    @dispatcher
    def Kbd(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Label(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Legend(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Link(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def List(jhtml, *elements, **styles):
        ...
    Ul = List

    @classmethod
    @dispatcher
    def ListItem(jhtml, *elements, **styles):
        ...
    Li = ListItem

    @classmethod
    @dispatcher
    def Main(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Map(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Mark(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Meta(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Meter(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Nav(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Noscript(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def NumberedList(jhtml, *elements, **styles):
        ...
    Ol = NumberedList

    @classmethod
    @dispatcher
    def Object(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Optgroup(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Option(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Output(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Param(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Picture(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Pre(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Progress(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Q(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Rp(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Rt(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Ruby(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def S(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Samp(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Script(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Section(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Select(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Small(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Source(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Span(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Strong(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Style(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Sub(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def SubHeading(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def SubsubHeading(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def SubsubsubHeading(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def SubHeading5(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def SubHeading6(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Summary(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Sup(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Svg(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Table(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def TableBody(jhtml, *elements, **styles):
        ...
    Tbody = TableBody

    @classmethod
    @dispatcher
    def TableFooter(jhtml, *elements, **styles):
        ...
    Tfoot = TableFooter

    @classmethod
    @dispatcher
    def TableHeader(jhtml, *elements, **styles):
        ...
    Thead = TableHeader

    @classmethod
    @dispatcher
    def TableHeading(jhtml, *elements, **styles):
        ...
    Th = TableHeading

    @classmethod
    @dispatcher
    def TableItem(jhtml, *elements, **styles):
        ...
    Td = TableItem

    @classmethod
    @dispatcher
    def TableRow(jhtml, *elements, **styles):
        ...
    Tr = TableRow

    @classmethod
    @dispatcher
    def Template(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Text(jhtml, *elements, **styles):
        ...
    P = Text

    @classmethod
    @dispatcher
    def Textarea(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Time(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Title(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Track(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def U(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Var(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Video(jhtml, *elements, **styles):
        ...

    @classmethod
    @dispatcher
    def Wbr(jhtml, *elements, **styles):
        ...
    OutputArea = HTMLWidgets.OutputArea
    JavascriptAPI = HTMLWidgets.JavascriptAPI

    class Bootstrap:
        Class = Bootstrap.Class
        Variant = Bootstrap.Variant

        @classmethod
        def _dispatch(jhtml, *elems, **attrs):
            ...

        def dispatcher(fn):
            ...

        @classmethod
        @dispatcher
        def Icon(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def Alert(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def Badge(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def PanelBody(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def PanelHeader(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def Panel(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def CardBody(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def CardHeader(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def CardFooter(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def CardImage(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def Card(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def Jumbotron(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def Col(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def Row(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def Container(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def Button(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def ButtonGroup(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def LinkButton(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def Table(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def ListGroup(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def ListGroupItem(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def FontAwesomeIcon(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def GlyphIcon(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def Label(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def Pill(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def ListComponent(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def ListItemComponent(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def Breadcrumb(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def BreadcrumbItem(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def Accordion(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def AccordionItem(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def AccordionCollapse(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def AccordionBody(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def Carousel(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def CarouselInner(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def CarouselItem(boots, *elements, **styles):
            ...

        @classmethod
        @dispatcher
        def Collapse(boots, *elements, **styles):
            ...

    class Styled:

        def __init__(self, base, **attrs):
            ...

        def __call__(self, *args, **kwargs):
            ...

        def __repr__(self):
            ...

    class Compound:

        def __init__(self, *wrappers):
            ...

        @staticmethod
        def destructure_wrapper(wrapper):
            ...

        class CompoundWrapperData:
            __slots__ = ['list', 'dict']

            def __init__(self, list, dict):
                ...

            def __getitem__(self, item):
                ...

        def __call__(self, *args, wrapper_attrs=None, **kwargs):
            ...

        def __repr__(self):
            ...
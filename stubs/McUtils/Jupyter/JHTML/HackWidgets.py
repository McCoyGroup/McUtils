class JHTMLShadowDOMElement:
    """
    Provides a shadow DOM tree that can makes it easier to update
    chunks of a tree constructed from JupyterHTMLWrappers
    """

    def __init__(self, widg, wrapper=None, parent=None):
        ...

    def link(self, dom_el, recursive=False):
        ...

    @property
    def tree(self):
        ...

    def to_tree(self, refresh=False):
        ...

    def _invalidate_cache(self):
        ...

    class Refresher:

        def __init__(self, dom_el, which=None):
            ...

        def __call__(self, el, key, value):
            ...

    def refresh(self, el, key, value):
        ...

    def refresh_child(self, el, key, value, which):
        ...

    def get_parent(self, n):
        ...

    def find(self, path, find_element=True):
        ...

    def findall(self, path, find_element=True):
        ...

    def iterfind(self, path, find_element=True):
        ...

    def find_by_id(self, id, mode='first', parent=None, find_element=True):
        ...

    def __getitem__(self, item):
        ...

class JupyterHTMLWrapper:
    """
    Provides simple access to Jupyter display utilities
    """
    reset_attrs = ['background', 'color', 'font', 'font-family']

    @classmethod
    def load_styles(cls):
        """
        Embeds widget restyle definitions into the active notebook

        :return:
        :rtype:
        """
        ...
    stripped_classes = ['lm-Widget', 'p-Widget', 'lm-Panel', 'p-Panel', 'jupyter-widgets', 'widget-container', 'widget-box', 'widget-html']
    protecting_classes = ['widget-slider']
    stripped_unprotected = ['widget-inline-hbox']

    @classmethod
    def get_class_stripper_js(cls):
        ...

    @classmethod
    def get_class_stripper(cls):
        ...
    cls = None
    tag = None
    layout = None
    container = False

    def __init__(self, *elements, tag=None, event_handlers=None, layout=None, extra_classes=None, cls=None, debug_pane=None, **styles):
        ...

    @staticmethod
    def _handle_event(e, event_handlers, self, widg):
        ...

    def _event_handler(self, widg):
        ...
    inherited_classes = ['d-inline', 'd-flex', 'd-inline-block', 'd-block', 'd-none']
    inherited_class_tag_map = {'span': ['d-inline-block'], None: ['d-inline-block']}
    inherited_class_cls_map = {'btn': ['d-inline-block']}

    def _convert(self, x, parent=None):
        ...

    @classmethod
    def manage_styles(cls, styles, validate=True):
        ...

    def _invalidate_cache(self):
        ...

    def to_widget(self, parent=None):
        ...

    @classmethod
    def display_widget(cls, w):
        ...

    def display(self):
        ...

    def _ipython_display_(self):
        ...

    def find(self, path, find_element=True):
        ...

    def findall(self, path, find_element=True):
        ...

    def iterfind(self, path, find_element=True):
        ...

    def find_by_id(self, id, mode='first', parent=None, find_element=True):
        ...
    _widget_sources = []
    _base_map = None

    @classmethod
    def load_base_map(cls):
        ...

    @property
    def base_map(self):
        ...

class JupyterHTMLWidgets:
    """
    Provides convenience constructors for HTML components
    """

    @classmethod
    def load(cls):
        ...

    class WrappedElement(JupyterHTMLWrapper):
        base = None
        container = False

        def __init__(self, *elems, base=None, event_handlers=None, container=None, layout=None, extra_classes=None, **attrs):
            ...

        def copy(self):
            ...

        def add_child_class(self, *cls, copy=True):
            ...

        def add_class(self, *cls, copy=True):
            ...

        def remove_class(self, *cls, copy=True):
            ...

        def add_styles(self, copy=True, **sty):
            ...

    class ContainerWrapper(WrappedElement):
        container = True

    class Abbr(WrappedElement):
        base = HTML.Abbr

    class Address(WrappedElement):
        base = HTML.Address

    class Anchor(WrappedElement):
        base = HTML.Anchor
    A = Anchor

    class Area(WrappedElement):
        base = HTML.Area

    class Article(WrappedElement):
        base = HTML.Article

    class Aside(WrappedElement):
        base = HTML.Aside

    class Audio(WrappedElement):
        base = HTML.Audio

    class B(WrappedElement):
        base = HTML.B

    class Base(WrappedElement):
        base = HTML.Base

    class BaseList(WrappedElement):
        base = HTML.BaseList

    class Bdi(WrappedElement):
        base = HTML.Bdi

    class Bdo(WrappedElement):
        base = HTML.Bdo

    class Blockquote(WrappedElement):
        base = HTML.Blockquote

    class Body(WrappedElement):
        base = HTML.Body

    class Bold(WrappedElement):
        base = HTML.Bold

    class Br(WrappedElement):
        base = HTML.Br

    class Button(WrappedElement):
        base = HTML.Button

    class Canvas(WrappedElement):
        base = HTML.Canvas

    class Caption(WrappedElement):
        base = HTML.Caption

    class Cite(WrappedElement):
        base = HTML.Cite

    class ClassAdder(WrappedElement):
        base = HTML.ClassAdder

    class ClassRemover(WrappedElement):
        base = HTML.ClassRemover

    class Code(WrappedElement):
        base = HTML.Code

    class Col(WrappedElement):
        base = HTML.Col

    class Colgroup(WrappedElement):
        base = HTML.Colgroup

    class Data(WrappedElement):
        base = HTML.Data

    class Datalist(WrappedElement):
        base = HTML.Datalist

    class Dd(WrappedElement):
        base = HTML.Dd

    class Del(WrappedElement):
        base = HTML.Del

    class Details(WrappedElement):
        base = HTML.Details

    class Dfn(WrappedElement):
        base = HTML.Dfn

    class Dialog(WrappedElement):
        base = HTML.Dialog

    class Div(WrappedElement):
        base = HTML.Div

    class Dl(WrappedElement):
        base = HTML.Dl

    class Dt(WrappedElement):
        base = HTML.Dt

    class ElementModifier(WrappedElement):
        base = HTML.ElementModifier

    class Em(WrappedElement):
        base = HTML.Em

    class Embed(WrappedElement):
        base = HTML.Embed

    class Fieldset(WrappedElement):
        base = HTML.Fieldset

    class Figcaption(WrappedElement):
        base = HTML.Figcaption

    class Figure(WrappedElement):
        base = HTML.Figure

    class Footer(WrappedElement):
        base = HTML.Footer

    class Form(WrappedElement):
        base = HTML.Form

    class Head(WrappedElement):
        base = HTML.Head

    class Header(WrappedElement):
        base = HTML.Header

    class Heading(WrappedElement):
        base = HTML.Heading

    class Hr(WrappedElement):
        base = HTML.Hr

    class Iframe(WrappedElement):
        base = HTML.Iframe

    class Image(WrappedElement):
        base = HTML.Image

    class Img(WrappedElement):
        base = HTML.Img

    class Input(WrappedElement):
        base = HTML.Input

    class Ins(WrappedElement):
        base = HTML.Ins

    class Italic(WrappedElement):
        base = HTML.Italic

    class Kbd(WrappedElement):
        base = HTML.Kbd

    class Label(WrappedElement):
        base = HTML.Label

    class Legend(WrappedElement):
        base = HTML.Legend

    class Li(WrappedElement):
        base = HTML.Li

    class Link(WrappedElement):
        base = HTML.Link

    class List(WrappedElement):
        base = HTML.List

    class ListItem(WrappedElement):
        base = HTML.ListItem

    class Main(WrappedElement):
        base = HTML.Main

    class Map(WrappedElement):
        base = HTML.Map

    class Mark(WrappedElement):
        base = HTML.Mark

    class Meta(WrappedElement):
        base = HTML.Meta

    class Meter(WrappedElement):
        base = HTML.Meter

    class Nav(WrappedElement):
        base = HTML.Nav

    class Noscript(WrappedElement):
        base = HTML.Noscript

    class NumberedList(WrappedElement):
        base = HTML.NumberedList

    class Object(WrappedElement):
        base = HTML.Object

    class Ol(WrappedElement):
        base = HTML.Ol

    class Optgroup(WrappedElement):
        base = HTML.Optgroup

    class Option(WrappedElement):
        base = HTML.Option

    class Output(WrappedElement):
        base = HTML.Output

    class P(WrappedElement):
        base = HTML.P

    class Param(WrappedElement):
        base = HTML.Param

    class Picture(WrappedElement):
        base = HTML.Picture

    class Pre(WrappedElement):
        base = HTML.Pre

    class Progress(WrappedElement):
        base = HTML.Progress

    class Q(WrappedElement):
        base = HTML.Q

    class Rp(WrappedElement):
        base = HTML.Rp

    class Rt(WrappedElement):
        base = HTML.Rt

    class Ruby(WrappedElement):
        base = HTML.Ruby

    class S(WrappedElement):
        base = HTML.S

    class Samp(WrappedElement):
        base = HTML.Samp

    class Script(WrappedElement):
        base = HTML.Script

    class Section(WrappedElement):
        base = HTML.Section

    class Select(WrappedElement):
        base = HTML.Select

    class Small(WrappedElement):
        base = HTML.Small

    class Source(WrappedElement):
        base = HTML.Source

    class Span(WrappedElement):
        base = HTML.Span

    class Strong(WrappedElement):
        base = HTML.Strong

    class Style(WrappedElement):
        base = HTML.Style

    class StyleAdder(WrappedElement):
        base = HTML.StyleAdder

    class Sub(WrappedElement):
        base = HTML.Sub

    class SubHeading(WrappedElement):
        base = HTML.SubHeading

    class SubsubHeading(WrappedElement):
        base = HTML.SubsubHeading

    class SubsubsubHeading(WrappedElement):
        base = HTML.SubsubsubHeading

    class SubHeading5(WrappedElement):
        base = HTML.SubHeading5

    class SubHeading6(WrappedElement):
        base = HTML.SubHeading6

    class Summary(WrappedElement):
        base = HTML.Summary

    class Sup(WrappedElement):
        base = HTML.Sup

    class Svg(WrappedElement):
        base = HTML.Svg

    class Table(WrappedElement):
        base = HTML.Table

    class TableBody(WrappedElement):
        base = HTML.TableBody

    class TableHeading(WrappedElement):
        base = HTML.TableHeading

    class TableItem(WrappedElement):
        base = HTML.TableItem

    class TableRow(WrappedElement):
        base = HTML.TableRow

    class TagElement(WrappedElement):
        base = HTML.TagElement

    class Tbody(WrappedElement):
        base = HTML.Tbody

    class Td(WrappedElement):
        base = HTML.Td

    class Template(WrappedElement):
        base = HTML.Template

    class Text(WrappedElement):
        base = HTML.Text

    class Textarea(WrappedElement):
        base = HTML.Textarea

    class Tfoot(WrappedElement):
        base = HTML.Tfoot

    class Th(WrappedElement):
        base = HTML.Th

    class Thead(WrappedElement):
        base = HTML.Thead

    class Time(WrappedElement):
        base = HTML.Time

    class Title(WrappedElement):
        base = HTML.Title

    class Tr(WrappedElement):
        base = HTML.Tr

    class Track(WrappedElement):
        base = HTML.Track

    class U(WrappedElement):
        base = HTML.U

    class Ul(WrappedElement):
        base = HTML.Ul

    class Var(WrappedElement):
        base = HTML.Var

    class Video(WrappedElement):
        base = HTML.Video

    class Wbr(WrappedElement):
        base = HTML.Wbr

    class OutputArea(JupyterHTMLWrapper):

        def __init__(self, *elements, autoclear=False, event_handlers=None, layout=None, extra_classes=None, cls=None, **styles):
            ...

        def print(self, *args, **kwargs):
            ...

        def display(self, *args):
            ...

        def clear(self):
            ...

        def __enter__(self):
            ...

        def __exit__(self, exc_type, exc_val, exc_tb):
            ...
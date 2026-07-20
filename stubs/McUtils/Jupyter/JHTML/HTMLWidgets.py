import os.path, pathlib
import sys
import weakref, io, asyncio, threading, time
from .HTML import CSS, HTML, HTMLManager
from .WidgetTools import JupyterAPIs, DefaultOutputWidget
__all__ = ['HTMLWidgets', 'ActiveHTMLWrapper']
__reload_hook__ = ['.HTML', '.WidgetTools']

class ActiveHTMLWrapper:
    base = None
    _subwrappers = weakref.WeakKeyDictionary()

    def __init__(self, *elements, tag=None, cls=None, id=None, value=None, style=None, event_handlers=None, inner_html=None, javascript_handles=None, onevents=None, data=None, unsynced_properties=None, debug_pane=None, track_value=None, continuous_update=None, **attributes):
        ...

    def __call__(self, *elems, **kwargs):
        ...

    @classmethod
    def canonicalize_widget(cls, x):
        ...

    @classmethod
    def clean_props(cls, props, to_str=False):
        ...

    @classmethod
    def _prep_val(cls, y, to_str=False):
        ...

    @classmethod
    def from_HTML(cls, x: HTML.XMLElement, event_handlers=None, debug_pane=None, **props):
        ...

    @classmethod
    def load_HTMLElement(cls):
        ...

    @classmethod
    def convert_child(cls, c):
        ...

    def to_html(self):
        ...

    def find(self, path, find_mirror=True):
        ...

    def findall(self, path, find_mirror=True):
        ...

    def iterfind(self, path, find_mirror=True):
        ...

    def find_by_id(self, id, mode='first', parent=None, find_mirror=True):
        ...

    def to_widget(self, parent=None):
        ...

    def __repr__(self):
        ...

    def display(self):
        ...

    def _ipython_display_(self):
        ...

    def get_mime_bundle(self):
        ...

    @staticmethod
    def _handle_event(e, event_handlers, self):
        ...

    def handle_event(self, e):
        ...

    def link(self, elem):
        ...

    @property
    def tag(self):
        ...

    @property
    def id(self):
        ...

    @id.setter
    def id(self, val):
        ...

    @property
    def text(self):
        ...

    @text.setter
    def text(self, val):
        ...

    @property
    def value(self):
        ...

    @value.setter
    def value(self, val):
        ...

    @property
    def attrs(self):
        ...

    @attrs.setter
    def attrs(self, val):
        ...

    def __getitem__(self, item):
        ...

    def __setitem__(self, item, value):
        ...

    def __delitem__(self, item):
        ...

    def get_attribute(self, key):
        ...

    def set_attribute(self, key, value):
        ...

    def del_attribute(self, key):
        ...

    def get_child(self, position, wrapper=False):
        ...

    def set_child(self, position, value):
        ...

    def insert(self, where, child):
        ...

    def append(self, child):
        ...

    def del_child(self, position):
        ...

    def activate_body(self):
        ...

    @property
    def elements(self):
        ...

    @property
    def children(self):
        ...

    @children.setter
    def children(self, kids):
        ...

    @property
    def html_string(self):
        ...

    @html_string.setter
    def html_string(self, val):
        ...

    @property
    def html(self):
        ...

    @html.setter
    def html(self, html):
        ...

    def _track_html_change(self, *_):
        ...

    def load_HTML(self):
        ...

    @property
    def javascript_handles(self):
        ...

    @javascript_handles.setter
    def javascript_handles(self, js):
        ...

    @property
    def class_list(self):
        ...

    @class_list.setter
    def class_list(self, cls):
        ...

    def add_class(self, *cls):
        ...

    def remove_class(self, *cls):
        ...

    @property
    def style(self):
        ...

    @style.setter
    def style(self, style):
        ...

    def add_styles(self, **sty):
        ...

    def remove_styles(self, *sty):
        ...

    @property
    def data(self):
        ...

    @data.setter
    def data(self, d: dict):
        ...

    @property
    def event_handlers(self):
        ...

    @event_handlers.setter
    def event_handlers(self, event_handlers):
        ...

    def update_events(self, events):
        ...

    def add_event(self, send=True, **events):
        ...

    def remove_event(self, *events, send=True):
        ...
    _message_waiting_semaphores = {}

    @staticmethod
    def _on_msg(msg, callback, current_event):
        ...

    async def _wait_for_message(self, msg, poll_interval=0.05):
        ...

    async def wait_for_message(self, msg, callback, suppress_others=False, timeout=1, poll_interval=0.05):
        ...

    def call(self, method, buffers=None, return_message=None, callback=None, timeout=1, poll_interval=0.05, suppress_others=False, **content):
        ...

    def _setup_thread_listener(self, msg, callback, suppress_others=False):
        ...

    def _wait_for_thread_message(self, msg, poll_interval=0.05):
        ...

    def _wait_for_result(self, msg, og_listener, timeout=1, poll_interval=0.05):
        ...

    def _thread_call(self, method, buffers=None, return_message=None, callback=None, timeout=1, poll_interval=0.05, suppress_others=False, **content):
        ...

    def add_javascript(self, **methods):
        ...

    def remove_javascript(self, *methods):
        ...

    def trigger(self, method, buffers=None, **content):
        ...

    @property
    def onevents(self):
        ...

    @onevents.setter
    def onevents(self, onevents):
        ...

    def update_onevents(self, events):
        ...

    def on(self, send=True, **events):
        ...

    def off(self, *events, send=True):
        ...

    @property
    def track_value(self):
        ...

    @track_value.setter
    def track_value(self, v):
        ...

    @property
    def continuous_update(self):
        ...

    @continuous_update.setter
    def continuous_update(self, v):
        ...

    class LazyLoader:

        def __init__(self, base_cls, args, kwargs):
            ...

        def load(self):
            ...

    @classmethod
    def loader(cls, *args, **kwargs):
        ...

class HTMLWidgets:

    @classmethod
    def get_exec_prefix(cls):
        ...

    @classmethod
    def load(cls, exec_prefix=None, overwrite=False):
        ...
    _cls_map = None

    @classmethod
    def get_class_map(cls):
        ...

    @classmethod
    def from_HTML(cls, html: HTML.XMLElement, event_handlers=None, debug_pane=None, **props):
        ...

    class JavascriptAPI(ActiveHTMLWrapper):

        def __init__(self, safety_wrap=True, _debugPrint=False, disable_caching=True, **javascript_handles):
            ...

        def safety_wrap(self, v):
            ...

    class WrappedHTMLElement(ActiveHTMLWrapper):

        def __repr__(self):
            ...

    class Abbr(WrappedHTMLElement):
        base = HTML.Abbr

    class Address(WrappedHTMLElement):
        base = HTML.Address

    class Anchor(WrappedHTMLElement):
        base = HTML.Anchor
    A = Anchor

    class Area(WrappedHTMLElement):
        base = HTML.Area

    class Article(WrappedHTMLElement):
        base = HTML.Article

    class Aside(WrappedHTMLElement):
        base = HTML.Aside

    class Audio(WrappedHTMLElement):
        base = HTML.Audio

    class B(WrappedHTMLElement):
        base = HTML.B

    class Base(WrappedHTMLElement):
        base = HTML.Base

    class BaseList(WrappedHTMLElement):
        base = HTML.BaseList

    class Bdi(WrappedHTMLElement):
        base = HTML.Bdi

    class Bdo(WrappedHTMLElement):
        base = HTML.Bdo

    class Blockquote(WrappedHTMLElement):
        base = HTML.Blockquote

    class Body(WrappedHTMLElement):
        base = HTML.Body

    class Bold(WrappedHTMLElement):
        base = HTML.Bold

    class Br(WrappedHTMLElement):
        base = HTML.Br

    class Button(WrappedHTMLElement):
        base = HTML.Button

    class Canvas(WrappedHTMLElement):
        base = HTML.Canvas

    class Caption(WrappedHTMLElement):
        base = HTML.Caption

    class Cite(WrappedHTMLElement):
        base = HTML.Cite

    class Code(WrappedHTMLElement):
        base = HTML.Code

    class Col(WrappedHTMLElement):
        base = HTML.Col

    class Colgroup(WrappedHTMLElement):
        base = HTML.Colgroup

    class Data(WrappedHTMLElement):
        base = HTML.Data

    class Datalist(WrappedHTMLElement):
        base = HTML.Datalist

    class Dd(WrappedHTMLElement):
        base = HTML.Dd

    class Del(WrappedHTMLElement):
        base = HTML.Del

    class Details(WrappedHTMLElement):
        base = HTML.Details

    class Dfn(WrappedHTMLElement):
        base = HTML.Dfn

    class Dialog(WrappedHTMLElement):
        base = HTML.Dialog

    class Div(WrappedHTMLElement):
        base = HTML.Div

    class Dl(WrappedHTMLElement):
        base = HTML.Dl

    class Dt(WrappedHTMLElement):
        base = HTML.Dt

    class Em(WrappedHTMLElement):
        base = HTML.Em

    class Embed(WrappedHTMLElement):
        base = HTML.Embed

    class Fieldset(WrappedHTMLElement):
        base = HTML.Fieldset

    class Figcaption(WrappedHTMLElement):
        base = HTML.Figcaption

    class Figure(WrappedHTMLElement):
        base = HTML.Figure

    class Footer(WrappedHTMLElement):
        base = HTML.Footer

    class Form(WrappedHTMLElement):
        base = HTML.Form

    class Head(WrappedHTMLElement):
        base = HTML.Head

    class Header(WrappedHTMLElement):
        base = HTML.Header

    class Heading(WrappedHTMLElement):
        base = HTML.Heading

    class Hr(WrappedHTMLElement):
        base = HTML.Hr

    class Html(WrappedHTMLElement):
        base = HTML.Html

    class Iframe(WrappedHTMLElement):
        base = HTML.Iframe

    class Image(WrappedHTMLElement):
        base = HTML.Image

    class Img(WrappedHTMLElement):
        base = HTML.Img

    class Input(WrappedHTMLElement):
        base = HTML.Input

    class Ins(WrappedHTMLElement):
        base = HTML.Ins

    class Italic(WrappedHTMLElement):
        base = HTML.Italic

    class Kbd(WrappedHTMLElement):
        base = HTML.Kbd

    class Label(WrappedHTMLElement):
        base = HTML.Label

    class Legend(WrappedHTMLElement):
        base = HTML.Legend

    class Li(WrappedHTMLElement):
        base = HTML.Li

    class Link(WrappedHTMLElement):
        base = HTML.Link

    class List(WrappedHTMLElement):
        base = HTML.List

    class ListItem(WrappedHTMLElement):
        base = HTML.ListItem

    class Main(WrappedHTMLElement):
        base = HTML.Main

    class Map(WrappedHTMLElement):
        base = HTML.Map

    class Mark(WrappedHTMLElement):
        base = HTML.Mark

    class Meta(WrappedHTMLElement):
        base = HTML.Meta

    class Meter(WrappedHTMLElement):
        base = HTML.Meter

    class Nav(WrappedHTMLElement):
        base = HTML.Nav

    class Noscript(WrappedHTMLElement):
        base = HTML.Noscript

    class NumberedList(WrappedHTMLElement):
        base = HTML.NumberedList

    class Object(WrappedHTMLElement):
        base = HTML.Object

    class Ol(WrappedHTMLElement):
        base = HTML.Ol

    class Optgroup(WrappedHTMLElement):
        base = HTML.Optgroup

    class Option(WrappedHTMLElement):
        base = HTML.Option

    class Output(WrappedHTMLElement):
        base = HTML.Output

    class P(WrappedHTMLElement):
        base = HTML.P

    class Param(WrappedHTMLElement):
        base = HTML.Param

    class Picture(WrappedHTMLElement):
        base = HTML.Picture

    class Pre(WrappedHTMLElement):
        base = HTML.Pre

    class Progress(WrappedHTMLElement):
        base = HTML.Progress

    class Q(WrappedHTMLElement):
        base = HTML.Q

    class Rp(WrappedHTMLElement):
        base = HTML.Rp

    class Rt(WrappedHTMLElement):
        base = HTML.Rt

    class Ruby(WrappedHTMLElement):
        base = HTML.Ruby

    class S(WrappedHTMLElement):
        base = HTML.S

    class Samp(WrappedHTMLElement):
        base = HTML.Samp

    class Script(WrappedHTMLElement):
        base = HTML.Script

    class Section(WrappedHTMLElement):
        base = HTML.Section

    class Select(WrappedHTMLElement):
        base = HTML.Select

    class Small(WrappedHTMLElement):
        base = HTML.Small

    class Source(WrappedHTMLElement):
        base = HTML.Source

    class Span(WrappedHTMLElement):
        base = HTML.Span

    class Strong(WrappedHTMLElement):
        base = HTML.Strong

    class Style(WrappedHTMLElement):
        base = HTML.Style

    class Sub(WrappedHTMLElement):
        base = HTML.Sub

    class SubHeading(WrappedHTMLElement):
        base = HTML.SubHeading

    class SubsubHeading(WrappedHTMLElement):
        base = HTML.SubsubHeading

    class SubsubsubHeading(WrappedHTMLElement):
        base = HTML.SubsubsubHeading

    class SubHeading5(WrappedHTMLElement):
        base = HTML.SubHeading5

    class SubHeading6(WrappedHTMLElement):
        base = HTML.SubHeading6

    class Summary(WrappedHTMLElement):
        base = HTML.Summary

    class Sup(WrappedHTMLElement):
        base = HTML.Sup

    class Svg(WrappedHTMLElement):
        base = HTML.Svg

    class Table(WrappedHTMLElement):
        base = HTML.Table

    class TableHeader(WrappedHTMLElement):
        base = HTML.TableHeader

    class TableBody(WrappedHTMLElement):
        base = HTML.TableBody

    class TableHeading(WrappedHTMLElement):
        base = HTML.TableHeading

    class TableItem(WrappedHTMLElement):
        base = HTML.TableItem

    class TableRow(WrappedHTMLElement):
        base = HTML.TableRow

    class TagElement(WrappedHTMLElement):
        base = HTML.TagElement

    class Tbody(WrappedHTMLElement):
        base = HTML.Tbody

    class Td(WrappedHTMLElement):
        base = HTML.Td

    class Template(WrappedHTMLElement):
        base = HTML.Template

    class Text(WrappedHTMLElement):
        base = HTML.Text

    class Textarea(WrappedHTMLElement):
        base = HTML.Textarea

    class Tfoot(WrappedHTMLElement):
        base = HTML.Tfoot

    class Th(WrappedHTMLElement):
        base = HTML.Th

    class Thead(WrappedHTMLElement):
        base = HTML.Thead

    class Time(WrappedHTMLElement):
        base = HTML.Time

    class Title(WrappedHTMLElement):
        base = HTML.Title

    class Tr(WrappedHTMLElement):
        base = HTML.Tr

    class Track(WrappedHTMLElement):
        base = HTML.Track

    class U(WrappedHTMLElement):
        base = HTML.U

    class Ul(WrappedHTMLElement):
        base = HTML.Ul

    class Var(WrappedHTMLElement):
        base = HTML.Var

    class Video(WrappedHTMLElement):
        base = HTML.Video

    class Wbr(WrappedHTMLElement):
        base = HTML.Wbr

    class OutputArea(ActiveHTMLWrapper):

        def __init__(self, *elements, max_messages=None, autoclear=False, event_handlers=None, cls=None, **styles):
            ...

        def print(self, *args, **kwargs):
            ...

        def show_output(self, *args, **kwargs):
            ...

        def _get_display_data(self, args, mimetype=None):
            ...

        def append_stdout(self, arg):
            ...

        def append_stderr(self, arg):
            ...

        def show_buffered(self, *args):
            ...

        def set_output(self, *args):
            ...

        def show_raw(self, *args):
            ...

        def clear(self, wait=False):
            ...

        def __enter__(self):
            ...

        def __exit__(self, exc_type, exc_val, exc_tb):
            ...
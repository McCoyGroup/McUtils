from .HTML import HTML
from .HTMLWidgets import ActiveHTMLWrapper, HTMLWidgets
from .Bootstrap import Bootstrap3, Bootstrap4, Bootstrap5
__all__ = ['BootstrapWidgets']
__reload_hook__ = ['.HTML', '.HTMLWidgets', '.Bootstrap']

class BootstrapWidgetsBase:
    cdn_loader = None
    cdn_css = []
    cdn_js = []
    _cdn_cache = {}
    bootstrap_version = None

    @classmethod
    def load(cls):
        """
        Embeds Bootstrap style definitions into the active notebook

        :return:
        :rtype:
        """
        ...

    @classmethod
    def _monkey_patch(cls):
        ...

    @classmethod
    def Grid(cls, rows, row_attributes=None, item_attributes=None, auto_size=True, **attrs):
        ...

class Bootstrap3Widgets(BootstrapWidgetsBase):
    bootstrap_version = Bootstrap3

    class Icon(ActiveHTMLWrapper):
        base = Bootstrap3.Icon

    class Alert(ActiveHTMLWrapper):
        base = Bootstrap3.Alert

    class Badge(ActiveHTMLWrapper):
        base = Bootstrap3.Badge

    class PanelBody(ActiveHTMLWrapper):
        base = Bootstrap3.PanelBody

    class PanelHeader(ActiveHTMLWrapper):
        base = Bootstrap3.PanelHeader

    class Panel(ActiveHTMLWrapper):
        base = Bootstrap3.Panel

    class Jumbotron(ActiveHTMLWrapper):
        base = Bootstrap3.Jumbotron

    class Col(ActiveHTMLWrapper):
        base = Bootstrap3.Col

    class Row(ActiveHTMLWrapper):
        base = Bootstrap3.Row

    class Container(ActiveHTMLWrapper):
        base = Bootstrap3.Container

    class Button(ActiveHTMLWrapper):
        base = Bootstrap3.Button

    class LinkButton(HTML.Anchor):
        base = Bootstrap3.LinkButton

    class Table(ActiveHTMLWrapper):
        base = Bootstrap3.Table

    class ListGroup(ActiveHTMLWrapper):
        base = Bootstrap3.ListGroup

    class ListGroupItem(ActiveHTMLWrapper):
        base = Bootstrap3.ListGroupItem

    class FontAwesomeIcon(ActiveHTMLWrapper):
        base = Bootstrap3.FontAwesomeIcon

    class GlyphIcon(ActiveHTMLWrapper):
        base = Bootstrap3.GlyphIcon

    class Label(ActiveHTMLWrapper):
        base = Bootstrap3.Label

    class ListComponent(ActiveHTMLWrapper):
        base = Bootstrap3.ListComponent

    class ListItemComponent(ActiveHTMLWrapper):
        base = Bootstrap3.ListItemComponent

    class Breadcrumb(ActiveHTMLWrapper):
        base = Bootstrap3.Breadcrumb

    class BreadcrumbItem(ActiveHTMLWrapper):
        base = Bootstrap3.BreadcrumbItem

class Bootstrap4Widgets(BootstrapWidgetsBase):
    bootstrap_version = Bootstrap4

    class Icon(ActiveHTMLWrapper):
        base = Bootstrap4.Icon

    class Alert(ActiveHTMLWrapper):
        base = Bootstrap4.Alert

    class Badge(ActiveHTMLWrapper):
        base = Bootstrap4.Badge

    class CardBody(ActiveHTMLWrapper):
        base = Bootstrap4.CardBody

    class CardHeader(ActiveHTMLWrapper):
        base = Bootstrap4.CardHeader

    class CardFooter(ActiveHTMLWrapper):
        base = Bootstrap4.CardFooter

    class CardImage(ActiveHTMLWrapper):
        base = Bootstrap4.CardImage

    class Card(ActiveHTMLWrapper):
        base = Bootstrap4.Card

    class Jumbotron(ActiveHTMLWrapper):
        base = Bootstrap4.Jumbotron

    class Col(ActiveHTMLWrapper):
        base = Bootstrap4.Col

    class Row(ActiveHTMLWrapper):
        base = Bootstrap4.Row

    class Container(ActiveHTMLWrapper):
        base = Bootstrap4.Container

    class Button(ActiveHTMLWrapper):
        base = Bootstrap4.Button

    class LinkButton(HTML.Anchor):
        base = Bootstrap4.LinkButton

    class Table(ActiveHTMLWrapper):
        base = Bootstrap4.Table

    class ListGroup(ActiveHTMLWrapper):
        base = Bootstrap4.ListGroup

    class ListGroupItem(ActiveHTMLWrapper):
        base = Bootstrap4.ListGroupItem

    class FontAwesomeIcon(ActiveHTMLWrapper):
        base = Bootstrap4.FontAwesomeIcon

    class GlyphIcon(ActiveHTMLWrapper):
        base = Bootstrap4.GlyphIcon

    class Label(ActiveHTMLWrapper):
        base = Bootstrap4.Label

    class Pill(ActiveHTMLWrapper):
        base = Bootstrap4.Pill

    class ListComponent(ActiveHTMLWrapper):
        base = Bootstrap4.ListComponent

    class ListItemComponent(ActiveHTMLWrapper):
        base = Bootstrap4.ListItemComponent

    class Breadcrumb(ActiveHTMLWrapper):
        base = Bootstrap4.Breadcrumb

    class BreadcrumbItem(ActiveHTMLWrapper):
        base = Bootstrap4.BreadcrumbItem

class Bootstrap5Widgets(BootstrapWidgetsBase):
    cdn_js = ['https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js']
    bootstrap_version = Bootstrap5

    class Icon(HTMLWidgets.WrappedHTMLElement):
        base = Bootstrap5.Icon

    class Alert(HTMLWidgets.WrappedHTMLElement):
        base = Bootstrap5.Alert

    class Badge(HTMLWidgets.WrappedHTMLElement):
        base = Bootstrap5.Badge

    class CardBody(HTMLWidgets.WrappedHTMLElement):
        base = Bootstrap5.CardBody

    class CardHeader(HTMLWidgets.WrappedHTMLElement):
        base = Bootstrap5.CardHeader

    class CardFooter(HTMLWidgets.WrappedHTMLElement):
        base = Bootstrap5.CardFooter

    class CardImage(HTMLWidgets.WrappedHTMLElement):
        base = Bootstrap5.CardImage

    class Card(HTMLWidgets.WrappedHTMLElement):
        base = Bootstrap5.Card

    class Col(HTMLWidgets.WrappedHTMLElement):
        base = Bootstrap5.Col

    class Row(HTMLWidgets.WrappedHTMLElement):
        base = Bootstrap5.Row

    class Container(HTMLWidgets.WrappedHTMLElement):
        base = Bootstrap5.Container

    class ButtonGroup(HTMLWidgets.WrappedHTMLElement):
        base = Bootstrap5.ButtonGroup

    class Button(HTMLWidgets.WrappedHTMLElement):
        base = Bootstrap5.Button

    class CloseButton(HTMLWidgets.WrappedHTMLElement):
        base = Bootstrap5.CloseButton

    class LinkButton(HTMLWidgets.WrappedHTMLElement):
        base = Bootstrap5.LinkButton

    class Table(HTMLWidgets.WrappedHTMLElement):
        base = Bootstrap5.Table

    class ListGroup(HTMLWidgets.WrappedHTMLElement):
        base = Bootstrap5.ListGroup

    class ListGroupItem(HTMLWidgets.WrappedHTMLElement):
        base = Bootstrap5.ListGroupItem

    class FontAwesomeIcon(HTMLWidgets.WrappedHTMLElement):
        base = Bootstrap5.FontAwesomeIcon

    class GlyphIcon(HTMLWidgets.WrappedHTMLElement):
        base = Bootstrap5.GlyphIcon

    class Label(HTMLWidgets.WrappedHTMLElement):
        base = Bootstrap5.Label

    class Pill(HTMLWidgets.WrappedHTMLElement):
        base = Bootstrap5.Pill

    class ListComponent(HTMLWidgets.WrappedHTMLElement):
        base = Bootstrap5.ListComponent

    class ListItemComponent(HTMLWidgets.WrappedHTMLElement):
        base = Bootstrap5.ListItemComponent

    class Breadcrumb(HTMLWidgets.WrappedHTMLElement):
        base = Bootstrap5.Breadcrumb

    class BreadcrumbItem(HTMLWidgets.WrappedHTMLElement):
        base = Bootstrap5.BreadcrumbItem
BootstrapWidgets = Bootstrap5Widgets
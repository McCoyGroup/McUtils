from .HTML import HTML
from .HTMLWidgets import HTMLWidgets, JupyterHTMLWrapper
from .Bootstrap import Bootstrap3, Bootstrap4, Bootstrap5

__all__ = ["BootstrapWidgets"]
__reload_hook__ = [".HTML", ".HTMLWidgets", ".Bootstrap"]

class BootstrapWidgetsBase:
    cdn_loader = None
    bootstrap_version = None

    @classmethod
    def load(cls):
        """
        Embeds Bootstrap style definitions into the active notebook

        :return:
        :rtype:
        """
        from IPython.core.display import HTML as IPyHTML
        return IPyHTML(
            cls.cdn_loader
            + """
            <div class="alert alert-info">Boostrap loaded</div>
            """
        )

    @classmethod
    def _monkey_patch(cls):
        for key, value in vars(cls.bootstrap_version).items():
            if (
                    not hasattr(cls, key)
                    and isinstance(value, type)
                    and issubclass(value, HTML.XMLElement)
            ): setattr(cls, key, type(key, (HTMLWidgets.WrappedElement,), dict(base=value)) )

    @classmethod
    def Grid(cls, rows, row_attributes=None, item_attributes=None, auto_size=True, **attrs):
        return HTMLWidgets.WrappedElement(rows, base=cls.bootstrap_version.Grid, row_attributes=row_attributes,
                                          item_attributes=item_attributes, auto_size=auto_size, **attrs)

class Bootstrap3Widgets(BootstrapWidgetsBase):
    cdn_loader = """
    <!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
<!-- Optional theme -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">
<!-- Latest compiled and minified JavaScript -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
"""
    bootstrap_version = Bootstrap3
    class Icon(HTMLWidgets.WrappedElement): base = Bootstrap3.Icon
    class Alert(HTMLWidgets.WrappedElement): base = Bootstrap3.Alert
    class Badge(HTMLWidgets.WrappedElement): base = Bootstrap3.Badge
    class PanelBody(HTMLWidgets.WrappedElement): base = Bootstrap3.PanelBody
    class PanelHeader(HTMLWidgets.WrappedElement): base = Bootstrap3.PanelHeader
    class Panel(HTMLWidgets.WrappedElement): base = Bootstrap3.Panel
    class Jumbotron(HTMLWidgets.WrappedElement): base = Bootstrap3.Jumbotron
    class Col(HTMLWidgets.ContainerWrapper): base = Bootstrap3.Col
    class Row(HTMLWidgets.ContainerWrapper): base = Bootstrap3.Row
    class Container(HTMLWidgets.ContainerWrapper): base = Bootstrap3.Container
    class Button(HTMLWidgets.WrappedElement): base = Bootstrap3.Button
    class LinkButton(HTML.Anchor): base = Bootstrap3.LinkButton
    class Table(HTMLWidgets.WrappedElement): base = Bootstrap3.Table
    class ListGroup(HTMLWidgets.WrappedElement): base = Bootstrap3.ListGroup
    class ListGroupItem(HTMLWidgets.WrappedElement): base = Bootstrap3.ListGroupItem
    class FontAwesomeIcon(HTMLWidgets.WrappedElement): base = Bootstrap3.FontAwesomeIcon
    class GlyphIcon(HTMLWidgets.WrappedElement): base = Bootstrap3.GlyphIcon
    class Label(HTMLWidgets.WrappedElement): base = Bootstrap3.Label
    class ListComponent(HTMLWidgets.WrappedElement): base = Bootstrap3.ListComponent
    class ListItemComponent(HTMLWidgets.WrappedElement): base = Bootstrap3.ListItemComponent
    class Breadcrumb(HTMLWidgets.WrappedElement): base = Bootstrap3.Breadcrumb
    class BreadcrumbItem(HTMLWidgets.WrappedElement): base = Bootstrap3.BreadcrumbItem
Bootstrap3Widgets._monkey_patch()

class Bootstrap4Widgets(BootstrapWidgetsBase):
    cdn_loader = """
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css" integrity="sha384-zCbKRCUGaJDkqS1kPbPd7TveP5iyJE0EjAuZQTgFLD2ylzuqKfdKlfG/eSrtxUkn" crossorigin="anonymous">
            <script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-fQybjgWLrvvRgtW6bFlB7jaZrFsaBXjsOMm/tB9LTS58ONXgqbR9W8oWht/amnpF" crossorigin="anonymous"></script>
            """
    bootstrap_version = Bootstrap4
    class Icon(HTMLWidgets.WrappedElement): base = Bootstrap4.Icon
    class Alert(HTMLWidgets.WrappedElement): base = Bootstrap4.Alert
    class Badge(HTMLWidgets.WrappedElement): base = Bootstrap4.Badge
    class CardBody(HTMLWidgets.WrappedElement): base = Bootstrap4.CardBody
    class CardHeader(HTMLWidgets.WrappedElement): base = Bootstrap4.CardHeader
    class CardFooter(HTMLWidgets.WrappedElement): base = Bootstrap4.CardFooter
    class CardImage(HTMLWidgets.WrappedElement): base = Bootstrap4.CardImage
    class Card(HTMLWidgets.WrappedElement): base = Bootstrap4.Card
    class Jumbotron(HTMLWidgets.WrappedElement): base = Bootstrap4.Jumbotron
    class Col(HTMLWidgets.ContainerWrapper): base = Bootstrap4.Col
    class Row(HTMLWidgets.ContainerWrapper): base = Bootstrap4.Row
    class Container(HTMLWidgets.ContainerWrapper): base = Bootstrap4.Container
    class Button(HTMLWidgets.WrappedElement): base = Bootstrap4.Button
    class LinkButton(HTML.Anchor): base = Bootstrap4.LinkButton
    class Table(HTMLWidgets.WrappedElement): base = Bootstrap4.Table
    class ListGroup(HTMLWidgets.WrappedElement): base = Bootstrap4.ListGroup
    class ListGroupItem(HTMLWidgets.WrappedElement): base = Bootstrap4.ListGroupItem
    class FontAwesomeIcon(HTMLWidgets.WrappedElement): base = Bootstrap4.FontAwesomeIcon
    class GlyphIcon(HTMLWidgets.WrappedElement): base = Bootstrap4.GlyphIcon
    class Label(HTMLWidgets.WrappedElement): base = Bootstrap4.Label
    class Pill(HTMLWidgets.WrappedElement): base = Bootstrap4.Pill
    class ListComponent(HTMLWidgets.WrappedElement): base = Bootstrap4.ListComponent
    class ListItemComponent(HTMLWidgets.WrappedElement): base = Bootstrap4.ListItemComponent
    class Breadcrumb(HTMLWidgets.WrappedElement): base = Bootstrap4.Breadcrumb
    class BreadcrumbItem(HTMLWidgets.WrappedElement): base = Bootstrap4.BreadcrumbItem
Bootstrap4Widgets._monkey_patch()

class Bootstrap5Widgets(BootstrapWidgetsBase):
    cdn_loader = """
            <!-- CSS only -->
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
            <!-- JavaScript Bundle with Popper -->
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.1/font/bootstrap-icons.css">
            """
    bootstrap_version = Bootstrap5
    class Icon(HTMLWidgets.WrappedElement): base = Bootstrap5.Icon
    class Alert(HTMLWidgets.WrappedElement): base = Bootstrap5.Alert
    class Badge(HTMLWidgets.WrappedElement): base = Bootstrap5.Badge
    class CardBody(HTMLWidgets.WrappedElement): base = Bootstrap5.CardBody
    class CardHeader(HTMLWidgets.WrappedElement): base = Bootstrap5.CardHeader
    class CardFooter(HTMLWidgets.WrappedElement): base = Bootstrap5.CardFooter
    class CardImage(HTMLWidgets.WrappedElement): base = Bootstrap5.CardImage
    class Card(HTMLWidgets.WrappedElement): base = Bootstrap5.Card
    class Col(HTMLWidgets.ContainerWrapper): base = Bootstrap5.Col
    class Row(HTMLWidgets.ContainerWrapper): base = Bootstrap5.Row
    class Container(HTMLWidgets.ContainerWrapper): base = Bootstrap5.Container
    class Button(HTMLWidgets.WrappedElement): base = Bootstrap5.Button
    class LinkButton(HTML.Anchor): base = Bootstrap5.LinkButton
    class Table(HTMLWidgets.WrappedElement): base = Bootstrap5.Table
    class ListGroup(HTMLWidgets.WrappedElement): base = Bootstrap5.ListGroup
    class ListGroupItem(HTMLWidgets.WrappedElement): base = Bootstrap5.ListGroupItem
    class FontAwesomeIcon(HTMLWidgets.WrappedElement): base = Bootstrap5.FontAwesomeIcon
    class GlyphIcon(HTMLWidgets.WrappedElement): base = Bootstrap5.GlyphIcon
    class Label(HTMLWidgets.WrappedElement): base = Bootstrap5.Label
    class Pill(HTMLWidgets.WrappedElement): base = Bootstrap5.Pill
    class ListComponent(HTMLWidgets.WrappedElement): base = Bootstrap5.ListComponent
    class ListItemComponent(HTMLWidgets.WrappedElement): base = Bootstrap5.ListItemComponent
    class Breadcrumb(HTMLWidgets.WrappedElement): base = Bootstrap5.Breadcrumb
    class BreadcrumbItem(HTMLWidgets.WrappedElement): base = Bootstrap5.BreadcrumbItem
Bootstrap5Widgets._monkey_patch()

BootstrapWidgets = Bootstrap5Widgets
JupyterHTMLWrapper._widget_sources.append(BootstrapWidgets)
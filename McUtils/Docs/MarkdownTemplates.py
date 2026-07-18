
import re, uuid, pathlib
from ..Formatters.TemplateEngine import *
from ..Jupyter.JHTML import *

class MarkdownOps:
    @classmethod
    def format_item(self, item, item_level = 0):
        """
        **LLM Docstring**

        Formats a value as an indented Markdown list item.

        :param item: the item content
        :type item: Any

        :param item_level: the zero-based nesting level
        :type item_level: int
        :return: the Markdown list-item string
        :rtype: str
        """
        return "{}- {}".format('  ' * (item_level + 1), item)
    @classmethod
    def format_link(self, alt, link):
        """
        **LLM Docstring**

        Formats a Markdown hyperlink.

        :param alt: the visible link text
        :type alt: str

        :param link: the target URL or path
        :type link: str
        :return: the Markdown link
        :rtype: str
        """
        return '[{}]({})'.format(alt, link)
    @classmethod
    def format_obj_link(self, spec, root=None):
        """
        **LLM Docstring**

        Formats a link to a documented object using its canonical name and path.

        :param spec: the object identifier
        :type spec: str

        :param root: an optional root passed to canonical-link generation
        :type root: str | None
        :return: the Markdown object link
        :rtype: str
        """
        return self.format_link(self.canonical_name(spec), self.canonical_link(spec, root=root))
    @classmethod
    def format_inline_code(self, arg):
        """

        :param arg:
        :type arg: str
        :return:
        :rtype:
        """
        nticks = arg.count("`")
        fence = "`"*(nticks+1)
        return fence + arg + fence
    @classmethod
    def format_code_block(self, arg):
        """

        :param arg:
        :type arg: str
        :return:
        :rtype:
        """
        nticks = arg.count("`")
        fence = "`"*(nticks+3)
        return fence + "python\n" + arg + "\n" + fence
    @classmethod
    def format_quote_block(self, arg):
        """

        :param arg:
        :type arg: str
        :return:
        :rtype:
        """

        return ">" + arg.replace("\n", "\n>")

    link_bar_template='<div class="container{boxed}">\n{links}\n</div>'
    link_row_template='  <div class="row">\n{cols}\n</div>'
    link_item_template='   <div class="col" markdown="1">\n{item}   \n</div>'
    @classmethod
    def format_grid(self, link_grid, boxed=False):
        """
        **LLM Docstring**

        Renders rows of Markdown content inside the module's Bootstrap-style HTML grid templates.

        :param link_grid: rows of already-formatted grid items
        :type link_grid: Iterable[Iterable[str]]

        :param boxed: whether to add alert/background classes to the outer container
        :type boxed: bool
        :return: the HTML grid markup
        :rtype: str
        """
        return self.link_bar_template.format(links="\n".join(
            self.link_row_template.format(
                cols="\n".join(self.link_item_template.format(item=item) for item in row)
            )
            for row in link_grid if len(row) > 0
        ),
        boxed=' alert alert-secondary bg-light' if boxed else ""
        )
    @classmethod
    def split(self, links, ncols=3, pad=""):
        """
        **LLM Docstring**

        Splits a sequence into fixed-width rows and pads the final row.

        :param links: the values to partition
        :type links: Iterable[Any]

        :param ncols: the number of entries per row
        :type ncols: int

        :param pad: the value used to fill the final row
        :type pad: Any
        :return: a list of rows, including a padded final row
        :rtype: list[list[Any]]
        """
        num_cols = ncols
        splits = []
        sub = []
        for x in links:
            sub.append(x)
            if len(sub) == num_cols:
                splits.append(sub)
                sub = []
        splits.append(sub + [pad] * (ncols - len(sub)))
        return splits

    collapse_template="""
<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
{header_fmt} <a class="collapse-link" data-toggle="collapse" href="#{name}" markdown="1">{header}</a> {opener}
 </div>
 <div class="collapsible-section collapsible-section-body collapse {show}" id="{name}" markdown="1">
 {content}
 </div>
</div>
"""
    collapse_opener = '<a class="float-right" data-toggle="collapse" href="#{name}"><i class="fa fa-chevron-down"></i></a>'
    @classmethod
    def format_collapse_section(self, header, content, name=None, open=True, include_opener=True):
        """
        **LLM Docstring**

        Formats content as a Bootstrap-compatible collapsible section.

        :param header: the section heading, optionally prefixed with Markdown heading markers
        :type header: str

        :param content: the section body
        :type content: str

        :param name: the collapse element identifier; generated from the heading when omitted
        :type name: str | None

        :param open: whether the body initially has the `show` class
        :type open: bool

        :param include_opener: whether to include the chevron toggle link
        :type include_opener: bool
        :return: the collapsible-section HTML
        :rtype: str
        """
        header_fmt = ""
        while header.startswith("#"):
            header_fmt += "#"
            header = header[1:]
        if name is None:
            name = re.sub(r"\W", "", header) + "-" + str(uuid.uuid4())[:6]
        return self.collapse_template.format(
            header_fmt=header_fmt,
            header=header,
            content=content,
            name=name,
            show="show" if open else "",
            opener=self.collapse_opener.format(name=name) if include_opener else ""
        )

    @classmethod
    def format_obj_link_grid(self, mems, ncols=3, root=None, boxed=True):
        """
        **LLM Docstring**

        Builds a boxed grid of canonical links for object identifiers.

        :param mems: object identifiers, or a mapping whose values are identifiers
        :type mems: Mapping[Any, str] | Iterable[str]

        :param ncols: the number of links per row
        :type ncols: int

        :param root: an optional root for canonical link generation
        :type root: str | None

        :param boxed: whether to style the outer grid as a boxed alert
        :type boxed: bool
        :return: the formatted grid markup
        :rtype: str
        """
        links = self.split(
            [self.format_obj_link(l, root=root) for l in (mems.values() if hasattr(mems, 'values') else mems)],
            ncols=ncols
        )
        return self.format_grid(links, boxed=boxed)

    @classmethod
    def canonical_name(self, identifier, formatter=None):
        """
        **LLM Docstring**

        Returns the final dotted component of an object identifier.

        :param identifier: the dotted identifier
        :type identifier: str

        :param formatter: unused formatter compatibility argument
        :type formatter: Any | None
        :return: the final identifier component
        :rtype: str
        """
        return identifier.split(".")[-1]

    @classmethod
    def canonical_link(self, identifier, root=None, formatter=None):
        """
        **LLM Docstring**

        Converts a dotted object identifier into a relative Markdown filename.

        :param identifier: the identifier, where leading dots request parent-directory traversal
        :type identifier: str

        :param root: unused root compatibility argument
        :type root: str | None

        :param formatter: unused formatter compatibility argument
        :type formatter: Any | None
        :return: a relative `.md` path
        :rtype: str
        """
        ups = 0
        # if root is not None and identifier.startswith(root):
        #     identifier = identifier[len(root):]
        #     if identifier.startswith('.'):
        #         identifier = identifier[1:]
        while identifier[0] == ".":
            ups += 1
            identifier = identifier[1:]
        if ups > 0:
            pad = "../"*ups
        else:
            pad = ""
        identifier = "/".join(identifier.split("."))
        return pad + identifier + ".md"

    @classmethod
    def html(kls, tag, content, markdown=True, formatter=None, **styles):
        """
        **LLM Docstring**

        Wraps content in a `JHTML.HTML` element and substitutes it after serialization.

        :param tag: the `HTML` constructor name
        :type tag: str

        :param content: the body inserted into the serialized element
        :type content: str

        :param markdown: whether to set `markdown="1"`
        :type markdown: bool

        :param formatter: unused formatter compatibility argument
        :type formatter: Any | None

        :param styles: additional element attributes
        :type styles: Any
        :return: serialized HTML markup
        :rtype: str
        """
        if markdown:
            styles["markdown"] = "1"
        return getattr(HTML, tag)("\n{content}\n", **styles).tostring().format(content=content)
    @classmethod
    def bootstrap(kls, tag, content, markdown=True, formatter=None, **styles):
        """
        **LLM Docstring**

        Wraps content in a Bootstrap JHTML component and substitutes it after serialization.

        :param tag: the `Bootstrap` constructor name
        :type tag: str

        :param content: the body inserted into the serialized element
        :type content: str

        :param markdown: whether to set `markdown="1"`
        :type markdown: bool

        :param formatter: unused formatter compatibility argument
        :type formatter: Any | None

        :param styles: additional component attributes
        :type styles: Any
        :return: serialized component markup
        :rtype: str
        """
        if markdown:
            styles["markdown"] = "1"
        return getattr(Bootstrap, tag)("\n{content}\n", **styles).tostring().format(content=content)
    @classmethod
    def alert(kls, content, variant='warning', markdown=True, formatter=None, **styles):
        """
        **LLM Docstring**

        Formats content with the Bootstrap `Alert` component.

        :param content: the alert body
        :type content: str

        :param variant: the Bootstrap alert variant
        :type variant: str

        :param markdown: whether the content should be interpreted as Markdown
        :type markdown: bool

        :param formatter: unused formatter compatibility argument
        :type formatter: Any | None

        :param styles: additional alert attributes
        :type styles: Any
        :return: serialized alert markup
        :rtype: str
        """
        return kls.bootstrap('Alert', content, variant=variant, markdown=markdown, **styles)

class MarkdownFormatDirective(FormatDirective):
    Link = "link", TemplateOps.wrap(MarkdownOps.format_link)
    ObjLink = "objlink", TemplateOps.wrap(MarkdownOps.format_obj_link)
    Item = "item", TemplateOps.wrap(MarkdownOps.format_item)
    Code = "code", TemplateOps.wrap(MarkdownOps.format_code_block)
    Quote = "quote", TemplateOps.wrap(MarkdownOps.format_quote_block)
    # Card = "card", TemplateOps.wrap(MarkdownFormatter.format_card)
    # Alert = "alert", TemplateOps.wrap(MarkdownFormatter.format_alert)
    Collapse = "collapse", TemplateOps.wrap(MarkdownOps.format_collapse_section)
    Grid = "grid", TemplateOps.wrap(MarkdownOps.format_grid)
    Split = "split", TemplateOps.wrap(MarkdownOps.split)
    ObjLinkGrid = "objlink_grid", TemplateOps.wrap(MarkdownOps.format_obj_link_grid)
    CanonicalName = "canonical_name", MarkdownOps.canonical_name
    CanonicalLink = "canonical_link", MarkdownOps.canonical_link
    HTML = "html", MarkdownOps.html
    Bootstrap = "bootstrap", MarkdownOps.bootstrap
    Alert = "alert", MarkdownOps.alert
MarkdownFormatDirective = TemplateFormatDirective.extend(MarkdownFormatDirective)

class MarkdownTemplateFormatter(TemplateFormatter):
    directives = MarkdownFormatDirective

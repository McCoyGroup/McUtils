"""
static_docs.py

Provides `static_doc`, a sibling to `McUtils.Docs.jdoc` that walks an object
with the *exact same* `DocWalker` / `ModuleWriter` / `ClassWriter` /
`FunctionWriter` / `MethodWriter` / `ObjectWriter` / `IndexWriter` machinery
`jdoc` uses, but swaps out the ipywidget-producing `InteractiveTemplateEngine`
for a new `StaticHTMLTemplateEngine` that builds its output with the same
`McUtils.Jupyter.JHTML` element interfaces `InteractiveTemplateEngine` uses
(`JHTML.Div`, `JHTML.Details`, `JHTML.Heading`, ...) -- just without any of
the calls that trigger JHTML's *widget* backend (`event_handlers`,
`track_value`, `Opener`/`CardOpener`/`VariableDisplay`, etc). JHTML dispatches
every element to a plain, kernel-free `XMLElement` unless one of those is
requested, so the same element constructors used for the live widget tree
serialize here straight to text via `.tostring()`.

The finx (McCoyGroup/finx) theme's CSS and a couple of its JS files are
embedded directly into the page (using `JHTML.Style`/`JHTML.Script`, whose
text children pass through unescaped), so the output is a single portable
`.html` file with no external dependencies (besides an optional CDN jQuery
needed by the baked-in `init.js`), explorable via native `<details>`
elements -- no live kernel, no ipywidgets, works fine on mobile.
"""
import io
import contextlib
from .DocWalker import DocWalker
from ..Jupyter import JHTML
from ..Formatters.TemplateEngine.TemplateEngine import TemplateInterfaceEngine, TemplateHandler
__all__ = ['JHTMLDocumentationEngine', 'static_doc']
_FINX_RAW = 'https://raw.githubusercontent.com/McCoyGroup/finx/master/assets'
_FINX_CSS_FILES = ['style.css', 'docs.css', 'pygment_trac.css']
_FINX_JS_FILES = ['init.js']
_FINX_ASSET_CACHE = {}

def _fetch_finx_asset(kind, name):
    """
    Downloads (and caches) one file from the finx assets/ directory.
    `kind` is 'css' or 'js'.
    """
    ...

def _bake_finx_assets(extra_css='', include_js=True):
    """
    **LLM Docstring**

    Builds JHTML style and script elements containing the configured finx assets.

    :param extra_css: additional CSS appended after the bundled styles
    :type extra_css: str

    :param include_js: whether to include jQuery and the finx JavaScript assets
    :type include_js: bool
    :return: style elements and, optionally, script elements
    :rtype: list
    """
    ...

class JHTMLDocumentationEngine(TemplateInterfaceEngine):
    """
    Renders the same fields `InteractiveTemplateEngine` renders into
    ipywidget-backed JHTML elements, but using only the plain (non-widget)
    side of the same `JHTML` element interfaces -- `JHTML.Div`,
    `JHTML.Details`/`JHTML.Summary`, `JHTML.Heading` & friends, `JHTML.Code`,
    `JHTML.Markdown`, `JHTML.List`/`JHTML.ListItem` -- so the whole tree
    serializes to plain text via `.tostring()` with no kernel involved.

    :related: McUtils.Docs.DocWalker.InteractiveTemplateEngine, McUtils.Docs.jdoc
    """

    def __init__(self, templates=None, ignore_missing=False, formatter_class=None, ignore_paths=()):
        """
        **LLM Docstring**

        Initializes the static documentation engine with callable templates for each documentation object type.

        :param templates: custom template handlers; defaults to the six browser methods
        :type templates: Mapping[str, Callable] | None

        :param ignore_missing: whether missing template fields should be ignored
        :type ignore_missing: bool

        :param formatter_class: an optional formatter class passed to the base engine
        :type formatter_class: type | None

        :param ignore_paths: template paths to ignore
        :type ignore_paths: Iterable[str]
        """
        ...

    @staticmethod
    def md(text):
        """
        **LLM Docstring**

        Converts nonempty Markdown text to a JHTML Markdown element.

        :param text: the text to render
        :type text: str | None
        :return: a Markdown element, or an empty span for falsey input
        :rtype: Any
        """
        ...

    @classmethod
    def clean_params(cls, params):
        """
        **LLM Docstring**

        Removes fields whose values are `None` or empty strings.

        :param params: the fields to filter
        :type params: Mapping[Any, Any]
        :return: a dictionary containing only nonempty values
        :rtype: dict
        """
        ...

    def params_table(self, parameters):
        """
        **LLM Docstring**

        Renders parsed parameter metadata as a documentation list.

        :param parameters: parameter names with type and description fields
        :type parameters: Mapping[str, Mapping[str, str]] | None
        :return: a JHTML list, or an empty span when no parameters are supplied
        :rtype: Any
        """
        ...

    def extra_sections(self, **fields):
        """
        **LLM Docstring**

        Renders nonempty named fields as native `<details>` sections.

        :param fields: section labels mapped to Markdown content
        :type fields: Any
        :return: the generated details elements
        :rtype: list
        """
        ...

    def code_block(self, decorator, name, signature):
        """
        **LLM Docstring**

        Renders a compact Python function signature block.

        :param decorator: decorator text prepended to the function definition
        :type decorator: str | None

        :param name: the function name
        :type name: str

        :param signature: the parenthesized signature
        :type signature: str
        :return: a highlighted JHTML preformatted block
        :rtype: Any
        """
        ...

    def index_browser(self, index_files=None, details=None, related=None, description=None, examples=None, _self=None, **kw):
        """
        **LLM Docstring**

        Renders an index page from its description, child index entries, and optional sections

        :param index_files: rendered index entries
        :type index_files: Iterable[Any] | None

        :param details: details Markdown
        :type details: str | None

        :param related: related-object Markdown
        :type related: str | None

        :param description: index description
        :type description: str | None

        :param examples: examples Markdown
        :type examples: str | None

        :param _self: the active template handler
        :type _self: Any | None

        :param kw: unused template fields
        :type kw: Any
        :return: a JHTML index container
        :rtype: Any
        """
        ...

    def module_browser(self, members=None, name=None, id=None, details=None, related=None, description=None, examples=None, tests=None, lineno=None, _self=None, **kw):
        """
        **LLM Docstring**

        Renders a module section with expandable output for each documented member

        :param members: member identifiers
        :type members: Mapping[str, Any] | None

        :param name: module name
        :type name: str | None

        :param id: anchor identifier
        :type id: str | None

        :param details: details Markdown
        :type details: str | None

        :param related: related-object Markdown
        :type related: str | None

        :param description: module description
        :type description: str | None

        :param examples: examples Markdown
        :type examples: str | None

        :param tests: test/example data
        :type tests: Any | None

        :param lineno: source line metadata
        :type lineno: int | str | None

        :param _self: the active template handler
        :type _self: Any

        :param kw: unused template fields
        :type kw: Any
        :return: a JHTML module section
        :rtype: Any
        """
        ...

    def class_browser(self, id=None, name=None, related=None, out_file=None, lineno=None, parameters=None, props=None, description=None, methods=None, examples=None, tests=None, details=None, _self=None, **_):
        """
        **LLM Docstring**

        Renders a class section containing description, properties, parameters, and handled methods

        :param id: anchor identifier
        :type id: str | None

        :param name: class name
        :type name: str | None

        :param related: related-object Markdown
        :type related: str | None

        :param out_file: unused output-file metadata
        :type out_file: str | None

        :param lineno: source line metadata
        :type lineno: int | str | None

        :param parameters: parsed parameter metadata
        :type parameters: Mapping[str, Any] | None

        :param props: public property metadata
        :type props: Iterable[tuple[str, Any]] | None

        :param description: class description
        :type description: str | None

        :param methods: method handlers
        :type methods: Iterable[Any] | None

        :param examples: examples Markdown
        :type examples: str | None

        :param tests: unused test metadata
        :type tests: Any | None

        :param details: details Markdown
        :type details: str | None

        :param _self: the active handler
        :type _self: Any | None

        :param _: unused template fields
        :type _: Any
        :return: a JHTML class section
        :rtype: Any
        """
        ...

    def method_browser(self, id=None, name=None, decorator=None, signature=None, related=None, out_file=None, lineno=None, parameters=None, props=None, description=None, examples=None, tests=None, details=None, **_):
        """
        **LLM Docstring**

        Renders a method as a collapsible details element with signature and documentation

        :param id: anchor identifier
        :type id: str | None

        :param name: method name
        :type name: str

        :param decorator: decorator text
        :type decorator: str | None

        :param signature: method signature
        :type signature: str

        :param related: unused related metadata
        :type related: str | None

        :param out_file: unused output metadata
        :type out_file: str | None

        :param lineno: source line metadata
        :type lineno: int | str | None

        :param parameters: parsed parameters
        :type parameters: Mapping[str, Any] | None

        :param props: unused property metadata
        :type props: Any | None

        :param description: method description
        :type description: str | None

        :param examples: examples Markdown
        :type examples: str | None

        :param tests: unused test metadata
        :type tests: Any | None

        :param details: details Markdown
        :type details: str | None

        :param _: unused template fields
        :type _: Any
        :return: a JHTML details element
        :rtype: Any
        """
        ...

    def object_browser(self, id=None, name=None, related=None, out_file=None, lineno=None, parameters=None, props=None, description=None, methods=None, examples=None, tests=None, details=None, _self=None, **_):
        """
        **LLM Docstring**

        Renders a generic object section with its runtime type and optional documentation sections

        :param id: anchor identifier
        :type id: str | None

        :param name: object name
        :type name: str

        :param related: unused related metadata
        :type related: str | None

        :param out_file: unused output metadata
        :type out_file: str | None

        :param lineno: source line metadata
        :type lineno: int | str | None

        :param parameters: unused parameter metadata
        :type parameters: Any | None

        :param props: unused property metadata
        :type props: Any | None

        :param description: object description
        :type description: str | None

        :param methods: unused method metadata
        :type methods: Any | None

        :param examples: examples Markdown
        :type examples: str | None

        :param tests: unused test metadata
        :type tests: Any | None

        :param details: details Markdown
        :type details: str | None

        :param _self: the active handler containing the object
        :type _self: Any

        :param _: unused template fields
        :type _: Any
        :return: a JHTML object section
        :rtype: Any
        """
        ...

    def function_browser(self, id=None, name=None, decorator=None, signature=None, related=None, out_file=None, lineno=None, parameters=None, props=None, description=None, examples=None, tests=None, details=None, **_):
        """
        **LLM Docstring**

        Renders a function section containing its signature, description, parameters, and optional sections

        :param id: anchor identifier
        :type id: str | None

        :param name: function name
        :type name: str

        :param decorator: decorator text
        :type decorator: str | None

        :param signature: function signature
        :type signature: str

        :param related: unused related metadata
        :type related: str | None

        :param out_file: unused output metadata
        :type out_file: str | None

        :param lineno: source line metadata
        :type lineno: int | str | None

        :param parameters: parsed parameters
        :type parameters: Mapping[str, Any] | None

        :param props: unused property metadata
        :type props: Any | None

        :param description: function description
        :type description: str | None

        :param examples: examples Markdown
        :type examples: str | None

        :param tests: unused test metadata
        :type tests: Any | None

        :param details: details Markdown
        :type details: str | None

        :param _: unused template fields
        :type _: Any
        :return: a JHTML function section
        :rtype: Any
        """
        ...

def static_doc(obj, max_depth=1, title=None, out_file=None, include_finx_js=True, verbose=False, return_string=False):
    """
    The static-HTML sibling of `McUtils.Docs.jdoc`.

    Walks `obj` with the exact same `DocWalker` machinery `jdoc` uses
    (`ModuleWriter`, `ClassWriter`, `FunctionWriter`, `MethodWriter`,
    `ObjectWriter`, `IndexWriter`), but renders through a
    `StaticHTMLTemplateEngine` instead of the ipywidget-producing
    `InteractiveTemplateEngine`. Both engines build their output out of the
    same `McUtils.Jupyter.JHTML` element interfaces; this one just never
    triggers JHTML's widget-dispatch path, so the whole tree comes back as
    one self-contained static HTML document (finx CSS/JS baked in) instead
    of a live widget tree.

    :param obj: the object (module, class, function, ...) to document
    :param max_depth: how far down the object tree to recurse (same meaning as in `jdoc`)
    :param title: page title (defaults to the object's name)
    :param out_file: if given, the HTML is written to this path and the path is returned;
        otherwise the HTML string itself is returned
    :param include_finx_js: whether to bake in finx's `init.js` (+ a CDN jQuery) for
        the sidebar-toggle behavior; the CSS is always included
    :param verbose: `DocWalker` prints a line per module/class it visits;
        set `True` to see that progress chatter
    :return: the HTML string, or the path written to if `out_file` was given
    """
    ...
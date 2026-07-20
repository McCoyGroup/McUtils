"""
Provides a class that will walk through a set of objects & their children, as loaded into memory, and will generate Markdown for each.
The actual object Markdown is written by the things in the `Writers` module.
"""
import os, types, collections, inspect, importlib, re, uuid
import subprocess
import sys
from ..Formatters.TemplateEngine import *
from ..Misc import mixedmethod
from .ExamplesParser import ExamplesParser
from .MarkdownTemplates import MarkdownTemplateFormatter, MarkdownOps
__reload_hook__ = ['..Misc']
__all__ = ['DocWalker', 'ModuleWriter', 'ClassWriter', 'FunctionWriter', 'MethodWriter', 'ObjectWriter', 'IndexWriter', 'jdoc']
from ..Formatters.TemplateEngine.TemplateEngine import TemplateInterfaceList

class DocSpec(ObjectSpec):
    """
    A specification for an object to document.
    Supports the fields given by `spec_fields`.
    """
    spec_fields = ('id', 'parent', 'children', 'examples_root', 'tests_root')

    def __repr__(self):
        """
        **LLM Docstring**

        Formats the object specification using its concrete class name and base representation.
        :return: the diagnostic representation
        :rtype: str
        """
        ...

class ExamplesExtractor(TemplateResourceExtractor):
    resource_keys = ['examples']
    resource_attrs = ['__examples__']

class TestsExtractor(TemplateResourceExtractor):
    resource_keys = ['tests']
    resource_attrs = ['__tests__']
    extension = 'Tests.py'

    def path_extension(self, handler: TemplateHandler):
        """
        Provides the default examples path for the object
        :return:
        :rtype:
        """
        ...

    def load(self, handler: TemplateHandler):
        """
        **LLM Docstring**

        Loads a test resource and wraps nonempty source in an `ExamplesParser`.

        :param handler: the documentation handler whose test resource is requested
        :type handler: TemplateHandler
        :return: the parsed tests, or `None` when no resource is found
        :rtype: ExamplesParser | None
        """
        ...

class TestExamplesFormatter:

    def __init__(self, parser):
        """
        **LLM Docstring**

        Initializes the formatter from an existing parser or raw test source.

        :param parser: the parser or Python test source
        :type parser: ExamplesParser | str
        """
        ...

    @classmethod
    def from_file(cls, tests_file):
        """
        **LLM Docstring**

        Creates an examples formatter from a test file.

        :param tests_file: the file to read
        :type tests_file: str | os.PathLike
        :return: the initialized formatter
        :rtype: TestExamplesFormatter
        """
        ...

    def get_template_parameters(self):
        """
        Formats an examples file

        :return:
        :rtype:
        """
        ...

class DocTemplateOps(MarkdownOps):
    ...

class InteractiveTemplateEngine(TemplateInterfaceEngine):

    def __init__(self, templates: TemplateInterfaceList=None, ignore_missing=False, formatter_class=None, ignore_paths=()):
        """
        **LLM Docstring**

        Initializes the interactive documentation engine and its default object templates.

        A unique namespace ID is created for Jupyter variables, and the root display pane is initialized lazily.

        :param templates: custom templates or `None` for the six browser methods
        :type templates: TemplateInterfaceList | None

        :param ignore_missing: whether missing template values should be tolerated
        :type ignore_missing: bool

        :param formatter_class: an optional formatter class
        :type formatter_class: type | None

        :param ignore_paths: template paths to ignore
        :type ignore_paths: Iterable[str]
        """
        ...

    def clean_params(self, params):
        """
        **LLM Docstring**

        Removes fields whose values are `None` or empty strings.

        :param params: the fields to filter
        :type params: Mapping[Any, Any]
        :return: the nonempty fields
        :rtype: dict
        """
        ...

    def prep_pars(self, writer, pars):
        """
        **LLM Docstring**

        Converts named documentation sections into JHTML heading/content pairs.

        `Details` and `Examples` are rendered as Markdown, while `Related` is converted to interactive links.

        :param writer: the writer used to resolve related links
        :type writer: DocTemplateHandler

        :param pars: section labels and values
        :type pars: Mapping[str, Any]
        :return: a mapping suitable for an `Opener`
        :rtype: dict
        """
        ...

    def format_parameters_table(self, parameters):
        """
        **LLM Docstring**

        Renders parsed parameter metadata as a vertical JHTML flex container.

        :param parameters: parameter names with type and description fields
        :type parameters: Mapping[str, Mapping[str, str]]
        :return: the parameter display
        :rtype: Any
        """
        ...

    def format_props_table(self, writer, props):
        """
        **LLM Docstring**

        Renders class property names and runtime type names as a vertical flex container.

        :param writer: unused writer compatibility argument
        :type writer: DocTemplateHandler

        :param props: property-name/value pairs
        :type props: Iterable[tuple[str, Any]]
        :return: the property display
        :rtype: Any
        """
        ...

    def format_related_links(self, writer, related):
        """
        **LLM Docstring**

        Builds interactive links that resolve and display related objects on demand.

        :param writer: the writer used for relative-object resolution
        :type writer: DocTemplateHandler

        :param related: a comma-separated list of related identifiers
        :type related: str
        :return: a JHTML list of link buttons
        :rtype: Any
        """
        ...

    def index_browser(self, index_files=None, details=None, related=None, description=None, examples=None, _self=None, **kw):
        """
        **LLM Docstring**

        Builds the interactive root index and initializes the shared display pane on first use.

        :param kw: template fields consumed according to the method signature
        :type kw: Any
        :return: the rendered JHTML/Flex component
        :rtype: Any
        """
        ...

    def module_browser(self, members=None, name=None, id=None, details=None, related=None, description=None, examples=None, tests=None, lineno=None, _self=None, **kw):
        """
        **LLM Docstring**

        Builds an interactive module view with lazily loaded member documentation.

        :param kw: template fields consumed according to the method signature
        :type kw: Any
        :return: the rendered JHTML/Flex component
        :rtype: Any
        """
        ...

    def class_browser(self, id=None, name=None, related=None, out_file=None, lineno=None, parameters=None, props=None, description=None, methods=None, examples=None, tests=None, details=None, _self=None, **_):
        """
        **LLM Docstring**

        Builds an interactive class view containing properties, parameters, methods, and optional sections.

        :param kw: template fields consumed according to the method signature
        :type kw: Any
        :return: the rendered JHTML/Flex component
        :rtype: Any
        """
        ...

    def method_browser(self, id=None, name=None, decorator=None, signature=None, related=None, out_file=None, lineno=None, parameters=None, props=None, description=None, examples=None, tests=None, details=None, **_):
        """
        **LLM Docstring**

        Builds a collapsible interactive method view with syntax-styled signature and parsed documentation.

        :param kw: template fields consumed according to the method signature
        :type kw: Any
        :return: the rendered JHTML/Flex component
        :rtype: Any
        """
        ...

    def object_browser(self, id=None, name=None, related=None, out_file=None, lineno=None, parameters=None, props=None, description=None, methods=None, examples=None, tests=None, details=None, _self=None, **_):
        """
        **LLM Docstring**

        Builds an interactive fallback view for a general documented object.

        :param kw: template fields consumed according to the method signature
        :type kw: Any
        :return: the rendered JHTML/Flex component
        :rtype: Any
        """
        ...

    def function_browser(self, id=None, name=None, decorator=None, signature=None, related=None, out_file=None, lineno=None, parameters=None, props=None, description=None, examples=None, tests=None, details=None, **_):
        """
        **LLM Docstring**

        Builds an interactive function view with signature, parameter metadata, and optional sections.

        :param kw: template fields consumed according to the method signature
        :type kw: Any
        :return: the rendered JHTML/Flex component
        :rtype: Any
        """
        ...

class DocTemplateHandler(TemplateHandler):
    protected_fields = {'id'}
    default_fields = {'details': '', 'related': ''}

    def __init__(self, obj, *, out=None, engine: TemplateEngine=None, root=None, examples_loader: ExamplesExtractor=None, tests_loader: TestsExtractor=None, include_line_numbers=True, walker: 'TemplateWalker'=None, **extra_fields):
        """
        **LLM Docstring**

        Initializes a documentation template handler and inherits defaults from its walker when needed.

        :param obj: the object being documented
        :type obj: Any

        :param out: the output target
        :type out: str | None

        :param engine: the rendering engine
        :type engine: TemplateEngine | None

        :param root: the documentation root
        :type root: str | None

        :param examples_loader: the examples resource loader
        :type examples_loader: ExamplesExtractor | None

        :param tests_loader: the tests resource loader
        :type tests_loader: TestsExtractor | None

        :param include_line_numbers: whether source-line lookup is enabled
        :type include_line_numbers: bool

        :param walker: the owning walker; a `DocWalker` is created when omitted
        :type walker: TemplateWalker | None

        :param extra_fields: additional template fields
        :type extra_fields: Any
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Formats the handler with its class and resolved identifier.
        :return: the diagnostic representation
        :rtype: str
        """
        ...

    def get_lineno(self):
        """
        **LLM Docstring**

        Finds the one-based source line for the handled object when line numbers are enabled.

        Descriptors are unwrapped to their getter or underlying function; ordinary instances are mapped to their type.
        :return: the source line, or an empty string when lookup fails or is disabled
        :rtype: int | str
        """
        ...

    def parse_doc(self, doc):
        """

        :param doc:
        :type doc: str
        :return:
        :rtype:
        """
        ...

    def load_examples(self):
        """
        **LLM Docstring**

        Loads examples through the configured examples extractor.
        :return: the loaded examples, or `None` without a loader
        :rtype: Any | None
        """
        ...

    def load_tests(self):
        """
        **LLM Docstring**

        Loads and formats tests, falling back to matching tests inherited from the parent handler.

        A nonempty parser is also stored as `parent_tests` for descendant handlers.
        :return: template parameters for matching tests, or `None`
        :rtype: dict | None
        """
        ...

class DocObjectTemplateHandler(DocTemplateHandler):

    def get_package_and_url(self, include_url_base=True):
        """
        **LLM Docstring**

        Normalizes package source URLs so package `__init__.py` paths point to the package module path.

        :param include_url_base: whether the base implementation should include its URL prefix
        :type include_url_base: bool
        :return: the package name and adjusted file URL
        :rtype: tuple[str, str]
        """
        ...

    def load_examples(self):
        """
        **LLM Docstring**

        Loads examples through the configured examples extractor.
        :return: the loaded examples, or `None` without a loader
        :rtype: Any | None
        """
        ...

    def load_tests(self):
        """
        **LLM Docstring**

        Loads and formats tests, falling back to matching tests inherited from the parent handler.

        A nonempty parser is also stored as `parent_tests` for descendant handlers.
        :return: template parameters for matching tests, or `None`
        :rtype: dict | None
        """
        ...

class ModuleWriter(DocTemplateHandler):
    """
    A writer targeted to a module object. Just needs to write the Module metadata.

    :related: DocWalker
    """
    template = 'module.md'

    def __init__(self, obj, is_package_root=None, **kwargs):
        """
        **LLM Docstring**

        Initializes a module writer, importing string module names and detecting package roots.

        :param obj: the module object or import name
        :type obj: types.ModuleType | str

        :param is_package_root: whether the module is a package root; inferred from `__init__.py` when omitted
        :type is_package_root: bool | None

        :param kwargs: additional handler options
        :type kwargs: Any
        """
        ...
    DROP_MODULE_NAMES = True

    def get_template_params(self):
        """
        Provides module specific parameters
        :return:
        :rtype:
        """
        ...

    @classmethod
    def get_members(cls, mod):
        """
        **LLM Docstring**

        Returns the module names explicitly exported through `__all__`.

        :param mod: the module being documented
        :type mod: types.ModuleType
        :return: the exported names, or an empty list
        :rtype: Iterable[str]
        """
        ...

class ClassWriter(DocObjectTemplateHandler):
    """
    A writer targeted to a class

    :related: DocWalker
    """
    template = 'class.md'

    def load_methods(self, function_writer=None):
        """
        Loads the methods supported by the class

        :param function_writer:
        :type function_writer:
        :return:
        :rtype:
        """
        ...

    def format_prop(self, k, o):
        """
        **LLM Docstring**

        Formats a property name and the concrete type name of its value.

        :param k: the property name
        :type k: str

        :param o: the property value
        :type o: Any
        :return: the formatted property description
        :rtype: str
        """
        ...

    def get_template_params(self, function_writer=None):
        """

        :param function_writer:
        :type function_writer:
        :return:
        :rtype:
        """
        ...

class FunctionWriter(DocObjectTemplateHandler):
    """
    Writer to dump functions to file

    :related: DocWalker

    """
    template = 'function.md'

    def get_signature(self):
        """
        **LLM Docstring**

        Obtains the inspectable call signature of the handled function.
        :return: the stringified signature
        :rtype: str
        """
        ...

    def get_template_params(self, **kwargs):
        """
        **LLM Docstring**

        Collects function metadata, parsed docstring fields, examples, tests, and source location for rendering.

        Object memory addresses in default-value representations are normalized to the text `instance`.

        :param kwargs: unused compatibility options
        :type kwargs: Any
        :return: the function template parameters
        :rtype: dict
        """
        ...

class MethodWriter(FunctionWriter):
    """
    Writes class methods to file
    (distinct from functions since not expected to exist solo)
    """
    template = 'method.md'

    def get_template_params(self, **kwargs):
        """
        **LLM Docstring**

        Collects method template parameters after unwrapping class, static, and property descriptors.

        The original descriptor is restored even if metadata extraction fails.

        :param kwargs: options forwarded to the function writer
        :type kwargs: Any
        :return: the method template parameters including decorator text
        :rtype: dict
        """
        ...

    def get_signature(self):
        """
        **LLM Docstring**

        Returns the handled method signature, falling back to `(self)` for non-inspectable properties.
        :return: the stringified method signature
        :rtype: str
        """
        ...

    @property
    def identifier(self):
        """
        **LLM Docstring**

        Resolves the method identifier, constructing property identifiers from their parent class.
        :return: the fully qualified method identifier
        :rtype: str
        """
        ...

class ObjectWriter(DocObjectTemplateHandler):
    """
    Writes general objects to file.
    Basically a fallback to support singletons and things
    of that nature.

    :related: DocWalker

    """
    template = 'object.md'

    @property
    def identifier(self):
        """
        **LLM Docstring**

        Builds a fallback identifier for a general object and drops the enclosing class component.
        :return: the normalized object identifier
        :rtype: str
        """
        ...

    def check_should_write(self):
        """
        Determines whether the object really actually should be
        documented (quite permissive)
        :return:
        :rtype:
        """
        ...

    def get_template_params(self):
        """
        **LLM Docstring**

        Collects fallback object metadata from its docstring, type, examples, and source line.

        Objects without `__doc__` are described as instances of their concrete type.
        :return: the object template parameters
        :rtype: dict
        """
        ...

class IndexWriter(DocTemplateHandler):
    """
    Writes an index file with all of the
    written documentation files.
    Needs some work to provide more useful info by default.

    :related: DocWalker

    """
    template = 'index.md'

    def __init__(self, *args, description=None, **kwargs):
        """
        **LLM Docstring**

        Initializes an index writer with a default documentation heading when no description is supplied.

        :param args: positional handler arguments
        :type args: Any

        :param description: the index description or heading
        :type description: str | None

        :param kwargs: additional handler options
        :type kwargs: Any
        """
        ...

    def get_identifier(cls, o):
        """
        **LLM Docstring**

        Returns the fixed identifier used for documentation indexes.

        :param o: unused indexed object
        :type o: Any
        :return: `"index"`
        :rtype: str
        """
        ...

    def get_file_paths(self):
        """
        **LLM Docstring**

        Normalizes written file paths relative to the configured documentation root.
        :return: normalized string paths and unchanged non-string entries
        :rtype: list
        """
        ...

    def get_index_files(self):
        """
        **LLM Docstring**

        Converts string paths into `[stem, path]` index entries.
        :return: the index entry list
        :rtype: list
        """
        ...

    def get_template_params(self):
        """
        **LLM Docstring**

        Parses the index description and assembles index entries and examples for rendering.
        :return: the index template parameters
        :rtype: dict
        """
        ...

class DocWalker(TemplateWalker):
    """
    A class that walks a module structure, generating `.md` files for every class inside it as well as for global functions,
    and a Markdown index file.

    Takes a set of objects & writers and walks through the objects, generating files on the way.

    :details: A `DocWalker` object is a light subclass of a `TemplateWalker`, but specialized for documentation & with specialized handlers
    :related: .DocsBuilder.DocBuilder, ModuleWriter, ClassWriter, FunctionWriter, MethodWriter, ObjectWriter, IndexWriter
    """
    module_handler = ModuleWriter
    class_handler = ClassWriter
    function_handler = FunctionWriter
    method_handler = MethodWriter
    object_handler = ObjectWriter
    index_handler = IndexWriter
    spec = DocSpec

    def __init__(self, out=None, engine=None, verbose=True, template_locator=None, examples_directory=None, tests_directory=None, **extra_fields):
        """
        :param objects: the objects to write out
        :type objects: Iterable[Any]
        :param out: the directory in which to write the files (`None` means `sys.stdout`)
        :type out: None | str
        :param ignore_paths: a set of paths not to write (passed to the objects)
        :type ignore_paths: None | Iterable[str]
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Formats the walker with its active template engine.
        :return: the diagnostic representation
        :rtype: str
        """
        ...

    def get_engine(self, locator):
        """
        **LLM Docstring**

        Resolves the configured template engine.

        Non-engine locators are wrapped in a Markdown `TemplateEngine` using `*.md` templates.

        :param locator: an existing engine, template locator, or `None` for the interactive engine
        :type locator: TemplateEngine | Any | None
        :return: the active engine
        :rtype: TemplateEngine
        """
        ...

    def get_examples_loader(self, examples_directory):
        """
        **LLM Docstring**

        Normalizes an examples directory into an `ExamplesExtractor`.

        :param examples_directory: the loader or resource root
        :type examples_directory: ExamplesExtractor | str | None
        :return: the normalized loader, or `None`
        :rtype: ExamplesExtractor | None
        """
        ...

    def get_tests_loader(self, tests_directory):
        """
        **LLM Docstring**

        Normalizes a tests directory into a `TestsExtractor`.

        :param tests_directory: the loader or resource root
        :type tests_directory: TestsExtractor | str | None
        :return: the normalized loader, or `None`
        :rtype: TestsExtractor | None
        """
        ...

    def get_handler(self, *args, examples_loader=None, tests_loader=None, **kwargs):
        """
        **LLM Docstring**

        Creates a handler while injecting the walker's default examples and tests loaders.

        :param args: positional arguments forwarded to the base walker
        :type args: Any

        :param examples_loader: an optional per-handler examples-loader override
        :type examples_loader: ExamplesExtractor | None

        :param tests_loader: an optional per-handler tests-loader override
        :type tests_loader: TestsExtractor | None

        :param kwargs: additional handler options
        :type kwargs: Any
        :return: the selected template handler
        :rtype: TemplateHandler
        """
        ...

    def visit_root(self, o, tests_directory=None, examples_directory=None, verbose=None, **kwargs):
        """
        **LLM Docstring**

        Visits one root specification while temporarily applying root-specific test and example directories.

        The previous loaders are restored in a `finally` block.

        :param o: the root object or mapping specification
        :type o: Any

        :param tests_directory: an optional tests-loader root
        :type tests_directory: Any | None

        :param examples_directory: an optional examples-loader root
        :type examples_directory: Any | None

        :param verbose: whether to print progress; defaults to the walker setting
        :type verbose: bool | None

        :param kwargs: options forwarded to the base root visitor
        :type kwargs: Any
        :return: the documentation produced by the base walker
        :rtype: Any
        """
        ...

    @mixedmethod
    def _ipython_pinfo_(cls):
        """
        **LLM Docstring**

        Displays documentation for the class or instance through `jdoc` when IPython requests rich object information.
        :return: the Jupyter documentation component
        :rtype: Any
        """
        ...

def jdoc(obj, max_depth=1, engine=None, verbose=False, **etc):
    """
    provides documentation in a Jupyter-friendly environment

    :param obj: the object to extract documentation for
    :type obj: Any
    :param max_depth: the depth in the object tree to go down to (default: `1`)
    :type max_depth: int
    :return docs:
    :rtype docs: ..Jupyter.Component

    :details:
    Makes use of the `JHTML` system to nicely format documentation as well as the
    documentation utilities found in `McUtils.Docs` (which were orginally written
    as part of the `Peeves` package).

    Asking for too many pieces of documentation at once can really slow things down,
    so by default the object tree is traversed only shallowly.
    In principle, the documentation could be directly exported to an HTML document as
    no `Widget`-necessary bits are used (at least as on when I write this) but a better
    choice is to generate Markdown docs using the standard `DocsBuilder` approach.
    This provides flexibility and can be ingested into any number of Markdown->HTML systems.

    :examples:
    Get documentation for `jdoc`

    ```python
    jdoc(jdoc)
    ```

    Get documentation for an entire module

    ```python
    import McUtils.Docs as MDoc
    jdoc(Mdoc)
    ```

    """
    ...
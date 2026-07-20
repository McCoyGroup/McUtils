import sys, os, pathlib, abc, enum, types, string, inspect
import ast, functools, re, fnmatch, collections
import typing, itertools, builtins
from typing import *
from ... import Devutils as dev
from .ObjectWalker import *
__reload_hook__ = ['.ObjectWalker']
__all__ = ['TemplateFormatter', 'FormatDirective', 'TemplateFormatDirective', 'TemplateOps', 'TemplateEngine', 'ResourceLocator', 'TemplateResourceExtractor', 'TemplateWalker', 'TemplateHandler', 'ModuleTemplateHandler', 'ClassTemplateHandler', 'FunctionTemplateHandler', 'MethodTemplateHandler', 'ObjectTemplateHandler', 'IndexTemplateHandler', 'TemplateInterfaceEngine', 'TemplateInterfaceFormatter']

class TemplateOps:

    @staticmethod
    def loop(caller: typing.Callable, *args, joiner='', formatter=None, **kwargs):
        """
        **LLM Docstring**

        Call a template operation over synchronized positional and keyword iterables and optionally join the results.

        :param caller: the callable applied to each synchronized argument group
        :type caller: typing.Callable
        :param joiner: the string used to combine generated values, or `None` to keep a list
        :type joiner: Any
        :param formatter: the active template formatter
        :type formatter: Any
        :param args: positional arguments forwarded to the wrapped callable
        :type args: Any
        :param kwargs: keyword arguments forwarded to the wrapped callable
        :type kwargs: Any

        :return: A joined string when `joiner` is not `None`; otherwise the list of callback results.
        :rtype: Any
        """
        ...

    @classmethod
    def loop_template(cls, template: str, *args, joiner='', formatter=None, **kwargs):
        """
        **LLM Docstring**

        Format a string template over synchronized iterables using `loop`.

        :param template: the template name, template text, or template callable
        :type template: str
        :param joiner: the string used to combine generated values, or `None` to keep a list
        :type joiner: Any
        :param formatter: the active template formatter
        :type formatter: Any
        :param args: positional arguments forwarded to the wrapped callable
        :type args: Any
        :param kwargs: keyword arguments forwarded to the wrapped callable
        :type kwargs: Any

        :return: The rendered iterations joined by `joiner`, or the list of rendered values when `joiner` is `None`.
        :rtype: Any
        """
        ...

    @staticmethod
    def join(*args, joiner=' ', formatter=None):
        """
        **LLM Docstring**

        Join a sequence of strings, accepting either separate values or one non-string iterable.

        :param joiner: the string used to combine generated values, or `None` to keep a list
        :type joiner: Any
        :param formatter: the active template formatter
        :type formatter: Any
        :param args: positional arguments forwarded to the wrapped callable
        :type args: Any

        :return: The input strings combined with `joiner`.
        :rtype: Any
        """
        ...

    @classmethod
    def load(cls, template, formatter=None):
        """
        **LLM Docstring**

        Load a named template through the active formatter.

        :param template: the template name, template text, or template callable
        :type template: Any
        :param formatter: the active template formatter
        :type formatter: Any

        :return: The template content returned by the formatter.
        :rtype: Any
        """
        ...

    @classmethod
    def include(cls, template, formatter=None):
        """
        **LLM Docstring**

        Load and immediately render another template using the current format parameters.

        :param template: the template name, template text, or template callable
        :type template: Any
        :param formatter: the active template formatter
        :type formatter: Any

        :return: The included template rendered with the current parameter scope.
        :rtype: Any
        """
        ...

    @classmethod
    def apply(cls, template, *args, formatter=None, **kwargs):
        """
        **LLM Docstring**

        Render a template with explicit arguments through the active formatter.

        :param template: the template name, template text, or template callable
        :type template: Any
        :param formatter: the active template formatter
        :type formatter: Any
        :param args: positional arguments forwarded to the wrapped callable
        :type args: Any
        :param kwargs: keyword arguments forwarded to the wrapped callable
        :type kwargs: Any

        :return: The rendered template string.
        :rtype: Any
        """
        ...

    @classmethod
    def nonempty(cls, data, formatter=None):
        """
        **LLM Docstring**

        Test whether a value is non-`None` and has positive length.

        :param data: the value or collection being tested
        :type data: Any
        :param formatter: the active template formatter
        :type formatter: Any

        :return: `True` when `data` is non-`None` and nonempty; otherwise `False`.
        :rtype: Any
        """
        ...

    @classmethod
    def wrap(cls, fn):
        """
        **LLM Docstring**

        Adapt a callable so it accepts and ignores the formatter keyword injected into directives.

        :param fn: the callable to wrap
        :type fn: Any

        :return: A wrapper callable that ignores the injected formatter keyword.
        :rtype: Any
        """
        ...

    @staticmethod
    def cleandoc(txt, formatter=None):
        """
        **LLM Docstring**

        Normalize indentation and surrounding whitespace in documentation text.

        :param txt: the text to normalize
        :type txt: Any
        :param formatter: the active template formatter
        :type formatter: Any

        :return: The cleaned documentation text.
        :rtype: Any
        """
        ...

    @staticmethod
    def wrap_str(obj, formatter=None):
        """
        **LLM Docstring**

        Convert an object to an escaped string literal, using triple quotes for multiline text.

        :param obj: the object to inspect or dispatch
        :type obj: Any
        :param formatter: the active template formatter
        :type formatter: Any

        :return: An escaped single-line or triple-quoted string representation.
        :rtype: Any
        """
        ...

    @staticmethod
    def optional(key, default='', formatter=None):
        """
        **LLM Docstring**

        Retrieve an optional formatting parameter with a fallback value.

        :param key: the lookup, assignment, or formatting key
        :type key: Any
        :param default: fallback callable or value used when no match is found
        :type default: Any
        :param formatter: the active template formatter
        :type formatter: Any

        :return: The current parameter value for `key`, or `default` when it is absent.
        :rtype: Any
        """
        ...

class FormatDirective(enum.Enum):
    """
    Base class for directives -- shouldn't be an enum really...
    """

    def __init__(self, name, callback=None):
        """
        **LLM Docstring**

        Initialize an enum directive with its template key and normalized callback.

        :param name: an explicit display name
        :type name: Any
        :param callback: the function receiving each generated comprehension result
        :type callback: Any

        :return: `None`.
        :rtype: None
        """
        ...

    def _call(self, *data, **kwargs):
        """
        **LLM Docstring**

        Invoke the callback associated with this directive.

        :param data: the value or collection being tested
        :type data: Any
        :param kwargs: keyword arguments forwarded to the wrapped callable
        :type kwargs: Any

        :return: The callback result for this directive.
        :rtype: Any
        """
        ...

    @classmethod
    def _keymap(cls):
        """
        **LLM Docstring**

        Return the lazily initialized directive-key cache for the enumeration.

        :return: The cached directive-key mapping, or `None` before initialization.
        :rtype: Any
        """
        ...

    @classmethod
    def _load(cls, name: str):
        """
        **LLM Docstring**

        Resolve a directive member by its external template key.

        :param name: an explicit display name
        :type name: str

        :return: The directive member registered under `name`.
        :rtype: Any
        """
        ...

    @classmethod
    def extend(cls, *others):
        """
        **LLM Docstring**

        Create a new directive enumeration containing members from this class and additional enumerations.

        :param others: additional directive enumerations to merge
        :type others: Any

        :return: A new `FormatDirective` enumeration containing the merged members.
        :rtype: Any
        """
        ...

class TemplateFormatDirective(FormatDirective):
    Loop = ('loop', TemplateOps.loop)
    LoopTemplate = ('loop_template', TemplateOps.loop_template)
    Join = ('join', TemplateOps.join)
    Load = ('load', TemplateOps.load)
    Include = ('include', TemplateOps.include)
    Apply = ('apply', TemplateOps.apply)
    NonEmpty = ('nonempty', TemplateOps.nonempty)
    CleanDoc = ('cleandoc', TemplateOps.cleandoc)
    Optional = ('optional', TemplateOps.optional)
    Str = ('str', TemplateOps.wrap_str)
    Int = ('int', TemplateOps.wrap(int))
    Float = ('float', TemplateOps.wrap(float))
    Round = ('round', TemplateOps.wrap(round))
    Len = ('len', TemplateOps.wrap(len))
    Dict = ('dict', TemplateOps.wrap(dict))
    List = ('list', TemplateOps.wrap(list))
    Tuple = ('tuple', TemplateOps.wrap(tuple))
    Set = ('set', TemplateOps.wrap(set))

class TemplateFormatterError(ValueError):
    ...

class TemplateASTEvaluator:

    def __init__(self, formatter, directives, format_parameters: dict):
        """
        **LLM Docstring**

        Store the formatter, directive set, and mutable variable mapping used for AST evaluation.

        :param formatter: the active template formatter
        :type formatter: Any
        :param directives: the directive enumeration available to expressions
        :type directives: Any
        :param format_parameters: the mutable mapping of template variables
        :type format_parameters: dict

        :return: `None`.
        :rtype: None
        """
        ...

    def handle_comprehension(self, g, expr, callback):
        """
        **LLM Docstring**

        Evaluate one comprehension generator while temporarily binding its target variable.

        :param g: the comprehension generator node
        :type g: Any
        :param expr: the expression evaluated for each accepted item
        :type expr: Any
        :param callback: the function receiving each generated comprehension result
        :type callback: Any

        :return: `None`; accepted values are delivered through `callback`.
        :rtype: Any
        """
        ...

    def evaluate_node(self, node: typing.Union[ast.AST, ast.expr, tuple]):
        """
        **LLM Docstring**

        Recursively interpret the supported subset of Python AST nodes used by template expressions.

        :param node: the AST node or node tuple to evaluate
        :type node: typing.Union[ast.AST, ast.expr, tuple]

        :return: The Python value produced by interpreting the supported AST node.
        :rtype: Any
        """
        ...

class TemplateFormatter(string.Formatter):
    """
    Provides a formatter for fields that allows for
    the inclusion of standard Bootstrap HTML elements
    alongside the classic formatting
    """
    max_recusion = 6
    directives = TemplateFormatDirective

    class frozendict(dict):

        def __setitem__(self, key, value):
            """
            **LLM Docstring**

            Reject mutation attempts on the template mapping.

            :param key: the lookup, assignment, or formatting key
            :type key: Any
            :param value: the value associated with the key
            :type value: Any

            :return: `None`.
            :rtype: None
            """
            ...

    def __init__(self, templates):
        """
        **LLM Docstring**

        Store an immutable template mapping and initialize the stack of active formatting scopes.

        :param templates: the mapping of template identifiers to resources
        :type templates: Any

        :return: `None`.
        :rtype: None
        """
        ...

    @property
    def format_parameters(self):
        """
        **LLM Docstring**

        Return the parameter mapping for the innermost active formatting operation.

        :return: The innermost parameter mapping, or `None` outside formatting.
        :rtype: dict | None
        """
        ...

    @property
    def templates(self):
        """
        **LLM Docstring**

        Expose the immutable template-resource mapping.

        :return: The immutable template mapping.
        :rtype: Mapping
        """
        ...

    @property
    def special_callbacks(self):
        """
        **LLM Docstring**

        Map special format-field markers to evaluation, directive, comment, raw, and assignment handlers.

        :return: A mapping from special field markers to their handler methods.
        :rtype: dict
        """
        ...

    @property
    def callback_map(self):
        """
        **LLM Docstring**

        Combine special markers with every registered directive marker.

        :return: The complete mapping from special and directive markers to handlers.
        :rtype: dict
        """
        ...

    def apply_eval_tree(self, _, spec) -> str:
        """
        **LLM Docstring**

        Parse and evaluate a cleaned Python expression or statement block against the active parameters.

        :param _: an unused callback key
        :type _: Any
        :param spec: the object specification or template expression
        :type spec: Any

        :return: The evaluated expression result, with `None` converted to an empty string.
        :rtype: str
        """
        ...

    def apply_directive_tree(self, _, spec) -> str:
        """
        **LLM Docstring**

        Evaluate a directive expression after wrapping it in parentheses.

        :param _: an unused callback key
        :type _: Any
        :param spec: the object specification or template expression
        :type spec: Any

        :return: The evaluated directive-expression result.
        :rtype: str
        """
        ...

    def apply_assignment(self, key, spec) -> str:
        """
        **LLM Docstring**

        Assign the literal right-hand text from an inline assignment into the active parameter mapping.

        :param key: the lookup, assignment, or formatting key
        :type key: Any
        :param spec: the object specification or template expression
        :type spec: Any

        :return: An empty string after updating the active parameter mapping.
        :rtype: str
        """
        ...

    def apply_raw(self, key, spec) -> str:
        """
        **LLM Docstring**

        Return a format specification unchanged.

        :param key: the lookup, assignment, or formatting key
        :type key: Any
        :param spec: the object specification or template expression
        :type spec: Any

        :return: The unmodified format specification.
        :rtype: str
        """
        ...

    def apply_comment(self, key, spec) -> str:
        """
        **LLM Docstring**

        Discard a template comment field.

        :param key: the lookup, assignment, or formatting key
        :type key: Any
        :param spec: the object specification or template expression
        :type spec: Any

        :return: An empty string, removing the comment from output.
        :rtype: str
        """
        ...

    def apply_directive(self, key, spec) -> str:
        """
        **LLM Docstring**

        Convert a directive marker and argument text into an evaluable directive call.

        :param key: the lookup, assignment, or formatting key
        :type key: Any
        :param spec: the object specification or template expression
        :type spec: Any

        :return: The evaluated result of the named directive call.
        :rtype: str
        """
        ...

    def format_field(self, value: Any, format_spec: str) -> str:
        """
        **LLM Docstring**

        Route special string-valued fields through callback handlers and otherwise use standard formatting.

        :param value: the value associated with the key
        :type value: Any
        :param format_spec: the format specification associated with the field
        :type format_spec: str

        :return: The special-callback result or the standard formatted field text.
        :rtype: str
        """
        ...
    _template_cache = {}

    def load_template(self, template):
        """
        **LLM Docstring**

        Resolve a registered template and read file-backed content with caching.

        :param template: the template name, template text, or template callable
        :type template: Any

        :return: The registered template text, read from disk when the resource is a file path.
        :rtype: Any
        """
        ...

    def vformat(self, format_string: str, args: Sequence[Any], kwargs: Mapping[str, Any]):
        """
        **LLM Docstring**

        Render a template within a temporary parameter scope populated with special callback markers.

        :param format_string: the template string being formatted
        :type format_string: str
        :param args: positional arguments forwarded to the wrapped callable
        :type args: Sequence[Any]
        :param kwargs: keyword arguments forwarded to the wrapped callable
        :type kwargs: Mapping[str, Any]

        :return: The fully rendered template string.
        :rtype: Any
        """
        ...

class OrderedSet(dict):

    def __init__(self, *iterable):
        """
        **LLM Docstring**

        Initialize insertion-ordered unique keys from an optional iterable.

        :param iterable: the iterable used to initialize the ordered set
        :type iterable: Any

        :return: `None`.
        :rtype: None
        """
        ...

    def union(self, other: 'OrderedSet'):
        """
        **LLM Docstring**

        Return a new ordered set containing this set followed by unseen keys from another set.

        :param other: another ordered set
        :type other: 'OrderedSet'

        :return: A new ordered set containing keys from both operands without duplicates.
        :rtype: Any
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a constructor-style representation containing the ordered keys.

        :return: A constructor-style string showing the ordered keys.
        :rtype: Any
        """
        ...

    def __iter__(self):
        """
        **LLM Docstring**

        Iterate over keys in insertion order.

        :return: An iterator over keys in insertion order.
        :rtype: Any
        """
        ...

    def add(self, k):
        """
        **LLM Docstring**

        Add a key while preserving insertion order and uniqueness.

        :param k: a dispatch key or parameter name
        :type k: Any

        :return: `None`.
        :rtype: None
        """
        ...

    def update(self, ks):
        """
        **LLM Docstring**

        Add every key from an iterable.

        :param ks: keys to add
        :type ks: Any

        :return: `None`.
        :rtype: None
        """
        ...

    def __delitem__(self, k):
        """
        **LLM Docstring**

        Delete a key from the ordered set.

        :param k: a dispatch key or parameter name
        :type k: Any

        :return: `None`.
        :rtype: None
        """
        ...

class Locator(typing.Protocol):

    def locate(self, identifier):
        """
        **LLM Docstring**

        Define the protocol operation that resolves a resource identifier.

        :param identifier: the resource or Python object identifier
        :type identifier: Any

        :return: The resolved resource for `identifier`.
        :rtype: Any
        """
        ...

    def paths(self, **opts) -> 'Iterable':
        """
        **LLM Docstring**

        Define the protocol operation that enumerates available resource identifiers.

        :param opts: additional protocol-specific path enumeration options
        :type opts: Any

        :return: An iterable of available resource identifiers.
        :rtype: 'Iterable'
        """
        ...

class ResourcePathLocator(Locator):

    def __init__(self, path: Iterable[str]):
        """
        **LLM Docstring**

        Normalize one or more filesystem search roots into a list.

        :param path: one or more resource search roots
        :type path: Iterable[str]

        :return: `None`.
        :rtype: None
        """
        ...

    def locate(self, identifier):
        """
        **LLM Docstring**

        Resolve an existing absolute or relative identifier, searching configured roots in order.

        :param identifier: the resource or Python object identifier
        :type identifier: Any

        :return: The first existing path matching `identifier`, or `None` when no resource exists.
        :rtype: Any
        """
        ...

    def resource_path(self, d, f):
        """
        **LLM Docstring**

        Join a search root with a resource-relative path.

        :param d: a resource root directory
        :type d: Any
        :param f: a resource-relative file name
        :type f: Any

        :return: The filesystem path formed from the root and relative resource name.
        :rtype: Any
        """
        ...

    def paths(self, max_depth=7, **_):
        """
        **LLM Docstring**

        Walk search roots and collect resource-relative file paths up to a maximum depth.

        :param max_depth: the maximum traversal depth, with negative values meaning unlimited
        :type max_depth: Any
        :param _: an unused callback key
        :type _: Any

        :return: An ordered set of resource-relative file paths.
        :rtype: Iterable[str]
        """
        ...

    def directories(self):
        """
        **LLM Docstring**

        Return the concrete root directories searched by this locator.

        :return: The concrete directories searched by this locator.
        :rtype: Iterable[str]
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a constructor-style representation of the configured search paths.

        :return: A constructor-style string containing the configured roots.
        :rtype: Any
        """
        ...

class SubresourcePathLocator(ResourcePathLocator):

    def __init__(self, roots, extension):
        """
        **LLM Docstring**

        Initialize a path locator that inserts a fixed subresource directory below each root.

        :param roots: the base search roots
        :type roots: Any
        :param extension: the subdirectory extension appended below each root
        :type extension: Any

        :return: `None`.
        :rtype: None
        """
        ...

    def resource_path(self, d, f):
        """
        **LLM Docstring**

        Join a root, fixed subresource directory, and resource-relative path.

        :param d: a resource root directory
        :type d: Any
        :param f: a resource-relative file name
        :type f: Any

        :return: The path formed from the root, fixed subresource directory, and resource name.
        :rtype: Any
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a constructor-style representation of roots and subresource extension.

        :return: A constructor-style string containing roots and the subresource extension.
        :rtype: Any
        """
        ...

class ResourceLocator(Locator):

    def __init__(self, locators: Iterable[Union[ResourcePathLocator, Iterable[str], Tuple[Iterable[str], Union[str, Iterable[str]]]]]):
        """
        **LLM Docstring**

        Normalize heterogeneous locator specifications into a flat sequence of path locators.

        :param locators: resource locator definitions to combine
        :type locators: Iterable[Union[ResourcePathLocator, Iterable[str], Tuple[Iterable[str], Union[str, Iterable[str]]]]]

        :return: `None`.
        :rtype: None
        """
        ...

    def locate(self, identifier):
        """
        **LLM Docstring**

        Return the first resource path resolved by the configured locators.

        :param identifier: the resource or Python object identifier
        :type identifier: Any

        :return: The first resource resolved by any component locator, or `None`.
        :rtype: Any
        """
        ...

    def paths(self, filter_pattern=None, **_):
        """
        **LLM Docstring**

        Combine resource paths from all locators and optionally filter them by regex or glob.

        :param filter_pattern: a regular expression or glob used to filter resource paths
        :type filter_pattern: Any
        :param _: an unused callback key
        :type _: Any

        :return: The combined resource identifiers, optionally filtered by the supplied pattern.
        :rtype: Iterable[str]
        """
        ...

    def directories(self):
        """
        **LLM Docstring**

        Return unique search directories from all component locators in encounter order.

        :return: The unique component search directories in encounter order.
        :rtype: Iterable[str]
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation based on the combined search directories.

        :return: A constructor-style string containing the combined directories.
        :rtype: Any
        """
        ...

class TemplateEngine:
    """
    Provides an engine for generating content using a
    `TemplateFormatter` and `ResourceLocator`
    """
    formatter_class = TemplateFormatter

    def __init__(self, locator: Locator, template_pattern='*.*', ignore_missing=False, formatter_class=None, ignore_paths=()):
        """
        **LLM Docstring**

        Discover matching template resources, construct the formatter, and store output-control options.

        :param locator: the resource locator supplying templates
        :type locator: Locator
        :param template_pattern: the pattern selecting template resources
        :type template_pattern: Any
        :param ignore_missing: whether missing format fields should resolve through a default mapping
        :type ignore_missing: Any
        :param formatter_class: the formatter implementation to instantiate
        :type formatter_class: Any
        :param ignore_paths: target paths that should not be written
        :type ignore_paths: Any

        :return: `None`.
        :rtype: None
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return an elided representation containing the locator.

        :return: An elided constructor-style string identifying the locator.
        :rtype: Any
        """
        ...

    def format_map(self, template, parameters):
        """
        **LLM Docstring**

        Resolve a template identifier when registered and render it with a parameter mapping.

        :param template: the template name, template text, or template callable
        :type template: Any
        :param parameters: the values exposed while formatting
        :type parameters: Any

        :return: The rendered template text.
        :rtype: Any
        """
        ...

    def format(self, template, **parameters):
        """
        **LLM Docstring**

        Render a template using keyword parameters.

        :param template: the template name, template text, or template callable
        :type template: Any
        :param parameters: the values exposed while formatting
        :type parameters: Any

        :return: The rendered template text.
        :rtype: Any
        """
        ...

    class outStream:

        def __init__(self, file, mode='w+', **kw):
            """
            **LLM Docstring**

            Store a destination and deferred file-opening options for the output context.

            :param file: a path or writable stream
            :type file: Any
            :param mode: the mode used when opening a path
            :type mode: Any
            :param kw: additional arguments passed to `open`
            :type kw: Any

            :return: `None`.
            :rtype: None
            """
            ...

        def __enter__(self):
            """
            **LLM Docstring**

            Open a path on first entry, creating its parent directory when possible, or reuse a supplied stream.

            :return: The opened file handle or supplied writable stream.
            :rtype: Any
            """
            ...

        def __exit__(self, exc_type, exc_val, exc_tb):
            """
            **LLM Docstring**

            Close path-backed output and clear the cached handle.

            :param exc_type: the exception class raised inside the context, if any
            :type exc_type: Any
            :param exc_val: the exception instance raised inside the context, if any
            :type exc_val: Any
            :param exc_tb: the traceback associated with the exception, if any
            :type exc_tb: Any

            :return: `None`.
            :rtype: None
            """
            ...

        def write(self, s):
            """
            **LLM Docstring**

            Open the output context, write one string, and return the original destination.

            :param s: the string written to the output stream
            :type s: Any

            :return: The original destination path or stream after writing.
            :rtype: Any
            """
            ...

    def write_string(self, target, txt):
        """
        **LLM Docstring**

        Write rendered text to a target through `outStream`.

        :param target: the destination path, stream, or key
        :type target: Any
        :param txt: the text to normalize
        :type txt: Any

        :return: The destination returned by `outStream.write`.
        :rtype: Any
        """
        ...

    def apply(self, template, target, **template_params):
        """
        **LLM Docstring**

        Render a template and either return the string or write it unless the target is ignored.

        :param template: the template name, template text, or template callable
        :type template: Any
        :param target: the destination path, stream, or key
        :type target: Any
        :param template_params: values supplied to the template
        :type template_params: Any

        :return: The rendered text when `target` is `None`, the written target otherwise, or `None` for ignored paths.
        :rtype: Any
        """
        ...

class TemplateHandler(ObjectHandler):
    template = None
    extension = '.md'
    squash_repeat_packages = True

    def __init__(self, obj, *, out=None, engine: TemplateEngine=None, root=None, squash_repeat_packages=True, is_package_root=False, **extra_fields):
        """
        **LLM Docstring**

        Initialize object-handling state, resolve the output target, and choose an object-specific or default template.

        :param obj: the object to inspect or dispatch
        :type obj: Any
        :param out: the output root, file, or stream
        :type out: Any
        :param engine: the template engine used to render content
        :type engine: TemplateEngine
        :param root: the output root used to compute relative URLs
        :type root: Any
        :param squash_repeat_packages: whether repeated package components are collapsed
        :type squash_repeat_packages: Any
        :param is_package_root: whether the documented object represents a package root
        :type is_package_root: Any
        :param extra_fields: additional fields exposed to handlers and templates
        :type extra_fields: Any

        :return: `None`.
        :rtype: None
        """
        ...

    def template_params(self, **kwargs):
        """
        **LLM Docstring**

        Merge handler extra fields with parameters computed for the current object.

        :param kwargs: keyword arguments forwarded to the wrapped callable
        :type kwargs: Any

        :return: The merged mapping of extra fields and object-specific template parameters.
        :rtype: Any
        """
        ...

    @abc.abstractmethod
    def get_template_params(self, **kwargs):
        """
        Returns the parameters that should be inserted into the template

        :return:
        :rtype: dict
        """
        ...

    @property
    def package_path(self):
        """
        **LLM Docstring**

        Return the package name and source URL tuple for the handled object.

        :return: A `(package_name, source_url)` tuple.
        :rtype: Any
        """
        ...

    def get_package_and_url(self, include_url_base=True):
        """
        Returns package name and corresponding URL for the object
        being documented
        :return:
        :rtype:
        """
        ...

    @property
    def target_identifier(self):
        """
        **LLM Docstring**

        Return the normalized dotted identifier used for the output target.

        :return: The normalized dotted target identifier.
        :rtype: Any
        """
        ...

    @classmethod
    def squash_reps(cls, ident):
        """
        **LLM Docstring**

        Collapse the leading repeated package components in a dotted identifier.

        :param ident: the dotted identifier to normalize
        :type ident: Any

        :return: The dotted identifier with leading repeated package components removed.
        :rtype: Any
        """
        ...

    def get_target_extension(self, identifier=None):
        """
        **LLM Docstring**

        Split an object identifier into normalized path components for output and resource lookup.

        :param identifier: the resource or Python object identifier
        :type identifier: Any

        :return: The normalized identifier components used as a resource or output path.
        :rtype: Any
        """
        ...

    def get_output_file(self, out):
        """
        Returns package name and corresponding URL for the object
        being documented
        :return:
        :rtype:
        """
        ...

    def handle(self, template=None, target=None, write=True):
        """
        Formats the documentation Markdown from the supplied template

        :param template:
        :type template:
        :return:
        :rtype:
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

class TemplateResourceExtractor(ResourceLocator):
    extension = '.md'

    def path_extension(self, handler: TemplateHandler):
        """
        Provides the default examples path for the object
        :return:
        :rtype:
        """
        ...
    resource_keys = []
    resource_attrs = []

    def get_resource(self, handler: TemplateHandler, keys=None, attrs=None):
        """
        **LLM Docstring**

        Locate a resource using configured handler fields, object attributes, or the default derived path.

        :param handler: the handler whose resource should be located
        :type handler: TemplateHandler
        :param keys: handler fields checked for an explicit resource
        :type keys: Any
        :param attrs: object attributes checked for an explicit resource
        :type attrs: Any

        :return: The resolved resource identifier or path, or `None` when none can be found.
        :rtype: Any
        """
        ...

    def load(self, handler: TemplateHandler):
        """
        Loads examples for the stored object if provided
        :return:
        :rtype:
        """
        ...

class ModuleTemplateHandler(TemplateHandler):
    template = 'module.md'

class ClassTemplateHandler(TemplateHandler):
    template = 'class.md'

class FunctionTemplateHandler(TemplateHandler):
    template = 'function.md'

class MethodTemplateHandler(TemplateHandler):
    template = 'method.md'

class ObjectTemplateHandler(TemplateHandler):
    template = 'object.md'

class IndexTemplateHandler(TemplateHandler):
    template = 'index.md'

class TemplateWalker(ObjectWalker):
    module_handler = ModuleTemplateHandler
    class_handler = ClassTemplateHandler
    function_handler = FunctionTemplateHandler
    method_handler = MethodTemplateHandler
    object_handler = ObjectTemplateHandler
    index_handler = IndexTemplateHandler

    def __init__(self, engine: TemplateEngine, out=None, description=None, **extra_fields):
        """
        **LLM Docstring**

        Store template-engine output settings and initialize the underlying object walker.

        :param engine: the template engine used to render content
        :type engine: TemplateEngine
        :param out: the output root, file, or stream
        :type out: Any
        :param description: the description passed to the generated index
        :type description: Any
        :param extra_fields: additional fields exposed to handlers and templates
        :type extra_fields: Any

        :return: `None`.
        :rtype: None
        """
        ...

    @property
    def default_handlers(self):
        """
        **LLM Docstring**

        Build the ordered mapping from modules, classes, functions, and fallback objects to handler classes.

        :return: The ordered mapping from dispatch tests to handler classes.
        :rtype: Any
        """
        ...

    def get_handler(self, obj, *, out=None, engine=None, tree=None, **kwargs):
        """
        **LLM Docstring**

        Construct a handler while injecting this walker’s output directory and template engine.

        :param obj: the object to inspect or dispatch
        :type obj: Any
        :param out: the output root, file, or stream
        :type out: Any
        :param engine: the template engine used to render content
        :type engine: Any
        :param tree: the shared object-documentation tree
        :type tree: Any
        :param kwargs: keyword arguments forwarded to the wrapped callable
        :type kwargs: Any

        :return: The handler constructed with this walker’s engine and output settings.
        :rtype: Any
        """
        ...

    def visit_root(self, o, **kwargs):
        """
        **LLM Docstring**

        Visit a root object through the standard traversal implementation.

        :param o: the object or import path to resolve
        :type o: Any
        :param kwargs: keyword arguments forwarded to the wrapped callable
        :type kwargs: Any

        :return: The result returned by visiting the root object.
        :rtype: Any
        """
        ...

    def write(self, objects, max_depth=-1, index='index.md'):
        """
        Walks through the objects supplied and applies the appropriate templates
        :return: index of written files
        :rtype: str
        """
        ...

class TemplateResourceList(Locator):
    """
    Implements the `ResourceLocator` interface, but is backed by a `dict` of
    explicit resources rather than a set of paths.
    """

    def __init__(self, resource_dict: Mapping[str, Any]):
        """
        **LLM Docstring**

        Store an explicit identifier-to-resource mapping.

        :param resource_dict: the explicit resource mapping
        :type resource_dict: Mapping[str, Any]

        :return: `None`.
        :rtype: None
        """
        ...

    def paths(self, **_):
        """
        **LLM Docstring**

        Return the identifiers available in the explicit resource mapping.

        :param _: an unused callback key
        :type _: Any

        :return: A dynamic view of the stored resource identifiers.
        :rtype: Iterable[str]
        """
        ...

    def locate(self, identifier):
        """
        **LLM Docstring**

        Retrieve the resource associated with an identifier, returning `None` when absent.

        :param identifier: the resource or Python object identifier
        :type identifier: Any

        :return: The resource mapped to `identifier`, or `None` when absent.
        :rtype: Any
        """
        ...

class TemplateInterfaceList(TemplateResourceList):
    """
    A set of functions to be used to construct interfaces
    """

    def __init__(self, resource_dict: Mapping[str, Callable]):
        """
        **LLM Docstring**

        Initialize an explicit mapping of interface names to template callables.

        :param resource_dict: the explicit resource mapping
        :type resource_dict: Mapping[str, Callable]

        :return: `None`.
        :rtype: None
        """
        ...

class TemplateInterfaceFormatter:
    """
    Provides an interface that mimics a `TemplateFormatter`
    but does nothing more than route to a set of template functions
    """

    def __init__(self, templates):
        """
        **LLM Docstring**

        Store callable templates and initialize the active parameter-scope stack.

        :param templates: the mapping of template identifiers to resources
        :type templates: Any

        :return: `None`.
        :rtype: None
        """
        ...

    @property
    def format_parameters(self):
        """
        **LLM Docstring**

        Return the innermost active interface parameter mapping.

        :return: The active interface parameter mapping, or `None` outside invocation.
        :rtype: dict | None
        """
        ...

    @property
    def templates(self):
        """
        **LLM Docstring**

        Expose the callable-template mapping.

        :return: The stored mapping of interface template callables.
        :rtype: Mapping
        """
        ...

    @property
    def special_callbacks(self):
        """
        **LLM Docstring**

        Return the currently empty special-callback mapping for interface templates.

        :return: An empty mapping; interface templates do not define special field callbacks.
        :rtype: dict
        """
        ...

    def load_template(self, template):
        """
        **LLM Docstring**

        Retrieve a callable template by identifier.

        :param template: the template name, template text, or template callable
        :type template: Any

        :return: The callable registered under the template identifier.
        :rtype: Any
        """
        ...

    def vformat(self, template: Callable, args: Sequence[Any], kwargs: Mapping[str, Any]):
        """
        **LLM Docstring**

        Invoke a callable template inside a temporary formatting-parameter scope.

        :param template: the template name, template text, or template callable
        :type template: Callable
        :param args: positional arguments forwarded to the wrapped callable
        :type args: Sequence[Any]
        :param kwargs: keyword arguments forwarded to the wrapped callable
        :type kwargs: Mapping[str, Any]

        :return: The value returned by invoking the callable template.
        :rtype: Any
        """
        ...

class TemplateInterfaceEngine(TemplateEngine):
    """
    A variant on a template engine designed for more interactive use.
    In many ways, _not_ a template engine, but too useful to ignore while I
    find a more uniform abstraction.
    Generates _interfaces_ from a set of interface template functions
    rather than strings from template files.
    """
    formatter_class = TemplateInterfaceFormatter

    def __init__(self, templates: 'TemplateInterfaceList|dict', ignore_missing=False, formatter_class=None, ignore_paths=()):
        """
        **LLM Docstring**

        Normalize a dictionary of callables into an interface resource list and initialize the base engine.

        :param templates: the mapping of template identifiers to resources
        :type templates: 'TemplateInterfaceList|dict'
        :param ignore_missing: whether missing format fields should resolve through a default mapping
        :type ignore_missing: Any
        :param formatter_class: the formatter implementation to instantiate
        :type formatter_class: Any
        :param ignore_paths: target paths that should not be written
        :type ignore_paths: Any

        :return: `None`.
        :rtype: None
        """
        ...

    def format_map(self, template, parameters):
        """
        **LLM Docstring**

        Resolve and invoke a callable template with the supplied parameter mapping.

        :param template: the template name, template text, or template callable
        :type template: Any
        :param parameters: the values exposed while formatting
        :type parameters: Any

        :return: The value returned by the resolved interface template.
        :rtype: Any
        """
        ...

    def apply(self, template, target, **template_params):
        """
        **LLM Docstring**

        Return an interface result directly or map it to a non-ignored target key.

        :param template: the template name, template text, or template callable
        :type template: Any
        :param target: the destination path, stream, or key
        :type target: Any
        :param template_params: values supplied to the template
        :type template_params: Any

        :return: The direct interface value, a `{target: value}` mapping, or `None` for ignored targets.
        :rtype: Any
        """
        ...
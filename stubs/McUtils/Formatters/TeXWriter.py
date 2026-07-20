from __future__ import annotations
import abc, numpy as np, io, weakref
import collections
import os
import functools
import re
import shutil
import tempfile as tf
import itertools
from .. import Devutils as dev
from .. import Numputils as nput
from .. import Parsers
from .TableFormatters import TableFormatter
from ..Misc.Symbolics import Abstract
__all__ = ['TeX', 'TeXTranspiler']

class TeXWriter(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def format_tex(self, context=None):
        """
        **LLM Docstring**

        Abstract formatting hook that subclasses must implement to produce TeX source.

        :param context: active `TeXContextManager` or context name used while formatting
        :type context: object
        :return: `None`; the operation mutates state, writes output, or raises by design.
        :rtype: None
        """
        ...
    real_digits = 3

    @classmethod
    def dispatch_format(cls, b, context):
        """
        **LLM Docstring**

        Convert supported Python, NumPy, and `TeXWriter` values into TeX-ready text using type-directed dispatch.

        :param b: value to dispatch into TeX text
        :type b: object
        :param context: active `TeXContextManager` or context name used while formatting
        :type context: object
        :return: TeX-formatted text for the supplied value
        :rtype: str
        """
        ...

    def as_expr(self):
        """
        **LLM Docstring**

        Wrap this writer as a symbolic `TeXExpr` so arithmetic and comparison composition can be used.
        :return: new symbolic or wrapper object
        :rtype: object
        """
        ...

class TeXContextManager:
    default_contexts = weakref.WeakValueDictionary()

    @classmethod
    def resolve(cls, name='default'):
        """
        **LLM Docstring**

        Return the weakly cached named context manager, creating it when no live manager exists.

        :param name: registry, resource, or output name
        :type name: object
        :return: named context manager
        :rtype: TeXContextManager
        """
        ...

    def __init__(self):
        """
        **LLM Docstring**

        Initialize an empty stack of nested TeX formatting contexts.
        :return: `None`; the operation mutates state, writes output, or raises by design.
        :rtype: None
        """
        ...

    def subcontext(self, cls):
        """
        **LLM Docstring**

        Instantiate a context class bound to this manager.

        :param cls: class being configured
        :type cls: object
        :return: new context instance bound to this manager
        :rtype: TeXContext
        """
        ...

    def set_context(self, ctx):
        """
        **LLM Docstring**

        Push a context onto the active-context stack.

        :param ctx: context object to push
        :type ctx: object
        :return: the pushed context
        :rtype: TeXContext
        """
        ...

    def leave_context(self):
        """
        **LLM Docstring**

        Pop the most recently entered context.
        :return: `None`; the operation mutates state, writes output, or raises by design.
        :rtype: None
        """
        ...

    @property
    def context(self):
        """
        **LLM Docstring**

        Return the currently active context, or `None` when the stack is empty.
        :return: active context or `None`
        :rtype: TeXContext | None
        """
        ...

    @property
    def math_mode(self):
        """
        **LLM Docstring**

        Report whether the current context is a `MathContext`.
        :return: whether math mode is active
        :rtype: bool
        """
        ...

class TeXContext:

    def __init__(self, manager: TeXContextManager):
        """
        **LLM Docstring**

        Bind a context object to the manager whose stack it controls.

        :param manager: context manager that owns this context
        :type manager: TeXContextManager
        :return: `None`; the operation mutates state, writes output, or raises by design.
        :rtype: None
        """
        ...

    def __enter__(self):
        """
        **LLM Docstring**

        Push this context and return it for use in a `with` block.
        :return: the entered context object
        :rtype: object
        """
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Remove this context from its manager when the `with` block exits.

        :param exc_type: exception class supplied by the context-manager protocol
        :type exc_type: object
        :param exc_val: exception instance supplied by the context-manager protocol
        :type exc_val: object
        :param exc_tb: traceback supplied by the context-manager protocol
        :type exc_tb: object
        :return: `None`; the operation mutates state, writes output, or raises by design.
        :rtype: None
        """
        ...

class MathContext(TeXContext):
    ...

class TeXBlock(TeXWriter):
    """Real access pattern: TeXBlock.<AttrName> (6 class attributes, e.g. TeXBlock.tag == None). Collapsed into a dict below purely for compactness -- do not index it as a dict in real code:"""
    _MEMBERS = {'tag': None, 'modifier': None, 'modifier_type': '[]', 'separator': '\n', 'context': None, 'label_header': None}

    def __init__(self, body=None, *, tag=None, modifier=None, modifier_type=None, separator=None, context=None, label=None):
        """
        **LLM Docstring**

        Initialize `TeXBlock` state from the supplied configuration.

        :param body: content to format or wrap
        :type body: object
        :param tag: TeX environment or command tag
        :type tag: object
        :param modifier: optional text appended to the environment opener
        :type modifier: object
        :param modifier_type: delimiter pair or pairs used around the modifier
        :type modifier_type: object
        :param separator: header separator character or block separator
        :type separator: object
        :param context: active `TeXContextManager` or context name used while formatting
        :type context: object
        :param label: parsed reference label
        :type label: object
        :return: `None`; the operation mutates state, writes output, or raises by design.
        :rtype: None
        """
        ...

    def prep_body(self, context=None):
        """
        **LLM Docstring**

        Format each body element, append a normalized `\\label{...}` when requested, and return the body fragments.

        :param context: active `TeXContextManager` or context name used while formatting
        :type context: object
        :return: formatted body fragments
        :rtype: list[str]
        """
        ...

    @classmethod
    def construct_modified_tag(self, tag, mod, mod_type='[]'):
        """
        **LLM Docstring**

        Build matching `\\begin` and `\\end` strings, inserting one or more delimited modifiers after the opener.

        :param tag: TeX environment or command tag
        :type tag: object
        :param mod: optional modifier text appended to the environment opener
        :type mod: object
        :param mod_type: delimiter pair or pairs used around modifiers
        :type mod_type: object
        :return: environment opener and closer
        :rtype: tuple[str, str]
        """
        ...

    def construct_header_footer(self):
        """
        **LLM Docstring**

        Construct this block’s environment opener and closer from its configured tag and modifier.
        :return: environment opener and closer
        :rtype: tuple[str, str]
        """
        ...

    def format_body(self, body_params):
        """
        **LLM Docstring**

        Wrap formatted body fragments in the environment tags, when a tag is configured, and join them with the block separator.

        :param body_params: already-formatted body fragments
        :type body_params: object
        :return: formatted TeX source
        :rtype: str
        """
        ...

    def format_tex(self, context=None):
        """
        **LLM Docstring**

        Format a block, entering its requested context while preparing the body and then emitting the environment text.

        :param context: active `TeXContextManager` or context name used while formatting
        :type context: object
        :return: formatted TeX source
        :rtype: str
        """
        ...

    def __call__(self, body):
        """
        **LLM Docstring**

        Clone the block configuration around a replacement body.

        :param body: content to format or wrap
        :type body: object
        :return: new symbolic or wrapper object
        :rtype: object
        """
        ...

class TeXRow(TeXBlock):
    tag = None
    separator = ' '

class TeXArray(TeXBlock):
    """Real access pattern: TeXArray.<AttrName> (9 class attributes, e.g. TeXArray.tag == 'tabular'). Collapsed into a dict below purely for compactness -- do not index it as a dict in real code:"""
    _MEMBERS = {'tag': 'tabular', 'modifier_type': '{}', 'separator': '\n', 'array_separator': ' & ', 'array_newline': ' \\\\\n', 'header_separator': '\n\\hline \\\\[-4ex]\n', 'header_lines': '\n\\hline \\\\[-4ex]', 'footer_lines': '\\hline \\\\[-4ex]\n', 'number_format': '{:8.3f}'}

    def __init__(self, headers_or_body, body=None, *, alignment='auto', number_format='{:8.3f}', content_join=None, column_join=None, row_join=None, separator=None, header_spans=None, header_alignments=None, resizeable=False, **opts):
        """
        **LLM Docstring**

        Initialize `TeXArray` state from the supplied configuration.

        :param headers_or_body: header rows or, when `body` is omitted, the table body itself
        :type headers_or_body: object
        :param body: content to format or wrap
        :type body: object
        :param alignment: column alignment specification or `auto`
        :type alignment: object
        :param number_format: formatter used for numeric table entries
        :type number_format: object
        :param content_join: separator between header and body
        :type content_join: object
        :param column_join: separator or separator sequence between columns
        :type column_join: object
        :param row_join: separator between rows
        :type row_join: object
        :param separator: header separator character or block separator
        :type separator: object
        :param header_spans: column spans for each header cell
        :type header_spans: object
        :param header_alignments: alignment codes for header cells
        :type header_alignments: object
        :param resizeable: whether to emit a `tabularx` environment sized to `\\textwidth`
        :type resizeable: object
        :param opts: additional keyword options forwarded to the underlying formatter or operation
        :type opts: dict
        :return: `None`; the operation mutates state, writes output, or raises by design.
        :rtype: None
        """
        ...

    def construct_alignment_spec(self, body):
        """
        **LLM Docstring**

        Infer one TeX alignment code per column, using centered columns for nonnumeric content and right alignment otherwise.

        :param body: content to format or wrap
        :type body: object
        :return: one-character alignment specification per column
        :rtype: str
        """
        ...

    def construct_header_footer(self):
        """
        **LLM Docstring**

        Build the `tabular` or `tabularx` delimiters, inferred alignment specification, and horizontal-rule decorations.
        :return: decorated environment opener and closer
        :rtype: tuple[str, str]
        """
        ...

    def format_numpy_array(self, array):
        """
        **LLM Docstring**

        Render a numeric array with `numpy.savetxt`, choosing field width from the largest magnitude and configured decimal precision.

        :param array: NumPy array to serialize as TeX table rows
        :type array: object
        :return: formatted TeX source
        :rtype: str
        """
        ...

    def format_mixed_array(self, array, context=None):
        """
        **LLM Docstring**

        Render heterogeneous rows after TeX-dispatching each cell and left-padding cells to common per-column widths.

        :param array: NumPy array to serialize as TeX table rows
        :type array: object
        :param context: active `TeXContextManager` or context name used while formatting
        :type context: object
        :return: formatted TeX source
        :rtype: str
        """
        ...

    def prep_body(self, context=None, headers=None, body=None):
        """
        **LLM Docstring**

        Normalize optional headers, multicolumn spans, and column formatters, then delegate table layout to `TableFormatter`.

        :param context: active `TeXContextManager` or context name used while formatting
        :type context: object
        :param headers: optional header rows
        :type headers: object
        :param body: content to format or wrap
        :type body: object
        :return: formatted body fragments
        :rtype: list[str]
        """
        ...

class TeXTable(TeXBlock):
    tag = 'table'
    modifier = 'ht'
    modifier_type = '[]'
    separator = '\n'

    def __init__(self, headers_or_body, body=None, width=1, caption=None, resizeable=False, number_format=None, header_spans=None, **etc):
        """
        **LLM Docstring**

        Initialize `TeXTable` state from the supplied configuration.

        :param headers_or_body: header rows or, when `body` is omitted, the table body itself
        :type headers_or_body: object
        :param body: content to format or wrap
        :type body: object
        :param width: fraction of text width used by the minipage
        :type width: object
        :param caption: optional caption content
        :type caption: object
        :param resizeable: whether to emit a `tabularx` environment sized to `\\textwidth`
        :type resizeable: object
        :param number_format: formatter used for numeric table entries
        :type number_format: object
        :param header_spans: column spans for each header cell
        :type header_spans: object
        :param etc: additional keyword options forwarded to the underlying formatter or operation
        :type etc: dict
        :return: `None`; the operation mutates state, writes output, or raises by design.
        :rtype: None
        """
        ...

    def prep_body(self, context=None, body=None):
        """
        **LLM Docstring**

        Wrap the table content in a centered minipage and append optional caption and label commands.

        :param context: active `TeXContextManager` or context name used while formatting
        :type context: object
        :param body: content to format or wrap
        :type body: object
        :return: formatted body fragments
        :rtype: list[str]
        """
        ...

class TeXFunction(TeXWriter):
    function_name = None

    def __init__(self, *args, function_name=None):
        """
        **LLM Docstring**

        Initialize `TeXFunction` state from the supplied configuration.

        :param args: additional positional values forwarded or collected by this operation
        :type args: tuple
        :param function_name: TeX command name without the leading backslash
        :type function_name: object
        :return: `None`; the operation mutates state, writes output, or raises by design.
        :rtype: None
        """
        ...

    def format_tex(self, context=None):
        """
        **LLM Docstring**

        Emit a TeX command followed by each dispatched argument enclosed in braces.

        :param context: active `TeXContextManager` or context name used while formatting
        :type context: object
        :return: formatted TeX source
        :rtype: str
        """
        ...

class TeXMulticolumn(TeXFunction):
    function_name = 'multicolumn'

    def __init__(self, width, fmt, body):
        """
        **LLM Docstring**

        Initialize `TeXMulticolumn` state from the supplied configuration.

        :param width: fraction of text width used by the minipage
        :type width: object
        :param fmt: formatter object or formatting specification
        :type fmt: object
        :param body: content to format or wrap
        :type body: object
        :return: `None`; the operation mutates state, writes output, or raises by design.
        :rtype: None
        """
        ...

class TeXBold(TeXFunction):
    function_name = 'textbf'

class TeXBracketed(TeXWriter):
    brackets = (None, None)

    def __init__(self, body, brackets=None):
        """
        **LLM Docstring**

        Initialize `TeXBracketed` state from the supplied configuration.

        :param body: content to format or wrap
        :type body: object
        :param brackets: left and right delimiters
        :type brackets: object
        :return: `None`; the operation mutates state, writes output, or raises by design.
        :rtype: None
        """
        ...

    def format_tex(self, context=None):
        """
        **LLM Docstring**

        Dispatch the wrapped body and surround it with the configured TeX delimiters.

        :param context: active `TeXContextManager` or context name used while formatting
        :type context: object
        :return: formatted TeX source
        :rtype: str
        """
        ...

class TeXParenthesized(TeXBracketed):
    brackets = ('\\left(', '\\right)')

class TeXEquation(TeXBlock):
    tag = 'equation'
    context = MathContext
    label_header = 'eq'

class TeXNode(Abstract.Expr):

    def to_ast(self):
        """
        **LLM Docstring**

        Reject AST conversion because TeX-only symbolic nodes are formatting constructs, not executable expressions.
        :return: `None`; the operation mutates state, writes output, or raises by design.
        :rtype: None
        """
        ...

class TeXSuperscript(TeXNode):
    __tag__ = 'Superscript'
    __slots__ = ['obj', 'index']

    def __init__(self, obj, index):
        """
        **LLM Docstring**

        Initialize `TeXSuperscript` state from the supplied configuration.

        :param obj: base symbolic object
        :type obj: object
        :param index: subscript or superscript index
        :type index: object
        :return: `None`; the operation mutates state, writes output, or raises by design.
        :rtype: None
        """
        ...

class TeXApply(TeXNode):
    __tag__ = 'Apply'
    __slots__ = ['function', 'argument']

    def __init__(self, function, argument):
        """
        **LLM Docstring**

        Initialize `TeXApply` state from the supplied configuration.

        :param function: symbolic function expression
        :type function: object
        :param argument: symbolic function argument
        :type argument: object
        :return: `None`; the operation mutates state, writes output, or raises by design.
        :rtype: None
        """
        ...

class TeXSymbol(Abstract.Name):

    def __call__(self, *args):
        """
        **LLM Docstring**

        Invoke the object’s configured conversion or construction behavior.

        :param args: additional positional values forwarded or collected by this operation
        :type args: tuple
        :return: new symbolic or wrapper object
        :rtype: object
        """
        ...

class TeXExpr(TeXWriter):

    @classmethod
    def name(cls, s):
        """
        **LLM Docstring**

        Normalize multi-character names to TeX control sequences and wrap them as a symbolic TeX expression.

        :param s: symbol name or source string
        :type s: object
        :return: new symbolic or wrapper object
        :rtype: object
        """
        ...

    @classmethod
    def symbol(cls, s):
        """
        **LLM Docstring**

        Normalize multi-character names to TeX control sequences and wrap them as a symbolic TeX expression.

        :param s: symbol name or source string
        :type s: object
        :return: new symbolic or wrapper object
        :rtype: object
        """
        ...

    def __init__(self, body):
        """
        **LLM Docstring**

        Initialize `TeXExpr` state from the supplied configuration.

        :param body: content to format or wrap
        :type body: object
        :return: `None`; the operation mutates state, writes output, or raises by design.
        :rtype: None
        """
        ...

    def __add__(self, other):
        """
        **LLM Docstring**

        Build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating the current expression.

        :param other: right-hand operand
        :type other: object
        :return: new symbolic or wrapper object
        :rtype: object
        """
        ...

    def __radd__(self, other):
        """
        **LLM Docstring**

        Build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating the current expression.

        :param other: right-hand operand
        :type other: object
        :return: new symbolic or wrapper object
        :rtype: object
        """
        ...

    def __mul__(self, other):
        """
        **LLM Docstring**

        Build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating the current expression.

        :param other: right-hand operand
        :type other: object
        :return: new symbolic or wrapper object
        :rtype: object
        """
        ...

    def __rmul__(self, other):
        """
        **LLM Docstring**

        Build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating the current expression.

        :param other: right-hand operand
        :type other: object
        :return: new symbolic or wrapper object
        :rtype: object
        """
        ...

    def __pow__(self, other):
        """
        **LLM Docstring**

        Build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating the current expression.

        :param other: right-hand operand
        :type other: object
        :return: new symbolic or wrapper object
        :rtype: object
        """
        ...

    def __neg__(self):
        """
        **LLM Docstring**

        Build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating the current expression.
        :return: new symbolic or wrapper object
        :rtype: object
        """
        ...

    def __xor__(self, other):
        """
        **LLM Docstring**

        Build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating the current expression.

        :param other: right-hand operand
        :type other: object
        :return: new symbolic or wrapper object
        :rtype: object
        """
        ...

    def __or__(self, other):
        """
        **LLM Docstring**

        Build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating the current expression.

        :param other: right-hand operand
        :type other: object
        :return: new symbolic or wrapper object
        :rtype: object
        """
        ...

    def __getitem__(self, item):
        """
        **LLM Docstring**

        Build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating the current expression.

        :param item: subscript or slice
        :type item: object
        :return: new symbolic or wrapper object
        :rtype: object
        """
        ...

    def Equals(self, other):
        """
        **LLM Docstring**

        Build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating the current expression.

        :param other: right-hand operand
        :type other: object
        :return: build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating the current expression
        :rtype: object
        """
        ...
    Eq = Equals

    def LessThan(self, other):
        """
        **LLM Docstring**

        Build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating the current expression.

        :param other: right-hand operand
        :type other: object
        :return: build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating the current expression
        :rtype: object
        """
        ...
    Lt = LessThan

    def LessEquals(self, other):
        """
        **LLM Docstring**

        Build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating the current expression.

        :param other: right-hand operand
        :type other: object
        :return: build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating the current expression
        :rtype: object
        """
        ...
    LtE = LessEquals

    def GreaterThan(self, other):
        """
        **LLM Docstring**

        Build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating the current expression.

        :param other: right-hand operand
        :type other: object
        :return: build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating the current expression
        :rtype: object
        """
        ...
    Gt = GreaterThan

    def GreaterEquals(self, other):
        """
        **LLM Docstring**

        Build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating the current expression.

        :param other: right-hand operand
        :type other: object
        :return: build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating the current expression
        :rtype: object
        """
        ...
    GtE = GreaterEquals

    @staticmethod
    def convert_name(name, converter):
        """
        **LLM Docstring**

        Convert a symbolic name node into its TeX string representation using the recursive converter.

        :param name: registry, resource, or output name
        :type name: object
        :param converter: recursive callable used to format child symbolic nodes
        :type converter: object
        :return: TeX representation of the symbolic node
        :rtype: str
        """
        ...

    @staticmethod
    def convert_const(const, converter):
        """
        **LLM Docstring**

        Convert a symbolic const node into its TeX string representation using the recursive converter.

        :param const: symbolic constant node whose value is emitted
        :type const: object
        :param converter: recursive callable used to format child symbolic nodes
        :type converter: object
        :return: TeX representation of the symbolic node
        :rtype: str
        """
        ...

    @staticmethod
    def convert_call(call, converter):
        """
        **LLM Docstring**

        Convert a symbolic call node into its TeX string representation using the recursive converter.

        :param call: symbolic call node containing a function and arguments
        :type call: object
        :param converter: recursive callable used to format child symbolic nodes
        :type converter: object
        :return: TeX representation of the symbolic node
        :rtype: str
        """
        ...

    @staticmethod
    def convert_superscript(op, converter):
        """
        **LLM Docstring**

        Convert a symbolic superscript node into its TeX string representation using the recursive converter.

        :param op: symbolic operation node being converted
        :type op: object
        :param converter: recursive callable used to format child symbolic nodes
        :type converter: object
        :return: TeX representation of the symbolic node
        :rtype: str
        """
        ...

    @staticmethod
    def convert_bitxor(op, converter):
        """
        **LLM Docstring**

        Convert a symbolic bitxor node into its TeX string representation using the recursive converter.

        :param op: symbolic operation node being converted
        :type op: object
        :param converter: recursive callable used to format child symbolic nodes
        :type converter: object
        :return: TeX representation of the symbolic node
        :rtype: str
        """
        ...

    @staticmethod
    def convert_power(op, converter):
        """
        **LLM Docstring**

        Convert a symbolic power node into its TeX string representation using the recursive converter.

        :param op: symbolic operation node being converted
        :type op: object
        :param converter: recursive callable used to format child symbolic nodes
        :type converter: object
        :return: TeX representation of the symbolic node
        :rtype: str
        """
        ...

    @staticmethod
    def convert_subscript(op, converter):
        """
        **LLM Docstring**

        Convert a symbolic subscript node into its TeX string representation using the recursive converter.

        :param op: symbolic operation node being converted
        :type op: object
        :param converter: recursive callable used to format child symbolic nodes
        :type converter: object
        :return: TeX representation of the symbolic node
        :rtype: str
        """
        ...

    @staticmethod
    def convert_add(op, converter):
        """
        **LLM Docstring**

        Convert a symbolic add node into its TeX string representation using the recursive converter.

        :param op: symbolic operation node being converted
        :type op: object
        :param converter: recursive callable used to format child symbolic nodes
        :type converter: object
        :return: TeX representation of the symbolic node
        :rtype: str
        """
        ...

    @staticmethod
    def convert_sub(op, converter):
        """
        **LLM Docstring**

        Convert a symbolic sub node into its TeX string representation using the recursive converter.

        :param op: symbolic operation node being converted
        :type op: object
        :param converter: recursive callable used to format child symbolic nodes
        :type converter: object
        :return: TeX representation of the symbolic node
        :rtype: str
        """
        ...

    @staticmethod
    def convert_mul(op, converter):
        """
        **LLM Docstring**

        Convert a symbolic mul node into its TeX string representation using the recursive converter.

        :param op: symbolic operation node being converted
        :type op: object
        :param converter: recursive callable used to format child symbolic nodes
        :type converter: object
        :return: TeX representation of the symbolic node
        :rtype: str
        """
        ...

    @staticmethod
    def convert_bitor(op, converter):
        """
        **LLM Docstring**

        Convert a symbolic bitor node into its TeX string representation using the recursive converter.

        :param op: symbolic operation node being converted
        :type op: object
        :param converter: recursive callable used to format child symbolic nodes
        :type converter: object
        :return: TeX representation of the symbolic node
        :rtype: str
        """
        ...

    @staticmethod
    def convert_div(op, converter):
        """
        **LLM Docstring**

        Convert a symbolic div node into its TeX string representation using the recursive converter.

        :param op: symbolic operation node being converted
        :type op: object
        :param converter: recursive callable used to format child symbolic nodes
        :type converter: object
        :return: TeX representation of the symbolic node
        :rtype: str
        """
        ...

    @staticmethod
    def convert_eq(op, converter):
        """
        **LLM Docstring**

        Convert a symbolic eq node into its TeX string representation using the recursive converter.

        :param op: symbolic operation node being converted
        :type op: object
        :param converter: recursive callable used to format child symbolic nodes
        :type converter: object
        :return: TeX representation of the symbolic node
        :rtype: str
        """
        ...

    @staticmethod
    def convert_raw(obj, converter):
        """
        **LLM Docstring**

        Convert a symbolic raw node into its TeX string representation using the recursive converter.

        :param obj: base symbolic object
        :type obj: object
        :param converter: recursive callable used to format child symbolic nodes
        :type converter: object
        :return: TeX representation of the symbolic node
        :rtype: str
        """
        ...

    @property
    def converter_dispatch(self):
        """
        **LLM Docstring**

        Return the mapping from symbolic node tags to TeX conversion functions, including a raw fallback.
        :return: symbolic-node conversion dispatch table
        :rtype: dict
        """
        ...

    def format_tex(self, context=None):
        """
        **LLM Docstring**

        Transmogrify the symbolic expression through TeX converters and add dollar delimiters only outside existing math mode.

        :param context: active `TeXContextManager` or context name used while formatting
        :type context: object
        :return: formatted TeX source
        :rtype: str
        """
        ...

class TeX:
    """
    Namespace for TeX-related utilities, someday might help with document prep from templates
    """
    Writer = TeXWriter
    Block = TeXBlock
    Row = TeXRow
    Expr = TeXExpr
    Symbol = TeXExpr.name
    Function = TeXExpr.symbol
    Array = TeXArray
    Table = TeXTable
    Equation = TeXEquation
    wrap_parens = TeXParenthesized
    bold = TeXBold

    @classmethod
    def Matrix(cls, mat, **kwargs):
        """
        **LLM Docstring**

        Construct a TeX array from the matrix and wrap it in scalable parentheses.

        :param mat: value consumed as `mat` by the documented formatting path
        :type mat: object
        :param kwargs: additional keyword options forwarded to the underlying formatter or operation
        :type kwargs: dict
        :return: new symbolic or wrapper object
        :rtype: object
        """
        ...

class TeXImportGraph:
    import_heads = ('input', 'import', 'module', 'loadsec', 'loadfig', 'loadtab')

    def __init__(self, tex_root, root_dir=None, head_parser=None, import_heads=None, strip_comments=True, aliases=None, ignored_files=None, **parser_options):
        """
        **LLM Docstring**

        Initialize `TeXImportGraph` state from the supplied configuration.

        :param tex_root: root TeX file
        :type tex_root: object
        :param root_dir: directory used to resolve relative TeX imports
        :type root_dir: object
        :param head_parser: callable that extracts a command head
        :type head_parser: object
        :param import_heads: TeX command heads treated as imports
        :type import_heads: object
        :param strip_comments: whether comments are removed before parsing
        :type strip_comments: object
        :param aliases: path-variable substitutions
        :type aliases: object
        :param ignored_files: files excluded from traversal
        :type ignored_files: object
        :param parser_options: additional keyword options forwarded to the underlying formatter or operation
        :type parser_options: dict
        :return: `None`; the operation mutates state, writes output, or raises by design.
        :rtype: None
        """
        ...

    @classmethod
    def import_parser(cls, head: str, tag: str):
        """
        **LLM Docstring**

        Extract the argument following an import-like command, normalize it to a `.tex` filename, and return no extra options.

        :param head: TeX command head
        :type head: str
        :param tag: TeX environment or command tag
        :type tag: str
        :return: resolved `.tex` filename and empty parser options
        :rtype: tuple[str, dict]
        """
        ...

    @classmethod
    def head_resolver(cls, tag: str):
        """
        **LLM Docstring**

        Extract a TeX command head by removing the leading backslash and truncating before optional or required arguments.

        :param tag: TeX environment or command tag
        :type tag: str
        :return: normalized TeX command head
        :rtype: str
        """
        ...
    module_root = 'sections'

    @classmethod
    def load_module_parser(cls, tag: str):
        """
        **LLM Docstring**

        Resolve a module command to `sections/<module>/main.tex` and record the module directory as the new import root.

        :param tag: TeX environment or command tag
        :type tag: str
        :return: module main-file path and nested root option
        :rtype: tuple[str, dict]
        """
        ...

    @classmethod
    def load_block_parser(cls, head: str, root, tag: str):
        """
        **LLM Docstring**

        Resolve a `load*` command under its resource root and inject a label header for non-figure/table/equation resources.

        :param head: TeX command head
        :type head: str
        :param root: current TeX file or resource root
        :type root: object
        :param tag: TeX environment or command tag
        :type tag: str
        :return: resource file path and optional label header
        :rtype: tuple[str, dict]
        """
        ...

    @classmethod
    def resolve_parser(cls, head: str):
        """
        **LLM Docstring**

        Select the path parser for an import-like TeX command head.

        :param head: TeX command head
        :type head: str
        :return: callable that resolves paths for the command head
        :rtype: callable
        """
        ...
    ImportNode = collections.namedtuple('ImportNode', ['root_dir', 'end_points', 'head', 'block', 'opts'])
    root_dir_var = '\\RootDirectory'

    def _resolve_aliases(self, root_dir):
        """
        **LLM Docstring**

        Build the alias substitution table for a root directory, resolving later aliases against earlier values.

        :param root_dir: directory used to resolve relative TeX imports
        :type root_dir: object
        :return: resolved alias substitution mapping
        :rtype: dict
        """
        ...

    def _handle_parse_block(self, parser, head_map, import_heads, root_dir):
        """
        **LLM Docstring**

        Scan import-like TeX calls, resolve aliases and relative paths, and return endpoint metadata for each referenced file.

        :param parser: open `TeXParser` instance
        :type parser: object
        :param head_map: mapping from command heads to path parsers
        :type head_map: object
        :param import_heads: TeX command heads treated as imports
        :type import_heads: object
        :param root_dir: directory used to resolve relative TeX imports
        :type root_dir: object
        :return: imported file paths mapped to endpoint metadata
        :rtype: dict
        """
        ...

    @classmethod
    def strip_tex_comments(cls, body):
        """
        **LLM Docstring**

        Remove full-line and unescaped trailing percent comments from TeX source.

        :param body: content to format or wrap
        :type body: object
        :return: comment-stripped TeX source
        :rtype: str
        """
        ...

    def find_imports(self, root=None, import_heads=None, root_dir=None) -> dict[str, ImportNode]:
        """
        **LLM Docstring**

        Parse one TeX file for configured import commands, optionally through a comment-stripped temporary stream.

        :param root: current TeX file or resource root
        :type root: object
        :param import_heads: TeX command heads treated as imports
        :type import_heads: object
        :param root_dir: directory used to resolve relative TeX imports
        :type root_dir: object
        :return: referenced files mapped to import metadata
        :rtype: dict
        """
        ...
    verbose = False

    def populate_graph(self, import_heads=None, root_dir=None):
        """
        **LLM Docstring**

        Breadth/depth traverse reachable TeX imports, skip missing files, and memoize the resulting adjacency mapping.

        :param import_heads: TeX command heads treated as imports
        :type import_heads: object
        :param root_dir: directory used to resolve relative TeX imports
        :type root_dir: object
        :return: import adjacency mapping
        :rtype: dict
        """
        ...

class TeXTranspiler:

    def __init__(self, tex_root, root_dir=None, figure_renaming_function=None, bib_renaming_function=None, strip_comments=True, figures_path=None, figure_merge_function=None, bib_path=None, bib_merge_function=None, bib_cleanup_function=None, citation_renaming_function=None, aliases=None, styles_path=None, parser_options=None):
        """
        **LLM Docstring**

        Initialize `TeXTranspiler` state from the supplied configuration.

        :param tex_root: root TeX file
        :type tex_root: object
        :param root_dir: directory used to resolve relative TeX imports
        :type root_dir: object
        :param figure_renaming_function: value consumed as `figure_renaming_function` by the documented formatting path
        :type figure_renaming_function: object
        :param bib_renaming_function: value consumed as `bib_renaming_function` by the documented formatting path
        :type bib_renaming_function: object
        :param strip_comments: whether comments are removed before parsing
        :type strip_comments: object
        :param figures_path: value consumed as `figures_path` by the documented formatting path
        :type figures_path: object
        :param figure_merge_function: value consumed as `figure_merge_function` by the documented formatting path
        :type figure_merge_function: object
        :param bib_path: value consumed as `bib_path` by the documented formatting path
        :type bib_path: object
        :param bib_merge_function: value consumed as `bib_merge_function` by the documented formatting path
        :type bib_merge_function: object
        :param bib_cleanup_function: value consumed as `bib_cleanup_function` by the documented formatting path
        :type bib_cleanup_function: object
        :param citation_renaming_function: callable used to rename citation keys
        :type citation_renaming_function: object
        :param aliases: path-variable substitutions
        :type aliases: object
        :param styles_path: value consumed as `styles_path` by the documented formatting path
        :type styles_path: object
        :param parser_options: options forwarded to `TeXParser`
        :type parser_options: object
        :return: `None`; the operation mutates state, writes output, or raises by design.
        :rtype: None
        """
        ...

    @classmethod
    def figure_counter(cls, name_root='Figure', start_at=1):
        """
        **LLM Docstring**

        Create a stateful renamer that assigns sequential names while preserving each figure extension.

        :param name_root: prefix for generated figure names
        :type name_root: object
        :param start_at: first numeric suffix to generate
        :type start_at: object
        :return: stateful figure-renaming callable
        :rtype: callable
        """
        ...

    @classmethod
    def add_bibs(cls, bib_list):
        """
        **LLM Docstring**

        Concatenate bibliography files into a persistent temporary file and mark it for later deletion.

        :param bib_list: bibliography files to concatenate
        :type bib_list: object
        :return: temporary bibliography path and deletion flag
        :rtype: tuple[str, bool]
        """
        ...

    @classmethod
    def pruned_bib(cls, bib_file_or_filter, cites=None, *, filter=None, **parser_options):
        """
        **LLM Docstring**

        Filter a BibTeX file in place to entries referenced by the supplied citation map, or return a configured filter closure.

        :param bib_file_or_filter: bibliography filename or a citation-filter factory argument
        :type bib_file_or_filter: object
        :param cites: parsed citation map
        :type cites: object
        :param filter: additional callable mask over retained index arrays
        :type filter: object
        :param parser_options: additional keyword options forwarded to the underlying formatter or operation
        :type parser_options: dict
        :return: configured pruning callable when invoked as a factory, otherwise `None`
        :rtype: callable | None
        """
        ...

    @classmethod
    def get_injection_body(cls, root_dir, node_data: TeXImportGraph.ImportNode, body: str):
        """
        **LLM Docstring**

        Resolve and return the requested derived value from the object’s current configuration.

        :param root_dir: directory used to resolve relative TeX imports
        :type root_dir: object
        :param node_data: value consumed as `node_data` by the documented formatting path
        :type node_data: TeXImportGraph.ImportNode
        :param body: content to format or wrap
        :type body: str
        :return: source endpoints paired with normalized imported body
        :rtype: tuple
        """
        ...

    @classmethod
    def apply_body_edit(cls, cur_text, edits, normalization_function=None):
        """
        **LLM Docstring**

        Apply endpoint-based replacements in source order while accounting for text already consumed from the working buffer.

        :param cur_text: source text to edit
        :type cur_text: object
        :param edits: endpoint ranges paired with replacement bodies
        :type edits: object
        :param normalization_function: callable converting edit records to endpoint/body pairs
        :type normalization_function: object
        :return: source text with all replacements applied
        :rtype: str
        """
        ...

    @classmethod
    def flatten_import_graph(cls, graph: dict[str, dict[str, TeXImportGraph.ImportNode]], root, cache=None, root_dir=None, strip_comments=False):
        """
        **LLM Docstring**

        Recursively inline imported TeX files, memoizing results and inserting `None` sentinels to break cycles.

        :param graph: import adjacency mapping
        :type graph: dict[str, dict[str, TeXImportGraph.ImportNode]]
        :param root: current TeX file or resource root
        :type root: object
        :param cache: memoized flattened file bodies
        :type cache: object
        :param root_dir: directory used to resolve relative TeX imports
        :type root_dir: object
        :param strip_comments: whether comments are removed before parsing
        :type strip_comments: object
        :return: flattened TeX source, optionally paired with auxiliary metadata
        :rtype: object
        """
        ...

    def remap_block(self, flat_tex, call_head, file_parser, replacement_path=None, renaming_function=None):
        """
        **LLM Docstring**

        Locate resource commands, extract filenames, optionally rename/repath them, and rewrite the command bodies.

        :param flat_tex: flattened TeX source or path to it
        :type flat_tex: object
        :param call_head: TeX command head to locate
        :type call_head: object
        :param file_parser: callable extracting resource paths from command text
        :type file_parser: object
        :param replacement_path: new resource directory prefix
        :type replacement_path: object
        :param renaming_function: callable mapping original resources to output names
        :type renaming_function: object
        :return: rewritten TeX source and any associated mapping metadata
        :rtype: object
        """
        ...

    @classmethod
    def _repath_resource(cls, new_root, figure_path, renaming_function=None):
        """
        **LLM Docstring**

        Move one or many resource paths under a new root, optionally renaming each basename.

        :param new_root: new directory prefix
        :type new_root: object
        :param figure_path: single resource path or collection of paths
        :type figure_path: object
        :param renaming_function: callable mapping original resources to output names
        :type renaming_function: object
        :return: resource path or comma-separated resource paths under the new root
        :rtype: str
        """
        ...

    @classmethod
    def _parse_graphics_file(cls, tag: str):
        """
        **LLM Docstring**

        Parse the matched TeX command into its command head, resource or reference type, and normalized payload.

        :param tag: TeX environment or command tag
        :type tag: str
        :return: single resource path or tuple of paths
        :rtype: str | tuple[str, ...]
        """
        ...

    @classmethod
    def _modify_resource_path(cls, tag: str, file_map):
        """
        **LLM Docstring**

        Replace the comma-separated resource payload inside a TeX command using the supplied path map.

        :param tag: TeX environment or command tag
        :type tag: str
        :param file_map: mapping from original resource names to rewritten names
        :type file_map: object
        :return: TeX command with its resource payload replaced
        :rtype: str
        """
        ...

    def remap_figures(self, flat_tex, figures_path=None):
        """
        **LLM Docstring**

        Rewrite the corresponding TeX resource or reference commands and return the updated source together with mapping metadata where applicable.

        :param flat_tex: flattened TeX source or path to it
        :type flat_tex: object
        :param figures_path: value consumed as `figures_path` by the documented formatting path
        :type figures_path: object
        :return: rewritten TeX source and any associated mapping metadata
        :rtype: object
        """
        ...

    def remap_bibliography(self, flat_tex, bib_path=None):
        """
        **LLM Docstring**

        Rewrite the corresponding TeX resource or reference commands and return the updated source together with mapping metadata where applicable.

        :param flat_tex: flattened TeX source or path to it
        :type flat_tex: object
        :param bib_path: value consumed as `bib_path` by the documented formatting path
        :type bib_path: object
        :return: rewritten TeX source and any associated mapping metadata
        :rtype: object
        """
        ...

    def remap_style_files(self, flat_tex, styles_path=None):
        """
        **LLM Docstring**

        Rewrite the corresponding TeX resource or reference commands and return the updated source together with mapping metadata where applicable.

        :param flat_tex: flattened TeX source or path to it
        :type flat_tex: object
        :param styles_path: value consumed as `styles_path` by the documented formatting path
        :type styles_path: object
        :return: rewritten TeX source and any associated mapping metadata
        :rtype: object
        """
        ...

    @classmethod
    def get_call_list(self, tex_stream, tags) -> dict[tuple[int, int], str]:
        """
        **LLM Docstring**

        Resolve and return the requested derived value from the object’s current configuration.

        :param tex_stream: TeX source string, file, or stream
        :type tex_stream: object
        :param tags: command tags to scan
        :type tags: object
        :return: source endpoint ranges mapped to raw TeX calls
        :rtype: dict
        """
        ...

    @classmethod
    def _parse_label_ref(cls, l: str):
        """
        **LLM Docstring**

        Parse the matched TeX command into its command head, resource or reference type, and normalized payload.

        :param l: raw TeX label/reference command text
        :type l: str
        :return: command head, label type, and label identifier
        :rtype: tuple[str, str, str]
        """
        ...
    LabelBlock = collections.namedtuple('LabelBlock', ['tag', 'ref', 'end_points', 'head', 'block'])

    @classmethod
    def create_label_block_map(cls, tex_stream, call_tags, block_parser):
        """
        **LLM Docstring**

        Scan the TeX source for the requested command family and organize parsed blocks by type and source endpoints.

        :param tex_stream: TeX source string, file, or stream
        :type tex_stream: object
        :param call_tags: command tags to scan
        :type call_tags: object
        :param block_parser: callable decomposing a matched command
        :type block_parser: object
        :return: parsed blocks organized by type and source endpoints
        :rtype: dict
        """
        ...

    @classmethod
    def create_label_map(cls, tex_stream):
        """
        **LLM Docstring**

        Scan the TeX source for the requested command family and organize parsed blocks by type and source endpoints.

        :param tex_stream: TeX source string, file, or stream
        :type tex_stream: object
        :return: parsed blocks organized by type and source endpoints
        :rtype: dict
        """
        ...

    @classmethod
    def _parse_ref_ref(cls, l):
        """
        **LLM Docstring**

        Parse the matched TeX command into its command head, resource or reference type, and normalized payload.

        :param l: raw TeX label/reference command text
        :type l: object
        :return: command head, reference type, and normalized reference payload
        :rtype: tuple
        """
        ...

    @classmethod
    def create_ref_map(cls, tex_stream):
        """
        **LLM Docstring**

        Scan the TeX source for the requested command family and organize parsed blocks by type and source endpoints.

        :param tex_stream: TeX source string, file, or stream
        :type tex_stream: object
        :return: parsed blocks organized by type and source endpoints
        :rtype: dict
        """
        ...

    @classmethod
    def _parse_cite_ref(cls, l):
        """
        **LLM Docstring**

        Parse the matched TeX command into its command head, resource or reference type, and normalized payload.

        :param l: raw TeX label/reference command text
        :type l: object
        :return: command head, `cite` type tag, and citation keys
        :rtype: tuple[str, str, list[str]]
        """
        ...

    @classmethod
    def create_cite_map(cls, tex_stream):
        """
        **LLM Docstring**

        Scan the TeX source for the requested command family and organize parsed blocks by type and source endpoints.

        :param tex_stream: TeX source string, file, or stream
        :type tex_stream: object
        :return: parsed blocks organized by type and source endpoints
        :rtype: dict
        """
        ...

    @classmethod
    def remap_citation_set(cls, tex_stream, ref_handler, cite_map=None):
        """
        **LLM Docstring**

        Rewrite the corresponding TeX resource or reference commands and return the updated source together with mapping metadata where applicable.

        :param tex_stream: TeX source string, file, or stream
        :type tex_stream: object
        :param ref_handler: callable producing endpoint-to-replacement edits
        :type ref_handler: object
        :param cite_map: precomputed citation map
        :type cite_map: object
        :return: rewritten TeX source and any associated mapping metadata
        :rtype: object
        """
        ...

    @classmethod
    def _rename_cites(cls, citations, renaming):
        """
        **LLM Docstring**

        Build replacement citation commands by applying the renamer to every key while preserving each command head and endpoint.

        :param citations: citation blocks keyed by source endpoints
        :type citations: object
        :param renaming: callable that renames citation keys
        :type renaming: object
        :return: endpoint-to-rewritten-citation mapping
        :rtype: dict
        """
        ...

    def remap_citations(self, flat_tex, si_tex: dict[str, str]=None, citation_renaming_function=None):
        """
        **LLM Docstring**

        Rewrite the corresponding TeX resource or reference commands and return the updated source together with mapping metadata where applicable.

        :param flat_tex: flattened TeX source or path to it
        :type flat_tex: object
        :param si_tex: supplementary-document source mapping
        :type si_tex: dict[str, str]
        :param citation_renaming_function: callable used to rename citation keys
        :type citation_renaming_function: object
        :return: rewritten TeX source and any associated mapping metadata
        :rtype: object
        """
        ...
    ref_tag_map = {'sec': ('Sec.', 'Secs.'), 'fig': ('Fig.', 'Figs.'), 'tab': ('Table', 'Tables'), 'eq': ('Eq.', 'Eqs.')}
    ref_label_formats = {'single': '{tag} {index}', 'pair': '{tag} {index[0]} and {index[1]}', 'range': '{tag} {index[0]}-{index[1]}'}
    si_ref_format = 'S{i}'
    main_ref_format = 'ref{{{ref}}}'

    @classmethod
    def ref_remapping_label(cls, head, label, si_index_map):
        """
        **LLM Docstring**

        Convert references to supplementary labels into explicit display text while leaving main-document references as TeX refs.

        :param head: TeX command head
        :type head: object
        :param label: parsed reference label
        :type label: object
        :param si_index_map: mapping of supplementary labels to one-based display indices
        :type si_index_map: object
        :return: replacement display text, or `None` when no supplementary reference is present
        :rtype: str | None
        """
        ...

    @classmethod
    def figure_table_remapping(cls, si_labels: dict[str, dict[tuple[int, int], LabelBlock]], label_function=None):
        """
        **LLM Docstring**

        Build a closure that rewrites references using stable supplementary figure/table/equation indices.

        :param si_labels: labels extracted from supplementary documents
        :type si_labels: dict[str, dict[tuple[int, int], LabelBlock]]
        :param label_function: callable converting a reference block to replacement text
        :type label_function: object
        :return: reference-map handler closure
        :rtype: callable
        """
        ...

    @classmethod
    def remap_refs(cls, tex_stream, ref_handler, ref_map=None):
        """
        **LLM Docstring**

        Rewrite the corresponding TeX resource or reference commands and return the updated source together with mapping metadata where applicable.

        :param tex_stream: TeX source string, file, or stream
        :type tex_stream: object
        :param ref_handler: callable producing endpoint-to-replacement edits
        :type ref_handler: object
        :param ref_map: precomputed reference map
        :type ref_map: object
        :return: rewritten TeX source and any associated mapping metadata
        :rtype: object
        """
        ...
    si_doc_labels = ('referenceExternalDocument',)

    @classmethod
    def find_si_documents(cls, flat_tex):
        """
        **LLM Docstring**

        Find external supplementary-document commands and map document names to their source endpoint ranges.

        :param flat_tex: flattened TeX source or path to it
        :type flat_tex: object
        :return: supplementary document names mapped to source endpoints
        :rtype: dict
        """
        ...

    def remap_si(self, flat_tex):
        """
        **LLM Docstring**

        Rewrite the corresponding TeX resource or reference commands and return the updated source together with mapping metadata where applicable.

        :param flat_tex: flattened TeX source or path to it
        :type flat_tex: object
        :return: rewritten TeX source and any associated mapping metadata
        :rtype: object
        """
        ...

    def create_flat_tex(self, include_aux=True):
        """
        **LLM Docstring**

        Flatten imports and optionally remap styles, figures, bibliography, supplementary documents, and citations into an auxiliary manifest.

        :param include_aux: whether resource remapping metadata is returned
        :type include_aux: object
        :return: flattened TeX source, optionally paired with auxiliary metadata
        :rtype: object
        """
        ...

    @classmethod
    def _copy_inputs(cls, root_dir, target_dir, resource_path, inputs, merge_function, search_paths=None, allow_missing=False, post_processor=None):
        """
        **LLM Docstring**

        Copy or merge auxiliary resources into the output tree, optionally searching fallback paths and post-processing copies.

        :param root_dir: directory used to resolve relative TeX imports
        :type root_dir: object
        :param target_dir: output directory for the transpiled document
        :type target_dir: object
        :param resource_path: resource subdirectory inside the output directory
        :type resource_path: object
        :param inputs: source-to-target resource mapping or iterable of resource paths
        :type inputs: object
        :param merge_function: callable combining multiple sources into one temporary resource
        :type merge_function: object
        :param search_paths: fallback subdirectories searched for missing sources
        :type search_paths: object
        :param allow_missing: whether absent resources are silently skipped
        :type allow_missing: object
        :param post_processor: callable run on each copied output file
        :type post_processor: object
        :return: `None`; the operation mutates state, writes output, or raises by design.
        :rtype: None
        """
        ...
    style_search_paths = ['styles']

    def transpile(self, target_dir, file_name='main.tex', include_si=True, include_aux=True, allow_missing_styles=False):
        """
        **LLM Docstring**

        Flatten the document, copy remapped auxiliary resources and supplementary files, and write the final root TeX file.

        :param target_dir: output directory for the transpiled document
        :type target_dir: object
        :param file_name: name of the generated root TeX file
        :type file_name: object
        :param include_si: whether flattened supplementary documents are written
        :type include_si: object
        :param include_aux: whether resource remapping metadata is returned
        :type include_aux: object
        :param allow_missing_styles: whether unavailable class/style files may be skipped
        :type allow_missing_styles: object
        :return: the output directory path
        :rtype: str
        """
        ...
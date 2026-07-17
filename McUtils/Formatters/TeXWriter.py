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

__all__ = [
    "TeX",
    "TeXTranspiler"
]

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
        if isinstance(b, TeXWriter) or hasattr(b, 'format_tex'):
            return b.format_tex(context)
        elif isinstance(b, (float, np.floating)):
            return ('{:.'+str(cls.real_digits)+'f}').format(b)
        elif isinstance(b, np.ndarray):
            return TeXArray(b).format_tex(context)
        elif isinstance(b, (list, tuple)):
            if isinstance(b[0], (list, tuple)):
                return TeXArray(b).format_tex(context)
            else:
                return TeXRow(b).format_tex(context)
        else:
            return str(b)

    def as_expr(self):
        """
        **LLM Docstring**

        Wrap this writer as a symbolic `TeXExpr` so arithmetic and comparison composition can be used.
        :return: new symbolic or wrapper object
        :rtype: object
        """
        return TeXExpr(self)

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
        if name not in cls.default_contexts:
            ctx = cls()
            cls.default_contexts[name] = ctx
        return cls.default_contexts[name]

    def __init__(self):
        """
        **LLM Docstring**

        Initialize an empty stack of nested TeX formatting contexts.
        :return: `None`; the operation mutates state, writes output, or raises by design.
        :rtype: None
        """
        self.context_stack = []
    def subcontext(self, cls):
        """
        **LLM Docstring**

        Instantiate a context class bound to this manager.

        :param cls: class being configured
        :type cls: object
        :return: new context instance bound to this manager
        :rtype: TeXContext
        """
        return cls(self)
    def set_context(self, ctx):
        """
        **LLM Docstring**

        Push a context onto the active-context stack.

        :param ctx: context object to push
        :type ctx: object
        :return: the pushed context
        :rtype: TeXContext
        """
        self.context_stack.append(ctx)
        return ctx
    def leave_context(self):
        """
        **LLM Docstring**

        Pop the most recently entered context.
        :return: `None`; the operation mutates state, writes output, or raises by design.
        :rtype: None
        """
        self.context_stack.pop()
    @property
    def context(self):
        """
        **LLM Docstring**

        Return the currently active context, or `None` when the stack is empty.
        :return: active context or `None`
        :rtype: TeXContext | None
        """
        if len(self.context_stack) == 0:
            return None
        else:
            return self.context_stack[-1]
    @property
    def math_mode(self):
        """
        **LLM Docstring**

        Report whether the current context is a `MathContext`.
        :return: whether math mode is active
        :rtype: bool
        """
        return isinstance(self.context, MathContext)

class TeXContext:
    def __init__(self, manager:TeXContextManager):
        """
        **LLM Docstring**

        Bind a context object to the manager whose stack it controls.

        :param manager: context manager that owns this context
        :type manager: TeXContextManager
        :return: `None`; the operation mutates state, writes output, or raises by design.
        :rtype: None
        """
        self.manager = manager
    def __enter__(self):
        """
        **LLM Docstring**

        Push this context and return it for use in a `with` block.
        :return: the entered context object
        :rtype: object
        """
        self.manager.set_context(self)
        return self
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
        self.manager.leave_context()
class MathContext(TeXContext):
    ...

class TeXBlock(TeXWriter):
    tag = None
    modifier = None
    modifier_type = '[]'
    separator = '\n'
    context = None
    label_header = None
    def __init__(self,
                 body=None, *,
                 tag=None,
                 modifier=None,
                 modifier_type=None,
                 separator=None,
                 context=None,
                 label=None
                 ):
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
        self.body = body
        if tag is None:
            tag = self.tag
        self.tag = tag
        if modifier is None:
            modifier = self.modifier
        self.modifier = modifier
        if modifier_type is None:
            modifier_type = self.modifier_type
        self.modifier_type = modifier_type
        if separator is None:
            separator = self.separator
        self.sep = separator
        if context is None:
            context = self.context
        self.ctx = context
        self.label = label
    def prep_body(self, context=None):
        """
        **LLM Docstring**

        Format each body element, append a normalized `\\label{...}` when requested, and return the body fragments.

        :param context: active `TeXContextManager` or context name used while formatting
        :type context: object
        :return: formatted body fragments
        :rtype: list[str]
        """
        if self.body is None:
            params = []
        elif isinstance(self.body, (list, tuple)):
            params = [self.dispatch_format(b, context) for b in self.body]
        else:
            params = [self.dispatch_format(self.body, context)]
        if self.label is not None:
            label = self.label
            if self.label_header is not None and ':' not in label:
                label = self.label_header + ':' + label
            params = params + ['\\label{' + label + "}"]
        return params
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
        header = "\\begin{"+str(tag)+"}"
        if mod is not None:
            if isinstance(mod_type, str):
                l, r = mod_type
                header = header + l + mod + r
            else:
                bits = []
                for m,t in zip(mod, mod_type):
                    l, r = t
                    bits.append(l + m + r)
                header = header + "".join(bits)
        return header, "\\end{"+str(tag)+"}"
    def construct_header_footer(self):
        """
        **LLM Docstring**

        Construct this block’s environment opener and closer from its configured tag and modifier.
        :return: environment opener and closer
        :rtype: tuple[str, str]
        """
        return self.construct_modified_tag(self.tag, self.modifier, self.modifier_type)
    def format_body(self, body_params):
        """
        **LLM Docstring**

        Wrap formatted body fragments in the environment tags, when a tag is configured, and join them with the block separator.

        :param body_params: already-formatted body fragments
        :type body_params: object
        :return: formatted TeX source
        :rtype: str
        """
        header, footer = self.construct_header_footer()
        if self.tag is not None:
            body_params = [header] + body_params + [footer]
        return self.sep.join(body_params)
    def format_tex(self, context=None):
        """
        **LLM Docstring**

        Format a block, entering its requested context while preparing the body and then emitting the environment text.

        :param context: active `TeXContextManager` or context name used while formatting
        :type context: object
        :return: formatted TeX source
        :rtype: str
        """
        if self.ctx is not None:
            if context is None:
                context = TeXContextManager.resolve()
            elif isinstance(context, str):
                context = TeXContextManager.resolve(context)

        if self.ctx is not None:
            with context.subcontext(self.ctx):
                body_args = self.prep_body(context)
        else:
            body_args = self.prep_body(context)
        return self.format_body(body_args)
    def __call__(self, body):
        """
        **LLM Docstring**

        Clone the block configuration around a replacement body.

        :param body: content to format or wrap
        :type body: object
        :return: new symbolic or wrapper object
        :rtype: object
        """
        return type(self)(
            body,
            tag=self.tag,
            modifier=self.modifier,
            modifier_type=self.modifier_type,
            separator=self.separator,
            context=self.ctx,
            label=self.label
        )

class TeXRow(TeXBlock):
    tag = None
    separator = ' '

class TeXArray(TeXBlock):
    tag = 'tabular'
    modifier_type = '{}'
    separator = '\n'
    array_separator = " & "
    array_newline = " \\\\\n"
    header_separator = "\n\\hline \\\\[-4ex]\n"
    header_lines = "\n\\hline \\\\[-4ex]"
    footer_lines = "\\hline \\\\[-4ex]\n"
    number_format = "{:8.3f}"
    def __init__(self, headers_or_body, body=None, *,
                 alignment='auto',
                 number_format="{:8.3f}",
                 content_join=None,
                 column_join=None,
                 row_join=None,
                 separator=None,
                 header_spans=None,
                 header_alignments=None,
                 resizeable=False,
                 **opts):
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
        self.resizeable = resizeable
        if resizeable:
            self.tag = 'tabularx'
            self.modifier_type = ["{}", "{}"]
            self.array_separator = " && "

        if body is None:
            body = headers_or_body
            headers_or_body = None
        self.headers = headers_or_body
        self.alignment = alignment
        if content_join is None:
            content_join = self.header_separator
        opts['content_join'] = content_join
        if row_join is None:
            row_join = self.array_newline
        opts['row_join'] = row_join
        if column_join is None:
            column_join = self.array_separator
        opts['column_join'] = column_join
        if separator is None:
            separator = ""
        opts['separator'] = separator
        self.format_opts, opts = dev.OptionsSet(opts).split(TableFormatter)
        self.format = number_format
        self.header_spans = header_spans
        self.header_alignments = header_alignments
        super().__init__(
            body,
            **opts
        )

    def construct_alignment_spec(self, body):
        """
        **LLM Docstring**

        Infer one TeX alignment code per column, using centered columns for nonnumeric content and right alignment otherwise.

        :param body: content to format or wrap
        :type body: object
        :return: one-character alignment specification per column
        :rtype: str
        """
        if isinstance(body, np.ndarray):
            if np.issubdtype(body.dtype, np.integer):
                spec = "c" * body.shape[1]
            elif np.issubdtype(body.dtype, np.floating):
                spec = 'r' * body.shape[1]
            else:
                spec = 'c' * body.shape[1]
        else:
            specs = []
            for array_row in body:
                for i, e in enumerate(array_row):
                    if i >= len(specs):
                        specs = specs + ['r']
                    if (
                            specs[i] != 'c' and
                            not isinstance(e, (float, np.floating)) and
                            not (isinstance(e, str) and len(e.strip()) == 0)
                    ):
                        specs[i] = 'c'
            spec = "".join(specs)
        return spec
    def construct_header_footer(self):
        """
        **LLM Docstring**

        Build the `tabular` or `tabularx` delimiters, inferred alignment specification, and horizontal-rule decorations.
        :return: decorated environment opener and closer
        :rtype: tuple[str, str]
        """
        body = self.body
        if isinstance(body, np.ndarray) and not np.issubdtype(body.dtype, (np.integer, np.floating)):
            body = body.tolist()
        if self.alignment is not None and self.modifier is None:
            mod = self.construct_alignment_spec(body)
        else:
            mod = self.modifier
        if self.resizeable:
            mod = ['\\textwidth', "X".join(mod)]
        header, footer = self.construct_modified_tag(self.tag, mod, self.modifier_type)
        return header + self.header_lines, self.footer_lines + footer

    def format_numpy_array(self, array):
        """
        **LLM Docstring**

        Render a numeric array with `numpy.savetxt`, choosing field width from the largest magnitude and configured decimal precision.

        :param array: NumPy array to serialize as TeX table rows
        :type array: object
        :return: formatted TeX source
        :rtype: str
        """
        int_digits = int(np.floor(np.log10(np.max(np.abs(array))))) + 1
        with io.StringIO() as stream:
            if np.issubdtype(array.dtype, np.floating):
                real_digits = self.real_digits
            else:
                real_digits = 0
            total_digits = int_digits + real_digits + 2
            fmt = '%{}.{}f'.format(total_digits, real_digits)
            np.savetxt(stream, array, fmt=fmt, delimiter=self.array_separator, newline=self.array_newline)
            stream.seek(0)
            return stream.read()
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
        row_padding = []
        string_array = []
        for array_row in array: # convert and track padding
            conv_row = []
            for i,c in enumerate(array_row):
                s = self.dispatch_format(c, context)
                conv_row.append(s)
                if i >= len(row_padding):
                    row_padding = row_padding + [0]
                if len(s) > row_padding[i]:
                    row_padding[i] = len(s)
            string_array.append(conv_row)
        return self.array_newline.join(
            self.array_separator.join(" " * (row_padding[i] - len(s)) + s for i,s in enumerate(string_row))
            for string_row in string_array
        )
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
        if body is None:
            body = self.body
        if headers is None:
            headers = self.headers
        if headers is None:
            if len(body) == 2 and not all(dev.is_atomic(b) for b in body[0]):
                headers, body = body
        opts = self.format_opts
        if 'column_formats' in opts:
            opts = opts.copy()
            column_formats = opts.pop('column_formats')
        else:
            column_formats = [
                ""
                    if not nput.is_numeric(o) else
                "{:>.0f}"
                    if nput.is_int(o) else
                self.format
                for o in body[0]
            ]

        if headers is not None:
            if dev.is_list_like(headers[0]):
                headers = [
                    [
                        h.format_tex(context=context)
                        if isinstance(h, TeXWriter) else
                        h
                        for h in hl
                    ]
                    for hl in headers
                ]
                if self.header_spans is not None:
                    alignments = self.header_alignments
                    if alignments is None:
                        alignments = [
                            ["c"] * len(hl)
                            for hl in headers
                        ]

                    _blocks = []
                    for lhl, lhs, lhc in zip(headers, self.header_spans, alignments):
                        _ = []
                        for hl, hs, hc in zip(lhl, lhs, lhc):
                            _.append(
                                TeXMulticolumn(2*hs - 1, hc, hl).format_tex(context)
                                    if hs > 1 else
                                hl
                            )
                        _blocks.append(_)
                    headers = _blocks
            else:
                headers = [
                    h.format_tex(context=context)
                        if isinstance(h, TeXWriter) else
                    h
                    for h in headers
                ]
                if self.header_spans is not None:
                    alignments = self.header_alignments
                    if alignments is None:
                        alignments = ["c"] * len(headers)

                    _ = []
                    for hl, hs, hc in zip(headers, self.header_spans, alignments):
                        _.append(
                            TeXMulticolumn(hs, hc, hl).format_tex(context)
                                if hs > 1 else
                            hl
                        )
                    headers = _

        wtf = TableFormatter(
            column_formats,
            headers=headers,
            header_spans=self.header_spans,
            **self.format_opts
        ).format(body) + self.array_newline.strip()
        return [
            wtf
        ]

class TeXTable(TeXBlock):
    tag = 'table'
    modifier = 'ht'
    modifier_type = '[]'
    separator = '\n'
    # array_separator = " & "
    # array_newline = " \\\\\n"
    def __init__(self,
                 headers_or_body,
                 body=None,
                 width=1,
                 caption=None,
                 # label=None,
                 resizeable=False,
                 number_format=None,
                 header_spans=None,
                 **etc
                 ):
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
        if body is None:
            body = headers_or_body
            headers_or_body = None
        body = [
            TeXArray(headers_or_body, body,
                     number_format=number_format,
                     resizeable=resizeable,
                     header_spans=header_spans
                     )
                if not isinstance(body, TeXWriter) else
            body
        ]
        self.width = width
        self.caption = caption
        # self.label = label
        super().__init__(body, **etc)

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
        if body is None:
            body = self.body

        base = [
            TeXBlock(
                TeXBlock(
                    body,
                    tag='minipage',
                    modifier_type=["[]", "{}"],
                    modifier=['c', f'{self.width} \\textwidth']
                ),
                tag="center"
            )
        ]
        if self.caption is not None:
            base.append(
                TeXFunction(self.caption, function_name="caption")
                    if not isinstance(self.caption, TeXWriter) else
                self.caption
            )
        if self.label is not None:
            base.append(
                TeXFunction(self.label, function_name="label")
                    if not isinstance(self.label, TeXWriter) else
                self.label
            )
        return [
            b.format_tex(context=context)
            for b in base
        ]

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
        if function_name is None:
            function_name = self.function_name
        self.function_name = function_name
        self.args = args
    def format_tex(self, context=None):
        """
        **LLM Docstring**

        Emit a TeX command followed by each dispatched argument enclosed in braces.

        :param context: active `TeXContextManager` or context name used while formatting
        :type context: object
        :return: formatted TeX source
        :rtype: str
        """
        tag = "\\" + self.function_name
        body = ["{" + self.dispatch_format(b, context) + "}" for b in self.args]
        return tag + "".join(body)

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
        super().__init__(width, fmt, body)

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
        self.body = body
        if brackets is None:
            brackets = self.brackets
        self.brackets = brackets
    def format_tex(self, context=None):
        """
        **LLM Docstring**

        Dispatch the wrapped body and surround it with the configured TeX delimiters.

        :param context: active `TeXContextManager` or context name used while formatting
        :type context: object
        :return: formatted TeX source
        :rtype: str
        """
        l, r = self.brackets
        base = self.dispatch_format(self.body, context)
        return l + base + r

class TeXParenthesized(TeXBracketed):
    brackets = ('\\left(', '\\right)')

class TeXEquation(TeXBlock):
    tag = 'equation'
    context = MathContext
    label_header = 'eq'

########################################################################################################################
#
#       TeX Equations
#
#

#region Equations
class TeXNode(Abstract.Expr):
    def to_ast(self):
        """
        **LLM Docstring**

        Reject AST conversion because TeX-only symbolic nodes are formatting constructs, not executable expressions.
        :return: `None`; the operation mutates state, writes output, or raises by design.
        :rtype: None
        """
        raise NotImplementedError("TeXNodes are for formatting only")
class TeXSuperscript(TeXNode):
    __tag__ = "Superscript"
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
        self.obj = obj
        self.index = index
class TeXApply(TeXNode):
    __tag__ = "Apply"
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
        self.function = function
        self.argument = argument
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
        return TeXApply(self, args)

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
        if isinstance(s, str) and len(s) > 1:
            s = "\\" + s
        return cls(Abstract.Name(s))
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
        if isinstance(s, str) and len(s) > 1:
            s = "\\" + s
        return cls(TeXSymbol(s))

    # a, b, c, f, g, i, j, k, l, m, n, x, y, z = Abstract.vars(
    #     'a', 'b', 'c', 'f', 'g', 'i', 'j', 'k', 'l', 'm', 'n',
    #     'x', 'y', 'z'
    # )
    # omega, nu, tau, psi, phi, sigma = Abstract.vars(
    #     '\\omega', '\\nu', '\\tau', '\\psi', '\\phi', '\\sigma'
    # )
    # Omega, Nu, Tau, Psi, Phi, Sigma = Abstract.vars(
    #     '\\Omega', '\\Nu', '\\Tau', '\\Psi', '\\Phi', '\\Sigma'
    # )
    # sum, int, prod, bra, ket, braket = Abstract.vars(
    #     '\\sum', '\\int', '\\prod',
    #     '\\bra', '\\ket', '\\braket',
    #     symbol_type=TeXSymbol
    # )

    def __init__(self, body):
        """
        **LLM Docstring**

        Initialize `TeXExpr` state from the supplied configuration.

        :param body: content to format or wrap
        :type body: object
        :return: `None`; the operation mutates state, writes output, or raises by design.
        :rtype: None
        """
        if not isinstance(body, Abstract.Expr):
            body = Abstract.Name(body)
        self.body = body
    def __add__(self, other):
        """
        **LLM Docstring**

        Build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating the current expression.

        :param other: right-hand operand
        :type other: object
        :return: new symbolic or wrapper object
        :rtype: object
        """
        if isinstance(other, TeXExpr):
            other = other.body
        return type(self)(self.body + other)
    def __radd__(self, other):
        """
        **LLM Docstring**

        Build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating the current expression.

        :param other: right-hand operand
        :type other: object
        :return: new symbolic or wrapper object
        :rtype: object
        """
        return type(self)(other + self.body)
    def __mul__(self, other):
        """
        **LLM Docstring**

        Build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating the current expression.

        :param other: right-hand operand
        :type other: object
        :return: new symbolic or wrapper object
        :rtype: object
        """
        if isinstance(other, TeXExpr):
            other = other.body
        return type(self)(self.body * other)
    def __rmul__(self, other):
        """
        **LLM Docstring**

        Build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating the current expression.

        :param other: right-hand operand
        :type other: object
        :return: new symbolic or wrapper object
        :rtype: object
        """
        return type(self)(other * self.body)
    def __pow__(self, other):
        """
        **LLM Docstring**

        Build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating the current expression.

        :param other: right-hand operand
        :type other: object
        :return: new symbolic or wrapper object
        :rtype: object
        """
        if isinstance(other, TeXExpr):
            other = other.body
        return type(self)(self.body ** other)
    def __neg__(self):
        """
        **LLM Docstring**

        Build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating the current expression.
        :return: new symbolic or wrapper object
        :rtype: object
        """
        return type(self)(-self.body)
    def __xor__(self, other):
        """
        **LLM Docstring**

        Build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating the current expression.

        :param other: right-hand operand
        :type other: object
        :return: new symbolic or wrapper object
        :rtype: object
        """
        if isinstance(other, TeXExpr):
            other = other.body
        return type(self)(self.body ^ other)
    def __or__(self, other):
        """
        **LLM Docstring**

        Build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating the current expression.

        :param other: right-hand operand
        :type other: object
        :return: new symbolic or wrapper object
        :rtype: object
        """
        if isinstance(other, TeXExpr):
            other = other.body
        return type(self)(self.body | other)
    def __getitem__(self, item):
        """
        **LLM Docstring**

        Build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating the current expression.

        :param item: subscript or slice
        :type item: object
        :return: new symbolic or wrapper object
        :rtype: object
        """
        return type(self)(self.body[item])

    def Equals(self, other):
        """
        **LLM Docstring**

        Build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating the current expression.

        :param other: right-hand operand
        :type other: object
        :return: build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating the current expression
        :rtype: object
        """
        if isinstance(other, TeXExpr):
            other = other.body
        return type(self)(self.body.Equals(other))
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
        if isinstance(other, TeXExpr):
            other = other.body
        return type(self)(self.body.LessThan(other))
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
        if isinstance(other, TeXExpr):
            other = other.body
        return type(self)(self.body.LessEquals(other))
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
        if isinstance(other, TeXExpr):
            other = other.body
        return type(self)(self.body.GreaterThan(other))
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
        if isinstance(other, TeXExpr):
            other = other.body
        return type(self)(self.body.GreaterEquals(other))
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
        name = name.name
        if hasattr(name, 'format_tex'):
            name = name.format_tex()
        return name
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
        return const.value
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
        return "{}({})".format(
            converter(call.fn),
            ",".join(converter(k) for k in call.args)
        )
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
        return "{}^{{{}}}".format(
            converter(op.obj),
            converter(op.index)
        )
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
        return "{}^{{{}}}".format(
            converter(op.left),
            converter(op.right)
        )
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
        return "{}^{{{}}}".format(
            converter(op.left),
            converter(op.right)
        )
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
        idx = op.index
        if isinstance(idx, slice):
            var = idx.start
            min = idx.stop
            max = idx.step
            if max is None:
                return "{}_{{{}={}}}".format(
                    converter(op.obj),
                    converter(var),
                    converter(min)
                )
            else:
                return "{}_{{{}={}}}^{{{}}}".format(
                    converter(op.obj),
                    converter(var),
                    converter(min),
                    converter(max)
                )
        else:
            return "{}_{{{}}}".format(
                converter(op.obj),
                converter(op.index)
            )
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
        return "{}+{}".format(
            converter(op.left),
            converter(op.right)
        )
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
        return "{}-{}".format(
            converter(op.left),
            converter(op.right)
        )
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
        return "{} {}".format(
            converter(op.left),
            converter(op.right)
        )
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
        return "{} {}".format(
            converter(op.left),
            converter(op.right)
        )
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
        return "\\frac{{{}}{{{}}}".format(
            converter(op.left),
            converter(op.right)
        )
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
        return "{} = {}".format(
            converter(op.left),
            converter(op.right)
        )
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
        if hasattr(obj, 'format_tex'):
            return obj.format_tex()
        else:
            return TeXBlock(obj, separator=", ").format_tex()

    @property
    def converter_dispatch(self):
        """
        **LLM Docstring**

        Return the mapping from symbolic node tags to TeX conversion functions, including a raw fallback.
        :return: symbolic-node conversion dispatch table
        :rtype: dict
        """
        return {
            'Name':self.convert_name,
            'Const':self.convert_const,
            'Superscript':self.convert_superscript,
            'Subscript':self.convert_subscript,
            'Pow':self.convert_power,
            'BitXOr':self.convert_bitxor,
            'BitOr':self.convert_bitor,
            'Add':self.convert_add,
            'Sub':self.convert_sub,
            'Mul':self.convert_mul,
            'Div':self.convert_div,
            'Equals':self.convert_eq,
            None:self.convert_raw
        }

    def format_tex(self, context=None):
        """
        **LLM Docstring**

        Transmogrify the symbolic expression through TeX converters and add dollar delimiters only outside existing math mode.

        :param context: active `TeXContextManager` or context name used while formatting
        :type context: object
        :return: formatted TeX source
        :rtype: str
        """
        if context is None:
            context = TeXContextManager.resolve()
        elif isinstance(context, str):
            context = TeXContextManager.resolve(context)

        pad_dollars = not context.math_mode
        with context.subcontext(MathContext):
            expr = self.body.transmogrify(
                self.converter_dispatch
            )
        if pad_dollars:
            expr = '${}$'.format(expr)

        return expr

#endregion

########################################################################################################################
#
#       Wrapper
#
#

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
        return cls.wrap_parens(cls.Array(mat, **kwargs))

class TeXImportGraph:
    import_heads = ("input", "import", "module", "loadsec", "loadfig", "loadtab")
    def __init__(self, tex_root,
                 root_dir=None,
                 head_parser=None,
                 import_heads=None,
                 strip_comments=True,
                 aliases=None,
                 ignored_files=None,
                 **parser_options
                 ):
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
        if root_dir is None:
            root_dir = os.path.dirname(tex_root)
        self.root = tex_root
        self.root_dir = root_dir
        self.graph = {}
        self._initialized = False
        if import_heads is None:
            import_heads = self.import_heads
        self.import_heads = import_heads
        if head_parser is None:
            head_parser = self.head_resolver
        self.head_parser = head_parser
        self.strip_comments = strip_comments
        self.aliases = aliases
        self.parser_options = parser_options

    @classmethod
    def import_parser(cls, head:str, tag:str):
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
        return tag.partition(head)[2].strip("{}").strip()+".tex", {}
    @classmethod
    def head_resolver(cls, tag:str):
        """
        **LLM Docstring**

        Extract a TeX command head by removing the leading backslash and truncating before optional or required arguments.

        :param tag: TeX environment or command tag
        :type tag: str
        :return: normalized TeX command head
        :rtype: str
        """
        return tag.strip()[1:].partition("{")[0].partition("[")[0]
    module_root = "sections"
    @classmethod
    def load_module_parser(cls, tag:str):
        """
        **LLM Docstring**

        Resolve a module command to `sections/<module>/main.tex` and record the module directory as the new import root.

        :param tag: TeX environment or command tag
        :type tag: str
        :return: module main-file path and nested root option
        :rtype: tuple[str, dict]
        """
        root = tag.partition('module')[2].strip("{}").strip()
        file = os.path.join(cls.module_root, root, "main.tex")
        return file, {'root':os.path.join(cls.module_root, root)}
    @classmethod
    def load_block_parser(cls, head:str, root, tag:str):
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
        filename = tag.partition(head)[2].strip("{}").strip()
        file = os.path.join(root, filename + ".tex")
        ref = head[4:]
        if ref not in {'fig', 'tab', 'eq'}:
            opts = {'header': f'\\label{{{ref}:{filename}}}\n'}
        else:
            opts = {}
        return file, opts
    @classmethod
    def resolve_parser(cls, head:str):
        """
        **LLM Docstring**

        Select the path parser for an import-like TeX command head.

        :param head: TeX command head
        :type head: str
        :return: callable that resolves paths for the command head
        :rtype: callable
        """
        if head == 'module':
            return cls.load_module_parser
        elif head.startswith("load"):
            subhead = head[4:]
            if subhead == 'sec':
                root = 'sections'
            elif subhead == 'fig':
                root = 'figures'
            elif subhead == 'tab':
                root = 'tables'
            else:
                root = subhead
            return functools.partial(cls.load_block_parser, head, root)
        else:
            return functools.partial(cls.import_parser, head)

    ImportNode = collections.namedtuple("ImportNode", ["root_dir", "end_points", "head", "block", "opts"])
    root_dir_var = r"\RootDirectory"
    def _resolve_aliases(self, root_dir):
        """
        **LLM Docstring**

        Build the alias substitution table for a root directory, resolving later aliases against earlier values.

        :param root_dir: directory used to resolve relative TeX imports
        :type root_dir: object
        :return: resolved alias substitution mapping
        :rtype: dict
        """
        base_aliases = {
            self.root_dir_var:root_dir
        }
        if self.aliases is not None:
            for a,v in self.aliases.items()  :
                if not isinstance(v, str):
                    v = v(base_aliases)
                else:
                    for rep_from,rep_to in base_aliases.items():
                        v = v.replace(rep_from, rep_to)
                base_aliases[a] = v
        return base_aliases
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
        imports = {}
        ep, block = parser.parse_tex_call(import_heads, return_end_points=True)
        aliases = self._resolve_aliases(root_dir)
        while block is not None:
            head = self.head_parser(block)
            filename, opts = head_map[head](block)
            for rep_from,rep_to in aliases.items():
                filename = filename.replace(rep_from, rep_to)
            if not filename.startswith("/"):
                file = os.path.join(root_dir, filename)
            else:
                file = filename
            imports[file] = self.ImportNode(root_dir, ep, head, block, opts)
            ep, block = parser.parse_tex_call(import_heads, return_end_points=True)
        return imports
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
        body = re.sub(r"($|^)%.*\n", "", body)
        body = re.sub(r"(?<!\\)%.*\n", "", body)
        return body
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
        if root is None:
            root = self.root
        if import_heads is None:
            import_heads = self.import_heads
        if root_dir is None:
            root_dir = self.root_dir

        if isinstance(import_heads, dict):
            head_map = import_heads
        else:
            head_map = {
                k:self.resolve_parser(k)
                for k in import_heads
            }
        if self.strip_comments:
            with tf.TemporaryFile(mode='w+') as new_root:
                new_body = self.strip_tex_comments(dev.read_file(root))
                new_root.write(new_body)
                new_root.seek(0)
                with Parsers.TeXParser(new_root, **self.parser_options) as parser:
                    imports = self._handle_parse_block(parser, head_map, import_heads, root_dir)
        else:
            with Parsers.TeXParser(root, **self.parser_options) as parser:
                imports = self._handle_parse_block(parser, head_map, import_heads, root_dir)
        return imports

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
        if root_dir is None:
            root_dir = self.root_dir
        if not self._initialized:
            self._initialized = True
            queue = collections.deque([(self.root, root_dir)])
            while queue:
                root, root_dir = queue.pop()
                new_imports = self.find_imports(root, import_heads=import_heads, root_dir=root_dir)
                new_imports = {
                    file: node
                    for file, node in new_imports.items()
                    if file not in self.graph
                }
                clean_imports = {}
                for file,node in new_imports.items():
                    if not os.path.isfile(file):
                        if self.verbose:
                            print(f"IGNORING MISSING FILE: {file}")
                    else:
                        clean_imports[file] = node
                new_imports = clean_imports
                self.graph[root] = new_imports
                for file, node in new_imports.items():
                    subroot = node.opts.get('root')
                    if subroot is not None:
                        subdir = os.path.join(root_dir, subroot)
                    else:
                        subdir = root_dir
                    queue.append((file, subdir))

        return self.graph

class TeXTranspiler:
    def __init__(self,
                 tex_root,
                 root_dir=None,
                 figure_renaming_function=None,
                 bib_renaming_function=None,
                 strip_comments=True,
                 figures_path=None,
                 figure_merge_function=None,
                 bib_path=None,
                 bib_merge_function=None,
                 bib_cleanup_function=None,
                 citation_renaming_function=None,
                 aliases=None,
                 styles_path=None,
                 parser_options=None
                 ):
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
        if parser_options is None:
            parser_options = {}
        self.graph = TeXImportGraph(tex_root,
                                    root_dir=root_dir,
                                    strip_comments=strip_comments,
                                    aliases=aliases,
                                    **parser_options
                                    )
        self.figure_renaming_function = figure_renaming_function
        self.figures_path = figures_path
        self.figure_merge_function = figure_merge_function
        self.bib_renaming_function = bib_renaming_function
        self.bib_path = bib_path
        self.bib_merge_function = bib_merge_function
        self.bib_cleanup_function = bib_cleanup_function
        self.citation_renaming_function = citation_renaming_function
        self.styles_path = styles_path
        self.parser_options = parser_options

    @classmethod
    def figure_counter(cls, name_root="Figure", start_at=1):
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
        counter = itertools.count()
        for _ in range(start_at):
            next(counter)
        return lambda fig: f"{name_root}{next(counter)}" + os.path.splitext(fig)[1]

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
        bib_bodies = []
        for b in bib_list:
            if not os.path.isfile(b) and os.path.splitext(b)[-1] == "":
                b = b + ".bib"
            bib_bodies.append(dev.read_file(b))
        body = "\n\n".join(bib_bodies)
        with tf.NamedTemporaryFile('w+', delete=False) as temp:
            temp.write(body)
        return temp.name, True

    @classmethod
    def pruned_bib(cls, bib_file_or_filter,  cites=None, *, filter=None, **parser_options):
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
        if filter is None and cites is None:
            def prune_bib(bib_file, cites):
                """
                **LLM Docstring**

                Invoke `pruned_bib` with the captured citation filter so the selected bibliography file is rewritten in place.

                :param bib_file: BibTeX file rewritten in place
                :type bib_file: object
                :param cites: parsed citation map
                :type cites: object
                :return: result of pruning the supplied bibliography in place
                :rtype: None
                """
                return cls.pruned_bib(bib_file, cites=cites, filter=bib_file_or_filter, **parser_options)
            return prune_bib
        else:
            bib_file = bib_file_or_filter

            if filter is not None:
                cites = filter(cites)

            allowed_cites = {
                r
                for label in cites.values()
                for r in label.ref
            }

            blocks = []
            with Parsers.BibTeXParser(bib_file, **parser_options) as parser:
                (s, e), text = parser.parse_bib_item(return_end_points=True)
                while text is not None:
                    keys = parser.parse_bib_body(text, parse_lines=False)
                    if keys['key'] in allowed_cites:
                        blocks.append(text)
                    (s, e), text = parser.parse_bib_item(return_end_points=True)


            dev.write_file(bib_file, "\n\n".join(blocks))

    @classmethod
    def get_injection_body(cls, root_dir, node_data:TeXImportGraph.ImportNode, body:str):
        # here to be overridden
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
        if root_dir is not None:
            root = dev.drop_directory_prefix(root_dir, node_data.root_dir)
        else:
            root = node_data.root_dir
        if len(root) > 0 and not root.endswith("/"):
            root = root + "/"
        body = (
            node_data.opts.get('header', "")
            + body.replace("\\RootDirectory/", root)
            + node_data.opts.get('footer', "")
        )
        return node_data.end_points, body

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
        chunks = []
        split_point = 0
        if hasattr(edits, 'items'):
            edits = edits.items()
        clean_edits = [
            normalization_function(node_data, body)
                if normalization_function is not None else
            (node_data, body)
            for node_data, body in edits
        ]
        for (s,e), body in sorted(clean_edits, key=lambda se: se[0][0]):
            s = s - split_point
            start_chunk = cur_text[:s]
            chunks.append(start_chunk)
            chunks.append(body)
            if e > 0:
                e = e - split_point
                cur_text = cur_text[e:]
                split_point = split_point + e
            else:
                cur_text = ""
        chunks.append(cur_text)

        return "".join(chunks)

    @classmethod
    def flatten_import_graph(cls,
                             graph:dict[str, dict[str, TeXImportGraph.ImportNode]],
                             root,
                             cache=None,
                             root_dir=None,
                             strip_comments=False
                             ):
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
        if cache is None:
            cache = {}
        if root in cache:
            return cache[root]

        cache[root] = None # to break cycles

        edits = []
        for file,node_data in graph[root].items():
            if file not in cache:
                cache[file] = cls.flatten_import_graph(graph, file, cache=cache, root_dir=root_dir, strip_comments=strip_comments)
            edits.append([node_data, cache[file]])

        cur_text = dev.read_file(root)
        if strip_comments:
            cur_text = TeXImportGraph.strip_tex_comments(cur_text)
        edit_block = cls.apply_body_edit(
            cur_text, edits,
            normalization_function=lambda node_data, body:cls.get_injection_body(root_dir, node_data, body)
        )

        cache[root] = edit_block

        return cache[root]

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
        blocks = None
        if os.path.isfile(flat_tex):
            temp_tex = flat_tex
            flat_tex = dev.read_file(flat_tex)
            if self.graph.strip_comments:
                flat_tex = TeXImportGraph.strip_tex_comments(flat_tex)
            else:
                with Parsers.TeXParser(temp_tex) as parser:
                    ep, block = parser.parse_tex_call(call_head, return_end_points=True)
                    while block is not None:
                        blocks[ep] = block
                        ep, block = parser.parse_tex_call(call_head, return_end_points=True)

        if blocks is None:
            with tf.TemporaryFile(mode="w+") as temp_tex:
                temp_tex.write(flat_tex)
                temp_tex.seek(0)
                with Parsers.TeXParser(temp_tex) as parser:
                    blocks = {}
                    ep, block = parser.parse_tex_call(call_head, return_end_points=True)
                    while block is not None:
                        blocks[ep] = block
                        ep, block = parser.parse_tex_call(call_head, return_end_points=True)

        filenames = [ file_parser(v) for v in blocks.values() ]

        if replacement_path is not None:
            repathing = functools.partial(self._repath_resource, replacement_path)
            if renaming_function is None:
                renaming_function = repathing
            else:
                renaming_function = lambda figure, _renaming=renaming_function : repathing(figure, _renaming)

        if renaming_function is not None:
            filenames = {
                k: renaming_function(k)
                for k in filenames
            }
            flat_tex = self.apply_body_edit(
                flat_tex, blocks,
                normalization_function=lambda edit_pos, body: (
                    edit_pos,
                    self._modify_resource_path(body, filenames)
                )
            )

        return flat_tex, filenames

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
        if isinstance(figure_path, str):
            if renaming_function is not None:
                basename = renaming_function(figure_path)
            else:
                basename = os.path.basename(figure_path)
            return os.path.join(new_root, basename)
        else:
            if renaming_function is not None:
                figure_path = renaming_function(figure_path)
                if isinstance(figure_path, str):
                    return os.path.join(new_root, figure_path)
            return ",".join(cls._repath_resource(new_root, fp) for fp in figure_path)
    @classmethod
    def _parse_graphics_file(cls, tag:str):
        """
        **LLM Docstring**

        Parse the matched TeX command into its command head, resource or reference type, and normalized payload.

        :param tag: TeX environment or command tag
        :type tag: str
        :return: single resource path or tuple of paths
        :rtype: str | tuple[str, ...]
        """
        files = tuple(s.strip() for s in tag.partition("{")[-1].partition("}")[0].split(","))
        if len(files) == 1:
            files = files[0]
        return files
    @classmethod
    def _modify_resource_path(cls, tag:str, file_map):
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
        head, _, path = tag.partition("{")
        name, _, rest = path.partition("}")
        names = tuple(s.strip() for s in name.split(","))
        if len(names) == 1:
            names = names[0]
        return head + "{" + file_map[names] + "}" + rest
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
        if figures_path is None:
            figures_path = self.figures_path
        return self.remap_block(flat_tex, "includegraphics", self._parse_graphics_file,
                                replacement_path=figures_path,
                                renaming_function=self.figure_renaming_function)

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
        if bib_path is None:
            bib_path = self.bib_path
        return self.remap_block(flat_tex, "bibliography",
                                self._parse_graphics_file,
                                replacement_path=bib_path,
                                renaming_function=self.bib_renaming_function)

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
        if styles_path is None:
            styles_path = self.styles_path
        flat_tex, classes = self.remap_block(flat_tex,
                                "documentclass",
                                self._parse_graphics_file,
                                replacement_path=styles_path)
        classes = [os.path.splitext(c)[0]+".cls" for c in classes]

        flat_tex, bib_styles = self.remap_block(flat_tex,
                                "bibliographystyle",
                                self._parse_graphics_file,
                                replacement_path=styles_path)
        bib_styles = [os.path.splitext(c)[0]+".bst" for c in bib_styles]
        return flat_tex, (classes + bib_styles)


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
        blocks = {}
        with dev.StreamInterface(tex_stream, file_backed=True) as stream:
            with Parsers.TeXParser(stream) as parser:
                ep, block = parser.parse_tex_call(tags, return_end_points=True)
                while block is not None:
                    blocks[ep] = block
                    ep, block = parser.parse_tex_call(tags, return_end_points=True)

        return blocks
    @classmethod
    def _parse_label_ref(cls, l:str):
        """
        **LLM Docstring**

        Parse the matched TeX command into its command head, resource or reference type, and normalized payload.

        :param l: raw TeX label/reference command text
        :type l: str
        :return: command head, label type, and label identifier
        :rtype: tuple[str, str, str]
        """
        head, _, tag = l.partition('{')
        tag_type, _, tag_ref = tag.partition('}')[0].partition(":")
        head = head.strip("\\").partition("[")[0]
        return head, tag_type.strip(), tag_ref.strip()
    LabelBlock = collections.namedtuple("LabelBlock", ["tag", "ref", "end_points", "head", "block"])
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
        maps = {}
        for ep, l in cls.get_call_list(tex_stream, call_tags).items():
            head, tag_type, tag_ref = block_parser(l)
            if len(tag_ref) == 0:
                tag_type, tag_ref = None, tag_type
            if tag_type not in maps:
                maps[tag_type] = {}
            maps[tag_type][ep] = cls.LabelBlock(tag_type, tag_ref, ep, head, l)
        return maps
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
        return cls.create_label_block_map(tex_stream, 'label', cls._parse_label_ref)

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
        refs = l.split('{')
        head, refs = refs[0], refs[1:]
        head = head.strip("\\").partition("[")[0]
        refs = [r.partition("}")[0] for r in refs]
        if ":" in refs[0]:
            tag_type, _, tag_ref = [r.strip() for r in refs[0].partition(":")]
        else:
            tag_type = head[3:]
            if head.endswith("s"):
                tag_type = tag_type[:-1]
                tag_ref = {'refs':refs, 'type':'pair'}
            elif head.endswith('rng'):
                tag_type = tag_type[:-3]
                tag_ref = {'refs':refs, 'type':'range'}
            else:
                tag_ref = refs[0]
        return head, tag_type, tag_ref
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
        return cls.create_label_block_map(tex_stream,
                                          ('ref',
                                           'reffig', 'reftab', 'refeq', 'refsec',
                                           'reffigs', 'reftabs', 'refeqs', 'refsecs',
                                           'reffigrng', 'reftabrng', 'refeqrng', 'refsecrng',
                                           ),
                                          cls._parse_ref_ref)

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
        head, _, body = l.partition('{')
        head = head.strip("\\").partition("[")[0]
        cites = [s.strip() for s in body.partition("}")[0].split(",")]
        return head, "cite", cites
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
        return cls.create_label_block_map(tex_stream,
                                          'cite',
                                          cls._parse_cite_ref)
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
        if cite_map is None:
            cite_map = cls.create_cite_map(tex_stream)
        edits = ref_handler(cite_map)
        return cls.apply_body_edit(tex_stream, edits)

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
        return {
            eps:f"\\{label.head}" + "{" + ",".join(renaming(l) for l in label.refs) + "}"
            for eps,label in citations.items()
        }
    def remap_citations(self, flat_tex, si_tex:dict[str,str]=None, citation_renaming_function=None):
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
        citations = self.create_cite_map(flat_tex)
        if si_tex is not None:
            for name,tex in si_tex.items():
                citations = dev.merge_dicts(citations, self.create_cite_map(tex))
        if len(citations) > 0:
            citations = citations['cite']
            if citation_renaming_function is not None:
                citation_renaming_function = self.citation_renaming_function
            if citation_renaming_function is not None:
                flat_tex = self.remap_citation_set(flat_tex,
                                                   lambda cites:self._rename_cites(cites, citation_renaming_function),
                                                   citations)
        return flat_tex, citations

    ref_tag_map = {
        'sec': ("Sec.", "Secs."),
        'fig': ("Fig.", "Figs."),
        'tab': ("Table", "Tables"),
        'eq': ("Eq.", "Eqs.")
    }
    ref_label_formats = {
        'single': "{tag} {index}",
        'pair': "{tag} {index[0]} and {index[1]}",
        'range': "{tag} {index[0]}-{index[1]}",
    }
    si_ref_format = "S{i}"
    main_ref_format = "ref{{{ref}}}"
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
        if isinstance(label.ref, str):
            if (head, label.ref) in si_index_map:
                return cls.ref_label_formats['single'].format(
                    tag=cls.ref_tag_map[head][0],
                    index=cls.si_ref_format.format(i=si_index_map[(head, label.ref)] + 1)
                )
            else:
                return None
        else:
            if any((head, r) in si_index_map for r in label.ref['refs']):
                fmt = cls.ref_label_formats[label.ref['type']]
                tag = cls.ref_tag_map[head][1]
                index = [
                    cls.si_ref_format.format(i=si_index_map[(head, r)] + 1)
                        if (head, r) in si_index_map else
                    cls.main_ref_format.format(r)
                    for r in label.ref['refs']
                ]
                return fmt.format(tag=tag, index=index)
            else:
                return None

    @classmethod
    def figure_table_remapping(cls, si_labels:dict[str, dict[tuple[int, int], LabelBlock]], label_function=None):
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
        si_ref_map = {}
        for head, labels in si_labels.items():
            for index,(_, label) in enumerate(labels.items()):
                si_ref_map[(head, label.ref)] = index

        if label_function is None:
            label_function = cls.ref_remapping_label

        def handle_refs(ref_map:dict[str, dict[tuple[int, int], cls.LabelBlock]]):
            """
            **LLM Docstring**

            Walk parsed references and emit replacements only for labels that resolve into the supplementary-document index map.

            :param ref_map: precomputed reference map
            :type ref_map: dict[str, dict[tuple[int, int], cls.LabelBlock]]
            :return: endpoint-to-replacement mapping for supplementary references
            :rtype: dict
            """
            edits = {}
            for head, labels in ref_map.items():
                for eps, label in labels.items():
                    label = label_function(head, label, si_ref_map)
                    if label is not None:
                        edits[eps] = label
            return edits
        return handle_refs
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
        if ref_map is None:
            ref_map = cls.create_ref_map(tex_stream)
        edits = ref_handler(ref_map)
        return cls.apply_body_edit(tex_stream, edits)

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
        si_docs = {}
        for ep, l in cls.get_call_list(flat_tex, cls.si_doc_labels).items():
            doc_name = l.partition("{")[-1].partition("}")[0].strip()
            si_docs[doc_name] = ep
        return si_docs

    def remap_si(self, flat_tex):
        """
        **LLM Docstring**

        Rewrite the corresponding TeX resource or reference commands and return the updated source together with mapping metadata where applicable.

        :param flat_tex: flattened TeX source or path to it
        :type flat_tex: object
        :return: rewritten TeX source and any associated mapping metadata
        :rtype: object
        """
        docs = self.find_si_documents(flat_tex)
        flat_docs = {
            t:type(self)(
                os.path.join(self.graph.root_dir, os.path.splitext(t)[0] + ".tex"),
                root_dir=self.graph.root_dir
            ).create_flat_tex(include_aux=False)
            for t in docs.keys()
        }

        #TODO: infer label style
        si_labels = {}
        for doc in flat_docs.values():
            si_labels = dev.merge_dicts(si_labels, self.create_label_map(doc))

        if len(si_labels) > 0:
            flat_tex = self.apply_body_edit(flat_tex, {e:"" for e in docs.values()})
            flat_tex = self.remap_refs(flat_tex, self.figure_table_remapping(si_labels))

        return flat_tex, flat_docs

    def create_flat_tex(self, include_aux=True):
        """
        **LLM Docstring**

        Flatten imports and optionally remap styles, figures, bibliography, supplementary documents, and citations into an auxiliary manifest.

        :param include_aux: whether resource remapping metadata is returned
        :type include_aux: object
        :return: flattened TeX source, optionally paired with auxiliary metadata
        :rtype: object
        """
        flat_tex = self.flatten_import_graph(
            self.graph.populate_graph(),
            self.graph.root,
            root_dir=self.graph.root_dir,
            strip_comments=self.graph.strip_comments
        )

        if include_aux:
            flat_tex, style_files = self.remap_style_files(flat_tex)
            flat_tex, figure_files = self.remap_figures(flat_tex)
            flat_tex, bib_files = self.remap_bibliography(flat_tex)
            flat_tex, si_tex = self.remap_si(flat_tex)
            flat_tex, cites = self.remap_citations(flat_tex, si_tex)
            # flat_tex = self.remap_si

            aux = {
                'styles':style_files,
                'figures':figure_files,
                'bibliography':bib_files,
                'si':si_tex,
                'citations': cites
            }

            return flat_tex, aux
        else:
            return flat_tex

    @classmethod
    def _copy_inputs(cls, root_dir, target_dir, resource_path, inputs, merge_function,
                     search_paths=None,
                     allow_missing=False,
                     post_processor=None
                     ):
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
        if resource_path is not None:
            fig_dir = os.path.join(target_dir, resource_path)
            os.makedirs(fig_dir, exist_ok=True)
        else:
            fig_dir = target_dir

        if not hasattr(inputs, 'items'):
            inputs = {k:os.path.basename(k) for k in inputs}
        for src, target in inputs.items():
            requires_delete = False
            if not isinstance(target, str):
                if isinstance(src, str):
                    raise ValueError(f"can't map single source file ({src}) to multiple outputs ({target})")
                elif len(src) != len(target):
                    raise ValueError(f"can't map {len(src)} source files to {len(target)} outputs ({src} to {target})")
            elif not isinstance(src, str):
                src, requires_delete = merge_function([os.path.join(root_dir, s) for s in src])
                if not isinstance(src, str):
                    if requires_delete:
                        os.remove(src)
                    raise ValueError(f"can't map non string source ({src}) to {target}")
            else:
                src = os.path.join(root_dir, src)

            if isinstance(src, str):
                src = [src]
                target = [target]
            try:
                for s, d in zip(src, target):
                    if not os.path.isfile(s):
                        if search_paths is not None:
                            s_dir, s_base = os.path.split(s)
                            for p in search_paths:
                                test = os.path.join(s_dir, p, s_base)
                                if os.path.isfile(test):
                                    s = test
                                    break
                    if allow_missing and not os.path.isfile(s):
                        continue
                    targ = os.path.join(fig_dir, d)
                    shutil.copy(s, targ)
                    if post_processor is not None:
                        post_processor(targ)
            finally:
                if requires_delete:
                    for s in src: os.remove(s)


    style_search_paths = ["styles"]
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
        flat_file = self.create_flat_tex(include_aux=include_aux)
        os.makedirs(target_dir, exist_ok=True)
        if include_aux:
            flat_file, aux = flat_file
            if 'styles' in aux:
                self._copy_inputs(self.graph.root_dir, target_dir,
                                  self.styles_path,
                                  aux['styles'],
                                  self.figure_merge_function,
                                  search_paths=self.style_search_paths,
                                  allow_missing=allow_missing_styles
                                  )
            if 'figures' in aux:
                self._copy_inputs(self.graph.root_dir, target_dir, self.figures_path, aux['figures'], self.figure_merge_function)

            if 'citations' in aux:
                if self.bib_cleanup_function is not None:
                    bib_post_processor = lambda file:self.bib_cleanup_function(file, aux['citations'], **self.parser_options)
                else:
                    bib_post_processor = None
                self._copy_inputs(self.graph.root_dir, target_dir, self.bib_path, aux['bibliography'],
                                  self.bib_merge_function,
                                  post_processor=bib_post_processor
                                  )
            if include_si and 'si' in aux:
                for name,flat in aux['si'].items():
                    dev.write_file(os.path.join(target_dir, name+'.tex'), flat)

        os.path.join(target_dir, file_name)
        dev.write_file(os.path.join(target_dir, file_name), flat_file)
        return target_dir

    # @classmethod
    # def condense_bibtex(cls, source_tex):
    #     ...
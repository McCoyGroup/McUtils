"""
Just a simple text table formatter with support for headers, separators, any kind of python formatting spec
etc.
"""
from __future__ import annotations
import string
import numpy as np
from .. import Devutils as dev
__all__ = ['TableFormatter']

class TableFormatter:
    __props__ = ('header_spans', 'header_format', 'column_join', 'row_join', 'header_column_join', 'header_row_join', 'separator', 'separator_lines', 'content_join', 'column_alignments', 'header_alignments', 'row_padding')
    "Real access pattern: TableFormatter.<AttrName> (7 class attributes, e.g. TableFormatter.default_header_format == ''). Collapsed into a dict below purely for compactness -- do not index it as a dict in real code:"
    _MEMBERS = {'default_header_format': '', 'default_column_join': '  ', 'default_row_join': '\n', 'default_separator': '-', 'default_column_alignment': '.', 'default_header_alignment': '^', 'default_row_padding': ''}

    def __init__(self, column_formats, *, headers=None, header_spans=None, header_format=None, column_join=None, row_join=None, header_column_join=None, header_row_join=None, separator=None, separator_lines=1, content_join=None, column_alignments=None, header_alignments=None, row_padding=None):
        """
        **LLM Docstring**

        Initialize `TableFormatter` state from the supplied configuration.

        :param column_formats: per-column formatting specifications
        :type column_formats: object
        :param headers: optional header rows
        :type headers: object
        :param header_spans: column spans for each header cell
        :type header_spans: object
        :param header_format: formatter or formatters applied to header cells
        :type header_format: object
        :param column_join: separator or separator sequence between columns
        :type column_join: object
        :param row_join: separator between rows
        :type row_join: object
        :param header_column_join: separator or separator sequence between header cells
        :type header_column_join: object
        :param header_row_join: separator between header rows
        :type header_row_join: object
        :param separator: header separator character or block separator
        :type separator: object
        :param separator_lines: number of separator rows inserted below headers
        :type separator_lines: object
        :param content_join: separator between header and body
        :type content_join: object
        :param column_alignments: alignment code or codes for body columns
        :type column_alignments: object
        :param header_alignments: alignment codes for header cells
        :type header_alignments: object
        :param row_padding: text prepended to the first formatted column
        :type row_padding: object
        :return: `None`; the operation mutates state, writes output, or raises by design.
        :rtype: None
        """
        ...

    @classmethod
    def prep_input_arrays(cls, headers, data, header_spans):
        """
        **LLM Docstring**

        Normalize headers, spans, and rows to rectangular lists with a shared maximum column count.

        :param headers: optional header rows
        :type headers: object
        :param data: tabular or tree data to process
        :type data: object
        :param header_spans: column spans for each header cell
        :type header_spans: object
        :return: normalized headers, rows, and header spans
        :rtype: tuple
        """
        ...

    @staticmethod
    def _has_template_variables(format_string: str):
        """
        **LLM Docstring**

        Detect whether a format string contains any replacement fields.

        :param format_string: Python format string to inspect
        :type format_string: str
        :return: whether the string contains replacement fields
        :rtype: bool
        """
        ...

    @classmethod
    def custom_formatter(cls, f):
        """
        **LLM Docstring**

        Convert format strings, iterable-format specifications, or callables into objects exposing a `.format` method.

        :param f: string or file path being tested
        :type f: object
        :return: object exposing a `.format` callable
        :rtype: object
        """
        ...

    @classmethod
    def resolve_formatters(cls, ncols, col_formats):
        """
        **LLM Docstring**

        Repeat the supplied formatter sequence cyclically and truncate it to the requested column count.

        :param ncols: number of output columns
        :type ncols: object
        :param col_formats: format specifications to repeat across columns
        :type col_formats: object
        :return: formatter specifications repeated to `ncols` entries
        :rtype: list
        """
        ...

    @classmethod
    def prep_formatters(cls, formats):
        """
        **LLM Docstring**

        Normalize one or more format specifications through `custom_formatter`.

        :param formats: format specifications to normalize
        :type formats: object
        :return: normalized formatter objects
        :rtype: list
        """
        ...

    @classmethod
    def _format_entry(cls, data, fmt, strict=False):
        """
        **LLM Docstring**

        Format one cell, optionally falling back to `str(data)` when non-strict formatting raises `IndexError` or `ValueError`.

        :param data: tabular or tree data to process
        :type data: object
        :param fmt: formatter object or formatting specification
        :type fmt: object
        :param strict: whether formatting errors propagate instead of falling back to `str`
        :type strict: object
        :return: formatted cell text
        :rtype: str
        """
        ...

    @classmethod
    def format_tablular_data_columns(cls, data, formats, row_padding=None, strict=False):
        """
        **LLM Docstring**

        Format row-major data into column-major strings, optionally padding the first column of each row.

        :param data: tabular or tree data to process
        :type data: object
        :param formats: format specifications to normalize
        :type formats: object
        :param row_padding: text prepended to the first formatted column
        :type row_padding: object
        :param strict: whether formatting errors propagate instead of falling back to `str`
        :type strict: object
        :return: column-major formatted strings
        :rtype: list[list[str]]
        """
        ...

    @classmethod
    def align_left(cls, col, width):
        """
        **LLM Docstring**

        Pad each string in a column using left alignment to the requested width.

        :param col: column strings to align
        :type col: object
        :param width: fraction of text width used by the minipage
        :type width: object
        :return: aligned column strings
        :rtype: list[str]
        """
        ...

    @classmethod
    def align_right(cls, col, width):
        """
        **LLM Docstring**

        Pad each string in a column using right alignment to the requested width.

        :param col: column strings to align
        :type col: object
        :param width: fraction of text width used by the minipage
        :type width: object
        :return: aligned column strings
        :rtype: list[str]
        """
        ...

    @classmethod
    def align_center(cls, col, width):
        """
        **LLM Docstring**

        Pad each string in a column using center alignment to the requested width.

        :param col: column strings to align
        :type col: object
        :param width: fraction of text width used by the minipage
        :type width: object
        :return: aligned column strings
        :rtype: list[str]
        """
        ...

    @classmethod
    def align_dot(cls, col, width, dot='.'):
        """
        **LLM Docstring**

        Align strings by their final decimal marker, pad missing fractional widths, and right-align the resulting column.

        :param col: column strings to align
        :type col: object
        :param width: fraction of text width used by the minipage
        :type width: object
        :param dot: marker whose final occurrence is used as the alignment point
        :type dot: object
        :return: aligned column strings
        :rtype: list[str]
        """
        ...
    supported_alignments = {'<': 'align_left', '>': 'align_right', '^': 'align_center', '.': 'align_dot'}

    @classmethod
    def resolve_aligner(cls, alignment):
        ...

    @classmethod
    def align_column(cls, header_data, cols_data, header_alignment, column_alignment, join_widths: list[int], header_widths):
        """
        **LLM Docstring**

        Jointly size a grouped header and its body columns while accounting for inter-column join widths.

        :param header_data: formatted header strings for a grouped column
        :type header_data: object
        :param cols_data: formatted body columns belonging to the group
        :type cols_data: object
        :param header_alignment: alignment code for the grouped header
        :type header_alignment: object
        :param column_alignment: alignment codes for body columns
        :type column_alignment: object
        :param join_widths: width contributions from separators between grouped columns
        :type join_widths: list[int]
        :param header_widths: reserved header widths; accepted for API compatibility
        :type header_widths: object
        :return: aligned column strings
        :rtype: list[str]
        """
        ...

    def format(self, headers_or_table, *table_data, header_format=None, header_spans=None, column_formats=None, column_alignments=None, header_alignments=None, column_join=None, row_join=None, header_column_join=None, header_row_join=None, separator=None, separator_lines=None, content_join=None, row_padding=None, strict=False):
        """
        **LLM Docstring**

        Assemble formatted headers, spanning groups, aligned body columns, separators, and joins into one text table.

        :param headers_or_table: headers when a separate table argument is supplied, otherwise the table itself
        :type headers_or_table: object
        :param table_data: additional positional values forwarded or collected by this operation
        :type table_data: tuple
        :param header_format: formatter or formatters applied to header cells
        :type header_format: object
        :param header_spans: column spans for each header cell
        :type header_spans: object
        :param column_formats: per-column formatting specifications
        :type column_formats: object
        :param column_alignments: alignment code or codes for body columns
        :type column_alignments: object
        :param header_alignments: alignment codes for header cells
        :type header_alignments: object
        :param column_join: separator or separator sequence between columns
        :type column_join: object
        :param row_join: separator between rows
        :type row_join: object
        :param header_column_join: separator or separator sequence between header cells
        :type header_column_join: object
        :param header_row_join: separator between header rows
        :type header_row_join: object
        :param separator: header separator character or block separator
        :type separator: object
        :param separator_lines: number of separator rows inserted below headers
        :type separator_lines: object
        :param content_join: separator between header and body
        :type content_join: object
        :param row_padding: text prepended to the first formatted column
        :type row_padding: object
        :param strict: whether formatting errors propagate instead of falling back to `str`
        :type strict: object
        :return: the assembled table text
        :rtype: str
        """
        ...

    @classmethod
    def _join_across(cls, iterable):
        """
        **LLM Docstring**

        Combine nested table fragments along the axis required by hierarchical header extraction.

        :param iterable: nested row or header fragments to transpose and concatenate
        :type iterable: object
        :return: transposed and flattened rows
        :rtype: list[list]
        """
        ...

    @classmethod
    def _join_data(cls, data_lists):
        """
        **LLM Docstring**

        Combine nested table fragments along the axis required by hierarchical header extraction.

        :param data_lists: arrays to concatenate
        :type data_lists: object
        :return: concatenated leaf arrays
        :rtype: numpy.ndarray
        """
        ...

    @classmethod
    def _is_terminal(cls, value, depth):
        """
        **LLM Docstring**

        Classify atomic values or one-dimensional atomic sequences as terminal table data.

        :param value: candidate tree value
        :type value: object
        :param depth: current tree depth
        :type depth: object
        :return: whether the value is terminal tabular data
        :rtype: bool
        """
        ...

    @classmethod
    def extract_tree_headers(cls, tree, key_normalizer=None, depth=0, default_key=None, terminal_data_function=None):
        """
        **LLM Docstring**

        Recursively derive hierarchical header rows, span metadata, and a tabular leaf array from a nested tree.

        :param tree: nested mapping or sequence
        :type tree: object
        :param key_normalizer: callable used to rewrite keys by depth
        :type key_normalizer: object
        :param depth: current tree depth
        :type depth: object
        :param default_key: header value used for sequence nodes
        :type default_key: object
        :param terminal_data_function: predicate deciding when tree data is tabular leaves
        :type terminal_data_function: object
        :return: header rows, span rows, and extracted tabular data
        :rtype: tuple
        """
        ...

    @classmethod
    def from_tree(cls, tree_data, header_spans=None, key_normalizer=None, depth=0, default_key=None, column_formats=None, header_normalization_function=None, header_function=None, terminal_data_function=None, **opts):
        """
        **LLM Docstring**

        Construct a formatter and leaf-data array from nested tree data, with optional header transformations.

        :param tree_data: nested mapping or sequence to tabulate
        :type tree_data: object
        :param header_spans: column spans for each header cell
        :type header_spans: object
        :param key_normalizer: callable used to rewrite keys by depth
        :type key_normalizer: object
        :param depth: current tree depth
        :type depth: object
        :param default_key: header value used for sequence nodes
        :type default_key: object
        :param column_formats: per-column formatting specifications
        :type column_formats: object
        :param header_normalization_function: callable that adjusts extracted headers and spans
        :type header_normalization_function: object
        :param header_function: callable that formats each header using its span
        :type header_function: object
        :param terminal_data_function: predicate deciding when tree data is tabular leaves
        :type terminal_data_function: object
        :param opts: additional keyword options forwarded to the underlying formatter or operation
        :type opts: dict
        :return: configured formatter and extracted tabular data
        :rtype: tuple
        """
        ...

    @classmethod
    def format_tree(cls, tree_data, data_normalization_function=None, **opts):
        """
        **LLM Docstring**

        Extract and optionally normalize tree data, then return its formatted table text.

        :param tree_data: nested mapping or sequence to tabulate
        :type tree_data: object
        :param data_normalization_function: callable applied to extracted leaf data
        :type data_normalization_function: object
        :param opts: additional keyword options forwarded to the underlying formatter or operation
        :type opts: dict
        :return: formatted text
        :rtype: str
        """
        ...
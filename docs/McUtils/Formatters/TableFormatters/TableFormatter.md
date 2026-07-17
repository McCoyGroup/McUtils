## <a id="McUtils.Formatters.TableFormatters.TableFormatter">TableFormatter</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TableFormatters.py#L15)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TableFormatters.py#L15?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
default_header_format: str
default_column_join: str
default_row_join: str
default_separator: str
default_column_alignment: str
default_header_alignment: str
default_row_padding: str
supported_alignments: dict
```
<a id="McUtils.Formatters.TableFormatters.TableFormatter.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, column_formats, *, headers=None, header_spans=None, header_format=None, column_join=None, row_join=None, header_column_join=None, header_row_join=None, separator=None, separator_lines=1, content_join=None, column_alignments=None, header_alignments=None, row_padding=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TableFormatters.py#L39)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TableFormatters.py#L39?message=Update%20Docs)]
</div>
**LLM Docstring**

Initialize `TableFormatter` state from the supplied configuration.
  - `column_formats`: `object`
    > per-column formatting specifications
  - `headers`: `object`
    > optional header rows
  - `header_spans`: `object`
    > column spans for each header cell
  - `header_format`: `object`
    > formatter or formatters applied to header cells
  - `column_join`: `object`
    > separator or separator sequence between columns
  - `row_join`: `object`
    > separator between rows
  - `header_column_join`: `object`
    > separator or separator sequence between header cells
  - `header_row_join`: `object`
    > separator between header rows
  - `separator`: `object`
    > header separator character or block separator
  - `separator_lines`: `object`
    > number of separator rows inserted below headers
  - `content_join`: `object`
    > separator between header and body
  - `column_alignments`: `object`
    > alignment code or codes for body columns
  - `header_alignments`: `object`
    > alignment codes for header cells
  - `row_padding`: `object`
    > text prepended to the first formatted column
  - `:returns`: `None`
    > `None`; the operation mutates state, writes output, or raises by design.


<a id="McUtils.Formatters.TableFormatters.TableFormatter.prep_input_arrays" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
prep_input_arrays(cls, headers, data, header_spans): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L107)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L107?message=Update%20Docs)]
</div>
**LLM Docstring**

Normalize headers, spans, and rows to rectangular lists with a shared maximum column count.
  - `headers`: `object`
    > optional header rows
  - `data`: `object`
    > tabular or tree data to process
  - `header_spans`: `object`
    > column spans for each header cell
  - `:returns`: `tuple`
    > normalized headers, rows, and header spans


<a id="McUtils.Formatters.TableFormatters.TableFormatter.custom_formatter" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
custom_formatter(cls, f): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L181)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L181?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert format strings, iterable-format specifications, or callables into objects exposing a `.format` method.
  - `f`: `object`
    > string or file path being tested
  - `:returns`: `object`
    > object exposing a `.format` callable


<a id="McUtils.Formatters.TableFormatters.TableFormatter.resolve_formatters" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
resolve_formatters(cls, ncols, col_formats): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L237)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L237?message=Update%20Docs)]
</div>
**LLM Docstring**

Repeat the supplied formatter sequence cyclically and truncate it to the requested column count.
  - `ncols`: `object`
    > number of output columns
  - `col_formats`: `object`
    > format specifications to repeat across columns
  - `:returns`: `list`
    > formatter specifications repeated to `ncols` entries


<a id="McUtils.Formatters.TableFormatters.TableFormatter.prep_formatters" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
prep_formatters(cls, formats): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L257)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L257?message=Update%20Docs)]
</div>
**LLM Docstring**

Normalize one or more format specifications through `custom_formatter`.
  - `formats`: `object`
    > format specifications to normalize
  - `:returns`: `list`
    > normalized formatter objects


<a id="McUtils.Formatters.TableFormatters.TableFormatter.format_tablular_data_columns" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
format_tablular_data_columns(cls, data, formats, row_padding=None, strict=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L300)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L300?message=Update%20Docs)]
</div>
**LLM Docstring**

Format row-major data into column-major strings, optionally padding the first column of each row.
  - `data`: `object`
    > tabular or tree data to process
  - `formats`: `object`
    > format specifications to normalize
  - `row_padding`: `object`
    > text prepended to the first formatted column
  - `strict`: `object`
    > whether formatting errors propagate instead of falling back to `str`
  - `:returns`: `list[list[str]]`
    > column-major formatted strings


<a id="McUtils.Formatters.TableFormatters.TableFormatter.align_left" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
align_left(cls, col, width): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L330)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L330?message=Update%20Docs)]
</div>
**LLM Docstring**

Pad each string in a column using left alignment to the requested width.
  - `col`: `object`
    > column strings to align
  - `width`: `object`
    > fraction of text width used by the minipage
  - `:returns`: `list[str]`
    > aligned column strings


<a id="McUtils.Formatters.TableFormatters.TableFormatter.align_right" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
align_right(cls, col, width): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L346)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L346?message=Update%20Docs)]
</div>
**LLM Docstring**

Pad each string in a column using right alignment to the requested width.
  - `col`: `object`
    > column strings to align
  - `width`: `object`
    > fraction of text width used by the minipage
  - `:returns`: `list[str]`
    > aligned column strings


<a id="McUtils.Formatters.TableFormatters.TableFormatter.align_center" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
align_center(cls, col, width): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L363)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L363?message=Update%20Docs)]
</div>
**LLM Docstring**

Pad each string in a column using center alignment to the requested width.
  - `col`: `object`
    > column strings to align
  - `width`: `object`
    > fraction of text width used by the minipage
  - `:returns`: `list[str]`
    > aligned column strings


<a id="McUtils.Formatters.TableFormatters.TableFormatter.align_dot" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
align_dot(cls, col, width, dot='.'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L380)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L380?message=Update%20Docs)]
</div>
**LLM Docstring**

Align strings by their final decimal marker, pad missing fractional widths, and right-align the resulting column.
  - `col`: `object`
    > column strings to align
  - `width`: `object`
    > fraction of text width used by the minipage
  - `dot`: `object`
    > marker whose final occurrence is used as the alignment point
  - `:returns`: `list[str]`
    > aligned column strings


<a id="McUtils.Formatters.TableFormatters.TableFormatter.resolve_aligner" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
resolve_aligner(cls, alignment): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L415)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L415?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TableFormatters.TableFormatter.align_column" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
align_column(cls, header_data, cols_data, header_alignment, column_alignment, join_widths: 'list[int]', header_widths): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L417)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L417?message=Update%20Docs)]
</div>
**LLM Docstring**

Jointly size a grouped header and its body columns while accounting for inter-column join widths.
  - `header_data`: `object`
    > formatted header strings for a grouped column
  - `cols_data`: `object`
    > formatted body columns belonging to the group
  - `header_alignment`: `object`
    > alignment code for the grouped header
  - `column_alignment`: `object`
    > alignment codes for body columns
  - `join_widths`: `list[int]`
    > width contributions from separators between grouped columns
  - `header_widths`: `object`
    > reserved header widths; accepted for API compatibility
  - `:returns`: `list[str]`
    > aligned column strings


<a id="McUtils.Formatters.TableFormatters.TableFormatter.format" class="docs-object-method">&nbsp;</a> 
```python
format(self, headers_or_table, *table_data, header_format=None, header_spans=None, column_formats=None, column_alignments=None, header_alignments=None, column_join=None, row_join=None, header_column_join=None, header_row_join=None, separator=None, separator_lines=None, content_join=None, row_padding=None, strict=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TableFormatters/TableFormatter.py#L486)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TableFormatters/TableFormatter.py#L486?message=Update%20Docs)]
</div>
**LLM Docstring**

Assemble formatted headers, spanning groups, aligned body columns, separators, and joins into one text table.
  - `headers_or_table`: `object`
    > headers when a separate table argument is supplied, otherwise the table itself
  - `table_data`: `tuple`
    > additional positional values forwarded or collected by this operation
  - `header_format`: `object`
    > formatter or formatters applied to header cells
  - `header_spans`: `object`
    > column spans for each header cell
  - `column_formats`: `object`
    > per-column formatting specifications
  - `column_alignments`: `object`
    > alignment code or codes for body columns
  - `header_alignments`: `object`
    > alignment codes for header cells
  - `column_join`: `object`
    > separator or separator sequence between columns
  - `row_join`: `object`
    > separator between rows
  - `header_column_join`: `object`
    > separator or separator sequence between header cells
  - `header_row_join`: `object`
    > separator between header rows
  - `separator`: `object`
    > header separator character or block separator
  - `separator_lines`: `object`
    > number of separator rows inserted below headers
  - `content_join`: `object`
    > separator between header and body
  - `row_padding`: `object`
    > text prepended to the first formatted column
  - `strict`: `object`
    > whether formatting errors propagate instead of falling back to `str`
  - `:returns`: `str`
    > the assembled table text


<a id="McUtils.Formatters.TableFormatters.TableFormatter.extract_tree_headers" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
extract_tree_headers(cls, tree, key_normalizer=None, depth=0, default_key=None, terminal_data_function=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L841)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L841?message=Update%20Docs)]
</div>
**LLM Docstring**

Recursively derive hierarchical header rows, span metadata, and a tabular leaf array from a nested tree.
  - `tree`: `object`
    > nested mapping or sequence
  - `key_normalizer`: `object`
    > callable used to rewrite keys by depth
  - `depth`: `object`
    > current tree depth
  - `default_key`: `object`
    > header value used for sequence nodes
  - `terminal_data_function`: `object`
    > predicate deciding when tree data is tabular leaves
  - `:returns`: `tuple`
    > header rows, span rows, and extracted tabular data


<a id="McUtils.Formatters.TableFormatters.TableFormatter.from_tree" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_tree(cls, tree_data, header_spans=None, key_normalizer=None, depth=0, default_key=None, column_formats=None, header_normalization_function=None, header_function=None, terminal_data_function=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L930)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L930?message=Update%20Docs)]
</div>
**LLM Docstring**

Construct a formatter and leaf-data array from nested tree data, with optional header transformations.
  - `tree_data`: `object`
    > nested mapping or sequence to tabulate
  - `header_spans`: `object`
    > column spans for each header cell
  - `key_normalizer`: `object`
    > callable used to rewrite keys by depth
  - `depth`: `object`
    > current tree depth
  - `default_key`: `object`
    > header value used for sequence nodes
  - `column_formats`: `object`
    > per-column formatting specifications
  - `header_normalization_function`: `object`
    > callable that adjusts extracted headers and spans
  - `header_function`: `object`
    > callable that formats each header using its span
  - `terminal_data_function`: `object`
    > predicate deciding when tree data is tabular leaves
  - `opts`: `dict`
    > additional keyword options forwarded to the underlying formatter or operation
  - `:returns`: `tuple`
    > configured formatter and extracted tabular data


<a id="McUtils.Formatters.TableFormatters.TableFormatter.format_tree" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
format_tree(cls, tree_data, data_normalization_function=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L998)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L998?message=Update%20Docs)]
</div>
**LLM Docstring**

Extract and optionally normalize tree data, then return its formatted table text.
  - `tree_data`: `object`
    > nested mapping or sequence to tabulate
  - `data_normalization_function`: `object`
    > callable applied to extracted leaf data
  - `opts`: `dict`
    > additional keyword options forwarded to the underlying formatter or operation
  - `:returns`: `str`
    > formatted text
 </div>
</div>












---


<div markdown="1" class="text-secondary">
<div class="container">
  <div class="row">
   <div class="col" markdown="1">
**Feedback**   
</div>
   <div class="col" markdown="1">
**Examples**   
</div>
   <div class="col" markdown="1">
**Templates**   
</div>
   <div class="col" markdown="1">
**Documentation**   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Bug](https://github.com/McCoyGroup/McUtils/issues/new?title=Documentation%20Improvement%20Needed)/[Request](https://github.com/McCoyGroup/McUtils/issues/new?title=Example%20Request)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Formatters/TableFormatters/TableFormatter.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Formatters/TableFormatters/TableFormatter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Formatters/TableFormatters/TableFormatter.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Formatters/TableFormatters/TableFormatter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TableFormatters.py#L15?message=Update%20Docs)   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
</div>
</div>
## <a id="McUtils.McUtils.Formatters.TableFormatters.TableFormatter">TableFormatter</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TableFormatters.py#L12)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TableFormatters.py#L12?message=Update%20Docs)]
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
<a id="McUtils.McUtils.Formatters.TableFormatters.TableFormatter.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, column_formats, *, headers=None, header_spans=None, header_format=None, column_join=None, row_join=None, header_column_join=None, header_row_join=None, separator=None, separator_lines=1, content_join=None, column_alignments=None, header_alignments=None, row_padding=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TableFormatters/TableFormatter.py#L21)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TableFormatters/TableFormatter.py#L21?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Formatters.TableFormatters.TableFormatter.prep_input_arrays" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
prep_input_arrays(cls, headers, data, header_spans): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L53)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L53?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Formatters.TableFormatters.TableFormatter.custom_formatter" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
custom_formatter(cls, f): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L97)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L97?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Formatters.TableFormatters.TableFormatter.resolve_formatters" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
resolve_formatters(cls, ncols, col_formats): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L115)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L115?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Formatters.TableFormatters.TableFormatter.prep_formatters" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
prep_formatters(cls, formats): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L123)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L123?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Formatters.TableFormatters.TableFormatter.format_tablular_data_columns" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
format_tablular_data_columns(cls, data, formats, row_padding=None, strict=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L142)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L142?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Formatters.TableFormatters.TableFormatter.align_left" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
align_left(cls, col, width): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L156)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L156?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Formatters.TableFormatters.TableFormatter.align_right" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
align_right(cls, col, width): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L160)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L160?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Formatters.TableFormatters.TableFormatter.align_center" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
align_center(cls, col, width): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L165)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L165?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Formatters.TableFormatters.TableFormatter.align_dot" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
align_dot(cls, col, width, dot='.'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L170)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L170?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Formatters.TableFormatters.TableFormatter.resolve_aligner" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
resolve_aligner(cls, alignment): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L191)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L191?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Formatters.TableFormatters.TableFormatter.align_column" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
align_column(cls, header_data, cols_data, header_alignment, column_alignment, join_width, header_widths): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L193)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L193?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Formatters.TableFormatters.TableFormatter.format" class="docs-object-method">&nbsp;</a> 
```python
format(self, headers_or_table, *table_data, header_format=None, header_spans=None, column_formats=None, column_alignments=None, header_alignments=None, column_join=None, row_join=None, header_column_join=None, header_row_join=None, separator=None, separator_lines=None, content_join=None, row_padding=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TableFormatters/TableFormatter.py#L237)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TableFormatters/TableFormatter.py#L237?message=Update%20Docs)]
</div>
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TableFormatters.py#L12?message=Update%20Docs)   
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
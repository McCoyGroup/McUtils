## <a id="McUtils.Formatters.TableFormatters.TableFormatter">TableFormatter</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Formatters/TableFormatters.py#L12)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TableFormatters.py#L12?message=Update%20Docs)]
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
__init__(self, column_formats, header_format=None, column_join=None, row_join=None, header_column_join=None, header_row_join=None, separator=None, separator_lines=1, content_join=None, column_alignments=None, header_alignments=None, row_padding=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Formatters/TableFormatters/TableFormatter.py#L21)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TableFormatters/TableFormatter.py#L21?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TableFormatters.TableFormatter.prep_input_arrays" class="docs-object-method">&nbsp;</a> 
```python
prep_input_arrays(headers, data, header_spans): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Formatters/TableFormatters/TableFormatter.py#L48)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TableFormatters/TableFormatter.py#L48?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TableFormatters.TableFormatter.custom_formatter" class="docs-object-method">&nbsp;</a> 
```python
custom_formatter(f): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Formatters/TableFormatters/TableFormatter.py#L92)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TableFormatters/TableFormatter.py#L92?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TableFormatters.TableFormatter.resolve_formatters" class="docs-object-method">&nbsp;</a> 
```python
resolve_formatters(ncols, col_formats): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Formatters/TableFormatters/TableFormatter.py#L110)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TableFormatters/TableFormatter.py#L110?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TableFormatters.TableFormatter.prep_formatters" class="docs-object-method">&nbsp;</a> 
```python
prep_formatters(formats): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Formatters/TableFormatters/TableFormatter.py#L118)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TableFormatters/TableFormatter.py#L118?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TableFormatters.TableFormatter.format_tablular_data_columns" class="docs-object-method">&nbsp;</a> 
```python
format_tablular_data_columns(data, formats, row_padding=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Formatters/TableFormatters/TableFormatter.py#L127)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TableFormatters/TableFormatter.py#L127?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TableFormatters.TableFormatter.align_left" class="docs-object-method">&nbsp;</a> 
```python
align_left(col, width): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Formatters/TableFormatters/TableFormatter.py#L141)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TableFormatters/TableFormatter.py#L141?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TableFormatters.TableFormatter.align_right" class="docs-object-method">&nbsp;</a> 
```python
align_right(col, width): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Formatters/TableFormatters/TableFormatter.py#L145)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TableFormatters/TableFormatter.py#L145?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TableFormatters.TableFormatter.align_center" class="docs-object-method">&nbsp;</a> 
```python
align_center(col, width): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Formatters/TableFormatters/TableFormatter.py#L150)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TableFormatters/TableFormatter.py#L150?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TableFormatters.TableFormatter.align_dot" class="docs-object-method">&nbsp;</a> 
```python
align_dot(col, width, dot='.'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Formatters/TableFormatters/TableFormatter.py#L155)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TableFormatters/TableFormatter.py#L155?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TableFormatters.TableFormatter.resolve_aligner" class="docs-object-method">&nbsp;</a> 
```python
resolve_aligner(alignment): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Formatters/TableFormatters/TableFormatter.py#L176)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TableFormatters/TableFormatter.py#L176?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TableFormatters.TableFormatter.align_column" class="docs-object-method">&nbsp;</a> 
```python
align_column(header_data, cols_data, header_alignment, column_alignment, join_width, format_data): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Formatters/TableFormatters/TableFormatter.py#L178)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TableFormatters/TableFormatter.py#L178?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TableFormatters.TableFormatter.format" class="docs-object-method">&nbsp;</a> 
```python
format(self, headers_or_table, *table_data, header_format=None, header_spans=None, column_formats=None, column_alignments=None, header_alignments=None, column_join=None, row_join=None, header_column_join=None, header_row_join=None, separator=None, separator_lines=None, content_join=None, row_padding=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Formatters/TableFormatters/TableFormatter.py#L216)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TableFormatters/TableFormatter.py#L216?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/examples/McUtils/Formatters/TableFormatters/TableFormatter.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/examples/McUtils/Formatters/TableFormatters/TableFormatter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/docs/McUtils/Formatters/TableFormatters/TableFormatter.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/docs/templates/McUtils/Formatters/TableFormatters/TableFormatter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TableFormatters.py#L12?message=Update%20Docs)   
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
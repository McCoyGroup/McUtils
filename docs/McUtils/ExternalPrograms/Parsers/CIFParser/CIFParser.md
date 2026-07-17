## <a id="McUtils.ExternalPrograms.Parsers.CIFParser.CIFParser">CIFParser</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/CIFParser.py#L116)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/CIFParser.py#L116?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
custom_handlers: dict
```
<a id="McUtils.ExternalPrograms.Parsers.CIFParser.CIFParser.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, file, fields=None, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/CIFParser.py#L130)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/CIFParser.py#L130?message=Update%20Docs)]
</div>
**LLM Docstring**

Open a CIF file for line-by-line reading.
  - `file`: `str`
    > the CIF file
  - `fields`: `Iterable[str] | None`
    > the fields to restrict parsing to (all if omitted)
  - `kw`: `Any`
    > extra arguments for the line reader


<a id="McUtils.ExternalPrograms.Parsers.CIFParser.CIFParser.check_tag" class="docs-object-method">&nbsp;</a> 
```python
check_tag(self, line: str, depth: int = 0, active_tag=None, label: str = None, history: list[str] = None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/CIFParser/CIFParser.py#L144)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/CIFParser/CIFParser.py#L144?message=Update%20Docs)]
</div>
**LLM Docstring**

Classify a CIF line for the line-by-line reader: block starts (`data_`, `loop_`,
`_key`), comments (`#`), block ends (`#END`), and loop boundaries.
  - `line`: `str`
    > the current line
  - `depth`: `int`
    > the current nesting depth
  - `active_tag`: `Any`
    > the currently active block tag
  - `label`: `str | None`
    > the current block label
  - `history`: `list[str] | None`
    > the lines seen so far in the current block
  - `:returns`: `object`
    > the reader tag (and any label/data), or `None` to accumulate the line


<a id="McUtils.ExternalPrograms.Parsers.CIFParser.CIFParser.get_block_handlers" class="docs-object-method">&nbsp;</a> 
```python
get_block_handlers(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/CIFParser/CIFParser.py#L189)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/CIFParser/CIFParser.py#L189?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the mapping of CIF field name to the handler that converts its raw text
into a typed value (floats, ints, or symmetry arrays).
  - `:returns`: `dict`
    > the field-to-handler mapping


<a id="McUtils.ExternalPrograms.Parsers.CIFParser.CIFParser.resolve_handler" class="docs-object-method">&nbsp;</a> 
```python
resolve_handler(self, label: 'str|None'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/CIFParser/CIFParser.py#L253)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/CIFParser/CIFParser.py#L253?message=Update%20Docs)]
</div>
**LLM Docstring**

Pick the handler for a field, falling back to the integer handler for fields
whose names end in `_num`/`_number`.
  - `label`: `str | None`
    > the field name
  - `:returns`: `Callable | None`
    > the handler, or `None`


<a id="McUtils.ExternalPrograms.Parsers.CIFParser.CIFParser.handle_block" class="docs-object-method">&nbsp;</a> 
```python
handle_block(self, label: 'str|None', block_data, join=True, depth=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/CIFParser/CIFParser.py#L271)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/CIFParser/CIFParser.py#L271?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert a parsed CIF block into typed data: apply a field handler when there is
one, join text otherwise, and for unlabeled `loop_` blocks split the leading key
lines from the value rows into per-key lists.
  - `label`: `str | None`
    > the block label (or `None` for a loop block)
  - `block_data`: `list | str`
    > the accumulated block lines
  - `join`: `bool`
    > join multi-line text values
  - `depth`: `int`
    > the current nesting depth
  - `:returns`: `Any`
    > the parsed block data


<a id="McUtils.ExternalPrograms.Parsers.CIFParser.CIFParser.parse" class="docs-object-method">&nbsp;</a> 
```python
parse(self, target_fields=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/CIFParser/CIFParser.py#L319)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/CIFParser/CIFParser.py#L319?message=Update%20Docs)]
</div>
**LLM Docstring**

Parse the CIF file into a list of block dicts, optionally restricting to a set of
target fields.
  - `target_fields`: `Iterable[str] | None`
    > the fields to keep (all if omitted)
  - `:returns`: `list`
    > the parsed blocks
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/Parsers/CIFParser/CIFParser.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/Parsers/CIFParser/CIFParser.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/Parsers/CIFParser/CIFParser.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/Parsers/CIFParser/CIFParser.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/CIFParser.py#L116?message=Update%20Docs)   
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
## <a id="McUtils.ExternalPrograms.Parsers.CubeParser.CubeFileParser">CubeFileParser</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/CubeParser.py#L46)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/CubeParser.py#L46?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.ExternalPrograms.Parsers.CubeParser.CubeFileParser.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, file, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/CubeParser.py#L47)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/CubeParser.py#L47?message=Update%20Docs)]
</div>
**LLM Docstring**

Open a Gaussian-style cube (volumetric data) file for line-by-line reading.
  - `file`: `str`
    > the cube file
  - `kw`: `Any`
    > extra arguments for the line reader


<a id="McUtils.ExternalPrograms.Parsers.CubeParser.CubeFileParser.check_tag" class="docs-object-method">&nbsp;</a> 
```python
check_tag(self, line: 'str', depth: 'int' = 0, active_tag=None, label: 'str' = None, history: 'list[str]' = None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/CubeParser/CubeFileParser.py#L77)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/CubeParser/CubeFileParser.py#L77?message=Update%20Docs)]
</div>
**LLM Docstring**

Drive the sequential cube-file parse: emit the header, grid, atoms, and values
blocks in order, tracking the declared atom count to know when the atoms block
ends.
  - `line`: `str`
    > the current line
  - `depth`: `int`
    > the current nesting depth
  - `active_tag`: `Any`
    > the active block tag
  - `label`: `str | None`
    > the current block label
  - `history`: `list[str] | None`
    > the lines accumulated in the current block
  - `:returns`: `object`
    > the reader tag (and label/data), or `None`


<a id="McUtils.ExternalPrograms.Parsers.CubeParser.CubeFileParser.handle_block" class="docs-object-method">&nbsp;</a> 
```python
handle_block(self, label: "'str|None'", block_data, join=True, depth=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/CubeParser/CubeFileParser.py#L177)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/CubeParser/CubeFileParser.py#L177?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert each parsed cube block (`header`, `grid`, `atoms`, `values`) into its
typed representation.
  - `label`: `str | None`
    > the block label
  - `block_data`: `list`
    > the accumulated block lines
  - `join`: `bool`
    > unused (kept for signature parity)
  - `depth`: `int`
    > the current nesting depth
  - `:returns`: `Any`
    > the parsed block


<a id="McUtils.ExternalPrograms.Parsers.CubeParser.CubeFileParser.parse" class="docs-object-method">&nbsp;</a> 
```python
parse(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/CubeParser/CubeFileParser.py#L207)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/CubeParser/CubeFileParser.py#L207?message=Update%20Docs)]
</div>
**LLM Docstring**

Parse the whole cube file, merging the block results into a single
`CubeFileData` record.
  - `:returns`: `CubeFileData`
    > the parsed cube data
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/Parsers/CubeParser/CubeFileParser.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/Parsers/CubeParser/CubeFileParser.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/Parsers/CubeParser/CubeFileParser.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/Parsers/CubeParser/CubeFileParser.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/CubeParser.py#L46?message=Update%20Docs)   
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
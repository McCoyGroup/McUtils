## <a id="McUtils.ExternalPrograms.Parsers.Orca.OrcaHessReader">OrcaHessReader</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/Orca.py#L16)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Orca.py#L16?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
ENumber: RegexPattern
matrix_types: dict
array_types: dict
OrcaCoords: OrcaCoords
```
<a id="McUtils.ExternalPrograms.Parsers.Orca.OrcaHessReader.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, file, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/Orca.py#L18)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Orca.py#L18?message=Update%20Docs)]
</div>
**LLM Docstring**

Open an ORCA `.hess` file for stream reading.
  - `file`: `str`
    > the `.hess` file
  - `kwargs`: `Any`
    > extra arguments for the stream reader


<a id="McUtils.ExternalPrograms.Parsers.Orca.OrcaHessReader.get_special_handlers" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_special_handlers(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L40)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L40?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the mapping of block tags that need a dedicated parser to that parser.
  - `:returns`: `dict`
    > the tag-to-handler mapping


<a id="McUtils.ExternalPrograms.Parsers.Orca.OrcaHessReader.handle_orca_block" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
handle_orca_block(cls, tag, data: str): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L54)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L54?message=Update%20Docs)]
</div>
**LLM Docstring**

Dispatch a `.hess` block to the appropriate parser, choosing by tag: a special
handler, a typed matrix/array parser, or a size-based guess between a scalar,
array, and matrix.
  - `tag`: `str`
    > the block tag
  - `data`: `str`
    > the block text
  - `:returns`: `Any`
    > the parsed block


<a id="McUtils.ExternalPrograms.Parsers.Orca.OrcaHessReader.parse_matrix" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_matrix(cls, data, col_blocks=5, data_pattern=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L97)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L97?message=Update%20Docs)]
</div>
**LLM Docstring**

Parse an ORCA block-formatted matrix (a header giving the dimensions followed by
column-blocked numeric data) into a dense array.
  - `data`: `str`
    > the block text
  - `col_blocks`: `int`
    > number of columns per printed block
  - `data_pattern`: `object | None`
    > the numeric pattern to match (defaults to ORCA's `E`-number)
  - `:returns`: `np.ndarray`
    > the parsed matrix


<a id="McUtils.ExternalPrograms.Parsers.Orca.OrcaHessReader.parse_array" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_array(cls, data, data_pattern=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L145)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L145?message=Update%20Docs)]
</div>
**LLM Docstring**

Parse an ORCA block whose header gives a length followed by that many numeric
rows, flattening single-column results.
  - `data`: `str`
    > the block text
  - `data_pattern`: `object | None`
    > the numeric pattern to match (defaults to ORCA's `E`-number)
  - `:returns`: `np.ndarray`
    > the parsed array


<a id="McUtils.ExternalPrograms.Parsers.Orca.OrcaHessReader.parse_atoms" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_atoms(cls, data): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L171)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L171?message=Update%20Docs)]
</div>
**LLM Docstring**

Parse the atoms block into element labels, masses, and coordinates.
  - `data`: `str`
    > the block text
  - `:returns`: `OrcaHessReader.OrcaCoords`
    > the parsed `(atoms, mass, coords)`


<a id="McUtils.ExternalPrograms.Parsers.Orca.OrcaHessReader.get_next_block" class="docs-object-method">&nbsp;</a> 
```python
get_next_block(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/Orca/OrcaHessReader.py#L191)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Orca/OrcaHessReader.py#L191?message=Update%20Docs)]
</div>
**LLM Docstring**

Read the next `$tag ... ` block from the file, returning its tag and body (or
`None` at end of file).
  - `:returns`: `tuple | None`
    > `(tag, body)` or `None`


<a id="McUtils.ExternalPrograms.Parsers.Orca.OrcaHessReader.parse" class="docs-object-method">&nbsp;</a> 
```python
parse(self, tags=None, excludes=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/Orca/OrcaHessReader.py#L206)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Orca/OrcaHessReader.py#L206?message=Update%20Docs)]
</div>
**LLM Docstring**

Parse the `.hess` file into a dict of tag to parsed block, optionally restricting
to (or excluding) specific tags.
  - `tags`: `Iterable[str] | None`
    > tags to include (all if omitted)
  - `excludes`: `Iterable[str] | None`
    > tags to exclude
  - `:returns`: `dict`
    > the parsed blocks keyed by tag
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/Parsers/Orca/OrcaHessReader.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/Parsers/Orca/OrcaHessReader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/Parsers/Orca/OrcaHessReader.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/Parsers/Orca/OrcaHessReader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Orca.py#L16?message=Update%20Docs)   
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
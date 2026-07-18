## <a id="McUtils.Docs.DocWalker.IndexWriter">IndexWriter</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/DocWalker.py#L1328)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/DocWalker.py#L1328?message=Update%20Docs)]
</div>

Writes an index file with all of the
written documentation files.
Needs some work to provide more useful info by default.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
template: str
```
<a id="McUtils.Docs.DocWalker.IndexWriter.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *args, description=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/DocWalker.py#L1339)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/DocWalker.py#L1339?message=Update%20Docs)]
</div>
**LLM Docstring**

Initializes an index writer with a default documentation heading when no description is supplied.
  - `args`: `Any`
    > positional handler arguments

  - `description`: `str | None`
    > the index description or heading

  - `kwargs`: `Any`
    > additional handler options


<a id="McUtils.Docs.DocWalker.IndexWriter.get_identifier" class="docs-object-method">&nbsp;</a> 
```python
get_identifier(cls, o): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/DocWalker/IndexWriter.py#L1357)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/DocWalker/IndexWriter.py#L1357?message=Update%20Docs)]
</div>
**LLM Docstring**

Returns the fixed identifier used for documentation indexes.
  - `o`: `Any`
    > unused indexed object
  - `:returns`: `str`
    > `"index"`


<a id="McUtils.Docs.DocWalker.IndexWriter.get_file_paths" class="docs-object-method">&nbsp;</a> 
```python
get_file_paths(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/DocWalker/IndexWriter.py#L1370)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/DocWalker/IndexWriter.py#L1370?message=Update%20Docs)]
</div>
**LLM Docstring**

Normalizes written file paths relative to the configured documentation root.
  - `:returns`: `list`
    > normalized string paths and unchanged non-string entries


<a id="McUtils.Docs.DocWalker.IndexWriter.get_index_files" class="docs-object-method">&nbsp;</a> 
```python
get_index_files(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/DocWalker/IndexWriter.py#L1385)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/DocWalker/IndexWriter.py#L1385?message=Update%20Docs)]
</div>
**LLM Docstring**

Converts string paths into `[stem, path]` index entries.
  - `:returns`: `list`
    > the index entry list


<a id="McUtils.Docs.DocWalker.IndexWriter.get_template_params" class="docs-object-method">&nbsp;</a> 
```python
get_template_params(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/DocWalker/IndexWriter.py#L1403)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/DocWalker/IndexWriter.py#L1403?message=Update%20Docs)]
</div>
**LLM Docstring**

Parses the index description and assembles index entries and examples for rendering.
  - `:returns`: `dict`
    > the index template parameters
 </div>
</div>










## See Also
[`DocWalker`](DocWalker.md)

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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Docs/DocWalker/IndexWriter.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Docs/DocWalker/IndexWriter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Docs/DocWalker/IndexWriter.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Docs/DocWalker/IndexWriter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/DocWalker.py#L1328?message=Update%20Docs)   
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
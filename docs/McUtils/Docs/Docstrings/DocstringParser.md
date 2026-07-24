## <a id="McUtils.Docs.Docstrings.DocstringParser">DocstringParser</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Docstrings.py#L694)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Docstrings.py#L694?message=Update%20Docs)]
</div>

Parse a Python source file into a list of :class:`DocstringData`.

Each function's docstring is parsed by whichever
`DocstringDialectHandler` matches it best (see `detect_dialect`), so a single file with a mix of Google-style and
Sphinx-style docstrings parses correctly function-by-function -- unless a
`dialect` is passed to force one convention for the whole file.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Docs.Docstrings.DocstringParser.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, dialect: 'Optional[DocstringDialectHandler]' = None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Docstrings.py#L703)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Docstrings.py#L703?message=Update%20Docs)]
</div>
Args:
dialect (Optional[DocstringDialectHandler]): If given, every
    docstring is parsed with this handler instead of
    auto-detecting one per function.


<a id="McUtils.Docs.Docstrings.DocstringParser.parse_source" class="docs-object-method">&nbsp;</a> 
```python
parse_source(self, src: 'str', only_missing: 'bool' = False) -> 'List[DocstringData]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Docstrings/DocstringParser.py#L712)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Docstrings/DocstringParser.py#L712?message=Update%20Docs)]
</div>
Parse `src` text and return one :class:`DocstringData` per function.

Args:
    src (str): Python source code.
    only_missing (bool): If True, skip functions that already have a
        docstring.

Returns:
    List[DocstringData]: records in source order.


<a id="McUtils.Docs.Docstrings.DocstringParser.parse_file" class="docs-object-method">&nbsp;</a> 
```python
parse_file(self, path: 'str', only_missing: 'bool' = False) -> 'List[DocstringData]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Docstrings/DocstringParser.py#L751)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Docstrings/DocstringParser.py#L751?message=Update%20Docs)]
</div>
Read `path` and delegate to :meth:`parse_source`.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Docs/Docstrings/DocstringParser.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Docs/Docstrings/DocstringParser.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Docs/Docstrings/DocstringParser.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Docs/Docstrings/DocstringParser.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Docstrings.py#L694?message=Update%20Docs)   
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
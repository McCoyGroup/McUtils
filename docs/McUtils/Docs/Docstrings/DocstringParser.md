## <a id="McUtils.Docs.Docstrings.DocstringParser">DocstringParser</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Docstrings.py#L709)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Docstrings.py#L709?message=Update%20Docs)]
</div>

Parse a Python source file into a list of :class:`DocstringData`.

Each function's docstring is parsed by whichever
`DocstringDialectHandler` matches it best (see `detect_dialect`), so a single file with a mix of Google-style and
Sphinx-style docstrings parses correctly function-by-function -- unless a
`dialect` is passed to force one convention for the whole file.

`filter`/`exclude` let a caller skip docstring parsing entirely for
functions/methods/classes-of-methods that don't matter to it -- neither
the docstring nor the signature is even read for anything they skip.
Both are called as ``predicate(qualname, package_name)``, where
`qualname` is the dotted ``Class.method`` (or bare function) name and
`package_name` is whatever the caller passed to `parse_source`/
`parse_file` (``None`` if not given -- `DocstringsHandler` passes the
actual top-level package name, giving predicates "package information"
alongside the name).







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Docs.Docstrings.DocstringParser.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, dialect: 'Optional[DocstringDialectHandler]' = None, filter=None, exclude=<function default_exclude at 0x7f218c980790>): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Docstrings.py#L728)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Docstrings.py#L728?message=Update%20Docs)]
</div>
Args:
dialect (Optional[DocstringDialectHandler]): If given, every
    docstring is parsed with this handler instead of
    auto-detecting one per function.
filter: optional ``(qualname, package_name) -> bool``. If
    given, only qualnames for which this returns True are
    parsed at all; ``None`` (the default) applies no filter,
    i.e. everything is a candidate.
exclude: optional ``(qualname, package_name) -> bool``.
    Qualnames for which this returns True are skipped, same as
    an inverted `filter`. Defaults to :func:`default_exclude`
    (skip anything with a leading-underscore name); pass
    ``None`` to disable exclusion entirely.


<a id="McUtils.Docs.Docstrings.DocstringParser.wanted" class="docs-object-method">&nbsp;</a> 
```python
wanted(self, qualname: 'str', package_name: 'Optional[str]' = None) -> 'bool': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Docstrings/DocstringParser.py#L749)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Docstrings/DocstringParser.py#L749?message=Update%20Docs)]
</div>
True if `qualname` should actually be parsed, given this
parser's `filter`/`exclude`.


<a id="McUtils.Docs.Docstrings.DocstringParser.parse_source" class="docs-object-method">&nbsp;</a> 
```python
parse_source(self, src: 'str', only_missing: 'bool' = False, package_name: 'Optional[str]' = None) -> 'List[DocstringData]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Docstrings/DocstringParser.py#L758)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Docstrings/DocstringParser.py#L758?message=Update%20Docs)]
</div>
Parse `src` text and return one :class:`DocstringData` per function.

Args:
    src (str): Python source code.
    only_missing (bool): If True, skip functions that already have a
        docstring.
    package_name (Optional[str]): Passed through to `filter`/
        `exclude` alongside each qualname; has no other effect.

Returns:
    List[DocstringData]: records in source order, excluding any
    qualname `filter`/`exclude` ruled out (those are never parsed
    at all, not merely omitted after the fact).


<a id="McUtils.Docs.Docstrings.DocstringParser.parse_file" class="docs-object-method">&nbsp;</a> 
```python
parse_file(self, path: 'str', only_missing: 'bool' = False, package_name: 'Optional[str]' = None) -> 'List[DocstringData]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Docstrings/DocstringParser.py#L805)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Docstrings/DocstringParser.py#L805?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Docstrings.py#L709?message=Update%20Docs)   
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
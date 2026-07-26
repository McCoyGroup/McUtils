## <a id="McUtils.Docs.Docstrings.DocstringsHandler">DocstringsHandler</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Docstrings.py#L1185)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Docstrings.py#L1185?message=Update%20Docs)]
</div>

`PackageHandler` that runs `DocstringParser` + `DocstringDataAnalyzer`
over every function/method in a package's source during `parse()`, then
-- at `write()` time, once every package has been processed -- writes a
single `docstring_quality.json` at the root of `out_dir` tracking the
score and issue breakdown for every docstring in the whole run.

Not one of `DocumentationPackageDispatcher.DEFAULT_HANDLERS`; opt in by
passing it explicitly, e.g.::

    DocumentationPackageDispatcher(
        ..., handlers=(StubSummaryHandler, ExampleHandler, DocstringsHandler))







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
name: str
QUALITY_JSON_FILENAME: str
SYNTAX_ERROR_WARNING_TEMPLATE: str
READ_ERROR_WARNING_TEMPLATE: str
```
<a id="McUtils.Docs.Docstrings.DocstringsHandler.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, dispatcher, dialect=None, analyses=None, filter=None, exclude=<function default_exclude at 0x7fcf5b91e0d0>): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Docstrings.py#L1205)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Docstrings.py#L1205?message=Update%20Docs)]
</div>
Args:
dialect: forced `DocstringDialectHandler`, passed straight
    through to `DocstringParser` (default: auto-detect per
    docstring).
analyses: forced subset/mapping of checks, passed straight
    through to every `DocstringDataAnalyzer` (default: all of
    `DocstringDataAnalyzer.default_analyses`).
filter: optional ``(qualname, package_name) -> bool`` forwarded
    to `DocstringParser` -- only matching functions/methods are
    parsed at all. Defaults to ``None`` (no filtering).
exclude: optional ``(qualname, package_name) -> bool`` forwarded
    to `DocstringParser` -- matching functions/methods are
    skipped entirely (never parsed). Defaults to
    :func:`default_exclude` (anything with a leading-underscore
    class or function/method name); pass ``None`` to disable.


<a id="McUtils.Docs.Docstrings.DocstringsHandler.parse" class="docs-object-method">&nbsp;</a> 
```python
parse(self, package_name, pkg_src_path): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Docstrings/DocstringsHandler.py#L1299)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Docstrings/DocstringsHandler.py#L1299?message=Update%20Docs)]
</div>
Score every docstring under `pkg_src_path`; safe against any one
file failing to read/parse (best-effort -- one bad module shouldn't
drop QA data for the rest of the package; its error is recorded
under `errors` instead). Functions/methods ruled out by `filter`/
`exclude` are never parsed in the first place -- see
`DocstringParser.wanted`.


<a id="McUtils.Docs.Docstrings.DocstringsHandler.write" class="docs-object-method">&nbsp;</a> 
```python
write(self, components, compact=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Docstrings/DocstringsHandler.py#L1324)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Docstrings/DocstringsHandler.py#L1324?message=Update%20Docs)]
</div>
Aggregate every package's `parse()` result into a single
docstring_quality.json at the root of out_dir.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Docs/Docstrings/DocstringsHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Docs/Docstrings/DocstringsHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Docs/Docstrings/DocstringsHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Docs/Docstrings/DocstringsHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Docstrings.py#L1185?message=Update%20Docs)   
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
## <a id="McUtils.Docs.Docstrings.DocstringWriter">DocstringWriter</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Docstrings.py#L764)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Docstrings.py#L764?message=Update%20Docs)]
</div>

Write (possibly edited) :class:`DocstringData` records back into source.

Each record renders via its own ``data.dialect`` handler by default, so a
docstring parsed as Sphinx is written back as Sphinx and one parsed as
Google comes back as Google -- pass `dialect` to force one convention for
every record instead (e.g. to upgrade a whole file to Sphinx style).

Guarantees, via :meth:`verify_code_identity`, that nothing except
docstring text changes.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
default_dialect: SphinxDialectHandler
```
<a id="McUtils.Docs.Docstrings.DocstringWriter.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, header: 'str' = '', add_header: 'bool' = True, dialect: 'Optional[DocstringDialectHandler]' = None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Docstrings.py#L776)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Docstrings.py#L776?message=Update%20Docs)]
</div>
Args:
header (str): Line prepended to every rewritten docstring.
add_header (bool): If False, no header is added.
dialect (Optional[DocstringDialectHandler]): If given, every
    record is rendered with this handler regardless of its own
    ``dialect`` field.


<a id="McUtils.Docs.Docstrings.DocstringWriter.write_source" class="docs-object-method">&nbsp;</a> 
```python
write_source(self, src: 'str', data_list: 'List[DocstringData]') -> 'str': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Docstrings/DocstringWriter.py#L807)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Docstrings/DocstringWriter.py#L807?message=Update%20Docs)]
</div>
Return a new source string with the given records' docstrings applied.

Records are matched to functions by ``qualname`` (not by stored line
numbers, which may be stale) and located freshly against `src`.

Args:
    src (str): Original source code.
    data_list (List[DocstringData]): Records to write; others in the
        file are left untouched.

Returns:
    str: The rewritten source. Raises ``SyntaxError`` if the result
    would not parse, and never returns a result that changes any
    executable code (see :meth:`verify_code_identity`).


<a id="McUtils.Docs.Docstrings.DocstringWriter.write_file" class="docs-object-method">&nbsp;</a> 
```python
write_file(self, path: 'str', data_list: 'List[DocstringData]', target: 'str' = <McUtils.Devutils.core.DefaultType instance>, backup: 'bool' = None) -> 'tuple[str, str]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Docstrings/DocstringWriter.py#L850)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Docstrings/DocstringWriter.py#L850?message=Update%20Docs)]
</div>
Read `path`, apply `data_list`, and write the result back to `path`.

Args:
    path (str): File to modify in place.
    data_list (List[DocstringData]): Records to write.
    backup (bool): If True (default), keep a ``<path>.docbak`` copy of
        the pre-rewrite source (only created the first time).

Returns:
    str: The new source that was written.


<a id="McUtils.Docs.Docstrings.DocstringWriter.verify_code_identity" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
verify_code_identity(original_src: 'str', new_src: 'str') -> 'bool': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L882)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L882?message=Update%20Docs)]
</div>
Confirm only docstrings differ between two versions of a file.

Args:
    original_src (str): The "before" source.
    new_src (str): The "after" source.

Returns:
    bool: True if stripping all docstrings from both yields identical
    (``ast.unparse``-normalized) code.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Docs/Docstrings/DocstringWriter.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Docs/Docstrings/DocstringWriter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Docs/Docstrings/DocstringWriter.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Docs/Docstrings/DocstringWriter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Docstrings.py#L764?message=Update%20Docs)   
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
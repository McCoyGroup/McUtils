## <a id="McUtils.Docs.Docstrings.DocstringDialectHandler">DocstringDialectHandler</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Docstrings.py#L174)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Docstrings.py#L174?message=Update%20Docs)]
</div>

A pluggable docstring convention: parses raw text into the canonical
``DocstringData`` fields, and renders those fields back into text using
the same convention.

Subclasses register themselves (see ``DIALECTS`` below) so a file can mix
conventions function-by-function and each one round-trips in its own
style.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
name: str
```
<a id="McUtils.Docs.Docstrings.DocstringDialectHandler.sniff" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
sniff(cls, raw: 'str') -> 'bool': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L186)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L186?message=Update%20Docs)]
</div>
Return True if `raw` looks like it was written in this dialect.


<a id="McUtils.Docs.Docstrings.DocstringDialectHandler.extract" class="docs-object-method">&nbsp;</a> 
```python
extract(self, raw: 'str', node: 'ast.AST') -> 'Dict[str, Any]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Docstrings/DocstringDialectHandler.py#L191)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Docstrings/DocstringDialectHandler.py#L191?message=Update%20Docs)]
</div>
Parse `raw` (+ signature info from `node`) into the canonical dict:
``{"short_description", "details", "examples", "type_info"}``.


<a id="McUtils.Docs.Docstrings.DocstringDialectHandler.render" class="docs-object-method">&nbsp;</a> 
```python
render(self, data: "'DocstringData'") -> 'str': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Docstrings/DocstringDialectHandler.py#L197)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Docstrings/DocstringDialectHandler.py#L197?message=Update%20Docs)]
</div>
Render a (possibly edited) ``DocstringData`` back into body text.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Docs/Docstrings/DocstringDialectHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Docs/Docstrings/DocstringDialectHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Docs/Docstrings/DocstringDialectHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Docs/Docstrings/DocstringDialectHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Docstrings.py#L174?message=Update%20Docs)   
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
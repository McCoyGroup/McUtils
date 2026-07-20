## <a id="McUtils.Docs.HTMLDocs.JHTMLDocumentationEngine">JHTMLDocumentationEngine</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/HTMLDocs.py#L88)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/HTMLDocs.py#L88?message=Update%20Docs)]
</div>

Renders the same fields `InteractiveTemplateEngine` renders into
ipywidget-backed JHTML elements, but using only the plain (non-widget)
side of the same `JHTML` element interfaces -- `JHTML.Div`,
`JHTML.Details`/`JHTML.Summary`, `JHTML.Heading` & friends, `JHTML.Code`,
`JHTML.Markdown`, `JHTML.List`/`JHTML.ListItem` -- so the whole tree
serializes to plain text via `.tostring()` with no kernel involved.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Docs.HTMLDocs.JHTMLDocumentationEngine.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, templates=None, ignore_missing=False, formatter_class=None, ignore_paths=()): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/HTMLDocs.py#L100)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/HTMLDocs.py#L100?message=Update%20Docs)]
</div>
**LLM Docstring**

Initializes the static documentation engine with callable templates for each documentation object type.
  - `templates`: `Mapping[str, Callable] | None`
    > custom template handlers; defaults to the six browser methods

  - `ignore_missing`: `bool`
    > whether missing template fields should be ignored

  - `formatter_class`: `type | None`
    > an optional formatter class passed to the base engine

  - `ignore_paths`: `Iterable[str]`
    > template paths to ignore


<a id="McUtils.Docs.HTMLDocs.JHTMLDocumentationEngine.md" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
md(text): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L136)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L136?message=Update%20Docs)]
</div>
**LLM Docstring**

Converts nonempty Markdown text to a JHTML Markdown element.
  - `text`: `str | None`
    > the text to render
  - `:returns`: `Any`
    > a Markdown element, or an empty span for falsey input


<a id="McUtils.Docs.HTMLDocs.JHTMLDocumentationEngine.clean_params" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
clean_params(cls, params): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L152)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L152?message=Update%20Docs)]
</div>
**LLM Docstring**

Removes fields whose values are `None` or empty strings.
  - `params`: `Mapping[Any, Any]`
    > the fields to filter
  - `:returns`: `dict`
    > a dictionary containing only nonempty values


<a id="McUtils.Docs.HTMLDocs.JHTMLDocumentationEngine.params_table" class="docs-object-method">&nbsp;</a> 
```python
params_table(self, parameters): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/HTMLDocs/JHTMLDocumentationEngine.py#L169)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/HTMLDocs/JHTMLDocumentationEngine.py#L169?message=Update%20Docs)]
</div>
**LLM Docstring**

Renders parsed parameter metadata as a documentation list.
  - `parameters`: `Mapping[str, Mapping[str, str]] | None`
    > parameter names with type and description fields
  - `:returns`: `Any`
    > a JHTML list, or an empty span when no parameters are supplied


<a id="McUtils.Docs.HTMLDocs.JHTMLDocumentationEngine.extra_sections" class="docs-object-method">&nbsp;</a> 
```python
extra_sections(self, **fields): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/HTMLDocs/JHTMLDocumentationEngine.py#L193)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/HTMLDocs/JHTMLDocumentationEngine.py#L193?message=Update%20Docs)]
</div>
**LLM Docstring**

Renders nonempty named fields as native `<details>` sections.
  - `fields`: `Any`
    > section labels mapped to Markdown content
  - `:returns`: `list`
    > the generated details elements


<a id="McUtils.Docs.HTMLDocs.JHTMLDocumentationEngine.code_block" class="docs-object-method">&nbsp;</a> 
```python
code_block(self, decorator, name, signature): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/HTMLDocs/JHTMLDocumentationEngine.py#L213)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/HTMLDocs/JHTMLDocumentationEngine.py#L213?message=Update%20Docs)]
</div>
**LLM Docstring**

Renders a compact Python function signature block.
  - `decorator`: `str | None`
    > decorator text prepended to the function definition

  - `name`: `str`
    > the function name

  - `signature`: `str`
    > the parenthesized signature
  - `:returns`: `Any`
    > a highlighted JHTML preformatted block


<a id="McUtils.Docs.HTMLDocs.JHTMLDocumentationEngine.index_browser" class="docs-object-method">&nbsp;</a> 
```python
index_browser(self, index_files=None, details=None, related=None, description=None, examples=None, _self=None, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/HTMLDocs/JHTMLDocumentationEngine.py#L237)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/HTMLDocs/JHTMLDocumentationEngine.py#L237?message=Update%20Docs)]
</div>
**LLM Docstring**

Renders an index page from its description, child index entries, and optional sections
  - `index_files`: `Iterable[Any] | None`
    > rendered index entries

  - `details`: `str | None`
    > details Markdown

  - `related`: `str | None`
    > related-object Markdown

  - `description`: `str | None`
    > index description

  - `examples`: `str | None`
    > examples Markdown

  - `_self`: `Any | None`
    > the active template handler

  - `kw`: `Any`
    > unused template fields
  - `:returns`: `Any`
    > a JHTML index container


<a id="McUtils.Docs.HTMLDocs.JHTMLDocumentationEngine.module_browser" class="docs-object-method">&nbsp;</a> 
```python
module_browser(self, members=None, name=None, id=None, details=None, related=None, description=None, examples=None, tests=None, lineno=None, _self=None, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/HTMLDocs/JHTMLDocumentationEngine.py#L273)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/HTMLDocs/JHTMLDocumentationEngine.py#L273?message=Update%20Docs)]
</div>
**LLM Docstring**

Renders a module section with expandable output for each documented member
  - `members`: `Mapping[str, Any] | None`
    > member identifiers

  - `name`: `str | None`
    > module name

  - `id`: `str | None`
    > anchor identifier

  - `details`: `str | None`
    > details Markdown

  - `related`: `str | None`
    > related-object Markdown

  - `description`: `str | None`
    > module description

  - `examples`: `str | None`
    > examples Markdown

  - `tests`: `Any | None`
    > test/example data

  - `lineno`: `int | str | None`
    > source line metadata

  - `_self`: `Any`
    > the active template handler

  - `kw`: `Any`
    > unused template fields
  - `:returns`: `Any`
    > a JHTML module section


<a id="McUtils.Docs.HTMLDocs.JHTMLDocumentationEngine.class_browser" class="docs-object-method">&nbsp;</a> 
```python
class_browser(self, id=None, name=None, related=None, out_file=None, lineno=None, parameters=None, props=None, description=None, methods=None, examples=None, tests=None, details=None, _self=None, **_): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/HTMLDocs/JHTMLDocumentationEngine.py#L337)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/HTMLDocs/JHTMLDocumentationEngine.py#L337?message=Update%20Docs)]
</div>
**LLM Docstring**

Renders a class section containing description, properties, parameters, and handled methods
  - `id`: `str | None`
    > anchor identifier

  - `name`: `str | None`
    > class name

  - `related`: `str | None`
    > related-object Markdown

  - `out_file`: `str | None`
    > unused output-file metadata

  - `lineno`: `int | str | None`
    > source line metadata

  - `parameters`: `Mapping[str, Any] | None`
    > parsed parameter metadata

  - `props`: `Iterable[tuple[str, Any]] | None`
    > public property metadata

  - `description`: `str | None`
    > class description

  - `methods`: `Iterable[Any] | None`
    > method handlers

  - `examples`: `str | None`
    > examples Markdown

  - `tests`: `Any | None`
    > unused test metadata

  - `details`: `str | None`
    > details Markdown

  - `_self`: `Any | None`
    > the active handler

  - `_`: `Any`
    > unused template fields
  - `:returns`: `Any`
    > a JHTML class section


<a id="McUtils.Docs.HTMLDocs.JHTMLDocumentationEngine.method_browser" class="docs-object-method">&nbsp;</a> 
```python
method_browser(self, id=None, name=None, decorator=None, signature=None, related=None, out_file=None, lineno=None, parameters=None, props=None, description=None, examples=None, tests=None, details=None, **_): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/HTMLDocs/JHTMLDocumentationEngine.py#L409)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/HTMLDocs/JHTMLDocumentationEngine.py#L409?message=Update%20Docs)]
</div>
**LLM Docstring**

Renders a method as a collapsible details element with signature and documentation
  - `id`: `str | None`
    > anchor identifier

  - `name`: `str`
    > method name

  - `decorator`: `str | None`
    > decorator text

  - `signature`: `str`
    > method signature

  - `related`: `str | None`
    > unused related metadata

  - `out_file`: `str | None`
    > unused output metadata

  - `lineno`: `int | str | None`
    > source line metadata

  - `parameters`: `Mapping[str, Any] | None`
    > parsed parameters

  - `props`: `Any | None`
    > unused property metadata

  - `description`: `str | None`
    > method description

  - `examples`: `str | None`
    > examples Markdown

  - `tests`: `Any | None`
    > unused test metadata

  - `details`: `str | None`
    > details Markdown

  - `_`: `Any`
    > unused template fields
  - `:returns`: `Any`
    > a JHTML details element


<a id="McUtils.Docs.HTMLDocs.JHTMLDocumentationEngine.object_browser" class="docs-object-method">&nbsp;</a> 
```python
object_browser(self, id=None, name=None, related=None, out_file=None, lineno=None, parameters=None, props=None, description=None, methods=None, examples=None, tests=None, details=None, _self=None, **_): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/HTMLDocs/JHTMLDocumentationEngine.py#L473)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/HTMLDocs/JHTMLDocumentationEngine.py#L473?message=Update%20Docs)]
</div>
**LLM Docstring**

Renders a generic object section with its runtime type and optional documentation sections
  - `id`: `str | None`
    > anchor identifier

  - `name`: `str`
    > object name

  - `related`: `str | None`
    > unused related metadata

  - `out_file`: `str | None`
    > unused output metadata

  - `lineno`: `int | str | None`
    > source line metadata

  - `parameters`: `Any | None`
    > unused parameter metadata

  - `props`: `Any | None`
    > unused property metadata

  - `description`: `str | None`
    > object description

  - `methods`: `Any | None`
    > unused method metadata

  - `examples`: `str | None`
    > examples Markdown

  - `tests`: `Any | None`
    > unused test metadata

  - `details`: `str | None`
    > details Markdown

  - `_self`: `Any`
    > the active handler containing the object

  - `_`: `Any`
    > unused template fields
  - `:returns`: `Any`
    > a JHTML object section


<a id="McUtils.Docs.HTMLDocs.JHTMLDocumentationEngine.function_browser" class="docs-object-method">&nbsp;</a> 
```python
function_browser(self, id=None, name=None, decorator=None, signature=None, related=None, out_file=None, lineno=None, parameters=None, props=None, description=None, examples=None, tests=None, details=None, **_): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/HTMLDocs/JHTMLDocumentationEngine.py#L533)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/HTMLDocs/JHTMLDocumentationEngine.py#L533?message=Update%20Docs)]
</div>
**LLM Docstring**

Renders a function section containing its signature, description, parameters, and optional sections
  - `id`: `str | None`
    > anchor identifier

  - `name`: `str`
    > function name

  - `decorator`: `str | None`
    > decorator text

  - `signature`: `str`
    > function signature

  - `related`: `str | None`
    > unused related metadata

  - `out_file`: `str | None`
    > unused output metadata

  - `lineno`: `int | str | None`
    > source line metadata

  - `parameters`: `Mapping[str, Any] | None`
    > parsed parameters

  - `props`: `Any | None`
    > unused property metadata

  - `description`: `str | None`
    > function description

  - `examples`: `str | None`
    > examples Markdown

  - `tests`: `Any | None`
    > unused test metadata

  - `details`: `str | None`
    > details Markdown

  - `_`: `Any`
    > unused template fields
  - `:returns`: `Any`
    > a JHTML function section
 </div>
</div>










## See Also
[`InteractiveTemplateEngine`](McUtils/Docs/DocWalker/InteractiveTemplateEngine.md)<span>&nbsp;&#9642;&nbsp;</span>[`jdoc`](McUtils/Docs/jdoc.md)

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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Docs/HTMLDocs/JHTMLDocumentationEngine.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Docs/HTMLDocs/JHTMLDocumentationEngine.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Docs/HTMLDocs/JHTMLDocumentationEngine.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Docs/HTMLDocs/JHTMLDocumentationEngine.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/HTMLDocs.py#L88?message=Update%20Docs)   
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
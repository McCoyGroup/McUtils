## <a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter">TemplateFormatter</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L633)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L633?message=Update%20Docs)]
</div>

Provides a formatter for fields that allows for
the inclusion of standard Bootstrap HTML elements
alongside the classic formatting







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
max_recusion: int
directives: TemplateFormatDirective
frozendict: frozendict
```
<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, templates): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L657)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L657?message=Update%20Docs)]
</div>
**LLM Docstring**

Store an immutable template mapping and initialize the stack of active formatting scopes.
  - `templates`: `Any`
    > the mapping of template identifiers to resources

  - `:returns`: `None`
    > `None`.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.format_parameters" class="docs-object-method">&nbsp;</a> 
```python
@property
format_parameters(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L671)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L671?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the parameter mapping for the innermost active formatting operation.
  - `:returns`: `dict | None`
    > The innermost parameter mapping, or `None` outside formatting.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.templates" class="docs-object-method">&nbsp;</a> 
```python
@property
templates(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L682)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L682?message=Update%20Docs)]
</div>
**LLM Docstring**

Expose the immutable template-resource mapping.
  - `:returns`: `Mapping`
    > The immutable template mapping.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.special_callbacks" class="docs-object-method">&nbsp;</a> 
```python
@property
special_callbacks(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L693)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L693?message=Update%20Docs)]
</div>
**LLM Docstring**

Map special format-field markers to evaluation, directive, comment, raw, and assignment handlers.
  - `:returns`: `dict`
    > A mapping from special field markers to their handler methods.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.callback_map" class="docs-object-method">&nbsp;</a> 
```python
@property
callback_map(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L704)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L704?message=Update%20Docs)]
</div>
**LLM Docstring**

Combine special markers with every registered directive marker.
  - `:returns`: `dict`
    > The complete mapping from special and directive markers to handlers.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.apply_eval_tree" class="docs-object-method">&nbsp;</a> 
```python
apply_eval_tree(self, _, spec) -> str: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L719)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L719?message=Update%20Docs)]
</div>
**LLM Docstring**

Parse and evaluate a cleaned Python expression or statement block against the active parameters.
  - `_`: `Any`
    > an unused callback key
  - `spec`: `Any`
    > the object specification or template expression

  - `:returns`: `str`
    > The evaluated expression result, with `None` converted to an empty string.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.apply_directive_tree" class="docs-object-method">&nbsp;</a> 
```python
apply_directive_tree(self, _, spec) -> str: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L738)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L738?message=Update%20Docs)]
</div>
**LLM Docstring**

Evaluate a directive expression after wrapping it in parentheses.
  - `_`: `Any`
    > an unused callback key
  - `spec`: `Any`
    > the object specification or template expression

  - `:returns`: `str`
    > The evaluated directive-expression result.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.apply_assignment" class="docs-object-method">&nbsp;</a> 
```python
apply_assignment(self, key, spec) -> str: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L753)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L753?message=Update%20Docs)]
</div>
**LLM Docstring**

Assign the literal right-hand text from an inline assignment into the active parameter mapping.
  - `key`: `Any`
    > the lookup, assignment, or formatting key
  - `spec`: `Any`
    > the object specification or template expression

  - `:returns`: `str`
    > An empty string after updating the active parameter mapping.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.apply_raw" class="docs-object-method">&nbsp;</a> 
```python
apply_raw(self, key, spec) -> str: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L770)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L770?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a format specification unchanged.
  - `key`: `Any`
    > the lookup, assignment, or formatting key
  - `spec`: `Any`
    > the object specification or template expression

  - `:returns`: `str`
    > The unmodified format specification.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.apply_comment" class="docs-object-method">&nbsp;</a> 
```python
apply_comment(self, key, spec) -> str: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L785)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L785?message=Update%20Docs)]
</div>
**LLM Docstring**

Discard a template comment field.
  - `key`: `Any`
    > the lookup, assignment, or formatting key
  - `spec`: `Any`
    > the object specification or template expression

  - `:returns`: `str`
    > An empty string, removing the comment from output.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.apply_directive" class="docs-object-method">&nbsp;</a> 
```python
apply_directive(self, key, spec) -> str: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L800)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L800?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert a directive marker and argument text into an evaluable directive call.
  - `key`: `Any`
    > the lookup, assignment, or formatting key
  - `spec`: `Any`
    > the object specification or template expression

  - `:returns`: `str`
    > The evaluated result of the named directive call.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.format_field" class="docs-object-method">&nbsp;</a> 
```python
format_field(self, value: Any, format_spec: str) -> str: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L818)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L818?message=Update%20Docs)]
</div>
**LLM Docstring**

Route special string-valued fields through callback handlers and otherwise use standard formatting.
  - `value`: `Any`
    > the value associated with the key
  - `format_spec`: `str`
    > the format specification associated with the field

  - `:returns`: `str`
    > The special-callback result or the standard formatted field text.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.load_template" class="docs-object-method">&nbsp;</a> 
```python
load_template(self, template): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L848)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L848?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolve a registered template and read file-backed content with caching.
  - `template`: `Any`
    > the template name, template text, or template callable

  - `:returns`: `Any`
    > The registered template text, read from disk when the resource is a file path.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.vformat" class="docs-object-method">&nbsp;</a> 
```python
vformat(self, format_string: str, args: Sequence[Any], kwargs: Mapping[str, Any]): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L883)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L883?message=Update%20Docs)]
</div>
**LLM Docstring**

Render a template within a temporary parameter scope populated with special callback markers.
  - `format_string`: `str`
    > the template string being formatted
  - `args`: `Sequence[Any]`
    > positional arguments forwarded to the wrapped callable
  - `kwargs`: `Mapping[str, Any]`
    > keyword arguments forwarded to the wrapped callable

  - `:returns`: `Any`
    > The fully rendered template string.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L633?message=Update%20Docs)   
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
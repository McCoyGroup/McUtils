## <a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateEngine">TemplateEngine</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L1276)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L1276?message=Update%20Docs)]
</div>

Provides an engine for generating content using a
`TemplateFormatter` and `ResourceLocator`







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
formatter_class: TemplateFormatter
outStream: outStream
```
<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateEngine.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, locator: McUtils.Formatters.TemplateEngine.TemplateEngine.Locator, template_pattern='*.*', ignore_missing=False, formatter_class=None, ignore_paths=()): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L1283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L1283?message=Update%20Docs)]
</div>
**LLM Docstring**

Discover matching template resources, construct the formatter, and store output-control options.
  - `locator`: `Locator`
    > the resource locator supplying templates
  - `template_pattern`: `Any`
    > the pattern selecting template resources
  - `ignore_missing`: `Any`
    > whether missing format fields should resolve through a default mapping
  - `formatter_class`: `Any`
    > the formatter implementation to instantiate
  - `ignore_paths`: `Any`
    > target paths that should not be written

  - `:returns`: `None`
    > `None`.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateEngine.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateEngine.py#L1319)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateEngine.py#L1319?message=Update%20Docs)]
</div>
**LLM Docstring**

Return an elided representation containing the locator.
  - `:returns`: `Any`
    > An elided constructor-style string identifying the locator.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateEngine.format_map" class="docs-object-method">&nbsp;</a> 
```python
format_map(self, template, parameters): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateEngine.py#L1332)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateEngine.py#L1332?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolve a template identifier when registered and render it with a parameter mapping.
  - `template`: `Any`
    > the template name, template text, or template callable
  - `parameters`: `Any`
    > the values exposed while formatting

  - `:returns`: `Any`
    > The rendered template text.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateEngine.format" class="docs-object-method">&nbsp;</a> 
```python
format(self, template, **parameters): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateEngine.py#L1353)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateEngine.py#L1353?message=Update%20Docs)]
</div>
**LLM Docstring**

Render a template using keyword parameters.
  - `template`: `Any`
    > the template name, template text, or template callable
  - `parameters`: `Any`
    > the values exposed while formatting

  - `:returns`: `Any`
    > The rendered template text.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateEngine.write_string" class="docs-object-method">&nbsp;</a> 
```python
write_string(self, target, txt): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateEngine.py#L1446)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateEngine.py#L1446?message=Update%20Docs)]
</div>
**LLM Docstring**

Write rendered text to a target through `outStream`.
  - `target`: `Any`
    > the destination path, stream, or key
  - `txt`: `Any`
    > the text to normalize

  - `:returns`: `Any`
    > The destination returned by `outStream.write`.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateEngine.apply" class="docs-object-method">&nbsp;</a> 
```python
apply(self, template, target, **template_params): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateEngine.py#L1461)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateEngine.py#L1461?message=Update%20Docs)]
</div>
**LLM Docstring**

Render a template and either return the string or write it unless the target is ignored.
  - `template`: `Any`
    > the template name, template text, or template callable
  - `target`: `Any`
    > the destination path, stream, or key
  - `template_params`: `Any`
    > values supplied to the template

  - `:returns`: `Any`
    > The rendered text when `target` is `None`, the written target otherwise, or `None` for ignored paths.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateEngine.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateEngine.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateEngine.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateEngine.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L1276?message=Update%20Docs)   
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
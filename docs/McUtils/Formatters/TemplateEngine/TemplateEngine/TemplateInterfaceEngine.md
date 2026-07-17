## <a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateInterfaceEngine">TemplateInterfaceEngine</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L2214)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L2214?message=Update%20Docs)]
</div>

A variant on a template engine designed for more interactive use.
In many ways, _not_ a template engine, but too useful to ignore while I
find a more uniform abstraction.
Generates _interfaces_ from a set of interface template functions
rather than strings from template files.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
formatter_class: TemplateInterfaceFormatter
```
<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateInterfaceEngine.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, templates: 'TemplateInterfaceList|dict', ignore_missing=False, formatter_class=None, ignore_paths=()): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L2224)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L2224?message=Update%20Docs)]
</div>
**LLM Docstring**

Normalize a dictionary of callables into an interface resource list and initialize the base engine.
  - `templates`: `'TemplateInterfaceList|dict'`
    > the mapping of template identifiers to resources
  - `ignore_missing`: `Any`
    > whether missing format fields should resolve through a default mapping
  - `formatter_class`: `Any`
    > the formatter implementation to instantiate
  - `ignore_paths`: `Any`
    > target paths that should not be written

  - `:returns`: `None`
    > `None`.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateInterfaceEngine.format_map" class="docs-object-method">&nbsp;</a> 
```python
format_map(self, template, parameters): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateInterfaceEngine.py#L2257)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateInterfaceEngine.py#L2257?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolve and invoke a callable template with the supplied parameter mapping.
  - `template`: `Any`
    > the template name, template text, or template callable
  - `parameters`: `Any`
    > the values exposed while formatting

  - `:returns`: `Any`
    > The value returned by the resolved interface template.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateInterfaceEngine.apply" class="docs-object-method">&nbsp;</a> 
```python
apply(self, template, target, **template_params): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateInterfaceEngine.py#L2279)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateInterfaceEngine.py#L2279?message=Update%20Docs)]
</div>
**LLM Docstring**

Return an interface result directly or map it to a non-ignored target key.
  - `template`: `Any`
    > the template name, template text, or template callable
  - `target`: `Any`
    > the destination path, stream, or key
  - `template_params`: `Any`
    > values supplied to the template

  - `:returns`: `Any`
    > The direct interface value, a `{target: value}` mapping, or `None` for ignored targets.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateInterfaceEngine.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateInterfaceEngine.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateInterfaceEngine.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateInterfaceEngine.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L2214?message=Update%20Docs)   
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
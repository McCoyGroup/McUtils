## <a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateInterfaceFormatter">TemplateInterfaceFormatter</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L2057)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L2057?message=Update%20Docs)]
</div>

Provides an interface that mimics a `TemplateFormatter`
but does nothing more than route to a set of template functions







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateInterfaceFormatter.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, templates): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L2062)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L2062?message=Update%20Docs)]
</div>
**LLM Docstring**

Store callable templates and initialize the active parameter-scope stack.
  - `templates`: `Any`
    > the mapping of template identifiers to resources

  - `:returns`: `None`
    > `None`.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateInterfaceFormatter.format_parameters" class="docs-object-method">&nbsp;</a> 
```python
@property
format_parameters(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateInterfaceFormatter.py#L2076)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateInterfaceFormatter.py#L2076?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the innermost active interface parameter mapping.
  - `:returns`: `dict | None`
    > The active interface parameter mapping, or `None` outside invocation.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateInterfaceFormatter.templates" class="docs-object-method">&nbsp;</a> 
```python
@property
templates(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateInterfaceFormatter.py#L2087)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateInterfaceFormatter.py#L2087?message=Update%20Docs)]
</div>
**LLM Docstring**

Expose the callable-template mapping.
  - `:returns`: `Mapping`
    > The stored mapping of interface template callables.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateInterfaceFormatter.special_callbacks" class="docs-object-method">&nbsp;</a> 
```python
@property
special_callbacks(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateInterfaceFormatter.py#L2098)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateInterfaceFormatter.py#L2098?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the currently empty special-callback mapping for interface templates.
  - `:returns`: `dict`
    > An empty mapping; interface templates do not define special field callbacks.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateInterfaceFormatter.load_template" class="docs-object-method">&nbsp;</a> 
```python
load_template(self, template): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateInterfaceFormatter.py#L2160)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateInterfaceFormatter.py#L2160?message=Update%20Docs)]
</div>
**LLM Docstring**

Retrieve a callable template by identifier.
  - `template`: `Any`
    > the template name, template text, or template callable

  - `:returns`: `Any`
    > The callable registered under the template identifier.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateInterfaceFormatter.vformat" class="docs-object-method">&nbsp;</a> 
```python
vformat(self, template: Callable, args: Sequence[Any], kwargs: Mapping[str, Any]): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateInterfaceFormatter.py#L2183)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateInterfaceFormatter.py#L2183?message=Update%20Docs)]
</div>
**LLM Docstring**

Invoke a callable template inside a temporary formatting-parameter scope.
  - `template`: `Callable`
    > the template name, template text, or template callable
  - `args`: `Sequence[Any]`
    > positional arguments forwarded to the wrapped callable
  - `kwargs`: `Mapping[str, Any]`
    > keyword arguments forwarded to the wrapped callable

  - `:returns`: `Any`
    > The value returned by invoking the callable template.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateInterfaceFormatter.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateInterfaceFormatter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateInterfaceFormatter.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateInterfaceFormatter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L2057?message=Update%20Docs)   
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
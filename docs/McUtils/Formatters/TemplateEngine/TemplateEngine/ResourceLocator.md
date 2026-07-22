## <a id="McUtils.Formatters.TemplateEngine.TemplateEngine.ResourceLocator">ResourceLocator</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L1185)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L1185?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.ResourceLocator.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, locators: Iterable[Union[McUtils.Formatters.TemplateEngine.TemplateEngine.ResourcePathLocator, Iterable[str], Tuple[Iterable[str], Union[str, Iterable[str]]]]]): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L1186)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L1186?message=Update%20Docs)]
</div>
**LLM Docstring**

Normalize heterogeneous locator specifications into a flat sequence of path locators.
  - `locators`: `Iterable[Union[ResourcePathLocator, Iterable[str], Tuple[Iterable[str], Union[str, Iterable[str]]]]]`
    > resource locator definitions to combine

  - `:returns`: `None`
    > `None`.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.ResourceLocator.locate" class="docs-object-method">&nbsp;</a> 
```python
locate(self, identifier): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/ResourceLocator.py#L1213)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/ResourceLocator.py#L1213?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the first resource path resolved by the configured locators.
  - `identifier`: `Any`
    > the resource or Python object identifier

  - `:returns`: `Any`
    > The first resource resolved by any component locator, or `None`.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.ResourceLocator.paths" class="docs-object-method">&nbsp;</a> 
```python
paths(self, filter_pattern=None, **_): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/ResourceLocator.py#L1229)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/ResourceLocator.py#L1229?message=Update%20Docs)]
</div>
**LLM Docstring**

Combine resource paths from all locators and optionally filter them by regex or glob.
  - `filter_pattern`: `Any`
    > a regular expression or glob used to filter resource paths
  - `_`: `Any`
    > an unused callback key

  - `:returns`: `Iterable[str]`
    > The combined resource identifiers, optionally filtered by the supplied pattern.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.ResourceLocator.directories" class="docs-object-method">&nbsp;</a> 
```python
directories(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/ResourceLocator.py#L1252)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/ResourceLocator.py#L1252?message=Update%20Docs)]
</div>
**LLM Docstring**

Return unique search directories from all component locators in encounter order.
  - `:returns`: `Iterable[str]`
    > The unique component search directories in encounter order.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.ResourceLocator.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/ResourceLocator.py#L1262)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/ResourceLocator.py#L1262?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a representation based on the combined search directories.
  - `:returns`: `Any`
    > A constructor-style string containing the combined directories.


<a id="typing.Protocol.__init_subclass__.<locals>._proto_hook" class="docs-object-method">&nbsp;</a> 
```python
__subclasshook__(other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/typing/Protocol/__init_subclass__/<locals>.py#L1200)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/typing/Protocol/__init_subclass__/<locals>.py#L1200?message=Update%20Docs)]
</div>
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Formatters/TemplateEngine/TemplateEngine/ResourceLocator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Formatters/TemplateEngine/TemplateEngine/ResourceLocator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Formatters/TemplateEngine/TemplateEngine/ResourceLocator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Formatters/TemplateEngine/TemplateEngine/ResourceLocator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L1185?message=Update%20Docs)   
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
## <a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateResourceExtractor">TemplateResourceExtractor</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L1812)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L1812?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
extension: str
resource_keys: list
resource_attrs: list
```
<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateResourceExtractor.path_extension" class="docs-object-method">&nbsp;</a> 
```python
path_extension(self, handler: McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateHandler): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateResourceExtractor.py#L1814)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateResourceExtractor.py#L1814?message=Update%20Docs)]
</div>
Provides the default examples path for the object
  - `:returns`: `_`
    >


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateResourceExtractor.get_resource" class="docs-object-method">&nbsp;</a> 
```python
get_resource(self, handler: McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateHandler, keys=None, attrs=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateResourceExtractor.py#L1823)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateResourceExtractor.py#L1823?message=Update%20Docs)]
</div>
**LLM Docstring**

Locate a resource using configured handler fields, object attributes, or the default derived path.
  - `handler`: `TemplateHandler`
    > the handler whose resource should be located
  - `keys`: `Any`
    > handler fields checked for an explicit resource
  - `attrs`: `Any`
    > object attributes checked for an explicit resource

  - `:returns`: `Any`
    > The resolved resource identifier or path, or `None` when none can be found.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateResourceExtractor.load" class="docs-object-method">&nbsp;</a> 
```python
load(self, handler: McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateHandler): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateResourceExtractor.py#L1870)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateResourceExtractor.py#L1870?message=Update%20Docs)]
</div>
Loads examples for the stored object if provided
  - `:returns`: `_`
    >


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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateResourceExtractor.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateResourceExtractor.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateResourceExtractor.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateResourceExtractor.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L1812?message=Update%20Docs)   
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
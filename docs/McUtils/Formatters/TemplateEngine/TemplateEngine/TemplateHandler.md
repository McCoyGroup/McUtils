## <a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateHandler">TemplateHandler</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L1474)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L1474?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
template: NoneType
extension: str
squash_repeat_packages: bool
blacklist_packages: set
```
<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateHandler.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, obj, *, out=None, engine: McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateEngine = None, root=None, squash_repeat_packages=True, is_package_root=False, **extra_fields): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L1478)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L1478?message=Update%20Docs)]
</div>
**LLM Docstring**

Initialize object-handling state, resolve the output target, and choose an object-specific or default template.
  - `obj`: `Any`
    > the object to inspect or dispatch
  - `out`: `Any`
    > the output root, file, or stream
  - `engine`: `TemplateEngine`
    > the template engine used to render content
  - `root`: `Any`
    > the output root used to compute relative URLs
  - `squash_repeat_packages`: `Any`
    > whether repeated package components are collapsed
  - `is_package_root`: `Any`
    > whether the documented object represents a package root
  - `extra_fields`: `Any`
    > additional fields exposed to handlers and templates

  - `:returns`: `None`
    > `None`.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateHandler.template_params" class="docs-object-method">&nbsp;</a> 
```python
template_params(self, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateHandler.py#L1530)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateHandler.py#L1530?message=Update%20Docs)]
</div>
**LLM Docstring**

Merge handler extra fields with parameters computed for the current object.
  - `kwargs`: `Any`
    > keyword arguments forwarded to the wrapped callable

  - `:returns`: `Any`
    > The merged mapping of extra fields and object-specific template parameters.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateHandler.get_template_params" class="docs-object-method">&nbsp;</a> 
```python
get_template_params(self, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateHandler.py#L1545)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateHandler.py#L1545?message=Update%20Docs)]
</div>
Returns the parameters that should be inserted into the template
  - `:returns`: `dict`
    >


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateHandler.package_path" class="docs-object-method">&nbsp;</a> 
```python
@property
package_path(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateHandler.py#L1555)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateHandler.py#L1555?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the package name and source URL tuple for the handled object.
  - `:returns`: `Any`
    > A `(package_name, source_url)` tuple.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateHandler.get_package_and_url" class="docs-object-method">&nbsp;</a> 
```python
get_package_and_url(self, include_url_base=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateHandler.py#L1566)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateHandler.py#L1566?message=Update%20Docs)]
</div>
Returns package name and corresponding URL for the object
being documented
  - `:returns`: `_`
    >


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateHandler.target_identifier" class="docs-object-method">&nbsp;</a> 
```python
@property
target_identifier(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateHandler.py#L1609)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateHandler.py#L1609?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the normalized dotted identifier used for the output target.
  - `:returns`: `Any`
    > The normalized dotted target identifier.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateHandler.squash_reps" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
squash_reps(cls, ident): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1620)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1620?message=Update%20Docs)]
</div>
**LLM Docstring**

Collapse the leading repeated package components in a dotted identifier.
  - `ident`: `Any`
    > the dotted identifier to normalize

  - `:returns`: `Any`
    > The dotted identifier with leading repeated package components removed.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateHandler.get_target_extension" class="docs-object-method">&nbsp;</a> 
```python
get_target_extension(self, identifier=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateHandler.py#L1641)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateHandler.py#L1641?message=Update%20Docs)]
</div>
**LLM Docstring**

Split an object identifier into normalized path components for output and resource lookup.
  - `identifier`: `Any`
    > the resource or Python object identifier

  - `:returns`: `Any`
    > The normalized identifier components used as a resource or output path.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateHandler.get_output_file" class="docs-object-method">&nbsp;</a> 
```python
get_output_file(self, out): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateHandler.py#L1666)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateHandler.py#L1666?message=Update%20Docs)]
</div>
Returns package name and corresponding URL for the object
being documented
  - `:returns`: `_`
    >


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateHandler.handle" class="docs-object-method">&nbsp;</a> 
```python
handle(self, template=None, target=None, write=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateHandler.py#L1686)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateHandler.py#L1686?message=Update%20Docs)]
</div>
Formats the documentation Markdown from the supplied template
  - `template`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateHandler.check_should_write" class="docs-object-method">&nbsp;</a> 
```python
check_should_write(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateHandler.py#L1784)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateHandler.py#L1784?message=Update%20Docs)]
</div>
Determines whether the object really actually should be
documented (quite permissive)
  - `:returns`: `_`
    >
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L1474?message=Update%20Docs)   
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
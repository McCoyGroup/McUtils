## <a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter">TemplateFormatter</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Formatters/TemplateEngine/TemplateEngine.py#L359)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TemplateEngine/TemplateEngine.py#L359?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L370)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L370?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.format_parameters" class="docs-object-method">&nbsp;</a> 
```python
@property
format_parameters(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L373)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L373?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.templates" class="docs-object-method">&nbsp;</a> 
```python
@property
templates(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L376)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L376?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.special_callbacks" class="docs-object-method">&nbsp;</a> 
```python
@property
special_callbacks(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L379)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L379?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.callback_map" class="docs-object-method">&nbsp;</a> 
```python
@property
callback_map(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L382)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L382?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.apply_eval_tree" class="docs-object-method">&nbsp;</a> 
```python
apply_eval_tree(self, _, spec) -> str: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L389)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L389?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.apply_directive_tree" class="docs-object-method">&nbsp;</a> 
```python
apply_directive_tree(self, _, spec) -> str: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L395)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L395?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.apply_assignment" class="docs-object-method">&nbsp;</a> 
```python
apply_assignment(self, key, spec) -> str: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L397)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L397?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.apply_raw" class="docs-object-method">&nbsp;</a> 
```python
apply_raw(self, key, spec) -> str: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L401)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L401?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.apply_comment" class="docs-object-method">&nbsp;</a> 
```python
apply_comment(self, key, spec) -> str: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L403)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L403?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.apply_directive" class="docs-object-method">&nbsp;</a> 
```python
apply_directive(self, key, spec) -> str: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L405)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L405?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.format_field" class="docs-object-method">&nbsp;</a> 
```python
format_field(self, value: Any, format_spec: str) -> str: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L410)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L410?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.load_template" class="docs-object-method">&nbsp;</a> 
```python
load_template(self, template): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L427)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L427?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.vformat" class="docs-object-method">&nbsp;</a> 
```python
vformat(self, format_string: str, args: Sequence[Any], kwargs: Mapping[str, Any]): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L451)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L451?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/examples/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/examples/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/docs/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/docs/templates/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TemplateEngine/TemplateEngine.py#L359?message=Update%20Docs)   
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
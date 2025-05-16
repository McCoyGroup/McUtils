## <a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter">TemplateFormatter</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L360)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L360?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L371)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L371?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.format_parameters" class="docs-object-method">&nbsp;</a> 
```python
@property
format_parameters(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L374)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L374?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.templates" class="docs-object-method">&nbsp;</a> 
```python
@property
templates(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L377)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L377?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.special_callbacks" class="docs-object-method">&nbsp;</a> 
```python
@property
special_callbacks(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L380)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L380?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.callback_map" class="docs-object-method">&nbsp;</a> 
```python
@property
callback_map(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L383)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L383?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.apply_eval_tree" class="docs-object-method">&nbsp;</a> 
```python
apply_eval_tree(self, _, spec) -> str: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L390)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L390?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.apply_directive_tree" class="docs-object-method">&nbsp;</a> 
```python
apply_directive_tree(self, _, spec) -> str: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L396)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L396?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.apply_assignment" class="docs-object-method">&nbsp;</a> 
```python
apply_assignment(self, key, spec) -> str: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L398)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L398?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.apply_raw" class="docs-object-method">&nbsp;</a> 
```python
apply_raw(self, key, spec) -> str: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L402)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L402?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.apply_comment" class="docs-object-method">&nbsp;</a> 
```python
apply_comment(self, key, spec) -> str: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L404)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L404?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.apply_directive" class="docs-object-method">&nbsp;</a> 
```python
apply_directive(self, key, spec) -> str: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L406)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L406?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.format_field" class="docs-object-method">&nbsp;</a> 
```python
format_field(self, value: Any, format_spec: str) -> str: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L411)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L411?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.load_template" class="docs-object-method">&nbsp;</a> 
```python
load_template(self, template): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L428)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L428?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateFormatter.vformat" class="docs-object-method">&nbsp;</a> 
```python
vformat(self, format_string: str, args: Sequence[Any], kwargs: Mapping[str, Any]): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L452)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.py#L452?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L360?message=Update%20Docs)   
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